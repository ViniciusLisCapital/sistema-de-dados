# Paiva 2006 — External Adjustment and Equilibrium Exchange Rate in Brazil

**Type:** Empirical paper (BEER / cointegration model)
**Tags:** #beer #fair-value #real-exchange-rate #brazil #balassa-samuelson #terms-of-trade #net-foreign-assets #risk-premium
**Source:** Claudio Paiva, IMF Working Paper, 2006
**Language:** English
**Raw file:** [[equilibrium_exchange_brazil (Paiva, 2006)]]

---

## Context and motivation

Written to explain a striking fact: the BRL appreciated ~40% in real effective terms from January 2003 to December 2005 — its strongest level since the 1999 float — *at the same time* Brazil's current account swung from a 4¼%-of-GDP deficit (1998) to a 1¾%-of-GDP surplus (2005). The paper's question is whether this simultaneous appreciation-and-surplus combination was a disequilibrium (overshooting) or whether the BRL's stronger value was itself the *equilibrium* response to genuinely improved fundamentals. This is the direct methodological ancestor of the GSDEER-style fair-value models already in the vault ([[Goldman 2023 - GSDEER A User's Manual]], [[Goldman 2025 - GSDEER and GSFEER Models Primer]]) — same "augmented PPP" logic, applied to Brazil two decades earlier with a Behavioral Equilibrium Exchange Rate (BEER) framework.

## Core argument / thesis

Using a cointegration (Johansen VECM) approach across five fundamentals, most (roughly 23–31%, across four model specifications) of the observed 2003–05 REER appreciation (~25%) is explained as an equilibrium response to fundamentals — not a misalignment. By 2005 the BRL was "broadly in line with" its estimated equilibrium value. The dominant fundamental behind the appreciation was Brazil's improving net foreign asset (NFA) position (≈60% of the estimated BEER movement), followed by improved terms of trade (≈40%); the only fundamental pushing the *other* direction was a decline in Brazil's tradables-sector relative productivity (Balassa-Samuelson channel).

## Key mechanisms / model

- **BEER methodology**: econometrically estimate REER as a function of fundamentals via a cointegrating (long-run) relationship; "equilibrium" here is *statistical* (matches the model's prediction given actual fundamental values), explicitly distinguished from a "true" macro equilibrium requiring fundamentals themselves to be at sustainable levels (full employment, price stability, external sustainability) — the same distinction GSDEER draws between fitted "fair value" and a deeper structural equilibrium.
- **Five fundamentals, same functional form MacDonald and Clark (1998) used for US/Japan/Germany**: `REER = f(NTT⁺, TOT⁺, RINTDIFF⁺, NFA⁻, RELDEBT⁻)`:
  - **NTT** (nontradables/tradables relative price, CPI/PPI ratio vs. trading partners) — direct empirical proxy for the Balassa-Samuelson effect: faster tradables-sector productivity growth → relatively cheaper tradables → equilibrium appreciation. Same mechanism as [[ppp_balassa_samuelson]].
  - **TOT** (terms of trade, export/import price ratio vs. partners) — deteriorating terms of trade require depreciation to compensate the external accounts; same channel as GSDEER's terms-of-trade driver.
  - **RINTDIFF** (real interest rate differential vs. trade-weighted partner average) — direct UIP implication: higher domestic real rates → appreciation, same mechanism as [[uip]].
  - **NFA** (net foreign assets/GDP) — worse NFA (more foreign borrowing) requires a weaker currency to generate the primary current account surplus needed to service the higher external debt/profit remittances; captures trade competitiveness indirectly since ΔNFA ≈ current account absent valuation effects.
  - **RELDEBT** (domestic public debt/GDP relative to partners) — proxies the country risk premium: higher relative government indebtedness → riskier domestic assets → equilibrium depreciation for a given real rate differential. Direct empirical analogue of [[risk_premium]]'s `ρ(B−A)` and the [[balance_of_payments_approach]]'s portfolio-balance channel.
- **Data and estimation**: annual data 1970–2004; all series I(1) (nonstationary in levels, stationary in first differences, confirmed by ADF tests); Johansen cointegration/VECM, four model specifications differing in whether RINTDIFF is treated as endogenous (in the cointegrating vector) or exogenous (short-run only, given ADF ambiguity on its stationarity), and in how heterodox-stabilization-plan disruptions (1986–94 hyperinflation-fighting plans) are controlled for (dummy vs. continuous intra-year inflation variance).
- **Decomposition of the 2003–05 appreciation**: NFA improvement (~15 percentage points of GDP) contributes ~60% of the estimated BEER appreciation; terms-of-trade improvement contributes ~40%; the NTT/Balassa-Samuelson variable is the *only* fundamental pushing toward depreciation, reflecting Brazil's relative tradables-productivity decline vs. partners over the period.

## Main results / findings

- All four model specifications estimate equilibrium appreciation (23–31%) close to the actual REER appreciation (~25%) over 2003–05 — the central conclusion that this was "an equilibrium phenomenon," not overshooting, is robust across specifications.
- The broader external-adjustment narrative (Section II): export growth (not import compression) drove the current account reversal; Brazil's EMBI spread collapsed from ~2,700bp (Jan 2002) to ~300bp (May 2006) alongside declining public/external debt ratios and the elimination of dollar-indexed domestic public debt — a country-risk-premium collapse that is the exact historical mirror image of the deterioration analyzed decades later in [[Itaú 2025 - Fiscal Dominance in Brazil]].
- BCB was already actively intervening to slow the appreciation by 2005–06 (large FX purchases to build reserves) — an early instance of the reserve-accumulation intervention behavior discussed generically in [[Krugman 2023 - Fixed Exchange Rates and Foreign Exchange Intervention]].

## Limitations and caveats

- **This extraction is incomplete** — the raw text cuts off mid-sentence discussing the "relatively small contribution from" (likely RELDEBT or RINTDIFF) to the estimated BEER movement, before the paper's concluding remarks section. Do not treat the decomposition (NFA ~60%, TOT ~40%, NTT negative) as necessarily the paper's final full account — the missing text may add nuance.
- Annual data over 1970–2004 spans multiple structural regimes (hyperinflation, heterodox stabilization plans, capital account liberalization, the 1999 currency crisis) — the paper's own robustness checks (dummy vs. continuous inflation-variance control) reflect awareness that a single stable cointegrating relationship across this entire period is a strong assumption.
- BEER "equilibrium" is explicitly statistical, not structural — the paper itself flags that if a fundamental (e.g., NFA) is itself away from a sustainable level, a REER matching current fundamentals is not necessarily "equilibrium" in the deeper macroeconomic sense.

## Connections

- [[ppp_balassa_samuelson]] — the NTT variable is a direct empirical Balassa-Samuelson proxy; BEER is the direct methodological ancestor of GSDEER's "augmented PPP" approach
- [[Goldman 2023 - GSDEER A User's Manual]] / [[Goldman 2025 - GSDEER and GSFEER Models Primer]] — same fundamentals-based fair-value logic (terms of trade, productivity/Balassa-Samuelson, real rate differentials) applied to Brazil specifically, two decades before GSDEER's own Brazil coverage
- [[uip]] — RINTDIFF is this model's direct UIP channel; treating it as endogenous vs. exogenous across specifications mirrors the vault's own UIP-fails-empirically discussion
- [[risk_premium]] / [[balance_of_payments_approach]] — RELDEBT is a country-risk-premium proxy nearly identical in spirit to Krugman's `ρ(B−A)`; the EMBI collapse (2,700bp→300bp, 2002–06) is the historical mirror image of the fiscal-deterioration case in [[Itaú 2025 - Fiscal Dominance in Brazil]]
- [[Krugman 2023 - Fixed Exchange Rates and Foreign Exchange Intervention]] — BCB's 2005–06 FX purchases to slow appreciation and build reserves are a real-world instance of that chapter's intervention mechanics
- [[Cortapasso 2023 - Padrões da Transmissão Cambial para a Taxa de Inflação no Brasil]] — this paper's 2003–05 appreciation episode is exactly the period Cortapasso (2023) identifies as driven by interest-arbitrage/falling risk premium, now given a formal fundamentals-based decomposition
