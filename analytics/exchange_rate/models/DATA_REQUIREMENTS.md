# FX driver models — data requirements mapping

*Companion to `referencia/fx_forecasting_theory_vs_practice.md` and `referencia/er_forecasting/`. Scopes what each candidate model needs, what's already in the database, and where the missing pieces could come from.*

## Status legend

- **Have** — already in `macro_brasil`/`macro_international`, ready to query today.
- **Fetchable, not stored** — a connector already supports pulling this; no ETL script exists yet.
- **No source wired yet** — no connector, no table; a real data-acquisition gap.

## Mapping

| Feeds | Series | Status | Where | Notes |
|---|---|---|---|---|
| PPP, UIP, monetary, scapegoat | Spot USD/BRL (PTAX) | **Have** | `macro_brasil.cmb_ptax.ptax_venda` | Daily since 1994-07-01 (Real Plan implementation — pre-Real data in extinct currencies removed 2026-07-22) |
| UIP, monetary, scapegoat | Selic × Fed Funds differential | **Have** | `macro_international.diferenciais_juros` | Already the rate-differential input |
| PPP | BR IPCA (headline) | **Have** | `macro_brasil.inflc_agregados` | |
| PPP | US CPI | **Have (partial)** | `macro_international.diferenciais_juros.cpi_12m_us` | Fetched via FRED `CPIAUCSL` inside `diferenciais_juros.py`; reusable directly for relative-PPP |
| Monetary/asset | US M1/M2, US real GDP | **Fetchable, not stored** | `connectors/fred.py` (`FredMultFrame`) supports any FRED series ID; no script fetches these yet | Needs a new `domain/db/us/` script + a new `macro_us` schema (see below) |
| Monetary/asset | BR monetary aggregates (M1/M2) | **No source wired yet** | Likely BCB SGS, exact series to confirm | BR GDP side is covered (`atv_pib`/`atv_pib_usd`) — only the money-supply side is missing |
| Monetary/asset | BR real GDP | **Have** | `macro_brasil.atv_pib`, `macro_brasil.atv_pib_usd` | |
| CA/BOP | Terms of trade, BOP, cambial flow, commodity index | **Have** | `macro_brasil.cmb_termos_troca`, `cmb_balanco_pagmt`, `cmb_fluxo_cambial`, `comm_icbr` | Strongest-covered model — no new data needed |
| Portfolio balance | Speculative positioning (proxy for order flow) | **Have (proxy only)** | `macro_international.cmb_cot_fx` (CFTC), `macro_brasil.cmb_fluxo_cambial` | True tick-level order flow (Evans & Lyons style) has **no identified free source** — treat as a proxy, not the real channel |
| Valuation anchor | Real effective exchange rate (REER) | **Have** | `macro_international.cmb_reer` | |
| Scapegoat model | Fiscal result / public debt (% GDP) | **No source wired yet** | Two candidate paths: (1) BCB SGS "Finanças Públicas" series via `connectors/bcb.py` — simplest, same connector as everything else, exact SGS codes need confirming at implementation time; (2) SICONFI via `siconfipy` (already a `pyproject.toml` dependency) — richer/more granular (debt maturity, issuance), but the only existing exploration (`connectors/not_in_production/siconfi.py`) is unfinished, with open questions the user already flagged (reconciling primary/nominal result vs. BCB, expanding to maturity/issuance) | **Not built in this pass** — flagged as future work |
| Scapegoat model | Country risk / sovereign spread (EMBI or CDS) | **Have** | `macro_brasil.cmb_risco_pais` (`name='cds_5y_usd'`) | Brazil 5Y sovereign CDS, USD, bps. Sourced 2026-07-23 via manual CSV export from investing.com (no free API for this series) — see `domain/db/brasil/investing/cmb_risco_pais.py`. Daily, 2007-12-19 → today; one real gap in the source exports, 2015-12-02 → 2015-12-31 (31 days). Not the same instrument as EMBI+ (IPEA Data candidate still unexplored) but the same "sovereign risk premium" concept UIP/scapegoat literature calls for. |

## Bottom line

Fiscal result is now the one genuine data gap left for this work (country-risk/CDS was closed 2026-07-23 via `cmb_risco_pais`) — both were already implicitly flagged by `analytics/monetary_policy/model.py`'s own docstring (it lists "CDS risk premium" and "cyclically-adjusted fiscal result" as unsourced IS-curve terms; that docstring hasn't been updated yet to reflect the CDS series now existing — out of scope for this pass, revisit if/when that model starts consuming it). Everything else needed for the first models either already exists in `macro_brasil`/`macro_international`, or is a small, low-risk extension of an existing connector (`connectors/fred.py`, `connectors/bcb.py`) rather than a new data source.

## `macro_us` schema (planned, not yet created)

US-only series (money supply, real GDP) get their own `macro_us` schema rather than being folded into `macro_international`, which is reserved for inherently cross-country/relational data (`diferenciais_juros`, `cmb_reer`, `cmb_cot_fx`). This also resolves the pre-existing `CLAUDE.md` pendência ("US — expandir dados: ... schema `macro_us`"). Table/column design deferred to the monetary/asset model step.
