# Krugman 2023 — Fixed Exchange Rates and Foreign Exchange Intervention

**Type:** Textbook chapter (International Economics, 12th ed., Ch. 18)
**Tags:** #textbook #fixed-exchange-rate #sterilization #currency-crisis #capital-flight #reserve-currency #gold-standard #risk-premium
**Source:** Krugman, Obstfeld & Melitz, *International Economics: Theory and Policy*, 12th ed. (2023), Part Three
**Language:** English
**Raw file:** [[fixed_exchange_rate_intervention (Krugman, 2023)_raw]]

---

## Context and motivation

Drops the "cleanly floating exchange rate" assumption carried through Chs. 14–17 and asks how a central bank actually pegs a currency, and what that commitment costs it in terms of monetary policy autonomy. Motivated as necessary background for four real-world cases: managed floating ("dirty float"), regional currency unions, developing-country pegs, and the historical fixed-rate eras (pre-1914, 1925–31, 1945–73) that inform current debates about reviving fixed rates.

## Core argument / thesis

Fixing the exchange rate at E₀ requires the central bank to keep R = R* (via UIP with zero expected depreciation), which means it must accommodate money demand automatically through FX intervention rather than setting the money supply independently. This single constraint explains almost everything else in the chapter: why monetary policy is powerless and fiscal policy is *more* potent under fixed rates than floating, why devaluations happen, why balance-of-payments crises and capital flight occur, and why sterilized intervention is effective only when domestic and foreign bonds are imperfect substitutes.

## Key mechanisms / model

- **Central bank balance sheet mechanics**: any FX purchase/sale directly changes the money supply one-for-one (before the money multiplier) unless offset — this offsetting operation is **sterilization** (equal and opposite domestic-asset transaction, leaving Ms unchanged).
- **Fixing the rate**: requires R = R* continuously; the central bank must buy foreign assets (expand Ms) whenever money demand rises (e.g., from higher Y) to prevent the appreciation that would otherwise occur, and vice versa.
- **Monetary policy is powerless under a fixed rate**: any attempted Ms change is automatically and fully reversed by the FX intervention needed to defend E₀ — the central bank can only change the *composition* of its balance sheet (foreign vs. domestic assets), not the total money supply.
- **Fiscal policy is more potent under fixed than floating rates**: a fiscal expansion that would normally appreciate the currency (crowding out net exports, per Ch. 17) instead forces the central bank to buy foreign assets to prevent that appreciation — this involuntary monetary expansion adds to, rather than offsets, the fiscal impulse.
- **Devaluation/revaluation mechanics**: distinguished from depreciation/appreciation by being a deliberate policy act under a fixed regime (passive voice: "the currency was devalued") vs. a market outcome under floating (active voice: "the currency depreciated"). A devaluation raises output, and — like a permanent Ms increase under floating — is neutral in the long run (price level rises proportionally).
- **Balance-of-payments crises / capital flight**: the moment the market expects a future devaluation to E₁ > E₀, UIP requires R to jump to R* + (E₁−E₀)/E₀ *today* even though the peg hasn't broken yet — this forces the central bank to sell reserves to shrink Ms and validate the higher rate, producing the sharp reserve loss ("capital flight") that is often the visible symptom, not the cause, of an unsustainable peg.
- **Two crisis archetypes**: (1) fundamentals-driven — a central bank monetizing fiscal deficits burns through reserves until collapse is mathematically inevitable, just accelerated by capital flight; (2) **self-fulfilling crises** — a fragile banking sector (short-term deposits funding bad loans) means *devaluation expectations alone* can force the central bank to lend to banks, burn reserves, and trigger the very collapse that was merely feared, not fundamentally inevitable.
- **Imperfect asset substitutability and the risk premium**: when domestic/foreign bonds aren't perfect substitutes, UIP becomes `R = R* + E[ΔE]/E + ρ`, and `ρ = ρ(B − A)` — the risk premium rises with the stock of domestic government debt the private market must hold (B) net of the central bank's own domestic asset holdings (A). This is what makes **sterilized intervention effective**: swapping A for foreign assets raises B−A, raises ρ, and depreciates the currency even with Ms unchanged. Empirically: little evidence sterilized intervention matters much in advanced economies (bonds ≈ perfect substitutes); more evidence it matters in EM (thinner markets, capital controls, imperfect substitutability) — directly relevant to how BCB's FX intervention toolkit is assessed.
- **Signaling effect**: sterilized intervention can move the rate even without a risk-premium channel, by credibly signaling future monetary/fiscal intent — but "crying wolf" (signaling without follow-through) destroys this channel over time.
- **Reserve currency asymmetry**: under a dollar-reserve system (1945–73), the N-th currency (the reserve issuer) never has to intervene — it exports its monetary policy to every pegging country, an asymmetry that eventually helped break the system. A gold standard restores symmetry (every country, including none, defends its currency against gold) but trades that for exposure to real gold-supply shocks and a hard floor on aggregate world liquidity.

## Main results / findings

- Swiss franc case study (2011–2015): SNB defended a floor of CHF 1.2/EUR by buying euros without limit (reserves reaching ~75% of Swiss GDP), then abandoned it abruptly in January 2015 once continuing to defend it risked open-ended capital losses from anticipated ECB QE — a real-world illustration that even a "strong-currency peg" (unlike a weak-currency peg, not limited by finite reserves) can become undesirable to defend, and that removing it can be a shock to third parties (Polish CHF-mortgage holders lost 15–20% via the correlated carry-trade channel, à la [[carry_trade]]).
- The chapter's own logic implies fixed-rate credibility is a continuum, not binary: the same UIP-plus-risk-premium machinery that describes an orderly peg also describes its collapse once expectations shift.

## Limitations and caveats

- The core DD-AA-with-fixed-E model assumes perfect asset substitutability by default; the risk-premium extension is presented as a secondary, "imperfect substitutability" case, not integrated into the main model — treat `ρ(B−A)` as a stylized microfoundation, not a calibrated empirical relationship (the chapter itself flags weak/mixed evidence for advanced economies).
- Self-fulfilling vs. fundamentals-driven crises are presented as a conceptual dichotomy for teaching purposes; in practice, distinguishing which type is occurring in real time is exactly the hard empirical problem policymakers face — the chapter does not offer a diagnostic.

## Connections

- [[risk_premium]] — Krugman's `ρ = ρ(B − A)` gives a specific microfoundation (relative bond supply) for the same risk-premium wedge this concept page already treats qualitatively for BRL (fiscal uncertainty, political risk, sub-investment-grade status)
- [[uip]] — imperfect asset substitutability is UIP's risk-premium extension, formalized here via central bank balance sheet composition rather than generic risk aversion
- [[carry_trade]] — the Polish zloty/Swiss franc mortgage carry trade (2015 SNB floor removal) is a textbook real-world carry-crash case, distinct from but structurally identical to the AUD/JPY case in [[Krugman 2023 - Exchange Rates and the Foreign Exchange Market (An Asset Approach)]]
- [[overshooting]] — permanent devaluation is shown to be long-run neutral just like a permanent Ms increase under floating (Ch. 15/16), reinforcing that the same money-neutrality logic underlies both regimes
- [[Krugman 2023 - Output and the Exchange Rate in the Short Run]] — directly extends the DD-AA apparatus from that chapter to the fixed-exchange-rate case; monetary/fiscal policy effectiveness results are the mirror image of the floating-rate results there
