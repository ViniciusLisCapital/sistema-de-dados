---
aliases: ["Blanchard & Perotti 2002 - Dynamic Effects of Government Spending and Taxes on Output"]
---

# An Empirical Characterization of the Dynamic Effects of Changes in Government Spending and Taxes on Output — Olivier Blanchard & Roberto Perotti 2002

**Type:** paper
**Tags:** #fiscal-multiplier #svar #fiscal-shocks #identification #automatic-stabilizers #us
**Source:** NBER Working Paper No. 7269, July 1999 (the version in the file; the tracker dates the paper 2002)
**Language:** English
**Source file:** [[fiscal_policy/clean_md/empirical_characterization_fiscal_shocks (Blanchard & Perotti, 2002)]]

---

## Context and motivation

Large macroeconometric models "largely postulate rather than document" an effect of fiscal policy on activity, and reduced-form studies look at one summary statistic (a cyclically adjusted deficit) or at spending or taxes alone — which implicitly assumes the excluded fiscal variable is uncorrelated with the included one. The paper does for fiscal policy what structural VARs had done for monetary policy: identify exogenous spending and tax shocks in postwar U.S. data and trace their dynamic effects on output and its components.

## Core argument / thesis

A structural VAR is better suited to fiscal than to monetary policy, for two reasons: budget variables move for many reasons other than output stabilization, so exogenous fiscal shocks exist; and decision and implementation lags mean that within a quarter there is little or no discretionary fiscal response to unexpected activity. So the within-quarter response of taxes and spending to output is only the **automatic** one, which can be built from institutional information on the tax and transfer systems. Removing it identifies the fiscal shocks. The results: spending shocks raise output, tax shocks lower it, multipliers are small (often close to one), and — the non-standard finding — both tax increases and spending increases crowd out investment.

## Key mechanisms / model

- **The VAR.** Quarterly log real per-capita net taxes (taxes minus transfers, including interest), government purchases (consumption plus investment) and GDP, with four lags whose coefficients may depend on the quarter, because collection lags (corporate taxes especially) make the response of revenue to GDP seasonal in a way that seasonal adjustment does not remove. Trends are treated either as deterministic (DT, quadratic) or stochastic (ST, unit root with slowly changing drift, removed with a one-sided filter so future events do not contaminate today's trend). Benchmark sample 1960:1–1997:4.
- **Identification, three steps** (equation 2):
  1. The output elasticity of net taxes (a1) is built outside the VAR as a weighted sum, over tax and transfer categories, of the elasticity of each tax to its base times the elasticity of the base to GDP, extending the OECD's annual elasticities (Giorno et al.) to quarterly frequency. Quarterly and annual elasticities can differ a lot (profits to GDP: 4.50 quarterly against 2.15 annual). No automatic response of purchases to activity was found, so b1 = 0. The average a1 over 1947:1–1997:4 is 2.08, rising over time.
  2. Cyclically adjusted tax and spending residuals are no longer correlated with the output shock and serve as instruments for the effects of taxes and spending on output within the quarter.
  3. Whether taxes respond to spending or the reverse cannot be identified, so both orderings are estimated; the correlation between the adjusted innovations is low, so the ordering hardly matters.
- **Event study for large shocks.** Changes too large to come from the same stochastic process — the 1975:2 temporary tax rebate, the Korean War buildup and early-1950s tax changes — are handled with dummies, and the response to the dummy is compared with the response to estimated shocks.
- **Assumptions that carry the result:** no discretionary fiscal response within a quarter (fails with annual data); the tax-base–GDP relation invariant to the type of shock (fine for broad income taxes, doubtful for profits); and shocks **unanticipated** by the private sector — which the authors call "particularly problematic here" since most tax and transfer changes are known quarters ahead.

## Main results / findings

- **Within the quarter (Table 2, DT):** a dollar of spending raises GDP by 0.96 dollars and a dollar of taxes lowers it by 0.87. The negative tax effect depends on the instrument: the raw correlation between unadjusted tax and output innovations is positive (0.38).
- **Tax shocks:** output falls on impact and keeps falling, with a trough multiplier of 0.78 after 5 quarters under DT and a larger, more persistent one (-1.33 after 7 quarters) under ST. The 1975:2 rebate gives very similar responses (peak multipliers 0.75 DT and 1.02 ST), reached sooner because that cut lasted one quarter.
- **Spending shocks:** persistent; GDP rises 0.84 on impact under DT, peaking at 1.29 after almost four years; under ST the peak (0.90) is on impact and the response turns insignificant after four quarters. Which multiplier is larger, tax or spending, depends on the specification. Shutting off the endogenous rise in taxes raises the spending response somewhat.
- **Robustness:** the sign is robust; the size is not. Dropping one decade at a time moves the DT tax multiplier from -0.49 (without the eighties) to -1.45 (without the nineties) and the ST spending multiplier from 0.62 to 1.80; varying a1 by ±0.5 changes impact and peak tax effects by up to 0.5–0.8; quarter dependence and cointegration change little.
- **No anticipation effect of the 1975:2 cut:** leads of the dummy pick up negative GDP residuals before the cut, not anticipatory gains.
- **The 1950s:** with dummies for 1950:1–1953:1, normal-shock multipliers look like the post-1959 ones; the composite Korean War path implies larger effects (peak output over peak spending more than 2.5 under DT, 1.5 under ST). Splitting spending, DT gives large and similar defense and non-defense multipliers (2.50 and 2.67), but the non-defense result is not robust to ST, which the authors cannot explain.
- **Components (Table 9, text):** taxes crowd out consumption and investment; spending crowds in consumption (peak 1.26 under DT) and crowds out investment strongly (peak effect of 1 under DT); exports and imports both fall after an initial rise. Since both spending and taxes cut investment, a balanced-budget expansion has "a strong negative effect on investment" — inconsistent with a standard Keynesian model, in which spending and taxes have opposite effects on investment. The investment and import responses are left unexplained.

## Limitations and caveats

- The authors' own: identification assumes unanticipated shocks; the a1 elasticity is an outside construction and quarter dependence is held fixed even though collection lags shifted slightly ("our adjustment is better than none, but still not quite right"); inflation is not controlled for although much spending is set in nominal terms; the counterfactuals ignore the Lucas critique and violate the intertemporal budget constraint.
- Magnitudes vary across trend specifications and subsamples, and standard-error bands are wide (output response to spending insignificant after four quarters under ST).
- U.S. only; general government; net taxes include interest payments and transfers, so "taxes" is a broad aggregate.
- **Damaged passages:** equations (1), (2), (3) and (5) are garbled — symbols for shocks and elasticities lost or replaced by stray characters; in Tables 3, 4, 6, 7, 8 and 9 minus signs appear as underscores or are missing and some cells are misplaced (Table 3 prints the DT and ST tax responses of GDP without the negative signs the text gives), so only magnitudes stated in the text are reliable; Table 5 has cells missing; Figures 1–9 survive only as scattered axis labels. The file is the 1999 working paper and contains no reference list.

## Connections

- [[fiscal_multiplier]] — the SVAR estimates of spending and tax multipliers for the U.S. and their sensitivity to trends, subsamples and elasticities; the investment crowding-out result
- [[structural_fiscal_balance]] — the cyclical adjustment of net taxes through tax-base and base-to-GDP elasticities, here built at quarterly frequency to identify fiscal shocks; shows how much quarterly and annual elasticities differ
- [[fiscal_foresight]] (proposed) — the authors flag anticipation as the weak point of their identification and test it only with leads of the 1975:2 dummy
- [[fiscal_policy/synthesis/can_government_purchases_stimulate_economy (Ramey, 2011)]] — Ramey's survey places this paper's spending multiplier within the range of U.S. aggregate estimates and criticizes SVAR methods for ignoring anticipated spending changes
