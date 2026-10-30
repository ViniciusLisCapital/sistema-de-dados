# Report — fiscal · ciclo 2026-10-27 · report final

Dados até: 26/10/2026 nos preços (CDS, curvas, PTAX); ago/2026 nas contas fiscais (RTN, NFSP, DLSP); 2T26 no governo geral (EFGG) e no PIB; notícias publicadas até 27/10/2026 · Horizontes: 4T26 a 1T28, o CDS de 5 anos no fechamento do trimestre (`fiscal`) e a NTN-B de 10 anos na média do trimestre (`rr_10a`)[^proc]

## 1. Tese

| Variável | Trimestre | Central | Base: faixa · P | Upside: limite · P | Downside: limite · P | P(up) − P(down) |
|---|---|---|---|---|---|---|
| CDS 5 anos[^cdsdef], fechamento (p.b.) | 4T26 | 140 | 125 a 160 · 60% | acima de 160 · 27% | abaixo de 125 · 13% | +0,14 |
| | 1T27 | 142 | 125 a 170 · 55% | acima de 170 · 30% | abaixo de 125 · 15% | +0,15 |
| | 2T27 | 139 | 121 a 174 · 55% | acima de 174 · 30% | abaixo de 121 · 15% | +0,15 |
| | 3T27 | 135 | 117 a 175 · 54% | acima de 175 · 30% | abaixo de 117 · 16% | +0,14 |
| | 4T27 | 130 | 113 a 176 · 54% | acima de 176 · 30% | abaixo de 113 · 16% | +0,14 |
| | 1T28 | 125 | 110 a 176 · 54% | acima de 176 · 30% | abaixo de 110 · 16% | +0,14 |
| `rr_10a`, NTN-B 10 anos, média (% a.a.) | 4T26 | 7,75 | 7,55 a 7,89 · 60% | acima de 7,89 · 25% | abaixo de 7,55 · 15% | +0,10 |
| | 1T27 | 7,95 | 7,55 a 8,45 · 55% | acima de 8,45 · 28% | abaixo de 7,55 · 17% | +0,11 |
| | 2T27 | 7,90 | 7,45 a 8,55 · 55% | acima de 8,55 · 28% | abaixo de 7,45 · 17% | +0,11 |
| | 3T27 | 7,80 | 7,35 a 8,60 · 54% | acima de 8,60 · 28% | abaixo de 7,35 · 18% | +0,10 |
| | 4T27 | 7,75 | 7,30 a 8,60 · 54% | acima de 8,60 · 28% | abaixo de 7,30 · 18% | +0,10 |
| | 1T28 | 7,70 | 7,25 a 8,60 · 54% | acima de 8,60 · 28% | abaixo de 7,25 · 18% | +0,10 |

Nas duas variáveis, **o upside é a cauda ruim para o Brasil**: CDS e juro real mais altos são o mercado cobrando mais pelo risco da dívida.

- **Acima da faixa** (upside, 25–30%) se o governo reeleito não entregar o que o ministro da Fazenda prometeu em 26–27/10 e as decisões de 2027 afrouxarem a política fiscal (estímulos de 2026 renovados, despesa fora da regra, novo crédito do Tesouro a bancos oficiais), com um risk-off global somado: CDS a 170 em 4T26 e ~205–210 no 1S27, `rr_10a` de ~8,9% a ~9,1% em 2027. No modelo, a PTAX vai a ~5,78 em 1T27 e a Selic média a ~14,3% (seção 3.1).
- **Abaixo da faixa** (downside, 13–18%) se o projeto de lei complementar anunciado pelo ministro para perseguir o centro da meta fiscal for enviado e aprovado, e o Orçamento de 2027 sair sem os estímulos de 2026, com apetite global a risco: CDS ~120 → ~105, `rr_10a` ~7,35% → ~6,95%. No modelo, PTAX de ~5,35 a ~5,47 e Selic média de ~12,7% em 1T27.

**A tese em uma frase:** a reeleição de Lula em 25/10 tirou dos preços o prêmio de troca de governo que o 1º turno tinha posto; a base mantém o juro real de 10 anos perto de 8,0%, o nível médio de jul/26, até o começo de 2027, cedendo ~0,25 p.p. até 1T28 conforme a alta de juros que a curva cobra não vem, e o CDS em 140 até 1T27, cedendo com o componente global a 125 em 1T28; as caudas de alta, as ruins, pesam 25–30% contra 13–18% das de baixa, porque as contas e as decisões já tomadas para 2027 sustentam mais a leitura de 26/10 do que as promessas feitas depois dela.

**O que mudou desde a rodada 2** (a rodada 2 já incluía as mudanças da moderação):

| Item | Rodada 2 → final | Por quê | Causa |
|---|---|---|---|
| `rr_10a` de 4T26 | 7,72 → 7,75; faixa 62% → 60%, upside 23% → 25% | no primeiro pregão depois do corte do F, o juro real longo do Tesouro subiu de novo enquanto os prefixados caíam | r2-07 (nível B) |
| Meta fiscal | "não se sabe o que a meta desconta" → a meta exclui precatórios e parte da Defesa (nível B) | a comparação certa com a meta é o primário do RTN sem precatórios | releitura de r1-18 (nível B) |
| Combustíveis | subvenção de 2027 proposta (nível B) → mais tributos da gasolina zerados desde 09/10, por 30 dias prorrogáveis, e subvenção de R$ 1,20/litro ao diesel importado desde abril (nível B) | resposta a IN-S6 | r2-16, r2-17 |
| Credibilidade das promessas | Durigan como autor do plano → a chefia da Fazenda do 2º mandato está em aberto | as promessas podem não ter dono em 2027 | r2-12, r2-13 (nível B) |
| CDS, caudas e demais probabilidades | sem mudança | nada novo no CDS depois de 26/10 | — |

Na rodada 2 (depois da moderação) os dois caminhos base tinham mudado contra a rodada 1: `rr_10a` 7,70 · 7,80 · 7,70 · 7,60 · 7,55 · 7,50 → 7,72 · 7,95 · 7,90 · 7,80 · 7,75 · 7,70, e o CDS 140 · 140 · 138 · 135 · 135 · 135 → 140 · 142 · 139 · 135 · 130 · 125 (seção 4, Divergências).

## 2. Argumentação

### O que aconteceu em outubro

Os dois fins de semana que moveram todos os preços domésticos foram os dois turnos da eleição presidencial. No 1º turno, em 04/10, Flávio Bolsonaro ficou à frente, e "a leitura inicial dos investidores foi de redução do prêmio de risco dos ativos brasileiros" (Agência Brasil · 05/10 · nível A); no 2º turno, em 25/10, Lula foi reeleito para um quarto mandato, e "o mercado vinha tratando a vitória de Flávio como a possibilidade de uma virada na política fiscal do governo" (CNN Brasil · 25/10 · nível A). A frase da CNN é a leitura do veículo, e é a mesma que os preços contam: nos dois pregões o real andou 4,6% e 9,2% em sentidos opostos com o DXY e o S&P 500 andando menos de 1% (`cmb_ptax`, `cmb_dollar_index`, `cmb_equity_us`; câmbio, rodada 1).

| Preço | 05/10 contra 02/10 | 26/10 contra 23/10 | 26/10 contra 30/09 |
|---|---|---|---|
| CDS 5 anos (p.b.) | −12 | +18 | +6 |
| NTN-B 10 anos (p.b.) | −50 | +135 | +50 |
| DI 10 anos (p.b.) | −134 | +239 | +116 |
| Inflação implícita 10 anos[^impl] (%) | 6,18 → 5,42 | 5,66 → 6,55 | 5,97 → 6,55 |
| PTAX (%) | −4,6 | +9,2 | +6,2 |

Fontes: `cmb_risco_pais`, `br_interest_rate`, `cmb_ptax`, pregões de 02/10, 05/10, 23/10 e 26/10.

**O salto de 26/10 devolveu a NTN-B 10a ao nível de meados do ano, e não a um nível novo.** Os 8,05% de 26/10 são a média de jul/26 (8,05%), e o máximo de 10 anos é 8,20%, em 02/07/2026; o atípico foi o mínimo de outubro, 6,70%, depois do 1º turno (`br_interest_rate`, médias mensais de 2026). Mas o CDS não voltou ao de meados do ano: estava em médias de 123 a 125 p.b. em jun–ago e fechou 26/10 em 137 (`cmb_risco_pais`).

**O mercado de títulos funcionou mal, e o Tesouro tirou duração dele.** O Tesouro cancelou os leilões de prefixados e de NTN-B da semana (InfoMoney · 26/10 · nível A) e o de LFT de 27/10 (InfoMoney · 27/10 · nível A), recomprou "mais de R$ 14 bilhões em títulos públicos" em 26/10, cerca de R$ 7 bi em NTN-F e R$ 7 bi em NTN-B, e anunciou nova recompra de NTN-B de 2030, 2035, 2040 e 2045 em 27/10 (InfoMoney e Agência Brasil · 27/10 · nível A), em que comprou de volta 3,8 milhões de NTN-B (InfoMoney · 27/10 · nível B).[^recompra] A data de volta dos leilões não foi noticiada. **Mas a recompra não derrubou o juro real longo:** em 27/10 os prefixados do Tesouro Direto caíram até 47 p.b. e os IPCA+ longos subiram, o de 2040 de IPCA + 7,29% para IPCA + 7,53% (InfoMoney · 27/10 · nível B), e o dólar fechou em R$ 5,350, −0,97% (Poder360 · 27/10 · nível B). No dia seguinte ao choque caiu a inflação implícita e subiu o juro real: é prêmio sobre a dívida indexada, e é por isso que a `rr_10a` de 4T26 passou para a metade de cima da faixa. As taxas do Tesouro Direto não são as da NTN-B de 10 anos do F, e a de 27/10 é um pregão; o número que conta é o do F do próximo ciclo.

**O governo respondeu com promessas fiscais, e a chefia da Fazenda está em aberto.** Dario Durigan, ministro da Fazenda, disse em 26/10 que o governo pretende ampliar o superávit primário em 2027 e que "parte das medidas de crédito subsidiado e de outros estímulos adotados em 2026 poderá ser reduzida ou não renovada" (Poder360 · 26/10 · nível B), e que vai "buscar o centro da meta" por um projeto de lei complementar (CNN Brasil, Exame e Poder360 · 27/10 · nível A de que disse), a apresentar "ainda em 2026", mudando "a legislação ou, se necessário, a Constituição" (Poder360 · 26/10 · nível B). O envio não foi noticiado. E "o comando do Ministério da Fazenda é uma das principais decisões pendentes" (InfoMoney · 27/10 · nível B); Durigan chamou Rafael Fonteles de "um excelente nome" para a pasta (Poder360 · 27/10 · nível B). Nível A e B sustentam que as frases foram ditas, não que o plano acontecerá, e um plano cujo autor pode não estar no cargo em 2027 é mais fraco do que a frase: as promessas entram na história do downside, com a probabilidade da cauda.

### F1 — A postura: a política fiscal está expandindo a demanda, pouco pelo primário e muito pelo crédito

| Medida (p.p. do PIB, + = expansionista) | Até | Impulso | Leitura |
|---|---|---|---|
| Setor público consolidado, primário 12m (NFSP), em 12 meses | ago/26 | +0,4 | expansão moderada |
| Governo central, primário 12m (RTN), em 12 meses | ago/26 | +0,3 | expansão moderada |
| Governo central sem precatórios, em 12 meses | ago/26 | +0,3 | a mesma, sem o calendário dos precatórios |
| Governo central, em 3 meses | ago/26 | −0,5 | contração aparente: é calendário |
| Governo central sem precatórios, em 3 meses | ago/26 | −0,05 | neutro |
| Governo geral (EFGG), despesa exceto juros, em 1 ano | 2T26 | +1,9 | expansão forte, metade é precatório |
| Parafiscal: crédito do Tesouro a instituições oficiais, em 1 ano | ago/26 | +0,9 | expansão pelo crédito |

Fontes: "O impulso fiscal em quatro medidas" do F (`fisc_nfsp`, `fisc_rtn`, `fisc_efgg`, `fisc_dlsp_fatores`) e, sem precatórios, `fisc_rtn` com o PIB de `atv_pib_mensal`, até ago/26.[^impulso][^prim]

- **As medidas de 12 meses concordam** (+0,3 a +0,4 p.p.), com ou sem precatórios[^prec], porque as duas janelas carregam um pagamento grande: R$ 64 bi em jul/25 e R$ 71 bi em mar/26 (`fisc_rtn`).
- **A de 3 meses discorda por calendário, não por decisão:** a melhora de ~0,5 p.p. do primário 12m entre mai/26 e ago/26 (`fisc_nfsp`, de −1,14% para −0,62% do PIB) vem de julho, quando saiu da janela o pagamento de jul/25. Sem precatórios, os três meses são neutros.
- **A EFGG exagera pelo mesmo motivo:** a janela de quatro trimestres até 2T26 carrega precatórios de 1,3% do PIB, contra 0,3% na anterior (`fisc_rtn`), o que responde por metade dos +1,9 p.p.; o resto é maior que nas medidas acima da linha porque a EFGG soma as três esferas sem consolidar, e estados e municípios pioraram (primário de 12 meses de +0,12% do PIB em ago/25 para −0,04% em ago/26, `fisc_nfsp`).
- **O parafiscal é o maior empurrão isolado:** o crédito do Tesouro a instituições oficiais (todo ao BNDES) passou de R$ 107 bi para R$ 233 bi em 12 meses até ago/26, de 0,9% para 1,8% do PIB (`fisc_dlsp_fatores`), em duas ondas, set–dez/25 e mai–ago/26.[^para] O saldo do BNDES cresceu ~10% e o crédito direcionado ~13% em 12 meses, contra ~9% do total (`cred_modalidade_direcionado_pj`, `cred_credito_resumo`, ago/26, TWA, premissa assumida). O agente web não achou a lei, MP ou contrato que corresponde aos R$ 126 bi (demanda r2, "Sem notícia").

Por grupo de despesa, a expansão está na parte que o governo liga e desliga. Crescimento real em 12 meses até ago/26, deflator IPCA (`fisc_rtn`, `fisc_investimento`):

| Grupo (governo central, RTN) | Real 12m (%) | 2T26 contra 2T25 (%) |
|---|---|---|
| Discricionárias do Executivo | +35 | +54 |
|   dessas, saúde · educação · assistência | +69 · +44 · +50 | — |
| Investimento federal pago (GND 4) | +26 | — |
|   dele, transferências a municípios | +70 | — |
| Pessoal e encargos | +5 | +4 |
| BPC/LOAS | +5 | +4 |
| Benefícios previdenciários | +4 | +3 |
| Bolsa Família | −10 | −10 |
| Despesa total | +5,6 | +7,3 |
| Receita líquida | +4,0 | +7,1 |

A despesa discricionária cresce acima de tudo o mais, e as transferências às famílias crescem menos (Bolsa Família −10% real). Mas jul–ago/26 mostram a despesa total ~11% abaixo de jul–ago/25 em termos reais, e as discricionárias ~16% abaixo (`fisc_rtn`); parte disso é bloqueio que acaba no fim do ano: a restrição de empenho "está prevista em R$ 24,058 bilhões até novembro" e o valor sujeito a ela "cai para zero em dezembro" (Agência Brasil · 01/10 · nível B). Por isso a base não lê jul–ago como o fim do empurrão e mantém o impulso de 4T26 positivo (F2).

Contra o ciclo: o hiato do BC caiu de 1,5% do potencial em 4T24 para 0,4% em 3T26 (`pm_hiato_produto`, edição de set/26, percentil[^pct] 57 no histórico), e o P2 o põe em 0,1% em 4T26 e −0,5% em 1T28. Uma postura que expande com o hiato positivo é pró-cíclica; o atividade usa o impulso deste report no tempero de resiliência da curva IS, a 0,09 p.p. de hiato por ponto de impulso (atividade, rodada 2), e quanto o impulso pesa no hiato é dele.

### F2 — Por onde chega ao hiato e à inflação, e o caminho do impulso

**A demanda do governo cresce acima do PIB.** O consumo do governo subiu 3,1% contra 2T25 e o PIB 2,0% (`atv_pib_taxas`, 2T26), e a participação dele no PIB foi de 18,7% para 19,6% em quatro trimestres (`atv_pib_valores_correntes`); as contas nacionais de 3T26 saem em dezembro (atividade, rodada 2). O Focus de 23/10 vê o consumo do governo crescendo 2,2% em 2026 e 1,1% em 2027 (`expc_focus_periodo`; expectativas, rodada 2): o consenso já esperava desaceleração em 2027, antes de 26/10.

**Transferências e renda: o canal mais fraco de 2026 fica mais forte em 2027.** O Orçamento de 2027 vai ter cerca de R$ 20 bi remanejados para "reajuste do Bolsa Família, ampliação do Pé-de-Meia para universitários, Desenrola 3.0 e Pix MEI", "sem elevar o teto de despesas nem alterar a meta de resultado primário" (Ministério do Planejamento, via Agência Brasil e CNN Brasil · 19/10 · nível A), e o salário mínimo proposto para 2027 cria "uma despesa obrigatória de cerca de R$ 49,6 bilhões" (CNN Brasil · 26/08 · nível B). O remanejamento muda a composição, não o total: tira demanda de onde ela chega devagar e põe onde chega rápido, no consumo das famílias.

**O parafiscal em 2027 tem sinais nos dois sentidos.** Durigan disse que parte do crédito subsidiado de 2026 "poderá ser reduzida ou não renovada" (Poder360 · 26/10 · nível B), mas o Orçamento de 2027 prevê "R$ 97,9 bilhões para programas de crédito de seis fundos públicos" (Exame · 31/08 · nível B, sem citar BNDES nem Tesouro). A base supõe que o crédito já concedido ao BNDES continua sendo desembolsado em 4T26–1S27 e que não há nova onda do Tesouro como as de 2025–26.

**Impostos e preços administrados: o governo está segurando o preço dos combustíveis com receita, e quer seguir em 2027.** Em 09/10 a MP 1.395 zerou "as alíquotas de PIS/Pasep, Cofins e Cide-Combustíveis" da gasolina e ampliou subsídios, e "a medida vale por 30 dias, com possibilidade de revisão ou prorrogação" (Agência Brasil · 09/10 · nível B); desde abril há subvenção "de R$ 1,20 por litro para a importação de diesel", que "pode chegar a R$ 4 bilhões", válida "inicialmente por dois meses" (Agência Brasil · 06/04 · nível B, sem o número da MP). Para 2027, Durigan disse que "é sim possível, e acho que essa deve ser a proposta do presidente, manter essa ajuda", se o Brent seguir alto, e que a lei que autoriza os recursos "vale apenas para 2026" (Poder360 · 23/10 · nível B); Lula falou em "subsidiar o óleo diesel e a gasolina" (Poder360 · 24/10 · nível B). Os monitorados de 12 meses estão em 4,1% (`inflc_agregados`, set/26) e o Brent em US$ 115 (`comm_brent`, 20/10). A mesma medida mexe em dois lados com sinais opostos: baixa o IPCA medido e custa receita, o que piora o primário. O custo fiscal da gasolina e o valor de 2027 não foram noticiados.

**O caminho do impulso, por trimestre** (premissa deste agente, seção 4): moderadamente expansionista em 4T26, com o desbloqueio de dezembro e os tributos da gasolina, e neutro a contracionista em 2027. A base continua sendo a mediana Focus de 23/10, anterior a 26/10: primário de −0,48% do PIB em 2026, −0,30% em 2027 e 0,00% em 2028 (`expc_focus_periodo`), o que dá impulso de ~+0,05 p.p. em 2026, ~−0,2 em 2027 e −0,3 em 2028 contra o primário de −0,43% de 2025 (`fisc_nfsp`, dez/25). As promessas de 26–27/10 apontam para um 2027 mais contracionista que o Focus; as decisões já tomadas (mínimo, remanejamento, subvenção) para o mesmo total com mais transferência. A base fica no Focus até a revisão pós-26/10 aparecer (FS-EP1).

### F3 — O policy mix

Em 2026, a política fiscal adicionou demanda enquanto o Copom cortou a Selic de 15,00% para 13,75% em cinco reuniões desde mar/26 (`pm_copom_reuniao`): as duas empurraram a demanda para o mesmo lado. O Copom lê a política fiscal pelos três canais, demanda, prêmio e neutro: "o esmorecimento no esforço de reformas estruturais e disciplina fiscal, o aumento de crédito direcionado e as incertezas sobre a estabilização da dívida pública têm o potencial de elevar a taxa de juros neutra" (ata da 281ª, §8, em política monetária, rodada 2). O crédito direcionado, que é o parafiscal de F1, está na frase, e o Relatório de Estabilidade Financeira de 27/10 põe o risco fiscal entre "as principais preocupações" (Agência Brasil · 27/10 · nível B).

A postura fiscal expansionista com o hiato positivo pede uma Selic mais alta para o mesmo resultado de inflação. A PM põe 77% em manter 13,75% em 04/11 e 57% em 09/12, e 32% em a Selic estar acima de 13,75% depois de dezembro (política monetária, rodada 2). No modelo o mix entra pela `rr_10a`, que subiu de 7,40% em 2T25 para 7,84% em 3T26 na média do trimestre (`br_interest_rate`), e que a base põe em 7,95% em 1T27: o neutro do modelo sobe junto, e a regra leva a Selic até ele.

### F4 — As contas e a dívida

**Resultado.** O primário do setor público consolidado em 12 meses é de −0,62% do PIB e o do governo central, −0,53% (`fisc_nfsp`, ago/26; negativo = déficit), contra −0,19% e −0,24% um ano antes. Com juros nominais de 8,9% do PIB, percentil 100 em 10 anos, o resultado nominal é de −9,5% (`fisc_nfsp`).

**Estrutura da receita.** A receita administrada pela RFB cresce ~6% real, com o IOF a +28%; a não administrada cai ~9%, puxada por dividendos (−49%) e concessões (−61%) (`fisc_rtn`, 12 meses até ago/26). A receita líquida (+4,0%) cresce menos que a despesa (+5,6%).

**A regra: cumprida, com a dívida subindo.** Segundo o Estadão Conteúdo, a meta de 2026 é superávit primário de 0,25% do PIB e a de 2027, de 0,50%, ambas com tolerância de 0,25 p.p. (IstoÉ Dinheiro · 15/04 · nível B), e o governo "é autorizado a excluir do cálculo R$ 65,6 bilhões em despesas", "como precatórios e alguns gastos com Defesa"; "considerando as exceções", o PLOA de 2027 promete cumprir a meta de R$ 73,2 bi "com uma folga de R$ 10,1 bilhões" (InfoMoney · 31/08 · nível B).[^meta] O documento oficial não foi aberto e a matéria não diz a que esfera a meta se refere.

| Comparação (% do PIB) | Valor | Contra o centro | Contra o piso |
|---|---|---|---|
| Governo central (RTN), 12m até ago/26, sem precatórios | +0,29 | +0,04 | +0,29 |
| Governo central (RTN), 12m até ago/26, com precatórios | −0,53 | — | −0,53 |
| Focus, primário de 2026 (23/10) | −0,48 | −0,73 | −0,48 |
| Focus, primário de 2027 (23/10) | −0,30 | −0,80 | −0,55 |

Fontes: `fisc_rtn` e `atv_pib_mensal` (ago/26), `expc_focus_periodo` (23/10), metas de r1-19.

Com os precatórios fora, o primário do governo central em 12 meses está no centro da meta de 2026, e Durigan diz que a execução "mira o piso" (CNN Brasil · 27/10 · nível A de que disse). **A regra está sendo cumprida, mas não é ela que o mercado precifica:** o primário que entra na dívida é o com precatórios, 0,5 p.p. abaixo do piso, e a dívida sobe 5 p.p. por ano. O Focus de 23/10 via o primário abaixo do piso nos dois anos; se o Focus mede com ou sem as deduções, nem o F nem as notícias dizem.[^focus]

**A dívida.** A dívida líquida (DLSP) está em 69,3% do PIB e a bruta (DBGG) em 82,9%, ambas ~5 p.p. acima de um ano antes, a DLSP no percentil 100 do histórico (`fisc_divida`, ago/26).[^div] O que a moveu em 12 meses (`fisc_dlsp_fatores`, + = aumenta a dívida): juros, R$ 1,18 tri (8,9% do PIB); primário, R$ 82 bi (0,6%); ajuste cambial, +R$ 60 bi (0,5%), com o real mais forte entre o fim de ago/25 e o de ago/26 (5,43 → 5,18, `cmb_ptax`), porque o setor público é credor líquido em moeda estrangeira.

O juro implícito nominal da DLSP é de 13,8% ao ano, 9,2% real pelo IPCA de 12 meses, contra crescimento nominal do PIB de 7,2% (`fisc_dlsp_fatores`, `atv_pib_mensal`, `inflc_agregados`, ago/26). **Com esses números, o primário que estabiliza a DLSP é de ~4,3% do PIB, a ~4,9 p.p. do primário de hoje**; com juro implícito 1 p.p. menor, ~3,6%. O caminho de Selic do P2 (13,4% no fim de 4T26 a 12,1% em 1T28) baixa o custo da dívida devagar, sem mudar a ordem de grandeza dessa distância (FS-PM1). O Focus de 23/10 projeta a DLSP a 74% em 2027 e 79% em 2029 (`expc_focus_periodo`): o consenso não vê estabilização no horizonte.

Outubro mexe nas contas pelos dois lados: o real mais fraco reduz a DLSP pelo ajuste cambial, mas o BC tinha US$ 91,6 bi vendidos em swap em ago/26 (`cmb_reservas_bc`), e a alta da PTAX de 23/10 para 26/10 implica um resultado de swap da ordem de −R$ 42 bi (~0,3% do PIB), que piora o resultado nominal de out/26; o câmbio chega à mesma ordem e lembra que a conta ignora o cupom e o diferencial de juros (câmbio, rodada 2).[^swap] O BC só rolou swap em outubro até 27/10 (InfoMoney · 27/10 · nível B).

### F5 — O preço do risco e a tese

**O que é fiscal e o que é global no CDS.** O CDS fechou 3T26 em 131 (`cmb_risco_pais`), 6 p.b. acima de 2T26, numa alta concentrada em 17/09–30/09 com o peso mexicano +5,5% e o dólar contra emergentes +1,5% (`cmb_fx_latam`, `cmb_dollar_index_em`): componente global ou regional. O externo, com datas casadas, mostra o mês de outubro em duas partes: de 30/09 a 23/10 o CDS caiu 12 p.b. enquanto o componente global pedia +8, e em 26/10 subiu 18 p.b. sem movimento global (externo, rodada 2, por G). O doméstico comprimiu o CDS até 23/10, com a expectativa de troca de governo, e o abriu em 26/10, quando ela caiu; o câmbio atribui ao CDS +1,6% dos +9,2% da PTAX no modelo e lê o resto como prêmio idiossincrático (câmbio, rodada 2). **Mas a regressão do externo superestima o global** pelo motivo que ele mesmo dá: o dólar contra emergentes contém o real, então a piora do Brasil entra no índice; não há CDS de pares no banco para separar.[^cds]

**O CDS reagiu pouco a um choque grande, e isso diz o que foi precificado.** Em 26/10 o real caiu 9,2% com o CDS subindo 18 p.b.: o real andou ~6 vezes o que o CDS explica no modelo; em 05/10, ~4 vezes. O choque foi precificado como risco de inflação e de juro local, não de calote em dólar: a inflação implícita de 10 anos subiu 0,9 p.p. num pregão, para 6,55%, e a NTN-B 10a foi a 8,05%, percentil 99 nos últimos 10 anos (`br_interest_rate`), enquanto o CDS de 137 está no percentil 17 em 10 anos (`cmb_risco_pais`). A PM decompõe a curva real: dos +135 p.b. da NTN-B de 10 anos, +22 vêm dos dois primeiros anos, onde está o caminho de política, +40 dos anos 2 a 5 e +73 dos anos 5 a 10 (política monetária, rodada 2). A maior parte é prêmio de prazo e fiscal, e o pregão de 27/10 o confirma do lado do Tesouro Direto: o juro real longo subiu enquanto a implícita caía.

**Que caminho fiscal o mercado precifica, contra F1–F4.** Entre 05/10 e 23/10 os preços precificavam a troca de governo: CDS de 109–119, NTN-B 10a de 6,70–7,01. Esse cenário não aconteceu. Em 26/10 os preços voltaram ao juro real de meados do ano com um CDS e uma inflação implícita mais altos: precificam um governo que continua com a política fiscal de 2026. As contas sustentam essa leitura: o impulso foi positivo em 2026, o parafiscal cresceu ~0,9 p.p. do PIB, a regra é cumprida com o primário que entra na dívida ~5 p.p. abaixo do que a estabiliza, e a dívida sobe 5 p.p. por ano. Contra ela estão as promessas de 26–27/10 (nível A e B, que sustentam que foram ditas) e a QPC de setembro, com só 17% de respostas de piora fiscal, contra 50% em junho (`expc_qpc`, 23/09), anterior aos dois choques.

**Por que a base não aposta na reversão que o histórico sugere.** Depois dos 52 saltos diários do CDS de 15 p.b. ou mais desde 2006, 62% devolveram mais da metade em 63 pregões; nos cinco saltos da NTN-B 10a de 40 p.b. ou mais, todos devolveram mais da metade (`cmb_risco_pais`, `br_interest_rate`, 2006–set/26). Aqueles saltos partiram de níveis normais e foram desfeitos pela política que os causou; o de 26/10 desfez um nível anormal, o da expectativa de troca de governo, por um fato que dura o horizonte inteiro. A devolução que a base tem é outra: a da parte da alta que é caminho de política (abaixo).

**Dominância fiscal: dois dos três conjuntos de sinais estão presentes, nenhum completo.**[^dom]
- *Sustentabilidade fiscal: presente.* Primário que entra na dívida ~4,9 p.p. abaixo do que a estabiliza, juro real implícito de ~9%, DLSP no maior nível do histórico e subindo 5 p.p. por ano, e um consenso que não vê estabilização até 2029. A regra cumprida não muda isso: as deduções da meta são despesa que entra na dívida.
- *Mercado: presente nos preços locais e no mercado de títulos, ausente no CDS e nas expectativas longas.* A inflação implícita longa subiu com o resultado da eleição, o Tesouro cancelou leilões e recomprou R$ 14 bi num dia, e o juro real longo subiu de novo no dia seguinte. Mas o CDS está no percentil 17 de 10 anos, e o Focus de IPCA para 2029–2030 seguia em 3,50% em 23/10 (`expc_focus_periodo`; expectativas, rodada 2). O teste decisivo, o real se depreciar quando o Copom sobe juros, não ocorreu.
- *Regime monetário: sinal fraco, só verbal.* Lula disse "quero que o Banco Central baixe o juro" (Poder360 · 24/10 · nível B), e Galípolo, presidente do BC, disse em 27/10 que seu mandato "vai até o final de 2028" e não comentou o Copom (CNN Brasil e Poder360 · 27/10 · nível B). A PM lê hoje uma pausa como credibilidade e uma alta sem sinal de segunda ordem como possível custo da dívida (política monetária, rodada 2, E2).

A cauda de dominância é a parte mais extrema do upside: ~10% no horizonte (dentro dos 25–30% da cauda de alta), condicionada a uma decisão fiscal explícita de afrouxamento mais uma reação monetária que o mercado leia como insuficiente. Condicionada a uma alta da Selic em 09/12 com o fiscal de 2027 ainda sem decisão, sobe para ~15%: é exatamente a combinação em que a alta pode ser lida como custo da dívida (resposta a S2/S7 do câmbio).

**A central.** Para a `rr_10a`, 7,75% em 4T26: os 17 pregões de outubro até 26/10 fizeram média de 6,99% (o F, "O preço do risco na convenção do modelo"), e os 43 restantes a ~8,05%, o nível de 26/10, dão 7,75 (G `fi_r2_juros`).[^q4] Depois, 7,95% em 1T27, perto do nível de meados do ano com o resultado da eleição dentro, e queda de 0,25 p.p. até 1T28, com três partes: ~−0,07 p.p. pela queda de 0,25 p.p. do Treasury de 10 anos até 1T28 no base do externo (externo, rodada 2, por G); a devolução da alta de juros que a curva cobra nos dois primeiros anos, +22 p.b. de 26/10, que não vem se o Copom não subir, o que a PM dá em ~2/3 dos casos; e alguma devolução de prêmio se o projeto do centro da meta for enviado. Os +73 p.b. dos anos 5 a 10 ficam: são prêmio de um resultado que dura o horizonte. Sobre o juro real de política que o Focus esperava para 2028–29 (6,02% e 6,28%, anterior ao choque), o prêmio de prazo e fiscal fica em ~1,7 a 1,9 p.p. em 1T27.[^prazo] Para o CDS, 140 em 4T26 e 142 em 1T27, com o componente global do externo (dólar contra emergentes subindo a 131 em 1T27), e queda a 125 em 1T28 conforme o dólar contra emergentes cede e a bolsa americana sobe; o CDS fica 3 a 5 p.b. acima do componente global do externo em 3T27–1T28 porque o prêmio doméstico da eleição fica parado, não cai.

**As faixas e as caudas.** Em 4T26 a faixa da `rr_10a` é estreita porque 17 dos 60 pregões já foram: 7,55 a 7,89 equivale aos 43 restantes entre ~7,75 e ~8,25 (G `fi_r2_juros`). De 1T27 em diante a faixa cobre a variação de um trimestre dos últimos 10 anos com folga (p25–p75 de −0,25 a +0,33 p.p. na `rr_10a` e de −35 a +9 p.b. no CDS, `br_interest_rate`, `cmb_risco_pais`, 2016–2026) e se abre com o horizonte. A cauda de alta é mais provável que a de baixa nas duas variáveis porque as contas e as decisões já tomadas para 2027 estão do lado da leitura de 26/10, porque o juro americano está no maior nível desde 2007 (Treasury de 10 anos a 5,00% em 23/10, `us_interest_rate`, do externo), porque o mercado de títulos ainda não reabriu e porque o autor das promessas pode não estar na Fazenda em 2027. A cauda de baixa fica em 13–18%: o que a sustenta é um projeto anunciado por dois veículos, ainda não enviado.

**O que derrubaria a tese** (signposts):
- CDS acima de 165 por dez pregões, ou NTN-B 10a acima de 8,50% por dez pregões: a cauda de alta passa a ser a base.
- NTN-B 10a abaixo de 7,50% e CDS abaixo de 125 por dez pregões, ou o envio do projeto de lei complementar do centro da meta com corte de despesa: a cauda de baixa ganha probabilidade.
- Leilões do Tesouro sem retomada até 13/11, ou mais recompras: o mercado de títulos segue sem funcionar e a `rr_10a` de 4T26 vai para o limite de cima da faixa.
- Projeto do centro da meta não enviado até o fim de 1T27, ou alta da Selic em 09/12 (os gatilhos que a PM dá para o argumento dela voltar para cima): a queda de 2027 da `rr_10a` sai da base.
- Focus de primário de 2027 revisado para abaixo de −0,50% do PIB, ou de IPCA de 2029 acima de 3,50%: o sinal de mercado da dominância deixa de ser só preço local.

**Olhado, sem sinal.**
- Primário das estatais · −0,04% do PIB em 12m (`fisc_nfsp` · ago/26) · pequeno e estável · diria algo se capitalizações virassem déficit relevante.
- DLSP de estados e municípios · 8,1% do PIB, sem variação em 12m (`fisc_divida` · ago/26) · parada · diria algo com renegociação de dívida subnacional.
- Subsídios, subvenções e Proagro · −0,8% real em 12m (`fisc_rtn` · ago/26) · sem movimento até agosto · diria algo em set–out, quando a desoneração da gasolina de 09/10 aparecer na receita.
- Inversões financeiras (GND 5) · −7,8% real (`fisc_investimento` · ago/26) · não é demanda e caiu · diria algo com capitalização de estatal.
- Inadimplência dos bancos públicos · 4,7%, +1,1 p.p. em 12m (`cred_credito_controle_capital` · ago/26, TWA) · os privados também subiram (+0,8) · diria algo sobre risco parafiscal se descolasse dos privados.
- Reservas internacionais · US$ 365 bi (`cmb_reservas_bc` · 26/10) · −US$ 4 bi em 3 meses · diria algo com venda à vista do BC, que entraria no ajuste da DLSP.
- Brasil Soberano · R$ 15 bi da MP 1.345/2026 para capital de giro pelo BNDES (CNN Brasil · 15/05 · nível B) · a matéria não cita o Tesouro e não chega perto dos R$ 126 bi · diria algo se a MP autorizasse empréstimo do Tesouro.
- Nomes cotados para a Fazenda · Fonteles e Alckmin, segundo o veículo, sem fonte (Poder360 · 27/10 · nível B; Alckmin também em CNN Brasil/Reuters · 05/10 · nível C) · nenhuma escolha anunciada · diria algo quando a equipe do segundo mandato for anunciada.

## 3. Premissas

### 3.1 Etapa 1 — o modelo

**Cenários.**
- **Base:** o governo reeleito mantém a política fiscal de 2026 com ajustes nas margens: as promessas de 26–27/10 viram um projeto que demora, o Orçamento de 2027 sai com o mínimo, o remanejamento e a subvenção, sem nova onda de crédito do Tesouro ao BNDES; o mercado de títulos reabre em novembro; o Copom não sobe, e a alta que a curva cobra nos dois primeiros anos devolve ao longo de 2027.
- **Upside (ruim):** as promessas não se cumprem e as decisões de 2027 afrouxam a política fiscal (estímulos renovados, despesa fora da regra, novo aporte ao BNDES), com o mercado lendo a reação monetária como insuficiente, e um risk-off global soma-se (o do externo); os sinais de mercado da dominância se espalham para o CDS e as expectativas longas.
- **Downside (bom):** o projeto do centro da meta é enviado com corte de despesa e aprovado, o Orçamento de 2027 sai sem os estímulos de 2026, e o apetite global a risco melhora.

**Caminhos das exógenas.** As outras exógenas seguem o caminho do P2, o dos seus principais.

| Exógena | Hoje (valor · tabela · data) | Cenário | 4T26 | 1T27 | 2T27 | 3T27 | 4T27 | 1T28 |
|---|---|---|---|---|---|---|---|---|
| CDS 5 anos, fechamento (`fiscal`, p.b.) | 137 · `cmb_risco_pais` · 26/10 (3T26: 131) | base | 140 | 142 | 139 | 135 | 130 | 125 |
| | | upside | 170 | 205 | 210 | 205 | 198 | 190 |
| | | downside | 122 | 115 | 112 | 110 | 108 | 106 |
| NTN-B 10 anos, média (`rr_10a`, % a.a.) | 8,05 · `br_interest_rate` · 26/10 (3T26: 7,84; 4T26 até 26/10: 6,99) | base | 7,75 | 7,95 | 7,90 | 7,80 | 7,75 | 7,70 |
| | | upside | 8,15 | 8,90 | 9,10 | 9,10 | 9,00 | 8,90 |
| | | downside | 7,36 | 7,30 | 7,15 | 7,05 | 7,00 | 6,95 |

- Motivo da `rr_10a` em 4T26: a média já tem 17 pregões a 6,99%; os três valores equivalem aos 43 restantes a ~8,05% (base), ~8,6% (upside) e ~7,5% (downside) (G `fi_r2_juros`).
- Motivo do upside: o CDS fica perto do risk-off do externo somado ao componente global (175 em 4T26 e 204 em 1T27, externo, rodada 2), e a `rr_10a` de 9,10% fica ~0,9 p.p. acima do máximo de 10 anos (8,20%) e ~1,3 p.p. acima de 3T26, dentro da faixa do percentil 95 da variação de dois a três trimestres desde 2016 (+1,15 a +1,51 p.p.).
- Motivo do downside: a NTN-B volta abaixo da média de set/26 (7,59%) e o CDS ao nível de abr–mai/26 (médias de 129 e 124, `cmb_risco_pais`), níveis vistos sem a expectativa de troca de governo.
- Além de 1T28, os três caminhos repetem o último valor.

**O que o modelo faz com esses caminhos** (as endógenas são teses dos outros agentes; aqui só o que o modelo devolve, G `fi_rf_cenarios`).

| Variável (modelo) | Cenário | 4T26 | 1T27 | 2T27 | 3T27 | 4T27 | 1T28 |
|---|---|---|---|---|---|---|---|
| PTAX, fechamento (R$/US$) | base | 5,43 | 5,52 | 5,52 | 5,50 | 5,51 | 5,53 |
| | upside | 5,55 | 5,78 | 5,81 | 5,79 | 5,79 | 5,80 |
| | upside, `F.b_fiscal` × 1,2 | 5,59 | 5,86 | 5,89 | 5,86 | 5,85 | 5,85 |
| | downside | 5,35 | 5,41 | 5,42 | 5,41 | 5,44 | 5,47 |
| Selic, média (% a.a.) | base | 13,51 | 13,37 | 13,04 | 12,69 | 12,43 | 12,18 |
| | upside | 13,91 | 14,33 | 14,25 | 14,02 | 13,72 | 13,44 |
| | downside | 13,12 | 12,72 | 12,28 | 11,93 | 11,66 | 11,41 |
| Selic, fechamento (derivada, % a.a.) | base | 13,44 | 13,21 | 12,87 | 12,56 | 12,30 | 12,10 |
| IPCA 12 meses (%) | base | 5,34 | 4,95 | 4,46 | 4,48 | 4,32 | 4,14 |
| | upside | 5,35 | 5,01 | 4,58 | 4,64 | 4,49 | 4,28 |
| | downside | 5,33 | 4,92 | 4,41 | 4,42 | 4,26 | 4,10 |
| Hiato (% do potencial) | os três | 0,13 | −0,08 | −0,24 | −0,36 | −0,45 | −0,52 |

Fonte: Modelo Estrutural do ciclo, centrais, com as exógenas do P2 nas chaves de outros principais; faixas de 90% do posterior no log da G. A base é a do P2 com a `rr_10a` de 4T26 0,03 p.p. mais alta, o que muda a Selic média de 4T26 em 0,03 p.p. e nada depois.

**A história que o modelo conta, antes de discordar dela.**

- **O CDS chega pelo câmbio, e só a variação conta.** Na base, o CDS sobe 9 p.b. em 4T26 e 2 em 1T27 e depois cai 3 a 5 p.b. por trimestre: deprecia um pouco no começo e aprecia um pouco depois, e a PTAX fica perto de 5,50–5,53 no horizonte. No upside, o CDS a 205 em 1T27 leva a PTAX a ~5,78 (~5,86 com o × 1,2 que o câmbio aplica), e daí sobem alimentos e bens industriais: IPCA de 12 meses de 4,28% em 1T28 contra 4,14% na base.
- **A `rr_10a` chega pela âncora da regra, e o modelo a repassa à Selic um a um.** Como na curva IS o aperto é `(Selic − meta) − rr_10a`, e a Selic sobe junto, o hiato sai idêntico nos três cenários. Na leitura do mapa (2.10): um prêmio fiscal maior no juro longo sobe o neutro do modelo, e a regra leva a Selic até ele sem apertar a demanda; a queda da `rr_10a` no downside (consolidação precificada) dá ao modelo espaço para cortar ~0,65 p.p. a mais em 1T27 sem afrouxar o hiato.
- **Onde este agente discorda:** a alta de 26/10 é, na maior parte, prêmio de prazo e fiscal sobre um juro real de política que mudou pouco (+22 dos +135 p.b. nos dois primeiros anos); repassá-la um a um à Selic trata prêmio como neutro. A PM mediu o tamanho: o prêmio de 26/10 põe 0,8 a 1,0 p.p. na Selic de fechamento do modelo, e a distribuição dela já o desconta, porque os regimes dela não seguem a `rr_10a` (ata da moderação, item 5); o atividade o lê como custo de capital, no tempero dele. O modelo não muda neste ciclo; a proposta está na seção 6.

### 3.2 Etapa 2 — o tempero

A distribuição da tese vem dos três cenários e das probabilidades acima. Os dois temperos que este agente argumenta são aplicados por outros (seção 4):

**(i) CDS — efeito no câmbio mais forte que o estimado** · cenário upside
- O multiplicador é do agente de câmbio, que aplica × 1,2 no upside (câmbio, rodada 2); aqui só o argumento.
- Coeficiente: `F.b_fiscal` estimado em 25,1 por desvio-padrão da variação do CDS (298,5 p.b.), intervalo de 90% de 19,5 a 30,6. Multiplicador × 1,2, dentro do intervalo, percentil 94.
- Efeito: a PTAX do upside vai de ~5,78 para ~5,86 em 1T27 e de ~5,81 para ~5,89 em 2T27 (G `fi_rf_cenarios`).
- Por quê: em outubro o real andou 4 a 6 vezes o que o CDS explica no modelo, e o prêmio de agora, o de um resultado eleitoral que dura o horizonte, é de inflação e juro local, que o CDS mede mal. No upside, que é o cenário de estresse, o canal não linear pesa mais.
- Por que não na base: na regressão trimestral simples, 2006 a 3T26, a PTAX sobe 1,35% por 10 p.b. de CDS com o CDS abaixo de 200 no início do trimestre, contra 1,21% na amostra inteira (`cmb_ptax`, `cmb_risco_pais`, G `fi_r2_moderacao`): pouco a mais, sem os outros regressores da (F), e a conta do câmbio, que os tem, dá o contrário. Em log o canal é mais fraco com o CDS baixo (2,2% por 10% de CDS, contra 3,0% acima de 200). Retirei também o × 1,5 do limite da cauda, fora do intervalo.
- Onde entra: limite da cauda de alta da PTAX.

**(ii) Impulso e parafiscal sobre o hiato · tributos e subsídios sobre o IPCA**: direção, tamanho e duração na seção 4 (para atividade e inflação).

### 3.3 Da etapa 1 à tese

| Trimestre | CDS: central · upside · downside (p.b.) | `rr_10a`: central · upside · downside (%) |
|---|---|---|
| 4T26 | 140 · 170 · 122 | 7,75 · 8,15 · 7,36 |
| 1T27 | 142 · 205 · 115 | 7,95 · 8,90 · 7,30 |
| 2T27 | 139 · 210 · 112 | 7,90 · 9,10 · 7,15 |
| 3T27 | 135 · 205 · 110 | 7,80 · 9,10 · 7,05 |
| 4T27 | 130 · 198 · 108 | 7,75 · 9,00 · 7,00 |
| 1T28 | 125 · 190 · 106 | 7,70 · 8,90 · 6,95 |

A faixa da base fica entre a central e cada caminho de cauda, mais perto da central do lado de baixo, porque o cenário bom tem menos probabilidade; os caminhos de cauda ficam fora da faixa, como pontos típicos de cada cauda, e a probabilidade de cada cauda é a do cenário dela.

## 4. Para os outros agentes

**Premissas fiscais para os outros, primeiro.**

- **Ao agente de atividade (FE-AT1, S-FI1):** o impulso por trimestre, em p.p. do PIB, impulso de 12 meses no fim do trimestre (+ = expansionista), premissa deste agente sobre o Focus de 23/10. Não mudou desde a rodada 1, e as falas de Durigan de 26–27/10 não o mudam: elas são a história do downside, não um corte decidido.

  | | 4T26 | 1T27 | 2T27 | 3T27 | 4T27 | 1T28 |
  |---|---|---|---|---|---|---|
  | Base | +0,1 | 0,0 | −0,1 | −0,1 | −0,2 | −0,3 |
  | Upside (afrouxamento) | +0,3 | +0,3 | +0,4 | +0,4 | +0,5 | +0,3 |
  | Downside (consolidação) | 0,0 | −0,2 | −0,3 | −0,4 | −0,5 | −0,5 |

  Medido hoje: +0,3 a +0,4 (12 meses até ago/26). 4T26: o bloqueio de empenho de R$ 24 bi "cai para zero em dezembro" (Agência Brasil · 01/10 · nível B), e os tributos da gasolina estão zerados desde 09/10 (nível B): os dois sustentam o +0,1. 2027: o remanejamento de ~R$ 20 bi para Bolsa Família, Pé-de-Meia, Desenrola 3.0 e Pix MEI (nível A) e o salário mínimo de ~R$ 50 bi de despesa (nível B) põem mais da despesa em transferência às famílias, o canal que chega mais rápido ao consumo; o total segue o Focus. Parafiscal: ~0,9 p.p. do PIB de crédito do Tesouro ao BNDES em 12 meses, com desembolso em 4T26–1S27, sem nova onda na base.
- **Ao agente de atividade (FE-AT2, S-FI2):** o caminho da `rr_10a` está na seção 3.1, ~0,1 p.p. acima de 3T26 em 1T27. Do salto de 26/10 leio como prêmio o que está depois dos dois primeiros anos (+40 p.b. nos anos 2 a 5 e +73 nos anos 5 a 10, decomposição da PM); a base devolve em 2027 a parte de política, e o prêmio dos anos 5 a 10 fica. Concordo com a sua leitura de custo de capital, que é sua.
- **Ao agente de inflação (FE-IN1, IN-S6), em destaque:** o que as notícias trazem, todas de nível B, que sustenta que foi feito ou dito, sem documento oficial aberto:
  - Gasolina: a MP 1.395, de 09/10, zerou PIS/Pasep, Cofins e Cide-Combustíveis e ampliou subsídios, "por 30 dias, com possibilidade de revisão ou prorrogação" (Agência Brasil · 09/10). Se não for prorrogada, o tributo volta no começo de novembro, um degrau para cima na gasolina dentro do 4T26; se for, a alta fica para depois.
  - Diesel: subvenção "de R$ 1,20 por litro para a importação de diesel", "pode chegar a R$ 4 bilhões", válida "inicialmente por dois meses" (Agência Brasil · 06/04), sem o número da MP; o valor e o prazo da MP 1.391 não foram achados.
  - 2027: Durigan disse que a proposta deve ser manter a ajuda, se o Brent seguir alto, e que a lei atual vale só para 2026 (Poder360 · 23/10).

  Direção: as duas medidas baixam os combustíveis medidos enquanto durarem, e o fim de cada uma é um degrau para cima. Não há o tamanho do tributo da gasolina em centavos. Tratar 2027 no tempero de combustíveis do 1T27, e não na central, é coerente com o nível B; a decisão é sua.
- **Ao agente de PM (FE-PM1, FE-PM2, S11, S12):** a postura fiscal é expansionista em 2026 e, na base, levemente contracionista em 2027, com o primário respondendo à dívida só em promessa. O caminho da `rr_10a` é o que você aceitou na moderação, com 4T26 a 7,75 em vez de 7,72, porque o juro real longo subiu de novo em 27/10 (nível B). S12, o que o projeto do centro da meta tira, se for enviado com corte de despesa: é a diferença entre a base e o downside, ~0,2 a 0,3 p.p. do PIB de impulso por trimestre em 2027, ~0,65 a 0,75 p.p. de `rr_10a` e ~20 a 27 p.b. de CDS (G `fi_rf_cenarios`); o conteúdo não foi noticiado, então o tamanho é o do meu cenário, não o do projeto.
- **Aos agentes de câmbio, PM e externo (FE-CB1, FE-EX1):** o caminho do CDS é a tese da seção 1. Leitura: o 3T26 foi global; em outubro o doméstico comprimiu o CDS até 23/10 e o abriu em 26/10 (a conta do externo com datas casadas); os +18 p.b. de 26/10 são o resultado da eleição, fiscal no sentido do mapa, porque vieram com o juro longo e a inflação implícita e com o governo respondendo com promessas fiscais. A base carrega o componente global do externo na alta e na queda, com o doméstico parado. Possível emenda de fonte no CDS em 21/09: se a carga da Bloomberg substituir o trecho provisório e o nível mudar, leia os caminhos em variação a partir de 3T26.
- **Ao agente de câmbio (S6, sobre `F.b_fiscal`):** × 1,2 só no upside, a ficha (i). O projeto de Durigan (nível A de que foi anunciado) é a história do downside, a 13–16% no CDS; os subsídios de 2027 (nível B) e a Fazenda em aberto (nível B) são parte do upside, a 27–30%.
- **Ao agente de câmbio (FE-CB2, S2/S7), leitura de dominância:** sustentabilidade presente, mercado presente nos preços locais e no mercado de títulos, regime monetário com sinal só verbal; cauda de dominância de ~10% no horizonte, ~15% condicionada a uma alta em 09/12 com o fiscal de 2027 sem decisão.
- **Ao agente de expectativas (FE-EP1, XS8):** o fato entre 23 e 26/10 foi o 2º turno (nível A); depois houve resposta fiscal do governo (nível A e B), e não evento fiscal antes. O projeto do centro da meta é a história do meu downside de CDS e NTN-B, a 13–18%; ele ganha probabilidade com o envio, que o ministro situou "ainda em 2026" (nível B). A alta da implícita longa é prêmio de evento com fundamento fiscal: a dívida sobe 5 p.p. por ano.
- **Ao agente externo (XS5, XS6):** respondidos na moderação; a parte americana da queda da `rr_10a` em 2027 é a sua, ~−0,07 dos −0,25 p.p.

**Pedidos** (para o próximo ciclo).

- **FS-EP1, em destaque:** a revisão do Focus de primário, nominal, DLSP e DBGG depois de 26/10, e se o primário do Focus conta ou não as deduções da meta. (F4, a comparação com a meta, e as caudas.)
- **FS-EP2:** o Focus de IPCA de 2029–2030 depois de 26/10. (Sinal de mercado da dominância.)
- **FS-PM4:** se o Copom mantiver ou subir em 04/11 ou 09/12, a curva longa e o real reagem como credibilidade ou como custo da dívida? (Probabilidade da cauda de dominância.)
- **FS-CB1:** os pares latinos de 26–27/10, quando entrarem no F. (A divisão global/doméstica do CDS de 4T26.)
- **FS-IN2:** a gasolina do 4T26 com e sem a prorrogação da MP 1.395. (Mesma decisão nos dois cenários, mapa 3.3.)
- **FS-AT2:** consumo e investimento do governo de 3T26, em dezembro. (A direção do impulso.)

**Ao agente web.**

- **W8:** a meta fiscal de 2026 e 2027 é do governo central? O que entra nos R$ 65,6 bi de exclusões, de documento oficial (LDO, PLOA, relatório bimestral)? (Tese: F4.)
- **W9:** o projeto de lei complementar do centro da meta: enviado, quando, conteúdo (corte de despesa, contingenciamento, banda). (Tese: a probabilidade do downside.)
- **W10:** o custo fiscal da MP 1.395 (gasolina) e se foi prorrogada depois dos 30 dias; o valor e o prazo da MP 1.391 (diesel); proposta formal para 2027. (Tese: FE-IN1 e o primário.)
- **W11:** quando os leilões do Tesouro voltaram e quanto mais foi recomprado depois de 27/10. (Tese: a `rr_10a` de 4T26.)
- **W12:** a base legal dos R$ 126 bi de crédito do Tesouro ao BNDES entre set/25 e ago/26, e novo aporte em 2027. (Tese: o parafiscal; terceira vez.)
- **W13:** o ministro da Fazenda do segundo mandato. (Tese: a credibilidade das promessas, as caudas.)
- **W14:** declaração ou proposta sobre a meta de inflação ou o regime de metas. (Insumo de `meta_12m`.)

**Como subordinado.**

- `meta_12m` · principal: política monetária
- Insumos: nenhuma informação nem sinal de que o governo pretende mudar ou discutir a meta de inflação. O agente web não achou nada nas duas rodadas (demanda r1 e r2, "Sem notícia", item sobre a meta); as matérias sobre "centro da meta" tratam da meta fiscal. A fala de Lula de 24/10, "quero que o Banco Central baixe o juro" (Poder360 · nível B), é sobre a Selic, não sobre a meta; a de Galípolo de 27/10, sobre o mandato e as prerrogativas do presidente da República (Poder360 · nível B).
- Argumento e caminho de referência: nada a acrescentar neste ciclo; 3,00% do principal.

**Divergências** (como principal de `fiscal` e `rr_10a`). O P2 não lista nenhuma.

- **`rr_10a`, política monetária (subordinada):** fechada na moderação. A PM argumentou na rodada 1 por 8,05% segurado e eu subi o caminho; na rodada 2 ela retirou o caminho de referência com o argumento da curva real (+22 p.b. nos dois primeiros anos devolvem se o Copom não subir), e eu fui a um ponto intermediário, 7,72 · 7,95 · 7,90 · 7,80 · 7,75 · 7,70, que ela aceitou. No report final só o 4T26 muda, de 7,72 para 7,75, pelo pregão de 27/10 (nível B), na direção do argumento original dela; o resto fica.
- **`rr_10a`, externo (subordinado):** fechada. A parte americana da queda de 2027 é a dele.
- **`fiscal` (CDS), externo (subordinado):** fechada na moderação. Ele retirou o caminho de referência (140 · 140 · 138 · 132 · 126 · 120) depois que eu apliquei o desconto do viés do dólar contra emergentes às duas pernas do componente global; a cauda de alta tem o risk-off dele.
- **Com o câmbio, sobre `F.b_fiscal`:** fechada; × 1,2 só no upside.
- **Com a inflação, sobre a subvenção:** aberta, e estreita: é sobre a decisão, não sobre o preço. Nos combustíveis, as duas bases deixam o degrau de janeiro de fora: o fim da subvenção sem renovação é upside dela (inflação, rodada 2, IN-E7). Divergimos em como a base chega lá. Eu suponho que o governo renova para 2027 a autorização legal da subvenção, com custo no primário de 2027; ela não supõe decisão, o que deixa o custo fora e o degrau só na cauda. Três coisas decidem:
  - **O fato:** um ato legal (MP ou projeto) que estenda a subvenção a 2027, com valor, antes de 31/12/2026, quando acaba a autorização atual (Durigan, Poder360 · 23/10 · nível B). Se sair, a minha base vale e o custo entra no primário de 2027. Se 2026 terminar sem ele, a minha base tira o custo, e o degrau de janeiro fica onde a inflação já o põe: alta no 1T27, na cauda de alta dela (dentro dos +5% de combustíveis do upside), não na central, que não vê combustíveis.
  - **O primeiro sinal, no começo de novembro:** a MP 1.395, da gasolina, prorrogada ou não ao fim dos seus 30 dias (Agência Brasil · 09/10 · nível B).
  - **A condição que o ministro pôs:** o Brent "num patamar muito elevado" (r1-22), que no base do externo segue em ~US$ 105 em 1T27.
  Não muda nenhum caminho do P.

## 5. Placar

Primeiro ciclo: não há report final anterior deste agente.

## 6. Sobre o modelo

O modelo não muda neste ciclo (decisão do usuário); o que segue são propostas.

| Fonte | O que sugere | Teste proposto | Por que importa para a tese deste ciclo |
|---|---|---|---|
| Rodadas do modelo deste ciclo e mapa 2.10; a PM mediu 0,8 a 1,0 p.p. de Selic pelo prêmio de 26/10 e propõe liberar o coeficiente da âncora; o atividade propõe um termo de custo de capital na (H) | A regra repassa a `rr_10a` à Selic um a um, e o hiato fica invariante a ela; um prêmio fiscal no juro longo vira juro neutro integral | Separar a `rr_10a` na parte de política (os dois primeiros anos da curva real) e no prêmio (anos 2 a 10, ou a parte explicada pelo CDS e pela inflação implícita), e estimar a regra e a IS com as duas; se o peso do prêmio na âncora for menor que 1, ou negativo na IS, a âncora deveria ser construída sem ele | Decide se o caminho da `rr_10a` deste agente move a Selic do P na medida certa: hoje ele é, na prática, a central da Selic |
| Dados do ciclo (inflação implícita 10a +0,9 p.p. em 26/10; em 27/10 o juro real longo subiu com a implícita caindo) e mapa 2.9; câmbio e expectativas propõem o mesmo para a (F) e a (E) | O choque fiscal de hoje aparece na curva local e não no CDS; a (F) não tem regressor que o capture | Incluir na (F) a variação da inflação implícita de 10 anos (ou do diferencial NTN-B 10a − Treasury 10a) e ver se ela tira poder do CDS e do resíduo nos trimestres de choque doméstico | O CDS sozinho subestima o canal fiscal no câmbio em choques como o de 26/10 |
| Regressão trimestral deste ciclo (G `fi_r2_moderacao`) e a do câmbio | A sensibilidade da PTAX ao CDS não é estável: em p.b. muda pouco com o nível do CDS, em log cai com o CDS baixo. Nem p.b. nem log resolvem, e o canal não linear de 26/10 não aparece no trimestral | Testar na (F) a interação ΔCDS × volatilidade implícita, ou uma dummy de episódio eleitoral, em 2006–2026; mudar se a interação entrar com sinal positivo e intervalo fora de zero | Decide se o peso do CDS no estresse é um multiplicador de cauda (como hoje) ou especificação |

[^proc]: Primeiro ciclo conjunto, report final: sem literatura (o agente lê só o mapa conceitual), com as notícias que o agente web achou para os pedidos das rodadas 1 e 2, os reports das rodadas 1 e 2 dos outros seis agentes, a consolidação P2 e a ata da moderação. Não há dado de pesquisa eleitoral nesta análise; o resultado da eleição entra como notícia de nível A. Dados fiscais com defasagem: RTN, NFSP e DLSP até ago/26 (87 dias antes do corte), EFGG e PIB até 2T26 (209 dias). Os preços de 27/10 não estão no F e entram só por notícia.
[^cdsdef]: CDS de 5 anos: o preço de um seguro contra o calote da dívida externa do Brasil por 5 anos, em pontos-base por ano sobre o valor segurado. 137 p.b. quer dizer pagar US$ 1,37 milhão por ano para segurar US$ 100 milhões. Sobe quando o mercado vê mais risco de o governo não pagar em dólar.
[^impl]: Inflação implícita: a diferença entre o juro prefixado e o juro real da NTN-B do mesmo prazo, (1 + DI)/(1 + NTN-B) − 1. Mede a inflação que o mercado cobra para emprestar sem indexação, com um prêmio de risco de inflação dentro. Ex.: DI de 15,13% e NTN-B de 8,05% dão 6,55%.
[^recompra]: Leilão e recompra: o Tesouro financia a dívida vendendo títulos em leilões semanais. Cancelar leilões e recomprar títulos é o contrário, tirar títulos do mercado, o que o Tesouro faz quando a taxa que o mercado pede num pregão disfuncional é alta demais para travar por anos.
[^impulso]: Impulso fiscal: a mudança da postura de um período para o outro. Se o déficit primário passa de 0,2% para 0,6% do PIB sem que a economia tenha esfriado, o governo pôs 0,4% do PIB a mais de demanda na economia: impulso de +0,4. Aqui ele não é corrigido pelo ciclo, porque o hiato é do agente de atividade.
[^prim]: Resultado primário: receitas menos despesas do governo, sem contar os juros da dívida. Um primário de −0,62% do PIB quer dizer que, antes de pagar juros, o setor público gastou 0,62% do PIB a mais do que arrecadou. "Acima da linha" (RTN, Tesouro) mede pelas receitas e despesas; "abaixo da linha" (NFSP, BC) mede pela variação da dívida. Na NFSP, negativo é déficit; nos fatores da DLSP, positivo é déficit.
[^prec]: Precatórios: dívidas do governo reconhecidas pela Justiça. O pagamento se concentra num ou dois meses do ano, e o mês mudou de jul/25 para mar/26; por isso uma janela de 3 meses que perde um pagamento parece um ajuste fiscal que não houve. A meta fiscal pode excluí-los; a dívida, não.
[^para]: Parafiscal: o governo empurrando a demanda sem passar pelo primário, emprestando a bancos públicos (aqui, o Tesouro ao BNDES) que emprestam a empresas. Na dívida líquida o empréstimo é um ativo do governo e aparece com sinal negativo: o estoque ir de −R$ 107 bi para −R$ 233 bi é mais crédito concedido.
[^pct]: Percentil: a posição do valor de hoje no histórico, de 0 (o menor já visto) a 100 (o maior). Percentil 57 do hiato quer dizer que 57% dos trimestres desde 2003 tiveram hiato menor.
[^meta]: Meta com banda e deduções: a regra fixa um primário a perseguir (o centro) e uma tolerância em torno dele. Com meta de 0,25% do PIB e tolerância de 0,25 p.p., um resultado entre 0,00% e 0,50% cumpre a regra; o piso é 0,00%. E certas despesas, como precatórios, podem ser descontadas antes da comparação: por isso a regra pode ser cumprida com um primário que, contado inteiro, é déficit.
[^focus]: O F não diz a que conceito de primário a pesquisa Focus se refere, e a notícia não diz a que esfera a meta se aplica; a tabela compara números que podem ter coberturas diferentes. A confirmação foi pedida em FS-EP1 e W8.
[^div]: Dívida líquida (DLSP) contra bruta (DBGG): a bruta soma o que o governo deve; a líquida desconta o que ele tem a receber, como as reservas internacionais e os empréstimos ao BNDES. Por isso o real mais fraco reduz a líquida (as reservas valem mais em reais) e mal mexe na bruta, e o crédito ao BNDES aumenta a bruta sem mexer na líquida.
[^swap]: Ordem de grandeza: a posição vendida de ago/26 (US$ 91,6 bi) vezes a alta da PTAX de 23/10 para 26/10 (R$ 0,46). A posição de outubro e o ajuste diário dos contratos tornam o número de out/26 diferente; ele sai na NFSP de outubro.
[^cds]: O CDS é carregado à mão de um export da Bloomberg, com um trecho provisório de outra fonte (aviso do F). O F não diz onde o trecho provisório começa; o salto de 21/09 (+9 p.b. num pregão com o real mais forte e o DI 10a mais baixo) é o candidato. Se for emenda, o nível de 3T26 em diante pode estar alto em ~9 p.b., e as variações a partir dali continuam válidas.
[^dom]: Dominância fiscal: quando a dívida pesa tanto que subir juros piora o risco da dívida, o real se deprecia e a inflação sobe, em vez de cair. É um espectro, e os sinais vêm em três conjuntos: o regime monetário, a sustentabilidade fiscal e os preços de mercado.
[^q4]: A conta da média de 4T26 supõe 43 pregões restantes (dias úteis de 27/10 a 31/12, menos 02/11, 20/11, 24/12, 25/12 e 31/12); um ou dois pregões a mais ou a menos mudam a média em menos de 0,02 p.p.
[^prazo]: Prêmio de prazo e fiscal: o quanto o juro de 10 anos paga acima do juro de política que se espera para os próximos anos, por travar o dinheiro por mais tempo e pelo risco de a dívida ser paga com inflação ou mudança de regras. A medida aqui é a da PM: a NTN-B 10a contra o juro real de política que o Focus esperava para 2028 (6,02%) e 2029 (6,28%), antes do choque.
