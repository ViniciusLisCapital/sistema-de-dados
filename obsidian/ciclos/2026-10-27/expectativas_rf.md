# Report — expectativas · ciclo 2026-10-27 · report final

Dados até: Focus[^2] de 23/10/2026; curvas, PTAX e CDS de 26/10/2026; QPC de 23/09/2026; notícias publicadas até 27/10/2026[^7] · Horizontes: 4T26 a 1T28, com a variável medida como a **média das pesquisas do trimestre** da Focus IPCA 12 meses à frente, suavizada, base de 30 dias, mediana (a `focus_12m` do Modelo Estrutural)[^6] · Central: a do P2

## 1. Tese

| Variável | Trimestre | Central | Base: faixa · P | Upside: limite · P | Downside: limite · P | P(up) − P(down) |
|---|---|---|---|---|---|---|
| Focus IPCA 12m, média do trimestre (% a.a.) | 4T26 | 4,17 | 4,05 a 4,45 · 14% | acima de 4,45 · 85% | abaixo de 4,05 · 1% | +0,84 |
| | 1T27 | 4,00 | 3,80 a 4,15 · 26% | acima de 4,15 · 70% | abaixo de 3,80 · 4% | +0,66 |
| | 2T27 | 3,82 | 3,60 a 3,95 · 35% | acima de 3,95 · 58% | abaixo de 3,60 · 7% | +0,51 |
| | 3T27 | 3,71 | 3,50 a 3,90 · 39% | acima de 3,90 · 52% | abaixo de 3,50 · 9% | +0,43 |
| | 4T27 | 3,63 | 3,40 a 3,90 · 41% | acima de 3,90 · 48% | abaixo de 3,40 · 11% | +0,37 |
| | 1T28 | 3,55 | 3,30 a 3,75 · 41% | acima de 3,75 · 47% | abaixo de 3,30 · 12% | +0,35 |

- **Como a faixa foi desenhada.** O limite de cima é a trajetória que a própria Focus de 23/10 implica se ninguém revisar: 4,47; 4,17; 3,93; 3,88; 3,87; 3,70 (medianas mensais, trimestrais e anuais de `expc_focus_periodo` (inflação) · 23/10)[^9]. Upside quer dizer a pesquisa revisar para cima a partir dela mesma. O limite de baixo fica onde chega o cenário de downside com tempero (4,01; 3,77; 3,57; 3,48; 3,40; 3,34, seção 3.3).
- **Upside, ruim para o Brasil (desancoragem): acima de 4,45 no 4T26 e de 3,75 a 3,95 de 2T27 em diante.** O caminho é o prêmio que os preços cobraram em 26/10, depois da reeleição, se aprofundar porque as decisões fiscais de 2027 não entregam o que o governo prometeu. Na etapa 1, com as caudas que os principais escreveram (CDS de 170 a 210 p.b., NTN-B de 10 anos de 8,15% a 9,10%, volatilidade de 24% caindo a 15%), a PTAX do modelo vai a 5,64–5,88 e a Focus fica em 4,18 no 4T26 e 3,61 no 1T28. Na etapa 2, com o peso da meta na (E) caindo de 0,26 para 0,09 (E.e1 × 1,2 e E.e2 × 1,3, os dois dentro do posterior), ela fica entre 4,26 e 4,45 nos seis trimestres, 1,3 a 1,5 p.p. acima da meta.
- **Downside, bom para o Brasil (convergência mais rápida): abaixo de 4,05 no 4T26 e de 3,30 no 1T28.** O caminho é a resposta fiscal anunciada depois da eleição convencer e o prêmio voltar para perto de onde estava antes do 2º turno. Na etapa 1 (CDS de 122 a 106 p.b., NTN-B de 7,36% a 6,95%, volatilidade de 13% a 12%), a PTAX do modelo fica em 5,28–5,43 e a Focus vai de 4,17 a 3,52. Na etapa 2, com E.e1 × 0,8, de 4,01 a 3,34. No 4T26 isso é remoto pela aritmética das pesquisas já feitas: 1%.
- **A tese em uma frase:** a expectativa de 12 meses converge mais devagar do que o P2 projeta. O P2 a põe em 4,17 no 4T26 e 3,55 no 1T28, mas a pesquisa de 23/10, sem nenhuma revisão, já fica 0,11 a 0,30 p.p. acima em todos os trimestres, e o choque de 26/10, causado pela reeleição de Lula, é do tipo que a pesquisa costuma seguir: nas oito vezes desde 2006 em que a inflação implícita de 2 anos subiu 0,60 p.p. ou mais em uma semana, a Focus de 12 meses subiu em seis nos 45 dias úteis seguintes. O risco de cima predomina nos seis trimestres (P(up) − P(down) de +0,84 a +0,35), e o sinal que o confirmaria é a Focus de 2028 passar de 4,00.

## 2. Argumentação

### O fato do ciclo: a eleição de 25/10, e o que os preços fizeram depois

**A causa do pregão de 26/10 é o resultado do 2º turno.** Lula foi reeleito em 25/10, e "o mercado vinha tratando a vitória de Flávio como a possibilidade de uma virada na política fiscal do governo", segundo a CNN Brasil (CNN Brasil · 25/10 · nível A). No pregão seguinte os juros futuros longos subiram até 182 p.b. e o Tesouro cancelou os leilões da semana (InfoMoney/Estadão Conteúdo · 26/10 · nível A). O pregão de 05/10 foi o espelho: depois do 1º turno, com Flávio Bolsonaro à frente, a leitura foi "de redução do prêmio de risco dos ativos brasileiros" (Agência Brasil · 05/10 · nível A).

| Série | 02/10 | 05/10 | 23/10 | 26/10 |
|---|---|---|---|---|
| PTAX venda (`cmb_ptax`) | 5,22 | 4,99 | 5,04 | 5,50 |
| CDS 5 anos, p.b. (`cmb_risco_pais`) | — | — | 119 | 137 |
| Inflação implícita 2 anos, % (`br_interest_rate`) | 5,89 | 5,24 | 5,46 | 6,69 |
| Inflação implícita 5 anos, % (`br_interest_rate`) | — | — | 5,60 | 6,81 |

Fonte: as tabelas indicadas · datas na coluna. A alta da PTAX em 26/10 (+9,2%) é a 2ª maior diária desde fev/1999, e as das implícitas de 2 e 5 anos (+1,2 p.p. cada) são as maiores diárias desde 2006. Em 5 dias úteis até 26/10 a implícita de 2 anos subiu 1,25 p.p., mais que em qualquer semana desde 2006: a maior anterior foi +1,12 em 24/10/2008 (`br_interest_rate`).

O que isso diz para as expectativas: a incerteza do evento se resolveu em 25/10, e o prêmio subiu. O que está nos preços de 26/10 é o preço do resultado, que dura o mandato, e não de uma dúvida que passa. O agente fiscal lê o mesmo, como prêmio de evento com fundamento fiscal: a dívida sobe cerca de 5 p.p. do PIB por ano e o primário está 4,9 p.p. abaixo do que a estabiliza (fiscal_r2).

**O dia seguinte devolveu parte, e não o todo.** Em 27/10 o dólar fechou em R$ 5,350, queda de 0,97% (Poder360 · 27/10 · nível B), e os DIs tiveram "baixas firmes", com o de janeiro de 2028 em 14,41% (InfoMoney/Reuters · 27/10 · nível B). O Tesouro Prefixado 2029 caiu 47 p.b., de 15,26% para 14,79%, mas o IPCA+ 2040 subiu de 7,29% para 7,53%, contra 7,22% em 02/10 (InfoMoney · 27/10 · nível B), com o Tesouro recomprando NTN-B de 2030 a 2045 (Agência Brasil · 27/10 · nível A). A perna nominal devolveu e a real longa subiu, as duas na direção de uma implícita menor. Os vencimentos das matérias não casam, e por isso o tamanho da devolução da implícita não sai delas. O F não tem preço depois de 26/10, e a Focus de 23/10 continua sendo a última pesquisa: nada nela vê a eleição.

**O governo respondeu com promessa, sem conteúdo ainda.** O ministro da Fazenda, Dario Durigan, disse que vai "buscar o centro da meta de maneira formal" por projeto de lei complementar (CNN Brasil e Poder360 · 27/10 · nível A), a ser apresentado "ainda em 2026", alterando "a legislação ou, se necessário, a Constituição" (Poder360 · 26/10 · nível B). O conteúdo e o envio não aparecem nas notícias até 27/10.

### Q1 — As expectativas estão ancoradas na meta?

Não. A distância à meta é positiva em todos os horizontes e está no quinto superior da história em todos. Nos longos ela estava parada até 23/10:

| Horizonte | Expectativa − meta (p.p.) | Δ desde 02/10 | Pctl hist.[^1] | Pctl 10a | Maior da série |
|---|---|---|---|---|---|
| 12 meses à frente | +1,53 | −0,06 | 79 | 77 | +8,35 (19/12/2002) |
| ano corrente (2026) | +2,19 | +0,18 | 78 | 77 | +9,06 (31/12/2002) |
| t+1 (2027) | +1,34 | +0,04 | 84 | 87 | +7,00 (13/12/2002) |
| t+2 (2028) | +0,75 | −0,05 | 82 | 83 | +2,50 (31/12/2002) |
| t+3 (2029) | +0,50 | −0,01 | 86 | 87 | +1,50 (09/12/2002) |

Fonte: "Desancoragem", `expc_focus` e `expc_focus_periodo` (inflação) · 23/10.

- **Os longos estão desancorados em nível e, até 23/10, parados.** t+2 e t+3 estão acima de 82% e de 86% das leituras desde 2000. As medianas de 2029 e 2030 são 3,50, meio ponto acima da meta, e não se moveram em quatro semanas (`expc_focus_periodo` (inflação) · 23/10). O Copom tem a mesma leitura: segundo o agente de política monetária, disse que as expectativas "permanecem acima da meta de inflação em todos os horizontes", julga a ancoragem dois a três anos à frente e registrou a Focus de 2028 indo de 3,69% para 3,80% como "desancoragem adicional" (ata e RPM da 281ª). Desde então 2028 voltou a 3,75.
- **O que mudou é a chance de os longos saírem do lugar.** Depois de depreciações de 5% ou mais em 21 dias úteis, a mediana de t+2 ficou parada nos 45 dias úteis seguintes (variação menor que 0,05 p.p.) em 60% dos 45 episódios desde 2001, e subiu 0,25 p.p. ou mais em só 7% deles (`cmb_ptax` e `expc_focus_periodo` (inflação), 2001–2026). Depois de altas de 0,60 p.p. ou mais da implícita de 2 anos em 5 dias úteis, t+2 subiu em mediana 0,20 p.p. em 45 dias úteis, e 0,25 ou mais em quatro dos oito episódios (tabela em Q3). O choque de 26/10 é dos dois tipos ao mesmo tempo. Se a Focus de 2028 passar de 4,00, Q1 deixa de ser "desancorada e parada" e passa a "desancorando".
- **A medida de mercado desses horizontes já saltou.** A implícita de 5 anos está 3,8 p.p. acima da meta, no percentil 97 da história e 99 dos 10 anos, e a de 10 anos 3,6 p.p., percentis 93 e 95 (`br_interest_rate` · 26/10).
- **A cauda de respondentes nos longos segue acima.** Em 2029 a média passa a mediana em 0,12 p.p. (3,62 contra 3,50), no percentil 71 desde 2000; em 2028 as duas coincidem (`expc_focus_periodo` (inflação) · 23/10).
- **Os curtos se movem por choque já visível.** 2026 subiu de 5,01 para 5,19 desde 02/10, com desvio-padrão de 0,15 entre 142 respondentes (`expc_focus_periodo` (inflação) · 23/10): é inflação realizada entrando no ano, e não crença.

### Q2 — O que move as expectativas, e é nível ou ruído?

**No horizonte de 12 meses, o movimento das quatro semanas até 23/10 é aritmética, e não revisão.** A Focus 12m caiu 0,11 p.p., de 4,64 em 25/09 para 4,53, com a base de 4 dias úteis[^4] só 0,02 p.p. acima da de 30 dias, média igual à mediana e desvio-padrão de 0,47, percentil 73 (`expc_focus` (inflação) · 23/10). A queda veio da janela: a série sem suavização caiu de 4,88 para 4,48 entre 08 e 09/10, quando um mês alto saiu do cálculo (`expc_focus` (inflação) · 08 e 09/10). Nada disso é reação à eleição, que veio depois.

**Por componente, a pressão de curto prazo é de choques datados. A de longo prazo está em serviços.**

| Componente | 12m | Δ 13 sem. (12m) | Pctl 12m (desde 2021) | 24m (Δ 4 sem.) | 2027 (Δ 4 sem.) | 2028 (Δ 4 sem.) | 2029 (Δ 4 sem.) |
|---|---|---|---|---|---|---|---|
| IPCA | 4,53 | +0,35 | 42 | 3,87 (−0,06) | 4,34 (+0,03) | 3,75 (−0,05) | 3,50 (0,00) |
| Livres | 4,80 | +0,27 | 66 | 4,00 (+0,02) | 4,52 (+0,04) | 3,90 (0,00) | 3,66 (+0,10) |
| Administrados | 4,10 | +0,60 | 45 | 3,56 (−0,10) | 3,99 (+0,17) | 3,63 (+0,01) | 3,50 (0,00) |
| Serviços | 5,20 | −0,06 | 40 | 4,81 (+0,02) | 5,16 (+0,08) | 4,65 (+0,15) | 4,10 (+0,10) |
| Bens industrializados | 2,60 | −0,25 | 31 | 2,68 (−0,08) | 2,71 (−0,02) | 2,80 (0,00) | 2,98 (0,00) |
| Alimentação no domicílio | 6,77 | +1,21 | 99 | 4,49 (+0,17) | 5,76 (+0,10) | 4,00 (0,00) | 4,00 (0,00) |

Fonte: `expc_focus` (inflação) e `expc_focus_periodo` (inflação) · 23/10.

- **Alimentação é choque datado, mas já passa para o segundo ano.** Em 12 meses ela está no percentil 99 desde 2021; em 2026 subiu 0,53 p.p. em quatro semanas, para 7,38, e a pesquisa a vê voltar a 4,00 em 2028 e 2029. A causa que o agente de inflação vê é de horta, e no atacado de setembro a batata subiu 32,9%, a cebola 29,3% e o tomate 48,9%, com chuva atrapalhando colheita e plantio (CNN Brasil · 27/10 · nível B). O agente externo não vê choque de alimentos em dólar: o IC-Br agropecuária cede de 204 para 197 até o 1T28 no caminho dele. Mas a alimentação de 24 meses subiu 0,17 p.p. em quatro semanas, para 4,49, percentil 82: parte do choque já foi posta em 2027 (5,76).
- **Administrados de 2027 sobem com duas forças contrárias à frente.** 2027 subiu 0,17 p.p. em quatro semanas, para 3,99. A Abicom diz que, com Lula reeleito, a Petrobras reajustará "de maneira lenta e gradual" preços que estão "muito defasados" (CNN Brasil/Estadão Conteúdo · 26/10 · nível B), o que espalha combustíveis por 2027, e o agente externo dá 25% de o bloqueio em Hormuz não se resolver. Durigan disse que manter a subvenção aos combustíveis em 2027 "deve ser a proposta do presidente" se o Brent seguir alto (Poder360 · 23/10 · nível B), o que segura a bomba e adia o custo. As duas são falas, e não decisões, e o agente fiscal confirmou que não há valor, prazo nem base legal para a subvenção de 2027.
- **Serviços é a exceção, e é o sinal deste ciclo na composição.** Serviços de 2028 subiram 0,15 p.p. e de 2029 0,10 p.p. em quatro semanas, e os livres de 2029 0,10, enquanto o IPCA de 2028 caiu 0,05 e o de 2029 não se moveu (`expc_focus_periodo` (inflação) · 23/10). O agente de inflação diz que a Focus de serviços de 2028 tem sustentação: o modelo dá ~4,7% para serviços no 1T28, com os subjacentes a 5,32% e subindo. Mas o painel de serviços é menor (65 respondentes em 2028, contra 124 no IPCA): duas pesquisas seguidas com serviços de 2029 acima de 4,10 confirmariam.
- **A pesquisa espera menos demanda, então serviços longos são inércia e salário.** Ela cortou o consumo das famílias de 2027 em 0,40 p.p. e o investimento em 0,54 em 13 semanas (para 1,20 e 1,06), e o PIB de 2027 em 0,29, para 1,31 (`expc_focus_periodo` (PIB) · 23/10). O agente de atividade não vê demanda apertando serviços de forma ampla: só os serviços às famílias (percentil 100 em 10 anos) e o mercado de trabalho estão quentes, e o hiato vira negativo no 1T27. As duas leituras convergem: serviços de 2028–2029 sobem na pesquisa por inércia e salário, e não por demanda.

### Q3 — Pesquisa, mercado e Copom: onde divergem, e o que isso diz da credibilidade

| Fonte | Horizonte | IPCA (%) | Data |
|---|---|---|---|
| Copom, cenário de referência[^8] | 4 trimestres até 1T28 | 3,2 | 24/09 (`pm_copom_projecoes`) |
| QPC, mediana[^3] | 4 trimestres até 1T28 | 4,00 (p25 a p75: 3,77 a 4,20) | 23/09 (`expc_qpc`) |
| Focus, medianas trimestrais 2T27 a 1T28 compostas | 4 trimestres até 1T28 | 4,03 | 23/10 (`expc_focus_periodo` (inflação)) |
| Focus 24m | 24 meses | 3,87 | 23/10 (`expc_focus` (inflação)) |
| Inflação implícita 1 ano[^5] | 1 ano | 7,87 | 26/10 (`br_interest_rate`) |
| Inflação implícita 2 anos | 2 anos | 5,46 em 23/10 → 6,69 em 26/10 | `br_interest_rate` |
| Inflação implícita 5 anos | 5 anos | 5,60 em 23/10 → 6,81 em 26/10 | `br_interest_rate` |

- **Pesquisa contra Copom: 0,8 p.p. no horizonte relevante, com a mesma Selic.** A projeção de 3,2% usa a Selic da Focus, e com essa Selic a Focus espera 4,0% e o QPC 4,0% para os quatro trimestres até 1T28. É um déficit de credibilidade medido, e anterior à eleição. O agente de política monetária espera que o Copom mantenha 13,75% em 04/11 (77%) e em 09/12 (57%), com 32% de a Selic estar acima de 13,75% depois de dezembro: para a credibilidade, é a resposta que um déficit desse tamanho pede.
- **Pesquisa contra mercado: o mercado saiu na frente, e a pesquisa costuma seguir.** Com a curva de 26/10 contra a Focus de 23/10, a implícita de 2 anos fica 2,8 p.p. acima da Focus 24m (percentil 96 desde 2021), e a de 1 ano 3,3 p.p. acima da Focus 12m, percentil 100 desde 2006 (`br_interest_rate` e `expc_focus` (inflação)). A implícita carrega prêmio de risco de inflação, o vértice de 1 ano tem distorção de carregamento da NTN-B curta, e a curva de 26/10 se formou com o Tesouro fora dos leilões. Por isso não leio o nível como expectativa. Leio o que a pesquisa fez depois de saltos parecidos do preço:

| Episódio | Implícita 2 anos em 5 du (p.p.) | Focus 12m em 45 du | IPCA t+1 em 45 du | IPCA t+2 em 45 du |
|---|---|---|---|---|
| 16/08/2007 | +0,93 | +0,14 | +0,10 | 0,00 |
| 22/10/2008 | +1,11 | −0,26 | 0,00 | 0,00 |
| 04/09/2015 | +0,83 | +1,07 | +0,92 | +0,30 |
| 21/01/2016 | +0,64 | −0,46 | +0,47 | +0,49 |
| 21/10/2021 | +0,70 | +0,47 | +0,82 | +0,11 |
| 04/03/2022 | +0,68 | +0,31 | +0,62 | +0,13 |
| 11/11/2022 | +0,65 | +0,24 | +0,46 | +0,26 |
| 30/12/2024 | +0,69 | +0,36 | +0,66 | +0,38 |
| 26/10/2026 | +1,25 | ? | ? | ? |

Fonte: `br_interest_rate`, `expc_focus` (inflação) e `expc_focus_periodo` (inflação), 2006–2026; episódios separados por pelo menos 63 dias úteis; t+1 e t+2 fixados no ano do episódio. A Focus de 12 meses subiu em seis dos oito episódios (mediana +0,28 p.p.), o IPCA de t+1 em sete (mediana +0,54) e o de t+2 em seis (mediana +0,20). E isso com a implícita devolvendo toda a alta, na mediana: 45 dias úteis depois, ela estava abaixo de onde estava antes da semana do salto. A pesquisa seguiu a direção mesmo quando o preço voltou, o que torna a devolução parcial de 27/10 um argumento fraco contra a revisão. Depois de depreciações de 5% ou mais sem essa condição, o IPCA de t+1 subiu 0,26 p.p. ou mais em 30 dias úteis em só 16% dos 45 episódios, e nos cinco de 8% ou mais a mediana de t+1 e de t+2 ficou parada (`cmb_ptax` e `expc_focus_periodo` (inflação), 2001–2026). A pesquisa reage ao preço da inflação, e não ao câmbio em si. Mas são oito episódios, o F não diz o que houve em cada um, e o mais parecido em tamanho, 22/10/2008, foi o único em que nem a Focus de 12 meses nem os anos subiram.
- **A pesquisa contra ela mesma: espera a Selic chegar ao neutro com a inflação acima da meta.**

| Ano | Selic fim de ano | IPCA do ano | IPCA − meta | Juro real implícito na pesquisa |
|---|---|---|---|---|
| 2026 | 13,25 | 5,19 | +2,19 | 7,66 |
| 2027 | 11,75 | 4,34 | +1,34 | 7,11 |
| 2028 | 10,00 | 3,75 | +0,75 | 6,02 |
| 2029 | 10,00 | 3,50 | +0,50 | 6,28 |

Fonte: "A pesquisa contra ela mesma", `expc_focus_periodo` (Selic e inflação) · 23/10. Em 2028 o juro real esperado, 6,0%, é o neutro de 2 anos do QPC (6,0%, `expc_qpc` · R279, 24/06) com a inflação 0,75 p.p. acima da meta, e nas quatro semanas até 23/10 a pesquisa cortou a Selic de 2028 em 0,50 p.p. e a inflação de 2028 em só 0,05: o sinal de credibilidade do mapa (2.8) na direção de um Copom que aceita inflação acima da meta. A Selic que a pesquisa esperava para 04/11 (13,50, `expc_focus_copom` · 23/10) está abaixo do que o agente de política monetária espera (manter 13,75), e a curva de 26/10 está 23 a 403 p.b. acima da pesquisa de 04/11 a dez/2027, a maior parte prêmio, segundo ele. O teste das próximas pesquisas é o par: Selic esperada subindo com a inflação esperada parada seria credibilidade; as duas subindo, desancoragem.
- **O que as autoridades disseram.** Lula (presidente da República) disse, na véspera da votação: "Quero que o Banco Central baixe o juro." (Poder360 · 24/10 · nível B). Gabriel Galípolo (presidente do BC) disse em 27/10 que "Meu mandato vai até o final de 2028" (CNN Brasil · 27/10 · nível B) e não comentou o resultado da eleição, a intervenção cambial nem a próxima decisão do Copom (Poder360 · 27/10 · nível B). Em duas rodadas de busca, o agente web não achou proposta de mudar a meta de inflação, o regime de metas ou a lei de autonomia do BC. A meta de 3,00% não está em discussão nos arquivos deste ciclo. O que está em dúvida é o empenho em alcançá-la, que é o que o peso da meta na (E) mede, e o agente de política monetária põe 5% num Copom que volta a cortar com a PTAX acima de 5,40 sob a pressão de quem foi reeleito pedindo juro mais baixo.

### Q4 — O cenário para a Focus 12m: por que a central, por que a distribuição

**A central é a do P2, e o modelo a puxa para baixo pela meta, não por inflação menor.** No 4T26 a (E) dá 4,17 como soma de três termos: inércia, 0,581 × 4,37 (a média do 3T26) = 2,54; IPCA de 12 meses, 0,162 × 5,34 (o do 4T26 no P2) = 0,86; meta, 0,257 × 3,00 = 0,77 (Modelo Estrutural, P2). Contra ficar parada em 4,37, a meta puxa −0,35 p.p. e a inflação empurra +0,16. A expectativa cai com a inflação de 12 meses do modelo subindo de 4,58% para 5,34%. Daí em diante ela segue a inflação do modelo, que desce a 4,14% no 1T28, e a meta, e chega a 3,55. O P2 fica 0,01 a 0,02 p.p. abaixo do P1 de 3T27 em diante porque o CDS do fiscal cede a 125 p.b. no 1T28, e com ele a PTAX e o IPCA de 12 meses do modelo. Como fato do modelo, a (R) reage a esse desvio, e a Selic média do P2 vai de 13,48% no 4T26 a 12,18% no 1T28.

**O que o modelo erra, e por quê.** Quatro evidências, todas na mesma direção:
1. **A aritmética do 4T26.** As 16 pesquisas já feitas no trimestre têm média de 4,52 (`expc_focus` (inflação) · até 23/10). Para fechar em 4,17, as 46 a 49 restantes teriam de marcar em média 4,05, quase meio ponto abaixo de 23/10. Uma queda dessas na média das 46 pesquisas seguintes aconteceu em 3,1% dos dias desde 2001 (`expc_focus` (inflação), 2001–2026), e agora com o real 9% mais fraco e a eleição decidida contra a leitura do mercado.
2. **A trajetória da própria pesquisa.** Sem nenhuma revisão[^9], a Focus 12m dá 4,47; 4,17; 3,93; 3,88; 3,87; 3,70, isto é 0,30; 0,17; 0,11; 0,17; 0,24 e 0,15 p.p. acima do P2. O modelo exige que os respondentes revisem para baixo a cada trimestre só para chegar à central.
3. **O viés recente da (E).** Nos 8 trimestres de 4T24 a 3T26, o resíduo de um passo foi positivo em 7, com média de +0,35 p.p., e o do 3T26 (+0,50) está no percentil 91 da amostra (Modelo Estrutural, retrato do ciclo). Os longos parados em 3,50 dizem o mesmo: a âncora de fato dos respondentes é 3,50, e não 3,00.
4. **A pesquisa segue saltos do preço da inflação** (tabela de Q3), e o de 26/10 é o maior desde 2006. A (E) não tem termo para isso.

A âncora da (E) é imposta: o modelo não produz desancoragem além da trajetória da inflação (mapa 2.1). Essa leitura entra como tempero e não move a central. Os agentes de política monetária e de inflação leram o mesmo e levaram o efeito do tempero às suas distribuições.

**Por que a distribuição é tão assimétrica para cima.** Quatro forças. O tempero (i) no base: só com E.e1 × 1,2, dentro do posterior, a trajetória do P2 vai a 4,33; 4,25; 4,11; 4,03; 3,96; 3,88, acima do limite de cima do 1T27 em diante. A revisão que a pesquisa ainda não mostra, com a causa do choque conhecida (tempero (ii) 1). O mercado à frente da pesquisa, com tamanho medido (tempero (ii) 2). E o balanço de riscos do QPC de 23/09, com 60% vendo risco de alta para o IPCA de 2027 e 5% de baixa (`expc_qpc`).

Contra o upside, três coisas. O Copom deve reagir: um Copom que para de cortar no meio do choque é a âncora funcionando. O governo respondeu ao preço em um dia, com a promessa de mirar o centro da meta fiscal. E os preços devolveram parte do choque em 27/10, e bens industrializados, o componente mais sensível ao câmbio, caíam até 23/10 (2,60 em 12 meses, −0,25 em 13 semanas).

A assimetria é maior no 1T27 e no 2T27, onde a evidência de reação da pesquisa ao preço pesa mais, e cai com o horizonte (+0,84 → +0,35) porque o 4T26 é quase todo aritmética já dada, e o 1T28 depende de inflação que ainda não aconteceu e de um Copom que, no horizonte mais longo, tem mais tempo para reagir.

O downside, bom, tem 1% a 12%. Ele precisa de o prêmio voltar para perto do nível de antes da eleição e de uma âncora mais forte que a mediana do posterior, e a amostra recente diz o contrário.

### Olhado, sem sinal

- Focus 24m, base de 4 dias contra 30 dias · −0,01 p.p. (3,87 contra 3,87, `expc_focus` (inflação) · 23/10) · as respostas frescas não divergiam antes da eleição · diria algo se a de 4 dias passar a de 30 dias em mais de 0,10 nas pesquisas de depois de 26/10.
- Desvio-padrão de 2027 · 0,43, de 3,25 a 6,00, 142 respondentes (`expc_focus_periodo` (inflação) · 23/10) · dispersão normal para t+1 · diria algo se o desvio subir com a mediana parada.
- IPCA trimestral da Focus · 4/2026 em 1,19 (−0,05 em 4 sem.), 1/2027 em 1,63 (+0,10) (`expc_focus_periodo` (inflação) · 23/10) · já dentro da trajetória sem revisão · diria algo se 1/2027 subir junto com o câmbio da pesquisa.
- Selic por reunião · R7/2026 em 13,50, R1/2027 em 13,00 (−0,50 em 4 sem.) (`expc_focus_copom` · 23/10) · o caminho do juro é do agente de política monetária · entra em Q3 como o par Selic–inflação das próximas pesquisas.
- Variáveis estruturais do QPC · neutro de 5 anos 5,50, PIB potencial 2,00 (`expc_qpc` · R279, 24/06) · de junho · diria algo se o próximo QPC subir o neutro.
- Exportação e importação da Focus · 2027 em 3,00 e 1,96 (`expc_focus_periodo` (PIB) · 23/10) · não chegam à inflação esperada por canal do mapa · diria algo num choque externo.
- IPCA-15 de outubro · 0,32 (`inflc_agregados` · out/2026) contra a mediana mensal da Focus para outubro de 0,28 (`expc_focus_periodo` (inflação) · 23/10) · surpresa pequena · diria algo se o IPCA cheio de outubro passar de 0,40.
- Galípolo sobre a escala 6x1: "a gente vai esperar a implementação para saber se precisa agir" (InfoMoney · 27/10 · nível B) · a página traz só a manchete, sem ligar a fala a inflação ou à reunião de 04/11 · diria algo se fosse sobre a resposta do Copom ao choque.

## 3. Premissas

### 3.1 Etapa 1 — o modelo

**Cenários.**
- **Base:** os caminhos do P2, que são os dos principais depois da moderação da rodada 2. O prêmio de 26/10 fica em parte: o CDS sobe a 142 p.b. no 1T27 e cede a 125 no 1T28; a NTN-B de 10 anos fica perto de 8,0% no 1T27 e cede a 7,70% no 1T28, porque a alta de juros que a curva cobra nos dois primeiros anos não vem se o Copom não subir; a volatilidade cambial cai de 17% a 13,5%; o externo segue o caminho do agente externo.
- **Upside:** as promessas fiscais não se cumprem e as decisões de 2027 afrouxam a política, com o risk-off do agente externo somado. Os caminhos de cauda são os que os principais escreveram: fiscal (CDS e NTN-B) e câmbio (volatilidade).
- **Downside:** a resposta fiscal convence e o prêmio volta para perto de onde estava antes da eleição. Caminhos de cauda do fiscal e do câmbio.

**Caminhos das exógenas.** Nenhuma é deste agente. Os de upside e downside são a condição das caudas, escritos pelos principais nos reports da rodada 2, e ficam só neste report (`caminhos` vazio no JSON).

| Exógena | Hoje (valor · tabela · data) | Cenário | 4T26 | 1T27 | 2T27 | 3T27 | 4T27 | 1T28 |
|---|---|---|---|---|---|---|---|---|
| Meta 12 meses (`meta_12m`, %) · principal: política monetária | 3,00 · `inflc_meta` · 2026 | todos | 3,00 | 3,00 | 3,00 | 3,00 | 3,00 | 3,00 |
| CDS 5 anos (`fiscal`, p.b.) · principal: fiscal | 137 · `cmb_risco_pais` · 26/10 | base (P2) | 140 | 142 | 139 | 135 | 130 | 125 |
| | | upside | 170 | 205 | 210 | 205 | 198 | 190 |
| | | downside | 122 | 115 | 112 | 110 | 108 | 106 |
| NTN-B 10 anos (`rr_10a`, %) · principal: fiscal | 8,05 · `br_interest_rate` · 26/10 | base (P2) | 7,72 | 7,95 | 7,90 | 7,80 | 7,75 | 7,70 |
| | | upside | 8,15 | 8,90 | 9,10 | 9,10 | 9,00 | 8,90 |
| | | downside | 7,36 | 7,30 | 7,15 | 7,05 | 7,00 | 6,95 |
| Volatilidade implícita do dólar (`vol`, %) · principal: câmbio | fora do meu F (o P2 segura 12,19 no 3T26) | base (P2) | 17,0 | 15,5 | 14,5 | 14,0 | 13,5 | 13,5 |
| | | upside | 24,0 | 21,0 | 18,0 | 16,0 | 15,0 | 15,0 |
| | | downside | 13,0 | 12,5 | 12,0 | 12,0 | 12,0 | 12,0 |
| Inflação dos EUA no trimestre (`infl_us`, %) · principal: externo | fora do meu F | todos (P2) | 0,86 | 0,61 | 0,61 | 0,65 | 0,63 | 0,65 |
| Fed Funds (`ffr`, %) · principal: externo | fora do meu F | todos (P2) | 4,13 | 4,13 | 4,13 | 4,13 | 4,13 | 3,88 |
| Dólar contra emergentes (`dxy_em`) · principal: externo | fora do meu F | todos (P2) | 130,5 | 131,0 | 130,5 | 130,0 | 129,5 | 129,0 |
| S&P 500 (`sp500`) · principal: externo | fora do meu F | todos (P2) | 7.750 | 7.900 | 8.050 | 8.200 | 8.350 | 8.500 |
| IC-Br em dólar (`icbr_usd`) · principal: externo | fora do meu F | todos (P2) | 206,2 | 202,6 | 201,0 | 199,9 | 199,0 | 198,3 |
| IC-Br agropecuária em dólar (`icbr_agr_usd`) · principal: externo | fora do meu F | todos (P2) | 203,9 | 200,9 | 199,3 | 198,4 | 197,8 | 197,4 |
| IC-Br metal em dólar (`icbr_met_usd`) · principal: externo | fora do meu F | todos (P2) | 331,7 | 330,0 | 330,0 | 328,7 | 327,3 | 325,7 |

O externo fica no caminho base nas três: as caudas desta tese são domésticas, e o risk-off do agente externo já está na cauda de alta do CDS do fiscal.

**Saída do modelo** (Modelo Estrutural, central [faixa de 90% do posterior dos pesos, que não é intervalo de previsão]).

| Variável | Cenário | 4T26 | 1T27 | 2T27 | 3T27 | 4T27 | 1T28 |
|---|---|---|---|---|---|---|---|
| Focus 12m | base (P2) | 4,17 [4,07; 4,28] | 4,00 [3,85; 4,16] | 3,82 [3,65; 4,01] | 3,71 [3,55; 3,92] | 3,63 [3,47; 3,84] | 3,55 [3,39; 3,77] |
| | upside | 4,18 | 4,01 | 3,85 | 3,77 | 3,69 | 3,61 |
| | downside | 4,17 | 3,99 | 3,80 | 3,69 | 3,60 | 3,52 |
| IPCA 12m | base · upside · downside | 5,34 · 5,36 · 5,32 | 4,95 · 5,04 · 4,89 | 4,46 · 4,62 · 4,38 | 4,48 · 4,68 · 4,39 | 4,32 · 4,52 · 4,24 | 4,14 · 4,29 · 4,09 |
| PTAX fechamento | base · upside · downside | 5,43 · 5,64 · 5,28 | 5,51 · 5,87 · 5,35 | 5,52 · 5,88 · 5,36 | 5,50 · 5,83 · 5,37 | 5,51 · 5,82 · 5,40 | 5,53 · 5,83 · 5,43 |
| Selic média | base · upside · downside | 13,48 · 13,91 · 13,12 | 13,37 · 14,33 · 12,72 | 13,04 · 14,26 · 12,28 | 12,69 · 14,03 · 11,92 | 12,43 · 13,73 · 11,65 | 12,18 · 13,46 · 11,40 |

A história econômica: no upside, a PTAX do modelo fica R$ 0,21 a 0,36 acima do base e o IPCA de 12 meses 0,03 a 0,20 p.p. acima, mas a Focus sobe só 0,00 a 0,06 p.p. A expectativa recebe o choque só pela inflação, com peso 0,16, e a regra de juros, que segue a NTN-B de 10 anos, leva a Selic a 14,33% no 1T27. O que o modelo erra está em Q4: a pesquisa reage ao preço da inflação além do que passa pelo IPCA, e a âncora pesa menos do que a mediana do posterior. As duas coisas são tempero.

### 3.2 Etapa 2 — o tempero qualitativo

**(i) E.e1 (inércia da expectativa) — efeito mais forte que o estimado** · cenário base
- Coeficiente: estimado 0,581, intervalo de 90% do posterior de 0,452 a 0,710. Multiplicador × 1,2 (0,697, percentil 92): **dentro** do intervalo. O peso da meta cai de 0,257 para 0,141.
- Efeito: Focus 12m do P2 de 4,17 / 4,00 / 3,82 / 3,71 / 3,63 / 3,55 para 4,33 / 4,25 / 4,11 / 4,03 / 3,96 / 3,88. A Selic média do modelo no 1T28 vai de 12,18% para 12,71%, e o IPCA de 12 meses de 4,14% para 4,33%.
- Por quê: 7 dos 8 últimos resíduos de um passo da (E) foram positivos, com média de +0,35; com × 1,2 o viés cai para +0,19 (Modelo Estrutural, retrato do ciclo). Os longos parados em 3,50 mostram uma âncora de fato acima da meta.
- Onde entra: assimetria do base nos seis trimestres. É o principal motivo de P(up) ≥ 47% mesmo em 4T27 e 1T28.

**(i) E.e1 × 1,2 e E.e2 × 1,3 — âncora fraca** · cenário upside
- Coeficientes: e1 × 1,2 = 0,697, percentil 92; e2 × 1,3 = 0,210, percentil 94 (intervalo de 0,109 a 0,216). Os dois **dentro** do intervalo. O peso da meta vai a 0,092, e o viés dos 8 últimos resíduos cai para +0,10.
- Efeito: no upside, a Focus 12m vai de 4,18 / 4,01 / 3,85 / 3,77 / 3,69 / 3,61 para 4,45 / 4,45 / 4,37 / 4,35 / 4,31 / 4,26. A Selic média do modelo sobe a 14,56% no 1T27 e 14,68% no 2T27.
- Por quê: o upside é o cenário em que a eleição confirma o prêmio fiscal, e é nesse tipo de episódio que a pesquisa seguiu o preço (Q3: t+1 com mediana de +0,54 e t+2 de +0,20 em 45 dias úteis). A âncora quase sem peso (E.e1 × 1,3, fora do posterior, peso da meta de 0,03, Focus em ~4,6 nos seis trimestres) precisaria de um Copom que não reage, e o agente de política monetária dá a isso 5%. Ela fica como o extremo da cauda, sem peso próprio nas probabilidades.
- Onde entra: limite e probabilidade da cauda de cima.

**(i) E.e1 × 0,8 — âncora mais forte** · cenário downside
- Coeficiente: e1 × 0,8 = 0,465, percentil 6, dentro do intervalo.
- Efeito: no downside, a Focus 12m vai de 4,17 / 3,99 / 3,80 / 3,69 / 3,60 / 3,52 para 4,01 / 3,77 / 3,57 / 3,48 / 3,40 / 3,34.
- Por quê: é a âncora mais forte que o posterior admite. Um Copom que para de cortar no choque e um governo que entrega o centro da meta fiscal são a história em que ela vale. A amostra recente diz o contrário, por isso a cauda é magra.
- Onde entra: limite e probabilidade da cauda de baixo.

**(ii) Revisão em curso que a mediana ainda não mostra — Focus 12m nas pesquisas depois de 26/10** · cenários base e upside
- Hoje: Focus 12m em 4,53, base de 4 dias em 4,56 (`expc_focus` (inflação) · 23/10), anterior à eleição e ao pregão de 26/10.
- Por que o modelo não vê: a (E) só recebe o choque pela inflação de 12 meses, com peso 0,16, e não sabe o que já foi pesquisado no trimestre.
- Efeito: de +0,15 a +0,30 p.p. sobre a trajetória sem revisão no 4T26 e no 1T27, sumindo até o 3T27. O tamanho tem duas medidas que concordam: o p75 dos episódios de depreciação (+0,23 em 45 dias úteis) e a mediana dos episódios de salto da implícita (+0,28). A duração é julgamento: a causa é um resultado de eleição, que não se desfaz como uma dúvida, e a devolução parcial de 27/10 não muda isso, porque nos episódios a pesquisa subiu mesmo com a implícita devolvendo a alta.
- Onde entra: probabilidade do upside no 4T26 e no 1T27 (85% e 70%).

**(ii) O mercado à frente da pesquisa — inflação implícita de 2 e 5 anos** · cenário base
- Hoje: 6,69% e 6,81% (`br_interest_rate` · 26/10); +1,25 p.p. no de 2 anos em 5 dias úteis.
- Por que o modelo não vê: a (E) explica a pesquisa, e a curva não entra nela (mapa 2.6).
- Efeito: para cima em t+1 e t+2 da pesquisa, com o tamanho dos oito episódios de Q3 (medianas de +0,54 e +0,20 p.p. em 45 dias úteis). Uso a metade disso de 2T27 em diante, porque desta vez a reação do Copom está anunciada pelo agente de política monetária, e nos episódios o F não diz se houve.
- Onde entra: assimetria do base de 2T27 em diante (P(up) de 58% a 47%).

**(ii) Composição — serviços longos subindo com o cheio parado** · cenário base
- Hoje: serviços de 2028 em 4,65 (+0,15 em 4 sem.) e de 2029 em 4,10 (+0,10); IPCA de 2028 −0,05 e de 2029 sem mudança (`expc_focus_periodo` (inflação) · 23/10).
- Por que o modelo não vê: a (E) lê só o IPCA cheio de 12 meses (mapa 2.9).
- Efeito: leve para cima de 3T27 a 1T28, e só se a alta se confirmar em duas pesquisas.
- Onde entra: assimetria do base nos três últimos trimestres, com peso pequeno.

### 3.3 Da etapa 1 à tese

| Trimestre | Central (P2) | Upside: modelo → com tempero | Downside: modelo → com tempero | Limite de cima (sem revisão) |
|---|---|---|---|---|
| 4T26 | 4,17 | 4,18 → 4,45 | 4,17 → 4,01 | 4,45 (4,47) |
| 1T27 | 4,00 | 4,01 → 4,45 | 3,99 → 3,77 | 4,15 (4,17) |
| 2T27 | 3,82 | 3,85 → 4,37 | 3,80 → 3,57 | 3,95 (3,93) |
| 3T27 | 3,71 | 3,77 → 4,35 | 3,69 → 3,48 | 3,90 (3,88) |
| 4T27 | 3,63 | 3,69 → 4,31 | 3,60 → 3,40 | 3,90 (3,87) |
| 1T28 | 3,55 | 3,61 → 4,26 | 3,52 → 3,34 | 3,75 (3,70) |

O upside com tempero fica de 0,00 a 0,51 p.p. acima do limite de cima. No 4T26 ele só encosta no limite, porque lá a cauda vem da revisão que a pesquisa ainda não fez (tempero (ii)), e não da (E). O base com E.e1 × 1,2 passa o limite do 1T27 em diante. Por isso P(up) vai de 85% a 47%. O downside com tempero chega ao limite de baixo e exige o prêmio desfeito e uma âncora mais forte do que a amostra recente mostra: P(down) de 1% a 12%.

**Mudanças desde a rodada 2**

| O quê | Antes → depois | Por quê | Causa |
|---|---|---|---|
| Central, 3T27 a 1T28 | 3,72 / 3,64 / 3,57 → 3,71 / 3,63 / 3,55 | A central é a do P2; o CDS do fiscal cede a 125 p.b. no 1T28 | P2 (moderação, item 3) |
| Faixas e probabilidades | sem mudança | A central andou 0,01–0,02; a devolução parcial de 27/10 pesa contra a revisão, mas nos episódios a pesquisa subiu mesmo com a implícita devolvendo; a chance de 5% de um Copom que corta sob pressão e o Brent que pode não devolver (25% no externo) pesam a favor | Notícias de 27/10, relatórios de política monetária e externo |
| Condição das caudas | caudas de fiscal e câmbio da rodada 1 → as da rodada 2 (CDS de 170 a 210 e NTN-B de 8,15% a 9,10% no upside; 122 a 106 e 7,36% a 6,95% no downside) | Usar os caminhos dos principais | Relatório fiscal da rodada 2 |
| Leitura de serviços longos | demanda nos curtos, inércia nos longos → inércia e salário, com demanda só nos serviços às famílias | A atividade não vê demanda ampla em serviços | Relatório de atividade (E5) |
| Pedido sobre `R.t3` | aberto → fechado | A política monetária mostra que a âncora mais fraca já chega à regra pela (E) e que a distribuição dela já está nesse nível; subir `R.t3` no base contaria a desancoragem duas vezes. Aceito | Moderação, item 8 |

## 4. Para os outros agentes

**Respostas às entradas fixas (Parte 4 do mapa) e aos pedidos da rodada 2.**
- **XE2 e S9 (política monetária), em destaque:** a tese da seção 1. Os longos estão desancorados em nível e parados até 23/10 (t+2 +0,75, t+3 +0,50, percentis 82 e 86), e a cauda de cima tem 47% a 70% de 1T27 a 1T28. Ao S9: a Focus de 30/10 fica para o próximo ciclo. Nos oito saltos da implícita desde 2006, a mediana subiu +0,5 p.p. em t+1 e +0,2 em t+2 em 45 dias úteis; o IPCA de t+1 subiu 0,26 ou mais em 30 dias úteis em seis, e o de t+2 0,25 ou mais em quatro. Meus números para os seus sinalizadores, até a reunião de 09/12: Focus de 2027 acima de 4,6 com 55% (tão provável quanto não) e de 2028 acima de 4,0 com 35% (pouco provável). Na (R), a central implica Selic média de 12,18% no 1T28; com E.e1 × 1,2, 12,71%. Aceito a sua resposta da moderação sobre `R.t3`.
- **XE3 (inflação):** a (E) desce rápido demais. O P2 dá 4,17 no 4T26 com as 16 pesquisas do trimestre em 4,52 de média, e a trajetória da própria pesquisa sem revisão fica 0,11 a 0,30 p.p. acima do P2. Com E.e1 × 1,2, o IPCA de 12 meses do modelo vai de 4,14% para 4,33% no 1T28.
- **XE4 e IN-S10 (inflação):** a alimentação no domicílio é choque datado na pesquisa (4,00 em 2028), com parte dele já posta em 2027 (24 meses +0,17 em quatro semanas, para 4,49). Serviços de 2028 e 2029 subiram 0,15 e 0,10 com o cheio parado. Serviços de 2029 acima de 4,10 em duas pesquisas seguidas: a de 23/10 é a primeira em 4,10, e as seguintes ficam para o próximo ciclo.
- **XE1 e S10/E15 (câmbio):** a Focus de 23/10 tinha 5,05 para o fim de 2026 e 5,15 para o de 2027 (−0,15 e −0,13 em quatro semanas), com IPCA de 5,19 e 4,34 e Selic de 13,25 e 11,75 (`expc_focus_periodo`). Ela é anterior à eleição e está 0,45 abaixo da PTAX de 26/10. Nos 45 episódios de depreciação de 5% ou mais desde 2001, o câmbio de fim de ano da pesquisa incorporou 2% da depreciação em 5 dias úteis e 31% em 30 dias úteis, na mediana (p25 0%, p75 76%) (`cmb_ptax` e `expc_focus_periodo` (câmbio)). Uma revisão pequena na Focus de 30/10 é a regra, e não sinal de transitoriedade.
- **XE7 e FS-EP1 (fiscal):** o consumo do governo da Focus é de 2,20% em 2026 e 1,14% em 2027 (−0,15 em quatro semanas) (`expc_focus_periodo` (PIB) · 23/10). O corte fiscal da Focus (primário, nominal, dívida) e o conceito de primário que ela usa não estão no meu F, e nenhuma pesquisa depois de 26/10 está no F.
- **XE8 e FS-EP2 (fiscal), em destaque:** a Focus de 2029 e 2030 estava em 3,50 em 23/10, sem mudança em quatro semanas. A de 30/10 fica para o próximo ciclo. O que mudou é a chance de ela se mover: depois de saltos da implícita, t+2 subiu em seis dos oito episódios. t+3 não está na minha conta de episódios; a cauda de respondentes de 2029 está acima (média 3,62, percentil 71).
- **XE5 e S-EXP1 (atividade):** PIB de 2026 em 1,80% e de 2027 em 1,31% (−0,10 em quatro semanas, −0,29 em 13); consumo das famílias de 2027 −0,40 e investimento −0,54 em 13 semanas; trimestral de 1,67% no 4/2026 (`expc_focus_periodo` (PIB) · 23/10). Nenhuma coleta depois de 25/10 está no F. QPC de 23/09: PIB de 0,20% t/t no 3T26 e no 4T26, hiato de +0,20 no 4T26 e −0,20 no 4T27.
- **XE6 (atividade):** QPC de 24/06: potencial de 2,00%, desemprego neutro de 7,40% (2 anos), juro neutro de 6,00% (2 anos). Sem dado novo.
- **XE9 e XS8 (externo):** fora o QPC (67% veem o ambiente externo menos favorável), a Focus não pergunta Fed nem petróleo, e a de 30/10 fica para o próximo ciclo. O que nela reflete petróleo são os administrados: 4,10 em 12 meses, +0,60 p.p. em 13 semanas, e 2026 em 4,80 (+0,17 em quatro semanas) (`expc_focus` e `expc_focus_periodo` (inflação) · 23/10). É coerente com petróleo alto chegando à bomba, sem provar que a pesquisa supõe Brent acima de 110.

**Pedidos para o próximo ciclo (saídas fixas do mapa e deste ciclo).**
- **XS1 (política monetária):** a decisão de 04/11 e a comunicação, contra a pausa que você espera. Um corte é o cenário de âncora quase sem peso, e uma pausa com comunicação dura é o downside da âncora.
- **XS2 (política monetária):** o que o Copom disser de expectativas na 282ª, e se trata 3,50 nos longos como desancoragem a combater ou como piso aceito. Decide a evidência 3 de Q4.
- **XS3 (política monetária):** `meta_12m` em 3,00 e qualquer sinal sobre a meta ou a diretoria do BC a partir de 2027.
- **XS4 (política monetária):** a divisão entre Selic esperada e prêmio na curva depois de 26/10, para medir o tamanho do tempero (ii) 2.
- **XS5 e XS6 (inflação):** o IPCA de outubro contra a mediana mensal da Focus de 0,28. Acima de 0,40, somado ao choque, é o gatilho do upside de 4T26 e 1T27.
- **XS7 (câmbio):** a persistência do patamar depois de 27/10. Decide a duração do tempero (ii) 1.
- **XS8 (fiscal):** o conteúdo do projeto para o centro da meta fiscal e se foi enviado. É a história do downside.
- **XS9 (atividade):** os serviços às famílias seguem quentes com o hiato negativo a partir do 1T27?
- **XS10 (externo):** o Brent e a política da Petrobras, que decidem os administrados de 2027.
- **Ao agente web:**
  1. Revisões públicas de IPCA 2027 e 2028 de instituições nomeadas depois de 25/10 (nível B). Nada foi achado em duas rodadas. Tese que depende: o tamanho do tempero (ii) 1.
  2. Falas de diretores do Copom sobre expectativas depois de 27/10 e o comunicado de 04/11. Tese que depende: XS1, XS2 e o peso da âncora.
  3. Envio e conteúdo do projeto de lei complementar para o centro da meta fiscal. Tese que depende: a probabilidade do downside.

**Como subordinado:** nenhuma exógena neste ciclo.

**Divergências:** não sou principal de nenhuma exógena, e o P2 não registra divergência. Não escrevi caminho de exógena no JSON (`caminhos` vazio). O pedido à política monetária sobre `R.t3` foi respondido na moderação e está fechado. Fica uma discordância com o modelo, e não com outro agente: a central que a (E) produz está abaixo da própria pesquisa, como os agentes de política monetária e de inflação também escreveram. Ela vai para a seção 6.

## 5. Placar

Primeiro ciclo conjunto. O ciclo de 2026-10-02 foi um teste e não é lido, e não há report final anterior cujos trimestres tenham fechado. Para registro, sem faixa a conferir: o 3T26 fechou em 4,37, média de 65 pesquisas (`expc_focus` (inflação)). O 4T26 deste report é o primeiro a ser conferido.

## 6. Sobre o modelo

Ciclo sem literatura. As propostas vêm dos dados, e o modelo não muda neste ciclo.

| Fonte | O que sugere (regressor, defasagem, quebra, âncora) | Teste proposto (dado, amostra, que resultado mudaria a especificação) | Por que importa para a tese deste ciclo |
|---|---|---|---|
| Resíduos de um passo da (E) (Modelo Estrutural, retrato do ciclo) | Quebra no peso da meta: 7 de 8 resíduos positivos de 4T24 a 3T26, média de +0,35 contra desvio de 0,34; zerar o viés pede peso da meta de ~0,03 em vez de 0,26 | Reestimar a (E) em 2002–2016 e 2017–2026, e com peso da meta variável no tempo; alternativa, trocar a âncora `meta_12m` pela Focus de t+3 (hoje 3,50). Comparar o erro de um passo fora da amostra em 4T24–3T26; se cair mais de um terço, mudar | É a razão da assimetria para cima em todos os trimestres; com a âncora em 3,50, a central do 1T28 seria mais alta |
| A aritmética do 4T26 (`expc_focus` (inflação), pesquisas do trimestre) | O primeiro trimestre projetado ignora as pesquisas já feitas nele: 4,17 para um trimestre cujas 16 primeiras pesquisas têm média de 4,52 | Condicionar o primeiro trimestre de `focus_12m` à média parcial já observada, como o modelo já faz ao partir do último trimestre com dado; medir o erro do 1º trimestre projetado com e sem isso. O agente de inflação propõe o mesmo para a (I) | A central do 4T26 está fora do que a aritmética permite com 99% de probabilidade, e o erro se propaga pela inércia e, pela (R), para a Selic |
| Saltos da implícita e a pesquisa (`br_interest_rate`, `expc_focus`, `expc_focus_periodo` (inflação), 2006–2026) | A pesquisa segue saltos do preço da inflação (t+1 com mediana de +0,54 em 45 dias úteis em oito episódios) e quase não reage a depreciação sem eles; a (E) só vê o câmbio pelo IPCA, com peso 0,16 | Acrescentar à (E) a variação trimestral da implícita de 2 anos (ou o desvio dela contra a Focus 24m), 2006–2026; mudar se o coeficiente for positivo com intervalo fora de zero e os resíduos de 1T25 e 4T21 caírem. O fiscal propõe a implícita de 10 anos na (F), pelo mesmo motivo | Decide se o choque de 26/10 entra pelo modelo ou só pelo tempero, e é o maior salto da amostra |

[^1]: Percentil: a posição do valor de hoje entre todas as leituras da série, de 0 (o menor já visto) a 100 (o maior). Na distância à meta, quanto maior, mais longe da meta em relação ao histórico.
[^2]: Focus: pesquisa semanal do Banco Central com cerca de 100 a 140 instituições sobre o que esperam para inflação, PIB, câmbio e Selic. A mediana é o número que se cita.
[^3]: QPC (Questionário Pré-Copom): pesquisa do Banco Central com economistas antes de cada reunião do Copom, sobre o que o Copom fará e deveria fazer, projeções e balanço de riscos. O último é de 23/09/2026.
[^4]: Base de 30 dias: a mediana de todas as respostas atualizadas nos últimos 30 dias. Base de 4 dias úteis: só quem respondeu nos últimos quatro dias úteis. Quando a de 4 dias se afasta da de 30, há revisão em curso que a mediana ainda não mostra.
[^5]: Inflação implícita: a inflação que iguala o título prefixado e o atrelado ao IPCA no mesmo prazo, (1 + taxa prefixada)/(1 + taxa real) − 1. É preço, e não pesquisa: inclui um prêmio pelo risco de a inflação surpreender e efeitos de liquidez, por isso costuma ficar acima da pesquisa.
[^6]: A variável da tese é a média, no trimestre, das medianas diárias da Focus para o IPCA dos próximos 12 meses, na série suavizada, que interpola entre as janelas para não saltar quando um mês sai do cálculo. O placar confere a média, e não o último valor do trimestre.
[^7]: Sobre o processo: o report final sai depois de duas rodadas com os outros seis agentes, duas consolidações do Modelo Estrutural (P1 e P2) e uma moderação das divergências. A pesquisa mais recente no F continua sendo a de 23/10, e preços e curvas são de 26/10; as notícias trazem fatos até 27/10, mas nenhum número de pesquisa. A central é a do P2.
[^8]: A projeção do Copom no cenário de referência é condicional aos caminhos que ele supõe (a Selic da Focus, câmbio, petróleo). É o que acontece se essas premissas valerem, e não a previsão do Copom.
[^9]: Trajetória sem revisão: a inflação mês a mês que a própria pesquisa de 23/10 espera (medianas mensais até out/2028; o resto de 2028 e o ano de 2029 pelas anuais, com o perfil sazonal de 2028), acumulada em janelas de 12 meses e suavizada pelo dia do mês. A conta reproduz a Focus 12m publicada em 23/10 com erro de 0,01 p.p. É o que a Focus 12m marcaria se nenhum respondente mudasse de ideia.
