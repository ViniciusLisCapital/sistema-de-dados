# Report — câmbio · ciclo 2026-10-27 · rodada 2

Dados até: 27/10/2026 (PTAX até 26/10); notícias até 27/10 · Horizontes: 4T26 a 1T28, USD/BRL pela PTAX de venda do último dia útil de cada trimestre[^ptax]

## 1. Tese

| Variável | Trimestre | Central | Base: faixa · P | Upside: limite · P | Downside: limite · P | P(up) − P(down) |
|---|---|---|---|---|---|---|
| USD/BRL, PTAX de fechamento | 4T26 | 5,435 | 5,30 a 5,60 · 47% | acima de 5,60 · 31% | abaixo de 5,30 · 22% | +0,09 |
| | 1T27 | 5,503 | 5,33 a 5,75 · 46% | acima de 5,75 · 30% | abaixo de 5,33 · 24% | +0,06 |
| | 2T27 | 5,508 | 5,33 a 5,80 · 45% | acima de 5,80 · 28% | abaixo de 5,33 · 27% | +0,01 |
| | 3T27 | 5,495 | 5,32 a 5,80 · 44% | acima de 5,80 · 27% | abaixo de 5,32 · 29% | −0,02 |
| | 4T27 | 5,526 | 5,35 a 5,82 · 44% | acima de 5,82 · 29% | abaixo de 5,35 · 27% | +0,02 |
| | 1T28 | 5,565 | 5,37 a 5,84 · 43% | acima de 5,84 · 26% | abaixo de 5,37 · 31% | −0,05 |

A central é a PTAX do P1, sem ajuste[^modelo].

- **Upside (real mais fraco, ruim para a inflação e para o Brasil):** as decisões fiscais de 2027 confirmam a leitura que o mercado fez da reeleição. Com o CDS a 165 p.b. no 4T26 e 190–200 em 2027, a NTN-B de 10 anos a 8,80–9,00% (os caminhos de cauda do fiscal) e a volatilidade implícita a 24%, o modelo dá 5,62 no 4T26 e 5,82 no 2T27; com o peso do CDS × 1,2, 5,65 e 5,89; com o resto da desmontagem de posição (+1%) e o BC vendendo dólar (−1,5%), 5,63 no 4T26. Se a alta da Selic que o modelo faz nesse cenário (14,19% no 1T27) não segurar o real, que é a cauda de dominância fiscal, o upside vai a 5,66 no 4T26 e 5,93 no 2T27.
- **Downside (real mais forte, bom para a inflação):** o projeto que o ministro da Fazenda anunciou para mirar o centro da meta fiscal convence o mercado. Com o CDS de 115 a 105 p.b., a NTN-B de 10 anos de 7,35% a 6,70% (as caudas do fiscal) e a volatilidade a 12–13%, o modelo dá 5,26 no 4T26 e 5,42 no 1T28; com o peso que o modelo dá ao S&P 500 reduzido a 55%, 5,25 e 5,36.
- **A tese em uma frase:** a reeleição levou o real a um patamar que não reverte sozinho; o P1 põe a PTAX entre 5,44 e 5,57 em todo o horizonte, a saída sazonal de dezembro e o prêmio fiscal ainda não testado inclinam o 4T26 e o 1T27 para a depreciação, e de meados de 2027 em diante o risco fica equilibrado, porque parte da alta da central vem de um canal do modelo, o S&P 500, cujo sinal o mecanismo não sustenta.

## 2. Argumentação

### Q3 — O que explica a dinâmica recente

**A eleição explica o mês, e o saldo dela é um real mais fraco que antes do 1º turno.** O real se apreciou depois do 1º turno e se depreciou depois do 2º:
- Em 05/10, depois do 1º turno de 04/10 com Flávio Bolsonaro à frente, a PTAX caiu 4,55% contra 02/10 (`cmb_ptax`), e a leitura dos investidores foi de "redução do prêmio de risco dos ativos brasileiros" (Agência Brasil · 05/10 · nível A).
- Em 26/10, depois da reeleição de Lula em 25/10 (CNN Brasil · 25/10 · nível A), a PTAX subiu 9,19%, de 5,0377 em 23/10 para 5,5007 (`cmb_ptax`). Segundo a CNN, "o mercado vinha tratando a vitória de Flávio como a possibilidade de uma virada na política fiscal do governo" (CNN Brasil · 25/10 · nível A).
- O saldo: a PTAX de 26/10 está 5,30% acima da de 02/10 (5,2238, véspera do 1º turno) com o CDS 6 p.b. mais alto, de 131 para 137 (`cmb_risco_pais`), o que mostra que o mercado não só desfez o que tinha precificado em 05/10 como passou a cobrar um prêmio acima do de antes do 1º turno, quando o resultado ainda estava em aberto[^processo]. Desde o fechamento do 3T26 (5,1809 em 30/09) a alta é de 6,17% (`cmb_ptax`).

**Parte do exagero de 26/10 já voltou no próprio choque.** No pior momento, na noite de 25/10, o real chegou a perder 12% (CNN Brasil · 25/10 · nível A); o dólar à vista fechou 26/10 em alta de 8,36% e, às 9h52 de 27/10, caía 1,29%, a R$ 5,333, segundo o InfoMoney (InfoMoney · 27/10 · nível B). O ministro da Fazenda, Dario Durigan, disse que a reação foi "de posição" e não de desconfiança nas contas públicas (Poder360 · 27/10 · nível B): é a fala de quem tem interesse em dizê-la e não prova a causa, mas o caminho do preço (12% na noite de domingo, 8,4% no fechamento de segunda, devolução na terça) é o de uma desmontagem concentrada num pregão. Isso pesa contra o tempero de posicionamento da rodada 1 (Q1). Mas a PTAX de 27/10 não está no F, e os 5,333 são cotação intradiária do dólar à vista, não PTAX.

**O movimento é idiossincrático, e agora há prova pelos pares num dos dois pregões.**[^split] Em 05/10, mesma natureza de evento, o real caiu 4,55% e nenhum par passou de 1,95%:

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

O dólar subiu contra os desenvolvidos e caiu pouco contra os emergentes (num índice que contém o próprio real), enquanto o real caía 4,55%, com o CDS −12 p.b. (`cmb_risco_pais`): a apreciação foi do Brasil. Em 26/10 o DXY subiu 0,15% (`cmb_dollar_index`) e o S&P 500 0,70% (`cmb_equity_us`), sem fuga de risco global, e o CDS subiu 18 p.b. Mas os pares não têm dado depois de 15–20/10 (`cmb_fx_latam`) e o dólar contra emergentes, depois de 23/10 (`cmb_dollar_index_em`), então a prova pelos pares de 26/10 continua faltando; a causa ser a eleição torna improvável que eles tenham caído junto.

**O CDS explica pouco do salto, e isso não é novidade do canal.** Pelo modelo, o CDS de 26/10 explica +1,63% dos +9,18% desde 22/10 (rodada 1). Testei o argumento do fiscal de que o real reage mais a um p.b. de CDS quando o CDS está baixo: no dado diário de 2006–2026, com o dólar contra emergentes como controle, a PTAX sobe 0,42% por 10 p.b. quando o CDS está abaixo de 200 p.b., contra 0,26% na amostra inteira e 0,07% acima de 400 (`cmb_ptax`, `cmb_risco_pais`, `cmb_dollar_index_em`). Mas no dado trimestral, que é a frequência do modelo, a relação se inverte: 0,57% por 10 p.b. com o CDS abaixo de 200 contra 0,85% na amostra inteira (mesmas tabelas, 2006–2026). O pregão amplifica o CDS quando ele está baixo, e o trimestre devolve parte disso, como 26/10 já começou a devolver. É por isso que fico com o peso do CDS × 1,2 no upside e não aceito o × 1,5 (seção 3.2).

**A expectativa ainda não viu o salto.** A mediana do Focus para o fim de 2026 era 5,05 em 23/10, revisada de 5,20 quatro semanas antes (`expc_focus_periodo` câmbio), pesquisa fechada antes de 26/10. A revisão de 30/10 não está no F deste ciclo.

### Q1 — Condições do mercado de câmbio

**O BC deixou o preço andar.** Não há intervenção à vista nem de linha em outubro até 26/10 (`cmb_reservas_bc` · 26/10), e em 27/10 o BC fez o leilão de rolagem de swap cambial de até US$ 4 bi, que é a rolagem programada do estoque; a página não registra leilão à vista ou de linha (InfoMoney · 27/10 · nível B). O mercado que travou foi o de juros: uma analista da Empiricus, Lais Costa, disse que "o mercado está muito disfuncional" (InfoMoney/Reuters · 26/10 · nível B), e o Tesouro cancelou os leilões de prefixados e indexados de 27 a 29/10 (InfoMoney/Estadão Conteúdo · 26/10 · nível A). Um câmbio que sobe 9% sem o BC vender dólar, com o Tesouro saindo do mercado de títulos, mostra que o BC leu preço e não disfunção no câmbio. Mas o cupom cambial, que mostraria escassez de dólar no mercado local, não está no dado, e as reservas de US$ 364,9 bi (`cmb_reservas_bc` · 26/10) e a intervenção de setembro (US$ 2 bi à vista e US$ 2 bi em linhas, com a PTAX entre 5,12 e 5,21) mostram que o BC tem o instrumento e já o usou neste ano.

**Mercado fino antes do choque.** O volume interbancário D+2 teve média de US$ 985 mi/dia no último mês, percentil 19 em 10 anos[^pctl] (`cmb_ptax` · 23/10), o que ajuda a explicar 9% num pregão; o D+1 está no percentil 67, então não é falta de liquidez em todo prazo. Os bancos fecharam setembro vendidos em US$ 26,2 bi no mercado à vista, percentil 24 em 10 anos (`cmb_reservas_bc` · set)[^posbancos].

**Posição muito comprada em real quando o choque veio, provavelmente já reduzida.** Em 20/10 os fundos alavancados e os asset managers estavam comprados em ~70 mil contratos, percentil 95 em 10 anos, com as posições em aberto no percentil 98 (`cmb_cot_fx` · 20/10)[^cot]. A posição extrema é o que faz um choque virar 12% numa noite; o caminho do preço de 25 a 27/10 (Q3) sugere que boa parte dela saiu no próprio pregão. Mas o COT de 27/10 não está no F: se ele mostrar a posição ainda comprada, o tempero de posicionamento volta ao tamanho da rodada 1.

**Fluxo: entrada antes do choque, sem dado depois.** De 1º a 16/10 o fluxo cambial foi positivo em US$ 5,15 bi, US$ 4,13 bi pelo financeiro (`cmb_cambio_contratado` · 16/10), coerente com a apreciação depois do 1º turno. O fluxo de 26/10 não está no F.

### Q2 — Fundamentos

**Carry alto e mais alto depois do choque, mas descolado do real.** O diferencial real ex-post era 9,14 p.p. em setembro, percentil 81 em 10 anos (`diferenciais_juros` · set)[^carry]. No pregão em que o DI de 1 ano menos a meta do Fed foi de 9,14 para 10,82 p.p. (`br_di_grade`, `us_interest_rate`, 22 e 26/10), o real caiu 9%. A política monetária lê que uma pausa hoje é lida como credibilidade, mas que uma alta só o é se vier com sinal de que o Copom reage aos efeitos de segunda ordem; sem ele, num choque de prêmio fiscal e político, ela pode ser lida como custo da dívida (report de política monetária, E2). O fiscal vê dois dos três sinais de dominância presentes, nenhum completo, e põe a cauda de dominância em ~10% (report do fiscal, F5)[^dominancia]. Por isso o upside tem uma versão em que a alta da Selic do modelo não segura o real (seção 3.1). A volatilidade também come o carry: a realizada de 63 dias foi de 12,3% em 23/10 (`cmb_ptax`) para 21,4% em 26/10, percentil 96 em 10 anos ("O real e os pares" · 26/10).

**Contas externas não são o problema; a saída financeira é.** Déficit em transações correntes de US$ 60,0 bi em 12 meses, 2,33% do PIB, contra investimento direto de US$ 88,3 bi, 3,43% do PIB, percentil 93 (`cmb_balanco_pagmt` · set), e exportações de bens em recorde, US$ 376,6 bi. Mas a renda primária tem o maior déficit da série (−US$ 84,2 bi em 12 meses) e o fluxo financeiro de 12 meses é de −US$ 62,3 bi, percentil 18 (`cmb_cambio_contratado` · set), com remessa de renda no percentil 6: é essa saída que se concentra em dezembro (seção 3.2).

**Termos de troca bons, sem papel no mês.** O IC-Br em dólar está 12,8% acima de um ano antes (`comm_icbr_usd` · set) e o petróleo exportado somou US$ 54,1 bi em 12 meses, contra US$ 43,9 bi um ano antes (`cmb_comex_produto` · set). Mas os termos de troca da Funcex caíram 3,0% em três meses até agosto (`cmb_termos_troca`), e o Brent recuou de 135,51 em 02/10 para 115,22 em 20/10 (`comm_brent`) num mês em que o real foi e voltou com a eleição.

**Valuation: neutra antes do choque, barata depois.** O câmbio real efetivo estava no percentil 53 em 10 anos em setembro (`cmb_reer` · set)[^reer], e a PTAX de 26/10 está 6,92% acima da média de setembro (`cmb_ptax`). O real mais barato sustenta o downside de 2027, e não entra no modelo.

### Q4 — Por que a central e por que a distribuição

**A central.** É a PTAX do P1: 5,435 no 4T26, 5,50 em 2027 e 5,565 no 1T28 (seção 3.1). Ela subiu de 0,06 a 0,19 contra a da rodada 1 porque o P1 usa os caminhos do externo e do fiscal em vez dos níveis de hoje segurados. O que move a PTAX do modelo, canal a canal:
- A volatilidade implícita de 17% no 4T26 divide o carry e é o canal que mais pesa no primeiro trimestre[^carry]; ela recua a 13,5% no fim de 2027 e devolve apreciação.
- A Selic do modelo cai de 13,34% no fechamento do 4T26 para 11,91% no 1T28 e tira carry, o que deprecia o real ao longo de 2027. É a Selic da regra do modelo: a política monetária tem 13,49% e 12,39% nos mesmos trimestres, e a curva precifica 15,78% em dez/27 (`br_di_grade` · 26/10).
- O CDS do fiscal sobe de 131 no 3T26 para 140 no 4T26 e fica, o que deprecia pouco (+0,75% contra o padrão, report do fiscal).
- O S&P 500 do externo sobe de 7.750 no 4T26 a 8.500 no 1T28, e o modelo lê isso como depreciação: +0,005 na PTAX do 4T26 e +0,12 (2,2%) na do 1T28, contra o S&P parado em 7.717 (Modelo Estrutural).

**A distribuição.** No 4T26 a central fica 1,2% abaixo da PTAX de 26/10, e duas forças que o modelo não vê a empurram para cima: a saída sazonal de dezembro, que sozinha leva a central a 5,55 (seção 3.2), e o prêmio fiscal que só as decisões de 2027 vão testar, com o fiscal dando mais chance à cauda de alta do CDS (25–28%) que à de baixa (15–18%). Contra elas: o exagero de 26/10 começou a voltar no dia seguinte (Q3), o ministro da Fazenda disse que vai "buscar o centro da meta de maneira formal" por um projeto de lei complementar (CNN Brasil · 27/10 · nível A, também Exame), e o real ficou barato. A posição comprada, que na rodada 1 empurrava o 4T26 para cima, provavelmente já saiu em boa parte. Por isso o upside do 4T26 cai de 33% para 31% e o downside fica em 22%. Em 2027 a sazonalidade só volta no 4T27, e a força para baixo é o S&P: o sinal positivo do S&P na (F) vem de ele entrar junto com o dólar contra emergentes, e o mecanismo do mapa (2.3) diz o contrário, que bolsa americana em alta é apetite a risco e real mais forte. Com o peso reduzido a 55%, a PTAX do base fica 0,06 mais baixa no 1T28 (5,51). Somado ao real barato, isso leva a assimetria a −0,02 no 3T27 e −0,05 no 1T28; no 4T27 a sazonalidade a devolve a +0,02. A faixa para de abrir depois do 2T27 porque os caminhos de cauda do fiscal param de se afastar ali; a incerteza que cresce com o horizonte entra na probabilidade da faixa, que cai de 47% para 43%.

**O que derrubaria a tese:** a PTAX abaixo de 5,30 por duas semanas com o CDS abaixo de 120 p.b. leva a probabilidade para o downside; o CDS acima de 160 p.b. por dez pregões, ou a PTAX acima de 5,70 por uma semana sem venda do BC, leva o 4T26 para o upside.

### Olhado, sem sinal

- Estoque de swaps cambiais · −US$ 91,6 bi (`cmb_reservas_bc` · ago) · dado de agosto, e a rolagem de 27/10 só renova o estoque · diria algo se o BC ofertasse swap novo acima dos vencimentos.
- Reservas no conceito de liquidez · US$ 368,9 bi (`cmb_reservas_bc` · 26/10) · +1,0 no mês, sem venda · diria algo se caíssem com leilões à vista.
- Carteira, ações · −US$ 5,3 bi em 12 meses, percentil 10 (`cmb_balanco_pagmt` · set) · saída lenta, sem mudança no mês · diria algo se a saída de setembro (−US$ 2,1 bi) se repetisse em outubro, com o choque.
- Exportação para os EUA · US$ 35,8 bi em 12 meses contra US$ 40,4 bi um ano antes (`cmb_comex_pais` · set) · compensada pela China · diria algo se a queda chegasse ao saldo total.
- Treasury de 10 anos · 5,00% (`us_interest_rate` · 23/10) · −0,11 p.p. no mês · diria algo se a alta de 12 meses (+0,99 p.p.) voltasse.
- Fala de Galípolo sobre a escala 6x1, "a gente vai esperar a implementação para saber se precisa agir" (InfoMoney · 27/10 · nível B) · não trata de câmbio nem da reunião de 04/11 · diria algo se ligasse o mercado de trabalho à decisão de juros.

## 3. Premissas

### 3.1 Etapa 1 — o modelo

**Cenários.**
- **Base:** Lula reeleito (CNN Brasil · 25/10 · nível A); as decisões fiscais de 2027 demoram e não confirmam nem ruptura nem consolidação (o base do fiscal); a volatilidade sobe no 4T26 e volta devagar ao normal ao longo de 2027; o bloco global segue o base do externo.
- **Upside:** o governo afrouxa o fiscal de 2027 e o mercado lê a reação monetária como insuficiente: é o upside do fiscal. Lula disse antes da votação que quer "que o Banco Central baixe o juro" e subsidiar diesel e gasolina (Poder360 · 24/10 · nível B), e Durigan, que os subsídios aos combustíveis devem continuar em 2027 (Poder360 · 23/10 · nível B): dizer não é fazer, e é por isso que é cauda. A volatilidade fica perto dos níveis de 2015. O choque é doméstico, então o bloco global fica no base do externo.
- **Downside:** um arcabouço de 2027 que o mercado compre desfaz parte da leitura de 26/10, e os preços voltam para perto do intervalo de 05 a 23/10: é o downside do fiscal. Durigan prometeu um projeto de lei complementar para mirar o centro da meta (CNN Brasil e Exame · 27/10 · nível A) e disse que pretende ampliar o superávit de 2027 (Poder360 · 26/10 · nível B); a escolha de um ministro da Fazenda de perfil de centro, como o noticiado sobre Alckmin, é expectativa e não fato (Reuters via CNN Brasil · 05/10 · nível C, sem reação de preço registrada). A volatilidade volta aos níveis de 2025–2026. Bloco global no base do externo.

**Caminhos das exógenas.** A volatilidade implícita é minha (principal). O CDS e o juro real de 10 anos são do fiscal (principal), nos três cenários do report dele; o bloco global é do externo (principal), no base dele em todos os cenários; a meta é da política monetária. O base de todas é o do P1.

| Exógena | Hoje (valor · tabela · data) | Cenário | 4T26 | 1T27 | 2T27 | 3T27 | 4T27 | 1T28 |
|---|---|---|---|---|---|---|---|---|
| Volatilidade implícita do real (% a.a.) · principal: câmbio | sem dado no F; 12,19 no 2T26 (Modelo Estrutural) | base | 17,0 | 15,5 | 14,5 | 14,0 | 13,5 | 13,5 |
| | | upside | 24,0 | 21,0 | 18,0 | 16,0 | 15,0 | 15,0 |
| | | downside | 13,0 | 12,5 | 12,0 | 12,0 | 12,0 | 12,0 |
| CDS 5 anos (p.b.) · principal: fiscal | 137 · `cmb_risco_pais` · 26/10 | base | 140 | 140 | 138 | 135 | 135 | 135 |
| | | upside | 165 | 190 | 200 | 200 | 195 | 190 |
| | | downside | 115 | 110 | 108 | 106 | 105 | 105 |
| Juro real de 10 anos, NTN-B (% a.a., média) · principal: fiscal | 8,05 em 26/10 (report do fiscal) | base | 7,70 | 7,80 | 7,70 | 7,60 | 7,55 | 7,50 |
| | | upside | 8,05 | 8,80 | 9,00 | 9,00 | 8,90 | 8,80 |
| | | downside | 7,35 | 6,90 | 6,80 | 6,75 | 6,70 | 6,70 |
| Dólar contra emergentes (pontos) · principal: externo | 130,21 · `cmb_dollar_index_em` · 23/10 | todos | 130,5 | 131,0 | 130,5 | 130,0 | 129,5 | 129,0 |
| S&P 500 (pontos) · principal: externo | 7.717 · `cmb_equity_us` · 27/10 | todos | 7.750 | 7.900 | 8.050 | 8.200 | 8.350 | 8.500 |
| IC-Br em dólar (pontos) · principal: externo | 205,70 · `comm_icbr_usd` · set | todos | 204,8 | 203,7 | 202,9 | 202,3 | 201,8 | 201,4 |
| Fed Funds efetivo (% a.a.) · principal: externo | 3,75 · `diferenciais_juros` · set | todos | 4,13 | 4,13 | 4,13 | 4,13 | 4,13 | 3,88 |
| CPI dos EUA (% no trimestre) · principal: externo | 3,72 em 12 meses · `diferenciais_juros` · set | todos | 0,86 | 0,61 | 0,61 | 0,65 | 0,63 | 0,65 |

A meta de inflação (3,00%) e o IC-Br agropecuária e metais ficam no P1 em todos os cenários.

Motivo do caminho da volatilidade (base), mantido da rodada 1: o F não traz a implícita, e o modelo não tem o 3T26 (segura 12,19). Pela relação histórica com a realizada (implícita = 6,65 + 0,274 × realizada de 21 dias + 0,389 × realizada de 63 dias, 82 trimestres desde 2006; `cmb_ptax` e a série do Modelo Estrutural), a implícita de 31/12 seria de 17,3% a 19,3% se os pregões restantes do ano tivessem volatilidade de 8% a 13%, porque a janela de 63 dias ainda conterá 05/10 e 26/10. Fico em 17%, no piso dessa conta: os dois pregões precificaram a eleição, um evento que já passou, e a implícita é o preço do risco à frente, não do que aconteceu. Com 18,5% a central do 4T26 subiria de 5,435 para 5,456. Depois de picos, a implícita recuou em um a três trimestres (21,6 → 14,6 do 3T18 ao 4T18), e o caminho chega perto da mediana (14,3%) no 2T27. No upside, a persistência de 2015 (25,1 → 22,8 → 21,8); no downside, a volta rápida de 2018.

**Saída do modelo** (central; a faixa de 90% do posterior dos pesos não inclui o erro da equação, de ~3,6% por trimestre).

| Variável | Cenário | 4T26 | 1T27 | 2T27 | 3T27 | 4T27 | 1T28 |
|---|---|---|---|---|---|---|---|
| PTAX (R$/US$) | base (P1) | 5,435 | 5,503 | 5,508 | 5,495 | 5,526 | 5,565 |
| | upside, sem multiplicador | 5,622 | 5,791 | 5,823 | 5,796 | 5,796 | 5,816 |
| | upside, CDS × 1,2 | 5,654 | 5,848 | 5,891 | 5,863 | 5,859 | 5,874 |
| | upside, CDS × 1,2, NTN-B no base (Selic sem a alta) | 5,662 | 5,872 | 5,928 | 5,908 | 5,904 | 5,918 |
| | downside | 5,256 | 5,337 | 5,349 | 5,350 | 5,386 | 5,422 |
| Selic de fechamento (% a.a.) | base | 13,34 | 13,03 | 12,67 | 12,36 | 12,12 | 11,91 |
| | upside (CDS × 1,2) | 14,02 | 14,19 | 14,04 | 13,79 | 13,51 | 13,30 |
| | downside | 12,71 | 12,12 | 11,77 | 11,49 | 11,25 | 11,07 |
| IPCA 12 meses (%) | base | 5,32 | 4,96 | 4,48 | 4,52 | 4,38 | 4,19 |
| | upside (CDS × 1,2) | 5,35 | 5,05 | 4,64 | 4,73 | 4,59 | 4,36 |
| | downside | 5,30 | 4,89 | 4,39 | 4,42 | 4,29 | 4,13 |

Faixa de 90% do posterior da PTAX base: 5,348 a 5,525 no 4T26 e 5,336 a 5,821 no 1T28. No upside, a NTN-B a 8,80–9,00% leva a Selic do modelo a 14,19% no 1T27, e esse carry a mais aprecia o real em 0,008 (4T26) a 0,045 (3T27) contra a mesma rodada com a NTN-B no base: a linha "NTN-B no base" é a versão do upside em que a alta de juros não segura a moeda. No downside, a NTN-B a 6,70% deixa a Selic do modelo cortar até 11,07% e tira carry: sem esse corte, a PTAX ficaria de 0,013 (4T26) a 0,035 (2T27) mais baixa.

### 3.2 Etapa 2 — o tempero

**(i) CDS 5 anos — efeito mais forte que o estimado** · cenário upside
- Coeficiente: `F.b_fiscal`, estimado 25,1 por desvio-padrão da variação (298,5 p.b.), intervalo de 90% do posterior 19,5 a 30,6. Multiplicador: × 1,2 (30,1), dentro do intervalo, percentil 94 do posterior[^mult].
- Efeito: PTAX do upside de 5,62 para 5,65 no 4T26 e de 5,82 para 5,89 no 2T27.
- Por quê: o modelo é linear na variação do CDS e o estresse não é: em 26/10 o real andou 5,9 vezes o que o CDS explica no modelo, e em 05/10, 4,4 vezes (report do fiscal). O fiscal argumenta por × 1,5 no upside, fora do intervalo, porque o desvio-padrão que padroniza o peso é dominado pelos anos de CDS muito alto. O dado diário sustenta o argumento (0,42% por 10 p.b. com o CDS abaixo de 200, contra 0,26% na amostra inteira), mas o trimestral, que é o do modelo, não (0,57% contra 0,85%) (Q3). Sair do intervalo exige que o histórico subestime o canal na frequência do modelo, e ele não subestima. Com × 1,5 o upside iria a 5,70 no 4T26 e 5,99 no 2T27.
- O × 1,2 que o fiscal propõe no base não aplico: o base não tem estresse de regime, e o efeito seria de +0,008 na PTAX do 4T26.
- Onde entra: limite do upside.

**(i) S&P 500 — efeito mais fraco que o estimado** · cenário base (assimetria) e downside
- Coeficiente: `F.b_sp500`, estimado +1,89 por desvio-padrão da variação (8,4%), intervalo de 90% do posterior 0,98 a 2,79: a bolsa americana em alta deprecia o real no modelo. Multiplicador: × 0,55 (1,04), dentro do intervalo, perto do limite de baixo.
- Efeito: no base, a PTAX fica de 0,007 (4T26) a 0,059 (1T28) mais baixa, 5,43 a 5,51; no downside, de 5,26 para 5,25 no 4T26 e de 5,42 para 5,36 no 1T28.
- Por quê: o sinal contraria o mecanismo do mapa (2.3), em que bolsa americana em alta é apetite a risco e o real, moeda de beta alto, se aprecia; o próprio externo registra que o sinal é condicional ao CDS e ao dólar contra emergentes na mesma equação. Neste ciclo o canal deixou de ser pequeno: o S&P do externo sobe 10% no horizonte e é a maior contribuição externa à PTAX do 1T28 (+0,12 contra o S&P parado). Fico dentro do intervalo porque não testei o coeficiente sem o dólar contra emergentes (seção 6).
- Onde entra: assimetria do base de 2T27 em diante e limite do downside.

**(ii) Saída sazonal de dezembro — fluxo financeiro** · cenário base (4T26 e 4T27)
- Hoje: o fluxo financeiro de dezembro teve média de −US$ 11,9 bi de 2010 a 2025, e novembro mais dezembro, −US$ 13,1 bi, contra −US$ 5,6 bi de dois meses quaisquer; em 2024 e 2025 foram −US$ 31,4 bi e −US$ 26,8 bi (`cmb_cambio_contratado`).
- Por que o modelo não vê: a equação (F) não tem termo sazonal, e o resíduo dela no 4º trimestre foi positivo em 8 dos 9 anos desde 2017, com média de +2,1% (Modelo Estrutural)[^sazonal]; na amostra inteira a média é +0,3% e não se distingue de zero, então é um efeito recente, que coincide com a remessa de renda recorde (Q2).
- Efeito: +2,1% sobre o modelo no trimestre de dezembro: 5,435 → 5,55 no 4T26 e 5,53 → 5,64 no 4T27.
- Onde entra: assimetria do base no 4T26 e no 4T27 (não move a central).

**(ii) Posicionamento — o que sobra da desmontagem da posição comprada em real** · cenário upside e base
- Hoje: fundos alavancados e asset managers comprados em ~70 mil contratos, percentil 95 em 10 anos (`cmb_cot_fx` · 20/10); o real perdeu até 12% na noite de 25/10 e devolveu parte em 27/10 (Q3).
- Por que o modelo não vê: nenhuma exógena da (F) mede posição.
- Efeito: +1% no 4T26, só no upside (era +2% no 4T26 e +1% no 1T27); no base, peso pequeno na assimetria do 4T26. Volta ao tamanho da rodada 1 se o COT de 27/10 mostrar a posição ainda comprada.
- Onde entra: limite do upside e assimetria do base no 4T26.

**(ii) O BC no mercado de câmbio — venda à vista e linhas** · cenário upside
- Hoje: reservas de US$ 364,9 bi (`cmb_reservas_bc` · 26/10); em setembro o BC vendeu US$ 2 bi à vista e US$ 2 bi em linhas; em outubro, só a rolagem de swap de 27/10 (InfoMoney · 27/10 · nível B).
- Por que o modelo não vê: a intervenção não é exógena da (F).
- Efeito: −1,5% no 4T26 e −1% no 1T27, só no upside: o BC não vendeu num pregão de +9%, então só entra quando o mercado deixar de funcionar, e isso limita a cauda, não a elimina.
- Onde entra: limite do upside.

### 3.3 Da etapa 1 à tese

| Trimestre | Central (P1) | Upside: modelo → com tempero | Downside: modelo → com tempero |
|---|---|---|---|
| 4T26 | 5,435 | 5,62 → 5,65 (CDS × 1,2) → 5,63 (posição +1%, BC −1,5%) | 5,26 → 5,25 (S&P × 0,55) |
| 1T27 | 5,503 | 5,79 → 5,85 → 5,79 (BC −1%) | 5,34 → 5,32 |
| 2T27 | 5,508 | 5,82 → 5,89 | 5,35 → 5,32 |
| 3T27 | 5,495 | 5,80 → 5,86 | 5,35 → 5,31 |
| 4T27 | 5,526 | 5,80 → 5,86 | 5,39 → 5,34 |
| 1T28 | 5,565 | 5,82 → 5,87 | 5,42 → 5,36 |

Cada limite da faixa base fica entre a central e o ponto de cauda com tempero, logo antes dele: o de cima no 4T26 (5,60) contém a PTAX de 26/10 e a central com a sazonalidade (5,55), e os de baixo ficam acima dos pontos de downside (5,25 a 5,36). O upside pesa mais no 4T26 e no 1T27 pela sazonalidade e pelo prêmio fiscal ainda não testado; do 2T27 em diante o S&P com peso menor e a valuation equilibram a sazonalidade e o prêmio, e no 1T28 a assimetria fica negativa.

## 4. Para os outros agentes

**Respostas às entradas fixas**

- **E1, em destaque (persistência):** persistente. O salto de 26/10 é o mercado passando de uma probabilidade de vitória de Flávio a um quarto mandato de Lula (CNN Brasil · 25/10 · nível A), e a PTAX ficou 5,30% acima da de 02/10, véspera do 1º turno (Q3). Parte do exagero do pregão já voltou. A central fica em 5,44–5,57 em todo o horizonte, contra 5,04 em 22/10.
- **E2, em destaque (global ou idiossincrático):** idiossincrático. Em 05/10, o real −4,55% contra −0,31% a −1,95% dos pares e −0,37% do dólar contra emergentes (Q3, tabela); em 26/10, o real +9,19% com o DXY +0,15% e o S&P +0,70%. A prova pelos pares de 26/10 falta no F.
- **E3, em destaque:** o Copom condicionou a projeção a R$ 5,15 pela PPC (report de política monetária, comunicado da 281ª)[^condicionante]. A PTAX estava 2,2% abaixo disso em 23/10 e 6,8% acima em 26/10; a central do 4T26 fica 5,5% acima, e a faixa base do 4T26 inteira (5,30 a 5,60) fica acima do condicionante. O câmbio de partida da reunião de 09/12 (média de dez dias úteis antes da semana da reunião, segundo a política monetária) cai, no meu base, dentro dessa faixa.
- **E4, em destaque:** CDS e real andaram juntos em 26/10 (+18 p.b. e +9,19%) com o DXY parado, e contra os pares em 05/10 (Q3). O prêmio é fiscal e de juro local, não de calote em dólar (leitura do fiscal). Institucional: Galípolo disse que "Meu mandato vai até o final de 2028" (CNN Brasil · 27/10 · nível B), e Lula, antes da votação, que quer "que o Banco Central baixe o juro" (Poder360 · 24/10 · nível B): risco dito, nenhuma decisão.
- **E5, em destaque:** carry e real se descolaram: o DI de 1 ano menos a meta do Fed subiu de 9,14 para 10,82 p.p. e o real caiu 9% no mesmo pregão (Q2). Se o carry voltou a segurar o real depois de 26/10 o F não diz; o dólar caía 1,29% na manhã de 27/10 (InfoMoney · 27/10 · nível B).
- **E6:** sem intervenção nova no câmbio: nenhuma venda à vista ou de linha em outubro até 26/10 (`cmb_reservas_bc`) e só a rolagem de swap de até US$ 4 bi em 27/10 (InfoMoney · 27/10 · nível B). A disfunção foi no mercado de juros, com o Tesouro cancelando leilões (InfoMoney/Estadão Conteúdo · 26/10 · nível A). O cupom cambial não está no dado. Não marco em destaque: a condição do mapa (intervenção ou pico do cupom) não aconteceu.
- **E7 (inflação):** a tese por trimestre (seção 1) e E1.
- **E8, em destaque (inflação):** risco relevante de depreciação: upside de 31% no 4T26 (acima de 5,60) e 30% no 1T27 (acima de 5,75), puxado pelo prêmio fiscal e, no 4T26, pela saída de dezembro; idiossincrático (E2). No upside do modelo o IPCA de 12 meses do 1T27 vai a 5,05%, contra 4,96% no base; o repasse é seu.
- **E9 (atividade):** a tese e E1: câmbio persistentemente mais depreciado, 5,44–5,57 contra 5,04 em 22/10.
- **E10 (atividade):** termos de troca: preço a favor (IC-Br +12,8% em 12 meses, petróleo exportado de US$ 43,9 bi para US$ 54,1 bi), mas Funcex −3,0% em três meses até agosto; o F não traz volume para separar preço de quantidade.
- **E11, em destaque (fiscal):** o idiossincrático domina e o CDS andou junto, nos dois pregões; em 05/10 contra os pares, com prova (Q3).
- **E12 (fiscal):** a tese; o BC só rolou swap em outubro. Sobre FS-CB2: o estoque vendido de US$ 91,6 bi (`cmb_reservas_bc` · ago) vezes a variação da PTAX de 23 para 26/10 dá ~R$ 42 bi de perda só pela variação cambial, a ordem que você apontou; contra 30/09, ~R$ 29 bi. É conta sobre o estoque de agosto e ignora o cupom e o diferencial de juros.
- **E13, em destaque (externo):** idiossincrático (E2). O dólar contra emergentes de 26/10 em diante contém o salto do real; não o leia como movimento global.
- **E14 (externo):** fluxo financeiro positivo em US$ 4,13 bi até 16/10 e posição comprada em real no percentil 95 em 20/10: o apetite chegou ao Brasil por dinheiro e por posição antes do choque, e a posição saiu em boa parte em 26/10 (Q1).
- **E15 (expectativas):** persistente e idiossincrático (E1, E2), com a tese por trimestre: é o caso que chega aos horizontes longos.

**Pedidos**

- **S1 (política monetária):** respondido na rodada 1 (manter em 04/11 com 75%; 35% de regime de alta). Para o final: se a PTAX ficar acima de 5,50 até a reunião de 09/12, quanto sobe a probabilidade de alta em dezembro? Depende disso o carry do 1T27 e qual versão do upside vale.
- **S2 e S7 (política monetária e fiscal):** com uma alta em 09/12 e o fiscal de 2027 sem decisão, a cauda de dominância passa de ~10%? Decide entre o upside com a alta da Selic segurando o real (5,65 no 4T26) e o sem (5,66 no 4T26, 5,93 no 2T27).
- **S3 (política monetária):** respondido (R$ 5,15 pela PPC; câmbio de partida pela média de dez dias úteis). Para o final: o câmbio de partida da reunião de 04/11 mistura dias antes e depois de 26/10; que número ele dá, e o Copom o usa sem ajuste? Depende E3.
- **S4 (política monetária):** respondido (reação pela segunda ordem e pela projeção, sem postura de defesa do câmbio). A condição do mapa para ampliar a pergunta à função de reação do BC (intervenção sem disfunção, ou fala sobre o nível do real) não aconteceu.
- **S5 (inflação):** o IPCA de 12 meses do P1 (5,32% no 4T26, 4,19% no 1T28) é o que uso na perna de PPC. Se a defasagem do diesel e a reação da Petrobras mudarem a sua cauda de alta, avise: ela entra na (F) pela inflação.
- **S6 (fiscal):** usei os seus três caminhos de CDS e de NTN-B. Decidi × 1,2 no upside e nenhum multiplicador no base (seção 3.2), porque o dado trimestral não mostra o canal mais forte com o CDS baixo; se você tiver evidência na frequência trimestral, ou o CDS em log (sua seção 6), argumente de novo. E: o projeto de Durigan para o centro da meta (nível A) e os subsídios de 2027 (nível B) mudam as probabilidades das suas caudas? Depende a assimetria de 2027.
- **S8 (externo):** usei os seus caminhos (P1). O S&P do base sobe 10% e é o maior canal externo na PTAX do 1T28; reduzi o peso a 55%, por causa do sinal. Se você tiver um motivo para o S&P subir que não seja apetite a risco, diga: ele mudaria a leitura do sinal.
- **S9 (externo):** o que fizeram os pares e o dólar contra emergentes de 21 a 27/10? Fecha a prova de E2 para 26/10.
- **S10 (expectativas):** a revisão do Focus de 30/10 para o câmbio de 2026 (5,05 em 23/10) não está no F deste ciclo; fica para o próximo. Separa surpresa de convergência.
- **Ao agente web:**
  1. A volatilidade implícita de 3 meses do dólar contra o real depois de 26/10, em qualquer veículo. Sou o principal dessa exógena e ela não está no F; a rodada 1 não achou nada.
  2. O BC fez leilão à vista, de linha ou de swap novo (fora da rolagem) entre 28/10 e 03/11, e algum diretor falou sobre o funcionamento do câmbio antes da reunião de 04/11? Depende o tempero do BC e E6.
  3. Quem Lula anunciou, ou disse que vai anunciar, para a Fazenda e a equipe econômica depois de 25/10, e o conteúdo do projeto de lei complementar de Durigan (meta, prazo, mecanismo). Dependem as probabilidades das duas caudas.
  4. Alguma reportagem nomeada sobre a desmontagem de posição comprada em real por fundos estrangeiros em 26–27/10, ou o COT da CFTC de 27/10 para o real? Depende o tempero de posicionamento.
  5. O que fizeram o peso mexicano, o chileno e o colombiano em 26/10? Depende E2.

**Como subordinado**

- **Dólar contra emergentes · principal: externo**
  - Insumos: em 26/10 o real subiu 9,19% com o DXY a +0,15% (`cmb_ptax`, `cmb_dollar_index`), e em 05/10 o real caiu 4,55% com o índice a −0,37% (Q3): o índice vai conter um movimento do real que é do Brasil. Em outubro a alta do índice (+1,6% no mês até 23/10, `cmb_dollar_index_em`) se concentrou no peso mexicano (+7,8% no mês até 20/10, `cmb_fx_latam`), e uma economista do Grupo Financiero Base, Gabriela Siller, atribuiu o pico do peso à "desmantelamiento de posturas de carry trade" (Investing.com México · 22/10 · nível B). Os asset managers estavam vendidos em peso no percentil 0 de 10 anos em 20/10 (`cmb_cot_fx`): sobra pouco para vender.
  - Argumento: o seu base de 130,5–131 até o 1T27 é coerente com isso, e o risco nele é para baixo, se o peso mexicano se recuperar de uma posição vendida recorde; não tenho como medir quanto. As leituras do índice de 26/10 em diante não devem subir o caminho do 4T26: parte delas é o real.
  - Caminho de referência: nenhum.
  - Resposta do principal: o report do externo da rodada 1 foi escrito em paralelo e não responde; aberta, aguarda a rodada 2 do externo.
- **IC-Br em dólar · principal: externo**
  - Insumos: exportações de bens em recorde (US$ 376,6 bi em 12 meses, `cmb_balanco_pagmt` · set), com petróleo de US$ 43,9 bi para US$ 54,1 bi (`cmb_comex_produto` · set); o Brent passou de US$ 110 com ataques a petroleiros (OilPrice · 19/10 · nível B); o minério de ferro caiu à mínima de dois anos, segundo um analista que a reportagem só identifica como "Jiang" (Yahoo Finance/Bloomberg · 27/10 · nível C), com o futuro de Singapura a US$ 89,25 a tonelada. O real não seguiu as commodities neste mês (Q2).
  - Argumento: retiro o da rodada 1 (o 4T26 baixo pela energia): o 4T26 é o valor de dezembro, e o seu Brent devolve o pico até lá. O risco que vejo é nos metais: a notícia do minério é de nível C e não sustenta caminho, mas é um risco para baixo no seu ~330.
  - Caminho de referência: nenhum.
  - Resposta do principal: aberta, aguarda a rodada 2 do externo.

**Divergências** (volatilidade implícita, de que sou principal)

- Nenhum subordinado argumentou sobre `vol`, e o P1 não lista divergência nela. A expectativas usou 18% de vol no próprio upside como condição, não como caminho (report de expectativas, seção 3.1), o que cabe no meu upside de 24%.
- Mantenho o caminho base (17,0 → 13,5). Conferi contra a realizada (seção 3.1): a relação histórica daria 17,3–19,3% no fim do 4T26; fico no piso porque o evento que gerou a realizada já passou. A diferença para 18,5% seria de +0,02 na central do 4T26.

## 5. Placar

Não há report final anterior do câmbio: o ciclo de 22/10 não tem `cambio_rf`. O 3T26 fechou com a PTAX em 5,1809 (30/09, `cmb_ptax`), sem tese final em vigor para conferir.

## 6. Sobre o modelo

Ciclo sem literatura: as propostas vêm do dado e do mapa.

| Fonte | O que sugere | Teste proposto | Por que importa para a tese deste ciclo |
|---|---|---|---|
| Resíduo da (F) por trimestre (Modelo Estrutural, 2006–2026) e fluxo financeiro de dezembro (`cmb_cambio_contratado`) | Dummy de 4º trimestre, ou o fluxo financeiro de nov–dez como regressor, com quebra em 2017 | Reestimar a (F) com a dummy na amostra inteira e com interação pós-2017; mudar se a dummy pós-2017 tiver intervalo de 90% acima de zero e o erro fora da amostra de 2021–2025 cair | A central do 4T26 fica abaixo da PTAX de hoje, e a sazonalidade explica a maior parte da distância; hoje ela é tempero |
| Volatilidade implícita sem 3T26 e fora do banco (mapa, 2.7; modelo segura 12,19) | Trazer a implícita para o banco; até lá, preencher o trimestre faltante pela realizada (implícita ≈ 6,65 + 0,274 × realizada 21d + 0,389 × realizada 63d, erro 2,1 p.p.) | Comparar a (F) estimada com a implícita preenchida contra a atual nos trimestres em que as duas existem; adotar se o coeficiente do carry/vol não sair do intervalo | Sou o principal da vol e escrevo o caminho sem o dado de hoje; é o canal que mais move a central do 4T26 |
| Sensibilidade da PTAX ao CDS por nível (G deste ciclo, 2006–2026): diária 0,42% por 10 p.b. com CDS < 200 contra 0,26% na amostra; trimestral 0,57% contra 0,85% | CDS em log na (F), como o fiscal propõe, ou interação ΔCDS × nível | Reestimar a (F) trimestral com Δlog(CDS) e com a interação; mudar se o coeficiente em log for estável entre 2006–2015 e 2016–2026 e o em p.b. não, ou se a interação tiver sinal e intervalo fora de zero | Decide se o argumento do fiscal (× 1,5) é multiplicador ou especificação; no dado trimestral, hoje, não sustenta o × 1,5 |
| Sinal do S&P 500 na (F): +1,89 por desvio (alta da bolsa americana deprecia o real), contra o mecanismo do mapa (2.3); no P1 vale +0,12 na PTAX do 1T28 | O sinal é condicional ao dólar contra emergentes (e ao CDS) na mesma equação | Reestimar sem o dólar contra emergentes e medir a correlação entre as duas variações; se o sinal virar, ou se o coeficiente perder significância, tirar o S&P da (F) ou entrar com ele ortogonalizado | Neste ciclo o canal deixou de ser pequeno: é a maior contribuição externa à central de 2027 e a razão da assimetria negativa do 1T28 |

[^ptax]: A PTAX é a taxa de câmbio de referência calculada pelo Banco Central a partir das cotações do dia. O report projeta a PTAX de venda do último dia útil de cada trimestre (4T26 = 31/12/2026).
[^modelo]: O Modelo Estrutural resolve juntas cinco equações (hiato, inflação, expectativas, Selic e câmbio). O P1 é a rodada do modelo com o caminho de cada premissa escrito pelo agente responsável por ela. A faixa que o modelo imprime mede só a incerteza sobre os pesos estimados; a distribuição da tese é do agente.
[^processo]: O F não traz dado eleitoral: o resultado das eleições e as falas citadas vêm das notícias do ciclo, com o veículo, a data e o nível de cada uma. Nível A é fato confirmado por documento ou por dois veículos com atribuição nominal; B é fonte identificada, e prova que a pessoa disse, não que vai acontecer; C é fonte anônima e só entra como expectativa ou risco.
[^split]: Global ou idiossincrático: se o real cai junto com os pares e com os índices de dólar, o motivo é global; se cai sozinho, é do Brasil. A comparação é feita no mesmo período para todos.
[^pctl]: Percentil é a posição do número no histórico: 0 é o menor já visto, 100 o maior. No volume, percentil 19 quer dizer que em 81% dos meses dos últimos 10 anos o volume foi maior.
[^posbancos]: Posição à vista dos bancos: quanto os bancos compraram menos venderam de dólar à vista, acumulado. Vendida e crescendo quer dizer que eles financiam saída de dólar com o próprio balanço, sinal de escassez de dólar no mercado à vista.
[^cot]: O COT é o relatório semanal da CFTC com as posições em contratos futuros de real em Chicago. Posição extrema como sinal contrário: quando os fundos já estão muito comprados em real, sobra pouco comprador novo, e um choque faz muitos venderem ao mesmo tempo.
[^carry]: Carry é o ganho de aplicar no juro brasileiro, mais alto, financiado em dólar, ao juro americano. Ele atrai capital e sustenta o real enquanto o câmbio não oscila demais: por isso o modelo usa o carry dividido pela volatilidade. Exemplo: o mesmo diferencial de juros, dividido por uma volatilidade maior, dá um quociente menor, e o modelo lê isso como menos atração para o real.
[^dominancia]: Dominância fiscal é quando a dívida pública pesa tanto que subir os juros piora a percepção de risco em vez de atrair capital: a alta encarece a dívida, o prêmio sobe e a moeda se deprecia, ao contrário do usual.
[^reer]: O câmbio real efetivo (BIS) compara o real com uma cesta de moedas de parceiros, corrigido pelas inflações. Alta do índice é real mais caro.
[^mult]: Multiplicador: o peso que o modelo estima para cada canal tem uma faixa de valores plausíveis (o intervalo de 90%). Multiplicar o peso por 1,2 é dizer que, num cenário, o canal age 20% mais forte que a estimativa central, ainda dentro dessa faixa; sair dela é afirmar que o histórico subestima o canal.
[^sazonal]: Resíduo é a parte da variação trimestral do câmbio que o modelo não explica. Positivo no 4º trimestre quer dizer que, em dezembro, o real costuma se depreciar mais do que o modelo prevê; é a época de remessa de lucros e dividendos.
[^condicionante]: O Copom projeta a inflação supondo um caminho para o câmbio; hoje, um caminho que parte de R$ 5,15 e segue a paridade do poder de compra (o câmbio corrigido pela diferença entre a inflação brasileira e a americana). Câmbio de mercado acima desse caminho é risco de inflação mais alta que a projetada.
