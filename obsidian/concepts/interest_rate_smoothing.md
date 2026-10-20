# Interest Rate Smoothing (Policy Inertia)

**Type:** Feature of estimated policy rules / partial adjustment
**Tags:** #interest-rate-smoothing #policy-inertia #partial-adjustment #taylor-rule #gradualism

---

## Definition

The tendency of central banks to move the policy rate toward its desired (target) level gradually rather than at once. In estimated reaction functions it is captured by **partial adjustment**: each period the actual rate closes only a fraction of the gap between the rule's target rate and (a combination of) its own past values, so the lagged policy rate enters the rule with a large coefficient — the smoothing parameter.

## Mechanism

Clarida, Galí & Gertler (2000), equation 3: the actual funds rate equals a weighted combination of the target rate from the forward-looking rule and past funds rates, plus a zero-mean exogenous interest rate shock; the weight on the past is the smoothing parameter. Combined with the target rule it gives a reaction function in which the rate responds to expected inflation and the output gap only by the fraction (one minus the smoothing parameter) within the quarter. The long-run responses are those of the target rule; the short-run ones are scaled down.

Explanations offered in the sources, none established:
- fear of disrupting financial markets (Goodfriend 1991) and uncertainty about the effects of rate changes (Sack 1997), cited by Clarida, Galí & Gertler (2000, footnote 12);
- Brainard-type parameter uncertainty, which dampens the response but, per Clarida, Galí & Gertler (1999), does not explain the partial adjustment of estimated rules;
- leverage over long rates: lagged dependence makes small, persistent moves in short rates move long rates (Rotemberg and Woodford, as presented by Clarida, Galí & Gertler 1999);
- in Clarida, Galí & Gertler (1999) the financial-markets story is spelled out — sharp unanticipated increases can cause capital losses at banks exposed to interest rate risk, which might explain the gradual tightening of 1994 — alongside disagreement among policymakers; "Neither of these alternative stories have been well developed", and why smoothing occurs is "an important unresolved issue".

## When it applies / when it fails

- Empirically robust for the Fed: smoothing parameters of 0.68 pre-Volcker and 0.79 Volcker-Greenspan in Clarida, Galí & Gertler (2000, Table II) — "Only between 10 and 30 percent of a change in the interest rate target is reflected in the Funds rate within the quarter of the change"; their 1999 survey reports 0.76 and 0.66 (Table 1 there). Smoothing was significantly higher under Greenspan than under Volcker at a one-year inflation horizon (0.91 against 0.74, Table VI).
- Why it occurs remains open: Clarida, Galí & Gertler (2000) call it "beyond the scope of this paper", and their 1999 survey lists it among unresolved questions.
- Smoothing changes the short-run response, not the long-run one that matters for the Taylor principle: the determinacy and stabilization comparisons in Clarida, Galí & Gertler (2000) hold the smoothing parameter fixed and vary the long-run inflation coefficient.

## How it appears across sources

| Source | Role |
|---|---|
| [[monetary_policy/synthesis/science_of_monetary_policy (Clarida, Gali & Gertler, 1999)]] | Section 5.2: estimated partial adjustment and its candidate explanations (parameter uncertainty, long-rate leverage, fear of disrupting financial markets, policymaker disagreement); smoothing in the estimated rule (7.3) |
| [[monetary_policy/synthesis/monetary_policy_rules_stability (Clarida, Gali & Gertler, 2000)]] | Partial-adjustment specification (3)–(4) estimated by GMM for the Fed: 0.68 pre-Volcker, 0.79 Volcker-Greenspan; 10 to 30 percent of a target change within the quarter; higher under Greenspan |
| [[monetary_policy/synthesis/policy_rules_real_time_data (Orphanides, 2001)]] | Partial-adjustment Taylor-type and forward-looking reaction functions estimated on real-time and revised data, 1987-1992: "large and tight" smoothing coefficients; on revised data ρ rises with the forecast horizon, partly as a proxy for misspecified inflation and gap terms |
| [[monetary_policy/synthesis/optimal_monetary_policy_inertia (Woodford, 1999)]] | Why inertia can be optimal: with forward-looking agents, small persistent rate changes move long rates and demand; the optimal commitment has intrinsic inertia (inertia coefficient .46 in the calibration) even with serially uncorrelated shocks; a smoothing objective assigned to a discretionary bank recovers more than 99.9 percent of the gain; optimal simple rules are super-inertial (lag coefficient 13.0) |
| [[monetary_policy/synthesis/it_lessons_and_challenges (Minella et al., 2002)]] | BCB reaction function, monthly 1999–2002: "a high degree of interest-rate smoothing", the two Selic lags summing to 0.8 or above |
| [[monetary_policy/synthesis/it_credibility_fx_volatility (Minella et al., 2003)]] | BCB reaction function through 2002:12: lagged Selic coefficient between 0.7 and 0.9 |
| [[monetary_policy/synthesis/it_and_debt_brazil (Favero & Giavazzi, 2004)]] | BCB rule, 2000:01 to 2004:01: persistence of 0.92 on monthly data (Table 3) and 0.994 on daily data |

## BRL / application to the current analysis

The sources linked here say nothing about Brazil yet.

## Connections

- [[taylor_rule]] — estimated rules add the lagged policy rate to the Taylor-type target; the smoothing term is what lets them fit the funds rate quarter by quarter
- [[taylor_principle]] — the principle concerns the long-run inflation response, which smoothing scales over time but does not change
- [[monetary_policy/synthesis/science_of_monetary_policy (Clarida, Gali & Gertler, 1999)]] — candidate explanations and the open question
- [[monetary_policy/synthesis/monetary_policy_rules_stability (Clarida, Gali & Gertler, 2000)]] — the partial-adjustment specification and its estimates for the Fed
- [[monetary_policy/synthesis/policy_rules_real_time_data (Orphanides, 2001)]] — smoothing coefficients estimated with real-time Greenbook data and with revised data
- [[monetary_policy/synthesis/optimal_monetary_policy_inertia (Woodford, 1999)]] — the formal case that policy inertia is a benefit of commitment, not a delay, and the delegated smoothing objective and super-inertial rules that implement it
- [[monetary_policy/synthesis/it_lessons_and_challenges (Minella et al., 2002)]] — smoothing in the BCB's estimated rule
- [[monetary_policy/synthesis/it_credibility_fx_volatility (Minella et al., 2003)]] — smoothing in the BCB's rule including the 2002 crisis
- [[monetary_policy/synthesis/it_and_debt_brazil (Favero & Giavazzi, 2004)]] — Selic persistence in the estimated BCB rule
