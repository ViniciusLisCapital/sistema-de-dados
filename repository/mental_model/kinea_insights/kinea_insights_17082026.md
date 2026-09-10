# O Grande Truque

**Data de publicação:** 17/08/2026
**Fonte:** https://www.kinea.com.br/blog/kinea-insights-o-grande-truque/

## Estados Unidos, China e a disputa pela liderança da inteligência artificial

Em *O Grande Truque* (*The Prestige*, 2006), Christopher Nolan conta a história de dois mágicos rivais na Londres vitoriana, obcecados pelo mesmo truque: fazer um homem desaparecer de um lado do palco e reaparecer, no mesmo instante, do outro. Robert Angier e Alfred Borden chegam ao mesmo efeito por caminhos opostos, e é essa diferença de método que move o filme.

Angier é o *showman* de recursos ilimitados: incapaz de decifrar o segredo do rival, atravessa o Atlântico para comprar, de Nikola Tesla, uma máquina extraordinária e cara que resolve o problema por força bruta. Já Borden é o engenheiro cujo truque não custa quase nada, mas exige elegância de desenho e compromisso absoluto com o segredo: um compra o espetáculo a qualquer preço, o outro o constrói com engenho e sacrifício.

Por que usamos “O Grande Truque” como analogia para esse Kinea Insights?

A corrida da inteligência artificial entre Estados Unidos e China é, atualmente, de certa forma, um duelo entre Angier e Borden. De um lado, os laboratórios de fronteira americanos, como OpenAI e Anthropic, apostam na máquina de Angier: investimentos colossais em treinamento e modelos proprietários.

Do outro, os laboratórios chineses, como DeepSeek, Alibaba, Moonshot e Z.AI, apostam na elegância do desenho, com soluções criativas que usam menos recursos e se apoiando no gesto mais subversivo de todos: a publicação aberta de seus truques.

Os modelos chineses ainda não lideram, mas encurtaram a distância rapidamente e o diferencial deles é o custo, muito abaixo dos rivais. Desde o “DeepSeek Day” de janeiro de 2025, quando um modelo chinês treinado por uma fração do custo dos concorrentes chegou ao topo dos benchmarks, a pergunta ficou no ar: os modelos chineses vão alcançar os pares ocidentais a uma fração do custo?

Cutter, o engenheiro de palco do filme, explica que todo grande truque tem três atos: a Promessa, quando o mágico mostra algo comum; a Virada, quando o comum vira extraordinário; e o Prestígio, quando ele traz de volta o que sumiu e colhe os aplausos.

Neste Insights, seguiremos os três atos aplicados aos grandes modelos de linguagem: o que são e por que foram fáceis de replicar (Promessa), as diferenças entre o método americano e o chinês (Virada), e quem ficará com os aplausos (Prestígio).

### A PROMESSA: POR QUE O TRUQUE ERA REPLICÁVEL

Um grande modelo de linguagem (LLM, na sigla em inglês) é, em essência, um previsor de palavras: uma rede neural treinada sobre trilhões de palavras para estimar, a cada instante, a continuação mais provável de um texto. Dessa tarefa banal, surgem capacidades complexas, como programar e “raciocinar”.

A receita tem três ingredientes: arquitetura, dados e computação. E nenhum dos três era segredo. A arquitetura, o *Transformer*, foi publicada pelo próprio Google, em 2017, em artigo acadêmico aberto (“*Attention Is All You Need*”). Os dados são, em grande parte, a internet pública. E as “leis de escala”, a relação previsível entre computação e capacidade obtida, tem sido documentada exaustivamente ao longo dos últimos anos.

Quando o ChatGPT estreou, em novembro de 2022, o efeito foi o de um mágico executando um número inédito em praça pública: o espanto foi universal, mas o método, para quem sabia ler os artigos científicos, estava à vista. Foi por isso que Anthropic, Google, Meta, xAI e, crucialmente, os laboratórios chineses, apresentaram números comparáveis no palco em questão de meses. O ChatGPT não revelou um segredo; revelou que havia um palco. E que o público pagaria para ver.

### A VIRADA: A EXTRAVAGÂNCIA CONTRA A SIMPLIFICAÇÃO

É na Virada que os métodos divergem. A estratégia do lado americano é o de Angier: resolver o problema com capital. Os laboratórios de fronteira gastam dezenas de bilhões de dólares por ano em *clusters* de chips para treinar modelos cada vez maiores, mantidos proprietários. O truque fica trancado no teatro, e o público paga ingresso (a API) para assisti-lo. É a lógica que exploramos em *[Devoradores de Estrelas](https://www.kinea.com.br/blog/insights-devoradores-de-estrelas-inteligencia-artificial/)*: um *capex* que já supera US$ 1 trilhão à espera de monetização.

Já do lado chinês, a estratégia é a de Borden e tem três movimentos. O primeiro é a engenhosidade de desenho. Sob restrição de chips, os laboratórios chineses foram forçados a extrair mais de menos: o DeepSeek R1, estopim do “DeepSeek Day”, era um modelo de baixo custo relativo aos ocidentais, graças, entre outros, a arquiteturas de “mistura de especialistas” (MoE), em que só uma fração do modelo é ativada a cada pergunta.

O segundo movimento é a destilação. Destilar é treinar um modelo novo usando as respostas de um modelo mais capaz como professor: em vez de aprender com a internet bruta, o aluno aprende com o produto acabado do rival, herdando parte de sua inteligência por uma fração do custo.

Neste ano, os principais laboratórios americanos, ao lado da Casa Branca, acusaram formalmente laboratórios chineses de destilação “em escala industrial” de seus modelos de fronteira. Como no filme, o truque copiado sobe ao palco poucos quarteirões adiante, e a plateia não distingue o original da cópia.

O terceiro movimento é o mais subversivo: publicar o truque. DeepSeek, Alibaba (Qwen), Moonshot (Kimi) e Z.AI (GLM) liberam os pesos de seus modelos muitas vezes sob licenças permissivas, que autorizam qualquer empresa a usar, modificar e comercializar o modelo, gratuitamente e sem pedir permissão.

A estratégia de Borden já começa a dar resultados. A diferença dos modelos abertos chineses para os de fronteira americanos caiu à menor distância já registrada. Ou seja, os chineses colocaram os modelos de pesos abertos com performance similar à dos americanos e a uma fração do custo de seus concorrentes.

A lógica econômica de abrir o truque tem nome nos manuais de estratégia: *comoditizar*. Se a inteligência vira insumo gratuito e abundante, o valor migra para quem domina as aplicações que a utilizam, e é aí que a China enxerga sua vantagem. No discurso em que dobrou a aposta no código aberto, em julho de 2026, Xi Jinping ligou explicitamente a abertura dos modelos de I.A. à estratégia chinesa “do mundo digital para o mundo físico”: o mundo das fábricas, dos robôs e do *hardware*, onde a liderança chinesa é, hoje, incontestável.

Há também o cálculo geopolítico: a China não quer que os Estados Unidos obtenham vantagem assimétrica na tecnologia. Ao distribuir gratuitamente modelos de quase fronteira, enfraquece o poder de preço dos laboratórios americanos, fortalece potenciais adversários dos EUA e captura a inovação que naturalmente se agrega a um ecossistema aberto. Quem não pode vender o ingresso prefere que o espetáculo seja de graça.

### “O SEGREDO NÃO IMPRESSIONA NINGUÉM”: A CONTA DA I.A.

O próprio filme oferece a síntese desta seção: o segredo não impressiona ninguém, o que importa é o uso que se faz dele. À medida que todos os modelos ficam bons o suficiente para a maioria das tarefas, a pergunta “qual modelo usar” perde relevância. E o que passa a importar, para as empresas, é o custo total.

E o custo cresceu rápido: em um mundo onde a demanda por inteligência de fronteira excede em muito a oferta, limitada pela escassez de computação, o poder de barganha ainda está com os laboratórios ocidentais.

A receita anualizada da Anthropic e OpenAI já chega perto de $130 bilhões de dólares e segue acelerando em 2026. A I.A. virou linha relevante de orçamento, e o corte de custos virou disciplina.

A primeira resposta das empresas foi em arquitetura. Ferramentas como Auto Router, RouteLLM e o Model Router da Microsoft analisam cada pergunta em tempo real e a direcionam ao modelo mais barato capaz de respondê-la bem. Em *benchmarks* do RouteLLM, o roteamento reduziu os custos entre 35% e 85%, dependendo da tarefa, preservando cerca de 95% do desempenho.

A segunda resposta foi a migração para os modelos abertos, em geral, chineses. Para as tarefas de alto volume e baixa complexidade, trocar o *flagship* americano por um modelo aberto 5 a 30 vezes mais barato virou decisão trivial. Dados da OpenRouter, agregadores de modelos muito utilizados por desenvolvedores de *software* e *startup**s*, já mostram uma penetração de 50% dos modelos abertos chineses nessa plataforma.

Apesar da participação elevada no segmento de desenvolvedores e *startups*, a participação total de mercado efetivamente conquistada pelos modelos abertos chineses permanece pouco clara. Grandes *marketplaces* de modelos, onde o consumo se concentra, como o Amazon Bedrock, ainda não disponibilizam alguns dos modelos chineses mais avançados, a exemplo do Kimi K3. À medida que esses modelos forem incorporados às grandes plataformas de *cloud*, será possível avaliar com mais clareza seu verdadeiro potencial e sua adoção no mercado.

Uma ressalva importante: preço por token não é preço por resposta. Na era dos modelos de raciocínio, cada modelo gasta uma quantidade diferente de tokens para chegar à mesma resposta correta. A *commodity* não é o token, é a inteligência. O que importa é o custo por tarefa resolvida. Mesmo com essa diferença menor, a vantagem em modelos chineses baratos continua clara.

Para os laboratórios que investiram bilhões na marca de seus modelos, é um mundo desconfortável: a escolha do modelo passou a levar em conta o custo-benefício de suas respostas, e não somente sua qualidade isolada.

### O PREÇO DO SEGREDO: DADOS, SEGURANÇA E DISPONIBILIDADE

Grandes empresas exigem de seus provedores de I.A. políticas de retenção zero de dados (Zero Data Retention, ZDR): a garantia contratual de que perguntas, documentos e códigos enviados ao modelo não são armazenados após o processamento nem usados para treinar modelos futuros. Para um banco, uma farmacêutica ou um governo, ZDR não é diferencial, é pré-requisito.

É aqui que os serviços chineses tropeçam. O DeepSeek hospedado na China, por exemplo, não oferece retenção zero: armazena dados em servidores próprios e admite compartilhamento com terceiros. A API hospedada na China é inaceitável para boa parte do mundo corporativo ocidental.

Entretanto, modelos abertos são simplesmente arquivos que podem ser baixados para qualquer computador e executados localmente nos Estados Unidos: DeepSeek, Kimi, Qwen e GLM já rodam como modelos gerenciados na Amazon, Microsoft e Google, sob contrato ocidental e com retenção zero de dados. O truque chinês atravessa o Pacífico; o teatro chinês fica onde está.

Mesmo com soluções adequadas para a retenção de dados, os modelos abertos ainda exigem atenção do ponto de vista da segurança. Embora os dados possam ficar protegidos, as barreiras contra respostas perigosas, principalmente em temas como cibersegurança, biotecnologia e terrorismo, podem ser mais fracas ou removidas. Os modelos ocidentais, em geral, passam por controles mais rigorosos de segurança e veracidade, como mostram rankings especializados.

No fim, os modelos abertos chineses resolvem parte importante do problema corporativo: podem operar sob regras ocidentais, dentro da infraestrutura do cliente e sem dependência do laboratório de origem. Mas essa autonomia tem um preço: a empresa troca a confiança no fornecedor pela responsabilidade de garantir a segurança e a atualização do modelo. Abrir o truque não elimina os riscos, apenas muda quem precisa administrá-los.

### A MÁQUINA DE ANGIER: A GUERRA DA INFRAESTRUTURA

Nolan esconde no filme uma segunda rivalidade: a “guerra das correntes” de Nikola Tesla e Thomas Edison, que decidiu quem forneceria a eletricidade do século XX. A versão atual é a guerra dos chips, e é nela que a vantagem americana permanece mais nítida. Os controles de exportação cortaram o acesso chinês aos aceleradores de fronteira da Nvidia: a participação da China na receita da empresa caiu de 20% para 10%.

A resposta chinesa veio, mas ainda está longe dos competidores ocidentais. O chip mais avançado da Huawei entrega cerca de 2,8 vezes o desempenho do H20, o chip “rebaixado” que a Nvidia desenhou para a China, no entanto ainda tem 4 vezes menos capacidade que os últimos modelos da empresa americana. Ou seja, apesar do esforço chinês, a maior parte da capacidade de processamento de I.A. ainda se encontra fora da região.

A capacidade chinesa é aplicada principalmente para inferência dos modelos. Treinar na fronteira, porém, é outra história: relatos indicam que a própria DeepSeek não conseguiu completar ciclos longos de treinamento em Ascend em 2025 e, segundo fontes de notícias, modelos do DeepSeek teriam sido treinados em chips Blackwell contrabandeados ou fora da China.

Soma-se o software: o ecossistema CANN, da Huawei, ainda está longe da maturidade do CUDA, da Nvidia. Sem chips de primeira linha, a capacidade chinesa de servir seus modelos globalmente, em escala e com a confiabilidade que clientes corporativos exigem, fica limitada.

O equilíbrio provável para os próximos anos é híbrido: treinar onde houver Nvidia e servir domesticamente em Ascend, enquanto o país cria uma rede nacional de *data centers* para compensar, com escala horizontal, o que falta em cada chip.

### CENÁRIOS: QUEM FICA COM O PRESTÍGIO?

Do duelo entre a máquina de Angier e o gêmeo de Borden, enxergamos três cenários para os próximos meses e anos, não mutuamente excludentes, e cada um com sinais próprios a monitorar.

No primeiro, fronteira americana dispara: um novo salto de capacidade que dependa de computação massiva, com agentes autônomos de longa duração e avanços científicos genuínos reabrem a distância entre a fronteira americana e os competidores, e o teatro de Angier volta a lotar a preços premium.

No segundo, modelos abertos viram padrão: a inteligência vira insumo abundante e barato, qualquer que seja a bandeira do fornecedor. Trajetória natural à medida que a oferta de semicondutores e infraestrutura alcance a demanda. Nesse cenário o uso e as aplicações devem crescer exponencialmente pelo baixo custo de adoção.

No terceiro, dois ecossistemas: controles de exportação de um lado e exigências de segurança de dados do outro dividem o mundo em duas pilhas tecnológicas completas: chips, modelos, nuvem, com o resto do mundo escolhendo palco a palco, como na Guerra Fria das infraestruturas.

Independentemente do cenário, enquanto a Inteligência Artificial seguir crescendo, preferimos ser donos do arsenal e do palco (infraestrutura e semicondutores), a apostar em qual mágico ficará com os aplausos.

### CONCLUSÃO

Cutter avisa na abertura: fazer algo desaparecer não basta, é preciso trazê-lo de volta. Construir um modelo espantoso é a Virada, e os dois lados do Pacífico já provaram ser capazes dela. O Prestígio, transformar espanto em lucro, ninguém executou. Os americanos gastam sem garantia de plateia. Os chineses operam com margens mínimas, sem acesso aos chips e ao maior mercado consumidor do mundo.

O filme guarda, ainda, uma lição sobre plateias: no fundo, o público quer ser enganado, é para isso que compra o ingresso. Mercados em meio a revoluções tecnológicas não são diferentes: querem acreditar. Nosso trabalho como investidores é o oposto do da plateia. Enquanto o duelo não define um vencedor, seguimos posicionados nos insumos escassos que qualquer desfecho exigirá, evitando as camadas em que o truque já virou *commodity* e desconfiando de todo número que pareça mágica.

Ao final da sessão, a plateia deixa o teatro sem saber como o truque foi feito e é justamente isso que a faz voltar. A corrida da inteligência artificial seguirá lotando o teatro por muitos anos. Para quem investe, a pergunta que abre o filme continua sendo a única que importa: você está observando atentamente?

Estamos sempre à disposição de nossos clientes e parceiros.

#### Kinea Investimentos
