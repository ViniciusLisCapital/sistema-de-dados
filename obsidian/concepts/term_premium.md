# Term Premium

**Type:** Bond risk premium / yield-curve decomposition
**Tags:** #term-premium #yield-curve #affine-term-structure #bond-risk-premia #expectations

---

## Definition

The part of a long-term bond yield that is not the expected average of future short-term rates over the bond's life: compensation for bearing interest-rate risk. In an affine term structure model, Adrian, Crump & Moench obtain the risk-neutral yield by setting the prices of risk to zero in the bond-pricing recursions — it equals the expected average future short rate — and define the term premium as the difference between the model-implied fitted yield and the risk-neutral yield.

## Mechanism

- **Where it comes from**: one-period excess returns on bonds are the exposures of each bond to the pricing factors' shocks times the market prices of those risks, plus a convexity term. Accumulated over maturities through the recursions, time-varying prices of risk make the term premium time-varying (Adrian, Crump & Moench, equations 12, 25–26).
- **Which risk is priced**: in Adrian, Crump & Moench's five-factor model practically all time variation in risk premia is a price of **level** risk; slope risk is not priced. The variation is driven by factors that barely move yields but predict returns — the slope and the fifth principal component, or the Cochrane–Piazzesi return-forecasting factor in a four-factor model.
- **Why it matters for reading rates**: separating expected short rates from the term premium turns a move in long yields into a statement about expected policy versus compensation for risk; Adrian, Crump & Moench present the decomposition as useful for real-time analysis at daily frequency.

## When it applies / when it fails

- The estimate is model-dependent: it requires a specification of the pricing factors and of the dynamics of the prices of risk. Adrian, Crump & Moench find that five-factor and unrestricted four-factor models give similar term premia in sample, but differ out of sample — the four-factor model implies long-maturity yields far below realized ones when estimated on maturities up to ten years.
- Factors the yield curve does not span (real activity, inflation) can carry information about the prices of risk; adding an unspanned real activity factor makes slope risk priced (Adrian, Crump & Moench).
- Weakly spanned higher-order components make some prices of risk weakly identified; Adrian, Crump & Moench report that treating them as unspanned leaves the term premium very similar.
- As a check that the estimate measures risk, Adrian, Crump & Moench's daily ten-year term premium is strongly correlated with the MOVE index of Treasury option-implied volatility, though no option data enter the model.

## How it appears across sources

| Source | Role |
|---|---|
| [[monetary_policy/synthesis/term_structure_linear_regressions (Adrian, Crump & Moench, 2013)]] | Defines and estimates it with a three-step regression approach: term premium = fitted yield minus risk-neutral yield; five principal components as pricing factors, level risk carrying almost all its time variation; daily estimates since August 2009 correlated with the MOVE index |
| [[monetary_policy/synthesis/zero_bound_alternatives (Bernanke, Reinhart & Sack, 2004)]] | Observable-factor affine model of US and Japanese yields used as a benchmark: risk-neutral yields obtained by setting prices of risk to zero; residual deviations attributed to statements, relative supplies and quantitative easing; the zero bound itself steepens the curve |
| [[monetary_policy/synthesis/it_and_debt_brazil (Favero & Giavazzi, 2004)]] | Emerging-market version: Brazilian swap yields minus the Selic path implied by an estimated rule, assuming no expectational errors; the premium contains policy-rate volatility and credit risk, and its correlation with the EMBI rises with maturity (Table 4, 1999:2-2003:1) |
| [[fiscal_policy/synthesis/determinantes_premio_risco_taxas_nominais (BCB, 2025)]] | Determinants of the ACM 5-year premium on Brazilian nominal bonds, Jan/2007–Apr/2025: positively associated with Selic, TLP, Focus expectations, gross debt/GDP (sign unstable across specifications), the US real rate and curve slope, the dollar and the VIX; domestic rates dominate the time decomposition, US rates the per-standard-deviation effects |
| [[external/synthesis/us_mp_spillovers_bond_markets (Albagli et al., 2018)]] | US FOMC shocks (2-year Treasury, two-day window) decomposed into foreign risk-neutral and term-premium responses with ACM for 12 developed and 12 emerging markets, 2003–2016: the TP carries most of the 10-year spillover in emerging markets (0.239 of 0.293, Table 2) and almost none in developed ones |

## BRL / application to the current analysis

Two linked sources are about Brazil's nominal curve, and they read the premium differently. [[monetary_policy/synthesis/it_and_debt_brazil (Favero & Giavazzi, 2004)]] measure it on swaps as the yield minus the Selic path implied by an estimated BCB rule, assuming no expectational errors; in Brazil it prices default risk as well as policy-rate volatility, and its correlation with the EMBI rises with maturity (Table 4, 1999:2-2003:1). In an economy with a fiscal question, then, a rise in the premium can be a credit signal and not only compensation for duration. [[fiscal_policy/synthesis/determinantes_premio_risco_taxas_nominais (BCB, 2025)]] applies ACM to the LTN and NTN-F curve, Jan/2007–Apr/2025: almost all the volatility of the 5-year rate comes from the premium rather than from the expected Selic path. The premium moves with domestic rates (Selic, TLP), Focus inflation expectations, gross debt/GDP (with a sign that changes across specifications) and US rates, the dollar and the VIX; domestic rates dominate its decomposition over time, while per standard deviation the US real rate and slope move it most. These are reduced-form associations with lagged regressors, not causal effects.

The other sources say nothing direct about Brazil: Adrian, Crump & Moench estimate the US Treasury curve, 1987:01 – 2011:12, and Bernanke, Reinhart & Sack the US and Japanese curves; Albagli et al. find that emerging-market long yields absorb US policy shocks mostly through term premia, but Brazil is not in their sample.

## Connections

- [[risk_premium]] — the currency analogue: an expected excess return beyond what the expected path of the price (there, the exchange rate) requires
- [[monetary_policy/synthesis/term_structure_linear_regressions (Adrian, Crump & Moench, 2013)]] — the regression-based affine model behind the decomposition
- [[monetary_policy/synthesis/zero_bound_alternatives (Bernanke, Reinhart & Sack, 2004)]] — a macro-finance no-arbitrage model used to gauge whether nonstandard policies moved yields beyond what the economy and policy stance explain
- [[monetary_policy/synthesis/it_and_debt_brazil (Favero & Giavazzi, 2004)]] — term premia where default risk, not only interest-rate risk, is priced at short maturities
- [[fiscal_policy/synthesis/determinantes_premio_risco_taxas_nominais (BCB, 2025)]] — what moves the Brazilian nominal term premium: domestic rates, inflation expectations, public debt and US rates
- [[external/synthesis/us_mp_spillovers_bond_markets (Albagli et al., 2018)]] — US policy spillovers to foreign long yields run through term premia in emerging markets, where FX intervention amplifies bond inflows
