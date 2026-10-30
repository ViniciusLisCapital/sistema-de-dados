# Mental models — the process

How a manager's letters become the mental-model documents the analyst agents read. Built
2026-10-20; before that the four FX documents were written by hand-run sessions with no fixed process.

```
repository/mental_model/<manager>/raw_pdf/<letter>.pdf
  └─ /ingest mental_model/<manager>      ingestion agent: rename by date, extract, page check
       ├─ repository/mental_model/<manager>/raw_md/<letter>.md
       └─ repository/mental_model/<manager>/clean_md/<letter>.md
            └─ /mental <manager> <area>
                 ├─ mental-model agent: reads, repacks, writes the claims, check passes
                 │    └─ obsidian/<area>/mental_models/<manager>_<code>_mental_models.md
                 ├─ mental-model-reviewer (fresh agent): judges every claim → verdicts
                 └─ mental.py done: ledger/<document>.tsv + ledger/<document>.log.md
```

Kinea has no PDFs: `kinea/fetch_kinea.py` saves the letters as markdown, and those files are the corpus.

## Files

| file | what it holds |
|---|---|
| `mental_models.yaml` | the corpora of each manager (folder + date pattern of the file names, which is also the naming rule `/ingest` applies), the area codes of the document names, and each document's `start` and optional `end` (the window of letters it reads) |
| `ledger/<document>.tsv` | the letters a document has read, one per line, written only by `mental.py done` (`seeded` = read before the ledger existed) |
| `ledger/.<document>.run.json` | an open run: its letters and the document's snapshot |
| `ledger/.<document>.claims.json` | the writer's claims: per block repacked or added, the old text cut into statements and the new statements with their letter and `evidence` (the letter's sentence that supports it, word for word; required when the run file says `evidence_required`, which `begin` writes from 2026-10-30) |
| `ledger/.<document>.review.json` | the reviewer's verdict on every claim, anchored in the texts (after a fix, only on the blocks the fix changed) |
| `ledger/.<document>.review_base.json` | per block, the hash of its text and claims and its verdict entry, written by `done` whenever the review matches the current document (also when `done` ends blocked); what `packet --delta` compares against and `done` merges from. The four hidden files go with `done` or `abort`; not versioned |
| `ledger/<document>.log.md` | one section per run: blocks repacked and added, the verdict on every statement, what the user accepted |
| `repository/ingestion/scripts/mental.py` | `--list`, `begin`, `check`, `packet [--delta]`, `findings`, `done`, `abort`, `audit`, `seed` (its docstring says what each does) |

## Decisions

- **Area × manager**, one file each, built only from that manager's letters; comparison across
  managers is a separate exercise. Frameworks, not opinions: a dated view enters as an application.
- **The letters' text stays in `repository/`**: one letter feeds every area, so it is not an
  area's vault file. Analyst agents read only the documents.
- **Extraction is the ingestion pipeline's**, not the mental-model agent's: one set of tools and one
  page check for every PDF in the system (user's call, 2026-10-20).
- **Date order, a word budget per run** (~18,000 words, at most 10 letters), so every letter is read
  in full. A letter with nothing for the area still enters the ledger.
- **Repack, never drop** (user's call, 2026-10-20). An entry the new letters add to is rewritten as
  one coherent text that takes in the nuance — the definition, the conditions, how the manager's use
  of it evolved — instead of a bullet bolted onto an outgrown definition. Nothing it held may go:
  `check` compares with the snapshot and fails on a lost entry number, quote, dated application,
  number or link; on a rewrite of an entry this run adds nothing to; and on a repack keeping under
  75% of the entry's words (warning under 90%). Entry numbers are permanent: other notes cite them.
- **Meaning is checked by a second agent** (user's call, 2026-10-20). The script cannot see that
  "fortalece" became "enfraquece". So the writer lists, per repacked block, every statement of the
  old text and every new one with its letter; a fresh reviewer agent, which never sees the writer's
  reasoning, judges each against the old text, the new text and the letters (kept / sharpened /
  weakened / contradicted / missing; supported / unsupported), and lists what the writer's list left
  out and what the new text says on no evidence. Every passing verdict must quote the text it rests
  on, and `done` refuses anything else unless the user accepts it. Residual risk: the reviewer is a
  model too; the log is where a user audits it.
- **A fine comb, not a second full read** (user's call, 2026-10-30). Measured on the first run of
  a new document (10 letters): the writer cost 166k tokens; three fixes by resuming the same writer
  cost 180k, 210k and 212k (the last changed two sentences in 23 s; resuming carries all the
  context); four full reviewers at ~150k each flagged 4, 5, 2 and 2 statements, never the same one
  twice, because each full re-read finds new sentences in blocks nobody touched, so the loop does
  not converge. All 13 flagged statements were one defect: a causal link, motive, generalization or
  scope the letter does not state. Four changes. (1) A fix is a fresh, lean writer (`mental-model
  <manager> <area> --fix`) that reads `findings` (every blocking item in full) and only the
  flagged blocks and the letters they cite. (2) After a fix the reviewer judges only the blocks
  whose text or claims changed (`packet --delta`); `done` carries the earlier verdict of every
  other block from the review base, and a failing verdict carried over still blocks. (3) The
  writer gives each new claim its evidence, a letter sentence word for word, which `check`
  verifies, and ends with a self-audit of the four defect types; runs begun before this have no
  `evidence_required` and keep passing. (4) At most one fix round per run; if still blocked, the
  user gets the findings in full and chooses between accepting and aborting.
  Amended the same day (user's calls): **two** fix rounds, the second without asking ("corrigir
  sempre, sem perguntar"); and a finding left after the second whose exact letter wording is
  already in the same entry is accepted by the conductor (`done --accept`), with a line in the
  log: "aceite por regra do usuário de 2026-10-30". Anything else still goes to the user. Run
  `done` after every review, delta ones included: it is what moves the review base forward.
- **Quotes literal, numbers from the letters**: `check` looks for both in the run's letters.

## State (2026-10-30)

| document | read | pending | note |
|---|---|---|---|
| verde_fx | 80 (2020-01 → 2026-08) | 0 | its About says 73 letters; the ledger was seeded with the whole range, 77 in the corpus |
| kapitalo_fx | 83 (2019-07 → 2026-05) | 3 | |
| kinea_fx | 124 (2021-05 → 2026-06) | 5 | 60 letters + 64 Insights |
| verde_mp | 24 | 0 | window 2021-01 → 2022-12 only (the 2021–2022 tightening cycle), decided 2026-10-21; done the same day in 3 runs |
| goldman_sachs_fx | 25 of 80 issues (→ 2025-06-20) | — | the 80 PDFs need `/ingest mental_model/goldman_sachs` first; then `mental.py seed goldman_sachs exchange_rate 2025-01-03 2025-06-20` |
| verde_inflation | 24 (2024-09 → 2026-08) | 0 | layer 1 of the inflation agent (decided 2026-10-30, one manager per area, the ~24 most recent letters); 3 runs, ~2.8M tokens (run 1 ~1.6M before the 2026-10-30 trim, runs 2–3 ~0.57–0.59M each) |
| verde_expectations | — | — | dropped 2026-10-30 (user): one run of 10 letters produced only entries that repeat verde_inflation (the Verde never discusses surveys, Focus or revisions); the expectations agent has no mental model of its own in layer 1 and reaches verde_inflation through the concepts |
| kapitalo_external | 0 | 24 | layer 1 of the external agent, window from 2024-09 |
| kinea_fiscal | 0 | 26 | layer 1 of the fiscal agent, window from 2025-09 (Carta + Insights) |
| kinea_activity | 0 | 26 | layer 1 of the activity agent, window from 2025-09 (Carta + Insights) |

Known gaps:
- The three older FX documents quote literally ~80% of the time (`mental.py audit`: Verde 116/137,
  Kapitalo 126/145, Kinea 83/100); the rest are lightly edited sentences inside quote marks. Left as
  they are; the check holds every new quote to the letter.
- Verde's 1999–2009 PDFs (124) were never extracted; the FX document starts in 2020 (`start`).
- New Kapitalo letters through `/ingest` get the generic cleaner, not `kapitalo/curate.py`.
- SPX (7 PDFs) has no document yet.
