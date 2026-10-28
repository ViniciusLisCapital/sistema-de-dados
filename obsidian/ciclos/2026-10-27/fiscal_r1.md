# Report — fiscal · ciclo 2026-10-27 · rodada 1

Dados até: 26/10/2026 nos preços (CDS, curvas, PTAX); ago/2026 nas contas fiscais (RTN, NFSP, DLSP); 2T26 no governo geral (EFGG) e no PIB · Horizontes: 4T26 a 1T28, o CDS de 5 anos no fechamento do trimestre (`fiscal`) e a NTN-B de 10 anos na média do trimestre (`rr_10a`)[^proc]

## 1. Tese

| Variável | Trimestre | Central | Base: faixa · P | Upside: limite · P | Downside: limite · P | P(up) − P(down) |
|---|---|---|---|---|---|---|
| CDS 5 anos, fechamento (p.b.) | 4T26 | 140 | 125 a 160 · 60% | acima de 160 · 25% | abaixo de 125 · 15% | +0,10 |
| | 1T27 | 140 | 122 a 168 · 55% | acima de 168 · 28% | abaixo de 122 · 17% | +0,11 |
| | 2T27 | 138 | 118 a 172 · 55% | acima de 172 · 28% | abaixo de 118 · 17% | +0,11 |
| | 3T27 | 135 | 115 a 172 · 54% | acima de 172 · 28% | abaixo de 115 · 18% | +0,10 |
| | 4T27 | 135 | 110 a 175 · 54% | acima de 175 · 28% | abaixo de 110 · 18% | +0,10 |
| | 1T28 | 135 | 108 a 178 · 54% | acima de 178 · 28% | abaixo de 108 · 18% | +0,10 |
| `rr_10a`, NTN-B 10 anos, média (% a.a.) | 4T26 | 7,70 | 7,45 a 7,95 · 60% | acima de 7,95 · 22% | abaixo de 7,45 · 18% | +0,04 |
| | 1T27 | 7,80 | 7,30 a 8,30 · 55% | acima de 8,30 · 27% | abaixo de 7,30 · 18% | +0,09 |
| | 2T27 | 7,70 | 7,15 a 8,30 · 55% | acima de 8,30 · 27% | abaixo de 7,15 · 18% | +0,09 |
| | 3T27 | 7,60 | 7,05 a 8,30 · 54% | acima de 8,30 · 28% | abaixo de 7,05 · 18% | +0,10 |
| | 4T27 | 7,55 | 6,95 a 8,30 · 54% | acima de 8,30 · 28% | abaixo de 6,95 · 18% | +0,10 |
| | 1T28 | 7,50 | 6,90 a 8,30 · 54% | acima de 8,30 · 28% | abaixo de 6,90 · 18% | +0,10 |

Nas duas variáveis, **o upside é a cauda ruim para o Brasil**: CDS e juro real mais altos são o mercado cobrando mais pelo risco da dívida.

- **Acima da faixa** (upside, 25–28%) se as decisões fiscais de 2027 confirmarem a leitura que os preços fizeram em 26/10 e a afrouxarem explicitamente (regra mudada, despesa fora do limite, mais crédito do Tesouro a bancos oficiais): CDS a 165 em 4T26 e 190–200 em 2027, `rr_10a` a 8,80–9,00 em 2027. No modelo, a PTAX vai a 5,52 em 2T27 e a Selic média a 14,2% em 1T27 (seção 3.1).
- **Abaixo da faixa** (downside, 15–18%) se o que os preços leram em 26/10 for desfeito por um arcabouço de 2027 que o mercado compre, como ele já mostrou que compra: entre 05/10 e 23/10 o CDS ficou entre 109 e 119 e a NTN-B 10a entre 6,70 e 7,01 (`cmb_risco_pais`, `br_interest_rate`). Caminho: CDS 115 → 105, `rr_10a` 7,35 → 6,70. No modelo, PTAX 5,16–5,21 e Selic média de 12,3% em 1T27.

**A tese em uma frase:** o choque de 26/10 foi doméstico e caiu muito mais na curva local e no real do que no CDS; a base mantém o CDS perto de 140 até meados de 2027 e devolve a NTN-B 10a ao nível médio de 3T26 (~7,8%) em 1T27, caindo devagar depois, com a cauda de alta (a ruim) mais provável que a de baixa porque as contas sustentam mais a leitura de 26/10 do que a de 05/10.

## 2. Argumentação

### O que aconteceu em outubro (o contexto de F5, primeiro)

Dois fins de semana moveram todos os preços domésticos, em sentidos opostos, e o segundo movimento foi maior. O F não diz o que aconteceu neles; o fato está pedido ao agente web (seção 4, W1).[^eleicao]

| Preço | 05/10 contra 02/10 | 26/10 contra 23/10 | 26/10 contra 30/09 |
|---|---|---|---|
| CDS 5 anos (p.b.) | −12,2 | +18,2 | +6,2 |
| NTN-B 10 anos (p.b.) | −50 | +135 | +50 |
| DI 10 anos (p.b.) | −134 | +239 | +116 |
| DI 1 ano (p.b.) | −70 | +172 | +115 |
| Inflação implícita 10 anos[^impl] (%) | 6,18 → 5,42 | 5,66 → 6,55 | 5,97 → 6,55 |
| PTAX (%) | −4,55 | +9,19 | +6,17 |
| Peso mexicano · chileno · colombiano (%) | −1,0 · +0,1 · −1,0 | sem dado no F | — |
| Dólar contra emergentes · S&P 500 (%) | −0,4 · +0,7 | sem dado · +0,7 | — |

Fontes: `cmb_risco_pais`, `br_interest_rate`, `cmb_ptax`, `cmb_fx_latam`, `cmb_dollar_index_em`, `cmb_equity_us`, pregões de 02/10, 05/10, 23/10 e 26/10.

Os dois movimentos foram domésticos: em 05/10 o real andou 4,55% e os pares em torno de 1%, e em 26/10 a bolsa americana subiu 0,7% enquanto o real caiu 9,2%. **A alta de 135 p.b. da NTN-B 10a em 26/10 é o maior salto de um pregão desde 2006**; o maior anterior, 106,5 p.b., foi em 18/05/2017 (`br_interest_rate`, desde 2006). Mas o pedaço global do mês não é zero: de 30/09 a 20/10 o peso mexicano se depreciou 2,2% e o dólar contra emergentes subiu 1,6% em um mês até 23/10 (`cmb_fx_latam`, `cmb_dollar_index_em`), e os pares de 26/10 não estão no F. A divisão fina é do câmbio (FS-CB1) e do externo (FS-EX1).

### F1 — A postura: a política fiscal está expandindo a demanda, pouco pelo primário e muito pelo crédito

A postura de 2026 é expansionista, e a maior parte do empurrão não passa pelo primário. Quatro medidas, que discordam por um motivo identificável:

| Medida (p.p. do PIB, + = expansionista) | Até | Impulso | Leitura |
|---|---|---|---|
| Setor público consolidado, primário 12m (NFSP), em 12 meses | ago/26 | +0,43 | expansão moderada |
| Governo central, primário 12m (RTN), em 12 meses | ago/26 | +0,29 | expansão moderada |
| Governo central sem precatórios, em 12 meses | ago/26 | +0,28 | a mesma, sem o calendário dos precatórios |
| Governo central, em 3 meses | ago/26 | −0,53 | contração aparente: é calendário |
| Governo central sem precatórios, em 3 meses | ago/26 | −0,05 | neutro |
| Governo geral (EFGG), despesa exceto juros, em 1 ano | 2T26 | +1,95 | expansão forte, metade é precatório |
| Parafiscal: crédito do Tesouro a instituições oficiais, em 1 ano | ago/26 | +0,89 | expansão pelo crédito |

Fontes: "O impulso fiscal em quatro medidas" do F (`fisc_nfsp`, `fisc_rtn`, `fisc_efgg`, `fisc_dlsp_fatores`) e, sem precatórios, `fisc_rtn` com o PIB de `atv_pib_mensal`, até ago/26.[^impulso][^prim]

- **As medidas de 12 meses concordam** (+0,3 a +0,4 p.p.), com ou sem precatórios[^prec], porque as duas janelas carregam um pagamento grande: R$ 63,7 bi em jul/25 e R$ 71,4 bi em mar/26 (`fisc_rtn`).
- **A de 3 meses discorda por calendário, não por decisão:** a melhora de 0,52 p.p. do primário 12m entre mai/26 e ago/26 (`fisc_nfsp`, de −1,14 para −0,62) vem de julho, quando saiu da janela o pagamento de jul/25; o primário do governo central de jul/26 foi de +R$ 10,8 bi contra −R$ 59,1 bi em jul/25 (`fisc_rtn`). Sem precatórios, os três meses são neutros (−0,05).
- **A EFGG exagera pelo mesmo motivo:** a janela de quatro trimestres até 2T26 carrega precatórios de 1,30% do PIB, contra 0,32% na janela anterior (`fisc_rtn`), o que responde por +0,98 dos +1,95 p.p. O resto (+0,97) é maior que o das medidas acima da linha porque a EFGG soma três esferas sem consolidar as transferências entre elas, e estados e municípios pioraram: o primário deles em 12 meses foi de +0,12% do PIB em ago/25 para −0,04% em ago/26 (`fisc_nfsp`).
- **O parafiscal é o maior empurrão isolado:** o estoque de crédito do Tesouro a instituições oficiais (todo ele ao BNDES) passou de R$ 106,7 bi para R$ 232,9 bi em 12 meses até ago/26, de 0,86% para 1,75% do PIB (`fisc_dlsp_fatores`), em duas ondas, set–dez/25 (+R$ 50 bi) e mai–ago/26 (+R$ 85 bi).[^para] Crédito não é gasto: ele vira demanda quando é desembolsado. O saldo do BNDES cresceu 10,3% e o crédito direcionado 12,9% em 12 meses, contra 9,2% do crédito total, e o direcionado foi a 24,4% do PIB, +1,2 p.p. (`cred_modalidade_direcionado_pj`, `cred_credito_resumo`, ago/26, TWA, premissa assumida). Mas os bancos públicos não lideram o crédito (+8,2% contra +10,0% dos privados nacionais, `cred_credito_controle_capital`), então o canal passa pelo BNDES e pelo direcionado, não pela carteira dos bancos públicos em geral.

Por grupo de despesa, a expansão está na parte que o governo liga e desliga. Crescimento real em 12 meses até ago/26, deflator IPCA (`fisc_rtn`; para as funções, a mesma tabela por item):

| Grupo (governo central, RTN) | Real 12m (%) | 2T26 contra 2T25 (%) |
|---|---|---|
| Discricionárias do Executivo | +34,6 | +54,0 |
|   dessas, saúde · educação · assistência | +68,9 · +43,8 · +49,5 | — |
| Investimento federal pago (GND 4) | +25,5 | — |
|   dele, transferências a municípios | +70,4 | — |
| Pessoal e encargos | +5,2 | +3,6 |
| BPC/LOAS | +5,0 | +3,8 |
| Benefícios previdenciários | +3,7 | +3,2 |
| Bolsa Família | −10,2 | −9,5 |
| Despesa total | +5,6 | +7,3 |
| Receita líquida | +4,0 | +7,1 |

Fontes: `fisc_rtn` e `fisc_investimento`, até ago/26.

A despesa discricionária cresce acima de tudo o mais (+R$ 64 bi em 12 meses, a preços de ago/26), e saúde responde por quase metade (+R$ 31 bi). A transferência a famílias cresce menos: Bolsa Família cai 10,2% real, e previdência e BPC andam a 4–5%. O RTN registra ainda R$ 5,0 bi de financiamento de campanha eleitoral nos 12 meses, contra zero um ano antes. Mas jul–ago/26 mostram a despesa total 11,2% abaixo de jul–ago/25 em termos reais, e as discricionárias 15,8% abaixo (`fisc_rtn`); o recuo é dois meses de dado, contra a base de jul/25 inflada pelos precatórios, e só diria que o empurrão está acabando se setembro e outubro o repetirem.

Contra o ciclo: o hiato do BC caiu de 1,47% do potencial em 4T24 para 0,41% em 3T26 (`pm_hiato_produto`, edição de set/26, percentil[^pct] 57 no histórico). Uma postura que expande com o hiato ainda positivo é pró-cíclica; quanto ela pesa no hiato é do agente de atividade (FS-AT1).

### F2 — Por onde chega ao hiato e à inflação, e o caminho do impulso

**A demanda do governo cresce acima do PIB.** O consumo do governo subiu 3,1% contra 2T25 e o PIB 2,0% (`atv_pib_taxas`, 2T26), e a participação dele no PIB foi de 18,7% para 19,6% em quatro trimestres (`atv_pib_valores_correntes`). O dado é de 2T26 (209 dias antes do corte) e é do agente de atividade; aqui ele confirma pelo lado das contas nacionais a direção que as contas fiscais dão.

**Transferências** crescem menos que o gasto total (acima), então o canal da renda das famílias é o mais fraco dos três neste ciclo.

**Impostos e preços administrados:** o F não traz decisão de governo sobre preços. Os monitorados de 12 meses caíram de 5,52% para 4,14% em três meses, com 1,59% em setembro (`inflc_agregados`), e o Brent está em US$ 115, +89,8% em 12 meses (`comm_brent`, 20/10). Com o petróleo nesse nível, uma decisão sobre tributo ou subsídio de combustível é o choque fiscal mais provável sobre o IPCA no horizonte; ela não está no F e foi pedida ao agente web (W4). Do lado da receita, o petróleo ajuda: as receitas de exploração de recursos naturais cresceram 19,4% real em 12 meses (`fisc_rtn`).

**O caminho do impulso, por trimestre** (premissa deste agente, seção 4): moderadamente expansionista em 4T26 e neutro a contracionista em 2027, condicionado ao que se decidir para 2027. A base é a mediana Focus de 23/10, que é **anterior a 26/10**: primário de −0,48% do PIB em 2026, −0,30% em 2027 e 0,00% em 2028 (`expc_focus_periodo`), o que dá impulso de +0,05 p.p. em 2026, −0,18 em 2027 e −0,30 em 2028 contra o primário de −0,43% de 2025 (`fisc_nfsp`, dez/25). Para chegar a −0,48% em dezembro, set–dez/26 precisam ser 0,14 p.p. do PIB melhores que set–dez/25, o que pede que o empurrão discricionário desacelere no fim do ano.

### F3 — O policy mix

Em 2026, a política fiscal adicionou demanda (acima) enquanto o Copom cortou a Selic de 15,00% para 13,75% em cinco reuniões desde mar/26 (`pm_copom_reuniao`). As duas empurram a demanda para o mesmo lado na margem: a fiscal acelerando, a monetária retirando aperto. Uma postura fiscal expansionista pede uma Selic mais alta para o mesmo resultado de inflação; se a Selic atual ainda é restritiva o bastante é do agente de PM (FS-PM1), e como o Copom lê a política fiscal também (FS-PM2).

No modelo, o mix entra pela `rr_10a`, que subiu de 7,40% em 2T25 para 7,84% em 3T26 na média do trimestre (`br_interest_rate`): o juro neutro do modelo subiu junto. Em 26/10 a curva de um ano foi a 14,69%, 94 p.b. acima da Selic, contra 12,97% em 23/10 (`br_interest_rate`), o que é compatível com alta de juros precificada; a leitura é do PM.

### F4 — As contas e a dívida

**Resultado.** O primário do setor público consolidado em 12 meses é de −0,62% do PIB e o do governo central, −0,53% (`fisc_nfsp`, ago/26; negativo = déficit), contra −0,19% e −0,24% um ano antes. Com juros nominais de 8,86% do PIB, percentil 100 em 10 anos, o resultado nominal é de −9,48% (`fisc_nfsp`). Os juros pesam 1,25 p.p. do PIB a mais que um ano antes.

**Estrutura da receita.** A receita administrada pela RFB cresce 6,1% real e a do RGPS 6,7%, com o IOF a +27,8%; a não administrada cai 8,9%, puxada por dividendos (−49,4%, BNDES −51,5% e Petrobras −48,0%) e concessões (−61,0%) (`fisc_rtn`, 12 meses até ago/26). O resultado se apoia em receita recorrente, não em extraordinária, o que é bom para a qualidade do ajuste, mas a receita líquida (+4,0%) cresce menos que a despesa (+5,6%).

**A regra.** As metas, a banda e o limite de despesa não estão no F, e este report não escreve nenhuma de memória (pedido W5). Contra o consenso, o primário de 12 meses (−0,62%) está 0,14 p.p. abaixo da mediana Focus para 2026 (−0,48%)[^focus]. O Focus melhorou o primário de 2028 de −0,30% para 0,00% e o de 2029 de −0,15% para +0,10% nas quatro semanas até 23/10 (`expc_focus_periodo`), na janela do otimismo de 05/10; a revisão depois de 26/10 é o primeiro dado a pedir (FS-EP1).

**A dívida.** A dívida líquida (DLSP) está em 69,3% do PIB e a bruta (DBGG) em 82,9%, +5,2 e +5,6 p.p. em 12 meses, a DLSP no percentil 100 do histórico (`fisc_divida`, ago/26).[^div] O que moveu a DLSP em 12 meses (`fisc_dlsp_fatores`, + = aumenta a dívida): juros, R$ 1.182 bi (8,86% do PIB); primário, R$ 82 bi (0,62%); ajuste cambial da dívida externa, +R$ 60,5 bi (0,45%), com o real mais forte (PTAX de 5,43 no fim de ago/25 para 5,18 no fim de ago/26, `cmb_ptax`), porque o setor público é credor líquido em moeda estrangeira; privatizações e ajuste caixa-competência abateram R$ 17 bi cada.

O juro implícito nominal da DLSP é de 13,8% ao ano sobre o estoque médio de 12 meses, 9,2% real deflacionado pelo IPCA de 12 meses, contra crescimento nominal do PIB de 7,2% (`fisc_dlsp_fatores`, `atv_pib_mensal`, `inflc_agregados`, ago/26). **Com esses números, o primário que estabiliza a DLSP é de 4,3% do PIB, a 4,9 p.p. do primário de hoje**; com juro implícito 1 p.p. menor, 3,6%, e com PIB nominal crescendo 1 p.p. a mais, 3,6%. O Focus de 23/10 projeta a DLSP a 74,0% em 2027 e 79,1% em 2029 (`expc_focus_periodo`): o consenso não vê estabilização no horizonte.

Outubro mexe nas contas pelos dois lados. O real mais fraco reduz a DLSP pelo ajuste cambial, porque as reservas valem mais em reais. Mas o BC tinha US$ 91,6 bi vendidos em swap em ago/26 (`cmb_reservas_bc`), e a alta da PTAX de 23/10 para 26/10 implica um resultado de swap da ordem de −R$ 42 bi (0,32% do PIB), que entra nos juros nominais e piora o resultado nominal de out/26.[^swap]

### F5 — O preço do risco e a tese

**O que é fiscal e o que é global no CDS.** O CDS fechou 3T26 em 131 (`cmb_risco_pais`), 6 p.b. acima de 2T26 (125). A alta concentrou-se em 17/09–30/09 (+20 p.b.), com o peso mexicano +5,5% e o dólar contra emergentes +1,5% (`cmb_fx_latam`, `cmb_dollar_index_em`), o que aponta componente global ou regional. Mas o salto de 21/09 (+9,3 p.b. em um pregão) veio com o real **mais forte** (−0,9%) e o DI 10a 13 p.b. mais baixo (`cmb_ptax`, `br_interest_rate`), o que não é um movimento fiscal; pode ser a emenda entre a carga da Bloomberg e o trecho provisório de outra fonte.[^cds] Em outubro, os dois saltos foram domésticos (tabela acima). Desde o ciclo anterior (02/10), o CDS subiu 6 p.b.

**O CDS reagiu pouco a um choque grande.** Em 26/10 o real caiu 9,2% com o CDS subindo 18 p.b.; no Modelo Estrutural, um CDS 18,2 p.b. mais alto deprecia a PTAX de 4T26 em 1,55%. O real andou 5,9 vezes o que o CDS explica no modelo; em 05/10, 4,4 vezes. O choque de 26/10 foi precificado como risco de inflação e de juro local, não de calote em dólar: a inflação implícita de 10 anos subiu 0,89 p.p. num pregão, para 6,55%, e a NTN-B 10a foi a 8,05%, percentil 99 nos últimos 10 anos (`br_interest_rate`), enquanto o CDS de 137 está no percentil 17 em 10 anos (`cmb_risco_pais`). Daí o argumento ao câmbio sobre o peso do CDS (seção 4).

**Que caminho fiscal o mercado precifica, contra F1–F4.** Entre 05/10 e 23/10 os preços e o Focus precificavam convergência: CDS de 109–119, NTN-B 10a de 6,70–7,01 e o Focus melhorando o primário de 2028–29. Em 26/10 os preços passaram a precificar um caminho pior que o de setembro: NTN-B 10a 50 p.b. acima de 30/09, inflação implícita 0,58 p.p. acima. As contas sustentam mais a segunda leitura: o impulso virou positivo em 2026, o parafiscal cresceu 0,89 p.p. do PIB, o primário está 4,9 p.p. abaixo do que estabiliza a dívida e a dívida sobe 5 p.p. por ano. Mas a QPC registrou só 17% de respostas de piora fiscal na reunião de setembro, contra 50% em junho (`expc_qpc`, 23/09), e é anterior aos dois choques. É por isso que a base não devolve o CDS a 125 e não leva a NTN-B ao nível de 05/10–23/10.

**Por que a base não aposta na reversão que o histórico sugere.** Depois dos 52 saltos diários do CDS de 15 p.b. ou mais desde 2006, a mediana da variação adicional em 63 pregões foi de −34,7 p.b., e 62% deles devolveram mais da metade do salto; nos cinco saltos da NTN-B 10a de 40 p.b. ou mais, todos devolveram mais da metade em 63 pregões (`cmb_risco_pais`, `br_interest_rate`, 2006–set/26). Esses episódios partiram, em geral, de CDS bem mais alto (mediana perto de 220) e muitos foram choques globais revertidos por política global (2008–09, 2020). O de hoje é doméstico, parte de um CDS baixo e encontra a dívida em alta. A regularidade entra na base como uma devolução parcial da NTN-B até 1T27 (de 8,05% para ~7,8%) e na probabilidade da cauda de baixa, não como a central.

**Dominância fiscal: dois dos três conjuntos de sinais estão presentes, nenhum completo.**[^dom]
- *Sustentabilidade fiscal: presente.* Primário 4,9 p.p. abaixo do que estabiliza a DLSP, juro real implícito de 9,2%, DLSP no maior nível do histórico e subindo 5 p.p. por ano, e um consenso que não vê estabilização até 2029.
- *Mercado: presente nos preços locais, ausente no CDS e nas expectativas longas.* A inflação implícita de 10 anos subiu com a notícia de 26/10 e o real caiu 9,2%. Mas o CDS está no percentil 17 de 10 anos, e o Focus de IPCA para 2029–2030 seguia em 3,50% em 23/10 (`expc_focus_periodo`), antes do choque. O teste decisivo, o real se depreciar quando o Copom sobe juros, não ocorreu: não há alta de juros no F.
- *Regime monetário: sem sinal no F.* O Copom cortou 25 p.b. em 16/09 (`pm_copom_reuniao`); se ele vai reagir como de costume ao choque é do PM (FS-PM4).

A cauda de dominância é a parte mais extrema do upside: a coloco em cerca de 10% no horizonte (dentro dos 25–28% da cauda de alta), condicionada a uma decisão fiscal explícita de afrouxamento mais uma reação monetária que o mercado leia como insuficiente.

**A central.** Para o CDS, 140 em 4T26 a 2T27 (cerca de 3 p.b. acima do último dado) e 135 a partir de 3T27: o prêmio novo fica enquanto as decisões de 2027 não saem e devolve 5 p.b. depois, sem ruptura e sem consolidação crível. Para a `rr_10a`, 7,70% em 4T26: os 17 pregões de outubro já fizeram média de 6,99% (o F, "O preço do risco na convenção do modelo"), e os ~43 restantes a cerca de 7,95% dão 7,70.[^q4] Depois, 7,80% em 1T27, o nível médio de 3T26, e queda de 0,3 p.p. ao longo de 2027, que supõe o ciclo de corte da Selic retomado e o juro americano parado (aguarda PM, FS-PM3, e externo, FS-EX2).

**As faixas e as caudas.** A faixa da base cobre a variação dos últimos 10 anos com folga menor que a interquartil histórica no primeiro trimestre (no CDS, a variação de um trimestre teve p25–p75 de −35 a +9 p.b.; na `rr_10a`, de −0,25 a +0,33 p.p., `cmb_risco_pais`, `br_interest_rate`, 2016–2026) e se abre com o horizonte. A cauda de alta é mais provável que a de baixa nas duas variáveis pelos três motivos acima: as contas estão do lado da leitura de 26/10; o juro americano está alto, com o Treasury de 10 anos a 5,00% (`us_interest_rate`, 23/10, do externo); e a ruptura de 26/10 é recente o bastante para não ter sido testada por nenhuma decisão. O que mantém a cauda de baixa em 15–18%, e não menos, é o próprio mercado ter mostrado em três semanas de outubro o preço da consolidação.

**O que derrubaria a tese** (signposts):
- CDS acima de 160 por dez pregões, ou NTN-B 10a acima de 8,50% por dez pregões: a cauda de alta passa a ser a base.
- NTN-B 10a abaixo de 7,20% e CDS abaixo de 120 por dez pregões: a cauda de baixa ganha probabilidade.
- Focus de primário de 2027 revisado para abaixo de −0,50% do PIB, ou de IPCA de 2029 acima de 3,50%: o sinal de mercado da dominância deixa de ser só preço local.

**Olhado, sem sinal.**
- Primário das estatais · −0,04% do PIB em 12m (`fisc_nfsp` · ago/26) · pequeno e estável · diria algo se capitalizações virassem déficit relevante.
- DLSP de estados e municípios · 8,1% do PIB, Δ 12m de 0,0 (`fisc_divida` · ago/26) · parada · diria algo com renegociação de dívida subnacional.
- Subsídios, subvenções e Proagro · −0,8% real em 12m (`fisc_rtn` · ago/26) · sem movimento · diria algo com equalização nova para crédito direcionado.
- Inversões financeiras (GND 5) · −7,8% real (`fisc_investimento` · ago/26) · não é demanda e caiu · diria algo com capitalização de estatal.
- Inadimplência dos bancos públicos · 4,67%, +1,10 p.p. em 12m (`cred_credito_controle_capital` · ago/26, TWA) · subiu, mas os privados também (+0,77) · diria algo sobre risco parafiscal se descolasse dos privados.
- Focus de resultado nominal · −8,93% em 2026 e −8,50% em 2027 (`expc_focus_periodo` · 23/10) · estável, e anterior a 26/10 · diria algo se a revisão pós-choque passasse de 0,5 p.p.
- Reservas internacionais · US$ 364,9 bi (`cmb_reservas_bc` · 26/10) · −US$ 4,0 bi em 3 meses · diria algo com venda à vista do BC, que entraria no ajuste da DLSP.
- Reconhecimento de dívidas · R$ 8,2 bi em 12m, 0,06% do PIB (`fisc_dlsp_fatores` · ago/26) · pequeno · diria algo com um esqueleto novo.

## 3. Premissas

### 3.1 Etapa 1 — o modelo

**Cenários.**
- **Base:** o que os preços leram em 26/10 (fato pedido ao agente web, W1) fica em parte: as decisões fiscais de 2027 (orçamento, regra, crédito a bancos oficiais) demoram e não confirmam nem uma ruptura nem uma consolidação; o impulso de 2026 se dissipa no fim do ano, como o Focus de 23/10 supõe.
- **Upside (ruim):** as decisões de 2027 afrouxam explicitamente a política fiscal (regra mudada ou despesa fora do limite, novo aporte do Tesouro ao BNDES), e o mercado lê a reação monetária como insuficiente; os sinais de mercado da dominância se espalham para o CDS e as expectativas longas.
- **Downside (bom):** um arcabouço de 2027 com meta e corte de despesa que o mercado compre desfaz a leitura de 26/10, e os preços voltam ao intervalo de 05/10–23/10.

**Caminhos das exógenas.**

| Exógena | Hoje (valor · tabela · data) | Cenário | 4T26 | 1T27 | 2T27 | 3T27 | 4T27 | 1T28 |
|---|---|---|---|---|---|---|---|---|
| CDS 5 anos, fechamento (`fiscal`, p.b.) | 137 · `cmb_risco_pais` · 26/10 (3T26: 131) | base | 140 | 140 | 138 | 135 | 135 | 135 |
| | | upside | 165 | 190 | 200 | 200 | 195 | 190 |
| | | downside | 115 | 110 | 108 | 106 | 105 | 105 |
| NTN-B 10 anos, média (`rr_10a`, % a.a.) | 8,05 · `br_interest_rate` · 26/10 (3T26: 7,84; 4T26 até 26/10: 6,99) | base | 7,70 | 7,80 | 7,70 | 7,60 | 7,55 | 7,50 |
| | | upside | 8,05 | 8,80 | 9,00 | 9,00 | 8,90 | 8,80 |
| | | downside | 7,35 | 6,90 | 6,80 | 6,75 | 6,70 | 6,70 |

- Motivo da `rr_10a` em 4T26: a média já tem 17 pregões a 6,99%; os três valores equivalem a ~43 pregões restantes a cerca de 7,95% (base), 8,6% (upside) e 7,5% (downside).
- Motivo do upside: a alta de ~69 p.b. do CDS em dois trimestres fica perto do percentil 90 da variação de dois trimestres desde 2016 (+100 p.b.), e a `rr_10a` de 9,00% fica ~1,2 p.p. acima de 3T26, perto do percentil 95 da variação de dois a três trimestres (+1,15 a +1,51 p.p.) (`cmb_risco_pais`, `br_interest_rate`).
- Motivo do downside: o nível em que os preços ficaram por três semanas de outubro, o preço que o próprio mercado deu à consolidação.
- `meta_12m`: no caminho do principal (PM); nesta rodada, o padrão do simulador, 3,00%. Os demais exógenos no padrão.

**O que o modelo faz com esses caminhos** (as endógenas são teses dos outros agentes; aqui só o que o modelo devolve).

| Variável (modelo) | Cenário | 4T26 | 1T27 | 2T27 | 3T27 | 4T27 | 1T28 |
|---|---|---|---|---|---|---|---|
| PTAX, fechamento (R$/US$) | padrão do simulador | 5,21 | 5,25 | 5,25 | 5,24 | 5,25 | 5,28 |
| | base | 5,26 | 5,29 | 5,29 | 5,26 | 5,28 | 5,31 |
| | upside | 5,35 | 5,47 | 5,52 | 5,50 | 5,50 | 5,51 |
| | downside | 5,16 | 5,19 | 5,19 | 5,17 | 5,18 | 5,21 |
| Selic, média (% a.a.) | padrão | 13,60 | 13,26 | 12,96 | 12,70 | 12,47 | 12,27 |
| | base | 13,46 | 13,21 | 12,82 | 12,46 | 12,18 | 11,93 |
| | upside | 13,81 | 14,22 | 14,13 | 13,88 | 13,57 | 13,28 |
| | downside | 13,11 | 12,31 | 11,91 | 11,60 | 11,31 | 11,11 |
| IPCA 12 meses (%) | base | 5,28 | 4,87 | 4,35 | 4,36 | 4,24 | 4,09 |
| | upside | 5,29 | 4,91 | 4,44 | 4,49 | 4,38 | 4,21 |
| | downside | 5,27 | 4,83 | 4,30 | 4,30 | 4,18 | 4,04 |
| Hiato (% do potencial) | os três | 0,13 | −0,08 | −0,24 | −0,36 | −0,45 | −0,51 |

Fonte: Modelo Estrutural do ciclo, centrais (faixas de 90% do posterior no log da G).

**A história que o modelo conta, antes de discordar dela.** Os dois caminhos chegam por portas diferentes e quase não se misturam.

- **O CDS chega pelo câmbio.** Só a variação conta: o CDS de 131 para 140 em 4T26 deprecia a PTAX do modelo em 0,75% contra o padrão; o CDS do upside sozinho (`rr_10a` no padrão) a leva a 5,56 em 2T27, e daí sobe a inflação de alimentos e de bens industriais (IPCA de 12 meses de 4,23% em 1T28 contra 4,08% no padrão). A Selic do modelo mal reage ao CDS sozinho: o efeito sobre a inflação é pequeno demais para mover a regra.
- **A `rr_10a` chega pela âncora da regra, e o modelo a repassa à Selic um a um.** A `rr_10a` do upside sozinha (8,80% em 1T27, 0,96 p.p. acima do padrão) leva a Selic média de 1T27 de 13,26% a 14,21%, a mesma distância. Como na curva IS o aperto é `(Selic − meta) − rr_10a`, e a Selic sobe junto com a `rr_10a`, o aperto não muda e o hiato sai idêntico nos três cenários. Na leitura do mapa (2.10): um prêmio fiscal maior no juro longo sobe o neutro do modelo, e a regra leva a Selic até ele sem apertar a demanda; a queda da `rr_10a` no downside (consolidação precificada) dá ao modelo espaço para cortar 0,9 p.p. a mais em 1T27 sem afrouxar o hiato.
- **Onde este agente discorda:** a alta de 135 p.b. de 26/10 é em boa parte prêmio de risco (a inflação implícita subiu 0,89 p.p. no mesmo dia), não alta do juro real esperado de equilíbrio; repassá-la um a um à Selic trata prêmio como neutro. Quanto do caminho da `rr_10a` é prêmio fiscal e quanto é juro esperado e prêmio de prazo é a pergunta FS-PM3, e o efeito disso na regra é do PM. Registrado também na seção 6.

### 3.2 Etapa 2 — o tempero

A distribuição da tese vem dos três cenários e das probabilidades acima. Os dois temperos que este agente argumenta são aplicados por outros (seção 4):

**(i) CDS — efeito no câmbio mais forte que o estimado** · cenários base e upside
- O multiplicador é do agente de câmbio; aqui só o argumento.
- Coeficiente: `F.b_fiscal` estimado em 25,1 por desvio-padrão da variação do CDS (298,5 p.b.), intervalo de 90% de 19,5 a 30,6.
- Efeito: × 1,2 (dentro do intervalo, percentil 94) leva a PTAX do modelo na base de 5,255 para 5,262 em 4T26 (a variação do CDS na base é pequena) e × 1,5 (fora do intervalo) leva a do upside de 5,52 para 5,68 em 2T27.
- Por quê: em outubro o real andou 4,4 e 5,9 vezes o que o CDS explica no modelo; o desvio-padrão que padroniza o coeficiente é dominado por episódios de CDS muito alto (2002–2009, 2015), quando o risco era de calote em dólar; o risco precificado agora é de inflação e juro local, que o CDS mede mal. Reproduzir 26/10 só pelo CDS exigiria × 5,7, fora de qualquer leitura do posterior: o que sobra é choque doméstico fora do canal, e cabe ao câmbio decidir se o trata como multiplicador ou como fator próprio.
- Onde entra: no limite da cauda de alta da PTAX, que é do câmbio.

**(ii) Impulso e parafiscal sobre o hiato · tributos e subsídios sobre o IPCA**: direção, tamanho e duração na seção 4 (para atividade e inflação).

### 3.3 Da etapa 1 à tese

| Trimestre | CDS: central · upside · downside (p.b.) | `rr_10a`: central · upside · downside (%) |
|---|---|---|
| 4T26 | 140 · 165 · 115 | 7,70 · 8,05 · 7,35 |
| 1T27 | 140 · 190 · 110 | 7,80 · 8,80 · 6,90 |
| 2T27 | 138 · 200 · 108 | 7,70 · 9,00 · 6,80 |
| 3T27 | 135 · 200 · 106 | 7,60 · 9,00 · 6,75 |
| 4T27 | 135 · 195 · 105 | 7,55 · 8,90 · 6,70 |
| 1T28 | 135 · 190 · 105 | 7,50 · 8,80 · 6,70 |

A faixa da base fica entre a central e cada caminho de cauda, mais perto da central do lado de baixo, porque o cenário bom tem menos probabilidade e o ruim está mais longe; os caminhos de cauda ficam fora da faixa, como pontos típicos de cada cauda. A probabilidade de cada cauda é a do cenário dela.

## 4. Para os outros agentes

**Premissas fiscais para os outros, primeiro.**

- **Ao agente de atividade (FE-AT1), em destaque**[^dest]: o impulso por trimestre, em p.p. do PIB, impulso de 12 meses no fim do trimestre (+ = expansionista), premissa deste agente sobre o Focus de 23/10:

  | | 4T26 | 1T27 | 2T27 | 3T27 | 4T27 | 1T28 |
  |---|---|---|---|---|---|---|
  | Base | +0,1 | 0,0 | −0,1 | −0,1 | −0,2 | −0,3 |
  | Upside (afrouxamento) | +0,3 | +0,3 | +0,4 | +0,4 | +0,5 | +0,3 |
  | Downside (consolidação) | 0,0 | −0,2 | −0,3 | −0,4 | −0,5 | −0,5 |

  Medido hoje: +0,28 a +0,43 (12 meses até ago/26, conforme a medida, seção 2 F1). Por cima disso, o **parafiscal**: +0,89 p.p. do PIB de crédito do Tesouro ao BNDES em 12 meses, dois terços dele em mai–ago/26; o efeito na demanda vem com o desembolso, ao longo de 4T26 e 2027. Composição: a expansão está em discricionárias (saúde, educação) e investimento transferido a municípios, não em transferências às famílias (Bolsa Família −10,2% real). A conclusão sobre o hiato é sua.
- **Ao agente de inflação (FE-IN1):** o F não traz decisão de governo sobre tributos ou preços; declaro a lacuna e pedi ao agente web (W4). Com o Brent a US$ 115, o risco é uma decisão sobre combustível (tributo ou subsídio) dentro do horizonte, de efeito direto e de primeira rodada, em sentido incerto. Os monitorados de 12 meses estão em 4,14% (`inflc_agregados`, set/26).
- **Ao agente de PM (FE-PM1, FE-PM2), em destaque:** a postura fiscal é expansionista em 2026 e, na base, deixa de ser em 2027; no upside, segue expansionista com o parafiscal. O caminho da `rr_10a` é a tabela da seção 3.1. Divisão que proponho, a confirmar com FS-PM3 e FS-EX2: dos +135 p.b. de 26/10, a maior parte é prêmio (a inflação implícita subiu 0,89 p.p. no mesmo dia), e a base devolve ~25 p.b. até 1T27; a queda de 0,3 p.p. em 2027 supõe a Selic voltando a cair e o Treasury de 10 anos estável. No modelo, cada p.p. de `rr_10a` vira um p.p. de Selic sem mexer no hiato (seção 3.1): a leitura do prêmio na regra é sua.
- **Aos agentes de câmbio, PM e externo (FE-CB1, FE-EX1), em destaque:** o caminho do CDS é a tese da seção 1. Leitura: o CDS subiu pouco num choque grande e doméstico; a parte global relevante foi a de fim de setembro. Possível emenda de fonte no CDS em 21/09 (seção 2 F5): se a carga da Bloomberg substituir o trecho provisório e o nível mudar, os caminhos deste report devem ser lidos em variação a partir de 3T26, e eu os reescrevo na rodada seguinte.
- **Ao agente de câmbio, sobre `F.b_fiscal`:** o argumento da ficha (i) da seção 3.2: × 1,2 na base e × 1,5 no upside; a decisão é sua.
- **Ao agente de câmbio (FE-CB2), leitura de dominância:** sustentabilidade presente, mercado presente só nos preços locais, regime monetário sem sinal; cauda de dominância em ~10% no horizonte.
- **Ao agente de expectativas (FE-EP1):** a mesma leitura de risco, com o primário 4,9 p.p. abaixo do que estabiliza a DLSP.

**Pedidos.**

- **FS-CB1:** que parte da alta de 9,2% da PTAX em 26/10 e da queda de 4,55% em 05/10 foi idiossincrática contra os pares, nos mesmos pregões? (Tese: a divisão fiscal/global do CDS e a probabilidade da cauda de alta.)
- **FS-CB2:** o caminho da PTAX e a posição de swap em outubro; o resultado de swap de out/26 confirma a ordem de −R$ 42 bi? (F4, resultado nominal.)
- **FS-PM1:** o caminho da Selic de fechamento, e se ele muda com a curva de 1 ano a 14,69% em 26/10. (r − g e o primário que estabiliza a dívida.)
- **FS-PM2:** como o comunicado e a ata de setembro descreveram a política fiscal, e se a próxima reunião muda essa linguagem. (Policy mix, F3.)
- **FS-PM3:** a divisão da alta de 135 p.b. da NTN-B 10a em 26/10 entre juro real esperado, prêmio de prazo e prêmio fiscal; e se o repasse um a um da `rr_10a` à Selic no modelo é aceitável para um choque de prêmio. (O caminho base da `rr_10a`, sobretudo 1T27–1T28.)
- **FS-PM4:** se o Copom interromper o corte ou subir juros depois de 26/10, isso é lido como credibilidade ou como mais risco da dívida? (Probabilidade da cauda de dominância.)
- **FS-IN1:** o caminho do IPCA de 12 meses (deflator do gasto e do juro real implícito da dívida).
- **FS-IN2:** que decisões de governo sobre combustível e energia o caminho do IPCA supõe, com o Brent a US$ 115.
- **FS-AT1:** crescimento real e hiato por trimestre (o g de r − g e a correção cíclica do impulso).
- **FS-AT2:** consumo e investimento do governo nas contas nacionais de 3T26, quando saírem: confirmam a direção do impulso?
- **FS-EX1:** outubro teve movimento de prêmio de risco entre emergentes? O peso mexicano se depreciou 7,8% em um mês até 20/10 (`cmb_fx_latam`). (A parte global do CDS.)
- **FS-EX2:** o caminho do Treasury de 10 anos, hoje em 5,00%: o piso que ele põe sob a `rr_10a`. (O declive da base em 2027.)
- **FS-EX3:** o caminho do Brent: royalties cresceram 19,4% real em 12 meses e sustentam a receita.
- **FS-EP1, em destaque:** a revisão do Focus de primário, nominal, DLSP e DBGG **depois de 26/10**, e a confirmação de que o primário do Focus é o do setor público consolidado. (F4 e a probabilidade das caudas.)
- **FS-EP2, em destaque:** o Focus de IPCA de 2029–2030 se moveu depois de 26/10? (Sinal de mercado da dominância.)

**Ao agente web.**

- **W1:** o que aconteceu nos fins de semana de 03–04/10/2026 e de 24–25/10/2026 que moveu todos os ativos domésticos em 05/10 (PTAX −4,55%, DI 10a −134 p.b.) e em 26/10 (PTAX +9,19%, DI 10a +239 p.b., NTN-B 10a +135 p.b.)? A hipótese a confirmar é o calendário eleitoral; preciso do fato, de fonte de nível A, e das primeiras declarações nomeadas sobre política fiscal depois de 26/10. (Tese: a história dos três cenários e a probabilidade de cada cauda.)
- **W2:** propostas ou declarações, depois de 26/10, sobre o arcabouço fiscal de 2027: mudança na regra, despesa fora do limite, meta de primário do PLOA 2027, com nome e cargo de quem disse. (Tese: a cauda de alta do CDS e da `rr_10a`.)
- **W3:** a que corresponde o aumento de R$ 126 bi do crédito do Tesouro ao BNDES entre set/25 e ago/26 (lei, MP, programa, finalidade), e se há novo aporte previsto. (Tese: o parafiscal no impulso de 4T26–2027 e no cenário de alta.)
- **W4:** decisões ou propostas de governo sobre tributos e subsídios de combustíveis e energia desde set/26, com o Brent acima de US$ 110, e a regra do salário mínimo de 2027. (Tese: FE-IN1, efeito direto no IPCA.)
- **W5:** a meta de primário de 2026 e de 2027, a banda de tolerância e o limite de crescimento da despesa de 2027, de documento oficial (LDO/PLOA). (Tese: F4; hoje é lacuna.)
- **W6:** o salto das discricionárias (+34,6% real em 12 meses; saúde +68,9%) e das transferências de investimento a municípios (+70,4%) vem de emendas parlamentares, de pisos de saúde e educação ou de outra decisão? Há contingenciamento anunciado para o fim de 2026? (Tese: o impulso de 4T26, +0,1 na base.)
- **W7:** alguma declaração ou proposta, depois de 26/10, sobre mudar a meta de inflação ou o regime de metas? (Insumo de `meta_12m`, abaixo.)

**Como subordinado.**

- `meta_12m` · principal: política monetária
- Insumos: nenhum nesta rodada. O F não carrega decisão sobre a meta, e a rodada 1 não tem notícias; a pergunta foi feita ao agente web (W7), porque um choque doméstico do tamanho do de 26/10 é o tipo de evento em que a discussão da meta pode aparecer.
- Argumento e caminho de referência: nada a acrescentar neste ciclo.

**Divergências:** rodada 1, nada a responder.

## 5. Placar

Primeiro ciclo: não há report final anterior deste agente.

## 6. Sobre o modelo

| Fonte | O que sugere | Teste proposto | Por que importa para a tese deste ciclo |
|---|---|---|---|
| Dados do ciclo (`cmb_ptax`, `cmb_risco_pais`, 05/10 e 26/10) e mapa 2.9 | O peso do CDS na (F) é padronizado por um desvio-padrão (298,5 p.b.) dominado por 2002–2009; com o CDS baixo, o real anda 4–6 vezes o que o CDS explica | Reestimar (F) com a variação do CDS em log, ou em 2010–2026; se o coeficiente em log for estável entre subamostras e o em p.b. não, ler o CDS em log | Decide se o argumento ao câmbio é um multiplicador ou uma mudança de especificação |
| Dados do ciclo (inflação implícita 10a, +0,89 p.p. em 26/10) e mapa 2.9 | O choque fiscal de hoje aparece na curva local e não no CDS; a (F) não tem regressor que o capture | Incluir na (F) a variação da inflação implícita de 10 anos (ou do diferencial NTN-B 10a − Treasury 10a) e ver se ela tira poder do CDS e do resíduo nos trimestres de choque doméstico | O CDS sozinho subestima o canal fiscal no câmbio em choques como o de 26/10 |
| Rodadas do modelo deste ciclo e mapa 2.10 | A regra repassa a `rr_10a` à Selic um a um, e o hiato fica invariante a ela; um prêmio fiscal no juro longo vira juro neutro integral | Separar a `rr_10a` na parte explicada pelo CDS e no resto, e estimar a regra e a IS com as duas; se o peso da parte do prêmio for menor que 1 na âncora, a âncora deveria ser construída sem ela | É o que decide se o caminho da `rr_10a` deste agente move a Selic do P na medida certa |

[^proc]: Primeiro ciclo conjunto, rodada 1: sem literatura (o agente lê só o mapa conceitual), sem notícias (o agente web responde aos pedidos da seção 4 antes da rodada 2) e sem ler os reports dos outros agentes, escritos em paralelo. Não há dado eleitoral nem de pesquisa nesta análise. Dados fiscais com defasagem: RTN, NFSP e DLSP até ago/26 (87 dias antes do corte), EFGG e PIB até 2T26 (209 dias).
[^eleicao]: Este report não afirma o que aconteceu nesses fins de semana: nenhum dado do F o diz, e eventos e datas políticas não são escritos de memória. Os preços dizem o tamanho e o sentido da leitura que o mercado fez.
[^impl]: Inflação implícita: a diferença entre o juro prefixado e o juro real da NTN-B do mesmo prazo, (1 + DI)/(1 + NTN-B) − 1. Mede a inflação que o mercado cobra para emprestar sem indexação, com um prêmio de risco de inflação dentro. Ex.: DI de 15,13% e NTN-B de 8,05% dão 6,55%.
[^impulso]: Impulso fiscal: a mudança da postura de um período para o outro. Se o déficit primário passa de 0,2% para 0,6% do PIB sem que a economia tenha esfriado, o governo pôs 0,4% do PIB a mais de demanda na economia: impulso de +0,4. Aqui ele não é corrigido pelo ciclo, porque o hiato é do agente de atividade.
[^prim]: Resultado primário: receitas menos despesas do governo, sem contar os juros da dívida. Um primário de −0,62% do PIB quer dizer que, antes de pagar juros, o setor público gastou 0,62% do PIB a mais do que arrecadou. "Acima da linha" (RTN, Tesouro) mede pelas receitas e despesas; "abaixo da linha" (NFSP, BC) mede pela variação da dívida. Na NFSP, negativo é déficit; nos fatores da DLSP, positivo é déficit.
[^prec]: Precatórios: dívidas do governo reconhecidas pela Justiça. O pagamento se concentra num ou dois meses do ano, e o mês mudou de jul/25 para mar/26; por isso uma janela de 3 meses que perde um pagamento parece um ajuste fiscal que não houve.
[^para]: Parafiscal: o governo empurrando a demanda sem passar pelo primário, emprestando a bancos públicos (aqui, o Tesouro ao BNDES) que emprestam a empresas. Na dívida líquida o empréstimo é um ativo do governo e aparece com sinal negativo: o estoque ir de −R$ 106,7 bi para −R$ 232,9 bi é mais crédito concedido.
[^pct]: Percentil: a posição do valor de hoje no histórico, de 0 (o menor já visto) a 100 (o maior). Percentil 57 do hiato quer dizer que 57% dos trimestres desde 2003 tiveram hiato menor.
[^focus]: O F não diz a que conceito de primário a pesquisa Focus se refere; a comparação supõe o do setor público consolidado (NFSP) e a confirmação foi pedida em FS-EP1.
[^div]: Dívida líquida (DLSP) contra bruta (DBGG): a bruta soma o que o governo deve; a líquida desconta o que ele tem a receber, como as reservas internacionais e os empréstimos ao BNDES. Por isso o real mais fraco reduz a líquida (as reservas valem mais em reais) e mal mexe na bruta, e o crédito ao BNDES aumenta a bruta sem mexer na líquida.
[^swap]: Ordem de grandeza: a posição vendida de ago/26 (US$ 91,6 bi) vezes a alta da PTAX de 23/10 para 26/10 (R$ 0,46). A posição de outubro e o ajuste diário dos contratos tornam o número de out/26 diferente; ele sai na NFSP de outubro.
[^cds]: O CDS é carregado à mão de um export da Bloomberg, com um trecho provisório de outra fonte (aviso do F). O F não diz onde o trecho provisório começa; o salto de 21/09 sem contrapartida nos outros preços é o candidato. Se for emenda, o nível de 3T26 em diante pode estar alto em ~9 p.b., e as variações a partir dali continuam válidas.
[^dom]: Dominância fiscal: quando a dívida pesa tanto que subir juros piora o risco da dívida, o real se deprecia e a inflação sobe, em vez de cair. É um espectro, e os sinais vêm em três conjuntos: o regime monetário, a sustentabilidade fiscal e os preços de mercado.
[^q4]: A conta da média de 4T26 supõe 43 pregões restantes (dias úteis até 31/12 menos 02/11, 20/11, 24/12, 25/12 e 31/12); um ou dois pregões a mais ou a menos mudam a média em menos de 0,02 p.p.
[^dest]: "Em destaque" neste primeiro report marca o que mudou materialmente com os preços de 26/10 contra o que os dados até 23/10 diziam; não há report anterior deste agente para comparar.
