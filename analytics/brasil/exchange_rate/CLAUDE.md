# analytics/brasil/exchange_rate/ — Panorama Cambial

Self-contained HTML report on Brazilian FX fundamentals (`reports/brasil/FX Report.html`) — single file, opens in any browser, safe to email. Reads from `macro_brasil` and `macro_international` (see [`domain/db/CLAUDE.md`](../../../domain/db/CLAUDE.md) for schema-naming conventions). This is the applied/analytics branch of the exchange-rate work — see root `CLAUDE.md`'s `repository/` section for how it relates to the literature-curation and consolidated-synthesis branches.

**Since 2026-08 this is one report, not two.** The three model tabs that used to render as a separate dashboard (`reports/ppp_dashboard.html`, from `models/ppp_dashboard_template.html`) were fused into `report.html` at direct user request, so there is a single template, a single entry point, and a single deliverable. The old template and `ppp_equilibrium.render()` are gone; `ridge_deviation_model.render_dashboard()` survives only as an alias for the merged generator.

## Generating the report

```powershell
uv run python jobs/update_db.py             # refreshes macro_brasil (cmb_reservas_bc, cmb_cambio_contratado, cmb_ptax, cmb_balanco_pagmt, cmb_fluxo_cambial, cmb_termos_troca, cmb_comex_*, atv_pib_usd)
uv run python jobs/update_international.py  # refreshes macro_international (cmb_reer, cmb_cot_fx, diferenciais_juros)
uv run python -c "from analytics.brasil.exchange_rate.generate_report import run; run()"
# → reports/brasil/FX Report.html (~1.9 MB)

# data tabs only — skips the live FRED fetch and the Ridge fits (seconds, not minutes);
# the three model tabs then render their own "no data embedded" state
uv run python -c "from analytics.brasil.exchange_rate.generate_report import run; run(include_models=False)"
```

Updating the DB first is optional — only needed for fresher data. `generate_report.py` alone re-renders against whatever is already in MySQL (plus a live FRED CPI fetch, for the model tabs).

## Report architecture

Fixed template (`report.html`) with a `/*REPORT_DATA*/` marker inside a `<script>` block, plus `/*PPP_DATA*/`, `/*FXATTR_DATA*/` and `/*RIDGE_DATA*/` for the model tabs (filled via `render_report()`'s `extra_markers=`, which substitutes the bare JSON, or the literal `null` when that payload wasn't built). `generate_report.py` loads each table, serializes to JSON, and hands it to `analytics.report_structure.builder.render_report()` — no Jinja2, no templating engine, just marker substitution. Every `_load_*()` function is independently try/excepted, so one missing or broken table degrades just that section (prints a warning) instead of failing the whole report; `_load_models()` degrades the same way, per model tab.

**Since 2026-08**, `_bindYAutofit()`/`_toComparableX()` are no longer inline in this `report.html` — a `/*Y_AUTOFIT_JS*/` marker is filled in at generation time from `analytics/report_structure/y_autofit.js` (edit that file, not this one — see [`../report_structure/CLAUDE.md`](../../report_structure/CLAUDE.md)). **The theme CSS is *not* migrated** — this report's `:root` palette/typography predates the 2026-07 LIS-dashboard reskin `inflation/` got (navy header, `system-ui` font, no Barlow/JetBrains Mono import, different `--bg`/`--border`/`--text` values than `report_structure/theme.css`), so swapping in the shared `/*THEME_CSS*/` marker as-is would silently change this report's look without an actual design pass. That reskin is a separate follow-up (see root `CLAUDE.md`'s `analytics/` Pendências / `report_structure/CLAUDE.md`'s Migration status) — do it first, then point at the shared theme file.

Seven tabs, real switching via JS `display` toggling (not scroll anchors) — four data tabs, in nav order: Balanço de Pagamentos (`tab-bop`), Fluxo Cambial (`tab-flow`), **Posicionamento: BCB e mercado** (`tab-bcb`), Valuation (`tab-valuation`); then three model tabs: Equilíbrio PPP (`tab-data`), FX Attribution (`tab-fxattr`), FX Model (`tab-ridge`, chamada "Ridge" até 2026-09-01). Duas abas de dados saíram a pedido do usuário: **Mapa de Calor — BP** em 2026-08-27 e **Cotação** em 2026-09-01 (as duas, abaixo).

**How the two halves coexist** (they were written years apart against different design systems, so the merge scoped rather than reconciled them):
- `activateTab()` is the single owner of tab state. The model tabs kept their own lazy-render listeners (they key off `btn.dataset.tab`, so they still fire), but the ex-dashboard's own class-toggling loop was dropped — re-adding one would double-toggle. `activateTab()` also resizes `.chart-wrap`/`.mini-chart-wrap` divs, not just `.chart-card > div`: the model tabs' Plotly divs live in the former, and a chart first drawn inside a `display:none` panel renders at zero width until resized.
- All of the ex-dashboard's CSS is scoped under `.ppp-scope` (a class on each of the three model panels), including `.tab-panel.ppp-scope.active { display: block }` — the data panels are flex columns with a 36px gap, the model panels expect block flow. Its palette/typography vars (`--navy`/`--gold`/`--ice`/`--sans`/`--cond`/`--mono`) were folded into this report's `:root` under their original names, so its CSS and JS merged in unchanged. Net effect: the model tabs still read in Barlow/JetBrains Mono while the data tabs stay on `system-ui`. Deliberate for now — unifying them is the pending reskin below, not a merge artifact to patch around.
- Two `<script>` blocks, one per half (they share no top-level name — verified before merging). Chart.js went away entirely: no `new Chart(` call survived the 2026-07 move to Plotly, so its CDN tags and `Chart.register()` were dropped with the merge.

## A aba Balanço de Pagamentos é uma árvore só (2026-08-27)

Os 6 gráficos de composição que existiam nela — Conta Corrente, Balança de Bens, Serviços, Renda
Primária, Conta Financeira, Investimentos no Exterior, Financiamento Externo — eram todos recortes
de **uma mesma hierarquia**, repetindo eixo, legenda e seletor para mostrar níveis diferentes dela.
Viraram uma tabela hierárquica única alimentando um gráfico, no formato de `analytics/brasil/credit`
(`makeTreeChartTab()` em `report.html`). "Balança de Bens — Detalhe" saiu como seção a pedido do
usuário; o **ramo** continua na árvore, senão a Conta Corrente deixa de fechar.

A árvore é declarada em três pedaços — `BOP_TREE_CURRENT`/`FINANCIAL`/`CAPITAL` — e concatenada em
`BOP_TREE_FULL` na ordem do BPM6. A divisão vinha da aba Mapa de Calor, que dava um card a cada
conta; ela saiu em 2026-08-27 e a concatenação ordenada é o que restou disso.

### A reorganização da hierarquia (2026-08-27, segunda rodada)

O usuário reportou que a hierarquia estava "um tanto bagunçada". Eram quatro coisas distintas, e vale
separá-las porque só duas eram de taxonomia:

1. **Ordem das contas.** A concatenação ingênua punha a Conta Capital *depois* da Financeira. A ordem
   do BPM6 é Corrente → Capital → Financeira → Erros e Omissões, e isso importa porque as quatro
   formam uma identidade: com a convenção de sinal deste relatório, **somam exatamente zero** —
   conferido nos 379 meses, resíduo máximo 0,0001 USD Bi. `BOP_TREE_FULL` agora intercala por chave
   em vez de concatenar as 3 raízes na ordem em que foram declaradas.
2. **Os dois lados da Conta Financeira eram classificados por critérios diferentes.** Ativos seguia as
   3 categorias funcionais do BPM6 (direto / carteira / outros investimentos); Passivos era uma mistura
   de funcional, instrumento e prazo — e "Empr./Tít. LP Externo" **atravessava duas categorias
   funcionais**, somando título de carteira com empréstimo de outros investimentos só porque ambos são
   de longo prazo. Resultado: não dava para ler um lado contra o outro nível a nível. Passivos agora
   espelha Ativos, com o detalhe por prazo um nível abaixo, dentro da categoria a que cada item
   pertence. **Nada se perdeu** — o que era `emprestimos_titulos_lp_externo` virou duas linhas
   (`titulos_externo_lp` + `emprestimos_lp_passivos`) somáveis pelo usuário. Exigiu exportar
   `outros_inv_passivos`/`emprestimos_{cp,lp}_passivos` no payload e derivar `demais_outros_passivos`
   (os dois empréstimos não fecham "Outros Investimentos — Passivos": resíduo médio 1,4 e máximo 16,7
   USD Bi). Sobra uma assimetria que é de **dado**, não de desenho: "Outros Investimentos — Ativos" é
   folha porque o BCB não publica a quebra do lado ativo (a pendência "Ativos de bancos vs Demais
   ativos" registrada no docstring de `cmb_balanco_pagmt.py`).
3. **Alinhamento — o que mais parecia bagunça sem ser hierarquia.** Uma folha não tinha o espaçador do
   `▸`, então começava 16px à esquerda de um grupo do mesmo nível; e o quadradinho de cor só era
   renderizado na linha *marcada*, então marcar a caixa empurrava o rótulo mais 15px. Os rótulos nunca
   formavam coluna. As duas colunas invisíveis agora existem em toda linha (`.tree-toggle.is-empty`,
   `.swatch-dot.is-off`), e as contas de nível 0 ganharam filete separando os blocos.
4. **Rótulos repetidos na legenda.** "Exportação" existe sob Mercadorias e sob Ouro; "Ações e Fundos"
   passou a existir dos dois lados da Conta Financeira. Na tabela o recuo desambigua, na legenda do
   gráfico não há recuo. `buildDisplayNames()` dá a cada nó o **menor sufixo do seu caminho que o
   identifica sozinho** — quem já é único fica com o rótulo curto, só quem colide recebe o pai (e o
   avô, se o pai também colidir).

A tabela fica **acima** do gráfico (pedido do usuário, mesma rodada), nas quatro seções, e os cards de
gráfico das abas de dados passaram de 560px para **600px** de altura. Linha pai em cinza claro, folha
em branco, com as contas de nível 0 num tom um pouco mais escuro.

## A aba Fluxo Cambial lia a tabela errada (2026-08-27)

Descoberto ao ir aplicar o formato de tabela hierárquica nela. **`cmb_fluxo_cambial` não
contém fluxo cambial.** As evidências, todas medidas:

| | `cmb_fluxo_cambial.total_saldo` | `cmb_cambio_contratado.cc_saldo_total` (mensal) |
|---|---|---|
| amplitude em 25 anos | 81,0 → 82,9 | ±10 USD Bi/mês |
| trocas de sinal | **0** em 307 meses | 107 em 216 meses |
| correlação entre as duas | 0,05 | — |

Um saldo de fluxo cambial oscila em torno de zero por definição — se o país fica meses
sem trocar de sinal, ou o dado está errado ou o Brasil parou de importar. A série da
tabela antiga sobe monotonicamente, o que é forma de estoque/índice, não de fluxo. Os
códigos SGS 24352/24363/24364/24369/24370/24371 não são o que o docstring de
`domain/db/brasil/bcb/cmb_fluxo_cambial.py` afirma — e ele **já registrava a dúvida**
("valores em USD billions — confirmar unidade na BCB SGS", "24366 retornou timeout na
pesquisa"). A verificação nunca foi feita, e o relatório vinha plotando isso desde então.

A fonte certa já estava no banco: **`cmb_cambio_contratado`**, Tabelas 13 (diária desde
set/2008) e 14 (mensal desde 2011) dos Indicadores Econômicos Selecionados do BCB, com os
códigos conferidos um a um no docstring. Todas as identidades fecham **exatamente**
(resíduo 0,000 em 4.501 dias): total = comercial + financeiro, comercial = exportação −
importação, exportação = ACC + PA + demais, financeiro = compras − vendas, e o detalhe da
Tabela 14 = serviços + rendas + capitais BR + capitais estrangeiros.

A aba tem 3 seções agora, todas no formato tabela-árvore + gráfico: **Câmbio Contratado**
(a árvore de 4 níveis acima), **Financeiro Detalhado** (Tabela 14 — mensal na fonte, por
isso seção própria em vez de mais um nível) e **Volume Interbancário** (de `cmb_ptax`,
T+1/T+2 — mede liquidez, não direção). E foi para o **2º lugar** no nav, a pedido do
usuário.

`_load_cambio_contratado()` soma a série diária em meses e **descarta o mês em curso**
(mesma regra de período incompleto). O corte usa o último dia útil do mês: feriado no
último pregão faz descartar um mês que estava completo, o que erra para menos — o lado
seguro.

**Fica pendente, e é decisão de fora deste relatório:** `agent_data.get_fx_snapshot()`
ainda alimenta o subagente `cambio-analyst` com `_load_fluxo()`, ou seja, com a série
errada; e a tabela `cmb_fluxo_cambial` + o script de ETL dela precisam ser corrigidos
(achar os códigos SGS certos) ou dropados. `_load_fluxo()` continua no arquivo só por
causa desse consumidor, com o achado documentado no próprio docstring.

### Cabeçalho de gráfico (2026-08-27, terceira rodada)

Todo gráfico das seis abas de dados ganhou o bloco de três linhas de
`analytics/brasil/labor_market`: título, o que a série mede e em que unidade, e
`Fonte: … · <primeiro mês> a <último mês>`. Existe pela mesma razão de lá — um print do
gráfico circula sozinho, longe do `<h2>` da seção e das notas, e sem isso o leitor deduz
tudo pelos eixos. O período vem das **datas realmente plotadas**, não de um intervalo
escrito à mão que envelheceria a cada divulgação.

Implementação: `CHART_META`, um registro só por `divId`, em vez de metadado espalhado
pelas 17 chamadas de `Plotly.newPlot`; `finishChart(divId, dates, meta)` faz as três
coisas que todo gráfico precisa depois de plotado (y-autofit, régua, cabeçalho). As
fontes vieram do docstring do script de ETL de cada tabela, não de memória. As quatro
abas-árvore montam o `meta` a cada redesenho, porque ali as séries e a unidade vêm das
caixas marcadas e dos seletores. **O título do Plotly foi removido** (`mkLayout` perdeu o
primeiro argumento) — com o cabeçalho HTML ele apareceria duas vezes; a margem superior
caiu de 44 para 16.

Consequência de layout: os 600px passaram do `.chart-card` para o `.chart-card > div`.
Com altura fixa no card, o cabeçalho comeria área de plotagem em vez de somar a ela.

### Período incompleto: o bug que o cabeçalho expôs

Escrevendo o cabeçalho apareceu que a aba anunciava "a set/2026" numa série que
termina em jul/2026. A causa era `aggregateSum()`, que somava um bucket com os meses que
tivesse, sem exigir que estivesse fechado: um "T3/26" de um mês só, um "2026" de sete. Em
número: a conta corrente de 2026 saía **−36,0 contra −66,7 de 2025**, que se lê como uma
melhora de 46% e é só o ano pela metade.

Isso **contraria a convenção escrita** em [`../../metric_layers.md`](../../metric_layers.md)
("uma janela incompleta mostra nada — nem soma parcial, nem estimativa sinalizada"), e era
anterior a esta rodada: os gráficos de composição antigos tinham o mesmo comportamento. O
que mudou foi a visibilidade — enquanto era a última barra de um gráfico passava batido;
virou uma coluna rotulada "2026" quando a aba ganhou tabela. `aggregateSum()` agora exige
3 meses no trimestre e 12 no ano, e `_extentPlotado()` faz o cabeçalho e a régua
anunciarem só o que tem valor, para não apontarem para um bucket que a regra vetou.

### A vista inicial também precisa de janela calculada (2026-08-27)

Reportado com print: o gráfico do Câmbio Contratado abria com o eixo X começando em **1982** e a
série espremida no terço direito. A série começa em **2008-09** — eram 26,6 anos de faixa vazia.

A causa é a mesma família do bug do "10a", mas por um caminho que os fixes anteriores não cobriam,
porque **nenhum botão produz a vista inicial**: ela ficava no `autorange` do Plotly. E `autorange` não
percorre os *valores*, percorre o **array x** — um ponto com `y` nulo continua tendo `x` e continua
empurrando o eixo. A aba Fluxo Cambial tem um payload só, cuja grade vai a 1982-02 por causa do saldo
da Tabela 14; as séries da Tabela 13, que são as da primeira seção, só começam em 2008-09. Plotar só
as segundas arrastava o histórico da primeira como espaço em branco.

Duas correções, e a segunda é a que impede a reincidência:

- **`_ensureRangeBar()` aplica "Tudo" quando não há faixa escolhida**, em vez de deixar no autorange —
  e marca a pílula como ativa, que é honesto, porque essa *é* a vista. A regra passa a ser uniforme:
  toda janela vem do dado, inclusive a que significa "tudo".
- **`finishChart()` deriva o extent de `gd.data`**, não do `dates` que quem chama passa. Os 11 gráficos
  fora das abas-árvore passavam a grade do payload, não a série plotada — `chart-diferencial-nominal`
  tinha 4,2 anos de banda pelo mesmo motivo. Derivando no hook comum, um gráfico novo não tem como
  esquecer. Ao fazer isso, `_extentPlotado()` passou a ler **`z` antes de `y`**: num trace de mapa de
  calor o `y` são os *rótulos* das linhas, e lê-los como valores marcava as primeiras N colunas como
  preenchidas, N = número de categorias.

Medido depois do fix nos **21 gráficos**: todos dentro de meio passo da própria série nas duas pontas.
A seção 2b do teste tira um retrato da janela que cada gráfico aplica na primeira pintura — antes de
qualquer clique do próprio teste — e exige isso; confirmado que ela falha no arquivo pré-fix.

### A colisão de `.data-table` — a razão real de a hierarquia parecer chapada

Vale por si porque é uma armadilha da fusão de 2026-08. O `CLAUDE.md` diz que **todo** o CSS do
ex-dashboard PPP foi escopado sob `.ppp-scope`; um bloco escapou — `table.data-table`, que define
`text-align: right` no `td`. Enquanto só a metade de modelo usava esse nome de classe, o descuido era
invisível. Quando a aba BP ganhou tabelas hierárquicas com o mesmo nome (herdado do padrão de
`analytics/brasil/credit`), a regra solta capturou as células de rótulo delas — e `table.data-table td`
(0,1,2) vence `.data-table td` (0,1,1). O efeito era enganoso: o recuo por `padding-left` **continuava
sendo aplicado**, mas com o texto encostado na direita ele não desenhava nada, e uma árvore de 4 níveis
aparecia como lista chapada. Foi diagnosticado a partir de um print do usuário, não do código — o
sintoma ("não consigo ver quem é pai e quem é filho") lia como pedido de estilo e era colisão de CSS.

O bloco está escopado agora, `.data-table td.col-label` declara `text-align: left` explicitamente como
defesa contra a próxima colisão, e a seção 7g de `tests/test_fx_report_js.js` falha se qualquer regra
`table.data-table` voltar a aparecer fora de `.ppp-scope`. **Lição para reuso de nome de classe neste
relatório**: ele hospeda dois design systems num arquivo só, então antes de trazer um componente de
outro relatório, `grep` o nome da classe aqui.

Duas decisões que valem por si:

- **Barra ou linha é derivado, não escolhido linha a linha.** Em "Barras empilhadas", um nó marcado
  que tenha descendente marcado vira **linha**; todos os outros viram barras. Isso reproduz de graça
  a leitura "componentes empilhados + total por cima" que os gráficos antigos davam, e — mais
  importante — torna a dupla contagem impossível: se A e B fossem ambos barras com A ancestral de B,
  A teria descendente marcado e seria linha. Logo duas barras nunca são aninhadas.
- **Comex Stat fica fora da árvore, em 3 tabelas próprias.** Não é BPM6 (SISCOMEX, comércio geral),
  então o total dele não fecha com o ramo "Balança de Bens" e ele não é decomposição de nada da
  árvore. Em troca abre o que o BPM6 não publica: **exportação e importação separadas** por
  parceiro/categoria/produto — `_load_comex_*()` agora emite `export_*`/`import_*` além de `saldo_*`,
  e a importação entra negada na árvore para somar ao saldo do pai. A raiz de cada recorte tem como
  filhos os **itens**, não exportação/importação: as duas partições do mesmo total não podem ser
  irmãs, ou marcar as duas empilharia o valor em dobro.

Os seletores de Agregação/Unidade/tipo de gráfico deixaram de ser da aba e passaram a ser **por
gráfico** (`<select>`, ids `sel-<prefixo>-{period,mode,kind}`), também a pedido do usuário. Só o BP
tem Unidade — o Comex é sempre USD Bi.

### Cartões de definição nas linhas (2026-08-27)

Padrão de `analytics/brasil/labor_market` portado para as 7 tabelas hierárquicas: o rótulo da linha é
curto, e um botão `i` de 14 px abre um cartão com o **nome oficial da fonte** (`full`), a explicação
(`desc`) e a unidade. Hover abre, clique fixa, clique fora ou Esc fecha; **um único `.info-pop` no
`<body>`**, reposicionado a cada abertura, não um por linha.

Duas diferenças em relação ao original valem por si:

- **O conteúdo mora fora da árvore**, num mapa `NODE_INFO` por chave de nó. As árvores já carregam
  `key`/`label`/`get`/`children`, e três parágrafos dentro de cada literal tornariam ilegível
  justamente a estrutura da hierarquia — que é o que se lê ali. Os nós do Comex, que são gerados por
  `_comexNode()`, levam `info` direto no nó porque as chaves são prefixadas por recorte.
- **A unidade é função, não string.** No `labor_market` a unidade é fixa por linha; aqui ela depende
  dos seletores de Agregação e Unidade, então `unitLine()` monta o mesmo par (unidade, janela) que o
  eixo Y e o cabeçalho do gráfico mostram — "fluxo no mês, USD bilhões", "fluxo no ano, % do PIB".
  Uma string fixa passaria a mentir no primeiro clique. `opts.unitNoun` existe porque nem toda tabela
  é fluxo: o interbancário é **volume negociado**, e chamá-lo de fluxo sugeriria direção onde não há
  nenhuma.

Regra que o teste tranca: linha sem `full` nem `desc` **não ganha botão** (o cartão nunca abre vazio),
e `full` só é anexado quando difere do rótulo exibido — senão o cartão abriria para repetir a linha de
volta para quem está lendo. A seção 12 também falha se uma entrada de `NODE_INFO` apontar para chave
que não existe mais, para renomear um nó quebrar o teste em vez de deixar um cartão órfão.

`tests/test_fx_report_js.js` (238 asserções) roda o script real das abas de dados contra um
`document`/`Plotly` stubados e afirma sobre o que ele **produz**: a aditividade filhos→pai lida das
próprias células da tabela — nas 4 agregações × 2 unidades para a Conta Corrente, e ramo a ramo para a
árvore inteira —, a identidade das 4 contas somando zero, a simetria estrutural entre os dois lados da
Conta Financeira, o papel barra/linha, o alinhamento das duas colunas invisíveis, o `[from, to]` de
cada botão da régua, e `saldo = exportação − importação` em toda a série do Comex.

## A aba Posicionamento do BCB ganhou árvores — e a fábrica aprendeu estoque (2026-08-27)

Pedido do usuário: pôr a aba em terceiro, dar-lhe tabelas hierárquicas "com agregações quando
fizerem sentido" e barra empilhada, tirar o gráfico de "Reservas em Ouro" e empilhar o de
intervenções. A ressalva sobre a agregação é a parte que ensina algo.

**Reserva é estoque, e a fábrica só sabia somar.** `makeTreeChartTab()` nasceu para fluxo: toda a
sua agregação passa por `aggregateSum()`/`rollingSum12()`. Aplicada a um saldo em aberto, a opção
"Trimestral" devolveria ~1.100 USD Bi de reservas — **sem lançar exceção nenhuma**, e numa ordem de
grandeza que ainda parece um gráfico de reservas para quem não conferir o eixo. A fábrica ganhou
`stat: 'last'` e um `aggregateLast()` irmão do `aggregateSum()`, com duas escolhas que valem além
daqui: o valor sai da **última posição do bucket, atribuída sem condição**, e não do último valor
não-nulo — se o mês de fechamento não tem dado, a resposta certa é "não sei", não o mês anterior
carimbado com a data do fechamento; e **bucket incompleto continua null**, pela mesma razão de
sempre, porque um ano rotulado "2026" com o valor de julho lê como fim de ano e não é. A aba não
oferece "12m acumulado": acumular estoque não produz grandeza nenhuma.

**"% do PIB" de estoque tem outro denominador**, e essa é a segunda armadilha. Nas abas de fluxo a
regra é numerador e denominador somados na **mesma janela**. Um estoque não tem "PIB do trimestre"
que lhe corresponda — dividi-lo pelo PIB de um mês daria ~1.700% e a escala mudaria a cada clique no
seletor de agregação. Aqui a razão é montada na grade mensal contra o PIB dos **12 meses até a data**
(a leitura usual de adequação de reservas, ~14% hoje) e **só então** agregada por fim de período; o
teste afirma exatamente isso, exigindo que o número não mude de escala entre mensal e trimestral.

**A árvore de reservas é o template de ativos de reserva do FMI** como o BCB o publica (SGS
3546–3556 e 7323), e a aditividade fecha na própria fonte: resíduo médio 0,0005 USD Bi e máximo
0,010 em 307 meses, que é o arredondamento de uma fonte publicada em USD milhões. Começa em
**jan/2001**, onde a decomposição começa — o total sozinho vai a 1971, e mantê-lo aqui abriria a
árvore com 30 anos em que só a raiz tem valor; essa história longa é do gráfico de manchete da seção
acima, que **não é árvore de propósito**: liquidez e caixa são dois *conceitos* do mesmo agregado, e
pendurar um no outro quebraria a aditividade.

**As intervenções expuseram um detalhe do ETL que muda a leitura.**
`domain/db/brasil/bcb/cmb_reservas_bc.py` **descarta os zeros** das 4 séries de intervenção por
decisão explícita (`_drop_zero_interventions`). Então dia ausente dentro da janela de publicação é
intervenção **zero**, não dado faltante — e propagar null ali abriria um buraco de seis anos em
2013-2018 que o leitor entenderia como "sem dado" onde o certo é "não interveio" (naquele período o
BCB atuou por **swap**, que não é intervenção liquidada e vive no gráfico da seção acima). A
consequência prática é que a janela de publicação **não pode sair do `max()` das próprias séries**:
2023 não tem um único registro de mercado à vista, e cortar ali esconderia meses de zeros que são
informação. Ela vem de `reserves_total_daily`, que é diária na mesma tabela e não sofre a remoção de
zeros. Sanidade do resultado contra a história conhecida: +78,6 USD Bi em 2007 (o ano em que as
reservas saltaram de 86 para 180), acumulação contínua 2005-2011, −34,6 em 2019 e −36,3 em 2024.

O gráfico solto de **Reservas em Ouro** virou a linha `res_gold` da árvore: isolado, ele lia como
decisão de política monetária quando quase toda a sua variação é o preço do metal. E o de
intervenções virou a árvore mensal — em base diária as barras empilhadas eram invisíveis (cada dia é
um traço de 1px num eixo de 27 anos), que é o que motivou o pedido de "barra empilhada" nele. O
gráfico de swap passou a mostrar as **3** linhas de exposição do BCB fora das reservas mais a posição
dos bancos. Achado lateral que vale por si: as **SGS 29534 e 29535 já estavam no payload e nunca
tinham sido desenhadas por nenhum gráfico**. Um payload pode carregar série morta por anos sem que
nada acuse.

**A seção de posição cambial ganhou tabela mesmo não sendo hierarquia** (2026-08-27, pedido do
usuário na mesma rodada: *"mesmo que não tenha hierarquia, você pode colocar uma tabela, pois isso
ajuda, assim como as tags de explicação"*). É o argumento certo: **a maior parte do que a fábrica de
árvores entrega não depende de hierarquia** — célula mês a mês ao lado do gráfico, caixa que escolhe
o que plotar, marcador de cor casando tabela e legenda, cartão de definição por linha, cabeçalho do
gráfico e régua de período. O que depende são só o recuo, a seta de expandir e a regra barra/linha.
Então a seção reusa `makeTreeChartTab()` com uma árvore **plana** de 4 nós sem filhos, e o que não se
aplica simplesmente **não é oferecido**: sem "Expandir Tudo", sem seletor de tipo de gráfico. Isso
exigiu um `defaultKind: 'lines'` na fábrica — sem pai, nenhum nó vira linha pela regra de "total
sobre a pilha", e o default de barras empilharia quatro exposições que **não somam um total**: a
fonte não publica agregado das três linhas do BCB, e a dos bancos é de outra entidade. Empilhar ali
não seria preferência de visualização, seria inventar um agregado. A posição também é **estoque**, e
por isso herda o `stat: 'last'` e o denominador de 12 meses (swap em −3,7% do PIB hoje).

A generalização, para a próxima tabela sem hierarquia: **"não é árvore" é razão para desligar três
controles, não para não ter tabela.**

Fechado pela seção 13 de `tests/test_fx_report_js.js` (35 asserções), cujo teste central é o que
pegaria o erro que importa: o valor trimestral tem de ser o do **último mês** do trimestre e **nunca**
a soma dos três.

## A aba Mapa de Calor — BP saiu (2026-08-27)

Pedido direto do usuário, sem contraproposta. Três painéis de z-score (Conta Corrente, Conta
Financeira, Conta de Capital + Erros e Omissões) sobre a mesma hierarquia do BP, com cor =
`(x − média 12 trimestres) / desvio 12 trimestres` da própria linha.

O que a remoção levou junto, porque nada mais no relatório usava: `rollingZScore()`,
`renderHeatmapPanel()`, `applyHeatmapTextVisibility()`, `HEATMAP_TEXT_MAX_COLS`, `heatmapState`,
`rowLabel()` (rótulo com recuo em espaços, coisa de eixo Y categórico) e o CSS `.heatmap-*`. O que
**ficou** e não devia ser confundido com material do heatmap: as três `BOP_TREE_*`, que são a
declaração em pedaços de `BOP_TREE_FULL` e alimentam a aba Balanço de Pagamentos; `flattenVisibleRows()`
e `collectParentKeys()`, que a fábrica de árvores usa; e `subtractArrays()`, usado pelo nó de balança
comercial.

Um detalhe menos óbvio: o ramo de matriz `z` de `_extentPlotado()` saiu também. Ele existia porque
num trace de mapa de calor o `y` são os **rótulos** das linhas e não valores — ler `y` ali marcaria
como "tem dado" as N primeiras colunas, N = número de categorias. Sem nenhum gráfico de `z` no
relatório, o ramo virava código morto que ninguém exercita; a lição segue registrada em
`.claude/rules/lis-dashboards.md`, que é onde ela é reutilizável.

A seção 11 de `tests/test_fx_report_js.js` foi invertida: em vez de afirmar que os 3 painéis são
plotados, afirma que **nenhum** é — um painel morto que continua sendo desenhado não aparece na UI
e só se descobre pelo custo — e que as 3 árvores continuam de pé. Saída: 2,14 MB (era 2,26).

## As abas de posicionamento e de valuation foram redistribuídas (2026-09-01)

Pedido do usuário: renomear a aba do BCB para **Posicionamento: BCB e mercado**, trazer o
posicionamento especulativo em real para dentro dela, levar o PTAX para **Valuation** e **apagar a
aba Cotação**. Nenhum gráfico foi criado ou destruído — os dois que mudaram de casa são os mesmos
`chart-cot-brl` e `chart-ptax` de sempre, com os mesmos loaders.

O que a redistribuição resolve é uma **incoerência de critério** que as duas abas carregavam. A aba
do BCB media *exposição cambial em aberto* — reservas, swap, posição dos bancos, intervenção — e
parava exatamente onde o mercado especulativo começa; o posicionamento da CFTC, que é a mesma
pergunta feita da outra ponta, morava em Valuation, entre medidas de **valor justo** (juros, câmbio
real, termos de troca) com as quais não compartilha nem unidade nem lógica. Trocados de lugar, cada
aba passa a responder uma pergunta só: *quem está posicionado como* de um lado, *o preço está caro ou
barato* do outro. O nome novo da aba é o que torna isso legível — "Posicionamento do BCB" não
comportaria a seção da CFTC.

O PTAX abre Valuation porque é **o nível que as outras seções qualificam**: o câmbio efetivo real e
os termos de troca não significam nada sem o preço contra o qual são lidos. Sozinho ele nunca
justificou uma aba — a de Cotação tinha um gráfico só, e a pendência de moedas pares que a povoaria
segue bloqueada em coleta de dado nova.

**Ainda em 2026-09-01, a seção Diferenciais de Juros saiu inteira** (pedido do usuário), com os seus
três gráficos: Taxas Básicas — Brasil e EUA, Diferencial de Juros Nominal, e Juros Reais ex-post e
Diferencial. Valuation ficou com **PTAX, câmbio efetivo real e termos de troca**, e o relatório com
15 gráficos nas abas de dados. O carry não sumiu do relatório — `diferenciais_juros.diferencial_nominal`
segue sendo um dos canais explicativos da aba **Ridge**, por `ppp_equilibrium.load_data()`; o que
saiu foi a leitura descritiva dele.

**Remover um gráfico é remover quatro coisas, e três delas somem em silêncio.** O div é a única que
tem sintoma visual. Um **CHART_META órfão** é texto que nunca aparece na tela; um **IIFE órfão**
chama `Plotly.newPlot` num id inexistente (o Plotly não levanta nada de útil, e o gráfico
simplesmente não existe); e a **chave do payload** continua sendo serializada — aqui eram **39 KB**
de `diferenciais` para três gráficos que não existem mais, 1,41 → 1,37 MB de payload e 2,25 → 2,21 MB
de arquivo. `tests/test_fx_report_js.js` §15 afirma sobre os quatro, mais uma varredura de
**CHART_META órfão no mapa inteiro** (não só nos três removidos), e §15e fixa a composição exata de
Valuation. Verificado contra 5 mutantes — div órfão, meta órfã, payload vivo, IIFE órfão desenhando,
e um quarto gráfico em Valuation; os 5 são pegos.

Duas decisões de limpeza que ficaram registradas no código, porque o padrão delas é o reutilizável:
**`_load_diferenciais()` fica no `generate_report.py`** mesmo sem consumidor no payload — quem o
importa é `agent_data.py`, para o snapshot do subagente `cambio-analyst`, que não passa por esse
caminho; e **o `.chart-grid-2` fica no CSS** apesar de a seção removida ter sido a única a usá-lo.
É utilitário de layout, não markup de um gráfico, e o `closest()` do `_ensureRangeBar` existe
justamente para sobreviver a um embrulho desses — tirar os dois juntos é o que faz a régua quebrar
quando alguém recriar uma grade de dois. Os dois casos estão comentados no ponto de uso.

Três detalhes de implementação que valem para qualquer remanejo de aba deste relatório:

- **Mover a `<section>` basta; o JS não precisa acompanhar.** Todos os gráficos das abas de dados são
  desenhados no load, direto no `id` do div, e `activateTab()` chama `Plotly.Plots.resize()` no painel
  que abre — que é o que salva um chart desenhado dentro de um `display:none`. Os blocos de JS foram
  movidos junto **só por legibilidade**, para o arquivo continuar lido na ordem das abas.
- **A assertion que faltava era a de PERTENCIMENTO.** As 238 asserções que já existiam continuavam
  todas verdes com o gráfico no painel errado: ele existe, é desenhado, tem cabeçalho, tem régua, os
  dados batem. O único sintoma é que o leitor não o encontra onde foi procurar. `tests/test_fx_report_js.js`
  §14 fatia o HTML nos limites dos painéis e afirma qual aba hospeda cada div, mais o par
  botão↔painel dos dois lados — um painel sem botão fica invisível para sempre, um botão sem painel é
  clique morto, e nenhum dos dois levanta erro. Verificado contra 5 mutantes (CFTC de volta em
  Valuation, botão de Cotação sem painel, nome antigo da aba, nota sem o sinal, PTAX no fim de
  Valuation); os 5 são pegos.
- **A nota do CFTC tinha de dizer o sinal, e não dizia.** O texto anterior — *"Net comprado em USD
  (vendido em BRL) tende a coincidir com pressão de depreciação"* — é verdadeiro e não responde a
  única pergunta que o gráfico levanta: **o que a barra positiva significa**. `lev_net = lev_long −
  lev_short` em contratos do futuro de real da CME, que é cotado em **dólares por real**, então
  positivo é comprado em real. Lida do lado errado, a frase inverte a leitura do gráfico inteiro, e
  esse é o único erro possível ali que não tem tell visual — as barras continuam verdes e laranjas do
  mesmo jeito. A nota nova declara o sinal, o que o open interest acrescenta, e que a foto é semanal,
  com data de terça, e só do real negociado em Chicago.

## O posicionamento da CFTC virou tabela, e o dado ganhou os outros quatro participantes (2026-09-01)

Pedido do usuário, em quatro partes: apagar o gráfico de manchete das **Reservas Internacionais**;
pôr uma caixa de seleção no gráfico do posicionamento para escolher entre open interest e posição
líquida, **os dois em barras** e as médias móveis em linha; mostrar **quem são os outros
participantes** além dos fundos alavancados; e acrescentar médias móveis de **12 e 24 semanas**.

**A terceira parte era uma lacuna de dado, não de gráfico.** `cmb_cot_fx` guardava só
`open_interest`, `lev_*` e `nonrept_*` — o relatório TFF da CFTC classifica cada participante em
**cinco** categorias, e três delas nunca foram carregadas. `connectors/cftc.py` passou a extrair as
15 colunas brutas (long/short/spread das quatro reportáveis, long/short da não-reportável, que a
fonte não abre em spread) e a derivar os cinco líquidos; a tabela foi recarregada de 2011 a hoje e
saiu de 6 para **20 séries por moeda**, 9.534 → 31.444 linhas.

O que a expansão mostra, e é o motivo do pedido: **os fundos alavancados não são o maior grupo do
contrato de real.** Medido nas 748 semanas, o Dealer/Intermediário é **36%** do open interest e os
alavancados **28%** — depois Asset Manager 20,5%, Outros Reportáveis 10,5% e Não-Reportáveis 5,0%.
Ler "posicionamento especulativo" como se fosse o mercado inteiro é ler pouco mais de um quarto dele.

Cinco coisas medidas ou decididas que valem além desta seção:

- **Duas identidades fecham EXATAMENTE nas 748 semanas, e cada uma autoriza uma leitura diferente.**
  Os cinco líquidos somam **zero** (um futuro é jogo de soma zero) — é isso que autoriza a pilha, e
  é o que a pilha mostra: quem está do outro lado de quem. E `Σ(comprado + spread) = Σ(vendido +
  spread) = open interest` — é isso que faz "participação no open interest" ser participação em
  alguma coisa. Resíduo zero nas duas, dos dois lados.
- **O open interest não é a soma dos líquidos, então não pode entrar na mesma pilha.** O pedido era
  "os dois em barras", e a saída não é escolher entre barra e correção: é `offsetgroup`. Os cinco
  líquidos dividem uma pilha, o open interest tem a sua, os dois são barra, e nenhum topo de pilha
  passa a significar algo que não existe. Ele também saiu do **eixo Y secundário** que tinha — e
  isso foi medido antes de mexer: a amplitude do open interest e a do maior líquido são a **mesma
  ordem de grandeza** (razão 1,0), então o eixo duplo nunca foi necessário e só dificultava comparar.
- **"12 semanas" tem de ser 12 semanas, não 12 observações.** A série tem 16 buracos maiores que uma
  semana até 2015, um deles de **196 dias** (out/2011 → abr/2012), então uma janela de 12 linhas pode
  cobrir oito meses. A média móvel carrega um **guarda de span**: sai em branco quando a janela se
  estica além de `(k−1)×7 + 10` dias. Medido, ele apaga 58 pontos na MM12 e 94 na MM24, **todos
  anteriores a 2016** — custa nada na amostra que se lê e impede um rótulo falso onde custaria.
  A folga de 10 dias existe porque 8 das 748 datas caem na **segunda**, não na terça (semana de
  feriado nos EUA).
- **O `spread` entra no payload mesmo sem nenhum gráfico desenhá-lo.** Sem ele a identidade bruta não
  fecha no arquivo entregue e as participações que a nota **afirma em número** deixam de ser
  reproduzíveis por quem lê. Custou ~25 KB e transformou três frases de prosa em asserção: o teste
  recalcula as cinco participações do payload, exige que somem 100% (sem o spread somam **91%**), e
  confere 36% e 28% contra o que está escrito na nota.
- **A tabela é plana e escrita à parte da fábrica de árvores.** `makeTreeChartTab()` agrega em
  mês/trimestre/ano sobre USD Bi com denominador de PIB; aqui o dado é **semanal** e a unidade é
  contrato. Herdar dela custaria mais override do que código próprio, e generalizá-la poria em risco
  as 7 tabelas que já a usam. `COT_ROWS` é global, como as outras árvores, porque é assim que o
  harness resolve as chaves de `NODE_INFO` — uma lista escondida dentro do IIFE viraria seis cartões
  que nenhuma asserção alcança.

**A remoção do gráfico de Reservas custa duas coisas, e vale registrar quais.** A árvore de
composição começa em **jan/2001**, então a história de 1971-2000 do total agora só existe na
linha-raiz daquela tabela (que carrega a série inteira) e não em gráfico nenhum ao abrir a aba. E o
**conceito liquidez** (SGS 13982, diário desde 2008) **sai do relatório por completo** — ele não está
na árvore de propósito, por ser medida alternativa do mesmo estoque e não componente dele. A nota da
árvore foi reescrita para não mandar mais o leitor olhar "o gráfico acima".

`tests/test_fx_report_js.js` §16 (34 asserções) cobre as duas identidades no arquivo entregue, as
participações contra a prosa, as duas `offsetgroup`, a MM recalculada valor a valor com o guarda de
span (incluindo que ele **morde** e que nada depois de 2015 é vetado), a ordem das linhas sobre as
barras e os seis cartões. Verificado contra 8 mutantes — open interest na pilha dos líquidos, MM sem
guarda, MM em barras, open interest de volta como linha de eixo secundário, MM desenhada por baixo,
número errado na nota, série faltando no payload e gráfico de reservas de volta; os 8 são pegos.

## O PPP voltou ao modelo Ridge com beta fixo em 1 (2026-09-01)

Pedido do usuário, e **não** é reversão da decisão de 2026-07-30 ("Remove the ppp entirely, let the alfa
capture it"). Aquela decisão era sobre um coeficiente **estimado livremente**, e continua certa para
esse caso; o que ela nunca cobriu foi um coeficiente **imposto**, que é outro objeto — uma identidade
que o modelo é mandado respeitar, não um parâmetro que ele é convidado a aprender.

**"Colocar o PPP" significa três coisas, e duas não fazem nada com a tendência.** Medido nas 222
observações do painel (2008-01 a 2026-06, movimento acumulado do câmbio +107,2 pp de log):

| variante | MSE walk-forward | IC95 | R² | α acum | PPP acum |
|---|---|---|---|---|---|
| sem PPP (spec anterior) | 6,968 | — | 0,677 | **+96,8** | 0 |
| PPP z-scored, β livre (`include_ppp=True`) | 7,054 | [−1,7; +5,1] | 0,679 | **+100,1** | **−2,1** |
| PPP cru, β livre | 7,014 | [−1,6; +3,3] | 0,679 | +74,2 | +23,7 |
| **PPP com β=1 (`ppp_offset=True`)** | **7,013** | **[−3,2; +4,8]** | 0,677 | **+41,5** | **+57,7** |

O achado que motiva a escolha: **o `include_ppp=True` que já existia no código não captura tendência
nenhuma, porque z-score subtrai a média e a média É a tendência.** O α não cai — sobe, de 96,8 para
100,1 pp. Quem tiver testado "PPP como canal" no passado testou isso.

**Por que 1 é o número certo mesmo com o ajuste mensal não conseguindo enxergá-lo.** Os dois fatos são
o mesmo visto duas vezes: o `Δppp` mensal tem **0,79% da variância** do câmbio (dp 0,40 contra 4,47
pp/mês) e correlação +0,155, então mínimos quadrados mensais ajustam ruído — o β livre sai +0,41 na
amostra inteira mas percorre −0,76 a +0,87 no rolling, com **sinal contrário em 60% das janelas**. No
horizonte longo a relação aparece limpa: regredindo a variação de log do PTAX em h meses contra o
diferencial acumulado no mesmo h, o β é 1,74 / 2,79 / 2,19 / 1,92 / 1,76 / 1,98 em h = 1/12/24/36/60/120,
**distinguível de 0 em todos** (Newey-West t 2,25 a 3,39) e **de 1 em nenhum** (t 0,95 a 1,75), com R²
subindo de 0,02 para 0,32.

**O que se ganha:** o α deixa de ser uma tendência estatisticamente real que o modelo não explica —
+0,435 pp/mês com t=+2,48 antes, **+0,187 pp/mês com t=+1,06 depois**. Os canais quase não se mexem
(dxy_em +8,8 → +8,9 pp acumulados, sp500 +6,0 → +6,3, icbr_usd +5,8 → +5,4): o que foi realocado é a
**tendência**, não a história dos canais.

**O limite honesto:** o PPP leva 54% da tendência, não toda. No período o PTAX subiu 192%, o
diferencial de inflação acumulado responde por 78% e sobram **64% de depreciação real** — os 41,5 pp
que ficam no α. Ele deixa de ser significante; não deixa de existir.

Cinco coisas de implementação que valem para qualquer termo fixo futuro:

- **Offset, não regressor.** `walk_forward_lambda()`/`fit_whole_sample()`/`rolling_fit()` ganharam
  `offset_col=`: ajustam em `y − offset` e preveem `offset + α + Xβ`, o que mantém **todo erro e R²
  reportado na escala do `delta_fx`** e portanto comparável com um ajuste sem offset. Sem isso, o R²
  passaria a medir "quanto dos resíduos ex-PPP os canais explicam", que é outra pergunta.
- **O PPP não entra no balde Baseline.** Ele tem barra própria na decomposição. Enfiá-lo junto do α
  desfaria exatamente o que ele foi adicionado para mostrar.
- **Na grade de previsão ele é mais um canal, sem ramo próprio no simulador.** O truque é o que a
  aba expõe como "nível": o **índice de preços relativos** (IPCA ÷ CPI, rebaseado em 100), com
  `is_log_return: true` e estatísticas identidade — assim o `channelDeltas()` que já existia produz
  exatamente o `delta_ppp`, e no modo "%Δ m/m" a caixa se lê como *quanto o Brasil inflacionou a mais
  que os EUA naquele mês*, que é o input sobre o qual alguém tem opinião.
- **"Plano por default" deixa de ser neutro quando o nível é um índice.** Congelar o índice significa
  Brasil e EUA inflacionando igual por 12 meses — hipótese forte disfarçada de ausência de hipótese, e
  enviesaria toda previsão intocada em ~3 pp/ano. As caixas do PPP nascem seguindo a **deriva média dos
  últimos 12 meses** (`TREND_SEEDED_RG`), e o botão *Reset shocks* devolve a mesma semente, não o índice
  congelado.
- **O cache da banda de erro precisou de chave de spec.** `window`/`horizon` continuam idênticos com e
  sem o offset, então sem um campo `spec` o `forecast_error_bands_w72.json` antigo seria reaproveitado
  e a banda entregue descreveria um modelo que a página não roda mais.

`tests/test_ridge_ppp_js.js` (44 asserções, **primeiro teste da aba Ridge**) afirma sobre o arquivo
entregue: as identidades β=1 nos três lugares do payload, que diferenciar a série de nível reproduz a
contribuição mensal, que **a previsão é a soma das barras** (é a asserção que pega o offset caindo no
resíduo — a ponte de nível continua fechando quando isso acontece), a ponte, a semente por deriva, o
`spec` do cache e a separação de cor CIEDE2000. Verificado contra **15 mutantes**, todos pegos.
Descoberta lateral: as cores do mapa do Ridge **não passam** na régua de ΔE≥20 da regra do
`lis-dashboard` (curve_steep_real × sp500 = 10,6; fiscal × dxy_em = 10,8) — a nova (#7A9E1F, ΔE 21,6)
passa, o resto é anterior à regra e ficou registrado como pendência.

**O que este teste NÃO cobre:** execução do bloco de `<script>` das abas de modelo. Ele só confere
sintaxe. O stub de DOM completo existe apenas para o primeiro bloco (`tests/test_fx_report_js.js`); um
stub genérico por Proxy foi tentado e dá **falso negativo** (a aba PPP quebra no stub, não no produto).

## E os canais foram cortados de 8 para 5, no mesmo dia

Pedido do usuário ("enxugue os canais para 5"), medido **com o PPP já no modelo** — a eliminação
pré-PPP foi refeita, não reaproveitada.

**O que torna o corte fácil é que quase nada era identificado.** Drop-one walk-forward, IC de bootstrap
de blocos entre colchetes: `fiscal` +28,5% [+12,7; +47,4] — **o único cujo intervalo exclui zero** —,
depois `dxy_em` +13,6% [−8,1; +39,7], `icbr_usd` +4,6%, `sp500` +2,5%, `curve_steep_real` +1,6%,
`carry_vol` +0,6%, `real_yield_diff` +0,2% e `dxy` **−0,3%**. A causa é colinearidade, e ela é
mensurável: as contribuições **únicas** ao R² somam 0,196 de um total de 0,677, ou seja **71% do ajuste
é compartilhado**. Nove regressores estavam medindo umas três coisas.

Eliminação backward gulosa (melhor conjunto em cada tamanho): 8 → 7,0132 · 7 → 6,9922 · 6 → 6,9633 ·
**5 → 6,9602** · 4 → 7,1629. Cinco é o **mínimo da curva** — o modelo enxuto pontua marginalmente
melhor fora da amostra que o de oito —, e de 8 até 3 tudo está dentro do ruído de qualquer jeito.

**A escolha do 5º canal não foi por MSE, e é o ponto que vale reter.** O guloso pega
`curve_steep_real` (6,9602); `carry_vol` dá 7,0410. A diferença é **1,15%**, dentro de uma faixa em que
uma diferença de 8,9% já não era distinguível — então o erro não decide. Decide a **estabilidade de
sinal**: com `curve_steep_real`, o coeficiente dele **cruza zero** nas 151 janelas móveis (−0,47 a
+1,21), e um canal que troca de sinal não explica nada, só ajusta. Com `carry_vol`, os **seis**
coeficientes mantêm o sinal em todas as janelas, e o R² é marginalmente maior (0,6614 contra 0,6607).
Benefício secundário: `curve_steep_real` e `real_yield_diff` eram os dois canais vindos de
`base_mercado.interest_rates`, o schema externo do CentralManagement — sem eles, os canais do modelo
ficam inteiramente em tabelas deste projeto (mais o FRED).

Spec entregue (n=222, 2008-01 a 2026-06): λ 0,010, R² 0,6614, R² médio das janelas 0,701, α **+0,199
pp/mês com t=+1,12** — não distinguível de zero, que é o efeito do offset de PPP. Decomposição
acumulada dos +107,2 pp: PPP +57,7 · α +44,2 · dxy_em +9,9 · sp500 +8,3 · icbr_usd +4,8 · carry_vol
−3,3 · fiscal −0,0 · AR(1) −14,3.

Quatro coisas que o corte obrigou, e que valem para o próximo:

- **A lista do JS tem de bater com o payload, conjunto a conjunto.** `CHANNEL_ORDER_RIDGE` alimenta
  `DECOMP_CHANNELS_RG`, que indexa `contrib_monthly`/`level_decomposition` direto: chave a mais faz o
  loop ler `undefined`, chave a menos **apaga uma barra em silêncio**. §12 do teste compara os dois
  conjuntos e varre os três mapas (rótulo de série, cor, rótulo de parâmetro) atrás de buraco e de
  órfão.
- **A tag do cache da banda de erro passou a ser derivada do channel set.** `window`/`horizon` ficam
  idênticos quando o modelo muda, então a tag literal `ppp_offset_b1` que bastava para o offset não
  bastaria para o corte — o cache de 8 canais seria reaproveitado e a banda entregue descreveria um
  modelo que a página não roda.
- **`composite_primitives` passou a ser filtrado pelos canais ativos.** Sem isso o payload continuaria
  carregando (e lendo do banco) os três rendimentos que só serviam a `real_yield_diff` e
  `curve_steep_real`, e o cliente ofereceria "Break down into parts" para canal sem cartão.
- **A paleta teve de ser remedida, e não passava antes.** Separabilidade é propriedade do conjunto
  que está no gráfico junto. Com 8 canais, `fiscal × dxy_em` dava ΔE 10,8 e `curve_steep_real × sp500`
  dava 10,6 — as duas piores entre as séries mais desenhadas. Com o conjunto novo, duas cores mudaram
  por busca em grade (`dxy_em` para âmbar `#EE9900`, `sp500` para azul `#0088CC`) e **os 36 pares agora
  ficam em ΔE ≥ 20**, pior par `fiscal × fx_lag1` em 20,5.

`tests/test_ridge_ppp_js.js` cobre PPP e corte junto: **56 asserções, 22 mutantes, todos pegos**.

## A aba virou "FX Model", e o que mudou na apresentação (2026-09-01)

Seis ajustes pedidos pelo usuário na mesma rodada. Cinco são de apresentação e um muda o
que o leitor digita.

- **Nome.** `Ridge` → **`FX Model`**. "Ridge" nomeia o *estimador*, que é detalhe de
  implementação; a aba é o modelo.
- **A metodologia virou click-drop** (`<details class="fold" id="ridgeMethodFold">`, fechado por
  default) e foi reescrita. A equação saiu de uma linha corrida de nove termos para um bloco em
  display, **uma linha por termo**, com o símbolo à esquerda e a leitura em linguagem comum à
  direita — e o termo de coeficiente imposto marcado à parte (`.eq-fixed`).
- **"Descriptive stats" saiu.** Os números não sumiram: viraram **uma linha** dentro da
  metodologia (`#ridgeFitLine`, montada do payload). Três cartões no topo anunciando λ e
  contagem de janelas apareciam antes de o leitor saber o que é λ.
- **"Rolling Coefficient" e "R² Over Time" foram para um click-drop no fim** (`#ridgeDiagFold`).
  São diagnósticos *do modelo*, não leitura do câmbio.
- **Baseline + PPP viraram uma barra só, "Trend"**, com a composição no rodapé do gráfico.
- **O input do PPP virou inflação em % a/a.**

Quatro coisas técnicas que valem para a próxima:

- **Gráfico dentro de `<details>` fechado renderiza com largura zero e continua assim depois de
  aberto** — o Plotly mede o container uma vez. Mesmo motivo pelo qual `activateTab()` chama
  `resize` ao trocar de aba. O evento `toggle` do `<details>` **não borbulha**, então é um
  listener por bloco.
- **A fusão Baseline+PPP é de APRESENTAÇÃO, feita no cliente.** O payload continua trazendo as
  duas séries separadas — são dado. `DECOMP_CHANNELS_RG` mantém o PPP (a grade de previsão o
  edita como qualquer canal) e só `DECOMP_BARS_RG` o exclui. O rodape é recalculado a cada
  render, porque a janela escolhida muda os três pedaços, e ele diz que eles **compõem, não
  somam**: em pontos de log somam, em percentual multiplicam, e escrever "+78% +55% −13% = ..."
  seria falso.
- **A conversão do input em % a/a é exata e não encadeia.** O estado canônico segue sendo o
  índice de preços relativos (é o que `channelDeltas()` consome); a caixa mostra
  `100·ln(nível(h) / nível(h−12))`. Como o horizonte é de 12 meses, **o nível(h−12) de toda caixa
  cai dentro do histórico**, nunca em outra caixa — é isso que torna a conversão independente da
  ordem de edição: editar a caixa 5 não move o que a caixa 6 mostra.
- **As caixas passaram a imprimir a unidade de exibição arredondada.** Elas imprimiam
  `levels[key][h]` cru, o que num canal em % a/a mostraria o índice (177,76) no lugar da
  inflação — e em qualquer canal vazava a precisão inteira do float (`178.102290899`, no print
  que motivou o pedido).

**E o erro de edição que vale registrar, porque é reincidente**: o anchor `<h2>What this tab is</h2>`
usado para achar a introdução casou com a **aba FX Attribution**, que tem uma seção de mesmo título e
vem antes no arquivo. O slice apagou aquela aba inteira mais a abertura do painel `tab-ridge`.
Quem pegou foi `tests/test_fx_report_js.js` **§14b** — a asserção de que todo botão tem painel e
todo painel tem botão, escrita em 2026-09-01 para outra coisa. É a segunda vez que este arquivo
pune um anchor não ancorado no painel (a primeira foi no próprio teste, mesma seção): **num
relatório de 9 abas, fatie pelo painel antes de procurar qualquer título.**

`tests/test_ridge_ppp_js.js` §13 cobre os seis ajustes (91 asserções no arquivo, 40 mutantes entre
os dois harnesses de mutação, todos pegos).

## Section → schema → table mapping

| Report tab | Loader (`generate_report.py`) | Schema | Table(s) |
|---|---|---|---|
| Valuation | `_load_ptax` | `macro_brasil` | `cmb_ptax` |
| ~~Valuation~~ | `_load_diferenciais` | `macro_international` | `diferenciais_juros` — **fora do relatório desde 2026-09-01** (a seção Diferenciais de Juros saiu); a função fica porque `agent_data.py` a importa, e a tabela segue alimentando o canal de carry da aba Ridge via `ppp_equilibrium` |
| Valuation | `_load_reer` | `macro_international` | `cmb_reer` |
| Valuation | `_load_termos` | `macro_brasil` | `cmb_termos_troca` |
| Posicionamento: BCB e mercado | `_load_cot_fx` | `macro_international` | `cmb_cot_fx` (20 séries por moeda desde 2026-09-01: as 5 categorias do TFF × long/short/spread/net, + `open_interest`) |
| Posicionamento: BCB e mercado | `_load_bcb_positioning` | `macro_brasil` | `cmb_reservas_bc` (4 recortes: `reserves`/`swap` diretos, `reservas_arvore` mensal 2001+, `intervencoes` diária→mensal) |
| Fluxo Cambial | `_load_cambio_contratado` | `macro_brasil` | `cmb_cambio_contratado` (diária→mensal) |
| Fluxo Cambial — volume interbancário | `_load_interbancario` | `macro_brasil` | `cmb_ptax` (diária→mensal) |
| ~~Fluxo Cambial~~ | `_load_fluxo` | `macro_brasil` | ~~`cmb_fluxo_cambial`~~ — **não é fluxo cambial**, fora do relatório desde 2026-08-27 (ver acima); só `agent_data.py` ainda consome |
| BOP | `_load_bop` | `macro_brasil` | `cmb_balanco_pagmt` (+ `atv_pib_usd` for the "% of GDP" toggle) |
| Comex Stat — by partner country | `_load_comex_pais` | `macro_brasil` | `cmb_comex_pais` (saldo + export/import) |
| Comex Stat — by aggregate factor | `_load_comex_fator_agregado` | `macro_brasil` | `cmb_comex_fator_agregado` (saldo + export/import) |
| Comex Stat — by product | `_load_comex_produto` | `macro_brasil` | `cmb_comex_produto` (saldo + export/import) |

Note: interbank FX volume (`fx_interbank_vol_t1`/`t2`) lives in `cmb_ptax` but is charted under Fluxo Cambial, not Valuation — the PTAX section shows only the spot level.

The three model tabs don't go through `_load_*()` at all: they source through `models/ppp_equilibrium.load_data()` (a much wider set — `cmb_ptax`, IPCA, `cmb_risco_pais`, `cmb_dollar_index*`, `cmb_policy_rates`, `cmb_fx_latam`, `inflc_meta`, the external `base_mercado.interest_rates`, plus a live FRED CPI fetch) and the hand-extracted CSVs under `models/fx_attribution_data/`. See `models/` below.

`agent_data.py` (`get_fx_snapshot()`, consumed by the `cambio-analyst` subagent) reuses these same `_load_*()` functions and reduces each series to latest value + 1m/3m/12m deltas + a `stale` flag (per-group expected-gap thresholds hardcoded in `_EXPECTED_GAP_DAYS`).

## Current data-quality gotchas

- **`cmb_ptax.ptax_venda` starts 1994-07-01, not 1984** — SGS 1 technically goes back to 1984-11-28, but everything before 1994-07-01 is denominated in extinct pre-Real currencies (Cruzeiro Real and, further back, Cruzeiro/Cruzado/Cruzado Novo), confirmed directly in the data by the 1994-06-30 (2750.00) → 1994-07-01 (1.00) break at exactly the Real's fixed launch parity. Pre-Real rows were deleted from the DB 2026-07-22 (not economically comparable without a conversion factor this project doesn't carry); `cmb_ptax.py`'s `_START_YEAR`/chunking was updated so a future `run(start="all")` backfill won't reintroduce them.
- **Financial Account sign flip is deliberate** (`_load_bop()` only — never touches the DB): `idp_exterior`, `portfolio_ativos`, `outros_inv_ativos`, `acoes_ativos`, `fundos_ativos`, `titulos_ativos_cp`, `titulos_ativos_lp`, `derivativos`, `ativos_reserva`, and `conta_financeira` are negated so the whole report reads "negative = USD outflow, positive = inflow" consistently, matching how Current Account already reads. Liabilities-side series (`investimento_direto_liquido`, `portfolio_passivos`, etc.) already publish in that convention and are left untouched. If you touch this function, re-derive the sign from a real month rather than assuming Assets/Liabilities are symmetric.
- **Units are not uniform:** `cmb_balanco_pagmt`, `cmb_reservas_bc`, `cmb_fluxo_cambial` store USD MM (divided by 1000 for display). `cmb_comex_pais`/`cmb_comex_fator_agregado`/`cmb_comex_produto` store raw USD (divided by 1e9).
- **Comex Stat breakdowns ≠ BPM6:** the by-country/by-factor/by-product tables use general-trade methodology (SISCOMEX), not BPM6 — their totals will not reconcile line-for-line with `cmb_balanco_pagmt.mercadorias_gerais`. Treat them as complementary cuts, not a decomposition of it.
- **Some "missing" months in Comex/product series are real zeros, not gaps** (e.g. `demais_import` in the Fator Agregado breakdown, `minerio_ferro_import`/`petroleo_export` in the product breakdown — confirmed as months with zero transactions, not pipeline failures). `generate_report.py` `fillna(0)`s these deliberately; do the same for any new derived series built on top.
- **`lucros_reinvestidos` (BCB SGS 22815) has no data 1999–2010** (confirmed 404 from the BCB API, not a pipeline bug) — already `fillna(0)`'d before summing into `lucros_dividendos`.
- **No "gross reserves" series** — SGS 13127 (`reservas_brutas_usd`) times out consistently (wrong/discontinued code); resolved by using the liquidity concept (`cmb_reservas_bc.reserves_liquidity_daily`) plus its detailed components instead. Not a gap to revisit.

## Os dois arquivos do Ridge que a geração lê e nunca reescreve (declarados em 2026-09-01)

`build_dashboard_payload()` lê dois JSON de `models/ridge_results/` a cada geração, e nenhum dos
dois estava declarado em `domain/dashboards/manifest.yaml` até 2026-09-01 — invisibilidade da mesma
classe que motivou a camada de `procedures` na política monetária: arquivo calculado que o relatório
consome, com atraso que nenhuma tela mostrava.

| arquivo | o que é | por que **não** é um `procedures:` |
|---|---|---|
| `model_fit_cutoff.json` | mês até onde os coeficientes são estimados (`cutoff_month`, hoje 2026-06) | fixado **por decisão** do usuário (2026-08: *"I still don't want to re-run the model"* quando só alguns canais têm dado novo). Avançar é escolha, não consequência de ter saído dado |
| `forecast_error_bands_w72.json` | desvio-padrão do erro por passo à frente, 139 reajustes móveis | estatística da amostra inteira, ~90s; muda junto com o ajuste, não com o mês novo |

Há um motivo técnico além da decisão, e ele vale para qualquer cache futuro: **o corte da banda é um
mínimo, e a regra de `reads` compara com um máximo.** O painel da banda termina no mês em que
*todos* os canais já têm dado (o `dropna()` de `build_deltas_contemporaneous`), enquanto
`estado_procedimentos()` marca atraso contra a fonte **mais adiantada** — declarar como passo faria
o Regerar recalcular 90s todo mês, o corte não avançaria (o canal atrasado continua atrasado) e o
passo ficaria atrasado para sempre. É o laço que essa camada evita em toda parte.

O que mudou no código: `forecast_error_bands_w72()` passou a gravar `data_max` no JSON, o mês do
painel a que ela chegou. Caches escritos antes disso só têm mtime — declarar `json_date: data_max`
no dep passa a valer depois do primeiro recálculo, e por isso o dep hoje não declara.

## Reference material (`referencia/`)


Not read by any script — background only. **Reorganized into subfolders 2026-08**; `ppp_dashboard.html` moved out entirely (it was a code-generated deliverable, not background reading, and is now three tabs of `report.html` — see "Model tabs" below):
- `balance_payments_breakdown.xlsx` — the official SGS-code mapping behind `cmb_balanco_pagmt.py`; check this before adding or changing BOP series. Kept loose at the top level, unrelated to either subfolder below.
- `literature/` — the FX-forecasting literature review track:
  - `fx_forecasting_theory_vs_practice.md` and `fx_forecasting_literature_review.md`/`.pdf` — standalone writeups on FX forecasting theory vs. practice (UIP failure, scapegoat theory, terms-of-trade channel, with a Brazil-specific section).
  - `papers/` (renamed from `er_forecasting/` 2026-08) — the 9 underlying academic papers those two documents draw from.
- `equilibrium_model/` — concept notes and hand-built tools for the state-space equilibrium research track:
  - `state_space_equilibrium_model.md` — concept note for a Kalman-filter BEER-style model treating "equilibrium" USD/BRL as an unobserved state, with carry/terms-of-trade/fiscal-credibility as pull variables. The implementation this note motivated (`state_space_model.py`, plus `carry_model.py`/`terms_of_trade_model.py`/`fiscal_credibility_model.py`) was retired 2026-08 in favor of the Ridge model — see `models/` below; this note stays only as background on the original idea, not an active plan.
  - `ridge_window_horizon_grid.md` — window/horizon grid-search note for the Ridge deviation model (see `models/` below).
  - `state_space_simulator.html` — self-contained interactive dashboard (no build step, open directly in a browser) letting you hand-tune the concept note's 3 equations (driver shapes plus γ_ppp, φ, β_carry, β_tot, β_fiscal) and watch the simulated equilibrium/deviation/observed-rate paths. Synthetic data only, not fit to real BRL series, and never regenerated by any script — a genuine one-off reference tool, unlike the generated report's own model tabs. Same known sign-convention inconsistency flagged above. **Rebuilt 2026-07-24 across two same-day revisions** (user-initiated design discussion, then a direct challenge to the first revision's own equilibrium equation):
    - *First revision*: made all drivers enter contemporaneously (time t, not t−1) — financial variables adjust in real time, so a lagged spec mostly discards the real relationship and keeps noise, which is exactly why `carry_model.py`'s lagged tests came back so weak.
    - *Second revision, same day* (user caught two problems with the first): (i) the transition equation was adding a driver's raw *level* every period, which for a "permanent shift" (Step) shape produced unbounded compounding drift instead of a one-time shift — fixed by driving the deviation equation off each channel's period-over-period *change* (Δ) instead; (ii) the first revision had moved `carry` into the transition equation using an I(1)/I(0) argument borrowed out of context from `bayesian_deviation_model.py`, without checking that the real fitted model already treats **PPP as the entire equilibrium** and regresses the deviation from it on all four channels (carry, terms-of-trade, breakeven, fiscal) together — never splitting any of them into a separate transition-equation role. Fixed by making equilibrium an explicit relative-PPP path (`π_diff`, a synthetic inflation-differential proxy — since it's a *rate*, accumulating its raw level is the correct construction, unlike the stock-level drivers) and moving carry/terms-of-trade/fiscal *all* onto the deviation side as Δ-regressors, matching `bayesian_deviation_model.py` exactly. φ's default is now 0.98, matching the ~44-month mean-reversion half-life that model's error-correction follow-up found in real data. Does not model that same model's own unexplained drift/intercept (~0.2–0.4/month) — a known simplification.
    - Also gained click-to-isolate legend items on the main "Observed vs. equilibrium" chart (click a legend entry to hide/show that line; y-axis rescales to what's left).
    - *Third pass, same day*: default π_diff shape changed from Trend to a new Constant option — a steady (non-widening) inflation differential is the more realistic baseline and produces the expected straight-line equilibrium; the inherited Trend shape ramps π_diff's own level, which once accumulated produces an ever-accelerating (quadratic) equilibrium path instead — caught by the user directly from the chart's shape, not anticipated in advance.

## Model tabs (ex-`reports/ppp_dashboard.html`, fused 2026-08)

The three model tabs are the real-data companion to the PPP-equilibrium work below: **Equilíbrio PPP** (the PPP equilibrium candidate plus raw-data panels for the candidate explanatory channels), **FX Attribution (Manager Letters)**, and **Ridge (Regularized, Rolling)** — see `models/` for what each one's underlying model does. `_load_models()` in `generate_report.py` builds all three payloads (`ppp_equilibrium.load_data()`/`build_payload()`, `fx_attribution_model.build_dashboard_payload()`, `ridge_deviation_model.build_dashboard_payload()`); there is no separate render path.

**Gotcha — one `<script>` block, three tabs, no isolation** (bug found and fixed 2026-08-24: a
shipped build had all three model panels rendering completely blank). The three model tabs share a
single `<script>` block, so an uncaught throw in any one of them aborts the rest of the block. The
`include_models=False` build sets all three payloads to `null`; FX Attribution and Ridge each guard
for that, but the PPP IIFE went straight to `D.months.length` and threw — killing the block before
the other two guards ever ran, so both fell through with `*NoData` **and** `*Content` still
`display:none`. The PPP IIFE now has the same guard (`#pppNoData`, plus hiding the panel's other
children). If you add a fourth model tab, guard its payload before first use for the same reason.

They need Barlow/Barlow Condensed/JetBrains Mono from Google Fonts, so they fall back to system fonts offline (the data tabs never depended on a web font). Every chart has TradingView-style pan/zoom per the standing [`.claude/rules/lis-dashboards.md`](../../../.claude/rules/lis-dashboards.md) convention — note these tabs carry their own `_bindPlotlyYAutofit()`/`plotlyBaseLayout()`, distinct from the data tabs' shared `_bindYAutofit()`/`mkLayout()`. Two toolkits, one per half; don't merge them without re-checking both halves' charts.

Until 2026-08 this was a standalone dashboard — `models/ppp_dashboard_template.html` → `reports/ppp_dashboard.html`, via `ppp_equilibrium.render()`, entry point `ridge_deviation_model.render_dashboard()`. All three are retired: template deleted, `render()` deleted, `render_dashboard()` kept as an alias for `generate_report.run()`. `git log -- analytics/brasil/exchange_rate/models/ppp_dashboard_template.html` has the pre-merge history.

## `models/` — research track (three feed the report's model tabs; one has its own output)

Statistical models testing FX theory directly against this database — distinct from `generate_report.py`, which only displays raw series, no estimation. Original goal (2026-07-22): understand where simple models fail at explaining USD/BRL, starting from carry, terms-of-trade, and fiscal credibility as candidate channels. Most of what was tried here was tested and then retired as of 2026-08: `uip_model.py` (strict UIP test, wrong-signed β), `carry_model.py` (broader carry specs, all weak/insignificant), `bayesian_deviation_model.py` ("attempt one," PPP-deviation Bayesian regression), `state_space_model.py` ("attempt two," AR(1)-with-regressors and a real two-state Kalman filter), `beer_model.py` (static levels-only BEER regression plus a rolling-window variant) — `terms_of_trade_model.py`/`fiscal_credibility_model.py` were planned but never built (abandoned 2026-07-23 in favor of going straight to PPP as the equilibrium anchor). `export_excel_audit.py` and `generate_model_spec_pdf.py` were companion exports for that retired batch and were retired alongside it. The user's call: keep only the FX Attribution model and the Ridge model going forward. For the full design/results detail on any retired model — equations, sample windows, fit results, betas/HDIs, the whole session-by-session history — recover it from git history, e.g. `git log --all -- analytics/brasil/exchange_rate/models/state_space_model.py` (swap in any of the other filenames above).

What's actually still here:

- **`ppp_equilibrium.py`** — the shared data-loading and PPP-equilibrium core every surviving model tab sits on top of. `load_data()` builds the relative-PPP equilibrium candidate (headline IPCA index ÷ headline CPI index, anchored to actual PTAX at a selectable base month, sample 1994-07→today) from BR IPCA/PTAX (MySQL) + US CPI (live FRED fetch, not cached), and also fetches the full set of candidate explanatory channels the Ridge model draws on — carry (`diferenciais_juros`), terms-of-trade (`cmb_termos_troca`), breakeven inflation expectations and the CMN de-anchoring gap (`base_mercado.interest_rates` + `inflc_meta`), fiscal risk/CDS (`cmb_risco_pais`), DXY and the EM dollar index, nominal and real 10Y-2Y curve steepening (`base_mercado.interest_rates`), the BR-US real yield differential, S&P 500, the USD-denominated commodity index, and LatAm-peer-relative carry/carry-vol variants (`cmb_policy_rates`/`cmb_fx_latam`) — sourced across `macro_brasil`/`macro_international` plus one external fund-ops schema. `build_payload()` shapes all of this for the Equilíbrio PPP tab's charts; `compute_equilibrium()`/`compute_deviation()` are the equilibrium/deviation math reused by every model that needs it. Its `render()` (which used to fill the standalone dashboard's markers) is gone — `generate_report.py` owns rendering now, and `run()` here is diagnostics-only (per-channel coverage + latest deviation, no file written).
- **`fx_attribution_model.py`** (+ `fx_attribution_model.md`, `generate_fx_attribution_pdf.py`, `fx_attribution_data/`) — turns qualitative FX commentary from asset-manager monthly letters into a numeric monthly time series across 9 fixed causal categories (`fiscal_br`, `monetary_br`, `politics_br`, `global_usd`, `commodities`, `risk_sentiment`, `china_em`, `trade_policy`, `capital_flows` — full taxonomy/extraction rules in `fx_attribution_model.md`). Sign convention: +1 = strongly BRL-appreciation-supportive, −1 = strongly depreciation-driving, scored on the claim's effect on BRL, never on the claim's own subject. Manual-extraction pilot, not an automated pipeline: each manager's `documents.csv`/`claims.csv`/`monthly.csv`/`fx_attribution.xlsx` under `fx_attribution_data/<manager>/` is hand-extracted from source letters (currently `kinea/`, `verde_asset/`, `kapitalo/`); the module itself only covers claims → monthly matrix → Excel export (`export_excel()`) and → dashboard payload (`build_manager_payload()`/`build_dashboard_payload()`). Framework is manager-agnostic by design — onboarding a new manager means hand-extracting its own `fx_attribution_data/<manager>/` folder, no code changes.
- **`ridge_deviation_model.py`** (+ `generate_layman_model_doc.py`) — the shipped model: the exchange rate's own log return, `delta_fx(t) = 100·diff(log(ptax(t)))`, regressed on each channel's own contemporaneous z-scored delta plus an AR(1) term on `delta_fx` itself, fit via Ridge (L2-penalized, `sklearn.linear_model.Ridge`) rather than OLS/Bayesian — a point estimate, no posterior/HDI. **Relative PPP re-entered the spec in 2026-09-01 with its coefficient pinned at 1** (see the section above) — it is an *offset*, not a regressor, and never appears in `delta_cols`. **The channel set was cut from eight to five the same day** (`_CHANNELS_5`): fiscal (CDS), the EM dollar index, a carry-to-volatility metric, S&P 500 and the USD commodity index. Out went DXY, real curve steepening and the BR-US real yield differential. Lambda is chosen by walk-forward temporal cross-validation (`walk_forward_lambda()` — expanding window, one-step-ahead OOS scoring, never fit on the point being scored); coefficients are also re-estimated on a rolling 72-month window (`rolling_fit()`, window size chosen via a training-window × forecast-horizon grid search, see `referencia/equilibrium_model/ridge_window_horizon_grid.md`) so the Ridge tab can show whether a channel's relationship is stable over time. Several variant specs were tested and mostly rejected by walk-forward OOS validation before landing on this shape — a per-channel 6-lag structure (overfit OOS, removed), a level-on-level regression (spurious/non-stationary result, rejected), and a persistent carry-in-level variant (kept as exploratory-only, not wired into the report). The Ridge tab also has a 12-month forecast/stress-test tool: per-channel editable level boxes (with a level/%-change-m/m display toggle) that chain into deltas the same way the fitting sample does, using the most recent rolling window's own coefficients, with a widening standard-error band built from a cached walk-forward re-simulation (`forecast_error_bands_w72()`, cached to `ridge_results/forecast_error_bands_w72.json` since it's expensive to (re)compute) — plus a decomposition/level-bridge chart with rebasable start/end dates and a toggle to use the last rolling window's own coefficients instead of the whole-sample fit. `generate_layman_model_doc.py` generates `reports/brasil/ridge_model_explained.pdf`, a plain-English (no jargon, no equations) companion documenting the shipped channel spec, aimed at a non-technical internal audience. **2026-08-04 fix**: the three helpers `ridge_deviation_model.py` used to import from the now-deleted `bayesian_deviation_model.py` (`_REFERENCE_START`, `_standardize_ext`, `build_deltas_contemporaneous`) are now inlined directly in this module, and `render_dashboard()` no longer delegates to the now-deleted `state_space_model.render_dashboard()` — since the 2026-08 merge it's just an alias for `generate_report.run()`.

- **`real_rates_comparison.py`** (+ `real_rates_comparison_template.html`) — the one thing in this
  folder with an output of its own: `reports/brasil/real_rates_comparison.html`, a self-contained page
  (same `/*REPORT_DATA*/` + `render_report()` harness as `report.html`) comparing Brazil's ex-post real
  policy rate against MX/CL/CO/PE from `macro_international.cmb_real_rates`, plus a second chart against
  real growth in government consumption (`atv_pib.consumo_adm_publica`, NSA, YoY computed here — growth
  rates stay in the consumption layer, never as a second source of truth in the database). Not a tab of
  the FX report and not run by any job — generate it on demand:
  `uv run python -c "from analytics.brasil.exchange_rate.models.real_rates_comparison import run; run()"`.
  It is also the **only** consumer of `cmb_real_rates`, which is why that table isn't orphaned.

## Pending / next steps

- **As 3 abas de modelo ainda usam o `xaxis.rangeselector` nativo**, via
  `PLOTLY_RANGE_SELECTOR`/`plotlyBaseLayout()` no segundo bloco de `<script>` — carregam o mesmo bug
  do "10a" que as abas de dados tinham (janela terminando depois do último dado, porque `stepmode`
  ancora no range atual do eixo, que com autorange já inclui o padding do Plotly). As abas de dados
  migraram para `_ensureRangeBar()` em 2026-08-27; as de modelo ficaram fora do escopo daquela
  rodada. Migrar é a mesma troca: tirar `rangeselector` de `plotlyBaseLayout()` e chamar
  `_ensureRangeBar(divId, dates)` depois de cada `plotlyRenderAndBind()`. Note que as duas metades
  têm toolkits distintos (`mkLayout`/`_bindYAutofit` vs `plotlyBaseLayout`/`_bindPlotlyYAutofit`) —
  `_ensureRangeBar` é genérico e serve às duas, mas confira os gráficos de modelo que **não** são
  série temporal em X antes de aplicar em bloco.
- **O toggle barras/linhas só existe na aba BP** — as outras 4 abas de dados ficaram como estavam
  por decisão do usuário (2026-08-27), com gráfico de tipo fixo; só ganharam a régua de período nova.
- **Confirm the merged report in a real browser** — the 2026-08 fusion was verified by generating the file and driving its real inline scripts through a jsdom harness with a stubbed Plotly (all 9 tabs activate with exactly one panel visible, all 36 chart divs render, every id the JS reaches for exists, no uncaught error from any tab/select/toggle, y-autofit fires; re-run 2026-08-24 after the PPP guard fix — both the full build and the `include_models=False` build come back with zero errors, the latter now showing three no-data messages instead of three blank panels, and every option of all 7 model-tab selects plus the Ridge tab's 8 buttons and 197 numeric inputs fire clean). That covers wiring, not *looks*: nobody has yet eyeballed the two typographies side by side, the model panels' spacing inside this report's `main` (they were laid out for a wider `.page`), or the model tabs' first paint after a tab switch (they're drawn hidden, then resized).
- **Unify the two design systems** — the reskin item below is now also a merge cleanup: the six data tabs are `system-ui`/navy-header era, the three model tabs are the 2026-07 Barlow/JetBrains reskin. Doing the reskin collapses `.ppp-scope` and both Plotly layout factories (`mkLayout()` + `plotlyBaseLayout()`) into one each.
- **BOP "Financiamento Externo" — 10 lines with no SGS code identified**: asset-side bank/non-bank split, and the public/private/direct/other split within LP external loans (both inflows and amortizations). Two next steps identified, neither executed: (1) accept the coarser breakdown `balance_payments_breakdown.xlsx` already provides instead of forcing an exact match, or (2) search the BCB SGS series finder for codes outside the 22701–23060 range already in use.
- **Interest differentials are ex-post only** — ex-ante (Focus Selic/IPCA 12m for Brazil; Fed funds futures/OIS and Michigan survey or breakevens for the US) is not implemented. Add as new `_ex_ante`-suffixed series in `diferenciais_juros`, not a replacement of the existing ones. Note que **desde 2026-09-01 nenhuma aba de dados desenha essa tabela** — o consumidor vivo é o canal de carry da aba Ridge e o `agent_data.py`, então um diferencial ex-ante entraria hoje por ali, não por uma seção de Valuation.
- **The PTAX section shows only BRL/USD** — explicit user ask for EM peer currencies (MXN, CLP, COP) side by side; no spot series for those pairs exists in the DB yet (FRED has candidates like `DEXMXUS`) — blocked on authorization for new data collection, not on a technical blocker.
- **Fluxo cambial — CEP/CBE sub-items** (candidate SGS codes 24372–24376) returned data in an initial search but descriptions are unconfirmed — cross-check against the BCB's weekly Nota Cambial before using them.
- **Cupom cambial + B3 FX futures (DOL/WDO)** — deferred indefinitely; requires Bloomberg (`blpapi`/`xbbg`) on the running machine.
