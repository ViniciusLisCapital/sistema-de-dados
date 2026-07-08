# Exchange Rate — Consolidated Data Inventory

**Purpose:** a presentable map of the data series relevant to exchange-rate (BRL) analysis — what LIS should be tracking for this topic, full stop. Like `bibliography.md`, this file does **not** flag which series are already in the database vs. still to be built; that acquisition/build tracking remains the job of `agent_bibliography/agent_mapping/recommended_data/exchange_rate_data_inventory.md`, which stays the working pipeline-maintenance file. This is the presentation-layer cut of the same analytical ground, current as of 2026-07.

**Where this lives:** part of the same `agent_bibliography/consolidated/exchange_rate/` folder as `bibliography.md` (step i). Nothing in `agent_mapping/recommended_data/` was modified to produce this file.

**This is step (ii) of the three-part deliverable.** Step (iii) — integrating this data map with the concepts in `exchange_rate_conceptual_map.md` (which theory each series is evidence *for*) — has not been built yet, by design.

Eight analytical categories, ordered roughly the way an FX argument is actually built: the price itself, then the two fastest-moving determinants (carry — including its inflation-differential inputs — and terms of trade), then balance-of-payments flow and stock measures, then market positioning.

---

## 1. Spot price

| Series | Source | Frequency | Why it matters |
|---|---|---|---|
| USD/BRL PTAX (venda) | BCB SGS 1 (or SGS 10813, closing) | Daily, since 1984 | The dependent variable — every other category in this inventory exists to explain moves in this one series. |

## 2. Interest rate differential (carry)

| Series | Source | Frequency | Why it matters |
|---|---|---|---|
| Selic (nominal) | BCB SGS 432 | Daily/monthly, since 1996 | The domestic leg of every carry argument (Verde's §3.1/§3.2 mental models). |
| Fed Funds (nominal) | FRED (`FEDFUNDS`) | Monthly, since 1954 | The foreign leg. |
| Nominal ex-post differential | Selic − Fed Funds | Derived | Simplest carry signal. |
| IPCA (headline + cores) | BCB SGS | Monthly, since 1980 | The domestic inflation leg needed to turn the nominal Selic into a real rate — feeds the real ex-post differential row below. |
| US CPI | FRED | Monthly | The foreign inflation leg, symmetric to IPCA above. |
| Real ex-post differential | (Selic − IPCA 12m) vs. (Fed Funds − US CPI 12m) | Derived | The UIP-relevant comparison — strips out the pure inflation-differential effect from the real-rate signal. |
| Focus expectations (IPCA 12m/24m, IGP-M, Selic) | BCB Focus/Olinda | Weekly, since 2001 | The forward-looking domestic input the ex-ante differential below needs, and the raw material for any credibility/anchoring argument (Verde's §1.7). |
| Ex-ante differential | Focus Selic EOP 12m × Fed Funds futures/OIS-implied path; Focus IPCA 12m × US breakevens (TIPS 5y, `MICH`) | Derived, forward-looking | What markets are actually pricing, as opposed to the backward-looking ex-post version — the input UIP and the fair-value models in `bibliography.md` cluster 2 actually need. |
| Cupom cambial (implied dollar rate, DDI/FRC curve) | B3 | Daily | The BCB's own named gauge for the cost of onshore dollar liquidity — Brazil's local instance of the CIP-basis concept in the map, and Verde's tracked carry instrument (§3.4). |
| B3 DOL/WDO futures curve | B3 | Daily | Direct market-implied forward points, the instrument-level complement to the cupom cambial. |

## 3. Terms of trade / commodity prices

| Series | Source | Frequency | Why it matters |
|---|---|---|---|
| Terms of trade index (export/import price ratio) | BCB SGS 22099, 22100 | Monthly | The aggregate terms-of-trade signal behind every commodity-exporter currency argument (BEER's fundamental driver set, GSFEER's current-account channel). |
| Individual commodity prices in USD (iron ore, soybeans, Brent/WTI) | External (e.g. World Bank Pink Sheet, futures exchanges) | Daily/monthly | Decomposes which commodity is actually driving a terms-of-trade move — needed to distinguish a structural, volume-driven surplus from a cyclical, price-driven one (Verde's §2.1/§2.2 mental models). |

## 4. Balance of payments

| Series | Source | Frequency | Why it matters |
|---|---|---|---|
| Current account, trade balance + services, goods exports | BCB (BPM6) | Monthly, since 2001 | The flow-side counterpart to the trade-balance/capital-account identity at the base of the whole determination cluster. |
| Financial account, FDI (net, inflows), outward FDI | BCB (BPM6) | Monthly, since 2001 | FDI is the "safest" instrument in the capital-inflow riskiness ranking (Ostry et al. 2010) — tracking it separately from portfolio flows matters for reading crisis vulnerability. |
| Portfolio investment (total, equities, fixed income) | BCB (BPM6) | Monthly, since 2001 | The riskier, more reversible counterpart to FDI — the instrument split the capital-controls literature (bibliography.md cluster 7) is built around. |

## 5. FX flow

| Series | Source | Frequency | Why it matters |
|---|---|---|---|
| Registered FX flow — total/commercial/financial balance | BCB Nota Cambial | Weekly/monthly, since 2003 | The broadest registered-channel flow measure — the empirical counterpart to the flow-supply/demand channel in the current-account-adjustment framework. |
| Registered FX flow — CEP/CBE sub-items | BCB Nota Cambial | Weekly | Finer granularity on the financial-flow side than the aggregate above. |
| Contracted FX — bank-client settlements (daily totals: exports, imports, commercial/financial balance) | BCB Tables 13/14 | Daily, since Sep/2008 | The transactional, settlement-level view — conceptually distinct from registered flow, not a substitute for it. |
| Contracted FX — detailed monthly financial breakdown (services, income, domestic/foreign capital) | BCB Tables 13/14 | Monthly, since 1982/2011 | Longer history and finer categorization than the daily series. |

## 6. International reserves and BCB intervention

| Series | Source | Frequency | Why it matters |
|---|---|---|---|
| Total reserves and by component (FX securities, deposits, IMF, SDR, gold, other) | BCB | Monthly | The stock side of "how much ammunition the BCB has" — central to every fixed/managed-rate defense argument in `bibliography.md` cluster 3. |
| Reserves — total and liquidity concept | BCB | Daily | Higher-frequency read on the same stock. |
| Banks' net FX spot position | BCB SGS 21195 | Monthly | The banking-system mirror of the carry trade (`posicao_vendida_carry_incentive` in the conceptual map, sourced from the BCB technical note) — who's actually short/long FX onshore. |
| BCB FX swap — net position | BCB SGS 29533 | Monthly | The off-balance-sheet hedging instrument the BCB uses instead of spot intervention. |
| Stock of repo lines/loans/repurchase agreements in FX | BCB SGS 29534 | Monthly | Temporary-liquidity instrument, distinct from a permanent reserves change. |
| BCB interventions — spot, forwards, FX loans/repos, repo lines | BCB | Daily (sparse, intervention days only) | The flow side of "what the BCB is doing right now," distinguishable from the stock series above. |

## 7. Real effective exchange rate (REER)

| Series | Source | Frequency | Why it matters |
|---|---|---|---|
| Real (broad) and nominal (broad) REER — Brazil | BIS | Monthly, since 1994 | The core equilibrium-valuation benchmark underlying BEER/GSDEER-style arguments. |
| Same, for an EM comparison set (Mexico, Chile, Colombia; ideally also Turkey, South Africa, India) | BIS | Monthly | Lets BRL's REER move be read relative to peers rather than in isolation — the base's non-Brazil EM depth is otherwise thin (see `bibliography.md` cluster 3). |

## 8. Speculative positioning

| Series | Source | Frequency | Why it matters |
|---|---|---|---|
| CFTC positioning — open interest, leveraged-money net/long/short, non-reportables (BRL, MXN) | CFTC Traders in Financial Futures | Weekly, since 2010 | The standard futures-market positioning gauge behind Verde's §5.3 "positioning as contrarian signal" mental model. |
| Options-based positioning (risk reversal, skew) | Bank/exchange derivatives data | Daily/weekly | The volatility-market complement to futures positioning — ties directly to the FX-options literature gap flagged in `bibliography.md` cluster 1 (Garman-Kohlhagen, the options/risk-reversal primer). |

---

## Status

Data map (step ii of iii) complete: 8 analytical categories covering the full arc from the spot price itself through carry (now including its inflation-differential inputs), terms of trade, balance of payments, FX flow, reserves/intervention, REER, and positioning. Domestic activity backdrop was dropped as a category — it's general macro context, not FX-specific data. Next step (iii): integrate this map with `bibliography.md`'s clusters and `exchange_rate_conceptual_map.md`'s concepts — which theory each series actually serves as evidence for — not started yet.
