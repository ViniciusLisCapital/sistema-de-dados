# Pendências — Curva de Phillips desagregada

Tudo o que falta na equação (I) do modelo estrutural: variáveis a acrescentar, formas a testar,
testes a escrever e dívidas de produto. **O que já está decidido, medido e no ar vive no
[`CLAUDE.md`](CLAUDE.md) da pasta** — aqui só entra o que ainda não foi feito.

Estado na abertura deste arquivo (2026-09-17): quatro equações (serviços, alimentação, bens
industriais, monitorados) em inflação do trimestre, 91 trimestres (2003T4→2026T2), dummies de
trimestre soma-zero, média móvel de 4 trimestres em (IS) e (II), erros-padrão HAC(4). Reconstrução
do cheio RMSE 0,616 contra um piso de 0,025.

Convenção deste arquivo: **P#** pendência, **T#** teste. Cada item diz se está bloqueado por dado,
por decisão ou por trabalho. A exceção é o **§5**, que é material de referência — o gabarito do BC
para preços administrados — e cuja pendência é o **P15** lá dentro.

---

## 1. Variáveis a acrescentar

### P1 — Brent em (II), bens industriais · *não bloqueado*

A eq. (1) do modelo desagregado do BC tem Brent na equação de bens industriais; a nossa não.

| | |
|---|---|
| tabela | `macro_international.comm_brent`, `name='brent_usd'` |
| cobertura | diária, 1990-01-02 → 2026-09-15 (9.308 obs) — cobre a amostra inteira |
| forma a testar | variação do trimestre em USD, contemporânea e defasada um trimestre, como o IC-Br metálico já entra |

**O que medir antes de aceitar:** a colinearidade com `pi_met_usd`. As duas são commodity em dólar e
podem estar medindo o mesmo canal — se o `t` do metálico cair quando o Brent entra, o que se ganhou
foi rótulo, não informação. O critério de entrada é o mesmo que fez a MM4 entrar: **melhora medida no
Ljung-Box ou no `t` de um canal existente**, não presença na especificação do BC.

### P2 — Bloco de clima (ONI) em (IA), alimentação · *não bloqueado, com ressalva de ponta*

| | |
|---|---|
| tabela | `macro_international.clima_oni`, `name='oni'` |
| cobertura | mensal (trimestres móveis da NOAA), 1950-01 → **2026-04** (306 obs) |
| ressalva | a série termina ~5 meses atrás do IPCA. O trimestre da ponta do painel fica **sem ONI** |

Três decisões, nesta ordem:

1. **A defasagem de publicação tem de ser tratada explicitamente**, não preenchida em silêncio.
   Repetir o último valor é premissa, e premissa vai para a tela. A alternativa honesta é a coluna
   `completo` já existente passar a exigir ONI também — o que encurtaria a amostra estimável.
2. **Testar o efeito em MÓDULO, não só em nível.** El Niño e La Niña prejudicam safras diferentes;
   um coeficiente linear sobre o ONI assume que um ajuda tanto quanto o outro atrapalha. Rodar
   `oni`, `|oni|` e os dois juntos.
3. **Defasagem:** clima afeta preço via safra, então o efeito contemporâneo é o menos provável.
   Testar t−1 a t−4.

### P3 — (IM) indexado à parte LIVRE, não ao cheio · *não bloqueado, e não precisa de dado novo*

É o conserto do defeito declarado na página: `im2` sai **−0,225 (t −0,40)**, sinal invertido, porque
o IPCA cheio contém os próprios monitorados com peso médio de **0,2691**. A conta acaba explicando
monitorados por eles mesmos, e a diferença é jogada no peso da expectativa.

**Já está medido que o horizonte da âncora não é a causa** — as três âncoras testadas dão negativo, e
as duas de horizonte longo jogam o peso da expectativa acima de 1 (1,274 e 1,338), o que não tem
leitura possível. Ver a tabela no `CLAUDE.md`.

O insumo sai do próprio painel: os quatro pesos somam exatamente 1, e três dos quatro grupos são
livres, então

```
pi_livres_q = (wq_is·pi_is_q + wq_ia·pi_ia_q + wq_ii·pi_ii_q) / (1 − wq_im)
```

Coluna nova em `panel.py`, âncora nova em `ANCORAS_IM`, e ela entra na mesma tabela comparativa que
a página já mostra — o registro de que foi testada é parte da entrega.

**Critério de aceite:** `im2` positivo *e* peso da expectativa em [0, 1]. Se o sinal continuar
negativo com a parte livre, a hipótese mecânica está errada e o problema é outro — e isso é um achado
que vai para a página, não um motivo para esconder a equação.

### P4 — Dummies de crise (d08, d20) · *previstas no plano, nunca implementadas*

O plano de 2026-09-16 previa `d08` = 2008T4–2009T4 e `d20` = 2020T1–2020T4, as mesmas janelas do BC,
**estimadas com e sem**. O painel não tem as colunas e as equações não as usam.

Ordem de trabalho: medir o efeito **antes** de decidir. Duas dummies de 5 e 4 trimestres numa amostra
de 91 custam 9 graus de liberdade, e o argumento para elas é que 2020 distorce a inércia — o que é
medível, não presumível.

### P5 — Hiato em tempo real, como coluna de robustez · *não bloqueado*

`pm_hiato_produto_vintages` existe e `panel.py` já sabe dela (está citada no código). O hiato da
edição corrente é um objeto suavizado dos dois lados: ele conhece o futuro, o que **atenua** o
coeficiente estimado e faz a equação parecer menos sensível ao ciclo do que é.

Entra como coluna de comparação, não como substituto. Atenção à quebra metodológica entre as edições
2024-06 e 2024-09: só `central` é comparável entre os dois regimes.

### P6 — Expectativa por subíndice · *bloqueado por amostra, com data de revisão*

Hoje a âncora das quatro equações é a expectativa do **IPCA cheio**, o que impõe que os quatro
convirjam ao mesmo número — preços relativos constantes no longo prazo, que a história nega. É um dos
dois defeitos declarados na página.

`expc_focus` publica expectativa por subíndice, mas só desde **set/2021** — 20 trimestres contra 91.
**Revisar quando houver ~40 trimestres (meados de 2031)**, ou antes se for para rodar uma amostra
curta lado a lado só como diagnóstico.

### P7 — Canais ainda não testados · *especulativos, em ordem de prioridade*

- **Distribuição de defasagens do câmbio.** Hoje (IA) usa `de` contemporâneo e (II) usa `de_l1`, cada
  um com uma defasagem só, escolhida por analogia ao BC. Testar t a t−4 em ambas, e a soma dos
  coeficientes como o repasse total.
- **Termos de troca** (`macro_brasil.cmb_termos_troca`) — não está no BC, mas é o preço relativo que
  liga commodity e câmbio numa variável só. Vale como diagnóstico de se o par `de` + `pi_*_usd` está
  capturando o canal inteiro.
- **Salário/mercado de trabalho em (IS).** O BC não põe, e serviços é justamente onde o custo é
  salário. Candidatos no banco: rendimento da PNAD, CAGED. **Cuidado com a endogeneidade** — salário
  responde a inflação passada, então sem instrumento o coeficiente mede as duas direções.
- **Preço de energia/combustível dentro de (IM).** Monitorados é uma cesta de regimes muito
  diferentes (energia, combustível, saúde, transporte público), e o R² de 0,070 é o sintoma. Abrir o
  grupo é uma equação a mais, não um regressor a mais — e por isso está aqui e não em P1.

---

## 2. Formas e estruturas a testar

### P8 — Parâmetros variando no tempo · *o item grande*

**Já há evidência medida, e é o argumento para começar por aqui:** o ajuste sazonal de Q1 em serviços
cai **0,042 p.p. por ano (t −3,02** com a MM4 dentro; −0,058 e t −3,64 sem**)** — cerca de 1 p.p. ao
longo da amostra. Q2 e Q3 não se mexem. Serviços também é o único dos quatro que rejeita Chow no vetor
sazonal com quebra em 2015T1 (F 3,71, p 0,0147).

Uma tendência linear na dummy **melhora o R² de 0,626 para 0,695 e foi recusada de propósito**: é
muleta. O lugar certo é um sazonal estocástico em espaço de estados.

### P9 — Os `A_t` do BC · *depende da mesma maquinaria de P8*

Um passeio aleatório não observado por setor, que é o que permite preços relativos derivarem em vez de
os quatro convergirem ao mesmo número. Sem eles sobra viés sistemático de sinal oposto em serviços e
industriais — que é exatamente o que os vieses de 12 meses mostram hoje (**−0,438** em serviços contra
**+0,585** em industriais).

P8 e P9 são o mesmo passo de engenharia: sair de MQ equação a equação para filtro de Kalman. Vale
fazer juntos, e **é a fronteira entre "quatro regressões" e "um modelo"**.

### P10 — Abrir monitorados · *ver a última alínea de P7, e agora o §5*

**Não abra antes de P15.** O §5.6 mostra o caminho mais barato: reconstruir π^A pelas 24 identidades
do BC e medir o resíduo. Se ele for pequeno, o R² de 0,070 está explicado e o grupo não precisa de
mais equações estimadas — precisa de menos.

---

## 3. Testes e asserções que faltam

`tests/test_structural_model_js.js` tem **592 asserções** e pega **25 de 25** mutantes. O que ele
ainda não alcança:

### T1 — Pan/zoom confirmado visualmente · *a pendência que sobrevive a todas*

A confirmação em browser real (Chrome headless via CDP) cobre carga, pintura, os dez cabeçalhos e o
seletor indo e voltando, com zero exceções. **Não cobre o gesto**: arrastar, rolar e o duplo-clique
nunca foram confirmados por um humano olhando a tela.

### T2 — Estabilidade dos coeficientes principais

Chow só foi rodado no **vetor sazonal**, e só em (IS). Falta nos coeficientes de inércia, expectativa
e choques das quatro equações. Sem isso, "a inércia de serviços é 0,027" é uma afirmação sobre a
amostra inteira que pode não valer em nenhum pedaço dela.

### T3 — Coeficientes em janela móvel, na página

Não há gráfico de estabilidade no relatório. É o complemento visual de T2, e é o que torna P8
argumentável para quem lê em vez de só para quem estima.

### T4 — Avaliação fora da amostra de verdade

Tudo hoje é dentro da amostra: os coeficientes usados em qualquer trimestre foram estimados com dado
daquele trimestre. Falta o exercício recursivo — estimar até T, avaliar em T+1, repetir. **Isto é
diferente da vista de 12 meses**, que é tradução de unidade do ajuste histórico e não previsão (ver
`CLAUDE.md`).

### T5 — Gabarito dos pesos contra o IBGE

Os `wq_*` são reconstruídos da decomposição e renormalizados. A página compara a **soma** dos quatro
contra o cheio (RMSE 0,025, e isso é forte), mas **nenhuma asserção confere os pesos em si** contra os
pesos publicados pelo IBGE. É o tipo de erro que a soma absorve.

### T6 — O `panel.csv` versionado contra `construir()`

O CSV está no git e o relatório chama `construir()` ao vivo. Nada garante que os dois concordem — um
CSV velho no repositório é uma afirmação sobre o dado que ninguém está checando.

### T7 — Duas coisas medidas que NÃO têm asserção, e por quê

Registradas aqui para não serem "descobertas" de novo:

- **Peso do trimestre: média dos três meses contra o último mês.** RMSE 0,0318 nos dois, igual à
  quarta casa. Um mutante que troque os dois não muda número nenhum — **não há asserção a escrever**.
  (Na métrica de 12 meses importava: 0,065 contra 0,106.)
- **MA(1) no resíduo de alimentação.** Ljung-Box não rejeita (p 0,211), então não há autocorrelação a
  modelar; o θ da máxima verossimilhança (−0,641) é incompatível com a ACF de MQ (−0,082) e o RMSE
  piora de 1,927 para 2,152. Encerrado pelo diagnóstico, não por asserção.

---

## 4. Dívidas de produto

### P11 — Decomposição e teste de estresse · *pedido em 2026-09-16, nunca entregue*

No padrão das seções *Exchange Rate Decomposition* e *12-Month Forecast (Stress Test)* do
`FX Report`. A vista de 12 meses construída em 2026-09-17 **não** cobre a segunda: ela lê o ajuste
histórico numa unidade anual, não projeta sob cenário.

### P12 — As outras quatro equações · *RESOLVIDO em 2026-09-22*

(E) expectativas, (H) IS, (R) Taylor e (F) câmbio estão estimadas, cada uma com a sua aba e a sua
lista de pendências. O que falta do plano da pasta é o Apêndice.

### ~~P13 — Simulador~~ · *retirado do plano em 2026-09-22*

Propagaria `H → I → E → R → F` com toggle Endógeno/Manual por equação. Decisão do usuário não
construí-lo. Consequência para as outras listas: **F2** e **E6** existiam por causa dele e ficaram
sem gatilho, e **F4** perdeu metade do argumento.

### P14 — Vol implícita de opções do câmbio · *bloqueado no usuário*

Até chegar, `VOL_SOURCE=realizada_lag`. Destino recomendado: tabela `macro_brasil.cmb_vol_implicita`
pelo conector Bloomberg que já existe — **não** CSV exportado à mão.

### P16 — Margem e teste para o peso da expectativa · *adiado por escolha, em 2026-09-21*

Desde 2026-09-21 o peso da expectativa tem linha própria na tabela, com margem e t em travessão —
ele é `1 − Σ` dos pesos restritos e não tem coluna na regressão. **Mas a margem é calculável, e
exatamente**: sendo combinação linear dos estimados, `Var(1 − Σβ) = 1'V1` com o mesmo V de
Newey-West que a tabela já usa (`res.cov_params()`), sem aproximação nenhuma.

O que isso acrescentaria é um teste que hoje não existe em lugar nenhum da página: **o peso da
expectativa é distinguível de zero?** Em monitorados ele é 0,914 — quase a conta inteira —, e é lá
que a pergunta importa, porque é a equação que não fecha (ver §5). A outra leitura útil é contra
**um**: um peso de expectativa igual a 1 quer dizer inércia nula.

Quando for feito: o payload ganha `se_e`/`t_e` por equação, a linha troca os dois travessões pelos
números e perde o rótulo *conta de sobra* como justificativa da ausência (mas **não** a subtração
impressa, que é o que torna o número verificável na linha). A nota de rodapé do `‡` muda junto, e
há mutante para a linha inventar margem — ele passa a precisar de outra âncora.

O usuário pediu explicitamente para **não** construir isso na mesma rodada: *"Não precisa fazer tudo
isso, somente coloque ele na lista indicando que ele é uma conta de sobra."*

---

## 5. Preços administrados: o que o BCB faz, e o que isso diz da nossa (IM)

Levantamento de 2026-09-17 nas fontes primárias do BC (boxes de RI/RPM e o Trabalho para Discussão
305). Entra aqui, e não no `CLAUDE.md`, porque **não descreve o que está no ar — descreve o gabarito
contra o qual a nossa quarta equação está sendo julgada**, e é o insumo de P15, P3 e P10.

**O achado que muda a leitura da equação (IM): o BC não estima curva de Phillips para monitorados.**
Não é que ele estime uma melhor que a nossa. Ele projeta os administrados por **24 identidades
trimestrais calibradas**, uma por item, derivadas da regra de reajuste de cada setor — sem hiato do
produto, sem expectativa, sem Selic. Isso reenquadra dois números que hoje estão na página como
defeito: o R² de **0,070** e o `im2` de **−0,225 (t −0,40)** não são sintoma de regressor faltando,
são o que se espera de tentar estimar um objeto que é, por construção, contrato indexado mais cunha
exógena.

### 5.1 As três camadas

O BC separa por horizonte, e é isso que deixa o modelo de médio prazo tão simples:

| camada | o quê | horizonte |
|---|---|---|
| curto prazo | **especialista, bottom-up** — reajuste da ANEEL já homologado, tabela CMED, bandeira tarifária, defasagem PPI/crack spread | **4 a 5 trimestres** — mais longo que o de preços livres, porque a vantagem informacional do especialista é maior |
| médio prazo | **as 24 equações calibradas**, acopladas aos semiestruturais de pequeno porte (agregado e desagregado) com feedback nos dois sentidos | do fim do especialista em diante |
| Samba (DSGE) | bloco reduzido, só duas elasticidades estimadas: administrados ao câmbio real **υ₁,A = 0,03** e a commodities **υ₂,A = 0,02** | — |

O feedback é o ponto que nos interessa: o IPCA cheio projetado entra na indexação de quase todos os
itens administrados, e os administrados voltam para o IPCA cheio. Não é um bloco satélite pendurado
no fim.

### 5.2 A forma comum: indexação plena ao IPCA de 4 trimestres

Dezessete dos 24 itens são uma destas duas linhas:

```
π_t^item = Σ_{j=1..4} d_{j,t} · c_j · ( Σ_{i=1..4} ΔIPCA_{t−i} )      [com sazonalidade]
π_t^item = (1/4) · Σ_{i=1..4} ΔIPCA_{t−i}                            [sem sazonalidade]
```

Os `c_j` **somam 1** em todos eles (a tabela publica sempre `c₄ = 1 − c₁ − c₂ − c₃`): repasse unitário
da inflação passada no longo prazo, com os `d_{j,t}` distribuindo o reajuste pelo trimestre em que ele
sai. As constantes sazonais são "combinação de estimação com amostra desde 2020 e julgamento" — a
única coisa no modelo que olha para dado, e ainda assim com a mão do especialista dentro.

Os 24 itens, com código IBGE e peso do IPCA de maio/2025 (soma **25,76%**):

| item | cód. | peso | forma |
|---|---|---|---|
| Gasolina | 5104001 | 5,24% | contábil (petróleo + câmbio) |
| Plano de saúde | 6203 | 4,06% | regra da ANS (IVDA) |
| Energia elétrica residencial | 2202003 | 3,78% | Itaipu + IPCA passado |
| Produtos farmacêuticos | 6101 | 3,46% | regra CMED |
| Emplacamento e licença | 5102004 | 2,69% | IPCA do ano anterior ÷ 4 |
| Taxa de água e esgoto | 2101004 | 1,84% | genérico sazonal (0,19 / 0,50 / 0,09 / 0,22) |
| Gás de botijão | 2201004 | 1,25% | contábil (GLP) |
| Ônibus urbano | 5101001 | 1,12% | genérico sazonal (0,75 / 0,20 / 0,05 / 0) |
| Jogos de azar | 7201063 | 0,44% | genérico sem sazonalidade |
| Ônibus intermunicipal | 5101006 | 0,41% | genérico sazonal (0,55 / 0,14 / 0,18 / 0,13) |
| Óleo diesel | 5104003 | 0,25% | contábil (diesel) |
| Plano de telefonia fixa | 9101002 | 0,22% | genérico sem sazonalidade |
| Táxi | 5101002 | 0,20% | genérico sazonal (0,48 / 0,31 / 0,04 / 0,17) |
| Gás encanado | 2201005 | 0,15% | regressão estimada |
| Ônibus interestadual | 5101007 | 0,11% | genérico sazonal (0,17 / 0,02 / 0,06 / 0,75) |
| Multa | 5102006 | 0,088% | genérico sem sazonalidade |
| Pedágio | 5102015 | 0,087% | genérico sazonal (0,22 / 0,04 / 0,42 / 0,32) |
| Gás veicular | 5104005 | 0,070% | regressão estimada |
| Metrô | 5101011 | 0,066% | genérico sazonal (0,38 / 0,58 / 0,04 / 0) |
| Correio | 9101001 | 0,065% | genérico sazonal (0,17 / 0,83 / 0 / 0) |
| Integração transporte público | 5101053 | 0,052% | IPCA passado no 1ºT |
| Conselho de classe | 7101090 | 0,048% | IPCA do ano anterior ÷ 4 |
| Trem | 5101004 | 0,038% | IPCA passado no 1ºT |
| Cartório | 7101034 | 0,023% | IPCA passado no 1ºT |

**Gás encanado e gás veicular são as duas únicas equações estimadas do modelo inteiro** — e as duas
são regressões lineares sobre IPCA acumulado, petróleo em reais e o item vizinho (botijão e gasolina,
respectivamente).

### 5.3 Os quatro itens grandes, na íntegra

São 55% da cesta administrada e onde está todo o conteúdo econômico. Transcritos do anexo do boxe de
jun/2025 (págs. 87-90).

**Gasolina** — `c₀=0,4  c₁=0,4  c₂=0,2  c₃=0` · `p₁=0,35  p₂=0,13  p₃=0,24  p₄=0,11  p₅=0,17`

```
ΔPetrobras_t        = Σ_{i=0..3} c_i (ΔPetróleo_{t−i} + ΔCâmbio_{t−i}) + ε
ΔEtanol_t           = ΔPetrobras_t + ε
ΔICMS_t             = d_{1,t} · Σ_{i=1..4} ΔIPCA_{t−i} + ε          [só no 1º trimestre]
ΔImpostos federais_t = ε                                             [fixos]
ΔMargem_t           = (1/4)·[ (2/3)Σ_{i=1..4} ΔIPCA_{t−i} + (1/3)Σ_{i=0..3} ΔIPCA_{t−i} ] + ε
π_t^Gasolina        = p₁ΔPetrobras + p₂ΔEtanol + p₃ΔICMS + p₄ΔImpostos federais + p₅ΔMargem + ε
```

Como o etanol segue a Petrobras, o repasse direto de câmbio+petróleo para a bomba é `p₁ + p₂ = 0,48` —
que é de onde saem os ~50% da IRF.

**Plano de saúde** — `a = 0,6`

```
IVDA_A       = a·IVDA_{A−1} + (1−a)·IPCA_{A−1} + ε                   [anual]
Reajuste_A   = 0,8·IVDA_A + 0,2·ΔIPCA^{ex plano saúde}_{A−1}         [a regra literal da ANS]
π_t^Plano    = d_{1,t}(Reajuste_{A−1}/4) + Σ_{i=2..4} d_{i,t}(Reajuste_A/4)
```

O ¼ por trimestre não é suavização: o IBGE distribui o reajuste linearmente pelos 12 meses seguintes,
porque cada contrato é reajustado no seu mês de aniversário. O IVDA do ano seguinte é **julgamento do
especialista**; daí em diante vira inércia mais indexação.

**Energia elétrica residencial** — `α_Itaipu=0,086  α_energia=0,6` · `c = 0,08 / 0,40 / 0,42 / 0,10` ·
`c_Itaipu = 0,10 / 0,35 / 0,42 / 0,13`

```
π_t^Energia        = π_t^{Energia ex-band} + π_t^bandeira
π_t^bandeira       = −(π_{t−1}^band + π_{t−2}^band + π_{t−3}^band) + ε
π_t^{Energia ex-band} = (1 − α_Itaipu·α_energia)·( Σ_j d_{j,t} c_j Σ_i ΔIPCA_{t−i} )
                      + α_Itaipu·α_energia·( Σ_j d_{j,t} c_{Itaipu_j} Σ_i (ΔItaipu_{t−i} + ΔCâmbio_{t−i}) ) + ε
ΔItaipu_t          = d_{1,t} · Σ_{i=1..4} ΔCPI^{USA}_{t−i} + ε
```

Duas coisas valem ser copiadas de desenho. A primeira: **só ~5% da tarifa tem câmbio**
(`0,086 × 0,6`), porque a energia de Itaipu é ~8% da consumida pelo mercado cativo e tem preço em
dólar — o resto é Parcela A/B indexada a índice de inflação. A segunda: **a bandeira é modelada para
se anular.** A soma de quatro trimestres consecutivos daquela recursão é ε, então a projeção acumulada
em 12 meses da energia não depende da bandeira, que é decisão do especialista e não do modelo.

**Produtos farmacêuticos** — `c_câmbio=0,15  c_energia=0,07` · `c_rep = 0,10 / 0,80 / 0,05 / 0,05`

```
Fator X_t = ε ;  Fator Z_t = ε                                       [zerados no médio prazo]
Fator Y_t = [ c_câmbio( Σ ΔCâmbio_{t−i} + Σ ΔCPI^{USA}_{t−i} − Σ ΔIPCA_{t−i} )
            + c_energia( Σ π^{Energia ex-band}_{t−i} − Σ ΔIPCA_{t−i} ) ] + ε
reajuste_t = Σ_{i=1..4} ΔIPCA_{t−i} − Fator X_t + Fator Y_t + Fator Z_t
π_t^farmacêuticos = d_{1,t}c_{rep,1}·reajuste_{t−3} + d_{2,t}c_{rep,2}·reajuste_t
                  + d_{3,t}c_{rep,3}·reajuste_{t−1} + d_{4,t}c_{rep,4}·reajuste_{t−2} + ε
```

X (produtividade) e Z (preços relativos intrassetores) viram choque puro por parcimônia — são difíceis
de prever e, no horizonte em que importam, quem projeta é o especialista. O reajuste sai em abril e
80% dele cai no 2º trimestre.

### 5.4 Os canais, medidos

IRFs publicadas no boxe, **sem reação da Selic**, acumulado em 4 trimestres:

| choque | administrados | livres | IPCA |
|---|---|---|---|
| câmbio +10% | **+1,8 p.p.** | +0,70 p.p. | +1,0 p.p. |
| Brent +10% (US$) | +1,3 p.p. | — | — |
| livres +1 p.p. | resposta defasada e mais persistente | 1 p.p. | — |
| IVDA +1 p.p. | +0,14 p.p. (plano de saúde +0,8 p.p.) | +0,02 p.p. | +0,04 p.p. |

Três leituras que importam para cá:

- **O repasse cambial dos administrados é ~2,6× o dos livres**, e vem quase todo de combustíveis,
  medicamentos e energia. Nos demais itens o efeito existe, mas é indireto, via indexação.
- **No choque de livres, a partir do 5º trimestre a resposta dos administrados supera a dos livres**,
  quando a dos livres já está se dissipando. A indexação ao IPCA de 4 trimestres é o que produz isso —
  e é exatamente o mecanismo que a nossa (IM) tentaria capturar com `im2`.
- Repasse do petróleo: ~50% acumulado para a gasolina, ~20% para o botijão (menor porque distribuição
  e revenda pesam proporcionalmente mais).

### 5.5 A linhagem — a econometria foi testada e abandonada

| quando | o que era |
|---|---|
| 2002 (Springer de Freitas et al.) | coeficientes de repasse cambial por item: gasolina 0,23, GLP 0,27, energia 0,18, telefone fixo 0,00 |
| 2012-13 (**TD 305**) | híbrido: 12 itens "contábeis" (14,1% do IPCA) + o resto **econométrico agregado** — 4 AR e 2 VAR para administrados, 3 AR e 3 VAR para o subconjunto não contábil, escolhidos por REQM fora da amostra contra um AR(1). **Zerou todos os repasses cambiais**: a correlação entre preço internacional e preço de realização da Petrobras cai de ρ 0,76 (2002-2007) para **−0,10** (2006-2011) |
| **set/2017** | acaba o VAR/AR: 23 itens, cada um com equação derivada do contrato ("semiestrutural calibrado"). Única exceção estimada: energia elétrica |
| **jun/2025** | 24 itens; energia elétrica **sai da estimação** e vira calibração por peso de Itaipu em cada distribuidora; sazonalidade recalibrada com amostra desde 2020; ICMS dos combustíveis simplificado; equações e IRFs publicadas na íntegra pela primeira vez |

Vale reter o sentido da trajetória: **o BC caminhou de VAR para identidade calibrada, não o
contrário.** Série curta, quebra de regra de reajuste e mudança de política de preços da Petrobras
fazem o parâmetro estimado envelhecer mais rápido que o calibrado — que é o mesmo argumento pelo qual
o `im2` da nossa (IM), estimado em 91 trimestres que atravessam três regimes de preço de combustível,
não deveria ser esperado estável.

### 5.6 P15 — trazer o bloco para cá · *não bloqueado por dado*

O que isso habilita, em ordem:

1. **π^A deixa de ser premissa no simulador da RÉPLICA** — o de `monetary_policy/modelo_agregado.py`,
   que é outro objeto e continua existindo; o simulador desta pasta saiu de escopo em 2026-09-22.
   Hoje `modelo_agregado.py` roda com `π^A = meta/4`, e é
   isso que separa o nosso IRF da primeira linha do C2 Boxe3 Graf 4B. Com o bloco, o choque de câmbio
   no IPCA cheio vai de ~0,7 p.p. para ~1,0 p.p. — **43% num canal que a aba FX Model já usa**.
2. **A (IM) ganha um gabarito.** Reconstruir π^A pelas 24 identidades e comparar com o realizado diz
   quanto da variância de monitorados é regra de reajuste, e o resíduo é o que sobra para uma
   equação estimada explicar. Se o resíduo for pequeno, P10 (abrir monitorados) está respondido: o
   grupo não precisa de mais equações estimadas, precisa de menos.
3. **Não custa dado novo.** Os códigos das equações são códigos IBGE, e são a chave das tabelas que já
   mantemos:

| insumo | onde está |
|---|---|
| 22 subitens (7 dígitos) | `macro_brasil.inflc_decomposicao` — `var_mensal` e `pesos` por `subitem_codigo` |
| 2 itens (4 dígitos: 6203 plano de saúde, 6101 farmacêuticos) | `macro_brasil.inflc_decomposicao_item` |
| ΔCâmbio, ΔIPCA | painel do modelo (`panel.py`) |
| ΔPetróleo (Brent) | `macro_international.comm_brent` — a mesma série de P1 |
| ΔCPI^USA | FRED, já no `macro_us` |
| IVDA | **único que não temos**: é anual, da ANS, e no modelo do BC é julgamento do especialista de qualquer forma |

**Ressalva de escopo, e ela é a razão de isto ser P15 e não um item da fila curta:** o bloco é 24
identidades e uma tabela de parâmetros, mas as camadas 1 e 3 do §5.1 **não** vêm junto. Sem o
especialista, os 4-5 primeiros trimestres ficam piores que os do BC por construção — o que é aceitável
para fechar o repasse cambial do IRF e não é aceitável para publicar projeção de administrados como
número. Se entrar, entra dito assim na página.

### 5.7 Fontes

- [Atualização do modelo para projeção de médio prazo dos preços administrados — RPM jun/2025](https://www.bcb.gov.br/content/ri/relatorioinflacao/202506/rpm202506b9p.pdf)
  — a referência principal; as 24 equações e seus parâmetros estão no anexo, págs. 87-90
- [Reformulação dos modelos para projeção de médio prazo dos preços administrados — RI set/2017](https://www.bcb.gov.br/htms/relinf/port/2017/09/ri201709b7p.pdf)
- [TD 305 — Preços Administrados: projeção e repasse cambial (Alves, Figueiredo, Nascimento Jr. e Perez, 2013)](https://www.bcb.gov.br/pec/wps/port/TD305.pdf)
- [Atualização dos modelos semiestruturais de pequeno porte — RI jun/2024](https://www.bcb.gov.br/content/ri/relatorioinflacao/202406/ri202406b12p.pdf)
- [Revisão do Modelo Estrutural de Médio Porte – Samba — RI mar/2023](https://www.bcb.gov.br/content/ri/relatorioinflacao/202303/ri202303b5p.pdf)
- [Relatório de Política Monetária — jun/2026](https://www.bcb.gov.br/content/ri/relatorioinflacao/202606/rpm202606p.pdf) — a prática corrente de projeção e os condicionantes

---

## 6. Fora de escopo, declarado

Não são pendências; são decisões de não fazer, registradas para não voltarem como pergunta:

- ~~**Preços administrados como bloco próprio** do modelo agregado~~ — **revisto em 2026-09-17.** A
  exclusão supunha que o bloco fosse trabalho de modelagem; o levantamento do §5 mostrou que são 24
  identidades calibradas com parâmetros publicados, sem estimação. Virou **P15**. O que continua fora
  é reproduzir a camada de especialista de curto prazo, que é julgamento e não modelo.
- **Hiato mundial.**
- **Hiato estimado como estado latente** — usamos o publicado pelo BC.
- **CDS endógeno a um bloco fiscal.**
- **Unificação com o modelo do `FX Report`**, que continua servindo o relatório cambial até este
  provar que o substitui.

---

## 7. Ordem sugerida

Em ordem de razão-entrega-sobre-esforço, com a dependência entre eles:

| # | item | por quê nesta posição |
|---|---|---|
| 1 | **P3** (IM) na parte livre | conserta um defeito que a página já declara; não precisa de dado novo; poucas linhas |
| 2 | **P1** Brent · **P2** ONI | fecham a diferença declarada contra a especificação do BC; dado no banco e em dia |
| 3 | **P4** dummies de crise · **P5** hiato real-time | baratos, e mudam a leitura dos coeficientes que já estão na tela |
| 4 | **P15** bloco de administrados | mecânico (parâmetros publicados) e aproveita o Brent que P1 já traz; fecha o repasse cambial do IRF e dá gabarito à (IM), o que **responde P10 antes de gastar equação nova nele** |
| 5 | **T2/T3** estabilidade | é o que dá base empírica ao passo seguinte |
| 6 | **P8/P9** parâmetros variando no tempo | o passo grande; sai de quatro regressões para um modelo |
| 7 | **P12** próxima equação (E) | começa a segunda metade do §IV.I |

**T1** (pan/zoom com humano olhando) e **T5/T6** (gabarito de pesos, CSV contra o vivo) são baratos e
não dependem de nada — cabem em qualquer rodada.
