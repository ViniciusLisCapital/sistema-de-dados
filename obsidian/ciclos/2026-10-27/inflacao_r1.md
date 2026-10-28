# Report — inflação · ciclo 2026-10-27 · rodada 1

Dados até: 2026-10-27 (IPCA de set/26, IPCA-15 de out/26, PTAX de 26/10, Focus de 23/10) · Horizontes: 4T26 a 1T28, a variável é o IPCA acumulado em 12 meses no fechamento do trimestre (mar, jun, set, dez)

## 1. Tese

| Variável | Trimestre | Central | Base: faixa · P | Upside: limite · P | Downside: limite · P | P(up) − P(down) |
|---|---|---|---|---|---|---|
| IPCA 12 meses, fim do trimestre (%) | 4T26 | 5,28 | 5,10 a 5,45 · 65% | acima de 5,45 · 25% | abaixo de 5,10 · 10% | +0,15 |
| | 1T27 | 4,85 | 4,60 a 5,15 · 58% | acima de 5,15 · 30% | abaixo de 4,60 · 12% | +0,18 |
| | 2T27 | 4,33 | 4,05 a 4,70 · 58% | acima de 4,70 · 30% | abaixo de 4,05 · 12% | +0,18 |
| | 3T27 | 4,34 | 4,05 a 4,75 · 58% | acima de 4,75 · 30% | abaixo de 4,05 · 12% | +0,18 |
| | 4T27 | 4,23 | 3,95 a 4,60 · 58% | acima de 4,60 · 28% | abaixo de 3,95 · 14% | +0,14 |
| | 1T28 | 4,08 | 3,80 a 4,40 · 60% | acima de 4,40 · 25% | abaixo de 3,80 · 15% | +0,10 |

**Decomposição da central** — contribuição de cada grupo ao IPCA de 12 meses no cenário base do modelo, em p.p. (os quatro mais o resíduo somam a central):

| Trimestre | Serviços | Alimentação | Bens industriais | Monitorados | Resíduo |
|---|---|---|---|---|---|
| 3T26 (observado) | 2,14 | 0,66 | 0,69 | 1,09 | 0,00 |
| 4T26 | 2,06 | 0,96 | 0,90 | 1,37 | 0,00 |
| 1T27 | 1,96 | 0,88 | 0,81 | 1,22 | −0,01 |
| 2T27 | 1,96 | 0,59 | 0,77 | 1,01 | 0,00 |
| 3T27 | 1,86 | 0,64 | 0,80 | 1,05 | 0,00 |
| 4T27 | 1,76 | 0,63 | 0,82 | 1,01 | 0,00 |
| 1T28 | 1,69 | 0,61 | 0,81 | 0,97 | 0,00 |

A assimetria está em **alimentação e monitorados**: o upside viria do repasse da depreciação de 26/10 aos alimentos (no modelo) e do petróleo aos combustíveis (fora dele); o downside, da reversão dos alimentos in natura e de um petróleo mais barato chegando à bomba. Serviços carregam a persistência da central, não a cauda.

- **Acima da faixa** se a depreciação de 26/10 persistir (PTAX perto de 5,50 no fechamento do 4T26) e a Petrobras repassar petróleo e câmbio à bomba: o câmbio sozinho leva o 1T27 a 5,11 no modelo com o repasse a alimentos e bens industriais × 1,5, e combustíveis 5% mais caros em nov/26–jan/27 somam +0,30 p.p., chegando a 5,41. Ruim para o Brasil: é inflação de choque sobre uma inflação de tendência já acima da meta.
- **Abaixo da faixa** se a depreciação se desfizer (PTAX perto de 5,05), os in natura devolverem a alta e o petróleo mais barato chegar à bomba no 2T27: 4,71 no modelo para o 1T27, 4,47 com a reversão dos in natura. Bom para o Brasil se vier de oferta; se vier de corte de imposto sobre combustível, é custo adiado.

**A tese em uma frase:** o IPCA de 12 meses sobe a ~5,3% em dezembro porque sai da janela um 4T25 muito baixo, e cai a ~4,1% no 1T28 — acima da meta de 3,00% e acima da projeção do Copom (3,2%) — porque serviços desaceleram devagar; o risco está para cima, concentrado em alimentos e combustíveis, pela depreciação de 26/10 e pelo petróleo.

## 2. Argumentação

### Q1 — O que explica a inflação corrente: quanto é choque e quanto é tendência?

**Setembro foi choque concentrado; a tendência está estável, mas acima da meta.** O IPCA de set/26 subiu 0,82% (`inflc_agregados` · set/26) contra 0,34% na média dos setembros dos dez anos anteriores, e só um dos dez foi maior (`F, padrão sazonal` · set/26). A alta veio de poucos itens: as cinco maiores contribuições — energia elétrica residencial (+7,98%, 0,318 p.p.), tomate, passagem aérea, gasolina e batata-inglesa — somam 0,58 p.p., ~70% do índice do mês, e a energia sozinha responde por ~39% (`inflc_decomposicao` · set/26). Os núcleos[^1] mostram o mês normal por baixo do choque: o EX3 subiu 0,26% contra 0,28% na média dos setembros, e a média aparada 0,31% contra 0,31% (padrão sazonal · set/26). A difusão[^2] de 54,9% está abaixo da média dos setembros de 2016–2025 (56,0%; quatro dos dez setembros foram menores) (`inflc_agregados` · set/26), o que confirma que a alta não se espalhou pela cesta.

| Grupo (BC) | Set/26 no mês (%) | Média dos setembros, 10a (%) | 12 meses (%) | 12 meses, 3 meses antes (%) |
|---|---|---|---|---|
| Serviços | 0,61 | 0,33 | 5,97 | 5,90 |
| Alimentação | 0,96 | 0,03 | 4,19 | 3,01 |
| Bens industriais | 0,17 | 0,23 | 3,07 | 2,76 |
| Monitorados | 1,59 | 0,65 | 4,14 | 5,52 |

(`inflc_agregados` e padrão sazonal · set/26)

**O IPCA-15 de outubro confirma a leitura e desloca o choque para alimentos.** Subiu 0,32% (`inflc_indice_geral` · out/26), contra 0,34% que a QPC esperava para o IPCA de outubro (`expc_qpc` · R281). Por grupo, alimentação subiu 1,01% e contribuiu 0,16 p.p., puxada por tomate (+24,5%), arroz (+5,8%), cebola (+13,6%) e batata (+11,0%); serviços +0,23%, industriais +0,20%, monitorados +0,15% (`inflc_decomposicao`, IPCA-15 · out/26). A energia devolveu (−0,89%) e a passagem aérea caiu 9,24%, mas gasolina (+0,92%) e óleo diesel (+3,70%) subiram (mesma fonte). Mas serviços subjacentes[^3] no IPCA-15 subiram 0,45% (recorte por subitem, `inflc_decomposicao` · out/26), acima dos 0,40% da QPC para o IPCA de outubro (p75 de 0,46): se o IPCA de outubro confirmar acima de 0,46, a leitura de "tendência estável" fica mais fraca.

**O choque de alimentos é de horta, não de commodity.** Os alimentos in natura acumulam +13,0% em 12 meses e +5,10% em setembro, depois de −5,98% e −4,38% em julho e agosto; os semi-elaborados, +6,1% em 12 meses; os industrializados, +0,3% (`inflc_decomposicao` · set/26, por classe do BC). Os tubérculos, raízes e legumes acumulam +48,3% em 12 meses (`inflc_decomposicao_item` · set/26).

**Que mês moveu o 12 meses.** O 12 meses foi de 4,22% em agosto para 4,58% em setembro porque entrou o 0,82% de set/26 e saiu o 0,48% de set/25 (`inflc_indice_geral`). No trimestre, o 3T26 (0,57%) substituiu um 3T25 de 0,63%, e o 12 meses do fechamento ficou quase parado (4,64% → 4,58%) (`F, IPCA por trimestre`). Monitorados caíram de 5,52% para 4,14% em 12 meses no trimestre pela saída da energia de set/25 (+10,31%, `inflc_decomposicao`).

**Surpresas contra a expectativa de curto prazo (IN-E10).** Setembro veio 0,82% contra 0,56% da mediana da QPC (p75 0,60), toda a diferença em energia; serviços subjacentes vieram 0,36% contra 0,30% (`expc_qpc` · R281; `inflc_decomposicao` · set/26). A surpresa de serviços é a que importa para a tendência.

### Q2 — Quão persistente é a inflação, e o que a propaga?

**A persistência está em serviços, e serviços estão firmes.** Serviços acumulam 5,97% em 12 meses e os subjacentes 5,32%, contra 5,00% três meses antes (`inflc_decomposicao` · set/26); no 3T26 o núcleo EX3 de serviços subiu 1,18%, contra 0,99% na média dos terceiros trimestres de 2016–2025 (`inflc_agregados`). Os não comercializáveis acumulam 6,22% contra 2,65% dos comercializáveis (`inflc_agregados` · set/26): a inflação que fica é doméstica. O mercado de trabalho sustenta isso, sem concluir sobre ele (é leitura do agente de atividade, IN-S5): desocupação de 5,3% em agosto, rendimento real habitual +3,7% e massa de rendimento +4,8% em 12 meses (`mt_pnad` · ago/26), emprego formal em serviços +2,9% (`mt_caged` · ago/26). Mas o volume de serviços está parado — +0,6% em 12 meses no total, +4,2% nos prestados às famílias (`atv_pms` · ago/26) — e o hiato do BC caiu de 1,47% no 4T24 para 0,41% no 3T26 (`pm_hiato_produto` · RPM set/26): a pressão de demanda está diminuindo, e o que mantém serviços altos é sobretudo inércia e salário.

**Indexação formal.** Plano de saúde acumula 5,69% em 12 meses e aluguel e taxas 6,32% (`F, monitorados item a item` · set/26), os dois reajustados olhando a inflação passada; transporte público, 4,91%.

**Expectativas acima da meta, em todos os horizontes (leitura, não conclusão: IN-S9).** A Focus 12 meses à frente está em 4,53%, a de 24 meses em 3,87% (`expc_focus` · 23/10); por ano, 5,19% para 2026, 4,34% para 2027, 3,75% para 2028 e 3,50% para 2029 (`expc_focus_periodo` · 23/10), contra meta de 3,00% (`inflc_meta`). Com âncora acima da meta, um choque de primeira ordem dura mais. A QPC dá 25% de probabilidade de o IPCA no horizonte relevante ficar mais de 0,5 p.p. acima da meta, contra 15% abaixo (`expc_qpc` · R281).

**Primeira ou segunda ordem?** Por ora, o choque de setembro–outubro (energia, in natura, combustíveis) é de primeira ordem[^4]: núcleos no padrão sazonal, difusão abaixo da média do mês. A segunda ordem está em risco por dois canais — expectativas já acima da meta e serviços subjacentes acelerando no 12 meses (de 5,00% para 5,32% no trimestre) — e o que a confirmaria é o EX3 de outubro e novembro acima da média dos mesmos meses do histórico.

### Q3 — Que pressões estão chegando ao IPCA, grupo a grupo?

| Grupo | Pressão | Direção | Quando |
|---|---|---|---|
| Alimentação | in natura no IPCA-15 de outubro (+1,01% no grupo); depreciação de 26/10 | alta | 4T26–1T27 |
| Monitorados | Brent alto chegando a gasolina e diesel; bandeira tarifária | alta (combustíveis), indefinida (energia) | 4T26–1T27 |
| Bens industriais | depreciação, com um trimestre de defasagem; metais | alta, pequena | 1T27–4T27 |
| Serviços | hiato fechando; salários reais crescendo | desaceleração lenta | todo o horizonte |

- **Câmbio (aguarda câmbio, IN-S1).** A PTAX saltou 9,2% num pregão, de 5,0377 em 23/10 para 5,5007 em 26/10, depois de ter caído para ~5,0 no começo de outubro (`cmb_ptax` · 26/10). É um dado de um dia, e se ele é persistente é o agente de câmbio que diz. Se persistir, o modelo leva a depreciação a alimentos no mesmo trimestre e a bens industriais no seguinte: +0,10 p.p. no 12 meses do 1T27 e +0,18 p.p. no 3T27 (seção 3.1). O cenário base do modelo, com as exógenas no padrão, fecha o 4T26 com a PTAX em 5,21 — isto é, supõe que o salto se desfaça.
- **Petróleo e combustíveis (fora do modelo).** O Brent fez média de 125 dólares em outubro, ~30% acima da média do 3T26 (96), mas caiu 15% desde 02/10 (135,51), para 115,22 em 20/10 (`comm_brent`). A alta já aparece na bomba: diesel +3,70% e gasolina +0,92% no IPCA-15 de outubro, depois de gasolina +1,21% em setembro (`inflc_decomposicao`). Combustíveis (veículos) acumulam −0,71% em três meses e 5,95% em 12 meses (`F, monitorados` · set/26): a alta do Brent ainda não chegou inteira, e a política de preços da Petrobras é o que decide quanto e quando (pedido ao agente web, seção 4). A Focus do IGP-M de 2026 subiu 0,85 p.p. em quatro semanas, a 5,61% (`expc_focus_periodo` · 23/10), o que mostra pressão nos preços no atacado.
- **Energia elétrica (fora do modelo).** +7,98% em setembro e −0,89% no IPCA-15 de outubro, depois de −7,63% em agosto (`inflc_decomposicao`): a bandeira tarifária[^5] mudou de patamar mês a mês, e a de novembro e dezembro decide até ±0,10 p.p. do 4T26. O F não carrega o calendário das bandeiras (pedido ao agente web).
- **Commodities.** O IC-Br agropecuária em reais subiu 3,3% da média do 2T26 para a do 3T26 (`comm_icbr`), e em dólar ficou de lado (média 197,67 no 2T26, 200,53 no 3T26, `comm_icbr_usd`). O IC-Br metal em dólar acumula +42,2% em 12 meses (`comm_icbr_usd` · set/26), mas a média do 3T26 (330,14) ficou abaixo da do 2T26 (339,45), e o núcleo EX3 de industriais desacelerou de 4,15% para 3,70% em 12 meses (`inflc_agregados` · set/26): os metais não estão chegando ao consumidor.
- **Base de comparação.** Saem da janela trimestres muito diferentes entre si: o 4T25 (0,60%) foi o mais baixo dos quartos trimestres de 2016 a 2025, salvo o de 2018 (0,39%; média 1,49%); o 1T26 (1,92%) e o 2T26 (1,42%) ficaram acima da média dos mesmos trimestres (1,71% e 1,08%) (`F, IPCA por trimestre`; padrão de 2016–2025 por G). Por isso o 12 meses sobe no 4T26 mesmo com o trimestre abaixo da média sazonal, e cai no 1T27 e no 2T27 mesmo sem desinflação.

### Q4 — O cenário para o IPCA

**Por que a central.** O modelo põe o IPCA do 4T26 em 1,27% no trimestre e o 12 meses de dezembro em 5,28%. É o efeito-base[^6] do 4T25: para o 12 meses ficar em 5,00% bastaria um 4T26 de 1,01%. O canal por grupo: alimentação sobe de 0,66 para 0,96 p.p. de contribuição pela sazonalidade do quarto trimestre (o padrão de 2016–2025 dá 2,49% para alimentação num 4T) e pela inércia do choque in natura; monitorados sobem de 1,09 para 1,37 p.p. porque sai da janela a queda de energia do 4T25 (monitorados −0,17% no 4T25, `F, por trimestre`). Daí em diante, o 12 meses cai a 4,33% no 2T27 com a saída do 1T26 e do 2T26 e a 4,08% no 1T28. Serviços carregam a queda: a contribuição deles vai de 2,14 para 1,69 p.p. (~4,7% em 12 meses no 1T28), porque o hiato do modelo passa de 0,41% para −0,51% e a Selic média recua de 14,06% para 12,27%, mas devagar, porque a equação de serviços lê a média dos últimos quatro trimestres com peso 0,685 (`I.IS.is1b`). Monitorados ficam em ~1,0 p.p. (~3,7%), a equação mais fraca do modelo (indexação com sinal trocado, mapa 2.2) — não leio a central dela como informação sobre combustíveis e energia.

**Contra o Copom e a Focus.**

| | 4T26 | 1T27 | 2T27 | 3T27 | 4T27 | 1T28 |
|---|---|---|---|---|---|---|
| Modelo (central) | 5,28 | 4,85 | 4,33 | 4,34 | 4,23 | 4,08 |
| Copom, cenário de referência (R281) | 5,2 | 4,9 | 4,5 | 4,5 | 3,9 | 3,2 |
| Focus por ano (23/10) | 5,19 | | | | 4,34 | |

(`pm_copom_projecoes` · 24/09; `expc_focus_periodo` · 23/10)

No 4T26 o modelo, o Copom (5,2%), a Focus (5,19%) e a QPC (outubro–dezembro de 0,34%, 0,32% e 0,55% dão 5,21% em dezembro) estão juntos. A diferença está no horizonte relevante: 4,08% no modelo contra 3,2% do Copom no 1T28, 0,9 p.p. A QPC dá 4,00% para o mesmo trimestre (`expc_qpc` · R281), perto do modelo. Pelos grupos, a diferença está nos preços livres: o modelo dá ~4,2% para livres no 1T28 contra 3,2% do Copom, e ~3,7% para monitorados contra 3,2%. Dentro dos livres, serviços explicam a maior parte, pela inércia de quatro trimestres e por uma âncora de expectativas que no modelo cai devagar (a Focus 12 meses do modelo ainda está em 3,52% no 1T28). Quais condicionantes o Copom usou (Selic da Focus, câmbio, petróleo, bandeira) chegam pela IN-S4 — **aguarda política monetária (IN-S4)**; a projeção do Copom é condicional a esses caminhos e não é a previsão dele (mapa 2.8). Contra a Focus por componente de 2027, o modelo põe menos em alimentação (0,63 p.p. no 4T27 contra ~0,89 p.p. que a mediana de 5,76% para alimentação no domicílio implica com o peso do grupo) e mais em bens industriais (0,82 contra ~0,61 p.p.); o total fica perto (4,23% contra 4,34%).

**Por que a faixa e a assimetria para cima.** Quatro forças, todas fora da central:
1. A PTAX de 26/10 (5,50) já está no nível do cenário de upside; a central supõe que ela volte a ~5,21 até dezembro. Enquanto o agente de câmbio não disser se o salto é persistente, a probabilidade do upside fica maior que a do downside.
2. O petróleo ~30% acima da média do 3T26 ainda não chegou inteiro à bomba, e o modelo não vê combustíveis.
3. A Focus de alimentação no domicílio (7,38% para 2026, +0,53 p.p. em quatro semanas; 5,76% para 2027) está acima do que o modelo dá ao grupo, e a QPC tem 60% das respostas com risco de alta para 2027 (`expc_qpc` · R281).
4. A expectativa de 12 meses do modelo para o 4T26 (4,16%, média do trimestre) já está abaixo da Focus observada em outubro (4,53%, `expc_focus` · 23/10). Como a âncora dos quatro grupos é a Focus do trimestre anterior, uma expectativa que cai mais devagar do que o modelo supõe põe a inflação de 2027 acima da central (pedido ao agente de expectativas, seção 4).

Para baixo pesam a reversão dos in natura (que já devolveram ~10% em julho e agosto, depois de alta no primeiro semestre), o Brent em queda desde 02/10 e um hiato que o modelo já põe negativo a partir do 1T27. A faixa do 4T26 é mais estreita porque outubro está quase medido pelo IPCA-15; do 1T27 ao 3T27 as faixas abrem com o câmbio e o petróleo.

### Olhado, sem sinal

- Núcleo EX0 · 4,85% em 12 meses (`inflc_agregados` · set/26) · conta a mesma história do EX3 e da média aparada, sem informação própria · diria algo se se descolasse dos outros núcleos.
- Núcleo de dupla ponderação · 4,06% em 12 meses (`inflc_agregados` · set/26) · estável contra 4,01% três meses antes · diria algo com movimento acima de 0,2 p.p. num trimestre.
- Taxa de informalidade · 37,5% (`mt_pnad` · ago/26) · estável · diria algo se mudasse a leitura do mercado de trabalho que o agente de atividade traz.
- Desocupação dessazonalizada retropolada · 5,41% (`mt_desocupacao_retro` · jul/26) · repete a PNAD · diria algo numa virada de tendência.
- Veículo próprio (monitorado) · −0,06% em 12 meses (`F, monitorados` · set/26) · sem movimento · diria algo com mudança de tributo sobre veículos.
- IC-Br energia em reais · +10,4% no mês (`comm_icbr` · set/26) · repete o Brent, que já está no argumento · diria algo se divergisse do Brent.
- PMS informação e comunicação · +4,8% em 12 meses (`atv_pms` · ago/26) · comunicação pesa pouco e subiu 2,78% em 12 meses no IPCA · diria algo com reajuste de telecom.

## 3. Premissas

### 3.1 Etapa 1 — o modelo

**Cenários.**
- Base: as exógenas do modelo ficam no último valor (padrão do simulador; na rodada 1 nenhum principal publicou caminho). No modelo, isso é a PTAX voltando a ~5,21 no fechamento do 4T26 e ficando em ~5,25, o salto de 26/10 desfeito.
- Upside: a depreciação de 26/10 persiste, PTAX em ~5,50 no fechamento do 4T26 e ~5,55 depois; commodities agrícolas em dólar 5% acima do último valor a partir do 1T27.
- Downside: a depreciação se desfaz e vai além, PTAX em ~5,05 (o nível de 23/10); commodities agrícolas 5% abaixo a partir do 1T27.

**Caminhos das exógenas.**

| Exógena | Hoje (valor · tabela · data) | Cenário | 4T26 | 1T27 | 2T27 | 3T27 | 4T27 | 1T28 |
|---|---|---|---|---|---|---|---|---|
| `icbr_agr_usd` — IC-Br agropecuária em US$, média do trimestre | 200,53 · `comm_icbr_usd` · média 3T26 | base (padrão; aguarda externo) | 200,53 | 200,53 | 200,53 | 200,53 | 200,53 | 200,53 |
| | | upside | 200,53 | 210,56 | 210,56 | 210,56 | 210,56 | 210,56 |
| | | downside | 200,53 | 190,50 | 190,50 | 190,50 | 190,50 | 190,50 |
| `icbr_met_usd` — IC-Br metal em US$, média do trimestre | 330,14 · `comm_icbr_usd` · média 3T26 | base · upside · downside (padrão; aguarda externo) | 330,14 | 330,14 | 330,14 | 330,14 | 330,14 | 330,14 |
| `fiscal` — CDS 5 anos, fechamento (pontos-base) | 131 · padrão do simulador · 3T26 | base (padrão; aguarda o principal) | 131 | 131 | 131 | 131 | 131 | 131 |
| | | upside | 195 | 195 | 195 | 195 | 195 | 195 |
| | | downside | 94 | 94 | 94 | 94 | 94 | 94 |

As demais exógenas (meta, juro real de 10 anos, vol, inflação e juro dos EUA, dólar contra emergentes, S&P 500, IC-Br em US$) ficam no padrão do simulador nos três cenários.

Motivo do CDS nas caudas: o modelo não aceita a PTAX como entrada, e o CDS é a exógena que mais a move; 195 e 94 são os valores que levam a PTAX de fechamento do 4T26 a 5,50 e 5,05. É um artifício para pôr a depreciação de 26/10 no modelo, não uma tese sobre o risco fiscal[^7]. Os caminhos das caudas ficam só neste report.

**Saída do modelo.**

| Variável | Cenário | 4T26 | 1T27 | 2T27 | 3T27 | 4T27 | 1T28 |
|---|---|---|---|---|---|---|---|
| IPCA 12m (%) | base | 5,28 | 4,85 | 4,33 | 4,34 | 4,23 | 4,08 |
| | upside | 5,31 | 5,05 | 4,60 | 4,64 | 4,53 | 4,25 |
| | downside | 5,25 | 4,69 | 4,12 | 4,10 | 3,99 | 3,96 |
| IPCA no trimestre (%) | base | 1,27 | 1,51 | 0,91 | 0,58 | 1,16 | 1,36 |
| PTAX, fechamento (R$/US$) | base | 5,21 | 5,25 | 5,25 | 5,24 | 5,25 | 5,28 |
| | upside | 5,50 | 5,54 | 5,54 | 5,53 | 5,55 | 5,57 |
| | downside | 5,05 | 5,08 | 5,08 | 5,07 | 5,09 | 5,11 |
| Selic, média (% a.a.) | base | 13,60 | 13,26 | 12,96 | 12,70 | 12,47 | 12,27 |
| Hiato (% do potencial) | base | 0,13 | −0,08 | −0,24 | −0,36 | −0,45 | −0,51 |
| Focus 12m, média (%) | base | 4,16 | 3,97 | 3,78 | 3,67 | 3,59 | 3,52 |

A faixa de 90% do posterior[^8] da central do IPCA 12m vai de 5,09–5,46 no 4T26 a 3,76–4,42 no 1T28; não inclui o erro das equações.

**Só o câmbio, para a IN-E1:** com a PTAX ~0,29 R$ acima da base em todo o horizonte, o modelo soma ao IPCA 12m +0,04 p.p. no 4T26, +0,10 no 1T27, +0,15 no 2T27, +0,18 no 3T27, +0,17 no 4T27 e +0,13 no 1T28; alimentação leva quase tudo no começo (+0,08 p.p. no 1T27), bens industriais no fim (+0,11 p.p. no 4T27), monitorados e serviços nada.

### 3.2 Etapa 2 — o tempero

**(i) Repasse cambial a alimentos e bens industriais — mais forte que o estimado** · cenário upside
- Coeficientes: `I.IA.ia3` estimado 0,085, intervalo de 90% 0,020 a 0,153; `I.II.ii4` 0,040, intervalo 0,016 a 0,064. Multiplicador × 1,5 nos dois (0,128 e 0,060), dentro do intervalo; o de bens industriais perto da borda.
- Efeito: upside de 5,31 → 5,33 no 4T26, 5,05 → 5,11 no 1T27, 4,64 → 4,76 no 3T27, 4,53 → 4,64 no 4T27.
- Por quê: o repasse é maior quando a depreciação é de prêmio doméstico e vista como persistente, quando a inflação já está acima da meta e quando as expectativas estão acima dela (mapa 2.5) — as três condições valem se o salto de 26/10 ficar. Um salto de 9,2% num pregão também é maior que a variação trimestral típica da amostra, e o modelo é linear.
- Onde entra: limite e probabilidade do upside.

**(i) Repasse cambial mais fraco e hiato mais forte em serviços** · cenário downside
- Coeficientes: `I.IA.ia3` e `I.II.ii4` × 0,7 (0,060 e 0,028, dentro do intervalo); `I.IS.is2` estimado 0,092, intervalo 0,042 a 0,142, × 1,5 (0,138, perto da borda).
- Efeito: downside de 4,69 → 4,71 no 1T27 e 3,96 → 3,94 no 1T28 (os dois movimentos quase se anulam).
- Por quê: apreciação que só desfaz um salto é absorvida em margem; e o hiato negativo que o modelo projeta chega a serviços com um setor que já mostra volume parado (`atv_pms` · ago/26).
- Onde entra: limite do downside.

**(ii) Combustíveis — Brent e política de preços da Petrobras** · upside e downside
- Hoje: Brent 115,22 US$/barril (`comm_brent` · 20/10), média de outubro ~30% acima da do 3T26; diesel +3,70% e gasolina +0,92% no IPCA-15 de outubro (`inflc_decomposicao`).
- Por que o modelo não vê: petróleo e câmbio não entram na equação de monitorados (mapa 2.7).
- Efeito: upside, combustíveis +5% na bomba (metade em nov–dez/26, metade em jan/27) → +0,15 p.p. no 4T26 e +0,30 p.p. no 12 meses do 1T27 ao 3T27, +0,15 no 4T27 (peso de combustíveis para veículos de 6,05%, `inflc_decomposicao_item` · set/26). Downside, combustíveis −3% no 2T27 → −0,18 p.p. do 2T27 ao 1T28.
- Onde entra: limites das duas caudas; o lado do upside pesa mais na assimetria porque o Brent médio de outubro ainda não chegou à bomba.

**(ii) Bandeira tarifária de energia** · upside e downside
- Hoje: energia elétrica residencial +7,98% em setembro, −0,89% no IPCA-15 de outubro (`inflc_decomposicao`).
- Por que o modelo não vê: decisão regulatória, fora de qualquer exógena.
- Efeito: ±5% na conta em nov–dez → ±0,10 p.p. no 4T26 (peso 3,98%), devolvido no 1T27.
- Onde entra: limites do 4T26.

**(ii) Clima e safra de hortaliças — alimentos in natura** · downside (reversão); upside no tempero de expectativa abaixo
- Hoje: in natura +5,10% em setembro e +13,0% em 12 meses; tomate +24,5% no IPCA-15 de outubro.
- Por que o modelo não vê: clima e safra doméstica não estão no modelo; o IC-Br agro não carrega hortaliças.
- Efeito: downside, in natura −5% no 4T26 e −5% no 1T27 → −0,12 p.p. no 4T26, −0,24 p.p. do 1T27 ao 3T27, −0,12 no 4T27 (peso 2,38%).
- Onde entra: limite do downside. Não há série de clima no F (Faltou).

**(ii) Salários além do hiato em serviços** · upside
- Hoje: rendimento real habitual +3,7% em 12 meses, desocupação 5,3% (`mt_pnad` · ago/26).
- Por que o modelo não vê: salários não estão no modelo; só a parte que o hiato não carrega conta, para não dobrar o efeito.
- Efeito: +0,10 p.p. no 4T27 e no 1T28, quando o hiato do modelo já está negativo e o salário real ainda não terá ajustado.
- Onde entra: limite do upside nos dois últimos trimestres.

**(ii) Expectativas por componente** · assimetria do cenário base
- Hoje: Focus de alimentação no domicílio 5,76% para 2027, contra ~4% de alimentação no 12 meses que a contribuição do modelo implica no 4T27; Focus 12 meses à frente 4,53% contra 4,16% do modelo no 4T26 (`expc_focus`, `expc_focus_periodo` · 23/10).
- Por que o modelo não vê: a âncora dos quatro grupos é a Focus do IPCA cheio; a expectativa por componente não entra.
- Efeito: não movo a central; pesa na probabilidade do upside (30% contra 12% de downside do 1T27 ao 3T27).

### 3.3 Da etapa 1 à tese

| Trimestre | Central (modelo, base) | Upside: modelo → com tempero | Downside: modelo → com tempero |
|---|---|---|---|
| 4T26 | 5,28 | 5,33 → 5,58 | 5,26 → 5,04 |
| 1T27 | 4,85 | 5,11 → 5,41 | 4,71 → 4,47 |
| 2T27 | 4,33 | 4,69 → 4,99 | 4,14 → 3,72 |
| 3T27 | 4,34 | 4,76 → 5,06 | 4,12 → 3,70 |
| 4T27 | 4,23 | 4,64 → 4,89 | 3,99 → 3,69 |
| 1T28 | 4,08 | 4,34 → 4,44 | 3,94 → 3,76 |

A faixa base vai da central até pouco antes de cada cenário de cauda com tempero, um pouco mais larga para cima porque as forças de alta (câmbio já depreciado, petróleo, expectativas) já estão em curso e as de baixa dependem de reversão. O cenário de upside fica fora da faixa com ~25–30% de probabilidade e o de downside com ~10–15%; a assimetria cai no 1T28 porque o choque de combustíveis sai da janela de 12 meses.

## 4. Para os outros agentes

**Respostas às entradas fixas**

- **IN-E1 (pass-through), em destaque: a PTAX subiu 9,2% em 26/10.** No modelo, a depreciação chega primeiro a alimentos, no mesmo trimestre (`I.IA.ia3`), e a bens industriais com um trimestre de defasagem (`I.II.ii4`); serviços e monitorados não recebem nada no modelo. Uma PTAX ~0,29 R$ acima da base por todo o horizonte soma +0,10 p.p. ao IPCA 12m no 1T27 e +0,18 no 3T27; com o repasse × 1,5, +0,16 e +0,29. Fora do modelo, a depreciação chega a combustíveis pela paridade da Petrobras (com defasagem de política), a medicamentos no reajuste anual e, pela indexação, a contratos e monitorados no ano seguinte: com combustíveis 5% mais caros, mais +0,30 p.p. por quatro trimestres. O câmbio usado é o do cenário, não uma tese; a persistência vem do agente de câmbio (IN-S1).
- **IN-E2 (câmbio):** a tese da seção 1; a cauda de alta vem de alimentos e combustíveis e depende do próprio câmbio.
- **IN-E3 (política monetária):** 4,08% no 1T28 (horizonte relevante), faixa 3,80–4,40, upside 25% contra 15% de downside; o choque corrente é de primeira ordem, e a segunda ordem está em risco por serviços subjacentes e expectativas (Q2).
- **IN-E4 (atividade):** alimentação contribui 0,96 p.p. no 4T26 e cai a ~0,6 p.p. de 2T27 em diante; monitorados 1,37 p.p. no 4T26 e ~1,0 p.p. depois. A cauda de alta está nesses dois grupos, os que mais pesam no consumo de baixa renda.
- **IN-E5 (atividade):** serviços subjacentes acumulam 5,32% em 12 meses, contra 5,00% três meses antes, com volume de serviços parado e hiato do BC caindo — serviços estão acima do que o hiato explicaria, o que aponta para inércia e salário, ou para um hiato medido baixo demais.
- **IN-E6 (fiscal):** a tese da seção 1; IPCA no trimestre de 1,27% no 4T26, 1,51% no 1T27, 0,91% no 2T27 (modelo, base).
- **IN-E7 (fiscal):** a central não supõe nenhuma decisão de governo sobre preços; as caudas supõem a Petrobras repassando (upside) ou reduzindo (downside) o preço, sem mudança de tributo. Um corte de imposto sobre combustível entraria como downside e custo adiado.
- **IN-E8 (externo):** a tese depende mais do agro que dos metais: +10% no IC-Br agropecuária em US$ somam +0,19 a +0,25 p.p. ao IPCA 12m do 4T26 ao 3T27; +10% nos metais, +0,04 a +0,19 p.p., crescendo ao longo do horizonte. A cauda de alta depende do Brent (fora do modelo).
- **IN-E9 (expectativas):** a central sobe a 5,28% em dezembro por efeito-base (sai o 4T25 de 0,60%), não por aceleração; saem da janela o 1T26 (1,92%) e o 2T26 (1,42%), o que derruba o 12 meses no 1T27 e no 2T27. Energia e in natura são choques de primeira ordem.
- **IN-E10 (expectativas):** setembro 0,82% contra 0,56% da QPC (energia); IPCA-15 de outubro 0,32% contra 0,34% esperado para o IPCA do mês; serviços subjacentes acima da mediana nos dois.

**Pedidos**

- **IN-S1 (câmbio):** a PTAX de fechamento por trimestre, 4T26 a 1T28, e se o salto de 9,2% em 26/10 é persistente. A central do 4T26–1T27 e a probabilidade do upside dependem disso: a central de hoje supõe ~5,21 em dezembro.
- **IN-S2 (câmbio):** o salto de 26/10 é idiossincrático (prêmio doméstico) ou global? Qual a probabilidade de a PTAX fechar o 4T26 acima de 5,50? Decide o multiplicador × 1,5 do repasse.
- **IN-S3 (política monetária):** o caminho da Selic por reunião até o 2T27, e se a depreciação de 26/10 muda a decisão de novembro. A central do 1T28 depende dele.
- **IN-S4 (política monetária):** os condicionantes da projeção do Copom na R281 — petróleo, bandeira, câmbio e a projeção de monitorados por trimestre. Explica a diferença de 0,9 p.p. contra o modelo no 1T28.
- **IN-S5 (atividade):** o hiato por trimestre, e se a pressão de demanda em serviços está nos prestados às famílias (+4,2% em 12 meses) ou no mercado de trabalho. Decide o tempero de salário e o multiplicador de `I.IS.is2`.
- **IN-S6 (fiscal):** medidas sobre preço de combustível e energia (PIS/Cofins, ICMS, subvenção ao diesel), com data, anunciadas ou em discussão depois de 26/10. Decide a cauda de baixa de monitorados.
- **IN-S7 (externo):** os caminhos de `icbr_agr_usd` e `icbr_met_usd` por trimestre, base e caudas.
- **IN-S8 (externo):** o caminho do Brent por trimestre e se a queda desde 02/10 (de 135,51 para 115,22) é reversão do choque ou ruído. Decide o tempero de combustíveis.
- **IN-S9 (expectativas):** o caminho da Focus 12 meses por trimestre. O modelo dá 4,16% de média no 4T26 com a Focus em 4,53% em 23/10: a equação (E) está descendo rápido demais? Se sim, os quatro grupos ficam mais altos em 2027 (multiplicador de `E.e1` é do agente de expectativas).
- **IN-S10 (expectativas):** a Focus de alimentação no domicílio subiu 0,53 p.p. em quatro semanas para 2026 e está em 5,76% para 2027, contra ~4% no modelo. O que move isso, e vai durar?

**Ao agente web**

- Bandeira tarifária da ANEEL para novembro e dezembro de 2026 e o motivo da alta de setembro (+7,98%). Tese: limites do 4T26.
- Reajustes da Petrobras em gasolina, diesel e GLP desde setembro de 2026 e a defasagem contra o preço internacional com o Brent entre 115 e 135. Tese: tempero de combustíveis, 4T26–1T27.
- Medidas anunciadas sobre tributos de combustível ou energia, ou subsídio ao diesel, desde 25/10. Tese: cauda de baixa de monitorados.
- Preços de hortaliças no atacado (tomate, batata, cebola) em outubro e a perspectiva de oferta para novembro–dezembro (chuva, safra). Tese: reversão dos in natura no downside.
- Reajuste dos planos de saúde individuais (ANS, ciclo 2026–27) e reajustes de ônibus urbano já anunciados para jan/2027 nas capitais. Tese: inércia dos monitorados no 1T27.

**Como subordinado**

- `icbr_agr_usd` · principal: externo
  - Insumos: a pressão doméstica em alimentos é de hortaliças, fora da cesta do IC-Br: in natura +13,0% em 12 meses, semi-elaborados +6,1%, industrializados +0,3% (`inflc_decomposicao` · set/26). Entre os produtos de commodity, o arroz subiu 5,8% no IPCA-15 de outubro (`inflc_decomposicao`). O IC-Br agro em reais subiu 3,3% do 2T26 para o 3T26 (`comm_icbr`), quase todo câmbio. Sensibilidade: +10% no caminho somam +0,19 a +0,25 p.p. ao IPCA 12m do 4T26 ao 3T27 — é onde a precisão do principal mais rende.
  - Argumento: os preços domésticos de alimentos não dão razão para mover o caminho; a safra e o clima que mexeriam com soja, milho, café e carnes não estão no F (pedido ao agente web). Peço ao principal que diga se o Brent alto (fertilizante e diesel) entra no caminho.
  - Caminho de referência: nenhum.
- `icbr_met_usd` · principal: externo
  - Insumos: com o IC-Br metal em US$ +42,2% em 12 meses, o núcleo EX3 de industriais desacelerou de 4,15% para 3,70% em 12 meses e bens industriais acumulam 3,07% (`inflc_agregados` · set/26); automóvel novo caiu 0,35% em setembro (`inflc_decomposicao`). Os metais não chegaram ao consumidor até aqui. Sensibilidade: +10% somam +0,04 a +0,19 p.p. ao IPCA 12m, crescendo até o 3T27.
  - Argumento: nada a acrescentar ao caminho neste ciclo; se o principal subir o caminho, eu leria o efeito do modelo como teto, dado o repasse que os preços não mostram.
  - Caminho de referência: nenhum.

## 5. Placar

Primeiro ciclo.

## 6. Sobre o modelo

| Fonte | O que sugere | Teste proposto | Por que importa para a tese deste ciclo |
|---|---|---|---|
| Mapa 2.7 e o F deste ciclo (Brent +30% em um mês; diesel +3,70% no IPCA-15) | Petróleo em reais (Brent × PTAX, ou o IC-Br energia em R$) como regressor da equação de monitorados, com defasagem de um trimestre, e o IPCA livre no lugar do cheio na indexação (`I.IM.im2`) | Monitorados trimestral, 2003–2026, com e sem a variação do Brent em reais defasada e com o IPCA livre defasado; muda a especificação se o coeficiente do petróleo for positivo com intervalo fora de zero e o sinal da indexação se acertar | O choque de petróleo e câmbio deste ciclo não aparece em monitorados no modelo; hoje ele vive todo no tempero |
| Mapa 2.6 e o F (in natura +13,0% em 12 meses, IC-Br agro em US$ de lado) | Separar in natura do resto de alimentação, ou um termo de clima na equação de alimentação | Alimentação trimestral dividida em in natura e restante, 2006–2026; muda se o ajuste da parte sem in natura melhorar e `I.IA.ia2` subir | O choque de alimentos atual não é commodity e o modelo o trata só como inércia |
| O cenário base deste ciclo (Focus do modelo 4,16% no 4T26 contra 4,53% observada em outubro) | Usar no trimestre em curso o dado que já saiu dentro dele (Focus semanal, IPCA-15, PTAX diária) em vez de partir só do último trimestre fechado | Erro do primeiro trimestre projetado com e sem esse dado parcial, nas projeções fora da amostra de 2015–2026 | A central do 4T26–1T27 supõe expectativa e câmbio que já estão longe do observado em outubro |
| Mapa 2.3 e Focus por componente (alimentação 2027 5,76%, bens industriais 2,71%) | Âncora por componente em vez da Focus do IPCA cheio para os quatro grupos | Equação (I) com a Focus de cada componente como âncora, 2021–2026 (amostra curta); muda se o ajuste de alimentação e industriais melhorar | A Focus põe mais inflação em alimentação e menos em industriais do que o modelo |

[^1]: Núcleo é uma medida que tira ou suaviza os itens mais voláteis do IPCA para mostrar a tendência. O EX3 exclui alimentos e monitorados, entre outros; a média aparada corta os extremos da distribuição de variações do mês.
[^2]: Difusão é a fatia dos subitens do IPCA que subiram no mês. Uma alta de inflação com difusão baixa vem de poucos itens.
[^3]: Serviços subjacentes são os serviços sem os itens mais voláteis (passagem aérea, alimentação fora de casa e outros) e os mais ligados a salário e demanda doméstica. O número do IPCA-15 aqui foi refeito pelos subitens com a marca de subjacente da classificação do BC; a QPC pergunta pelo IPCA do mês, então a comparação é aproximada.
[^4]: Efeito de primeira ordem é a alta do próprio item que sofreu o choque (a energia, o tomate). O de segunda ordem é a alta se espalhar para outros preços e salários, por indexação ou por expectativa; é a esse que o Banco Central reage. Pass-through é a fatia de uma variação do câmbio que chega aos preços ao consumidor.
[^5]: A bandeira tarifária é um adicional na conta de luz definido pela ANEEL todo mês, mais caro quando a geração custa mais (reservatório baixo, térmicas ligadas). Por isso a energia sobe e devolve de um mês para o outro.
[^6]: O IPCA de 12 meses muda tanto pelo mês que entra quanto pelo que sai da janela. Quando sai um trimestre muito baixo, o 12 meses sobe mesmo que a inflação do trimestre novo seja normal: é o efeito-base.
[^7]: Nesta rodada não li os reports dos outros agentes nem notícias (rodada 1). Nenhuma exógena tem caminho de principal ainda; a central usa o padrão do simulador, e o CDS das caudas só existe para levar a PTAX ao nível de 26/10.
[^8]: A faixa do posterior mostra só a incerteza sobre os pesos estimados do modelo, não a incerteza da previsão; a faixa da tese, na seção 1, é a do agente.
