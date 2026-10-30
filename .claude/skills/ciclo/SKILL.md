---
name: ciclo
description: Conduct one cycle of the LIS macro agent system end to end — prepare the data and knowledge snapshots, run every analyst's R1, the moderator's D1, the web agent, the R1 final, the P of the opening, the moderated conversation, the PF*, the update and the escrivão — writing the cycle's log as it goes. Run as /ciclo <AAAA-MM-DD> [etapa] to start a cycle or resume it at a step.
argument-hint: "<AAAA-MM-DD> [preparacao | r1 | d1 | r1-final | p1 | pauta | conversa | pf | atualizacao | relatorio]"
disable-model-invocation: true
---

Conduct the cycle. Arguments: $ARGUMENTS

You are the **session that conducts the cycle** (`SISTEMA_AGENTES.md` III.III.viii, decided
2026-10-30). You do not analyse: you prepare the snapshots, call each agent with the right arguments,
carry messages between the agents and the moderator, run the consolidation, and write the log.
Subagents cannot call each other, so every hand-off goes through you.

The texts this procedure follows, and does not repeat:

- the R1 template: `obsidian/ciclos/_modelo_report.md`;
- the ata template: `obsidian/ciclos/_modelo_ata.md`, written by the moderator;
- the log template: `obsidian/ciclos/_modelo_log.md`, written by you;
- the agents: `.claude/agents/<area>-analyst.md`, `moderador.md`, `web.md` and `escrivao.md`;
- the paths contract: the docstring of `analytics/agent_system/consolidacao.py`.

## Rules for the whole cycle

- **The cycle date is `ciclo`**, the folder is `obsidian/ciclos/<ciclo>/`. The data is everything in
  the database at extraction time; there is no cut by release date (III.III.viii, "Dados").
- **The analysts are the agents of `AGENTES` in `analytics/agent_system/dados/__main__.py`**, one
  `.claude/agents/<agente com - no lugar de _>-analyst.md` each. Never hard-code the list: it grows
  as new agents are registered.
- **Who owns each exogenous variable** comes from the aba "Exógenas" of
  `repository/agent_mapping/data_tracker.xlsx`, read with
  `analytics.agent_system.consolidacao.ler_tutela()`. Pass each analyst its keys as
  `principal=<chaves> subordinado=<chaves>`.
- **Keep every agent's id.** Every step after the R1 resumes the same agent with `SendMessage`, so it
  keeps its context. Note each id (analysts, moderator, escrivão) in the session scratchpad as soon
  as the agent returns. An agent whose id is lost can be started fresh with its own R1 to read, at a
  higher cost: say so in the log.
- **One web call at a time.** Every web call rewrites `noticias/INDICE.md`.
- **Cost.**
  - After every step, add the tokens of each agent call (the `subagent_tokens` of its result) to the
    log's tables, and keep a running total.
  - **Ceiling for cycle 2: 10M.** When the total reaches it, stop before the next call and ask the
    user, with the total so far and what is left.
- **Decisions that only the user can take** go to the user in a question window, with the
  recommended option first. Nothing else stops the cycle: what the conversation cannot settle goes to
  the ata's "Para o usuário".
- **Never** edit an agent's R1, its paths JSON, the ata or the relatório yourself, except as written
  below. Never commit unless the user asks, and then add only the cycle's paths.

## 0. Preparation (`preparacao`)

1. **The previous cycle** is the most recent folder of `obsidian/ciclos/`, earlier than `ciclo`, that
   holds `relatorio.md`.
   - For each analyst, `tipo=atualizacao` if that folder has `<agente>_r1.md`, or `<agente>_rf.md`
     in a cycle before 2026-10-30. Otherwise the analyst gets `tipo=completo`.
   - In cycle 2, mercado de trabalho and crédito write `completo` and the other seven `atualizacao`.
2. **The data and knowledge snapshots**, once per analyst:
   `uv run python -m analytics.agent_system.dados <agente> --ciclo <ciclo>`. Every cycle runs with
   literature (decided 2026-10-30, III.III.viii). `--sem-literatura` exists only to redo the
   benchmark of 2026-10-27, which ran without it; never use it in a normal cycle.
   - It writes `dados/A/`, `dados/F_<agente>.md` and `conhecimento/<agente>/`.
   - It stops with "já existe" if the F is there. Use `--refazer` only before the cycle starts.
3. **The model snapshot:** `uv run python -m analytics.agent_system.modelo --ciclo <ciclo>`.
4. **The log:** copy `_modelo_log.md` to `log.md`. Fill "Informação nova desde o ciclo anterior":
   what triggered the cycle, from the release calendar and what the user said.

## 1. R1 (`r1`)

- **One fresh agent per analyst, all in parallel**, with
  `ciclo=<ciclo> modo=r1 tipo=<atualizacao|completo> principal=<…> subordinado=<…>`.
- Each writes `<agente>_r1.md` and `caminhos/<agente>_r1.json` and returns the "Para o log" block.
- **Noise run (cycle 2 only):** at the same time, a second fresh agent for câmbio and one for
  política monetária, with the same arguments plus `saida=r1b`.
  - They write `<agente>_r1b.md` and `caminhos/<agente>_r1b.json`.
  - Nobody reads them, they are never resumed, and the consolidation ignores them.
  - When both are back, fill the log's "Ruído" table: central, range and probabilities of each
    quarter, and the paths that differ.
- Log: one "R1 · <agente>" block per analyst, from its return, and the rows of the tables
  "Conhecimento", "Faltou" and "Funções G".

## 2. D1 (`d1`)

1. Start the moderator (`.claude/agents/moderador.md`) with `ciclo=<ciclo> d1`.
   - It writes "D1 e perguntas entre agentes" in `ata.md`.
   - It returns the `D1` block: the web demand item by item, and the questions grouped by recipient.
2. Write the demand to `noticias/pedidos_d1.md` exactly as the moderator returned it, one request
   per line, numbered.
3. Run the web agent (`.claude/agents/web.md`) with `ciclo=<ciclo> modo=demanda d=1`. It writes
   `noticias/demanda_d1.md` and updates `noticias/INDICE.md`.
4. Log: the D1 row of "Agente web".

## 3. R1 final (`r1-final`)

- **Resume each analyst** (`SendMessage` to its id), in parallel, with:
  - `modo=r1-final`;
  - the path `noticias/demanda_d1.md`;
  - the questions the moderator grouped for it, literal, each with who asks.
- An analyst with no question and no news addressed to it is still resumed: it reads the principals'
  paths files and records "R1 final · nada mudou" when nothing changes.
- Log: the table "R1 final" (from each R1's section 7, step "R1 final") and the cost per agent.

## 4. P of the opening (`p1`)

- `uv run python -m analytics.agent_system.consolidacao --ciclo <ciclo> --etapa p1`.
- It writes `P1.md` and `P1.json`, and raises with the list of what is wrong if a paths file breaks
  the contract.
  - Send the error to the agent that wrote the file, resumed, so it fixes its own file.
  - Run the consolidation again.
- Log: the section "P da abertura".

## 5. Pauta (`pauta`)

1. Resume the moderator with `pauta`. It writes the ata's "Pauta" and returns the agenda, "Fora da
   pauta" and `VOLTA 1`.
2. **Cycle 2 only:** show the agenda to the user before the first volta. The user may add or cut
   items. Resume the moderator with the user's answer, literal; it records it and returns the revised
   `VOLTA 1`.
   - From cycle 3 on, the user sees the agenda only in the ata.

## 6. Conversation (`conversa`)

Repeat until the moderator returns `ENCERRADA`:

- **`VOLTA <n>`:** for each `PARA: <agente>` block, resume that analyst with `modo=conversa` and the
  message, literal, exactly as the moderator wrote it.
  - The messages of one volta are independent: send them in parallel.
  - Gather the answers, literal, each with its agent. Resume the moderator with `volta` and all of
    them, never summarised.
- **`PAUSA WEB · D<n>`:**
  1. Write the demand to `noticias/pedidos_d<n>.md`.
  2. Run the web agent with `ciclo=<ciclo> modo=demanda d=<n>`.
  3. Resume the moderator with `web` and the path `noticias/demanda_d<n>.md`.
- **`ENCERRADA`:** the paths are frozen from here. Log the section "Conversa", from the moderator's
  closing block and the ata, with the cost of the moderator, of the agents' answers and of the web.

## 7. PF\* (`pf`)

- `uv run python -m analytics.agent_system.consolidacao --ciclo <ciclo> --etapa pf`, which writes
  `PF.md` and `PF.json`.
- Log: the section "PF\*", including what changed against the P of the opening and which item of
  the ata caused it.

## 8. Update (`atualizacao`)

1. **Resume each analyst**, in parallel, with `modo=atualizacao`, the path `PF.md` and the ata's
   "Encerramento", literal.
   - Each one rewrites only what the conversation changed and rewrites the `tese` of its JSON.
   - Each one records the step "conversa" in section 7, even when nothing changed.
   - None changes a path.
2. **Run the PF\* again:**
   `uv run python -m analytics.agent_system.consolidacao --ciclo <ciclo> --etapa pf`.
   - It checks that the paths used, the central and the band are identical to the stored `PF.json`,
     and rewrites it with the updated theses.
   - **If it raises, an agent changed a path in the update.** Do not use `--refazer`. Resume that
     agent with the difference the error lists, so it restores the path. Then run it again.
3. Log: the table "Atualização depois da conversa" and the cost per agent.

## 9. Relatório (`relatorio`)

1. **Start the escrivão** (`.claude/agents/escrivao.md`) with `ciclo=<ciclo>`. It writes
   `relatorio.md` and, when something is missing, `cobrancas.md`.
2. **For each cobrança**, resume the agent it names. Pass the cobrança, literal, and ask it to rewrite
   only the excerpt cited and answer in the cobrança's "Resposta" line.
   - Agents in the same area can go in parallel.
   - An agent whose id was lost: a fresh agent of the same type, with only the cobrança and the
     excerpts it cites.
3. **Resume the escrivão** with `ciclo=<ciclo> retomada`.
4. **Check every number of the relatório against the source** (III.III.iii):
   - data numbers against the cycle's A, recomputed from the raw files;
   - model numbers against `PF.json`;
   - news against `noticias/`.

   With nine agents, use two Sonnet subagents in parallel, one per half of the relatório. Each one
   returns a table of number · source · value at the source · matches or not, and edits nothing.
   - A wrong number goes to the user, with the correction proposed.
   - The relatório changes only after the user decides.
5. **Close the log:** the line "Relatório", the tables "Divergências registradas" and "Custo do
   ciclo", and the total cost.

## Resuming a cycle

`/ciclo <ciclo> <etapa>` starts at that step. First read `log.md` and the cycle folder to confirm
that the earlier steps are done.
- Their files exist: the R1 and its JSON per analyst, `ata.md`, `noticias/demanda_d<n>.md`,
  `P1.json` and `PF.json`.
- Their log sections are filled.

Say what is missing instead of redoing a step that is done. The agents' ids do not survive a new
session; for the steps that resume an analyst, start a fresh one with its own R1 to read, and note
the extra cost in the log.
