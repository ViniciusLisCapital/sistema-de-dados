---
aliases: ["Clarida 2000 - Monetary Policy Rules and Macroeconomic Stability: Evidence and Some Theory"]
---

# Monetary Policy Rules and Macroeconomic Stability: Evidence and Some Theory — Richard Clarida, Jordi Galí & Mark Gertler 2000

**Type:** paper
**Tags:** #taylor-rule #taylor-principle #interest-rate-smoothing #indeterminacy #sunspots #fed #volcker #gmm
**Source:** the clean_md is a version dated May 1999 (first draft March 1997), with no journal named; authors at Columbia University, New York University and Universitat Pompeu Fabra (JEL E32, E52)
**Language:** English
**Source file:** [[monetary_policy/clean_md/monetary_policy_rules_stability (Clarida, Gali & Gertler, 2000)]]

---

## Context and motivation

From the late 1960s to the early 1980s the US had high and volatile inflation and several severe recessions; afterwards inflation stayed low and output growth relatively stable. Supply (oil) shocks are the usual explanation, but they cannot explain persistent inflation without accommodating monetary policy, and the build-up of inflation preceded the oil crises (De Long 1997). The paper asks how monetary policy differed before and after 1979, the year Volcker became Fed Chairman, and whether that difference can account for the change in macroeconomic behavior — adding "precision to this conventional wisdom".

## Core argument / thesis

Estimating a forward-looking reaction function for the federal funds rate, the authors find that before Volcker the Fed raised nominal rates by less than the rise in expected inflation, letting real rates fall, while under Volcker and Greenspan it "systematically raised real as well as nominal short term interest rates in response to higher expected inflation" — roughly two-for-one. In a standard New Keynesian model, the pre-Volcker rule (inflation coefficient below one) is destabilizing in two ways: it permits self-fulfilling ("sunspot") fluctuations in inflation and output, and, even near the boundary, it insulates the economy much worse from fundamental shocks. The 1970s stagflation is read as supply shocks interacting with an accommodating rule.

## Key mechanisms / model

- **Forward-looking target rule (equation 1)**: the target funds rate responds to the gap between expected inflation k periods ahead and the inflation target, and to the expected average output gap q periods ahead, with an intercept equal to the desired rate when both are on target. It nests Taylor (1993) when lagged inflation and output are sufficient statistics for forecasting inflation, but lets the Fed use a broad information set. The implied real-rate rule (2) shows the benchmark: an inflation coefficient above one is stabilizing, below one accommodative or destabilizing; a positive output coefficient is stabilizing.
- **Interest rate smoothing and policy shocks (equations 3–4)**: the actual rate adjusts partially to the target — each period the Fed closes only a fraction of the gap between the target and a linear combination of past rates — plus a zero-mean exogenous interest rate shock. The smoothing parameter measures the degree of inertia. Why smoothing occurs is "beyond the scope of this paper"; footnote 12 cites fear of disrupting financial markets (Goodfriend 1991) and uncertainty about the effects of rate changes (Sack 1997).
- **Estimation (equation 5)**: GMM on orthogonality conditions with instruments known when the rate is set, with an optimal weighting matrix for serial correlation; the inflation target is identified by setting the equilibrium real rate equal to the sample-average real rate (relaxed in robustness). Quarterly data 1960:1–1996:4; funds rate in the first month of each quarter; GDP deflator inflation and CBO output gap as baseline; instruments include lags of the funds rate, inflation, the gap, commodity price inflation, M2 growth and the long-short spread. Two lags of the interest rate; four lags of instruments. Subperiods: pre-Volcker (60:1–79:2: Martin, Burns, Miller) and Volcker-Greenspan (79:3–96:4).
- **Theoretical model (section IV, equations 6–9)**: a log-linearized sticky-price model (King and Wolman; Woodford; Yun) — a forward-looking Phillips curve from Calvo pricing, an IS equation from the Euler equation with a demand shock, and the estimated rule with a one-period horizon. Supply (natural output) and demand shocks follow AR(1) processes. The output elasticity of inflation is set at an intermediate value following Woodford (1996), printed "0:30" with a colon for the decimal point (footnote 32, which gives the literature range as "0:05" to "1:22").
- **Indeterminacy mechanism**: with an inflation coefficient below unity, a rise in expected inflation lowers the real rate, stimulates demand and raises inflation, so "the initial rise in expected inflation thus becomes self-confirmed". Footnote 33: the unit threshold is exact only with no output response, and too strong a response can also cause indeterminacy (Bernanke and Woodford 1997).

## Main results / findings

**Volatility (Table I).** Standard deviation of inflation (level): 2.77 pre-Volcker, 2.18 Volcker-Greenspan, 1.00 post-82; output gap: 2.71, 2.36, 2.06. The fall is "more dramatic" when the second subperiod starts in 82:4.

**Baseline estimates (Table II, one-quarter horizons; standard errors in brackets).** The text lists the columns as the inflation target, the inflation coefficient, the output-gap coefficient, the smoothing parameter and the p-value of Hansen's J-test.
- Pre-Volcker: 4.24 (1.09), 0.83 (0.07), 0.27 (0.08), 0.68 (0.05); p-value 0.834.
- Volcker-Greenspan: 3.58 (0.50), 2.15 (0.40), 0.93 (0.42), 0.79 (0.04); p-value 0.316.
- The overidentifying restrictions are not rejected; the inflation coefficient is "significantly below unity" pre-Volcker and "far greater than one" after; the output coefficient is significant in both, only marginally after 1979. The inflation targets ("roughly four and a quarter percent pre-Volcker and three and half percent post-Volcker") do not differ significantly, so the change is not just a lower target.
- **Smoothing**: "Only between 10 and 30 percent of a change in the interest rate target is reflected in the Funds rate within the quarter of the change", confirming "the conventional wisdom that the Federal Reserve smooths adjustments in the interest rate."
- Over 1987–1992 the estimated target rate tracks the actual rate about as well as Taylor's rule (Figures I–II).

**Robustness.**
- *Alternative measures (Table III)*: detrended output, unemployment-based gap and CPI give inflation coefficients of 0.75, 0.84 and 0.68 pre-Volcker against 1.97, 2.01 and 2.14 after; the post-1979 output coefficient becomes insignificant.
- *Horizons (Table IV)*: with a one-year inflation horizon (k=4, q=1 and k=4, q=2), 0.86 and 0.88 pre-Volcker against 2.62 and 2.73 after.
- *Unrestricted intercept (Table V)*: only the post-1979 output coefficient loses significance.
- *Chairmen (Table VI)*: the inflation target and inflation coefficient do not differ between Martin and Burns-Miller (coefficient 0.86 or 0.92 depending on horizon) nor between Volcker and Greenspan (2.02 or 2.38). The output coefficient is near zero under Volcker (-0.02) and 0.99 under Greenspan at the (1,1) horizon, a difference that vanishes at (4,1); at (4,1) smoothing is significantly higher under Greenspan (0.91 against 0.74). Post-82 (excluding the 1979:4–1982:4 non-borrowed reserves targeting and the disinflation from roughly 10 percent in 1980 to 4 percent in 1983): inflation coefficients 1.58 (noisy) and 3.13, output coefficients small and insignificant — "we cannot reject the hypothesis that the Fed has effectively pursued a pure inflation targeting policy."
- *Backward-looking Taylor-type rule (Table VII)*: inflation coefficients 0.86 pre-Volcker, 1.72 Volcker-Greenspan, 2.55 post-82 — the result does not depend on the forward-looking specification.

**Oil shocks (section III.D).** The inflation build-up of the late 1960s and early 1970s preceded the first oil shock, with the real oil price falling while inflation rose (Figure III); inflation rose for three years before the 1979 shock and fell before oil prices did. In a multivariate system the oil-shock measure explains "at best roughly ten percent" of GDP deflator variation over 1960:1–1984:4 (footnote 27). The ex post real rate fell as inflation rose before 1979 and rose sharply in late 1979 (Figure IV).

**Model simulations.**
- Under the pre-Volcker rule, sunspot shocks produce persistent fluctuations in output and inflation with no fundamental shock (Figures V–VI): the nominal rate rises but by less than expected inflation, so the real rate falls and validates the expectation. Under the Volcker-Greenspan rule they cannot occur.
- Near-indeterminacy (Table VIII): with the output and smoothing coefficients held at their pre-Volcker values, raising the inflation coefficient from one to two cuts the volatility of both output and inflation "by more than half", for supply and demand shocks alike — "The reduction in volatility that the Volcker-Greenspan rule achieves is thus quite substantial."
- A negative supply shock has a persistent effect on inflation only for an inflation coefficient near unity (Figure VII) — the accommodating rule can account for 1970s stagflation; the Volcker-Greenspan rule cannot.
- Results carry over to any model with an IS-type relation and a short-run Phillips curve; in a backward-looking model a coefficient below one gives explosive behavior rather than sunspots (footnote 37).

**Open question (section V).** Why the Fed followed an inferior rule before 1979: it may have overestimated potential output or underestimated the natural unemployment rate (De Long; Orphanides on real-time estimates), or policymakers and the profession did not yet understand inflation dynamics, expectations and credibility.

## Limitations and caveats

- **The text is font-encoded in symbols and in-line numbers.** The paper's Greek letters (the inflation coefficient, the output coefficient, the smoothing parameter) print as substituted characters ("n", blank, "1") or vanish, and equations (1)–(9) are unreadable strings. Several numbers in the prose are encoded and lost: the J-test p-values and the pre-Volcker inflation estimate quoted in section III.A, the calibrated discount factor, implied risk-free rate, risk aversion and AR(1) coefficient in section IV.A, the output and smoothing coefficients held fixed in section IV.C, the normalization point of Table VIII and the range of inflation coefficients in Figure VII. The note gives these only where the tables print them.
- **Table headers are blank** in Tables II–VII (only "T" and "p" survive); the column attribution above follows the text's listing of the parameters for Table II. Table V lost its pre-Volcker row label, and its coefficient columns are identical to the CPI rows of Table III (only the first column differs: 2.19 and -0.27); flagged, not corrected. The instrument notes of Tables III–V and VII are cut after "The set of instruments includes".
- **Table VIII is entirely garbled** (encoded labels and numbers), so the volatility ratios cannot be read; the result is reported from the text. Figures I–VII survive only as titles and a few axis ticks.
- The "ff" and "fi" ligatures are dropped throughout ("di\nerences", "signicant", "in ation"), which splits words across lines; numbers in the text otherwise read normally.
- Authors' caveats: the inflation target is identified only by assuming the equilibrium real rate equals the sample-average real rate; short samples with little inflation variation can mislead; the 1979–82 reserves-targeting period is a special operating regime; for some pre-Volcker specifications the inflation coefficient cannot be statistically distinguished from one (footnote 35); the question of why the pre-1979 rule was chosen is left open.

## Connections

- [[taylor_principle]] — the paper's central empirical application: an inflation coefficient below one pre-Volcker (indeterminacy, sunspot fluctuations) and around two under Volcker-Greenspan, plus the near-indeterminacy volatility result
- [[taylor_rule]] — a forward-looking rule that nests Taylor (1993), estimated by GMM; matches Taylor's rule over 1987–1992; the backward-looking Taylor-type version in Table VII gives the same split
- [[interest_rate_smoothing]] — partial adjustment of the funds rate to its target (equation 3), with smoothing parameters of 0.68 and 0.79 (Table II): only 10 to 30 percent of a target change passes through within the quarter
- [[nk_phillips_curve]] — the forward-looking Phillips curve (6) of the model in which the rules are evaluated; a short-run Phillips curve is one of the two features the results need
- [[monetary_policy/synthesis/science_of_monetary_policy (Clarida, Gali & Gertler, 1999)]] — the companion survey, whose section 7 reports a related forward-looking estimate (its Table 1) and the same pre-Volcker sunspot argument in summary; here the evidence and the model are developed in full
- [[monetary_policy/synthesis/taylor_rule (Taylor, 1993)]] — the rule this forward-looking specification nests, and the 1987–1992 period over which both fit the funds rate
- [[monetary_policy/synthesis/monetary_policy_design_nk_ch4 (Gali, 2015)]] — the textbook determinacy conditions for current- and forward-looking rules that this paper applies to estimated US rules
