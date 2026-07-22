# Modelos Mentais de Câmbio — Kapitalo Investimentos (2019–2026)

## Sobre este documento

Este é um documento de referência sobre os **modelos mentais de análise cambial** (BRL/USD, moedas de mercados emergentes e dinâmica global do dólar) extraídos das cartas mensais "Carta do Gestor K10" da Kapitalo Investimentos, cobrindo 83 cartas consecutivas entre julho de 2019 e maio de 2026 (`repository/mental_model/kapitalo/`).

O K10 é um fundo macro global multi-ativo: cada carta traz um "Cenário" narrativo curto seguido de listas de posições por livro (Commodities, Moedas, Bolsa, Renda Fixa) e uma tabela de P&L mensal por classe de ativo. Diferente da Kinea e da Verde — gestoras Brasil-cêntricas cujas cartas dedicam parágrafos extensos a justificar cada posição —, as cartas do K10 são telegráficas: a seção "Moedas" é, na maioria dos meses, apenas uma lista curta de posições adicionadas/zeradas, com racional textual concentrado em uma minoria de cartas (tipicamente quando um tema novo emerge ou vira "case" dedicado). Por isso, boa parte dos modelos abaixo foi reconstruída cruzando o parágrafo de "Cenário" do mês (que discute o tema macro dominante — Fed, China, tarifas, fiscal brasileiro etc.) com a lista de posições que imediatamente o segue, e não apenas transcrevendo frases isoladas da seção de câmbio.

Como nas outras gestoras, o documento reúne conteúdo **diretamente** cambial (posições em BRL, USD, EUR, CNY, MXN, TRY, ARS/peso, e outras moedas) e **indiretamente** cambial — diferencial de juros, termos de troca, condições financeiras, risco fiscal, geopolítica — sempre que o texto usa esse conteúdo para embasar uma tese de câmbio. Uma característica distintiva da Kapitalo (ausente nos outros dois modelos já documentados) é a presença de um bloco extenso de frameworks *metodológicos* — estilo de investimento, dimensionamento de posição, valuation por paridade de poder de compra — descritos com grande explicitação em cartas de 2019-2020 e depois aplicados implicitamente (sem repetir a exposição teórica) ao longo dos anos seguintes.

Os modelos foram consolidados por tema, não por carta. Quando o mesmo arcabouço aparece em múltiplos anos — o que é comum, dado que vários frameworks (divergência de crescimento/Fed, risco fiscal brasileiro, cestas de carry EM) persistem com composição tática variável mas lógica constante —, foi unificado em uma única entrada com a evolução temporal documentada nos exemplos. Citações em português são literais das cartas, nunca traduzidas.

Este documento foi construído de forma independente, só a partir das fontes da Kapitalo — sem cruzamento ou comparação com os modelos equivalentes já existentes para a Kinea (`kinea_fx_mental_models.md`) e a Verde Asset (`verde_fx_mental_models.md`).

---

# 1. Processo e Filosofia de Investimento em Câmbio

Cluster sem equivalente direto nos documentos da Kinea/Verde: a Kapitalo, nas suas primeiras cartas (2019-2020), dedica espaço incomum a explicitar o *processo* de decisão — não apenas o diagnóstico macro — de forma que se aplica ao livro de câmbio tanto quanto aos demais. Esses princípios raramente são re-expostos em detalhe nos anos seguintes, mas continuam visivelmente orientando como as posições cambiais são montadas, dimensionadas e desmontadas ao longo de toda a amostra.

## 1.1 Estilo Híbrido: Diagnóstico Fundamentalista + Confirmação Técnica como Gatilho de Tamanho

**O que é:** O estilo de investimento declarado da casa, aplicado ao câmbio: uma tese fundamentalista identifica *o quê* (uma moeda desalinhada com potencial de movimento), mas o tamanho da posição só é ampliado conforme o preço efetivamente começa a confirmar essa tendência (momentum/trend-following) — a boa análise econômica isolada não é suficiente para justificar alocação grande. Alocação inicial modesta (ex.: 4 em escala de 0 a 10) mesmo com convicção fundamentalista alta, aumentada só com confirmação de preço.

**Variáveis-chave:**
- Existência de tendência de preço já em curso (time-series momentum)
- Posicionamento técnico dos investidores
- Reação de preço a eventos positivos/negativos
- Escala de alocação (0–10) ajustada conforme confirmação
- Orçamento de perda máxima por tese

**Como a Kapitalo aplicou:**
- **Jul/2019** (carta inaugural, case da coroa norueguesa): "montar posições compradas ou vendidas em mercados que estão subindo ou caindo e apostar que estas condições continuarão." Apesar do diagnóstico fundamentalista favorável (NOK ~10% barata via PPP), a alocação inicial foi de tamanho 4 de 10 porque "os sinais de início de uma tendência de preços ainda são fracos... A reação de preço a eventos positivos tem sido relativamente frustrante." Conclusão: "Como sabemos de nossa incapacidade de imaginar todos os cenários possíveis, mantemos uma alocação inicial de tamanho 4... precisamos de sinais técnicos mais fortes para aumentar nossa alocação."
- Ao longo de 2019–2020, as posições em moedas são tipicamente ajustadas de forma incremental mês a mês (NOK reduzida em jul/2019, mantida estável em ago-set/2019), consistente com gestão ativa de uma tendência em desenvolvimento, não uma aposta binária de tamanho fixo.

## 1.2 Framework Tripartite de Horizontes: "Vetores e Indicadores Econômicos para Câmbio de Moedas"

**O que é:** A taxonomia-mestra mais explícita do documento — uma matriz de drivers cambiais organizada por horizonte temporal (longo, médio, curto prazo), funcionando como o "mapa" que organiza todos os demais frameworks de valuation e ciclo dentro de um único processo de diagnóstico.

**Variáveis-chave:**
- Longo prazo: Paridade do Poder de Compra (PPP), Produtividade Relativa, Custo Unitário do Trabalho Relativo
- Médio prazo: Divergência de Política Monetária, Diferencial de Crescimento, Contas externas
- Curto prazo: Apetite ao Risco, Posicionamento Técnico, Dinâmica de Preço

**Como a Kapitalo aplicou:**
- **Jul/2019:** apresentado como tabela explícita no case da coroa norueguesa, com título "Alguns Vetores e Indicadores Econômicos para Câmbio de Moedas," estruturando toda a análise que segue (PPP → Balassa-Samuelson → termos de troca → diferencial de crescimento/política monetária → apetite ao risco/técnico) — cada seção subsequente do case ("Big Picture," "A dinâmica atual," "Análise técnica e possíveis catalisadores") mapeia para uma linha da tabela.

## 1.3 Dimensionamento de Posição e Risco de Ruína (Stop-Loss por Alocação, Estilo Kelly)

**O que é:** Framework de gestão de risco — não específico de câmbio, mas explicitamente aplicado a ele junto com as demais classes: mesmo com valor esperado positivo conhecido, exposição/alavancagem excessiva reduz o retorno composto de longo prazo além de um ponto ótimo. Usado para justificar disciplina de stop-loss por alocação e redução ativa de posições cambiais quando a perda estimada em cenário adverso fica alta demais.

**Variáveis-chave:**
- Valor esperado e desvio-padrão da tese
- Retorno composto (geométrico) vs. retorno esperado simples
- Perda potencial estimada em cenário adverso (stop-loss por alocação)

**Como a Kapitalo aplicou:**
- **Jul/2020:** ensaio dedicado com exemplo numérico ("cara ganha 50%, coroa perde 35%") mostrando que "a exposição ao risco, acima de um ponto ótimo, reduz o retorno de longo prazo da carteira": "Buscamos retornos através da seleção de bons ativos financeiros, moedas e commodities: para isso estimamos para cada oportunidade, não somente quanto temos a ganhar, mas também a perda potencial em cenários adversos. Utilizamos o Stop-Loss por alocação, como ferramenta de gestão."
- Referenciado indiretamente ao longo de todas as cartas via reduções táticas de posições cambiais em momentos de alta incerteza (ago/2019, fev-mar/2020, mar/2026 — ver 1.7) mesmo mantendo a tese direcional de fundo.

## 1.4 Cenário Central vs. Distribuição de Probabilidades ("Contamos Barris, Mas Negociamos Probabilidades")

**O que é:** Princípio metodológico explícito de como todas as teses macro da casa (inclusive cambiais) são construídas: decisões não se baseiam apenas no cenário central esperado, mas em um exercício recorrente de desenho de cenários e balanços de oferta/demanda que serve para identificar desequilíbrios e assimetrias — ou seja, posicionamento pensado em distribuições de probabilidade, não em um único cenário-base.

**Variáveis-chave:**
- Cenário central de atividade/inflação por país
- Balanços de oferta e demanda
- Assimetrias de risco/retorno nas posições

**Como a Kapitalo aplicou:**
- **Dez/2023:** "Como dissemos em cartas anteriores, não tomamos decisões de investimentos baseadas somente em cenário econômico central. Contudo, o exercício de desenhar diagnósticos e projetar cenários e/ou balanços de oferta e demanda, quando feito de forma recorrente, é de suma importância para identificar possíveis desequilíbrios e fragilidades" — citado imediatamente antes de reafirmar a tese de moedas cíclicas/EM (BRL, MXN) bem posicionadas no cenário-base de desinflação global com atividade resiliente (ver 2.3/2.5).

## 1.5 Decomposição Idiossincrático vs. Beta Global: Pares de Valor Relativo entre Moedas de Risco Semelhante

**O que é:** Separar o retorno de uma moeda em componente sistemático (dirigido pelo apetite a risco global) e componente idiossincrático (fundamentos específicos do país) — usado para construir pares de valor relativo entre duas moedas de perfil de risco parecido (ex.: rublo russo vs. rand sul-africano, ambas EM/commodity) que isolam a diferenciação idiossincrática reduzindo exposição ao beta direcional do dólar/risco global.

**Variáveis-chave:**
- Retorno idiossincrático vs. retorno explicado por fator de risco comum
- Pares de moedas com perfil de risco semelhante mas fundamentos distintos
- Sanções/geopolítica vs. risco fiscal/político como exemplo de diferenciação

**Como a Kapitalo aplicou:**
- **Set/2019:** "Algumas de nossas alocações tiveram uma nítida melhora na parte idiossincrática... Mantivemos nossas alocações compradas em rublo russo contra o rand sul-africano e coroa norueguesa contra o euro" — RUB/ZAR e NOK/EUR tratados explicitamente como pares de valor relativo idiossincrático, distintos do book direcional de risco.
- **Fev/2020:** "Reduzimos também a posição comprada em rublo russo contra o rand sul-africano" durante o choque de liquidez do COVID — mesmo pares de valor relativo são reduzidos quando a dispersão de correlações aumenta.

## 1.6 Opções vs. Posições Diretas Conforme Custo de Volatilidade Implícita

**O que é:** Decisão tática de instrumento (não de direção): quando a volatilidade implícita cai a níveis historicamente baixos, a Kapitalo substitui apostas direcionais em câmbio (futuros/forwards) por opções, mantendo a mesma visão de mercado mas aproveitando o preço barato de opcionalidade.

**Variáveis-chave:**
- Nível de volatilidade implícita (histórico vs. atual)
- Direção da tese fundamental (mantida constante ao trocar o instrumento)

**Como a Kapitalo aplicou:**
- **Mar/2024:** "No mercado de moedas, alteramos o perfil das posições ao trocar as apostas direcionais em BRL e AUD por opções, aproveitando os níveis historicamente baixos de volatilidade implícita."

## 1.7 Redução de Risco Direcional Condicionada à Previsibilidade de Eventos Geopolíticos Extremos

**O que é:** Heurística de dimensionamento: quando o grau de previsibilidade subjetivo sobre o desfecho de um evento geopolítico extremo é muito baixo e a janela de tempo até um desfecho relevante é curta, a resposta é reduzir taticamente o tamanho das posições direcionais nos livros mais expostos — incluindo moedas — independentemente da convicção estrutural de médio prazo.

**Variáveis-chave:**
- Grau de previsibilidade subjetivo sobre o desfecho do conflito/choque
- Janela de tempo estimada até a resolução
- Probabilidade de movimentos de preço não lineares
- Tamanho das alocações direcionais por livro

**Como a Kapitalo aplicou:**
- **Mar/2026** (guerra EUA/Israel-Irã, fechamento do Estreito de Ormuz): "Nosso grau de previsibilidade sobre quais serão as próximas etapas do conflito e, por consequência, qual solução será dada para o estreito de Ormuz, ainda é muito baixo... a janela de tempo para que o mercado de petróleo continue funcional é pequena, de apenas algumas semanas." Ação: "Reduzimos taticamente as alocações direcionais em moedas e em bolsas" — mês em que o livro de moedas teve sua única contribuição negativa de toda a amostra (-0,68%).
- **Fev/2026** (episódio correlato, início do conflito): mesma lógica aplicada ao livro de commodities (zeragem de posição vendida em petróleo antes da escalada) — padrão de corte de risco direcional diante de choque geopolítico súbito que depois se estende ao livro de moedas.

---

# 2. Valuation Cambial de Longo Prazo: PPP, REER e Termos de Troca

## 2.1 Valuation por PPP/REER como Âncora de Realinhamento de Longo Prazo

**O que é:** Comparação do câmbio real efetivo (REER) atual contra sua média histórica (ajustada por inflação) para estimar se uma moeda está "cara" ou "barata" versus uma cesta de parceiros comerciais, derivando um preço-alvo de realinhamento de longo prazo.

**Variáveis-chave:**
- REER (CPI-based) vs. média de 10 anos
- Cesta de moedas de comparação (BIS)
- Preço-alvo implícito do câmbio bilateral

**Como a Kapitalo aplicou:**
- **Jul/2019** (case da coroa norueguesa): "Contra uma cesta de moedas e ajustando para a inflação, a Coroa Norueguesa está 'barata' em aproximadamente 10%... Um realinhamento com um modelo de PPP de longo prazo poderia levar o EUR/NOK para aproximadamente 8,853" — base fundamentalista central da posição comprada em NOK vs. EUR.

## 2.2 Efeito Balassa-Samuelson / Custo Unitário do Trabalho Relativo

**O que é:** Mecanismo pelo qual um boom de commodities eleva salários domésticos além do crescimento de produtividade, minando a competitividade externa e pressionando a moeda a se desvalorizar (ou exigindo ajuste de preços relativos) quando o boom reverte.

**Variáveis-chave:**
- Custo Unitário do Trabalho (variação anual, comparado entre países)
- Crescimento de produtividade
- Preço da commodity de exportação

**Como a Kapitalo aplicou:**
- **Jul/2019:** explicação da queda do NOK em 2013–2015: "a bonança dos altos preços de petróleo do período entre 2004 e 2012 gerou uma alta generalizada de salários. Esse movimento foi incompatível com o crescimento de produtividade – efeito Balassa-Samuelson" — usado para contextualizar por que a moeda precisou desvalorizar antes de poder voltar a se valorizar.

## 2.3 Termos de Troca e Ciclo de Commodities como Driver Estrutural de Moedas Exportadoras

**O que é:** Moedas de países fortemente dependentes de exportação de commodities (petróleo, metais, agrícolas) se movem com o ciclo de preços dessas commodities via termos de troca e conta corrente — tese estrutural (caso norueguês) e cesta tática recorrente (RUB, AUD, CAD, NOK, MXN compradas/vendidas ao longo dos anos conforme o ciclo global de commodities e apetite a risco).

**Variáveis-chave:**
- Termos de troca (índice)
- Preço da commodity-chave de exportação
- Superávit/déficit em conta corrente
- Custo de break-even de produção

**Como a Kapitalo aplicou:**
- **Jul/2019:** "A recuperação dos preços do petróleo também levou à melhora dos termos de troca desde 2016, gerando um aumento do superávit da conta-corrente" (Noruega) + análise de break-even de exploração de petróleo abaixo da curva futura.
- **Nov/2019:** "Adicionamos uma alocação comprada em peso mexicano e peso chileno contra o dólar americano" — expansão da cesta de moedas exportadoras de commodities/EM.
- **Mar/2022:** "Adicionamos posições compradas no dólar australiano e no dólar canadense contra o dólar" — longs clássicos de moeda-commodity (AUD: metais/energia; CAD: petróleo), mantidos boa parte do ano.
- **Nov/2023:** "A balança comercial segue surpreendendo para cima e deve ficar próxima a USD 90 bilhões em 2023, o maior valor da série histórica. O aumento da produção de grãos e de petróleo deve garantir um fluxo comercial e um aumento de arrecadação bastante positivos" — usado tanto para BRL quanto, em dez/2023, estendido ao México: "nos parece inegável a melhora recorrente nas contas externas de Brasil, assim como as do México."

## 2.4 Regras Fiscais / Fundos Soberanos como Amortecedor do Repasse ao Câmbio

**O que é:** Mesmo quando termos de troca melhoram e a conta corrente registra superávit, regras fiscais que reciclam receita de commodities para um fundo soberano (em vez de permitir conversão doméstica) limitam a apreciação cambial que, de outra forma, ocorreria — mecanismo de fluxo de capital/BOP que modera (mas não elimina) a tese de valorização.

**Variáveis-chave:**
- Regras fiscais de transferência de receita ao fundo soberano
- Tamanho do fundo soberano (% do PIB)
- Posição internacional de investimento (% do PIB)

**Como a Kapitalo aplicou:**
- **Jul/2019:** "as regras fiscais vigentes limitam o impacto da melhora do superávit na moeda, uma vez que o governo transfere parte dessas receitas para o fundo soberano... Por outro lado, isso leva a uma melhora da posição internacional de investimento, que já soma 220% do PIB" — usado para explicar por que a tese de apreciação do NOK, mesmo fundamentada, é mais lenta/limitada do que sugeriria só o superávit em conta corrente.

## 2.5 Modelo de Câmbio de Equilíbrio via Posição Externa (BOP Fair-Value), Aplicado ao Brasil

**O que é:** Modelo explícito, com projeções numéricas de balanço de pagamentos, que deriva um câmbio de equilíbrio a partir da conta corrente, financiamento externo (IED), reservas e endividamento externo. Quando o crescimento da demanda doméstica supera o potencial (puxado por massa salarial e impulso fiscal), as importações sobem, a conta corrente piora e isso justifica uma revisão altista do câmbio de equilíbrio — mesmo com a posição externa (dívida externa baixa, reservas elevadas, déficit financiado por IED) permanecendo "sólida".

**Variáveis-chave:**
- Projeção de conta corrente (USD bi e % do PIB)
- Crescimento da quantidade importada
- Financiamento do déficit em conta corrente (IED vs. outros fluxos)
- Nível de reservas internacionais e endividamento externo
- Massa salarial e impulso fiscal como drivers de demanda agregada

**Como a Kapitalo aplicou:**
- **Jun/2024:** tabela comparativa "ANTIGO" vs. "NOVO" de projeção de conta corrente para dez/24 (revisada de -1,0% para -2,2% do PIB; balança comercial de 3,9% para 2,7% do PIB): "Nossas projeções de conta corrente pioraram desde o início do ano, muito influenciadas pelo forte crescimento da quantidade importada, subindo levemente nossas projeções de câmbio de equilíbrio." Ressalva: "a posição externa do Brasil segue sólida, com baixo endividamento externo e elevado nível de reservas, e um déficit de 2,2% do PIB em conta corrente tem sido financiado pelos investimentos estrangeiros diretos."
- **Jun/2024** (encadeamento causal): "O forte crescimento da massa salarial e o expressivo impulso fiscal vêm gerando expansão da demanda agregada acima dos patamares consistentes com o potencial da economia, produzindo uma queda contínua da taxa de desemprego e uma deterioração gradual das contas externas."

---

# 3. Ciclo Global do Dólar, Fed e Divergência entre Desenvolvidos

## 3.1 Diferencial de Crescimento e Divergência de Política Monetária como Driver Central e Recorrente

**O que é:** O framework mais persistente do documento inteiro: o dólar (e demais moedas) se aprecia ou deprecia em função da divergência entre o ciclo de crescimento e o timing/velocidade de alta ou corte de juros do respectivo banco central frente aos pares. Países com atividade mais forte e BC mais hawkish (ou mais lento a cortar) têm moeda valorizada; países com atividade mais fraca e corte mais rápido, moeda vendida. O sinal se inverte completamente conforme o ciclo evolui, sendo reaplicado ano após ano a pares diferentes.

**Variáveis-chave:**
- Diferencial de crescimento/PIB entre países
- Trajetória e velocidade da taxa de política monetária (hiking vs. easing) por BC
- Inflação doméstica vs. meta
- Postura declarada do Banco Central (guidance)
- Mercado de trabalho como gatilho de mudança de rota

**Como a Kapitalo aplicou:**
- **Jul/2019:** sobre a Noruega — "a Noruega chama a atenção pelo sólido desempenho econômico... também é distinto o comportamento do Banco Central do país que, ao contrário dos outros BCs do G10, continua no processo de normalização da taxa de juros."
- **Jan/2022:** "Mantivemos a carteira do K10 focada em alocações compradas em commodities, comprada no dólar americano e tomada em juros globais" — postura de dólar amplo justificada pelo aperto sincronizado das economias desenvolvidas.
- **Jan/2024:** "seguimos com posições aplicadas e com maior exposição às economias europeias – Zona do Euro, Suécia e Reino Unido, onde a atividade continua fraca e pode entrar em recessão" — vendidos EUR/GBP, comprados AUD/BRL contra USD.
- **Set/2024:** inversão completa — "Seguimos com um livro vendido no dólar norte-americano e no renminbi chinês e comprados no real brasileiro, no peso mexicano, na lira turca e na rúpia indiana", coincidindo com corte de 0,5% do Fed mais célere que o esperado.
- **Out/2024:** retorno à tese de dólar forte — "Vemos uma assimetria altista para o dólar americano... Ajustamos nosso livro de câmbio, aumentando nossa exposição comprada em dólar norte-americano contra uma cesta de países desenvolvidos e o renmimbi chinês."
- **Jan/2025:** "A divergência do ciclo econômico e da política monetária cria um ambiente para que os ativos norte-americanos sigam outperformando. Seguimos comprados no dólar norte-americano contra uma cesta de moedas."
- **Abr/2025:** zeragem total da posição comprada em USD após deterioração das condições financeiras pós-"Liberation Day" (ver 4.1); **Mai/2025:** virada para posição vendida em USD, mantida pelo resto do ano.
- **Mai/2026:** reversão final registrada na amostra — "O diferencial de crescimento a favor dos Estados Unidos e o Fed mais preocupado com a inflação jogam a favor de um dólar norte-americano mais forte, principalmente contra as moedas dos países desenvolvidos. Adicionamos uma posição comprada no dólar norte-americano contra o euro e contra a libra esterlina", citando consumo doméstico resiliente, impulso fiscal e ciclo de investimento em IA como fontes do diferencial de crescimento.

## 3.2 Índice de Condições Financeiras — Câmbio como Componente Equivalente a Juros na Transmissão Monetária

**O que é:** O câmbio não é tratado como um mercado separado, mas como um dos cinco componentes estruturais de um índice de condições financeiras (US-FCI da Goldman Sachs) que determina quanto aperto monetário foi de fato transmitido à economia real. A apreciação de uma moeda é funcionalmente equivalente a uma alta de juros em termos de efeito restritivo sobre o PIB — o que significa que movimentos cambiais podem substituir, ou amplificar, movimentos da taxa de política na entrega do aperto necessário.

**Variáveis-chave:**
- US-FCI (Goldman Sachs): (i) juros de curto prazo, (ii) juros de longo prazo, (iii) mercado acionário, (iv) spread de crédito, (v) taxa de câmbio
- Impacto de 1 ponto do índice ≈ 1% do PIB real
- Gap entre aperto "esperado" pela alta de juros de curto prazo e aperto observado no FCI

**Como a Kapitalo aplicou:**
- **Mai/2022** (anexo dedicado): "O índice de condições financeiras é o US-FCI da Goldman Sachs... uma combinação de variáveis de i) taxa de juros de curto prazo, ii) taxa de juros de longo prazo, iii) mercado acionário iv) spread de crédito e v) taxa de câmbio." Conclusão: "desde o início do ano, o aperto financeiro acarretaria, em teoria, uma desaceleração extra de 2% do PIB... é possível concluir que o aperto prometido pelo Fed e precificado pelo mercado de juros já é condizente com o crescimento do PIB aproximadamente em linha com o potencial."
- **Mai/2022** (nota metodológica): decomposição do aperto do FCI atribuível à alta de juros curtos vs. outras fontes (câmbio incluído): "as condições financeiras pioraram além do que seria de se esperar apenas pelas altas das taxas de juros curtas... Pode ser que isso indique uma transmissão monetária maior do que o esperado."

## 3.3 Excepcionalismo Americano e Risco Político-Eleitoral como Reforço Estrutural do Dólar

**O que é:** Além da divergência cíclica normal (3.1), a eleição americana de 2024 é tratada como um choque estrutural adicional que reforça a força do dólar por múltiplos canais simultâneos: produtividade relativa atraindo capital ("excepcionalismo"), tarifas elevando inflação doméstica e o diferencial de crescimento, e restrições migratórias reduzindo o espaço de corte do Fed.

**Variáveis-chave:**
- Resultado eleitoral e composição do Congresso
- Agenda de tarifas, desregulamentação e corte de impostos
- Restrições à imigração
- Produtividade relativa EUA vs. resto do mundo
- Volatilidade implícita do câmbio

**Como a Kapitalo aplicou:**
- **Out/2024:** "O aumento da probabilidade de vitória do candidato republicano, aliado à estabilização do mercado de trabalho norte-americano, produziu alta expressiva das taxas de juros globais, fortalecimento do dólar e aumento da volatilidade implícita."
- **Nov/2024** (pós-eleição): "as diretrizes vão na direção de reforçar o excepcionalismo da economia e dos ativos norte-americanos e criam um ambiente mais desafiador para os países emergentes... A imposição de tarifas sobre as importações de bens deve aprofundar o diferencial de crescimento dos Estados Unidos com o resto do mundo e produzir alguma elevação da inflação. As maiores restrições à imigração também vão no sentido de uma inflação mais persistente, o que reduz o espaço para cortes de juros pelo Fed e gera uma força adicional de apreciação do dólar." Posição: "Seguimos com posições compradas no dólar norte-americano contra o renminbi chinês, o euro, o real brasileiro e o franco suíço."

## 3.4 Fluxo de Diversificação Global / "De-Dolarização" Tática Beneficiando FX de Emergentes

**O que é:** Tese de 2026: o ativismo geopolítico do governo americano (disputas territoriais, tarifas, agenda populista pré-eleitoral) somado a sinalizações de fundos de pensão internacionais reduzindo alocação em ativos americanos acelera um movimento de realocação de portfólios globais para fora dos EUA — beneficiando especificamente bolsas, commodities e moedas de mercados emergentes, expresso via posição estruturalmente vendida em USD contra uma cesta EM.

**Variáveis-chave:**
- Postura geopolítica/tarifária do governo americano
- Sinalizações de realocação por fundos de pensão internacionais
- Cesta de moedas EM long vs. USD como veículo de expressão
- Risco agregado do livro de moedas (mantido baixo apesar da tese estrutural)

**Como a Kapitalo aplicou:**
- **Jan/2026:** "Nosso livro de moedas está com risco baixo, mas segue vendido no dólar norte-americano contra países emergentes... Essa busca por diversificação beneficiou os ativos de países emergentes, principalmente as bolsas, e algumas commodities." Mantidos comprados iene, lira turca, peso chileno, rand sul-africano e rúpia indiana contra USD.
- **Mar/2026:** racional muda de eixo temporariamente — a tese estrutural de diversificação segue, mas o tamanho é cortado por choque geopolítico agudo (ver 1.7).
- **Mai/2026:** o racional para os shorts remanescentes em moedas desenvolvidas (EUR, GBP) migra desta tese para o Framework 3.1 (diferencial de crescimento/Fed) — mostrando como a mesma posição pode trocar de racional subjacente sem trocar de direção.

## 3.5 Moedas Porto-Seguro (Iene, Franco Suíço) como Hedge de Risco Global/Recessão

**O que é:** Independentemente da tese direcional específica sobre o dólar, a Kapitalo mantém recorrentemente uma alocação em iene japonês (e, em episódios de risco de recessão mais aguda, franco suíço) como hedge estrutural contra deterioração de apetite a risco — usado tanto para amortecer o livro quanto como posição tática quando a incerteza aumenta.

**Variáveis-chave:**
- Iene japonês (JPY) e franco suíço (CHF) vs. dólar
- Probabilidade de recessão implícita em curvas de juros, inflação implícita e derivativos de commodities
- Sincronização de movimentos entre classes de ativos (sinal de mudança de regime)

**Como a Kapitalo aplicou:**
- **Jul/2019:** "Mantivemos... nossa posição comprada em iene, ambos contra o dólar" mesmo em mês de redução geral de posições.
- **Jan/2020:** em resposta ao surgimento do coronavírus: "aumentamos o nível de proteção em nossa carteira em função do aumento recente da incerteza relacionada aos efeitos do surto de coronavírus na atividade global", mantendo/adicionando iene, dólar australiano e libra vs. dólar.
- **Mar–Set/2020:** iene mantido como posição estrutural longa durante toda a crise do COVID, mesmo com zeragem de outras posições de risco.
- **Jun/2022:** "O mês de junho foi marcado pelo aumento da probabilidade de recessão nos preços dos ativos... (i) a surpresa no aumento de 75 pontos base pelo Federal Reserve, e (ii) a queda inesperada no fornecimento de gás da Rússia para a Alemanha." Ação: "Adicionamos uma posição comprada no franco suíço."
- **Mar/2025:** durante o choque de "Liberation Day", "o livro de moedas continua com suas maiores alocações comprado em dólar americano e no iene japonês" — JPY como hedge dentro de um livro ainda long-USD.

## 3.6 Apetite a Risco Global (Risk-On/Risk-Off) como Overlay de Dimensionamento da Carteira

**O que é:** Um regime macro de "apetite a risco global" que determina o tamanho agregado de exposição em moedas de risco/EM, independentemente das teses idiossincráticas individuais — funciona como um multiplicador de exposição aplicado sobre as teses estruturais de fundo.

**Variáveis-chave:**
- "Viés" declarado da carteira (otimista/cauteloso)
- Escaladas geopolíticas e eventos de risco (guerra comercial, protestos, pandemia)
- Prêmios de risco globais (spreads, vol implícita)

**Como a Kapitalo aplicou:**
- **Ago/2019:** "Reduzimos nossas posições, mas mantivemos um livro otimista com bolsa e moedas de alguns países emergentes" em resposta à "escalada da guerra comercial... acirramento dos protestos em Hong Kong e a surpresa no resultado das primárias na Argentina."
- **Fev-Mar/2020:** "Reduzimos de forma expressiva nossas posições durante o início do mês de março" por conta do COVID, cortando GBP, AUD, MXN, RUB/ZAR.
- **Mai-Jun/2020:** reversão — "mantivemos as posições compradas em iene e dólar australiano... Adicionamos posições compradas em real, peso mexicano e euro contra o dólar americano" à medida que o apetite a risco voltava.
- **Nov/2020:** "A confirmação de resultados com alta eficácia de algumas vacinas contra o COVID e o resultado de menor risco nas eleições americanas foram os principais catalisadores... Mantemos o viés otimista, mas reduzimos algumas alocações" (realização de lucro após forte alta do regime de risco).

---

# 4. Comércio, Tarifas e Geopolítica

## 4.1 Tarifas como Choque de Oferta: Trade-off Crescimento/Inflação e Competitividade Relativa

**O que é:** A agenda tarifária americana (2025) é tratada como um choque de oferta análogo a um imposto sobre consumo: eleva o nível de preços doméstico nos EUA e desacelera a atividade global, sendo potencialmente desinflacionário fora dos EUA (abrindo espaço para mais cortes de juros alhures). A diferença de alíquotas entre países cria um incentivo a realocação de manufatura, beneficiando a competitividade relativa de certos países (asiáticos), com efeitos diretos sobre pares de câmbio.

**Variáveis-chave:**
- Alíquota média de importação dos EUA e sua evolução
- Diferencial de tarifas entre China e demais parceiros
- Risco de recessão global vs. probabilidade de acordo bilateral
- Realocação de cadeias de manufatura (reshoring/friend-shoring)

**Como a Kapitalo aplicou:**
- **Mar/2025** ("Liberation Day"): analogia histórica — "o último evento similar ocorreu na década de 1930, que agravou a Grande Depressão da economia americana." Livro de moedas/juros/commodities com perfil baixista para desaceleração global.
- **Abr/2025:** "a discrepância entre as alíquotas incidentes sobre a China e os demais países permanecerá, o que deve afetar a competitividade relativa e criar um incentivo à realocação da manufatura global. Alguns países asiáticos podem se beneficiar." Ação: "Adicionamos posições compradas na rúpia indiana, no dólar canadense e no dólar australiano contra o renminbi" — trade explícito de realocação de manufatura.
- **Mai/2025:** reversão da tese de risco extremo após recuo do governo Trump nas tarifas à China e derrota judicial — redução de hedges (mas dólar seguiu vendido, ver 3.1).
- **Jul/2025:** "a imposição de tarifas comerciais pelo presidente Trump tende ter impacto contracionista sobre atividade global e pode até ter efeito desinflacionário fora dos Estados Unidos, reforçando o espaço para cortes adicionais de juros."
- **Out/2025:** desfecho positivo — "o acordo comercial entre os Estados Unidos e a China resultou em uma redução marginal das tarifas comerciais e reduziu o risco de ruptura nas cadeias globais de produção."

## 4.2 Divisão Intra-Europeia Exportador vs. Importador de Energia (Guerra Rússia-Ucrânia)

**O que é:** A guerra Rússia-Ucrânia e a crise energética resultante são tratadas como um choque de termos de troca que atinge economias importadoras líquidas de energia (Zona do Euro) muito mais duramente do que exportadoras líquidas dentro da mesma região (Noruega). Gera uma postura persistente vendida em EUR (reforçada por um ECB visto como mais devagar a apertar que o Fed) e um cruzamento específico NOK longo vs. EUR curto como expressão mais pura da divisão intraeuropeia.

**Variáveis-chave:**
- Dependência de gás/petróleo russo da Zona do Euro
- Sanções e cortes de fornecimento de energia
- Postura relativa ECB vs. Fed
- Produção/exportação de petróleo e gás da Noruega

**Como a Kapitalo aplicou:**
- **Fev/2022** (invasão): "A invasão da Ucrânia pelo exército russo gerou uma reação contundente das economias ocidentais... A Rússia enfrentará uma profunda recessão econômica e o crescimento global deve ser impactado, principalmente o da Europa." Ação: "Adicionamos... posição comprada na coroa norueguesa contra o euro."
- **Abr/2022:** "Com a vitória do Macron na França e o apoio popular na Alemanha para mais sanções econômicas, acreditamos que um embargo às compras de gás e petróleo da Rússia será aprovado em breve" — reforço do short EUR.
- **Ago/2022:** "a alta dos preços de energia na Europa vem causando uma forte reação fiscal dos governos e, consequentemente, uma postura mais dura do ECB" — nota que o diferencial de política começa a se estreitar, mas o short EUR é mantido.
- **Dez/2022:** posição finalmente zerada — "Zeramos posição vendida no euro e comprada no franco suíço" — encerrando a tese após ~11 meses, coincidindo com a estabilização parcial do quadro energético europeu.

## 4.3 EM Importador de Energia/Déficit Externo como Elo Mais Fraco em Choques de Commodities

**O que é:** Dentro da narrativa geral de escassez global de commodities, a Kapitalo vende moedas de EM asiáticos com vulnerabilidades estruturais de conta corrente e forte dependência de importação de energia, na visão de que um choque global de preços de energia/commodities piora desproporcionalmente suas contas externas e prêmio de risco cambial em relação a exportadores de commodities.

**Variáveis-chave:**
- Dependência de importação de energia/commodities
- Saldo em conta corrente
- Exposição a cadeias de suprimento afetadas por guerra/lockdowns

**Como a Kapitalo aplicou:**
- **Abr/2022** (lockdowns em Xangai): "Adicionamos posições vendidas no yuan chinês, no rupee indiano e no baht tailandês contra o dólar."
- **Mai-Jun/2022:** posições mantidas ("Mantivemos as posições vendidas no peso colombiano, no rupee indiano, no baht tailandês e no euro contra o dólar").
- **Set/2022:** THB zerado, INR mantido — reavaliação seletiva dentro do grupo, não uma tese binária de "toda a Ásia EM".

## 4.4 China: Política Doméstica (Covid-Zero, Crédito Imobiliário, Consolidação Política) como Driver de EM/Commodities

**O que é:** As escolhas de política doméstica chinesa — restrições de mobilidade da política covid-zero, postura regulatória/creditícia sobre o setor imobiliário, e (a partir de outubro/2022) a consolidação política em torno de Xi Jinping — são tratadas como canal primário de transmissão para a demanda global de commodities, moedas EM da Ásia e, na direção oposta, para um rali amplo de FX/metais quando a política se afrouxa.

**Variáveis-chave:**
- Casos de Covid e restrições de mobilidade
- Estímulos monetários/fiscais chineses
- Crédito para o setor de construção/imobiliário
- Composição política do Politburo/Congresso do PCC

**Como a Kapitalo aplicou:**
- **Mar-Abr/2022:** "uma nova onda de casos de COVID na China vem afetando bastante a mobilidade do país... a sua manutenção deve gerar custos econômicos significativos" — CNY short adicionado (ver 4.3) diretamente ligado a este contexto.
- **Mai/2022:** "Na China, os casos de COVID caíram e Shanghai reabriu boa parte dos negócios locais... A moeda parou de depreciar contra a cesta e a bolsa subiu 4,5% no mês."
- **Set/2021:** primeira menção da tese via imobiliário — "Os problemas financeiros enfrentados por uma das maiores empresas de construção elevaram os custos de financiamento de todo o setor... vemos efeitos relevantes na economia real." Conclusão operacional: "Nossa carteira continua com alocações compradas nos mercados de energia, tomada nos mercados de juros, e com alocações defensivas em ativos relacionados à China" (ZAR, COP, CNY vendidos).
- **Out/2022:** "O Congresso do Partido Comunista Chinês reconduziu Xi Jinping para um terceiro mandato... A consolidação de poder em torno de Xi sugere um distanciamento das políticas pró-mercado" — reclassificação do risco chinês como estrutural, não apenas cíclico.
- **Nov/2022:** reversão — "Os sinais de que estamos entrando na fase final do ciclo de aperto monetário e a melhor expectativa de reabertura da economia chinesa produziram uma alta substancial nos ativos de risco. As bolsas da China, as commodities metálicas e as moedas de países emergentes foram os maiores beneficiários deste movimento."

## 4.5 Choque Geopolítico de Oferta (Ormuz) e Resposta Assimétrica de Política Monetária Conforme Ponto de Partida do Ciclo

**O que é:** Um choque negativo de oferta (fechamento do Estreito de Ormuz, colapso do fluxo de petróleo) cria um dilema de política monetária — alta de preços de energia empurra a inflação para cima, mas reduz a atividade. A prescrição "correta" é reagir de forma gradual, desde que expectativas de inflação de longo prazo permaneçam ancoradas — mas a resposta observada diverge conforme o "ponto de partida" cíclico de cada país: bancos centrais já em ambiente de atividade forte/inflação elevada reagem de forma mais pró-ativa (alta de juros); os em posição mais equilibrada apenas endurecem o discurso. Este framework, majoritariamente de juros, organiza os diferenciais de política monetária que alimentam diretamente o arcabouço cambial (carry/diferencial, ver 3.1).

**Variáveis-chave:**
- Grau de fechamento do Estreito de Ormuz / fluxo de petroleiros
- Estado cíclico inicial de cada economia (hiato do produto, inflação corrente, juros vs. neutro)
- Ancoragem das expectativas de inflação de longo prazo

**Como a Kapitalo aplicou:**
- **Mar/2026:** "Choques negativos de oferta criam um dilema para a condução da política monetária... Teoricamente, as autoridades monetárias devem reagir de forma gradual ou mesmo não reagir." Contraste com 2022: "a situação atual é distinta, já que os países se encontram em posição cíclica mais equilibrada, juros próximos ao neutro e com inflação corrente baixa."
- **Abr/2026:** confirmação empírica — "Bancos centrais como o RBA, da Austrália, e o Norges Bank, da Noruega, que já se encontravam diante de um cenário de atividade forte e inflação elevada, foram mais pró-ativos e subiram as taxas de juros. Por outro lado, bancos centrais que se encontravam diante de uma economia mais equilibrada endureceram o discurso, mas deixaram claro que podem subir as taxas de juros caso não haja normalização nos preços do petróleo."

---

# 5. Ciclos de Juros Cross-Country e Vulnerabilidade Doméstica

## 5.1 EM "Adiantado" vs. DM no Timing do Ciclo de Juros

**O que é:** Bancos centrais de emergentes (Brasil, Chile, República Tcheca, Polônia, Hungria) são tratados como tendo iniciado seus ciclos de aperto muito antes dos desenvolvidos, chegando a (ou perto de) uma taxa terminal mais cedo apesar da inflação ainda elevada. Informa tanto posições de juros locais (aposta sobre se o mercado precifica corretamente o fim de cada ciclo) quanto, por extensão, o prêmio de risco cambial: um BC de EM que encerra seu ciclo de forma crível é câmbio-positivo; um que aperta menos que a inflação exigiria é câmbio-negativo.

**Variáveis-chave:**
- Timing relativo do ciclo de alta (EM vs. DM)
- "Taxa terminal" precificada vs. crença da Kapitalo
- Confiança do BC na convergência da inflação à meta
- Projeções de inflação de mercado vs. meta

**Como a Kapitalo aplicou:**
- **Mar/2022:** "Os países emergentes estão mais avançados no ciclo de aperto de política monetária... Um exemplo é o Brasil, onde BCB vem dando indícios de que o fim do ciclo de altas está próximo, mesmo com as projeções de inflação do mercado não convergindo à meta no horizonte relevante."
- **Set/2022:** "Bancos Centrais de algumas economias emergentes estão encerrando o ciclo de aumento de juros, como é o caso do Brasil, República Tcheca e Hungria. A inflação e a atividade desses países seguem elevadas, mas os Bancos Centrais têm demonstrado uma atípica confiança da convergência da inflação à meta." Livro de moedas positivo (+1,53%) no mesmo mês em que o de juros era negativo — consistente com um split EM-câmbio-positivo/EM-duration-cauteloso.

## 5.2 Posição Gêmea Câmbio + Juros Locais para Expressar a Mesma Tese de País

**O que é:** Padrão estrutural (não enunciado como regra, mas consistentemente observado) em que a Kapitalo pareia uma posição cambial contra USD com uma posição de juros locais do mesmo país para expressar uma única tese direcional — vendido numa moeda + tomado em juros locais (ambas expressando "a postura monetária/fiscal deste país ainda não é crível o bastante"), ou comprado na moeda + aplicado em juros (ambas expressando "o ciclo deste país está encerrado e crível").

**Variáveis-chave:**
- Direção da moeda vs. USD
- Direção da posição de juros locais (tomado = aposta de alta adicional; aplicado = aposta de fim de ciclo/corte)
- Consistência direcional entre os dois livros para o mesmo país

**Como a Kapitalo aplicou:**
- **Jan-Fev/2022** (África do Sul): vendido no rand + tomado no juro longo sul-africano — bearish ZAR pareado com aposta de que os juros da África do Sul precisam subir mais.
- **Fev-Set/2022** (Polônia): tomado em juros da Polônia (fev), depois vendido no zloty (jul) — mesma tese expressa em dois livros com defasagem temporal.
- **Abr-Dez/2022** (Chile): tomada em inclinação do Chile (abr, mantida o ano) + vendida no peso chileno (ago) — tese bearish-CLP/steepener de longa duração.
- **Set-Nov/2022** (Brasil): aplicada em inflação do Brasil (set) seguida de comprada no real (out) — tentativa de capturar fim do ciclo de alta + resolução da incerteza eleitoral, revertida em novembro quando o risco político doméstico passou a dominar (ver 6.2).

## 5.3 Vulnerabilidade Institucional de Países Emergentes a Choques de Inflação (Credibilidade e Indexação)

**O que é:** Framework teórico geral: ambiente institucional frágil, menor credibilidade do banco central, maior indexação de preços/salários e economia menos flexível transformam choques temporários de inflação em processos mais duradouros em países emergentes, forçando bancos centrais de EM a apertar mais e mais rápido do que seus pares desenvolvidos — com efeitos diretos sobre a moeda (perda de credibilidade pressiona; aperto mais agressivo dá suporte de carry, às custas de maior volatilidade).

**Variáveis-chave:**
- Credibilidade do banco central / ambiente institucional
- Grau de indexação de preços e salários
- Ritmo e magnitude do aperto monetário (bps por reunião)

**Como a Kapitalo aplicou:**
- **Out/2021:** "O ambiente institucional frágil, a menor credibilidade, a maior indexação e a economia menos flexível são condições bastante propícias para que um choque temporário se torne um processo mais duradouro." Exemplos concretos: Chile subiu a taxa em 125bps, Rússia surpreendeu com alta de 75bps, Colômbia acelerou de 25 para 50bps, e o Bacen acelerou de 100 para 150bps.
- **Out/2021** (contraste DM): "Os Bancos Centrais de países desenvolvidos, por contarem com um melhor arcabouço institucional e com maior credibilidade, têm o privilégio de poderem coletar mais informações antes de agir" — justificou por que Canadá e Austrália só começaram a apertar tardiamente, informando diretamente posições vendidas/defensivas em ZAR, COP, CLP, CNY nesse período.

## 5.4 Estrutura de Dívida das Famílias (Taxa Pós-Fixada) como Acelerador da Transmissão do Aperto Monetário

**O que é:** Cesta persistente contra o dólar: comprar moedas de economias mais resilientes ao aperto monetário global e vender moedas de economias cuja estrutura de endividamento das famílias (hipotecas/crédito pós-fixado) amplifica e acelera a transmissão da política monetária para a economia real, tornando-as mais vulneráveis a uma desaceleração abrupta.

**Variáveis-chave:**
- Estrutura de dívida das famílias (proporção pós-fixada/hipotecas de taxa flutuante)
- Estágio do ciclo de aperto monetário de cada país
- Mercado de trabalho e vendas no varejo por país

**Como a Kapitalo aplicou:**
- **Jan-Ago/2023:** cesta praticamente inalterada — vendidos dólar neozelandês e libra esterlina; comprados dólar australiano e peso mexicano contra USD.
- **Jun/2023:** explicitação do mecanismo — "em países com elevado endividamento das famílias e com taxas de empréstimos pós-fixadas, como é o caso de Canadá, Reino Unido, Nova Zelândia e Suécia, a transmissão de política monetária para a economia real tende a ser ainda mais célere e potente."
- **Nov/2023:** zeraram a posição vendida em dólar neozelandês, sinalizando reavaliação dessa perna à medida que o ciclo global amadurecia.

## 5.5 Juro Real vs. Taxa Neutra (r*) como Termômetro do Aperto Monetário Global

**O que é:** Framework quantitativo (baseado em estimativas do Fed/Dallas Fed) que mede o quão restritiva está a política monetária americana comparando a taxa real de curto prazo com estimativas da taxa neutra. Serve como termômetro do ciclo global — quando aponta território muito restritivo, reforça a tese de desaceleração global que embasa tanto o livro de juros quanto, indiretamente, a visão de câmbio (moedas de economias mais vulneráveis ao aperto tendem a sofrer mais, ver 5.4).

**Variáveis-chave:**
- Taxa real de 3 meses dos EUA
- Estimativas da taxa neutra (Fed/Dallas Fed)
- Indicadores de atividade (vendas no varejo, construção, produção manufatureira)

**Como a Kapitalo aplicou:**
- **Jun/2023:** "As estimativas do Federal Reserve e os nossos modelos indicam que os juros reais estão em território bastante restritivo... Há também sinais de impacto na atividade econômica, como a queda das vendas do varejo, a desaceleração no setor de construção e a queda da produção manufatureira" — usado para justificar manutenção do viés aplicado em juros e do viés vendido nas moedas mais vulneráveis (Framework 5.4).

## 5.6 Indicadores de Folga do Mercado de Trabalho Americano (JOLTS, Poupança Excedente) como Sinal do Ciclo do Fed

**O que é:** Métricas específicas do mercado de trabalho americano — razão entre vagas em aberto e desempregados (JOLTS) e excesso de poupança acumulado na pandemia — usadas como indicadores avançados de quando a política monetária vai finalmente desacelerar a economia americana, informando diretamente a visão sobre a trajetória do Fed e, por consequência, a força do dólar.

**Variáveis-chave:**
- Razão vagas em aberto/desempregados (JOLTS)
- Excesso de poupança das famílias
- Retomada dos pagamentos de crédito estudantil
- Déficit fiscal e espaço para estímulo anticíclico

**Como a Kapitalo aplicou:**
- **Ago/2023:** "A razão de vagas em aberto sobre desempregados, uma métrica mais ampla de aperto do mercado de trabalho, vem corrigindo. Além disso, o excesso de poupança acumulado durante a pandemia está próximo à exaustão e o retorno do pagamento dos créditos estudantis devem impactar negativamente o consumo à frente" — usado para questionar a resiliência americana e sustentar viés de desaceleração global que baliza a cesta cambial (long AUD/NOK/MXN/BRL vs. short NZD/CNY/GBP).

## 5.7 Seleção Cross-Country por Estágio do Ciclo Econômico ("Países Mais Avançados no Ciclo")

**O que é:** Heurística recorrente e cross-asset para selecionar países onde alocar posições aplicadas (long duration): busca por países cujo ciclo de afrouxamento está mais avançado — evidenciado por arrefecimento do mercado de trabalho, desaceleração salarial e queda de inflação — argumentando que o mercado ainda subprecifica cortes adicionais. Primariamente uma tese de juros, mas alimenta o livro de moedas quando o diferencial de política é usado para justificar posições cambiais no mesmo país.

**Variáveis-chave:**
- Hiato do mercado de trabalho / taxa de desemprego
- Trajetória de salários nominais e de inflação
- Precificação de cortes futuros pela curva vs. avaliação própria da Kapitalo
- Estágio do ciclo de afrouxamento por banco central

**Como a Kapitalo aplicou:**
- **Jul/2025:** "temos buscado, de forma seletiva, posições aplicadas em juros onde os sinais de abertura do hiato econômico são mais evidentes. A combinação de: (1) arrefecimento do mercado de trabalho; (2) desaceleração dos salários; e (3) trajetória de queda da inflação não nos parece compatível com juros terminais próximos ao nível neutro. Mantemos, portanto, posições aplicadas em Canadá e Suécia."
- **Abr/2025:** ligação direta ao livro de moedas — compra de dólar canadense e dólar australiano contra o renminbi, coincidindo com posições aplicadas em juros nesses mesmos países.
- **Nov-Dez/2025:** extensão do critério ao Brasil e à África do Sul — "o gradual afrouxamento do mercado de trabalho, a inflação benigna e a queda das expectativas de inflação devem permitir o início de um ciclo de recalibragem dos juros já na reunião de janeiro."

## 5.8 Ciclo Doméstico do BCB (Recalibragem) como Termômetro do Real

**O que é:** Aplicação mais recente (2026) do framework de ciclo de juros ao próprio real: quando o BCB sinaliza início de um ciclo de "recalibragem" (corte de juros) apoiado em melhora genuína da inflação e desaceleração da atividade, isso é lido como ambiente favorável ao real; quando o crescimento/emprego aceleram, o governo anuncia estímulo fiscal adicional e a inflação/expectativas voltam a subir, as condições para a continuidade do corte "se exaurem" — sinal de deterioração do ambiente doméstico.

**Variáveis-chave:**
- Sinalização do BCB sobre início/continuidade da recalibragem
- Trajetória da inflação corrente e das expectativas
- Crescimento e geração de emprego domésticos
- Anúncios de estímulo fiscal do governo

**Como a Kapitalo aplicou:**
- **Jan/2026:** "No Brasil, o Banco Central reconheceu a melhora da inflação e a desaceleração da economia, passando então a sinalizar o início de um ciclo de recalibragem da política monetária na reunião de março." Adicionaram compra de real contra o dólar no mesmo mês.
- **Mai/2026:** reversão do diagnóstico — "No Brasil, as condições para o prosseguimento do ciclo de recalibragem monetária estão se exaurindo. O crescimento e a geração de emprego aceleraram, o governo segue anunciando medidas de estímulo fiscal, a inflação piorou nos últimos meses e as expectativas de inflação seguem subindo." Ação tomada no livro de juros (redução de posições aplicadas), mesmo bloco de variáveis que historicamente informa a visão de câmbio da casa.

---

# 6. Brasil: Risco Fiscal, Credibilidade e o Real

## 6.1 Risco Fiscal/Político Doméstico como Termômetro do Real

**O que é:** Tratamento do real como caso especial dentro do livro EM, no qual o trade-off entre avanço da agenda de reformas/ajuste fiscal (bearish se travar) e recuperação cíclica/contas externas (bullish) determina a direção da exposição — às vezes levando a posições contrárias à tese geral de risco global (ver 3.6). Formalizado a partir de 2021 como um cluster próprio (deterioração fiscal, fragilidade política, governança), com possibilidade explícita de evoluir para "dominância fiscal".

**Variáveis-chave:**
- Avanço/travamento da agenda de reformas fiscais e ajuste de gastos
- Percepção de risco fiscal (prêmio de risco Brasil)
- Recuperação cíclica doméstica e contas externas
- Discussão de "dominância fiscal"

**Como a Kapitalo aplicou:**
- **Set/2020:** "No Brasil, o desafio fiscal é muito grande e os mercados começaram a sinalizar que o governo não pode parar com os ajustes de gastos e reformas estruturais. Em paralelo, a recuperação cíclica e as contas externas estão melhores que o esperado" — explicitação do trade-off entre risco fiscal (negativo) e ciclo/externo (positivo).
- **Mar/2021:** "O imbróglio do orçamento de 2021 evidencia a frágil articulação política do governo e indica que dificilmente teremos a aprovação de reformas econômicas estruturantes no atual mandato presidencial." Ação: "Adicionamos uma posição comprada em dólar americano contra o real."
- **Abr/2021:** mantida a venda de real; adicionaram "uma posição comprada em inflação implícita longa no Brasil" como hedge complementar (depreciação alimentando inflação).
- **Ago/2021:** reafirmação isolada do tema mesmo com pano de fundo externo favorável: "Esta conjuntura de baixo juros internacionais e elevados preços de commodities é bastante favorável às economias emergentes. Contudo, não estamos otimistas com os ativos brasileiros, pois os desafios internos – deterioração fiscal e governança – não estão sendo endereçados."
- **Out/2021:** desenvolvimento mais completo do ano — "O Brasil é um dos casos mais emblemáticos, pois também convive com uma instabilidade política, tem um elevado nível de endividamento e, recentemente, flexibilizou a âncora fiscal, reascendendo as discussões, em cenário limite, sobre dominância fiscal." Posições: real vendido + CDS do Brasil comprado (dupla expressão da mesma tese).

## 6.2 "Twin-Deficit Override": Risco Fiscal-Político Domina Mesmo com Fundamentos Externos Saudáveis (Eleição Lula, 2022)

**O que é:** A partir de out/2022, a Kapitalo desenvolve um framework explícito no qual reconhecem que as contas externas e a trajetória de desinflação do Brasil são objetivamente sólidas, mas argumentam que o risco fiscal/político doméstico (o programa econômico do governo entrante) pode dominar e sobrepor esses fundamentos, podendo gerar uma "crise de confiança" que atinge os ativos locais (câmbio incluído) de forma aguda independentemente do pano de fundo externo.

**Variáveis-chave:**
- Resultado eleitoral e composição do Congresso
- Plano econômico (macro e micro) do novo governo
- Balanço externo (saudável ou não)
- Risco de "crise de confiança" (ruptura súbita de credibilidade fiscal)

**Como a Kapitalo aplicou:**
- **Out/2022:** "Lula foi eleito presidente em uma disputa acirrada e com uma composição desfavorável no Congresso. A situação fiscal segue sendo um grande problema e o cenário global adverso deixam pouca margem de manobra para medidas menos ortodoxas." Ação: "Adicionamos uma posição comprada no real" — aposta inicial e ainda otimista na resolução da incerteza eleitoral.
- **Nov/2022:** posição já zerada — reversão em apenas um mês, à medida que o risco fiscal ganhou peso na leitura da equipe.
- **Dez/2022** (carta de fechamento do ano, formulação mais explícita): "Tudo indica que o novo governo acredita em fórmulas econômicas que já se provaram erradas no passado, e pode deixar passar outra oportunidade. Começamos a ver a maturação das importantes reformas implementadas nos últimos anos; nosso balanço externo é saudável; e a desaceleração cíclica com melhora nos indicadores de inflação são fatores bem-vindos. Por outro lado, o plano econômico (macro e micro) que está sendo proposto é inadequado e pode colocar tudo a perder... se formos nessa direção corremos o risco de termos uma crise de confiança com piora aguda dos ativos locais nos próximos anos."

## 6.3 Arcabouço Fiscal e Catalisadores Político-Institucionais como Determinantes do Prêmio de Risco (2023, Virada Positiva)

**O que é:** Continuação direta do Framework 6.2 em 2023: a trajetória da nova regra fiscal ("arcabouço fiscal"), a postura do Congresso em relação às reformas, e ataques/pressões políticas sobre o Banco Central e a meta de inflação são tratados como os principais determinantes do prêmio de risco embutido nos ativos brasileiros. A incerteza fiscal trava o real no início do ano; conforme a regra é aprovada e o Congresso resiste a desmontar reformas anteriores, o prêmio de risco cai e o real passa a ser comprado.

**Variáveis-chave:**
- Desenho e aprovação do arcabouço fiscal
- Comportamento do Congresso em relação a reformas e à meta de inflação
- Ataques políticos ao Banco Central
- Expectativas de inflação de longo prazo (Focus) e inflação implícita

**Como a Kapitalo aplicou:**
- **Jan/2023:** "a indefinição sobre a nova regra fiscal e a possibilidade de mudança de meta de inflação seguem impactando as expectativas de inflação de longo prazo" — cautela, sem posição comprada em BRL.
- **Fev/2023:** "a discussão sobre a meta de inflação no atual momento é contraproducente e os ataques ao Banco Central podem enfraquecer a instituição... não há ainda um plano crível de ajuste das contas públicas."
- **Mar/2023:** primeiro sinal de virada — "o governo apresentou o arcabouço fiscal que na prática gera um ajuste muito gradual e dependente do aumento de carga tributária, mas pelo menos sinaliza alguma preocupação com o controle das contas públicas."
- **Mai/2023** (gatilho de entrada): "a aprovação do arcabouço fiscal, a derrubada de trechos do decreto do saneamento, mensagens moderadoras vindas do Congresso e, principalmente, a inflexão no cenário prospectivo de inflação... Adicionamos posições que tendem a se beneficiar desse cenário: compramos o real contra o dólar, a bolsa e aplicamos juros reais."
- **Jun/2023** (retrospectiva): "Víamos de forma bastante negativa os sinais da política econômica do novo governo, principalmente na dimensão fiscal... O desenrolar do arcabouço fiscal, um Congresso resistente em desfazer as reformas dos governos anteriores e, posteriormente, o cenário mais benigno do que o esperado para a inflação foram os gatilhos para montarmos posições compradas em ativos locais."

## 6.4 Valuation Descontado + Posicionamento Técnico como Gatilho de Entrada

**O que é:** Complementar ao Framework 6.3 — mesmo com viés fundamentalmente negativo sobre a política fiscal, os modelos internos indicavam que juros, bolsa e câmbio brasileiros estavam "baratos" e com posicionamento técnico favorável, o que permitiu manter opcionalidade para comprar rapidamente assim que os catalisadores (fiscais/políticos) se confirmassem — um framework de "preço e posição antes do catalisador".

**Variáveis-chave:**
- Preço relativo (valuation) de juros, bolsa e câmbio brasileiros vs. histórico/pares
- Posicionamento técnico do mercado (crowding)
- Catalisadores esperados

**Como a Kapitalo aplicou:**
- **Jun/2023:** "Começamos o ano com baixa convicção e poucas alocações em ativos locais... Por outro lado, nossos modelos mostravam que os ativos locais – juros, bolsa e moeda – apresentavam preços bastante descontados e uma posição técnica atrativa."

## 6.5 Ancoragem do Câmbio e das Expectativas como Validação da Credibilidade

**O que é:** A estabilidade da taxa de câmbio e das expectativas de inflação implícitas — mesmo diante de choques negativos pontuais (depreciação cambial, alta de combustíveis, ruído de comunicação do BC) — é usada como evidência de que a credibilidade da política monetária/fiscal doméstica está se consolidando. Quando câmbio e implícitas permanecem "comportados" apesar de más notícias, isso é lido como sinal estrutural positivo.

**Variáveis-chave:**
- Nível e volatilidade implícita do câmbio
- Inflação implícita de mercado (breakevens)
- Preço de combustíveis e pass-through cambial
- Comunicação do Banco Central

**Como a Kapitalo aplicou:**
- **Set/2023:** "As inflações implícitas estão contidas apesar da desvalorização do câmbio e alta dos combustíveis" — evidência de ancoragem mesmo em mês de reprecificação global de juros longos.
- **Out/2023:** "os dados de inflação corrente vêm surpreendendo positivamente, as inflações implícitas de mercado vêm caindo, o prêmio de risco dos ativos brasileiros vem caindo e a taxa de câmbio continua bastante comportada, com queda das volatilidades implícitas." Nota-se, porém, que adicionaram uma posição tática vendida no real no mesmo mês (contágio de juros longos dos EUA) — a tese de ancoragem conviveu com hedge tático de curto prazo.

## 6.6 Crise de Credibilidade da Âncora Fiscal (2024) e Repasse Cambial à Inflação

**O que é:** A partir de meados de 2024, o framework central para o real deixa de ser cíclico/externo e volta a ser doméstico-político: a perda de credibilidade do arcabouço fiscal (não cumprimento de metas de gasto, pacote fiscal frustrante) gera desancoragem das expectativas de inflação de longo prazo, eleva o prêmio de risco e força o BC a apertar mais os juros. A depreciação cambial resultante é tratada como um dos inputs diretos da dinâmica prospectiva de inflação, criando um ciclo de retroalimentação câmbio–inflação–juros; em situações extremas, isso se manifesta em venda de reservas cambiais pelo BC como termômetro de estresse.

**Variáveis-chave:**
- Crescimento da despesa real vs. teto do arcabouço fiscal
- Metas de déficit primário
- Percepção sobre a leniência da nova diretoria do BCB
- Expectativas de inflação de longo prazo vs. centro da meta
- Venda de reservas cambiais pelo BC (proxy de saída de capital/estresse)

**Como a Kapitalo aplicou:**
- **Jun/2024:** "A credibilidade do Novo Arcabouço fiscal, que limita o crescimento dos gastos, começou a ser testada sem uma resposta contundente do governo... Os questionamentos sobre o compromisso do governo com o arcabouço fiscal, a leve piora das contas externas e a percepção de que o novo Banco Central será leniente com a inflação aumentaram de forma aguda o prêmio de risco dos ativos brasileiros. Vemos esse prêmio como excessivo" — mesmo assim, aumentaram exposição em Brasil via bolsa/juros reais, apostando que o prêmio já compensava os riscos (ver 6.8).
- **Jun/2024:** "Uma depreciação do câmbio, nesse ambiente, alimenta o risco da dinâmica futura da inflação, justamente quando há uma crescente percepção de que a nova diretoria do Banco Central será mais leniente com a estabilidade de preços."
- **Jul/2024:** "há elementos que tendem a piorar a dinâmica inflacionária prospectiva: a atividade forte, o mercado de trabalho apertado, os expressivos ganhos de renda real, a desvalorização cambial e o aumento das expectativas mais longas de inflação."
- **Nov/2024:** "Na falta de uma âncora fiscal, o real vem depreciando bem mais do que os pares e as expectativas de inflação mais longas vem se distanciando ainda mais da meta."
- **Dez/2024:** "houve uma saída recorde de recursos do país em dezembro, levando o Banco Central a vender USD 21,7 bilhões de reservas cambiais" — citado junto com alta de 1,0 p.p. na Selic como evidência da severidade da crise. Sobre o carrego: "praticamente dois anos nos separam da eleição presidencial. Há muita incerteza envolvida e o custo de carregamento é elevado, dificultando apostas mais otimistas neste momento."

## 6.7 Dominância Fiscal e Múltiplos Prêmios de Risco Subestimados (2025)

**O que é:** Evolução de 2025 do Framework 6.6: uma política fiscal expansionista (transferências de renda financiadas por aumento de carga tributária) obriga o BC a manter política monetária muito contracionista — um "policy mix" que eleva o prêmio de risco exigido pelos investidores e pressiona câmbio, juros e bolsa locais simultaneamente. Revisitado no fim do ano tratando o câmbio como um de vários prêmios de risco (junto com inflação implícita, spreads de crédito e equity risk premium) que deveriam refletir o risco de continuidade da política atual, à luz das eleições de 2026.

**Variáveis-chave:**
- Trajetória da dívida pública / carga tributária
- Grau de contracionismo monetário vs. expansão fiscal
- Prêmio de risco embutido no câmbio, na inflação implícita, nos spreads de crédito e no equity risk premium
- Probabilidade de alternância de governo nas eleições

**Como a Kapitalo aplicou:**
- **Fev/2025:** montagem de posição vendida no real — "O atual governo deve continuar perseguindo uma política econômica calcada na expansão das transferências de renda financiada com aumento de carga tributária, o que gera uma forte expansão da demanda doméstica e resulta em uma política monetária muito contracionista. Esse policy mix é extremamente desfavorável para os ativos de risco locais... os investidores passam a exigir um maior prêmio de risco dada a insustentabilidade da trajetória fiscal." Ressalva: "As eleições presidenciais de 2026 são o maior risco para esta posição."
- **Dez/2025:** projeção de dívida pública a 84% do PIB até fim de 2026 sob continuidade da política atual; racional de mispricing cross-asset — "os prêmios de risco (câmbio, inflação implícita, spreads de crédito, equity risk premium) são muito baixos e subestimam sobremaneira os riscos de continuidade da atual política econômica. Do outro lado... os juros reais a termo estão baratos e devem sofrer um repricing importante num cenário de alternância de poder. Desta forma, temos concentrado nossas apostas positivas nesse instrumento" — a tese cambial (câmbio "barato" em termos de prêmio de risco) expressa via juros reais, não posição direta em BRL neste momento específico.

## 6.8 Posicionamento Técnico Extremo como Sinal Contrário de Valuation

**O que é:** Além dos fundamentos (fiscal, prêmio de risco), o grau de posicionamento técnico do mercado é usado como input adicional e independente para avaliar se o prêmio de risco embutido no ativo está justificado ou excessivo — posicionamento extremo (mercado já muito vendido/pessimista) é lido como suporte para uma posição contrária.

**Variáveis-chave:**
- Posicionamento técnico do mercado (extremo vs. neutro)
- Retorno esperado do ativo dado o prêmio de risco

**Como a Kapitalo aplicou:**
- **Jun/2024:** "Acreditamos que o retorno esperado dos ativos e o posicionamento técnico extremo compensam os riscos acima citados" — usado para justificar manutenção/aumento de exposição em ativos brasileiros (bolsa e juros reais) apesar da crise de credibilidade fiscal em curso (ver 6.6).

---

# 7. Transições Políticas em Mercados Emergentes como Catalisador de Repricing (Fora do Brasil)

## 7.1 Mudança de Governo Populista→Ortodoxo como Catalisador de Compressão do Prêmio de Risco

**O que é:** Framework comparativo aplicado a países emergentes com governos de esquerda populista fiscalmente deteriorados, alta probabilidade de troca de governo e prêmio de risco elevado: a expectativa de eleição de um governo de centro-direita fiscalista deve gerar compressão relevante dos prêmios de risco (câmbio, CDS, juros). A qualidade do financiamento externo (conta corrente financiada por IED vs. fluxos de portfólio) é usada como filtro de vulnerabilidade cambial. A Kapitalo usa explicitamente dois precedentes latino-americanos como template analógico para calibrar a magnitude do "delta" de repreciação: o impeachment de Dilma Rousseff no Brasil (2016) e a eleição de Javier Milei na Argentina (2023).

**Variáveis-chave:**
- Popularidade do governo incumbente vs. histórico de reeleição na América Latina
- Déficit fiscal e trajetória de gasto público (% do PIB)
- CDS 5 anos, yield de bonds soberanos
- Composição de financiamento do déficit em conta corrente (IED vs. portfólio)
- Espaço fiscal disponível para ajuste (carga tributária, subsídios, folha)

**Como a Kapitalo aplicou:**
- **Jun/2025** (Colômbia, tese central do mês): "A conjuntura atual se assemelha muito a do Brasil de 2015-16: governo de esquerda impopular, considerável probabilidade de troca de governo, desequilíbrio fiscal crescente e elevado prêmio de risco nos ativos locais." Dados: gasto do Governo Central de 21% para 24% do PIB (2022-24), déficit nominal de 7,1% do PIB em 2024, suspensão da regra fiscal, rebaixamento de rating. Qualidade do financiamento externo destacada: "o déficit em conta corrente está baixo e sendo totalmente financiado pelo FDI."
- **Ago-Set/2025** (Argentina, mesmo framework em contexto de ajuste já em curso): CDS de 5 anos sobe ~500 pontos após derrota eleitoral provincial — "Houve uma queda expressiva nos preços dos ativos locais e o CDS de 5 anos subiu 500 pontos, refletindo alta probabilidade de default da dívida soberana." Set/2025: "câmbio apreciado e o baixo nível de reservas" como fragilidades a serem endereçadas pós-eleição.
- **Out/2025** (Argentina, catalisador confirmado): "Uma vitória dessa magnitude indica alta aprovação do governo, baixo risco de retorno do kirchnerismo e aumento da probabilidade de reeleição em 2027. Essa combinação reduziu a incerteza no horizonte de investimentos e produziu uma alta substancial nos ativos." Fundo manteve/aumentou posições em ações e dívida externa argentina, e adicionou posição comprada no peso chileno (mesmo padrão de transição política).
- **Mai/2026** (atualização da tese colombiana): candidato de direita à frente por ~3 p.p. no 1º turno; ajuste fiscal de 4% do PIB julgado factível. Conclusão: "A guinada na política econômica colombiana tem o potencial de se comparar às mudanças implementadas após o impeachment de Dilma Rousseff, no Brasil, em 2016, e pela eleição de Javier Milei, na Argentina em 2023. Se formos por esse caminho, a correção do desequilíbrio fiscal implicará em uma redução significativa no prêmio de risco nos ativos colombianos ao longo dos próximos anos" (apresentado como research/monitoramento; nenhuma posição em peso colombiano explicitada nesta carta).

## 7.2 Liberalização Cambial e Controle de Capitais como Gatilho de Fluxo (Bandas Cambiais Argentinas)

**O que é:** Framework específico sobre o regime cambial argentino: a manutenção de bandas cambiais e controles de capital ("cepo") limita o acúmulo de reservas e mantém o país fora dos índices globais; a liberalização gradual do câmbio (facilitada por acordos com FMI/Tesouro dos EUA) é vista como o principal catalisador para destravar fluxos de capital estrangeiro, permitir emissão de dívida externa, viabilizar inclusão em índices globais de ações/bonds e permitir acúmulo de reservas — elementos que juntos sustentam uma tese de reprecificação de ativos locais.

**Variáveis-chave:**
- Nível de reservas internacionais do Banco Central
- Distância do peso ao teto/piso da banda cambial
- Grau de controle de capitais (fluxo restrito vs. livre)
- Apoio de organismos internacionais (FMI, Tesouro dos EUA)
- Elegibilidade a índices globais de ações e títulos públicos

**Como a Kapitalo aplicou:**
- **Ago/2025:** "acordo com o FMI [que] permitiu o aumento das reservas internacionais e foi acompanhado pela flexibilização de grande parte do mercado cambial" como pano de fundo para reabrir posições em crédito e ações argentinas.
- **Set/2025:** estresse do regime — "O peso argentino se desvalorizou e atingiu o teto da banda cambial, exigindo vendas expressivas de reservas pelo Tesouro e pelo Banco Central", com o Tesouro americano sinalizando apoio incondicional.
- **Out/2025** (pós-eleição, formulação mais prospectiva): "o regime de flutuação cambial regido por bandas e o fluxo restrito de capitais seguem em vigor, mas devem ser flexibilizados conjuntamente ao longo dos próximos meses. Entendemos que esse processo deve destravar os fluxos globais de capitais... permitir a inclusão da Argentina nos índices globais de ações e de títulos públicos, permitir a emissão de dívida externa... e traduzir-se em um acúmulo de reservas por parte do Banco Central."

---

# 8. Ouro, Debasement Fiscal-Monetário e o Status de Reserva do Dólar

## 8.1 Ouro como Ativo-Moeda Alternativo em Cenário de Debasement Fiscal-Monetário

**O que é:** Framework de longo prazo sobre o próprio sistema de moeda fiduciária: com bancos centrais comprando ativos em massa, taxas reais negativas e debate sobre MMT (financiamento ilimitado de déficits via emissão de dívida), o ouro readquire relevância como reserva de valor alternativa a moedas fiduciárias — e, por extensão, moedas de países com instituições mais fracas (tipicamente EM) são vistas como mais vulneráveis a uma eventual perda de confiança/desancoragem inflacionária.

**Variáveis-chave:**
- % de reservas de bancos centrais em ouro (EM vs. DM)
- Juros reais de títulos soberanos
- Percentual de títulos investment-grade com juros nominais negativos
- Qualidade institucional/credibilidade fiscal-monetária (proxy de vulnerabilidade cambial)

**Como a Kapitalo aplicou:**
- **Abr/2020** (anexo dedicado, "O Ouro como Alternativa de Investimento"): "cerca de 20% dos títulos com grau de investimento do mundo estão com taxas de juros nominais negativas... o debate sobre a validade da Teoria Monetária Moderna (MMT)... já é comum em vários países." Conclusão direta para câmbio: "acreditamos que moedas de países emergentes, com instituições menos sólidas, serão mais vulneráveis" a uma eventual perda de controle da inflação/endividamento.
- **Abr/2020:** citação do World Gold Council: "Gold is the only reserve asset that bears no political or credit risk, nor can it be devalued by the printing presses or extraordinary monetary policy measures."
- **Abr/2020** (tese qualificada, não uma convicção definitiva): "o ouro pode ser um candidato adequado no caso de uma mudança de regime econômico, como o ocorrido na década de 1970... o endividamento sem precedentes de governos ao redor do mundo acendem uma luz amarela." Posição em ouro mantida de jan/2020 a set/2020, reduzida gradualmente a partir de jul/2020.

## 8.2 Separar Sinal de Ruído: Juros Reais (Não o Dólar) como o Verdadeiro Driver de Câmbio e Ouro

**O que é:** Exercício explícito de "separar ruído de sinal": a narrativa popular de mercado (queda do dólar + alta do ouro = início de debasement/desancoragem inflacionária) é rejeitada como causa principal — o verdadeiro driver é a queda dos juros reais americanos de longo prazo, que reprecifica todos os ativos de risco (câmbio incluído) via valuation.

**Variáveis-chave:**
- Juros reais de títulos americanos de 10 anos
- Movimento do índice dólar (DXY) contra parceiros comerciais
- Preço de metais preciosos

**Como a Kapitalo aplicou:**
- **Jul/2020** (seção "Separando ruído de sinal"): "O dólar americano... caiu contra seus principais parceiros comerciais. Além disso, os metais preciosos tiveram um movimento de alta expressivo. Várias análises colocaram esses dois movimentos como o início de um processo de debasement da moeda americana... não acreditamos que este seja o real motivo... Acreditamos que o verdadeiro sinal vem do mercado de juros. Os juros reais americanos caíram de forma expressiva para os vencimentos longos após a crise do COVID... Os títulos de 10 anos estão com taxa de juros reais de -1% a.a."

## 8.3 Revisão da Tese de Debasement (2026): Sinais Ainda Ausentes + Credibilidade do Fed como Contraponto

**O que é:** Atualização de 2026 do Framework 8.1: a Kapitalo monitora explicitamente se o processo de debasement (perda de valor do numerário via endividamento público e repressão financeira) está de fato em curso, olhando juro real, inflação implícita e o status de reserva do dólar — e conclui que, apesar da tese estrutural, os sinais ainda não se confirmaram. Um evento institucional específico (indicação de um chairman do Fed percebido como "tecnocrata independente") é lido como reforço, não enfraquecimento, da credibilidade monetária americana, atuando como contraponto ao risco de debasement no curto prazo. O mesmo framework conecta a compra de ouro por bancos centrais (acelerada após as sanções às reservas russas em 2022) ao tema de diversificação de reservas para fora do dólar.

**Variáveis-chave:**
- Déficits fiscais e endividamento público (EUA)
- Juro real 5y5y vs. preço do ouro (relação historicamente inversa até 2023)
- Inflação implícita 5y5y vs. juro real 5y5y
- Compras de ouro por bancos centrais como reserva alternativa
- Credibilidade institucional do Fed (independência do chairman)

**Como a Kapitalo aplicou:**
- **Jan/2026** (atualização da tese de 2020): observam que, até 2023, queda do juro real coincidia com alta do ouro, mas que a partir de 2023 as sanções dos EUA às reservas russas aceleraram compras de ouro por bancos centrais como alternativa às reservas em dólar — dissociando o ouro do seu driver tradicional e ligando-o a um driver de "de-dolarização de reservas".
- **Jan/2026** (checagem de sinais): "não vemos sinais nos mercados financeiros de que esse processo de debasement tenha começado. Os investidores seguem se beneficiando de retornos reais positivos nos títulos públicos do governo dos Estados Unidos e a inflação implícita segue com prêmio de risco próximo ao histórico recente. Além disso, o dólar norte-americano segue apreciado em termos históricos e continua representando uma parcela significativa das reservas internacionais dos bancos centrais, sendo ainda a moeda mais utilizada no comércio internacional."
- **Jan/2026** (contraponto institucional): sobre a nomeação de Kevin Warsh — "Warsh é reconhecido como um tecnocrata independente, o que reforça a institucionalidade do Banco Central dos Estados Unidos."
- Posição em ouro reduzida taticamente em jan/2026 e ausente do livro de commodities em abr-mai/2026 — sinal de que a convicção declinou conforme a conclusão de que o debasement "ainda não começou".

---

# 9. Cestas de Moedas: Padrões Recorrentes de Composição de Portfólio

## 9.1 Cesta Pró-Cíclica de Moedas-Commodity/Carry como Expressão de Reflação Global

**O que é:** Em vez de operar uma visão isolada sobre uma única moeda, a Kapitalo expressa sua visão macro central de reabertura/crescimento global comprando um cesto de moedas ligadas a commodities e/ou de alto carry contra o dólar (e ocasionalmente contra o euro) — produtores de commodities, ciclos de juros mais altos, ou países com reabertura adiantada — capturando de forma diversificada o tema de crescimento global forte.

**Variáveis-chave:**
- Ritmo de vacinação/reabertura por país
- Preços de commodities
- Diferencial de juros (carry) entre a moeda-alvo e USD/EUR
- Condições financeiras globais

**Como a Kapitalo aplicou:**
- **Jan/2021:** "Acreditamos que o processo de retomada econômica continua intacto... Aproveitamos para aumentar algumas de nossas alocações com viés otimista." Posições: comprados MXN, CAD, AUD contra USD; adicionaram real e shekel israelense.
- **Ago/2021:** "Esta conjuntura de baixo juros internacionais e elevados preços de commodities é bastante favorável às economias emergentes." Mantidos MXN, RUB, CAD, NOK.
- A cesta é progressivamente desmontada a partir de set-out/2021 conforme o fundo migra para uma postura de dólar comprado outright (ver Framework 3.1).

## 9.2 Cesta de Carry EM (Alto Carrego/Normalização) Financiada Contra Moedas de Funding de Baixo Carrego

**O que é:** Padrão persistente de portfólio: o livro de moedas mantém, na maior parte do tempo, posições compradas em moedas de maior carry ou em processo de estabilização (lira turca, rúpia indiana, peso chileno, rand sul-africano, florim húngaro) financiadas contra o dólar ou, pontualmente, contra o renminbi chinês e o franco suíço (moedas de funding de baixo carry/gerenciadas). A composição da cesta é ajustada mês a mês, mas o padrão estrutural (alto carry/normalização vs. baixo carry) se mantém constante ao longo de vários anos.

**Variáveis-chave:**
- Diferencial de juros entre moeda-alvo e moeda de funding
- Estágio do programa de estabilização/desinflação em cada país-alvo (ex.: Turquia)
- Grau de intervenção cambial da moeda de funding
- Volatilidade implícita e liquidez dos pares

**Como a Kapitalo aplicou:**
- **Mar-Ago/2024:** cesta ampla — vendidos EUR, CNY, GBP; comprados AUD, BRL, e adições pontuais (rúpia indiana, peso mexicano em mai/2024).
- **Ago/2024:** rotação de convicção — "Em moedas, estamos com baixa exposição" e "Adicionamos uma posição comprada na lira turca contra o dólar americano", zerando simultaneamente GBP, EUR e AUD.
- **Jun/2025:** fechamento quase total do padrão clássico de funding CNY/CHF — "Zeramos as posições compradas na lira turca e no euro e as posições vendidas no renminbi chinês e no franco suíço."
- **Jul/2025:** retomada com a cesta migrando para ser expressa quase toda contra o USD — "Adicionamos compra de lira turca, euro e rúpia indiana contra o dólar norte-americano. Zeramos a venda de renminbi chinês contra o dólar norte-americano."
- **Ago-Dez/2025:** cesta long-only contra USD se consolida e expande (iene, lira turca, rúpia indiana mantidos o tempo todo; adições sucessivas de peso chileno, florim húngaro, rand sul-africano).

## 9.3 Exposição Cambial Derivada da Tese sobre o Crédito/Imobiliário Chinês

**O que é:** A desaceleração do mercado imobiliário chinês e a redução do impulso de crédito são tratadas como risco para a demanda global de commodities e para moedas de países cuja economia depende de exportações/comércio com a China. A resposta é montar "alocações defensivas em ativos relacionados à China" — venda do yuan e de moedas de exportadores de commodities/EM (rand, peso colombiano, peso chileno) como hedge, mesmo mantendo posições compradas em commodities específicas por outras razões de oferta.

**Variáveis-chave:**
- Impulso de crédito chinês
- Alavancagem do setor de construção/imobiliário
- Condições de financiamento do setor
- Postura do PBoC

**Como a Kapitalo aplicou:**
- **Mai/2021:** primeira menção do canal de transmissão — "acreditamos que a redução do impulso de crédito na China terá efeitos negativos na demanda de commodities no segundo semestre."
- **Ago/2021:** primeira posição vendida "no yuan chinês contra o dólar", junto com rand e peso colombiano, mesmo mês em que "Apesar da desaceleração da economia Chinesa, ainda vemos um cenário econômico global favorável para os ativos de risco."
- **Set/2021** (desenvolvimento mais extenso, incorporadora em dificuldades financeiras): "Os problemas financeiros enfrentados por uma das maiores empresas de construção elevaram os custos de financiamento de todo o setor... há um risco relevante de uma desaceleração mais pronunciada da atividade econômica." Conclusão operacional: "Nossa carteira continua com alocações compradas nos mercados de energia, tomada nos mercados de juros, e com alocações defensivas em ativos relacionados à China" (ZAR, COP, CNY vendidos, CLP adicionado).
- **Nov-Dez/2021:** desmonte gradual (zeram CLP em nov, ZAR/CNY em dez) sem nova narrativa específica — o tema perde protagonismo à medida que a variante Ômicron e o ciclo do Fed dominam a pauta.

---

## Connections

- [[ppp_balassa_samuelson]] — 2.1–2.2 (valuation por PPP/REER e o efeito Balassa-Samuelson/custo unitário do trabalho, aplicados explicitamente como âncora de realinhamento de longo prazo)
- [[balance_of_payments_approach]] — 2.5 (modelo de câmbio de equilíbrio via posição externa/BOP fair-value aplicado ao Brasil, com projeções numéricas de conta corrente e financiamento via IED)
- [[uip]] — 3.1, 5.1–5.2 (divergência de crescimento/política monetária como driver central; diferencial de juros cross-country)
- [[carry_trade]] — 9.1–9.2 (cestas pró-cíclicas de moedas-commodity e cesta de carry EM financiada contra moedas de funding de baixo carrego, padrão estrutural mantido por vários anos)
- [[risk_premium]] — 6.1, 6.3, 6.8 (risco fiscal-político doméstico como termômetro do Real; posicionamento técnico extremo como sinal contrário de valuation)
- [[fiscal_dominance]] — 6.6–6.7 (crise de credibilidade da âncora fiscal de 2024 e repasse cambial; dominância fiscal e múltiplos prêmios de risco subestimados em 2025)
- [[exchange_rate_pass_through]] — 6.6 (repasse cambial à inflação como consequência direta da crise de credibilidade fiscal de 2024)
- [[currency_regimes]] — 7.1–7.2 (transição de governo populista→ortodoxo como catalisador de repricing; liberalização cambial e bandas cambiais argentinas)
- [[currency_crisis_indicators]] — 7.2 (controle de capitais e bandas cambiais argentinas como gatilho de fluxo, mesmo padrão de saída de regime cambial documentado nesse concept)
- [[kinea_fx_mental_models]] — mesmo gênero de documento (mental model de câmbio de gestora macro brasileira), construído de forma independente sobre a mesma janela temporal; comparar Framework 1.1 (Kapitalo: estilo híbrido fundamentalista+técnico) com o processo de escolha de veículo da Kinea (2.3)
- [[verde_fx_mental_models]] — terceiro documento da mesma família (mental models de câmbio por gestora), útil para contraste de estilo: Kapitalo é multi-ativo global e telegráfico, Verde e Kinea são Brasil-cêntricas e mais discursivas
