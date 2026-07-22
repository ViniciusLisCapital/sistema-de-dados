# analytics/exchange_rate/ — Panorama Cambial

Self-contained HTML report on Brazilian FX fundamentals (`reports/fx_report.html`) — single file, opens in any browser, safe to email. Reads from `macro_brasil` and `macro_international` (see [`domain/db/CLAUDE.md`](../../domain/db/CLAUDE.md) for schema-naming conventions). This is the applied/analytics branch of the exchange-rate work — see root `CLAUDE.md`'s `repository/` section for how it relates to the literature-curation and consolidated-synthesis branches.

## Generating the report

```powershell
uv run python jobs/update_db.py             # refreshes macro_brasil (cmb_reservas_bc, cmb_cambio_contratado, cmb_ptax, cmb_balanco_pagmt, cmb_fluxo_cambial, cmb_termos_troca, cmb_comex_*, atv_pib_usd)
uv run python jobs/update_international.py  # refreshes macro_international (cmb_reer, cmb_cot_fx, diferenciais_juros)
uv run python -c "from analytics.exchange_rate.generate_report import run; run()"
# → reports/fx_report.html (~50 KB)
```

Updating the DB first is optional — only needed for fresher data. `generate_report.py` alone re-renders against whatever is already in MySQL.

## Report architecture

Fixed template (`report.html`) with a `/*REPORT_DATA*/` marker inside a `<script>` block. `generate_report.py` loads each table, serializes to JSON, and does a plain `str.replace()` — no Jinja2, no templating engine. Every `_load_*()` function is independently try/excepted, so one missing or broken table degrades just that section (prints a warning) instead of failing the whole report.

Six tabs, real switching via JS `display` toggling (not scroll anchors): Balanço de Pagamentos (`tab-bop`, plus a companion BOP heatmap at `tab-heatmap`), Posicionamento do BCB (`tab-bcb`), Fluxo Cambial (`tab-flow`), Cotação (`tab-quotation`), Valuation (`tab-valuation`).

## Section → schema → table mapping

| Report tab | Loader (`generate_report.py`) | Schema | Table(s) |
|---|---|---|---|
| Cotação | `_load_ptax` | `macro_brasil` | `cmb_ptax` |
| Valuation | `_load_diferenciais` | `macro_international` | `diferenciais_juros` |
| Valuation | `_load_reer` | `macro_international` | `cmb_reer` |
| Valuation | `_load_cot_fx` | `macro_international` | `cmb_cot_fx` |
| Valuation | `_load_termos` | `macro_brasil` | `cmb_termos_troca` |
| Posicionamento do BCB | `_load_bcb_positioning` | `macro_brasil` | `cmb_reservas_bc` |
| Fluxo Cambial | `_load_fluxo` | `macro_brasil` | `cmb_fluxo_cambial` |
| BOP + Heatmap | `_load_bop` | `macro_brasil` | `cmb_balanco_pagmt` (+ `atv_pib_usd` for the "% of GDP" toggle) |
| BOP — by partner country | `_load_comex_pais` | `macro_brasil` | `cmb_comex_pais` |
| BOP — by aggregate factor | `_load_comex_fator_agregado` | `macro_brasil` | `cmb_comex_fator_agregado` |
| BOP — by product | `_load_comex_produto` | `macro_brasil` | `cmb_comex_produto` |

Note: interbank FX volume (`fx_interbank_vol_t1`/`t2`) lives in `cmb_ptax` but is charted under Fluxo Cambial, not Cotação — Cotação shows only the spot level.

`agent_data.py` (`get_fx_snapshot()`, consumed by the `cambio-analyst` subagent) reuses these same `_load_*()` functions and reduces each series to latest value + 1m/3m/12m deltas + a `stale` flag (per-group expected-gap thresholds hardcoded in `_EXPECTED_GAP_DAYS`).

## Current data-quality gotchas

- **Financial Account sign flip is deliberate** (`_load_bop()` only — never touches the DB): `idp_exterior`, `portfolio_ativos`, `outros_inv_ativos`, `acoes_ativos`, `fundos_ativos`, `titulos_ativos_cp`, `titulos_ativos_lp`, `derivativos`, `ativos_reserva`, and `conta_financeira` are negated so the whole report reads "negative = USD outflow, positive = inflow" consistently, matching how Current Account already reads. Liabilities-side series (`investimento_direto_liquido`, `portfolio_passivos`, etc.) already publish in that convention and are left untouched. If you touch this function, re-derive the sign from a real month rather than assuming Assets/Liabilities are symmetric.
- **Units are not uniform:** `cmb_balanco_pagmt`, `cmb_reservas_bc`, `cmb_fluxo_cambial` store USD MM (divided by 1000 for display). `cmb_comex_pais`/`cmb_comex_fator_agregado`/`cmb_comex_produto` store raw USD (divided by 1e9).
- **Comex Stat breakdowns ≠ BPM6:** the by-country/by-factor/by-product tables use general-trade methodology (SISCOMEX), not BPM6 — their totals will not reconcile line-for-line with `cmb_balanco_pagmt.mercadorias_gerais`. Treat them as complementary cuts, not a decomposition of it.
- **Some "missing" months in Comex/product series are real zeros, not gaps** (e.g. `demais_import` in the Fator Agregado breakdown, `minerio_ferro_import`/`petroleo_export` in the product breakdown — confirmed as months with zero transactions, not pipeline failures). `generate_report.py` `fillna(0)`s these deliberately; do the same for any new derived series built on top.
- **`lucros_reinvestidos` (BCB SGS 22815) has no data 1999–2010** (confirmed 404 from the BCB API, not a pipeline bug) — already `fillna(0)`'d before summing into `lucros_dividendos`.
- **No "gross reserves" series** — SGS 13127 (`reservas_brutas_usd`) times out consistently (wrong/discontinued code); resolved by using the liquidity concept (`cmb_reservas_bc.reserves_liquidity_daily`) plus its detailed components instead. Not a gap to revisit.

## Reference material (`referencia/`)

Not read by any script — background only:
- `balance_payments_breakdown.xlsx` — the official SGS-code mapping behind `cmb_balanco_pagmt.py`; check this before adding or changing BOP series.
- `fx_forecasting_theory_vs_practice.md` and `fx_forecasting_literature_review.md`/`.pdf` — standalone writeups on FX forecasting theory vs. practice (UIP failure, scapegoat theory, terms-of-trade channel, with a Brazil-specific section).
- `er_forecasting/` — the 9 underlying academic papers those two documents draw from.

## `models/` (new — not yet wired into any report)

A separate research track: statistical models testing FX theory directly against this database (currently a UIP regression, `models/uip_model.py`). See `models/DATA_REQUIREMENTS.md` for what each candidate model needs vs. what already exists in `macro_brasil`/`macro_international`, and `models/uip_model.md` for the first model's results and next steps. Distinct from `generate_report.py`, which only displays raw series — no estimation.

## Pending / next steps

- **BOP "Financiamento Externo" — 10 lines with no SGS code identified**: asset-side bank/non-bank split, and the public/private/direct/other split within LP external loans (both inflows and amortizations). Two next steps identified, neither executed: (1) accept the coarser breakdown `balance_payments_breakdown.xlsx` already provides instead of forcing an exact match, or (2) search the BCB SGS series finder for codes outside the 22701–23060 range already in use.
- **Interest differentials are ex-post only** — ex-ante (Focus Selic/IPCA 12m for Brazil; Fed funds futures/OIS and Michigan survey or breakevens for the US) is not implemented. Add as new `_ex_ante`-suffixed series in `diferenciais_juros`, not a replacement of the existing ones.
- **Cotação tab shows only BRL/USD** — explicit user ask for EM peer currencies (MXN, CLP, COP) side by side; no spot series for those pairs exists in the DB yet (FRED has candidates like `DEXMXUS`) — blocked on authorization for new data collection, not on a technical blocker.
- **Fluxo cambial — CEP/CBE sub-items** (candidate SGS codes 24372–24376) returned data in an initial search but descriptions are unconfirmed — cross-check against the BCB's weekly Nota Cambial before using them.
- **Cupom cambial + B3 FX futures (DOL/WDO)** — deferred indefinitely; requires Bloomberg (`blpapi`/`xbbg`) on the running machine.
