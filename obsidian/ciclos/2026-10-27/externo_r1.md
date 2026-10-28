# Report — externo · ciclo 2026-10-27 · rodada 1

Dados até: 27/10/2026 (F_externo, fixo no ciclo; a data do último dado vai com cada número) · Horizontes: 4T26 a 1T28, cada variável na convenção do Modelo Estrutural (`modelo.CONVENCAO`)[^conv]

## 1. Tese

**A tese em uma frase:** o Fed sobe mais uma vez no 4T26 e para (efetivo de 4,13% de dez/26 a dez/27), uma alta a menos do que os T-bills precificam; a inflação americana desacelera de 1,12% no 3T26 para ~0,6% por trimestre em 2027 conforme o Brent devolve o pico de outubro (média de ~114 no 4T26 para ~91 no 1T28); o dólar contra emergentes fica em 130–131 enquanto o Fed aperta e cede a 129 no 1T28; e as commodities em dólar ficam paradas no alto (IC-Br ~202–205), com metais em ~330 e agro em ~202. No modelo, esse conjunto pesa no real pelos canais da (F) na mesma direção, e o maior risco para o Brasil atravessa blocos: um risk-off em que o CDS carrega o seu componente global.

**Bloco 1 — Política dos EUA** (cenários: base 50%, upside 30%, downside 20%)

| Variável | Trimestre | Central | Base: faixa · P | Upside: limite · P | Downside: limite · P | P(up) − P(down) |
|---|---|---|---|---|---|---|
| `ffr` — Fed Funds efetivo, média do último mês do trimestre (% a.a.) | 4T26 | 4,13 | 4,00 a 4,25 · 50% | acima de 4,25 · 30% | abaixo de 4,00 · 20% | +0,10 |
| | 1T27 | 4,13 | 3,88 a 4,38 · 50% | acima de 4,38 · 30% | abaixo de 3,88 · 20% | +0,10 |
| | 2T27 | 4,13 | 3,75 a 4,38 · 50% | acima de 4,38 · 30% | abaixo de 3,75 · 20% | +0,10 |
| | 3T27 | 4,13 | 3,63 a 4,38 · 50% | acima de 4,38 · 30% | abaixo de 3,63 · 20% | +0,10 |
| | 4T27 | 4,13 | 3,63 a 4,38 · 50% | acima de 4,38 · 30% | abaixo de 3,63 · 20% | +0,10 |
| | 1T28 | 3,88 | 3,50 a 4,25 · 50% | acima de 4,25 · 30% | abaixo de 3,50 · 20% | +0,10 |
| `infl_us` — CPI cheio, variação no trimestre (%, sem anualizar) | 4T26 | 0,86 | 0,65 a 1,10 · 50% | acima de 1,10 · 30% | abaixo de 0,65 · 20% | +0,10 |
| | 1T27 | 0,61 | 0,46 a 0,76 · 50% | acima de 0,76 · 30% | abaixo de 0,46 · 20% | +0,10 |
| | 2T27 | 0,61 | 0,46 a 0,76 · 45% | acima de 0,76 · 30% | abaixo de 0,46 · 25% | +0,05 |
| | 3T27 | 0,65 | 0,50 a 0,80 · 45% | acima de 0,80 · 30% | abaixo de 0,50 · 25% | +0,05 |
| | 4T27 | 0,63 | 0,48 a 0,78 · 45% | acima de 0,78 · 30% | abaixo de 0,48 · 25% | +0,05 |
| | 1T28 | 0,65 | 0,50 a 0,80 · 45% | acima de 0,80 · 30% | abaixo de 0,50 · 25% | +0,05 |

**Bloco 2 — Risco e dólar** (cenários: base 55%, risk-off 25%, risk-on 20%; o risk-off é o upside do dólar EM e o downside do S&P)

| Variável | Trimestre | Central | Base: faixa · P | Upside: limite · P | Downside: limite · P | P(up) − P(down) |
|---|---|---|---|---|---|---|
| `dxy_em` — dólar contra emergentes, fechamento (índice) | 4T26 | 130,5 | 129,2 a 132,0 · 55% | acima de 132,0 · 25% | abaixo de 129,2 · 20% | +0,05 |
| | 1T27 | 131,0 | 129,0 a 133,8 · 55% | acima de 133,8 · 25% | abaixo de 129,0 · 20% | +0,05 |
| | 2T27 | 130,5 | 128,2 a 133,0 · 55% | acima de 133,0 · 25% | abaixo de 128,2 · 20% | +0,05 |
| | 3T27 | 130,0 | 127,5 a 132,2 · 55% | acima de 132,2 · 25% | abaixo de 127,5 · 20% | +0,05 |
| | 4T27 | 129,5 | 127,0 a 131,5 · 55% | acima de 131,5 · 25% | abaixo de 127,0 · 20% | +0,05 |
| | 1T28 | 129,0 | 126,5 a 130,8 · 55% | acima de 130,8 · 25% | abaixo de 126,5 · 20% | +0,05 |
| `sp500` — S&P 500, fechamento (pontos) | 4T26 | 7.750 | 7.375 a 7.982 · 55% | acima de 7.982 · 20% | abaixo de 7.375 · 25% | −0,05 |
| | 1T27 | 7.900 | 7.200 a 8.137 · 55% | acima de 8.137 · 20% | abaixo de 7.200 · 25% | −0,05 |
| | 2T27 | 8.050 | 7.375 a 8.350 · 55% | acima de 8.350 · 20% | abaixo de 7.375 · 25% | −0,05 |
| | 3T27 | 8.200 | 7.575 a 8.575 · 55% | acima de 8.575 · 20% | abaixo de 7.575 · 25% | −0,05 |
| | 4T27 | 8.350 | 7.775 a 8.775 · 55% | acima de 8.775 · 20% | abaixo de 7.775 · 25% | −0,05 |
| | 1T28 | 8.500 | 7.975 a 8.975 · 55% | acima de 8.975 · 20% | abaixo de 7.975 · 25% | −0,05 |

**Bloco 3 — Commodities** (cenários: base 55%, alta 20%, queda ampla 25%)

| Variável | Trimestre | Central | Base: faixa · P | Upside: limite · P | Downside: limite · P | P(up) − P(down) |
|---|---|---|---|---|---|---|
| `icbr_usd` — IC-Br em dólar, último mês do trimestre (índice) | 4T26 | 204,8 | 199,7 a 209,9 · 55% | acima de 209,9 · 20% | abaixo de 199,7 · 25% | −0,05 |
| | 1T27 | 203,7 | 195,8 a 210,6 · 55% | acima de 210,6 · 20% | abaixo de 195,8 · 25% | −0,05 |
| | 2T27 | 202,9 | 193,4 a 210,9 · 55% | acima de 210,9 · 20% | abaixo de 193,4 · 25% | −0,05 |
| | 3T27 | 202,3 | 192,4 a 210,2 · 55% | acima de 210,2 · 20% | abaixo de 192,4 · 25% | −0,05 |
| | 4T27 | 201,8 | 192,2 a 209,7 · 55% | acima de 209,7 · 20% | abaixo de 192,2 · 25% | −0,05 |
| | 1T28 | 201,4 | 192,1 a 209,4 · 55% | acima de 209,4 · 20% | abaixo de 192,1 · 25% | −0,05 |
| `icbr_agr_usd` — IC-Br agropecuária, média do trimestre (índice) | 4T26 | 202,0 | 198,0 a 206,0 · 55% | acima de 206,0 · 20% | abaixo de 198,0 · 25% | −0,05 |
| | 1T27 | 202,0 | 197,0 a 206,3 · 55% | acima de 206,3 · 20% | abaixo de 197,0 · 25% | −0,05 |
| | 2T27 | 202,0 | 195,0 a 208,0 · 55% | acima de 208,0 · 20% | abaixo de 195,0 · 25% | −0,05 |
| | 3T27 | 202,0 | 193,8 a 208,5 · 55% | acima de 208,5 · 20% | abaixo de 193,8 · 25% | −0,05 |
| | 4T27 | 202,0 | 193,5 a 208,5 · 55% | acima de 208,5 · 20% | abaixo de 193,5 · 25% | −0,05 |
| | 1T28 | 202,0 | 193,5 a 208,5 · 55% | acima de 208,5 · 20% | abaixo de 193,5 · 25% | −0,05 |
| `icbr_met_usd` — IC-Br metal, média do trimestre (índice) | 4T26 | 331,7 | 321,7 a 341,7 · 55% | acima de 341,7 · 20% | abaixo de 321,7 · 25% | −0,05 |
| | 1T27 | 330,0 | 314,1 a 344,0 · 55% | acima de 344,0 · 20% | abaixo de 314,1 · 25% | −0,05 |
| | 2T27 | 330,0 | 306,6 a 346,0 · 55% | acima de 346,0 · 20% | abaixo de 306,6 · 25% | −0,05 |
| | 3T27 | 328,7 | 302,9 a 345,4 · 55% | acima de 345,4 · 20% | abaixo de 302,9 · 25% | −0,05 |
| | 4T27 | 327,3 | 301,1 a 344,6 · 55% | acima de 344,6 · 20% | abaixo de 301,1 · 25% | −0,05 |
| | 1T28 | 325,7 | 300,4 a 343,9 · 55% | acima de 343,9 · 20% | abaixo de 300,4 · 25% | −0,05 |

A faixa base de cada linha vai até a metade da distância entre o caminho base e o caminho do cenário de cauda, com uma meia-largura mínima (0,12 p.p. no `ffr`, 0,15 p.p. no `infl_us`, 1% no dólar EM, 3% no S&P, 2,5% no IC-Br, 2% no agro, 3% nos metais). No `infl_us` de 2T27 em diante a probabilidade da faixa cai para 45%: ali os cenários convergem e o ruído trimestral do CPI (desvio-padrão de 0,30 p.p. entre 1T23 e 3T26, `inflc_cpi`) pesa mais que a distância entre eles.

**O que leva a cada cauda**

- **Política dos EUA, upside** (Fed acima de 4,25 no 4T26; inflação acima da faixa): o Brent fica em 125–132 até o 1T27 e o núcleo do CPI mantém o ritmo de setembro (0,33% ao mês); o Fed sobe duas vezes até dezembro e chega a 4,63 no 2T27, o caminho que os T-bills já precificam. No modelo a PTAX fica **abaixo** da base (5,27 contra 5,29 no 4T26), porque a inflação americana maior pesa mais pelo desconto de PPC[^ppc] do que a perda de carry: bom para o real dentro do modelo, ruim fora dele, pelo aperto das condições financeiras globais.
- **Política dos EUA, downside** (Fed abaixo da faixa; inflação abaixo): o Brent volta a ~80 no 1T27, o mercado de trabalho cede e o Fed não só para como devolve a alta de setembro e corta até 3,13 no 3T27; a inflação cai a 0,3–0,5% por trimestre. No modelo a PTAX fica **acima** da base (5,53 contra 5,50 no 1T28): a inflação americana menor pesa mais que o carry maior.
- **Risco e dólar, risk-off** (dólar EM acima da faixa, S&P abaixo): o S&P cai ~16% até o 1T27 (6.500, contra 7.717 em 27/10) e o dólar EM sobe a 136,5 (+5%). Ruim para o Brasil, mas só aparece no modelo se o CDS subir junto: com o CDS carregando o componente global medido por G, a PTAX vai a 5,71 no 1T27; com o CDS parado no padrão, o modelo **aprecia** o real (5,35), porque o S&P em queda, sozinho, aprecia o real na (F).
- **Risco e dólar, risk-on** (dólar EM abaixo, S&P acima): dólar EM a 124 e S&P a 9.450 no 1T28. Bom para o real: PTAX de 5,12–5,20 em todo o horizonte com o CDS global, 5,25–5,45 com o CDS parado.
- **Commodities, alta**: Brent de 129–130 no 4T26–1T27, metais a 362 (+10% contra a média do 3T26), agro a 215 (+7%). Bom pelo câmbio (PTAX 5,24 no 4T26 e 5,42 no 1T28, contra 5,29 e 5,50) e ruim pela inflação (IPCA 12m de 4,63% no 2T27, contra 4,42%).
- **Commodities, queda ampla**: Brent a 78, metais a 275 (−17%), agro a 185 (−8%) até o fim de 2027. Ruim pelo câmbio (PTAX 5,60 no 1T28) e bom pela inflação (IPCA 12m de 3,79% no 1T28, contra 4,18%). No modelo, pelos números acima, o canal do câmbio e o da inflação têm tamanhos comparáveis; qual domina na Selic é leitura da política monetária.

## 2. Argumentação

### 2.1 Política dos EUA (Q1)

**O Fed voltou a subir porque a inflação acelerou e a expectativa desancorou na margem, e não por um mercado de trabalho apertado.** A meta subiu 0,25 p.p. em 17/09/2026, para 3,75–4,00% (ponto médio 3,875; `us_interest_rate`, curva POLICY), depois de três cortes de 0,25 p.p. em 18/09, 30/10 e 11/12/2025 (mesma tabela, por G). O que sustenta a leitura de que o gatilho foi inflação:

| Medida | Último | Leitura |
|---|---|---|
| CPI cheio, 12 meses | 3,72% (`inflc_cpi` · set/26) | 3m anualizado 4,56% |
| CPI núcleo, 3m anualizado | 3,41% (`inflc_cpi` · set/26) | 12 meses 2,57% |
| CPI serviços sem energia, 3m anualizado | 3,76% (`inflc_cpi` · set/26) | 12 meses 3,16% |
| CPI energia, 12 meses | +20,4% (`inflc_cpi` · set/26) | +5,2% só em setembro |
| PCE núcleo, 12 meses | 3,01% (`inflc_pce` · ago/26) | 3m anualizado 2,05% |
| Inflação esperada 1 ano (Cleveland Fed) | 2,98% (`expc_inflacao` · out/26) | +0,59 p.p. em 3 meses |
| Inflação esperada 10 anos | 2,73% (`expc_inflacao` · out/26) | percentil 100 em 10 anos[^pctl] |

O núcleo do CPI acelerou três meses seguidos (0,22%, 0,29% e 0,33% em jul, ago e set; `inflc_cpi`, por G), o que mostra que o choque de energia começa a passar para o resto da cesta; e a inflação esperada subiu em todos os prazos, com a de 10 anos no maior nível da década. Um Fed que sobe com a inflação esperada de longo prazo no topo de dez anos está reagindo à âncora. **Mas** a medida que o Fed persegue é mais calma: o PCE núcleo subiu só 0,13% em junho e em julho e 0,25% em agosto (`inflc_pce`, por G), 2,05% anualizado em três meses. Se o PCE núcleo de setembro vier abaixo de 0,25%, o argumento para uma segunda alta enfraquece; acima de 0,30%, ele passa a ser o cenário base.

**O mercado de trabalho não pede aperto, mas também não força corte.** A criação de vagas é fraca: +29 mil em setembro (preliminar), média de 51 mil em 3 meses e de 41 mil em 12 meses (`mt_ces`, por G). Contratações e pedidos de demissão estão nos percentis 16 e 10 dos últimos dez anos (3,3% e 1,9%; `mt_jolts` · ago/26), um mercado de pouca rotatividade, e o salário por hora sobe 3,0% em 12 meses (`mt_ces` · set/26), o que afasta uma espiral salário-preço. **Mas** o desemprego não sobe: 4,2% (`mt_cps` · set/26), 0,2 p.p. abaixo de um ano antes, com a participação subindo 0,3 p.p. em 3 meses. Vagas fracas com desemprego estável dizem que pouca criação já basta para absorver a força de trabalho, e é isso que deixa o Fed livre para subir. O downside (o Fed devolve a alta) precisa do desemprego subindo: acima de 4,5% por dois meses, ele ganha probabilidade.

**Onde o meu caminho difere do mercado.** Os T-bills de 23/10 estão todos acima da meta (tabela). Descontado o prêmio que eles carregam em meses de Fed parado (de −0,03 a +0,05 p.p. no de 3 meses, +0,03 a +0,08 no de 6 meses, +0,09 a +0,10 no de 1 ano; `us_interest_rate` e `diferenciais_juros`, por G[^tbill]), eles precificam um efetivo médio de 4,17–4,25% nos próximos três meses e de 4,41–4,48% entre seis e doze meses, contra 3,88% hoje: perto de uma alta imediata e de duas em doze meses. O meu base tem uma. A diferença, ~0,3 p.p. em 2027, é a razão de o upside do bloco ter 30% e o downside 20%.

| Vértice (23/10/2026) | Taxa | Menos a meta (p.p.) |
|---|---|---|
| Treasury 3 meses | 4,22 | +0,34 |
| Treasury 6 meses | 4,30 | +0,42 |
| Treasury 1 ano | 4,44 | +0,57 |
| Treasury 2 anos | 4,69 | +0,82 |

(`us_interest_rate`, leitura combinada do F)

**A ponta longa sobe com a curta, não por prêmio.** O Treasury de 10 anos está em 5,00% (`us_interest_rate` · 23/10), +0,99 p.p. em 12 meses, depois de tocar 5,31% em 05/10, o maior nível desde 2007 (por G). O juro real ex-ante[^real] de 10 anos é 2,27% no ponto de 23/10 (5,00 − 2,73, leitura combinada do F) e 2,45% na média de outubro (por G), também o maior desde 2007. Em três meses, o de 2 anos subiu 0,32 p.p. e o de 10 anos 0,29 p.p., e a inclinação 30 anos − 10 anos caiu de +0,46 para +0,33 p.p. (`us_interest_rate`): o longo andou com a expectativa de juro, não com um prêmio de prazo[^tp] crescente na ponta, o que põe o movimento no bloco do Fed e da inflação. Desde 02/10 (data do ciclo anterior do F), o 10 anos caiu 0,28 p.p. e o 2 anos 0,14 p.p., junto com o Brent (−15% no período, `comm_brent`): a ponta longa está negociando petróleo. **Mas** o banco não tem estimativa de prêmio de prazo nem futuros de Fed Funds; a separação acima é por inclinações, e uma queda de 0,17 p.p. do 10 anos num único pregão (21/10 → 22/10, por G) não tem explicação no F (pedido ao agente web, seção 4).

**Caminho do Treasury de 10 anos** (média do trimestre, % a.a.; não é variável do modelo, vai ao fiscal pelo XE10, juízo meu sobre os cenários do bloco): base 5,05 · 4,95 · 4,90 · 4,85 · 4,80 · 4,75 (4T26 a 1T28); upside 5,40 · 5,55 · 5,50 · 5,45 · 5,40 · 5,35; downside 4,70 · 4,45 · 4,35 · 4,30 · 4,30 · 4,30.

**A inflação americana do modelo.** O `infl_us` do 3T26 foi 1,12% (leitura combinada do F), com o núcleo em 0,84% e a energia em +5,65% no trimestre (`inflc_cpi`, por G), contra uma média de 0,45% em 2015–2019 e 0,79% de 1T23 a 3T26 (por G). O caminho base sai de um núcleo de 0,27% ao mês no 4T26, cedendo a 0,24%, e do Brent base (seção 2.3), pela regressão trimestral do CPI cheio no núcleo, na energia e nos alimentos (2010–2026, por G): 0,86% no 4T26, porque o Brent médio de outubro (125,0 até 20/10, `comm_brent`) ainda chega à energia de outubro e novembro, e 0,61–0,65% de 2027 em diante. É abaixo do padrão do simulador (0,91%, a média dos últimos quatro trimestres), e isso tem efeito no câmbio do modelo (2.4).

### 2.2 Risco e dólar (Q2)

**O ciclo financeiro global[^gfc] virou contra os emergentes na margem, pelo juro americano, e não por aversão a risco.** O dólar contra emergentes[^em] subiu de 126,1 em 09/09 (a mínima de 2026) para 130,2 em 23/10 (`cmb_dollar_index_em`, por G), +1,6% no último mês; o DXY foi de 99,7 em 01/09 para 102,2 em 27/10 (`cmb_dollar_index`, por G). O dólar subiu contra desenvolvidos e emergentes ao mesmo tempo, na janela da alta do Fed e do salto do Brent. Que o motor é juro, e não pânico, mostra o S&P: 7.717 em 27/10 (`cmb_equity_us`), a 1,3% da máxima histórica de 7.819 de 06/10 (por G), +4,1% em 3 meses. Na correlação dos retornos diários (leitura combinada do F), o dólar EM anda mais com o DXY (+0,59 em 3 meses) do que contra o S&P (−0,43 em 3 meses, contra −0,49 em 12 meses): o fator dólar global está mais forte que o fator risco.

As moedas latinas, dado do câmbio lido como consulta, enfraqueceram todas no mês (`cmb_fx_latam` · 20/10): peso mexicano +7,8%, peso chileno +2,8%, peso colombiano +2,3%, sol +2,5%. O movimento é amplo; o do peso mexicano é grande demais para ser só global, e se o dólar EM subiu puxado pelo México, parte do meu cenário de dólar está superestimada (pergunta ao câmbio, XS1, e ao agente web). Se o real acompanhou ou se descolou é do câmbio (aguarda câmbio, XS1). No QPC de 23/09, 67% dos respondentes viam o ambiente externo menos favorável, contra 62% em agosto (`expc_qpc`, dado de expectativas, lido como consulta).

**Os pares não andam juntos.** México em 6,50% (−1,00 p.p. em 12 meses), Chile em 4,50%, Peru em 4,25%, todos parados no último mês; a Colômbia subiu 0,25 p.p. no mês e 3,00 p.p. em 12 meses, para 12,25% (`inter_interest_rate` · 20/10). Nos juros reais ex-post de agosto (`cmb_real_rates`), o Brasil tem o maior (9,78%), à frente de Colômbia (5,76%), México (3,24%), Chile (0,37%) e Peru (−0,19%). **Mas** o ex-post subestima o aperto de quem está desinflando e superestima o de quem tem inflação subindo (Colômbia, 6,24% em 12 meses), então a comparação é de ordem, não de distância.

**Por que o dólar EM fica alto, e não sobe mais, no base.** Não há regularidade estável de o dólar EM subir quando o Fed sobe: nos 11 trimestres de alta do efetivo de 2007 a 2026, o dólar EM subiu em média 0,25%, contra 0,19% nos 55 trimestres de Fed parado (`diferenciais_juros` e `cmb_dollar_index_em`, por G). O que move o dólar EM de verdade é aversão a risco: nos 9 trimestres em que o S&P caiu 8% ou mais (2007–2026), o dólar EM subiu 4,1% em média (por G), e a correlação trimestral entre os dois é −0,62. Por isso o base tem o dólar EM em 130,5–131 enquanto o Fed sobe (uma alta só, já na metade precificada) e cedendo a 129 no 1T28, quando o Brent já caiu e o Fed começa a cortar; e o S&P subindo ~2% por trimestre, abaixo da mediana histórica de 3,8% por trimestre (por G), porque o juro real de 10 anos está no maior nível desde 2007 e o Fed está apertando.

**Por que o risk-off tem mais probabilidade que o risk-on (25% contra 20%).** O S&P está no percentil 99 de dez anos (F) com o juro real americano no topo de quase duas décadas; uma correção não precisa de recessão, só de mais uma alta do Fed. **Mas** o banco não tem medida de valuation, VIX nem spread de crédito emergente: o argumento é a combinação de preço alto com juro real alto, não um indicador de estresse. Se o S&P fechar abaixo de 7.375 com o dólar EM acima de 132, o risk-off passa a ser o cenário corrente.

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

**Energia: o padrão é de choque de oferta, e o base é a devolução gradual.** O Brent fez em 2026 dois picos e uma volta: 66,6 de média em janeiro, 117,3 em abril (máxima diária de 138,21 em 07/04), 83,8 em julho, 114,2 em setembro (`comm_brent`, por G). Em 02/10 ele saltou de 114,82 para 135,51 num pregão e desde 16/10 recua, a 115,22 em 20/10. Saltos de 18% num dia e devoluções em semanas são assinatura de evento de oferta, mas o banco não diz qual; o base supõe que ele se resolve devagar (Brent médio de 114 no 4T26, 105 no 1T27, 91 no 1T28), sem voltar aos 84 de julho no horizonte, e é a premissa mais frágil deste report (pedido ao agente web, seção 4). O IC-Br energia segue o Brent com elasticidade de 0,48 no mês (2010–2026, R² 0,59, por G).

**Metais: estáveis no topo, com o dólar contra.** O IC-Br metal está em 335,1 (`comm_icbr_usd` · set/26), abaixo do pico de 350,9 de maio e de lado desde o 1T26 (médias trimestrais de 328,8, 339,4 e 330,1; por G). O motor histórico é a demanda chinesa, e o banco não tem dado da China: a exportação brasileira para a China somou US$ 109,0 bi em 12 meses, contra US$ 93,5 bi um ano antes (`cmb_comex_pais` · set/26, dado do câmbio lido como consulta), o que é coerente com preço alto, mas mistura preço e volume e não separa demanda de oferta. O dólar é um vento contra só neste grupo: a correlação mensal dos metais com o dólar EM é −0,45 em 24 meses e −0,55 em 60 meses, enquanto a do índice total caiu a −0,04 em 24 meses (contra −0,44 de 2010 a 2026; `comm_icbr_usd` e `cmb_dollar_index_em`, por G). "Commodities caem quando o dólar sobe" vale hoje para metais e não para o índice. Com o dólar EM alto no base, os metais derivam de 331,7 no 4T26 para 325,7 no 1T28.

**Agro: no recorde e sem sinal de direção.** O IC-Br agropecuária está em 201,8 (`comm_icbr_usd` · set/26), a 1% do recorde de 203,9 de jan/25 (por G), com +0,7% em 12 meses e correlação com o dólar EM de +0,13 em 24 meses (por G). Sem dado de safra, clima ou estoques, o base é parado em 202. **Mas** o petróleo caro encarece fertilizante e frete e puxa os biocombustíveis; se o Brent ficar acima de 125 (o upside), o agro sobe junto, e por isso o cenário de alta tem os três grupos subindo.

**Consistência das convenções.** O total do trimestre é o último mês e os grupos são média: no base, o total do 4T26 (dezembro, 204,8) já carrega a queda do Brent de outubro para dezembro, enquanto a média da energia no trimestre (96,1) ainda carrega o pico de outubro.

### 2.4 Como chega ao Brasil (Q4)

Pelos números do modelo com os meus caminhos base e as outras exógenas no padrão do simulador[^proc], a PTAX vai a 5,29 no 4T26 e 5,50 no 1T28, contra 5,21 e 5,28 do padrão; o IPCA 12m sobe pouco (4,18% contra 4,08% no 1T28) e a Selic quase não muda. A decomposição tira uma exógena de cada vez do base (por G):

| Linha do mapa (2.8) | Moveu? | Sinal para o Brasil, no modelo | Quanto na PTAX (1T28, base contra base sem a variável) | Quem precisa ouvir |
|---|---|---|---|---|
| Fed (`ffr`, carry) | sim: alta em set/26 e mais uma no 4T26 | real mais fraco | +0,01 (até +0,015 em 2T27) | câmbio; política monetária (espaço do Copom contra o Fed) |
| Curva dos EUA (fora do modelo) | sim: 10 anos em 5,00%, juro real no topo desde 2007 | pressão de alta em `rr_10a` | via `rr_10a`, que não escrevo | fiscal (principal de `rr_10a`) |
| Inflação dos EUA (`infl_us`, desconto de PPC) | sim: 3T26 em 1,12%; base cai a ~0,6% | real mais fraco (inflação americana abaixo do padrão de 0,91%) | +0,08 | câmbio |
| Dólar global (`dxy_em`) | sim: +1,6% no mês | real mais fraco no 4T26–1T27; mais forte depois | +0,04 no 4T26; −0,01 no 1T28 | câmbio |
| Apetite a risco (`sp500`) | não no nível; base sobe ~2% por trimestre | real mais fraco (sinal condicional da (F)[^sp]) | +0,13, o maior canal | câmbio; fiscal (CDS) |
| Commodities (`icbr_usd`; `icbr_agr_usd`, `icbr_met_usd`) | sim: energia +10,6% em set; metais +42% em 12 meses | `icbr_usd` levemente em queda: real mais fraco; grupos parados: pouco na inflação | +0,03 | câmbio; inflação |
| Energia (fora do modelo) | sim: Brent +90% em 12 meses | combustíveis e monitorados | — | inflação, fiscal (royalties) |
| Pares (fora do modelo) | Colômbia subindo, México parado depois de cortar | carry relativo | — | política monetária, câmbio |

O canal que mais move a PTAX no meu base é o S&P subindo, que no modelo deprecia o real porque o coeficiente é condicional ao CDS e ao dólar EM. Isso só é coerente se o CDS do fiscal carregar a compressão que um S&P em alta costuma trazer; pelo componente global medido por G (seção 4), o base do bloco de risco põe o CDS em ~141–145 no 4T26–1T27 e em ~120 no 1T28, e com esse CDS a PTAX do base fica em 5,45 no 1T28 em vez de 5,50 (por G). É o argumento a XS5.

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
- Base (50%): o choque de energia passa ao núcleo devagar (0,27% ao mês caindo a 0,24%); o Brent devolve o pico de outubro sem voltar a 84; o Fed sobe mais 0,25 p.p. numa reunião do 4T26 antes de dezembro, para 4,00–4,25%, e para; o primeiro corte vem no 1T28, com a inflação de volta a ~0,6% por trimestre. Uma alta só na reunião de meados de dezembro dá uma média de dezembro perto do piso da faixa, 4,00; a faixa cobre.
- Upside (30%): o Brent fica em 125–132 até o 1T27, o núcleo segue a 0,33% ao mês e a inflação esperada de 1 ano passa de 3%; o Fed sobe duas vezes até dezembro e mais uma no 1T27, até 4,50–4,75% (o caminho dos T-bills), e fica lá.
- Downside (20%): o Brent cai a ~80 no 1T27, o desemprego passa de 4,5% e o núcleo volta a 0,20% ao mês; o Fed não sobe mais, devolve a alta no 1T27 e corta até 3,00–3,25% no 3T27.

*Bloco 2, Risco e dólar*
- Base (55%): o dólar segue sustentado pelo juro americano enquanto o Fed sobe e cede a partir de 2027; o S&P sobe ~2% por trimestre, abaixo da história, com juro real alto.
- Upside do dólar EM / downside do S&P, risk-off (25%): mais uma alta do Fed com o Treasury de 10 anos acima de 5,4% derruba o S&P ~16% até o 1T27; o dólar EM sobe ~5%; recuperação lenta depois.
- Downside do dólar EM / upside do S&P, risk-on (20%): o Brent cai, o Fed para e depois corta, o dólar EM enfraquece ~5% até o 1T28 e o S&P sobe ~4% por trimestre até o 3T27.

*Bloco 3, Commodities*
- Base (55%): Brent de 114 (4T26) a 91 (1T28) em média do trimestre; metais estáveis em ~330 com o dólar alto; agro parado em 202.
- Upside (20%): o evento de oferta de petróleo se prolonga (Brent 129–130 no 4T26–1T27); custo de energia e demanda puxam metais a 362 e agro a 215.
- Downside, queda ampla (25%): o petróleo normaliza (Brent 78), a desaceleração global e o dólar forte derrubam metais a 275 e agro a 185.

**Caminhos das exógenas** (só as sete de que sou principal; as outras no padrão do simulador[^proc])

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
| `icbr_usd` (índice, último mês) | 205,7 · `comm_icbr_usd` · set/26 | base | 204,8 | 203,7 | 202,9 | 202,3 | 201,8 | 201,4 |
| | | alta | 213,8 | 217,5 | 218,9 | 218,0 | 217,5 | 217,4 |
| | | queda | 195,7 | 187,9 | 184,0 | 182,5 | 182,5 | 182,7 |
| `icbr_agr_usd` (índice, média) | 200,5 · `comm_icbr_usd` · 3T26 | base | 202,0 | 202,0 | 202,0 | 202,0 | 202,0 | 202,0 |
| | | alta | 205,0 | 210,7 | 214,0 | 215,0 | 215,0 | 215,0 |
| | | queda | 198,0 | 192,0 | 188,0 | 185,7 | 185,0 | 185,0 |
| `icbr_met_usd` (índice, média) | 330,1 · `comm_icbr_usd` · 3T26 | base | 331,7 | 330,0 | 330,0 | 328,7 | 327,3 | 325,7 |
| | | alta | 346,0 | 358,0 | 362,0 | 362,0 | 362,0 | 362,0 |
| | | queda | 320,0 | 298,3 | 283,3 | 277,0 | 275,0 | 275,0 |
| Brent, média do trimestre (US$/barril; fora do modelo) | 115,22 · `comm_brent` · 20/10 | base | 114,4 | 105,0 | 99,3 | 96,0 | 93,0 | 91,0 |
| | | alta | 129,0 | 130,0 | 124,0 | 118,0 | 113,3 | 110,0 |
| | | queda | 104,1 | 84,3 | 79,0 | 78,0 | 78,0 | 78,0 |

Motivo dos caminhos que não saem direto da história: o `infl_us` sai, por G, de caminhos mensais do núcleo e dos alimentos do CPI e do Brent do cenário, pela regressão trimestral do CPI cheio (0,756 · núcleo + 0,079 · energia + 0,157 · alimentos, 2010–2026) e pela ligação mensal Brent → CPI energia (0,14 no mês e 0,09 no seguinte, 2010–2026); cada cenário do bloco dos EUA usa o Brent do cenário de commodities de mesmo nome. O `icbr_usd` sai dos três grupos pela combinação estimada (seção 2.3) e é o valor de dezembro, março, junho, setembro; o 4T26 do total cai abaixo de setembro porque o Brent de dezembro no base (110) fica abaixo do de setembro (114,2). O `ffr` do 4T26 supõe a alta numa reunião antes de dezembro.

**Saída do modelo** (informação para os donos, não tese minha; faixa do modelo omitida[^faixa])

| Variável | Cenário | 4T26 | 1T27 | 2T27 | 3T27 | 4T27 | 1T28 |
|---|---|---|---|---|---|---|---|
| PTAX (R$/US$, fechamento) | padrão do simulador | 5,21 | 5,25 | 5,25 | 5,24 | 5,25 | 5,28 |
| | base (os três blocos) | 5,29 | 5,39 | 5,42 | 5,43 | 5,47 | 5,50 |
| | EUA upside | 5,27 | 5,37 | 5,39 | 5,39 | 5,43 | 5,47 |
| | EUA downside | 5,30 | 5,41 | 5,44 | 5,44 | 5,48 | 5,53 |
| | risk-off, CDS no padrão | 5,27 | 5,35 | 5,38 | 5,39 | 5,43 | 5,47 |
| | risk-off, CDS com o componente global | 5,48 | 5,71 | 5,68 | 5,64 | 5,63 | 5,61 |
| | risk-on, CDS com o componente global | 5,20 | 5,18 | 5,16 | 5,12 | 5,14 | 5,15 |
| | commodities em alta | 5,24 | 5,32 | 5,34 | 5,35 | 5,39 | 5,42 |
| | commodities em queda | 5,34 | 5,48 | 5,53 | 5,54 | 5,57 | 5,60 |
| | conjunto adverso (EUA up, risk-off, commodities em queda; CDS no padrão) | 5,31 | 5,42 | 5,45 | 5,46 | 5,49 | 5,53 |
| | conjunto choque de petróleo (EUA up, risk-off, commodities em alta; CDS no padrão) | 5,21 | 5,26 | 5,26 | 5,27 | 5,31 | 5,35 |
| IPCA 12 meses (%) | base | 5,30 | 4,91 | 4,42 | 4,45 | 4,34 | 4,18 |
| | commodities em alta | 5,34 | 5,04 | 4,63 | 4,72 | 4,60 | 4,39 |
| | commodities em queda | 5,26 | 4,76 | 4,15 | 4,08 | 3,92 | 3,79 |
| | risk-off, CDS com o componente global | 5,33 | 4,99 | 4,56 | 4,61 | 4,47 | 4,25 |
| Selic, média do trimestre (% a.a.) | base | 13,60 | 13,26 | 12,97 | 12,72 | 12,50 | 12,31 |
| | commodities em alta | 13,61 | 13,27 | 13,00 | 12,77 | 12,58 | 12,42 |
| | commodities em queda | 13,60 | 13,25 | 12,94 | 12,66 | 12,40 | 12,17 |

(`modelo.rodar`, retrato do ciclo, por G; os blocos não citados no cenário ficam no base; o CDS com componente global é ilustração, não caminho de referência: seção 4.) Duas leituras para os donos. No bloco dos EUA, o modelo dá o sinal contrário ao intuitivo: o cenário de Fed mais alto aprecia o real, porque a inflação americana entra com coeficiente 1 no desconto de PPC e pesa mais que o carry (seção 6). No conjunto "choque de petróleo", o mais provável dos conjuntos adversos dado o que o Brent fez em 2026, o real fica mais forte que no base porque o IC-Br sobe; se isso vale para uma alta puxada pela energia é pergunta ao câmbio (tempero i, abaixo).

### 3.2 Etapa 2 — o tempero qualitativo

**(i) `sp500` — efeito possivelmente mais fraco que o estimado no cenário base** · cenário base
- O multiplicador é do câmbio, dono da (F); argumento na seção 4.
- Coeficiente: `F.b_sp500` estimado 1,888 por desvio-padrão (8,4% de variação), intervalo de 90% do posterior de 0,980 a 2,787.
- Efeito: no meu base o S&P sobe ~11% em seis trimestres e responde por +0,13 na PTAX do 1T28 (decomposição por G), o maior canal externo.
- Por quê: o coeficiente mede o S&P com CDS e dólar EM parados; no base, o S&P sobe por lucro, com o dólar EM caindo de 2027 em diante e um CDS que, pelo componente global, comprimiria. Se o fiscal não carregar essa compressão, a (F) lê uma alta de bolsa como saída de capital do Brasil, o que não é a história do cenário. Dentro do intervalo, um multiplicador abaixo de 1 é defensável só se o CDS ficar parado.
- Onde entra: assimetria do câmbio (decisão do câmbio).

**(i) `icbr_usd` — efeito possivelmente mais fraco quando a alta é de energia** · cenário de commodities em alta e conjunto choque de petróleo
- O multiplicador é do câmbio; argumento na seção 4.
- Coeficiente: `F.b_icbr_usd` estimado −1,720 por desvio-padrão (7,5%), intervalo de 90% de −2,504 a −0,954.
- Efeito: no conjunto choque de petróleo, a alta do IC-Br leva a PTAX do 1T28 de 5,53 (conjunto adverso, commodities em queda) a 5,35.
- Por quê: o coeficiente é estimado numa amostra em que o agro pesa ~0,63 do índice; uma alta puxada pela energia, que o Brasil também importa em derivados, melhora menos os termos de troca. É hipótese, não medida: o banco do meu F não separa termos de troca por grupo, e o câmbio tem os dados (`cmb_termos_troca`, `cmb_comex_*`).
- Onde entra: limite da cauda de apreciação no cenário de commodities em alta (decisão do câmbio).

**(ii) Ponta longa americana e prêmio de prazo — Treasury de 10 anos** · todos os cenários
- Hoje: 5,00% (`us_interest_rate`, 23/10); juro real ex-ante 2,27% no ponto, 2,45% na média de outubro.
- Por que o modelo não vê: nenhum juro longo americano está no modelo; chega pelo `rr_10a`, do fiscal.
- Efeito: pressão de alta em `rr_10a`, pequena pelo histórico trimestral (seção 4, como subordinado).
- Onde entra: argumento ao fiscal; não muda meus caminhos.

**(ii) Componente global do CDS** · bloco de risco
- Hoje: CDS 137 p.b. (`cmb_risco_pais`, 26/10, dado do fiscal); +6 p.b. desde o fim do 3T26, contra +8 p.b. que o dólar EM e o S&P explicariam (por G).
- Por que o modelo não vê: o CDS é exógena do fiscal; os meus cenários de risco não o movem.
- Efeito: risk-off sem o CDS aprecia o real no modelo; com o componente global, a PTAX do 1T27 vai de 5,35 a 5,71.
- Onde entra: argumento ao fiscal (XS5) e ao câmbio; probabilidade do risk-off.

**(ii) Energia e combustíveis — Brent** · bloco de commodities
- Hoje: 115,22 (`comm_brent`, 20/10); média de outubro 125,0 até 20/10.
- Por que o modelo não vê: a (I) não tem energia; o Brent chega a combustíveis e monitorados fora do modelo.
- Efeito: caminhos do Brent na tabela da seção 3.1, o único caminho de petróleo do ciclo.
- Onde entra: tempero da inflação (decisão dela) e receita de royalties (fiscal).

**(ii) Demanda chinesa — sem dado** · bloco de commodities
- Hoje: só preço (metais 335,1, `comm_icbr_usd`, set/26) e exportação para a China (dado do câmbio).
- Por que o modelo não vê: não há variável da China, nem dado no banco.
- Efeito: é o motor do cenário de metais em alta ou em queda; sem dado, a probabilidade fica simétrica em torno do vento contra do dólar.
- Onde entra: probabilidades do bloco.

**(ii) Ciclo dos pares** · bloco de risco
- Hoje: Colômbia subindo (12,25%), México parado em 6,50% depois de cortar 1,00 p.p. em 12 meses (`inter_interest_rate`, 20/10).
- Por que o modelo não vê: carry relativo aos pares não está na (F).
- Efeito: sem direção clara neste ciclo; o Brasil segue com o maior juro real do grupo.
- Onde entra: argumento à política monetária e ao câmbio.

### 3.3 Da etapa 1 à tese

A central de cada linha é o caminho base; não há modelo entre o caminho e a tese, porque nenhuma equação produz as minhas variáveis. A faixa sai da distância até o caminho de cauda do bloco (com o mínimo dito na seção 1), e as probabilidades são as dos cenários do bloco: 50/30/20 no bloco dos EUA (upside maior porque os T-bills precificam uma alta a mais que o meu base), 55/25/20 no de risco (risk-off maior pelo preço alto do S&P com juro real alto) e 55/20/25 no de commodities (queda maior pelo nível perto do recorde, pelo dólar forte contra os metais e pela devolução recente do Brent). Os temperos do tipo (i) são decisão do câmbio e não movem nada aqui.

## 4. Para os outros agentes

**Respostas às entradas fixas (Parte 4 do mapa)**
- XE1 (câmbio): os sete caminhos estão na seção 3.1, com as probabilidades por bloco. É o primeiro ciclo, sem caminho anterior para comparar. Ponto que pesa na (F): no meu base, o S&P subindo é o maior canal externo na PTAX (+0,13 no 1T28), seguido do `infl_us` abaixo do padrão (+0,08).
- XE2 (câmbio), **em destaque**: o Brent está 89,8% acima de um ano antes e oscilou entre 114 e 136 desde 15/09 (`comm_brent` · 20/10, por G), um movimento sustentado de petróleo; o dólar subiu contra desenvolvidos e emergentes (DXY +1,2% e dólar EM +1,6% no mês) com o S&P perto da máxima, e a Colômbia segue subindo juro. O global se move pelo juro americano, não por aversão a risco (2.2).
- XE3 (política monetária), **em destaque**: o Fed virou, subiu 0,25 p.p. em 17/09/2026 depois de três cortes; o meu base tem mais uma alta no 4T26 e parada até o 1T28; os T-bills precificam duas em 12 meses. Os pares: Colômbia em alta, México, Chile e Peru parados.
- XE4 (inflação): `icbr_agr_usd` parado em 202,0 e `icbr_met_usd` de 331,7 a 325,7 no base, médias do trimestre; nas caudas, alta a 215 e 362, queda a 185 e 275, a partir do 1T27. Primeiro ciclo, sem mudança a apontar.
- XE5 (inflação), **em destaque**: o Brent fez um salto de 18% num pregão em 02/10 e está em 115,22 (20/10), com média de 125,0 em outubro até 20/10, contra 114,2 em setembro; o caminho do Brent (base de 114 no 4T26 a 91 no 1T28; alta de 129–130; queda a 78) está na seção 3.1. A inflação de bens nos EUA acelerou: núcleo de bens +0,25% em setembro (`inflc_cpi`, por G).
- XE6 (atividade): demanda externa pelo mercado de trabalho americano (criação fraca, desemprego estável), pelo bloco de risco e pelos metais no alto; a China só pelos preços e pela exportação para lá, sem dado de atividade. A probabilidade de recessão americana no horizonte que eu atribuo é a do downside do bloco dos EUA, 20%, julgamento sem modelo; o banco não tem PIB, produção ou pesquisas dos EUA.
- XE7 (atividade): os três caminhos do IC-Br e o Brent na seção 3.1; o nível de agro e metais perto do recorde sustenta renda agrícola e mineral no base.
- XE8 (atividade): Fed apertando (seção 2.1) e o S&P perto da máxima com juro real no topo desde 2007; risk-off com 25%.
- XE9 (fiscal), **em destaque**: as quatro moedas latinas enfraqueceram 2,3% a 7,8% no mês e o dólar EM subiu 1,6%, com o CDS +13 p.b. (`cmb_risco_pais` · 26/10); o componente global que vejo está abaixo, em "Como subordinado".
- XE10 (fiscal), **em destaque**: o Treasury de 10 anos subiu 0,99 p.p. em 12 meses e tocou 5,31% em 05/10, o maior desde 2007; caminho do 10 anos na seção 2.1 (base de 5,05 no 4T26 a 4,75 no 1T28).
- XE11 (fiscal): Brent e IC-Br na seção 3.1; o Brent médio de 114 no 4T26 no base, contra 66,6 em janeiro, é receita de royalties bem acima do início do ano.
- XE12 (expectativas): petróleo e commodities na seção 3.1; inflação americana pelo `infl_us` e pela inflação esperada de 1 ano do Cleveland Fed (2,98%, +0,59 p.p. em 3 meses). Leio o choque de energia como de oferta e em devolução gradual, não persistente, no base.

**Pedidos (saídas fixas da Parte 3 e deste ciclo)**
- XS1 ao câmbio: no último mês, quanto da depreciação do real foi global e quanto idiossincrática, contra o dólar EM e os pares? E o peso mexicano (+7,8% no mês) puxou o dólar EM? Depende disso a calibração do meu base do dólar EM (130,5–131) e do risk-off.
- XS2 ao câmbio: o fluxo financeiro e a posição especulativa em BRL nas últimas semanas confirmam que a alta do dólar EM chegou ao Brasil por dinheiro saindo, ou só por preço? Depende disso a probabilidade de 25% do risk-off.
- XS3 à política monetária: o caminho da Selic até o 1T28. Com o Fed a 4,13 no base, o diferencial contra o Fed e o maior juro real entre os pares (9,78% ex-post em agosto) se mantêm?
- XS4 à política monetária: o Copom já incorporou o petróleo acima de US$ 110 e o Fed em alta no cenário de referência? Qual a premissa de petróleo e de juro americano dele?
- XS5 ao fiscal: o caminho do CDS e quanto do seu movimento o fiscal atribui ao risco global. O meu base de risco pede ~141–145 p.b. no 4T26–1T27 pelo componente global e o risk-off pede ~175–210 p.b.; sem isso, a (F) aprecia o real num risk-off e deprecia num S&P em alta.
- XS6 ao fiscal (principal de `rr_10a`): o caminho do `rr_10a` e quanto dele vem da ponta longa americana.
- XS7 à inflação: a tese do IPCA depende mais de qual grupo de commodity, e em que trimestres? Em particular, do Brent no 4T26–1T27 (combustíveis)?
- XS8 às expectativas: o bloco externo do QPC piorou de 62% para 67% "menos favorável" entre R280 e R281; há outro sinal na Focus de que o mercado já precifica o Fed em alta e o petróleo acima de 110?

**Ao agente web** (marcados "(web)" no Faltou)
- O que causou o salto do Brent de 114,82 para 135,51 em 02/10/2026 e o recuo desde 16/10 (até 115,22 em 20/10): qual evento de oferta, em que região, e se há decisão da OPEP+ ou acordo em andamento. Depende disso o caminho base do Brent (devolução gradual) e a probabilidade do cenário de commodities em alta.
- O comunicado e a projeção (gráfico de pontos) do FOMC de setembro de 2026, que subiu a meta para 3,75–4,00%, e as datas das reuniões do FOMC no 4T26 e no 1T27; o que o presidente do Fed disse sobre altas adicionais. Depende disso a data da alta do meu base no 4T26 e a distância entre o meu caminho e o dos T-bills.
- O que explica a queda de 0,17 p.p. do Treasury de 10 anos de 21/10 para 22/10/2026. Depende disso a leitura de que a ponta longa negocia petróleo e não prêmio.
- O que explica a depreciação de 7,8% do peso mexicano entre 20/09 e 20/10/2026: evento do México ou global? Depende disso quanto da alta do dólar EM é global.
- Estado da demanda chinesa por metais em out/2026 (produção de aço, minério de ferro, estímulo ao setor imobiliário) e o estado do ENSO e das safras de soja e milho. Dependem disso os caminhos base de metais (parado em ~330) e agro (parado em 202).

**Como subordinado**

- **`rr_10a` · principal: fiscal**
  - Insumos: Treasury de 10 anos em 5,00% (`us_interest_rate` · 23/10), máximo de 5,31% em 05/10, o maior desde 2007; juro real ex-ante de 10 anos de 2,27% no ponto de 23/10 e 2,45% na média de outubro, o maior desde 2007 (`us_interest_rate` e `expc_inflacao`, por G); no 3T26, o juro real americano de 10 anos subiu 0,28 p.p. na média do trimestre e o `rr_10a` 0,18 p.p. (retrato do modelo, por G). O elo trimestral histórico é fraco: Δ`rr_10a` = 0,43 × Δ juro real americano de 10 anos (t 1,8; R² 0,04; 2006–2026), e 0,28 × Δ Treasury de 10 anos (t 1,8; R² 0,04) (por G). O meu caminho do 10 anos está na seção 2.1.
  - Argumento: o lado externo não sustenta um `rr_10a` em queda no 4T26–1T27, porque a ponta longa americana fica perto de 5% no base; mas o efeito do externo é pequeno pelo histórico: no base, a queda de 0,25 p.p. do 10 anos americano até o 1T28 dá −0,07 p.p. no `rr_10a`; no upside do bloco dos EUA (+0,50 p.p.), +0,14 p.p.; no downside (−0,60 p.p.), −0,17 p.p. (por G). Se o fiscal escrever o `rr_10a` caindo mais de 0,3 p.p. até o 1T27, o motivo tem de ser doméstico.
  - Caminho de referência: nenhum.
- **`fiscal` (CDS 5 anos) · principal: fiscal**
  - Insumos: ΔCDS trimestral = 12,4 p.b. por 1% de dólar EM (t 5,6) − 0,67 p.b. por 1% de S&P (t −0,8), R² 0,56, 2016–2026; desde 2006, 12,0 e −1,30 (R² 0,57) (retrato do modelo, por G). Desde o fim do 3T26, o dólar EM subiu de 129,38 para 130,21 e o CDS de 131 para 137 p.b. (+6), contra +8 p.b. que a regressão atribuiria ao global; no último mês, +13 p.b. contra +17 (`cmb_dollar_index_em`, `cmb_equity_us`, `cmb_risco_pais`, por G). O movimento recente do CDS cabe inteiro no componente global. Ressalva: o dólar EM contém o real, então uma piora do Brasil que deprecie o real entra no índice e a regressão superestima o global; não há CDS de pares nem spread emergente no banco para separar.
  - Argumento: o caminho do CDS do fiscal deveria carregar o meu bloco de risco. Pelo componente global (sem a constante), o base do dólar EM e do S&P põe o CDS em ~141 no 4T26 e ~145 no 1T27, caindo a ~120 no 1T28; o risk-off em ~176 no 4T26 e ~209 no 1T27; o risk-on em ~103 no 1T27 (por G; a regressão é linear e extrapola mal nos extremos do risk-on). Um CDS abaixo de 135 no 4T26 precisa de melhora doméstica; um CDS parado no risk-off faz o modelo apreciar o real.
  - Caminho de referência: nenhum (os números acima são o componente global, não o meu caminho do CDS).

**Divergências:** — (rodada 1).

## 5. Placar

Primeiro ciclo: não há report final anterior deste agente.

## 6. Sobre o modelo

Rodada sem literatura; as três propostas vêm dos dados e do mapa, e a terceira é a que mais pesa neste ciclo.

| Fonte | O que sugere (regressor, defasagem, quebra, âncora) | Teste proposto (dado, amostra, que resultado mudaria a especificação) | Por que importa para a tese deste ciclo |
|---|---|---|---|
| Dados (`inflc_cpi`) e mapa 2.3 | O desconto de PPC da (F) usa o CPI cheio com coeficiente fixo em 1; num choque de energia, a inflação americana sobe por energia e o modelo aprecia o real mecanicamente | Reestimar a (F) com o núcleo do CPI no lugar do cheio, e com o coeficiente livre, 2006–2026; se o coeficiente livre ficar abaixo de 0,5 ou o núcleo ajustar melhor, trocar | No meu bloco dos EUA, o cenário de Fed mais alto aprecia o real (PTAX 5,27 contra 5,29 no 4T26), o sinal oposto ao canal do carry que o mapa espera |
| Dados (`comm_brent`, `comm_icbr_usd`) e mapa 2.6 | Brent ou o IC-Br energia em reais nos monitorados da (I) | Acrescentar Δlog do Brent em reais, corrente e defasado, na equação de monitorados, 2006–2026; se significativo, a energia entra no modelo | O Brent subiu 89,8% em 12 meses e é o maior choque externo do ciclo; hoje ele chega ao IPCA só por tempero da inflação |
| Mapa 2.5 e a decomposição por G | O sinal condicional do S&P na (F): com o CDS parado, uma alta de bolsa deprecia o real | Reestimar a (F) com o S&P em excesso sobre a tendência de lucro (ou com interação S&P × ΔCDS), 2006–2026; se o efeito condicional desaparecer fora dos trimestres de crise, restringir | No meu base, o S&P subindo é o maior canal externo na PTAX (+0,13 no 1T28) |

[^conv]: Cada variável é medida como o modelo a lê: `ffr` é o Fed Funds **efetivo**, a média do último mês do trimestre (não o ponto médio da meta), porque é o juro que o carry da (F) usa; `infl_us` é a variação do CPI cheio no trimestre (100·Δlog de dezembro contra setembro, por exemplo), sem anualizar e sem acumular 12 meses; `dxy_em` e `sp500` são o fechamento; `icbr_usd` é o índice do último mês; `icbr_agr_usd` e `icbr_met_usd` são a média dos três meses. Um 1% de inflação no trimestre equivale a ~4% ao ano.
[^pctl]: Percentil: a posição do último valor no histórico, de 0 (o menor já visto) a 100 (o maior). Percentil 100 em 10 anos quer dizer que é o maior valor da década.
[^tbill]: Os T-bills (títulos curtos do Tesouro americano) rendem a média do juro do Fed esperada até o vencimento mais um prêmio pequeno. Medi o prêmio nos meses em que o Fed não mudou o juro nos 12 meses seguintes; o que sobra acima disso é a alta que o mercado espera. Não há futuros de Fed Funds no banco, que seriam a medida direta.
[^real]: Juro real ex-ante: o juro nominal menos a inflação esperada para o mesmo prazo (aqui, a do Cleveland Fed). Ex-post seria contra a inflação passada. Um juro real de 2,45% em 10 anos é o que um título americano sem risco paga acima da inflação esperada, e é contra isso que ativos emergentes competem.
[^tp]: Prêmio de prazo (term premium): o que o investidor exige a mais para ficar 10 anos num título em vez de rolar o juro curto por 10 anos. Ex.: se o mercado espera o juro curto médio em 4% por 10 anos e o 10 anos paga 4,5%, o prêmio é ~0,5 p.p. O banco não tem uma estimativa dele.
[^gfc]: Ciclo financeiro global: um fator comum que move bolsas, spreads de crédito e fluxos de capital em vários países ao mesmo tempo, e que tem o juro americano entre os seus motores. Quando ele vira, os emergentes perdem capital juntos.
[^em]: Dólar contra emergentes: índice do Fed (FRED) do dólar contra uma cesta de moedas de países emergentes, que inclui o real. Subir quer dizer dólar mais forte: se o peso mexicano, o real e as outras moedas da cesta perdem valor juntos, o índice sobe.
[^icbr]: IC-Br: índice de commodities do Banco Central, uma cesta de produtos que o Brasil exporta (agropecuária, metais e energia). Aqui em dólar, sem o efeito do câmbio; em reais, que é como chega ao IPCA, é dado da inflação.
[^ppc]: Desconto de PPC: na equação do câmbio do modelo, a diferença entre a inflação do Brasil e a dos EUA entra com peso 1 na variação do real. Se a inflação americana sobe 0,3 p.p. no trimestre, o modelo deprecia o real 0,3% a menos, sem passar pelo Fed.
[^sp]: Sinal condicional do S&P: na equação do câmbio, com o CDS e o dólar EM parados, uma alta da bolsa americana deprecia o real (capital indo para ações americanas). Sem condicionar, bolsa em alta costuma vir com real forte, porque o risk-on também comprime o CDS e enfraquece o dólar. Por isso o S&P e o dólar EM se escrevem juntos, e o CDS tem de acompanhar.
[^faixa]: A faixa que o simulador imprime é a incerteza dos pesos das equações (90% do posterior), não um intervalo de previsão; por isso fica fora da tabela.
[^proc]: Rodada 1: sem notícias e sem os caminhos dos outros agentes. As exógenas que não escrevo ficam no padrão do simulador: CDS 131,21 p.b., `rr_10a` 7,84%, volatilidade 12,19% e meta 3,00%, o último valor repetido. O F usado foi montado sem literatura; o conhecimento lido foi só o mapa conceitual.
