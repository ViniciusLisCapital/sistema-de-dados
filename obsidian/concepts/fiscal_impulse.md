# Fiscal Impulse

**Type:** Fiscal stance indicator (demand side)
**Tags:** #fiscal-impulse #fiscal-stance #output-gap #procyclicality

---

## Definition

The contribution of fiscal policy to aggregate demand over a period, measured as the negative of the change in the cyclically adjusted primary balance: a falling adjusted balance is an expansionary (positive) impulse, a rising one a contractionary (negative) impulse. Compared with the output gap, it classifies the stance as countercyclical (expansion with a negative gap, contraction with a positive gap) or procyclical (the other two combinations).

## Mechanism

- The balance is adjusted for the cycle first, so that revenue moving with activity is not mistaken for policy.
- One-offs are **not** removed in the impulse measure used by the SPE (unlike the [[structural_fiscal_balance]]): a one-off payment still injects demand in the year it is paid.
- The impulse of year t is set against the output gap at the end of t-1, not the contemporaneous gap, because the current gap already contains the effect of the current year's fiscal policy.

## When it applies / when it fails

- **It is a top-down measure.** It ignores the composition of the change in spending and revenue and their different multipliers; a reduction in the deficit through investment cuts and one through tax increases count the same (SPE-MF, 2025, note 7).
- **Timing follows cash.** A stock of arrears paid in one year enters that year's impulse, with no adjustment for when the demand effect actually falls (SPE-MF, 2025, note 9).
- **It inherits the uncertainty of the output gap**, both in the cyclical adjustment and in the pro/countercyclical classification.

## How it appears across sources

| Source | Role |
|---|---|
| [[fiscal_policy/synthesis/boletim_resultado_fiscal_estrutural (SPE-MF, 2025)]] | Official Brazilian measure by tier (general, central, subnational government): impulse plotted against the previous year-end gap since 1998; expansionary stance predominant over the period, 2024 procyclical-contractionary for the general government |
| [[fiscal_policy/synthesis/resultado_estrutural_impulso_fiscal_brasil (Schettini et al., 2011)]] | Impulse as the negative first difference of the structural balance, by tier, 1998-2010, set against the output gap; contractionary phase to early 2004, expansionary after; shows that atypical revenue left in the balance (Refis, state-company dividends in 2009) can flip the sign of the central government's impulse |

## BRL / application to the current analysis

The SPE bulletin is the only linked source so far: it classifies 2023 as countercyclical expansion and 2024 as procyclical contraction for the general government, with central and subnational governments diverging in 2024.

## Connections

- [[structural_fiscal_balance]] — the solvency reading, built on the same adjusted balance cleaned of one-offs
- [[fiscal_policy/synthesis/boletim_resultado_fiscal_estrutural (SPE-MF, 2025)]] — construction and the pro/countercyclical quadrant charts for Brazil
- [[fiscal_policy/synthesis/resultado_estrutural_impulso_fiscal_brasil (Schettini et al., 2011)]] — 1998-2010 impulse and automatic stabilizers by tier, and the 2009 sign reversal once atypical revenue is netted out
- [[fiscal_multiplier]] — the impulse measures the change in stance; its effect on output depends on the multipliers of each item, which the top-down measure ignores
