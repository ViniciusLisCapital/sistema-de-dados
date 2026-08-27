# Sistema de Dados — Contexto para o Claude

## Regras gerais

- **The text should remain in the language it already is, NO TRANSLATION.** When generating `.md` files from English-language PDFs, write in English. When generating from Portuguese-language sources, write in Portuguese.

## Sobre o Projeto

Sistema de dados da LIS Capital para coleta, processamento e visualização de variáveis macroeconômicas (Brasil, EUA). Alimenta dashboards Power BI e materiais de análise macro.

📄 **Racional estratégico e origem do projeto** (por que o vault `obsidian/` e a direção de agentes especialistas por área macro existem, fases de investimento planejadas): [`team_materials/structure_materials/macro-project-context.md`](team_materials/structure_materials/macro-project-context.md).

---

## Arquitetura atual

```
connectors/          — Clientes de APIs/fontes externas: IBGE, BCB (SGS + Focus/Olinda, agenda ICS,
                       tabelas especiais xlsx, anexo estatístico do RPM, comunicados do Copom),
                       FRED, BIS, BLS, BEA (tabelas NIPA da Secao 2 pela API; o xlsx
                       aberto só para a hierarquia, que a API não publica),
                       agendas de divulgação do BLS/BEA (us_agenda.py: página por release,
                       feeds ICS e /fred/release/dates como terceira opinião),
                       CFTC, IPEA,
                       Comex Stat/MDIC (API ao vivo + CSV em massa), Tesouro (RTN via CKAN + Séries
                       Temporais + EFGG), PDET/MTE (FTP do Novo CAGED), Yahoo Finance, MySQL
                       ↳ assinatura, gotchas e limites de cada um: connectors/CLAUDE.md
domain/
  dashboards/        — O lado do CONSUMO: manifest.yaml declara de que cada dashboard depende
                       (tabela, CSV, artefato de modelo, YAML ou fonte live) + status.py, que
                       resolve o estado ao vivo de cada dependência e compara com o stamp
                       gravado na última geração. É o que a aba "Status dashboard" do
                       calendário mostra, e onde o botão de regerar vai se apoiar
                       ↳ domain/dashboards/CLAUDE.md
  db/                — ETL: fetch → transform → insert. Uma pasta por schema e, dentro dela, uma por
                       FONTE: brasil/{ibge,bcb,tesouro,mdic,mte,ipea,investing},
                       international/{bis,cftc,fred,noaa,yfinance}, us/{inflation} (CPI do BLS + PCE
                       do BEA). Um script por
                       tabela, todos com a mesma interface run()
    registry.py      — tabela → script, derivado da convenção `_TABLE` (76 tabelas; valida em vez de
                       envelhecer em silêncio). É o que faz o --group/--tables/--continuous do
                       update_db.py e o botão do relatório de calendário funcionarem
                       ↳ tabelas ativas, fonte, range, chave primária e gotchas: domain/db/CLAUDE.md
  release_calendar/  — Config estática de QUANDO cada dado é divulgado (calendar_2026.yaml, 27 grupos,
                       uma entrada por evento) + sync.py (o dado chegou quando devia? e, desde
                       2026-08-26, `agenda_das_tabelas()`, a última/próxima divulgação que os
                       relatórios mostram) + update_calendar.py (datas do BCB, feeds ICS) e
                       update_us_calendar.py (BLS/BEA). Não é ETL, nada escreve no MySQL
                       ↳ domain/release_calendar/CLAUDE.md · virada de ano: ROLLOVER.md
analytics/           — Projetos que consomem o banco. Layout país > área desde 2026-08: módulo que lê
                       o schema de um país só vive em brasil/ ou us/; infra de apresentação e
                       cross-country fica na raiz
  report_structure/  — Scaffolding de build-time compartilhado: theme.css, y_autofit.js,
                       tree_helpers.py, builder.py (`render_report()`, que injeta /*REPORT_DATA*/)
  release_calendar/  — Relatório HTML do calendário + serve.py, o modo servido em que o botão
                       "Atualizar" roda o ETL do grupo (abrir_calendario.bat é o atalho de dois
                       cliques). Na raiz porque monitora o sistema inteiro, não uma área
  oraculo/           — Termômetro macro: notas 1–10 por variável (Brasil e EUA) → Power BI
  brasil/            — 9 áreas: exchange_rate, inflation, economic_activity, fiscal_policy, credit,
                       labor_market, monetary_policy (réplica do modelo agregado do BC +
                       relatório de cenários, 2026-08-21), expectations (Focus, 2026-08-24),
                       painel_setores. Cada área = generate_report.py + report.html (+ um módulo por
                       aba) e o seu próprio CLAUDE.md, que é onde vivem abas, fontes e pendências
  us/                — inflation (CPI-U do BLS + PCE do BEA), mesmo padrão; UI em inglês
                       ↳ padrões compartilhados e a regra de corte país/raiz: analytics/CLAUDE.md
jobs/                — Entry points. update_db.py: passe completo de macro_brasil (50 scripts) ou
                       recorte — --continuous (as 7 séries diárias, ~45s: é o que faz sentido agendar
                       todo dia), --group <slug> (o que o botão do calendário chama), --tables a,b,
                       --list. Mais update_international.py (3 scripts), update_us.py (4 passos e a
                       ORDEM importa — ver docstring) e update_oraculo.py
reports/             — Outputs gerados, não versionados, autocontidos e enviáveis. Espelha o país >
                       área de analytics/ (reports/brasil/, reports/us/) — sem isso o Inflation.html
                       do Brasil colidiria com o dos EUA; release_calendar.html fica na raiz pelo
                       mesmo motivo que analytics/release_calendar/. Nomes em Title Case com espaço
                       desde 2026-08 (o sufixo "_latest" foi abandonado), e os defaults de run() de
                       cada generate_report.py já apontam para lá
utils/               — Funções auxiliares compartilhadas
tests/               — Testes pontuais (pytest + harness .js), cada um nascido de um bug específico —
                       não é suíte de cobertura
```


---

## Atualização: quem escreve, quem lê, e o que ainda não se conecta

Três camadas, todas declarativas, cada uma respondendo uma pergunta:

| pergunta | onde | como |
|---|---|---|
| QUANDO cada dado sai | `domain/release_calendar/calendar_2026.yaml` | 25 grupos de divulgação |
| QUEM ESCREVE cada tabela | `domain/db/registry.py` | derivado da convenção `_TABLE` |
| QUEM LÊ cada tabela | `domain/dashboards/manifest.yaml` | 11 dashboards, 116 dependências |

O relatório de calendário tem **duas abas, e elas dividem o trabalho como a atualização
acontece de verdade**:

- **Divulgações** — atualiza o DADO que saiu. `POST /api/run` → `serve.py` valida o slug contra
  o YAML → `update_db.executar_grupo()` → `registry` resolve tabela→script → MySQL.
- **Status dashboard** (2026-08-26) — mostra, por dashboard, cada dependência com onde mora, o
  último dado na fonte e se ela andou depois da geração; e **regera o dashboard que interessa**,
  um por vez, via `POST /api/gerar` → `status.gerar()` (roda `run()` + grava o stamp).

**Não há regeneração em lote em lugar nenhum da página, e isso é decisão explícita do usuário**
(2026-08-26): quem acabou de atualizar o IPCA escolhe qual dos seis dashboards que o consomem
quer reconstruir agora. O calendário não encadeia regeração — foi considerado e recusado.

Custo medido (2026-08-26, contra o banco real): Labor Market 5s, Economic Activity 12s, US
Inflation 13s, Monetary Policy 23s, Credit 24s, Fiscal 30s, Inflation 30s (saída de 104 MB),
FX 43s (com os modelos, inclui FRED ao vivo), Expectations 53s — 233s se alguém regerar os
nove pelo `--gerar todos` do CLI, que existe para carga inicial de stamp.

Três coisas que **nenhum botão resolve**, e por isso saem marcadas como "fora do MySQL":
o CSV `ipca_bcb_series.csv` do relatório de inflação (só `fetch_bcb.py`, sem job), os ~11
artefatos de `analytics/brasil/monetary_policy/data/` (rodar o modelo leva minutos e não faz
parte da geração) e `base_mercado.interest_rates`, que é escrita pelo projeto
CentralManagement. O FX ainda busca CPIAUCSL e DFII10 no FRED durante a geração.

Não há **nenhuma tarefa agendada deste projeto** — a "Atualizacao da base de dados" das 09:30
no Windows pertence ao CentralManagement.

---

## Banco de dados: macro_brasil / macro_international / macro_us

📄 **Organização de schemas, convenção de nomes, tabelas ativas, padrões de chave primária:** [`domain/db/CLAUDE.md`](domain/db/CLAUDE.md) — carrega sob demanda quando o Claude lê arquivos dentro de `domain/db/`.

---

## Connectors

📄 **Documentação completa (API IBGE v3, SGS/Focus do BCB, FRED, MySQL insert/update):** [`connectors/CLAUDE.md`](connectors/CLAUDE.md) — carrega sob demanda quando o Claude lê arquivos dentro de `connectors/`.

---

## analytics/

📄 **Visão geral do diretório, padrões compartilhados entre os relatórios (`/*REPORT_DATA*/`, `data/` vs `referencia/`), e itens de organização pendentes:** [`analytics/CLAUDE.md`](analytics/CLAUDE.md) — carrega sob demanda quando o Claude lê arquivos dentro de `analytics/`.

---

## analytics/oraculo/ — Termômetro Macro

Calcula "notas" (scores 1–10) para variáveis macroeconômicas de Brasil e EUA, alimentando dashboards Power BI.

📄 **Componentes, fluxo de execução, padrão de `scores.py`:** [`analytics/oraculo/CLAUDE.md`](analytics/oraculo/CLAUDE.md) — carrega sob demanda quando o Claude lê arquivos dentro de `analytics/oraculo/`.

---

## analytics/brasil/exchange_rate/ — Panorama Cambial

Relatório HTML interativo de fundamentos cambiais. Arquivo único autocontido — abre em qualquer browser, enviável por email/Dropbox. Desde 2026-08 inclui as 3 abas de modelo que antes eram um segundo arquivo (`reports/ppp_dashboard.html`, template próprio + entry point próprio, ambos retirados na fusão).

**A aba Balanço de Pagamentos virou uma árvore só em 2026-08-27** (pedido do usuário): os 6 gráficos
de composição eram todos recortes da *mesma* hierarquia, repetindo
eixo, legenda e seletor para mostrar níveis diferentes dela. Viraram uma tabela hierárquica única
alimentando um gráfico, com Agregação/Unidade/tipo de gráfico agora **por gráfico**, em `<select>`,
em vez de dois seletores valendo para a aba inteira. A regra que faz o formato funcionar é derivada,
não configurada: em barras empilhadas, um nó marcado que tenha descendente marcado vira **linha** —
o que reproduz a leitura "componentes + total por cima" e torna a dupla contagem impossível, já que
duas barras nunca podem ficar aninhadas. Os 3 recortes do **Comex Stat** ficaram em tabelas próprias
porque não são BPM6 e não decompõem nada da árvore; em troca abrem o que o BPM6 não publica,
**exportação e importação separadas** por parceiro/categoria/produto.

E o bug que motivou a rodada, porque é reutilizável: o `xaxis.rangeselector` **nativo** do Plotly
ancora o fim da janela no range *atual* do eixo, que com `autorange` já inclui o padding automático —
numa série de 31 anos isso vale mais de 2 anos, então "10a" abria com uma faixa vazia à direita. As 6
abas de dados migraram para botões HTML que calculam `[from, to]` das próprias séries (`_ensureRangeBar()`,
régua **abaixo** do gráfico); as 3 abas de modelo ainda carregam o componente nativo. **A vista
inicial era o mesmo bug por um caminho que nenhum botão cobre** (2026-08-27): ela ficava no
`autorange`, que percorre o **array x** e não os valores — um ponto de `y` nulo continua empurrando o
eixo, então um gráfico cuja série começa em 2008 abria em 1982, porque a grade do payload daquela aba
vai a 1982 por causa de *outra* série. Agora `finishChart()` deriva o extent de `gd.data` (não do
`dates` que quem chama passa) e a vista sem faixa escolhida aplica "Tudo" explicitamente. Fechado por
`tests/test_fx_report_js.js` (238 asserções), que afirma sobre a janela que cada botão produz, não
sobre a definição dele.

**A hierarquia foi reorganizada numa segunda rodada no mesmo dia**, também a pedido do usuário. O
achado que vale além deste relatório: os dois lados da Conta Financeira estavam classificados por
critérios diferentes — Ativos pelas 3 categorias funcionais do BPM6, Passivos por uma mistura de
funcional, instrumento e prazo, com uma linha ("Empr./Tít. LP Externo") que **atravessava duas
categorias funcionais** para agrupar por prazo. Os dois lados agora espelham um ao outro, com o
prazo um nível abaixo, sem perder nenhum item. Junto: as 4 contas foram postas na ordem do BPM6 (a
Conta Capital vinha depois da Financeira) — elas somam **exatamente zero** neste dado, resíduo
máximo 0,0001 USD Bi em 379 meses. E metade do que parecia bagunça não era hierarquia e sim
alinhamento: folha sem o espaçador do `▸` e quadradinho de cor renderizado só na linha marcada,
que empurrava o rótulo ao marcar a caixa.

**E o recuo não aparecia de jeito nenhum, por uma colisão de nome de classe** — achado numa
terceira rodada, a partir de um print. Este relatório hospeda dois design systems num arquivo só
(a fusão de 2026-08), e um bloco `table.data-table` do lado de modelo tinha ficado **sem o escopo
`.ppp-scope` que todo o resto daquela metade tem**. Invisível enquanto só ela usava o nome; quando
a aba BP ganhou tabelas com a mesma classe, o `text-align: right` daquele bloco capturou as células
de rótulo. O `padding-left` do recuo continuava sendo aplicado — só não desenhava nada com o texto
encostado na direita. Lição de reuso: antes de trazer um componente de outro relatório para cá,
`grep` o nome da classe.

**As 7 tabelas hierárquicas ganharam cartões de definição** (2026-08-27), no padrão de
`analytics/brasil/labor_market`: rótulo curto na linha, botão `i` abrindo nome oficial da fonte +
explicação + unidade. Duas diferenças em relação ao original: o conteúdo mora **fora da árvore**, num
mapa `NODE_INFO` por chave (três parágrafos dentro de cada literal tornariam ilegível a estrutura da
hierarquia, que é o que se lê ali), e a unidade é **função, não string** — depende dos seletores de
Agregação/Unidade, então `unitLine()` monta o mesmo par que o eixo Y mostra; fixa, ela passaria a
mentir no primeiro clique. `unitNoun` existe porque o interbancário é **volume negociado**, não
fluxo, e chamá-lo de fluxo sugeriria direção onde não há nenhuma.

**Todo gráfico das 6 abas de dados ganhou cabeçalho** (título · o que mede e em que unidade ·
`Fonte: … · <primeiro> a <último>`), no padrão que `analytics/brasil/labor_market` já usava —
um print do gráfico circula sozinho, longe do `<h2>` e das notas. Escrever esse cabeçalho
**expôs um bug anterior**: o `aggregateSum()` do relatório somava um bucket com os meses que
tivesse, sem exigir que estivesse fechado, contrariando a convenção escrita em
`analytics/metric_layers.md` (janela incompleta mostra nada). Com a série terminando em
jul/2026, a conta corrente de 2026 saía **−36,0 contra −66,7 de 2025** — lê-se como melhora de
46% e é o ano pela metade. Era invisível enquanto era a última barra de um gráfico; virou uma
coluna rotulada "2026" quando a aba ganhou tabela. É o segundo achado desta sequência em que
**o defeito era antigo e o que mudou foi só a visibilidade**.

**E o terceiro foi o maior: a aba Fluxo Cambial lia a tabela errada.** Descoberto ao ir aplicar
o formato de tabela nela — `cmb_fluxo_cambial.total_saldo` vai de 81,0 a 82,9 em 307 meses e
**nunca troca de sinal**, contra 107 trocas em 216 meses no dado real; correlação entre os dois,
**0,05**. Um saldo de fluxo cambial oscila em torno de zero por definição, e aquela série sobe
monotonicamente — é forma de estoque, não de fluxo. Os códigos SGS 24352/24363/24364/24369/
24370/24371 não são o que o docstring de `cmb_fluxo_cambial.py` afirma, e o próprio script já
registrava a dúvida sem nunca tê-la resolvido. A fonte certa já estava no banco:
`cmb_cambio_contratado` (Tabelas 13 e 14 dos Indicadores Econômicos Selecionados do BCB), com
todas as identidades fechando **exatamente** em 4.501 dias. A aba foi reconstruída sobre ela, em
3 seções no formato tabela-árvore, e foi para o 2º lugar no nav. **Pendente:**
`agent_data.get_fx_snapshot()` ainda alimenta o subagente `cambio-analyst` com a série errada, e
a tabela/ETL `cmb_fluxo_cambial` precisa ser corrigida ou dropada.

**A aba Posicionamento do BCB foi para o 3º lugar e ganhou duas árvores** (2026-08-27, pedido do
usuário) — e o que ela ensinou vale para qualquer tabela hierárquica futura: **a fábrica
`makeTreeChartTab()` só sabia agregar fluxo**. Toda a sua agregação passa por `aggregateSum()`, e
apontá-la para um **estoque** faz "Trimestral" somar três meses de reservas — ~1.100 USD Bi, errado
por 3x, sem exceção nenhuma e numa ordem de grandeza que ainda parece um gráfico de reservas. Ela
ganhou `stat: 'last'` e um `aggregateLast()` que toma a **última posição do bucket**, não o último
valor não-nulo (mês de fechamento sem dado é "não sei", não o mês anterior carimbado com a data do
fechamento), mantendo a regra de bucket incompleto. E o toggle **"% do PIB" troca de denominador
junto**: estoque não tem "PIB do trimestre" que lhe corresponda, então a razão é contra o PIB de
**12 meses até a data** (~14% hoje) — a asserção que importa não é a magnitude, é que o número
**não muda de escala** quando o seletor de agregação muda. A árvore de reservas é o template do FMI
(SGS 3546–3556/7323, aditividade fechando na fonte com resíduo máximo 0,010 USD Bi em 307 meses) e
começa em jan/2001, onde a decomposição começa; a história desde 1971 fica no gráfico de manchete,
que **não é árvore de propósito** — liquidez e caixa são dois conceitos do mesmo agregado, e
pendurar um no outro quebraria a aditividade. As **intervenções** expuseram um detalhe do ETL que
muda a leitura: `cmb_reservas_bc.py` **descarta os zeros** das 4 séries, então dia ausente é
intervenção zero e não dado faltante, e a janela de publicação **não pode sair do `max()` das
próprias séries** (2023 não tem um único registro de mercado à vista — cortar ali esconderia meses
de zeros que são informação); ela vem de `reserves_total_daily`. Saíram o gráfico solto de **ouro**
(virou linha da árvore: isolado lia como decisão de política quando quase toda a variação é o preço
do metal) e o de intervenção **diária** (virou a árvore mensal — em base diária a barra empilhada é
um traço de 1px num eixo de 27 anos, que é o que motivou o pedido). Achado lateral: as SGS 29534 e
29535 estavam no payload e **nunca tinham sido desenhadas**. E a seção de posição cambial ganhou
tabela **mesmo não sendo hierarquia**, também a pedido do usuário — o argumento que vale reter é que
quase tudo que a fábrica de árvores entrega (célula mês a mês, caixa que plota, cor casando tabela e
legenda, cartão de definição, cabeçalho, régua) **não depende de hierarquia**; só o recuo, a seta de
expandir e a regra barra/linha dependem. Então ela roda com uma árvore plana e os três controles que
não se aplicam ficam **desligados**, incluindo o de barras — empilhar quatro exposições que não somam
um total seria inventar um agregado, não escolher uma visualização.

**A aba Mapa de Calor — BP foi removida em 2026-08-27**, a pedido do usuário: eram 3 painéis de
z-score (média/desvio móveis de 12 trimestres) sobre a mesma hierarquia do BP que a aba Balanço de
Pagamentos já mostra em tabela. O relatório ficou com **5 abas de dados** e caiu de 2,26 para 2,14 MB.
Saíram junto `rollingZScore()`, `renderHeatmapPanel()`, `applyHeatmapTextVisibility()`, `rowLabel()`
e o ramo de matriz `z` de `_extentPlotado()` — nada mais os usava. As 3 `BOP_TREE_*` **ficaram**: elas
nunca foram do heatmap, são a declaração em pedaços da árvore do BP.

📄 **Como gerar, arquitetura do relatório, mapeamento seção→schema→tabela, gotchas atuais, pendências:** [`analytics/brasil/exchange_rate/CLAUDE.md`](analytics/brasil/exchange_rate/CLAUDE.md) — carrega sob demanda quando o Claude lê arquivos dentro de `analytics/brasil/exchange_rate/`.

---

## analytics/brasil/inflation/ — Panorama de Inflação

Relatório HTML de decomposição do IPCA/IPCA-15. Decomposição por subitem vive em `macro_brasil` (`inflc_decomposicao` + `inflc_dim`); agregados BCB/SGS vêm de um CSV separado (`ipca_bcb_series.csv`, via `fetch_bcb.py`).

**A aba Decomposição virou uma tabela-árvore em 2026-08** (pedido do usuário), no formato de `analytics/brasil/credit`: o waterfall "Decomposição por Período" saiu e no lugar entrou linha expansível + checkbox que plota + 12 colunas de mês, com **duas árvores num seletor** — a estrutura de despesa do IBGE (9 grupos → 19 subgrupos → 53 itens → 614 subitens) e a classificação analítica do BC (Livres/Monitorados → …), eixos independentes em que nenhum deriva do outro. A do IBGE não existia no banco: virou 3 colunas em `inflc_dim`, e o parentesco **não precisou ser buscado** — o código de 7 dígitos já o carrega por prefixo, só os 81 nomes vêm da API, o que deixa o payload intacto. Os núcleos entram como bloco plano ao lado (se sobrepõem, não particionam o índice), com Contribuição sempre em branco e Peso só para os 7 por exclusão. O gráfico "Evolução Mensal" ganhou os **pills de profundidade** que o drilldown do waterfall fazia, mais um corte Top-14 + "Outros" — sem ele a profundidade Subitem empilharia 614 séries, já que era o *filtro* do drilldown, não o nível, que mantinha aquele nível legível. Cores da tabela: **verde >0, vermelho <0**, e só em Var. mensal e Contribuição — Var. 12M e Peso saem sem cor (o 12M é positivo em praticamente toda linha, então a cor viraria um bloco uniforme). É o inverso da convenção do ranking logo abaixo, daí classes próprias. Hierarquia é sinalizada duas vezes, pelo recuo e por um degradê de fundo/rótulo por nível. As legendas dos dois gráficos ficam **embaixo**, não na lateral. Todas as métricas saem com **2 casas decimais** — o que custa: 68,5% das células de contribuição no nível Subitem viram "0,00" (medido), daí o hover do gráfico manter 3 casas. `tests/test_inflation_js.js` (123 asserções, primeiro harness de JS deste relatório) fecha o invariante que importa: os filhos somam o pai em contribuição e em peso, em todos os pais e todos os meses, nas 3 combinações de árvore × índice.

📄 **Como gerar, arquitetura, mapa de dados, gotchas atuais, pendências:** [`analytics/brasil/inflation/CLAUDE.md`](analytics/brasil/inflation/CLAUDE.md) — carrega sob demanda quando o Claude lê arquivos dentro de `analytics/brasil/inflation/`.

**Aba "Inércia"** (2026-08): um corte novo dos mesmos subitens — não o que eles *são*, mas o quanto a
inflação deles **persiste**. Cada subitem é ranqueado por `corr(yoy_t, yoy_t−12)` numa janela fixa de
10 anos e cortado em 5 faixas de ~20% do **peso** do índice (`analytics/brasil/inflation/inercia.py`,
nada gravado no banco). A escolha da base foi medida, não suposta: no dado mensal bruto o lag 12 é um
detector de sazonalidade (os 8 primeiros são todos ensino, que reajusta em fevereiro), dessazonalizar
o mensal destrói o sinal, e o **lag 1 sobre o y/y é 97% construção** (0,921 real contra 0,895 da série
embaralhada, porque janelas consecutivas compartilham 11 meses) — só o lag 12 sobre o y/y tem janelas
disjuntas. A classificação passa no teste nominal com folga (Q5 = Plano de saúde, Empregado doméstico,
Mão de obra, Dentista; Q1 = Gasolina −0,44 e Energia elétrica −0,56), **mas não sobrevive fora da
amostra**: reestimando em 2006-2016, o Q5 continua Q5 em só 24% contra 20% de acaso. É uma etiqueta de
janela, não uma propriedade do produto, e a aba diz isso na própria nota.

Desde 2026-08 a aba tem **duas tabelas do mesmo `r`**, que só discordam em onde cortar: a de
quintis iguala o **peso** e deixa os limites andarem; a de **reversibilidade** fixa os limites em
±0,5 e deixa o peso sair desigual — 6,1% / 24,6% / **66,8%** / 2,5%, porque a distribuição de `r` é
unimodal em torno de +0,02 e ±0,5 só pega as caudas. A segunda é a menos estável das duas: as
pontas retêm 13% e 4% dos subitens fora da amostra (κ +0,11; +0,22 só no sinal), por regressão à
média. Nenhuma das duas mostra os núcleos (não particionam o índice), e o ramo "Não classificado"
— 237 subitens descontinuados que só rendiam travessão — saiu; eles seguem somando na raiz, que
continua sendo o índice publicado. Achado lateral que muda a leitura de tudo isso: o erro-padrão
que o hover mostra (`1/√n` ≈ 0,10) **subestima 2-3×** — as janelas de y/y se sobrepõem, e o
bootstrap por blocos dá 0,16-0,28 (a série embaralhada concorda, dp 0,24).

---

## analytics/brasil/monetary_policy/ — Modelo agregado do BC, cenários e Curva de Phillips

A réplica do modelo pequeno do BCB foi **removida em 2026-08** (junto com as tabelas
`pm_hiato_seed`/`pm_parametros`), e um modelo novo será construído sobre a extração automatizada do
anexo do RPM (`pm_hiato_produto`/`_vintages`). Ficaram o `phillips_excel.py` (Curva de Phillips
estimada → planilha de auditoria célula a célula) e o material de referência.

**O modelo agregado do BC foi replicado de ponta a ponta** (2026-08-21), do boxe do RI de
jun/2024: `modelo_painel.py` (painel trimestral, dois recortes de janela de HP) +
`modelo_agregado.py` (espaço de estados, estimação, decomposições, simulador de cenários) →
`generate_report.py` → `reports/brasil/Monetary Policy.html`. Desde **2026-08-25 o relatório tem
4 abas**: **Modelo BC — Agregado** (default), Condições para a reunião, Projeções do Copom
(que desde 2026-08-25 é também onde vive a previsão da próxima projeção do BC) e Apêndice — as abas Cenários, Decomposição, Taxa Neutra e Hiato do Produto foram apagadas a pedido do
usuário, com os loaders delas (os artefatos de `data/` continuam sendo gravados e alimentam o motor
e o teste). A
aba default é a única do projeto em que o modelo roda **no navegador**: o simulador está portado para JS, e a seção de inputs segue a estrutura da aba Ridge
do FX Report (uma caixa por trimestre sempre visível, atalhos que preenchem as caixas, gráfico por
input, cenários com plotar/carregar/editar). Cada input é endógeno, premissa ou estimativa do
modelo, e os cenários ficam no `localStorage`. A Selic pode ser resposta ali, pela
eq. (3) — extensão nossa, o `simular()` do Python só a aceita como caminho dado.

Validação: **17 dos 22** parâmetros dentro do intervalo de credibilidade de 90% que o próprio BC
publica, hiato latente com correlação **0,990** contra o `pm_hiato_produto`, e — o teste mais direto
de implementação — **o mesmo motor rodado com as modas publicadas reproduz o IRF do BC com erro
absoluto médio de 0,030 p.p., picando no mesmo trimestre**. O que sobra de diferença no IRF com os
nossos parâmetros é estimativa, não código.

**A equação (5) de expectativas está resolvida no simulador** (2026-08-21): o modelo é linear, então
o ponto fixo é um sistema afim `(I−G)π^e = g`, resolvido de uma vez em vez de iterado (resíduo 1e-14).
Isso reconcilia a nota antiga de que "Fair-Taylor divergiu por instabilidade" — o motor de então
aproximava a Selic esperada pela corrente, o mesmo bug que inflava o IRF 4-5x, e era ele que inflava
o laço; com `i^e` lido do caminho de juros o raio espectral cai para 0,68. Mas a fronteira é real:
passa de 1 em φ₂ ≈ 0,32, e acima disso a condição terminal passa a determinar a resposta. Os φ vêm
de estimador próprio (`estimar_eq5`, mínimos quadrados não lineares, R² 0,898); no filtro π^e segue
como dado observado da Focus. **A única premissa que sobrou no cenário são os preços administrados.**
306 asserções em `tests/test_monetary_policy_js.js` e 19 em `tests/test_eq5_expectativas.py` — as
seções 19-25 do primeiro rodam o motor JS nas **mesmas 12 configurações** que o Python pré-simulou e
exigem que batam série a série (discrepância máxima 5e-5, o piso do arredondamento do payload).

**Aba "Condições para a reunião"** (2026-08-25, `condicoes_copom.py`): o conjunto de
informação que o Copom tinha na última decisão contra o que já está na mesa para a próxima,
17 variáveis em heatmap hawk/dove — inflação corrente, atividade e mercado de trabalho,
expectativas da Focus e condições financeiras —, mais a agenda das divulgações que ainda
alimentam essas linhas até o corte. Renova-se
sozinha quando uma reunião passa; sem histórico de reuniões anteriores, por decisão explícita.
O ponto todo é a **regra de corte**: o comunicado sai no fim do dia 2 (~18:30), e uma série
mensal é indexada pelo *mês de referência*, não pela data em que existiu — o IPCA de julho
está no banco com data 01/07 e saiu em ~13/08, então na reunião de 05/08 o Comitê estava com
o de junho. Ler o banco por `date <= reunião` daria julho sem lançar exceção nenhuma. As
datas de divulgação vêm do `domain/release_calendar/`, com regra ajustada (e erro máximo
medido) onde o arquivo não cobre. Duas correções que mudaram o resultado: `_sa()` começa em
2000 (com a série desde 1980 o "dessazonalizado" saía mais volátil que o bruto) e σ é escala
robusta, não desvio-padrão.

**Antecipar a projeção do BC** (2026-08-25, `antecipa_copom.py`): prever que número o Copom vai
publicar para o horizonte relevante na próxima reunião, por âncora + delta (o alvo é 6 trimestres à
frente do trimestre da reunião, então reuniões consecutivas compartilham o alvo e o BC já publicou
um número para ele). **Desde 2026-08-25 a previsão está na aba Projeções do Copom**, como ponto em
losango vazado no fim da série e caixa verde com a procedência; o relatório lê dois artefatos de
`data/` e não roda o modelo. **O modelo agregado não serve para isso, e o backtest mede**: nas 17 reuniões
da era declarada o MAE é 0,145 com os nossos parâmetros e 0,208 com as modas publicadas do BC,
contra 0,106 do ingênuo "não vai revisar". O que ganha é o **delta da própria Focus** para o mesmo
trimestre — MAE 0,082, direção em 9 de 12, correlação 0,70 com a revisão do BC. A causa é o conjunto
de informação, não o ajuste: a revisão do BC vem do IPCA mensal novo, que a pesquisa semanal lê e um
modelo trimestral não — aqui t0 fica até 4,5 meses atrás da reunião. Achado lateral que vale por si:
**o BC declara no RPM a taxa real neutra que usa** (4,50% até jun/2024, 4,75% da 263ª, 5,00% da
267ª, reafirmada em jun/2026), e não é a mediana das medidas do boxe; trocar a nossa de 7,81% por
esses 5,00% move 2028T1 de 3,45 para 3,07 contra 3,2 publicado, e vira o hiato de +0,35 para −0,75.
A frase não está no `raw_md` (a extração guarda só páginas com tabela), está nos PDFs.
A pergunta prática de se isso só funciona quando o alvo já tem número publicado tem resposta medida:
das 17 reuniões, **9 são expansão de horizonte e 8 revisão, perfeitamente alternadas** (duas reuniões
por trimestre, uma edição do RPM por trimestre), e a expansão **não exige extrapolar nada** porque o
RPM publica o caminho trimestral contíguo — nas 9 a âncora é ele. A expansão é até o caso mais fácil
(MAE 0,080 pela Focus contra 0,089 do ingênuo, contra 0,084 e 0,125 nas revisões), e o motivo é o
intervalo: âncora a 34-41 dias da reunião contra 35-49.

**Aba "Projeções do Copom"** (2026-08-25): a projeção do BC para o horizonte relevante
contra o **passo de Selic da mesma reunião** — o que o Comitê projetava contra o que ele fez,
107 reuniões de 1999 a 2026. O lado da decisão veio de tabela nova, `pm_copom_reuniao`: 247
reuniões desde 1999, derivadas da SGS 432 (meta diária) cruzada com o calendário de reuniões,
não do texto do comunicado — aquele só é parseado da 206ª em diante. O comunicado entra como
conferência independente, e nas 63 reuniões em que escreve a decisão em prosa as duas fontes
concordam em todas. O passo é o **daquela reunião**, não o acumulado do ciclo (decisão explícita
do usuário). Duas escolhas fazem o gráfico: a **janela de cinco dias** para o passo, que é
medida e não escolhida (147 das 152 mudanças entram 1 dia depois da reunião, 4 em 2 por feriado
na quinta e 1 em 5; os 8 movimentos por viés estão todos a 7 dias ou mais, então cinco dias
separa decisão de viés exatamente); e **uma unidade de horizonte só** — sempre 6 trimestres, o
que exclui de propósito as 14 reuniões de 2020-2024 em que o comunicado chamava de horizonte
relevante um ano civil, cuja distância encurta de 12 para 4 trimestres ao longo do próprio ano.
Correlação desvio-da-meta × passo: 0,27, e a fraqueza é por construção — se o Copom já reagiu,
a projeção condicionada aos juros esperados volta para perto da meta. Em **2026-08-25 a aba ganhou a
previsão da próxima reunião** e a dispersão desvio × passo saiu no lugar dela, a pedido do usuário:
onde estava a nuvem de pontos agora está o **backtest** — o que cada um dos três métodos teria dito
contra o que o BC publicou, nas 17 reuniões, com pill de nível ou erro e a linha de MAE na tabela. O
pill de **previsão** (delta da Focus | modelo | ingênuo) governa as duas coisas ao mesmo tempo: o
ponto previsto no primeiro gráfico e o método em destaque no backtest. Com isso a aba deixou de ter
gráfico que não é série temporal em X, e a exceção ao `_reactPreserveX` que a dispersão documentava
desapareceu junto.

**Projeções do próprio BC → `pm_copom_projecoes`** (2026-08): as duas publicações de política
monetária viraram uma tabela só, separadas pela coluna `documento`. O **comunicado** de decisão (233
reuniões, 48ª/2000-06 → 280ª; carga da 206ª, 396 linhas) e o **Relatório de Política Monetária** (RI
até 2024-12; **109 edições de 1999-06 a 2026-06**, 1.967 linhas de 108 delas), ambos versionados em
`repository/monetary_policy/raw_md/`. É a contrapartida oficial do `expc_focus*`: o que o BC projeta,
não o que o mercado espera. O relatório não é redundante — publica o caminho trimestral **contíguo**,
então o ponto a 6 trimestres existe em toda edição e a série de horizonte relevante passou de 52 para
**150 pontos, começando em 1999-09**. Onde os dois cobrem a mesma célula batem exatas da 264ª reunião
em diante (60/60); antes divergem 0,037 p.p. em média, porque o relatório é vintage posterior e em
2017-2020 o comunicado publicava o cenário híbrido. Levantamento das duas fontes em
[`copom_comunicados.md`](domain/db/brasil/bcb/copom_comunicados.md) e
[`relatorio_politica_monetaria.md`](domain/db/brasil/bcb/relatorio_politica_monetaria.md).

📄 **O que foi removido e por quê, a lacuna da curva forward que não deve ser repetida no modelo novo,
conteúdo de `referencia/`/`models/`, pendências:**
[`analytics/brasil/monetary_policy/CLAUDE.md`](analytics/brasil/monetary_policy/CLAUDE.md) — carrega sob
demanda quando o Claude lê arquivos dentro de `analytics/brasil/monetary_policy/`.

---

## analytics/brasil/expectations/ — Panorama de Expectativas (Focus)

Relatório de **escopo fechado** (2026-08-24): lê `expc_focus`, `expc_focus_copom` e
`expc_focus_periodo` e **nada mais** — sem meta de inflação, sem realizado, sem projeção do Copom, por
decisão explícita do usuário. 8 abas: Boletim (mediana de hoje × 1/4/12/52 semanas), Revisão (fixa o
período previsto e varre as datas de pesquisa, com eixo alternativo em "meses até o período"), Curva
do Copom (curva por reunião + horizonte ao longo do tempo + mapa de calor), Horizonte Móvel, Trajetória
(a curva à frente inteira numa semana), Dispersão, Bases (0 × 1) e Apêndice.

**A aba Boletim virou uma tabela que chama gráfico** (2026-08-27, pedido do usuário): os cartões de
KPI saíram e clicar numa linha plota a série daquele indicador *para aquele ano de referência* — eixo
X = data da pesquisa, então se lê como a projeção do ano foi se formando (o IPCA de 2026 saiu de 3,00
em jan/2022 para 5,02). Cada rótulo ganhou o botão `i` do padrão `lis-dashboard`, com os 28
indicadores definidos num mapa `INFO`. Duas coisas foram **medidas** para os cards não afirmarem o
que não se sabia: a `Taxa de desocupação` anual do Focus é **fim de período** (erra 0,2 p.p. contra o
trimestre out–dez da PNAD e 1,1 p.p. contra a média do ano), e o **saldo da balança comercial não é
`Exportações − Importações`** — são três perguntas separadas, e mediana de diferença não é diferença
de medianas: 3,4 US$ bi de discrepância média em 8.310 datas, coincidindo em só 4,8% delas.

O que resolve o problema de tamanho: **grade semanal global** (1.425 semanas) e séries comprimidas
como `{i0, m[], s[], n[]}` — 1,28 M de linhas viram um payload de 5,6 MB. Duas regras de redução
diferentes de propósito (JOIN com o `MAX(date)` da semana na `expc_focus_periodo`, para a tabela do
Boletim ser transversal a uma mesma data de pesquisa; último ponto por série nas outras duas). Dois
testes: `tests/test_expectations_js.js` (framework + os 8 renderizadores contra o payload real) e
`tests/test_expectations_data.py` (o **arquivo gerado** contra o MySQL, valor a valor — a compressão
desloca séries no tempo sem lançar exceção nenhuma).

📄 **Abas, grade/compressão, gotchas da fonte e pendências:**
[`analytics/brasil/expectations/CLAUDE.md`](analytics/brasil/expectations/CLAUDE.md) — carrega sob
demanda quando o Claude lê arquivos dentro de `analytics/brasil/expectations/`.

---

## Extração de PDFs para bibliography

Ao converter PDFs em `.md` para alimentar o agente de análise, use a seguinte lógica de roteamento:

| Tipo de PDF | Abordagem | Custo |
|---|---|---|
| Born digital, coluna única (ex: cartas Verde) | Script `utils/extract_pdf.py` (pdfplumber) | Zero tokens |
| Artigos acadêmicos 2 colunas, relatórios de research | Ler com Claude diretamente na sessão (Read tool) | Zero tokens extras (já na sessão) |
| PDFs novos complexos num pipeline automatizado | API Claude Haiku via `anthropic` SDK | ~$0.02/artigo |
| PDFs escaneados (sem camada de texto) | Nenhuma das opções acima funciona — usar OCR externo | Variável |

**Regras:**
- Para as cartas da Verde (81 PDFs, coluna única, born digital): sempre usar o script.
- Para papers acadêmicos e relatórios de research na `repository/`: ler na sessão e gerar `.md` estruturado diretamente.
- A estrutura `.md` (headers, seções) só importa para legibilidade humana no Obsidian. Para o agente, texto limpo é suficiente.
- Nunca usar `pypdf` para PDFs de 2 colunas — a ordem de leitura fica errada.
- `pdfplumber` e `pymupdf` produzem Unicode correto (ç, ã, é) — o display `?` no terminal Windows é apenas artefato de codepage, não corrupção.

---

## repository/ — curated knowledge base (bibliography + conceptual maps)

Since 2026-07, organized by topic area (exchange rate, monetary policy, trader, and future ones: economic activity, fiscal policy, inflation, labor market), each with a literature → data → conceptual map pipeline. Named `agent_bibliography/` before — old name still turns up in git history/older docs, treat as a synonym. Doesn't use or reconcile with `obsidian/`'s own concept/synthesis pages — deliberately parallel systems, per explicit user instruction. Does interact with `repository/ingestion/` (2026-08) — that's the PDF ingestion pipeline itself, living inside this tree: drop a PDF in `repository/ingestion/land_space/<topic>/`, run `repository/ingestion/scripts/run.py`, and it populates `raw_pdf/`/`raw_md/`/`clean_md/` in one command.

📄 **Folder structure, methodology, per-topic status, and pending items:** [`repository/CLAUDE.md`](repository/CLAUDE.md) — loads on demand when Claude reads files inside `repository/` (unlike this root file, which loads in full every session).

**Three branches of exchange-rate material (2026-07):**
1. **Curation** (`repository/exchange_rate/` + `repository/agent_mapping/*`) — literature → conceptual map pipeline. Not team-facing, it's the base that feeds the agent. Full detail in `repository/CLAUDE.md`.
2. **Consolidated** (`team_materials/agent_materials/exchange_rate/`) — condensed, presentable synthesis for team discussion (bibliography, conceptual map, data inventory, EN/PT introduction, two interactive HTML explorers).
3. **Analytical** (`analytics/brasil/exchange_rate/`) — applied/analytical branch, same pattern as `analytics/brasil/inflation/` (code + HTML report + `referencia/`). See its own section above.

---

## obsidian/ — Vault de conhecimento macro

Vault Obsidian cross-linked por área macro (`exchange_rate`, `monetary_policy`, `inflation`, `fiscal_policy`, `labor_market`, `economic_activity`), voltado para leitura/navegação por humanos e agentes — não é um arquivo de material bruto. Cada tópico segue um modelo de três camadas: `concepts/` (notas atômicas de teoria, densamente linkadas), `sources/` (material completo por fonte, só com boilerplate/disclaimers removidos — equivalente ao `clean_md` do `repository/`, nova em 2026-08 e ainda vazia), `synthesis/` (notas condensadas por fonte, já populadas para várias áreas). Deliberadamente paralelo ao `repository/`'s `agent_mapping/`, por instrução explícita do usuário — mas as duas árvores passaram a compartilhar a camada de extração bruta em 2026-08 (ver histórico abaixo).

📄 **Definição de cada camada, status por tópico, histórico da reorganização de 2026-08, pendências:** [`obsidian/CLAUDE.md`](obsidian/CLAUDE.md) — carrega sob demanda quando o Claude lê arquivos dentro de `obsidian/`.

---

## Gerenciamento de pacotes: uv + pyproject.toml

📄 **Documentação completa:** [`AMBIENTE.md`](AMBIENTE.md) — racional do `uv`, papel de cada arquivo (`pyproject.toml`, `uv.lock`, `.venv`), setup em máquina nova, como atualizar versões, manutenção e troubleshooting. Resumo abaixo.

```powershell
# Adicionar pacote
uv add nome-do-pacote

# Configurar em nova máquina
uv sync
uv pip install -e .   # instala o projeto em modo editável (necessário uma vez)
cp .env.example .env
# Editar .env com credenciais
```

**Nunca** usar `pip install` direto — o `pyproject.toml` não será atualizado.

### Instalação editável (`uv pip install -e .`)

Cria um `.pth` no venv que aponta para a raiz do projeto, resolvendo todos os imports (`connectors`, `domain`, `analytics`, `utils`) independentemente de onde o script é executado. Deve ser rodado **uma vez** em cada máquina após `uv sync`. Sem isso, `python jobs\update_oraculo.py` falha com `ModuleNotFoundError: No module named 'analytics'`.

Todos os pacotes Python do projeto (`connectors/`, `domain/`, `analytics/`, `utils/`) precisam ter `__init__.py` para serem encontrados pelo `setuptools.packages.find`.

---

## Pendências (próximas sessões)

Cada relatório em reconstrução tem seu próprio "Pending" atualizado no `CLAUDE.md` da pasta — histórico
rodada-a-rodada de como cada um chegou ao estado atual vive só no git log, não aqui.

### Alta prioridade
- **`analytics/brasil/exchange_rate/`**: ver "Pending" em [`analytics/brasil/exchange_rate/CLAUDE.md`](analytics/brasil/exchange_rate/CLAUDE.md).
- **`analytics/brasil/inflation/`**: ver "Pending" em [`analytics/brasil/inflation/CLAUDE.md`](analytics/brasil/inflation/CLAUDE.md).
- **`analytics/brasil/economic_activity/`**: 6 abas (PIB, Produção Industrial, Comércio, Serviços, IBC-Br,
  Apêndice), framework interativo comum às 5 abas de dados (multiselect, toggle Y/Y↔acumulado, momentum
  scatter/heatmap); só a aba PIB tem decomposição de crescimento (as outras 4 não têm tabela de
  peso nominal/taxa oficial). Ver "Pending" em
  [`analytics/brasil/economic_activity/CLAUDE.md`](analytics/brasil/economic_activity/CLAUDE.md) — falta principalmente
  confirmar visualmente num browser real (sandbox sem browser disponível).
- **`analytics/brasil/fiscal_policy/`**: 5 abas (Receitas e Despesas GFSM+RTN — aba padrão, com seletor de Esfera
  União/Estados/Municípios/Geral —, Dívida Líquida/DLSP — 9 tabelas, uma por fator condicionante, nova em
  2026-08 —, Investimento — GND × função e GND × natureza, nova em 2026-08 —, Impulso Fiscal/IEG,
  Apêndice). Das 3 abas antigas apagadas a pedido do usuário, Dívida
  Pública foi superada pela nova aba Dívida Líquida (fonte melhor); Visão Geral e Resultado Fiscal seguem
  sem reconstrução. Ver "Pending" em [`analytics/brasil/fiscal_policy/CLAUDE.md`](analytics/brasil/fiscal_policy/CLAUDE.md)
  (inclui o double-count de transferências intergovernamentais no total Governo Geral, re-estimação dos
  multiplicadores do IEG, e o bloqueio do MEFA).
- **`analytics/brasil/credit/`**: substituiu `analytics/credit_stress/` (removida junto com a tabela
  `insolv_falencia_rj` e `connectors/datajud.py` a pedido do usuário — histórico só em git log). Hoje
  tem Saldo (+ 2ª tabela para Crédito Ampliado), Concessão (ambas via a fábrica JS `makeHierTab()`,
  toggle Nominal/Real/% PIB), Taxa & Spread e Inadimplência (formato bespoke, com overlay de Selic), +
  Impulso (3 tabelas via `makeImpulseTab()`) e PTC (`cred_ptc`, nova em 2026-08 — árvore
  Oferta/Demanda × 4 segmentos, pill Observada|Esperada, sem linha de total, régua da escala
  −2..+2 no topo, mais uma 2ª tabela+gráfico de **surpresa**: o desvio
  `observada(t) − esperada(t−1)` em **média móvel de 4 trimestres** na tabela e nas linhas grossas
  do gráfico, com o trimestre cru na linha fina; faixa "em linha" = |MA| ≤ σ₀ da própria MA (RQM em torno de zero, não sd em torno da
  média — a troca foi um bug corrigido em 2026-08) — um
  critério de 1/N foi tentado antes e retirado, ver o CLAUDE.md da pasta), + Apêndice.
  Ver "Pending" em [`analytics/brasil/credit/CLAUDE.md`](analytics/brasil/credit/CLAUDE.md) (confirmação em
  browser real, `cred_credito_controle_capital.saldo`/`provisoes` ainda não charteados).
- **`analytics/brasil/expectations/`**: construído e testado em 2026-08-24; falta **confirmação
  visual num browser real** — em especial o mapa de calor da aba Copom (único gráfico não-linha) e o
  eixo invertido da aba Revisão. Ver "Pending" em
  [`analytics/brasil/expectations/CLAUDE.md`](analytics/brasil/expectations/CLAUDE.md).

### Média prioridade
- **Expectativas Focus — consumo nos relatórios**: **o relatório dedicado existe desde 2026-08-24**
  (`analytics/brasil/expectations/` → `reports/brasil/Expectations.html`, 8 abas sobre as 3 tabelas e
  nada mais — inclusive o gráfico de convergência, que só a `expc_focus_periodo.data_referencia`
  permite). O que segue pendente é o consumo **dentro das outras áreas**, onde a expectativa entra
  cruzada com meta/realizado/modelo — coisa que o relatório de escopo "só Focus" deliberadamente não
  faz. Por ordem de retorno: (a) `expc_focus_copom` no modelo de política monetária — é a curva
  forward cuja ausência produziu o IRF 4-5x maior que o do BCB na réplica removida (o motor
  aproximava a Selic futura pela taxa corrente); o `MODEL_REPLICATION_PLAN.md` registra que
  `i^e_{t,t+4|t}` precisa da média ponderada 0,5/1/1/1/0,5 dos 4 trimestres à frente; (b) aba de
  expectativas em `analytics/brasil/inflation/` — o que o Panorama de Expectativas não pode mostrar:
  as medianas anuais **contra `inflc_meta`**; (c) diferenciais ex-ante em
  `analytics/brasil/exchange_rate/`, pendência já aberta em 3 `CLAUDE.md`; (d) consenso vs. realizado
  em `economic_activity/`, `fiscal_policy/` e `labor_market/`.
- **Focus Top5 não carregado**: os 6 endpoints Top5 têm a mesma forma de chave das 3 tabelas mais a
  dimensão `tipo_calculo`, que já existe na chave com valor `'geral'` — então é backfill de dados,
  não migração. Só vale se a leitura "consenso vs. Top5" interessar. `base_calculo=1` na
  `expc_focus_periodo` está na mesma situação.
- **Mercado de trabalho — pendências pós-Novo CAGED** (o conector do FTP e as 3 tabelas de corte
  ficaram prontos em 2026-08, ver `domain/db/brasil/mte/` e `analytics/brasil/labor_market/fontes_dados.md`;
  a rotulagem estoque-vs-saldo de `mt_caged.py` e a integração das 3 tabelas ao relatório foram
  resolvidas em 2026-08, ver a aba "Emprego Formal"):
  (a) cortes do microdado ainda não modelados: município, ocupação (CBO), sexo/idade/instrução/raça
  — todos disponíveis no mesmo microdado já baixado, adicionar é só uma tabela irmã nova com o
  mesmo padrão (`categoria`/`metrica`), sem migração;
  (b) `mt_pnad_trimestral`: nível UF/N3 deixado de fora deliberadamente, sem previsão.
- **US — expandir dados**: mapeamento de fontes das 8 áreas macro pronto em [`us_project/`](us_project/)
  (levantado ao vivo contra as APIs, 377 séries FRED conferidas uma a uma). Prontos: `connectors/bls.py`
  (2026-08, substitui o stub morto de `not_in_production/`; chave da API instalada no `.env`, limites
  medidos ao vivo — 50 séries / 20 anos por requisição) e a hierarquia do CPI em
  [`us_project/inflation_hierarchy.md`](us_project/inflation_hierarchy.md) (as **duas** árvores: a de
  despesa, 355 itens × 10 níveis na versão carregada, e a do news release, 37 linhas × 5 níveis — food/energy/core goods/
  core services, extraída da Tabela 1 do release, onde o BLS declara a hierarquia na própria marcação
  HTML; validada com 111/111 índices publicados batendo com a API).
  **O ramo de inflação está construído** (2026-08): schema `macro_us` com 5 tabelas
  (`inflc_cpi` 341 mil linhas 1913→hoje, `inflc_cpi_dim` as 2 árvores, `inflc_cpi_pesos` 2020-2025,
  mais `inflc_pce` 608 mil linhas 1959→hoje e `inflc_pce_dim`),
  ETL em `domain/db/us/inflation/` + `jobs/update_us.py`, e o relatório em `analytics/us/inflation/`.
  Validado contra a Tabela 1 publicada: os 111 índices conferem exatos e o headline/core/energy/food
  y/y batem na arredondamento do BLS. A importância relativa que a Tabela 1 imprime é *reconstruída*
  da planilha de dezembro (as 37 publicadas batem em 0,0008), então não há tabela de pesos mensais a
  carregar.
  **Em 2026-08-26 o relatório foi remodelado sobre o do Brasil, a pedido do usuário**: a visão
  "Table 1" saiu (reimprimia uma tabela que o próprio BLS publica no dia), as **duas árvores do CPI
  viraram um seletor dentro de uma aba só** — como as árvores IBGE/BC da aba Decomposição do relatório
  de inflação do Brasil, com marcas e ramos abertos guardados *por árvore*, já que as duas compartilham
  centenas de códigos — e a aba ganhou as duas leituras que faltavam: **maiores contribuições no
  período** e o **drilldown de componentes em 12 meses**. Duas coisas medidas nessa rodada valem por si.
  A contribuição na janela é peso × variação entre as pontas e **não** soma das contribuições mensais,
  porque **outubro de 2025 não foi divulgado** — é o único buraco da `inflc_cpi` (613 das 634 séries em
  branco, 21 com valor; paralisação do governo), e um mês sem índice apaga *dois* passos mensais, o que
  deixaria a coluna inteira vazia. E o ranking **imprime a própria cobertura**: ao contrário dos 614
  subitens do IPCA, nada aqui particiona o índice fora dos níveis 0-2 da árvore de divulgação — as
  folhas dela carregam 60,0 de 100 —, então a linha de rodapé diz quanto peso as linhas ranqueadas
  cobrem e quanto as contribuições somam contra o headline.
  **O PCE entrou em 2026-08-20** como 3ª aba do mesmo relatório, e sem precisar da chave do BEA que
  estava registrada aqui como pendência: o BEA publica as tabelas 2.4.4U (índice de preço) e 2.4.5U
  (despesa nominal) num xlsx aberto de 12 MB, mensais desde 1959, e as duas casam **linha a linha** —
  368 linhas
  de árvore em 9 níveis + 34 agregados de addenda. É fonte melhor que a do CPI em três pontos medidos:
  os **níveis 1-4 particionam o índice exatamente** (contra 0-2 da árvore de divulgação do CPI), o peso
  é **mensal** em vez de snapshot de dezembro, e a contribuição reconstrói o headline com 0,0009 p.p. de
  erro médio contra 0,0124 do CPI. O detalhe que não se adivinha: **19 linhas entram subtraindo** no
  total e só 4 dizem `Less:` no rótulo — a subárvore inteira herda o sinal, e somar um nível sem isso dá
  116% do PCE.
  **A chave do BEA chegou em 2026-08-26 e o passe de rotina ficou 100% API, sem baixar arquivo
  nenhum.** Os valores vêm da API (608.442 observações conferidas uma a uma contra o xlsx, zero
  diferentes). A **árvore** é o caso interessante: ela só existe no xlsx — a API não publica
  hierarquia em nenhum dos 13 datasets, e o próprio serviço responde que existem só 4 métodos —, mas
  ela não muda de mês para mês, então é **gravada e reaproveitada**. Cada rodada relê a estrutura do
  MySQL e usa a API para *provar* que ela continua valendo: mesmo conjunto de linhas, aditividade
  fechando em nominal sobre o parentesco gravado, níveis 1-4 em 100%. Passando as três, só a
  cobertura é reescrita; falhando qualquer uma, o xlsx é baixado e a árvore reconstruída. Verificado:
  a rota só-API grava tabela **idêntica** à reconstrução completa. `tests/test_bea_api.py` (60
  asserções) fecha o triângulo API = xlsx = PCEPI/PCEPILFE do FRED (exato em 19 meses) e exercita as
  duas metades do guarda, inclusive re-indentação — mover uma linha de pai produz resíduo de US$ 810
  bi, 405 mil vezes o limite de arredondamento. Três achados que custaram uma rodada de depuração
  cada: o BEA **revisa meses anteriores em cada divulgação** (junho/2026 saiu de 131,392 para 131,454
  em 26/08), então valor de mês fixo em teste envelhece; a API **devolve registro só onde há dado**,
  então numa janela curta as 2 linhas `ZZZZZZ` e as descontinuadas em 2001 faltam legitimamente; e o
  **SeriesCode codifica a medida** (`DPCERG` no índice, `DPCERC` no nominal), que é por que a dim
  guarda o código do índice e `_validar_casamento` nunca comparou código entre as abas.
  **Falta**: as outras 7 áreas macro (só `bls.py` e `bea.py` existem), os pesos pré-2020 do CPI (existem
  desde 1947 no site do BLS, em 2 formatos antigos sem parser — é lacuna de parser, não de dado),
  CPI-W/C-CPI-U (schema e loader suportam, não carregados) e, do lado do PCE, as tabelas **reais** nas
  mesmas 402 linhas (2.4.3U índices de quantidade e 2.4.6U dólares encadeados — seriam um `medida` novo
  na mesma árvore, mas são atividade, não inflação: pelo critério de prefixo temático virariam `atv_`).
  **As datas de divulgação entraram em 2026-08-26**: `connectors/us_agenda.py` + os grupos `bls_cpi`
  e `bea_pce` no calendário, e uma faixa no topo do relatório com última/próxima divulgação, hora em
  ET e em Brasília (convertida por data — os EUA têm horário de verão e o Brasil não) e o mês de
  referência que cada uma entrega. Adicionar série nova é declarativo: um bloco `us:` no grupo.
  Com isso o botão "Atualizar" do calendário passou a valer para CPI e PCE também.
  Ver "Pending" em [`analytics/us/inflation/CLAUDE.md`](analytics/us/inflation/CLAUDE.md).
- **`repository/` — curation pending items** (conceptual maps, bibliography gaps, trader scope): ver "Pending" em [`repository/CLAUDE.md`](repository/CLAUDE.md).
- **Jobs de rotina incompletos** (a checagem de freshness em `domain/release_calendar/sync.py` confirmou
  em 2026-08-17 que isto causa atraso real, não só teórico: `comm_icbr`/`comm_icbr_usd` estavam um mês
  atrás e avançaram ao rodar o script à mão). O `--continuous` do `update_db.py` (2026-08) fechou
  metade do buraco: `cmb_ptax`, `cmb_dollar_index`, `cmb_dollar_index_em`, `cmb_fx_latam`,
  `cmb_equity_us`, `comm_brent` e `cmb_policy_rates` já rodam por ele (via `registry.py`, mesmo as 6
  de `macro_international`), então basta agendar `update_db.py --continuous` diariamente. O que segue
  **sem nenhum job**, só à mão ou via `--tables`: `comm_icbr`/`comm_icbr_usd`/`inflc_meta` e
  `inflc_decomposicao_item` (este alimenta os núcleos MA/MS/DP do IPCA-15) em
  `domain/db/brasil/`, `clima_oni`/`cmb_real_rates` em `domain/db/international/`, e
  `cmb_risco_pais` (que por natureza não automatiza — CSV exportado à mão).
  `update_international.py` continua com 3 scripts só.
- **Órfãos de verdade são só duas tabelas** — `comm_brent` e `clima_oni`, ambas insumo da réplica do
  modelo do BCB removida em 2026-08: decidir se voltam a alimentar o modelo novo ou se são dropadas.
  A lista antiga de "órfãos" desta seção estava errada, conferida script a script em 2026-08-19:
  `comm_icbr` (ppp_equilibrium + ridge_deviation_model + phillips_excel), `comm_icbr_usd` e
  `inflc_meta` (ppp_equilibrium + phillips_excel), `atv_pib_usd` (generate_report do câmbio +
  ppp_equilibrium), `cmb_dollar_index`/`cmb_dollar_index_em`/`cmb_policy_rates`/`cmb_equity_us`
  (ppp_equilibrium) e `cmb_real_rates` (real_rates_comparison.py) todas têm consumidor vivo — o que
  a remoção da réplica quebrou foi menos do que se registrou na época.
- **`team_materials/agent_materials/exchange_rate/` — notas desatualizadas**: `data_inventory.md` ainda diz que o `conceptual_map.md` "não foi construído" (já foi); `introduction_pt.md` não lista o `conceptual_map.md` entre os documentos da pasta.
- **Kinea PDF órfão**: `team_materials/agent_materials/exchange_rate/kinea_fx_mental_models.pdf` existe mas não há `.md` de origem em lugar nenhum, e `bibliography.md` ainda marca Kinea como "pendente" — investigar se é um artefato de teste esquecido ou uma síntese real nunca finalizada (fonte bruta: `repository/mental_model/kinea_insights/`).
- **`analytics/brasil/monetary_policy/`**: a equação (5) e a escala do regressor de clima foram
  resolvidas em 2026-08-21 (o ONI entra em **décimos de grau**, não em graus — α₅ e α₆ saíram do teto
  da priori e caíram dentro do IC publicado; e a eq. (5) virou um sistema afim resolvido de uma vez
  no simulador). O que restou, em ordem: o **bloco de preços administrados** (boxe do RI de set/2017),
  que é a única premissa que ainda fecha o IPCA no cenário e o que separa o nosso IRF completo da
  primeira linha do Graf 4B — os alvos de validação já estão levantados (10% de depreciação → +1,65
  p.p. nos administrados, +0,72 nos livres, +0,96 no IPCA); e levar a
  eq. (5) **para dentro do filtro**, que é a única via para testar se o α₁ᴵ se corrige (exige π^e como
  estado e uma convenção, não publicada, para o que o modelo espera dos exógenos em cada trimestre da
  amostra). A **aba Projeções do Copom** saiu desta lista — foi construída em 2026-08-25 e em 2026-08-25
  também passou a carregar a previsão da próxima reunião e o backtest dos três métodos; o que resta
  ali é comparar **trajetória contra trajetória** (o RPM publica o caminho trimestral inteiro de cada
  edição, e o modelo produz um caminho também) em vez de ponto contra ponto, e **agendar o
  `antecipa_copom.salvar()`** — os dois artefatos que a aba lê são gravados à mão, então uma
  regeração do relatório sem regravá-los mostra previsão velha, avisada só pelo `corte_usado` na
  caixa. Ver "Pending" em
  [`analytics/brasil/monetary_policy/CLAUDE.md`](analytics/brasil/monetary_policy/CLAUDE.md).
- **Taxa neutra: a premissa que domina os cenários.** Com dado até 2026T2 a especificação do boxe
  põe r* em ~7,9% (tendência HP do juro real Focus + passeio aleatório), contra ~4,8% da mediana que
  o BC publicou para 2024T2. Isso faz a Selic de 15% parecer pouco restritiva e uma Selic de 10%
  parecer expansionista. Não é bug, é a definição — mas decidir se ela é aceitável vem antes de usar
  os cenários para decisão.

### Baixa prioridade
- (nenhuma pendência no momento)
