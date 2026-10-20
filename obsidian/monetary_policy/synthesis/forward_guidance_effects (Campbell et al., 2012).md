---
aliases: ["Campbell 2012 - Macroeconomic Effects of Federal Reserve Forward Guidance"]
---

# Macroeconomic Effects of Federal Reserve Forward Guidance — Campbell, Evans, Fisher & Justiniano 2012

**Type:** paper (with formal comments and general discussion)
**Tags:** #forward-guidance #delphic #odyssean #fomc #zlb #event-study #taylor-rule #dsge
**Source:** The Brookings Institution (Brookings Panel paper; the text prints "Copyright 2012, The Brookings Institution"), with comments by Charles W. Calomiris and Michael Woodford and the general discussion
**Language:** English
**Source file:** [[monetary_policy/clean_md/forward_guidance_effects (Campbell et al., 2012)]]

---

## Context and motivation

With the federal funds rate at the zero lower bound, the FOMC's main remaining tool was statement language about the future path of the rate: "for some time" (December 2008), "an extended period" (March 2009), "at least . . . mid-2013" (August 2011), "late 2014" (January 2012, kept in March 2012). Krugman (1999), Eggertsson and Woodford (2003) and Werning (2012) show that a central bank at the ZLB can stimulate demand today by credibly promising to keep the rate at zero longer than conditions would warrant. The paper asks whether "late 2014" is such a promise or merely a forecast, whether the FOMC can actually move private expectations with words, and whether committing to low rates puts the price stability mandate at risk.

## Core argument / thesis

The paper distinguishes **Delphic** forward guidance — a public forecast of macroeconomic performance and likely policy, based on the policymaker's possibly superior information, which "does not publicly commit the policymaker" — from **Odyssean** forward guidance, which "does publicly commit the policymaker, just as Odysseus committed himself to staying on his ship by having himself bound to the mast." Odyssean guidance faces a time-inconsistency problem: when the time comes, both the FOMC and the public will prefer to ignore the promise, so without an enforcement mechanism policymakers "must rely on their reputations for accuracy and honesty". The authors' claim: the FOMC has long and successfully telegraphed its intended deviations from typical policy, so "communication difficulties do not present an insurmountable barrier to Odyssean forward guidance"; and pairing such guidance with bright-line thresholds for liftoff (Evans's "7/3" rule: liftoff if unemployment falls below 7 percent or medium-term expected inflation rises above 3 percent) can manage the risk to price stability.

## Key mechanisms / model

- **Event study (section I), extending Gürkaynak, Sack, and Swanson (2005; GSS)**: changes in federal funds and Eurodollar futures around FOMC statements are summarized by two rotated factors — a **target factor** that moves the current rate and a **path factor** that moves only expected future rates. Daily data are used (intraday unavailable after 2004), with a risk premium of 1 bp per month added. Extensions: responses of corporate bond yields; responses of Blue Chip consensus forecasts of unemployment and CPI inflation; and a postcrisis sample (statements since August 2007).
- **Identification logic for Delphic content**: if surprises were pure policy shocks, a positive surprise should raise expected unemployment and lower expected inflation (the New Keynesian response). Revisions of the opposite sign mean forecasters read the surprise as news about fundamentals.
- **Rule-based measurement (section II)**: an interest rate rule for the quarterly average policy rate with two lags, the unemployment gap and inflation (equation 1), whose residual is a sum of shocks revealed up to M quarters before they are applied. The contemporaneous shock is the conventional policy disturbance; the others are **forward guidance shocks**. With futures prices and Blue Chip forecasts, each shock is the change in the expected rate for a future quarter corrected for the change in the rule's expected value (equations 2–3). M = 4, set by the Blue Chip horizon; the natural unemployment rate is the Blue Chip long-run forecast. Estimation by GMM with 16 moment restrictions, sample 1996Q1–2007Q2.
- **DSGE policy analysis (section III)**: a medium-scale New Keynesian model of the Chicago Fed, adapted from Justiniano, Primiceri, and Tambalotti (2011): sticky wages and prices with partial indexation, habit, investment adjustment costs, variable capacity utilization, a financial accelerator, eight structural shocks, and a policy rule with a time-varying inflation anchor and forward guidance shocks given the GSS target/path factor structure. Within the model forward guidance is "entirely Odyssean". Estimated over 1989Q2–2007Q2 with guidance 4 quarters out; forward guidance re-estimated over 2007Q3–2011Q4 with guidance 10 quarters out, after calibrating a more persistent discount shock (slow deleveraging), an inflation-anchor variance of one-fourth its precrisis estimate, and an output gap coefficient three times the precrisis estimate.

## Main results / findings

**Event study, precrisis (Tables 1–3).**
- Replicating GSS over February 1990 – June 2007 (September 2001 omitted): the path factor accounts for only 14 percent of the variance of next quarter's expected rate, about 50 percent at 2 quarters, and the clear majority for the two longest contracts. GSS's two factors explain more than 90 percent of the variation in the contracts.
- Asset prices (Table 2): GSS report that a 100-bp target factor raises 2-, 5- and 10-year Treasury yields by 41, 37 and 28 bp. In the authors' estimates all factor slopes on Treasuries are positive and significant at the 1 percent level in the longer sample. On long-term Aaa/AAA and Baa/BBB corporate yields the target factor "has no detectable influence", while a 100-bp path factor raises both by about 30 to 35 bp — forward guidance moves the rates relevant for investment.
- Private forecasts (Table 3): the statistically significant responses "all have the sign opposite to that predicted by the standard New Keynesian model": the target factor's coefficients on unemployment forecasts are significant and negative at all four horizons in the longer sample, and only 3 of the 16 inflation coefficients are negative (none significant). The authors read GSS surprises as having "a substantial Delphic component".

**Event study, postcrisis (Tables 4–7).** Statements following every FOMC meeting since August 2007 (39) plus the November 25, 2008 press release announcing QE1. The QE1 announcement of March 18, 2009 is an outlier — the 10-year yield fell 51 bp while the path factor rose 32 bp (markets read it as an earlier liftoff) — and is dropped. The path factor now dominates only expected rates 4 or more quarters ahead. Asset price responses "strongly resemble those from before the crisis", a "striking finding" given the change in conditions; forecast responses are too imprecise for conclusions (no coefficient in Table 7 is significant). Woodford's comment summarizes the variance shares: the path factor accounts for 67 percent of the expected rate 2 quarters out and 90 percent 4 quarters out (February 1994 – June 2007), and 53 percent 4 quarters out and 79 percent 6 quarters out (August 2007 – December 2011).

**Rule-based forward guidance (1996Q1–2007Q2).**
- The estimated rule has hump-shaped dynamics (second-order autoregression) and satisfies the Taylor principle; the J statistic is 0.25.
- The standard deviation of the 4-quarter-ahead forward guidance shock is only 9 bp; that of the rule's total residual is 30 bp, of which the anticipated component is 28 bp. Standard deviations by horizon: 12, 20, 13, 11 and 9 bp. About 40 percent of policy variance is communicated in the quarter before and another 40 percent 1 to 3 quarters before — about 80 percent in all (Conclusion).
- One factor ("policy acceleration") explains about 60 percent of the 4-quarter-ahead shock but little at shorter horizons (loadings 5, 6, 4, -3 and -7 bp); its minimum of -21 bp in 2002Q2, when unemployment forecasts rose 30 bp, shows the FOMC signalling accelerated accommodation after the 2001 recession.
- Asset prices (Table 8): a 100-bp shock to next quarter's rule residual raises 2- and 5-year Treasury yields by almost 200 bp and the 10-year by about 150 bp; corporate yields by 65 and 69 bp — much larger than the GSS estimates. The authors find this "puzzling" and suggest forward guidance shocks affect term premiums.
- Forecasts (Table 9): positive forward guidance shocks again lower expected unemployment (several significant coefficients on the one-quarter-ahead shock). The authors interpret this as **history-dependent** policy: the FOMC "reacts more aggressively to economic weakness revealed only shortly before its onset than to weakness foreseen 4 quarters in advance" (augmented rule, equation 4).

**DSGE scenarios (Figures 5–8).** The model sees the ZLB binding from 2008Q4 to 2011Q4. The baseline fits futures through mid-2014 and lifts the funds rate to about 1 percent at the end of 2014; hours per capita remain 10 log points below steady state. Two upside risks starting 2012Q1:
- *Faster deleveraging* (discount-shock persistence from 0.95 to 0.75; half-life from 3.4 years to 2.4 quarters): unemployment crosses the 7 percent threshold in 2012Q3 and inflation reaches 3 percent in late 2013, so the 7/3 rule would dictate liftoff in late 2012 — the threshold works as insurance.
- *Higher expected inflation* (long-run expectations up 1 percentage point, a shock of more than 4 standard deviations): neither threshold is crossed within 3 years, because the estimated price Phillips curve is "very flat" — its slope is "about an order of magnitude smaller than single-equation estimates".

**Comments and discussion.**
- *Calomiris*: nothing in the Fed's guidance is a commitment — its language "anticipates" but does not promise. The market reactions can be explained by guidance revealing the FOMC's shifting objectives or its beliefs about the natural rate of unemployment (which "may be 5 percent or it may be 7 percent" after a deep recession). He opposes further easing even with a 7/3 rule and argues for phased-in higher reserve requirements.
- *Woodford*: the rule-based shocks are forward guidance only if the authors' Taylor rule is the public's true model of the reaction function; under the history-dependent rule (equation 4) the residual picks up forecast revisions with no true shift in policy. Eggertsson and Woodford (2003) argue for a state-contingent commitment, not a fixed date. The 7/3 rule is "purely forward-looking", so it lacks the key feature of the optimal commitment — making up for target misses caused by the ZLB; a target path for a gap-adjusted price level or for nominal GDP comes closer.
- *General discussion*: Blinder recalls the FOMC looking at as many as a dozen Taylor-rule variants whose prescriptions differed across 150 basis points; Meyer surveyed 100 market participants, 98 of whom read the guidance as a forecast; Swanson notes the Odyssean component is measured as a residual, "whatever was not Delphic was identified as Odyssean by default".

## Limitations and caveats

- **Tables lost their structure.** Tables 1 and 5 (variance decompositions) survive only as titles, row labels and notes — none of their percentages is in the file; the shares quoted above come from the text and from Woodford's comment. Tables 2, 3, 6 and 7 are columns of coefficients with the row (asset/horizon) and column labels lost, so individual entries cannot be attributed; Table 8 keeps its column labels but not the asset names. Table 4 (postcrisis statements) is missing several dates and statement fragments.
- **Equations 1–7 are garbled** into scattered symbols, including the estimated interest rate rule, whose coefficients appear only as detached digits; none of its coefficients can be read. The sample correlation matrix of the shocks is likewise garbled. The models are described in words above.
- Text is cut at several points: the Introduction sentence on Evans's threshold proposal, the Gagnon et al. (2010) sentence in I.B, the sentence after "Werning" in III.C, the Conclusion sentence restating the 7/3 rule, and Woodford's footnote 2. Figures 1–8 survive only as captions and axis ticks.
- The text says the GMM provides "16 moment restrictions to estimate 4 parameters" while listing five parameters (µ, ρ1, ρ2, φπ, φu); flagged as written.
- The authors' own caveats: postcrisis forecast regressions too imprecise; the DSGE conclusions depend on model structure and on assuming the policy rule's credibility and price setting invariant to inflation expectations; only upside risks were simulated (Kiley, in the discussion). One author regularly attends FOMC meetings (footnote 1), which Calomiris raises.

## Connections

- [[forward_guidance]] — the paper's subject: defines Delphic vs. Odyssean guidance, measures its effects on futures, Treasury and corporate yields and private forecasts, and simulates threshold-based guidance at the ZLB
- [[taylor_rule]] — estimates a rule with anticipated residuals to identify forward guidance shocks; the discussion questions whether a single known Taylor rule exists (Blinder, Romer, Woodford)
- [[nk_phillips_curve]] — the estimated DSGE's very flat price Phillips curve is why a 1-percentage-point rise in inflation expectations barely moves inflation over 3 years
- [[information_effect]] (proposed) — the "wrong-sign" response of private forecasts to policy surprises, read as Delphic information about fundamentals
- [[time_inconsistency]] (proposed) — why Odyssean promises need reputation to be credible (Kydland and Prescott 1977), and the commitment-vs-discretion debate in the comments
- [[zero_lower_bound]] (proposed) — the constraint that makes forward guidance the main remaining tool, and the Eggertsson–Woodford case for keeping rates at zero longer
- [[monetary_policy/synthesis/basic_nk_model_ch3 (Gali, 2015)]] — the "correct sign" benchmark the paper tests against is the NK model's response to an exogenous policy shock (falling output and inflation after a tightening)
