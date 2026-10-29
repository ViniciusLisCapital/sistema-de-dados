---
aliases: ["da Gama Machado 2024 - Core Inflation in Brazil: past and present"]
---

# Core Inflation in Brazil: past and present — Vicente da Gama Machado 2024

**Type:** paper (BCB Working Paper; literature survey plus an evaluation)
**Tags:** #core-inflation #trimmed-mean #exclusion-measures #inflation-forecasting #ipca #brazil
**Source:** Banco Central do Brasil, Working Paper Series no. 602, October 2024 (Outubro 2024), p. 3-34
**Language:** English
**Source file:** [[inflation/clean_md/core_inflation_brazil_past_present (da Gama Machado, 2024)]]

---

## Context and motivation

Core measures gained prominence after the Covid shock, when headline inflation and relative prices both moved sharply. Brazil had a large literature on core inflation but no survey of it. The paper does two things: a chronological guide to the measures the BCB has used and a survey of the Brazilian academic literature (13 papers, 8 theses or dissertations, 8 BCB working papers; Table A1, printed as "Table 3" in the appendix); and a unified evaluation of the BCB's current five "official" measures and their average, rerun on a sample that includes the post-pandemic inflation. The set had been redefined in 2020 on pre-pandemic information, so the question is whether it held up.

## Core argument / thesis

No single core measure is best: each method filters a different kind of noise, and each fails in a different episode. The sensible practice, which the BCB follows, is to monitor a set of complementary measures and their simple average. Statistical measures (trimmed means, double weighting, percentiles) are better on bias, variance, trend-tracking and forecasting; exclusion measures are easier to communicate and more sensitive to the cycle. Core measures are useful as a description of underlying inflation but generally poor as predictors of headline inflation, and the post-pandemic episode made that worse.

## Key mechanisms / model

**The BCB's measures and what each filters (Section 2, Table 1).**
- *Trimmed means (MA, MS).* Each month items are ranked by price change and those below the 20th and above the 80th percentile of accumulated weight are dropped; the rest is reweighted. MS first smooths items that change price infrequently (about once a year), since otherwise their one big monthly jump would be trimmed or would bias the measure. The 20% cut was chosen by minimizing the RMSE against a 13-month centered moving average. MA (no smoothing) was dropped in 2020 for bias.
- *Exclusion (Ex-0 to Ex-3).* Ex-0 drops food-at-home and administered prices entirely. Later versions drop only the most volatile items within those groups, because many administered prices are persistent and excluding them all would bias the core downward. Ex-3 drops food-at-home and keeps the underlying components of services and industrial goods; the "underlying services" component it defines gained market attention for its persistence and cyclical sensitivity, though it is not a core measure. Ex-FE (ex-food and energy) is followed but not official: it leaves in volatile yet persistent energy prices with a large IPCA weight.
- *Double weighting (DP).* Expenditure weights are adjusted by each item's relative volatility, downweighting volatile items without excluding them.
- *P55.* The 55th percentile of the weighted cross-section of item changes, a median-type measure moved above the median because the cross-sectional distribution of price changes is historically right-skewed; the higher percentile minimizes bias.
- Since BCB (2020) the official set is Ex-0, Ex-3, MS, DP and P55, cut from seven for parsimony and redundancy.

**Evaluation criteria (Section 3.1).** Unbiasedness against headline; lower variability; tracking a trend proxy (centered moving averages of headline); acting as an *attractor* of headline — Cogley's equation regresses future headline change on the gap between core and headline, and a slope near 1 means headline converges to core; or core Granger-causes headline and not the reverse; forecasting ability. Less often: correlation with money, and sensitivity to slack.

**The unified evaluation (Section 4).** Monthly data from January 2004 to May 2023, seasonally adjusted annualized 3-month averages. Six criteria: bias, variance, trend-tracking (RMSE against 13- and 25-month centered averages), sensitivity to the cycle (a quarterly Phillips curve with lagged IPCA, Focus expectations, commodity prices in reais and the BCB output gap; equation 2), forecasting of 12-month-ahead IPCA (seven specifications, out of sample from January 2010; Appendix), and ease of communication (a subjective grade). Measures are ranked from 1 to 6 on each criterion (Table 7).

## Main results / findings

- **All core measures pass bias and variance**: their averages are statistically close to the IPCA's and their variability lower (Tables 3 and A3). All track trend inflation better than the IPCA itself, with P55 and DP best (Table 4).
- **Cyclical sensitivity runs the other way**: the output gap is insignificant for the IPCA (coefficient 0.06, p-value 0.67, Table 5) but significant for most cores, largest for the exclusion measures (Ex-3 0.44). MS is the exception, with an insignificant gap coefficient. Excluding the Covid period leaves this pattern unchanged (Table A4).
- **Forecasting is weak.** In most of the seven specifications the cores do not beat the IPCA's own RMSE (Table 6). In Diebold-Mariano tests only a few cases beat headline at 5%: P55 in the naive comparison and in the Cogley-equation model, DP and the core average in the naive comparison (Table A5). This matches most of the literature (Section 3.2) and contrasts with the earlier BCB evaluations using similar methods, which the author attributes to the post-pandemic episode.
- **Overall ranking**: the core average has the highest average grade across the six equally weighted criteria (4.3), followed by P55 (4.1) and DP (3.8) (Table 7). Statistical measures win on bias, variance, trend and forecasting; exclusion measures win on cycle and communication — the complementarity that justifies a set.
- **What the pandemic changed**: inflation peaked before the cores because the shock moved relative prices unusually (food first, then energy and goods amplified by fiscal expansion, supply chains and the war in Ukraine, then services on reopening). MS gained bias and lost trend-tracking because it trims away large moves; DP improved because it does not fully filter large moves in normally stable items.
- **From the survey**: trim studies generally find an optimal symmetric trim around 20%; several papers propose asymmetric trims for the right-skewed distribution; alternative methods (wavelets, dynamic factors, SVAR with activity variables, persistence weights, combined filters) often report better results than the official measures; combinations give mixed results; there is no consensus on a preferred measure.

## Limitations and caveats

- The author's own caveats: the output-gap coefficients depend on the gap specification, and Covid may have changed the relationships structurally; the evaluation sample is short and the post-pandemic shock large, which weighs on the forecasting results; the 1-to-6 grades are qualitative and their numeric differences are not meant as performance gaps; the communication grade is subjective; equal weighting of criteria is a simplification.
- A core measure that ranks well on one criterion can fail another, and the rankings shifted between the pre- and post-pandemic samples: the result is about this sample, not a property of the measures.
- The survey part reports the findings of other papers in one or two lines each (Table A1); the note does not and cannot verify them.
- Damaged passages: equations (1) to (7) — Cogley's equation, the Phillips curve of equation (2) and the forecasting models in the Appendix — are garbled, with symbols scattered across lines; Figures 1, 2 and 3 (the measures over time and the visual classification) and Figure A1 (Google Trends) are not in the file; the appendix survey table is labelled "Table 3" though the text calls it Table A1; the pages between the conclusion and the appendix (presumably the reference list) are missing.

## Connections

- [[core_inflation]] — the whole subject: the BCB's exclusion, trimmed-mean, double-weighting and percentile measures, the criteria used to judge them, and why a set and its average beat any single measure
- [[administered_prices]] — Ex-0 excludes them all; later exclusion measures keep the persistent ones because dropping them biases the core downward
- [[monetary_policy/synthesis/it_lessons_and_challenges (Minella et al., 2002)]] — the BCB's early case for core as a predictor (the 20% trimmed mean Granger-causing headline) that this survey finds generally not borne out in forecasting tests
