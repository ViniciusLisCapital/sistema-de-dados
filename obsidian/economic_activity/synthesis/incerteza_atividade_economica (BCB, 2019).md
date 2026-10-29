---
aliases: ["BCB 2019 - Incerteza e atividade econômica"]
---

# Incerteza e atividade econômica — Banco Central do Brasil 2019

**Type:** report (boxe / estudo especial)
**Tags:** #incerteza #atividade #curva-is #investimento #painel
**Source:** Estudo Especial nº 65/2019 – Divulgado originalmente como boxe do Relatório de Inflação (setembro/2019)
**Language:** Portuguese
**Source file:** [[economic_activity/clean_md/incerteza_atividade_economica (BCB, 2019)]]

---

## Context and motivation

A literatura trata a incerteza como determinante relevante da atividade: em ambiente incerto, consumo, investimento e contratações são adiados e a alocação de recursos piora. Os índices de incerteza de política econômica de Baker et al. (2016), construídos para vários países (inclusive o Brasil), tornaram a relação mensurável. O boxe pergunta se, controlando pelos determinantes usuais da demanda, a incerteza explica o ciclo do PIB, da FBCF, do consumo privado e do desemprego — e se a incerteza global tem papel próprio.

## Core argument / thesis

A incerteza é um determinante do hiato de atividade que se soma aos juros reais e à demanda externa numa curva IS: uma alta da incerteza reduz o componente cíclico do produto, e reduz mais o do investimento, porque decisões de investimento são mais irreversíveis e mais dependentes de expectativas. Parte relevante desse efeito vem de um fator comum entre países (incerteza global), cujos efeitos são persistentes. Implicação para o ciclo: períodos de maior incerteza tendem a produzir recuperações mais lentas.

## Key mechanisms / model

- **Especificação**: uma curva IS em painel — o componente cíclico de cada medida de atividade depende da própria defasagem, do desvio dos juros reais em relação ao juro real de equilíbrio, do hiato do produto mundial e do indicador de incerteza de política econômica (equação 1).
- **Construção das variáveis**: juro real = juro nominal de curto prazo menos a inflação realizada dos quatro trimestres seguintes; juro de equilíbrio e tendências das medidas de atividade pelo filtro passa-banda de Christiano e Fitzgerald (limites 6 e 32); hiato mundial como combinação de hiatos de países que somam cerca de 92% do PIB mundial; incerteza como desvio percentual em relação à própria média.
- **Estimação**: Arellano–Bover/Blundell–Bond para painéis dinâmicos, com instrumentos limitados ao número de países; o texto avisa que a endogeneidade "pode não ser completamente resolvida".
- **Canais pelos quais a incerteza atua** (da literatura, via Forbes 2016): (i) investimento e capacidade produtiva caem, sobretudo o irreversível, a construção e os setores exportadores; (ii) consumidores elevam a poupança precaucionária, com efeito maior sobre duráveis; (iii) cai a eficiência alocativa e com ela a produtividade (firmas produtivas crescem menos, entrada e saída são adiadas, cadeias de suprimento encurtam); (iv) firmas contratam, treinam e reajustam salários menos, e trabalhadores mudam menos de emprego.
- **Incerteza global**: o indicador é decomposto em um fator comum ao painel e um fator específico de cada país, e a equação é reestimada com os dois.
- **Premissas que carregam o resultado**: que os instrumentos defasados tratam a causalidade reversa (atividade fraca gerando incerteza), e que o coeficiente médio do painel vale para cada país — o texto adverte que um país em particular pode ter magnitudes próprias.

## Main results / findings

- Todos os coeficientes são significativos e com os sinais esperados (Tabela 1): mais juro real acima do equilíbrio reduz o hiato; mais hiato mundial o eleva; mais incerteza o reduz; no desemprego os sinais se invertem.
- A ordem dos efeitos é o ponto: com amostra comum de 17 países, um desvio-padrão de incerteza reduz o hiato da FBCF em 0,61 p.p., contra 0,28 p.p. no consumo privado e 0,18 p.p. no PIB (Tabela 1, coluna β4 x σinc). O investimento também é o mais sensível aos juros reais e ao hiato mundial.
- As respostas a um choque temporário de um desvio-padrão (Gráfico 1) são maiores para a FBCF do que para consumo e PIB, todas diferentes de zero a 90% de confiança.
- A incerteza global tem papel relevante e efeitos que "podem persistir por longos períodos de tempo" (Gráfico 2).
- O efeito no desemprego é fraco: os coeficientes de juros e de incerteza são significativos apenas a 10% (Tabela 1).

## Limitations and caveats

- Os próprios autores: a endogeneidade pode não estar resolvida, o que pede "cautela nas interpretações de causalidade"; as respostas são as do painel conjunto, e um país específico pode diferir.
- Nem todos os países têm todas as variáveis para toda a amostra (trimestral, primeiro trimestre de 1998 ao primeiro de 2019); a regressão do PIB com 23 países não é diretamente comparável às demais, por isso há a linha de amostra reduzida.
- O índice usado é o de incerteza de *política econômica* (base em notícias); o texto cita o IIE-Br da FGV como alternativa para o Brasil, mas não o usa. Não há resultado específico para o Brasil.
- A recuperação mais lenta em períodos de incerteza é afirmada nas considerações finais, sem um exercício próprio que a teste.
- Texto danificado: a equação (1) perdeu os símbolos na extração (sobra "(1)" e a descrição das variáveis com os nomes dos termos em branco); os nomes dos coeficientes no texto (β1 a β4) também sumiram, e só se recuperam pelo cabeçalho da Tabela 1, cujas colunas estão embaralhadas mas legíveis; os Gráficos 1 e 2 têm apenas rótulos de eixo; as notas 16 a 18, referidas no texto (fator comum, choque global e modelos do BCB), não estão no arquivo.

## Connections

- [[economic_uncertainty]] — o boxe mede o efeito da incerteza de política econômica sobre o hiato do PIB, da FBCF, do consumo e do desemprego e lista os canais
