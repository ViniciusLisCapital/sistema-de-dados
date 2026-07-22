# Ingestion Pipeline

Converts PDF research documents into clean, analysis-ready `.md` files for use by the macro analysis agent and other consumers in `repository/`.

---

## How it works

The pipeline runs in **3 AI passes** after an initial text extraction step:

```
PDF
 └─ [extract]     raw text extraction (pdfplumber, no AI)
     └─ [structure]   AI formats text, fixes artifacts, marks boilerplate
         └─ [identify]    AI returns a JSON report of boilerplate sections
             └─ [clean]       AI rewrites document with boilerplate removed
```

| Pass | Tool | What it does |
|---|---|---|
| Extract | pdfplumber | Reads PDF pages and writes raw text to `.md` |
| Structure | Claude Haiku | Adds headers, merges broken lines, fixes encoding artifacts, wraps boilerplate in `> [BOILERPLATE]` markers |
| Identify | Claude Haiku | Returns a JSON list of every boilerplate section found (type, excerpt, reason) |
| Clean | Claude Haiku | Rewrites the structured text with all boilerplate removed |

**Boilerplate removed includes:** disclaimers, legal notices, regulatory disclosures, analyst contact details (phone numbers, emails), copyright notices, table of contents, and blank filler pages.

---

## Folder layout

```
ingestion/
  inbox/                     ← DROP PDFs HERE
    general/                 ← macro/general research
    exchange_rate/           ← FX-related papers
    fiscal_policy/           ← fiscal policy papers
  work/                      ← intermediate files (auditable, not committed)
    general/
      paper_raw.md           ← raw extraction
      paper_structured.md    ← formatted intermediate
      paper_report.json      ← boilerplate identification report
  extract.py                 ← Step 1 script
  clean.py                   ← Steps 2–4 script
  run.py                     ← Full pipeline entry point
  INGESTION.md               ← this file

repository/                  ← FINAL OUTPUT LANDS HERE
  general/
    paper.md
  exchange_rate/
  fiscal_policy/
```

The topic subfolder (`general/`, `exchange_rate/`, etc.) is inferred automatically from where you place the PDF inside `inbox/`. The clean output is written to the matching subfolder in `repository/`.

---

## Usage

### Process all PDFs in inbox (standard workflow)

```powershell
uv run python ingestion/run.py
```

Scans `ingestion/inbox/**/*.pdf`, skips any PDF whose clean output already exists in `repository/`, and processes the rest.

### Process a single file

```powershell
uv run python ingestion/run.py ingestion/inbox/general/paper.pdf
```

### Force reprocess (re-run even if clean output exists)

```powershell
uv run python ingestion/run.py --overwrite
uv run python ingestion/run.py ingestion/inbox/general/paper.pdf --overwrite
```

### Run individual steps manually

```powershell
# Extract only (no AI)
uv run python ingestion/extract.py ingestion/inbox/general/paper.pdf --output ingestion/work/general/

# Clean only (runs all 3 AI passes on an existing raw .md)
uv run python ingestion/clean.py ingestion/work/general/paper.md --output ingestion/work/general/
```

---

## Step-by-step: adding a new document

1. Place the PDF in the appropriate topic folder inside `inbox/`:
   ```
   ingestion/inbox/general/goldman_sachs_gold_2026.pdf
   ```

2. Run the pipeline:
   ```powershell
   uv run python ingestion/run.py
   ```

3. Check the output in `repository/general/goldman_sachs_gold_2026.md`.

4. If the result looks wrong, inspect the intermediate files in `ingestion/work/general/`:
   - `*_raw.md` — raw text extracted from the PDF
   - `*_structured.md` — see how the AI formatted the raw text
   - `*_report.json` — see exactly which sections were flagged and why

5. To reprocess after fixing a prompt or settings:
   ```powershell
   uv run python ingestion/run.py --overwrite
   ```

---

## Skip logic

PDFs are **never deleted** from `inbox/`. Re-running the pipeline is safe by default — a document is skipped if its clean output already exists in `repository/`. Use `--overwrite` to force reprocessing.

---

## Adding a new topic

1. Create the subfolder in `inbox/`:
   ```powershell
   mkdir ingestion/inbox/monetary_policy
   ```

2. Drop PDFs into it and run the pipeline — the matching folder in `repository/` is created automatically.

---

## Cost

Each document makes **3 API calls** to `claude-haiku-4-5`. For a typical 10–40 page research report (~10k tokens input):

| Pass | Input tokens | Output tokens | Cost |
|---|---|---|---|
| Structure | ~10k | ~10k | ~$0.004 |
| Identify | ~10k | ~1k | ~$0.001 |
| Clean | ~11k | ~8k | ~$0.004 |
| **Total** | | | **~$0.01/doc** |

100 documents ≈ $1.

---

## Requirements

- `ANTHROPIC_API_KEY` must be set in `.env` at the project root.
- Run `uv pip install -e .` once after cloning or adding new packages.
