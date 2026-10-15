# Report — câmbio · ciclo 2026-10-15 · rodada 1 · teste parcial: só a projeção

Dados até: 15/10/2026 (PTAX até 14/10/2026) · Horizontes: os seis trimestres do Modelo Estrutural, do 4T26 ao 1T28, com a PTAX de venda do último dia útil de cada trimestre

Este arquivo traz só a tese (seção 1) e as premissas (seção 3) do report. Ficam de fora a argumentação (seção 2), a tabela de acompanhamento das exógenas, os alertas e checkpoints das fichas, a seção 4 e o placar.

## 1. Tese

| Variável | Trimestre | Central | Base: faixa · P | Cauda worst (depreciação): limite · P | Cauda best (apreciação): limite · P | Pbc − Pwc |
|---|---|---|---|---|---|---|
| USD/BRL, PTAX de venda no fechamento do trimestre | 4T26 | 5,13 | 5,00 a 5,25 · 48% | acima de 5,25 · 22% | abaixo de 5,00 · 30% | +0,08 |
| | 1T27 | 5,21 | 5,00 a 5,40 · 48% | acima de 5,40 · 26% | abaixo de 5,00 · 26% | 0,00 |
| | 2T27 | 5,25 | 5,00 a 5,50 · 47% | acima de 5,50 · 28% | abaixo de 5,00 · 25% | −0,03 |
| | 3T27 | 5,26 | 5,00 a 5,55 · 46% | acima de 5,55 · 30% | abaixo de 5,00 · 24% | −0,06 |
| | 4T27 | 5,31 | 5,00 a 5,65 · 45% | acima de 5,65 · 31% | abaixo de 5,00 · 24% | −0,07 |
| | 1T28 | 5,33 | 4,95 a 5,70 · 45% | acima de 5,70 · 31% | abaixo de 4,95 · 24% | −0,07 |

- **O que leva à cauda worst (depreciação).** No 4T26: o 2º turno de 25/10[^1] reverte a leitura que o mercado fez do 1º turno, o CDS vai a 150 p.b., a volatilidade implícita a 16%, o dólar contra emergentes a 133 e o Fed sobe para 4,125%; isso dá 5,54 no modelo, 5,56 com o efeito do CDS × 1,2, e 5,61 com a desmontagem da posição comprada em real (+2%) atenuada pela venda de dólar do BC (−1%). Em 2027: o plano fiscal não estabiliza a dívida, o CDS sobe a 170–180 p.b. com o Fed em 4,375% e as commodities recuando a 185; o modelo dá de 5,78 (2T27) a 5,88 (1T28), e o CDS × 1,2 leva a 5,82 e 5,93.
- **O que leva à cauda best (apreciação).** No 4T26: o 2º turno confirma, o CDS cai a 100 p.b., a volatilidade implícita a 11% e o dólar contra emergentes a 128; isso dá 4,97 no modelo e 4,94 com o efeito do CDS × 1,2. Em 2027: um plano fiscal que aponte para superávit primário leva o CDS a 90 p.b., com o Fed parado em 3,875%, o dólar contra emergentes em 127 e o IC-Br em dólar firme em 212; o modelo dá de 4,91 a 4,95, e o CDS × 1,2 leva a 4,88 a 4,92.
- **A tese em uma frase:** o modelo põe a PTAX em 5,13 no fim de 2026 e em 5,33 no 1T28; o 4T26 já incorpora a queda do CDS do 1º turno, e a alta de 2027 vem das commodities recuando, do carry encolhendo com os cortes da Selic e da inflação maior aqui do que nos EUA. Como o real de hoje (5,04) está 1,7% abaixo da central do 4T26, a cauda de apreciação pesa mais no 4T26; a partir do 2T27 pesa a de depreciação, quando o prêmio que caiu com a eleição precisa de validação fiscal.

## 3. Premissas

### 3.1 Etapa 1 — o modelo

O Modelo Estrutural[^2] parte do 3T26 observado (PTAX de 5,1809 em 30/09, `cmb_ptax`) e projeta do 4T26 em diante, com os pesos estimados até o 2T26. A equação do câmbio lê a **variação** de cada exógena de um trimestre para o outro, a partir do fechamento do 3T26.

**Cenários.**
- **Base:** o 2º turno (25/10) confirma a leitura do 1º turno e o CDS fica onde está no 4T26; em 2027 o plano fiscal do novo governo estabiliza a dívida devagar, sem convencer de todo, e o CDS sobe pouco. Lá fora, o petróleo alto mantém o CPI americano firme e o Fed sobe mais uma vez, no 1T27; o dólar contra emergentes e a bolsa americana ficam onde estão; as commodities sobem no 4T26 com o petróleo e recuam ao longo de 2027.
- **Worst:** o 2º turno reverte a leitura do 1º turno, ou, sem isso, o plano fiscal de 2027 não estabiliza a dívida; o CDS passa do nível de antes da eleição. Lá fora, o choque do petróleo leva o Fed a mais duas altas, o dólar se fortalece contra emergentes e a desaceleração global derruba as commodities em 2027.
- **Best:** o 2º turno confirma e o plano fiscal aponta para superávit primário; o CDS cai abaixo de 100 p.b. e a volatilidade do real recua. Lá fora, o Fed para, o dólar contra emergentes recua e as commodities ficam firmes.

**Caminhos das exógenas.** Níveis no fechamento do trimestre, na unidade do simulador.

| Exógena | Hoje (valor · tabela · data) | Cenário | 4T26 | 1T27 | 2T27 | 3T27 | 4T27 | 1T28 |
|---|---|---|---|---|---|---|---|---|
| CDS 5 anos (p.b.) | 112 · `cmb_risco_pais` · 14/10 | base | 112 | 112 | 115 | 118 | 120 | 120 |
| | | worst | 150 | 160 | 170 | 175 | 180 | 180 |
| | | best | 100 | 95 | 90 | 90 | 90 | 90 |
| Volatilidade implícita do real (% a.a.) | sem dado[^3]; a realizada de 63 dias está em 12,2 · "O real e os pares" · 14/10 | base | 12,19 | 12,19 | 12,19 | 12,19 | 12,19 | 12,19 |
| | | worst | 16 | 15 | 15 | 15 | 15 | 15 |
| | | best | 11 | 10,5 | 10,5 | 10,5 | 10,5 | 10,5 |
| Dólar contra emergentes (índice) | 129,77 · `cmb_dollar_index_em` · 09/10 | base | 129,8 | 129,8 | 129,8 | 129,8 | 129,8 | 129,8 |
| | | worst | 133 | 134 | 134 | 134 | 134 | 134 |
| | | best | 128 | 127 | 127 | 127 | 127 | 127 |
| S&P 500 (pontos) | 7.721 · `cmb_equity_us` · 15/10 | base | 7.721 | 7.721 | 7.721 | 7.721 | 7.721 | 7.721 |
| | | worst | 7.721 | 7.721 | 7.721 | 7.721 | 7.721 | 7.721 |
| | | best | 7.721 | 7.721 | 7.721 | 7.721 | 7.721 | 7.721 |
| IC-Br em dólar (índice) | 205,70 · `comm_icbr_usd` · set | base | 210 | 205 | 200 | 198 | 195 | 195 |
| | | worst | 205 | 195 | 190 | 185 | 185 | 185 |
| | | best | 212 | 212 | 212 | 212 | 212 | 212 |
| Fed Funds (% a.a.) | 3,875 (meta, ponto médio) · `us_interest_rate` · 15/10 | base | 3,875 | 4,125 | 4,125 | 4,125 | 4,125 | 4,125 |
| | | worst | 4,125 | 4,375 | 4,375 | 4,375 | 4,375 | 4,375 |
| | | best | 3,875 | 3,875 | 3,875 | 3,875 | 3,875 | 3,875 |
| CPI dos EUA (% no trimestre) | 3,72% em 12 meses · `diferenciais_juros` · set | base | 0,91 | 0,91 | 0,91 | 0,91 | 0,91 | 0,91 |
| | | worst | 1,00 | 1,00 | 1,00 | 1,00 | 1,00 | 1,00 |
| | | best | 0,91 | 0,91 | 0,91 | 0,91 | 0,91 | 0,91 |

- **CDS.** O modelo parte do fechamento do 3T26, 131,21 p.b. (`cmb_risco_pais`, 30/09), anterior ao 1º turno: o CDS foi de 131,04 em 02/10 a 108,96 em 06/10 e está em 112,19 em 14/10. A base de 112 no 4T26 é, para o modelo, uma queda de 131,21 para 112 no trimestre. A subida para 120 em 2027 vem da dívida: a bruta está em 82,9% do PIB, 5,5 p.p. acima de um ano antes, com déficit primário de 0,62% do PIB em 12 meses (`fisc_divida` e `fisc_nfsp`, ago).
- **Volatilidade implícita.** Não está nos dados; o simulador a segura em 12,19, o último valor que tem (2T26), e a base mantém esse número. Ela só entra como denominador do carry[^4]: no worst, o carry sobre a volatilidade, com a volatilidade a 16% e o Fed a 4,125%, soma +2,2% (em log) à PTAX no 4T26.
- **S&P 500 parado nos três cenários.** Na equação do câmbio a bolsa americana tem efeito positivo: com o dólar contra emergentes dado, +5% no S&P 500 deprecia o real em 1,13% no trimestre (pesos da mediana; coeficiente de 1,888, intervalo de 90% de 0,980 a 2,787). Uma queda da bolsa no worst apreciaria o real no modelo, o contrário do que a história de risco global pede; como nenhum dos três cenários passa pela bolsa americana, ela fica no nível de hoje. O 4T26 ainda leva +0,20% (em log) da alta de 7.651,54 (30/09) para 7.721.
- **Fed Funds.** A base põe mais uma alta no 1T27 porque o Treasury de 2 anos está em 4,79% (`us_interest_rate`, 13/10), 53 p.b. acima de três meses antes e acima da meta de 3,875%, e o CPI de 12 meses subiu 0,36 p.p. em um mês, para 3,72% (`diferenciais_juros`, set), com o Brent a US$ 125,44 (`comm_brent`, 06/10), +80,3% em três meses.
- **IC-Br em dólar.** A energia do índice subiu 10,6% em setembro (`comm_icbr_usd`), e a alta de 22,7% do Brent em um mês até 06/10 ainda não está no dado: daí 210 no 4T26. O recuo em 2027 é premissa do agente, a de que o petróleo volta. É o caminho que mais pesa na alta da central (próximo item).
- **CPI dos EUA.** A base usa o padrão do simulador, a média dos últimos quatro trimestres (0,91% no trimestre). No worst, 1,00% pelo petróleo; no modelo, inflação americana mais alta reduz a PTAX (o diferencial de inflação encolhe), o que atenua um pouco o worst.

**Saída do modelo.** A linha base da PTAX é a central da seção 1. Selic e IPCA são resolvidos pelo modelo; a Selic é premissa provisória até a resposta da política monetária (aguarda política monetária, S1).

| Variável | Cenário | 4T26 | 1T27 | 2T27 | 3T27 | 4T27 | 1T28 |
|---|---|---|---|---|---|---|---|
| PTAX de fechamento (R$/US$) | base | 5,13 | 5,21 | 5,25 | 5,26 | 5,31 | 5,33 |
| | worst | 5,54 | 5,70 | 5,78 | 5,82 | 5,86 | 5,88 |
| | best | 4,97 | 4,94 | 4,92 | 4,91 | 4,93 | 4,95 |
| Selic, média do trimestre (% a.a.) | base | 13,60 | 13,25 | 12,96 | 12,69 | 12,46 | 12,26 |
| | worst | 13,60 | 13,27 | 12,99 | 12,75 | 12,56 | 12,39 |
| | best | 13,60 | 13,25 | 12,94 | 12,66 | 12,41 | 12,19 |
| IPCA em 12 meses (%) | base | 5,27 | 4,82 | 4,31 | 4,33 | 4,24 | 4,12 |
| | worst | 5,32 | 4,98 | 4,56 | 4,64 | 4,56 | 4,37 |
| | best | 5,24 | 4,75 | 4,17 | 4,13 | 4,02 | 3,91 |

- **De onde vem a central.** No 4T26 a PTAX do modelo cai de 5,18 para 5,13 (−0,96% em log): a queda do CDS tira 1,62% e as commodities, 0,48%, enquanto o carry menor (Selic média de 14,06% no 3T26 para 13,60%, com o Fed a 3,875%) soma 0,42%, o diferencial de inflação 0,35% e o dólar contra emergentes 0,28%. Do 4T26 ao 1T28 ela sobe 3,85% (em log): o recuo das commodities soma 1,71%, o carry que encolhe com os cortes da Selic e a alta do Fed 1,13%, o diferencial de inflação 0,97% e o CDS 0,67%; a constante da equação tira 0,55%.
- **Quanto a central depende dos pesos.** A faixa de 90% do posterior[^5] vai de 5,09 a 5,18 no 4T26 e de 5,11 a 5,58 no 1T28. A PTAX de hoje, 5,0441 (14/10), está abaixo dela: o modelo explica pelo CDS uma parte da queda desde 30/09, e o resto é o que ele não vê (etapa 2).
- **A Selic quase não reage ao câmbio.** No worst ela termina o 1T28 em 12,39%, contra 12,26% na base, com a PTAX em 5,88 contra 5,33: a regra de juros do modelo responde ao desvio da expectativa contra a meta, e o câmbio só chega a ela pelo IPCA. O modelo não tem o BC defendendo a moeda com juros; se a política monetária responder a S4 que sim, o worst é menor do que este.

### 3.2 Etapa 2 — o tempero qualitativo

**(i) CDS 5 anos — efeito mais forte que o estimado** · cenários worst e best
- Coeficiente: estimado 25,11 (por desvio-padrão da variação do CDS; equivale a 0,084% de PTAX por p.b.), intervalo de 90% do posterior de 19,48 a 30,61. Multiplicador: × 1,2, que leva a 30,13, dentro do intervalo, no percentil 94 do posterior[^6].
- Efeito: worst de 5,54 para 5,56 no 4T26 e de 5,88 para 5,93 no 1T28; best de 4,97 para 4,94 no 4T26 e de 4,95 para 4,92 no 1T28.
- Por quê: o mercado acabou de mostrar o canal mais forte do que o modelo estima. De 02/10 a 06/10 a PTAX caiu 4,98% (em log) e o CDS 22 p.b.; descontado o dólar contra emergentes, a sensibilidade foi de 0,199% por p.b., 2,4 vezes a do modelo, e de 02/10 a 14/10, 2,2 vezes (`cmb_ptax`, `cmb_risco_pais`, `cmb_dollar_index_em`). O 2º turno e o plano fiscal de 2027 passam pelo mesmo canal, o prêmio de risco fiscal e político. Fico dentro do intervalo, e não perto das 2,2 vezes, por três razões: a janela é de dias e a equação é trimestral, e parte de um salto de um dia costuma voltar; na mesma janela a curva de juros inteira caiu (DI de 2 anos −134 p.b. em um mês, `br_di_grade`, 14/10), um prêmio que o CDS não mede sozinho; e a amostra da estimação, de 2006 a 2026, já tem 2008, 2015 e 2020.
- Onde entra: os limites e as probabilidades das duas caudas.

**(ii) Posicionamento — CFTC, contratos futuros de real (COT)** · cenário worst; assimetria da base
- Hoje: fundos alavancados com +27.396 contratos líquidos comprados em real, +11.350 em um mês, percentil 99 dos últimos 10 anos e 100 do histórico; asset managers com +56.610, percentil 89 (`cmb_cot_fx`, 06/10)[^7].
- Por que o modelo não vê: nenhuma exógena da equação mede quem já está comprado; o CDS e o dólar contra emergentes medem o choque, não quantos vendedores ele encontra.
- Efeito: no worst, +2% sobre o modelo no 4T26 e +1% no 1T27, zero depois. A desmontagem amplia a depreciação que o 2º turno começar e passa quando a posição se limpa. Na base, nenhum desvio: a posição cheia deixa pouco comprador novo e limita a apreciação adicional.
- Onde entra: limite da cauda worst no 4T26 e no 1T27; na base, segura a probabilidade da cauda best do 4T26 em 30%, apesar de a PTAX de hoje já estar perto do limite dela.

**(ii) O BC no mercado de câmbio — intervenção à vista e leilões de linha** · cenário worst
- Hoje: em setembro, venda de US$ 2,00 bi à vista e US$ 2,00 bi em linha; −US$ 8,00 bi à vista em 12 meses; reservas de US$ 362,6 bi em 14/10, −US$ 6,5 bi em um mês; estoque de swaps de −US$ 91,6 bi em agosto (`cmb_reservas_bc`).
- Por que o modelo não vê: a equação do câmbio não tem o BC; a oferta de dólar à vista, em linha ou em swap não está em nenhuma exógena.
- Efeito: −1% sobre o modelo no 4T26 e no 1T27. O BC vendeu em setembro e voltaria a vender numa depreciação desordenada; a venda atenua a pressão, não a elimina enquanto a causa continua[^8].
- Onde entra: limite da cauda worst no 4T26 e no 1T27.

Os temperos de 2027 são só o do tipo (i): posicionamento e BC são de curto prazo.

### 3.3 Da etapa 1 à tese

| Trimestre | Central (modelo, base) | Worst: modelo → com tempero | Best: modelo → com tempero |
|---|---|---|---|
| 4T26 | 5,13 | 5,54 → 5,61 | 4,97 → 4,94 |
| 1T27 | 5,21 | 5,70 → 5,73 | 4,94 → 4,91 |
| 2T27 | 5,25 | 5,78 → 5,82 | 4,92 → 4,89 |
| 3T27 | 5,26 | 5,82 → 5,86 | 4,91 → 4,88 |
| 4T27 | 5,31 | 5,86 → 5,91 | 4,93 → 4,89 |
| 1T28 | 5,33 | 5,88 → 5,93 | 4,95 → 4,92 |

**A faixa base** é a central mais e menos 0,75 desvio-padrão, em log, arredondada a R$ 0,05. O desvio junta o erro da equação do câmbio, 3,6% por trimestre e crescendo com a raiz do prazo, à incerteza dos pesos: vai de 3,7% no 4T26 a 9,3% no 1T28. Se só houvesse o erro da equação, 0,75 desvio para cada lado cobriria 55% dos casos; a probabilidade da faixa fica abaixo disso, entre 45% e 48%, porque os cenários worst e best somam massa fora dela. Os pontos das caudas, com tempero, caem fora da faixa em todos os trimestres.

**As probabilidades das caudas** são do agente. No 4T26 a best pesa mais (30% contra 22%): a PTAX de hoje, 5,04, já está dentro da faixa base, perto do limite de 5,00, e 1,7% abaixo da central, porque o modelo, que parte de 30/09, só vê pelo CDS uma parte da queda de outubro. A worst fica pouco provável no 4T26 porque o CDS de 112 segue perto do mínimo depois do 1º turno (108,96 em 06/10) e longe dos 131 de antes da eleição (30/09): o mercado já precifica a confirmação, e a reversão teria de vir contra esse preço. A partir do 2T27 a worst passa a pesar mais (28% a 31% contra 24% a 25%), porque o prêmio que caiu com a eleição precisa de um plano fiscal com a dívida bruta ainda subindo: a dívida subiu 5,5 p.p. do PIB em 12 meses (`fisc_divida`, ago) enquanto o CDS caía 40 p.b. (`cmb_risco_pais`, 14/10), e o worst de 2027 é esse prêmio sendo cobrado.

[^1]: Os dados não trazem informação eleitoral. As datas do 1º turno (04/10/2026) e do 2º turno (25/10/2026) são do calendário eleitoral público; o que se usa é a reação dos preços nas sessões seguintes ao 1º turno.
[^2]: O Modelo Estrutural é uma versão simplificada do modelo do Banco Central: cinco equações (hiato do produto, inflação, expectativas, Selic e câmbio) resolvidas juntas. A equação do câmbio explica a variação da PTAX num trimestre pela diferença de inflação entre Brasil e EUA e pela variação do CDS, do dólar contra emergentes, do carry sobre a volatilidade, do S&P 500 e do IC-Br em dólar. O agente escolhe os caminhos dessas variáveis; a Selic e a inflação, o modelo resolve.
[^3]: A volatilidade implícita das opções de dólar não está nos dados deste ciclo. O caminho dela é premissa declarada do agente.
[^4]: Carry sobre volatilidade: o juro a mais que se ganha por carregar reais (Selic menos Fed Funds) dividido pela oscilação que o mercado espera para a moeda. No 3T26, com a Selic média de 14,06%, o Fed Funds de 3,75% e a volatilidade de 12,19%, a razão era 0,85. Quanto maior, mais atraente o real para quem aplica no juro daqui; se a volatilidade sobe, o mesmo juro atrai menos.
[^5]: O modelo não tem um único conjunto de pesos, mas mil conjuntos compatíveis com o histórico (a distribuição posterior de uma estimação bayesiana). A faixa de 90% do posterior mostra quanto a central muda de um conjunto para outro. Ela não inclui as surpresas que a equação não explica, cujo tamanho típico é de 3,6% por trimestre; por isso não é a faixa da tese.
[^6]: Percentil 94 do posterior: só 6% dos conjuntos de pesos estimados dão ao CDS um efeito maior que o usado aqui.
[^7]: Quanto maior o percentil, mais comprados em real estão os fundos em relação ao histórico. Posicionamento extremo é lido como sinal contrário: quando os fundos já estão muito comprados, sobra pouco comprador novo, e uma notícia ruim provoca venda em bloco (Verde, §5.3).
[^8]: A intervenção como colchão temporário: a venda de dólares pelo BC atenua a pressão de saída, mas não a elimina enquanto a causa continua; compra tempo (Verde, §7.2).
