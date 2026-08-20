# Handover — 2026-08-17

Scope: the whole session. Two phases: (1) feasibility investigation of two BCB credit
metrics, (2) building the **Impulso** tab in `analytics/brasil/credit/` from the metric that
survived that investigation.

---

## 1. Goal

Started as a pure feasibility question: *"the BCB computes financial flow and credit
impulse — investigate and see if we can calculate them."* Explicitly framed as
investigation only, no build.

Shifted mid-session. After the investigation the user said **"Forget the BCB metric,
we'll not use that"** and asked for three specific tables in a new Impulse tab. The
final ask was the chart form: stacked bars for components, total as a line.

## 2. Instructions and constraints the user gave

- **"This is just a feasability investigation"** — phase 1 was research only, no code.
- **"Forget the BCB metric, we'll not use that."** The BCB Estudo Especial 110/2021
  measure (fluxo financeiro / impulso limpo via SCR) is OUT of the report. Do not build
  it, do not add it back without being asked. Only the IBRE/Biggs measure ships.
- Three tables, specified verbatim:
  - (a) Free and ear-marked with its immediate first division (PF / PJ)
  - (b) By company capitalization (MPME / Grande)
  - (c) By economic activity (Agro, Indústria, Serviços, Outros)
- **"Create the graph using stacked bar and on the total as line."**
- Standing: don't call the Agent tool or workflows unless requested (neither was used).

## 3. Conventions and decisions established

- **Measure**: Biggs, Mayer & Pick (2009) as applied to Brazil by Blog do IBRE/FGV
  (Borça Jr., Furtado & Barbosa-Filho, 2021):
  `I(t) = [Saldo(t)-Saldo(t-12)]/PIB12m(t) - [Saldo(t-12)-Saldo(t-24)]/PIB12m(t-12)`,
  x100, in p.p. of GDP. Each flow is divided by ITS OWN contemporaneous GDP — this is
  NOT the second difference of the ratio C/Y.
- **Denominator**: `atv_pib_mensal.pib_acum_12m` (BCB SGS 4382), the same one BCB uses
  for `cred_credito_resumo.pct_pib_*`.
- **"Anual (dez)" is not a second calculation** — it is the monthly series filtered to
  December, where the formula collapses into the annual one IBRE publishes. Keep it that
  way; never add a parallel annual code path.
- **Chart uses `barmode: 'relative'`, NEVER `'stack'`.** Impulse components routinely
  carry opposite signs; `'stack'` piles everything in one direction and the stack top
  stops matching the total line. Single most important decision in the tab.
- **Anti-double-count rule**: tree root = the line; every other checked node = a bar,
  EXCEPT a node that has a checked descendant (finest level of the selection wins).
  A non-exhaustive selection deliberately leaves a visible gap to the line.
- New JS factory `makeImpulseTab()` kept SEPARATE from `makeHierTab()` — the impulse is
  already a ratio to GDP, so there is no Nominal/Real/%PIB basis to select, only a read
  frequency. Forcing it into `makeHierTab` would have meant inventing a fake basis group.
- Value formatting rounds BEFORE choosing the sign, so residual contributions print
  `0,00` and not `-0,00`.

## 4. Work completed

**New file**

- `analytics/brasil/credit/impulso_tab.py` (9.2 KB) — `compute_impulse()` (date-based t-12/t-24
  lookups, not positional), `_variants()` (m12 + anual), `build()`, the three trees
  (`_RECURSO_TREE` / `_PORTE_TREE` / `_ATIVIDADE_TREE`), `TREES`/`ANCHORS`, table
  configs. Module docstring carries the full rationale + validation numbers.

**Edited**

- `analytics/brasil/credit/generate_report.py` — import, `_load_impulso_tab_data()`, `run()`
  block with its own try/except (same degrade-gracefully pattern as the other tabs).
- `analytics/brasil/credit/report.html` (+373 lines) — nav button `Impulso` (between Concessão
  and Taxa & Spread), the tab panel with 3 sections, `makeImpulseTab()` factory + 3
  instances (`IMP_RECURSO_TAB`/`IMP_PORTE_TAB`/`IMP_ATIV_TAB`), `renderImpulseChart()`
  (bars + line), `RENDERERS.impulso`, a long Apêndice item.
- `analytics/brasil/credit/CLAUDE.md` — Impulso section under Tabs + `makeImpulseTab()` in the
  shared-toolkit list.
- `CLAUDE.md` (root) — added Impulso to the credit `report.html` tab list (this also
  removed a pre-existing duplicated "+ Concessao" in that sentence).

**Generated**: `reports/brasil/Credit.html` (12.0 MB, 16:03). Regenerated several times; the
last regen (16:03) is AFTER the concurrent `transforms.py` edit (16:02), so the
`pct_change` Infinity fix IS baked into the current output.

**Not committed.** Everything is working-tree only.

## 5. Current state

Working and verified by a Node DOM-stub harness that executes the REAL generated
`<script>` (no browser available in this environment). All ~40 checks pass:

- Replication matches IBRE's published figures: 2016 total **-5,30** (published -5,3),
  2016 públicos -4,13 (-4,1), 2020 públicos +2,78 (+2,8), monthly series crossing zero
  in nov/2021 (+0,08). 2020 total +4,29 vs +4,4 published = BCB revisions to saldo/PIB
  since the post, not method divergence.
- Stack top == total line to **2e-4 p.p. across all 208 monthly points** (that bound is
  the payload's own 4-decimal rounding, not a modelling residual — the harness tolerance
  was initially set to 1e-9 and had to be relaxed to 1e-3 for this reason).
- Anti-double-count rule verified live; non-exhaustive selection leaves a 3,94 p.p. gap.
- The four pre-existing tabs still render.

Harness lives in the session scratchpad at
`%TEMP%\claude\c--Users-LIS-CAPITAL-...\07162023-7dba-4490-8064-7fc7e2cb365a\scratchpad\harness.js`
(disposable). Run: `node <path> reports/brasil/Credit.html`.

## 6. Open items / next steps

1. **Open `reports/brasil/Credit.html` in a real browser.** Never done — same standing sandbox
   limitation as every report here. Specifically check bar width at ~208 monthly points;
   if too dense, the fix is `bargap` or defaulting monthly to a shorter quick-range.
2. **Offered but not built** (user has not answered): a `Fluxo` / `Impulso` metric pill
   showing the first term alone (12m credit flow as % of GDP). The impulse is hard to
   read without the flow it is the change of. Deliberately left out to respect scope.
3. **Pre-2007 splice not done** — livre/direcionado start 2007-03, so table (a) starts
   2009-03. IBRE reaches 2002 by splicing SGS 12130 (livre) and 7524 (direcionado), both
   confirmed live (Jun/2000→Dec/2012, 151/150 obs). Small addition to
   `cred_credito_resumo`, not a new connector.
4. Possible further cuts, all additive and already in the DB: bank ownership
   (`cred_credito_controle_capital`, saldo from 1988-06) and BNDES
   (`cred_modalidade_direcionado_pj.credito_com_recursos_do_bndes_total`). Both were
   computed during the investigation and reproduce IBRE parts 2 and 3.

## 7. Files to read first

- `analytics/brasil/credit/impulso_tab.py` — the docstring is the spec for the whole metric.
- `analytics/brasil/credit/CLAUDE.md` — "Impulso" section under Tabs.
- `analytics/brasil/credit/report.html` — `makeImpulseTab()` and `renderImpulseChart()`.
- `.claude/rules/lis-dashboards.md` — chart interaction model (pan/zoom, `_bindYAutofit`,
  quick-range buttons).

## 8. Gotchas

- **`barmode: 'stack'` is a trap here.** Reads correct, silently breaks the
  stack-vs-total reconciliation the moment components have opposite signs — which is the
  normal state, not an edge case. `_bindYAutofit` handles both `stack` and `relative`.
- **Tables (b) and (c) show identical totals — correct, not a bug.** They are two
  partitions of the SAME PJ aggregate; confirmed live at <=R$5mi apart on R$2,76tri. That
  aggregate is NOT exactly `saldo_total_pj` from Tabelas 3-5 (up to ~R$37bn / 1,3% apart
  at the 2020 peak), so (a) will not reconcile to the decimal with (b)/(c).
- **Ruled out, do not retry**: write-offs (baixas para prejuízo) have no public monthly
  source. Checked and eliminated — not in SCR.data (publishes only carteira ativa /
  inadimplência / ativo problemático; written-off ops leave the carteira), not in the
  COSIF balancetes open data at any vintage (2023-12 has 187 accounts, 2026-03 has 1.011;
  neither carries a write-off account, only the *recoveries* income account 7192000007),
  not in SGS. This is what makes the BCB EE110 measure non-replicable and is the reason
  the user dropped it.
- Balancetes are also heavily lagged now (Comunicado 44.132/2025: quarterly batches; Mar
  2026 only published 2026-08-03).
- **Concurrent work in this folder by another session/user** — `analytics/metric_layers.md`
  (new, 16:14) and a `pct_change` Infinity guard in `analytics/brasil/credit/transforms.py`
  (16:02). Neither was touched by this session; `impulso_tab.py` does not use
  `pct_change` at all. `analytics/CLAUDE.md` gained a "Metric layers" section. Do not
  revert any of it.
- The date-based `_shift_months()` lookup is deliberate — positional `i-12`/`i-24` would
  silently corrupt results on any calendar gap.
- Harness `El` stub needed `createTextNode`, an `on()` method (Plotly's `el.on`, used by
  `_bindYAutofit`) and `change_()`; **jsdom is NOT installed** in this repo.
- Writing this file via a Bash heredoc failed with a quoting error; the Write tool worked.

---

→ also save to memory: nothing durable identified this session beyond what
`analytics/brasil/credit/CLAUDE.md` now records.

→ candidate for `CLAUDE.md` "Pendências" (not added, needs sign-off): the pre-2007
livre/direcionado splice (item 6.3 above). The "confirm in a real browser" item for the
credit report already exists there and now covers the Impulso tab too.
