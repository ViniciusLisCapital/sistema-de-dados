---
aliases: ["Areosa 2016 - What drives inflation expectations in Brazil? Public versus private information"]
---

# What drives inflation expectations in Brazil? Public versus private information — Waldyr D. Areosa 2016

**Type:** paper (BCB Working Paper; structural estimation on survey micro data)
**Tags:** #inflation-expectations #focus-survey #noisy-information #morris-shin #strategic-substitutability #information-rigidities #brazil
**Source:** Banco Central do Brasil, Working Paper Series n. 418, February 2016, p. 1-26
**Language:** English
**Source file:** [[expectations/clean_md/inflation_expectations_public_private_info (Areosa, 2016)]]

---

## Context and motivation

How much do professional forecasters rely on public information (the market consensus) versus their own private information when forecasting inflation, and do they weight the two efficiently? The information-frictions literature (Coibion and Gorodnichenko, sticky and noisy information) had measured rigidity, and the Morris–Shin strand had allowed forecasts to be strategic complements (forecasters wanting to stay close to the crowd), but not that forecasters might want to stand apart. Using confidential individual IPCA forecasts from the BCB Market Expectations System (Focus), January 2004 to December 2014, the paper estimates both the weights and the strategic motive behind them.

## Core argument / thesis

Forecasters filter inflation from a noisy private signal and a noisy public signal, and care both about accuracy and about where they stand relative to the average forecast. The weight they put on public information therefore reflects two things: its relative precision, and the value of coordination. In Brazil, public information gets the larger weight because it is more precise than private information; but the weight is below what precision alone would justify, so forecasters overweight their private information. The interpretation is strategic substitutability: forecasters want to differentiate themselves, possibly to raise their chances of entering the Top 5 ranking.

## Key mechanisms / model

**Morris–Shin forecaster with a beauty-contest term (Section 2, equations 1–5).** Each forecaster's loss combines the squared distance between the forecast and inflation and the squared distance between the forecast and the mean forecast, weighted by a parameter r between −1 and 1. Positive r is strategic complementarity (stay close to peers); negative r is substitutability (stand apart). Each forecaster sees a private signal (inflation plus idiosyncratic noise) and a public signal (inflation plus common noise; here the market consensus). The Bayesian posterior weights the public signal by its relative precision δ. In equilibrium the forecast is a convex combination of the two signals with public weight γ, which equals δ when r = 0, exceeds it under complementarity, and falls short of it under substitutability, because the public signal is the better predictor of what others will forecast.

**Identification (Section 3).** Subtracting inflation from the equilibrium forecast, an individual's forecast error equals γ times the public signal's error plus a private-noise term. So γ is the slope of a fixed-effects panel regression of individual forecast errors on the consensus error (equation 6). The residual variance and γ give the private signal's noise; the variance of the consensus error gives the public signal's noise; together they give the efficient weight δ, and comparing γ with δ gives r. Inference uses 10,000 simulated re-estimations.

**What carries the result.** The public signal must be what forecasters actually observe: it is the projection of realized inflation on the last aggregate mean forecast available when each forecast was made. Errors must be independent across forecasters except through the common public shock (relaxed with clustered errors in Section 6.1). And the model assumes all forecasters' private signals are equally precise; the Top 5 variants test whether some forecasters have better information.

**A competing reading the author addresses (Section 5).** Because the consensus dates from before the individual forecast, a low weight on it could reflect newer private information rather than a wish to differentiate. The author argues the gap is under 30 days and usually under 15, so little public information is being disregarded; the argument is not tested.

## Main results / findings

- **Public information weighs more.** γ is significant at 1% at every horizon from 0 to 12 months, between 0.50 and 0.80 (Table 2), highest at short (0–3 months) and long (10–12 months) horizons and lowest around 6–9 months. The implied noise of the public signal is below that of the private signal: public information is more precise.
- **But less than its precision warrants.** The efficient weight δ exceeds the actual weight γ at every horizon except 6 months, so r is negative: forecasts are strategic substitutes, by the author's reading a search for differentiation (Table 2). The simulation tests reject that public information is the less precise, that γ ≥ δ, and that r ≥ 0, with p-values near zero (Table 3).
- **Robust across checks (Section 6).** The significance of γ survives period, cross-section and two-way clustering (Table 4); the weights barely change with the median or the Top 5 mean or median as the public signal (Table 5); excluding short-lived forecasters or extreme errors leaves the signs unchanged (Tables 7–8). The strategic motive is stronger when the public signal is the Top 5 consensus (r ≈ −0.50 against r ≈ −0.25 for the mean of all forecasters, Section 6.2), and weaker once extreme errors are excluded (Table 8).
- **Error pattern (Table 1).** The consensus-based public signal tends to overestimate inflation, and individual forecasts correct part of that, so individual mean errors are small but dispersed.

## Limitations and caveats

- By the author's account: the incentives behind overweighting private information are "beyond the scope" of the paper; the timing gap between the consensus and the individual forecast offers an alternative interpretation, argued away rather than tested; the 30-observation threshold is arbitrary.
- What the text shows: δ and r are not estimated directly but backed out of the model, so the substitutability finding depends on the Morris–Shin structure, on equal private precision, and on the constructed public signal. At 6 months the implied r is positive in Table 2 while the simulated r in Table 3 is negative with a p-value of zero, which the text does not reconcile; implied and simulated r also differ noticeably at some horizons. The text states the tests in the opposite direction to the tables in two places: the first test is written "σy ⩾ σx" in Section 5.2 and "σx ⩾ σy" in Table 3, and the second test is said to show that forecasters "overweight public information", contradicting the conclusion that γ < δ. The forecaster filter is described as "at least 30 non-valid forecasts" in Section 6.3 and "non-zero" in its footnote and table notes. The sample covers 2004–2014 only and IPCA forecasts only.
- Damaged passages: the Greek letters and operators of equations (1)–(6) and the Section 3.2 formulas survive but with superscripts and integrals split across lines (e.g. the mean forecast as an integral, the precisions as inverse variances). Figure 1 (histograms of forecast errors) survives only as its caption. The reference list is not in the file, which ends with Table 8.

## Connections

- [[information_rigidities]] — the noisy-information model with strategic interaction (Morris–Shin with substitutability) estimated on Focus micro data, 2004–2014
- [[strategic_forecasting]] — forecasters' concern for their position relative to the consensus: estimated strategic substitutability (r < 0) and overweighting of private information, possibly linked to the Top 5 ranking
- [[survey_forecast_rationality]] — forecasts deviate from the efficient, error-minimizing weights on public and private information
- [[expectations/synthesis/empirical_findings_expectations_brazil (Gaglianone, 2017)]] — surveys this paper's two findings (more weight on public information, yet overweighting of private information to differentiate)
- [[expectations/synthesis/formation_expectations_phillips_curve (Coibion, Gorodnichenko & Kamdar, 2018)]] — the information-rigidity framework (Coibion and Gorodnichenko) this paper extends with strategic substitutability; there, professional forecasts are suspected of misreporting for publicity, here the motive is estimated
