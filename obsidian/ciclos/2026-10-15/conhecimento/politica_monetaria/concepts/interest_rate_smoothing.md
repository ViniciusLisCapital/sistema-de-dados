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
| [[monetary_policy/synthesis/policy_rules_real_time_data (Orphanides, 2001)]] | Partial-adjustment Taylor-type and forward-looking reaction functions estimated on real-time and revised data, 1987-1992: "large and tight" smoothing coefficients; on revised data ρ rises with the forecast horizon, partly as a proxy for misspecified inflation and gap terms |
| [[monetary_policy/synthesis/it_lessons_and_challenges (Minella et al., 2002)]] | BCB reaction function, monthly 1999–2002: "a high degree of interest-rate smoothing", the two Selic lags summing to 0.8 or above |
| [[monetary_policy/synthesis/it_credibility_fx_volatility (Minella et al., 2003)]] | BCB reaction function through 2002:12: lagged Selic coefficient between 0.7 and 0.9 |

## BRL / application to the current analysis

The sources linked here say nothing about Brazil yet.

## Connections

- [[taylor_rule]] — estimated rules add the lagged policy rate to the Taylor-type target; the smoothing term is what lets them fit the funds rate quarter by quarter
- [[taylor_principle]] — the principle concerns the long-run inflation response, which smoothing scales over time but does not change
- [[monetary_policy/synthesis/policy_rules_real_time_data (Orphanides, 2001)]] — smoothing coefficients estimated with real-time Greenbook data and with revised data
- [[monetary_policy/synthesis/it_lessons_and_challenges (Minella et al., 2002)]] — smoothing in the BCB's estimated rule
- [[monetary_policy/synthesis/it_credibility_fx_volatility (Minella et al., 2003)]] — smoothing in the BCB's rule including the 2002 crisis
