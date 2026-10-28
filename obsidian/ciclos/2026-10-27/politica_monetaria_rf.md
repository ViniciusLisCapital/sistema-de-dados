# Report — política monetária · ciclo 2026-10-27 · report final

Dados até: pregão de 26/10/2026 (curvas, PTAX, CDS), Focus de 23/10, QPC da 281ª (23/09), documentos do Copom até o RPM de 24/09; notícias publicadas até 27/10 · Horizontes: 4T26 a 1T28, a meta Selic no fechamento de cada trimestre (a decisão da última reunião dentro dele)[^1]

## 1. Tese

| Variável | Trimestre | Central | Base: faixa · P | Upside: limite · P | Downside: limite · P | P(up) − P(down) |
|---|---|---|---|---|---|---|
| Meta Selic, fechamento do trimestre (% a.a.) | 4T26 | 13,43 | 13,30 a 13,80 (13,50 ou 13,75) · 62% | acima de 13,80 (alta até 09/12) · 32% | abaixo de 13,30 (dois cortes) · 6% | +0,26 |
| | 1T27 | 13,21 | 13,00 a 14,05 · 67% | acima de 14,05 · 29% | abaixo de 13,00 · 4% | +0,25 |
| | 2T27 | 12,87 | 12,65 a 14,05 · 62% | acima de 14,05 · 30% | abaixo de 12,65 · 8% | +0,22 |
| | 3T27 | 12,56 | 12,35 a 14,05 · 61% | acima de 14,05 · 27% | abaixo de 12,35 · 12% | +0,15 |
| | 4T27 | 12,30 | 12,10 a 14,05 · 64% | acima de 14,05 · 22% | abaixo de 12,10 · 14% | +0,08 |
| | 1T28 | 12,10 | 11,90 a 14,05 · 70% | acima de 14,05 · 16% | abaixo de 11,90 · 14% | +0,02 |

A central é a Selic de fechamento do P2, a rodada conjunta do Modelo Estrutural com o caminho de cada exógena dado pelo seu principal, sem ajuste[^2]. A Selic anda em degraus de 25 p.b., então cada faixa é um conjunto de decisões possíveis: no 4T26, 13,30 a 13,80 quer dizer "13,50 ou 13,75"[^11].

**As duas próximas reuniões de cada trimestre, decisão a decisão** (Selic de partida 13,75%, decidida em 16/09; probabilidades deste agente, que somam 100% em cada linha e fecham nas linhas de 4T26 e 1T27 acima[^3]):

| Reunião | −50 p.b. | −25 p.b. | manter | +25 p.b. | +50 p.b. | Mais provável | Curva DI 26/10 | Focus 23/10 |
|---|---|---|---|---|---|---|---|---|
| 04/11/2026 | — | 11% | 77% | 9% | 3% | manter, 13,75 | 13,73 | 13,50 |
| 09/12/2026 | 1% | 15% | 57% | 16% | 11% | manter, 13,75 | 14,02 | 13,25 |
| 27/01/2027 | 1% | 19% | 56% | 15% | 9% | manter, 13,75 | 14,45 | 13,00 |
| 17/03/2027 | 1% | 19% | 60% | 15% | 5% | manter, 13,75 | 14,84 | 12,75 |

Curva DI e Focus: `br_di_grade` (26/10) e `expc_focus_copom` (23/10), a Selic de cada reunião na tabela "A Selic por reunião" do F.

- **Upside, acima da faixa: o Copom encerra a calibração e sobe a Selic.** No modelo, com os caminhos de cauda dos principais — CDS a ~205 p.b. e NTN-B de 10 anos a ~8,9% no 1T27 (fiscal), volatilidade implícita a 24% no 4T26 (câmbio) —, a Selic fecha o 4T26 em 14,12 e o 1T27 em 14,29; com a regra reagindo à expectativa 30% mais forte que o estimado (tempero i), em 14,28 e 14,57; com a reação do Copom ao câmbio e ao prêmio, que a regra (R) não tem (tempero ii-a), a 14,25 em dezembro e 14,75 no 1T27 (percentil 90[^10] da distribuição). É ruim para o Brasil: quer dizer câmbio, expectativas e prêmio piores que no base.
- **Downside, abaixo da faixa: os cortes voltam.** No modelo, um arcabouço fiscal que o mercado compre (CDS a 115 p.b. e NTN-B de 10 anos a 7,3% no 1T27, cauda do fiscal; volatilidade a 12,5%, cauda do câmbio) leva a Selic a 12,92 no 4T26 e 12,50 no 1T27; o gradualismo do Copom (tempero ii-b) limita a 13,50 em dezembro e 13,00 em março (percentil 10). Só é boa notícia se vier da queda do prêmio. Parte dela (5 dos 18 p.p. do regime de cortes) é outro caminho, ruim: um Copom que volta a cortar com a PTAX acima de 5,40, sob a pressão de quem foi reeleito pedindo juro mais baixo (tempero ii-c).

**A tese em uma frase:** o Copom mantém 13,75% em 04/11 (77%) e em 09/12 (57%), porque cortar depois de a reeleição de 25/10 levar a PTAX a +9% e a inflação implícita de 1 ano a +1,2 p.p. num pregão validaria a desancoragem; o modelo, com o juro real de 10 anos perto de 8% que o fiscal escreve, desenha cortes graduais até ~12,1% no 1T28, mas o risco é de alta — 32% de a Selic estar acima de 13,75% depois de dezembro — enquanto as expectativas não absorverem o choque e o ajuste fiscal prometido não tiver conteúdo.

**O que mudou desde a rodada 2**

| O quê | Rodada 2 | Report final | Por quê |
|---|---|---|---|
| Central, 4T26 a 1T28 | 13,34 · 13,03 · 12,67 · 12,36 · 12,12 · 11,91 | 13,43 · 13,21 · 12,87 · 12,56 · 12,30 · 12,10 | a central passa a ser a do P2: o fiscal subiu o `rr_10a` para 7,72 · 7,95 · 7,90 · 7,80 · 7,75 · 7,70 depois da moderação, e o modelo leva a diferença à Selic um por um (+0,09 a +0,20 p.p.) |
| Faixas, probabilidades, passos por reunião, pesos dos regimes | — | sem mudança | as faixas ainda contêm a central; a evidência nova sobre expectativas e a correção de 27/10 puxam em sentidos opostos e a conta de controle (seção 2, Q4) fecha com o peso do regime de alta |
| Caminhos de cauda das exógenas | os do fiscal r1 | os do fiscal r2 | o principal revisou as caudas |
| Saídas do modelo nas caudas | upside 14,02, downside 12,71 no 4T26 | upside 14,12, downside 12,92 no 4T26 | caminhos de cauda novos |

## 2. Argumentação

### O fato do ciclo: a reeleição de 25/10, o pregão de 26/10 e o de 27/10

Luiz Inácio Lula da Silva foi reeleito no 2º turno de 25/10 (CNN Brasil · 25/10 · nível A), depois de um 1º turno, em 04/10, em que Flávio Bolsonaro ficou à frente e o dólar caiu a R$ 5 (Agência Brasil · 05/10 · nível A). Os dois pregões de outubro em que tudo se moveu são as duas leituras do mercado sobre a eleição: "o mercado vinha tratando a vitória de Flávio como a possibilidade de uma virada na política fiscal" (CNN Brasil · 25/10 · nível A). De 23/10 para 26/10 a PTAX subiu 9,2% (5,04 → 5,50 · `cmb_ptax`), o CDS de 5 anos 18 p.b. (119 → 137 · `cmb_risco_pais`), o DI de 2 anos 252 p.b. e a NTN-B de 10 anos 135 p.b. (`br_interest_rate` · 23 e 26/10). O Tesouro cancelou os leilões da semana e recomprou mais de R$ 14 bi em títulos em 26/10 e voltou a recomprar NTN-B em 27/10 (InfoMoney e Agência Brasil · 26 e 27/10 · nível A); um analista nomeado chamou o mercado de "muito disfuncional" (InfoMoney/Reuters · 26/10 · nível B).

Para a política monetária o salto tem três partes, e cada dado responde a uma:
- **O câmbio passou do condicionante do Copom:** a PTAX de 5,50 está 6,8% acima dos R$ 5,15 do cenário de referência da 281ª (comunicado, Tabela 1), e uma "taxa de câmbio persistentemente mais depreciada" é o risco de alta (iii) da lista do Copom (ata da 281ª, §13). O agente de câmbio lê que "a reeleição levou o real a um patamar que não reverte sozinho" (cambio_r2).
- **A compensação por inflação subiu em todos os prazos:** a inflação implícita subiu 1,19 p.p. em 1 ano, 1,23 em 2, 1,20 em 5 e 0,89 em 10 anos, de 23 para 26/10 (`br_interest_rate`); em 1 ano ela está em 7,87%, contra a Focus de 12 meses em 4,53% (`expc_focus` · 23/10). O agente de expectativas lê os 7,87% como prêmio mais a direção que a pesquisa costuma seguir, não como expectativa (expectativas_r2).
- **A maior parte da alta do juro real longo é prêmio, não caminho de política.** Dos +135 p.b. da NTN-B de 10 anos, os dois primeiros anos da curva real, onde mora o caminho que o Copom controla, respondem por +22 p.b.; os anos 2 a 5, por +40; os anos 5 a 10, por +73 (`br_interest_rate` · 23 e 26/10, juros reais a termo[^12]).

O pregão de 27/10 não está no F[^4] e confirma essa divisão. O dólar comercial fechou em queda de 0,97%, a R$ 5,350 (Poder360 · 27/10 · nível B); o Tesouro Prefixado 2029 caiu 47 p.b., de 15,26% para 14,79%, e o DI para janeiro de 2028 estava em 14,41% no fim do dia (InfoMoney e InfoMoney/Reuters · 27/10 · nível B), abaixo do DI de 1 ano de 26/10, 14,70% (`br_di_grade`), com vencimento mais longo. Mas o Tesouro IPCA+ 2040 subiu de 7,29% para 7,53% no mesmo dia (InfoMoney · 27/10 · nível B). A parte nominal de prazo médio, onde está o ciclo de alta que a curva cobra, devolveu; o juro real longo, onde está o prêmio, subiu mais. O governo respondeu ao preço: Durigan disse que o governo "pretende ampliar o superavit primário em 2027" (Poder360 · 26/10 · nível B), que apresentará um projeto de lei complementar para perseguir o centro da meta fiscal (Poder360, CNN Brasil e Exame · 27/10 · nível A de que disse; conteúdo e prazo não detalhados) e que a proposta "deverá ser apresentada ainda em 2026" (Poder360 · 26/10 · nível B). O comando da Fazenda no novo mandato não foi anunciado (InfoMoney · 27/10 · nível B).

### Q1 — O que o Copom vai fazer?

**Em 04/11: manter 13,75% e encerrar a calibração (77%).** Três coisas do Copom sustentam a pausa, e uma regularidade sustenta que ela venha antes de uma alta:
- A função de reação declarada olha a projeção no horizonte relevante (1T28) e reage aos efeitos de segunda ordem dos choques (ata da 281ª, §16). O salto mexe nos condicionantes que a governança atualiza sozinha: a trajetória de Selic da Focus, o petróleo pela curva futura (ata, §11) e o câmbio de partida, a média de dez dias úteis encerrados na semana anterior à da reunião (ata, nota 2). Para 04/11 essa média fica entre R$ 5,21 e R$ 5,27, conforme os pregões de 27 a 30/10 fiquem perto de 5,35 ou de 5,50 (`cmb_ptax` de 19 a 26/10), 1% a 2% acima do condicionante de setembro: a projeção de novembro vê só uma parte do salto.
- A guidance é condicional: "a magnitude total do ciclo de calibração será estabelecida à luz de novas informações" (comunicado da 281ª, §6), com "serenidade e cautela" (§8) e a conclusão unânime de que, com expectativas desancoradas, "exige-se uma restrição monetária maior e por mais tempo do que outrora seria apropriado" (ata da 281ª, §10). Cortar oito dias depois do salto iria contra as três frases.
- O mercado já tirou o corte do preço: a curva de 26/10 dá 13,73% para 04/11 (`br_di_grade`), e a Reuters relatou que o mercado "passou a precificar a possibilidade de o Copom […] não cortar a Selic" (InfoMoney/Reuters · 26/10 · nível B). Antes do choque, 53% dos respondentes do QPC da 281ª já esperavam manutenção em novembro (`expc_qpc` · 23/09).
- Em 248 decisões desde 1999 o Copom nunca passou de um corte direto para uma alta: os 14 ciclos de corte terminaram numa manutenção, e as oito reversões para alta tiveram de uma a cinco manutenções no meio (`pm_copom_reuniao`, 1999–2026). Por isso uma alta já em 04/11 fica em 12%, e não em zero: em 2002 a primeira alta, de 300 p.b., veio depois de só duas manutenções (mesma tabela, 14/10/2002).

O BC não deu sinal na véspera: na coletiva do Relatório de Estabilidade Financeira de 27/10, Galípolo não respondeu sobre a eleição, sobre parâmetros de intervenção cambial nem sobre a próxima decisão do Copom (Poder360 · 27/10 · nível B), e sobre a escala 6x1 disse que "a gente vai esperar a implementação para saber se precisa agir" (InfoMoney · 27/10 · nível B). É a postura de reagir ao efeito, não de antecipá-lo, mas a segunda fala é sobre o mercado de trabalho, não sobre câmbio.

O corte de 25 p.b. fica com 11%. **Mas** há uma pressão nova a favor dele: Lula disse, na véspera da votação, "Quero que o Banco Central baixe o juro" (Poder360 · 24/10 · nível B). A frase mostra o que o reeleito quer, não o que o Copom fará; ela entra no downside como risco de um Copom leniente (tempero ii-c). O que limita esse risco no horizonte: Galípolo disse que "meu mandato vai até o final de 2028" (CNN Brasil · 27/10 · nível B), e o agente web não achou, nas duas buscas, proposta de mudar a meta de inflação, o regime ou a lei de autonomia do BC.

**Em 09/12 e no 1T27: a decisão depende de o prêmio ficar e de as expectativas o absorverem.** Manter é a moda (57% em dezembro), mas a Selic acima de 13,75% depois de 09/12 tem 32% (27% de alta só nessa reunião). O que move a decisão, em ordem: a Focus de 2027 e 2028 (hoje 4,34% e 3,75% · `expc_focus_periodo` · 23/10, pesquisa de antes da eleição), a média dos núcleos e os serviços subjacentes (5,32% em 12 meses, contra 5,00% três meses antes · `inflc_decomposicao` · set) e o câmbio de partida de dezembro, que já conterá só pregões depois da eleição. Se a PTAX ficar acima de 5,50 até lá, a alta em 09/12 sobe de 27% para cerca de 46%, porque esse estado pertence quase todo ao regime de alta. **Apesar de** a atividade desacelerar — IBC-Br −0,8% em três meses até agosto (`atv_ibcbr`), e o agente de atividade pondo o hiato em −0,08 já no 1T27, com risco de baixa em todos os trimestres (atividade_r2) —, o Copom já tinha a moderação no cenário (ata da 281ª, §5) e só uma desaceleração mais forte é risco de baixa (comunicado, §4).

O Copom está agindo como sua reação usual implica: cinco cortes iguais de 25 p.b. desde 18/03, de 15,00% para 13,75% (`pm_copom_reuniao`), com o horizonte relevante projetado em 3,2% nas duas últimas reuniões (`pm_copom_projecoes`), acima da meta de 3,00%. Um Copom que corta com a projeção acima da meta aceita convergência lenta; um choque cambial dessa ordem tira essa folga.

### Q2 — O que o Copom deveria fazer, pelos dados?

**Manter 13,75% em novembro e dezembro, dizer que a calibração acabou, e subir só se aparecer segunda ordem.** O argumento tem três partes.

*A política já é restritiva por qualquer neutro de pesquisa ou do Copom.* A Selic real ex-ante, com a Focus de 12 meses, é 8,8% (`br_interest_rate` e `expc_focus` · 23/10)[^5]:

| Neutro | Valor | Selic real ex-ante acima dele | Fonte |
|---|---|---|---|
| Copom, cenário de referência | 5,00% | +3,8 p.p. | RPM set/26, 2.2 |
| QPC, 5 anos | 5,50% | +3,3 p.p. | `expc_qpc` · R279 |
| QPC, 2 anos | 6,00% | +2,8 p.p. | `expc_qpc` · R279 |
| QPC, curto prazo | 6,40% | +2,4 p.p. | `expc_qpc` · R279 |
| Âncora do modelo (NTN-B 10a + meta), nominal, 26/10 | 11,05% | Selic nominal +2,7 p.p. | `br_interest_rate` · 26/10 |
| Âncora do modelo no 4T26 do P2 (`rr_10a` 7,72 + meta) | 10,72% | Selic nominal +3,0 p.p. | P2, caminho do fiscal |

Uso o intervalo do Copom e do QPC para julgar o aperto, porque são o que o Copom diz usar (RPM set/26, 2.2), e a âncora do modelo como alerta: ela carrega o prêmio de mercado (mapa, 2.5). De 23 para 26/10 a âncora subiu de 9,70% para 11,05% e a distância da Selic até ela caiu de 4,05 para 2,70 p.p. sem o Copom mexer (`br_interest_rate`). Pela leitura do modelo, que é também a do Copom — incerteza sobre a dívida eleva o juro neutro (ata da 281ª, §8) —, o choque de prêmio afrouxou a política. É o argumento contra cortar.

*A inflação e as expectativas não dão folga.* O IPCA de 12 meses está em 4,58% (`inflc_agregados` · set), acima dos 4,40% que o Copom projetava para setembro (RPM set/26, Tabela 2.1.2). O agente de inflação põe o IPCA de 12 meses em ~4,2% no 1T28, um ponto acima da projeção do Copom, "quase todo em preços livres e serviços, e não no câmbio" (inflacao_r2); o P2 dá 4,14%. O agente de expectativas mostra que, nas oito vezes desde 2006 em que a inflação implícita de 2 anos subiu 0,60 p.p. ou mais numa semana, a Focus de 12 meses subiu em seis nos 45 dias úteis seguintes, e dá 55% de a Focus de 2027 passar de 4,6% e 35% de a de 2028 passar de 4,0% até 09/12 (expectativas_r2) — os dois sinalizadores de alta deste report. O hiato da última edição é positivo, 0,41% no 3T26, revisado para cima nos trimestres recentes (`pm_hiato_produto_vintages` · set/26), e o desemprego está em 5,3% (`mt_pnad` · ago).

Os preços administrados vão ser contidos por decisão de governo, e isso é custo adiado. A MP 1.395 zerou PIS/Cofins e Cide da gasolina por 30 dias, "com possibilidade de revisão ou prorrogação" (Agência Brasil · 09/10 · nível B); Durigan disse que, com o Brent alto, a proposta deve ser "manter essa ajuda" em 2027 (Poder360 · 23/10 · nível B); e a Abicom, que o reajuste da Petrobras "terá que ser de maneira lenta e gradual" (CNN Brasil · 26/10 · nível B). A projeção do Copom supõe o fim das subvenções e desonerações no prazo legal (RPM set/26, 2.2, nota 45). Mantê-las baixa o IPCA medido de 2027 e transfere o custo para o fiscal, isto é, para o prêmio; uma meta cumprida por subsídio não reancora expectativas (mapa conceitual, 2.2).

*Mas subir agora seria cedo.* A transmissão está funcionando: a inadimplência da carteira livre de pessoa física subiu 1,0 p.p. em 12 meses, para 8,0% (`cred_credito_resumo` · ago), e o comprometimento de renda com a dívida 1,4 p.p., para 28,7% (`cred_credito_familias` · jul) — premissa *assumida*, crédito sem agente; o próprio BC apontou "o risco fiscal e a inadimplência" como as principais preocupações do Relatório de Estabilidade Financeira (Agência Brasil · 27/10 · nível B). O hiato deve virar negativo (RPM set/26, 2.2: −0,4% no 1T28; atividade_r2: −0,08 já no 1T27). E uma alta, agora, poderia não apreciar o real: em 26/10 o carry à frente subiu de 9,1 para 10,8 p.p. e o real caiu 9% (cambio_r1, E5), e o agente fiscal vê dois dos três conjuntos de sinais de dominância fiscal presentes, nenhum completo (fiscal_r1, F5)[^6]. A alta deveria vir com sinal de segunda ordem: Focus de 2027 acima de 4,6% ou de 2028 acima de 4,0%, serviços subjacentes acelerando no trimestre, ou PTAX acima de 5,40 por mais de duas semanas até a reunião de dezembro.

**A distância entre Q1 e Q2 é pequena em novembro e cresce em dezembro.** Em novembro as duas dizem manter. Em dezembro o Copom pode subir antes do que os dados pedem, empurrado pela curva, que já precifica a alta (Q3): esse é o peso do regime de alta (32%) na cauda de upside. O risco oposto, um Copom que retoma cortes com o câmbio em 5,50 — o BC "dócil" do mapa (Parte 1, item 5) —, alimenta o downside e seria ruim para a credibilidade; fica em 5 p.p., porque o comunicado e a ata da 281ª não deixam espaço para ele e o presidente do BC tem mandato até 2028.

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

- **Contra Q1:** em novembro a curva e eu dizemos o mesmo, manter. Em dezembro ela está 20 p.b. acima da média da minha distribuição, e em março 98 p.b. A curva desenha um ciclo de alta até 15,78% em dezembro de 2027; eu dou 32% a um ciclo de alta, com média de ~14,6% no 2T27 nesse regime (seção 3.3).
- **Contra Q2:** eu não subiria antes de ver segunda ordem; a curva já cobra a alta.
- **Contra o que o Copom sinaliza:** a projeção de 3,2% no 1T28 foi feita com a trajetória da Focus (RPM set/26, 2.2), que na curva de 26/10 está 2 a 4 p.p. abaixo do preço. O Copom não endossa nenhuma das duas: a Focus é condicionante de governança, não a previsão dele (mapa, 2.2).
- **Prêmio, não só caminho, e num mercado que não funcionava:** o salto cresce com o prazo e chega a +323 p.b. em dezembro de 2027, além de onde qualquer comunicação do Copom alcança; na curva real, os anos 5 a 10 levaram 73 dos 135 p.b. A curva de 26/10 foi formada com o Tesouro fora dos leilões e recomprando títulos: em pregão assim, a taxa carrega mais prêmio de liquidez e de risco[^8] do que expectativa. Em 27/10 o prazo médio nominal devolveu parte (Prefixado 2029 −47 p.b., nível B), o que mostra que uma parte do ciclo de alta de 26/10 era pressão de liquidez.
- **A Focus está velha para esta pergunta:** foi coletada até 23/10, antes da eleição. A pesquisa de 30/10 é a primeira com o resultado, e não estará neste ciclo; pela regularidade que o agente de expectativas mediu, ela deve vir mais alta.
- **Espaço para surpresa:** em 04/11 a curva precifica manter, então um corte seria surpresa baixista (11%) e uma alta, altista (12%). Em 09/12, manter com comunicação paciente derrubaria a ponta curta; é o desfecho mais provável (57%).

### Q4 — Por que a central e por que a distribuição

**A central é o que o modelo faz com o juro real de 10 anos que o fiscal escreve.** Na regra (R) a Selic segue a âncora, NTN-B de 10 anos mais a meta, e na curva IS o aperto é medido contra a mesma âncora; por isso o `rr_10a` move a Selic um por um e não move o hiato. O fiscal, principal dessa exógena, escreveu 7,72% de média no 4T26, 7,95% no 1T27 e queda de 0,25 p.p. até 7,70% no 1T28 (fiscal_r2): o nível perto de 8% porque o resultado da eleição dura o horizonte e os +73 p.b. dos anos 5 a 10 são prêmio desse resultado; a queda porque a alta que a curva cobra nos dois primeiros anos não vem se o Copom não subir, porque o Treasury de 10 anos cai no base do externo, e porque há um projeto fiscal anunciado. A história econômica é a do mapa (2.5): um juro real longo que cai porque o prêmio comprime precifica uma consolidação à frente, menos demanda e menos inflação, e a mesma Selic fica mais apertada; o modelo responde abrindo espaço para cortar. Com o juro real de 10 anos perto de 8%, o modelo corta devagar: 13,43% no 4T26 e 12,10% no 1T28, 0,09 a 0,20 p.p. acima do P1, a diferença entre os caminhos de `rr_10a` das duas rodadas. A Selic cai porque a expectativa do modelo converge (Focus de 12 meses de 4,17% no 4T26 para 3,55% no 1T28) e o hiato fica negativo (−0,52% no 1T28), o que encolhe o termo de desvio da regra.

**Onde acho que o modelo erra, e por que isso vai para a assimetria e não para a central:**
- *Ele trata prêmio como neutro.* Com o caminho do fiscal, o prêmio de 26/10 põe 0,8 a 1,0 p.p. na Selic de fechamento do modelo, contra a mesma conta com o `rr_10a` na média de 01 a 23/10 (6,93%), e o hiato sai igual (Modelo Estrutural, `br_interest_rate`). O Copom diz que a incerteza fiscal eleva o neutro (ata da 281ª, §8), mas não sobe nem corta porque o prêmio mexeu: reage à projeção e às expectativas. A (R) não tem um peso livre na âncora para eu multiplicar, então isso não entra como tempero (i). A minha mistura de regimes não segue o `rr_10a`: a Selic dela é a do Copom reagindo a expectativas e câmbio, que pesa mais do que esse 0,8 a 1,0 p.p. (a mediana fica acima da central). Se o prêmio cair sem as expectativas mexerem, o lugar disso é o regime de cortes.
- *A expectativa do modelo começa baixa.* O modelo dá 4,17% de média para o 4T26; a pesquisa de 23/10, sem nenhuma revisão, já fica 0,11 a 0,30 p.p. acima do caminho do modelo em todos os trimestres, e a implícita de 1 ano saltou para 7,87% (expectativas_r2). Com o peso da inércia na (E) 20% maior, ainda dentro do posterior, a Selic média do modelo no 1T28 sobe cerca de 0,5 p.p. (de 12,00% para 12,52%, expectativas_r2). Esse efeito chega à minha regra pela (E) com `R.t3` na mediana; subir também `R.t3` no base contaria a mesma desancoragem duas vezes, e por isso `R.t3` × 1,3 fica só no upside.
- *O modelo corta antes do que o Copom costuma.* Fechar o 4T26 em 13,43 (P2) ou 13,44 (rodada conjunta final, com o `rr_10a` de 7,75 do fiscal) pede mais de um corte de 25 p.b. até 09/12 (0,31 a 0,32 p.p. abaixo de 13,75), com a curva precificando alta; os ciclos de corte de 1999–2026 terminaram em manutenção, não em mais corte depois de um choque (`pm_copom_reuniao`).
- *A regra (R) não tem câmbio nem prêmio.* Com a volatilidade do câmbio, o P2 põe a PTAX em 5,43 no 4T26, perto dos 5,50 de 26/10 e dos 5,35 de 27/10 (nível B); o canal câmbio → inflação → expectativa já passa pelo modelo. O que fica fora é a resposta discreta do Copom ao balanço de riscos (comunicado da 281ª, §4).

Os quatro apontam para cima, e por isso P(up) − P(down) é positivo em todos os trimestres, maior em 4T26 a 2T27, quando a decisão sobre o prêmio se resolve. A assimetria cai até o 1T28 porque, no regime de alta, o Copom volta a cortar em 2027 com o hiato negativo.

**A distribuição** é a mistura de três regimes, com passos reunião a reunião (seção 3.3): cortes retomados (18%: 13 p.p. de reversão do prêmio, 5 p.p. de Copom leniente), pausa longa em 13,75% com cortes a partir do 2T27 (50%), ciclo de alta (32%). Ela não mudou desde a rodada 2, e a evidência nova foi conferida contra ela. A favor de mais alta: a probabilidade de 55% que o agente de expectativas dá ao sinalizador da Focus de 2027 até dezembro. Contra: o prazo médio nominal devolveu 47 p.b. em 27/10 e o governo prometeu enviar o projeto fiscal ainda em 2026. A conta de controle fecha: 55% de o sinal aparecer até dezembro, vezes uma chance de ~55% de o Copom subir quando ele aparece (e não só estender a pausa), dá ~30%, perto dos 32% do regime de alta.

### Notícias

Usadas (veículo · data · nível · papel):
- A causa: CNN Brasil · 25/10 · A (reeleição; a história dos cenários); Agência Brasil · 05/10 · A (1º turno); InfoMoney/Estadão · 26/10 · A e InfoMoney, Agência Brasil · 26–27/10 · A (leilões cancelados e recompras do Tesouro; Q3); InfoMoney/Reuters · 26/10 · B ("disfuncional"; precificação de não corte; Q1 e Q3).
- O pregão de 27/10: Poder360 · 27/10 · B (dólar a R$ 5,350); InfoMoney · 27/10 · B (Prefixado 2029 −47 p.b.; IPCA+ 2040 7,29% → 7,53%); InfoMoney/Reuters · 27/10 · B (DI jan/28 a 14,41%). Sustentam a divisão entre caminho e prêmio.
- A resposta do governo: Poder360 · 26/10 · B (ampliar o superávit; projeto "ainda em 2026"); Poder360, CNN Brasil e Exame · 27/10 · A (projeto de lei complementar para o centro da meta fiscal); InfoMoney · 27/10 · B (Fazenda ainda sem comando anunciado). Movem os pesos dos regimes, não a base.
- O BC: CNN Brasil · 27/10 · B (mandato até 2028); Poder360 · 27/10 · B (Galípolo sem comentar câmbio nem Copom); InfoMoney · 27/10 · B (6x1; rolagem programada de swap); Agência Brasil · 27/10 · B (REF: risco fiscal e inadimplência). Q1, Q2 e E4.
- O reeleito e os preços administrados: Poder360 · 24/10 · B (Lula: juro mais baixo e subsídio a combustíveis; tempero ii-c e Q2); Agência Brasil · 09/10 · B (MP 1.395); Poder360 · 23/10 · B (Durigan: ajuda em 2027); CNN Brasil · 26/10 · B (Abicom). Q2, E6 e S8.
- Meta de inflação: nas duas buscas o agente web não achou nada na janela; sustenta o caminho de `meta_12m`.

### Olhado, sem sinal

- Reservas internacionais · US$ 364,9 bi (`cmb_reservas_bc` · 26/10) · estáveis, nenhuma intervenção à vista ou em linha no mês; em 27/10 só a rolagem programada de swap (InfoMoney · 27/10 · nível B) · diria algo se o BC vendesse à vista ou em linha, o gatilho de E4.
- Swap cambial do BC · −US$ 91,6 bi (`cmb_reservas_bc` · ago) · dado de agosto, anterior ao choque · diria algo se o estoque crescesse acima dos vencimentos em outubro ou novembro.
- Fed Funds · 3,88% no ponto médio (`us_interest_rate` · 27/10) · o agente externo espera mais uma alta, em 28/10 ou em 09/12 (externo_r2) · diria algo se o FOMC acelerasse o passo, o que pesaria no dólar contra emergentes (S13).
- Juros de política dos pares · México 6,50%, Chile 4,50%, Colômbia 12,25%, Peru 4,25% (`inter_interest_rate` · 16–20/10) · nenhum mexeu depois do choque, que foi local · diria algo se os pares subissem juntos.
- Termos de troca · 108,4 (`cmb_termos_troca` · ago) · defasado e sem movimento que explique o choque · diria algo com queda forte das commodities, risco de baixa (iii) do Copom.
- Resultado primário de 12 meses · −0,62% do PIB (`fisc_nfsp` · ago) · anterior ao choque e à promessa de ajuste · diria algo com o conteúdo do projeto de Durigan (S12).
- Índice de difusão · 54,9% (`inflc_agregados` · set) · +2,7 p.p. em 12 meses, sem ruptura · diria algo acima de 60%, sinal de choque se espalhando (S8).

## 3. Premissas

### 3.1 Etapa 1 — o modelo

**Cenários:**
- **Base:** o prêmio de 26/10 fica perto de 8% no juro real de 10 anos até o 1T27 e cede 0,25 p.p. até o 1T28, como escreve o fiscal; o ajuste fiscal prometido não ganha conteúdo que mude o preço; o Copom pausa.
- **Upside:** o prêmio se aprofunda: as decisões fiscais de 2027 afrouxam a política e o mercado lê a reação monetária como insuficiente (cauda do fiscal: CDS a 210 p.b. e NTN-B de 10 anos a 9,1% no 2T27), com a volatilidade cambial perto dos níveis de 2015 (cauda do câmbio); o Copom encerra o ciclo e sobe.
- **Downside:** o projeto para o centro da meta fiscal ganha conteúdo e o mercado o compra (CDS a 115 e NTN-B a 7,3% no 1T27); o Copom retoma os cortes.

**Caminhos das exógenas** (G `pm_rf_cenarios`). O base de cada exógena é o do principal, como entrou no P2; nas caudas, os caminhos de cauda que o principal escreveu no report da rodada 2:

| Exógena | Hoje (valor · tabela · data) | Cenário | 4T26 | 1T27 | 2T27 | 3T27 | 4T27 | 1T28 |
|---|---|---|---|---|---|---|---|---|
| Meta de inflação, 12 meses (`meta_12m`) · principal: este agente | 3,00 · `inflc_meta` · 2026 | base · upside · downside | 3,00 | 3,00 | 3,00 | 3,00 | 3,00 | 3,00 |
| Juro real de 10 anos (`rr_10a`) · principal: fiscal | 8,05 · `br_interest_rate` · 26/10 | base (P2) | 7,72 | 7,95 | 7,90 | 7,80 | 7,75 | 7,70 |
| | | upside (fiscal) | 8,15 | 8,90 | 9,10 | 9,10 | 9,00 | 8,90 |
| | | downside (fiscal) | 7,36 | 7,30 | 7,15 | 7,05 | 7,00 | 6,95 |
| CDS 5 anos (`fiscal`) · principal: fiscal | 137 · `cmb_risco_pais` · 26/10 | base (P2) | 140 | 142 | 139 | 135 | 130 | 125 |
| | | upside (fiscal) | 170 | 205 | 210 | 205 | 198 | 190 |
| | | downside (fiscal) | 122 | 115 | 112 | 110 | 108 | 106 |
| Volatilidade implícita (`vol`) · principal: câmbio | sem dado no F (12,19 no 2T26, no modelo) | base (P2) | 17,0 | 15,5 | 14,5 | 14,0 | 13,5 | 13,5 |
| | | upside (câmbio) | 24,0 | 21,0 | 18,0 | 16,0 | 15,0 | 15,0 |
| | | downside (câmbio) | 13,0 | 12,5 | 12,0 | 12,0 | 12,0 | 12,0 |
| Fed Funds (`ffr`) · principal: externo | 3,88 · `us_interest_rate` · 27/10 | os três (P2) | 4,13 | 4,13 | 4,13 | 4,13 | 4,13 | 3,88 |
| Inflação dos EUA no trimestre (`infl_us`) · principal: externo | — | os três (P2) | 0,86 | 0,61 | 0,61 | 0,65 | 0,63 | 0,65 |
| Dólar contra emergentes (`dxy_em`) · principal: externo | 130,2 · `cmb_dollar_index_em` · 23/10 | os três (P2) | 130,5 | 131,0 | 130,5 | 130,0 | 129,5 | 129,0 |
| S&P 500 (`sp500`) · principal: externo | — | os três (P2) | 7.750 | 7.900 | 8.050 | 8.200 | 8.350 | 8.500 |
| IC-Br em dólar (`icbr_usd`) · principal: externo | 205,7 · `comm_icbr_usd` · set | os três (P2) | 206,2 | 202,6 | 201,0 | 199,9 | 199,0 | 198,3 |
| IC-Br agropecuária em dólar (`icbr_agr_usd`) · principal: externo | 201,8 · `comm_icbr_usd` · set | os três (P2) | 203,9 | 200,9 | 199,3 | 198,4 | 197,8 | 197,4 |
| IC-Br metal em dólar (`icbr_met_usd`) · principal: externo | 335,1 · `comm_icbr_usd` · set | os três (P2) | 331,7 | 330,0 | 330,0 | 328,7 | 327,3 | 325,7 |

- `meta_12m`: a meta contínua de 3,00% do CMN, sem decisão de mudança no dado (`inflc_meta`, 2026) nem notícia nas duas buscas do agente web; igual nos três cenários.
- As caudas do externo não entram: os cenários desta tese são domésticos, e o bloco externo fica no base do principal nos três.

**Saída do modelo** (centrais; a faixa de 90% do posterior dos pesos está no G e não é intervalo de previsão[^9]):

| Variável | Cenário | 4T26 | 1T27 | 2T27 | 3T27 | 4T27 | 1T28 |
|---|---|---|---|---|---|---|---|
| Selic, fechamento (% a.a.) | base (= P2) | 13,43 | 13,21 | 12,87 | 12,56 | 12,30 | 12,10 |
| | upside | 14,12 | 14,29 | 14,14 | 13,88 | 13,60 | 13,38 |
| | upside, R.t3 × 1,3 | 14,28 | 14,57 | 14,50 | 14,29 | 14,02 | 13,80 |
| | downside | 12,92 | 12,50 | 12,10 | 11,78 | 11,52 | 11,31 |
| Selic, média do trimestre (% a.a.) | base | 13,48 | 13,37 | 13,04 | 12,69 | 12,43 | 12,18 |
| IPCA 12 meses (%) | base | 5,34 | 4,95 | 4,46 | 4,48 | 4,32 | 4,14 |
| | upside | 5,36 | 5,04 | 4,62 | 4,68 | 4,52 | 4,29 |
| | downside | 5,32 | 4,89 | 4,38 | 4,39 | 4,24 | 4,09 |
| Focus IPCA 12m, média do trimestre (%) | base | 4,17 | 4,00 | 3,82 | 3,71 | 3,63 | 3,55 |
| | upside | 4,18 | 4,01 | 3,85 | 3,77 | 3,69 | 3,61 |
| | downside | 4,17 | 3,99 | 3,80 | 3,69 | 3,60 | 3,52 |
| Hiato (% do potencial) | base, upside e downside | 0,13 | −0,08 | −0,24 | −0,36 | −0,45 | −0,52 |
| PTAX, fechamento (R$/US$) | base | 5,43 | 5,52 | 5,52 | 5,50 | 5,51 | 5,53 |
| | upside | 5,64 | 5,87 | 5,88 | 5,83 | 5,82 | 5,83 |
| | downside | 5,28 | 5,35 | 5,36 | 5,37 | 5,40 | 5,43 |

O hiato é praticamente o mesmo nos três cenários (diferença máxima de 0,01 p.p.) porque a Selic acompanha a âncora um por um e a IS mede o aperto contra a mesma âncora; só com R.t3 × 1,3 ele cai mais, a −0,61% no 1T28. Do 3T27 em diante a Selic do upside sem tempero (13,88 a 13,38) fica dentro da faixa base: o que leva à cauda de cima, a partir dali, é o tempero, não o modelo. O IPCA de 12 meses do modelo fica em 4,14% no 1T28 no base, contra 3,2% do Copom (`pm_copom_projecoes`, RPM 281ª); a leitura do caminho é do agente de inflação (S8).

### 3.2 Etapa 2 — o tempero qualitativo

**(i) Regra de juros (R), reação ao desvio da expectativa contra a meta — efeito mais forte que o estimado** · cenário upside
- Coeficiente `R.t3`: estimado 1,96, intervalo de 90% do posterior 1,15 a 2,73. Multiplicador × 1,3 (2,55), dentro do intervalo, no percentil 87.
- Efeito: Selic de fechamento do upside de 14,12 → 14,28 no 4T26 e de 14,14 → 14,50 no 2T27 (G `pm_rf_cenarios`).
- Por quê: o Copom disse, por unanimidade, que expectativas desancoradas exigem "uma restrição monetária maior e por mais tempo do que outrora seria apropriado" (ata da 281ª, §10), e a desancoragem prolongada torna as expectativas mais sensíveis a choques (RPM set/26, 2.3, risco i). No upside a desancoragem é o que acontece; reagir mais a ela é a função de reação que o próprio Copom descreveu. Fica dentro do intervalo, então não afirmo que o histórico subestima o canal, só que este Copom está na ponta de cima dele. Não aplico no base: a âncora mais fraca que o agente de expectativas argumenta já chega à regra pela (E) com `R.t3` na mediana (+0,5 p.p. na Selic média do 1T28), e a minha distribuição já está nesse nível.
- Onde entra: limite da cauda de upside.

**(ii-a) A reação do Copom ao câmbio e ao prêmio, que a regra (R) não tem** · cenários base e upside
- Hoje: PTAX 5,50 (`cmb_ptax` · 26/10) e dólar comercial a 5,35 em 27/10 (Poder360 · nível B), contra o condicionante de R$ 5,15 da 281ª; CDS 137 p.b. (`cmb_risco_pais` · 26/10).
- Por que o modelo não vê: (R) só lê a Selic defasada, a âncora e o desvio da Focus; o Copom reage à projeção no horizonte relevante, cujo câmbio de partida é o de mercado nos dez dias úteis anteriores (ata da 281ª, nota 2), e põe o câmbio depreciado entre os riscos de alta (§13). A PTAX do modelo já está perto do mercado (5,43 no P2), então o canal câmbio → inflação → expectativa passa pelo modelo; o que fica fora é a resposta discreta do Copom ao balanço de riscos.
- Efeito: +25 a +50 p.b. sobre o caminho do modelo até 09/12 enquanto a PTAX ficar acima de ~5,40; é o que faz o regime de alta (32%). Com a PTAX acima de 5,50 até dezembro, a alta em 09/12 vai a ~46%.
- Onde entra: assimetria do cenário base (+0,26 no 4T26) e limite da cauda de upside (14,25 em dezembro, 14,75 em março).

**(ii-b) Gradualismo e "serenidade e cautela"** · todos os cenários
- Hoje: cinco cortes seguidos de 25 p.b. desde 18/03 (`pm_copom_reuniao`); em 248 decisões desde 1999, nenhuma alta veio logo depois de um corte e os 14 ciclos de corte terminaram numa manutenção (mesma tabela).
- Por que o modelo não vê: (R) é contínua sobre médias trimestrais; no downside ela leva a Selic de 13,75% a 12,92% até dezembro, o que pediria um corte de 50 p.b. e outro de 25 nas duas reuniões, quando o ciclo de 2026 andou só de 25 em 25.
- Efeito: comprime as caudas do 4T26 e do 1T27: o downside do modelo, 12,92, vira 13,50 em dezembro (percentil 10); uma alta em 04/11 fica em 12%.
- Onde entra: limites das caudas do 4T26 e 1T27; probabilidades da reunião de 04/11.

**(ii-c) Pressão política por juro mais baixo** · cenário downside
- Hoje: Lula, reeleito em 25/10 (nível A), disse em 24/10 "Quero que o Banco Central baixe o juro" (Poder360 · nível B). Contra: Galípolo disse que o seu mandato vai até o fim de 2028 (CNN Brasil · 27/10 · nível B), e não há, nas duas buscas, proposta de mudar a meta ou a autonomia do BC.
- Por que o modelo não vê: a postura do BC diante do governo não passa por nenhuma exógena; a (R) não tem um termo de independência.
- Efeito: 5 p.p. de probabilidade de cortes de 25 p.b. a partir de dezembro mesmo com a PTAX acima de 5,40; no fechamento, os mesmos passos do regime de cortes. Dura enquanto a resposta do Copom ao choque não for conhecida (04/11 e 09/12).
- Onde entra: probabilidade do downside, que deixa de ser só boa notícia.

### 3.3 Da etapa 1 à tese

| Trimestre | Central (P2) | Upside: modelo → com tempero | Downside: modelo → com tempero |
|---|---|---|---|
| 4T26 | 13,43 | 14,12 → 14,28 (R.t3) → 14,25 | 12,92 → 13,50 |
| 1T27 | 13,21 | 14,29 → 14,57 → 14,75 | 12,50 → 13,00 |
| 2T27 | 12,87 | 14,14 → 14,50 → 14,75 | 12,10 → 12,75 |
| 3T27 | 12,56 | 13,88 → 14,29 → 14,75 | 11,78 → 12,25 |
| 4T27 | 12,30 | 13,60 → 14,02 → 14,50 | 11,52 → 12,00 |
| 1T28 | 12,10 | 13,38 → 13,80 → 14,25 | 11,31 → 11,75 |

Os pontos "com tempero" são os percentis 10 e 90 da distribuição da Selic de fechamento que sai da mistura dos três regimes, com passos de reunião a reunião (G `pm_r2_distribuicao`, sem mudança no report final). No 4T26 o percentil 90 (14,25) fica abaixo do upside do modelo com R.t3 (14,28) porque a Selic só anda em degraus e o gradualismo limita dezembro a duas decisões. Os regimes, com a média da Selic de fechamento em cada um:

| Regime | Peso | 4T26 | 1T27 | 2T27 | 3T27 | 4T27 | 1T28 |
|---|---|---|---|---|---|---|---|
| Cortes de 25 p.b. retomados (reversão do prêmio 13 p.p.; Copom leniente 5 p.p.) | 18% | 13,45 | 13,05 | 12,65 | 12,25 | 11,85 | 11,60 |
| Pausa: 13,75% até o 1T27, cortes de 25 p.b. a partir do 2T27, mais firmes no 2S27 | 50% | 13,76 | 13,74 | 13,56 | 13,26 | 12,96 | 12,69 |
| Alta: ciclo de 50 a 100 p.b. até o 2T27, cortes no fim de 2027 | 32% | 14,11 | 14,51 | 14,61 | 14,54 | 14,36 | 14,14 |

A faixa base de cada trimestre contém a central do P2 e o grosso da pausa; as probabilidades da seção 1 são a massa da mistura dentro da faixa, acima e abaixo dela. A mediana da mistura é 13,75 até o 2T27, acima da central em todos os trimestres: é a forma numérica de dizer que a central não leva tempero e que a força que eu acredito estar ausente do modelo foi para a assimetria.

**O que derrubaria a tese:**
- Focus de 2027 acima de 4,6% ou de 2028 acima de 4,0%, ou PTAX acima de 5,50 por duas semanas antes de 09/12: a alta em dezembro passa a ser o mais provável, e a faixa do 4T26 sobe.
- Copom cortando em 04/11, ou comunicado sem encerrar a calibração com a PTAX acima de 5,40: o regime leniente ganha peso e o downside deixa de ser boa notícia.
- Projeto fiscal enviado com corte de despesa e NTN-B de 10 anos abaixo de 7,20% com o CDS abaixo de 120 por dez pregões (o signpost do fiscal): o regime de cortes por reversão ganha peso.

## 4. Para os outros agentes

### Respostas às entradas fixas

- **E1 (câmbio), em destaque:** a tese da seção 1, com as reuniões de 04/11 a 17/03. O motivo do destaque: num pregão a curva passou a precificar alta em vez de corte a partir de dezembro. Para o carry à frente: no regime mais provável (50%) a Selic fica em 13,75% até o 1T27; no de alta (32%), sobe até ~14,6% de média no 2T27. A central do modelo, que corta devagar, está abaixo das duas. Ao seu S1 do r2: se a PTAX ficar acima de 5,50 até 09/12, a alta em dezembro vai de 27% para ~46%.
- **E2 (câmbio):** uma pausa é lida como credibilidade e um corte como validação da desancoragem. Uma alta só é lida como credibilidade se vier com sinal de segunda ordem nas expectativas (Q2); sem ele, num choque de prêmio político e fiscal, com o carry descolado do real em 26/10 e dois dos três sinais de dominância presentes (fiscal), ela pode ser lida como custo da dívida, e o sinal do elo juro → câmbio deixa de ser garantido (mapa, 2.6). Ao seu S2/S7: com uma alta em 09/12 sem sinal de segunda ordem, eu poria a cauda de dominância acima dos ~10% do fiscal; com o sinal, abaixo. A estimativa da cauda é do fiscal.
- **E3 (câmbio), em destaque:** o Copom condicionou a projeção a R$ 5,15 seguindo a PPC, a média de dez dias úteis encerrados na semana anterior à da reunião (comunicado da 281ª, Tabela 1; ata, nota 2), listou "uma taxa de câmbio persistentemente mais depreciada" como risco de alta (ata, §13) e explicou a depreciação anterior pelo diferencial de juros em queda (RPM set/26, 2.2). Ao seu S3: o câmbio de partida de 04/11 (19 a 30/10) fica entre R$ 5,21 e R$ 5,27, conforme os pregões de 27 a 30/10 fiquem perto de 5,35 ou de 5,50 (`cmb_ptax` até 26/10); a governança o usa como sai, sem ajuste (ata, nota 2: "procedimento usual"). O de 09/12 será só de pregões depois da eleição.
- **E4 (câmbio):** o gatilho não disparou: nenhuma intervenção à vista ou em linha em outubro até 26/10 (`cmb_reservas_bc`), só a rolagem programada de swap em 27/10 (InfoMoney · 27/10 · nível B), e Galípolo não comentou parâmetros de intervenção (Poder360 · 27/10 · nível B). Pela taxa: o Copom responde ao câmbio pela segunda ordem e pela projeção (ata da 281ª, §16); minha leitura é manter em 04/11 (77%), com 32% de a Selic estar acima de 13,75% depois de 09/12.
- **E5 (inflação):** a tese da seção 1. Ao IN-S3 do r2: sim, o câmbio de partida de 09/12 deve ficar perto da PTAX de então; com a central do câmbio (5,43 no 4T26), a próxima projeção fecha parte da diferença contra o modelo, não toda, porque o agente de inflação a põe em preços livres e serviços.
- **E6 (inflação):** projeção do cenário de referência, IPCA 12 meses: 4,4 (3T26), 5,2 (4T26), 4,9 (1T27), 4,5 (2T27), 4,5 (3T27), 3,9 (4T27), 3,2 (1T28); administrados 3,9 / 5,3 / 4,5 / 4,0 / 4,3 / 3,5 / 3,2 (`pm_copom_projecoes`, RPM 281ª). Condicionantes: Selic da Focus, câmbio de R$ 5,15 pela PPC, Brent na curva futura por seis meses — partindo de US$ 90 no 3T26, pico no 4T26 e cerca de US$ 84 no 2T27 — e 2% ao ano depois, bandeira amarela em dezembro de 2026 e de 2027 (comunicado), fim das subvenções e desonerações de combustíveis no prazo legal (RPM set/26, 2.2 e nota 45). Ao IN-S4: o RPM descreve as subvenções ao diesel e à gasolina de 2026 (MP 1.340, 1.358, 1.363 e 1.391, esta sem o ato que fixa valor e datas) mas não separa quanto dos 4,5% de administrados do 1T27 vem do fim delas; a bandeira "neutra" de 2027 não é uma cor: é "uma sequência de bandeiras idêntica à observada e projetada para os meses finais de trimestre de 2026", amarela em dezembro de 2026 (RPM set/26, 2.2), escolhida para que a energia não afete as projeções do horizonte relevante. Condicionamento, não previsão do Copom. Depois da 281ª, a MP 1.395 zerou tributos da gasolina por 30 dias (Agência Brasil · 09/10 · nível B), fora da projeção de setembro.
- **E7 (atividade):** a tese da seção 1 e as caudas; a média do trimestre é a do P2 (13,48 no 4T26, 13,37 no 1T27, 12,18 no 1T28) e o fechamento é a tese. Ao seu S-PM1 do r2: a minha distribuição tem médias no fechamento de 13,82 (4T26), 13,86 (1T27), 13,73 (2T27), 13,49 (3T27), 13,21 (4T27) e 12,96 (1T28); a média dentro do trimestre ela não calcula. A decisão de 04/11 não está tomada neste report: o ciclo fecha antes dela.
- **E8 (atividade):** a tabela de neutros de Q2. Contra o neutro do Copom (5,00%) a Selic real ex-ante está 3,8 p.p. acima; contra a âncora do modelo, 2,7 p.p. no pregão de 26/10 e 3,0 p.p. na média do 4T26 do P2. O prêmio de 26/10 entra no modelo como neutro mais alto (0,8 a 1,0 p.p. de Selic) e, para a atividade, como custo de capital; os dois estão certos para o seu lado, e o meu tempero não segue a âncora (Q4).
- **E9 (atividade):** "moderação gradual da atividade econômica, principalmente em setores mais cíclicos, embora ainda em patamar resiliente, e mercado de trabalho aquecido" (comunicado da 281ª, §2); hiato de 0,5% no 2T26 e 0,4% no 3T26, projetado em −0,4% no 1T28 (RPM set/26, 2.2); na edição de set/26 os trimestres de 2T25 a 2T26 foram revistos para cima de 0,10 a 0,15 p.p. (`pm_hiato_produto_vintages`); salários reais acima da produtividade (ata, §7). Sobre o 3T26: o RPM diz que julho e agosto "apontam para nova moderação da atividade no terceiro trimestre", revisou o PIB de 2026 de 2,0% para 1,8% e, para o hiato do 3T26, usou "projeções das variáveis de atividade quando os dados não estavam disponíveis" (RPM set/26, nota 50); não achei no texto o número de PIB do 3T26 por trás dos 0,41.
- **E10 (fiscal):** a tese da seção 1.
- **E11 (fiscal):** a política fiscal age no curto prazo pela demanda e estruturalmente pelo prêmio a termo; "o esmorecimento no esforço de reformas estruturais e disciplina fiscal, o aumento de crédito direcionado e as incertezas sobre a estabilização da dívida pública têm o potencial de elevar a taxa de juros neutra" (ata da 281ª, §8); o Comitê "segue acompanhando como os desenvolvimentos da política fiscal doméstica impactam a política monetária e os ativos financeiros" (comunicado, §5). O Copom lê fiscal como demanda, como prêmio e como neutro. O choque de 26/10 é do segundo tipo, e o Copom ainda não falou dele.
- **E12 (fiscal):** a divisão está em "Como subordinado", abaixo.
- **E13 (fiscal):** a mesma leitura de E2. Ao FS-PM4 do r2 (manter ou subir em 04/11: credibilidade ou custo da dívida?): manter é lido como credibilidade, e o pregão de 27/10 é o primeiro indício — o prazo médio nominal devolveu 47 p.b. enquanto a curva passava a esperar pausa. Uma alta em 04/11 (12%) sem sinal de segunda ordem é o caso em que eu esperaria a leitura de custo da dívida, com o juro real longo, que subiu de novo em 27/10, abrindo.
- **E14 (externo):** a tese da seção 1. O juro real brasileiro ex-post era o maior entre os pares, 9,8% em agosto (`cmb_real_rates`); na central do modelo o diferencial contra o Fed cai de cerca de 9,3 p.p. no 4T26 para cerca de 8,2 p.p. no 1T28, e na pausa fica perto de 9,6 até o 1T27[^13]. Ao XS3: o Copom cita "a incerteza sobre a política monetária em algumas economias avançadas" como razão de cautela (comunicado, §1); um Fed em alta pesa contra cortar, não a favor de subir.
- **E15 (externo):** ambiente externo "incerto em função da indefinição acerca dos conflitos armados no Oriente Médio e da incerteza sobre a política monetária em algumas economias avançadas" (comunicado da 281ª, §1); riscos de baixa vindos de fora: desaceleração global e queda das commodities (§4). Ao XS4: a premissa de petróleo não é decisão: o Brent "segue aproximadamente a curva futura pelos próximos seis meses e passa a aumentar 2% ao ano posteriormente, conforme governança usual" (ata, §11); na reunião de 04/11 ela se atualiza sozinha à curva do momento, e um Brent acima de US$ 110 entra na projeção de administrados sem que o Copom precise revisar nada.
- **E16 e E21:** não se aplicam: o principal de `rr_10a` é o fiscal. Meus insumos estão em "Como subordinado".
- **E17 (expectativas):** o Copom responde à desancoragem com "restrição monetária maior e por mais tempo" (ata da 281ª, §10); na regra do modelo, o coeficiente sobre o desvio da Focus contra a meta é 1,96 (`R.t3`, mediana). Ao XS1: com a eleição como causa, a pausa em 04/11 foi de 75% (r1) para 77%, e a alta até 09/12 de 29% para 27%, com a Selic acima de 13,75% depois de dezembro em 32%; a divisão do upside entre âncora fraca e âncora quase sem peso fica com você, e o meu `R.t3` × 1,3 só vale no upside.
- **E18 (expectativas):** o Copom julga a ancoragem em horizontes de dois ou três anos (RPM set/26, 2.3); diz que as expectativas "permanecem acima da meta de inflação em todos os horizontes" e que "monitora com atenção a desancoragem das expectativas de inflação para prazos mais longos" (ata da 281ª, §10); registrou a Focus de 2028 subindo de 3,69% para 3,80% como desancoragem adicional (RPM set/26, 2.2). Ao XS2: os 3,50% dos longos são, para o Copom, desancoragem a combater, não piso aceito — é a esse horizonte que se refere a frase da ata, e foi a ele que o Copom atribuiu o custo de desinflação maior. Nenhum diretor falou de expectativas depois de 26/10 na janela: Galípolo não comentou o Copom (Poder360 · 27/10 · nível B).
- **E19 (expectativas):** `meta_12m` em 3,00% nos seis trimestres. Ao XS3: a fala de Lula é sobre a Selic, não sobre a meta; o mandato de Galípolo vai até o fim de 2028, depois do horizonte; nas duas buscas do agente web não houve proposta nem discussão sobre a meta ou a diretoria. O risco de mudança da meta no horizonte da tese fica fora da distribuição.
- **E20 (expectativas):** a tabela de Q3: curva menos Focus de +23 p.b. em 04/11 a +403 p.b. em dezembro de 2027, a maior parte prêmio. Ao XS4: em 2027, dos +145 a +403 p.b. entre curva e Focus, a parte que eu espero de Selic é a diferença entre a minha média e a Focus (+85 p.b. em janeiro, +111 em março); o resto, a maior parte, é prêmio e pesquisa velha. Na curva real, dois anos levaram 22 dos 135 p.b.

### Pedidos

Para o próximo ciclo, com a pergunta e a tese que depende dela:
- **S1 a S6 (câmbio):** o patamar de 5,35–5,50 fica até 09/12? Qual o câmbio de partida da projeção de dezembro? O carry voltou a segurar o real depois de 27/10? Houve disfunção que o BC tenha respondido com câmbio? Teses dependentes: o peso do regime de alta e o gatilho de E4.
- **S7 e S8 (inflação):** o repasse da PTAX de 5,43–5,50 no 4T26–2T27, e quanto a MP 1.395 e a subvenção de 2027 tiram do IPCA de 12 meses e devolvem quando acabarem. Tese dependente: a diferença de 0,9 a 1,0 p.p. contra o Copom no 1T28 e o critério de segunda ordem.
- **S9 (expectativas):** a Focus de 30/10 e de 06/11 em 2027 e 2028 contra os limiares de 4,6% e 4,0%. Tese dependente: a alta em 09/12.
- **S10 (atividade):** o PIB do 3T26 (dez/26) e a revisão do hiato de partida no RPM de dezembro. Tese dependente: o "cedo demais para subir".
- **S11 e S12 (fiscal):** o conteúdo do projeto para o centro da meta e o que ele faz com o `rr_10a` de 2027. Tese dependente: o peso do regime de cortes por reversão e a central inteira.
- **S13 (externo):** a decisão do FOMC de 28/10 e o caminho até 09/12. Tese dependente: o dólar contra emergentes na véspera da reunião de dezembro.
- **Ao agente web:** a decisão e o comunicado do Copom de 04/11 (para o placar e a guidance); falas de diretores sobre câmbio e expectativas depois de 27/10; o envio do projeto fiscal; decisões da Petrobras e a prorrogação da MP 1.395; qualquer proposta sobre a meta de inflação ou a diretoria do BC.

### Como subordinado

- **`rr_10a` · principal: fiscal**
  - Insumos:
    - A divisão da alta de 23 para 26/10 pelos trechos da curva real: dos +135 p.b. da NTN-B de 10 anos, +4 p.b. vêm do primeiro ano, +18 do segundo, +40 dos anos 2 a 5 e +73 dos anos 5 a 10 (`br_interest_rate` · 23 e 26/10). O caminho de política que o Copom controla está nos dois primeiros anos; o salto concentrado depois do 5º ano é prêmio.
    - O pregão de 27/10 separou as duas partes: o prazo médio nominal devolveu (Prefixado 2029 −47 p.b.) e o juro real longo subiu mais (IPCA+ 2040 de 7,29% para 7,53%) (InfoMoney · 27/10 · nível B).
    - O juro real de política que a Focus espera é 7,1% em 2027, 6,0% em 2028 e 6,3% em 2029 (`expc_focus_periodo` · 23/10, antes da eleição): o caminho do fiscal, 7,70% no 1T28, fica ~1,7 p.p. acima do de 2028, a medida do prêmio de prazo e fiscal que sobra.
    - No simulador, `rr_10a` move a Selic um por um, no mesmo trimestre, e não move o hiato; o prêmio de 26/10 põe 0,8 a 1,0 p.p. na Selic de fechamento da base.
  - Argumento: o caminho do P2 (7,72 · 7,95 · 7,90 · 7,80 · 7,75 · 7,70) separa as duas partes do salto como eu separo, e o pregão de 27/10 confirma a divisão. Sem argumento para mais alto ou mais baixo. Volta para cima se o projeto fiscal não sair até o 1T27 ou se o Copom subir em dezembro sem sinal de segunda ordem.
  - Caminho de referência: nenhum.
  - Resposta do principal: o fiscal aceitou o argumento dos dois primeiros anos e foi a esse caminho na moderação da rodada 2 (ata_r2, item 1); divergência fechada.

### Divergências

- **`meta_12m` · subordinado: fiscal.** O fiscal não trouxe argumento nem caminho de referência nas duas rodadas e diz não ter "nenhuma informação nem sinal de que o governo pretende mudar ou discutir a meta de inflação" (fiscal_r2); o P2 não lista divergência. Mantenho 3,00% nos seis trimestres. Mudaria com uma decisão ou proposta formal do CMN, ou uma fala nominal do governo pedindo meta mais alta.

## 5. Placar

Primeiro ciclo: não há report final anterior deste agente (o ciclo de 2026-10-22 não tem `politica_monetaria_rf.md`). Nenhum trimestre nem reunião a conferir; o placar deste report começa com a reunião de 04/11/2026 (o passo mais provável é manter, com 77%) e com o fechamento do 4T26 (faixa 13,30 a 13,80).

## 6. Sobre o modelo

O Modelo Estrutural não muda neste ciclo (decisão do usuário); o que segue são propostas.

| Fonte | O que sugere (regressor, defasagem, quebra, âncora) | Teste proposto (dado, amostra, que resultado mudaria a especificação) | Por que importa para a tese deste ciclo |
|---|---|---|---|
| Mapa conceitual, 2.5 (a âncora carrega prêmio de prazo e fiscal, não é o neutro do Copom); RPM set/26, 2.2 (neutro de 5,00%); a divisão por trechos da curva real (`br_interest_rate`, 23 e 26/10: 73 dos 135 p.b. nos anos 5 a 10); a proposta do fiscal pelo outro lado (separar o `rr_10a` explicado pelo CDS) e a da atividade (o prêmio como custo de capital na IS); moderação da rodada 2, item 5 | Na (R), a Selic segue `rr_10a` + meta um por um e no mesmo trimestre, e o prêmio de 26/10 vira 0,8 a 1,0 p.p. de Selic. Liberar o coeficiente da âncora, ou trocá-la por um trecho mais curto da curva real (NTN-B de 5 anos ou o termo de 2 a 5 anos) | (R) com o coeficiente da âncora livre, 2006–2026, `br_interest_rate` e `pm_copom_reuniao`; e a mesma (R) com a âncora de 5 anos e com o termo de 2 a 5 anos. Coeficiente bem abaixo de 1 (digamos < 0,5) com a de 10 anos, ou ajuste melhor fora da amostra com uma âncora mais curta, muda a âncora | A central deste ciclo é, na prática, o caminho de `rr_10a`: as duas revisões do fiscal moveram a central em 0,1 a 0,5 p.p. sem nenhum dado novo de inflação ou atividade |
| Comunicado da 281ª, §4 (câmbio depreciado como risco de alta); `pm_copom_reuniao` (2002: +300 p.b. em 14/10/2002, depois de duas manutenções) | (R) não tem câmbio nem prêmio de risco; acrescentar a variação trimestral da PTAX ou do CDS | (R) com a variação da PTAX (ou do CDS) no trimestre, 2003–2026, `cmb_ptax`, `cmb_risco_pais`, `pm_copom_reuniao`. Coeficiente positivo e estável, com ganho de ajuste fora da amostra, entra na regra | O choque é de câmbio e prêmio, e a regra só o vê pela Focus, com defasagem: é o tempero (ii-a), que hoje está fora do modelo |
| `pm_copom_reuniao` (cinco cortes iguais de 25 p.b. em 2026; nenhuma alta logo depois de um corte em 248 decisões) | A Selic de fechamento derivada da média é contínua; a decisão é discreta e gradual. Um termo de passo máximo, ou a regra estimada sobre o fechamento | Comparar, 2006–2026, o erro da Selic de fechamento derivada com o de uma regra estimada direto no fechamento com o passo arredondado a 25 p.b.; mudar se o erro cair nos trimestres de virada de ciclo | A central do 4T26 (13,43) pede mais de um corte de 25 p.b. até 09/12 com a curva precificando alta; o tempero (ii-b) corrige isso fora do modelo |
| A pesquisa de 23/10 acima do caminho da (E) em todos os trimestres (expectativas_r2; o mesmo nos reports de inflação e deste agente) | O primeiro trimestre projetado de `focus_12m` ignora as pesquisas já feitas nele, e o erro chega à (R) pelo desvio contra a meta | A proposta é do agente de expectativas (condicionar o 1º trimestre à média parcial já observada); para a (R), medir nos ciclos passados quanto o erro do 1º trimestre da (E) move a Selic projetada | O termo de desvio da (R) começa baixo neste ciclo, e é por ele que a central corta |

[^1]: A meta Selic muda só nas reuniões do Copom, cerca de duas por trimestre. O valor de fechamento do trimestre é a decisão da última reunião dentro dele: 09/12 para o 4T26, 17/03 para o 1T27, e assim por diante. O calendário oficial vai até 08/12/2027; para o 1T28 supus duas reuniões, como em todos os trimestres de 2022 a 2027.
[^2]: O Modelo Estrutural só tem a Selic média de cada trimestre. A de fechamento é derivada: a média deste trimestre e do seguinte, dividida por dois. Medida de 2006 a 2026, a regra erra 0,12 p.p. em média e 0,55 no pior trimestre.
[^3]: As probabilidades de cada reunião saem de três regimes (cortes retomados, pausa, alta), cada um com a chance de cada passo em cada reunião; a tabela é a média ponderada. O mesmo cálculo dá a distribuição do fechamento de cada trimestre, então a tabela de reuniões e a tese não podem se contradizer.
[^4]: Comentário de processo: os números vêm de uma fotografia dos dados tirada no início do ciclo, que vai até 26/10; o que aconteceu em 27/10 entra só pelas notícias que o agente web buscou, com o nível de cada uma.
[^5]: Juro neutro é a taxa real que não acelera nem freia a economia. Se a Selic real (descontada da inflação esperada) está acima dele, a política é restritiva. Exemplo: Selic real de 8,8% contra neutro de 5,0% é um aperto de cerca de 3,8 p.p. O neutro não é observado; cada fonte o estima de um jeito.
[^6]: Dominância fiscal, na versão de Blanchard (2004) para o Brasil de 2002: quando a dívida é alta e o investidor teme o calote, subir os juros pode aumentar o risco percebido e depreciar a moeda, em vez de apreciá-la. É um espectro, não uma chave; a avaliação fiscal é do agente fiscal.
[^7]: A Selic esperada para cada reunião sai da curva de DI: a taxa a termo entre a vigência de uma decisão e a da seguinte, somada a 0,10 p.p., a distância usual entre o CDI e a meta Selic. É preço, não previsão. O cálculo deste report e o do F diferem em até 0,15 p.p. em algumas reuniões; o salto de 23 para 26/10 usa o mesmo cálculo nas duas datas.
[^8]: Prêmio de prazo é a remuneração extra que o investidor pede para travar um juro longo em vez de rolar juros curtos. Por isso a taxa de um contrato de DI para dezembro de 2027 não é só a Selic que o mercado espera para lá: ela inclui um prêmio, que sobe quando a incerteza sobe e quando o mercado funciona mal.
[^9]: A faixa que o modelo imprime cobre só a incerteza dos pesos estimados das equações, não os erros delas. Não é um intervalo de previsão; a distribuição da tese é deste agente.
[^10]: Percentil 10 é o valor abaixo do qual ficam 10% dos desfechos possíveis; percentil 90, o valor abaixo do qual ficam 90%. Entre os dois estão 80% dos desfechos.
[^11]: Como a Selic só assume múltiplos de 0,25, o limite de cada faixa é posto entre dois degraus, de modo que a faixa contenha a central do modelo (que não é um degrau) e um conjunto exato de decisões. No 4T26, 13,30 a 13,80 contém 13,43 e as decisões 13,50 e 13,75.
[^12]: Juro real a termo é o juro real que a curva de hoje implica para um trecho do futuro: o "de 5 a 10 anos" é o juro real anual que o investidor trava hoje para os anos 5 a 10. A NTN-B de 10 anos é, aproximadamente, a média desses trechos ponderada pela duração de cada um, então a alta dela pode ser dividida entre eles. O caminho da Selic que o Copom controla pesa nos primeiros dois anos; o que sobe depois disso é prêmio.
[^13]: Diferencial aproximado: a Selic de fechamento da central (13,43 e 12,10) menos o Fed Funds efetivo do caminho do agente externo (4,13 no 4T26 e 3,88 no 1T28, P2); na pausa, 13,75 menos 4,13.
