---
aliases: ["Cusinato 2010 - Output Gap and GDP in Brazil real time"]
---

# Output Gap and GDP in Brazil: a real-time data analysis — Cusinato, Minella & Pôrto Júnior 2010

**Type:** paper (central bank working paper)
**Tags:** #real-time-data #output-gap #gdp-revisions #potential-output #brazil
**Source:** Banco Central do Brasil, Working Paper Series n. 203, Apr. 2010, p. 1-65
**Language:** English
**Source file:** [[economic_activity/clean_md/output_gap_brazil_real_time (Cusinato, Minella & Porto Junior, 2013)]]

---

## Context and motivation

GDP growth and the output gap are the main activity measures behind consumption, investment and, above all, monetary policy decisions — a positive gap "may call for a monetary policy reaction", as in a Taylor rule. But they are decided on with data as first released, and the US, Canadian and Norwegian literature (Croushore and Stark; Orphanides and van Norden 2002; Cayen and van Norden; Bernhardsen et al.) found large revisions to both, with real-time gaps unreliable. The paper asks whether that holds for Brazil, building the first real-time data set of Brazil's quarterly GDP: 51 vintages of seasonally adjusted GDP released by the IBGE from 1996Q1 to 2008Q2, each starting in 1990Q1.

## Core argument / thesis

What the policymaker sees at the margin is a noisy version of what will later be known. For GDP growth the revisions are large quarter-on-quarter but partly offset each other from one quarter to the next, so they shrink when growth is measured over longer windows. For the output gap the problem is worse and does not wash out: the gap is revised both because GDP is revised and because each new observation changes the estimated trend at the end of the sample, and the second source makes errors persistent — a wrong reading of the cycle can last several quarters. Hence real-time gap estimates should be used "with great caution", and policy rules or forecast comparisons evaluated on today's revised data misjudge what was knowable at the time.

## Key mechanisms / model

- **Why data are revised** (Section 2): the information set grows, seasonal factors are reestimated, and methodology changes. Statistical agencies trade off speed against precision. The IBGE revises the previous quarter at each release, does a broader revision with the third-quarter release, and benchmarks quarterly series to the annual accounts (Denton's method, footnote 8).
- **Real-time vs. final**: the real-time series takes the first release of each quarter (the diagonal of the vintage table); the final series takes every quarter from the last vintage (2008Q2); the revision is final minus real-time. The paper assumes revisions improve estimates, so what it measures is the error later corrected, not the total error.
- **Why GDP revisions shrink with aggregation**: quarter-on-quarter revisions are negatively autocorrelated (a positive revision tends to be followed by a negative one), so they cancel within longer windows; growth of i-quarter averages improves even more, since the averaged denominator has been revised more times.
- **Output gap as deviation from trend**: output = potential (trend) + gap. Four detrending methods: HP filter (smoothing parameter 1600), linear trend, quadratic trend, and the Harvey-Clark unobserved-components model (potential a random walk with a drifting drift, gap an AR(2), estimated by Kalman filter). The authors note this statistical gap is not the New Keynesian flexible-price gap, which is harder to measure; production-function methods and Phillips-curve UC models are excluded (the post-1994 sample is too short for recursive estimation).
- **Decomposition of gap revisions** (Orphanides and van Norden method): a "quasi-real" gap is estimated on final data truncated at each quarter. Quasi-real minus real-time isolates the effect of GDP data revisions; final minus quasi-real isolates the sample-size effect, which is mostly the low precision of the trend at the end of the sample (including the HP filter's end-point problem).
- **What carries the result**: the end-of-sample problem is generic to any trend-based gap, so it would survive perfectly measured GDP; and the persistence of revisions (high first-order autocorrelation) is what turns noise into a lasting misreading of the cycle.

## Main results / findings

- **GDP growth** (Brazil, 1996Q1-2008Q2, Table 4): quarter-on-quarter growth is revised by 0.67 p.p. on average in absolute value; the sign flips in 16 percent of cases and the revision exceeds the final growth rate in 26 percent. The mean revision is positive (0.13 p.p.): first releases understate growth. Revisions are negatively autocorrelated (-0.34), so aggregation helps: for four-quarter growth of averages the mean absolute revision falls to 0.16 per quarter, 0.64 in annual terms (Table 6), with fewer sign changes; for year-over-year growth it is 0.23 p.p. per quarter.
- **Methodological change**: the new IBGE methodology introduced with the 2006Q4 vintage raised growth estimates on average and was a relevant source of revisions, but only part of them (Tables 7 and 8).
- **International comparison**: Brazil's GDP revisions are larger than in most countries in Ahmad, Bournot and Koechlin (2007), with positive bias as elsewhere (Table 10).
- **Output gap** (Table 12): all four methods are revised substantially. The real-time gap has the "wrong" sign in 30 percent of quarters with HP and HC and 44 percent with the quadratic trend; for HP, QT and HC the revision is larger than the final gap in roughly half the cases or more. The linear trend is the exception on most indicators (correlation 0.91 between real-time and final, sign wrong in 14 percent), despite the largest bias. The quadratic trend is worst on almost every indicator (correlation 0.21). The authors stress that smaller revisions do not make a method better, since the final estimates' own errors are unknown.
- **Sources of gap revisions** (Table 14): both GDP revisions and the sample-size effect matter for the size of revisions; the sample effect dominates for the quadratic trend and data revisions dominate for Harvey-Clark. In every method most of the *persistence* of revisions comes from the sample-size (end-of-sample) effect, while most of the *bias* comes from data revisions — largely the 2006Q4 methodological change (Table 15).
- Compared with the US, Canada and Norway, Brazil's gap-revision indicators are generally less unfavorable, but still point to "relevant limitations in real-time output gap estimates".
- Implications drawn: be very cautious with real-time gaps; evaluate past policy and estimate Taylor rules on real-time data; do not judge real-time inflation forecasts against models run on final data; and use a broad set of activity indicators, which reduces the risk of relying on revised series.

## Limitations and caveats

- The "final" vintage (2008Q2) is itself subject to revision and to the limits of any GDP estimate, and the gap is unobservable even with perfect GDP; revisions measure only the corrected part of the error.
- The sample is short (1990Q1 start, real-time window 1996Q1-2008Q2) and spans a methodological break; the authors use the new-methodology 2006Q4 vintage as standard.
- Only statistical detrending methods are assessed; the conclusions say nothing about production-function or structural gaps, and the paper warns that revision size is not a ranking of methods.
- The questions it raises are left open: whether past Copom decisions would differ with revised data, how a real-time Taylor rule differs from a final-data one, and whether gap revisions are predictable.
- Text inconsistency: Section 4.3 gives the quadratic-trend MAR as 2.16 p.p. in one sentence and 2.26 p.p. in the next; Table 12 prints 2.26.
- Damaged text: the display equations (1)-(12) — growth rates, the trend/cycle decomposition, the HP loss function, the trend regressions, the Harvey-Clark state-space model — and the formulas in footnotes 7 and 31 and in the back-filling procedure of Section 3.1 are not in the text layer (only fragments and equation numbers remain); the prose describing them is intact. Figures 1-12 and the appendix figures survive only as axis labels. Multi-column tables (9, 13, 16) have their column headers scrambled. Footnote 32 is cut off mid-sentence, the reference list is missing (the text jumps from the conclusion to the appendix), and the file ends with the BCB's list of working papers. The file name and the tracker carry a different year from the 2010 printed on the title page.

## Connections

- [[real_time_data]] — builds Brazil's real-time GDP vintages and measures GDP-growth and output-gap revisions, decomposing the latter into data-revision and end-of-sample effects
- [[output_gap]] — compares four trend-based gap estimators and shows how unreliable each is at the end of the sample
- [[monetary_policy/synthesis/policy_rules_real_time_data (Orphanides, 2001)]] — Orphanides shows real-time data change Taylor-rule prescriptions in the US; this paper measures the input revisions for Brazil and draws the same caution for estimating rules
- [[economic_activity/synthesis/ibcbr_vs_pib_metodologia (BCB, 2018)]] — both show that quarter-on-quarter activity readings are noisy (seasonal adjustment, revisions) and that longer comparison windows are more reliable
