# Report — câmbio · ciclo 2026-10-02 · rodada 1

Dados até: 02/10/2026 · Horizontes: 4T26 a 1T28, USD/BRL pela PTAX de venda do último dia útil de cada trimestre[^1]

## 1. Tese

| Variável | Trimestre | Central | Base: faixa · P | Upside: limite · P | Downside: limite · P | P(up) − P(down) |
|---|---|---|---|---|---|---|
| USD/BRL, PTAX de fechamento | 4T26 | 5,223 | 5,01 a 5,43 · 50% | acima de 5,43 · 29% | abaixo de 5,01 · 21% | +0,08 |
| | 1T27 | 5,260 | 4,96 a 5,56 · 50% | acima de 5,56 · 29% | abaixo de 4,96 · 21% | +0,08 |
| | 2T27 | 5,263 | 4,90 a 5,63 · 50% | acima de 5,63 · 28% | abaixo de 4,90 · 22% | +0,06 |
| | 3T27 | 5,249 | 4,83 a 5,67 · 50% | acima de 5,67 · 28% | abaixo de 4,83 · 22% | +0,06 |
| | 4T27 | 5,265 | 4,79 a 5,74 · 50% | acima de 5,74 · 27% | abaixo de 4,79 · 23% | +0,04 |
| | 1T28 | 5,289 | 4,77 a 5,81 · 50% | acima de 5,81 · 27% | abaixo de 4,77 · 23% | +0,04 |

- **Acima da faixa (real mais fraco; ruim para a inflação).** Aversão a risco global: o dólar contra emergentes a 134,9 (+4% sobre 02/10), a volatilidade implícita a 16%, o IC-Br em dólar a 198 e o CDS a 150 p.b. (aguarda fiscal, S6) dão 5,64 no 4T26 no modelo; o efeito do carry/vol × 1,5 leva a 5,69, e o BC vendendo dólar traz de volta a 5,64. No 1T27 e no 2T27 o mesmo cenário dá 5,66 e 5,67, ainda acima da faixa. De 3T27 em diante ele fica dentro dela (5,67 a 5,70), e a cauda pede uma segunda perna: o CDS a 200 p.b. no 2T27 leva o modelo, com o tempero (i), a 5,88–5,92.
- **Abaixo da faixa (real mais forte; bom para a inflação).** O dólar global devolve a alta de setembro (dólar contra emergentes a 126,9, o nível de 31/08), a volatilidade cai a 11%, o IC-Br vai a 212 e o CDS a 120 p.b. (aguarda fiscal): 5,00 no 4T26 no modelo, 4,98 com o petróleo além do IC-Br. No 1T27 dá 4,97, na borda da faixa (4,96). Do 2T27 em diante a cauda pede o dólar contra emergentes caindo mais, a 122 no 2T27: 4,80–4,84 com o tempero, abaixo da faixa no 2T27 e no 3T27 e ainda dentro dela, perto do limite, no 4T27 e no 1T28.
- **A tese em uma frase:** o real fecha o 4T26 perto do nível de hoje (5,22) e anda devagar para 5,29 até o 1T28, porque o modelo lê o dólar global, as commodities e a volatilidade quase parados e o carry encolhendo com a queda da Selic; o risco pende para a depreciação (+0,08 no 4T26), porque o real se descolou dos pares em setembro com o apoio de um choque de petróleo e com o posicionamento comprado em real perto do máximo de 10 anos.

## 2. Argumentação

### Q1 — Condições do mercado de câmbio

**O mercado à vista ficou mais curto de dólar em setembro, e o BC entrou para supri-lo.** São três partes.

- *Saída financeira acima do normal para o mês.* O fluxo cambial total foi de −US$ 5,20 bi em setembro, com o financeiro em −US$ 7,33 bi (`cmb_cambio_contratado` · set), contra uma média de −US$ 3,11 bi no total e −US$ 4,65 bi no financeiro nos setembros de 2016 a 2025 (`cmb_cambio_contratado`). O comercial (+US$ 2,13 bi) não cobriu a diferença.
- *Bancos mais vendidos no à vista.* A posição à vista dos bancos foi a −US$ 26,2 bi em setembro, −US$ 4,1 bi no mês, percentil 24 em 10 anos[^2] (`cmb_reservas_bc` · set), o que mostra que os bancos financiaram a saída vendendo dólar que não tinham em caixa.
- *O BC supriu dólar.* Vendeu US$ 1 bi à vista em 14/09 e outro em 17/09 (depois de US$ 1 bi em 31/08) e US$ 1 bi em leilões de linha[^3] em 22/09 e outro em 28/09 (`cmb_reservas_bc`). As reservas caíram US$ 9,1 bi em um mês, a US$ 362,8 bi (`cmb_reservas_bc` · 02/10), mais do que as vendas: o resto não é intervenção, e a tabela não traz a decomposição diária.

Mas o preço não mostra desordem: a volatilidade realizada de 63 dias do real é de 7,8% ao ano, percentil 4 em 10 anos (`cmb_ptax` · 02/10), contra uma mediana de 12,0% no período, e a PTAX ficou entre 5,06 e 5,22 de 01/07 a 02/10 (`cmb_ptax`). O BC agiu com o mercado calmo, o que pesa para a leitura de E6 e para a pergunta S4 (seção 4). O que confirmaria escassez de financiamento em dólar, e não só uma saída concentrada, é o cupom cambial, que não está nos dados[^4].

**A liquidez à vista está abaixo da média de 12 meses, sem ser escassa:** o volume interbancário D+2 foi de US$ 1,23 bi/dia em média no último mês, contra US$ 1,57 bi/dia em 12 meses, percentil 44 em 10 anos (`cmb_ptax` · 02/10).

**O posicionamento estrangeiro está comprado em real perto do máximo histórico, e quem comprou em setembro foi o investidor não alavancado.** Os asset managers estão comprados em ~67 mil contratos, +18 mil no mês, percentil 96 em 10 anos, e as posições em aberto estão no percentil 99 (`cmb_cot_fx` · 29/09). Os fundos alavancados reduziram (~10 mil, −5 mil no mês). Posicionamento extremo é sinal contrário[^5]: sobra pouco comprador novo, e uma saída amplifica o movimento que outro fator começar. É a base do tempero (i).

**A saída de fim de ano não é motivo para tempero.** Em 2016–2025, o fluxo financeiro de dezembro teve média de −US$ 15,2 bi, e o total de outubro a dezembro, −US$ 13,0 bi (`cmb_cambio_contratado`); mas o BC vendeu linhas em dezembro em quase todos esses anos (`cmb_reservas_bc`), e a PTAX subiu em só 10 dos 20 quartos trimestres de 2006 a 2025, com mediana de −0,6% (`cmb_ptax`). A saída sazonal é conhecida e tem sido absorvida.

### Q2 — Fundamentos

**Carry: o real é, de longe, a moeda de carry mais atraente da região.** O carry contra o Fed é de 10,12 p.p. e, dividido pela volatilidade de 63 dias, dá 1,29, contra 0,57 no peso colombiano e 0,45 no mexicano (`O real e os pares` · 02/10).

| Medida | Valor | Fonte · data |
|---|---|---|
| Selic − meta do Fed | 10,12 p.p. | `O real e os pares` · 02/10 |
| Diferencial nominal (Selic − Fed Funds efetivo) | 10,00 p.p., −0,78 p.p. em 12 meses | `diferenciais_juros` · set |
| Diferencial real ex-post | 9,14 p.p., percentil 81 em 10 anos | `diferenciais_juros` · set |
| DI de 1 ano | 13,50% | `br_di_grade` · 02/10 |
| Selic na curva em dez/2027 | 13,95% | `br_di_grade` · 02/10 |

O carry à frente depende da Selic, que é da política monetária (S1). A curva e a pesquisa divergem: a curva precifica 13,95% em dez/2027 (`br_di_grade` · 02/10), e a Focus, 12,50% em set/2027 (`expc_focus_copom` · 02/10). É leitura, não conclusão.

**Prêmio de risco: o CDS subiu, mas o real não o acompanhou.** O CDS de 5 anos está em 131 p.b., +9 p.b. desde 31/08 (`cmb_risco_pais` · 02/10). Se o movimento é fiscal é do agente fiscal (S6); o que é deste agente é que o real se apreciou contra os pares no mesmo mês (Q3), o que não é o padrão de estresse fiscal (E4, E11).

**Termos de troca e comércio: o volume está carregando a receita de exportação.** O IC-Br em dólar subiu 4,1% em 3 meses e 12,8% em 12 (`comm_icbr_usd` · set); o índice de termos de troca da Funcex caiu 2,7% em 3 meses, mas o dado é de julho, 93 dias antes do corte, anterior à maior parte do choque do Brent (`cmb_termos_troca` · jul). As exportações somaram US$ 375,0 bi em 12 meses até setembro, contra US$ 339,9 bi um ano antes, percentil 100 (`cmb_comex_pais` · set), com petróleo (US$ 51,6 bi contra 43,2), soja (48,7 contra 40,8) e carnes (33,8 contra 27,4) em alta (`cmb_comex_produto` · ago). O saldo comercial do fluxo cambial em 12 meses é de US$ 58,3 bi, percentil 93 (`cmb_cambio_contratado` · set).

**Contas externas: o investimento direto cobre o déficit em conta corrente.** O déficit em 12 meses é de US$ 63,0 bi, 2,47% do PIB, menor que os US$ 76,9 bi de um ano antes, e o investimento direto no país soma US$ 86,6 bi, 3,39% do PIB (`cmb_balanco_pagmt` · ago). No fluxo, a entrada de capital estrangeiro foi de US$ 81,7 bi em 12 meses, contra US$ 37,7 bi um ano antes (`cmb_cambio_contratado` · set). Mas a saída de residentes compensa boa parte: rendas em −US$ 66,0 bi (percentil 6) e capitais brasileiros em −US$ 49,6 bi (percentil 3) em 12 meses (`cmb_cambio_contratado` · set), e a carteira de ações teve saída de US$ 5,6 bi em agosto (`cmb_balanco_pagmt` · ago).

**Valor: o real está no meio da sua faixa de 10 anos.** O câmbio real efetivo está em 117,2, percentil 53 em 10 anos, com apreciação real de 4,5% em 12 meses (`cmb_reer` · set)[^6]. Não há desalinhamento que puxe o nível para um lado nos seis trimestres.

### Q3 — O que explica o movimento recente

A janela é de 1 a 3 meses (de 30/06 e de 31/08 a 02/10); não há ciclo anterior[^7].

**O real subiu menos do que o dólar global explicaria: a parte global depreciou, a idiossincrática apreciou.**

| | De 30/06 a 02/10 | De 31/08 a 02/10 |
|---|---|---|
| Real (PTAX) | +0,9% | +0,8% |
| Média de MXN, CLP, COP e PEN | +2,2% | +4,6% |
| DXY | +0,7% | +2,5% |
| Dólar contra emergentes | +0,2% | +2,2% |

Fonte: `cmb_ptax`, `cmb_fx_latam`, `cmb_dollar_index`, `cmb_dollar_index_em` · 02/10; CLP e COP com a taxa formada no dia (Atenção do F).

Numa regressão dos retornos diários do real sobre o DXY e a média dos pares, estimada nos 12 meses anteriores[^8], a parte global do movimento de 31/08 a 01/10 é de +3,9% e a idiossincrática, de −3,4 p.p.: o real ficou estável (+0,5%) porque algo próprio dele compensou quase todo o dólar global. De 30/06 a 01/10 a divisão é +1,9% global e −1,3 p.p. idiossincrático. A regressão explica 36% a 43% da variação diária, então a divisão é aproximada.

O que está por trás da parte idiossincrática tem duas partes:
- *Petróleo.* O Brent subiu 97,7% em 3 meses, a US$ 135,5 (`comm_brent` · 02/10), e entre os pares quem se saiu melhor desde 30/06 foi o outro exportador de petróleo, o peso colombiano (−3,9%), enquanto o peso chileno subiu 6,7% e o mexicano 5,0% (`cmb_fx_latam` · 02/10). Parte do que a regressão chama de idiossincrático é a divisão entre exportadores e importadores de petróleo dentro da própria cesta de pares, e não algo só do Brasil.
- *Carry.* O real é a moeda de maior carry/vol da região (Q2), e os asset managers aumentaram a compra de real em ~18 mil contratos no mês (`cmb_cot_fx` · 29/09).

Mas três dados puxaram no sentido contrário e não impediram a apreciação relativa: o CDS subiu 9 p.b. desde 31/08 (`cmb_risco_pais` · 02/10), o fluxo financeiro de setembro foi pior que o padrão do mês (Q1), e o BC precisou vender dólar. O apoio idiossincrático, portanto, não veio de fluxo financeiro: veio de preço (petróleo) e de posição (carry). Os dois podem reverter rápido, e é por isso que a assimetria pende para cima.

**O começo de outubro.** Do fechamento do 3T26 (5,181 em 30/09) a 02/10, a PTAX subiu 0,8%, a 5,224, o máximo desde 01/07 (`cmb_ptax`), num pregão em que o Brent subiu 16,9% em dois dias (`comm_brent` · 02/10). Desde 02/09, a alta é de 1,9% (`cmb_ptax` · 02/10).

**E1 — persistência:** o real não mudou de patamar. A PTAX está no topo de uma faixa de 5,06 a 5,22 que já dura três meses (`cmb_ptax`), e o que subiu em setembro acompanha o dólar global. Classifico o movimento como transitório: ele persiste se o dólar global persistir (aguarda externo, S8), e o que mudaria a classificação é o real passar a se depreciar contra os pares, não só contra o dólar.

**E2 — global ou idiossincrático:** o movimento bruto foi global (+3,9%), e a parte idiossincrática foi de apreciação (−3,4 p.p.), quase do mesmo tamanho. Para a inflação e as expectativas, isso significa que o real não carrega hoje prêmio de risco doméstico; o risco é o apoio idiossincrático acabar.

### Q4 — Cenário prospectivo

**Por que a central.** Os caminhos do cenário base estão na seção 3.1. O CDS, o S&P 500, os Fed funds e a inflação americana ficam no padrão do simulador (o último valor repetido; na inflação americana, a média de 4 trimestres), à espera dos agentes fiscal e externo. Os três caminhos deste agente mudam pouco a central: no 4T26, o padrão do simulador dá 5,210; só a volatilidade a 12,7% dá 5,225; só o dólar contra emergentes a 129,7, 5,222; só o IC-Br a 207,9, 5,197; os três juntos, 5,223. Do 4T26 ao 1T28 a central sobe de 5,22 a 5,29 por dois canais do modelo: o diferencial de inflação, que entra na equação com peso 1 (o IPCA de 12 meses do modelo vai de 5,28% a 4,08%, contra a inflação americana no padrão), e o carry que encolhe com a Selic do modelo caindo de 13,43% a 12,18% no fechamento. A central não leva tempero.

**Por que a faixa.** A faixa base é a central ± 0,67 desvio de uma volatilidade de 12% ao ano, a mediana de 10 anos da realizada de 63 dias (`cmb_ptax`), escalada pelo horizonte: ±4,0% no 4T26 e ±9,8% no 1T28, para 50% de probabilidade. É mais estreita que a dispersão histórica de 20 anos, que inclui as crises: a variação da PTAX em um trimestre ficou entre −3,4% e +4,2% na metade central dos trimestres de 2006 a 2026, e em seis trimestres, entre −6,9% e +21,6% (`cmb_ptax`).

**Por que a assimetria pende para a depreciação.**
- Para cima: o posicionamento comprado em real perto do máximo de 10 anos, com o real como a moeda de maior carry/vol da região (tempero (i)); o apoio idiossincrático depende do petróleo, e o Brent subiu 18,0% em um único pregão (de US$ 114,8 em 01/10 a US$ 135,5 em 02/10, `comm_brent`), um preço que também pode devolver; o Treasury de 10 anos subiu 0,49 p.p. no mês, a 5,28%, e a meta do Fed subiu 0,25 p.p. (`us_interest_rate` · 02/10), o que é do agente externo, mas é o tipo de movimento que precede aversão a risco em emergentes; e o CDS subiu 9 p.b. desde 31/08.
- Para baixo: o petróleo além do que o IC-Br capta (tempero (ii)); o BC disposto a vender dólar (tempero (ii)), o que limita a cauda de cima; e a Focus de 2026 a 5,20 (`expc_focus_periodo` · 02/10), um pouco abaixo da central.
- O peso dos dois lados: os fatores de cima agem pelo mesmo mecanismo, o desmonte de carry, e reforçam um ao outro; os de baixo são graduais (receita de exportação) ou só freiam (o BC). Daí +0,08 no 4T26 e no 1T27, caindo a +0,04 em 2027 e 2028, quando a incerteza do horizonte domina a assimetria.

### Outros pontos

**O BC no mercado de câmbio entra em destaque (E6, seção 4).** Vender US$ 2 bi à vista com a volatilidade no percentil 4 é a parte do mês que mais pesa para a política monetária, porque responde à pergunta S4 do mapa: a venda atendeu a uma saída concentrada (Q1) ou indica preocupação com o nível? Os dados mostram o primeiro, mas sem o cupom cambial e sem a comunicação do BC (S3, S4) não consigo excluir o segundo.

**Olhado, sem sinal.**
- Estoque de swaps cambiais · −US$ 91,6 bi (`cmb_reservas_bc` · ago) · +US$ 1,3 bi no mês, rolagem de rotina, e o dado é de agosto · diria algo se o BC ampliasse a oferta acima dos vencimentos.
- Volume interbancário D+1 · US$ 327 mi/dia em média no mês, percentil 68 (`cmb_ptax` · 02/10) · o D+2 é o mercado relevante · diria algo se caísse junto com o D+2.
- Erros e omissões · −US$ 2,6 bi em 12 meses (`cmb_balanco_pagmt` · ago) · perto dos −US$ 2,2 bi de um ano antes · diria algo se a saída não registrada crescesse.
- Juro real ex-post dos pares · México 3,24%, Colômbia 5,76% (`cmb_real_rates` · ago) · 62 dias de defasagem, e o carry já está na tabela dos pares · diria algo com um corte ou alta de juros de um par (S9).
- Focus de câmbio de 2028 e 2029 · 5,30 e 5,33 (`expc_focus_periodo` · 02/10) · quase paradas em 4 semanas (0,00 e −0,02) e além do horizonte · diria algo se se movessem junto com o real.
- Fundos alavancados no peso mexicano · ~81 mil contratos comprados, percentil 97 em 10 anos (`cmb_cot_fx` · 29/09) · posição em outra moeda · diria algo sobre contágio se a liquidação no peso começasse a aparecer na posição em real.
- Exportação para os EUA · US$ 35,8 bi em 12 meses, contra US$ 40,4 bi um ano antes (`cmb_comex_pais` · set) · pequena diante do total, que está no recorde · diria algo se a queda se espalhasse para outros destinos.

## 3. Premissas

### 3.1 Etapa 1 — o modelo

**Cenários.**
- Base: o choque do petróleo para no nível médio de outubro, o dólar global fica onde está em 02/10, a volatilidade implícita sobe pouco com o ambiente global e o CDS fica parado (aguarda fiscal).
- Upside (real mais fraco): o choque do petróleo e a alta dos juros americanos viram aversão a risco em emergentes: o dólar contra emergentes sobe 4%, a volatilidade vai a 16%, as commodities fora do petróleo caem e o CDS sobe a 150–155 p.b. (aguarda fiscal).
- Downside (real mais forte): o dólar global devolve a alta de setembro, a volatilidade cai, o petróleo fica alto e as commodities sobem, e o CDS cai a 120 p.b. (aguarda fiscal).

**Caminhos das exógenas.**

| Exógena | Hoje (valor · tabela · data) | Cenário | 4T26 | 1T27 | 2T27 | 3T27 | 4T27 | 1T28 |
|---|---|---|---|---|---|---|---|---|
| CDS 5 anos (p.b.) — aguarda fiscal | 131 · `cmb_risco_pais` · 02/10 | base | 131,2 | 131,2 | 131,2 | 131,2 | 131,2 | 131,2 |
| | | upside | 150 | 155 | 155 | 155 | 155 | 155 |
| | | downside | 120 | 120 | 120 | 120 | 120 | 120 |
| Volatilidade implícita do real (% a.a.) — tutela do câmbio | 12,19 · `modelo_estrutural` · 2T26 | base | 12,7 | 12,7 | 12,7 | 12,7 | 12,7 | 12,7 |
| | | upside | 16,0 | 15,0 | 14,0 | 13,5 | 13,0 | 13,0 |
| | | downside | 11,0 | 11,0 | 11,0 | 11,0 | 11,0 | 11,0 |
| Dólar contra emergentes (índice) — tutela do câmbio, nível 2 | 129,71 · `cmb_dollar_index_em` · 02/10 | base | 129,7 | 129,7 | 129,7 | 129,7 | 129,7 | 129,7 |
| | | upside | 134,9 | 134,9 | 134,9 | 134,9 | 134,9 | 134,9 |
| | | downside | 126,9 | 126,9 | 126,9 | 126,9 | 126,9 | 126,9 |
| S&P 500 (pontos) — aguarda externo | 7.723 · `cmb_equity_us` · 02/10 | os três | 7.651,5 | 7.651,5 | 7.651,5 | 7.651,5 | 7.651,5 | 7.651,5 |
| IC-Br em dólar (índice) — tutela do câmbio, nível 2 | 205,7 · `comm_icbr_usd` · set | base | 207,9 | 207,9 | 207,9 | 207,9 | 207,9 | 207,9 |
| | | upside | 198,0 | 198,0 | 198,0 | 198,0 | 198,0 | 198,0 |
| | | downside | 212,0 | 212,0 | 212,0 | 212,0 | 212,0 | 212,0 |
| Fed Funds efetivo (% a.a.) — aguarda externo | 3,75 · `diferenciais_juros` · set | os três | 3,75 | 3,75 | 3,75 | 3,75 | 3,75 | 3,75 |
| CPI dos EUA (% no trimestre) — aguarda externo | 1,12 · `modelo_estrutural` · 3T26 | os três | 0,91 | 0,91 | 0,91 | 0,91 | 0,91 | 0,91 |

Motivos dos caminhos que não são óbvios pela história:
- *Volatilidade.* O simulador não tem a implícita do 3T26 e segura a do 2T26, 12,19%. Como a equação lê a variação, 12,7% no base é "+0,5 p.p. sobre o nível do fim de setembro": a realizada de 21 dias (9,2%) está acima da de 63 dias (7,8%) (`O real e os pares` · 02/10), e o ambiente global ficou mais volátil. Quando a implícita do 3T26 entrar, o caminho deve ser reancorado nela mais 0,5 p.p.; sem isso, uma implícita do 3T26 abaixo de 12,19% (a realizada de 63 dias caiu de 10,8% em 30/06 para 7,8% em 30/09, `cmb_ptax`) faria o modelo ler uma alta de volatilidade no 4T26 que não está na minha premissa[^9].
- *IC-Br.* 207,9 é o IC-Br de setembro com o Brent na média de outubro até 02/10 (US$ 125,2, contra US$ 114,2 em setembro, `comm_brent`) e o resto parado: o IC-Br energia pesa ~0,20 no índice e responde ~0,6 ao Brent (regressão mensal, 2021–2026, `comm_icbr_usd` e `comm_brent`). Se o Brent ficar no nível de 02/10, o índice vai a 209,9.
- *Dólar contra emergentes.* O nível de 02/10, segurado: o agente externo tem a decisão (nível 1), e sem a leitura dele o passeio aleatório é a premissa honesta.
- *S&P 500, nos três cenários.* O peso do S&P 500 na equação é positivo (bolsa americana em alta, real mais fraco), então pôr uma queda da bolsa no upside aliviaria o real no modelo. Deixei no padrão nos três cenários, à espera do externo, e a questão vai para a seção 6.

**Saída do modelo.**

| Variável | Cenário | 4T26 | 1T27 | 2T27 | 3T27 | 4T27 | 1T28 |
|---|---|---|---|---|---|---|---|
| PTAX de fechamento (R$/US$) | base | 5,223 | 5,260 | 5,263 | 5,249 | 5,265 | 5,289 |
| | upside | 5,636 | 5,668 | 5,652 | 5,626 | 5,631 | 5,658 |
| | downside | 5,002 | 5,043 | 5,047 | 5,034 | 5,050 | 5,074 |
| Selic de fechamento, derivada (% a.a.) | base | 13,43 | 13,11 | 12,83 | 12,59 | 12,37 | 12,18 |
| | upside | 13,44 | 13,13 | 12,87 | 12,65 | 12,46 | 12,29 |
| | downside | 13,43 | 13,10 | 12,81 | 12,55 | 12,32 | 12,12 |
| IPCA 12 meses (%) | base | 5,28 | 4,85 | 4,34 | 4,35 | 4,23 | 4,08 |
| | upside | 5,33 | 5,00 | 4,55 | 4,60 | 4,46 | 4,24 |
| | downside | 5,25 | 4,77 | 4,22 | 4,20 | 4,10 | 3,98 |

A faixa de 90% do posterior da PTAX no base vai de 5,18–5,27 no 4T26 a 5,07–5,53 no 1T28; ela mede só a incerteza dos pesos, não o erro da equação[^10]. Selic e IPCA são do modelo, não deste agente: ficam aqui porque mostram o laço (a Selic do modelo mal reage ao câmbio mais fraco do upside).

### 3.2 Etapa 2 — o tempero qualitativo

**(i) Carry/vol — efeito mais forte que o estimado** · cenário upside
- Coeficiente: estimado −1,363 por desvio da variação do carry/vol, intervalo de 90% do posterior −2,207 a −0,528. Multiplicador: × 1,5, a −2,045, dentro do intervalo, no percentil 8,8 do posterior.
- Efeito: PTAX do upside de 5,636 a 5,693 no 4T26 e de 5,668 a 5,720 no 1T27; +0,7% a +1,0% conforme o trimestre.
- Por quê: o desmonte de carry é não linear e o modelo é linear; o posicionamento estrangeiro comprado em real está no percentil 96 de 10 anos e as posições em aberto no 99 (`cmb_cot_fx` · 29/09), o que deixa muito para desmontar; o real tem o maior carry/vol da região (1,29 contra 0,57 no COP, `O real e os pares` · 02/10), então é a posição que mais perde quando a volatilidade sobe; e a volatilidade realizada parte do percentil 4, o nível em que posições ajustadas por risco estão mais alavancadas. Fica no percentil 8,8, e não além, porque o fluxo de setembro não mostra saída de estrangeiro (Q2), só de residentes.
- Onde entra: limite e probabilidade da cauda de cima, e a assimetria do cenário base.

**(ii) O BC no mercado de câmbio — vendas à vista e linhas** · cenário upside
- Hoje: US$ 2 bi vendidos à vista e US$ 2 bi em linhas em setembro, mais US$ 1 bi à vista em 31/08 (`cmb_reservas_bc`); reservas de US$ 362,8 bi (`cmb_reservas_bc` · 02/10).
- Por que o modelo não vê: a equação (F) não tem a intervenção como entrada; ela entra no histórico só pela média dos episódios passados.
- Efeito: −1,0% sobre o upside (já com o tempero (i)) no 4T26 e no 1T27, −0,5% no 2T27, zero depois: de 5,693 a 5,636 no 4T26, de 5,720 a 5,663 no 1T27, de 5,698 a 5,670 no 2T27. O BC já age com o mercado calmo, então agiria cedo num movimento desordenado; o efeito some porque a intervenção suaviza o caminho e não muda o nível de chegada.
- Onde entra: limite da cauda de cima nos três primeiros trimestres.

**(ii) Petróleo além do IC-Br — exportação de petróleo** · cenário downside, e a assimetria do base
- Hoje: Brent a US$ 135,5, +97,7% em 3 meses (`comm_brent` · 02/10); IC-Br energia +11,2% em 3 meses (`comm_icbr_usd` · set); exportação de petróleo de US$ 51,6 bi em 12 meses, contra US$ 43,2 bi um ano antes (`cmb_comex_produto` · ago).
- Por que o modelo não vê: o modelo só vê o petróleo pelo IC-Br, em que a energia pesa ~0,20 e responde ~0,6 ao Brent; mesmo com o Brent parado no nível de 02/10, o índice só subiria 2,0% (G do IC-Br). A receita de exportação responde ao preço cheio e ao volume.
- Efeito: −0,5% no 4T26 e −1,5% do 1T27 em diante sobre o downside, persistente (a receita chega com defasagem e fica enquanto o preço ficar): de 5,002 a 4,977 no 4T26 e de 5,043 a 4,967 no 1T27.
- Onde entra: limite e probabilidade da cauda de baixo; no base, reduz a assimetria para cima, que seria maior sem ele. O dado não traz a importação de derivados (diesel, gasolina), e é ela que diz o saldo de petróleo de fato[^11].

### 3.3 Da etapa 1 à tese

| Trimestre | Central (modelo, base) | Upside: modelo → com tempero | Downside: modelo → com tempero |
|---|---|---|---|
| 4T26 | 5,223 | 5,636 → 5,693 (i) → 5,636 (ii) | 5,002 → 4,977 |
| 1T27 | 5,260 | 5,668 → 5,720 → 5,663 | 5,043 → 4,967 |
| 2T27 | 5,263 | 5,652 → 5,698 → 5,670 | 5,047 → 4,971 |
| 3T27 | 5,249 | 5,626 → 5,669 → 5,669 | 5,034 → 4,958 |
| 4T27 | 5,265 | 5,631 → 5,672 → 5,672 | 5,050 → 4,974 |
| 1T28 | 5,289 | 5,658 → 5,703 → 5,703 | 5,074 → 4,998 |

O upside com tempero fica ~8% acima da central e o downside ~5% abaixo em todos os trimestres. A faixa base é a central ± 0,67 desvio (seção 2, Q4), com 50%. Até o 2T27, os dois cenários com tempero caem fora da faixa e são o ponto típico de cada cauda; de 3T27 em diante, a faixa alcança os dois, e a cauda passa a pedir a segunda perna da seção 1. A assimetria (+0,08 a +0,04) é o peso relativo dos temperos: o (i) e o posicionamento pesam mais que o petróleo e o BC, e perdem peso para a incerteza do horizonte depois de 2027.

## 4. Para os outros agentes

### Respostas às entradas

- **E1** (persistência): transitório; sem mudança de patamar, a PTAX no topo da faixa de 5,06 a 5,22 de três meses (seção 2, Q3).
- **E2, em destaque:** a parte idiossincrática (−3,4 p.p., de apreciação) foi quase do tamanho da global (+3,9%) de 31/08 a 01/10. O alerta é de direção inversa à usual: o real não carrega prêmio doméstico, mas o apoio idiossincrático vem de petróleo e carry, que podem reverter (seção 2, Q3).
- **E3** (o real contra a premissa do Copom): aguarda política monetária (S3); não tenho os documentos do Copom.
- **E4** (prêmio de risco): o real não está precificando estresse fiscal ou institucional: o CDS subiu 9 p.b. desde 31/08 e o real se apreciou contra os pares no mesmo período.
- **E5** (carry): o carry sustenta o real: carry/vol de 1,29, o maior da região, e asset managers comprando ~18 mil contratos no mês. Carry e real não se descolaram.
- **E6, em destaque:** o BC vendeu US$ 2 bi à vista (14 e 17/09) e US$ 2 bi em linhas (22 e 28/09) em setembro, com a volatilidade realizada no percentil 4 de 10 anos. O que os dados mostram é uma saída financeira concentrada (−US$ 7,3 bi no mês) e bancos mais vendidos no à vista (−US$ 26,2 bi), não desordem de preço; sem o cupom cambial, não consigo dizer se houve escassez de financiamento em dólar. Isso abre a pergunta S4.
- **E7** (inflação, o caminho e a persistência): a tese da seção 1 e E1.
- **E8, para a inflação:** a cauda de depreciação tem 29% no 4T26 e no 1T27, e o cenário que a representa é de 5,64 a 5,67, ~8% acima da central; a origem é global (dólar contra emergentes, volatilidade), amplificada pelo desmonte de carry, e não doméstica. O repasse é seu.
- **E9** (atividade, o caminho e a persistência): a tese da seção 1 e E1.
- **E10** (atividade, preço contra volume): o volume carrega. O índice de termos de troca caiu 2,7% em 3 meses até julho (dado de 93 dias), enquanto a exportação em 12 meses está no recorde, com petróleo, soja e carnes acima de um ano antes (seção 2, Q2).
- **E11** (fiscal): não. A parte idiossincrática foi de apreciação, e o CDS subiu enquanto o real se saiu melhor que os pares.
- **E12** (fiscal, o caminho e as operações do BC): a tese da seção 1; reservas de US$ 362,8 bi, −US$ 9,1 bi no mês; swaps em −US$ 91,6 bi em agosto, +US$ 1,3 bi no mês.
- **E13** (externo): seção 2, Q3, e E2. A divisão usa o DXY e os pares, porque o índice de emergentes contém o real.
- **E14** (externo, fluxo e posição): o ciclo global chegou ao Brasil por posição, não por dinheiro saindo. O capital estrangeiro entrou (+US$ 4,9 bi em setembro, +US$ 81,7 bi em 12 meses), a saída de setembro foi de residentes (capitais brasileiros −US$ 5,0 bi, rendas −US$ 4,6 bi), e os asset managers aumentaram a compra de real (`cmb_cambio_contratado` · set; `cmb_cot_fx` · 29/09).
- **E15** (expectativas): E1, E2 e a tese da seção 1. Movimento transitório e de origem global, sem prêmio doméstico a passar para as expectativas longas.

### Pedidos

- **S1 (política monetária).** Qual a Selic no fechamento de cada trimestre de 4T26 a 1T28, e reunião a reunião em 04/11 e 09/12? A central sobe de 5,22 a 5,29 em parte porque a Selic do modelo cai a 12,18% no 1T28; a curva precifica 13,95% em dez/2027. Uma Selic mais perto da curva tira parte dessa subida.
- **S2 (política monetária).** Com o IPCA de 12 meses subindo no 4T26 (5,2% na projeção do Copom, `pm_copom_projecoes` · 24/09) e a Selic em corte, o mercado lê o ciclo como crível ou como tolerância com a inflação? Decide o sinal do juro sobre o câmbio na cauda de cima.
- **S3 (política monetária).** Como o Copom descreveu o câmbio no comunicado, na ata e no RPM da reunião 281, e qual a premissa de câmbio do cenário de referência (valor e como é formada)? E3 depende disso.
- **S4 (política monetária).** As vendas de setembro foram comunicadas como provisão de liquidez ou como resposta ao nível? Se for o segundo, a pergunta se amplia para a função de reação do BC com a intervenção, com você liderando, e o tempero (ii) do BC passa de um freio na cauda de cima a parte do cenário base.
- **S5 (inflação).** Qual o IPCA de 12 meses por trimestre e de onde vêm as caudas, em particular quanto do Brent chega ao IPCA? O diferencial de inflação entra na equação do câmbio com peso 1, e a curva de Phillips do modelo não tem o petróleo.
- **S6 (fiscal).** Qual o caminho do CDS, base e caudas, e a alta de 9 p.b. desde 31/08 é fiscal? Usei o padrão (131 p.b.) no base e 150–155 e 120 nas caudas; e você argumenta por um peso do CDS maior ou menor que o estimado? A seção 6 levanta uma dúvida sobre esse peso.
- **S7 (fiscal).** A âncora fiscal é crível, com o primário em −0,62% do PIB e a dívida bruta a 82,9%, +5,6 p.p. em 12 meses (`fisc_nfsp`, `fisc_divida` · ago)? Decide se um aperto monetário na cauda de cima sustentaria o real.
- **S8 (externo).** Quais os caminhos do dólar contra emergentes, do S&P 500, do IC-Br em dólar, dos Fed funds e da inflação americana, base e caudas? Escrevi o dólar contra emergentes (129,7) e o IC-Br (207,9) com nível 2; os seus valem. O padrão dos Fed funds (3,75%) fica abaixo da meta de 02/10 (ponto médio 3,88%, `us_interest_rate`).
- **S9 (externo).** O Brent de US$ 135,5 em 02/10 (+18,0% no pregão) é um nível ou um pico? E o ciclo dos pares e o apetite a risco global? O apoio idiossincrático do real e o tempero do petróleo dependem disso.
- **S10 (expectativas).** Por que a Focus de câmbio de 2026 ficou em 5,20 por 13 semanas (`expc_focus_periodo` · 02/10) enquanto a PTAX foi ao máximo de três meses? É convergência esperada ou a pesquisa ainda não reagiu?
- **Pedido deste ciclo (externo).** Dá para separar, entre os pares, exportadores e importadores de petróleo na sua leitura do ciclo global? A parte idiossincrática do real (−3,4 p.p.) é em parte essa divisão, e a resposta muda o tamanho do tempero do petróleo.

## 5. Placar

Primeiro ciclo.

## 6. Sobre o modelo

Ciclo sem literatura: as propostas vêm dos dados e do mapa.

| Fonte | O que sugere | Teste proposto | Por que importa para a tese deste ciclo |
|---|---|---|---|
| Os coeficientes da (F) e o mapa (2.3: o real é de beta alto em aversão a risco) | O peso do S&P 500 é positivo (+1,888 por desvio): bolsa americana em alta, real mais fraco, o oposto do canal de apetite a risco. Pode ser um efeito de juros americanos ou do dólar que o índice de emergentes não capta | Reestimar a (F) sem o S&P 500 e com ele em subamostras (antes e depois de 2016); se o sinal mudar ou o peso não for diferente de zero, tirar o regressor ou trocá-lo por uma medida de volatilidade global | No upside, uma queda da bolsa apreciaria o real no modelo; deixei o S&P 500 no padrão para não somar esse efeito |
| A unidade do peso do CDS (desvio da variação de 298,5 p.b. por trimestre) | O desvio é dominado pelos anos de CDS acima de 1.000 p.b.; o efeito por p.b. de hoje pode estar mal medido | Reestimar a (F) com quebra em 2010, ou com a variação do log do CDS; se o efeito por p.b. em 2010–2026 diferir do da amostra toda fora do intervalo de 90%, mudar a forma funcional | Decide o tamanho das caudas que o agente fiscal escrever: 20 p.b. valem ~1,7% no modelo de hoje |
| Os dados do ciclo (o Brent em +97,7% em 3 meses, o IC-Br energia em +11,2%) | O IC-Br passa pouco do petróleo à equação; o Brent pode ter efeito próprio sobre o real, como para um exportador líquido | Acrescentar a variação do log do Brent à (F), 2010–2026; se o peso for negativo e diferente de zero com o IC-Br na equação, incluir | É o tempero (ii) do petróleo: se o canal estiver na equação, ele sai do tempero e entra pelo caminho do Brent |

[^1]: A PTAX é a taxa de câmbio de referência calculada pelo Banco Central a partir das cotações do dia. O 3T26 fechou em R$ 5,181 (30/09).
[^2]: Percentil: a posição do valor de hoje no histórico, de 0 (o menor já visto) a 100 (o maior). Na posição à vista dos bancos, quanto menor o percentil, mais vendidos em dólar os bancos estão em relação aos últimos 10 anos.
[^3]: Leilão de linha: o BC vende dólar com compromisso de recompra. Dá liquidez temporária sem reduzir as reservas para sempre, ao contrário da venda à vista.
[^4]: O cupom cambial é o juro em dólar implícito no mercado doméstico; quando ele sobe em relação ao juro americano, falta dólar para financiamento no Brasil. Os dados deste ciclo não o trazem.
[^5]: Posicionamento como sinal contrário: quando os investidores já estão muito comprados numa moeda, sobra pouco comprador novo, e qualquer motivo para vender encontra muita gente querendo sair ao mesmo tempo.
[^6]: O câmbio real efetivo (do BIS) compara o real com uma cesta de moedas, descontada a inflação de cada país. Aqui, um índice maior é um real mais forte.
[^7]: Este é o primeiro ciclo do sistema: não há report anterior de câmbio para comparar.
[^8]: A regressão mede quanto o real costuma andar quando o dólar global (DXY) e os pares andam, e aplica isso ao período. O que ela explica é a parte global; o que sobra é a idiossincrática, própria do real. Os pares não são só global: cada um tem a sua história, e o peso mexicano subiu 7,8% em um mês.
[^9]: A volatilidade implícita, tirada do preço das opções de dólar, é a que o mercado espera para os próximos meses. O modelo a lê de uma planilha que não faz parte dos dados deste ciclo, e o dado do 3T26 ainda não existe nela.
[^10]: A faixa do modelo vem de mil conjuntos de pesos estimados para as equações; ela diz quanto a central mudaria com outros pesos plausíveis, não quanto o câmbio pode variar. A faixa da tese, na seção 1, é a que mede isso.
[^11]: O Brasil exporta petróleo cru e importa derivados; os dados deste ciclo trazem só o cru, então o saldo de petróleo de fato não está medido aqui.
