# Exchange Rate Overshooting

**Type:** Theoretical result / empirical pattern  
**Tags:** #overshooting #dornbusch #sticky-prices #expectations #monetary-policy #volatility

---

## Definition

**Overshooting** occurs when a monetary shock moves the nominal exchange rate *beyond* its new long-run equilibrium value on impact, followed by gradual convergence back.

| Shock | Short-run | Long-run |
|---|---|---|
| Monetary expansion (↑m) | Exchange rate depreciates beyond `ē` | Gradually appreciates back to `ē` |
| Monetary contraction (↓m) | Exchange rate appreciates beyond `ē` | Gradually depreciates back to `ē` |

---

## Mechanism (Dornbusch 1976)

Overshooting arises from **two markets adjusting at different speeds**:

| Market              | Speed         | Variable          |
| ------------------- | ------------- | ----------------- |
| Financial (capital) | Instantaneous | Exchange rate `e` |
| Goods (prices)      | Slow — sticky | Price level `p`   |

After a monetary expansion (`↑m`), step by step:

1. **Long run**: both `e` and `p` rise proportionally to `Δm` (quantity theory holds).
2. **Short run** (`p` fixed): LM must clear with the same price level but higher money supply → domestic rate falls (`↓r`).
3. With `r < r*`, UIP requires the market to expect appreciation. For that expectation to be consistent, `e` must *already* be depreciated beyond `ē` — the expected return path from the overshoot back to `ē` provides exactly the appreciation needed to compensate the negative rate differential.

**Formal result:**

```
Δe₀ = Δm · (1 + λθ/σ) > Δm
```

The impact depreciation exceeds the long-run depreciation. The exchange rate overshoots.

**Convergence path:**

```
e(t) = ē − (ē − e₀) · e^{−θt}
```

The exchange rate decays exponentially from the overshoot back to equilibrium.

---

## Why it matters

1. **Volatility is rational**: FX volatility after monetary shocks is not irrational speculation — it is the equilibrium path under sticky prices and perfect capital mobility.
2. **Policy credibility effects**: A credible, anticipated tightening produces an immediate currency appreciation (undershooting in depreciation terms) that then reverses. This is how BCB hawkishness feeds into the BRL.
3. **Timing matters**: After a rate hike, the currency appreciates on impact, then gradually depreciates as the rate advantage narrows. The carry window is the gradual phase. Verde often enters and exits carry positions based on this timing.
4. **Contractionary bias via trade**: If a monetary tightening causes the currency to appreciate beyond its long-run level, the trade balance deteriorates more than it will in the long run — a temporary contractionary drag.

---

## Empirical pattern (Verde observations)

Verde letters describe BRL as "running ahead of fundamentals" in both directions — appreciating or depreciating beyond what fundamentals seem to justify, then mean-reverting. This is consistent with Dornbusch dynamics in a world with:
- Sticky Brazilian prices (IPCA inertia, indexation)
- High capital mobility (BRL is a liquid EM currency)
- Frequent monetary surprises (BCB communications)

Verde's framework of "ruído vs. sinal" (section 1.6 in [[verde_fx_mental_models]]) — distinguishing transitional BRL overshoots from structural deterioration — is operationally equivalent to asking whether a given BRL move is an overshoot (fade it) or a regime shift (stay short).

---

## Connections

- [[Dornbusch 1976 - Expectations and Exchange Rate Dynamics]] — formal derivation of overshooting
- [[uip]] — overshooting is a direct consequence of UIP: the exchange rate must be far enough from equilibrium that the expected return path satisfies `r = r* + E[Δe]`
- [[Krugman 2023 - Money, Interest Rates, and Exchange Rates]] — same overshooting result derived via a simple money-market + UIP diagram (no continuous-time optimization); Zimbabwe/Venezuela hyperinflations as extreme, compressed-timescale illustrations of the underlying long-run-neutrality logic
- [[Krugman 2023 - Output and the Exchange Rate in the Short Run]] — derives overshooting a third way via the DD-AA model (permanent money supply increase) and adds the J-curve as a second, independent amplifier of exchange-rate volatility
- [[exchange_rate_pass_through]] — incomplete pass-through and the J-curve both delay the real-economy effects of a nominal move, which is part of why the nominal rate has to overshoot further to clear asset markets in the meantime
- [[Krugman 2023 - Fixed Exchange Rates and Foreign Exchange Intervention]] — a permanent devaluation is long-run neutral in exactly the same way as a permanent money supply increase under floating rates, reinforcing the same overshooting/neutrality logic across regimes
- [[currency_regimes]] — the post-1973 float's surprisingly high volatility (far more than trade-flow models predicted) is the historical/empirical motivation for the asset-approach overshooting framework
- [[CFA L2 2025 - Currency Exchange Rates Understanding Equilibrium Value]] — explicitly cites Dornbusch (1976) as the source of the sticky-price overshooting mechanism, contrasted with the "pure" (always-PPP) monetary approach
- [[BIS 2026 - Monetary Policy Transmission to Exchange Rates via Carry Trades]] — a distinct, positioning-driven overshooting mechanism (deleveraging of crowded carry shorts on a tightening surprise), additive to the sticky-price/Dornbusch channel
- [[Fleming 1962 - Domestic Financial Policies Under Fixed and Floating Exchange Rates]] — Fleming's section on speculative capital flows seeds the idea; Dornbusch formalizes it with rational expectations
- [[verde_fx_mental_models]] — empirical pattern: "running ahead of fundamentals" (section 1.6), technical corrections (section 7.3), carry unwind timing (9.4)
- [[kinea_fx_mental_models]] — cluster 8 (technical shocks and short-run overshoots distinct from fundamentals, e.g. the Aug/2024 JPY carry unwind); 8.2 (safe-haven flows vs. positioning unwind as two distinct drivers of a dollar rally)
- [[kapitalo_fx_mental_models]] — 1.4 (central scenario vs. probability distribution — "we count barrels, but we trade probabilities"), a practitioner framing of trading around a fundamentals path that the spot rate can overshoot in either direction
- [[carry_trade]] — the carry window (gradual depreciation after overshooting appreciation) is when carry is collected
- [[fiscal_dominance]] — fiscal-dominance overshooting (rate hike → depreciation via ρ) is directionally opposite to Dornbusch monetary overshooting (rate hike → appreciation)
- [[Itaú 2025 - Fiscal Dominance in Brazil]] — Blanchard (2004) anti-Dornbusch mechanism: rate hike causes depreciation not appreciation when fiscal risk premium dominates
