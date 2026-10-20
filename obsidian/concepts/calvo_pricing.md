# Calvo Pricing

**Type:** Price-setting friction (modeling device)
**Tags:** #calvo #sticky-prices #staggered-prices #new-keynesian

---

## Definition

A model of staggered price setting in which each firm may change its price only when a random signal arrives, with a constant probability per unit of time that does not depend on how long ago the firm last changed its price and is independent across firms. Introduced by Calvo (1983) as "an analytically more tractable price-setting technology" than the fixed-length staggered contracts of Phelps (1978) and Taylor (1979, 1980).

## Mechanism

- **Continuous time (Calvo 1983)**: the waiting time to the next signal is exponential with parameter δ, so the expected length of a price quotation is 1/δ. With a continuum of firms, the law of large numbers makes a measure δ of firms reprice per unit of time and gives the surviving quotations a geometric age distribution; the price level is their weighted average and is therefore predetermined. A resetting firm prices on the future price level and future excess demand, each date weighted by the probability that its quotation is still in force.
- **Discrete time (Galí ch. 3)**: each firm resets with probability 1−θ per period; θ is "a natural index of price stickiness", inflation is proportional to the gap between the reset price and last period's price level, and a resetting firm sets a markup over a weighted average of current and expected marginal costs with weights in θ^k β^k. With θ = 3/4 the average price duration is four quarters.
- Aggregating either version gives a forward-looking inflation equation — the New Keynesian Phillips curve — whose slope falls as prices get stickier.

## When it applies / when it fails

- Its appeal is tractability: the history of each firm does not matter, so aggregation is simple. Calvo argues it "does not really depend on the existence of nominal contracts" and fits firms hit by random shocks that prevent continuous revisions.
- The timing of price changes is exogenous; Calvo calls the exogeneity of δ "a not very satisfactory feature" of the model, though his qualitative results hold for any constant δ. It differs in this from menu-cost models, where the firm chooses when to change its price.
- Purely forward-looking pricing gives no intrinsic inflation persistence; Galí's exercises add indexation or backward-looking firms for that.

## How it appears across sources

| Source | Role |
|---|---|
| [[monetary_policy/synthesis/staggered_prices (Calvo, 1983)]] | Origin: constant hazard of price change, aggregation by the law of large numbers, predetermined price level, and the resulting "higher-order inverse Phillips Curve" in a utility-maximizing model |
| [[monetary_policy/synthesis/basic_nk_model_ch3 (Gali, 2015)]] | Discrete-time version as the pricing block of the basic NK model: reset probability 1−θ, forward-looking reset price, NKPC slope decreasing in θ |

## BRL / application to the current analysis

The sources linked here say nothing about Brazil yet.

## Connections

- [[nk_phillips_curve]] — the inflation equation obtained by aggregating Calvo pricing
- [[taylor_principle]] — with Calvo pricing the price level is predetermined, yet an interest-rate peg still leaves a continuum of equilibria (Calvo 1983)
- [[monetary_policy/synthesis/staggered_prices (Calvo, 1983)]] — the original paper
- [[monetary_policy/synthesis/basic_nk_model_ch3 (Gali, 2015)]] — the discrete-time version in the textbook NK model
