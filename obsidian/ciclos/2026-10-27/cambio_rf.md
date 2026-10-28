# Report — câmbio · ciclo 2026-10-27 · report final

Dados até: 27/10/2026 (PTAX até 26/10); notícias até 27/10 · Horizontes: 4T26 a 1T28, USD/BRL pela PTAX de venda do último dia útil de cada trimestre[^ptax]

## 1. Tese

| Variável | Trimestre | Central | Base: faixa · P | Upside: limite · P | Downside: limite · P | P(up) − P(down) |
|---|---|---|---|---|---|---|
| USD/BRL, PTAX de fechamento | 4T26 | 5,427 | 5,30 a 5,60 · 47% | acima de 5,60 · 31% | abaixo de 5,30 · 22% | +0,09 |
| | 1T27 | 5,515 | 5,34 a 5,78 · 46% | acima de 5,78 · 30% | abaixo de 5,34 · 24% | +0,06 |
| | 2T27 | 5,517 | 5,34 a 5,82 · 45% | acima de 5,82 · 29% | abaixo de 5,34 · 26% | +0,03 |
| | 3T27 | 5,501 | 5,34 a 5,82 · 44% | acima de 5,82 · 28% | abaixo de 5,34 · 28% | 0,00 |
| | 4T27 | 5,511 | 5,36 a 5,82 · 44% | acima de 5,82 · 30% | abaixo de 5,36 · 26% | +0,04 |
| | 1T28 | 5,528 | 5,38 a 5,83 · 43% | acima de 5,83 · 27% | abaixo de 5,38 · 30% | −0,03 |

A central é a PTAX do P2, sem ajuste[^modelo].

- **Upside (real mais fraco, ruim para a inflação e para o Brasil):** as decisões fiscais de 2027 confirmam a leitura que o mercado fez da reeleição. Com o CDS a 170 p.b. no 4T26 e ~205–210 em 2027, a NTN-B de 10 anos a ~9% (os caminhos de cauda do fiscal) e a volatilidade implícita a 24%, o modelo dá 5,64 no 4T26 e 5,88 no 2T27. Com o peso do CDS × 1,2 vai a 5,67 e 5,96, e com o resto da desmontagem de posição (+1%) e o BC vendendo dólar (−1,5%) fica em 5,64 no 4T26. Se a alta da Selic que o modelo faz nesse cenário (~14,3% no 1T27) não segurar o real, que é a cauda de dominância fiscal, o upside vai a 5,68 no 4T26 e 5,99 no 2T27.
- **Downside (real mais forte, bom para a inflação):** o projeto de lei complementar que o ministro da Fazenda anunciou para mirar o centro da meta fiscal convence o mercado. Com o CDS de ~120 a ~105 p.b., a NTN-B de 10 anos de 7,4% a 7,0% (as caudas do fiscal) e a volatilidade a 12–13%, o modelo dá 5,28 no 4T26 e 5,43 no 1T28. Com o peso do S&P 500 reduzido a 55%, 5,27 e 5,38.
- **A tese em uma frase:** a reeleição levou o real a um patamar que não reverte sozinho. O P2 põe a PTAX entre 5,43 e 5,53 em todo o horizonte. A saída sazonal de dezembro e um prêmio fiscal que só as decisões de 2027 vão testar inclinam 2026 e 2027 para a depreciação. No 1T28 o risco fica levemente para a apreciação, porque parte da alta da central vem de um canal do modelo, o S&P 500, cujo sinal o mecanismo não sustenta.

## 2. Argumentação

### Q3 — O que explica a dinâmica recente

**A eleição explica o mês, e o saldo dela é um real mais fraco que antes do 1º turno.**
- Em 05/10, depois do 1º turno de 04/10 com Flávio Bolsonaro à frente, a PTAX caiu 4,55% contra 02/10 (`cmb_ptax`). A leitura dos investidores foi de "redução do prêmio de risco dos ativos brasileiros" (Agência Brasil · 05/10 · nível A).
- Em 26/10, depois da reeleição de Lula em 25/10 (CNN Brasil · 25/10 · nível A), a PTAX subiu 9,2%, de 5,04 em 23/10 para 5,50 (`cmb_ptax`). "O mercado vinha tratando a vitória de Flávio como a possibilidade de uma virada na política fiscal do governo" (CNN Brasil · 25/10 · nível A). Na noite de domingo, um estrategista da Lombard Odier, Homin Lee, disse ser "inevitável que os mercados revertam uma parcela significativa do rali de Bolsonaro" (Bloomberg Línea · 25/10 · nível B).
- O saldo: a PTAX de 26/10 está 5,3% acima da de 02/10, véspera do 1º turno, com o CDS só ~6 p.b. mais alto, de 131 para 137 (`cmb_risco_pais`). O mercado desfez o que tinha precificado em 05/10 e passou a cobrar um prêmio acima do de antes do 1º turno, quando o resultado ainda estava em aberto[^processo]. Desde o fechamento do 3T26 (5,18 em 30/09) a alta é de 6,2% (`cmb_ptax`).

**Parte do exagero de 26/10 já voltou.** No pior momento, na noite de 25/10, o real chegou a perder 12% (CNN Brasil · 25/10 · nível A). O dólar à vista fechou 26/10 em alta de 8,36% (InfoMoney · 27/10 · nível B), e em 27/10 fechou em queda de 0,97%, a R$ 5,350 (Poder360 · 27/10 · nível B). O ministro da Fazenda, Dario Durigan, disse que a reação foi "de posição" e não de desconfiança nas contas públicas (Poder360 · 27/10 · nível B). É a fala de quem tem interesse em dizê-la e não prova a causa. Mas o caminho do preço (12% na noite de domingo, 8,4% no fechamento de segunda, devolução na terça) é o de uma desmontagem concentrada num pregão. A PTAX de 27/10 não está no F, e os R$ 5,35 são o fechamento do dólar comercial, não a PTAX.

**O movimento é idiossincrático, com prova pelos pares em 05/10 e indício em 26/10.**[^split] Em 05/10, mesma natureza de evento, o real caiu 4,55% e nenhum par passou de 1,95%:

| 02/10 → 05/10 | Variação (moeda por dólar) |
|---|---|
| Real | −4,55% |
| Peso colombiano | −1,95% |
| Peso mexicano | −1,01% |
| Peso chileno | −0,77% |
| Sol peruano | −0,31% |
| Dólar contra emergentes | −0,37% |
| DXY | +0,24% |

Fonte: `cmb_ptax`, `cmb_fx_latam` (chileno e colombiano na taxa formada no dia), `cmb_dollar_index_em`, `cmb_dollar_index`, 02 e 05/10.

O dólar subiu contra os desenvolvidos e caiu pouco contra os emergentes, num índice que contém o próprio real, enquanto o real caía 4,55% com o CDS −12 p.b. (`cmb_risco_pais`): a apreciação foi do Brasil. Em 26/10 o DXY subiu 0,15% (`cmb_dollar_index`), o S&P 500 subiu 0,70% (`cmb_equity_us`) e o CDS subiu 18 p.b. Pelo Investing.com México, o peso mexicano se apreciou 0,56% no dia e foi "a quarta divisa mais apreciada", segundo Gabriela Siller (Grupo Financiero Base), enquanto o real caía 8,63% (Investing.com México · 26/10 · nível B). Isso indica que o choque não foi regional. Mas o F não tem os pares depois de 15–20/10 (`cmb_fx_latam`) nem o dólar contra emergentes depois de 23/10 (`cmb_dollar_index_em`), e o chileno e o colombiano de 26/10 não aparecem em fonte aberta. A prova por dado de 26/10 fica para o próximo ciclo.

**O CDS explica pouco do salto, e isso não é falta de força do canal no trimestre.** Pelo modelo, o CDS de 26/10 explica ~1,6% dos ~9,2% de alta desde 22/10. No dado diário de 2006–2026, com o dólar contra emergentes como controle, a PTAX sobe 0,42% por 10 p.b. de CDS quando o CDS está abaixo de 200 p.b., contra 0,26% na amostra inteira (`cmb_ptax`, `cmb_risco_pais`, `cmb_dollar_index_em`). Mas no dado trimestral, a frequência do modelo, a relação se inverte: 0,57% contra 0,85% (mesmas tabelas). O pregão amplifica o CDS quando ele está baixo, e o trimestre devolve parte disso, como 26/10 já começou a devolver. O fiscal, depois de refazer a conta pelo lado dele, aceitou o peso do CDS × 1,2 só no upside (report do fiscal, seção 4).

**A expectativa ainda não viu o salto.** A mediana do Focus para o fim de 2026 era 5,05 em 23/10, revisada de 5,20 quatro semanas antes (`expc_focus_periodo` câmbio), numa pesquisa fechada antes de 26/10. Pelo agente de expectativas, nos 45 episódios de depreciação de 5% ou mais desde 2001 a pesquisa incorporou ~31% da alta em 30 dias úteis, na mediana (report de expectativas). Então uma revisão pequena em 30/10 será a regra, e não sinal de que o salto é transitório.

### Q1 — Condições do mercado de câmbio

**O BC deixou o preço andar.** Não há intervenção à vista nem de linha em outubro até 26/10 (`cmb_reservas_bc` · 26/10). Em 27/10 houve só o leilão de rolagem de swap cambial de até US$ 4 bi, que é a rolagem programada do estoque (InfoMoney · 27/10 · nível B). Na coletiva de 27/10, Galípolo não respondeu sobre parâmetros de intervenção cambial nem sobre a próxima decisão do Copom (Poder360 · 27/10 · nível B). O mercado que travou foi o de juros. Uma analista da Empiricus, Lais Costa, disse que "o mercado está muito disfuncional" (InfoMoney/Reuters · 26/10 · nível B). O Tesouro cancelou os leilões de 27 a 29/10 (InfoMoney/Estadão Conteúdo · 26/10 · nível A), recomprou títulos, e os DIs recuaram em 27/10 "após nova intervenção do Tesouro" (InfoMoney/Estadão Conteúdo · 27/10 · nível A).

Um câmbio que sobe 9% sem venda de dólar do BC, enquanto o Tesouro age no mercado de títulos, mostra que o BC leu preço, e não disfunção, no câmbio. Mas o cupom cambial, que mostraria escassez de dólar no mercado local, não está no dado. E as reservas de ~US$ 365 bi (`cmb_reservas_bc` · 26/10) e a intervenção de setembro (US$ 2 bi à vista e US$ 2 bi em linhas, com a PTAX entre 5,12 e 5,21) mostram que o BC tem o instrumento e já o usou neste ano.

**Mercado fino antes do choque.** O volume interbancário D+2 teve média de ~US$ 1,0 bi/dia no último mês, percentil 19 em 10 anos[^pctl] (`cmb_ptax` · 23/10), o que ajuda a explicar 9% num pregão. O D+1 está no percentil 67, então não é falta de liquidez em todo prazo. Os bancos fecharam setembro vendidos em ~US$ 26 bi no mercado à vista, percentil 24 em 10 anos (`cmb_reservas_bc` · set)[^posbancos].

**Posição muito comprada em real quando o choque veio, provavelmente já reduzida.** Em 20/10 os fundos alavancados e os asset managers estavam comprados em ~70 mil contratos, percentil 95 em 10 anos, com as posições em aberto no percentil 98 (`cmb_cot_fx` · 20/10)[^cot]. A posição extrema é o que faz um choque virar 12% numa noite; o caminho do preço de 25 a 27/10 (Q3) sugere que boa parte dela saiu no próprio pregão. Mas o COT de 27/10 não está no F, e nenhuma reportagem nomeada sobre a desmontagem apareceu nas notícias do ciclo. Se o COT mostrar a posição ainda comprada, o tempero de posicionamento volta ao dobro.

**Fluxo: entrada antes do choque, sem dado depois.** De 1º a 16/10 o fluxo cambial foi positivo em ~US$ 5,2 bi, ~US$ 4,1 bi pelo financeiro (`cmb_cambio_contratado` · 16/10), coerente com a apreciação depois do 1º turno. O fluxo de 26/10 não está no F.

### Q2 — Fundamentos

**Carry alto e mais alto depois do choque, mas descolado do real.** O diferencial real ex-post era ~9,1 p.p. em setembro, percentil 81 em 10 anos (`diferenciais_juros` · set)[^carry]. No pregão em que o DI de 1 ano menos a meta do Fed foi de ~9,1 para ~10,8 p.p. (`br_di_grade`, `us_interest_rate`, 22 e 26/10), o real caiu 9%.

Para a política monetária, uma pausa hoje seria lida como credibilidade. Uma alta só seria lida assim se viesse com sinal de que o Copom reage aos efeitos de segunda ordem; sem ele, num choque de prêmio político e fiscal, ela pode ser lida como custo da dívida (report de política monetária, E2). O fiscal vê dois dos três sinais de dominância presentes, nenhum completo, e põe essa cauda em ~10% (report do fiscal, seção 4)[^dominancia]. Por isso o upside tem uma versão em que a alta da Selic do modelo não segura o real (seção 3.1).

A volatilidade também come o carry: a realizada de 63 dias foi de ~12% em 23/10 (`cmb_ptax`) para ~21% em 26/10, percentil 96 em 10 anos ("O real e os pares" · 26/10).

**Contas externas não são o problema; a saída financeira é.** O déficit em transações correntes é de ~US$ 60 bi em 12 meses, 2,3% do PIB, contra investimento direto de ~US$ 88 bi, 3,4% do PIB, percentil 93 (`cmb_balanco_pagmt` · set). As exportações de bens estão em recorde, ~US$ 377 bi. Mas a renda primária tem o maior déficit da série (~−US$ 84 bi em 12 meses), e o fluxo financeiro de 12 meses é de ~−US$ 62 bi, percentil 18 (`cmb_cambio_contratado` · set), com a remessa de renda no percentil 6. É essa saída que se concentra em dezembro (seção 3.2).

**Termos de troca bons, sem papel no mês.** O IC-Br em dólar está 12,8% acima de um ano antes (`comm_icbr_usd` · set), e o petróleo exportado somou ~US$ 54 bi em 12 meses, contra ~US$ 44 bi um ano antes (`cmb_comex_produto` · set). Mas os termos de troca da Funcex caíram 3,0% em três meses até agosto (`cmb_termos_troca`), e o Brent recuou de ~136 em 02/10 para ~115 em 20/10 (`comm_brent`) num mês em que o real foi e voltou com a eleição.

**Valuation: neutra antes do choque, barata depois.** O câmbio real efetivo estava no percentil 53 em 10 anos em setembro (`cmb_reer` · set)[^reer], e a PTAX de 26/10 está 6,9% acima da média de setembro (`cmb_ptax`). O real mais barato sustenta o downside de 2027, e o modelo não o vê.

### Q4 — Por que a central e por que a distribuição

**A central.** É a PTAX do P2: 5,43 no 4T26, ~5,50–5,52 em 2027 e 5,53 no 1T28 (seção 3.1). Contra a rodada 2, ela subiu ~0,01 do 1T27 ao 3T27 e caiu 0,02 no 4T27 e 0,04 no 1T28, pelos caminhos novos do fiscal e do externo. O que move a PTAX do modelo, canal a canal:
- A volatilidade implícita de 17% no 4T26 divide o carry e é o canal que mais pesa no primeiro trimestre[^carry]. Ela recua a 13,5% no fim de 2027 e devolve apreciação.
- A Selic do modelo cai de 13,43% no fechamento do 4T26 para 12,10% no 1T28 e tira carry ao longo de 2027. É a Selic da regra do modelo, mais alta que no P1 porque o juro real de 10 anos do fiscal subiu (7,72% → 7,95% no 1T27). A política monetária tem a mediana dela acima dessa central (report de política monetária), e a curva precificava 15,78% em dez/27 (`br_di_grade` · 26/10).
- O CDS do fiscal vai de 131 no 3T26 a 142 no 1T27 e cede a 125 no 1T28, pelo componente global do externo, o que aprecia o real no fim do horizonte.
- O S&P 500 do externo sobe de 7.750 no 4T26 a 8.500 no 1T28, e o modelo lê isso como depreciação: +0,006 na PTAX do 4T26 e +0,12 (2,2%) na do 1T28, contra o S&P parado em 7.717 (Modelo Estrutural).
- O IC-Br em dólar cede de 206 no 4T26 a 198 no 1T28 (externo), o que deprecia pouco.

**A distribuição.** No 4T26 a central fica cerca de 1,35% abaixo da PTAX de 26/10, e duas forças que o modelo não vê a empurram para cima. Uma é a saída sazonal de dezembro, que sozinha leva a central a 5,54 (seção 3.2). A outra é o prêmio fiscal que só as decisões de 2027 vão testar: o fiscal dá 27–30% à cauda de alta do CDS e 13–16% à de baixa.

Três coisas pesam contra elas. O exagero de 26/10 começou a voltar em 27/10 (Q3). O ministro da Fazenda disse que vai "buscar o centro da meta" por um projeto de lei complementar (Poder360, CNN Brasil e Exame · 27/10 · nível A), a ser apresentado "ainda em 2026" (Poder360 · 26/10 · nível B). E o real ficou barato. A posição comprada, que na rodada 1 empurrava o 4T26 para cima, provavelmente já saiu em boa parte. O conteúdo do projeto não foi detalhado, e a escolha do ministro da Fazenda do próximo mandato segue pendente (InfoMoney · 27/10 · nível B; Poder360 · 27/10 · nível B): os dois sinais que decidem as caudas saem dentro do 4T26 ou logo depois. Daí 31% de upside e 22% de downside no 4T26.

Em 2027 a sazonalidade só volta no 4T27, e a força para baixo é o S&P. O sinal positivo do S&P na (F) vem de ele entrar junto com o dólar contra emergentes e o CDS, e o mecanismo do mapa (2.3) diz o contrário: bolsa americana em alta é apetite a risco e real mais forte. O externo confirmou que no base dele o S&P sobe por lucro e crescimento nominal, e não por apetite a risco (ata da rodada 2, item 4). Com o peso reduzido a 55%, a PTAX do base fica 0,06 mais baixa no 1T28 (5,47).

Contra isso, o fiscal subiu as probabilidades da cauda de alta do CDS para 27–30% e a assimetria dele para +0,14–0,15. Por isso 2T27, 3T27 e 4T27 ficam em +0,03, 0,00 e +0,04, e só o 1T28 fica negativo (−0,03). A faixa para de abrir depois do 2T27 porque os caminhos de cauda do fiscal param de se afastar ali; a incerteza que cresce com o horizonte entra na probabilidade da faixa, que cai de 47% para 43%.

**O que derrubaria a tese:**
- **Downside:** a PTAX abaixo de 5,30 por duas semanas com o CDS abaixo de 120 p.b. leva a probabilidade para o downside.
- **Upside:** o CDS acima de 160 p.b. por dez pregões, ou a PTAX acima de 5,70 por uma semana sem venda do BC, leva o 4T26 para o upside.
- **Eventos que decidem:** o envio do projeto fiscal com meta e mecanismo e o nome do ministro da Fazenda; cada um move as caudas antes de mover o dado.

### Olhado, sem sinal

- Estoque de swaps cambiais · ~−US$ 92 bi (`cmb_reservas_bc` · ago) · dado de agosto, e a rolagem de 27/10 só renova o estoque · diria algo se o BC ofertasse swap novo acima dos vencimentos.
- Reservas no conceito de liquidez · ~US$ 369 bi (`cmb_reservas_bc` · 26/10) · estáveis no mês, sem venda · diria algo se caíssem com leilões à vista.
- Carteira, ações · ~−US$ 5 bi em 12 meses, percentil 10 (`cmb_balanco_pagmt` · set) · saída lenta, sem mudança no mês · diria algo se a saída de setembro (~−US$ 2 bi) se repetisse em outubro, com o choque.
- Exportação para os EUA · ~US$ 36 bi em 12 meses contra ~US$ 40 bi um ano antes (`cmb_comex_pais` · set) · compensada pela China · diria algo se a queda chegasse ao saldo total.
- Treasury de 10 anos · 5,00% (`us_interest_rate` · 23/10) · −0,11 p.p. no mês · diria algo se a alta de 12 meses (~+1 p.p.) voltasse.
- Operação compromissada do BC de até R$ 5 bi em 27/10 (InfoMoney · 27/10 · nível B) · é liquidez em reais, não câmbio · diria algo se viesse junto de leilão de dólar.

## 3. Premissas

### 3.1 Etapa 1 — o modelo

**Cenários.**
- **Base:** Lula reeleito (CNN Brasil · 25/10 · nível A). As decisões fiscais de 2027 demoram e não confirmam nem ruptura nem consolidação (o base do fiscal). A volatilidade sobe no 4T26 e volta devagar ao normal ao longo de 2027. O bloco global segue o base do externo.
- **Upside:** o governo afrouxa o fiscal de 2027 e o mercado lê a reação monetária como insuficiente; é o upside do fiscal, que já carrega o risk-off do externo no CDS. Antes da votação, Lula disse que quer "que o Banco Central baixe o juro" e subsidiar diesel e gasolina (Poder360 · 24/10 · nível B). Durigan disse que os subsídios aos combustíveis devem continuar em 2027 (Poder360 · 23/10 · nível B). Dizer não é fazer, e é por isso que é cauda. A volatilidade fica perto dos níveis de 2015. O choque é doméstico, então o resto do bloco global fica no base do externo.
- **Downside:** um arcabouço de 2027 que o mercado compre desfaz parte da leitura de 26/10, e os preços voltam para perto do intervalo de 05 a 23/10; é o downside do fiscal. Durigan prometeu um projeto de lei complementar para mirar o centro da meta (Poder360, CNN Brasil e Exame · 27/10 · nível A) e disse que quer mudar a legislação "ou, se necessário, a Constituição" (Poder360 · 26/10 · nível B). Ele também chamou Rafael Fonteles de "excelente nome" para a Fazenda, numa escolha que o veículo dá como em discussão, com Fonteles e Alckmin entre os cotados (Poder360 · 27/10 · nível B). A volatilidade volta aos níveis de 2025–2026, e o bloco global fica no base do externo.

**Caminhos das exógenas.** A volatilidade implícita é minha (principal). O CDS e o juro real de 10 anos são do fiscal (principal), nos três cenários do report r2 dele. O bloco global é do externo (principal), no base dele em todos os cenários. A meta é da política monetária. O base de todas é o do P2.

| Exógena | Hoje (valor · tabela · data) | Cenário | 4T26 | 1T27 | 2T27 | 3T27 | 4T27 | 1T28 |
|---|---|---|---|---|---|---|---|---|
| Volatilidade implícita do real (% a.a.) · principal: câmbio | sem dado no F; 12,19 no 2T26 (Modelo Estrutural) | base | 17,0 | 15,5 | 14,5 | 14,0 | 13,5 | 13,5 |
| | | upside | 24,0 | 21,0 | 18,0 | 16,0 | 15,0 | 15,0 |
| | | downside | 13,0 | 12,5 | 12,0 | 12,0 | 12,0 | 12,0 |
| CDS 5 anos (p.b.) · principal: fiscal | 137 · `cmb_risco_pais` · 26/10 | base | 140 | 142 | 139 | 135 | 130 | 125 |
| | | upside | 170 | 205 | 210 | 205 | 198 | 190 |
| | | downside | 122 | 115 | 112 | 110 | 108 | 106 |
| Juro real de 10 anos, NTN-B (% a.a., média) · principal: fiscal | 8,05 em 26/10 (report do fiscal) | base | 7,72 | 7,95 | 7,90 | 7,80 | 7,75 | 7,70 |
| | | upside | 8,15 | 8,90 | 9,10 | 9,10 | 9,00 | 8,90 |
| | | downside | 7,36 | 7,30 | 7,15 | 7,05 | 7,00 | 6,95 |
| Dólar contra emergentes (pontos) · principal: externo | 130,2 · `cmb_dollar_index_em` · 23/10 | todos | 130,5 | 131,0 | 130,5 | 130,0 | 129,5 | 129,0 |
| S&P 500 (pontos) · principal: externo | 7.717 · `cmb_equity_us` · 27/10 | todos | 7.750 | 7.900 | 8.050 | 8.200 | 8.350 | 8.500 |
| IC-Br em dólar (pontos) · principal: externo | 205,7 · `comm_icbr_usd` · set | todos | 206,2 | 202,6 | 201,0 | 199,9 | 199,0 | 198,3 |
| Fed Funds efetivo (% a.a.) · principal: externo | 3,75 · `diferenciais_juros` · set | todos | 4,13 | 4,13 | 4,13 | 4,13 | 4,13 | 3,88 |
| CPI dos EUA (% no trimestre) · principal: externo | 3,72 em 12 meses · `diferenciais_juros` · set | todos | 0,86 | 0,61 | 0,61 | 0,65 | 0,63 | 0,65 |

A meta de inflação (3,00%) e o IC-Br agropecuária e metais ficam no P2 em todos os cenários.

Motivo do caminho da volatilidade (base), mantido desde a rodada 1. O F não traz a implícita, e o modelo não tem o 3T26 (segura 12,19). Pela relação histórica com a realizada (82 trimestres desde 2006; `cmb_ptax` e a série do Modelo Estrutural), a implícita de 31/12 seria de ~17% a ~19% se os pregões restantes do ano tivessem volatilidade de 8% a 13%, porque a janela de 63 dias ainda conterá 05/10 e 26/10. Fico em 17%, no piso dessa conta: os dois pregões precificaram a eleição, um evento que já passou, e a implícita é o preço do risco à frente, não do que aconteceu. Com 18,5% a central do 4T26 subiria ~0,02.

Depois de picos, a implícita recuou em um a três trimestres (21,6 → 14,6 do 3T18 ao 4T18), e o caminho chega perto da mediana (14,3%) no 2T27. No upside, a persistência de 2015 (25,1 → 22,8 → 21,8); no downside, a volta rápida de 2018.

**Saída do modelo** (central; a faixa de 90% do posterior dos pesos não inclui o erro da equação, de ~3,6% por trimestre).

| Variável | Cenário | 4T26 | 1T27 | 2T27 | 3T27 | 4T27 | 1T28 |
|---|---|---|---|---|---|---|---|
| PTAX (R$/US$) | base (P2) | 5,427 | 5,515 | 5,517 | 5,501 | 5,511 | 5,528 |
| | upside, sem multiplicador | 5,636 | 5,869 | 5,880 | 5,831 | 5,824 | 5,831 |
| | upside, CDS × 1,2 | 5,673 | 5,942 | 5,958 | 5,904 | 5,890 | 5,889 |
| | upside, CDS × 1,2, NTN-B no base (Selic sem a alta) | 5,682 | 5,966 | 5,992 | 5,945 | 5,932 | 5,930 |
| | downside | 5,279 | 5,350 | 5,363 | 5,369 | 5,403 | 5,433 |
| Selic de fechamento (% a.a.) | base | 13,43 | 13,21 | 12,87 | 12,56 | 12,30 | 12,10 |
| | upside (CDS × 1,2) | 14,12 | 14,30 | 14,15 | 13,89 | 13,61 | 13,40 |
| | downside | 12,92 | 12,50 | 12,10 | 11,78 | 11,52 | 11,31 |
| IPCA 12 meses (%) | base | 5,34 | 4,95 | 4,46 | 4,48 | 4,32 | 4,14 |
| | upside (CDS × 1,2) | 5,37 | 5,06 | 4,65 | 4,72 | 4,56 | 4,32 |
| | downside | 5,32 | 4,89 | 4,38 | 4,39 | 4,24 | 4,09 |

A faixa de 90% do posterior da PTAX base vai de 5,34 a 5,52 no 4T26 e de 5,30 a 5,78 no 1T28.

No upside, a NTN-B a ~9% leva a Selic do modelo a 14,30% no 1T27, e esse carry a mais aprecia o real em ~0,01 (4T26) a ~0,04 (2027) contra a mesma rodada com a NTN-B no base. A linha "NTN-B no base" é a versão do upside em que a alta de juros não segura a moeda. No downside, a NTN-B a ~7% deixa a Selic do modelo cortar até 11,31% e tira carry: sem esse corte, a PTAX ficaria ~0,01 a ~0,03 mais baixa.

### 3.2 Etapa 2 — o tempero

**(i) CDS 5 anos — efeito mais forte que o estimado** · cenário upside
- Coeficiente: `F.b_fiscal`, estimado 25,1 por desvio-padrão da variação (298,5 p.b.), intervalo de 90% do posterior de 19,5 a 30,6. Multiplicador: × 1,2 (30,1), dentro do intervalo, percentil 94 do posterior[^mult].
- Efeito: PTAX do upside de 5,64 para 5,67 no 4T26 e de 5,88 para 5,96 no 2T27.
- Por quê: o modelo é linear na variação do CDS e o estresse não é. Em 26/10 o real andou ~6 vezes o que o CDS explica no modelo, e em 05/10 ~4 vezes (report do fiscal). Não saio do intervalo: no dado trimestral, o do modelo, o real não reage mais ao CDS quando ele está baixo (Q3). O fiscal aceitou esse ponto e retirou o pedido de × 1,5 no upside e de × 1,2 no base (ata da rodada 2, item 2).
- Onde entra: limite do upside.

**(i) S&P 500 — efeito mais fraco que o estimado** · cenário base (assimetria) e downside
- Coeficiente: `F.b_sp500`, estimado +1,89 por desvio-padrão da variação (8,4%), intervalo de 90% do posterior de 0,98 a 2,79: a bolsa americana em alta deprecia o real no modelo. Multiplicador: × 0,55 (1,04), dentro do intervalo, perto do limite de baixo.
- Efeito: no base, a PTAX fica de 0,007 (4T26) a 0,058 (1T28) mais baixa, 5,42 a 5,47; no downside, de 5,28 para 5,27 no 4T26 e de 5,43 para 5,38 no 1T28.
- Por quê: o sinal contraria o mecanismo do mapa (2.3), em que bolsa americana em alta é apetite a risco e o real, moeda de beta alto, se aprecia. O externo registra que o peso mede o S&P com o CDS e o dólar contra emergentes parados, e que no base dele o S&P sobe por lucro, não por risco (ata da rodada 2, item 4). Neste ciclo o canal deixou de ser pequeno: é a maior contribuição externa à PTAX do 1T28 (+0,12 contra o S&P parado). Fico dentro do intervalo porque não testei a (F) sem o dólar contra emergentes (seção 6).
- Onde entra: assimetria do base de 2T27 em diante e limite do downside.

**Dois argumentos do externo que não aplico.** O primeiro pede `F.b_icbr_usd` mais fraco quando a alta de commodities é de energia; ele só vale no cenário de commodities em alta, que não é nenhum dos meus três. O segundo pede que eu leia `F.b_dxy_em` como teto, porque o índice contém o real. Leio assim: nos meus cenários o dólar contra emergentes fica no base do externo, sem o salto do real, e ele vale ~+0,04 na PTAX do 4T26 (report do externo). Não peço multiplicador abaixo de 1, porque o viés é da estimação e não sei medi-lo sem o índice sem o real (seção 6).

**(ii) Saída sazonal de dezembro — fluxo financeiro** · cenário base (4T26 e 4T27)
- Hoje: o fluxo financeiro de dezembro teve média de ~−US$ 12 bi de 2010 a 2025, e novembro mais dezembro, ~−US$ 13 bi, contra ~−US$ 6 bi de dois meses quaisquer; em 2024 e 2025 foram ~−US$ 31 bi e ~−US$ 27 bi (`cmb_cambio_contratado`).
- Por que o modelo não vê: a equação (F) não tem termo sazonal. O resíduo dela no 4º trimestre foi positivo em 8 dos 9 anos desde 2017, com média de +2,1% (Modelo Estrutural)[^sazonal]. Na amostra inteira a média é +0,3% e não se distingue de zero, então é um efeito recente, que coincide com a remessa de renda recorde (Q2).
- Efeito: +2,1% sobre o modelo no trimestre de dezembro: 5,43 → 5,54 no 4T26 e 5,51 → 5,63 no 4T27.
- Onde entra: assimetria do base no 4T26 e no 4T27 (não move a central).

**(ii) Posicionamento — o que sobra da desmontagem da posição comprada em real** · cenários upside e base
- Hoje: fundos alavancados e asset managers comprados em ~70 mil contratos, percentil 95 em 10 anos (`cmb_cot_fx` · 20/10). O real perdeu até 12% na noite de 25/10 e devolveu parte em 27/10 (Q3).
- Por que o modelo não vê: nenhuma exógena da (F) mede posição.
- Efeito: +1% no 4T26, só no upside; no base, peso pequeno na assimetria do 4T26. Volta a +2% se o COT de 27/10 mostrar a posição ainda comprada.
- Onde entra: limite do upside e assimetria do base no 4T26.

**(ii) O BC no mercado de câmbio — venda à vista e linhas** · cenário upside
- Hoje: reservas de ~US$ 365 bi (`cmb_reservas_bc` · 26/10). Em setembro o BC vendeu US$ 2 bi à vista e US$ 2 bi em linhas; em outubro, só a rolagem de swap de 27/10 (InfoMoney · 27/10 · nível B).
- Por que o modelo não vê: a intervenção não é exógena da (F).
- Efeito: −1,5% no 4T26 e −1% no 1T27, só no upside. O BC não vendeu num pregão de +9%, então só entra quando o mercado deixar de funcionar; isso limita a cauda, não a elimina.
- Onde entra: limite do upside.

### 3.3 Da etapa 1 à tese

| Trimestre | Central (P2) | Upside: modelo → com tempero | Downside: modelo → com tempero |
|---|---|---|---|
| 4T26 | 5,427 | 5,64 → 5,67 (CDS × 1,2) → 5,64 (posição +1%, BC −1,5%) | 5,28 → 5,27 (S&P × 0,55) |
| 1T27 | 5,515 | 5,87 → 5,94 → 5,88 (BC −1%) | 5,35 → 5,33 |
| 2T27 | 5,517 | 5,88 → 5,96 | 5,36 → 5,34 |
| 3T27 | 5,501 | 5,83 → 5,90 | 5,37 → 5,33 |
| 4T27 | 5,511 | 5,82 → 5,89 | 5,40 → 5,36 |
| 1T28 | 5,528 | 5,83 → 5,89 | 5,43 → 5,38 |

Cada limite da faixa base fica entre a central e o ponto de cauda com tempero, logo antes dele. No 4T26, o de cima (5,60) contém a PTAX de 26/10 e a central com a sazonalidade (5,54). O upside pesa mais no 4T26 e no 1T27, pela sazonalidade e pelo prêmio fiscal ainda não testado. De 2T27 a 4T27 a cauda de alta do fiscal mais provável contrabalança o S&P com peso menor e a valuation; no 1T28, sem a sazonalidade, a assimetria fica negativa.

## 4. Para os outros agentes

**Respostas às entradas fixas**

- **E1, em destaque (persistência):** persistente, mesmo com a correção de 27/10. O salto é o mercado passando de uma probabilidade de vitória de Flávio a um quarto mandato de Lula (CNN Brasil · 25/10 · nível A), e a PTAX de 26/10 ficou 5,3% acima da de 02/10, véspera do 1º turno. O dólar comercial a R$ 5,35 em 27/10 (Poder360 · 27/10 · nível B) devolve o exagero do pregão, não o resultado. Central de 5,43 a 5,53 em todo o horizonte, contra 5,04 em 22/10.
- **E2, em destaque (global ou idiossincrático):** idiossincrático. Em 05/10, o real caiu 4,55% contra 0,31% a 1,95% dos pares e 0,37% do dólar contra emergentes (Q3, tabela). Em 26/10, o real subiu 9,2% com o DXY a +0,15%, o S&P a +0,70% e o peso mexicano se apreciando 0,56% (Investing.com México · 26/10 · nível B). A prova por dado de 26/10 fica para o próximo ciclo.
- **E3, em destaque:** o Copom condicionou a projeção a R$ 5,15 pela PPC (report de política monetária)[^condicionante]. A PTAX estava 2,2% abaixo disso em 23/10 e 6,8% acima em 26/10. O câmbio de partida de 04/11, média dos dez dias úteis encerrados em 30/10, tem seis dias com dado no F (média 5,11). Com os quatro que faltam entre R$ 5,35 e 5,50, ele dá ~5,21 a ~5,27, só 1% a 2% acima do condicionante: a projeção de novembro carrega pouco do choque. O de 09/12 cai, no meu base, dentro da faixa do 4T26 (5,30 a 5,60), de 3% a 9% acima de 5,15, e é nessa reunião que o câmbio chega inteiro à projeção.
- **E4, em destaque:** CDS e real andaram juntos em 26/10 (+18 p.b. e +9,2%) com o DXY parado, e contra os pares em 05/10 (Q3). O prêmio é fiscal e de juro local, não de calote em dólar (leitura do fiscal): o real carrega estresse que o CDS não mede. Institucional: Galípolo disse que fica no BC até 2028 (CNN Brasil e Poder360 · 27/10 · nível B), e Lula, antes da votação, que quer "que o Banco Central baixe o juro" (Poder360 · 24/10 · nível B). É risco dito, sem decisão.
- **E5, em destaque:** carry e real se descolaram. O DI de 1 ano menos a meta do Fed subiu de ~9,1 para ~10,8 p.p. e o real caiu 9% no mesmo pregão (Q2). Uma alta em 09/12 aprecia o real só na leitura de credibilidade; na de dominância (~10%), não (upside com a NTN-B no base, seção 3.1).
- **E6:** sem intervenção nova no câmbio. Não houve venda à vista nem de linha em outubro até 26/10 (`cmb_reservas_bc`), só a rolagem de swap de até US$ 4 bi em 27/10 (InfoMoney · 27/10 · nível B). A disfunção ficou no mercado de títulos, e foi o Tesouro quem agiu, cancelando leilões e recomprando títulos (InfoMoney/Estadão Conteúdo · 26 e 27/10 · nível A). O cupom cambial não está no dado. Não marco em destaque: a condição do mapa (intervenção ou pico do cupom) não aconteceu.
- **E7 (inflação):** a tese por trimestre (seção 1) e E1.
- **E8, em destaque (inflação):** há risco relevante de depreciação. A probabilidade de a PTAX fechar o 4T26 acima de 5,60 é de 31% (era 33% na rodada 1), e a de fechar o 1T27 acima de 5,78, de 30%. O risco é puxado pelo prêmio fiscal e, no 4T26, pela saída de dezembro, e é idiossincrático (E2), o que sustenta o seu repasse com prêmio doméstico. No upside do modelo, o IPCA de 12 meses do 1T27 vai a 5,06%, contra 4,95% no base; o repasse é seu.
- **E9 (atividade):** PTAX de 5,43 no 4T26 (faixa de 5,30 a 5,60) e 5,52 no 1T27 (5,34 a 5,78), persistente (E1).
- **E10 (atividade):** termos de troca: o preço está a favor (IC-Br +12,8% em 12 meses, petróleo exportado de ~US$ 44 bi para ~US$ 54 bi), mas a Funcex caiu 3,0% em três meses até agosto. O F não traz volume para separar preço de quantidade.
- **E11, em destaque (fiscal):** o idiossincrático domina e o CDS andou junto, nos dois pregões; em 05/10 com prova contra os pares (Q3).
- **E12 (fiscal):** a tese. O BC só rolou swap em outubro. O estoque vendido de ~US$ 92 bi (`cmb_reservas_bc` · ago) vezes a variação da PTAX de 23 para 26/10 dá ~R$ 42 bi de perda só pela variação cambial; contra 30/09, ~R$ 29 bi. É conta sobre o estoque de agosto e ignora o cupom e o diferencial de juros.
- **E13, em destaque (externo):** idiossincrático (E2). O dólar contra emergentes de 26/10 em diante contém o salto do real; não o leia como movimento global, que é o que o seu caminho já faz.
- **E14 (externo):** o fluxo financeiro foi positivo em ~US$ 4 bi até 16/10, e a posição comprada em real estava no percentil 95 em 20/10: o apetite chegou ao Brasil por dinheiro e por posição antes do choque. Pelo caminho do preço, a posição saiu em boa parte em 26/10, mas o F não tem fluxo nem COT depois disso (XS2): um risk-off que viesse agora provavelmente encontraria o real com menos posição comprada do que em 20/10.
- **E15 (expectativas):** persistente e idiossincrático (E1, E2), com a tese por trimestre: é o caso que chega aos horizontes longos. A correção de 27/10 não muda a duração do seu tempero: ela é o exagero saindo, não o prêmio.

**Pedidos para o próximo ciclo**

- **S1 (política monetária):** a decisão de 04/11, e quanto sobe a probabilidade de alta em 09/12 se a PTAX ficar acima de 5,50 até lá. Depende dela o carry do 1T27 e a versão do upside que vale.
- **S2 e S7 (política monetária e fiscal):** depois de 04/11, a pausa ou a alta foi lida como credibilidade? A cauda de dominância passou de ~10%? Decide entre as duas versões do upside.
- **S3 (política monetária):** o câmbio de partida que o Copom de fato usou em 04/11, e como o comunicado descreveu o câmbio. Depende E3.
- **S4 (política monetária):** respondido nesta rodada (reação pela segunda ordem e pela projeção, sem postura de defesa do câmbio). Sigo acompanhando se a condição do mapa para ampliar a pergunta acontece.
- **S5 (inflação):** o IPCA de 12 meses do P2 (5,34% no 4T26 e 4,14% no 1T28) é a perna de PPC que uso. Avise se a cauda de combustíveis mudar.
- **S6 (fiscal):** o caminho do CDS depois do envio do projeto de lei complementar e do nome do ministro da Fazenda. Os dois decidem as caudas.
- **S8 e S9 (externo):** os caminhos do bloco global, e os pares e o dólar contra emergentes de 21/10 em diante, quando entrarem no F. Fecham a prova de E2.
- **S10 (expectativas):** a revisão do Focus de 30/10 e da seguinte para o câmbio de 2026 e 2027, contra o que os 45 episódios desde 2001 dão. Separa surpresa de convergência.
- **Ao agente web:**
  1. A volatilidade implícita de 3 meses do dólar contra o real depois de 26/10, em qualquer veículo. Sou o principal dessa exógena, ela não está no F, e as duas rodadas não acharam nada.
  2. O conteúdo e a data de envio do projeto de lei complementar de Durigan (meta, mecanismo, prazo) e o anúncio do ministro da Fazenda do próximo mandato. Dependem as probabilidades das duas caudas.
  3. Leilão à vista, de linha ou de swap novo do BC depois de 27/10, e falas de diretores sobre câmbio. Depende o tempero do BC e E6.

**Como subordinado**

- **Dólar contra emergentes · principal: externo**
  - Insumos: o índice vai conter movimentos do real que são do Brasil (05/10 e 26/10, Q3). Em outubro, a alta do índice se concentrou no peso mexicano, por desmontagem de carry (Investing.com México · 22/10 · nível B), com os asset managers vendidos em peso no percentil 0 (`cmb_cot_fx` · 20/10). Em 26/10 o peso mexicano se apreciou (Investing.com México · 26/10 · nível B).
  - Argumento: nenhum além do da rodada 2; o risco no seu base é para baixo, se o peso mexicano se recuperar.
  - Caminho de referência: nenhum.
  - Resposta do principal: o externo aceitou o argumento. O caminho segue o dólar global sem o salto do real, e a cauda de cima passou a 28% para o índice publicado carregar o salto (report do externo, Divergências). Divergência fechada. Sobre XS1, o peso do real no índice: o F não traz os pesos da cesta, então não tenho número melhor que o seu (~0,07 pela regressão diária).
- **IC-Br em dólar · principal: externo**
  - Insumos: exportações em recorde e petróleo em alta (Q2). O minério de ferro caiu à mínima de dois anos, e Mengtian Jiang (Horizon Insights) disse que ele "is likely to stay soft through November" (Yahoo Finance/Bloomberg · 27/10 · nível B).
  - Argumento: nenhum além do da rodada 2; o risco é nos metais, e o externo já pôs 30% na cauda de baixa deles.
  - Caminho de referência: nenhum.
  - Resposta do principal: aceitou o argumento da rodada 1 para outubro e subiu o 4T26 de 204,8 para 206,2, pelo agro (report do externo, Divergências). Divergência fechada.

**Divergências** (volatilidade implícita, de que sou principal)

- Nenhum subordinado argumentou sobre `vol`, e nem o P1 nem o P2 listam divergência nela.
- Mantenho o caminho base (17,0 → 13,5), pelo motivo da seção 3.1.

## 5. Placar

Primeiro ciclo: não há report final anterior do câmbio, porque o ciclo de 22/10 não tem `cambio_rf`. O 3T26 fechou com a PTAX em 5,18 (30/09, `cmb_ptax`), sem tese final em vigor para conferir.

## 6. Sobre o modelo

Ciclo sem literatura: as propostas vêm do dado e do mapa.

| Fonte | O que sugere | Teste proposto | Por que importa para a tese deste ciclo |
|---|---|---|---|
| Resíduo da (F) por trimestre (Modelo Estrutural, 2006–2026) e fluxo financeiro de dezembro (`cmb_cambio_contratado`) | Dummy de 4º trimestre, ou o fluxo financeiro de nov–dez como regressor, com quebra em 2017 | Reestimar a (F) com a dummy na amostra inteira e com interação pós-2017. Mudar se a dummy pós-2017 tiver intervalo de 90% acima de zero e o erro fora da amostra de 2021–2025 cair | A central do 4T26 fica abaixo da PTAX de hoje, e a sazonalidade explica a maior parte da distância; hoje ela é tempero |
| Volatilidade implícita sem 3T26 e fora do banco (mapa, 2.7; modelo segura 12,19) | Trazer a implícita para o banco; até lá, preencher o trimestre faltante pela realizada (implícita ≈ 6,65 + 0,274 × realizada 21d + 0,389 × realizada 63d, erro 2,1 p.p.) | Comparar a (F) estimada com a implícita preenchida contra a atual nos trimestres em que as duas existem. Adotar se o coeficiente do carry/vol não sair do intervalo | Sou o principal da vol e escrevo o caminho sem o dado de hoje; é o canal que mais move a central do 4T26 |
| Sensibilidade da PTAX ao CDS por nível (G deste ciclo, 2006–2026): diária 0,42% por 10 p.b. com CDS < 200 contra 0,26% na amostra; trimestral 0,57% contra 0,85% | CDS em log na (F), como o fiscal propõe, ou interação ΔCDS × nível | Reestimar a (F) trimestral com Δlog(CDS) e com a interação. Mudar se o coeficiente em log for estável entre 2006–2015 e 2016–2026 e o em p.b. não, ou se a interação tiver sinal e intervalo fora de zero | Decide se o peso do CDS no upside é multiplicador ou especificação |
| Sinal do S&P 500 na (F): +1,89 por desvio (alta da bolsa americana deprecia o real), contra o mecanismo do mapa (2.3); no P2 vale +0,12 na PTAX do 1T28 | O sinal é condicional ao dólar contra emergentes (e ao CDS) na mesma equação | Reestimar sem o dólar contra emergentes e medir a correlação entre as duas variações. Se o sinal virar, ou se o coeficiente perder significância, tirar o S&P da (F) ou entrar com ele ortogonalizado | É a maior contribuição externa à central de 2027–28 e a razão da assimetria negativa do 1T28 |
| O dólar contra emergentes contém o real (peso ~0,07 pela regressão diária do externo) | A (F) estimada com o índice publicado lê parte dos movimentos do próprio real como dólar global | Reestimar a (F) com o índice sem o real (reconstruído pelos pesos da cesta, que o banco não tem, ou por resíduo da regressão do índice no real). Mudar se `F.b_dxy_em` cair fora do intervalo atual | Decide se o coeficiente do dólar contra emergentes é teto, como o externo pede, e o tamanho do risk-off no real |

[^ptax]: A PTAX é a taxa de câmbio de referência calculada pelo Banco Central a partir das cotações do dia. O report projeta a PTAX de venda do último dia útil de cada trimestre (4T26 = 31/12/2026).
[^modelo]: O Modelo Estrutural resolve juntas cinco equações (hiato, inflação, expectativas, Selic e câmbio). O P2 é a rodada do modelo com o caminho de cada premissa escrito pelo agente responsável por ela, depois de duas rodadas de discussão. A faixa que o modelo imprime mede só a incerteza sobre os pesos estimados; a distribuição da tese é do agente.
[^processo]: O F não traz dado eleitoral: o resultado das eleições e as falas citadas vêm das notícias do ciclo, com o veículo, a data e o nível de cada uma. Nível A é fato confirmado por documento ou por dois veículos com atribuição nominal. Nível B é fonte identificada, e prova que a pessoa disse, não que vai acontecer. Nível C é fonte anônima e só entra como expectativa ou risco.
[^split]: Global ou idiossincrático: se o real cai junto com os pares e com os índices de dólar, o motivo é global; se cai sozinho, é do Brasil. A comparação é feita no mesmo período para todos.
[^pctl]: Percentil é a posição do número no histórico: 0 é o menor já visto, 100 o maior. No volume, percentil 19 quer dizer que em 81% dos meses dos últimos 10 anos o volume foi maior.
[^posbancos]: Posição à vista dos bancos: quanto os bancos compraram menos o que venderam de dólar à vista, acumulado. Vendida e crescendo quer dizer que eles financiam saída de dólar com o próprio balanço, sinal de escassez de dólar no mercado à vista.
[^cot]: O COT é o relatório semanal da CFTC com as posições em contratos futuros de real em Chicago. Posição extrema funciona como sinal contrário: quando os fundos já estão muito comprados em real, sobra pouco comprador novo, e um choque faz muitos venderem ao mesmo tempo.
[^carry]: Carry é o ganho de aplicar no juro brasileiro, mais alto, financiado em dólar ao juro americano. Ele atrai capital e sustenta o real enquanto o câmbio não oscila demais; por isso o modelo usa o carry dividido pela volatilidade. Exemplo: o mesmo diferencial de juros, dividido por uma volatilidade maior, dá um quociente menor, e o modelo lê isso como menos atração para o real.
[^dominancia]: Dominância fiscal é quando a dívida pública pesa tanto que subir os juros piora a percepção de risco em vez de atrair capital: a alta encarece a dívida, o prêmio sobe e a moeda se deprecia, ao contrário do usual.
[^reer]: O câmbio real efetivo (BIS) compara o real com uma cesta de moedas de parceiros, corrigido pelas inflações. Alta do índice é real mais caro.
[^mult]: Multiplicador: o peso que o modelo estima para cada canal tem uma faixa de valores plausíveis (o intervalo de 90%). Multiplicar o peso por 1,2 é dizer que, num cenário, o canal age 20% mais forte que a estimativa central, ainda dentro dessa faixa; sair dela é afirmar que o histórico subestima o canal.
[^sazonal]: Resíduo é a parte da variação trimestral do câmbio que o modelo não explica. Positivo no 4º trimestre quer dizer que, em dezembro, o real costuma se depreciar mais do que o modelo prevê; é a época de remessa de lucros e dividendos.
[^condicionante]: O Copom projeta a inflação supondo um caminho para o câmbio; hoje, um caminho que parte de R$ 5,15 e segue a paridade do poder de compra (o câmbio corrigido pela diferença entre a inflação brasileira e a americana). O ponto de partida é a média da PTAX nos dez dias úteis antes da semana da reunião. Câmbio de mercado acima desse caminho é risco de inflação mais alta que a projetada.
