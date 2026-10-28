# Report — externo · ciclo 2026-10-27 · rodada 2

Dados até: 27/10/2026 (F_externo, fixo no ciclo; a data do último dado vai com cada número) · Horizontes: 4T26 a 1T28, cada variável na convenção do Modelo Estrutural (`modelo.CONVENCAO`)[^conv] · Notícias: `noticias/demanda_r1.md`[^proc]

## 1. Tese

**A tese em uma frase:** o Fed sobe mais uma vez no 4T26, em 28/10 ou em 09/12, e para (efetivo de 4,13% de dez/26 a dez/27, ou 4,06% em dez/26 se a alta ficar para 09/12), uma alta a menos do que os T-bills precificam e a mesma que a projeção do próprio Fed de setembro indicava para 2026; a inflação americana desacelera de 1,12% no 3T26 para ~0,6% por trimestre em 2027 conforme o Brent devolve o pico de outubro (média de ~114 no 4T26 para ~91 no 1T28), devolução que o bloqueio em Hormuz torna menos provável do que na rodada 1; o dólar contra emergentes fica em 130–131 enquanto o Fed aperta e cede a 129 no 1T28; e as commodities em dólar ficam no alto e cedem devagar (IC-Br de 206 no 4T26 a 198 no 1T28), com metais em ~330 e o agro descendo de 204 para 197 junto com o petróleo. O salto do real depois de 25/10 é do Brasil: ele entra no índice do dólar EM, mas não no meu caminho. O maior risco para o Brasil continua atravessando blocos: um risk-off em que o CDS carrega o seu componente global.

**Bloco 1 — Política dos EUA** (cenários: base 55%, upside 30%, downside 15%)

| Variável | Trimestre | Central | Base: faixa · P | Upside: limite · P | Downside: limite · P | P(up) − P(down) |
|---|---|---|---|---|---|---|
| `ffr` — Fed Funds efetivo, média do último mês do trimestre (% a.a.) | 4T26 | 4,13 | 4,00 a 4,25 · 55% | acima de 4,25 · 30% | abaixo de 4,00 · 15% | +0,15 |
| | 1T27 | 4,13 | 3,88 a 4,38 · 55% | acima de 4,38 · 30% | abaixo de 3,88 · 15% | +0,15 |
| | 2T27 | 4,13 | 3,75 a 4,38 · 55% | acima de 4,38 · 30% | abaixo de 3,75 · 15% | +0,15 |
| | 3T27 | 4,13 | 3,63 a 4,38 · 55% | acima de 4,38 · 30% | abaixo de 3,63 · 15% | +0,15 |
| | 4T27 | 4,13 | 3,63 a 4,38 · 55% | acima de 4,38 · 30% | abaixo de 3,63 · 15% | +0,15 |
| | 1T28 | 3,88 | 3,50 a 4,25 · 55% | acima de 4,25 · 30% | abaixo de 3,50 · 15% | +0,15 |
| `infl_us` — CPI cheio, variação no trimestre (%, sem anualizar) | 4T26 | 0,86 | 0,65 a 1,10 · 55% | acima de 1,10 · 30% | abaixo de 0,65 · 15% | +0,15 |
| | 1T27 | 0,61 | 0,46 a 0,76 · 55% | acima de 0,76 · 30% | abaixo de 0,46 · 15% | +0,15 |
| | 2T27 | 0,61 | 0,46 a 0,76 · 50% | acima de 0,76 · 30% | abaixo de 0,46 · 20% | +0,10 |
| | 3T27 | 0,65 | 0,50 a 0,80 · 50% | acima de 0,80 · 30% | abaixo de 0,50 · 20% | +0,10 |
| | 4T27 | 0,63 | 0,48 a 0,78 · 50% | acima de 0,78 · 30% | abaixo de 0,48 · 20% | +0,10 |
| | 1T28 | 0,65 | 0,50 a 0,80 · 50% | acima de 0,80 · 30% | abaixo de 0,50 · 20% | +0,10 |

**Bloco 2 — Risco e dólar** (cenários: base 55%, risk-off 25%, risk-on 20%; o risk-off é o upside do dólar EM e o downside do S&P)

| Variável | Trimestre | Central | Base: faixa · P | Upside: limite · P | Downside: limite · P | P(up) − P(down) |
|---|---|---|---|---|---|---|
| `dxy_em` — dólar contra emergentes, fechamento (índice) | 4T26 | 130,5 | 129,2 a 132,0 · 55% | acima de 132,0 · 28% | abaixo de 129,2 · 17% | +0,11 |
| | 1T27 | 131,0 | 129,0 a 133,8 · 55% | acima de 133,8 · 28% | abaixo de 129,0 · 17% | +0,11 |
| | 2T27 | 130,5 | 128,2 a 133,0 · 55% | acima de 133,0 · 28% | abaixo de 128,2 · 17% | +0,11 |
| | 3T27 | 130,0 | 127,5 a 132,2 · 55% | acima de 132,2 · 28% | abaixo de 127,5 · 17% | +0,11 |
| | 4T27 | 129,5 | 127,0 a 131,5 · 55% | acima de 131,5 · 28% | abaixo de 127,0 · 17% | +0,11 |
| | 1T28 | 129,0 | 126,5 a 130,8 · 55% | acima de 130,8 · 28% | abaixo de 126,5 · 17% | +0,11 |
| `sp500` — S&P 500, fechamento (pontos) | 4T26 | 7.750 | 7.375 a 7.982 · 55% | acima de 7.982 · 20% | abaixo de 7.375 · 25% | −0,05 |
| | 1T27 | 7.900 | 7.200 a 8.137 · 55% | acima de 8.137 · 20% | abaixo de 7.200 · 25% | −0,05 |
| | 2T27 | 8.050 | 7.375 a 8.350 · 55% | acima de 8.350 · 20% | abaixo de 7.375 · 25% | −0,05 |
| | 3T27 | 8.200 | 7.575 a 8.575 · 55% | acima de 8.575 · 20% | abaixo de 7.575 · 25% | −0,05 |
| | 4T27 | 8.350 | 7.775 a 8.775 · 55% | acima de 8.775 · 20% | abaixo de 7.775 · 25% | −0,05 |
| | 1T28 | 8.500 | 7.975 a 8.975 · 55% | acima de 8.975 · 20% | abaixo de 7.975 · 25% | −0,05 |

**Bloco 3 — Commodities** (cenários: base 55%, alta 25%, queda ampla 20%; nos metais, mais 10 p.p. de uma queda só deles)

| Variável | Trimestre | Central | Base: faixa · P | Upside: limite · P | Downside: limite · P | P(up) − P(down) |
|---|---|---|---|---|---|---|
| `icbr_usd` — IC-Br em dólar, último mês do trimestre (índice) | 4T26 | 206,2 | 201,0 a 211,4 · 55% | acima de 211,4 · 25% | abaixo de 201,0 · 20% | +0,05 |
| | 1T27 | 202,6 | 195,4 a 209,8 · 55% | acima de 209,8 · 25% | abaixo de 195,4 · 20% | +0,05 |
| | 2T27 | 201,0 | 192,7 a 209,1 · 55% | acima de 209,1 · 25% | abaixo de 192,7 · 20% | +0,05 |
| | 3T27 | 199,9 | 191,6 a 208,4 · 55% | acima de 208,4 · 25% | abaixo de 191,6 · 20% | +0,05 |
| | 4T27 | 199,0 | 191,2 a 207,3 · 55% | acima de 207,3 · 25% | abaixo de 191,2 · 20% | +0,05 |
| | 1T28 | 198,3 | 191,1 a 206,8 · 55% | acima de 206,8 · 25% | abaixo de 191,1 · 20% | +0,05 |
| `icbr_agr_usd` — IC-Br agropecuária, média do trimestre (índice) | 4T26 | 203,9 | 199,8 a 208,0 · 70% | acima de 208,0 · 15% | abaixo de 199,8 · 15% | 0,00 |
| | 1T27 | 200,9 | 196,4 a 206,0 · 55% | acima de 206,0 · 25% | abaixo de 196,4 · 20% | +0,05 |
| | 2T27 | 199,3 | 193,9 a 205,6 · 55% | acima de 205,6 · 25% | abaixo de 193,9 · 20% | +0,05 |
| | 3T27 | 198,4 | 192,5 a 205,6 · 55% | acima de 205,6 · 25% | abaixo de 192,5 · 20% | +0,05 |
| | 4T27 | 197,8 | 192,1 a 205,1 · 55% | acima de 205,1 · 25% | abaixo de 192,1 · 20% | +0,05 |
| | 1T28 | 197,4 | 192,1 a 204,6 · 55% | acima de 204,6 · 25% | abaixo de 192,1 · 20% | +0,05 |
| `icbr_met_usd` — IC-Br metal, média do trimestre (índice) | 4T26 | 331,7 | 321,7 a 341,7 · 50% | acima de 341,7 · 20% | abaixo de 321,7 · 30% | −0,10 |
| | 1T27 | 330,0 | 314,1 a 344,0 · 50% | acima de 344,0 · 20% | abaixo de 314,1 · 30% | −0,10 |
| | 2T27 | 330,0 | 306,6 a 346,0 · 50% | acima de 346,0 · 20% | abaixo de 306,6 · 30% | −0,10 |
| | 3T27 | 328,7 | 302,9 a 345,4 · 50% | acima de 345,4 · 20% | abaixo de 302,9 · 30% | −0,10 |
| | 4T27 | 327,3 | 301,1 a 344,6 · 50% | acima de 344,6 · 20% | abaixo de 301,1 · 30% | −0,10 |
| | 1T28 | 325,7 | 300,4 a 343,9 · 50% | acima de 343,9 · 20% | abaixo de 300,4 · 30% | −0,10 |

A faixa base de cada linha vai até a metade da distância entre o caminho base e o caminho do cenário de cauda, com uma meia-largura mínima (0,12 p.p. no `ffr`, 0,15 p.p. no `infl_us`, 1% no dólar EM, 3% no S&P, 2,5% no IC-Br, 2% no agro, 3% nos metais). Três linhas fogem da probabilidade do bloco, cada uma por um motivo: no `infl_us` de 2T27 em diante a faixa fica com 50%, porque ali os cenários convergem e o ruído trimestral do CPI (desvio-padrão de 0,30 p.p. entre 1T23 e 3T26, `inflc_cpi`) pesa mais que a distância entre eles; no dólar EM a cauda de cima ganha 3 p.p., porque o índice publicado vai carregar o salto do real de 26/10 que o meu caminho não carrega (seção 2.2); e no agro do 4T26 a faixa fica com 70%, porque com dois meses por medir os caminhos de cauda ainda caem dentro da meia-largura mínima.

**O que leva a cada cauda**

- **Política dos EUA, upside** (Fed acima de 4,25 no 4T26; inflação acima da faixa): o Brent fica em 125–132 até o 1T27 e o núcleo do CPI mantém o ritmo de setembro (0,33% ao mês); o Fed sobe em 28/10 e de novo em 09/12 e chega a 4,63 no 1T27, o caminho que os T-bills precificam. No modelo a PTAX fica **abaixo** da base (5,41 contra 5,43 no 4T26), porque a inflação americana maior pesa mais pelo desconto de PPC[^ppc] do que a perda de carry: bom para o real dentro do modelo, ruim fora dele, pelo aperto das condições financeiras globais.
- **Política dos EUA, downside** (Fed abaixo da faixa; inflação abaixo): o fluxo por Hormuz volta, o Brent cai a ~80 no 1T27, o desemprego passa de 4,5% e o Fed não sobe mais em 2026, devolve a alta no 1T27 e corta até 3,13 no 3T27. No modelo a PTAX fica **acima** da base (5,62 contra 5,58 no 1T28): a inflação americana menor pesa mais que o carry maior.
- **Risco e dólar, risk-off** (dólar EM acima da faixa, S&P abaixo): o S&P cai ~16% até o 1T27 (6.500, contra 7.717 em 27/10) e o dólar EM sobe a 136,5. Ruim para o Brasil, mas só aparece no modelo se o CDS subir junto: com o CDS do fiscal acrescido do componente global (175 p.b. no 4T26, 204 no 1T27), a PTAX vai a 5,79 no 1T27; com o CDS do fiscal sem ele, o modelo põe a PTAX **abaixo** da base (5,48 contra 5,51), porque o S&P em queda, sozinho, aprecia o real na (F).
- **Risco e dólar, risk-on** (dólar EM abaixo, S&P acima): dólar EM a 124 e S&P a 9.450 no 1T28. Bom para o real: PTAX de 5,18–5,29 em todo o horizonte com o componente global no CDS, 5,38–5,52 sem ele.
- **Commodities, alta**: os ataques a petroleiros em Hormuz continuam e o fluxo não volta; Brent de 129–130 no 4T26–1T27, metais a 362 (+10% contra a média do 3T26), agro a ~212. Bom pelo câmbio (PTAX 5,37 no 4T26 e 5,50 no 1T28, contra 5,43 e 5,58) e ruim pela inflação (IPCA 12m de 4,67% no 2T27, contra 4,46%).
- **Commodities, queda ampla**: o fluxo por Hormuz se normaliza (Brent a 78), a desaceleração global e o dólar forte derrubam metais a 275 (−17%) e agro a ~187 (−7%) até o fim de 2027. Ruim pelo câmbio (PTAX 5,66 no 1T28) e bom pela inflação (IPCA 12m de 3,82% no 1T28, contra 4,15%). Nos metais, a cauda de baixa tem mais 10 p.p.: a demanda chinesa por minério fraca, sem queda do petróleo nem do agro (seção 2.3).

## 2. Argumentação

### 2.1 Política dos EUA (Q1)

**O Fed voltou a subir porque a inflação acelerou e a expectativa desancorou na margem, e não por um mercado de trabalho apertado, e o próprio Fed sinalizou mais uma alta em 2026.** O FOMC decidiu em 16/09 subir a meta em 0,25 p.p., para 3,75–4,00%, dizendo que "Inflation remains elevated", e as projeções trimestrais indicavam "one more rate increase this year" (Al Jazeera · 16/09 · nível A); a meta nova vale desde 17/09 (ponto médio 3,875; `us_interest_rate`, curva POLICY), depois de três cortes de 0,25 p.p. vigentes em 18/09, 30/10 e 11/12/2025 (mesma tabela, por G). Segundo o Yahoo Finance, os 18 membros apoiaram a alta e "most expect another hike by year-end", e as próximas reuniões são em 27–28/10 e 08–09/12 (Yahoo Finance · 08/10 · nível B, datas atribuídas pela página ao The Hill). A decisão de 28/10 sai depois do corte do F e não está em nenhuma notícia do ciclo: ela é o primeiro evento dos cenários do bloco. O que sustenta a leitura de que o gatilho foi inflação:

| Medida | Último | Leitura |
|---|---|---|
| CPI cheio, 12 meses | 3,72% (`inflc_cpi` · set/26) | 3m anualizado 4,56% |
| CPI núcleo, 3m anualizado | 3,41% (`inflc_cpi` · set/26) | 12 meses 2,57% |
| CPI serviços sem energia, 3m anualizado | 3,76% (`inflc_cpi` · set/26) | 12 meses 3,16% |
| CPI energia, 12 meses | +20,4% (`inflc_cpi` · set/26) | +5,2% só em setembro |
| PCE núcleo, 12 meses | 3,01% (`inflc_pce` · ago/26) | 3m anualizado 2,05% |
| Inflação esperada 1 ano (Cleveland Fed) | 2,98% (`expc_inflacao` · out/26) | +0,59 p.p. em 3 meses |
| Inflação esperada 10 anos | 2,73% (`expc_inflacao` · out/26) | percentil 100 em 10 anos[^pctl] |

O núcleo do CPI acelerou três meses seguidos (0,22%, 0,29% e 0,33% em jul, ago e set; `inflc_cpi`, por G), o que mostra que o choque de energia começa a passar para o resto da cesta; e a inflação esperada subiu em todos os prazos, com a de 10 anos no maior nível da década. **Mas** a medida que o Fed persegue é mais calma: o PCE núcleo subiu só 0,13% em junho e em julho e 0,25% em agosto (`inflc_pce`, por G), 2,05% anualizado em três meses. Se o PCE núcleo de setembro vier abaixo de 0,25%, o argumento para uma segunda alta enfraquece; acima de 0,30%, ele passa a ser o cenário base.

**Com as datas das reuniões, a alta do base cabe no 4T26 nos dois casos.** Com o efetivo 0,005 p.p. acima do ponto médio da meta (média de mai a ago/26, `diferenciais_juros` e `us_interest_rate`, por G), uma alta em 28/10 dá média de dezembro de 4,13; uma alta só em 09/12, de 4,06; duas altas (28/10 e 09/12), 4,31; nenhuma, 3,88 (por G). As duas primeiras caem na faixa base do 4T26 (4,00 a 4,25), a terceira no upside e a última no downside. O downside do 4T26 cai de 20% para 15% porque ele pede que o Fed não faça a alta que ele mesmo projetou para 2026; o upside fica em 30%, porque a maioria que quer mais uma alta (nível B) e os T-bills (abaixo) não dizem que serão duas.

**O mercado de trabalho não pede aperto, mas também não força corte.** A criação de vagas é fraca: +29 mil em setembro (preliminar), média de 51 mil em 3 meses e de 41 mil em 12 meses (`mt_ces`, por G). Contratações e pedidos de demissão estão nos percentis 16 e 10 dos últimos dez anos (3,3% e 1,9%; `mt_jolts` · ago/26), um mercado de pouca rotatividade, e o salário por hora sobe 3,0% em 12 meses (`mt_ces` · set/26), o que afasta uma espiral salário-preço. **Mas** o desemprego não sobe: 4,2% (`mt_cps` · set/26), 0,2 p.p. abaixo de um ano antes, com a participação subindo 0,3 p.p. em 3 meses. Vagas fracas com desemprego estável dizem que pouca criação já basta para absorver a força de trabalho, e é isso que deixa o Fed livre para subir. O downside (o Fed devolve a alta) precisa do desemprego subindo: acima de 4,5% por dois meses, ele ganha probabilidade.

**Onde o meu caminho difere do mercado.** Os T-bills de 23/10 estão todos acima da meta (tabela). Descontado o prêmio que eles carregam em meses de Fed parado (de −0,03 a +0,05 p.p. no de 3 meses, +0,03 a +0,08 no de 6 meses, +0,09 a +0,10 no de 1 ano; `us_interest_rate` e `diferenciais_juros`, por G[^tbill]), eles precificam um efetivo médio de 4,17–4,25% nos próximos três meses e de 4,41–4,48% entre seis e doze meses, contra 3,88% hoje: perto de uma alta imediata e de duas em doze meses. O meu base tem uma. A diferença, ~0,3 p.p. em 2027, é a razão de o upside do bloco ter o dobro da probabilidade do downside.

| Vértice (23/10/2026) | Taxa | Menos a meta (p.p.) |
|---|---|---|
| Treasury 3 meses | 4,22 | +0,34 |
| Treasury 6 meses | 4,30 | +0,42 |
| Treasury 1 ano | 4,44 | +0,57 |
| Treasury 2 anos | 4,69 | +0,82 |

(`us_interest_rate`, leitura combinada do F)

**A ponta longa sobe com a curta, não por prêmio.** O Treasury de 10 anos está em 5,00% (`us_interest_rate` · 23/10), +0,99 p.p. em 12 meses, depois de tocar 5,31% em 05/10, o maior nível desde 2007 (por G). O juro real ex-ante[^real] de 10 anos é 2,27% no ponto de 23/10 (5,00 − 2,73, leitura combinada do F) e 2,45% na média de outubro (por G), também o maior desde 2007. Em três meses, o de 2 anos subiu 0,32 p.p. e o de 10 anos 0,29 p.p., e a inclinação 30 anos − 10 anos caiu de +0,46 para +0,33 p.p. (`us_interest_rate`): o longo andou com a expectativa de juro, não com um prêmio de prazo[^tp] crescente na ponta, o que põe o movimento no bloco do Fed e da inflação. Desde 02/10 (data do ciclo anterior do F), o 10 anos caiu 0,28 p.p. e o 2 anos 0,14 p.p., junto com o Brent (−15% no período, `comm_brent`): a ponta longa está negociando petróleo. **Mas** o banco não tem estimativa de prêmio de prazo nem futuros de Fed Funds, a separação acima é por inclinações, e a queda de 0,17 p.p. do 10 anos num único pregão (21/10 → 22/10, por G) segue sem explicação: o agente web não achou notícia com data de 22/10 que a explique.

**Caminho do Treasury de 10 anos** (média do trimestre, % a.a.; não é variável do modelo, vai ao fiscal pelo XE10, juízo meu sobre os cenários do bloco; sem mudança contra a rodada 1): base 5,05 · 4,95 · 4,90 · 4,85 · 4,80 · 4,75 (4T26 a 1T28); upside 5,40 · 5,55 · 5,50 · 5,45 · 5,40 · 5,35; downside 4,70 · 4,45 · 4,35 · 4,30 · 4,30 · 4,30.

**A inflação americana do modelo.** O `infl_us` do 3T26 foi 1,12% (leitura combinada do F), com o núcleo em 0,84% e a energia em +5,65% no trimestre (`inflc_cpi`, por G), contra uma média de 0,45% em 2015–2019 e 0,79% de 1T23 a 3T26 (por G). O caminho base sai de um núcleo de 0,27% ao mês no 4T26, cedendo a 0,24%, e do Brent base (seção 2.3), pela regressão trimestral do CPI cheio no núcleo, na energia e nos alimentos (2010–2026, por G): 0,86% no 4T26, porque o Brent médio de outubro (125,0 até 20/10, `comm_brent`) ainda chega à energia de outubro e novembro, e 0,61–0,65% de 2027 em diante. É abaixo do padrão do simulador (0,91%, a média dos últimos quatro trimestres), e isso tem efeito no câmbio do modelo (2.4).

### 2.2 Risco e dólar (Q2)

**O ciclo financeiro global[^gfc] virou contra os emergentes na margem, pelo juro americano e pela desmontagem de carry, e não por aversão a risco.** O dólar contra emergentes[^em] subiu de 126,1 em 09/09 (a mínima de 2026) para 130,2 em 23/10 (`cmb_dollar_index_em`, por G), +1,6% no último mês; o DXY foi de 99,7 em 01/09 para 102,2 em 27/10 (`cmb_dollar_index`, por G). O dólar subiu contra desenvolvidos e emergentes ao mesmo tempo, na janela da alta do Fed e do salto do Brent. Que o motor é juro, e não pânico, mostra o S&P: 7.717 em 27/10 (`cmb_equity_us`), a 1,3% da máxima histórica de 7.819 de 06/10 (por G), +4,1% em 3 meses. Na correlação dos retornos diários (leitura combinada do F), o dólar EM anda mais com o DXY (+0,59 em 3 meses) do que contra o S&P (−0,43 em 3 meses, contra −0,49 em 12 meses): o fator dólar global está mais forte que o fator risco.

As moedas latinas, dado do câmbio lido como consulta, enfraqueceram todas no mês até 20/10 (`cmb_fx_latam`): peso mexicano +7,8%, peso chileno +2,8%, peso colombiano +2,3%, sol +2,5%. O do México é o maior, e Gabriela Siller (Grupo Financiero Base) disse que a máxima do dólar contra o peso em 22/10 foi "impulsado por el desmantelamiento de posturas de carry trade", com "temores por los incrementos en precios de energía y la corrección a la baja de emisoras del sector tecnológico" (Investing.com México · 22/10 · nível B). Os três motivos são de fora do México: carry, petróleo e bolsa americana. Isso sustenta que a alta do dólar EM de outubro é global e não um evento mexicano, e por isso o meu base não a desconta; e o dado de posição vai no mesmo sentido: os asset managers passaram de comprados a vendidos em peso no mês, com −77 mil contratos em um mês até −24 mil em 20/10, e os fundos alavancados cortaram 26 mil (`cmb_cot_fx`, dado do câmbio). **Mas** desmontagem de posição é um movimento que se esgota quando a posição acaba, e por isso não a projeto adiante: ela explica parte da alta de outubro, não sustenta mais alta. No QPC de 23/09, 67% dos respondentes viam o ambiente externo menos favorável, contra 62% em agosto (`expc_qpc`, dado de expectativas, lido como consulta).

**O salto do real depois de 25/10 entra no índice, mas não no meu caminho.** O real foi de 5,04 em 23/10 para 5,50 em 26/10 (+8,8%, `cmb_ptax`, dado do câmbio), depois da reeleição do presidente Lula em 25/10 (CNN Brasil · 25/10 · nível A). No mesmo pregão o DXY subiu 0,15% e o S&P 0,69%, e de 23/10 a 27/10, 0,39% e 1,22% (`cmb_dollar_index`, `cmb_equity_us`, por G): não houve movimento global, como o câmbio concluiu (E2, E13). O índice do dólar EM ainda não tem dado depois de 23/10, mas o real está dentro dele: numa regressão diária do dólar EM no real, nos pesos mexicano, chileno e colombiano, no sol e no DXY (2023–2026, R² 0,68), o real tem coeficiente de 0,072 (t 6,6) (`cmb_dollar_index_em`, `cmb_ptax`, `cmb_fx_latam`, `cmb_dollar_index`, por G)[^peso]. Por ele, o pregão de 26/10 sobe o índice ~0,6% (~0,8 ponto) sem nenhum dólar global; com o real na central do câmbio da rodada 1 (5,35–5,39 em todo o horizonte, contra 5,04 em 23/10), o efeito fica em 0,43–0,48% enquanto o real não voltar (por G). Escrevo o caminho sem esse salto, como o câmbio pede como subordinado: posto no caminho, ele levaria a PTAX do modelo de 5,43 para 5,45 no 4T26 e de 5,58 para 5,61 no 1T28 (por G), uma depreciação do real explicada pelo próprio real, que a (F) leria como dólar global e somaria ao que o câmbio já escreveu na volatilidade e no CDS. O preço da escolha é que o índice publicado deve fechar acima do caminho pelo salto mecânico, e por isso a cauda de cima ganha 3 p.p. (de 25% para 28%) e a de baixo perde 3 (de 20% para 17%). O placar deste ciclo tem de ler o dólar EM descontado do real.

**Os pares não andam juntos.** México em 6,50% (−1,00 p.p. em 12 meses), Chile em 4,50%, Peru em 4,25%, todos parados no último mês; a Colômbia subiu 0,25 p.p. no mês e 3,00 p.p. em 12 meses, para 12,25% (`inter_interest_rate` · 20/10). Nos juros reais ex-post de agosto (`cmb_real_rates`), o Brasil tem o maior (9,78%), à frente de Colômbia (5,76%), México (3,24%), Chile (0,37%) e Peru (−0,19%). **Mas** o ex-post subestima o aperto de quem está desinflando e superestima o de quem tem inflação subindo (Colômbia, 6,24% em 12 meses), então a comparação é de ordem, não de distância.

**Por que o dólar EM fica alto, e não sobe mais, no base.** Não há regularidade estável de o dólar EM subir quando o Fed sobe: nos 11 trimestres de alta do efetivo de 2007 a 2026, o dólar EM subiu em média 0,25%, contra 0,19% nos 55 trimestres de Fed parado (`diferenciais_juros` e `cmb_dollar_index_em`, por G). O que move o dólar EM de verdade é aversão a risco: nos 9 trimestres em que o S&P caiu 8% ou mais (2007–2026), o dólar EM subiu 4,1% em média (por G), e a correlação trimestral entre os dois é −0,62. Por isso o base tem o dólar EM em 130,5–131 enquanto o Fed sobe (uma alta só, já na metade precificada) e cedendo a 129 no 1T28, quando o Brent já caiu e o Fed começa a cortar; e o S&P subindo ~2% por trimestre, abaixo da mediana histórica de 3,8% por trimestre (por G), porque o juro real de 10 anos está no maior nível desde 2007 e o Fed está apertando.

**Por que o risk-off tem mais probabilidade que o risk-on (25% contra 20%).** O S&P está no percentil 99 de dez anos (F) com o juro real americano no topo de quase duas décadas; uma correção não precisa de recessão, só de mais uma alta do Fed. A mesma analista citou a "corrección a la baja" do setor de tecnologia como motivo da saída do peso (Investing.com México · 22/10 · nível B), e o S&P chegou a 7.624 em 23/10, 2,5% abaixo da máxima de 06/10 (por G), antes de voltar a 7.717 em 27/10 (`cmb_equity_us`, por G): uma correção pequena já tirou dinheiro de carry. **Mas** o banco não tem medida de valuation, VIX nem spread de crédito emergente: o argumento é a combinação de preço alto com juro real alto, não um indicador de estresse. Se o S&P fechar abaixo de 7.375 com o dólar EM acima de 132 (descontado o real), o risk-off passa a ser o cenário corrente.

### 2.3 Commodities (Q3)

**O IC-Br em dólar[^icbr] está perto do recorde, e em 12 meses quem puxou foram metais e energia, não o agro.** O índice total marcou 205,7 em setembro (`comm_icbr_usd`), percentil 99 em dez anos e +12,8% em 12 meses. Na combinação estimada por G (regressão mensal do Δlog do total nos três grupos, 2022–2026, R² 0,99), o agro pesa 0,63, metais 0,17 e energia 0,19; em 12 meses, metais subiram 42,2% e energia 29,2%, contra 0,7% do agro (`comm_icbr_usd` · set/26). No último mês publicado, a energia sozinha subiu 10,6%.

| Mês | IC-Br | Agro | Metal | Energia | Brent, média do mês |
|---|---|---|---|---|---|
| 2026-06 | 197,6 | 195,3 | 332,9 | 86,3 | 85,4 |
| 2026-07 | 196,8 | 198,6 | 318,3 | 84,0 | 83,8 |
| 2026-08 | 202,3 | 201,2 | 337,1 | 86,8 | 91,1 |
| 2026-09 | 205,7 | 201,8 | 335,1 | 96,0 | 114,2 |
| 2026-10 | — | — | — | — | 125,0 (até 20/10) |

(`comm_icbr_usd`, `comm_brent`, leitura combinada do F; outubro por G)

**Energia: um choque de oferta com nome, Hormuz, ainda aberto.** O Brent fez em 2026 dois picos e uma volta: 66,6 de média em janeiro, 117,3 em abril (máxima diária de 138,21 em 07/04), 83,8 em julho, 114,2 em setembro (`comm_brent`, por G). Em 02/10 ele saltou de 114,82 para 135,51 num pregão e desde 16/10 recua, a 115,22 em 20/10. A rodada 1 lia isso como evento de oferta sem saber qual; as notícias dão o evento. Segundo a Kpler, via Al Jazeera, "10 tankers were struck in the strait between September 28 and October 4", e só 2,9 milhões de barris passaram por Hormuz em 11/10 (Al Jazeera · 14/10 · nível B); em 19/10, com o Brent acima de US$ 110, os operadores estavam "increasingly pessimistic about the resumption of normal oil flows out of the Persian Gulf", e o ING disse que "the market is pricing in a significant risk premium" (OilPrice.com · 19/10 · nível B). A queda de 135 para 115 aconteceu, portanto, com o fluxo ainda interrompido: é prêmio saindo do preço, não o choque se resolvendo. Mantenho o caminho base (Brent médio de 114 no 4T26, 105 no 1T27, 91 no 1T28), porque nenhuma das duas notícias diz quando o fluxo volta, e o ING aponta prêmio a devolver; **mas** o cenário de alta, em que o fluxo não volta, passa de 20% para 25%, e o de queda ampla, que pede o Brent a 78 já no 2T27, de 25% para 20%. A decisão da OPEP+ de 04/10 aparece só em fonte fora da lista do agente web e não entra. O IC-Br energia segue o Brent com elasticidade de 0,48 no mês (2010–2026, R² 0,59, por G). O cenário de referência do Copom parte de um Brent de US$ 90 no 3T26 e chega a ~84 no 2T27 (RPM de set/26, citado pelo agente de política monetária): abaixo do meu base em todo o horizonte, e no 2T27 mais perto do meu cenário de queda (79) do que do base (99).

**Metais: estáveis no topo, com o dólar contra e um risco de baixa que vem da China.** O IC-Br metal está em 335,1 (`comm_icbr_usd` · set/26), abaixo do pico de 350,9 de maio e de lado desde o 1T26 (médias trimestrais de 328,8, 339,4 e 330,1; por G). O motor histórico é a demanda chinesa, e o banco não tem dado da China: a exportação brasileira para a China somou US$ 109,0 bi em 12 meses, contra US$ 93,5 bi um ano antes (`cmb_comex_pais` · set/26, dado do câmbio lido como consulta), o que é coerente com preço alto, mas mistura preço e volume. O dólar é um vento contra só neste grupo: a correlação mensal dos metais com o dólar EM é −0,45 em 24 meses e −0,55 em 60 meses, enquanto a do índice total caiu a −0,04 em 24 meses (contra −0,44 de 2010 a 2026; `comm_icbr_usd` e `cmb_dollar_index_em`, por G). Com o dólar EM alto no base, os metais derivam de 331,7 no 4T26 para 325,7 no 1T28. A notícia nova vai contra o grupo: o minério de ferro caiu em 27/10 à mínima de dois anos, com o futuro de Singapura a US$ 89,25 a tonelada, e um analista citado só como "Jiang" disse que as usinas chinesas compram "hand-to-mouth" e ficaram "desensitized to macro stimulus" (Yahoo Finance/Bloomberg · 27/10 · nível C). Por ser nível C, ela não move o caminho: entra como risco, com 10 p.p. a mais na cauda de baixa dos metais, de uma queda só deles, sem o petróleo e o agro (cauda de 30%); e a cauda de cima dos metais fica em 20%, cinco abaixo do cenário de alta do bloco, porque com a China fraca parte desse cenário (o petróleo subindo por Hormuz) não leva os metais junto. A faixa fica com 50%. O banco não separa o minério dentro do IC-Br metal, e o índice perto do recorde com o minério na mínima de dois anos diz que outros metais sustentam o grupo; se o IC-Br metal de outubro vier abaixo de 322, a queda só de metais passa a ser o cenário corrente.

**Agro: no recorde, e agora descendo junto com o petróleo.** O IC-Br agropecuária está em 201,8 (`comm_icbr_usd` · set/26), a 1% do recorde de 203,9 de jan/25 (por G), com +0,7% em 12 meses. Na rodada 1 o base era parado em 202, por falta de sinal; o agente de inflação perguntou se o Brent alto entra no caminho, e entra, pelo dado: numa regressão mensal do Δlog do agro no Δlog do Brent (corrente e defasado até seis meses) e do dólar EM, 2016–2026, o Brent corrente tem coeficiente de 0,11 (t 5,2), a soma de seis meses dá 0,16 (t 2,9) e o dólar EM −0,46 (t −2,5), com R² de 0,32 (`comm_icbr_usd`, `comm_brent`, `cmb_dollar_index_em`, por G)[^agro]. O caminho base passa a sair dessa ligação: o agro sobe a 203,9 de média no 4T26, com o Brent de outubro chegando, e cede a 197,4 no 1T28 conforme o Brent devolve. **Mas** o sinal da oferta fica dividido: a Conab prevê safra de grãos acima de 367 milhões de toneladas, +1,4% sobre a anterior, mesmo com um El Niño que "atingirá o Brasil de forma severa neste segundo semestre de 2026 e início de 2027" (Agência Brasil · 15/10 · nível B). Safra maior pesa nos preços, e o clima é risco de alta; sem dado de safra, clima ou estoques no banco, nenhum dos dois move o caminho, e o cenário de alta continua tendo o agro subindo com o custo de fertilizante e frete.

**Consistência das convenções.** O total do trimestre é o último mês e os grupos são média. No base, o IC-Br de outubro deve sair perto de 208, acima dos 205,7 de setembro pela energia (por G), como o câmbio argumenta; o total do 4T26 é o de dezembro (206,2), que já carrega parte da queda do Brent de outubro para dezembro, enquanto a média da energia no trimestre (96,1) ainda carrega o pico de outubro.

### 2.4 Como chega ao Brasil (Q4)

Com os meus caminhos base e as outras exógenas nos caminhos do P1 (meta, `rr_10a` e CDS do fiscal e da política monetária, volatilidade do câmbio), a PTAX do modelo vai a 5,43 no 4T26 e 5,58 no 1T28, contra 5,36 e 5,34 com as minhas sete no padrão do simulador; o IPCA 12m sobe pouco (4,15% contra 4,09% no 1T28) e a Selic quase não muda (11,98% contra 11,95% de média no 1T28) (por G). Contra o P1, a PTAX sobe 0,017 no 1T28 e o IPCA cai 0,04 p.p.: os dois vêm do agro mais baixo em 2027. A decomposição tira uma exógena de cada vez do base (por G):

| Linha do mapa (2.8) | Moveu? | Sinal para o Brasil, no modelo | Quanto na PTAX (base contra base sem a variável) | Quem precisa ouvir |
|---|---|---|---|---|
| Fed (`ffr`, carry) | sim: alta em set/26 e mais uma no 4T26 | real mais fraco | +0,01 no 4T26; +0,005 no 1T28 | câmbio; política monetária (espaço do Copom contra o Fed) |
| Curva dos EUA (fora do modelo) | sim: 10 anos em 5,00%, juro real no topo desde 2007 | pressão de alta em `rr_10a` | via `rr_10a`, que não escrevo | fiscal (principal de `rr_10a`) |
| Inflação dos EUA (`infl_us`, desconto de PPC) | sim: 3T26 em 1,12%; base cai a ~0,6% | real mais fraco (inflação americana abaixo do padrão de 0,91%) | +0,08 no 1T28 | câmbio |
| Dólar global (`dxy_em`) | sim: +1,6% no mês até 23/10; o salto do real fica fora | real mais fraco no 4T26–1T27; mais forte depois | +0,04 no 4T26; −0,01 no 1T28 | câmbio |
| Apetite a risco (`sp500`) | não no nível; base sobe ~2% por trimestre | real mais fraco (sinal condicional da (F)[^sp]) | +0,02 no 4T26; +0,13 no 1T28, o maior canal | câmbio; fiscal (CDS) |
| Commodities (`icbr_usd`; `icbr_agr_usd`, `icbr_met_usd`) | sim: energia +10,6% em set; metais +42% em 12 meses; agro cedendo com o Brent | `icbr_usd` em queda: real mais fraco; agro em queda: pouco menos inflação | +0,05 no 1T28 | câmbio; inflação |
| Energia (fora do modelo) | sim: Brent +90% em 12 meses; Hormuz aberto | combustíveis e monitorados | — | inflação, fiscal (royalties) |
| Pares (fora do modelo) | Colômbia subindo, México parado depois de cortar | carry relativo | — | política monetária, câmbio |

O canal que mais move a PTAX no meu base continua sendo o S&P subindo, que no modelo deprecia o real porque o coeficiente é condicional ao CDS e ao dólar EM. Isso só é coerente se o CDS do fiscal carregar a compressão que um S&P em alta e um dólar EM em queda trazem em 2027. O caminho do fiscal não carrega: ele fica em 135 de 3T27 a 1T28, enquanto o componente global do meu base cai de +13 p.b. no 1T27 para −11 p.b. no 1T28 (seção 4, "Como subordinado"). É o argumento ao fiscal.

**Olhado, sem sinal**
- Juro real ex-post dos EUA · 0,03% (`diferenciais_juros` · set/26) · o CPI de 12 meses está inflado pela energia, então o ex-post fica perto de zero sem dizer nada sobre o aperto · diria algo se o núcleo convergisse e o ex-post continuasse baixo.
- PCE cheio, 3m anualizado · 1,03% (`inflc_pce` · ago/26) · a janela pega a queda da energia de junho e julho · diria algo depois do salto de setembro chegar ao PCE.
- Desemprego amplo (U-6) · 7,6% (`mt_cps` · set/26), −0,5 p.p. em 12 meses · anda com o U-3 · diria algo se divergisse dele.
- Payroll privado · +46 mil em set (`mt_ces`) · mesmo sinal do total · diria algo se o governo passasse a explicar a fraqueza do total.
- Demissões, taxa · 1,0% (`mt_jolts` · ago/26), percentil 31 · sem demissões, o mercado esfria pela contratação · diria algo acima de 1,3%.
- Chile, Peru · 4,50% e 4,25% (`inter_interest_rate` · 20/10), parados · sem movimento no ciclo · diria algo com corte ou alta.
- Termos de troca (Funcex) · 108,44, −3,0% em 3 meses (`cmb_termos_troca` · ago/26, dado do câmbio) · conclusão é do câmbio · diria algo ao meu bloco se caísse com o IC-Br subindo (choque de energia contra o Brasil).
- Exportação para os EUA · US$ 35,8 bi em 12 meses, contra 40,4 bi (`cmb_comex_pais` · set/26, dado do câmbio) · é demanda externa da atividade, não muda meus caminhos · diria algo se viesse junto de queda da atividade americana, que o banco não tem.

## 3. Premissas

### 3.1 Etapa 1 — o modelo

**Cenários.**

*Bloco 1, Política dos EUA*
- Base (55%): o choque de energia passa ao núcleo devagar (0,27% ao mês caindo a 0,24%); o Brent devolve o pico de outubro sem voltar a 84; o Fed faz em 28/10 ou em 09/12 a alta que projetou para 2026, para 4,00–4,25%, e para; o primeiro corte vem no 1T28, com a inflação de volta a ~0,6% por trimestre.
- Upside (30%): o fluxo por Hormuz não volta e o Brent fica em 125–132 até o 1T27, o núcleo segue a 0,33% ao mês e a inflação esperada de 1 ano passa de 3%; o Fed sobe em 28/10 e em 09/12 e mais uma vez no 1T27, até 4,50–4,75% (o caminho dos T-bills), e fica lá.
- Downside (15%): o fluxo por Hormuz volta, o Brent cai a ~80 no 1T27, o desemprego passa de 4,5% e o núcleo volta a 0,20% ao mês; o Fed não faz a alta projetada, devolve a de setembro no 1T27 e corta até 3,00–3,25% no 3T27.

*Bloco 2, Risco e dólar*
- Base (55%): o dólar segue sustentado pelo juro americano enquanto o Fed sobe e cede a partir de 2027; o S&P sobe ~2% por trimestre, abaixo da história, com juro real alto. O dólar EM do caminho não carrega o salto do real de 26/10.
- Upside do dólar EM / downside do S&P, risk-off (25%): mais uma alta do Fed com o Treasury de 10 anos acima de 5,4% derruba o S&P ~16% até o 1T27, com a correção de tecnologia que já tirou carry do peso mexicano em outubro; o dólar EM sobe ~5%; recuperação lenta depois.
- Downside do dólar EM / upside do S&P, risk-on (20%): o Brent cai, o Fed para e depois corta, o dólar EM enfraquece ~5% até o 1T28 e o S&P sobe ~4% por trimestre até o 3T27.

*Bloco 3, Commodities*
- Base (55%): Brent de 114 (4T26) a 91 (1T28) em média do trimestre, com o prêmio de Hormuz saindo devagar; metais estáveis em ~330 com o dólar alto; agro de 204 a 197, seguindo o Brent pela ligação medida.
- Upside (25%): os ataques em Hormuz continuam e o fluxo não volta (Brent 129–130 no 4T26–1T27); custo de energia e demanda puxam metais a 362 e agro a ~212.
- Downside, queda ampla (20%): o fluxo por Hormuz se normaliza (Brent 78), a desaceleração global e o dólar forte derrubam metais a 275 e agro a ~187. Nos metais, mais 10 p.p. de uma queda só deles, pela demanda chinesa por minério, sem caminho próprio no modelo (a probabilidade é da linha dos metais, seção 1).

**Caminhos das exógenas** (só as sete de que sou principal; as outras nos caminhos do P1[^proc])

| Exógena | Hoje (valor · tabela · data) | Cenário | 4T26 | 1T27 | 2T27 | 3T27 | 4T27 | 1T28 |
|---|---|---|---|---|---|---|---|---|
| `ffr` (% a.a.) | 3,75 · `diferenciais_juros` · set/26 (meta 3,875 desde 17/09) | base | 4,13 | 4,13 | 4,13 | 4,13 | 4,13 | 3,88 |
| | | upside | 4,38 | 4,63 | 4,63 | 4,63 | 4,63 | 4,63 |
| | | downside | 3,88 | 3,63 | 3,38 | 3,13 | 3,13 | 3,13 |
| `infl_us` (% no trimestre) | 1,12 · `inflc_cpi` · 3T26 | base | 0,86 | 0,61 | 0,61 | 0,65 | 0,63 | 0,65 |
| | | upside | 1,35 | 0,88 | 0,78 | 0,73 | 0,73 | 0,74 |
| | | downside | 0,44 | 0,32 | 0,47 | 0,56 | 0,57 | 0,57 |
| `dxy_em` (índice) | 130,21 · `cmb_dollar_index_em` · 23/10 | base | 130,5 | 131,0 | 130,5 | 130,0 | 129,5 | 129,0 |
| | | risk-off | 133,5 | 136,5 | 135,5 | 134,5 | 133,5 | 132,5 |
| | | risk-on | 128,5 | 127,0 | 126,0 | 125,0 | 124,5 | 124,0 |
| `sp500` (pontos) | 7.717 · `cmb_equity_us` · 27/10 | base | 7.750 | 7.900 | 8.050 | 8.200 | 8.350 | 8.500 |
| | | risk-off | 7.000 | 6.500 | 6.700 | 6.950 | 7.200 | 7.450 |
| | | risk-on | 7.950 | 8.300 | 8.650 | 8.950 | 9.200 | 9.450 |
| `icbr_usd` (índice, último mês) | 205,7 · `comm_icbr_usd` · set/26 | base | 206,2 | 202,6 | 201,0 | 199,9 | 199,0 | 198,3 |
| | | alta | 216,3 | 217,1 | 217,1 | 216,8 | 215,7 | 215,3 |
| | | queda | 197,3 | 188,2 | 184,3 | 183,2 | 183,5 | 183,8 |
| `icbr_agr_usd` (índice, média) | 200,5 · `comm_icbr_usd` · 3T26 | base | 203,9 | 200,9 | 199,3 | 198,4 | 197,8 | 197,4 |
| | | alta | 208,1 | 211,1 | 211,9 | 212,8 | 212,4 | 211,7 |
| | | queda | 200,6 | 192,0 | 188,4 | 186,6 | 186,4 | 186,8 |
| `icbr_met_usd` (índice, média) | 330,1 · `comm_icbr_usd` · 3T26 | base | 331,7 | 330,0 | 330,0 | 328,7 | 327,3 | 325,7 |
| | | alta | 346,0 | 358,0 | 362,0 | 362,0 | 362,0 | 362,0 |
| | | queda | 320,0 | 298,3 | 283,3 | 277,0 | 275,0 | 275,0 |
| Brent, média do trimestre (US$/barril; fora do modelo) | 115,22 · `comm_brent` · 20/10 | base | 114,4 | 105,0 | 99,3 | 96,0 | 93,0 | 91,0 |
| | | alta | 129,0 | 130,0 | 124,0 | 118,0 | 113,3 | 110,0 |
| | | queda | 104,1 | 84,3 | 79,0 | 78,0 | 78,0 | 78,0 |

Motivo dos caminhos que não saem direto da história: o `infl_us` sai, por G, de caminhos mensais do núcleo e dos alimentos do CPI e do Brent do cenário, pela regressão trimestral do CPI cheio (0,756 · núcleo + 0,079 · energia + 0,157 · alimentos, 2010–2026) e pela ligação mensal Brent → CPI energia (0,14 no mês e 0,09 no seguinte, 2010–2026); cada cenário do bloco dos EUA usa o Brent do cenário de commodities de mesmo nome. O agro sai, por G, do Brent do cenário (defasagens de 0 a 6 meses) e do dólar EM do base de risco pela ligação mensal de 2016–2026, sem a constante (0,3% ao mês, a tendência da amostra, que um índice no recorde não precisa repetir), mais um componente próprio do cenário: na alta, +4% em rampa até o 3T27, pela demanda e pelos biocombustíveis; na queda, −3%. O `icbr_usd` sai dos três grupos pela combinação estimada (seção 2.3) e é o valor de dezembro, março, junho, setembro. O `ffr` do 4T26 vale para uma alta em 28/10 (4,13) e fica na faixa para uma alta só em 09/12 (4,06).

**Saída do modelo** (informação para os donos, não tese minha; exógenas que não escrevo nos caminhos do P1; faixa do modelo omitida[^faixa])

| Variável | Cenário | 4T26 | 1T27 | 2T27 | 3T27 | 4T27 | 1T28 |
|---|---|---|---|---|---|---|---|
| PTAX (R$/US$, fechamento) | minhas sete no padrão do simulador | 5,36 | 5,36 | 5,34 | 5,31 | 5,31 | 5,34 |
| | base (os três blocos) | 5,43 | 5,51 | 5,52 | 5,51 | 5,54 | 5,58 |
| | EUA upside | 5,41 | 5,48 | 5,48 | 5,47 | 5,50 | 5,54 |
| | EUA downside | 5,44 | 5,53 | 5,54 | 5,53 | 5,56 | 5,62 |
| | risk-off, CDS do fiscal | 5,42 | 5,48 | 5,49 | 5,48 | 5,51 | 5,56 |
| | risk-off, CDS do fiscal + componente global | 5,58 | 5,79 | 5,76 | 5,73 | 5,74 | 5,76 |
| | risk-on, CDS do fiscal | 5,38 | 5,42 | 5,43 | 5,42 | 5,47 | 5,52 |
| | risk-on, CDS do fiscal + componente global | 5,29 | 5,23 | 5,22 | 5,18 | 5,22 | 5,26 |
| | commodities em alta | 5,37 | 5,43 | 5,43 | 5,42 | 5,46 | 5,50 |
| | commodities em queda | 5,48 | 5,60 | 5,62 | 5,60 | 5,62 | 5,66 |
| | conjunto adverso (EUA up, risk-off, commodities em queda; CDS do fiscal) | 5,45 | 5,54 | 5,55 | 5,53 | 5,55 | 5,59 |
| | conjunto petróleo (EUA up, risk-off, commodities em alta; CDS do fiscal) | 5,34 | 5,38 | 5,37 | 5,36 | 5,39 | 5,43 |
| | base com o salto mecânico do real no dólar EM (+0,47%) | 5,45 | 5,53 | 5,54 | 5,53 | 5,56 | 5,61 |
| IPCA 12 meses (%) | base | 5,34 | 4,95 | 4,46 | 4,48 | 4,32 | 4,15 |
| | commodities em alta | 5,39 | 5,09 | 4,67 | 4,76 | 4,60 | 4,37 |
| | commodities em queda | 5,30 | 4,81 | 4,22 | 4,15 | 3,96 | 3,82 |
| | risk-off, CDS do fiscal + componente global | 5,35 | 4,99 | 4,53 | 4,58 | 4,43 | 4,24 |
| Selic, média do trimestre (% a.a.) | base | 13,46 | 13,22 | 12,84 | 12,49 | 12,23 | 11,98 |
| | commodities em alta | 13,46 | 13,23 | 12,87 | 12,55 | 12,31 | 12,10 |
| | commodities em queda | 13,46 | 13,21 | 12,81 | 12,44 | 12,13 | 11,85 |

(`modelo.rodar`, retrato do ciclo, por G; os blocos não citados no cenário ficam no base; o CDS com o componente global é o do fiscal mais a diferença entre o componente global do cenário e o do base, 175 p.b. no 4T26 e 204 no 1T27 no risk-off, 119 e 98 no risk-on, ilustração e não caminho de referência: seção 4.) Três leituras para os donos. No bloco dos EUA, o modelo dá o sinal contrário ao intuitivo: o cenário de Fed mais alto aprecia o real, porque a inflação americana entra com coeficiente 1 no desconto de PPC e pesa mais que o carry (seção 6). No conjunto "petróleo", o mais provável dos conjuntos adversos dado o que Hormuz faz com o Brent, o real fica mais forte que no base porque o IC-Br sobe; se isso vale para uma alta puxada pela energia é pergunta ao câmbio (tempero i, abaixo). E o risk-off só deprecia o real se o CDS andar: com o CDS do fiscal parado, o modelo põe a PTAX do 1T27 abaixo da do base.

### 3.2 Etapa 2 — o tempero qualitativo

**(i) `sp500` — efeito possivelmente mais fraco que o estimado no cenário base** · cenário base
- O multiplicador é do câmbio, dono da (F); argumento na seção 4.
- Coeficiente: `F.b_sp500` estimado 1,888 por desvio-padrão (8,4% de variação), intervalo de 90% do posterior de 0,980 a 2,787.
- Efeito: no meu base o S&P sobe ~11% em seis trimestres e responde por +0,13 na PTAX do 1T28 (decomposição por G), o maior canal externo.
- Por quê: o coeficiente mede o S&P com CDS e dólar EM parados; no base, o S&P sobe por lucro, com o dólar EM caindo de 2027 em diante e um CDS que, pelo componente global, comprimiria. Se o fiscal não carregar essa compressão, a (F) lê uma alta de bolsa como saída de capital do Brasil, o que não é a história do cenário. Dentro do intervalo, um multiplicador abaixo de 1 é defensável só se o CDS ficar parado.
- Onde entra: assimetria do câmbio (decisão do câmbio).

**(i) `icbr_usd` — efeito possivelmente mais fraco quando a alta é de energia** · cenário de commodities em alta e conjunto petróleo
- O multiplicador é do câmbio; argumento na seção 4.
- Coeficiente: `F.b_icbr_usd` estimado −1,720 por desvio-padrão (7,5%), intervalo de 90% de −2,504 a −0,954.
- Efeito: no conjunto petróleo, a alta do IC-Br leva a PTAX do 1T28 de 5,59 (conjunto adverso, commodities em queda) a 5,43.
- Por quê: o coeficiente é estimado numa amostra em que o agro pesa ~0,63 do índice; uma alta puxada pela energia, que o Brasil também importa em derivados, melhora menos os termos de troca. É hipótese, não medida: o banco do meu F não separa termos de troca por grupo, e o câmbio tem os dados (`cmb_termos_troca`, `cmb_comex_*`).
- Onde entra: limite da cauda de apreciação no cenário de commodities em alta (decisão do câmbio).

**(i) `dxy_em` — efeito possivelmente superestimado, porque o índice contém o real** · todos os cenários
- O multiplicador é do câmbio; argumento na seção 4.
- Coeficiente: `F.b_dxy_em` estimado 2,262 por desvio-padrão (3,4 pontos do índice), intervalo de 90% de 1,138 a 3,315.
- Efeito: no base, o dólar EM responde por +0,04 na PTAX do 4T26; num risk-off de +5% no índice, por bem mais.
- Por quê: o real tem coeficiente de ~0,07 no índice (2.2), e a (F) foi estimada com o índice publicado, de modo que uma parte dos movimentos próprios do real foi lida como dólar global. Neste ciclo eu tiro o salto do real do caminho, então o coeficiente se aplica só ao global, como deve; o viés que resta é o da estimação, que não sei medir sem o índice sem o real (seção 6). Não peço multiplicador abaixo de 1; peço que o câmbio diga se lê o coeficiente como teto.
- Onde entra: assimetria do câmbio (decisão do câmbio).

**(ii) Ponta longa americana e prêmio de prazo — Treasury de 10 anos** · todos os cenários
- Hoje: 5,00% (`us_interest_rate`, 23/10); juro real ex-ante 2,27% no ponto, 2,45% na média de outubro.
- Por que o modelo não vê: nenhum juro longo americano está no modelo; chega pelo `rr_10a`, do fiscal.
- Efeito: pressão de alta em `rr_10a`, pequena pelo histórico trimestral (seção 4, como subordinado).
- Onde entra: argumento ao fiscal; não muda meus caminhos.

**(ii) Componente global do CDS** · bloco de risco
- Hoje: CDS 137 p.b. (`cmb_risco_pais`, 26/10, dado do fiscal); de 30/09 a 23/10, −12 p.b. contra +8 p.b. que o dólar EM e o S&P explicariam, e +18 p.b. no pregão de 26/10, que é doméstico (por G; seção 4).
- Por que o modelo não vê: o CDS é exógena do fiscal; os meus cenários de risco não o movem.
- Efeito: risk-off sem o componente global aprecia o real no modelo; com ele, a PTAX do 1T27 vai de 5,48 a 5,79.
- Onde entra: argumento ao fiscal (XS5) e ao câmbio; probabilidade do risk-off.

**(ii) Energia e combustíveis — Brent** · bloco de commodities
- Hoje: 115,22 (`comm_brent`, 20/10); média de outubro 125,0 até 20/10; fluxo por Hormuz interrompido em 11/10 (Al Jazeera · 14/10 · nível B).
- Por que o modelo não vê: a (I) não tem energia; o Brent chega a combustíveis e monitorados fora do modelo.
- Efeito: caminhos do Brent na tabela da seção 3.1, o único caminho de petróleo do ciclo; acima da premissa do Copom (~84 no 2T27) em todo o horizonte do base.
- Onde entra: tempero da inflação (decisão dela) e receita de royalties (fiscal).

**(ii) Demanda chinesa — sem dado** · bloco de commodities
- Hoje: só preço (metais 335,1, `comm_icbr_usd`, set/26), exportação para a China (dado do câmbio) e o minério na mínima de dois anos (Yahoo Finance/Bloomberg · 27/10 · nível C).
- Por que o modelo não vê: não há variável da China, nem dado no banco.
- Efeito: é o motor do cenário de metais em alta ou em queda; com a notícia de nível C, a cauda de baixa dos metais ganha 10 p.p.
- Onde entra: probabilidade da linha dos metais.

**(ii) Ciclo dos pares** · bloco de risco
- Hoje: Colômbia subindo (12,25%), México parado em 6,50% depois de cortar 1,00 p.p. em 12 meses (`inter_interest_rate`, 20/10); peso mexicano com desmontagem de carry (Investing.com México · 22/10 · nível B).
- Por que o modelo não vê: carry relativo aos pares não está na (F).
- Efeito: sem direção clara neste ciclo; o Brasil segue com o maior juro real do grupo.
- Onde entra: argumento à política monetária e ao câmbio.

### 3.3 Da etapa 1 à tese

A central de cada linha é o caminho base; não há modelo entre o caminho e a tese, porque nenhuma equação produz as minhas variáveis. A faixa sai da distância até o caminho de cauda do bloco (com o mínimo dito na seção 1), e as probabilidades são as dos cenários do bloco: 55/30/15 no bloco dos EUA (upside com o dobro do downside porque os T-bills precificam uma alta a mais que o meu base e o downside pede que o Fed não faça a alta que projetou), 55/25/20 no de risco (risk-off maior pelo preço alto do S&P com juro real alto; no dólar EM, 55/28/17 pelo salto mecânico do real) e 55/25/20 no de commodities (alta maior porque Hormuz segue aberto; nos metais, 50/20/30 pela China). Os temperos do tipo (i) são decisão do câmbio e não movem nada aqui.

## 4. Para os outros agentes

**Respostas às entradas fixas (Parte 4 do mapa)**
- XE1 (câmbio): os sete caminhos estão na seção 3.1, com as probabilidades por bloco. Mudaram contra a rodada 1 o agro e o IC-Br total (agro de 202 parado para 204 → 197; IC-Br de 204,8 → 201,4 para 206,2 → 198,3) e as probabilidades dos três blocos. No meu base, o S&P subindo segue o maior canal externo na PTAX (+0,13 no 1T28), seguido do `infl_us` abaixo do padrão (+0,08) e do IC-Br em queda (+0,05).
- XE2 (câmbio), **em destaque**: o Brent está 89,8% acima de um ano antes e oscilou entre 114 e 136 desde 15/09 (`comm_brent` · 20/10, por G), com o fluxo por Hormuz interrompido (Al Jazeera · 14/10 · nível B); o dólar subiu contra desenvolvidos e emergentes (DXY +1,2% e dólar EM +1,6% no mês) com o S&P perto da máxima, e a Colômbia segue subindo juro. O global se move pelo juro americano e por desmontagem de carry (peso mexicano), não por aversão a risco (2.2). De 23/10 a 27/10, nada global: DXY +0,39%, S&P +1,22%.
- XE3 (política monetária), **em destaque**: o Fed subiu 0,25 p.p. em 16/09 e projetou mais uma alta em 2026 (Al Jazeera · 16/09 · nível A); reuniões em 27–28/10 e 08–09/12 (Yahoo Finance · 08/10 · nível B). O meu base tem essa alta no 4T26 e parada até o 1T28; os T-bills precificam duas em 12 meses. Os pares: Colômbia em alta, México, Chile e Peru parados.
- XE4 (inflação), **em destaque**: o agro mudou: 203,9 no 4T26 e 197,4 no 1T28 no base (média do trimestre), contra 202 parado na rodada 1, pela ligação Brent → agro (2.3); metais de 331,7 a 325,7, sem mudança. Caudas: alta a ~212 e 362, queda a ~187 e 275. A cauda de baixa dos metais ganhou 10 p.p. (30%).
- XE5 (inflação), **em destaque**: o Brent fez um salto de 18% num pregão em 02/10 e está em 115,22 (20/10), com média de 125,0 em outubro até 20/10, contra 114,2 em setembro; o evento é o bloqueio em Hormuz, ainda aberto em 19/10 (OilPrice.com · 19/10 · nível B). Caminho do Brent sem mudança (base de 114 no 4T26 a 91 no 1T28; alta de 129–130, agora com 25%; queda a 78, agora com 20%), seção 3.1. A queda desde 02/10 é prêmio saindo do preço com o fluxo ainda interrompido, não reversão do choque (IN-S8). O meu base fica acima da premissa do Copom em todo o horizonte (~84 no 2T27 nela, 99 no meu base).
- XE6 (atividade): demanda externa pelo mercado de trabalho americano (criação fraca, desemprego estável), pelo bloco de risco e pelos metais no alto; a China só pelos preços, pela exportação para lá e pela notícia de nível C sobre o minério, sem dado de atividade. A probabilidade de recessão americana no horizonte que eu atribuo é a do downside do bloco dos EUA, agora 15%, julgamento sem modelo; o banco não tem PIB, produção ou pesquisas dos EUA.
- XE7 (atividade): os três caminhos do IC-Br e o Brent na seção 3.1; o nível de agro e metais perto do recorde sustenta renda agrícola e mineral no base, com o agro cedendo ~3% do 4T26 ao 1T28.
- XE8 (atividade): Fed apertando (seção 2.1) e o S&P perto da máxima com juro real no topo desde 2007; risk-off com 25%.
- XE9 (fiscal), **em destaque**: o dólar EM subiu 1,6% no mês até 23/10, com o peso mexicano puxado por desmontagem de carry; com datas casadas, o CDS caiu 12 p.b. de 30/09 a 23/10 enquanto o componente global pedia +8, e subiu 18 p.b. em 26/10 sem movimento global (seção "Como subordinado").
- XE10 (fiscal), **em destaque**: o Treasury de 10 anos subiu 0,99 p.p. em 12 meses e tocou 5,31% em 05/10, o maior desde 2007; caminho do 10 anos na seção 2.1 (base de 5,05 no 4T26 a 4,75 no 1T28, sem mudança).
- XE11 (fiscal): Brent e IC-Br na seção 3.1; o Brent médio de 114 no 4T26 no base, contra 66,6 em janeiro, é receita de royalties bem acima do início do ano, e o cenário de alta (Brent ~130) ganhou probabilidade (FS-EX3).
- XE12 (expectativas): petróleo e commodities na seção 3.1; inflação americana pelo `infl_us` e pela inflação esperada de 1 ano do Cleveland Fed (2,98%, +0,59 p.p. em 3 meses). Leio o choque de energia como de oferta, com nome (Hormuz) e em devolução gradual no base, com 25% de não se resolver.

**Respostas aos pedidos da rodada 1**
- Câmbio, S8: os caminhos estão na seção 3.1. S9: no fim de semana de 24–25/10 e no pregão de 26/10, nada global no meu F (DXY +0,15%, S&P +0,69% em 26/10) nem nas notícias do ciclo, que tratam desses dias só pela eleição; dos pares, só a notícia do peso mexicano em 22/10 (desmontagem de carry, nível B); o `cmb_fx_latam` termina em 20/10.
- Política monetária, S13: o Fed na seção 2.1 (uma alta a mais no 4T26, parado em 2027, corte no 1T28) e o apetite a risco na seção 2.2 (risk-off com 25%; nada global depois de 26/10).
- Inflação, IN-S7: na seção 3.1. IN-S8: XE5 acima.
- Atividade, S-EXT1: recessão americana em 15% (downside do bloco dos EUA); crescimento da China e dos EUA em 2027 fora do banco, e a única notícia da China é de nível C (minério fraco, usinas insensíveis a estímulo). S-EXT2: Brent na seção 3.1; minério de ferro não está no banco, só o IC-Br metal (331,7 → 325,7 no base, com 30% de cauda de baixa). S-EXT3: Fed na seção 2.1; depois de 26/10, o apetite global não piorou (S&P +1,22% de 23/10 a 27/10).
- Fiscal, FS-EX1: houve movimento de prêmio entre emergentes em outubro, concentrado no peso mexicano (+7,8% no mês até 20/10) e atribuído a carry, petróleo e tecnologia (nível B); o componente global do CDS no mês até 23/10 foi de +21 p.b., e o CDS caiu 2 p.b. (por G): o doméstico foi o lado da compressão. FS-EX2: XE10. FS-EX3: XE11.
- Expectativas, XS10: não há choque externo de alimentos em dólar: o IC-Br agro subiu 0,7% em 12 meses (`comm_icbr_usd` · set/26) e, no base, cede ~3% do 4T26 ao 1T28 com o Brent; está no recorde em nível, e o que encarece o alimento em reais é o câmbio e os in natura, que são do agente de inflação.

**Pedidos (saídas fixas da Parte 3 e deste ciclo)**
- XS1 ao câmbio: quanto o real pesa no dólar EM? A minha regressão diária dá ~0,07, e com ela o salto de 26/10 vale ~0,6% no índice; se o câmbio tiver os pesos da cesta, troco a estimativa. Depende disso a cauda de cima do dólar EM (28%) e a leitura do placar do 4T26.
- XS2 ao câmbio: o fluxo e a posição em BRL depois de 26/10 mostram saída de dinheiro ou só repreço? Depende a probabilidade de o risk-off, se vier, encontrar o real já descoberto.
- XS3 à política monetária: o caminho da Selic até o 1T28 depois de 26/10 e da reunião de 04/11, e se o Copom lê o Fed em alta como restrição. Na rodada 1, a sua central de Selic de fechamento ia de 13,49 no 4T26 a 12,39 no 1T28, contra o `ffr` de 4,13 e 3,88 no meu base.
- XS4 à política monetária: com o Brent no meu base US$ 15 acima da premissa do Copom no 2T27 (por G), o Copom revisa a premissa de petróleo na reunião de 04/11?
- XS5 ao fiscal: o caminho do CDS de 3T27 a 1T28 (135 parado) supõe piora doméstica de ~15 p.b. ou não carrega o componente global do meu base? E a cauda de alta do CDS (25–28%) inclui o meu risk-off? Depende disso o sinal do S&P na (F) e a PTAX do risk-off (seção "Como subordinado").
- XS6 ao fiscal (principal de `rr_10a`): quanto da queda de 0,30 p.p. do `rr_10a` em 2027 vem do Treasury de 10 anos? Pelo meu base, ~0,07 p.p.
- XS7 à inflação: o agro mais baixo em 2027 (−2,1% contra a rodada 1 no 4T27 e −2,3% no 1T28) muda a sua tese de alimentação? E o Brent acima da premissa do Copom entra no tempero de combustíveis com que caminho?
- XS8 às expectativas: a Focus de 30/10 revisa a premissa externa (câmbio, petróleo) depois de 26/10?

**Ao agente web** (marcados "(web)" no Faltou)
- A decisão do FOMC de 28/10/2026 (meta, comunicado, votos) e o que o presidente do Fed disse sobre a reunião de dezembro; e as datas das reuniões do 1T27. Depende disso o `ffr` do 4T26 (4,13 com a alta em 28/10, 4,06 com a alta em 09/12) e a probabilidade do upside (duas altas em 2026).
- O estado do fluxo de petróleo por Hormuz depois de 19/10: ataques, escoltas, negociação ou acordo; e a decisão da OPEP+ de 04/10 numa fonte da lista. Depende disso o caminho base do Brent e as probabilidades de alta (25%) e queda (20%) das commodities.
- O fechamento do peso mexicano, do chileno e do colombiano em 26 e 27/10. Depende disso a leitura de que o dólar EM do 4T26 só sobe pelo real, e não pelos pares.
- Produção de aço e preço do minério de ferro na China em outubro numa fonte nominal (nível A ou B) que confirme ou não a notícia de nível C de 27/10. Depende disso a cauda de baixa dos metais (30%).

**Como subordinado**

- **`rr_10a` · principal: fiscal**
  - Insumos: Treasury de 10 anos em 5,00% (`us_interest_rate` · 23/10), máximo de 5,31% em 05/10, o maior desde 2007; juro real ex-ante de 10 anos de 2,27% no ponto de 23/10 e 2,45% na média de outubro, o maior desde 2007 (`us_interest_rate` e `expc_inflacao`, por G); no 3T26, o juro real americano de 10 anos subiu 0,28 p.p. na média do trimestre e o `rr_10a` 0,18 p.p. (retrato do modelo, por G). O elo trimestral histórico é fraco: Δ`rr_10a` = 0,43 × Δ juro real americano de 10 anos (t 1,8; R² 0,04; 2006–2026), e 0,28 × Δ Treasury de 10 anos (t 1,8; R² 0,04) (por G). A NTN-B de 10 anos subiu 135 p.b. em 26/10 (dado citado pelo fiscal), sem dado do Treasury desse dia no meu F (a curva vai até 23/10).
  - Argumento: o caminho do fiscal (7,70 no 4T26, 7,80 no 1T27 e queda a 7,50 no 1T28) é compatível com o lado externo. A queda de 2027 supõe o juro americano parado, e o meu base tem o 10 anos caindo 0,30 p.p. de 5,05 a 4,75, o que dá ~−0,07 p.p. no `rr_10a`: o externo explica ~23% da queda, o resto é doméstico (por G). No upside do bloco dos EUA (10 anos +0,50 p.p.) o externo põe +0,14 p.p.; no downside (−0,60 p.p.), −0,17 p.p. (por G). O caminho de referência da política monetária (8,05 de 1T27 em diante, +0,55 p.p. acima do fiscal no 1T28) não tem apoio do lado externo: o meu upside dá um quarto disso (por G).
  - Caminho de referência: nenhum.
  - Resposta do principal: a rodada 1 do fiscal foi escrita em paralelo e pedia o caminho do 10 anos (FS-EX2), respondido acima; sem divergência aberta.
- **`fiscal` (CDS 5 anos) · principal: fiscal**
  - Insumos: ΔCDS trimestral = 12,4 p.b. por 1% de dólar EM (t 5,6) − 0,67 p.b. por 1% de S&P (t −0,8), R² 0,56, 2016–2026 (retrato do modelo, por G). **Correção contra a rodada 1**: lá eu comparei o CDS de 26/10 com o dólar EM de 23/10 e escrevi que o movimento recente cabia inteiro no componente global; com as datas casadas, não cabe. De 30/09 a 23/10, o dólar EM subiu 0,64% e o S&P caiu 0,36%, o que pedia +8 p.b., e o CDS caiu 12 p.b. (131 → 119): −20 p.b. domésticos, a maior parte no 1º turno (−12 p.b. de 02/10 a 05/10, com −5 de global; a Agência Brasil registrou a "redução do prêmio de risco dos ativos brasileiros", Agência Brasil · 05/10 · nível A). Em 26/10 o CDS subiu 18 p.b. (119 → 137) com o S&P a +0,69% e o DXY a +0,15%: doméstico, a reeleição (CNN Brasil · 25/10 · nível A). Somados, o doméstico de outubro é quase zero (−20 e +18), e os +6 p.b. desde o fim do 3T26 são o global (`cmb_risco_pais`, `cmb_dollar_index_em`, `cmb_equity_us`, por G). Ressalva que segue: o dólar EM contém o real (2.2), e não há CDS de pares nem spread emergente no banco.
  - Argumento: com o meu base, o componente global do CDS contra o fechamento do 3T26 é de +10 p.b. no 4T26, +13 no 1T27, +7 no 2T27, +1 no 3T27, −5 no 4T27 e −11 no 1T28 (por G). Até o 2T27 o caminho do fiscal (140, 140, 138) deixa o doméstico perto de zero (−1, −5, −1), coerente com o que outubro mostrou. De 3T27 em diante, o caminho parado em 135 deixa o doméstico subindo a +3, +9 e +15 p.b.: ou o fiscal espera piora doméstica em 2027, e deve dizer, ou o caminho não carrega a compressão global do meu base. Na cauda: o meu risk-off soma +45 p.b. no 4T26 e +78 p.b. no 1T27 ao componente global (CDS de ~175 e ~204, acima dos limites do upside do fiscal, 160 e 168); se a cauda de alta do fiscal (25% e 28%) for só doméstica e independente do meu risk-off (25%), a probabilidade de o CDS passar do limite é de ~44% e ~46% (por G), não 25–28%.
  - Caminho de referência: retirado na moderação da rodada 2 (era 140 · 140 · 138 · 132 · 126 · 120). O fiscal mudou o caminho para 140 · 142 · 139 · 135 · 130 · 125, aplicando as duas pernas do componente global com o mesmo desconto, e o upside dele (170 · 205 · 210) já carrega o meu risk-off (PTAX de 5,56 e 5,78 no modelo, contra 5,58 e 5,79 no meu G). Os 2 a 5 p.b. que sobram são o prêmio doméstico da eleição, que é conclusão do principal.
  - Resposta do principal: a rodada 1 do fiscal leu que "o CDS subiu pouco num choque grande e doméstico; a parte global relevante foi a de fim de setembro" (FE-CB1, FE-EX1), o que a conta com datas casadas confirma. Na moderação da rodada 2 ele aceitou a queda global de 2027 e manteve a cauda de alta com o risk-off dentro: divergência fechada.

**Divergências** (sobre as sete variáveis de que sou principal)
- P1: nenhuma divergência listada nas minhas sete exógenas; nenhum subordinado escreveu caminho de referência.
- Câmbio sobre `dxy_em` ("a leitura do índice do 4T26 deve descontar o real: a alta que ele mostrar em 26/10 é mecânica e não é sinal de dólar global"): aceito. O caminho segue o dólar global, sem o salto do real, e a cauda de cima passa de 25% para 28% para o índice publicado carregar o salto (2.2). Medi o tamanho do salto (~0,6% no pregão de 26/10) e quanto ele moveria a PTAX se entrasse no caminho (+0,02 a +0,03).
- Câmbio sobre `icbr_usd` ("o IC-Br de outubro deve vir acima de 205,70 pela energia, então o 4T26 segurado em 205,70 é baixo"): aceito para outubro, que pela minha conta sai perto de 208; mas o `icbr_usd` do 4T26 é o de dezembro, não o de outubro, e em dezembro o Brent do base já devolveu parte do pico. O 4T26 subiu de 204,8 para 206,2, acima de 205,7, pelo agro (que agora carrega o Brent de outubro), e não por mudança no caminho do Brent.
- Inflação sobre `icbr_agr_usd` ("peço ao principal que diga se o Brent alto, fertilizante e diesel, entra no caminho"): aceito, e o caminho mudou. A ligação medida (soma de 0,16 em seis meses, t 2,9) põe o agro em 203,9 no 4T26 e 197,4 no 1T28, em vez de 202 parado: o Brent alto entra, e a devolução dele também. Os in natura e o arroz que a inflação cita não estão na cesta do IC-Br e não mudam o caminho.
- Inflação sobre `icbr_met_usd` ("nada a acrescentar; se o principal subir o caminho, eu leria o efeito do modelo como teto"): mantido o caminho; a mudança é na cauda de baixa (30%), pela China, que vai no sentido do que a inflação lê nos preços de bens industriais.

## 5. Placar

Primeiro ciclo: não há report final anterior deste agente.

## 6. Sobre o modelo

Rodada sem literatura; as propostas vêm dos dados e do mapa. O modelo não muda neste ciclo (decisão do usuário): são só propostas.

| Fonte | O que sugere (regressor, defasagem, quebra, âncora) | Teste proposto (dado, amostra, que resultado mudaria a especificação) | Por que importa para a tese deste ciclo |
|---|---|---|---|
| Dados (`cmb_dollar_index_em`, `cmb_ptax`) e mapa 2.4–2.5 | O dólar EM da (F) contém o real (coeficiente de ~0,07 na regressão diária), então a equação explica o real em parte por ele mesmo | Montar o dólar EM sem o real (pesos da cesta do Fed, que não estão no banco; ou o resíduo da regressão diária do índice no real) e reestimar a (F) com ele, 2006–2026; se `F.b_dxy_em` cair para fora do intervalo atual (abaixo de 1,138), trocar o regressor | Neste ciclo o real saltou 8,8% num pregão por motivo doméstico, e o índice publicado do 4T26 vai carregar ~0,5–0,6% disso; escrevi o caminho sem o salto para não contar o real duas vezes |
| Dados (`inflc_cpi`) e mapa 2.3 | O desconto de PPC da (F) usa o CPI cheio com coeficiente fixo em 1; num choque de energia, a inflação americana sobe por energia e o modelo aprecia o real mecanicamente | Reestimar a (F) com o núcleo do CPI no lugar do cheio, e com o coeficiente livre, 2006–2026; se o coeficiente livre ficar abaixo de 0,5 ou o núcleo ajustar melhor, trocar | No meu bloco dos EUA, o cenário de Fed mais alto aprecia o real (PTAX 5,41 contra 5,43 no 4T26), o sinal oposto ao canal do carry que o mapa espera |
| Dados (`comm_brent`, `comm_icbr_usd`) e mapa 2.6 | Brent ou o IC-Br energia em reais nos monitorados da (I) | Acrescentar Δlog do Brent em reais, corrente e defasado, na equação de monitorados, 2006–2026; se significativo, a energia entra no modelo | O Brent subiu 89,8% em 12 meses e é o maior choque externo do ciclo; hoje ele chega ao IPCA só pelo agro (ligação medida) e pelo tempero da inflação |
| Mapa 2.5 e a decomposição por G | O sinal condicional do S&P na (F): com o CDS parado, uma alta de bolsa deprecia o real | Reestimar a (F) com o S&P em excesso sobre a tendência de lucro (ou com interação S&P × ΔCDS), 2006–2026; se o efeito condicional desaparecer fora dos trimestres de crise, restringir | No meu base, o S&P subindo é o maior canal externo na PTAX (+0,13 no 1T28) |

[^conv]: Cada variável é medida como o modelo a lê: `ffr` é o Fed Funds **efetivo**, a média do último mês do trimestre (não o ponto médio da meta), porque é o juro que o carry da (F) usa; `infl_us` é a variação do CPI cheio no trimestre (100·Δlog de dezembro contra setembro, por exemplo), sem anualizar e sem acumular 12 meses; `dxy_em` e `sp500` são o fechamento; `icbr_usd` é o índice do último mês; `icbr_agr_usd` e `icbr_met_usd` são a média dos três meses. Um 1% de inflação no trimestre equivale a ~4% ao ano.
[^pctl]: Percentil: a posição do último valor no histórico, de 0 (o menor já visto) a 100 (o maior). Percentil 100 em 10 anos quer dizer que é o maior valor da década.
[^tbill]: Os T-bills (títulos curtos do Tesouro americano) rendem a média do juro do Fed esperada até o vencimento mais um prêmio pequeno. Medi o prêmio nos meses em que o Fed não mudou o juro nos 12 meses seguintes; o que sobra acima disso é a alta que o mercado espera. Não há futuros de Fed Funds no banco, que seriam a medida direta.
[^real]: Juro real ex-ante: o juro nominal menos a inflação esperada para o mesmo prazo (aqui, a do Cleveland Fed). Ex-post seria contra a inflação passada. Um juro real de 2,45% em 10 anos é o que um título americano sem risco paga acima da inflação esperada, e é contra isso que ativos emergentes competem.
[^tp]: Prêmio de prazo (term premium): o que o investidor exige a mais para ficar 10 anos num título em vez de rolar o juro curto por 10 anos. Ex.: se o mercado espera o juro curto médio em 4% por 10 anos e o 10 anos paga 4,5%, o prêmio é ~0,5 p.p. O banco não tem uma estimativa dele.
[^gfc]: Ciclo financeiro global: um fator comum que move bolsas, spreads de crédito e fluxos de capital em vários países ao mesmo tempo, e que tem o juro americano entre os seus motores. Quando ele vira, os emergentes perdem capital juntos.
[^em]: Dólar contra emergentes: índice do Fed (FRED) do dólar contra uma cesta de moedas de países emergentes, que inclui o real. Subir quer dizer dólar mais forte: se o peso mexicano, o real e as outras moedas da cesta perdem valor juntos, o índice sobe.
[^peso]: O coeficiente de 0,072 não é o peso oficial do real na cesta, que não está no banco: é quanto o índice anda, em média, quando o real anda 1% e as outras cinco moedas e o DXY ficam paradas. Ex.: com o real 8,8% mais fraco num dia em que o resto parou, o índice sobe ~0,6%. Na amostra de 2016–2026 o coeficiente é 0,069, quase o mesmo.
[^agro]: A ligação diz quanto o agro em dólar se move, em média, nos seis meses depois de um movimento do Brent: 1% a mais no Brent, ~0,16% a mais no agro, quase tudo no mesmo mês. O canal é o custo (fertilizante, diesel, frete) e os biocombustíveis, que puxam milho, cana e soja. Com o Brent caindo de 114 para 91 no base, o agro cede ~3,6% pelo petróleo; o dólar EM parado quase não acrescenta.
[^icbr]: IC-Br: índice de commodities do Banco Central, uma cesta de produtos que o Brasil exporta (agropecuária, metais e energia). Aqui em dólar, sem o efeito do câmbio; em reais, que é como chega ao IPCA, é dado da inflação.
[^ppc]: Desconto de PPC: na equação do câmbio do modelo, a diferença entre a inflação do Brasil e a dos EUA entra com peso 1 na variação do real. Se a inflação americana sobe 0,3 p.p. no trimestre, o modelo deprecia o real 0,3% a menos, sem passar pelo Fed.
[^sp]: Sinal condicional do S&P: na equação do câmbio, com o CDS e o dólar EM parados, uma alta da bolsa americana deprecia o real (capital indo para ações americanas). Sem condicionar, bolsa em alta costuma vir com real forte, porque o risk-on também comprime o CDS e enfraquece o dólar. Por isso o S&P e o dólar EM se escrevem juntos, e o CDS tem de acompanhar.
[^faixa]: A faixa que o simulador imprime é a incerteza dos pesos das equações (90% do posterior), não um intervalo de previsão; por isso fica fora da tabela.
[^proc]: Rodada 2: as exógenas que não escrevo vêm do P1 (meta de 3,00 da política monetária; `rr_10a` de 7,70 a 7,50 e CDS de 140 a 135 do fiscal; volatilidade de 17,0 a 13,5 do câmbio). As notícias são as do agente web para a rodada 1 (`noticias/demanda_r1.md`); nenhuma traz número usado como dado, e a decisão do FOMC de 28/10 não está nelas. O F foi montado sem literatura; o conhecimento lido foi só o mapa conceitual.
