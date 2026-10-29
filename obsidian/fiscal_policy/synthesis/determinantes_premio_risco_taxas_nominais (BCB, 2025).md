---
aliases: ["BCB 2025 - Determinantes do prêmio de risco nas taxas nominais"]
---

# Determinantes do prêmio de risco nas taxas nominais brasileiras — Banco Central do Brasil 2025

**Type:** report (boxe)
**Tags:** #premio-a-termo #curva-de-juros #modelo-acm #divida-publica #juros-externos #brasil
**Source:** Banco Central do Brasil, Relatório de Política Monetária, junho de 2025 (boxe, p. 69–73)
**Language:** Portuguese
**Source file:** [[fiscal_policy/clean_md/determinantes_premio_risco_taxas_nominais (BCB, 2025)]]

---

## Context and motivation

Um boxe anterior (Relatório de Inflação de dezembro de 2022) decompôs as taxas nominais longas brasileiras em expectativa de juros futuros e prêmio de risco (prêmio a termo) pelo modelo de Adrian, Crump e Moench (ACM), e mostrou que a maior parte da volatilidade das taxas longas vem do prêmio, não da trajetória esperada da Selic. Este boxe pergunta o que move esse prêmio: fatores domésticos (juros, inflação, fiscal) ou externos (juros americanos, dólar, aversão a risco).

## Core argument / thesis

O prêmio de risco da taxa nominal de 5 anos responde a fatores domésticos e externos ao mesmo tempo. Na especificação preferida, ele sobe com a Selic, a TLP, a expectativa de inflação Focus e a dívida bruta/PIB, e com a taxa real americana, a inclinação da curva americana, o dólar e o VIX. Na decomposição ao longo do tempo, o fator juros domésticos é o mais importante na maior parte da amostra, seguido de inflação, fiscal e externo; já para um choque de um desvio-padrão, os juros americanos são os que mais movem o prêmio.

## Key mechanisms / model

- **Variável dependente.** Média mensal do prêmio diário de 5 anos estimado pelo ACM sobre a curva nominal de títulos públicos (LTN e NTN-F) interpolada por Svensson (1995), janeiro de 2007 a abril de 2025. O prazo de 5 anos é escolhido porque títulos mais longos não tinham liquidez no início da amostra; os prêmios de diferentes prazos são altamente correlacionados (nota 1).
- **Por que o prêmio, e não a expectativa.** O coeficiente de variação da expectativa da taxa nominal é 0,08 e o do prêmio, 1,11 (nota 2): quase toda a volatilidade da taxa vem do prêmio.
- **Regressões em forma reduzida por MQO**, com erros Newey-West, e todos os regressores defasados um mês para mitigar endogeneidade. Grupos: inflação efetiva e esperada, juros domésticos, juros americanos, fiscal (primário, dívida bruta e líquida), atividade (hiato por filtro HP sobre o IBC-Br), bolsas, câmbio, commodities e VIX. Taxas prefixadas em reais ficam de fora porque foram usadas para gerar o próprio prêmio. Sete especificações, escolhidas por significância e pelo critério de Schwarz; a Regressão 7 é a de melhor ajuste.
- **Como ler os canais.** O texto não formaliza mecanismos: os sinais são associações condicionais. A TLP entra como o custo dos financiamentos de longo prazo do BNDES; a dívida bruta/PIB como o indicador fiscal; juros americanos (nível real e inclinação), dólar e VIX como canal externo.

## Main results / findings

- **Ajuste:** o R² ajustado vai de 0,75 na Regressão 1 a 0,84 nas Regressões 5 a 7 (Tabela 1, 220 observações).
- **Inflação:** com a expectativa Focus no modelo, o IPCA corrente perde significância; os componentes do IPCA não são significativos (nota 5). O prêmio responde à inflação esperada, não à corrente.
- **Fiscal — sinal instável:** a dívida bruta/PIB entra com sinal negativo na Regressão 1, perde significância nas Regressões 2 e 3 e só volta significativa, com sinal positivo, nas Regressões 6 e 7 (Tabela 1). O resultado preferido (prêmio positivamente associado à dívida) é robusto à troca pela dívida líquida (nota 7), mas não é estável entre especificações. O resultado primário não é significativo.
- **Externo:** taxa real americana de 5 anos (TIPS) e inclinação 10 anos menos 2 anos significativas em todas as especificações em que entram; trocar a taxa nominal americana pela real não altera o coeficiente. O dólar perde e recupera significância conforme a especificação.
- **Tamanho relativo (Tabela 2, choque de 1 desvio-padrão, Regressão 7):** os maiores efeitos são da TIPS de 5 anos (0,732 p.p.) e da inclinação americana (0,693), seguidos da Selic (0,522), da dívida bruta/PIB (0,301) e da TLP (0,236).
- **Decomposição temporal (Gráfico 2):** juros domésticos dominam a maior parte da série, sobretudo até 2016 e de novo a partir de 2022; inflação ganha peso a partir de 2014 e perde após 2017; o fiscal, inicialmente o menor, cresce a partir de 2016; o externo é volátil, com pico na crise de 2008 e altas em 2013–2016 e no período recente.
- **O que não se encaixa:** na Tabela 2, Focus e dólar, ambos significativos na Regressão 7, aparecem com efeitos de 0,005 e 0,001 p.p. por desvio-padrão, muito menores que os demais; o texto não comenta essa discrepância entre coeficiente e efeito por desvio.

## Limitations and caveats

- Regressões em forma reduzida: associações condicionais com regressores defasados, não efeitos causais; a especificação final resulta de busca entre sete modelos, o que favorece o ajuste dentro da amostra.
- O prêmio é ele próprio estimado por um modelo (ACM), sobre uma curva interpolada; erros de estimação do prêmio entram na variável dependente.
- Selic e expectativa de inflação são também determinantes da parte "expectativa" da taxa; o boxe não discute por que elas explicam o prêmio, nem a direção de causalidade entre prêmio e política monetária.
- A conclusão sobre o fiscal depende da especificação (sinal negativo, não significativo e positivo em diferentes regressões).
- **Passagens danificadas:** a equação (1) do modelo em forma reduzida não está no arquivo — só a lista de símbolos sem os símbolos; os Gráficos 1 e 2 chegaram como eixos e rótulos, sem valores legíveis; na Tabela 1, linhas com menos coeficientes que colunas (IPCA, TLP, RES_PRIMARIO, IBC-BR, IBOV, CRB etc.) não permitem saber com segurança em qual regressão cada coeficiente entra, exceto onde o texto o diz.

## Connections

- [[term_premium]] — o boxe explica os determinantes do prêmio a termo da curva nominal brasileira estimado pelo ACM: juros domésticos, expectativa de inflação, dívida bruta e juros americanos
- [[monetary_policy/synthesis/term_structure_linear_regressions (Adrian, Crump & Moench, 2013)]] — o modelo ACM que gera a variável dependente, aplicado à curva de LTN e NTN-F
