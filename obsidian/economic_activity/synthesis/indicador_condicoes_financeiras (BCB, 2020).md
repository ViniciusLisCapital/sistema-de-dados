---
aliases: ["BCB 2020 - Indicador de Condições Financeiras"]
---

# Indicador de Condições Financeiras — Banco Central do Brasil 2020

**Type:** report (boxe)
**Tags:** #condicoes-financeiras #icf #indicador-antecedente #atividade #previsao
**Source:** Banco Central do Brasil, Relatório de Inflação, Março 2020, pp. 69–71 (resultados do estudo em andamento "A new Financial Conditions Indicator for Brazil using daily data", de Wagner Piazza Gaglianone e Fernando Nascimento de Oliveira)
**Language:** Portuguese
**Source file:** [[economic_activity/clean_md/indicador_condicoes_financeiras (BCB, 2020)]]

---

## Context and motivation

As decisões de oferta e demanda dependem não só da taxa básica, mas de outras variáveis financeiras — preços de ativos, spreads, risco, câmbio —, de modo que a Selic sozinha não descreve as condições financeiras da economia. Depois da crise de 2008 os indicadores de condições financeiras (ICFs) se multiplicaram na literatura e nos bancos centrais. O boxe propõe um ICF diário para o Brasil, construído com o critério explícito de informar sobre a atividade futura, aperfeiçoando o indicador mensal de Gaglianone e Areosa (2016).

## Core argument / thesis

Um índice diário que resume juros domésticos e externos, risco, moedas, petróleo, commodities e bolsas, ponderado pela capacidade de cada grupo de antecipar o IBC-Br, mede as condições financeiras melhor do que a taxa de juros e antecipa a atividade melhor do que qualquer variável financeira isolada. Ele acompanha a Selic, mas tem movimentos próprios — vindos sobretudo do prêmio de juros longo, do câmbio e do risco —, e esses movimentos são justamente a informação que a taxa básica não carrega.

## Key mechanisms / model

- **Construção** (Tabela 1): sete grupos — Juros Brasil (swap pré-DI de 1 e 5 anos), Juros exterior (EUA, Reino Unido, Alemanha e Japão), Risco (CDS Brasil de 5 anos e VIX), Moedas (índices do dólar e R$/US$), Petróleo, Commodities (CRB) e Mercado de capitais (MSCI e Ibovespa). Etapas: remoção de tendência dos grupos 4 a 7; padronização; primeira componente principal de cada grupo; média ponderada; nova padronização (z-score), de modo que o ICF mede condições em relação ao padrão histórico da amostra. Alta do ICF = condições mais restritivas.
- **Pesos com critério preditivo**: vêm de regressões da variação em seis meses do IBC-Br sobre as componentes principais dos grupos, com intercepto e dummy para a crise de 2008 (nota 8). Juros Brasil (0,34) e Juros exterior (0,33) têm os maiores pesos; Commodities e Mercado de capitais entram com sinal negativo (-0,13 e -0,15), porque alta desses preços afrouxa as condições. Os pesos dão às variáveis externas mais peso relativo do que no indicador anterior.
- **Decomposição**: a separação em grupos permite atribuir cada movimento do ICF a suas fontes.
- **Teste preditivo** (equação 1): projeção direta, mensal, do crescimento acumulado do log do IBC-Br dessazonalizado em h meses sobre a variação passada da atividade, a variação de um indicador financeiro e a dummy de 2008, nos moldes de Hatzius et al. (2010); comparação de REQM com teste de Diebold e Mariano.
- **Premissa que carrega o resultado**: que a relação estimada entre grupos financeiros e atividade futura é estável — os pesos são escolhidos dentro da amostra para prever o IBC-Br; se a relação mudar, os pesos deixam de resumir as condições relevantes.

## Main results / findings

- O ICF segue os grandes movimentos da Selic, mas se move sozinho: entre julho de 2015 e outubro de 2016, com a Selic estável, subiu em agosto–setembro de 2015 e reverteu entre fevereiro e abril de 2016 (Juros Brasil, Moedas e Risco); entre março de 2018 e julho de 2019, também com Selic estável, teve rápida subida e reversão (Juros Brasil, Moedas, Mercado de capitais e Petróleo).
- No início de 2020 o ICF atingiu mínimos históricos — política monetária estimulativa no Brasil e nas principais economias, preços de ativos em alta, risco baixo — e depois subiu com o estresse do novo coronavírus.
- A relação câmbio–risco, historicamente positiva em momentos de incerteza, se inverteu em 2019 (risco em queda com depreciação); por isso o ICF sem o grupo Moedas mostra condições mais favoráveis de meados de 2019 ao fim da amostra.
- Previsão (Tabela 2): o modelo com o ICF completo tem o menor REQM em todos os horizontes (3, 6, 9 e 12 meses). Em 12 meses, REQM de 0,19 contra 0,70 do modelo com o Ibovespa — redução de 73%, significativa a 1%. Taxas de juros reais de 1 e 5 anos e a inclinação da curva real preveem muito pior em todos os horizontes; excluir o grupo Moedas piora a previsão a partir de 6 meses.
- O texto afirma que testes de Granger "não rejeitam a hipótese nula, aos níveis usuais de significância, de que a dinâmica do ICF proposto antecede temporalmente variações" do IBC-Br — redação que, lida ao pé da letra, não estabelece precedência; a evidência preditiva que sustenta o argumento é a da Tabela 2.

## Limitations and caveats

- É resultado de estudo em andamento, apresentado em boxe: não traz a amostra exata das regressões de peso nem das projeções, nem se a avaliação de previsão é fora da amostra.
- Os pesos são estimados para prever o IBC-Br na mesma amostra; o ganho de previsão pode refletir esse ajuste, e mudanças na relação entre câmbio e risco (como a de 2019) alteram a leitura do índice.
- O z-score mede condições em relação à média histórica da amostra; o nível "neutro" do índice não é uma referência estrutural.
- Texto danificado: os Gráficos 1 a 3 chegaram apenas como rótulos e escalas embaralhados, sem dados; na equação (1) e na sua descrição, os subscritos t caíram em linhas separadas; a nota de rodapé referida após a definição do resíduo não está no arquivo.

## Connections

- [[financial_conditions_index]] — o boxe define, constrói e testa como indicador antecedente um ICF diário para o Brasil
- [[economic_activity/synthesis/ibcbr_vs_pib_metodologia (BCB, 2018)]] — o ICF é calibrado e avaliado contra o IBC-Br, cuja relação com o PIB o outro boxe descreve
