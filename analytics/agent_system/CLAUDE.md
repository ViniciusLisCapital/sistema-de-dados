# analytics/agent_system/ — diagrama do sistema de agentes e o F(A)

Gera `team_materials/structure_materials/Sistema de Agentes.html`: um diagrama SVG da visão geral
— processos de entrada, as três fontes do agente (MySQL, ferramentas, conhecimento), cada uma
apontando para cada agente, e o ciclo dos agentes (rodada 1 → P1 → rodada 2 → P2 → report final →
PF*), no desenho do usuário de 2026-10-07. Não está no manifesto de dashboards.

```
uv run python -m analytics.agent_system.generate_report
```

- **À mão, no `report.html`:** caixas, setas e o estado de cada bloco (existe / em construção /
  planejado), em `SPECS.geral` e `rodadasGeral()`; a lista `FERRAMENTAS`; o texto de cada detalhe.
- **Lido na geração:** contagens do registry, dos connectors e das notas do vault por área; a lista
  de dados do câmbio, da seção V.I do `SISTEMA_AGENTES.md` (com a fonte de cada tabela pelo
  registry).

## Guia expansível

O diagrama é um guia expansível (pedido do usuário, 2026-10-07): seta ou caixa com entrada em
`DETALHES` ganha o selo "+" e abre uma caixa (`<dialog>`) com o "under the hood". Para acrescentar
um detalhe: uma entrada em `DETALHES` (chave `<fonte>><agente>` para as setas do leque, ou `det` na
caixa) e a função que monta o HTML. Ir aos poucos, sem encher de conteúdo.

Hoje: **MySQL → Câmbio** (como os dados chegam e as tabelas da lista, lidas da V.I do
`SISTEMA_AGENTES.md`), **Ferramentas** e **Câmbio · report 1** (as perguntas centrais, lidas da Parte 1
do mapa conceitual), e as duas mesmas caixas da política monetária (**MySQL → Política monetária**, da
V.II, e **Política monetária · report 1**; 2026-10-21, quando o agente passou a existir). O tratamento de cada tabela (as métricas do F) não entra na caixa: é do sistema,
não do usuário (2026-10-07). Tabela da lista fora do registry vira aviso na página.

Conferido em Chrome headless (2026-10-07): zero exceções, as três caixas abrem, sem rolagem
horizontal a 390 px.

## dados/ — o retrato de dados do ciclo (A → F(A))

```
uv run python -m analytics.agent_system.dados {cambio|politica_monetaria} [--ciclo AAAA-MM-DD] [--refazer]
```

Grava em `obsidian/ciclos/<data>/dados/`: `A/` (cada tabela da lista do agente, um `.csv.gz`, mais
`_manifesto.json` com a consulta; fora do git), `F_<agente>.md` (o que o agente lê) e `G/` (vazia,
para as funções G do agente). Regras de SISTEMA_AGENTES.md IV.iv.

- `motor.py`: igual para todo agente. Lê a lista da seção V, **levanta se a declaração do agente
  divergir dela**, extrai A uma vez por ciclo (compartilhado entre agentes) e calcula F **a partir
  dos arquivos de A**, nunca do banco. Leituras: `pct`, `dif`, `fluxo`, `media`, `var_mensal`; o
  grupo "Endógeno" ganha a leitura completa (percentis, mín–máx de 10 anos).
- `especiais.py`: F próprio de curva DI (prazos redondos e Selic precificada por reunião, com o
  `caminho_di` do relatório de política monetária), Focus, calendário, decisões e projeções do Copom.
- `cambio.py`: as tabelas do câmbio, as séries e a leitura de cada uma, e as leituras combinadas
  (o real e os pares: variação, volatilidade, carry). Agente novo = um arquivo destes e uma linha em
  `AGENTES` no `__main__.py`.
- `politica_monetaria.py` (2026-10-21): as 69 entradas da V.II (68 aprovadas mais o `comm_icbr_usd`, 2026-10-21), até o grupo ix, "Fora da lista" (fora do
  F). Tabela que o câmbio também lê sai da declaração dele (`de`/`so`, abaixo): mesma consulta,
  outras séries, e o A do ciclo serve aos dois. F próprio: ciclo de juros em curso, projeções da
  última reunião e o horizonte relevante nas últimas oito, hiato e as revisões entre edições, QPC,
  recortes do BC refeitos dos subitens (`inflc_dim`; batem com `inflc_agregados`), fatores da DLSP,
  EFGG, contas nacionais. Combinadas: a Selic por reunião na curva DI e na Focus, e o juro real
  contra o neutro do QPC.
- **Tabela de outro agente: `motor.de(modulo, nome, recorte=None, **mudar)` e
  `motor.so(modulo, nome, chaves, ...)`** (2026-10-22). Copiam a declaração do outro agente: mesma
  consulta, mesmo arquivo de A, outras séries. Mudar a consulta exige `variante`. Antes de extrair,
  `gerar()` roda `conferir_consultas()` sobre **todos os pares** de `AGENTES`: mesmo arquivo de A com
  consulta diferente levanta.
- O F é gravado por último, depois do retrato do conhecimento: se o retrato falhar, o F não fica e
  rodar de novo funciona; `--refazer` apaga o F antigo antes de extrair.
- `--sem-literatura` (no `dados` e no `conhecimento`): o retrato leva só o mapa conceitual e, na PM, o
  Copom da camada 1. O mapa é obrigatório; `INDICE.md` e `retrato.json` dizem que o retrato é sem
  literatura; um retrato existente feito no outro modo levanta em vez de passar como "já existe".
- **Os sete agentes** (2026-10-22): `cambio`, `politica_monetaria`, `inflacao`, `atividade`, `fiscal`,
  `externo`, `expectativas`, um módulo cada, listas em V.I–V.VII do `SISTEMA_AGENTES.md` (V.VII termina
  em "*Fim das listas por agente.*"). Tabelas que os novos agentes tiram de câmbio e PM vêm por `de`/`so`;
  as que vieram de outro agente novo levam `variante="<agente>"` (hoje só recortes da
  `expc_focus_periodo` em inflação, atividade e fiscal), a unificar quando o dono as declarar.
- `Tabela.variante`: outra consulta da mesma tabela que a de outro agente, em outro arquivo de A (a
  curva americana inteira do agente de PM vai para `us_interest_rate__curva.csv.gz`; o câmbio lê
  três vértices). Sem ela, consulta diferente no mesmo arquivo levanta.
- A lista aceita um item com várias tabelas ("- `a`, `b`, `c`: papel"); série trimestral sai com
  Δ 1t/4t; `dims=()` para tabela sem coluna de dimensão.
- `fisc_efgg`: o `geral_` é a soma das três esferas, sem consolidar; o F diz para ler a variação,
  não o nível.
- O F(A) é fixo no ciclo: rodar de novo para a mesma data para; `--refazer` reextrai. **`--refazer`
  reextrai TODAS as tabelas do agente, inclusive as que ele divide com outro agente no A do ciclo**;
  num ciclo em uso, refaça só o texto do F com `motor.montar_f` sobre o A que já está lá.
- `Tabela.fora` tira da conta uma tabela da lista com defeito conhecido (hoje nenhuma; a
  `cmb_fluxo_cambial` saiu da lista em 2026-10-07); `Tabela.nota` imprime um defeito conhecido no F (hoje uma: a da `cmb_fx_latam`,
  de 2026-10-22, avisa que CLP e COP do BIS chegam com um dia de defasagem, e o `cambio.py` as alinha com `shift(-1)`).

O diagrama lê a lista pelo mesmo `motor.ler_lista()`.

Desde 2026-10-21 o mesmo comando grava também o retrato do conhecimento do agente (abaixo), no
mesmo ciclo e com o mesmo `--refazer`.

## conhecimento.py — o retrato do conhecimento do ciclo (SISTEMA_AGENTES.md I.III.xvi–xvii)

```
uv run python -m analytics.agent_system.conhecimento <agente> [--ciclo AAAA-MM-DD] [--refazer]
```

`AREA` liga o agente à pasta do vault (`externo` → `external`, `expectativas` → `expectations`, desde
2026-10-22). Grava `obsidian/ciclos/<data>/conhecimento/<agente>/`, com os caminhos do vault preservados para os
wikilinks resolverem. O agente lê literatura, conceitos e modelos mentais **só dali**. O dono e a
camada de cada item vêm do `data_tracker.xlsx` (colunas Dono/Camada das abas "Qual", Camada da aba
"Mental Models"; o Copom pela regra da camada 1, `copom_layer()` do `tracker.py`). Entram:

- a camada 1 de que o agente é dono (síntese + clean_md; modelo mental; para `politica_monetaria`,
  os documentos do Copom);
- as páginas de conceito que linkam esses itens, podadas às linhas que apontam para o retrato;
- a camada 1 de outros donos que essas páginas linkam, marcada "outro dono" (sem transitividade);
- o mapa conceitual, inteiro.

Em todo arquivo copiado, menos o mapa, link para fora do retrato vira texto simples. `INDICE.md`
(para o agente) e `retrato.json` listam cada arquivo com dono, camada, a marca de outro dono e o
motivo da entrada; o log do ciclo usa isso para mostrar quando o agente leu material de outro dono.
Fonte com dono e sem camada fica fora (ainda não classificada). Fixo no ciclo, como o F(A).
Teste: `tests/test_conhecimento.py`.

## modelo.py — o Modelo Estrutural para os G (SISTEMA_AGENTES.md IV.vi)

```
uv run python -m analytics.agent_system.modelo --ciclo AAAA-MM-DD [--refazer]
```

A função fixa que o G do agente chama para rodar o simulador do Modelo Estrutural, sem
reestimar: `carregar(ciclo)`, `listar(sim)`, `rodar(sim, caminhos, mult)`, `texto(res)`. Uso e
regras na docstring do módulo.

- **Retrato por ciclo:** `dados/A/modelo_estrutural.json` (fora do git, ~0,6 MB), o payload de
  `simulator.construir()` com os pesos de hoje. O `dados` o grava junto com o A; o comando acima
  serve para um ciclo que já tem A. Monta do banco na hora em que roda (~40 s), então é para o
  início do ciclo, como o A.
- **A conta é `simulator.resolver()`**, não uma cópia. `carregar()` levanta se o retrato não
  reproduzir o `sistema_padrao` do payload.
- **Faixa:** a de `_simFaixasSistema` da página (desenho s de cada equação junto, quantis de
  caudas iguais a 90%), só incerteza dos pesos. Conferida contra o JS no mesmo payload em
  2026-10-15: 3e-9 no pior quantil. O teste não pega uma troca de `ceil` por `floor` no quantil
  (mutante verificado); só essa paridade pegaria.
- **Multiplicador:** `"<equação>.<coeficiente>"`, aplicado à mediana e a cada desenho. As
  restrições continuam valendo (na (E) o peso da meta é `1 − e1 − e2`, na (R) `1 − t1 − t2`),
  então multiplicar uma inércia move o peso que sobra. `sigma` e as marcas de crise não aceitam.
- **A partida é o último trimestre com dado** (decisão do usuário, 2026-10-15: trimestre que
  já fechou não se projeta). Os 12 trimestres seguintes saem projetados; o último com dado sai
  como "observado". Exógena sem o dado dele fica no último valor e aparece como segurada (hoje
  a vol implícita, que vem de planilha). Retrato gravado antes dessa regra levanta.

- **Selic de fechamento (derivada; decisão do usuário em 2026-10-21, a revisar no fim de
  tudo):** o modelo só tem a média do trimestre (`panel.selic_bc("media")`). `selic_fim` de q =
  (média de q + média de q+1) / 2, na central e em cada desenho; o 12º trimestre fica em branco.
  No trimestre de partida, o fechamento observado da curva POLICY de `br_interest_rate`: do A do
  ciclo se a tabela estiver lá (o agente de PM a lê), senão do campo `selic_fim` do retrato, que
  `retratar()` grava desde 2026-10-21 (o retrato de 2026-10-15 não tem e não precisa). Medido de
  2006 a 2026T3: erro médio 0,12 p.p., máximo 0,55. Degraus nas reuniões do Copom erram 0,06 um
  trimestre por vez, mas encadeados por 12 trimestres chegam a 41,8 p.p.: por isso não.
- **Convenção de cada exógena (`CONVENCAO`, 2026-10-21):** como o simulador põe cada uma no
  trimestre e de onde vem o valor; `listar()` imprime, e caminho digitado tem de vir na mesma
  convenção. Fechamento: CDS, dólar contra emergentes, S&P, IC-Br em dólar total, vol implícita.
  Média: NTN-B 10a, IC-Br agro e metal, meta. CPI dos EUA: variação no trimestre. O payload não
  carrega isso: está escrito à mão, conferido contra o banco nos dois últimos trimestres, e o
  teste levanta se uma exógena entrar ou sair sem a declaração acompanhar.
- **Fed Funds = efetivo, média do último mês do trimestre** (FRED FEDFUNDS em
  `diferenciais_juros`): o simulador o reconstrói como Selic de fechamento − carry, e o carry da
  estimação é o do último mês. Não é o ponto médio da banda nem a média do trimestre (3T26: 3,75,
  com o Fed subindo em 17/09). Convenção da estimação, não defeito.

- **Grupos do IPCA (2026-10-22, SISTEMA III.III.vii):** `rodar()` devolve `ipca_12m_servicos`,
  `_alimentacao`, `_industriais`, `_monitorados` e `ipca_12m_residuo`, a contribuição de cada grupo
  para o IPCA de 12 meses, em p.p.: Σ, nos 4 trimestres da janela, peso × variação do grupo,
  encadeada pelo cheio dos trimestres anteriores. Grupos + resíduo somam o IPCA 12m em todo trimestre
  (o teste confere). O resíduo só existe enquanto a janela tem trimestre observado, onde o IPCA
  publicado não é Σ peso × grupo trimestral, porque o IBGE agrega mês a mês (0,014 p.p. em média,
  0,14 no pior); do 4º trimestre projetado em diante é zero. Faixa por grupo, dos mesmos desenhos;
  as faixas não somam. `GRUPOS` liga o grupo da (I) ao sufixo e levanta se a (I) mudar.

Teste: `uv run python tests/test_modelo_agentes.py` (lê o payload do relatório entregue, não o
banco; ~1 min).

## consolidacao.py — P1, P2 e PF* (SISTEMA_AGENTES.md IV.ii, IV.vi; 2026-10-22)

```
uv run python -m analytics.agent_system.consolidacao --ciclo AAAA-MM-DD --rodada {r1|r2|rf} [--sem-faixa]
```

Lê `obsidian/ciclos/<data>/caminhos/<agente>_<rodada>.json` (o contrato está na docstring: caminhos
base na convenção do `modelo.CONVENCAO`, mais a tese por trimestre, validada) e a tutela da aba
"Exógenas" do `data_tracker.xlsx` (colunas achadas pelo nome; aba sem nenhum nível levanta). Por
exógena vale o melhor nível entre quem tem tutela e escreveu; no empate, a média trimestre a
trimestre de quem tem valor; sem ninguém, o padrão do simulador, com aviso. Quem escreveu fora da
tutela, ou num nível pior, com valor diferente vira divergência. Uma rodada de `modelo.rodar` sem
multiplicadores grava `P1|P2|PF.md` e o `.json` ao lado. No PF* a faixa do agente não é deslocada
para a central conjunta: o P mostra a diferença e marca "fora da faixa". O dono de cada endógena
está em `ENDOGENA_DONO`, no topo do módulo; o das exógenas, só na aba.
Caudas da tese (2026-10-22, SISTEMA III.III.i): `p_faixa`, `p_upside` (acima de `faixa[1]`) e
`p_downside` (abaixo de `faixa[0]`), que somam 100; um JSON com `worst`/`p_worst`/`p_best` levanta.
Assimetria = (P(up) − P(down))/100. Os grupos do IPCA são da inflação em `ENDOGENA_DONO`.
Teste: `uv run python tests/test_consolidacao.py` (cópia do tracker com tutela fictícia, retrato de
2026-10-22, pasta temporária; ~25 s).
