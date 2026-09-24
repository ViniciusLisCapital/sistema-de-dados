# Reunião — Modelo de Câmbio: Convergência Metodológica

**kicker:** SISTEMA MULTIAGENTE — MESA MACRO
**subtítulo:** Resolução da divergência sobre o uso explicativo do modelo
**meta:** 17/09/2026 · Reunião bilateral · modelo quantitativo de câmbio (USD/BRL)

---

## 01 · CONTEXTO — DO QUE SE TRATOU A REUNIÃO

Na reunião de 11/09 com a equipe, Vinícius apresentou o modelo quantitativo de câmbio que
construiu. Surgiu ali uma divergência metodológica com Paulo Cesar Nunes sobre **para que aquele
modelo pode ser usado**. Por consumir tempo desproporcional à agenda do dia, a discussão foi
deixada de lado na reunião ampla, com o encaminhamento de que os dois a retomassem em separado até
chegar a uma convergência.

Houve duas conversas. Na primeira, em 16/09, **não houve entendimento sobre esse ponto específico**.
Na segunda, em 17/09, com pesquisa feita pelos dois lados no intervalo, **a divergência foi
resolvida** — e resolvida em favor da especificação que já estava em uso.

Esta ata registra a convergência, o raciocínio que a sustenta e o encaminhamento do trabalho.

**Participantes:** Vinícius Barcelos e Paulo Cesar Nunes.

---

## 02 · A DIVERGÊNCIA — O QUE ESTAVA EM DISPUTA

> *Cards*

**Posição de Paulo — o modelo serve à predição, não à explicação**
*`posição inicial`*
Na leitura apresentada na reunião de 11/09, o modelo não poderia ser usado para explicar
movimentos passados do câmbio; seu uso legítimo seria apenas prever. A decomposição para trás não
seria correta.

**O argumento: a equação é estática e as variáveis são simultâneas**
*`o núcleo técnico da objeção`*
Como o preditor é medido em T e o alvo também em T, features e câmbio são contemporâneos. Por essa
leitura, a especificação teria de usar informação até T e prever T+1 — um lag deliberado separando
o que se sabe do que se quer estimar.

**Posição de Vinícius — os betas decompõem o passado**
*`posição inicial`*
Os coeficientes estimados podem ser usados para atribuir, período a período, quanto cada canal
contribuiu para o movimento observado do câmbio — que é precisamente a pergunta que a mesa faz ao
modelo.

---

## 03 · ESPECIFICAÇÕES — O QUE MUDA DE UMA LEITURA PARA A OUTRA

O ponto que destravou a discussão é que **explicação e predição não são o mesmo exercício** — e que
a diferença entre elas não está necessariamente na equação, mas em de onde vêm os números que
entram nela.

> *Tabela*

| LEITURA | ESPECIFICAÇÃO | O QUE ELA RESPONDE |
|---|---|---|
| Preditivo com lag — *alternativa levantada, não adotada* | ŷ(T+1) = β₀ + β₁·CDS(T) + β₂·carry(T) + … | Prevê o câmbio de T+1 com a informação disponível em T. O R² mede a qualidade da previsão em períodos que o modelo não viu no treino. |
| Contemporâneo — *a especificação em uso* | ŷ(T) = β₀ + β₁·CDS(T) + β₂·carry(T) + … | Mede quanto as features explicam da variância do câmbio. É desta equação que sai a decomposição por contribuição. |

**A predição não vem do lag — vem da estimativa das features**
*`o que efetivamente foi acordado`*
A equação adotada permanece contemporânea. Para projetar T+1 não se troca a especificação nem se
estima um segundo modelo: mantêm-se os mesmos betas e alimentam-se as features de T+1 —
`ŷ(T+1) = β₀ + β₁·CDS(T+1) + β₂·carry(T+1) + …`, em que CDS(T+1) e carry(T+1) virão do
próprio sistema ou serão assumidos como premissa. **É uma equação só, lida em dois sentidos.**

**A decomposição é direta e exata num modelo linear**
*`como se lê a contribuição de um dia`*
Os betas são coeficientes médios sobre toda a janela e, sozinhos, não dizem quanto cada feature
contribuiu num dia específico. Isso vem da decomposição de ŷ(T): a contribuição de cada canal no
dia T é o beta multiplicado pela variação observada da feature naquele dia —
`contribuição_CDS(T) = β₁ × ΔCDS(T)`. Num modelo linear como o Ridge, essa conta é exata.

---

## 04 · OS MODELOS AVALIADOS — O QUE A LITERATURA OFERECE

Paulo levantou as alternativas que a literatura aponta para o problema. São três, e **a última é
exatamente o modelo que já estava em uso**.

> *Tabela*

| MODELO | O QUE FAZ | QUANDO É SUPERIOR |
|---|---|---|
| VAR (Vector Autoregression) | Modela cada variável como função das defasagens de todas as demais, simultaneamente. A função de impulso-resposta mostra como um choque se propaga pelo sistema ao longo do tempo. | Quando a pergunta é como um choque no CDS se propaga pelo sistema ao longo de vários períodos. |
| Modelo de fatores | Trata as variáveis observadas como manifestação de fatores latentes (risco global, condições financeiras). As cargas fatoriais saem por PCA. | Quando a pergunta é quais fatores subjacentes explicam o câmbio além das features observadas. |
| Regressão de atribuição (Ridge) | Estima os betas contemporâneos e, para cada período, calcula a contribuição de cada feature ao movimento do câmbio naquele período. | Quando a pergunta é quanto cada canal contribuiu para o câmbio num dia específico. |

**A escolha do modelo é a escolha da pergunta**
*`critério de decisão`*
Nenhum dos três é melhor em abstrato. Se o que a mesa precisa é quantificar as sensibilidades dos
canais e atribuir o movimento do câmbio a cada um deles num dia determinado, a regressão de
atribuição resolve o problema de forma adequada — **e sem a complexidade adicional do VAR ou do
modelo de fatores**.

**O VAR foi listado como opção, mas o caminho é o do Banco Central**
*`onde a escolha recai`*
Paulo trouxe o VAR entre as alternativas. Comentou-se na própria reunião que **a estrutura usada
pelo Banco Central é parecida com um VAR, porém com bem mais estrutura econômica imposta** — as
relações entre as variáveis são escritas a partir da teoria, não deixadas livres na estimação. É
nessa direção que o trabalho segue, e não na do VAR puro.

---

## 05 · A CONVERGÊNCIA — UM MODELO, DUAS ETAPAS

A conclusão conjunta é que o modelo já construído **pode sim ter seus betas usados para explicar os
movimentos passados do câmbio**, e que os mesmos betas servem, num momento posterior, à estimativa
para frente. **Não são dois modelos: é um só, usado em duas etapas.**

> *Cards*

**Primeira etapa — o passado, com features observadas**
*`estimação dos betas`*
Estima-se a equação contemporânea sobre a série histórica e dela sai a decomposição: quanto cada
canal contribuiu para o movimento observado em cada período. É o uso que estava em disputa, e é o
que a mesa precisa hoje.

**Segunda etapa — o futuro, com features estimadas**
*`mesmos betas, outros insumos`*
A projeção do câmbio passará a ser a composição de duas coisas: a estimativa das features em T+1 e os
betas já calculados na primeira etapa. Nada na equação muda — muda a origem dos números que entram
nela.

**Parte das features será endogeneizada, parte continuará premissa**
*`a divisão seguirá o modelo do Banco Central`*
As variáveis que o arcabouço do BC já trata em equações — inflação, juros, expectativas — passarão
a ser determinadas dentro do próprio sistema. As que ficarem de fora dele, como o dólar global,
entrarão como premissa assumida.

**A premissa é por onde entra o julgamento**
*`e isso é uma vantagem, não uma lacuna`*
Manter parte das variáveis como premissa é o que permitirá incorporar eventos qualitativos da
realidade que nenhuma equação captura. O que for endogeneizado ganhará consistência interna; o
que for premissa preservará a leitura de mesa.

---

## 06 · DEFINIÇÕES — O QUE FICOU DECIDIDO

✓ **A divergência foi resolvida em favor da especificação em uso**
Vinícius e Paulo convergiram que os betas do modelo Ridge já construído podem ser usados para
explicar os movimentos passados do câmbio. O modelo não precisa ser trocado para cumprir esse
papel.

✓ **Um modelo só, em duas etapas — explicação primeiro, previsão depois**
A equação permanece contemporânea. A primeira etapa entrega a decomposição do passado; a segunda
combinará os mesmos betas com a estimativa das features em T+1 para projetar à frente.

✓ **A decomposição por contribuição é a leitura correta dos betas**
`contribuição_i(T) = β_i × ΔX_i(T)`, exata por ser o modelo linear. É o que permite responder
quanto cada canal moveu o câmbio num dia específico.

✓ **O sistema seguirá a estrutura do modelo do Banco Central, não a do VAR**
O VAR foi avaliado e registrado como alternativa. A opção é pelo arcabouço do BC, que é próximo
dele em forma, mas impõe estrutura econômica às relações entre as variáveis.

✓ **O que for endógeno seguirá as equações do BC; o que ficar de fora entrará como premissa**
Inflação, juros e expectativas serão determinados dentro do sistema; variáveis como o dólar
global permanecerão exógenas e serão assumidas.

✓ **O trabalho segue para o sistema completo de equações**
Com o ponto metodológico fechado, a equação de câmbio passa a ser montada dentro do arcabouço
estrutural, junto com as demais.

---

## 07 · PRÓXIMOS PASSOS

→ **Paulo Cesar Nunes — estudar os papers do modelo do Banco Central**
Os dois boxes do Relatório de Inflação que descrevem o modelo semiestrutural de pequeno porte — o
agregado e o desagregado — já foram enviados por Vinícius.

→ **Vinícius Barcelos — construir as demais equações do sistema**
Em paralelo ao estudo, seguir montando as equações do arcabouço, definindo o que será
endogeneizado e o que entrará como premissa.

→ **Ambos — afinar a especificação ao longo da construção**
Trocar impressões sobre cada equação à medida que forem ficando prontas, até chegar a um sistema
consistente.

---

**PRINCÍPIO DE MÉTODO**
Uma especificação não é certa ou errada em abstrato — é certa ou errada em relação à pergunta. A
equação é a mesma nos dois sentidos: lida com as features observadas, ela diz o que moveu o câmbio;
lida com as features estimadas, ela diz para onde ele vai. O que muda não é o modelo — é de onde
vêm os números que entram nele.
