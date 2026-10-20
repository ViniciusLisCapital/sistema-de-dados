# Taylor Rule

**Type:** Policy rule
**Tags:** #taylor-rule #policy-rule #monetary-policy #interest-rate

---

## Definition

A simple interest rate rule in which the policy rate responds systematically to inflation and to the output gap (or detrended output). Taylor (1993, 1999) proposed it as a good description of the federal funds rate under Greenspan. Not to be confused with the Taylor principle, the stability condition on the rule's inflation coefficient.

## Formal statement

Taylor's original rule, as Galí prints it: `i = 4 + 1.5(πt − 2) + 0.5(yt − y∗t)`, with i the annualized federal funds rate, π year-on-year inflation and y∗ trend log GDP — implicitly a 2 percent inflation target and a 2 percent steady-state real rate. In the basic New Keynesian model the rule is written with an intercept equal to the discount rate, coefficients φπ and φy on inflation and output, and an exogenous policy shock; empirical rules are estimated in annual rates, so in a quarterly model the output coefficient is divided by 4 (Galí's calibration: φπ = 1.5, φy = 0.5/4).

## When it applies / when it fails

- In the basic NK model the rule yields a unique equilibrium only if its coefficients satisfy a determinacy condition (Galí's (28)); see the Taylor principle.
- A rule that responds to output rather than to the output gap responds to movements in natural output too, which matters after technology shocks (Galí).

## How it appears across sources

| Source | Role |
|---|---|
| [[monetary_policy/synthesis/basic_nk_model_ch3 (Gali, 2015)]] | Closes the basic NK model (26); original rule in footnote 5; quarterly calibration; equilibrium responses to policy, preference and technology shocks under the rule |
| [[monetary_policy/synthesis/forward_guidance_effects (Campbell et al., 2012)]] | Estimated rule (1996Q1–2007Q2) whose anticipated residuals identify forward guidance shocks; discussion on whether a single known Taylor rule exists |
| [[monetary_policy/synthesis/taylor_rule (Taylor, 1993)]] | The original: equation (1) with a 2 percent inflation target and 2 percent real rate, its fit to the federal funds rate in 1987-1992, and its proposed use as an FOMC input rather than a mechanical formula |
| [[monetary_policy/synthesis/monetary_policy_design_nk_ch4 (Gali, 2015)]] | Simple rule (19) with Taylor's quarterly calibration (φπ = 1.5, φy = 0.125); welfare evaluation against inflation-only and output-heavy variants (Table 4.1) and against constant money growth (Table 4.2) |
| [[monetary_policy/synthesis/science_of_monetary_policy (Clarida, Gali & Gertler, 1999)]] | Taylor's rule checked against optimal-policy principles; forward-looking version with smoothing estimated by GMM — inflation coefficient 0.80 pre-Volcker vs. 1.96 Volcker-Greenspan (Table 1) |
| [[monetary_policy/synthesis/monetary_policy_rules_stability (Clarida, Gali & Gertler, 2000)]] | Forward-looking rule nesting Taylor's, with partial adjustment, estimated by GMM 1960–1996; robust split between pre-Volcker and Volcker-Greenspan coefficients, also in a backward-looking Taylor-type version (Table VII) |
| [[monetary_policy/synthesis/natural_rate_measurement (Laubach & Williams, 2003)]] | Reads the rule's intercept as a time-varying natural rate; using a real-time or constant r* in the Taylor Rule raises the loss by 34 and 53 percent (Table 5) |

## BRL / application to the current analysis

The sources linked here say nothing about Brazil yet.

## Connections

- [[nk_phillips_curve]] — the rule closes the NKPC + DIS block
- [[natural_rate_of_interest]] — the rule's stance is judged against the natural rate
- [[fiscal_dominance]] — Selic vs. Taylor Rule is one of the detection signals listed there
- [[monetary_policy/synthesis/basic_nk_model_ch3 (Gali, 2015)]] — the rule in the basic New Keynesian model
- [[monetary_policy/synthesis/forward_guidance_effects (Campbell et al., 2012)]] — forward guidance measured as anticipated deviations from an estimated interest rate rule; Blinder's dozen Taylor-rule variants
- [[monetary_policy/synthesis/taylor_rule (Taylor, 1993)]] — the paper that proposed the rule, as a representative of research on rules and as a description of Fed policy, to be operated with judgment
- [[monetary_policy/synthesis/monetary_policy_design_nk_ch4 (Gali, 2015)]] — welfare-based evaluation of the rule as a simple rule; an aggressive inflation-only version approximates the optimal policy
- [[monetary_policy/synthesis/science_of_monetary_policy (Clarida, Gali & Gertler, 1999)]] — the rule as a robust simple rule, and estimates showing the pre-Volcker Fed responding less than one-for-one to expected inflation
- [[monetary_policy/synthesis/monetary_policy_rules_stability (Clarida, Gali & Gertler, 2000)]] — forward-looking and backward-looking estimated rules for the Fed, before and after 1979
- [[monetary_policy/synthesis/natural_rate_measurement (Laubach & Williams, 2003)]] — the intercept of the rule as an estimated, time-varying r*
