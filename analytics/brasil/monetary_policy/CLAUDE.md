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
node tests/test_monetary_policy_js.js                               # asserções do relatório
uv run python tests/test_eq5_expectativas.py                        # 19 asserções (eq. 5)
```

| Módulo | O que faz |
|---|---|
| `modelo_painel.py` | Painel trimestral dos insumos. Escreve **dois**: `_est` (HP até 2023T4, fiel ao conjunto de informação do boxe — o único em que comparar parâmetros é legítimo) e `_full` (HP até hoje, para estender os estados e partir daí nos cenários). |
| `modelo_agregado.py` | Espaço de estados + estimação + decomposições + simulador + validações. `rodar()` grava tudo em `data/`. |
| `generate_report.py` | Lê os artefatos de `data/` e injeta em `report.html`. |

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
| Cenários | 12 trajetórias pré-simuladas + a escada de validação do IRF | pronta |
| Decomposição | contribuições das eqs. (1), (2) e (3) | pronta |
| Taxa Neutra | r* latente (IS e Taylor) + as 5 medidas publicadas | pronta |
| Hiato do Produto | latente vs. `pm_hiato_produto` + dispersão da suíte | pronta |
| Projeções do Copom | `pm_copom_projecoes` | **stub** |
| Apêndice | descrição do modelo + validação dos parâmetros + notas | pronta |

Os **cenários** da aba homônima são pré-calculados em Python (`cenarios_padrao()`): caminho de Selic
(Focus / constante / ±100 pb por 4T) × tratamento da expectativa (endógena pela eq. 5, default / fixa
na Focus / convergindo à meta). As duas premissas fixas são contrafactual — a distância até a
endógena é o tamanho do canal de expectativa.

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

## Comunicados do Copom

O texto dos comunicados virou dado estruturado **fora desta pasta**, porque é ETL:
`connectors/bcb_copom.py` → `domain/db/brasil/bcb/_copom_texto.py` → `pm_copom_projecoes`. As 233
reuniões que a API devolve ficam versionadas em
`repository/monetary_policy/raw_md/central_bank_comunication/`; a tabela carrega da 206ª (2017-04),
396 linhas. Levantamento da fonte, os 5 regimes de comunicação e a armadilha do nome do cenário:
[`domain/db/brasil/bcb/copom_comunicados.md`](../../../domain/db/brasil/bcb/copom_comunicados.md).

## Pending

- **Aba Projeções do Copom** — a única não construída. Uso natural: alvo de validação do cenário. Se
  o modelo reproduz a projeção que o BC publicou para o horizonte relevante, está calibrado contra o
  número que o próprio Comitê olha. Ler `copom_comunicados.md` antes: sem filtro de `regime` três
  conceitos de horizonte relevante se misturam, e `cenario` classifica pelo condicionamento, não
  pelo rótulo publicado.
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
- **Comunicados: o que o parser lê mas não grava** — câmbio inicial do cenário, bandeira tarifária,
  decisão/direção da Selic. São atributos de reunião, então pedem uma tabela irmã
  `pm_copom_reuniao`. O câmbio inicial explica boa parte das revisões de projeção entre reuniões.
- **Atas não estão no pipeline** — só o comunicado. A ata sai ~1 semana depois, em PDF.
