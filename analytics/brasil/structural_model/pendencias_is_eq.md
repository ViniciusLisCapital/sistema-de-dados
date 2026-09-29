# Pendências — Equação (H), a curva IS

Tudo o que falta na equação (H) do modelo estrutural. **O que está no ar vive no
[`CLAUDE.md`](CLAUDE.md) da pasta** — aqui só entra o que ainda não foi feito, mais o que foi
medido e **não** entrou.

```
(H) H(t) = h1·H(t-1) + h2·gap(t-1) + d08 + d20 + ε

    gap = Selic − (juro real de 10 anos + meta), p.p. — a âncora da regra de juros
```

Estado em 2026-09-25 — 81 trimestres, 2006T2→2026T2:

| parâmetro | peso | margem | t (HAC 4) | t (MQ) |
|---|---|---|---|---|
| hiato do trimestre anterior | 0,8766 | ± 0,0700 | 12,52 | 18,37 |
| aperto do trimestre anterior | −0,0713 | ± 0,0336 | −2,12 | −2,44 |
| crise de 2008-2009 | −0,4807 | ± 0,4319 | −1,11 | −1,63 |
| pandemia de 2020 | −1,0760 | ± 0,7618 | −1,41 | −2,82 |

R² 0,870 · RMSE 0,636 · meia-vida de um hiato **6 trimestres** · efeito de longo prazo **−0,578**
· **Ljung-Box Q(4) p 0,070 e Q(8) p 0,261 — nenhum rejeita**.

Por MCMC (`bayes/is_bayes.py`), que é o que o simulador roda: mediana de `h2` −0,0709, HDI 90%
[−0,1205; −0,0230], **99,1%** da massa abaixo de zero; R² e RMSE idênticos aos do MQ; R-hat 1,0000,
zero divergências, pior distância ao MQ 0,04 desvio do posterior. **0,49% da massa tem `|h1| ≥ 1`**
(explosiva) — fica no posterior, porque tirá-la seria impor estacionariedade como priori, e em 12
trimestres o desenho mais explosivo dos mil gravados (`h1` 1,0053) leva um hiato de 1 p.p. a 1,065.

Convenção deste arquivo: **H#** pendência. Cada item diz se está bloqueado por dado, por decisão
ou por trabalho.

---

## 0. Duas decisões do usuário que fecham perguntas

**A medida de aperto é a Selic contra a âncora da regra de juros**, decidida em 2026-09-25 com a
medição ao lado (*"quero rodar a equação do hiato substituindo o gap com a inclinação pelo gap com
a Selic − (real NTN-B + meta), como na nossa equação de Selic"*). Até ali era a inclinação real
2a−10a, decidida em 2026-09-21. **As duas têm o mesmo neutro** — o juro real de 10 anos — e diferem
só na perna da política: o juro real de 2 anos do mercado, ou a Selic descontada da meta. A
diferença entre elas é exatamente `(Selic − meta) − rr_2a`, e as duas pernas correlacionam +0,875.

| aperto, 81 trimestres | h2 | t | **h2 × desvio** | R² | RMSE | LB(4) |
|---|---|---|---|---|---|---|
| inclinação 2a−10a | −0,164 | −2,62 | −0,167 | 0,8678 | 0,642 | **0,021** |
| Selic contra a âncora | −0,071 | −2,12 | **−0,185** | 0,8703 | 0,636 | **0,070** |

Os `h2` não se comparam — o gap oscila 2,60 e a inclinação 1,02 —, e por desvio da própria medida
os dois quase coincidem. O que decidiu não foi ajuste: **com a inclinação a Selic nunca chega ao
produto**, e uma (H) assim seria espectadora dentro do simulador. Com o gap, `(R) → (H)` é elo. De
brinde, o resíduo deixou de reprovar Ljung-Box, e o efeito de um ponto (−0,071) passou a ser
comparável com o do BC — e cai **dentro** da margem que ele publica (−0,165 a −0,053).

**O hiato em tempo real fica de fora**, por decisão explícita do usuário em 2026-09-21: *"use a
última série, não vou lidar com o problema de vintage agora."* É o item H1 abaixo, e continua sendo
a pendência de maior consequência da lista.

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

### H2 — A autocorrelação de um trimestre continua lá · *rebaixado em 2026-09-25*

Com a inclinação, Q(4) p 0,021 **rejeitava**. Com o gap, **p 0,070 e Q(8) p 0,261 — nenhum
rejeita**, e a aba passou a dizer "nada sobrando" nos quatro lugares em que fala do erro (a
asserção que exige os quatro concordando é a mesma, e o fio que exigia "ainda tem padrão" inverteu
junto). Mas a autocorrelação de primeira ordem é **0,30** — o padrão ficou menor, não sumiu, e o
teste passa por pouco. Parte dele vem de H1: um hiato suavizado pela fonte produz erro suavizado.

### H3 — As duas dummies de crise não são individualmente firmes · *medido, e é uma tensão real*

`d08` tem t −1,11 e `d20` tem t −1,41 sob HAC(4). Pelo t individual, nenhuma das duas sobreviveria.
**Mas tirá-las enfraquece o aperto**: `h2` vai de −0,0745 para −0,0589 e o t de −2,13 para −1,93,
com o RMSE subindo de 0,639 para 0,680 (amostra comum, na tabela da página). Com a inclinação o
efeito era maior — o t caía a −1,22 —, então o gap depende menos das duas marcas.

A leitura honesta é que elas não são estimativas do tamanho da crise — são o que impede dois
episódios que nenhuma política monetária explica de definirem o peso do resto. O HAC(4) é
severo com elas justamente porque são poucos trimestres consecutivos. **Decisão em aberto:** manter
como está (a escolha atual, e a do plano), ou substituir por uma dummy só de 2020, que é a que
carrega quase todo o efeito — os quatro maiores resíduos da amostra são os quatro trimestres de
2020, mesmo com `d20` dentro.

### H4 — O `h1` fica acima do intervalo que o BC publica · *medido, e provavelmente é H1*

O BC publica `b1 = 0,85` com IC 90% de [0,70; 0,95] — o nosso 0,877 está dentro. Mas o `t(MQ)` de
18,37 contra o `t(HAC)` de 12,52 mostra o quanto o erro correlacionado pesa aqui, e a suspeita é
que a persistência esteja inflada pela suavização da fonte (H1). Reestimar com o hiato real-time é
o que separa as duas hipóteses.

### H5 — Não há termo de condições financeiras · *previsto no BC, ausente aqui*

A eq. (2) do BC tem `−b3·rp_hat`, o prêmio de risco ciclicamente ajustado, com `b3 = 0,030` e IC
[0,027; 0,032] — estreito, portanto bem identificado lá. `modelo_painel.py` já constrói `rp_hat`
(CDS winsorizado, ajustado pela semielasticidade fiscal, filtrado por HP), então **o insumo existe
e é importável**. Não entrou porque o plano da pasta não o pede.

Vale notar o que isso significa para a comparação: parte do que o nosso `h2` mede pode ser condição
financeira, já que o aperto e o prêmio de risco andam juntos em crise.

### H10 — O gap perde força na década recente · *medido, e é a ressalva da troca*

As duas medidas do aperto não são histórias rivais — correlacionam 0,767, e postas no mesmo ajuste
nenhuma sobrevive (inclinação t −0,99, gap t −1,23). Mas elas **se separam por subamostra**, e ali
a inclinação ganha:

| subamostra | inclinação | gap |
|---|---|---|
| 2006T2–2016T2 | −0,153 (t −1,03) | **−0,200 (t −2,28)** |
| 2016T3–2026T2, sem a pandemia (n 32) | **−0,105 (t −2,94)** | −0,006 (t −0,44) |

A significância do gap na amostra cheia vem sobretudo de 2006–2016. Não há diagnóstico ainda do
porquê. Duas hipóteses a testar: (a) a Selic de 2017–2021 ficou muito abaixo da âncora por muito
tempo (o gap mínimo é −5,10 em 2020T4) sem que o hiato respondesse na proporção, o que seria o piso
de juro efetivo e não falha da medida; (b) o juro real de 10 anos carrega prêmio de maturidade que
variou no período (§2), o que desloca o neutro do gap e não o da inclinação, que tem o mesmo prêmio
nas duas pontas. **A aba não diz isso ainda** — está aqui para não se perder.

---

## 2. O que foi medido e está DESCARTADO

Não são pendências: são medições que fecham perguntas que voltariam sozinhas.

- **Taxa de juro de equilíbrio constante, ou quase.** Com `RR*` fixo em 4,5% ou com a neutra que o
  BC declara no RPM (4,50 → 4,75 em jun/2024 → 5,00 em dez/2024), `h2` sai em **−0,052 e −0,055**,
  com t de −1,44 e −1,45. Na amostra mais longa que cada uma permite (90 trimestres), pior ainda:
  −0,016 e −0,017, t −0,63 e −0,65. **A causa é medida:** o juro real ex-ante cai de 12,2% em
  2001T4 a −0,9% em 2020T4 e volta a 8,5%, e o hiato não tem essa tendência — um nível fixo não
  remove nada.
- **A mediana das 5 medidas do boxe do BC** (`modelo_agregado/data/modelo_neutra_pub.csv`): −0,075,
  t −1,61. E ela **para em 2024T2**, porque o boxe é de jun/2024 — não serve para o período
  corrente sem ser estendida.
- **A inclinação real 2a−10a** foi a medida até 2026-09-25 e continua medida ao lado, na tabela
  de candidatas e na de formas. Ela empata com o gap por desvio da medida e o supera na década
  recente (H10), e perdeu o lugar por uma razão de estrutura: ela é feita de dois preços de mercado,
  então a Selic do simulador não passaria por ela.
- **O filtro HP com cauda Focus ajusta MELHOR que a inclinação e que o gap** e mesmo assim não foi
  escolhido: −0,231 (t −4,42) contra −0,164 (t −2,62) e −0,071 (t −2,12), na mesma janela. Isso está na tabela da página em vez
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

### H6 — O neutro do aperto carrega o prêmio de maturidade · *ganhou peso em 2026-09-25*

Desde que o aperto virou `Selic − meta − juro real de 10 anos`, **o juro de 10 anos É o neutro da
conta** — não mais só uma leitura de contexto. E ele carrega o prêmio de maturidade medido acima
(0,9–1,1 p.p.), então o gap subestima o aperto nesse tanto, em nível. Como a equação não tem termo
constante, nível importa: descontar o prêmio muda o gap médio e, portanto, o repouso do hiato. É
também uma das duas hipóteses de H10. O que falta é medir o gap com o neutro descontado (7,56 − 1,1
≈ 6,45% hoje, confirmado pela Focus de 4 anos em 6,42%) e pôr a frase na aba, derivada do payload.

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
[`pendencias_taylor_eq.md`](pendencias_taylor_eq.md). **Desde 2026-09-25 H9 e R12 são literalmente
o mesmo item**: as duas equações medem distância até a MESMA âncora (`juro real de 10 anos + meta`),
então uma neutra estimada substituiria o juro de 10 anos nas duas de uma vez, e trocá-la numa só
desfaria a coerência que motivou a troca. A tabela de candidatas da §2 continua não cobrindo uma
neutra estimada que se mova e não olhe para o futuro.

Vale notar que **o BC usa duas neutras diferentes**, uma na IS e outra na Taylor (`rr_IS` e
`rr_TAY`, correlação 0,994, diferença média 0,12 p.p.) — então "estimar a neutra" é, no modelo dele,
estimar duas.

---

## 4. Ordem sugerida

1. **H1 é a pendência-raiz.** Ela é a única que pode mover `h1` e `h2` de verdade, e H2 e H4
   provavelmente são consequência dela.
2. **H10 e H6 andam juntos**: medir o gap com o neutro descontado do prêmio responde uma das duas
   hipóteses da fraqueza recente e põe o nível do neutro na aba.
3. **H3 depende de uma decisão**, não de trabalho.
4. **H5 entra se e quando o plano quiser o termo de condições financeiras** — o insumo já existe.
5. **H8 é pequeno e sai junto com P16 e E7.**
6. **H9 não tem data.** É intenção declarada do usuário, e o caminho barato passa por R11 na
   equação (R) — a mesma decomposição serve as duas.
