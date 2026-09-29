# analytics/brasil/structural_model/ — Contexto para o Claude

**Estado: as cinco equações estão estimadas e as cinco rodam no simulador** — (I) Phillips em
quatro grupos de preço, (E) expectativas, (H) curva IS, (R) regra de juros e (F) câmbio —, na ordem
de solução **(H) → (I) → (E) → (R) → (F)**, resolvidas juntas porque desde 2026-09-28 o modelo é um
laço, com os pesos vindos de uma estimação bayesiana da mesma equação. A aba do simulador se chama
**Structural Model** desde o mesmo dia: é o modelo agregado, e a oitava aba, **Impulso-resposta**, choca
o mesmo sistema (ver a seção dela, no fim). Do plano original falta o **Apêndice**. Este arquivo ainda é, em parte, o *plano*
aprovado em 2026-09-16, e vai sendo substituído pelo estado real à medida que cada equação fica
pronta. Histórico rodada-a-rodada vive no git log, não aqui.

## Como rodar

```powershell
uv run python analytics/brasil/structural_model/panel.py                      # painel -> data/panel.csv
uv run python -m analytics.brasil.structural_model.equations.phillips_sub     # as quatro de (I)
uv run python -m analytics.brasil.structural_model.equations.expectations     # a equação (E)
uv run python -m analytics.brasil.structural_model.equations.is_curve         # a equação (H)
uv run python -m analytics.brasil.structural_model.equations.taylor           # a equação (R)
uv run python -m analytics.brasil.structural_model.equations.fx               # a equação (F)
uv run python -m analytics.brasil.structural_model.simulator                  # a corrida solta das cinco
uv run python -m analytics.brasil.structural_model.irf                        # impulso-resposta, pesos da mediana
uv run python -c "from analytics.brasil.structural_model.generate_report import run; run()"
node tests/test_structural_model_js.js                                        # 1.926 asserções
node tests/test_structural_model_browser.js                                   # 112, em Chrome
```

**Os pesos do simulador NÃO são recalculados na geração** — ela lê três arquivos de desenhos
gravados por [`bayes/`](bayes/CLAUDE.md). Reestimar é um passo próprio e explícito; o caminho
inteiro está lá.

| Módulo | O que faz |
|---|---|
| `panel.py` | Painel trimestral dos insumos. `construir()` monta do banco, `salvar()` grava `data/panel.csv`. Importa `q`/`serie`/`para_q`/`focus_ipca_12m` de `modelo_agregado/modelo_painel.py` — não copia. `ipca_12m_publicado()` é **gabarito** da leitura de 12 meses e o termo de inflação de (E); `metas()` monta a meta do horizonte de 12 meses e devolve o último ano que o CMN de fato publicou; `ntnb_real()` lê a curva real da B3 nos vértices de 2 e 10 anos, de onde sai o aperto de (H) |
| `equations/phillips_sub.py` | As quatro equações. `estimar()` roda na amostra comum e reconstrói o cheio; `comparar_ia()` e `comparar_im()` são os dois testes de forma registrados na tela; `sem_sazonais()` é o contrafactual das dummies de trimestre; `leitura_12m()` encadeia o ajuste trimestral de quatro em quatro — **tradução de unidade, não previsão** |
| `equations/expectations.py` | A equação (E), **na especificação do plano e nada além dela**. `estimar()` impõe a soma-um por reparametrização e devolve a meia-vida e o repasse; `repouso()` confere **numericamente** que a conta devolve a meta e que o repasse simulado bate com a fórmula |
| `equations/is_curve.py` | A equação (H), a curva IS. O aperto monetário é a **inclinação da curva de juro real** (2 anos menos 10), não um juro contra um neutro — `comparar_rr()` é o registro medido do porquê, e `comparar()` traz as outras formas testadas. `repouso()` confere **numericamente** que o hiato volta a zero sem intercepto e que o efeito de longo prazo bate com a fórmula |
| `equations/taylor.py` | A equação (R), com **duas defasagens** e a âncora `RR* + Meta`. `DI_BASE` declara em que horizonte o desvio é medido (12 meses desde 2026-09-24), e `COMPARAR` lê essa declaração em vez de repetir o nome dela |
| `equations/fx.py` | A equação (F), construída **sobre** o `ridge_deviation_model.py` do FX Report — importa o carregamento, a escala, a validação cruzada e o ajuste, sem reescrever o mensal |
| `bayes/` | As três equações do simulador por MCMC, cada uma chamando a `montar()` do módulo pontual e trocando só o estimador. É de onde sai a faixa ↳ [`bayes/CLAUDE.md`](bayes/CLAUDE.md) |
| `irf.py` | A aba Impulso-resposta: os alvos de choque, o perfil e a resposta, que é a mesma conta do navegador. `construir()` grava no payload os alvos e um **gabarito** de cinco choques resolvidos aqui |
| `simulator.py` | Monta o payload do simulador e roda a **mesma recursão** que o navegador roda, para o teste poder conferir as duas pontas. `derivadas()` faz as contas que cada equação declara em `deriva`; `_ajuste_*()` são os gabaritos de um passo |
| `generate_report.py` | Chama `panel.construir()` e as cinco estimações **ao vivo** (≈90s) e injeta em `report.html`. Sem artefato intermediário e sem passo de recálculo declarado. Importa as modas publicadas da eq. (2) do BC de `monetary_policy.modelo_agregado` em vez de redigitá-las |

**Duas subpastas que não são este dashboard** (desde 2026-09-24, vindas de
`analytics/brasil/monetary_policy/` quando aquela pasta passou a guardar só o relatório):
[`modelo_agregado/`](modelo_agregado/CLAUDE.md) — a réplica do modelo agregado do BC, de onde este
modelo importa as modas publicadas e as funções do painel — e
[`experimentos/`](experimentos/CLAUDE.md) — Curva de Phillips em planilha, teste do LSTM, teste TVP e
o legado `curva_juros`, que nenhum dashboard usa.

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

## As oito abas

**Impulso-resposta** — a oitava, desde 2026-09-28; ver a seção dela no fim do arquivo.


**Dados** — os dezoito insumos em dez gráficos: o cheio e os quatro grupos num só (mesma unidade, e
a aba seguinte decompõe o primeiro nos outros quatro), expectativa, hiato, **as duas pontas da
curva de juro real num só e a inclinação delas em outro** (unidades diferentes: % ao ano contra
p.p., e perguntas diferentes — onde estão as pontas, contra quanto aperta), câmbio, e as duas
cestas de commodity num só, a Selic, as duas expectativas de horizonte longo num só (Focus de 18
meses e projeção do Copom) e as duas metas num só. O trimestre em aberto é marcado em três lugares
(faixa cinza, aviso no topo, linha em itálico na tabela); a coluna `completo` do painel é o que
sustenta isso.

O gráfico da inflação tem, desde 2026-09-28 e a pedido do usuário, um seletor **Do trimestre / Em
12 meses** dentro do cartão. É só leitura: `D.doze.s12` sai de `phillips_sub.acum12` (a mesma do
seletor da aba de Phillips), o título, o eixo, o resumo, a régua e a unidade do cartão de definição
trocam juntos, e a introdução imprime o erro contra o IPCA de 12 meses publicado (0,0024 p.p. de
média, 0,0056 de máximo, 96 trimestres). Só as cinco taxas de inflação ganharam a segunda leitura —
câmbio e commodities também são variações do trimestre, mas não há 12 meses publicado para conferir
e o que se lê deles é o choque de cada trimestre. A tabela segue na leitura das contas.

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
| Fechamento | **Estima aberto, simula solto — uma equação de cada vez.** Cada equação é estimada sozinha contra dado observado. O simulador saiu de escopo em 2026-09-22 de manhã e **voltou no mesmo dia**, com o desenho trocado: em vez de resolver as cinco juntas, ele recebe uma equação por vez (*"vamos ajeitá-la e depois vamos adicionar outra equação"*). Desde 2026-09-24 estão nele a **(R)** e a **(F)**, nessa ordem de solução. Continua sem realimentação: a (F) lê a Selic que a (R) produz, e a (R) não lê o câmbio — então a recursão fecha sem ponto fixo |
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
`modelo_agregado/data/`).

Importa de [modelo_painel.py](modelo_agregado/modelo_painel.py): `q`, `serie`,
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

### E o gráfico ganhou 300 px, e devolveu 150

*"Os gráficos estão ridiculamente pequenos, colocar mais uns 300px na dimensão Y."* `.chart-plot` e
o `height` de `mkLayout()` foram de **340 para 640**; o gráfico pequeno dentro do cartão de input,
que é um painel auxiliar e não um gráfico da página, foi de 200 para 320. Vale para as sete abas,
porque as duas medidas são compartilhadas. Dois dias depois, *"pode retirar uns 150px do gráfico"* —
**490** hoje. O painel auxiliar ficou em 320: ele não estava no pedido, e é o gráfico dentro do
cartão, não o da página.

## Quinto round: o que ficou foi o que não é escolha · *2026-09-24*

Quatro cortes num dia, e eles têm um fio comum que vale mais que cada um: **sobrou na tela só o que
o leitor de fato decide.** O que a conta usa e ninguém escolhe passou a ser impresso, não oferecido.

### A barra "o desenho" saiu, e a faixa ficou

*"Coisa para retirar"*, com o print da barra: as duas caixas de marcar (a faixa do posterior e o
erro da equação). A faixa **continua desenhada** e não se desliga mais, que é a conclusão coerente
com o corte dos pesos dois dias antes: *incerteza medida não é controle* — quem lê não escolhe
nada ali. O erro da equação saiu inteiro, com o gerador de normal de semente fixa que só existia
para ele, e a recursão do JS voltou a ser **exatamente** a de `simulator._sim` (sem o parâmetro
`eps`, que o Python nunca teve).

O que a caixa de marcar dizia não se perdeu: virou o **nome da faixa na legenda** — *"Faixa de 90%
dos 1000 conjuntos de pesos estimados"*. Um controle que some levando a informação junto é um corte
pela metade.

### E o horizonte também não é escolha

*"Esse negócio para escolher a quantidade de trimestres no horizonte não é necessário. Deixe sempre
12T."* A barra da janela deixou de ter qualquer controle: ela **diz** `2026T3 a 2029T2 · 12
trimestres`, e a delegação de eventos caiu de três containers para um. `SIM.h` continua clampado em
`renderSim()` — não por causa da tela, que não escreve mais nele, mas porque caixa, grade e faixa
são dimensionadas por ele e não há onde checar isso depois.

### As crises saíram do bloco 2

*"Pode retirar os choques de crise do dashboard, pois pretendo usá-las mais como ajuste do que
variáveis exógenas."* Elas **continuam na equação**, com o peso que a estimação mediu, e valem zero
em todo trimestre projetado.

O detalhe de encanamento é o que vale registrar: a série das duas marcas era uma **primitiva**
(`prim.d08`, `prim.d20`), e primitiva é parte de um cartão. Sem cartão elas ficariam penduradas —
uma chave que nada alcança, com entrada de choque criada no `initSim` e nunca usada. Foram para
dentro da própria equação, `eq.dummy_obs`, que é quem as lê. Com isso `simCaminhoParte()` ficou sem
chamador e saiu junto.

**O risco desse corte é silencioso**, e é o motivo de ele ter ganhado guarda próprio (§8a2): tirar o
cartão e tirar os pesos da recursão junto produz um caminho de Selic ligeiramente diferente e
inteiramente plausível. O teste afirma as duas metades — não há cartão nem primitiva de crise, **e**
a equação continua com as duas marcas, com peso no posterior e com `ent[c]` valendo zero nos doze
trimestres projetados.

### E a linha da premissa segue junto

*"O juro nominal também faz parte do gráfico, sendo assim, pode extrapolá-lo para frente também."*

O gráfico tinha três coisas atravessando o corte — a Selic observada, a Selic que a conta produz e a
faixa — e uma que parava nele: o juro nominal de equilíbrio, desenhado só sobre a amostra. Mas ele é
um **input da conta**, e a conta o usa nos doze trimestres projetados; a linha parava onde o número
não parava.

O que torna a extensão honesta é ela não ser extrapolação nenhuma: o trecho projetado é
**exatamente `r.ent.ancora`**, o caminho que a recursão consome. Se a premissa é Observado, é o
último valor repetido; se é Exógeno, é o que foi digitado; se levou choque, é o choque. É a regra
das caixas aplicada à linha — *mostra o número em uso*. Uma extrapolação própria do desenho poderia
discordar da conta sem nada avisar, e é isso que a asserção fecha, trimestre a trimestre.

Duas escolhas de desenho: ela **parte do último ponto observado**, pela mesma razão da linha da
Selic (senão flutua solta à direita); e **não ganha legenda própria**, porque é a mesma linha
continuando — a faixa cinza da projeção já diz onde o dado acaba, e o hover marca `(premissa)`.

### E depois a expectativa foi uniformizada em 12 meses

*"Antes de seguirmos, vamos uniformizar a expectativa de inflação para 12 meses."* Uma linha —
`taylor.DI_BASE` de `focus2a` para `focus` — mais reestimar o MCMC, porque os desenhos que o
simulador lê tinham sido gerados sobre a outra janela.

**A razão não é de ajuste, é de horizonte**, e é o que torna a decisão estrutural em vez de
estatística: as três equações que falam de expectativa — (I), (E) e (R) — passam a falar da mesma
janela, e só assim a equação de expectativas pode alimentar a regra de juros. **Fecha E6 e a
ressalva de R8 de uma vez**, e o detalhe medido está em [`pendencias_taylor_eq.md`](pendencias_taylor_eq.md) §R5:
o efeito de longo prazo sai de 2,62 (encostado no teto de 2,64 que o BC publica) para **1,962**, no
meio do intervalo, enquanto as medianas das duas defasagens saem dos intervalos estreitos do BC — os
pontos publicados continuam dentro do nosso HDI de 90%, que é a comparação que 80 trimestres
sustentam.

Dois efeitos colaterais que valem além desta pasta:

- **A prosa que justificava a escolha dizia o contrário do que a tabela ao lado passou a mostrar.**
  A nota da tabela de comparação explicava por que a de 18 meses tinha ficado; com a base trocada,
  a mesma frase virou mentira ao lado de números derivados que a negavam. É a terceira ocorrência do
  defeito que `.claude/rules/lis-dashboards.md` já registra. O corretivo foi derivar também a
  variante: `COMPARAR["base"]` passou a ler `DI_BASE` em vez de repetir o nome dela, então tabela e
  base não têm mais como divergir.
- **Uma parte passou a pertencer a DOIS agregados.** Com o desvio medido em 12 meses, `meta_12m` é
  parte do desvio *e* do juro nominal de equilíbrio. O caminho da caixa já refazia todos os pais; o
  do choque refazia só o cartão clicado, e o outro agregado ficava calado discordando da própria
  parte. Os dois passam por `_simPaisDaParte()` agora.

### A organização do bloco 2: endógenas, gerais, específicas

*"A organização das variáveis endógenas e exógenas será: Endógenas aqueles que possuem equação, e as
exógenas separe em gerais (afetam mais de uma equação) e específicas (afetam somente uma equação)
separadas por equação. Favor, colocar clique-expand."*

Três perguntas, nessa ordem: tem equação? → endógena. Não tem: quantas equações a leem? mais de uma
→ geral; uma só → específica daquela equação. O payload ganhou `consumida_por` por variável e
`eq_nomes` com as cinco equações do modelo.

**A contagem é sobre o MODELO, não sobre o simulador**, e essa é a decisão que faz o mapa valer.
Fosse sobre o que está rodando, toda exógena seria "específica" enquanto houvesse uma equação só, e a
mesma variável trocaria de grupo a cada equação nova — o mapa deixaria de ser um mapa do modelo para
ser um retrato do estado da obra.

**O selo e o grupo passam a poder discordar, de propósito.** O desvio da inflação está entre as
endógenas, porque a (E) o produz; e o selo dele diz *"endógena no modelo · a equação (E) ainda não
está no simulador"*, porque aqui o caminho continua vindo do observado ou do que se digita. Antes o
selo ramificava pelo `tipo` — com `tipo` virando propriedade do modelo, isso passou a prometer uma
equação que não está rodando. Ele ramifica por `produtor_no_sim` agora.

**Gerais está vazio hoje, e o que ele imprime é onde a geral está.** A meta de inflação é lida por
(E) e por (R), mas ela não é cartão: é parte das duas contas. Dizer "nenhuma" seria informação
errada, então a caixa vazia nomeia a meta e diz onde mexer nela. Promovê-la a cartão próprio é a
alternativa, e não foi feita porque ela teria duas superfícies de escrita para o mesmo número
(`SIM.cx` e `SIM.px`), que é a incoerência que este round veio consertar.

O clique-expande é `<details>`, com o estado guardado em `SIM.grupoAberto` — **o `toggle` do
`<details>` não borbulha**, então é um listener por grupo, religado a cada render, e sem o mapa o
grupo que o usuário fechou reabre sozinho no clique seguinte em qualquer controle do bloco. Mesma
armadilha dos cards da aba de dashboards do calendário.

### E clique-expande no gráfico do simulador

*"Coloque clique-expande nos gráficos também."* O cabeçalho de três linhas do cartão vira a linha
clicável, com o mesmo caret dos grupos do bloco 2. Recolhido, some o plot, o resumo e a régua; **o
cabeçalho fica**, para o cartão recolhido continuar dizendo o que é.

**Duas correções no mesmo dia, e as duas valem como regra.** A primeira foi de escopo: a primeira
versão aplicou o recolhimento nos 23 gráficos das sete abas, e o pedido era na aba em que estávamos
trabalhando — *"era para fazer somente na aba do simulador; por que você foi mexer nas outras?"*.
Hoje o seletor é `#tab-sim .chart-card`, e há asserção de que nenhum cartão das outras seis ganhou
caret nem virou clicável.

A segunda foi de afordância, e é a mais transferível: a primeira versão pôs um botão de 22 px no
canto do cartão, ao lado dos `i` e do "Dados no gráfico" — funcionava, e o usuário olhou a tela e
disse *"parece que não mudou nada"*. **Um controle que não se parece com os controles do mesmo tipo
que já existem na página não é lido como um deles.** A aba tinha acabado de ganhar clique-expande
nos grupos, com caret e linha de título clicável; o gráfico precisava do mesmo desenho, não de um
ícone novo. É a regra de reusar o desenho, de novo, agora dentro da mesma página.

Três detalhes de implementação, cada um a origem de um defeito:

- **O caret vem de `::before`, não de um elemento.** `describeChart()` reescreve o `textContent` do
  título a cada render e apagaria qualquer nó posto ali dentro.
- **O estado vive por ID DO PLOT, não no DOM.** Vários cartões são remontados quando um seletor
  troca, e uma classe no elemento morreria com ele.
- **Reabrir chama `Plotly.Plots.resize`.** Dentro de um elemento em `display: none` a caixa mede
  zero e o Plotly guarda a medida da última pintura — sem remedir, o gráfico volta espremido. A
  asserção mede `_fullLayout.width` antes e depois (1451 → 1451).

E `align-items: start` no grid **da aba do simulador**: no default do CSS grid os cartões de uma
linha esticam até a altura do mais alto, então um recolhido ficaria com a altura do vizinho aberto,
só que em branco.

### O rótulo NOMEIA; a descrição descreve

Dois pedidos separados, a mesma correção, e por isso virou regra na skill de dashboards:

| era (descrição) | virou (nome) |
|---|---|
| Inflação esperada menos a meta | **Desvio da inflação** |
| Âncora: juro real de equilíbrio mais a meta | **Juro nominal de equilíbrio** |
| Meta de inflação no horizonte de 18 meses | **Meta de inflação (18m)** |
| sobe até o valor e fica lá | **Choque permanente** |
| entra de uma vez e vai passando | **Choque com decaimento** |
| fica alguns trimestres e depois vai passando | **Choque constante + decaimento** |

Nada foi perdido: cada descrição desceu um nível — a da variável para o texto do cartão, a da forma
de choque para o `title` da `<option>`, onde a frase inteira cabe sem alargar a caixa fechada do
seletor.

Duas coisas que o print pegou e nenhuma asserção pegaria:

- **O campo `desc` não passa pelo renderizador de markdown**; só a `nota` passa. Um `**a âncora**`
  escrito ali sai com os asteriscos na tela.
- **O mesmo objeto tem dois nomes de propósito**, e isso precisa estar dito: no simulador ele é uma
  variável de input e se chama *juro nominal de equilíbrio*; na aba Juros ele é um termo da equação
  e se chama *a âncora*. A ponte está no texto do cartão. Renomear a aba Juros junto seria trocar a
  notação de uma derivação inteira para alinhar um rótulo.


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


## Sexto round: a segunda equação entrou · *2026-09-24*

> *"Em seguida, rode os sistema com as duas equações: Taylor e Câmbio"*

O simulador passou a rodar **(R) regra de juros → (F) câmbio**, nessa ordem, que é a ordem de
solução dentro do trimestre. Não há realimentação — a regra de juros não lê o câmbio —, então a
recursão fecha sem ponto fixo.

### A (F) foi reestimada por MCMC, e essa foi a escolha do usuário

A (F) é Ridge, e Ridge é estimativa pontual: **não tem posterior para virar faixa**. Com a (R)
desenhando uma faixa de 90% ao lado, entrar com a linha pelada da (F) deixaria a tela com duas
equações afirmando coisas de tipos diferentes sem nada que explicasse a diferença. Perguntado, o
usuário escolheu reestimar. `bayes/fx_bayes.py` é o resultado.

**Ele não remonta a matriz**: chama a mesma `fx.montar()` e corta na mesma `fx.corte()`. Só o
estimador muda, e isso é verificável — `conferir()` mede a distância entre a mediana do posterior e
o beta do Ridge em desvios do próprio posterior:

```
parametro      mediana   desvio        HDI 90%      priori  encolh.   Ridge
alpha           -0,028    0,466  [ -0,81,  +0,72]     5,00     0,09  -0,035
phi             -0,086    0,056  [ -0,18,  +0,01]     0,50     0,11  -0,087
b_fiscal       +27,121    3,390  [+21,63, +32,68]    42,48     0,08 +27,033
b_dxy_em        +2,335    0,675  [ +1,25,  +3,46]     8,13     0,08  +2,354
b_carry_vol     -0,570    0,548  [ -1,46,  +0,34]     9,62     0,06  -0,576
b_sp500         +1,883    0,577  [ +0,95,  +2,85]     8,21     0,07  +1,898
b_icbr_usd      -2,050    0,475  [ -2,82,  -1,26]     7,47     0,06  -2,054
        pior distância: 0,028 desvio do posterior · R-hat 1,0000 · 0 divergências
        R² sobre `de` 0,8115 contra 0,8115 do Ridge · RMSE 3,591 contra 3,591
```

Três coisas que essa tabela carrega e valem para qualquer reestimação bayesiana de um modelo já
ajustado por outro estimador:

- **A priori é AUTOESCALADA, e ela precisava ser.** Os betas vivem em escalas muito diferentes
  mesmo depois da padronização, porque o `sd` que escala cada canal vem da janela de referência
  (2000 em diante) e o CDS tem 2002 lá dentro: o beta dele é +27 contra +1,9 da bolsa. Uma priori
  única — `N(0, 5)` para todos — não seria neutra: seria frouxa para a bolsa e apertaria o canal
  fiscal em mais de cinco desvios. Cada canal recebe `N(0, sd(y)/sd(z_c))`, medido na amostra: *este
  canal sozinho poderia explicar toda a variância do câmbio, e não muito mais que isso.*
- **"A priori não está mandando" se mede, não se afirma.** A coluna `encolh.` é o desvio do
  posterior sobre o da priori: 0,06 a 0,11 quer dizer que o dado estreitou o parâmetro dez vezes. E
  a variante `larga`, com todas as prioris multiplicadas por 4, devolve os mesmos números com
  `encolh.` de 0,01 a 0,02.
- **Dois R² e eles não são o mesmo número.** Esta regressão explica `de − dppp`, porque o offset de
  PPP é imposto em 1 e entra do lado esquerdo; o Ridge publica o R² sobre `de`. Os dois lados a lado
  sem dizer qual é qual dariam 0,8024 contra 0,8115 e leriam como discordância. Somando o offset de
  volta, os dois batem em **0,8115 exatamente** — que é a prova de que é a mesma equação.

### O elo entre as duas é UM canal, e ele é o mais fraco da (F)

A Selic chega ao câmbio por `carry_vol = (Selic − Fed Funds) ÷ volatilidade`, e só por aí. Medido
no cenário que a aba abre:

| experimento | efeito no nível do câmbio |
|---|---|
| Selic +2 p.p. nos 12 trimestres | **−0,39%** (R$ 5,603 contra 5,625) |
| Selic +2 p.p. só no 1º trimestre, voltando depois | **0,00%** no acumulado; −0,42 p.p. naquele trimestre |
| coeficiente do canal | mediana −0,58, faixa de 90% [−1,45; +0,34], 85% da massa abaixo de zero |

**O segundo experimento é a parte contraintuitiva e é propriedade da especificação, não defeito.**
O canal entra em DIFERENÇA, então um juro que sobe e depois volta soma zero — o efeito aparece no
trimestre em que o carry muda e é desfeito quando ele volta. Um leitor que espere "juro alto
segurando o câmbio por três anos" lê o gráfico errado, então isso está escrito na ficha da equação
e afirmado no teste, nas duas metades (move o trimestre em que acontece, não move o acumulado).

E o elo é fraco de propósito declarado: o `carry_vol` é o canal menos decisivo da (F). **A tela diz
o número em vez de sugerir um acoplamento que os dados não sustentam.**

### A convenção de trimestralização virou pendência COM consumidor

A (F) foi estimada com a Selic pelo **fechamento** do trimestre; a (R) produz a **média**. Um
simulador que ligue as duas tem de usar uma no lugar da outra. Medido, 2006T2–2026T2:

- média e fechamento diferem **0,384 p.p.** em média e **1,565 p.p.** no pior trimestre (2021T4, no
  meio do ciclo de alta);
- na **variação** do canal, que é o que o coeficiente multiplica: 0,0217 em média, 0,0701 no máximo;
- em câmbio: **0,049 p.p. em média e 0,16 p.p. no pior trimestre**, contra um RMSE de 3,59 p.p. por
  trimestre da própria equação.

A escolha é a média, e ela é usada **inclusive na âncora do trimestre anterior**. Ancorar no
fechamento e projetar com a média pareceria mais fiel à estimação e poria um degrau de convenção
exatamente no primeiro trimestre projetado — o único que ninguém tem como conferir. É F2 ganhando
um consumidor e um número.

O Fed Funds não foi buscado de novo: sai por identidade do que já estava carregado,
`ffr = selic_fim − carry`. Reconstruído assim, `(selic_fim − ffr) ÷ vol` devolve o `carry_vol` da
estimação com erro máximo de **0,000000** — que é o que prova que a identidade fecha e que o resto
da diferença é só convenção de Selic.

### O `carry_vol` NÃO virou cartão, e as três peças dele viraram

Pela regra do próprio painel — *a caixa mostra o número que aquele trimestre vai usar* —, um cartão
de `carry_vol` deixaria digitar um valor que contradiz a Selic da rodada. Ele é **conta, não
premissa**. Quem ganhou cartão foram as peças que o leitor de fato escolhe: o **Fed Funds**, a
**volatilidade do real**, e a Selic, que já tinha o seu. Os sete cartões novos da (F):

```
ppp        Diferencial de inflação BR−US   p.p./tri   composta de infl_br e infl_us
fiscal     Risco fiscal (CDS de 5 anos)    bps        nível; a equação lê a variação
dxy_em     Dólar contra emergentes         pontos     idem
sp500      Bolsa americana (S&P 500)       pontos     idem, em log-retorno
icbr_usd   Commodities em dólar (IC-Br)    pontos     idem, em log-retorno
ffr        Juro dos Fed Funds              % a.a.     entra pelo carry
vol        Volatilidade do real            % a.a.     denominador do carry
```

**A volatilidade tem um trimestre a mais que a grade, e isso é conteúdo.** Ela é medida com um
trimestre de defasagem — de propósito, para o denominador já ser conhecido no início do trimestre
que a equação explica —, então a do **primeiro trimestre projetado já terminou de ser medida**. A
série dela vai um índice além de `D.sim.rot`, e a caixa nasce travada e verde pela mesma regra que
vale para o resto. Isso custou um defeito: `_simRotUltimo` lia `D.sim.rot[i]` e imprimia
`Hoje em 10,63 % ao ano (undefined)`. O indexador que sabe contar trimestres além da grade já
existia (`_simRotIdx`); faltava usá-lo ali.

### Três defeitos que só o print pegou

- **`.toLowerCase()` come a sigla.** A ficha imprimia *"Consome risco fiscal (cds de 5 anos), bolsa
  americana (s&p 500), commodities em dólar (ic-br)"* e *"explica a selic"*. É a terceira vez que
  este defeito aparece nesta página — a primeira foi *"Voltar a o que foi observado"* —, e a
  correção é sempre a mesma: **o rótulo e o nome-dentro-da-frase são dois campos, não um com
  transformação**. Cada variável ganhou `nome_frase` no payload.
- **A mesma nota, quatro vezes seguidas.** Os quatro canais de índice recebiam palavra por palavra
  *"A equação não lê o nível: ela lê a variação…"*. A regra é a mesma nos quatro e é verdadeira, e
  quatro parágrafos idênticos em sequência não se leem — o olho pula o segundo. Cada cartão passou
  a dizer a consequência **dele**: *"Um CDS parado em 300 pontos não desvaloriza nada — o que
  desvaloriza é ele ir de 120 para 300."*
- **Prosa afirmando número, quarta ocorrência.** A ficha da (F) dizia *"2 p.p. de Selic a mais movem
  o câmbio 0,4%"* escrito à mão. Agora o número é medido a cada render, no cenário que está na tela
  — então ele muda quando as premissas mudam, em vez de contradizê-las.

### As duas pontas da mesma recursão, afirmadas

`simulator._sim_fx` (Python) e `_simCaminhoDe` (JS) são a mesma conta escrita duas vezes. **Duas
implementações divergem em silêncio**: um `sd` trocado, um log esquecido, um sinal invertido
continuam produzindo um caminho plausível. O payload passou a levar `eq.ajuste` — o ajuste de **um
passo**, trimestre a trimestre, calculado em Python com os pesos da mediana — e o teste exige que o
JS devolva os mesmos números, rodando `h = 1` a partir de cada trimestre.

**Um passo, e não o caminho solto**, porque ali todas as defasagens vêm do observado: a comparação
é exata em vez de aproximada. Medido: 81 trimestres, pior diferença **1,56e-6 p.p.** — que é o
arredondamento do payload a seis casas, e não resíduo de conta. E o ajuste tem RMSE 3,585, na ordem
do estimado, o que impede a asserção de passar comparando duas contas erradas iguais.

O mutante que fecha isso: apagar a divisão `dz / eq.sd[c]` no JS. **Nenhuma asserção de
comportamento o pega**, porque na janela padrão todos os canais exógenos estão parados no último
valor e a variação deles é zero — o defeito só aparece dentro da amostra. Com a asserção de
paridade ele sai com 5,96e+3 p.p. de diferença.

### E a corrida solta, com as duas

```
corrida solta de 2006T3, 12 trimestres, tudo no observado:
  (R) Selic            erro médio abs. 1,345 p.p.   RMSE 1,478
  (F) var. do câmbio   erro médio abs. 2,941 p.p.   RMSE 3,645
  nível ao fim de 12 trimestres: 2,177 simulado contra 1,952 observado
```

A (F) solta custa quase nada sobre o ajuste (3,645 contra 3,591), e a razão é o AR ser quase zero
(−0,086): ela quase não se realimenta, então soltá-la não compõe erro. É o oposto da (R), cuja
corrida solta custa um fator de 3,5 — lá a persistência é 0,85.


### O cartão do câmbio fala em NÍVEL, e a equação em variação

> *"Embora o que entre no modelo seja a variação do câmbio, conseguimos trabalhar com ela no
> simulador (nos boxes) em nível?"*

Sim, e é melhor assim: a conversão é uma **bijeção exata** ancorada no último fechamento observado
(`de = 100·ln(Pₜ/Pₜ₋₁)`), e até aqui o cartão e o gráfico falavam unidades diferentes da mesma
coisa — o gráfico já desenhava reais por dólar. Agora as caixas mostram `5,233 … 5,625`, os mesmos
números da linha logo acima.

Quatro coisas que a troca de unidade obrigou, e que valem para qualquer caixa que mude de unidade:

- **O que a caixa deixou de imprimir tem de continuar alcançável.** A variação implícita de cada
  trimestre foi para o `title` da própria caixa (`+0,64% no trimestre`), tirada do caminho **já
  resolvido** daquela rodada — e não recalculada ali, que é o que impede o rótulo de discordar da
  linha desenhada.
- **"Observado" muda de significado, para melhor.** Segurar o último **nível** quer dizer câmbio
  parado depois do último dado; segurar a última **variação** faria o nível derivar para sempre na
  taxa do último trimestre. O segundo não é "a ausência de projeção", é uma projeção — e era o que
  estava lá.
- **Um choque em nível e um choque em variação são cenários diferentes**, e o cartão diz qual é
  qual: um choque que sobe e depois volta devolve o câmbio ao ponto de partida em nível, e
  deslocaria o nível para sempre em variação.
- **O valor padrão do choque tem de escalar com a unidade.** Um `v: 1` fixo servia enquanto todo
  cartão estava em pontos percentuais; num cartão em reais ele virou +1 real, 19% de uma vez. Passou
  a ser `4 × passo`, o que de quebra conserta o CDS (que nascia com +1 ponto-base) e o S&P (+1 ponto
  de índice).

### E de onde vem a projeção, com todas as premissas paradas

> *"De onde vem o valor positivo do câmbio?"* · *"As variáveis do modelo estão todas paradas"*

As duas perguntas têm a mesma resposta, e ela precisava estar na tela. Decomposto no cenário que a
aba abre:

```
tri       ppp    alpha      AR    carry   fiscal  dxy_em   sp500    icbr      de
2026T3  +0,283   -0,028  +0,071  +0,317   +0,000  +0,000  +0,000  -0,000  +0,643
  …
soma    +3,396   -0,336  -0,205  +0,597   +0,000  +0,000  +0,000  +0,000  +3,451
```

**98% da desvalorização projetada é o diferencial de inflação**, com peso **imposto em 1**. O resto
quase se cancela, e os quatro canais de mercado somam **exatamente zero**. (A tabela acima já traz
a premissa corrigida da seção seguinte; com a leitura isolada de 2026T2 no lugar da média, o `ppp`
somava +8,634 e o acumulado ia a +8,308.)

O zero não é arredondamento e é a lição: **a equação lê a *variação* de cada canal, então um canal
parado contribui zero**. A assimetria que faz a projeção não ser plana é que `ppp` está em **taxa** e
os outros quatro em **nível** — taxa parada é força permanente, nível parado é força nenhuma. E o
carry se mexe porque a Selic se mexe, que é o elo com a (R).

Isso virou frase derivada na ficha da (F), com o número recalculado a cada rodada, mais a contagem
de canais parados e o convite (*"mexa num deles no bloco 2 e ele passa a aparecer aqui"*). A
decomposição sai da **mesma recursão** — um acumulador opcional em `_simCaminhoDe` —, e não de uma
segunda função: o teste exige que as partes somem exatamente o caminho, o que uma segunda
implementação deixaria de garantir no dia em que uma das duas mudasse.

#### E a premissa que carrega tudo era a leitura de UM trimestre

Consequência da anterior, e ela é uma **pendência de especificação, não um conserto feito**. O
`ppp` segurado é o último trimestre publicado, e um trimestre de inflação relativa é barulhento — o
desvio-padrão trimestre a trimestre é **0,94 p.p.**, maior que a própria média:

| premissa segurada | p.p./tri | ao ano | câmbio em 12 tri |
|---|---|---|---|
| último trimestre (2026T2) | +0,7195 | +2,91% | 5,643 (**+9,02%**) |
| média dos últimos 4 tri | +0,2830 | +1,14% | 5,355 (**+3,45%**) |
| média dos últimos 8 tri | +0,4625 | +1,86% | 5,472 (+5,71%) |
| média da amostra inteira (82 tri) | +0,7154 | +2,89% | — |

**5,6 pontos percentuais de câmbio em três anos separam as duas primeiras linhas**, e a escolha
entre elas é uma premissa, não um resultado. O último trimestre calha de sentar praticamente em
cima da média histórica (0,7195 contra 0,7154), o que é tranquilizador e é coincidência: os oito
trimestres anteriores vão de −0,24 a +1,34.

**O usuário escolheu a média de quatro trimestres**, no mesmo dia (*"pode colocar a média dos
últimos 4 trimestres"*). O que importa do desenho é que ela **não virou regra do painel**: a regra
da casa continua sendo *segure o último valor*, que é a leitura certa em NÍVEL — o CDS de hoje é a
melhor estimativa do CDS de amanhã. A exceção é **declarada por variável**, num campo `segura` do
payload, e vale só para as três taxas de fluxo que existem aqui: `ppp` e as duas metades dela.

Quatro coisas que a exceção exigiu:

- **A média só vale DEPOIS do último dado.** Um buraco no meio da série continua segurando o último
  valor conhecido — ali o que falta é uma observação, não o futuro.
- **O que a caixa dourada DIZ tem de acompanhar a regra.** "É o último valor conhecido, repetido" e
  "é a média dos últimos 4 trimestres publicados" são afirmações diferentes, e a mesma frase nas
  duas mentiria numa. O `title` passou a sair de `_simTitSeg(segura)`.
- **Abrir em partes tem de fechar.** `média(infl_br) − média(infl_us)` é a média de `ppp` porque a
  média é linear; o teste afirma isso, com tolerância de 1e-5 — que é o arredondamento a seis casas
  de três séries gravadas separadamente, e não folga escolhida.
- **E o guarda que importa é o negativo:** *nenhum* cartão de nível declara `segura`. Um `segura`
  que vazasse para o CDS projetaria a média de quatro trimestres de um nível — plausível, errado, e
  sem sintoma nenhum na tela.

Efeito medido na tela: a projeção caiu de **+9,02% para +3,51%** em três anos (R$ 5,358 contra
5,643), e a ficha da (F) imprime a premissa com os dois números — *"segurado na média dos últimos 4
trimestres (0,28 p.p. por trimestre; a última leitura isolada foi 0,72, e um trimestre sozinho é
ruído)"*. Escrever isso custou uma correção de regência que já é a terceira desta página: a função
devolve o **complemento regido pronto** (`na média…`), e não um sintagma para quem chama prefixar
com `em` — senão sai *"segurado em a média"*.


## Sétimo round: a terceira equação, e o fim das premissas compostas · *2026-09-25*

> *"(i) Vamos introduzir a equação de expectativas; (ii) quero fazer uma mudança na
> organização das premissas: Vamos separar as premissas em Endógenas e Exógenas. Para as
> exógenas vamos separar todas aquelas que precisam de partes, não haverá mais premissas
> com subpremissas. (…) As exógenas vamos separar somente em Doméstica e Externa. Nesse
> caso, por exemplo, a Fed Funds é externa, Volatilidade do câmbio é doméstica."*

Os dois pedidos vieram juntos e **um obriga o outro**. Com a (E) entrando, a expectativa
passa a ser produzida — e o cartão `di` (*desvio da inflação esperada*) deixaria digitar
um desvio que contradiz a expectativa da própria rodada. Era a mesma regra que já
impedia o `carry_vol` de ter cartão: *ele é conta, não premissa*. O corte das
subpremissas é o que torna a (E) instalável sem incoerência.

Ordem de solução agora: **(E) expectativas → (R) regra de juros → (F) câmbio**. Continua
sem ponto fixo — a (E) lê a inflação do trimestre, que é premissa, porque a curva de
Phillips ainda não está aqui. É uma **corrente de três elos**, não um laço.

### A (E) por MCMC, e o que a priori não precisou ser

`bayes/expectations_bayes.py`, mesmo desenho dos outros dois: chama a mesma
`expectations.montar()`, impõe a restrição pela mesma reparametrização, e só o estimador
muda.

```
parametro      mediana   desvio        HDI 90%      priori  encolh.      MQ
e1              +0,581    0,079  [ +0,452, +0,710]    1,00     0,08   +0,586
e2              +0,162    0,033  [ +0,109, +0,216]    1,00     0,03   +0,160
sigma           +0,580    0,043  [ +0,513, +0,654]  HN 2,0        -
peso_meta *     +0,257    0,054  [ +0,169, +0,347] derivado        -   +0,254
repasse_lp *    +0,387    0,045  [ +0,317, +0,461] derivado        -   +0,387
meia_vida *     +2,000    0,451  [ +1,000, +2,000] derivado        -   +2,000
        pior distância: 0,061 desvio do posterior · R-hat 1,0000 · 0 divergências
        R² sobre a expectativa 0,7778 contra 0,7778 do MQ · RMSE 0,5692 contra 0,5692
```

Três coisas que diferem da (F) e valem registrar:

- **A priori aqui é UMA só, e isso é uma conclusão e não uma economia.** Na (F) ela
  precisava ser autoescalada porque os betas viviam em escalas muito diferentes; aqui os
  dois regressores estão na mesma unidade (p.p. de desvio contra a meta) e os dois
  coeficientes são **pesos**, cujo intervalo útil é [0, 1]. `N(0, 1)` cobre isso várias
  vezes. A variante `larga` (×4) devolve os mesmos números.
- **A priori do BC NÃO entra, e a razão é o objeto e não a data.** O `f2` da eq. (5)
  multiplica a previsão do próprio modelo quatro trimestres à frente; o nosso `e2`
  multiplica a inflação realizada. São regressores diferentes — transplantar o número
  seria pôr a priori no lugar errado.
- **Os pesos não são restritos ao simplex, e que eles caiam nele é MEDIÇÃO.** Nada na
  priori proíbe `e1 < 0` ou `e1 + e2 > 1`; manter assim é o que faz esta estimação ser o
  espelho exato do MQ. Medido: **0,00% da massa do posterior fora do simplex**.

**E a restrição vale desenho a desenho, não só na mediana.** `repouso_draws()` afirma
sobre a amostra inteira que, com a inflação na meta, a conta devolve a meta — pior
desvio **1,78e-15**. Num simulador isso importa mais que na estimação: é cada desenho
que roda, e um deles convergindo para um número que não é a meta produziria uma faixa
assimétrica sem causa.

#### O peso da meta é refeito, e NÃO lido do desenho gravado

O `peso_meta` está gravado no arquivo de desenhos, e usá-lo na recursão pareceria
equivalente. **Não é**, e a diferença só aparece no conjunto de pesos que a tela usa por
padrão: a **mediana não é linear**, então `mediana(peso_meta)` não é
`1 − mediana(e1) − mediana(e2)`, e a equação deixaria de devolver a meta em repouso por
alguns milésimos. A recursão refaz a subtração nas duas pontas.

**Nenhuma asserção de comportamento pega isso** — o mutante que lê o desenho gravado
passa em tudo, inclusive no repouso por desenho (ali os dois coincidem). Quem o pega é o
gabarito de um passo, com 1,88e-3 p.p. de diferença.

### Não há mais premissa com subpremissa

Três cartões eram contas de outros dois, com as peças atrás de "abrir em partes".
O que era peça virou cartão e **a conta mudou de dono**: quem a declara agora é a
equação que a consome, no campo `deriva` do payload.

| conta | de quem é | peças (agora cartões) |
|---|---|---|
| desvio da inflação esperada | (R) | `pi_e` − `meta_12m` |
| juro nominal de equilíbrio | (R) | `rr_10a` + `meta_12m` |
| diferencial de inflação BR−US | (F) | `infl_br` − `infl_us` |
| IPCA acumulado em 12 meses | (E) | 4 trimestres de `infl_br`, compostos |
| carry sobre a volatilidade | (F) | já era conta desde 2026-09-24 |

O que saiu junto, porque só existia para alimentar aquilo: `D.sim.prim` inteiro,
`SIM.px`, `SIM.aberto`, `simPrim`, `simAgregarDePartes`, `_simPaisDaParte`, o parâmetro
`pai` do choque, e quatro regras de CSS.

**Os cartões passaram de 11 para 13** e cada um é uma série própria — o que simplificou
`simObs`, `_simSegura` e `_simCobertura`, que ramificavam entre variável e primitiva.

#### O IPCA aparece em duas formas, e ISSO tinha de ser resolvido antes

A (E) lê o IPCA acumulado em **12 meses**; a (F) lê a variação **do trimestre**. Dois
cartões digitáveis da mesma série seriam duas premissas livres para se contradizer sem
nada avisar. Medido antes de decidir: compor quatro trimestres de `infl_br` reproduz o
`ipca_12m` publicado (SGS 13522) com **erro médio de 0,0024 p.p. e máximo de 0,0056** em
99 trimestres — o arredondamento da própria série publicada, que tem duas casas.

São a mesma série. Então há **um cartão** (o trimestral) e o acumulado é conta, com o
gabarito viajando no payload (`i12_pub`) para o teste poder exigir isso a cada geração.
A composição é `100·(exp(Σ/100) − 1)` e não a soma: somar erra **0,658 p.p. contra 0,005**
— duas ordens de grandeza —, e é o mutante que fecha a asserção.

Detalhe que custou uma execução: a inversão para "que inflação trimestral dá exatamente
a meta em 12 meses" é `ln(1 + meta/100)/4`, e **não** `(1 + meta/100)^(1/4) − 1` — o
cartão está em 100·Δlog. As duas diferem 0,004 p.p. por trimestre, que a conta amplifica
para 0,006 p.p. na expectativa de repouso.

#### E a grade precisou de três trimestres para trás

A grade do simulador começa onde a **(R)** consegue ser calculada (2006T1, limitada pelo
juro real de dez anos). A inflação existe muito antes, e o acumulado do *primeiro*
trimestre da grade precisa dos três anteriores. `pre_insumo` carrega exatamente esses
três — mesmo instinto do trimestre a mais da volatilidade, no sentido contrário do
tempo. Sem eles uma corrida solta partindo do começo da grade não teria expectativa.

Pela mesma razão a (E) é a única das três estimada **antes** do começo da grade (2002T1
contra 2006T1), então `est_i0` é recortado e o payload diz que foi
(`est_antes_da_grade`) — um índice negativo pintaria a faixa da amostra no lugar errado.

### Doméstica e externa: o critério é DE QUEM é a variável

O usuário deu dois exemplos ao definir o corte, e eles resolvem o caso ambíguo: a
**volatilidade do real é doméstica** embora seja negociada no mundo inteiro, porque é o
preço de um ativo brasileiro; os **Fed Funds são externos**. Por essa régua o CDS
soberano é doméstico (é risco de crédito do Brasil) e o **IC-Br em dólar é externo** — a
cesta é da pauta de exportação daqui, mas quem forma o preço está fora. O que o Brasil
traz para ele é o peso de cada produto, não o preço.

```
domésticas (5)   infl_br · meta_12m · rr_10a · fiscal · vol
externas   (5)   infl_us · ffr · dxy_em · sp500 · icbr_usd
```

#### E `tipo` passou a ser sobre ESTE simulador

A divisão anterior (*gerais* × *específicas por equação*) contava sobre o **modelo**, de
propósito. A nova não pode: a `infl_br` tem equação no modelo — a curva de Phillips — e
ela não está aqui, então é premissa que se digita. Pô-la no grupo das que **não** se
digitam responderia errado a pergunta que o bloco existe para responder.

Então `tipo == "endogena"` quer dizer *uma equação que roda aqui a produz*, é sempre
igual a `produtor_no_sim`, e `_variaveis` levanta se os dois discordarem. O fato do
modelo continua em `produzida_por`, e é o **selo do cartão** que o imprime — *"endógena
no modelo · a equação (I) ainda não está no simulador"*. O rótulo do grupo foi corrigido
junto (*"uma equação deste simulador as produz"*): era ele que prometia o modelo.

### O que a (E) muda no cenário que a aba abre

```
tri        i12    pi_e    meta   selic   câmbio
2026T3   5,172   3,959   3,000  13,989   5,2103
2027T2   4,641   3,784   3,000  12,807   5,2577
2029T2   4,641   3,636   3,000  11,908   5,3666
```

A expectativa **não** converge para a meta, e isso é o dado falando: com a inflação
trimestral segurada na média de quatro trimestres, o acumulado de doze meses fica em
**4,64%** — acima da meta de 3,0%. O repouso da equação é
`(e2·4,641 + peso·3,0)/(1−e1) = 3,634`, que é onde ela para.

| elo | medido no cenário da aba |
|---|---|
| (I) → (E) | +1 p.p. de inflação por trimestre leva a expectativa **+1,64 p.p.** no fim |
| (E) → (R) | a expectativa da equação contra a segurada: **−0,79 p.p.** de Selic no fim (11,908 contra 12,693) |
| (R) → (F) | o câmbio sobe **+0,15%** por causa disso — juro menor, carry menor |

**A corrida solta melhorou com a (E) dentro**, e vale registrar porque a expectativa
oposta era a minha: encadear mais uma equação costuma compor erro.

```
corrida solta de 2006T3, 12 trimestres, tudo no observado:
  (E) expectativa      erro médio abs. 0,311 p.p.   RMSE 0,376
  (R) Selic            erro médio abs. 1,118 p.p.   RMSE 1,300   (era 1,345 / 1,478)
  (F) var. do câmbio   erro médio abs. 2,934 p.p.   RMSE 3,632
```

A (R) com a expectativa **observada** dá 1,345 / 1,478; com a que a (E) produz, 1,118 /
1,300 — **12% menos de RMSE**. A causa é que a Focus observada carrega o desvio
contemporâneo inteiro, inclusive o que a regra de juros não deveria perseguir, enquanto
a (E) o filtra pela âncora da meta.

### A faixa da (R) passou a carregar duas, e a do câmbio três

O desenho `s` da (R) roda com a expectativa do desenho `s` da (E), como já acontecia
entre (R) e (F). Os posteriores foram estimados separadamente, então parear amostras
independentes é amostrar do produto.

**A comparação que mede isso tem de ser com o MESMO caminho central**, e a primeira
versão da asserção errou nisso. Comparar "(E) ligada" com "(E) imposta" compara duas
coisas ao mesmo tempo, e medido a segunda sai **mais larga** (1,77 contra 1,37): segurar
a Focus no último valor mantém um desvio grande e constante, e é o desvio que a
incerteza de `t3` multiplica. O que isola a propagação é trocar só os desenhos, com o
caminho da mediana fixo dos dois lados — e aí ela alarga, como tem de ser. Trimestre a
trimestre ela não *contém* a outra, e isso é amostragem: com 1000 desenhos de cada lado,
onde a contribuição da (E) ainda é pequena o ruído do quantil inverte a ordem. A
tolerância (0,02 p.p.) é o ruído medido, não um número escolhido.

### Três defeitos que só o print pegou

- **`.toLowerCase()` comeu a sigla, pela QUARTA vez nesta página.** A ficha imprimia
  *"a conta forma ipca acumulado em 12 meses"*. A correção é sempre a mesma e agora está
  no payload das contas derivadas: `nome` rotula, `nome_frase` é o nome como se lê dentro
  de uma frase.
- **A chave do payload apareceu como nome.** *"(infl br)"* — as peças eram impressas com
  `de.join(...).replace(/_/g, ' ')`. Passaram a sair pelo `nome_frase` **delas**.
- **A legenda da faixa dizia "das duas equações" com três propagando.** Era a frase da
  caixa de marcar cortada em 2026-09-24, que virou o nome da faixa — e um número escrito
  à mão ao lado de uma faixa calculada é a quinta ocorrência do mesmo defeito aqui.
  `_simRotFaixa(eq, nEq)` conta.

E um de coerência interna, que o print expôs mas não causou: `simEq()` sem argumento
devolvia a primeira equação da ordem de solução — comodidade que virou armadilha no
minuto em que a (E) passou a ser a primeira. As chamadas sem chave continuaram
compilando e passaram a ler a equação **errada**, em silêncio. `simEq` agora exige a
chave e levanta.

### O gabarito de um passo passou a existir nas TRÊS

A (R) não tinha: o desvio e a âncora chegavam prontos no payload, então não havia conta
a duplicar. Com as duas virando **conta refeita nas duas pontas**, elas passaram a ser
exatamente o tipo de coisa que diverge em silêncio — e o guarda foi junto com a mudança
que criou o risco, não depois.

| equação | trimestres comparados | pior diferença | RMSE do ajuste |
|---|---|---|---|
| (E) | 81 | 7,41e-7 p.p. | 0,336 |
| (R) | 80 | 1,58e-6 p.p. | 0,537 |
| (F) | 81 | 1,98e-6 p.p. | 3,585 |

A diferença não é zero e nem deveria ser: é o **arredondamento do payload** a seis casas.
Vale saber disso antes de escrever a tolerância, senão ela nasce apertada demais.

E o RMSE do gabarito da (E) — 0,336 contra 0,569 da estimação — não é discordância: o
gabarito roda na **grade do simulador**, que começa em 2006T1, e a estimação começa em
2002T1. A desancoragem de 2002 está fora dali, e é onde mora o maior resíduo da equação
(+3,63 p.p. em 2002T4). O que a asserção exige é que o erro esteja *na ordem* do
estimado, justamente porque as duas janelas não são a mesma.

Mutantes verificados: a composição virando soma (5 falhas), o peso da meta saindo do
desenho gravado (**1 falha, só a paridade**), e a (R) voltando a ler a expectativa
carregada em vez da produzida (2 falhas no node, 2 em Chrome).


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

## Oitavo round: o denominador do carry vira preço · *2026-09-25*

O usuário baixou a série de volatilidade implícita das opções de dólar e a discussão que veio
com ela mudou a equação (F). O pedido, na íntegra: *"o carry procura capturar o diferencial de
juros entre duas moedas, e o retorno que ele terá será o diferencial de juros + a desvalorização
da moeda de carry. Portanto, quando a perspectiva de elevação da volatilidade (risco de perder
dinheiro) sobe, o benefício do carry se esvai. Nesse sentido, assim como no CDS, o que importa é
a precificação do momento não do período anterior. Portanto, a especificação deve ser
(diferencial de juros)/vol_implicita_n_meses — ambos em T."*

Ele estava certo, e a lição é de método antes de ser de câmbio.

### Uma correção herdada vira inconsistência quando a fonte muda de natureza

A vol realizada de 126 pregões terminando em *t* entrava **defasada um trimestre**, e a razão
estava escrita: a janela contém inteiro o trimestre que se quer explicar. Mas ela é mais forte do
que "endogeneidade" — a vol realizada de *t* **é** a dependente por construção, o desvio-padrão
exatamente dos retornos diários cuja soma é o `de(t)`. Defasar era o único conserto possível.

A vol implícita no fechamento de *t* é outro objeto: é um **preço**, da mesma classe do CDS, do
dólar EM, do S&P e do IC-Br — e os quatro já entravam contemporâneos. A (F) nunca foi preditiva;
ela é uma decomposição do movimento **do** trimestre. Exigir predeterminação só deste denominador
era uma inconsistência dentro da própria especificação, herdada de um conserto cuja razão não
transferia.

**E o dado separa as duas leituras.** Mesmos 81 trimestres, tudo o mais segurado:

| denominador | β(dp) | t(HAC) | R² | RMSE | λ | MSE walk-forward |
|---|---|---|---|---|---|---|
| realizada 6m defasada (até aqui) | −0,576 | −1,35 | 0,8115 | 3,59 | piso | 17,34 |
| implícita 3M **no fechamento de t−1** | +0,413 | 0,68 | 0,8099 | 3,61 | 0,0261 | 19,04 |
| **implícita 3M no trimestre** | **−1,364** | **−2,78** | **0,8261** | **3,45** | piso | **16,15** |

A linha do meio é a que fecha o argumento: uma vol implícita *predeterminada* é prospectiva e
mesmo assim não informa nada — e ainda tira o λ do piso da grade, o que derruba a coluna de `t`
junto. **Ser prospectiva não torna uma série exógena**; o que a torna informativa aqui é ser o
preço do risco no mesmo trimestre.

Por MCMC, que é o que o simulador roda: mediana −1,363, HDI 90% **[−2,207; −0,528]**, que não
cruza zero (a especificação anterior dava −0,570 com [−1,461; +0,338], que cruzava). A priori
larga (×4) move a mediana em 0,002. R-hat 1,0000, zero divergências, pior distância ao Ridge 0,06
desvio do posterior.

**O prazo:** na convenção contemporânea *todos* passam — 1M −1,150 (t −2,14), 2M −1,279 (−2,53),
**3M −1,364 (−2,78)**, 6M −1,230 (−2,51), 9M −1,565 (−2,62), 1Y −1,278 (−2,78). Na predeterminada
nenhum passava. Escolhido o 3M, que casa com o trimestre; o 1Y empata no ajuste (R² 0,8262).

### O que mais mudou de número, e um que não é ganho

O ganho **não é aditivo**: fiscal +27,03 → +25,04 e IC-Br −2,05 → −1,72, porque os três canais
precificam o mesmo risk-off. O elo (R)→(F) do simulador ficou 3,5× maior — 2 p.p. de Selic em
todos os 12 trimestres levam o câmbio a **−1,37%** contra 0,39% antes, e a massa do posterior
abaixo de zero foi de 85% para **99,7%**.

E o que piorou, dito porque medido: a corrida solta de 12 trimestres a partir de 2006T3 foi de
MAE 2,934 / RMSE 3,632 para **3,151 / 3,728**. Ajuste dentro da amostra melhorou e aquela janela
específica piorou; é uma janela só, não uma contradição.

### O trimestre a mais tinha de sumir junto

Consequência que não estava no pedido e é a parte que custa acertar. Com a vol defasada, a série
do cartão ia **um trimestre além da grade** — a vol do primeiro trimestre projetado já estava
medida, e a caixa nascia travada e verde. Com a implícita contemporânea isso deixa de ser
verdade: a cotação de um trimestre que ainda não aconteceu não existe. O `am_mais1` saiu, e a
caixa virou premissa dourada como as outras quatro da (F).

As duas asserções que afirmavam a exceção (*"a única com trimestre já publicado é a
volatilidade"*) foram invertidas e ficaram mais fortes: **nenhuma** premissa tem trimestre
publicado adiante da grade, e a série da vol termina no mesmo trimestre que a do risco fiscal.
Um trimestre a mais ali seria um número que ninguém observou, impresso em verde e travado.

O cartão também trocou de nome e de texto — *Volatilidade do real* virou **Volatilidade implícita
do dólar**, e a nota explica o porquê do denominador em vez de explicar a defasagem que não
existe mais. Um recorte novo obriga a reler o rótulo do recorte velho.

### O que ficou decidido junto

- **A série está na equação; a tabela não existe.** Ela viaja em
  `data/vol_implicita_usdbrl_3m.csv`, extraída da automação Bloomberg do fundo, parando em
  2026-08-04. O usuário adiou o ETL de propósito (*"criamos a tabela depois"*) — está registrado
  em **F4** e em `PENDENCIAS.md`, porque insumo fora do banco é dívida, não recurso.
- **As abas por equação continuam publicando a estimativa pontual**, e isso é decisão e não
  atraso: o usuário declarou que o produto final é a aba do modelo agregado e que *"as abas
  individuais servirão para investigação, aprofundamento, acompanhamento"*. O simulador já roda
  as três equações por MCMC; a vitrine das abas segue como está.
- **`comparar()` ganhou a forma `vol_realizada`**, para a especificação anterior continuar
  medível em vez de virar história.

---

## Nono round: a quarta equação, e o aperto medido contra a mesma âncora · *2026-09-25*

Dois pedidos em sequência. O primeiro: *"Quero rodar a equação do hiato substituindo o gap com a
inclinação pelo gap com a Selic − (real NTN-B + meta, como na nossa equação de Selic). Quero ver o
que acontece."* Medido e mostrado, o segundo: *"Pode rodar e colocar no simulador."*

### A oposição que a docstring fazia não existia

A (H) usava a inclinação real 2a−10a e a docstring a opunha a "um juro contra um neutro". A álgebra
dissolve a oposição:

    inclinação = rr_2a          − rr_10a
    gap        = (Selic − meta) − rr_10a

**O neutro é o mesmo nos dois.** O que muda é a perna da política — o juro real de 2 anos que o
mercado precifica, ou a Selic descontada da meta —, e as duas pernas correlacionam +0,875. As duas
medidas do aperto correlacionam +0,767, e no mesmo ajuste nenhuma sobrevive (t −0,99 e −1,23).

| aperto, 81 trimestres | h2 | t | **h2 × desvio** | R² | RMSE | LB(4) |
|---|---|---|---|---|---|---|
| inclinação (até aqui) | −0,164 | −2,62 | −0,167 | 0,8678 | 0,642 | **0,021** |
| **Selic contra a âncora** | **−0,071** | **−2,12** | **−0,185** | **0,8703** | **0,636** | **0,070** |

**Os `h2` não se comparam** — o gap oscila 2,60 e a inclinação 1,02 —, e por desvio da própria
medida os dois quase coincidem. A tabela de candidatas da aba ganhou a coluna *peso por desvio da
medida* por isso, e a nota ao lado cita os dois números, derivados. Em troca o gap tira o resíduo da
reprovação de Ljung-Box, e o efeito de um ponto passa a ser comparável com o do BC (antes a linha
dizia "não — é outro objeto"): **−0,071 contra −0,110, dentro da margem publicada** (−0,165 a
−0,053), com o peso do BC convertido de `b2` sobre um quarto do juro para o efeito por ponto.

**A ressalva, que vai escrita em H10:** as duas se separam por subamostra. Em 2016T3–2026T2 sem a
pandemia a inclinação dá −0,105 (t −2,94) e o gap −0,006 (t −0,44); a significância do gap vem de
2006–2016.

**O que decidiu foi estrutura, não ajuste.** A inclinação é feita de dois preços de mercado, então
uma (H) escrita com ela seria espectadora dentro do simulador — a Selic da (R) nunca chegaria ao
produto. Com o gap, `(R) → (H)` é elo.

### A (H) no simulador

`eq_ordem` passou a `E → R → H → F`. A (H) lê a Selic da (R) **com um trimestre de atraso**, então
vem depois dela sem ponto fixo; a (H) e a (F) não se leem, e a (H) vem antes porque é ela que a curva
de Phillips vai ler quando entrar — aí a ordem vira a do plano, `H → I → E → R → F`. Por MCMC
(`bayes/is_bayes.py`), `h2` mediana −0,0709 com HDI [−0,121; −0,023] e 99,1% da massa abaixo de zero.

O aperto é **conta, não cartão** — `deriva.gap` com a operação nova `lin` (combinação linear com os
pesos declarados, `[1, −1, −1]` sobre Selic, juro real de 10 anos e meta), porque os `-`/`+` das
outras equações têm duas peças e esta tem três. O aperto das defasagens **anteriores** à janela sai
do observado dos cartões pela mesma conta (`_deriv_obs_em` / `_simDerivObsEm`), e não de uma cópia
gravada. O cartão novo é **Hiato do produto**, endógeno, lido pela (H) e pela (I) — que não está aqui,
então ninguém no simulador o consome ainda. Os cartões da Selic, do juro real e da meta ganharam o
leitor novo, e **três frases que afirmavam "a única" deixaram de ser verdade** — a meta "é a única
variável que DUAS equações leem" (agora três), a inflação "é a única premissa que duas equações
leem" (o juro real também é, agora). Saíram, em vez de serem recontadas.

No cenário que a aba abre: hiato de partida +0,36 e aperto de 3,88 p.p. (Selic 14,54 contra âncora
10,67). A regra corta a Selic a 11,91 em 12 trimestres, o aperto cai a 1,24 p.p., e o hiato vai a
**−0,72** e para ali — que é `h2/(1−h1) × 1,24`, o repouso de um aperto que sobra porque a
expectativa repousa acima da meta. Com a Selic segurada em 14,54 o hiato iria a **−1,68**: a Selic
da regra vale **+0,96 p.p.** de hiato no fim. E 1 p.p. de Selic a mais em todo o horizonte deixa o
hiato **0,44 p.p. mais baixo**. Na corrida solta de 2006T3, MAE 0,902 / RMSE 1,011 — a janela inclui
2008.

### O que o print pegou

A ficha dizia *"leva o hiato a −0,44 p.p. no fim"*, que se lê como o nível a que ele chega e não o
quanto ele se move; virou *"deixa o hiato 0,44 p.p. mais baixo"*, com a direção por extenso e o
número em módulo — e o mesmo para o elo. E o parágrafo estático do bloco do BC prometia *"a ressalva
que importa marcada na própria linha"*, que era a linha do aperto dizendo "não comparável"; com as
três linhas comparáveis, a frase passou a descrever uma tabela que não existia.

### O gabarito de um passo NÃO alcança o que só entra no segundo passo

Achado dos mutantes, e é a parte que vale além desta equação. Com um regressor defasado, um passo
usa **só a defasagem observada** — então a conta que produz o aperto **dentro** da janela nunca roda
no gabarito. O mutante que soma as três peças ignorando o sinal passa pela paridade inteira e é
pego só pelo teste de repouso de 400 trimestres. Quatro mutantes, os quatro pegos: sinal da `lin`
(repouso), a (H) lendo a Selic observada (o elo), aperto contemporâneo (paridade e o primeiro
trimestre parado), leitura pontual sem a meta (a identidade com o painel).

### O que ficou registrado

**H10** (o gap fraco na década recente, com duas hipóteses a testar), **H6** reescrito (o juro de 10
anos passou a ser o neutro da conta, e carrega 0,9–1,1 p.p. de prêmio), **H9 = R12** literalmente
(as duas equações medem distância até a mesma âncora, então uma neutra estimada troca nas duas), e
**H2** rebaixado (Ljung-Box passa, mas a autocorrelação de um trimestre é 0,30).

---

## Décimo round: a quinta equação, e o modelo vira um laço · *2026-09-28*

Três pedidos em sequência: estimar a (I) por MCMC (*"Estimate via bayesian and report the
results"*), explicar o repasse cambial, e *"Please, you can enter this in the simulator. One
additional point: rename the tab 'Structural Model'"*.

### A (I) por MCMC

`bayes/phillips_bayes.py`, as quatro equações do MQ pela mesma `phillips_sub.matriz()` — separada de
`estimar_uma()` para isso, sem mover número nenhum do MQ. Quatro posteriores independentes, então
os desenhos são **pareados** e o que só existe no sistema é medido desenho a desenho: 1 p.p. de hiato
por um ano soma **0,23 p.p.** ao IPCA de 12 meses; uma depreciação de 1% chega **3,3%** ao nível do
IPCA em um ano e **5,8%** no longo prazo, com a expectativa parada. Detalhe e diagnósticos em
[`bayes/CLAUDE.md`](bayes/CLAUDE.md).

### Por que o simulador deixou de resolver em uma passada

Até aqui era uma corrente, `E → R → H → F`, e cada equação rodava uma vez, lendo o que as
anteriores tinham produzido. A (I) lê o hiato, a expectativa e o câmbio, e o que ela produz volta
para a (E) e para a (F). `resolver()` (e `_simResolver()` no navegador) faz **Gauss-Seidel sobre o
caminho**: cada volta roda as equações ligadas na ordem de solução, cada uma lendo o que já saiu na
volta e, do resto, o da anterior, até nenhum caminho mudar mais que 1e-10. O resultado é o ponto
fixo das cinco — o mesmo de resolver trimestre a trimestre — e **as funções de cada equação ficaram
as mesmas**, que é o que tornou a mudança pequena.

A ordem passou a ser a do plano, `H → I → E → R → F`: a (H) lê a Selic de um trimestre antes, então
dentro do trimestre ela é conhecida primeiro. O único elo contra a ordem é a alimentação lendo o
câmbio do próprio trimestre, com ganho **0,007**; os laços que passam por defasagem têm ganho da
mesma ordem. Medido: **10 voltas** no cenário padrão, 11 na corrida solta, e um render inteiro com as
mil resoluções da faixa leva **349 ms** no Chrome.

A faixa virou uma só: `_simFaixasSistema()` resolve o laço para cada desenho, com o desenho `s` de
cada equação ligada entrando junto. As seis funções de faixa por equação saíram. **A contagem de
equações da legenda sai do grafo de quem lê quem** (`_simNEq`): com as cinco ligadas toda faixa
carrega as cinco; com a Selic imposta o hiato carrega só a (H), e o câmbio quatro.

### Três pontes que a (I) precisou, e o tamanho de cada uma

- **O câmbio médio.** A (I) foi estimada com a variação do câmbio MÉDIO do trimestre (convenção do
  BC, `panel.py`); a (F) produz o de fechamento. A ponte é a média de duas variações de fechamento
  seguidas, `50·ln(P_t/P_{t−2})` — o câmbio andando em linha reta dentro do trimestre. Contra o
  médio de verdade ela correlaciona **0,91** (o fechamento sozinho, 0,64), e o erro de alimentação vai
  de 1,927 a 1,949 p.p.; o de industriais cai de 0,614 para 0,608. Declarada em `deriva.de_med`, com o
  nome na ficha.
- **As commodities em NÍVEL.** O painel só guarda a variação; um cartão de variação seguraria a alta
  do último trimestre por três anos. Dois cartões novos, externos, com o nível médio do IC-Br
  agropecuária e metal em dólar — `simulator._insumos_inflacao` levanta se `100·dlog` do nível não
  devolver a coluna do painel (medido: 3,6e-15).
- **O IPCA do trimestre em duas unidades.** As quatro equações trabalham em variação simples; o
  cartão guarda `100·dlog`, que é o que a (E) compõe e a (F) subtrai. `infl_br = 100·ln(1 + π/100)`
  — medido, 0 de diferença em 99 trimestres.

Os pesos dos grupos são os publicados em cada trimestre da grade e, adiante, os do último trimestre
(2026T2) — os do IBGE andam com os preços relativos, e três anos disso os movem em centésimos.

### O que a (I) muda no cenário que a aba abre

No fim dos 12 trimestres, contra a mesma rodada com a inflação segurada na média dos últimos
quatro: Focus **3,20 contra 3,64**, Selic **11,28 contra 11,91**, hiato **−0,60 contra −0,72**, câmbio
**R$ 5,29 contra 5,38**. O IPCA de 12 meses vai de 4,64 a **3,36**, passando por **5,45** no fim de 2026 —
o 2025T4 de 0,60% (alimentação −0,22%, monitorados −0,17%) sai da janela e o 2026T4 que entra carrega
a sazonalidade do quarto trimestre. Na corrida solta de 2007T1: IPCA do trimestre RMSE 0,396 p.p.,
de 12 meses 1,085.

### O defeito que só a (I) acordou: o `%` do JavaScript

`_simPassoTri(i)` devolve o trimestre do ano da posição `i`, e servia só para rotular trimestres
ALÉM da grade. A (I) a usa dentro da grade, para a dummy sazonal — e `(−77) % 4` em JavaScript é
**−1**: todo trimestre antes do último rótulo virava o "trimestre 0", a sazonal sumia, e o gabarito de
um passo errava 1,45 p.p. em alimentação. O Python (`%` sempre positivo) estava certo. Normalizado
o resto. É a regra do gabarito de um passo pagando o que custou: sem ele a projeção sairia certa
(ela vive além da grade) e o erro só apareceria numa corrida sobre a história.

### Três gabaritos, e o que cada um alcança

- **Um passo por grupo**, feito das COLUNAS do painel (`_ajuste_infl`) — prova a recursão e a
  reconstrução de cada regressor a partir dos cartões. Paridade 5,5e-7 a 8,0e-7.
- **Vários passos contra a forma fechada** (400 trimestres): sem choque cada grupo converge para a
  expectativa; um hiato permanente e uma depreciação única chegam ao cheio na fórmula com o
  multiplicador da indexação dos monitorados. É o que alcança a conta DENTRO da janela, que o
  gabarito de um passo não alcança (lição do nono round).
- **O laço**: `sistema_padrao`, o cenário que a aba abre resolvido no Python. Nenhum gabarito de
  equação alcança a conta que junta as cinco.

### O que ficou para decisão do usuário

A indexação dos monitorados sai negativa também no posterior (−0,21, 29% da massa acima de zero),
e o hiato não entra em alimentação (−0,002) — os dois entram no simulador como estimados, porque
mudar especificação não é decisão de quem implementa. **P3** em
[`pendencias_philips_eq.md`](pendencias_philips_eq.md) já tem o conserto proposto do primeiro. E
4,0% dos desenhos são explosivos (inércia de industriais acima de 1): ficam na faixa.

---

## A aba Impulso-resposta · *2026-09-28*

> *"Escolhemos a variável de choque (que receberá o choque) e como isso impacta cada variável
> endógena. Sendo que as variáveis exógenas também podem ser escolhidas para receber o choque.
> Os choques podem ser modelados como temos na aba 'Structural Model' — o mesmo esquema."* E,
> no meio: *"eu quero poder ver e 'chocar' os subíndices"*.

A resposta é a **diferença** entre duas soluções do laço com os mesmos pesos: o cenário que a
aba Structural Model abre, e o mesmo com o choque. O modelo não é linear em tudo (câmbio em
log, carry em razão, IPCA de 12 meses composto), então ela é medida contra esse cenário e não
tirada de forma fechada. Nove gráficos: hiato, IPCA, Focus, Selic, câmbio (em % do nível) e os
quatro grupos do IPCA, com um seletor do trimestre / 12 meses para os cinco de inflação.

**Onde o choque entra — decisão do usuário, perguntada antes de construir:**

- **Numa endógena, no RESÍDUO da equação dela** (`eps` em `_roda` / `_simRoda`), somado
  antes de o valor virar defasagem — a própria dinâmica o propaga. É o impulso-resposta
  estrutural. A (I) tem quatro resíduos, então os alvos são os quatro grupos; o IPCA responde
  como a soma ponderada deles (asserção exata).
- **Numa exógena, no caminho** que o cenário padrão segura; nos cinco índices (S&P, dólar
  contra emergentes, as três cestas de commodity) em **% do nível**, e não em pontos.
- A forma é a mesma do simulador (`_simPerfilChoque`): permanente, com decaimento, constante
  + decaimento. **O preço do resíduo, que a tela avisa com o número derivado:** um erro
  permanente acumula pela persistência da própria equação — na regra de juros
  `1/(1 − t1 − t2)` ≈ 7 vezes o choque; na (F), que é em variação, é uma desvalorização todo
  trimestre, para sempre. A aba abre num choque de 1 p.p. no resíduo da regra, sobrando metade
  a cada trimestre.

**Horizonte de 20 trimestres**, também decisão do usuário: a meia-vida do hiato é 6 e a da
Selic uns 5, e em 12 a maioria das respostas não voltou.

**Números do choque padrão, pesos da mediana:** Selic +2,2 p.p. no pico (trimestre 3), hiato
−0,57 (trimestre 8), IPCA de 12 meses −0,28 (trimestre 16), Focus −0,11, câmbio −1,6% no
trimestre 4. O câmbio não volta ao nível: o carry entra em diferença, então um juro que sobe e
volta deixa o nível deslocado — a mesma propriedade descrita no sexto round.

**A faixa é medida contra o cenário do MESMO desenho.** O cenário sem choque é resolvido uma
vez por conjunto de pesos (cacheado — não muda quando o choque muda) e cada resposta é o choque
menos ele. Contra o cenário da mediana a faixa mediria a distância entre dois cenários de pesos,
e não o choque; a asserção é que com choque zero a faixa inteira é zero. As voltas do choque
partem do sistema já resolvido sem ele, que é o mesmo ponto fixo em menos voltas.

**Gabarito:** `irf.construir()` grava cinco choques — um de cada tipo de alvo e de cada forma —
resolvidos no Python; o JS tem de devolver os mesmos números (pior diferença ~1e-9). O gabarito
de um passo de cada equação não alcança o resíduo novo, e o `sistema_padrao` não alcança choque
nenhum.

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
- **A (R) mede o desvio na Focus de 12 meses desde 2026-09-24** (era 18; ver §R5 do arquivo dela).
  O módulo é
  [`equations/taylor.py`](equations/taylor.py) e o painel ganhou `selic`, `selic_fim`, `pi_e_2a`,
  `meta_24m` e `pi_bcb` — nenhuma dessas cinco aparece na aba de Dados, porque o `_ORDEM` de
  `generate_report.py` é lista explícita. A forma tem **duas defasagens**, por decisão do usuário. Com ela os **três parâmetros comparáveis
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
- **O simulador está no ar com TRÊS equações desde 2026-09-25**: (E) → (R) → (F), nessa ordem de
  solução. A (E) entrou por escolha do usuário, e ela é a que produz o insumo da (R) — desde a
  uniformização em 12 meses, exatamente o objeto que a regra de juros consome. Do plano da pasta
  sobra o **Apêndice**.

  **A quarta é a (I), a curva de Phillips, e ela é a que fecha o laço.** Hoje há uma *corrente*
  de três elos e não realimentação: a (E) lê a inflação do trimestre, que é premissa. Com a (I)
  dentro, o câmbio que a (F) produz volta para a inflação, a inflação volta para a expectativa, e
  a expectativa volta para o juro — **e aí a ordem de solução `H → I → E → R → F` do plano passa a
  ter executor**. É também a mais cara das que faltam: quatro subequações, o resíduo MA(3) e a
  ressalva de que o `i1` não é comparável ao publicado. A (H) continua sem tocar a Selic.

  **O que a (I) acorda:** `F4` e `P13`, as duas que dependiam de alguma coisa propagar `F` de uma
  equação para outra, mais `F2` numa segunda face — a (F) mede o câmbio pelo **fechamento** do
  trimestre e a coluna `de` do painel, que é o `F(t)` da curva de Phillips, mede a variação da
  **média** (desvios 8,32 contra 6,76). Hoje isso é inconsistência declarada porque nada propaga;
  no dia em que a (I) entrar, passa a ser decisão a tomar. `E6` fechou em 2026-09-24.

  **E o que a (E) cobrou ao entrar:** o fim das premissas compostas (três cartões viraram cinco),
  o gabarito de um passo na (R), e a decisão de que o IPCA tem **um** cartão e não dois — todos no
  sétimo round acima. Da (F), a vol do `carry_vol` virou premissa de tela; a outra metade da
  simultaneidade continua esperando vol implícita de opções, que não tem tabela no banco.
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
