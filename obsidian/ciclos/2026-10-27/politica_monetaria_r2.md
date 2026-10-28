# Report — política monetária · ciclo 2026-10-27 · rodada 2

Dados até: pregão de 26/10/2026 (curvas, PTAX, CDS), Focus de 23/10, QPC da 281ª (23/09), documentos do Copom até o RPM de 24/09; notícias publicadas até 27/10 · Horizontes: 4T26 a 1T28, a meta Selic no fechamento de cada trimestre (a decisão da última reunião dentro dele)[^1]

## 1. Tese

| Variável | Trimestre | Central | Base: faixa · P | Upside: limite · P | Downside: limite · P | P(up) − P(down) |
|---|---|---|---|---|---|---|
| Meta Selic, fechamento do trimestre (% a.a.) | 4T26 | 13,34 | 13,30 a 13,80 (13,50 ou 13,75) · 62% | acima de 13,80 (alta até 09/12) · 32% | abaixo de 13,30 (dois cortes) · 6% | +0,26 |
| | 1T27 | 13,03 | 13,00 a 14,05 · 67% | acima de 14,05 · 29% | abaixo de 13,00 · 4% | +0,25 |
| | 2T27 | 12,67 | 12,65 a 14,05 · 62% | acima de 14,05 · 30% | abaixo de 12,65 · 8% | +0,22 |
| | 3T27 | 12,36 | 12,35 a 14,05 · 61% | acima de 14,05 · 27% | abaixo de 12,35 · 12% | +0,15 |
| | 4T27 | 12,12 | 12,10 a 14,05 · 64% | acima de 14,05 · 22% | abaixo de 12,10 · 14% | +0,08 |
| | 1T28 | 11,91 | 11,90 a 14,05 · 70% | acima de 14,05 · 16% | abaixo de 11,90 · 14% | +0,02 |

A central é a Selic de fechamento do P1, a rodada conjunta do Modelo Estrutural com o caminho de cada exógena dado pelo seu principal, sem ajuste[^2]. A Selic anda em degraus de 25 p.b., então cada faixa é um conjunto de decisões possíveis: no 4T26, 13,30 a 13,80 quer dizer "13,50 ou 13,75", e o limite de baixo fica em 13,30 só para conter a central, 13,34[^11].

**As duas próximas reuniões de cada trimestre, decisão a decisão** (Selic de partida 13,75%, decidida em 16/09; probabilidades deste agente, que somam 100% em cada linha e fecham nas linhas de 4T26 e 1T27 acima[^3]):

| Reunião | −50 p.b. | −25 p.b. | manter | +25 p.b. | +50 p.b. | Mais provável | Curva DI 26/10 | Focus 23/10 |
|---|---|---|---|---|---|---|---|---|
| 04/11/2026 | — | 11% | 77% | 9% | 3% | manter, 13,75 | 13,73 | 13,50 |
| 09/12/2026 | 1% | 15% | 57% | 16% | 11% | manter, 13,75 | 14,02 | 13,25 |
| 27/01/2027 | 1% | 19% | 56% | 15% | 9% | manter, 13,75 | 14,45 | 13,00 |
| 17/03/2027 | 1% | 19% | 60% | 15% | 5% | manter, 13,75 | 14,84 | 12,75 |

Curva DI e Focus: `br_di_grade` (26/10) e `expc_focus_copom` (23/10), a Selic de cada reunião na tabela "A Selic por reunião" do F.

- **Upside, acima da faixa: o Copom encerra a calibração e sobe a Selic.** No modelo, com os caminhos de cauda dos principais — CDS a 190 p.b. e NTN-B de 10 anos a 8,80% no 1T27 (fiscal), volatilidade implícita a 24% no 4T26 (câmbio) —, a Selic fecha o 4T26 em 14,02 e o 1T27 em 14,19; com a regra reagindo à expectativa 30% mais forte que o estimado (tempero i), em 14,18 e 14,46; com a reação do Copom ao câmbio e ao prêmio, que a regra (R) não tem (tempero ii-a), a 14,25 em dezembro e 14,75 no 1T27 (percentil 90[^10] da distribuição). É ruim para o Brasil: quer dizer câmbio, expectativas e prêmio piores que no base.
- **Downside, abaixo da faixa: os cortes voltam.** No modelo, um arcabouço fiscal que o mercado compre (CDS a 110 p.b., NTN-B de 10 anos a 6,90% e volatilidade a 12,5% no 1T27, caminhos de cauda do fiscal e do câmbio) leva a Selic a 12,71 no 4T26 e 12,12 no 1T27; o gradualismo do Copom (tempero ii-b) limita a 13,50 em dezembro e 13,00 em março (percentil 10). Só é boa notícia se vier da queda do prêmio. Parte dela (5 dos 18 p.p. do regime de cortes) é outro caminho, ruim: um Copom que volta a cortar com a PTAX acima de 5,40, sob a pressão de quem foi reeleito pedindo juro mais baixo (tempero ii-c).

**A tese em uma frase:** o Copom mantém 13,75% em 04/11 (77%) e em 09/12 (57%), porque cortar depois de a reeleição de 25/10 levar a PTAX a +9,2% e a inflação implícita de 1 ano a +1,2 p.p. num pregão validaria a desancoragem; o modelo, com o juro real de 10 anos que o fiscal devolve em parte, desenha cortes até 11,9% no 1T28, mas o risco é de alta — 32% de a Selic estar acima de 13,75% depois de dezembro — enquanto o ajuste fiscal prometido depois da eleição não tiver conteúdo.

**O que mudou desde a rodada 1** (antes → depois; o detalhe está em cada seção):

| O quê | Rodada 1 | Rodada 2 | Por quê |
|---|---|---|---|
| Central, 4T26 a 1T28 | 13,49 · 13,32 · 13,04 · 12,80 · 12,58 · 12,39 | 13,34 · 13,03 · 12,67 · 12,36 · 12,12 · 11,91 | a central passa a ser a do P1, que usa o `rr_10a` do fiscal (7,70 a 7,50) em vez do meu de referência (8,05 segurado) |
| Limite de baixo da faixa | 13,45 · 13,25 · 12,75 · 12,50 · 12,25 · 12,00 | 13,30 · 13,00 · 12,65 · 12,35 · 12,10 · 11,90 | conter a central nova; só no 1T27 a faixa ganha um degrau (13,00) |
| Pesos dos regimes (cortes · pausa · alta) | 20% · 45% · 35% | 18% · 50% · 32% | a causa do choque é conhecida e permanente (a eleição), e o governo respondeu com promessa de ajuste; seção 2, Q4 |
| 04/11 | 11 · 75 · 9 · 5 | 11 · 77 · 9 · 3 (−25 · manter · +25 · +50) | menos alta imediata no regime de alta: o governo reagiu e o dólar corrigiu em parte em 27/10 |
| Probabilidades por trimestre | 4T26: 59 · 34 · 7 | 4T26: 62 · 32 · 6 | os dois motivos acima; os outros trimestres na tabela da tese |
| `rr_10a`, caminho de referência (subordinado) | 7,76 · 8,05 × 5 | nenhum: divergência fechada | a decomposição da curva real mostra que o meu próprio caminho de Selic devolve parte do salto; seção 4 |
| Caminhos de cauda das exógenas dos outros | meus | os dos principais (fiscal, câmbio) | regra da rodada 2 |
| Novo tempero | — | (ii-c) pressão política por juro mais baixo, no downside | notícia de 24/10 (nível B) |

## 2. Argumentação

### O fato do ciclo: a reeleição de 25/10 e o pregão de 26/10

A causa do salto de 26/10 deixou de ser pedido: Luiz Inácio Lula da Silva foi reeleito no 2º turno de 25/10 (CNN Brasil · 25/10 · nível A), depois de um 1º turno, em 04/10, em que Flávio Bolsonaro ficou à frente e o dólar caiu a R$ 5 (Agência Brasil · 05/10 · nível A). Os dois pregões de outubro que a rodada 1 descreveu sem causa são as duas leituras do mercado sobre a eleição: a CNN Brasil registrou que "o mercado vinha tratando a vitória de Flávio como a possibilidade de uma virada na política fiscal" (25/10 · nível A). De 23/10 para 26/10 a PTAX subiu 9,19% (5,0377 → 5,5007 · `cmb_ptax`), o CDS de 5 anos 18 p.b. (119 → 137 · `cmb_risco_pais`), o DI de 2 anos 252 p.b. e a NTN-B de 10 anos 135 p.b. (`br_interest_rate` · 23 e 26/10). Os juros futuros longos chegaram a subir 182 p.b. no dia e o Tesouro cancelou os leilões de prefixados e de títulos de inflação de 27 a 29/10 (InfoMoney/Estadão Conteúdo · 26/10 · nível A); Lais Costa (Empiricus Research) disse que "o mercado está muito disfuncional" (InfoMoney/Reuters · 26/10 · nível B).

Para a política monetária o salto tem três partes, e cada dado responde a uma:
- **O câmbio passou do condicionante do Copom:** a PTAX de 5,50 está 6,8% acima dos R$ 5,15 do cenário de referência da 281ª (comunicado, Tabela 1), e uma "taxa de câmbio persistentemente mais depreciada" é o risco de alta (iii) da lista do Copom (ata da 281ª, §13). O agente de câmbio leu o salto como idiossincrático e, na maior parte, persistente (cambio_r1, E1 e E2), e a causa conhecida reforça a leitura: um resultado de eleição não se desfaz como um boato.
- **A compensação por inflação subiu em todos os prazos:** a inflação implícita subiu 1,19 p.p. em 1 ano, 1,23 em 2, 1,20 em 5 e 0,89 em 10 anos, de 23 para 26/10 (`br_interest_rate`); em 1 ano ela está em 7,87%, contra a Focus de 12 meses em 4,53% (`expc_focus` · 23/10). O agente de expectativas mediu as altas de 2 e 5 anos como as maiores num dia desde 2006 (expectativas_r1).
- **A maior parte da alta do juro real longo é prêmio, não caminho de política.** Dos +135 p.b. da NTN-B de 10 anos, os dois primeiros anos da curva real, onde mora o caminho que o Copom controla, respondem por +22 p.b.; os anos 2 a 5, por +40; os anos 5 a 10, por +73 (`br_interest_rate` · 23 e 26/10, juros reais a termo[^12]). O juro real a termo entre 1 e 2 anos subiu 184 p.b., para 9,62%: é ali que a curva cobra o ciclo de alta da Selic que ela precifica para 2027 (Q3).

O que veio depois do pregão ainda não está no F.[^4] Em 27/10 o dólar abriu em queda de 1,29%, a R$ 5,333 às 9h52, "em movimento de correção" (InfoMoney · 27/10 · nível B). O ministro da Fazenda, Dario Durigan, disse que o governo "pretende ampliar o superavit primário em 2027" (Poder360 · 26/10 · nível B), que vai propor ajustes para buscar "o centro da meta de maneira formal" (CNN Brasil e Exame · 27/10 · nível A, sem o conteúdo do projeto) e que a reação do mercado foi "de posição" (Poder360 · 27/10 · nível B). Isso mostra que o governo respondeu ao preço, não que o ajuste vá acontecer; é a história do downside, não um fato da base.

### Q1 — O que o Copom vai fazer?

**Em 04/11: manter 13,75% e encerrar a calibração (77%).** Três coisas do Copom sustentam a pausa, e uma regularidade sustenta que ela venha antes de uma alta:
- A função de reação declarada olha a projeção no horizonte relevante (1T28) e reage aos efeitos de segunda ordem dos choques (ata da 281ª, §16). O salto mexe nos dois condicionantes que a governança atualiza sozinha: a trajetória de Selic da Focus e o câmbio de partida, que é a média de dez dias úteis encerrados na semana anterior à da reunião (ata da 281ª, nota 2). Para 04/11 a janela acaba em 30/10 e contém os pregões depois de 26/10.
- A guidance é condicional: "a magnitude total do ciclo de calibração será estabelecida à luz de novas informações" (comunicado da 281ª, §6), com "serenidade e cautela" (§8) e a conclusão unânime de que, com expectativas desancoradas, "exige-se uma restrição monetária maior e por mais tempo do que outrora seria apropriado" (ata da 281ª, §10). Cortar oito dias depois do salto iria contra as três frases.
- O mercado já tirou o corte do preço: a curva de 26/10 dá 13,73% para 04/11 (`br_di_grade`), e a Reuters relatou que o mercado "passou a precificar a possibilidade de o Copom […] não cortar a Selic" (InfoMoney/Reuters · 26/10 · nível B). Antes do choque a pausa já dividia: 53% dos respondentes do QPC da 281ª esperavam manutenção em novembro (`expc_qpc` · 23/09).
- Em 248 decisões desde 1999 o Copom nunca passou de um corte direto para uma alta: os 14 ciclos de corte terminaram numa manutenção, e as oito reversões para alta tiveram de uma a cinco manutenções no meio (`pm_copom_reuniao`, 1999–2026). Por isso uma alta já em 04/11 fica em 12%, e não em zero: em 2002 a primeira alta, de 300 p.b., veio depois de só duas manutenções (mesma tabela, 14/10/2002).

A alta imediata caiu de 14% para 12% porque o governo respondeu ao preço em menos de 24 horas e o dólar corrigiu em parte em 27/10 (as notícias acima, nível B): uma alta oito dias depois, com a resposta fiscal ainda sem conteúdo, anteciparia o que o Copom diz só fazer quando a segunda ordem aparece. O presidente do BC, Gabriel Galípolo, disse em 27/10, sobre a escala 6x1, que "a gente vai esperar a implementação para saber se precisa agir" (InfoMoney · 27/10 · nível B): é a postura de reagir ao efeito, não de antecipá-lo, mas a fala é sobre o mercado de trabalho, não sobre câmbio nem sobre 04/11.

O corte de 25 p.b. fica com 11%. **Mas** há uma pressão nova a favor dele: Lula disse, na véspera da votação, "Quero que o Banco Central baixe o juro" (Poder360 · 24/10 · nível B). A frase mostra o que o reeleito quer, não o que o Copom fará; ela entra no downside como risco de um Copom leniente (tempero ii-c), e é por ela que o corte em 04/11 não caiu mais. O que limita esse risco no horizonte da tese: Galípolo disse que "meu mandato vai até o final de 2028" (CNN Brasil · 27/10 · nível B), e o agente web não achou, na janela, proposta de mudar a meta de inflação ou a lei de autonomia do BC (notícias, "Sem notícia", item 6).

**Em 09/12 e no 1T27: a decisão depende de o prêmio ficar.** Manter é a moda (57% em dezembro), mas a Selic acima de 13,75% depois de 09/12 tem 32% (27% de alta só nessa reunião: 16% de +25 e 11% de +50). O que move a decisão, em ordem: a Focus de 2027 e 2028 (hoje 4,34% e 3,75% · `expc_focus_periodo` · 23/10, pesquisa de antes do choque), a média dos núcleos e os serviços subjacentes (5,32% em 12 meses, contra 5,00% três meses antes · `inflc_decomposicao` · set) e o câmbio de partida da projeção de dezembro. **Apesar de** a atividade desacelerar — IBC-Br −0,8% em três meses até agosto (`atv_ibcbr`), e o agente de atividade pondo o hiato em −0,08 já no 1T27, com 32% de cauda abaixo no 4T26 (atividade_r1) —, o Copom já tinha a moderação no cenário (ata da 281ª, §5) e só uma desaceleração mais forte é risco de baixa (comunicado, §4).

O Copom está agindo como sua reação usual implica: o ciclo de 2026 foi de cinco cortes iguais de 25 p.b. desde 18/03, de 15,00% para 13,75% (`pm_copom_reuniao`), com o horizonte relevante projetado em 3,2% nas duas últimas reuniões (`pm_copom_projecoes`, 281ª e 280ª), acima da meta de 3,00%. Um Copom que corta com a projeção acima da meta aceita convergência lenta; um choque cambial dessa ordem tira essa folga.

### Q2 — O que o Copom deveria fazer, pelos dados?

**Manter 13,75% em novembro e dezembro, dizer que a calibração acabou, e subir só se aparecer segunda ordem.** O argumento tem três partes.

*A política já é restritiva por qualquer neutro de pesquisa ou do Copom.* A Selic real ex-ante, com a Focus de 12 meses, é 8,82% (`br_interest_rate` e `expc_focus` · 23/10)[^5]:

| Neutro | Valor | Selic real ex-ante acima dele | Fonte |
|---|---|---|---|
| Copom, cenário de referência | 5,00% | +3,82 p.p. | RPM set/26, 2.2 |
| QPC, 5 anos | 5,50% | +3,32 p.p. | `expc_qpc` · R279 |
| QPC, 2 anos | 6,00% | +2,82 p.p. | `expc_qpc` · R279 |
| QPC, curto prazo | 6,40% | +2,42 p.p. | `expc_qpc` · R279 |
| Âncora do modelo (NTN-B 10a + meta), nominal, 26/10 | 11,05% | Selic nominal +2,70 p.p. | `br_interest_rate` · 26/10 |
| Âncora do modelo no 4T26 do P1 (`rr_10a` 7,70 + meta) | 10,70% | Selic nominal +3,05 p.p. | P1, caminho do fiscal |

Uso o intervalo do Copom e do QPC para julgar o aperto, porque são o que o Copom diz usar (RPM set/26, 2.2), e a âncora do modelo como alerta: ela carrega o prêmio de mercado (mapa, 2.5). De 23 para 26/10 a âncora subiu de 9,70% para 11,05% e a distância da Selic até ela caiu de 4,05 para 2,70 p.p. sem o Copom mexer (`br_interest_rate`). Pela leitura do modelo, que é a do Copom — incerteza sobre a dívida eleva o juro neutro (ata da 281ª, §8) —, o choque de prêmio afrouxou a política. É o argumento contra cortar. O caminho do fiscal devolve parte do prêmio (âncora de 10,70% na média do 4T26), e a folga volta a +3,05 p.p.; é dessa devolução que sai a central mais baixa desta rodada (Q4).

*A inflação e as expectativas não dão folga.* O IPCA de 12 meses está em 4,58% (`inflc_agregados` · set), acima dos 4,40% que o Copom projetava para setembro (RPM set/26, Tabela 2.1.2), e o IPCA-15 de outubro em 4,62%. O agente de inflação põe o IPCA de 12 meses em 4,08% no 1T28, com o risco para cima, e lê o choque corrente como de primeira ordem, mas com a segunda ordem "em risco por serviços subjacentes e expectativas" (inflacao_r1, IN-E3); o P1 dá 4,19%, contra 3,2% do Copom. O agente de expectativas mostra que as 16 pesquisas Focus já feitas no 4T26 têm média de 4,52%, contra 4,17% que o modelo dá para o trimestre inteiro (expectativas_r1). O hiato da última edição é positivo, 0,41% no 3T26, e os trimestres recentes foram revisados para cima, de +0,10 a +0,15 p.p. (`pm_hiato_produto_vintages` · edição de set/26); o desemprego está em 5,3% (`mt_pnad` · ago).

Há um risco novo nos monitorados, em sentido duplo. Lula falou em "subsidiar o óleo diesel e a gasolina" (Poder360 · 24/10 · nível B), Durigan disse que, com o Brent alto, "deve ser a proposta do presidente, manter essa ajuda" em 2027 (Poder360 · 23/10 · nível B), e a Abicom, que os preços da Petrobras "estão muito defasados" e o reajuste "terá que ser de maneira lenta e gradual" (CNN Brasil · 26/10 · nível B). A projeção do Copom supõe o fim das subvenções no prazo legal (RPM set/26, 2.2, nota 45); mantê-las baixa o IPCA medido em 2027 e transfere o custo para o fiscal, e uma meta cumprida por subsídio é custo adiado (mapa conceitual, 2.2). Quanto isso move o IPCA é do agente de inflação (S8).

*Mas subir agora seria cedo.* A transmissão está funcionando: a inadimplência da carteira livre de pessoa física subiu 1,04 p.p. em 12 meses, para 8,01% (`cred_credito_resumo` · ago), e o comprometimento de renda com a dívida 1,40 p.p., para 28,72% (`cred_credito_familias` · jul) — premissa *assumida*, crédito sem agente. O hiato deve virar negativo (RPM set/26, 2.2: −0,4% no 1T28; atividade_r1: −0,08 já no 1T27). E há dois sinais de que uma alta, agora, poderia não apreciar o real: no pregão de 26/10 o carry à frente subiu de 9,14 para 10,82 p.p. e o real caiu 9% (cambio_r1, E5), e o agente fiscal vê dois dos três conjuntos de sinais de dominância fiscal presentes, nenhum completo (fiscal_r1, F5)[^6]. A alta deveria vir com sinal de segunda ordem: Focus de 2027 acima de 4,6% ou de 2028 acima de 4,0%, serviços subjacentes acelerando no trimestre, ou PTAX acima de 5,40 por mais de duas semanas até a reunião de dezembro.

**A distância entre Q1 e Q2 é pequena em novembro e cresce em dezembro.** Em novembro as duas dizem manter. Em dezembro o Copom pode subir antes do que os dados pedem, empurrado pela curva, que já precifica a alta (Q3): esse é o peso do regime de alta (32%) na cauda de upside. O risco oposto, um Copom que retoma cortes com o câmbio em 5,50 — o BC "dócil" do mapa (Parte 1, item 5) —, alimenta o downside e seria ruim para a credibilidade; ele ganhou uma fonte nesta rodada (a fala de Lula de 24/10) e fica em 5 p.p., porque o comunicado e a ata da 281ª não deixam espaço para ele e o presidente do BC tem mandato até 2028.

### Q3 — O que o mercado precifica, e onde diverge

| Reunião | Curva DI 23/10 | Curva DI 26/10 | Salto (p.b.) | Focus 23/10 | Curva 26/10 − Focus (p.b.) | Média da minha distribuição | Curva 26/10 − minha média (p.b.) |
|---|---|---|---|---|---|---|---|
| 04/11/2026 | 13,57 | 13,73 | +18 | 13,50 | +23 | 13,76 | −3 |
| 09/12/2026 | 13,45 | 14,02 | +54 | 13,25 | +77 | 13,82 | +20 |
| 27/01/2027 | 13,26 | 14,45 | +124 | 13,00 | +145 | 13,85 | +60 |
| 17/03/2027 | 13,16 | 14,84 | +161 | 12,75 | +209 | 13,86 | +98 |
| 16/06/2027 | 12,81 | 15,31 | +247 | 12,25 | +306 | — | — |
| 22/09/2027 | 12,46 | 15,54 | +299 | 12,00 | +354 | — | — |
| 08/12/2027 | 12,46 | 15,78 | +323 | 11,75 | +403 | — | — |

Curva 26/10, Focus e diferença: tabela "A Selic por reunião: curva DI e Focus" do F (`br_di_grade`, `expc_focus_copom`). Curva 23/10 e salto: `br_di_grade` · 23 e 26/10, no mesmo método aproximado[^7].

- **Contra Q1:** em novembro a curva e eu dizemos o mesmo, manter. Em dezembro ela está 20 p.b. acima da média da minha distribuição, e em março 98 p.b. A curva desenha um ciclo de alta até 15,78% em dezembro de 2027; eu dou 32% a um ciclo de alta, com média de 14,61% no 2T27 nesse regime (seção 3.3).
- **Contra Q2:** eu não subiria antes de ver segunda ordem; a curva já cobra a alta.
- **Contra o que o Copom sinaliza:** a projeção de 3,2% no 1T28 foi feita com a trajetória da Focus (RPM set/26, 2.2), que na curva de 26/10 está 2 a 4 p.p. abaixo do preço. O Copom não endossa nenhuma das duas: a Focus é condicionante de governança, não a previsão dele (mapa, 2.2).
- **Prêmio, não só caminho, e num mercado que não funcionava:** o salto cresce com o prazo e chega a +323 p.b. em dezembro de 2027, além de onde qualquer comunicação do Copom alcança; na curva real, os anos 5 a 10 levaram 73 dos 135 p.b. (seção acima). A curva de 26/10 foi formada com o Tesouro fora dos leilões (nível A) e num mercado que um analista nomeado chamou de "muito disfuncional" (nível B): em pregão assim, a taxa carrega mais prêmio de liquidez e de risco[^8] do que expectativa, e a leitura do caminho fica pior. Leio a maior parte da diferença entre curva e Focus em 2027 como prêmio; quanto exatamente, a curva sozinha não separa.
- **A Focus está velha para esta pergunta:** foi coletada até 23/10, antes da eleição. A pesquisa de 30/10 é a primeira com o resultado, e não estará no F deste ciclo.
- **Espaço para surpresa:** em 04/11 a curva precifica manter, então um corte seria surpresa baixista (11%) e uma alta, altista (12%). Em 09/12, manter com comunicação paciente derrubaria a ponta curta; é o desfecho mais provável (57%).

### Q4 — Por que a central e por que a distribuição

**A central é o que o modelo faz com o juro real de 10 anos que o fiscal escreve.** Na regra (R) a Selic segue a âncora, NTN-B de 10 anos mais a meta, e na curva IS o aperto é medido contra a mesma âncora; por isso o `rr_10a` move a Selic um por um e não move o hiato. O agente fiscal, principal dessa exógena, leu a maior parte dos +135 p.b. de 26/10 como prêmio e escreveu uma devolução parcial: 7,95% no resto do 4T26 (média de 7,70%), 7,80% no 1T27, a média do 3T26, e queda de 0,3 p.p. ao longo de 2027, supondo a Selic voltando a cair e o juro americano parado (fiscal_r1, F5). A história econômica é a do mapa (2.5): um juro real longo que cai porque o prêmio fiscal comprime precifica uma consolidação à frente, menos demanda e menos inflação, e a mesma Selic fica mais apertada contra a demanda que vem; o modelo responde abrindo espaço para cortar. Com o meu caminho de referência da rodada 1 (8,05% segurado) e todo o resto igual ao P1, a Selic fecharia em 13,50 no 4T26 e 12,46 no 1T28; o P1 dá 13,34 e 11,91 — a diferença, de 0,16 a 0,55 p.p., é a diferença entre os dois caminhos de `rr_10a`. O hiato sai igual nos dois. Depois, a Selic do modelo cai devagar porque a expectativa do modelo converge (Focus de 12 meses de 4,17% no 4T26 para 3,57% no 1T28) e o hiato fica negativo (−0,52% no 1T28), o que encolhe o termo de desvio da regra.

**Onde acho que o modelo erra, e por que isso vai para a assimetria e não para a central:**
- *Ele trata prêmio como neutro.* Dos +135 p.b., 73 estão nos anos 5 a 10 da curva real. O Copom diz que a incerteza fiscal eleva o neutro (ata da 281ª, §8), mas não corta porque o prêmio caiu um pouco: corta quando a projeção e as expectativas deixam. Um prêmio que devolve 25 p.b. abre, no modelo, 25 p.b. de corte no mesmo trimestre; no Copom, abre nada enquanto a Focus não reagir. O tamanho: com o caminho do fiscal, o prêmio de 26/10 põe 0,76 a 1,00 p.p. na Selic de fechamento do modelo, contra a mesma conta com o `rr_10a` na média de 01 a 23/10 (6,93%), e o hiato sai igual (Modelo Estrutural, `br_interest_rate`). A (R) não tem um peso livre na âncora para eu multiplicar, então isso não entra como tempero (i): a minha mistura de regimes não segue o `rr_10a`, e a Selic dela é a do Copom reagindo a expectativas e câmbio, que pesa mais do que esse 0,8 a 1,0 p.p. (a mediana fica acima da central). Se o prêmio cair sem as expectativas mexerem, o lugar disso é o regime de cortes (18%).
- *A expectativa do modelo começa baixa.* O modelo dá 4,17% de média para o 4T26; as pesquisas já feitas no trimestre têm média de 4,52% (expectativas_r1), e a inflação implícita de 1 ano saltou para 7,87%. Com o peso da inércia na (E) 20% maior, ainda dentro do posterior, o próprio agente de expectativas mostra a Selic média do 1T28 subindo cerca de 0,5 p.p. no modelo (expectativas_r1, tempero i). O multiplicador é dele; o efeito chega à minha regra e está na assimetria.
- *O modelo corta antes do que o Copom costuma.* Fechar o 4T26 em 13,34 pede quase dois cortes de 25 p.b. até 09/12, com a curva precificando alta; os ciclos de corte de 1999–2026 terminaram em manutenção, não em mais corte depois de um choque (`pm_copom_reuniao`).
- *A regra (R) não tem câmbio nem prêmio.* Este argumento enfraqueceu desde a rodada 1: com a volatilidade do agente de câmbio, o P1 põe a PTAX em 5,435 no fechamento do 4T26, contra 5,50 no mercado (`cmb_ptax` · 26/10); na rodada 1 o modelo dava 5,24. O que sobra é a reação discreta do Copom ao balanço de riscos (comunicado da 281ª, §4), que não passa por nenhuma exógena.

Os quatro apontam para cima, e por isso P(up) − P(down) é positivo em todos os trimestres, maior em 4T26 a 2T27, quando a decisão sobre o prêmio se resolve. A assimetria cai até o 1T28 porque, no regime de alta, o Copom volta a cortar em 2027 com o hiato negativo.

**A distribuição** é a mistura de três regimes, com passos reunião a reunião (seção 3.3): cortes retomados (18%: 13 p.p. de reversão do prêmio, 5 p.p. de Copom leniente), pausa longa em 13,75% com cortes a partir do 2T27 (50%), ciclo de alta (32%). Os pesos da rodada 1 eram 20%, 45% e 35%. Mudaram por três notícias: a causa do choque é um resultado de eleição, que não se reverte como um ruído, o que tira peso da reversão; o governo respondeu ao preço em 24 horas (Durigan, níveis A e B) e o dólar corrigiu em parte em 27/10 (nível B), o que tira peso da alta; e a fala de Lula pedindo juro mais baixo (nível B) põe dentro do regime de cortes uma versão ruim dele. A pausa ganha o que os dois extremos perdem.

### Notícias

Usadas (veículo · data · nível · papel):
- A causa: CNN Brasil · 25/10 · A (reeleição; sustenta a história dos cenários); Agência Brasil · 05/10 · A (1º turno; o pregão de 05/10); InfoMoney/Estadão · 26/10 · A (juros longos e leilões cancelados; Q3); InfoMoney/Reuters · 26/10 · B (mercado "disfuncional"; precificação de não corte; Q1 e Q3).
- A resposta do governo: Poder360 · 26/10 · B (ampliar o superávit); CNN Brasil e Exame · 27/10 · A (projeto para o centro da meta fiscal); Poder360 · 27/10 · B (reação "de posição"). Movem os pesos dos regimes (downside), não a base.
- O BC: CNN Brasil · 27/10 · B (Galípolo, mandato até 2028); InfoMoney · 27/10 · B (Galípolo sobre a 6x1); InfoMoney · 27/10 · B (rolagem de swap; dólar em queda). Q1 e E4.
- O reeleito e os preços administrados: Poder360 · 24/10 · B (Lula: juro mais baixo e subsídio a combustíveis; tempero ii-c e Q2); Poder360 · 23/10 · B (Durigan: subsídio em 2027); CNN Brasil · 26/10 · B (Abicom). Q2 e S8.
- Meta de inflação: o agente web não achou nada na janela (item 6 da pauta), o que sustenta o caminho de `meta_12m`.

### Olhado, sem sinal

- Reservas internacionais · US$ 364,9 bi (`cmb_reservas_bc` · 26/10) · −0,1 desde 22/10, nenhuma intervenção à vista ou em linha no mês; em 27/10 só a rolagem programada de swap (InfoMoney · 27/10 · nível B) · diria algo se o BC vendesse à vista ou em linha, o gatilho de E4.
- Swap cambial do BC · −US$ 91,6 bi (`cmb_reservas_bc` · ago) · dado de agosto, anterior ao choque · diria algo se o estoque crescesse acima dos vencimentos em outubro ou novembro.
- Fed Funds · 3,88% no ponto médio (`us_interest_rate` · 27/10) · sem mudança desde 22/10; o agente externo espera mais uma alta no 4T26 (externo_r1) · diria algo se o FOMC acelerasse o passo, o que pesaria no dólar contra emergentes (S13).
- Juros de política dos pares · México 6,50%, Chile 4,50%, Colômbia 12,25%, Peru 4,25% (`inter_interest_rate` · 16–20/10) · nenhum mexeu depois do choque, que foi local · diria algo se os pares subissem juntos.
- Diferencial Selic − Fed Funds · 10,00 p.p. (`diferenciais_juros` · set) · anterior ao choque · diria algo se o carry deixasse de segurar o real por mais de um pregão (S5).
- Termos de troca · 108,44 (`cmb_termos_troca` · ago) · defasado e sem movimento que explique o choque · diria algo com queda forte das commodities, risco de baixa (iii) do Copom.
- Resultado primário de 12 meses · −0,62% do PIB (`fisc_nfsp` · ago) · anterior ao choque e à promessa de ajuste · diria algo com o conteúdo do projeto de Durigan (S12).
- Índice de difusão · 54,9% (`inflc_agregados` · set) · +2,7 p.p. em 12 meses, sem ruptura · diria algo acima de 60%, sinal de choque se espalhando (S8).
- Alckmin na Fazenda · "A proposta ainda está em discussão" (CNN Brasil/Reuters · 05/10 · nível C) · fonte anônima, de antes do 2º turno, sem confirmação · diria algo se o nome da equipe econômica fosse anunciado.

## 3. Premissas

### 3.1 Etapa 1 — o modelo

**Cenários:**
- **Base:** o prêmio de 26/10 devolve uma parte até o 1T27 e cai devagar em 2027, como escreve o fiscal; o ajuste fiscal prometido não ganha conteúdo que mude o preço; o Copom pausa.
- **Upside:** o prêmio se aprofunda: as decisões fiscais de 2027 afrouxam a política e o mercado lê a reação monetária como insuficiente (cauda do fiscal: CDS a 200 p.b. e NTN-B de 10 anos a 9,00% no 2T27), com a volatilidade cambial perto dos níveis de 2015 (cauda do câmbio); o Copom encerra o ciclo e sobe.
- **Downside:** o projeto para o centro da meta fiscal ganha conteúdo e o mercado o compra, e os preços voltam ao intervalo de 05/10–23/10 (CDS a 110 e NTN-B a 6,90% no 1T27); o Copom retoma os cortes.

**Caminhos das exógenas** (G `pm_r2_cenarios`). O base de cada exógena é o do principal, como entrou no P1; nas caudas, os caminhos de cauda que o principal escreveu no report da rodada 1:

| Exógena | Hoje (valor · tabela · data) | Cenário | 4T26 | 1T27 | 2T27 | 3T27 | 4T27 | 1T28 |
|---|---|---|---|---|---|---|---|---|
| Meta de inflação, 12 meses (`meta_12m`) · principal: este agente | 3,00 · `inflc_meta` · 2026 | base · upside · downside | 3,00 | 3,00 | 3,00 | 3,00 | 3,00 | 3,00 |
| Juro real de 10 anos (`rr_10a`) · principal: fiscal | 8,05 · `br_interest_rate` · 26/10 | base (P1) | 7,70 | 7,80 | 7,70 | 7,60 | 7,55 | 7,50 |
| | | upside (fiscal) | 8,05 | 8,80 | 9,00 | 9,00 | 8,90 | 8,80 |
| | | downside (fiscal) | 7,35 | 6,90 | 6,80 | 6,75 | 6,70 | 6,70 |
| CDS 5 anos (`fiscal`) · principal: fiscal | 137 · `cmb_risco_pais` · 26/10 | base (P1) | 140 | 140 | 138 | 135 | 135 | 135 |
| | | upside (fiscal) | 165 | 190 | 200 | 200 | 195 | 190 |
| | | downside (fiscal) | 115 | 110 | 108 | 106 | 105 | 105 |
| Volatilidade implícita (`vol`) · principal: câmbio | sem dado no F (12,19 no 2T26, no modelo) | base (P1) | 17,0 | 15,5 | 14,5 | 14,0 | 13,5 | 13,5 |
| | | upside (câmbio) | 24,0 | 21,0 | 18,0 | 16,0 | 15,0 | 15,0 |
| | | downside (câmbio) | 13,0 | 12,5 | 12,0 | 12,0 | 12,0 | 12,0 |
| Fed Funds (`ffr`) · principal: externo | 3,88 · `us_interest_rate` · 27/10 | os três (P1) | 4,13 | 4,13 | 4,13 | 4,13 | 4,13 | 3,88 |
| Inflação dos EUA no trimestre (`infl_us`) · principal: externo | — | os três (P1) | 0,86 | 0,61 | 0,61 | 0,65 | 0,63 | 0,65 |
| Dólar contra emergentes (`dxy_em`) · principal: externo | 130,21 · `cmb_dollar_index_em` · 23/10 | os três (P1) | 130,5 | 131,0 | 130,5 | 130,0 | 129,5 | 129,0 |
| S&P 500 (`sp500`) · principal: externo | — | os três (P1) | 7.750 | 7.900 | 8.050 | 8.200 | 8.350 | 8.500 |
| IC-Br em dólar (`icbr_usd`) · principal: externo | 205,70 · `comm_icbr_usd` · set | os três (P1) | 204,8 | 203,7 | 202,9 | 202,3 | 201,8 | 201,4 |
| IC-Br agropecuária em dólar (`icbr_agr_usd`) · principal: externo | 201,80 · `comm_icbr_usd` · set | os três (P1) | 202,0 | 202,0 | 202,0 | 202,0 | 202,0 | 202,0 |
| IC-Br metal em dólar (`icbr_met_usd`) · principal: externo | 335,06 · `comm_icbr_usd` · set | os três (P1) | 331,7 | 330,0 | 330,0 | 328,7 | 327,3 | 325,7 |

- `meta_12m`: a meta contínua de 3,00% do CMN, sem decisão de mudança no dado (`inflc_meta`, 2026) nem notícia na janela (item 6 da pauta do agente web); igual nos três cenários.
- As caudas do externo não entram: os cenários desta tese são domésticos, e o bloco externo fica no base do principal nos três.

**Saída do modelo** (centrais; a faixa de 90% do posterior dos pesos está no G e não é intervalo de previsão[^9]):

| Variável | Cenário | 4T26 | 1T27 | 2T27 | 3T27 | 4T27 | 1T28 |
|---|---|---|---|---|---|---|---|
| Selic, fechamento (% a.a.) | base (= P1) | 13,34 | 13,03 | 12,67 | 12,36 | 12,12 | 11,91 |
| | upside | 14,02 | 14,19 | 14,04 | 13,78 | 13,50 | 13,29 |
| | upside, R.t3 × 1,3 | 14,18 | 14,46 | 14,40 | 14,19 | 13,93 | 13,71 |
| | downside | 12,71 | 12,12 | 11,77 | 11,49 | 11,25 | 11,07 |
| Selic, média do trimestre (% a.a.) | base | 13,46 | 13,22 | 12,84 | 12,50 | 12,23 | 12,00 |
| IPCA 12 meses (%) | base | 5,32 | 4,96 | 4,48 | 4,52 | 4,38 | 4,19 |
| | upside | 5,34 | 5,03 | 4,62 | 4,69 | 4,56 | 4,33 |
| | downside | 5,30 | 4,89 | 4,39 | 4,42 | 4,29 | 4,13 |
| Focus IPCA 12m, média do trimestre (%) | base | 4,17 | 4,00 | 3,82 | 3,72 | 3,64 | 3,57 |
| | upside | 4,17 | 4,01 | 3,85 | 3,77 | 3,70 | 3,62 |
| | downside | 4,17 | 3,98 | 3,80 | 3,69 | 3,61 | 3,54 |
| Hiato (% do potencial) | base, upside e downside | 0,13 | −0,08 | −0,24 | −0,36 | −0,45 | −0,52 |
| PTAX, fechamento (R$/US$) | base | 5,435 | 5,503 | 5,508 | 5,495 | 5,526 | 5,565 |
| | upside | 5,622 | 5,791 | 5,823 | 5,796 | 5,796 | 5,816 |
| | downside | 5,256 | 5,337 | 5,349 | 5,350 | 5,386 | 5,422 |

O hiato é praticamente o mesmo nos três cenários (a diferença máxima é 0,01 p.p.) porque a Selic acompanha a âncora um por um e a IS mede o aperto contra a mesma âncora; só com R.t3 × 1,3 ele cai mais, a −0,61% no 1T28. Do 2T27 em diante a Selic do upside sem tempero (14,04 a 13,29) fica dentro da faixa base: o que leva à cauda de cima, a partir dali, é o tempero, não o modelo. O IPCA de 12 meses do modelo fica em 4,19% no 1T28 no base, contra 3,2% do Copom (`pm_copom_projecoes`, RPM 281ª); a leitura do caminho é do agente de inflação (S8).

### 3.2 Etapa 2 — o tempero qualitativo

**(i) Regra de juros (R), reação ao desvio da expectativa contra a meta — efeito mais forte que o estimado** · cenário upside
- Coeficiente `R.t3`: estimado 1,962, intervalo de 90% do posterior 1,148 a 2,726. Multiplicador × 1,3 (2,550), dentro do intervalo, no percentil 87.
- Efeito: Selic de fechamento do upside de 14,02 → 14,18 no 4T26 e de 14,04 → 14,40 no 2T27 (G `pm_r2_cenarios`; na rodada 1, 13,97 → 14,13 e 13,61 → 13,96, com os meus caminhos de cauda).
- Por quê: o Copom disse, por unanimidade, que expectativas desancoradas exigem "uma restrição monetária maior e por mais tempo do que outrora seria apropriado" (ata da 281ª, §10), e a desancoragem prolongada torna as expectativas mais sensíveis a choques (RPM set/26, 2.3, risco i). No upside a desancoragem é o que acontece; reagir mais a ela é a função de reação que o próprio Copom descreveu. Fica dentro do intervalo, então não afirmo que o histórico subestima o canal, só que este Copom está na ponta de cima dele. O agente de expectativas argumenta, para a (E), que a inércia é maior que a estimada (expectativas_r1); se ele aplicar o multiplicador dele, os dois efeitos se somam na minha regra.
- Onde entra: limite da cauda de upside.

**(ii-a) A reação do Copom ao câmbio e ao prêmio, que a regra (R) não tem** · cenários base e upside
- Hoje: PTAX 5,5007 (`cmb_ptax` · 26/10), 6,8% acima do condicionante de R$ 5,15 da 281ª; CDS 137 p.b. (`cmb_risco_pais` · 26/10).
- Por que o modelo não vê: (R) só lê a Selic defasada, a âncora e o desvio da Focus; o Copom reage à projeção no horizonte relevante, cujo câmbio de partida é o de mercado nos dez dias úteis anteriores (ata da 281ª, nota 2), e põe o câmbio depreciado entre os riscos de alta (§13). Desde a rodada 1 a PTAX do modelo chegou perto do mercado (5,435 no P1, contra 5,24 na rodada 1), então o canal câmbio → inflação → expectativa já passa pelo modelo; o que fica fora é a resposta discreta do Copom ao balanço de riscos.
- Efeito: +25 a +50 p.b. sobre o caminho do modelo até 09/12 enquanto a PTAX ficar acima de ~5,40; é o que faz o regime de alta (32%).
- Onde entra: assimetria do cenário base (+0,26 no 4T26) e limite da cauda de upside (14,25 em dezembro, 14,75 em março).

**(ii-b) Gradualismo e "serenidade e cautela"** · todos os cenários
- Hoje: cinco cortes seguidos de 25 p.b. desde 18/03 (`pm_copom_reuniao`); em 248 decisões desde 1999, nenhuma alta veio logo depois de um corte e os 14 ciclos de corte terminaram numa manutenção (mesma tabela).
- Por que o modelo não vê: (R) é contínua sobre médias trimestrais; no downside ela leva a Selic de 13,75% a 12,71% até dezembro, o que pediria cortes de 50 p.b. nas duas reuniões, quando o ciclo de 2026 andou só de 25 em 25. O mesmo vale, em menor grau, para a central: 13,34 em dezembro pede quase dois cortes.
- Efeito: comprime as caudas do 4T26 e do 1T27: o downside do modelo, 12,71, vira 13,50 em dezembro (percentil 10); uma alta em 04/11 fica em 12%.
- Onde entra: limites das caudas do 4T26 e 1T27; probabilidades da reunião de 04/11.

**(ii-c) Pressão política por juro mais baixo** · cenário downside (novo nesta rodada)
- Hoje: Lula, reeleito em 25/10 (nível A), disse em 24/10 "Quero que o Banco Central baixe o juro" (Poder360 · nível B). Contra: Galípolo disse que o seu mandato vai até o fim de 2028 (CNN Brasil · 27/10 · nível B), e não há, na janela, proposta de mudar a meta ou a autonomia do BC (agente web, item 6).
- Por que o modelo não vê: a postura do BC diante do governo não passa por nenhuma exógena; a (R) não tem um termo de independência.
- Efeito: 5 p.p. de probabilidade de cortes de 25 p.b. a partir de dezembro mesmo com a PTAX acima de 5,40; no fechamento, os mesmos passos do regime de cortes. Dura enquanto a resposta do Copom ao choque não for conhecida (04/11 e 09/12).
- Onde entra: probabilidade do downside, que deixa de ser só boa notícia.

### 3.3 Da etapa 1 à tese

| Trimestre | Central (P1) | Upside: modelo → com tempero | Downside: modelo → com tempero |
|---|---|---|---|
| 4T26 | 13,34 | 14,02 → 14,18 (R.t3) → 14,25 | 12,71 → 13,50 |
| 1T27 | 13,03 | 14,19 → 14,46 → 14,75 | 12,12 → 13,00 |
| 2T27 | 12,67 | 14,04 → 14,40 → 14,75 | 11,77 → 12,75 |
| 3T27 | 12,36 | 13,78 → 14,19 → 14,75 | 11,49 → 12,25 |
| 4T27 | 12,12 | 13,50 → 13,93 → 14,50 | 11,25 → 12,00 |
| 1T28 | 11,91 | 13,29 → 13,71 → 14,25 | 11,07 → 11,75 |

Os pontos "com tempero" são os percentis 10 e 90 da distribuição da Selic de fechamento que sai da mistura dos três regimes, com passos de reunião a reunião (G `pm_r2_distribuicao`). Os regimes, com a média da Selic de fechamento em cada um:

| Regime | Peso | 4T26 | 1T27 | 2T27 | 3T27 | 4T27 | 1T28 |
|---|---|---|---|---|---|---|---|
| Cortes de 25 p.b. retomados (reversão do prêmio 13 p.p.; Copom leniente 5 p.p.) | 18% | 13,45 | 13,05 | 12,65 | 12,25 | 11,85 | 11,60 |
| Pausa: 13,75% até o 1T27, cortes de 25 p.b. a partir do 2T27, mais firmes no 2S27 | 50% | 13,76 | 13,74 | 13,56 | 13,26 | 12,96 | 12,69 |
| Alta: ciclo de 50 a 100 p.b. até o 2T27, cortes no fim de 2027 | 32% | 14,11 | 14,51 | 14,61 | 14,54 | 14,36 | 14,14 |

A faixa base de cada trimestre contém a central do P1 e o grosso da pausa; as probabilidades da seção 1 são a massa da mistura dentro da faixa, acima e abaixo dela. A mediana da mistura é 13,75 até o 2T27, acima da central em todos os trimestres: é a forma numérica de dizer que a central não leva tempero e que a força que eu acredito estar ausente do modelo foi para a assimetria. A cauda de baixa do 1T27 caiu de 13% para 4% porque a faixa passou a incluir 13,00 (três cortes em quatro reuniões, que antes era cauda) e o regime de cortes perdeu peso.

## 4. Para os outros agentes

### Respostas às entradas fixas

- **E1 (câmbio), em destaque:** a tese da seção 1, com as reuniões de 04/11 a 17/03. O motivo do destaque: num pregão a curva passou a precificar alta em vez de corte a partir de dezembro, e a causa agora é conhecida (a eleição). Para o carry à frente: no regime mais provável (50%) a Selic fica em 13,75% até o 1T27; no de alta (32%), sobe até ~14,6% de média no 2T27. A central do modelo, que corta, está abaixo das duas.
- **E2 (câmbio):** hoje, uma pausa é lida como credibilidade e um corte como validação da desancoragem. Uma alta só é lida como credibilidade se vier com sinal de segunda ordem nas expectativas (Q2); sem ele, num choque de prêmio político e fiscal, com o carry já descolado do real em 26/10 (seu E5) e dois dos três sinais de dominância presentes (fiscal_r1), ela pode ser lida como custo da dívida, e o sinal do elo juro → câmbio deixa de ser garantido (mapa, 2.6).
- **E3 (câmbio), em destaque:** o Copom condicionou a projeção a R$ 5,15 seguindo a PPC, valor que é a média de dez dias úteis antes da semana da reunião (comunicado da 281ª, Tabela 1; ata, nota 2), listou "uma taxa de câmbio persistentemente mais depreciada" como risco de alta (ata, §13) e explicou a depreciação recente pelo diferencial de juros em queda (RPM set/26, 2.2). O motivo do destaque: a PTAX de 26/10, 5,50, está 6,8% acima do condicionante; o movimento é notícia para o Copom. Para 04/11 a janela do câmbio de partida acaba em 30/10 e já contém os pregões depois da eleição.
- **E4 (câmbio):** o gatilho não disparou: não há intervenção à vista ou em linha em outubro até 26/10 (`cmb_reservas_bc`), e em 27/10 houve só a rolagem programada de até US$ 4 bi em swap (InfoMoney · 27/10 · nível B). Pela taxa: o Copom responde ao câmbio pela segunda ordem e pela projeção (ata da 281ª, §16); minha leitura é manter em 04/11 (77%), com 32% de a Selic estar acima de 13,75% depois de 09/12.
- **E5 (inflação):** a tese da seção 1.
- **E6 (inflação):** projeção do cenário de referência, IPCA 12 meses: 4,4 (3T26), 5,2 (4T26), 4,9 (1T27), 4,5 (2T27), 4,5 (3T27), 3,9 (4T27), 3,2 (1T28); administrados 3,9 / 5,3 / 4,5 / 4,0 / 4,3 / 3,5 / 3,2 (`pm_copom_projecoes`, RPM 281ª). Condicionantes: Selic da Focus, câmbio de R$ 5,15 pela PPC, Brent na curva futura por seis meses — partindo de US$ 90 no 3T26, pico no 4T26 e cerca de US$ 84 no 2T27 — e 2% ao ano depois, bandeira amarela em dezembro de 2026 e de 2027 (comunicado; a ata cita só 2026), fim das subvenções e desonerações de combustíveis no prazo legal (RPM set/26, 2.2 e nota 45). Mensal de curto prazo: set 0,65, out 0,29, nov 0,41, dez 0,68 (RPM, Tabela 2.1.2). Condicionamento, não previsão do Copom. Novo nesta rodada: o ministro da Fazenda indicou manter a ajuda aos combustíveis em 2027 (Poder360 · 23/10 · nível B), contra a premissa do Copom.
- **E7 (atividade):** a tese da seção 1 e as caudas; a média do trimestre é a do P1 (base: 13,46 no 4T26, 13,22 no 1T27, 12,00 no 1T28) e o fechamento é a tese. As médias da minha distribuição ficam acima: 13,82 no fechamento do 4T26 e 13,86 no do 1T27.
- **E8 (atividade):** a tabela de neutros de Q2. Contra o neutro do Copom (5,00%) a Selic real ex-ante está 3,82 p.p. acima; contra a âncora do modelo, 2,70 p.p. no pregão de 26/10 e 3,05 p.p. na média do 4T26 do P1. O aperto efetivo que a IS mede caiu sem o Copom mexer, e volta em parte se o prêmio devolver como o fiscal escreve.
- **E9 (atividade):** "moderação gradual da atividade econômica, principalmente em setores mais cíclicos, embora ainda em patamar resiliente, e mercado de trabalho aquecido" (comunicado da 281ª, §2); hiato de 0,5% no 2T26 e 0,4% no 3T26, projetado em −0,4% no 1T28 (RPM set/26, 2.2); na edição de set/26 os trimestres de 2T25 a 2T26 foram revistos para cima de 0,10 a 0,15 p.p. (`pm_hiato_produto_vintages`); salários reais acima da produtividade (ata, §7). Sobre o 3T26 (seu S-PM3): o RPM diz que julho e agosto, "considerados em conjunto, apontam para nova moderação da atividade no terceiro trimestre", com carregamento estatístico de −0,7% no IBC-Br deixado por julho (RPM set/26, capítulo 1), revisou o PIB de 2026 de 2,0% para 1,8% por causa desses "primeiros indicadores do terceiro trimestre" (RPM set/26) e, para o hiato do 3T26, usou "projeções das variáveis de atividade quando os dados não estavam disponíveis" (RPM set/26, nota 50). Não achei no texto o número de PIB do 3T26 por trás dos 0,41.
- **E10 (fiscal):** a tese da seção 1.
- **E11 (fiscal):** a política fiscal age no curto prazo pela demanda e estruturalmente pelo prêmio a termo; "o esmorecimento no esforço de reformas estruturais e disciplina fiscal, o aumento de crédito direcionado e as incertezas sobre a estabilização da dívida pública têm o potencial de elevar a taxa de juros neutra" (ata da 281ª, §8). O comunicado diz que o Comitê "segue acompanhando como os desenvolvimentos da política fiscal doméstica impactam a política monetária e os ativos financeiros" (§5). O Copom lê fiscal como demanda, como prêmio e como neutro — os três. O choque de 26/10 é do segundo tipo, e o Copom ainda não falou dele.
- **E12 (fiscal):** a divisão está em "Como subordinado", abaixo: dos +135 p.b., +22 nos dois primeiros anos (caminho de política), +40 nos anos 2 a 5, +73 nos anos 5 a 10.
- **E13 (fiscal):** a mesma leitura de E2.
- **E14 (externo):** a tese da seção 1. O juro real brasileiro ex-post era o maior entre os pares, 9,78% em agosto (`cmb_real_rates`); na central do modelo o diferencial contra o Fed cai de cerca de 9,2 p.p. no 4T26 para cerca de 8,0 p.p. no 1T28, e na pausa fica perto de 9,6 até o 1T27[^13].
- **E15 (externo):** ambiente externo "incerto em função da indefinição acerca dos conflitos armados no Oriente Médio e da incerteza sobre a política monetária em algumas economias avançadas" (comunicado da 281ª, §1); riscos de baixa vindos de fora: desaceleração global pelos choques de comércio e do petróleo, e queda das commodities (§4). Condicionante: Brent pela curva futura, partindo de US$ 90 (RPM set/26, 2.2). O cenário de referência é de 24/09 e não tem o Brent acima de US$ 110 nem a alta do Fed como dado: os dois são notícia para o Copom de novembro.
- **E16 e E21:** não se aplicam: o principal de `rr_10a` é o fiscal. Meus insumos estão em "Como subordinado".
- **E17 (expectativas):** o Copom responde à desancoragem com "restrição monetária maior e por mais tempo" (ata da 281ª, §10); na regra do modelo, o coeficiente sobre o desvio da Focus contra a meta é 1,96 (`R.t3`, mediana). A minha resposta ao choque é Q1: pausa agora, alta se a Focus de 2027–28 subir; um Copom que corta apesar do choque é o tempero (ii-c), com 5%.
- **E18 (expectativas):** o Copom julga a ancoragem em horizontes de dois ou três anos à frente (RPM set/26, 2.3); chama as expectativas de desancoradas e diz que elas "permanecem acima da meta de inflação em todos os horizontes" (ata da 281ª, §10); registrou a Focus de 2028 subindo de 3,69% para 3,80% como desancoragem adicional (RPM set/26, 2.2); projeta 3,2% no 1T28 contra a Focus de 2028 de 3,75% (`expc_focus_periodo` · 23/10).
- **E19 (expectativas):** `meta_12m` em 3,00% nos seis trimestres (seção 3.1); nenhuma decisão do CMN de mudar a meta no dado (`inflc_meta`), e o agente web não achou proposta nem discussão na janela.
- **E20 (expectativas):** a tabela de Q3: curva menos Focus de +23 p.b. em 04/11 a +403 p.b. em dezembro de 2027, a maior parte prêmio, numa curva formada em mercado disfuncional; e a curva contra a minha média, de −3 p.b. em 04/11 a +98 p.b. em março.

### Pedidos

- **S1 (câmbio):** com a causa conhecida (reeleição, nível A) e a correção parcial de 27/10 (nível B), o salto de 26/10 continua "na maior parte persistente"? Tese dependente: o peso do regime de alta (32%) e as probabilidades de 09/12.
- **S2 (câmbio):** a correção de 27/10 mudou a sua divisão entre prêmio e posição (a desmontagem da posição comprada de 20/10)? Tese dependente: se o salto é prêmio, ele chega às expectativas (Q2).
- **S3 (câmbio):** qual é o câmbio de partida provável nas projeções de 04/11 (dez dias úteis encerrados em 30/10) e de 09/12 (encerrados em 04/12), contra o condicionante de R$ 5,15? Tese dependente: a alta em dezembro.
- **S4 (câmbio):** o real está precificando estresse político e fiscal que o CDS não carrega (o fiscal diz que o CDS subiu pouco num choque grande)? Tese dependente: o neutro mais alto que o modelo põe na âncora.
- **S5 (câmbio):** com a curva precificando alta e o carry descolado em 26/10, uma alta em 09/12 apreciaria o real? Tese dependente: E2 e o peso do regime de alta.
- **S6 (câmbio):** o cancelamento dos leilões do Tesouro e a fala de "mercado muito disfuncional" (níveis A e B) se estenderam ao câmbio (liquidez, cupom cambial)? Tese dependente: o gatilho de E4.
- **S7 (inflação):** repasse de uma PTAX de 5,44 a 5,50 no 4T26 (P1 e mercado) para alimentação, industriais e monitorados no 4T26–2T27, e quanto disso é primeira ordem. Tese dependente: segunda ordem, o critério do Copom (ata da 281ª, §16).
- **S8 (inflação):** o caminho do IPCA de 12 meses e dos serviços subjacentes até o 1T28 se a subvenção aos combustíveis continuar em 2027 (Poder360 · 23/10 · nível B) e a Petrobras reajustar "de maneira lenta e gradual" (CNN Brasil · 26/10 · nível B). Tese dependente: o modelo dá 4,19% no 1T28 contra 3,2% do Copom; qual dos dois, e quanto o subsídio esconde?
- **S9 (expectativas):** com as pesquisas do 4T26 em 4,52% de média antes da eleição, quanto você espera que a Focus de 2027 e de 2028 suba depois de 25/10? Tese dependente: os sinalizadores de alta de Q2 (Focus 2027 acima de 4,6%, 2028 acima de 4,0%).
- **S10 (atividade):** a contração que o dado mensal aponta no 3T26 leva o BC a revisar o hiato de partida (0,41) para baixo no RPM de dezembro, e a partir de quanto isso muda a leitura do Copom? Tese dependente: o "cedo demais para subir" de Q2.
- **S11 (fiscal):** a resposta à divisão da seção abaixo: o seu caminho devolve 25 p.b. até o 1T27 e 0,3 p.p. em 2027; quanto disso é prêmio fiscal que depende do projeto de Durigan ter conteúdo, e quanto é o caminho de Selic que a curva hoje cobra e que eu não espero? Tese dependente: a central inteira (+1 p.p. em `rr_10a` move a central +1 p.p.).
- **S12 (fiscal):** se o projeto para o centro da meta fiscal for enviado com corte de despesa, quanto ele tira do impulso de 2027 e do prêmio? Tese dependente: o peso do regime de cortes (reversão, 13 p.p.).
- **S13 (externo):** a alta do Fed que você espera no 4T26 é na reunião de 27–28/10 ou na de dezembro? Tese dependente: o dólar contra emergentes na véspera de 09/12 e o peso do regime de alta.
- **Ao agente web:**
  1. O que o Copom ou seus diretores disseram entre 27/10 e o fim da janela sobre câmbio, a reunião de 04/11 ou o funcionamento do mercado, e se houve leilão à vista, de linha ou de swap extraordinário depois de 27/10. Tese dependente: as probabilidades de 04/11 e o gatilho de E4.
  2. O conteúdo do projeto de lei complementar que Durigan anunciou para buscar o centro da meta fiscal (corte de despesa, regra, prazo de envio) e a meta de primário de 2027 depois da eleição. Tese dependente: o peso do regime de cortes por reversão do prêmio.
  3. Fechamento do dólar, do DI de 2 anos e da NTN-B de 10 anos em 27 e 28/10, com a fonte e a reação. Tese dependente: se o choque de 26/10 ficou (base) ou começou a se desfazer (downside).
  4. Decisões da Petrobras sobre gasolina e diesel depois de 26/10, e a proposta de manter a subvenção em 2027 (instrumento, valor). Tese dependente: E6 e S8, e o custo fiscal no prêmio.
  5. Qualquer fala do presidente reeleito ou da equipe econômica sobre a meta de inflação, o CMN ou a diretoria do BC depois de 25/10. Tese dependente: `meta_12m` e o tempero (ii-c).

### Como subordinado

- **`rr_10a` · principal: fiscal**
  - Insumos:
    - A divisão da alta de 23 para 26/10 pelos trechos da curva real: dos +135 p.b. da NTN-B de 10 anos, +4 p.b. vêm do primeiro ano, +18 do segundo, +40 dos anos 2 a 5 e +73 dos anos 5 a 10 (`br_interest_rate` · 23 e 26/10). Contra 30/09, a alta é de +50 p.b., com +33 nos anos 5 a 10. O caminho de política que o Copom controla está nos dois primeiros anos; o salto concentrado depois do 5º ano é prêmio.
    - O juro real a termo entre 1 e 2 anos foi a 9,62% (+184 p.b. em 26/10): é a curva cobrando o ciclo de alta até 15,78% em dezembro de 2027 (Q3). Eu dou 32% a um ciclo de alta e 50% a uma pausa com cortes a partir do 2T27. Se a alta não vier, esse trecho comprime: uma queda de 1 a 1,5 p.p. nele tira 10 a 15 p.b. da NTN-B de 10 anos, pelo peso de um ano em dez (aproximação da mesma conta).
    - O juro real de política que a Focus espera é 7,10% em 2027, 6,02% em 2028 e 6,28% em 2029 (Selic 11,75%, 10,00% e 10,00% contra IPCA 4,34%, 3,75% e 3,50% · `expc_focus_periodo` · 23/10). O seu caminho de 7,50% no 1T28 fica cerca de 1,5 p.p. acima do de 2028, a medida do prêmio de prazo e fiscal que sobra (com a ressalva de que a Focus é de antes da eleição).
    - No simulador, `rr_10a` move a Selic um por um, no mesmo trimestre, e não move o hiato: com o meu caminho de referência da rodada 1 a central seria 0,16 a 0,55 p.p. mais alta (G `pm_r2_cenarios`).
  - Argumento: o seu caminho de base é coerente com a minha tese. A devolução de ~25 p.b. até o 1T27 e de 0,3 p.p. em 2027 cabe, pela metade, no caminho de política que eu espero (a curva cobra uma alta que eu dou a 32%); a outra metade é prêmio, e depende de o projeto anunciado por Durigan ter conteúdo (níveis A e B, sem detalhe). Por isso retiro o meu caminho de referência. Se o projeto não sair até o 1T27, ou se o Copom subir em dezembro, o argumento volta para cima: o prêmio dos anos 5 a 10 fica e o caminho deveria ficar perto de 8,0% em 2027.
  - Caminho de referência: nenhum nesta rodada (na rodada 1, 7,76 no 4T26 e 8,05 do 1T27 ao 1T28).
  - Resposta do principal (moderação da rodada 2): o fiscal aceitou o argumento dos dois primeiros anos e passou a 7,72 · 7,95 · 7,90 · 7,80 · 7,75 · 7,70, com o 1T27 perto de 8,0 pelo prêmio dos anos 5 a 10. Aceito esse caminho, sem caminho de referência: ele separa as duas partes do salto como eu separo. No modelo, a Selic de fechamento da base fica em 13,43 · 13,21 · 12,87 · 12,56 · 12,32 · 12,11, que é a central da rodada final se o P2 o usar. Divergência fechada.

### Divergências

- **`meta_12m` · subordinado: fiscal.** O fiscal não trouxe argumento nem caminho de referência na rodada 1 ("nada a acrescentar neste ciclo", fiscal_r1), e o P1 não lista divergência nessa exógena. O agente web, a pedido dos dois, não achou na janela proposta ou discussão de mudar a meta de inflação; as matérias de 26–27/10 sobre "centro da meta" tratam da meta fiscal (notícias, "Sem notícia", item 6). Mantenho 3,00% nos seis trimestres. Mudaria o caminho com uma decisão ou proposta formal do CMN, ou uma fala nominal do governo pedindo meta mais alta (pedido 5 ao agente web).

## 5. Placar

Primeiro ciclo: não há report final anterior deste agente (o ciclo de 2026-10-22 não tem `politica_monetaria_rf.md`). Nenhum trimestre nem reunião a conferir.

## 6. Sobre o modelo

O Modelo Estrutural não muda neste ciclo (decisão do usuário); o que segue são propostas.

| Fonte | O que sugere (regressor, defasagem, quebra, âncora) | Teste proposto (dado, amostra, que resultado mudaria a especificação) | Por que importa para a tese deste ciclo |
|---|---|---|---|
| Mapa conceitual, 2.5 (a âncora carrega prêmio de prazo e fiscal, não é o neutro do Copom); RPM set/26, 2.2 (neutro de 5,00%); a divisão por trechos da curva real (`br_interest_rate`, 23 e 26/10: 73 dos 135 p.b. nos anos 5 a 10); o agente fiscal propõe o mesmo teste pelo outro lado (fiscal_r1, seção 6) | Na (R), a Selic segue `rr_10a` + meta um por um e no mesmo trimestre. Liberar o coeficiente da âncora, ou trocá-la por um trecho mais curto da curva real (a NTN-B de 5 anos ou o termo de 2 a 5 anos), que carrega menos prêmio longo | (R) com o coeficiente da âncora livre, 2006–2026, `br_interest_rate` e `pm_copom_reuniao`; e a mesma (R) com a âncora de 5 anos e com o termo de 2 a 5 anos. Coeficiente bem abaixo de 1 (digamos < 0,5) com a de 10 anos, ou ajuste melhor fora da amostra com uma âncora mais curta, muda a âncora | A central deste ciclo é, na prática, o caminho de `rr_10a`: a diferença entre o meu caminho e o do fiscal moveu a central em até 0,55 p.p. sem nenhum dado novo de inflação ou atividade |
| Comunicado da 281ª, §4 (câmbio depreciado como risco de alta); `pm_copom_reuniao` (2002: +300 p.b. em 14/10/2002, depois de duas manutenções) | (R) não tem câmbio nem prêmio de risco; acrescentar a variação trimestral da PTAX ou do CDS | (R) com a variação da PTAX (ou do CDS) no trimestre, 2003–2026, `cmb_ptax`, `cmb_risco_pais`, `pm_copom_reuniao`. Coeficiente positivo e estável, com ganho de ajuste fora da amostra, entra na regra | O choque é de câmbio e prêmio, e a regra só o vê pela Focus, com defasagem: é o tempero (ii-a), que hoje está fora do modelo |
| `pm_copom_reuniao` (cinco cortes iguais de 25 p.b. em 2026; nenhuma alta logo depois de um corte em 248 decisões) | A Selic de fechamento derivada da média (média deste trimestre e do seguinte) é contínua; a decisão é discreta e gradual. Um termo de passo máximo, ou a regra estimada sobre o fechamento | Comparar, 2006–2026, o erro da Selic de fechamento derivada com o de uma regra estimada direto no fechamento com o passo arredondado a 25 p.b.; mudar se o erro cair nos trimestres de virada de ciclo | A central do 4T26 (13,34) pede quase dois cortes até 09/12 com a curva precificando alta; o tempero (ii-b) corrige isso fora do modelo |

[^1]: A meta Selic muda só nas reuniões do Copom, cerca de duas por trimestre. O valor de fechamento do trimestre é a decisão da última reunião dentro dele: 09/12 para o 4T26, 17/03 para o 1T27, e assim por diante. O calendário oficial vai até 08/12/2027; para o 1T28 supus duas reuniões, como em todos os trimestres de 2022 a 2027.
[^2]: O Modelo Estrutural só tem a Selic média de cada trimestre. A de fechamento é derivada: a média deste trimestre e do seguinte, dividida por dois. Medida de 2006 a 2026, a regra erra 0,12 p.p. em média e 0,55 no pior trimestre.
[^3]: As probabilidades de cada reunião saem de três regimes (cortes retomados, pausa, alta), cada um com a chance de cada passo em cada reunião; a tabela é a média ponderada. O mesmo cálculo dá a distribuição do fechamento de cada trimestre, então a tabela de reuniões e a tese não podem se contradizer.
[^4]: Comentário de processo: esta rodada já tem as notícias que o agente web buscou a pedido de todos os agentes depois da rodada 1. Os números continuam vindo do F, fixo no ciclo, que vai até 26/10; o que aconteceu em 27/10 entra só pelas notícias.
[^5]: Juro neutro é a taxa real que não acelera nem freia a economia. Se a Selic real (descontada da inflação esperada) está acima dele, a política é restritiva. Exemplo: Selic real de 8,8% contra neutro de 5,0% é um aperto de cerca de 3,8 p.p. O neutro não é observado; cada fonte o estima de um jeito.
[^6]: Dominância fiscal, na versão de Blanchard (2004) para o Brasil de 2002: quando a dívida é alta e o investidor teme o calote, subir os juros pode aumentar o risco percebido e depreciar a moeda, em vez de apreciá-la. É um espectro, não uma chave; a avaliação fiscal é do agente fiscal.
[^7]: A Selic esperada para cada reunião sai da curva de DI: a taxa a termo entre a vigência de uma decisão e a da seguinte, somada a 0,10 p.p., a distância usual entre o CDI e a meta Selic. É preço, não previsão. O cálculo deste report e o do F diferem em até 0,15 p.p. em algumas reuniões; o salto de 23 para 26/10 usa o mesmo cálculo nas duas datas.
[^8]: Prêmio de prazo é a remuneração extra que o investidor pede para travar um juro longo em vez de rolar juros curtos. Por isso a taxa de um contrato de DI para dezembro de 2027 não é só a Selic que o mercado espera para lá: ela inclui um prêmio, que sobe quando a incerteza sobe e quando o mercado funciona mal.
[^9]: A faixa que o modelo imprime cobre só a incerteza dos pesos estimados das equações, não os erros delas. Não é um intervalo de previsão; a distribuição da tese é deste agente.
[^10]: Percentil 10 é o valor abaixo do qual ficam 10% dos desfechos possíveis; percentil 90, o valor abaixo do qual ficam 90%. Entre os dois estão 80% dos desfechos.
[^11]: Como a Selic só assume múltiplos de 0,25, o limite de cada faixa é posto entre dois degraus, de modo que a faixa contenha a central do modelo (que não é um degrau) e um conjunto exato de decisões. No 4T26, 13,30 a 13,80 contém 13,34 e as decisões 13,50 e 13,75.
[^12]: Juro real a termo é o juro real que a curva de hoje implica para um trecho do futuro: o "de 5 a 10 anos" é o juro real anual que o investidor trava hoje para os anos 5 a 10. A NTN-B de 10 anos é, aproximadamente, a média desses trechos ponderada pela duração de cada um, então a alta dela pode ser dividida entre eles. O caminho da Selic que o Copom controla pesa nos primeiros dois anos; o que sobe depois disso é prêmio.
[^13]: Diferencial aproximado: a Selic de fechamento da central (13,34 e 11,91) menos o Fed Funds efetivo do caminho do agente externo (4,13 no 4T26 e 3,88 no 1T28, P1); na pausa, 13,75 menos 4,13.
