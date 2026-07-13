# CFA L1 2025 — Exchange Rate Calculations

**Type:** Curriculum reading (CFA Program, Level I)
**Tags:** #cfa #cross-rate #triangular-arbitrage #forward-points #covered-interest-parity #cip
**Source:** CFA Institute, Level I curriculum, Learning Module 8 (Economics)
**Language:** English
**Raw file:** [[exchange_rate_calculation (CFA L1, 2025)]]

---

## Context and motivation

A practitioner-mechanics companion to the vault's theoretical UIP/CIP treatment (Krugman): how FX desks actually quote and compute cross-rates and forward points day to day, and the precise arbitrage arithmetic (with day-count conventions) behind covered interest rate parity. No new theory — this is the computational layer under concepts already in the vault.

## Core argument / thesis

Four market variables — spot rate, forward rate, and the two countries' interest rates — are locked together by a no-arbitrage (CIP) relationship; given any three, the fourth is determined. Separately, any exchange rate between two currencies not directly quoted (a cross-rate) can be backed out from two quotes that share a common currency, with inversion as needed — and if a market-quoted cross-rate doesn't match the implied one, triangular arbitrage forces convergence.

## Key mechanisms / model

- **Cross-rate arithmetic**: multiply/invert quoted pairs sharing a common currency to cancel it out (e.g., CAD/USD × USD/EUR = CAD/EUR). The FX market doesn't use "direct/indirect quote" framing (that's location-dependent) — it uses fixed conventional currency-pair quotes (EUR always base vs. USD, etc.).
- **Triangular arbitrage**: if a dealer's quoted cross-rate doesn't match the rate implied by the two underlying conventional quotes, a riskless round-trip trade captures the discrepancy — kept negligible in practice by continuous algorithmic monitoring.
- **Forward points/pips**: forward − spot, scaled to the last quoted decimal (×10,000 for 4-decimal pairs, ×100 for yen's 2-decimal convention). Positive points = base currency at a forward premium (price currency at a discount), and vice versa.
- **CIP arbitrage equation** (f/d quoting convention): `(1+r_d) = S_(f/d)(1+r_f)(1/F_(f/d))`, rearranged to `F_(f/d) = S_(f/d) · (1+r_f)/(1+r_d)` — this is the same covered interest parity condition documented in [[uip]]'s variants table, here derived from first principles via the "swap financing" round-trip (convert → invest abroad → convert back forward) rather than stated as a given.
- **Day-count/maturity scaling**: `F − S = S · [(r_f − r_d)/(1 + r_d·τ)] · τ`, where τ is the fraction of a year (LIBOR-style actual/360) — forward points are *approximately* but not exactly proportional to maturity, since the denominator itself scales with τ.
- **Forward rate as a (poor) predictor of the future spot rate**: setting `F_t = S_(t+1)` in the CIP formula gives `%ΔS = (r_f − r_d)/(1 + r_d)` — i.e., UIP restated. The reading explicitly warns this interpretation is unreliable in practice: forward rates may be statistically unbiased predictors, but with error margins too wide to be useful, and are not how professional FX traders actually form expectations (they track the *trend* in the differential, not just its level).

## Main results / findings

- The reading is explicit that a higher domestic interest rate implies the domestic currency's forward rate is at a *discount* (i.e., UIP-consistent expected depreciation) — flagged as "counterintuitive" relative to the folk-wisdom "higher rates → stronger currency," the same tension Krugman's textbook resolves by distinguishing sticky-price (Ch. 15) from Fisher-effect (Ch. 16) sources of a rate change.

## Limitations and caveats

- Purely mechanical/computational — no discussion of why CIP holds empirically better than UIP, or of the post-2008 CIP breakdown documented in [[Krugman 2023 - Exchange Rates and the Foreign Exchange Market (An Asset Approach)]]. Treat as a reference for quote conventions and arithmetic, not as an independent theoretical source.

## Connections

- [[uip]] — this reading's CIP arbitrage equation is the same covered interest parity condition already in the "Variants" table, here with full swap-financing derivation and day-count mechanics
- [[Krugman 2023 - Exchange Rates and the Foreign Exchange Market (An Asset Approach)]] — same CIP condition, same "forward rate ≈ expected future spot rate only if UIP also holds" logic, from the textbook-theory side rather than the trading-desk side
