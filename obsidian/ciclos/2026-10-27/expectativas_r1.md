# Report — expectativas · ciclo 2026-10-27 · rodada 1

Dados até: Focus de 23/10/2026; curvas, PTAX e CDS de 26/10/2026; QPC de 23/09/2026 · Horizontes: 4T26 a 1T28, com a variável medida como a **média das pesquisas do trimestre** da Focus IPCA 12 meses à frente, suavizada, base de 30 dias, mediana (a `focus_12m` do Modelo Estrutural)[^6]

## 1. Tese

| Variável | Trimestre | Central | Base: faixa · P | Upside: limite · P | Downside: limite · P | P(up) − P(down) |
|---|---|---|---|---|---|---|
| Focus IPCA 12m, média do trimestre (% a.a.) | 4T26 | 4,16 | 4,05 a 4,45 · 14% | acima de 4,45 · 85% | abaixo de 4,05 · 1% | +0,84 |
| | 1T27 | 3,97 | 3,80 a 4,15 · 30% | acima de 4,15 · 65% | abaixo de 3,80 · 5% | +0,60 |
| | 2T27 | 3,78 | 3,60 a 3,95 · 38% | acima de 3,95 · 55% | abaixo de 3,60 · 7% | +0,48 |
| | 3T27 | 3,67 | 3,45 a 3,90 · 40% | acima de 3,90 · 52% | abaixo de 3,45 · 8% | +0,44 |
| | 4T27 | 3,59 | 3,35 a 3,90 · 42% | acima de 3,90 · 48% | abaixo de 3,35 · 10% | +0,38 |
| | 1T28 | 3,52 | 3,25 a 3,75 · 42% | acima de 3,75 · 47% | abaixo de 3,25 · 11% | +0,36 |

- **Como a faixa foi desenhada.** O limite de cima de cada trimestre é a trajetória que a própria Focus de 23/10 implica **se ninguém revisar** (4,47; 4,17; 3,93; 3,88; 3,87; 3,70, das medianas mensais, trimestrais e anuais de `expc_focus_periodo` (inflação) · 23/10)[^9]. Upside quer dizer, portanto, a pesquisa revisar para cima a partir dela mesma. O de baixo fica um pouco abaixo da central do modelo, onde o cenário de downside com tempero chega.
- **Upside, ruim para o Brasil (desancoragem): acima de 4,45 no 4T26 e de 3,75 a 3,95 de 2T27 em diante.** O caminho é o choque de 26/10 persistir e a pesquisa incorporá-lo além do que passa pela inflação. Na etapa 1, CDS a 190 p.b. e vol a 18% levam a PTAX do modelo a 5,60 e a Focus só a 4,17 no 4T26 e 3,59 no 1T28. Na etapa 2, com o peso da meta na (E) caindo de 0,26 para 0,03 (E.e1 × 1,3 e E.e2 × 1,3), ela fica em 4,52 a 4,58 nos seis trimestres. A expectativa para de convergir.
- **Downside, bom para o Brasil (convergência mais rápida): abaixo de 4,05 no 4T26 e de 3,25 no 1T28.** O caminho é o choque de 26/10 se desfazer, com o CDS de volta ao nível de 06 a 09/10, e a âncora puxar mais do que a mediana do posterior. Na etapa 1, CDS a 110 p.b. e vol a 11% dão PTAX de 5,08 no modelo e Focus de 4,16 a 3,49. Na etapa 2, com E.e1 × 0,8, a Focus vai a 4,00 e chega a 3,32 no 1T28. No 4T26 isso é quase impossível pela aritmética das pesquisas já feitas: 1%.
- **A tese em uma frase:** a expectativa de 12 meses converge mais devagar do que o modelo projeta. O modelo a põe em 4,16 no 4T26, mas as 16 pesquisas já feitas no trimestre têm média de 4,52. A pesquisa de 23/10 já implicava uma trajetória 0,15 a 0,31 p.p. acima da central em todos os trimestres, antes do pior pregão de inflação implícita desde 2006 (26/10). O risco de cima predomina nos seis trimestres (P(up) − P(down) de +0,84 a +0,36), pela inércia que a (E) subestima desde 2024 e pela revisão que a pesquisa ainda não mostra.

## 2. Argumentação

### O que mudou depois da última pesquisa: o pregão de 26/10

A Focus mais recente do F é de 23/10, uma sexta-feira[^7]. O pregão seguinte foi o maior choque de preços de inflação da amostra:

| Série | 23/10 | 26/10 | Variação no dia | Onde fica na história |
|---|---|---|---|---|
| PTAX venda (`cmb_ptax`) | 5,0377 | 5,5007 | +9,19% | 2ª maior alta diária desde fev/1999, atrás só de 08/10/2008 (+9,33%) |
| CDS 5 anos (`cmb_risco_pais`) | 119 | 137 | +18 p.b. | — |
| Inflação implícita 2 anos (`br_interest_rate`) | 5,46% | 6,69% | +1,23 p.p. | maior alta diária desde 2006 (a anterior, +0,95 em 22/10/2008) |
| Inflação implícita 5 anos (`br_interest_rate`) | 5,60% | 6,81% | +1,20 p.p. | maior alta diária desde 2006 (a anterior, +0,88 em 22/10/2008) |
| DI × pré 2 anos (`br_interest_rate`) | 12,67% | 15,19% | +2,52 p.p. | — |

Fonte: G sobre `cmb_ptax`, `cmb_risco_pais` e `br_interest_rate` · 23/10 e 26/10. Três fontes independentes andam juntas, o que afasta erro de dado. O F não diz o que causou o choque. O pregão é o primeiro depois do fim de semana de 24 e 25/10. O de 05/10 (PTAX de 5,22 para 4,99, −4,55%, implícita de 2 anos de 5,89% para 5,24%, mesmas tabelas · 02/10 e 05/10) foi o primeiro depois de 03 e 04/10, na direção oposta. A hipótese que o calendário sugere são os dois turnos da eleição presidencial. Ela não sustenta nada neste report e vai como pedido ao agente web (seção 4).

O que isso faz com a tese: **toda a leitura da pesquisa abaixo é anterior ao choque.** A base de 4 dias úteis[^4] de 23/10 não podia mostrá-lo. As próximas pesquisas são as primeiras com ele.

### Q1 — As expectativas estão ancoradas na meta?

Não. A distância à meta é positiva em todos os horizontes e está no quinto superior da história em todos. Nos longos ela está parada, e não subindo:

| Horizonte | Expectativa − meta (p.p.) | Δ desde 02/10 | Pctl hist.[^1] | Pctl 10a | Maior da série |
|---|---|---|---|---|---|
| 12 meses à frente | +1,53 | −0,06 | 79 | 77 | +8,35 (19/12/2002) |
| ano corrente (2026) | +2,19 | +0,18 | 78 | 77 | +9,06 (31/12/2002) |
| t+1 (2027) | +1,34 | +0,04 | 84 | 87 | +7,00 (13/12/2002) |
| t+2 (2028) | +0,75 | −0,05 | 82 | 83 | +2,50 (31/12/2002) |
| t+3 (2029) | +0,50 | −0,01 | 86 | 87 | +1,50 (09/12/2002) |

Fonte: "Desancoragem", `expc_focus` e `expc_focus_periodo` (inflação) · 23/10.

- **Os longos estão desancorados em nível, mas parados.** t+2 e t+3, onde a ancoragem se julga, estão acima de 82% e de 86% das leituras desde 2000. A mediana de 2029 e a de 2030 são 3,50, meio ponto acima da meta (`expc_focus_periodo` (inflação) · 23/10). Nas últimas quatro semanas elas variaram −0,00 e +0,00. A desancoragem é antiga e estável, e não está acelerando na pesquisa. **Mas** a medida de mercado desses mesmos horizontes saltou. A implícita de 5 anos está 3,81 p.p. acima da meta, no percentil 97 da história e 99 dos 10 anos (`br_interest_rate` · 26/10), e subiu 1,20 p.p. num só pregão. Se a pesquisa seguir o mercado, Q1 deixa de ser "desancorada e parada" e passa a "desancorando".
- **A cauda de respondentes nos longos está acima.** Em t+3, a média passa a mediana em 0,115 p.p. (3,62 contra 3,50 em 2029), no percentil 71 da história desde 2000 e 72 dos 10 anos (G sobre `expc_focus_periodo` (inflação) · 23/10). É um grupo de respondentes acima de 3,50, e não um deslocamento do centro. Em t+2 a média é igual à mediana (+0,004, percentil 33).
- **Os curtos se movem por choque já visível.** O ano corrente subiu 0,18 p.p. desde 02/10 (2026 de 5,01 para 5,19). A pesquisa se aperta em torno disso: desvio-padrão de 0,15, de 4,80 a 5,75, 142 respondentes (`expc_focus_periodo` (inflação) · 23/10). É inflação realizada entrando no ano, e não crença.

### Q2 — O que move as expectativas, e é nível ou ruído?

**No horizonte de 12 meses, o movimento das quatro semanas até 23/10 é aritmética e ruído, e não revisão.** A Focus 12m caiu 0,11 p.p. (de 4,64 em 25/09 para 4,53, `expc_focus` (inflação) · 23/10). Os indicadores de revisão não andaram: a base de 4 dias úteis está 0,02 p.p. acima da de 30 dias (4,56 contra 4,53), a média é igual à mediana e o desvio-padrão é de 0,47 (percentil 73 do desvio, `expc_focus` (inflação) · 23/10). A queda vem da janela. A série sem suavização caiu de 4,88 para 4,48 entre 08 e 09/10 (`expc_focus` (inflação) · 08/10 e 09/10), quando um mês alto saiu da janela, e a suavizada acompanhou aos poucos. É o efeito do mapa (2.1, armadilha): um mês que sai da janela move a série sem ninguém mudar de ideia.

**Por componente, a pressão de curto prazo é de choques datados. A de longo prazo está em serviços.**

| Componente | 12m | Δ 13 sem. (12m) | Pctl 12m (desde 2021) | 24m | 2028 (Δ 4 sem.) | 2029 (Δ 4 sem.) |
|---|---|---|---|---|---|---|
| IPCA | 4,53 | +0,35 | 42 | 3,87 | 3,75 (−0,05) | 3,50 (−0,00) |
| Livres | 4,80 | +0,27 | 66 | 4,00 | 3,90 (+0,00) | 3,66 (+0,10) |
| Administrados | 4,10 | +0,60 | 45 | 3,56 | 3,63 (+0,01) | 3,50 (+0,00) |
| Serviços | 5,20 | −0,06 | 40 | 4,81 | 4,65 (+0,15) | 4,10 (+0,10) |
| Bens industrializados | 2,60 | −0,25 | 31 | 2,68 | 2,80 (+0,00) | 2,98 (+0,00) |
| Alimentação no domicílio | 6,77 | +1,21 | 99 | 4,49 | 4,00 (+0,00) | 4,00 (+0,00) |

Fonte: `expc_focus` (inflação) e `expc_focus_periodo` (inflação) · 23/10.

- **Alimentação e administrados são o choque datado.** A alimentação no domicílio em 12 meses está no percentil 99 desde 2021 e subiu 1,21 p.p. em 13 semanas. Em 2026 ela subiu 0,53 p.p. em 4 semanas, para 7,38. A pesquisa a vê voltar a 4,00 em 2028 e 2029. Os administrados em 24 meses estão no percentil 5. O movimento é concentrado e com data para acabar: o tipo de pressão que não deveria tocar os longos (mapa 2.4).
- **Serviços é a exceção, e é o sinal deste ciclo na composição.** Serviços em 2028 subiu 0,15 p.p. e em 2029 0,10 p.p. em 4 semanas. Os preços livres de 2029 subiram 0,10. No mesmo período, o IPCA de 2028 caiu 0,05 e o de 2029 não se moveu (`expc_focus_periodo` (inflação) · 23/10). É a composição dizendo mais que o cheio, que é o que o agente de inflação pediu para ser avisado (XE4). **Mas** o painel dos componentes é menor (65 respondentes em serviços 2028, contra 124 no IPCA 2028), e 0,10 a 0,15 p.p. em quatro semanas pode ser troca de respondentes. Duas pesquisas seguidas com serviços 2029 acima de 4,10 confirmariam.
- **A pesquisa espera menos demanda, o que torna a alta de serviços longos menos explicável por atividade.**

| PIB (Focus) | 2026 | Δ 13 sem. | 2027 | Δ 13 sem. | 2028 | Δ 13 sem. |
|---|---|---|---|---|---|---|
| PIB | 1,80 | −0,19 | 1,31 | −0,29 | 1,81 | −0,19 |
| Consumo das famílias | 1,30 | −0,70 | 1,20 | −0,40 | 1,80 | −0,18 |
| Investimento (FBCF) | 0,90 | +0,00 | 1,06 | −0,54 | 1,75 | −0,15 |
| Agropecuária | 2,50 | +0,90 | 1,00 | −1,00 | 2,51 | +0,01 |
| Serviços (setor) | 1,70 | −0,30 | 1,50 | −0,14 | 1,80 | −0,20 |

Fonte: `expc_focus_periodo` (PIB) · 23/10. Os respondentes cortaram consumo e investimento de 2027, a demanda que pressionaria preços (mapa 2.9). O QPC de 23/09 tem a mesma leitura: hiato de +0,20 no 4T26 e de −0,20 no 4T27, que na pergunta anterior eram +0,21 e 0,00 (`expc_qpc` · 23/09). Uma pesquisa que corta demanda e sobe serviços longos está dizendo que serviços não cai por inércia ou indexação, e não por aquecimento. Se é isso mesmo é pergunta ao agente de atividade (XS9) e ao de inflação (XS5).

### Q3 — Pesquisa, mercado e Copom: onde divergem, e o que isso diz da credibilidade

| Fonte | Horizonte | IPCA (%) | Data |
|---|---|---|---|
| Copom, cenário de referência[^8] | 4 trimestres até 1T28 | 3,2 | 24/09 (`pm_copom_projecoes`) |
| QPC, mediana[^3] | 4 trimestres até 1T28 | 4,00 (p25 a p75: 3,77 a 4,20) | 23/09 (`expc_qpc`) |
| Focus, medianas trimestrais 2T27 a 1T28 compostas | 4 trimestres até 1T28 | 4,03 | 23/10 (G sobre `expc_focus_periodo` (inflação)) |
| Focus 24m | 24 meses | 3,87 | 23/10 (`expc_focus` (inflação)) |
| Inflação implícita 2 anos[^5] | 2 anos | 5,46 em 23/10 → 6,69 em 26/10 | `br_interest_rate` |
| Inflação implícita 5 anos | 5 anos | 5,60 em 23/10 → 6,81 em 26/10 | `br_interest_rate` |

- **Pesquisa contra Copom: 0,8 p.p. no horizonte relevante, com a mesma Selic.** A projeção de 3,2 do Copom usa a Selic da Focus. Com essa mesma Selic, a Focus espera 4,03 e o QPC 4,00 para os quatro trimestres até 1T28. Os respondentes não compram a convergência que o modelo do Copom produz com o juro que eles mesmos esperam. É um déficit de credibilidade medido, e anterior a 26/10. Leio só a distância. O que o Copom disse sobre ela é do agente de política monetária (XS2).
- **Pesquisa contra mercado: o mercado saiu na frente, e muito.** Antes do choque, a implícita de 2 anos já estava 1,59 p.p. acima da Focus 24m, no percentil 62 desde 2021. Com a curva de 26/10 contra a Focus de 23/10, a distância vai a 2,82 p.p., percentil 96. Em 12 meses vai a 3,34 p.p., percentil 100 desde 2006, abaixo só dos +3,61 de 07/01/2025 (G sobre `br_interest_rate` e `expc_focus` (inflação)). A implícita carrega prêmio de risco de inflação, e o vértice de 1 ano tem distorção de carregamento da NTN-B curta. Por isso não leio o nível como expectativa. Leio a direção e o tamanho do salto: num dia o mercado passou a cobrar 1,2 p.p. a mais de inflação em 2 a 5 anos, e a pesquisa ainda não teve como responder. **Mas** em 05/10 a mesma curva caiu 0,65 p.p. no vértice de 2 anos num só pregão e devolveu cerca de um terço disso em três semanas (5,24 em 05/10, 5,46 em 23/10, `br_interest_rate`; a PTAX devolveu ~22% da queda de 4,55%). Um salto desse tamanho pode ser, em parte, prêmio de evento, que sai quando a incerteza se resolve. Prêmio persistente seria a implícita de 5 anos acima de 6,5% por duas semanas.
- **A pesquisa contra ela mesma: espera a Selic chegar ao neutro com a inflação acima da meta.**

| Ano | Selic fim de ano | IPCA do ano | IPCA − meta | Juro real implícito na pesquisa |
|---|---|---|---|---|
| 2026 | 13,25 | 5,19 | +2,19 | 7,66 |
| 2027 | 11,75 | 4,34 | +1,34 | 7,11 |
| 2028 | 10,00 | 3,75 | +0,75 | 6,02 |
| 2029 | 10,00 | 3,50 | +0,50 | 6,28 |

Fonte: "A pesquisa contra ela mesma", `expc_focus_periodo` (Selic e inflação) · 23/10. Em 2028 o juro real que a pesquisa espera (6,02%) é o neutro de 2 anos do QPC (6,00%, `expc_qpc` · R279, 24/06), com a inflação ainda 0,75 p.p. acima da meta. Em 2029 e 2030 a pesquisa não espera a meta em ano nenhum. Nas quatro semanas até 23/10, ela cortou a Selic de 2028 em 0,50 p.p. (de 10,50 para 10,00) e a inflação de 2028 em só 0,05. Pôs mais corte sem pôr menos inflação: o sinal de credibilidade do mapa 2.8, na direção de um Copom que aceita inflação acima da meta. **Mas** o neutro do QPC é de junho, e o juro real de 7,11% em 2027 está acima dele, o que é coerente com convergência. O sinal é de 2028 em diante. Se o Copom vai reagir ao choque de 26/10 é do agente de política monetária (XS1), e o QPC de 23/09 dava 97% para corte de 25 p.b. na R281 e 53% para pausa na R282.

### Q4 — O cenário para a Focus 12m: por que a central, por que a distribuição

**A central é a do modelo, e o modelo a puxa para baixo pela meta, não por inflação menor.** No 4T26 a (E) dá ≈4,16 como soma de três termos: inércia, 0,581 × 4,37 (a média do 3T26) = 2,54; IPCA de 12 meses, 0,162 × 5,28 (o IPCA do 4T26 no modelo) = 0,85; meta, 0,257 × 3,00 = 0,77 (G `xp_equacao_E` sobre o retrato do modelo). Contra ficar parada em 4,37, a meta puxa −0,35 p.p. e a inflação empurra +0,15. A expectativa cai mesmo com a inflação de 12 meses do modelo **subindo** de 4,58 para 5,28. Daí em diante ela segue a inflação do modelo, que desce a 4,08 no 1T28, e a meta, e chega a 3,52. Para a Selic, como fato do modelo: a (R) reage a esse desvio, e a Selic média do cenário base vai de 13,60 no 4T26 a 12,27 no 1T28.

**O que o modelo erra, e por quê.** Três evidências, todas na mesma direção:
1. **A aritmética do 4T26.** As 16 pesquisas do trimestre já feitas têm média de 4,52 (`expc_focus` (inflação) · até 23/10). Para o trimestre fechar em 4,16, as 46 a 49 restantes teriam de marcar em média 4,04, quase meio ponto abaixo do nível de 23/10 (G `xp_trajetoria_pesquisa`). Uma queda dessas na média das 46 pesquisas seguintes aconteceu em 3,1% dos dias desde 2001 e em 2,0% nos últimos 10 anos (G `xp_historico` (a) sobre `expc_focus` (inflação)). E isso com o real se depreciando 9% no meio do trimestre.
2. **A trajetória da própria pesquisa.** Montada com as medianas mensais, trimestrais e anuais de 23/10 e sem nenhuma revisão[^9], a Focus 12m dá 4,47, 4,17, 3,93, 3,88, 3,87 e 3,70 do 4T26 ao 1T28. São 0,31, 0,20, 0,15, 0,21, 0,28 e 0,18 p.p. acima da central do modelo. O modelo exige que os respondentes revisem **para baixo** a cada trimestre só para chegar à central.
3. **O viés recente da (E).** Nos últimos 8 trimestres (4T24 a 3T26), o resíduo de um passo da (E) foi positivo em 7, com média de +0,35 p.p. O do 3T26 (+0,50; a (E) dava 3,86 e a Focus foi 4,37) está no percentil 91 dos resíduos da amostra, cujo desvio-padrão é 0,34 (G `xp_equacao_E` sobre o retrato do modelo). Para esse viés sumir, o peso da meta teria de cair de 0,26 para ~0,03 (E.e1 × 1,3 e E.e2 × 1,3). Nos últimos dois anos a pesquisa se comportou como se a meta de 3,00 quase não puxasse. Isso bate com os longos parados em 3,50: a âncora de fato dos respondentes é 3,50, e não 3,00.

A âncora da (E) é imposta: o modelo não produz desancoragem além da trajetória da inflação (mapa 2.1). Por isso essa leitura entra como tempero (i) e não move a central.

**Por que a distribuição é tão assimétrica para cima.** O upside, ruim, ganha nos seis trimestres por quatro motivos. O tempero (i) no cenário base: só com E.e1 × 1,2, ainda dentro do posterior, a trajetória vai a 4,32, 4,22, 4,08, 3,98, 3,91 e 3,84, perto ou acima do limite de cima da faixa. O choque de 26/10, que a pesquisa ainda não incorporou (tempero (ii) 1). O mercado à frente da pesquisa (tempero (ii) 2). O balanço de riscos do próprio QPC, com 60% vendo risco de alta para o IPCA de 2027 e 5% de baixa (`expc_qpc` · 23/09).

Contra o upside, três coisas. **Mas** depois de 45 episódios de depreciação de 5% ou mais em 21 dias úteis desde 2001, a Focus 12m subiu em 56% deles, com mediana de +0,09 p.p. em 45 dias úteis (p25 −0,20, p75 +0,23; G `xp_historico` (d) sobre `cmb_ptax` e `expc_focus` (inflação)). Câmbio sozinho não basta. As altas grandes (+0,92 em ago/2002, +0,85 em out/2020, +0,82 em jan/2021, +0,96 em out/2024) vieram em episódios que o F não qualifica. Também contra: a pesquisa corta demanda; e bens industrializados, o componente mais sensível ao câmbio, caíam até 23/10 (2,60 em 12m, −0,25 em 13 semanas).

O downside, bom, tem 1% a 11%. Ele precisa do choque desfeito **e** de uma âncora mais forte que a mediana do posterior, e a amostra recente diz o contrário.

A assimetria cai com o horizonte (+0,84 → +0,36) porque o 4T26 é quase todo aritmética já dada, enquanto o 1T28 depende de inflação que ainda não aconteceu.

### Olhado, sem sinal

- Focus 24m, base de 4 dias contra 30 dias · −0,01 p.p. (3,87 contra 3,87, `expc_focus` (inflação) · 23/10) · as respostas frescas não divergem · diria algo se a de 4 dias passar a de 30 dias em mais de 0,10 nas pesquisas de depois de 26/10.
- Desvio-padrão e mínimo–máximo de 2027 · 0,43, de 3,25 a 6,00, 142 respondentes (`expc_focus_periodo` (inflação) · 23/10) · dispersão normal para t+1 · diria algo se o desvio subir com a mediana parada (revisão a caminho).
- IPCA trimestral da Focus · 4/2026 em 1,19 (−0,05 em 4 sem.), 1/2027 em 1,63 (+0,10) (`expc_focus_periodo` (inflação) · 23/10) · já está dentro da trajetória sem revisão · diria algo se 1/2027 subir junto com o câmbio da pesquisa.
- Câmbio da Focus · 2026 em 5,05 (−0,15 em 4 sem.), 2027 em 5,15 (`expc_focus_periodo` (câmbio) · 23/10) · é anterior a 26/10 e ficou 0,45 abaixo da PTAX de 26/10 (5,50, `cmb_ptax`) · diria algo quando a pesquisa revisar o câmbio de fim de ano para perto de 5,50 (XE1).
- Selic por reunião · R7/2026 em 13,50 (sem mudança), R1/2027 em 13,00 (−0,50 em 4 sem.) (`expc_focus_copom` · 23/10) · trajetória do juro é do agente de política monetária · diria algo para a tese se a pesquisa tirar cortes com a inflação esperada subindo (credibilidade recuperada) ou mantiver cortes com ela subindo (o contrário).
- Variáveis estruturais do QPC · neutro de 5 anos 5,50, PIB potencial 2,00 (`expc_qpc` · R279, 24/06) · de junho, sem dado novo · diria algo se o próximo QPC subir o neutro, o que mudaria a leitura de 2028 em Q3.
- Exportação e importação da Focus · 2027 em 3,00 e 1,96 (`expc_focus_periodo` (PIB) · 23/10) · não chegam à inflação esperada por canal que o mapa liste · diria algo num choque externo (XE9).
- IPCA-15 de outubro · 0,32 (`inflc_agregados` · out/2026) contra a mediana mensal da Focus para outubro de 0,28 (`expc_focus_periodo` (inflação) · 23/10) · surpresa pequena, e a leitura da inflação é do agente de inflação · diria algo se o IPCA cheio de outubro passar de 0,40 (XS6).

## 3. Premissas

### 3.1 Etapa 1 — o modelo

**Cenários.**
- **Base:** o padrão do simulador. As exógenas ficam no último valor (CDS em 131 p.b., o fechamento do 3T26; meta de 3,00). Na rodada 1, este agente não é principal nem subordinado de exógena nenhuma e não tem os caminhos dos principais. O cenário base não carrega o choque de 26/10: a PTAX do modelo fecha o 4T26 em 5,21, contra 5,50 no mercado em 26/10. Esta é a premissa mais frágil do report, e é do agente de câmbio (XS7).
- **Upside:** o choque de 26/10 persiste. O prêmio de risco soberano e a volatilidade cambial ficam altos o trimestre inteiro, e a PTAX do modelo vai para perto do mercado de 26/10.
- **Downside:** o choque de 26/10 se desfaz. O CDS volta ao nível de 06 a 09/10 e a vol cai.

**Caminhos das exógenas.** Só as que os cenários mudam. As outras ficam no padrão do simulador. Nenhuma destas é deste agente: os caminhos de upside e downside são a **condição das caudas**, ficam só neste report e não vão para o JSON.

| Exógena | Hoje (valor · tabela · data) | Cenário | 4T26 | 1T27 | 2T27 | 3T27 | 4T27 | 1T28 |
|---|---|---|---|---|---|---|---|---|
| CDS 5 anos (`fiscal`, fechamento, p.b.) | 137 · `cmb_risco_pais` · 26/10 | base (padrão) | 131 | 131 | 131 | 131 | 131 | 131 |
| | | upside | 190 | 190 | 190 | 190 | 190 | 190 |
| | | downside | 110 | 110 | 110 | 110 | 110 | 110 |
| Vol implícita do dólar (`vol`, fechamento, % a.a.) | 12,19 · simulador, último dado 2T26 (fora do meu F) | base (padrão) | 12,19 | 12,19 | 12,19 | 12,19 | 12,19 | 12,19 |
| | | upside | 18 | 18 | 18 | 18 | 18 | 18 |
| | | downside | 11 | 11 | 11 | 11 | 11 | 11 |
| Meta 12 meses (`meta_12m`, % a.a.) | 3,00 · `inflc_meta` · 2026 | todos (padrão) | 3,00 | 3,00 | 3,00 | 3,00 | 3,00 | 3,00 |

Motivo dos caminhos: CDS de 190 e vol de 18 foram escolhidos para a PTAX do modelo chegar a ~5,60 no 4T26, perto da PTAX de 5,50 de 26/10. O cenário é "o mercado de 26/10 vira o trimestre", e não uma leitura própria de fiscal ou câmbio. O CDS de 110 é o nível de 06 a 09/10 (108,8 a 110,5, `cmb_risco_pais`).

**Saída do modelo** (G `xp_cenarios`, central [faixa de 90% do posterior dos pesos, que não é intervalo de previsão]).

| Variável | Cenário | 4T26 | 1T27 | 2T27 | 3T27 | 4T27 | 1T28 |
|---|---|---|---|---|---|---|---|
| Focus 12m | base | 4,16 [4,06; 4,27] | 3,97 [3,82; 4,14] | 3,78 [3,61; 3,98] | 3,67 [3,51; 3,87] | 3,59 [3,43; 3,79] | 3,52 [3,36; 3,72] |
| | upside | 4,17 | 4,00 | 3,83 | 3,74 | 3,66 | 3,59 |
| | downside | 4,16 | 3,97 | 3,76 | 3,65 | 3,56 | 3,49 |
| IPCA 12m | base | 5,28 | 4,85 | 4,33 | 4,34 | 4,23 | 4,08 |
| | upside | 5,32 | 4,99 | 4,53 | 4,58 | 4,45 | 4,24 |
| | downside | 5,26 | 4,80 | 4,26 | 4,25 | 4,15 | 4,02 |
| PTAX fechamento | base · upside · downside | 5,21 · 5,60 · 5,08 | 5,25 · 5,63 · 5,12 | 5,25 · 5,63 · 5,12 | 5,24 · 5,62 · 5,11 | 5,25 · 5,63 · 5,13 | 5,28 · 5,66 · 5,15 |
| Selic média | base · upside · downside | 13,60 · 13,60 · 13,60 | 13,26 · 13,27 · 13,25 | 12,96 · 12,99 · 12,95 | 12,70 · 12,75 · 12,68 | 12,47 · 12,55 · 12,44 | 12,27 · 12,37 · 12,23 |

No modelo, uma PTAX 7,5% mais alta (5,60 contra 5,21) sobe o IPCA de 12 meses em 0,04 a 0,24 p.p. e a Focus em só 0,01 a 0,07 p.p. O câmbio chega à expectativa só pela inflação, com peso 0,16. Esse é o canal que está no modelo. Tudo o que a expectativa fizer além dele é tempero.

### 3.2 Etapa 2 — o tempero qualitativo

**(i) E.e1 (inércia da expectativa) — efeito mais forte que o estimado** · cenário base
- Coeficiente: estimado 0,581, intervalo de 90% do posterior de 0,452 a 0,710. Multiplicador × 1,2 (0,697, percentil 92 do posterior): **dentro** do intervalo. O peso da meta cai de 0,257 para 0,141.
- Efeito: Focus 12m de 4,16 / 3,97 / 3,78 / 3,67 / 3,59 / 3,52 para 4,32 / 4,22 / 4,08 / 3,98 / 3,91 / 3,84. A Selic do modelo no 1T28 vai de 12,27 para 12,78.
- Por quê: 7 dos 8 últimos resíduos de um passo da (E) foram positivos, com média de +0,35. Com × 1,2 o viés cai para +0,19 (G `xp_equacao_E`). Os longos da pesquisa parados em 3,50 desde pelo menos o ciclo anterior mostram uma âncora de fato acima da meta.
- Onde entra: assimetria do cenário base nos seis trimestres. É o principal motivo de P(up) ≥ 47% mesmo em 4T27 e 1T28.

**(i) E.e1 × 1,3 e E.e2 × 1,3 — âncora quase sem peso** · cenário upside
- Coeficientes: e1 × 1,3 = 0,756, percentil 98,9 do posterior, **fora** do intervalo (0,452 a 0,710). e2 × 1,3 = 0,210, percentil 93,8, dentro do intervalo (0,109 a 0,216). O peso da meta vai a 0,034.
- Efeito: no cenário upside, a Focus 12m vai de 4,17 / 4,00 / 3,83 / 3,74 / 3,66 / 3,59 para 4,52 / 4,58 / 4,54 / 4,55 / 4,55 / 4,53. A Selic média do modelo para de cair: 13,71 no 1T28.
- Por quê, fora do intervalo: é o multiplicador que zera o viés dos 8 últimos trimestres (viés de +0,025, G `xp_equacao_E`). O peso da meta foi estimado de 2002 a 2026, em boa parte com os longos perto da meta. Hoje t+3 está 0,50 acima, no percentil 86. O choque de 26/10 é do tipo em que a (E) mais errou: o maior resíduo dos últimos 14 trimestres (+1,24, 1T25) veio depois do episódio de out/2024, em que a Focus 12m subiu 0,96 p.p. em 45 dias úteis (G `xp_historico` (d)). A (E) é linear e esses episódios não são.
- Onde entra: limite e probabilidade da cauda de cima.

**(i) E.e1 × 0,8 — âncora mais forte** · cenário downside
- Coeficiente: e1 × 0,8 = 0,465, percentil 6 do posterior, dentro do intervalo.
- Efeito: no downside, a Focus 12m vai de 4,16 / 3,97 / 3,76 / 3,65 / 3,56 / 3,49 para 4,00 / 3,75 / 3,55 / 3,44 / 3,37 / 3,32.
- Por quê: é a âncora mais forte que o posterior admite sem sair dele. A amostra recente diz o contrário, por isso a cauda é magra.
- Onde entra: limite e probabilidade da cauda de baixo.

**(ii) Revisão em curso que a mediana ainda não mostra — Focus 12m e t+2/t+3 nas pesquisas depois de 26/10** · cenários base e upside
- Hoje: Focus 12m em 4,53, base de 4 dias em 4,56 (`expc_focus` (inflação) · 23/10), anterior ao pregão de 26/10 (PTAX +9,19%, implícita de 2 e 5 anos +1,2 p.p.).
- Por que o modelo não vê: a (E) só recebe o choque pela inflação de 12 meses, e com peso 0,16. A reação direta dos respondentes a um choque de câmbio e de prêmio desse tamanho (mapa 2.3 e 2.4), além do repasse, não está em termo nenhum. O modelo também não sabe o que já foi pesquisado no trimestre corrente.
- Efeito: de +0,15 a +0,30 p.p. sobre a trajetória sem revisão no 4T26 e no 1T27, sumindo até o 3T27. O tamanho vem do p75 dos episódios de depreciação de 5% ou mais (+0,23 em 45 dias úteis, desde 2010 +0,27). Este choque está no topo da distribuição de tamanho, e os episódios grandes chegaram a +0,8 a +0,96. A duração (até o 3T27) é julgamento: o choque de 05/10 foi devolvido só em um terço na implícita em três semanas, então não assumo reversão rápida.
- Onde entra: probabilidade do upside no 4T26 e no 1T27 (85% e 65%).

**(ii) O mercado à frente da pesquisa — inflação implícita de 2 e 5 anos** · cenário base
- Hoje: 6,69% e 6,81% (`br_interest_rate` · 26/10). A distância para a Focus 24m vai a +2,82 p.p., percentil 96 desde 2021.
- Por que o modelo não vê: a (E) explica a pesquisa, e a curva não entra nela (mapa 2.6).
- Efeito: direção para cima nos longos da pesquisa (t+2, t+3). O tamanho não sai do F, porque a parte de prêmio é desconhecida. O movimento de 05/10 foi devolvido só em um terço em três semanas. Uso só a direção, por dois trimestres.
- Onde entra: assimetria do base de 2T27 em diante (P(up) de 55% a 47%, e não perto de 35%, onde estaria só com o viés da (E)).

**(ii) Composição — serviços longos subindo com o cheio parado** · cenário base
- Hoje: serviços 2028 em 4,65 (+0,15 em 4 sem.), 2029 em 4,10 (+0,10); IPCA 2028 −0,05 e 2029 −0,00 (`expc_focus_periodo` (inflação) · 23/10).
- Por que o modelo não vê: a (E) lê só o IPCA cheio de 12 meses, e não a composição esperada (mapa 2.9).
- Efeito: leve para cima, de 3T27 a 1T28, e só se a alta se confirmar em duas pesquisas. Hoje é sinal de painel pequeno.
- Onde entra: assimetria do base nos três últimos trimestres, com peso pequeno.

### 3.3 Da etapa 1 à tese

| Trimestre | Central (modelo, base) | Upside: modelo → com tempero | Downside: modelo → com tempero |
|---|---|---|---|
| 4T26 | 4,16 | 4,17 → 4,52 | 4,16 → 4,00 |
| 1T27 | 3,97 | 4,00 → 4,58 | 3,97 → 3,75 |
| 2T27 | 3,78 | 3,83 → 4,54 | 3,76 → 3,55 |
| 3T27 | 3,67 | 3,74 → 4,55 | 3,65 → 3,44 |
| 4T27 | 3,59 | 3,66 → 4,55 | 3,56 → 3,37 |
| 1T28 | 3,52 | 3,59 → 4,53 | 3,49 → 3,32 |

O limite de cima da faixa é a trajetória sem revisão da própria pesquisa (4,45 a 3,75). O upside com tempero fica 0,07 a 0,78 p.p. acima dela, e o base com E.e1 × 1,2 encosta nela ou a passa. Por isso P(up) vai de 85% a 47%. O limite de baixo fica no ponto aonde o downside com tempero chega (4,05 a 3,25). Como esse cenário exige o choque desfeito e uma âncora mais forte do que a amostra recente mostra, P(down) fica entre 1% e 11%.

## 4. Para os outros agentes

**Respostas às entradas fixas (Parte 4 do mapa).**
- **XE1 (câmbio, consenso do câmbio), em destaque:** a Focus de 23/10 espera 5,05 no fim de 2026 e 5,15 no de 2027 (−0,15 e −0,13 em 4 semanas, `expc_focus_periodo` (câmbio)), IPCA de 5,19 e 4,34 e Selic de 13,25 e 11,75. O câmbio da pesquisa foi revisado na direção da apreciação de 05/10 e é anterior à alta de 9,19% de 26/10. A pesquisa está 0,45 abaixo da PTAX de 26/10.
- **XE2 (política monetária, leitura de ancoragem), em destaque:** a tese da seção 1. Os longos estão desancorados em nível e parados (t+2 +0,75, t+3 +0,50, percentis 82 e 86). A cauda de cima ganhou probabilidade neste ciclo: a implícita de 5 anos subiu 1,20 p.p. em 26/10 e a pesquisa ainda não reagiu. Na (R), a central do modelo implica Selic média de 12,27 no 1T28. Com o tempero do base (E.e1 × 1,2), 12,78.
- **XE3 (inflação, trajetória da Focus 12m e ancoragem):** a mesma de XE2. Central 4,16 → 3,52, com assimetria para cima de +0,84 a +0,36.
- **XE4 (inflação, componentes), em destaque:** serviços 2028 +0,15 e 2029 +0,10 em 4 semanas com o IPCA cheio parado. Alimentação no domicílio em 12m no percentil 99 desde 2021 (6,77), vista como datada (4,00 em 2028). Administrados em 24m no percentil 5 (3,56).
- **XE5 (atividade, consenso de atividade):** PIB de 2026 em 1,80 e 2027 em 1,31 (−0,10 em 4 semanas, −0,29 em 13). Consumo das famílias 2027 −0,21 e investimento 2027 −0,54 em 13 semanas. Trimestral: 1,67 no 4/2026, −0,12 em 4 semanas (`expc_focus_periodo` (PIB)). QPC de 23/09: PIB de 0,20 t/t no 3T26 e no 4T26, hiato de +0,20 no 4T26 e −0,20 no 4T27 (`expc_qpc`). Esses blocos aparecem no meu F. A desocupação não aparece.
- **XE6 (atividade, leituras estruturais):** QPC de 24/06: potencial de 2,00, desemprego neutro de 7,40 (2 anos) e juro neutro de 6,00 (2 anos). Sem dado novo neste ciclo.
- **XE7 (fiscal, consenso fiscal):** consumo do governo em 2,20 em 2026 (+0,05) e 1,14 em 2027 (−0,15 em 4 semanas) (`expc_focus_periodo` (PIB)). O corte fiscal da Focus não está no meu F.
- **XE8 (fiscal, longos com notícia fiscal), em destaque:** na pesquisa, os longos não se moveram até 23/10 (2029 −0,00, 2030 +0,00). No mercado, a implícita de 5 anos subiu 1,20 p.p. e o CDS 18 p.b. em 26/10, a maior alta diária da implícita desde 2006. Se a causa foi fiscal é pergunta de XS8 e do agente web.
- **XE9 (externo, ambiente externo):** câmbio da pesquisa como em XE1. Administrados e alimentação são os componentes que se moveram no curto prazo. QPC de 23/09: 67% veem o ambiente externo menos favorável.

**Pedidos (saídas fixas do mapa e deste ciclo).**
- **XS1 (política monetária):** depois de 26/10, o Copom de 04/11 corta 25 p.b. como a pesquisa esperava em 23/10 (13,50, `expc_focus_copom`), pausa ou sobe? E sua tese de Selic por trimestre. Disso depende a probabilidade do upside de 2T27 em diante: um Copom que não reage ao choque é o cenário de âncora com peso perto de zero.
- **XS2 (política monetária):** o que o Copom disse sobre expectativas na R281 (comunicado e RPM de 24/09). Ele chama os longos (3,50) de desancorados? Que horizonte ele olha? Isso sustenta ou derruba a leitura de Q1.
- **XS3 (política monetária):** o caminho de `meta_12m` e qualquer risco de o CMN mudar a meta ou o regime. Uso 3,00 em todos os trimestres. Uma meta mais alta moveria o ponto de repouso da (E) e mudaria o sentido de "desancoragem" nesta tese.
- **XS4 (política monetária):** a Selic que a curva de 26/10 precifica contra a da pesquisa de 23/10 (DI 1 ano em 14,69% contra Selic esperada de 13,25 no fim de 2026 e 11,75 no de 2027) e o prêmio entre as duas. Disso depende quanto da alta da implícita é prêmio e quanto é expectativa (tempero (ii) 2).
- **XS5 (inflação):** a trajetória do IPCA 12m por trimestre e a composição. O IPCA de 12 meses chega a 5,28 no 4T26 no modelo: é isso que o agente de inflação vê? Quanto da depreciação de 26/10 passa para o 1T27 e o 2T27? A alta de serviços esperada para 2028 e 2029 tem sustentação em serviços subjacentes?
- **XS6 (inflação):** surpresas contra a pesquisa. O IPCA de setembro (0,82, `inflc_agregados`) contra a mediana do QPC para setembro (0,56, `expc_qpc` · 23/09). E o IPCA de outubro, quando sair, contra 0,28 da Focus. Uma surpresa para cima em outubro somada ao choque cambial é o gatilho do upside de 4T26 e 1T27.
- **XS7 (câmbio):** o movimento de 26/10 (PTAX 5,50) é persistente? É idiosincrático ou global? E a tese de PTAX por trimestre. O cenário base do modelo fecha o 4T26 em 5,21. Se o câmbio escrever caminhos de exógena que levem a PTAX para perto de 5,50, o base da rodada 2 sobe e parte do meu upside vira central.
- **XS8 (fiscal):** a leitura de risco fiscal e o caminho do CDS (137 em 26/10, +18 no dia). Houve evento fiscal entre 23 e 26/10? Há risco de dominância fiscal na leitura do agente? Disso depende se a alta da implícita longa é desancoragem por fiscal (mapa 2.3) ou prêmio de evento.
- **XS9 (atividade):** a trajetória do hiato (modelo: 0,13 no 4T26 → −0,51 no 1T28) e se a demanda está pressionando serviços. A pesquisa corta consumo e sobe serviços longos, e eu leio isso como inércia. A atividade vê demanda apertando serviços?
- **XS10 (externo):** commodities agrícolas e petróleo. A alimentação no domicílio esperada para 2026 subiu 0,53 em 4 semanas: há choque externo de alimentos persistente?
- **Ao agente web:**
  1. O que aconteceu entre o fechamento de 23/10 e o de 26/10 que explica PTAX +9,19%, CDS +18 p.b. e implícita de 2 e 5 anos +1,2 p.p. num pregão (resultado do 2º turno da eleição presidencial em 25/10? anúncio de política econômica, de equipe, de regra fiscal?). Tese que depende: a probabilidade do upside em todos os trimestres e o tempero (ii) 1.
  2. O que aconteceu em 03 e 04/10 que levou à apreciação de 05/10 (PTAX −4,55%, implícita de 2 anos −0,65 p.p.). Tese que depende: se o choque de 26/10 é a reversão do de 05/10, que é a história do downside.
  3. Depois de 26/10, alguma autoridade (Fazenda, BC, CMN) ou candidato eleito falou sobre a meta de inflação, o regime de metas, a autonomia do BC ou a diretoria do BC? Tese que depende: XS3 e o peso da meta na (E), tempero (i).
  4. O BC fez intervenção cambial extraordinária ou comunicação fora de reunião em 26 e 27/10? Tese que depende: a duração do tempero (ii) 1.
  5. Revisões públicas de IPCA 2027 e de longo prazo de bancos e consultorias depois de 26/10 (nível B, com nome). Tese que depende: o tamanho da revisão que a Focus ainda não mostra, tempero (ii) 1.

**Como subordinado:** nenhuma exógena neste ciclo.

**Divergências:** rodada 1, sem P. Não escrevi caminho de exógena no JSON (`caminhos` vazio). Os caminhos de CDS e vol das caudas ficam só neste report, como condição.

## 5. Placar

Primeiro ciclo conjunto. O ciclo de 2026-10-02 foi um teste e não é lido. Não há report final anterior cujos trimestres fecharam. Para registro, sem faixa a conferir: o 3T26 fechou em 4,37, média de 65 pesquisas (`expc_focus` (inflação)).

## 6. Sobre o modelo

Ciclo sem literatura. As propostas vêm dos próprios dados e o modelo não muda neste ciclo.

| Fonte | O que sugere (regressor, defasagem, quebra, âncora) | Teste proposto (dado, amostra, que resultado mudaria a especificação) | Por que importa para a tese deste ciclo |
|---|---|---|---|
| Resíduos de um passo da (E) no retrato do ciclo (G `xp_equacao_E`) | Quebra no peso da meta: 7 de 8 resíduos positivos de 4T24 a 3T26, média de +0,35 contra desvio de 0,34 na amostra. Zerar o viés pede peso da meta de ~0,03 em vez de 0,26 | Reestimar a (E) em duas amostras (2002–2016 e 2017–2026) e com peso da meta variável no tempo. Alternativa: trocar a âncora `meta_12m` pela Focus de t+3 (hoje 3,50). Comparar o erro de um passo fora da amostra em 2024T4–2026T3. Se a âncora em t+3 ou o peso recente reduzirem o erro em mais de um terço, mudar a especificação | É a razão da assimetria para cima em todos os trimestres. Com a âncora em 3,50, a central do 1T28 seria mais alta |
| A aritmética do 4T26 (G `xp_trajetoria_pesquisa`) | O primeiro trimestre projetado ignora as pesquisas já feitas nele: o modelo dá 4,16 para um trimestre cujas 16 primeiras pesquisas têm média de 4,52 | Condicionar o primeiro trimestre projetado de `focus_12m` à média parcial já observada (nowcast pela fração de pesquisas), como o modelo já faz ao partir do último trimestre com dado. Medir, nos ciclos passados, o erro do 1º trimestre projetado com e sem esse condicionamento | A central do 4T26 está fora do que a aritmética permite com 99% de probabilidade, e o erro se propaga pela inércia (e1) para 1T27 em diante e, pela (R), para a Selic |
| Choques de câmbio e a (E) (G `xp_historico` (d)) | Não linearidade: a Focus reage pouco à depreciação típica (mediana +0,09) e muito a algumas (+0,8 a +0,96), e a (E) só vê o efeito médio via IPCA | Acrescentar à (E) uma variação trimestral da implícita de 2 anos ou do CDS, ou uma interação com o tamanho da depreciação. Testar se o termo é significativo em 2006–2026 e se tira o resíduo de 1T25 | Decide se o choque de 26/10 entra pelo modelo ou só pelo tempero |

[^1]: Percentil: a posição do valor de hoje entre todas as leituras da série, de 0 (o menor já visto) a 100 (o maior). Na distância à meta, quanto maior, mais longe da meta em relação ao histórico.
[^2]: Focus: pesquisa semanal do Banco Central com cerca de 100 a 140 instituições sobre o que esperam para inflação, PIB, câmbio e Selic. A mediana é o número que se cita.
[^3]: QPC (Questionário Pré-Copom): pesquisa do Banco Central com economistas antes de cada reunião do Copom. Pergunta o que o Copom fará e deveria fazer, projeções e balanço de riscos. O último é de 23/09/2026.
[^4]: Base de 30 dias: a mediana de todas as respostas atualizadas nos últimos 30 dias. Base de 4 dias úteis: só quem respondeu nos últimos quatro dias úteis. Quando a de 4 dias se afasta da de 30, há revisão em curso que a mediana ainda não mostra.
[^5]: Inflação implícita: a inflação que iguala o título prefixado e o título atrelado ao IPCA no mesmo prazo, (1 + taxa prefixada)/(1 + taxa real) − 1. É preço, e não pesquisa: inclui um prêmio pelo risco de a inflação surpreender e efeitos de liquidez. Por isso costuma ficar acima da pesquisa.
[^6]: A variável da tese é a média, no trimestre, das medianas diárias da Focus para o IPCA dos próximos 12 meses, na série "suavizada", que interpola entre as janelas para não saltar quando um mês sai do cálculo. É a variável do Modelo Estrutural, e o placar confere a média, e não o último valor do trimestre.
[^7]: Sobre o processo: rodada 1 sem notícias e sem literatura. A pesquisa mais recente no F é de 23/10, e preços e curvas são de 26/10. Nada do que a pesquisa mostra incorpora o pregão de 26/10.
[^8]: A projeção do Copom no cenário de referência é condicional aos caminhos que ele supõe (a Selic da Focus, câmbio, petróleo). É o que acontece se essas premissas valerem, e não a previsão do Copom.
[^9]: Trajetória sem revisão: a inflação mês a mês que a própria pesquisa de 23/10 espera (medianas mensais até out/2028; o resto de 2028 e o ano de 2029 pelas medianas anuais, com o perfil sazonal de 2028), acumulada em janelas de 12 meses e suavizada pelo dia do mês. A conta reproduz a Focus 12m publicada em 23/10 com erro de 0,01 p.p. (4,52 contra 4,53). É o que a Focus 12m marcaria se nenhum respondente mudasse de ideia.
