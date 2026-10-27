# Report — inflação · ciclo 2026-10-02 · rodada 1

Dados até: 2026-10-02 · Horizontes: 4T26 a 1T28, os seis trimestres do Modelo Estrutural a partir do trimestre em curso, com a variável medida no fechamento do trimestre (IPCA acumulado em 12 meses de dezembro, março, junho, setembro)

Informação usada: o IPCA até ago/26 e o IPCA-15 de set/26. O IPCA de set/26 saiu em 9/10, depois do corte, e fica fora da argumentação[^corte].

## 1. Tese

| Variável | Trimestre | Central | Base: faixa · P | Upside: limite · P | Downside: limite · P | P(up) − P(down) |
|---|---|---|---|---|---|---|
| IPCA 12 meses, fim do trimestre (%) | 4T26 | 5,28 | 5,05 a 5,50 · 50% | acima de 5,50 · 28% | abaixo de 5,05 · 22% | +0,06 |
| | 1T27 | 4,85 | 4,55 a 5,15 · 48% | acima de 5,15 · 32% | abaixo de 4,55 · 20% | +0,12 |
| | 2T27 | 4,33 | 4,00 a 4,70 · 45% | acima de 4,70 · 35% | abaixo de 4,00 · 20% | +0,15 |
| | 3T27 | 4,34 | 4,00 a 4,75 · 43% | acima de 4,75 · 36% | abaixo de 4,00 · 21% | +0,15 |
| | 4T27 | 4,23 | 3,90 a 4,65 · 42% | acima de 4,65 · 33% | abaixo de 3,90 · 25% | +0,08 |
| | 1T28 | 4,08 | 3,85 a 4,40 · 40% | acima de 4,40 · 33% | abaixo de 3,85 · 27% | +0,06 |

A central é o `ipca_12m` do Modelo Estrutural no cenário base (seção 3.1), sem ajuste.

**Os quatro grupos na central** (contribuição para o IPCA de 12 meses, p.p., cenário base do modelo):

| Trimestre | Serviços | Alimentação | Bens industriais | Monitorados | Resíduo | IPCA 12m |
|---|---|---|---|---|---|---|
| 3T26 (partida) | 2,14 | 0,66 | 0,69 | 1,09 | 0,00 | 4,58 |
| 4T26 | 2,06 | 0,96 | 0,90 | 1,37 | 0,00 | 5,28 |
| 1T27 | 1,96 | 0,88 | 0,81 | 1,22 | −0,01 | 4,85 |
| 2T27 | 1,96 | 0,59 | 0,77 | 1,01 | 0,00 | 4,33 |
| 3T27 | 1,86 | 0,64 | 0,80 | 1,05 | 0,00 | 4,34 |
| 4T27 | 1,76 | 0,63 | 0,82 | 1,01 | 0,00 | 4,23 |
| 1T28 | 1,69 | 0,61 | 0,81 | 0,97 | 0,00 | 4,08 |

A assimetria está nos **monitorados**: o upside sai de combustíveis (o Brent quase dobrou e a bomba não acompanhou) e o downside, menor, de energia elétrica. Alimentação e bens industriais carregam a parte da cauda que vem das commodities em dólar; serviços não carregam cauda neste ciclo.

- **Acima da faixa** (pior para o Brasil: o choque é de custo e chega sem demanda que o justifique): as commodities agrícolas e os metais em dólar vão ao percentil 90 da variação histórica e o repasse a alimentos é 1,4 vez o estimado, o que leva o modelo a 5,54 no 4T26 e 4,57 no 1T28; um reajuste de combustíveis no 4T26 (+6% nos combustíveis de veículos, +5% nos domésticos) soma +0,40 p.p. enquanto está na janela de 12 meses, e chega a 5,94 no 4T26 e 5,57 no 3T27.
- **Abaixo da faixa**: as commodities vão ao percentil 10, o que leva o modelo a 5,13 no 4T26 e 3,82 no 1T28; a energia elétrica devolve 5% (bandeira mais barata) e os alimentos in natura recuam, −0,28 p.p. até o 3T27, o que dá 4,85 no 4T26 e 3,62 no 3T27. Se o recuo vier de corte de tributo ou de preço de combustível segurado por decisão, ele é custo adiado, e não boa notícia.

**A tese em uma frase:** o IPCA de 12 meses sobe a ~5,3% no 4T26 porque saem da janela os meses baixos do 4T25, e cai devagar até ~4,1% no 1T28, segurado por serviços, cuja persistência o modelo estima alta; o risco é de alta, concentrado em combustíveis, porque o petróleo a US$ 135 ainda não chegou à bomba.

## 2. Argumentação

### Q1 — O que explica a inflação corrente: choque ou tendência?

**Os dois últimos números são choque de preço relativo, e a tendência corre abaixo do padrão sazonal.** O IPCA de agosto foi −0,32% (`inflc_agregados` · ago/26), abaixo do mesmo mês em 9 dos 10 anos anteriores (média de agosto de 2016 a 2025: 0,15%), porque três itens o puxaram para baixo: energia elétrica residencial −7,63% (−0,33 p.p.), passagem aérea −13,17% (−0,11 p.p.) e batata-inglesa −19,89% (−0,05 p.p.) (`inflc_decomposicao` · ago/26). O IPCA-15 de setembro veio na direção oposta, 0,70% (`inflc_agregados` · set/26), acima do mesmo mês em 9 de 10 anos (média 0,27%), e pelos mesmos itens: energia +7,42% (+0,29 p.p.), passagem aérea +9,82% (+0,08 p.p.) e tomate +20,76% (+0,04 p.p.) (`inflc_decomposicao`, IPCA-15 · set/26). Energia de −7,63% num mês e +7,42% no seguinte é uma oscilação, e não um nível: o IPCA-15 acumula 2,82% de energia em 12 meses até setembro.

| IPCA-15 set/26, grupos do BC | Variação (%) | Contribuição (p.p.) |
|---|---|---|
| Serviços | 0,59 | 0,22 |
| Alimentação | 0,38 | 0,06 |
| Bens industriais | 0,43 | 0,10 |
| Monitorados | 1,28 | 0,33 |

Fonte: `inflc_decomposicao` (IPCA-15 · set/26), subitens agregados pela classificação do BC (`inflc_dim`).

**Os núcleos[^nucleo] dizem que a tendência não acelerou, e até corre abaixo do padrão.** Em agosto, o EX3 foi 0,27% e o de médias aparadas com suavização 0,29%, contra médias de agosto de 0,37% nos dois (`inflc_agregados` · ago/26). No trimestre de junho a agosto o EX3 acumulou 0,74% contra 1,00% na média da mesma janela dos dez anos anteriores, e as médias aparadas 0,82% contra 1,11%. A média de EX0, EX3, médias aparadas, P55 e dupla ponderação foi 0,23% em agosto. A difusão foi 54,4% em agosto (`inflc_agregados` · ago/26), no percentil 28 dos últimos dez anos[^pctl], contra média de 58,8%: poucos itens sobem, o que é a assinatura de um choque concentrado.

| Núcleo, ago/26 | Mês (%) | 3 meses (%) | 12 meses (%) | 12 meses, 3 meses antes (%) |
|---|---|---|---|---|
| EX0 | 0,18 | 0,73 | 4,50 | 4,68 |
| EX3 | 0,27 | 0,74 | 4,45 | 4,70 |
| EXFE | 0,22 | 0,77 | 4,46 | 4,74 |
| Médias aparadas com suavização | 0,29 | 0,82 | 4,34 | 4,48 |
| P55 | 0,27 | 0,73 | 4,61 | 4,63 |
| Dupla ponderação | 0,14 | 0,46 | 3,88 | 4,12 |

Fonte: `inflc_agregados` (ago/26). Os seis núcleos caíram em 12 meses no trimestre.

**Serviços subjacentes são a exceção que pede atenção, mas não mudam a leitura.** Subiram 0,42% em julho e 0,40% em agosto, 1,04% de junho a agosto (`inflc_decomposicao` · ago/26), e o EX3 de serviços acumula 4,99% em 12 meses (`inflc_agregados` · ago/26), acima da meta de 3,00% (`inflc_meta` · 2026). Mas o IPCA-15 de setembro trouxe serviços subjacentes a 0,28% (`inflc_decomposicao`, IPCA-15 · set/26), e o QPC esperava 0,30% para o IPCA de setembro (`expc_qpc` · 23/09): o ritmo está alto em nível, sem aceleração no trimestre. Isso mudaria se o subjacente voltasse a 0,40% ou mais nos dois próximos meses.

**Um item fora da curva nos bens industriais: cigarro**, +19,59% em agosto (+0,11 p.p., o maior impulso para cima do mês) e +14,00% no IPCA-15 de setembro (+0,09 p.p.) (`inflc_decomposicao` · ago/26 e set/26). Um salto desse tamanho num item é, em geral, decisão de tributo ou de preço mínimo, e não tendência; é pedido ao fiscal (IN-S6). Ele importa para o modelo porque a inércia dos bens industriais é alta (`I.II.ii1` 0,537), e a equação propaga um degrau de nível como se fosse persistência.

**Qual mês move o 12 meses.** De julho para agosto o IPCA de 12 meses caiu de 4,44% para 4,22% (`inflc_indice_geral` · ago/26) porque entrou o −0,32% de ago/26 e saiu o −0,11% de ago/25. No 4T26 o movimento vem do mês que sai: out/25, nov/25 e dez/25 foram 0,09%, 0,18% e 0,33% (`inflc_indice_geral`), com energia a −2,39% em outubro e −2,41% em dezembro (`inflc_decomposicao`). Com as medianas do QPC para setembro a dezembro (0,56%, 0,34%, 0,32% e 0,55%, `expc_qpc` · 23/09), o 12 meses de dezembro iria a 4,94%, contra 4,30% em setembro: a alta de 0,64 p.p. no 4T26 é efeito de base.

### Q2 — Quão persistente é a inflação, e o que a propaga?

**A persistência está em serviços, e o motor é o mercado de trabalho.** Serviços acumulam 5,46% em 12 meses até agosto (`inflc_agregados`), com hiato de +0,41% do potencial no 3T26 (`pm_hiato_produto` · edição de set/26), desocupação de 5,3% e rendimento habitual real +3,7% em 12 meses (`mt_pnad` · ago/26). É o canal que o modelo carrega pelo hiato (`I.IS.is2` 0,092) e pela média de quatro trimestres de serviços (`I.IS.is1b` 0,685): serviços demoram a ceder mesmo com o hiato fechando. Salário acima do que o hiato já carrega seria tempero (ii), mas com o hiato positivo e a renda real crescendo junto não separo os dois neste ciclo sem contar duas vezes; fica como argumento da cauda de alta em serviços, que não precifico.

**As expectativas estão acima da meta em todos os horizontes** (leitura, a conclusão é do agente de expectativas, IN-S9). A Focus de 12 meses está em 4,59%, +0,47 p.p. em três meses; a de 24 meses em 3,94%; as medianas para 2028 e 2029 em 3,80% e 3,51% (`expc_focus` e `expc_focus_periodo` · 02/10), contra a meta de 3,00% (`inflc_meta`). Âncora acima da meta é o que torna um choque mais persistente e o repasse maior (mapa, 2.3 e 2.5); é por isso que o tempero de alimentos (ficha (i)) entra na cauda de alta.

**Primeira rodada, por enquanto.** O que há de choque (energia, passagem aérea, in natura, cigarro) não espalhou: difusão no percentil 28 e núcleos abaixo do padrão sazonal (Q1). O canal de segunda rodada[^rodada] mais próximo é a indexação: a mediana do IGP-M de 2026 subiu de 4,34% para 5,27% em quatro semanas (`expc_focus_periodo` · 02/10), e aluguéis reajustam por ele; e os planos de saúde e medicamentos, regulados olhando a inflação passada (plano de saúde +0,42% em agosto, `inflc_decomposicao`). A leitura muda se a difusão passar de 60% com os núcleos acima da média sazonal.

### Q3 — Que pressões estão chegando ao IPCA, grupo a grupo?

**Monitorados: o petróleo, para cima, a partir do 4T26.** O Brent fechou 02/10 a US$ 135,51 (`comm_brent`), 18,0% acima do dia anterior e 61,8% acima da média de julho; a média de setembro foi US$ 114,16, 36,3% acima da de julho. A bomba não acompanhou: a gasolina caiu 3,5% de maio a agosto e subiu 0,30% no IPCA-15 de setembro, e o diesel caiu nos quatro últimos meses (−0,78% no IPCA-15 de setembro) (`inflc_decomposicao`). Em 2026 houve um episódio comparável: o Brent médio subiu 65,5% de fevereiro a abril e a gasolina 6,54% em março e abril (`comm_brent`, `inflc_decomposicao`). Um episódio não é regularidade, e a política de preços da Petrobras e os tributos estão fora do F (Faltou); por isso o reajuste é cauda e assimetria, e não central. Combustíveis de veículos pesam 5,45% e domésticos 1,39% (`inflc_decomposicao` · peso de set/26): +6% e +5% somam +0,40 p.p. ao IPCA.

**Monitorados: energia, direção incerta.** A oscilação de agosto e setembro sugere bandeira tarifária, mas o calendário de bandeiras não está no F (Faltou). O que se sabe é o efeito de base: os −2,39% e −2,41% de out/25 e dez/25 saem da janela, e a contribuição dos monitorados no modelo sobe de 1,09 p.p. para 1,37 p.p. no 4T26. Uma bandeira mais barata no fim do ano é o downside.

**Alimentação: para cima no 4T26 e no 1T27, por base e sazonalidade.** A alimentação acumulou −2,13% de junho a agosto, contra −0,03% na média da janela (2 de 10 anos abaixo) (`inflc_agregados` · ago/26), e virou no IPCA-15 de setembro (+0,38%). As commodities agrícolas em dólar estão estáveis: média de 200,53 no 3T26 contra 197,67 no 2T26 (`comm_icbr_usd`). O mercado vê alta: a Focus de alimentação no domicílio 12 meses à frente está em 6,95%, +1,92 p.p. em três meses (`expc_focus` · 02/10), bem acima da Focus do índice cheio (4,59%), o que o modelo não reproduz, porque ancora todos os grupos no cheio (mapa, 2.3). Não há série de clima ou safra no F (Faltou), então não sei se a Focus de alimentos lê clima; fica como argumento da cauda de alta em alimentos.

**Bens industriais: metais e câmbio, para cima, devagar.** Metais em dólar na média de 330,14 no 3T26 (`comm_icbr_usd`), +42,2% em 12 meses em setembro; a PTAX fechou 02/10 a R$ 5,2238, +1,9% em um mês (`cmb_ptax`); se a alta é persistente é do câmbio (IN-S1). Os bens industriais subiram 0,43% em agosto, com 12 meses de 2,95% (`inflc_agregados` · ago/26). O modelo leva a contribuição de 0,69 p.p. para 0,90 p.p. no 4T26 e a mantém perto de 0,8.

**Serviços: para baixo, devagar.** O hiato fecha no modelo (0,13% no 4T26, −0,51% no 1T28), e a contribuição de serviços cai de 2,14 p.p. para 1,69 p.p. no 1T28. O caminho do hiato é do agente de atividade (IN-S5).

### Q4 — O cenário para o IPCA

**Por que a central.** No cenário base as commodities em dólar ficam na média do 3T26 e as outras exógenas no padrão do simulador. O modelo faz quatro coisas, nesta ordem de tamanho:
1. **Efeito de base no 4T26.** O IPCA do trimestre projetado é 1,27%, contra 0,60% no 4T25 que sai (`inflc_agregados`, trimestral): é o que leva o 12 meses de 4,58% para 5,28%. Alimentação (0,66 → 0,96 p.p.) e monitorados (1,09 → 1,37 p.p.) respondem por quase todo o salto, porque são os dois grupos que tiveram o 4T25 mais baixo (−0,22% e −0,17%).
2. **Sazonalidade no 1T27**, quando o modelo põe 1,51% no trimestre (`I.IA.s1` 0,501, `I.IM.s1` 0,413) e o 12 meses ainda fica em 4,85%.
3. **A queda de 2T27 a 1T28 é lenta**, porque serviços têm persistência alta e o hiato fecha devagar: serviços tiram só 0,37 p.p. do 12 meses entre o 4T26 e o 1T28. A Selic cai de 13,43% no fim do 4T26 para 12,18% no fim do 1T28 no modelo, e a Focus do modelo vai de 4,16% para 3,52%.
4. **Câmbio e commodities quase não mexem**: a PTAX do modelo vai de 5,21 a 5,28, e o repasse estimado (`I.IA.ia3` 0,085; `I.II.ii4` 0,040) sobre isso é pequeno.

**Contra o Copom e a Focus.** A diferença está no fim do horizonte:

| | 4T26 | 1T27 | 2T27 | 3T27 | 4T27 | 1T28 |
|---|---|---|---|---|---|---|
| Modelo, base | 5,28 | 4,85 | 4,33 | 4,34 | 4,23 | 4,08 |
| Copom, R281, cenário de referência (`pm_copom_projecoes` · 24/09) | 5,2 | 4,9 | 4,5 | 4,5 | 3,9 | 3,2 |
| Modelo − Copom (p.p.) | +0,08 | −0,05 | −0,17 | −0,16 | +0,33 | +0,88 |

No 1T28, o horizonte relevante, o modelo fica 0,88 p.p. acima do Copom e 0,08 p.p. acima da mediana do QPC (4,00%, `expc_qpc` · 23/09); no 4T27, 0,07 p.p. abaixo da Focus de 2027 (4,30%, `expc_focus_periodo` · 02/10). O modelo, portanto, concorda com o mercado e não com o Copom. A projeção do Copom é condicional a caminhos da governança dele (juros da Focus, petróleo, bandeira), não uma previsão[^copom], e sem a IN-S4 não sei qual condicionante explica a diferença: **aguarda política monetária (IN-S4)**. Pelos números, a queda do Copom de 4,5% no 3T27 para 3,2% no 1T28 é rápida demais para a persistência que o modelo estima em serviços; os livres do Copom no 1T28 estão em 3,2%. Assumi que a diferença está nos livres, e é a primeira pergunta da IN-S4. No 4T26 o modelo fica 0,27 p.p. acima da Focus de 2026 (5,01%) e 0,34 p.p. acima do 12 meses de dezembro que as medianas do QPC dão (4,94%); quase toda essa diferença está no ponto de partida do modelo, e não no 4T26[^corte].

**Por que a distribuição.** O upside é mais provável que o downside em todos os trimestres porque a fonte principal de cauda, combustíveis, só tem um lado: o Brent subiu e a bomba caiu. A assimetria é máxima (+0,15) no 2T27 e no 3T27, quando um reajuste do 4T26 ainda está inteiro na janela, e cai a +0,06 no 1T28, quando ele sai. No 4T26 ela é pequena (+0,06) porque o modelo parte acima do que o mercado esperava no corte: o QPC e a Focus de 2026 ficam abaixo da faixa base, e isso pesa a cauda de baixa. As faixas crescem com o horizonte, e a probabilidade da faixa cai de 50% para 40%; a faixa de 90% do modelo, que só tem a incerteza dos pesos[^faixa], vai de ±0,2 p.p. no 4T26 a ±0,3 p.p. no 1T28, e o erro das equações é maior que isso.

Sinais que mudam a tese:
- Gasolina +3% ou mais num IPCA-15 de out/26 ou nov/26: a cauda de alta do 4T26 passa a mais provável que a faixa base.
- Brent abaixo de US$ 100 por quatro semanas sem reajuste na bomba: a assimetria do 1T27 ao 3T27 vai a zero.
- Serviços subjacentes acima de 0,45% em dois meses seguidos: a persistência que segura o 4T27 e o 1T28 é maior que a do modelo, e as caudas de alta desses trimestres ganham probabilidade.
- Difusão acima de 60% com o EX3 acima da média do mesmo mês: o choque começou a espalhar.

### Olhado, sem sinal

- Comercializáveis e não comercializáveis · 12 meses de 2,65% e 6,22% (`inflc_agregados` · set/26, último do F) · repetem a leitura de bens contra serviços · diriam algo se os comercializáveis acelerassem com o câmbio parado.
- Livres · 4,11% em 12 meses (`inflc_agregados` · ago/26) · sem sinal além dos grupos · diriam algo se divergissem dos núcleos.
- CAGED · estoque formal +1,9% em 12 meses (`mt_caged` · ago/26) · confirma o mercado de trabalho apertado, sem informação nova sobre preços · diria algo se virasse.
- Desocupação dessazonalizada do BC · 5,41% (`mt_desocupacao_retro` · jul/26) · repete a PNAD.
- PMS · ago/26 · divulgada depois do corte[^corte] · não usada.
- Projeção do Copom para administrados · 5,3% no 4T26 (`pm_copom_projecoes` · 24/09) · bate com o salto dos monitorados no modelo · diria algo com os condicionantes (IN-S4).

## 3. Premissas

### 3.1 Etapa 1 — o modelo

**Cenários.**
- Base: as commodities agrícolas e os metais em dólar ficam na média do 3T26; câmbio, Selic, hiato e expectativas como o modelo os resolve; as demais exógenas no padrão do simulador. O reajuste de combustíveis e a bandeira não estão no modelo (seção 3.2).
- Upside: o choque de petróleo contamina as commodities: custo de diesel e fertilizante e a ligação com biocombustíveis levam a agropecuária em dólar ao percentil 90 da variação histórica de um e de dois trimestres; os metais seguem a alta dos últimos 12 meses, também no percentil 90.
- Downside: o petróleo a US$ 135 desacelera a economia mundial e as commodities vão ao percentil 10 da variação histórica de um e de dois trimestres.

**Caminhos das exógenas** (média do trimestre, pontos do índice; tutela do externo, nível 1, e minha, nível 2):

| Exógena | Hoje (valor · tabela · data) | Cenário | 4T26 | 1T27 | 2T27 | 3T27 | 4T27 | 1T28 |
|---|---|---|---|---|---|---|---|---|
| `icbr_agr_usd`, IC-Br agropecuária em US$ | 200,53 · `comm_icbr_usd` · média do 3T26 | base | 200,53 | 200,53 | 200,53 | 200,53 | 200,53 | 200,53 |
| | | upside | 217,23 | 226,32 | 226,32 | 226,32 | 226,32 | 226,32 |
| | | downside | 188,66 | 184,01 | 184,01 | 184,01 | 184,01 | 184,01 |
| `icbr_met_usd`, IC-Br metal em US$ | 330,14 · `comm_icbr_usd` · média do 3T26 | base | 330,14 | 330,14 | 330,14 | 330,14 | 330,14 | 330,14 |
| | | upside | 373,35 | 408,51 | 408,51 | 408,51 | 408,51 | 408,51 |
| | | downside | 308,13 | 293,69 | 293,69 | 293,69 | 293,69 | 293,69 |

Motivo dos caminhos: na base, a média do 3T26 segurada, sem depender do mês de setembro; nas caudas, a média do 3T26 deslocada pelos percentis 90 e 10 da variação logarítmica das médias trimestrais desde 1998 (agropecuária +8,0% e +12,1%, −6,1% e −8,6%; metal +12,3% e +21,3%, −6,9% e −11,7%, para um e dois trimestres; `comm_icbr_usd`). Não há tendência na base porque não tenho fonte que a justifique; o caminho de quem tem o nível 1 (externo, IN-S7) prevalece no P.

**Saída do modelo:**

| Variável | Cenário | 4T26 | 1T27 | 2T27 | 3T27 | 4T27 | 1T28 |
|---|---|---|---|---|---|---|---|
| IPCA 12m (%) | base | 5,28 | 4,85 | 4,33 | 4,34 | 4,23 | 4,08 |
| | upside (caminhos + `I.IA.ia2` × 1,4) | 5,54 | 5,40 | 5,05 | 5,17 | 4,90 | 4,57 |
| | downside | 5,13 | 4,56 | 3,96 | 3,90 | 3,88 | 3,82 |
| IPCA no trimestre (%) | base | 1,27 | 1,51 | 0,92 | 0,58 | 1,16 | 1,36 |
| PTAX de fechamento (R$/US$) | base | 5,21 | 5,25 | 5,25 | 5,24 | 5,25 | 5,28 |
| | upside · downside | 5,22 · 5,20 | 5,27 · 5,23 | 5,28 · 5,24 | 5,27 · 5,22 | 5,29 · 5,23 | 5,32 · 5,26 |
| Selic de fechamento (% a.a.) | base | 13,43 | 13,11 | 12,83 | 12,58 | 12,37 | 12,18 |
| | upside · downside | 13,46 · 13,41 | 13,19 · 13,06 | 12,98 · 12,75 | 12,82 · 12,46 | 12,68 · 12,20 | 12,54 · 11,99 |
| Hiato (% do potencial) | base | 0,13 | −0,08 | −0,24 | −0,36 | −0,45 | −0,51 |
| Focus 12 meses do modelo (%) | base | 4,16 | 3,97 | 3,78 | 3,67 | 3,59 | 3,52 |

No upside, as commodities sobem a contribuição de alimentação a 1,26 p.p. no 1T27 (0,88 na base) e a de bens industriais a 1,24 p.p. no 4T27 (0,82 na base), porque os metais entram no trimestre e no seguinte; a Selic responde, 0,36 p.p. mais alta que a base no fim do 1T28. No downside, alimentação cai a 0,38 p.p. no 2T27 e bens industriais a 0,58 p.p. no 3T27.

### 3.2 Etapa 2 — o tempero qualitativo

**(i) `I.IA.ia2`, commodities agrícolas em US$ na alimentação — efeito mais forte que o estimado** · cenário upside
- Coeficiente: estimado 0,121, intervalo de 90% do posterior 0,050 a 0,190. Multiplicador: × 1,4 (0,170), dentro do intervalo, percentil 88.
- Efeito: IPCA 12m do upside, só caminhos → com o multiplicador: 5,48 → 5,54 no 4T26, 5,30 → 5,40 no 1T27, 4,93 → 5,05 no 2T27, 5,04 → 5,17 no 3T27.
- Por quê: um choque de commodities puxado por energia chega ao alimento também pelo custo (diesel, fertilizante), que o coeficiente médio da amostra não separa; e com a expectativa acima da meta em todos os horizontes o repasse tende a ser maior (mapa, 2.5).
- Onde entra: limite da cauda de alta.

**(ii) Petróleo e combustíveis — Brent e gasolina** · cenário upside, e assimetria da base
- Hoje: Brent US$ 135,51 (`comm_brent`, 02/10); gasolina −0,59% em agosto (`inflc_decomposicao`, ago/26) e +0,30% no IPCA-15 de setembro.
- Por que o modelo não vê: os monitorados só têm inércia e indexação ao IPCA (`I.IM.im1`, `I.IM.im2`); petróleo e política de preços não estão em nenhuma exógena.
- Efeito: +0,40 p.p. no IPCA 12m (combustíveis de veículos +6%, domésticos +5%) do 4T26 ao 3T27, enquanto o reajuste está na janela; +0,10 p.p. no 4T27 e no 1T28, de segunda rodada pela indexação (frete, IGP-M nos aluguéis), por julgamento.
- Onde entra: limite da cauda de alta; e, no cenário base, a assimetria positiva de todos os trimestres.

**(ii) Bandeira tarifária e alimentos in natura — energia elétrica residencial e tubérculos** · cenário downside
- Hoje: energia −7,63% em agosto e +7,42% no IPCA-15 de setembro; tomate +20,76% no IPCA-15 de setembro (`inflc_decomposicao`).
- Por que o modelo não vê: decisão regulatória e clima não estão no modelo.
- Efeito: −0,28 p.p. no IPCA 12m do 4T26 ao 3T27 (energia −5%, peso 3,98%: −0,20 p.p.; in natura: −0,08 p.p.), e zero depois.
- Onde entra: limite da cauda de baixa.

### 3.3 Da etapa 1 à tese

| Trimestre | Central (modelo, base) | Upside: modelo → com tempero | Downside: modelo → com tempero |
|---|---|---|---|
| 4T26 | 5,28 | 5,54 → 5,94 | 5,13 → 4,85 |
| 1T27 | 4,85 | 5,40 → 5,80 | 4,56 → 4,28 |
| 2T27 | 4,33 | 5,05 → 5,45 | 3,96 → 3,68 |
| 3T27 | 4,34 | 5,17 → 5,57 | 3,90 → 3,62 |
| 4T27 | 4,23 | 4,90 → 5,00 | 3,88 → 3,88 |
| 1T28 | 4,08 | 4,57 → 4,67 | 3,82 → 3,82 |

A faixa base fica entre a central e os pontos das caudas, de modo que cada cenário de cauda cai fora dela; o downside do 4T27 e do 1T28 só fica um pouco abaixo do limite, porque ali nenhum tempero (ii) age. As probabilidades da faixa caem com o horizonte, e a cauda de alta é maior que a de baixa pelo tempero de combustíveis, que só tem um lado.

## 4. Para os outros agentes

**Respostas às entradas fixas:**
- **IN-E1 (política monetária, repasse):** na PTAX do modelo, que vai de 5,18 a 5,28 até o 1T28, o repasse é pequeno. Pelo modelo, 1% de depreciação no trimestre põe 0,085 p.p. na alimentação no mesmo trimestre (`I.IA.ia3`) e 0,040 p.p. nos bens industriais no trimestre seguinte (`I.II.ii4`), propagados depois pela inércia de cada grupo. Combustíveis, energia e medicamentos não têm câmbio no modelo, e o canal mais rápido hoje é o petróleo: a gasolina subiu 6,54% em março e abril com o Brent médio +65,5% de fevereiro a abril, e não subiu com a alta de julho a setembro. Aguarda câmbio (IN-S1) sobre a persistência.
- **IN-E2 (câmbio):** a tese da seção 1; a cauda de alta vem de combustíveis e commodities, e põe mais inflação doméstica no diferencial.
- **IN-E3 (política monetária):** no 1T28, horizonte relevante, 4,08% (3,85 a 4,40, 40%), 0,88 p.p. acima do Copom. O choque é de primeira rodada (Q1, Q2); a persistência está em serviços.
- **IN-E4 (atividade):** alimentação e monitorados somam 2,32 p.p. dos 5,28% do 4T26 e 1,58 p.p. dos 4,08% do 1T28 (seção 1); a cauda de alta cai sobre os dois, que pesam mais no consumo de baixa renda.
- **IN-E5 (atividade):** serviços subjacentes rodam a 0,40% ao mês com o hiato de +0,41%; não medi neste ciclo o desvio contra o caminho da equação de serviços (Faltou).
- **IN-E6 (fiscal):** a tese da seção 1 e o IPCA do trimestre da seção 3.1 (1,27% no 4T26, 1,51% no 1T27).
- **IN-E7 (fiscal):** a central não assume nenhuma decisão de governo sobre preços; a cauda de alta assume reajuste de combustíveis no 4T26, e a de baixa, bandeira mais barata. Um corte de tributo sobre combustível tiraria da cauda de alta e iria para a de baixa (IN-S6).
- **IN-E8 (externo), em destaque:** a cauda de alta depende de energia (Brent, pelos combustíveis) no 4T26 a 3T27 e de agropecuária e metais em dólar no 4T26 e 1T27. O Brent é a premissa de que a tese mais depende.
- **IN-E9 (expectativas):** o salto de 4,58% para 5,28% no 4T26 é efeito de base (saem out/25 a dez/25, 0,09%, 0,18% e 0,33%) e choque de preço relativo, que não deveria mover os horizontes longos; o que persiste é serviços.
- **IN-E10 (expectativas):** para os próximos números, o risco contra as medianas do QPC (out 0,34%, nov 0,32%) é de alta, por combustíveis.

**Pedidos:**
- **IN-S1 (câmbio):** qual a PTAX de fechamento por trimestre de 4T26 a 1T28, e a alta de 1,9% em um mês até 02/10 é persistente? A cauda de alta de alimentos e bens depende disso.
- **IN-S2 (câmbio):** um choque de petróleo deste tamanho deprecia ou aprecia o real (o Brasil exporta petróleo)? A depreciação de cauda é global ou idiossincrática? Do sinal depende se câmbio e combustíveis somam ou se compensam na cauda de alta.
- **IN-S3 (política monetária):** qual a Selic por trimestre e por reunião nos dois próximos trimestres? O modelo leva a 13,43% no fim do 4T26.
- **IN-S4 (política monetária):** que petróleo, que bandeira e que câmbio condicionam a projeção da R281, e o que ela assume para os livres no 1T28 (3,2%)? É o que explica os 0,88 p.p. entre o modelo e o Copom no horizonte relevante.
- **IN-S5 (atividade):** qual o caminho do hiato até o 1T28, e a demanda de serviços sustenta serviços subjacentes a 0,40% ao mês? A persistência que segura a tese do 4T27 e do 1T28 depende disso.
- **IN-S6 (fiscal):** houve mudança de tributo sobre cigarro em ago/26 e set/26 (+19,59% e +14,00%)? Há medida sobre combustíveis em estudo diante do Brent a US$ 135, e com que data? As duas caudas do 4T26 ao 3T27 dependem disso.
- **IN-S7 (externo):** qual o caminho da agropecuária e dos metais em dólar por trimestre, base e caudas? Escrevi a média do 3T26 segurada e os percentis 90 e 10 históricos nas caudas.
- **IN-S8 (externo):** o Brent a US$ 135,51 em 02/10, +18% num pregão, é um evento de oferta? Qual o caminho por trimestre? O tamanho e a duração do tempero de combustíveis dependem disso.
- **IN-S9 (expectativas):** a Focus de 12 meses vai de 4,59% para onde, e a de 2029 em 3,51% conta como ancorada? O modelo leva a Focus de 12 meses a 3,52% no 1T28, bem abaixo da de hoje.
- **IN-S10 (expectativas):** por que a Focus de alimentação no domicílio subiu 1,92 p.p. em três meses, a 6,95%, com o cheio em 4,59%? Se for clima, a cauda de alta de alimentos ganha probabilidade.

## 5. Placar

Primeiro ciclo.

## 6. Sobre o modelo

| Fonte | O que sugere | Teste proposto | Por que importa para a tese deste ciclo |
|---|---|---|---|
| Mapa, 2.7 e "o que o modelo não carrega"; dados do ciclo (`comm_brent`, `inflc_decomposicao`) | Petróleo em reais (Brent × PTAX, ou o IC-Br energia em R$) na equação dos monitorados, no trimestre e com uma defasagem | Reestimar (I) monitorados de 2003 a 2026 com o regressor; muda a especificação se o coeficiente tiver o 90% do posterior longe de zero e o ajuste da equação melhorar | O maior risco do ciclo está num canal que o modelo não tem; com ele, o reajuste de combustíveis sairia da etapa 2 para a etapa 1 |
| Mapa, 2.2 (sinal errado de `I.IM.im2`, −0,209, 90%: −0,843 a 0,387) | Indexar os monitorados aos livres do trimestre anterior, e não ao cheio, que contém os próprios monitorados | Reestimar com os livres defasados e comparar o sinal e o ajuste | O salto dos monitorados no 4T26 é base e sazonalidade; a indexação, como está, não ajuda a ler a segunda rodada |
| Dados do ciclo (cigarro +19,59% em ago/26 nos bens industriais) | Uma dummy de medida tributária, ou excluir da série do grupo os itens de preço decidido por tributo | Medir o resíduo de (I) industriais nos trimestres com degrau de tributo | Com inércia de 0,537, um degrau de preço vira persistência no modelo |

[^corte]: O F deste ciclo corta pela data de referência, não pela de divulgação: traz o IPCA de set/26 (divulgado em 9/10) e a PMS de ago/26 (divulgada em outubro), que não existiam em 02/10. Este report não os usa. O Modelo Estrutural, porém, parte do 3T26 com o IPCA de 12 meses de setembro, 4,58%; com a mediana do QPC para setembro ele seria 4,30%. A central da seção 1 é a do modelo, como a regra manda, e carrega essa diferença.
[^nucleo]: Núcleo é uma medida que tira do índice os preços mais voláteis (por exclusão, como o EX3, ou cortando os extremos de cada mês, como as médias aparadas) para mostrar a tendência. Difusão é a fatia dos subitens que subiram no mês: alta com poucos itens subindo indica choque concentrado; alta com muitos, inflação espalhada.
[^pctl]: Percentil é a posição no histórico: 28 quer dizer que em 28% dos meses dos últimos dez anos a difusão foi menor que a de agosto.
[^rodada]: Primeira rodada é o efeito direto de um choque no preço atingido (a gasolina sobe porque o petróleo subiu). Segunda rodada é quando o choque passa a outros preços e salários, por contratos indexados ou por expectativas, e vira inflação persistente. Repasse (pass-through) é quanto de uma variação do câmbio ou de um custo chega ao preço final, e em quanto tempo.
[^copom]: O cenário de referência do Copom usa caminhos definidos pela própria governança (juros da Focus, petróleo, bandeira, câmbio); por isso é uma projeção condicional, e não a previsão do Copom.
[^faixa]: A faixa que o modelo imprime é a incerteza dos coeficientes estimados, não o erro de previsão; a distribuição da seção 1 é deste agente.
