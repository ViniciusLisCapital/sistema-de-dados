# obsidian/ — Context for Claude

## Purpose

The macro knowledge base, organized by area, and **the only knowledge layer the analyst agents read**
(decided 2026-09-30). `repository/` holds the raw material behind it: PDFs, untouched extractions
and the acquisition planning. No agent reads `repository/`.

Until 2026-09-30 the two trees were deliberately parallel, and `clean_md/` existed in both as
byte-identical copies. The copy in `repository/` was removed and the ingestion pipeline now writes
straight into this vault. The one-way flow:

```
repository/<área>/raw_pdf/*.pdf   (o PDF sem raw_md é o pendente)
   └─ /ingest [área]  (agente de ingestão → repository/ingestion/scripts/run.py)
        ├─ repository/<área>/raw_pdf/  + raw_md/     (bruto, trilha de auditoria)
        └─ obsidian/<área>/clean_md/<name>.md        (texto integral, sem lixo)
             └─ /vault [área]  (agente do vault → repository/ingestion/scripts/vault.py)
                  ├─ obsidian/<área>/synthesis/<name>.md   (o mesmo nome do clean_md)
                  └─ obsidian/concepts/<slug>.md           (patch ou página nova)
```

## Structure

```
obsidian/
  concepts/                     — atomic theory notes, densely [[wikilinked]]; ONE folder for every area
  <área>/
    clean_md/                   — full text of each source, garbage removed, nothing condensed
    synthesis/                  — one condensed note per source, named exactly like its clean_md
    mental_models/              — one file per asset manager: that manager's frameworks FOR THIS AREA
    <área>_conceptual_map.md    — the area's contract with the system (see below)
```

| área | clean_md | synthesis | mental_models | map |
|---|---|---|---|---|
| exchange_rate | 16 | 17 | 4 (Verde, Kapitalo, Kinea, GS — GS partial) | yes |
| monetary_policy | papers (ingestion under way) + central_bank/ | 14 of 44 (2026-10-19) | 0 | no |
| fiscal_policy | 1 | 1 | 0 | no |
| inflation | 1 | 1 | 0 | no |
| trader (new agent's literature, 2026-10-20) | 26 | 0 | — | no |
| labor_market, economic_activity | empty | | | |

`concepts/`: 24 pages (2026-10-19). Live counts: `uv run python repository/ingestion/scripts/vault.py --list`.

**One concepts folder** (decided 2026-10-19): a concept is theory, not an area's property, and
UIP is the same page whether the FX or the monetary-policy agent follows the link. One folder
means a concept cannot exist twice and nothing moves when a second area starts using it.

**Synthesis notes carry the clean_md's name** (decided 2026-10-19; the 19 older notes were renamed
the same day, their old titles kept as `aliases:`). That makes `--list` and the tracker's
"Synthesis" column exact. The cost: a note and its clean_md share a name, so `[[<name>]]` alone is
ambiguous, and links to either are written with the path from the vault root —
`[[exchange_rate/synthesis/<name>]]`, `[[exchange_rate/clean_md/<name>]]`. Concept and
mental-model links stay bare (`[[uip]]`). `vault.py check` fails an ambiguous link. Fleming 1962
keeps its free name: it has no clean_md.

### The vault agent (`/vault [topic] [file ...]`)

`.claude/agents/vault.md`, run by the skill in its own context, opus, at most 5 files per run. Per
file: read the clean_md in full → write the synthesis (template in the agent file; it replaced
the `/add` and `/sync-vault` commands, deleted 2026-10-19) → patch the concept pages it links (a row in the appearances table and a Connections
bullet, never a rewrite) or create the missing ones → `vault.py check` → `tracker.py`. Every number
in a note must be in the clean_md text, and damaged text is reported under "Limitations and
caveats", not reconstructed; the Source line alone may take title, author and date from the
tracker row when the clean_md has no title page (`vault.py biblio`). Numbers on concept pages are
checked too (`vault.py concept`): each against the clean_md of the notes the page links.

**A synthesis is about the material, not about the area's questions** (decided 2026-10-20): it
condenses what the source says, unfiltered by what an analyst agent has to answer, so a change in
those questions never forces a re-synthesis and nothing is dropped for not being asked. Synthesis
and the conceptual map are independent: the vault agent neither reads the maps nor the tracker's
clusters and notes, and proposes no map additions. Not swept: `monetary_policy/clean_md/central_bank/` (500+ Copom documents, needs its own
design, II.III.ix) and topics on hold.

**The 19 older notes predate the check and fail it** (measured 2026-10-19): 4 lack the template
sections (Mundell, Dornbusch, the two GSDEER notes), and 12 carry numbers the clean_md does not
contain — journal volumes and page ranges, sample sizes, coefficients from tables the extraction
lost (Goldfajn & Werlang 2000: five coefficients). Decided 2026-10-20: the user re-runs their
sources through ingestion first; check them again after that.

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
today. Built by the mental-model agent (`/mental <manager> <area>`, `.claude/agents/mental-model.md`),
from letters ingested by `/ingest mental_model/<manager>`; process in `repository/mental_model/MENTAL_MODELS.md`.

### The conceptual map is a contract, not an inventory

Five parts: (1) **central questions** — what every report answers, the floor and not the ceiling;
(2) **causal skeleton** — what moves the area's variable, each channel with the concepts,
mental-model sections and tables behind it; (3) **outputs** — what this agent tells each other agent
matters TO IT, coming from that agent; (4) **inputs** — what the other agents told it matters TO THEM,
coming from it; (5) **concept index** from the literature. An input gives emphasis, never a limit.
Every output must appear as the other agent's input and vice versa. The map holds the **fixed** layer;
the **dynamic** layer (what a given cycle's thesis needs) lives in the reports.
Curation (which sources exist and their status, coverage notes, open gaps) lives in
`repository/agent_mapping/data_tracker.xlsx`: the area's Qual tab and the Notes tab. Only
`exchange_rate` has the new format so far (2026-09-30); its monetary-policy rows are drafts until
that map exists.

**Three folders are not areas:** `concepts/` (above), `ciclos/` (report and log templates, one folder per cycle: `dados/`
with A, the F(A) of each agent and the G scripts; `<agente>_r1.md`, `_r2.md`, `_rf.md`; `P1.md`,
`P2.md`, `PF.md`; `log.md`; `relatorio.md` — when the cycle ends only the `_rf.md`, the log, the
relatório and `dados/` stay) and
`escrivao/` (the writer agent's style manual, `manual_do_escrivao.md` — the condensation of the
clear-writing literature it applies to the final report and demands from the analyst agents).

### Reading path for an agent

map → concept → synthesis (is the condensation enough?) → clean_md (full text) when it isn't.

## Pending

- **Two concept pages fail `vault.py concept`** (2026-10-20), both predating the check, not changed:
  `exchange_rate_pass_through` (the cross-country coefficients 0.69, 0.91, 0.61, −15.3 come from
  Goldfajn & Werlang 2000 tables the extraction lost — should clear with the re-ingestion above) and
  `currency_regimes` (Bretton Woods 1944, ERM 1979: history no linked source states).
- **Copom documents (`clean_md/central_bank/`)**: how to synthesize them is an important open
  discussion, deferred by the user 2026-10-20 (SISTEMA_AGENTES.md II.III.ix).
- **Fleming 1962** has a synthesis but no `clean_md` — its scan is garbled and blocked in ingestion.
- **RPM full text before Dec/2023** is pending (the 12 most recent are in the vault).
- **`labor_market` / `economic_activity`** are empty pillars.
