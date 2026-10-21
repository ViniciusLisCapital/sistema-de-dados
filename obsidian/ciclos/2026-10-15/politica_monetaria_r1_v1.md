# Report — política monetária · ciclo 2026-10-15 · rodada 1

Dados até: 15/10/2026 · Horizontes: os seis trimestres do Modelo Estrutural a partir do trimestre em curso (4T26 a 1T28), com a meta Selic no fechamento do trimestre (a decisão da última reunião do Copom dentro dele)

## 1. Tese

| Variável | Trimestre | Central | Base: faixa · P | Cauda worst: limite · P | Cauda best: limite · P | Pbc − Pwc |
|---|---|---|---|---|---|---|
| Selic meta, fechamento do trimestre (% a.a.) | 4T26 | 12,47[^1] | 12,25 a 12,75 · 0% | acima de 12,75 · 100% | abaixo de 12,25 · 0% | −1,00 |
| | 1T27 | 12,14 | 12,00 a 12,50 · 4% | acima de 12,50 · 96% | abaixo de 12,00 · 0% | −0,96 |
| | 2T27 | 11,86 | 11,50 a 12,00 · 3% | acima de 12,00 · 97% | abaixo de 11,50 · 0% | −0,97 |
| | 3T27 | 11,62 | 11,25 a 11,75 · 11% | acima de 11,75 · 89% | abaixo de 11,25 · 0% | −0,89 |
| | 4T27 | 11,41 | 11,25 a 11,75 · 29% | acima de 11,75 · 70% | abaixo de 11,25 · 1% | −0,69 |
| | 1T28 | 11,22 | 11,00 a 11,50 · 29% | acima de 11,50 · 68% | abaixo de 11,00 · 3% | −0,65 |

- **Worst (Selic acima da faixa).** Em 4T26–3T27 a massa está aqui por dois caminhos que se somam. O primeiro está no próprio cenário base: o Copom move a Selic no máximo 25 p.b. por reunião, e com isso ela não fecha 4T26 abaixo de 13,25 nem 1T27 abaixo de 12,75, contra 12,47 e 12,14 do modelo (tempero (ii) do gradualismo, seção 3.2). O segundo é o cenário worst: a queda de outubro no juro real de 10 anos se desfaz (NTN-B 10a de volta a 7,80) e o CDS vai a 150; o modelo dá 13,15 no 4T26 e 12,27 no 1T28, a regra reagindo 1,3 vez ao desvio da expectativa leva a 13,31 e 12,68, e a pausa do Copom diante do petróleo a US$ 125 (tempero (ii)) põe o fechamento em 13,75 no 4T26 e no 1T27.
- **Best (Selic abaixo da faixa).** Só ganha probabilidade a partir do 4T27 (1% e 3%). O cenário best (NTN-B 10a a 6,30, CDS a 95, Fed devolvendo a alta de setembro) dá 12,21 no 4T26 e 10,54 no 1T28; com a expectativa convergindo à meta mais depressa (tempero (i)), 12,16 e 10,35. O gradualismo eleva esses pontos a 13,25 no 4T26 e 10,75 no 1T28: o fechamento só cai abaixo da faixa se o Copom cortar 25 p.b. em todas as reuniões até lá (dez no 4T27, doze no 1T28), ou acelerar para 50.
- **Onde está a massa**[^2]: média do fechamento 13,45 (4T26), 13,15 (1T27), 12,85 (2T27), 12,55 (3T27), 12,28 (4T27) e 12,02 (1T28); intervalo de 90% de 13,25–13,75 no 4T26 a 11,00–13,50 no 1T28. É de 0,07 a 0,30 p.p. acima da Focus e da curva DI em cada trimestre de 2026–2027.
- **A tese em uma frase:** o Copom segue cortando 25 p.b. por reunião, com pausas prováveis já em novembro ou dezembro, e fecha 2026 entre 13,25% e 13,75% e 2027 perto de 12,25%; isso fica acima do modelo, que corta quase 1 p.p. a mais porque a âncora da sua regra (o juro real de 10 anos) caiu 0,97 p.p. em outubro, e um pouco acima da Focus e da curva, porque o petróleo a US$ 125, a surpresa do IPCA de setembro e o descumprimento provável da meta em fevereiro empurram o Copom para pausas.

**Reunião a reunião, os dois próximos trimestres** (probabilidade de cada passo; incondicional)

| Reunião | Trimestre | +25 | Manter | −25 | −50 | Curva DI: passo implícito | Focus: mediana |
|---|---|---|---|---|---|---|---|
| 04/11/26 | 4T26 | 0% | 37% | 60% | 3% | −18 p.b. | 13,50 |
| 09/12/26 | 4T26 | 1% | 46% | 52% | 1% | −19 p.b. | 13,25 |
| 27/01/27 | 1T27 | 3% | 37% | 58% | 2% | −20 p.b. | 13,25 |
| 17/03/27 | 1T27 | 3% | 35% | 60% | 2% | −19 p.b. | 13,00 |

Curva: `br_di_grade` · 14/10. Focus: `expc_focus_copom` · 09/10. As probabilidades de cada reunião dependem do que aconteceu na anterior (uma pausa em novembro torna outra pausa em dezembro mais provável), e é essa cadeia que dá o fechamento de cada trimestre:
- 4T26: 13,00 · 3% · 13,25 · 40% · 13,50 · 31% · 13,75 · 25% · 14,00 · 1%. Todos acima de 12,75: é a linha do 4T26 na tese.
- 1T27: 12,50 · 4% · 12,75 · 24% · 13,00 · 23% · 13,25 · 21% · 13,50 · 16% · 13,75 · 9% · 14,00 · 2% · 14,25 · 1%. Só 12,50 (4%) cai na faixa base.

## 2. Argumentação

### Q1. Qual é a função de reação do Copom, e a que ela está respondendo agora?

O Copom opera por metas de inflação com alvo na projeção (forecast targeting)[^3] e com gradualismo[^4]: cortou 25 p.b. em cada uma das cinco últimas reuniões, de 15,00% para 13,75% (`pm_copom_reuniao` · 16/09), enquanto a projeção no horizonte relevante[^5] ficou "ao redor da meta". Essa projeção é 3,2% para o 1T28, 0,2 p.p. acima dos 3,00% (`pm_copom_projecoes` · RPM de 24/09), e foi feita com a trajetória da Focus de 11/09 (13,75% no fim de 2026, 12,00% em 2027, 10,50% em 2028; RPM set/26, 2.2). O Copom aceita, portanto, uma convergência um pouco acima da meta para não mover a Selic aos saltos: em junho escolheu trajetórias "que não induziam volatilidade excessiva nos preços dos ativos", mesmo que convergissem um trimestre depois (RPM set/26, 2.4). A orientação não mudou entre a 280ª e a 281ª: "a magnitude total do ciclo de calibração será estabelecida à luz de novas informações" (comunicado da 281ª, 6º parágrafo; ata da 281ª, §17), com "serenidade e cautela" (ata da 281ª, §19). O que mudou no texto foi a atividade, que passou de "sugere uma moderação" para "mostra uma moderação gradual, principalmente em setores mais cíclicos" (comunicados da 280ª e da 281ª, 2º parágrafo).

O que move a decisão agora, em ordem de peso:
- **Expectativas desancoradas, o motivo da cautela.** A conclusão unânime da 281ª é que "em um ambiente de expectativas desancoradas, como é o caso do atual, exige-se uma restrição monetária maior e por mais tempo do que outrora seria apropriado" (ata da 281ª, §10). A Focus segue acima da meta em todo horizonte: 4,30% para 2027 e 3,79% para 2028 (`expc_focus_periodo` · 09/10), praticamente sem mudança em quatro semanas (+0,00 e −0,01 p.p.), o que mostra que a queda das expectativas não começou.
- **A inflação de setembro surpreendeu para cima**, porque o IPCA de 0,82% (`inflc_agregados` · set/26) ficou 0,17 p.p. acima da projeção do próprio Copom para o mês (0,65%, RPM set/26, Tabela 2.1.2) e 0,26 p.p. acima da mediana do QPC (0,56%, `expc_qpc` · 23/09). A surpresa não ficou só na energia, que o Copom já esperava pela devolução do bônus de Itaipu: a média dos cinco núcleos do BC (EX0, EX3, MS, DP, P55) foi 0,36%, 0,07 p.p. acima do QPC, e o EX3 de serviços foi 0,36%, 0,06 p.p. acima (`inflc_agregados` · set/26). Com isso o IPCA de 12 meses voltou a 4,58%, acima do teto de 4,50%.
- **O hiato foi revisto para cima.** A edição de setembro do RPM elevou em 0,10 a 0,15 p.p. todos os trimestres desde o 2T25 (`pm_hiato_produto_vintages` · 01/09), e o RPM cita o hiato mais alto como a primeira pressão altista no horizonte relevante (RPM set/26, Sumário executivo). Serviços seguem em 5,97% em 12 meses (`inflc_agregados` · set/26), que é o grupo mais sensível ao hiato (RPM set/26, 2.3, risco ii).
- **O choque do petróleo: o Copom não reage ao efeito primário, e reage "com firmeza" ao de segunda ordem** (ata da 281ª, §16). O Brent está em US$ 125,44 (`comm_brent` · 06/10), 39% acima da média de US$ 90 que o cenário de referência usou para o 3T26 e 49% acima dos ~US$ 84 que ele supõe para o 2T27 (RPM set/26, 2.2). É a maior notícia desde a reunião, e ela não está na projeção de 3,2%. O boxe do RPM não encontra efeito de segunda ordem relevante até agosto, mas registra que as expectativas de inflação das empresas e dos consumidores e a expectativa de custo de mão de obra subiram depois do conflito (RPM set/26, boxe "evidências de efeitos de segunda ordem")[^6].
- **Fiscal**, como determinante do prêmio e do neutro (ata da 281ª, §8). O resultado primário de 12 meses está em −0,62% do PIB, 0,43 p.p. pior que um ano antes, e a dívida bruta em 82,9% do PIB, +5,5 p.p. em 12 meses (`fisc_nfsp` e `fisc_divida` · ago/26), mas o CDS de 5 anos está em 112 p.b., 40 p.b. abaixo de um ano antes (`cmb_risco_pais` · 14/10). O dado fiscal piora devagar e o preço do risco soberano não o acompanha neste momento.
- **Câmbio**, como risco de alta: "uma taxa de câmbio persistentemente mais depreciada" (comunicado da 281ª, 4º parágrafo, risco iii). A PTAX de 5,0441 em 14/10 está 2,1% abaixo dos R$ 5,15 do cenário de referência (`cmb_ptax`), o que hoje joga a favor do corte; se isso persiste é **aguarda câmbio (S1, S4)**.
- **Externo**: o Fed subiu 25 p.b. em setembro (`us_interest_rate` · 15/10: meta de 3,75%–4,00%, ponto médio 3,88) e a Treasury de 10 anos está em 5,10%, +1,05 p.p. em 12 meses. O Copom cita a incerteza sobre a política monetária nas economias avançadas (ata da 281ª, §1 e §4).

O Copom está agindo como sua função de reação implica: os passos são os mesmos e a projeção no horizonte relevante não se moveu (3,2% nas duas últimas reuniões, `pm_copom_projecoes`). Mas o quadro que entra na 282ª é pior que o da 281ª em três dados (IPCA de setembro, Brent, Focus de 2026 a 5,22%, +0,32 p.p. em 4 semanas, `expc_focus_periodo` · 09/10) e melhor em dois (câmbio e curva longa). A próxima projeção também vai usar uma Focus com Selic mais baixa (13,25% no fim de 2026, contra 13,75% em 11/09, `expc_focus_periodo` · 09/10), o que por si só sobe a projeção. Por isso dou 37% a uma pausa em 04/11, contra 28% implícitos na curva (o passo implícito de −18 p.b. equivale a 72% de chance de −25 se as opções forem só manter ou −25; `br_di_grade` · 14/10).

A equação (R) do Modelo Estrutural não é a função de reação do Copom (mapa 2.1), e neste ciclo a diferença é grande. Na (R), a Selic persegue o juro real de 10 anos mais a meta, e uma mudança da NTN-B passa para a Selic média do mesmo trimestre quase uma por uma: com tudo o mais igual, segurar a NTN-B 10a na média do 3T26 (7,84) em vez do nível de 15/10 (6,87) sobe a Selic média do modelo em 0,95 a 0,97 p.p. em todos os trimestres. O Copom usa outro neutro (5,00%, RPM set/26, 2.2), que não se move com o preço do título, e move a Selic 25 p.b. por reunião.

### Q2. Quão restritiva está a política monetária, e contra qual juro neutro?

Restritiva contra qualquer neutro, e mais contra o do próprio Copom:

| Medida | Valor (% a.a.) | Fonte · data | Selic real ex-ante menos o neutro (p.p.) |
|---|---|---|---|
| Selic real ex-ante: 13,75 deflacionada pela Focus 12 meses (4,48) | 8,88 | F, Leituras combinadas · 15/10 | — |
| Neutro do Copom, cenário de referência | 5,00 | RPM set/26, 2.2 | +3,88 |
| Neutro do QPC, curto prazo / 2 anos / 5 anos | 6,40 / 6,00 / 5,50 | `expc_qpc` · R279, 24/06 | +2,48 / +2,88 / +3,38 |
| Âncora do Modelo Estrutural: NTN-B 10 anos | 6,87 | `br_interest_rate` · 15/10 | +2,01 |
| Juro real de mercado de 1 ano (NTN-B 1a) | 5,80 | `br_interest_rate` · 15/10 | — |

- **Uso o neutro do Copom (5,00%) para ler a decisão do Copom**, porque é com ele que o Copom projeta e decide; a Selic real ex-ante fica acima dele em toda a trajetória da Focus, e o próprio RPM descreve a política como contracionista em todo o horizonte de projeção (RPM set/26, 2.2)[^7]. A central da tese, porém, sai da âncora do modelo, a NTN-B de 10 anos, e as duas medidas discordam neste ciclo: a âncora caiu 0,97 p.p. contra a média do 3T26 (`br_interest_rate`), e pela medida do modelo (Selic − NTN-B 10a − meta) o aperto subiu de 3,22 p.p. na média do 3T26 para 3,88 hoje. É por isso que o modelo corta: para ele, outubro apertou a política sem o Copom fazer nada.
- **O juro real de mercado de 1 ano conta outra história**: 5,80%, só 0,80 p.p. acima do neutro do Copom, porque a inflação implícita de 1 ano (6,84%) está 2,36 p.p. acima da Focus de 12 meses (`br_interest_rate` · 15/10). A diferença mistura a inflação maior que o mercado espera do petróleo e o prêmio de risco de inflação[^8]; a medida da Focus é a que o Copom usa (RPM set/26, 2.2), por isso fica como contraponto, não como medida principal.
- **O que move o neutro, e para que lado.** Para cima: o neutro do QPC de 2 anos subiu 0,50 p.p. entre a R275 e a R279 (`expc_qpc`), e o Copom aponta o crédito direcionado e a incerteza da dívida como forças que elevam o neutro (ata da 281ª, §8). O crédito direcionado cresce bem acima do livre: saldo imobiliário +13,8% e rural PJ +30,6% em 12 meses (`cred_modalidade_direcionado_pf` e `_pj` · ago/26), contra saldo livre PJ +0,5% (`cred_credito_resumo` · ago/26). Para baixo: o prêmio de risco longo, porque a NTN-B de 10 anos caiu 0,74 p.p. em um mês (`br_interest_rate` · 15/10) com o CDS parado (`cmb_risco_pais` · 14/10). Todo neutro é medido com erro; Perrelli e Roache mostram que o erro custa pouco quando a regra reage com força à inflação e ao hiato, e muito quando a regra se ancora na estimativa do neutro[^9]. A regra do modelo está mais perto do segundo caso.
- A Selic de 13,75% está no percentil[^10] 84 dos últimos 10 anos e no 56 do histórico (`br_interest_rate` · 13/10).

### Q3. A política monetária está chegando à inflação?

Chega à atividade e ao crédito; ainda não chega às expectativas.
- **Atividade, sim.** O PIB cresceu 0,5% no 2T26 com o consumo das famílias −0,4% (`atv_pib_taxas` · 2T26); o IBC-Br caiu 0,9% em três meses até julho (`atv_ibcbr`), a indústria 2,1% em três meses até agosto (`atv_pim`) e o varejo ampliado 0,9% (`atv_pmc` · ago/26). A queda está nos setores mais sensíveis ao juro, o que mostra o canal agindo: móveis e eletrodomésticos −8,7% em três meses (`atv_pmc`), bens de capital −3,9% em 12 meses (`atv_pim_uso` · ago/26). O RPM baixou o PIB de 2026 de 2,0% para 1,8% e projeta 1,4% para 2027 (RPM set/26, boxe do PIB).
- **Crédito e balanço das famílias, sim**, pelo canal do balanço[^11]: a inadimplência do crédito livre PF está em 8,01% (+1,04 p.p. em 12 meses) e o comprometimento de renda com dívida em 28,72% (+1,40 p.p.) (`cred_credito_resumo` · ago/26; `cred_credito_familias` · jul/26), e o saldo livre PJ caiu 1,1% em três meses. Mas o direcionado enfraquece o canal (ata da 281ª, §6), como mostram os números da Q2.
- **Mercado de trabalho, ainda não.** A desocupação está em 5,3% e a renda real habitual cresce 3,7% em 12 meses (`mt_pnad` · ago/26), acima da produtividade (ata da 281ª, §7). A criação de vagas desacelera: o saldo do Caged de 12 meses no comércio foi 97,7 mil, contra 322,2 mil um ano antes, e na indústria 15,9 mil contra 210,3 mil (`mt_caged_setor` · ago/26).
- **Expectativas, não.** A Focus de 2027 subiu de 4,10% em junho para 4,30% (RPM set/26, 2.2; `expc_focus_periodo` · 09/10), a de 2028 está em 3,79% e a de 2029 em 3,50%; a de 24 meses à frente em 3,91% (`expc_focus` · 09/10). O único sinal bom de credibilidade é de mercado: a inflação implícita de 10 anos caiu 0,73 p.p. em um mês, para 5,55% (`br_interest_rate` · 15/10), mas segue 2,55 p.p. acima da meta e caiu toda num único pregão, de 6,18% em 02/10 para 5,42% em 05/10, junto com a curva inteira, o que aponta para prêmio de risco e não para uma releitura do Copom.

A inflação subjacente de três meses (julho a setembro) somou 0,85% na média dos cinco núcleos, 3,45% anualizados sem ajuste sazonal (`inflc_agregados` · set/26), perto da meta; mas o próprio Copom espera variações trimestrais dessazonalizadas dos núcleos acima da meta nos próximos meses (RPM set/26, 2.1), e serviços estão em 5,97% em 12 meses. Para eu concluir que a política chegou à inflação, a Focus de 2027 teria de cair abaixo de 4,0% sem a ajuda de desonerações.

### Q4. Que trajetória de Selic o mercado precifica, e onde ela diverge da sinalização do Copom e da leitura do agente?

| Reunião | Focus (09/10) | Curva DI (14/10) | Curva − Focus (p.b.) | Média do agente no fechamento do trimestre |
|---|---|---|---|---|
| 04/11/26 | 13,50 | 13,57 | +7 | |
| 09/12/26 | 13,25 | 13,38 | +13 | 4T26: 13,45 |
| 27/01/27 | 13,25 | 13,18 | −7 | |
| 17/03/27 | 13,00 | 12,99 | −1 | 1T27: 13,15 |
| 28/04/27 | 12,75 | 12,79 | +4 | |
| 16/06/27 | 12,62 | 12,58 | −5 | 2T27: 12,85 |
| 04/08/27 | 12,50 | 12,39 | −11 | |
| 22/09/27 | 12,25 | 12,25 | −0 | 3T27: 12,55 |
| 27/10/27 | 12,00 | 12,16 | +16 | |
| 08/12/27 | 12,00 | 12,13 | +13 | 4T27: 12,28 |

Fonte das três primeiras colunas: F, Leituras combinadas (`br_di_grade`, `expc_focus_copom`).

- **Curva e Focus quase coincidem**: a diferença fica entre −11 e +16 p.b. em todas as reuniões, e as duas põem a Selic em 12,00–12,13 no fim de 2027, 1,62 a 1,75 p.p. abaixo de hoje. Isso indica pouco prêmio de prazo[^8] na parte curta, ou prêmio que compensa uma discordância; a curva não separa os dois.
- **A curva mudou de patamar em outubro, não por causa do Copom.** Em um mês a Selic precificada caiu 6 p.b. na reunião de novembro e 194 p.b. na de dezembro de 2027 (`br_di_grade` · 14/10 contra 14/09), e o DI de 10 anos saiu de 14,15 (02/10) para 12,81 (05/10) num pregão, enquanto a Treasury de 10 anos subia de 5,28 para 5,31 (`br_interest_rate`, `us_interest_rate`). O salto coincide com o primeiro pregão depois do 1º turno (04/10)[^12], e é o mesmo arcabouço que a Verde usou para 2022: o calendário eleitoral põe prêmio na curva acima do ciclo esperado, e a resolução de risco de cauda o tira de uma vez[^13].
- **A sinalização do Copom é condicional**, sem trajetória: o tamanho do ciclo depende de novas informações (comunicado da 281ª, 6º parágrafo). Em 23/09, antes da reprecificação, a maioria do QPC esperava pausa na 282ª (53%) e na 283ª (66%) (`expc_qpc`); a Focus passou de 13,75 para 13,50 na reunião de novembro em quatro semanas (`expc_focus_copom` · 09/10).
- **Minha leitura diverge para cima** em 0,07 a 0,30 p.p. por trimestre, porque ponho mais peso em pausas do que a curva (37% em novembro, 46% em dezembro). Espaço para surpresa: se o Copom mantiver em 04/11, a curva curta tem 18 p.b. a ajustar; se cortar 25, 7 p.b.
- A curva é preço com prêmio, e a Focus é a trajetória que entra no cenário de referência do Copom, não a que ele pretende (mapa 2.9).

### Q5. Qual o cenário prospectivo para a Selic?

**Por que a central.** No cenário base cada exógena fica no nível de hoje: NTN-B 10a em 6,87%, CDS em 112, Fed funds em 3,88%, dólar contra emergentes em 129,77, commodities no nível de setembro (seção 3.1). O modelo faz três coisas com isso. Primeiro, a âncora da regra cai 0,97 p.p. contra o 3T26, e a Selic média do 4T26 cai para 12,65%, quase 1 p.p. abaixo do caminho com a âncora antiga. Segundo, a expectativa de 12 meses converge devagar, de 4,17% no 4T26 para 3,52% no 1T28, e o desvio contra a meta que a regra lê encolhe. Terceiro, o hiato fica negativo a partir do 1T27 (−0,51 no 1T28), sem segurar a inflação: o IPCA de 12 meses sai de 5,29% no 4T26 para 4,09% no 1T28, acima dos 3,2% do Copom. O modelo, portanto, corta mais que o Copom e entrega menos desinflação; a central é a dele, sem ajuste[^1].

**Por que a distribuição.** Quatro temperos (seção 3.2):
- o gradualismo do Copom, que o modelo não vê: está no cenário base e, por não mover a central, entra como assimetria, a maior delas (+0,78 p.p. sobre o modelo no 4T26, +0,03 no 1T28);
- a pausa diante do petróleo a US$ 125 com sinais de segunda ordem, no worst;
- a regra reagindo 1,3 vez ao desvio da expectativa, no worst, porque é o que a ata da 281ª, §10, diz que o Copom fará;
- a expectativa convergindo mais depressa, no best, apoiada só na queda da inflação implícita longa.

O worst é mais provável que o best em todos os trimestres. O gradualismo põe sozinho quase toda a massa acima da faixa até 2T27, e entre os riscos dos dados (petróleo, IPCA, expectativa de 2027) não há nenhum que empurre o Copom a acelerar para 50 p.b., enquanto há três que o levam a pausar.

**O que derrubaria a tese** (indicador e limiar):
- Para baixo: corte de 50 p.b. em 04/11; ou Focus de 2027 abaixo de 4,00% com o Brent abaixo de US$ 100 até 09/12.
- Para cima, além da faixa do worst: Focus de 2027 acima de 4,50%; ou NTN-B 10a de volta acima de 7,50% por duas semanas; ou o Copom trocando "calibração" por linguagem de manutenção prolongada.

### Outros pontos

- **Descumprimento provável da meta no 1T27.** O IPCA de 12 meses passou o teto de 4,50% em setembro (4,58%, `inflc_agregados`), e o Copom projeta 5,2% no 4T26 e 4,9% no 1T27 (`pm_copom_projecoes`). Se ficar acima até fevereiro, como a projeção indica, são seis meses seguidos fora do intervalo, e a meta contínua é formalmente descumprida com o IPCA de fevereiro, divulgado antes da reunião de 17/03[^14]. O RPM estima 90% de chance de o IPCA passar do teto no fim de 2026 (RPM set/26, Tabela 2.2.2). Uma carta aberta às vésperas da reunião de março pesa contra cortes nela: é parte dos 35% de pausa que dou a 17/03.
- **Desonerações de combustíveis seguram o IPCA medido.** A Lei Complementar 235, o Decreto 13.116 (PIS/Cofins da gasolina −R$ 0,63/L por trinta dias) e a MP 1.391 (subvenção ao diesel anunciada em R$ 1,00/L) entraram depois do conflito; o cenário de referência supõe o fim delas no prazo legal e não incorpora a MP 1.391 (RPM set/26, 2.2, nota 45). A Verde leu o mesmo expediente em 2022 como meta salva por corte de imposto e custo adiado[^15]: se o Copom cortar apoiado num IPCA desonerado, o risco aparece quando as desonerações acabarem. Fica no worst, pela via do petróleo.
- **O câmbio jogou a favor em outubro, mas a leitura não é minha.** A PTAX caiu 2,4% em um mês enquanto o peso mexicano subiu 8,0% e o chileno 4,4% contra o dólar (`cmb_ptax` · 14/10; `cmb_fx_latam` · 13/10). Se a apreciação é persistente e idiossincrática é **aguarda câmbio (S1, S2)**; assumi que ela não muda o passo de novembro sozinha.

### Olhado, sem sinal

- Swap cambial do BC · −US$ 91,6 bi (`cmb_reservas_bc` · ago/26) · posição estável (+1,3 em um mês) · diria algo se o BC ampliasse a oferta acima dos vencimentos (leitura do câmbio, S7).
- Taxa de câmbio real efetiva · 116,46 (`cmb_reer` · ago/26) · 75 dias defasada, anterior ao movimento de outubro · diria algo com o dado de outubro.
- Pesquisa trimestral de crédito · oferta PF consumo −0,23 (`cred_ptc` · 2T26) · 197 dias defasada · diria algo com a edição do 3T26, se a oferta apertasse ainda mais.
- Fluxo financeiro · −2,8% do PIB em 12 meses (`cred_fluxo_financeiro` · abr/26) · defasado e sem ligação clara com o passo do Copom · diria algo se virasse de sinal.
- Despesa do governo geral · +3,7 p.p. do PIB em 4 trimestres (`fisc_efgg` · 2T26) · soma sem consolidar, e juros explicam 1,8 p.p. da alta · diria algo como impulso se a parte primária crescesse sem os juros.
- Juros de política na América Latina · Colômbia +0,25 para 12,25%, México, Chile e Peru parados (`inter_interest_rate` · 13/10) · nenhum par muda o que o Copom pondera · diria algo se vários subissem por causa do petróleo.
- Índice de difusão do IPCA · 54,9% (`inflc_agregados` · set/26) · +2,7 p.p. em 12 meses, sem salto · diria algo acima de 60% por dois meses.
- Posição de fundos alavancados em BRL · 27.396 contratos, +11.350 em um mês (`cmb_cot_fx` · 06/10) · posicionamento é leitura do câmbio · diria algo pela S6.

## 3. Premissas

### 3.1 Etapa 1 — o modelo

**Cenários.**
- Base: o 2º turno (25/10) e o início do novo governo não desfazem a reprecificação de 05/10; o Fed fica em 3,75%–4,00%; dólar e commodities no nível de hoje.
- Worst: o 2º turno ou o primeiro sinal fiscal do governo eleito desfaz a reprecificação, e o prêmio volta ao nível do 3T26; o Fed sobe mais uma vez; o dólar se fortalece contra emergentes; El Niño encarece as commodities agrícolas (RPM set/26, 2.2).
- Best: a reprecificação se aprofunda e o CDS cai; o Fed devolve a alta de setembro; o dólar cede contra emergentes; commodities agrícolas recuam com a desaceleração global.

**Caminhos das exógenas** (na unidade do simulador; as do bloco do câmbio que a política monetária não usa ficam no padrão: inflação americana 0,91% por trimestre, S&P 500 em 7.651,54, volatilidade implícita em 12,19, segurada do 2T26)

| Exógena | Hoje (valor · tabela · data) | Cenário | 4T26 | 1T27 | 2T27 | 3T27 | 4T27 | 1T28 |
|---|---|---|---|---|---|---|---|---|
| Meta de inflação, 12 meses (%) | 3,00 · `inflc_meta` · 2026 | base · worst · best | 3,00 | 3,00 | 3,00 | 3,00 | 3,00 | 3,00 |
| Juro real de 10 anos, NTN-B (% a.a., média do trimestre) | 6,87 · `br_interest_rate` · 15/10 | base | 6,89 | 6,87 | 6,87 | 6,87 | 6,87 | 6,87 |
| | | worst | 7,30 | 7,80 | 7,80 | 7,80 | 7,80 | 7,80 |
| | | best | 6,75 | 6,50 | 6,30 | 6,30 | 6,30 | 6,30 |
| CDS 5 anos (p.b., fechamento) | 112 · `cmb_risco_pais` · 14/10 | base | 112 | 112 | 112 | 112 | 112 | 112 |
| | | worst | 135 | 150 | 150 | 150 | 150 | 150 |
| | | best | 105 | 95 | 95 | 95 | 95 | 95 |
| Fed funds (% a.a.)[^16] | 3,88 · `us_interest_rate` · 15/10 | base | 3,88 | 3,88 | 3,88 | 3,88 | 3,88 | 3,88 |
| | | worst | 3,88 | 4,13 | 4,13 | 4,13 | 4,13 | 4,13 |
| | | best | 3,88 | 3,63 | 3,63 | 3,63 | 3,63 | 3,63 |
| Dólar contra emergentes (índice, fechamento) | 129,77 · `cmb_dollar_index_em` · 09/10 | base | 129,77 | 129,77 | 129,77 | 129,77 | 129,77 | 129,77 |
| | | worst | 132 | 133 | 133 | 133 | 133 | 133 |
| | | best | 128 | 126 | 126 | 126 | 126 | 126 |
| IC-Br em dólar (índice) | 205,70 · `comm_icbr_usd` · set/26 | base · worst · best | 205,70 | 205,70 | 205,70 | 205,70 | 205,70 | 205,70 |
| IC-Br agropecuária em dólar (índice, média do trimestre) | 201,80 · `comm_icbr_usd` · set/26 | base | 201,80 | 201,80 | 201,80 | 201,80 | 201,80 | 201,80 |
| | | worst | 206 | 212 | 212 | 212 | 212 | 212 |
| | | best | 198 | 192 | 192 | 192 | 192 | 192 |
| IC-Br metal em dólar (índice, média do trimestre) | 335,06 · `comm_icbr_usd` · set/26 | base · worst · best | 335,06 | 335,06 | 335,06 | 335,06 | 335,06 | 335,06 |

- NTN-B 10a no 4T26 do base: a média do trimestre até 15/10 com o último valor mantido até 31/12 (6,89). No worst, 7,80 é a volta à média do 3T26 (7,84), o nível de antes de 05/10; o 4T26 fica a meio caminho porque metade do trimestre já passou perto de 6,9.
- O CDS e o dólar contra emergentes entram no simulador como fechamento do trimestre; a NTN-B e os IC-Br de agropecuária e metal, como média.
- O Brent não é exógena do modelo: entra pelo tempero (ii) do petróleo.

**Saída do modelo** (central; a faixa do posterior está no log da G)

| Variável | Cenário | 4T26 | 1T27 | 2T27 | 3T27 | 4T27 | 1T28 |
|---|---|---|---|---|---|---|---|
| Selic, fechamento do trimestre, derivada (% a.a.) | base | 12,47 | 12,14 | 11,86 | 11,62 | 11,41 | 11,22 |
| | worst | 13,15 | 13,09 | 12,84 | 12,63 | 12,44 | 12,27 |
| | best | 12,21 | 11,65 | 11,25 | 10,98 | 10,75 | 10,54 |
| Selic, média do trimestre (% a.a.) | base | 12,65 | 12,29 | 11,99 | 11,73 | 11,51 | 11,31 |
| | worst | 13,06 | 13,23 | 12,96 | 12,73 | 12,53 | 12,35 |
| | best | 12,51 | 11,90 | 11,39 | 11,11 | 10,86 | 10,64 |
| IPCA, 12 meses (%) | base | 5,29 | 4,87 | 4,35 | 4,37 | 4,24 | 4,09 |
| | worst | 5,35 | 5,05 | 4,60 | 4,65 | 4,50 | 4,26 |
| | best | 5,24 | 4,72 | 4,15 | 4,12 | 4,02 | 3,95 |
| Focus IPCA 12 meses à frente (%) | base | 4,17 | 3,98 | 3,79 | 3,68 | 3,60 | 3,52 |
| | worst | 4,18 | 4,01 | 3,85 | 3,76 | 3,68 | 3,60 |
| | best | 4,16 | 3,95 | 3,74 | 3,61 | 3,52 | 3,46 |
| Hiato (% do potencial) | base | 0,13 | −0,08 | −0,24 | −0,36 | −0,45 | −0,51 |
| PTAX, fechamento (R$/US$; saída do modelo, sem leitura minha) | base | 5,18 | 5,22 | 5,22 | 5,21 | 5,23 | 5,25 |
| | worst | 5,35 | 5,48 | 5,49 | 5,47 | 5,49 | 5,52 |
| | best | 5,09 | 5,02 | 5,03 | 5,02 | 5,03 | 5,05 |

A faixa de 90% do posterior da central do base vai de 12,14–12,78 no 4T26 a 10,46–12,15 no 1T28. Ela mede só a incerteza dos pesos, não o erro das equações; a distribuição da tese é minha.

### 3.2 Etapa 2 — o tempero qualitativo

**(i) Regra de juros: reação ao desvio da expectativa contra a meta — efeito mais forte que o estimado** · cenário worst
- Coeficiente: estimado 1,962, intervalo de 90% do posterior 1,148 a 2,726. Multiplicador: × 1,3 (2,550), dentro do intervalo, no percentil 87.
- Efeito: Selic de fechamento do worst de 13,15 → 13,31 (4T26), 13,09 → 13,37 (1T27), 12,84 → 13,20 (2T27), 12,63 → 13,03 (3T27), 12,44 → 12,86 (4T27), 12,27 → 12,68 (1T28).
- Por quê: a conclusão unânime da 281ª é que expectativas desancoradas exigem "restrição monetária maior e por mais tempo do que outrora seria apropriado" (ata da 281ª, §10), o que é dizer que a reação ao desvio é hoje maior que a média histórica; a amostra da estimação (2006–2026) mistura períodos de expectativa ancorada. Fica perto da cauda (percentil 87), por isso só no worst, onde a expectativa sobe.
- Onde entra: limite e probabilidade da cauda worst.
- Checkpoints: Copom · 04/11; Copom · 09/12.

**(i) Expectativas: inércia da expectativa — efeito mais fraco que o estimado** · cenário best
- Coeficiente: estimado 0,581, intervalo de 90% do posterior 0,452 a 0,710. Multiplicador: × 0,9 (0,523), dentro do intervalo, no percentil 22. Como o peso da meta é 1 − e1 − e2, menos inércia é mais peso na meta.
- Efeito: Selic de fechamento do best de 12,21 → 12,16 (4T26), 11,65 → 11,56 (1T27), 11,25 → 11,13 (2T27), 10,98 → 10,83 (3T27), 10,75 → 10,57 (4T27), 10,54 → 10,35 (1T28).
- Por quê: a inflação implícita de 10 anos caiu 0,73 p.p. em um mês (`br_interest_rate` · 15/10), sinal de que o prêmio de inflação longo pode ceder mais rápido se a reprecificação se aprofundar. A Focus de 2027 e de 2028 não mostra isso, por isso o multiplicador é leve e só no best.
- Onde entra: cauda best.
- Checkpoints: Focus de 2027 · semanal; Copom · 09/12.

**(ii) Gradualismo e o neutro do Copom — passo máximo de 25 p.b. por reunião** · cenários base, worst e best
- Hoje: Selic 13,75% (`br_interest_rate` · 13/10), cinco cortes seguidos de 25 p.b. (`pm_copom_reuniao`); NTN-B 10a 6,87%, 0,97 p.p. abaixo da média do 3T26 (`br_interest_rate` · 15/10); neutro do Copom 5,00% (RPM set/26, 2.2).
- Por que o modelo não vê: a regra (R) é trimestral, não conhece o calendário de reuniões e se ancora na NTN-B 10a, que repassa para a Selic do mesmo trimestre quase uma por uma (Q1). O Copom ancora no próprio neutro e anda 25 p.b. por reunião sob "serenidade e cautela" (ata da 281ª, §19). Pelo calendário, a Selic de 13,75% vale em pouco mais de um terço do 4T26 antes da primeira decisão (04/11); o fechamento de 12,47% pede 1,25 p.p. de corte em duas reuniões.
- Efeito: um piso para o fechamento de 13,25 (4T26), 12,75 (1T27), 12,25 (2T27), 11,75 (3T27), 11,25 (4T27) e 10,75 (1T28). Sobre a central do modelo, +0,78, +0,61, +0,39, +0,13, +0,09 e +0,03 p.p.: forte em 2026, quase nulo a partir do 4T27.
- Onde entra: assimetria do cenário base (é a maior parte do Pwc de 4T26 a 2T27) e limite da cauda best.
- Checkpoints: Copom · 04/11; Copom · 09/12; Copom · 27/01.

**(ii) Petróleo e efeitos de segunda ordem — Brent** · cenário worst
- Hoje: US$ 125,44 (`comm_brent` · 06/10), máximo de US$ 135,51 em 02/10; 39% acima da média de US$ 90 que o cenário de referência usou no 3T26 e 49% acima dos ~US$ 84 que ele supõe no 2T27 (RPM set/26, 2.2).
- Por que o modelo não vê: o petróleo não é exógena do simulador. Os preços monitorados entram na curva de Phillips só pela própria inércia e pelo IPCA defasado, e o IC-Br em dólar entra só na equação do câmbio.
- O que o Copom faz com isso: não reage ao efeito primário e reage com firmeza ao de segunda ordem (ata da 281ª, §16). Os sinais de segunda ordem estão nas expectativas das empresas e dos consumidores e no custo de mão de obra esperado, que subiram depois do conflito (RPM set/26, boxe de efeitos de segunda ordem), não ainda nos preços. As desonerações de combustíveis seguram o IPCA medido e acabam no prazo legal.
- Efeito: no worst, o Copom para em 13,75% de novembro a março (duas reuniões por trimestre, dois trimestres) e depois volta a cortar 25 p.b. por reunião sem ir abaixo do worst do modelo com o tempero (i): 13,31 → 13,75 (4T26), 13,37 → 13,75 (1T27), 13,20 → 13,25 (2T27), 13,03 → 13,00 (3T27), 12,86 → 12,75 (4T27), 12,68 → 12,75 (1T28).
- Onde entra: probabilidade da cauda worst (a pausa de 37% em 04/11 e de 46% em 09/12).
- Checkpoints: Copom · 04/11; IPCA de outubro; Copom · 09/12.

### 3.3 Da etapa 1 à tese

| Trimestre | Central (modelo, base) | Worst: modelo → com tempero | Best: modelo → com tempero |
|---|---|---|---|
| 4T26 | 12,47 | 13,15 → 13,75 | 12,21 → 13,25 |
| 1T27 | 12,14 | 13,09 → 13,75 | 11,65 → 12,75 |
| 2T27 | 11,86 | 12,84 → 13,25 | 11,25 → 12,25 |
| 3T27 | 11,62 | 12,63 → 13,00 | 10,98 → 11,75 |
| 4T27 | 11,41 | 12,44 → 12,75 | 10,75 → 11,25 |
| 1T28 | 11,22 | 12,27 → 12,75 | 10,54 → 10,75 |

A faixa base é a grade de 25 p.b. em volta da central (três fechamentos possíveis, ±0,375 p.p.); as probabilidades saem da cadeia de reuniões da seção 1. Até 3T27, o best com tempero fica acima da faixa base, e o base com tempero também (13,25; 12,75; 12,25; 11,75): a massa vai quase toda para a cauda worst, que vai do piso do gradualismo ao worst com tempero. O best só tem probabilidade quando o piso desce abaixo da faixa, no 4T27 e no 1T28, e ela é pequena porque exige cortes em todas as reuniões.

## 4. Para os outros agentes

**Respostas às entradas fixas (mapa, Parte 4):**
- **E1 · trajetória esperada e balanço de riscos:** a tese da seção 1 e a tabela reunião a reunião. Na minha distribuição, o fechamento médio é 13,45% no 4T26, 13,15% no 1T27, 12,85% no 2T27, 12,55% no 3T27, 12,28% no 4T27 e 12,02% no 1T28, de 0,07 a 0,30 p.p. acima da Focus e da curva. O risco é de alta, por pausas: 37% em 04/11 e 46% em 09/12. O diferencial à frente cai menos que a curva precifica. A central do modelo (12,47 a 11,22) é a que o Modelo Estrutural consolida, mas fica abaixo do que o calendário permite até 2T27.
- **E2 · credibilidade:** no ciclo de cortes a pergunta é se o corte é lido como validar inflação, e até aqui não é, porque a inflação implícita de 10 anos caiu 0,73 p.p. no mês em que o Copom manteve o ritmo (`br_interest_rate` · 15/10). A credibilidade segue incompleta: a implícita longa está 2,55 p.p. acima da meta, e a Focus de 2027 (4,30%) e de 2028 (3,79%) não cai (`expc_focus_periodo` · 09/10). Com o CDS em 112 p.b. não há sinal de dominância fiscal[^17], e uma pausa ou uma alta seria lida como credibilidade, não como validação: o sinal juro → câmbio é o usual.
- **E3 · como o Copom descreveu o câmbio na última reunião:** como risco de alta, "uma taxa de câmbio persistentemente mais depreciada" (comunicado da 281ª, 4º parágrafo, risco iii); no cenário de referência, R$ 5,15 seguindo a PPC (ata da 281ª, §11). O RPM registra que o real voltou a se depreciar no 3T26, interrompendo cinco trimestres de apreciação, em parte pelo estreitamento do diferencial de juros (RPM set/26, 2.2). A apreciação de outubro (PTAX 5,0441 em 14/10, 2,1% abaixo de 5,15) é notícia para o Copom, na direção favorável; o condicionante da próxima reunião sai da média dos dez dias úteis até a sexta anterior (RPM set/26, Apêndice metodológico).
- **E4 · função de reação a uma depreciação:** o Copom não reage ao efeito primário; reage se a depreciação, por ser persistente, chegar às expectativas e aos preços (ata da 281ª, §16; RPM set/26, 2.3, risco iii). Neste ciclo de cortes, a primeira resposta seria pausar, que é a minha cauda worst; alta só se a Focus de 2027 subisse além de 4,50%. Em setembro o BC vendeu US$ 2,00 bi à vista e US$ 2,00 bi em linha (`cmb_reservas_bc` · set/26); se isso respondeu a disfunção ou defendeu o nível é a S7, e até a leitura do câmbio respondo pela Selic. Não marco em destaque porque o gatilho (postura de defesa do nível) depende dessa leitura.

**Pedidos ao câmbio** (mapa, Parte 3):
- **S1:** a apreciação do real em outubro (PTAX 5,0441 em 14/10, −2,4% em um mês, `cmb_ptax`) é persistente ou transitória, e o que a desfaria até 09/12? Depende disso a probabilidade de pausa em 04/11 e 09/12, e com ela as linhas de 4T26 e 1T27.
- **S2:** quanto do movimento de um mês do real é idiossincrático, se o peso mexicano subiu 8,0% e o chileno 4,4% contra o dólar no mesmo período (`cmb_fx_latam` · 13/10)? Depende disso a leitura de credibilidade da E2 e a premissa da NTN-B 10a no base.
- **S3** (provisório, até existir o agente de inflação): uma depreciação de volta a R$ 5,35 no 4T26, como no worst do modelo, chega a que preços e em quanto tempo, com o IPCA de 12 meses já acima do teto? Depende disso o tempero do petróleo e da segunda ordem no worst.
- **S4:** com a PTAX 2,1% abaixo do condicionante de R$ 5,15, você espera que o real ainda esteja abaixo dele na média dos dez dias antes de 04/11 e de 09/12? Depende disso a projeção que o Copom terá na mesa nas duas reuniões, e com ela o passo.
- **S5:** o real está precificando menos estresse fiscal ou institucional depois de 05/10, com o CDS parado em 112 p.b. em um mês (`cmb_risco_pais` · 14/10)? E essa leitura sobrevive ao 2º turno (25/10)? Depende disso o caminho da NTN-B 10a no base e a probabilidade do worst.
- **S6:** quanto o carry ainda sustenta o real, com o diferencial nominal em 10,00 p.p. (`diferenciais_juros` · set/26) e a curva precificando 1,62 p.p. a menos de Selic até dez/27? Depende disso o canal juro → câmbio → inflação no best.
- **S7:** as vendas de setembro (US$ 2,00 bi à vista e US$ 2,00 bi em linha, `cmb_reservas_bc`) responderam a disfunção de mercado ou defenderam o nível? Depende disso se a E4 passa a valer para a função de reação inteira, intervenção incluída.

**Pedido deste ciclo:** o câmbio tem uma leitura do prêmio de risco ligado ao calendário eleitoral (2º turno em 25/10) que separe o que já está no preço do que um resultado diferente desfaria? A probabilidade do cenário worst da NTN-B 10a (volta a 7,80) é a premissa mais pesada da cauda worst da tese.

## 5. Placar

Primeiro ciclo: não há report final anterior para pontuar.

---

[^1]: A central é a Selic de fechamento que o Modelo Estrutural dá no cenário base, sem ajuste. O modelo só tem a Selic média de cada trimestre; o fechamento é derivado como a média do trimestre mais a do seguinte, dividida por dois (erro histórico de 0,12 p.p. em média e 0,55 no pior trimestre, 2006–3T26). No 4T26 o número do modelo não é alcançável pelo calendário: a Selic de 13,75% vale até 04/11, e fechar em 12,47% pediria cortar 1,25 p.p. em duas reuniões. É por isso que a faixa base em volta dele tem probabilidade quase nula nos primeiros trimestres.
[^2]: As probabilidades da tese saem de um julgamento reunião a reunião (a chance de cada passo dado o que aconteceu na reunião anterior), agregado em fechamentos por trimestre. O calendário oficial do Copom termina em 08/12/2027; no 1T28 supus duas reuniões, como de hábito no primeiro trimestre.
[^3]: Metas de inflação com alvo na projeção (Svensson, 1997): o banco central fixa o juro para que a sua própria projeção de inflação, no prazo em que o juro faz efeito, fique na meta. Na prática, prever o juro vira prever a inflação projetada: projeção acima da meta, aperta; abaixo, afrouxa.
[^4]: Gradualismo (suavização dos juros): os bancos centrais andam em passos pequenos e seguidos em direção ao juro que querem, em vez de saltar de uma vez. Na regra estimada do BCB de 1999–2002, as duas defasagens da Selic somam 0,8 ou mais (Minella et al., 2002).
[^5]: Horizonte relevante: o trimestre à frente em que o Copom avalia se a inflação volta à meta, porque a Selic leva cerca de um ano e meio para fazer efeito pleno. Hoje é o 1T28. A projeção dele é condicional: usa a Selic da Focus, um câmbio que parte da cotação recente e segue a paridade de poder de compra, e o petróleo pela curva futura, e por isso não é a previsão do Copom.
[^6]: Efeito primário é o reajuste direto (gasolina, diesel) e indireto (frete, passagem aérea) que o petróleo causa; efeito de segunda ordem é quando essa inflação inicial muda a forma como empresas e trabalhadores reajustam preços e salários, por exemplo pela expectativa. O primeiro passa sozinho; o segundo, não.
[^7]: Juro neutro: o juro real que nem acelera nem freia a economia. Se o neutro é 5% e o juro real é 8,88%, a política está freando; se o neutro subir para 7%, o mesmo juro freia menos. Ninguém o observa: cada medida (o Copom, os analistas do QPC, o título de 10 anos) é uma estimativa.
[^8]: Prêmio de prazo (e prêmio de risco de inflação): o que o investidor cobra a mais para carregar um título longo ou nominal, além do juro e da inflação que ele de fato espera. Por isso a curva DI não é a previsão do mercado para a Selic, e a inflação implícita (a diferença entre o título nominal e o indexado) não é a inflação esperada.
[^9]: Perrelli e Roache (2014) estimam um neutro brasileiro que caiu cerca de 575 p.b. entre 2002–04 e 2010–13 com a queda da dívida, do risco soberano e dos juros globais, e mostram em simulação que errar o neutro custa pouco a um banco central que reage com força à inflação e ao hiato, porque o erro reaparece nesses desvios e é corrigido.
[^10]: Percentil: a posição do valor de hoje no histórico, de 0 (o menor já visto) a 100 (o maior). Percentil 84 em 10 anos quer dizer que a Selic esteve abaixo de 13,75% em 84% do tempo desde 2016.
[^11]: Canal do crédito e do balanço (Bernanke e Gertler, 1995): o juro alto encarece a dívida e corrói a renda livre de quem toma crédito, e o banco passa a cobrar mais caro de quem tem balanço pior. Inadimplência e comprometimento de renda em alta são a marca desse canal.
[^12]: O F não tem dado eleitoral. A data do 1º turno (04/10) e do 2º turno (25/10) é a do calendário eleitoral; o que os dados mostram é só o salto da curva no pregão de 05/10.
[^13]: Modelo mental da Verde Asset (§2.1), lido nas cartas de 2021–2022: a curva carrega prêmio fiscal e eleitoral acima do ciclo de juros esperado, e um resultado que reduz o risco de cauda o tira de uma vez, como o "rally importante no primeiro pregão de outubro" de 2022. É um modo de raciocinar, não uma opinião da Verde sobre hoje.
[^14]: Meta contínua: desde 2025 a meta é de 3% medida todo mês no IPCA de 12 meses, com intervalo de 1,5 p.p. para cada lado; ela só é considerada descumprida quando o IPCA fica fora do intervalo por seis meses seguidos, e então o BC publica uma carta explicando por quê.
[^15]: Modelo mental da Verde (§2.6), lido na carta de jan/2022 sobre o período 2011–2014: metas salvas por cortes temporários de impostos permitiram a um banco central "dócil" manter juros artificialmente baixos, e a conta veio depois. A meta cumprida por desoneração não é inflação controlada; é custo adiado.
[^16]: Comentário de processo: o simulador mostra 3,75 para os Fed funds no 3T26 e a série de A dá 3,88 para o ponto médio da meta em 30/09 e 3,66 para a média do trimestre; não consegui identificar qual medida ele usa. Usei o ponto médio da meta, o que soma 0,13 p.p. ao Fed funds no 4T26 do base contra o padrão do simulador.
[^17]: Dominância fiscal (Blanchard, 2004): quando a dívida é alta e o risco soberano é sensível ao juro, subir a Selic aumenta o risco de calote percebido e deprecia o câmbio, e a alta passa a gerar inflação em vez de contê-la. É um espectro, mais provável quanto maior a dívida e a aversão a risco; com o CDS em 112 p.b., o Brasil está longe da ponta.
