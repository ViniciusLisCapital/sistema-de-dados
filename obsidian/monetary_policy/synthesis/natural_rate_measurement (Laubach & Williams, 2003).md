---
aliases: ["Laubach 2003 - Measuring the Natural Rate of Interest"]
---

# Measuring the Natural Rate of Interest — Thomas Laubach & John C. Williams 2003

**Type:** paper
**Tags:** #natural-rate #r-star #kalman-filter #potential-output #trend-growth #policy-stance #taylor-rule #mismeasurement
**Source:** Board of Governors of the Federal Reserve System; the clean_md is a version dated November 2001, with no journal named (JEL C32, E43, E52, O40)
**Language:** English
**Source file:** [[monetary_policy/clean_md/natural_rate_measurement (Laubach & Williams, 2003)]]

---

## Context and motivation

With the short-term interest rate as the main instrument, the "equilibrium" or "natural" rate is the metric for the stance of policy. The authors define it as "the real short-term interest rate consistent with output converging to potential, where potential is the level of output consistent with stable inflation" — a medium-run anchor that corresponds to the intercept of feedback rules such as Taylor's (1993). Theory (the optimal growth model, equation 1) ties the real rate to trend growth and time preference, and US trend growth has shifted, so a constant natural rate "appears untenable". Simple alternatives fail: a sample mean (about 3 percent) ignores time variation; univariate filters ignore inflation and would read the Volcker disinflation as a rise in r*; Woodford's (2000) period-by-period Wicksellian rate is model-specific and estimated on detrended data, so it misses the low-frequency movements this paper targets.

## Core argument / thesis

Jointly estimating r*, potential output and its trend growth rate with the Kalman filter shows "substantial variation in the natural rate of interest over the past four decades in the United States", moving "about one-for-one with changes in the trend growth rate". The estimates are imprecise, but ignoring the time variation is costly: policymakers' mismeasurement of r* "can cause a significant deterioration in macroeconomic stabilization", which timely updating of r* estimates mitigates.

## Key mechanisms / model

- **Measurement equations**: an output-gap equation (2) — the gap depends on its own two lags and on a moving average of the lagged real funds-rate gap (the ex ante real funds rate minus r*); the sum of lag coefficients must be below one, so persistent shifts in the gap–real rate relation are attributed to r*. A Phillips curve (3) for core PCE inflation with eight lags (summing to one), the lagged gap, and core import and oil import price inflation relative to core PCE; potential output is the output level consistent with unchanged inflation absent relative-price and transitory shocks.
- **Transition equations**: r* = c × trend growth + z (4), where z captures other determinants such as time preference and follows an AR(2) or a random walk (5); potential output is a random walk with drift equal to trend growth (6), and trend growth itself a random walk (7) — potential output is I(2), and if c is nonzero r* is I(1).
- **Estimation (section 3.1)**: quarterly US data 1961:1 to 2000:4. Because the innovations to trend growth and r* are small, maximum likelihood estimates of their standard deviations "were zero" (the "pile-up problem"); the authors instead use Stock and Watson's (1998) median-unbiased estimator for the signal-to-noise ratios λg and λz, via exponential Wald tests for a structural break at an unknown date, in three steps, and estimate the rest by maximum likelihood. Confidence intervals by Hamilton's (1986) Monte Carlo procedure (filter and parameter uncertainty).
- **Ex ante real rate (Appendix)**: funds rate minus expected inflation over the next four quarters from a univariate AR(3) on the previous 40 quarters (the discount rate is used before 1965).
- **Policy experiment (section on monetary policy)**: a rule with the policymaker's r* estimate as intercept (9); if the estimate converges to the wrong value, inflation converges to a level away from target, so for permanent r* shifts the estimate must converge in expectation to the truth. Simulations of the baseline model under the Taylor Rule (both response coefficients .5) with a loss on the variances of the output gap, inflation and half the variance of the change in the funds rate (10), as in Rudebusch and Svensson (1999).

## Main results / findings

- **Signal-to-noise ratios (Table 1)**: for trend growth, Wald statistic 1.51 (just below the 10 percent critical value of 1.55) and λg of .039, implying a standard deviation of trend-growth changes of about 0.1 percentage point a year; for z, Wald statistic 4.28 (significant at 1 percent) and λz of .071 (90 percent interval .015 to .117).
- **One-for-one link with trend growth (Table 2)**: c is .97 (standard error .25) with stationary z and 1.062 in the random-walk baseline (t-statistics not reported there because of possible spurious correlation between two nonstationary processes). The real rate gap enters the output equation with the right sign, significant at 1 percent (coefficient -.104 in the baseline). Log likelihoods cannot discriminate among the specifications.
- **Path of r* (baseline, random-walk z)**: "peaks at about 4-1/2 percent in the mid-1960s, reaches a minimum of 1-1/4 percent in the early 1990s, and ends the sample period at just above its sample average of 3 percent." Trend growth peaks in the mid-1960s at about 3-3/4 percent and falls to about 3 percent in the early 1990s, then rises by about one-half point. The AR(2) version swings much more in the short run, which is why the random walk is preferred (not rejected at 5 percent).
- **Imprecision**: average standard errors of r* range from 1 to 2-1/2 percentage points across specifications; about 1/2 point for trend growth; 2 to 4-1/2 points for potential output.
- **Robustness (Tables 3–4)**: with constant trend growth (λg = 0) c is not identified and r* is much less variable; with λg at its upper bound (0.103) results change little. Adding an equation for private nonfarm hours (Roberts 2001) cuts output-gap uncertainty to less than one fifth of the baseline, gives c of about 0.9, and changes the history — r* low in 1973 and peaking in 1983, and output above potential in the late 1990s — but the authors suspect its precision "may be spurious". In the six variants without hours, r* peaked in 1965 and hit its low in 1992 or 1993.
- **Policy stance (Figure 3)**: allowing for a time-varying r*, policy in the early 1990s "may not have been as expansionary" as a constant r* suggests, and policy in the late 1960s looks much easier.
- **Mismeasurement (Figure 4, Table 5)**: taking the smoothed estimate as truth, the real-time (one-sided) estimate has a measurement-error standard deviation of about 0.9 percentage point, with nearly 10 percent of the error eliminated each quarter; the smoothed r* has a standard deviation of 0.8 point and first-order autocorrelation of 1.00. Under the Taylor Rule over 1964–1997: loss 3.5 with the true r*, 4.7 with the one-sided Kalman filter estimate (34 percent higher), 5.4 assuming a constant 3.0 (53 percent higher). Mismeasurement mostly hurts output stabilization (output-gap standard deviation 1.1 vs. 1.5 and 1.6), with little effect on inflation (1.4, 1.4, 1.6). This contrasts with Rudebusch (2001), who found modest effects with transitory shocks around a known mean and reoptimized rule coefficients (footnote 15).

## Limitations and caveats

- **Symbols lost in tables**: the summation sign in Table 2 and 3 row labels prints as "P ay" and "P dz" (the sum of the lagged output-gap and z coefficients), and the formula for the standard deviation of r* innovations is split over lines. The definition of λz in section 3.1 and footnote 9 is garbled (square-root sign separated). The text of equation (1) in footnote 2 and footnote 3 lost its fraction layout.
- **Table inconsistencies, flagged not corrected**: Table 2's note says σ5 is at an annual rate, Table 3's says σ4. Table 3's Hours log likelihood prints as "-466.51", apparently the value with its footnote marker 1 attached (the note says it is not comparable). Table 2 shows a t-statistic in parentheses under λz in the stationary column, which the note does not explain. Table 4 has dashes for the trend-growth dates in the Low λg column (trend growth is constant there).
- Figures 1–4 survive only as titles and legends (Figure 4 keeps its axis ticks); the paths described above come from the text. The section number for "Monetary Policy and a Time-varying Natural Interest Rate" (section five in the introduction's outline) and the start of the first-page footnote are missing.
- Authors' caveats: the states are measured imprecisely ("as is typical for Kalman filter estimates"); the one-sided estimates use parameters estimated on the full sample, "so the analogy is not exact"; the simulation assumes the policymaker knows the sample mean of r* and the true potential output, isolating only the time-variation component of mismeasurement; a real-bond-rate version and the term premium are left to further research; other countries and other "natural" financial variables are suggested extensions.

## Connections

- [[natural_rate_of_interest]] — the paper's subject: an operational, medium-run definition of r* as the intercept of policy rules, its joint Kalman-filter estimation with potential output and trend growth, and its one-for-one link with trend growth
- [[taylor_rule]] — r* is the rule's intercept; Table 5 measures the loss from using a real-time or constant r* in the Taylor Rule
- [[monetary_policy/synthesis/basic_nk_model_ch3 (Gali, 2015)]] — Galí's flexible-price natural rate is the period-by-period (Woodford) concept that Laubach and Williams contrast with their medium-run, low-frequency one
- [[monetary_policy/synthesis/monetary_policy_design_nk_ch4 (Gali, 2015)]] — optimal rules there track the unobservable natural rate one-for-one; this paper quantifies what its mismeasurement costs a simple rule
- [[monetary_policy/synthesis/taylor_rule (Taylor, 1993)]] — the rule whose intercept the paper reinterprets as a time-varying r* rather than a fixed 2 percent real rate
