# Pendências — Equação (E), expectativas

Tudo o que falta na equação (E) do modelo estrutural. **O que está no ar vive no
[`CLAUDE.md`](CLAUDE.md) da pasta** — aqui só entra o que ainda não foi feito, mais o que foi
medido e **não** entrou.

**A forma no ar é a do plano da pasta, e nada além dela.** Em 2026-09-21 a equação foi primeiro
construída com uma forma mais rica — segunda defasagem, o trimestre anualizado no lugar dos doze
meses, o câmbio e ajustes de trimestre — sem que essa mudança de especificação tivesse sido pedida.
Ela foi desfeita no mesmo dia, a pedido do usuário, e **as medições sobreviveram aqui**: elas são o
material da decisão, que vem depois de todas as equações estarem de pé. Nada desta lista entra sem
essa decisão.

```
(E) E(t) = e1·E(t-1) + e2·I12(t) + (1-e1-e2)·Meta(t) + ε
```

Estado em 2026-09-21 — 98 trimestres, 2002T1→2026T2:

| parâmetro | peso | margem | t (HAC 4) | t (MQ) |
|---|---|---|---|---|
| expectativa do trimestre anterior | 0,5860 | ± 0,1573 | 3,72 | 7,51 |
| IPCA acumulado em 12 meses | 0,1603 | ± 0,0746 | 2,15 | 4,96 |
| **peso da meta** (conta de sobra) | **0,2537** | — | — | — |

R² 0,778 · RMSE 0,569 · erro médio 0,339 · meia-vida de um desvio **2 trimestres** · repasse de
longo prazo **0,387** · **Ljung-Box Q(4) 32,1 (p 0,000002) e Q(8) 37,8 (p 0,000008)**.

Convenção deste arquivo: **E#** pendência. Cada item diz se está bloqueado por dado, por decisão ou
por trabalho.

---

## 0. A procedência dos números desta lista

A escada de leituras abaixo foi medida numa **amostra comum de 95 trimestres (2002T4→2026T2)**, e
não nos 98 de hoje: as leituras com duas defasagens precisam de dois trimestres a mais de história,
e rodar todas na mesma janela é o que torna as linhas comparáveis entre si. Por isso a linha "a
forma do plano" naquela tabela lê R² 0,780 e RMSE 0,575, e não os 0,778 / 0,569 de hoje — **a
diferença são os três trimestres, não a especificação**. Qualquer decisão tomada a partir dela deve
ser reconfirmada na janela que estiver valendo na hora.

---

## 1. O que está aberto na forma atual

### E1 — O resíduo ainda tem padrão · *não bloqueado, e é a pendência-raiz desta lista*

Os dois Ljung-Box rejeitam com folga (p 0,000002 e 0,000008), e a autocorrelação do erro é
**0,393** em um trimestre, **−0,234** em dois e **−0,318** em três. O padrão está declarado na
página, no cartão de erro típico, na tabela de erro e na ficha de abertura — não está escondido, e
há asserção exigindo que as quatro frases digam a mesma coisa que o teste mede.

**O que isso muda na leitura, e o que não muda.** Não invalida os pesos: a margem deles já é a
conservadora (HAC 4), que existe exatamente para aguentar erro correlacionado. O que muda é a
leitura do **erro típico**: 0,569 p.p. é o piso do que uma forma mais rica pode melhorar, e não o
acaso irredutível da expectativa.

**Parte do padrão é do objeto, não da conta.** O regressando é uma expectativa de doze meses lida a
cada três e o regressor é um acumulado de doze meses amostrado a cada três: trimestres vizinhos
falam do mesmo período em nove dos doze meses, então há autocorrelação por construção. Quanto do
0,393 é isso e quanto é falta de termo é a pergunta que E2–E5 respondem.

### E2 — A inflação do trimestre anualizada no lugar dos doze meses · *medido, fora da forma*

Trocar `I12(t)` pela inflação do **trimestre** em taxa anual, `(1+π/100)⁴−1`:

| leitura | R² | RMSE | Ljung-Box Q(4) |
|---|---|---|---|
| três termos, inflação de 12 meses (a forma no ar) | 0,780 | 0,575 | **p 0,000** |
| três termos, trimestre anualizado | 0,876 | 0,431 | **p 0,017** |

**E o achado que vale mais que o ganho de ajuste:** postos **lado a lado** na mesma conta, os doze
meses ficam com 0,024 (t 0,9) e o trimestre anualizado com 0,094 (t 2,7), e o R² não se move.
A expectativa de doze meses reage ao **trimestre que acabou**, não ao ano que passou — o contrário
do que a intuição de "expectativa adaptativa" sugere.

**Ressalva de unidade:** anualizar é `(1+π/100)⁴`, que **não comuta** com média ponderada. Em
2002T4, com 6,6% no trimestre, anualizar compondo dá 29% e multiplicar por 4 dá 26%.

### E3 — Segunda defasagem da expectativa · *medido, fora da forma*

`e1b = −0,1882` (t −3,15). Entra **negativa**, o mesmo perfil em corcova da regra de juros do BC
(t₁ 1,48, t₂ −0,58). Sozinha leva o Ljung-Box de 0,017 para 0,045: melhora sem resolver.

Consequência de implementação, se um dia entrar: a meia-vida deixa de ser uma exponencial só e tem
de ser **simulada**, não lida da maior raiz. O `_meia_vida()` já é simulado por isso, e continua
valendo com uma defasagem só.

### E4 — Câmbio em (E) · *medido, fora da forma — e o de maior consequência*

`e3 = 0,0183` (t 2,11), fora da restrição de soma-um: uma desvalorização de 10% levanta a
expectativa em 0,18 p.p. no impacto e **0,67 p.p. acumulado**. Não tem problema de calendário —
câmbio é observado todo dia, e a pesquisa do trimestre viu o mesmo que a regressão vê.

**O que ele custa é a ordem de solução do modelo.** O plano resolve `H → I → E → R → F` dentro do
trimestre; com o câmbio em (E) a ordem passa a ser **`H → I → F → E → R`**. Continua recursiva —
(F) usa a inflação de (I) e não usa a expectativa, então nada vira ponto fixo —, mas é uma decisão
sobre o modelo inteiro, não sobre uma equação. **Por isso este item não é uma troca local: ele
precisa de (F) estimada antes de valer a pena discutir.**

### E5 — Ajustes de trimestre soma-zero · *medido, fora da forma*

Três dummies pela mesma codificação de (I) (`1{Q=q} − 1{Q=4}`). São o que fechava o diagnóstico na
forma rica: Q(4) de 0,145 para **0,433**.

**Aqui elas significam o CONTRÁRIO do que significam em (I)**, e é isso que precisa de decisão. Em
(I) corrigem a estação do **regressando** — inflação trimestral é sazonal, e isso é fato do preço.
Em (E) o regressando tem amplitude sazonal de **0,27 p.p.**, quase nada, e o **regressor** tem
**4,47**: as dummies tirariam a estação de um insumo que a expectativa, sendo de doze meses,
corretamente ignora.

Isso é medido, não interpretação: o padrão estimado (−0,19 / −0,04 / +0,22 / +0,02) correlaciona
**0,800** com `−e2 × sazonal do regressor` e bate nos dois trimestres significativos (T1 −0,192
contra −0,222 previsto; T3 +0,217 contra +0,269).

**Nota de dependência:** o efeito é do regressor, então ele existe com o trimestre anualizado (E2) e
some quase todo com os doze meses, que já são a soma de quatro estações. E5 sem E2 não tem o que
corrigir.

---

## 2. O que fica para quando o modelo fechar

### E6 — Qual objeto é `I12(t)` quando as contas rodarem juntas · *sem gatilho desde 2026-09-22*

A especificação pede a série **publicada** (SGS 13522), e é ela que está no ar. Se as equações algum
dia rodarem juntas, porém, o que (I) produz é inflação **do trimestre** por grupo, e o acumulado de
doze meses do modelo é o **encadeamento** dela. O simulador, que era o que faria isso acontecer, saiu
de escopo em 2026-09-22 — então este item não tem mais gatilho, e o número medido abaixo é o que
justifica não se preocupar com ele quando tiver.

Os dois não são o mesmo objeto, mas a diferença é pequena e está medida: encadear quatro trimestres
da nossa `pi_q` reproduz a série publicada com **erro médio 0,0025 p.p. e máximo 0,0052**. (Somar os
quatro em vez de encadear erra 0,149 em média e 0,861 no máximo — sessenta vezes mais, e é por isso
que o gabarito existe.)

A decisão é declarativa e tem de aparecer na tela: em simulação a equação passa a ler o encadeado,
porque ler a série publicada do futuro é impossível.

### E7 — Margem e t para o peso da meta · *adiado por escolha, mesma álgebra do P16 de (I)*

O peso da meta é `1 − e1 − e2` e sai na tabela como conta de sobra, com margem e t em travessão.
Ele **tem** variância e ela é calculável da matriz de covariância dos dois: `Var(1 − 1'β) = 1'V1`,
com `V` já em mãos e o sinal cuidado. É o mesmo item que o
[`pendencias_philips_eq.md`](pendencias_philips_eq.md) registra como **P16** para o peso da
expectativa — se um for construído, o outro sai junto, porque a conta é a mesma.

### E8 — Dummies de crise · *previstas no plano, nunca implementadas*

O plano prevê `d08` (2008T4–2009T4) e `d20` (2020T1–2020T4) nas equações, estimadas com e sem. (E)
não as carrega. **Há um argumento explícito para não carregar**, e ele precisa ser decidido em vez
de herdado: é nas crises que esta equação é informativa — o maior resíduo da amostra é **2002T4**,
a desancoragem da eleição —, e uma dummy ali compra ajuste apagando justamente o episódio que
identifica a sensibilidade da expectativa.

---

## 3. O que foi medido e está DESCARTADO

Não são pendências: são medições que fecham perguntas que voltariam sozinhas.

- **Não é a suavização da Focus.** A série publicada é suavizada por construção, o que poderia
  fabricar persistência sozinho. Com a série **não** suavizada o padrão é o mesmo e um pouco pior
  (Q(4) p 0,004 contra 0,009 na forma de três termos com o trimestre). As duas correlacionam
  **0,9967**.
- **Não é a mistura da meta.** O padrão de calendário é **maior** quando a meta está parada: 0,450
  de amplitude nos 61 trimestres sem transição contra 0,161 nos 34 com, e **0,611** na década de
  meta fixa em 4,5%.
- **Não é olhar um mês à frente.** O IPCA de um mês só sai no meio do mês seguinte, então a pesquisa
  do trimestre *t* não viu o último mês de *t*. Trocando o regressor pelo que ela de fato tinha
  visto, o peso vai de 0,110 para 0,114 e o Ljung-Box melhora — o resultado não é um mês de
  vantagem.
- **A meta ajustada de 2003 não muda nada.** `inflc_meta` (SGS 13521) traz a meta do CMN já revisada
  — 4,0% para 2003 e 5,5% para 2004 —, e não a *meta ajustada* de 8,5% que o BC perseguiu depois da
  carta aberta. Substituindo, o RMSE fica **igual** (0,3765 contra 0,3751 — a do CMN é levemente
  melhor), os coeficientes andam dentro da margem e o resíduo de 2003 **piora** (erro médio 0,76
  contra 0,67). Fica a do CMN, que é a publicada.
- **Cortar na janela de (I) muda a leitura, e para pior.** A amostra de (E) começa antes da curva de
  Phillips porque (E) não usa hiato. Recortando em 2003T4: inércia 0,728 → 0,851, inflação 0,110 →
  0,054, meta 0,163 → 0,095 (medido na forma rica). Sem o episódio de 2002, que é o que identifica a
  sensibilidade, a equação vê uma expectativa mais inerte e menos sensível.

---

## 4. Ordem sugerida

1. **E1 é a pendência-raiz**, e E2 é a primeira candidata a resolvê-la — é a de maior ganho medido
   (RMSE 0,575 → 0,431) e a que carrega o achado sobre o que a expectativa de fato lê.
2. **E5 depende de E2** e não faz sentido sozinha.
3. **E4 espera (F)**, porque o que ele muda é a ordem de solução do modelo inteiro.
4. ~~**E6 entra com o simulador**~~ — que saiu de escopo em 2026-09-22. Sem gatilho.
5. **E3, E7 e E8** são independentes e pequenas.
