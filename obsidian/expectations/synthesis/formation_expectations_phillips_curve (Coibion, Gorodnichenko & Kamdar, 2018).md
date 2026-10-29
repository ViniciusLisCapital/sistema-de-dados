---
aliases: ["Coibion 2017 - The Formation of Expectations, Inflation and the Phillips Curve"]
---

# The Formation of Expectations, Inflation and the Phillips Curve — Olivier Coibion, Yuriy Gorodnichenko & Rupal Kamdar 2017

**Type:** paper (NBER Working Paper; survey plus own estimates)
**Tags:** #inflation-expectations #fire #information-rigidities #phillips-curve #nkpc #household-expectations #survey-data
**Source:** NBER Working Paper No. 23304, March 2017, Revised November 2017
**Language:** English
**Source file:** [[expectations/clean_md/formation_expectations_phillips_curve (Coibion, Gorodnichenko & Kamdar, 2018)]]

---

## Context and motivation

Full-information rational expectations (FIRE) became the workhorse after the rational expectations revolution because it makes models immune to the Lucas critique and tractable; the New Keynesian Phillips curve (NKPC) is its most prominent application. But micro survey data show systematic deviations from FIRE (bias, predictable forecast errors, disagreement), and the FIRE-based Phillips curve has accumulated puzzles: it needs ad hoc lags, it is unstable or flattening, it missed the disinflation that should have followed the Great Recession, it forecasts no better than naïve rules, and its slope depends on the slack measure chosen. The paper asks whether the two problems are one: whether replacing the FIRE expectation with real-time survey expectations repairs the Phillips curve.

## Core argument / thesis

The expectations-formation process should be modeled and measured, not assumed. Surveys consistently reject FIRE, and several alternatives (sticky information, noisy information, rational inattention, bounded rationality, diagnostic expectations, learning) can account for the deviations. In the Phillips curve, using survey expectations in place of FIRE resolves most of the documented puzzles. Among survey measures, household expectations work best: with them the US CPI Phillips curve is stable over 1978–2014, dominates other expectation measures in horse races, and predicts the missing disinflation of 2009–2011. The authors' interpretation is that firms, whose expectations are the ones that matter for price setting, form expectations more like households than like professional forecasters.

## Key mechanisms / model

**What information rigidities predict (Section 4).** Sticky information (agents update infrequently, but fully), noisy information (agents update every period on noisy signals) and rational inattention (agents choose what to attend to) share two predictions. The mean forecast under-responds to shocks: some agents do not know the shock happened, or discount the signal as noise, or are not paying attention. And mean ex-post forecast errors are predictable from ex-ante mean forecast revisions, because the mean forecast is anchored to the previous one. Both are found in the SPF, Livingston, FOMC, Michigan (MSC), financial-market and Consensus Economics forecasts (Coibion and Gorodnichenko 2012, 2015b), with economically large implied rigidity. The other families relax rationality: agents use simplified or misspecified models (sparse max, natural or diagnostic expectations) or learn parameters by least squares, possibly switching among forecasting rules.

**Why survey expectations can legitimately enter the NKPC (Sections 5, 5.D, Appendix B).** The NKPC is derived under FIRE, so plugging in a survey average looks like a misspecification; different information structures do give different Phillips curves (Table 5). Adam and Padula show the standard form survives with subjective expectations if agents cannot predict revisions in their own or others' forecasts ("Condition 1"), which lets the law of iterated expectations (LIE) collapse the forward sums of expected marginal costs and inflation into one-period-ahead expected inflation. The authors derive a test: if the LIE holds, the one-year inflation forecast is a sufficient statistic, so adding expected future slack or a 5-year inflation forecast should not matter. In the MSC and the SPF those added terms are insignificant (Table 6), so they do not detect a violation.

**Whose expectations (Section 5.E).** The relevant expectation in the NKPC is the firm's, and the US has no long national firm survey. Market measures (TIPS break-evens, inflation swaps) are high-frequency but confounded by inflation risk and liquidity premia and have short histories. Professional forecasters may not report true beliefs (cheap talk, publicity incentives, herding). Consumer expectations are argued to be the better proxy: consumers have no strategic reason to misreport, their survey answers predict their incentivized choices, they fit the Phillips curve better, and in New Zealand firms' forecasts resemble households' in both level and dispersion, far from professionals'. Against this, households are sensitive to survey wording and may not track the economy.

**The estimated curve (Section 5.F, equations 9–10).** Quarterly annualized CPI inflation on the mean one-year-ahead inflation forecast and the unemployment gap (unemployment minus the CBO NAIRU), OLS with Newey-West errors, 1978–2014 and subsamples, excluding 2008Q4 as an outlier, with final-vintage data. Equation (10) adds a second expectation measure as a horse race. A third exercise estimates each curve on 1995-2007 and predicts 2009–2011.

## Main results / findings

- **Literature (Section 5.C).** With survey expectations, the forward-looking term dominates and lagged inflation becomes insignificant in a hybrid curve (Brissimis and Magginas, US 1968–2006); survey expectations generate the persistence ad hoc lags were introduced for (Fuhrer), because individual forecasters revise toward the lagged consensus; slack enters with the right sign and significance with survey expectations but not with the FIRE/McCallum approach (Roberts, US 1949 to 1990, Table 3); survey expectations dominate rational expectations in horse races (Fuhrer et al., US 1990:Q1 to 2010:Q2, Table 4).
- **Stability with household expectations (Table 8).** With MSC expectations the slope on the unemployment gap is stable across 1978-1989, 1990-1999 and 2000-2014 (equality not rejected); a point above NAIRU is associated with a 0.2 percentage point decline in inflation. With naïve (backward-looking) expectations the slope swings and the coefficient on expected inflation turns negative in 2000-2014. With SPF, Greenbook and market (Cleveland Fed) expectations the slope shrinks and is insignificant in 2000-2014, the familiar "flattening". R² falls over time with every measure, which the authors attribute to the general decline in inflation predictability.
- **Horse races (Table 9).** Household expectations stay large and significant when any other measure is added (naïve, SPF, Greenbook, markets, MSC 5-year), and the slope stays stable.
- **Missing disinflation (Table 10).** Households expected higher inflation than other agents in 2009–2011, and Phillips curves built on household expectations (the MSC mean and Binder's confident-household measure) have the smallest mean prediction errors; curves on professional, market and Greenbook expectations under-predict inflation.
- **What does not fit.** The result depends on the price index: with core CPI, PCE or the GDP deflator there is no stable downward-sloping curve (Appendix Table 6), which the authors read as consumers forming CPI expectations. Controlling for oil prices (Appendix Table 5) lowers the household coefficient, and the other measures, when each is paired with households, then become significant too; the text nonetheless states that household measures "remain dominant". The coefficient on MSC expected inflation is above one in the full sample (Table 8), which the text does not discuss.
- **Anchoring is not the answer to missing disinflation (footnote 15).** Anchored long-run expectations cannot by themselves explain stable inflation in the NKPC, because inflation depends on next-period expectations and the slack coefficient operates regardless.

## Limitations and caveats

- By the authors' account: no direct historical measure of firms' expectations; the many explanations of non-FIRE behaviour are not discriminated; aggregation (mean against median), the endogeneity of survey expectations collected mid-period, and point forecasts against probability distributions are open issues; the household result holds for CPI only; Greenbook projections give only four observations in the Great Recession exercise.
- What the text shows: the evidence is US only, plus New Zealand firm surveys; the regressions are OLS treating survey expectations as exogenous, which the authors themselves list as contested. "Households are a better proxy for firms" is supported by fit and by the New Zealand evidence, not by observing US firms. The LIE test is a failure to reject in short samples (as few as 91 observations).
- Damaged passages: every equation in the body and in Appendix B, (1) to (10) and (B1) to (B18), is rendered in substitute glyphs with subscripts on separate lines, so none can be read from the file; the note describes them from the text. In Tables 1–2, 4, 6, 8–9 and Appendix Tables 1–6 the regressor names (unemployment gap, expected inflation, oil price terms) are in the same glyphs; the rows can be identified only from the table notes. Figure 1 survives as axis values and labels. The page numbering jumps from 29 to 37: the reference list is not in the file. The file is dated November 2017 (the working-paper revision); its file name carries a different year.

## Connections

- [[information_rigidities]] — sticky information, noisy information and rational inattention: shared predictions (under-reaction of mean forecasts, errors predictable from revisions) and US evidence of large rigidity
- [[survey_forecast_rationality]] — the four classic rationality tests, the Peso problem, and the consistent rejection of FIRE in US survey data, with demographic and experience biases
- [[nk_phillips_curve]] — the FIRE NKPC, its empirical puzzles, and the Adam–Padula condition under which survey expectations can replace FIRE; a LIE test on MSC and SPF data (Table 6)
- [[phillips_curve]] — the expectations-augmented curve in the unemployment gap estimated with six expectation measures, US 1978–2014: stable with household expectations, flattening with professional and market ones (Table 8)
- [[inflation_expectations_anchoring]] — footnote 15: anchored long-run expectations do not by themselves explain the missing disinflation in the NKPC
- [[inflation_expectations_disagreement]] — firms and households disagree far more than professionals; dispersion rises with the level and variance of inflation
- [[breakeven_inflation]] — TIPS break-evens and inflation swaps as expectation measures confounded by inflation risk and liquidity premia, with short histories and the TIPS indexation lag
- [[external/synthesis/us_inflation_phillips_curve (Hooper, Mishkin & Sufi, 2019)]] — the same US flattening puzzle, explained there by anchored expectations; here by the choice of expectations measure, with anchoring judged insufficient
- [[expectations/synthesis/empirical_findings_expectations_brazil (Gaglianone, 2017)]] — cites this paper for the debate on modeling expectations formation; the Brazilian evidence on rigidities and bias it surveys is the counterpart of the US evidence here
