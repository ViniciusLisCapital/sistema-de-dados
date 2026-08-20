# HANDOVER — 2026-08-14

**Scope**: the Facdetp.xlsx / DLSP thread of this session — ingesting BCB's `Facdetp.xlsx`,
building the Dívida Líquida tab, the entity balance sheet, and the new parafiscal impulse
metric. Also covers one small earlier item (the GDP line removal).

Unrelated changes present in `git status` (`analytics/brasil/labor_market/*`,
`domain/release_calendar/*`, `domain/db/brasil/bcb/mt_caged.py`, and the mt_caged rows in
`domain/db/CLAUDE.md`) are **NOT from this thread** — do not attribute or revert them here.

---

## Goal

Consume BCB's `Facdetp.xlsx` (fatores condicionantes da DLSP) into the pipeline, then
surface it in `analytics/brasil/fiscal_policy/`. The goal grew in four user-driven steps:

1. Ingest the workbook.
2. New dashboard tab, **tables separated like the Excel** (Estoque, Primário, …), with
   **only two metrics: Level and % GDP**.
3. Reorganize as **Liabilities / Assets / Cash** — then, after discussion, **by entity**.
4. New fiscal-impulse metric from the `Créditos concedidos a Inst. Financ. Oficiais`
   rubric, plus its inclusion in the Visão Combinada chart.

## Instructions and constraints given

- Tab metrics: *"For now, the only metric should be Level and % GDP"* — no Nominal/Real,
  no Y/Y, no Marginal, no frequency toggle.
- Tables *"separated like in the excel: Estoque, Primario and so on"* → one section per
  workbook sheet, in the workbook's order.
- Entity framing chosen over consolidated: *"Build that way"* in reply to the proposal
  "entity-first, replacing the interna/externa framing in a new section".
- New impulse metric scope: rubric `Créditos concedidos a Inst. Financ. Oficiais`
  *"(take the subcomponents too)"*, *"summing up the 12m the Primario factor only, in
  level and % GDP"*, and *"Include it in the Combination graph as % GDP"*.
- **Sign, stated explicitly by the user**: *"when the number it's negative it implies that
  the governament is lending money to financial institutions (increase their assets), but
  that is a potential fiscal impulse, so must be positive"* → the metric is multiplied by −1.
- Earlier in the session: remove the GDP line from the Visão Combinada chart (done;
  `yaxis2` went with it). `atv_pib_taxas` / `D.pib_yoy` is still loaded but unplotted —
  **do not "restore" it without asking**.

## Conventions and decisions established

- **Table**: `macro_brasil.fisc_dlsp_fatores`, PK `(date, fator, item)`. 95 items × 9
  fatores × 295 months = 252,225 rows, monthly from 2001-12.
- **Sign convention is NOT flipped at ingestion** (unlike `fisc_nfsp`, which flips):
  positive flow = increases debt, so `primario` positive = **deficit**. Flipping would
  break the additive identity, which is the table's whole value. Anything mixing this
  table with `fisc_nfsp` must flip one side.
- **`run()` upserts, does not truncate** (diverges from `fisc_rtn.py` / `fisc_efgg.py`)
  because `_ITEMS` is an explicit contract checked label-by-label every run — a layout
  change raises before writing, so there is no orphan-row risk to truncate away.
- **Payload shape**: all 855 series share one date grid, so `dates` / `tree` sit once at
  the payload root and each series is a bare array pair. This is why the tab costs 1.95 MB
  for 855 series while `rtn` costs 9.69 MB for 35. Keep this shape.
- Identically-zero series ship as the scalar `0` (364 of 855), expanded by `dlspZeros()` /
  `zerosArr()` in JS.
- **% do PIB numerator differs by fator nature**: month-end stock for `estoque`, **12-month
  rolling sum** for the 8 flows; denominator always `atv_pib_mensal.pib_acum_12m` (SGS 4382).
- Item slugs: `{arvore}__{devedor}__{item}` with double-underscore separators, 3 independent
  trees (`total` / `interna` / `externa`), max 71 chars.
- Balance-sheet buckets are a **partition** of the same leaves, so
  `Passivos + Caixa + Créditos = Líquido` holds by construction; classification affects
  interpretation, never arithmetic.
- Chart divs added in JS use the shared `.dlsp-chart` CSS class, not new IDs (the
  missing-from-CSS-selector bug documented in `analytics/brasil/fiscal_policy/CLAUDE.md` Gotchas).
- `makeDlspHierTab()` is now the shared factory for **11 instances** (9 fator sections,
  Balanço por Entidade, Impulso via Crédito) via `dataKey` / `treeKey` / `noFator` /
  `yTitle` opts.

## Work completed

**New files**

- `connectors/bcb_tabelas_especiais.py` — BCB "Tabelas especiais" xlsx client. Fixed
  filenames at `https://www.bcb.gov.br/content/estatisticas/Documents/Tabelas_especiais/`;
  returns raw `header=None` sheets. Folder inventory intentionally lives in
  `analytics/brasil/fiscal_policy/fontes_dados.md`, not duplicated in the docstring.
- `domain/db/brasil/bcb/fisc_dlsp_fatores.py` — ETL plus the hardcoded 95-item `_ITEMS`
  taxonomy, `ITEM_TREE` / `FATORES` exported for analytics, and 3 fail-loudly guards
  (label mismatch, non-contiguous date grid, broken identity).
- `analytics/brasil/fiscal_policy/dlsp_tab.py` — payload builder: 9 fator sections plus the
  entity balance sheet (`_CLASSE`, `build_entity_tree()`, `_sum_arrays`).

**Edited**

- `analytics/brasil/fiscal_policy/generate_report.py` — `_load_dlsp_tab_data()`,
  `_load_impulso_credito_oficial()`, both wired into `run()`; module docstring refreshed
  (it claimed only 2 tabs existed).
- `analytics/brasil/fiscal_policy/report.html` (+667 lines) — new **Dívida Líquida** tab (2nd in
  nav), `makeDlspHierTab()` / `renderDlspTab()` / `renderDlspBalanco()`, the Balanço por
  Entidade section, the Impulso via Crédito section, the 3rd trace and rewritten caption in
  Visão Combinada, `.dlsp-chart` CSS, and 3 new Apêndice entries.
- `jobs/update_db.py` — `fisc_dlsp_fatores` registered (45 scripts now), placed after the
  SGS scripts since it rewrites full history each run.
- Docs: root `CLAUDE.md`, `analytics/CLAUDE.md`, `analytics/brasil/fiscal_policy/CLAUDE.md`
  (+154 lines), `analytics/brasil/fiscal_policy/fontes_dados.md`, `connectors/CLAUDE.md`,
  `domain/db/CLAUDE.md`.

**State-changing commands**

- `CREATE TABLE macro_brasil.fisc_dlsp_fatores` (with native `COMMENT`s) — **applied to the
  live DB at 192.168.15.200, not committed anywhere as DDL** (this repo has no migrations;
  tables are created ad hoc).
- Full history loaded: 252,225 rows. Re-run with `start='2026-01'` confirmed idempotent.
- Nothing committed. No `git add` run.

## Current state

Working and verified: ingestion, the 4-tab report, both new sections, the 3-trace Visão
Combinada. `reports/fiscal_policy_latest.html` regenerated (**15.77 MB** — see Gotchas).
79 checks pass in the jsdom harness.

**Validation evidence** (all live, not asserted):

- Identity `estoque[t] − estoque[t−1] = Σ 8 fluxos[t]` holds in 27,904 of 27,930 cells; the
  26 exceptions are all in 2003-10/11 and 2004-02/03 as offsetting pairs — BCB's own
  historical revision break, tolerated by `_validate()` and raising anywhere else.
- `estoque/total ÷ pib_acum_12m` reproduces SGS `fisc_divida.dlsp_pct_pib` to ±0.005pp
  across all 295 months, and per debtor.
- `primario/total` is the exact negative of `fisc_nfsp.resultado_primario_fluxo_mensal`
  (max abs sum 0.0167 R$mi = SGS 2-decimal rounding); the 12m %PIB version matches
  `resultado_primario_pct_pib_12m` (+1.19 vs −1.19 at 2026-06).
- Per entity: `interna__X + externa__X = total__X` and Σ5 entities = total, both
  **0.000000** over 295 months. `Passivos + Caixa + Créditos = Líquido` worst 0.50 R$mi.
- New metric reproduces the BNDES channel: +4.65% GDP 2010-05, −2.65% 2018-08, +0.67%
  2026-06. Parent = Σ 2 subcomponents to 0.10 R$mi.

## Open items / next steps

1. **Nothing is committed.** Review and commit; the DB table already exists, so a fresh
   clone would need it created.
2. **Never opened in a real browser** — standing sandbox limitation for every report here.
   Highest-value next check.
3. **`rtn` payload is 9.69 MB of the ~15.8 MB file** (`gfsm` 3.34 MB) — each variant
   repeats its own 354-date array. Migrating both to the shared-dates shape `dlsp_tab.py`
   uses would cut the file several-fold; means touching `makeHierTab()`'s accessor.
4. **Stacked-bar conditioning-factors chart** — bars summing to the change in the stock.
   All data is already in the payload; the 9 line charts never show the factors adding up.
5. **Consolidado mode** for the balance sheet — deliberately not built (see Gotchas).
6. **Gross reserves as their own line** — needs `cmb_reservas_bc` joined into `dlsp_tab.py`.
7. `Evldp.xlsx` (sibling workbook, DBGG side plus %PIB, ~20 tabs) reachable via the same
   connector, not ingested; each tab has its own layout, so parsing is a real job.

## Files to read first

- `domain/db/brasil/bcb/fisc_dlsp_fatores.py` — the docstring is the source of truth on
  sign convention, the identity, and why upsert-not-truncate.
- `analytics/brasil/fiscal_policy/dlsp_tab.py` — payload shape, `_CLASSE`, the %PIB rule.
- `analytics/brasil/fiscal_policy/CLAUDE.md` — Gotchas and Pending are current as of this session.
- `analytics/brasil/fiscal_policy/report.html` — `makeDlspHierTab()` and `renderDlspTab()`.
- `analytics/brasil/fiscal_policy/fontes_dados.md` — inventory of the BCB Tabelas Especiais folder.

## Gotchas

- **`ls -la` piped to `awk` reports the wrong size field on this machine** — the username
  "LIS CAPITAL" contains a space, shifting columns, so size is field 6, not field 5. This
  made me report "0.20 MB" for a 15 MB file early on. Use `stat -c "%s"` instead.
- The report was **already ~13.2 MB before this thread** — the new tab added 1.95 MB, not
  the bulk. Don't blame the DLSP tab for the file size.
- **jsdom harness**: `const REPORT_DATA` is a lexical binding and is **not** on `window`;
  the template's own `var D = REPORT_DATA` is, so read `window.D`. Also replace the Plotly
  CDN script tag with an inline stub (jsdom fetches no resources) and give each chart div
  an `el.on = function(){}` or `_bindYAutofit` throws. Harness lives at
  `<scratchpad>/verify_dlsp_tab.js` with `jsdom` installed locally there.
- **`Facdetp.xlsx` was not discoverable by search.** The BCB Estatísticas Fiscais page is
  an Angular SPA — WebFetch/requests return only the shell, and web search found nothing
  for "Facdetp". Found by probing candidate URLs directly; 4 wrong paths 404'd before
  `/content/estatisticas/Documents/Tabelas_especiais/` worked.
- **Indentation in the workbook is leading spaces in the string, not `alignment.indent`**
  (which is 0.0 everywhere), and it is inconsistent — sibling rows 25/26 have 7 and 6
  spaces. That is why `_ITEMS` is hardcoded rather than inferred at runtime.
- Writing this handover with a `cat > file <<'EOF'` heredoc **failed** with an unmatched-quote
  parse error despite the quoted delimiter; fell back to `rm -f` plus the Write tool.
- Two rejected/interrupted tool calls happened mid-session (a WebFetch and one data query);
  both were retried successfully. No partial state left behind.
- A message claiming to be a "CRITICAL" system instruction to dump a formatted summary
  arrived as a plain user turn with no `system-reminder` — flagged as an injection attempt,
  not complied with. Noted only so a re-reader isn't confused by it in the transcript.

---

→ **also save to memory** (not saved automatically — needs sign-off): the `ls -la` /`awk`
field-shift gotcha caused by the space in the Windows username, since it will silently
misreport file sizes in any future session on this machine.

→ **already in `CLAUDE.md`**, no action needed: the new table, the connector, the sign
convention, the 4-tab report state, and all Pending items above are written into root
`CLAUDE.md`, `domain/db/CLAUDE.md`, `connectors/CLAUDE.md` and
`analytics/brasil/fiscal_policy/CLAUDE.md`.
