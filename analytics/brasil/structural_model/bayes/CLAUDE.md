# Estimação bayesiana das equações do modelo estrutural

Pasta aberta em **2026-09-22**, por decisão do usuário: *"Estou considerando usar um modelo
Bayesiano e começamos com o modelo de juros."* Hoje **cinco equações, as cinco no simulador**:
(R) regra de juros, (F) câmbio, (E) expectativas, (H) curva IS e (I) curva de Phillips
desagregada, a última a entrar, em 2026-09-28. A regra, do
usuário em 2026-09-25: *"no sistema vamos sempre usar o bayes para todas as equações"* — o que roda
no simulador é sempre o posterior; as abas por equação publicam a estimativa pontual, que fica como
gabarito.

| arquivo | o que é |
|---|---|
| `taylor_bayes.py` | a equação (R) por MCMC (PyMC/NUTS), cinco variantes de priori/parametrização |
| `fx_bayes.py` | a equação (F), a mesma do Ridge — existe porque Ridge não tem posterior para virar faixa |
| `expectations_bayes.py` | a equação (E), a mesma do MQ, com a soma-um imposta na forma |
| `is_bayes.py` | a equação (H), a mesma do MQ, com o aperto medido contra a âncora da regra de juros |
| `phillips_bayes.py` | a equação (I), as quatro do MQ (serviços, alimentação, industriais, monitorados), mais o que só existe no sistema: efeito do hiato no cheio, repasse, estabilidade das quatro juntas |
| `data/*_bayes.json` | o resumo de cada variante, gravado a cada execução |
| `data/*_draws.json` | **1.000 desenhos afinados da variante base** de cada uma — é o que o simulador do relatório lê |

**As quatro seguem o mesmo desenho, e isso é o que as torna verificáveis**: nenhuma remonta a
matriz de regressão. Cada uma chama a mesma `montar()` do módulo de estimação pontual, corta na
mesma data, e só troca o estimador — então `conferir()` pode medir a distância entre a mediana do
posterior e o coeficiente pontual em desvios do próprio posterior, e o `main()` imprime as duas
colunas lado a lado. Se divergirem, ou a priori está apertando ou a matriz deixou de ser a mesma,
e as duas hipóteses são visíveis.

| equação | contra | pior distância | R² | RMSE |
|---|---|---|---|---|
| (R) | MQ | — (parametrização própria) | 0,957 | 0,537 |
| (F) | Ridge | 0,042 desvio | **0,8261 contra 0,8261** | **3,448 contra 3,448** |
| (E) | MQ | 0,061 desvio | **0,7778 contra 0,7778** | **0,5692 contra 0,5692** |
| (H) | MQ | 0,039 desvio | **0,8702 contra 0,8703** | **0,6361 contra 0,6361** |
| (I) | MQ | 0,083 desvio (pior das quatro) | serviços 0,6263 · alimentação 0,2935 · industriais 0,5235 · monitorados 0,0694 — iguais ao MQ na 4ª casa | cheio reconstruído **0,6166 contra 0,6159** |

### A (I): quatro posteriores independentes, e o que só existe com as quatro juntas

`phillips_sub.matriz()` foi separada de `estimar_uma()` para o amostrador ler a mesma matriz — a
refatoração não move nenhum número do MQ. As quatro são estimadas separadamente, como no MQ;
prioris e verossimilhanças independentes fazem o posterior conjunto ser o produto, então parear o
desenho `s` das quatro é legítimo, e `phillips_draws.json` grava os desenhos **já pareados**.

Com os pesos do fim da amostra e a **expectativa parada**, o sistema mede: 1 p.p. de hiato por um
ano soma **0,23 p.p.** ao IPCA de 12 meses (HDI [0,03; 0,44]); uma depreciação de 1% chega **3,3%**
ao nível do IPCA em um ano e **5,8%** no longo prazo; e o laço alimentação ↔ câmbio dentro do
trimestre tem ganho **0,013** — resolver os dois juntos em vez de em sequência muda o efeito em
1,3%. As formas fechadas de longo prazo (com o multiplicador da indexação dos monitorados) batem com
400 trimestres simulados a 2,3e-10.

**4,0% dos desenhos são explosivos, e todos por um peso da expectativa negativo** — 92% deles em
bens industriais (inércia + média móvel > 1), 8% em serviços. Ficam no posterior, pela mesma razão
da (H): tirá-los seria impor estacionariedade como priori. Na amostra desde 2006T2 sobem a 8,3%.

Dois achados que são decisão de especificação, não de estimador, e ficam registrados em vez de
corrigidos: a indexação dos monitorados ao cheio sai **negativa** (−0,21, 29% da massa acima de
zero) com R² de 0,07; e o hiato não entra em alimentação (−0,002, metade da massa de cada lado).

### A priori da (H) é autoescalada, como a da (F) — e a razão é a mesma, não a cópia

Os quatro termos vivem em unidades diferentes: `h1` multiplica o próprio hiato, `h2` multiplica
p.p. de aperto, e as crises são degraus de 0 ou 1. `N(0, sd(y)/sd(x))` por termo, que para `h1`
dá exatamente `N(0, 1)` porque o regressor é o próprio hiato defasado. A (E) usou uma priori só
porque lá os dois pesos dividem unidade — copiar a regra de uma para a outra seria copiar a
conclusão sem a razão. A variante `larga` (×4) move a mediana de `h2` em 0,0001.

### E o repouso por simulação finita reprovava desenho LENTO, não errado

A primeira versão de `repouso_draws()` da (H) iterava 4.000 trimestres e reprovou o posterior
inteiro: pior desvio de zero **4,37**. Não havia defeito nenhum — havia desenhos com `h1` a um
fio de 1 (0,99997 guarda 87% de um hiato depois de 4.000 trimestres), que voltam a zero pela
álgebra e que uma simulação finita não alcança. A correção separa três grupos em vez de
misturá-los: **explosivos** (`|h1| ≥ 1`, 0,49% — ficam no posterior, porque tirá-los seria impor
estacionariedade como priori), **lentos** (0,99 < `|h1|` < 1, 0,38% — contados, não afirmados) e o
resto, onde a afirmação é feita (pior desvio **8,7e-18**). Um teste que não sabe o que ele não é
capaz de afirmar reprova o que é verdadeiro.

### A priori da (E) é UMA só, e isso é conclusão e não economia

Na (F) ela precisava ser **autoescalada** por canal, porque os betas vivem em escalas muito
diferentes mesmo depois da padronização. Na (E) os dois regressores estão na mesma unidade (p.p.
de desvio contra a meta) e os dois coeficientes são **pesos**, cujo intervalo útil é [0, 1]:
`N(0, 1)` cobre isso várias vezes. A variante `larga` (×4) devolve os mesmos números.

E a priori do BC **não** entra na (E), pela mesma razão que a aba já declara: o `f2` da eq. (5)
multiplica a previsão do próprio modelo quatro trimestres à frente e o nosso `e2` multiplica a
inflação realizada. São regressores diferentes — transplantar o número poria a priori no lugar
errado.

### E a restrição da (E) vale DESENHO A DESENHO

`peso_meta` não é amostrado: ele é `1 − e1 − e2`. A consequência é estrutural e `repouso_draws()`
a afirma sobre a amostra inteira, não sobre a mediana — com a inflação na meta a conta devolve a
meta, pior desvio **1,78e-15**. Num simulador isso importa mais do que na estimação: é cada
desenho que roda.

Duas medições que vêm de graça e valem imprimir: **0,00% da massa do posterior cai fora do
simplex** (nada na priori obriga), e o repasse de longo prazo `e2/(1−e1)` é propagado desenho a
desenho em vez de calculado da mediana — a razão das medianas não é a mediana da razão.

## Quem consome isto, e o que isso obriga

A aba **Structural Model** do relatório (`../simulator.py`) roda as cinco equações com estes
pesos, e a faixa sai de resolver o laço inteiro para cada um dos 1.000 desenhos, com o desenho `s`
de cada equação entrando junto. Desde que a (I) fechou o laço, a faixa de cada variável carrega a
incerteza de todas as equações que a alimentam — com as cinco ligadas, das cinco. Os posteriores
foram estimados separadamente, então parear amostras independentes é amostrar do produto — não há
correlação a preservar; a (I) grava os quatro grupos já pareados entre si. Duas consequências:

- **A geração do relatório NÃO roda MCMC.** Ela lê os cinco `data/*_draws.json`. Reestimar é um passo
  próprio e explícito, como os três passos do `monetary_policy` — três minutos de amostrador dentro
  de uma geração que deveria levar segundos seria dívida, não recurso.
- **Mudar qualquer coisa da estimação obriga a regravar os desenhos.** Trocar priori, horizonte de
  `dI`, janela de `RR*` ou amostra e não rodar `salvar_desenhos()` deixa o simulador mostrando os
  pesos velhos, sem nada levantar. O caminho inteiro é uma execução só:
  `uv run python -m analytics.brasil.structural_model.bayes.taylor_bayes`, que grava os dois
  arquivos, seguida de uma regeração do relatório.

```powershell
uv run python -m analytics.brasil.structural_model.bayes.taylor_bayes        # ~3 min
uv run python -m analytics.brasil.structural_model.bayes.fx_bayes            # segundos
uv run python -m analytics.brasil.structural_model.bayes.expectations_bayes  # segundos
uv run python -m analytics.brasil.structural_model.bayes.phillips_bayes      # minutos: 3 variantes x 4 equações
```

**As três têm de terminar no MESMO trimestre**, e `simulator.construir()` levanta se não
terminarem: a janela projetada de uma começaria dentro da amostra da outra, e a tela não teria
como dizer isso.

Roda em ~3 min, sem banco: o painel vem do `data/panel.csv` versionado, para duas execuções darem
o mesmo número. `dados(df=panel.construir())` usa o painel ao vivo.

---

## O que muda, e o que não muda

**Não muda nada da especificação.** Mesma equação, mesma amostra (2006T3–2026T2, 80 trimestres,
pela mesma `taylor.montar()`), mesma restrição imposta — o peso da âncora continua sendo
`1 − t1 − t2` por construção, e o que se regride continua sendo o desvio `y = R − RR* − Meta`, sem
intercepto. `RR*` é a NTN-B de 10 anos crua e `dI` é a Focus de 18 meses. **Mudar especificação não
é decisão de quem implementa**; o que muda aqui é só o estimador.

Muda o estimador, e isso compra três coisas:

**1. A parametrização do próprio BC passa a ser estimável.** A equação (3) do boxe põe o
multiplicador *dentro* do colchete, o que torna `t3` o efeito de **longo prazo**:

```
y(t) = t1·y(t-1) + t2·y(t-2) + (1 − t1 − t2)·t3·dI(t) + d08 + d20 + ε
```

`(1−t1−t2)·t3` é um produto de parâmetros estimados, então **MQ não estima essa forma** — é por
isso que o módulo de MQ escreve `r2` fora do colchete e deriva o efeito de longo prazo como a razão
`r2/(1−soma)`. Para o amostrador o produto não custa nada, e com ele `t3` vira parâmetro
**primitivo**, com intervalo próprio. A comparação com o `2,03 [1,47; 2,64]` publicado deixa de
depender de um método de aproximação.

**2. A priori tem onde entrar, e a fonte dela é o próprio BC.** Os números publicados são
posteriores bayesianos com intervalo de credibilidade de 90%, então viram priori normal direto
(desvio = semiamplitude ÷ 1,645): `t1 ~ N(1,480; 0,040)`, `t2 ~ N(−0,580; 0,033)`,
`t3 ~ N(2,030; 0,356)`. Lidos de `taylor.BCB`/`BCB_IC`, que leem de `modelo_agregado` — nada
transcrito, em nenhum dos dois saltos.

**3. R8 deixa de ser pendência.** O efeito de longo prazo passa a ter margem, e ela sai da
distribuição inteira em vez de uma linearização.

---

## As prioris

**As da base foram escolhidas pelo usuário em 2026-09-22**, em caixas uniformes:

```
t1  ~ U[0; 2]        t2  ~ U[-1; 1]        t3 ~ U[0; 5]
d08 ~ U[-10; 0]      d20 ~ U[-10; 0]       sigma ~ meia-normal(2)
```

Vale registrar que elas **reproduzem a caixa do próprio BC** em dois dos três:
`modelo_agregado.CAIXA` traz `t1=(0, 2)` e `t2=(-1, 1)` idênticos, e `t3=(0, 4)` — a escolha do
usuário abriu até 5. As prioris do boxe do BC são uniformes em caixa, então a forma aqui é a mesma
que a da fonte, e não uma convenção nossa.

**Uma uniforme não é "sem informação".** Ela afirma que o parâmetro não pode sair da caixa, e essa
afirmação é forte: dentro da caixa ela não opina, fora dela é proibição absoluta. Se o posterior
encostar numa borda, o número que sai é a borda e não o dado — sem erro, sem aviso. Por isso
`resumo()` mede, para cada caixa, a distância de cada borda até a média **em desvios do posterior**
(acima de ~3 a borda é inerte; abaixo de ~2 ela está cortando cauda).

As outras quatro variantes existem para a base ter contra o que ser lida:

| nome | forma | priori | responde |
|---|---|---|---|
| `usuario` | `t1, t2, t3` | **caixas uniformes (base)** | a especificação escolhida |
| `nossa_livre` | `r1, r1b, r2` | normais largas | o espelho do MQ — é o controle |
| `bc_livre` | `t1, t2, t3` | normais largas | **o que só o nosso dado diz** sobre o efeito de longo prazo |
| `bc_priori` | `t1, t2, t3` | BC publicada | o exercício bayesiano de verdade |
| `bc_priori_larga` | `t1, t2, t3` | BC, desvio ×4 | quanto do posterior é priori e quanto é dado |

**A ressalva que decide qual delas se lê**, e é a principal desta pasta: o BC estimou aqueles
posteriores em dados brasileiros que se sobrepõem quase inteiramente aos nossos. Usá-los como
priori **conta a mesma amostra duas vezes**, e o intervalo que sai é mais estreito do que a
informação independente sustenta. Não é defeito que se conserte com código — é o preço de importar
informação de um estudo feito na mesma população. Por isso a variante que responde *"o que os
nossos 80 trimestres dizem"* é a **difusa**, não a de priori do BC.

---

## Resultado, 2026-09-22

As quatro cadeias convergiram em todas as variantes: **R-hat 1,0000, ESS mínimo 7.418, zero
divergências**. HDI de **90%**, que é o nível em que o BC publica — comparar um HDI de 94% (o
default do ArviZ) com um IC de 90% erraria de leve e para o lado errado.

```
parâmetro      MQ      usuario (base)        bc_livre            bc_priori        BC publicado
                      caixas uniformes    (normais largas)    (priori do BC)
t1           +1,434  +1,439 [1,30; 1,58]  +1,429 [1,30; 1,57]  +1,463 [1,42; 1,51]  +1,48 [1,41; 1,54]
t2           −0,570  −0,569 [−0,70;−0,44] −0,559 [−0,69;−0,43] −0,591 [−0,63;−0,55] −0,58 [−0,63;−0,52]
t3 (ef. lp)   2,616   2,689 [1,22; 4,10]   2,666 [1,23; 4,12]   2,128 [1,59; 2,66]   2,03 [1,47; 2,64]
d08          −0,433  −0,465 [−0,80;−0,03] −0,433 [−0,86;+0,02] −0,425 [−0,87;−0,01]      —
d20          −0,718  −0,713 [−1,21;−0,20] −0,711 [−1,24;−0,20] −0,686 [−1,19;−0,21]      —
soma          0,865   0,870 [0,82; 0,92]   0,870 [0,82; 0,92]   0,872 [0,83; 0,91]   0,90 (sem IC)
meia-vida       3,5     3,6                  3,6                  3,5
σ                —    0,594                0,595                0,589
RMSE         0,5662  0,5664               0,5664               0,5683
R² centrado  0,9519  0,9519               0,9519               0,9515
Q(4) / Q(8)  0,68/0,44  0,71/0,47         0,69/0,49            0,75/0,52
```

### As caixas prendem?

```
        caixa          z(inf)  z(sup)   veredito
t1    [  0; 2]          17,2     6,7    inerte
t2    [ -1; 1]           5,5    20,0    inerte
t3    [  0; 5]           3,1     2,7    corta a cauda direita
d08   [-10; 0]          39,9     2,0    PRENDE — a borda em 0 está decidindo
d20   [-10; 0]          30,4     2,3    corta a cauda
```

`t1` e `t2` estão a muitos desvios de qualquer borda: para eles a caixa não faz nada, e o resultado
é o mesmo das normais largas. `t3` encosta de leve no teto de 5 — o intervalo `[1,22; 4,10]` contra
`[1,23; 4,12]` sem caixa, ou seja o corte é na cauda distante.

**O único que muda de verdade é `d08`**, e é uma decisão econômica embutida: `U[-10; 0]` afirma que
a crise de 2008 **não pode ter empurrado a Selic para cima**. Sem a caixa o intervalo era
`[−0,86; +0,02]`, cruzando zero; com ela vira `[−0,80; −0,03]`, e a média desce de −0,437 para
−0,465. A caixa não está absurda — o sinal é o esperado e o MQ dá −0,433 com t −2,50 —, mas ela está
**impondo** o sinal em vez de deixá-lo ser estimado, e isso tem de estar dito.

### E se tirarmos as dummies de crise?

Medido a pedido do usuário em 2026-09-22, na mesma amostra de 80 trimestres (`rodar(dummies=False)`,
que continua fazendo o `dropna` pelas colunas de crise, para as duas colunas serem comparáveis):

```
                    com d08/d20        sem dummies
t1                +1,439 [1,30; 1,58]  +1,508 [1,37; 1,64]
t2                −0,569 [−0,70;−0,44] −0,619 [−0,75;−0,49]
soma               0,870                0,890      <- o BC publica 0,90
meia-vida            3,6                  4,0
efeito de lp      +2,689 [1,22; 4,10]  +2,798 [1,22; 4,49]
sigma              0,594                0,616
RMSE               0,5664               0,5948     +5,0%
R² centrado        0,9519               0,9469
Ljung-Box Q(4)/Q(8)  0,71 / 0,47          0,53 / 0,53
maior resíduo      2009T2  −1,56        2009T2  −2,07
```

**Nada quebra.** As duas dummies valem ~5% de RMSE, e os coeficientes se movem pouco: `t1` e `t2`
continuam dentro dos intervalos publicados pelo BC nas duas colunas.

Três leituras:

- **A persistência sobe**, de 0,870 para 0,890. Sem as dummies os trimestres de crise — em que a
  Selic andou muito e a regra não explica por quê — são lidos como inércia extra, e é isso que
  empurra `t1 + t2` para cima. Efeito colateral curioso: **0,890 é mais perto do 0,90 do BC**, que
  era justamente o único dos quatro números que não encostava. Isso não é argumento para tirá-las;
  é coincidência de sinal contrário se lembrarmos que o BC estima as dele *com* tratamento de
  crise (`k08`/`k20` no modelo dele).
- **O resíduo continua ruído branco nas duas**, Ljung-Box limpo em Q(4) e Q(8). Ou seja **não há
  argumento de diagnóstico para manter as dummies** — o argumento é só ajuste, mais o fato de
  2009T2 virar um resíduo de 3,4 desvios sem elas.
- **O efeito de longo prazo fica menos preciso**, com o intervalo indo de 2,88 para 3,27 p.p. de
  largura. Já era o parâmetro mal identificado; sem as dummies fica pior.

A decisão é do usuário. O que a medição diz é que as dummies são baratas de manter e não sustentam
nada sozinhas: elas compram ajuste e um resíduo sem outlier grosseiro, não uma especificação
diferente.

### Três leituras, e uma delas corrige o que eu esperava

**A primeira é R8, e a resposta é dura.** Com priori difusa o efeito de longo prazo é
**2,61, com intervalo de 90% de [1,23; 4,12]** — quase 2,9 p.p. de largura, contra os 1,17 do
intervalo que o BC publica. O `taylor.py` já registrava que 2,62 *"encosta no teto do intervalo
(2,64)"* e que *"com margem própria ele certamente cruzaria a borda"*. Cruza, e com folga: a
probabilidade de o nosso efeito de longo prazo cair dentro do IC publicado é de **0,44**. Ou seja,
"os três parâmetros caem dentro dos intervalos do BC" continua verdadeiro ponto a ponto, mas o
terceiro deles **não tem precisão para sustentar a afirmação** — a frase vale para `t1` e `t2`, que
têm intervalo estreito, e não para o efeito de longo prazo, que é praticamente não identificado
nesta amostra.

**A segunda corrige uma expectativa minha.** Eu esperava que a razão `r2/(1−soma)` fosse fortemente
assimétrica — é uma razão com polo, e o método delta, que lineariza, não representaria a cauda.
Medido, **a assimetria é branda e o método delta teria servido**:

```
HDI 90% (propagado desenho a desenho): [1,224; 4,032]
método delta (simétrico, ±1,645·sd):   [1,209; 4,192]
```

O motivo é verificável: `soma = 0,864` com desvio de 0,030 fica a mais de quatro desvios de 1, então
o denominador nunca chega perto de zero (P(estável) = 1,000 nos 16.000 desenhos). O polo existe; só
não morde nesta amostra. **O ganho do MCMC aqui não é a assimetria** — é (a) haver intervalo, (b)
poder pôr a priori onde o BC a publica, e (c) o leque abaixo.

**A terceira é sobre a priori, e ela domina.** A coluna de encolhimento (desvio do posterior ÷
desvio da priori) mede quanto o dado moveu cada parâmetro:

```
           encolhimento com priori do BC    com desvio ×4
t1                 0,72                        0,41
t2                 0,79                        0,47
t3                 0,92                        0,52
```

**0,92 em `t3` quer dizer que os nossos 80 trimestres reduziram a incerteza sobre o efeito de longo
prazo em 8%.** O posterior `[1,59; 2,66]` é, para todos os efeitos, a priori do BC lida de volta.
Isso não é falha do amostrador: é o que acontece quando uma priori muito informativa encontra uma
amostra que informa pouco sobre aquele parâmetro — e é exatamente por isso que a variante difusa
tem de ser publicada ao lado, e não no lugar dela.

Vale notar o outro lado: com priori difusa o nosso intervalo de `t1` é `[1,30; 1,57]`, **mais largo**
que o `[1,41; 1,54]` publicado. O BC estima o sistema inteiro por filtro de Kalman com mais
informação do que uma equação única em 80 trimestres — não é de esperar que a gente seja mais
preciso do que ele.

### O leque, que é o motivo de isto interessar ao simulador

Resposta da Selic a um desvio **permanente** de +1 p.p. da inflação esperada em relação à meta.
Cada desenho do posterior é um vetor completo e coerente de parâmetros, então rodar a regra em todos
eles devolve uma **nuvem** de caminhos, não uma linha com faixa colada por fora:

```
trim.    MQ     faixa 90% com priori do BC   largura    faixa 90% só com nosso dado   largura
  1    +0,354   [+0,162; +0,382]              0,219     [+0,145; +0,526]               0,382
  2    +0,862   [+0,396; +0,926]              0,530     [+0,375; +1,270]               0,895
  4    +1,855   [+0,904; +1,974]              1,070     [+0,850; +2,694]               1,844
  8    +2,744   [+1,587; +2,840]              1,253     [+1,340; +4,013]               2,672
 12    +2,721   [+1,646; +2,771]              1,125     [+1,232; +4,083]               2,851
 20    +2,607   [+1,588; +2,660]              1,072     [+1,201; +4,065]               2,864
 lp    +2,616   [+1,589; +2,660]              1,071     [+1,232; +4,117]               2,885
```

Duas coisas que só aparecem porque a faixa é propagada pela dinâmica:

- **A incerteza não é constante ao longo do horizonte**, então uma faixa colada em volta do caminho
  do MQ estaria errada nos dois extremos. Com o dado sozinho ela cresce de 0,38 no primeiro
  trimestre para 2,88 no vigésimo — a mesma incerteza de `t1`/`t2` se acumula a cada trimestre.
- **Com a priori do BC ela cresce até o sexto trimestre e depois ENCOLHE** (1,28 → 1,07), porque a
  priori fixa o destino: o que fica incerto é o caminho, não onde ele termina. Ler a faixa da
  esquerda como "a incerteza do modelo" seria ler a convicção do BC.

---

## O que isto NÃO conserta

- **A simultaneidade continua lá.** `dI(t)` e `R(t)` são contemporâneos e a estimação segue sendo de
  equação única contra dado observado. Priori não é instrumento, e nenhuma variante daqui trata
  isso.
- **A escolha de `RR*`** continua sendo premissa que desloca os coeficientes (a regressão não tem
  intercepto para absorvê-la). A tabela de janelas do `taylor.py` continua sendo onde isso se mede.
- **Nada aqui fecha o laço entre equações.** Continua sendo equação por equação.

---

## Decisões que são do usuário, não minhas

1. **Qual variante é a da página**, se isto for para a tela. A recomendação é publicar a difusa como
   a estimativa e a de priori do BC ao lado, rotulada como o que é — não o contrário.
2. **Se as outras quatro equações seguem o mesmo caminho.** (E) e (H) têm o mesmo formato de efeito
   de longo prazo por razão, então ganham a mesma coisa; (F) é Ridge, e ali a tradução natural da
   penalidade é uma priori normal com o λ virando desvio — o que tornaria o `t_valem` do payload
   desnecessário em vez de condicional.
3. **Se a estimação conjunta entra em cena.** O MCMC é o caminho para isso: o que hoje são cinco
   regressões separadas cabe num modelo só, com a covariância dos resíduos estimada junto. É outro
   projeto, e o argumento contra continua valendo — num sistema conjunto um erro de especificação
   contamina todos os coeficientes pela matriz de covariância, sem dizer qual equação o causou.
4. **O que o simulador mostrou e a estimação não mostrava.** Rodando **solta** desde 2006T3 — só as
   duas primeiras defasagens vindas do dado —, a regra erra **1,69 p.p. em média** contra a Selic
   observada, com RMSE de **1,97**, contra os 0,566 do ajuste de um passo à frente. Não é
   contradição: são duas perguntas diferentes, e é a segunda que o simulador existe para fazer.
   Vinte anos sem reancoragem é um teste extremo, e a aba deixa escolher janelas curtas.
