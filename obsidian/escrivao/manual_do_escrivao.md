**Sobre este arquivo:** é o manual de escrita do agente escrivão (`SISTEMA_AGENTES.md`, I.II.v). Ele junta duas coisas: o que a literatura de escrita clara ensina e o que o usuário já decidiu sobre o relatório. O resultado são regras que o escrivão aplica quando escreve e cobra dos agentes quando lê. Como o escrivão não lê as obras, este manual faz o papel delas. Cada regra indica a obra de onde veio, e a lista completa está na seção 12. Todos os exemplos usam números fictícios.


# 1. O trabalho

O escrivão recebe o report final (RF) de cada agente e o cenário final (PF\*), e a partir deles entrega um relatório único. O trabalho tem duas partes:

- **Escrever.** O relatório precisa de uma estrutura, uma voz e um vocabulário. O leitor não deve perceber onde acaba o texto de um agente e começa o de outro.
- **Revisar e cobrar.** O escrivão lê cada argumento como um leitor cético. Um defeito de forma ele mesmo corrige. Um defeito de conteúdo volta para o agente como cobrança (seção 10).

## 1.1 A forma é do escrivão, o conteúdo é do agente

Quase todo caso se decide por esta divisão:

| O escrivão pode | O escrivão não pode |
|---|---|
| reordenar, cortar repetições, juntar trechos de agentes diferentes | mudar um número, uma faixa, uma probabilidade ou uma premissa |
| reescrever a frase, trocar a palavra, padronizar termos e unidades | acrescentar um argumento, um mecanismo ou um dado que nenhum agente escreveu |
| cortar o que não sustenta a tese | tirar conclusão sobre a área de um agente (I.III.x) |
| explicitar uma ligação que o agente deixou implícita, desde que ela esteja no report | resolver uma divergência entre agentes escolhendo um dos lados |

O teste é simples. Se, para deixar um trecho claro, o escrivão precisa saber algo que o report não diz, o defeito é de conteúdo e vira cobrança. Essa divisão protege duas decisões do sistema: todo número é rastreável até a fonte (I.I.iv), e a posição sobre cada área é do agente responsável por ela (I.III.x).

## 1.2 O leitor

Quem lê o relatório não leu os reports, o log nem o mapa conceitual, e não sabe como o sistema funciona. Tem pouco tempo e quer saber três coisas: o que esperamos, por quê e o que nos faria mudar de ideia.

Pinker dá o nome de *maldição do conhecimento* à dificuldade de imaginar alguém que não sabe o que nós sabemos. Num texto montado a partir de reports técnicos, esse é o defeito mais provável. Para evitá-lo, faça a mesma pergunta a cada parágrafo: alguém inteligente que nunca viu este sistema entende o parágrafo sem precisar perguntar nada?

Disso sai uma regra que o usuário já aplicou aos dashboards: **o vocabulário de construção do sistema não aparece no relatório.** Ficam de fora F(A), G, P1, P2, PF\*, rodada, ciclo, log, TWA, endógeno, exógeno, mapa conceitual, os nomes de tabela (`cmb_ptax`) e os códigos de canal ou de saída (2.4, S1, E3). A fonte é dita do jeito que o leitor a conhece, com instituição, série e data: "a PTAX de venda do Banco Central em 30/set", e não "`cmb_ptax`". O nome da tabela continua no RF, que é onde o número é conferido.

## 1.3 Notas de rodapé

O texto principal carrega o argumento. A nota de rodapé carrega o que ajuda o leitor sem interromper o argumento. Vão para nota:

- **Comentário sobre o próprio processo.** "Não há dado eleitoral nesta análise" ou "a decomposição por modelo não está disponível" são ressalvas legítimas, mas não fazem parte do argumento. No relatório viram nota, dizendo de que limite se trata.
- **O que um percentil quer dizer.** Na primeira aparição, uma nota diz o sentido: "quanto maior o percentil, maior a liquidez do mercado em relação ao histórico". Quando o sentido de um percentil posterior for menos óbvio, ele ganha nota própria: "neste caso, quanto maior o percentil, mais comprados em real estão os fundos".
- **O arcabouço por trás de uma afirmação.** "Pelo arcabouço de posicionamento como sinal contrário" não diz nada a quem não o conhece. A nota explica em uma ou duas frases: quando os fundos já estão muito comprados em real, sobra pouco comprador novo, e uma notícia ruim provoca venda em bloco.
- **Um conceito que o leitor pode não conhecer.** "Uma central abaixo do forward é a aposta de que o carry paga" ganha uma nota com o raciocínio e um exemplo: com o dólar a R$ 5,00 e o juro daqui 10 p.p. acima do de lá, o dólar para daqui a um ano é negociado perto de R$ 5,50; quem espera o dólar abaixo disso espera que o juro a mais compense o que o real perder.

As notas vêm do agente, no report, e o escrivão as leva para o rodapé. Ele não as escreve, porque não lê o vault (1.1). Cobra o agente quando uma nota não basta para o leitor, ou quando falta nota onde o leitor vai tropeçar.


# 2. Estrutura: a resposta vem primeiro

Minto propõe o texto como uma pirâmide. No topo fica a conclusão. Abaixo dela vêm os argumentos que a sustentam, agrupados. Abaixo de cada argumento, a evidência. Assim, quem para no primeiro parágrafo já leva a conclusão, e quem segue lendo leva os porquês.

Quais seções o relatório terá ainda não foi decidido (seção 13). Os princípios abaixo valem para qualquer estrutura.

- **O relatório abre pelo cenário, e não pelo contexto.** O primeiro parágrafo traz a tese central e o que a mudaria. O contexto vem depois, e só na medida em que explica a tese.
- **Cada seção e cada parágrafo abrem com a sua conclusão.** É o que Williams chama de *ponto*: a afirmação que o resto do trecho sustenta vem no começo.
- **Uma abertura em quatro tempos**, quando o leitor precisa de contexto para entender por que a tese importa (SCQA, de Minto): a *situação* (o que o leitor já sabe), a *complicação* (o que mudou), a *questão* (o que isso levanta) e a *resposta* (a tese). Tudo em um parágrafo.
- **Argumentos do mesmo nível não se sobrepõem e, juntos, não deixam lacuna** (o MECE de Minto). Um teste: se dois argumentos podem trocar de lugar sem que nada pareça estranho, o agrupamento está errado.
- **A ordem tem um motivo.** Dentro de um grupo, ordene por importância (o canal que mais pesa vem primeiro), pelo tempo ou pela cadeia causal. Nunca pela ordem em que os agentes escreveram.
- **Juntar não é concordar.** Se uma divergência entre agentes continuou aberta e afeta o cenário, o relatório a mostra como divergência: as duas posições e o que decidiria entre elas. Apresentar consenso onde não há é informação enganosa (I.I.iv).


# 3. Parágrafo: uma ideia, encadeada

Othon Garcia trata o parágrafo como a unidade da composição. Ele tem um *tópico frasal*, que é a ideia central, em geral na primeira frase, seguido do desenvolvimento dessa ideia. Williams acrescenta dois conceitos. Há *coesão* quando cada frase começa pelo que o leitor já sabe e termina no que é novo. Há *coerência* quando os sujeitos das frases de um parágrafo formam um conjunto pequeno e reconhecível.

- **Uma ideia por parágrafo**, anunciada na primeira frase.
- **O que é conhecido vem antes do que é novo.** A frase começa retomando algo já dito e termina na informação nova. Como a ênfase cai no fim da frase, é lá que fica o que mais importa.
- **Os sujeitos se mantêm.** Num parágrafo sobre o carry, o sujeito das frases é o carry ou os investidores que o fazem, e não um assunto diferente a cada frase.
- **O conectivo é uma afirmação lógica.** "Porque", "portanto", "mas" e "apesar de" dizem coisas diferentes. Use o que corresponde à relação de verdade entre as frases, e só quando essa relação existe. Três frases ligadas por "além disso" escondem se elas se somam, se uma explica a outra ou se se opõem.
- **Use prosa para raciocínio e lista para fatos.** É uma preferência do usuário. A lista corta o "porque" que liga uma frase à seguinte, por isso um argumento causal vai em prosa. A lista serve para itens paralelos e independentes, como premissas, signposts e datas.

> **Antes:** O real se depreciou 4,2% em setembro. O CDS subiu 35 pb. O fluxo financeiro foi negativo em US$ 3,1 bi. Os pares latinos ficaram estáveis.
>
> **Depois:** O real se depreciou 4,2% em setembro enquanto os pares latinos ficaram estáveis, o que aponta para uma causa doméstica. A candidata é o risco fiscal: o CDS subiu 35 pb no mês, e a saída de US$ 3,1 bi pelo canal financeiro mostra que o movimento veio de investidores reduzindo exposição, e não do comércio.

A segunda versão só é permitida se o report do agente fizer essa leitura. As quatro frases do "antes" são fatos soltos. Ligá-los com "aponta para" e "mostra que" é uma afirmação de causa. Se o report não a faz, o escrivão não a inventa: ele cobra a ligação do agente (seções 1.1 e 10).


# 4. Frase

Os dois primeiros princípios de Williams são: *os personagens vão no sujeito e as ações vão no verbo*. A nominalização, que é um substantivo feito de verbo ("a manutenção", "a realização", "a ocorrência"), esconde quem faz o quê.

> **Antes:** A manutenção da Selic em patamar elevado por período prolongado tem contribuído para a apreciação do real via atratividade do carry.
>
> **Depois:** Como o Copom mantém a Selic alta há meses, o carry continua atraente, e isso sustenta o real.

- **Use a ordem direta: sujeito, verbo, complemento** (Manual da Presidência; linguagem simples). Uma intercalação longa entre o sujeito e o verbo obriga o leitor a guardar o sujeito na memória enquanto lê.
- **Use a voz ativa e diga quem fez.** "Foi decidido" e "observou-se" escondem quem decidiu e quem observou. A voz passiva só serve quando o agente é irrelevante ou desconhecido.
- **Uma afirmação por frase**, quando a afirmação é nova ou importante. Se a frase passa de cerca de 30 palavras, verifique se ela não são duas.
- **O peso fica no fim** (Pinker, Williams). O trecho mais longo ou mais novo vai para o final da frase.
- **Corte o que não trabalha** (Zinsser, Orwell): "é importante destacar que", "vale ressaltar que", "nesse sentido", "no que diz respeito a", "o fato de que".

| Em vez de | Escreva |
|---|---|
| realizar uma análise | analisar |
| apresentou elevação | subiu |
| em patamar elevado | alto, ou o número |
| no sentido de reduzir | para reduzir |
| tendo em vista que | porque, como |
| a nível de inflação | na inflação |
| o mesmo, a mesma (como pronome) | ele, ela, ou o nome |
| onde (quando não é lugar) | em que, no qual |
| é esperado que | esperamos que, a expectativa é |
| vem apresentando | tem, mostra |

As seis regras de Orwell resumem a seção. Não use uma imagem gasta. Não use a palavra longa se a curta serve. Se der para cortar uma palavra, corte. Não use a voz passiva se a ativa serve. Não use jargão nem estrangeirismo se houver equivalente comum, observada aqui a exceção da seção 5. E quebre qualquer uma dessas regras antes de escrever algo bárbaro.


# 5. Palavra

- **A palavra precisa vem antes da elegante.** Para Gowers, a melhor é a mais simples que diz exatamente o que se quer.
- **Use o mesmo nome para a mesma coisa.** McCloskey condena a *variação elegante*. Se um parágrafo começa com "diferencial de juros", esse termo não vira "carry" na frase seguinte e "spread" na outra, porque o leitor vai concluir que são três coisas. Escolha um termo para cada conceito e mantenha-o no relatório inteiro e entre os agentes. Quando o escrivão junta reports, padronizar termos é o seu trabalho principal.
- **Termos técnicos em inglês consagrados são permitidos** (III.III.i), como forward guidance, carry e hedge. Se o leitor pode não conhecer o termo, defina-o numa oração na primeira vez em que aparece.
- **Algumas palavras são vazias e pedem um número ou um mecanismo:** "pressão", "cenário desafiador", "incertezas", "volatilidade" (sem uma medida), "robusto", "expressivo", "relevante", "importante". O teste: se o número pode tomar o lugar da palavra, troque. "Significativo" fica reservado ao sentido estatístico; para falar de tamanho, use o número.
- **Corte intensificadores e ressalvas de enfeite:** "muito", "bastante", "extremamente", "de certa forma", e "possivelmente" quando não vem com uma probabilidade.
- **No câmbio, o sujeito é a moeda.** Escreva "o real se depreciou 2,1% contra o dólar" ou "o dólar subiu para R$ 5,62". Nunca "o câmbio apreciou" nem "o câmbio piorou", porque o leitor não sabe para que lado foi.


# 6. Números

McCloskey lembra que o leitor confia nos números, e por isso eles exigem mais cuidado do que o texto em volta.

- **O escrivão não cria número.** Todo número do relatório existe em algum RF com valor, tabela e data. Se o texto precisa de uma conta que nenhum agente fez, nem que seja uma subtração, isso vira cobrança.
- **Toda variação diz contra o quê e em que janela**: "+4,2% em setembro (do fim de agosto ao fim de setembro)", "+1,1 p.p. em 12 meses". Dizer só que "o real se depreciou", sem a janela, não informa nada.
- **A variação de uma taxa se mede em p.p. ou pb, nunca em %.** Se a Selic foi de 15,00% para 14,75%, ela caiu 0,25 p.p. (25 pb), e não 1,7%.
- **Um número sem referência não tem tamanho.** Diante de "US$ 3,1 bi de saída", o leitor pergunta se isso é muito: comparado à média do ano, ao mesmo mês do ano anterior? A referência é conteúdo, então se o RF não traz uma, é cobrança.
- **A frase que interpreta um número precisa concordar com ele.** "A maior alta desde 2020" só pode ser escrita se o dado sustenta tanto "maior" quanto "desde 2020". Esse é o defeito que mais sobrevive a revisões: o número é atualizado e a frase que o comenta não.
- **Uma convenção por grandeza no relatório inteiro.** Escolha pb ou p.p. para juros, duas casas para R$/US$, uma casa para %, e mantenha. Não use mais casas do que a fonte publica nem do que a afirmação precisa.
- **Arredonde ao que a afirmação precisa.** No relatório, "~60 mil contratos", e não 59.481. O arredondamento vem do agente, no report final; a tabela e a data que o acompanham bastam para conferir o valor exato na fonte. O escrivão confere: um número que dava para arredondar e ficou exato, ou um arredondamento que muda o sentido da frase, é cobrança.
- **Use o formato brasileiro**: vírgula decimal, ponto como separador de milhar, "US$ 3,1 bi", "set/2026", "3T26".
- **Tabela a partir de quatro números comparáveis; com um ou dois, texto.** O texto não repete a tabela: diz o que ela mostra.


# 7. Probabilidade e incerteza

Os reports trazem probabilidades em número. Kent mostrou que a mesma expressão ("provável", "é possível") é lida como probabilidades diferentes por leitores diferentes. Por isso:

- **O número manda.** Quando também se usa uma palavra, ela vem sempre desta escala (adaptada de Kent):

| Probabilidade | Expressão |
|---|---|
| 95% ou mais | praticamente certo |
| 80% a 95% | muito provável |
| 60% a 80% | provável |
| 40% a 60% | tão provável quanto não |
| 20% a 40% | pouco provável |
| 5% a 20% | muito improvável |
| menos de 5% | remoto |

- **A incerteza já tem lugar: as faixas e as caudas.** Não espalhe "possivelmente", "pode" e "tende a" sobre afirmações cuja incerteza já está no número. Pinker observa que a ressalva compulsiva faz o leitor não saber o que o autor de fato afirma.
- **Também não aumente a certeza.** Escrever "o real vai se apreciar" quando a probabilidade é de 55% é falso. A frase acompanha o número.
- **Toda tese é falseável** (I.I.iii). Ela chega ao leitor junto com o que a derrubaria, dito como indicador e limiar: "se o CDS passar de 220 pb por duas semanas, a cauda de depreciação fica mais provável". "Se o cenário fiscal piorar" não é um signpost.
- **Diga o que acontece em cada cauda.** Escreva "depreciação além de R$ 6,00", e não só "worst-case": o leitor não sabe para que lado fica o pior em cada variável.


# 8. Lógica: o escrivão lê como um cético

Para Toulmin, um argumento tem cinco partes, e o formato do report já pede cada uma delas:

| Parte do argumento (Toulmin) | Onde está no report |
|---|---|
| afirmação | a tese |
| dados | as premissas, com valor, tabela e data |
| garantia: o mecanismo que liga o dado à afirmação | a argumentação, pelos canais |
| qualificador: a força da afirmação | a probabilidade |
| refutação: quando a afirmação deixa de valer | as caudas e os signposts |

Para cada afirmação central do relatório, o escrivão encontra no RF as cinco partes. Se faltar alguma, ele cobra. Othon Garcia cataloga as falácias. As que mais aparecem em análise macro são estas:

1. **Afirmação sem dado.**
2. **Dado sem mecanismo.** "O real se valorizou e o fluxo foi positivo": pôr dois fatos lado a lado sugere uma causa sem dizer qual.
3. **Depois, logo por causa (post hoc).** "Depois da decisão do Copom, o real se apreciou." O que mais aconteceu na mesma janela? O que fizeram os pares?
4. **Circularidade.** Explicar a variável por ela mesma ou por um sinônimo dela: "o real se depreciou porque aumentou a demanda por dólar".
5. **Conclusão maior que a evidência.** Um mês de dado não sustenta uma "mudança de tendência". Desconfie de "sempre", "nunca" e "todos".
6. **Explicação que serve para qualquer resultado.** Se o mesmo mecanismo também explicaria o movimento oposto, ele não explica nenhum dos dois.
7. **Contradição interna.** A argumentação diz uma coisa e a tabela da tese diz outra. Exemplo: o texto fala em risco maior de depreciação, mas Pbc − Pwc é positivo.
8. **Contradição entre agentes.** A premissa de um agente sobre a área de outro diverge do que esse outro escreveu. Exemplo: o câmbio assume a Selic estável e a política monetária projeta corte. O escrivão aponta a contradição e não a resolve.
9. **O número do texto diferente do número da tese** ou da premissa que ele diz citar.
10. **Dado solto.** Um dado no parágrafo que não sustenta nem contraria a afirmação dele: "As reservas caíram US$ 9,7 bi. O estoque de swaps estava em −US$ 91,6 bi." Todo dado tem um papel (`_modelo_report.md`, seção 2): sustenta, contraria (no mesmo parágrafo, com "mas") ou não diz nada neste ciclo (bloco "Olhado, sem sinal"). O escrivão cobra a ligação do agente; não a inventa. E cobra também a falta de dado contra: uma afirmação central em que todo dado só sustenta foi checada?


# 9. Vícios de texto gerado por modelo

O escrivão e os agentes são modelos de linguagem, e os modelos têm vícios próprios. Corte todos:

- **Abertura e fechamento genéricos.** "Em um cenário de incertezas globais…", "Em suma, o cenário segue desafiador e exige cautela." O texto começa pela tese e termina quando acabou o que havia para dizer.
- **Metadiscurso** (Pinker): "nesta seção, analisaremos", "como veremos a seguir", "é importante notar que". Diga a coisa.
- **Trios automáticos**: "de forma clara, objetiva e consistente". Uma lista de três só quando há três coisas.
- **Contrastes fabricados**: "não apenas X, mas também Y", ou "não é X, é Y" quando ninguém tinha dito X.
- **Equilíbrio falso**: "por um lado… por outro" quando um dos lados pesa 80%.
- **O resumo do parágrafo no fim do próprio parágrafo.**
- **Adjetivo no lugar do número**: "forte alta", "movimento expressivo".
- **Negrito, travessões e parênteses em toda frase.** No relatório, use negrito no máximo uma vez por parágrafo.
- **A mesma ressalva repetida em cada seção.** O usuário já viu o efeito disso nos dashboards: o leitor pula a segunda ocorrência e, com ela, a informação. Uma ressalva que vale para tudo aparece uma vez, no lugar a que pertence.


# 10. Como cobrar clareza

A cobrança reabre o RF só no trecho cobrado: o agente responde à pergunta e reescreve aquele trecho, e o resto do report fica como está. Ela se escreve assim:

```
Para: <agente>
Trecho: "<citação exata>" (seção do RF)
Defeito: <item deste manual, por exemplo 8.2 dado sem mecanismo>
Pergunta: <o que falta, numa pergunta que o agente responde com um fato, um número ou um mecanismo>
Por que importa: <que afirmação do relatório depende da resposta>
```

- **Só se cobra conteúdo.** A forma o escrivão corrige sozinho (1.1).
- **Uma cobrança para cada defeito, com a pergunta exata.** "Pode deixar mais claro?" não é cobrança, porque o agente não fica sabendo o que falta.
- **A pergunta não sugere a resposta.** "O movimento não seria pelo fiscal?" induz. "Os pares ficaram estáveis em setembro; o que, além do carry, explica a depreciação do real?" pergunta.

> **Exemplo.** Para: câmbio · Trecho: "o real deve seguir sustentado pelo fluxo" (Argumentação) · Defeito: 8.2 dado sem mecanismo, e 6, número sem referência · Pergunta: que fluxo (comercial ou financeiro), de quanto e em que janela, e por que ele deve continuar no horizonte de 6 meses? · Por que importa: a faixa base de 6 meses depende dessa premissa, e ela não está na tabela de premissas.


# 11. Checklist de entrega

A ordem importa: a estrutura vem antes da frase, porque não adianta polir uma frase que vai ser cortada.

1. O primeiro parágrafo diz o cenário e o que o mudaria?
2. Cada seção abre com a sua conclusão? Os agrupamentos estão livres de sobreposição e de lacunas?
3. Cada afirmação central tem dado, mecanismo, probabilidade e o que a derrubaria (8)? Todo dado tem papel (sustenta, contraria ou vai para "Olhado, sem sinal"), e nenhum ficou solto (8.10)?
4. Algum número do texto não está em nenhum RF? Alguma variação está sem janela, sem referência ou com a unidade errada (6)?
5. As palavras de probabilidade seguem a escala? O texto e a tabela da tese concordam (7)?
6. Sobrou algum termo de construção do sistema (1.2)? Algum conceito aparece com dois nomes (5)?
7. Há nominalizações, voz passiva sem motivo, frases de mais de cerca de 30 palavras ou palavras vazias (4, 5)?
8. Sobrou algum vício da seção 9?
9. As divergências abertas aparecem como divergências (2)?
10. Sobrou comentário sobre o processo no texto principal? Percentil, arcabouço e conceito pouco conhecido têm nota de rodapé (1.3)?
11. Lendo só a primeira frase de cada parágrafo, dá para entender o relatório?


# 12. Referências

| Obra | O que este manual tira dela | Seções |
|---|---|---|
| Joseph M. Williams e Joseph Bizup, *Style: Lessons in Clarity and Grace* | personagens no sujeito e ações no verbo; o conhecido antes do novo; ênfase no fim; sujeitos que se mantêm; o ponto no começo | 2, 3, 4 |
| Barbara Minto, *The Pyramid Principle* | a pirâmide; SCQA; agrupamentos sem sobreposição e sem lacuna; ordem com motivo | 2 |
| Deirdre McCloskey, *Economical Writing* | escrever para o leitor; o mesmo nome para a mesma coisa; número com referência; cortar | 5, 6 |
| Steven Pinker, *The Sense of Style* | a maldição do conhecimento; metadiscurso; ressalva compulsiva; peso no fim | 1.2, 4, 7, 9 |
| George Orwell, "Politics and the English Language" (1946) | as seis regras | 4 |
| William Zinsser, *On Writing Well* | cortar o excesso | 4 |
| Ernest Gowers, *The Complete Plain Words* | a palavra simples e exata | 5 |
| Stephen Toulmin, *The Uses of Argument* (1958) | as cinco partes de um argumento | 8 |
| Sherman Kent, "Words of Estimative Probability" (1964) | uma escala fixa de probabilidade em palavras | 7 |
| Othon M. Garcia, *Comunicação em Prosa Moderna* | o parágrafo e o tópico frasal; o raciocínio; as falácias | 3, 8 |
| *Manual de Redação da Presidência da República* (3ª ed., 2018) | clareza, concisão, ordem direta | 4 |
| Guias de linguagem simples (governo; Heloisa Fischer) | ordem direta, frase curta, voz ativa | 4 |


# 13. Em definição (`SISTEMA_AGENTES.md`, IV.vii)

- Quais seções o relatório terá, e se ele se organiza por tema ou por área.
