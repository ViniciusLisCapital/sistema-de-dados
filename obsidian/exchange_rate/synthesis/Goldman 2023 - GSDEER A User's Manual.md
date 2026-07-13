# GSDEER — A User's Manual

**Authors:** Sid Bhushan, Michael Cahill  
**Source:** Goldman Sachs Global Markets Analyst, 30 May 2023  
**Type:** Empirical research note — forecasting performance assessment  
**Tags:** #GSDEER #fair-value #PPP #forecasting #convergence #G10 #exchange-rate #goldman-sachs  
**Raw file:** [[gsdeer_manual_guide (Goldman, 2025)]]

---

## Summary

This paper empirically evaluates when and for which currencies GSDEER fair value estimates are actually useful for forecasting spot FX. The headline findings: (1) GSDEER takes ~3 years to outperform a random walk and ~5 years for spot to fully converge; (2) the model works best for AUD, EUR, CAD, NZD and is a "firm anchor" for GBP, JPY, CHF; (3) fair value has moved sharply since 2019 — commodity exporters (NOK, AUD) stronger, EUR and GBP weaker — but this doesn't translate to spot immediately.

The paper distinguishes two senses of "firm anchor": a currency that converges quickly, and a currency that doesn't diverge far. These can be different currencies.

---

## Context: Large GSDEER Swings Since 2019

Between 2019Q4 and 2023Q2, GSDEER fair value shifted materially:
- **NOK, AUD**: strengthened by >10% — driven by energy/commodity ToT surge
- **EUR, GBP**: weakened — inflation and productivity differentials vs US
- Inflation differentials were still limited at time of writing (common global shock), but scope for divergence as central banks faced different trade-offs

Key point: **large swings in fair value ≠ large swings in spot** — in the short run, macro and news dominate.

---

## Section 1 — When Does GSDEER Work? ("Take the Long Way Home")

### Forecasting horizon results (G10 mean)

| Horizon    | GSDEER performance                                                                 |
| ---------- | ---------------------------------------------------------------------------------- |
| < 3 years  | Underperforms or matches random walk                                               |
| ~3 years   | Begins to outperform random walk (RMSE crosses zero)                               |
| ~5 years   | Full convergence on average; substantially outperforms random walk and FX forwards |
| 5–8 years  | Improvement continues but at slower pace                                           |
| 8–10 years | Spot tends to **overshoot** fair value                                             |

**Convergence path:** Nearly linear at ~20%/year until full convergence at ~5 years. This is consistent with the academic literature finding a real exchange rate half-life of 3–5 years.

**Overshoot vs. moving target check:** When they test convergence to a *future* fair value (rather than the current level), the overshoot is slightly reduced but minimal — the overshoot is real, not just a moving-target artifact.

---

## Section 2 — Which Currencies? ("Choose the Right Vehicle")

### Performance by currency (5-year horizon)

**Group 1 — Best GSDEER forecasters** (high R², good RMSE improvement):
- AUD, EUR, CAD, NZD

**Group 2 — Firm anchors** (low divergence probability, even if not always fastest convergence):
- GBP, JPY, CHF

**Group 3 — Poor performance** (underperform random walk even at 5-year horizon):
- SEK, NOK, CHF (for CHF it's moderate; for SEK and NOK, systematically poor)

### Convergence speed ranking (quarters to reach 100%)

GBP is the fastest converger. AUD and CAD tend to overshoot (converge fast but then go past). NOK never fully converges in the 40-quarter (10-year) window.

### Two types of "firm anchor"

| Type | Example | Description |
|---|---|---|
| Fast convergence | GBP, AUD, NZD | Spot crosses fair value frequently — good for directional bets |
| Low divergence | GBP, JPY, CHF | Spot rarely gets far from fair value — good as a bound on mispricing |

GBP and JPY have the best of both: they converge and don't diverge. AUD converges fast but overshoots. CHF rarely diverges but when it does, divergence can be persistent.

**Probit model** for probability of further divergence given a 10% mispricing at 3-year horizon:
- Lowest probability of further divergence: **CHF, GBP, JPY** (~20%)
- Highest: **SEK, NOK** (~50%)

---

## Section 3 — Which Component Drives Fair Value? ("Pick the Best Driver")

GSDEER is essentially an augmented PPP model with three drivers: inflation differential, terms of trade, and productivity differential vs US. The paper evaluates each component separately.

### Inflation component

Works best for: **EUR, GBP, CAD** (in that order)

Why: These countries have the strongest trade linkages with the US, so the law of one price is most applicable and inflation differentials translate into exchange rate moves.

### Terms of Trade component

Works best for: **EUR, CAD, AUD, SEK**

Works poorly for: **NOK** — counterintuitive given Norway is a large oil exporter. Explanation: Norway's sovereign wealth fund (Government Pension Fund Global) invests all excess oil revenues internationally, effectively sterilizing the commodity windfall from the domestic economy and the currency.

### Productivity component

Less discussed in the paper — implied to matter mostly for JPY and CHF as the other two components are relatively flat for those currencies.

### Contribution to 2019–2023 fair value changes

The change in GSDEER fair value between 2019Q4 and 2023Q2 was driven primarily by:
- **NOK**: ToT (oil surge) — but ToT is a poor forecaster for NOK → discount this signal
- **AUD**: ToT (commodity surge) — ToT works well for AUD → take this signal seriously
- **EUR/GBP**: Inflation differential vs US → use with care (inflation component works for these)

---

## Section 4 — Investment Implications ("Navigate the Next Turns")

As of May 2023:

### AUD (GSDEER fair value: 0.94 AUD/USD)
**Signal: Take seriously.** Reasons:
1. AUD is a currency where GSDEER forecasts well
2. The current overvaluation of USD vs AUD is driven by the ToT component, which is a good forecaster for AUD
3. AUD is ~40% undervalued against USD on GSDEER
4. AUD tends to converge to fair value in ~4 years and then overshoot
5. Implication: over 20% AUD appreciation against USD over multi-year horizon

### EUR (GSDEER fair value: 1.21) and GBP (1.27)
**Signal: Don't expect too much.** Reasons:
1. EUR only ~10% undervalued after 2023 rally — already near fair value
2. GBP roughly already at fair value
3. GSDEER is a less strong anchor for EUR vs other currencies where it works well
4. Both already near 12-month spot forecasts

### NOK (GSDEER fair value: 5.55)
**Signal: Discount.** Reason: The stronger fair value is driven by the ToT component, which is a systematically poor forecaster for NOK due to the sovereign wealth fund mechanism.

---

## Methodology Appendix

**Out-of-sample evaluation** (avoids in-sample bias):
- Start date: 1986 (post-Plaza Accord) for all countries
- Rolling expanding window: at each quarter, only use data available up to that date to construct GSDEER and estimate forecasting regressions
- Evaluate against realized out-of-sample spot
- Metric: RMSE relative to random walk (positive = better than random walk), R-squared

**Why not in-sample?** In-sample would regress the latest GSDEER (2023) on all history — this gives GSDEER an unfair advantage because by construction the series have the same average value. Out-of-sample avoids this.

**Remaining caveat:** Both methods still have an advantage over true real-time forecasting because input data (productivity, inflation, ToT) are subject to revisions.

---

## Key Numbers to Remember

| Metric | Value |
|---|---|
| Years before GSDEER outperforms random walk | ~3 |
| Years for full convergence | ~5 |
| Annual convergence rate | ~20%/yr |
| Spot behavior beyond 5 years | Overshoot |
| Real exchange rate half-life (academic) | 3–5 years |
| Best-performing currencies (5yr) | AUD, EUR, CAD, NZD |
| Firmest anchors (low divergence) | GBP, JPY, CHF |
| Worst performers | SEK, NOK |

---

## Connections in the bibliography

- [[Goldman 2025 - GSDEER and GSFEER Models Primer]] — companion piece explaining the model construction and BRL case study (2025 vintage)
- [[Dornbusch 1976]] — provides the theoretical basis for why fair value is a long-run concept and short-run deviations are rational (overshooting)
- [[Mundell 1963]] / [[Fleming 1962]] — the policy effectiveness framework that underpins why exchange rates deviate from PPP in the short run
- [[Sarno-Taylor]] — academic treatment of PPP mean-reversion and the 3–5 year half-life that GS references
- [[verde_fx_mental_models]] — Verde letters treat GSDEER-type structural undervaluation as a necessary-but-not-sufficient condition for BRL appreciation; consistent with this paper's finding that convergence is slow and requires a catalyst
