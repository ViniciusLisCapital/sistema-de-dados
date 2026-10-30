# FX Intervention (Intervenção cambial)

**Type:** Policy instrument
**Tags:** #fx-intervention #sterilization #swaps #reserves #bcb #brl

---

## Definition

A central bank's purchases or sales of foreign currency, or of instruments indexed to it, to affect the exchange rate or the functioning of the FX market. In Brazil the BCB has three families of instruments, which differ in what they do to reserves: **spot auctions** (selling or buying dollars outright, which changes reserves for good), **repo-type line auctions** (selling dollars with a commitment to buy them back, which lends liquidity without a permanent change in reserves) and **FX swaps** (contracts settled in reais that pay the exchange-rate variation, which provide hedge without touching reserves). **Sterilized** intervention offsets the effect of the purchase or sale on domestic liquidity, so the interest rate does not move with it.

## Mechanism

- **Liquidity channel.** When the flow of dollars out of the onshore market is large, a spot sale supplies the currency the banks would otherwise have to fund abroad, reduces the system's short position and lowers the cost of dollar liquidity in Brazil (the spread of the cupom cambial). See [[bank_fx_position]].
- **Sterilization and its limits.** Buying reserves during inflows and sterilizing them keeps inflation in check, but has a fiscal cost (domestic interest paid against the yield on reserves), may not be absorbed by shallow bond markets and, by keeping domestic rates high, can perpetuate the inflows it was meant to absorb.
- **Arbitrage can undo it.** When the onshore dollar rate is above the offshore rate, BCB purchases push the onshore rate further up and banks bring in short-term funds to arbitrage it, supplying the very dollars the central bank bought.

## When it applies / when it fails

- Evidence from Brazil's inflow-control period finds no measurable effect of sterilized intervention on the real in either direction, with purchases and sales acting asymmetrically for the arbitrage reason above; sales episodes were few, so that half of the result is weakly identified.
- Intervention changes the flow picture before it changes reserves: reserves move on settlement, the banks' position on contracting.
- In a peg under attack, reserves (own or borrowed) and the interest rate are the defense; whether the defense is kept is a policy choice that depends on its cost to the economy, not only on how many reserves are left. See [[currency_crisis_models]].

## How it appears across sources

| Source | Role |
|---|---|
| [[exchange_rate/synthesis/posicao_de_cambio (BCB, 2020)]] | BCB spot sales in 2019 as dollar liquidity that kept the system's short position far below what the year's negative saldo cambial would have produced; distinguishes spot auctions from line auctions and swaps |
| [[exchange_rate/synthesis/capital_controls_brazil (Chamon & Garcia, 2016)]] | Sterilized intervention shows no effect on the real in either direction; footnote 19 explains why purchases have no traction (onshore-offshore arbitrage) and why sales do not trigger the reverse |
| [[external/synthesis/capital_inflow (IMF, 2010)]] | Reserve accumulation with sterilization as the first response to inflows, and its limits: fiscal cost, shallow markets, and higher domestic rates that perpetuate the inflows |
| [[exchange_rate/synthesis/logic_currency_crises (Obstfeld, 1994)]] | Sweden 1992: the krona survived an attack with an overnight rate pushed to 500 percent and borrowed reserves, and the peg was then dropped without a comparable defense — the decision, not the reserves, ended it |
| [[external/synthesis/us_mp_spillovers_bond_markets (Albagli et al., 2018)]] | Model and evidence that sterilized intervention against US-driven flows dampens the currency move but strengthens the inflows and pushes the adjustment into long-term term premia; emerging-market currencies move roughly half as much as developed ones per bp of US shock (Table 7) |

## BRL / application to the current analysis

The BCB's intervention data are in `cmb_reservas_bc` (spot auctions, line auctions, swap stock). What the sources say for reading them: a large negative FX flow is the situation in which spot sales are expected; swaps hedge without spending reserves; and the evidence for Brazil does not support expecting sterilized purchases to move the level of the real.

## Connections

- [[bank_fx_position]] — the stock that spot sales reduce and that the saldo cambial deepens
- [[capital_controls]] — the alternative tool for inflows when sterilization runs into its limits
- [[currency_crisis_models]] — reserves and interest-rate defense in a peg under attack
- [[carry_trade]] — onshore-offshore arbitrage as the channel that undoes purchases
- [[external/synthesis/us_mp_spillovers_bond_markets (Albagli et al., 2018)]] — intervention cushions the currency but raises inflows and term-premium moves, a cost to add to its cost-benefit analysis
