---
aliases: ["Dornbusch 1976"]
---

# Expectations and Exchange Rate Dynamics

**Author:** Rudiger Dornbusch  
**Source:** Journal of Political Economy, 1976, vol. 84, no. 6, pp. 1161–1176  
**Type:** Foundational theoretical article  
**Tags:** #overshooting #exchange-rate #monetary-policy #expectations #sticky-prices #foundational

---

## Summary

Dornbusch shows that a permanent monetary expansion causes **exchange rate overshooting**: in the short run, the exchange rate depreciates beyond its long-run equilibrium value, then gradually appreciates back. The mechanism is the combination of sticky goods prices with perfect capital mobility and rational expectations. The result dismantles the view that flexible exchange rates are inherently unstable — the volatility is endogenous to the price adjustment regime, not to the exchange rate regime itself.

---

## Model

### Variables and notation

| Variable | Description |
|---|---|
| `e` | Log of the nominal exchange rate (domestic per foreign currency) |
| `p` | Log of the domestic price level |
| `ē`, `p̄` | Long-run equilibrium values of `e` and `p` |
| `m` | Log of the money stock |
| `r`, `r*` | Domestic and foreign interest rates |
| `θ` | Speed at which the exchange rate converges to ē |

---

### Block 1 — Capital mobility and expectations

**Uncovered interest parity (UIP):**

```
r = r* + ε
```

where `ε` is the expected rate of depreciation. With rational expectations and stable convergence:

```
ε = θ(ē − e)     (θ > 0)
```

Expected depreciation is proportional to the gap between the current rate and its long-run level. If `e > ē` (the rate is too depreciated), the market expects future appreciation, which compresses `r` below `r*` by exactly the required amount.

---

### Block 2 — Money market (LM)

```
m − p = φy − λr
```

In long-run equilibrium, `r = r*`, so:

```
m − p̄ = φy − λr*
```

`p̄` is pinned by `m` given fixed `r*` and `y`.

---

### Block 3 — Goods market (IS / long-run PPP)

In the long run, PPP holds:

```
ē = p̄ − p̄*
```

In the short run, prices are sticky (`p` fixed), but aggregate demand responds to the real exchange rate:

```
ṗ = π[d(e, p, ...) − ȳ]     (π > 0)
```

The price adjustment speed `π` determines how slowly the system converges.

---

### Solution: Overshooting

**Long-run exchange rate after a monetary expansion of size `Δm`:**

```
Δē = Δm    (quantity theory: proportional)
```

**Short-run exchange rate (on impact, p fixed):**

```
Δe₀ = Δm · (1 + λθ/σ) > Δm
```

where `σ` is the price semi-elasticity of goods demand. The exchange rate **overshoots** on impact. It then converges:

```
e(t) = ē − (ē − e₀) · e^{−θt}
```

**Intuition:** With sticky prices, the entire real adjustment of money must occur through the nominal exchange rate in the short run. Because the LM must clear with fixed `p` and higher `m`, the domestic interest rate falls. For capital markets to clear with domestic rates below foreign rates, the exchange rate must sit beyond its equilibrium — depreciated enough that the market expects future **appreciation** that exactly compensates the negative interest differential.

---

## Section V — Extension with variable output

When output `y` is endogenous (real output responds to the real exchange rate in the short run):

```
ẏ = δ(e − p)    (real depreciation expands output)
```

The system becomes second-order. Overshooting can be larger or smaller depending on `δ` and `π`. The qualitative property survives: the exchange rate anchors expectations via UIP and the adjustment is gradual via prices.

---

## Key results

1. **Overshooting is rational**, not irrational — it emerges from consistent expectations combined with price stickiness.
2. **Exchange rate volatility** does not imply destabilizing speculation. It is the optimal system response.
3. **Asymmetric adjustment speeds**: the exchange rate adjusts instantaneously (financial market), prices adjust slowly (goods market). This difference generates overshooting.
4. **Contractionary monetary policy**: causes the exchange rate to appreciate beyond long-run equilibrium (undershooting in depreciation terms) — then depreciate gradually.
5. **Exchange rate as expectational anchor**: UIP + slow prices means the exchange rate path carries all the information about future monetary policy.

---

## Implications for BRL/USD analysis

| Context | Model implication |
|---|---|
| BCB unexpectedly hikes the Selic | BRL appreciates beyond new ē (undershooting); then depreciates gradually as domestic prices rise |
| Fed unexpectedly hikes rates | USD appreciates too much on impact vs. all currencies; expected further USD appreciation turns negative |
| Domestic money shock (fiscal monetization) | BRL depreciates beyond long-run on impact; expected appreciation compensates required interest spread |
| Floating exchange rate regime | High short-run volatility does NOT imply fundamental instability — consistent with dynamic equilibrium |

---

## Connections in the bibliography

- [[Mundell 1963]] — no price stickiness; exchange rate adjusts instantly → no overshooting
- [[Fleming 1962]] — same Mundell-Fleming framework; Dornbusch adds dynamic expectations
- [[Obstfeld-Rogoff]] — extensions with microfoundations (Redux model, ch. 9–10)
- [[verde_fx_mental_models]] — Verde letters frequently describe FX "running ahead of fundamentals" — consistent with this mechanism

---

## References in the paper

- Calvo & Rodriguez (1977) — extension with consumption goods and capital  
- Kouri (1976) — portfolio balance approach  
- Mussa (1976) — expectations and exchange rates  
- Niehans (1975) — overshooting in a portfolio model  
