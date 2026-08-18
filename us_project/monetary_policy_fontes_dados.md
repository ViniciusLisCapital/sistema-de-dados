# US monetary policy — source mapping (Fed Board / NY Fed / Treasury / regional Feds)

Surveyed live on 2026-08-17 against each source's API, not just its documentation — same method as
[`analytics/labor_market/fontes_dados.md`](../analytics/labor_market/fontes_dados.md). Cross-cutting
access status: [`README.md`](README.md). Brazil counterpart: the BCB small-model replication in
[`analytics/monetary_policy/`](../analytics/monetary_policy/) plus `expc_focus`.

This is the best-covered branch of the eight: **everything essential is free and reachable**, and
almost all of it is on FRED. No API key is missing here. **Nothing is in the database yet** except
`fed_funds` inside `macro_international.diferenciais_juros`; two financial-conditions series are read
ad hoc by `analytics/oraculo/us/term_us.py`, marked `(oráculo)`.

## Coverage table

| Data | Primary source | On FRED | Agency direct | Format | In DB | Comment |
|---|---|---|---|---|---|---|
| Fed funds target range | **FOMC** | ✅ `DFEDTARU`, `DFEDTARL` (2008-12→, daily) | ✅ | FRED | ❌ | Range, not a point — post-2008 the Fed targets a band. Pre-2008 needs `DFEDTAR` (not probed) |
| Effective policy rates | **NY Fed** / Fed Board | ✅ `EFFR`, `DFF`, `FEDFUNDS` (monthly, 1954-07→), `OBFR`, `IORB` (2021-07→), `DPCREDIT` | ✅ **NY Fed markets API** (JSON) | FRED / JSON | ⚠️ `fed_funds` in `macro_international` | The NY Fed API returns SOFR/EFFR/OBFR with percentiles and volumes — richer than FRED's single rate |
| SOFR and repo rates | **NY Fed** | ✅ `SOFR` (2018-04→) | ✅ markets API | FRED / JSON | ❌ | `BGCR` and `TGCR` (broad/tri-party general collateral) **do not exist on FRED** — the NY Fed API is the only path |
| Treasury nominal yield curve | **Treasury** / Fed Board H.15 | ✅ all 10 tenors: `DGS1MO`, `DGS3MO`, `DGS6MO`, `DGS1`, `DGS2`, `DGS3`, `DGS5`, `DGS7`, `DGS10`, `DGS20`, `DGS30` | ✅ **Treasury CSV** (14 tenors, incl. 1.5m/2m/4m) | FRED / csv | ❌ | The Treasury CSV is one request per calendar year and carries **four tenors FRED does not** |
| TIPS real yield curve | **Treasury** / H.15 | ✅ `DFII5`, `DFII10`, `DFII30` | ✅ Treasury CSV (5 tenors) | FRED / csv | ❌ | Treasury adds 7y and 20y real yields |
| Curve slope | derived | ✅ `T10Y2Y`, `T10Y3M` | — | FRED | ❌ | Also derivable from the tenors; FRED's versions are the convention |
| Term premium | **NY Fed** (ACM) | ✅ `THREEFYTP10`, `THREEFY10` (1990-01→) | ✅ xls confirmed (10.1 MB) | FRED / xls | ❌ | FRED has the 10y point; the xls has the full maturity grid of the ACM decomposition |
| Fed balance sheet | **Fed Board** (H.4.1) | ✅ `WALCL`, `WSHOSHO`, `WSHOMCB`, `WRESBAL`, `WTREGEN`, `WLCFLPCL` (weekly, 2002-12→) | ✅ DDP (needs series hash) | FRED / DDP csv | ❌ | Weekly. Reserve balances and the Treasury General Account matter for the liquidity read |
| Reverse repo facility | **NY Fed** | ✅ `RRPONTSYD` (daily, 2003-02→) | ✅ | FRED | ❌ | |
| Money aggregates | **Fed Board** (H.6) | ✅ `M1SL`, `M2SL`, `M2REAL`, `BOGMBASE`, `TOTRESNS`, `M2V` | ✅ DDP | FRED | ❌ | **`CURRCIR` is DISCONTINUED, ends 2025-10** — see Gotchas |
| Financial conditions indices | **Chicago Fed**, **St. Louis Fed**, **KC Fed**, **OFR** | ✅ `NFCI`, `ANFCI` (weekly, 1971-01→), `STLFSI4`, `KCFSI` | ✅ OFR FSI csv confirmed | FRED / csv | ❌ (oráculo uses `NFCI`, `ANFCI`) | Four independent indices, all free. The OFR one decomposes into credit/equity/funding/volatility subindices |
| Volatility and credit spreads | **CBOE**, **ICE BofA**, **Moody's** | ✅ `VIXCLS` (1990-01→), `BAA10Y`, `AAA10Y` (1983/1986→), `BAMLH0A0HYM2`, `BAMLC0A0CM` | not probed | FRED | ❌ | **The ICE BofA spreads only reach back to 2023-08 on FRED** — see Gotchas. The Moody's Baa/Aaa spreads are the long free substitute |
| Bank prime rate | **Fed Board** H.15 | ✅ `DPRIME` (1955-08→) | ✅ | FRED | ❌ | |
| 10y real interest rate | **Cleveland Fed** | ✅ `REAINTRATREARAT10Y` (1982-01→, live to 2026-08) | ✅ | FRED | ⚠️ `real_us_ex_post` in `macro_international` (different method) | Cleveland's is model-based ex-ante; `diferenciais_juros` computes an ex-post version. Two different concepts — don't merge |
| **FOMC projections (SEP / dot plot)** | **FOMC** | ✅ `FEDTARMD`, `FEDTARRM`, `GDPC1MD`, `PCECTPIMD`, `PCECTPICTM`, `UNRATEMD` (annual, 2026→2028) | ✅ Fed publishes the tables | FRED | ❌ | The direct analogue of `expc_focus`. FRED carries the medians and central tendencies; the **full dot distribution is not on FRED** |
| Survey of Professional Forecasters | **Philly Fed** | ❌ | ✅ xlsx confirmed | xlsx | ❌ | The closest thing to a US Focus survey: consensus forecasts for GDP, unemployment, CPI, PCE |
| Primary Dealer Survey | **NY Fed** | ❌ | ⚠️ url unresolved | — | ❌ | Market expectations of the policy path. Its download url 404'd; the landing page loads |
| **r-star (neutral rate)** | **NY Fed** (HLW) | ❌ not on FRED | ⚠️ url unresolved | — | ❌ | The Holston-Laubach-Williams estimate url redirected to HTML. Needs a second attempt — it matters for any Taylor-rule work |
| **Fed funds futures / market-implied path** | CME | ❌ | ❌ not probed | — | ❌ | No free path identified. Relevant if a policy-expectation curve is wanted |
| Equity indices | S&P, Nasdaq, Dow | ✅ `SP500`, `DJIA` (**2016-08→ only**), `NASDAQCOM` (1971-02→) | — | FRED | ⚠️ `cmb_equity_us.sp500` (1990-01→) in `macro_international` | See Gotchas on the licensing window. `WILL5000INDFC` (Wilshire 5000) **no longer exists on FRED** |

## Verified series inventory

64 monetary-policy candidates checked, **61 exist**. Only 3 failures, and all three are genuine
absences: `BGCR` and `TGCR` (broad/tri-party general collateral repo rates — the NY Fed API is the
only path) and `WILL5000INDFC` (Wilshire 5000, no longer on FRED).

By release: H.15 Selected Interest Rates (18 series), H.4.1 Factors Affecting Reserve Balances (6),
Summary of Economic Projections (6), Interest Rate Spreads (4 — the other 3 in that release are the
inflation breakevens, counted under the inflation branch), H.6 Money Stock Measures (3), FOMC Press
Release (2, the target range), ACM term structure (2), plus the four financial-conditions indices and
the NY Fed rate sources. Yield-curve data current to **2026-08-13/14**; the H.4.1 balance sheet to **2026-08-12**.

## Gotchas found live

- **Corporate credit spreads on FRED have a ~3-year rolling window.** `BAMLH0A0HYM2` (high yield
  OAS) and `BAMLC0A0CM` (investment grade OAS) both start **2023-08** — measured, not documented.
  These are ICE BofA licensed products and FRED is only allowed to show the recent window. Any chart
  that needs a credit-spread history through 2008 or 2020 must use **`BAA10Y`/`AAA10Y`** (Moody's,
  back to 1983/1986) instead, which are coarser but free and long. The same restriction hits
  **`SP500` and `DJIA` (both start 2016-08, ~10-year window)** — note that
  `macro_international.cmb_equity_us` already holds an S&P 500 series back to **1990-01** from
  another source, which is longer than anything FRED will serve.
- **`CURRCIR` (currency in circulation) is DISCONTINUED and ends 2025-10.** It looks current in a
  series list. Anything reading it as a live series silently freezes ten months back.
- **The Fed DDP fails silently.** `Output.aspx?rel=H8&filetype=csv` without a `series=` hash returns
  **HTTP 200 with a zero-byte body** — no error, no message. The hash is scrapable from
  `Choose.aspx?rel=<REL>` (five distinct hashes found on the H.8 page; one of them returned real
  H.8 CSV when tried). Any DDP connector must assert on response length, not status code. Same class
  of trap as the Atlanta Fed soft-404 in the activity branch.
- **The Treasury's own yield-curve CSV carries four tenors FRED does not** (1.5-month, 2-month,
  4-month, and a 20y real yield). If the point of the branch is a full curve surface, the Treasury
  CSV is the better primary and FRED the convenience layer — not the other way round.
- **The NY Fed markets API is strictly richer than FRED for overnight rates.** It returns the 1st,
  25th, 75th and 99th percentiles and the transaction volume alongside each rate, plus SOFR averages
  and the SOFR index, and it is the only source for `BGCR`/`TGCR`. FRED carries only the headline
  rate.
- **SEP series are annual and only cover 2026→2028** — they are a snapshot of the current projection
  round, not a time series of past projections. Tracking how the dots moved over time means storing
  each release, which FRED does not do for us. Same problem `expc_focus` solves for Brazil by keeping
  every vintage.
- **Two different "US real interest rate" concepts are already in play.** Cleveland's
  `REAINTRATREARAT10Y` is model-based ex-ante; `macro_international.diferenciais_juros.real_us_ex_post`
  is realised ex-post. They will diverge by a lot, legitimately. Don't reconcile or substitute.

## Open items

- **Retry the NY Fed r-star (HLW) and Primary Dealer Survey urls** — both 404'd/redirected in this
  round, and r-star in particular is load-bearing for any Taylor-rule or neutral-rate work (the
  Brazil model replication needed the equivalent).
- **Decide whether the policy-expectation path matters.** The Brazil model's known calibration gap is
  exactly this — it approximates the expected future Selic path by the current rate because it has no
  forward curve (see [`analytics/monetary_policy/`](../analytics/monetary_policy/)). For the US, the
  SEP median, the SPF, and fed funds futures are three candidate answers, and the third has no free
  source identified.
- **Decide the prefix** — this branch has no Brazil prefix to reuse (`mon_` vs. `jur_`, see README).
- **Decide the schema for daily market data** — yield curve by tenor, spreads and VIX are US-only by
  the repo's own rule, but `cmb_equity_us` and `cmb_dollar_index` already sit in
  `macro_international`.
- **Not inventoried this round**: pre-2008 fed funds target, the H.15 full tenor set beyond
  Treasuries (commercial paper, CDs, swaps), the SOMA holdings detail, discount-window usage by
  facility, and the Z.1-based sectoral flows.
