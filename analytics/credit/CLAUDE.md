# analytics/credit/ — Panorama de Crédito

Self-contained HTML report on Brazilian bank credit, built on `cred_credito_amplo`, `cred_credito_resumo`,
`cred_credito_familias`, `cred_inadimplencia_pj`, the 4 `cred_modalidade_*` tables, `cred_credito_porte`,
`cred_credito_atividade_economica`, `cred_credito_tipo_cliente`, and `cred_credito_controle_capital` — all
`macro_brasil`. Same `/*REPORT_DATA*/` marker-substitution pattern as the other analytics reports, built
directly on [`analytics/report_structure/`](../report_structure/CLAUDE.md) (no Jinja2, no build step).

Replaces `analytics/credit_stress/` (deleted by the user, along with its `insolv_falencia_rj` table and
`connectors/datajud.py` — see root `CLAUDE.md`'s Pendências if that history is ever needed). Scope is
bank credit only — no bankruptcy/insolvency data.

## Generate

```powershell
uv run python -c "from analytics.credit.generate_report import run; run()"
# Output: reports/credit_latest.html
```

All source tables are already in `jobs/update_db.py`'s routine run — no manual refresh needed first.

## Data source

The BCB workbook in this folder (`202607_Tabelas_de_estatisticas_monetarias_e_de_credito.xlsx`, "Tabelas
de Estatísticas Monetárias e de Crédito") is the map of what's SGS-available for this theme.
[`fontes_dados.md`](fontes_dados.md) has the full per-tabela inventory (what's in the database, what
isn't, and why) — don't re-derive that mapping here. Tabela 2 is the only credit tab left out of the
database entirely (fully redundant with Tabelas 3+4+5). The 3 monetary-aggregate tabs (base monetária,
fatores condicionantes, M1-M4) are a different theme and out of scope for this report.

**Unit**: `cred_credito_resumo`'s `saldo`/`concessao`/`concessao_sa` come from SGS in **R$ milhões**, not
R$ bilhões as the workbook's own headers claim — `report.html`'s `toBi()`/`toTri()` convert client-side.
Percentage-type metrics (`taxa_juros`, `spread`, `icc`, `inadimplencia`, `pct_pib`) need no conversion.

## Shared toolkit

- `analytics/credit/transforms.py` — `stl_seasonal_adjust()` (STL, frozen-factor "amostra anual"
  convention, same as `analytics/inflation/fetch_bcb.py`), `pct_change()`, `deflate_series()` (IPCA,
  chained to constant reais of the latest available IPCA month), `compute_pct_pib()`, `moving_average()`,
  and `compute_variants()`/`compute_variants_ma3()` — pre-compute every Nível/Y-Y/M-M/T-T ×
  Nominal/Real/% PIB combination in Python so the browser only reads, never computes.
- `analytics/credit/tree_helpers.py` — `leaf()`/`group()`/`direct()` build the hierarchical trees shared
  by all 4 tabs. A node only becomes an expandable "group" when the BCB actually publishes an SGS code
  for that rollup; a structural cut with no native total (e.g. porte, controle de capital) gets its total
  as a Python-side `sum_series()` **only when summing a level (R$) is valid** — never for growth-rate or
  percentage children, since summing a ratio across groups is not mathematically valid.
- `report.html`'s `makeHierTab(opts)` — one JS factory (table + expand/collapse + checkbox + chart) reused
  by the Saldo and Concessão tabs; Taxa & Spread and Inadimplência are bespoke JS instead (their shape —
  a data-source switch, an overlay checkbox, no growth/deflation math — diverges enough that forcing them
  into the factory would add more special-casing than it saves).
- Every interactive tab clips series to `_TAB_MIN_DATE = "2000-01-01"` before building — most
  modality-level codes only start 2007-03, so a shared start keeps every row on a comparable window.

## Tabs

**Saldo** — hierarchical table (Livre/Direcionado × PJ/PF × modalidade, 67 modalidades + 7
`cred_credito_resumo` totals), plus 3 more top-level groups (Por Porte de Empresa, Por Atividade
Econômica, Por Tipo de Cliente — all PJ-only, `saldo` metric, totals synthesized via `sum_series()` where
no native SGS total exists) and a second hierarchical table below for Crédito Ampliado
(`cred_credito_amplo`, Governo/Empresas/Famílias by instrument — all 4 totals synthesized). Toggles:
Nível/Y-Y/M-M(SA)/T-T(SA) × Nominal/Real/% PIB (% PIB is level-only, by explicit user decision — picking
it disables the other metric pills).

**Concessão** — same tree shape as Saldo, `metrica='concessao'`. Differences from Saldo: the "Nível"
itself is STL+MM3M-smoothed (concessão is a noisy flow, not a stock); only M/M and T/T (no Y/Y); Crédito
Livre PJ's "Cartão de Crédito" has 1 child instead of 3 (the BCB doesn't publish a concessão code for
parcelado/rotativo there — confirmed from the actual SGS codes, not assumed from Saldo's tree).

**Taxa & Spread** — a `Taxa Média | Spread` source switch, not a metric/basis toggle (no STL/deflation/%
PIB — already percentages). Taxa Média has smaller modality coverage than Saldo (no "Outros" rate
published anywhere; Livre PJ/PF also missing "Cartão — À Vista"). Spread has no modality breakdown at
all — the BCB never publishes it below recurso×segmento. Independent "Mostrar Selic" checkbox overlays
`cred_inadimplencia_pj.selic` regardless of which rows are checked.

**Inadimplência** — one tree reuniting every cut that publishes inadimplência (>90d, %), not just the
dedicated `cred_inadimplencia_pj` series: the 7 `cred_credito_resumo` totals, modality-level data from all
4 `cred_modalidade_*` tables (smaller coverage than Saldo — Livre PJ's "Cartão" is a single code, Livre
PF's has no "à vista" split), `cred_credito_porte` and `cred_credito_controle_capital` (neither publishes
a native total for this metric, and summing a ratio isn't valid — both render as **header-only rows**:
expandable, but no checkbox/value of their own since their `seriesKey` deliberately doesn't exist in
`series`), and `cred_inadimplencia_pj.atraso_pj` (15-90d, a different metric, kept as an isolated leaf).
Same "Mostrar Selic" pattern as Taxa & Spread.

- **Saldo de Maior Risco** (risk-rating classification, not realized delinquency) lives in this tab as
  two independent top-level groups: `saldo_maior_risco` (pre-4.966 methodology) and
  `saldo_maior_risco_res4966` (current). Confirmed live against the database: **zero date overlap** — the
  old methodology ends 2024-12, the new one starts 2025-01. Never concatenate these into one series —
  splicing would fabricate a level jump that reflects a classification-rule change, not an actual change
  in credit risk.

**Apêndice** — accordion of methodology notes for each tab above (small-base noise in near-extinct
modalities, coverage gaps, the % PIB/unit conventions, the Saldo de Maior Risco break).

## Gotchas

- Crédito ampliado (~R$19.7tri) and crédito do sistema financeiro (~R$7.3tri) are different universes and
  shouldn't reconcile — `cred_credito_amplo` includes government securities and external debt that never
  touch a bank balance sheet.
- `cred_ptc` (Pesquisa Trimestral de Condições de Crédito, 16 series) exists in the database but isn't
  charted in any tab yet.
- Small-base modalities (e.g. "Arrendamento Mercantil — Veículos", ~R$5-13mi saldo) can show
  thousands-of-percent swings month to month — mathematically correct, not a bug; read by level, not
  growth rate, documented in the Apêndice.
- No browser has been used to visually confirm any interaction in this report — same standing sandbox
  limitation as every report in this project. Verification so far is a Node harness (stub
  `document`/`Plotly`, not jsdom) run against the real generated `<script>` and real DB output.

## Pending

- Open `reports/credit_latest.html` in an actual browser and confirm table/expand/checkbox/toggle/chart
  interactions across all 4 tabs, plus pan/zoom/quick-range behavior on every chart.
- `cred_credito_controle_capital`'s `saldo`/`provisoes` metrics are still unused (only `inadimplencia` is
  charted, in the Inadimplência tab's "Por Controle de Capital" group).
- `cred_credito_resumo`'s residual un-charted series (`icc`, `concessao_sa`, the Tabela 14 "crédito não
  rotativo" cut) and `cred_ptc` — no tab surfaces either yet.
