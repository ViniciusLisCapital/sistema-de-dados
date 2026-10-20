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
| [[monetary_policy/synthesis/policy_rules_real_time_data (Orphanides, 2001)]] | The rule rebuilt with data available in real time (1987-1992): real-time prescriptions were consistently below the funds rate and fit worse (standard deviation 68 basis points against 52 with revised data); within-year revisions exceed the quarterly change in the funds rate; real-time forward-looking rules fit better than Taylor's contemporaneous rule |
| [[monetary_policy/synthesis/sticky_wages_prices_ch6 (Gali, 2015)]] | Rule (23) with φp = 1.5 and φy = 0.125 in the monetary shock experiment; simple rules it = 0.01 + 1.5πt on price, wage or composite inflation ranked by welfare loss (Table 6.1) |
| [[monetary_policy/synthesis/unemployment_nk_model_ch7 (Gali, 2015)]] | Taylor rule (17) compared with the optimal policy: unemployment rises strongly after a technology shock and demand shocks are not offset; a rule responding to unemployment, it = 0.01 + 1.5πp − 0.5u (22), fits the Fed 1987–2008 and tracks the optimum much better |
| [[monetary_policy/synthesis/open_economy_monetary_policy_ch8 (Gali, 2015)]] | Open-economy Taylor-type rule (39); flexible domestic and CPI inflation rules with Taylor (1993) coefficients give the largest welfare losses among the rules in Table 8.1 (0.61 and 0.43) |
| [[monetary_policy/synthesis/inflation_forecast_targeting (Svensson, 1997)]] | The optimal reaction function under inflation forecast targeting (2.13) has the Taylor form but responds to an exogenous variable too, with coefficients that generally differ from 0.5; commitment to a target rule is preferred to commitment to the Taylor rule (Section 8) |
| [[monetary_policy/synthesis/optimal_monetary_policy_inertia (Woodford, 1999)]] | Estimated Taylor-type targets with partial adjustment (1.1)–(1.2) as the starting fact; a generalized rule with the lagged rate (5.3) implements the near-optimal plan, and the optimal one responding only to inflation and the lagged rate is super-inertial (coefficients 46.1 and 13.0) |
| [[monetary_policy/synthesis/neutral_rate_time_varying_brazil (Perrelli & Roache, 2014)]] | Small model calibrated to Brazil: when the rule's intercept (the neutral-rate estimate) is wrong, an activist rule responding strongly to inflation and the output gap self-corrects and keeps the real-rate gap near zero; a passive rule passes the error into the stance |
| [[monetary_policy/synthesis/it_lessons_and_challenges (Minella et al., 2002)]] | Forward-looking Taylor-type rule for the BCB, 1999–2002, on the expected deviation of inflation from target (Inflation Report or market forecasts), the output gap and two Selic lags; the output gap is insignificant or wrong-signed and the exchange rate insignificant |
| [[monetary_policy/synthesis/it_credibility_fx_volatility (Minella et al., 2003)]] | The BCB reaction function re-estimated through 2002:12 with the 12-month exchange rate change added; the output gap comes out wrong-signed, explained by supply shocks (electricity rationing) that raise inflation and cut output at once |
| [[monetary_policy/synthesis/it_and_debt_brazil (Favero & Giavazzi, 2004)]] | A smoothed rule on one-year-ahead expected inflation alone describes BCB policy after the float (output gap and exchange rate add nothing); simulated forward to predict the Selic path and extract term premia from swap yields |

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
- [[monetary_policy/synthesis/policy_rules_real_time_data (Orphanides, 2001)]] — the informational burden of the rule: real-time output gaps and inflation, revisions to the prescription, and what estimated rules look like on real-time data
- [[monetary_policy/synthesis/sticky_wages_prices_ch6 (Gali, 2015)]] — Taylor-type rules on price, wage or composite inflation evaluated with sticky wages
- [[monetary_policy/synthesis/unemployment_nk_model_ch7 (Gali, 2015)]] — the case for adding unemployment to a Taylor-type rule
- [[monetary_policy/synthesis/open_economy_monetary_policy_ch8 (Gali, 2015)]] — Taylor rules in domestic vs. CPI inflation in a small open economy
- [[monetary_policy/synthesis/inflation_forecast_targeting (Svensson, 1997)]] — the Taylor rule as an instrument rule, against a target rule on the inflation forecast
- [[monetary_policy/synthesis/optimal_monetary_policy_inertia (Woodford, 1999)]] — inertial generalizations of the Taylor rule that implement the optimal commitment
- [[monetary_policy/synthesis/neutral_rate_time_varying_brazil (Perrelli & Roache, 2014)]] — why rule activism, not a better neutral-rate estimate, limits the cost of a mismeasured intercept
- [[monetary_policy/synthesis/it_lessons_and_challenges (Minella et al., 2002)]] — an estimated reaction function for the BCB in the first years of inflation targeting
- [[monetary_policy/synthesis/it_credibility_fx_volatility (Minella et al., 2003)]] — why an estimated rule can show a negative output-gap response when supply shocks dominate
- [[monetary_policy/synthesis/it_and_debt_brazil (Favero & Giavazzi, 2004)]] — an estimated BCB rule used both to forecast policy rates and as the monetary block of a fiscal-dominance model
