# Report final — inflação · ciclo 2026-10-27

Dados até: 2026-10-27 (IPCA de set/26, IPCA-15 de out/26, PTAX de 26/10, Focus de 23/10; notícias até 27/10) · Horizontes: 4T26 a 1T28, a variável é o IPCA acumulado em 12 meses no fechamento do trimestre (mar, jun, set, dez)

## 1. Tese

| Variável | Trimestre | Central | Base: faixa · P | Upside: limite · P | Downside: limite · P | P(up) − P(down) |
|---|---|---|---|---|---|---|
| IPCA 12 meses, fim do trimestre (%) | 4T26 | 5,34 | 5,15 a 5,50 · 65% | acima de 5,50 · 22% | abaixo de 5,15 · 13% | +0,09 |
| | 1T27 | 4,95 | 4,70 a 5,25 · 58% | acima de 5,25 · 29% | abaixo de 4,70 · 13% | +0,16 |
| | 2T27 | 4,46 | 4,15 a 4,85 · 57% | acima de 4,85 · 30% | abaixo de 4,15 · 13% | +0,17 |
| | 3T27 | 4,48 | 4,20 a 4,90 · 57% | acima de 4,90 · 30% | abaixo de 4,20 · 13% | +0,17 |
| | 4T27 | 4,32 | 4,05 a 4,75 · 57% | acima de 4,75 · 29% | abaixo de 4,05 · 14% | +0,15 |
| | 1T28 | 4,14 | 3,85 a 4,55 · 58% | acima de 4,55 · 27% | abaixo de 3,85 · 15% | +0,12 |

**Decomposição da central** — contribuição de cada grupo ao IPCA de 12 meses no cenário base (P2), em p.p.; os quatro mais o resíduo somam a central:

| Trimestre | Serviços | Alimentação | Bens industriais | Monitorados | Resíduo |
|---|---|---|---|---|---|
| 3T26 (observado) | 2,14 | 0,66 | 0,69 | 1,09 | 0,00 |
| 4T26 | 2,06 | 1,02 | 0,90 | 1,37 | 0,00 |
| 1T27 | 1,96 | 0,96 | 0,83 | 1,21 | −0,01 |
| 2T27 | 1,96 | 0,67 | 0,83 | 1,01 | 0,00 |
| 3T27 | 1,86 | 0,70 | 0,88 | 1,04 | 0,00 |
| 4T27 | 1,77 | 0,63 | 0,91 | 1,01 | 0,00 |
| 1T28 | 1,69 | 0,58 | 0,89 | 0,98 | 0,00 |

A assimetria está em **monitorados** no começo do horizonte e na **âncora de expectativas** no fim. O upside viria de combustíveis (preço da Petrobras defasado, desoneração e subvenção com prazo), de hortaliças com chuva e, de 3T27 em diante, de uma Focus que cai mais devagar do que o modelo supõe. O downside viria de petróleo e commodities em queda chegando à bomba e à mesa, da desoneração da gasolina prorrogada e da reversão dos in natura. Serviços carregam a persistência da central, não a cauda.

- **Acima da faixa** se o prêmio de 26/10 se confirmar nas decisões fiscais de 2027 (CDS a ~205–210 p.b. e NTN-B a ~9%, o upside do agente fiscal; PTAX ~5,8 no modelo), se Hormuz seguir fechado (Brent a 129–130, agro e metais em alta, o upside do agente externo) e se a Petrobras repassar 5% à bomba entre novembro e janeiro. O modelo leva o 3T27 a 5,14 com o repasse a alimentos e bens industriais × 1,5; combustíveis, bandeira e hortaliças, fora do modelo, o levam a 5,41. É ruim para o Brasil: choque de câmbio e de oferta sobre uma inflação de tendência acima da meta.
- **Abaixo da faixa** se um arcabouço de 2027 que o mercado compre desfizer o prêmio (CDS de ~110 p.b., PTAX ~5,33 no 4T26), se Hormuz se normalizar (Brent a ~80 no 1T27) e se os in natura devolverem a alta no primeiro semestre. O modelo dá 4,00 para o 3T27, e com combustíveis mais baratos e a reversão dos in natura a cauda chega a 3,50. Por câmbio e oferta, é bom para o Brasil. Pela desoneração da gasolina prorrogada, é custo adiado: o imposto volta um dia, e a inflação com ele.

**A tese em uma frase:** o IPCA de 12 meses sobe a ~5,3% em dezembro porque sai da janela um 4T25 muito baixo, e cai a ~4,1% no 1T28, ~0,9 p.p. acima da projeção do Copom (3,2%), diferença que está em preços livres e serviços e não no câmbio; o risco é para cima, por combustíveis, hortaliças e expectativas.

## 2. Argumentação

### Q1 — O que explica a inflação corrente: quanto é choque e quanto é tendência?

**Setembro foi choque concentrado; a tendência está estável, mas acima da meta.** O IPCA de set/26 subiu 0,82% (`inflc_agregados` · set/26), contra 0,34% na média dos setembros dos dez anos anteriores; só um dos dez foi maior (padrão sazonal do F · set/26). Também veio 0,17 p.p. acima dos 0,65% que o Copom projetava para o mês (RPM de set/26, pela IN-S4 do agente de política monetária). As cinco maiores contribuições — energia elétrica residencial (+7,98%), tomate, passagem aérea, gasolina e batata-inglesa — somam ~0,58 p.p., ~70% do índice do mês (`inflc_decomposicao` · set/26). Os núcleos[^1] mostram o mês normal por baixo do choque: o EX3 subiu 0,26% contra 0,28% na média dos setembros, e a média aparada 0,31% contra 0,31% (padrão sazonal · set/26). A difusão[^2] de 54,9% ficou abaixo da média dos setembros de 2016–2025 (56,0%) (`inflc_agregados` · set/26).

| Grupo (BC) | Set/26 no mês (%) | Média dos setembros, 10a (%) | 12 meses (%) | 12 meses, 3 meses antes (%) |
|---|---|---|---|---|
| Serviços | 0,61 | 0,33 | 5,97 | 5,90 |
| Alimentação | 0,96 | 0,03 | 4,19 | 3,01 |
| Bens industriais | 0,17 | 0,23 | 3,07 | 2,76 |
| Monitorados | 1,59 | 0,65 | 4,14 | 5,52 |

(`inflc_agregados` e padrão sazonal · set/26)

**O IPCA-15 de outubro desloca o choque para alimentos, e a energia de outubro já está quase toda nele.** O IPCA-15 subiu 0,32% (`inflc_indice_geral` · out/26), contra 0,34% da QPC e 0,28% da mediana mensal da Focus para o IPCA de outubro (`expc_qpc` · R281; `expc_focus_periodo` · 23/10). Alimentação subiu 1,01%, com tomate +24,5%, cebola +13,6%, batata +11,0% e arroz +5,8%. A energia caiu 0,89% e a passagem aérea 9,2%; a gasolina subiu 0,92% e o diesel 3,7% (`inflc_decomposicao`, IPCA-15 · out/26). A ANEEL pôs a bandeira tarifária[^5] verde em outubro, pelas chuvas no Sul e no Sudeste (Agência Brasil · 25/09 · nível B). Em 2025–2026 a energia do IPCA-15 andou com a do IPCA do mesmo mês: −6,3% e −7,6% em agosto, +7,4% e +8,0% em setembro (`inflc_decomposicao`). Por isso não espero do IPCA cheio de outubro uma queda de energia muito maior que a do IPCA-15. Mas serviços subjacentes[^3] subiram 0,45% no IPCA-15 (recorte por subitem, `inflc_decomposicao` · out/26), acima dos 0,40% que a QPC espera para os serviços subjacentes do IPCA de outubro (p75 de 0,46). Se os serviços subjacentes do IPCA de outubro vierem acima de 0,46%, a leitura de "tendência estável" enfraquece; o limiar vale para os subjacentes, não para o índice cheio.

**O choque de alimentos é de horta, e continuou em outubro.** Os in natura acumulam +13,0% em 12 meses e subiram 5,1% em setembro, depois de −6,0% e −4,4% em julho e agosto (`inflc_decomposicao` · set/26, por classe do BC). O tomate subiu 38% no IPCA de setembro e 25% no IPCA-15 de outubro (`inflc_decomposicao`). No atacado, setembro teve tomate +48,9%, batata +32,9% e cebola +29,3%, com "as chuvas [dificultando] a colheita e os plantios" e risco de atraso no plantio da batata (CNN Brasil · 27/10 · nível B). Não há notícia do atacado de outubro.

**Que mês moveu o 12 meses.** O 12 meses foi de 4,22% em agosto para 4,58% em setembro porque entrou o 0,82% de set/26 e saiu o 0,48% de set/25 (`inflc_indice_geral`). No trimestre, o 3T26 (0,57%) substituiu um 3T25 de 0,63%, e o 12 meses do fechamento ficou quase parado: de 4,64% para 4,58% (F, IPCA por trimestre). Monitorados caíram de 5,52% para 4,14% em 12 meses pela saída da energia de set/25, que tinha subido 10,3% (`inflc_decomposicao`).

**Surpresas contra a expectativa de curto prazo (IN-E10).** Setembro veio 0,82% contra 0,56% da mediana da QPC (p75 0,60), e a diferença está toda em energia. Serviços subjacentes vieram 0,36% contra 0,30% (`expc_qpc` · R281; `inflc_decomposicao` · set/26). A surpresa de serviços é a que importa para a tendência.

### Q2 — Quão persistente é a inflação, e o que a propaga?

**A persistência está em serviços, e serviços estão firmes.** Serviços acumulam 5,97% em 12 meses. Os subjacentes estão em 5,32%, contra 5,00% três meses antes (`inflc_decomposicao` · set/26). No 3T26 o núcleo EX3 de serviços subiu 1,18%, contra 0,99% na média dos terceiros trimestres de 2016–2025 (`inflc_agregados`). Os não comercializáveis acumulam 6,22%, contra 2,65% dos comercializáveis (`inflc_agregados` · set/26). O agente de atividade põe a pressão de demanda nos serviços prestados às famílias, no percentil 100 dos últimos dez anos[^9] (+4,2% em 12 meses, `atv_pms` · ago/26), e no mercado de trabalho, não nos bens. Mas o mesmo agente põe o hiato fechando no 4T26 (0,13) e negativo do 1T27 em diante, com o risco para baixo em todos os trimestres. A demanda perde força, e o que segura serviços é inércia e salário (IN-E5, seção 4).

**Indexação formal: os planos de saúde desaceleram.** O plano de saúde sobe 0,42% ao mês desde julho de 2026, contra 0,49–0,50% de agosto de 2025 a maio de 2026 (`inflc_decomposicao`). O ritmo novo é compatível com o teto de 5,11% da ANS para o ciclo de 2026 (Agência Brasil · 29/05 · nível B) e fica abaixo dos 5,69% acumulados em 12 meses até setembro (F, monitorados item a item · set/26). Aluguel e taxas seguem em 6,32%, e transporte público em 4,91% (mesma tabela).

**Expectativas acima da meta, com o mercado à frente da pesquisa (IN-S9, leitura do agente de expectativas).** A Focus 12 meses estava em 4,53% e a de 24 meses em 3,87% em 23/10 (`expc_focus`). Por ano, a Focus dava 5,19% para 2026, 4,34% para 2027, 3,75% para 2028 e 3,50% para 2029 (`expc_focus_periodo` · 23/10), contra a meta de 3,00% (`inflc_meta`). O agente de expectativas lê os longos desancorados em nível e parados até 23/10, numa pesquisa anterior à eleição. Nas oito vezes em que a implícita de 2 anos saltou 0,60 p.p. ou mais numa semana desde 2006, a Focus do ano seguinte subiu em sete, com mediana de +0,54 p.p. em 45 dias úteis — e 26/10 foi um salto desses. As 16 pesquisas do 4T26 já feitas têm média de 4,52%, e o modelo põe a média do trimestre em 4,17%. Como a âncora dos quatro grupos é a Focus do trimestre anterior, isso pesa na inflação de 2027 em diante (Q4).

**Primeira ou segunda ordem?** O choque de setembro e outubro (energia, in natura, combustíveis) segue de primeira ordem[^4]: núcleos no padrão sazonal, difusão abaixo da média do mês. A segunda ordem está em risco por dois canais: expectativas acima da meta, com o mercado precificando mais inflação depois de 26/10, e serviços subjacentes acelerando no 12 meses (de 5,00% para 5,32% no trimestre). A segunda ordem se confirma se o EX3 de outubro e novembro vier acima da média dos mesmos meses e a Focus de 2027 passar de 4,6% nas pesquisas de depois de 26/10.

### Q3 — Que pressões estão chegando ao IPCA, grupo a grupo?

| Grupo | Pressão | Direção | Quando |
|---|---|---|---|
| Alimentação | hortaliças com chuva; câmbio a ~5,4–5,5; agro em US$ cedendo com o Brent | alta no 4T26–1T27; alívio do agro em 2027 | 4T26–4T27 |
| Monitorados | gasolina e diesel defasados; desoneração da gasolina por 30 dias e subvenção com base legal só em 2026; bandeira | alta (combustíveis, ao fim das medidas), baixa (enquanto duram; bandeira verde) | 4T26–1T27 |
| Bens industriais | câmbio, com um trimestre de defasagem; metais parados, com risco de queda | alta, pequena | 1T27–4T27 |
| Serviços | hiato negativo a partir do 1T27; salário real crescendo; planos de saúde desacelerando | desaceleração lenta | todo o horizonte |

- **Câmbio (IN-S1, IN-S2).** O agente de câmbio lê o salto de 26/10 (+9,2% num pregão, `cmb_ptax`) como idiossincrático e de patamar: "a reeleição levou o real a um patamar que não reverte sozinho". O evento é a reeleição do presidente em 25/10 (CNN Brasil · 25/10 · nível A). No P2 a PTAX fica em 5,43 no 4T26 e 5,53 no 1T28. Ela já devolveu parte do salto: o dólar fechou a R$ 5,350 em 27/10 (Poder360 · 27/10 · nível B). No modelo, essa depreciação chega a alimentos no mesmo trimestre e a bens industriais no seguinte, e já está na central (Q4).
- **Petróleo e combustíveis (fora do modelo).** O Brent fez média de 125 dólares em outubro até 20/10, ~30% acima da do 3T26 (`comm_brent`). Ele fechou a US$ 113,88 em 27/10, com "October has been the worst month for attacks on commercial shipping in the Strait of Hormuz" (Reuters/Investing.com · 27/10 · nível B). Para o agente externo, a queda desde 02/10 é prêmio saindo do preço com o fluxo ainda interrompido, e não reversão do choque. Ele dá ao Brent 114 no 4T26 e 91 no 1T28, com 25% para ficar em 129–130.

  Do lado das decisões, há quatro fatos e falas:
  - O governo zerou PIS/Pasep, Cofins e Cide da gasolina pela MP 1.395, de 09/10. A medida "vale por 30 dias, com possibilidade de revisão ou prorrogação" (Agência Brasil · 09/10 · nível B). O IPCA-15 de outubro, ainda com gasolina +0,92%, não mostra a medida chegando à bomba.
  - Desde abril vale uma subvenção de R$ 1,20 por litro ao diesel importado (Agência Brasil · 06/04 · nível B).
  - O ministro da Fazenda disse que a proposta deve ser manter a ajuda em 2027, e que a lei atual "vale apenas para 2026" (Poder360 · 23/10 · nível B).
  - A Abicom diz que os preços da Petrobras estão "muito defasados" e que o reajuste "terá que ser de maneira lenta e gradual" (CNN Brasil · 26/10 · nível B).

  O Copom supõe o fim das subvenções e desonerações no prazo legal (IN-S4), numa projeção anterior à MP 1.395. Gasolina, diesel e GNV pesam 5,45% no IPCA, e a gasolina sozinha 5,13%: cada 1% de gasolina na bomba vale ~0,05 p.p. (`inflc_decomposicao` · set/26). Combustíveis (veículos) acumulam −0,7% em três meses e +6,0% em 12 meses (F, monitorados · set/26): o Brent e o câmbio ainda não chegaram inteiros à bomba.
- **Energia elétrica (fora do modelo).** A bandeira de outubro é verde (Agência Brasil · 25/09 · nível B). O Copom supõe amarela em dezembro de 2026 e de 2027 (IN-S4). As bandeiras de novembro e dezembro não estavam publicadas, e decidem até ±0,10 p.p. do 4T26.
- **Commodities (IN-S7).** O agente externo passou a pôr o Brent no caminho do agro, pela ligação medida entre os dois. O agro em dólar vai de 204 no 4T26 a 197 no 1T28, contra 202 parado na rodada 1, e os metais de 332 a 326. Agora a cauda de alta das commodities tem mais chance que a de queda (25% contra 20%); nos metais, a de queda tem 30%, pela demanda chinesa por minério. O IC-Br metal em dólar acumula +42,2% em 12 meses (`comm_icbr_usd` · set/26), mas o EX3 de industriais desacelerou de 4,15% para 3,70% em 12 meses (`inflc_agregados` · set/26): os metais não estão chegando ao consumidor.
- **Base de comparação.** O 4T25 (0,60%) foi o mais baixo dos quartos trimestres de 2016 a 2025, salvo o de 2018 (0,39%; média de 1,49%). O 1T26 (1,92%) e o 2T26 (1,42%) ficaram acima da média dos mesmos trimestres, 1,71% e 1,08% (F, IPCA por trimestre; padrão de 2016–2025). Por isso o 12 meses sobe no 4T26 mesmo com o trimestre abaixo da média sazonal, e cai no 1T27 e no 2T27 sem desinflação.

### Q4 — O cenário para o IPCA

**Por que a central.** A central é a do P2: 5,34% em dezembro e 4,14% no 1T28. O 4T26 sobe por efeito-base[^6]: o modelo põe o trimestre em 1,33%, contra o 0,60% do 4T25 que sai da janela.
- Alimentação sobe de 0,66 para 1,02 p.p. de contribuição (~6,6% em 12 meses), pela sazonalidade do quarto trimestre, pela inércia do choque in natura e pelo câmbio.
- Monitorados sobem de 1,09 para 1,37 p.p., porque sai da janela a queda de energia do 4T25 (−0,17% no trimestre, F por trimestre).

Depois, o 12 meses cai a 4,46% no 2T27, com a saída do 1T26 e do 2T26. Serviços carregam a queda e a persistência ao mesmo tempo. A contribuição deles vai de 2,14 para 1,69 p.p. (~4,7% em 12 meses no 1T28), porque o hiato vai de 0,41% a −0,52% e a Selic média de 14,06% a 12,18%. A queda é lenta porque a equação de serviços lê a média dos últimos quatro trimestres com peso 0,685 (`I.IS.is1b`) e o hiato com 0,092 (`I.IS.is2`). Monitorados ficam em ~1,0 p.p. (~3,8%). Essa é a equação mais fraca do modelo (indexação com sinal trocado, mapa 2.2), e não leio a central dela como informação sobre combustíveis e energia.

**O que o P2 mudou contra a rodada 2.** A central subiu 0,02 p.p. no 4T26 e caiu 0,01 a 0,06 de 1T27 a 1T28, e quase toda a mudança é o agro. Com o Brent no caminho do agro, o índice fica mais alto no 4T26 (203,9 contra 202) e mais baixo de 2027 em diante (até 197,4). O bloco de commodities soma +0,02 p.p. no 4T26 e tira 0,03 a 0,06 de 2T27 a 1T28. O CDS mais baixo no fim do horizonte tira 0,01 no 1T28. A NTN-B mais alta (7,72 a 7,95, contra 7,70 a 7,80) move a Selic, mas não o IPCA dentro do horizonte (G sobre o modelo, por bloco).

**Contra o Copom e a Focus.**

| | 4T26 | 1T27 | 2T27 | 3T27 | 4T27 | 1T28 |
|---|---|---|---|---|---|---|
| Modelo, central do P2 | 5,34 | 4,95 | 4,46 | 4,48 | 4,32 | 4,14 |
| Copom, cenário de referência (R281) | 5,2 | 4,9 | 4,5 | 4,5 | 3,9 | 3,2 |
| Diferença (p.p.) | +0,14 | +0,05 | −0,04 | −0,02 | +0,42 | +0,94 |
| Focus por ano (23/10) | 5,19 | | | | 4,34 | |

(`pm_copom_projecoes` · 24/09; `expc_focus_periodo` · 23/10)

Até o 3T27 o modelo e o Copom estão juntos, embora o câmbio do P2 fique 5–7% acima do condicionante do Copom (5,15). O motivo é que o Copom carrega o que o modelo não vê: Brent de 90 dólares com pico no 4T26, bandeira amarela e o fim das subvenções a combustíveis no prazo legal (IN-S4). Os administrados do Copom, 5,3% no 4T26 e 4,5% no 1T27, estão perto dos do modelo (~5,3% e ~4,7%).

A diferença abre no 4T27 e chega a 0,94 p.p. no 1T28, e não é o câmbio: com a PTAX do cenário de baixa do fiscal e do câmbio (5,28 no 4T26), o modelo ainda dá 4,09% no 1T28. A diferença está nos preços livres, ~4,3% no modelo contra 3,2% do Copom, que explicam 0,79 dos 0,94 p.p.; os monitorados (~3,8% contra 3,2%) explicam 0,14. Dentro dos livres, o que separa as duas projeções são serviços a ~4,7% no 1T28 e uma âncora que cai devagar: a Focus 12 meses do modelo ainda está em 3,55% no 1T28.

A projeção do Copom é condicional aos caminhos que a governança dele fixa; ela não é a previsão dele (mapa 2.8). Com o câmbio de ~5,4–5,5 e o Brent do agente externo, os condicionantes do Copom ficariam piores, e não melhores. Já a desoneração e a subvenção, se mantidas, deixam os administrados do Copom de 2027 abaixo do que ele projetou. Contra a Focus, que é anterior a 26/10, o modelo está perto em 2026 (5,34 contra 5,19) e em 2027 (4,32 contra 4,34).

**Por que a faixa e a assimetria para cima.** O câmbio de 26/10 está na central desde a rodada 2. Ficam quatro forças de alta, todas fora da central:
1. **Expectativas.** A (E) põe a Focus do 4T26 em 4,17%, contra 4,52% de média nas pesquisas já feitas no trimestre. Passei pelo modelo o tempero que o agente de expectativas aplica no base dele (`E.e1` × 1,2, decisão dele, não cenário meu). Com ele, a Focus vai a 4,33% no 4T26 e 3,88% no 1T28, e o IPCA de 12 meses sobe +0,10 p.p. no 3T27 e +0,19 no 1T28, mesmo com a Selic 0,5 p.p. mais alta. A história recente pesa a favor: depois de saltos da implícita como o de 26/10, a pesquisa seguiu o preço em sete de oito vezes. É a força que mais pesa no horizonte relevante.
2. **Combustíveis.** O preço da Petrobras está defasado (Abicom, nível B). A desoneração da gasolina tem 30 dias de prazo, e a subvenção tem base legal só até dezembro (Durigan, nível B). O Brent é de 114 no 4T26 no caminho do agente externo, com 25% de ficar em 129–130.
3. **Hortaliças.** Há chuva no atacado e no plantio (CNN Brasil, nível B), e o tomate ainda subia 25% no IPCA-15 de outubro. A Conab espera o El Niño "de forma severa neste segundo semestre de 2026 e início de 2027" (Agência Brasil · 15/10 · nível B): é risco de oferta para o primeiro semestre.
4. **Câmbio e commodities, nas caudas.** O agente de câmbio dá 31% a uma PTAX acima de 5,60 no 4T26, contra 22% abaixo de 5,30. O externo dá à alta das commodities mais chance que à queda.

Para baixo pesam:
- a desoneração da gasolina chegando à bomba e prorrogada;
- o Brent devolvendo o pico de outubro;
- a bandeira verde;
- a reversão dos in natura no primeiro semestre;
- a queda dos metais (30% no externo);
- um hiato com risco de baixa em todos os trimestres (agente de atividade).

Frente à rodada 2, a assimetria de 1T27 a 1T28 sobe 1 a 2 p.p.: a cauda das commodities virou para cima e a evidência de expectativas ficou mais forte, mais do que compensando o câmbio, cuja assimetria o agente de câmbio reduziu. A faixa do 4T26 é a mais estreita porque outubro está quase medido pelo IPCA-15. Do 1T27 ao 3T27 ela abre com combustíveis e câmbio. No 1T28 a assimetria cai porque o choque de combustíveis sai da janela, mas fica positiva pela âncora.

### Olhado, sem sinal

- Núcleo EX0 · 4,85% em 12 meses (`inflc_agregados` · set/26) · conta a mesma história do EX3 e da média aparada · diria algo se se descolasse dos outros núcleos.
- Núcleo de dupla ponderação · 4,06% em 12 meses (`inflc_agregados` · set/26) · estável, contra 4,01% três meses antes · diria algo com movimento acima de 0,2 p.p. num trimestre.
- Taxa de informalidade · 37,5% (`mt_pnad` · ago/26) · estável · diria algo se mudasse a leitura do mercado de trabalho do agente de atividade.
- Veículo próprio (monitorado) · −0,06% em 12 meses (F, monitorados · set/26) · sem movimento · diria algo com mudança de tributo sobre veículos.
- Etanol · 0,60% de peso, +3,2% em setembro, classificado em bens industriais (`inflc_decomposicao` · set/26) · acompanha a gasolina e não entra no tempero de combustíveis · diria algo se divergisse dela.
- IC-Br energia em reais · +10,4% no mês (`comm_icbr` · set/26) · repete o Brent · diria algo se divergisse do Brent.
- PMS informação e comunicação · +4,8% em 12 meses (`atv_pms` · ago/26) · comunicação pesa pouco e subiu 2,8% em 12 meses no IPCA · diria algo com reajuste de telecom.

## 3. Premissas

### 3.1 Etapa 1 — o modelo

**Cenários.**
- Base: os caminhos do P2, cada um do principal da exógena. No modelo, a PTAX fica em 5,43 no 4T26 e 5,53 no 1T28, com o salto de 26/10 mantido.
- Upside: as decisões fiscais de 2027 confirmam o prêmio de 26/10, e Hormuz segue fechado. Entram os caminhos de cauda de alta do agente fiscal (CDS e NTN-B) e do agente de câmbio (volatilidade), e os de alta do agente externo para o IC-Br e para os grupos agro e metal.
- Downside: um arcabouço de 2027 que o mercado compre desfaz o prêmio, e Hormuz se normaliza. Entram as caudas de baixa dos mesmos agentes.

**Caminhos das exógenas.** No base, todas as do P2. Nas caudas mudam só as seis abaixo; dólar contra emergentes, S&P 500, juros e inflação americanos e a meta ficam no P2, como no câmbio do agente de câmbio.

| Exógena | Hoje (valor · tabela · data) | Cenário | 4T26 | 1T27 | 2T27 | 3T27 | 4T27 | 1T28 |
|---|---|---|---|---|---|---|---|---|
| `fiscal` — CDS 5 anos, fechamento (p.b.) · principal: fiscal | 137 · `cmb_risco_pais` · 26/10 (agente fiscal) | base (P2) | 140 | 142 | 139 | 135 | 130 | 125 |
| | | upside | 170 | 205 | 210 | 205 | 198 | 190 |
| | | downside | 122 | 115 | 112 | 110 | 108 | 106 |
| `rr_10a` — NTN-B 10 anos, média (% a.a.) · principal: fiscal | 8,05 · `br_interest_rate` · 26/10 (agente fiscal) | base (P2) | 7,72 | 7,95 | 7,90 | 7,80 | 7,75 | 7,70 |
| | | upside | 8,15 | 8,90 | 9,10 | 9,10 | 9,00 | 8,90 |
| | | downside | 7,36 | 7,30 | 7,15 | 7,05 | 7,00 | 6,95 |
| `vol` — volatilidade implícita do real (% a.a.) · principal: câmbio | sem dado no F; 12,19 no 2T26 (modelo) | base (P2) | 17,0 | 15,5 | 14,5 | 14,0 | 13,5 | 13,5 |
| | | upside | 24,0 | 21,0 | 18,0 | 16,0 | 15,0 | 15,0 |
| | | downside | 13,0 | 12,5 | 12,0 | 12,0 | 12,0 | 12,0 |
| `icbr_usd` — IC-Br em US$, último mês · principal: externo | 205,7 · `comm_icbr_usd` · set/26 | base (P2) | 206,2 | 202,6 | 201,0 | 199,9 | 199,0 | 198,3 |
| | | upside | 216,3 | 217,1 | 217,1 | 216,8 | 215,7 | 215,3 |
| | | downside | 197,3 | 188,2 | 184,3 | 183,2 | 183,5 | 183,8 |
| `icbr_agr_usd` — IC-Br agropecuária em US$, média · principal: externo | 200,5 · `comm_icbr_usd` · média 3T26 | base (P2) | 203,9 | 200,9 | 199,3 | 198,4 | 197,8 | 197,4 |
| | | upside | 208,1 | 211,1 | 211,9 | 212,8 | 212,4 | 211,7 |
| | | downside | 200,6 | 192,0 | 188,4 | 186,6 | 186,4 | 186,8 |
| `icbr_met_usd` — IC-Br metal em US$, média · principal: externo | 330,1 · `comm_icbr_usd` · média 3T26 | base (P2) | 331,7 | 330,0 | 330,0 | 328,7 | 327,3 | 325,7 |
| | | upside | 346,0 | 358,0 | 362,0 | 362,0 | 362,0 | 362,0 |
| | | downside | 320,0 | 298,3 | 283,3 | 277,0 | 275,0 | 275,0 |

Motivo das caudas: são os caminhos de cauda que os principais escreveram na rodada 2, combinados na direção que é ruim (upside) ou boa (downside) para a inflação. Não são tese minha sobre essas variáveis e ficam só neste report[^7].

**Saída do modelo.**

| Variável | Cenário | 4T26 | 1T27 | 2T27 | 3T27 | 4T27 | 1T28 |
|---|---|---|---|---|---|---|---|
| IPCA 12m (%) | base | 5,34 | 4,95 | 4,46 | 4,48 | 4,32 | 4,14 |
| | upside | 5,41 | 5,18 | 4,83 | 4,96 | 4,79 | 4,51 |
| | downside | 5,28 | 4,75 | 4,14 | 4,05 | 3,87 | 3,76 |
| IPCA no trimestre (%) | base | 1,33 | 1,55 | 0,94 | 0,59 | 1,17 | 1,37 |
| PTAX, fechamento (R$/US$) | base | 5,43 | 5,52 | 5,52 | 5,50 | 5,51 | 5,53 |
| | upside | 5,58 | 5,79 | 5,79 | 5,74 | 5,74 | 5,74 |
| | downside | 5,33 | 5,43 | 5,46 | 5,46 | 5,48 | 5,51 |
| Selic, média (% a.a.) | base | 13,48 | 13,37 | 13,04 | 12,69 | 12,43 | 12,18 |
| Hiato (% do potencial) | base | 0,13 | −0,08 | −0,24 | −0,36 | −0,45 | −0,52 |
| Focus 12m, média (%) | base | 4,17 | 4,00 | 3,82 | 3,71 | 3,63 | 3,55 |

A faixa de 90% do posterior[^8] da central vai de 5,15–5,53 no 4T26 a 3,82–4,50 no 1T28, e não inclui o erro das equações. No downside a PTAX sobe ao longo do horizonte porque, no modelo, as commodities em queda enfraquecem o real.

**Só o câmbio, para a IN-E1** (CDS, NTN-B e volatilidade de cada cauda, commodities no base, contra o base):

| Cenário de câmbio | | 4T26 | 1T27 | 2T27 | 3T27 | 4T27 | 1T28 |
|---|---|---|---|---|---|---|---|
| Upside: PTAX contra o base | % | +3,9 | +6,4 | +6,6 | +6,0 | +5,7 | +5,5 |
| | IPCA 12m (p.p.) | +0,03 | +0,09 | +0,16 | +0,20 | +0,20 | +0,15 |
| | alimentação (p.p.) | +0,03 | +0,07 | +0,10 | +0,11 | +0,08 | +0,03 |
| | bens industriais (p.p.) | 0,00 | +0,02 | +0,06 | +0,10 | +0,12 | +0,12 |
| | com repasse × 1,5 (p.p.) | +0,05 | +0,19 | +0,32 | +0,40 | +0,40 | +0,32 |
| Downside: PTAX contra o base | % | −2,7 | −3,0 | −2,8 | −2,4 | −2,0 | −1,7 |
| | IPCA 12m (p.p.) | −0,02 | −0,06 | −0,08 | −0,10 | −0,08 | −0,05 |

No modelo, serviços e monitorados recebem no máximo +0,01 p.p. de um câmbio 4–7% mais fraco.

### 3.2 Etapa 2 — o tempero

**(i) Repasse cambial a alimentos e bens industriais — mais forte que o estimado** · cenário upside
- Coeficientes: `I.IA.ia3` estimado 0,085, intervalo de 90% 0,020 a 0,153; `I.II.ii4` 0,040, intervalo 0,016 a 0,064. Multiplicador × 1,5 nos dois (0,127 e 0,060), dentro do intervalo; o de bens industriais fica perto da borda.
- Efeito: o upside passa de 5,41 para 5,44 no 4T26, de 5,18 para 5,27 no 1T27, de 4,96 para 5,14 no 3T27 e de 4,79 para 4,97 no 4T27.
- Por quê: o repasse é maior quando a depreciação vem de prêmio doméstico, é vista como persistente e encontra inflação e expectativas acima da meta (mapa 2.5). O agente de câmbio confirmou as duas primeiras condições (idiossincrática, de patamar), e o agente de expectativas lê a implícita de 2 a 5 anos +1,2 p.p. em 26/10. Um salto de 9,2% num pregão é maior que a variação trimestral típica da amostra, e o modelo é linear.
- Onde entra: limite e probabilidade do upside.

**(i) Repasse cambial mais fraco e hiato mais forte em serviços** · cenário downside
- Coeficientes: `I.IA.ia3` e `I.II.ii4` × 0,7 (0,059 e 0,028, dentro do intervalo); `I.IS.is2` estimado 0,092, intervalo 0,042 a 0,142, × 1,5 (0,138, perto da borda).
- Efeito: o downside passa de 4,75 para 4,74 no 1T27, de 4,05 para 4,00 no 3T27 e de 3,76 para 3,68 no 1T28.
- Por quê: uma apreciação que só desfaz um salto é absorvida em margem. E o hiato negativo chega a serviços com o volume total do setor parado (+0,6% em 12 meses, `atv_pms` · ago/26) e com o 3T26 em contração no dado mensal (agente de atividade). O agente de atividade não pede multiplicador para `I.IS.is2`, porque a dúvida sobre o hiato vale para os dois lados. Por isso o × 1,5 fica só na cauda, não no base.
- Onde entra: limite do downside.

**(ii) Combustíveis — Brent, câmbio e a política de preços da Petrobras** · upside e downside
- Hoje: Brent a US$ 113,88 (Reuters/Investing.com · 27/10 · nível B; `comm_brent`: 115,22 em 20/10). O caminho do agente externo vai de 114 no 4T26 a 91 no 1T28, com alta a 129–130 e queda a 78. No IPCA-15 de outubro, o diesel subiu 3,7% e a gasolina 0,9% (`inflc_decomposicao`). A Abicom descreve os preços como "muito defasados" (CNN Brasil · 26/10 · nível B).
- Por que o modelo não vê: petróleo e câmbio não entram na equação de monitorados (mapa 2.7).
- Efeito no upside: gasolina e diesel +5% na bomba, metade em nov–dez/26 e metade em jan/27. É o repasse "lento e gradual" que a Abicom descreve, somado ao fim da desoneração e da subvenção. Soma +0,14 p.p. no 4T26, +0,27 do 1T27 ao 3T27 e +0,14 no 4T27 (peso de 5,45%, `inflc_decomposicao` · set/26).
- Efeito no downside: −3% no 2T27, quando o Brent da cauda de queda já está em 79 e fecha a defasagem. Tira 0,16 p.p. do 2T27 ao 1T28.
- Onde entra: limites das duas caudas. O upside pesa mais na assimetria porque a defasagem já existe e o downside depende de o Brent cair primeiro.

**(ii) Desoneração da gasolina (MP 1.395)** · downside
- Hoje: PIS/Pasep, Cofins e Cide da gasolina zerados desde 09/10, por 30 dias, "com possibilidade de revisão ou prorrogação" (Agência Brasil · 09/10 · nível B). A gasolina subiu 0,92% no IPCA-15 de outubro (`inflc_decomposicao`): a medida ainda não aparece na bomba.
- Por que o modelo não vê: tributo sobre preço, fora de qualquer exógena.
- Efeito: suponho a desoneração prorrogada e chegando à bomba como gasolina 2% mais barata no 4T26. Isso tira 0,10 p.p. do 4T26 ao 3T27, enquanto o mês da queda está na janela (cada 1% de gasolina vale ~0,05 p.p., peso de 5,13%). O tamanho do tributo zerado por litro não está no F nem nas notícias (Faltou): os 2% são hipótese de tamanho, e a sensibilidade por ponto está aqui para quem tiver o número.
- No upside, a volta do tributo ao fim do prazo é parte dos +5% de combustíveis.
- Onde entra: limite do downside. É custo adiado: se a desoneração cai, ela volta como alta no trimestre em que acaba.

**(ii) Bandeira tarifária de energia** · upside e downside
- Hoje: a energia subiu 7,98% em setembro e caiu 0,89% no IPCA-15 de outubro (`inflc_decomposicao`); a bandeira de outubro é verde (Agência Brasil · 25/09 · nível B).
- Por que o modelo não vê: decisão regulatória, fora de qualquer exógena.
- Efeito: um patamar de bandeira acima ou abaixo em novembro e dezembro move a conta em ±2,5% no 4T26, o que vale ±0,10 p.p. no 4T26 (peso de 3,98%), devolvido no 1T27.
- Onde entra: limites do 4T26.

**(ii) Clima e safra de hortaliças — alimentos in natura** · upside e downside
- Hoje: os in natura subiram 5,1% em setembro e acumulam +13,0% em 12 meses. No IPCA-15 de outubro, o tomate subiu 25% e a batata 11% (`inflc_decomposicao`). A chuva atrapalha colheita e plantio (CNN Brasil · 27/10 · nível B).
- Por que o modelo não vê: clima e safra doméstica não estão no modelo, e o IC-Br agro não carrega hortaliças.
- Efeito no upside: in natura 5% acima do que o modelo dá no 4T26, devolvido no 2T27. Soma +0,12 p.p. no 4T26 e no 1T27 (peso de 2,38%).
- Efeito no downside: −5% no 1T27 e −5% no 2T27. Tira 0,12 p.p. no 1T27, 0,24 do 2T27 ao 4T27 e 0,12 no 1T28.
- Onde entra: limites das duas caudas. Não há série de clima no F (Faltou).

**(ii) Salários além do hiato em serviços** · upside
- Hoje: rendimento real habitual +3,7% em 12 meses, desocupação de 5,3% (`mt_pnad` · ago/26).
- Por que o modelo não vê: salários não estão no modelo. Só conta a parte que o hiato não carrega, para não dobrar o efeito.
- Efeito: +0,10 p.p. no 4T27 e no 1T28, quando o hiato do modelo já está negativo e o salário real ainda não terá ajustado.
- Onde entra: limite do upside nos dois últimos trimestres. É por aqui, e só por aqui, que a leitura de um hiato medido baixo demais chega ao IPCA (ver IN-E5). O desconto de −0,15 que o agente de atividade aplica na partida do hiato valeria ~0,02 p.p. no IPCA de 12 meses; nenhuma das duas leituras move a tese.

**(ii) Expectativas acima da (E) e por componente** · assimetria do cenário base
- Hoje: média de 4,52% nas pesquisas do 4T26, contra 4,17% da (E). A Focus de serviços para 2028 está em 4,65%, +0,15 p.p. em quatro semanas, com o IPCA de 2028 parado. A alimentação no domicílio é vista como choque datado, 4,00% em 2028 (`expc_focus`, `expc_focus_periodo` · 23/10, leitura do agente de expectativas).
- Por que entra aqui: a (E) é do agente de expectativas e o multiplicador dela é dele; a âncora por componente não está no modelo.
- Efeito: não movo a central nem as caudas. O efeito medido do tempero do agente de expectativas (+0,10 p.p. no 3T27 e +0,19 no 1T28) pesa na probabilidade do upside de 3T27 em diante.

### 3.3 Da etapa 1 à tese

| Trimestre | Central (P2) | Upside: modelo → (i) → com (ii) | Downside: modelo → (i) → com (ii) |
|---|---|---|---|
| 4T26 | 5,34 | 5,41 → 5,44 → 5,80 | 5,28 → 5,28 → 5,08 |
| 1T27 | 4,95 | 5,18 → 5,27 → 5,66 | 4,75 → 4,74 → 4,52 |
| 2T27 | 4,46 | 4,83 → 4,97 → 5,24 | 4,14 → 4,10 → 3,60 |
| 3T27 | 4,48 | 4,96 → 5,14 → 5,41 | 4,05 → 4,00 → 3,50 |
| 4T27 | 4,32 | 4,79 → 4,97 → 5,21 | 3,87 → 3,80 → 3,40 |
| 1T28 | 4,14 | 4,51 → 4,65 → 4,75 | 3,76 → 3,68 → 3,40 |

A faixa base vai da central até um pouco antes de cada cauda com tempero. Ela é mais larga para cima porque as forças de alta (combustíveis defasados e medidas com prazo, hortaliças, expectativas) já estão em curso, e as de baixa dependem de reversão ou de prorrogação. O upside fica fora da faixa com 22–30% de probabilidade e o downside com 13–15%.

### 3.4 O que mudou desde a rodada 2

| O quê | Antes → depois | Por quê | Causa |
|---|---|---|---|
| Central | 5,32 / 4,96 / 4,48 / 4,52 / 4,38 / 4,19 → 5,34 / 4,95 / 4,46 / 4,48 / 4,32 / 4,14 | o agro do externo passou a seguir o Brent (mais alto no 4T26, mais baixo em 2027); CDS mais baixo no fim; NTN-B mais alta (sem efeito no IPCA) | P2 (com a moderação) |
| Faixas | sem mudança | a central andou no máximo 0,06 p.p.; as caudas com tempero continuam fora das faixas | — |
| P(up) / P(down) | 22/13, 28/14, 29/14, 29/14, 28/15, 26/16 → 22/13, 29/13, 30/13, 30/13, 29/14, 27/15 | a alta das commodities passou a ter mais chance que a queda (25% contra 20%); a evidência de que a pesquisa segue o preço depois de saltos como o de 26/10; a assimetria do câmbio caiu, o que segura o 4T26 | reports do externo, de expectativas e do câmbio (r2) |
| Caudas da etapa 1 | caudas do câmbio (r1) e do externo (r1) → caudas do fiscal (CDS, NTN-B), do câmbio (vol) e do externo (r2) | os principais revisaram as caudas na rodada 2; CDS e NTN-B são do fiscal | reports r2 |
| Desoneração da gasolina | não havia → downside de −0,10 p.p. do 4T26 ao 3T27, por hipótese de tamanho | MP 1.395 zerou os tributos da gasolina por 30 dias, prorrogáveis | notícia (Agência Brasil · 09/10 · nível B) |
| Tempero de combustíveis no upside | mesmo tamanho (+5%) | agora inclui a volta da desoneração e da subvenção ao fim dos prazos | notícias (Agência Brasil · 09/10 e 06/04 · nível B) |
| Multiplicadores | sem mudança | — | — |

## 4. Para os outros agentes

**Respostas às entradas fixas**

- **IN-E1 (pass-through), em destaque: o câmbio de 26/10 é de patamar, segundo o agente de câmbio.** O caminho do P2 (PTAX de 5,43 a 5,53) já põe na central uma depreciação de ~4–5% contra o padrão do simulador. Para uma PTAX 4–7% acima disso (as caudas de alta do fiscal e do câmbio), o modelo soma ao IPCA 12m +0,09 p.p. no 1T27 e +0,20 no 3T27. Primeiro vêm alimentos, no mesmo trimestre (`I.IA.ia3`; +0,07 p.p. no 1T27), depois bens industriais, com um trimestre de defasagem (`I.II.ii4`; +0,12 no 4T27). Serviços e monitorados não recebem nada. Com repasse × 1,5, a soma vai a +0,19 e +0,40. Fora do modelo, a depreciação chega a gasolina e diesel pela paridade da Petrobras, com defasagem de política: 5% na bomba somam +0,27 p.p. por quatro trimestres. Chega também a medicamentos no reajuste anual e, pela indexação, a contratos no ano seguinte. Tudo isso é primeira ordem. A segunda ordem apareceria nas expectativas (a Focus do modelo sobe +0,06 p.p. no 4T27 nesse cenário) e em serviços.
- **IN-E2 (câmbio, S5 dele):** a tese da seção 1. A cauda de alta vem de combustíveis, hortaliças e expectativas, e o câmbio entra nela pelo repasse. A defasagem do diesel e a reação da Petrobras estão no tempero de combustíveis (+0,27 p.p. no upside), e não na central que você usa na perna de PPC.
- **IN-E3 (política monetária, S7 e S8 dele):** 4,14% no 1T28, faixa de 3,85–4,55, upside de 27% contra 15%.
  - Entre o modelo e o Copom, fico com o modelo. A diferença de 0,94 p.p. está nos preços livres (0,79 p.p.) e não no câmbio: com a PTAX mais baixa do downside, o modelo dá 4,09%.
  - O repasse de uma PTAX de 5,44–5,50 está na IN-E1.
  - Ao S8: o subsídio e a desoneração não estão na central, porque o modelo não vê combustíveis. Se mantidos em 2027, eles abaixam o IPCA medido. O tamanho do que escondem não está no F nem nas notícias: cada 1% de gasolina na bomba vale ~0,05 p.p., e a minha hipótese de 2% vale 0,10. Voltam como alta quando acabam.
  - O choque corrente é de primeira ordem. A segunda ordem está em risco por serviços subjacentes (5,32% e subindo) e por expectativas (o mercado à frente da pesquisa).
- **IN-E4 (atividade, S-IN1):** alimentação contribui 1,02 p.p. no 4T26 e cai a 0,58–0,70 de 2T27 em diante; monitorados contribuem 1,37 p.p. no 4T26 e ~1,0 depois. A cauda de alta está nesses dois grupos, os que mais pesam no consumo de baixa renda. Com a depreciação persistindo além do P2, alimentação sobe +0,07 a +0,11 p.p. de 1T27 a 3T27 (IN-E1).
- **IN-E5 (atividade, S-IN2):** serviços estão acima do que o hiato explica. No modelo, o nível de serviços vem da média dos quatro trimestres anteriores (`I.IS.is1b` 0,685), e não do hiato (`I.IS.is2` 0,092). Os subjacentes aceleraram de 5,00% para 5,32% no trimestre enquanto o hiato do BC caía. Isso cabe num hiato medido baixo demais ou em salário além do hiato, e o dado do ciclo não separa os dois. Fica como nota, sem tempero sobre o hiato (que é seu): no IPCA, entra só pelo tempero de salários (+0,10 p.p. no 4T27–1T28). A divergência com a sua leitura de partida (−0,15) segue aberta como leitura, sem efeito na tese (~0,02 p.p.).
- **IN-E6 (fiscal, FS-IN1):** a tese da seção 1. IPCA no trimestre (P2): 1,33% no 4T26, 1,55% no 1T27, 0,94% no 2T27, 0,59% no 3T27, 1,17% no 4T27 e 1,37% no 1T28.
- **IN-E7 (fiscal, FS-IN2):** a central (o modelo) não supõe decisão de governo sobre preços; ela não vê combustíveis. Na direção, não divergimos: a sua base supõe a subvenção mantida em 2027 (nível B), e a minha leitura também, porque o fim das medidas está só no meu upside, que é onde fica a premissa do Copom (fim no prazo legal). A diferença é de onde a decisão mora: você a põe na premissa da base; eu não a ponho na central, porque o modelo não vê combustíveis, nem lhe dou tamanho, porque nenhum de nós tem o valor por litro. O que decide é a renovação em lei ou MP, com valor, até dezembro: se ela vier, o fim sai do meu upside; se não vier, o fim em janeiro entra como alta no 1T27, dentro dos +5% de combustíveis do upside. A desoneração da gasolina prorrogada está no meu downside, como custo adiado.
- **IN-E8 (externo, XS7):**
  - O agro mais baixo em 2027 entra na central e não muda a tese de alimentação: tira 0,04 a 0,06 p.p. de 4T27 a 1T28. A pressão de alimentos é de hortaliças e câmbio, fora da cesta.
  - O Brent acima da premissa do Copom entra no tempero de combustíveis com o seu caminho: +5% na bomba no upside (Brent de 129–130) e −3% no downside (Brent de 79 no 2T27). No base, a defasagem que já existe não move a central, mas pesa na assimetria.
  - No modelo, +10% no agro somam +0,19 a +0,25 p.p. ao IPCA 12m do 4T26 ao 3T27, e +10% nos metais, +0,04 a +0,19, crescendo até o 3T27.
- **IN-E9 (expectativas, XS5):** a central sobe a 5,34% em dezembro por efeito-base, não por aceleração. Saem da janela o 1T26 (1,92%) e o 2T26 (1,42%), o que derruba o 12 meses no 1T27 e no 2T27. A parte do câmbio de 26/10 que o P2 carrega já está na central; um câmbio 4–7% mais fraco passaria +0,09 p.p. ao 1T27 e +0,16 ao 2T27. A Focus de serviços para 2028 em 4,65% tem sustentação: o modelo dá ~4,7% a serviços no 1T28, com os subjacentes a 5,32% hoje.
- **IN-E10 (expectativas, XS6):** setembro veio 0,82% contra 0,56% da QPC, por energia. O IPCA-15 de outubro veio 0,32%, contra 0,28% da Focus mensal e 0,34% da QPC para o IPCA do mês. A energia de outubro já está quase toda no IPCA-15. Para o IPCA de outubro, o risco de alta vem de alimentos; o de baixa, da desoneração da gasolina, se chegar à bomba nas semanas que o IPCA-15 não cobriu.

**Pedidos para o próximo ciclo**

- **IN-S1 e IN-S2 (câmbio):** a PTAX fechou a ~5,35 em 27/10. Segue o patamar de 5,43 no 4T26 e a probabilidade de 31% acima de 5,60? Quando os pares latinos tiverem dado depois de 26/10, a comparação confirma o idiossincrático? Decide o × 1,5 do repasse.
- **IN-S3 (política monetária):** a decisão de 04/11 e o câmbio de partida da projeção de 09/12. Decidem quanto da diferença de 0,94 p.p. contra o Copom fecha na próxima projeção.
- **IN-S4 (política monetária):** a próxima projeção já inclui a MP 1.395 e a subvenção de 2027? Quanto dos 4,5% de administrados no 1T27 é o fim das medidas? Decide a comparação de monitorados.
- **IN-S5 (atividade):** o IBC-Br de setembro (meados de novembro). Decide o multiplicador de `I.IS.is2` no downside.
- **IN-S6 (fiscal):** o valor por litro dos tributos zerados pela MP 1.395, se ela foi prorrogada, e o valor e o prazo da subvenção ao diesel em 2027. Decide o tamanho da desoneração no downside (hoje é hipótese) e o degrau de combustíveis quando as medidas acabarem.
- **IN-S7 e IN-S8 (externo):** o caminho do agro incorpora o El Niño que a Conab espera para o início de 2027? E a OPEP+ de 01/11? Decidem a cauda de alimentos no 1S27 e o tempero de combustíveis.
- **IN-S9 e IN-S10 (expectativas):** a Focus de 30/10, a primeira depois de 26/10, em 12 meses, 2027 e serviços 2029. Decide a assimetria de 3T27 em diante.

**Ao agente web**

- Bandeira tarifária da ANEEL para novembro e dezembro de 2026. Tese: limites do 4T26 (sem resposta nas duas rodadas).
- MP 1.395: prorrogação depois de 08/11 e o valor por litro dos tributos zerados; reajustes da Petrobras em gasolina e diesel depois de 25/10. Tese: tempero de combustíveis e desoneração.
- Preços de tomate, batata e cebola no atacado em outubro e a previsão de chuva para novembro–dezembro nas regiões produtoras. Tese: in natura.
- Reajustes de ônibus urbano para janeiro de 2027 nas capitais. Tese: inércia dos monitorados no 1T27 (sem resposta nas duas rodadas).

**Como subordinado**

- `icbr_agr_usd` · principal: externo
  - Insumos: a pressão doméstica em alimentos é de hortaliças, fora da cesta do IC-Br: in natura +13,0% em 12 meses, semi-elaborados +6,1%, industrializados +0,3% (`inflc_decomposicao` · set/26). O IC-Br agro em reais subiu 3,3% do 2T26 para o 3T26, quase todo câmbio (`comm_icbr`). A Conab espera safra de grãos acima de 367 milhões de toneladas, +1,4%, apesar de um El Niño severo no 2S26 e no início de 2027 (Agência Brasil · 15/10 · nível B). Sensibilidade no P2: +10% no caminho somam +0,19 a +0,25 p.p. ao IPCA 12m do 4T26 ao 3T27.
  - Argumento: aceito o caminho novo (203,9 → 197,4). A ligação com o Brent responde à pergunta que fiz na rodada 1, e os preços domésticos não pedem outra coisa. O risco que eu acrescentaria ao principal é o El Niño no 1S27, mais na cauda de alta do que no base.
  - Caminho de referência: nenhum.
  - Resposta do principal (r2): aceitou o Brent no agro e mudou o caminho; disse que in natura e arroz não estão na cesta. Divergência fechada.
- `icbr_met_usd` · principal: externo
  - Insumos: com o IC-Br metal em US$ +42,2% em 12 meses, o EX3 de industriais desacelerou de 4,15% para 3,70% e bens industriais acumulam 3,07% (`inflc_agregados` · set/26). O minério está na mínima de dois anos, e "is likely to stay soft through November", segundo Mengtian Jiang, da Horizon Insights (Yahoo Finance/Bloomberg · 27/10 · nível B). Sensibilidade no P2: +10% somam +0,04 a +0,19 p.p., crescendo até o 3T27.
  - Argumento: nada a acrescentar ao caminho base. A cauda de queda com 30% é coerente com o que leio nos preços de bens industriais.
  - Caminho de referência: nenhum.
  - Resposta do principal (r2): manteve o caminho e subiu a cauda de queda para 30%, no sentido da minha leitura. Sem divergência.

## 5. Placar

Primeiro ciclo: não há report final anterior com trimestre fechado. O 4T26 será conferido com o IPCA de 12 meses de dezembro de 2026, publicado no começo de janeiro de 2027.

## 6. Sobre o modelo

Propostas só; o modelo não muda neste ciclo.

| Fonte | O que sugere | Teste proposto | Por que importa para a tese deste ciclo |
|---|---|---|---|
| Mapa 2.7; Brent +30% em um mês; diesel +3,7% no IPCA-15; MP 1.395; o agente externo propõe o mesmo | Petróleo em reais (Brent × PTAX, ou o IC-Br energia em R$) na equação de monitorados, com defasagem de um trimestre, uma variável de tributo sobre combustível, e o IPCA livre no lugar do cheio na indexação (`I.IM.im2`) | Monitorados trimestral, 2003–2026, com e sem a variação do Brent em reais defasada e com o IPCA livre defasado. Muda se o coeficiente do petróleo for positivo com intervalo fora de zero e o sinal da indexação se acertar | O choque de petróleo, câmbio e tributo do ciclo não aparece em monitorados. Ele vive todo no tempero, e é a maior cauda da tese |
| Mapa 2.6; in natura +13,0% em 12 meses com o IC-Br agro em US$ de lado | Separar in natura do resto de alimentação, ou um termo de clima na equação de alimentação | Alimentação trimestral dividida em in natura e restante, 2006–2026. Muda se o ajuste da parte sem in natura melhorar e `I.IA.ia2` subir | O choque de alimentos atual não é commodity, e o modelo o trata só como inércia |
| Focus do modelo de 4,17 no 4T26 contra 4,52 de média nas pesquisas já feitas; energia do IPCA-15 andando com a do IPCA do mesmo mês; o agente de expectativas propõe o mesmo para a (E) | Usar no trimestre em curso o dado que já saiu dentro dele (Focus semanal, IPCA-15, PTAX diária), em vez de partir só do último trimestre fechado | Erro do primeiro trimestre projetado com e sem esse dado parcial, nas projeções fora da amostra de 2015–2026 | A âncora do 4T26 está abaixo do que a aritmética das pesquisas permite, e o erro passa à inflação de 2027 pela âncora dos quatro grupos |
| Mapa 2.3; Focus por componente (serviços 2028 +0,15 com o IPCA de 2028 parado) | Âncora por componente em vez da Focus do IPCA cheio | Equação (I) com a Focus de cada componente como âncora, 2021–2026 (amostra curta). Muda se o ajuste de serviços e alimentação melhorar | O mercado põe mais inflação em serviços e menos em alimentação a partir de 2028 do que a âncora comum permite |

[^1]: Núcleo é uma medida que tira ou suaviza os itens mais voláteis do IPCA para mostrar a tendência. O EX3 exclui alimentos e monitorados, entre outros; a média aparada corta os extremos da distribuição de variações do mês.
[^2]: Difusão é a fatia dos subitens do IPCA que subiram no mês. Uma alta de inflação com difusão baixa vem de poucos itens.
[^3]: Serviços subjacentes são os serviços sem os itens mais voláteis (passagem aérea, alimentação fora de casa e outros), os mais ligados a salário e demanda doméstica. O número do IPCA-15 foi refeito pelos subitens com a marca de subjacente da classificação do BC; a QPC pergunta pelo IPCA do mês, então a comparação é aproximada.
[^4]: Efeito de primeira ordem é a alta do próprio item que sofreu o choque (a energia, o tomate). O de segunda ordem é a alta se espalhar para outros preços e salários, por indexação ou por expectativa; é a esse que o Banco Central reage. Pass-through é a fatia de uma variação do câmbio que chega aos preços ao consumidor.
[^5]: A bandeira tarifária é um adicional na conta de luz definido pela ANEEL todo mês, mais caro quando a geração custa mais (reservatório baixo, térmicas ligadas). Por isso a energia sobe e devolve de um mês para o outro.
[^6]: O IPCA de 12 meses muda tanto pelo mês que entra quanto pelo que sai da janela. Quando sai um trimestre muito baixo, o 12 meses sobe mesmo que a inflação do trimestre novo seja normal: é o efeito-base.
[^7]: A central é a do P2, rodado com os caminhos base dos principais depois da moderação da rodada 2. Os caminhos de cauda acima são dos reports r2 e não entram no P. Os números da seção 2 que vêm de outros agentes (hiato, percentis do PMS, média das pesquisas do 4T26, episódios de salto da implícita, probabilidades de câmbio e commodities) são leituras deles, citadas como tais.
[^8]: A faixa do posterior mostra só a incerteza sobre os pesos estimados do modelo, não a incerteza da previsão; a faixa da tese, na seção 1, é a do agente.
[^9]: Percentil é a posição do último valor no histórico, de 0 (o menor já visto) a 100 (o maior). Percentil 100 em dez anos quer dizer o maior valor da série nesse período.
