# US housing — source mapping (Census/HUD / NAR / FHFA / S&P-Cotality / Freddie Mac)

Surveyed live on 2026-08-17 against each source's API, not just its documentation — same method as
[`analytics/labor_market/fontes_dados.md`](../analytics/labor_market/fontes_dados.md). Cross-cutting
access status: [`README.md`](README.md).

**No Brazil counterpart.** This branch exists because US housing has a monthly statistical complex
with no equivalent in the Brazil pipeline: five distinct primary publishers, its own release cycle,
and a direct transmission channel from policy rates through mortgage rates to activity. It is also
**the branch where licensing bites hardest** — two of the five publishers are private, and one of them
is restricted on FRED to thirteen monthly observations.

`analytics/oraculo/us/term_us.py` already scores six housing series (new homes sold, homes for sale,
months' supply, 30-year mortgage rate, Case-Shiller), marked `(oráculo)`. **Nothing is in the
database.**

## The five publishers

| Publisher | Owns | Free? |
|---|---|---|
| **Census + HUD** | New residential construction (starts, permits, completions, under construction), new home sales, construction spending, vacancy/homeownership rates | ✅ (Census API needs a key; FRED redistributes) |
| **NAR** (National Association of Realtors) | **Existing** home sales — ~85% of transaction volume | ❌ private; FRED window is 13 months |
| **FHFA** | House price index from conforming-mortgage transactions | ✅ csv, no key |
| **S&P / Cotality** (ex-CoreLogic) | Case-Shiller repeat-sales price indices | ⚠️ on FRED with a 2-month lag |
| **Freddie Mac** | Primary Mortgage Market Survey (30y/15y fixed rates) | ✅ via FRED |

## Coverage table

| Data | Primary source | On FRED | Agency direct | Format | In DB | Comment |
|---|---|---|---|---|---|---|
| Housing starts | **Census/HUD** | ✅ `HOUST` (SAAR, 1959-01→), `HOUST1F` (single-family), `HOUST5F` (5+ units), `HOUSTNSA` | 🔑 Census key needed | FRED | ❌ | Live at 2026-06: **1,427k SAAR total, 895k single-family, 513k multifamily**. The single/multi split matters — they cycle differently |
| Building permits | **Census/HUD** | ✅ `PERMIT`, `PERMIT1`, `PERMITNSA` | 🔑 Census | FRED | ❌ | Leads starts. Live: **1,374k SAAR** |
| Completions and units under construction | **Census/HUD** | ✅ `COMPUTSA`, `UNDCONTSA` | 🔑 Census | FRED | ❌ | The pipeline view — `UNDCONTSA` at 1,264k against 1,392k completions says the backlog is clearing |
| New home sales and inventory | **Census/HUD** | ✅ `HSN1F` (SAAR, 1963-01→), `HSN1FNSA`, `HNFSEPUSSA` (for sale), `MSACSR` (months' supply) | 🔑 Census | FRED | ❌ (oráculo uses all four) | Live at 2026-06: **628k sold, 485k for sale, 9.3 months' supply** |
| **Existing home sales** | **NAR** | ⚠️ `EXHOSLUSM495S`, `HOSSUPUSM673N` — **start 2025-07** | ❌ private | FRED | ❌ | **13 monthly observations, total.** Live: 4.06m SAAR, 4.6 months' supply at 2026-07. This is ~85% of the market and we effectively have no history for it — see Gotchas |
| New home prices | **Census/HUD** | ✅ `MSPUS` (median, quarterly, 1963-01→), `ASPUS` (average) | 🔑 Census | FRED | ❌ | Live at 2026-Q2: median **$410.7k**, average **$502.7k**. Quarterly, and new-construction only — not a market price index |
| Repeat-sales price index | **S&P/Cotality** | ✅ `CSUSHPINSA`, `CSUSHPISA` (national, 1987-01→), `SPCS20RSA` (20-city, 2000-01→) | ❌ | FRED | ❌ (oráculo uses `CSUSHPINSA`) | Live at **2026-05** — a 2-3 month lag by construction (3-month moving average of a lagged transaction record). Renamed from "S&P CoreLogic Case-Shiller" to **"S&P Cotality"** |
| Conforming-mortgage price index | **FHFA** | ✅ `USSTHPI` (quarterly, 1975-01→) | ✅ **`hpi_master.csv`, 17.0 MB, no key** | FRED / csv | ❌ | The csv carries every flavour (purchase-only, all-transactions), frequency and geography level in one file — far more than FRED's national quarterly series. `ATNHPIUS100S` does **not** exist; the metro ids look like `ATNHPIUS12420Q` |
| Mortgage rates | **Freddie Mac** (PMMS) | ✅ `MORTGAGE30US` (weekly, 1971-04→), `MORTGAGE15US` (1991-08→) | not probed | FRED | ❌ (oráculo uses `MORTGAGE30US`) | Live at 2026-08-13: **6.67% (30y), 5.96% (15y)**. **`MORTGAGE5US` (5/1 ARM) is dead — ends 2022-11** |
| Mortgage debt service burden | **Fed Board** | ✅ `MDSP` (quarterly, 2005-01→) | ✅ | FRED | ❌ | Also in [`credit_fontes_dados.md`](credit_fontes_dados.md) |
| Vacancy and homeownership rates | **Census** (HVS) | ✅ `RHORUSQ156N` (homeownership, 1965-01→), `RRVRUSQ156N` (rental vacancy, 1956-01→), `RHVRUSQ156N` (homeowner vacancy) | 🔑 Census | FRED | ❌ | Live at 2026-Q2: homeownership **65.0%**, rental vacancy **7.3%**, homeowner vacancy **1.2%** |
| Residential construction spending | **Census** | ✅ `PRRESCONS` (private, 1993-01→), `TLRESCONS` (total, 2002-01→) | 🔑 Census | FRED | ❌ | Live at 2026-06: **$877bn private SAAR** |
| Residential fixed investment | **BEA** | ✅ `PRFIC1` (quarterly, real) | 🔑 BEA | FRED | ❌ | The GDP-consistent measure; see [`activity_fontes_dados.md`](activity_fontes_dados.md) |
| Shelter inflation | **BLS** | ✅ `CUSR0000SAH1` (shelter), `CUSR0000SEHA` (rent), `CUSR0000SEHC` (owners' equivalent rent) | ✅ | FRED | ❌ | The bridge to the inflation branch — shelter is ~35% of core CPI |
| **Homebuilder sentiment (NAHB HMI)** | NAHB | ❌ **absent** | ❌ licensed | — | ❌ | Zero FRED search results. The standard leading indicator for starts, and not obtainable |
| **Market rents (Zillow ZORI, ZHVI)** | Zillow | ❌ `ZORI` does not exist | ⚠️ not probed | — | ❌ | Zillow's own research download page was not tested — worth trying, since ZORI leads CPI shelter by ~12 months and is the usual way to forecast it |
| Mortgage applications (MBA) | MBA | ❌ | ❌ | — | ❌ | Weekly purchase/refi applications index. Licensed, no free path identified |

🔑 = the direct path needs an API key we do not have yet (free registration; see README).

## Verified series inventory

33 housing candidates checked, **30 exist**. Failures: `ATNHPIUS100S` (wrong FHFA id form — the real
metro ids carry a CBSA code and a frequency suffix), `RENTSMOO` (invented) and `ZORI` (Zillow — a
genuine absence, not a wrong id).

By release: New Residential Construction (9 series), New Residential Sales (6), Housing Vacancies and
Homeownership (3), S&P Cotality Case-Shiller (3), Existing Home Sales (2), Primary Mortgage Market
Survey (2 here, plus `MORTGAGE30US` counted under credit), Construction Spending (2), FHFA House Price
Index (1), Household Debt Service Ratios (1), and the CPI shelter components.

Frequency mix: mostly **monthly SAAR** (starts, permits, sales), with prices split between monthly
(Case-Shiller, 2-3 month lag), quarterly (FHFA, Census median/average) and weekly (mortgage rates).

## Gotchas found live

- **Existing home sales — the licensing problem, and it is severe.** `EXHOSLUSM495S` starts
  **2025-07** and ends 2026-07: **thirteen monthly observations**. `HOSSUPUSM673N` (months' supply) is
  identical. NAR is a private association and FRED is only permitted a rolling window — the 13-month
  span is exactly consistent with that, though the rolling-window mechanism is my inference from the
  measured dates rather than a documented statement. Either way: **existing home sales covers ~85% of
  US transactions and we have no usable history for it.** Any housing tab has to be built around new
  home sales (Census, 1963→) as the volume proxy, with existing sales as a current-level annotation
  only. `analytics/oraculo/us/term_us.py` already scores only Census series, which sidesteps this by
  accident rather than by design.
- **Case-Shiller lags 2-3 months by construction.** Latest observation was **2026-05** when probed on
  2026-08-17. It is a 3-month moving average of already-lagged recorded transactions, so this is
  inherent, not a FRED delay. For a current price read, FHFA's purchase-only monthly index (in
  `hpi_master.csv`) is fresher; for the long history Case-Shiller reaches 1987.
- **FHFA's csv is one 17 MB file containing every series** — `hpi_type` × `hpi_flavor` × `frequency` ×
  `level` × `place_name`, with `index_nsa`, `index_sa` and a standard error per row. Confirmed live
  from the header. This is much richer than FRED's single quarterly national series and is free with
  no key, which makes it the better primary for prices.
- **Three id traps in this branch.** `ATNHPIUS100S` does not exist (the FHFA metro ids look like
  `ATNHPIUS12420Q`, with a CBSA code and a frequency suffix). `MORTGAGE5US` exists but **ends
  2022-11**. `HOUST` is SAAR in thousands while `HOUSTNSA` is the raw monthly count in thousands
  (1,427 vs. 134.2 for the same month) — same unit label, factor-of-12 difference.
- **Median new home price is quarterly and is not a price index.** `MSPUS` measures the mix of houses
  actually built and sold, so it moves when builders shift to smaller units even with flat prices.
  Case-Shiller and FHFA are repeat-sales indices and are the right measure of price *change*. Do not
  put them on the same axis.
- **NAHB is unavailable** (zero FRED results), which removes the conventional leading indicator for
  starts. Permits (`PERMIT`, `PERMIT1`) are the free substitute and lead starts by ~1-2 months, but
  they are an activity measure rather than a sentiment one.

## Open items

- **Get the Census key** for starts/permits/sales by region and structure type, and the HVS detail.
- **Try Zillow's own research download** (ZORI/ZHVI) — not probed this round. ZORI leads CPI shelter
  by roughly a year and is the standard input for forecasting the largest single component of core
  inflation, so it is worth more than its absence from FRED suggests.
- **Decide how to handle the existing-home-sales history gap** before designing the tab: build the
  volume view on new home sales only, buy NAR data, or accept a 13-month chart for the biggest part of
  the market.
- **Prefix decision** — no Brazil counterpart to reuse (`hous_` vs. `imob_`, see README).
- **Not inventoried this round**: regional/metro cuts of everything above, MBA applications, HUD's own
  publications, rental market indices other than CPI, and homebuilder financials.
