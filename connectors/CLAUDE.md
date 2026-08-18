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
em `analytics/fiscal_policy/CLAUDE.md`, tinha concluido "so PDF" e estava errada/desatualizada):
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
  `analytics/fiscal_policy/reference/rtn_vs_efgg.md` para a diferenciacao completa vs. a RTN
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
