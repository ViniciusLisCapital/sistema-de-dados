# Report — política monetária · ciclo 2026-10-02 · rodada 1

Dados até: 02/10/2026[^corte] · Horizontes: 4T26 a 1T28, os seis trimestres do Modelo Estrutural a partir do trimestre em curso · Variável: meta Selic no fechamento do trimestre, a decisão da última reunião do Copom dentro dele (`pm_copom_calendario`)

## 1. Tese

| Variável | Trimestre | Central | Base: faixa · P | Upside: limite · P | Downside: limite · P | P(up) − P(down) |
|---|---|---|---|---|---|---|
| Meta Selic, fechamento do trimestre (% a.a.) | 4T26 | 13,10 | 13,00 a 13,50 · 47% | acima de 13,50 · 53% | abaixo de 13,00 · 0% | +0,53 |
| | 1T27 | 12,78 | 12,75 a 13,50 · 53% | acima de 13,50 · 46% | abaixo de 12,75 · 1% | +0,45 |
| | 2T27 | 12,50 | 12,50 a 13,50 · 65% | acima de 13,50 · 32% | abaixo de 12,50 · 3% | +0,29 |
| | 3T27 | 12,25 | 12,25 a 13,25 · 57% | acima de 13,25 · 37% | abaixo de 12,25 · 6% | +0,31 |
| | 4T27 | 12,04 | 12,00 a 13,00 · 51% | acima de 13,00 · 40% | abaixo de 12,00 · 9% | +0,31 |
| | 1T28 | 11,85 | 11,75 a 13,00 · 56% | acima de 13,00 · 32% | abaixo de 11,75 · 12% | +0,20 |

A central é a Selic de fechamento que o Modelo Estrutural dá no cenário base, sem ajuste[^fim]; faixa, limites e probabilidades são meus, lidos da trajetória reunião a reunião abaixo. A distância entre as duas é o assunto da tese: o modelo fecha 2026 em 13,10%, entre o que dariam dois cortes de 25 p.b. (13,25%) e um de 50 seguido de um de 25 (13,00%) (G `pm_calendario`); eu espero que o Copom pare.

**Reunião a reunião, 4T26 e 1T27** (probabilidade de cada passo, sem condicionar ao passo anterior[^arvore]):

| Reunião | Decisão | −50 p.b. | −25 p.b. | manter | +25 p.b. |
|---|---|---|---|---|---|
| 282ª | 04/11/2026 | 1% | 39% | **55%** | 5% |
| 283ª | 09/12/2026 | 1% | 24% | **67%** | 8% |
| 284ª | 27/01/2027 | 1% | 19% | **70%** | 10% |
| 285ª | 17/03/2027 | 1% | 18% | **70%** | 11% |

Fechamento que essa trajetória dá: no 4T26, 13,75% com 44%, 13,50% com 29%, 13,25% com 16%, 13,00% com 2%, 14,00% ou mais com 9% (média 13,61%); no 1T27, 13,75% com 30%, 13,50% com 26%, 13,25% com 16%, 13,00% ou menos com 13%, 14,00% ou mais com 16% (média 13,56%). São esses pontos que dão a faixa e as caudas das duas primeiras linhas da tese.

- **Upside (Selic acima da faixa)**, ruim para o Brasil: o petróleo fica acima de US$ 120, aparecem efeitos de segunda ordem e o real e o CDS pioram. No modelo, juro real de 10 anos a 8,05%, CDS a 180 e dólar contra emergentes 4% mais forte dão 13,52% no 4T26 e 12,49% no 1T28; com a reação da regra à expectativa × 1,35 e o tempero do petróleo (+25 a +50 p.b.), 13,95% e 13,21%.
- **Downside (Selic abaixo da faixa)**, bom se vier pela via provável: o petróleo devolve, o ciclo global desacelera e as commodities caem 8%. No modelo, juro real de 10 anos a 7,20% e CDS a 115 dão 12,85% no 4T26 e 11,37% no 1T28; com a reação à expectativa × 0,75, 12,72% e 11,09%. A outra via, um Copom que corta com expectativas desancoradas, é downside ruim e está nas caudas de 0% a 3% até o 2T27.

**A tese em uma frase:** o Copom encerra (ou suspende) o ciclo de calibração em 13,75% já em novembro, com 55%, e fica parado até o 1T27 enquanto o choque do petróleo não devolver; o Modelo Estrutural, que lê a queda do juro real de 10 anos como espaço para cortar e não conhece o calendário nem o petróleo, põe a central em 13,10% no fim de 2026, e por isso a distribuição pende para cima em todo o horizonte, de +0,53 no 4T26 a +0,20 no 1T28.

## 2. Argumentação

### Q1 — O que o Copom vai fazer

Manter 13,75% em 04/11 é o passo mais provável (55%), contra 39% de mais um corte de 25 p.b.; depois de uma parada, a manutenção é o padrão até o 1T27. A previsão tem três partes.

**A projeção que sustentou o corte de setembro ficou para trás.** O Copom cortou com IPCA projetado de 3,2% no 1T28, o horizonte relevante[^hr] (`pm_copom_projecoes` · RPM de 24/09), já acima da meta de 3,00% (`inflc_meta` · 2026). Essa projeção supunha Selic de 13,75% no fim de 2026, Brent partindo de US$ 90 de média no 3T26, com pico no 4T26 e queda a cerca de US$ 84 no 2T27, e câmbio partindo de R$ 5,15 (RPM set/26, 2.2; comunicado da 281ª)[^cond]. Desde a reunião, as três hipóteses andaram contra a projeção: a Focus passou a pôr 13,50% em novembro e dezembro (`expc_focus_copom` · 25/09; era 13,75% em 11/09), o Brent fechou a US$ 135,51 (`comm_brent` · 02/10), 51% acima do ponto de partida do RPM[^brent], e a PTAX a R$ 5,2238 (`cmb_ptax` · 02/10), 1,4% acima do condicionante. Refeita com esses insumos, a projeção sobe; com ela já acima da meta, o Copom perde o argumento que usou para cortar ("compatível com a estratégia de convergência", ata da 281ª, §18). Mas as expectativas longas não pioraram desde a reunião: a Focus para 2028 estava em 3,80% em 11/09 e continuou em 3,80% em 25/09 (`expc_focus_periodo` IPCA), e é isso que teria de piorar de novo para a alta entrar no cenário base.

**A doutrina do próprio Copom aponta para parar, não para subir.** A ata diz que expectativas desancoradas exigem "uma restrição monetária maior e por mais tempo do que outrora seria apropriado" (ata da 281ª, §10), e que o Comitê "não deve reagir aos efeitos primários" de choques de oferta, mas reagirá "com firmeza" aos de segunda ordem (§16). O boxe do RPM conclui que o choque do petróleo "ainda não gerou propagação inflacionária relevante" por segunda ordem, mas que os riscos "não podem ser descartados", com condições iniciais menos benignas: inflação perto do teto, expectativas desancoradas, hiato positivo (RPM set/26, boxe de efeitos de segunda ordem). Parar é a resposta que concilia as duas frases; subir exige ver segunda ordem, e por isso a alta fica em 5% em novembro.

**O histórico diz como um ciclo de corte termina no Brasil.** Dos seis ciclos de corte encerrados desde 2005, cinco terminaram num corte de 25 p.b. seguido de manutenções, e nenhum teve uma pausa de uma reunião seguida de retomada (`pm_copom_reuniao`, 2005 a 2026; a única pausa entre dois cortes é de 1999). Por isso uma parada em novembro tende a durar, e a árvore dá 67% a 70% de manutenção de dezembro a março. Um desses seis, o de 2023-24, foi revertido: corte de 25 p.b. em 08/05/2024, duas manutenções e alta em seguida (`pm_copom_reuniao`), o precedente das caudas de alta da árvore.

Contra a parada: o Copom cortou 25 p.b. em cinco reuniões seguidas desde 18/03 (`pm_copom_reuniao`), começando já com o conflito no Oriente Médio em curso (comunicado da 277ª), e a atividade desacelera, com PIB de +0,5% no 2T26 contra o 1T26 e consumo das famílias de −0,4% (`atv_pib_taxas` · 2T26) e produção industrial de −0,6% em agosto (`atv_pim` · ago). O juro real ex-ante de 8,70% está 3,70 p.p. acima do neutro que o Copom usa (Q2). E o mercado espera o corte (Q3). O corte de novembro passa a ser o mais provável se, até a semana anterior à reunião, o Brent voltar para perto dos US$ 115 de 25/09 a 01/10 (`comm_brent`) e a PTAX para perto de R$ 5,15.

### Q2 — O que o Copom deveria fazer, pelos dados

Manter 13,75% em novembro e até o 1T27, e só voltar a cortar quando o petróleo devolver sem segunda ordem. A política já é restritiva por qualquer neutro; o que os dados pedem é não continuar cortando durante um choque de oferta com expectativas desancoradas.

**A postura é restritiva por qualquer neutro.** Com a Focus de 12 meses em 4,65% (`expc_focus` · 25/09), a Selic real ex-ante é 8,70%[^neutro]:

| Medida | Valor | Selic real ex-ante acima dele |
|---|---|---|
| Neutro do Copom, cenário de referência (RPM set/26, 2.2) | 5,00% | +3,70 p.p. |
| Neutro do QPC, 2 anos (`expc_qpc` · R279) | 6,00% | +2,70 p.p. |
| Neutro do QPC, 5 anos (`expc_qpc` · R279) | 5,50% | +3,20 p.p. |
| Neutro do QPC, curto prazo (`expc_qpc` · R279) | 6,40% | +2,30 p.p. |
| Âncora do Modelo Estrutural, NTN-B 10 anos (`br_interest_rate` · 02/10) | 7,51% | +1,19 p.p. |
| DI de 1 ano contra a Focus de 12 meses (`br_interest_rate` · 25/09) | 8,56% | — |

Uso o neutro do QPC de 2 anos, 6,00%: o de 5,00% do Copom é uma convenção do cenário de referência, que o próprio Copom testa contra alternativas (RPM 2.2) e diz estar sendo empurrado para cima por disciplina fiscal fraca, crédito direcionado e incerteza da dívida (ata da 281ª, §8); a âncora do modelo é um juro de mercado com prêmio de prazo e fiscal dentro (mapa, 2.5)[^ancora]. Mesmo contra 6,00%, a política está 2,70 p.p. acima do neutro.

**Mas a inflação ainda não dá espaço.** O IPCA de 12 meses estava em 4,22% em agosto, baixo pelo bônus de Itaipu (−0,32% no mês), e o IPCA-15 de setembro veio a 0,70%, com 4,47% em 12 meses (`inflc_agregados` · ago e set); o Copom projeta 5,2% no 4T26 e dá 90% de chance de passar o teto de 4,50% no fim de 2026 (RPM 2.2, Tabela 2.2.2)[^meta]. A parte que a política alcança está acima da meta: serviços com 5,46% em 12 meses e a média dos seis núcleos com 4,37% (`inflc_agregados` · ago). O hiato é positivo, 0,41% no 3T26 (`pm_hiato_produto` · RPM set/26), a desocupação está em 5,3% (`mt_pnad` · ago) e o rendimento real habitual cresce 3,7% em 12 meses (`mt_pnad` · ago), acima da produtividade, como diz a ata (§7). As expectativas estão acima da meta em todos os horizontes: 4,31% para 2027, 3,80% para 2028 e 3,50% para 2029 (`expc_focus_periodo` · 25/09). A leitura de inflação, hiato e ancoragem é dos agentes de inflação, atividade e expectativas (aguarda S8, S10, S9); o que é meu é o que ela pede da Selic: num choque de oferta com essas condições iniciais, cortar agora aumenta o custo da segunda ordem que a ata §10 descreve, e manter custa um trimestre a mais com a política 2,70 p.p. acima do neutro e o hiato fechando.

**A transmissão está enfraquecida no crédito direcionado**, o que pede juro alto por mais tempo, não mais alto. Premissa assumida (crédito, TWA): o saldo total cresce 9,2% em 12 meses (`cred_credito_resumo` · ago), puxado pelo direcionado, com imobiliário +13,8% (`cred_modalidade_direcionado_pf` · ago), BNDES +10,3% e rural PJ +30,6% (`cred_modalidade_direcionado_pj` · ago), como a ata descreve (§6). Mas a política está chegando às famílias: a inadimplência do crédito livre PF subiu a 8,01% (+1,04 p.p. em 12 meses) e a taxa a 61,74% (`cred_credito_resumo` · ago).

**A distância entre Q1 e Q2.** Eu manteria com certeza; espero que o Copom mantenha com 55%. Os 39% de corte em novembro são o risco de um Copom que corta à frente dos dados, e esse risco alimenta a cauda de cima mais adiante, não a de baixo agora: cortar dentro do choque aumenta a chance de ter de reverter, como em 2024. É por isso que a árvore mantém de 8% a 11% de alta por reunião até março.

### Q3 — O que o mercado precifica, e onde diverge

| Reunião | Curva DI (02/10) | Passo implícito | Focus, mediana (25/09) | QPC, "fará" (23/09) | Este report (passo mais provável) |
|---|---|---|---|---|---|
| 282ª · 04/11/26 | 13,60% | −15 p.b. | 13,50% | manter, 53% das respostas; média −12 p.b. | manter, 55% |
| 283ª · 09/12/26 | 13,54% | −6 p.b. | 13,50% | manter, 66%; média −9 p.b. | manter, 67% |
| 284ª · 27/01/27 | 13,55% | +1 p.b. | 13,50% | — | manter, 70% |
| 285ª · 17/03/27 | 13,57% | +1 p.b. | 13,25% | — | manter, 70% |
| 287ª · 16/06/27 | 13,58% | +1 p.b. | 13,00% | — | fechamento médio 13,39% |
| 291ª · 08/12/27 | 13,95% | +16 p.b. | 12,00% | — | fechamento médio 12,96% |

Fontes: `br_di_grade` (02/10), `expc_focus_copom` (25/09), `expc_qpc` (R281). A curva é preço, com prêmio de prazo[^premio]; a Focus é a mediana.

**Contra o que eu espero do Copom (Q1):** a curva e a Focus põem um corte em novembro como mais provável que não; eu ponho 39%. Há espaço para surpresa dura em 04/11. O QPC, respondido depois da ata, está mais perto de mim: 53% dizem que o Copom manterá e 61% que deveria manter (`expc_qpc` · R281).

**Contra o que os dados pedem (Q2) e contra o próprio Copom:** depois de março, a curva sobe e a Focus desce. A distância entre as duas chega a +195 p.b. na reunião de dezembro de 2027 (G sobre `br_di_grade` e `expc_focus_copom`): a Focus espera 12,00% e a curva cobra 13,95%, acima da Selic de hoje. Parte disso é prêmio; parte é o mercado pagando por uma reversão em 2027, que é a cauda de cima deste report. E o mercado não acredita na projeção do Copom: a mediana do QPC para o IPCA no 1T28 é 4,00% (p25 a p75 de 3,77% a 4,20%[^pctl], `expc_qpc` · R281), contra 3,2% do Copom. O próprio modelo, com a Selic caindo a 11,85%, dá IPCA de 4,08% no 1T28 (seção 3.1). A inflação implícita nos títulos de 2 e 10 anos estava em 5,95% em 25/09 e a de 10 anos foi a 6,18% em 02/10 (G sobre `br_interest_rate`, DI contra NTN-B); a conclusão sobre o que ela diz de ancoragem é do agente de expectativas (S9).

### Q4 — O cenário para a Selic: por que a central e por que a distribuição

**A central é do modelo, e a história que ele conta é a do juro de equilíbrio.** Com o juro real de 10 anos segurado em 7,51% (o último pregão, `br_interest_rate` · 02/10) em vez de 7,84% (a média do 3T26, o padrão do simulador), a âncora da regra, juro real de 10 anos mais a meta, cai de 10,84% para 10,51%, e a regra passa essa queda para a Selic no mesmo trimestre: o fechamento do 4T26 vai de 13,43% para 13,10% e o do 1T28 de 12,18% para 11,85% (G `pm_cenarios_r1`). O argumento econômico do modelo é o do mapa (2.5): um juro real longo mais baixo é um juro de equilíbrio mais baixo, a mesma Selic fica mais apertada, e há espaço para cortar sem afrouxar. O hiato sai igual nos dois cenários, 0,13% no 4T26 e −0,51% no 1T28, porque a distância entre a Selic e a âncora é a mesma. Daí em diante a regra corta devagar, com inércia (t1 1,34, t2 −0,48), porque a Focus que ela lê cai de 4,37% para 3,52% no 1T28.

**Onde o modelo erra neste ciclo, e por que isso põe a distribuição para cima.**

1. **A queda do juro real longo não foi compressão do prêmio fiscal.** De 30/06 a 02/10, a NTN-B de 10 anos caiu cerca de 0,5 p.p. (de 8,04% para 7,51%), mas o DI de 10 anos ficou em 14,15% e a inflação implícita de 10 anos subiu cerca de 0,5 p.p., de 5,66% para 6,18% (G `pm_leituras` sobre `br_interest_rate`); o CDS subiu de 124,8 para 131,0 (`cmb_risco_pais`). O juro nominal longo não caiu: o que mudou foi a parte que paga inflação, no meio de um choque do petróleo. A âncora do modelo usa a meta (3,00%), não a inflação que o mercado cobra, e lê um choque de oferta como espaço para cortar. A história do mapa 2.5, uma consolidação fiscal precificada, exigiria CDS e juro nominal em queda, e os dois não caíram. A leitura do prêmio fiscal é do agente fiscal (S11), e ela pode mudar este item.
2. **A regra não conhece o calendário.** 35 dos 92 dias do 4T26, 38% do trimestre, já estão em 13,75% até a 282ª (G `pm_calendario` sobre `pm_copom_calendario`). A média de 13,27% que o modelo dá ao 4T26 exige mais de 50 p.b. em cada uma das duas reuniões (−50 e −50 dariam média de 13,32%), depois de cinco cortes de 25 p.b.
3. **O modelo parte de expectativas mais baixas que as do corte.** A (E) parte da média da Focus no 3T26, 4,37%, e projeta 4,16% para o 4T26, quando a pesquisa estava em 4,65% em 25/09 (`expc_focus`). A equação é do agente de expectativas (S9).
4. **O petróleo não está no modelo.** A curva de Phillips de monitorados tem só inércia e o IPCA anterior (`modelo.listar`, I.IM), sem combustível nem Brent (seção 6). O choque entra pelo tempero (ii).

Nenhum desses quatro move a central, pela regra do sistema; todos entram na assimetria. A média da minha trajetória de reuniões é 13,61% no 4T26 e 12,74% no 1T28 (G `pm_reunioes`), acima da central em todo o horizonte. A assimetria cai de +0,53 para +0,20 porque, com o tempo, a central do modelo se aproxima da Focus (12,04% contra 12,00% no fim de 2027) e a cauda de baixo ganha a via do petróleo devolvido. O upside é ruim para o Brasil: Selic acima da faixa significa segunda ordem do petróleo, desancoragem ou prêmio de risco maior. O downside provável é bom (petróleo e commodities devolvendo); o ruim, um Copom que corta sem a inflação deixar, está nas caudas pequenas de 0% a 3% até o 2T27.

### Olhado, sem sinal

- Posição de swaps do BC · −US$ 91,6 bi (`cmb_reservas_bc` · ago) · estável, +1,3 em 1 mês · diria algo se o BC ampliasse a oferta acima dos vencimentos, que é uma resposta ao câmbio fora da Selic.
- Juro de política dos pares · México 6,50%, Chile 4,50%, Peru 4,25% sem mudança em 1 mês; Colômbia 12,25%, +0,25 (`inter_interest_rate` · 02/10) · um par só subiu · diria algo se dois ou mais emergentes subissem juros pelo petróleo, um ciclo global de aperto (S13).
- Posicionamento em real · fundos alavancados com 9.553 contratos líquidos (`cmb_cot_fx` · 29/09) · posição pequena · diria algo se uma posição grande se desfizesse perto da reunião (S5).
- Termos de troca · 111,35 (`cmb_termos_troca` · jul) · 93 dias de defasagem · diria algo com a leitura de setembro, se o petróleo os mover.
- Condições de crédito (PTC) · oferta PF consumo −0,23 (`cred_ptc` · 2T26) · 184 dias de defasagem · diria algo na edição do 3T26.
- Dívida bruta · 82,9% do PIB, +5,6 p.p. em 12 meses (`fisc_divida` · ago) · move devagar e é do fiscal · diria algo se mudasse a trajetória que o mercado precifica (S11, S12).
- Endividamento das famílias · 49,86% da renda (`cred_credito_familias` · jul) · estável em 3 meses · diria algo se o comprometimento com juros, 10,83%, acelerasse.

## 3. Premissas

### 3.1 Etapa 1 — o modelo

**Cenários.**
- **Base:** o Brent fica alto no 4T26 e devolve devagar em 2027; o real e o CDS ficam onde estão em 02/10; o juro real de 10 anos não muda; a meta continua em 3,00%. Os dois turnos da eleição, em 04/10 e 25/10, não mudam o prêmio de risco de forma persistente[^eleicao].
- **Upside:** o Brent segue acima de US$ 120, a segunda ordem aparece em serviços e salários, a leitura fiscal e eleitoral piora, o real se deprecia e o juro real longo volta ao nível de 30/06.
- **Downside:** um acordo no Oriente Médio devolve o petróleo, a economia global desacelera, as commodities caem e o juro real longo cai junto com o prêmio de risco.

**Caminhos das exógenas.** Trimestre a trimestre, depois do último valor escrito vale o mesmo valor (o simulador segura). As exógenas que não estão aqui ficam no padrão do simulador.

| Exógena | Hoje (valor · tabela · data) | Cenário | 4T26 | 1T27 | 2T27 | 3T27 | 4T27 | 1T28 |
|---|---|---|---|---|---|---|---|---|
| Meta de inflação, 12 meses (`meta_12m`) · tutela pm, nível 1 · próprio | 3,00 · `inflc_meta` · 2026 | base · upside · downside | 3,00 | 3,00 | 3,00 | 3,00 | 3,00 | 3,00 |
| Juro real de 10 anos (`rr_10a`) · tutela pm, nível 2 (fiscal, nível 1) · próprio | 7,51 · `br_interest_rate` · 02/10 (média do 3T26: 7,84) | base | 7,51 | 7,51 | 7,51 | 7,51 | 7,51 | 7,51 |
| | | upside | 7,80 | 8,05 | 8,05 | 8,05 | 8,05 | 8,05 |
| | | downside | 7,35 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 |
| CDS 5 anos (`fiscal`) · aguarda fiscal (S11) | 131 · `cmb_risco_pais` · 02/10 | base (padrão) | 131 | 131 | 131 | 131 | 131 | 131 |
| | | upside | 160 | 180 | 180 | 180 | 180 | 180 |
| | | downside | 120 | 115 | 115 | 115 | 115 | 115 |
| Dólar contra emergentes (`dxy_em`) · aguarda externo (S13) | 129,71 · `cmb_dollar_index_em` · 02/10 (fechamento do 3T26 no modelo: 129,38) | base (padrão) | 129,38 | 129,38 | 129,38 | 129,38 | 129,38 | 129,38 |
| | | upside | 131,97 | 134,55 | 134,55 | 134,55 | 134,55 | 134,55 |
| IC-Br agropecuária em US$ (`icbr_agr_usd`) · aguarda externo (S13) | 200,53 · média do 3T26 no modelo (`comm_icbr_usd`) | base (padrão) | 200,53 | 200,53 | 200,53 | 200,53 | 200,53 | 200,53 |
| | | downside | 192,51 | 184,48 | 184,48 | 184,48 | 184,48 | 184,48 |
| IC-Br metal em US$ (`icbr_met_usd`) · aguarda externo (S13) | 330,14 · média do 3T26 no modelo (`comm_icbr_usd`) | base (padrão) | 330,14 | 330,14 | 330,14 | 330,14 | 330,14 | 330,14 |
| | | downside | 316,94 | 303,73 | 303,73 | 303,73 | 303,73 | 303,73 |
| Fed funds efetivo (`ffr`) · aguarda externo (S13) | 3,75 no modelo (3T26); meta, ponto médio, 3,88 · `us_interest_rate` · 02/10 | base · upside · downside (padrão) | 3,75 | 3,75 | 3,75 | 3,75 | 3,75 | 3,75 |

- **Meta:** a meta é contínua, 3,00% desde 2025 (`inflc_meta`), e nenhum documento do Copom lido aponta mudança pelo CMN.
- **Juro real de 10 anos, base:** o último pregão, segurado. Não projeto queda nem alta porque os dois lados têm força: a inflação implícita subindo empurra a NTN-B para baixo, e o Fed e o CDS subindo a empurram para cima (Treasury de 10 anos a 5,28%, +0,79 p.p. em 3 meses, `us_interest_rate` · 02/10). Upside: volta a 8,05%, perto de 8,04% em 30/06 (G `pm_leituras`); downside: 7,20%, perto do mínimo de 2025-26, 7,16%.
- **CDS, dólar contra emergentes e IC-Br:** caminhos de cauda escritos por mim para ilustrar os cenários; não tenho a tutela e eles não entram no P. O `ffr` padrão do simulador é o efetivo do 3T26; a alta do Fed em setembro (meta a 3,88%) ainda não está nele, e o caminho é do agente externo.

**Saída do modelo** (central dos pesos da mediana; G `pm_cenarios_r1`)[^faixa]:

| Variável | Cenário | 4T26 | 1T27 | 2T27 | 3T27 | 4T27 | 1T28 |
|---|---|---|---|---|---|---|---|
| Selic, fechamento (% a.a.) | base | 13,10 | 12,78 | 12,50 | 12,25 | 12,04 | 11,85 |
| | base, faixa de 90% dos pesos | 12,77 a 13,40 | 12,23 a 13,29 | 11,80 a 13,16 | 11,48 a 13,05 | 11,24 a 12,93 | 11,10 a 12,79 |
| | upside | 13,52 | 13,33 | 13,07 | 12,85 | 12,66 | 12,49 |
| | downside | 12,85 | 12,43 | 12,12 | 11,83 | 11,58 | 11,37 |
| | padrão do simulador (`rr_10a` 7,84) | 13,43 | 13,11 | 12,83 | 12,58 | 12,37 | 12,18 |
| Selic, média do trimestre (% a.a.) | base | 13,27 | 12,92 | 12,63 | 12,37 | 12,14 | 11,94 |
| IPCA 12 meses (%) | base | 5,28 | 4,85 | 4,34 | 4,35 | 4,23 | 4,08 |
| | upside | 5,30 | 4,95 | 4,51 | 4,57 | 4,47 | 4,28 |
| | downside | 5,18 | 4,59 | 3,99 | 3,95 | 3,88 | 3,84 |
| Focus IPCA 12 meses, média (%) | base | 4,16 | 3,98 | 3,78 | 3,67 | 3,59 | 3,52 |
| Hiato (% do potencial) | base | 0,13 | −0,08 | −0,24 | −0,36 | −0,45 | −0,51 |
| PTAX, fechamento (R$/US$) | base | 5,22 | 5,26 | 5,26 | 5,25 | 5,27 | 5,29 |
| | upside | 5,43 | 5,65 | 5,65 | 5,64 | 5,66 | 5,68 |

A IPCA, a Focus, o hiato e a PTAX são do modelo, não conclusões minhas; os donos são os agentes de inflação, expectativas, atividade e câmbio.

### 3.2 Etapa 2 — o tempero qualitativo

**(i) Reação da Selic ao desvio da expectativa contra a meta (`R.t3`) — mais forte que o estimado** · cenário upside
- Coeficiente: estimado 1,96, intervalo de 90% do posterior de 1,15 a 2,73. Multiplicador: × 1,35, dentro do intervalo (2,65, no percentil 90 do posterior).
- Efeito: Selic de fechamento do upside de 13,52% para 13,70% no 4T26 e de 12,49% para 12,96% no 1T28.
- Por quê: o Copom disse por escrito que, com expectativas desancoradas, "exige-se uma restrição monetária maior e por mais tempo do que outrora seria apropriado" (ata da 281ª, §10), conclusão "compartilhada por todos os membros". É exatamente uma reação ao desvio da expectativa maior que a média da amostra da regra. Fica perto da borda do posterior porque a frase descreve o Copom de agora, não o de 2006 a 2026.
- Onde entra: limite e probabilidade da cauda de cima.

**(i) Reação da Selic ao desvio da expectativa contra a meta (`R.t3`) — mais fraca que o estimado** · cenário downside
- Coeficiente: estimado 1,96, intervalo de 90% de 1,15 a 2,73. Multiplicador: × 0,75, dentro do intervalo (1,47, no percentil 13).
- Efeito: Selic de fechamento do downside de 12,85% para 12,72% no 4T26 e de 11,37% para 11,09% no 1T28.
- Por quê: no downside a expectativa cai junto com o petróleo, e o Copom, que não reage ao efeito primário de um choque de oferta na subida (ata da 281ª, §16), não segura a Selic por um desvio que está se desfazendo pelo mesmo motivo na descida.
- Onde entra: limite e probabilidade da cauda de baixo.

**(ii) Choque do petróleo e combustíveis fora do modelo — Brent** · cenários base e upside
- Hoje: US$ 135,51 (`comm_brent`, 02/10); +97,7% em 3 meses e US$ 114,16 de média em setembro (G `pm_leituras`).
- Por que o modelo não vê: nenhuma equação tem petróleo; monitorados têm só inércia e o IPCA anterior, e o IC-Br em dólar entra só no câmbio. O Copom projeta combustíveis condicionados à curva futura e às subvenções (RPM 2.1 e 2.2, MP 1.363, LC 235, Decreto 13.116; a MP 1.391 não está no cenário).
- Efeito: na base, não move a central; é o motivo dos 55% de manutenção em novembro e da persistência da pausa até março. No upside, +25 p.b. sobre o modelo no 4T26, +50 p.b. do 1T27 ao 4T27 e +25 p.b. no 1T28: a segunda ordem aparecendo leva o Copom a desfazer parte do ciclo.
- Onde entra: assimetria da base e limite da cauda de cima.

**(ii) O calendário e a doutrina de fim de ciclo — reuniões do Copom** · cenário base
- Hoje: 38% do 4T26 já em 13,75% (G `pm_calendario`); cinco cortes de 25 p.b. seguidos (`pm_copom_reuniao`); guidance sem passo, "a magnitude total do ciclo de calibração será estabelecida à luz de novas informações" (comunicado da 281ª).
- Por que o modelo não vê: a regra (R) trabalha com a média do trimestre e não sabe que só há duas reuniões no 4T26, nem que ciclos no Brasil terminam num corte de 25 p.b. e ficam parados.
- Efeito: põe a Selic de fechamento do 4T26 acima da central do modelo em quase todo caminho plausível (média da árvore, 13,61%), e mantém a média acima até o 1T28.
- Onde entra: assimetria da base.

### 3.3 Da etapa 1 à tese

| Trimestre | Central (modelo, base) | Upside: modelo → com tempero | Downside: modelo → com tempero |
|---|---|---|---|
| 4T26 | 13,10 | 13,52 → 13,95 | 12,85 → 12,72 |
| 1T27 | 12,78 | 13,33 → 14,14 | 12,43 → 12,22 |
| 2T27 | 12,50 | 13,07 → 13,97 | 12,12 → 11,85 |
| 3T27 | 12,25 | 12,85 → 13,81 | 11,83 → 11,54 |
| 4T27 | 12,04 | 12,66 → 13,64 | 11,58 → 11,29 |
| 1T28 | 11,85 | 12,49 → 13,21 | 11,37 → 11,09 |

A faixa base de cada trimestre vai da central do modelo, ou um degrau de 25 p.b. abaixo, até a mediana da minha árvore de reuniões; os limites ficam entre a central e os pontos com tempero, e as probabilidades são a massa da árvore dentro e fora da faixa (G `pm_reunioes`). Os pontos com tempero ficam todos fora da faixa, do lado certo: a cauda de cima é a do petróleo com segunda ordem, a de baixo a do petróleo devolvido.

## 4. Para os outros agentes

### Respostas às entradas fixas

- **E1 (câmbio S1), caminho da Selic e balanço de riscos:** a tese da seção 1, com a tabela de reuniões; o carry adiante fica mais alto que o da Focus, porque espero 13,75% até março (70% de manutenção por reunião) contra 13,25% da Focus em março (`expc_focus_copom` · 25/09); assimetria de +0,53 a +0,20.
- **E2 (câmbio S2), alta lida como credibilidade ou como validação da inflação:** credibilidade. Expectativas desancoradas (ata da 281ª, §10) e choque de oferta são o caso em que uma alta reancora; o CDS em 131 (`cmb_risco_pais` · 02/10) está longe de um regime de dominância fiscal, mas subiu 19 p.b. desde a reunião, e a leitura é do fiscal (S11, S12).
- **E3 (câmbio S3), como o Copom descreveu o câmbio, em destaque:** risco de alta por "uma taxa de câmbio persistentemente mais depreciada" (comunicado da 281ª); condicionante de R$ 5,15 seguindo a PPC; o RPM atribui parte da depreciação recente ao diferencial de juros menor (RPM 2.2). Em destaque porque a PTAX abriu 1,4% acima do condicionante desde a reunião (R$ 5,1527 em 16/09, R$ 5,2238 em 02/10, `cmb_ptax`), na direção que o Copom lista como risco.
- **E4 (câmbio S4), reação a uma depreciação:** pela Selic, o Copom não reage ao primeiro efeito e reage com firmeza à segunda ordem (ata da 281ª, §16); uma depreciação persistente junto com o petróleo é o que leva a árvore a 9% de Selic em 14,00% ou mais no fim de 2026. O BC vendeu US$ 2,0 bi à vista e US$ 2,0 bi em linha em setembro (`cmb_reservas_bc` · set); se foi resposta a disfunção é leitura do câmbio (S6). Nenhum documento do Copom fala do nível do real, então a pergunta não se amplia à função de reação inteira neste ciclo.
- **E5 (inflação IN-S3), caminho da Selic:** a tese da seção 1.
- **E6 (inflação IN-S4), projeção do Copom e condicionantes, em destaque:** IPCA de 4,4% (3T26), 5,2% (4T26), 4,9% (1T27), 4,5% (2T27), 4,5% (3T27), 3,9% (4T27) e 3,2% (1T28); administrados 3,9%, 5,3%, 4,5%, 4,0%, 4,3%, 3,5% e 3,2% (`pm_copom_projecoes` · RPM de 24/09). Condicionantes: Selic da Focus, câmbio de R$ 5,15 pela PPC, Brent de US$ 90 de média no 3T26, pico no 4T26, cerca de US$ 84 no 2T27 e +2% a.a. depois, margens de refino normalizando, fim das subvenções no prazo legal, bandeira amarela até dezembro de 2026 e sequência "neutra" em 2027 (RPM 2.2). São condicionantes, não previsão. Em destaque porque o Brent de 02/10 está 51% acima do ponto de partida.
- **E7 (atividade S-PM1), Selic média e de fechamento:** a média do modelo na base é 13,27% no 4T26 e 11,94% no 1T28 (seção 3.1); o fechamento é a tese. Na minha árvore o fechamento médio é 13,61% no 4T26: o aperto que chega à (H) tende a ser maior que o do modelo.
- **E8 (atividade S-PM2), a postura:** Q2. Selic real ex-ante de 8,70%, 2,70 p.p. acima do neutro do QPC de 2 anos, que é o que uso; 3,70 p.p. acima do neutro do Copom; Selic 3,24 p.p. acima da âncora nominal do modelo (G `pm_juro_real`). A âncora do modelo carrega prêmio e caiu por inflação implícita, então o aperto efetivo é maior que o que a (H) mede.
- **E9 (atividade S-PM3), como o Copom leu a atividade e o hiato, em destaque:** "moderação gradual", mais forte nos setores cíclicos, PIB do 2T26 confirmando a desaceleração, desaceleração como "elemento essencial" da convergência (ata da 281ª, §2 e §5); hiato de 0,5% no 2T26 e 0,4% no 3T26, indo a −0,4% no 1T28 (RPM 2.2). Em destaque porque a edição de setembro revisou para cima os trimestres recentes: +0,15 p.p. no 2T26, +0,11 no 1T26, +0,14 no 4T25 (`pm_hiato_produto_vintages` · set).
- **E10 (fiscal FS-PM1), caminho da Selic:** a tese da seção 1.
- **E11 (fiscal FS-PM2), como o Copom descreveu a política fiscal:** impacto de curto prazo pela demanda e dimensão estrutural no prêmio a termo; esmorecimento de reformas, crédito direcionado e incerteza da dívida elevam o neutro (ata da 281ª, §8); estímulos à demanda como risco de alta (iv); no cenário de referência, melhora gradual do primário estrutural (RPM 2.2). O Copom lê o fiscal como demanda e como neutro, as duas coisas.
- **E12 (fiscal FS-PM3), divisão do juro real longo:** a parte da política é o caminho da tese. Não tenho decomposição de prêmio de prazo neste ciclo (Faltou); o que a curva deixa ler é que a queda da NTN-B de 10 anos desde 30/06 veio com o DI de 10 anos parado e a inflação implícita subindo, não com queda do caminho nominal esperado (Q4, item 1).
- **E13 (fiscal FS-PM4), alta como credibilidade ou como risco da dívida:** a mesma leitura de E2.
- **E14 (externo XS3), caminho da Selic:** a tese da seção 1; o diferencial contra o Fed fica maior que o da Focus em 2027 (Fed funds, meta, a 3,88%, `us_interest_rate` · 02/10).
- **E15 (externo XS4), como o Copom lê o cenário externo:** incerteza pelos conflitos no Oriente Médio e pela política monetária em economias avançadas, volatilidade de ativos e commodities (ata da 281ª, §1 e §4); riscos: câmbio mais depreciado por políticas externa e interna (alta, iii), desaceleração global e queda de commodities (baixa, ii e iii); condicionante do petróleo pela curva futura (§11).
- **E16 (externo XS6), `rr_10a` e quanto dele é juro americano:** meu caminho é 7,51% segurado, e quem usa o P é o do fiscal (nível 1). Neste trimestre a NTN-B de 10 anos caiu enquanto o Treasury de 10 anos subiu 0,79 p.p. em 3 meses (`us_interest_rate` · 02/10), então o movimento não veio dos EUA.
- **E17 (expectativas XS1), reação a expectativas acima da meta:** sim, com mais força que a média histórica (ata da 281ª, §10; tempero (i) × 1,35 no upside); neste momento, pela pausa, não pela alta, que fica condicionada à segunda ordem.
- **E18 (expectativas XS2), o que o Copom disse das expectativas:** acima da meta "em todos os horizontes", desancoragem nos prazos longos, custo de desinflação maior (ata da 281ª, §10; comunicado: 4,9% para 2026 e 4,3% para 2027); o RPM mede a ancoragem a dois ou três anos e registra 2028 de 3,69% para 3,80% (RPM 2.3); projeção de 3,2% no 1T28 contra a Focus de 3,80% para 2028.
- **E19 (expectativas XS3), meta:** 3,00% em todo o horizonte (seção 3.1), meta contínua; nenhum sinal de mudança pelo CMN nos documentos lidos.
- **E20 (expectativas XS4), Selic da curva contra a Focus:** Q3. A curva fica acima da Focus em toda reunião, de +10 p.b. em novembro a +195 p.b. em dezembro de 2027 (G `pm_juro_real`, curva de 02/10 contra Focus de 25/09).
- **E21 (atividade S-FI2), `rr_10a` e o prêmio fiscal nele:** 7,51% segurado; o prêmio fiscal não está comprimindo (CDS de 111,6 em 16/09 para 131,0 em 02/10, `cmb_risco_pais`). Vale só se o P usar o meu caminho.

### Pedidos

- **S1 (câmbio):** a alta de 1,4% da PTAX desde 16/09 é persistente? Dela depende a probabilidade de manutenção em novembro e dezembro (tese, 4T26 e 1T27).
- **S2 (câmbio):** a depreciação do mês é global ou idiossincrática? O peso mexicano subiu 7,8% e o chileno 5,0% em 1 mês contra o dólar (`cmb_fx_latam` · 02/10), o que parece global, mas a eleição cai na mesma janela. Idiossincrática aumenta a cauda de cima.
- **S3 (câmbio):** onde fica o real contra a média de dez dias úteis até 30/10, que será o ponto de partida do câmbio na 282ª? Uma abertura acima de R$ 5,15 move a projeção do Copom para cima (Q1).
- **S4 (câmbio):** o real está precificando estresse fiscal ou eleitoral? O CDS subiu 19 p.b. desde a reunião. Pesa no upside e na leitura do neutro.
- **S5 (câmbio):** quanto do suporte do carry se perde se o mercado passar a precificar fim de ciclo em 13,75%? Se nada, o canal do câmbio continua ajudando a desinflação.
- **S6 (câmbio):** as vendas de US$ 2 bi à vista e US$ 2 bi em linha de setembro responderam a disfunção? Decide se E4 se amplia na rodada 2.
- **S7 (inflação):** quanto do Brent a US$ 135 e do câmbio chega a combustíveis, energia e passagens até o 1T27, com as subvenções em vigor e a MP 1.391? É o tamanho do tempero (ii) do petróleo.
- **S8 (inflação):** o choque está se espalhando? Serviços subjacentes, difusão e núcleos: a segunda ordem que a ata §16 diz que o Copom vigia já aparece? É o que separa a pausa (base) da alta (upside).
- **S9 (expectativas):** a Focus de 12 meses em 4,65% e a de 2028 em 3,80% são desancoragem ou reação de curto prazo ao choque? E o caminho da (E), que parte de 4,37% e dá 4,16% no 4T26 com a pesquisa em 4,65%, é crível, ou você aplicaria multiplicador na (E)? Muda a probabilidade de alta e o limite de cima.
- **S10 (atividade):** o hiato fecha no 1T27, como no modelo (−0,08%), ou fica positivo mais tempo, como sugere a revisão para cima da edição de setembro? E salários contra produtividade? Um hiato positivo por mais tempo alonga a pausa.
- **S11 (fiscal):** a queda da NTN-B de 10 anos desde 30/06, com DI de 10 anos parado e CDS subindo, é compressão do prêmio fiscal ou não? E qual o seu caminho para `rr_10a`? Se for o meu (7,51%), a central não muda; se for mais baixo, ela cai, e a minha divergência cresce (Q4, item 1).
- **S12 (fiscal):** qual o impulso fiscal do 4T26 e 1T27, incluindo subvenções a combustíveis, e a eleição muda a leitura de dominância fiscal? Estímulo à demanda é o risco (iv) do Copom.
- **S13 (externo):** o salto do Brent de US$ 114,82 para US$ 135,51 em 02/10 é um novo patamar? Qual o caminho do Brent, do `ffr` (a meta subiu para 3,88%) e da inflação americana, e os pares vão subir juros? Define a duração da pausa e a cauda de cima.
- **Pedido deste ciclo, ao externo:** a curva futura do Brent, que o Copom usa como condicionante dos seis meses seguintes; sem ela não sei quanto da projeção da 282ª já vai subir só pela governança.

## 5. Placar

Primeiro ciclo: não há report final anterior nem trimestre fechado a conferir.

## 6. Sobre o modelo

| Fonte | O que sugere (regressor, defasagem, quebra, âncora) | Teste proposto (dado, amostra, que resultado mudaria a especificação) | Por que importa para a tese deste ciclo |
|---|---|---|---|
| Mapa conceitual, 2.5 (armadilha: a âncora do modelo é um juro de mercado com prêmio, não o neutro do Copom); dados de `br_interest_rate` deste ciclo | Âncora da (R) e da (H): o juro real de 10 anos (NTN-B) é DI nominal menos inflação implícita; a especificação impõe que uma alta da inflação implícita, com DI parado, baixe a Selic um por um | Reestimar a (R) com a âncora aberta em DI de 10 anos e inflação implícita de 10 anos, com coeficientes livres, 2006T1 a 2026T3. Se o coeficiente da inflação implícita for zero ou positivo (o Copom não corta quando a inflação implícita sobe), trocar a âncora por DI de 10 anos menos uma expectativa de pesquisa de longo prazo | Neste ciclo a NTN-B caiu cerca de 0,5 p.p. com o DI de 10 anos parado, e o modelo cortou a Selic cerca de um terço de ponto por isso (Q4, item 1) |
| Mapa, 2.1 (Taylor 1993: a regra literal dá a resposta errada a um choque temporário de petróleo); RPM set/26, boxe de efeitos primários | Monitorados (I.IM) sem petróleo nem combustível; o choque só entra por inércia | Acrescentar a variação do Brent em reais (e, se houver, o preço de combustível na refinaria) à equação de monitorados, 2006T1 a 2026T3; mudar se o coeficiente for significativo e o erro de um passo cair em 2021-22 e 2026 | Brent +97,7% em 3 meses e a contribuição de monitorados do modelo não o vê (tempero (ii)) |
| Comunicados e calendário do Copom (`pm_copom_calendario`) | O primeiro trimestre projetado já está em parte decidido: a Selic vigente vale até a próxima reunião | Condicionar a média do primeiro trimestre projetado na Selic vigente até a primeira reunião (só a fração restante sai da regra); comparar o erro de um passo da Selic média, 2006 a 2026, com e sem a restrição; adotar se o erro cair | A média do 4T26 do modelo (13,27%) exige mais de 50 p.b. por reunião, com 38% do trimestre já em 13,75% (Q4, item 2) |

[^corte]: O F foi cortado pela data de **referência** dos dados, não pela de divulgação, e traz dados publicados depois de 02/10: o IPCA de setembro (divulgado em 09/10), as pesquisas Focus de 28/09 a 02/10 (05/10), o IC-Br de setembro (07/10), a balança comercial de setembro (06/10), a PMS, a PMC e o IBC-Br de agosto (14, 15 e 16/10). A argumentação usa só o que existia em 02/10: a Focus de 25/09, o IPCA até agosto e o IPCA-15 de setembro. O ponto de partida do Modelo Estrutural (3T26) não pôde ser separado: ele usa o IPCA e o IC-Br de setembro e a inflação americana de setembro.
[^fim]: O modelo só tem a Selic média do trimestre. O fechamento é derivado: média deste trimestre mais a do seguinte, dividido por dois. Erro histórico dessa regra, 0,12 p.p. em média.
[^arvore]: A trajetória de reuniões é uma árvore: para cada reunião, a chance de cada passo depende do passo da reunião anterior (depois de uma parada, parar de novo é mais provável que depois de um corte). A tabela mostra a chance de cada passo somando todos os caminhos que levam até aquela reunião.
[^hr]: Horizonte relevante: o trimestre em que o Copom mira a inflação na meta, cerca de seis trimestres à frente, porque a política leva esse tempo para agir sobre os preços. Hoje é o 1T28.
[^cond]: A projeção do cenário de referência do Copom é condicional: a Selic vem da Focus, o câmbio segue a paridade de poder de compra e o petróleo segue a curva futura por seis meses. O próprio Copom diz que esses caminhos "não necessariamente refletem o cenário mais provável" (RPM set/26, 2.3). Por isso a projeção é lida como o que acontece se esses caminhos se confirmarem, não como a previsão do Copom.
[^brent]: O Brent subiu de US$ 114,82 em 01/10 para US$ 135,51 em 02/10, 18% num pregão. É um salto raro; se ele é patamar ou ruído é pergunta ao agente externo (S13).
[^neutro]: Juro neutro: a taxa real que nem acelera nem freia a economia. Se o neutro é 6% e a Selic real é 8,7%, a política está freando a economia em cerca de 2,7 p.p. Ninguém observa o neutro; cada fonte o estima de um jeito.
[^ancora]: A regra de juros do Modelo Estrutural ancora a Selic no juro real da NTN-B de 10 anos mais a meta. Quando o juro real longo cai, a âncora cai e a regra corta a Selic no mesmo trimestre.
[^meta]: Meta contínua: desde 2025 a meta de 3% é conferida todo mês pelo IPCA de 12 meses, e só é descumprida se ficar fora do intervalo de 1,5% a 4,5% por seis meses seguidos. Passar do teto num trimestre não é, sozinho, descumprimento.
[^premio]: Prêmio de prazo: o que o investidor cobra a mais para emprestar por prazo longo em vez de rolar o curto. Por isso a curva DI fica acima do caminho que o mercado de fato espera para a Selic, e mais acima quanto mais longe a reunião. A inflação implícita (DI contra NTN-B de mesmo prazo) também carrega um prêmio, o de risco de inflação.
[^faixa]: A faixa de 90% que o modelo imprime é só a incerteza dos pesos estimados; não inclui o erro das equações e não é intervalo de previsão. A distribuição da tese é minha.
[^eleicao]: Não há dado eleitoral nesta análise; as datas dos dois turnos vêm do calendário eleitoral e entram só como evento que pode mover o prêmio de risco.
[^pctl]: Percentil: a posição de um valor numa distribuição, de 0 a 100. No QPC, p25 a p75 é o intervalo em que fica a metade central das respostas: um quarto dos analistas respondeu menos de 3,77% e um quarto mais de 4,20%. Nos multiplicadores da seção 3.2, o percentil diz onde o coeficiente multiplicado cai entre os valores que a estimação considera plausíveis: no 90, só 10% dos desenhos são maiores.
