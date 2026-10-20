---
aliases: ["Perrelli 2014 - Time-Varying Neutral Interest Rate: The Case of Brazil"]
---

# Time-Varying Neutral Interest Rate — The Case of Brazil — Perrelli & Roache 2014

**Type:** paper (IMF working paper)
**Tags:** #natural-rate #neutral-rate #brazil #emerging-markets #policy-rules #parameter-uncertainty #inflation-targeting
**Source:** IMF Working Paper WP/14/84, Strategy, Policy, and Review and Monetary and Capital Markets Departments (May 2014)
**Language:** English
**Source file:** [[monetary_policy/clean_md/neutral_rate_time_varying_brazil (Perrelli & Roache, 2014)]]

---

## Context and motivation

The neutral rate — the real rate consistent with output at potential and stable inflation — is the benchmark for the policy stance, but it is unobserved, estimated with low confidence, and can shift, especially in emerging markets undergoing rapid structural change. Neutral rates fell across emerging markets after 2002; Brazil had one of the largest declines yet remained the highest in the sample. The paper asks (i) how far and why Brazil's neutral rate fell, triangulating several methods, and (ii) how costly it is for an inflation-targeting central bank to get a moving neutral rate wrong — a question the literature had studied mostly for potential output.

## Core argument / thesis

- Brazil's neutral rate fell substantially over the decade to 2013, for both domestic reasons (lower public debt, lower sovereign risk, a larger supply of saving reflected in financial deepening — the payoff of inflation targeting and fiscal frameworks) and global ones (lower world real rates, a common emerging-market trend).
- No single method is reliable in a fast-changing economy; contrasting structural, filter, yield-curve, state-space and fundamentals-based estimates gives an interval rather than a point.
- Mismeasuring the neutral rate is **not very costly if the policy rule stays activist**: a rule that responds strongly to inflation and the output gap partly corrects the error every period, because the error shows up as gaps the rule reacts to. The danger is the opposite instinct — anchoring policy on the neutral-rate estimate and responding less to outcomes. This contrasts with Orphanides (2002), where activism worsens outcomes under potential-output mismeasurement.

## Key mechanisms / model

**Stylized facts (Section II).** Hodrick–Prescott trends of ex post real policy rates fell across most emerging markets between 2002 and 2011; a principal-components decomposition of real rates in a 17-country sample shows a first component ("common trend") declining over 2002–10 and a cyclical second component that rose with the 2013 taper episode — evidence of global factors, both persistent and transient.

**Structural estimate (Section IV).** The consumption Euler equation of a representative agent with constant relative risk aversion links the neutral rate positively to expected per-capita income growth and the rate of time preference, and negatively (precautionary) to growth volatility. Calibrated to Brazil, it gives a falling but wide range; Brazil's historically high real rates would require implausibly impatient or risk-averse households, so habit persistence is added (calibrated to match the filtered trend), and a modest decline in habit persistence helps explain the fall. The saving channel follows: neutral rates in low-saving countries (Brazil, Turkey, South Africa) are higher than in high-saving ones, so higher household saving would lower Brazil's.

**Econometric estimates (Section V).**
- *Statistical filters* (HP, Ravn–Uhlig, Christiano–Fitzgerald) on ex post real rates for 24 emerging markets. Weaknesses: they cannot separate persistent from long cyclical swings, and two-sided filters have end-point bias.
- *Yield curve*: with anchored expectations the average slope reflects the term premium; adding the "excess" term premium to the trend short real rate backs out a neutral rate. Weakness: needs cyclically neutral end points in a short sample, and futures may price in expected hikes.
- *State space*: short and long nominal rates driven by a latent random-walk neutral rate, expected inflation, the output gap, US Treasury yields (interest parity), Brazil's CDS spread and a term premium.
- *Fundamentals*: cointegrating regressions of the ex ante real policy rate on global rates, inflation gap and surprise, private credit/GDP, public debt/GDP, productivity growth and sovereign risk (long-run equilibrium); and an IS equation (10) in the gaps of domestic and world output, the real rate, the real exchange rate, government consumption and BNDES lending, solved for the short-run equilibrium rate.

**Small monetary model (Section VI).** A four-equation semi-structural open-economy model (Berg, Karam and Laxton): IS curve, Phillips curve with exchange-rate pass-through, uncovered interest parity with a risk premium, and an inertial policy rule whose intercept is the policymaker's estimate of the neutral rate (r**), calibrated to Brazil 2000Q1–2012Q2. The true neutral rate (r*) falls gradually over eight years. Scenarios: (1) the central bank tracks it exactly; (2) its estimate lags two years (too high, so policy is inadvertently tight); (3) its estimate falls too fast (too low, policy too loose). In the mistaken scenarios the rule targets current observed inflation (equation 15), so the bank acts on observables rather than on its own model forecast.

What carries the result: the policy rule's coefficients on inflation and the output gap. Because the bank keeps following its rule, a too-high r** produces a negative gap and below-target inflation, which the rule reads as shocks and offsets; the stronger the response, the smaller the actual real-rate gap (r − r*). With a near-zero response, the neutral-rate error passes almost one-for-one into the stance. A simple linear rule is not certainty-equivalent (Söderlind), so higher uncertainty about r* argues for keeping or raising activism.

## Main results / findings

- **A large fall in Brazil.** Filtered neutral rate: from an average of 9¼ percent in 2002–04 to 3½ percent in 2010–13, "a 575 basis points decline", still the highest in the 24-country sample (Table 2). The consumption model gives about 7¼ percent for 2005–08 and 5¾ percent for 2010–13, 3½ percent once habit persistence is calibrated (Table 1); the yield-curve approach about 4½ percent in the second half of 2013; the state-space model between 3 and 5 percent over the last two years (Figure 5); the long-run fundamentals model 2½ to 3 percent by mid-2013.
- **Which channel wins.** In the fundamentals model the domestic drivers of the decline are lower public debt, lower sovereign risk and financial deepening; inflation performance contributed little since 2007 (the inflation gap did not narrow and surprises were mostly on the upside, Figure 7). Lower global rates contributed about 200 basis points in 2010–13 relative to 2005–08. In the state-space model the estimate is driven mainly by expected inflation, US long yields and the CDS spread (Table 3).
- **Short vs. long run.** The short-run equilibrium rate departs substantially from the long-run one with domestic and world output gaps and the exchange rate; the two met around 4 percent early in 2012, after which the short-run rate was lower (Figure 8). BNDES lending enters the IS gap equation with a positive, significant sign — public lending was procyclical in the sample — while government consumption is not significant (Table 5).
- **Policy simulations.** Mistakes have modest costs: in scenarios 2 and 3 the output gap peaks at about −0.5 and 0.5 percentage points and inflation deviates by about 0.7 points in opposite directions (Figure 10). With an aggressive rule the real-rate gap "hardly diverges from zero"; with a near-passive rule it tracks the neutral-rate error (Figure 11). Even correct tracking (scenario 1) gives a small negative gap because policy inertia slows the cut.

**What would contradict it.** A rule that responds strongly to outcomes but still produces large, persistent gaps when the neutral rate is misjudged; or a fall in Brazil's neutral rate unexplained by debt, risk, saving and global rates.

## Limitations and caveats

- Authors' own: every method is fragile in a rapidly changing emerging market — behavioral parameters are uncertain, filters suffer end-point bias, the yield-curve approach needs cyclically neutral end points and may be circular, the fundamentals regressions have small samples (35 to 44 observations, Table 4) and wide confidence intervals; the simulations change r* holding potential output constant (justified by preference shifts and comparability with the literature), model policymaker beliefs heuristically rather than by learning, and isolate the neutral-rate error from other shocks. Macroprudential measures may affect gap estimates and transmission (footnote 11), not modeled.
- From the text: the favourable verdict on activism depends on the bank continuing to follow its rule and reacting to observable inflation; it does not cover simultaneous mismeasurement of potential output, which is where Orphanides' opposite result comes from. Some estimates use ex post real rates (actual rather than expected inflation) for lack of survey data.
- **Damaged passages.** Equations (1)–(9) (utility, budget constraint, Euler conditions, the habit-persistence condition, and the state-space signal and state equations) are missing from the file; equation (10) and the model equations (11)–(15) survive as scrambled symbols — described in words only. The calibrated parameters said to be "provided in the appendix" are not in the file, nor is the reference list (the file stops at page 29). Figures 1–11 are scrambled axis labels and legends (Figure 1's country labels are partly reversed text); Tables 1–5 and the text tables are readable.

## Connections

- [[natural_rate_of_interest]] — the paper's subject: a time-varying neutral rate for Brazil, its domestic and global determinants, and an interval from several methods
- [[taylor_rule]] — the cost of a mismeasured rule intercept depends on the rule's response to inflation and the output gap; activist rules self-correct neutral-rate errors
- [[real_time_data]] — policy set on a mismeasured unobservable (the neutral rate) and the contrast with Orphanides' result for potential-output mismeasurement
- [[inflation_targeting]] — Brazil's 1999 adoption of inflation targeting, with fiscal frameworks, credited for lower sovereign risk and the fall in the neutral rate
- [[monetary_policy/synthesis/natural_rate_measurement (Laubach & Williams, 2003)]] — the Kalman-filter approach the paper cites as the reference for state-space estimates of the neutral rate
- [[monetary_policy/synthesis/natural_rate_international (Holston, Laubach & Williams, 2017)]] — the advanced-economy counterpart: a falling neutral rate with a large common global component
- [[monetary_policy/synthesis/policy_rules_real_time_data (Orphanides, 2001)]] — the real-time mismeasurement literature whose pessimism about activist rules this paper qualifies for neutral-rate errors
