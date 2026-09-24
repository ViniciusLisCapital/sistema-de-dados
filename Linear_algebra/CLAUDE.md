# Linear_algebra — geometria da regressão

Ferramenta de **estudo**, não relatório: não lê o MySQL, não entra em `domain/dashboards/manifest.yaml`
e não tem `generate_report.py`. `regression_geometry.html` é autocontido (Plotly do CDN) — abrir com
duplo clique.

| arquivo | o que é |
|---|---|
| `regression_geometry.html` | o dashboard, duas abas: **2D — ℝ²** (n=2) e **3D — ℝ³** (n=3) |
| `tests/test_regression_geometry_js.js` | `node Linear_algebra/tests/test_regression_geometry_js.js` — 549 asserções |

O teste **extrai as fatias `LINALG` e `GEO` do próprio HTML entregue** e as executa, em vez de manter
uma cópia da matemática. Ele aceita um caminho por argumento, que é o que permite rodar o mesmo
harness contra um mutante.

## O que o dashboard mostra

Cada aba tem **dois gráficos que respondem perguntas diferentes** e é fácil confundi-los:

- **Espaço das observações** — um eixo por observação, cada coluna de dados é um vetor. É aqui que
  mínimos quadrados vira projeção ortogonal: ŷ é o ponto do espaço das colunas mais próximo de y, e
  `e = y − ŷ` é perpendicular a ele.
- **Espaço das variáveis** — o gráfico de dispersão de sempre, um eixo por variável. Existe para
  ligar a figura nova à que o leitor já conhece; na aba 3D ele muda de cartesiano para cena 3D
  conforme x₂ entra, porque a dimensão dele é o **número de regressores**, não o de observações.

Mais: painel de números (β̂, cos²θ, R² centrado, ‖e‖, graus de liberdade, det(XᵀX), menor ângulo
entre colunas, máx |xⱼᵀe|), as matrizes das equações normais com os valores correntes, e um card
"o que testar" com quatro ou cinco experimentos.

## Decisões que não se leem no código

**Os eixos são travados em escala 1:1** — `scaleanchor`/`scaleratio` em 2D, janela cúbica explícita
em 3D. Sem isso o ângulo reto não aparece reto, que é a única coisa que a figura existe para mostrar.
Medido em Chrome: com ranges explícitos e iguais, `aspectmode` `'cube'` e `'data'` resolvem os mesmos
vãos — a garantia está no **range**, não na string, e é assim que o teste afirma.

**A janela 3D é explícita porque a decomposição sequestraria o autorange.** No preset colinear as
parcelas β̂ⱼxⱼ medem ~1.157 contra um ŷ de 3,54 (327×); deixar o Plotly enquadrar sozinho colapsa
plano, vetores e resíduo num ponto. Com o cubo fixo, as setas saem dele — que é a leitura certa —, e
a linha de leitura imprime a razão medida.

**São dois R², e eles não são intercambiáveis.** `cos²θ = ‖ŷ‖²/‖y‖²` é o não centrado, sempre
definido e geométrico. O centrado só aparece quando há coluna constante no espaço das colunas; sem
intercepto ele sai como `n/d` com o motivo, porque não é comparável. `hasConst` aceita qualquer
coluna constante não nula, não só a de 1s.

**O preset "quase colineares" é calibrado, não escolhido.** `x₂ = (1,01, 2,01, 4,03)` dá ângulo de
0,066° com x₁, det 0,0006, β̂ = ±250 e move β̂ 248× mais que o caso bem condicionado sob a mesma
perturbação de y. Os limiares da §6 do teste vêm dessa medição — mexer no vetor sem refazer a medição
esvazia as asserções, e há um guarda que liga os dois.

**A caixa "mostrar decomposição" fica na tela, desligada, quando p = 1**, com o motivo no `title`:
com uma coluna só, β̂₁x₁ *é* o próprio ŷ. Ao invalidar, o estado cai de volta — marcada-e-inerte é
pior que cinza.

**Os números da prosa saem sem zeros de cauda** (`fc()`), porque `toFixed(3)` de 10 imprime `10.000`
e isso lê como dez mil em português. As matrizes e os KPIs mantêm casas fixas, onde o alinhamento
vale mais.

## Verificação

Além do harness, este arquivo foi confirmado em **Chrome headless real** (CDP, ver
[[project-browser-verification]]): 37 sondas, zero exceções, incluindo layout resolvido, troca de
aba, troca de cartesiano para cena 3D no mesmo div, e os casos singular e saturado. A matemática e os
guardas foram verificados contra **30 mutantes, todos mortos**; um 31º foi descartado por ser
equivalente (o `aspectmode` acima).

## Pendências

- Nada aberto. Se ganhar uma terceira aba (n > 3 não tem figura, mas caberia uma tabela de
  diagnóstico), a fatia `LINALG` já serve — ela não assume dimensão.
