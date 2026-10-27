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
| [[monetary_policy/synthesis/policy_rules_real_time_data (Orphanides, 2001)]] | The rule rebuilt with data available in real time (1987-1992): real-time prescriptions were consistently below the funds rate and fit worse (standard deviation 68 basis points against 52 with revised data); within-year revisions exceed the quarterly change in the funds rate; real-time forward-looking rules fit better than Taylor's contemporaneous rule |
| [[monetary_policy/synthesis/inflation_forecast_targeting (Svensson, 1997)]] | The optimal reaction function under inflation forecast targeting (2.13) has the Taylor form but responds to an exogenous variable too, with coefficients that generally differ from 0.5; commitment to a target rule is preferred to commitment to the Taylor rule (Section 8) |
| [[monetary_policy/synthesis/neutral_rate_time_varying_brazil (Perrelli & Roache, 2014)]] | Small model calibrated to Brazil: when the rule's intercept (the neutral-rate estimate) is wrong, an activist rule responding strongly to inflation and the output gap self-corrects and keeps the real-rate gap near zero; a passive rule passes the error into the stance |
| [[monetary_policy/synthesis/it_lessons_and_challenges (Minella et al., 2002)]] | Forward-looking Taylor-type rule for the BCB, 1999–2002, on the expected deviation of inflation from target (Inflation Report or market forecasts), the output gap and two Selic lags; the output gap is insignificant or wrong-signed and the exchange rate insignificant |
| [[monetary_policy/synthesis/it_credibility_fx_volatility (Minella et al., 2003)]] | The BCB reaction function re-estimated through 2002:12 with the 12-month exchange rate change added; the output gap comes out wrong-signed, explained by supply shocks (electricity rationing) that raise inflation and cut output at once |

## BRL / application to the current analysis

The sources linked here say nothing about Brazil yet.

## Connections

- [[nk_phillips_curve]] — the rule closes the NKPC + DIS block
- [[natural_rate_of_interest]] — the rule's stance is judged against the natural rate
- [[fiscal_dominance]] — Selic vs. Taylor Rule is one of the detection signals listed there
- [[monetary_policy/synthesis/policy_rules_real_time_data (Orphanides, 2001)]] — the informational burden of the rule: real-time output gaps and inflation, revisions to the prescription, and what estimated rules look like on real-time data
- [[monetary_policy/synthesis/inflation_forecast_targeting (Svensson, 1997)]] — the Taylor rule as an instrument rule, against a target rule on the inflation forecast
- [[monetary_policy/synthesis/neutral_rate_time_varying_brazil (Perrelli & Roache, 2014)]] — why rule activism, not a better neutral-rate estimate, limits the cost of a mismeasured intercept
- [[monetary_policy/synthesis/it_lessons_and_challenges (Minella et al., 2002)]] — an estimated reaction function for the BCB in the first years of inflation targeting
- [[monetary_policy/synthesis/it_credibility_fx_volatility (Minella et al., 2003)]] — why an estimated rule can show a negative output-gap response when supply shocks dominate
