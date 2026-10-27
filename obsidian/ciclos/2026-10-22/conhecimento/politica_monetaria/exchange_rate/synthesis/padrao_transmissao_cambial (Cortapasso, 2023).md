---
aliases: ["Araújo 2023 - Padrões da transmissão cambial para taxa de inflação no Brasil"]
---

# Padrões da transmissão cambial para taxa de inflação no Brasil — Araújo, Caldarelli & Cortapasso 2023

**Type:** paper
**Tags:** #pass-through #brasil #metas-de-inflacao #var #nao-linearidade #ipca
**Source:** Nova Economia, v.33 n.2 p.363-392, 2023 (DOI 10.1590/0103-6351/7570)
**Language:** Portuguese
**Source file:** [[exchange_rate/clean_md/padrao_transmissao_cambial (Cortapasso, 2023)]]

---

## Context and motivation

Com a liberalização da conta de capitais em meados dos anos 1990 e o câmbio flutuante a partir de 1999, o canal cambial da política monetária passou a ser, segundo os autores, "extremamente relevante para o controle de preços". O fato estilizado de partida: sob metas de inflação, os anos de câmbio mais depreciado (2002, 2015 e 2021) foram os de inflação mais alta, e o período de câmbio relativamente apreciado (2005 a 2014) foi de inflação mais baixa. A literatura brasileira mede o tamanho do repasse (Belaisch, 2003; Minella et al., 2003), denuncia a sobreutilização do canal cambial (Modenesi & Araújo, 2013) e procura não linearidades (Pimentel et al., 2016; Fonseca et al., 2019). A pergunta do artigo: sob o regime de metas, o repasse cambial muda de tamanho quando o câmbio está em tendência de apreciação ou de depreciação? O objetivo empírico declarado não é explicar os determinantes do coeficiente, e sim detectar essa mudança.

## Core argument / thesis

O regime de metas brasileiro depende de forma "exacerbada" do repasse cambial, e esse repasse não é linear: é maior, mais efetivo e mais persistente quando o câmbio tende a se apreciar do que quando tende a se depreciar. A razão proposta é de demanda: no Brasil as depreciações coincidem com crises e retração da demanda agregada e com baixa utilização da capacidade, situação em que as empresas competem por preço e não conseguem repassar custos. Daí a combinação de juros altos e câmbio apreciado ser a que torna o regime de metas mais eficaz — e, para os autores, também a que impõe custos fiscais (dívida pública), distributivos (margens de lucro e concentração da renda), de crescimento (crédito e investimento) e industriais (conteúdo tecnológico, importações). A implicação de política é rediscutir o papel do câmbio "para além do controle de preços" (Bresser-Pereira, 2007).

## Key mechanisms / model

**Canais do repasse (seção 2, revisão da literatura):**
- *Direto*: a depreciação encarece insumos importados, o custo de produção sobe e chega ao consumidor final.
- *Indireto*: as exportações crescem, a procura por substitutos aumenta, a demanda por trabalho e os salários sobem e são repassados aos preços; e os preços de tradables sobem em relação aos non-tradables, de modo que o grau de abertura e a composição tradables/non-tradables governam o repasse.
- *Visão microeconômica*: o repasse é incompleto por poder de mercado; cresce com a diferenciação do produto e cai com a elasticidade do custo marginal (Goldberg & Knetter, 1997; Yang, 1997).
- *Três estágios* (Souza & Silva, 2018): ajuste de markup das empresas → transmissão aos preços, ampliada pela abertura e pela participação de importados na cesta → reajustes salariais posteriores, **menores se ocorrerem em recessão**. Este último elo é o que sustenta a explicação do resultado principal.
- *Visão macroeconômica*: inflação baixa e estável reduz o poder de precificação e, com ele, o repasse (Taylor, 2000; Gagnon & Ihrig, 2004).
- *Câmbio como amortecedor*: o efeito de choques de commodities sobre a inflação é mais intenso em simulações sem a taxa de câmbio (Stockl et al., 2017).
- Fonseca et al. (2019): a situação de câmbio baixo e juro alto seria a de coeficientes de repasse mais elevados.

**Leitura do período (seção 3):** de 2002 a 2012 a política monetária não acompanhou a queda do risco-país; o diferencial de juros abriu espaço para arbitragem de baixo risco, que apreciou o real e acumulou reservas, e a apreciação levou a inflação às metas. O câmbio apreciado baixava o preço de matérias-primas e de bens finais importados (e dos nacionais concorrentes) e os preços administrados reajustados pelo IGP-M, "fortemente influenciado pelo dólar". Depois de 2012, o fim do quantitative easing, a crise política e econômica e a pandemia explicam a depreciação e a inflação mais alta.

**Estratégia empírica (seção 4):**
- VAR mensal de outubro de 2002 a novembro de 2021, cinco variáveis em logaritmo: IPCA (índice), câmbio R$/US$ comercial (venda, média), Selic over acumulada no mês, PIB mensal deflacionado pelo IGP-DI (proxy de demanda) e o índice global de commodities do FMI (proxy de oferta).
- Identificação por Cholesky, com as variáveis em "ordem decrescente de endogeneidade" IPCA, câmbio, Selic, PIB, ICOM: o IPCA é a variável mais endógena e o índice de commodities a menos. As restrições são os zeros da matriz de relações contemporâneas (eq. 5).
- A data de quebra vem do teste multivariado de Bai e Perron (1998): julho de 2011, que separa o período de câmbio com tendência à apreciação (outubro de 2002 a julho de 2011) do de tendência à depreciação (agosto de 2011 a novembro de 2021).
- Séries I(1) pelos testes DF-GLS, Phillips-Perron e ADF (Tabelas A1 e A2), sem cointegração pelo teste de máximo autovalor, portanto VAR em primeira diferença e não VEC. Defasagens por LR, AIC, HQ e SC com ausência de autocorrelação (Breusch-Godfrey): VAR (4) no período completo e VAR (2) em cada subperíodo.
- Respostas a impulso de um desvio-padrão lidas como elasticidades, 12 passos à frente para o choque cambial e 24 no apêndice.

**O que carrega o resultado:** a separação da amostra numa única data, que faz cada subperíodo coincidir com uma direção de câmbio; e a hipótese de que a direção do câmbio é a diferença relevante entre os dois subperíodos. A explicação pela demanda depende de as depreciações brasileiras coincidirem com recessão; numa depreciação com demanda forte, o argumento prevê repasse maior, não menor.

## Main results / findings

- **Período completo**: o choque cambial eleva o IPCA, confirmando o canal; o efeito atinge o máximo e se dissipa por volta do sexto mês (Figura 3).
- **Subperíodos**: o repasse é maior, "mais efetivo e persistente" no período de câmbio com tendência à apreciação do que no de depreciação (Figura 4). Os autores dizem que a decomposição da variância reforça a importância relativa do câmbio no período de apreciação, mas não a apresentam.
- **Correlações de Pearson**: câmbio e IPCA têm correlação de 0,49 no período de depreciação e de 0,08 no de apreciação; Selic e IPCA, de –0,83 na apreciação e de –0,52 na depreciação. Os autores leem os números como indício de que o padrão cambial altera o repasse e a transmissão da política monetária. Note-se que a correlação câmbio-IPCA é maior justamente no período em que o VAR acha repasse menor (ver Limitations).
- **Política monetária por subperíodo** (Figuras A2 e A3): com câmbio em depreciação, a Selic responde mais a um choque no IPCA e a inflação converge mais devagar após um choque na Selic — mais esforço de política para menos resultado.
- **Price puzzle**: o IPCA sobe após um choque na Selic nos três modelos, embora o índice de commodities esteja no VAR. Os autores o leem como canal de custos: a alta de juros encarece a produção e é repassada aos preços de imediato, e só depois o desaquecimento da demanda derruba a inflação. Mais do que o sinal, destacam a baixa sensibilidade da inflação aos juros, sobretudo com câmbio em depreciação.
- **Utilização da capacidade** (Figura 5): os períodos de depreciação são também de NUCI mais baixa, o que os autores usam para justificar o repasse menor na depreciação.

## Limitations and caveats

- *Dos autores*: a pandemia (inflação baixa, Selic baixa e câmbio depreciado ao mesmo tempo) pede um modelo específico; a inflação de oferta precisa ser explorada mais a fundo.
- *Correlação contra VAR*: o texto diz que o resultado do VAR "corrobora as evidências sugeridas pela análise preliminar das séries por meio de correlações de Pearson", mas a correlação câmbio-IPCA é maior no período de depreciação (0,49) do que no de apreciação (0,08), o oposto do resultado do VAR. O texto não reconcilia os dois.
- *Tempo contra direção do câmbio*: com uma única quebra, "câmbio em apreciação" é também 2002–2011 e "câmbio em depreciação" é 2011–2021. A seção 3 atribui o segundo período a fatores externos e a crises; a comparação não isola a direção do câmbio de tudo o mais que mudou entre os dois períodos. A não linearidade não é estimada como dependente de estado (limiar ou regime), só como quebra.
- *Resultados não apresentados*: a decomposição da variância e os testes de estabilidade "podem ser solicitados aos autores" (notas 4 e 5). Nenhuma resposta a impulso é dada em número: as afirmações sobre tamanho e persistência vêm só das figuras.
- *Identificação*: o texto usa Cholesky e, na seção 5, descreve as respostas como "choques não ortogonais de um desvio padrão" — as duas coisas não se conciliam no texto.
- *Teste de quebra*: o texto diz que "não se pode rejeitar a hipótese nula de uma quebra estrutural", enquanto as notas da Figura 2 dão as estatísticas como significativas a 1% (supW = 53,28; W = 17,08 para julho de 2011). A formulação da hipótese nula está invertida ou confusa; o que as notas sustentam é evidência de quebra.
- *Raiz unitária*: o ICOM no período completo e o PIB no período de apreciação têm resultado inconclusivo (Tabela A1) e entram diferenciados mesmo assim.
- *Inconsistência numérica*: a seção 3 diz que a inflação "fechou 2021 em 10,6% a.a.", enquanto a Tabela 1 dá 10,06.
- *Texto danificado*: as equações (1) a (4) e a matriz de relações contemporâneas (5) estão reduzidas a símbolos soltos; as Figuras 1 a 5 e A1 a A3 sobrevivem só como rótulos e marcas de eixo; a Tabela 1 está desmontada em um valor por linha (2003 e 2004 com duas resoluções cada); na Tabela A2, a estatística ADF do câmbio no período completo aparece sem sinal negativo.
- *Nome do arquivo*: o arquivo atribui o trabalho a Cortapasso, que é o terceiro autor; a primeira autora é Eliane Araújo.

## Connections

- [[exchange_rate_pass_through]] — repasse brasileiro de 2002 a 2021 medido por VAR, maior e mais persistente com câmbio em tendência à apreciação do que em depreciação; explicação pela demanda fraca nas depreciações
- [[inflation_targeting]] — o regime de metas brasileiro descrito como dependente do canal cambial, mais eficaz com juros altos e câmbio apreciado, e os custos dessa combinação
- [[monetary_policy_shocks]] — choque na Selic identificado por Cholesky produz price puzzle mesmo com o índice de commodities no VAR, lido como canal de custos
- cost_channel (proposed) — alta de juros encarece a produção e é repassada aos preços antes de a demanda desaquecer; explicação proposta para o price puzzle brasileiro
- depreciation_pass_through (Belaisch, 2003) — estimativa anterior do repasse brasileiro por VAR em 1999–2002, citada como parte da literatura que mede o coeficiente; este artigo estende a amostra e pergunta se o coeficiente muda com a direção do câmbio
- depreciation_pass_through (Goldfajn, 2000) — o repasse que cai em recessão (procíclico) é o mesmo argumento que aqui explica o repasse menor nas depreciações brasileiras
- [[monetary_policy/synthesis/it_credibility_fx_volatility (Minella et al., 2003)]] — citado como medida do repasse no início do regime de metas; lá o repasse cai depois da flutuação de 1999, aqui ele depende da direção do câmbio
- kinea_fx_mental_models — 3.5: apreciação do real e commodities em reais como motor da desinflação, o canal que este artigo encontra mais forte em períodos de apreciação
