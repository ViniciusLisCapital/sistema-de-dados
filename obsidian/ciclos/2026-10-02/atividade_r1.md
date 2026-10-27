# Report — atividade · ciclo 2026-10-02 · rodada 1

Dados até: 02/10/2026 · Horizontes: 4T26 a 1T28, o hiato do produto de cada trimestre como o BC o mede (central, % do produto potencial)[^hiato], e o PIB interanual oficial do IBGE como linha companheira[^proc]

## 1. Tese

| Variável | Trimestre | Central | Base: faixa · P | Upside: limite · P | Downside: limite · P | P(up) − P(down) |
|---|---|---|---|---|---|---|
| Hiato do produto (BC, % do potencial) | 4T26 | 0,13 | −0,15 a 0,35 · 50% | acima de 0,35 · 20% | abaixo de −0,15 · 30% | −0,10 |
| | 1T27 | −0,08 | −0,45 a 0,30 · 50% | acima de 0,30 · 22% | abaixo de −0,45 · 28% | −0,06 |
| | 2T27 | −0,24 | −0,70 a 0,20 · 50% | acima de 0,20 · 23% | abaixo de −0,70 · 27% | −0,04 |
| | 3T27 | −0,36 | −0,90 a 0,15 · 50% | acima de 0,15 · 24% | abaixo de −0,90 · 26% | −0,02 |
| | 4T27 | −0,45 | −1,05 a 0,10 · 50% | acima de 0,10 · 25% | abaixo de −1,05 · 25% | 0,00 |
| | 1T28 | −0,51 | −1,15 a 0,10 · 50% | acima de 0,10 · 25% | abaixo de −1,15 · 25% | 0,00 |
| PIB, variação interanual (%) | 4T26 | 1,88 | 1,40 a 2,20 · 50% | acima de 2,20 · 18% | abaixo de 1,40 · 32% | −0,14 |
| | 1T27 | 1,81 | 1,30 a 2,25 · 50% | acima de 2,25 · 18% | abaixo de 1,30 · 32% | −0,14 |
| | 2T27 | 1,74 | 1,15 a 2,20 · 50% | acima de 2,20 · 20% | abaixo de 1,15 · 30% | −0,10 |
| | 3T27 | 1,72 | 1,10 a 2,25 · 50% | acima de 2,25 · 21% | abaixo de 1,10 · 29% | −0,08 |
| | 4T27 | 1,91 | 1,25 a 2,45 · 50% | acima de 2,45 · 22% | abaixo de 1,25 · 28% | −0,06 |
| | 1T28 | 2,06 | 1,35 a 2,60 · 50% | acima de 2,60 · 23% | abaixo de 1,35 · 27% | −0,04 |

**A tese em uma frase:** o hiato, que o BC estimou em 0,41% do potencial no 3T26, fecha no 4T26 e fica negativo a partir do 1T27, chegando a −0,51% no 1T28, porque a Selic segue cerca de 3 p.p. acima da âncora do modelo e o aperto do trimestre anterior tira ~0,2 p.p. do hiato a cada trimestre; o risco no começo do horizonte é de baixa, porque o dado mensal do 3T26 já está abaixo do que o hiato do BC supõe.

O que leva a cada cauda:
- **Hiato acima da faixa (upside: mais atividade, mais pressão inflacionária).** Etapa 1: o modelo não tem cenário de alta, porque o agente não escreve exógena e o caminho do `rr_10a` não move o hiato (seção 3.1). Etapa 2: o aperto transmite metade do estimado (`H.h2` × 0,5 dá 0,24 no 4T26 e −0,16 no 1T28, contra 0,13 e −0,51 no base), por causa do crédito direcionado e parafiscal e do impulso fiscal do 4T26–1T27; a isso se soma a revisão do BC para cima, que aconteceu em todos os 20 trimestres desde 3T21 (seção 2, Q3). Com tudo isso, o hiato do 4T26 passa de 0,35 e o do 1T28 de 0,10.
- **Hiato abaixo da faixa (downside: menos atividade, menos pressão inflacionária).** Etapa 1: o mesmo. Etapa 2: o ponto de partida está alto (um hiato de 0,10 no 3T26, compatível com o IBC-Br, dá −0,14 no 4T26 com os coeficientes medianos), o aperto transmite 1,5 vez o estimado (`H.h2` × 1,5 dá 0,02 no 4T26 e −0,85 no 1T28) e o ciclo de inadimplência aperta a oferta de crédito às famílias. Com os três, o hiato do 4T26 fica abaixo de −0,15 e o do 1T28 abaixo de −1,15.
- **PIB acima da faixa.** A cauda de alta do hiato, mais oferta: a extrativa cresceu 12,0% no 2T26 contra o 2T25 (`atv_pib_taxas` · 2T26) e um choque de oferta move o PIB mais que o hiato.
- **PIB abaixo da faixa.** A cauda de baixa do hiato, ou um potencial mais baixo que o implícito no hiato do BC: com o potencial de 2,00% da QPC, a mesma trajetória do hiato dá PIB de 1,39% no 4T26 e 1,32% no 1T27, perto do Focus (seção 2, Q4).

## 2. Argumentação

### Q1 — Onde está a atividade agora

**O 2T26 fechou com o PIB acima do que o dado mensal indicava, e com a demanda doméstica privada fraca.** O PIB cresceu 0,5% contra o 1T26, dessazonalizado, e 2,0% contra o 2T25 (`atv_pib_taxas` · 2T26), contra +0,3% do IBC-Br no trimestre (`atv_ibcbr` · F, "O trimestre pelos indicadores mensais"). Pela oferta, o crescimento veio da agropecuária (+2,8%) e da extrativa (+3,4%), enquanto a transformação caiu 0,4% e os serviços cresceram 0,2%. Pela demanda, o consumo das famílias caiu 0,4% e o investimento subiu 1,2%, com a importação (+1,8%) levando parte disso para fora (`atv_pib_taxas` · 2T26). O consumo do governo cresceu 0,4% no trimestre e 3,1% contra o 2T25.

**O 3T26 está em contração pelo dado mensal, e é isso que pesa contra o ponto de partida do modelo.**

| Indicador (dessaz.) | Média de jul–ago contra o 2T26 | Carrego: agosto contra o 2T26 | 2T26 contra 1T26 |
|---|---|---|---|
| IBC-Br | −0,6% | −0,4% | +0,3% |
| IBC-Br ex-agropecuária | −0,7% | −0,6% | +0,4% |
| Indústria geral (PIM) | −1,6% | −1,9% | +0,3% |
| Bens de capital | −0,2% | −0,6% | +0,2% |
| Bens de consumo duráveis | +2,0% | +1,5% | −0,1% |
| Varejo ampliado | −0,5% | −0,6% | −1,0% |
| Serviços (PMS) | 0,0% | −0,1% | +0,4% |

Fonte: `atv_ibcbr`, `atv_pim`, `atv_pim_uso`, `atv_pmc`, `atv_pms` · ago/2026 (F, "O trimestre pelos indicadores mensais").

Com setembro igual a agosto, o IBC-Br cai 0,55% no 3T26 contra o 2T26, e o ex-agropecuária 0,67% (`atv_ibcbr` · ago/2026). Em termos interanuais, sem ajuste, julho e agosto cresceram 1,17% contra os mesmos meses de 2025. Nos quatro trimestres até o 2T26, o PIB interanual ficou entre 0,12 e 0,47 p.p. acima do IBC-Br interanual (`atv_pib_taxas`, `atv_ibcbr`), o que põe o PIB do 3T26 em torno de 1,3% a 1,6% contra o 3T25. O mercado está acima disso: a QPC espera +0,20% contra o 2T26 e 1,82% contra o 3T25 (`expc_qpc` · R281, 23/09), e o Focus 1,80% (`expc_focus_periodo` · 02/10).

**O hiato do BC para o 3T26 supõe um trimestre mais forte que o dado mensal.** O BC estima 0,41 no 3T26 (`pm_hiato_produto` · edição de set/2026), o que, pela identidade da linha companheira, corresponde a 1,96% de PIB interanual (F, "O hiato do BC e o potencial implícito nele"). Com o PIB de 1,3% a 1,6% que o IBC-Br sugere, a mesma identidade dá um hiato de −0,2 a +0,1 no 3T26; com os 1,82% da QPC, 0,28. A distância, de 0,1 a 0,6 p.p., é o tamanho do desacordo com o ponto de partida, e ele entra como assimetria de baixa nos dois primeiros trimestres (seção 3.2). Mas a identidade é só uma média: o hiato do BC é suavizado dos dois lados e não acompanha o PIB trimestre a trimestre, e o 2T26 mostrou o PIB 0,2 p.p. acima do IBC-Br no trimestre. Um setembro forte (0,5% acima de agosto) ainda deixaria o IBC-Br em −0,38% no 3T26.

**O 4T26 começa sem carrego.** Se o IBC-Br ficar no nível de agosto até dezembro, o 4T26 cresce 1,15% contra o 4T25 (dessaz.; 0,98% no ex-agropecuária, `atv_ibcbr` · ago/2026), abaixo dos 1,88% da linha companheira, que supõe a atividade voltando a crescer.

### Q2 — O que move a atividade, e por qual canal

**A desaceleração é cíclica, concentrada nos setores sensíveis ao juro, e o crescimento que sobra vem da oferta.**

- **Política monetária (2.1).** Os segmentos que o mapa aponta como os primeiros a sentir o aperto estão caindo: móveis e eletrodomésticos −8,4% em 12 meses e −8,7% em 3 meses, veículos −2,1% em 3 meses (`atv_pmc` · ago/2026), bens de capital −3,9% em 12 meses (`atv_pim_uso` · ago/2026). O que mostra a transmissão em curso, com a Selic em 13,75% depois de cinco cortes de 0,25 p.p. desde 15,00% (`pm_copom_reuniao` · 16/09). Mas os bens duráveis da indústria subiram 3,2% em 12 meses e 2,0% no 3T26 até agosto (`atv_pim_uso`), e o investimento cresceu 1,2% no 2T26; se o investimento seguir crescendo no 3T26, o aperto está pesando mais no consumo que no capital, e a cauda de transmissão fraca ganha peso.
- **Crédito (2.2), TWA, premissas assumidas.** O preço do crédito às famílias subiu e a inadimplência com ele: taxa do livre PF em 61,74% a.a. (+2,95 p.p. em 12 meses), spread livre +2,29 p.p., inadimplência do livre PF em 8,01% (+1,04 p.p.) (`cred_credito_resumo` · ago/2026), comprometimento de renda em 28,72% (+1,40 p.p. em 12 meses, `cred_credito_familias` · jul/2026). Os bancos leem oferta restrita no consumo das famílias (−0,23, `cred_ptc` · 2T26). A parte disso que é efeito da Selic já está em (H); o ciclo de inadimplência, que restringe a oferta além da Selic, é tempero de baixa. **Contra**, o crédito às empresas por fora do juro livre cresce: concessões de capital de giro de R$ 534,9 bi em 12 meses contra R$ 335,3 bi um ano antes (`cred_modalidade_livre_pj` · ago/2026), saldo do BNDES +10,3% e rural +30,6% em 12 meses, com a taxa do BNDES em 11,73% a.a., abaixo da Selic (`cred_modalidade_direcionado_pj` · ago/2026). Crédito direcionado responde pouco à Selic (mapa 2.2), o que enfraquece a transmissão: é o tempero de alta sobre `H.h2`. No saldo, o fluxo financeiro do RPM está em −2,8% do PIB em 12 meses, 2,1 p.p. abaixo de um ano antes (`cred_fluxo_financeiro` · abr/2026), o que mostra o crédito total puxando para baixo, com dado de 184 dias.
- **Fiscal (2.3).** O primário do setor público em 12 meses foi a −0,62% do PIB, 0,43 p.p. pior que um ano antes (`fisc_nfsp` · ago/2026), e o consumo do governo nas contas nacionais cresce 3,1% contra o 2T25. As duas medidas apontam para estímulo; o tamanho e o tempo do impulso são do agente fiscal, que no r1 dele o lê expansionista no 4T26, fraco no 1T27 e neutro depois (aguarda fiscal, S-FI1). É tempero de alta nos dois primeiros trimestres.
- **Renda e trabalho (2.4).** A massa de rendimento real cresceu 4,8% em 12 meses e o rendimento real 3,7% (`mt_pnad` · ago/2026), o que sustenta o consumo. Mas o consumo das famílias caiu 0,4% no 2T26 e o varejo ampliado 0,5% no 3T26 até agosto: a renda cresce e o consumo não, compatível com o serviço da dívida tomando parte da renda (`cred_credito_familias`). O emprego formal desacelera, como o mapa espera de uma variável que segue o produto com atraso: o saldo de 12 meses da indústria de transformação caiu de 210,3 mil para 15,9 mil, e o do comércio de 322,2 mil para 97,7 mil (`mt_caged_setor` · ago/2026).
- **Externo (2.5).** A exportação em dólar cresce (US$ 375,0 bi em 12 meses até setembro, contra US$ 339,9 bi um ano antes, `cmb_comex_pais` · set/2026), com petróleo, soja e carnes acima de um ano antes (`cmb_comex_produto` · ago/2026). Mas em volume a exportação caiu 0,8% no 2T26 e 2,1% no 1T26 (`atv_pib_taxas`), e os termos de troca caíram 2,7% em 3 meses (`cmb_termos_troca` · jul/2026, 93 dias). O efeito sobre a renda é do lado do câmbio e do externo (aguarda S-CB2, S-EXT1).
- **Oferta (2.7).** A extrativa cresceu 12,0% e a agropecuária 6,8% no 2T26 contra o 2T25 (`atv_pib_taxas`), contra −0,9% da transformação. A medida do ciclo é o ex-agropecuária, e ele está pior que o total no 3T26 (−0,67% contra −0,55%, com setembro igual a agosto). O crescimento que sobra é de oferta, e por isso a linha do PIB tem risco de alta que o hiato não tem.

### Q3 — Quanta folga há

**O hiato do BC está positivo e caindo, mas cada edição o revê para cima.**

| Trimestre | Placar: 1º RPM depois do PIB | Edição dez/25 | Edição mar/26 | Edição jun/26 | Edição set/26 |
|---|---|---|---|---|---|
| 3T26 | ainda não saiu | — | — | — | 0,41 |
| 2T26 | 0,51 (set/26) | — | — | 0,36 | 0,51 |
| 1T26 | 0,49 (jun/26) | — | 0,13 | 0,49 | 0,60 |
| 4T25 | 0,39 (mar/26) | 0,17 | 0,39 | 0,60 | 0,74 |
| 3T25 | 0,54 (dez/25) | 0,54 | 0,70 | 0,82 | 0,95 |

Fonte: `pm_hiato_produto_vintages` · edições de dez/2025 a set/2026.

Nos 20 trimestres de 3T21 a 2T26, a central do primeiro RPM depois do PIB ficou acima da estimativa do fechamento do próprio trimestre em todos, em média 0,28 p.p. (de +0,01 a +0,67; +0,21 nos 8 trimestres desde a quebra metodológica de 2024) (`pm_hiato_produto_vintages`). E a revisão anda com o PIB do trimestre: a correlação entre ela e o PIB contra o trimestre anterior foi 0,58, e nos 5 trimestres com PIB até 0,3% a revisão média foi +0,11. Com um 3T26 de −0,3%, a reta dá +0,04. Na amostra não há trimestre de PIB negativo, então a regularidade não diz o que acontece num trimestre de contração: ela pesa para cima na pontuação, menos do que a média sugere neste ciclo. Na última edição, todos os trimestres desde 1T24 subiram, em média 0,09 p.p.

A dispersão entre os modelos do BC é grande: para o 3T26, p25 a p75 de 0,00 a 0,89, e mínimo a máximo de −0,33 a 1,81 (`pm_hiato_produto` · set/2026). O mercado vê um hiato um pouco maior que o modelo no fim de 2026 e menor em 2027: 0,20 no 4T26 e −0,20 no 4T27, este revisado de 0,00 (`expc_qpc` · R281), contra 0,13 e −0,45 no modelo.

**O mercado de trabalho mostra menos folga do que o hiato do BC.** A desocupação dessazonalizada do BC está em 5,41% (`mt_desocupacao_retro` · jul/2026), 1,89 a 2,04 p.p. abaixo da NAIRU que o mercado estima (7,30% no curto prazo, 7,45% em 5 anos, `expc_qpc` · R279) (F, "O hiato do BC e o potencial implícito nele"), e no percentil 1 da série desde 2004[^pctl]. O nível de ocupação está no percentil 99 e a subutilização no percentil 2 (`mt_pnad` · ago/2026). Um mercado de trabalho tão apertado com um hiato de 0,41 é uma das duas coisas: a NAIRU caiu mais do que a QPC registra, ou o hiato está subestimado. As duas não se decidem com os dados deste ciclo (Faltou). O sinal de preço é dos serviços, cuja inflação está em 5,97% em 12 meses (`inflc_agregados` · set/2026); se isso está acima do que o hiato explica é a leitura do agente de inflação (aguarda S-IN2).

**A minha leitura:** a folga está abrindo pela atividade (o 3T26) mais cedo do que o hiato do BC mostra, e o mercado de trabalho ainda não a mostra. A distância com o BC é de baixa no 3T26–4T26, e não muda a direção.

### Q4 — O cenário

**Por que a central.** A equação (H) diz que o hiato de um trimestre é 0,875 vezes o do trimestre anterior mais −0,071 vezes o aperto do trimestre anterior, medido como a Selic média menos a âncora `rr_10a + meta` (`modelo.listar`, medianas). No 3T26, a Selic média de 14,06% contra a âncora de 10,84% (7,84% do NTN-B de 10 anos na média do trimestre, mais 3,00% de meta) deu um aperto de 3,22 p.p. A persistência guarda 0,36 dos 0,41 do 3T26, e o aperto tira 0,23: o hiato do 4T26 é 0,13. Daí em diante, a Selic do modelo cai pela regra de juros, de 13,60% no 4T26 a 12,27% no 1T28, conforme a expectativa de inflação cai de 4,16% para 3,52%, e o aperto diminui de 2,76 para 1,43 p.p. Mesmo assim ele continua acima do que manteria o hiato parado, e o hiato chega a −0,51 no 1T28, ainda caindo.

Uma consequência do modelo que vale dizer antes de discordar: o NTN-B de 10 anos caiu 0,69 p.p. em 3 meses, para 7,51% (`br_interest_rate` · 02/10). Em (H), um juro longo mais baixo com a mesma Selic é uma política mais apertada. Mas a regra de juros usa a mesma âncora, e a Selic do modelo cai junto: com o caminho do `rr_10a` do agente fiscal (7,55 no 4T26 a 7,40 no 1T28), a Selic média do 4T26 cai de 13,60 para 13,31 e o aperto fica igual (2,76 nos dois), e o hiato também, até a segunda casa, em todos os trimestres. No modelo, o juro longo move o nível da Selic e não move a atividade. É aqui que o modelo perde o canal de custo de capital (mapa 2.6), e a proposta vai para a seção 6.

**Por que a linha do PIB.** A central é mecânica: o potencial implícito no hiato do BC (2,50% ao ano, média dos últimos quatro trimestres, F) mais a variação do hiato em quatro trimestres. Ela fica acima do consenso em 2027 (1,81% no 1T27 contra 1,40% do Focus, `expc_focus_periodo` · 02/10) por causa do potencial: o mercado o estima em 2,00% (`expc_qpc` · R279), e com 2,00% a mesma trajetória do hiato dá 1,32% no 1T27 e 1,42% no 4T27, perto do Focus. O modelo e o consenso concordam sobre a folga e divergem sobre o potencial. Esse é o principal motivo da assimetria de baixa na linha do PIB, maior que a do hiato.

**Por que a distribuição.** No 4T26 e no 1T27 o risco é de baixa, porque o dado mensal do 3T26 já é mais fraco do que o ponto de partida supõe (Q1), o crédito às famílias está num ciclo de inadimplência e o balanço de riscos do mercado também pesa para baixo (34% das respostas com risco de baixa para o PIB de 2026 e 73% para o de 2027, contra 4% e 1% de alta, `expc_qpc` · R281). Pesam contra isso a revisão do BC para cima, o impulso fiscal e parafiscal e o mercado de trabalho apertado. Do 2T27 em diante as duas forças se equilibram: um ponto de partida errado perde efeito com a persistência (um hiato 0,31 p.p. mais baixo no 3T26 deixa só 0,14 p.p. de diferença no 1T28), e o que decide é a força do aperto, com risco dos dois lados. A faixa abre com o horizonte porque a faixa do posterior abre (de −0,03 a 0,30 no 4T26 para −1,10 a 0,00 no 1T28, sem o erro das equações) e porque a revisão do BC soma até 0,67 p.p. num trimestre.

Signposts: o PIB do 3T26 abaixo de 1,5% contra o 3T25 (IBGE, dezembro) torna a cauda de baixa do 4T26 mais provável; a edição de dez/2026 do RPM com o 3T26 acima de 0,41 e o 2T26 revisado para cima de novo a torna menos provável; desocupação dessazonalizada acima de 6,0% (`mt_desocupacao_retro`) diria que a folga chegou ao trabalho.

### Olhado, sem sinal

- Varejo restrito · −0,4% em 3 meses e +1,0% em 12 meses (`atv_pmc` · ago/2026) · na mesma direção do ampliado, sem informação a mais · diria algo se divergisse do ampliado (veículos e material de construção).
- Serviços prestados às famílias · +2,1% no mês (`atv_pms` · ago/2026) · um mês, numa série de 4,2% em 12 meses · diria algo se três meses seguidos acelerassem o total dos serviços.
- PIB nominal em 12 meses · R$ 13.402 bi, +7,0% (`atv_pib_mensal` · set/2026) · deflator, não volume · diria algo para a dívida (agente fiscal).
- Capacidade de financiamento · −2,3% do PIB, 1,1 p.p. melhor em 12 meses (`atv_renda_poupanca` · 2T26) · consequência da queda da formação de capital (−1,1 p.p.), com a poupança parada em 14,4% · diria algo se a poupança se movesse.
- Taxa de participação · 62,2% (`mt_pnad` · ago/2026) · estável em 12 meses (−0,1 p.p.) · diria algo se caísse junto com a desocupação (desalento).
- PTAX · R$ 5,2238, +1,9% em um mês (`cmb_ptax` · 02/10) · movimento de um mês, cuja persistência é do agente de câmbio · diria algo se ele a classificar como persistente (S-CB1).
- IC-Br energia em dólar · +29,2% em 12 meses (`comm_icbr_usd` · set/2026) · renda do petróleo, que já aparece na extrativa · diria algo pelo investimento do setor se o caminho do externo o mantiver.

## 3. Premissas

### 3.1 Etapa 1 — o modelo

**Cenários.**
- Base: o padrão do simulador. O Copom segue cortando pela regra de juros do modelo, a meta fica em 3,00% e o NTN-B de 10 anos na média do 3T26.
- Upside e downside: não há cenário de exógena para as caudas do hiato. O agente não tem nível na aba "Exógenas", e as duas exógenas que (H) lê não movem o hiato no modelo (o `rr_10a` acima; a meta, fixa em 3,00%, não tem história de mudança neste ciclo). As caudas saem da etapa 2.

**Caminhos das exógenas.** Nenhum escrito. As duas que (H) lê, no padrão do simulador, com status **assumida, aguarda** quem tem a tutela:

| Exógena | Hoje (valor · tabela · data) | Cenário | 4T26 | 1T27 | 2T27 | 3T27 | 4T27 | 1T28 |
|---|---|---|---|---|---|---|---|---|
| `rr_10a`, NTN-B 10 anos, média do trimestre (%) | 7,51 · `br_interest_rate` · 02/10 (média do 3T26: 7,84) | base (padrão) | 7,84 | 7,84 | 7,84 | 7,84 | 7,84 | 7,84 |
| `meta_12m`, meta de inflação (%) | 3,00 · `inflc_meta` · 2026 | base (padrão) | 3,00 | 3,00 | 3,00 | 3,00 | 3,00 | 3,00 |

O `rr_10a` aguarda o agente fiscal (o r1 dele escreve 7,55 a 7,40) e a meta aguarda o de política monetária. Com o caminho do fiscal, o hiato fica igual até a segunda casa (Q4), então a central desta tese não depende dessa espera.

**Saída do modelo.**

| Variável | Cenário | 4T26 | 1T27 | 2T27 | 3T27 | 4T27 | 1T28 |
|---|---|---|---|---|---|---|---|
| Hiato (% do potencial) | base | 0,13 | −0,08 | −0,24 | −0,36 | −0,45 | −0,51 |
| | `H.h2` × 0,5 | 0,24 | 0,12 | 0,02 | −0,06 | −0,12 | −0,16 |
| | `H.h2` × 1,5 | 0,02 | −0,28 | −0,50 | −0,66 | −0,78 | −0,85 |
| | `H.h2` × 1,5 e `H.h1` × 1,05 | 0,03 | −0,26 | −0,50 | −0,68 | −0,82 | −0,93 |
| Selic, média do trimestre (%) | base | 13,60 | 13,26 | 12,96 | 12,70 | 12,47 | 12,27 |
| | base com o `rr_10a` do fiscal | 13,31 | 13,01 | 12,67 | 12,36 | 12,08 | 11,83 |
| IPCA 12 meses, fim do trimestre (%) | base | 5,28 | 4,85 | 4,33 | 4,34 | 4,23 | 4,08 |
| PIB interanual, conta mecânica (%) | base | 1,88 | 1,81 | 1,74 | 1,72 | 1,91 | 2,06 |
| | `H.h2` × 0,5 | 1,99 | 2,01 | 2,00 | 2,02 | 2,13 | 2,21 |
| | `H.h2` × 1,5 | 1,77 | 1,61 | 1,48 | 1,42 | 1,69 | 1,92 |
| | base, potencial da QPC (2,00%) | 1,39 | 1,32 | 1,25 | 1,23 | 1,42 | 1,57 |

Os multiplicadores mudam a Selic só na segunda casa (13,60 no 4T26 nos três), porque a regra de juros não lê o hiato.

### 3.2 Etapa 2 — o tempero qualitativo

**(i) `H.h2`, o efeito do aperto — mais fraco que o estimado** · cenário upside
- Coeficiente: estimado −0,071, intervalo de 90% do posterior −0,121 a −0,023. Multiplicador: × 0,5 (−0,036), dentro do intervalo.
- Efeito: hiato de 0,13 para 0,24 no 4T26 e de −0,51 para −0,16 no 1T28.
- Por quê: o crédito direcionado e o parafiscal crescem com taxas abaixo da Selic (BNDES a 11,73% a.a., saldo rural +30,6% em 12 meses), e a concessão de capital de giro subiu de R$ 335,3 bi para R$ 534,9 bi em 12 meses (`cred_modalidade_direcionado_pj`, `cred_modalidade_livre_pj` · ago/2026): uma parte maior do crédito que não responde à Selic; a massa de rendimento real cresce 4,8% em 12 meses (`mt_pnad`).
- Onde entra: limite e probabilidade da cauda de alta.

**(i) `H.h2` e `H.h1` — aperto mais forte e mais persistente que o estimado** · cenário downside
- Coeficientes: `H.h2` −0,071 (−0,121 a −0,023), × 1,5 (−0,107), dentro; `H.h1` 0,875 (0,794 a 0,953), × 1,05 (0,919), dentro.
- Efeito: hiato de 0,13 para 0,03 no 4T26 e de −0,51 para −0,93 no 1T28.
- Por quê: os segmentos sensíveis ao juro já caem mais do que a média (móveis e eletrodomésticos −8,4% e bens de capital −3,9% em 12 meses), o comprometimento de renda subiu 1,40 p.p. em 12 meses, e o 3T26 contrai com a Selic cortada só 1,25 p.p.
- Onde entra: limite e probabilidade da cauda de baixa, com mais peso do 2T27 em diante.

**(ii) Ponto de partida do modelo — hiato do BC no 3T26** · cenário base
- Hoje: 0,41 (`pm_hiato_produto` · set/2026), compatível com 1,96% de PIB interanual; o IBC-Br sugere 1,3% a 1,6% (Q1).
- Por que o modelo não vê: o modelo parte da estimativa do BC por construção, e o agente não move a central (mapa, Parte 1, item 6).
- Efeito: um hiato de 0,10 no 3T26 dá −0,14 no 4T26 (−0,27 contra o base) e deixa −0,14 p.p. no 1T28; um de 0,28, o da QPC, dá 0,02 no 4T26. Contra isso, a revisão do BC para cima (+0,04 a +0,11 p.p. num trimestre de PIB fraco, Q3).
- Onde entra: assimetria de baixa do 4T26 (−0,10) e do 1T27 (−0,06), e o limite inferior desses dois trimestres.

**(ii) Ciclo de inadimplência e oferta de crédito às famílias — inadimplência do livre PF** · cenário downside
- Hoje: 8,01% da carteira, +1,04 p.p. em 12 meses (`cred_credito_resumo` · ago/2026); oferta para consumo de −0,23 (`cred_ptc` · 2T26). Premissa assumida (TWA).
- Por que o modelo não vê: (H) não tem termo de crédito; a parte da inadimplência que vem da Selic já está em `H.h2`, e a restrição de oferta dos bancos além disso não está em lugar nenhum.
- Efeito: −0,1 p.p. no hiato do 1T27 ao 1T28, acumulando pelo consumo das famílias.
- Onde entra: limite da cauda de baixa.

**(ii) Impulso fiscal e parafiscal — primário de 12 meses e crédito público** · cenário base
- Hoje: primário de −0,62% do PIB em 12 meses, 0,43 p.p. pior que um ano antes (`fisc_nfsp` · ago/2026); consumo do governo +3,1% contra o 2T25 (`atv_pib_taxas`). Direção e tempo: aguarda fiscal (S-FI1).
- Por que o modelo não vê: (H) não tem termo fiscal; o efeito indireto, pelo `rr_10a`, não move o hiato no modelo (Q4), então não há dupla contagem.
- Efeito: +0,05 a +0,10 p.p. no hiato do 4T26 e do 1T27, perto de zero depois. Não há multiplicador fiscal nos dados nem no retrato deste ciclo; o tamanho é julgamento (Faltou).
- Onde entra: assimetria do base (reduz a de baixa nos dois primeiros trimestres) e limite da cauda de alta.

**(ii) Oferta: extrativa e agropecuária — PIB setorial** · cenário upside da linha do PIB
- Hoje: extrativa +12,0% e agropecuária +6,8% no 2T26 contra o 2T25 (`atv_pib_taxas`); agropecuária do IBC-Br −1,8% em agosto (`atv_ibcbr`).
- Por que o modelo não vê: as dummies de crise são zero na projeção, e o choque de oferta pode mover o potencial tanto quanto o produto.
- Efeito: +0,1 a +0,2 p.p. no PIB interanual do 4T26–1T27 sem mover o hiato.
- Onde entra: limite da cauda de alta da linha do PIB.

### 3.3 Da etapa 1 à tese

| Trimestre | Central (modelo, base) | Upside: modelo → com tempero | Downside: modelo → com tempero |
|---|---|---|---|
| 4T26 | 0,13 | 0,13 → 0,24 (`H.h2` × 0,5) → ~0,35 (impulso fiscal e revisão do BC) | 0,13 → 0,02 (`H.h2` × 1,5) → ~−0,15 a −0,25 (ponto de partida em 0,10 a 0,28) |
| 1T27 | −0,08 | −0,08 → 0,12 → ~0,30 | −0,08 → −0,28 → ~−0,45 (ponto de partida, inadimplência) |
| 2T27 | −0,24 | −0,24 → 0,02 → ~0,20 | −0,24 → −0,50 → ~−0,70 |
| 3T27 | −0,36 | −0,36 → −0,06 → ~0,15 | −0,36 → −0,68 → ~−0,90 |
| 4T27 | −0,45 | −0,45 → −0,12 → ~0,10 | −0,45 → −0,82 → ~−1,05 |
| 1T28 | −0,51 | −0,51 → −0,16 → ~0,10 | −0,51 → −0,93 → ~−1,15 |

A faixa base vai do ponto em que os dois temperos de cada lado se somam ao ponto em que um deles falha, e a probabilidade de 50% dentro dela reflete que cada cauda precisa de dois fatores na mesma direção. A assimetria de baixa do 4T26 e do 1T27 é o ponto de partida; ela some até o 4T27 porque a persistência apaga o erro de partida e o que fica é a força do aperto, com risco dos dois lados. A linha do PIB soma à assimetria do hiato a do potencial (2,50% do BC contra 2,00% do mercado), e por isso pesa mais para baixo.

## 4. Para os outros agentes

**Respostas às entradas fixas (Parte 4 do mapa).**
- **E1 (PM S10), em destaque:** a trajetória do hiato é a da seção 1, e ela muda de sinal no 1T27; a edição de set/2026 do RPM reviu para cima todos os trimestres recentes (+0,15 no 2T26, +0,11 no 1T26, +0,14 no 4T25, `pm_hiato_produto_vintages`). Trabalho: desocupação de 5,41%, cerca de 2 p.p. abaixo da NAIRU do mercado, com rendimento real +3,7% em 12 meses; a produtividade não está nos dados deste ciclo.
- **E2 (inflação IN-S5), em destaque:** o hiato muda de sinal no 1T27. A pressão de demanda está mais na renda (massa real +4,8% em 12 meses) que no consumo de bens (varejo ampliado −0,5% no 3T26 até agosto); serviços às famílias +4,2% em 12 meses e o total dos serviços estável no 3T26 (`atv_pms`). A atividade de serviços não diverge do hiato neste ciclo.
- **E3 (fiscal FS-AT1):** crescimento e hiato na seção 1; o PIB interanual da tese fica 0,4 p.p. acima do Focus em 2027 só por causa do potencial (Q4). Se o potencial for o da QPC, o g do r − g cai na mesma medida.
- **E4 (fiscal FS-AT2):** consumo do governo +0,4% no 2T26 e +3,1% contra o 2T25, 19,6% do PIB em 4 trimestres contra 18,7% um ano antes (`atv_pib_valores_correntes`); mesma direção do impulso que o agente fiscal dá, sem alerta.
- **E5 (expectativas XS9), em destaque:** o hiato vira negativo no 1T27; a atividade de serviços não sobe com o hiato positivo neste ciclo (−0,1% de carrego no 3T26).

**Pedidos (saídas da Parte 3 e deste ciclo).**
- **S-PM1:** qual a Selic média e de fechamento de cada trimestre do 4T26 ao 1T28, e o balanço de riscos? A Selic do modelo cai a 12,27% no 1T28; um ritmo de 0,25 p.p. por reunião daria outra trajetória do aperto e move as caudas do 2T27 em diante.
- **S-PM2:** com a Selic em 13,75% e o neutro de curto prazo da QPC em 6,40% (`expc_qpc` · R279), quanto a política é restritiva na sua leitura, e o NTN-B de 10 anos (7,51%) carrega quanto de prêmio que o neutro não carrega? Se o aperto efetivo for maior que o do modelo, o multiplicador × 1,5 em `H.h2` ganha peso.
- **S-PM3:** como o Copom leu a atividade e o mercado de trabalho na ata de setembro e no RPM, e o que explicou a revisão para cima dos trimestres recentes? É a pergunta que decide se a revisão do BC continua pesando para cima na pontuação.
- **S-CB1:** a alta de 1,9% da PTAX em um mês é persistente? Uma depreciação persistente aperta a renda real pelo lado dos preços (tempero de baixa no consumo).
- **S-CB2:** a queda de 2,7% dos termos de troca em 3 meses é preço ou volume, e persiste? Ela decide se a renda do setor exportador sustenta o investimento.
- **S-IN1:** qual a trajetória do IPCA, com alimentação e monitorados? O modelo leva o IPCA a 5,28% no 4T26, o que corrói a massa real que sustenta o consumo.
- **S-IN2:** os serviços (5,97% em 12 meses) estão acima do que um hiato de 0,41 explica? Se sim, é evidência de que o hiato está subestimado, como o mercado de trabalho sugere, e a cauda de alta ganha peso.
- **S-FI1:** qual o impulso fiscal e parafiscal por trimestre, em p.p. do PIB, e quanto dele é transferência às famílias? O tempero fiscal da seção 3.2 está em +0,05 a +0,10 p.p. no 4T26–1T27, sem multiplicador nos dados.
- **S-FI2:** qual o caminho do `rr_10a` e a parte de prêmio fiscal nele? No modelo ele não move o hiato; o prêmio é custo de capital que o modelo não vê (seção 6).
- **S-EXT1:** qual a probabilidade de recessão global no horizonte, e o crescimento da China e dos EUA? As exportações para os EUA caíram de US$ 40,4 bi para US$ 35,8 bi em 12 meses (`cmb_comex_pais` · set/2026).
- **S-EXT2:** qual o caminho das commodities em dólar, energia e metais? Renda e investimento da extrativa.
- **S-EXT3:** há episódio de aversão a risco ou mudança no Fed no horizonte? Chega ao crédito e ao juro longo.
- **S-EXP1:** o Focus de PIB foi revisto para baixo em 4 semanas (2026 −0,08 e 2027 −0,10 p.p.) e a QPC do hiato de 2027 de 0,00 para −0,20: o consenso está convergindo para um hiato negativo em 2027, ou é revisão de potencial?
- **S-EXP2:** o crescimento potencial de 2,00% e a NAIRU de 7,30% a 7,45% da QPC são de jun/2026 (R279); há leitura mais recente? A NAIRU decide o cruzamento do mercado de trabalho com o hiato, e o potencial explica toda a diferença entre a linha do PIB e o Focus.

## 5. Placar

Primeiro ciclo: não há report anterior a pontuar.

## 6. Sobre o modelo

Sem literatura neste ciclo; as propostas saem dos dados e do mapa.

| Fonte | O que sugere (regressor, defasagem, quebra, âncora) | Teste proposto (dado, amostra, que resultado mudaria a especificação) | Por que importa para a tese deste ciclo |
|---|---|---|---|
| Mapa 2.1 e 2.6; G deste ciclo (o `rr_10a` do fiscal muda a Selic e deixa o hiato igual) | A âncora `rr_10a + meta` está em (R) e em (H), então um movimento do juro longo se cancela: o prêmio no NTN-B não tem efeito real. Separar a âncora em neutro (QPC, ou uma média longa) e prêmio, e pôr o prêmio em (H) como custo de capital com sinal próprio | (H) com o aperto contra um neutro de fundamentos mais o termo `rr_10a − neutro`, 2006–2026 na edição atual do hiato. Se o termo de prêmio tiver sinal negativo e intervalo fora de zero, o modelo passa a ter o canal de custo de capital | O NTN-B caiu 0,69 p.p. em 3 meses; no modelo isso não alivia nem aperta a atividade |
| Mapa 2.8; `pm_hiato_produto_vintages` (20 de 20 revisões para cima) | (H) é estimada na série reescrita, mas a tese é pontuada no 1º RPM depois do PIB; um viés de revisão desloca a pontuação sem mudar o modelo | Medir a revisão do nowcast ao placar contra o PIB do trimestre e a surpresa contra a QPC, com todas as edições desde 2021-09; se a revisão for previsível, ela entra como correção do ponto de partida (o objetivo do usuário de regredir a parte consolidada do hiato, Parte 1, item 4) | A revisão média de +0,28 p.p. é do tamanho da assimetria do 4T26 |
| Mapa 2.2; `cred_fluxo_financeiro`, `cred_modalidade_direcionado_pj` | Um termo de condições de crédito em (H) além da Selic (o fluxo financeiro do RPM, ou a parte direcionada do crédito) | Acrescentar o fluxo financeiro em % do PIB, defasado 1 a 2 trimestres, 2012–2026; se significativo, o tempero de crédito sai do julgamento | O crédito direcionado e o parafiscal são a principal razão da cauda de alta |

[^hiato]: **Hiato do produto** é a distância, em % do produto potencial, entre o que a economia produz e o que ela produziria sem pressionar a inflação. **Produto potencial** é esse nível sustentável, que não se observa e é estimado. Um hiato de +0,5 quer dizer que a economia opera 0,5% acima do potencial, o que tende a acelerar a inflação; −0,5, que há folga. O número é uma estimativa do BC, revista a cada Relatório de Política Monetária, e não um dado observado.

[^pctl]: O percentil diz onde o último valor fica no histórico da série: 0 é o menor já visto, 100 o maior. A desocupação no percentil 1 quer dizer que só 1% dos meses desde 2004 tiveram desocupação mais baixa.

[^proc]: Rodada 1, sem literatura: o agente leu só o mapa conceitual da área e os dados do ciclo, até 02/10/2026. O agente não escreve caminho de exógena do Modelo Estrutural (não tem nível na aba de tutela); a central do hiato é a do modelo no padrão do simulador. O **carrego** (carry-over) é quanto um trimestre cresce sobre o anterior se os meses que faltam repetirem o último: um índice que fecha agosto 0,4% abaixo da média do trimestre anterior "carrega" −0,4% para o 3T26. A **NAIRU** é a taxa de desocupação que não acelera os salários; desocupação abaixo dela indica mercado de trabalho apertado.
