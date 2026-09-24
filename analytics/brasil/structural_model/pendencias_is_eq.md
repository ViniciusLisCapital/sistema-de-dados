# Pendências — Equação (H), a curva IS

Tudo o que falta na equação (H) do modelo estrutural. **O que está no ar vive no
[`CLAUDE.md`](CLAUDE.md) da pasta** — aqui só entra o que ainda não foi feito, mais o que foi
medido e **não** entrou.

```
(H) H(t) = h1·H(t-1) + h2·g_rr(t-1) + d08 + d20 + ε

    g_rr = juro real de mercado de 2 anos − o de 10 anos (NTN-B), p.p.
```

Estado em 2026-09-21 — 81 trimestres, 2006T2→2026T2:

| parâmetro | peso | margem | t (HAC 4) | t (MQ) |
|---|---|---|---|---|
| hiato do trimestre anterior | 0,8864 | ± 0,0738 | 12,01 | 17,95 |
| aperto do trimestre anterior | −0,1639 | ± 0,0626 | −2,62 | −2,10 |
| crise de 2008-2009 | −0,4376 | ± 0,4091 | −1,07 | −1,47 |
| pandemia de 2020 | −1,1447 | ± 0,7727 | −1,48 | −2,89 |

R² 0,868 · RMSE 0,642 · erro médio 0,412 · meia-vida de um hiato **6 trimestres** · efeito de
longo prazo **−1,443** · **Ljung-Box Q(4) p 0,021 (rejeita) e Q(8) p 0,097 (não rejeita)**.

Convenção deste arquivo: **H#** pendência. Cada item diz se está bloqueado por dado, por decisão
ou por trabalho.

---

## 0. Duas decisões do usuário que fecham perguntas

**A medida de aperto é a inclinação da curva real**, decidida em 2026-09-21 depois de a
alternativa ser medida item a item (ver §2). Não é uma escolha de conveniência: é a única
candidata que não exige estimar uma taxa de juro de equilíbrio, objeto sobre o qual as fontes
discordam em 2,7 p.p. hoje.

**O hiato em tempo real fica de fora**, também por decisão explícita do usuário no mesmo dia:
*"use a última série, não vou lidar com o problema de vintage agora."* É o item H1 abaixo, e é a
pendência de maior consequência da lista.

---

## 1. O que está aberto na forma atual

### H1 — O hiato é a edição corrente, não o que se sabia na época · *decisão tomada, pendência aberta*

`pm_hiato_produto` guarda a **última** leitura do anexo do RPM, e o BCB reescreve o passado a cada
edição. Então a variável explicada de 2010 é o que o BCB acha hoje sobre 2010, não o que ele
publicava em 2010.

**A direção do viés é conhecida e o tamanho não foi medido.** A edição corrente é suavizada dos
dois lados, o que infla `h1` (a série fica mais suave do que era) e atenua `h2` (parte do
movimento que a política causou foi reescrita). Com `h1` em 0,886 e meia-vida de 6 trimestres, o
espaço para isso não é pequeno.

`pm_hiato_produto_vintages` existe e tem o dado. **Atenção à quebra metodológica entre as edições
2024-06 e 2024-09** — só `central` é comparável entre os dois regimes, e o plano da pasta já
registra isso. O trabalho é montar a série real-time (cada trimestre com a leitura da edição mais
próxima posterior a ele) e reestimar ao lado.

### H2 — O resíduo ainda tem padrão em quatro trimestres · *não bloqueado*

Q(4) p 0,021 rejeita; Q(8) p 0,097 não. A autocorrelação do erro é **0,33** em um trimestre e cai
para 0,03 em dois — o padrão está concentrado na primeira defasagem, o que aponta para termo
faltando e não para sazonalidade.

Isso está declarado em quatro lugares da aba (ficha, cartão de erro, tabela e nota), com asserção
exigindo que os quatro digam o que o teste mede, nos dois sentidos. Parte do padrão vem de H1: um
hiato suavizado pela fonte produz erro suavizado.

### H3 — As duas dummies de crise não são individualmente firmes · *medido, e é uma tensão real*

`d08` tem t −1,07 e `d20` tem t −1,48 sob HAC(4). Pelo t individual, nenhuma das duas sobreviveria.
**Mas tirá-las derruba o aperto**: `h2` vai de −0,175 para −0,113 e o t de −2,75 para −1,22, com o
RMSE subindo de 0,645 para 0,687 (amostra comum, na tabela da página).

A leitura honesta é que elas não são estimativas do tamanho da crise — são o que impede dois
episódios que nenhuma política monetária explica de definirem a inclinação do resto. O HAC(4) é
severo com elas justamente porque são poucos trimestres consecutivos. **Decisão em aberto:** manter
como está (a escolha atual, e a do plano), ou substituir por uma dummy só de 2020, que é a que
carrega quase todo o efeito — os quatro maiores resíduos da amostra são os quatro trimestres de
2020, mesmo com `d20` dentro.

### H4 — O `h1` fica acima do intervalo que o BC publica · *medido, e provavelmente é H1*

O BC publica `b1 = 0,85` com IC 90% de [0,70; 0,95] — o nosso 0,886 está dentro. Mas o `t(MQ)` de
17,95 contra o `t(HAC)` de 12,01 mostra o quanto o erro correlacionado pesa aqui, e a suspeita é
que a persistência esteja inflada pela suavização da fonte (H1). Reestimar com o hiato real-time é
o que separa as duas hipóteses.

### H5 — Não há termo de condições financeiras · *previsto no BC, ausente aqui*

A eq. (2) do BC tem `−b3·rp_hat`, o prêmio de risco ciclicamente ajustado, com `b3 = 0,030` e IC
[0,027; 0,032] — estreito, portanto bem identificado lá. `modelo_painel.py` já constrói `rp_hat`
(CDS winsorizado, ajustado pela semielasticidade fiscal, filtrado por HP), então **o insumo existe
e é importável**. Não entrou porque o plano da pasta não o pede.

Vale notar o que isso significa para a comparação: parte do que o nosso `h2` mede pode ser condição
financeira, já que a inclinação da curva real e o prêmio de risco andam juntos em crise.

---

## 2. O que foi medido e está DESCARTADO

Não são pendências: são medições que fecham perguntas que voltariam sozinhas.

- **Taxa de juro de equilíbrio constante, ou quase.** Com `RR*` fixo em 4,5% ou com a neutra que o
  BC declara no RPM (4,50 → 4,75 em jun/2024 → 5,00 em dez/2024), `h2` sai em **−0,052 e −0,055**,
  com t de −1,44 e −1,45. Na amostra mais longa que cada uma permite (90 trimestres), pior ainda:
  −0,016 e −0,017, t −0,63 e −0,65. **A causa é medida:** o juro real ex-ante cai de 12,2% em
  2001T4 a −0,9% em 2020T4 e volta a 8,5%, e o hiato não tem essa tendência — um nível fixo não
  remove nada.
- **A mediana das 5 medidas do boxe do BC** (`monetary_policy/data/modelo_neutra_pub.csv`): −0,075,
  t −1,61. E ela **para em 2024T2**, porque o boxe é de jun/2024 — não serve para o período
  corrente sem ser estendida.
- **O filtro HP com cauda Focus ajusta MELHOR que a inclinação** e mesmo assim não foi escolhido:
  −0,231 (t −4,42) contra −0,164 (t −2,62), na mesma janela. Isso está na tabela da página em vez
  de escondido. As duas razões para não usá-lo: é um filtro de **dois lados**, então para decidir
  qual era o equilíbrio em 2010 ele usa dado de 2012 — look-ahead que não existia na época —, e o
  nível dele hoje é **7,7%**, o que diz que a Selic de 15% quase não aperta. *Se um dia o
  look-ahead for resolvido (HP recursivo, refeito a cada trimestre com o dado daquele trimestre),
  esta linha volta a ser candidata.*
- **A expectativa de juro real da Focus por horizonte não serve como `RR*`.** Ela anda com o juro
  corrente quase um para um: beta de **1,031** em 1 ano, 0,748 em 2, 0,579 em 3 e 0,510 em 4, contra
  0,504 da NTN-B de 10 anos e 0,350 do a termo 5a5a. Subtraindo a de 1 ano sobra um gap com desvio
  de **0,35 p.p.**, que é ruído: `h2` sai **+0,035**, sinal trocado. As de 2 e 3 anos dão −0,069 e
  −0,049, nenhuma significativa. A série existe e é construível para qualquer horizonte
  (`focus_anual()` interpolado, o `cauda_juro_real()` generalizado), cobrindo 2000T1→2026T3.
- **Descontar o prêmio de maturidade da NTN-B não muda nada na estimação.** Com intercepto, subtrair
  uma constante de `RR*` deixa `h2` idêntico à quarta casa (−0,1422, t −2,95, nos dois casos) e move
  só o intercepto. Sem intercepto, **piora**: −0,144 vira −0,107 (t −3,45 → −1,88). O prêmio é
  informação sobre o **nível**, não sobre a inclinação da equação.
- **A convenção de trimestralização não decide nada.** Média do trimestre dá `h2` = −0,164
  (t −2,62) e fechamento dá −0,177 (t −2,65). A média ficou por argumento — é o aperto que vigorou
  ao longo do trimestre, o mesmo raciocínio do câmbio nesta pasta — e `g_rr_fim` anda ao lado no
  painel. As duas divergem até **0,99 p.p.** num trimestre isolado, o que é grande contra um desvio
  de 1,04, então a coluna paralela não é decorativa.
- **A defasagem de um trimestre é o pico nas duas convenções**, o que é o que torna a escolha
  robusta em vez de garimpada: L0 −0,113/−0,069, **L1 −0,164/−0,177**, L2 −0,122/−0,137.

### O prêmio de maturidade, medido — para o nível, não para a equação

Pedido do usuário em 2026-09-21: a NTN-B carrega taxa estrutural **e** prêmio, então compará-la com
a expectativa de juro real da Focus separa os dois. Medido, `NTN-B − Focus`, média e (desvio):

| | Focus 1a | Focus 2a | Focus 3a | Focus 4a |
|---|---|---|---|---|
| NTN-B 60M | +0,34 (1,24) | +0,56 (0,72) | +0,87 (0,82) | +1,11 (0,91) |
| NTN-B 120M | +0,36 (1,49) | +0,58 (0,77) | **+0,89 (0,61)** | **+1,11 (0,65)** |
| NTN-B 5a5a | +0,39 (1,82) | +0,60 (1,04) | +0,91 (0,68) | +1,12 (0,68) |

**O spread cresce com o horizonte e a volatilidade dele cai** — é o padrão que separa as duas coisas
misturadas. Em 1 e 2 anos o spread não é prêmio: é prêmio *mais* a convergência da política que
ainda falta acontecer, que é cíclica, e daí o desvio dobrado. Em 3–4 anos a convergência se esgotou
e o que sobra é estável: **o prêmio de maturidade da NTN-B de 10 anos é 0,9–1,1 p.p.** Descontando
hoje, 7,56 − 1,11 = **6,45%**, que é exatamente onde a Focus de 4 anos está (6,42%) — dois caminhos
independentes no mesmo lugar.

**Isto não está na página ainda**, e é o item H6.

---

## 3. O que ainda não foi feito

### H6 — A página não diz qual é a taxa estrutural em nível · *trabalho pequeno, decisão tomada*

A aba explica por que não usa uma taxa de equilíbrio, mas não diz **onde ela está**. O número medido
acima (7,56 − 1,1 ≈ 6,45%, confirmado pela Focus de 4 anos em 6,42%) é uma leitura útil e
verificável, e ele contrasta com os 5,0% que o BC declara usar — uma diferença de 1,4 p.p. que
muda a leitura de quão apertada a política está. Entra como frase derivada do payload, não escrita
à mão.

### H7 — O hiato mundial · *previsto no modelo do BC, excluído por ele mesmo*

A eq. (2) do BC tem `+b4·h*`, e o próprio BC excluiu: `b4 = 0,054` com IC cruzando zero. Registrado
para não voltar como pergunta.

### H8 — Margem e t do efeito de longo prazo · *mesma álgebra do P16 e do E7*

O efeito de longo prazo é `h2/(1−h1)`, razão de dois estimadores correlacionados, e sai na página
sem margem. O delta-method resolve com a matriz de covariância que já está em mãos. **É o mesmo
item que [`pendencias_philips_eq.md`](pendencias_philips_eq.md) registra como P16 e
[`pendencias_expectativas_eq.md`](pendencias_expectativas_eq.md) como E7** — se um for construído,
os três saem juntos.

### H9 — Estimar a neutra, em vez de contornar · *intenção do usuário, 2026-09-22*

O registro completo está em **R12** de
[`pendencias_taylor_eq.md`](pendencias_taylor_eq.md), porque lá a neutra é um termo explícito da
equação. O que muda **aqui** se ele for resolvido é maior do que parece: a inclinação 2a−10a foi
escolhida contra uma tabela de candidatas a `RR*` que ou **não se movem** (constante, a neutra
declarada no RPM — `h2` indistinguível de zero) ou **têm look-ahead** (o HP com cauda, que ajusta
melhor e foi rejeitado por isso). Uma neutra estimada, que se mova e não olhe para o futuro, é uma
categoria que **ainda não foi testada** — a §2 acima não a cobre.

Se ela existir e funcionar, `g_rr` volta a poder ser `r − RR*`, que é a forma da própria eq. (2) do
BC, e a §2 passa a ser história em vez de justificativa. Enquanto não existir, a inclinação
continua sendo a única candidata medida que entrega `h2` firme sem look-ahead.

Vale notar que **o BC usa duas neutras diferentes**, uma na IS e outra na Taylor (`rr_IS` e
`rr_TAY`, correlação 0,994, diferença média 0,12 p.p.) — então "estimar a neutra" é, no modelo dele,
estimar duas.

---

## 4. Ordem sugerida

1. **H1 é a pendência-raiz.** Ela é a única que pode mover `h1` e `h2` de verdade, e H2 e H4
   provavelmente são consequência dela.
2. **H6 é barato e melhora a leitura da página agora**, sem tocar na estimação.
3. **H3 depende de uma decisão**, não de trabalho.
4. **H5 entra se e quando o plano quiser o termo de condições financeiras** — o insumo já existe.
5. **H8 é pequeno e sai junto com P16 e E7.**
6. **H9 não tem data.** É intenção declarada do usuário, e o caminho barato passa por R11 na
   equação (R) — a mesma decomposição serve as duas.
