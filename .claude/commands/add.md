# /add — Add a source to the bibliography vault

Full pipeline: PDF → synthesis → update existing concept pages → create missing concept pages.

## Argument

`$ARGUMENTS` is the path to the PDF file to process.

---

## Step 1 — Synthesize

Determine extraction route from CLAUDE.md rules:
- Born-digital, single-column (e.g. Verde letters): run `utils/extract_pdf.py` first, synthesize from extracted text
- Academic papers, research reports, complex layout: read the PDF directly with the Read tool
- Scanned PDFs: warn the user — OCR required, stop here

Determine the vault topic from the PDF path: the subfolder under `agent_bibliography/` maps directly to a vault folder under `obsidian/`. Examples:
- `agent_bibliography/exchange_rate/...` → `obsidian/exchange_rate/synthesis/`
- `agent_bibliography/fiscal_policy/...` → `obsidian/fiscal_policy/synthesis/`
- `agent_bibliography/general/...` → ask the user which vault topic applies
- If the path is outside `agent_bibliography/` or the subfolder has no matching vault folder, ask the user before placing the file

Create the synthesis file. Follow this structure exactly:

```
# [Title — Author(s) Year]

**Type:** [paper / book chapter / letter / report]
**Tags:** #[relevant] #[tags]
**Source:** [journal / publication / series]
**Language:** [English / Portuguese]

---

## Context and motivation

## Core argument / thesis

## Key mechanisms / model

## Main results / findings

## Limitations and caveats

## Connections

- [[concept_slug]] — one-line note on how it appears here
- [[other_concept]] — ...
- [[other_synthesis_file]] — ...
```

**The `## Connections` section is the most important part.** It is the index that guides all subsequent updates. Only link to concepts this source genuinely informs. Be precise — omissions are cheaper to fix than false links.

Write the synthesis file. Keep the source language (English PDF → English synthesis; Portuguese → Portuguese).

---

## Step 2 — Parse wikilinks

Read the `## Connections` section of the newly written synthesis file. Extract all `[[wikilink]]` names that refer to concept pages (i.e. short slugs like `carry_trade`, not full synthesis filenames).

---

## Step 3 — Update or create concept pages

For each wikilink from Step 2:

### Concept page exists (`obsidian/*/concepts/[slug].md` is found)

- Read the existing concept page
- Add a new row to its appearances table (the table listing which sources reference it)
- Add the new synthesis file to the `## Connections` section if not already present
- Do not restructure or rewrite the existing page — patch only

### Concept page is missing

1. Grep `obsidian/*/synthesis/` for `[[slug]]` — find all synthesis files that already reference this concept
2. Read only those files (not the full vault)
3. Build a new concept page with this structure:

```
# [Concept Name]

**Type:** [concept type — e.g. "Core arbitrage condition", "Investment strategy", "Theoretical result"]
**Tags:** #[tags]

---

## Definition

## [Formal statement or mechanism — if applicable]

## When it applies / when it fails

## How it appears across sources

| Source | Role |
|---|---|
| [[synthesis_file]] | one-line note |

## BRL / application to the current analysis

## Connections

- [[related_concept]] — why linked
```

Place the file in the `concepts/` folder that matches the majority of its sources. If sources span multiple topics, place in `obsidian/concepts/` (create the folder if it does not exist).

---

## Step 4 — Report

End with a concise summary:
- **Synthesis created:** `[path]`
- **Concept pages updated:** list
- **Concept pages created:** list
- **Suggested new concepts (wikilinks in synthesis without a concept page):** list — user can confirm which ones to create next
