# Pendências — Equação (R), a regra de juros

Tudo o que falta na equação (R) do modelo estrutural. **O que está no ar vive no
[`CLAUDE.md`](CLAUDE.md) da pasta** — aqui só entra o que ainda não foi feito, mais o que foi
medido e **não** entrou.

```
(R) R(t) = r1·R(t-1) + r1b·R(t-2) + (1-r1-r1b)·(RR*(t) + Meta(t)) + r2·dI(t) + d08 + d20 + ε

    R    = Selic, média do trimestre (curva POLICY, fonte BIS)
    RR*  = juro real de mercado de 10 anos (NTN-B 120M), sem média móvel
    Meta = meta do CMN no horizonte de 12 meses
    dI   = Focus de IPCA 18 meses − Meta 24m
```

**Um objeto, dois nomes.** O BC publica esta série como *"IPCA 24 meses à frente"*: é a inflação
acumulada em **doze** meses terminando daqui a vinte e quatro, ou seja a janela [12, 24) meses. O
**centro** dela está a 18 meses, que é o horizonte efetivo, e é por isso que interpolar a curva
anual do Focus acerta em h = 1,5 ano. A tela diz "18 meses"; as colunas do painel (`pi_e_2a`,
`meta_24m`) usam o nome da fonte, que é o que se procura para conferir contra o BC.

Estimada com a restrição **imposta**: regride-se `y = R − RR* − Meta` contra `y(t-1)`, `y(t-2)` e
`dI`, sem intercepto, e o peso da âncora fica sendo `1 − r1 − r1b` por construção.

Estado em 2026-09-21 — 80 trimestres, 2006T3→2026T2:

| parâmetro | peso | margem | t (HAC 4) | t (MQ) |
|---|---|---|---|---|
| juros do trimestre anterior | 1,4344 | ± 0,1689 | 13,97 | 17,48 |
| juros de dois trimestres atrás | −0,5697 | ± 0,1716 | −5,46 | −7,38 |
| inflação esperada acima da meta | 0,3540 | ± 0,2373 | 2,45 | 3,13 |
| crise de 2008-2009 | −0,4328 | ± 0,2842 | −2,50 | −1,64 |
| pandemia de 2020 | −0,7181 | ± 0,2451 | −4,82 | −2,29 |

R² centrado 0,952 · RMSE 0,566 · meia-vida de um desvio **3 trimestres** · soma das defasagens
0,865 · efeito de longo prazo **2,62** · **Ljung-Box Q(4) p 0,683 e Q(8) p 0,438 — o resíduo é
indistinguível de ruído branco**, com autocorrelação de primeira ordem de −0,00.

**Os três parâmetros comparáveis caem dentro dos intervalos que o BC publica:**

| | nosso | BC publicado | |
|---|---|---|---|
| `r1` | +1,4344 | +1,48 [1,41; 1,54] | dentro |
| `r1b` | −0,5697 | −0,58 [−0,63; −0,52] | dentro |
| efeito de longo prazo | 2,62 | 2,03 [1,47; 2,64] | dentro, **encostado no teto** |
| soma das defasagens | 0,865 | 0,90 (sem IC publicado) | abaixo |

Convenção deste arquivo: **R#** pendência. Cada item diz se está bloqueado por dado, por decisão
ou por trabalho.

---

## 0. Cinco decisões do usuário que fecham perguntas

**RR\* é o juro real de mercado de 10 anos, sem média móvel**, em duas etapas no mesmo dia.
Primeiro a série: *"rr_star estou pensando em usar aqui uma média móvel da taxa de juros real de 10
anos."* Depois, vista a tabela de janelas de §2: *"Não quero perder essa amostra agora. Portanto,
por hora vamos manter a relação sem média móvel."*

Foi uma escolha entre dois custos reais, e o segundo continua de pé como **R2**: suavizar limparia a
correlação de +0,80 entre RR\* e o próprio aperto monetário, e custaria 19 trimestres e a crise de
2008 inteira. O que a decisão comprou, medido depois de tomada, foi mais do que amostra — ver §2.

**A questão do nível e da regressão sem intercepto fica parada**, por decisão explícita: *"Não
entendi o ponto do nível e regressão sem intercepto, mas não quero mexer nisso agora."* É o item
**R3**. É premissa declarada, não defeito escondido: a tabela de janelas mede o que ela custa.

**A base tem duas defasagens**, promovidas de coluna de robustez a especificação em
2026-09-21: *pode colocar as duas defasagens*. Fecha o item **R1**, e o comparativo que motivou a
troca fica registrado lá.

**`dI` é medido na Focus de 18 meses, por enquanto**, escolhido em 2026-09-21 depois de as três
leituras serem medidas: *"vamos usar o Focus 18 meses por enquanto, e deixa anotado nas pendências
para olharmos o de 12 meses novamente."* O "por enquanto" é o item **R5**. A projeção do Copom sai
de cena aqui — *"as projeções do BC eu vou olhar em outra análise"* — e o que foi medido dela fica
registrado em R5 para quem for fazer essa análise.

**A Selic entra pela média do trimestre**, como o plano pede. Medido, a convenção quase não decide:
pelo fechamento o efeito de longo prazo vai de 2,62 para 2,53. `selic_fim` fica no painel para a
divergência ser visível.

---

## 1. O que está aberto na forma atual

### R1 — Uma ou duas defasagens · *RESOLVIDO em 2026-09-21: duas*

O plano punha uma defasagem na base e a segunda como *coluna de robustez*. A coluna de robustez
ganhou em tudo o que se pode medir, e o usuário promoveu-a. O comparativo fica aqui porque é o
registro do porquê — cada forma na sua própria amostra:

| | uma defasagem | duas defasagens | BC publicado |
|---|---|---|---|
| n | 81 | 80 | |
| soma das defasagens | 0,849 | **0,865** | 0,90 |
| efeito de longo prazo | 3,75 | **2,62** | 2,03 [1,47; 2,64] |
| R² centrado | 0,912 | **0,952** | |
| RMSE | 0,763 | **0,566** | |
| autocorrelação do resíduo (1ª ordem) | 0,61 | **−0,00** | |
| Ljung-Box Q(4) | p 0,000 | **p 0,683** | |
| Ljung-Box Q(8) | p 0,000 | **p 0,438** | |

*Re-medida em 2026-09-22 na Focus de 18 meses, que é o `dI` da base desde a decisão de R5. A versão
anterior desta tabela estava na Focus de 12 meses e não foi refeita quando o horizonte mudou.*

Com uma defasagem só o resíduo carrega 0,61 de autocorrelação e o Ljung-Box rejeita nos dois
horizontes — não é rejeição de fronteira, é a conta não capturando a dinâmica de suavização. Com
duas, **o resíduo fica indistinguível de ruído branco** e o efeito de longo prazo continua dentro do
intervalo publicado.

E o perfil em corcova aparece sozinho: `r1 = +1,434` (t 14,0) e `r1b = −0,570` (t −5,5), a mesma
forma que o BC estima com `t1 = 1,48` e `t2 = −0,58` — e, na base de hoje, **os dois dentro** dos
intervalos publicados. *Isto mudou com a decisão de R5: na Focus de 12 meses os dois ficavam fora,
pelo lado de baixo (1,329 e −0,482), e era assim que este parágrafo estava escrito.* A soma, 0,865,
segue abaixo dos 0,90 dele — é o único dos quatro números que não encosta.

**Um efeito colateral da promoção, e ele é grande:** com duas defasagens a escolha da janela de
RR\* encolhe muito. Na mesma amostra comum de 53 trimestres, os efeitos de longo prazo das sete
janelas vão de **2,52 a 3,17**, contra **4,78 a 7,30** com uma defasagem só — a faixa cai de 2,5
para 0,65 ponto. O que parecia sensibilidade a RR\* era, em boa parte, a defasagem faltando.

**O que NÃO se deve dizer é que todas entram no intervalo publicado**: com duas defasagens só 1 das
7 cai dentro de [1,47; 2,64] nessa amostra, contra 0 das 7 com uma defasagem. A amostra comum de 53
trimestres desloca todas para cima — na amostra própria, que é a que a página usa, a base dá 2,62 e
entra. O ponto que a comparação sustenta é o encolhimento da faixa, não a entrada no intervalo.

A forma de uma defasagem continua estimada, em `COMPARAR["lag1"]`.

### R2 — Com a série crua, RR\* correlaciona +0,80 com o próprio aperto monetário · *decisão tomada, pendência aberta*

É a metade do trade-off que a decisão de §0 deixou de pé. Uma âncora `RR* + Meta` que se move junto
com a política faz a regra **subestimar sistematicamente o quanto ela está apertada**: quando o
Copom aperta, a curva real longa sobe junto, a âncora sobe, e o desvio medido fica menor que o real.
É o mesmo defeito que reprovou o filtro HP como RR\* na equação (H) — lá o HP dava 7,7% e dizia que
uma Selic de 15% quase não apertava.

O tamanho está medido em §2: entre a série crua e a média de 7 anos, o nível de RR\* hoje vai de
7,67% para 5,46% e o efeito de longo prazo estimado sobe de 2,83 para 3,09 (na amostra comum às
sete). **Quanto mais limpa a RR\*, maior o efeito estimado** — a direção que a teoria prevê, e a
confirmação de que a contaminação de fato atenua o coeficiente. A subida não é monótona: ela cresce
até a média de 5 anos (3,17) e recua na de 7, que é a janela em que a amostra já ficou curta.

**Uma saída foi testada e NÃO funciona: a taxa a termo.** A ideia era que a taxa a termo de 5 a 10
anos remove por construção a política esperada dos próximos cinco anos, então ela escaparia da
contaminação. Medido (aba *Taxas a termo* da planilha, 2006T2→2026T2):

| candidata a RR\* | corr. com o aperto | corr. com a NTN-B de 2a | efeito de longo prazo |
|---|---|---|---|
| NTN-B 10 anos (em uso) | +0,80 | 0,964 | 2,62 |
| NTN-B 20 anos | +0,77 | 0,944 | 2,50 |
| a termo real 2a→5a | +0,72 | 0,918 | 2,77 |
| a termo real 5a→10a | +0,70 | 0,907 | 2,66 |
| a termo real 10a→20a | +0,69 | 0,875 | 2,44 |

O melhor segmento tira 0,11 da correlação e é o mais ilíquido da curva. **O motivo está na coluna
do meio: todo ponto da curva real correlaciona pelo menos 0,88 com a NTN-B de 2 anos**, e é ela que
domina a medida de aperto — desvio de 2,30 contra 1,41 na ponta de 10 anos, com correlação de 0,965
entre as duas. A curva se move em bloco. A contaminação é um **fator de nível comum**, não uma
componente de política de curto prazo que se recorte escolhendo outro vértice.

Consequência direta: **separar expectativa de prêmio exige um modelo**, não um recorte da curva —
strip pela pesquisa Focus (o dado existe: `expc_focus_copom` reunião a reunião desde 2004, e a Selic
anual do Focus alcança ~4,5 anos) ou uma estrutura a termo afim tipo ACM. É o item R11.

O achado colateral é tranquilizador para a forma atual: as sete candidatas dão efeito de longo prazo
entre **2,44 e 2,77, todas dentro do intervalo publicado**, e resíduo limpo em todas. A NTN-B de 10
anos continua sendo a única com os três parâmetros dentro dos intervalos do BC.

Dois corretivos que continuam abertos, nenhum feito: voltar à média móvel quando a NTN-B tiver
histórico para que 5 anos não custem 19 trimestres, ou deixar a regressão ter intercepto (R3), que
devolveria parte do deslocamento como número.

### R3 — A regressão não tem intercepto para absorver erro de nível em RR\* · *decisão tomada, pendência aberta*

Numa regressão **sem intercepto**, um erro constante `c` no nível de RR\* deixa um termo omitido de
`c·(1 − soma das defasagens)` — não há constante livre para absorvê-lo, e ele enviesa os dois
coeficientes. Com a soma das defasagens em 0,865, cada 1 p.p. de erro no nível de RR\* vira
0,14 p.p. de constante omitida.

O corretivo é deixar a regressão ter um intercepto e ler nele o quanto a RR\* escolhida está
deslocada. Custa um grau de liberdade e devolve o viés como número em vez de premissa. O usuário
optou por não tratar isso agora.

### R4 — O resíduo · *RESOLVIDO junto com R1*

Com uma defasagem a autocorrelação de primeira ordem era 0,61 e o Ljung-Box rejeitava nos dois
horizontes. Com duas ela vai a **−0,00** e os dois testes passam com folga larga (p 0,683 e 0,438).

Fica registrado porque **(E) e (H) rejeitam na forma escolhida** e esta não — a (R) não carrega essa
ressalva. O que não vale dizer é que ela seja a única: as quatro contas por grupo de preço da curva
de Phillips também passam (p 0,341, 0,211, 0,202 e 0,471).

### R5 — Voltar a olhar a Focus de 12 meses · *decisão provisória tomada: 18 meses*

O usuário escolheu o horizonte de 18 meses **por enquanto** e pediu que a de 12 ficasse anotada para
ser reexaminada. Este é o item.

As três leituras, na mesma amostra comum (78 trimestres, 2006T4→2026T2), com duas defasagens:

| leitura de `dI` | `r2` | t | efeito de longo prazo | R² cent. | RMSE | Q(4) |
|---|---|---|---|---|---|---|
| **Focus de 18 meses** (base) | 0,312 | 2,20 | **2,36** | 0,9564 | 0,5458 | 0,535 |
| Focus de 12 meses | 0,263 | 3,15 | 1,78 | 0,9601 | 0,5217 | 0,625 |
| projeção do Copom | 0,422 | 2,77 | 3,25 | 0,9590 | 0,5293 | 0,493 |

**O ajuste não separa as três** — 0,4% de R² e 4,6% de RMSE entre a melhor e a pior, resíduo limpo
nas três. O que decidiu foi outra coisa: **com a de 18 meses os três parâmetros comparáveis caem
dentro dos intervalos publicados do BC**, e com a de 12 meses os dois pesos de suavização ficam
fora, pelo lado de baixo (+1,329 contra [1,41; 1,54] e −0,482 contra [−0,63; −0,52]). Alongar o
horizonte da expectativa alongou junto a suavização estimada.

**Os dois motivos para reexaminar, que é o que o "por enquanto" registra:**

1. O efeito de longo prazo, 2,62, **encosta no teto** do intervalo publicado (2,64). Sem margem
   própria — que é o item R8 — a afirmação "está dentro" é mais frágil do que parece: qualquer
   intervalo de confiança ao redor de 2,62 cruza a borda.
2. A de 12 meses **ajusta um pouco melhor** (R² centrado 0,957 contra 0,952; RMSE 0,537 contra
   0,566) e é a que o BC usa na equação (3) dele (`pi^e_{t,t+4|t}`). Cair dentro de três intervalos
   publicados e ajustar melhor não apontam para o mesmo lado aqui, e essa tensão não se resolve por
   medição — é escolha.

**A projeção do Copom sai do escopo desta equação** por decisão do usuário, que vai examiná-la em
outra análise. O que ficou medido aqui e vale para essa análise:

- ela dá o maior `r2` das três (0,422), mas isso é quase todo **escala**: o desvio medido por ela
  tem desvio-padrão de 0,53 contra 0,92 da Focus de 12 meses, razão 1,7, e a razão dos coeficientes
  é 1,6;
- o **cenário não é a explicação**. A hipótese natural era que o cenário de `juros_esperado`
  condiciona na trajetória de juros da Focus e portanto já embute a resposta da política, o que
  seria endógeno à regra. Testado contra o cenário de **juros constantes**, na janela em que os dois
  existem (60 trimestres até 2024T3): dispersões praticamente iguais (0,570 e 0,565) e **o mesmo
  efeito de longo prazo, 2,47 e 2,48**, enquanto a Focus dava 1,50 ali. A hipótese não se sustentou;
- o que resta é de **nível**: o Copom projeta sistematicamente mais perto da meta que o mercado —
  desvio médio de +0,25 p.p. contra +0,67 da Focus de 12 meses, e hoje 0,70 contra 1,05. É um
  objeto diferente, medido 6 trimestres à frente, onde a projeção já convergiu boa parte do caminho.

As três séries correlacionam 0,79 (as duas Focus entre si), 0,76 (Focus de 18 meses × Copom) e 0,67
(Focus de 12 meses × Copom).

### R6 — Não há termo de hiato na regra · *ausente por especificação, nos dois lados*

Nem o plano nem a equação (3) do BC põem o hiato na regra de juros. Fica registrado porque é a
primeira pergunta de quem lê uma Taylor e não a encontra: a resposta é que o hiato entra
indiretamente, pela expectativa de inflação, e que testá-lo aqui seria mudar a especificação.

---

## 2. O que foi medido e está DESCARTADO

### As sete janelas de RR\*, e o trade-off que a decisão resolveu

`corr(RR*, aperto)` é contra `g_rr`, a inclinação da curva real que a equação (H) usa como medida de
aperto monetário. As colunas de estimativa estão na **amostra comum às sete linhas**, que a média de
7 anos limita a **53 trimestres (2013T2→2026T2)**. *Re-medida em 2026-09-22, na forma base de hoje —
duas defasagens e Focus de 18 meses. Os números anteriores deste bloco eram de uma defasagem e da
Focus de 12 meses, e ficaram para trás quando a forma mudou.*

| janela | corr(RR\*, aperto) | nível hoje | amostra própria | efeito de longo prazo | R² cent. | Q(4) |
|---|---|---|---|---|---|---|
| **crua (em uso)** | **+0,80** | **7,67%** | **80** (2006T3) | **2,83** | 0,973 | **0,981** |
| 1 ano | +0,76 | 7,54% | 77 | 2,52 | 0,984 | 0,187 |
| 2 anos | +0,63 | 7,29% | 73 | 2,69 | 0,986 | 0,074 |
| 3 anos | +0,38 | 6,76% | 69 | 2,93 | 0,987 | 0,059 |
| 4 anos | +0,18 | 6,57% | 65 | 3,07 | 0,989 | 0,082 |
| 5 anos | −0,06 | 6,30% | 61 (2011T2) | 3,17 | 0,989 | **0,041** |
| 7 anos | −0,35 | 5,46% | 53 | 3,09 | 0,989 | **0,032** |

**O diagnóstico de resíduo separa as linhas, e separa a favor da série crua** — o que não era
verdade na versão anterior desta tabela, medida com uma defasagem, em que o Ljung-Box rejeitava nas
sete. Com duas defasagens a série crua deixa o resíduo praticamente sem padrão (p 0,981) e as duas
janelas mais longas **rejeitam a 5%**. O R² centrado anda na direção contrária, de 0,973 a 0,989,
mas a diferença é de segunda casa e ele não distingue nada útil aqui: uma âncora mais lisa deixa
menos para a conta explicar, o que sobe o R² sem que a conta tenha melhorado.

**O que a decisão pela série crua comprou, medido na amostra própria de cada janela**, que é o que a
tabela acima não mostra (ela iguala todas em 53 linhas; a decisão devolve 80):

- o efeito de longo prazo da forma base fica em **2,62**, dentro do intervalo publicado;
- as **duas** dummies de crise têm suporte e ficam firmes (t **−2,50** e **−4,82**). A de 2008 já
  sai da conta na média de **4 anos** por não ter nenhum trimestre na amostra, e nas de 5 e 7 anos
  também;
- o resíduo fica **limpo**: Q(4) p **0,683**, contra **0,014** com a média de 5 anos — a única das
  sete que rejeita na própria amostra.

A amostra maior não custou ajuste: melhorou os três diagnósticos ao mesmo tempo. O que ela não
resolve é R2.

Para referência, o que as outras fontes dizem do mesmo objeto hoje: o BC declara **5,0%** no RPM; o
filtro HP com cauda Focus dá **7,7%**; a curva real descontado o prêmio de maturidade dá **~6,45%**.

**Três amostras aparecem neste arquivo e elas não são a mesma** — cada tabela usa a janela comum das
linhas que compara, que é o único jeito de as linhas serem comparáveis entre si:

| tabela | amostra | n | por quê |
|---|---|---|---|
| a do topo, e a de R1 | 2006T2→2026T2 (2006T3 com duas defasagens) | 81 / 80 | cada forma na sua |
| R5 | 2006T4→2026T2 | 78 | a projeção do Copom não tem os T3 de 2006 e 2007 |
| a de janelas acima | 2013T2→2026T2 | 53 | a média de 7 anos só começa aí, e com duas defasagens |

É por isso que a série crua lê efeito **2,83** na tabela de janelas e **2,62** na do topo: são 27
trimestres de diferença, não duas contas. A coluna de nível de RR\*, essa sim, é lida na ponta da
série **completa** de cada janela — de propósito, porque o nível de hoje é o que se quer confrontar
com o 5,0% do BC (é o item R9).

### A expectativa Focus de horizonte longo: publicada só desde 2021, reconstruída desde 2001

A série rolante publicada (`expc_focus`, horizonte `24m`, suavizada) existe e é limpa, mas começa em
**2021-03-31** — cinco anos, contra os vinte e cinco que a regra de juros precisaria. **Nenhuma
série publicada de horizonte longo tem histórico anterior a 2021**: a única de história longa é a de
12 meses, que vai a 2001.

A reconstrução vem da pesquisa **anual** do Focus, que vai a 2000 e projeta até 2030, interpolada no
horizonte certo. O horizonte certo é **h = 1,5 ano** e não 2,0: a janela de 24 meses acumula os
meses 12 a 24, então o centro dela está a 18 meses, e os pontos anuais do Focus já vêm datados no
meio do ano. O horizonte saiu da definição da janela, e o dado confirmou:

| interpolar em | erro médio contra a publicada de 24m |
|---|---|
| h = 1,0 | 0,365 p.p. |
| **h = 1,5** | **0,071 p.p.** |
| h = 2,0 | 0,246 p.p. |

Nos 1.370 boletins em que as duas coexistem: erro máximo 0,681, correlação 0,931, viés −0,027. É
`panel.focus_ipca_2a()`, e ela cobre 2001T4→hoje.

**O que continua sem gabarito é 2001–2021**, e isso é limitação e não descuido: a validação só pode
ser feita onde as duas séries coexistem. O que se afirma é que o método reproduz a publicada com
0,071 p.p. nos cinco anos em que dá para conferir, e que é o mesmo método que
`focus_selic_12m_diario()` usa para a Selic — não que o trecho antigo esteja verificado.

### A projeção do Copom: um vintage por trimestre, sem buraco desde 2008

`pm_copom_projecoes` marca qual linha é o horizonte relevante (`horizonte_relevante=1`), então não há
escolha de horizonte a fazer — ele é **6 trimestres à frente** em toda a amostra útil, o que o põe
entre a Focus de 12 meses e a de 2 anos. Cenário de `juros_esperado` (condicionado na trajetória de
juros da Focus), que é o que o Copom trata como referência desde 2017.

Cobertura: um vintage por trimestre, sem buraco, de 2008T1 até hoje. Faltam os T3 de 2003 a 2007 —
cinco trimestres, dos quais dois (2006T3 e 2007T3) caem dentro da amostra desta equação e são o que
encurta a tabela de R5 para 78.

### A meta na âncora é sempre a de 12 meses, inclusive com `dI` de 2 anos

Não é descuido: a âncora `RR* + Meta` é o nível nominal de repouso, e o alvo do Copom é a meta
vigente, não uma meta de dois anos à frente. O horizonte de 24 meses entra só na medida do *desvio*,
onde `meta_24m` existe para casar com `pi_e_2a` pelos mesmos pesos de `META_W_Q` deslocados um ano.
Comparar uma expectativa de dois anos contra a meta de doze meses injetaria o degrau de janeiro que
`META_W_Q` foi escrito para evitar.

### O que o `r2` NÃO é

O `t3 = 2,03` que o BC publica está **dentro** do colchete da equação (3) dele, multiplicado por
`(1 − t1 − t2) = 0,10`. O nosso `r2` está fora. Comparar os dois direto erra por um fator de dez — o
objeto comparável é `r2 / (1 − soma das defasagens)`, que é o que o módulo e a página imprimem ao
lado do publicado. Mesma classe do `h2` da equação (H), que também não era o `b2` do BC.

---

## 3. O que ainda não foi feito

### R7 — A aba de Juros · *RESOLVIDO em 2026-09-22*

A aba existe. Traz a Selic contra a conta e contra a âncora no mesmo gráfico (a distância entre as
duas últimas **é** o aperto), a decomposição do desvio em relação à âncora, a tabela de pesos com o
peso da âncora marcado como conta de sobra, e um bloco de método com as quatro tabelas: as sete
janelas de RR\*, as formas testadas, o diagnóstico de resíduo e a comparação com o que o BC publica.

O painel também entrou na aba de Dados: `selic`, `meta_12m`, `pi_e_2a`, `meta_24m` e `pi_bcb`, em
três gráficos novos. `selic_fim` continua fora, como `g_rr_fim` e `de_fim` — são colunas paralelas
de convenção, e desenhá-las ao lado da principal só duplicaria o gráfico.

**Duas coisas que a construção da aba encontrou e consertou**, ambas de medição e não de tela: a
amostra comum da tabela de janelas não incluía a segunda defasagem, então a linha de 7 anos rodava
com um trimestre a menos que as outras seis enquanto a legenda dizia "mesma amostra"; e a coluna de
início de cada janela era calculada com uma defasagem só. Os números de §2 foram re-medidos.

### R8 — Margem e t do efeito de longo prazo · *mesma álgebra do P16, do E7 e do H8*

`r2 / (1 − soma)` é uma razão de estimativas e a página imprime o ponto sem margem. O método delta
resolve, e aqui **importa mais** do que nas outras três equações: é o número que se compara com o
intervalo publicado do BC, e dizer que 2,63 está dentro de [1,47; 2,64] sem margem própria é afirmar
menos do que parece. É o mesmo item nas quatro equações e vale fazer de uma vez.

### R9 — O nível de RR\* na tabela de janelas tem proveniência diferente dos coeficientes · *limitação declarada*

As sete linhas usam a mesma amostra comum para os coeficientes, que é o certo para compará-los. Mas
o **nível** de RR\* de cada linha é lido na ponta da série completa daquela janela, não na amostra
comum — as duas colunas têm proveniências diferentes, e isso fica dito na legenda em vez de
corrigido, porque o nível de hoje é justamente o que se quer confrontar com o 5,0% do BC.

### R11 — Separar expectativa de prêmio de maturidade · *proposta apresentada, não executada*

Saiu do teste de R2: a decomposição `taxa longa = média das taxas curtas esperadas + prêmio` não se
obtém recortando a curva, precisa de modelo. Quatro caminhos foram levantados em 2026-09-21, do mais
barato ao mais defensável:

1. **Taxa a termo** — testado, e é o que reprovou (está em R2 acima).
2. **Strip por pesquisa.** Emendar `expc_focus_copom` (reunião a reunião, desde 2004-11, 88.502
   linhas) com a Selic anual de `expc_focus_periodo` (alcance mediano de 4,52 anos, desde 2000) para
   montar o caminho esperado; a média dele até *n* anos é a componente de expectativa e o resto é
   prêmio. **O limite é duro:** a pesquisa para em ~4,5 anos, então dá para decompor até 5 anos sem
   hipótese nenhuma, e 10 anos exigiria uma. ~150 linhas.
3. **Modelo afim tipo ACM** — cinco regressões, sem otimizador; 8 vértices mensais desde 2006 ≈ 240
   observações. Três coisas a verificar antes: se os vértices da B3 são taxa zero ou rendimento com
   cupom (a curva bate com a indicativa da ANBIMA, que é de título com cupom); a distorção do
   carrego do IPCA na ponta curta da curva real; e o viés de amostra pequena, que achata a
   componente de expectativa. ~250 linhas.
4. **Afim aumentado por pesquisa**, no espírito do Kim-Wright — corrige o viés de (3) pondo a Focus
   como observação ruidosa. A maquinaria de espaço de estados já existe em `modelo_agregado.py`.

Alimentaria três itens de uma vez: o RR\* limpo de R2; um termo de condições financeiras para a
curva IS, que é a pendência H5; e a separação do `g_rr` da equação (H) em política esperada contra
prêmio.

**Um benchmark que não custa nada:** a série ACM do Fed de NY (`THREEFYTP10`) está confirmada como
disponível no FRED e **não carregada** (ver `analytics/us/monetary_policy/fontes_dados.md`). Serve
de gabarito para validar uma implementação de (3) contra resultado publicado.

### R12 — Estimar a neutra, em vez de escolher um proxy · *intenção do usuário, 2026-09-22*

Dito pelo usuário ao ver que o BC usa duas neutras diferentes: *"vamos seguir dessa forma, por
enquanto, mas minha ideia é estimar isso melhor."* As duas formas atuais ficam; este item é o
registro do que teria de acontecer para substituí-las.

**O BC não tem uma neutra, tem duas.** São dois estados latentes no mesmo filtro de Kalman —
`rr_IS` e `rr_TAY` —, cada um entrando na sua equação, compartilhando a tendência comum `rr_trend`
e diferindo pelo desvio próprio. Medido na réplica desta casa
(`monetary_policy/data/modelo_estados.csv`, 99 trimestres): correlação **0,994**, diferença média
**0,12 p.p.**, e hoje **7,81% na IS contra 8,28% na Taylor**. São próximas, não iguais. E nenhuma
das duas é a que o BC **anuncia** nas projeções (4,50% → 4,75% em jun/2024 → 5,00% em dez/2024),
que fica **2,8 p.p. abaixo** do que o filtro dele estima — a neutra declarada e a neutra do modelo
são objetos diferentes, e essa diferença sozinha muda a leitura de quão apertada está a política.

**Aqui não há nenhuma das duas, e por dois contornos diferentes:**

| | o que faz as vezes de neutra | o que isso custa |
|---|---|---|
| (R) Taylor | NTN-B de 10 anos crua, em nível | R2: correlaciona +0,80 com o próprio aperto |
| (H) IS | nada — o aperto é a inclinação 2a−10a | não há leitura de nível; ver H6 |

Os dois foram escolhidos equação a equação, medindo, e cada um tem a sua justificativa registrada.
O que nenhum dos dois tem é uma estimativa de equilíbrio que se sustente sozinha.

**Três caminhos, e eles não custam o mesmo:**

1. **Importar `rr_IS` e `rr_TAY` do modelo agregado.** A maquinaria está pronta e validada
   (`modelo_agregado.estados()`), então é trabalho de encanamento. O que ela traz junto é a
   identificação do modelo do BC inteira — inclusive o suavizador de dois lados, que é o mesmo
   look-ahead pelo qual o HP foi descartado na (H).
2. **Deduzir do mercado, via R11.** Separando expectativa de prêmio de maturidade sai um RR\* de
   preço observado, sem filtro e sem look-ahead. É o caminho que casa com a escolha já feita nas
   duas equações, e o strip por pesquisa alcança 5 anos sem hipótese nenhuma.
3. **Estimar em conjunto aqui**, como estado latente das duas equações ao mesmo tempo — que é
   exatamente o que o plano da pasta declarou **fora de escopo** (*"sem estimação conjunta por
   filtro de Kalman"*). Reabrir isso é decisão de plano, não de implementação.

**O que se destrava se isso for feito:** R2, R3 e R9 nesta equação, e a tabela inteira da §2 de
[`pendencias_is_eq.md`](pendencias_is_eq.md) — ver **H9** lá, que é o mesmo item visto do outro
lado. Nada disso bloqueia a forma atual.

### R10 — Sem vintage, e é a única das quatro assim · *registro, não pendência*

A Selic é observada em tempo real e não é revista; RR\* é preço de mercado, também nunca revisto; a
meta é anunciada. A projeção do Copom é, por construção, o que ele publicou na época. **A única
série desta equação que poderia ser revista é a Focus, e ela não é.** Então o problema que a equação
(H) tem com o hiato não existe aqui, e vale dizer isso na página em vez de deixar o leitor supor.

---

## 4. Ordem sugerida

1. **R8** — o método delta, nas quatro equações de uma vez. Subiu para primeiro porque o efeito de
   longo prazo da forma base encosta no teto do intervalo publicado: sem margem própria não dá para
   dizer o quanto isso significa, e é esse número que sustenta a escolha de R5.
2. **R5** — reexaminar a Focus de 12 meses, depois de R8 dar a margem.
3. **R3** e **R2** — o intercepto e a volta à média móvel, quando o usuário quiser voltar a isso.
4. **R11** — o strip de expectativa contra prêmio, se e quando o RR\* voltar a incomodar. É o
   caminho que o teste da taxa a termo deixou como único viável, e é o caminho 2 de R12.
5. **R12** — estimar a neutra. É o item que engloba R2, R3 e R9, e o usuário já sinalizou que quer
   chegar lá; não tem data e não bloqueia.
6. **R6**, **R9**, **R10** — registro; nenhum bloqueia. **R1**, **R4** e **R7** estão fechados.
