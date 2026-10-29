# Output Gap

**Type:** Unobservable state variable / measure of the business cycle
**Tags:** #output-gap #potential-output #business-cycle #detrending

---

## Definition

The difference between actual output (GDP) and potential output. In practice potential is estimated as a trend, and the gap is the deviation of (log) GDP from it. This statistical gap is not the New Keynesian one — the deviation of output from what would prevail with fully flexible prices and wages — which is theoretically preferable but much harder to measure (Cusinato, Minella & Pôrto Júnior).

## Mechanism / estimation

- **Role in policy**: the gap summarizes actual versus potential growth; a positive gap "may call for a monetary policy reaction", which is how it enters rules such as the Taylor rule (Cusinato et al.).
- **Common estimators**: the Hodrick-Prescott filter (the smoothing parameter sets how closely potential follows GDP — towards a linear trend as it grows, towards a zero gap as it falls), linear and quadratic trends fitted to log GDP, and unobserved-components models such as Harvey-Clark (potential a random walk with drifting drift, gap an AR(2), estimated with the Kalman filter). Production-function methods use unemployment and capacity utilization instead (Cusinato et al.).
- **Why the latest estimate is fragile**: it moves when GDP is revised and when new quarters change the estimated trend at the end of the sample — the end-point problem of filters and trends.

## When it applies / when it fails

- It is least reliable exactly when it is needed: at the end of the sample, in real time. Revisions are large for every trend method and persistent, so a wrong reading of the cycle tends to last several quarters (Cusinato et al.).
- Different methods give gaps with strong short-run co-movement but different amplitude and, often, different signs; the size of a method's revisions does not show which is closer to the truth, because the final estimates' own errors are unknown (Cusinato et al.).
- The authors' remedies: use the gap with great caution, read it alongside a broad set of activity indicators, and evaluate past policy with the gap as it was estimated at the time.

## How it appears across sources

| Source | Role |
|---|---|
| [[economic_activity/synthesis/output_gap_brazil_real_time (Cusinato, Minella & Porto Junior, 2013)]] | Brazil, 1996Q1-2008Q2: real-time HP, linear-trend, quadratic-trend and Harvey-Clark gaps compared with their final values; the sign is wrong in 30 percent of quarters for HP and HC and 44 percent for the quadratic trend (Table 12); revisions come from both GDP revisions and the end-of-sample effect, which drives their persistence |

## BRL / application to the current analysis

Cusinato et al. measure the problem on Brazilian GDP: real-time gaps are revised less than in US, Canadian and Norwegian studies but still enough to flip the sign often, and much of the revision bias came from the IBGE's 2006Q4 methodological change.

## Connections

- [[real_time_data]] — the gap is the variable most damaged by data revisions and end-of-sample uncertainty
- [[taylor_rule]] — the rule that turns the gap into an interest-rate prescription
- [[economic_activity/synthesis/output_gap_brazil_real_time (Cusinato, Minella & Porto Junior, 2013)]] — four detrending methods and the size and sources of their real-time revisions in Brazil
