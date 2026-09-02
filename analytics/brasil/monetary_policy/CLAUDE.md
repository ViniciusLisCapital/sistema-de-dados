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
| **Modelo BC — Agregado** | o simulador **rodando no navegador** (aba default) | pronta |
| Condições para a reunião | `condicoes_copom.py` — MySQL + `domain/release_calendar/` | pronta |
| Projeções do Copom | `pm_copom_projecoes` × `pm_copom_reuniao` | pronta |
| Apêndice | descrição do modelo + validação dos parâmetros + notas | pronta |

**Quatro abas foram removidas em 2026-08-25** a pedido do usuário — Cenários, Decomposição, Taxa
Neutra e Hiato do Produto — junto com os `_load_*` delas, para o payload não carregar série que
ninguém lê (a seção 13 do teste cobra isso nos dois sentidos). O que **não** mudou: `rodar()`
continua gravando todos os artefatos em `data/`, e dois consumidores dependem deles — o
`_motor_cfg()` lê `modelo_cenario_focus__eq5.csv` para a curva de Selic da Focus, e o teste JS lê os
12 CSVs de cenário e o `modelo_irf.csv` como referência do Python. Antes essa referência vinha pelo
payload; ler do artefato é melhor, porque não passa pelo arredondamento de 4 casas do `_ser()`.

Os **cenários** seguem pré-calculados por `cenarios_padrao()`: caminho de Selic (Focus / constante /
±100 pb por 4T) × tratamento da expectativa (endógena pela eq. 5, default / fixa na Focus /
convergindo à meta). As duas premissas fixas são contrafactual — a distância até a endógena é o
tamanho do canal de expectativa. Hoje só o teste os lê.

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

### A aba Modelo BC — Agregado

A única aba do projeto em que **o modelo roda no navegador**: `simular()` está portado para JS e roda
a cada mudança de input, porque a pergunta que ela responde ("e se eu fixar isto e deixar aquilo
endógeno?") tem combinação demais para pré-calcular. Divergir do Python é bug — a seção 19 do teste
roda o motor JS nas **mesmas 12 configurações** de `cenarios_padrao()` e exige que batam série a
série (máx. 5e-5, o piso do arredondamento do payload).

Duas seções: o que o modelo **estima** (Inflação, Hiato, Juros, Expectativas) e o que ele **recebe**.
A seção de inputs segue a aba Ridge do FX Report — caixas sempre visíveis, uma por trimestre; atalhos
que **preenchem as caixas** em vez de serem modos paralelos; gráfico próprio por input.

Cada input é de um de três tipos, e o eixo é próprio daqui:

| tipo | quem resolve | inputs |
|---|---|---|
| **endógeno** | o modelo, com toggle Endógeno/Manual | Selic (eq. 3), expectativa (eq. 5), câmbio (eq. 4) |
| **premissa** | o boxe, por fora | π^A, IC-Br, r̂p, Clima² El Niño/La Niña |
| **estimativa do modelo** | o filtro | r* da IS, r* da Taylor, h₀, choque s^h |

**As duas neutras não são redundância.** Compartilham a mesma tendência HP e diferem só no desvio,
que tem estado próprio em cada equação — o que muda é a **identificação**: a da IS (eq. 2.3) sai do
que a atividade diz sobre o quanto a política tem sido restritiva; a da Taylor (eq. 3.1), do que a
Selic observada revela sobre onde o Copom acha que a neutra está. A distância entre elas (hoje 7,81
vs 8,28) é política sistematicamente mais apertada do que a demanda pedia. A da Taylor **só age
quando a Selic está endógena**.

**A eq. (3) é extensão nossa, não porte** — `simular()` só aceita a Selic como caminho dado. Não vira
ponto fixo novo (a Taylor sai recursivamente dado o vetor de expectativa), mas troca o **sinal de um
choque de inflação**: com a Selic exógena, expectativa maior derruba o juro real ex-ante e *abre* o
hiato; com o Taylor ligado o BC reage e o hiato *fecha*. Esse par está na seção 22 do teste.

Armadilhas já pisadas — cada uma custou um bug:

- **`vals` guarda números exatos**, não a string arredondada de exibição: guardar o exibido faz o
  cenário default deixar de reproduzir o Python bit a bit.
- **`s^h` decai por β₅ no buffer** além do horizonte, ao contrário de todos os outros inputs (que
  seguram o último valor). É o único `_mtVals` com `decai`; segurá-lo vira choque permanente.
- **Duas âncoras diferentes no payload**: `ini.selic`/`ini.pi_e` são lidos **em t₀** porque são a
  defasagem que as equações usam; `dflt.selic_ult`/`dflt.pi_e_focus` são o **último valor publicado**,
  que já pode estar um trimestre à frente — e são eles que "Selic constante" e "expectativa fixa na
  Focus" significam. Confundir os dois acusou em 11 dos 12 cenários.
- **A inflação importada é o IC-Br, não o π\* cru**: o modelo usa π* = variação do índice − meta/4,
  então o card mostra a variação do índice e converte internamente. Sem isso, digitar 0 seria um
  choque desinflacionário de meta/4 sem o usuário perceber.
- **Administrados**: o atalho "Projeção do Copom" trimestraliza `pm_copom_projecoes` por **divisão
  simples**, não raiz quarta (é assim que `ipca_4t` acumula), e no ano corrente desconta o já
  observado antes de dividir pelo que falta.
- **O horizonte não é janela de exibição**: depois dele o último trimestre digitado se repete (o
  `vec()` do Python faz o mesmo), porque a eq. (5) precisa de condicionante definido no buffer.
- **O marcador de horizonte relevante tem duas fontes** e `_mtHR()` prefere a declarada pelo próprio
  Copom (`motor_cfg.hr`), com a regra dos seis trimestres (`MT_HR_TRI`) como fallback. Divergir é
  legítimo (painel atrasado) mas troca a fonte em silêncio, então `generate_report.py` imprime AVISO.
- **O teste de folga substitui o raio espectral**: em JS calcular autovalor não vale o código, então
  o motor resolve com a folga normal e de novo com o dobro e compara. Foi o que calibrou `FOLGA=40`.
- **Um key fora de `MT_GRUPOS` simplesmente não é renderizado** — a seção 25 cobra a cobertura nos
  dois sentidos.
- **Cenários salvos guardam a configuração, nunca os números** (`localStorage`,
  `lis_mp_motor_cenarios_v1`): um cenário plotado é re-simulado do zero.

### A aba Condições para a reunião (2026-08-25)

O que o Copom tinha na mesa na última decisão contra o que já está na mesa para a próxima,
17 variáveis em quatro blocos — inflação corrente (IPCA 12m, média dos 5 núcleos e EX3 em
mm3m anualizada), atividade e mercado de trabalho (IBC-Br 3m/3m anualizada, desocupação da
PNAD, saldo do CAGED), expectativas da Focus (IPCA de dois anos + 12m, PIB de dois anos,
Selic) e condições financeiras (juro real ex-ante, PTAX, Brent, IC-Br). Mais a agenda de
divulgações até o corte, **filtrada ao que alimenta uma das linhas** — o calendário inteiro
tem relatório próprio. Renova-se sozinha quando uma reunião passa; **não há histórico de
reuniões anteriores**, por decisão explícita.

**O ponto todo é a regra de corte, e ela não é sobre a reunião — é sobre a natureza do
índice de cada série.** Uma série de mercado ou da Focus é indexada pela data em que o dado
existiu: corte direto. Uma série mensal é indexada pelo **mês de referência** e só é
publicada semanas depois — o IPCA de julho está no banco com data 01/07 e saiu em ~13/08, de
modo que na reunião de 05/08 o Comitê ainda estava com o de junho. Ler o banco por
`date <= reunião` daria julho, e **não levantaria exceção nenhuma**: devolveria um número
plausível do período errado. Para essas, a data de divulgação vem do `calendar_2026.yaml`.

O corte é `datetime(dia 2, 18:30)`, não a data. Três consequências que já custariam bug:
o horário decide o IC-Br (o de julho saiu às 14:30 de 05/08, o dia da 280ª — entrou por
quatro horas); no dia 2 antes das 18:30 a reunião em curso ainda é a *próxima*, senão a aba
compararia a reunião consigo mesma; e a "Selic esperada na próxima reunião" fixa o **mesmo
rótulo da Focus** (`R6/2026`) nas duas colunas — recalculá-lo por corte compararia duas
reuniões diferentes.

Onde o calendário não tem a entrada exata (ele começa em 2026-08-13, depois da 280ª), a data
é **estimada** pela regra ajustada do grupo: mediana da defasagem em meses e mediana do
índice de dia útil. `regra()` devolve junto o **erro máximo medido** contra as próprias
entradas, e `montar()` só avisa quando a estimativa cai a menos desse erro do corte — ou
seja, quando ele poderia virar a célula. O erro não é uniforme: IPCA e IPCA-15 são ancorados
no mês e fecham em ≤4 dias; o IC-Br sai em cadência de 4-5 semanas ancorada em **quarta-feira**
e a regra mensal erra até 5 dias ali (nunca exercida — o IC-Br tem entrada exata desde
2026-05).

Outras decisões que custaram uma rodada cada:

- **`_sa()` começa em 2000.** `inflc_agregados` guarda o IPCA desde 1980, e ajuste sazonal
  aditivo numa série que vai de 80% ao mês para 0,4% produzia fator sazonal de −2,0 p.p. em
  agosto: o "dessazonalizado" saía **mais volátil que o bruto** (sd 1,03 contra 0,39), e esse
  ruído ia direto para o σ que define a cor. Com a janela certa, serviços mm3m anualizada
  passou de "+0,39, z=+0,13" para "+1,81, z=+1,21" — o sinal hawkish estava escondido pelo
  próprio ajuste.
- **σ é escala robusta (1,4826 × MAD), não desvio-padrão.** Dez anos de história contêm
  2020-2021, e com desvio-padrão aquele episódio vira a régua.
- **Nível de preço entra em variação percentual** (`modo='pct'`, hoje só o câmbio): o repasse
  cambial é proporcional, e 10 centavos a 3,00 não são a mesma notícia que 10 centavos a 6,00.
  O σ dessa linha é medido em 100×Δlog, senão o z dividiria centavos por uma escala de log.
  Brent e IC-Br são o mesmo tipo de variável e continuam em nível — é um campo, se mudar.
- **Fatores sazonais congelados** até dezembro do ano anterior: reestimá-los a cada rodada
  faria o valor "na reunião passada" mudar junto com o de hoje, e a diferença entre as duas
  colunas deixaria de ser só dado novo.
- **`sinal = 0` não recebe cor.** As expectativas de Selic da Focus são *reação* do mercado à
  decisão passada, não condição que antecede a próxima — colori-las seria circular. Aparecem
  porque o número interessa; só não recebem veredito.
- **"Sem dado novo" não é "neutro".** As duas coisas têm `z = 0` e significados opostos —
  mudez contra ausência de movimento. Contá-las juntas foi bug na primeira versão do resumo.
- **A coluna "hoje" é limitada pelo banco**, não só pelo calendário: se o calendário diz que
  já saiu dado mais recente e o ETL não rodou, a linha vem marcada `pendente` em vez de
  afirmar um valor que não está carregado.

Cobertura: seção 32 de `tests/test_monetary_policy_js.js` (o payload já pronto — nenhuma
célula da coluna "na reunião" veio de divulgação posterior ao corte, as categorias do resumo
particionam, a cor sai do z) e `tests/test_condicoes_copom.py` (a mecânica que produz aquelas
datas, varrida dia a dia contra checagem independente). O primeiro não alcança o segundo:
errar o mês não lança exceção.

### A aba Projeções do Copom (2026-08-25)

A projeção do BC para o horizonte relevante contra o **passo de Selic da mesma reunião** — o que o
Comitê projetava contra o que ele fez —, mais a **previsão da próxima**. Três seções: a série
temporal (barras de pontos-base no eixo da direita, projeção no da esquerda, e o ponto previsto em
losango vazado ligado por tracejado), o **backtest** do que estimamos contra o que o BC publicou, e a
tabela reunião a reunião. Pills de cenário (juros esperado | constante), escala (nível | desvio da
meta), **defasagem** (mesma reunião | próxima) e **previsão** (delta da Focus | modelo | ingênuo).

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
traces separadas — uma ponte tracejada sem legenda e sem hover, e um losango vazado verde — e nunca
como mais um ponto da série dourada: é o único número da aba que ninguém publicou, e a caixa verde
acima do gráfico diz de onde ele vem (âncora, documento, delta, MAE do método, corte de informação).
Três decisões que a seção 33 do teste fixa, porque nenhuma delas lança exceção se quebrar:

- **Só no cenário de juros esperado.** A previsão é construída condicionando na curva de Selic da
  Focus, que *é* o condicionamento desse cenário. No de juros constante ela não tem leitura, e
  desenhá-la ali seria pior que omitir: o ponto pareceria continuar uma série que ele não continua.
- **Só com "mesma reunião".** Com defasagem a série desenhada para na penúltima reunião (a última
  não tem passo seguinte), então o tracejado saltaria por cima de uma reunião **já publicada**.
- **A linha da meta se estende ao ponto previsto**, senão o único ponto do gráfico sem referência
  seria justo o que mais precisa dela. E a meta dele vem do mesmo dicionário das linhas publicadas,
  com `meta_estendida` marcado — na escala "desvio" a régua tem de ser a mesma.
- **Bolinha, não losango.** O marcador é círculo do mesmo tamanho dos da série publicada, só em
  verde: o losango vazado da primeira versão foi rejeitado pelo usuário — lia como sujeira, não
  como ponto. O que distingue previsão de dado publicado é a cor e o tracejado que leva até ela.

**O backtest também aponta para a frente** (2026-08-25, ainda a pedido do usuário): no eixo Nível
as três linhas de método ganham um ponto extra na próxima reunião, com uma vertical pontilhada
separando o que já pode ser conferido do que não pode, e a linha do publicado recebe `null` ali — é
essa parada que sinaliza a ausência de contrapartida do BC. No eixo **Erro** não estende, porque não
há número publicado para subtrair. O valor do ponto extra é lido pelo mesmo `pjPrevBruto()` que
alimenta o gráfico principal e a caixa verde, e o teste cobra que os três batam: são três
consumidores do mesmo número na mesma tela.

**As duas tabelas da aba são click-drop** (`<details class="tbl-fold">`, mesma mecânica do
apêndice), fechadas por default — 17 e 107 linhas abertas empurravam tudo que vem depois para fora
da tela. O `<summary>` recebe a contagem pelo JS, senão a tabela fechada não diz o que tem dentro.

O relatório **não roda o modelo**: `antecipa_copom.salvar()` grava `data/antecipa_backtest.csv` e
`data/antecipa_previsao.json`, e `_load_antecipa()` só os lê. Sem os arquivos a aba mostra o
histórico publicado e nada mais — `antecipar()` roda o espaço de estados duas vezes e o backtest 34,
o que não cabe num `generate_report`. O contrapeso é que os artefatos envelhecem em silêncio: o
`corte_usado` fica no JSON e a caixa avisa quando ele é anterior à reunião.

A meta vem de `inflc_meta`, anual e terminando em 2026; os trimestres projetados vão a 2028. A meta
do último ano publicado é estendida para frente, o que sob o regime de **meta contínua** (3%, desde
janeiro de 2025) não é extrapolação — é o próprio desenho da meta. As reuniões afetadas vêm marcadas
com `meta_estendida` e o `generate_report.py` imprime a contagem.

Correlação desvio × passo: **0,27** contemporânea e 0,28 contra o passo seguinte, em 107 reuniões. O
sinal é o esperado e a magnitude modesta também: se o Copom já reagiu, a projeção condicionada aos
juros esperados volta para perto da meta, e o desvio pequeno é *resultado* da política. Por isso o
cenário de **juros constantes** é a leitura mais informativa dos dois — e é justo o que o BC parou
de publicar em 2024. Nenhuma das duas é estimativa de função de reação: falta o juro real contra a
neutra, que a eq. (3) deste modelo usa e que separa duas reuniões com o mesmo desvio e Selic em 8%
ou em 15%.

Cobertura: seção 33 de `tests/test_monetary_policy_js.js` (107 asserções — homogeneidade do
horizonte, ausência de duplicata por reunião, `bps` conferido contra os dois níveis que viajam no
payload, `pjCorr` contra Pearson calculado à parte, e o que cada pill faz com os traces).

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

## Pending
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
  seis tabelas que `antecipar()` lê, `_load_antecipa()` embute isso em `previsao.frescor`, e a caixa
  da previsão imprime uma faixa — laranja se o HTML foi feito com artefato velho, verde se em dia.
  Funciona em arquivo estático, então viaja com o relatório enviado por email.
  **O texto da faixa foi reescrito em 2026-09-01** (correção do usuário: a prosa dos dashboards
  não pode ser a nossa conversa sobre eles). Ela não imprime mais nome de tabela nem comando de
  terminal: `_FONTES_FRESCOR` passou a guardar `(coluna, nome)` — "a pesquisa Focus", "as
  projeções publicadas pelo Copom" — e `frescor()` devolve `fonte_nome` junto do `fonte_ref`, que
  segue existindo para o aviso de console da geração. O teste passou a exercitar a faixa laranja
  **sinteticamente**: ela não aparece no payload de um relatório recém-regerado, que é justamente
  o estado em que ninguém percebe que o texto dela envelheceu.
  **Segue pendente** o agendamento (junto do `bcb_copom`), que é o que tiraria a dependência de
  alguém clicar. Ver `domain/dashboards/CLAUDE.md`.

- **Aba Condições — ampliar o recorte.** As 17 variáveis de hoje cobrem inflação corrente,
  atividade e mercado de trabalho, expectativas e condições financeiras. Fora, todos por falta
  de dado e não de método: PIM/PMC/PMS e o hiato do BCB, crédito e fiscal, CDS de 5 anos
  (`cmb_risco_pais` é CSV exportado à mão e costuma estar semanas atrás) e Treasury de 10
  anos (não está no banco). Acrescentar qualquer um é uma entrada nova em `SPEC` — a mecânica
  de corte, σ e cor já é genérica. **Antes de acrescentar, conferir que o grupo do
  `calendar_2026.yaml` tem `reference_period` nas entradas**: sem ele `regra()` devolve
  `None` e a série não tem como ser cortada por divulgação. O `bcb_focus` é a exceção que já
  existe — não tem `reference_period` (cada boletim é o estado corrente, não um período
  fechado), e por isso entra como `grupo_agenda`, que só alimenta a agenda e não corta série.
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
