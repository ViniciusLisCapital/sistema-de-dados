# Financial Conditions Index (FCI)

**Type:** Composite indicator / summary of monetary and financial transmission
**Tags:** #financial-conditions #fci #leading-indicator #monetary-transmission

---

## Definition

A single index summarizing how tight or loose financial conditions are, built from many financial variables — domestic and foreign interest rates, spreads and risk measures, exchange rates, commodity and equity prices — on the premise that spending and production decisions respond to more than the policy rate. FCIs are usually aggregated by weighted averages or principal components and expressed as a z-score, so they measure conditions relative to their own historical norm (BCB 2020).

## Mechanism

- **Why the policy rate is not enough**: the monetary transmission literature implies that asset prices, risk premia and the exchange rate also move financing costs and wealth; the policy rate can be stable while conditions tighten or ease through these other prices (BCB 2020, citing Hatzius et al., 2010).
- **Construction (BCB version)**: group the variables, extract the first principal component of each group, weight the groups by their ability to predict future activity (the 6-month change in the IBC-Br) and standardize; a rise means tighter conditions. Equity and commodity prices enter with negative weights, since higher prices ease conditions.
- **Use**: decomposition by group says where a tightening comes from; as a leading indicator, the change in the index is used to forecast activity growth.

## When it applies / when it fails

- Informative precisely when conditions move without the policy rate: in Brazil, 2015-2016 and 2018-2019 episodes with a stable Selic were driven by long domestic rates, the currency, risk, equities and oil (BCB 2020).
- Weights fitted to predict activity in one sample assume a stable relation; a shift in the co-movement of components — the 2019 inversion of the usual positive exchange-rate–risk correlation in Brazil — changes what the index says, and excluding the currency group gave a looser reading from mid-2019 (BCB 2020).
- A z-score is relative to the sample's average conditions, not to a structural neutral level.

## How it appears across sources

| Source | Role |
|---|---|
| [[economic_activity/synthesis/indicador_condicoes_financeiras (BCB, 2020)]] | Daily FCI for Brazil in seven groups weighted by their power to predict the IBC-Br; it forecasts activity better than real rates, the curve slope or the Ibovespa at 3 to 12 months (12-month RMSE 0,19 vs 0,70 for the Ibovespa, Table 2) |

## BRL / application to the current analysis

The BCB (2020) index is built for Brazil: the domestic and foreign interest-rate groups carry the largest weights, and the currency group (including R$/US$) improves forecasts of the IBC-Br beyond 3 months. The index reached historical lows in early 2020 and rose with the coronavirus market stress.

## Connections

- [[economic_activity/synthesis/indicador_condicoes_financeiras (BCB, 2020)]] — construction and forecast test of the BCB's daily FCI
