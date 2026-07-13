# Krugman 2023 — Output and the Exchange Rate in the Short Run

**Type:** Textbook chapter (International Economics, 12th ed., Ch. 17)
**Tags:** #textbook #dd-aa-model #fiscal-policy #monetary-policy #j-curve #pass-through #global-value-chains #crowding-out
**Source:** Krugman, Obstfeld & Melitz, *International Economics: Theory and Policy*, 12th ed. (2023), Part Three
**Language:** English
**Raw file:** [[output_exchange_rates_sr (Krugman, 2023)_raw]]

---

## Context and motivation

Closes out the textbook's open-economy macro model by letting output itself become endogenous (Chs. 14–16 all took Y as given). Combines a sticky-price output-market equilibrium (the DD schedule) with the asset-market equilibrium already built in Chs. 14–15 (the AA schedule) to explain why, e.g., the US and Canada — similarly hit by the 2009 global recession — saw their currencies move in opposite directions (USD −8%, CAD +16%): the answer lives in differing monetary/fiscal responses, not in the output shock itself.

## Core argument / thesis

Short-run equilibrium is the intersection of DD (output market clears: aggregate demand = aggregate output, upward-sloping in E-Y space because depreciation raises net exports and demand) and AA (asset markets clear: money market + UIP, downward-sloping because higher Y raises money demand, raises R, and appreciates the currency to preserve interest parity). Whether a policy is *temporary* or *permanent* is decisive: permanent policy shifts also move `E^e` (Ch. 16's long-run exchange rate), which shifts AA itself — so permanent and temporary versions of the same policy have very different short-run output/exchange-rate effects.

## Key mechanisms / model

- **DD schedule**: real depreciation → cheaper domestic goods → higher aggregate demand → higher equilibrium output. Shifts right with ↑G, ↓T, ↑I, ↑P*, ↓P, or a demand shift toward domestic goods.
- **AA schedule**: ↑Y → ↑money demand → ↑R → currency appreciates (via UIP) to keep the return on foreign deposits competitive. Shifts up with ↑Ms, ↓P, ↑E^e, ↑R*, or ↓ money demand.
- **Temporary monetary expansion**: shifts AA up only (E^e unaffected) → currency depreciates, output rises.
- **Temporary fiscal expansion**: shifts DD right only (E^e unaffected) → currency *appreciates*, output rises. Fiscal and monetary expansion move the exchange rate in opposite directions despite both raising output.
- **Permanent money supply increase**: also raises E^e proportionally (Ch. 16 long-run neutrality) → AA shifts up by *more* than the temporary case → sharper depreciation and larger output rise on impact, followed by inflationary adjustment that gradually reverses part of the depreciation as P rises — this reversal is exchange rate overshooting, derived here independently of Ch. 15's version, via the DD-AA apparatus instead of the pure money-market one.
- **Permanent fiscal expansion — the "no multiplier" result**: because it also appreciates E^e (Ch. 16: permanent ↑G → real and nominal appreciation), AA shifts down as DD shifts right. Formal five-step argument shows that, starting from full employment, these two shifts exactly cancel: **the government spending multiplier for a permanent fiscal expansion is zero** — the entire effect is 100% crowding-out of net exports via currency appreciation. This is much stronger than the standard closed-economy partial-crowding-out story.
- **Liquidity trap case**: at the zero lower bound, temporary monetary policy is powerless (AA's horizontal segment), but temporary fiscal policy's multiplier is *larger* than normal (no interest-rate or exchange-rate crowding out) — cites empirical multiplier estimates (Hall: 0.5–1.0 normally, up to 1.7 in a liquidity trap; Christiano-Eichenbaum-Rebelo: up to 3.7; Auerbach-Gorodnichenko: ~2 in recessions) and flags 2010s European austerity as the real-world stakes of this parameter.
- **Current account policy effects (XX schedule)**: monetary expansion improves the current account (depreciation + output rise, net effect positive); both temporary and (more strongly) permanent fiscal expansion worsen it (appreciation dominates the income effect).
- **J-curve**: a real depreciation can worsen the current account on impact (pre-contracted trade volumes at old prices, now revalued at the new exchange rate) before improving it over 6–12 months as volumes adjust — an additional amplifier of exchange-rate overshooting on top of the Ch. 15/16 mechanism, because monetary policy's output effect is delayed.
- **Exchange rate pass-through**: formally defined as the percentage change in *import prices* per 1% change in E. The DD-AA baseline assumes pass-through = 1 (P, P* fixed short-run ⇒ nominal ≈ real exchange rate movement). In practice, pass-through is incomplete — pricing-to-market by import-competing firms protecting market share means US import prices historically rise by only ~half of a dollar depreciation within a year. Incomplete pass-through dampens the J-curve but also weakens the relative-price channel, so its net effect on current-account adjustment speed is ambiguous.
- **Global value chains and pass-through**: backward linkages (imported inputs in a country's own exports) mute the export-price effect of depreciation (Italy bicycle example: 50% imported input content halves the effective export-price decline from a 10% euro depreciation); forward linkages work symmetrically on the import side. Net macro effect on demand is ambiguous because GVC participation also raises gross trade volumes, which independently amplifies the exchange-rate elasticity of demand.

## Main results / findings

- The 2009 US/Canada divergence (from the chapter's opening) is explained by the model's own logic: differing monetary and fiscal responses to a common shock produce opposite exchange-rate paths even with similar output outcomes.
- Permanent fiscal expansion's zero multiplier is the chapter's sharpest, most counterintuitive result — it depends entirely on assuming the economy starts at full employment; the liquidity-trap case explicitly breaks this (no crowding out via rates or FX at the ZLB).

## Limitations and caveats

- The full DD-AA apparatus assumes small-country-style asset markets (R* and P* exogenous) and abstracts from the current account's dynamic wealth effects (flagged but not resolved in-chapter — deferred, per the chapter's own text, to a "Current Account, Wealth, and Exchange Rate Dynamics" section and later chapters).
- Pass-through and J-curve discussions are qualitative/illustrative (no formal Marshall-Lerner elasticity estimates in the main text — relegated to an appendix); treat magnitudes as textbook approximations, not calibrated parameters.
- The permanent-fiscal-expansion "zero multiplier" result is a comparative-statics long-run-anchor result; it is not a claim that fiscal stimulus is never effective in the short run (temporary fiscal expansion, and any expansion during a liquidity trap, does raise output in this same model).

## Connections

- [[overshooting]] — this chapter derives overshooting a second, independent way (via DD-AA under a permanent money supply increase) and adds the J-curve as a second, distinct amplifier of exchange-rate overshooting
- [[uip]] — the AA schedule is UIP + money-market equilibrium restated as a function of output; permanent-vs-temporary policy distinctions here are the same E^e-sensitivity logic as Ch. 15/16
- [[ppp_balassa_samuelson]] — the real exchange rate `q = EP*/P` is the operative variable throughout the current-account/DD analysis, same definition as Ch. 16
- [[Krugman 2023 - Money, Interest Rates, and Exchange Rates]] — direct continuation; this chapter's permanent-money-supply overshooting result is the DD-AA restatement of that chapter's money-market-only derivation
- [[Krugman 2023 - Price Levels and the Exchange Rate in the Long Run]] — E^e here is exactly that chapter's long-run exchange rate; permanent policy shifts move it, temporary ones don't
