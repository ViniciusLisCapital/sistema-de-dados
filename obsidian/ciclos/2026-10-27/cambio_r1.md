# Report — câmbio · ciclo 2026-10-27 · rodada 1

Dados até: 27/10/2026 (PTAX até 26/10) · Horizontes: 4T26 a 1T28, USD/BRL pela PTAX de venda do último dia útil de cada trimestre[^ptax]

## 1. Tese

| Variável | Trimestre | Central | Base: faixa · P | Upside: limite · P | Downside: limite · P | P(up) − P(down) |
|---|---|---|---|---|---|---|
| USD/BRL, PTAX de fechamento | 4T26 | 5,38 | 5,25 a 5,60 · 45% | acima de 5,60 · 33% | abaixo de 5,25 · 22% | +0,11 |
| | 1T27 | 5,39 | 5,20 a 5,65 · 45% | acima de 5,65 · 32% | abaixo de 5,20 · 23% | +0,09 |
| | 2T27 | 5,37 | 5,15 a 5,65 · 46% | acima de 5,65 · 29% | abaixo de 5,15 · 25% | +0,04 |
| | 3T27 | 5,35 | 5,10 a 5,65 · 46% | acima de 5,65 · 28% | abaixo de 5,10 · 26% | +0,02 |
| | 4T27 | 5,35 | 5,10 a 5,65 · 45% | acima de 5,65 · 30% | abaixo de 5,10 · 25% | +0,05 |
| | 1T28 | 5,38 | 5,10 a 5,70 · 46% | acima de 5,70 · 27% | abaixo de 5,10 · 27% | 0,00 |

- **Upside (real mais fraco, ruim para a inflação e para o Brasil):** o choque de 26/10 se aprofunda. CDS a 185 p.b. no 4T26 e 200 no 1T27, volatilidade implícita a 24% e dólar contra emergentes a 132,5 dão 5,78 no modelo no 4T26; com o peso do CDS × 1,2, 5,83; com a desmontagem de posição comprada em real (+2%) e o BC vendendo dólar (−1,5%), 5,86.
- **Downside (real mais forte, bom para a inflação):** o prêmio de 26/10 se desfaz. CDS de volta a 118 (o nível de 22/10), volatilidade a 13%, dólar contra emergentes a 128,5 e IC-Br a 210 dão 5,13 no modelo no 4T26, sem tempero.
- **A tese em uma frase:** o salto de 26/10 é idiossincrático e, em boa parte, persistente; o modelo põe o real perto de 5,38 em todo o horizonte, abaixo dos 5,50 de hoje porque não vê a saída sazonal de dezembro nem a posição comprada em real que o choque pegou, e por isso o risco do 4T26 e do 1T27 pende para a depreciação.

## 2. Argumentação

### Q3 — O que explica a dinâmica recente

**Um pregão explica o mês.** A PTAX foi de 5,0377 em 23/10 a 5,5007 em 26/10, +9,19% num pregão (`cmb_ptax`), a terceira maior alta diária desde 1994, atrás de 15/01/1999 e 08/10/2008 (`cmb_ptax`). Desde o ciclo anterior (22/10) a alta é de +9,18%, e desde o fechamento do 3T26 (5,1809 em 30/09), de +6,17%. Antes disso o real tinha se apreciado: −2,75% de 30/09 a 22/10, concentrado em outro pregão de salto, 05/10, de −4,55% (`cmb_ptax`). O F não traz a causa de nenhum dos dois; os dois vêm depois de um fim de semana e foram pedidos ao agente web[^processo].

**O movimento de 26/10 é idiossincrático, por eliminação do global.** No mesmo pregão o DXY subiu 0,15% (`cmb_dollar_index` · 26/10) e o S&P 500, 0,70% (`cmb_equity_us` · 26/10), o que mostra que não houve fuga de risco global; desde 22/10 o DXY sobe 0,59% (até 27/10) e o dólar contra emergentes fica estável, −0,05% de 22/10 a 23/10 (`cmb_dollar_index_em`). O real andou com os preços domésticos, porque no mesmo pregão o CDS subiu 18 p.b. (`cmb_risco_pais`), o DI de 1 ano 171 p.b. e o de 2 anos 252 p.b. (`br_di_grade`). Mas falta a prova pelos pares: o peso mexicano, o chileno, o colombiano e o sol têm dado só até 15–20/10 (`cmb_fx_latam`), então a comparação de 26/10 contra a América Latina não é possível neste ciclo; ela mudaria a conclusão só se os pares tivessem caído junto num dia em que o DXY ficou parado, o que é improvável. O modelo dá a mesma leitura: com o CDS de 22/10 (118,3) ele põe o 4T26 em 5,154; com o de 26/10 (137,4), em 5,238, ou seja, o canal de risco fiscal explica +1,63% dos +9,18% (`cmb_risco_pais`, Modelo Estrutural). O resto é prêmio que as variáveis do modelo não carregam, e parte dele pode estar na volatilidade implícita, que o F não traz[^vol].

**No mês anterior ao salto o real foi melhor que os pares, e por motivo próprio.**[^split]

| De 30/09 até o último dado | Variação (moeda por dólar) | Último dado |
|---|---|---|
| Real | −2,75% | 22/10 |
| Peso mexicano | +2,18% | 20/10 |
| Peso chileno | +0,95% | 19/10 |
| Peso colombiano | −4,30% | 15/10 |
| Sol peruano | +0,22% | 19/10 |
| Dólar contra emergentes | +0,70% | 22/10 |
| DXY | +0,16% | 22/10 |

Fonte: `cmb_ptax`, `cmb_fx_latam` (chileno e colombiano na taxa formada no dia), `cmb_dollar_index_em`, `cmb_dollar_index`.

O dólar subiu contra os emergentes e o real caiu contra o dólar, o que mostra um componente idiossincrático de apreciação; ele se concentrou em 05/10, quando o real caiu 4,55% com o CDS a −12 p.b. e o DI de 2 anos a −110 p.b., enquanto o DXY subia 0,24% (`cmb_ptax`, `cmb_risco_pais`, `br_di_grade`, `cmb_dollar_index`). De 05/10 a 22/10 o real devolveu só 1,05% (`cmb_ptax`). Em três meses, a alta do real (+8,34% de 31/07 a 26/10) parece com a do peso mexicano (+6,62%) e a do chileno (+5,76%, os dois até 19–20/10), mas a semelhança engana: em 22/10 a PTAX (5,0383) ainda estava abaixo da de 31/07 (5,0773), então os três meses do real são o pregão de 26/10, e o dos pares, um movimento lento, com DXY +2,42% e dólar contra emergentes +1,46% no período (`cmb_ptax`, `cmb_fx_latam`, `cmb_dollar_index`, `cmb_dollar_index_em`).

**A expectativa ainda não viu o salto.** A mediana do Focus para o fim de 2026 era 5,05 em 23/10, revisada de 5,20 quatro semanas antes (`expc_focus_periodo` câmbio), e a pesquisa foi fechada antes de 26/10: a PTAX de 5,50 está bem acima dela. O que mostra se o mercado trata o salto como permanente é a revisão do Focus de 30/10 (S10).

### Q1 — Condições do mercado de câmbio

**Mercado fino.** O volume interbancário D+2 teve média de US$ 985 mi/dia no último mês, contra US$ 1.508 mi na média de 12 meses, percentil 19 em 10 anos[^pctl] (`cmb_ptax` · 23/10), o que ajuda a explicar por que um choque de preço virou 9% num pregão. Mas o D+1 está no percentil 67 (média de US$ 326 mi/dia), então não é falta de liquidez em todo prazo.

**Escassez de dólar à vista antes do choque, e o BC já tinha agido.** Os bancos fecharam setembro vendidos em US$ 26,2 bi no mercado à vista, US$ 4,1 bi mais vendidos que em agosto, percentil 24 em 10 anos (`cmb_reservas_bc` · set)[^posbancos], e o BC respondeu em setembro com US$ 2 bi em leilões de linha e US$ 2 bi em venda à vista (`cmb_reservas_bc` · set). Em outubro, até 26/10, não há intervenção registrada, nem no pregão do salto, e as reservas estão em US$ 364,9 bi, estáveis no mês (`cmb_reservas_bc` · 26/10). O BC deixou o preço andar 9% sem intervir, o que, se o dado de 26/10 estiver completo, mostra que ele não leu disfunção; a confirmação é pedida ao agente web.

**Posição muito comprada em real quando o choque veio.** Em 20/10 os fundos alavancados estavam comprados em 18.677 contratos (percentil 96 em 10 anos, +17.002 em três meses) e os asset managers em 51.268 (percentil 85), juntos 69.945 contratos, percentil 95 em 10 anos; os dealers, do outro lado, vendidos em 65.413 (percentil 4), e as posições em aberto em 135.679, percentil 98 (`cmb_cot_fx` · 20/10). Posição extrema é sinal contrário[^cot]: o choque pegou o mercado comprado, e uma desmontagem raramente cabe num pregão. Mas o dado é de seis dias antes do salto, e o próximo relatório da CFTC é o que diz se a posição já saiu; se tiver saído, o tempero de posicionamento da seção 3.2 cai.

**Fluxo: entrada antes do choque, sem dado depois.** De 1º a 16/10 o fluxo cambial foi positivo em US$ 5,15 bi, US$ 4,13 bi pelo financeiro (`cmb_cambio_contratado` · 16/10), o que é coerente com a apreciação pré-salto; setembro tinha sido negativo em US$ 5,20 bi, com o financeiro em −US$ 7,33 bi. O fluxo de 26/10 não está no F.

### Q2 — Fundamentos

**Carry alto, e mais alto depois do choque, mas o real se descolou dele.** O diferencial nominal Selic − Fed Funds era 10,00 p.p. em setembro e o real ex-post 9,14 p.p., percentil 81 em 10 anos (`diferenciais_juros` · set)[^carry]. O diferencial à frente subiu com o choque: DI de 1 ano menos a meta do Fed foi de 9,14 p.p. em 22/10 para 10,82 p.p. em 26/10 (`br_di_grade`, `us_interest_rate`). No pregão em que o carry à frente foi de 9,14 para 10,82 p.p., o real caiu 9%: o carry não sustentou a moeda. Isso pode querer dizer que a alta de juros precificada é lida como sinal de risco e não como aperto crível (S2, S7), e é essa leitura que decide se uma alta da Selic em 04/11 ou 09/12 aprecia ou não o real. A volatilidade também anulou parte do carry: o carry sobre a volatilidade realizada de 63 dias é 0,47, contra 0,37 do peso mexicano e 0,57 do colombiano ("O real e os pares" · 26/10), mas a volatilidade de 63 dias do real foi de 12,3% em 23/10 para 21,4% em 26/10 (`cmb_ptax`), percentil 96 em 10 anos.

**Contas externas não são o problema.** O déficit em transações correntes de 12 meses é de US$ 60,0 bi, 2,33% do PIB, e o investimento direto no país, de US$ 88,3 bi, 3,43% do PIB, percentil 93 (`cmb_balanco_pagmt` · set), o que mostra financiamento estável com folga. As exportações de bens somam US$ 376,6 bi em 12 meses, recorde (`cmb_balanco_pagmt` · set), e o saldo comercial do fluxo cambial, US$ 58,3 bi, percentil 93 (`cmb_cambio_contratado` · set). Mas a renda primária tem o maior déficit da série (−US$ 84,2 bi em 12 meses, percentil 0, `cmb_balanco_pagmt`) e o fluxo financeiro de 12 meses é de −US$ 62,3 bi, percentil 18 (`cmb_cambio_contratado` · set), com remessa de renda (−US$ 66,0 bi, percentil 6) e saída de capital de residentes (−US$ 49,6 bi, percentil 3): a saída financeira é estrutural e se concentra em dezembro (seção 3.2).

**Termos de troca bons, mas não são o que move o real agora.** O IC-Br em dólar está 12,8% acima de um ano antes, puxado por metais (+42,2%) e energia (+29,2%) (`comm_icbr_usd` · set), e o Brent médio de outubro, US$ 124,96, está 9,5% acima do de setembro (`comm_brent`); petróleo exportado somou US$ 54,1 bi em 12 meses, contra US$ 43,9 bi um ano antes (`cmb_comex_produto` · set). Mas os termos de troca da Funcex caíram 3,0% em três meses até agosto (`cmb_termos_troca`), e de 30/09 a 20/10 o Brent ficou estável (−0,6%) enquanto o real caía 2,75% e depois subia 9,18%: o canal de commodities não explica o mês.

**Valuation: neutra antes do choque, barata depois.** O câmbio real efetivo estava no percentil 53 em 10 anos em setembro (`cmb_reer` · set)[^reer], e a PTAX de 26/10 está 6,92% acima da média de setembro (5,1447, `cmb_ptax`). A leitura de setembro não carrega o salto; com ele, o real ficou mais barato que a sua média de 10 anos, o que sustenta o downside dos trimestres de 2027 e não entra no modelo.

### Q4 — Por que a central e por que a distribuição

**A central.** No cenário base o modelo põe a PTAX em 5,38 no 4T26 e entre 5,35 e 5,39 até o 1T28 (seção 3.1). Sem nenhum caminho, o modelo daria 5,21 no 4T26, porque segura as exógenas no fechamento do 3T26; com CDS, dólar contra emergentes e S&P 500 no nível de hoje, 5,275; com a volatilidade implícita de 17% no 4T26, 5,381. A volatilidade é o canal que mais pesa, porque divide o carry: o mesmo diferencial atrai menos quando a moeda balança mais[^carry]. Depois do 4T26, a volatilidade recua (15,5% no 1T27 a 13,5% no 4T27) e devolve apreciação, mas a Selic do modelo cai de 13,43% no 4T26 para 12,22% no 1T28 e tira carry, e os dois quase se anulam: a central fica plana. Essa Selic é a da regra do modelo, que não vê a curva: o DI precifica Selic de 14,02% em dez/26 e 15,78% em dez/27, contra 13,58% e 14,02% um mês antes (`br_di_grade` · 26/10). Se a política monetária escrever um caminho de alta e ele for lido como crível, a central de 2027 cai (S1, S2).

**A distribuição.** A central fica 2,2% abaixo da PTAX de hoje, e três forças que o modelo não vê empurram o 4T26 para cima dela: a saída sazonal de dezembro, que sozinha leva a central a 5,49 (seção 3.2); a posição comprada em real de 20/10; e o resto do prêmio de 26/10 que o CDS não explica. Contra elas, o real ficou barato e o BC tem US$ 365 bi de reservas e já interveio em setembro com a PTAX entre 5,12 e 5,21. Mas uma volta rápida ao nível de 22/10 é menos provável que a permanência, porque o choque de 05/10, no sentido contrário, ficou quase inteiro por três semanas. Por isso a faixa base do 4T26 vai de 5,25 a 5,60, contém a central e a PTAX de hoje, e o upside (33%) pesa mais que o downside (22%). Em 2027 a sazonalidade só volta no 4T27, a posição já terá se ajustado e a valuation passa a pesar: a assimetria cai para perto de zero no 1T28, e as faixas abrem porque a incerteza cresce com o horizonte.

**O que derrubaria a tese:** a PTAX abaixo de 5,25 por duas semanas com o CDS de volta a 120 p.b. leva a probabilidade para o downside; o CDS acima de 170 p.b. ou a PTAX acima de 5,70 por uma semana, sem intervenção do BC, leva o 4T26 para o upside.

### Olhado, sem sinal

- Estoque de swaps cambiais · −US$ 91,6 bi (`cmb_reservas_bc` · ago) · dado de agosto, anterior ao choque · diria algo com o dado de outubro, se o BC ampliar a oferta.
- Reservas no conceito de liquidez · US$ 368,9 bi (`cmb_reservas_bc` · 26/10) · +1,0 no mês, sem venda · diria algo se caíssem com leilões à vista.
- Volume interbancário D+1 · US$ 326 mi/dia, percentil 67 (`cmb_ptax` · 23/10) · normal · diria algo se secasse junto com o D+2.
- Carteira, ações · −US$ 5,3 bi em 12 meses, percentil 10 (`cmb_balanco_pagmt` · set) · saída lenta, sem mudança no mês · diria algo se a saída de setembro (−US$ 2,1 bi) se repetir em outubro, com o choque.
- Exportação para os EUA · US$ 35,8 bi em 12 meses contra US$ 40,4 bi um ano antes (`cmb_comex_pais` · set) · compensada pela China · diria algo se a queda chegasse ao saldo total.
- Peso mexicano e posição em MXN · asset managers vendidos em 24.064 contratos, percentil 0 (`cmb_cot_fx` · 20/10) · história do México, sem efeito no real neste ciclo · diria algo se a venda se espalhasse para o real.
- Treasury de 10 anos · 5,00% (`us_interest_rate` · 23/10) · −0,11 p.p. no mês · diria algo se a alta de 12 meses (+0,99 p.p.) voltasse.

## 3. Premissas

### 3.1 Etapa 1 — o modelo

**Cenários.**
- **Base:** o prêmio de risco de 26/10 fica; a volatilidade sobe no 4T26 e volta devagar ao normal ao longo de 2027; o bloco global fica onde está. A causa do choque (pedida ao agente web) não reverte.
- **Upside:** o choque se aprofunda: o prêmio de risco sobe (CDS a 185 no 4T26 e 200 no 1T27, cedendo devagar), a volatilidade fica perto dos níveis de 2015 e há algum contágio para os emergentes.
- **Downside:** o prêmio volta ao de antes de 26/10, como o choque de 05/10 se manteve no sentido contrário; a volatilidade volta aos níveis de 2025–2026, o dólar cede contra emergentes e as commodities sobem.

**Caminhos das exógenas.** A volatilidade implícita é minha (principal). As outras são de outros agentes: o CDS do fiscal (aguarda fiscal, S6); dólar contra emergentes, S&P 500, IC-Br, Fed Funds e CPI dos EUA do externo (aguarda externo, S8). Para rodar a rodada 1, pus o 4T26 dessas no nível do último dado do F e segurei; elas não vão no JSON e não entram no P.

| Exógena | Hoje (valor · tabela · data) | Cenário | 4T26 | 1T27 | 2T27 | 3T27 | 4T27 | 1T28 |
|---|---|---|---|---|---|---|---|---|
| Volatilidade implícita do real (% a.a.) · principal: câmbio | sem dado no F; 12,19 no 2T26 (Modelo Estrutural) | base | 17,0 | 15,5 | 14,5 | 14,0 | 13,5 | 13,5 |
| | | upside | 24,0 | 21,0 | 18,0 | 16,0 | 15,0 | 15,0 |
| | | downside | 13,0 | 12,5 | 12,0 | 12,0 | 12,0 | 12,0 |
| CDS 5 anos (p.b.) · aguarda fiscal | 137 · `cmb_risco_pais` · 26/10 | base | 137 | 137 | 137 | 137 | 137 | 137 |
| | | upside | 185 | 200 | 190 | 175 | 165 | 160 |
| | | downside | 118 | 115 | 115 | 115 | 115 | 115 |
| Dólar contra emergentes (pontos) · aguarda externo | 130,21 · `cmb_dollar_index_em` · 23/10 | base | 130,2 | 130,2 | 130,2 | 130,2 | 130,2 | 130,2 |
| | | upside | 132,5 | 132,5 | 132,5 | 132,5 | 132,5 | 132,5 |
| | | downside | 128,5 | 128,5 | 128,5 | 128,5 | 128,5 | 128,5 |
| S&P 500 (pontos) · aguarda externo | 7.717 · `cmb_equity_us` · 27/10 | base, upside, downside | 7.717 | 7.717 | 7.717 | 7.717 | 7.717 | 7.717 |
| IC-Br em dólar (pontos) · aguarda externo | 205,70 · `comm_icbr_usd` · set | base, upside | padrão (205,70) | | | | | |
| | | downside | 210,0 | 210,0 | 210,0 | 210,0 | 210,0 | 210,0 |
| Fed Funds efetivo (% a.a.) · aguarda externo | 3,75 · `diferenciais_juros` · set | todos | padrão (3,75) | | | | | |
| CPI dos EUA (% no trimestre) · aguarda externo | 3,72 em 12 meses · `diferenciais_juros` · set | todos | padrão (média de 4 trimestres, 0,91) | | | | | |

Motivo do caminho da volatilidade (base). O F não traz a volatilidade implícita, e o modelo não tem o dado do 3T26 (segura 12,19, do 2T26). Estimei o nível pela realizada: de 2006 a 2026, a implícita de fim de trimestre se explica pela realizada de 21 e de 63 dias com erro de 2,1 p.p. (82 trimestres; `cmb_ptax` e a série do Modelo Estrutural), e essa relação põe a implícita de hoje perto de 25% e a do fim do 3T26 em 12,3%. Os 25% de hoje vêm de um pregão só, que domina a janela de 21 dias; no fechamento do 4T26 a janela de 63 dias ainda conterá 26/10, e há duas reuniões do Copom no trimestre (04/11 e 09/12, `pm_copom_calendario`). Por isso 17%, perto do percentil 75 da implícita trimestral desde 2006 (17,7%; mediana 14,3%). Depois de picos, a implícita recuou em um a três trimestres (21,6 → 14,6 do 3T18 ao 4T18; 22,7 → 21,9 → 19,3 do 2T20 ao 4T20), e o caminho volta à mediana no 2T27 e fica um pouco abaixo dela, perto dos níveis de 2025–2026 (11,5 a 13,9), no fim do horizonte. No upside, a persistência é a de 2015 (25,1 → 22,8 → 21,8); no downside, a volta rápida de 2018.

Motivo do downside no CDS: 118 é o fechamento de 22/10 (`cmb_risco_pais`), o nível de antes do choque.

**Saída do modelo** (central; a faixa de 90% do posterior dos pesos está no G e não inclui o erro da equação, de ~3,6% por trimestre)[^modelo].

| Variável | Cenário | 4T26 | 1T27 | 2T27 | 3T27 | 4T27 | 1T28 |
|---|---|---|---|---|---|---|---|
| PTAX (R$/US$) | base | 5,381 | 5,387 | 5,371 | 5,346 | 5,350 | 5,375 |
| | upside (com × 1,2 no CDS) | 5,829 | 5,911 | 5,818 | 5,684 | 5,627 | 5,625 |
| | upside (sem multiplicador) | 5,776 | 5,844 | 5,761 | 5,643 | 5,595 | 5,598 |
| | downside | 5,130 | 5,141 | 5,131 | 5,117 | 5,132 | 5,156 |
| Selic de fechamento (% a.a.) | base | 13,43 | 13,12 | 12,85 | 12,61 | 12,40 | 12,22 |
| | upside | 13,44 | 13,14 | 12,89 | 12,68 | 12,50 | 12,33 |
| | downside | 13,43 | 13,10 | 12,82 | 12,57 | 12,34 | 12,15 |
| IPCA 12 meses (%) | base | 5,30 | 4,91 | 4,41 | 4,42 | 4,29 | 4,11 |
| | upside | 5,35 | 5,07 | 4,66 | 4,70 | 4,51 | 4,23 |
| | downside | 5,27 | 4,82 | 4,28 | 4,27 | 4,15 | 4,01 |

Faixa de 90% do posterior da PTAX base: 5,300 a 5,464 no 4T26 e 5,154 a 5,623 no 1T28.

### 3.2 Etapa 2 — o tempero

**(i) CDS 5 anos — efeito mais forte que o estimado** · cenário upside
- Coeficiente: estimado 25,1 por desvio-padrão da variação, intervalo de 90% do posterior 19,5 a 30,6. Multiplicador: × 1,2 (30,1), dentro do intervalo, percentil 94 do posterior.
- Efeito: PTAX do upside de 5,78 para 5,83 no 4T26 e de 5,84 para 5,91 no 1T27.
- Por quê: o modelo é linear na variação do CDS e o estresse não é. Em 26/10 o CDS subiu 18 p.b. e o modelo atribui a isso +1,63% (seção 2, Q3), contra +9,18% observado: num choque de prêmio, o real reagiu muito mais do que o canal estimado sobre 2006–2026. Fico dentro do intervalo porque uma observação não basta para afirmar que o histórico subestima o canal; o fiscal argumenta pelo peso (S6), e eu aplico.
- Onde entra: limite do upside.

**(ii) Saída sazonal de dezembro — fluxo financeiro** · cenário base (4T26 e 4T27)
- Hoje: o fluxo financeiro de dezembro teve média de −US$ 11,9 bi de 2010 a 2025, e novembro mais dezembro, −US$ 13,1 bi, contra −US$ 5,6 bi de dois meses quaisquer; em 2024 e 2025 foram −US$ 31,4 bi e −US$ 26,8 bi (`cmb_cambio_contratado`).
- Por que o modelo não vê: a equação (F) não tem termo sazonal, e o resíduo dela no 4º trimestre foi positivo em 8 dos 9 anos desde 2017, com média de +2,1% (Modelo Estrutural)[^sazonal]. Na amostra inteira a média é +0,3% e não se distingue de zero, então é um efeito recente, que coincide com a remessa de renda recorde (seção 2, Q2).
- Efeito: +2,1% sobre o modelo no trimestre de dezembro, uma vez por ano: 5,38 → 5,49 no 4T26 e 5,35 → 5,46 no 4T27.
- Onde entra: assimetria do base no 4T26 e no 4T27 (não move a central).

**(ii) Posicionamento — desmontagem da posição comprada em real** · cenários base e upside
- Hoje: fundos alavancados e asset managers comprados em 69.945 contratos, percentil 95 em 10 anos; posições em aberto no percentil 98 (`cmb_cot_fx` · 20/10).
- Por que o modelo não vê: nenhuma exógena da (F) mede posição; o canal é a velocidade com que quem estava comprado sai, num mercado à vista fino (D+2 no percentil 19).
- Efeito: +2% no 4T26 e +1% no 1T27 no upside; no base, entra como assimetria nos mesmos trimestres. Cai se o COT de 27/10 mostrar a posição já reduzida.
- Onde entra: limite do upside e assimetria do base no 4T26 e no 1T27.

**(ii) O BC no mercado de câmbio — venda à vista e linhas** · cenário upside
- Hoje: reservas de US$ 364,9 bi (`cmb_reservas_bc` · 26/10); em setembro o BC vendeu US$ 2 bi à vista e US$ 2 bi em linhas com a PTAX entre 5,12 e 5,21 nos dias dos leilões (`cmb_reservas_bc`, `cmb_ptax`); nenhuma intervenção registrada em outubro até 26/10.
- Por que o modelo não vê: a intervenção não é exógena da (F).
- Efeito: −1,5% no 4T26 e −1% no 1T27, só no upside: num mercado disfuncional o BC vende, e isso limita a cauda, não a elimina.
- Onde entra: limite do upside.

### 3.3 Da etapa 1 à tese

| Trimestre | Central (modelo, base) | Upside: modelo → com tempero | Downside: modelo → com tempero |
|---|---|---|---|
| 4T26 | 5,38 | 5,78 → 5,83 (CDS × 1,2) → 5,86 (posição +2%, BC −1,5%) | 5,13 → 5,13 |
| 1T27 | 5,39 | 5,84 → 5,91 → 5,91 (posição +1%, BC −1%) | 5,14 → 5,14 |
| 2T27 | 5,37 | 5,76 → 5,82 | 5,13 → 5,13 |
| 3T27 | 5,35 | 5,64 → 5,68 | 5,12 → 5,12 |
| 4T27 | 5,35 | 5,60 → 5,63 | 5,13 → 5,13 |
| 1T28 | 5,38 | 5,60 → 5,63 | 5,16 → 5,16 |

O limite superior de cada faixa base fica entre a central e o upside do modelo, perto da metade do caminho no 4T26 (5,60) e mais perto da central nos trimestres seguintes; o inferior fica entre a central e o downside. No 4T26 a central com a sazonalidade (5,49) e a PTAX de hoje (5,50) caem dentro da faixa e acima da central, e a posição comprada pesa para o mesmo lado: é daí que vêm os 33% de upside contra 22% de downside. Do 2T27 em diante as três forças de cima perdem peso, a valuation entra contra elas e a assimetria vai a zero, menos no 4T27, onde a sazonalidade volta.

## 4. Para os outros agentes

**Respostas às entradas fixas**

- **E1, em destaque (persistência):** o salto de 26/10 é, na maior parte, persistente: veio com o DI de 2 anos +252 p.b. e o CDS +18 p.b. no mesmo pregão, o que é repreço de prêmio e não ruído de fluxo, e o choque de 05/10, no sentido contrário, ficou quase inteiro por três semanas. A central fica em 5,35–5,39 em todo o horizonte, contra 5,04 em 22/10. O julgamento depende da causa (agente web) e de S2/S7.
- **E2, em destaque (global ou idiossincrático):** idiossincrático. Em 26/10, DXY +0,15% e S&P +0,70% contra real +9,19%; o modelo atribui +1,63% ao CDS e nada ao bloco global. Os pares não têm dado depois de 20/10 (seção 2, Q3).
- **E3, em destaque:** a PTAX de 5,50 está acima do Focus de 2026 (5,05, pré-choque) e se afasta de qualquer trajetória compatível com a PPC; o mapa registra que o comunicado da 281ª reunião lista "uma taxa de câmbio persistentemente mais depreciada" entre os riscos de alta. A premissa condicionante do Copom (valor e forma) aguarda política monetária (S3).
- **E4, em destaque:** CDS e real andaram juntos em 26/10 contra o DXY parado; contra os pares, falta dado. Se o prêmio é fiscal, é do fiscal (S6).
- **E5, em destaque:** carry e real se descolaram: o DI de 1 ano menos a meta do Fed subiu de 9,14 para 10,82 p.p. e o real caiu 9% no mesmo pregão (seção 2, Q2).
- **E6:** sem disfunção registrada: nenhuma intervenção até 26/10 e reservas estáveis; mas o D+2 está no percentil 19 e os bancos estavam vendidos em US$ 26,2 bi à vista em setembro. O cupom cambial não está no dado. Não marco em destaque porque a condição do mapa (intervenção ou pico do cupom) não aconteceu.
- **E7 (inflação):** a tese por trimestre (seção 1) e E1.
- **E8, em destaque (inflação):** risco relevante de depreciação: upside de 33% no 4T26 e 32% no 1T27, acima de 5,60–5,65, puxado por prêmio de risco e posição, idiossincrático (E2). No upside do modelo o IPCA de 12 meses do 1T27 vai a 5,07%, contra 4,91% no base; o repasse é do agente de inflação.
- **E9 (atividade):** a tese e E1: câmbio persistentemente mais depreciado, central de 5,35–5,39 contra 5,04 em 22/10.
- **E10 (atividade):** termos de troca: preço a favor (IC-Br +12,8% em 12 meses, petróleo exportado de US$ 43,9 bi para US$ 54,1 bi), mas Funcex −3,0% em três meses até agosto; o F não traz volume para separar preço de quantidade.
- **E11, em destaque (fiscal):** o idiossincrático domina e o CDS subiu junto (+18 p.b. em 26/10); é a confirmação de mercado que o mapa pede, com a ressalva de que a comparação contra os pares falta.
- **E12 (fiscal):** a tese; operações do BC: US$ 2 bi à vista e US$ 2 bi em linhas em setembro, nada em outubro até 26/10, swaps em −US$ 91,6 bi (agosto).
- **E13, em destaque (externo):** idiossincrático (E2). O índice de dólar contra emergentes de 26/10 em diante vai conter o salto do real e não deve ser lido como movimento global.
- **E14 (externo):** fluxo financeiro positivo em US$ 4,13 bi até 16/10 e posição comprada em real no percentil 95 em 20/10: o apetite chegou ao Brasil por dinheiro e por posição antes do choque.
- **E15 (expectativas):** persistente e idiossincrático (E1, E2), com a tese por trimestre; é o caso que o mapa descreve como o que chega aos horizontes longos.

**Pedidos**

- **S1 (política monetária):** qual o caminho da Selic de fechamento por trimestre até o 1T28, e reunião a reunião para 04/11 e 09/12? O modelo corta até 12,22% no 1T28 e a curva precifica 15,78% em dez/27. Depende disso o carry da central de 2027; se o seu caminho for de alta, argumente pelos multiplicadores da regra (R), que não são meus.
- **S2 (política monetária):** uma alta em 04/11 ou 09/12 seria lida como credibilidade ou como validação de inflação mais alta? Em 26/10 o carry subiu e o real caiu. Decide se a alta reduz o upside de 2027.
- **S3 (política monetária):** como o Copom descreveu o câmbio na 281ª reunião e no RPM de setembro, e qual a premissa condicionante para o real (valor e como é fixada)? Os documentos não estão no meu retrato. Depende E3.
- **S4 (política monetária):** com a PTAX a 5,50, o Copom responderia com a Selic, e quanto? A ausência de intervenção em 26/10 muda a leitura da função de reação do BC? Depende o tempero do BC no upside.
- **S5 (inflação):** o caminho do IPCA de 12 meses por trimestre depois do salto, e de onde vêm as caudas. Entra na perna de PPC da (F).
- **S6 (fiscal):** o caminho do CDS (base e caudas) e se os +18 p.b. de 26/10 são fiscais. Usei 137 segurado no base, 185–200 no upside e 118 no downside, como premissa; argumente pelo peso do CDS, que eu aplico (× 1,2 no upside nesta rodada).
- **S7 (fiscal):** há risco de dominância fiscal, em que uma alta de juros sobe o prêmio em vez de sustentar o real? Junto com S2, decide o sinal juro → câmbio.
- **S8 (externo):** os caminhos de dólar contra emergentes, S&P 500, IC-Br em dólar, Fed Funds e CPI dos EUA. Usei os níveis de hoje segurados.
- **S9 (externo):** o ciclo global fora do modelo: houve algo global no fim de semana de 24–25/10, e o que fizeram os pares de 20 a 27/10? Depende E2.
- **S10 (expectativas):** quanto o Focus de 30/10 revisa o câmbio de fim de 2026 (5,05 em 23/10) e a Selic esperada. Separa surpresa de convergência.
- **Ao agente web:**
  1. O que aconteceu entre 23/10 e 26/10 que levou o real a +9,2%, o DI de 2 anos a +252 p.b. e o CDS a +18 p.b. em 26/10? É o resultado do 2º turno da eleição presidencial (25/10)? Se sim, o que o mercado leu nele (equipe econômica, arcabouço fiscal, falas do eleito). Depende E1 e a história dos três cenários.
  2. O mesmo para 03–04/10 (real −4,6% em 05/10). Depende a leitura de reversão do downside.
  3. O BC fez leilão à vista, de linha ou de swap em 26 ou 27/10, e algum diretor falou sobre o funcionamento do mercado de câmbio? Depende o tempero do BC e E6.
  4. Algum veículo publicou a volatilidade implícita de 3 meses do dólar contra o real depois de 26/10? Sou o principal dessa exógena e ela não está no F.
  5. O que o eleito ou a equipe dele anunciou, depois de 25/10, sobre meta fiscal, arcabouço e Banco Central? Depende o upside (CDS a 185–200).

**Como subordinado**

- **Dólar contra emergentes · principal: externo**
  - Insumos: em 26/10 o real subiu 9,19% com o DXY a +0,15% (`cmb_ptax`, `cmb_dollar_index`), então o salto é do real e não dos emergentes. De 30/09 a 20/10 o movimento dos emergentes foi concentrado na América Latina e no peso mexicano (+2,18%; +7,8% em um mês, `cmb_fx_latam`), com os asset managers vendidos em peso no percentil 0 (`cmb_cot_fx` · 20/10), enquanto o real se apreciava. O índice (130,21 em 23/10) ainda não tem o dado de 26/10.
  - Argumento: a leitura do índice do 4T26 deve descontar o real: a alta que ele mostrar em 26/10 é mecânica e não é sinal de dólar global. Não tenho argumento para um caminho acima ou abaixo do nível de hoje.
  - Caminho de referência: nenhum.
- **IC-Br em dólar · principal: externo**
  - Insumos: o Brent médio de outubro está 9,5% acima do de setembro (`comm_brent`), e a energia do IC-Br já subiu 10,6% em setembro (`comm_icbr_usd`); as exportações estão em recorde (US$ 376,6 bi em 12 meses, `cmb_balanco_pagmt`), com petróleo de US$ 43,9 bi para US$ 54,1 bi (`cmb_comex_produto`). O real não está seguindo as commodities neste mês (seção 2, Q2).
  - Argumento: o IC-Br de outubro deve vir acima de 205,70 pela energia, então o 4T26 segurado em 205,70 é baixo; não sei quanto, porque o F não traz os pesos da cesta. O efeito no real é pequeno perto do prêmio de risco.
  - Caminho de referência: nenhum.

## 5. Placar

Não há report final anterior do câmbio: o ciclo de 22/10 não tem `cambio_rf`. O 3T26 fechou com a PTAX em 5,1809 (30/09, `cmb_ptax`), sem tese final em vigor para conferir.

## 6. Sobre o modelo

Ciclo sem literatura: as propostas vêm do dado e do mapa.

| Fonte | O que sugere | Teste proposto | Por que importa para a tese deste ciclo |
|---|---|---|---|
| Resíduo da (F) por trimestre (Modelo Estrutural, 2006–2026) e fluxo financeiro de dezembro (`cmb_cambio_contratado`) | Dummy de 4º trimestre, ou o fluxo financeiro de nov–dez como regressor, com quebra em 2017 | Reestimar a (F) com a dummy na amostra inteira e com interação pós-2017; mudar se a dummy pós-2017 tiver intervalo de 90% acima de zero e o erro fora da amostra de 2021–2025 cair | A central do 4T26 fica 2,2% abaixo da PTAX de hoje, e a sazonalidade explica quase tudo; hoje ela é tempero |
| Volatilidade implícita sem 3T26 e fora do banco (mapa, 2.7; modelo segura 12,19) | Trazer a implícita para o banco (API Bloomberg prevista para 01/11); até lá, preencher o trimestre faltante pela realizada (implícita ≈ 6,65 + 0,274 × realizada 21d + 0,389 × realizada 63d, erro 2,1 p.p.) | Comparar a (F) estimada com a implícita preenchida contra a atual nos trimestres em que as duas existem; adotar se o coeficiente do carry/vol não mudar fora do intervalo | Sou o principal da vol e escrevi o caminho sem o dado de hoje; o canal carry/vol é o que mais move a central do 4T26 |
| Pregão de 26/10: CDS +18 p.b., modelo +1,63%, observado +9,18% | Não linearidade no prêmio: interação ΔCDS × nível da volatilidade, ou dummy de episódios eleitorais | Estimar com a interação na amostra 2006–2026; mudar se ela entrar com sinal positivo e intervalo fora de zero, e se os resíduos de 2008T4, 2015T3 e 2018T3 caírem | O upside depende de um multiplicador no CDS que hoje é tempero, no limite do intervalo |
| Sinal do S&P 500 na (F): +1,89 por desvio (alta da bolsa americana deprecia o real), contra o mecanismo do mapa (2.3, apetite a risco) | O sinal é condicional ao dólar contra emergentes na mesma equação | Reestimar sem o dólar contra emergentes e medir a correlação entre os dois regressores; se o sinal virar, documentar que o S&P entra como resíduo do índice | Pequeno neste ciclo (S&P parado), mas um caminho de queda do S&P apreciaria o real no modelo |

[^ptax]: A PTAX é a taxa de câmbio de referência calculada pelo Banco Central a partir das cotações do dia. O report projeta a PTAX de venda do último dia útil de cada trimestre (4T26 = 31/12/2026).
[^processo]: Nesta rodada o report não usa notícia nenhuma, e o F não traz dado eleitoral. A data do 2º turno (25/10) coincide com o fim de semana anterior ao salto, mas o resultado e o que o mercado leu nele foram pedidos ao agente web e não sustentam nenhuma afirmação deste texto.
[^vol]: Volatilidade implícita é o quanto o mercado de opções cobra para proteger contra a oscilação do câmbio nos próximos três meses, em % ao ano; a realizada é a oscilação que já aconteceu. A implícita é uma variável do modelo, e o F deste ciclo não a traz.
[^split]: Global ou idiossincrático: se o real cai junto com os pares e com os índices de dólar, o motivo é global; se cai sozinho, é do Brasil. A comparação é feita no mesmo período para todos.
[^pctl]: Percentil é a posição do número no histórico: 0 é o menor já visto, 100 o maior. No volume, percentil 19 quer dizer que em 81% dos meses dos últimos 10 anos o volume foi maior.
[^posbancos]: Posição à vista dos bancos: quanto os bancos compraram menos venderam de dólar à vista, acumulado. Vendida (negativa) e crescendo quer dizer que eles estão financiando saída de dólar com o próprio balanço, sinal de escassez de dólar no mercado à vista.
[^cot]: O COT é o relatório semanal da CFTC com as posições em contratos futuros de real em Chicago. Posição extrema como sinal contrário: quando os fundos já estão muito comprados em real, sobra pouco comprador novo, e um choque faz muitos venderem ao mesmo tempo.
[^carry]: Carry é o ganho de aplicar no juro brasileiro, mais alto, financiado em dólar, ao juro americano. Ele atrai capital e sustenta o real enquanto o câmbio não oscila demais: por isso o modelo usa o carry dividido pela volatilidade. Exemplo: o mesmo diferencial de juros, dividido por uma volatilidade maior, dá um quociente menor, e o modelo lê isso como menos atração para o real.
[^reer]: O câmbio real efetivo (BIS) compara o real com uma cesta de moedas de parceiros, corrigido pelas inflações. Alta do índice é real mais caro.
[^modelo]: O Modelo Estrutural resolve juntas cinco equações (hiato, inflação, expectativas, Selic e câmbio). A faixa que ele imprime mede só a incerteza sobre os pesos estimados; a distribuição da tese é do agente.
[^sazonal]: Resíduo é a parte da variação trimestral do câmbio que o modelo não explica. Positivo no 4º trimestre quer dizer que, em dezembro, o real costuma se depreciar mais do que o modelo prevê; é a época de remessa de lucros e dividendos.
