# Report — externo · ciclo 2026-10-02 · rodada 1

Dados até: 02/10/2026 (conjunto de informação de 02/10; o que saiu depois está separado na nota [^corte]) · Horizontes: 4T26 a 1T28, cada variável na convenção do Modelo Estrutural[^conv]

## 1. Tese

**A tese em uma frase:** um choque de oferta de petróleo (Brent de US$ 114 de média em setembro a US$ 135,51 em 02/10) levou o Fed a subir 25 p.b. em 17/09 com o núcleo ainda comportado; espero mais uma alta no 4T26 e juro parado até o 3T27, menos do que os T-bills precificam (de duas a três altas até abril de 2027), dólar contra emergentes firme perto de 130 e commodities sustentadas pela energia no 4T26 e devolvendo devagar em 2027; o risco principal é um risk-off com dólar acima de 132, que o modelo transmite pouco ao real porque a queda da bolsa americana compensa parte do dólar.

### Política dos EUA (cenários: base 50% · upside, Fed atrás da inflação, 30% · downside, petróleo devolve e o Fed desfaz a alta, 20%)

| Variável | Trimestre | Central | Base: faixa · P | Upside: limite · P | Downside: limite · P | P(up) − P(down) |
|---|---|---|---|---|---|---|
| `ffr`, Fed funds efetivo, média do último mês (% a.a.) | 4T26 | 4,13 | 3,88 a 4,13 · 65% | acima de 4,13 · 30% | abaixo de 3,88 · 5% | +0,25 |
| | 1T27 | 4,13 | 3,88 a 4,38 · 50% | acima de 4,38 · 30% | abaixo de 3,88 · 20% | +0,10 |
| | 2T27 | 4,13 | 3,88 a 4,38 · 50% | acima de 4,38 · 30% | abaixo de 3,88 · 20% | +0,10 |
| | 3T27 | 4,13 | 3,88 a 4,38 · 50% | acima de 4,38 · 30% | abaixo de 3,88 · 20% | +0,10 |
| | 4T27 | 3,88 | 3,38 a 4,38 · 50% | acima de 4,38 · 30% | abaixo de 3,38 · 20% | +0,10 |
| | 1T28 | 3,88 | 3,38 a 4,38 · 50% | acima de 4,38 · 30% | abaixo de 3,38 · 20% | +0,10 |
| `infl_us`, CPI no trimestre (100·Δlog, %) | 4T26 | 0,95 | 0,70 a 1,15 · 50% | acima de 1,15 · 30% | abaixo de 0,70 · 20% | +0,10 |
| | 1T27 | 0,56 | 0,45 a 0,70 · 50% | acima de 0,70 · 30% | abaixo de 0,45 · 20% | +0,10 |
| | 2T27 | 0,58 | 0,50 a 0,70 · 50% | acima de 0,70 · 30% | abaixo de 0,50 · 20% | +0,10 |
| | 3T27 | 0,60 | 0,50 a 0,70 · 60% | acima de 0,70 · 25% | abaixo de 0,50 · 15% | +0,10 |
| | 4T27 | 0,63 | 0,50 a 0,75 · 60% | acima de 0,75 · 20% | abaixo de 0,50 · 20% | 0,00 |
| | 1T28 | 0,64 | 0,50 a 0,75 · 60% | acima de 0,75 · 20% | abaixo de 0,50 · 20% | 0,00 |

- **Upside (Fed acima de 4,13 em dez/26, 4,63 em mar/27, 4,88 em jun/27):** o petróleo fica acima de US$ 135 até o 1T27 e o núcleo acelera para ~0,30% ao mês; o Fed segue o que os T-bills já precificam. Bom para o real dentro do modelo (o CPI mais alto abate a depreciação pela PPC e a alta do Fed só pesa no trimestre em que acontece), ruim fora dele: condições financeiras mais apertadas para emergentes e menos espaço para o Copom.
- **Downside (Fed de volta a 3,88 em mar/27 e a 3,13 em set/27):** o Brent devolve como em junho de 2026 e o mercado de trabalho, já fraco, enfraquece mais; o Fed desfaz a alta de setembro. A cauda abaixo de 3,88 no 4T26 é um corte já em dezembro, por isso só 5%.

### Risco e dólar (cenários: base 50% · risk-off 30% · risk-on 20%)

| Variável | Trimestre | Central | Base: faixa · P | Upside: limite · P | Downside: limite · P | P(up) − P(down) |
|---|---|---|---|---|---|---|
| `dxy_em`, dólar contra emergentes, fechamento (índice) | 4T26 | 130,0 | 128,0 a 132,5 · 50% | acima de 132,5 · 30% | abaixo de 128,0 · 20% | +0,10 |
| | 1T27 | 130,0 | 127,5 a 133,0 · 50% | acima de 133,0 · 30% | abaixo de 127,5 · 20% | +0,10 |
| | 2T27 | 129,5 | 127,0 a 132,5 · 50% | acima de 132,5 · 30% | abaixo de 127,0 · 20% | +0,10 |
| | 3T27 | 129,0 | 126,5 a 132,0 · 50% | acima de 132,0 · 30% | abaixo de 126,5 · 20% | +0,10 |
| | 4T27 | 128,5 | 126,0 a 131,0 · 50% | acima de 131,0 · 30% | abaixo de 126,0 · 20% | +0,10 |
| | 1T28 | 128,5 | 126,0 a 130,5 · 50% | acima de 130,5 · 30% | abaixo de 126,0 · 20% | +0,10 |
| `sp500`, S&P 500, fechamento (pontos) | 4T26 | 7.700 | 7.300 a 7.900 · 50% | acima de 7.900 · 20% | abaixo de 7.300 · 30% | −0,10 |
| | 1T27 | 7.800 | 7.300 a 8.050 · 50% | acima de 8.050 · 20% | abaixo de 7.300 · 30% | −0,10 |
| | 2T27 | 7.900 | 7.400 a 8.150 · 50% | acima de 8.150 · 20% | abaixo de 7.400 · 30% | −0,10 |
| | 3T27 | 8.000 | 7.550 a 8.300 · 50% | acima de 8.300 · 20% | abaixo de 7.550 · 30% | −0,10 |
| | 4T27 | 8.100 | 7.700 a 8.400 · 50% | acima de 8.400 · 20% | abaixo de 7.700 · 30% | −0,10 |
| | 1T28 | 8.200 | 7.850 a 8.550 · 50% | acima de 8.550 · 20% | abaixo de 7.850 · 30% | −0,10 |

- **Risk-off (upside do `dxy_em`, downside do `sp500`):** o choque de petróleo e o juro longo americano em máxima de dez anos derrubam a bolsa ~10% (6.900 no 4T26, 6.800 no 1T27) e levam o dólar EM a 134,5–135, como em março de 2026 e nos trimestres de queda forte da bolsa desde 2006 (seção 2.2). Ruim para o Brasil pelo dólar EM e, fora do modelo, pelo CDS; dentro do modelo o efeito no real sai pequeno, porque a queda do S&P compensa (seção 3.1).
- **Risk-on (downside do `dxy_em`, upside do `sp500`):** o petróleo se resolve rápido, o Fed não sobe mais, o dólar EM volta a 127 e a 125 em 2027 e a bolsa segue subindo. Bom para o real.

### Commodities (cenários: base 50% · upside 25% · downside 25%)

| Variável | Trimestre | Central | Base: faixa · P | Upside: limite · P | Downside: limite · P | P(up) − P(down) |
|---|---|---|---|---|---|---|
| `icbr_usd`, IC-Br em US$, último mês (índice) | 4T26 | 207,2 | 202,0 a 211,0 · 50% | acima de 211,0 · 25% | abaixo de 202,0 · 25% | 0,00 |
| | 1T27 | 204,1 | 198,0 a 210,0 · 50% | acima de 210,0 · 25% | abaixo de 198,0 · 25% | 0,00 |
| | 2T27 | 202,1 | 195,0 a 210,0 · 50% | acima de 210,0 · 25% | abaixo de 195,0 · 25% | 0,00 |
| | 3T27 | 200,7 | 192,0 a 211,0 · 50% | acima de 211,0 · 25% | abaixo de 192,0 · 25% | 0,00 |
| | 4T27 | 199,6 | 189,0 a 211,0 · 50% | acima de 211,0 · 25% | abaixo de 189,0 · 25% | 0,00 |
| | 1T28 | 198,6 | 186,0 a 212,0 · 50% | acima de 212,0 · 25% | abaixo de 186,0 · 25% | 0,00 |
| `icbr_agr_usd`, IC-Br agropecuária, média do trimestre | 4T26 | 200,8 | 198,5 a 202,5 · 50% | acima de 202,5 · 25% | abaixo de 198,5 · 25% | 0,00 |
| | 1T27 | 200,2 | 196,5 a 203,5 · 50% | acima de 203,5 · 25% | abaixo de 196,5 · 25% | 0,00 |
| | 2T27 | 199,6 | 194,5 a 204,5 · 50% | acima de 204,5 · 25% | abaixo de 194,5 · 25% | 0,00 |
| | 3T27 | 199,0 | 192,5 a 205,5 · 50% | acima de 205,5 · 25% | abaixo de 192,5 · 25% | 0,00 |
| | 4T27 | 198,4 | 190,5 a 207,0 · 50% | acima de 207,0 · 25% | abaixo de 190,5 · 25% | 0,00 |
| | 1T28 | 197,8 | 188,0 a 208,5 · 50% | acima de 208,5 · 25% | abaixo de 188,0 · 25% | 0,00 |
| `icbr_met_usd`, IC-Br metal, média do trimestre | 4T26 | 335,7 | 330,0 a 340,0 · 50% | acima de 340,0 · 25% | abaixo de 330,0 · 25% | 0,00 |
| | 1T27 | 333,7 | 322,0 a 344,0 · 50% | acima de 344,0 · 25% | abaixo de 322,0 · 25% | 0,00 |
| | 2T27 | 331,7 | 315,0 a 348,0 · 50% | acima de 348,0 · 25% | abaixo de 315,0 · 25% | 0,00 |
| | 3T27 | 329,8 | 307,0 a 352,0 · 50% | acima de 352,0 · 25% | abaixo de 307,0 · 25% | 0,00 |
| | 4T27 | 327,8 | 300,0 a 357,0 · 50% | acima de 357,0 · 25% | abaixo de 300,0 · 25% | 0,00 |
| | 1T28 | 325,8 | 293,0 a 362,0 · 50% | acima de 362,0 · 25% | abaixo de 293,0 · 25% | 0,00 |

- **Upside (IC-Br a 215 em dez/26 e 226 em mar/28):** a interrupção de oferta de petróleo dura (Brent de US$ 143 de média no 4T26 e US$ 130 no 2T27) e os metais sobem ~1% ao mês. Bom para o real (termos de troca, o `icbr_usd` na equação do câmbio), ruim para a inflação (alimentos e bens industriais na curva de Phillips, mais combustíveis fora do modelo).
- **Downside (IC-Br a 198 em dez/26 e 175 em mar/28):** o petróleo devolve como em junho (Brent a US$ 85 no 1T27) e a desaceleração global derruba os metais ~1,5% ao mês. Ruim para o real, bom para a inflação; no modelo o segundo efeito domina a Selic só a partir de 2027 (seção 3.1).

## 2. Argumentação

### 2.1 Política dos EUA (Q1)

**O Fed subiu 25 p.b. com o núcleo comportado, e a razão visível no dado é o petróleo e a inflação esperada de curto prazo.** A meta passou de 3,50–3,75% para 3,75–4,00% em 17/09 (ponto médio 3,875, `us_interest_rate` · 17/09), depois de três cortes no fim de 2025 e nove meses parada. Com a informação de 02/10, o CPI até agosto mostrava o núcleo a 2,0% anualizado em três meses e 2,45% em 12 meses, e serviços sem energia a 2,4% e 3,0% (`inflc_cpi` · ago/26); o PCE núcleo, a medida do Fed, estava em 3,0% em 12 meses e 2,05% anualizado em três meses (`inflc_pce` · ago/26). O que subiu foi a energia, +16% em 12 meses até agosto (`inflc_cpi` · ago/26), e a inflação esperada de um ano, de 2,40% em agosto para 2,66% em setembro (`expc_inflacao` · set/26). A alta de setembro diz, portanto, que a função de reação deste Fed responde ao risco de o choque de energia contaminar as expectativas, e não só ao núcleo. Mas a âncora longa se mexeu pouco: 2,47% em junho e 2,58% em setembro para dez anos (`expc_inflacao` · set/26), o que limita quanto mais o Fed precisa fazer.

**O mercado de trabalho não pede aperto.** O payroll criou 29 mil vagas em setembro (preliminar) e 51 mil por mês na média de três meses, contra 41 mil na de doze (`mt_ces` · set/26); a taxa de pedidos de demissão está em 1,9%, no percentil 10 dos últimos dez anos[^pctl], e a de contratações em 3,3%, percentil 16 (`mt_jolts` · ago/26); o desemprego está em 4,2% (`mt_cps` · set/26). Mas o salário por hora ainda cresce 3,0% em 12 meses (`mt_ces` · set/26), em linha com núcleo de 2,5–3%, e não abaixo: o mercado de trabalho fraco reduz o risco de segunda rodada, não o elimina.

**Espero menos do que os T-bills precificam.** Descontado o prêmio histórico dos bills sobre o efetivo em meses sem mudança da meta (+0,02 p.p. no de 3 meses e +0,04 no de 6, desde 2010, `us_interest_rate` e `diferenciais_juros`), os vértices de 02/10 precificam cerca de duas altas de 25 p.b. até o início de janeiro (3 meses a 4,19%), quase três até abril (6 meses a 4,27%) e de quatro a seis em doze meses (1 ano a 4,46%, onde o prêmio histórico tem só quatro observações) (`us_interest_rate` · 02/10)[^bills]. Meu cenário base tem uma alta no 4T26 e o juro parado até o 3T27, com um corte no 4T27, quando o petróleo já devolveu: o efetivo de dezembro a 4,13% contra ~4,4% no preço. A diferença é a aposta deste report: o choque é de oferta, o núcleo e o emprego não acompanham, e uma vez que a inflação esperada de um ano pare de subir o Fed não precisa validar o resto da curva. **O meu upside é o preço de mercado**, por isso ele tem 30%. Não há futuros de Fed funds nem o calendário do FOMC no banco: a leitura do preço sai dos bills, com prêmio.

**A parte longa subiu mais que a curta, e é juro real.** Desde 30/06 o Treasury de 2 anos subiu 0,69 p.p. (4,14% para 4,83%) e o de 10 anos 0,84 p.p. (4,44% para 5,28%), no percentil 100 de dez anos (`us_interest_rate` · 02/10); a inclinação 10a−2a foi de 0,30 para 0,45 p.p. Como a inflação esperada de dez anos subiu só 0,12 p.p. no período (`expc_inflacao` · jun–set/26), o juro real ex-ante de dez anos foi de 1,97% para 2,70%, percentil 98 de dez anos (G sobre `us_interest_rate` e `expc_inflacao`). Uma parte disso é o Fed (o 2 anos subiu junto), mas o excesso no longo é prêmio de prazo[^tp]: a parte longa não é sinal do Fed e vai para o bloco de quem escreve o `rr_10a`. Meu caminho do Treasury de 10 anos, fora do modelo: 5,25% no fim do 4T26, 5,15, 5,05, 4,95, 4,85 e 4,80 no 1T28 (base); acima de 5,6% no upside, abaixo de 4,6% no downside.

**Por que a central do `infl_us`.** O CPI cheio do trimestre (0,95% no 4T26) sai do Brent: com a relação medida de 2015 a agosto de 2026, uma alta de 10% no Brent no mês soma ~0,09 p.p. ao CPI cheio do mês e ~0,05 no seguinte, sobre 0,88 vez o núcleo (R² 0,71, `inflc_cpi` e `comm_brent`). Com o Brent médio de US$ 124 no 4T26 (US$ 96 no 3T26) e o núcleo a 0,25% ao mês, o CPI de 12 meses vai a ~4,0% em dezembro e volta a ~2,4% em dez/27 na base. O 1T27 cai para 0,56% porque o Brent já devolve. A cauda de cima tem mais peso porque o núcleo de setembro, divulgado depois do corte, veio mais alto que a média recente[^corte]; isso não entrou na central.

### 2.2 Risco e dólar (Q2)

**O ciclo financeiro global virou contra os emergentes em setembro, pelo dólar e não pela bolsa.** O dólar contra emergentes[^dxyem] subiu de 126,86 em 31/08 (perto da mínima do ano, 126,12 em 09/09) para 129,38 em 30/09 e 129,71 em 02/10 (`cmb_dollar_index_em`), e o DXY subiu 2,4% em um mês, para 101,93 (`cmb_dollar_index` · 02/10). As moedas latinas se depreciaram todas no mês: peso mexicano +7,8%, chileno +5,0%, colombiano +3,9%, sol +2,5% (`cmb_fx_latam` · 02/10), e a correlação delas com o dólar EM em três meses está entre +0,45 e +0,72 (F, "o que anda junto"). O que mostra que é um movimento comum é o DXY andar junto com o dólar EM (+0,60 em três meses); a divisão do real entre global e próprio é do câmbio (XS1). Mas a bolsa não acompanhou: o S&P está em 7.723, a 1% da máxima de 13/08 (7.799) e no percentil 99 de dez anos (`cmb_equity_us` · 02/10). Um choque de petróleo com o juro real de dez anos em 2,7% e a bolsa na máxima é a combinação que deixa a cauda de risk-off com 30%: o preço das ações ainda não incorpora o que o juro e o dólar já mostram.

**O risk-off tem precedente neste mesmo ano e no histórico.** No pico de petróleo de março, o Brent foi de US$ 71,32 (27/02) a US$ 121,88 (30/03), o S&P caiu de 6.879 para 6.344 e o dólar EM subiu de 127,4 para 131,3 (`comm_brent`, `cmb_equity_us`, `cmb_dollar_index_em`). Nos nove trimestres desde 2006 em que o S&P caiu 8% ou mais, o dólar EM subiu 4,05% em média, e a correlação trimestral entre os dois é −0,62 (G, 2006–3T26). O cenário de risk-off (S&P −10%, dólar EM +3,7% no 4T26) está dentro dessa régua. A variação trimestral do dólar EM tem percentil 90 de +4,5% e percentil 10 de −2,8% (G, 2006–3T26): os limites das faixas (132,5 e 128,0 no 4T26) ficam entre o meio e essas pontas.

**Os pares estão em ciclos diferentes, e o único que aperta é a Colômbia.** A Colômbia subiu 0,25 p.p. no mês, para 12,25% (+3,00 p.p. em 12 meses), o México está parado em 6,50% depois de cortar 1,00 p.p. em 12 meses, e Chile (4,50%) e Peru (4,25%) estão parados (`inter_interest_rate` · 02/10). Em juro real ex-post, o Brasil tem 9,78%, a Colômbia 5,76%, o México 3,24%, o Chile 0,37% e o Peru −0,19% (`cmb_real_rates` · ago/26)[^realexpost]. O Fed subindo enquanto o México e o Chile param reduz o carry relativo deles; o do Brasil continua o maior da amostra. Como o Copom usa esse espaço é da política monetária (XS3).

**O CDS subiu junto com o dólar EM em setembro.** O CDS de 5 anos foi de 122 p.b. (31/08) para 131 (30/09 e 02/10) (`cmb_risco_pais`), no mesmo mês em que o dólar EM subiu 2,0% e todos os pares latinos se depreciaram. É um movimento que tem cara de componente global, mas o banco não tem o CDS de outro país nem spread de emergentes para separá-lo: a parte global é argumento, e a trajetória é do fiscal (XS5).

### 2.3 Commodities (Q3)

**A energia comanda o IC-Br neste trimestre; agro e metais estão parados em níveis altos.** Com a informação de 02/10, o último IC-Br publicado era o de agosto: 202,3, com agropecuária a 201,2, metal a 337,1 e energia a 86,8 (`comm_icbr_usd` · ago/26). O Brent saiu de US$ 91 de média em agosto para US$ 114 em setembro e US$ 135,51 em 02/10, depois de subir de US$ 114,82 para US$ 135,51 só no último pregão (`comm_brent` · 02/10). O grupo energia responde ao Brent com elasticidade de ~0,46 no mês (G, 2010–ago/26, R² 0,60), e pesa ~17% na variação do IC-Br; agro pesa ~66% e metais ~19% (G, regressão das variações mensais do total nas dos grupos, 2023–ago/26, R² 0,99)[^icbr]. Por isso o IC-Br de dezembro na base (207,2) sobe pela energia mesmo com agro e metais levemente em queda.

**O que causa o choque de petróleo o banco não mostra.** O tamanho e a forma (dois saltos no ano, março–abril e setembro–outubro, com a devolução de junho a US$ 70,46 no meio, `comm_brent`) e o fato de os metais terem caído 0,6% e o S&P subido 0,7% no mesmo mês (F) apontam para oferta, não para demanda. Mas não há dado de estoques, de produção da OPEP ou de notícia: a persistência do choque, que decide a cauda de cima, é a maior incerteza deste bloco. A base supõe devolução gradual (US$ 110 no 1T27, US$ 90 no 1T28), mais lenta que a de junho.

**O dólar forte joga contra agro e metais, mas não contra a energia neste ano.** A correlação mensal entre o dólar EM e o IC-Br é −0,40 em dez anos e −0,24 nos últimos doze meses; nos metais é −0,51 em doze meses; na energia é +0,33 em doze meses, contra −0,18 em dez anos (G, até ago/26): no último ano dólar e petróleo subiram juntos, o que é a assinatura de um choque de oferta que também aperta o Fed. Daí a base com agro −0,1% e metais −0,2% ao mês. A China, que decide os metais, não está no banco: a leitura que sobra é o preço dos metais (perto da máxima de dez anos, 350,9 em mai/26) e as exportações para a China, que são dado do câmbio (`cmb_comex_pais`: US$ 109 bi em 12 meses até setembro, contra US$ 94 bi um ano antes).

### 2.4 Como chega ao Brasil (Q4)

| Linha do mapa (2.8) | Andou? | Sinal para o Brasil | Quem precisa ouvir |
|---|---|---|---|
| Fed (`ffr`) | sim: +25 p.b. em 17/09, mais uma na base | no modelo, só no trimestre da alta (carry em diferença); fora, menos espaço para o Copom | câmbio, política monetária |
| Curva americana (fora do modelo) | sim: 10 anos +0,84 p.p. desde junho, juro real 2,7% | pressiona o `rr_10a` para cima | quem escreve o `rr_10a` |
| Inflação dos EUA (`infl_us`) | sim: 0,95% no 4T26 pelo petróleo | aprecia o real mecanicamente (PPC); deprecia pelo Fed, que o modelo não liga | câmbio |
| Dólar global (`dxy_em`) | sim: +2,0% em setembro | deprecia o real | câmbio |
| Apetite a risco (`sp500`) | não: bolsa na máxima | é a cauda; S&P sozinho em queda aprecia o real no modelo | câmbio, fiscal (CDS) |
| Commodities (`icbr_usd`, agro, metal) | energia sim; agro e metal parados | energia: termos de troca melhores e combustível mais caro (fora do modelo); agro e metal neutros | câmbio, inflação, atividade, fiscal |
| Pares (fora do modelo) | Colômbia sobe; México, Chile e Peru param | carry relativo do Brasil maior | política monetária, câmbio |

Dentro do modelo, a soma dos três blocos na base é pequena e o bloco que mais move o real é o de commodities: o downside de commodities leva a PTAX a 5,60 no 1T28 contra 5,46 na base, o risk-off a 5,46 e o upside do Fed a 5,43 (seção 3.1). Fora do modelo, o que chega mais forte é o juro longo americano (pelo `rr_10a`) e o petróleo (pelos combustíveis), e nenhum dos dois é variável minha.

**Olhado, sem sinal.**
- Desemprego amplo (U-6) · 7,6% (`mt_cps` · set/26) · caiu 0,3 p.p. em três meses, contra o resto do mercado de trabalho · diria algo se subisse junto com a U-3.
- Taxa de participação · 61,8% (`mt_cps` · set/26) · +0,3 p.p. em três meses, dentro do ruído · diria algo com uma queda que explicasse a U-3 estável.
- Posicionamento em BRL e MXN · fundos alavancados comprados em MXN, +24 mil contratos em três meses (`cmb_cot_fx` · 29/09) · dado do câmbio, e a leitura dele é XS2 · diria algo se a posição em BRL virasse junto com a depreciação dos pares.
- QPC, ambiente externo · "menos favorável" de 62% para 67% (`expc_qpc` · 23/09) · a mudança de 5 p.p. confirma a leitura, não acrescenta · diria algo se o consenso divergisse do cenário (XS8).
- Termos de troca · 111,35 (`cmb_termos_troca` · jul/26) · três meses de defasagem, antes do salto do petróleo · diria algo com o dado de setembro.

## 3. Premissas

### 3.1 Etapa 1 — o modelo

**Cenários.**
- Política dos EUA — Base (50%): o Fed sobe mais 25 p.b. no 4T26 e para; corta 25 p.b. no 4T27, com o Brent de volta a ~US$ 92. Upside (30%): o petróleo fica acima de US$ 135 até o 1T27, o núcleo acelera e o Fed segue o preço dos bills (efetivo a 4,88% em jun/27). Downside (20%): o Brent devolve como em junho, o emprego enfraquece e o Fed desfaz a alta e corta até 3,13% em set/27.
- Risco e dólar — Base (50%): dólar EM firme em 130 até o 1T27, cedendo a 128,5; S&P +1,3% por trimestre, abaixo da mediana histórica (+3,8%), pelo juro real alto. Risk-off (30%): o choque de petróleo e o juro longo derrubam a bolsa ~10% e levam o dólar EM a 134,5–135. Risk-on (20%): o petróleo se resolve, o Fed para em 3,88% e o dólar EM volta a 125.
- Commodities — Base (50%): Brent médio de US$ 124 no 4T26, US$ 110 no 1T27, US$ 90 no 1T28; agro −0,1% e metais −0,2% ao mês. Upside (25%): a interrupção de oferta dura (US$ 143 no 4T26, US$ 130 no 2T27) e os metais sobem 1% ao mês. Downside (25%): o petróleo devolve rápido (US$ 85 no 1T27) e a desaceleração global derruba agro (−0,7% ao mês) e metais (−1,5% ao mês).

**Caminhos das exógenas.** Na convenção do modelo; o Brent, fora do modelo, vai na última linha porque é dele que saem o `infl_us` e o `icbr_usd`.

| Exógena | Hoje (valor · tabela · data) | Cenário | 4T26 | 1T27 | 2T27 | 3T27 | 4T27 | 1T28 |
|---|---|---|---|---|---|---|---|---|
| `ffr` | 3,75 · `diferenciais_juros` · set/26 (média de set, com a alta de 17/09) | base | 4,13 | 4,13 | 4,13 | 4,13 | 3,88 | 3,88 |
| | | upside | 4,38 | 4,63 | 4,88 | 4,88 | 4,88 | 4,63 |
| | | downside | 3,88 | 3,63 | 3,38 | 3,13 | 3,13 | 3,13 |
| `infl_us` | 0,47 · `inflc_cpi` · jun–ago/26 (3T26 parcial em 02/10) | base | 0,95 | 0,56 | 0,58 | 0,60 | 0,63 | 0,64 |
| | | upside | 1,33 | 0,84 | 0,81 | 0,73 | 0,69 | 0,68 |
| | | downside | 0,44 | 0,43 | 0,47 | 0,56 | 0,52 | 0,56 |
| `dxy_em` | 129,71 · `cmb_dollar_index_em` · 02/10 | base | 130,0 | 130,0 | 129,5 | 129,0 | 128,5 | 128,5 |
| | | risk-off | 134,5 | 135,0 | 134,0 | 133,0 | 132,0 | 131,0 |
| | | risk-on | 127,0 | 126,0 | 125,5 | 125,0 | 124,5 | 124,5 |
| `sp500` | 7.723 · `cmb_equity_us` · 02/10 | base | 7.700 | 7.800 | 7.900 | 8.000 | 8.100 | 8.200 |
| | | risk-off | 6.900 | 6.800 | 7.000 | 7.200 | 7.400 | 7.600 |
| | | risk-on | 8.050 | 8.250 | 8.400 | 8.550 | 8.700 | 8.850 |
| `icbr_usd` | 202,3 · `comm_icbr_usd` · ago/26 | base | 207,2 | 204,1 | 202,1 | 200,7 | 199,6 | 198,6 |
| | | upside | 214,7 | 216,7 | 219,2 | 221,4 | 223,6 | 226,2 |
| | | downside | 198,1 | 192,5 | 187,2 | 183,1 | 178,7 | 174,7 |
| `icbr_agr_usd` | 201,2 · `comm_icbr_usd` · ago/26 | base | 200,8 | 200,2 | 199,6 | 199,0 | 198,4 | 197,8 |
| | | upside | 203,2 | 206,3 | 209,4 | 212,6 | 215,8 | 219,0 |
| | | downside | 198,4 | 194,3 | 190,2 | 186,3 | 182,4 | 178,6 |
| `icbr_met_usd` | 337,1 · `comm_icbr_usd` · ago/26 | base | 335,7 | 333,7 | 331,7 | 329,8 | 327,8 | 325,8 |
| | | upside | 343,9 | 354,4 | 365,2 | 376,3 | 387,8 | 399,6 |
| | | downside | 327,1 | 312,8 | 299,0 | 285,8 | 273,3 | 261,2 |
| Brent, média do trimestre (fora do modelo, US$/barril) | 135,51 · `comm_brent` · 02/10 | base | 124 | 110 | 100 | 95 | 92 | 90 |
| | | upside | 143 | 138 | 130 | 122 | 115 | 110 |
| | | downside | 103 | 85 | 80 | 80 | 78 | 78 |

- O `ffr` é o efetivo, não o ponto médio: em 2026 o efetivo ficou 0,005 a 0,015 p.p. acima do ponto médio (`diferenciais_juros` e `us_interest_rate`), e uma alta de 25 p.b. leva o efetivo de ~3,89% a ~4,13%[^ffr].
- O `infl_us` e os três IC-Br saem de caminhos mensais do Brent, do núcleo do CPI e dos grupos, pelas relações medidas na seção 2 (G `ex_cenarios_r1.py`). O IC-Br total é o de dezembro, março etc.; agro e metal são médias do trimestre, por isso o total do 4T26 (207,2) já carrega o pico de energia de outubro e as médias não.
- As outras exógenas ficaram no padrão do simulador: CDS em 131,21 p.b. (aguarda fiscal, XS5), `rr_10a` em 7,84% (aguarda quem o escreve, XS6), vol implícita em 12,19% (2T26, segurada, aguarda câmbio) e meta de inflação em 3,00%.

**Saída do modelo** (G `ex_cenarios_r1.py`; cada cenário move só o próprio bloco, com os outros na base; informação para os donos, não tese minha).

| Variável | Cenário | 4T26 | 1T27 | 2T27 | 3T27 | 4T27 | 1T28 |
|---|---|---|---|---|---|---|---|
| PTAX de fechamento (R$/US$) | base | 5,24 | 5,33 | 5,36 | 5,37 | 5,40 | 5,46 |
| | Fed upside · downside | 5,23 · 5,26 | 5,32 · 5,35 | 5,35 · 5,38 | 5,35 · 5,38 | 5,38 · 5,42 | 5,43 · 5,48 |
| | risk-off · risk-on | 5,27 · 5,19 | 5,35 · 5,26 | 5,38 · 5,30 | 5,39 · 5,31 | 5,41 · 5,34 | 5,46 · 5,41 |
| | commodities upside · downside | 5,20 · 5,30 | 5,27 · 5,40 | 5,27 · 5,45 | 5,27 · 5,47 | 5,28 · 5,52 | 5,32 · 5,60 |
| IPCA 12 meses (%) | base | 5,29 | 4,88 | 4,38 | 4,40 | 4,28 | 4,12 |
| | commodities upside · downside | 5,32 · 5,26 | 4,97 · 4,80 | 4,54 · 4,21 | 4,66 · 4,12 | 4,62 · 3,91 | 4,53 · 3,68 |
| | Fed e risco (todos) | 5,28 a 5,29 | 4,86 a 4,89 | 4,34 a 4,39 | 4,36 a 4,41 | 4,24 a 4,29 | 4,09 a 4,12 |
| Selic, média do trimestre (% a.a.) | base | 13,60 | 13,26 | 12,97 | 12,71 | 12,49 | 12,29 |
| | commodities upside · downside | 13,60 · 13,60 | 13,27 · 13,25 | 12,99 · 12,95 | 12,75 · 12,67 | 12,56 · 12,41 | 12,40 · 12,18 |
| | Fed e risco (todos) | 13,60 | 13,26 | 12,96 a 12,97 | 12,70 a 12,71 | 12,48 a 12,49 | 12,28 a 12,30 |

Três leituras, para os donos dessas variáveis:
- **O Fed mais duro aprecia o real no modelo** (5,43 contra 5,46 no 1T28): o CPI mais alto entra pela PPC com coeficiente 1, e o carry só pesa no trimestre da alta. O efeito que importa para o Brasil, condições financeiras mais apertadas, não está no modelo.
- **O risk-off quase não move o real** (5,27 contra 5,24 no 4T26): o dólar EM +3,5% deprecia, e o S&P −10% aprecia, pelo sinal condicional da bolsa. O S&P sozinho em queda leva a PTAX a 5,12 no 4T26 (G, teste), o que mostra que escrever o risk-off só pela bolsa daria o sinal errado. Com o CDS parado no padrão, o modelo também não carrega o canal pelo qual um risk-off costuma chegar ao real.
- **Commodities é o bloco que divide o efeito**: o downside deprecia o real (5,60 no 1T28) e desinflaciona (IPCA 12m 3,68% contra 4,12%), e o modelo responde com a Selic 0,11 p.p. mais baixa no 1T28. Um estresse combinado (Fed upside, risk-off e commodities upside) dá PTAX 5,22 no 4T26 e 5,29 no 1T28, abaixo da base: no modelo a energia e o CPI americano compensam o dólar.

A faixa que o modelo imprime é só do posterior dos pesos, não intervalo de previsão.

### 3.2 Etapa 2 — o tempero qualitativo

Os canais das minhas variáveis estão todos em equações de outros agentes; não aplico multiplicador. Os argumentos de (i) vão para o dono na seção 4.

**(i) `sp500` — efeito mais fraco que o estimado num risk-off de petróleo e juro** · cenário risk-off
- O multiplicador é do câmbio (`F.b_sp500`).
- Coeficiente: estimado 1,888, intervalo de 90% do posterior 0,980 a 2,787. Proposta: × 0,5 a 0,6, na borda de baixo do intervalo.
- Efeito: sem a compensação da bolsa, o risk-off se aproxima do efeito do dólar EM sozinho; o câmbio mede.
- Por quê: o sinal condicional (bolsa subindo, real mais fraco) é a competição por capital entre ações americanas e emergentes; num risk-off puxado por petróleo e juro longo, o capital que sai da bolsa não vai para emergentes, e os pares latinos já se depreciaram em setembro com a bolsa parada.
- Onde entra: limite da cauda de depreciação do real no risk-off (do câmbio).

**(i) `dxy_em` — efeito mais forte que o estimado** · cenário risk-off
- O multiplicador é do câmbio (`F.b_dxy_em`).
- Coeficiente: estimado 2,262, intervalo de 90% 1,138 a 3,315. Proposta: × 1,3, dentro do intervalo.
- Por quê: com o Fed subindo e o carry dos pares caindo (México e Chile parados), o real, que tem o maior juro real da amostra, é a moeda que tem mais posição a desmontar; isso é hipótese, que XS2 (posição e fluxo) confirma ou derruba.
- Onde entra: probabilidade da cauda de depreciação do real (do câmbio).

**(ii) Juro longo americano e prêmio de prazo — Treasury de 10 anos** · cenário base e upside do Fed
- Hoje: 5,28% (`us_interest_rate`, 02/10); juro real ex-ante 2,70%.
- Por que o modelo não vê: nenhum juro longo americano está no modelo; chega ao Brasil pelo `rr_10a`, que não escrevo.
- Efeito: pressão de alta no `rr_10a` enquanto o 10 anos ficar acima de 5%; na base, cede ~0,5 p.p. até o 1T28; no upside do Fed, sobe a 5,6–5,7%.
- Onde entra: o caminho do `rr_10a` de quem o escreve (XS6).

**(ii) Energia e combustíveis — Brent** · todos os cenários de commodities
- Hoje: US$ 135,51 (`comm_brent`, 02/10); média de setembro US$ 114.
- Por que o modelo não vê: a energia não está na curva de Phillips; chega pelos combustíveis e pelos preços administrados.
- Efeito: alta de combustíveis no 4T26 e no 1T27 na base, maior no upside; direção de devolução a partir do 2T27.
- Onde entra: tempero da inflação (é o único caminho de petróleo do ciclo).

**(ii) Componente global do CDS** · risk-off
- Hoje: 131 p.b. (`cmb_risco_pais`, 02/10), +9 p.b. em setembro, junto com o dólar EM.
- Por que o modelo não vê: o modelo lê o CDS como fiscal; a parte global depende da trajetória que o fiscal escrever.
- Efeito: no risk-off, um CDS parado subestima a depreciação; a régua que vejo é o setembro de 2026 (+9 p.b. com o dólar EM +2,0%).
- Onde entra: a trajetória do CDS do fiscal (XS5).

**(ii) Ciclo dos pares** · base
- Hoje: Colômbia 12,25% e subindo; México, Chile e Peru parados (`inter_interest_rate`, 02/10).
- Por que o modelo não vê: o modelo não tem os pares.
- Efeito: carry relativo do Brasil maior com o Fed subindo e os pares parados.
- Onde entra: leitura da política monetária e do câmbio.

### 3.3 Da etapa 1 à tese

As centrais são os caminhos base. Para cada bloco, a faixa base fica entre o caminho base e os caminhos das caudas, e a probabilidade da faixa é a do cenário base (50%), com duas exceções: o `ffr` do 4T26, em que o downside (um corte já em dezembro) é muito menos provável do que o cenário de downside inteiro (5% contra 20%), e o `infl_us` de 3T27 em diante, em que os cenários convergem pelo núcleo e a faixa absorve mais probabilidade (60%). No bloco de risco, a cauda de cima do `dxy_em` e a de baixo do `sp500` são o mesmo cenário (30%). No de commodities, as caudas são simétricas (25% cada): o petróleo pode durar mais que a base e pode devolver como em junho, e não tenho dado para pesar um mais que o outro.

## 4. Para os outros agentes

**Respostas às entradas fixas (Parte 4 do mapa).**
- XE1 (câmbio), **em destaque**: os caminhos do bloco global da (F) são os da seção 3.1. Destaque porque o dólar EM subiu 2,0% em setembro com o Fed subindo, e porque no modelo o risk-off quase não move o real: o câmbio decide se aplica os temperos (i) da seção 3.2.
- XE2 (câmbio), **em destaque**: dólar contra desenvolvidos +2,4% em um mês (DXY 101,93); bolsa na máxima; pares latinos todos depreciados em setembro; Colômbia subindo, os outros parados; Brent a US$ 135,51, movimento sustentado de petróleo.
- XE3 (política monetária), **em destaque**: o Fed subiu 25 p.b. em 17/09; base com mais uma alta no 4T26, upside (30%) com o efetivo a 4,88% em jun/27; os bills precificam o upside.
- XE4 (inflação): agro na base estável (200,8 no 4T26 a 197,8 no 1T28) e metal estável (335,7 a 325,8); sem mudança material contra o último publicado.
- XE5 (inflação), **em destaque**: Brent base US$ 124 de média no 4T26, US$ 110 no 1T27 e US$ 90 no 1T28; upside US$ 143 no 4T26; downside US$ 85 no 1T27. Bens no CPI americano a 0,9% anualizados em três meses até agosto: o ciclo global de bens não está quente.
- XE6 (atividade): sem dado de PIB de parceiros; o que há é emprego americano fraco (51 mil vagas por mês), metais estáveis e exportação para a China de US$ 109 bi em 12 meses até setembro. Probabilidade de recessão global: não tenho como medi-la; o cenário mais próximo é o downside de commodities (25%).
- XE7 (atividade): os três IC-Br e o Brent na seção 3.1; o que se moveu é energia.
- XE8 (atividade): Fed na seção 2.1, risk-off com 30%.
- XE9 (fiscal), **em destaque**: o CDS subiu 9 p.b. em setembro junto com o dólar EM e os pares; vejo componente global nesse movimento, sem spread de emergentes para medi-lo. No risk-off (dólar EM 134,5), um CDS parado é inconsistente com o bloco.
- XE10 (fiscal), **em destaque**: Treasury de 10 anos 5,28%, +0,84 p.p. desde junho, máxima de dez anos; caminho base 5,25% no 4T26 a 4,80% no 1T28.
- XE11 (fiscal), **em destaque**: Brent a US$ 135,51 (royalties e dividendos); IC-Br total 207,2 em dez/26 na base.
- XE12 (expectativas), **em destaque**: choque de petróleo que a base trata como persistente por dois trimestres; inflação esperada americana de um ano subindo (2,40% em agosto, 2,66% em setembro).

**Pedidos (saídas fixas XS1–XS8 e deste ciclo).**
- XS1, câmbio: quanto da depreciação do real em setembro foi global e quanto foi própria, contra os pares e o dólar EM? Depende disso o peso do risk-off (30%) e o tempero de `F.b_dxy_em`.
- XS2, câmbio: os fundos alavancados reduziram a posição em BRL em setembro (`cmb_cot_fx` mostra −5,2 mil contratos em um mês até 29/09): isso é desmonte de carry por causa do Fed? Depende disso o tempero (i) de `F.b_dxy_em`.
- XS3, política monetária: a trajetória da Selic; com o Fed subindo e os pares parados, o diferencial se abre ou o Copom corta mais? Depende disso a leitura de carry relativo (2.2).
- XS4, política monetária: o Copom de setembro mudou a avaliação do cenário externo ou o condicionante de petróleo? Depende disso se o choque de energia é notícia para o Copom.
- XS5, fiscal: a trajetória do CDS e a parte que o fiscal atribui ao global; no risk-off deste report, qual CDS o fiscal escreve? Depende disso a consistência do bloco de risco com a (F).
- XS6, quem escreve o `rr_10a`: a trajetória e quanto dela vem do Treasury de 10 anos (+0,84 p.p. desde junho). Depende disso o tempero (ii) de juro longo.
- XS7, inflação: em quais trimestres a tese do IPCA depende de agro, metal ou energia? A base de energia é a que mais pode errar.
- XS8, expectativas: o QPC de setembro tem 67% vendo o externo menos favorável; o Focus já incorpora petróleo mais caro?
- Pedido deste ciclo, câmbio: com a vol implícita segurada em 12,19% (2T26), o carry no modelo não registra o aumento de volatilidade de setembro; qual vol o câmbio escreve para o 4T26?

**Divergências:** rodada 1, nenhuma.

## 5. Placar

Primeiro ciclo.

## 6. Sobre o modelo

| Fonte | O que sugere | Teste proposto | Por que importa para a tese deste ciclo |
|---|---|---|---|
| Dado e mapa (2.5), sem literatura | O sinal condicional do S&P na (F) pode depender do tipo de risk-off | Reestimar a (F) com o S&P interagido com uma dummy de trimestre de risk-off (S&P ≤ −8% e dólar EM ≥ +3%), 2006–3T26; se o coeficiente cair à metade ou menos nesses trimestres, a especificação linear compensa demais | No risk-off deste report o modelo deprecia o real só 0,5% no 4T26, porque a bolsa compensa o dólar |
| Dado e mapa (2.6) | O Brent em reais, ou o grupo energia do IC-Br, nos preços monitorados | Somar a variação do Brent em reais (corrente e defasada) à equação dos monitorados e testar a significância e o ganho de ajuste, 2006–3T26 | Com o Brent a US$ 135,51, o canal que mais move o IPCA de curto prazo está fora do modelo |
| Dado e mapa (2.2) | O juro real de 10 anos americano como parte da âncora `rr_10a` | Regredir a variação trimestral do `rr_10a` na do Treasury real ex-ante de 10 anos e no CDS, 2006–3T26; se o coeficiente americano for significativo com o CDS na regressão, a âncora tem componente externo que hoje ninguém escreve | O juro real americano subiu 0,73 p.p. desde junho e o `rr_10a` está no padrão |

[^corte]: O F corta as tabelas pela data de referência. Pelo calendário de divulgação, quatro dados do F não existiam em 02/10: o CPI de setembro (divulgado em 14/10; núcleo de setembro +0,33% no mês e CPI cheio de 12 meses de 3,72%), o IC-Br de setembro (07/10; total 205,7, energia 96,0), a inflação esperada de outubro (publicada no meio do mês; 1 ano a 2,98%) e, com eles, o CPI de 12 meses e o juro real ex-post de setembro em `diferenciais_juros`. A argumentação usa o CPI e o IC-Br até agosto e a inflação esperada até setembro. O que não deu para separar: o ponto de partida do modelo (3T26 observado) já contém o CPI e o IC-Br de setembro. Para conferir, projetei setembro com a informação de 02/10: o IC-Br sairia 206,3 (publicado 205,7) e o `infl_us` do 3T26 0,97% (publicado 1,12%).

[^conv]: O `ffr` é o Fed funds efetivo na média do último mês do trimestre, e não o ponto médio da meta, porque é o que entra no carry da equação do câmbio; o `infl_us` é a variação do CPI no trimestre (100·Δlog, sem anualizar), porque a equação compara a inflação de um trimestre aqui e lá. Os 12 meses que a imprensa cita são outra coisa.

[^pctl]: Percentil 10 em dez anos quer dizer que só 10% dos meses da década tiveram taxa de pedidos de demissão menor que a de agosto: quanto menor, menos gente se sente segura para trocar de emprego.

[^bills]: Um T-bill de 3 meses rende, grosso modo, a média do juro do Fed nos próximos três meses mais um prêmio pequeno. Se ele rende 0,3 p.p. acima do juro de hoje, a média esperada está 0,3 p.p. acima; com um caminho que sobe em linha reta, isso dá ~0,6 p.p. no fim do prazo, duas altas de 25 p.b. A conta tem incerteza: não há futuros de Fed funds no banco.

[^tp]: Prêmio de prazo é o que o investidor pede a mais para ficar com um título longo em vez de rolar títulos curtos: se o juro curto esperado nos próximos dez anos é 4% e o título de dez anos paga 5%, o prêmio é ~1 p.p. Sobe com incerteza de inflação e oferta de títulos.

[^dxyem]: O dólar contra emergentes é um índice do Fed que mede o dólar contra uma cesta de moedas de emergentes, com o real dentro dela; subir quer dizer dólar mais forte.

[^realexpost]: O juro real ex-post é o juro de política menos a inflação dos últimos 12 meses; um país em desinflação parece mais apertado do que está.

[^icbr]: O IC-Br é o índice de commodities do Banco Central, uma cesta de agropecuária, metais e energia com os preços relevantes para o Brasil. Os pesos não estão no banco; os ~66%, ~19% e ~17% são estimados da variação mensal do índice contra a dos grupos, que reproduz o total com R² de 0,99.

[^ffr]: Em setembro o efetivo foi 3,63% até 17/09 e ~3,89% depois, o que dá a média de 3,75% publicada.
