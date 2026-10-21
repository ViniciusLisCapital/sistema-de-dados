# Report — política monetária · ciclo 2026-10-15 · rodada 1

Dados até: 15/10/2026 (F fixo do ciclo) · Horizontes: 4T26 a 1T28, a meta Selic no fechamento de cada trimestre (a decisão da última reunião dentro dele); 4T26 e 1T27 também reunião a reunião.

## 1. Tese

| Variável | Trimestre | Central[^1] | Base: faixa · P | Cauda worst: limite · P | Cauda best: limite · P | Pbc − Pwc |
|---|---|---|---|---|---|---|
| Meta Selic, fechamento do trimestre (% a.a.) | 4T26 | 12,47 | 12,25 a 12,75 · 5% | acima de 12,75 · 95% | abaixo de 12,25 · 0% | −0,95 |
| | 1T27 | 12,13 | 11,75 a 12,50 · 21% | acima de 12,50 · 79% | abaixo de 11,75 · 0% | −0,79 |
| | 2T27 | 11,85 | 11,50 a 12,25 · 35% | acima de 12,25 · 61% | abaixo de 11,50 · 4% | −0,57 |
| | 3T27 | 11,61 | 11,25 a 12,00 · 38% | acima de 12,00 · 51% | abaixo de 11,25 · 11% | −0,40 |
| | 4T27 | 11,39 | 11,00 a 11,75 · 40% | acima de 11,75 · 44% | abaixo de 11,00 · 16% | −0,28 |
| | 1T28 | 11,20 | 10,75 a 11,75 · 52% | acima de 11,75 · 29% | abaixo de 10,75 · 19% | −0,10 |

Worst é a Selic acima da faixa (inflação, expectativas ou prêmio piores que no cenário base); best é abaixo. As probabilidades saem do caminho reunião a reunião abaixo, somado trimestre a trimestre[^2].

**Reunião a reunião, 4T26 e 1T27** (probabilidade de cada passo; soma 100% por reunião):

| Reunião (`pm_copom_calendario`) | +25 | manter | −25 | −50 | DI · Focus |
|---|---|---|---|---|---|
| 04/11/2026 | 0% | 25% | 65% | 10% | 13,57 · 13,50 |
| 09/12/2026 | 1% | 30% | 57% | 12% | 13,38 · 13,25 |
| 27/01/2027 | 1% | 31% | 55% | 13% | 13,18 · 13,25 |
| 17/03/2027 | 1% | 31% | 54% | 14% | 12,99 · 13,00 |

DI = Selic precificada na curva para a reunião (`br_di_grade` · 14/10); Focus = mediana por reunião (`expc_focus_copom` · 09/10). O fechamento do 4T26 que esse caminho dá: 13,25% com 44%, 13,50% com 26%, 13,75% com 13%, 13,00% com 11%, 12,75% com 5%, 14,00% com 1%. O do 1T27 tem mediana 13,00%, e 94% da massa entre 12,25% e 13,75%.

**O que leva a cada cauda:**
- **Worst (Selic acima de 12,75% no 4T26 … acima de 11,75% no 1T28).** Na maior parte da probabilidade, não é preciso cenário nenhum: é o Copom mantendo o passo de 25 p.b. com pausas enquanto o modelo passa a queda do juro real de 10 anos inteira para a Selic (tempero (ii), calibração gradual e calendário, que entra como assimetria). No cenário worst do modelo, o salto de 05/10 se desfaz (NTN-B 10 anos de volta a 7,84%–8,00%, CDS a 150): a Selic do modelo vai a 13,18% no 4T26 e 12,40% no 1T28; com a regra reagindo ao desvio das expectativas 1,3 vez o estimado (tempero (i)), a 13,34% e 12,79%; com o Brent perto de US$ 125 segurando uma pausa a mais (tempero (ii)), a 13,71% no 1T27.
- **Best (Selic abaixo de 12,25% no 4T26 … abaixo de 10,75% no 1T28).** A compressão continua (NTN-B 10 anos a 6,20%, CDS a 95): o modelo dá 12,16% no 4T26 e 10,51% no 1T28; com o Copom acelerando para 50 p.b. depois do pico do IPCA de 12 meses (tempero (i), inércia da regra × 0,95), 12,06% e 10,27%. No 4T26 essa cauda é remota: a Selic está em 13,75% até 04/11 e fechar abaixo de 12,25% exige cortar mais de 150 p.b. em duas reuniões.

**A tese em uma frase:** o Copom deve seguir cortando 25 p.b. por reunião, com pausas, e fechar 2026 em 13,25% e 2027 perto de 11,75% (medianas do caminho por reunião); o Modelo Estrutural, que leva a queda de 0,95 p.p. do juro real de 10 anos para a Selic no mesmo trimestre, dá 12,47% e 11,39%, e por isso o risco fica quase todo acima da central até o 2T27 e se equilibra no 1T28.

## 2. Argumentação

### Q1 — O que o Copom vai fazer

**Em 04/11, −25 p.b., para 13,50% (65%); manter tem 25% e −50, 10%.** O Copom cortou 25 p.b. nas cinco reuniões desde 18/03 (15,00% → 13,75%, `pm_copom_reuniao`), e desde a 279ª o comunicado repete que "a magnitude total do ciclo de calibração será estabelecida à luz de novas informações" (comunicado da 281ª, §6): um ciclo com fim, decidido passo a passo, num passo que não mudou. A reação à projeção sustenta a continuidade, porque a projeção no horizonte relevante[^3] ficou em 3,2% nas duas últimas reuniões (`pm_copom_projecoes` · 24/09), e o Copom julgou esse 3,2% "compatível com a estratégia de convergência da inflação para o redor da meta" ao cortar (ata da 281ª, §18). O tom da 281ª andou para o lado do corte: "desancoragem adicional" virou "desancoragem" e a atividade passou de "sugere uma moderação" a "mostra uma moderação gradual … principalmente em setores mais cíclicos" (comunicados da 280ª e da 281ª, §2 e §5).

Mas três coisas puxam para a pausa, e elas dão os 25% de manter. A projeção de 3,2% foi feita com a Selic da Focus de 11/09, que parava em 13,75% no fim de 2026 (RPM set/26, 2.2): o Copom chegou a 3,2% sem nenhum corte além de setembro. O IPCA de setembro veio 0,82% (`inflc_agregados` · set/26), 0,17 p.p. acima dos 0,65% que o RPM projetava para o mês (Tabela 2.1.2), e o de 12 meses, 4,58%, já está 0,08 p.p. acima do teto de 4,50%, a caminho dos 5,21% que o próprio Copom projeta para dezembro. E o Brent está em US$ 125,44 (`comm_brent` · 06/10), 39% acima dos ~US$ 90 de onde o cenário de referência partiu (RPM set/26, 2.2). O que impede essas três de virarem pausa em novembro é a regra que o Copom declarou para choques de oferta: não reagir aos efeitos primários e reagir com firmeza aos de segunda ordem (ata da 281ª, §16)[^4]; o petróleo e a energia elétrica são efeito primário, e o próprio RPM não viu, até setembro, propagação de segunda ordem relevante (boxe sobre efeitos de segunda ordem, conclusão).

**Em 09/12, −25 p.b. é o mais provável (57%), com 30% de pausa.** A pausa sobe em relação a novembro porque dezembro é o mês em que o IPCA de 12 meses chega ao pico projetado (5,21%, RPM, Tabela 2.1.2) e em que a mediana da Focus para 2026 subiu para 5,22% (+0,32 p.p. em 4 semanas, `expc_focus_periodo` · 09/10). O −50 (12%) existe porque, antes deste, todo ciclo de corte desde 2003 usou passos de 50 p.b. ou mais em boa parte das reuniões: 7 de 11 no de 2003, 13 de 18 no de 2005, 5 de 5 em 2009, 9 de 10 em 2011, 15 de 31 em 2016 e 6 de 7 em 2023; este é o primeiro com cinco cortes seguidos de 25 (`pm_copom_reuniao`, 2003–2026).

**No 1T27, −25 por reunião com 31% de pausa em cada uma; mediana de 13,00% em 17/03.** A Focus põe pausa em janeiro (13,25% em R1/2027) e corte em março (13,00%); o modelo de inflação do sistema dá o IPCA de 12 meses ainda em 4,84% no 1T27, acima do teto. A partir do 2T27, quando o modelo põe o IPCA de 12 meses de volta abaixo do teto (4,32%), o caminho admite mais −50 (17% a 18% por reunião).

### Q2 — O que o Copom deveria fazer, pelos dados

**Pelos dados, −25 em novembro e pausa em dezembro.** O critério é o da meta de inflação como meta para a projeção[^5]: o juro se põe onde a projeção no horizonte relevante volta à meta. A projeção do Copom foi 3,2%, 0,20 p.p. acima da meta, com uma Selic que não caía mais em 2026. Desde então a notícia líquida sobre essa projeção é de alta:
- **Inflação corrente e núcleo.** Serviços subjacentes acumulam 5,32% em 12 meses (`inflc_decomposicao` · set/26), 0,32 p.p. acima de três meses antes, o que mostra que o segmento mais sensível ao hiato e mais inercial (RPM set/26, 2.3) ainda não desacelerou. Os núcleos ficam entre 4,06% (dupla ponderação) e 4,85% (EX0) em 12 meses (`inflc_agregados` · set/26), todos acima da meta. Mas os industriais subjacentes caíram para 3,70% (−0,44 p.p. em três meses) e a difusão, 54,9% (`inflc_agregados` · set/26), não indica espalhamento novo.
- **Hiato.** A edição de set/26 revisou o hiato para cima em todos os trimestres desde o 2T25, de 0,10 a 0,15 p.p. (`pm_hiato_produto_vintages`), e o deixou em 0,41% no 3T26 (`pm_hiato_produto`): a economia estava mais aquecida do que o Copom pensava em tempo real[^6]. A atividade, porém, desacelera: IBC-Br −0,9% em três meses até jul/26 (`atv_ibcbr`), produção industrial −2,1% até ago/26 (`atv_pim`), varejo ampliado −0,9% (`atv_pmc`). O mercado de trabalho segue o contraponto: desocupação de 5,3% (`mt_pnad` · ago/26) e rendimento real +3,7% em 12 meses.
- **Expectativas.** A Focus para 2027 parou em 4,30% e para 2028 em 3,79% nas últimas quatro semanas (`expc_focus_periodo` · 09/10), 0,79 p.p. acima da meta em 2028, o horizonte que o RPM usa para julgar ancoragem (2.3). A desancoragem não piorou no mês, mas não recuou.
- **Petróleo.** O Brent a US$ 125 está fora do cenário de referência, que supunha queda depois do 4T26 até ~US$ 84 no 2T27 (RPM set/26, 2.2). Gasolina pesa 5,13% no IPCA (`inflc_decomposicao` · set/26) e o RPM estima que diesel, gasolina e gás de botijão somaram 0,42 p.p. ao IPCA de março e abril (boxe sobre efeitos primários).

Contra a pausa, e é por isso que novembro ainda leva corte: a postura é muito apertada. A Selic real ex-ante está em 8,88% (`br_interest_rate` com a Focus de 12 meses, 09/10), 3,88 p.p. acima do neutro de 5,00% que o Copom usa nas projeções (RPM set/26, 2.2)[^7]. Uso o neutro do Copom porque a pergunta é se a projeção dele volta à meta; contra os neutros do QPC (6,00% em 2 anos, 5,50% em 5 anos, `expc_qpc`, R279) a distância é de 2,9 a 3,4 p.p., e contra o juro real de 10 anos do modelo (6,87%, `br_interest_rate` · 15/10), de 2,0 p.p. Com qualquer dos três, um corte de 25 p.b. deixa a política contracionista. A transmissão também está passando: a inadimplência do crédito livre a pessoas físicas está em 8,01% (+1,04 p.p. em 12 meses, `cred_credito_resumo` · ago/26) e o comprometimento de renda em 28,72% (+1,40 p.p., `cred_credito_familias` · jul/26), o canal do balanço das famílias[^8]. Mas o crédito direcionado segue fora do alcance da Selic: imobiliário +13,8% e BNDES +10,3% em 12 meses (`cred_modalidade_direcionado_pf` e `_pj` · ago/26) contra +0,5% no livre a empresas (`cred_credito_resumo`), o que o Copom diz elevar o neutro (ata da 281ª, §6 e §8).

O que faria esta leitura mudar: um IPCA de outubro e novembro nos 0,34% e 0,32% da mediana do QPC (`expc_qpc`), com serviços subjacentes parando de subir, tira o argumento da pausa em dezembro; um repasse do Brent à gasolina antes de dezembro o reforça.

**A distância entre Q1 e Q2 é pequena e tem sinal:** o Copom que prevejo (13,25% no 4T26) corta 25 p.b. a mais do que os dados pedem (13,50%). Isso puxa a Selic para baixo agora, a cauda best do 4T26–1T27, e para cima depois, porque um corte antes da hora é o que obriga a parar mais cedo se os efeitos de segunda ordem aparecerem: é a razão das probabilidades de pausa de 31% a 39% por reunião ao longo de 2027 no caminho por reunião.

### Q3 — O que o mercado precifica, e onde diverge

| Fechamento do trimestre | Curva DI (`br_di_grade` · 14/10) | Focus (`expc_focus_copom` · 09/10) | Mediana do caminho por reunião (Q1) | Q2 | Central do modelo |
|---|---|---|---|---|---|
| 4T26 (09/12) | 13,38 | 13,25 | 13,25 | 13,50 | 12,47 |
| 1T27 (17/03) | 12,99 | 13,00 | 13,00 | — | 12,13 |
| 2T27 (16/06) | 12,58 | 12,62 | 12,50 | — | 11,85 |
| 3T27 (22/09) | 12,25 | 12,25 | 12,25 | — | 11,61 |
| 4T27 (08/12) | 12,13 | 12,00 | 11,75 | — | 11,39 |

- **O mercado e o Q1 quase coincidem até o 3T27.** A curva DI precifica −18 p.b. em novembro e −19 p.b. em dezembro (`br_di_grade` · 14/10): se só houvesse corte de 25 ou manutenção, seriam 72% e 76% de corte, contra 75% e 69% de corte (de 25 ou 50) no meu caminho. A curva e a Focus ficam a no máximo 16 p.b. uma da outra em todas as reuniões até dez/27, e por isso leio pouco prêmio a termo[^9] na parte curta hoje. No 4T27 o caminho por reunião (11,75%) fica abaixo do mercado (12,00% na Focus, 12,13% na curva), porque admite mais −50 depois que o IPCA de 12 meses volta para baixo do teto.
- **O mercado mudou em um pregão, e a Focus de 2027 não.** Há um mês a curva punha a Selic entre 13,59% e 13,76% em todas as reuniões até jun/27 (`br_di_grade` · 14/09), quase nenhum corte; a Selic precificada para dez/27 caiu 194 p.b. em um mês. A queda está quase toda em 05/10: o DI de 2 anos caiu 1,10 p.p. e a NTN-B de 10 anos 0,50 p.p. entre 02/10 e 05/10 (`br_interest_rate`), um recuo de 21 pregões que fica no percentil 2,5 dos recuos desde 2006[^10]. A mediana da Focus para o fim de 2027 está em 12,00% há 13 semanas (`expc_focus_periodo` · 09/10). A curva foi até a Focus, não o contrário[^11].
- **O mercado diverge do que o Copom sinalizou.** A projeção de 3,2% usou 13,75% no fim de 2026 (RPM set/26, 2.2); a curva e a Focus põem 38 a 50 p.b. de corte a mais em 2026. E o QPC respondido antes da 281ª dava pausa em 04/11 como a resposta mais frequente para o que o Copom faria (53%) e para o que deveria fazer (61%) (`expc_qpc` · R281)[^12]. O mercado pré-05/10 estava mais perto do meu Q2 do que o de hoje.
- **O mercado diverge do modelo em 61 a 91 p.b.** em todos os trimestres, sempre com o modelo abaixo. A razão está no Q4.
- **Espaço para surpresa em 04/11:** a manutenção tem 25% no meu caminho e ~28% no preço; um −50 (10%) não está no preço. Como, na evidência de Gürkaynak, Sack & Swanson, o que move os juros longos é a sinalização sobre o caminho e não a decisão do dia[^13], a frase sobre a "magnitude total do ciclo" no comunicado de 04/11 vale mais para a curva do que o passo.

### Q4 — Por que a central, e por que a distribuição

**A central é a do modelo no cenário base: os preços de 15/10 segurados.** A NTN-B de 10 anos fica em 6,87% (média do 4T26 de 6,89% se ela não sair dali; `br_interest_rate` · 15/10), o CDS em 112 (`cmb_risco_pais` · 14/10), a meta em 3,00%, o Fed Funds em 3,88% e depois 4,13% (o T-bill de 3 meses está 0,41 p.p. acima do ponto médio da meta, `us_interest_rate` · 15/10). Desses caminhos, só a NTN-B move a Selic do modelo: com o CDS em 131 em vez de 112, ou o Fed parado em 3,88%, a Selic de fechamento muda no máximo 0,02 p.p. em qualquer trimestre (saída do modelo, seção 3.1).

**A história econômica do corte do modelo.** A regra de juros do modelo ancora a Selic no juro real de 10 anos mais a meta (`rr_10a` + `meta_12m`). A NTN-B de 10 anos caiu de 7,84% na média do 3T26 para 6,87%; o modelo leva os 0,95 p.p. inteiros para a Selic média do 4T26 (13,60% sem caminho nenhum, 12,65% com a NTN-B de hoje). A leitura é a do mapa (2.5): quando o prêmio fiscal comprime, o mercado está precificando consolidação — gasto mais lento, menos demanda, menos inflação à frente —, e a mesma Selic fica mais apertada contra a demanda que vem; cortar devolve o aperto ao mesmo nível. Por isso o hiato projetado é praticamente o mesmo nos três cenários (0,13% no 4T26 a −0,51% no 1T28): o modelo move a Selic com o neutro para manter a postura.

**Onde eu discordo, em três partes.**
1. *O que caiu foi prêmio local, não risco soberano.* O CDS foi de 111,62 em 16/09 a 131,04 em 02/10 e voltou a 112,19 em 14/10 (`cmb_risco_pais`): o prêmio em dólar é o mesmo da última reunião. O que caiu depois de 02/10 foi o juro real de 10 anos (−0,64 p.p.) e a inflação implícita de 10 anos (−0,64 p.p., de 6,18% para 5,55%; `br_interest_rate`)[^14]. Isso é informação sobre credibilidade e prêmio a termo, mas não é ainda a consolidação fiscal que baixa o neutro com que o Copom projeta, e o Copom não revisa os 5,00% por um pregão (RPM set/26, 2.2). E o movimento já devolveu parte: o DI de 2 anos subiu 0,19 p.p. no pregão de 15/10 (`br_interest_rate`).
2. *A regra suaviza a distância entre a Selic e a âncora, não a Selic.* Por isso a queda da âncora passa inteira no mesmo trimestre. O Copom suaviza a própria Selic: cinco cortes iguais de 25 p.b. e um ciclo de "calibração". Nenhum multiplicador dentro do posterior fecha essa diferença: com 5% a mais de inércia na regra o fechamento do 4T26 vai só de 12,47% a 12,57%. Ela entra como tempero (ii).
3. *O calendário.* A Selic fica em 13,75% até 04/11, 35 dos 92 dias do trimestre; a média de 12,65% que o modelo dá ao 4T26 exigiria cortar perto de 150 p.b. em novembro e 100 em dezembro (a combinação −150/−100 dá média de 12,58%), passos que o Copom só deu em 2003 e 2009 (`pm_copom_reuniao`).

Há ainda uma tensão dentro do próprio modelo, que reforço como risco: o modelo corta a Selic para 11,20% no 1T28 com o IPCA de 12 meses em 4,07% no mesmo trimestre, contra 3,2% na projeção do Copom, porque a regra lê a Focus de 12 meses (3,51% no modelo) e não o IPCA.

**Por que a distribuição.** O caminho por reunião (Q1) põe a mediana 0,78 p.p. acima da central no 4T26, 0,87 no 1T27, ~0,65 no 2T27–3T27, 0,36 no 4T27 e 0,05 no 1T28. A cauda worst concentra a probabilidade no começo (95% no 4T26) e perde peso conforme as pausas do caminho e a regra do modelo convergem; no 1T28 o caminho e a central quase coincidem, e o Pbc − Pwc vai a −0,10. A cauda best só ganha massa a partir do 2T27, quando o −50 entra no caminho e o cenário best do modelo (12,16% a 10,51%) e o tempero (i) de menos inércia (até 10,27%) ficam abaixo da faixa. A distância Q1–Q2 alimenta a cauda best no 4T26–1T27 e a worst depois (Q2). A força qualitativa em que acredito no cenário base — o passo de 25 p.b. e o calendário — não move a central: está toda na assimetria.

### Outros pontos

- **O real e o Copom.** A PTAX de 5,0441 (`cmb_ptax` · 14/10) está 2,1% abaixo do R$ 5,15 do cenário de referência; o Copom lista o câmbio "persistentemente mais depreciado" como risco de alta (comunicado da 281ª, §4). Se a apreciação persiste, o risco do item (iii) recua e a pausa de dezembro perde força; não concluo sobre isso: **aguarda câmbio (S1, S4)**. Para os cenários, assumi a PTAX que o modelo resolve (5,18 no 4T26, base).
- **O Fed subiu e os juros longos lá fora subiram, e aqui caíram.** O Fed Funds foi a 3,88% (+0,25 em um mês) e o Treasury de 10 anos está em 5,10% (+0,55 p.p. em três meses, `us_interest_rate` · 15/10), contra a NTN-B de 10 anos −1,06 p.p. em três meses (`br_interest_rate`). O descolamento reforça que o movimento de outubro foi local; se a leitura local reverte, o juro global não ajuda a segurar a NTN-B. Global contra idiossincrático é do câmbio: **aguarda câmbio (S2)**.
- **Intervenção em setembro.** O BC vendeu US$ 2,0 bi à vista e US$ 2,0 bi em linhas em set/26, e as reservas caíram US$ 6,5 bi em um mês (`cmb_reservas_bc` · 14/10), no período em que a PTAX subiu de 5,15 para 5,22 (16/09 a 02/10, `cmb_ptax`). Se foi resposta a disfunção ou defesa do nível decide se E4 se amplia: **aguarda câmbio (S7)**.
- **Fiscal.** O primário de 12 meses está em −0,62% do PIB e a dívida bruta em 82,9% (+5,5 p.p. em 12 meses) (`fisc_nfsp`, `fisc_divida` · ago/26); o RPM registra o mercado projetando déficit em 2027 e dívida sem estabilizar (1.2, Fiscal). Nada nesses dados de agosto antecipa a compressão de outubro, e é por isso que trato a queda da NTN-B como premissa de preço, não como fato fiscal: até haver um agente fiscal, a pergunta "que consolidação o mercado precifica" fica aberta (seção 4).

**Olhado, sem sinal**
- Estoque de swaps · −US$ 91,6 bi (`cmb_reservas_bc` · ago/26) · nível, +1,3 no mês · diria algo se o BC ampliasse a oferta acima dos vencimentos.
- Posição dos fundos alavancados em BRL · 27.396 contratos, +11.350 em um mês (`cmb_cot_fx` · 06/10) · leitura de posicionamento é do câmbio · diria algo à PM se o câmbio a ligasse a carry (S6).
- Juros de política dos pares · México 6,50%, Chile 4,50% parados, Colômbia +0,25 (`inter_interest_rate` · 13/10) · nenhum par em ciclo comparável ao do Copom · diria algo se dois pares passassem a subir juros pelo petróleo.
- Poupança bruta · 14,4% do PIB, igual a um ano antes (`atv_renda_poupanca` · 2T26) · a alavanca estrutural do neutro (Segura-Ubiergo) não se moveu · diria algo com uma mudança de ~1 p.p. do PIB.
- Termos de troca · 111,35, −2,7% em três meses (`cmb_termos_troca` · jul/26) · dado de 106 dias · diria algo atualizado com o Brent de outubro.
- Pesquisa de condições de crédito · oferta PF consumo −0,23 (`cred_ptc` · 2T26) · dado de 197 dias · diria algo na leitura do 3T26.
- Índice de difusão · 54,9%, +2,7 p.p. em 12 meses (`inflc_agregados` · set/26) · dentro da faixa recente · diria algo acima de 60%.
- Saldo do CAGED na indústria de transformação · 15,9 mil em 12 meses contra 210,3 mil um ano antes (`mt_caged_setor` · ago/26) · confirma a desaceleração já lida na PIM · diria algo se ficasse negativo, sinal de hiato fechando mais rápido.

## 3. Premissas

### 3.1 Etapa 1 — o modelo

**Cenários.**
- **Base:** os preços de 15/10 ficam. A leitura de 05/10[^11] nem se confirma nem se desfaz; o Fed sobe mais uma vez (é o que o T-bill de 3 meses precifica); o dólar contra emergentes fica onde está.
- **Worst:** o salto de 05/10 se desfaz e o prêmio sobe além de onde estava em setembro: a NTN-B de 10 anos volta à média do 3T26 e vai a 8,00%, o CDS sobe a 150; o Fed sobe duas vezes; o dólar se fortalece contra emergentes.
- **Best:** a compressão continua, porque o mercado passa a precificar uma consolidação fiscal mais funda: NTN-B de 10 anos a 6,20%, CDS a 95; o Fed para em 3,88%.

**Caminhos das exógenas** (nível, unidade do simulador; um valor vale até o próximo):

| Exógena | Hoje (valor · tabela · data) | Cenário | 4T26 | 1T27 | 2T27 | 3T27 | 4T27 | 1T28 |
|---|---|---|---|---|---|---|---|---|
| Meta de inflação, 12 meses (`meta_12m`) | 3,00 · `inflc_meta` · 2026 | base · worst · best | 3,00 | 3,00 | 3,00 | 3,00 | 3,00 | 3,00 |
| Juro real de 10 anos, média do trimestre (`rr_10a`) | 6,87 · `br_interest_rate` · 15/10 (3T26: 7,84) | base | 6,89 | 6,87 | 6,87 | 6,87 | 6,87 | 6,87 |
| | | worst | 7,35 | 7,84 | 8,00 | 8,00 | 8,00 | 8,00 |
| | | best | 6,75 | 6,40 | 6,20 | 6,20 | 6,20 | 6,20 |
| CDS 5 anos, fechamento (`fiscal`) | 112 · `cmb_risco_pais` · 14/10 (3T26: 131) | base | 112 | 112 | 112 | 112 | 112 | 112 |
| | | worst | 131 | 150 | 150 | 150 | 150 | 150 |
| | | best | 105 | 95 | 95 | 95 | 95 | 95 |
| Fed Funds efetivo, último mês (`ffr`) | 3,75 · `diferenciais_juros` · set/26 (meta 3,88 · `us_interest_rate` · 15/10) | base | 3,88 | 4,13 | 4,13 | 4,13 | 4,13 | 4,13 |
| | | worst | 3,88 | 4,38 | 4,38 | 4,38 | 4,38 | 4,38 |
| | | best | 3,88 | 3,88 | 3,88 | 3,88 | 3,88 | 3,88 |
| Dólar contra emergentes, fechamento (`dxy_em`) | 129,77 · `cmb_dollar_index_em` · 09/10 | base | 129,77 | 129,77 | 129,77 | 129,77 | 129,77 | 129,77 |
| | | worst | 131,0 | 133,7 | 133,7 | 133,7 | 133,7 | 133,7 |
| | | best | 129,77 | 129,77 | 129,77 | 129,77 | 129,77 | 129,77 |

- A NTN-B de 10 anos do base fica plana porque a curva real é plana entre 2 e 10 anos (6,80% a 6,87%, `br_interest_rate` · 15/10): o mercado não precifica mudança do juro real longo à frente. No worst, 8,00% fica abaixo do máximo de 8,20% desde 2016.
- As exógenas que não fixo ficam no padrão do simulador (último valor repetido): volatilidade implícita do dólar (12,19, do 2T26, sem dado no 3T26), inflação americana (média de 4 trimestres), S&P 500 e os três índices de commodities em dólar (IC-Br 205,70, agropecuária 200,53, metais 330,14, `comm_icbr_usd` · set/26). O Brent não é exógena do modelo; entra pela etapa 2.

**Saída do modelo** (central; a faixa de 90% do posterior dos pesos vem abaixo da tabela[^15]):

| Variável | Cenário | 4T26 | 1T27 | 2T27 | 3T27 | 4T27 | 1T28 |
|---|---|---|---|---|---|---|---|
| Selic, fechamento do trimestre (derivada), % a.a. | base | 12,47 | 12,13 | 11,85 | 11,61 | 11,39 | 11,20 |
| | worst | 13,18 | 13,19 | 13,00 | 12,77 | 12,57 | 12,40 |
| | best | 12,16 | 11,56 | 11,18 | 10,93 | 10,71 | 10,51 |
| Selic, média do trimestre, % a.a. | base | 12,65 | 12,28 | 11,99 | 11,72 | 11,49 | 11,29 |
| IPCA 12 meses, fim do trimestre, % | base | 5,27 | 4,84 | 4,32 | 4,32 | 4,21 | 4,07 |
| | worst | 5,29 | 4,90 | 4,44 | 4,49 | 4,39 | 4,22 |
| | best | 5,27 | 4,82 | 4,29 | 4,29 | 4,18 | 4,04 |
| Focus IPCA 12 meses, % | base | 4,16 | 3,97 | 3,78 | 3,67 | 3,58 | 3,51 |
| Hiato, % do potencial | base · worst · best | 0,13 | −0,08 | −0,24 | −0,36 | −0,45 | −0,51 |
| PTAX, fechamento, R$/US$ | base | 5,180 | 5,227 | 5,231 | 5,217 | 5,233 | 5,257 |
| | worst | 5,290 | 5,511 | 5,506 | 5,493 | 5,511 | 5,537 |
| | best | 5,154 | 5,161 | 5,172 | 5,158 | 5,174 | 5,198 |

Faixa do posterior no base, Selic de fechamento: 4T26 12,14 a 12,77; 1T28 10,44 a 12,14. Sensibilidades no base: CDS em 131 em vez de 112 dá 12,47 no 4T26 e 11,22 no 1T28; Fed Funds parado em 3,88 dá 12,47 e 11,20. A NTN-B no padrão (7,84) dá 13,43 e 12,16.

### 3.2 Etapa 2 — o tempero

**(i) Regra de juros: reação ao desvio da expectativa contra a meta (`R.t3`) mais forte que o estimado** · cenário worst
- Coeficiente: estimado 1,962, intervalo de 90% do posterior 1,148 a 2,726. Multiplicador: × 1,3 (2,55), dentro do intervalo, na parte alta.
- Efeito: Selic de fechamento no worst, modelo → com o multiplicador: 4T26 13,18 → 13,34; 1T27 13,19 → 13,46; 2T27 13,00 → 13,35; 3T27 12,77 → 13,16; 4T27 12,57 → 12,98; 1T28 12,40 → 12,79.
- Por quê: o próprio Copom diz que reage hoje mais do que no histórico: "em um ambiente de expectativas desancoradas, como é o caso do atual, exige-se uma restrição monetária maior e por mais tempo do que outrora seria apropriado" (ata da 281ª, §10; igual na 280ª, §9). Com a Focus de 2028 em 3,79% e a inflação implícita de 5 anos em 5,54% (`br_interest_rate` · 15/10, 2,04 p.p. acima da Focus de 2029), um cenário em que o prêmio volta a subir é um em que essa frase vira ação. Fica dentro do intervalo porque a frase descreve o regime atual, não uma quebra.
- Onde entra: limite da cauda worst.

**(i) Regra de juros: menos inércia (`R.t1`)** · cenário best
- Coeficiente: estimado 1,336, intervalo de 90% 1,201 a 1,484. Multiplicador: × 0,95 (1,269), dentro do intervalo.
- Efeito: Selic de fechamento no best: 4T26 12,16 → 12,06; 1T27 11,56 → 11,39; 2T27 11,18 → 10,96; 3T27 10,93 → 10,68; 4T27 10,71 → 10,45; 1T28 10,51 → 10,27.
- Por quê: nos ciclos de corte desde 2005 o Copom começou devagar e acelerou (2005: −25 e depois −50 e −75; 2016: −25, −25 e depois −75 e −100; `pm_copom_reuniao`), e este ciclo ainda não acelerou; se o IPCA de 12 meses voltar para baixo do teto no 2T27 com a NTN-B mais baixa, a aceleração é o padrão histórico. A ressalva da Verde sobre o BC "dócil"[^16] vale aqui: abaixo da central por leniência também conta como best.
- Onde entra: limite da cauda best.

**(ii) Calibração gradual e calendário — o passo do Copom** · cenário base
- Hoje: cinco cortes seguidos de 25 p.b. (`pm_copom_reuniao` · 16/09); "a magnitude total do ciclo de calibração será estabelecida à luz de novas informações" (comunicado da 281ª, §6); Selic em 13,75% até 04/11.
- Por que o modelo não vê: a regra é trimestral, não conhece o calendário de reuniões nem a prática de passo, e suaviza a distância entre a Selic e a âncora, não a Selic. A comunicação do Copom é fator fora das variáveis do modelo.
- Efeito: Selic acima do modelo em ~+0,80 p.p. no 4T26–1T27, ~+0,65 no 2T27–3T27, ~+0,35 no 4T27 e ~0 no 1T28 (mediana do caminho por reunião contra a central). Duração: até o fim de 2027.
- Onde entra: assimetria do cenário base (Pbc − Pwc de −0,95 a −0,10).

**(ii) Petróleo e combustíveis** · cenário worst
- Hoje: Brent US$ 125,44 (`comm_brent` · 06/10), 39% acima do ponto de partida do cenário de referência (~US$ 90, RPM set/26, 2.2) e +80,3% em três meses.
- Por que o modelo não vê: o Brent não é exógena; o IC-Br em dólar entra só na equação do câmbio, e a de monitorados tem só inércia e o IPCA defasado. O repasse a gasolina e diesel, e o que o governo abate dele (Decreto 13.116 e MP 1.391, RPM set/26, nota 45), ficam fora.
- Efeito: uma pausa a mais (+25 p.b.) no 1T27–2T27 sobre o worst com o tempero (i): 1T27 13,71, 2T27 13,60. Duração: dois trimestres; some se o Brent voltar à trajetória do RPM.
- Onde entra: probabilidade da cauda worst no 1T27–2T27 (é parte dos 31% de pausa por reunião).

Um tempero que testei e descartei: o aperto pesando mais no hiato (`H.h2` × 1,5, dentro do intervalo) leva o hiato do 1T28 de −0,51 a −0,85 no base, mas a Selic só de 11,20 para 11,17. No modelo uma desaceleração mais forte chega à Selic só pela Focus, devagar; o risco de baixa "desaceleração mais acentuada" do Copom (comunicado da 281ª, §4) não move a tese dentro do horizonte.

### 3.3 Da etapa 1 à tese

| Trimestre | Central (modelo, base) | Worst: modelo → com tempero | Best: modelo → com tempero |
|---|---|---|---|
| 4T26 | 12,47 | 13,18 → 13,34 | 12,16 → 12,06 |
| 1T27 | 12,13 | 13,19 → 13,46 (13,71 com o petróleo) | 11,56 → 11,39 |
| 2T27 | 11,85 | 13,00 → 13,35 (13,60 com o petróleo) | 11,18 → 10,96 |
| 3T27 | 11,61 | 12,77 → 13,16 | 10,93 → 10,68 |
| 4T27 | 11,39 | 12,57 → 12,98 | 10,71 → 10,45 |
| 1T28 | 11,20 | 12,40 → 12,79 | 10,51 → 10,27 |

A faixa base é a central mais e menos 30 p.b. no 4T26, alargando até 65 p.b. no 1T28, na grade de 25 p.b. das decisões; o worst e o best com tempero ficam fora dela em todos os trimestres, e por isso marcam o que leva a cada cauda. As probabilidades vêm do caminho por reunião, que já embute os dois temperos (ii): o passo gradual põe a massa acima da faixa no começo, e o petróleo é parte das pausas.

## 4. Para os outros agentes

**Respostas às entradas fixas (mapa, Parte 4):**
- **E1 (caminho esperado da Selic):** fechamento do trimestre, central do modelo 12,47 · 12,13 · 11,85 · 11,61 · 11,39 · 11,20 (4T26 a 1T28); a mediana do meu caminho por reunião é 13,25 · 13,00 · 12,50 · 12,25 · 11,75 · 11,25, e a cauda acima da faixa tem 95% · 79% · 61% · 51% · 44% · 29%. Em 04/11: −25 com 65%, manter 25%, −50 10%; em 09/12: −25 57%, manter 30%, −50 12%. Para o carry à frente, use a mediana do caminho, não a central, no 4T26–3T27.
- **E2 (credibilidade):** uma alta hoje seria lida como credibilidade, não como validação de inflação: o CDS está em 112 (`cmb_risco_pais` · 14/10), a dívida em dólar não é o problema de 2002 que torna a alta perversa (Blanchard), e a queda de 0,64 p.p. na inflação implícita de 10 anos depois de 02/10 mostra que o mercado leu o choque de outubro como ganho de credibilidade. Mas a desancoragem segue: Focus 2028 em 3,79% e implícita de 5 anos em 5,54%. O sinal Selic → câmbio é o usual (alta aprecia) enquanto o CDS não subir com a Selic.
- **E3 (o câmbio no Copom):** o Copom condiciona em R$ 5,15 seguindo a PPC e lista "uma taxa de câmbio persistentemente mais depreciada" como risco de alta (comunicado da 281ª, §4); o RPM (2.2) atribui parte da depreciação do 3T26 ao diferencial de juros que diminui. A PTAX em 5,04, 2,1% abaixo do condicionante, é notícia para o Copom, do lado benigno.
- **E4 (reação a uma depreciação):** com a Selic, não com câmbio. O Copom não reage ao efeito primário e reage "com firmeza" ao de segunda ordem (ata da 281ª, §16): uma depreciação primeiro tira cortes (pausa), e só com expectativas subindo vira alta. No modelo, cada 1 p.p. da Focus de 12 meses acima da meta vale 1,96 p.p. de Selic (`R.t3`). As vendas de setembro (US$ 2,0 bi à vista e US$ 2,0 bi em linhas) deixam a pergunta do gatilho aberta até a leitura de S7.

**Pedidos (saídas fixas, mapa, Parte 3):**
- **S1:** a apreciação de 02/10 a 14/10 (PTAX 5,22 → 5,04) é persistente até o fim do 1T27? A probabilidade de pausa em 09/12 (30%) e a força do argumento de Q2 dependem disso.
- **S2:** o movimento de outubro é idiossincrático? Leio PTAX −2,4% em um mês contra o peso mexicano +8,0% e o chileno +4,4% (`cmb_ptax`, `cmb_fx_latam`), mas a conclusão é sua. O caminho base da NTN-B de 10 anos (plano em 6,87%) supõe que a compressão local fica; se ela for majoritariamente global, o worst ganha peso.
- **S3:** quanto de um real em 5,04, contra os 5,15 do Copom, chega a preços livres e administrados até o 1T27; e quanto do Brent a US$ 125 chega à gasolina, dado o abatimento fiscal? O tempero (ii) do petróleo depende disso (até existir o agente de inflação).
- **S4:** onde o real ficará em relação ao condicionante do Copom na data de corte de 04/11 (média de dez dias úteis até 30/10)? A projeção do Copom de novembro, e a manutenção (25%), dependem disso.
- **S5:** o real está precificando estresse fiscal ou institucional? O CDS subiu 19 pontos entre 16/09 e 02/10 e devolveu tudo até 14/10; o cenário worst (CDS 150) depende de saber se aquela alta era fiscal ou eleitoral.
- **S6:** com o diferencial nominal em 10,00 p.p. (`diferenciais_juros` · set/26) e caindo (Fed subindo, Selic caindo), o carry ainda sustenta o real em 2027? O best (Copom acelerando) depende de o câmbio não reagir mal a um diferencial menor.
- **S7:** as vendas de US$ 2,0 bi à vista e US$ 2,0 bi em linhas em set/26 responderam a disfunção ou ao nível? Se ao nível, E4 vira a função de reação inteira, com intervenção, e a dependência do caminho da Selic ao câmbio aumenta.

**Pedidos deste ciclo:**
- Ao câmbio: qual a sua leitura do pregão de 05/10 (PTAX −4,6%, DI de 2 anos −1,10 p.p., NTN-B 10 anos −0,50 p.p., CDS −12 em um dia)? A central do modelo depende da NTN-B de 10 anos ficar onde está, e a sua decomposição global/local é a melhor evidência disponível neste ciclo sobre isso.
- Ao agente fiscal, quando existir: que consolidação a NTN-B de 10 anos a 6,87% está precificando, e quanto de demanda ela tira? É o canal pelo qual o modelo corta 0,95 p.p. de Selic.

## 5. Placar

Primeiro ciclo.

## 6. Sobre o modelo

| Fonte | O que sugere | Teste proposto | Por que importa para a tese deste ciclo |
|---|---|---|---|
| Conceito `interest_rate_smoothing` (ajuste parcial em Clarida, Galí & Gertler: a taxa efetiva fecha só uma fração da distância até a taxa-alvo por período) e Minella et al. 2002 (defasagens da Selic somando 0,8 ou mais na regra do BCB) | Suavizar o **nível** da Selic, não a distância Selic − âncora: Selic_t = ρ1·Selic_t−1 + ρ2·Selic_t−2 + (1 − ρ1 − ρ2)·(âncora_t + t3·desvio_t). Hoje a âncora passa 1 para 1 no mesmo trimestre | Estimar as duas formas da regra (R) no trimestral de 2006 a 2026, com o mesmo posterior; comparar o erro fora da amostra e o efeito de impacto de `rr_10a` na Selic. Se a forma em nível ajustar igual ou melhor e o impacto cair de ~1 para ~(1 − ρ1 − ρ2), a especificação muda | É a diferença inteira entre a central e o mercado no 4T26 (0,91 p.p. contra a curva) |
| Comunicados e calendário do Copom (`pm_copom_calendario`) | A média do trimestre em curso tem uma parte já decidida: a Selic projetada no primeiro trimestre não pode ignorar os dias até a próxima reunião | Em `modelo.py`, restringir a Selic média do trimestre de partida aos dias já fixados (aqui, 35 de 92 a 13,75%) e medir, de 2006 a 2026, o erro do fechamento derivado com e sem a restrição | A média de 12,65% do 4T26 só é atingível com −150/−100 em novembro e dezembro |
| Perrelli & Roache 2014 (neutro em espaço de estados movido pela inflação esperada, pelo juro longo americano e pelo CDS; abordagem pela curva soma o prêmio a termo) e Adrian, Crump & Moench 2013 (prêmio a termo = taxa ajustada − taxa neutra ao risco) | A âncora `rr_10a` mistura neutro, prêmio a termo e prêmio de risco de inflação. A regra talvez devesse reagir só à parte explicada por fundamentos (CDS, juro real americano) | Regredir `rr_10a` no CDS e no juro real americano de 10 anos (2006–2026), separar ajustado e resíduo, e reestimar (R) com os dois termos separados. Se o coeficiente do resíduo for estatisticamente menor que o do ajustado, a âncora deveria ser o ajustado | Em outubro o CDS voltou ao nível de 16/09 e a NTN-B caiu 0,64 p.p.: o modelo trata compressão de prêmio local como queda de neutro |
| RPM set/26, boxe sobre efeitos primários do petróleo (gasolina, diesel e gás somaram 0,42 p.p. ao IPCA em mar–abr/26; efeito indireto do diesel uma ordem de grandeza maior que o direto) | A equação de monitorados (I.IM) não tem petróleo; o Brent em reais (ou o IC-Br energia) como regressor, com uma defasagem | Acrescentar Brent em reais à I.IM no trimestral de 2006 a 2026; se o coeficiente for positivo e o erro fora da amostra cair, entra. Testar também na de bens industriais (efeito indireto) | Hoje o choque de US$ 125 só entra no report pelo tempero (ii) |

---

[^1]: A central é a Selic de fechamento do trimestre do Modelo Estrutural no cenário base, sem ajuste. O modelo só tem a Selic média do trimestre; o fechamento é derivado como a média deste trimestre e do seguinte, uma conta mecânica, que historicamente erra 0,12 p.p. em média.
[^2]: O caminho por reunião é julgamento: para cada reunião, a probabilidade de cada passo depende do passo anterior (um Copom que acabou de pausar tende a pausar de novo; um que cortou 25 tende a repetir), com mais espaço para −50 a partir do 2T27. A distribuição do fechamento de cada trimestre é a soma desses passos. O 1T28 supõe duas reuniões, em janeiro e março, porque o calendário oficial termina em dez/27 e todo primeiro trimestre desde 2006 teve duas reuniões.
[^3]: Horizonte relevante: o trimestre em que o Copom quer ver a inflação de volta à meta, hoje o 1T28, cerca de 18 meses à frente. É longe porque juro leva tempo para agir: o que se decide hoje afeta pouco a inflação dos próximos meses.
[^4]: Efeito primário de um choque de petróleo é a gasolina subir (direto) e o frete encarecer outros preços (indireto). Efeito de segunda ordem é quando isso muda expectativas e salários e passa a subir preços que nada têm a ver com petróleo. O Copom diz que só o segundo pede juro.
[^5]: Meta de inflação como meta para a projeção (Svensson, 1997): o banco central põe o juro onde a sua própria projeção no horizonte relevante fica igual à meta. A inflação de hoje só importa pelo que diz da inflação futura.
[^6]: Hiato é a distância entre o PIB e o que a economia produz sem pressionar preços; positivo é economia aquecida. Ele não é observado e é revisado: Orphanides (2001) mostra que regras de juros desenhadas com o hiato revisado dão respostas diferentes das que se teria com o hiato de tempo real.
[^7]: Juro neutro é o juro real que nem acelera nem freia a economia. Exemplo: com neutro de 5% e Selic real de 8,9%, a política está 3,9 p.p. acima do ponto em que deixaria de frear. É estimado, não observado, e cada fonte usa o seu.
[^8]: Canal do crédito (Bernanke & Gertler, 1995): o juro não age só pelo custo do dinheiro; ele piora o balanço de famílias e empresas (mais juros a pagar, mais inadimplência), e os bancos emprestam menos e mais caro a quem está pior.
[^9]: Prêmio a termo é o que o investidor cobra para travar uma taxa por mais tempo, além da Selic que espera. Se a curva paga mais que a Selic esperada, a diferença é prêmio e não previsão de alta.
[^10]: Percentil 2,5: só 2,5% das janelas de 21 pregões desde 2006 tiveram queda maior da NTN-B de 10 anos. Quanto menor o percentil, mais raro o recuo.
[^11]: 05/10 foi o primeiro pregão depois do 1º turno da eleição presidencial (04/10). O F deste ciclo não traz dado eleitoral, nem dado fiscal posterior a ago/26: o report lê o movimento pelos preços e não afirma a causa. A Verde leu o mesmo tipo de movimento em out/2022 (prêmio eleitoral na curva que comprime quando o resultado reduz o risco de cauda, "rally importante no primeiro pregão de outubro", Verde §2.1); é um modo de raciocinar, não um dado sobre 2026.
[^12]: O QPC é o questionário que o Copom manda aos economistas antes de cada reunião. O da 281ª foi respondido antes de 16/09, portanto antes de 05/10.
[^13]: Gürkaynak, Sack & Swanson (2005), para o Fed: a parte das decisões que move os juros de 5 e 10 anos é quase toda a sinalização do caminho futuro, não a surpresa com a taxa do dia.
[^14]: Inflação implícita é a diferença entre o juro prefixado e o juro real da NTN-B do mesmo prazo: a inflação que o mercado cobra, com prêmio de risco de inflação dentro. Uma queda dela é o mercado cobrando menos proteção contra inflação.
[^15]: A faixa do modelo vem só da incerteza dos pesos estimados; não inclui o erro das equações, e por isso não é um intervalo de previsão. A distribuição da tese é do agente.
[^16]: "BC dócil" (Verde, jan/2022, §2.6): um Banco Central que mantém juro baixo enquanto cortes de imposto seguram a inflação medida. A meta cumprida assim é custo adiado, e uma Selic baixa por esse motivo aparece como "best" no placar sem ser boa notícia.
