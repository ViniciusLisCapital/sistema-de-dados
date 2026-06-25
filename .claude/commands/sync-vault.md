# /sync-vault — Reconcile concept pages with synthesis wikilinks

Maintenance command. Scans all synthesis files, extracts their wikilinks, and patches concept pages that are missing rows or connections. Run after bulk additions or manual edits to the vault.

---

## Step 1 — Index all wikilinks

Read only the `## Connections` section of every synthesis file in `obsidian/*/synthesis/`. For each file, collect:
- The synthesis file path
- All `[[wikilink]]` slugs that refer to concept pages (short slugs, not full filenames)

Do not read the full synthesis files at this stage — the Connections section is sufficient.

---

## Step 2 — Map against existing concept pages

For each concept page found in `obsidian/*/concepts/`:
- Read the concept page
- Check its appearances table and `## Connections` section
- Compare against the index from Step 1: which synthesis files link to this concept but are not yet represented in the concept page?

---

## Step 3 — Patch gaps

For each gap found (synthesis file links to a concept but is not in that concept's page):
- Read the relevant synthesis file (now read in full)
- Add the missing row to the concept page's appearances table
- Add the synthesis file to the concept page's `## Connections` section if absent
- Do not restructure or rewrite the existing page — patch only

---

## Step 4 — Report

End with a concise summary:
- **Concept pages patched:** list with number of rows/links added per page
- **Missing concept pages (wikilinks with no concept file):** list of slugs — candidates for future `/add` or manual creation
- **Synthesis files with empty or missing `## Connections` section:** list — these may need review
