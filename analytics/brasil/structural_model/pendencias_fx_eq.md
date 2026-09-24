# Pendências — Equação (F), o câmbio trimestral

Estado do módulo [`equations/fx.py`](equations/fx.py), no padrão das outras quatro equações desta
pasta: o que está decidido, o que está aberto, o que já foi medido e não volta, e o que ainda não
foi feito. Números medidos em 2026-09-22.

```
(F) de(t) = dppp(t) + α + φ·de(t−1) + Σ β_c·z(Δc(t)) + ε

    de    100·Δlog(PTAX) no trimestre, pelo FECHAMENTO
    dppp  100·Δlog(IPCA/CPI) — o diferencial de inflação BR-US, coeficiente IMPOSTO em 1
    Δc    variação trimestral de cada canal
    φ     AR(1) na própria variação do câmbio
```

Estimada por Ridge, com λ escolhido por validação cruzada walk-forward (`min_train` 16 trimestres).
**81 trimestres, 2006T2→2026T2**, corte fixado em disco (`data/fx_fit_cutoff.json`).

| termo | β (em sd) | t (HAC 4) | contribuição acumulada | unidade nativa |
|---|---|---|---|---|
| risco fiscal (CDS de 5 anos) | +27,03 | **9,82** | −2,1 p.p. | +0,0906 por bp |
| dólar contra emergentes | +2,354 | 2,94 | +20,2 p.p. | +0,693 por ponto |
| carry sobre volatilidade | −0,577 | −1,35 | −0,5 p.p. | −2,275 por unidade |
| bolsa americana | +1,898 | 3,34 | **+39,8 p.p.** | +0,227 por 1% |
| commodities em dólar | −2,054 | −3,44 | −18,8 p.p. | −0,275 por 1% |
| câmbio do trimestre anterior | −0,087 | −1,32 | −7,0 p.p. | −0,087 |
| constante (α) | −0,035 | −0,08 | −2,9 p.p. | p.p./trimestre |
| diferencial de inflação | *imposto em 1* | — | **+58,0 p.p.** | |

R² **0,8115** · RMSE 3,59 p.p./trimestre · λ 0,0100 (o piso da grade) · **resíduo limpo**:
autocorrelação de primeira ordem −0,02, Ljung-Box Q(4) p 0,822 e Q(8) p 0,755. O câmbio andou
+86,8 p.p. de log na amostra (2,38×) e a soma das contribuições devolve +86,8 exatamente.

**Contra o modelo mensal que serve o FX Report** (n 245, 2006-02→2026-06, λ 0,0100, R² 0,6532), em
unidade nativa — é o número que se compara entre frequências, porque o `sd` se cancela:

| canal | trimestral | mensal | unidade |
|---|---|---|---|
| risco fiscal | +0,0906 | +0,0652 | p.p. de câmbio por bp de CDS |
| dólar contra emergentes | +0,693 | +1,027 | por ponto do índice |
| carry sobre volatilidade | −2,275 | −4,483 | por unidade de vol |
| bolsa americana | +0,227 | +0,173 | por 1% de log-retorno |
| commodities em dólar | −0,275 | −0,171 | por 1% de log-retorno |
| AR(1) | −0,087 | −0,130 | p.p. |
| α | −0,035 | −0,043 | p.p. por período |

**Os seis coeficientes têm o mesmo sinal nas duas frequências**, e o α é indistinguível de zero nas
duas — que é o que o offset de PPP existe para produzir. O R² sobe de 0,65 para 0,81 ao passar para
trimestral, o que é o esperado: parte do que é ruído mensal se cancela dentro do trimestre.

---

## 0. Cinco decisões que fecham perguntas

**Os 5 canais são herdados do mensal**, não reselecionados aqui — `fiscal`, `dxy_em`, `carry_vol`,
`sp500`, `icbr_usd`. O corte de 8 para 5 foi medido em frequência mensal e o plano da pasta declarou
a reseleção fora de escopo. Ver **F3**.

**Os níveis são trimestralizados pelo FECHAMENTO**, e só então diferenciados — é o que o plano
manda, e é o que mantém a coerência com o modelo mensal, que também lê fechamento de mês. Custa uma
divergência com o painel desta pasta, que é o item **F2**.

**A volatilidade do `carry_vol` é defasada um trimestre.** A janela de 126 pregões terminando em *t*
contém inteiro o trimestre que se quer explicar, então a variação do câmbio entraria dos dois lados
da regressão. Defasada, o denominador é predeterminado. Ver §2 para o que isso custa, medido.

**O diferencial de inflação entra como offset com coeficiente 1**, não como regressor estimado. A
informação sobre esse coeficiente vive em baixa frequência — no mensal, regredir a variação de *h*
meses do câmbio sobre o diferencial de *h* meses dá β entre 1,74 e 2,79, distinguível de 0 e **não**
distinguível de 1 em todos os horizontes testados. Impor é como uma regressão de alta frequência usa
essa informação.

**Este módulo não reescreve o mensal.** Importa `load_data`, `_standardize_ext`,
`walk_forward_lambda` e `fit_whole_sample` de
[`ridge_deviation_model.py`](../exchange_rate/models/ridge_deviation_model.py) e monta a amostra
trimestral por cima. O `fx_fit_cutoff.json` daqui é **separado** do `model_fit_cutoff.json` de lá:
reestimar um não pode mover o outro.

---

## 1. O que está aberto na forma atual

### F1 — A bolsa americana troca de sinal entre a correlação bruta e o coeficiente · *medido, e vale para o modelo mensal também*

**É a pendência mais importante desta equação, e ela não nasceu aqui.** A correlação bruta de
Δ`sp500` com a variação do câmbio é **−0,435** — S&P subindo vem com real mais forte, que é a
leitura intuitiva de *risk-on*. O coeficiente estimado é **+1,898**, com t 3,34. Sinal trocado, e é
o único dos cinco canais em que isso acontece:

| canal | corr. bruta com o câmbio | β estimado | |
|---|---|---|---|
| risco fiscal | +0,831 | +27,03 | mesmo sinal |
| dólar contra emergentes | +0,745 | +2,354 | mesmo sinal |
| carry sobre volatilidade | −0,086 | −0,577 | mesmo sinal |
| commodities em dólar | −0,561 | −2,054 | mesmo sinal |
| **bolsa americana** | **−0,435** | **+1,898** | **trocado** |

**O mecanismo está medido, e é colinearidade, não erro.** Δ`sp500` correlaciona **−0,574** com o
CDS e **−0,606** com o dólar contra emergentes. Acrescentando um controle de cada vez:

| regressores | β do sp500 | t |
|---|---|---|
| sp500 sozinho | **−3,542** | −4,25 |
| + dólar EM | +0,290 | 0,37 |
| + fiscal | +0,529 | 0,83 |
| + fiscal + dólar EM | +1,364 | 2,21 |
| o modelo inteiro | **+1,907** | 3,38 |

Lido em palavras: sozinha, a bolsa americana subindo vem com real mais forte, porque bolsa subindo
**é** *risk-on*, e *risk-on* comprime o CDS e enfraquece o dólar contra emergentes — os outros dois
canais. Segurados esses dois, o que sobra da bolsa move o real na direção oposta, que é a leitura de
atração de capital para ativo americano. É defensável, e é **condicional**.

**A consequência prática é sobre a barra de decomposição, não sobre o ajuste.** A contribuição
acumulada de +39,8 p.p. faz da bolsa americana o maior contribuinte isolado dos +86,8 p.p. de
desvalorização — 46% dela. Quem lê a barra como causa independente lê errado, e a barra não tem como
dizer isso sozinha.

**E isto vale igualmente para o modelo mensal que já está publicado no FX Report**: lá a correlação
bruta é **−0,428** e o β é **+0,764**, exatamente o mesmo padrão. Não é artefato da frequência
trimestral nem desta amostra.

Duas coisas a fazer, nenhuma delas decidida: escrever o aviso junto da decomposição (barato), e
testar se um proxy de *risk-on* mais direto — VIX, ou o próprio S&P ortogonalizado contra os outros
dois canais — resolve a leitura em vez de só documentá-la.

### F2 — A convenção de trimestralização diverge da do painel · *medido; rebaixado a registro em 2026-09-22*

Esta equação mede o câmbio pelo **fechamento** do trimestre. A coluna `de` do painel, que é o `F(t)`
que a curva de Phillips e a equação de bens industriais usam, é a variação da **média** do trimestre.
São duas séries diferentes: desvio-padrão **8,32 contra 6,76**, e o próprio plano da pasta pede as
duas coisas em lugares diferentes — fechamento aqui, média no painel.

Enquanto cada equação é estimada sozinha contra dado observado, isso não é erro: cada uma usa a
convenção que o seu próprio desenho pede. **Viraria erro no simulador**, que propagaria `F` de (F)
para (I) — a equação de inflação foi estimada com a variação da média e receberia a do fechamento.

**E o simulador saiu de escopo em 2026-09-22, por decisão do usuário.** Então hoje não há nada que
ligue as duas convenções, e este item deixou de ser decisão a tomar: é inconsistência declarada, com
o tamanho medido. Ele volta a ser decisão no dia em que qualquer coisa propagar a saída de uma
equação para a entrada de outra — uma projeção, um cenário, um fechamento parcial.

O que está medido: rodar (F) inteira na convenção de média dá R² 0,7950 e α −0,210 (t −0,48), contra
0,8115 e −0,035 (t −0,08) no fechamento. **O RMSE das duas não é comparável** — a dependente é outra,
e mais lisa.

**Três saídas, se um dia ela for necessária, e a escolha não é de quem implementa:** (i) o painel
carrega as duas e cada equação declara a sua, que é o que já acontece de fato (`de` e `de_fim`
existem) — e é o estado em que a decisão de 2026-09-22 nos deixou; (ii) tudo vai para fechamento;
(iii) tudo vai para média. `comparar()` mantém a coluna de média estimada ao lado para a diferença
seguir visível.

### F3 — O corte de 8 para 5 canais não foi refeito em trimestral · *fora de escopo declarado*

Os 5 canais vêm de uma seleção feita em frequência mensal. O plano da pasta declarou a reseleção
fora de escopo e nomeou a alternativa medida caso o `carry_vol` saísse instável: dividi-lo em gap de
política mais volatilidade, cujos *loaders* já existem. **Ele saiu fraco, não instável** — β −0,577
com t −1,35, o único dos cinco que não é distinguível de zero, e contribuição acumulada de −0,5 p.p.
Ver F9.

### F4 — Volatilidade implícita de opções · *insumo ausente, caminho pronto; metade do argumento caiu em 2026-09-22*

A vol defasada resolve a simultaneidade da **estimação**, e não resolvia a da **simulação**: vol
realizada continua sendo função da história da própria dependente, então num cenário fechado ela teria
de ser atualizada a partir do caminho simulado ou declarada como premissa na tela. **Com o simulador
fora de escopo, essa metade deixou de ter consumidor** — e a metade que sobra, a da estimação, já
está resolvida pela defasagem.

O que mantém o item vivo é conceitual e não é um defeito em aberto: o prêmio de carrego é uma razão
entre juro e **risco à frente**, e vol implícita é esse objeto — prospectiva, observável em *t*, e
não função de realização passada. **Não há tabela dela no banco.** `VOL_SOURCE='implicita'` já existe no módulo e
levanta com a mensagem do destino recomendado (`macro_brasil.cmb_vol_implicita`, pelo caminho do
conector Bloomberg que já existe), para a troca ser de série e não de equação.

### F5 — Ridge não tem erro-padrão, e os `t` da tabela são de MQ · *limitação declarada, hoje inofensiva*

Ridge é estimativa pontual: não há distribuição a resumir. Os `t` publicados são de **MQ com HAC(4)
sobre o mesmo desenho**, e eles são legíveis apenas porque o λ escolhido pousa no **piso da grade**
— a penalidade é nominal. Isso não é empate: a MSE fora da amostra é monótona crescente ao longo dos
25 pontos da grade, de **17,34 em λ=0,01 até 61,55 em λ=1000**. A validação está pedindo a
penalidade mais fraca disponível, exatamente como no mensal.

O módulo carrega o campo `t_valem`, que fica falso se o λ um dia subir. Se subir, esta coluna sai da
página em vez de continuar sendo impressa.

### F6 — Não há janela móvel aqui · *decisão de tamanho de amostra*

O modelo mensal reestima numa janela móvel de 60-72 meses, e é assim que ele mostra mudança de
regime. Em trimestral a mesma ideia pediria 20-24 trimestres de janela sobre 81 observações: sairiam
~57 janelas com 6 regressores cada, quase todas sobrepostas. **Não foi feito**, e o que está no
lugar é a tabela de formas de `comparar()`. Se a aba precisar de leitura de regime, o caminho mais
honesto é a janela móvel do **mensal**, que tem amostra para isso.

### F9 — O `carry_vol` é o canal mais fraco · *medido, não resolvido*

β −0,577, t −1,35, correlação bruta com o câmbio de apenas −0,086, contribuição acumulada de −0,5
p.p. em 81 trimestres. É o único dos cinco que não passa. Duas leituras possíveis e não separadas: o
canal de juro simplesmente não move o câmbio nesta frequência, ou a construção (carry dividido por
vol) mistura duas coisas que deveriam entrar separadas — que é a alternativa já nomeada em F3.

---

## 2. O que foi medido e está DESCARTADO

Não são pendências: são medições que fecham perguntas que voltariam sozinhas.

- **Defasar a volatilidade não mexe em mais nada.** Quatro dos cinco canais mudam na terceira casa
  (fiscal +27,03 → +26,66; dólar EM +2,354 → +2,394; bolsa +1,898 → +1,928; commodities −2,054 →
  −2,090). O que muda é o canal que ela toca: `carry_vol` vai de **−0,162 para −0,577**. O R² quase
  não se mexe (0,8115 contra 0,8087). Vale notar que a direção da mudança é o **contrário** da
  história mecânica simples — desvalorização eleva a vol contemporânea e derruba o `carry_vol`, o
  que deveria inflar o coeficiente negativo, e infla o contrário. Nenhum dos dois é significativo,
  então não se deve ler mais do que isso na diferença.
- **Tirar o offset de PPP melhora um fio o ajuste e devolve a tendência para o α**: R² 0,8136 contra
  0,8115, e α salta de −0,035 (t −0,08) para **+0,685 (t 1,59)**, ou ~2,7 p.p. ao ano de deriva não
  explicada. O offset leva +58,0 p.p. dos +86,8 — **67% da desvalorização acumulada é diferencial de
  inflação**, e sobram +28,8 p.p. (1,33×) de desvalorização real. *Ressalva honesta:* com 81
  trimestres o α sem offset também não é significativo a 5%, então o argumento aqui é mais fraco do
  que no mensal, onde n é 245. O offset continua justificado pelo argumento de baixa frequência de
  §0, não por este t.
- **Tirar o AR(1) custa pouco**: R² 0,8050 contra 0,8115. O coeficiente é −0,087 com t −1,32 e
  correlação bruta de −0,027 com a dependente — em trimestral quase não há persistência a capturar,
  ao contrário do mensal (−0,130).
- **O λ não é escolha de fronteira.** A curva de validação é monótona em toda a grade (17,34 →
  61,55), então a escolha do piso não depende de onde a grade começa; alargá-la para baixo só tornaria
  o resultado mais literal.
- **A escala não centra**, e isso já estava medido no módulo mensal: a média de uma coluna em
  diferença é uma deriva, e subtraí-la injeta sinal constante em todo trimestre. Não muda o ajuste
  (o intercepto do Ridge não é penalizado) e muda muito a **atribuição**.

---

## 3. O que ainda não foi feito

### F7 — A aba de Câmbio · *RESOLVIDO em 2026-09-22*

A aba existe, e saiu junto com a de Juros. Traz a variação observada contra a conta, a decomposição
por trimestre em sete parcelas (as cinco do modelo, o diferencial de inflação e um bloco de
persistência mais constante), a tabela de pesos com a coluna de acumulado, e um bloco de método com
as formas testadas, o modelo mensal em unidade nativa e a escolha da penalidade.

**F1 ficou no fluxo da página, não dentro de um fold** — é a ressalva de leitura sobre a coluna de
acumulado, e escondê-la seria o mesmo que não escrevê-la. O canal que troca de sinal é **derivado**
(`troca_sinal` compara o sinal do peso com o da correlação bruta), e a interpretação econômica vive
num mapa por canal: se um dia outro canal virar, a página mostra a tabela de degraus e **não** a
explicação da bolsa.

### F8 — Quando avançar o corte fixado · *convenção a declarar*

`data/fx_fit_cutoff.json` está em **2026T2**. Ele existe para que uma regeração de rotina não
reestime o modelo por acidente, e avançá-lo é decisão explícita (`corte(force=True)`). O que falta é
a convenção: o mensal avança quando o usuário decide; aqui ninguém disse ainda. Enquanto não houver
regra, o número na página é do corte fixado, e a página tem de dizer isso.

### F10 — Margem do efeito acumulado de cada canal · *não é a mesma álgebra das outras três*

As equações (I), (E), (H) e (R) têm um item de método delta (P16, E7, H8, R8). Aqui o objeto
análogo — a contribuição acumulada `β_c · Σ z_c` — não tem margem, e **Ridge não dá uma de graça**.
O caminho é *bootstrap* em blocos sobre a amostra, não o método delta. Fica registrado para não ser
confundido com aquele item.

---

## 4. Ordem sugerida

1. **F1** — o aviso já está na página desta equação, no fluxo e não dentro de um fold. O que
   **falta** é levá-lo ao FX Report publicado, onde a mesma barra de decomposição aparece sem ele; e
   testar um proxy de risco mais direto, que resolveria a leitura em vez de só documentá-la.
2. ~~**F2** — a convenção.~~ Deixou de ser decisão pendente em 2026-09-22, com o simulador: nada
   liga as duas convenções hoje. Fica como registro.
3. **F8** — a convenção do corte, que é uma frase.
4. **F3/F9** — separar o `carry_vol` em gap de política e volatilidade, se o canal fraco incomodar.
5. **F4** — a vol implícita, quando a série existir.
6. **F5**, **F6**, **F10** — registro; nenhum bloqueia. **F7** está fechado.
