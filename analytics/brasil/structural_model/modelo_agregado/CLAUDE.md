# analytics/brasil/structural_model/modelo_agregado/ — Contexto para o Claude

Réplica do **modelo agregado semiestrutural do BC** (boxe do RI de jun/2024) — estimada, decomposta
e validada contra o que o BC publica. **Não alimenta nenhum dashboard.** Morou em
`analytics/brasil/monetary_policy/` até 2026-09-24, quando aquela pasta passou a guardar só o
relatório; veio para cá porque o Modelo Estrutural é quem ainda a usa:

| quem | importa |
|---|---|
| `../generate_report.py`, `../equations/taylor.py` | `modelo_agregado.BCB`/`BCB_IC`/`CAIXA` (as modas e intervalos publicados pelo BC) |
| `../panel.py`, `../equations/is_curve.py`, `../planilha_curvas.py` | funções do `modelo_painel.py` (`q`, `serie`, `hp`, `cauda_juro_real`, `para_q`…) |

O relatório de Política Monetária não importa nada daqui: as três funções de leitura que ele usava
(`q`, `serie`, `focus_anual`) foram copiadas para `monetary_policy/dados.py`. O único caminho no
sentido contrário é `antecipa_modelo.py`, que parte do backtest da Focus de lá.

## Como rodar

A estimação leva minutos e depende de MySQL, IPEADATA e do anexo do RPM:

```powershell
uv run python analytics/brasil/structural_model/modelo_agregado/modelo_painel.py     # 2 painéis + sigma calibrado
uv run python analytics/brasil/structural_model/modelo_agregado/modelo_agregado.py   # estima, decompõe, valida
uv run python -m analytics.brasil.structural_model.modelo_agregado.antecipa_modelo   # backtest com o modelo, 4 variantes
uv run python tests/test_eq5_expectativas.py                        # 19 asserções (eq. 5)
```

| Módulo | O que faz |
|---|---|
| `modelo_painel.py` | Painel trimestral dos insumos. Escreve **dois**: `_est` (HP até 2023T4, fiel ao conjunto de informação do boxe — o único em que comparar parâmetros é legítimo) e `_full` (HP até hoje, para estender os estados e partir daí nos cenários). |
| `modelo_agregado.py` | Espaço de estados + estimação + decomposições + simulador + validações. `rodar()` grava tudo em `data/`. |
| `antecipa_modelo.py` | O modelo tentando antecipar a projeção do Copom, ao lado do delta da Focus que o relatório usa. Não grava nada. |

`data/` é versionada de propósito: `rodar()` sempre re-estima (não há caminho barato para recriar só
as séries derivadas) e `tests/test_eq5_expectativas.py` roda self-contained a partir de
`modelo_painel_full.csv` + `modelo_params.json`.

## O que o modelo é

**Equações**: transcritas na docstring de `modelo_agregado.py`, com a numeração do boxe, e na seção
"O modelo, equação por equação" do Apêndice do relatório de Política Monetária enquanto ele existiu
(até 2026-09-24), lá com os coeficientes estimados no lugar dos símbolos. As fórmulas são **imagem** no PDF — `pdfplumber`/`pymupdf` extraem o texto ao redor mas
perdem a matemática; foram lidas renderizando as páginas 97-101 em PNG.

**No filtro**: Phillips de livres (1), IS (2), Taylor (3), UIP (4), observação do hiato (6)-(9), por
máxima verossimilhança restrita. As prioris uniformes do BC entram como caixa e a única informativa
— a Beta de β₃ — como penalidade, o que faz a moda a posteriori coincidir com MQV restrita, sem MCMC.
Estados: `[h, h₋₁, sʰ, rr_IS, rr_TAY]`.

**Fora do filtro, mas no simulador**: a equação (5). Os três φ vêm de `estimar_eq5()`, em mínimos
quadrados não lineares — daí a coluna de método na tabela de validação.

**Não implementado**: o bloco de preços administrados e o hiato mundial β₄ (0,054, IC [0; 0,23] —
decisão explícita do usuário).

## O que reproduz

| | resultado |
|---|---|
| Parâmetros no IC 90% publicado | **17 de 22** (15 de 19 no filtro + 2 de 3 dos φ) |
| Hiato latente vs. `pm_hiato_produto` | corr **0,990**, sd 1,73 vs 1,73, n=81 |
| r* vs. coluna "Modelos BC" publicada | corr **0,906** |
| **Nosso motor com as modas do BC vs. IRF publicado** | erro absoluto médio **0,030 p.p.**, pico no mesmo T12 |
| β₂ (juro real) | 0,430 vs 0,44 |

**A escada de validação do IRF.** O `C2 Boxe3 Graf 4B` publica três respostas, uma por conjunto de
canais ligados, e o simulador tem exatamente essas três configurações:

| configuração | nosso pico | coluna publicada | pico dela | erro \|médio\| |
|---|---|---|---|---|
| `so_demanda` | −0,055 (T6) | "Expectativa IPCA e câmbio fixos" | −0,230 (T11) | 0,113 |
| `com_expectativa` (+ eq. 5) | −0,122 (T9) | "Câmbio fixo" | −0,300 (T12) | 0,105 |
| `completo` (+ eq. 4) | −0,119 (T8) | modelo cheio | −0,270 (T4) | 0,130 |
| **mesmo motor, modas do BC** | **−0,251 (T12)** | "Câmbio fixo" | −0,300 (T12) | **0,030** |

A última linha separa as duas perguntas: com os parâmetros publicados o motor reproduz o IRF do BC
dentro de 0,03 p.p., **então o que sobra de diferença é parâmetro estimado, não implementação**. Com
os nossos a transmissão é cerca de metade, e a causa é conjunta — trocar β₁, α₄ e α₁ᴵ pelos do BC ao
mesmo tempo faz o IRF *passar* de −0,30 para −0,56, então nenhum isolado explica a diferença.

O canal de câmbio quase não aparece no nosso (−0,119 contra −0,122 sem ele) porque α₃ = 0,0024 contra
0,011 do BC e, principalmente, porque falta o bloco de administrados: no modelo deles o repasse
cambial dos administrados é 1,65 p.p. por 10% de depreciação contra 0,72 dos livres.

### As 5 que ficam fora, com diagnóstico

- **α₁ᴵ = 0,054 contra 0,38** — a substantiva. Nossa Phillips ficou muito mais prospectiva, e com
  ela choques propagam menos. A hipótese de que a ausência da (5) explicava isso **não se
  confirmou**: com a (5) resolvida no simulador o α₁ᴵ do filtro não se move (π^e continua sendo
  dado observado ali). Só entra em teste se a (5) for para dentro do filtro.
- **φ₂ = 0,211 contra 0,11** — no sentido oposto ao de α₁ᴵ: a nossa expectativa é o dobro mais
  sensível à previsão do modelo. Estimador diferente do deles, e máximo interior.
- **α₄ = 0,0706** contra o piso 0,072, **θ₂ = −0,659** e **γ do Caged = 0,802** — marginalmente fora.

**O multiplicador não é a estatística robusta.** β₂/(1−β₁) sai 1,64 contra 2,93, e a diferença é
inteiramente β₁ (0,738 vs 0,85) — que está *dentro* do intervalo deles. Perto de 0,85 o multiplicador
muda ~17% por 0,01 em β₁.

## A equação (5)

Resolvida **no simulador**, não no filtro, e a assimetria é proposital. Num cenário os condicionantes
exógenos são dados por construção, então `E_t π_{t,t+4}` é a soma da própria trajetória simulada
quatro trimestres à frente; no filtro o mesmo objeto exigiria fixar o que o modelo espera de π^A, π*,
Δe e rp em cada trimestre da amostra — convenção que o boxe não publica e que moveria E_t π mais do
que os próprios φ.

O modelo é linear, então `T(π^e)` é **afim** e a equação vira o sistema `(I − G)π^e = g`, resolvido de
uma vez (resíduo ~1e-14). Com `i^e` lido do caminho de juros o raio espectral cai para 0,68 — a nota
antiga de que "Fair-Taylor divergiu por instabilidade genuína" descrevia um motor que aproximava a
Selic esperada pela corrente, o mesmo bug que inflava o IRF 4-5x. **Mas a fronteira é real**: o raio
passa de 1 em φ₂ ≈ 0,32, e acima disso a condição terminal é que determina a resposta; o simulador
levanta erro quando isso acontece.

| φ | nosso | BC | IC 90% | |
|---|---|---|---|---|
| φ₁ inércia | 0,710 | 0,75 | [0,68; 0,82] | dentro |
| φ₂ previsão do modelo | **0,211** | 0,11 | [0,06; 0,13] | **fora** |
| φ₃ inflação passada | 0,048 | 0,021 | [0; 0,049] | dentro |
| peso da meta | 0,032 | 0,119 | — | |

R² de 0,898 contra 0,884 nas modas do BC, com **máximo interior em 0,21** (0,873 em 0,06; 0,884 em
0,11; 0,870 em 0,30) — não é canto de restrição. O cuidado que domina o desenho do estimador é não
criar simultaneidade: condicionar a previsão no π^e **observado** em t faz ela herdar o próprio
regressando (π^e entra na Phillips com peso 1−α₁ᴸ−α₁ᴵ ≈ 0,69) e φ₂ sai em 0,42. Ancorar tudo no
conjunto de informação de t−1 resolve, e o timing é a favor: a Focus do trimestre t é coletada com
dado até t−1.

## Decisões validadas contra número publicado

Não escolhidas por plausibilidade — testadas. As três primeiras também estão no Apêndice do
relatório:

- **i^e é a Selic esperada NO horizonte de 12 meses** (ponto), não a média do caminho: contra a
  Tabela 1 do boxe da neutra, o ponto erra +0,14 e a média +0,82.
- **O HP roda com cauda de projeção Focus** — sem ela r* em 2023T4 dá 7,15% contra 4,82% publicado;
  com ela, 5,01%. O BC faz o mesmo (título do `C2 Boxe1 Graf 1B`).
- **Juro real é diferença simples** i^e − π^e, como na eq. (2.1). Fisher exato descola ~0,2 p.p.
- **Nuci dessazonalizada por X-13** — crua tem sazonalidade de 25% do próprio desvio-padrão e
  inflava γ_nuci (2,164, fora, contra 2,057 dentro).
- **O ONI entra em décimos de grau, não em graus** (a nota 6 nomeia a série mas não a unidade, e a
  diferença é 100x em Clima²). Três medidas apontam para décimos: com α₅/α₆ livres a verossimilhança
  pede ~107x as modas publicadas e o `k = √(α₅/0,0012)` implícito fica entre **10,2 e 10,6 em todos**
  os ajustes deixa-um-episódio-ENSO-de-fora; reescalado, α₅ = 0,0013 cai praticamente na moda
  (0,0012) e α₆ = 0,0017 dentro do IC; e o suporte [0; 0,01], "pouco informativo" segundo o BC,
  limitaria o clima a **0,05 p.p.** se fosse em graus.
- **Dummies em zero, não no ±0,5 do NOAA** — o boxe diz "valor 1 quando a anomalia é positiva".
- **Prior própria no filtro, não difusa** (sd 2 p.p. para o desvio de r*, 3 p.p. para o hiato): com
  difusa o filtro fixa `rr_TAY` num nível arbitrário do qual não sai.
- **Regressor exógeno faltante ⇒ observação faltante**, não intercepto zero — sem isso uma defasagem
  ausente no início da amostra gera resíduo artificial de +18 p.p. na Taylor. É também o que mantém
  a UIP genuinamente inativa antes de 2008T1 (onde o CDS começa).

Duas coisas que o BC não publica, recuperadas por regressão: pesos do IC-Br (agro 0,687 / metal 0,154
/ energia 0,159, R² 0,995) e do IPCA (livres 0,767 / administrados 0,233, R² 0,978).

## Fontes que não estavam no projeto

- **Nuci da FGV** — IPEADATA `CE12_CUTIND12`, 1970→hoje. Estava registrada como lacuna real; não é.
- **Desocupação retropolada do próprio BC** (Alves e Fasolo, BCB WP 400/2015) — `Graf 1.2.11` do
  anexo do RPM, mensal a.s. desde 2004-04; as tabelas de PNAD do projeto só começam em 2012. Entra
  com **sinal invertido** (desocupação é contracíclica, γ_emp > 0).
- **Anexo de jun/2024** — publica o modelo inteiro como dado: `C2 Boxe3 Tab 1` (os 22 parâmetros),
  `Graf 1A-4B` (os IRFs) e `C2 Boxe2 Graf 1` (5 medidas de taxa neutra). O boxe da neutra e o dos
  modelos só saem em **algumas edições** — jun/2025, mar/2026 e jun/2026 não os trazem, então a série
  publicada de r* para em 2024T2.

## A antecipação da projeção com o modelo (`antecipa_modelo.py`)

O relatório de Política Monetária prevê o número que o Copom vai publicar pelo **delta da Focus**
(ver `../../monetary_policy/CLAUDE.md`, "Antecipar a projeção do BC"). Este é o registro de por que
não é pelo modelo — e o `antecipa_modelo.py` refaz a medição.

**O modelo agregado não serve para isto.** Com as modas do BC fica *pior*, então não é a nossa
estimação — é a estrutura. O que funciona é a revisão da própria Focus para o mesmo
trimestre-alvo, com correlação de **0,70** contra a revisão do BC, e ela acerta justo a que o
modelo mais erra: na 267ª a revisão real foi +0,4 e o delta da Focus deu +0,31.

A explicação é o conjunto de informação, não o ajuste: a revisão do BC entre duas reuniões vem
sobretudo do **IPCA mensal novo**, que a pesquisa semanal incorpora e um modelo trimestral não vê —
aqui `t0` fica até 4,5 meses atrás da reunião, porque um trimestre só fecha quando sai o IPCA do
último mês dele. Reuniões do mesmo par chegam a compartilhar `t0`, e aí o delta do modelo vem
apenas da curva da Focus, dos administrados e de r*.

Duas coisas foram testadas e não salvaram o modelo, e as duas ficaram implementadas com
interruptor (`backtest(parametros=..., cambio=...)`) porque a comparação **é** o resultado:

- **Condicionar o câmbio** (observado até o corte, PPC depois) move o MAE de 0,1452 para 0,1453. O
  canal é mudo porque `a3` aqui é 0,0024 contra 0,011 do BC e porque o bloco de administrados — onde
  o repasse cambial deles é 1,65 p.p. por 10% de depreciação, mais que o dobro do de livres — não
  existe. Com `a3` tão pequeno, 2 p.p. de depreciação extra valem 0,005 p.p. de inflação.
- **Usar as modas do BC** piora, como a tabela mostra.

### A taxa neutra que o BC anuncia, que não é a nossa

Achado desta rodada, e ele é a peça que mais move o nível. O BC **declara** no RPM a r\* real que
usa nas projeções, fixa por várias reuniões, e avisa quando muda:

| decidido na reunião | RPM que anuncia | r\* real |
|---|---|---|
| até a 262ª | — | 4,50% |
| **263ª** (jun/2024) | 2024-06-27, p.74 | **4,75%** |
| **267ª** (dez/2024) | 2024-12-19, p.59 | **5,00%** |
| segue valendo | 2026-06-25, p.66 reafirma | 5,00% |

Não confundir com a mediana das *medidas* de r\* do boxe de jun/2024 (4,8% para 2024T2, que a p.95
daquela edição diz ter subido para 5,0%): aquilo é estimativa da neutra, isto é o valor plugado no
cenário. Trocar a nossa r\* de 7,81% por esses 5,00% move 2028T1 de **3,45 para 3,07** (contra 3,2
publicado) e vira o hiato de +0,35 para −0,75 — a política passa a ser genuinamente restritiva.
`simular()` ganhou três argumentos opcionais para isso (`rr`, `h0`, `sh0`), todos inertes por
default; conferido que os 12 cenários padrão não se movem.

**A frase da neutra não está no `raw_md`**: a extração do RPM guarda só as páginas com tabela de
projeção, e ela vive numa página sem tabela. Está nos PDFs em disco. `R_NEUTRA_BC` no módulo é a
transcrição, com edição e página.

### Insumos do cenário, todos cortados na data da decisão

| insumo | fonte | armadilha |
|---|---|---|
| r\* real | `R_NEUTRA_BC` (RPM) | muda 2× na amostra |
| Selic | `expc_focus_copom` | **a Focus descarta as reuniões que já aconteceram** — em 21/08/2026 o primeiro rótulo é R6/2026, a 280ª sumiu. Como `t0` fica meses atrás, a janela começa no passado: o caminho é realizado até o corte e esperado depois, agregado por **média** ponderada por dias (é assim que o `selic` do painel é construído) |
| π^A | `expc_focus_periodo`, administrados trimestral | horizonte trimestral vai a 2028T2, não precisa trimestralizar |
| câmbio | `cmb_ptax` | observado até o corte, PPC depois |
| hiato inicial | `pm_hiato_produto_vintages` | o que o BC publicou, não o nosso latente — evita reconstruir o painel 17 vezes |

O painel e os estados entram na versão **corrente**, de propósito: as séries que `simular()` lê em
`t0` ou não sofrem revisão ou são indexadas pela data em que o dado existiu. O único genuinamente
revisado é o hiato, e é justo o que vem do vintage.

## O resultado que precisa de olhar

Com dado até 2026T2, a tendência HP do juro real Focus está em **7,7%** e o r* da IS em **7,9%** —
contra ~4,8% da mediana que o BC publicou para 2024T2. Isso implica que a Selic de 15% está pouco
restritiva e que uma Selic de 10% seria **expansionista** (r̂ = −2,1 no cenário Focus, com o hiato
abrindo para +1,0 e o IPCA em ~4,2%). É consequência da especificação do boxe, não de bug: r* é
definido como tendência HP do juro real corrente mais um passeio aleatório. Mas é a premissa que
domina todo cenário, e vale decidir se ela é aceitável antes de usar os cenários para decisão.

## Pending

- **Equação (5) dentro do filtro** — exige (a) π^e como estado e (b) uma convenção para o que o
  modelo espera dos exógenos em cada trimestre da amostra, que o boxe não publica e que move E_t π
  mais do que os φ. É a única via para testar se o α₁ᴵ se corrige.
- **Bloco de preços administrados** — o boxe do RI de set/2017. É a **única premissa que sobrou** no
  cenário, e é o que separa o nosso IRF completo da primeira linha do Graf 4B. Alvos de validação
  já levantados: 10% de depreciação → +1,65 p.p. nos administrados e +0,72 nos livres, fechando
  +0,96 no IPCA (texto do boxe, p. 102-103).
- **Hiato mundial** — excluído por decisão. Se voltar: construível de `cmb_comex_pais` (pesos de
  exportação) + PIB dos parceiros via FRED/BIS, que é a receita da nota 9 do boxe.
- **CDS pré-2008** — a UIP fica inativa em 17 dos 81 trimestres. O EMBI+ do IPEADATA emendaria.
