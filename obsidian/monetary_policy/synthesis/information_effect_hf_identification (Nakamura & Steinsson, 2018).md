---
aliases: ["Nakamura 2018 - High Frequency Identification of Monetary Non-Neutrality: The Information Effect"]
---

# High Frequency Identification of Monetary Non-Neutrality: The Information Effect — Nakamura & Steinsson 2018

**Type:** paper (working paper, with appendices A–H)
**Tags:** #information-effect #high-frequency-identification #fomc #tips #real-rates #forward-guidance #natural-rate #phillips-curve
**Source:** NBER Working Paper No. 19260, July 2013, Revised January 2018 (JEL E30, E40, E50)
**Language:** English
**Source file:** [[monetary_policy/clean_md/information_effect_hf_identification (Nakamura & Steinsson, 2018)]]

---

## Context and motivation

Most changes in interest rates "happen for a reason", so VAR and narrative identification (Christiano, Eichenbaum & Evans; Bernanke, Boivin & Eliasz; Romer & Romer 2004) must control for confounders and some endogeneity bias may remain. The paper instead uses the discontinuity created by the eight scheduled FOMC meetings a year: unexpected changes in interest rates in a 30-minute window around the announcement (10 minutes before to 20 minutes after, footnote 4) are taken to arise from news about monetary policy. The cost is power — the shocks have a standard deviation of only about 5 basis points, too small to estimate effects on future output directly — so the paper measures variables that respond at once: nominal and real (TIPS) rates, break-even inflation, and Blue Chip survey expectations. Real rates matter because the link from nominal to real rates is what separates New Keynesian from Neoclassical models.

## Core argument / thesis

A surprise tightening raises nominal and real rates roughly one-for-one several years out, barely moves expected inflation, and — contrary to standard models — **raises** survey expectations of output growth. Following Romer and Romer (2000), the authors call the effect of FOMC announcements on private views of non-monetary fundamentals the **"Fed information effect"**: when the Fed signals higher rates than expected, markets infer that the Fed is more optimistic about the economy and update their own beliefs. The evidence then implies that the Fed is powerful either through the conventional channel (large nominal and real rigidities) or through its influence over beliefs about fundamentals, or both. In the estimated model, "Roughly 2/3 of the response of real interest rates to FOMC announcements are estimated to be a response of the natural rate of interest and only 1/3 a tightening of real rates relative to the natural rate."

## Key mechanisms / model

- **Policy news shock (section 3, Appendix A)**: first principal component of the 30-minute change in five rates — the current-month fed funds future (scaled for the days remaining), the expected rate after the next FOMC meeting, and 3-month eurodollar futures two, three and four quarters ahead (the same five futures as Gürkaynak, Sack & Swanson 2005; closely related to their "path factor"). It therefore captures forward guidance, not only the surprise in the funds rate. Rescaled so its effect on the 1-year nominal Treasury yield is one. Regressions take the form of equation (1), the one-day change in an outcome on the shock.
- **Background noise test (section 3.2, Appendices B–C)**: Rigobon's heteroskedasticity-based estimator compares FOMC windows with non-FOMC Tuesdays and Wednesdays, assuming only the variance of monetary shocks rises on FOMC days (equation 10); confidence intervals by a weak-instrument-robust test inversion (Fieller method).
- **Risk premia (section 3.3, Appendix D)**: Blue Chip expectations of short rates, the Abrahams, Adrian, Crump & Moench (2015) affine term structure decomposition, and longer event windows.
- **Information test (section 4, Appendices F–G)**: monthly change in Blue Chip expected output growth on the shock in that month (shocks in the first week of the month dropped); Greenbook-minus-Blue Chip forecast gaps as a measure of Fed relative optimism (equations 23–24).
- **Fed information model (section 5.1, Appendix H)**: a New Keynesian model with internal habits (b = 0.9) and price indexation to past inflation (a backward-looking Phillips curve), equations (2)–(4). Policy: the real rate equals an AR(2) component plus a weak inflation response (equations 5–6, φπ = 0.01); the innovation is the monetary shock and the AR(2) produces the hump across the term structure. **Information effect**: private beliefs about the path of the natural rate of interest shift by a fraction ψ of the shock to the policy component (equation 7), and beliefs about current natural output by the same proportion; ψ is the information share, 1−ψ the conventional real-rate gap. Estimated by simulated method of moments (ρ1, ρ2, ψ and the Phillips curve slope), with β = 0.99, IES σ = 0.5, ω = 2; bootstrap with 1000 repetitions.
- **Why it matters for inference (Appendix E)**: in the textbook NK model the inflation response relative to the real-rate response pins down the product of rigidity and IES parameters (equation 16); with information effects it is the **real interest rate gap** — real rate minus the believed natural rate — that drives the output gap and inflation (equations 18–19), so ignoring information overstates rigidities.

## Main results / findings

**Interest rates and break-even inflation (Table 1; sample 1/1/2000–3/19/2014, July 2008–June 2009 dropped; 106 observations, 74 for 2- and 3-year yields and forwards from 2004).**
- Nominal yields: 0.67 (3M), 0.85 (6M), 1.00 (1Y), 1.10 (2Y), 1.06 (3Y), 0.73 (5Y), 0.38 (10Y). Nominal instantaneous forwards fall from 1.14 at 2 years to -0.08 at 10 years.
- Real (TIPS) yields: 1.06 (2Y), 1.02 (3Y), 0.64 (5Y), 0.44 (10Y). Real forwards: 0.99 at 2 years, 0.88 at 3, 0.47 at 5, 0.12 at 10 (not significant) — "in the long-run, the effect of monetary policy shocks on real interest rates is zero as theory would predict."
- Break-even inflation from yields is small and insignificant; from forwards it is -6, -21 and -20 basis points at 3, 5 and 10 years, significant only at 5 and 10. A tightening "eventually reduces inflation", but the response is small and comes with a long lag.
- Robust to the pre-crisis 2000–2007 sample, the full sample with the crisis, and adding unscheduled meetings (Table A.1). Using the fed funds surprise alone gives much smaller effects (Table A.2).

**Background noise (Table 2).** With a 30-minute window OLS and Rigobon estimates nearly coincide. With a one-day window they diverge — point estimates differ by dozens of basis points and change sign in three of six cases — and OLS "massively overstates the true statistical precision". Using the one-day change in the 2-year yield as indicator (Hanson & Stein 2015), OLS finds a significant effect on the 10-year real forward that the Rigobon estimator shows to be insignificant.

**Risk premia (Appendix D).** Blue Chip expected short rates respond persistently, nominal and real (Table D.1, noisy); risk-neutral rates from the affine model respond much like raw rates, and the risk-premium component barely moves (Table D.2); effects do not dissipate over 1 to 250 trading days (Table D.3, large standard errors). The expectations hypothesis is "a good approximation in response to our monetary shocks, even though it is not a good approximation unconditionally." Inflation swaps (from 2005) are too noisy to be informative (Table A.4).

**Expected output growth rises after a tightening (Table 3).** Coefficients 1.01 (1995–2014, 120 observations), 1.04 (2000–2014), 0.95 (2000–2007), 0.79 (1995–2000), "In sharp contrast to the conventional theory". By quarter (Table A.5) all eight horizons are positive. Greenbook evidence (Table G.1): policy news shocks tend to be positive when the Greenbook growth forecast exceeds Blue Chip's, and the gap narrows after the shock (significant at q = 0 and q = 5).

**Estimated model (Table 4, Figures 3–9).** The information share is about 2/3; the model reproduces the hump-shaped rate responses, the small delayed inflation response and the rise in expected growth, while the output gap falls (the Fed raises rates by more than the believed rise in the natural rate). The Phillips curve is "very flat", which the authors relate to the persistence of their shocks (forward guidance far into the future). Setting the information effect to zero yields a flatter Phillips curve — an overestimate of rigidities; setting it near one yields a much steeper one. Varying the IES barely changes the estimates; without habits the whole rate change is estimated to be information and the fit to output growth is much worse.

**Causal effect and policy (section 6).** A tightening raises expected output permanently in the model, but most of that is news that would have arrived anyway; against a counterfactual in which productivity follows the same path and the Fed tracks the natural rate, the causal effect splits into a fall in the output gap (conventional channel) and a rise in natural output from learning good news earlier (through habit, or investment in a model with capital). For the estimated parameters the overall effect of a surprise hike is to **raise** output: the Fed is "fighting against itself" when it surprises markets, and a surprise easing "may be counter-productive". Systematic policy carries no information effect, so rule-based rate increases "reduce output substantially" (Figure 9) — an external validity problem when shock estimates are used to infer the effects of systematic policy. Withholding bad news may be optimal only when the Fed cannot track the natural rate, e.g. at the zero lower bound (footnote 1, section 6.1). The Volcker tightening is cited as a case with a small information effect.

**Stock prices (Table 5).** The S&P500 falls 6.5% after a shock that raises the 2-year nominal forward by 1%; the model gives -6.8 with the information effect and -11.1 without it, so the data favour information.

## Limitations and caveats

- **Table 4 lost its column headers** (the parameter symbols survive only as blank characters and an "x"). The row labels show the first column is the information parameter (0.68 baseline, fixed at 0.00 and 0.99 in the No Information and Full Information rows); the second column moves as the text describes the Phillips curve slope (11.2 baseline, 3.4 without information, 563 with near-full information), but its scale is not stated in the file. The last two columns (0.9 and 0.79 in every row) are presumably the autoregressive roots, unlabeled.
- **Stock price standard error is inconsistent**: Table 5 prints (3.9), the text says "a standard error of 3.3%". Flagged as written.
- Table 2's column layout is scrambled: the column labels (2-Year, 5-Year, 10-Year Forward; OLS, Rigobon) were moved to the bottom, and rows must be matched by order; the intervals quoted in words above come from the text. Tables D.3 and G.1 likewise have their labels displaced; Table G.1's second panel (the reversal regression) has its title after the numbers.
- Figures 1–9 survive only as axis ticks and legends; the quantitative paths of Figures 3–9 (including the 2/3 decomposition in Figure 5 and the causal-effect decomposition in Figure 8) cannot be read from the file — the numbers above come from the text.
- Several URLs (FOMC calendar, Gürkaynak–Sack–Wright yield data, Greenbook data, CME guides) are cut mid-string; the copyright notice is truncated. Equations (2)–(7) and Appendix H are legible but with hats and subscripts split across lines.
- Authors' own caveats: the Blue Chip regressions require the shock to be orthogonal to confounders over a whole month (stronger than for the high-frequency rate regressions); predictability of the shocks is hard to establish ("data mining and peso problem concerns"); the counterfactual for the causal effect is an assumption ("We don't have any data to precisely pin down the counterfactual"); and the information effect is modeled as a single fraction ψ with no heterogeneity across episodes.

## Connections

- [[information_effect]] — the paper's subject: defines the Fed information effect, measures it through the rise in expected output growth after a tightening, and estimates its share at about 2/3
- [[natural_rate_of_interest]] — the information effect is modeled as a shift in private beliefs about the path of the natural rate; the real-rate gap, not the real rate, drives inflation and output
- [[forward_guidance]] — the policy news shock is built from futures out to four quarters, so it captures forward guidance; the AR(2) policy component models shocks that are "mostly but not exclusively forward guidance shocks"
- [[nk_phillips_curve]] — estimated very flat; ignoring the information effect makes it flatter still and overstates nominal and real rigidities
- [[monetary_policy/synthesis/forward_guidance_effects (Campbell et al., 2012)]] — the earlier evidence that a surprise tightening lowers expected unemployment, which the authors cite as similar; Campbell et al. read it as Delphic content, here it is modeled as information about the natural rate
- [[monetary_policy/synthesis/basic_nk_model_ch3 (Gali, 2015)]] — the textbook Euler equation and Phillips curve of Appendix E are the conventional benchmark the information model departs from
