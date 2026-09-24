# analytics/brasil/monetary_policy/ — Contexto para o Claude

Réplica do **modelo agregado semiestrutural do BC** (boxe do RI de jun/2024) — estimada, decomposta
e servindo cenários no relatório HTML — mais a Curva de Phillips em planilha auditável e o material
de referência.

Histórico rodada-a-rodada de como cada peça chegou ao estado atual vive no git log, não aqui.

## Como rodar

A estimação **não** roda na geração do relatório: leva minutos e depende de MySQL, IPEADATA e do
anexo do RPM, enquanto gerar o HTML tem de ser rápido. Nesta ordem:

```powershell
uv run python analytics/brasil/monetary_policy/modelo_painel.py     # 2 painéis + sigma calibrado
uv run python analytics/brasil/monetary_policy/modelo_agregado.py   # estima, decompõe, valida
uv run python analytics/brasil/monetary_policy/generate_report.py   # HTML
uv run python analytics/brasil/monetary_policy/antecipa_copom.py    # backtest + previsão
node tests/test_monetary_policy_js.js                               # asserções do relatório
uv run python tests/test_eq5_expectativas.py                        # 19 asserções (eq. 5)
```

| Módulo | O que faz |
|---|---|
| `modelo_painel.py` | Painel trimestral dos insumos. Escreve **dois**: `_est` (HP até 2023T4, fiel ao conjunto de informação do boxe — o único em que comparar parâmetros é legítimo) e `_full` (HP até hoje, para estender os estados e partir daí nos cenários). |
| `modelo_agregado.py` | Espaço de estados + estimação + decomposições + simulador + validações. `rodar()` grava tudo em `data/`. |
| `condicoes_copom.py` | O conjunto de informação da última reunião contra o de hoje. Independente do modelo: lê MySQL e o `domain/release_calendar/` na hora, não usa `data/`. |
| `antecipa_copom.py` | Antecipa a projeção do BC para o horizonte relevante da próxima reunião. Independente do relatório; lê MySQL e os artefatos de `data/`. |
| `generate_report.py` | Lê os artefatos de `data/` e injeta em `report.html`. |

O teste de `condicoes_copom.py` roda junto: `uv run python tests/test_condicoes_copom.py`
(não toca no banco — varre o calendário e séries sintéticas).

`data/` é versionada de propósito: `rodar()` sempre re-estima (não há caminho barato para recriar só
as séries derivadas) e `tests/test_eq5_expectativas.py` roda self-contained a partir de
`modelo_painel_full.csv` + `modelo_params.json`.

## O que o modelo é

**Equações**: transcritas na docstring de `modelo_agregado.py`, com a numeração do boxe, e na seção
"O modelo, equação por equação" do Apêndice do relatório, lá com os coeficientes estimados no lugar
dos símbolos. As fórmulas são **imagem** no PDF — `pdfplumber`/`pymupdf` extraem o texto ao redor mas
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

## Relatório HTML

`generate_report.py` + `report.html` → `reports/brasil/Monetary Policy.html`. Construído sobre
`analytics/report_structure/`. **`_reactPreserveX()` é o ponto de entrada de todo gráfico — não
chamar `Plotly.newPlot`/`react` direto.**

| Aba | Fonte | Estado |
|---|---|---|
| **Condições** | `condicoes_copom.py` — MySQL + `domain/release_calendar/`. Matriz 25 variáveis × 9 reuniões (aba default) | pronta |
| Projeções do Copom | `pm_copom_projecoes` × `pm_copom_reuniao` | pronta |
| Apêndice | descrição do modelo + validação dos parâmetros + notas | pronta |

**Cinco abas foram removidas a pedido do usuário**, todas com os `_load_*` delas, para o payload
não carregar série que ninguém lê (a seção 13 do teste cobra isso nos dois sentidos): Cenários,
Decomposição, Taxa Neutra e Hiato do Produto em **2026-08-25**, e Modelo BC — Agregado em
**2026-09-22** (ver abaixo). O que **não** mudou: `rodar()` continua gravando todos os artefatos em
`data/`. Quem os lê agora são dois — o Apêndice, via `_load_info()` (parâmetros, validação, IRF,
estados e painel), e o teste JS, que lê os 12 CSVs de cenário e o `modelo_irf.csv` como referência
do Python. Essa referência já veio pelo payload um dia; ler do artefato é melhor, porque não passa
pelo arredondamento de 4 casas do `_ser()` — e desde 2026-09-22 é a **única** via, já que o HTML
não carrega mais nada do simulador.

Os **cenários** seguem pré-calculados por `cenarios_padrao()`: caminho de Selic (Focus / constante /
±100 pb por 4T) × tratamento da expectativa (endógena pela eq. 5, default / fixa na Focus /
convergindo à meta). As duas premissas fixas são contrafactual — a distância até a endógena é o
tamanho do canal de expectativa. Hoje só o teste os lê (seções 16 e 17).

### A seção "O modelo, equação por equação" (2026-08-25)

Primeiro bloco do Apêndice: dez notas expansíveis com as equações (1) a (9), mais como o **hiato** e
a **taxa neutra** são recuperados, e uma tabela dos parâmetros de variância que a Tabela 1 do boxe
não publica (`s_h`, `k₀₈`, `k₂₀`, `s_pi`, `k_pi`, `s_i`, `s_e` e o `σ(εʳ*)` calibrado).

**A prosa vive no script, não no HTML**, e é a única coisa aqui que não é preferência: cada equação
é escrita com o **coeficiente estimado no lugar do símbolo**, lido de `D.info.params` — reestimar o
modelo reescreve a descrição em vez de deixá-la envelhecer ao lado de números novos. Uma nota nova é
um objeto `{t, c}` novo em `MODELO_ITENS()`; o `<details>` em volta é montado por `renderModelo()`.
Dourado = coeficiente nosso, azul = estado latente. A seção 31 do teste cobra cada coeficiente na
tela contra o payload, inclusive os pesos implícitos (`1−α₁ᴸ−α₁ᴵ`, `1−θ₁−θ₂`), que não estão em
`params` e têm de ser calculados.

A nota antiga "Por que a equação (5) está fora, e o que isso custa" **saiu**: afirmava que a (5)
estava fora do modelo e que Fair-Taylor divergira por instabilidade genuína, e as duas deixaram de
valer. No lugar ficou uma nota de histórico que reconcilia a afirmação — um apêndice que se
contradiz é pior que um incompleto.

### A aba Modelo BC — Agregado saiu em 2026-09-22

Era a única aba do projeto em que **o modelo rodava no navegador**: `simular()` estava portado para
JS e re-resolvia as equações — inclusive o ponto fixo da eq. (5) — a cada mudança de input, com um
card por condicionante, horizonte selecionável e cenários guardados no `localStorage`. Saiu inteira,
a pedido do usuário: ~1.200 linhas de JS, ~165 de CSS, o painel HTML, os loaders `_load_motor()` e
`_motor_cfg()` (com `_copom_administrados()` e `_copom_hr()`) e as seções 19 a 30 do teste.

O que sobrou dela, e não é pouco: **o modelo continua estimado e continua no Apêndice**. As equações
saem escritas com o coeficiente estimado, a tabela de validação segue conferindo os 22 parâmetros
contra a Tabela 1 do boxe, e o IRF contra o publicado. O que deixou de existir é a interface de
cenário — não o modelo.

Se um dia voltar, três coisas valem uma releitura antes (as três foram bug uma vez, nenhuma tem
sintoma): `vals` guardava número exato e nunca a string arredondada de exibição, senão o cenário
default deixava de reproduzir o Python bit a bit; o choque `s^h` decaía por β₅ no buffer além do
horizonte, ao contrário de todos os outros inputs, que seguravam o último valor; e
`ini.selic`/`ini.pi_e` eram lidos **em t₀** (a defasagem que as equações usam) enquanto
`dflt.selic_ult`/`dflt.pi_e_focus` eram o **último valor publicado**, que já pode estar um trimestre
à frente — confundir os dois acusava em 11 dos 12 cenários. O código está no git, no commit da
remoção.

### A aba Condições: a matriz reunião a reunião (2026-09-22)

**Uma linha por variável, uma coluna por reunião** — as 8 últimas já decididas mais a
próxima. A célula é o valor que a variável tinha **no fechamento daquela reunião**, com o
período de referência impresso embaixo, e recebe cor só quando trouxe informação **nova**
desde a coluna anterior. Mais a agenda de divulgações até o corte, **filtrada ao que
alimenta uma das linhas** — o calendário inteiro tem relatório próprio.

A versão anterior (2026-08-25) era duas colunas: a última reunião contra hoje, com KPIs e
uma régua de saldo hawkish/dovish. As três coisas saíram a pedido do usuário; a mecânica de
corte, σ e cor **não mudou** — ela já era genérica, e passar de 2 para 9 cortes foi
generalizar `_valor_em()`, não reescrevê-lo.

**25 variáveis em quatro blocos**, com a especificação em `_spec()`:

| bloco | linhas |
|---|---|
| Inflação | **projeção do próprio BC no horizonte relevante**, IPCA 12m, núcleos (média de 5) mm3m anualizada, Focus para T/T+1/T+2, Focus no horizonte relevante, implícita de 2 e 10 anos |
| Atividade | IBC-Br 12m, Focus PIB T/T+1, PIB/consumo/FBCF em 4T/4T |
| Condições Financeiras | PTAX, juro real ex-ante de 2 e 10 anos (NTN-B), juro real de 2 anos pela Focus, crédito livre e direcionado (real, 12m) |
| Condições Externas | juro real americano de 2 e 10 anos, IC-Br m/m, Brent |

**O ponto todo continua sendo a regra de corte, e ela não é sobre a reunião — é sobre a
natureza do índice de cada série.** Uma série de mercado ou da Focus é indexada pela data em
que o dado existiu: corte direto, e é por isso que essas linhas mudam em toda coluna (numa
reunião de meio de mês vale o pregão daquele dia, não o fechamento do mês). Uma série mensal
ou trimestral é indexada pelo **período de referência** e só é publicada semanas depois — o
IPCA de julho está no banco com data 01/07 e saiu em ~13/08, de modo que na reunião de 05/08
o Comitê ainda estava com o de junho. Ler o banco por `date <= reunião` daria julho, e **não
levantaria exceção nenhuma**: devolveria um número plausível do período errado. Medido no
mutante que faz isso: **65 asserções** caem.

O corte é `datetime(dia 2, 18:30)`, não a data. Três consequências que já custariam bug: o
horário decide o IC-Br (o de julho saiu às 14:30 de 05/08, o dia da 280ª — entrou por quatro
horas); no dia 2 antes das 18:30 a reunião em curso ainda é a *próxima*; e a coluna da
próxima reunião é cortada em **agora**, não no fechamento dela — afirmar o corte futuro seria
ler dado que ainda não existe.

O que a generalização exigiu, e cada item é a origem de um defeito silencioso:

- **A janela interna tem N+1 reuniões e a tabela mostra N.** A coluna mais antiga precisa de
  uma anterior para ter delta; sem ela a primeira coluna nunca receberia cor, o que seria
  propriedade da janela e não do dado.
- **Cor só onde `novo`.** Uma série trimestral repete o último número entre divulgações, e
  colorir a repetição afirmaria notícia onde houve silêncio — sem sintoma, porque o número
  repetido é plausível. `novo` é `pos` andar entre duas colunas, e o teste cobra que ele bata
  com a troca do período de referência.
- **"Sem dado novo" e "dado novo que não mudou nada" têm as duas fundo neutro** e precisam se
  distinguir: a célula repetida ganha lavagem cinza do CSS, e por isso ela **não** leva
  `style` inline — um `background:transparent` inline venceria o CSS e as duas voltariam a ser
  indistinguíveis. Há mutante para isso.
- **A lista de reuniões vem de DUAS fontes.** `pm_copom_reuniao` tem a história e o passo de
  Selic, mas só depois que o ETL roda — a 281ª (16/09/2026) já aconteceu e ainda não está lá.
  O calendário tem as datas e nenhum passo. A união dá a janela; o passo fica vazio onde só o
  calendário alcança, em vez de virar um zero inventado (parado é uma decisão).
- **Referência trimestral.** `_ref()` infere a frequência em vez de fixar mês: `2026-Q2`
  forçado a mensal devolveria um mês que não existe no índice trimestral e a linha sumiria. E
  a defasagem conta do **fim** do trimestre — o PIB do 2º tri sai ~3 meses depois de junho,
  não de abril.
- **Duas entradas para o mesmo período: vale a mais tarde.** Não é hipotético — o
  `bcb_credit_note` de 2026 carimba `2026-06` em 01/07 e de novo em 30/07, e a cadência do
  grupo mostra que a primeira é rótulo errado do ICS. Pegar a primeira poria o dado de junho
  disponível um mês antes de existir. O mesmo desempate entra no **ajuste da regra**: com a
  duplicata dentro, o erro máximo do grupo ia a **27 dias** e marcava como ambígua toda célula
  de crédito da matriz; sem ela, 2 dias.
- **O seletor traz só o rótulo da reunião.** O passo de Selic saiu dele em 2026-09-22, a
  pedido do usuário: ele já está na linha **Decisão** do cabeçalho, embaixo da própria
  coluna, e repetido na pill só alongava um rótulo que precisa caber nove vezes na mesma
  barra. O teste cobra as duas metades — fora da pill, e ainda na linha Decisão.
- **A agenda depende do corte REAL da próxima reunião**, não do corte da coluna. Como a coluna
  futura é cortada em agora, usar o mesmo campo deixaria a janela `[hoje, corte]` com ~zero
  dia e a agenda sairia **vazia sem erro nenhum**.

Decisões de série que vieram com as linhas novas:

- **A projeção do BC entra pelo COMUNICADO, nunca pelo relatório** (pedida em
  2026-09-22, acima do IPCA). O mesmo número da aba Projeções, com um filtro a mais, e as
  duas razões são independentes: o comunicado sai **no fechamento da reunião** e o
  relatório 7 a 28 dias depois, então só o primeiro estava na mesa daquele dia; e até
  2024-06 o horizonte relevante só existia no relatório, que é trimestral — misturar os
  dois põe no mesmo índice pontos separados por ~45 e por ~90 dias, e `_sigma` mede a
  variação por POSIÇÃO. Medido: mediana de espaçamento de **84 dias** com o trecho antigo
  dentro contra **45** sem ele, e a escala típica de uma variação dobra (**0,297 p.p.**
  contra **0,148**), o que apagaria pela metade a cor de toda a linha. De 2024-07 em
  diante o comunicado tem projeção em todas as reuniões, então o que se perde é história
  velha e o que se ganha é um índice em que uma posição é uma reunião.
- **E ela é a única linha cujo rótulo de referência NÃO identifica a observação.** O
  índice da série é a data do comunicado; o rótulo impresso embaixo do valor é o trimestre
  PROJETADO, que é o que responde "sobre o que é este 3,2". Como o horizonte só anda a
  cada dois meses, **duas reuniões seguidas projetam o mesmo trimestre com números
  diferentes** — e a equivalência "trocou de referência ⇔ tem dado novo", que vale em
  todas as outras linhas e é cobrada no teste, fica falsa aqui. Daí `ref_map` (o rótulo) e
  `ref_alvo` (a marca que tira a linha daquela regra). E daí também `div_hora`: dizer que
  aquele índice é uma data de PUBLICAÇÃO é o que põe a linha debaixo da mesma fronteira de
  anacronismo das demais — sem isso a célula sai sem data de divulgação e o teste deixa de
  checar justo a linha que não tem outra guarda. Não vale para a Focus, cujo índice é a
  data de referência da pesquisa e cujo boletim sai na segunda seguinte.
- **Na coluna da próxima reunião a projeção repete a última publicada**, cinza e sem cor — a
  seguinte só passa a existir com o comunicado dela. O usuário pediu assim por ora; a
  ideia é pôr ali uma PREVISÃO do que o BC vai projetar, depois de rever a aba Projeções.
  A caixa de previsão daquela aba já calcula um candidato
  (`antecipa_copom.py`) — quando entrar, a célula deixa de ser repetição e precisa dizer na
  tela que é estimativa, não publicação.
- **Inflação implícita é razão, não diferença.** A 14% de DI e 7,5% de NTN-B a subtração dá
  6,50 e a forma correta 6,05 — 0,45 p.p., maior que o movimento típico de um mês. A forma
  errada funciona na faixa em que se costuma olhar, como na identidade produto/horas do
  relatório de produtividade.
- **O horizonte relevante é acumulado de 4 trimestres, 6 à frente**, composto e não somado, e
  derivado do trimestre da **pesquisa** — o que faz a série ser uma só em vez de uma por
  reunião, e a janela ser rolante em vez de ter o dente de serra do ano-calendário.
- **O juro real de 2 anos da Focus é MÉDIA, não taxa a termo**, porque a NTN-B de 24M ao lado
  dele é média. Selic da curva anual da Focus lida em 0,25/0,50/…/2,00 e mediada (com âncora
  em h=0 na Selic corrente, sem a qual a curva não cobre 0,25 no fim do ano) sobre o IPCA
  acumulado em 8 trimestres, por Fisher.
- **Os dois juros reais americanos usam o mesmo método** — nominal menos inflação esperada do
  Fed de Cleveland — porque o Treasury **não publica TIPS de 2 anos** e as duas linhas ficam
  lado a lado. Os números que decidiram isso estão na docstring de
  `domain/db/us/inflation/expc_inflacao.py`.
- **IBC-Br em 12m entra pela série NSA**: o acumulado de 12 meses já é sazonalmente neutro por
  construção, e ajustar em cima seria dessazonalizar duas vezes.
- **O crédito real cruza nominal e IPCA pelo MÊS DE REFERÊNCIA**, não pelo de divulgação —
  cruzar por divulgação misturaria dois calendários para produzir um número que não é de
  nenhum dos dois.

O que continua valendo da versão anterior, e não foi tocado: `_sa()` começa em 2000 (com a
série inteira o "dessazonalizado" saía **mais volátil que o bruto**, sd 1,03 contra 0,39, e
esse ruído ia direto para o σ); σ é escala **robusta** (1,4826 × MAD), porque dez anos de
história contêm 2020-2021 e com desvio-padrão aquele episódio vira a régua; fatores sazonais
**congelados** até dezembro do ano anterior; nível de preço em variação percentual
(`modo='pct'` — hoje câmbio e Brent, com σ medido em 100×Δlog); e a marca `pendente` quando o
calendário diz que saiu dado que o ETL não carregou.

**O que saiu com o recorte novo:** as linhas de desocupação da PNAD, saldo do CAGED, núcleo
EX3 e as três da Focus de Selic — e com elas os helpers que só as serviam
(`desocupacao_sa`, `caged_saldo_sa`, `nucleo_ex3_mm3m`, `mm3m_anual`, `ibcbr_3m3m`,
`focus_reuniao_serie`, `rotulo_focus`, `numero_reuniao`, `juro_real_ex_ante`,
`focus_ipca_12m_diario`). Com elas foi embora o caso `sinal = 0`, que existia só para a Selic
esperada da Focus (reação do mercado à decisão, não condição que a antecede). `mt_pnad` saiu
das dependências do dashboard; `mt_caged` ficou, porque o painel do modelo a lê como
observável do hiato.

Cobertura: seção 32 de `tests/test_monetary_policy_js.js` (o payload pronto e a markup — a
fronteira de divulgação em cada uma das 9 colunas, `novo` contra a troca de referência, a
pill que esmaece só as posteriores e não traz o passo de Selic, o card de definição, e a
nota de cada linha contra uma lista de vocabulário de mecanismo) e seções 10-15 de
`tests/test_condicoes_copom.py` (a mecânica que produz aquelas datas, mais o espaçamento
da série de projeção e o efeito dele no σ). Verificado contra **13 mutantes**, todos pegos,
e confirmado em Chrome real: 225 células, 184 pintadas, 25 cards, zero exceções.

### A aba Projeções do Copom (2026-08-25)

A projeção do BC para o horizonte relevante contra o **passo de Selic da mesma reunião** — o que o
Comitê projetava contra o que ele fez —, mais a **previsão da próxima**. Três seções: a série
temporal (barras de pontos-base no eixo da direita, projeção no da esquerda, e o ponto previsto
em bolinha verde ligada por tracejado), o **backtest** do que estimamos contra o que o BC publicou, e a
tabela reunião a reunião. Desde 2026-09-23 sobraram **dois** seletores, e a posição de cada um
segue o que ele comanda: **previsão** (delta da Focus | modelo | ingênuo) no alto da aba, porque
governa os dois gráficos, e **projeção** (nível | desvio da meta) colado no gráfico de cima,
que é o único que ele muda.

Saíram na mesma rodada, a pedido do usuário, os de **cenário** e de **defasagem**. O de cenário
alternava entre juros esperado e juros constantes: o segundo é a leitura mais próxima de uma
função de reação e é justamente o que o BC parou de publicar — a série termina em **jul/2024** —,
então o seletor convidava a comparar uma janela corrente com uma parada há dois anos sem dizer
que eram diferentes. O de defasagem escolhia entre o passo da própria reunião e o da seguinte, e
as duas leituras dão **0,27 e 0,28** de associação: o clique custava uma escolha e não mudava
resposta nenhuma. O payload deixou de carregar `juros_constante` e `bps_prox` junto — voltar a
carregar o cenário é uma palavra na tupla de `_projecoes()`.

**A régua de período cede o lugar.** `_ensurePeriodSelector()` se insere acima da barra que tiver
`chart-ctrl-bar`, e não imediatamente antes do `.chart-card`: quem comanda *o que* o gráfico
desenha fica colado nele, e quem só move a janela de tempo fica acima. Sem a classe o markup
fica idêntico e a régua volta a se meter no meio — nada na ordem denuncia, e foi o mutante que
escapou na primeira rodada.

O **grid de quatro KPIs saiu em 2026-09-23**, a pedido do usuário. Três dos quatro repetiam
número que a página já dava — a projeção e o passo da última reunião estão no último ponto do
gráfico e na última linha da tabela, e a contagem de reuniões por documento está na legenda do
gráfico, palavra por palavra. O quarto era a **correlação**, e esse número deixou de existir na
tela: ele continua medido aqui embaixo, e se voltar o lugar dele é uma oração da legenda, não um
cartão. `pjKPI()` e `pjCorr()` saíram junto — função que só alimentava markup removido é órfã.

A **dispersão desvio × passo foi retirada em 2026-08-25** a pedido do usuário e o backtest ficou no
lugar dela. Com isso a aba deixou de ter gráfico que não é série temporal em X, e a exceção ao
`_reactPreserveX` que ela documentava desapareceu junto: os dois gráficos de hoje passam por ele.

O lado da decisão veio de tabela nova, `macro_brasil.pm_copom_reuniao` — 247 reuniões da 34ª
(1999-04) à 280ª, derivadas da **SGS 432** cruzada com o calendário de reuniões. Não é o texto do
comunicado: aquele só é parseado da 206ª em diante, e o passo precisa cobrir a série toda. O texto
entra como **conferência independente**, e nas 63 reuniões em que ele escreve a decisão em prosa as
duas fontes concordam em todas.

**O passo é o da reunião, não o acumulado do ciclo** (decisão explícita do usuário): parado, parado,
+25, +50 aparece como 0, 0, +25, +50. É a variável de decisão, e é comparável entre ciclos porque
não depende de quantas reuniões o ciclo já teve.

Quatro coisas que decidiram o resultado:

- **A janela de cinco dias**, e ela é medida, não escolhida. A meta nova vale do dia útil seguinte,
  mas feriado emendado empurra isso: das 152 mudanças de nível desde 1999, 147 entram 1 dia depois
  da reunião, 4 em 2 (reunião de quarta com feriado na quinta — Corpus Christi de 2003/2007/2009 e
  o 7 de setembro de 2017) e 1 em 5 (20/04/2011, Tiradentes na quinta e Sexta-feira Santa no dia
  seguinte). Os **8 movimentos por viés** estão todos a 7 dias ou mais. Uma primeira versão pegava
  o *último* ponto de uma janela de 12 dias e com isso atribuía à 45ª reunião um corte por viés
  ocorrido 7 dias depois dela; pegar o *primeiro* ponto quebrava o caso contrário, a 209ª, cujo
  corte só entrou 2 dias depois por causa do feriado. Cinco dias separa as duas coisas exatamente,
  e foi a conferência contra o comunicado que apontou o erro.
- **Uma unidade de horizonte só.** A série é sempre o ponto a **seis trimestres** da reunião. Os
  regimes `ano_calendario` e `horizonte_suavizado` do comunicado pré-2024 ficam fora: um horizonte
  relevante que é o ano civil encurta de 12 para 4 trimestres à frente ao longo do próprio ano, e
  isso põe na série um dente de serra que não é mudança de projeção nenhuma. Custa 14 reuniões de
  2020-2024 e sobram 107.
- **Comunicado ganha do relatório na mesma reunião**, porque sai no dia da decisão. Sem filtro de
  `documento` a reunião entra duas vezes com números diferentes. Da 264ª em diante os dois publicam
  o mesmo número, então a preferência é inócua justo onde seria mais visível.
- **Um eixo Y na escala "desvio da meta", dois na de nível** (2026-08-25, a pedido do usuário), e a
  razão é unidade. Desvio e passo estão ambos em pontos percentuais — 100 pb de Selic é 1,00 p.p. de
  desvio —, então dividir régua é o que torna "o desvio era +1,0 e o Comitê mexeu +1,0" uma frase
  legível do gráfico. Na escala de nível não existe essa leitura (3,5% de IPCA projetado e +50 pb não
  dividem régua nenhuma) e ali o eixo duplo é o certo. Duas coisas têm de acontecer juntas: as barras
  mudarem para `y` **e** o `yaxis2` sair do layout — um eixo sobreposto sem trace nenhuma ainda
  desenha título e ticks à direita, e o leitor lê duas escalas onde há uma. O rótulo em cima da barra
  segue em **pb** mesmo com o eixo em p.p., porque passo de Selic se fala em pb.
- **`barmode: 'relative'` com uma barra só** não empilha nada — é o que faz o `_bindYAutofit` dobrar
  o zero dentro do range do eixo das barras. Sem isso, numa janela de ciclo de alta o autofit
  devolveria `[20, 105]` e as barras sairiam desenhadas do fundo do eixo, como se +25 pb fosse quase
  nada. Erro puramente visual: nenhuma exceção, nenhum número errado.

**A previsão dentro da aba** (2026-08-25). O ponto previsto entra no gráfico principal como duas
traces separadas — uma ponte tracejada sem legenda e sem hover, e uma bolinha verde — e nunca
como mais um ponto da série dourada: é o único número da aba que ninguém publicou.

**A caixa verde que ficava acima do gráfico saiu em 2026-09-23**, a pedido do usuário, na mesma
rodada do grid de KPIs — ela trazia âncora, documento, delta, MAE do método, corte de informação e
a faixa de frescor, seis linhas de texto sobre um número só. O que saiu com ela e **não podia**
sumir é o **corte de informação**, que era a única procedência do ponto na tela: ele passou para a
legenda do gráfico, na mesma oração que já nomeava a reunião prevista e o método. A faixa de
frescor deixou de existir na página; o aviso equivalente continua no console da geração
(`generate_report` imprime `AVISO previsao calculada com dado ate …`), que é onde ele é acionável —
mas quem só abre o HTML não é mais avisado de artefato velho. Vale como pendência se o caso
voltar a acontecer.

Três decisões que a seção 33 do teste fixa, porque nenhuma delas lança exceção se quebrar:

- **A previsão é condicionada na curva de Selic da Focus**, que *é* o condicionamento do cenário
  que a aba lê. Era por isso que ela desaparecia no cenário de juros constante, enquanto esse
  seletor existiu: desenhá-la ali faria o ponto parecer continuar uma série que ele não continua.
- **A linha da meta se estende ao ponto previsto**, senão o único ponto do gráfico sem referência
  seria justo o que mais precisa dela. E a meta dele vem do mesmo dicionário das linhas publicadas,
  com `meta_estendida` marcado — na escala "desvio" a régua tem de ser a mesma.
- **Bolinha, não losango.** O marcador é círculo do mesmo tamanho dos da série publicada, só em
  verde: o losango vazado da primeira versão foi rejeitado pelo usuário — lia como sujeira, não
  como ponto. O que distingue previsão de dado publicado é a cor e o tracejado que leva até ela.
  A prosa da aba ainda dizia "losango vazado" em dois lugares até 2026-09-23: **o marcador mudou e
  as duas frases que o descreviam não**, e nada na página as contradizia.
- **A chamada da aba só promete o ponto quando ele é desenhado.** Ela testava `P.previsao` — existe
  previsão no payload? — e o gráfico testa `pjPrevValor(pv) != null`, que é outra pergunta: o método
  SELECIONADO tem valor? As duas divergem hoje mesmo, com `previsto_focus` nulo, e a frase anunciava
  um ponto verde que não estava lá. Corrigido em 2026-09-23: a chamada usa a mesma condição, diz
  explicitamente quando não há ponto, e passou para dentro do `redraw()` — a resposta depende do
  pill de método, então uma chamada escrita uma vez só fica errada no primeiro clique. O mutante que
  a tira do `redraw()` só é pego por uma asserção que **clica** na pill, não por uma que escreve em
  `PJ.metodo` e chama a função.

**O backtest também aponta para a frente** (2026-08-25, ainda a pedido do usuário): no eixo Nível
as três linhas de método ganham um ponto extra na próxima reunião, com uma vertical pontilhada
separando o que já pode ser conferido do que não pode, e a linha do publicado recebe `null` ali — é
essa parada que sinaliza a ausência de contrapartida do BC. No eixo **Erro** não estende, porque não
há número publicado para subtrair. O valor do ponto extra é lido pelo mesmo `pjPrevBruto()` que
alimenta o gráfico principal, e o teste cobra que os dois batam: são dois consumidores do
mesmo número na mesma tela.

**As duas tabelas da aba são click-drop** (`<details class="tbl-fold">`, mesma mecânica do
apêndice), fechadas por default — 17 e 107 linhas abertas empurravam tudo que vem depois para fora
da tela. O `<summary>` recebe a contagem pelo JS, senão a tabela fechada não diz o que tem dentro.

O relatório **não roda o modelo**: `antecipa_copom.salvar()` grava `data/antecipa_backtest.csv` e
`data/antecipa_previsao.json`, e `_load_antecipa()` só os lê. Sem os arquivos a aba mostra o
histórico publicado e nada mais — `antecipar()` roda o espaço de estados duas vezes e o backtest 34,
o que não cabe num `generate_report`. O contrapeso é que os artefatos envelhecem em silêncio: o
`corte_usado` fica no JSON, a legenda do gráfico o imprime e a geração avisa no console quando ele
ficou atrás do que o banco já tem.

A meta vem de `inflc_meta`, anual e terminando em 2026; os trimestres projetados vão a 2028. A meta
do último ano publicado é estendida para frente, o que sob o regime de **meta contínua** (3%, desde
janeiro de 2025) não é extrapolação — é o próprio desenho da meta. As reuniões afetadas vêm marcadas
com `meta_estendida` e o `generate_report.py` imprime a contagem.

Correlação desvio × passo: **0,27** contemporânea e **0,28** contra o passo seguinte, em 107
reuniões — medidas aqui, e desde 2026-09-23 não calculadas na página (era o quarto KPI). As duas
sobrevivem como **texto do apêndice**, que é onde elas explicam por que não há mais um seletor de
defasagem. O sinal é o esperado e a magnitude modesta também: se o Copom já reagiu, a projeção
condicionada aos juros esperados volta para perto da meta, e o desvio pequeno é *resultado* da
política. O cenário de **juros constantes** seria a leitura mais informativa dos dois — e é justo o
que o BC parou de publicar em 2024. Nenhuma das duas é estimativa de função de reação: falta o
juro real contra a neutra, que a eq. (3) deste modelo usa e que separa duas reuniões com o mesmo
desvio e Selic em 8% ou em 15%.

Cobertura: seção 33 de `tests/test_monetary_policy_js.js` (homogeneidade do horizonte, ausência de
duplicata por reunião, `bps` conferido contra os dois níveis que viajam no payload, o que cada pill
faz com os traces, e o guarda de que o grid de KPI não volta — sobre a **fatia do markup** da aba,
nunca sobre `getElementById`, que no stub cria elemento para qualquer id).

**A seção 33 aborta no meio hoje**, por duas pendências de dado listadas abaixo: a 281ª não tem
linha em `pm_copom_reuniao` e `delta_focus` está nulo, então o gráfico sai com 3 traces e a
asserção seguinte lê `traces[4]` de `undefined`. Tudo que estiver escrito depois desse ponto **não
roda** — foi por isso que o guarda do grid de KPI foi posto logo após o render, e não junto das
asserções de tabela. Verificado contra 3 mutantes (um cartão de volta no markup, a contagem de
reuniões saindo da legenda, e um controle inócuo que tem de passar).

## Antecipar a projeção do BC (`antecipa_copom.py`, 2026-08-25)

Prever **que número o Copom vai publicar** para o horizonte relevante na próxima reunião — não
qual vai ser a inflação. O horizonte é sempre 6 trimestres à frente do *trimestre* da reunião
(17/17 na era em que o Copom o declara) e há duas reuniões por trimestre, então reuniões
consecutivas costumam ter o mesmo trimestre-alvo e o BC já publicou um número para ele. O método é
**âncora + delta**, nunca nível: `projeção(281ª) = 3,2 publicado para 2028T1 + delta`.

### O resultado, medido nas 17 reuniões da era declarada

| método | MAE | direção da revisão |
|---|---|---|
| ingênuo ("não vai revisar") | 0,106 p.p. | — |
| modelo agregado, nossos parâmetros | 0,145 | 7/12 |
| modelo agregado, **modas publicadas do BC** | 0,208 | 6/12 |
| **delta da Focus** | **0,082** | **9/12** |

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

`date = 2026-10-01` é **ambíguo** e isso decidiu a busca da âncora: significa o trimestre 2026T4 ou
o ano civil 2026, que a tabela normaliza para o T4. Como o IPCA acumulado nos 4 trimestres até o T4
*é* o ano civil, os dois são o mesmo objeto econômico — filtrar `periodo_tipo='trimestre'`
descartava o comunicado da 270ª e pegava um relatório dois meses mais velho.

O benchmark é severo e por isso é reportado sempre: as revisões têm |média| de 0,106 p.p. e **13 das
17** caem dentro de um tique de arredondamento (o BC publica com uma casa). Só 4 excedem um tique.

Cobertura: `tests/test_antecipa_copom.py` (41 asserções — cada seção nasceu de um erro que devolvia
número plausível e errado sem levantar exceção: `t0` no trimestre não fechado, r\* confundida com a
estimativa, a curva da Focus sem as decisões já tomadas, e a âncora filtrada por `periodo_tipo`).

## O resultado que precisa de olhar

Com dado até 2026T2, a tendência HP do juro real Focus está em **7,7%** e o r* da IS em **7,9%** —
contra ~4,8% da mediana que o BC publicou para 2024T2. Isso implica que a Selic de 15% está pouco
restritiva e que uma Selic de 10% seria **expansionista** (r̂ = −2,1 no cenário Focus, com o hiato
abrindo para +1,0 e o IPCA em ~4,2%). É consequência da especificação do boxe, não de bug: r* é
definido como tendência HP do juro real corrente mais um passeio aleatório. Mas é a premissa que
domina todo cenário, e vale decidir se ela é aceitável antes de usar os cenários para decisão.

## O que ficou na pasta

- **`phillips_excel.py`** — Curva de Phillips "flavored" (12m Y/Y, sem intercepto, pesos de inércia
  e expectativa somando 1) → `data/curva_phillips_auditoria.xlsx`, auditável célula a célula.
  Independente do modelo agregado. **Rodar recria a planilha e destrói abas adicionadas à mão.**
- **`referencia/`** — os PDFs do BC (`atualizacao_modelos.pdf` é o boxe de jun/2024 que este modelo
  replica; `modelo_agregado.pdf`/`modelo_desagregado.pdf` são as versões de 2021), os CSVs das
  tabelas dropadas, e `tvp_2026-08-21/` (teste de parâmetro variante no tempo para a transmissão do
  juro real, movido da raiz do projeto em 2026-08-25 — **o script que o produziu não existe**, ver o
  README de lá).
- **`models/curva_juros/`** — material legado, nunca integrado; imports apontam para um layout de
  pacote que não existe mais.
- **`data/`** — artefatos do modelo (`modelo_*`), a planilha da Phillips, e os caches dos pulls
  lentos (`modelo_nuci_fgv.csv`, `modelo_desoc_retro.csv`, `modelo_neutra_pub.csv`, `modelo_irf_pub.csv`).

## Projeções do próprio BC: comunicados + RPM

O texto das duas publicações de política monetária virou dado estruturado **fora desta pasta**, porque
é ETL. As duas alimentam a mesma tabela, `pm_copom_projecoes`, separadas pela coluna `documento`:

- **comunicado**: `connectors/bcb_copom.py` → `_copom_texto.py`. 233 reuniões versionadas em
  `raw_md/central_bank_comunication/`; carga da 206ª (2017-04) em diante, **396 linhas**.
- **relatório** (RPM, chamado RI até 2024-12): `connectors/bcb_rpm.py` → `_rpm_projecoes.py`.
  **109 edições** de 1999-06 a 2026-06 em `raw_md/relatorio_politica_monetaria/`; **1.967 linhas**
  de 108 delas.

O relatório não é redundante: o comunicado publica 2 ou 3 períodos escolhidos, o relatório publica o
caminho trimestral **contíguo**. Por isso o ponto a 6 trimestres à frente existe em toda edição desde
1999, e a série de horizonte relevante passou de 52 pontos (2020→) para **150 (1999-09 → 2026-08)**.
Onde os dois cobrem a mesma célula, batem **exatamente da 264ª reunião em diante** (60 de 60); antes
divergem 0,037 p.p. em média, porque o relatório é vintage posterior (7 a 28 dias) e porque em
2017-2020 o comunicado publicava o cenário **híbrido** (juros Focus com câmbio constante) enquanto o
relatório publica os puros.

**Para o uso aqui como alvo de validação, isso importa**: a projeção da mesma reunião pode existir
duas vezes com números diferentes. Filtrar `documento` é obrigatório — e o relatório é o que dá o
caminho inteiro, não só o HR.

Desde 2026-08-25 há uma terceira tabela no par, `pm_copom_reuniao`: uma linha por reunião com o
**passo de Selic** decidido, das 247 reuniões desde 1999. Não vem de texto — vem da SGS 432 cruzada
com o calendário de reuniões, e é o que fecha o par projeta/faz que a aba Projeções usa.

Levantamento das duas fontes:
[`copom_comunicados.md`](../../../domain/db/brasil/bcb/copom_comunicados.md) (5 regimes de
comunicação, a armadilha do nome do cenário) e
[`relatorio_politica_monetaria.md`](../../../domain/db/brasil/bcb/relatorio_politica_monetaria.md)
(3 formatos de tabela, 5 armadilhas silenciosas do PDF, a grade 2×2 de cenários de 2016-2020).

## Cabecalho de cada grafico (2026-09-14)

Todo grafico desta pasta carrega, dentro do proprio card e acima do plot, as tres linhas do
padrao: titulo, subtitulo derivado e `Fonte: … · <periodo>`. So o titulo e a fonte sao texto
fixo (`CHART_META` no `report.html`); subtitulo e periodo sao reescritos a cada render. A
mecanica e compartilhada -- `/*CHART_HEAD_CSS*/` e `/*CHART_HEAD_JS*/`, de
`analytics/report_structure/chart_head.{css,js}` --, entao o que mora aqui e so o
`CHART_META` e a chamada de `describeChart()`.

**Desde 2026-09-22 sao dois graficos**, os dois da aba Projecoes (`chart-pj-serie` e
`chart-pj-bt`): os 4 da aba do motor e os paineis por input sairam com ela, e com eles o
unico uso da variante `compact`. A aba Condicoes nao tem grafico nenhum de proposito -- ela
e uma matriz de 225 celulas, e o cabecalho de tres linhas existe para um grafico que sai da
pagina como print; o equivalente dela e a legenda de cores mais o card por linha. Nos dois que ficaram uma pill troca o que a linha E --
escala na serie, eixo no backtest --, entao o **titulo tambem e derivado**: ali o unico
texto fixo e a fonte.

Coberto por `tests/test_chart_head_js.js`; o porque e o levantamento de quem faltava
estao em `.claude/rules/lis-dashboards.md`, secao "Every chart carries its own header".

## Pending
- **Aba Projeções — o aviso de previsão velha não aparece mais na página.** Ele morava na
  faixa dentro da caixa verde, que saiu em 2026-09-23. `previsao.frescor` continua no payload e o
  `generate_report` continua imprimindo `AVISO previsao calculada com dado ate …` no console, então
  quem regera é avisado — quem só abre o HTML, não. Se a previsão voltar a envelhecer em silêncio, o
  lugar dela é uma oração na legenda do gráfico, do lado do corte de informação que já está lá, e
  não uma caixa nova.
- **Aba Projeções — a previsão pelo delta da Focus fica indefinida ~8 dias por trimestre.**
  Medido em 2026-09-23: o alvo da 282ª é 2028T2, a Focus só abriu esse trimestre em
  **10/07/2026** e a âncora disponível é o RPM de **25/06/2026** — 15 dias antes —, então o delta
  não tem "antes" para diferenciar e `previsto_focus` sai nulo. Não é acaso: o RPM sai ~8 dias
  depois da segunda reunião do trimestre (273ª→25/09, 275ª→18/12, 277ª→26/03, 279ª→25/06) e a
  Focus abre o trimestre-alvo no dia ~10 do trimestre seguinte, então a janela entre os dois
  produz o buraco **todo trimestre**, justo na semana seguinte a uma decisão. O backtest nunca o vê
  porque corta na data de cada reunião, onde o RPM já saiu — daí `anc_dias` ser 34–49 nas 18 e 89
  aqui. Enquanto não houver decisão sobre isso, a aba fica sem ponto previsto nesses dias e diz
  isso na chamada.
- **Antecipar a projeção — o que falta testar.** O delta da Focus ganha do ingênuo (MAE 0,082 contra
  0,106) com repasse 1:1 e sem ajuste nenhum. Três coisas por ordem de retorno: (a) a Focus de
  **administrados** e de **livres** separadas, já que é o bloco de administrados que o modelo não tem;
  (b) o delta do **IPCA de curto prazo** (a Focus mensal dos próximos 3 meses), que é o canal pelo
  qual a notícia entra; (c) um coeficiente estimado no lugar do 1:1 — com n=17 isso é pescaria, então
  só vale quando a amostra crescer. Não tentar melhorar o modelo agregado para esta finalidade: o
  backtest mostra que o problema é o conjunto de informação trimestral, não o ajuste. Medido por
  tipo de horizonte, a **expansão é o caso mais fácil** (MAE 0,080 pela Focus contra 0,089 do
  ingênuo) e a **revisão o mais difícil** (0,084 contra 0,125), o que aponta o intervalo entre
  âncora e reunião como a variável a explorar antes de qualquer coisa nova.
- **Os artefatos da previsão entraram no botão Regerar** (2026-08-31, depois de o usuário regerar o
  relatório e a previsão continuar a de seis dias antes). `generate_report.py` continua só lendo
  `data/` — de propósito: encadear `salvar()` dentro do `run()` custaria 36 rodadas do espaço de
  estados a cada geração. O que mudou é uma camada acima: `domain/dashboards/manifest.yaml` declara os
  três passos de recálculo deste relatório em `procedures:` (`painel`, `modelo`, `previsao`), e
  `status.gerar()` — que é o que o botão **Regerar** da aba "Status dashboard" chama — refaz antes os
  que estiverem atrás. Medido em 2026-08-31: `salvar()` em 50,5s + geração em 15,8s. Os dois passos do
  modelo são declarados **trimestrais**, então não são refeitos a cada boletim Focus; a previsão é
  diária.
  Em paralelo, `antecipa_copom.frescor()` compara o `corte_usado` gravado no artefato com o `MAX` das
  seis tabelas que `antecipar()` lê e `_load_antecipa()` embute isso em `previsao.frescor`. Até
  2026-09-23 a caixa da previsão imprimia isso como faixa — laranja se o HTML foi feito com artefato
  velho, verde se em dia —, e **com a caixa removida a faixa não tem mais onde aparecer**: o campo
  continua no payload e o aviso continua no console da geração, mas a página não o mostra.
  **O texto da faixa foi reescrito em 2026-09-01** (correção do usuário: a prosa dos dashboards
  não pode ser a nossa conversa sobre eles). Ela não imprime mais nome de tabela nem comando de
  terminal: `_FONTES_FRESCOR` passou a guardar `(coluna, nome)` — "a pesquisa Focus", "as
  projeções publicadas pelo Copom" — e `frescor()` devolve `fonte_nome` junto do `fonte_ref`, que
  segue existindo para o aviso de console da geração. O teste passou a exercitar a faixa laranja
  **sinteticamente**: ela não aparece no payload de um relatório recém-regerado, que é justamente
  o estado em que ninguém percebe que o texto dela envelheceu.
  **Segue pendente** o agendamento (junto do `bcb_copom`), que é o que tiraria a dependência de
  alguém clicar. Ver `domain/dashboards/CLAUDE.md`.

- **Aba Condições — a célula da próxima reunião na linha de projeção do BC é repetição, e
  deveria virar previsão.** O usuário pediu o observado por ora e disse que define o número
  depois de rever a aba Projeções. Quando entrar, a célula precisa dizer na tela que é
  estimativa — hoje ela é indistinguível de qualquer outra repetição cinza.
- **Aba Condições — ampliar o recorte.** As 25 variáveis de hoje cobrem inflação, atividade,
  condições financeiras e externas. Fora, por falta de dado e não de método: PIM/PMC/PMS, o
  hiato do BCB e o CDS de 5 anos (`cmb_risco_pais` é xlsx exportado à mão e costuma estar
  semanas atrás). Acrescentar qualquer um é uma entrada nova em `_spec()` — a mecânica de
  corte, σ e cor já é genérica, e desde 2026-09-22 vale para série diária, mensal **e
  trimestral**. **Antes de acrescentar, conferir que o grupo do `calendar_2026.yaml` tem
  `reference_period` nas entradas**: sem ele `regra()` devolve `None` e a série não tem como
  ser cortada por divulgação. O `bcb_focus` é a exceção que já existe — não tem
  `reference_period` (cada boletim é o estado corrente, não um período fechado), e por isso
  entra como `grupo_agenda`, que só alimenta a agenda e não corta série.
- **Aba Condições — o calendário de 2026 tem um rótulo errado, e ele está contornado, não
  corrigido.** `bcb_credit_note` carimba `2026-06` em 01/07 **e** em 30/07; pela cadência do
  grupo (abril→28/05, junho→30/07, julho→28/08) a primeira deveria ser `2026-05`. O módulo
  desempata pela data mais tarde e o ajuste da regra usa uma entrada por referência, então
  nenhuma célula fica errada — mas a entrada do YAML segue errada e o mês de maio do crédito
  cai na regra estimada em vez da data exata. Corrigir no `calendar_2026.yaml` é de uma linha.
- **Aba Condições — 55 das 225 células têm data de divulgação estimada**, porque
  `calendar_2026.yaml` só cobre 2026 e a janela de 8 reuniões chega a nov/2025. Em 6 delas a
  estimativa cai perto demais do fechamento para o erro da regra ser inofensivo, e a página
  marca. O corretivo definitivo é um calendário com as entradas de 2025; enquanto não houver,
  a marca é a resposta honesta.
- **Aba Condições — virada de ano.** `condicoes_copom.py` lê `calendar_2026.yaml` por nome
  fixo. Quando o calendário virar, ver `domain/release_calendar/ROLLOVER.md`; sem reunião
  futura no arquivo a aba degrada com mensagem em vez de quebrar, mas para de servir.
- **Aba Projeções — comparar trajetória contra trajetória.** A aba construída em 2026-08-25 usa um
  ponto por reunião (o horizonte relevante). O RPM publica o **caminho trimestral inteiro** de cada
  edição desde 1999, e o modelo desta pasta produz um caminho também — então o alvo de validação
  natural é curva contra curva, não ponto contra ponto: se o cenário reproduz a trajetória que o BC
  publicou, está calibrado contra o que o próprio Comitê olhou. Isso não cabe na aba atual, cujo eixo
  é a reunião; é uma segunda seção com o eixo no período projetado e uma edição selecionável.
- **Aba Projeções — a variável que falta para virar função de reação.** A correlação de 0,27 entre
  desvio e passo é o que se mede hoje, e ela é fraca por construção: o desvio pequeno é resultado da
  política, não ausência de reação. O passo seguinte é acrescentar o juro real contra a neutra (que a
  eq. (3) já estima nesta pasta) — sem ele, duas reuniões com o mesmo desvio e Selic em 8% ou em 15%
  entram na mesma nuvem.
- **RPM: 43 tabelas lidas e não gravadas, todas por motivo registrado em `avisos`.** 32 são cenários
  **mistos** da grade 2×2 de 2016-2020 (juros de um tipo, câmbio de outro), que não cabem numa coluna
  `cenario` que classifica só o juro — precisariam de uma dimensão de câmbio. 4 são o par
  Básico/Alternativo com o mesmo juro (RI de dez/2002 e mar/2003), 4 ficaram sem cenário identificado
  (título em fonte de subconjunto sem cmap legível) e 7 foram classificadas por **ordem** das tabelas
  na página, e por isso têm `cenario_publicado` nulo. O **leque** de confiança (limites de 50/30/10%)
  está no `.md` de cada edição e não foi gravado, por decisão explícita de escopo. O RI de 1999-06
  não entra: publica o leque só como gráfico.
- **Equação (5) dentro do filtro** — exige (a) π^e como estado e (b) uma convenção para o que o
  modelo espera dos exógenos em cada trimestre da amostra, que o boxe não publica e que move E_t π
  mais do que os φ. É a única via para testar se o α₁ᴵ se corrige.
- **Bloco de preços administrados** — o boxe do RI de set/2017. É a **única premissa que sobrou** no
  cenário, e é o que separa o nosso IRF completo da primeira linha do Graf 4B. Alvos de validação
  já levantados: 10% de depreciação → +1,65 p.p. nos administrados e +0,72 nos livres, fechando
  +0,96 no IPCA (texto do boxe, p. 102-103).
- **Confirmação em browser real** do relatório — nunca feita (sandbox sem browser).
- **`referencia/tvp_2026-08-21/`** — decidir se o teste de TVP vira script versionado (hoje só o
  resultado sobreviveu) ou se é descartado. O veredito depende de qual neutra se assume e não
  sobrevive fora da amostra, então a barra para reescrevê-lo é alta.
- **Hiato mundial** — excluído por decisão. Se voltar: construível de `cmb_comex_pais` (pesos de
  exportação) + PIB dos parceiros via FRED/BIS, que é a receita da nota 9 do boxe.
- **CDS pré-2008** — a UIP fica inativa em 17 dos 81 trimestres. O EMBI+ do IPEADATA emendaria.
- **`models/curva_juros/`** — decidir entre integrar ou descartar.
- **Comunicados: o que o parser lê mas não grava** — câmbio inicial do cenário e bandeira tarifária.
  São atributos de reunião, e a tabela irmã onde eles cabem já existe: `pm_copom_reuniao`, criada em
  2026-08-25 com a decisão de Selic. O câmbio inicial explica boa parte das revisões de projeção
  entre reuniões, e acrescentá-lo é uma coluna nova ali, sem migração. A decisão/direção saiu desta
  lista: está gravada, e de fonte melhor que o parser (SGS 432 cobre desde 1999, o texto só da 206ª).
- **Atas não estão no pipeline** — só o comunicado. A ata sai ~1 semana depois, em PDF.
