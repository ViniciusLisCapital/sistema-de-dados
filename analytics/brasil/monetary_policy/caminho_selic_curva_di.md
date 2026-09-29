# Da curva DI à Selic reunião a reunião

Como a aba **Expectativas de Juros** do relatório de Política Monetária transforma a curva DI × pré
da B3 no caminho da meta Selic que o mercado precifica depois de cada reunião do Copom — o número
que se compara, reunião por reunião, com a mediana da pesquisa Focus.

Método e números de 2026-09-25. Código: `expectativas_juros.py` (`caminho_di()`, `SUAVIZACAO`),
`condicionais.py` (`data_da_posicao()`), `domain/db/brasil/bcb/pm_copom_calendario.py` (datas
oficiais) e `domain/db/brasil/b3/br_di_grade.py` (a curva). Conferência:
`tests/test_expectativas_juros.py`.

---

## 1. O que a curva informa

Cada contrato futuro de DI1 vence no **primeiro dia útil de um mês** e paga o CDI acumulado de hoje
até lá. A taxa dele é, portanto, a **média composta dos overnights** até o vencimento — não a
Selic daquele mês. A Selic de uma reunião específica tem de ser tirada da diferença entre
vencimentos.

A fonte é a curva de referência DI × pré que a B3 publica no arquivo de pregão (`TaxaSwap.txt`,
código `PRE`), guardada inteira em `macro_brasil.br_di_grade`: todos os vértices, ~280 por pregão,
flat-forward entre vencimentos de DI1. **É o mesmo insumo da Bloomberg**: no pregão de 22/09/2026 os
17 vencimentos da tela de CDI implícito dela (coluna *Last*) batem com a curva da B3 a 0,001 p.p.,
exceto set/27 (0,5 p.b.).

## 2. Convenções

| | regra |
|---|---|
| Contagem | dias úteis, base 252, capitalização composta — a do contrato |
| Calendário | o de feriados **vigente no pregão**: o 20 de novembro só é feriado nacional desde 21/12/2023 (Lei 14.759). Com essa regra o `du` calculado reproduz o publicado pela B3 em todos os 9.531 vértices conferidos |
| Quando a Selic muda | no overnight do **dia útil seguinte** à decisão — é a data que a Bloomberg chama de *COPOM Eff* |
| CDI → meta | a curva é de CDI, que negocia abaixo da meta. Soma-se a diferença **do próprio pregão**: meta vigente menos o CDI do primeiro overnight (0,10 p.p. hoje; entre −0,04 e 0,67 desde 2006) |
| Horizonte | 24 meses de vencimentos; reunião depois do último vencimento não recebe número |

## 3. A conta

Em taxa anual em log, `y = ln(1 + r)`, a taxa de um vencimento é uma **média simples** dos
overnights, e a conta fica linear. Com `y₀` o overnight de hoje, `y_k` o CDI depois da reunião `k`
e `n_k(T)` o número de overnights até o vencimento `T` em que vigora o degrau `k`:

```
média_T(y) = ( n₀(T)·y₀ + Σ_k n_k(T)·y_k ) / T
```

O caminho é o `y` que minimiza

```
Σ_T ( média_T(y) − taxa_T )²   +   λ · Σ_k ( y_k − y_(k−1) )²
```

O primeiro termo pede que o caminho reproduza as taxas dos contratos. O segundo cobra por cada
mudança de uma reunião para a seguinte — inclusive a passagem do CDI de hoje para o da primeira
reunião. **λ = 0,1** (`SUAVIZACAO`): um degrau de 1 p.b. custa o mesmo que errar em ~0,3 p.b. a
taxa de um contrato.

## 4. Por que o termo de suavização existe

Sem ele (λ = 0) a conta devolve a escada que **melhor** reproduz os contratos — exata numa curva
sintética, e é assim que o teste confere a convenção de datas. Na curva de verdade, essa escada
repete o ruído dos contratos **amplificado**. A taxa de um contrato a um ano e meio é a média de
~270 dias úteis; um ponto-base a mais nela tem de ser carregado pelos ~20 dias do último mês, e o
forward daquele mês anda ~13 p.b. Numa curva sintética de Selic parada, 1 p.b. a mais num único
contrato a sete meses vira um degrau de **7,0 p.b.** sem suavização e de **0,5 p.b.** com ela.

O resultado era um caminho em zigue-zague, e a comparação com a Bloomberg mostrou de onde ele vinha
(pregão de 22/09/2026, CDI depois de cada reunião, % a.a.):

| reunião | Bloomberg | com suavização | sem suavização |
|---|---|---|---|
| 04/11/2026 | 13,477 | 13,484 | 13,457 |
| 09/12/2026 | 13,429 | 13,431 | 13,415 |
| 27/01/2027 | 13,446 | 13,449 | 13,494 |
| 17/03/2027 | 13,468 | 13,464 | 13,451 |
| 28/04/2027 | 13,478 | 13,472 | 13,494 |
| 16/06/2027 | 13,480 | 13,475 | 13,481 |
| 04/08/2027 | 13,484 | 13,480 | 13,520 |
| 22/09/2027 | 13,505 | 13,499 | 13,436 |
| 27/10/2027 | 13,550 | 13,538 | 13,375 |
| 08/12/2027 | 13,619 | 13,602 | 13,617 |
| diferença média / máxima | | **0,7 / 1,7 p.b.** | 4,0 / 17,5 p.b. |

As duas colunas da direita usam a mesma curva e as mesmas datas; só o termo de suavização muda.
Somar 0,10 p.p. dá a meta Selic que o gráfico mostra.

**O que se sabe do método da Bloomberg é o que se mede, não o que ela publica.** A coluna *Est* da
tela é a taxa que o caminho dela implica para cada contrato — refeita daqui a partir do caminho, a
menos de 0,5 p.b. —, e ela erra a taxa negociada (*Last*) em até 2,1 p.b. em 22/09 e 2,4 p.b. em
24/09 (0,9 e 1,1 p.b. de erro quadrático médio). Ou seja: **a Bloomberg aceita errar os contratos
em ~1 p.b. em troca de um caminho liso**. As duas escadas explicam os preços negociados dentro do
ruído deles, e a curva sozinha não decide entre elas; o critério de estabilidade é uma escolha, e é
a da Bloomberg.

## 5. Como λ foi escolhido

Contra as duas telas da Bloomberg (22 e 24/09/2026), com os contratos e as datas dela: cinco formas
de custo (diferença primeira, sem a primeira reunião, ponderada pelo horizonte, pelo quadrado dele,
e diferença segunda) × onze pesos, de 0,0001 a 10. A diferença primeira com λ = 0,1 foi a mais perto
nos dois dias. Os pesos vizinhos ficam piores dos dois lados: 0,03 alisa pouco e 0,3 começa a errar
os contratos mais do que a própria Bloomberg erra.

O que fica medido e cobrado no teste:

- **24/09/2026, contratos e datas da Bloomberg**: as 10 reuniões até dez/2027 a menos de 2,1 p.b. do
  caminho dela (19,3 p.b. sem suavização).
- **22/09/2026, curva da B3 e datas do sistema** (o que a aba usa): a menos de 1,7 p.b. As duas
  primeiras de 2028, cujas datas diferem (ver §7), a 1,8 e 2,0 p.b.
- Em 24/09 a curva da B3 (ajuste do fim do dia) difere da tela (negócio intradiário) em até 2 p.b.
  num contrato, e o caminho da aba fica a até 4,3 p.b. do da Bloomberg — diferença de preço, não de
  método.

## 6. O que a suavização custa

Nas 1.082 curvas semanais desde 2006:

| | sem suavização | com suavização |
|---|---|---|
| zigue-zague: variação média da mudança de uma reunião para a seguinte, 10 primeiras reuniões | 29,3 p.b. | **6,3 p.b.** |
| erro nas taxas dos contratos (quadrático médio): mediana / p95 / pior | 0,5 / 1,3 / 3,0 p.b. | 1,3 / 2,3 / 8,0 p.b. |
| no pregão do dia de cada decisão (165), distância entre o preço da reunião e a decisão: mediana / pior | 3,0 / 45,5 p.b. | 3,5 / 46,3 p.b. |

E três limites, todos consequência de preferir o caminho estável:

- **Pausa e ritmo constante não se distinguem a um ano.** Numa curva sintética com pausas no meio
  de um ciclo de cortes, o caminho suavizado reproduz os contratos a 1,2 p.b. e ainda assim erra
  reuniões isoladas em até 9 p.b. — mostra um ritmo constante onde havia pausa. Um ciclo de ritmo
  constante volta a menos de 3 p.b. Ler o nível e a inclinação, não o passo de uma reunião lá na
  frente.
- **Movimento grande e rápido muda um pouco.** Nas 327 semanas em que a primeira reunião
  precificava 50 p.b. ou mais, a suavização mudou esse passo de −12 a +15 p.b. (+0,7 em média). As
  semanas em que o caminho mais erra os contratos são as de choque: 12/11/2021 (8,0 p.b.),
  set/2020, out/2008.
- **Depois de ~16 meses os vencimentos são trimestrais** (jan, abr, jul, out). A curva só dá uma
  taxa por trimestre, e o que aparece entre duas reuniões do mesmo trimestre é a passagem mais suave
  de um trimestre para o outro.

E um limite que não é da conta: **nada aqui separa expectativa de prêmio de prazo**. O caminho é o
que o preço implica, e o preço carrega os dois.

## 7. As datas das reuniões

A data decide em que mês cada degrau entra, então ela importa para a curva — e é a mesma lista para
a pesquisa, para a reunião `j` de uma ser sempre a reunião `j` da outra.

**Oficiais, quando o BC já marcou.** O Copom publica o calendário do ano seguinte com meses de
antecedência na agenda do BCB (feed "Reuniões do Copom"). O calendário anual do sistema
(`calendar_2026.yaml`) não recebe datas de outro ano, então o feed tem tabela própria,
`pm_copom_calendario`, atualizada todo dia. Em 2026-09-25 ela trazia as 73 reuniões de dez/2018 a
dez/2027, e **as oito de 2027 são exatamente as da Bloomberg**: 27/01, 17/03, 28/04, 16/06, 04/08,
22/09, 27/10 e 08/12.

**Estimadas, quando ainda não marcou.** A mesma reunião do último ano conhecido, 52 semanas depois
por ano de distância — o que a mantém numa quarta-feira, o dia de toda decisão desde 2006. Medido de
2012 a 2027, estimando cada ano só com os anteriores (128 reuniões):

| regra | erro médio | erro mediano | até 3 dias | mês errado |
|---|---|---|---|---|
| mesma reunião do ano anterior + 52 semanas | **4,0 dias** | **0** | 60% | 25 |
| dia do ano típico da posição (mediana de 10 anos), a regra anterior | 7,0 dias | 6 | 32% | 37 |

A regra anterior também caía em sábado e domingo. Para 2028 ela dá 26/01, 15/03, 26/04, 14/06,
02/08, 20/09, 25/10 e 06/12. **A Bloomberg também estima 2028, e estima outra coisa**: 19/01, 01/03
e 19/04 para as três primeiras. Nenhuma das duas é oficial; no pregão de 22/09 a diferença de data
move o caminho dessas reuniões em ~2 p.b., porque elas já caem na parte trimestral da curva. Quando
o BC publicar 2028, as datas passam a ser as dele sem ninguém mexer.

## 8. Onde cada coisa é conferida

`tests/test_expectativas_juros.py`, sem nada disso ir para a tela:

1. o calendário de dias úteis da época do pregão;
2. sem suavização, a escada sintética volta exata — e uma escada deslocada de um dia não volta, que
   é o que prova a convenção de datas; com suavização, 1 p.b. num contrato não vira degrau, um
   ciclo constante volta a menos de 3 p.b. e os contratos continuam reproduzidos;
3. o `du` publicado pela B3;
4. no dia de cada decisão desde 2006, o preço da própria reunião a menos de 50 p.b. do decidido;
5. o caminho da Bloomberg de 24/09/2026, a partir dos contratos e das datas dela;
6. as datas oficiais de 2027, as estimadas numa quarta, e o caminho da aba contra a Bloomberg em
   22/09/2026.

Quatro mutantes conferidos contra essa lista, todos pegos: sem suavização, suavização três vezes
maior, estimar datas com 365 dias em vez de 52 semanas, e o calendário oficial fora da conta.
