---
aliases: ["Alves 2013 - Preços Administrados: projeção e repasse cambial"]
---

# Preços Administrados: projeção e repasse cambial — Alves, Figueiredo, Nascimento Junior & Perez 2013

**Type:** paper (Trabalho para Discussão do BCB)
**Tags:** #preços-administrados #previsão-de-inflação #repasse-cambial #ipca #brasil
**Source:** Banco Central do Brasil, Trabalhos para Discussão nº 305, março 2013, p. 1-37
**Language:** Portuguese
**Source file:** [[inflation/clean_md/administered_prices_projection_pass_through (Alves et al., 2013)]]

---

## Context and motivation

Os preços administrados (por contrato ou monitorados) são fixados por contrato, órgão público ou agência reguladora e respondem pouco às condições de mercado; ainda são cerca de um quarto do IPCA. A nova ponderação do IPCA (POF 2008/2009, em vigor desde janeiro de 2012) e a revisão da lista do BCB reduziram o grupo de 28 para 23 itens e de cerca de 30% para cerca de 24% da cesta. O texto documenta como o BCB passou a projetar esse grupo depois da mudança e reavalia os coeficientes de repasse cambial usados para gasolina, GLP, energia elétrica e telefone fixo — coeficientes que alimentam a trajetória do IPCA cheio nos modelos de projeção do Copom. A amostra termina no fim de 2011 ou início de 2012.

## Core argument / thesis

Como os administrados seguem regras de reajuste conhecidas (contratos de concessão, fórmulas de agências, calendários municipais), a melhor projeção de curto prazo não é econométrica, é **contábil**: reproduzir item a item a regra de reajuste e a metodologia do IBGE. No médio prazo, quando as regras viram hipóteses, combina-se essa contabilidade (para os itens com regra estável) com modelos econométricos do agregado. Quanto ao câmbio, o argumento é que o repasse aos administrados dependia de indexação e de uma política de preços de combustíveis que mudaram: com a Petrobras suavizando preços e os contratos trocando indexadores, a correlação com o câmbio desapareceu e os coeficientes devem ser zerados.

## Key mechanisms / model

**Estratégia em dois horizontes (Seção 2, Figura 1, Tabela 1).**
- Curto prazo (ano corrente): projeção "contábil" por cenários, a partir de contratos, regras de reajuste e da forma como o IBGE incorpora cada reajuste ao índice.
- Médio prazo (dois ou três anos seguintes): duas abordagens. A econométrica modela o agregado dos administrados; a híbrida separa 12 itens modelados contabilmente (14,1% do IPCA) dos demais, modelados econometricamente em bloco (10,4% do IPCA).

**A lógica contábil, item a item (Seção 2.1).** O mecanismo comum é um índice de preços defasado menos um fator de produtividade, aplicado numa data fixa e repassado ao IPCA com um calendário próprio:
- *Derivados de petróleo*: o preço na refinaria é fixado pela Petrobras, que alinha à tendência de longo prazo dos preços internacionais suavizando as flutuações; isso dá ao petróleo menos volatilidade no IPCA do que nos EUA. O preço na bomba soma ainda álcool anidro, margens e tributos (a Cide amorteceu reajustes). Dado o comportamento recente, os reajustes de gasolina e GLP têm sido quase sempre supostos zero no curto prazo.
- *Produtos farmacêuticos*: teto de preços da CMED — IPCA menos fator X (produtividade), mais fatores Y (preços relativos entre setores) e Z (concorrência intra-setor, via participação dos genéricos). Como o reajuste autorizado é negociado e chega com defasagem, aplica-se um coeficiente de repasse de 0,88 e distribui-se o reajuste em três meses (Tabela 2).
- *Energia elétrica*: reajuste anual da Aneel em duas parcelas — Parcela A (custos não gerenciáveis: encargos, transmissão, compra de energia) e Parcela B (custos gerenciáveis, corrigidos pelo IGP-M menos fator X) —, além das revisões periódica e extraordinária. A projeção é feita para cada uma das quinze concessionárias cobertas pelo IPCA.
- *Plano de saúde*: reajuste máximo da ANS em maio, distribuído igualmente ao longo de doze meses; projeta-se pelo IPCA de maio a abril.
- *Ônibus urbano*: reajuste municipal, custo por km sobre passageiros por km, com o diesel como principal custo e as eleições municipais afetando data e magnitude; regra padrão é o IPCA de 12 meses, com sazonalidade de janeiro (Figura 4).
- *Telefone fixo*: desde o fim de 2005 indexado ao IST, índice setorial de custos em que IPCA e IPA-OG de máquinas respondem por 80% (Tabela 4); como o IPA divergia do IST, projeta-se só pelo IPCA.
- *Água e esgoto e itens menores*: mês e índice de reajuste por região inferidos do padrão histórico (Tabela 5), com IPCA, IGP-M ou IGP-DI.

**A lógica econométrica (Seção 2.2).** Modelos trimestrais estimados com amostra de 2003 a 2011, sobre séries retroagidas para a nova ponderação (método no Anexo). Para o agregado, quatro AR e dois VAR (Tabela 6); para o bloco não contábil, três AR e três VAR (Tabela 7). Os regressores são a inflação dos livres, o IGP-DI, a energia elétrica e, num caso, a inflação importada (PPI em reais). A seleção exige ajuste e significância, respostas a impulso coerentes com a teoria, desempenho fora da amostra contra um AR(1) e "razoabilidade" — projeções sem valores extremos, próximas ao padrão sugerido pelo especialista. Alguns modelos piores no erro fora da amostra são mantidos por carregarem um canal que os outros não têm (o IGP-DI; a inflação externa).

**Repasse cambial (Seção 3).** Para os combustíveis o coeficiente é o produto de dois termos: a parcela do preço na refinaria no preço ao consumidor e a relação entre o preço internacional (em reais) e o preço da Petrobras (equações 6 e 7). Para a energia, soma-se o impacto por concessionária: a fração do reajuste que depende do câmbio (Itaipu cotada em dólar; transmissão e Parcela B via IGP-M), ponderada pelos pesos regionais (Tabela 13). O resultado carrega a hipótese decisiva: **o repasse depende da regra de formação de preço** (política da Petrobras, indexador do contrato), não de uma elasticidade estável.

## Main results / findings

- **Gasolina**: o termo internacional-Petrobras cai de 0,76 (2002-2007) a -0,10 (2006-2011), e o coeficiente de repasse de 0,23 para -0,03 (Tabela 10). Os preços da Petrobras ficam estáveis a partir de 2005. A hipótese de repasse indireto via álcool não se confirma: álcool e gasolina andam juntos, mas o álcool não se relaciona significativamente com o câmbio. Coeficiente zerado.
- **GLP**: de 0,27 a 0,00 na amostra recente (Tabela 12); o preço da Petrobras não mudou do início de 2003 ao fim da amostra, e o que varia ao consumidor são os outros custos. Coeficiente zero.
- **Energia elétrica**: o cálculo por concessionária dá 0,08, menos da metade do anterior 0,18 (Tabela 13), mas os autores o tratam com cautela (o reajuste da receita total e o que chega ao consumidor podem ter sinais opostos; a apropriação de PIS/Cofins e ICMS contamina a série mensal) e zeram o coeficiente.
- **Telefone fixo**: correlações positivas entre câmbio, IST e o item no IPCA, mas regressões sem coeficientes significativos; mantém-se zero.
- **Síntese**: queda "acentuada e generalizada" do repasse nos quatro itens; todos os coeficientes passam a zero. Um novo estudo seria necessário se as regras de indexação mudassem ou se a correlação histórica voltasse.
- **Projeção**: na maioria dos horizontes os modelos selecionados superam o AR(1) simples fora da amostra (Figuras 5 e 6); no agregado, as exceções no médio prazo são o VAR 2 e o AR 4.

## Limitations and caveats

- O repasse nulo é propriedade de um regime de preços, não do câmbio: ele resulta de a Petrobras ter congelado ou suavizado preços e de os contratos terem trocado o IGP pelo IST ou pelo IPCA. Os próprios autores ressalvam que o resultado vale enquanto essas regras valerem. Os coeficientes saem de correlações e de pesos contábeis, não de um modelo estrutural de formação de preço.
- A projeção contábil depende de hipóteses de especialista (reajuste zero de combustíveis, calendários municipais inferidos do passado, o coeficiente de 0,88 dos medicamentos), e o critério de "razoabilidade" na seleção econométrica é julgamento, não teste.
- A amostra econométrica é curta (2003-2011, trimestral) e as séries foram retroagidas para a nova ponderação; o texto não reporta coeficientes estimados dos AR e VAR, só as especificações e o erro relativo.
- Passagens danificadas: as equações (1) a (5) (regras de reajuste de medicamentos e de telefone fixo) não estão no arquivo, só seus números e as definições ao redor; os eixos das Figuras 7 e 8 estão embaralhados (rótulos e meses em texto invertido); os rótulos de colunas da Tabela 13 (concessionárias) estão deslocados para o rodapé da tabela, sem correspondência clara com as colunas; as fórmulas do Anexo (retroação dos pesos) estão espalhadas em várias linhas e com símbolos perdidos.

## Connections

- [[administered_prices]] — o grupo em si: definição operacional do BCB, composição pós-POF 2008/2009 e a regra de reajuste de cada item como base da projeção
- [[exchange_rate_pass_through]] — revisão dos coeficientes de repasse dos administrados mais expostos ao câmbio; o repasse vai a zero quando a política de preços e os indexadores mudam
- [[monetary_policy/synthesis/it_lessons_and_challenges (Minella et al., 2002)]] — lá o repasse dos administrados era mais do que o dobro do dos livres, por preços internacionais e indexação ao IGP; aqui esses canais foram desligados por mudança de regra e os coeficientes zerados
- [[monetary_policy/synthesis/it_credibility_fx_volatility (Minella et al., 2003)]] — a mesma ligação entre câmbio e administrados no período de crise que esta revisão encontra desaparecida em 2006-2011
