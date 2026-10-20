---
aliases: ["Holston 2017 - Measuring the Natural Rate of Interest: International Trends and Determinants"]
---

# Measuring the Natural Rate of Interest: International Trends and Determinants — Holston, Laubach & Williams 2017

**Type:** paper (working paper)
**Tags:** #natural-rate #r-star #trend-growth #kalman-filter #global-factors #zero-lower-bound
**Source:** Federal Reserve Bank of San Francisco Working Paper Series, Working Paper 2016-11 (December 2016)
**Language:** English
**Source file:** [[monetary_policy/clean_md/natural_rate_international (Holston, Laubach & Williams, 2017)]]

---

## Context and motivation

The natural rate of interest is the benchmark for the stance of monetary policy (policy is expansionary when the real rate is below it) and the intercept of rules such as Taylor's, but it is latent and must be inferred. US estimates with the Laubach–Williams (2003) model had fallen to close to zero during the global financial crisis and stayed there into 2016, prompting the question whether the decline is permanent and why (demographics, slower productivity, global saving). The paper asks whether the same happened elsewhere and whether the national declines move together — a test of whether the causes are domestic or global.

## Core argument / thesis

- The natural rate, defined in Wicksell's sense as the real short rate consistent with output at its natural rate and constant inflation, is a **low-frequency** object that can shift permanently, not a stationary combination of transitory shocks as in DSGE models.
- Applied country by country, the Laubach–Williams method finds large declines in trend growth and in the natural rate over the past 25 years in the United States, Canada, the Euro Area and the United Kingdom, to historically low levels with no sign of a rebound.
- Although nothing links the countries in estimation, the estimates **co-move**, so the decline stems "in large part from developments common to many countries, rather than idiosyncratic national factors".
- A persistently low natural rate makes episodes at the effective lower bound more frequent and longer, everywhere.

## Key mechanisms / model

**Theory.** In the neoclassical growth model the steady-state real rate equals trend consumption growth scaled by the inverse of the intertemporal elasticity of substitution, plus the rate of time preference (equation 1). So shifts in trend growth or in preferences/saving move the natural rate. The open-economy New Keynesian model (equations 2–3) adds that the natural rate depends on expected world as well as domestic output growth.

**Empirical model (equations 4–9).** Two reduced-form equations: an IS curve in which the output gap depends on its own lags and on the lagged gap between the real rate and r*; and a Phillips curve in which inflation depends on its lags and the lagged output gap. The natural rate is written as trend growth plus a residual component z (other determinants: saving, fiscal policy, global factors), with a one-for-one link to trend growth imposed (estimated near unity in Laubach–Williams 2003, but poorly identified). Potential output follows a random walk with a drift that is itself a random walk (I(2)); z is a random walk. Transitory shocks to the gap and inflation are kept out of r*, so r* is the rule intercept, not the period-by-period DSGE natural rate.

**Estimation.** Kalman filter on real GDP, core inflation and the short rate (ex ante real rate built with a four-quarter average of past inflation). To avoid the "pile-up problem" (maximum likelihood pushing the variance of small persistent shocks to zero), the signal-to-noise ratios for trend growth and z are fixed with Stock–Watson median-unbiased estimators in sequential steps, then the rest is estimated by maximum likelihood, with the IS slope constrained negative and the Phillips slope positive.

What carries the result: r* is identified only through the IS slope (the real rate gap's effect on the output gap) and the Phillips slope (the output gap's effect on inflation). When either is close to zero, r* is barely identified — the source of the wide bands for the Euro Area and the UK. The one-for-one link to trend growth decides how much of the decline is attributed to g rather than z.

**Cross-country analysis.** Since the estimates are nonstationary, comovement is described with vector error-correction models (one or three cointegrating vectors) and variance decompositions, explicitly as description rather than inference, because the series are generated regressors.

## Main results / findings

- **Decline everywhere, in two phases.** A moderate fall over 1990–2007 and a larger one since 2007 (Table 3, Figures 1–4): in 1990 the estimates range "between about 2-1/2 and 3-1/2", in 2007 "roughly 2 to 2-1/2 percent", and in 2016 they are at historical lows — slightly negative for the Euro Area. Market and survey measures of real rates (inflation-linked bond yields five to ten years ahead) fall in the same direction.
- **Trend growth is the main, not the only, driver.** Trend growth fell in all four economies, accelerating at the end, "by a percentage point on average over 2007–2016" (Table 2). In Canada, the US and the UK most of the 2007–2016 fall in r* is lower trend growth; in the Euro Area trend growth explains less than half, so other persistent factors (z) dominate. Over 1990–2007 the decline in Canada and the Euro Area is fully accounted for by trend growth, while in the US and UK z also contributed.
- **Output gaps after the crisis are smaller than other estimates**, because core inflation fell only modestly — in the model a large negative gap would have pulled inflation down more.
- **Comovement.** A single cointegrating vector links the four natural rates; shocks to the US natural rate account for about 35 percent of Canada's natural-rate variance at a ten-year horizon, and the US is the least dependent (around 20 percent from other economies) (Figure 5). Results are robust to imposing three cointegrating vectors; trend growth rates co-move similarly.
- **Imprecision.** Even smoothed, the US r* has a sample-average standard error of 1.1 percentage points (Table 1); one-sided ("real-time"-like) estimates are less precise, and the other three economies less precise still.
- **Robustness.** Other methods (time-varying-parameter VARs, macro-finance models, DSGE medium-run forecasts) also find large declines; estimates for Canada and the UK sit within other studies' ranges.

**What would contradict it.** A rebound in natural-rate estimates with no change in trend growth; or national estimates that move independently, which would point to domestic rather than global causes.

## Limitations and caveats

- Authors' own: estimates are "highly imprecise", especially for the Euro Area and the UK, where the IS slope is close to zero; the UK estimates differ markedly (little persistence in the gap, a very steep Phillips slope, a near-zero IS slope). The one-for-one link between r* and trend growth is imposed, not estimated. The VECM analysis rests on generated regressors and should not be read for specific numbers or significance; a single cointegrating vector allows divergences that are "somewhat puzzling" under high capital mobility. Global and local factors are not modeled jointly — left to future work.
- From the text: the definition is a medium-run concept (the intercept of a simple rule) that differs from the DSGE period-by-period natural rate, so comparisons across concepts need care. The ex ante real rate uses backward-looking inflation expectations (a four-quarter average), a departure from LW (2003) forced by Euro Area data. Market-based real yields embed risk and liquidity premia.
- **Damaged or missing passages.** The text, equations and tables are readable (tables extracted cell by cell). Figures 1–11 survive as axis ticks and legends only. The reference list is not in the file (the page numbering jumps from 17 to 23).

## Connections

- [[natural_rate_of_interest]] — the paper's subject: a low-frequency, possibly permanent r* tied to trend growth and other persistent factors, estimated for four economies and shown to have fallen together
- [[zero_lower_bound]] — a lower average natural rate implies more frequent and longer episodes at the effective lower bound, and stronger international spillovers there
- [[monetary_policy/synthesis/natural_rate_measurement (Laubach & Williams, 2003)]] — the model this paper extends to Canada, the Euro Area and the UK; an appendix compares the two US estimates and their parameters
