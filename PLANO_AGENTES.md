**Sobre este arquivo:** o plano de construção do sistema de agentes-analistas até o agente de política monetária (PM) finalizado, com fases, estimativas e o que pode rodar em paralelo. Aprovado pelo usuário em 2026-10-21. As decisões ficam no [`SISTEMA_AGENTES.md`](SISTEMA_AGENTES.md) e os princípios no [`PRINCIPIOS_AGENTES.md`](PRINCIPIOS_AGENTES.md); aqui fica a ordem do trabalho. Ao fim de cada fase, o chat principal marca o status na tabela abaixo.

"Finalizado" = o primeiro ciclo conjunto completo de câmbio + PM, só com a camada 1, com relatório do escrivão (III.III.v do `SISTEMA_AGENTES.md`). Depois vem a Fase 9, "Crescer e outros agentes", a discutir.


# Status

| Fase | O quê | Status |
|---|---|---|
| 0 | Registrar o framework e arrumar | feito (2026-10-21) |
| 1 | Camada 1 e fila do câmbio | feito (2026-10-21): donos, camada 1 e fila no tracker; as 6 fontes da camada 1 com síntese que passa no check; conceito fx_intervention criado; Kalemli-Ozcan 2019 entrou na camada 1 (canal 2.3) |
| 2 | Mapa conceitual, camada 1 e fila de PM | feito (2026-10-21): mapa com as Partes 1–4 aprovadas (perguntas Q1–Q5, horizonte, worst/best, saídas e entradas espelhadas no câmbio); camada 1 de PM (10 fontes, uma por canal, todas com síntese) e fila aprovadas e marcadas no tracker |
| 3 | Infraestrutura | feito (2026-10-21): 3A (F de PM, acea399, 6698688), 3B (Selic de fechamento derivada da média de dois trimestres, 5fdab47; a revisar no fim do plano), 3C, 3D e 3E |
| 4 | Re-teste do câmbio só com o núcleo | feito (2026-10-21, dados de 15/10): report completo com pouca literatura aberta; promovida a Kapitalo para a camada 1; síntese do Cortapasso removida para ser refeita pelo `/vault`; o câmbio declara a lacuna do Copom em vez de escrever de memória (SISTEMA II.II.iv) |
| 5 | Material da camada 1 de PM | feito (2026-10-21): modelo mental da Verde, 24 cartas em 3 rodadas (14d91ac); as 10 fontes da camada 1 já tinham síntese |
| 6 | Agente de PM e teste solo | em andamento (2026-10-21): definição escrita (`.claude/agents/politica-monetaria-analyst.md`); retrato de PM do ciclo 2026-10-15 refeito com a camada 1 (102 arquivos, 16 de outros donos); rodada 1 solo rodando como subagente |
| 7 | Engrenagem do ciclo conjunto (consolidação, exógenas, escrivão) | — |
| 8 | Primeiro ciclo conjunto câmbio + PM | — |
| 9 | Crescer e outros agentes | a discutir |

**Em curso (2026-10-21, noite):** nada rodando. Falta o usuário rodar `/vault exchange_rate` para refazer a síntese do Cortapasso.
**Próximo:** revisão do report solo de PM; depois as decisões da Fase 7 (consolidação IV.vi, donos das exógenas IV.ii, estrutura do relatório do escrivão) e a seta do agente de PM no diagrama.

**A revisar quando o plano terminar** (pedidos do usuário, 2026-10-21): a Selic de fechamento derivada da média de dois trimestres (reestimar a regra no fechamento?); um pente fino no processo dos modelos mentais (as regras gravadas no `mental-model.md` e no revisor nesse dia); a estrutura do modelo mental da Verde de PM (juros dos desenvolvidos no bloco 3, 2.3 × 3.2, 2.6 de uma carta só, 1.1 × a 1.2 do câmbio).

Atualizado em 2026-10-21. Decisões do dia fora das fases: dono da literatura (SISTEMA_AGENTES I.III.xvii); camada 1 do Copom = comunicados, atas e RPMs desde 2025-01-01; a camada 1 do Copom e os modelos mentais têm acompanhamento próprio no tracker (abas "Copom" e "Mental Models").


# (I) O framework: começar pequeno, testar, ampliar

Ingerir e sintetizar toda a literatura de câmbio e de PM antes de ter o agente foi um erro estratégico (avaliação do usuário, 2026-10-21). Ainda não se sabe quanto o agente de fato busca na literatura nem como a usa, e isso só aparece rodando. Daqui em diante, o sistema fica de pé com o mínimo e cresce conforme recebe mais conteúdo; se errarmos, erramos pequeno e corrigimos em escala menor. Registrado como princípio em `PRINCIPIOS_AGENTES.md` (I.VI).

- **Camadas do material** (literatura, modelos mentais, documentos do Copom):
    - **Camada 1, o núcleo:** o mínimo que cobre cada pergunta central e cada canal do esqueleto causal do mapa, com uma fonte por canal (~8–12 por agente). Uma gestora nos modelos mentais. Do Copom: comunicados, atas e RPMs publicados desde o início do mandato do Galípolo (2025-01-01), sempre anteriores à data do ciclo.
    - **Camada 2:** profundidade, alternativas, evidência brasileira adicional, as outras gestoras.
    - **Camada 3:** o resto, inclusive o histórico.
- **Dados:** ficam as listas atuais (V.I e V.II). O F(A) já resume as tabelas, então cortar dado economiza pouco. Reavaliar depois do primeiro teste de PM.
- **Agente novo:** ingere e sintetiza só a camada 1. As camadas 2 e 3 ficam listadas no tracker e não são ingeridas.
- **Agente que já existe** (câmbio, PM): nada é apagado. O agente enxerga só a camada 1, por um **retrato do conhecimento por ciclo**: uma cópia da camada 1 em `obsidian/ciclos/<data>/conhecimento/<agente>/`, fixa no ciclo como o F(A).
- **Promoção, por dois caminhos:**
    - **Fila de prioridade por agente, o caminho normal.** Junto com a camada 1, o Claude classifica o resto em camadas 2 e 3, ordenadas numa fila. A cada ciclo aprovado sobe o próximo lote (proposta: 3 a 5 itens), e o ciclo seguinte testa esse lote.
    - **Demanda do ciclo, que fura a fila.** O que um ciclo mostra que faltou vai para o topo. O sinal vem do log, onde o agente lista o que abriu e o que faltou, ou da revisão do usuário.
    - Até existir o agente administrador, o usuário aprova cada lote.
- **O log de cada ciclo lista os arquivos de conhecimento que o agente abriu.** É isso que responde quanto ele de fato usa da literatura.


# (II) Onde estamos (2026-10-21)

## Pronto
- **Base de conhecimento:** agentes `ingestion`, `vault`, `mental-model` e `mental-model-reviewer`; skills `/ingest`, `/vault` e `/mental`; o `data_tracker.xlsx`.
- **Ciclo:** o motor do F(A) (`analytics/agent_system/dados/`); o `modelo.py`, que roda o Modelo Estrutural para os G; os modelos de report e de log; o `manual_do_escrivao.md`.
- **Agente de câmbio:** `.claude/agents/cambio-analyst.md`; o mapa conceitual, com as saídas S1–S4 e as entradas E1–E7 em rascunho; dois testes solo (`obsidian/ciclos/2026-10-07/` e `2026-10-15/`).
- **Estoque de conhecimento** (visível ao agente até a Fase 3D; depois, só a camada 1):
    - PM: 64 fontes ingeridas, 53 com síntese.
    - Copom: 234 comunicados, 261 atas, 12 RPMs.
    - Câmbio: 35 fontes ingeridas, 17 com síntese; 4 modelos mentais.
    - 49 conceitos.
- **Lista de dados de PM:** escrita em V.II do `SISTEMA_AGENTES.md`, ~67 tabelas.

## No meio do caminho
- O mapa de câmbio espera o de PM para fechar S1–S4 e E1–E7.
- O formato das premissas e dos signposts (IV.ix) ainda não convence o usuário.
- No Modelo Estrutural, a Selic sai como média do trimestre, e o r\* domina os cenários.

## Fora do caminho crítico: estoque, entra só se promovido
- As 11 sínteses pendentes de PM, salvo as que caírem na camada 1.
- As 19 sínteses pendentes de câmbio.
- As 16 notas antigas de câmbio que falham no `vault.py check`, salvo as da camada 1.
- O modelo mental do Goldman Sachs (25 de 80 edições; os PDFs ainda não foram extraídos).
- As 8 cartas recentes da Kapitalo e da Kinea.
- O RPM histórico, o modelo mental do BC e a síntese trimestral do Copom.
- `/vault trader`.
- Otimizar o agente `vault` (um subagente por paper, ~40% menos tokens).


# (III) Fases

Tempo em dias úteis, com o usuário disponível. Tokens = total processado, ~95% leitura de cache (a parte barata). Precedentes medidos nas sessões passadas: `/vault` ~2 M por paper; `/mental` ~2 M por carta, com o revisor; uma rodada de agente ~5–6 M; uma sessão de construção grande 150–190 M. Os valores reais ficam no `/usage-credits`.

**Total até o ponto final:** ~0,55 bi de tokens. **Caminho crítico:** Fase 0 → 2 → 6 → 8, com 3, 4, 5 e 7 em paralelo. Cerca de 9 dias úteis, ou umas 2 semanas.

## Fase 0 — Registrar o framework e arrumar · 0,5 dia · ~10 M · chat principal
- Registrar o framework em `PRINCIPIOS_AGENTES.md` (I.VI e III), em `SISTEMA_AGENTES.md` (a decisão, e "só se promovido" nas pendências que viraram estoque) e na memória do projeto.
- Atualizar os status defasados: `SISTEMA_AGENTES` II.II.ii e II.III.v, `obsidian/CLAUDE.md`, `repository/CLAUDE.md`, a tabela de estado do `MENTAL_MODELS.md` e o tracker (pelo `tracker.py`).
- Corrigir a numeração das seções S/E do mapa de câmbio.

## Fase 1 — Camada 1 e fila do câmbio · 1 dia · ~30 M · chat principal, com o usuário
- O Claude propõe, numerado:
    - o dono de cada uma das 35 fontes da pasta de câmbio (SISTEMA_AGENTES I.III.xvii); as que não são do câmbio vão para a biblioteca do dono, provisória se ele ainda não existe;
    - a camada 1 do câmbio: entre as fontes de que ele é dono, uma por canal (2.1–2.9), e a Verde entre as 4 gestoras. Canal sem fonte própria é coberto pelos conceitos (a camada 1 de outro dono) ou fica sem literatura (o 2.3, decidido 2026-10-21);
    - a fila: o resto das fontes do câmbio e as outras 3 gestoras, em camada 2 e camada 3, ordenadas.
- O usuário aprova. As colunas "Camada" e "Fila" são preenchidas no tracker (depende da Fase 3E).
- Toda fonte da camada 1 tem de ter síntese que passe no `vault.py check`: sintetizar as que faltam e consertar as notas antigas que caírem no núcleo (~2 M cada).

## Fase 2 — Mapa conceitual, camada 1 e fila de PM · 2–3 dias · ~80 M · chat principal, com o usuário
- Rascunho de `obsidian/monetary_policy/monetary_policy_conceptual_map.md` a partir das 53 sínteses. O Claude lê o estoque para montar o contrato; o agente não o lê.
- Aprovações, na ordem:
    0. O dono de cada uma das 64 fontes da pasta de PM. Candidatas a sair: Kohlscheen (2014) e Tambakis & Tarashev (2012) para o câmbio; as de dominância fiscal em si para o fiscal.
    1. A lista V.II, numerada. No primeiro dia, porque é ela que libera a Fase 3A.
    2. As perguntas centrais.
    3. A direção de worst e best da Selic, e a exceção ao horizonte: a Selic no fim do trimestre, resultado das reuniões do Copom dentro dele.
    4. As saídas e entradas, fechadas com S1–S4 e E1–E7 do câmbio.
    5. A camada 1 de PM: as fontes, o modelo mental da Verde (cartas de 2021–2022) e a regra dos documentos do Copom.
    6. A fila de PM: o resto das 64 fontes, as outras gestoras e janelas de cartas e o histórico do Copom, em camadas 2 e 3, ordenados.

## Fase 3 — Infraestrutura · em paralelo, desde o dia 1 · ~100 M
- **3A. Dados de PM** (subagente D, depois da aprovação 2.1, ~1 dia): `analytics/agent_system/dados/politica_monetaria.py` e uma linha em `AGENTES` no `dados/__main__.py`. Reusa o `especiais.py`. O `motor.conferir` valida contra a V.II.
- **3B. Modelo** (subagente D, ~0,5 dia): o `modelo.py` passa a dar a Selic no fechamento do trimestre, além da média; o `tests/test_modelo_agentes.py` cobre a mudança.
- **3C. Retrato do conhecimento** (chat G, ~1–1,5 dia): módulo novo `analytics/agent_system/conhecimento.py`, chamado junto com o `dados` no início do ciclo.
    - Lê o dono e a camada de cada item no tracker.
    - Regra de alcance (SISTEMA_AGENTES I.III.xvii): leva a camada 1 do agente, os conceitos ligados a ela e, por esses conceitos, a camada 1 dos outros donos, inclusive os provisórios; nunca a camada 2 ou 3 de ninguém.
    - Grava `obsidian/ciclos/<data>/conhecimento/<agente>/` com os caminhos do vault preservados, para os wikilinks resolverem.
    - Copia:
        - as sínteses e os `clean_md` da camada 1;
        - as páginas de conceito, só com as linhas que apontam para notas da camada 1 (conceito sem nenhuma dessas linhas fica fora);
        - os modelos mentais da camada 1;
        - os documentos do Copom da camada 1 (comunicados, atas e RPMs publicados desde 2025-01-01), sempre anteriores à data do ciclo;
        - o mapa conceitual, inteiro.
    - É fixo no ciclo, como o F(A): rodar de novo não refaz, salvo com `--refazer`. Tem teste em `tests/`.
- **3D. Câmbio lê o retrato** (chat G, depois da 3C, ~0,5 dia). Em `cambio-analyst.md`:
    - o agente lê só de `obsidian/ciclos/<ciclo>/conhecimento/cambio/`, nunca do vault direto;
    - o log ganha a lista de arquivos abertos e a linha "faltou: <tema>". O `_modelo_log.md` recebe a mesma mudança.
- **3E. Tracker: modelos mentais e documentos do BC** (chat G, ~1 dia). O `repository/ingestion/scripts/tracker.py` passa a escrever duas abas novas, reconstruídas a partir das pastas:
    - "Mental Models": um resumo por documento área × gestora (janela, cartas na janela, cartas lidas pelo `ledger/`, pendentes, última rodada, camada, fila) e uma linha por carta.
    - "Copom": um resumo por tipo e uma linha por documento, com a camada calculada pela regra da camada 1 do Copom.
    - As colunas "Dono", "Camada" e "Fila" entram também nas abas "Qual - <Área>", como colunas do usuário (decidido 2026-10-21; a camada é a da biblioteca do dono). As colunas do sistema andam duas posições; conferir que a planilha migra sem perder dado.
    - Quem chama o `tracker.py`:
        - o `run.py` da ingestão, agora também para as cartas;
        - o `mental.py done`;
        - o passo do ETL do Copom que grava o vault (`domain/db/brasil/bcb/_copom_texto.py`), que, se o arquivo estiver aberto no Excel, avisa e não derruba o ETL.
    - O `.claude/agents/ingestion.md` deixa de dizer que cartas não atualizam o tracker.

## Fase 4 — Re-teste do câmbio só com o núcleo · 1 dia · ~15 M · chat principal (depois das Fases 1 e 3D)
- Rodada 1 solo num ciclo novo, com o retrato da camada 1, comparada com o report de `2026-10-15`: o que se perdeu, o que o agente abriu, o que ele disse que faltou.
- É o primeiro teste do framework, barato, antes de investir no agente de PM. Se a qualidade cair, a camada 1 do câmbio é revista antes de repetir o desenho na PM.

## Fase 5 — Material da camada 1 de PM · 1–2 dias corridos · ~60 M
- `/vault` das fontes da camada 1 sem síntese, das 11 pendentes só as escolhidas (no chat principal, depois da aprovação 2.5).
- Modelo mental de PM da Verde, cartas de jan/2021 a dez/2022 (~24), no chat H com `/mental` em `/loop`. Pode começar já: a gestora e a janela estão decididas.
    - Preparação no chat principal: a entrada `verde_mp_mental_models` no `mental_models.yaml`, com início em 2021-01 e fim em 2022-12 (o `mental.py` precisa aceitar o fim da janela), e a pasta `obsidian/monetary_policy/mental_models/`.
    - O modelo mental descreve como a gestora raciocinou num ciclo de aperto, não a opinião atual dela. O agente o lê como arcabouço (PRINCIPIOS I.I.iii).

## Fase 6 — Agente de PM e teste solo · 2–3 dias · ~80 M · chat principal (depois das Fases 2, 3 e 4)
- `.claude/agents/politica-monetaria-analyst.md`, por analogia com o `cambio-analyst.md` já ajustado na 3D. O agente lê só o F de PM e `conhecimento/politica_monetaria/`.
- A seta do agente no diagrama (`analytics/agent_system/generate_report.py`).
- Teste solo da rodada 1, revisão do usuário, v2. Se o modelo mental não estiver pronto, a v1 roda sem ele e registra a falta.

## Fase 7 — Engrenagem do ciclo conjunto · 2–3 dias · ~120 M · em paralelo com as Fases 2 a 6
- **7A.** Decidir a IV.vi no chat principal, com o usuário: como os reports viram P1, P2 e PF*. Implementar depois, no subagente E, num módulo de consolidação junto do `modelo.py`.
- **7B.** Decidir a IV.ii no mínimo: quem responde pelas exógenas comuns aos dois agentes (CDS, Fed Funds, commodities).
- **7C.** Agente escrivão: primeiro decidir a estrutura do relatório (§13 do manual), depois escrever `.claude/agents/escrivao.md` (subagente F).
- **7D.** Tirar o "aguarda PM (Sx)" do `cambio-analyst.md`, depois da Fase 6.

## Fase 8 — Primeiro ciclo conjunto câmbio + PM · 2–3 dias corridos · ~70 M · chat principal
- Um retrato do F(A) e um do conhecimento por agente.
- A sequência:
    1. rodada 1 dos dois agentes, em paralelo;
    2. P1;
    3. rodada 2;
    4. P2;
    5. RF;
    6. PF*;
    7. relatório do escrivão, em markdown;
    8. checagem dos números (III.III.iii);
    9. log.
- Revisão do usuário e **primeira promoção:** sobe o primeiro lote da fila de cada agente, com o "faltou" do log no topo. Promover inclui ingerir ou sintetizar o item que ainda não tem síntese.
- Para fechar: marcar III.II e III.III.v como feitos, levar as lições ao `PRINCIPIOS_AGENTES.md` e reabrir o número de rodadas (IV.iii).

## Fase 9 — Crescer e outros agentes (a discutir)
- **Mover os arquivos para a pasta do dono**, de uma vez, ao criar o primeiro agente novo (provavelmente o de inflação, que recebe a literatura de repasse). Um script move os arquivos e reescreve os wikilinks; o `vault.py check` confere. Até lá o dono vive só no tracker, e o retrato lê pelo tracker, não pela pasta, então mover antes não muda nada para os agentes.
- **Agentes novos** (inflação, fiscal, atividade, crédito, mercado de trabalho, externo, trader, administrador): mapa → camada 1 e fila (partindo da camada 1 provisória que já tiverem) → ingerir e sintetizar só a camada 1 → teste.
- **Promoções** do câmbio e da PM, lote a lote.
- **O estoque** da seção (II), conforme for promovido.


# (IV) Despacho: chat separado ou subagente

Os dois rodam em paralelo e gastam praticamente os mesmos tokens pelo trabalho, mas não funcionam da mesma forma.

- **Subagente** (disparado pelo chat principal): roda em segundo plano, sem conversar com o usuário, e devolve só o relatório final. Serve para tarefa bem especificada e que se confere sozinha. Não pode disparar outro subagente, então não roda `/mental` (escritor + revisor).
- **Chat separado:** uma sessão inteira com o usuário, que acompanha e corrige no meio. Roda `/loop` e skills que disparam subagentes. **Quem abre é o usuário** (o Claude não abre aba nova no VS Code), colando o pedido pronto da seção (V).

**Regra:** subagente para o que é mecânico e se confere sozinho; chat separado para o que roda por dias, precisa de `/loop` ou precisa do olho do usuário; chat principal para toda decisão.

| Onda | Quem | Como | Fase | Começa quando | Escreve em |
|---|---|---|---|---|---|
| 1 | Principal | — | 0 → 1 → 2; decisões 7A, 7B e estrutura do relatório | já | docs, camada 1 e fila do câmbio, mapa de PM |
| 1 | G | chat separado | 3E → 3C → 3D | já | `tracker.py`, `run.py`, `mental.py` (só a chamada ao tracker), `_copom_texto.py`, `analytics/agent_system/conhecimento.py`, `tests/`, `cambio-analyst.md`, `_modelo_log.md`, `ingestion.md` |
| 1 | H | chat separado | 5: `/mental` da Verde em PM | preparação feita pelo principal | `obsidian/monetary_policy/mental_models/verde_mp_mental_models.md` e o ledger dele |
| 2 | D | subagente | 3A + 3B | lista V.II aprovada | `analytics/agent_system/dados/`, `modelo.py`, `tests/` |
| 2 | Principal | `/vault` (já roda como subagente) | 5: sínteses da camada 1 de PM | camada 1 de PM aprovada | sínteses, `obsidian/concepts/` |
| 2 | E, F | subagentes | 7A implementação; 7C escrivão | decisões tomadas | módulo de consolidação; `.claude/agents/escrivao.md` |
| 2 | Principal | — | 4 | Fases 1 e 3D | `obsidian/ciclos/<data>/` |
| 3 | Principal | — | 6 → 8 | Fases 2, 3 e 4 | agente de PM, ciclo |

**Regras do trabalho em paralelo** (tudo roda na mesma pasta):
- Só o chat principal edita `SISTEMA_AGENTES.md`, `PRINCIPIOS_AGENTES.md`, este arquivo, os `CLAUDE.md`, o `mental_models.yaml` e os valores das colunas "Camada" e "Fila" do tracker. Os outros devolvem o que mudou, e o principal consolida.
- `obsidian/concepts/` é escrito só pelo `/vault`.
- Cada chat commita só os próprios caminhos.
- O chat G mexe no `mental.py`, que o chat H usa. Ele só troca o script entre duas rodadas do H e avisa antes.


# (V) Pedidos prontos para colar

## Chat G — tracker, retrato do conhecimento, câmbio lê o retrato

```
Leia PLANO_AGENTES.md, seções (I), (III) Fase 3 itens 3E, 3C e 3D, e (IV). Você é o chat G.
Faça, nesta ordem, parando para eu revisar ao fim de cada item:
1. 3E: as abas "Mental Models" e "Copom" e as colunas "Camada" e "Fila" no tracker.py,
   e as chamadas ao tracker (run.py para cartas, mental.py done, _copom_texto.py).
   Antes de rodar contra a planilha real, faça uma cópia e migre a cópia; me mostre que
   as colunas A–I das abas "Qual" ficaram intactas.
2. 3C: analytics/agent_system/conhecimento.py, com teste em tests/. Enquanto a coluna
   "Camada" estiver vazia, teste com uma camada 1 fictícia do câmbio.
3. 3D: cambio-analyst.md e _modelo_log.md lendo só o retrato e registrando o que abriu
   e o que faltou.
Escreva só nos caminhos da linha "G" da tabela da seção (IV). Não edite SISTEMA_AGENTES.md,
PRINCIPIOS_AGENTES.md, PLANO_AGENTES.md nem os CLAUDE.md: no fim, me devolva o que mudou
para o chat principal registrar. O chat H usa o mental.py: só mexa nele entre duas rodadas
do H, e me avise antes. Commite só os seus caminhos.
Verificação: seção (VI) para 3E e 3C.
```

## Chat H — modelo mental de PM da Verde (2021–2022)

```
Leia PLANO_AGENTES.md, seção (III) Fase 5, e repository/mental_model/MENTAL_MODELS.md.
Você é o chat H. Rode /mental verde monetary_policy em /loop até o ledger do
documento verde_mp_mental_models cobrir todas as cartas de 2021-01 a 2022-12.
Antes da primeira rodada, confirme com `mental.py --list` que a janela está certa
(começa em 2021-01 e termina em 2022-12). Se o revisor recusar uma rodada, pare e me
mostre o veredito, sem aceitar no meu lugar.
Escreva só o documento e o ledger desse modelo mental. Não edite mental_models.yaml,
SISTEMA_AGENTES.md, PLANO_AGENTES.md nem os CLAUDE.md. No fim, me devolva quantas
cartas foram lidas e os blocos do documento, para o chat principal registrar.
```


# (VI) Verificação
- **Fase 0:** o framework está no `PRINCIPIOS_AGENTES.md` (I.VI) e no `SISTEMA_AGENTES.md`, e este arquivo está na raiz.
- **Fases 1 e 5:** toda fonte da camada 1 tem síntese que passa no `vault.py check`; o `mental.py check` e o revisor aprovam cada rodada.
- **3A:** `uv run python -m analytics.agent_system.dados politica_monetaria` roda sem erro no `motor.conferir`.
- **3B:** `uv run python tests/test_modelo_agentes.py`.
- **3E:**
    - As abas novas batem com as pastas: 80 cartas lidas no câmbio da Verde; 234 comunicados, 261 atas e 12 RPMs do Copom.
    - Uma rodada de `/mental` e uma carga do Copom atualizam as abas sem passo manual.
    - As colunas A–I das abas "Qual" ficam intactas.
- **3C:**
    - O retrato tem só a camada 1.
    - Nenhum wikilink aponta para fora dele, salvo os do mapa.
    - Nenhum documento do Copom é posterior à data do ciclo.
    - Rodar de novo sem `--refazer` não refaz.
- **Fases 4, 6 e 8:** o log lista o que o agente abriu e o que faltou; os reports seguem o `_modelo_report.md`; o usuário aprova.
