# FX Carry Trade

**Type:** Investment strategy  
**Tags:** #carry-trade #uip #interest-differential #brl #risk-premium #emerging-markets

---

## Definition

Borrow in a low-yield currency, invest in a high-yield currency, pocket the interest differential without hedging the exchange rate exposure.

**Strategy:** Short funding currency (low `r*`) → Long target currency (high `r`) → collect `r − r*`

Profitable as long as the target currency does not depreciate by more than the interest differential. **The carry trade is a bet on the empirical failure of UIP** — if UIP held exactly, expected returns would be zero.

---

## Stylized facts

1. **Carry trades are profitable on average** — high-yield currencies depreciate less than UIP predicts (forward premium puzzle).
2. **Carry trades crash** — they unwind violently in risk-off episodes. The return distribution is left-skewed: small regular gains, rare large losses.
3. **The crash risk is the risk premium**: average carry premium = compensation for bearing global risk-off exposure.

---

## When carry fails

| Condition                      | Mechanism                                                                     |
| ------------------------------ | ----------------------------------------------------------------------------- |
| Global risk-off (VIX spike)    | Simultaneous carry unwind across all EM → target currencies collapse          |
| Fiscal/sovereign deterioration | Risk premium `ρ` rises → `r − r*` is eaten by higher `ρ`, not by carry        |
| Central bank credibility loss  | Expected future depreciation rises, reducing effective carry                  |
| Structural USD appreciation    | Safe-haven flows → USD strengthens against all EM regardless of differentials |
| **Monetary tightening in the *funding* currency** | Forces deleveraging (short-covering) of the funding-currency leg, causing sharp funding-currency appreciation — see below |

### Monetary policy tightening in the funding currency (BIS 2026)

The carry trade's crash risk isn't only about the *target*-currency side — it also depends on monetary policy shocks hitting the *funding* currency. When speculators are heavily net short a funding currency (CHF and JPY are the canonical cases), a monetary tightening surprise there forces short-covering: net CHF short futures positions have been found to shrink by over 60% of total open interest following a contractionary shock, causing an outsized appreciation (~4% for CHF, ~10% for JPY per 25bp surprise) *relative to* the same shock hitting a currency with little prior carry positioning (statistically insignificant FX response in that case). This state-dependence — same-size policy shock, wildly different FX outcome depending on prior positioning — is measurable in real time via net non-commercial futures positioning (CME) and the carry-to-risk ratio (interest differential ÷ implied vol). See [[BIS 2026 - Monetary Policy Transmission to Exchange Rates via Carry Trades]].

---

## BRL as a carry currency

BRL has one of the highest nominal rates globally (Selic) — it is a natural carry target. But BRL carry is structurally impaired by:

1. **High risk premium** (fiscal uncertainty, institutional risk): effective carry = `r_BRL − r_US − ρ_BRL`
2. **Carry vs. risk premium trade-off**: Verde observed in May 2024 that BRL weakened even as Brazilian real rates rose to their highest level since the tightening cycle began — risk premium dominated carry
3. **High-beta EM in unwinds**: when risk-off hits, BRL amplifies the move

**Verde's rule:** carry "can be overridden by dynamics sufficiently adverse." The Verde book is rarely long BRL on carry alone — there is always a macro view behind the position.

---

## Verde's multi-leg carry book

Verde constructs carry as a spread trade: long high-carry EM (BRL, MXN, INR) funded by short low-yield / structurally weak currencies (EUR, CHF, CNY). This:
- Reduces USD directionality
- Diversifies idiosyncratic EM risk
- Keeps the funding leg earning negative carry (adds to total return)

The composition rotates as relative fundamentals shift (e.g., MXN was zeroed after the 2024 Mexican election).

---

## Connections

- [[uip]] — carry trade is the empirical violation of UIP; the risk premium is the theoretical explanation for why it works on average
- [[risk_premium]] — risk premium is the carry trade's dual concept: carry premium = risk premium for bearing the downside
- [[verde_fx_mental_models]] — carry is model 3.1 (Carry as BRL Support), with caveats in 3.2–3.4; multi-leg carry book in 9.1
- [[kinea_fx_mental_models]] — cluster 2 (carry and rate-differential support for BRL, 2.1–2.6); cluster 5 (RMB as a structural funding currency)
- [[kapitalo_fx_mental_models]] — 9.1–9.2: pro-cyclical commodity/carry currency baskets and an EM carry basket (high-carry/normalization currencies) funded against low-carry currencies (CNY, CHF), a structural portfolio pattern maintained for years
- [[Goldman 2025 - GSDEER and GSFEER Models Primer]] — BRL GSDEER undervaluation doesn't trigger convergence because carry positioning (not structural value) drives short-run BRL
- [[Dornbusch 1976 - Expectations and Exchange Rate Dynamics]] — carry differentials (`r − r*`) are the short-run mechanism; the Dornbusch path describes how they unwind
- [[overshooting]] — after a rate hike, the currency overshoots appreciation; the carry window is the gradual reversal phase
- [[fiscal_dominance]] — the regime in which carry is structurally disabled; effective carry `(r − r*) − ρ` inverts at peak nominal rates
- [[Itaú 2025 - Fiscal Dominance in Brazil]] — Brazil 2025 near-fiscal-dominance case: Selic at cycle high, BRL depreciating — empirical instance of carry overwhelmed by fiscal risk premium
- [[Krugman 2023 - Exchange Rates and the Foreign Exchange Market (An Asset Approach)]] — AUD/JPY 2000s case study: textbook-level illustration of carry profitability and the 2008 crash, framed as a peso-problem (small-probability large-crash) rather than a UIP failure in expectation
- [[Krugman 2023 - Fixed Exchange Rates and Foreign Exchange Intervention]] — Polish zloty/Swiss franc mortgage carry trade: when the SNB abandoned its EUR floor in Jan. 2015, CHF borrowers (funding currency) were hit exactly like a funding-currency appreciation shock in any carry unwind
- [[CFA L2 2025 - Currency Exchange Rates Understanding Equilibrium Value]] — Turkish lira 2002–2010: ~1,000bp TRY-USD spread stayed profitable via the yield channel alone even though FX intervention suppressed the spot-appreciation leg
- [[BIS 2026 - Monetary Policy Transmission to Exchange Rates via Carry Trades]] — quantifies exactly when/how much a monetary tightening shock in a funding currency (CHF, JPY) amplifies FX response via forced deleveraging, using CFTC-style futures positioning as a real-time carry-crowding gauge
