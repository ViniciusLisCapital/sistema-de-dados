# Report — câmbio · ciclo 2026-10-07 · rodada 1

Dados até: 07/10/2026 (PTAX até 06/10/2026) · Horizontes: os seis trimestres do Modelo Estrutural a partir do trimestre em curso, do 4T26 ao 1T28, com a PTAX de venda do último dia útil de cada trimestre

## 1. Tese

| Variável | Trimestre | Central | Base: faixa · P | Cauda worst (depreciação): limite · P | Cauda best (apreciação): limite · P | Pbc − Pwc |
|---|---|---|---|---|---|---|
| USD/BRL, PTAX de venda no fechamento do trimestre | 4T26 | 5,05 | 4,85 a 5,25 · 55% | acima de 5,25 · 27% | abaixo de 4,85 · 18% | −0,09 |
| | 1T27 | 5,08 | 4,85 a 5,35 · 52% | acima de 5,35 · 27% | abaixo de 4,85 · 21% | −0,06 |
| | 2T27 | 5,10 | 4,80 a 5,45 · 50% | acima de 5,45 · 28% | abaixo de 4,80 · 22% | −0,06 |
| | 3T27 | 5,13 | 4,75 a 5,55 · 46% | acima de 5,55 · 32% | abaixo de 4,75 · 22% | −0,10 |
| | 4T27 | 5,16 | 4,75 a 5,65 · 43% | acima de 5,65 · 34% | abaixo de 4,75 · 23% | −0,11 |
| | 1T28 | 5,18 | 4,75 a 5,70 · 42% | acima de 5,70 · 33% | abaixo de 4,75 · 25% | −0,08 |

- **O que leva à cauda worst (depreciação).** No 4T26: o 2º turno de 25/10[^1] reverte a leitura que o mercado fez em 05/10, o CDS vai a 150 p.b., o DI de 2 anos devolve a queda de 110 p.b. daquela sessão e o canal de estresse de regime soma +5% ao caminho do modelo; ou, sem evento doméstico, o dólar contra emergentes sobe para 135 com o Fed Funds a caminho de 4,38% e os fundos desmontam a posição comprada em real (+2% de desvio). Em 2027: o plano fiscal do novo governo não estabiliza a dívida bruta, o CDS sobe para 170 a 180 p.b., e um corte de Selic lido como perda de credibilidade (S2) leva o diferencial de juros para baixo de 7,5 p.p.
- **O que leva à cauda best (apreciação).** No 4T26: o 2º turno confirma a leitura de 05/10 e o CDS cai para 95 p.b., com o dólar global estável. Em 2027: um plano fiscal que aponte para superávit primário leva o CDS a 85 p.b., o diferencial de juros fica acima de 8 p.p. com a volatilidade do real em 9% ao ano, o IC-Br em dólar se mantém em 215 com o petróleo alto e o dólar contra emergentes recua para 126.
- **A tese em uma frase:** o real deve devolver pouco da apreciação de 05/10 — central de 5,05 no fim de 2026, perto do forward, e alta gradual até 5,18 no 1T28, abaixo do forward em todos os trimestres seguintes, porque o carry continua o maior entre os pares e o petróleo alto favorece o Brasil, enquanto a queda do diferencial de juros e o diferencial de inflação puxam devagar para cima; a assimetria é de depreciação em todos os trimestres, concentrada no 2º turno (4T26) e, em 2027, na validação fiscal do prêmio de risco que o mercado já comprimiu.

A consolidação pelo Modelo Estrutural está pendente: o caminho acima é do agente, montado a partir dos caminhos de canal e dos desvios da seção 3[^2].

## 2. Argumentação

### Q1. Quais as condições subjacentes do mercado de câmbio brasileiro?

O mercado funciona sem sinal de escassez aguda de dólar, mas com o Banco Central presente em setembro e com o posicionamento especulativo já comprado em real antes do salto de 05/10.

- **Liquidez normal.** O volume interbancário D+2 fez média de US$ 1.240 mi/dia no último mês (`cmb_ptax`, até 06/10), percentil 45 dos últimos 10 anos[^3]; o D+1, US$ 331 mi/dia, percentil 68.
- **Volatilidade concentrada num dia.** A volatilidade realizada de 21 dias está em 18,6% ao ano, contra 12,2% na de 63 dias (tabela "O real e os pares", 06/10), que está no percentil 53 dos últimos 10 anos. A diferença vem da sessão de 05/10, quando a PTAX caiu 4,66% (`cmb_ptax`, 02/10 → 05/10).
- **Fluxo cambial negativo nos dois últimos meses, positivo em 12 meses.** O saldo total foi de −US$ 3,90 bi em agosto e −US$ 4,02 bi em setembro até 25/09 (financeiro −US$ 4,62 bi, comercial +US$ 0,60 bi) (`cmb_cambio_contratado`). Em 12 meses o saldo é de +US$ 1,00 bi, contra −US$ 46,46 bi um ano antes: a virada veio dos capitais estrangeiros (+US$ 87,32 bi em 12 meses, contra +US$ 33,20 bi). Do outro lado, as rendas (lucros, dividendos e juros remetidos) somam −US$ 67,00 bi em 12 meses, percentil 5 do histórico: só 5% das leituras de 12 meses tiveram saída maior.
- **O BC vendeu dólar em setembro.** Foram US$ 1 bi à vista em 31/08, 14/09 e 17/09 e US$ 1 bi em leilão de linha[^4] em 22/09 (`cmb_reservas_bc`). A venda de 14/09 coincidiu com a maior alta diária da PTAX desde 01/09, +1,52% (`cmb_ptax`). As reservas estão em US$ 363,2 bi (06/10), US$ 9,7 bi abaixo de um mês antes; a queda é maior que as vendas de setembro, e o F não decompõe o restante.
- **Bancos vendidos à vista.** A posição à vista dos bancos estava em −US$ 22,1 bi em agosto (`cmb_reservas_bc`), percentil 15 do histórico e 40 dos últimos 10 anos: abaixo da mediana do histórico longo, perto dela na última década. O estoque de swaps era de −US$ 91,6 bi (ago). O cupom cambial, que mediria a escassez de dólar no mercado local, não está nos dados[^5].
- **Posicionamento comprado em real e perto do extremo.** Em 22/09, antes de 05/10, os asset managers tinham +59.481 contratos líquidos comprados em real, percentil 93 dos últimos 10 anos, e os fundos alavancados +14.917, percentil 91 (`cmb_cot_fx`)[^6]. As posições em aberto, 117.063 contratos, estão no percentil 94.

### Q2. Como estão os fundamentos macroeconômicos para o câmbio?

O carry e as contas externas sustentam o real; o prêmio de risco está baixo para a trajetória da dívida, e é aí que mora a vulnerabilidade de 2027.

- **Carry: o maior dos pares, mas encolhendo.** Selic de 13,75% (`pm_copom_reuniao`, 16/09) contra Fed Funds de 3,875% (meta, ponto médio, `us_interest_rate`, desde 17/09, quando subiu 0,25 p.p.) dão 9,875 p.p. de diferencial. A tabela "O real e os pares" mostra carry sobre volatilidade de 0,83 para o real (com o Fed ainda em 3,63%), contra 0,56 do peso colombiano, 0,49 do mexicano, 0,14 do sol e 0,09 do peso chileno; com o Fed de hoje a razão do real é 0,81. O diferencial real ex-post é de 9,50 p.p. (`diferenciais_juros`, ago), percentil 87 dos últimos 10 anos. Para a frente, a curva de 06/10 precifica a Selic em 13,26% em dez/2026 e 12,20% em dez/2027 (`br_di_grade`), o que leva o diferencial, com o Fed parado, a 9,38 p.p. no 4T26 e 8,32 p.p. no 4T27.
- **Prêmio de risco baixo para o fiscal.** O CDS de 5 anos estava em 112 p.b. em 08/09 (`cmb_risco_pais`), 24 p.b. abaixo de um ano antes, e o dado está parado desde então[^7]. No mesmo período a dívida bruta subiu 5,5 p.p., para 82,9% do PIB (`fisc_divida`, ago), com déficit primário de 0,62% e nominal de 9,48% do PIB em 12 meses (`fisc_nfsp`, ago). Um prêmio que cai enquanto a dívida sobe é um prêmio comprimido: deixa pouca folga se a política fiscal de 2027 decepcionar[^8].
- **Termos de troca e petróleo a favor.** O Brent está em US$ 113,96 (`comm_brent`, 29/09), +27,0% em um mês e +59,2% em três. O Brasil exporta petróleo: US$ 51,62 bi exportados em 12 meses contra US$ 6,59 bi importados (`cmb_comex_produto`, ago), com a exportação no percentil 100 do histórico. Num choque de petróleo, a conta de um exportador melhora enquanto a dos emergentes importadores piora[^9]. O IC-Br em dólar estava em 202,35 em agosto (`comm_icbr_usd`), +12,6% em 12 meses, e ainda não registra a alta do Brent em setembro; os termos de troca da Funcex, 111,35 em julho (`cmb_termos_troca`, percentil 75 dos últimos 10 anos), estão com 98 dias de defasagem.
- **Contas externas financiadas.** O déficit em transações correntes é de US$ 63,04 bi em 12 meses, 2,47% do PIB, menor que os US$ 76,92 bi de um ano antes, e o investimento direto no país soma US$ 86,56 bi, 3,39% do PIB (`cmb_balanco_pagmt`, ago): o déficit é coberto pelo fluxo mais estável que existe[^10].
- **Valuation neutro em agosto, menos barato hoje.** O câmbio real efetivo do real estava em 116,46 em agosto (`cmb_reer`), percentil 50 dos últimos 10 anos, +5,5% em 12 meses[^11]. Desde então a PTAX caiu 4,09% (31/08 → 06/10, `cmb_ptax`) enquanto os pares se desvalorizaram, de modo que o real está hoje mais apreciado em termos efetivos do que em agosto; o F não traz o índice depois de agosto.
- **Diferencial de inflação pequeno.** IPCA de 4,22% e CPI dos EUA de 3,35% em 12 meses (ago, `diferenciais_juros`): 0,87 p.p. A mediana da Focus para o IPCA de 2027, 4,31% (`expc_focus_periodo`, 25/09), dá 0,96 p.p. contra o CPI de agosto. Pela paridade do poder de compra, isso empurra a PTAX para cima em cerca de 1% ao ano, devagar.

### Q3. O que explica a dinâmica recente do câmbio?

Janela de referência: o 3T26 e as sessões de outubro, com atenção a setembro, quando o dólar global subiu, e a 05/10. Não há ciclo anterior.

A PTAX fechou o 3T26 em 5,1809 (30/09), praticamente igual aos 5,1766 de 30/06 (+0,08%), e está em 4,9698 em 06/10: −4,07% desde o fim do trimestre, −3,99% em três meses e −9,68% desde o fim de 2025 (5,5024 em 31/12/2025) (`cmb_ptax`). O movimento tem duas fases, e nas duas o componente do real domina o global.

| Variação no período (moeda local por dólar; + = desvalorização) | Real | DXY | Dólar contra emergentes | Peso mexicano | Peso chileno | Peso colombiano | Sol peruano |
|---|---|---|---|---|---|---|---|
| 3T26 (30/06 → 30/09) | +0,08% | +0,26% | −0,06% | +2,46% | +5,13% | −6,82% | +0,34% |
| Setembro (31/08 → 30/09) | −0,01% | +2,03% | +1,98% | +5,23% | +4,36% | +0,18% | +1,74% |
| Sessões de 05 e 06/10 (02/10 → 06/10) | −4,86% | −0,10% | sem dado | sem dado | sem dado | sem dado | sem dado |

Fontes: `cmb_ptax`, `cmb_dollar_index`, `cmb_dollar_index_em`, `cmb_fx_latam`. Os pares terminam em 29/09 (México e Chile), 25/09 (Peru) e 23/09 (Colômbia); o dólar contra emergentes, em 02/10.

- **Setembro: o real parado num mês de dólar forte.** O DXY e o dólar contra emergentes subiram cerca de 2%, o Fed subiu os juros em 17/09, o Treasury de 2 anos subiu 47 p.b. e o de 10 anos 53 p.b. (04/09 → 05/10, `us_interest_rate`), e o Brent subiu 27,0% (`comm_brent`, um mês até 29/09). O peso mexicano se desvalorizou 5,23% e o chileno 4,36%. O real ficou estável. Com a sensibilidade média do real ao dólar contra emergentes estimada em jul/2024–jun/2026 (beta de 1,37)[^12], o dólar global teria desvalorizado o real em 2,7% (em log) em setembro; o real não se mexeu, um componente próprio de −2,7%. O DI de 2 anos caiu só 9 p.b. entre 04/09 e 02/10 (`br_di_grade`), então esse ganho relativo não veio de uma reprecificação do risco doméstico. Os canais que restam são o petróleo, a favor de um exportador num universo de importadores, e o carry, o maior dos pares em relação à volatilidade, com o BC vendendo dólar no pior dia do mês (14/09).
- **05/10: um choque doméstico.** Na primeira sessão depois do 1º turno da eleição (04/10)[^1], a PTAX caiu de 5,2238 para 4,9859, −4,66%, e o DI caiu 70 p.b. no prazo de 1 ano, 110 p.b. no de 2, 135 p.b. no de 5 e 134 p.b. no de 10 (`br_di_grade`, 02/10 → 05/10). No mesmo dia o Treasury de 2 anos subiu 1 p.b. e o de 10 anos 3 p.b. (`us_interest_rate`); nas sessões de 05 e 06/10 o DXY caiu 0,10%. Com a sensibilidade ao DXY estimada no mesmo período, o componente global dessas duas sessões é de −0,05% e o próprio do real é de −4,94% (em log). Real e curva inteira de juros se moveram juntos, com o resto do mundo parado: é a assinatura de uma queda do prêmio de risco doméstico. O F não traz o resultado da eleição; o que se lê é o preço.
- **Saldo de três meses.** Contra o DXY, os −4,08% (em log) do real entre 30/06 e 06/10 se dividem em +0,31% de componente global e −4,39% de componente próprio. A curva de juros conta a mesma história: um mês antes, em 04/09, ela precificava a Selic subindo para 14,10% em dez/2027; em 06/10, cortes até 12,20% (`br_di_grade`).

### Q4. Qual o cenário prospectivo para o câmbio?

**Por que a central e a faixa base.** A PTAX parte de 4,9698, depois de uma queda de prêmio de risco que o mercado precificou em um dia. O cenário base assume que essa queda se mantém em grande parte: o CDS fica perto de 105 p.b. e o dólar global estável. Três forças impedem que a PTAX fique no nível de hoje no 4T26: a posição comprada em real já perto do extremo antes do salto, que deixa pouco comprador novo; o dólar firme lá fora, com o Fed subindo juros e os Treasuries em alta; e dezembro, quando o fluxo cambial é sistematicamente negativo (média de −US$ 12,56 bi nos dezembros de 2016 a 2025, contra +US$ 0,10 bi nos outros meses, `cmb_cambio_contratado`). Por isso a central do 4T26, 5,05, fica 1,6% acima de hoje e 0,3% abaixo do forward de 5,0676[^13]. Ela fica 0,15 abaixo da mediana da Focus para o fim de 2026, 5,20 (25/09), que é anterior a 05/10.

De 2027 em diante a central sobe devagar, até 5,18 no 1T28 (+4,2% sobre hoje), por dois canais do modelo: o diferencial de juros cai de 9,38 p.p. para 8,32 p.p. com a Selic precificada na curva, e o diferencial de inflação, perto de 1 p.p. ao ano, empurra a PTAX nominal para cima. A central fica abaixo do forward em todos esses trimestres, de 1,7% no 1T27 a 6,4% no 1T28: é a aposta de que o carry continua pagando, porque o diferencial segue acima de 8 p.p. e o petróleo continua a favor do Brasil. O condicionante de câmbio do Copom parte de R$ 5,15 na 281ª reunião e sobe pela paridade do poder de compra[^14]; a central do 4T26 fica 1,9% abaixo do ponto de partida.

As faixas foram calibradas na distribuição histórica da variação da PTAX em prazos iguais aos de cada trimestre, de out/2016 a out/2026 (`cmb_ptax`)[^15], e se alargam com o prazo: de 40 centavos no 4T26 para 95 no 1T28. A probabilidade da faixa base cai de 55% para 42% pela mesma razão.

**Por que a cauda de depreciação é mais provável que a de apreciação.** Em todos os trimestres a cauda worst pesa mais (Pbc − Pwc entre −0,06 e −0,11), por quatro razões:

1. **O ponto de partida já incorpora a boa notícia.** Em 05/10 o mercado precificou um desfecho doméstico favorável. O 2º turno (25/10) pode confirmar, o que mantém a PTAX perto de hoje, ou reverter, o que a devolve aos 5,22 de 02/10 e acima. A reversão pesa mais no preço do que a confirmação, porque a confirmação já está no preço.
2. **Posicionamento cheio.** Com os fundos comprados em real no percentil 91 a 93 dos últimos 10 anos antes de 05/10, uma notícia ruim encontra muitos vendedores potenciais e poucos compradores novos.
3. **O prêmio comprimido precisa de validação fiscal em 2027.** Com a dívida bruta subindo 5,5 p.p. em 12 meses, a queda do CDS e do DI depende de o novo governo apresentar uma trajetória de dívida crível. É por isso que a cauda worst cresce de 27% para 32% a 34% na segunda metade de 2027.
4. **O dólar global está do lado errado.** O Fed subiu juros em setembro e o Treasury de 2 anos, a 4,84% (05/10), está bem acima do Fed Funds de 3,875%, o que precifica mais altas. O real tem sensibilidade alta ao dólar contra emergentes (beta de 1,37); em setembro o carry e o petróleo compensaram, mas um segundo mês igual encontraria o real sem o colchão do prêmio de risco, já gasto em 05/10.

A cauda best não é pequena (18% a 25%) porque o carry continua o maior entre os pares e o petróleo alto melhora a conta externa de um exportador num mundo de importadores: se o 2º turno confirmar e o plano fiscal convencer, o real tem espaço para seguir o caminho de 05/10, com a PTAX abaixo de 4,85 no 4T26.

### Outros pontos

- **O real se descolou dos pares antes da eleição, não só depois.** O ganho relativo de setembro (componente próprio de −2,7%) aconteceu com o DI parado, o que sugere que petróleo e carry seguravam o real independentemente da eleição. Se essa leitura estiver certa, esse suporte vale nos dois resultados do 2º turno: numa reversão, o que leva a PTAX além dos 5,22 de 02/10 é o prêmio de risco subir acima do nível anterior a 05/10, que é o que o canal de estresse de regime registra. É uma hipótese a testar na rodada 2.
- **A dívida subindo com o prêmio caindo é a principal incoerência dos fundamentos hoje.** O mercado está precificando a política fiscal que espera, não a que os dados mostram até agosto.

## 3. Premissas

### 3.1 Canais do modelo quantitativo

**Prêmio de risco / fiscal — CDS 5 anos** · exógeno · assumida
- Hoje: 112 p.b. (`cmb_risco_pais`, 08/09/2026), −24 p.b. em 12 meses; o dado não registra a sessão de 05/10[^7].
- Base: 4T26 105 · 1T27 105 · 2T27 110 · 3T27 115 · 4T27 115 · 1T28 120 — a queda de prêmio de 05/10 se mantém no 4T26 e o CDS sobe devagar em 2027 com a dívida bruta em 82,9% do PIB e subindo (`fisc_divida`, ago).
- Na cauda worst: 4T26 150 · 1T27 160 · 2T27 170 · 3T27 175 · 4T27 180 · 1T28 180 — 2º turno reverte a leitura de 05/10, ou o plano fiscal de 2027 não estabiliza a dívida.
- Na cauda best: 4T26 95 · 1T27 90 · 2T27 a 1T28 85 — 2º turno confirma e o plano fiscal aponta para superávit primário.
- Alerta: CDS 5 anos · variação · +25 p.b. · 10 sessões
- Checkpoints: 2º turno · 25/10/2026[^1]; primeiro CDS posterior a 08/09 na base · sem data; resultado fiscal de 12 meses (`fisc_nfsp`) · mensal.

**Dólar global e apetite a risco — dólar contra emergentes, S&P 500, Fed Funds** · TWA · assumida
- Hoje: dólar contra emergentes 129,71 (`cmb_dollar_index_em`, 02/10), +2,4% em um mês; DXY 102,31 (`cmb_dollar_index`, 07/10), +3,2% em um mês; S&P 500 7.769 (`cmb_equity_us`, 07/10), +15,7% em 12 meses; Fed Funds 3,875% (`us_interest_rate`, 07/10), +0,25 p.p. em 17/09; Treasury 2 anos 4,84% e 10 anos 5,31% (05/10).
- Base: dólar contra emergentes 130 · S&P 500 7.700 · Fed Funds 3,875%, iguais nos seis trimestres. A curva americana precifica mais altas do que esta premissa.
- Na cauda worst: dólar contra emergentes 133 no 4T26 e 135 de 1T27 a 1T28 · S&P 500 6.600 a partir do 1T27 · Fed Funds 4,125% no 4T26 e 4,375% de 1T27 a 1T28 — o choque do petróleo leva o Fed a mais duas altas e aperta as condições financeiras globais.
- Na cauda best: dólar contra emergentes 126 a partir do 1T27 · S&P 500 8.000 · Fed Funds 3,625% a partir do 2T27 — o Brent recua e a alta de setembro é desfeita.
- Alerta: dólar contra emergentes · variação · +2% · 10 sessões **e** Treasury 2 anos · variação · +30 p.b. · 10 sessões
- Checkpoints: reuniões do FOMC de out e dez/2026 (datas fora dos dados).

**Commodities — IC-Br em dólar** · TWA · assumida
- Hoje: 202,35 (`comm_icbr_usd`, ago/2026), +12,6% em 12 meses; energia −11,7% em três meses até agosto. Brent US$ 113,96 (`comm_brent`, 29/09), +27,0% em um mês. O índice ainda não registra a alta do petróleo de setembro.
- Base: 4T26 210 · 1T27 205 · 2T27 200 · 3T27 198 · 4T27 195 · 1T28 195 — a energia sustenta o índice no 4T26 e recua em 2027, em linha com a curva futura do petróleo, que o RPM de setembro descreve com "queda mais acentuada após alta no quarto trimestre de 2026".
- Na cauda worst: 4T26 200 · 1T27 a 1T28 185 — desaceleração global derruba commodities (um dos riscos de baixa listados pelo Copom em 16/09).
- Na cauda best: 215 nos seis trimestres — o petróleo fica alto e os metais (+49,2% em 12 meses até agosto) se mantêm.
- Alerta: Brent · variação · −20% · 20 sessões
- Checkpoints: IC-Br de setembro e outubro · próximas divulgações.

**Carry — Selic, Fed Funds e volatilidade do real** · Selic: endógeno de política monetária, aguarda política monetária (S1); Fed Funds: TWA, assumida; volatilidade: endógeno, próprio
- Hoje: Selic 13,75% (`pm_copom_reuniao`, 16/09); Fed Funds 3,875% (07/10); diferencial 9,875 p.p.; volatilidade de 63 dias 12,2% ao ano, percentil 53 dos últimos 10 anos, e de 21 dias 18,6% (tabela "O real e os pares", 06/10).
- Base: Selic 4T26 13,26 · 1T27 12,83 · 2T27 12,42 · 3T27 12,18 · 4T27 12,20 · 1T28 12,20, a precificada na curva de 06/10 na última reunião de cada trimestre (`br_di_grade`; o calendário oficial termina em 08/12/2027, e o 1T28 repete o 4T27). Premissa provisória até a resposta a S1. Diferencial com o Fed Funds da base: 9,38 · 8,96 · 8,54 · 8,30 · 8,32 · 8,32 p.p. Volatilidade de 63 dias: 12% no 4T26 e 10% de 1T27 a 1T28.
- Na cauda worst: diferencial abaixo de 7,5 p.p. de 2T27 em diante (Selic abaixo da curva com inflação acima da meta, lido como perda de credibilidade em S2, ou Fed Funds em 4,375%); volatilidade de 63 dias em 18%.
- Na cauda best: diferencial igual ao da base; volatilidade de 63 dias em 9% de 1T27 em diante.
- Alerta: carry sobre volatilidade de 63 dias do real · patamar · abaixo de 0,50 · —
- Checkpoints: Copom · 04/11/2026, 09/12/2026 e 27/01/2027 (`pm_copom_calendario`).

**Diferencial de inflação — IPCA e CPI dos EUA** · TWA · assumida
- Hoje: IPCA 4,22% em 12 meses (`inflc_agregados`, ago); CPI dos EUA 3,35% (`diferenciais_juros`, ago); diferencial de 0,87 p.p. O IPCA-15 de setembro subiu 0,70% no mês (`inflc_agregados`), depois de −0,40% em agosto.
- Base: IPCA em 12 meses 4T26 5,0 · 1T27 4,8 · 2T27 4,6 · 3T27 4,5 · 4T27 4,3 · 1T28 4,2, com os pontos de dezembro nas medianas da Focus para 2026 (4,99%) e 2027 (4,31%) (`expc_focus_periodo`, 25/09) e os trimestres intermediários assumidos; CPI dos EUA em 3,35% nos seis trimestres.
- Na cauda worst: IPCA 5,5 no 4T26 e 4,8 ao longo de 2027 — efeitos de segunda ordem do petróleo, o primeiro risco de alta listado pelo Copom em 16/09.
- Na cauda best: IPCA 4,6 no 4T26 e 3,8 no 4T27 — o petróleo recua e a apreciação de outubro chega aos preços.
- Alerta: mediana da Focus para o IPCA de 2027 · variação · +0,20 p.p. · 4 semanas
- Checkpoints: IPCA de setembro · divulgação em outubro; RPM de dezembro/2026.

### 3.2 Canais qualitativos

**Balanço de pagamentos e fluxos — fluxo cambial contratado, saldo total** · endógeno · próprio
- Hoje: −US$ 4,02 bi em setembro até 25/09 e −US$ 3,90 bi em agosto; +US$ 1,00 bi em 12 meses (`cmb_cambio_contratado`). Transações correntes −2,47% do PIB e investimento direto no país 3,39% do PIB em 12 meses (`cmb_balanco_pagmt`, ago).
- A tese assume: o déficit externo segue coberto pelo investimento direto, e a saída de dezembro fica perto da média sazonal (−US$ 12,56 bi nos dezembros de 2016 a 2025), atendida pelas linhas do BC como de costume. Nesses dez dezembros a PTAX subiu em quatro e a variação média no mês foi de −0,8% (`cmb_ptax`): a saída sazonal não costuma, sozinha, depreciar o real.
- Desvio no cenário base: nenhum.
- Se o alerta disparar: +1,5% sobre o modelo no 4T26, some no 1T27.
- Alerta: fluxo cambial contratado, saldo total · patamar · saída acima de US$ 20 bi · mês calendário
- Checkpoints: fluxo cambial de outubro, novembro e dezembro · divulgações semanais; balanço de pagamentos de setembro · fim de outubro.

**Posicionamento — CFTC, contratos futuros de real (COT)** · endógeno · próprio
- Hoje: asset managers +59.481 contratos líquidos, percentil 93 dos últimos 10 anos; fundos alavancados +14.917, percentil 91; dealers −52.093, percentil 10 (`cmb_cot_fx`, 22/09)[^6]. O dado é anterior a 05/10.
- A tese assume: a posição comprada não é desmontada de uma vez. Ela limita a apreciação adicional, mas não inicia sozinha uma depreciação.
- Desvio no cenário base: nenhum.
- Se o alerta disparar: +2% sobre o modelo por um trimestre — a desmontagem amplia uma depreciação que outro canal começou.
- Alerta: asset managers, líquido em real · variação · −20.000 contratos · 2 relatórios semanais **e** PTAX · variação · +3% · 10 sessões
- Checkpoints: relatórios semanais da CFTC, o primeiro que cobre 05/10.

**O BC no mercado de câmbio — intervenção à vista e leilões de linha** · endógeno · próprio
- Hoje: vendas à vista de US$ 1 bi em 31/08, 14/09 e 17/09 e leilão de linha de US$ 1 bi em 22/09; em 12 meses, −US$ 8,00 bi à vista, contra −US$ 22,57 bi um ano antes; reservas de US$ 363,2 bi (06/10), −US$ 9,7 bi em um mês; swaps em −US$ 91,6 bi e posição à vista dos bancos em −US$ 22,1 bi (ago) (`cmb_reservas_bc`).
- A tese assume: o BC oferece linhas em dezembro, como de costume, e não precisa vender à vista com o real apreciado.
- Desvio no cenário base: nenhum.
- Se o alerta disparar: +1% sobre o modelo enquanto durarem as vendas — a venda sinaliza uma pressão de saída que o modelo não vê; ela atenua, não anula, essa pressão[^16].
- Alerta: intervenção à vista · patamar · vendas acima de US$ 3 bi · mês calendário
- Checkpoints: comunicados de leilão do BC · contínuo; dezembro/2026.

**Estresse de regime — PTAX e DI de 2 anos em conjunto** · endógeno · próprio
- Hoje: sem sinal. O último movimento conjunto grande foi no sentido da apreciação: −4,66% da PTAX e −110 p.b. no DI de 2 anos em 05/10 (`cmb_ptax`, `br_di_grade`). Reservas de US$ 363,2 bi (06/10).
- A tese assume: nenhuma depreciação desordenada.
- Desvio no cenário base: nenhum.
- Se o alerta disparar: +5% sobre o modelo por dois trimestres — no 4T26 e no 1T27 se vier do 2º turno, em 2027 se vier do fiscal. É o que o CDS sozinho não capta: a desmontagem simultânea de carry, posição e curva.
- Alerta: PTAX · variação · +4% · 5 sessões **e** DI 2 anos · variação · +75 p.b. · 5 sessões
- Checkpoints: 2º turno · 25/10/2026; plano fiscal do novo governo · sem data nos dados.

## 4. Para os outros agentes

**Respostas às entradas fixas (E1–E7, para política monetária)**

- **E1, em destaque: o movimento de 05/10 é persistente no cenário base.** A queda de 4,66% da PTAX veio com a curva de juros inteira (−110 p.b. no DI de 2 anos), e não com o dólar global, o que é o perfil de uma mudança de nível do prêmio de risco e não de ruído. A central do 4T26, 5,05, fica 3,3% abaixo dos 5,2238 de 02/10: o cenário base mantém a maior parte da apreciação. A persistência depende do 2º turno (25/10) e, em 2027, da política fiscal; a reversão tem 27% de probabilidade no 4T26 (cauda worst).
- **E2, em destaque: o componente idiossincrático domina.** Em setembro, componente próprio de −2,7% contra +2,7% do global; em 05 e 06/10, −4,94% próprio contra −0,05% global; em três meses, −4,39% próprio contra +0,31% global (em log). A apreciação veio de dentro, e com queda de prêmio de risco, não de alta.
- **E3: repasse.** No Brasil, cerca de 17% de uma variação cambial chegam ao IPCA em 12 meses, contra repasse integral nos preços no atacado (Belaisch, 2003)[^17]. A apreciação atua primeiro nos comercializáveis (2,52% em 12 meses, `inflc_agregados`, ago) e quase nada nos administrados; ela vem no sentido contrário ao do choque do petróleo, que pressiona os combustíveis.
- **E4: a PTAX está 3,5% abaixo do condicionante do Copom** (R$ 5,15 na 281ª reunião), e a central do 4T26, 1,9% abaixo. O desvio é para o lado da apreciação, e o risco que o Copom lista é o de um câmbio "persistentemente mais depreciado"; por isso não está em destaque. Pelo procedimento descrito na ata, o condicionante da reunião de 04/11 sai da média de dez dias úteis encerrada na sexta-feira anterior à semana da reunião, janela que inclui o 2º turno.
- **E5, em destaque: o real e a curva de juros se moveram juntos contra os pares em 05/10, no sentido da compressão do prêmio de risco.** O CDS não registra a sessão (último dado 08/09), e o DI faz o papel de termômetro. O sentido é o oposto do estresse: o mesmo prêmio que em 05/10 caiu reduz o juro neutro que o mercado embute, se a queda se mantiver.
- **E6, em destaque: carry e real se descolaram.** Em 05/10 a curva passou a precificar menos carry à frente (Selic de 12,20% em dez/2027, contra 14,10% precificados em 04/09) e o real se apreciou 4,66%. Quem sustenta o real agora é a queda do prêmio de risco, não o carry. Em setembro foi o contrário: o carry, o maior dos pares em relação à volatilidade (0,83), e o petróleo seguraram o real contra o dólar global.
- **E7, em destaque: o BC vendeu US$ 3 bi à vista e US$ 1 bi em linha entre 31/08 e 22/09** (`cmb_reservas_bc`), num mês em que a PTAX ficou estável. A venda de 14/09 coincidiu com a maior alta diária do período (+1,52%). Os bancos estavam vendidos à vista em US$ 22,1 bi em agosto. O cupom cambial não está nos dados, então não há como confirmar se houve escassez de dólar no mercado local.

**Pedidos**

- **S1 (política monetária).** Qual o caminho esperado da Selic, reunião a reunião, até o fim de 2027, e o balanço de riscos? A curva de 06/10 precifica 13,26% em dez/2026 e 12,20% em dez/2027; a Focus de 25/09, anterior a 05/10, dá 13,50% e 12,00%. Depende disso: o canal de carry em todos os trimestres e a central de 3T27 a 1T28, que assume diferencial acima de 8 p.p.
- **S2 (política monetária).** Se o Copom acelerar os cortes depois da queda do prêmio de risco, com a inflação projetada em 5,2% no 4T26, o mercado lerá isso como credibilidade (real estável) ou como afrouxamento com inflação acima da meta (real mais fraco)? Depende disso: a cauda worst de 2027, que assume diferencial abaixo de 7,5 p.p. lido como perda de credibilidade.
- **S3 (política monetária).** O Copom vê a apreciação de outubro como mudança de cenário? O RPM de setembro atribuiu a depreciação anterior à queda do diferencial de juros e partiu de R$ 5,15. Depende disso: a resposta a E4 e se a central do 4T26 (5,05) fica dentro ou fora do cenário do Copom.
- **S4 (política monetária).** Na cauda worst do 4T26 (PTAX acima de 5,25 depois do 2º turno), o Copom interromperia os cortes? O BC usaria swaps ou venda à vista, e em que escala? Depende disso: o tamanho do desvio de estresse de regime (+5%) e a duração de dois trimestres.
- **Pedido deste ciclo (política monetária).** Leitura da reunião de 04/11/2026: o passo de 25 p.b. precificado na curva se mantém, e qual o condicionante cambial? Depende disso: o caminho do carry no 4T26 e a resposta a E4 na rodada 2.
- **Pedido deste ciclo (fiscal, quando houver agente).** O que o novo governo precisa apresentar em 2027 para estabilizar a dívida bruta, hoje em 82,9% do PIB e subindo 5,5 p.p. em 12 meses? Depende disso: o caminho do CDS de 2T27 a 1T28 e a cauda worst de 2027.

## 5. Placar

Primeiro ciclo.

[^1]: Os dados não trazem informação eleitoral. As datas do 1º turno (04/10/2026) e do 2º turno (25/10/2026) são do calendário eleitoral público; o resultado do 1º turno não é usado nesta análise, só a reação dos preços na sessão seguinte.
[^2]: O Modelo Estrutural ainda não recebe os caminhos dos agentes. A central de cada trimestre é a leitura do agente sobre como os caminhos de canal da seção 3 se combinam; quando o modelo entrar, ele dará a PTAX condicional a esses caminhos, e os desvios qualitativos se somam a ela.
[^3]: Percentil: posição do valor de hoje no histórico, de 0 (o menor já visto) a 100 (o maior). No volume interbancário, quanto maior o percentil, mais líquido o mercado em relação ao passado.
[^4]: Leilão de linha: o BC vende dólares com compromisso de recomprá-los numa data futura. Dá liquidez em dólar por um período sem reduzir as reservas de forma permanente, ao contrário da venda à vista.
[^5]: O cupom cambial (o juro em dólar no mercado brasileiro) e a volatilidade implícita do real não estão na lista de dados deste ciclo.
[^6]: Neste caso, quanto maior o percentil, mais comprados em real estão os fundos. Posicionamento extremo é lido como sinal contrário: quando os fundos já estão muito comprados em real, sobra pouco comprador novo, e uma notícia ruim provoca venda em bloco (Verde, §5.3; Kapitalo, §6.8).
[^7]: O CDS de 5 anos tem o último dado em 08/09/2026, 29 dias antes do corte, e não reflete a sessão de 05/10. O caminho de base parte de um nível estimado pelo agente, não observado.
[^8]: Deterioração fiscal gradual costuma não aparecer no preço no curto prazo, mas é mais perigosa quando os prêmios de risco já estão baixos, porque deixa pouca folga para uma reprecificação súbita (Verde, §1.11).
[^9]: O Brasil é exportador líquido de petróleo. Quando o petróleo sobe, a balança comercial e a arrecadação melhoram, enquanto a maioria dos emergentes, importadores de energia, perde; o capital tende a migrar para os exportadores (Verde, §2.4; Kapitalo, §4.3).
[^10]: Nem todo fluxo de entrada tem a mesma qualidade: o investimento direto é o mais estável e a dívida em moeda estrangeira, o mais frágil. Um déficit em conta corrente coberto por investimento direto é o caso mais confortável.
[^11]: No índice de câmbio real efetivo do BIS, alta significa apreciação do real contra a cesta de parceiros comerciais, já descontada a inflação de cada um.
[^12]: O beta mede quanto o real se move, em média, quando o dólar sobe 1% contra as moedas emergentes: com beta de 1,37, uma alta de 1% do dólar costuma vir com desvalorização de 1,37% do real. A parte do movimento que o beta explica é a "global"; o resto é a "própria" do real. A sensibilidade foi estimada em dados diários de jul/2024 a jun/2026 e explica cerca de um terço da variação diária do real. As contas estão em variação logarítmica, que para movimentos pequenos é quase igual à variação percentual.
[^13]: O forward é o preço do dólar para uma data futura, travado hoje. Ele fica acima do dólar à vista na proporção da diferença de juros: com o dólar a R$ 4,97 e juros de cerca de 12,5% ao ano aqui e 4,6% nos EUA nesse prazo, o dólar para o fim de março de 2028 é negociado perto de R$ 5,53. Uma central abaixo do forward é a aposta de que o juro a mais compensa o que o real perder no período. Aqui o forward foi aproximado com a curva de DI e os juros americanos, porque o cupom cambial não está nos dados.
[^14]: No cenário de referência, o Copom não projeta o câmbio: parte da média recente da cotação (R$ 5,15 na reunião de 16/09) e a corrige pela paridade do poder de compra, isto é, pela diferença entre a inflação daqui e a de fora (comunicado e ata da 281ª reunião; RPM de setembro de 2026).
[^15]: Para cada trimestre, a variação da PTAX em todos os períodos de mesma duração, em dias úteis, nos últimos dez anos, centrada na central da tese. A distribuição histórica é assimétrica para o lado da depreciação e inclui 2020 e 2024; ela dá o tamanho das faixas, e a probabilidade de cada cauda foi ajustada pelo agente a partir dela.
[^16]: Intervenção como colchão temporário: a venda de dólares pelo BC atenua a pressão de saída, mas não a elimina enquanto a causa continua; compra tempo (Verde, §7.2).
[^17]: Repasse cambial é a parte de uma variação do câmbio que chega aos preços. No Brasil de 1999–2002, cerca de 17% de uma depreciação chegavam ao IPCA em 12 meses, enquanto os preços no atacado subiam mais que a própria depreciação: quase todo o choque é absorvido nas margens da cadeia antes de chegar ao consumidor (Belaisch, 2003).
