# Padrões da transmissão cambial para taxa de inflação no Brasil

## Abstract

This paper analyzes the importance of the exchange rate in the inflation determination under Inflation Targeting in Brazil. Its main contribution is recognizing that the exchange rate pass-through can vary in more or less appreciated exchange rate situations. Thereby, this paper starts from a theoretical analysis of the determinants of exchange rate pass-through, followed by an investigation of the relationship between exchange rate and inflation in Brazil. Finally, the article presents the estimates of a Vector Autoregressive model (VAR) for a Brazilian economy, between 2002 and 2021. The main results of this article indicate the exacerbated dependence of the exchange rate as a mechanism of price control in Brazil, especially in moments of exchange rate with a trend to appreciate. The main implication of this result is the necessity to evaluate the role of this policy beyond price control.

## Resumo

Este artigo analisa a importância da taxa de câmbio na determinação da inflação no Brasil sob o regime de metas para a inflação. Sua principal contribuição é o reconhecimento de que a transmissão cambial para os preços pode variar em situações de câmbio mais ou menos apreciado. Para tanto, parte-se de uma análise teórica sobre os determinantes do repasse cambial, seguida da investigação sobre a relação entre taxa de câmbio e inflação no Brasil. Por fim, o artigo apresenta as estimativas de um modelo de Autorregressão Vetorial (VAR) para a economia brasileira, entre 2002 e 2021. Os principais resultados indicam a dependência exacerbada do câmbio como mecanismo de controle de preços no Brasil, em especial em momentos de câmbio com tendência à apreciação. A principal implicação desse resultado é a necessidade de se avaliar o papel dessa política para além do controle de preços.

## 1 Introdução

Com a liberalização da conta de capitais, promovida pela economia brasileira em meados da década de 1990, e a adoção do regime de câmbio flutuante, em 1999, o canal de transmissão da política monetária via taxa de câmbio tornou-se extremamente relevante para o controle de preços. Desde então, observa-se no Brasil que os anos com taxas de câmbios mais depreciadas – 2002, 2015 e 2021 – também foram os que registraram maiores taxas de inflação, inclusive acima de dois dígitos. Já os anos nos quais a taxa de câmbio manteve-se relativamente apreciada também foram caracterizados por taxas de inflação mais baixas, a exemplo do período entre 2005 e 2014.

A importância do câmbio como mecanismo de transmissão da política monetária tem sido objeto recorrente de investigação na economia brasileira, podendo se destacar autores que tentam calcular o tamanho do coeficiente de repasse cambial no Brasil (Belaisch, 2003; Minella et al., 2003; Carneiro et al., 2004; Minella; Correia, 2005; Ferreira; Matos, 2021); autores que destacam a existência de problemas nos mecanismos de transmissão da política monetária e a consequente sobreutilização do canal do câmbio na busca pela estabilidade de preços (Modenesi; Araújo, 2013; Araújo et al., 2018) e também alguns autores que investigam a existência de não linearidades nos efeitos do câmbio sobre os preços no Brasil (Pimentel et al., 2016; Fonseca et al., 2019).

É nesse contexto que o presente artigo está inserido, buscando entender a importância da taxa de câmbio na determinação da inflação no Brasil. Sua principal contribuição é o reconhecimento de que o repasse cambial (exchange rate pass-through) pode variar em situações de câmbio mais ou menos apreciado, considerando uma amostra de dados que se inicia com a fase inicial da implementação do Regime de Metas de Inflação (RMI) e vai até os últimos valores disponíveis para as séries analisadas.

Para atender ao objetivo proposto este artigo parte de análise teórica sobre os determinantes do repasse cambial, seguida de uma investigação sobre a relação entre taxa de câmbio e inflação no Brasil. Para oferecer evidências empíricas sobre a temática investigada, apresentam-se as estimativas de um modelo de Autorregressão Vetorial (VAR) para a economia Brasileira, entre 2002 e 2021, considerando a possibilidade de quebras estruturais em períodos de tendência à apreciação ou depreciação relativa da taxa de câmbio.

---

## 2 Fundamentos teóricos da relação entre câmbio e inflação

O efeito exchange rate pass-through (ERPT) é definido como a relação entre a variação dos preços nacionais e as variações na taxa de câmbio. Os estudos atinentes ao tema mostram que o repasse cambial afeta a economia como um todo, seja pelas alterações nos preços repassados ao consumidor final ou por meio de canais de investimentos e do volume de comércio do país (Campa; Goldberg, 2005).

A literatura sobre repasse cambial amplificou-se, sobretudo, após a década de 1970, como resultado da maior integração entre os mercados com maior liberalização e regimes cambiais flexíveis, em que as análises micro e macroeconômicas passaram desde então a serem utilizadas, por diversos caminhos, para explorar a dinâmica das variações cambiais e suas implicações, seja sobre o preço de um produto, ou sobre o nível geral de preços de uma determinada economia.

Os estudos especificam que o exchange rate pass-through impacta de forma direta ou indireta a economia quando há uma depreciação cambial. Na sua forma direta, o choque inicial é sentido no aumento dos preços dos insumos importados, que são transmitidos ao consumidor final por meio do encarecimento dos custos de produção, enquanto as consequências indiretas induzem aumento no volume de exportação, ampliando a procura por bens substitutos e elevando a demanda por trabalho, ocasionando incremento salarial que é repassado aos preços finais (Laflèche, 1997; Assis et al., 2019).

Nesse sentido, Andrés e Santiago (2016) acrescentam que, de forma indireta, uma depreciação cambial gera aumento nos preços dos bens tradables em comparação aos non-tradables. Portanto, o grau de abertura de uma economia e a relação entre tradables e non-tradables são fundamentais para o repasse cambial.

Stockl et al. (2017) avaliam os choques nos preços internacionais das commodities e sua influência sobre a inflação brasileira, estimando como as variações dos preços de commodities, no período recente, impactam na dinâmica da inflação ao consumidor no Brasil, assim como nas decisões de política monetária do Banco Central. Os resultados encontrados pelos autores indicam que o efeito líquido do aumento no preço das commodities é positivo sobre a inflação e mostra-se ainda mais intenso em simulações sem a taxa de câmbio. Os autores concluem que a variável câmbio tem a capacidade de absorver choques dos preços de commodities sobre a inflação.

O repasse cambial também pode ser interpretado como a elasticidade do câmbio de acordo com sua incidência nos preços de uma economia, sendo completo quando as alterações cambiais são repassadas aos preços em sua totalidade, e incompleto no caso em que apenas parte das variações cambiais é transmitida aos preços, ou nulo quando não há repercussão nos preços em geral.

Os estudos pioneiros ao tema partem da análise das estruturas de mercado para identificar o grau de repasse cambial para as economias. Pela visão microeconômica, as variações cambiais são repassadas de forma incompleta aos preços, pois o poder de precificação de mercado, sobretudo a Lei do Preço Único (LPU) e a Paridade do Poder de Compra (PPC) é fator que baliza o grau do repasse. Além disso, o determinante de um repasse cambial maior estaria positivamente relacionado com a diferenciação do produto e apresenta conexão negativa com a elasticidade do custo marginal, assim as empresas possuem, em parte, poder acerca do grau do repasse aos preços (Goldberg; Knetter, 1997; Yang, 1997).

Em suma, quando há depreciação cambial, esta passa por três estágios para impactar a economia. Primeiro, quando há depreciação cambial, os impactos iniciais são sentidos pelas empresas, que buscam ajustar seu preço de markup, resultando em aumento dos preços de importados. O segundo estágio está relacionado à transmissão das flutuações cambiais aos preços, potencializada pelo grau de abertura da economia, e quanto maior for o nível de participação de produtos importados na cesta de consumo. Por fim, o terceiro estágio estende-se ao efeito pós-repasse, no qual o aumento dos preços motiva reajustes salariais, que serão menores se ocorridos em cenários de recessão (Souza; Silva, 2018).

O decréscimo no grau do pass-through observado por diversos estudos a partir da década de 1980 é associado às políticas monetárias mais difundidas, sobretudo após a década de 1990 em economias emergentes e desenvolvidas. A hipótese de que um regime no qual a taxa de inflação encontra-se baixa e estável seria o fator mantenedor de um nível de repasse cambial aos preços com menor incidência, por conta da redução do poder de precificação das empresas. Na visão macroeconômica, a diminuição do repasse fundamenta-se em políticas monetárias criadas pelos bancos centrais para estabilizar a inflação. Assim, as variações nos preços domésticos tendem a ser menores diante de um choque cambial conforme as expectativas dos agentes da economia sobre a ação da autoridade monetária (Taylor, 2000; Gagnon; Ihrig, 2004).

Ante o exposto, a questão que se examina é que os repasses cambiais, que têm papel fundamental no controle de preços em modelos centrados em metas nominais de inflação, passaram por modificações em seus padrões ao longo dos anos de 1980 e 1990, em que se observa o decaimento desse repasse ao longo do tempo, com destaque para cenários pós-crises onde a inflação era contida e apresentava-se em baixos níveis. Assim, as economias, tanto desenvolvidas quanto emergentes, passam a observar redução no efeito pass-through em cenários de preços baixos (Jašová et al., 2016).

Não há consenso na literatura acerca de que fatores estariam influenciando essa tendência e se há um padrão para tal, sendo tais repasses diferentes em países desenvolvidos e em desenvolvimento. No caso de economias em desenvolvimento, como a brasileira, investiga-se a relação entre taxa de juros, câmbio e o repasse cambial, conforme destaca Fonseca et al. (2019), sendo que os autores argumentam que podem existir evidências de não linearidades no repasse cambial associadas a períodos de câmbio com tendência à apreciação/depreciação, como colateral dos juros. Os aludidos autores argumentam que a situação câmbio baixo e juro alto seria potencialmente mais eficiente para coeficientes de pass-through mais elevados e, consequentemente, reforça a importância do câmbio como mecanismo de transmissão monetária.

Mendonça e Tostes (2015) apresentaram evidências empíricas sobre os efeitos do repasse cambial para a inflação na economia brasileira após a adoção das metas de inflação. Os resultados indicam que o efeito do repasse cambial é importante para explicar a taxa de inflação, e a principal contribuição deste estudo foi a avaliação do impacto das políticas fiscais e a credibilidade monetária no mecanismo de transmissão da taxa de câmbio para a inflação no Brasil, indicando que ambas as políticas são importantes para explicar o repasse cambial na economia brasileira. Para Assis et al. (2019), economias abertas como o Brasil dependem da influência que a taxa de câmbio exerce sobre os preços para garantir o equilíbrio do regime de metas de inflação. Na visão dos autores, o grau do pass-through de produtos importados depende da moeda, seja a moeda originária do país produtor, do mercado de destino ou de uma moeda que não faz parte das transações entre as duas economias. No Brasil, Santolin e Carvalho (2019) estimam o pass-through entre 1999 a 2017 e confirmam que o coeficiente de repasse cambial diminuiu ao longo do tempo, sobretudo após 2009, quando o impacto sobre o Índice de Preços ao Consumidor Amplo (IPCA) foi reduzido consideravelmente.

O estudo de Arestis et al. (2009), focado em analisar diferentes países emergentes que adotaram o RMI e compará-los com países onde o regime não foi adotado, constata que em ambos os casos houve sucesso no controle da inflação. Mesmo o Brasil apresentando uma das maiores taxas de juros do mundo, ainda ostenta uma inflação média anual elevada, impactando negativamente no crescimento econômico do país e na dívida pública. Os autores destacam que economias abertas da América Latina apresentam certa vulnerabilidade a choques externos, e a volatilidade cambial ocasiona mudanças na taxa de inflação que provoca a inabilidade desses países inseridos no RMI de atingir suas metas, uma das razões pode estar relacionada ao repasse cambial menor ao longo do tempo.

Portanto, o objetivo desta seção foi entender quais os fatores que contribuem para explicar o coeficiente de repasse da taxa de câmbio para os níveis de preços, ressaltando abordagens microeconômicas e macroeconômicas. À luz dessa literatura, a próxima seção vai analisar a relação entre taxa de câmbio e inflação no Brasil, seguida de uma análise empírica sobre o coeficiente de repasse cambial no Brasil. Vale destacar que o principal objetivo empírico da referida seção não é investigar quais os determinantes do coeficiente de repasse como fizeram Gagnon e Ihrig (2004) e Murchison (2009), na perspectiva macroeconômica, ou Goldberg e Knetter (1997) e Yang (1997) na perspectiva microeconômica, mas identificar se sob o regime de metas de inflação no Brasil houve mudanças no tamanho do coeficiente de repasse em momentos de taxa de câmbio apreciada ou depreciada. No entanto, a discussão teórica desta seção é importante para a interpretação dos resultados encontrados.

---

## 3 Economia brasileira e a dinâmica da relação entre taxa de câmbio e preços

Para a economia brasileira o ano de 1999 é caracterizado pelo abandono do regime de metas cambiais e adoção do Regime de Metas de Inflação. Após as crises em diversos países – crise do México em 1994, a crise Asiática em 1997 e a crise Russa em 1998 –, em 1998, o Brasil sofre com ataques especulativos, que tornaram inevitável a mudança do regime cambial para o câmbio flutuante. Segundo os dados do Banco Central do Brasil (BCB, 2022), em 1997, o déficit em transações correntes era de cerca de 5% do Produto Interno Bruto (PIB), o déficit público nominal em torno de 6% do PIB, as reservas cambiais, em abril de 1998, eram de US$74 bilhões e, em 15 de janeiro de 1999, caíram para algo em torno de US$30 bilhões. Os fortes ataques especulativos e a consequente fuga de capitais sofrida pelo Brasil no período em destaque tornam o regime cambial então adotado insustentável. A mudança de regime veio acompanhada de forte depreciação da moeda, com variação média da taxa de câmbio de 56% de 1998 para 1999, conforme a Tabela 1. Um desafio latente para o Plano Real nesse período esteve associado à vulnerabilidade externa desencadeada por um plano de estabilização dos preços associado a fluxos de capitais externos voláteis, os quais garantiam uma "âncora cambial".[^1]

[^1]: Para mais detalhes dessa mudança, ver Barbosa-Filho (2008).

Após se manter em torno de 1,8 R$/US$ nos anos de 1999 e 2000, a taxa de câmbio, agora flutuante, sofre nos anos seguintes novas pressões ligadas às incertezas acerca da eleição presidencial em 2002. Apesar de o então candidato Luiz Inácio Lula da Silva, antes de assumir, sinalizar compromisso e respeito aos contratos e distanciar-se de discursos de mudanças radicais, sinalizações essas sintetizadas no documento "carta aos brasileiros", as incertezas e o temor com o novo governo foram intensas, conforme ressalta Erber (2011). Agentes econômicos, temerosos e buscando barganhas vantajosas, produziram depreciação do câmbio, elevação da inflação e redução do crescimento do produto, conforme indicam os dados da Tabela 1. Além disso, fatos como a crise das empresas de energia, os atentados de 11 de setembro e o colapso argentino ainda ecoavam sobre a formação de expectativa dos agentes.

Nos primeiros momentos do governo Lula, assim como nos anos anteriores, a resposta imediata às especulações foi uma forte elevação da taxa básica de juros, soma-se a isso, em meados de 2003, uma forte expansão da liquidez e do comércio internacional, com bons resultados ao setor primário e, sobretudo, aos bens semielaborados, como demonstra Erber (2011). Desse modo, a restrição externa deixava de se manifestar, e o temor do governo Lula foi substituído por mais otimismo e entrada de capitais. No câmbio, a consequência foi um movimento de apreciação do câmbio real e nominal.

### Tabela 1: Indicadores selecionados da economia brasileira – período de 1999 a 2021

| Ano | Norma | Meta (%) | Limites (%) | IPCA (%) | Selic (%) | Variação cambial (%) | Variação PIB (%) |
|-----|-------|----------|-------------|----------|-----------|----------------------|------------------|
| 1999 | Res. 2.615 | 8,00 | 6,0-10,0 | 8,94 | 19,0 | 56,4 | 0,5 |
| 2000 | Res. 2.615 | 6,00 | 4,0-8,0 | 5,97 | 15,8 | 0,8 | 4,4 |
| 2001 | Res. 2.615 | 4,0 | 2,0-6,0 | 7,67 | 19,1 | 22,1 | 1,4 |
| 2002 | Res. 2.744 Res. 2.842 | 3,5 3,25 | 1,5-5,5 1,25-5,25 | 12,53 | 24,9 | 19,5 | 3,1 |
| 2003 | Res. 2.972 Res. 2.842 | 4,00 3,75 | 1,5-6,5 1,25-6,25 | 9,3 | 16,3 | 5,4 | 1,1 |
| 2004 | Res. 3.018 | 5,5 | 3,0-8,0 | 7,6 | 17,7 | –5,0 | 5,8 |
| 2005 | Res. 3.108 | 4,5 | 2,0-7,0 | 5,69 | 18,0 | –20,2 | 3,2 |
| 2006 | Res. 3.210 | 4,5 | 2,5-6,5 | 3,14 | 13,2 | –11,9 | 4,0 |
| 2007 | Res. 3.291 | 4,5 | 2,5-6,5 | 4,46 | 11,25 | –11,7 | 6,0 |
| 2008 | Res. 3.378 | 4,5 | 2,5-6,5 | 5,9 | 13,75 | –6,2 | 5,0 |
| 2009 | Res. 3.463 | 4,5 | 2,5-6,5 | 4,31 | 8,75 | 8,2 | –0,2 |
| 2010 | Res. 3.584 | 4,5 | 2,5-6,5 | 5,91 | 10,75 | –13,5 | 7,6 |
| 2011 | Res. 3.748 | 4,5 | 2,5-6,5 | 6,5 | 11,0 | –5,1 | 3,9 |
| 2012 | Res. 3.880 | 4,5 | 2,5-6,5 | 5,84 | 7,25 | 14,3 | 1,8 |
| 2013 | Res. 3.991 | 4,5 | 2,5-6,5 | 5,91 | 10,0 | 9,4 | 2,7 |
| 2014 | Res. 4.095 | 4,5 | 2,5-6,5 | 6,41 | 11,75 | 8,3 | 0,1 |
| 2015 | Res. 4.237 | 4,5 | 2,5-6,5 | 10,67 | 14,25 | 29,4 | –3,8 |
| 2016 | Res. 4.345 | 4,5 | 2,5-6,5 | 6,29 | 14,18 | 4,5 | –3,6 |
| 2017 | Res. 4.419 | 4,5 | 3,0-6,0 | 2,95 | 10,11 | –9,3 | 1,3 |
| 2018 | Res. 4.499 | 4,5 | 3,0-6,0 | 3,75 | 6,58 | 12,7 | 1,8 |
| 2019 | Res. 4.582 | 4,25 | 2,75-5,75 | 4,31 | 6,03 | 7,4 | 1,4 |
| 2020 | Res. 4.582 | 4,0 | 2,5-5,5 | 4,52 | 4,51 | 23,5 | –4,1 |
| 2021 | Res. 4.671 | 3,75 | 2,25-5,25 | 10,06 | 11,25 | 4,4 | 6,0 |

**Fonte:** BCB (2022). Elaboração própria.

**Nota 1:** A Carta Aberta, de 21/1/2003, estabeleceu metas ajustadas de 8,5% para 2003 e de 5,5% para 2004.

O subperíodo, que se inicia ao final de 2002 e vai até 2012 é caracterizado pela apreciação cambial e relativa estabilidade de preços, conforme ilustra a Figura 1, que mostra a análise conjunta da inflação e da taxa de câmbio no país entre 1999 e 2021.

Nesse período cabe destacar que uma das principais causas da apreciação cambial foi a política monetária, que não acompanhou, proporcionalmente, a redução da percepção de risco-país, fato esse que gerou espaço para arbitragem dado o diferencial de taxas de juros interna e externa, com baixo risco inclusive. Como consequência, isso pressionou o mercado de câmbio e induziu a apreciação da moeda doméstica e acumulação de reservas, que garantiram a convergência da taxa de inflação para as metas estabelecidas (ver Tabela 1).

### Figura 1: Inflação (var. IPCA% a.a.) e taxa de câmbio (R$/US$) no Brasil – 1999-2021

[Gráfico de linha mostrando a evolução do IPCA (eixo esquerdo) e taxa de câmbio (eixo direito) entre 1999 e 2021. O IPCA varia entre aproximadamente 2% e 14%, enquanto a taxa de câmbio varia entre 1 e 6 R$/US$.]

**Fonte:** Elaboração própria, baseada em BCB (2022).

Cabe destaque que a apreciação do real está relacionada à política de controle da inflação condicionada à valorização dessa moeda. Nesse ponto é relevante avaliar que no início do Plano Real adotou-se sistema de âncora cambial com liberalização financeira e comercial, sendo a taxa de câmbio fixa e sobrevalorizada o instrumento para conter a inflação. A preponderância do câmbio como elemento de destaque no controle inflacionário mantém-se, pós-1999, mesmo com a adoção do regime de metas de inflação.

No período de 2002 a 2012 o patamar do câmbio no Brasil contribuiu para manter a inflação baixa. O câmbio apreciado diminuía o preço das importações, sejam matérias-primas ou produtos finais. As matérias-primas diminuíam os preços finais de produtos nacionais que as usavam como insumos, e os produtos finais importados pressionavam para baixo os preços dos bens nacionais concorrentes. Além disso, o dólar baixo exerceu importantes efeitos de baixa sobre os preços administrados, como da energia elétrica, telefonia e planos de saúde, por exemplo. Esses preços têm seus reajustes pela variação do Índice Geral de Preços do Mercado (IGP-M), que é fortemente influenciado pelo dólar.

No período recente, posterior a 2012, são os fatores externos como o fim das políticas de quantitative-easy adotadas por alguns países desenvolvidos como resposta à crise do subprime de 2008, aliado à crise política, econômica e, mais recentemente, sanitária, que explicam de forma mais direta a alta da taxa de câmbio e consequente elevação da inflação no Brasil.

Quanto à crise política, as incertezas em relação à efetivação da política econômica durante o segundo governo de Dilma Rousseff pressionaram o real brasileiro, como mostra a variação cambial de 2014 para 2015 (Tabela 1). Também a profunda recessão que se seguiu entre 2015 e 2016, conforme mostra a Tabela 1, em que o PIB registrou queda acumulada de cerca de 7% (–3,8% em 2015 e –3,6% em 2016), explica a manutenção da taxa de câmbio elevada nesses anos, apesar de o Banco Central Brasileiro ter aumentado gradual e continuamente a meta da taxa de juros Selic a partir de 2014.[^2]

[^2]: Ver Prates et al. (2017) para uma discussão sobre mudanças na política cambial no período do governo de Dilma Rousseff.

Desde então, a taxa de câmbio começou a sofrer contínua tendência à depreciação, conforme mostram as variações cambiais positivas, desde 2014 (Tabela 1). Mais recentemente, incertezas ligadas à pandemia de Covid-19 e às inseguranças políticas no Brasil têm contribuído para desvalorização constante do real, que foi uma das moedas que mais perdeu valor nos últimos anos.

Associados à depreciação cambial, a elevação dos preços das commodities – com o início da recuperação das economias da crise da Covid e as políticas fiscais expansionistas empreendidas para combatê-la – e o desmantelamento das cadeias globais de valor – caracterizados pela paralisação compulsória de muitas empresas por restrição de oferta por falta de produtos como semicondutores, eletrônicos, produtos químicos etc. – pressionaram o nível de preços, que fechou 2021 em 10,6% a.a., conforme a Tabela 1 indica.

Diante da análise anterior, é possível concluir que, sob metas de inflação e câmbio flutuante, observa-se na economia brasileira que os anos com taxas de câmbios mais depreciadas – 2002, 2015 e 2021 – também foram os que registraram maiores taxas de inflação (Tabela 1 e Figura 1), inclusive acima de dois dígitos. Já os anos nos quais a taxa de câmbio manteve-se relativamente apreciada também foram caracterizados por taxas de inflação mais baixas, a exemplo do período entre 2005 e 2014.

É essa relação entre câmbio e preços que se tenciona investigar, empiricamente, com o intuito de identificar os diferentes padrões de transmissão das variações na taxa de câmbio para a inflação no Brasil e permitir melhor compreensão do mecanismo de repasso cambial no contexto do regime de metas para a inflação e suas consequências para a economia brasileira.

---

## 4 Estratégia empírica

### 4.1 Modelo econométrico

Observa-se nos estudos empíricos sobre repasse cambial que há diferentes métodos para avaliação do fenômeno na economia brasileira. Este estudo optou por utilizar o modelo econométrico de Autorregressão Vetorial (VAR).

De acordo com Enders (2014), um VAR é uma extensão do modelo Autorregressivo (AR) em um contexto multivariado, em que se utiliza um conjunto de séries temporais sendo que cada variável é uma função linear de seus valores defasados e dos valores defasados de outras variáveis. O VAR é utilizado para