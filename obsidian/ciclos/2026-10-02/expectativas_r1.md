# Report — expectativas · ciclo 2026-10-02 · rodada 1

Dados até: 02/10/2026, com a argumentação limitada ao que estava divulgado nessa data (a última Focus divulgada era a de 28/09, com respostas coletadas até 25/09)[^corte] · Horizontes: 4T26 a 1T28, a Focus IPCA 12 meses à frente (suavizada, base de 30 dias, mediana) como **média das pesquisas do trimestre**

## 1. Tese

| Variável | Trimestre | Central | Base: faixa · P | Upside: limite · P | Downside: limite · P | P(up) − P(down) |
|---|---|---|---|---|---|---|
| Focus IPCA 12m, média do trimestre (% a.a.) | 4T26 | 4,16 | 4,10 a 4,45 · 31% | acima de 4,45 · 68% | abaixo de 4,10 · 1% | +0,67 |
| | 1T27 | 3,97 | 3,90 a 4,25 · 30% | acima de 4,25 · 61% | abaixo de 3,90 · 9% | +0,52 |
| | 2T27 | 3,78 | 3,70 a 4,05 · 28% | acima de 4,05 · 60% | abaixo de 3,70 · 12% | +0,48 |
| | 3T27 | 3,67 | 3,60 a 4,00 · 25% | acima de 4,00 · 54% | abaixo de 3,60 · 21% | +0,33 |
| | 4T27 | 3,59 | 3,50 a 3,90 · 26% | acima de 3,90 · 49% | abaixo de 3,50 · 25% | +0,24 |
| | 1T28 | 3,52 | 3,45 a 3,85 · 16% | acima de 3,85 · 47% | abaixo de 3,45 · 37% | +0,10 |

**A tese em uma frase:** a expectativa de 12 meses cai ao longo dos seis trimestres no modelo, de 4,16% no 4T26 para 3,52% no 1T28, puxada pela meta e pela inflação de 12 meses que recua, mas a própria pesquisa implica hoje um caminho entre 0,2 e 0,4 p.p. acima desse em todo o horizonte, e por isso a cauda de cima (uma expectativa que desce mais devagar e fica longe da meta, o que é ruim para o Brasil) é a mais provável em todos os trimestres, com mais força no curto prazo.

- **Upside (acima da faixa):** no modelo, uma âncora mais fraca (inércia da expectativa × 1,15 e peso da inflação de 12 meses × 1,30, os dois dentro do intervalo de 90% do posterior) leva a expectativa a 4,39 no 4T26 e 3,97 no 1T28; com as commodities agrícolas em dólar 15% acima do padrão (condição fora da tutela deste agente), a 4,45 e 4,10. O tempero (ii) do ponto de partida soma +0,16 p.p. no 4T26, e o tempero (ii) do choque de alimentos e da curva leva o 4T26 e o 1T27 acima do limite da faixa. É de-ancoragem para cima: ruim para o Brasil.
- **Downside (abaixo da faixa):** no modelo, uma âncora mais forte (inércia × 0,85, peso da inflação × 0,75, dentro do intervalo) leva a expectativa a 3,95 no 4T26 e 3,27 no 1T28; com as commodities agrícolas 10% abaixo do padrão, a 3,93 e 3,24. É convergência para a meta: bom para o Brasil, e não chega a ser de-ancoragem para baixo em nenhum trimestre (o piso do cenário fica acima de 3,00%). No 4T26 a cauda é quase vazia, porque a média do trimestre teria de ficar abaixo de 4,10 com a pesquisa em 4,65 no fim de setembro.

## 2. Argumentação

### Q1 — As expectativas estão ancoradas na meta?

Não estão, e a distância hoje é alta contra o histórico em todos os horizontes, inclusive nos longos. A Focus de 25/09 põe a inflação acima da meta de 3,00% em todo ano que a pesquisa pergunta, e de t+1 a t+3 a distância está no percentil 84 ou acima das leituras desde 2000[^pctl]:

| Horizonte | Focus, mediana (25/09) | Distância da meta (p.p.) | Pctl hist. | Pctl 10a | Δ 13 sem. da mediana (p.p.) |
|---|---|---|---|---|---|
| 12 meses à frente (a variável da tese) | 4,65 | +1,65 | 82 | 80 | +0,51 |
| 2026 (ano corrente) | 4,99 | +1,99 | 73 | 70 | −0,34 |
| 2027 (t+1) | 4,31 | +1,31 | 84 | 86 | +0,15 |
| 2028 (t+2) | 3,80 | +0,80 | 84 | 86 | +0,10 |
| 2029 (t+3) | 3,50 | +0,50 | 86 | 87 | 0,00 |
| 24 meses à frente (12 meses que começam daqui a um ano) | 3,93 | — | — | — | −0,02 |

Fontes: `expc_focus` (inflação) e `expc_focus_periodo` (inflação), 25/09 contra 26/06; percentis sobre todas as pesquisas até 25/09 e sobre os últimos 10 anos. O F, na pesquisa de 02/10, dá os mesmos números com diferença de até 3 pontos de percentil.

A ancoragem se julga em t+2 e t+3, e ali está o ponto. A mediana de 2029 está em 3,50 e a de 2030 também (`expc_focus_periodo` (inflação) · 25/09): a pesquisa não espera a inflação na meta em horizonte nenhum, e isso é uma âncora em 3,5%, não em 3,0%. Os horizontes longos **não estão se mexendo** (2029 sem variação em 13 semanas, 24 meses −0,02 p.p.), o que diz que a desancoragem não piorou no trimestre, mas também que ela não está sendo corrigida apesar de cinco cortes da Selic com a inflação acima da meta. O que se moveu foi o curto prazo: a expectativa de 12 meses subiu 0,51 p.p. em 13 semanas (de 4,14 em 26/06 para 4,65 em 25/09) enquanto 2028 subiu 0,10 e 2029 ficou parado, o desenho de um choque de curto prazo absorvido pelos horizontes curtos. A exceção, que impede ler o quadro como só choque, é serviços em 2028: +0,34 p.p. em 13 semanas, para 4,50 (`expc_focus_periodo` (inflação) · 25/09), o componente persistente revisado para cima no horizonte em que se julga a âncora.

### Q2 — O que move as expectativas, e é nível ou ruído?

A alta da expectativa de 12 meses desde julho é **revisão de nível dos trimestres próximos, e não a janela andando**. Compondo as medianas trimestrais da pesquisa[^comp], a janela de julho (3T26 a 2T27) dava 4,13% em 03/07 e a de setembro (4T26 a 3T27) dava 4,48% em 25/09; trocar o 3T26 pelo 3T27 com os outros trimestres fixos explica −0,04 p.p. dessa alta, e a revisão dos trimestres comuns explica +0,40 p.p.: o 4T26 subiu de 1,02% para 1,24% no trimestre e o 1T27 de 1,40% para 1,54% (`expc_focus_periodo` (inflação), trimestral, 03/07 e 25/09). Ao mesmo tempo o 3T26 foi revisto de 0,70% para 0,31%, o que explica a queda de 0,34 p.p. no ano de 2026: a pesquisa tirou inflação do trimestre que passou e pôs nos dois seguintes. Por isso a queda de 4,65 para 4,59 entre 25/09 e 02/10 (pesquisa divulgada só em 05/10) não é uma virada: com a entrada de outubro a janela de 12 meses perde peso de 2026 e ganha de 2027, e a pesquisa de 2026 e 2027 ficou parada nessa semana.

A revisão está concentrada nos componentes que a pesquisa costuma tratar como choque datado, e não no núcleo da inflação:

| Componente | 12m (25/09) | Δ 4 sem. | Δ 13 sem. | 24m (25/09) | Δ 13 sem. 24m | Ano 2028 (Δ 13 sem.) |
|---|---|---|---|---|---|---|
| IPCA | 4,65 | +0,11 | +0,51 | 3,93 | −0,02 | 3,80 (+0,10) |
| Alimentação no domicílio | 7,01 | +0,67 | +2,04 | 4,33 | −0,17 | 4,00 (0,00) |
| Administrados | 4,34 | +0,14 | +0,93 | 3,66 | +0,04 | 3,62 (+0,12) |
| Livres | 4,73 | +0,08 | +0,15 | 3,99 | −0,09 | 3,90 (+0,10) |
| Serviços | 5,16 | +0,04 | −0,11 | 4,78 | −0,03 | 4,50 (+0,34) |
| Bens industrializados | 2,68 | −0,09 | −0,21 | 2,76 | +0,07 | 2,80 (0,00) |

Fonte: `expc_focus` (inflação) e `expc_focus_periodo` (inflação), 25/09 contra 28/08 e 26/06.

Alimentação no domicílio carrega a revisão: +2,04 p.p. em 13 semanas a 12 meses, para um nível no percentil 99 da série, que começa em set/2021 (`expc_focus` (inflação) · 02/10, o percentil do F[^pctlcomp]), enquanto a 24 meses ela caiu 0,17 p.p. e o ano de 2028 ficou em 4,00. A pesquisa vê um choque de alimentos que volta depois de um 3T26 de deflação e passa em um ano, o que sustenta ler a alta do cheio como choque. Administrados vai no mesmo sentido (+0,93 a 12 meses, +0,04 a 24 meses). Serviços e bens industriais, os componentes de demanda, recuaram a 12 meses, **mas** serviços subiu 0,34 p.p. em 2028; se essa revisão se espalhar para 2029, hoje em 4,00 e parado, a leitura de choque datado deixa de valer.

A revisão é ampla na base de respostas e não de poucos respondentes. A base de 4 dias úteis, só com respostas frescas, estava 0,05 p.p. acima da de 30 dias a 12 meses em 25/09 (4,70 contra 4,65, 55 respondentes) e média e mediana coincidiam (4,65 e 4,65); a 24 meses as respostas frescas estavam abaixo (3,85 contra 3,93) (`expc_focus` (inflação) · 25/09)[^bases]. A dispersão a 12 meses, 0,48 de desvio-padrão, fica no percentil 76 da série (`expc_focus` (inflação) · 02/10): o painel discorda mais que o usual, sem uma cauda puxando a média.

O PIB esperado conta a mesma história pela demanda. Entre 26/06 e 25/09 a pesquisa cortou o consumo das famílias de 2026 em 0,55 p.p., para 1,45%, e o investimento de 2027 em 0,44 p.p., para 1,06%, enquanto subiu a agropecuária de 2026 em 0,70 p.p. (`expc_focus_periodo` (PIB) · 25/09). O crescimento que a pesquisa tira é o que pressiona preços, e o que ela põe é o que não pressiona: é coerente com serviços e bens industriais recuando a 12 meses, e contrário a uma desancoragem puxada por demanda. O hiato e a atividade em si são do agente de atividade (aguarda atividade, XS9).

O motor de fundo dessas revisões (a inflação de 12 meses e a composição dela) é do agente de inflação: aguarda inflação (XS5). Premissa usada aqui: a inflação de 12 meses sobe até o fim de 2026 e recua em 2027, que é o que o modelo produz (5,28% no 4T26, 4,08% no 1T28) e o que a projeção do Copom de 24/09 desenha (5,2% no 4T26, 3,9% no 4T27; `pm_copom_projecoes` · 24/09).

### Q3 — Onde a pesquisa, o mercado e o Copom divergem?

A curva cobra muito mais inflação que a pesquisa no curto prazo, e a distância diminui com o prazo. Lado a lado:

| Fonte | Horizonte | IPCA (%) | Data |
|---|---|---|---|
| Inflação implícita na curva, 1 ano[^impl] | próximos 12 meses | 6,94 | `br_interest_rate` · 02/10 |
| Focus | próximos 12 meses | 4,65 | `expc_focus` (inflação) · 25/09 |
| Inflação implícita a termo, 2º ano | 12 meses que começam daqui a um ano | 4,86 | `br_interest_rate` · 02/10 |
| Focus | 24 meses à frente (o mesmo 2º ano) | 3,93 | `expc_focus` (inflação) · 25/09 |
| QPC, mediana | 4 trimestres até 1T28 | 4,00 (p25 a p75: 3,77 a 4,20) | `expc_qpc` · 23/09 |
| Focus | ano de 2028 | 3,80 | `expc_focus_periodo` (inflação) · 25/09 |
| Copom, cenário de referência[^copom] | 4 trimestres até 1T28 | 3,2 | `pm_copom_projecoes` · 24/09 |
| Inflação implícita na curva, 5 e 10 anos | | 6,02 e 6,18 | `br_interest_rate` · 02/10 |

A implícita de 1 ano fica 2,29 p.p. acima da Focus de 12 meses e a do segundo ano a termo 0,93 p.p. acima da Focus de 24 meses. A implícita de 1 ano subiu de 5,05% em 02/07 para 6,28% em 02/09 e 6,94% em 02/10 (`br_interest_rate`), +1,88 p.p. em três meses (`br_interest_rate` · 02/10) contra +0,51 p.p. da Focus de 12 meses; a de 10 anos subiu 0,40 p.p. no mesmo período e só 0,02 no último mês (`br_interest_rate` · 02/10). O movimento está no vértice curto, que carrega pouco prêmio de prazo, e por isso a leitura mais provável é que o mercado está cobrando a mesma inflação de curto prazo que a pesquisa vê (alimentos e administrados), em tamanho maior, e não um prêmio fiscal, que apareceria primeiro nos vértices longos. **Mas** a NTN-B de 1 ano é pouco líquida e o seu juro real é afetado pelos meses de IPCA já conhecidos que ela carrega, então parte da distância pode ser liquidez; o que desfaria a leitura seria a implícita de 5 e 10 anos subir junto com a de 1 ano. A implícita no percentil 91 da série a 1 ano e 86 a 10 anos (`br_interest_rate` · 02/10), contra o percentil 82 da distância da Focus de 12 meses, diz que o mercado está mais alarmado que o painel.

Entre os três que olham o horizonte relevante do Copom, a ordem é Copom 3,2% < Focus 2028 3,80% < QPC 4,00%. O Copom projeta a meta quase atingida no 1T28, com a Selic da Focus como premissa, enquanto os analistas, perguntados sobre a mesma Selic na mesma semana, põem a inflação 0,8 p.p. acima no QPC e 0,6 p.p. acima na Focus de 2028 (`xp_condicoes`). A projeção do Copom é condicional e não é a previsão dele; ainda assim, a distância diz que o painel não compra o caminho de convergência que a política descrita pela própria pesquisa produziria no modelo do BC. O que o Copom disse das expectativas na reunião de setembro é do agente de política monetária: aguarda PM (XS2).

**A pesquisa contra ela mesma.** A Focus de 25/09 espera Selic de 13,50% no fim de 2026, 12,00% em 2027, 10,50% em 2028 e 10,00% em 2029, com IPCA de 4,99%, 4,31%, 3,80% e 3,50% (`expc_focus_periodo` (Selic e inflação) · 25/09). O juro real que isso implica cai de 8,10% para 7,37%, 6,45% e 6,28% (conta da pesquisa, não taxa de mercado), e fica acima do juro real neutro que os mesmos analistas declararam no QPC de junho, 6,00% a dois anos e 5,50% a cinco (`expc_qpc` · 24/06). Os analistas esperam juro real acima do neutro por mais de três anos e, mesmo assim, inflação parada em 3,5% e não em 3,0%. Ou eles acham que o neutro é mais alto que o que declararam, ou não acreditam que o Copom manterá a restrição até a meta: nos dois casos é uma dúvida de credibilidade, porque a política que eles próprios esperam não leva a inflação à meta. Qual das duas é a função de reação do Copom é do agente de política monetária: aguarda PM (XS1).

Há uma divergência dentro da própria pesquisa sobre a próxima reunião. A Focus de 25/09 espera corte para 13,50% em novembro (`expc_focus_copom` · 25/09), enquanto no QPC de 23/09 a resposta mais frequente para a reunião 282 era manter (53% dos respondentes, média de −12 p.b.; `expc_qpc` · 23/09). É o agente de política monetária quem lê isso contra a curva (XS4); aqui ela entra só como sinal de que o painel não está seguro de que o ciclo de cortes continua, o que, com a inflação esperada acima da meta, seria um bom sinal para a credibilidade.

### Q4 — O cenário para a expectativa de 12 meses

**Por que a central.** O modelo derruba a expectativa de 4,37% (média do 3T26) para 4,16% no 4T26 e 3,52% no 1T28, e o motor é a meta. Na equação (E), em cada trimestre a expectativa é 0,58 vezes a do trimestre anterior, mais 0,16 vezes a inflação de 12 meses, mais 0,26 vezes a meta de 3,00%. No 4T26 as três parcelas valem 2,54 (a inércia), 0,85 (a inflação de 12 meses a 5,28%) e 0,77 (a meta) (`xp_decomp_E`, cenário base). A inflação de 12 meses do modelo sobe no 4T26 e cai depois, mas mesmo com ela a 5,28% a expectativa cai, porque a meta pesa 0,26 a cada trimestre e a expectativa de partida está acima do ponto de repouso: com a inflação de 12 meses do 1T28 (4,08%), o repouso da equação é 3,42%. Nenhuma exógena deste agente entra; a meta está em 3,00% em todo o horizonte, no padrão do simulador (o caminho é do agente de política monetária, XS3).

**O que o modelo erra, e por quê.** Ele erra em dois pontos, os dois medidos.

O primeiro é o ponto de partida. A equação lê a média do 3T26, 4,37%, mas a pesquisa terminou o trimestre em 4,65% (25/09, a última divulgada em 02/10), porque subiu durante todo o trimestre. A diferença, 0,28 p.p., multiplicada pela inércia, deixa o 4T26 do modelo 0,16 p.p. abaixo do que a mesma equação daria partindo do nível do fim do trimestre (`xp_decomp_E`). Para a média do 4T26 ficar em 4,16, ela teria de ficar 0,48 p.p. abaixo da leitura de 25/09 (`xp_condicoes`): nos últimos 10 anos, uma média de trimestre 0,45 p.p. ou mais abaixo da última leitura do trimestre anterior aconteceu em 3% dos trimestres, e desde 2002 em 5% (`xp_calibracao`).

O segundo é a força da âncora. A pesquisa já diz qual caminho ela espera se ninguém revisar nada: compondo as medianas trimestrais e anuais de 25/09, a expectativa de 12 meses passa de 4,56% no 4T26 a 4,36% no 1T27, 4,17% no 2T27, 4,02% no 3T27, 3,86% no 4T27 e 3,73% no 1T28 (`xp_distribuicao_r1`, uma aproximação[^comp]). O modelo fica entre 0,21 e 0,40 p.p. abaixo desse caminho em todos os trimestres (`xp_condicoes`): ele põe a expectativa caminhando para 3,0%, e a pesquisa a põe caminhando para 3,5%. Como a âncora da (E) é imposta e não estimada, essa diferença só entra pelos multiplicadores (seção 3.2).

**Por que a distribuição.** A faixa base de cada trimestre contém a central do modelo, mas a distribuição está centrada no caminho que a pesquisa implica, com a dispersão histórica da variável nos últimos 10 anos (`xp_distribuicao_r1`). Por isso a central do modelo cai no percentil 3 da distribuição no 4T26, 13 no 1T27, 16 no 2T27, 31 no 3T27 e no 4T27 e 41 no 1T28, e a assimetria é positiva em todos os trimestres, maior no começo. Sobre essa base, o tempero (ii) desloca de 3 a 4 pontos para cima no 4T26, no 1T27 e no 2T27 (alimentos a 12 meses no topo da série, respostas frescas acima da mediana, a curva cobrando mais que a pesquisa), e quase nada nos três últimos, onde a pesquisa longa não se moveu. A cauda de baixo cresce com o horizonte porque a dispersão histórica da variável cresce com ele, e porque a Selic real acima do neutro que a pesquisa espera é a força que traria a expectativa para a meta, se o Copom a mantiver.

**O que a tese implica para a Selic, como fato do modelo.** A regra de juros reage ao desvio da expectativa contra a meta. Com a central, a Selic média do modelo vai de 13,60% no 4T26 a 12,27% no 1T28; com a âncora mais fraca do upside, a 13,67% e 12,98%; com a mais forte do downside, a 13,54% e 11,80% (`xp_cenarios_r1`). Não é uma posição sobre a Selic, que é do agente de política monetária.

### Olhado, sem sinal

- Câmbio esperado pela pesquisa · 5,20 no fim de 2026, 5,28 em 2027 (`expc_focus_periodo` (câmbio) · 02/10), sem variação em 4 semanas · a pesquisa não revisou o câmbio enquanto revisou a inflação, então o câmbio não é o que move as expectativas neste ciclo · diria algo se o câmbio esperado subisse junto com administrados e bens industriais.
- PTAX · 5,2238, +1,9% em um mês (`cmb_ptax` · 02/10) · a depreciação do mês não aparece em bens industriais a 12 meses, que caíram (−0,09 p.p. em 4 semanas até 25/09) · diria algo se bens industriais revisassem para cima; se ela é persistente é do agente de câmbio (XS7).
- CDS 5 anos · 131 p.b., +10 em um mês (`cmb_risco_pais` · 02/10) · baixo, e os vértices longos da implícita quase não se mexeram no mês · diria algo se o CDS subisse com a implícita de 10 anos e a Focus de 2029 juntas (aguarda fiscal, XS8).
- QPC, balanço de riscos · 60% veem risco de alta para o IPCA de 2027 e 5% de baixa; para 2026, 33% e 6% (`expc_qpc` · 23/09) · aponta para o mesmo lado da assimetria, mas é uma pergunta sem histórico no F para dizer se 60% é muito · diria algo comparado com as reuniões anteriores.
- IPCA mensal esperado para setembro · 0,56% na Focus (25/09) e no QPC (23/09) · é a referência da surpresa do próximo IPCA, que saiu depois do corte (09/10) e não entra aqui · diria algo na rodada 2, pelo agente de inflação (XS6).
- Inflação implícita de 2 e 5 anos · 5,89% e 6,02% (`br_interest_rate` · 02/10) · coerentes com a leitura de 1 e 10 anos acima, sem informação própria · diriam algo se se descolassem dos vértices vizinhos.

## 3. Premissas

### 3.1 Etapa 1 — o modelo

**Cenários.**
- Base: a inflação de 12 meses sobe até o fim de 2026 e recua em 2027, como o modelo a produz; o Copom segue a regra estimada; a meta fica em 3,00%; as exógenas no padrão do simulador (o último valor repetido).
- Upside: a pesquisa trata o choque de alimentos e administrados como mais persistente e a âncora fica mais fraca do que o histórico estimado (tempero (i)); como condição, as commodities agrícolas em dólar sobem 15%.
- Downside: a Selic real alta que a própria pesquisa espera leva a expectativa à meta mais depressa que o histórico (tempero (i) com a âncora mais forte); como condição, as commodities agrícolas em dólar caem 10%.

**Caminhos das exógenas.** Este agente não tem tutela de nenhuma exógena (aba "Exógenas") e não escreve caminho: na rodada 1 vale o padrão do simulador. A única exógena que a (E) lê é a meta:

| Exógena | Hoje (valor · tabela · data) | Cenário | 4T26 | 1T27 | 2T27 | 3T27 | 4T27 | 1T28 |
|---|---|---|---|---|---|---|---|---|
| Meta de 12 meses (`meta_12m`) | 3,00 · `inflc_meta` · 2026 | base · upside · downside | 3,00 | 3,00 | 3,00 | 3,00 | 3,00 | 3,00 |

Status: aguarda PM (XS3). Condições de cauda fora da tutela, só no report e não no JSON: IC-Br agropecuária em dólar (`icbr_agr_usd`) em 230,6 a partir do 4T26 no upside (+15,0% sobre 200,53 do 3T26) e em 180,5 no downside (−10,0%), do agente externo (XS10); um CDS de 200 p.b. foi medido e move a expectativa em no máximo 0,05 p.p. (`xp_cenarios_r1`), e por isso não entra em cauda nenhuma.

**Saída do modelo** (`xp_cenarios_r1`; central com os pesos da mediana; a faixa entre colchetes é o intervalo de 90% dos pesos, não de previsão):

| Variável | Cenário | 4T26 | 1T27 | 2T27 | 3T27 | 4T27 | 1T28 |
|---|---|---|---|---|---|---|---|
| Focus 12m, média do trimestre | base | 4,16 [4,06; 4,27] | 3,97 [3,82; 4,14] | 3,78 [3,61; 3,98] | 3,67 [3,51; 3,87] | 3,59 [3,43; 3,79] | 3,52 [3,36; 3,72] |
| | upside: e1 × 1,15, e2 × 1,30 | 4,39 | 4,33 | 4,18 | 4,10 | 4,04 | 3,97 |
| | upside com agro +15% | 4,45 | 4,43 | 4,33 | 4,28 | 4,19 | 4,10 |
| | downside: e1 × 0,85, e2 × 0,75 | 3,95 | 3,69 | 3,49 | 3,39 | 3,32 | 3,27 |
| | downside com agro −10% | 3,93 | 3,65 | 3,44 | 3,33 | 3,28 | 3,24 |
| IPCA 12m | base | 5,28 | 4,85 | 4,33 | 4,34 | 4,23 | 4,08 |
| | upside com agro +15% | 5,55 | 5,21 | 4,77 | 4,86 | 4,58 | 4,44 |
| | downside com agro −10% | 5,07 | 4,58 | 4,00 | 3,95 | 3,99 | 3,85 |
| Selic, média do trimestre | base | 13,60 | 13,26 | 12,96 | 12,70 | 12,47 | 12,27 |
| | upside com agro +15% | 13,69 | 13,50 | 13,40 | 13,35 | 13,30 | 13,23 |
| | downside com agro −10% | 13,53 | 13,07 | 12,65 | 12,27 | 11,96 | 11,72 |

Partida do modelo (3T26 observado): Focus 12m 4,37, IPCA 12m 4,58, Selic média 14,06, hiato 0,41. Sem dado de 3T26 da volatilidade implícita do dólar, segurada em 12,19 (2T26).

### 3.2 Etapa 2 — o tempero qualitativo

**(i) Âncora mais fraca — inércia e peso da inflação maiores que o estimado** · cenário upside
- Coeficientes: `E.e1` estimado 0,581, intervalo de 90% de 0,452 a 0,710; × 1,15 = 0,668, dentro (percentil 86). `E.e2` estimado 0,162, intervalo de 0,109 a 0,216; × 1,30 = 0,210, dentro (percentil 94). O peso da meta cai de 0,26 para 0,12 (`xp_condicoes`).
- Efeito: a expectativa no modelo passa de 4,16 → 4,39 no 4T26 e de 3,52 → 3,97 no 1T28 (+0,23 a +0,45 p.p.).
- Por quê: a pesquisa não espera a meta em ano nenhum (2029 e 2030 em 3,50) e a do modelo converge para ela; os horizontes longos não cederam em 13 semanas apesar dos cortes; serviços em 2028 subiu 0,34 p.p.; e a mesma forma da (E) estimada por MQO com a média de trimestre como defasagem dá inércia de 0,76 e peso da meta de 0,14, acima e abaixo do posterior do modelo (`xp_teste_defasagem`, seção 6). Com os multiplicadores, o upside do modelo reproduz o caminho que a pesquisa implica do 1T27 ao 2T27 (4,33 e 4,18 contra 4,36 e 4,17).
- Onde entra: limite e probabilidade da cauda de cima, e a assimetria de todos os trimestres.
- Checkpoints: as Focus de 2029 e serviços de 2028–2029, semana a semana; a próxima reunião do Copom (04/11).

**(i) Âncora mais forte — inércia e peso da inflação menores que o estimado** · cenário downside
- Coeficientes: `E.e1` × 0,85 = 0,494 (percentil 13, dentro); `E.e2` × 0,75 = 0,121 (percentil 11, dentro). O peso da meta sobe para 0,39 (`xp_condicoes`).
- Efeito: 4,16 → 3,95 no 4T26 e 3,52 → 3,27 no 1T28.
- Por quê: a pesquisa espera juro real acima do neutro declarado até 2029, que é a política que traria a expectativa para a meta se o Copom a mantiver; e a revisão recente está nos componentes datados (alimentos a 24 meses já em queda). É a cauda menos provável porque o painel, com a mesma Selic, ainda põe 2029 em 3,50.
- Onde entra: limite e probabilidade da cauda de baixo.
- Checkpoints: Focus de 2028 e 2029 abaixo de 3,50 · o Copom de 04/11.

**(ii) O ponto de partida pela média do trimestre — Focus 12m, última leitura contra a média do 3T26** · cenário base
- Hoje: 4,65 em 25/09 contra a média do 3T26 de 4,37 (`expc_focus` (inflação)).
- Por que o modelo não vê: a (E) lê a média do trimestre anterior; quando a pesquisa sobe dentro do trimestre, a média carrega o atraso para o seguinte.
- Efeito: +0,16 p.p. sobre o modelo no 4T26, +0,09 no 1T27, +0,05 no 2T27, apagando-se pela inércia (`xp_decomp_E`).
- Onde entra: assimetria do cenário base (não move a central).

**(ii) Choque de alimentos e a curva à frente da pesquisa — Focus de alimentação no domicílio a 12 meses e implícita de 1 ano** · cenário base e upside
- Hoje: alimentação no domicílio a 12 meses em 7,01 (+2,04 p.p. em 13 semanas, `expc_focus` (inflação) · 25/09), percentil 99 desde 2021; implícita de 1 ano em 6,94 (`br_interest_rate` · 02/10), 2,29 p.p. acima da Focus; respostas frescas 0,05 p.p. acima da mediana.
- Por que o modelo não vê: a (E) lê o IPCA cheio de 12 meses realizado, e não o choque que a pesquisa já põe nos próximos trimestres, nem o preço da curva.
- Efeito: para cima, 3 a 4 pontos de probabilidade da faixa para a cauda de cima no 4T26, 1T27 e 2T27; nada depois do 2T27.
- Onde entra: probabilidade da cauda de cima.

### 3.3 Da etapa 1 à tese

| Trimestre | Central (modelo, base) | Upside: modelo → com tempero | Downside: modelo → com tempero |
|---|---|---|---|
| 4T26 | 4,16 | 4,45 → 4,45 + 0,16 da partida, e o choque de alimentos para cima | 3,93 → 3,93 + 0,16 da partida |
| 1T27 | 3,97 | 4,43 → 4,43 + 0,09 da partida, e o choque de alimentos para cima | 3,65 → 3,65 + 0,09 da partida |
| 2T27 | 3,78 | 4,33 → 4,33 + 0,05 da partida, e o choque de alimentos para cima | 3,44 → 3,44 + 0,05 da partida |
| 3T27 | 3,67 | 4,28 → sem tempero (ii) | 3,33 → sem tempero (ii) |
| 4T27 | 3,59 | 4,19 → sem tempero (ii) | 3,28 → sem tempero (ii) |
| 1T28 | 3,52 | 4,10 → sem tempero (ii) | 3,24 → sem tempero (ii) |

A faixa base de cada trimestre vai da central do modelo menos um pouco até perto do caminho que a pesquisa implica, e as probabilidades saem da distribuição histórica centrada nesse caminho (`xp_distribuicao_r1`: 36/64/0 no 4T26, 32/58/11 no 1T27, 30/57/14 no 2T27, 25/53/22 no 3T27, 26/49/26 no 4T27, 15/47/38 no 1T28, faixa/acima/abaixo), com os temperos (ii) deslocando 3 a 4 pontos para a cauda de cima nos três primeiros trimestres (no 4T26, mais 1 ponto para a de baixo, que o histórico deixava vazia) e arredondamentos de 1 ponto nos demais.

## 4. Para os outros agentes

**Respostas às entradas (Parte 4 do mapa).**
- XE1 (câmbio, consenso): a pesquisa de 02/10 espera R$ 5,20 no fim de 2026, 5,28 em 2027, 5,30 em 2028 e 5,33 em 2029, sem revisão relevante em 4 semanas; IPCA de 4,99% e 4,31% e Selic de 13,50% e 12,00% em 2026 e 2027 (25/09). A pesquisa não revisou o câmbio na direção da depreciação de setembro.
- XE2 (política monetária, ancoragem), **em destaque**: a tese da seção 1 por trimestre, com a central do modelo abaixo do caminho que a própria pesquisa implica em 0,21 a 0,40 p.p. e a cauda de cima mais provável em todos os trimestres. Longos parados em 3,50% (2029 e 2030), não na meta; desancoragem alta contra o histórico (percentis 84–87 de t+1 a t+3), mas sem piora no trimestre; a alta recente é curto prazo e concentrada em alimentos e administrados.
- XE3 (inflação, expectativa e ancoragem): a mesma resposta do XE2.
- XE4 (inflação, componentes), **em destaque**: alimentação no domicílio a 12 meses subiu 2,04 p.p. em 13 semanas (7,01%) com o cheio subindo 0,51; serviços caiu a 12 meses (−0,11) mas subiu 0,34 p.p. em 2028, para 4,50%; administrados +0,93 a 12 meses e +0,04 a 24. O mercado espera alimentos e administrados acima do cheio no próximo ano e serviços acima no longo prazo.
- XE5 (atividade, consenso): PIB de 1,86% em 2026 e 1,41% em 2027 (25/09), cortados em 0,13 e 0,27 p.p. em 13 semanas; o corte está no consumo das famílias (−0,55 em 2026) e no investimento (−0,44 em 2027), com a agropecuária de 2026 revisada +0,70. QPC: hiato de 0,20 no 4T26 e −0,20 no 4T27 (23/09). O corte de desemprego não está na lista deste agente.
- XE6 (atividade, estruturais): fora da lista deste agente; o neutro do QPC de junho é 6,00% a dois anos e 5,50% a cinco, contra 5,50% e 5,00% na pergunta anterior (`expc_qpc` · 24/06).
- XE7 (fiscal, consenso): consumo do governo de 2,15% em 2026 e 1,30% em 2027 (25/09), estável; os cortes fiscais da Focus não estão nesta lista.
- XE8 (fiscal, longos e notícia fiscal): a Focus de 2029 não se mexeu em 13 semanas e a implícita de 10 anos subiu 0,02 p.p. no mês até 02/10; não há sinal de desancoragem longa por notícia fiscal neste ciclo.
- XE9 (externo): câmbio esperado estável; os componentes que as commodities alcançam primeiro (alimentos, administrados) são exatamente os que subiram a 12 meses. O bloco externo do QPC não está nesta lista; no QPC de 23/09, 67% acham o ambiente externo menos favorável.

**Pedidos.**
- XS1 (PM): o Copom reage a uma expectativa de 12 meses que fica 0,4 p.p. acima do caminho do modelo, com os longos em 3,5%, ou segue cortando? A probabilidade da cauda de cima e o tempero (i) de âncora fraca dependem disso.
- XS2 (PM): na reunião de setembro, que horizonte o Copom disse acompanhar, e ele chamou as expectativas de desancoradas? A leitura de credibilidade da Q3 depende disso.
- XS3 (PM): o caminho de `meta_12m` fica em 3,00% em todo o horizonte, e há risco de mudança? É o repouso da (E) e da central.
- XS4 (PM): quanto a curva cobra de Selic contra a Focus (13,50% em novembro) e contra o QPC (manutenção modal na reunião 282)? É o teste de coerência da Q3.
- XS5 (inflação): o caminho trimestral da inflação de 12 meses e a sua composição, e se o choque de alimentos do 4T26–1T27 é datado ou persistente. A leitura de choque da Q1–Q2 e a cauda de cima dependem disso.
- XS6 (inflação): o IPCA de setembro (divulgado em 09/10) contra 0,56% esperado pela Focus e pelo QPC, e os componentes; a rodada 2 usa a surpresa para rever a assimetria do 4T26 e do 1T27.
- XS7 (câmbio): a depreciação de 1,9% no mês até 02/10 é persistente e idiossincrática? A cauda de cima longa depende disso.
- XS8 (fiscal): o arcabouço está sob estresse neste ciclo? A leitura de que a curva não está cobrando prêmio fiscal depende disso.
- XS9 (atividade): o hiato do modelo vai de 0,41 no 3T26 a −0,51 no 1T28; a demanda ainda pressiona serviços? A cauda de baixo depende disso.
- XS10 (externo): o caminho das commodities agrícolas em dólar no 4T26–2T27, e se o choque é persistente. As condições de cauda (+15% e −10%) estão no lugar do caminho dele.

## 5. Placar

Primeiro ciclo.

## 6. Sobre o modelo

| Fonte | O que sugere (regressor, defasagem, quebra, âncora) | Teste proposto (dado, amostra, que resultado mudaria a especificação) | Por que importa para a tese deste ciclo |
|---|---|---|---|
| Os dados deste ciclo (`xp_teste_defasagem`), sem literatura | Na (E), trocar a defasagem "média do trimestre anterior" pela **última leitura do trimestre anterior**. Na forma restrita da (E), por MQO de 2004T1 a 2026T2 (90 trimestres), a troca reduz o erro médio quadrático de 0,31 para 0,19 p.p. (0,32 para 0,20 desde 2016), e o peso da meta cai de 0,14 para 0,05 | Reestimar a (E) bayesiana com as duas defasagens e comparar o ajuste de um passo dentro e fora da amostra; se a última leitura vencer, ela entra como regressor (ou o dado de partida do simulador passa a ser o fim do trimestre). Se o peso da meta cair como no MQO, a âncora imposta hoje é forte demais | A central do 4T26 depende disso em 0,16 p.p. só pela partida, e a distância de 0,2 a 0,4 p.p. entre o modelo e o caminho da pesquisa em todo o horizonte é, em boa parte, o peso da meta |

[^corte]: A pesquisa Focus é divulgada às segundas com as respostas coletadas até a sexta anterior: em 02/10 a última divulgada era a de 28/09, com coleta até 25/09. Por isso os números da Focus neste report são de 25/09, salvo quando dito. Os dados posteriores ao corte que o modelo usa no ponto de partida (o IPCA de setembro, divulgado em 09/10, e as pesquisas de 28 a 30/09 dentro da média do 3T26) não puderam ser separados e estão declarados no registro do ciclo.
[^pctl]: Percentil: a posição da leitura de hoje entre todas as leituras da série, de 0 (a menor) a 100 (a maior). Aqui, quanto maior o percentil, mais longe da meta a pesquisa está em relação ao histórico: 84 quer dizer que só 16% das pesquisas desde 2000 estiveram mais longe da meta naquele horizonte.
[^pctlcomp]: Neste caso o percentil é do nível da expectativa de alimentos, e não da distância da meta, e a série só começa em set/2021, quando o Banco Central passou a perguntar pelos componentes: 99 quer dizer que a pesquisa nunca esperou alimentos tão altos desde então.
[^comp]: A Focus pergunta a inflação de cada trimestre e de cada ano. Multiplicando as medianas de quatro trimestres seguidos tem-se uma aproximação da inflação de 12 meses que a pesquisa espera para aquela janela; é aproximação porque a combinação das medianas não é a mediana das combinações, e a série suavizada do Banco Central usa outro método (ficou 0,17 p.p. acima da composição em 25/09).
[^bases]: A Focus é a pesquisa semanal do Banco Central com cerca de 130 instituições sobre inflação, PIB, Selic e câmbio. A "base de 30 dias" usa a resposta mais recente de cada instituição no último mês; a "base de 4 dias úteis" só conta quem respondeu nos últimos quatro dias úteis, e mostra antes da mediana uma revisão que está começando.
[^impl]: A inflação implícita é a que se tira dos títulos: o juro prefixado dividido pelo juro real da NTN-B do mesmo prazo. É um preço, não uma pesquisa: além da inflação esperada, carrega o prêmio que o investidor cobra pelo risco de inflação e efeitos de liquidez. A termo do 2º ano é a inflação que a curva cobra para os 12 meses que começam daqui a um ano.
[^copom]: O Questionário Pré-Copom (QPC) é a pesquisa que o Banco Central faz com os analistas antes de cada reunião do Copom. A projeção do Copom no cenário de referência usa a Selic da Focus como premissa: diz para onde a inflação iria com aquela Selic no modelo do Banco Central, e não é a previsão do Copom.
