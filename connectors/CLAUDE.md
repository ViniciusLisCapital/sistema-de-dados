# connectors/ — Contexto para o Claude

Clientes de APIs externas usados pelos scripts de domínio (`domain/db/`). Cada connector é paramétrico — não tem lógica de negócio, só chamada de API + parsing.

### `connectors/ibge.py` — API de Agregados IBGE v3

Cliente paramétrico baseado em `view=flat`. Substituiu o antigo `ibge_get(url, start, end, freq)`.

```python
from connectors.ibge import IBGE

ibge = IBGE()
df = ibge.get(
    agregado=8888,
    variaveis=12606,
    classificacoes={544: "all"},
    localidades={"N1": "all"},
    periodos="last:24",    # ou "202401-202412", "all", (2024, 2024)
)
# date: Timestamp, value: float64, sentinels -> NaN
```

**Detalhes técnicos da API IBGE v3:**
- `periodos`: aceita `YYYYMM-YYYYMM`, `last:N`, `-N`, `all`. A tupla `(ano_ini, ano_fim)` usa metadados para inferir o sufixo correto.
- `view=flat`: primeiro item do array é sempre o cabeçalho — `_parse_flat` pula automaticamente.
- Frequência inferida do cabeçalho `D2N` (`"Mês"`, `"Trimestre"`, `"Trimestre Móvel"`, `"Semestre"`, `"Ano"`).
- `"trimestral móvel"` (PNAD) é mapeado para formato `YYYYMM` igual ao mensal.
- Retry: 6 tentativas, backoff 1s, respeita `Retry-After`.

### `connectors/bcb.py` — APIs SGS e Focus do BCB

```python
from connectors.bcb import BCB

bcb = BCB()

# SGS: últimos N meses
df = bcb.get_sgs_ultimos({"ibcbr_nsa": 24363, "ibcbr_sa": 24364}, n=36)

# SGS: por período ou histórico completo
df = bcb.get_sgs(series, start="01/01/2020")
df = bcb.get_sgs(series, start="all")   # série histórica completa desde o início

# Focus/Olinda — uma serie especifica
df = bcb.get_focus(
    endpoint="ExpectativasMercadoInflacao12Meses",
    indicador="IPCA",
    campos=["Data", "Media", "Mediana", "DesvioPadrao"],
    start="2020-01-01",
    filtros_extras="Suavizada eq 'S' and baseCalculo eq 0",
)
# colunas em snake_case, date como Timestamp

# Focus/Olinda — endpoint inteiro numa janela de datas (indicador/campos opcionais)
df = bcb.get_focus(
    "ExpectativaMercadoMensais",
    start="2025-06-01", end="2025-06-30",
    filtros_extras="baseCalculo eq 0",
)
# todos os indicadores, todos os campos do recurso
```

**Detalhes técnicos:**
- SGS: `/ultimos/{n}` tem limite ~24 — `get_sgs_ultimos` usa `/dados?dataInicial=...` calculando a data.
- SGS `start="all"` mapeia para `"01/01/1970"` internamente; a API retorna desde o início real da série.
- Focus: URL deve ter `$` literal — `requests(params={})` percent-encoda para `%24` e a API rejeita. URL é construída manualmente.
- `$count` não suportado pelo endpoint Focus do BCB — paginação por `$skip` até `len(page) < page_size`.
  **Paginar história longa com `$skip` crescente é lento e não é seguro**: o `$orderby=Data` não tem
  desempate, então a ordem entre linhas da mesma data não é garantida entre páginas. Os scripts de
  `expc_focus*` varrem por janela de **um mês** em vez de paginar o histórico inteiro — o endpoint
  mais denso (`ExpectativaMercadoMensais`) dá ~4.200 linhas/mês contra o `$top` de 5.000, então na
  prática o skip nunca sai de zero. Ver `domain/db/brasil/bcb/_focus_core.py`.
- `indicador` e `campos` são opcionais: omitir `indicador` varre o endpoint inteiro (mais barato que
  uma chamada por indicador quando são dezenas); omitir `campos` traz todos os campos do recurso.
  `end=` fecha a janela do outro lado do `start=`.
- `ExpectativasMercadoSelic` não tem campo `Suavizada` — filtro diferente de inflação. Ele devolve
  **uma linha por reunião do Copom** (~16 por data de pesquisa), no campo `Reuniao` — não é um valor
  por data, e tratar como se fosse foi o bug que a tabela `expc_focus` carregou até 2026-08.
- **`baseCalculo`** (documentação oficial do serviço, `/aplicacao`): `0` = usa as submissões mais
  recentes de cada instituição a partir do **30º dia anterior** ao cálculo; `1` = a partir do **4º dia
  útil anterior**. Não são duas pesquisas — é a mesma com dois prazos de validade. Base 0 é ampla mas
  carrega expectativa velha, base 1 é fresca mas magra (135 vs. 62 respondentes no IPCA 12m de
  2026-08-14). `Suavizada` S/N existe **só** nos endpoints `Inflacao12Meses`/`24Meses`; `tipoCalculo`
  (C/M/L, ou `CURTO_/MEDIO_/LONGO_PRAZO` nos de inflação) existe **só** nos endpoints Top5.
- **A pesquisa foi reformulada quatro vezes** e as séries têm início/fim descontínuos: 2018-07-05
  encerra Top5 IGP-DI; **2021-02-17 encerra a família antiga de índices de preços** (IGP-DI, INPC,
  IPA-DI, IPA-M, IPC-Fipe, IPCA-15) em todos os endpoints; **2021-09-13→14** troca em um dia (sai
  "Produção industrial" e saem PIB Agropecuária/Indústria/Serviços do endpoint *trimestral* — as
  versões *anuais* seguem vivas —, entram os 5 componentes do IPCA, Taxa de desocupação, os
  componentes de demanda do PIB e Câmbio/IPCA trimestrais); 2026-01-29 encerra Top5 IGP-M e Top5 IPCA
  Administrados. Medir antes de assumir que uma série cobre o histórico inteiro.
- Paralelismo: `ThreadPoolExecutor` para múltiplas séries SGS simultâneas.

### `connectors/bcb_agenda.py` — Agenda de divulgações do BCB (feeds ICS)

```python
from connectors.bcb_agenda import BCBAgenda

ag = BCBAgenda()

ag.listas()       # 29 listas de calendario: {lista, categorias, link, e_evento}
ag.categorias()   # 14 categorias (Copom, Estatisticas, Sondagens do BC, ...)

ag.eventos("Sondagens - PTC PEF", start="2026-08-01", end="2026-12-31",
           summary_contains="PTC")
# [{'date': date(2026,8,20), 'time': '14:30', 'summary': '...', 'date_end': None}]

ag.ics("Focus")   # texto cru do .ics
```

**Detalhes técnicos** (confirmados ao vivo em 2026-08-17):
- **Os feeds trazem HORA de divulgação**, em `DTSTART;TZID=America/Sao_Paulo` — fuso declarado pela
  fonte, não inferido, e é o que `domain/release_calendar/` usa para não cobrar o dado antes do
  anúncio. Medido lista por lista em 2026-08-24: PTC e IC-Br 14:30, notas de estatísticas e Focus
  08:30, IBC-Br 09:00, ata do Copom e RPM 08:00. **A hora muda de era** (as notas de estatísticas
  saíram de 10:30 em 2019 para 09:30 e depois 08:30 em 2023), então ela é propriedade do evento, não
  da lista. A exceção é `Reuniões do Copom`: emite `00:00` nas 16 reuniões de 2026, que é placeholder
  de evento de dia inteiro e não meia-noite (a decisão sai perto das 18:30) — quem consome tem que
  descartar, não gravar.
- `/api/exportarics/sitebcb/agendaics?lista=<Nome>` devolve `.ics` real, mas o horizonte é curto e
  em geral **preso ao ano corrente** — medido em 2026-08-17: 7 das 10 listas do calendário paravam em
  dez/2026, IBC-Br/ICBr chegavam a fev/2027, e só `Reuniões do Copom` ia a dez/2027 (publicado com
  anos de antecedência por norma). Uma versão anterior desta nota dizia "~18 meses para frente" — está
  errado, medir antes de assumir. **Não** é a rota `/acessoinformacao/calendariobc_ics`, que é SPA
  Angular e cujo conteúdo está morto no backend (`/api/pagina/sitebcb/calendariobc[_ics]` retorna
  stub SharePoint "File Not Found"). A página renderiza no browser porque o Angular monta o
  seletor a partir dos endpoints de serviço abaixo, não do conteúdo da página — daí a confusão de
  "abre no meu browser mas não pra você".
- **Os nomes de `lista` são enumeráveis** — não chutar. `listas()` usa
  `/api/servico/sitebcb/calendario/catassociado?lista=CalendariosAssociacaoCategorias`; os dois
  nomes de lista do SharePoint saíram do bundle Angular (`calendario-card.component-*.js`, que
  hardcoda `identificador="calendario"`). Há também `/selecionacatassociado`, que exige
  `&categoria=<nome>` e dá 500 sem ele — `catassociado` sem categoria já traz tudo.
- **Não exigem headers de browser**, ao contrário de outros `/api/servico/sitebcb/*` (copom/atas,
  rpm): testado com User-Agent genérico e sem User-Agent nenhum, ambos HTTP 200.
- Uma lista pode misturar divulgações diferentes — `Sondagens - PTC PEF` traz PTC e PEF,
  `Estatísticas macroeconômicas` traz 4 pesquisas trimestrais. Daí `summary_contains`.
- O feed do Copom emite os **dois dias** da reunião como eventos separados (00:00, sem DTEND);
  quem pareia é `domain/release_calendar/update_calendar.py`.
- Parsing próprio de ICS (sem dependência nova). Faz unfolding do RFC 5545 — linha continuada
  começa com espaço/tab — senão um SUMMARY longo vira dois e perde metade. Aceita
  `DTSTART;TZID=...:20260817T090000` e `DTSTART;VALUE=DATE:20260817`.
- Retorna `list[dict]`, não DataFrame como os outros connectors: é metadado de calendário, não
  série temporal, e o consumidor escreve YAML.
- Único consumidor: `domain/release_calendar/update_calendar.py`.

### `connectors/bcb_copom.py` — comunicados do Copom (JSON com HTML)

```python
from connectors import bcb_copom

c = bcb_copom.comunicado(280)          # None se a reuniao nao existe no endpoint
c.data_referencia, c.titulo            # '2026-08-05', 'Copom reduz a taxa Selic para 14,00% a.a.'
c.markdown()                           # texto em markdown + cabecalho de procedencia
c.nome_arquivo()                       # 'copom_280_comunicado_2026-08-05.md'

bcb_copom.ultima_reuniao()             # 280 (sobe de um chute ate achar o vazio)
for nro, c in bcb_copom.intervalo(48): ...   # itera o historico, gentil com o servidor

bcb_copom.calendario_reunioes()        # {21: '1998-01-28', ..., 280: '2026-08-05'} -- UMA chamada
```

**`calendario_reunioes()` vem da listagem de ATAS, não dos comunicados** (`api/servico/sitebcb/
atascopom/ultimas`), e é por isso que existe: cobre **260 reuniões desde a 21ª (1998-01-28)**, contra
233 dos comunicados, que só respondem da 48ª em diante. É a única fonte do projeto para o número das
reuniões de 1998-2000, e o que permite ligar uma edição do RPM à reunião que a condiciona sem inferir
numeração. Inclui as **extraordinárias** (a 28ª, de 1998-09-10), que entram na mesma sequência. Só
número e data — o PDF da ata não está no pipeline.

**Detalhes técnicos** (medidos ao vivo em 2026-08, varrendo as reuniões 1–281):
- `api/servico/sitebcb/copom/comunicados_detalhes?nro_reuniao=N`, sem autenticação. Endpoint não
  documentado, mas é o que o próprio site do BCB consome. Melhor que raspar a página: a **Tabela 1**
  (projeções de inflação no cenário de referência) vem como `<table>` estruturada.
- **Cobertura: reunião 48 (2000-06-20) → 280.** De 47 para trás devolve `conteudo: []`, sem erro.
- **O servidor é instável** — timeouts esporádicos (WinError 10060) em requisições isoladas. `_get()`
  tenta 3× com backoff; uma varredura completa do histórico sem isso falha no meio.
- **`html_para_markdown()` não é conversor genérico** — resolve as quatro formas que o BCB usa:
  `<p>`, `<ul>/<ol>`, `<table>` e ênfase inline. As listas **não** são opcionais: os comunicados de
  2020-2023 põem as observações de cenário — e com elas as projeções — em `<li>`, e uma primeira
  versão que só lia `<p>` perdeu 24 reuniões de dados sem erro nenhum.
- Texto com lixo de editor SharePoint: NBSP, zero-width space no início de parágrafo, entidades
  numéricas (`&#58;`), parágrafos-espaçador `<p><strong> </strong></p>`. Tudo limpo na conversão.
- **As atas não saem por aqui.** São PDF, listadas em
  `api/servico/sitebcb/atascopom/ultimas?quantidade=N&filtro=`, com o caminho no campo `Url`.
  Não implementado.
- Consumidor: `domain/db/brasil/bcb/_copom_texto.py` → `pm_copom_projecoes.py`. Panorama da fonte
  por era em [`domain/db/brasil/bcb/copom_comunicados.md`](../domain/db/brasil/bcb/copom_comunicados.md).

### `connectors/bcb_tabelas_especiais.py` — "Tabelas especiais" de estatísticas fiscais do BCB (xlsx)

```python
from connectors.bcb_tabelas_especiais import TabelasEspeciais

te = TabelasEspeciais()
sheets = te.read_sheets("Facdetp.xlsx")             # todas as abas, header=None
sheets = te.read_sheets("Facdetp.xlsx", ["Juros"])  # só uma aba
```

**Detalhes técnicos** (confirmados ao vivo em 2026-08):
- Fonte é uma pasta de conteúdo estático: `https://www.bcb.gov.br/content/estatisticas/Documents/Tabelas_especiais/{arquivo}`.
  Nome de arquivo **fixo** — o BCB sobrescreve o mesmo arquivo a cada divulgação mensal. Ao contrário
  da EFGG (`tesouro_efgg.py`), não há `id` variável para resolver, então não precisa parse de HTML.
- **Não há listagem de diretório** e a página de Estatísticas Fiscais é SPA Angular (`requests`/WebFetch
  trazem só o shell, sem os links) — um nome novo se descobre por tentativa direta. A pasta responde
  200 para nome válido e 404 para inválido; `download()` levanta com mensagem explícita no 404.
- Retorna abas cruas (`header=None`), igual a `tesouro_efgg.py` — parsing de cabeçalho/hierarquia é
  responsabilidade do script de domínio.
- Único consumidor hoje: `domain/db/brasil/bcb/fisc_dlsp_fatores.py` (`Facdetp.xlsx`, fatores
  condicionantes da DLSP). Esses dados **não existem no SGS** — foi por isso que o connector nasceu.

### `connectors/bcb_rpm.py` — anexo estatístico do RPM (xlsx trimestral)

```python
from connectors.bcb_rpm import AnexoRPM

anexo = AnexoRPM()
vintages = anexo.vintages_disponiveis()      # [date(2021,9,1), ..., date(2026,6,1)]
wb = anexo.abrir(vintages[-1])               # openpyxl read-only (150+ abas)
ws, titulo = anexo.localizar_aba(wb, r"^grafico 2\.2\.\d+ .*hiato do produto")
grade = anexo.grade(ws)                       # DataFrame cru, header=None
```

**O módulo também serve o RELATÓRIO em si, não só o anexo** (adicionado 2026-08):

```python
from connectors.bcb_rpm import edicoes, baixar_pdf

eds = edicoes()                # 109 edicoes, 1999-06 -> 2026-06, sem buraco, UMA requisicao
eds[-1].ano_mes, eds[-1].vintage, eds[-1].url_pdf, eds[-1].nome_arquivo
pdf_bytes = baixar_pdf(eds[-1])   # 3 tentativas com backoff -- o CDN da timeout esporadico
```

A coleção do endpoint chama-se **`rpm`** e devolve a série inteira desde 1999-06, inclusive as edições
publicadas quando o relatório ainda se chamava RI. A coleção irmã `ri` é **subconjunto** (para em
2024-12) e não serve. Descoberto por tentativa: `relatorioinflacao`,
`relatoriopoliticamonetaria` e variantes dão **400**.

Isso resolve a descoberta do **relatório**; não a do **anexo**, que a listagem não menciona e que só
existe de 2021-09 em diante — por isso a enumeração de URLs do `AnexoRPM` continua necessária.

**Gotcha do PDF**: a extração de texto tem cinco armadilhas silenciosas (coluna central que muda de
lugar, separador ano/trimestre que muda, layout de 2 colunas que perde tabela larga ou linha de
tabela, fonte de subconjunto sem cmap, rótulo de cenário que troca de significado). Todas
documentadas em
[`domain/db/brasil/bcb/relatorio_politica_monetaria.md`](../domain/db/brasil/bcb/relatorio_politica_monetaria.md)
— ler antes de escrever qualquer parser novo sobre estes PDFs.

A planilha que o BCB publica junto do Relatório de Política Monetária com os dados por trás de
**cada gráfico e tabela** do relatório — uma aba por figura, 130-190 abas por edição.

**A unidade aqui é a EDIÇÃO, não a série** (é o que diferencia este connector de todos os outros):
cada trimestre republica a série inteira revisada, então o mesmo trimestre do calendário tem um
valor diferente em cada edição. Nenhuma outra fonte do projeto diz o que o BCB *achava* na época.

**Detalhes** (confirmados ao vivo em 2026-08, varrendo 2014-03 → 2026-06):
- URL: `…/content/ri/relatorioinflacao/{AAAAMM}/{prefixo}{AAAAMM}anp.xlsx`. O prefixo muda no meio
  da série — `ri` até 2024-12, `rpm` de 2025-03 (o relatório foi renomeado). `url_de()` tenta o
  outro prefixo no 404, então uma renomeação futura não quebra a descoberta.
- **Série começa em 2021-09.** O relatório existe desde 1999, mas passou a publicar anexo de dados
  só nessa edição — antes disso os números são imagem de gráfico no PDF.
- Sem listagem de diretório e a página é SPA: `vintages_disponiveis()` **enumera** os trimestres
  candidatos e testa cada URL com um GET de 2 bytes (`Range: bytes=0-1`). HEAD não é usado — nem
  todo caminho do CDN do BCB responde a ele.
- **Localizar aba por nome é furado**: o número do gráfico anda a cada edição (o hiato já foi
  `Graf 2.2.3`, `2.2.4`, `2.2.6`, `2.2.8`). `localizar_aba()` casa um regex contra o bloco de
  cabeçalho da coluna A, onde vive o título publicado.
- Devolve grade crua (`header=None`), igual a `bcb_tabelas_especiais.py` — cada figura do anexo tem
  uma forma diferente e o parsing fica no script de domínio.
- Consumidores hoje: `domain/db/brasil/bcb/pm_hiato_produto.py` e `pm_hiato_produto_vintages.py`,
  ambos via o parser compartilhado `domain/db/brasil/bcb/_rpm_hiato.py` (que documenta as cinco
  armadilhas da aba do hiato — vale ler antes de adicionar a 3ª série deste anexo); e
  `cred_fluxo_financeiro.py`, que lê o gráfico recorrente de **fluxo financeiro do crédito** e, pelo
  trecho 2015-2017, o boxe de 2025-03. Duas lições dele que valem para qualquer série nova daqui:
  **o mesmo gráfico muda de unidade entre eras** (o fluxo saía em R$ deflacionados até a edição
  2025-12 e passou a % do PIB na 2026-03 — só a segunda encadeia entre edições, e o padrão de título
  exige o "acumulado em 12 meses" justamente para levantar em vez de carregar R$ como se fosse %); e
  **emendar duas fontes do anexo só é seguro se as duas publicarem o MESMO conjunto de séries** —
  onde o boxe publica um nível a mais que o gráfico recorrente, a edição nova sobrepõe o pai e não o
  filho, e a hierarquia deixa de fechar.

### `connectors/fred.py` — API FRED (Federal Reserve)

```python
from connectors.fred import FredUniFrame, FredMultFrame

# Série única
df = FredUniFrame("PCE", "PCEPI", "2010-01-01", "2024-12-31")
# colunas: Date, <NameSerie>

# Múltiplas séries (wide ou unpivoted)
df = FredMultFrame({"PCE": "PCEPI", "CPI": "CPIAUCSL"}, "2010-01-01", "2024-12-31")
df_long = FredMultFrame({...}, start, end, Pivot=True)
```

**Detalhes:**
- API key via `FRED_API_KEY` no `.env` — nunca hardcoded.
- `US_IndexNormalize`: expande dados trimestrais para mensais via merge com CPI e `ffill(limit=2)`.

### `connectors/bls.py` — BLS (Bureau of Labor Statistics)

Reescrito em 2026-08 a partir do stub morto que vivia em `not_in_production/` (chave hardcoded
e inválida, path absoluto de Dropbox inexistente, `int(period[1:])` estourando em `M13`).
**Três caminhos de acesso com papéis diferentes** — a escolha entre eles não é estilística:

```python
from connectors.bls import BLS

bls = BLS()                                   # chave opcional (BLS_API_KEY)

# 1. API — atualização incremental, qualquer pesquisa do BLS
df = bls.get_series(["CUSR0000SA0", "CUSR0000SA0L1E"], 2000, 2026)
# colunas: date (Timestamp, dia 1), series_id, value, period ("M01".."M13", "S01".."S03")

# 2. Arquivos brutos — backfill e dimensões, sem chave e sem cota
itens    = bls.get_item_tree("cu")            # 400 itens, display_level 0-8
catalogo = bls.get_series_catalog("cu")       # 8.104 séries com begin_year/end_year
hist     = bls.get_data_file("cu", "cu.data.1.AllItems")   # 1913→hoje numa requisição

# 3. Importância relativa (pesos) — nem na API nem nos arquivos brutos
pesos = bls.get_relative_importance(2025)     # long: section/indent_level/item_name/area/population/weight
```

**Chave de API — opcional, mas os limites mudam.** `BLS_API_KEY` no `.env` (registro gratuito e
imediato em https://data.bls.gov/registrationEngine/) — **configurada desde 2026-08-18**. Sem chave a
v2 responde normalmente, com os limites da v1: **25 séries / 10 anos / 25 requisições por dia**, e
`catalog`/`calculations` desabilitados (o BLS avisa em `message[]` e ignora os flags). Com chave:
**50 séries / 20 anos / 500 requisições**. Os limites por requisição das duas situações foram
**medidos ao vivo** (51 séries → aviso "limit of 50 series"; 21 anos → aviso "limit of 20 years"); só
a cota diária segue documentada-e-não-medida, porque o BLS não expõe contador de uso.
`calculations=True` passou a funcionar e devolve as variações de 1/3/6/12 meses calculadas pelo
próprio BLS em cada observação; `catalog=True` devolve survey/área/item/sazonalidade por série.

**Detalhes e armadilhas** (todas verificadas ao vivo):
- **A degradação sem chave é silenciosa e a janela truncada é a ERRADA.** Pedir 1990-2026 devolve
  `REQUEST_SUCCEEDED` com **1990-1999**: o truncamento ancora no `startyear` e avança 10 anos, não
  pega os 10 anos mais recentes. O connector fatia séries e anos antes de chamar e trata qualquer
  aviso de truncamento como `BLSTruncationError` — se o limite real divergir de `_LIMITS`, estoura
  em vez de devolver janela errada.
- **Id inválido também volta com `REQUEST_SUCCEEDED`**, só com `"Invalid Series for Series X"` em
  `message[]` e a série presente porém vazia. `get_series(strict=True)` (default) levanta;
  `strict=False` avisa e devolve o resto.
- **`M13` não é um mês.** O BLS intercala médias no meio da própria série: `M13`/`S03` = média anual,
  `A01` = anual. `get_series`/`get_data_file` filtram por default (`include_aggregates=True` mantém).
  **`S01`/`S02` (semestres) são caso diferente e NÃO são filtrados**: são a frequência real de séries
  que o BLS só publica semestralmente — em `cu.data.1.AllItems`, 100 das 201 séries são semestrais e
  101 mensais, e nenhuma tem as duas (conferido ao vivo). Filtrá-las apagaria dado legítimo; use a
  coluna `period` para separar frequências antes de plotar.
- **Os arquivos brutos são o caminho de backfill, não a API.** `cu.data.1.AllItems` traz 54.380
  observações de 201 séries (CPI-U NSA desde 1913) numa requisição sem cota; a mesma janela pela API
  custaria 12 requisições — metade da cota diária sem chave. `get_series` avisa quando a chamada
  planejada excede a cota. **Cruzado ao vivo: API e arquivo bruto batem exatamente** (319 meses de
  `CUSR0000SA0`, diferença máxima 0.0).
- **`download.bls.gov` recusa o User-Agent default do `requests`** e serve página de erro com HTTP
  200 em path inválido — `get_flat_file()` manda UA identificável e checa o corpo, não o status.
- **Importância relativa: xlsx por ano, e o ano do arquivo não é o ano dos pesos.** `2025.xlsx` diz
  "(2024 Weights) ... December 2025" — cesta de 2024 a preço de dez/2025; `weights_year` e
  `reference_period` leem os dois rótulos do arquivo. O rótulo de peso só existe de 2022 em diante
  (antes a cesta era bienal e `weights_year` volta `None`). Publicados: **2020-2025**, mais
  `historical-relative-importance-1947-1986.xlsx` e um zip de 1987-1989 — **1990-2019 não tem xlsx
  nessa página**.
- **Cada tabela de pesos empilha várias árvores independentes**, separadas pela coluna `section`:
  na Table 1, "Expenditure category" (294 itens, soma 100 no nível 1) e "Special aggregate indexes"
  (cortes sobrepostos — "All items less food and energy", "Services less energy services" — que
  somam 664). Somar sem filtrar `section` dá 764. As tabelas 2-6 são grades área × população com
  2-3 linhas de header e células mescladas; por isso o retorno é sempre long. Identidade conferida
  nas 7 abas: a árvore de despesa soma 100 em cada par (área, população), 84 checagens, desvio
  máximo 0.002 (arredondamento do próprio arquivo).
- **Os pesos são chaveados por NOME de item + nível de indentação, não por `item_code`** — juntar
  com `get_item_tree()` exige casamento por nome. É o custo de o BLS publicar peso só em tabela de
  divulgação, e é o passo que falta para montar o par `inflc_decomposicao`/`inflc_dim` do lado US.
- **A API é genérica por pesquisa**: CPI (`cu`/`cw`/`su`), PPI (`wp`/`pc`), CES (`ce`), CPS (`ln`),
  JOLTS (`jt`) e preços de importação/exportação (`ei`) respondem na mesma chamada — testado ao
  vivo com uma requisição cobrindo as cinco. Um connector serve inflação, mercado de trabalho e
  parte do setor externo.
- **Mas nem sempre a API é o caminho certo, e o JOLTS é o contra-exemplo medido** (2026-09-01): as 913
  séries úteis da pesquisa `jt` são **19 requisições** de API por janela de 20 anos contra **uma**
  requisição de 34 MB (`get_data_file("jt", "jt.data.1.AllItems")`) que traz a história inteira em
  1,6 s e não gasta cota nenhuma. O dump venceu nas duas pontas — backfill e rotina —, e a API ficou
  como **conferência de vintage**: 10 séries de manchete em 2 anos, uma requisição, e qualquer
  divergência levanta em vez de gravar um mês atrasado em silêncio. A regra que sai disso: compare o
  número de requisições contra o tamanho do dump antes de escolher; para uma pesquisa pequena e larga
  (muitas séries, história curta) o dump ganha, e o inverso do `inflc_cpi`, onde a janela de rotina é
  estreita e a série é longuíssima, é o que faz a API ganhar lá.
- **O layout do `series_id` tem largura fixa e errar a contagem devolve `None`, não erro.** No JOLTS
  são 21 caracteres — `JT` + S/U + indústria(6) + estado(2) + área(5) + tamanho(2) + medida(2) + L/R —
  e uma primeira tentativa com 19 fez as 168 células da Tabela A voltarem vazias, o que se lê como
  "o dado não existe" e não como "o id está errado". `mt_jolts_dim.series_id()` valida o comprimento
  antes de devolver; vale copiar o padrão para qualquer pesquisa nova do BLS.

### `connectors/bea.py` — BEA (Bureau of Economic Analysis)

**Duas portas para o mesmo dado**, e o connector serve as duas: o **xlsx** de release (sem chave, sem
cota) e a **API** (`BEA_API_KEY` no `.env`, dataset `NIUnderlyingDetail`). A escolha inicial pelo xlsx
foi por conveniência — só não pedia chave —, e desde 2026-08-26, com a chave instalada, as duas foram
medidas uma contra a outra. O resultado divide o problema em dois, e é por isso que nenhuma das duas
foi descartada:

- **Nos valores a API é melhor, e as duas concordam exatamente.** `tests/test_bea_api.py` confere valor
  a valor: **608.442 observações** (as duas tabelas, 1959-01→hoje), **0 diferentes, diferença máxima
  0**, nada existindo só de um lado, rótulos idênticos após a mesma `_limpar_rotulo()`. A API entrega
  número tipado, sem depender de `"Line"` na célula A8, de 2 espaços por nível, de `.....` como ausente
  nem de nota de rodapé no fim da coluna A — camada de apresentação que um reformat cosmético do BEA
  quebraria. A conferência é o que torna esse risco medido em vez de retórico, igual ao que `bls.py`
  faz entre API e arquivo bruto.
- **Na estrutura a API não serve: não publica hierarquia nenhuma.** Medido no registro de `GetData`:
  **10** campos (TableName, SeriesCode, LineNumber, LineDescription, TimePeriod, METRIC_NAME, CL_UNIT,
  UNIT_MULT, DataValue, NoteRef) e nenhum é pai, nível ou indentação; `LineDescription` vem **sem** os
  espaços da coluna B e `LineNumber` é ordem, não profundidade. Daí `TabelaNipa.fonte`: `inflc_pce_dim`
  exige `"xlsx"` e levanta se receber `"api"`, senão a árvore sairia toda no nível 0 sem exceção
  nenhuma.
- **Duas divergências entre o guia oficial (69 páginas, abr/2026) e a API real**, ambas medidas: o campo
  é `METRIC_NAME` em maiúsculas (o guia escreve `Metric_Name`) e há um 10º campo, `NoteRef`, que o guia
  não lista. "vintage" aparece **zero** vezes no guia — uma versão anterior desta nota dizia que a chave
  serviria para vintages, sem base.
- **Erro vem com HTTP 200**, em **um de dois** nós: `BEAAPI.Error` (tabela/frequência/ano inválidos) ou
  `BEAAPI.Results.Error` (chave inválida ou vazia). Olhar só um deixa o outro passar como resposta
  válida e vazia. E a resposta **ecoa a chave** em `Request.RequestParam` — nunca colocar o corpo cru
  num log ou numa mensagem de erro.
- **Limites.** Documentados: 100 req/min, 100 MB/min, 30 erros/min, timeout de 1 min. Medido: `Year=X`
  traz a série inteira numa requisição (75 MB, 303.410 registros, 10-20s), e as duas tabelas seguidas
  (150 MB em ~40s) passaram sem estrangulamento. `IncompleteRead` acontece e **não** é limite de
  tamanho — é truncamento de conexão, então `_get_api` repete até 4 vezes. O xlsx não tem cota — a
  única dimensão em que ele ganha.

```python
from connectors.bea import (ler_tabela, ler_tabela_api, conferir_api_xlsx,
                            ABA_PCE_INDICE, ABA_PCE_NOMINAL, ABA_PARA_TABELA)

t = ler_tabela(ABA_PCE_INDICE)     # "U20404-M" = tabela 2.4.4U, mensal (xlsx)
t.titulo, t.unidade, t.periodo, t.publicado_em, t.sazonalidade   # metadados do arquivo
t.periodos                          # ['1959M01', ..., '2026M07']
t.estrutura                         # linha, code, rotulo, rotulo_bruto, indentacao
t.observacoes                       # long: linha, date (dia 1), value
t.fonte                             # "xlsx"

a = ler_tabela_api("U20404")        # mesmo retorno pela API; anos="X" = tudo
a.fonte                             # "api" -- e estrutura["indentacao"] toda nula
conferir_api_xlsx(ABA_PCE_INDICE)   # dict: n_comum, n_diferentes, dif_max, ...

anos_param(2024, 2026)              # "2024,2025,2026" -- a API manda so a janela pedida
caminho_cache_hoje()                # o xlsx de hoje ja em disco, ou None (nao baixa)
```

**Quem usa qual porta:** `inflc_pce` (valores) carrega pela **API** desde 2026-08-26 — é o contrato
melhor e só transfere a janela pedida, então a rotina de 3 anos custa ~6 MB contra os 12 MB fixos do
xlsx. `inflc_pce_dim` (árvore) **também roda só de API no passe de rotina**, apesar de a hierarquia só
existir no xlsx: ela é gravada uma vez e depois relida do MySQL, com a API provando que continua válida
(mesmo conjunto de linhas + aditividade em nominal sobre o parentesco gravado). O xlsx é baixado só
quando essa prova falha, e `ler_tabela_api` continua marcando `fonte="api"` justamente para o
`inflc_pce_dim` recusar montar árvore de lá.

Duas armadilhas medidas, ambas custaram uma rodada:

- **A API devolve registro só onde há dado**, então `ler_tabela_api(anos=...)` numa janela curta traz
  `estrutura` com MENOS linhas: faltam as 2 `ZZZZZZ` (sem índice de preço em janela nenhuma) e as
  descontinuadas (157/158, terminadas em 2001-12). Ausência não é remoção — só é, se a cobertura
  gravada disser que a linha deveria estar publicando.
- **O `SeriesCode` codifica a medida**: a linha 1 é `DPCERG` na 2.4.4U e `DPCERC` na 2.4.5U. Comparar
  código entre as duas tabelas falha nas 402 linhas — que é exatamente por que
  `inflc_pce_dim._validar_casamento` sempre comparou linha/rótulo/indentação e nunca código.

Uma requisição de 12 MB (`Section2All_xls.xlsx`), cacheada por dia no temp do sistema
(`%TEMP%/lis_bea/`, não no repositório) e em memória por processo — os dois scripts de PCE rodam na mesma passada do `update_us.py` e não baixam duas vezes.

As abas (o nome é o número da tabela sem pontos + a frequência). As 7 tabelas do arquivo, todas SA (linhas e meses medidos, não da documentação):

| Aba | Tabela | Conteúdo | Linhas | Meses | Carregada |
|---|---|---|---|---|---|
| `U20404-M` | 2.4.4U | **Índice de preço** encadeado, 2017=100 | 402 | 810 | ✅ `inflc_pce`, `medida='indice'` |
| `U20405-M` | 2.4.5U | **Despesa nominal**, US$ mi SAAR | 402 | 810 | ✅ `inflc_pce`, `medida='nominal'` |
| `U20403-M` | 2.4.3U | PCE **real**, índices de quantidade | 402 | 810 | ❌ |
| `U20406-M` | 2.4.6U | PCE **real**, dólares encadeados | 402 | 234 | ❌ |
| `U20304-M` | 2.3.4U | Índice de preço, corte grosso | 46 | 810 | ❌ |
| `U20305-M` | 2.3.5U | Despesa nominal, corte grosso | 46 | 810 | ❌ |
| `U20306-M` | 2.3.6U | PCE real encadeado, corte grosso | 46 | 234 | ❌ |

`-A`/`-Q` são as mesmas tabelas em anual e trimestral.

**As `2.3.xU` NÃO são "o corte por função"** (uma versão anterior desta nota dizia isso e estava
errada, corrigido ao ler os títulos das abas): são *"by Major Type of Product **and** by Major
Function"*, 46 linhas — uma tabela grossa que mistura os dois critérios, não um espelho de 402 linhas
por função. A árvore detalhada por função é a **2.5.x**, que não está neste arquivo; a nota de rodapé
da 2.4.4U referencia as linhas da 2.5.4 exatamente porque é outra tabela.

**As 4 tabelas `2.4.xU` compartilham as mesmas 402 linhas**, então a árvore de `inflc_pce_dim` serve
para todas — adicionar quantidade ou encadeado é um `medida` novo, não uma dimensão nova.

**Detalhes e armadilhas** (todas verificadas ao vivo):
- **2.4.4U e 2.4.5U casam linha a linha** — as mesmas 402 linhas, na mesma ordem, com o mesmo rótulo e
  a mesma indentação. Preço e despesa se juntam pelo NÚMERO DA LINHA, sem casar nome, que é o oposto
  do lado do CPI (onde cinco itens sumiram por uma vírgula de diferença). `inflc_pce_dim` confere isso
  a cada carga e se recusa a gravar se deixar de valer.
- **A indentação é a hierarquia** (2 espaços por nível, coluna B) e é a única fonte de parentesco no
  arquivo — não há coluna de pai.
- **A linha 1 é indentada errado**: `Personal consumption expenditures` vem com 6 espaços e
  `Goods`/`Services` com 0. Cosmético do stub head. O connector devolve `indentacao` crua; quem monta
  a árvore trata a raiz.
- **O bloco de addenda não é árvore.** Nas linhas 369-402, `Market-based PCE` vem MAIS indentado que
  as linhas que ele encabeça. Inferir parentesco ali é inventar.
- **13 códigos aparecem em duas linhas cada** (a mesma série entra 2x na árvore, com pais diferentes).
  Valores idênticos nas duas posições, conferido série a série — por isso a chave é a linha.
- **`ZZZZZZ` não é código**, é o marcador de "não publico série para esta linha": as duas linhas de
  net (`Net expenditures abroad`, `Net foreign travel`) têm despesa e não têm índice de preço.
- **`.....` = não disponível** (vira ausência de linha em `observacoes`), e as últimas linhas do
  arquivo são notas de rodapé com texto na coluna A — descartadas porque o filtro exige número.
- **O rótulo publicado carrega ruído**: marcadores de nota (`\1\`) e referências cruzadas para a
  linha equivalente da tabela 2.5.4 (`(55)`, `(parts of 31, 33, and 36)`). 80 dos 402 rótulos têm um
  ou outro; saem de `rotulo` e o original fica em `rotulo_bruto`. Auditado: todo sufixo removido é
  referência cruzada ou nota, nenhum é parte do nome.
- **Só existe SA.** O mensal do BEA é dessazonalizado e não há contrapartida NSA destas tabelas. É da
  fonte, não da carga.
- **O parser levanta se o layout mudar** — exige `"Line"` na coluna A da linha 8 e períodos no formato
  `YYYYMnn`, e recusa um download menor que 1 MB (página de erro servida com HTTP 200).

### `connectors/us_agenda.py` — Agenda de divulgações do BLS e do BEA

Contrapartida americana do `bcb_agenda.py`. É daqui que saem as **datas e horas** que
`domain/release_calendar/` grava para `inflc_cpi` e `inflc_pce` (grupos `bls_cpi` e `bea_pce`).

```python
from connectors.us_agenda import BLSAgenda, BEAAgenda, FREDReleases

BLSAgenda().releases()            # 13 slugs com página de agenda (cpi, ppi, empsit, jolts, ...)
BLSAgenda().schedule("cpi")       # [{reference_period, date, time, tz}]  <- a única fonte com o período
BEAAgenda().eventos(summary_starts="Personal Income and Outlays")
FREDReleases().dates(10)          # conferência independente; release_for_series() descobre o id
```

**Três fontes porque nenhuma sozinha tem as três coisas** (data + hora + período de referência),
medido ao vivo em 2026-08-26:

| fonte | data | hora | período | horizonte |
|---|---|---|---|---|
| BLS, página por release (`/schedule/news_release/<slug>.htm`) | ✅ | ✅ | **✅** | ano corrente |
| BLS, feed ICS (`bls.ics`, 313 eventos) | ✅ | ✅ | ❌ | 2025-01 → 2026-12 |
| BEA, feed ICS (119 eventos) | ✅ | ✅ | **✅** | 2025-01 → 2026-12 |
| BEA, página de agenda (HTML) | ✅ | ✅ | ✅ | só o futuro (19 linhas) |
| FRED `/fred/release/dates` | ✅ | ❌ | ❌ | 1948 → agendado |

Daí: **no BLS a página é primária** (o ICS só tem o nome do release no `SUMMARY`, sem mês); **no BEA
o ICS é primário** (o período vem no próprio título, `"Personal Income and Outlays, August 2026"`); e
o **FRED é a terceira opinião** e o caminho de descoberta para série nova — 331 releases, e
`release_for_series("PPIACO")` devolve o id sem adivinhação.

Gotchas medidos, todos com custo real se ignorados:

- **`bls.gov` responde 403 a User-Agent genérico**, não só `download.bls.gov`. O módulo reusa o `_UA`
  de `connectors/bls.py`.
- **O TZID do ICS do BLS não é nome IANA**: `DTSTART;TZID=US-Eastern:...`, e `ZoneInfo("US-Eastern")`
  levanta. O bloco `VTIMEZONE` do arquivo declara as regras de `America/New_York` — daí o alias.
- **O ICS do BEA vem em UTC com `Z`, e é o `Z` que carrega o horário de verão**: `20260930T123000Z` é
  08:30 EDT e `20261125T133000Z` é 08:30 EST. Ler como ingênuo (o que `bcb_agenda._parse_dt` faz,
  correto para o BCB) erraria em 4-5 horas e mudaria até o dia em alguns eventos.
- **`APIDatasetMetaData` do BEA tem `ReleaseDate` e `NextReleaseDate` por tabela, e os dois estão
  congelados em 2019** — `MetaDataUpdated: 2019-03-06` nas 386 tabelas do NIPA, todas dizendo
  `NextReleaseDate: Mar 28 2019`. É o único campo da API do BEA que parece um calendário. Não usar.
- **A API v2 do BLS não tem endpoint de calendário** — os quatro que existem são `timeseries/data/`,
  `timeseries/popular`, `surveys` e `surveys/<id>`.
- **O `DTSTAMP` do ICS do BEA é inútil como sinal de frescor**: os 119 eventos, de 2025-01 a 2026-12,
  carregam todos `DTSTAMP:20250923T143030Z`. O conteúdo está em dia (conferido evento a evento contra
  o HTML ao vivo); o carimbo é que é de geração única.
- **Nenhuma das duas publicava 2027 em 2026-08-26** (os dois ICS terminam em dezembro/2026,
  `/schedule/2027/home.htm` é 404).
- **O release do FRED é um superconjunto**: um "release" lá é o conjunto de publicações que mexem
  naquelas séries, não um evento com título. O 54 inclui as divulgações trimestrais de PIB, que
  republicam o índice de preço do PCE — daí o FRED ter 2025-12-23 e a agenda do BEA, filtrada por
  título, não. A conferência é direcional por isso.

Testado por [`tests/test_us_agenda.py`](../tests/test_us_agenda.py): metade offline (os três formatos
acima contra fixtures) e metade ao vivo (as três fontes uma contra a outra, mais a conversão de fuso
nas duas pontas do ano).

### `connectors/bis.py` — BIS Statistics API v1

Sem autenticação. Três datasets SDMX-CSV expostos:

```python
from connectors.bis import BIS

bis = BIS()

# WS_EER — Effective Exchange Rates (REER/NEER)
df = bis.get_eer(countries=["BR", "MX", "CL", "CO"], types=[("R", "B"), ("N", "B")])
# colunas: date (month-start), country_code, reer_type (real_broad | nominal_broad | ...), value

# WS_CBPOL — Central Bank Policy Rates
df = bis.get_policy_rates(countries=["BR", "MX", "CL", "CO", "PE", "AR"], freq="D")
# colunas: date, country_code, value (% a.a.)

# WS_LONG_CPI — Consumer Prices (série longa)
df = bis.get_cpi(countries=["BR", "MX", "CL", "CO", "PE"], unit="yoy")
# colunas: date (month-start), country_code, value (% a.a., YoY)
```

**Detalhes técnicos:**
- Key SDMX difere por dataset: `WS_EER` é `FREQ.ADJUSTMENT.REF_AREA.BASKET` (4 dimensões); `WS_CBPOL` é
  `FREQ.REF_AREA` (2 dimensões); `WS_LONG_CPI` é `FREQ.REF_AREA.UNIT_MEASURE` (3 dimensões, `UNIT_MEASURE`
  `771`=YoY % ou `628`=índice 2010=100 — `get_cpi(unit=...)` aceita `"yoy"`/`"index"` ou o código direto).
- `WS_CBPOL` também expõe frequência mensal, mas é só o fechamento de mês da série diária — por isso a
  maioria dos scripts de domínio usa `freq="D"`; `cmb_real_rates.py` é a exceção, usa `freq="M"` para
  alinhar com o CPI (também mensal).
- Cuidado com o range de valores: Brasil na hiperinflação (1989-1994) chega a ~790.799% a.a. — coluna
  `value` no banco precisa de `decimal(12,4)`, não `decimal(8,4)`, em qualquer tabela que use `WS_CBPOL`
  sem truncar esse período.
- Argentina (`AR`) parou de ser atualizada pelo BIS em 2025-07 — gap esperado no fim da série, não é
  falha do connector/script. `WS_LONG_CPI` não cobre AR nos países acompanhados aqui (não testado).
- `WS_LONG_CPI` é live/atualizado mensalmente (cobre até o mês corrente, checado em 2026-08) — ao
  contrário do CPI de MX/CL/CO exposto no FRED (fonte OECD, descontinuado lá em 2023-2024) e de PE
  (sem série mensal alguma no FRED). Preferir `WS_LONG_CPI` a FRED para CPI desses 4 países.
- Retry: 4 tentativas, backoff 1s, respeita `Retry-After` (429/5xx).

### `connectors/yfinance.py` — Yahoo Finance (via pacote `yfinance`)

```python
from connectors.yfinance import get_history

df = get_history("DX-Y.NYB", start="1971-01-01")
# colunas: date, value (value = Close)
```

**Detalhes:**
- Usado por `domain/db/international/yfinance/cmb_dollar_index.py` (DXY) — historico desde 1971,
  bem mais longo que o equivalente FRED (`DTWEXBGS`, so cobre a partir de 2006).
- `end=None` (default) baixa ate a data atual.
- `yf.download` retorna colunas em MultiIndex (`Price`, `Ticker`) — `get_history` ja acha e renomeia.

### `connectors/tesouro.py` — RTN (Resultado do Tesouro Nacional)

```python
from connectors.tesouro import RTN

rtn = RTN()
df = rtn.get_series({"receita_total": "1.", "despesa_total": "4.", "resultado_nominal": "10."})
# date (Timestamp), name (str), value (float) — R$ milhoes, mensal desde 1997-01
```

**Detalhes técnicos:**
- Fonte: workbook "Resultado do Tesouro Nacional - Série Histórica - Mensal" (XLSX), publicado no
  CKAN da Tesouro Transparente. O nome do arquivo muda todo mês (ex: `seriehistoricamai26.xlsx`) —
  a URL de download é resolvida a cada chamada via `package_show` (dataset id
  `ab56485b-9c40-4efb-8563-9ce3e1973c4b`), nunca hardcoded.
- Lê a aba `"1.1"` (Resumida) do workbook, que é wide-format: coluna A = rótulo com prefixo
  hierárquico (ex: `"4.1  Benefícios Previdenciários"`), colunas B em diante = uma por mês.
  `get_series()` casa o **primeiro token** do rótulo (ex: `"4.1"`) contra o dict `line_items`
  passado — não por substring, para não confundir `"1."` com `"1.1"`/`"1.2"`.
- Linhas "abaixo da linha" (Ajustes Metodológicos, Juros Nominais, Resultado Nominal etc.) ficam
  tipicamente 1 mês defasadas em relação às linhas "acima da linha" (Receita, Despesa) — API do BCB
  atualiza com lag. `get_series()` já descarta (`dropna`) células vazias, então cada série retorna
  só até sua própria última leitura disponível, sem erro.
- API de séries temporais mencionada na documentação oficial (`apiapex.tesouro.gov.br/...`) redireciona
  em loop (`sisweb.tesouro.gov.br`, testado em 2026-08) — não usada; o download direto do XLSX via
  CKAN é o caminho confirmado funcionando.

### `connectors/tesouro_efgg.py` — EFGG (Estatisticas Fiscais do Governo Geral)

```python
from connectors.tesouro_efgg import EFGG

efgg = EFGG()
urls = efgg.get_current_urls()   # {"central": url, "estados": url, "municipios": url, "investimento_geral": url}
raw = efgg.download_table(urls["estados"], sheet_name="1.3")
# DataFrame cru (header=None) -- parsing por codigo GFSM fica no script de dominio
```

**Detalhes tecnicos** (achados investigando ao vivo em 2026-08, apos o usuario perguntar se a
classificacao GFSM/Governo Geral teria planilha, nao so boletim PDF -- pesquisa anterior, documentada
em `analytics/brasil/fiscal_policy/CLAUDE.md`, tinha concluido "so PDF" e estava errada/desatualizada):
- Pagina fixa (`_PAGE_URL`, `tesourotransparente.gov.br/publicacoes/estatisticas-fiscais-do-governo-
  geral/2021/22`) cujo conteudo e sobrescrito a cada publicacao trimestral nova -- mesmo padrao das
  "tabelas especiais" do BCB. **E HTML puro (Plone), nao SPA** -- confirmado com `requests` simples,
  sem headless browser (suspeita inicial de que precisaria de Playwright estava errada).
- Os 4 anexos xlsx (`demonstrativos_governo_central_orcamentario.xlsx`,
  `..._governos_estaduais.xlsx`, `..._governos_municipais.xlsx`,
  `..._investimento_governo_geral.xlsx`) tem um `id` numerico
  (`thot-arquivos.tesouro.gov.br/publicacao-anexo/{id}`) que muda a cada trimestre -- resolvido a cada
  chamada via parse do `<a title="...">` na pagina fixa, nunca hardcoded.
- Sem autenticacao.
- Metodologia GFSM 2014 do FMI, harmonizada com o SNA 2008/IBGE — e a mesma fonte que o paper do IEG
  (Impulso Estrutural do Gasto, Resende & Pires 2024) usa. Ver
  `analytics/brasil/fiscal_policy/reference/rtn_vs_efgg.md` para a diferenciacao completa vs. a RTN
  (`connectors/tesouro.py`), o mapeamento de codigos e a validacao de que Central+Estados+Municipios
  somam exatamente ao arquivo consolidado de Governo Geral.
- Cada esfera tem seu proprio nome de aba para a despesa trimestral: Governo Central e `"2.3"` (tem
  tambem uma versao mensal, `"1.3"`, que este connector nao usa -- ver docstring de
  `domain/db/brasil/tesouro/fisc_efgg.py`); Estados/Municipios so tem trimestral, na aba `"1.3"`.

### `connectors/pdet_ftp.py` — FTP do PDET/MTE (microdados do Novo CAGED)

```python
from connectors.pdet_ftp import baixar_7z, extrair_csv, listar_arquivos, listar_competencias

listar_competencias(2026)          # ['202601', ..., '202606']
listar_arquivos('202001')          # ['CAGEDMOV202001.7z'] -- nem todo release tem os 3
conteudo = baixar_7z('202606', 'MOV')             # bytes do .7z
path = extrair_csv(conteudo, 'CAGEDMOV202606.txt', dest_dir)   # extrai e devolve o caminho
```

**Detalhes técnicos** (todos confirmados ao vivo em 2026-08):
- FTP puro, login anônimo, sem TLS ("Microsoft FTP Service"/IIS).
- **Encoding Latin-1/cp1252 nos nomes de pasta/arquivo acentuados**, não UTF-8.
  `FTP(..., encoding="latin-1")` resolve de forma transparente. `urllib.request.urlopen`
  com percent-encoding **não funciona** (decodifica como UTF-8 antes de repassar ao
  ftplib e corrompe o byte) — usar sempre este módulo, nunca `urlopen`, para caminhos
  com acento.
- Três arquivos por competência de release: `CAGEDMOV` (no prazo), `CAGEDFOR` (fora do
  prazo), `CAGEDEXC` (exclusões). **Nem toda competência tem os 3** — 2020-01 (primeiro
  release) só tem MOV; 2020-02/03 têm MOV+FOR sem EXC. Checar com `listar_arquivos()`
  antes de baixar, senão `error_perm: 550`.
- CSV dentro do 7z: `sep=";"`, conteúdo em UTF-8 (não confundir com o Latin-1 dos
  *nomes* no FTP).
- **Separador decimal NÃO é consistente entre releases**: a maioria usa vírgula
  (`"4800,00"`), mas os arquivos de **2023-08 e 2023-09 usam ponto** (`"2333.8"`).
  Confirmado ao vivo no texto cru dos dois. Um `decimal=","` fixo no `read_csv` deixa a
  coluna como `object` no formato inesperado e estoura `TypeError` na primeira operação
  aritmética — ver `_normalizar_salario` em `domain/db/brasil/mte/_caged_core.py`, que
  lê a coluna como texto e normaliza os dois casos.
- Tamanho: MOV ~50MB comprimido / ~450MB extraído / ~4M linhas por mês; FOR/EXC ~0,6MB.
- `py7zr` (1.1.3) não lê 7z puramente em memória — só `extract()`/`extractall()`, que
  escrevem em disco. Por isso `extrair_csv` recebe um `dest_dir` e o chamador é
  responsável por apagá-lo (padrão "agregar-e-descartar", ver
  `domain/db/brasil/mte/_caged_core.py`).
- Sem checksums publicados para validar a integridade do download.

### `connectors/comexstat.py` — API do Comex Stat (MDIC), ao vivo

```python
from connectors.comexstat import ComexStat

cs = ComexStat()
df = cs.get_trade("export", "1997-01", "2026-06", country_code="160")  # China
df_mundo = cs.get_trade("export", "1997-01", "2026-06")                # sem filtro
```

**Detalhes técnicos:**
- `https://api-comexstat.mdic.gov.br`, sem autenticação, mas com **rate limit agressivo**
  (HTTP 429 depois de poucas chamadas rápidas em sequência, confirmado empiricamente) — todo
  método usa retry com backoff exponencial e `min_interval=2.0s` entre chamadas. Para janelas
  grandes/históricas use o `comexstat_bulk.py` abaixo, não este.
- Cobertura 1997-01 → presente (mensal), publicado ~3 dias após o fim do mês — mais rápido que
  o Balanço de Pagamentos do BCB. Valores em USD FOB.
- **Não é BPM6.** Comex Stat/SECEX usa "comércio geral" (registro aduaneiro, SISCOMEX); o BCB
  aplica ajustes documentados para chegar de lá até `cmb_balanco_pagmt.mercadorias_gerais`. Os
  totais das duas fontes **não** devem ser somados ou comparados linha a linha — o Comex Stat é
  recorte complementar (quebra por país/categoria), não reconciliação da BOP.
- A quebra clássica "Fator Agregado" (Básicos/Semimanufaturados/Manufaturados) **não existe como
  filtro da API** — só no arquivo de correlação `NCM.csv` do download em massa.

### `connectors/comexstat_bulk.py` — Comex Stat em massa (CSV anual por NCM)

```python
from connectors.comexstat_bulk import get_year, get_year_by_fator_agregado, get_year_by_produto

df = get_year("export", 2015)                       # NCM-level, ano inteiro
df_fa = get_year_by_fator_agregado("export", 2015)  # via correlação NCM.csv
```

**Detalhes técnicos:**
- `balanca.economia.gov.br/balanca/bd/comexstat-bd/ncm/{EXP,IMP}_{ano}.csv` — arquivos anuais
  estáticos, **sem rate limit** (a própria documentação da API recomenda esta rota para consultas
  grandes). Uso: **somente o backfill histórico** (1997→hoje, uma vez); update rotineiro é pela
  API ao vivo.
- `;` como separador, aspas duplas em texto. Colunas de export:
  `CO_ANO;CO_MES;CO_NCM;CO_UNID;CO_PAIS;SG_UF_NCM;CO_VIA;CO_URF;QT_ESTAT;KG_LIQUIDO;VL_FOB`;
  import acrescenta `VL_FRETE;VL_SEGURO`.
- Códigos `CO_PAIS` confirmados **idênticos** aos da API ao vivo (China=160, EUA=249,
  Argentina=063, Alemanha=023) — as duas rotas alimentam a mesma tabela sem tradução.
- É daqui que sai a correlação NCM → fator agregado (`get_ncm_fator_agregado`) e NCM → SH6
  (`get_ncm_sh6`), que a API não expõe.

### `connectors/cftc.py` — CFTC Commitments of Traders (TFF)

```python
from connectors.cftc import CFTC
```

**Detalhes técnicos:**
- ZIPs anuais em `https://www.cftc.gov/files/dea/history/fut_fin_txt_{YYYY}.zip`, sem
  autenticação.
- Contratos de **moeda (BRL, MXN, …) estão no relatório TFF** (Traders in Financial Futures),
  não no disaggregated de commodities — procurar no arquivo errado é o erro fácil aqui.
- **Desde 2026-09-01 extrai as CINCO categorias de participante do TFF**, não só os fundos
  alavancados: `open_interest`, mais `<p>_long`/`_short`/`_spread`/`_net` para `dealer`
  (Dealer/Intermediary), `asset_mgr` (Asset Manager/Institutional), `lev` (Leveraged Funds),
  `other` (Other Reportables) e `nonrept` (Nonreportable). Os nomes antigos (`lev_*`,
  `nonrept_*`) foram preservados, então a expansão é backfill, não migração — mas as séries
  novas **só existem nas linhas recarregadas**, e a recarga completa é
  `run(years=list(range(2011, ANO+1)))`.
- **`nonrept` não tem coluna de spread na fonte** — o CFTC não abre o resíduo assim. Uma leitura
  que assuma as 5 × 4 séries acha 20 e encontra 19.
- **`spread` fica fora do líquido**: uma posição travada é comprada e vendida ao mesmo tempo e
  cancela na exposição direcional. É o que faz os cinco líquidos somarem **exatamente zero** —
  conferido nas 748 semanas do BRL, resíduo 0, junto com `Σ(long + spread) = Σ(short + spread) =
  open_interest`.
- **Cobertura do BRL: começa em 2011-04-05.** O arquivo de 2010 não tem uma linha de BRAZILIAN
  REAL, então não há backfill anterior — e há 16 buracos maiores que uma semana até 2015, um
  deles de 196 dias. Quem consumir isto como série semanal densa precisa tratar os buracos; o
  relatório cambial o faz com um guarda de span na média móvel.

### `connectors/ipeadata.py` — API do Ipeadata (OData v4)

```python
from connectors.ipeadata import IPEA

ipea = IPEA()
df = ipea.get_series("FUNCEX12_TTR12")     # date (Timestamp), value (float)
ipea.buscar_series("termos de troca")      # busca por nome
```

**Detalhes técnicos:**
- `http://www.ipeadata.gov.br/api/odata4`, sem autenticação. Usado para séries que o SGS do BCB
  não tem — hoje só termos de troca (Funcex), em `domain/db/brasil/ipea/cmb_termos_troca.py`.
- **Gotcha de OData**: `$filter=contains(...)` devolve **400** nesta API — usar
  `substringof('valor', CAMPO)`, a sintaxe do OData v3, no lugar.

### `connectors/tesouro_series_temporais.py` — API de Séries Temporais do Tesouro

```python
from connectors.tesouro_series_temporais import SeriesTemporais

st = SeriesTemporais()
temas = st.get_temas()                     # 10-20 temas
arvore = st.get_arvore(subtema_id)         # plano de contas hierárquico
df = st.get_series_bulk({"nome": 12345})   # uma chamada HTTP por série
```

**Detalhes técnicos:**
- Backend **não documentado** no CKAN da Tesouro Transparente — descoberto rastreando as chamadas
  de rede da própria página de séries temporais. Sem autenticação,
  `Access-Control-Allow-Origin: *`. Por não ser documentado, pode mudar sem aviso.
- Estrutura Tema → Subtema → árvore de séries com plano de contas (`10.03.1.1.02.1`) e id próprio
  por série. `flatten_arvore()` achata a árvore; `get_series_bulk()` faz uma chamada por série —
  a API **não** tem download em lote, e é por isso que `fisc_investimento` custa ~80 requests.
- Alimenta `domain/db/brasil/tesouro/fisc_investimento.py` (Tema 13). A API "oficial" do CKAN para
  o RTN (`apiapex.tesouro.gov.br`) segue **morta** (loop de redirecionamento, testado ao vivo) —
  o RTN continua vindo do xlsx via `tesouro.py`.

### `connectors/mysql.py` — Insert/Update no banco

```python
from connectors.mysql import insert_data_into_database, truncate_table, backup_table_before_truncate

insert_data_into_database("macro_brasil", "atv_pim", df)

# Para tabelas alimentadas por uma fonte que so distribui historico completo
# (nunca incremental) e que por isso trunca+recarrega toda vez (ver fisc_rtn.py/fisc_efgg.py):
backup_table_before_truncate("macro_brasil", "fisc_efgg", backup_dir, keep=5)  # snapshot CSV antes
truncate_table("macro_brasil", "fisc_efgg")
insert_data_into_database("macro_brasil", "fisc_efgg", df)
```

`insert_data_into_database` faz `SHOW COLUMNS FROM table`, reordena o df, e executa `INSERT ... ON DUPLICATE KEY UPDATE` em batches de 1000 linhas.

**Bug corrigido:** `.where(pd.notna(df), None)` não convertia NaN em float64 para None — `executemany` enviava `float('nan')` como string `'nan'` ao MySQL. Fix: `df.astype(object).where(...)`.

**`backup_table_before_truncate`** (2026-08, adicionado depois de truncar `fisc_rtn` sem backup na
migração Excel→API desse script — os valores antigos daquela migração específica já se perderam):
salva um CSV com timestamp do conteúdo atual da tabela antes de truncar, mantendo só os últimos `keep`
(default 5) — dá um "antes desta rodada" para comparar se uma carga futura trouxer uma revisão abrupta
ou errada da fonte. **Não é chamado automaticamente por `truncate_table()`** — escopo deliberadamente
restrito aos scripts que pedem (`fisc_rtn.py`, `fisc_efgg.py`, ambos salvando em
`domain/db/brasil/tesouro/_backups/`, gitignored), não todo script que trunca. Usa `cursor.fetchall()`
(não `pd.read_sql`) para evitar o warning do pandas sobre conexão não-SQLAlchemy.
