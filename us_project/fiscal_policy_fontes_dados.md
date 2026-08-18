# US fiscal — source mapping (Treasury / BEA / CBO / OMB)

Surveyed live on 2026-08-17 against each source's API, not just its documentation — same method as
[`analytics/fiscal_policy/fontes_dados.md`](../analytics/fiscal_policy/fontes_dados.md), the Brazil
counterpart of this branch. Cross-cutting access status: [`README.md`](README.md).

The good news, and the headline of this survey: **the US Treasury has a real, open, documented JSON
API** — no key, no scraping, no xlsx parsing. That is a materially better position than the Brazil
fiscal branch, which needed reverse-engineering of both the Tesouro's undocumented Séries Temporais
API and the BCB's static-xlsx "tabelas especiais" directory. Every Treasury endpoint tried returned
live data on the first attempt.

**Nothing is in the database yet**, and no US fiscal series is used by the oráculo either — this
branch is starting from zero.

## The three-methodology problem

Brazil's fiscal report carries two incompatible methodologies (GFSM/EFGG by economic nature vs. RTN
by rubrica orçamentária) and spends an Apêndice note explaining that they do not reconcile. The US
has **three**, and the same discipline applies:

- **MTS** (Monthly Treasury Statement, Treasury) — cash basis, federal government, budget
  functions and agencies. Monthly. The RTN analogue.
- **NIPA government accounts** (BEA) — accrual basis, national-accounts concepts, federal *and*
  state/local, integrated with GDP. Quarterly. The GFSM/EFGG analogue.
- **Unified budget / fiscal year** (OMB and CBO) — the appropriations-and-projections frame, fiscal
  years ending 30 September. Annual.

They differ on timing (cash vs. accrual), scope (federal vs. general government) and period
(calendar vs. fiscal year). A single "US deficit" number without saying which of the three is a
category error.

## Coverage table

| Data | Primary source | On FRED | Agency direct | Format | In DB | Comment |
|---|---|---|---|---|---|---|
| Monthly receipts, outlays, deficit | **Treasury** (MTS) | ✅ `MTSR133FMS`, `MTSO133FMS`, `MTSDS133FMS` (1980-10→, live to 2026-07) | ✅ **Fiscal Data API** `/v1/accounting/mts/mts_table_1` | FRED / JSON | ❌ | FRED has the three headline totals only. The API has the full table hierarchy with `parent_id`/`classification_desc` — a real tree, ready for the hierarchical-table pattern the Brazil reports use |
| Receipts by source | **Treasury** (MTS t4) | ❌ (aggregate only) | ✅ `/v1/accounting/mts/mts_table_4` | JSON | ❌ | Individual income tax, corporate, social insurance, excise, customs. **No FRED equivalent at this granularity** |
| Outlays by agency | **Treasury** (MTS t5) | ❌ | ✅ `/v1/accounting/mts/mts_table_5` | JSON | ❌ | Legislative/Judicial/Executive by department. The analogue of the RTN-by-Poder-e-Órgão cut the Brazil report still doesn't have |
| Total public debt | **Treasury** | ✅ `GFDEBTN` (quarterly, 1966-01→), `GFDEGDQ188S` (% GDP, SA), `FYGFD` (annual) | ✅ **`/v2/accounting/od/debt_to_penny`, daily** | FRED / JSON | ❌ | Live probe: **$39.93tn total, $32.20tn held by the public, $7.73tn intragovernmental** at 2026-08-13. Daily granularity via the API vs. quarterly on FRED |
| Debt by holder | **Treasury** | ✅ `FYGFDPUN` (public), `FDHBFIN` (foreign), `FDHBPIN` (private), `FDHBFRBN` (Federal Reserve) | ✅ TIC for the foreign detail | FRED / csv | ❌ | `FDHBFIN` lags the others (ends 2025-10 vs. 2026-01). Country-level foreign holdings are in [`external_sector_fontes_dados.md`](external_sector_fontes_dados.md) |
| Debt by security type and maturity | **Treasury** (MSPD) | ❌ | ✅ `/v1/debt/mspd/mspd_table_1` | JSON | ❌ | Marketable vs. non-marketable, bills/notes/bonds/TIPS/FRN. The analogue of the Tesouro's Tema 18 estoque cut |
| Average interest rate on the debt | **Treasury** | ❌ | ✅ `/v2/accounting/od/avg_interest_rates` | JSON | ❌ | Live: **3.758% on Treasury bills** at 2026-07-31. The direct analogue of the BCB's `Tximplnp.xlsx` implicit-rate table — and here it is an API, not a spreadsheet |
| Treasury cash balance (TGA) | **Treasury** (DTS) | ✅ `WTREGEN` (weekly, via H.4.1) | ✅ `/v1/accounting/dts/operating_cash_balance`, **daily** | FRED / JSON | ❌ | Live: TGA opening balance **$959.4bn** at 2026-08-13. Daily cash flows are the highest-frequency fiscal read available anywhere |
| Interest cost | **BEA** / Treasury | ✅ `A091RC1Q027SBEA` (quarterly NIPA), `FYOIGDA188S` (% GDP, annual) | 🔑 BEA | FRED | ❌ | Live: **$1,247bn SAAR** in 2026-Q2 — worth flagging as a headline given where it now sits relative to defence spending |
| Government accounts, NIPA basis | **BEA** | ✅ `FGEXPND`, `FGRECPT`, `FGDEF`, `W068RCQ027SBEA`, `W006RC1Q027SBEA`, `AD01RC1Q027SBEA` (net lending/borrowing) | 🔑 BEA key needed | FRED | ❌ | This is the accrual/general-government frame. FRED has the aggregates; the **line-item detail needs the BEA key** |
| State and local government | **BEA** / Census | ✅ `SLEXPND`, `SLINV` | 🔑 BEA; Census for the survey detail | FRED | ❌ | The US analogue of Brazil's SICONFI gap — except here the aggregates *are* available, unlike Brazil where subnational was ruled out of scope entirely |
| Annual fiscal-year budget | **OMB** | ✅ `FYFR`, `FYONET`, `FYFSD` (**1901-06→**), `FYFSGDA188S` (% GDP, 1929→) | not probed | FRED | ❌ | Live: FY2025 receipts **$5.24tn**, outlays **$7.01tn**, deficit **−$1.77tn** |
| Projections / baseline | **CBO** | ✅ `GDPPOT`, `NROU` only | ❌ **CBO site 403s** | FRED | ❌ | CBO's own xlsx is bot-protected. The budget baseline (deficit and debt projections) has **no confirmed machine path** — the biggest gap in this branch |
| **Fiscal impulse / structural balance** | derived | ❌ | ❌ | — | ❌ | No published US equivalent of the IEG. CBO publishes a cyclically-adjusted balance in reports, not as a series. Would have to be built |

🔑 = the direct path needs an API key we do not have yet (free registration; see README).

## Treasury Fiscal Data API — reference notes

Base: `https://api.fiscaldata.treasury.gov/services/api/fiscal_service`. All confirmed live on
2026-08-17, no authentication, JSON, with `page[size]` and `sort=-record_date` working as documented.

| Endpoint | Content | Verified |
|---|---|---|
| `/v1/accounting/mts/mts_table_1` | Receipts, outlays, deficit/surplus — hierarchical | 2026-07-31 |
| `/v1/accounting/mts/mts_table_4` | Receipts by source | 2026-07-31 |
| `/v1/accounting/mts/mts_table_5` | Outlays by agency | 2026-07-31 |
| `/v2/accounting/od/debt_to_penny` | Total debt, daily | 2026-08-13 |
| `/v1/debt/mspd/mspd_table_1` | Debt by security type | 2026-07-31 |
| `/v2/accounting/od/avg_interest_rates` | Average rate by security type | 2026-07-31 |
| `/v1/accounting/dts/operating_cash_balance` | Treasury General Account, daily | 2026-08-13 |
| `/v1/accounting/od/rates_of_exchange` | Official exchange rates (bonus, not fiscal) | — |

**The MTS tables carry `parent_id` and `classification_id`** alongside `classification_desc`, so the
budget hierarchy comes out of the API already structured — no prefix-matching on label strings like
`connectors/tesouro.py` has to do for the RTN. That is a real advantage worth exploiting in the table
design.

## Verified series inventory (FRED side)

31 fiscal candidates checked, **30 exist**; the only failure (`GFDEBTNGDP`) was an invented id — the
real debt-to-GDP series is `GFDEGDQ188S`. By release: Gross Domestic Product/NIPA (11 series, the
accrual frame), Treasury Bulletin (5, the debt holders), Monthly Treasury Statement (3), Fiscal Year
Budget Data (3), Debt to GDP Ratios (3), Economic Report of the President (2).

FRED's fiscal coverage is **shallow but sufficient for aggregates**, and the Treasury API more than
compensates below that. The one thing neither has is projections.

## Gotchas found live

- **The MTS carries `null` values in the amount columns of the most recent record.** The 2026-07-31
  rows returned `"current_month_gross_rcpt_amt": "null"` (the string, not JSON null) on the header
  rows of table 1. Header/subtotal rows and data rows share the same shape and are distinguished only
  by `parent_id`. Any parser must handle the string `"null"` and must not assume every row has a
  value — the same "header-only rows" convention the Brazil credit and labor reports already use in
  their trees.
- **Fiscal year ≠ calendar year.** The US fiscal year ends 30 September, so `FYFR`/`FYONET`/`FYFSD`
  are dated `2025-09-30` for FY2025, and MTS table 1's `classification_desc` literally contains
  `"FY 2025"` as a row label. Any year-over-year or accumulated-in-the-year metric (the Brazil
  reports' "Acum. no ano") has to reset in **October**, not January. Getting this wrong silently
  produces a 3-month-offset series that still looks plausible.
- **`FDHBFIN` (debt held by foreign investors) lags its siblings by a quarter** — ends 2025-10 while
  `FYGFDPUN`/`FDHBPIN`/`FDHBFRBN` reach 2026-01. A holder-composition chart built on the four will
  have a hole in the most recent quarter unless the foreign line is sourced from TIC instead.
- **CBO is bot-protected (403 on the xlsx).** FRED redistributes only `GDPPOT` and `NROU` from CBO,
  both of which extend to **2036-10** as projections — see the activity/labor gotchas about reading
  "the last observation" off a forecast series. The deficit and debt *baseline* projections have no
  confirmed machine-readable path, so a "current-policy debt trajectory" chart is not costed yet.
- **Debt-to-the-penny is daily and the % of GDP series is quarterly and SA.** `GFDEGDQ188S` is
  seasonally adjusted (unusual for a debt ratio, and it is FRED's own construction over a quarterly
  GDP denominator). Mixing the daily stock with the quarterly ratio in one chart means two different
  denominators and two different frequencies.
- **No fiscal-impulse equivalent exists off the shelf.** Brazil's report has the IEG (published
  multipliers from a named paper) plus a primary-result impulse plus a parafiscal credit channel. The
  US has none of those as a series. If an impulse metric is wanted, it has to be constructed, and the
  multiplier problem the Brazil report documents as unresolved on the revenue side applies here on
  both sides.

## Open items

- **Get the BEA key** for the NIPA government accounts at line-item detail (the accrual frame, and
  the only one that covers state and local properly).
- **Find a machine path to CBO's baseline** or accept that projections are out of scope. Worth a
  second attempt with different headers before concluding — the Brazil side has a precedent for a
  "blocked" verdict turning out to be wrong on re-check.
- **Decide whether state and local is in scope.** Brazil ruled subnational out explicitly (SICONFI).
  For the US the aggregates are free and easy (`SLEXPND`, `SLINV`), so the trade-off is different.
- **Not inventoried this round**: the remaining Fiscal Data endpoints (there are dozens — Treasury
  auctions, TreasuryDirect, Financial Report of the US Government), MTS tables 6-9, the DTS deposits
  and withdrawals detail, and the Treasury Bulletin's ownership tables.
