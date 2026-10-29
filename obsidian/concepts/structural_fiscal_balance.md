# Structural Fiscal Balance

**Type:** Fiscal indicator (cyclically and one-off adjusted balance)
**Tags:** #structural-balance #fiscal-policy #output-gap #one-off-measures

---

## Definition

The primary balance the government would run with output at potential, with the commodity prices that drive revenue at their long-run trend, and without non-recurrent revenues and expenditures. It is meant to isolate the discretionary and recurrent part of fiscal policy from what the cycle and one-off events do to the observed balance. Its change from one year to the next is read as the structural fiscal effort: a rise improves solvency, a fall worsens it.

## Construction

The observed balance is cleaned in steps:

1. **Observed → recurrent:** remove the non-recurrent ("one-off") revenues and expenditures — decisions with a temporary effect, confined to one or a few years (asset sales, extraordinary dividends, signing bonuses, extraordinary credits, calendar shifts between cash and accrual).
2. **Recurrent → cyclically adjusted:** remove the effect of the output gap (and, for a commodity exporter, of commodity-price gaps) on revenue, through revenue elasticities to output.
3. The result is the structural balance; the cyclically adjusted balance alone (without the one-off cleaning) is the base of the [[fiscal_impulse]] measure.

The two inputs that carry the result are the **output gap** (how much of revenue is "cycle") and the **classification of one-offs** (what counts as transitory).

## When it applies / when it fails

- **It is only as good as the potential-output estimate.** A mismeasured gap shifts the whole structural series; the SPE builds potential with a production function, which is itself a model choice.
- **A volume output gap misses price cycles.** Most revenue is ad valorem, so inflation well above target inflates revenue without moving primary spending at the same pace; the conventional indicator then records that as structural effort. The SPE's nominal-gap alternative changes the sign or size of the balance precisely in the high-inflation years (SPE-MF, 2025, Boxe 1).
- **One-off classification is a judgment and must be revisited.** Something recorded as temporary may become permanent — the SPE reclassifies part of the 2020–2022 cash-transfer extraordinary credits as recurrent, since a temporary pandemic benefit set a new level — and a flow that is recurrent but finite (tax-credit compensations from a court ruling) can be treated either way, with a large effect on the level.
- **The consolidated figure can hide opposite stances.** Central and subnational governments can move in opposite directions, so the decomposition by tier matters.

## How it appears across sources

| Source | Role |
|---|---|
| [[fiscal_policy/synthesis/boletim_resultado_fiscal_estrutural (SPE-MF, 2025)]] | The Ministry of Finance's official indicator for Brazil: production-function potential, oil and iron-ore cycles, an inventory of one-offs since 1997, decomposition by tier, and two alternative exercises (nominal gap, "Tese do Século" compensations) that each move the level by about 1 p.p. of potential GDP in recent years |
| [[fiscal_policy/synthesis/empirical_characterization_fiscal_shocks (Blanchard & Perotti, 2002)]] | Builds the output elasticity of net taxes from tax-to-base and base-to-GDP elasticities (extending the OECD's annual ones to quarterly frequency) to strip the automatic response of revenue to activity and identify fiscal shocks; quarterly and annual base elasticities can differ sharply |
| [[fiscal_policy/synthesis/resultado_estrutural_impulso_fiscal_brasil (Schettini et al., 2011)]] | First estimate for Brazil's general government, 1997-2010: accounting pre-adjustment for non-recurrent revenue and creative accounting, revenue elasticities by tax base estimated with time-varying Kalman-filter models, oil-price cycle for royalties, no adjustment on the spending side; reviews the historical measures (full-employment, cyclically neutral, cyclically adjusted, Blanchard's moving base) |

## BRL / application to the current analysis

The SPE bulletin is the official Brazilian series: it reads 2022–2023 as structural deterioration and 2024 and the first half of 2025 as pro-consolidation effort, while showing that the level depends on the treatment of inflation above target and of the "Tese do Século" compensations.

## Connections

- [[fiscal_impulse]] — the demand-side reading built on the cyclically adjusted balance
- [[fiscal_policy/synthesis/boletim_resultado_fiscal_estrutural (SPE-MF, 2025)]] — construction of the indicator for Brazil and its sensitivity to method
- [[fiscal_policy/synthesis/empirical_characterization_fiscal_shocks (Blanchard & Perotti, 2002)]] — cyclical adjustment of net taxes by elasticities, used as an identification device
- [[fiscal_policy/synthesis/resultado_estrutural_impulso_fiscal_brasil (Schettini et al., 2011)]] — Ipea's 2011 estimate for Brazil, the methodological precursor of the SPE indicator; argues for structural targets
- [[fiscal_multiplier]] — the same elasticity-based cyclical adjustment of net taxes that cleans the balance is what Blanchard & Perotti use to identify fiscal shocks and estimate multipliers
