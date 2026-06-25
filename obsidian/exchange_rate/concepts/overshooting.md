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
- [[Fleming 1962 - Domestic Financial Policies Under Fixed and Floating Exchange Rates]] — Fleming's section on speculative capital flows seeds the idea; Dornbusch formalizes it with rational expectations
- [[verde_fx_mental_models]] — empirical pattern: "running ahead of fundamentals" (section 1.6), technical corrections (section 7.3), carry unwind timing (9.4)
- [[carry_trade]] — the carry window (gradual depreciation after overshooting appreciation) is when carry is collected
- [[fiscal_dominance]] — fiscal-dominance overshooting (rate hike → depreciation via ρ) is directionally opposite to Dornbusch monetary overshooting (rate hike → appreciation)
- [[Itaú 2025 - Fiscal Dominance in Brazil]] — Blanchard (2004) anti-Dornbusch mechanism: rate hike causes depreciation not appreciation when fiscal risk premium dominates
