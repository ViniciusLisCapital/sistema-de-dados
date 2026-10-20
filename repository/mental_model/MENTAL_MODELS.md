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
| `mental_models.yaml` | the corpora of each manager (folder + date pattern of the file names, which is also the naming rule `/ingest` applies), the area codes of the document names, and each document's `start` |
| `ledger/<document>.tsv` | the letters a document has read, one per line, written only by `mental.py done` (`seeded` = read before the ledger existed) |
| `ledger/.<document>.run.json` | an open run: its letters and the document's snapshot |
| `ledger/.<document>.claims.json` | the writer's claims: per block repacked or added, the old text cut into statements and the new statements with their letter |
| `ledger/.<document>.review.json` | the reviewer's verdict on every claim, anchored in the texts. The three hidden files go with `done` or `abort`; not versioned |
| `ledger/<document>.log.md` | one section per run: blocks repacked and added, the verdict on every statement, what the user accepted |
| `repository/ingestion/scripts/mental.py` | `--list`, `begin`, `check`, `done`, `abort`, `audit`, `seed` (its docstring says what each does) |

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
- **Quotes literal, numbers from the letters**: `check` looks for both in the run's letters.

## State (2026-10-20)

| document | read | pending | note |
|---|---|---|---|
| verde_fx | 77 (2020-01 → 2026-05) | 3 | its About says 73 letters; the ledger was seeded with the whole range, 77 in the corpus |
| kapitalo_fx | 83 (2019-07 → 2026-05) | 3 | |
| kinea_fx | 124 (2021-05 → 2026-06) | 5 | 60 letters + 64 Insights |
| goldman_sachs_fx | 25 of 80 issues (→ 2025-06-20) | — | the 80 PDFs need `/ingest mental_model/goldman_sachs` first; then `mental.py seed goldman_sachs exchange_rate 2025-01-03 2025-06-20` |

Known gaps:
- The three older FX documents quote literally ~80% of the time (`mental.py audit`: Verde 116/137,
  Kapitalo 126/145, Kinea 83/100); the rest are lightly edited sentences inside quote marks. Left as
  they are; the check holds every new quote to the letter.
- Verde's 1999–2009 PDFs (124) were never extracted; the FX document starts in 2020 (`start`).
- New Kapitalo letters through `/ingest` get the generic cleaner, not `kapitalo/curate.py`.
- SPX (7 PDFs) has no document yet.
