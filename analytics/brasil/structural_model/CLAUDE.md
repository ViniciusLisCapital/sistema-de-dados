# analytics/brasil/structural_model/ — Contexto para o Claude

**Estado: a curva de Phillips (I), a equação de expectativas (E) e a curva IS (H) estão estimadas;
as outras duas — juros e câmbio — não.** Este arquivo ainda é, em parte, o
*plano* aprovado em 2026-09-16, e vai sendo substituído pelo estado real à medida que cada equação
fica pronta. Histórico rodada-a-rodada vive no git log, não aqui.

## Como rodar

```powershell
uv run python analytics/brasil/structural_model/panel.py                      # painel -> data/panel.csv
uv run python -m analytics.brasil.structural_model.equations.phillips_sub     # as quatro equações
uv run python -m analytics.brasil.structural_model.equations.expectations     # a equação (E)
uv run python -m analytics.brasil.structural_model.equations.is_curve         # a equação (H)
uv run python -c "from analytics.brasil.structural_model.generate_report import run; run()"
node tests/test_structural_model_js.js                                        # 1.057 asserções
```

| Módulo | O que faz |
|---|---|
| `panel.py` | Painel trimestral dos insumos. `construir()` monta do banco, `salvar()` grava `data/panel.csv`. Importa `q`/`serie`/`para_q`/`focus_ipca_12m` de `monetary_policy/modelo_painel.py` — não copia. `ipca_12m_publicado()` é **gabarito** da leitura de 12 meses e o termo de inflação de (E); `metas()` monta a meta do horizonte de 12 meses e devolve o último ano que o CMN de fato publicou; `ntnb_real()` lê a curva real da B3 nos vértices de 2 e 10 anos, de onde sai o aperto de (H) |
| `equations/phillips_sub.py` | As quatro equações. `estimar()` roda na amostra comum e reconstrói o cheio; `comparar_ia()` e `comparar_im()` são os dois testes de forma registrados na tela; `sem_sazonais()` é o contrafactual das dummies de trimestre; `leitura_12m()` encadeia o ajuste trimestral de quatro em quatro — **tradução de unidade, não previsão** |
| `equations/expectations.py` | A equação (E), **na especificação do plano e nada além dela**. `estimar()` impõe a soma-um por reparametrização e devolve a meia-vida e o repasse; `repouso()` confere **numericamente** que a conta devolve a meta e que o repasse simulado bate com a fórmula |
| `equations/is_curve.py` | A equação (H), a curva IS. O aperto monetário é a **inclinação da curva de juro real** (2 anos menos 10), não um juro contra um neutro — `comparar_rr()` é o registro medido do porquê, e `comparar()` traz as outras formas testadas. `repouso()` confere **numericamente** que o hiato volta a zero sem intercepto e que o efeito de longo prazo bate com a fórmula |
| `generate_report.py` | Chama `panel.construir()`, `phillips_sub.estimar()`, `expectations.estimar()` e `is_curve.estimar()` **ao vivo** (≈9s) e injeta em `report.html`. Sem artefato intermediário e sem passo de recálculo declarado. Importa as modas publicadas da eq. (2) do BC de `monetary_policy.modelo_agregado` em vez de redigitá-las |

**`equations/phillips.py` não existe mais** (removido em 2026-09-17, a pedido do usuário): a equação
agregada sobre o IPCA cheio e a métrica de 12 meses saíram do modelo. O índice cheio sobrevive em
dois papéis que **não são** "rodar o modelo nele": alvo da reconstrução, e âncora da indexação em
(IM).

## A métrica: inflação do trimestre, e por que ela substituiu o acumulado de 12 meses

Medido na troca, mesma especificação agregada e mesma amostra:

| | 12 meses | trimestral |
|---|---|---|
| inércia `i1` | 0,7282 (t 5,17) | **0,3222** (t 2,70) |
| peso da expectativa | 0,272 | **0,678** |
| Ljung-Box Q(4) do resíduo | p **0,0008** — rejeita | p 0,123 |
| repasse cambial de longo prazo | 0,128 | **0,190** |

**Mais da metade da "inércia" era a sobreposição das janelas.** Um acumulado de doze meses lido a
cada três faz trimestres vizinhos compartilharem nove meses de dado; o resíduo é MA(3) por
construção e a inércia sai mecanicamente alta. Com janelas que não se sobrepõem, o `i1` cai para
dentro do intervalo de credibilidade de 90% que o BC publica para o `a1L` ([0,02; 0,38]) — comparação
que na métrica anterior não fazia sentido nenhum. E a métrica de 12 meses estava **subestimando o
repasse cambial em quase metade**.

### E a unidade é a NATIVA do trimestre, não anualizada

Anualizar é `(1+π)⁴`, que não comuta com média ponderada. Medido, a identidade do IPCA fecha com:

| reconstrução do cheio | RMSE | erro médio |
|---|---|---|
| **trimestral nativa** | **0,0253** | 0,0167 |
| trimestral anualizada | 0,2326 | 0,1467 |
| 12 meses | 0,0785 | — |

Como a tese da página é que a soma ponderada dos quatro reproduz o cheio, a unidade nativa é a única
que não estraga o que se quer mostrar. Estatisticamente as duas empatam (os `t` mal se movem); é a
identidade que decide.

A expectativa é anual e entra **dividida por 4**, como na eq. (1) do modelo agregado do BC. Hiato,
câmbio e IC-Br já são trimestrais e não mudam.

## As dummies de trimestre, e por que soma-zero

A inflação trimestral é sazonal: o padrão explica 20% da variância do cheio e **32% da de serviços**,
com amplitude de 3,9 p.p. anualizados no cheio e 10,3 em alimentação. Deixar isso no resíduo joga um
padrão autocorrelacionado direto no coeficiente de inércia.

A codificação é `1{Q=q} − 1{Q=4}`, três colunas, e o quarto efeito é `−(s1+s2+s3)`. **Soma-zero não é
convenção, é consequência**: escrevendo `I(t) = Ĩ(t) + σ_q`, o termo sazonal que sobra na equação é
`s_q = σ_q − i1·σ_{q−1}`, e como σ soma zero no ano, s também soma. Com indicadoras comuns o estado
estacionário viraria `E/4 + s_Q`, diferente em cada trimestre e igual à expectativa em nenhum.

Corolário que a página diz: os coeficientes estimados **não são** a sazonalidade da inflação — são o
padrão líquido do que a inércia já propaga.

**Por que dummy e não X-13:** cinco filtros independentes quebram a aditividade. Medido, a soma
ponderada dos quatro reproduz o cheio com RMSE 0,0253 no espaço cru e **0,0859 no dessazonalizado por
X-13** — 3,4× pior, contra um piso de 0,0253. E os dois descrevem o mesmo padrão médio (correlação
0,996 a 1,000; 0,917 em monitorados), então trocar não custa descrição.

## A média móvel de 4 trimestres em (IS) e (II)

Não foi copiada do BC, foi medida. (IS) era a única equação cujo resíduo rejeitava Ljung-Box
(Q(4) = 19,1, p 0,0007) com o pico na defasagem 4. Acrescentando a MM4 da própria inflação dentro da
restrição, o teste deixa de rejeitar (p 0,34) e a **defasagem de um trimestre colapsa para 0,027
(t 0,23)** enquanto a MM4 fica com 0,688 (t 4,73): a inércia de serviços não é o trimestre passado,
é a média do último ano. O hiato, que era t 3,47, vai a 4,88.

| | MM4 | t | defasagem de 1 tri | t | Ljung-Box p, antes → depois |
|---|---|---|---|---|---|
| IS | **0,688** | 4,73 | 0,027 | 0,23 | 0,0007 → **0,341** |
| II | 0,266 | 2,11 | 0,542 | 4,40 | 0,084 → 0,202 |
| IA | 0,135 | 0,83 | — | — | não entra |
| IM | −0,215 | −1,03 | — | — | não entra |

Bate com o BC, que põe média móvel só na equação de serviços.

## Os números, em 2026-09-17 (2003T4→2026T2, 91 trimestres)

```
(IS) IS = is1·IS(-1) + is1b·MM4(IS) + (1-is1-is1b)·E(-1)/4 + is2·H                       + saz
(IA) IA = ia1·IA(-1) +                (1-ia1)·E(-1)/4      + ia2·IAGR + ia3·F   + ia4·H   + saz
(II) II = ii1·II(-1) + ii1b·MM4(II) + (1-ii1-ii1b)·E(-1)/4 + ii2·IMET + ii3·IMET(-1)
                                                           + ii4·F(-1)         + ii5·H   + saz
(IM) IM = im1·IM(-1) + im2·I(-1)    + (1-im1-im2)·E(-1)/4                                 + saz
```

| | inércia | MM4 | peso da expectativa | choques | R² | RMSE | LB p |
|---|---|---|---|---|---|---|---|
| **IS** serviços | 0,027 (t 0,23) | **0,688 (t 4,73)** | 0,285 | hiato **0,0927 (t 4,88)** | 0,626 | 0,442 | 0,341 |
| **IA** alimentação | 0,245 (t 2,72) | — | 0,755 | agro **0,1234 (t 3,20)** · câmbio **0,0871 (t 2,79)** · hiato −0,0016 (t −0,01) | 0,294 | 1,927 | 0,211 |
| **II** industriais | 0,543 (t 4,40) | 0,266 (t 2,11) | 0,192 | metal 0,0178 (t 2,37) · metal(−1) 0,0209 (t 2,43) · **câmbio(−1) 0,0406 (t 3,37)** · hiato 0,0465 (t 1,28) | 0,524 | 0,614 | 0,202 |
| **IM** monitorados | 0,312 (t 2,41) | — | 0,914 | indexação ao cheio **−0,2253 (t −0,40)** | 0,070 | 1,655 | 0,471 |

`t` é HAC(4) — aqui margem conservadora, não correção de artefato: **nenhuma das quatro rejeita
Ljung-Box**, o que é exatamente o que a troca de métrica comprou.

Reconstrução do cheio: **RMSE 0,6159, R² 0,4046, piso 0,0253** — somar quase não custa, o que se
perde está nas equações.

Ajustes de trimestre (p.p. do trimestre, líquidos) e o que valem:

| | Q1 | Q2 | Q3 | Q4 | R² sem → com | RMSE sem → com |
|---|---|---|---|---|---|---|
| IS | 0,613 | −0,418 | −0,296 | 0,100 | 0,321 → **0,626** | 0,595 → 0,442 |
| IA | 0,508 | −0,084 | −1,465 | 1,040 | 0,140 → 0,294 | 2,126 → 1,927 |
| II | −0,190 | −0,043 | −0,265 | 0,499 | 0,425 → 0,524 | 0,674 → 0,614 |
| IM | 0,422 | −0,030 | −0,240 | −0,151 | 0,050 → 0,070 | 1,672 → 1,655 |

Em serviços elas **dobram o R²**.

## A leitura de 12 meses é TRADUÇÃO, não previsão

Pedido do usuário em 2026-09-17, em duas rodadas. A primeira entrega foi uma previsão dinâmica de
quatro trimestres (cada origem iterando a equação com a própria saída como defasagem e média móvel),
e **foi corrigida no mesmo dia**: *"o que eu quero saber é o que as variações trimestrais significam
em termos anuais. não é para prever nada. Pegue os números trimestrais + sazonalidade e crie o que
seria o 12m."*

Então a vista de 12 meses é o **mesmo ajuste** da vista trimestral, encadeado de quatro em quatro:
`(1+m1)(1+m2)(1+m3)(1+m4) − 1`. Nada é simulado, nada realimenta, as defasagens e a média móvel
seguem sendo as realizadas — é uma troca de unidade, não um exercício diferente. O código é
`leitura_12m()`, e a iteração dinâmica foi **removida** em vez de ficar como segunda opção: caminho
que ninguém usa é dívida.

**Por que isso é o que responde à pergunta.** Um coeficiente de 0,0927 sobre o hiato não diz nada a
quem pensa em 4,5% ao ano. E o encadeamento é onde a sazonalidade se resolve sozinha: como as quatro
dummies somam zero e **toda janela de quatro trimestres cobre um de cada trimestre do ano**, o ajuste
de calendário sai da leitura anual sem precisar ser desligado. Medido, refazendo a leitura com o
sazonal retirado de cada trimestre:

| | move dentro do trimestre | sobra em 12 meses |
|---|---|---|
| IS serviços | 1,03 p.p. | 0,008 |
| IA alimentação | **2,51 p.p.** | 0,060 |
| II industriais | 0,76 p.p. | 0,006 |
| IM monitorados | 0,66 p.p. | 0,007 |

O resíduo é o cruzado da composição, de segunda ordem. Ou seja: **a leitura de 12 meses já é
comparável a uma série dessazonalizada, e sem nenhum filtro rodando** — as três asserções (janela
cobre os quatro trimestres, amplitude > 0,5 p.p., sobra < 0,1 p.p. e < 1/5 da amplitude) são o que
mantém isso verdadeiro.

88 janelas, 2004T3→2026T2:

| | RMSE | erro médio | viés |
|---|---|---|---|
| **cheio** | **1,378** | 0,929 | −0,255 |
| IS serviços | 0,998 | 0,702 | −0,438 |
| IA alimentação | 4,069 | 3,207 | −0,630 |
| II industriais | 1,328 | 1,078 | +0,585 |
| IM monitorados | 3,536 | 2,426 | −0,877 |

**O erro maior não é o modelo piorando** — é a mesma conta numa unidade maior, com os quatro erros
trimestrais se somando dentro da janela. Se eles fossem independentes daria 0,616 × 2 = 1,23; sai
1,378, ou **2,24×** o trimestral contra o 2,0× independente: os erros trimestrais andam um pouco
juntos, e o cartão da página imprime justamente essa razão. O teto de 4× (erros perfeitamente
correlacionados) também é afirmado, pelo outro lado.

Para registro, a previsão iterada que foi removida dava cheio RMSE 1,800 / erro 1,209 / viés −0,262
em 84 janelas — pior, como tem de ser, e respondendo outra pergunta.

### O gabarito do encadeamento

Encadear quatro trimestres da nossa `pi_q` reproduz o **IPCA de 12 meses publicado** com erro médio
de **0,0025 p.p.** (máx 0,0052). Somar os quatro em vez de encadear erra **0,1491** (máx 0,8614) —
sessenta vezes mais. É a única conferência da página contra um número que não saiu daqui, e é o que
pega qualquer troca de encadeamento por soma.

## Os dois defeitos declarados na página

**A âncora é o IPCA cheio nas quatro.** `expc_focus` publica expectativa por subíndice, mas só desde
set/2021 — 20 trimestres contra 91. Isso impõe preços relativos constantes no longo prazo, o que a
história nega. O BC resolve com um passeio aleatório não observado por setor (`A_t`), que não está
aqui.

**(IM) continua mal especificada, e o horizonte não é a causa.** Testadas as três âncoras possíveis,
com as unidades certas (o acumulado de 12 meses tem de ser dividido por 4 para entrar numa equação
trimestral):

| âncora | im2 | t | peso da expectativa |
|---|---|---|---|
| IPCA do trimestre (t−1) — **a em uso** | −0,225 | −0,40 | 0,914 |
| IPCA 12 meses ÷ 4 (t−1) | −0,565 | −1,09 | **1,274** |
| média móvel de 4 tri (t−1) | −0,631 | −1,13 | **1,338** |

Todas negativas, nenhuma significativa, e as duas de horizonte longo jogam o peso da expectativa
acima de 1 — que não tem leitura. A causa é mecânica: o cheio contém os próprios monitorados com
peso ~0,26. O conserto é indexar à parte livre, e está pendente.

## O sazonal de serviços está andando

Medido: o ajuste de Q1 em serviços cai **0,042 p.p. por ano** (t −3,02, com a MM4 dentro; −0,058 e
t −3,64 sem ela) — ~1 p.p. ao longo da amostra. Q2 e Q3 não se mexem. Serviços também é o único corte
que rejeita Chow no vetor sazonal com quebra em 2015T1 (F 3,71, p 0,0147).

**Deliberadamente não corrigido com tendência linear.** Ela melhora o R² (0,626 → 0,695) mas é
muleta: o lugar certo é um sazonal estocástico no espaço de estados, junto com os `A_t`. Fica medido
e declarado em vez de remendado — e é o argumento empírico para o passo de parâmetros variando no
tempo.

## Duas coisas que foram medidas e NÃO fazem diferença

- **Peso do trimestre: média dos três meses contra o último mês.** RMSE 0,0318 nos dois, igual à
  quarta casa. Na métrica de 12 meses a escolha importava (0,065 contra 0,106); em três meses o peso
  não anda o bastante. Fica a média, que é a conceitualmente certa, mas **não há assertiva a escrever
  sobre isso** — um mutante que troque as duas não muda número nenhum.
- **MA(1) no resíduo de alimentação.** Na métrica de 12 meses o veredito vinha da janela; aqui vem do
  diagnóstico direto: **Ljung-Box não rejeita** (p 0,211), então não há autocorrelação a modelar. O
  θ que a máxima verossimilhança acha (−0,641) é incompatível com a ACF do resíduo de MQ (−0,082) —
  é o ajuste conjunto realocando, não um erro MA. E o RMSE piora, de 1,927 para 2,152.

## A equação (E): de onde vem a expectativa (2026-09-21)

```
(E) E(t) = e1·E(t-1) + e2·I12(t) + (1-e1-e2)·Meta(t) + ε

    E     expectativa Focus de IPCA 12m à frente, suavizada, % ao ano
    I12   IPCA acumulado em 12 meses publicado (SGS 13522), % ao ano
    Meta  meta do CMN no horizonte de 12 meses, % ao ano
```

**É a especificação do plano desta pasta, sem acréscimo nenhum**, e isso é uma decisão e não um
resíduo: a equação foi construída primeiro com uma forma mais rica (segunda defasagem, o trimestre
anualizado no lugar dos doze meses, o câmbio e ajustes de trimestre) sem que a mudança de
especificação tivesse sido pedida, e foi desfeita no mesmo dia. **As medições não se perderam** —
estão em [`pendencias_expectativas_eq.md`](pendencias_expectativas_eq.md), com o número de cada
coisa, e a decisão de incorporar vem depois de todas as equações estarem de pé.

Tudo em **taxa anual**, ao contrário da curva de Phillips. O que a equação explica é uma expectativa
de doze meses e o alvo dela é a meta, que também é anual — por isso `pi_e` entra inteiro aqui e
dividido por quatro lá.

98 trimestres, 2002T1→2026T2:

| parâmetro | peso | margem | t (HAC 4) | t (MQ) |
|---|---|---|---|---|
| expectativa do trimestre anterior | 0,5860 | ± 0,1573 | 3,72 | 7,51 |
| IPCA acumulado em 12 meses | 0,1603 | ± 0,0746 | 2,15 | 4,96 |
| **peso da meta** (conta de sobra) | **0,2537** | — | — | — |

R² 0,778 · RMSE 0,569 · meia-vida de um desvio **2 trimestres** · repasse de longo prazo **0,387** ·
**Ljung-Box Q(4) 32,1 (p 0,000002) e Q(8) 37,8 (p 0,000008)**.

**A ancoragem é imposta, não estimada** — com os três pesos somando um, a conta devolve a meta em
repouso quaisquer que sejam os coeficientes, e `repouso()` afirma isso numericamente em quatro
níveis de meta. O que se mede são as duas leituras derivadas: a meia-vida, e quanto de uma inflação
permanentemente 1 p.p. acima da meta a expectativa incorpora no fim (0,387 — nem âncora perfeita,
que seria 0, nem expectativa puramente adaptativa, que seria 1).

### O resíduo rejeita o teste de padrão, e a página diz isso

Os dois Ljung-Box rejeitam com folga, e a autocorrelação do erro é 0,393 em um trimestre. **Isso
está declarado em quatro lugares da aba** — a ficha de abertura, o cartão de erro típico, a tabela
de erro e a nota ao lado dela — e há asserção exigindo que os quatro digam a mesma coisa que o teste
mede, nos dois sentidos: se um dia o resíduo ficar limpo, a prosa que promete o contrário reprova.

Duas coisas seguem valendo e uma muda. Os pesos continuam sendo a melhor leitura desta forma, e a
margem deles já é a conservadora (HAC 4), que existe para aguentar erro correlacionado. O que muda é
a leitura do **erro típico**: 0,569 p.p. é o piso do que uma forma mais rica pode melhorar, não o
acaso irredutível. E **parte do padrão é do objeto, não da conta** — o regressando é uma expectativa
de doze meses lida a cada três e o regressor é um acumulado de doze meses amostrado a cada três, e
trimestres vizinhos falam do mesmo período em nove dos doze meses.

### Contra a eq. (5) do BC, e onde a comparação NÃO vale

```
(5) pi^e = f1·pi^e(-1) + f2·E_t[pi(t,t+4)] + f3·MA4(pi^IPCA) + (1-f1-f2-f3)·meta
```

Modas publicadas: f1 0,75 · f2 0,11 · f3 0,021 · meta 0,119 (réplica em `monetary_policy/`). As duas
diferenças que a aba declara são as que o plano previa:

- **Não há o termo de MA(4) de IPCA passado** (`f3`), que no BC já é desprezível: 0,021 com IC
  [0; 0,049]. A linha aparece na tabela **sem número nosso**, em vez de sumir.
- **`f2` não é `e2`.** Lá é a previsão do próprio modelo quatro trimestres à frente, que exige rodar
  o filtro a cada trimestre; aqui é a inflação realizada, que olha para trás. A tabela marca a linha
  como não comparável e a nota diz por quê. Foi essa troca que eliminou a simultaneidade que no BC
  custou um estimador em dois passos (condicionar em π^e observado em t leva f2 de 0,21 para 0,42).
- **O peso da meta é comparável**: 0,119 lá, **0,254** aqui.

### A meta é a do HORIZONTE, e a amostra é a mais longa

`meta_12m` mistura a meta do ano e a do seguinte na mesma proporção que a Focus de 12 meses usa
(`panel.META_W_Q` = 2/12, 5/12, 8/12, 11/12). Sem isso, um degrau de janeiro entra no desvio que a
equação explica — em 2003T4, com a meta indo de 4,0% para 5,5%, ele vale 1,5 p.p. O guarda de teste
é direto no dado: nos anos de transição, os quatro trimestres têm metas **diferentes**, o que zerar
a mistura destruiria.

A amostra começa em **2002T1**, antes da curva de Phillips, porque (E) não usa hiato. Não é folga: é
ali que a Focus de 12 meses chega a 9,6% na eleição de 2002, o único episódio de desancoragem
franca, e o maior resíduo da equação (+3,63 p.p. em 2002T4) está exatamente lá.

## A equação (H): de onde vem o aquecimento da economia (2026-09-21)

```
(H) H(t) = h1·H(t-1) + h2·g_rr(t-1) + d08 + d20 + ε

    H     hiato do produto do BCB, % do produto potencial
    g_rr  inclinação real 2a−10a (NTN-B), p.p. — o aperto monetário
```

81 trimestres, 2006T2→2026T2:

| parâmetro | peso | margem | t (HAC 4) | t (MQ) |
|---|---|---|---|---|
| hiato do trimestre anterior | 0,8864 | ± 0,0738 | 12,01 | 17,95 |
| aperto do trimestre anterior | **−0,1639** | ± 0,0626 | **−2,62** | −2,10 |
| crise de 2008-2009 | −0,4376 | ± 0,4091 | −1,07 | −1,47 |
| pandemia de 2020 | −1,1447 | ± 0,7727 | −1,48 | −2,89 |

R² 0,868 · RMSE 0,642 · meia-vida de um hiato **6 trimestres** · efeito de longo prazo **−1,443** ·
Ljung-Box Q(4) p 0,021 (rejeita) e Q(8) p 0,097 (não rejeita). Sinal `h2 < 0` como o plano previa,
e `h1` dentro do IC 90% que o BC publica para `b1` ([0,70; 0,95]).

### O aperto é uma INCLINAÇÃO, e essa é a decisão que define a equação

O plano pedia `g_RR(t) = i^e − π^e − RR*(t)`, com `RR*` por HP com cauda Focus. **Medido, a forma
com taxa de equilíbrio não sobrevive a nenhuma escolha que seja constante ou quase** — na mesma
janela de 81 trimestres:

| RR\* | h2 | t |
|---|---|---|
| constante 4,5% | −0,052 | −1,44 |
| a neutra declarada no RPM (5,0% hoje) | −0,055 | −1,45 |
| HP com cauda Focus | **−0,231** | **−4,42** |
| **a inclinação 2a−10a** (a escolhida) | −0,164 | −2,62 |

A causa é medida e não é sobre nível: **o juro real ex-ante cai de 12,2% em 2001T4 a −0,9% em
2020T4 e volta a 8,5%, e o hiato não tem essa tendência.** O que decide a estimativa é o que
*remove* a tendência, não o nível escolhido — por isso as duas candidatas fixas entregam um peso
três vezes menor e indistinguível de zero.

**O HP ajusta melhor e mesmo assim não foi escolhido, e isso está na tabela da aba em vez de
escondido.** Duas razões que a tabela não mostra: ele é filtro de dois lados, então para decidir o
equilíbrio de 2010 usa dado de 2012 — look-ahead que não existia na época —, e o nível dele hoje é
**7,7%**, o que implica que a Selic de 15% quase não aperta. A inclinação não tem nenhum dos dois:
é a diferença entre dois preços observados no mesmo pregão, mean-reverting por construção.

Decisão do usuário em 2026-09-21, depois de as alternativas terem sido medidas uma a uma. O
caminho inteiro — inclusive a expectativa de juro real da Focus por horizonte, que **não** serve
porque anda com o juro corrente (beta 1,03 em um ano) — está em
[`pendencias_is_eq.md`](pendencias_is_eq.md) §2.

### E ela entra DEFASADA um trimestre, contra o que o plano pedia

L1 é o pico nas duas convenções de trimestralização, o que torna a escolha robusta em vez de
garimpada: L0 dá −0,113 (média) e −0,069 (fechamento), **L1 dá −0,164 e −0,177**, L2 dá −0,122 e
−0,137. Três razões, todas na mesma direção:

- **É a forma do próprio BC.** A eq. (2) dele é `h = b1·h(−1) − b2·r̂(−1)/4 − b3·rp̂ + …`.
- **A contemporânea tem simultaneidade, visível no dado**: a correlação bruta de `g_rr(t)` com o
  hiato é **positiva** em todas as candidatas (+0,18 a +0,43), sinal trocado, porque o Copom aperta
  quando o hiato abre.
- **Com a média do trimestre ela nem seria predeterminada** — `g_rr(t)` é a média da curva *dentro*
  do trimestre que se quer explicar. A defasagem é o que torna a convenção de média legítima.

### O prêmio de maturidade: medido, e ele é sobre o NÍVEL

A NTN-B carrega taxa estrutural **e** prêmio. Comparando com a expectativa de juro real da Focus,
o spread cresce com o horizonte e a volatilidade dele cai — em 1 e 2 anos ele mistura prêmio com a
convergência de política que falta acontecer; em 3–4 anos o que sobra é estável: **0,89 (desvio
0,61) e 1,11 (desvio 0,65) p.p.** Descontando hoje, 7,56 − 1,11 = **6,45%**, que é onde a Focus de
4 anos está (6,42%) — dois caminhos independentes no mesmo lugar, contra os 5,0% que o BC declara.

**Isso não muda a estimação e a página ainda não diz.** Com intercepto, subtrair uma constante de
`RR*` deixa `h2` idêntico à quarta casa e move só o intercepto; sem intercepto, piora. O prêmio é
informação sobre o nível, e entra como frase — é o item H6 das pendências.

### Sem intercepto, e a média do hiato foi conferida

O plano manda não pôr intercepto "porque o hiato do BC tem média ~0 — **conferir e reportar**".
Conferido: **média −0,18, desvio 1,68**. É pequena contra o desvio, e a página imprime as duas.
`repouso()` afirma numericamente que, com a política neutra e sem crise, a conta devolve **zero**
partindo de quatro pontos diferentes — que é a propriedade que a ausência de intercepto compra.

O intercepto, aliás, quase não decide nada aqui: com ele, `h2` vai de −0,1771 para −0,1752. Ele só
seria decisivo se `RR*` fosse constante, que é justamente a forma descartada.

### O resíduo rejeita em Q(4), e a página diz isso

Q(4) p 0,021 rejeita, Q(8) p 0,097 não; a autocorrelação do erro é 0,33 em um trimestre e 0,03 em
dois — padrão concentrado na primeira defasagem, o que aponta termo faltando e não sazonalidade.
Declarado em quatro lugares da aba, com asserção exigindo que os quatro concordem com o teste nos
dois sentidos.

**Parte disso é o objeto:** o hiato publicado é uma estimativa suavizada dos dois lados, e o BCB
reescreve o passado a cada edição. A série usada é sempre a corrente — o hiato em tempo real ficou
**de fora por decisão do usuário** ("não vou lidar com o problema de vintage agora") e é a
pendência H1, a de maior consequência: a suavização infla `h1` e atenua `h2`.

### As duas crises não são firmes sozinhas, e mesmo assim ficam

`d08` tem t −1,07 e `d20` t −1,48. Pelo t individual nenhuma sobreviveria — mas **tirá-las derruba
o aperto**: `h2` vai de −0,175 para −0,113 e o t de −2,75 para −1,22. Elas não estimam o tamanho da
crise; impedem dois episódios que nenhuma política explica de definirem a inclinação do resto. Os
quatro maiores resíduos da amostra são os quatro trimestres de 2020, **mesmo com `d20` dentro**.

## A aba de Hiato

**Hiato** — a quarta aba. Quatro cartões (o quanto o aperto segura, a meia-vida, o efeito de longo
prazo, o erro típico), dois gráficos, a tabela de pesos e dois folds: a notação matemática e o
bloco de método, que traz **quatro** tabelas — as candidatas a taxa de equilíbrio, as formas
testadas, o diagnóstico de resíduo e a comparação com o BC.

**O segundo gráfico é uma identidade, não um modelo.** Decompõe o hiato em três parcelas — o
aquecimento que já havia, o aperto e as crises — e as três mais o resíduo somam o hiato observado,
com asserção para isso. Empilha em **`relative`** e não em `stack`, porque as parcelas trocam de
sinal. Há guarda de que a parcela de crise é **exatamente zero** fora de 2008-2009 e 2020.

Os ids dos gráficos são `ch-eqis` e `ch-eqis-dec`, e não `ch-hiato*`: **`ch-hiato` já é o gráfico
do hiato na aba de dados** — é a mesma colisão que custou uma rodada na aba de expectativas, e §23b
a proíbe para a página inteira.

## A aba de expectativas

**Expectativas** — a terceira aba. Quatro cartões (a força da âncora, a meia-vida, o repasse de
longo prazo, o erro típico), dois gráficos, a tabela de pesos com a linha de sobra da meta, e dois
folds: a notação matemática e o bloco de erro/comparação com o BC. **A aba mostra a equação como ela
é estimada e nada mais** — não há escada de leituras alternativas nela, porque não há leituras
alternativas na forma no ar; o que foi testado está no arquivo de pendências.

**O segundo gráfico é uma identidade, não um modelo.** Ele decompõe a *distância entre a expectativa
e a meta* em duas parcelas — o que já se esperava e a inflação que saiu — e as duas mais o resíduo
somam exatamente a distância observada, que é a linha por cima. Há asserção para isso, com tolerância de 1e-3 que é o arredondamento do payload e não folga
escolhida. As barras empilham em **`relative`** e não em `stack`: as parcelas trocam de sinal, e
`stack` poria uma contribuição negativa por cima de uma positiva como se as duas somassem.

### O bug que só o browser pegou: dois gráficos com o mesmo `id`

A aba nasceu com os divs `ch-exp` e `ch-exp-dec`. **`ch-exp` já era o gráfico da expectativa na aba
de dados.** `getElementById` devolve o primeiro, então o gráfico desta aba plotou dentro do cartão
da outra, o cartão dele ficou vazio, e a chave repetida em `CHART_META` foi silenciosamente vencida
pela última — o gráfico novo herdou o título e a fonte do antigo. **Nada levantou**: o harness JS
passou com 915 asserções verdes, porque o `getElementById` dele é um mapa e o div novo simplesmente
sobrescreveu a entrada.

O que pegou foi a contagem em browser real: 2 gráficos plotados, **1** cabeçalho, **1** régua de
tempo. O guarda que fecha isso é §23b — os ids de todos os gráficos das três abas têm de ser
distintos, e `CHART_META` não pode ter chave repetida (uma chave repetida num objeto literal não é
erro em JavaScript, a última vence).

## As sete abas

**Dados** — os dezoito insumos em dez gráficos: o cheio e os quatro grupos num só (mesma unidade, e
a aba seguinte decompõe o primeiro nos outros quatro), expectativa, hiato, **as duas pontas da
curva de juro real num só e a inclinação delas em outro** (unidades diferentes: % ao ano contra
p.p., e perguntas diferentes — onde estão as pontas, contra quanto aperta), câmbio, e as duas
cestas de commodity num só, a Selic, as duas expectativas de horizonte longo num só (Focus de 18
meses e projeção do Copom) e as duas metas num só. O trimestre em aberto é marcado em três lugares
(faixa cinza, aviso no topo, linha em itálico na tabela); a coluna `completo` do painel é o que
sustenta isso.

**Juros** e **Câmbio** — as duas últimas, desde 2026-09-22, no mesmo desenho das de Expectativas e
Hiato: dois gráficos (o nível ou a variação contra a conta, e a decomposição em barras que somam o
observado), a tabela de pesos, e um fold de método. Duas coisas próprias delas: na de Juros a âncora
`RR* + Meta` é uma **linha** do primeiro gráfico, e é a distância dela até a Selic que a decomposição
explica — decompor o nível poria a âncora respondendo por quase tudo; e na de Câmbio a ressalva de
que a bolsa americana tem coeficiente de sinal oposto ao da correlação bruta fica **no fluxo da
página**, com a tabela de degraus que mostra em qual controle a virada acontece.

**Curva de Phillips** — o seletor Inflação do trimestre / Acumulado em 12 meses no topo, quatro
cartões de resumo que trocam com ele, o gráfico do cheio (três linhas: realizado, soma dos quatro, e
o piso — ou, em 12 meses, o IPCA publicado como gabarito), a tabela de pesos por grupo, e um gráfico
por grupo. São **dois** folds: o de notação matemática (logo abaixo da introdução) e o de método,
que traz as cinco tabelas — equações em texto, ajustes de calendário, diagnóstico de resíduo,
variantes de alimentação e âncoras de monitorados.

### O peso da expectativa tem LINHA na tabela, marcada como conta de sobra (2026-09-21)

Pedido do usuário, a partir de um print com os quatro cabeçalhos de grupo circulados: *"Por que você
não colocou as expectativas como um parâmetro na lista?"* Ele estava impresso só no cabeçalho de
cada seção, com uma nota de rodapé explicando a ausência.

A razão de ele não ser um coeficiente continua valendo — a restrição é imposta na reparametrização,
então não existe coluna dele na regressão e ele **não tem** margem nem t. Mas isso é argumento para
a linha **dizer o que ela é**, não para ela não existir: o leitor procura o número na lista, e uma
nota de rodapé explicando por que ele não está lá custa mais do que a linha.

Como ficou, e as três decisões que a fazem não mentir:

- **Ela entra logo depois do último peso †**, que é de onde ela sai, e não no fim do bloco.
- **Margem e t saem em travessão.** Inventar `± 0,0000` ali seria afirmar precisão infinita; deixar
  a célula vazia leria como dado faltando. E ela **não** recebe a classe de significância, porque
  não há p-valor a colorir. Há mutante para os três.
- **A coluna de leitura imprime a subtração inteira** — `conta de sobra: 1 − 0,0274 − 0,6880` —, o
  que torna o número verificável na própria linha. Em monitorados, cujo peso restrito é negativo,
  ela sai como `1 − 0,3117 + 0,2253`, e é isso que explica o 0,9136.

**O cabeçalho do grupo deixou de repetir o número**, pela regra de não dizer duas vezes. Há asserção
para isso, senão a duplicata volta na próxima edição da linha.

O que **não** foi feito, e por quê: a margem dele é calculável, porque é combinação linear exata
(`Var(1 − Σβ) = 1'V1`, com o mesmo V de Newey-West). O usuário optou por não construir isso agora.
Está em `pendencias_philips_eq.md`.

### E o click-drop de notação matemática (2026-09-21)

Do mesmo pedido: *"coloque uma parte com click-drop onde eu consigo ver, com boa representação
matemática, as equações do modelo."* O fold antigo já trazia as quatro contas, mas **em texto**
(`Serviços = inércia + média dos 4 trimestres anteriores + expectativa + ...`), que serve para
explicar e não para conferir.

O fold novo traz cinco blocos: as quatro equações em símbolos, a legenda, a restrição na forma em
que é **estimada** (o desvio contra o desvio, sem intercepto) com o estado de repouso e a fórmula do
efeito de longo prazo, o ajuste de trimestre com a soma-zero, a volta ao índice cheio e o
encadeamento de doze meses, e por fim as quatro equações de novo com os pesos ajustados no lugar dos
símbolos.

Quatro decisões, todas com mutante:

- **A notação é GERADA do payload, não escrita à mão.** Símbolo por `key` do coeficiente
  (`MATH_VAR`), parâmetro por posição dentro da equação, e a legenda montada dos mesmos símbolos —
  então nenhum símbolo aparece sem definição e uma equação que mude de forma muda nos dois blocos.
  Uma equação estática ao lado de uma tabela derivada é a terceira face do defeito que
  `.claude/rules/lis-dashboards.md` já documenta duas vezes.
- **Dois regressores da mesma equação não podem dividir símbolo.** É o que separa a defasagem da
  média móvel, que só diferem pela barra — e o `textContent` das duas é idêntico, então a asserção
  compara o HTML. Sem ela, trocar `π̄` por `π` deixa a equação ambígua sem erro nenhum.
- **Um peso negativo vira subtração, nunca `+ −0,2253`.** E a asserção tem de olhar o **texto**: o
  `<span class="tm">` fica entre o sinal e o número, então procurar `"+ −"` no markup nunca casa —
  foi um mutante escapando.
- **Nada de KaTeX nem MathJax.** A notação é HTML e CSS (serif itálico, `sub`/`sup`,
  `text-decoration: overline` para a média móvel), o que evita um terceiro CDN e um stub novo no
  harness. O que se perde é fração empilhada e integral, que esta página não tem.

Sem regra de CSS, `.fold-hint` colava no título do click-drop na mesma fonte e no mesmo peso — a
regra que faltava foi escrita agora e vale para os dois folds da aba.

**O título do gráfico é derivado, não fixo** — um clique no seletor muda o que o gráfico afirma, não
só a escala, então deixá-lo fixo faria a página mentir em metade das vistas. E a régua de tempo é
refeita na troca, porque as duas leituras começam em trimestres diferentes.

---

## Context

`Workflow.md` §(IV.I).i pede **um** modelo estrutural para o sistema macro — equações para inflação,
câmbio, juros, hiato e expectativas — no lugar do modelo de câmbio isolado que hoje vive dentro do
`FX Report.html`. Este plano é o primeiro passo: um dashboard **Structural Model** com uma versão
simplificada do modelo semiestrutural do BC, **estimada equação por equação**, com o modelo do FX
Report reestimado em frequência trimestral como a equação de câmbio.

Simplificações aceitas de partida: sem bloco de preços administrados (IPCA cheio), sem hiato
mundial, sem clima, sem estimação conjunta por filtro de Kalman, e o hiato do produto **lido do
BC** em vez de estimado como estado latente.

---

## O que já existe, e é o que muda o tamanho do trabalho

`analytics/brasil/monetary_policy/` já contém a **réplica completa do modelo agregado do BC**
(boxe RI jun/2024) — 17 dos 22 parâmetros dentro do IC 90% publicado, hiato correlacionando 0,990
com o do BC. As cinco equações pedidas têm correspondente direto:

| pedido | equação do BC já replicada | onde |
|---|---|---|
| `I(t)` Phillips | (1), preços livres | `modelo_agregado.py` docstring |
| `E(t)` expectativas | (5), `estimar_eq5()` | idem |
| `H(t)` IS | (2), hiato latente | idem |
| `R(t)` Taylor | (3), com 2 defasagens | idem |
| `F(t)` câmbio | (4) UIP — **substituída** pelo Ridge do FX Report | idem |

E `modelo_painel.py` já constrói, **validado contra número publicado**, quase todos os insumos:
`focus_ipca_12m()`, `focus_selic_12m()` (ponto de 12m, não média do caminho — erra +0,14 contra
+0,82), `hp(..., cauda=)` (HP com cauda Focus: r\* 2023T4 em 5,01% contra 4,82% publicado; sem a
cauda, 7,15%), `cauda_juro_real()`, `para_q()`, `meta`, `rr_trend`, `r_focus`, `de`, `rp_hat`.
Artefato versionado: `data/modelo_painel_full.csv`, 2001Q4→2026Q3.

Dados no banco (todos confirmados): `inflc_agregados` (`ipca_12m` = SGS 13522), `expc_focus`
(`horizonte='12m', suavizada='S'` desde 2001-11 — a série rolante existe, não precisa ser
interpolada), `expc_focus_copom`, `pm_hiato_produto` (+ `_vintages`), `inflc_meta` (SGS 13521),
`pm_copom_projecoes`, `cmb_ptax`, `comm_icbr_usd` (SGS 29042), `cmb_risco_pais`,
`cmb_dollar_index_em`, `cmb_equity_us`, `diferenciais_juros`.

**Consequência:** o trabalho é escrever um painel e um estimador *simplificados* que **importam**
essas funções (não copiam), reestimar o câmbio em trimestral, e construir o dashboard.

---

## Decisões tomadas

| tema | decisão |
|---|---|
| Frequência | **Tudo trimestral**, incluindo reestimar o Ridge do câmbio |
| Taylor | `R(t) = r1·R(t-1) + (1-r1)·(RR*(t) + Meta) + r2·dI` — steady state = RR*+Meta, `r2` livre |
| Fechamento | **Estima aberto, simula solto — uma equação de cada vez.** Cada equação é estimada sozinha contra dado observado. O simulador saiu de escopo em 2026-09-22 de manhã e **voltou no mesmo dia**, com o desenho trocado: em vez de resolver as cinco juntas, ele recebe uma equação por vez (*"vamos ajeitá-la e depois vamos adicionar outra equação"*). Hoje só a (R) está nele, e enquanto for uma só nada realimenta nada |
| Estimador | **MQ nas cinco; MCMC também na (R)**, desde 2026-09-22. A versão bayesiana não muda a especificação — ela permite pôr priori onde o BC publica, e é ela que dá a faixa do simulador. Ver [`bayes/CLAUDE.md`](bayes/CLAUDE.md) |
| Endogeneidade no câmbio | `carry_vol` (via Selic) e o offset PPP (via IPCA); CDS, `dxy_em`, `sp500`, `icbr_usd` seguem exógenos |
| RR\* | **HP com cauda de projeção Focus** (`modelo_painel.hp`), mais a medição do perfil de revisão |
| `I*(t)` | **IC-Br em USD** (`comm_icbr_usd`) — todo o repasse cambial fica em `i3`, um coeficiente só |
| Volatilidade no `carry_vol` | Janela **defasada** (termina no fecho do trimestre t−1), com fonte trocável para vol implícita de opções quando o usuário fornecer |

### Sobre a volatilidade — a resposta à sua pergunta

Dá, sim, e é o certo. O que existe hoje é `_annualized_vol_6m()`
([ppp_equilibrium.py:438](../exchange_rate/models/ppp_equilibrium.py#L438)): σ móvel
de 126 pregões **terminando em t**. Em trimestral essa janela cobre ~2 trimestres e o trimestre
explicado está dentro dela — a variação do câmbio entra dos dois lados da regressão. Defasar a
janela para terminar no último pregão de t−1 elimina isso inteiramente: o denominador passa a ser
**predeterminado**, conhecido no início de t. É a correção padrão e não custa nada.

O que sobrava depois disso era de *simulação*, não de estimação — e **deixou de ter consumidor em
2026-09-22**, quando o simulador saiu de escopo: vol realizada defasada continua sendo função da
história da própria variável dependente, o que só machucaria dentro de um cenário fechado.

**Vol implícita de opções seria o objeto certo mesmo assim** — é prospectiva, observável em t e não é
função de realização passada do câmbio. O que ela resolve hoje é conceitual e não um defeito: a
defasagem já deixa o denominador predeterminado, que era a metade que valia para a estimação. O código nasce com um seletor `VOL_SOURCE` (`realizada_lag` |
`implicita`) para que a troca seja de série, não de equação. **Não há tabela de vol implícita no
banco** (varredura completa: nada). Quando você fornecer, o destino recomendado é uma tabela
`macro_brasil.cmb_vol_implicita` pelo caminho do conector Bloomberg que já existe
([domain/db/brasil/bloomberg/cmb_risco_pais.py](../../../domain/db/brasil/bloomberg/cmb_risco_pais.py)) — e
**não** um CSV exportado à mão, precisamente porque o `cmb_risco_pais` nesse formato é registrado no
repo como algo que "costuma estar semanas atrás".

---

## O modelo, como vai ser escrito

Todas as variáveis trimestrais. `Meta(t)` é a meta vigente **no horizonte de 12 meses**, não a do
ano corrente (mistura ponderada por meses entre o ano t e t+1; contínua em 3,0% desde 2025).

```
(I)  I(t)  = i1·I(t-1) + (1-i1)·E(t-1) + i2·H(t) + i3·F(t-1) + i4·I*(t) + d08 + d20 + ε
(E)  E(t)  = e1·E(t-1) + e2·I(t) + (1-e1-e2)·Meta(t)                           + ε
(H)  H(t)  = h1·H(t-1) + h2·g_RR(t)                             + d08 + d20 + ε
(R)  R(t)  = r1·R(t-1) + (1-r1)·(RR*(t) + Meta(t)) + r2·dI(t)   + d08 + d20 + ε
(F)  100·Δlog E(t) = Δppp(t)·1 + α + φ·100·Δlog E(t-1) + Σ β_c·z(Δc(t)) + ε
```

Com:
- `I` = IPCA cheio acumulado em 12 meses, no último mês do trimestre (SGS 13522)
- `E` = Focus IPCA 12m à frente, suavizada (`expc_focus`, `suavizada='S'`)
- `H` = `pm_hiato_produto` (`variavel='central'`), % do produto potencial, nível
- `F` = 100·Δlog(PTAX) no trimestre — variação, não nível (é o que torna a equação dimensionalmente
  consistente com `I` em pontos percentuais)
- `I*` = variação trimestral do IC-Br **em USD** (SGS 29042)
- `g_RR(t) = i^e(t,t+4) − π^e(t,t+4) − RR*(t)` — **observável em t**: é a expectativa Focus formada
  em t para 12 meses à frente, não uma realização futura. Diferença simples, como a eq. (2.1) do BC
  (Fisher exato descola ~0,2 p.p.)
- `dI(t)` = `E(t) − Meta(t)` na v1; `pm_copom_projecoes` no horizonte relevante − Meta na v2
- `d08` = 2008Q4–2009Q4, `d20` = 2020Q1–2020Q4 (mesmas janelas do BC), estimado com e sem

**Ordem de solução dentro de t** (recursiva, sem ponto fixo): `H → I → E → R → F`. `I(t)` usaria
`F(t-1)`, predeterminado; `F(t)` usaria `I(t)`, já resolvido. *Esta era a ordem em que o simulador
resolveria as cinco contas. Com ele fora de escopo desde 2026-09-22 nada a executa — fica registrada
porque é a ordem em que as equações foram construídas, e porque volta a valer no dia em que o laço
fechar.*

### Duas ressalvas que vão para a página, não para o rodapé

1. **`I` acumulada em 12 meses amostrada trimestralmente tem janelas sobrepostas**, então o resíduo
   é MA(3) e `i1` é mecanicamente alto (~0,75 só pela sobreposição). Não invalida a especificação —
   ela é coerente em espaço de 12 meses, que é o espaço em que `E` também vive. Duas providências:
   erros-padrão **Newey-West** em todas as equações, e uma coluna de robustez com a inflação
   **trimestral** (a convenção do BC), medida lado a lado. `i1` não é comparável ao `a1L` publicado.
2. **IPCA cheio inclui administrados, que não respondem ao hiato** — então `i2` sai atenuado contra
   o do BC, que estima em preços livres. É o preço da simplificação que você pediu, e a coluna de
   comparação com livres (pesos já recuperados no repo: livres 0,767 / administrados 0,233, R² 0,978)
   mede quanto custa.
3. **`comm_icbr_usd` contra a posição documentada do repo.**
   [domain/db/CLAUDE.md:170](../../../domain/db/CLAUDE.md#L170) diz que o IC-Br em reais é "adequado, sim,
   para a curva de Phillips, onde o repasse cambial é parte do que se quer capturar". A escolha do
   USD é defensável aqui **porque o câmbio é endógeno e `F(t-1)` já está na equação** — os dois
   textos falam de modelos diferentes. Para não ficar só no argumento, a versão em BRL entra como
   **coluna de diagnóstico** no Apêndice, com o repasse cambial total medido nas duas.

---

## Passos, para executar e estudar um a um

### Passo 0 — o painel trimestral

`analytics/brasil/structural_model/panel.py` → `data/panel.csv` (versionado, como em
`monetary_policy/data/`).

Importa de [modelo_painel.py](../monetary_policy/modelo_painel.py): `q`, `serie`,
`para_q`, `hp`, `focus_ipca_12m`, `focus_selic_12m`, `cauda_juro_real`. **Importar, não copiar** —
são funções validadas contra número publicado e duas cópias divergem.

Colunas: `ipca_12m`, `pi_q` (robustez), `pi_e`, `i_e`, `meta_12m`, `rr_star`, `g_rr`, `hiato`,
`hiato_rt` (vintages), `selic`, `de`, `pi_star_usd`, `pi_star_brl`, `dI_focus`, `dI_bcb`, `d08`, `d20`.

Convenção de trimestralização, declarada por coluna porque cada uma é diferente: acumulados de 12m
e PTAX pelo **último** mês; Focus pelo último boletim do trimestre; Selic pela **média**; hiato é
nativo trimestral.

**Entrega para estudar:** o perfil de revisão do HP — `rr_star` calculado com dado até T−k para
k = 0, 2, 4, 8, 12 trimestres, contra uma data fixa. É isso que dá número à sua ideia da defasagem
de 2 anos em vez de intuição.

### Passo 1 — Equação (I), Phillips + o esqueleto do dashboard

`equations/phillips.py`. Restrição `i1 + (1−i1) = 1` imposta regredindo `I(t) − E(t-1)` contra
`I(t-1) − E(t-1)`, `H(t)`, `F(t-1)`, `I*(t)` e as dummies. Newey-West.

Junto vai o esqueleto do relatório (ver Passo 7), para que cada equação seguinte já caia numa aba.

### Passo 2 — Equação (E), expectativas

`equations/expectations.py`. Restrição imposta regredindo `E(t) − Meta` contra `E(t-1) − Meta` e
`I(t) − Meta`, **sem intercepto**. Difere da eq. (5) do BC em dois pontos que a aba declara: não tem
o termo de MA(4) do IPCA passado, e usa a inflação **realizada** no lugar da previsão do próprio
modelo — o que elimina a simultaneidade que no BC custou um estimador em dois passos (condicionar em
π^e observado em t leva φ₂ de 0,21 para 0,42).

### Passo 3 — Equação (H), IS

`equations/is_curve.py`. Sem intercepto (o hiato do BC tem média ~0 — **conferir e reportar**).
`h2 < 0` esperado. Duas colunas: hiato da edição corrente e hiato **real-time** por
`pm_hiato_produto_vintages` — a edição corrente é um objeto suavizado dos dois lados, então `h1` sai
alto e `h2` atenuado, e a coluna real-time é o que mede isso. Atenção à quebra metodológica entre as
edições 2024-06 e 2024-09: só `central` é comparável entre os dois regimes.

### Passo 4 — Equação (R), Taylor

`equations/taylor.py`. Restrição imposta regredindo `R(t) − RR* − Meta` contra
`R(t-1) − RR* − Meta` e `dI(t)`, sem intercepto → devolve `r1` e `r2` diretamente. Duas versões de
`dI` (Focus e projeção do Copom). Coluna de robustez com **segunda defasagem**: o BC estima
t₁ = 1,48 e t₂ = −0,58 (soma 0,90), um perfil de suavização em corcova que uma defasagem só não
reproduz.

### Passo 5 — Equação (F), câmbio trimestral

`equations/fx.py`, uma função nova em cima de
[ridge_deviation_model.py](../exchange_rate/models/ridge_deviation_model.py) — **não
reescrever o mensal**, que continua servindo o FX Report.

- Níveis agregados por `para_q(..., como='last')`, depois diferenciados → Δ trimestral.
- Mesma especificação: offset PPP com β≡1 (perna BR endógena = IPCA da eq. I; perna US = CPI
  exógena), α, AR(1), e os 5 canais (`fiscal`, `dxy_em`, `carry_vol`, `sp500`, `icbr_usd`).
- `carry_vol` = (Selic − Fed Funds) ÷ vol **defasada**, com `VOL_SOURCE` trocável.
- Padronização **escala e não centra** (`z = x/sd`), como o mensal — em colunas de diferença,
  subtrair a média injeta deriva constante de −μ/σ todo período.
- λ por CV walk-forward, `min_train = 16` trimestres.
- **Reportar o modelo mensal ao lado, convertido para unidade nativa** (β nativo = β do payload ÷ o
  σ em `channel_stats`; ex. `fiscal` = 8,236 / 126,31 = 0,0652 pp de câmbio por bp de CDS). A amostra
  cai de 245 para ~81 observações e as bandas de erro ficam mais ruidosas — a coluna mensal é o que
  permite dizer *quanto*.
- Manter o `model_fit_cutoff.json` **separado** do mensal: reestimar um não pode mover o outro.

### Passo 6 — O simulador · *retirado e retomado em 2026-09-22*

Retirado de manhã (*"Não vou mais fazer o simulador"*, *"Pode retirar"*) e retomado à tarde, com
**outro desenho**: *"Vamos fazer a aba do simulador, incorporando equação por equação... começamos
com o modelo de juros"*, e depois *"Coloque essa equação no simulador, vamos ajeitá-la e depois
vamos adicionar outra equação."*

**A diferença entre o plano velho e o que foi construído** é o que decide quais pendências voltam a
valer. O plano pedia um simulador que resolvesse as cinco equações dentro do mesmo trimestre, na
ordem `H → I → E → R → F`, com toggle Endógeno/Manual por equação. O que existe recebe **uma equação
por vez**, e hoje tem uma só — então **nada ainda propaga a saída de uma conta para a entrada de
outra**, e as pendências que dependiam disso (F2, F4, E6, P13) continuam rebaixadas. Elas voltam a
ser decisão **no dia em que a segunda equação entrar**, e não antes.

`simulator.py` monta o payload; a recursão roda **no navegador**, porque o usuário mexe nos
controles. Os pesos vêm do posterior bayesiano gravado em `bayes/data/taylor_draws.json` — a geração
do relatório **não roda MCMC**, ela lê o arquivo, e reestimar é um passo próprio e explícito.

### Dois blocos, e a taxonomia de inputs · *2026-09-22, depois de olhar o FX Report*

Pedido do usuário: *"a aba do simulador vai ter dois blocos: (i) as equações, com as séries
estimadas e o que de fato foi observado; (ii) Os inputs do modelo (Veja o FX_Report). Nos inputs,
teremos variáveis que são endógenas e outras que são exógenas."*

**A divisão não é cosmética, e no segundo round ela ficou mais nítida:** o bloco 1 é o que o
modelo **afirma** e o bloco 2 é o que o usuário **supõe**. Na primeira versão o bloco 1 trazia os
pesos como controle, e o usuário cortou isso — *"por algum motivo você entendeu que eu queria
simular mudanças nos parâmetros. Não quero, a simulação vem dos inputs"*. Num painel só — que é o
que o simulador do `monetary_policy` faz — não dá para dizer se um número mudou porque a conta
mudou ou porque o cenário mudou.

**Endógena e exógena são propriedades DO MODELO, e mudam.** Uma variável é endógena quando alguma
equação *do simulador* a produz; como as equações entram uma de cada vez, a mesma variável troca de
lado ao longo do tempo. O payload carrega os dois fatos **separados**, porque respondem perguntas
diferentes:

```
produzida_por     qual equação do MODELO a produz, exista ela no simulador ou não
produtor_no_sim   se essa equação já está no simulador
```

| input | hoje | produzida por | partes |
|---|---|---|---|
| `selic` | endógena | (R), no simulador | — |
| `di` | **exógena hoje, endógena depois** | (E), fora do simulador | `pi_e_2a`, `meta_24m` |
| `ancora` | exógena | nenhuma | `rr_10a`, `meta_12m` |
| `crise` | exógena | nenhuma | `d08`, `d20` |

A janela padrão são **12 trimestres a partir do primeiro depois do último dado** — ver
"A janela padrão abre PARA A FRENTE", abaixo.

Escrever só "exógena" no cartão do `di` **mentiria por omissão**: o dia em que (E) entrar é
exatamente o dia em que F2, F4, E6 e P13 voltam a ser decisão. E há um desencaixe já visível, que a
nota do cartão declara: **(E) explica a Focus de 12 meses e (R) consome a de 18** (pendência E6) —
`produzida_por` afirma qual equação é a candidata, não que o encaixe esteja resolvido.

**Duas decisões do usuário no mesmo round:** horizonte com **teto** — 8 trimestres na primeira
versão, **12 no fim do dia** —, o que fixa o número de caixas e dispensa a regra de "o que acontece
depois da última caixa" que o FX Report precisa ter; e **nada de controle global de modo** — cada
variável escolhe a própria fonte, o que é o que permite rodar sobre a história com uma entrada
estressada e o resto no observado.

**Três armadilhas de implementação, cada uma já paga:**

- **Listener por `getElementById` em nó criado por `innerHTML` não sobrevive ao re-render** e
  religa a cada desenho, deixando listeners velhos presos aos nós antigos. A ligação é **uma só,
  delegada nos três containers** que existem no markup (`simOpcoes`, `simJanela`, `simInputs`), e o
  render só reescreve conteúdo.
- **O stub de DOM do harness não constrói árvore a partir de `innerHTML`.** Ele ganhou um
  `querySelectorAll` que devolve **sempre vazio** — deliberado: não ter o método faria o código
  estourar num caminho que no navegador funciona, e devolver algo faria um teste de clique passar
  sem exercitar nada. A fiação é coberta em `tests/test_structural_model_browser.js`, em Chrome.
- **O botão de abrir em partes é um alterna e o estado sobrevive ao re-render.** Clicar duas vezes
  fecha, e o seletor seguinte não acha caixa nenhuma — foi uma falha do harness de browser
  reprovando a página certa.

### Segundo round: seis cortes, e o que cada um ensina · *2026-09-22, mesmo dia*

O usuário abriu a aba pronta e mandou seis coisas de uma vez. Cinco são cortes e uma é
alinhamento — e as seis têm a mesma raiz, que vale mais do que a lista: **a aba estava
respondendo perguntas que ninguém fez.**

| pedido | o que saiu |
|---|---|
| *"Por que não usou o padrão do FX para as variáveis de input?"* | o cartão inteiro foi refeito |
| *"Tira essas merdas de cards"* | os 4 stat cards |
| *"deixa a equação somente nas abas individuais"* | o fold de notação e a legenda de símbolos |
| *"a simulação vem dos inputs"* | as 3 caixas de peso e o "Voltar ao estimado" |
| *"tire essa tabela 'O caminho, trimestre a trimestre'"* | a tabela e a nota dela |
| *"'A conta rodando sozinha' tirar essa merda"* | a introdução de cinco parágrafos |

**(i) O cartão de input já tinha um padrão no repositório, e a primeira versão o descreveu em
vez de o reusar.** A seção *12-Month Forecast (Stress Test)* do FX Report tinha sido lida no
round anterior — e o que atravessou foi a *lista de recursos* (caixas por período, choque em
rampa, abrir em partes), não a **forma**. O que faltava era exatamente o que se vê num print:
cartão de largura cheia com fundo mais claro que a página, nome + selo na primeira linha, duas
linhas em mono logo abaixo (**a leitura de hoje** e **a instrução do que se digita ali**), as
ações como **link sublinhado** à direita e não como botão, o par de pills para a escolha
mutuamente exclusiva, e as caixas numa **grade** `repeat(auto-fill, minmax(84px, 1fr))` em vez
de flex com largura fixa. A lição que generaliza: *reusar um padrão é copiar o desenho, não a
lista de recursos* — e a maneira de garantir isso é abrir os dois lado a lado, não a memória do
que se leu.

**A instrução é o pedaço que não tem como derivar**, então ela virou campo do payload
(`instrucao`, um por variável). "Digite quanto a inflação esperada fica acima (ou abaixo) da meta
em cada trimestre, em pontos percentuais" não sai do nome nem da unidade.

**E a caixa ganhou o estado que faltava.** O FX distingue `final` (já publicado, travado) do que
é digitável; aqui a distinção útil é outra, porque o simulador pode partir de qualquer trimestre
da história: **verde ✓** quando aquele trimestre tem dado publicado, **dourado ~** quando passou
do último dado e o valor é o último conhecido repetido. Sem isso uma caixa de 2027 tem a mesma
cara de uma de 2010 e o leitor lê projeção onde há ausência dela. `_simCobertura()` é quem
decide, e o harness afirma nas duas pontas — na função e na classe impressa.

**(iv) Uma faixa de posterior não é um controle de parâmetro.** Foi a única coisa do bloco 1 que
ficou, e o critério é esse: o usuário não escolhe nada ali, a faixa é a **incerteza medida** dos
pesos passando pela dinâmica. O que saiu foram as três caixas em que se digitava `t1`, `t2`,
`t3`. O guarda contra a recaída é uma asserção sobre a **barra renderizada** (`input[type=number]`
com contagem zero), e não um grep no arquivo entregue: a barra nasce de `innerHTML`, então o
texto do fonte não a contém.

**(iii) e (vi): o corte de prosa tem um teste que ele não passava.** A introdução explicava a
diferença entre *ajuste* e *corrida solta* em cinco parágrafos, e a notação repetia a equação que
a aba Juros já escreve. Os dois eram a **nossa conversa transposta para a página** — o mesmo
defeito que `.claude/rules/lis-dashboards.md` já registra na seção de audiência, em outra roupa:
ali era vocabulário de mecanismo, aqui é *volume*. O que sobreviveu do argumento inteiro foi uma
frase dentro do cabeçalho do bloco 1, e o subtítulo do cartão passou a **apontar** para a aba onde
a equação mora, em vez de reproduzi-la.

**Um efeito colateral do corte, que só apareceu no print:** com as duas fontes dos rótulos fundidas
num mapa só, o link saía *"Voltar a o que foi observado"* e o aviso *"A Selic vem de o que foi
observado"*. Rótulo de pill é **nome** e o da prosa é **complemento regido** — são dois mapas
(`SIM_FONTE_ROT` e `SIM_FONTE_DE`), e forçar um só produz português errado nas duas pontas.

**O que continua fora, de propósito:** os cenários salvos em `localStorage` com nome e razão, e o
fold de cenários-base medidos por episódio — os dois existem no FX Report, os dois se pagam, e
nenhum foi pedido. Ficam como próximo passo do simulador.

### A janela padrão abre PARA A FRENTE · *2026-09-22, terceiro round*

*"Eu quero a projeção sempre para frente, não em 2008; e vamos colocar 12 trimestres de projeção."*

A aba abria em `est_i0`, o primeiro trimestre da amostra de estimação (**2006T3**). Tecnicamente é
o mesmo caminho de código de uma projeção — o ponto de partida sempre foi livre, e rodar sobre a
história é um backtest legítimo. Mas **a tela que abre é a resposta que a página dá antes de
alguém clicar em nada**, e a resposta que ela dava era um backtest de 2008. Agora `i0` nasce no
primeiro trimestre *depois* do último dado (2026T3) e o horizonte vai a 12 (2029T2); o backtest
continua a um seletor de distância.

Três coisas que a mudança quebrou, e nenhuma delas levanta erro:

- **O rótulo de um trimestre que não existe.** Com a janela inteira além da série, *todo* índice
  precisa de rótulo derivado — antes era o caso de borda e virou o caso comum. `_simRotIdx` e
  `_simXIdx` derivam da **contagem** de trimestres, nunca somando 3 meses a uma data, que erra na
  virada do ano. O teste exige `\d{4}T[1-4]` no último dos 12, que é o que pega um `2029T5`.
- **A régua de tempo deixava a projeção fora da tela.** O `Tudo` sai dos dados reais (regra da
  casa), e "dados reais" era só `D.sim.x`, que termina no último observado — os 12 trimestres
  eram desenhados e **invisíveis**. A extensão passou a ser a união do observado com a grade
  simulada, e a régua é refeita **quando a ponta direita anda**, não só na primeira pintura. É a
  quarta face da armadilha de eixo de `.claude/rules/lis-dashboards.md` por um caminho novo: lá a
  janela inicial vinha de `autorange`, aqui ela vinha de uma extensão calculada certa para os
  dados **errados**.
- **A linha projetada flutuava solta.** Ela começa no valor que a equação produz para o primeiro
  trimestre, que não é o último observado — então havia um salto visível e nenhuma ligação entre
  as duas linhas. O caminho desenhado passou a **partir do último ponto observado**, e a faixa
  junto, com largura zero ali: no trimestre que já aconteceu não há incerteza de peso. É âncora de
  **desenho** — a recursão não usa aquele ponto como saída, ele é uma das duas defasagens que a
  alimentam.

E o título do gráfico é sempre o da projeção, porque *"a Selic que a conta produz, sem consultar a
observada"* é verdade num backtest e não diz nada aqui, onde não há observada para consultar.

### E a janela deixou de ser escolha · *2026-09-22, ainda no mesmo dia*

*"Não precisa disso, sempre projeta para frente da janela estimada. Por exemplo, se rodamos até o
2T/2026, a projeção passa a ser a partir de 3T/2026 até +12T. Conforme os dados forem saindo, vai
registrando, aqui procura a prática do FX_Report."*

O seletor "Começar em" saiu. `i0` é declarado no payload como **o índice seguinte ao fim da janela
estimada** e a página não oferece outro; a função continua aceitando qualquer `i0`, que é como
`main()` e o teste rodam backtest. O preço está declarado: não dá mais para rodar a conta sobre a
história pela tela.

**A prática do FX Report que isso traz junto é o `FC.nowcast`**, e ela é o que faz a tela se
atualizar sozinha. A janela não se mexe quando o dado anda, então o trimestre que sai passa a cair
**dentro** dela — e um trimestre da janela que já tem dado publicado aparece **travado e verde**,
como o estado `final` de lá, cuja razão está escrita no CSS daquele arquivo: *"so a guess never
overrides data that's already known"*. A trava é por **trimestre**, não por cartão: em Exógeno
destravam as caixas sem dado publicado e as publicadas continuam travadas. A barra imprime quantas
são, e esse número cresce sozinho conforme o dado sai. Reestimar move o corte e a janela anda junto.

### A caixa mostra o número EM USO, e a cor diz de onde ele veio

Do mesmo dia, e o defeito que o usuário viu antes de mim: *"Quando mexo nas premissas os inputs da
selic não se mexem. O contrário deveria ser verdadeiro."*

Estava certo, e a causa é de desenho e não de fiação. As caixas sempre mostravam `SIM.cx[k]`, que é
o caminho **carregado do observado** — para uma variável em Endógeno isso é o último valor repetido,
que não é o que a conta usa e não é o que a linha logo acima desenha. Duas coisas diferentes com a
mesma aparência, e a que estava na tela era a que não vale.

A regra passou a ser uma só: **a caixa mostra o número que aquele trimestre vai usar nesta rodada, e
a cor diz de onde ele veio.**

| cor | de onde vem | edita? |
|---|---|---|
| azul | a equação do simulador produziu | não |
| verde ✓ | dado publicado | nunca |
| dourado ~ | o último valor conhecido, repetido | não |
| branca | você digitou | sim |

Com isso mexer numa premissa move as caixas da Selic, que é o que o usuário esperava — e a mesma
regra deu a resposta para o que mostrar em cada modo, em vez de um `if` por caso.

### O choque ganhou forma, e passou a alcançar as partes

Dois pedidos juntos: *"Não consigo aplicar choque nas partes"* e *"Quero mais opções de choque com
choque temporário — impacto de X p.p. e decaimento com 0.8, choque constante por h trimestres e
decaimento em 0.8 (ou outro número)"*.

Três formas, com ρ = 0,8 de padrão:

```
rampa   v · min(1, (i+1)/n)                sobe até o valor e fica lá
decai   v · ρ^i                            entra de uma vez e vai passando
const   v até i < n, depois v · ρ^(i−n+1)  fica n trimestres e depois vai passando
```

A terceira **contém** a segunda (`n = 1` faz as duas coincidirem) e as duas existem separadas
porque foram pedidas separadas e porque a segunda se escreve com dois campos em vez de três — o
teste afirma a coincidência, que é o que impede as duas implementações de divergirem.

Duas coisas que valem além deste relatório:

- **O choque começa no primeiro trimestre que dá para editar**, não no primeiro da janela. Com a
  janela fixa, o trimestre publicado entra nela conforme o dado sai — e um choque que somasse
  posicionalmente iria perdendo os primeiros períodos em silêncio. "X no primeiro trimestre" quer
  dizer o primeiro que o usuário controla.
- **A prévia do perfil fica ao lado dos campos** (`soma +2,00 · +2,00 · +1,60 · +1,28 …`). Uma
  forma de choque descrita em prosa é uma forma que o usuário só descobre depois de aplicar; a
  prévia custa uma linha e torna os três campos legíveis de uma vez.

E o choque numa **parte** soma na primitiva e recompõe o agregado pela fórmula — que é o que faz
estressar o juro real sem mexer na meta ser um cenário diferente de estressar a soma. A fonte que
passa para Exógeno é a do **pai**, porque é ele que a conta lê, e o cartão abre nas partes para o
usuário ver onde o choque entrou. O contrário continua valendo: chocar o **agregado** devolve as
partes ao observado, porque distribuir uma soma entre duas parcelas exigiria uma regra que não
existe.

### E o gráfico ganhou 300 px

*"Os gráficos estão ridiculamente pequenos, colocar mais uns 300px na dimensão Y."* `.chart-plot` e
o `height` de `mkLayout()` foram de **340 para 640**; o gráfico pequeno dentro do cartão de input,
que é um painel auxiliar e não um gráfico da página, foi de 200 para 320. Vale para as sete abas,
porque as duas medidas são compartilhadas.


**As armadilhas já pisadas no simulador do `monetary_policy`** valem aqui e estão respeitadas:
guardar valor exato e não a string arredondada; o horizonte não é janela de exibição; e duas âncoras
distintas. Mais duas que nasceram aqui:

- **As dummies de crise entram na recursão.** A primeira versão as esqueceu e a corrida solta
  acusava o maior desvio em 2020T4, exatamente dentro da janela da `d20` — o erro era da simulação,
  não da equação. Nada levanta: o caminho sai plausível e errado.
- **A faixa que inclui o choque tem semente fixa.** Sem isso ela treme a cada clique em qualquer
  outro controle, e o leitor lê movimento de ruído como mudança de resultado.

**E o que a corrida solta mediu, que é o motivo de a aba existir.** Rodando a regra sem
reancoragem, partindo de cada trimestre possível e comparando com a Selic observada:

```
horizonte   partidas   erro médio abs.   RMSE
  4 tri         77          0,945        1,205
  8 tri         73          1,257        1,574
 12 tri         69          1,399        1,718
 20 tri         61          1,563        1,882
 40 tri         41          1,659        1,969
 80 tri          1          1,694        1,969
        ajuste de um passo à frente:     0,566
```

**O erro cresce e SATURA**, em torno de 1,7 p.p. a partir de uns 20 trimestres. Isso é o que se
espera de uma conta estacionária: ela volta para a âncora sozinha, e o que sobra é o tamanho dos
choques que ela não vê. Se houvesse viés de especificação o erro não pararia de crescer — foi a
primeira hipótese ao ver 1,97 de RMSE contra 0,566, e a tabela a descarta. O que a corrida solta
custa é um fator de 3,5 sobre o ajuste, e é esse o preço honesto de não reancorar.


### Passo 7 — O dashboard

`analytics/brasil/structural_model/` → `reports/brasil/Structural Model.html`. Nome de arquivo em
inglês, conteúdo em pt-BR (`lang="pt-BR"`), como os outros 8 relatórios do Brasil.

Arquivos: `__init__.py`, `report.html`, `generate_report.py`, um `*_tab.py` por aba, `CLAUDE.md`,
`data/`, `panel.py`, `equations/`, `simulator.py`, `bayes/`.

Abas: **Dados · Curva de Phillips · Expectativas · Hiato · Juros · Câmbio · Simulador · Apêndice**.
As sete primeiras estão no ar desde 2026-09-22; o **Apêndice é o único que falta**.

Contrato do relatório (tudo já padronizado no repo, ver
[report_structure/CLAUDE.md](../../report_structure/CLAUDE.md)):
os 5 marcadores (`/*REPORT_DATA*/`, `/*THEME_CSS*/`, `/*Y_AUTOFIT_JS*/`, `/*CHART_HEAD_CSS*/`,
`/*CHART_HEAD_JS*/`); `var D = REPORT_DATA;` com **`var`**, não `const` (o teste lê pelo contexto do
vm); `var CHART_META = {...}` com título e fonte por gráfico; Plotly 2.35.2; `run(output=...)` com
esse nome de parâmetro exato (`status.gerar()` chama assim, outro nome estoura TypeError);
`render_report(_TEMPLATE, data, output)`; um `_load_*()` por seção em try/except próprio.

Ler antes de escrever gráfico: [.claude/rules/lis-dashboards.md](../../../.claude/rules/lis-dashboards.md) —
réguas de range **abaixo** do gráfico e com `[from, to]` calculado dos traces (inclusive o "Tudo"),
primeira pintura com janela calculada e não `autorange`, `type:'linear'` explícito em todo eixo X que
não seja tempo, cabeçalho de 3 linhas dentro do card, ΔE2000 ≥ 20 entre séries que dividem gráfico, e
prosa escrita para quem nunca viu o dashboard.

### Passo 8 — Registro e testes

- `domain/dashboards/manifest.yaml`: entrada `key: brasil_structural_model`, `area: brasil`,
  `module`, `output`, `command`, `build_seconds` **medido**, um `role:` por dependência, `note:` em
  voz de produto (há um guarda em `tests/test_release_calendar_js.js` que reprova jargão como
  `generate_report`, `manifest.yaml`, `granularidade`).
- `procedures:` **sim, aqui é legítimo** — dois passos, `painel` e `modelo`, `granularidade:
  trimestre`. A regra da raiz ("um passo é dívida") pergunta se aquilo não deveria ser uma tabela;
  estimação de modelo não tem tabela que a substitua, que é exatamente por que os três passos do
  `monetary_policy` sobreviveram. `cut_from` obrigatório e dentro de `writes`.
- Nada a editar em `registry.py`, `update_db.py` ou `analytics/release_calendar/` — o regerar
  resolve pelo manifesto (`status.regerar_afetados`).
- `tests/test_structural_model_js.js` no padrão da casa (lê o HTML **gerado**, extrai o último
  `<script>`, DOM montado do markup real, stub de Plotly síncrono, `vm.runInContext`).
- Acrescentar `reports/brasil/Structural Model.html` à lista `GERADOS` de
  `tests/test_chart_head_js.js` (a §2 dele já varre `analytics/**/report.html` sozinha e reprova um
  relatório que plota sem cabeçalho).
- Linha nova na tabela de relatórios do `CLAUDE.md` da raiz e na de `analytics/CLAUDE.md`.

---

## Verification

Por passo, não só no fim:

```powershell
# painel
uv run python analytics/brasil/structural_model/panel.py
# cada equação: imprime coeficientes, NW t-stats, R2, e a coluna de robustez
uv run python -m analytics.brasil.structural_model.equations.phillips
# ... expectations, is_curve, taylor, fx
# relatório
uv run python -c "from analytics.brasil.structural_model.generate_report import run; run()"
node tests/test_structural_model_js.js
node tests/test_chart_head_js.js
uv run python -m domain.dashboards.status --validar
uv run python -m domain.dashboards.status --gerar brasil_structural_model
```

Validações que valem mais que "rodou sem exceção":

1. **Cada restrição fecha numericamente** — os pesos de (E) somam 1; o steady state de (R) com
   `dI=0` devolve `RR* + Meta`; o offset PPP de (F) tem β = 1 nos três lugares do payload.
2. **Sinais e ordens de grandeza contra o BC**: `i2 > 0`, `h2 < 0`, `r1` entre 0,7 e 0,95,
   `r2 > 1`. Cada um com o valor publicado do boxe ao lado na tabela do Apêndice.
3. **O câmbio trimestral contra o mensal**, em unidade nativa, canal a canal.
4. **Uma inversão de sinal que só um gabarito pega**: antes de dividir duas séries, conferir se a
   fonte já publica a razão. Vale aqui para `g_RR` — o juro real ex-ante da Focus é reconstruível de
   duas maneiras e o repo já mediu qual bate (diferença simples, não Fisher).
5. **Confirmação em browser real** — *feita em 2026-09-17 e refeita em 2026-09-22, com as seis abas
   no ar. Esta linha dizia "nunca foi feita em nenhum relatório desta pasta" e era do plano original.*
   Segue valendo como passo obrigatório a cada aba nova: Chrome headless via CDP, contando gráficos
   de fato pintados pelo Plotly, cabeçalhos e réguas — é o que pegou o `id` repetido que o harness JS
   não pegava.

*O que era o item 3 — "o simulador reproduz a história quando alimentado com os exógenos realizados"
— saiu com o Passo 6.*

---

## Fora de escopo, declarado

Preços administrados como bloco próprio; hiato mundial; hiato estimado como estado latente (usamos o
do BC); CDS endógeno a um bloco fiscal; reseleção dos 5 canais do câmbio em frequência trimestral
(o corte 8→5 foi medido em mensal — se o `carry_vol` sair instável no trimestral, a alternativa
medida é dividi-lo em gap de política + vol, cujos loaders já existem); e a unificação com o modelo
do `FX Report`, que continua servindo o relatório cambial até este provar que o substitui.

---

## Pending

**Uma lista por equação, e elas são a fonte:** [`pendencias_philips_eq.md`](pendencias_philips_eq.md) para (I) — variáveis a acrescentar e testar, formas a experimentar, testes que faltam e a ordem sugerida —, [`pendencias_expectativas_eq.md`](pendencias_expectativas_eq.md) para (E), [`pendencias_is_eq.md`](pendencias_is_eq.md) para (H), [`pendencias_taylor_eq.md`](pendencias_taylor_eq.md) para (R) e [`pendencias_fx_eq.md`](pendencias_fx_eq.md) para (F), que guardam tudo o que foi medido e **não** entrou nas formas. O que segue aqui é o resumo, e nele não entra detalhe que aqueles arquivos já carregam.

- **O plano de trabalho combinado com o usuário em 2026-09-21**, e que vale sobre qualquer item
  desta lista: **primeiro pôr todas as equações de pé na especificação do plano, depois listar as
  pendências de cada uma, e só então fazer os ajustes.** Mudança de especificação não é decisão de
  quem implementa.

- **(IM): indexar à parte LIVRE do índice, não ao cheio.** É o conserto do sinal negativo — medido
  que o horizonte da âncora não é a causa. Alternativa equivalente: cheio ex-monitorados.
- **Parâmetros variando no tempo**, e o sazonal de serviços é o caso com evidência: −0,042 p.p. por
  ano em Q1 (t −3,02). Mesma maquinaria dos `A_t` do BC — filtro de Kalman, não MQ.
- **Os `A_t` do BC**, um passeio aleatório por setor, que é o que permitiria preços relativos
  derivarem em vez de os quatro convergirem ao mesmo número.
- **O que a especificação do BC tem e a nossa não**: Brent em (II) e o bloco de clima (ONI) em (IA).
  A média móvel de 4 trimestres, que também faltava, **entrou em 2026-09-17** — e por medição, não
  por cópia.
- **Decomposição e teste de estresse**, no padrão das seções *Exchange Rate Decomposition* e
  *12-Month Forecast (Stress Test)* do `FX Report`. Pedido em 2026-09-16 e nunca entregue; a vista de
  12 meses construída em 2026-09-17 **não** cobre a segunda: ela é leitura do ajuste histórico,
  não projeção sob cenário.
- **A (R) está estimada e NÃO está na tela**, desde 2026-09-21. O módulo é
  [`equations/taylor.py`](equations/taylor.py) e o painel ganhou `selic`, `selic_fim`, `pi_e_2a`,
  `meta_24m` e `pi_bcb` — nenhuma dessas cinco aparece na aba de Dados, porque o `_ORDEM` de
  `generate_report.py` é lista explícita. A forma tem **duas defasagens** e mede o desvio na
  **Focus de 18 meses**, as duas por decisão do usuário. Com ela os **três parâmetros comparáveis
  caem dentro dos intervalos que o BC publica**: `r1` +1,434 contra +1,48 [1,41; 1,54], `r1b`
  −0,570 contra −0,58 [−0,63; −0,52] e efeito de longo prazo 2,62 contra 2,03 [1,47; 2,64]. O
  resíduo é **indistinguível de ruído branco** (Q(4) p 0,683, Q(8) p 0,438) — a única das quatro
  equações em que o Ljung-Box não rejeita. Duas ressalvas declaradas: o efeito de longo prazo
  encosta no teto do intervalo (2,62 contra 2,64) e ainda não tem margem própria (R8), e a Focus de
  12 meses ajusta um pouco melhor (R² 0,957 contra 0,952) — ela volta a ser olhada, é o item R5.
- **RR\* é o juro real de 10 anos CRU**, por decisão do usuário no mesmo dia — ele viu a tabela de
  janelas e escolheu não perder amostra. Custo aberto (R2): a RR\* correlaciona +0,80 com o próprio
  aperto monetário, o que atenua o coeficiente. Ganho medido: 81 trimestres em vez de 62, as duas
  dummies de crise com suporte, e o resíduo da coluna de duas defasagens limpo.
- **As sete abas estão na tela desde 2026-09-22**, e a confirmação em browser real foi refeita
  (Chrome headless via CDP): 23 gráficos pintados pelo Plotly de verdade, 23 cabeçalhos de três
  linhas, as réguas de tempo todas depois do gráfico, nenhum id repetido, zero exceções, e as duas
  identidades das barras empilhadas conferidas **na tela** e não só no payload.
- **A (F) está estimada**, desde 2026-09-22. O módulo é
  [`equations/fx.py`](equations/fx.py), construído **sobre** o `ridge_deviation_model.py` do FX
  Report (importa `load_data`, a escala, a validação cruzada e o ajuste), sem reescrever o mensal.
  81 trimestres, 2006T2→2026T2, R² **0,8115** contra 0,6532 do mensal, resíduo limpo (Q(4) p 0,822).
  **Os seis coeficientes têm o mesmo sinal nas duas frequências** e o α é indistinguível de zero nas
  duas, que é o que o offset de PPP existe para produzir — ele leva 67% da desvalorização acumulada,
  e sobram 1,33× de desvalorização real.
- **A ressalva que a barra de decomposição não diz sozinha** (F1, e ela vale para o FX Report
  publicado, não só para esta equação): `sp500` é o único canal cujo coeficiente tem sinal **oposto**
  ao da sua correlação bruta com o câmbio — corr −0,435 e β +1,898. Não é artefato: o mensal tem o
  mesmo padrão (−0,428 e +0,764). Bolsa subindo *é* risk-on, e risk-on comprime o CDS e enfraquece o
  dólar contra emergentes; segurados esses dois, o que sobra move o real na direção oposta. A
  contribuição acumulada de +39,8 p.p. — 46% do movimento — é objeto **condicional**.
- **Duas convenções de câmbio convivem, e desde 2026-09-22 nada as liga** (F2): a (F) mede o
  fechamento do trimestre e a coluna `de` do painel, que é o `F(t)` da curva de Phillips, mede a
  variação da média (desvios 8,32 contra 6,76). Enquanto cada equação é estimada sozinha contra dado
  observado, cada uma usa o que o seu desenho pede e isso não é erro. Era o simulador que não poderia
  ignorar a diferença, e ele saiu de escopo — **a pendência caiu de decisão a tomar para
  inconsistência declarada**, e volta a ser decisão no dia em que alguma coisa propagar `F` de uma
  equação para a outra.
- **O simulador está no ar com uma equação**, a (R), desde 2026-09-22. A próxima entra quando o
  usuário disser qual — e é a segunda que faz `F2`, `F4`, `E6` e `P13` voltarem a ser decisão. Do
  plano da pasta sobra o **Apêndice**.
- **R8 está respondida** desde 2026-09-22, pela estimação bayesiana: o efeito de longo prazo da
  regra de juros é **2,61, com intervalo de 90% de [1,23; 4,12]**, contra 1,17 de largura do
  intervalo que o BC publica. A probabilidade de ele cair dentro do IC publicado é **0,44** — ou
  seja, a frase "os três parâmetros caem dentro dos intervalos do BC" vale para `t1` e `t2` e **não**
  sustenta o terceiro, que é praticamente não identificado nesta amostra. As equivalentes P16/E7/H8
  continuam abertas.
- **A (H) está de pé, e a pendência-raiz dela é o hiato em tempo real** (H1 do arquivo dela),
  deixado de fora por decisão explícita do usuário em 2026-09-21. A série usada é a edição
  corrente do anexo do RPM, que é suavizada dos dois lados e infla a persistência.
- **A ordem de solução `H → I → E → R → F` ainda não tem executor.** Ela era a ordem em que o
  simulador do plano resolveria as cinco contas dentro do mesmo trimestre. O que existe roda **uma
  equação de cada vez**, então com uma só no ar a ordem não faz diferença nenhuma — ela passa a
  valer quando houver duas que se alimentem.
- ~~**Confirmação em browser real**~~ — **refeita em 2026-09-17** depois da troca de abas (Chrome
  headless via CDP, WebSocket nativo do Node, sem npm): 10 gráficos plotados pelo Plotly de verdade,
  10 cabeçalhos de três linhas, o seletor levando eixo/título/séries/régua para a leitura de 12
  meses e de volta, e **zero exceções**. Cobre carga, pintura e o seletor; pan/zoom continua sem
  confirmação visual.
- **Vol implícita de opções do câmbio** — o usuário vai fornecer. Até lá,
  `VOL_SOURCE=realizada_lag`. Destino recomendado: tabela `macro_brasil.cmb_vol_implicita` pelo
  conector Bloomberg, não CSV à mão.
