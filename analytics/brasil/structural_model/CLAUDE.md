# analytics/brasil/structural_model/ — Contexto para o Claude

**Estado: o painel de dados da equação (I) está pronto; nenhuma equação foi estimada.** Este
arquivo ainda é, em boa parte, o *plano* aprovado em 2026-09-16, e vai sendo substituído pelo estado
real à medida que cada equação fica pronta. Histórico rodada-a-rodada vive no git log, não aqui.

## Como rodar

```powershell
uv run python analytics/brasil/structural_model/panel.py                     # painel -> data/panel.csv
uv run python -c "from analytics.brasil.structural_model.generate_report import run; run()"
node tests/test_structural_model_js.js                                        # 196 asserções
```

| Módulo | O que faz |
|---|---|
| `panel.py` | Painel trimestral dos insumos. `construir()` monta do banco, `salvar()` grava `data/panel.csv` para inspeção. Importa `q`/`serie`/`para_q`/`focus_ipca_12m` de `monetary_policy/modelo_painel.py` — não copia |
| `generate_report.py` | Chama `panel.construir()` **ao vivo** (≈3s) e injeta em `report.html`. Sem artefato intermediário e sem passo de recálculo declarado: não há cálculo caro ainda |

## A aba Curva de Phillips

Quatro gráficos, não cinco. **Inflação e expectativa dividem um**: estão na mesma unidade e a
equação diz que a inflação é média ponderada das duas, então lidas em cartões separados a distância
entre elas — que é o que a relação afirma — desaparece. Hiato, câmbio e IC-Br têm escala própria e
ficam cada um no seu.

Sem barra de métrica, e isso é derivação e não economia de trabalho: cada série entra na equação em
**uma** forma só, então todas as sete camadas têm uma opção só — e camada com uma opção não vira
controle. Quando a aba de estimação entrar, aí sim haverá o que selecionar.

**O trimestre em aberto é marcado em três lugares** (faixa cinza no gráfico, aviso no topo, linha em
itálico na tabela). A coluna `completo` do painel é o que sustenta isso: um trimestre rotulado
"2026T3" carregando o IPCA de agosto e a média de 2,5 meses de câmbio não é um fechamento de
trimestre, e nada no número avisa. A estimação filtra por essa coluna.

### Conferências feitas contra a fonte

- IPCA 12m de 2026T2 = 4,64, igual à leitura de junho na série do Banco Central.
- `de` de 2026T2 = −4,0685, igual a 100·ln(média 2026T2 ÷ média 2026T1) do PTAX.
- Hiato de 2026T2 = 0,36, o mesmo `h0` que `monetary_policy/data/antecipa_previsao.json` registra
  para a vintage de junho/2026.
- Amostra com as cinco séries completas: **91 trimestres**, 2003T4 → 2026T2 — o hiato é o que
  limita, as demais vão a 2001T4.

## Context

`Workflow.md` §(IV.I).i pede **um** modelo estrutural para o sistema macro — equações para inflação,
câmbio, juros, hiato e expectativas — no lugar do modelo de câmbio isolado que hoje vive dentro do
`FX Report.html`. Este plano é o primeiro passo: um dashboard **Structural Model** com uma versão
simplificada do modelo semiestrutural do BC, **estimada equação por equação**, com o modelo do FX
Report reestimado em frequência trimestral como a equação de câmbio.

Simplificações aceitas de partida: sem bloco de preços administrados (IPCA cheio), sem hiato
mundial, sem clima, sem estimação conjunta por filtro de Kalman, e o hiato do produto **lido do
BC** em vez de estimado como estado latente.

---

## O que já existe, e é o que muda o tamanho do trabalho

`analytics/brasil/monetary_policy/` já contém a **réplica completa do modelo agregado do BC**
(boxe RI jun/2024) — 17 dos 22 parâmetros dentro do IC 90% publicado, hiato correlacionando 0,990
com o do BC. As cinco equações pedidas têm correspondente direto:

| pedido | equação do BC já replicada | onde |
|---|---|---|
| `I(t)` Phillips | (1), preços livres | `modelo_agregado.py` docstring |
| `E(t)` expectativas | (5), `estimar_eq5()` | idem |
| `H(t)` IS | (2), hiato latente | idem |
| `R(t)` Taylor | (3), com 2 defasagens | idem |
| `F(t)` câmbio | (4) UIP — **substituída** pelo Ridge do FX Report | idem |

E `modelo_painel.py` já constrói, **validado contra número publicado**, quase todos os insumos:
`focus_ipca_12m()`, `focus_selic_12m()` (ponto de 12m, não média do caminho — erra +0,14 contra
+0,82), `hp(..., cauda=)` (HP com cauda Focus: r\* 2023T4 em 5,01% contra 4,82% publicado; sem a
cauda, 7,15%), `cauda_juro_real()`, `para_q()`, `meta`, `rr_trend`, `r_focus`, `de`, `rp_hat`.
Artefato versionado: `data/modelo_painel_full.csv`, 2001Q4→2026Q3.

Dados no banco (todos confirmados): `inflc_agregados` (`ipca_12m` = SGS 13522), `expc_focus`
(`horizonte='12m', suavizada='S'` desde 2001-11 — a série rolante existe, não precisa ser
interpolada), `expc_focus_copom`, `pm_hiato_produto` (+ `_vintages`), `inflc_meta` (SGS 13521),
`pm_copom_projecoes`, `cmb_ptax`, `comm_icbr_usd` (SGS 29042), `cmb_risco_pais`,
`cmb_dollar_index_em`, `cmb_equity_us`, `diferenciais_juros`.

**Consequência:** o trabalho é escrever um painel e um estimador *simplificados* que **importam**
essas funções (não copiam), reestimar o câmbio em trimestral, e construir o dashboard.

---

## Decisões tomadas

| tema | decisão |
|---|---|
| Frequência | **Tudo trimestral**, incluindo reestimar o Ridge do câmbio |
| Taylor | `R(t) = r1·R(t-1) + (1-r1)·(RR*(t) + Meta) + r2·dI` — steady state = RR*+Meta, `r2` livre |
| Fechamento | **Estima aberto, simula fechado** — cada equação é MQ de equação única contra dado observado; o laço só fecha no simulador, com toggle Endógeno/Manual por equação |
| Endogeneidade no câmbio | `carry_vol` (via Selic) e o offset PPP (via IPCA); CDS, `dxy_em`, `sp500`, `icbr_usd` seguem exógenos |
| RR\* | **HP com cauda de projeção Focus** (`modelo_painel.hp`), mais a medição do perfil de revisão |
| `I*(t)` | **IC-Br em USD** (`comm_icbr_usd`) — todo o repasse cambial fica em `i3`, um coeficiente só |
| Volatilidade no `carry_vol` | Janela **defasada** (termina no fecho do trimestre t−1), com fonte trocável para vol implícita de opções quando o usuário fornecer |

### Sobre a volatilidade — a resposta à sua pergunta

Dá, sim, e é o certo. O que existe hoje é `_annualized_vol_6m()`
([ppp_equilibrium.py:438](../exchange_rate/models/ppp_equilibrium.py#L438)): σ móvel
de 126 pregões **terminando em t**. Em trimestral essa janela cobre ~2 trimestres e o trimestre
explicado está dentro dela — a variação do câmbio entra dos dois lados da regressão. Defasar a
janela para terminar no último pregão de t−1 elimina isso inteiramente: o denominador passa a ser
**predeterminado**, conhecido no início de t. É a correção padrão e não custa nada.

O que sobra depois disso é menor e é de *simulação*, não de estimação: vol realizada defasada
continua sendo função da história da própria variável dependente, então num cenário fechado ela
tem de ser atualizada a partir do caminho simulado ou declarada como premissa na tela.

**Vol implícita de opções resolve as duas metades** — é prospectiva, observável em t e não é função
de realização passada do câmbio. O código nasce com um seletor `VOL_SOURCE` (`realizada_lag` |
`implicita`) para que a troca seja de série, não de equação. **Não há tabela de vol implícita no
banco** (varredura completa: nada). Quando você fornecer, o destino recomendado é uma tabela
`macro_brasil.cmb_vol_implicita` pelo caminho do conector Bloomberg que já existe
([domain/db/brasil/bloomberg/cmb_risco_pais.py](../../../domain/db/brasil/bloomberg/cmb_risco_pais.py)) — e
**não** um CSV exportado à mão, precisamente porque o `cmb_risco_pais` nesse formato é registrado no
repo como algo que "costuma estar semanas atrás".

---

## O modelo, como vai ser escrito

Todas as variáveis trimestrais. `Meta(t)` é a meta vigente **no horizonte de 12 meses**, não a do
ano corrente (mistura ponderada por meses entre o ano t e t+1; contínua em 3,0% desde 2025).

```
(I)  I(t)  = i1·I(t-1) + (1-i1)·E(t-1) + i2·H(t) + i3·F(t-1) + i4·I*(t) + d08 + d20 + ε
(E)  E(t)  = e1·E(t-1) + e2·I(t) + (1-e1-e2)·Meta(t)                           + ε
(H)  H(t)  = h1·H(t-1) + h2·g_RR(t)                             + d08 + d20 + ε
(R)  R(t)  = r1·R(t-1) + (1-r1)·(RR*(t) + Meta(t)) + r2·dI(t)   + d08 + d20 + ε
(F)  100·Δlog E(t) = Δppp(t)·1 + α + φ·100·Δlog E(t-1) + Σ β_c·z(Δc(t)) + ε
```

Com:
- `I` = IPCA cheio acumulado em 12 meses, no último mês do trimestre (SGS 13522)
- `E` = Focus IPCA 12m à frente, suavizada (`expc_focus`, `suavizada='S'`)
- `H` = `pm_hiato_produto` (`variavel='central'`), % do produto potencial, nível
- `F` = 100·Δlog(PTAX) no trimestre — variação, não nível (é o que torna a equação dimensionalmente
  consistente com `I` em pontos percentuais)
- `I*` = variação trimestral do IC-Br **em USD** (SGS 29042)
- `g_RR(t) = i^e(t,t+4) − π^e(t,t+4) − RR*(t)` — **observável em t**: é a expectativa Focus formada
  em t para 12 meses à frente, não uma realização futura. Diferença simples, como a eq. (2.1) do BC
  (Fisher exato descola ~0,2 p.p.)
- `dI(t)` = `E(t) − Meta(t)` na v1; `pm_copom_projecoes` no horizonte relevante − Meta na v2
- `d08` = 2008Q4–2009Q4, `d20` = 2020Q1–2020Q4 (mesmas janelas do BC), estimado com e sem

**Ordem de solução dentro de t** (recursiva, sem ponto fixo): `H → I → E → R → F`. `I(t)` usa
`F(t-1)`, predeterminado; `F(t)` usa `I(t)`, já resolvido. O **único** ponto fixo é `g_RR`, que
precisa da Selic esperada 4 trimestres à frente — resolvido como no simulador existente, em que o
caminho de Selic é conhecido por construção no cenário.

### Duas ressalvas que vão para a página, não para o rodapé

1. **`I` acumulada em 12 meses amostrada trimestralmente tem janelas sobrepostas**, então o resíduo
   é MA(3) e `i1` é mecanicamente alto (~0,75 só pela sobreposição). Não invalida a especificação —
   ela é coerente em espaço de 12 meses, que é o espaço em que `E` também vive. Duas providências:
   erros-padrão **Newey-West** em todas as equações, e uma coluna de robustez com a inflação
   **trimestral** (a convenção do BC), medida lado a lado. `i1` não é comparável ao `a1L` publicado.
2. **IPCA cheio inclui administrados, que não respondem ao hiato** — então `i2` sai atenuado contra
   o do BC, que estima em preços livres. É o preço da simplificação que você pediu, e a coluna de
   comparação com livres (pesos já recuperados no repo: livres 0,767 / administrados 0,233, R² 0,978)
   mede quanto custa.
3. **`comm_icbr_usd` contra a posição documentada do repo.**
   [domain/db/CLAUDE.md:170](../../../domain/db/CLAUDE.md#L170) diz que o IC-Br em reais é "adequado, sim,
   para a curva de Phillips, onde o repasse cambial é parte do que se quer capturar". A escolha do
   USD é defensável aqui **porque o câmbio é endógeno e `F(t-1)` já está na equação** — os dois
   textos falam de modelos diferentes. Para não ficar só no argumento, a versão em BRL entra como
   **coluna de diagnóstico** no Apêndice, com o repasse cambial total medido nas duas.

---

## Passos, para executar e estudar um a um

### Passo 0 — o painel trimestral

`analytics/brasil/structural_model/panel.py` → `data/panel.csv` (versionado, como em
`monetary_policy/data/`).

Importa de [modelo_painel.py](../monetary_policy/modelo_painel.py): `q`, `serie`,
`para_q`, `hp`, `focus_ipca_12m`, `focus_selic_12m`, `cauda_juro_real`. **Importar, não copiar** —
são funções validadas contra número publicado e duas cópias divergem.

Colunas: `ipca_12m`, `pi_q` (robustez), `pi_e`, `i_e`, `meta_12m`, `rr_star`, `g_rr`, `hiato`,
`hiato_rt` (vintages), `selic`, `de`, `pi_star_usd`, `pi_star_brl`, `dI_focus`, `dI_bcb`, `d08`, `d20`.

Convenção de trimestralização, declarada por coluna porque cada uma é diferente: acumulados de 12m
e PTAX pelo **último** mês; Focus pelo último boletim do trimestre; Selic pela **média**; hiato é
nativo trimestral.

**Entrega para estudar:** o perfil de revisão do HP — `rr_star` calculado com dado até T−k para
k = 0, 2, 4, 8, 12 trimestres, contra uma data fixa. É isso que dá número à sua ideia da defasagem
de 2 anos em vez de intuição.

### Passo 1 — Equação (I), Phillips + o esqueleto do dashboard

`equations/phillips.py`. Restrição `i1 + (1−i1) = 1` imposta regredindo `I(t) − E(t-1)` contra
`I(t-1) − E(t-1)`, `H(t)`, `F(t-1)`, `I*(t)` e as dummies. Newey-West.

Junto vai o esqueleto do relatório (ver Passo 7), para que cada equação seguinte já caia numa aba.

### Passo 2 — Equação (E), expectativas

`equations/expectations.py`. Restrição imposta regredindo `E(t) − Meta` contra `E(t-1) − Meta` e
`I(t) − Meta`, **sem intercepto**. Difere da eq. (5) do BC em dois pontos que a aba declara: não tem
o termo de MA(4) do IPCA passado, e usa a inflação **realizada** no lugar da previsão do próprio
modelo — o que elimina a simultaneidade que no BC custou um estimador em dois passos (condicionar em
π^e observado em t leva φ₂ de 0,21 para 0,42).

### Passo 3 — Equação (H), IS

`equations/is_curve.py`. Sem intercepto (o hiato do BC tem média ~0 — **conferir e reportar**).
`h2 < 0` esperado. Duas colunas: hiato da edição corrente e hiato **real-time** por
`pm_hiato_produto_vintages` — a edição corrente é um objeto suavizado dos dois lados, então `h1` sai
alto e `h2` atenuado, e a coluna real-time é o que mede isso. Atenção à quebra metodológica entre as
edições 2024-06 e 2024-09: só `central` é comparável entre os dois regimes.

### Passo 4 — Equação (R), Taylor

`equations/taylor.py`. Restrição imposta regredindo `R(t) − RR* − Meta` contra
`R(t-1) − RR* − Meta` e `dI(t)`, sem intercepto → devolve `r1` e `r2` diretamente. Duas versões de
`dI` (Focus e projeção do Copom). Coluna de robustez com **segunda defasagem**: o BC estima
t₁ = 1,48 e t₂ = −0,58 (soma 0,90), um perfil de suavização em corcova que uma defasagem só não
reproduz.

### Passo 5 — Equação (F), câmbio trimestral

`equations/fx.py`, uma função nova em cima de
[ridge_deviation_model.py](../exchange_rate/models/ridge_deviation_model.py) — **não
reescrever o mensal**, que continua servindo o FX Report.

- Níveis agregados por `para_q(..., como='last')`, depois diferenciados → Δ trimestral.
- Mesma especificação: offset PPP com β≡1 (perna BR endógena = IPCA da eq. I; perna US = CPI
  exógena), α, AR(1), e os 5 canais (`fiscal`, `dxy_em`, `carry_vol`, `sp500`, `icbr_usd`).
- `carry_vol` = (Selic − Fed Funds) ÷ vol **defasada**, com `VOL_SOURCE` trocável.
- Padronização **escala e não centra** (`z = x/sd`), como o mensal — em colunas de diferença,
  subtrair a média injeta deriva constante de −μ/σ todo período.
- λ por CV walk-forward, `min_train = 16` trimestres.
- **Reportar o modelo mensal ao lado, convertido para unidade nativa** (β nativo = β do payload ÷ o
  σ em `channel_stats`; ex. `fiscal` = 8,236 / 126,31 = 0,0652 pp de câmbio por bp de CDS). A amostra
  cai de 245 para ~81 observações e as bandas de erro ficam mais ruidosas — a coluna mensal é o que
  permite dizer *quanto*.
- Manter o `model_fit_cutoff.json` **separado** do mensal: reestimar um não pode mover o outro.

### Passo 6 — O simulador

`simulator.py`, com o padrão de
[modelo_agregado.simular()](../monetary_policy/modelo_agregado.py). Dado um caminho
de Selic e dos exógenos, propaga na ordem `H → I → E → R → F`. Toggle Endógeno/Manual por equação,
como a aba Modelo BC — Agregado. Armadilhas já pisadas lá que valem aqui sem reaprender: guardar
valores exatos e não a string arredondada; o horizonte não é janela de exibição (depois dele o
último valor digitado se repete); e duas âncoras distintas no payload (o valor em t₀, que é a
defasagem que as equações usam, contra o último valor publicado, que é o que "Selic constante"
significa).

### Passo 7 — O dashboard

`analytics/brasil/structural_model/` → `reports/brasil/Structural Model.html`. Nome de arquivo em
inglês, conteúdo em pt-BR (`lang="pt-BR"`), como os outros 8 relatórios do Brasil.

Arquivos: `__init__.py`, `report.html`, `generate_report.py`, um `*_tab.py` por aba, `CLAUDE.md`,
`data/`, `panel.py`, `equations/`, `simulator.py`.

Abas: **Inflação · Expectativas · Hiato · Juros · Câmbio · Simulador · Apêndice** — uma por equação,
na ordem em que forem construídas.

Contrato do relatório (tudo já padronizado no repo, ver
[report_structure/CLAUDE.md](../../report_structure/CLAUDE.md)):
os 5 marcadores (`/*REPORT_DATA*/`, `/*THEME_CSS*/`, `/*Y_AUTOFIT_JS*/`, `/*CHART_HEAD_CSS*/`,
`/*CHART_HEAD_JS*/`); `var D = REPORT_DATA;` com **`var`**, não `const` (o teste lê pelo contexto do
vm); `var CHART_META = {...}` com título e fonte por gráfico; Plotly 2.35.2; `run(output=...)` com
esse nome de parâmetro exato (`status.gerar()` chama assim, outro nome estoura TypeError);
`render_report(_TEMPLATE, data, output)`; um `_load_*()` por seção em try/except próprio.

Ler antes de escrever gráfico: [.claude/rules/lis-dashboards.md](../../../.claude/rules/lis-dashboards.md) —
réguas de range **abaixo** do gráfico e com `[from, to]` calculado dos traces (inclusive o "Tudo"),
primeira pintura com janela calculada e não `autorange`, `type:'linear'` explícito em todo eixo X que
não seja tempo, cabeçalho de 3 linhas dentro do card, ΔE2000 ≥ 20 entre séries que dividem gráfico, e
prosa escrita para quem nunca viu o dashboard.

### Passo 8 — Registro e testes

- `domain/dashboards/manifest.yaml`: entrada `key: brasil_structural_model`, `area: brasil`,
  `module`, `output`, `command`, `build_seconds` **medido**, um `role:` por dependência, `note:` em
  voz de produto (há um guarda em `tests/test_release_calendar_js.js` que reprova jargão como
  `generate_report`, `manifest.yaml`, `granularidade`).
- `procedures:` **sim, aqui é legítimo** — dois passos, `painel` e `modelo`, `granularidade:
  trimestre`. A regra da raiz ("um passo é dívida") pergunta se aquilo não deveria ser uma tabela;
  estimação de modelo não tem tabela que a substitua, que é exatamente por que os três passos do
  `monetary_policy` sobreviveram. `cut_from` obrigatório e dentro de `writes`.
- Nada a editar em `registry.py`, `update_db.py` ou `analytics/release_calendar/` — o regerar
  resolve pelo manifesto (`status.regerar_afetados`).
- `tests/test_structural_model_js.js` no padrão da casa (lê o HTML **gerado**, extrai o último
  `<script>`, DOM montado do markup real, stub de Plotly síncrono, `vm.runInContext`).
- Acrescentar `reports/brasil/Structural Model.html` à lista `GERADOS` de
  `tests/test_chart_head_js.js` (a §2 dele já varre `analytics/**/report.html` sozinha e reprova um
  relatório que plota sem cabeçalho).
- Linha nova na tabela de relatórios do `CLAUDE.md` da raiz e na de `analytics/CLAUDE.md`.

---

## Verification

Por passo, não só no fim:

```powershell
# painel
uv run python analytics/brasil/structural_model/panel.py
# cada equação: imprime coeficientes, NW t-stats, R2, e a coluna de robustez
uv run python -m analytics.brasil.structural_model.equations.phillips
# ... expectations, is_curve, taylor, fx
# relatório
uv run python -c "from analytics.brasil.structural_model.generate_report import run; run()"
node tests/test_structural_model_js.js
node tests/test_chart_head_js.js
uv run python -m domain.dashboards.status --validar
uv run python -m domain.dashboards.status --gerar brasil_structural_model
```

Validações que valem mais que "rodou sem exceção":

1. **Cada restrição fecha numericamente** — os pesos de (E) somam 1; o steady state de (R) com
   `dI=0` devolve `RR* + Meta`; o offset PPP de (F) tem β = 1 nos três lugares do payload.
2. **Sinais e ordens de grandeza contra o BC**: `i2 > 0`, `h2 < 0`, `r1` entre 0,7 e 0,95,
   `r2 > 1`. Cada um com o valor publicado do boxe ao lado na tabela do Apêndice.
3. **O simulador reproduz a história** quando alimentado com os exógenos realizados — resíduo por
   equação igual ao resíduo da estimação, a menos de arredondamento.
4. **O câmbio trimestral contra o mensal**, em unidade nativa, canal a canal.
5. **Uma inversão de sinal que só um gabarito pega**: antes de dividir duas séries, conferir se a
   fonte já publica a razão. Vale aqui para `g_RR` — o juro real ex-ante da Focus é reconstruível de
   duas maneiras e o repo já mediu qual bate (diferença simples, não Fisher).
6. **Confirmação em browser real** — nunca foi feita em nenhum relatório desta pasta, e é a
   pendência que sobrevive a todas as outras.

---

## Fora de escopo, declarado

Preços administrados como bloco próprio; hiato mundial; hiato estimado como estado latente (usamos o
do BC); CDS endógeno a um bloco fiscal; reseleção dos 5 canais do câmbio em frequência trimestral
(o corte 8→5 foi medido em mensal — se o `carry_vol` sair instável no trimestral, a alternativa
medida é dividi-lo em gap de política + vol, cujos loaders já existem); e a unificação com o modelo
do `FX Report`, que continua servindo o relatório cambial até este provar que o substitui.

---

## Pending

- **Próximo passo: estimar a equação (I).** O painel e a aba de dados estão prontos; as colunas que
  faltam no painel (juro real, neutra, meta, Selic, `dI`) entram junto com as equações que as usam.
- **Confirmação em browser real** — nunca feita. O harness executa o script contra um DOM de
  mentira, então cobre lógica e não pintura.
- **`describeChart()` compartilhado varre `card.children` com `.filter`**, que é método de `Array` e
  não de `HTMLCollection` — o objeto que um navegador devolve ali. Este relatório não passa por esse
  caminho (entrega `card._chFrame` montado), mas os outros seis que usam `/*CHART_HEAD_JS*/` passam.
  Vale confirmar em browser antes de mexer: o harness de todos eles usa um DOM de mentira em que
  `children` é um array de verdade, então a diferença não aparece em teste nenhum.
- **Vol implícita de opções do câmbio** — o usuário vai fornecer. Até lá, `VOL_SOURCE=realizada_lag`
  (janela de 126 pregões terminando no fecho do trimestre t−1). Destino recomendado quando chegar:
  tabela `macro_brasil.cmb_vol_implicita` pelo conector Bloomberg, não CSV à mão.
