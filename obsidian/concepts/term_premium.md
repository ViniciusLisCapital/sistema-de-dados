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

## BRL / application to the current analysis

The linked source says nothing about Brazil: it estimates the US Treasury curve, 1987:01 – 2011:12.

## Connections

- [[risk_premium]] — the currency analogue: an expected excess return beyond what the expected path of the price (there, the exchange rate) requires
- [[monetary_policy/synthesis/term_structure_linear_regressions (Adrian, Crump & Moench, 2013)]] — the regression-based affine model behind the decomposition
- [[monetary_policy/synthesis/zero_bound_alternatives (Bernanke, Reinhart & Sack, 2004)]] — a macro-finance no-arbitrage model used to gauge whether nonstandard policies moved yields beyond what the economy and policy stance explain
- [[monetary_policy/synthesis/it_and_debt_brazil (Favero & Giavazzi, 2004)]] — term premia where default risk, not only interest-rate risk, is priced at short maturities
