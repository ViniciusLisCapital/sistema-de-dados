# Report — inflação · ciclo 2026-10-27 · rodada 2

Dados até: 2026-10-27 (IPCA de set/26, IPCA-15 de out/26, PTAX de 26/10, Focus de 23/10) · Horizontes: 4T26 a 1T28, a variável é o IPCA acumulado em 12 meses no fechamento do trimestre (mar, jun, set, dez)

## 1. Tese

| Variável | Trimestre | Central | Base: faixa · P | Upside: limite · P | Downside: limite · P | P(up) − P(down) |
|---|---|---|---|---|---|---|
| IPCA 12 meses, fim do trimestre (%) | 4T26 | 5,32 | 5,15 a 5,50 · 65% | acima de 5,50 · 22% | abaixo de 5,15 · 13% | +0,09 |
| | 1T27 | 4,96 | 4,70 a 5,25 · 58% | acima de 5,25 · 28% | abaixo de 4,70 · 14% | +0,14 |
| | 2T27 | 4,48 | 4,15 a 4,85 · 57% | acima de 4,85 · 29% | abaixo de 4,15 · 14% | +0,15 |
| | 3T27 | 4,52 | 4,20 a 4,90 · 57% | acima de 4,90 · 29% | abaixo de 4,20 · 14% | +0,15 |
| | 4T27 | 4,38 | 4,05 a 4,75 · 57% | acima de 4,75 · 28% | abaixo de 4,05 · 15% | +0,13 |
| | 1T28 | 4,19 | 3,85 a 4,55 · 58% | acima de 4,55 · 26% | abaixo de 3,85 · 16% | +0,10 |

**Decomposição da central** — contribuição de cada grupo ao IPCA de 12 meses no cenário base (P1), em p.p.; os quatro mais o resíduo somam a central:

| Trimestre | Serviços | Alimentação | Bens industriais | Monitorados | Resíduo |
|---|---|---|---|---|---|
| 3T26 (observado) | 2,14 | 0,66 | 0,69 | 1,09 | 0,00 |
| 4T26 | 2,06 | 1,00 | 0,90 | 1,37 | 0,00 |
| 1T27 | 1,96 | 0,96 | 0,83 | 1,21 | −0,01 |
| 2T27 | 1,96 | 0,69 | 0,83 | 1,01 | 0,00 |
| 3T27 | 1,86 | 0,74 | 0,88 | 1,04 | 0,00 |
| 4T27 | 1,77 | 0,69 | 0,91 | 1,01 | 0,00 |
| 1T28 | 1,69 | 0,64 | 0,89 | 0,97 | 0,00 |

A assimetria está em **monitorados e alimentação** no começo do horizonte e na **âncora de expectativas** no fim: o upside viria de combustíveis (a Petrobras repassando um preço defasado), de hortaliças com chuva e, de 3T27 em diante, de uma Focus que cai mais devagar do que o modelo supõe; o downside, de commodities e petróleo em queda chegando à bomba e da reversão dos in natura. Serviços carregam a persistência da central, não a cauda.

- **Acima da faixa** se o choque de 26/10 se aprofundar (PTAX ~5,75–5,85, o upside do agente de câmbio), as commodities subirem com o petróleo (o cenário de alta do agente externo) e a Petrobras repassar 5% à bomba entre novembro e janeiro: o modelo leva o 3T27 a 5,20 com o repasse a alimentos e bens industriais × 1,5, e combustíveis, bandeira e hortaliças fora do modelo o levam a 5,47. Ruim para o Brasil: choque de câmbio e de oferta sobre uma inflação de tendência acima da meta.
- **Abaixo da faixa** se o prêmio de 26/10 se desfizer (PTAX ~5,24 no 4T26), as commodities caírem (Brent a ~80 no 1T27) e os in natura devolverem a alta no primeiro semestre: 3,95 no modelo para o 3T27, 3,55 com combustíveis 3% mais baratos e a reversão dos in natura. Bom para o Brasil se vier de câmbio e oferta; se o corte de combustível vier de subsídio ou imposto, é custo adiado.

**A tese em uma frase:** o IPCA de 12 meses sobe a ~5,3% em dezembro porque sai da janela um 4T25 muito baixo, e cai a ~4,2% no 1T28 — um ponto acima da projeção do Copom (3,2%), quase todo em preços livres e serviços, e não no câmbio —; o risco segue para cima, agora menos pelo câmbio (que a central já carrega) e mais por combustíveis, hortaliças e expectativas.

## 2. Argumentação

### Q1 — O que explica a inflação corrente: quanto é choque e quanto é tendência?

**Setembro foi choque concentrado; a tendência está estável, mas acima da meta.** O IPCA de set/26 subiu 0,82% (`inflc_agregados` · set/26) contra 0,34% na média dos setembros dos dez anos anteriores, e só um dos dez foi maior (padrão sazonal do F · set/26); veio 0,17 p.p. acima dos 0,65% que o Copom projetava para o mês (RPM de set/26, pela IN-S4 do agente de política monetária). As cinco maiores contribuições — energia elétrica residencial (+7,98%, 0,318 p.p.), tomate, passagem aérea, gasolina e batata-inglesa — somam 0,58 p.p., ~70% do índice do mês (`inflc_decomposicao` · set/26). Os núcleos[^1] mostram o mês normal por baixo do choque: o EX3 subiu 0,26% contra 0,28% na média dos setembros, e a média aparada 0,31% contra 0,31% (padrão sazonal · set/26). A difusão[^2] de 54,9% ficou abaixo da média dos setembros de 2016–2025 (56,0%) (`inflc_agregados` · set/26).

| Grupo (BC) | Set/26 no mês (%) | Média dos setembros, 10a (%) | 12 meses (%) | 12 meses, 3 meses antes (%) |
|---|---|---|---|---|
| Serviços | 0,61 | 0,33 | 5,97 | 5,90 |
| Alimentação | 0,96 | 0,03 | 4,19 | 3,01 |
| Bens industriais | 0,17 | 0,23 | 3,07 | 2,76 |
| Monitorados | 1,59 | 0,65 | 4,14 | 5,52 |

(`inflc_agregados` e padrão sazonal · set/26)

**O IPCA-15 de outubro desloca o choque para alimentos, e a energia de outubro já está quase toda nele.** O IPCA-15 subiu 0,32% (`inflc_indice_geral` · out/26), contra 0,34% da QPC e 0,28% da mediana mensal da Focus para o IPCA de outubro (`expc_qpc` · R281; `expc_focus_periodo` · 23/10). Alimentação subiu 1,01%, com tomate +24,5%, arroz +5,8%, cebola +13,6% e batata +11,0%; a energia devolveu 0,89% e a passagem aérea caiu 9,24%; gasolina +0,92% e diesel +3,70% (`inflc_decomposicao`, IPCA-15 · out/26). A ANEEL pôs a bandeira tarifária[^5] verde em outubro pelas chuvas no Sul e no Sudeste (Agência Brasil · 25/09 · nível B), e em 2025–2026 a energia do IPCA-15 andou com a do IPCA do mesmo mês: −6,25% e −7,63% em agosto, +7,42% e +7,98% em setembro (`inflc_decomposicao` · 2025–2026). Por isso não espero do IPCA cheio de outubro uma devolução de energia muito maior que a do IPCA-15. Mas serviços subjacentes[^3] subiram 0,45% no IPCA-15 (recorte por subitem, `inflc_decomposicao` · out/26), acima dos 0,40% da QPC (p75 de 0,46): se o IPCA de outubro confirmar acima de 0,46, a leitura de "tendência estável" enfraquece.

**O choque de alimentos é de horta, e ele continuou em outubro.** Os in natura acumulam +13,0% em 12 meses e +5,10% em setembro, depois de −5,98% e −4,38% em julho e agosto (`inflc_decomposicao` · set/26, por classe do BC). O tomate subiu 37,76% no IPCA de setembro e 24,54% no IPCA-15 de outubro; a batata, 24,07% e 10,96% (`inflc_decomposicao`). No atacado, setembro teve tomate +48,9%, batata +32,88% e cebola +29,31%, com "as chuvas [dificultando] a colheita e os plantios" e risco de atraso no plantio da batata (CNN Brasil · 27/10 · nível B). A reversão que eu punha no 4T26 na rodada 1 fica mais tarde (seção 3.2).

**Que mês moveu o 12 meses.** O 12 meses foi de 4,22% em agosto para 4,58% em setembro porque entrou o 0,82% de set/26 e saiu o 0,48% de set/25 (`inflc_indice_geral`). No trimestre, o 3T26 (0,57%) substituiu um 3T25 de 0,63%, e o 12 meses do fechamento ficou quase parado (4,64% → 4,58%) (F, IPCA por trimestre). Monitorados caíram de 5,52% para 4,14% em 12 meses pela saída da energia de set/25 (+10,31%, `inflc_decomposicao`).

**Surpresas contra a expectativa de curto prazo (IN-E10).** Setembro veio 0,82% contra 0,56% da mediana da QPC (p75 0,60), a diferença toda em energia; serviços subjacentes vieram 0,36% contra 0,30% (`expc_qpc` · R281; `inflc_decomposicao` · set/26). A surpresa de serviços é a que importa para a tendência.

### Q2 — Quão persistente é a inflação, e o que a propaga?

**A persistência está em serviços, e serviços estão firmes.** Serviços acumulam 5,97% em 12 meses e os subjacentes 5,32%, contra 5,00% três meses antes (`inflc_decomposicao` · set/26); no 3T26 o núcleo EX3 de serviços subiu 1,18%, contra 0,99% na média dos terceiros trimestres de 2016–2025 (`inflc_agregados`). Os não comercializáveis acumulam 6,22% contra 2,65% dos comercializáveis (`inflc_agregados` · set/26). O agente de atividade põe a pressão de demanda nos serviços prestados às famílias, no percentil 100 dos últimos dez anos[^9] (+4,2% em 12 meses, `atv_pms` · ago/26), e não nos bens; e lê a desocupação dessazonalizada (5,41% em julho) 1,89 p.p. abaixo da NAIRU de curto prazo do QPC (`mt_desocupacao_retro`, `expc_qpc`). Mas o mesmo agente põe o hiato fechando no 4T26 (0,13) e negativo do 1T27 em diante, com risco de baixa no começo, porque o IBC-Br de julho e agosto aponta contração no 3T26: a demanda perde força, e o que segura serviços é inércia e salário (IN-E5, seção 4).

**Indexação formal: os planos de saúde desaceleram.** O plano de saúde sobe 0,42% ao mês desde julho de 2026, contra 0,49–0,50% de agosto de 2025 a maio de 2026 (`inflc_decomposicao`), compatível com o teto de 5,11% da ANS para o ciclo de 2026 (Agência Brasil · 29/05 · nível B); um ritmo abaixo dos 5,69% acumulados em 12 meses até setembro (F, monitorados item a item · set/26), que portanto tendem a cair ao longo do ciclo. Aluguel e taxas seguem em 6,32%, transporte público em 4,91% (mesma tabela).

**Expectativas acima da meta, e o mercado já à frente da pesquisa (leitura do agente de expectativas, IN-S9).** A Focus 12 meses estava em 4,53% e a de 24 meses em 3,87% em 23/10 (`expc_focus`); por ano, 5,19% para 2026, 4,34% para 2027, 3,75% para 2028 e 3,50% para 2029 (`expc_focus_periodo` · 23/10), contra meta de 3,00% (`inflc_meta`). O agente de expectativas lê os longos desancorados em nível e parados, e a implícita de 5 anos +1,20 p.p. num pregão em 26/10, com a pesquisa ainda anterior ao choque. As 16 pesquisas do 4T26 já feitas têm média de 4,52%, e o modelo põe a média do trimestre em 4,17% — para fechar ali, as restantes teriam de cair quase meio ponto (G do agente de expectativas sobre `expc_focus`). Como a âncora dos quatro grupos é a Focus do trimestre anterior, isso pesa na inflação de 2027 em diante (Q4).

**Primeira ou segunda ordem?** O choque de setembro–outubro (energia, in natura, combustíveis) segue de primeira ordem[^4]: núcleos no padrão sazonal, difusão abaixo da média do mês. A segunda ordem está em risco por dois canais — expectativas acima da meta, com o mercado precificando mais inflação depois de 26/10, e serviços subjacentes acelerando no 12 meses (de 5,00% para 5,32% no trimestre). O que a confirmaria é o EX3 de outubro e novembro acima da média dos mesmos meses do histórico e a Focus de 2027 subindo nas pesquisas de depois de 26/10.

### Q3 — Que pressões estão chegando ao IPCA, grupo a grupo?

| Grupo | Pressão | Direção | Quando |
|---|---|---|---|
| Alimentação | hortaliças com chuva (IPCA-15 de out, atacado de set); câmbio de 5,44 no 4T26 | alta | 4T26–1T27 |
| Monitorados | gasolina e diesel defasados contra Brent e câmbio; fim legal da subvenção em 2026; bandeira | alta (combustíveis), baixa (energia, bandeira verde) | 4T26–1T27 |
| Bens industriais | câmbio, com um trimestre de defasagem; metais parados | alta, pequena | 1T27–4T27 |
| Serviços | hiato negativo a partir do 1T27; salário real crescendo; planos de saúde desacelerando | desaceleração lenta | todo o horizonte |

- **Câmbio (IN-S1, IN-S2, agente de câmbio).** O agente de câmbio lê o salto de 26/10 (+9,19% num pregão, `cmb_ptax`) como idiossincrático e, em boa parte, persistente, e põe a PTAX em 5,35–5,39 no horizonte; o evento é a reeleição do presidente em 25/10 (CNN Brasil · 25/10 · nível A). No P1, com os caminhos de todos os principais, a PTAX fica em 5,44 no 4T26 e 5,57 no 1T28. No modelo, essa depreciação chega a alimentos no mesmo trimestre e a bens industriais no seguinte, e já está na central (Q4).
- **Petróleo e combustíveis (fora do modelo).** O Brent fez média de 125 dólares em outubro até 20/10, ~30% acima da média do 3T26, e estava em 115,22 em 20/10 (`comm_brent`), com o mercado cobrando "a significant risk premium" pelos ataques a petroleiros em Hormuz (OilPrice.com · 19/10 · nível B). O caminho do agente externo é de devolução gradual: 114 no 4T26, 105 no 1T27, 91 no 1T28. A Abicom diz que "os preços da Petrobras estão muito defasados" e que o reajuste, depois da eleição, "terá que ser de maneira lenta e gradual" (CNN Brasil · 26/10 · nível B). O ministro da Fazenda, Dario Durigan, disse que "deve ser a proposta do presidente" manter a subvenção aos combustíveis em 2027 se o Brent seguir alto, e que a lei que a financia "vale apenas para 2026" (Poder360 · 23/10 · nível B); o presidente falou em "subsidiar o óleo diesel e a gasolina" (Poder360 · 24/10 · nível B). O Copom supõe o fim das subvenções no prazo legal (IN-S4). Gasolina, diesel e GNV pesam 5,45% no IPCA, a gasolina sozinha 5,13% (`inflc_decomposicao` · set/26); combustíveis (veículos) acumulam −0,71% em três meses e 5,95% em 12 meses (F, monitorados · set/26): a alta do Brent e do câmbio ainda não chegou inteira à bomba.
- **Energia elétrica (fora do modelo).** Bandeira verde em outubro (Agência Brasil · 25/09 · nível B), contra o Copom, que supõe amarela até dezembro (IN-S4). A de novembro e a de dezembro não estavam publicadas nas fontes do agente web: elas decidem até ±0,10 p.p. do 4T26.
- **Commodities (IN-S7, agente externo).** O agro em dólar fica em 202 no base do principal, perto do recorde, e os metais em 332–326 (P1); a cauda de queda das commodities tem mais probabilidade que a de alta (25% contra 20%). O IC-Br metal em dólar acumula +42,2% em 12 meses (`comm_icbr_usd` · set/26), mas o EX3 de industriais desacelerou de 4,15% para 3,70% em 12 meses (`inflc_agregados` · set/26): os metais não estão chegando ao consumidor.
- **Base de comparação.** O 4T25 (0,60%) foi o mais baixo dos quartos trimestres de 2016 a 2025, salvo o de 2018 (0,39%; média 1,49%); o 1T26 (1,92%) e o 2T26 (1,42%) ficaram acima da média dos mesmos trimestres (1,71% e 1,08%) (F, IPCA por trimestre; padrão de 2016–2025 por G na rodada 1). Por isso o 12 meses sobe no 4T26 mesmo com o trimestre abaixo da média sazonal, e cai no 1T27 e no 2T27 sem desinflação.

### Q4 — O cenário para o IPCA

**Por que a central.** A central é a do P1: 5,32% em dezembro, 4,19% no 1T28. O 4T26 sobe por efeito-base[^6]: o modelo põe o trimestre em 1,32%, contra o 0,60% do 4T25 que sai da janela. Alimentação sobe de 0,66 para 1,00 p.p. de contribuição (~6,5% em 12 meses) pela sazonalidade do quarto trimestre, pela inércia do choque in natura e pelo câmbio; monitorados de 1,09 para 1,37 p.p. porque sai a queda de energia do 4T25 (−0,17% no trimestre, F por trimestre). Depois, o 12 meses cai a 4,48% no 2T27 com a saída do 1T26 e do 2T26. Serviços carregam a queda e a persistência ao mesmo tempo: a contribuição vai de 2,14 para 1,69 p.p. (~4,7% em 12 meses no 1T28) porque o hiato vai de 0,41% a −0,52% e a Selic média de 14,06% a 12,00%, mas devagar, porque a equação de serviços lê a média dos últimos quatro trimestres com peso 0,685 (`I.IS.is1b`) e o hiato com 0,092 (`I.IS.is2`). Monitorados ficam em ~1,0 p.p. (~3,75% no 1T28), da equação mais fraca do modelo (indexação com sinal trocado, mapa 2.2): não leio essa central como informação sobre combustíveis e energia.

**O que o P1 mudou contra a rodada 1, e por quê.** A central subiu 0,04 p.p. no 4T26, 0,11 no 1T27 e 0,15–0,18 de 2T27 a 4T27, e quase tudo é câmbio. Com os caminhos dos principais, a PTAX do modelo fica 4,3% a 5,4% acima da do padrão do simulador (5,44 contra 5,21 no 4T26; 5,57 contra 5,28 no 1T28). Dois blocos fazem isso: o CDS e a volatilidade do câmbio (+0,15 R$ na PTAX do 4T26, +0,05 a +0,06 p.p. no IPCA de 1T27 a 3T27) e o bloco externo — inflação americana mais baixa, que pesa na paridade, e dólar mais forte contra emergentes (+0,07 a +0,20 R$, +0,06 a +0,10 p.p. de 2T27 a 1T28). O bloco de commodities (o agro em 202 em vez de 200,5, quase todo) soma +0,02 a +0,03 p.p. até o 3T27. Pelos grupos, a contribuição de alimentação sobe +0,08 a +0,10 p.p. do 1T27 ao 3T27 contra a rodada 1, a de bens industriais +0,07 a +0,09 do 3T27 ao 1T28: o câmbio vai primeiro a alimentos e um trimestre depois a bens industriais; serviços e monitorados não se movem. A NTN-B mais baixa que o padrão tira até 0,34 p.p. da Selic, sem efeito no IPCA dentro do horizonte (G sobre o modelo, atribuição bloco a bloco).

**Contra o Copom e a Focus.**

| | 4T26 | 1T27 | 2T27 | 3T27 | 4T27 | 1T28 |
|---|---|---|---|---|---|---|
| Modelo, central do P1 | 5,32 | 4,96 | 4,48 | 4,52 | 4,38 | 4,19 |
| Copom, cenário de referência (R281) | 5,2 | 4,9 | 4,5 | 4,5 | 3,9 | 3,2 |
| Diferença (p.p.) | +0,12 | +0,06 | −0,02 | +0,02 | +0,48 | +0,99 |
| Focus por ano (23/10) | 5,19 | | | | 4,34 | |

(`pm_copom_projecoes` · 24/09; `expc_focus_periodo` · 23/10)

Até o 3T27 o modelo e o Copom estão juntos, embora o P1 tenha um câmbio 5,5% a 8,1% mais fraco que o condicionante do Copom (5,15) — porque o Copom carrega o que o modelo não vê: Brent de 90 dólares com pico no 4T26, bandeira amarela até dezembro e o fim das subvenções a combustíveis no prazo legal (IN-S4, agente de política monetária); os administrados do Copom (5,3% no 4T26, 4,5% no 1T27) estão perto dos do modelo (~5,3% e ~4,7%). A diferença abre no 4T27 e chega a 0,99 p.p. no 1T28, e não é o câmbio: com a PTAX do downside do agente de câmbio (5,19 no 4T26, perto do condicionante), o modelo ainda dá 4,13% no 1T28. Ela está nos preços livres: ~4,35% no modelo contra 3,2% do Copom, 0,85 dos 0,99 p.p.; os monitorados (~3,75% contra 3,2%) explicam 0,14. Dentro dos livres, serviços a ~4,7% no 1T28 e uma âncora que cai devagar (a Focus 12 meses do modelo ainda está em 3,57% no 1T28) separam as duas projeções. A projeção do Copom é condicional aos caminhos que a governança dele fixa e não é a previsão dele (mapa 2.8); com o câmbio de 5,44 e o Brent do agente externo, os condicionantes do Copom ficariam piores, e não melhores. Contra a Focus, que é anterior a 26/10, o modelo está perto em 2026 (5,32 contra 5,19) e em 2027 (4,38 contra 4,34).

**Por que a faixa e a assimetria para cima.** Na rodada 1 a primeira força de alta era o câmbio de 26/10; o agente de câmbio o leu como persistente e o P1 o pôs na central, então ela sai da assimetria e a do 4T26 cai de +0,15 para +0,09. Ficam quatro forças de alta, fora da central:
1. **Expectativas.** A (E) põe a Focus do 4T26 em 4,17%, contra 4,52% de média nas pesquisas já feitas no trimestre. Passando pelo modelo o tempero que o agente de expectativas aplica no base dele (`E.e1` × 1,2, decisão dele, não cenário meu), a Focus vai a 4,33% no 4T26 e 3,90% no 1T28, e o IPCA de 12 meses sobe +0,10 p.p. no 3T27 e +0,19 no 1T28, mesmo com a Selic 0,53 p.p. mais alta. É a força que mais pesa no horizonte relevante.
2. **Combustíveis.** Preço da Petrobras defasado (Abicom, nível B), Brent de 114 no 4T26 no caminho do agente externo e subvenção com base legal só até dezembro (Durigan, nível B).
3. **Hortaliças.** Chuva no atacado e no plantio (CNN Brasil, nível B) e tomate ainda +24,5% no IPCA-15 de outubro; o El Niño, que a Conab espera "de forma severa neste segundo semestre de 2026 e início de 2027" (Agência Brasil · 15/10 · nível B), é risco de oferta para o primeiro semestre.
4. **Câmbio, na cauda.** O agente de câmbio dá 33% à PTAX acima de 5,60 no 4T26, contra 22% abaixo de 5,25.

Para baixo pesam as commodities, cuja cauda de queda o agente externo põe acima da de alta (25% contra 20%), o Brent devolvendo o pico de outubro, a bandeira verde, a reversão dos in natura no primeiro semestre e um hiato com risco de baixa no 4T26–1T27 (agente de atividade, 32% abaixo da faixa no 4T26). A faixa do 4T26 é a mais estreita porque outubro está quase medido pelo IPCA-15; do 1T27 ao 3T27 ela abre com combustíveis e câmbio; no 1T28 a assimetria cai porque o choque de combustíveis sai da janela, e fica positiva pela âncora.

### Olhado, sem sinal

- Núcleo EX0 · 4,85% em 12 meses (`inflc_agregados` · set/26) · conta a mesma história do EX3 e da média aparada · diria algo se se descolasse dos outros núcleos.
- Núcleo de dupla ponderação · 4,06% em 12 meses (`inflc_agregados` · set/26) · estável contra 4,01% três meses antes · diria algo com movimento acima de 0,2 p.p. num trimestre.
- Taxa de informalidade · 37,5% (`mt_pnad` · ago/26) · estável · diria algo se mudasse a leitura do mercado de trabalho do agente de atividade.
- Veículo próprio (monitorado) · −0,06% em 12 meses (F, monitorados · set/26) · sem movimento · diria algo com mudança de tributo sobre veículos.
- Etanol · 0,60% de peso, +3,16% em setembro, classificado em bens industriais (`inflc_decomposicao` · set/26) · acompanha a gasolina e entra no tempero de combustíveis só pela gasolina · diria algo se divergisse dela.
- IC-Br energia em reais · +10,4% no mês (`comm_icbr` · set/26) · repete o Brent · diria algo se divergisse do Brent.
- PMS informação e comunicação · +4,8% em 12 meses (`atv_pms` · ago/26) · comunicação pesa pouco e subiu 2,78% em 12 meses no IPCA · diria algo com reajuste de telecom.

## 3. Premissas

### 3.1 Etapa 1 — o modelo

**Cenários.**
- Base: os caminhos do P1, cada um do principal da exógena. No modelo, a PTAX fica em 5,44 no 4T26 e sobe a 5,57 no 1T28, o salto de 26/10 mantido.
- Upside: o choque de 26/10 se aprofunda — os caminhos de cauda de alta do agente de câmbio para CDS, volatilidade e dólar contra emergentes — e as commodities sobem com o petróleo — os caminhos de alta do agente externo para o IC-Br e os seus grupos agro e metal.
- Downside: o prêmio de 26/10 se desfaz — os caminhos de cauda de baixa do agente de câmbio — e as commodities caem com o petróleo normalizando — os caminhos de queda do agente externo.

**Caminhos das exógenas.** No base, todas as do P1. Nas caudas, só mudam as seis abaixo; as outras ficam no P1.

| Exógena | Hoje (valor · tabela · data) | Cenário | 4T26 | 1T27 | 2T27 | 3T27 | 4T27 | 1T28 |
|---|---|---|---|---|---|---|---|---|
| `fiscal` — CDS 5 anos, fechamento (p.b.) · principal: fiscal | 137 · `cmb_risco_pais` · 26/10 (agente de câmbio) | base (P1) | 140 | 140 | 138 | 135 | 135 | 135 |
| | | upside | 185 | 200 | 190 | 175 | 165 | 160 |
| | | downside | 118 | 115 | 115 | 115 | 115 | 115 |
| `vol` — volatilidade implícita do real (% a.a.) · principal: câmbio | sem dado no F; 12,19 no 2T26 (modelo) | base (P1) | 17,0 | 15,5 | 14,5 | 14,0 | 13,5 | 13,5 |
| | | upside | 24,0 | 21,0 | 18,0 | 16,0 | 15,0 | 15,0 |
| | | downside | 13,0 | 12,5 | 12,0 | 12,0 | 12,0 | 12,0 |
| `dxy_em` — dólar contra emergentes (pontos) · principal: externo | 130,21 · `cmb_dollar_index_em` · 23/10 (agente externo) | base (P1) | 130,5 | 131,0 | 130,5 | 130,0 | 129,5 | 129,0 |
| | | upside | 132,5 | 132,5 | 132,5 | 132,5 | 132,5 | 132,5 |
| | | downside | 128,5 | 128,5 | 128,5 | 128,5 | 128,5 | 128,5 |
| `icbr_usd` — IC-Br em US$, último mês · principal: externo | 205,70 · `comm_icbr_usd` · set/26 | base (P1) | 204,8 | 203,7 | 202,9 | 202,3 | 201,8 | 201,4 |
| | | upside | 213,8 | 217,5 | 218,9 | 218,0 | 217,5 | 217,4 |
| | | downside | 195,7 | 187,9 | 184,0 | 182,5 | 182,5 | 182,7 |
| `icbr_agr_usd` — IC-Br agropecuária em US$, média · principal: externo | 200,53 · `comm_icbr_usd` · média 3T26 | base (P1) | 202,0 | 202,0 | 202,0 | 202,0 | 202,0 | 202,0 |
| | | upside | 205,0 | 210,7 | 214,0 | 215,0 | 215,0 | 215,0 |
| | | downside | 198,0 | 192,0 | 188,0 | 185,7 | 185,0 | 185,0 |
| `icbr_met_usd` — IC-Br metal em US$, média · principal: externo | 330,14 · `comm_icbr_usd` · média 3T26 | base (P1) | 331,7 | 330,0 | 330,0 | 328,7 | 327,3 | 325,7 |
| | | upside | 346,0 | 358,0 | 362,0 | 362,0 | 362,0 | 362,0 |
| | | downside | 320,0 | 298,3 | 283,3 | 277,0 | 275,0 | 275,0 |

Motivo das caudas: são os caminhos de cauda que os principais (ou, no CDS, o agente de câmbio) escreveram nos reports da rodada 1, combinados na direção que é ruim (upside) ou boa (downside) para a inflação. Não são tese minha sobre essas variáveis e ficam só neste report[^7].

**Saída do modelo.**

| Variável | Cenário | 4T26 | 1T27 | 2T27 | 3T27 | 4T27 | 1T28 |
|---|---|---|---|---|---|---|---|
| IPCA 12m (%) | base | 5,32 | 4,96 | 4,48 | 4,52 | 4,38 | 4,19 |
| | upside | 5,40 | 5,22 | 4,89 | 5,01 | 4,84 | 4,53 |
| | downside | 5,24 | 4,71 | 4,08 | 3,99 | 3,84 | 3,74 |
| IPCA no trimestre (%) | base | 1,32 | 1,57 | 0,96 | 0,60 | 1,19 | 1,38 |
| PTAX, fechamento (R$/US$) | base | 5,44 | 5,50 | 5,51 | 5,50 | 5,53 | 5,57 |
| | upside | 5,75 | 5,84 | 5,80 | 5,73 | 5,73 | 5,77 |
| | downside | 5,24 | 5,33 | 5,38 | 5,41 | 5,46 | 5,52 |
| Selic, média (% a.a.) | base | 13,46 | 13,22 | 12,84 | 12,50 | 12,23 | 12,00 |
| Hiato (% do potencial) | base | 0,13 | −0,08 | −0,24 | −0,36 | −0,45 | −0,52 |
| Focus 12m, média (%) | base | 4,17 | 4,00 | 3,82 | 3,72 | 3,64 | 3,57 |

A faixa de 90% do posterior[^8] da central vai de 5,13–5,51 no 4T26 a 3,86–4,56 no 1T28; não inclui o erro das equações. No downside a PTAX sobe ao longo do horizonte porque as commodities em queda enfraquecem o real no modelo.

**Só o câmbio, para a IN-E1** (commodities no base, contra o base):

| Cenário de câmbio | | 4T26 | 1T27 | 2T27 | 3T27 | 4T27 | 1T28 |
|---|---|---|---|---|---|---|---|
| Upside do câmbio: PTAX contra o base | % | +6,8 | +7,6 | +6,9 | +5,8 | +5,2 | +5,1 |
| | IPCA 12m (p.p.) | +0,04 | +0,13 | +0,20 | +0,23 | +0,20 | +0,12 |
| | alimentação (p.p.) | +0,04 | +0,10 | +0,12 | +0,11 | +0,06 | 0,00 |
| | bens industriais (p.p.) | 0,00 | +0,03 | +0,08 | +0,12 | +0,14 | +0,12 |
| | com repasse × 1,5 (p.p.) | +0,08 | +0,25 | +0,38 | +0,44 | +0,40 | +0,27 |
| Downside do câmbio: PTAX contra o base | % | −4,6 | −4,8 | −4,2 | −3,5 | −3,0 | −2,6 |
| | IPCA 12m (p.p.) | −0,03 | −0,09 | −0,14 | −0,15 | −0,12 | −0,07 |

Serviços e monitorados recebem no modelo no máximo +0,01 p.p. de um câmbio 7% mais fraco.

### 3.2 Etapa 2 — o tempero

**(i) Repasse cambial a alimentos e bens industriais — mais forte que o estimado** · cenário upside
- Coeficientes: `I.IA.ia3` estimado 0,085, intervalo de 90% 0,020 a 0,153; `I.II.ii4` 0,040, intervalo 0,016 a 0,064. Multiplicador × 1,5 nos dois (0,127 e 0,060), dentro do intervalo; o de bens industriais perto da borda.
- Efeito: upside de 5,40 → 5,44 no 4T26, 5,22 → 5,33 no 1T27, 5,01 → 5,20 no 3T27, 4,84 → 5,02 no 4T27.
- Por quê: o repasse é maior quando a depreciação é de prêmio doméstico e vista como persistente, com inflação e expectativas acima da meta (mapa 2.5). O agente de câmbio confirmou as duas primeiras condições (idiossincrática, persistente), e o agente de expectativas lê a implícita de 2 a 5 anos +1,2 p.p. em 26/10. Um salto de 9,19% num pregão é maior que a variação trimestral típica da amostra, e o modelo é linear.
- Onde entra: limite e probabilidade do upside.

**(i) Repasse cambial mais fraco e hiato mais forte em serviços** · cenário downside
- Coeficientes: `I.IA.ia3` e `I.II.ii4` × 0,7 (0,059 e 0,028, dentro do intervalo); `I.IS.is2` estimado 0,092, intervalo 0,042 a 0,142, × 1,5 (0,138, perto da borda).
- Efeito: downside de 4,71 → 4,71 no 1T27, 3,99 → 3,95 no 3T27 e 3,74 → 3,66 no 1T28.
- Por quê: apreciação que só desfaz um salto é absorvida em margem; e o hiato negativo chega a serviços com um setor de volume parado no total (+0,6% em 12 meses, `atv_pms` · ago/26) e com o 3T26 em contração no dado mensal (agente de atividade).
- Onde entra: limite do downside.

**(ii) Combustíveis — Brent, câmbio e a política de preços da Petrobras** · upside e downside
- Hoje: Brent 115,22 US$/barril (`comm_brent` · 20/10), caminho do agente externo de 114 (4T26) a 91 (1T28), alta a 129–130 e queda a 78; diesel +3,70% e gasolina +0,92% no IPCA-15 de outubro (`inflc_decomposicao`); preços "muito defasados" (Abicom; CNN Brasil · 26/10 · nível B).
- Por que o modelo não vê: petróleo e câmbio não entram na equação de monitorados (mapa 2.7).
- Efeito: upside, gasolina e diesel +5% na bomba (metade em nov–dez/26, metade em jan/27, o repasse "lento e gradual" que a Abicom descreve, ou o fim da subvenção em janeiro) → +0,14 p.p. no 4T26, +0,27 do 1T27 ao 3T27, +0,14 no 4T27 (peso de 5,45%, `inflc_decomposicao` · set/26). Downside, −3% no 2T27, quando o Brent da cauda de queda já está em 79 e fecha a defasagem → −0,16 p.p. do 2T27 ao 1T28; o mesmo tamanho viria de um subsídio à gasolina, que o presidente mencionou (Poder360 · 24/10 · nível B), e aí seria custo adiado.
- Onde entra: limites das duas caudas; o upside pesa mais na assimetria porque a defasagem já existe e o downside depende de o Brent cair primeiro.

**(ii) Bandeira tarifária de energia** · upside e downside
- Hoje: energia +7,98% em setembro, −0,89% no IPCA-15 de outubro (`inflc_decomposicao`); bandeira verde em outubro (Agência Brasil · 25/09 · nível B).
- Por que o modelo não vê: decisão regulatória, fora de qualquer exógena.
- Efeito: ±2,5% na conta no 4T26 (um patamar de bandeira acima ou abaixo em novembro–dezembro) → ±0,10 p.p. no 4T26 (peso 3,98%), devolvido no 1T27.
- Onde entra: limites do 4T26.

**(ii) Clima e safra de hortaliças — alimentos in natura** · upside e downside
- Hoje: in natura +5,10% em setembro e +13,0% em 12 meses; tomate +24,54% e batata +10,96% no IPCA-15 de outubro (`inflc_decomposicao`); chuva atrapalhando colheita e plantio (CNN Brasil · 27/10 · nível B).
- Por que o modelo não vê: clima e safra doméstica não estão no modelo; o IC-Br agro não carrega hortaliças.
- Efeito: upside, in natura +5% no 4T26 além do que o modelo dá, devolvido no 2T27 → +0,12 p.p. no 4T26 e no 1T27 (peso 2,38%). Downside, −5% no 1T27 e −5% no 2T27 → −0,12 p.p. no 1T27, −0,24 do 2T27 ao 4T27, −0,12 no 1T28.
- Onde entra: limites das duas caudas. Não há série de clima no F (Faltou).

**(ii) Salários além do hiato em serviços** · upside
- Hoje: rendimento real habitual +3,7% em 12 meses, desocupação 5,3% (`mt_pnad` · ago/26); desocupação dessazonalizada 1,89 p.p. abaixo da NAIRU do QPC (agente de atividade).
- Por que o modelo não vê: salários não estão no modelo; só a parte que o hiato não carrega conta, para não dobrar o efeito.
- Efeito: +0,10 p.p. no 4T27 e no 1T28, quando o hiato do modelo já está negativo e o salário real ainda não terá ajustado.
- Onde entra: limite do upside nos dois últimos trimestres.

**(ii) Expectativas acima da (E) e por componente** · assimetria do cenário base
- Hoje: média de 4,52% nas pesquisas do 4T26 contra 4,17% da (E); Focus de serviços para 2028 em 4,65%, +0,15 p.p. em quatro semanas, com o IPCA de 2028 parado; alimentação no domicílio vista como choque datado, 4,00% em 2028 (`expc_focus`, `expc_focus_periodo` · 23/10, leitura do agente de expectativas).
- Por que entra aqui: a (E) é do agente de expectativas, e o multiplicador dela é dele; a âncora por componente não está no modelo.
- Efeito: não movo a central nem as caudas; o efeito medido do tempero do agente de expectativas (+0,10 p.p. no 3T27, +0,19 no 1T28) pesa na probabilidade do upside de 3T27 em diante.

### 3.3 Da etapa 1 à tese

| Trimestre | Central (P1) | Upside: modelo → (i) → com (ii) | Downside: modelo → (i) → com (ii) |
|---|---|---|---|
| 4T26 | 5,32 | 5,40 → 5,44 → 5,80 | 5,24 → 5,24 → 5,14 |
| 1T27 | 4,96 | 5,22 → 5,33 → 5,72 | 4,71 → 4,71 → 4,59 |
| 2T27 | 4,48 | 4,89 → 5,05 → 5,32 | 4,08 → 4,06 → 3,66 |
| 3T27 | 4,52 | 5,01 → 5,20 → 5,47 | 3,99 → 3,95 → 3,55 |
| 4T27 | 4,38 | 4,84 → 5,02 → 5,26 | 3,84 → 3,78 → 3,38 |
| 1T28 | 4,19 | 4,53 → 4,66 → 4,76 | 3,74 → 3,66 → 3,38 |

A faixa base vai da central até pouco antes de cada cauda com tempero, um pouco mais larga para cima porque as forças de alta (combustíveis defasados, hortaliças, expectativas) já estão em curso e as de baixa dependem de reversão. O cenário de upside fica fora da faixa com 22–29% de probabilidade e o de downside com 13–16%.

### 3.4 O que mudou desde a rodada 1

| O quê | Antes → depois | Por quê | Causa |
|---|---|---|---|
| Central | 5,28 / 4,85 / 4,33 / 4,34 / 4,23 / 4,08 → 5,32 / 4,96 / 4,48 / 4,52 / 4,38 / 4,19 | exógenas dos principais: PTAX 5,44–5,57 no lugar de 5,21–5,28 | P1 |
| Faixas | 5,10–5,45 / 4,60–5,15 / 4,05–4,70 / 4,05–4,75 / 3,95–4,60 / 3,80–4,40 → 5,15–5,50 / 4,70–5,25 / 4,15–4,85 / 4,20–4,90 / 4,05–4,75 / 3,85–4,55 | acompanham a central; de 2T27 em diante, um pouco mais largas porque as caudas de commodities do agente externo são mais largas que as que eu supunha | P1; report do externo |
| P(up) / P(down) | 25/10, 30/12 (×3), 28/14, 25/15 → 22/13, 28/14, 29/14, 29/14, 28/15, 26/16 | a depreciação que puxava o upside entrou na central; bandeira verde em outubro; a cauda de queda das commodities é mais provável que a de alta | report do câmbio, do externo; notícia (Agência Brasil · 25/09) |
| Caudas da etapa 1 | CDS de 195 e 94 como artifício para levar a PTAX a 5,50 e 5,05, agro ±5% → caminhos de cauda do câmbio (CDS, vol, dólar EM) e do externo (IC-Br, agro, metais) | há caminhos de cauda dos donos; o artifício sai | reports do câmbio e do externo |
| Peso de combustíveis | 6,05% → 5,45%; +0,30 → +0,27 p.p. no upside, −0,18 → −0,16 no downside | o tempero é de gasolina, diesel e GNV, que são monitorados; o 6,05% incluía o etanol, que o BC classifica em bens industriais | revisão própria |
| Bandeira | premissa "±5% na conta" → "±2,5%", mesmo efeito de ±0,10 p.p. | o texto da rodada 1 não batia com a conta: ±5% sobre 3,98% de peso seriam ±0,20 p.p. | revisão própria |
| In natura | reversão no 4T26–1T27 → no 1T27–2T27; novo upside de +5% no 4T26 | chuva no atacado e no plantio; tomate +24,54% no IPCA-15 de outubro | notícia (CNN Brasil · 27/10 · nível B); dado |
| Multiplicadores | sem mudança | — | — |

## 4. Para os outros agentes

**Respostas às entradas fixas**

- **IN-E1 (pass-through), em destaque: o agente de câmbio leu o salto de 26/10 como persistente.** No caminho do P1 (PTAX 5,44–5,57), o modelo já põe na central uma depreciação de 4–5% contra o padrão. Para uma PTAX mais 7% acima disso (o upside do câmbio), o modelo soma ao IPCA 12m +0,13 p.p. no 1T27 e +0,23 no 3T27: primeiro alimentos, no mesmo trimestre (`I.IA.ia3`; +0,10 p.p. no 1T27), depois bens industriais, com um trimestre de defasagem (`I.II.ii4`; +0,14 no 4T27); serviços e monitorados, nada. Com repasse × 1,5, +0,25 e +0,44. Fora do modelo, a depreciação chega a gasolina e diesel pela paridade da Petrobras, com a defasagem de política que a Abicom descreve: 5% na bomba somam +0,27 p.p. por quatro trimestres; a medicamentos no reajuste anual; e, pela indexação, a contratos no ano seguinte. Tudo isso é primeira ordem; a segunda ordem apareceria nas expectativas (Focus do modelo +0,07 p.p. no 4T27 nesse cenário) e em serviços.
- **IN-E2 (câmbio):** a tese da seção 1; as caudas vêm de combustíveis, hortaliças e expectativas, e o câmbio entra nelas pelo repasse.
- **IN-E3 (política monetária, S7 e S8 dele):** 4,19% no 1T28, faixa 3,85–4,55, upside 26% contra 16%. Entre o modelo e o Copom, fico com o modelo: a diferença de 0,99 p.p. está em preços livres (0,85 p.p.) e não no câmbio (com a PTAX perto do condicionante, o modelo dá 4,13%), e os condicionantes do Copom (câmbio de 5,15, Brent de 84 no 2T27) ficaram mais favoráveis que os caminhos deste ciclo. O repasse de uma depreciação de 6–9% está na IN-E1. O choque corrente é de primeira ordem; a segunda está em risco por serviços subjacentes (5,32% e subindo) e por expectativas (mercado à frente da pesquisa).
- **IN-E4 (atividade, S-IN1):** alimentação contribui 1,00 p.p. no 4T26 e cai a 0,64–0,74 de 2T27 em diante; monitorados 1,37 p.p. no 4T26 e ~1,0 depois. A cauda de alta está nesses dois grupos, os que mais pesam no consumo de baixa renda.
- **IN-E5 (atividade, S-IN2):** sim, serviços estão acima do que o hiato explica. No modelo, o nível de serviços vem da média dos quatro trimestres anteriores (`I.IS.is1b` 0,685), não do hiato (`I.IS.is2` 0,092), e os subjacentes aceleraram de 5,00% para 5,32% no trimestre enquanto o hiato do BC caía. Isso é compatível com um hiato medido baixo demais ou com salário além do hiato; o dado deste ciclo não separa os dois. Os serviços às famílias no percentil 100 que você leu pesam a favor do primeiro.
- **IN-E6 (fiscal, FS-IN1):** a tese da seção 1; IPCA no trimestre de 1,32% no 4T26, 1,57% no 1T27, 0,96% no 2T27, 0,60% no 3T27, 1,19% no 4T27 e 1,38% no 1T28 (P1).
- **IN-E7 (fiscal, FS-IN2):** a central não supõe decisão de governo sobre preços. O upside supõe a Petrobras repassando 5% entre novembro e janeiro, ou o fim da subvenção em janeiro sem renovação; o downside, combustíveis 3% mais baratos no 2T27, por Brent ou por subsídio à gasolina (custo adiado). O Copom supõe o fim das subvenções no prazo legal; o ministro da Fazenda disse que a proposta deve ser mantê-las.
- **IN-E8 (externo, XS7):** a tese depende mais do petróleo, que chega por combustíveis (fora do modelo), do que de agro e metais. No modelo, +10% no agro somam +0,19 a +0,25 p.p. ao IPCA 12m do 4T26 ao 3T27 e +0,05 a +0,08 depois; +10% nos metais, +0,04 no 4T26 crescendo a +0,19 no 3T27. Os trimestres em que a precisão rende são 4T26–3T27 no agro e 2T27–4T27 nos metais.
- **IN-E9 (expectativas, XS5):** a central sobe a 5,32% em dezembro por efeito-base, não por aceleração; saem da janela o 1T26 (1,92%) e o 2T26 (1,42%), o que derruba o 12 meses no 1T27 e no 2T27. Do câmbio de 26/10, a parte que o P1 carrega já está na central; um câmbio mais 7% fraco passaria +0,13 p.p. ao 1T27 e +0,20 ao 2T27. A Focus de serviços para 2028 em 4,65% tem sustentação: o modelo dá ~4,7% para serviços no 1T28, com subjacentes a 5,32% hoje.
- **IN-E10 (expectativas, XS6):** setembro 0,82% contra 0,56% da QPC (energia); IPCA-15 de outubro 0,32% contra 0,28% da Focus mensal e 0,34% da QPC para o IPCA do mês. A energia de outubro já está quase toda no IPCA-15; o risco para o IPCA de outubro vem de alimentos.

**Pedidos**

- **IN-S1 (câmbio):** respondido (persistente; 5,35–5,39). Para o report final: o dólar caiu em 27/10 depois da alta de 8,36% (InfoMoney · 27/10 · nível B); a probabilidade de a PTAX fechar o 4T26 acima de 5,60 segue em 33%? Decide o multiplicador × 1,5 do repasse.
- **IN-S2 (câmbio):** respondido (idiossincrático). Quando os pares latinos tiverem dado depois de 26/10, a comparação confirma? Decide se a depreciação vem com prêmio doméstico, que é o que justifica o × 1,5.
- **IN-S3 (política monetária):** respondido (manter 13,75% em 04/11 com 75% e em 09/12 com 54%). A depreciação muda o câmbio de partida da projeção de 09/12 para perto de 5,40? Decide quanto da diferença de 0,99 p.p. contra o Copom fecha na próxima projeção.
- **IN-S4 (política monetária):** respondido. Quanto dos 4,5% de administrados do Copom no 1T27 é o fim das subvenções a combustíveis, e a bandeira "neutra" de 2027 é verde ou amarela? Decide a comparação de monitorados e o tempero de combustíveis no 1T27.
- **IN-S5 (atividade):** respondido. O IBC-Br de setembro (meados de novembro) acima de +1,0% sobre agosto tira a sua discordância de partida; abaixo de zero a leva para −0,45 — avise quando sair. Decide o multiplicador de `I.IS.is2` no downside.
- **IN-S6 (fiscal):** sem resposta na rodada 1 (o F não traz decisão de governo). Valor por litro e data de fim da subvenção ao diesel da MP 1.391, se há proposta de renovação para 2027 e qualquer medida sobre gasolina ou energia depois de 25/10. Decide o tempero de combustíveis do 1T27 e se o downside é custo adiado.
- **IN-S7 (externo):** respondido (P1). O caminho do agro incorpora o El Niño que a Conab espera para o início de 2027? Decide se a cauda de alta de alimentos no 1S27 é só hortaliça ou também commodity.
- **IN-S8 (externo):** respondido (Brent de 114 a 91). O que causou o salto de 02/10 segue sem resposta; ele decide a probabilidade do cenário de alta e, com ele, o tempero de combustíveis.
- **IN-S9 (expectativas):** respondido. A Focus de 30/10, a primeira depois de 26/10: 12 meses e 2027. Decide a assimetria de 3T27 em diante.
- **IN-S10 (expectativas):** respondido (alimentação datada; serviços 2028 +0,15). Serviços 2029 acima de 4,10 em duas pesquisas seguidas? Decide se a persistência de serviços que o modelo dá é a do mercado.

**Ao agente web**

- Bandeira tarifária da ANEEL para novembro e dezembro de 2026. Tese: limites do 4T26 (sem resposta na rodada 1).
- Reajustes da Petrobras em gasolina e diesel anunciados depois de 25/10, e a defasagem estimada contra o preço de importação. Tese: tempero de combustíveis, 4T26–1T27.
- Valor e prazo da subvenção ao diesel (MP 1.391) e proposta de renová-la em 2027; qualquer subsídio ou corte de tributo sobre gasolina anunciado depois de 25/10. Tese: tempero de combustíveis no 1T27 e natureza do downside.
- Preços de tomate, batata e cebola no atacado em outubro (Ceagesp ou Conab) e a previsão de chuva para novembro–dezembro nas regiões produtoras. Tese: tempero de in natura, upside do 4T26 e reversão no 1S27.
- Reajustes de ônibus urbano já anunciados para janeiro de 2027 nas capitais. Tese: inércia dos monitorados no 1T27 (sem resposta na rodada 1).

**Como subordinado**

- `icbr_agr_usd` · principal: externo
  - Insumos: a pressão doméstica em alimentos é de hortaliças, fora da cesta do IC-Br: in natura +13,0% em 12 meses, semi-elaborados +6,1%, industrializados +0,3% (`inflc_decomposicao` · set/26); o IC-Br agro em reais subiu 3,3% do 2T26 para o 3T26 (`comm_icbr`), quase todo câmbio. A Conab espera safra de grãos acima de 367 milhões de toneladas, +1,4%, apesar de um El Niño severo no 2S26–início de 2027 (Agência Brasil · 15/10 · nível B): oferta doméstica de grãos sem pressão, com risco climático no 1S27. Sensibilidade no P1: +10% no caminho somam +0,19 a +0,25 p.p. ao IPCA 12m do 4T26 ao 3T27.
  - Argumento: nada nos preços domésticos pede mexer no base de 202; a safra da Conab é coerente com a cauda de queda mais provável que a de alta.
  - Caminho de referência: nenhum.
  - Resposta do principal: o report do externo pôs o Brent no agro só no cenário de alta (o agro sobe junto se o Brent ficar acima de 125), que era a minha pergunta. Sem divergência aberta.
- `icbr_met_usd` · principal: externo
  - Insumos: com o IC-Br metal em US$ +42,2% em 12 meses, o EX3 de industriais desacelerou de 4,15% para 3,70% e bens industriais acumulam 3,07% (`inflc_agregados` · set/26). Uma notícia de nível C diz que o minério de ferro está na mínima de dois anos, com siderúrgicas chinesas comprando "hand-to-mouth" (Yahoo Finance/Bloomberg · 27/10 · nível C): entra só como risco, a favor da cauda de queda dos metais. Sensibilidade no P1: +10% somam +0,04 a +0,19 p.p., crescendo até o 3T27.
  - Argumento: nada a acrescentar ao caminho; se o principal subir o caminho, leio o efeito do modelo como teto, dado o repasse que os preços não mostram.
  - Caminho de referência: nenhum.
  - Resposta do principal: nada a responder (não houve argumento de mudança). Sem divergência aberta.

## 5. Placar

Primeiro ciclo.

## 6. Sobre o modelo

| Fonte | O que sugere | Teste proposto | Por que importa para a tese deste ciclo |
|---|---|---|---|
| Mapa 2.7; Brent +30% em um mês, diesel +3,70% no IPCA-15; o agente externo propõe o mesmo | Petróleo em reais (Brent × PTAX, ou o IC-Br energia em R$) na equação de monitorados, com defasagem de um trimestre, e o IPCA livre no lugar do cheio na indexação (`I.IM.im2`) | Monitorados trimestral, 2003–2026, com e sem a variação do Brent em reais defasada e com o IPCA livre defasado; muda se o coeficiente do petróleo for positivo com intervalo fora de zero e o sinal da indexação se acertar | O choque de petróleo e câmbio do ciclo não aparece em monitorados; vive todo no tempero, e é a maior cauda da tese |
| Mapa 2.6; in natura +13,0% em 12 meses com o IC-Br agro em US$ de lado | Separar in natura do resto de alimentação, ou um termo de clima na equação de alimentação | Alimentação trimestral dividida em in natura e restante, 2006–2026; muda se o ajuste da parte sem in natura melhorar e `I.IA.ia2` subir | O choque de alimentos atual não é commodity, e o modelo o trata só como inércia |
| Focus do modelo de 4,17 no 4T26 contra 4,52 de média nas pesquisas já feitas; energia do IPCA-15 andando com a do IPCA do mesmo mês; o agente de expectativas propõe o mesmo para a (E) | Usar no trimestre em curso o dado que já saiu dentro dele (Focus semanal, IPCA-15, PTAX diária) em vez de partir só do último trimestre fechado | Erro do primeiro trimestre projetado com e sem esse dado parcial, nas projeções fora da amostra de 2015–2026 | A âncora do 4T26 está abaixo do que a aritmética das pesquisas permite, e o erro passa à inflação de 2027 pela âncora dos quatro grupos |
| Mapa 2.3; Focus por componente (serviços 2028 +0,15 com o IPCA de 2028 parado) | Âncora por componente em vez da Focus do IPCA cheio | Equação (I) com a Focus de cada componente como âncora, 2021–2026 (amostra curta); muda se o ajuste de serviços e alimentação melhorar | O mercado põe mais inflação em serviços e menos em alimentação a partir de 2028 do que a âncora comum permite |

[^1]: Núcleo é uma medida que tira ou suaviza os itens mais voláteis do IPCA para mostrar a tendência. O EX3 exclui alimentos e monitorados, entre outros; a média aparada corta os extremos da distribuição de variações do mês.
[^2]: Difusão é a fatia dos subitens do IPCA que subiram no mês. Uma alta de inflação com difusão baixa vem de poucos itens.
[^3]: Serviços subjacentes são os serviços sem os itens mais voláteis (passagem aérea, alimentação fora de casa e outros), os mais ligados a salário e demanda doméstica. O número do IPCA-15 foi refeito pelos subitens com a marca de subjacente da classificação do BC; a QPC pergunta pelo IPCA do mês, então a comparação é aproximada.
[^4]: Efeito de primeira ordem é a alta do próprio item que sofreu o choque (a energia, o tomate). O de segunda ordem é a alta se espalhar para outros preços e salários, por indexação ou por expectativa; é a esse que o Banco Central reage. Pass-through é a fatia de uma variação do câmbio que chega aos preços ao consumidor.
[^5]: A bandeira tarifária é um adicional na conta de luz definido pela ANEEL todo mês, mais caro quando a geração custa mais (reservatório baixo, térmicas ligadas). Por isso a energia sobe e devolve de um mês para o outro.
[^6]: O IPCA de 12 meses muda tanto pelo mês que entra quanto pelo que sai da janela. Quando sai um trimestre muito baixo, o 12 meses sobe mesmo que a inflação do trimestre novo seja normal: é o efeito-base.
[^7]: Da rodada 2 em diante, a central é a do P1, rodada com os caminhos base dos principais; os caminhos de cauda acima são de reports da rodada 1 e não entram no P. Os números da seção 2 que vêm de outros agentes (hiato, percentis do PMS, média das pesquisas do 4T26, probabilidades de câmbio e commodities) são leituras deles, citadas como tais.
[^8]: A faixa do posterior mostra só a incerteza sobre os pesos estimados do modelo, não a incerteza da previsão; a faixa da tese, na seção 1, é a do agente.
[^9]: Percentil é a posição do último valor no histórico, de 0 (o menor já visto) a 100 (o maior). Percentil 100 em dez anos quer dizer o maior valor da série nesse período.
