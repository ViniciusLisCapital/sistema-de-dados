# obsidian/ — Context for Claude

## Purpose

The macro knowledge base, organized by area, and **the only knowledge layer the analyst agents read**
(decided 2026-09-30). `repository/` holds the raw material behind it: PDFs, untouched extractions
and the acquisition planning. No agent reads `repository/`.

Until 2026-09-30 the two trees were deliberately parallel, and `clean_md/` existed in both as
byte-identical copies. The copy in `repository/` was removed and the ingestion pipeline now writes
straight into this vault. The one-way flow:

```
repository/ingestion/land_space/<área>/*.pdf
   └─ repository/ingestion/scripts/run.py
        ├─ repository/<área>/raw_pdf/  + raw_md/     (bruto, trilha de auditoria)
        └─ obsidian/<área>/clean_md/                 (texto integral, sem lixo)
```

## Structure per area

```
obsidian/<área>/
  clean_md/                     — full text of each source, garbage removed, nothing condensed
  synthesis/                    — one condensed note per literature source
  concepts/                     — atomic theory notes, densely [[wikilinked]]
  mental_models/                — one file per asset manager: that manager's frameworks FOR THIS AREA
  <área>_conceptual_map.md      — the area's contract with the system (see below)
```

| área | clean_md | synthesis | concepts | mental_models | map |
|---|---|---|---|---|---|
| exchange_rate | 16 | 17 | 10 | 4 (Verde, Kapitalo, Kinea, GS — GS partial) | yes |
| monetary_policy | 1 paper + central_bank/ | 1 | 0 | 0 | no |
| fiscal_policy | 1 | 1 | 1 | 0 | no |
| inflation | 1 | 1 | 1 | 0 | no |
| labor_market, economic_activity | empty | | | | | |

**The map keeps the area prefix** because Obsidian resolves `[[wikilinks]]` by
note name across the whole vault; six files named `conceptual_map.md` would be ambiguous. Same
reason `mental_models/` files keep the `_fx_` in their name (`verde_fx_mental_models.md`): the
same manager will get one file per area.

**Central-bank documents** are the monetary-policy agent's own bibliography, in
`monetary_policy/clean_md/central_bank/{comunicados,atas,rpm}/`: 234 comunicados and 261 atas (all),
12 full RPMs (Dec/2023 on). They are refreshed by the Copom ETL (`pm_copom_projecoes.run()`), not by
the ingestion pipeline; the code is in `domain/db/brasil/bcb/_copom_texto.py` and `_rpm_projecoes.py`.

**Mental models are area × manager.** The letters themselves are cross-area raw material and stay in
`repository/mental_model/<gestora>/` (raw_pdf/raw_md/clean_md). Each area's agent reads only its
own area's file for each manager, so divergence between managers stays visible side by side. They
are frameworks, not current opinions: a view dated 2024 is a way of reasoning, never a fact about
today.

### The conceptual map is a contract, not an inventory

Four parts: (1) **causal skeleton** — what moves the area's variable, each channel with the concepts,
mental-model sections and tables behind it; (2) **outputs** — what this agent tells each other agent
matters TO IT, coming from that agent; (3) **inputs** — what the other agents told it matters TO THEM,
coming from it; (4) **concept index** from the literature. An input gives emphasis, never a limit.
Every output must appear as the other agent's input and vice versa. The map holds the **fixed** layer;
the **dynamic** layer (what a given cycle's thesis needs) lives in the memos.
Curation (sources processed, coverage, status) lives in the area's
`repository/agent_mapping/recommended_bibliography/<área>_bibliography.md`. Only
`exchange_rate` has the new format so far (2026-09-30); its monetary-policy rows are drafts until
that map exists.

### Reading path for an agent

map → concept → synthesis (is the condensation enough?) → clean_md (full text) when it isn't.

## Pending

- **`clean_md/` definition** (flagged 2026-08, not decided): today it is raw text minus true garbage,
  zero rewriting. The open question is whether it should become an *organized* version (paragraphs,
  headers restored) that still preserves all content — without reintroducing the AI-rewrite failure
  documented in [`repository/ingestion/INGESTION.md`](../repository/ingestion/INGESTION.md).
- **Fleming 1962** has a synthesis but no `clean_md` — its scan is garbled and blocked in ingestion.
- **RPM full text before Dec/2023** is pending (the 12 most recent are in the vault).
- **`labor_market` / `economic_activity`** are empty pillars.
