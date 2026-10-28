# Report — política monetária · ciclo 2026-10-27 · rodada 1

Dados até: pregão de 26/10/2026 (curvas, PTAX, CDS), Focus de 23/10, QPC da 281ª (23/09), documentos do Copom até o RPM de 24/09 · Horizontes: 4T26 a 1T28, a meta Selic no fechamento de cada trimestre (a decisão da última reunião dentro dele)[^1]

## 1. Tese

| Variável | Trimestre | Central | Base: faixa · P | Upside: limite · P | Downside: limite · P | P(up) − P(down) |
|---|---|---|---|---|---|---|
| Meta Selic, fechamento do trimestre (% a.a.) | 4T26 | 13,49 | 13,45 a 13,80 (13,50 ou 13,75) · 59% | acima de 13,80 (alta até 09/12) · 34% | abaixo de 13,45 (dois cortes) · 7% | +0,27 |
| | 1T27 | 13,32 | 13,25 a 14,05 · 56% | acima de 14,05 · 31% | abaixo de 13,25 · 13% | +0,18 |
| | 2T27 | 13,04 | 12,75 a 14,05 · 58% | acima de 14,05 · 33% | abaixo de 12,75 · 9% | +0,24 |
| | 3T27 | 12,80 | 12,50 a 14,05 · 57% | acima de 14,05 · 30% | abaixo de 12,50 · 13% | +0,17 |
| | 4T27 | 12,58 | 12,25 a 14,05 · 59% | acima de 14,05 · 25% | abaixo de 12,25 · 16% | +0,09 |
| | 1T28 | 12,39 | 12,00 a 14,05 · 66% | acima de 14,05 · 18% | abaixo de 12,00 · 16% | +0,02 |

A central é a Selic de fechamento do Modelo Estrutural no cenário base (seção 3.1), sem ajuste[^2]. A Selic anda em degraus de 25 p.b., então cada faixa é um conjunto de decisões possíveis: no 4T26, 13,45 a 13,80 quer dizer "13,50 ou 13,75", e o limite de baixo fica em 13,45 para conter a central do modelo, 13,49.

**As duas próximas reuniões de cada trimestre, decisão a decisão** (Selic de partida 13,75%, decidida em 16/09; probabilidades deste agente, que somam 100% em cada linha e fecham nas linhas de 4T26 e 1T27 acima[^3]):

| Reunião | −50 p.b. | −25 p.b. | manter | +25 p.b. | +50 p.b. | Mais provável | Curva DI 26/10 | Focus 23/10 |
|---|---|---|---|---|---|---|---|---|
| 04/11/2026 | — | 11% | 75% | 9% | 5% | manter, 13,75 | 13,73 | 13,50 |
| 09/12/2026 | 1% | 16% | 54% | 17% | 12% | manter, 13,75 | 14,02 | 13,25 |
| 27/01/2027 | 1% | 19% | 53% | 16% | 11% | manter, 13,75 | 14,45 | 13,00 |
| 17/03/2027 | 1% | 19% | 59% | 16% | 5% | manter, 13,75 | 14,84 | 12,75 |

Curva DI e Focus: `br_di_grade` (26/10) e `expc_focus_copom` (23/10), a Selic de cada reunião na tabela "A Selic por reunião" do F.

- **Upside, acima da faixa: o Copom encerra a calibração e sobe a Selic.** No modelo, o prêmio que saltou em 26/10 se aprofunda (CDS a 200 p.b. no 1T27, NTN-B de 10 anos a 8,60%) e a Selic fecha o 4T26 em 13,97; com a regra reagindo à expectativa 30% mais forte que o estimado (tempero i) vai a 14,13; com a reação do Copom ao câmbio, que a regra (R) não tem (tempero ii-a), a 14,25–14,50 em dezembro e a 14,75 no 1T27. É ruim para o Brasil: quer dizer câmbio, expectativas e prêmio piores que no base.
- **Downside, abaixo da faixa: o choque de 26/10 se desfaz e os cortes voltam.** No modelo, CDS a 115 p.b. e NTN-B de 10 anos de volta a 6,93% (a média de 01 a 23/10) levam a Selic a 12,53 no 4T26; o gradualismo do Copom (tempero ii-b) limita a 13,25 em dezembro e ~13,00 em março. Só é boa notícia se vier da reversão do prêmio; corte com o câmbio ainda em 5,50 seria um Copom leniente, ruim para a credibilidade.

**A tese em uma frase:** o Copom interrompe o ciclo de calibração em 04/11 e mantém 13,75% (75%), porque cortar na semana em que a PTAX saltou 9,2% e a inflação implícita subiu 1,2 p.p. validaria a desancoragem; o modelo, ancorado no juro real de 10 anos que saltou junto, desenha cortes graduais até 12,4% no 1T28, mas o risco é de alta, de 34% até dezembro, enquanto não se souber se o choque de 26/10 fica.

## 2. Argumentação

### O fato do ciclo: 26/10

O mercado brasileiro reprecificou em um pregão. De 23/10 para 26/10 a PTAX subiu 9,19% (5,0377 → 5,5007 · `cmb_ptax`), o CDS de 5 anos 18 p.b. (119 → 137 · `cmb_risco_pais`), o DI de 2 anos 252 p.b. e a NTN-B de 10 anos 135 p.b. (`br_interest_rate` · 23 e 26/10). Não foi um dia de dólar global: o DXY subiu 0,6% desde 22/10 (`cmb_dollar_index` · 27/10) e o dólar contra emergentes recuou 0,1% até 23/10 (`cmb_dollar_index_em`). O movimento espelha, no sentido oposto e maior, o da segunda-feira 05/10, quando a PTAX caiu 4,55%, o CDS 12 p.b. e o DI de 2 anos 110 p.b. (mesmas tabelas, 02/10 → 05/10). As duas datas são segundas-feiras depois de fins de semana (03–04/10 e 24–25/10) e o RPM de setembro registra 2026 como "ano eleitoral" (RPM set/26, Fiscal); o que aconteceu nesses fins de semana o F não carrega, e o report trata a causa como pedido ao agente web (seção 4), não como premissa[^4].

Para a política monetária o salto tem três partes, e cada dado responde a uma:
- **O câmbio passou do condicionante do Copom:** a PTAX de 5,50 está 6,8% acima dos R$ 5,15 do cenário de referência da 281ª (comunicado, Tabela 1), e uma "taxa de câmbio persistentemente mais depreciada" é o risco de alta (iii) da lista do Copom (ata da 281ª, §13). Se é persistente, é a pergunta S1 ao câmbio.
- **A compensação por inflação subiu em todos os prazos:** a inflação implícita (DI contra NTN-B) subiu 1,19 p.p. em 1 ano, 1,23 em 2, 1,20 em 5 e 0,89 em 10 anos, de 23 para 26/10 (`br_interest_rate`); em 1 ano ela está em 7,87%, contra a Focus de 12 meses em 4,53% (`expc_focus` · 23/10). Quanto disso é expectativa e quanto é prêmio é do agente de expectativas (S9).
- **O prêmio no juro real longo subiu, e não é caminho de política:** a NTN-B de 1 ano subiu 43 p.b., a de 10 anos 135 p.b., e o juro real de 5 anos daqui a 5 anos foi de 6,70% para 8,17% (`br_interest_rate` · 23 e 26/10). Um caminho de Selic mais alto apareceria na ponta curta da curva real; um movimento concentrado depois de 5 anos é prêmio, a leitura que a seção 4 leva ao fiscal como subordinado de `rr_10a`.

### Q1 — O que o Copom vai fazer?

**Em 04/11: manter 13,75% e encerrar a calibração (75%).** Três coisas do Copom sustentam a pausa, e uma regularidade sustenta que ela venha antes de uma alta:
- A função de reação declarada olha a projeção no horizonte relevante (1T28) e reage aos efeitos de segunda ordem dos choques (ata da 281ª, §16); o salto de 26/10 mexe nos dois condicionantes que a governança atualiza automaticamente: o câmbio de partida, que é a média de dez dias úteis antes da semana da reunião (RPM set/26, Apêndice metodológico), e a trajetória de Selic da Focus.
- A guidance é condicional: "a magnitude total do ciclo de calibração será estabelecida à luz de novas informações" (comunicado da 281ª, §6), com "serenidade e cautela" (§8) e a conclusão unânime de que, com expectativas desancoradas, "exige-se uma restrição monetária maior e por mais tempo" (ata da 281ª, §10). Cortar oito dias depois do salto iria contra as três frases.
- Antes do choque, a pausa já dividia o mercado: no QPC da 281ª, 53% dos respondentes esperavam manutenção em novembro, com passo médio de −12 p.b. (`expc_qpc` · 23/09), e a curva de 23/10 dava −18 p.b. para 04/11 (`br_di_grade`, 13,57%).
- Em 248 decisões desde 1999, o Copom nunca passou de um corte direto para uma alta na reunião seguinte: os 14 ciclos de corte terminaram numa manutenção, e as oito reversões para alta tiveram de uma a cinco manutenções no meio (`pm_copom_reuniao`, 1999–2026). Por isso uma alta já em 04/11 fica em 14%, mas não em zero: em 2002 a primeira alta, de 300 p.b., veio depois de só duas manutenções (mesma tabela, 14/10/2002).

O corte de 25 p.b. fica com 11%: exige que o choque reverta antes da reunião — um pregão de −4,55% na PTAX já aconteceu em 05/10 — e que o Copom leia o câmbio como transitório. **Mas** a Focus de 23/10, coletada antes do choque, ainda tinha 13,50% para 04/11 (`expc_focus_copom`); se a Focus de 30/10 mantiver o corte, a probabilidade de corte sobe.

**Em 09/12 e no 1T27: a decisão depende de o choque ficar.** Manter é a moda (54% em dezembro), mas a Selic acima de 13,75% depois de 09/12 tem 34%, e só a reunião de dezembro tem 29% de alta (17% de +25 e 12% de +50). O que move a decisão nessas reuniões, em ordem: a Focus de 2027 e 2028 (hoje 4,34% e 3,75% · `expc_focus_periodo` · 23/10), a média dos núcleos e os serviços subjacentes (5,32% em 12 meses · `inflc_decomposicao` · set) e o câmbio de partida da projeção de dezembro. **Apesar de** a atividade desacelerar — IBC-Br −0,8% em três meses até agosto (`atv_ibcbr`), produção industrial −2,1% (`atv_pim`), varejo ampliado −0,9% (`atv_pmc`) — o Copom já tinha a moderação no cenário (ata da 281ª, §5) e só uma desaceleração mais forte é risco de baixa (RPM set/26, 2.3).

O Copom está agindo como sua reação usual implica: o ciclo de 2026 foi de cinco cortes iguais de 25 p.b. desde 18/03, de 15,00% para 13,75% (`pm_copom_reuniao`), com o horizonte relevante projetado em 3,2% nas duas últimas reuniões (`pm_copom_projecoes`, 281ª e 280ª), acima da meta de 3,00%. Um Copom que corta com a projeção acima da meta está aceitando convergência lenta; um choque cambial dessa ordem tira essa folga.

### Q2 — O que o Copom deveria fazer, pelos dados?

**Manter 13,75% em novembro e dezembro, dizer que a calibração acabou, e subir só se aparecer segunda ordem.** O argumento tem três partes.

*A política já é restritiva por qualquer neutro de pesquisa ou do Copom.* A Selic real ex-ante, com a Focus de 12 meses, é 8,82% (`br_interest_rate` e `expc_focus` · 23/10)[^5]:

| Neutro | Valor | Selic real ex-ante acima dele | Fonte |
|---|---|---|---|
| Copom, cenário de referência | 5,00% | +3,82 p.p. | RPM set/26, 2.2 |
| QPC, 5 anos | 5,50% | +3,32 p.p. | `expc_qpc` · R279 |
| QPC, 2 anos | 6,00% | +2,82 p.p. | `expc_qpc` · R279 |
| QPC, curto prazo | 6,40% | +2,42 p.p. | `expc_qpc` · R279 |
| Âncora do modelo (NTN-B 10a + meta), nominal | 11,05% | Selic nominal +2,70 p.p. | `br_interest_rate` · 26/10 |

Uso o intervalo do Copom e do QPC para julgar o aperto, porque são o que o Copom diz usar (RPM set/26, 2.2), e a âncora do modelo como alerta: ela carrega o prêmio de mercado (mapa, 2.5). E o alerta é o ponto do ciclo: de 23 para 26/10 a âncora subiu de 9,70% para 11,05%, e a distância da Selic até ela caiu de 4,05 para 2,70 p.p. sem o Copom mexer em nada (`br_interest_rate`). Pela leitura do modelo, que é a do Copom na ata da 281ª (§8) — incerteza sobre a dívida eleva o juro neutro —, o choque de prêmio afrouxou a política. É o argumento contra cortar.

*A inflação e as expectativas não dão folga.* O IPCA de 12 meses está em 4,58% (`inflc_agregados` · set), acima dos 4,40% que o Copom projetava para setembro (RPM set/26, Tabela 2.1.2), e o IPCA-15 de outubro em 4,62%. Serviços rodam 5,97% e serviços subjacentes 5,32% (`inflc_decomposicao` · set), o grupo que o Copom diz ser o mais sensível ao hiato e o mais inercial (RPM set/26, 2.3). A Focus está acima da meta em todos os anos: 5,19% (2026), 4,34% (2027), 3,75% (2028), 3,50% (2029) (`expc_focus_periodo` · 23/10). O hiato da última edição é positivo, 0,41% no 3T26, e cada trimestre recente foi revisado para cima, de +0,10 a +0,15 p.p. (`pm_hiato_produto_vintages` · edição de set/26); o desemprego está em 5,3% (`mt_pnad` · ago). E o Brent a US$ 115 (`comm_brent` · 20/10) está muito acima do ponto de partida de US$ 90 do cenário de referência (RPM set/26, 2.2), o que pesa nos monitorados (S8).

*Mas subir agora seria cedo.* A transmissão está funcionando: a inadimplência da carteira livre de pessoa física subiu 1,04 p.p. em 12 meses, para 8,01% (`cred_credito_resumo` · ago), e o comprometimento de renda com a dívida 1,40 p.p., para 28,72% (`cred_credito_familias` · jul) — premissa *assumida*, crédito sem agente. O hiato deve virar negativo (RPM set/26, 2.2: −0,4% no 1T28) e a atividade desacelera (Q1). O choque tem um pregão, e sob estresse fiscal uma alta pode não apreciar o câmbio (mapa, 2.6)[^6]. A alta deveria vir com sinal de segunda ordem: Focus de 2027 acima de 4,6% ou de 2028 acima de 4,0%, serviços subjacentes acelerando no trimestre, ou PTAX acima de 5,40 por mais de duas semanas até a reunião de dezembro.

**A distância entre Q1 e Q2 é pequena em novembro e cresce em dezembro.** Em novembro as duas dizem manter. Em dezembro o Copom pode subir antes do que os dados pedem, empurrado pela curva, que já precifica a alta (Q3): esse é o peso do regime de alta (35%) na cauda de upside. O risco oposto, um Copom que retoma cortes com o câmbio em 5,50 — o BC "dócil" do mapa (Parte 1, item 5) —, alimenta o downside e seria ruim para a credibilidade; dou a ele pouco peso porque o comunicado e a ata da 281ª não deixam espaço para isso.

### Q3 — O que o mercado precifica, e onde diverge

| Reunião | Curva DI 23/10 | Curva DI 26/10 | Salto (p.b.) | Focus 23/10 | Curva 26/10 − Focus (p.b.) |
|---|---|---|---|---|---|
| 04/11/2026 | 13,57 | 13,73 | +18 | 13,50 | +23 |
| 09/12/2026 | 13,45 | 14,02 | +54 | 13,25 | +77 |
| 27/01/2027 | 13,26 | 14,45 | +124 | 13,00 | +145 |
| 17/03/2027 | 13,16 | 14,84 | +161 | 12,75 | +209 |
| 16/06/2027 | 12,81 | 15,31 | +247 | 12,25 | +306 |
| 22/09/2027 | 12,46 | 15,54 | +299 | 12,00 | +354 |
| 08/12/2027 | 12,46 | 15,78 | +323 | 11,75 | +403 |

Curva 26/10, Focus e diferença: tabela "A Selic por reunião: curva DI e Focus" do F (`br_di_grade`, `expc_focus_copom`). Curva 23/10 e salto: `br_di_grade` · 23 e 26/10, no mesmo método aproximado[^7].

- **Contra Q1:** em novembro a curva e eu dizemos o mesmo, manter. Em dezembro ela precifica +29 p.b.; a média da minha distribuição para 09/12 é 13,83% e a moda é manter. A partir de 2027 a curva desenha um ciclo de alta até 15,78% em dezembro de 2027; minha distribuição põe 35% num ciclo de alta, com média de 14,64% no 2T27 nesse regime (seção 3.3).
- **Contra Q2:** eu não subiria antes de ver segunda ordem; a curva já cobra a alta.
- **Contra o que o Copom sinaliza:** a projeção de 3,2% no 1T28 foi feita com a trajetória da Focus — 13,75% no fim de 2026 e 12,00% em 2027 (RPM set/26, 2.2) —, que na curva de 26/10 está 2 a 4 p.p. abaixo do preço. O Copom não endossa nenhuma das duas: a Focus é condicionante de governança, não a previsão dele (mapa, 2.2).
- **Prêmio, não só caminho:** o salto cresce com o prazo e chega a +323 p.b. em dezembro de 2027, muito além de onde qualquer comunicação do Copom alcança, e o juro real de 5 anos daqui a 5 anos subiu 147 p.b. no mesmo pregão. Leio a maior parte da diferença entre curva e Focus em 2027 como prêmio de prazo e de risco[^8], não como ciclo esperado; quanto exatamente, a curva sozinha não separa.
- **A Focus está velha para esta pergunta:** foi coletada até 23/10. A divergência de +403 p.b. em dezembro de 2027 mistura prêmio com a pesquisa que ainda não viu o choque.
- **Espaço para surpresa:** em 04/11 a curva precifica manter, então um corte seria surpresa baixista (11%) e uma alta, altista (14%). Em 09/12, manter com comunicação paciente derrubaria a ponta curta; é o desfecho mais provável (54%).

### Q4 — Por que a central e por que a distribuição

**A central é o que o modelo faz com o juro real de 10 anos do pós-choque.** Na regra (R) a Selic segue a âncora, NTN-B de 10 anos mais a meta: no simulador, +1 p.p. em `rr_10a` em todos os trimestres sobe a Selic de fechamento do 4T26 em 1,00 p.p. e não muda o hiato (G `pm_sensibilidade`), porque a curva IS mede o aperto contra a mesma âncora. A história econômica é a do mapa (2.5), lida ao contrário: um salto do juro real longo por prêmio fiscal precifica disciplina fiscal mais fraca à frente, mais demanda e mais inflação, isto é, um neutro mais alto (ata da 281ª, §8), e a mesma Selic fica menos apertada; o modelo responde segurando a Selic acima do que daria com o juro de outubro. No base, com a NTN-B de 10 anos em 8,05% do 1T27 em diante (a de 26/10, segurada), a Selic fecha o 4T26 em 13,49%; no downside, com a média de outubro (6,93%), em 12,53% — quase toda a diferença entre os dois cenários é a âncora. Depois a Selic do modelo cai devagar, para 12,39% no 1T28, porque a expectativa do modelo converge (Focus de 12 meses de 4,16% no 4T26 para 3,52% no 1T28) e o hiato fica negativo (−0,51% no 1T28), o que encolhe o termo de desvio da regra.

**Onde acho que o modelo erra, e por que isso vai para a assimetria e não para a central:**
- Ele parte do 3T26 e não vê o salto de 26/10 na PTAX: projeta 5,24 de fechamento no 4T26 contra 5,50 no mercado (`cmb_ptax` · 26/10). O CDS a 137 p.b. explica pouco do salto; o resto é resíduo da equação do câmbio, que é do agente de câmbio (pedido na seção 4).
- A expectativa do modelo começa em 4,16% no 4T26, abaixo da Focus de 12 meses observada em 23/10, 4,53% (`expc_focus`), que subiu 0,35 p.p. em três meses; e a inflação implícita de 1 ano saltou para 7,87%. O modelo vê as expectativas melhorando quando a última leitura vai no outro sentido.
- A regra (R) não tem câmbio nem prêmio; o Copom tem o câmbio na lista de riscos (comunicado da 281ª, §4) e o prêmio na leitura do neutro (ata da 281ª, §8).

Os três apontam para cima, e por isso P(up) − P(down) é positivo em todos os trimestres, maior em 4T26 a 2T27, quando a decisão sobre o choque se resolve. A assimetria cai até o 1T28 porque, no regime de alta, o Copom volta a cortar em 2027 com o hiato negativo.

**A distribuição** é a mistura de três regimes, com passos reunião a reunião (seção 3.3): reversão do choque e cortes retomados (20%), pausa longa em 13,75% com cortes a partir do 2T27 (45%), ciclo de alta (35%). A pausa é o regime mais provável e é o que a faixa base descreve no 4T26.

### Notícias

Rodada 1, sem notícias. Os fatos de que a tese depende estão em Pedidos, ao agente web (seção 4).

### Olhado, sem sinal

- Reservas internacionais · US$ 364,9 bi (`cmb_reservas_bc` · 26/10) · −0,1 desde 22/10 e nenhuma intervenção à vista ou em linha no mês até 26/10 · diria algo se o BC vendesse à vista ou em linha, o gatilho de E4.
- Swap cambial do BC · −US$ 91,6 bi (`cmb_reservas_bc` · ago) · dado de agosto, anterior ao choque · diria algo se o estoque crescesse acima dos vencimentos em outubro ou novembro.
- Fed Funds · 3,88% no ponto médio (`us_interest_rate` · 27/10) · sem mudança desde 22/10 · diria algo se o FOMC mudasse o passo ou o caminho (S13).
- Juros de política dos pares · México 6,50%, Chile 4,50%, Colômbia 12,25%, Peru 4,25% (`inter_interest_rate` · 16–20/10) · nenhum mexeu depois do choque, que foi local · diria algo se os pares subissem juntos num choque global.
- Diferencial Selic − Fed Funds · 10,00 p.p. (`diferenciais_juros` · set) · anterior ao choque · diria algo se o carry deixasse de segurar o real (S5).
- Termos de troca · 108,44 (`cmb_termos_troca` · ago) · defasado e sem movimento que explique o choque · diria algo com queda forte das commodities, risco de baixa (iii) do Copom.
- Resultado primário de 12 meses · −0,62% do PIB (`fisc_nfsp` · ago) · anterior ao choque · diria algo com o plano fiscal de 2027 (S11, S12).
- Índice de difusão · 54,9% (`inflc_agregados` · set) · +2,7 p.p. em 12 meses, sem ruptura · diria algo acima de 60%, sinal de choque se espalhando (S8).

## 3. Premissas

### 3.1 Etapa 1 — o modelo

**Cenários:**
- **Base:** o choque de 26/10 fica no nível de 26/10 (juro real longo e CDS segurados) e não se aprofunda; o Copom pausa; a causa do choque é o pedido ao agente web.
- **Upside:** o choque se aprofunda: o prêmio fiscal e político sobe por dois trimestres (CDS a 200 p.b. no 1T27, NTN-B de 10 anos a 8,60%, novo máximo de dez anos — o máximo de 10 anos é 8,20%, `br_interest_rate`), a PTAX passa de 5,50 e a Focus de 2027–28 sobe; o Copom encerra o ciclo e sobe.
- **Downside:** o choque reverte, com movimentos do tipo do de 05/10: CDS a 115 p.b. (o nível de 21/10) e NTN-B de 10 anos na média de 01 a 23/10; o Copom retoma os cortes.

**Caminhos das exógenas** (G `pm_cenarios`):

| Exógena | Hoje (valor · tabela · data) | Cenário | 4T26 | 1T27 | 2T27 | 3T27 | 4T27 | 1T28 |
|---|---|---|---|---|---|---|---|---|
| Meta de inflação, 12 meses (`meta_12m`) · principal: este agente | 3,00 · `inflc_meta` · 2026 | base · upside · downside | 3,00 | 3,00 | 3,00 | 3,00 | 3,00 | 3,00 |
| Juro real de 10 anos (`rr_10a`) · principal: fiscal; aguarda fiscal (S11) | 8,05 · `br_interest_rate` · 26/10 | base | 7,76 | 8,05 | 8,05 | 8,05 | 8,05 | 8,05 |
| | | upside | 8,16 | 8,60 | 8,60 | 8,60 | 8,60 | 8,60 |
| | | downside | 6,95 | 6,93 | 6,93 | 6,93 | 6,93 | 6,93 |
| CDS 5 anos (`fiscal`) · principal: fiscal; aguarda fiscal (S11) | 137,43 · `cmb_risco_pais` · 26/10 | base | 137,43 | 137,43 | 137,43 | 137,43 | 137,43 | 137,43 |
| | | upside | 180 | 200 | 190 | 180 | 170 | 160 |
| | | downside | 115 | 115 | 115 | 115 | 115 | 115 |

- `meta_12m`: a meta contínua de 3,00% do CMN, sem decisão de mudança no dado (`inflc_meta`, 2026); igual nos três cenários, porque uma mudança da meta não é premissa deste ciclo e sim um pedido ao agente web (seção 4).
- `rr_10a` no 4T26: o simulador usa a média do trimestre. Os 17 pregões de outubro até 26/10 dão 7,00%; base = 8,05% no resto do trimestre (média 7,76); upside = 8,60% já em novembro (8,16); downside = volta à média de 01 a 23/10, 6,93% (6,95). Do 1T27 em diante, o nível segurado.
- CDS: no base, o de 26/10 segurado; no upside, sobe até o 1T27 e devolve 10 p.b. por trimestre; no downside, o nível de 21/10 (114,52, `cmb_risco_pais`).
- As outras exógenas (Fed Funds, inflação americana, dólar contra emergentes, S&P 500, commodities, volatilidade) ficam no padrão do simulador: aguarda externo (S13) e câmbio. A volatilidade implícita está segurada no 2T26 (12,19), sem dado do 3T26.

**Saída do modelo** (centrais; a faixa de 90% do posterior dos pesos está no G e não é intervalo de previsão[^9]):

| Variável | Cenário | 4T26 | 1T27 | 2T27 | 3T27 | 4T27 | 1T28 |
|---|---|---|---|---|---|---|---|
| Selic, fechamento (% a.a.) | base | 13,49 | 13,32 | 13,04 | 12,80 | 12,58 | 12,39 |
| | upside | 13,97 | 13,88 | 13,61 | 13,38 | 13,18 | 13,00 |
| | upside, R.t3 × 1,3 | 14,13 | 14,15 | 13,96 | 13,77 | 13,58 | 13,39 |
| | downside | 12,53 | 12,19 | 11,91 | 11,66 | 11,45 | 11,26 |
| IPCA 12 meses (%) | base | 5,28 | 4,86 | 4,34 | 4,35 | 4,24 | 4,08 |
| | upside | 5,30 | 4,93 | 4,46 | 4,49 | 4,35 | 4,14 |
| | downside | 5,27 | 4,84 | 4,31 | 4,31 | 4,20 | 4,06 |
| Focus IPCA 12m, média do trimestre (%) | base | 4,16 | 3,98 | 3,79 | 3,68 | 3,59 | 3,52 |
| | upside | 4,17 | 3,99 | 3,81 | 3,71 | 3,63 | 3,55 |
| Hiato (% do potencial) | base, upside e downside | 0,13 | −0,08 | −0,24 | −0,36 | −0,45 | −0,51 |
| PTAX, fechamento (R$/US$) | base | 5,24 | 5,27 | 5,27 | 5,26 | 5,27 | 5,30 |
| | upside | 5,42 | 5,53 | 5,49 | 5,43 | 5,40 | 5,38 |
| | downside | 5,17 | 5,21 | 5,21 | 5,20 | 5,22 | 5,24 |

O hiato é o mesmo nos três cenários porque a Selic acompanha a âncora um por um, e a IS mede o aperto contra a mesma âncora. O IPCA de 12 meses do modelo fica em 4,08% no 1T28 no base, contra 3,2% do Copom (`pm_copom_projecoes`, RPM 281ª) — a inflação do modelo é mais persistente que a do Copom; a leitura do caminho é do agente de inflação (S8).

### 3.2 Etapa 2 — o tempero qualitativo

**(i) Regra de juros (R), reação ao desvio da expectativa contra a meta — efeito mais forte que o estimado** · cenário upside
- Coeficiente `R.t3`: estimado 1,962, intervalo de 90% do posterior 1,148 a 2,726. Multiplicador × 1,3 (2,550), dentro do intervalo, no percentil 87.
- Efeito: Selic de fechamento do upside de 13,97 → 14,13 no 4T26 e de 13,61 → 13,96 no 2T27 (G `pm_cenarios`).
- Por quê: o Copom disse, por unanimidade, que expectativas desancoradas exigem "uma restrição monetária maior e por mais tempo do que outrora seria apropriado" (ata da 281ª, §10), e a desancoragem prolongada torna as expectativas mais sensíveis a choques e aumenta o repasse cambial (RPM set/26, 2.3, risco i). No upside a desancoragem é o que acontece; reagir mais a ela é a função de reação que o próprio Copom descreveu. Fica dentro do intervalo, então não afirmo que o histórico subestima o canal, só que este Copom está na ponta de cima dele.
- Onde entra: limite da cauda de upside.

**(ii-a) A reação do Copom ao câmbio e ao prêmio, que a regra (R) não tem** · cenários base e upside
- Hoje: PTAX 5,5007 (`cmb_ptax` · 26/10), 6,8% acima do condicionante de R$ 5,15 da 281ª; CDS 137 p.b. (`cmb_risco_pais` · 26/10).
- Por que o modelo não vê: (R) só lê a Selic defasada, a âncora e o desvio da Focus; o Copom reage à projeção no horizonte relevante, cujo câmbio de partida é o de mercado nos dez dias úteis antes da reunião (RPM set/26, Apêndice), e põe o câmbio depreciado entre os riscos de alta (ata da 281ª, §13). O canal câmbio → inflação → expectativa está no modelo, mas a PTAX do modelo não viu o salto de 26/10 (5,24 contra 5,50), e a reação discreta do Copom ao balanço de riscos não passa por nenhuma exógena.
- Efeito: +25 a +50 p.b. sobre o caminho do modelo até 09/12 enquanto a PTAX ficar acima de ~5,40; é o que faz o regime de alta (35%).
- Onde entra: assimetria do cenário base (+0,27 no 4T26) e limite da cauda de upside (14,25–14,50 em dezembro).

**(ii-b) Gradualismo e "serenidade e cautela"** · todos os cenários
- Hoje: cinco cortes seguidos de 25 p.b. desde 18/03 (`pm_copom_reuniao`); em 248 decisões desde 1999, nenhuma alta veio logo depois de um corte e os 14 ciclos de corte terminaram numa manutenção (G `pm_historico_reversoes`).
- Por que o modelo não vê: (R) é contínua sobre médias trimestrais; no downside ela leva a Selic de 13,75% a 12,53% até dezembro, o que pediria passos de 50 e 75 p.b. nas duas reuniões, quando o ciclo de 2026 andou só de 25 em 25.
- Efeito: comprime as caudas do 4T26 e do 1T27: o downside do modelo, 12,53, vira 13,25 em dezembro; uma alta em 04/11 fica em 14%.
- Onde entra: limites das caudas do 4T26 e 1T27; probabilidades da reunião de 04/11.

### 3.3 Da etapa 1 à tese

| Trimestre | Central (modelo, base) | Upside: modelo → com tempero | Downside: modelo → com tempero |
|---|---|---|---|
| 4T26 | 13,49 | 13,97 → 14,13 (R.t3) → 14,25 | 12,53 → 13,25 |
| 1T27 | 13,32 | 13,88 → 14,15 → 14,75 | 12,19 → 13,00 |
| 2T27 | 13,04 | 13,61 → 13,96 → 14,75 | 11,91 → 12,50 |
| 3T27 | 12,80 | 13,38 → 13,77 → 14,75 | 11,66 → 12,25 |
| 4T27 | 12,58 | 13,18 → 13,58 → 14,75 | 11,45 → 11,75 |
| 1T28 | 12,39 | 13,00 → 13,39 → 14,50 | 11,26 → 11,50 |

Os pontos "com tempero" são os percentis 10 e 90[^10] da distribuição da Selic de fechamento que sai da mistura dos três regimes, com passos de reunião a reunião (G `pm_distribuicao`). Os regimes, com a média da Selic de fechamento em cada um:

| Regime | Peso | 4T26 | 1T27 | 2T27 | 3T27 | 4T27 | 1T28 |
|---|---|---|---|---|---|---|---|
| Reversão: o choque se desfaz, cortes de 25 p.b. retomados | 20% | 13,45 | 13,05 | 12,65 | 12,25 | 11,85 | 11,60 |
| Pausa: 13,75% até o 1T27, cortes de 25 p.b. a partir do 2T27, mais firmes no 2S27 | 45% | 13,76 | 13,74 | 13,56 | 13,26 | 12,96 | 12,69 |
| Alta: ciclo de 50 a 100 p.b. até o 2T27, cortes no fim de 2027 | 35% | 14,14 | 14,54 | 14,64 | 14,56 | 14,39 | 14,16 |

A faixa base de cada trimestre contém a central do modelo e o grosso da pausa; as probabilidades da seção 1 são a massa da mistura dentro da faixa, acima e abaixo dela. A mediana da mistura é 13,75 até o 2T27, acima da central do modelo em todos os trimestres: é a forma numérica de dizer que a central não leva tempero e que a força que eu acredito estar ausente do modelo foi para a assimetria.

## 4. Para os outros agentes

### Respostas às entradas fixas

- **E1 (câmbio), em destaque:** a tese da seção 1, com as reuniões de 04/11 a 17/03. O motivo do destaque: em um pregão a curva passou a precificar alta em vez de corte a partir de dezembro (Q3). Para o carry à frente: no regime mais provável o diferencial fica parado em 13,75% até o 2T27; no de alta, sobe até ~14,6% de média no 2T27.
- **E2 (câmbio):** hoje, uma pausa é lida como credibilidade e um corte como validação da desancoragem. Uma alta só é lida como credibilidade se vier com sinal de segunda ordem nas expectativas (Q2); sem ele, num choque de prêmio fiscal e político, e com a dívida bruta em 82,9% do PIB (`fisc_divida` · ago), ela pode ser lida como custo da dívida, e o sinal do elo juro → câmbio deixa de ser garantido (mapa, 2.6).
- **E3 (câmbio), em destaque:** o Copom condicionou a projeção a R$ 5,15 seguindo a PPC (comunicado da 281ª, Tabela 1), listou "uma taxa de câmbio persistentemente mais depreciada" como risco de alta (ata, §13) e explicou a depreciação recente pelo diferencial de juros em queda (RPM set/26, 2.2). O motivo do destaque: a PTAX de 26/10, 5,50, está 6,8% acima do condicionante; o movimento é notícia para o Copom, não está no cenário dele.
- **E4 (câmbio):** o gatilho não disparou: não há intervenção à vista ou em linha em outubro até 26/10 (`cmb_reservas_bc`). Pela taxa: o Copom responde ao câmbio pela segunda ordem e pela projeção (ata da 281ª, §16); minha leitura é manter em 04/11 (75%), com 34% de a Selic estar acima de 13,75% depois de 09/12.
- **E5 (inflação):** a tese da seção 1.
- **E6 (inflação):** projeção do cenário de referência, IPCA 12 meses: 4,4 (3T26), 5,2 (4T26), 4,9 (1T27), 4,5 (2T27), 4,5 (3T27), 3,9 (4T27), 3,2 (1T28); administrados 3,9 / 5,3 / 4,5 / 4,0 / 4,3 / 3,5 / 3,2 (`pm_copom_projecoes`, RPM 281ª). Condicionantes: Selic da Focus, câmbio de R$ 5,15 pela PPC, Brent na curva futura por seis meses — partindo de US$ 90 no 3T26, pico no 4T26 e cerca de US$ 84 no 2T27 — e 2% ao ano depois, bandeira amarela até dezembro de 2026 e "neutra" depois, fim das subvenções e desonerações de combustíveis no prazo legal; a MP 1.391 (subvenção ao diesel) não está na projeção (RPM set/26, 2.2 e nota 45). Mensal de curto prazo: set 0,65, out 0,29, nov 0,41, dez 0,68 (RPM, Tabela 2.1.2). Condicionamento, não previsão do Copom.
- **E7 (atividade):** a tese da seção 1 e as caudas; a média do trimestre é a do modelo (base: 13,52 no 4T26, 13,46 no 1T27, G `pm_cenarios`) e o fechamento é a tese.
- **E8 (atividade):** a tabela de neutros de Q2. Contra o neutro do Copom (5,00%) a Selic real ex-ante está 3,82 p.p. acima; contra a âncora do modelo, 2,70 p.p., depois de cair 1,35 p.p. em um pregão porque a âncora carrega o prêmio. O aperto efetivo que a IS mede caiu sem o Copom mexer.
- **E9 (atividade):** "moderação gradual da atividade econômica, principalmente em setores mais cíclicos, embora ainda em patamar resiliente, e mercado de trabalho aquecido" (comunicado da 281ª, §2); hiato de 0,5% no 2T26 e 0,4% no 3T26, projetado em −0,4% no 1T28 (RPM set/26, 2.2); na edição de set/26 os trimestres de 2T25 a 2T26 foram revistos para cima de 0,10 a 0,15 p.p. (`pm_hiato_produto_vintages`); salários reais acima da produtividade (ata, §7).
- **E10 (fiscal):** a tese da seção 1.
- **E11 (fiscal):** a política fiscal age no curto prazo pela demanda e estruturalmente pelo prêmio a termo; "o esmorecimento no esforço de reformas estruturais e disciplina fiscal, o aumento de crédito direcionado e as incertezas sobre a estabilização da dívida pública têm o potencial de elevar a taxa de juros neutra" (ata da 281ª, §8). O RPM registra a divergência entre governo e mercado sobre o primário de 2027 e a dívida, e a piora do primário "associada a gastos mais elevados em ano eleitoral" (RPM set/26, Fiscal). O Copom lê fiscal como demanda, como prêmio e como neutro — os três.
- **E12 (fiscal):** a divisão está em "Como subordinado", abaixo.
- **E13 (fiscal):** a mesma leitura de E2.
- **E14 (externo):** a tese da seção 1.
- **E15 (externo):** ambiente externo "incerto em função da indefinição acerca dos conflitos armados no Oriente Médio e da incerteza sobre a política monetária em algumas economias avançadas" (comunicado da 281ª, §1); riscos de baixa vindos de fora: desaceleração global pelos choques de comércio e do petróleo, e queda das commodities (§4). Condicionante externo: Brent pela curva futura, partindo de US$ 90 (RPM set/26, 2.2).
- **E16 e E21:** não se aplicam: o principal de `rr_10a` é o fiscal. Meus insumos estão em "Como subordinado".
- **E17 (expectativas):** o Copom responde à desancoragem com "restrição monetária maior e por mais tempo" (ata da 281ª, §10); na regra do modelo, o coeficiente sobre o desvio da Focus contra a meta é 1,96 (`R.t3`, mediana). A minha resposta ao choque é Q1: pausa agora, alta se a Focus de 2027–28 subir.
- **E18 (expectativas):** o Copom julga a ancoragem em horizontes de dois ou três anos à frente (RPM set/26, 2.3); chama as expectativas de "desancoradas" em todos os horizontes (ata da 281ª, §10); registrou a Focus de 2028 subindo de 3,69% para 3,80% como "desancoragem adicional" (RPM set/26, 2.2); projeta 3,2% no 1T28 contra a Focus de 2028 de 3,75% (`expc_focus_periodo` · 23/10).
- **E19 (expectativas):** `meta_12m` em 3,00% nos seis trimestres (seção 3.1); nenhuma decisão do CMN de mudar a meta no dado (`inflc_meta`). O risco de mudança é um pedido ao agente web.
- **E20 (expectativas):** a tabela de Q3: curva menos Focus de +23 p.b. em 04/11 a +403 p.b. em dezembro de 2027, a maior parte prêmio, com a ressalva de que a Focus é de antes do choque.

### Pedidos

- **S1 (câmbio):** o salto de 9,2% de 26/10 é persistente? Tese dependente: o peso do regime de alta (35%) e as probabilidades de 09/12.
- **S2 (câmbio):** quanto do movimento de 23 a 26/10 é idiossincrático? O DXY subiu 0,6% desde 22/10; peso mexicano e dólar contra emergentes não têm dado de 26/10 no F. Tese dependente: se for idiossincrático, o prêmio chega às expectativas (Q2).
- **S3 (câmbio):** onde você põe a PTAX contra o condicionante de R$ 5,15, e qual será o câmbio de partida provável na projeção da reunião de 09/12 (média de dez dias úteis antes da semana da reunião)? Tese dependente: a alta em dezembro.
- **S4 (câmbio):** o real está precificando estresse fiscal e institucional? CDS e real andaram juntos em 05/10 e em 26/10. Tese dependente: o neutro mais alto que o modelo põe na âncora.
- **S5 (câmbio):** com a curva precificando alta, o carry voltou a segurar o real depois de 26/10? Tese dependente: E2, se uma alta aprecia ou não.
- **S6 (câmbio):** houve disfunção no mercado em 26–27/10 (liquidez, cupom cambial, leilões)? Tese dependente: gatilho de E4.
- **S7 (inflação):** repasse de uma depreciação de ~6–9% para o IPCA por grupo (alimentação, industriais, monitorados via combustíveis) no 4T26–2T27, e quanto disso é primeira ordem. Tese dependente: segunda ordem, o critério do Copom (ata da 281ª, §16).
- **S8 (inflação):** caminho do IPCA de 12 meses e dos serviços subjacentes até o 1T28, com o Brent a US$ 115 e o fim das subvenções a combustíveis. Tese dependente: o modelo dá 4,08% no 1T28 contra 3,2% do Copom; qual dos dois?
- **S9 (expectativas):** a Focus de 2027 e 2028 vai reagir ao choque (a de 30/10 é a primeira depois de 26/10)? E a inflação implícita de 1 ano em 7,87% é expectativa ou prêmio? Tese dependente: os sinalizadores de alta de Q2 (Focus 2027 acima de 4,6%, 2028 acima de 4,0%).
- **S10 (atividade):** o caminho do hiato até o 1T28 e se o choque de crédito e câmbio antecipa o hiato negativo. Tese dependente: o "cedo demais para subir" de Q2.
- **S11 (fiscal):** o caminho de `rr_10a` e do CDS que você escreve: o salto de 26/10 fica, reverte ou se aprofunda, e por quê? Tese dependente: a central inteira (seção 3.1; +1 p.p. em `rr_10a` move a central +1 p.p.).
- **S12 (fiscal):** o impulso fiscal de 2027 e se o primário responde à dívida no novo quadro. Tese dependente: o regime de alta e o neutro.
- **S13 (externo):** o caminho dos Fed Funds e o apetite global por risco; ficaram no padrão do simulador nesta rodada. Tese dependente: o peso do regime de reversão.
- **Ao agente de câmbio, sobre o modelo:** a equação (F) projeta 5,24 para o 4T26 contra 5,50 no mercado; se você aplicar multiplicador ou levar o salto ao P por outro caminho, o canal câmbio → inflação → Focus chega à minha regra.
- **Ao agente web:**
  1. O que aconteceu nos fins de semana de 03–04/10 e 24–25/10 que explique os pregões de 05/10 (PTAX −4,55%) e 26/10 (PTAX +9,19%, DI 2 anos +252 p.b., CDS +18 p.b.)? Se houve eleição presidencial, o resultado e o que o eleito disse sobre política fiscal, sobre o Banco Central (autonomia, diretoria) e sobre a meta de inflação. Tese dependente: os pesos dos regimes de reversão, pausa e alta.
  2. O presidente do BC ou diretores do Copom falaram depois de 26/10 sobre o câmbio, a reunião de 04/11 ou intervenção? O BC fez leilão à vista, de linha ou de swap em 26–27/10? Tese dependente: as probabilidades de 04/11 e o gatilho de E4.
  3. Há proposta ou discussão de mudar a meta de inflação (CMN) ou a lei de autonomia do BC? Tese dependente: `meta_12m`, de que sou principal.
  4. Anúncios fiscais para 2027 depois de 25/10 (meta de primário, PLOA, gastos novos). Tese dependente: o caminho de `rr_10a` e do CDS.
  5. Decisões sobre combustíveis em outubro: valor e datas da subvenção ao diesel da MP 1.391 e reajustes da Petrobras. Tese dependente: a projeção de monitorados (E6, S8).

### Como subordinado

- **`rr_10a` · principal: fiscal**
  - Insumos:
    - A NTN-B de 10 anos subiu 135 p.b. em 26/10, para 8,05%, a de 1 ano só 43 p.b. (`br_interest_rate` · 23 e 26/10). O real de 5 anos daqui a 5 anos foi de 6,70% para 8,17%. Um caminho de Selic mais alto apareceria na ponta curta; o salto concentrado na ponta longa é prêmio.
    - O juro real de política que a Focus espera é 6,02% em 2028 e 6,28% em 2029 (Selic 10,00% contra IPCA 3,75% e 3,50% · `expc_focus_periodo` · 23/10). A NTN-B de 10 anos está 2,03 e 1,77 p.p. acima, a medida do prêmio de prazo e fiscal sobre o caminho esperado (com a ressalva de que a Focus é de antes do choque).
    - A curva precifica um ciclo de alta até 15,78% em dezembro de 2027 (Q3); eu dou 35% a um ciclo de alta, que acaba em 2027. A parte de `rr_10a` que é caminho de política é menor que o salto.
    - No simulador, `rr_10a` move a Selic um por um, no mesmo trimestre, e não move o hiato (G `pm_sensibilidade`): o caminho que você escrever é, na prática, o nível da central da Selic.
  - Argumento: o caminho deveria partir do nível de 26/10, e não do padrão do simulador (7,84%, a média do 3T26) nem da média de outubro: 7,76% de média no 4T26 se o nível ficar, 8,05% do 1T27 em diante. Não argumento por queda gradual no base porque a reversão depende de um fato que o F não tem (pedido 1 ao agente web); se o fato for de reversão, o caminho cai para a média de outubro (6,93%), e a Selic do modelo cai quase 1 p.p. com ele.
  - Caminho de referência (também no JSON, não entra no P): 7,76 (4T26), 8,05 (1T27 a 1T28).

### Divergências

Rodada 1: nenhuma ainda. `meta_12m` não recebeu argumento do subordinado (fiscal) nesta rodada.

## 5. Placar

Primeiro ciclo: não há report final anterior deste agente (o ciclo de 2026-10-22 não tem `politica_monetaria_rf.md`). Nenhum trimestre nem reunião a conferir.

## 6. Sobre o modelo

| Fonte | O que sugere (regressor, defasagem, quebra, âncora) | Teste proposto (dado, amostra, que resultado mudaria a especificação) | Por que importa para a tese deste ciclo |
|---|---|---|---|
| Mapa conceitual, 2.5 (a âncora carrega prêmio de prazo e fiscal, não é o neutro do Copom) e RPM set/26, 2.2 (neutro de 5,00% no cenário de referência); `pm_sensibilidade` | Na (R), a Selic segue `rr_10a` + meta um por um e no mesmo trimestre. Liberar o coeficiente da âncora, ou trocar a âncora por uma medida líquida de prêmio (neutro do QPC, ou NTN-B de 10 anos menos uma estimativa de prêmio de prazo) | (R) com o coeficiente da âncora livre, 2006–2026, `br_interest_rate` (NTN-B 10 anos) e `pm_copom_reuniao`; e a mesma (R) com o neutro do QPC onde houver pergunta. Coeficiente bem abaixo de 1 (digamos < 0,5), ou ajuste melhor com o neutro de pesquisa, muda a âncora | Em 26/10 a NTN-B de 10 anos subiu 135 p.b. num pregão; o modelo leva quase isso inteiro à Selic no mesmo trimestre. A central deste ciclo é, na prática, o caminho de `rr_10a` |
| Comunicado da 281ª, §4 (câmbio depreciado como risco de alta); `pm_copom_reuniao` (2002: +300 p.b. em 14/10/2002, depois de duas manutenções) | (R) não tem câmbio nem prêmio de risco; acrescentar a variação trimestral da PTAX ou do CDS | (R) com a variação da PTAX (ou do CDS) no trimestre, 2003–2026, `cmb_ptax`, `cmb_risco_pais`, `pm_copom_reuniao`. Coeficiente positivo e estável, com ganho de ajuste fora da amostra, entra na regra | Neste ciclo o choque é de câmbio e prêmio, e a regra só o vê pela Focus, com defasagem: é o tempero (ii-a), que hoje está fora do modelo |

[^1]: A meta Selic muda só nas reuniões do Copom, cerca de duas por trimestre. O valor de fechamento do trimestre é a decisão da última reunião dentro dele: 09/12 para o 4T26, 17/03 para o 1T27, e assim por diante. O calendário oficial vai até 08/12/2027; para o 1T28 supus duas reuniões, como em todos os trimestres de 2022 a 2027.
[^2]: O Modelo Estrutural só tem a Selic média de cada trimestre. A de fechamento é derivada: a média deste trimestre e do seguinte, dividida por dois. Medida de 2006 a 2026, a regra erra 0,12 p.p. em média.
[^3]: As probabilidades de cada reunião saem de três regimes (reversão do choque, pausa, alta), cada um com a chance de cada passo em cada reunião; a tabela é a média ponderada. O mesmo cálculo dá a distribuição do fechamento de cada trimestre, então a tabela de reuniões e a tese não podem se contradizer.
[^4]: Comentário de processo: na rodada 1 o sistema não tem notícias. O report diz quando e quanto os preços se moveram e deixa a causa para a rodada 2, quando o agente web responde.
[^5]: Juro neutro é a taxa real que não acelera nem freia a economia. Se a Selic real (descontada da inflação esperada) está acima dele, a política é restritiva. Exemplo: Selic real de 8,8% contra neutro de 5,0% é um aperto de cerca de 3,8 p.p. O neutro não é observado; cada fonte o estima de um jeito.
[^6]: Dominância fiscal, na versão de Blanchard (2004) para o Brasil de 2002: quando a dívida é alta e o investidor teme o calote, subir os juros pode aumentar o risco percebido e depreciar a moeda, em vez de apreciá-la. É um espectro, não uma chave; o mapa conceitual registra a condição, a avaliação fiscal é do agente fiscal.
[^7]: A Selic esperada para cada reunião sai da curva de DI: a taxa a termo entre a vigência de uma decisão e a da seguinte, somada a 0,10 p.p., a distância usual entre o CDI e a meta Selic. É preço, não previsão. O cálculo deste report e o do F diferem em até 0,15 p.p. em algumas reuniões; o salto de 23 para 26/10 usa o mesmo cálculo nas duas datas.
[^8]: Prêmio de prazo é a remuneração extra que o investidor pede para travar um juro longo em vez de rolar juros curtos. Por isso a taxa de um contrato de DI para dezembro de 2027 não é só a Selic que o mercado espera para lá: ela inclui um prêmio, que sobe quando a incerteza sobe.
[^9]: A faixa que o modelo imprime cobre só a incerteza dos pesos estimados das equações, não os erros delas. Não é um intervalo de previsão; a distribuição da tese é deste agente.
[^10]: Percentil 10 é o valor abaixo do qual ficam 10% dos desfechos possíveis; percentil 90, o valor abaixo do qual ficam 90%. Entre os dois estão 80% dos desfechos.
