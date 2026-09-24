# domain/dashboards/ — quem LÊ cada tabela

Config estática + resolvedor de estado, no mesmo formato de `domain/release_calendar/`.
Responde a pergunta que faltava no sistema: **este dashboard está olhando para dado velho?**

As três peças, e por que são separadas:

| | pergunta | onde |
|---|---|---|
| `domain/release_calendar/` | QUANDO cada dado sai | `calendar_2026.yaml` |
| `domain/db/registry.py` | QUEM ESCREVE cada tabela | derivado de `_TABLE` |
| **`domain/dashboards/`** | **QUEM LÊ cada tabela** | `manifest.yaml` |

Sem a terceira, apertar "Atualizar" no calendário deixava o banco em dia e todo HTML em
`reports/` parado — o ETL rodava e nada mais acontecia.

## Arquivos

- **`manifest.yaml`** — uma entrada por dashboard: saída, módulo com `run()`, comando, custo
  medido de geração, e a lista de dependências. Hoje 12 dashboards, 138 dependências —
  **todos com `module`**: o Oráculo, o único que não tinha, saiu em 2026-09-23 (ver o
  comentário no lugar dele no manifesto).
- **`status.py`** — resolve o estado ao vivo de cada dependência e compara com o *stamp*.

**Os campos `note:` são texto de PRODUTO, não comentário** (2026-09-01, correção do usuário
sobre um print: *"você está transferindo nossa conversa daqui para o dash"*). Eles são
renderizados no card da aba Status dashboard, para alguém que nunca viu aquele dashboard — então
não levam nome de função/arquivo do repositório, nome de tabela, data de decisão nossa ("desde
2026-08-31") nem pendência nossa ("segundos não medidos"). O que é decisão, medição e "por que"
vai em **comentário YAML** (`#`), que não sai no relatório, ou neste arquivo. Um guarda em
`tests/test_release_calendar_js.js` roda contra o payload real e reprova a lista de termos —
o teste falha aqui, no manifesto, não no template.

## Por que declarado à mão

O registry deriva tabela→script porque todo ETL declara `_TABLE`. Do lado do consumo não há
convenção equivalente: cada `generate_report.py` lê de um jeito (`MySQLDataRequester` direto,
`_load_flat()`, `pd.read_sql` com JOIN, e um caso que lê tabela de outro projeto). Varrer isso
com regex daria falso negativo em silêncio — que é o erro que este arquivo existe para impedir.

`validar()` cobra o que dá para cobrar sem adivinhar: toda tabela declarada existe no banco,
todo arquivo declarado existe em disco, todo módulo importa. O inverso (tabela lida pelo código
e não declarada aqui) **não** é checável — ao adicionar uma leitura nova num relatório, declare
aqui também.

## Os 5 tipos de dependência

`mysql` · `csv` · `artifact` · `yaml` · `live`. O que separa os quatro últimos do primeiro é
prático: **nenhum botão de ETL os move**. `fora_do_mysql()` marca isso, e `base_mercado`
entra na marcação apesar de ser MySQL — quem escreve nela é o projeto CentralManagement.

Como sai o `ultimo` de cada um: `mysql` `MAX(date_col)` · `csv` maior valor de `date_col` ·
`artifact` último rótulo de índice do CSV, ou a chave que `json_date` nomear num JSON · `yaml`
só mtime · `live` a última observação na fonte.

## Stamp: por que o veredito precisa dele

O mtime do HTML diz *quando* foi gerado, não *o que tinha dentro*. `stamp()` grava, no momento
da geração, o último dado de cada dependência — aí a comparação vira exata: "o banco tem IPCA de
agosto, o relatório foi feito com até julho". Sem stamp o veredito é `sem stamp`, nunca um
`em dia` de mentira.

**Quem grava é `render_report()`, desde 2026-09-23** — ver a seção seguinte. Antes era só
`gerar(key)`, e era por isso que quase metade dos relatórios não tinha retrato.

`gerar(key)` continua sendo o ponto de entrada do **botão** (é ele que recalcula o que ficou
atrás antes de gerar), e só regrava o retrato se o gerador não tiver gravado. O campo
`output_mtime_ns` é o que diz se o retrato é *daquele* arquivo — nanossegundos, não segundos:
com resolução de segundo, regerar à mão no mesmo segundo do stamp passava por "em dia".

Dependência de arquivo tem um segundo sinal, `arquivo_mais_novo`, que **não** precisa de stamp:
um artefato reescrito depois do HTML não está dentro dele, ponto.

## Quem grava o retrato é quem escreve o arquivo (2026-09-23)

Pedido do usuário depois de um diagnóstico: *"o processo de atualização não está funcionando,
está cheio de furo … vamos arrumar esse processo de atualizar e regenerar o dashboard, assim
como deixar o stamp correto."* Os furos eram dois, e os dois vinham do mesmo lugar — **o retrato
era gravado por um passo separado daquele que escreve o arquivo.**

**Furo 1: o caminho documentado não stampava.** Só `gerar()` gravava, e o comando escrito em 10
dos 13 `CLAUDE.md` de pasta é `generate_report.run()`, que não passa por lá. Medido naquele dia:
**8 dos 13 relatórios entregues** tinham retrato ausente (2, nunca gerados pelo botão) ou de
outra geração (6, stampados e depois regerados à mão — Crédito com o HTML 6 dias mais novo que o
retrato, us/Inflation 6, Inflação 5, Expectativas 2). A aba não conseguia dizer nada sobre quase
metade da lista. Um mecanismo cuja corretude depende de ninguém usar o caminho normal não fica
em dia — e a correção não é disciplina, é mudar quem grava.

`render_report()` passou a chamar `_registrar_procedencia()` logo **depois** do `write_text`, e
`chave_por_saida()` (aqui) resolve o caminho escrito contra o `output` do manifesto. Todos os 12
relatórios HTML do projeto passam por `render_report()`, então gerar de qualquer jeito deixa o
retrato em dia. Três cuidados, cada um a origem de um defeito silencioso:

- **Depois de escrever, nunca antes** — gravado antes, o retrato seria da versão anterior do
  arquivo e produziria um "em dia" de mentira na geração seguinte.
- **Falhar ali não derruba a geração.** O retrato consulta o banco; banco fora do ar não pode
  custar o relatório, que já está em disco. A falha é avisada e o veredito vira "não dá para
  conferir", que é a resposta honesta.
- **O casamento é pelo caminho RESOLVIDO, não pelo nome.** Brasil e EUA têm um `Inflation.html`
  cada; casar por nome stamparia um no lugar do outro. E um `output=` fora do manifesto não casa
  com nada e não stampa — melhor nenhum retrato do que o retrato de outro arquivo.

**Furo 2: o retrato velho virava acusação.** `estado()` testava `novos` **antes** da validade do
retrato: o código já sabia que aquele retrato não era daquele arquivo (`output_mtime_ns`
diferente) e comparava com ele assim mesmo. O resultado é pior do que não saber, porque não se
distingue de um alerta verdadeiro. Medido nos dois cards laranja daquele dia:

| card | acusação | arquivo entregue | veredito |
|---|---|---|---|
| Crédito | "falta a inadimplência de set/2026" | a maior data embutida **é 2026-09-01** | **falso** |
| Expectativas | "o Focus andou para 18/09" | 65 ocorrências de `2026-09-11`, zero de `18/09` | verdadeiro |

Dois avisos idênticos na tela, um certo e um errado — que é exatamente como um painel perde a
confiança de quem o lê. A marca `stamp_vale` entrou dentro de `novo`, então com retrato inválido
a comparação simplesmente não é feita; e **`arquivo_mais_novo` continua sendo testado antes da
falta de retrato**, porque aquele sinal não depende de retrato nenhum e sumiria na reordenação.

Trocar *só* a ordem do bloco de veredito, com a marca no lugar, é **mutante equivalente** —
verificado, não suposto. Quem carrega o conserto é a marca; a ordem existe para o ramo de
`arquivo_mais_novo` continuar alcançável.

**O que isso muda na tela, e vale saber antes de estranhar:** a lista passou a ter *mais*
"não dá para conferir" do que antes (de 5 para 7), porque a confiança falsa saiu. Cada um deles
some sozinho na primeira vez que aquele relatório for gerado, por qualquer caminho. Para limpar
tudo de uma vez: `--gerar todos`, que gera os doze **sem recalcular** — é o uso para que ele
existe.

Coberto pelas seções 2 e 2c de `tests/test_dashboard_status.py` (o retrato velho que não pode
acusar, o `render_report()` que grava sozinho, a ordem escrita-depois, a falha que não derruba a
geração e o casamento por caminho), verificado contra **8 mutantes** — um deles registrado como
equivalente, com o motivo.

## `procedures` — o que o Regerar recalcula antes de gerar (2026-08-31, estendido em 2026-09-01)

**São dois botões no sistema e só dois**, por pedido explícito do usuário: *"Atualizar os dados na
base de dados"* e *"regenerar o dashboard (trazendo os dados novos, recalculando as métricas, tudo
que houver para atualizar e recalcular)"*. Houve por algumas horas um terceiro botão, por
procedimento, e o processo ficou confuso — a versão final dobra o recálculo dentro do
`gerar()`.

Um bloco `procedures:` por dashboard declara os passos de recálculo:
`{id, label, module, call, seconds, writes[], cut_from, reads[], granularidade}`. `module` + `call`
são importados, como o `module` + `run()` do dashboard, então a página manda um id e quem resolve
id → função é o nosso lado; sem shell em ponto nenhum. A ordem da lista é a ordem de execução.

A ligação mora no **`writes` do procedimento**, não no dep, porque `salvar()` grava dois arquivos e
`rodar()` sete: declarada do lado do dep, a mesma rodada apareceria nove vezes. `proc_por_dep()`
inverte para a aba marcar cada linha.

### A segunda data de um artefato calculado

Um artefato tem duas, e só uma era observável: quando foi **escrito** (mtime) e com que **conjunto
de informação**. Rodar `salvar()` hoje contra o Focus de anteontem produz mtime de hoje e número de
anteontem — foi o que passou por "em dia" em 2026-08-31, com o relatório gerado no dia e a previsão
de seis dias antes.

`cut_from` é o artefato que carrega o corte, e `reads` são as fontes. O corte sai do próprio
artefato: `json_date` nomeia a chave num JSON (`corte_usado`), e num CSV indexado o último rótulo de
índice já é o corte. `reads` aceita **tabela ou artefato** — `modelo` lê o painel que `painel`
grava, e é isso que faz a cascata existir sem aresta declarada entre os dois passos.

**"CSV indexado" é uma armadilha, e a validação agora cobra.** O último rótulo de índice é o
*primeiro campo da última linha*, o que só é o corte num CSV **largo** (uma linha por data). Num CSV
**longo** — uma linha por série × data, o formato do `ipca_bcb_series.csv` — a última linha é a
última data da série alfabeticamente final, e se a coluna de rótulo vier na frente o corte sai como
`'IPCA_servicos_ma3_sa'`: `atrasado` fica `None` para sempre, sem erro nenhum. O dep tem de declarar
`date_col` (aí o corte é o `MAX` da coluna), e `validar()` reprova um `cut_from` cujo valor lido não
seja data na granularidade declarada.

### `granularidade` é o que impede "roda tudo sempre"

`dia` · `mes` · `trimestre`. Os dois lados da comparação são reduzidos a ela por `_para_gran()`, e é
isso que dá a cada passo a **frequência** dele. O painel é trimestral: o corte dele é `2026Q3` e a
Focus responde `2026-08-28`, que reduzido dá `2026Q3` — em dia. Só quando outubro abre (`2026Q4`) o
passo fica atrás. Sem isso, a estimação seria refeita a cada boletim diário, mudando os 22
parâmetros do modelo por nada. A previsão é diária, e fica atrás assim que a pesquisa anda.

Um passo **sem `cut_from`** fica em "sem veredito" e **não** roda automaticamente: 4 minutos de
estimação no escuro é pior do que não rodar. `validar()` cobra a ausência, justamente porque esse é
o silêncio que criou o bug.

### `gerar()` = recalcular o que está atrás + gerar + stampar

`recalcular_atrasados()` percorre os passos na ordem e **reavalia a cada um** — daí a cascata: se
`painel` ganhou um trimestre, o `modelo` que o lê passa a estar atrás na mesma rodada. As tabelas são
consultadas uma vez (não mudam no meio); os artefatos são relidos, porque são o que os passos
anteriores mexeram. Um passo que falha **não interrompe**: entra como `falhou`, a geração segue e o
relatório sai com o artefato antigo dizendo isso — a estimação depende do IPEADATA e do anexo do RPM,
e rede fora do ar não pode virar "sem relatório".

`gerar(key, recalcular=False)` gera sem tocar em artefato; é o que o `--gerar todos` usa, que existe
para carga inicial de stamp e não para refazer modelo.

### Quem tem passo, e por que os outros não têm (levantamento de 2026-09-01)

Pedido do usuário para estender o piloto "igual o de política monetária". O levantamento vale mais
que a extensão: dos 12 dashboards, **dois** têm passo.

| dashboard | passos | o que são |
|---|---|---|
| `brasil_monetary_policy` | 3 | painéis, estimação e previsão — cálculo, minutos |
| `brasil_inflation` | 1 | um **fetch** de ~18s: o `ipca_bcb_series.csv`, único insumo dela fora do MySQL |
| os outros 10 | 0 | leem o banco e calculam durante a geração — não há artefato entre o ETL e o HTML |

O passo da inflação prova o desenho por um caminho novo: não é um modelo caro, é um arquivo que
**nenhum dos dois botões alcançava** (o Atualizar mexe no MySQL, e o gerador só lê). Estava um mês
atrás quando foi medido — arquivo até 2026-07, `inflc_decomposicao` já com 2026-08 —, e a comparação
que revela isso é contra a tabela que recebe a **mesma divulgação**, já que a fonte real (o SGS do
BCB) não é dep declarada. Medido depois do fetch: o arquivo alcança o mesmo mês da tabela, que é a
condição para o passo não rodar a cada Regerar para sempre.

**`writes` aceita dep `csv` além de `artifact`**: o que separa os dois tipos no manifesto é *como a
data sai do arquivo* (coluna declarada vs. rótulo de índice/`json_date`), não quem o escreve.

**O câmbio é o caso que ficou de fora de propósito.** Os dois arquivos do modelo Ridge que a geração
lê passaram a ser **declarados** — não eram, e era invisibilidade da mesma classe —, mas como
dependência, não como passo: `model_fit_cutoff.json` fixa o mês do ajuste por decisão explícita do
usuário (2026-08: regerar não reestima) e `forecast_error_bands_w72.json` é estatística de erro da
amostra inteira, ~90s, que muda junto com o ajuste e não com o mês novo. Há um motivo técnico além da
decisão: o corte da banda é o mês em que **todos** os canais já têm dado (um mínimo), e a regra de
`reads` compara com o **máximo** das fontes — declarar como passo marcaria atraso todo mês sem que
refazer resolvesse, que é o laço que esta camada evita em toda parte.


**`atrasado` não entra no `veredito` do dashboard**, e a separação é o ponto: os vereditos comparam o
HTML com as fontes dele, isto compara um *insumo* com as fontes. Se virasse `desatualizado`, o
veredito não se apagaria com uma regeração e `regerar_afetados()` viveria em laço. Sai como
`n_proc_atrasados`, sinal próprio, e o recálculo entra uma vez, por dentro do `gerar()`.

Declarado em **`brasil_monetary_policy`** (`painel`, `modelo`, `previsao`) e em
**`brasil_inflation`** (o fetch do CSV do IPCA). `rodar_procedimento()` + `--rodar KEY:PROC`
continuam existindo para rodar um passo isolado sem gerar, mas não há botão para isso.

## `afetados()` / `regerar_afetados()` — fechar o circuito dado → métrica

`afetados(tabelas)` é o mapa lido ao contrário: dá os dashboards que **leem** as tabelas
passadas (nome nu ou `schema.tabela` — o casamento é pelo sufixo). `regerar_afetados(tabelas)`
usa isso e regera **só os que o veredito acusa como `desatualizado`**.

É o que `jobs/update_db.py` chama no fim de todo passe de linha de comando (2026-08-28, a
pedido do usuário: "quando atualizar os dados, as métricas também devem ser atualizadas"), e
o filtro por veredito é o que o separa de "regera tudo que toca a tabela": um passe de ETL que
não trouxe linha nova deixa todo mundo `em dia` e não regera nada.

Três decisões que valem reter:

- **`sem relatorio` não dispara.** Construir pela primeira vez um relatório que nunca existiu é
  uma decisão, não uma consequência de atualizar dado.
- **Dependência fora dos nossos schemas nunca dispara.** Uma tabela pode ser MySQL e ainda assim
  não ser movida por nenhum ETL daqui — e um passe nosso não pode alegar tê-la atualizado. O caso
  que motivou a regra era `base_mercado.interest_rates`, do CentralManagement; ela **saiu do
  manifesto em 2026-09-03** (virou `macro_brasil.br_interest_rate`, com ETL nosso), então hoje
  **nenhuma dependência declarada tem `owner`** e este ramo não tem usuário vivo. Ficou porque a
  situação volta assim que alguém declarar dependência de outro projeto — e `test_serve_calendar.py`
  agora afirma o contrário (que não sobrou nenhuma), o que é o que impede a regra de virar código
  morto sem ninguém notar.
- **Falha de geração não derruba o job de ETL.** O dado já está no banco; um gerador quebrado é
  problema do relatório. Fica no log e no veredito, que passa a acusar `desatualizado`.

O caminho da **página** não passa por aqui: `serve.py` chama `update_db.executar_grupo()`
direto, então a escolha um-a-um continua valendo (ver "Um de cada vez, por decisão" abaixo).

## Uso

```powershell
uv run python -m domain.dashboards.status                      # tabela de estado
uv run python -m domain.dashboards.status --detalhe brasil_credit
uv run python -m domain.dashboards.status --validar            # manifesto x banco x disco
uv run python -m domain.dashboards.status --live               # inclui FRED
uv run python -m domain.dashboards.status --gerar brasil_monetary_policy   # recalcula + gera
uv run python -m domain.dashboards.status --gerar X --sem-recalcular       # só o HTML
uv run python -m domain.dashboards.status --gerar todos        # stampa os 11, sem recalcular
uv run python -m domain.dashboards.status --rodar brasil_monetary_policy:previsao  # um passo só
```

Consumido por [`analytics/release_calendar/`](../../analytics/release_calendar/CLAUDE.md) — aba
"Status dashboard", e pelo endpoint `/api/dashboards` do `serve.py`.

Testes: [`tests/test_dashboard_status.py`](../../tests/test_dashboard_status.py) (lógica do
veredito sobre manifesto sintético + manifesto real contra banco e registry),
[`tests/test_dashboard_procedimentos.py`](../../tests/test_dashboard_procedimentos.py) (40
asserções sobre `procedures`, `json_date` e o veredito de atraso — inclusive que ele *não* virou
veredito de dashboard) e a seção "STATUS DASHBOARD" de
[`tests/test_release_calendar_js.js`](../../tests/test_release_calendar_js.js).

## Custo

`estado()` leva ~2s: um `UNION ALL` só resolve o `MAX(date)` das ~70 tabelas em 0,1s, e as
contagens de linha vêm aproximadas do `information_schema` de propósito — `COUNT(*)` exato no
mesmo conjunto custava 7,6s de varredura completa para preencher uma coluna informativa.
`--live` acrescenta uma chamada de rede por série externa.

## Um por requisição — e, desde 2026-09-03, um botão que percorre a fila

**O endpoint continua sendo um dashboard por requisição** (`POST /api/gerar` recebe uma `key`), e
isso não é só higiene de segurança: é o que faz cada card virar "em dia" na tela no momento em que
o dele volta, em vez de a página congelar por minutos.

O que mudou é a página. Ela ganhou **"Regerar pendentes"**, a pedido explícito do usuário
(*"colocar um botao, 'Regenerar pendentes' que regenerar todos os dash pendentes"*), o que
**reverte a decisão de 2026-08-26** de não haver lote em lugar nenhum — o argumento de então era
que quem acabou de atualizar o IPCA escolhe qual dos seis dashboards que o consomem interessa
naquele momento. Os botões de card ficaram: o lote é adição, não substituição, e serve o caso em
que a resposta é "tudo o que ficou para trás".

Ele é um **laço no cliente sobre o mesmo endpoint**, em série — não há rota de lote para auditar, e
dois geradores nunca disputam o banco. A fila é fotografada antes do primeiro POST (um dashboard que
continue pendente depois de gerar, porque um passo dele falhou, voltaria para a fila e seria
retentado para sempre) e uma falha não interrompe o resto.

**A fila é mais estreita que "não está verde"**, e é aqui que ela conversa com o resto deste
arquivo: entram `desatualizado` e *passo atrás dos dados*; ficam fora `sem relatorio` — construir
pela primeira vez é decisão, a mesma regra de `regerar_afetados()` — e `sem stamp`, que não é
atraso e sim a ausência do retrato. Sem `module` também fica fora.

O `--gerar todos` do CLI é outra coisa e continua sendo: ele gera os doze **sem recalcular**, para
carga inicial de stamp. É por isso que o modo arquivo do botão copia uma linha `--gerar <key>` por
dashboard pendente em vez de `--gerar todos`.

**A regeração automática de `update_db.py` (2026-08-28) também não é isto**, e a diferença
continua valendo: ela não é lote nem escolha, é *o que ficou para trás por causa do dado que acabou
de entrar* — tipicamente um dashboard, às vezes nenhum.

## Pending

- **`build_seconds` foi medido uma vez** (2026-08-26) e envelhece sozinho. `gerar()` já devolve
  o tempo real de cada execução; ninguém o grava de volta.
- **`POST /api/gerar` é síncrono**, igual ao `/api/run`: Expectations (53s) e FX (43s) deixam o
  botão em "regerando..." sem progresso. Fechar a aba não aborta. Se incomodar, a saída é job id
  + polling, não timeout — mesma pendência que o botão da outra aba já tinha.
- **`procedures` só existe em `brasil_monetary_policy`.** Candidato direto: o `fetch_bcb.py` do
  relatório de inflação (hoje com `refresh:` em texto). Os artefatos de extração manual de PDF não
  automatizam, e ali o texto continua sendo a resposta honesta.
- **O Regerar ficou síncrono e mais longo** — com a previsão atrasada são ~80s, e na virada de
  trimestre ~6 min com o botão em "recalculando...". Mesma saída dos outros dois se incomodar:
  job id + polling.
- **`seconds` de `painel` e `modelo` não foram medidos** (90 e 240 são estimativa; o de `previsao`,
  55, foi medido em 2026-08-31). O número aparece no tempo que o botão anuncia, então a estimativa
  errada é visível. `gerar()` devolve o tempo real e ninguém o grava de volta — mesma pendência do
  `build_seconds`.
- **A `granularidade` de `painel`/`modelo` é uma aposta declarada, não medida**: se algum insumo
  deles for revisado dentro do mesmo trimestre, o passo não vai perceber. O corretivo é rodar
  `--rodar` à mão; o alternativo seria comparar `MAX(date)` por tabela contra um stamp por passo,
  que é mais preciso e mais máquina.
- ~~**O Oráculo não tem `module` com `run()`**~~ — **resolvido tirando-o da lista** (2026-09-23,
  a pedido do usuário). Era o único sem `module`, então o card dele nunca tinha botão nem
  veredito: ocupava uma linha da aba para dizer "não dá para conferir" todo dia. O ramo que trata
  de dashboard sem `module` continua no código, sem usuário, com uma asserção que reprova se
  alguém voltar a criar um. Se `jobs/update_oraculo.py` virar função com `run()`, aí vale
  redeclarar a entrada — ela está no git.
