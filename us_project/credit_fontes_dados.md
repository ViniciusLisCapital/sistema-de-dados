# US credit — source mapping (Fed Board / FDIC / NY Fed / Freddie Mac)

Surveyed live on 2026-08-17 against each source's API, not just its documentation — same method as
[`analytics/labor_market/fontes_dados.md`](../analytics/labor_market/fontes_dados.md). Cross-cutting
access status: [`README.md`](README.md). Brazil counterpart:
[`analytics/credit/CLAUDE.md`](../analytics/credit/CLAUDE.md).

The Fed Board is to US credit what the BCB is to Brazilian credit: one publisher, several weekly and
quarterly releases, and a survey of lending conditions. The mapping onto the Brazil report's tabs is
unusually clean — **H.8** ↔ `cred_credito_resumo` (balances), **G.19** ↔ `cred_modalidade_*` (consumer
modalities and rates), **Charge-off and Delinquency Rates** ↔ the Inadimplência tab, **SLOOS** ↔
`cred_ptc`. What the US does *not* have is anything like the BCB's saldo-by-modality tree at 84-series
granularity from a single workbook.

**Nothing is in the database yet** and no US credit series is used by the oráculo.

## Coverage table

| Data | Primary source | On FRED | Agency direct | Format | In DB | Comment |
|---|---|---|---|---|---|---|
| Bank credit, total and by category | **Fed Board** (H.8) | ✅ `TOTBKCR` (weekly, 1973-01→), `TOTLL`, `INVEST`, `BUSLOANS` (**1947-01→**), `REALLN`, `CONSUMER`, `TOTCI` | ✅ DDP (hash confirmed working for H.8) | FRED / DDP csv | ❌ | The direct `cred_credito_resumo` analogue. Live: **bank credit $19.78tn, loans and leases $13.96tn, C&I $2.92tn** at 2026-08-05. FRED carries the aggregates; the H.8's ~100 series (by bank size, domestic vs. foreign-related) need the DDP |
| Bank credit growth rates | **Fed Board** (H.8) | ✅ `H8B1058NCBCMG` (deposits), `H8B1023NCBCMG` (C&I) | ✅ DDP | FRED | ❌ | Pre-computed month-over-month annualised growth — useful, but the naming is opaque and there is no way to guess siblings without the DDP catalog |
| **Bank lending standards and demand (SLOOS)** | **Fed Board** | ✅ `DRTSCILM` (large firms, 1990-04→), `DRTSCIS` (small firms), `DRTSCLCC` (credit cards), `DRTSSP` (residential), `DRSDCILM` (**demand**, 1991-10→), `DRIWCIL` (willingness to lend, 1982-04→) | ✅ | FRED | ❌ | The direct `cred_ptc` analogue — net percentage tightening, a diffusion index, quarterly. All live to **2026-07**. Note `DRTSDCILM`/`DRTSDCIS` (my guesses for the demand series) **do not exist** — the real one is `DRSDCILM` |
| Consumer credit outstanding | **Fed Board** (G.19) | ✅ `TOTALSL` (**1943-01→**), `REVOLSL`, `NONREVSL` | ✅ DDP | FRED | ❌ | Live: **$5.17tn total, $1.35tn revolving, $3.82tn non-revolving** at 2026-06 |
| Consumer credit interest rates | **Fed Board** (G.19) | ✅ `TERMCBAUTO48NS` (48m auto, 1972-02→), `TERMCBPER24NS` (personal), `TERMCBCCALLNS` (credit cards, 1994-11→), `RIFLPBCIANM60NM` (60m auto) | ✅ DDP | FRED | ❌ | Live: credit cards **20.94%**, 48m auto **7.47%**, personal **11.86%** at 2026-05. Note these lag the outstanding series by a month |
| Delinquency rates by loan type | **Fed Board** | ✅ `DRALACBN` (all loans, 1985-01→), `DRBLACBS` (business), `DRCLACBS` (consumer), `DRCCLACBS` (credit cards), `DRSFRMACBS` (single-family mortgages) | ✅ DDP | FRED | ❌ | The Inadimplência tab analogue. Live at 2026-Q1: all loans **1.49%**, credit cards **2.92%**, consumer **2.64%**, mortgages **1.89%**, business **1.34%**. **Quarterly, and lags ~2 quarters** (2026-01 was the latest when probed in August) |
| Charge-off rates | **Fed Board** | ✅ `CORCACBS` (consumer), `CORBLACBS` (business) | ✅ DDP | FRED | ❌ | Paired with the delinquency series above |
| Household debt service ratios | **Fed Board** | ✅ `TDSP` (total, 2005-01→), `CDSP` (consumer), `MDSP` (mortgage) | ✅ | FRED | ❌ | The `cred_credito_familias` analogue. **`FODSP` (financial obligations ratio) ends 2023-07** — dead |
| Sectoral debt levels | **Fed Board** (Z.1) | ✅ `TODNS` (domestic nonfinancial, 1945-10→), `BCNSDODNS` (nonfinancial corporate), `NCBDBIQ027S` (corporate debt securities), `CMDEBT` (households), `ASTMA` (all mortgages), `NCBCMDPMVCE` (corporate debt % of market value) | ✅ **z1_csv_files.zip, 8.08 MB** | FRED / zip | ❌ | Live at 2026-Q1: domestic nonfinancial debt **$81.86tn**, nonfinancial corporate **$14.45tn**, household **$21.07tn**. The zip is the path to the full ~10,000-series Z.1 |
| Household debt / GDP | **BIS** (via FRED) | ✅ `HDTGPDUSQ163N` (2005-01→2025-04), plus the BIS long credit series `QUSPAM770A`/`QUSHAM770A`/`QUSNAM770A` (**1947-10→**) | ✅ BIS API (already in `connectors/bis.py`) | FRED / SDMX | ❌ | We already have a working BIS connector for REER and policy rates — extending it to the credit-to-GDP dataset is cheap |
| Mortgage rates | **Freddie Mac** (PMMS) | ✅ `MORTGAGE30US` (weekly, 1971-04→), `MORTGAGE15US` | not probed | FRED | ❌ | **`MORTGAGE5US` (5/1 ARM) ends 2022-11** — discontinued |
| Household debt and credit report | **NY Fed** (Consumer Credit Panel) | ❌ not on FRED | ✅ xlsx confirmed (949 KB) | xlsx | ❌ | Balances *and* delinquency transitions by loan type and credit score, from a 5% credit-bureau panel. **Richer than anything on FRED** and the closest US thing to the BCB's saldo-de-maior-risco cut |
| Bank-level financials | **FDIC** | ❌ | ✅ **BankFind API**, no key | JSON | ❌ | Live: 4,352 institutions for `REPDTE:20260331`. Assets, net loans, non-performing. The analogue of the BCB's `cred_credito_controle_capital` cut, at far more granularity than we would need |
| Corporate credit spreads | **ICE BofA**, **Moody's** | ⚠️ `BAMLH0A0HYM2`, `BAMLC0A0CM` — **only from 2023-08**; `BAA10Y` (1986-01→), `AAA10Y` (1983-01→) | not probed | FRED | ❌ | See Gotchas — the licensing window makes the ICE series unusable for cycle work |
| **Nonperforming loans (call reports)** | FDIC | ⚠️ `NPTLTL` **ends 2020-07** | ✅ FDIC API | FRED / JSON | ❌ | The FRED series is dead; the FDIC API is the live path |
| **Mortgage debt outstanding** | Fed Board | ⚠️ `MDOAH` **DISCONTINUED, ends 2019-07** | ✅ Z.1 zip | FRED / zip | ❌ | Use `ASTMA` (all sectors, total mortgages, live to 2026-01) instead |
| **Leveraged loans / private credit** | — | ❌ | ❌ | — | ❌ | No free source identified. A real and growing blind spot in any US credit picture |

## Verified series inventory

45 credit candidates checked, **42 exist**. All 3 failures are my own guessed ids: `DRTSDCILM` and
`DRTSDCIS` (→ `DRSDCILM`, see Gotchas) and `QBPBSTLKTLNS`. No genuine coverage gap on FRED for the
concepts checked — the gaps in this branch are granularity (H.8 by bank size, the full SLOOS question
set) and history (the ICE BofA window), not existence.

By release: H.8 Assets and Liabilities of Commercial Banks (9 series), G.19 Consumer Credit (7),
Charge-Off and Delinquency Rates (7), SLOOS (6), Z.1 Financial Accounts (6), Household Debt Service
Ratios (3, one of them counted under housing), Primary Mortgage Market Survey (1 here, 2 more in
housing), Reports of Condition and Income (1, the dead `NPTLTL`).

Frequency mix: H.8 has both **weekly** (`TOTBKCR`, `TOTLL`, `TOTCI`, to 2026-08-05) and **monthly**
(`BUSLOANS`, `REALLN`, `CONSUMER`, to 2026-07) versions of overlapping concepts; G.19 is monthly to
2026-06 (rates to 2026-05); delinquencies, Z.1 and debt-service are quarterly to **2026-Q1**.

## Gotchas found live

- **Corporate spreads on FRED have a ~3-year rolling window.** `BAMLH0A0HYM2` and `BAMLC0A0CM` both
  start **2023-08** — an ICE BofA licensing restriction, measured not documented. A credit report
  whose central chart is a high-yield spread through the 2008 and 2020 stress episodes **cannot use
  them**. `BAA10Y`/`AAA10Y` (Moody's, 1983/1986→) are the long free substitute at coarser resolution.
  This is the same restriction that clips `SP500`/`DJIA` to 2016 and NAR home sales to 13 months.
- **Delinquency and charge-off data run two quarters behind.** Probed in mid-August 2026, the latest
  observation was **2026-Q1**. Any "current credit stress" reading is a quarter and a half old. The
  weekly H.8 balances and the NY Fed's quarterly panel are the more current signals.
- **H.8 publishes the same concept at two frequencies with different ids and different last dates.**
  `TOTCI` (weekly, to 2026-08-05) and `BUSLOANS` (monthly, to 2026-07) are both "Commercial and
  Industrial Loans, All Commercial Banks". Charting them together splices a weekly series onto a
  monthly one; picking the wrong one for a growth calculation changes the annualisation.
- **Three FRED credit series are dead and don't announce it in their titles**: `NPTLTL`
  (nonperforming loans) ends **2020-07**, `MDOAH` (mortgage debt outstanding) ends **2019-07**,
  `FODSP` (financial obligations ratio) ends **2023-07**. `MORTGAGE5US` (5/1 ARM) ends **2022-11**.
  Substitutes: FDIC API, `ASTMA`, and nothing respectively.
- **The SLOOS demand series is `DRSDCILM`, not `DRTSDCILM`.** The tightening series use `DRTS…` and
  the demand series use `DRS…` — a one-letter difference with no error if you guess wrong, just
  `"The series does not exist"`. Six SLOOS series verified; the release publishes far more (by firm
  size, by loan purpose, foreign banks) and those need the DDP catalog.
- **The Fed DDP fails silently without a series hash** — HTTP 200, zero-byte body. Confirmed here by
  scraping five hashes off `Choose.aspx?rel=H8` and getting real H.8 CSV back from one of them. Any
  DDP connector must check response length. (Same trap documented in the monetary-policy branch.)
- **The NY Fed Household Debt and Credit report is quarter-stamped in its filename**
  (`hhd_c_report_2026q1.xlsx` downloaded; `2026q2` did not exist yet at probe time). A connector must
  resolve the current quarter rather than hardcode it — the same pattern as
  `connectors/tesouro_efgg.py` resolving a changing anexo id, except here the variable part is
  predictable.

## Open items

- **Decide the primary path for the report: FRED aggregates or the DDP full releases.** FRED covers
  the headline of every H.8/G.19/SLOOS/delinquency concept, which is enough for a first tab set. The
  Brazil credit report's depth (84 resumo series, four modality tables, four structural cuts) has no
  FRED equivalent and would need the DDP plus the Z.1 zip.
- **Ingest the NY Fed Consumer Credit Panel** — it has no FRED path, downloads cleanly, and is the
  only source for delinquency *transitions* and credit-score cuts.
- **Extend `connectors/bis.py` to the credit-to-GDP dataset** — the connector already works for REER,
  policy rates and CPI, and the BIS long credit series reach 1947.
- **Decide whether FDIC bank-level data is in scope at all.** It is free and granular, but 4,352
  institutions per quarter is a different kind of dataset from everything else in this project.
- **Not inventoried this round**: the H.8 by bank size and foreign-related institutions, the full
  SLOOS question set, G.19 by holder, the Z.1 beyond 7 series, commercial real estate specifically,
  and auto/student loan detail.
