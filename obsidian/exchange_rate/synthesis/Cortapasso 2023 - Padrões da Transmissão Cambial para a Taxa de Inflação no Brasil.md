# Cortapasso 2023 — Padrões da Transmissão Cambial para a Taxa de Inflação no Brasil

**Type:** Artigo empírico (VAR)
**Tags:** #repasse-cambial #brasil #var #ipca #assimetria #metas-de-inflacao #selic
**Source:** J.P. Cortapasso, 2023
**Language:** Portuguese
**Raw file:** [[padrao_trasmissao_cambial (Cortapasso, J.P., 2023)]]

---

## Context and motivation

Atualiza a literatura de repasse cambial brasileiro (que vai de Goldfajn e Werlang 2000 e Belaisch 2003 até estudos mais recentes) estendendo a amostra até 2002–2021 — cobrindo múltiplos ciclos cambiais completos (depreciação 2002, apreciação 2003–2012, depreciação pós-2012) que os estudos anteriores, restritos a janelas mais curtas, não conseguiam captar. A contribuição central declarada é reconhecer que o coeficiente de repasse cambial (ERPT) pode variar sistematicamente entre momentos de tendência de apreciação e de depreciação — não é um parâmetro fixo ao longo do regime de metas de inflação.

## Core argument / thesis

Sob o Regime de Metas de Inflação (RMI, desde 1999), o câmbio segue sendo o mecanismo dominante de controle de preços no Brasil — mas de forma assimétrica: a dependência do câmbio como âncora de preços é mais acentuada em momentos de tendência à apreciação do que em momentos de depreciação. Isso implica que a política econômica brasileira usa a apreciação cambial (via diferencial de juros/arbitragem) como instrumento de desinflação além do seu papel "natural" de ajuste de preços relativos — levantando a questão normativa de até que ponto essa dependência é desejável.

## Key mechanisms / model

- **Repasse cambial em três estágios** (Souza e Silva, 2018, citado): (1) impacto inicial nas empresas via ajuste de markup sobre insumos importados; (2) transmissão amplificada pelo grau de abertura e participação de importados na cesta de consumo; (3) efeito pós-repasse via reajustes salariais, atenuados em cenários de recessão — mesma lógica de primeiro/segundo estágio (first-round/second-round) documentada em [[exchange_rate_pass_through]].
- **Canais direto e indireto** (Laflèche 1997; Assis et al. 2019): direto = encarecimento de insumos importados repassado ao custo de produção; indireto = depreciação eleva exportações → maior demanda por trabalho → reajuste salarial repassado a preços. Andrés e Santiago (2016): a depreciação eleva preços de tradables relativo a non-tradables — grau de abertura e proporção tradables/non-tradables são determinantes-chave, mesma lógica de [[Belaisch 2003 - Exchange Rate Pass-Through in Brazil]].
- **Visão microeconômica clássica** (Goldberg e Knetter 1997; Yang 1997): repasse incompleto explicado pela Lei do Preço Único e PPC como limites teóricos, mas o repasse efetivo depende do poder de mercado — maior para produtos diferenciados, menor quanto mais elástico o custo marginal (pricing-to-market, mesmo mecanismo do capítulo de Krugman em [[Krugman 2023 - Output and the Exchange Rate in the Short Run]]).
- **Visão macroeconômica — declínio do repasse com credibilidade monetária**: a literatura internacional (Taylor 2000; Gagnon e Ihrig 2004) e brasileira (Santolin e Carvalho 2019, que estimam repasse 1999–2017 e confirmam queda acentuada após 2009) associam o declínio do coeficiente de repasse à consolidação de regimes de metas de inflação críveis — reduz-se o poder de precificação das empresas porque a expectativa de reversão (via política monetária) fica mais forte.
- **Assimetria câmbio apreciado/depreciado como hipótese central**: Fonseca et al. (2019, citado) argumentam que a combinação câmbio baixo + juro alto seria potencialmente mais eficiente para gerar coeficientes de repasse mais elevados — reforçando o papel do câmbio como mecanismo de transmissão monetária justamente quando ele está em trajetória de apreciação. Mendonça e Tostes (2015): política fiscal e credibilidade monetária também explicam o tamanho do repasse cambial no Brasil (interação com [[fiscal_dominance]] e [[risk_premium]]).
- **Narrativa histórica 1999–2021** (Tabela 1, IPCA/Selic/variação cambial/PIB ano a ano): float de 1999 (fuga de capitais, reservas caem de USD 74bi para USD 30bi em 9 meses, depreciação de 56% no ano); depreciação de 2002 (incerteza eleitoral, "Carta aos Brasileiros"); apreciação 2003–2012 (juro doméstico alto vs. risco-país em queda → arbitragem de juros pressiona apreciação e acumulação de reservas, ancorando o IPCA); reversão pós-2012 (fim do QE nos EUA, crise política do 2º governo Dilma, recessão 2015–16 com queda acumulada de ~7% do PIB, Covid, choque de commodities/cadeias de valor 2021 fechando o ano em 10,6% de IPCA).

## Main results / findings

- **Padrão histórico direto**: anos com câmbio mais depreciado (2002, 2015, 2021) coincidem com os maiores IPCA do período (incluindo dois dígitos); anos com câmbio relativamente apreciado (2005–2014) coincidem com IPCA mais baixo e mais próximo da meta — suporte descritivo direto para a dependência do câmbio como âncora de preços sob o RMI.
- O resultado central do artigo (conforme abstract) é a "dependência exacerbada do câmbio como mecanismo de controle de preços no Brasil, em especial em momentos de câmbio com tendência à apreciação" — implicando que a política de juros brasileira usa a apreciação cambial induzida por arbitragem como um canal de desinflação adicional, motivando uma avaliação mais ampla do papel dessa política além do controle de preços em si.

## Limitations and caveats

- **Esta extração está incompleta**: o texto bruto disponível termina no meio da Seção 4.1 (estratégia empírica/especificação do VAR), antes da apresentação dos resultados quantitativos do modelo — os coeficientes de repasse por regime (apreciação vs. depreciação), a especificação exata do VAR, testes de quebra estrutural e a seção de conclusão não estão presentes nesta fonte. Não citar valores numéricos específicos de repasse deste artigo sem acessar o texto completo.
- A tabela histórica (1999–2021) é descritiva, não um teste estatístico formal da assimetria — a correlação visual entre anos de câmbio depreciado e IPCA alto é sugestiva mas não substitui as estimativas do VAR (ausentes nesta extração).

## Connections

- [[exchange_rate_pass_through]] — mecanismo de repasse em três estágios e canais direto/indireto, complementando a base teórica já existente com a literatura brasileira mais recente (2016–2021)
- [[Goldfajn and Werlang 2000 - The Pass-through from Depreciation to Inflation]] e [[Belaisch 2003 - Exchange Rate Pass-Through in Brazil]] — este artigo estende a janela de 1980–2002 (Goldfajn/Belaisch) até 2021, cobrindo o ciclo completo de apreciação 2003–2012 e a reversão pós-2012 que aquelas fontes não alcançam
- [[risk_premium]] / [[balance_of_payments_approach]] — a apreciação 2003–2012 é descrita exatamente como um caso de arbitragem de juros (carry) viabilizada pela queda do risco-país, mesmo mecanismo de "risk premium falling → carry inflow → appreciation" já documentado nesses conceitos
- [[fiscal_dominance]] — Mendonça e Tostes (2015, citado) já apontam a interação entre credibilidade fiscal e o tamanho do repasse cambial no Brasil, prefigurando o mecanismo formalizado em [[Itaú 2025 - Fiscal Dominance in Brazil]]
- [[currency_crisis_indicators]] — a crise cambial de 1999 (fuga de capitais, queda de reservas de USD74bi para USD30bi em meses, ataque especulativo) é um caso brasileiro direto dos indicadores de crise documentados nesse concept
