# Krugman 2023 — Money, Interest Rates, and Exchange Rates

**Type:** Textbook chapter (International Economics, 12th ed., Ch. 15)
**Tags:** #textbook #monetary-approach #overshooting #money-supply #hyperinflation #inflation-targeting #pass-through
**Source:** Krugman, Obstfeld & Melitz, *International Economics: Theory and Policy*, 12th ed. (2023), Part Three
**Language:** English
**Raw file:** [[money_interest_rate_exchange_rates (Krugman, 2023)_raw]]

---

## Context and motivation

Builds the "monetary approach" on top of Ch. 14's asset-market/UIP framework: having established that the exchange rate is whatever equates expected returns across currencies (UIP), this chapter explains what determines the two ingredients UIP takes as given — the interest rate (via national money-market equilibrium) and expectations of the future exchange rate (via the long-run price level). This is the textbook's own derivation of exchange rate overshooting, arrived at independently of — but structurally identical to — Dornbusch (1976).

## Core argument / thesis

Money market equilibrium (`Ms/P = L(R,Y)`) pins down the interest rate given the price level and output; combined with UIP, this links national money supplies directly to today's exchange rate. In the short run (sticky prices), a money supply increase lowers the interest rate and depreciates the currency. In the long run (flexible prices, money neutral), the price level and the exchange rate both rise proportionally to the money supply — money is neutral for real variables but not for nominal ones. The gap between these two horizons is exactly what forces the exchange rate to *overshoot* its long-run value on impact.

## Key mechanisms / model

- **Money demand**: `Md = P·L(R,Y)`, decreasing in R (opportunity cost of holding non-interest-bearing money), increasing in Y (transactions demand). Risk is argued away as irrelevant to money demand (money and bonds share the same price-level risk).
- **Money market equilibrium**: given P and Y, R adjusts to clear `Ms/P = L(R,Y)`. Standard comparative statics: `↑Ms → ↓R`; `↑Y → ↑R` (given P).
- **Short-run money–FX link**: combining the money market with the Ch. 14 UIP diagram (Figures 15-6/15-7) — a Fed money-supply increase lowers R$, which (via UIP) depreciates the dollar today; symmetric logic for the ECB and the euro.
- **Long-run neutrality**: a permanent doubling of Ms is analytically identical to a currency redenomination — no long-run effect on R, Y, or relative prices; P and the exchange rate both double. This is the anchor for the "expected future exchange rate" that Ch. 14 took as exogenous.
- **Overshooting derivation** (Figs. 15-13/15-14): after a *permanent* Ms increase, short-run R falls (sticky P) and stays below R* until P finishes adjusting — but UIP requires the interest gap to be offset by expected dollar appreciation, which is only consistent with market expectations if the exchange rate first jumps *past* its new long-run level, then appreciates back down as P catches up. Textbook-level statement of the same result as [[Dornbusch 1976 - Expectations and Exchange Rate Dynamics]], derived without an explicit dynamic optimization — just UIP + sticky-price money market equilibrium.
- **Hyperinflation case studies**: Zimbabwe (2007–09, price level ×36.7M in 18 months; four currency redenominations; eventual dollarization) and Venezuela (late 2010s) as "laboratory conditions" where the long-run money-price link plays out over months instead of decades — both driven by monetized fiscal deficits.
- **EM inflation-targeting case study**: explicitly ties this chapter's mechanics to policy practice — flags the "two targets (inflation + exchange rate), one instrument (interest rate)" tension in EM inflation targeters, citing Ostry/Ghosh/Chamon's "two targets, two instruments" prescription (FX intervention as a second tool). Distinguishes first-round pass-through (import prices) from second-round pass-through (inflation expectations de-anchoring) and notes IMF evidence that inflation targeters have smaller second-round pass-through — directly relevant to the exchange-rate-pass-through cluster of sources in this vault ([[depreciation_pass_through (Goldfajn, 2000)]] et al., pending).

## Main results / findings

- Money supply changes are neutral for real variables in the long run but move nominal exchange rates and price levels proportionally — the "quantity theory" backbone of the monetary approach.
- Overshooting is *not* Dornbusch-specific machinery — it's a generic consequence of combining UIP with any source of short-run price stickiness, which is why Krugman's textbook derives the identical result via a simpler money-market diagram rather than Dornbusch's continuous-time optimization.
- Empirically, money-supply growth and inflation track each other closely across Latin America 1980–2014 and extremely tightly in the Venezuela/Zimbabwe hyperinflations — offered as validation of the long-run neutrality result.

## Limitations and caveats

- Assumes a closed link from money supply to price level; doesn't address the exchange-rate-pass-through *mechanics* (how depreciation feeds into domestic prices) beyond a brief case-study aside — that is the subject of the Goldfajn/Belaisch/Cortapasso cluster in this vault.
- Long-run neutrality is a one-time-level-change result; explicitly does not claim changes in money growth *rates* are neutral (footnote 6).
- The EM inflation-targeting case study is a survey of others' findings (Samarina et al. 2014, Ouyang & Rajan 2016, Vegh & Vuletin 2012), not original analysis — treat as a pointer to the primary literature rather than a result in its own right.

## Connections

- [[Dornbusch 1976 - Expectations and Exchange Rate Dynamics]] — this chapter's Figs. 15-13/15-14 are the same overshooting result via a simpler (non-continuous-time) money-market argument
- [[overshooting]] — textbook-level derivation and the Zimbabwe/Venezuela hyperinflation case studies as extreme, compressed-timescale illustrations of the long-run neutrality/overshooting logic
- [[uip]] — money-market equilibrium is the missing piece that pins down R in the UIP condition from Ch. 14
- [[Krugman 2023 - Exchange Rates and the Foreign Exchange Market (An Asset Approach)]] — direct continuation; Figures 15-6/15-7 explicitly combine this chapter's money-market diagram with Ch. 14's FX equilibrium diagram
