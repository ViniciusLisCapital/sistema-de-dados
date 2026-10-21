# Report — câmbio · ciclo 2026-10-15 · rodada 1

Dados até: 15/10/2026 (PTAX até 14/10) · Horizontes: 4T26 a 1T28, USD/BRL pela PTAX de venda do último dia útil de cada trimestre

## 1. Tese

| Variável | Trimestre | Central | Base: faixa · P | Cauda worst: limite · P | Cauda best: limite · P | Pbc − Pwc |
|---|---|---|---|---|---|---|
| USD/BRL, PTAX de fechamento | 4T26 | 5,16 | 5,00 a 5,30 · 40% | acima de 5,30 · 30% | abaixo de 5,00 · 30% | 0,00 |
| | 1T27 | 5,19 | 4,95 a 5,40 · 40% | acima de 5,40 · 30% | abaixo de 4,95 · 30% | 0,00 |
| | 2T27 | 5,20 | 4,90 a 5,45 · 40% | acima de 5,45 · 30% | abaixo de 4,90 · 30% | 0,00 |
| | 3T27 | 5,18 | 4,90 a 5,50 · 35% | acima de 5,50 · 35% | abaixo de 4,90 · 30% | −0,05 |
| | 4T27 | 5,20 | 4,90 a 5,55 · 35% | acima de 5,55 · 35% | abaixo de 4,90 · 30% | −0,05 |
| | 1T28 | 5,22 | 4,90 a 5,60 · 35% | acima de 5,60 · 35% | abaixo de 4,90 · 30% | −0,05 |

- **Depreciação além do limite worst** (5,30 no 4T26, 5,60 no 1T28) se o 2º turno de 25/10 reverter a leitura que os preços fizeram em 05/10 e o choque do petróleo levar o Fed a mais duas altas: CDS de 150 a 180 p.b., dólar contra emergentes em 132 a 134 e vol. implícita em 16% dão 5,42 no 4T26 e 5,64 no 1T28 no modelo; o efeito do CDS × 1,5 leva a 5,46 e 5,76, e o desmonte da posição comprada dos fundos (+2%), em parte contido pelo BC (−1%), põe o 4T26 em 5,51.
- **Apreciação além do limite best** (5,00 no 4T26, 4,90 no 1T28) se o 2º turno confirmar a leitura de 05/10 e o plano fiscal de 2027 for lido como crível: CDS de 100 a 85 p.b., dólar contra emergentes em 127 a 128 e o Fed devolvendo a alta de setembro dão 5,01 no 4T26 e 5,00 no 1T28 no modelo; o efeito do CDS × 1,5 leva a 4,94 e 4,90.
- **A tese em uma frase:** o real fica perto de R$ 5,20 até o 1T28 no cenário base, porque a queda do prêmio de risco depois do 1º turno já está no preço e o carry, que ainda é o maior entre os pares, encolhe com os cortes da Selic e a alta do Fed; a distribuição é simétrica até o 2T27, com a mediana abaixo da central pelo prêmio que o modelo não captura e o risco de desmonte da posição comprada pesando do outro lado, e pende para a depreciação a partir do 3T27, porque o CDS de 112 p.b. deixa pouca folga diante de uma dívida que subiu 5,5 p.p. do PIB em 12 meses.

## 2. Argumentação

### Q1. Condições do mercado de câmbio

O mercado funciona com liquidez normal, mas com posicionamento especulativo no extremo comprado em real e um BC que vendeu dólares em agosto e setembro.

- **Liquidez normal.** O volume interbancário D+1 teve média de US$ 356 mi/dia no último mês, no percentil 68 dos 10 anos[^pctl] (`cmb_ptax` · 14/10), e o D+2 de US$ 1.233 mi/dia, no percentil 44 (`cmb_ptax` · 14/10), o que mostra um mercado sem secura de negócios.
- **Posicionamento no extremo.** Os fundos alavancados estão comprados em real em 27.396 contratos líquidos, no percentil 99 dos 10 anos e perto do máximo de 32.847 da década (`cmb_cot_fx` · 06/10); a posição subiu 17.843 contratos só na semana de 29/09 a 06/10, com 22.075 contratos de compras novas (`cmb_cot_fx` · 29/09 e 06/10). Os asset managers estão comprados em 56.610 contratos, percentil 89 (`cmb_cot_fx` · 06/10), e os dealers vendidos em 63.683, percentil 4. Posição tão concentrada de um lado é o sinal contrário de Verde §5.3[^posic]: sobra pouco comprador novo, e uma notícia ruim encontra muita gente para sair. O dado tem nove dias e não vê a semana de 07/10 a 14/10, em que a PTAX devolveu 1,17% (`cmb_ptax` · 05/10 e 14/10).
- **Fluxo: saída em setembro, entrada depois do 1º turno.** O fluxo financeiro contratado saiu US$ 7,37 bi em setembro (`cmb_cambio_contratado` · set) e entrou US$ 4,09 bi de 01/10 a 09/10 (`cmb_cambio_contratado` · 09/10), US$ 4,13 bi deles entre 05/10 e 09/10 (`cmb_cambio_contratado` · 09/10). A entrada coincide com o rali do real, o que mostra que ele teve dólar entrando no mercado à vista, e não só compra de real no mercado futuro. Em 12 meses o financeiro saiu US$ 62,3 bi, percentil 18 da história (`cmb_cambio_contratado` · set), mas o saldo total ficou quase zerado em −US$ 3,9 bi, contra −US$ 42,7 bi um ano antes (`cmb_cambio_contratado` · set), porque o comercial trouxe US$ 58,4 bi (percentil 93).
- **O BC esteve no mercado.** Vendeu US$ 1 bi à vista em cada um de 31/08, 14/09 e 17/09 e US$ 1 bi em linha em 22/09 e em 28/09 (`cmb_reservas_bc` · set), num mês de fluxo financeiro negativo e de PTAX subindo de 5,15 para 5,22 entre 17/09 e 29/09 (`cmb_ptax`). Não houve intervenção em outubro até 14/10 (`cmb_reservas_bc` · 14/10). As reservas caíram US$ 6,5 bi no último mês, para US$ 362,6 bi (`cmb_reservas_bc` · 14/10), percentil 54 dos 10 anos: o colchão não mudou de patamar.
- **A escassez de dólar onshore não dá para medir.** A posição à vista dos bancos estava vendida em US$ 22,1 bi em agosto, US$ 2,7 bi mais vendida que em julho (`cmb_reservas_bc` · ago), e o mês seguinte teve saída financeira de US$ 7,37 bi; isso sugere que a posição se aprofundou em setembro, mas o dado de setembro não saiu e o cupom cambial não está no F[^processo1].

### Q2. Fundamentos

**Carry: alto, o maior entre os pares, e encolhendo.**

| Medida | Valor | Fonte · data |
|---|---|---|
| Selic − Fed Funds (nominal) | 10,00 p.p. | `diferenciais_juros` · set |
| Carry contra a meta do Fed | 10,12 p.p. | O real e os pares · 14/10 |
| Diferencial real ex-post | 9,14 p.p., percentil 81 dos 10 anos | `diferenciais_juros` · set |
| DI 2 anos − Treasury 2 anos (ex-ante) | 7,68 p.p., contra 9,16 em 14/09 | `br_di_grade` e `us_interest_rate` · 13/10 |
| Carry / vol. 63d[^carryvol] | 0,83 (MXN 0,38 · COP 0,56 · PEN 0,14 · CLP 0,09) | O real e os pares · 14/10 |

O real paga o maior carry ajustado ao risco da região, o que sustenta a demanda por ele, mas o carry à frente caiu 1,48 p.p. em um mês (`br_di_grade`, `us_interest_rate` · 14/09 a 13/10), pelas duas pernas: o Fed subiu a meta em 25 p.b. em 17/09 (`us_interest_rate`) e o DI de 2 anos caiu 134 p.b. em um mês (`br_di_grade` · 14/10). O real se apreciou no mesmo mês em que o carry encolheu, então o que o moveu não foi o carry (ver Q3 e E6). O nível também ainda é alto pelo histórico: o diferencial nominal está no percentil 72 dos 10 anos (`diferenciais_juros` · set).

**Prêmio de risco: baixo no preço, alto nos números fiscais.** O CDS de 5 anos está em 112 p.b., 40 p.b. abaixo de um ano antes (`cmb_risco_pais` · 14/10). Os números fiscais andaram na direção contrária: a dívida bruta subiu 5,5 p.p. em 12 meses, para 82,9% do PIB (`fisc_divida` · ago), o déficit nominal está em 9,48% do PIB e o primário em déficit de 0,62% do PIB em 12 meses (`fisc_nfsp` · ago). O prêmio baixo, portanto, não vem do fiscal corrente: vem da expectativa de mudança que os preços embutiram em 05/10 (Q3). Na leitura de Verde §1.11[^verde], prêmio apertado sobre fundamento que piora deixa pouca folga para uma reprecificação súbita; é o que inclina as caudas para a depreciação a partir do 3T27. Os dados fiscais têm 75 dias e não pesam sobre o mês, só sobre o horizonte.

**Termos de troca e commodities: a favor do real, e mais do que o modelo vê.** O Brent está em US$ 125,44, alta de 80,3% em 3 meses (`comm_brent` · 06/10), e o Brasil exporta petróleo em termos líquidos: US$ 51,6 bi de exportação em 12 meses, percentil 100, contra US$ 6,6 bi de importação (`cmb_comex_produto` · ago). O IC-Br em dólar subiu 12,8% em 12 meses (`comm_icbr_usd` · set). É o canal de Verde §2.4[^oleo]: num universo emergente de importadores de energia, o petróleo caro favorece o real, o que ajuda a explicar por que ele se descolou dos pares no último mês (Q3). Mas o IC-Br de outubro ainda não saiu, e o Brent subiu 8,2% entre 30/09 e 06/10 (`comm_brent`), então o modelo, que lê o IC-Br, está com o petróleo de setembro.

**Contas externas: sem fragilidade.** O déficit em transações correntes é de US$ 63,0 bi em 12 meses, 2,47% do PIB, menor que os US$ 76,9 bi de um ano antes (`cmb_balanco_pagmt` · ago), e o investimento direto no país, de US$ 86,6 bi (3,39% do PIB, percentil 91), cobre o déficit com folga (`cmb_balanco_pagmt` · ago). A saída de 12 meses do fluxo financeiro vem de rendas (−US$ 67,0 bi, percentil 5) e de capitais brasileiros (−US$ 47,7 bi, percentil 3), enquanto os capitais estrangeiros entraram US$ 87,3 bi, percentil 72 (`cmb_cambio_contratado` · ago): quem sai é residente, não estrangeiro.

**Valor: neutro.** O câmbio real efetivo está em 116,46, no percentil 50 dos 10 anos (`cmb_reer` · ago), e caiu 3,4% em 3 meses: o real não está caro nem barato contra a própria década, então a valuation não puxa para lado nenhum no horizonte da tese.

### Q3. O que explica a dinâmica recente

A referência é de 3 meses, com foco no último mês, que tem dois episódios de sinal oposto.

- **De 17/09 a 02/10, depreciação junto com os pares e com o prêmio.** A PTAX foi de 5,15 a 5,22 entre 17/09 e 29/09 (+1,33%, `cmb_ptax`), com o CDS de 111 para 131 p.b. (`cmb_risco_pais` · 17/09 e 29/09), o peso mexicano de 17,19 para 17,90 (`cmb_fx_latam`) e o DXY de 100,2 para 101,4 (`cmb_dollar_index`). O Fed subiu os juros em 17/09 e o Brent tocou US$ 135,51 em 02/10 (`comm_brent`). Foi um movimento global com um componente doméstico pré-eleitoral no CDS.
- **Em 05/10, o salto idiossincrático.** Na primeira sessão depois do 1º turno de 04/10, a PTAX caiu 4,55%, de 5,22 para 4,99 (`cmb_ptax` · 02/10 e 05/10), o DI de 5 anos caiu 135 p.b. e o de 1 ano 70 p.b. (`br_di_grade` · 02/10 e 05/10), e o CDS caiu 22 p.b. entre 02/10 e 06/10 (`cmb_risco_pais`). Os pares se mexeram pouco no mesmo pregão: o peso mexicano e o colombiano se apreciaram 1,0%, o sol 0,3%, e o peso chileno ficou estável (`cmb_fx_latam` · 02/10 e 05/10). O F não traz dado eleitoral[^processo2]; o que os preços dizem é que o resultado reduziu o prêmio de risco brasileiro de uma vez.
- **De 06/10 a 14/10, devolução parcial.** A PTAX fez o mínimo de 4,9698 em 06/10 e voltou a 5,0441 em 14/10 (`cmb_ptax`), +1,0% desde o ciclo anterior (`cmb_ptax` · 07/10), com o CDS de volta a 112 p.b. (`cmb_risco_pais` · 14/10).

**Global contra idiossincrático.** O movimento do último mês é idiossincrático, e em favor do real:

| Janela | BRL | Média MXN, CLP, COP, PEN | Dólar contra emergentes | DXY |
|---|---|---|---|---|
| 1 mês | −2,4% | +4,6% | +2,9% | +2,4% |
| 3 meses | −0,6% | +2,1% | +0,2% | +1,6% |
| desde 30/09 | −2,6% | −0,3% | +0,3% | +0,6% |

Fontes: "O real e os pares" e `cmb_fx_latam` (13/10), `cmb_dollar_index_em` (09/10), `cmb_dollar_index` (15/10); Δ% positivo = moeda mais fraca. Em um mês o real se apreciou 7,0 p.p. a mais que a média dos pares, com o dólar se fortalecendo contra emergentes, o que mostra que o Brasil não foi "passageiro" do ciclo global desta vez (Verde §5.5[^passageiro]). Parte da diferença é dos pares, não do real: os asset managers reduziram a posição líquida no peso mexicano em 88.676 contratos em um mês e estão vendidos, no percentil 0 da década (`cmb_cot_fx` · 06/10), e o peso caiu 8,0% (O real e os pares · 13/10).

**O que o modelo explica.** Com as exógenas no valor do corte, o Modelo Estrutural põe a PTAX do 4T26 em 5,16, contra 5,21 com as exógenas em 30/09: −1,0%, quase todo pelo CDS (−1,6%), com o dólar contra emergentes (+0,3%), o S&P 500 (+0,2%) e a alta do Fed (+0,1%) puxando para o outro lado (Modelo Estrutural · ciclo 2026-10-15). O real de 14/10 está 2,2% abaixo dessa central (`cmb_ptax` · 14/10). O modelo lê o choque eleitoral só pelo CDS, a 0,085% de PTAX por p.b.; o mercado pagou 0,139% por p.b. entre 30/09 e 14/10 e 0,221% entre 02/10 e 06/10 (`cmb_ptax`, `cmb_risco_pais`). O resto do movimento de outubro está em canais fora do modelo: o prêmio que aparece no DI longo e não no CDS em dólar, a entrada de fluxo e a compra dos fundos alavancados.

### Q4. Cenário prospectivo

**Por que a central.** O cenário base mantém as exógenas no valor do corte (seção 3.1): o 2º turno confirma o que os preços embutiram em 05/10, o petróleo e o Fed não vão além do que já fizeram. Com isso o modelo dá 5,16 no 4T26 e 5,22 no 1T28. A subida de 1,3% ao longo do horizonte vem de dois canais (Modelo Estrutural · ciclo 2026-10-15): o carry/vol, porque a Selic do modelo cai de 13,60% para 12,25% enquanto o Fed fica em 3,88%, e responde por 1,4% do nível do 1T28; e a diferença de inflação, porque o IPCA do modelo roda acima de 0,91% por trimestre nos EUA (com a inflação americana a 1,20% por trimestre a subida some). A central fica perto da mediana do Focus, de 5,15 para o fim de 2026 e 5,26 para o fim de 2027 (`expc_focus_periodo` câmbio · 09/10). A Selic do modelo é endógena e fica a cargo da política monetária (S1).

**Por que a distribuição.** A referência é uma distribuição com o desvio da vol. realizada de 63 dias do real, 12,2% ao ano (O real e os pares · 14/10), e mediana na base com o tempero (i), que dá ~39% para a faixa base e 31% a 35% para a cauda best até o 2T27 (seção 3.3). Dois temperos agem sobre essa referência em sentidos opostos:
- **Para a apreciação:** o efeito do CDS × 1,5 (seção 3.2), porque o mercado está pagando mais por p.b. de CDS do que o modelo estima; ele põe a mediana do 4T26 em 5,12, abaixo da central de 5,16, e é a razão da cauda best ter 30% e não menos.
- **Para a depreciação:** o posicionamento. Com os fundos no percentil 99, o caminho de volta é mais curto que o de ida, e o BIS (2026)[^bis] mostra que a resposta do câmbio a um choque depende do tamanho da posição a desmontar. Ele tira 5 p.p. da cauda best e põe na worst no 4T26 e no 1T27, o que zera a assimetria.
- **A partir do 3T27, o fiscal.** O CDS em 112 p.b. com a dívida bruta subindo 5,5 p.p. do PIB em 12 meses (Q2) é a razão de a worst ganhar 5 p.p. sobre a best no fim do horizonte; o choque do petróleo, bom para o real, e o Fed subindo, ruim, se compensam no argumento e não mudam a assimetria.

**O que mudaria a tese.** Se o CDS passar de 131 p.b., o nível de 30/09, por duas semanas, a cauda worst do 4T26 e do 1T27 fica mais provável que a best. Se os fundos alavancados cortarem mais de 15 mil contratos da posição comprada numa semana com a PTAX acima de 5,15, o desmonte começou. Se o CDS cair abaixo de 100 p.b. com a PTAX abaixo de 5,00, a cauda best deixa de ser cauda.

### Outros pontos

- **O choque do petróleo é favorável ao real, e o mercado já o separou dos pares.** O Brent subiu 22,7% em um mês (`comm_brent` · 06/10) e as moedas dos pares se depreciaram no mesmo mês (peso chileno +4,4%, sol +2,8%, O real e os pares · 13/10 e 09/10). Se o Brent recuar, o real perde esse diferencial, mas o canal não está no cenário base porque o IC-Br de outubro não saiu.
- **O Fed voltou a subir.** A meta foi de 3,63% para 3,88% em 17/09 (`us_interest_rate`), o Treasury de 10 anos subiu 59 p.b. em 3 meses, para 5,21% (`us_interest_rate` · 13/10), e o CPI está em 3,72% em 12 meses (`diferenciais_juros` · set). É a perna externa do worst: a alta no funding de um carry trade lotado é o choque que o BIS (2026) associa a desmontes.

**Olhado, sem sinal.**
- Estoque de swaps do BC · −US$ 91,6 bi (`cmb_reservas_bc` · ago) · US$ 1,3 bi menor em um mês, rolagem sem oferta nova, e o dado tem 75 dias · diria algo se o BC ampliasse a oferta acima dos vencimentos.
- Sazonalidade de dezembro · o fluxo financeiro de dezembro saiu em média US$ 15,2 bi de 2016 a 2025, contra US$ 3,5 bi nos outros meses, mas a PTAX subiu em dezembro em só 4 dos 10 anos, com variação média de −0,8% (`cmb_cambio_contratado`, `cmb_ptax`) · a saída costuma ser coberta e não move o preço de fechamento do 4T26 · diria algo se o BC não estivesse vendendo linhas em dezembro.
- Termos de troca Funcex · 111,35, percentil 75 dos 10 anos (`cmb_termos_troca` · jul) · o dado tem 106 dias e é anterior à alta do Brent · diria algo com o dado de setembro.
- Erros e omissões · −US$ 2,6 bi em 12 meses (`cmb_balanco_pagmt` · ago) · perto dos −US$ 2,2 bi de um ano antes, sem fluxo escondido · diria algo se passasse a crescer mês a mês.
- Juro real ex-post dos pares · BR 9,78%, MX 3,24%, CO 5,76% (`cmb_real_rates` · ago) · o dado tem 75 dias e o carry/vol de 14/10 já diz o mesmo · diria algo se um par subisse juros.
- Comércio com China e EUA · exportação para a China de US$ 109,0 bi em 12 meses, para os EUA de US$ 35,8 bi, menos que os US$ 40,4 bi de um ano antes (`cmb_comex_pais` · set) · mudança de composição, sem efeito no saldo · diria algo se a exportação para a China caísse.

## 3. Premissas

### 3.1 Etapa 1 — o modelo

**Cenários.**
- **Base:** o 2º turno de 25/10 confirma a leitura que os preços fizeram em 05/10; o Fed fica em 3,75% a 4,00% e o petróleo para onde está; nada muda o prêmio de risco além do que já mudou.
- **Worst:** o 2º turno reverte a leitura de 05/10, ou o plano fiscal de 2027 decepciona, e o prêmio volta acima do nível de 30/09 e continua subindo com a dívida; ao mesmo tempo, o choque do petróleo leva o Fed a mais duas altas e fortalece o dólar contra emergentes.
- **Best:** o 2º turno confirma a leitura de 05/10 e o plano fiscal de 2027 é lido como crível, e o CDS cai abaixo de 100 p.b.; o petróleo sai do pico e o Fed devolve a alta de setembro em 2027.

**Caminhos das exógenas** (nível no fechamento do trimestre, na unidade do simulador).

| Exógena | Hoje (valor · tabela · data) | Cenário | 4T26 | 1T27 | 2T27 | 3T27 | 4T27 | 1T28 |
|---|---|---|---|---|---|---|---|---|
| CDS 5 anos (p.b.) | 112 · `cmb_risco_pais` · 14/10 | base | 112 | 112 | 112 | 112 | 112 | 112 |
| | | worst | 150 | 160 | 165 | 170 | 175 | 180 |
| | | best | 100 | 95 | 90 | 85 | 85 | 85 |
| Vol. implícita do real (% a.a.) | sem dado no F; o simulador segura 12,19 do 2T26 | base | 12,19 | 12,19 | 12,19 | 12,19 | 12,19 | 12,19 |
| | | worst | 16 | 15 | 14 | 14 | 14 | 14 |
| | | best | 11 | 11 | 11 | 11 | 11 | 11 |
| Dólar contra emergentes (índice) | 129,77 · `cmb_dollar_index_em` · 09/10 | base | 129,77 | 129,77 | 129,77 | 129,77 | 129,77 | 129,77 |
| | | worst | 132 | 133 | 134 | 134 | 134 | 134 |
| | | best | 128 | 127 | 127 | 127 | 127 | 127 |
| S&P 500 (pontos) | 7.721 · `cmb_equity_us` · 15/10 | base | 7.721 | 7.721 | 7.721 | 7.721 | 7.721 | 7.721 |
| | | worst | 7.300 | 7.300 | 7.300 | 7.300 | 7.300 | 7.300 |
| | | best | 7.721 | 7.721 | 7.721 | 7.721 | 7.721 | 7.721 |
| IC-Br em dólar (índice) | 205,70 · `comm_icbr_usd` · set | base | 205,70 | 205,70 | 205,70 | 205,70 | 205,70 | 205,70 |
| | | worst | 205,70 | 205,70 | 205,70 | 205,70 | 205,70 | 205,70 |
| | | best | 205,70 | 205,70 | 205,70 | 205,70 | 205,70 | 205,70 |
| Fed Funds (% a.a.) | 3,88 · `us_interest_rate` · 15/10 | base | 3,88 | 3,88 | 3,88 | 3,88 | 3,88 | 3,88 |
| | | worst | 4,13 | 4,38 | 4,38 | 4,38 | 4,38 | 4,38 |
| | | best | 3,88 | 3,88 | 3,63 | 3,63 | 3,63 | 3,63 |
| CPI dos EUA (% no trimestre) | 3,72% em 12 meses · `diferenciais_juros` · set | base | 0,91 | 0,91 | 0,91 | 0,91 | 0,91 | 0,91 |
| | | worst | 1,20 | 1,20 | 1,00 | 0,91 | 0,91 | 0,91 |
| | | best | 0,91 | 0,80 | 0,80 | 0,80 | 0,80 | 0,80 |

Motivos dos caminhos que não saem da história:
- **CDS worst:** 150 é o nível do 2T25 na série do simulador, acima dos 131 de 30/09; a subida até 180 é a dívida crescendo sem plano.
- **Vol. implícita:** o F não traz a série; a base usa o padrão do simulador, e a vol. realizada de 63 dias, de 12,2% (O real e os pares · 14/10), está no mesmo nível. A de 21 dias está em 18,0% pelo salto de 05/10.
- **S&P 500 no worst:** a queda para 7.300 pontos acompanha as altas do Fed. No modelo o peso do S&P é positivo (bolsa americana subindo deprecia o real, com o dólar contra emergentes e o CDS dados), então a queda puxa a PTAX do worst para baixo; deixei o caminho pela história e não pelo efeito.
- **IC-Br parado nos três cenários:** o índice de outubro não saiu, e o canal do petróleo fica no argumento (Q2) e não no caminho.
- **CPI dos EUA na base:** 0,91% por trimestre é a média dos últimos 4 trimestres do simulador, o ritmo coerente com os 3,72% de 12 meses.

**Saída do modelo** (sem tempero; a linha base da PTAX é a central da seção 1).

| Variável | Cenário | 4T26 | 1T27 | 2T27 | 3T27 | 4T27 | 1T28 |
|---|---|---|---|---|---|---|---|
| PTAX (R$/US$) | base | 5,16 | 5,19 | 5,20 | 5,18 | 5,20 | 5,22 |
| | worst | 5,42 | 5,50 | 5,54 | 5,55 | 5,59 | 5,64 |
| | best | 5,01 | 5,00 | 4,98 | 4,95 | 4,97 | 5,00 |
| Selic, média do trimestre (% a.a.) | base | 13,60 | 13,26 | 12,96 | 12,69 | 12,46 | 12,25 |
| | worst | 13,60 | 13,26 | 12,98 | 12,73 | 12,52 | 12,34 |
| | best | 13,60 | 13,25 | 12,94 | 12,67 | 12,42 | 12,20 |
| IPCA 12 meses, fim do trimestre (%) | base | 5,27 | 4,83 | 4,30 | 4,30 | 4,19 | 4,05 |
| | worst | 5,30 | 4,93 | 4,46 | 4,51 | 4,41 | 4,24 |
| | best | 5,25 | 4,77 | 4,20 | 4,16 | 4,05 | 3,93 |

A faixa de 90% que o simulador imprime para a PTAX base vai de 5,11–5,20 no 4T26 a 5,00–5,47 no 1T28; é a incerteza dos pesos, não do câmbio[^faixa].

### 3.2 Etapa 2 — o tempero qualitativo

**(i) CDS 5 anos — efeito mais forte que o estimado** · cenários base, worst e best
- Coeficiente: estimado 25,111 por desvio-padrão da variação do CDS (298,5 p.b.), intervalo de 90% do posterior de 19,481 a 30,608. Multiplicador: × 1,5, fora do intervalo.
- Efeito: base, 4T26 de 5,16 para 5,12 e 1T28 de 5,22 para 5,18; worst, 4T26 de 5,42 para 5,46 e 1T28 de 5,64 para 5,76; best, 4T26 de 5,01 para 4,94 e 1T28 de 5,00 para 4,90.
- Por quê: neste episódio o real andou mais por p.b. de CDS do que o modelo estima, 0,139% entre 30/09 e 14/10 e 0,221% entre 02/10 e 06/10, contra 0,085% no modelo (Q3); para o modelo reproduzir a PTAX de 14/10 no 4T26 o multiplicador teria de ser ~2,5. O desvio-padrão de 298,5 p.b. vem de uma amostra em que o CDS andou centenas de pontos nas crises, e o peso estimado é uma média que mistura esses episódios com os de prêmio baixo; com o CDS perto de 110 p.b., o prêmio político aparece mais no DI longo (−135 p.b. em 05/10) do que no CDS em dólar (−22 p.b. de 02/10 a 06/10), e a única porta que o modelo tem para ele é o CDS. Fiquei em × 1,5, e não em 2,5, porque parte do movimento de outubro é posicionamento e fluxo, que entram pelo tipo (ii).
- Onde entra: nas caudas, os pontos do worst e do best; na base, na assimetria, puxando a mediana do 4T26 para 5,12.

**(ii) Posicionamento — fundos alavancados comprados em real** · cenário worst, e assimetria da base
- Hoje: 27.396 contratos líquidos comprados, percentil 99 dos 10 anos, +17.843 na semana de 29/09 a 06/10; asset managers comprados em 56.610, percentil 89 (`cmb_cot_fx` · 06/10).
- Por que o modelo não vê: nenhuma exógena mede posição; o modelo só vê o preço que ela produz.
- Efeito: no worst, desmonte de +2% sobre o modelo no 4T26 e +1% no 1T27, zero depois; a posição se normaliza em um ou dois trimestres. Na base, tira 5 p.p. da cauda best e põe na worst no 4T26 e no 1T27.
- Por quê: posição extrema é sinal contrário (Verde §5.3), e a resposta do câmbio a um choque cresce com a posição a desmontar (BIS, 2026); a alta do Fed de 17/09 é exatamente uma alta no funding desse carry.
- Onde entra: ponto do worst no 4T26 e no 1T27; probabilidades do 4T26 e do 1T27.

**(ii) O BC no mercado de câmbio — vendas à vista e de linha** · cenário worst
- Hoje: US$ 3 bi vendidos à vista e US$ 2 bi em linha de 31/08 a 28/09, nada em outubro até 14/10; reservas de US$ 362,6 bi (`cmb_reservas_bc` · 14/10).
- Por que o modelo não vê: não há variável de intervenção no modelo.
- Efeito: −1% sobre o modelo no worst do 4T26, um trimestre; o BC vendeu em setembro com a PTAX em 5,15–5,22 e venderia num desmonte desordenado e no fluxo de dezembro.
- Por quê pequeno: a evidência para o Brasil não acha efeito mensurável de intervenção esterilizada sobre o nível do real (Chamon e Garcia, 2016[^chamon]), e Verde §7.2 trata a venda como algo que compra tempo, não que muda a direção. Entra como freio na velocidade, não como teto.
- Onde entra: ponto do worst no 4T26.

### 3.3 Da etapa 1 à tese

| Trimestre | Central (modelo, base) | Worst: modelo → com tempero | Best: modelo → com tempero |
|---|---|---|---|
| 4T26 | 5,16 | 5,42 → 5,51 | 5,01 → 4,94 |
| 1T27 | 5,19 | 5,50 → 5,63 | 5,00 → 4,92 |
| 2T27 | 5,20 | 5,54 → 5,62 | 4,98 → 4,89 |
| 3T27 | 5,18 | 5,55 → 5,64 | 4,95 → 4,85 |
| 4T27 | 5,20 | 5,59 → 5,69 | 4,97 → 4,87 |
| 1T28 | 5,22 | 5,64 → 5,76 | 5,00 → 4,90 |

Os limites da faixa base são números redondos entre a central e os pontos das caudas com tempero: o worst com tempero fica acima do limite superior em todos os trimestres, e o best com tempero cai abaixo do limite inferior até o 4T27 e encosta nele no 1T28. As probabilidades partem da referência lognormal (mediana na base com o tempero (i), desvio da vol. realizada de 63 dias): best 35%, base 39%, worst 27% no 4T26, e best 35%, base 34%, worst 30% no 1T28. O posicionamento move 5 p.p. da best para a worst no 4T26 e no 1T27; o fiscal move 5 p.p. da best para a worst do 3T27 ao 1T28; o resto é arredondamento para múltiplos de 5.

## 4. Para os outros agentes

**Respostas às entradas fixas (E1–E7).**
- **E1, em destaque:** a apreciação de outubro (−2,6% desde 30/09, `cmb_ptax`) é uma mudança de nível, persistente no cenário base, porque veio de uma queda de prêmio que o CDS e o DI confirmaram no mesmo dia; uma parte é técnica (a compra dos fundos alavancados na semana da eleição) e pode voltar, e o 2º turno de 25/10 decide qual das duas leituras vale.
- **E2, em destaque:** o componente idiossincrático domina; desde 30/09 o real se apreciou 2,6% e a média dos pares se apreciou 0,3%, com o dólar contra emergentes +0,3% (`cmb_fx_latam`, `cmb_dollar_index_em`); e é idiossincrático na direção de prêmio menor, não maior.
- **E3:** no modelo o câmbio chega à alimentação no mesmo trimestre (peso 0,085 do câmbio médio, intervalo 0,020 a 0,153) e aos bens industriais no trimestre seguinte (0,040, intervalo 0,016 a 0,064); no worst com tempero, a PTAX de 5,76 no 1T28 leva o IPCA de 12 meses a 4,30%, contra 4,05% na base com 5,22.
- **E4:** a PTAX de 5,04 em 14/10 está 1,2% abaixo da média de 5,10 dos cinco dias úteis até 11/09 (`cmb_ptax`), a aproximação que usei do câmbio do cenário de referência da reunião 281[^processo3]; o desvio é na direção de apreciação, que não é o risco listado pelo Copom.
- **E5, em destaque:** CDS e real andaram juntos contra os pares, mas no sentido do alívio: o CDS caiu 19 p.b. desde 30/09, para 112 (`cmb_risco_pais` · 14/10), com o real 2,4 p.p. melhor que a média dos pares. O real não precifica estresse fiscal hoje, apesar da dívida bruta em 82,9% do PIB e subindo (`fisc_divida` · ago).
- **E6, em destaque:** carry e real se descolaram. O diferencial DI 2 anos − Treasury 2 anos caiu 1,48 p.p. de 14/09 a 13/10 (`br_di_grade`, `us_interest_rate`) e o real se apreciou; o carry continua o maior entre os pares (carry/vol 0,83, O real e os pares · 14/10), mas o rali de outubro foi de prêmio, não de carry.
- **E7, em destaque:** o BC vendeu US$ 3 bi à vista e US$ 2 bi em linha entre 31/08 e 28/09, nada em outubro até 14/10 (`cmb_reservas_bc`); a liquidez interbancária está normal (percentil 68 do D+1) e o cupom cambial não está no F.

**Pedidos à política monetária.**
- **S1:** qual a trajetória da Selic até o 1T28 e o balanço de riscos? A curva precifica 12,13% na reunião de 08/12/2027, 194 p.b. abaixo de um mês antes (`br_di_grade` · 14/10), o Focus 12,00% no fim de 2027 (`expc_focus_periodo` Selic · 09/10), e o modelo, que a resolve, 12,46% de média no 4T27. Depende disso a subida da central de 5,16 para 5,22 (canal carry/vol, Q4) e a resposta E6.
- **S2:** o aprofundamento dos cortes que a curva passou a precificar depois de 05/10 é lido como credibilidade, porque a inflação esperada cai, ou como risco, porque o IPCA esperado para 2026 subiu 0,32 p.p. em 4 semanas, para 5,22% (`expc_focus_periodo` IPCA · 09/10)? Depende disso o sinal do efeito juro → câmbio nas duas caudas.
- **S3:** como o Copom descreveu o câmbio no comunicado e na ata da reunião 281 e no RPM de setembro, e a apreciação de outubro muda a projeção de 3,2% do 1T28 (`pm_copom_projecoes` · 24/09)? Depende disso a resposta E4.
- **S4:** se a PTAX for a 5,50 ou mais no 4T26 (cauda worst), o Copom interrompe os cortes, e o BC volta a vender à vista ou em linha? Depende disso o limite da cauda worst e o tamanho do tempero do BC.
- **Pedido deste ciclo:** a política monetária lê a alta do Fed de 17/09 e o Treasury de 10 anos em 5,21% como início de um ciclo de alta? A perna externa do worst (Fed a 4,38%) depende disso; enquanto não houver agente externo, é premissa assumida.

## 5. Placar

Primeiro ciclo.

[^pctl]: Percentil: a posição do valor de hoje no histórico, de 0 (o menor já visto) a 100 (o maior). No volume interbancário, percentil 68 quer dizer que o volume médio do último mês foi maior que o de 68% dos meses dos últimos 10 anos.
[^posic]: Posicionamento como sinal contrário: quando os especuladores já estão muito comprados numa moeda, sobra pouco comprador novo, e uma notícia ruim faz muitos venderem ao mesmo tempo. O dado é o relatório semanal da CFTC sobre os contratos de real negociados em Chicago, que cobre só uma parte do mercado.
[^carryvol]: Carry/vol: o diferencial de juros dividido pela volatilidade da moeda. Mede quanto juro a moeda paga por unidade de risco: 0,83 quer dizer que o real paga em um ano de juro extra 0,83 vez a oscilação típica de um ano.
[^verde]: Os modelos mentais da Verde Asset são maneiras de raciocinar tiradas das cartas da gestora de 2020 a 2026, não opiniões sobre hoje. §1.11: deterioração institucional e fiscal que não aparece no preço de imediato é perigosa justamente quando os prêmios de risco já estão baixos.
[^oleo]: Verde §2.4: entre os emergentes, a maioria importa energia; o Brasil exporta petróleo, então um petróleo mais caro melhora a balança comercial e as receitas do governo daqui e piora a dos vizinhos.
[^passageiro]: "Brasil como passageiro" (Verde §5.5): em muitos períodos o real só acompanha o humor global, como um passageiro, e a notícia local pesa pouco. No último mês foi o contrário: o dólar se fortaleceu contra emergentes e o real se apreciou.
[^bis]: BIS (2026): o mesmo choque de juros move pouco uma moeda que ninguém usa em carry trade e move muito uma que está no centro de posições alavancadas, porque o choque força quem está posicionado a desmontar de uma vez. O estudo é sobre o franco suíço e o iene como moedas de funding; aplico a lógica ao real como moeda-alvo.
[^chamon]: Chamon e Garcia (2016) estudam os controles de capital do Brasil de 2009 a 2012 e não encontram efeito mensurável da intervenção esterilizada (compra ou venda de dólares pelo BC sem mudar os juros) sobre o nível do real; as vendas foram poucas no período, então essa metade do resultado é fraca.
[^faixa]: A faixa do simulador mostra quanto a PTAX mudaria se os pesos do modelo fossem outros dentro do que a estimação admite; não inclui o erro das equações nem choques novos, e por isso é bem mais estreita que a faixa base da seção 1.
[^processo1]: O F não traz o cupom cambial nem a posição dos bancos de setembro, as duas medidas de escassez de dólar no mercado doméstico.
[^processo2]: Não há dado eleitoral nesta análise. A leitura do 1º turno vem só dos preços: câmbio, DI e CDS no pregão de 05/10.
[^processo3]: O F não traz o câmbio que o Copom usou no cenário de referência. Usei como aproximação a média da PTAX nos cinco dias úteis até a sexta-feira anterior à reunião de 16/09.
