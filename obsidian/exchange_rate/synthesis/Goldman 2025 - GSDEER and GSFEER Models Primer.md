# A Primer on Goldman Sachs' GSDEER and GSFEER Models

**Authors:** Teresa Alves, Stuart Jenkins  
**Source:** Goldman Sachs FX in Focus, 3 November 2025  
**Type:** Research note — proprietary fair value framework  
**Tags:** #fair-value #PPP #GSDEER #GSFEER #valuation #exchange-rate #goldman-sachs  
**Raw file:** [[primer_gsdeer_gsfeer (Goldman, 2025)]]

---

## Summary

Goldman Sachs maintains two complementary FX fair value models:

- **GSDEER** (Goldman Sachs Dynamic Equilibrium Exchange Rate) — long-run, based on augmented PPP. Structural.
- **GSFEER** (Goldman Sachs Fundamental Equilibrium Exchange Rate) — medium-run, based on cyclical macroeconomic balance. Cyclical.

The two models often give different signals, which is by design. GSDEER tells you where the exchange rate *should* be in the long run given structural fundamentals; GSFEER tells you where it *should* be once cyclical factors normalize. The gap between them reflects the cyclical misalignment component.

As of November 2025: the **Dollar is ~15% overvalued** on GSDEER. **BRL is undervalued on GSDEER but near norm on GSFEER** — meaning structural cheapness, but cyclical factors (carry, terms of trade) keep it from converging.

---

## GSDEER — Long-Run Structural Model

### Concept

GSDEER is an augmented PPP model. Raw PPP fails because of the Balassa-Samuelson effect (richer countries have structurally stronger currencies due to productivity differentials in tradables). GSDEER corrects for this by regressing the real exchange rate on fundamentals that drive systematic PPP deviations.

### Regression specification

```
REER = f(inflation differential vs US, terms of trade, productivity differential vs US)
```

All variables are measured relative to the US. The fitted value from this regression is the GSDEER fair value.

**Key drivers:**
| Driver | Direction | Intuition |
|---|---|---|
| Relative inflation (domestic vs US) | Negative | Higher domestic inflation → REER depreciates toward PPP |
| Terms of trade | Positive | Better ToT → stronger equilibrium REER |
| Relative productivity (Balassa-Samuelson) | Positive | Faster productivity growth in tradables → REER appreciation |

### Estimation

- Cross-country panel regression
- Long time series (decades) to capture structural relationships
- Residuals are the misalignment: positive = overvalued, negative = undervalued

### Convergence

GSDEER convergence is slow — roughly **~20%/year rule of thumb for G10** currencies. For EM, convergence is even slower or absent over medium horizons because carry, risk premium, and ToT volatility dominate.

---

## GSFEER — Medium-Run Cyclical Model

### Concept

GSFEER is a medium-run equilibrium concept based on macroeconomic balance. The question is: what exchange rate is consistent with the current account returning to its structural norm, given the current cyclical position?

### Two-step framework

**Step 1 — Current account norm:**  
Estimate the "structural" or "norm" current account (CA*) for each country based on fundamentals (demographics, stage of development, fiscal position, etc.).

**Step 2 — Exchange rate consistent with closing the gap:**  
Given the actual CA and the norm CA*, find the REER that would bring the CA back to norm, also accounting for the output gap.

```
GSFEER gap = f(CA − CA*, output gap)
```

### Key difference from GSDEER

GSFEER is explicitly **cyclical** — it moves with the business cycle, fiscal stance, and commodity prices. GSDEER is structural and moves much more slowly. In practice:
- GSFEER changes quarter to quarter as CA data and output gaps are revised
- GSDEER is more stable (structural drivers move slowly)

---

## Using the Two Models Together

| Situation | Interpretation |
|---|---|
| Currency cheap on both GSDEER and GSFEER | Strong undervaluation signal — structural AND cyclical |
| Currency cheap on GSDEER, near fair on GSFEER | Structural cheapness, but cyclical balance is already there; convergence requires structural shift |
| Currency cheap on GSDEER, expensive on GSFEER | Structural undervaluation offset by cyclical overvaluation — mixed signal |
| Both show overvaluation | Strong overvaluation — avoid or short |

The convergence question is separate: even if a currency is 20% cheap, it may not converge if carry is unfavorable or risk premium is high.

---

## BRL — Case Study (November 2025)

| Model | Signal | Magnitude |
|---|---|---|
| GSDEER | **Undervalued** | Material — BRL structurally cheap |
| GSFEER | **Near norm** | Cyclical position roughly balanced |

**Goldman's interpretation:** BRL undervaluation on GSDEER is real but convergence is low-probability in the medium run because:
1. **Carry dominates**: BRL positioning is driven by carry (Selic − Fed Funds differential), not structural valuation
2. **Terms of trade** are the main structural driver and are volatile (commodity prices)
3. **Risk premium** around fiscal/political uncertainty keeps BRL structurally weak

The implication: don't use GSDEER cheapness as a buy signal for BRL without a carry or ToT catalyst.

---

## USD — Global View (November 2025)

- Dollar is **~15% overvalued** on GSDEER
- Overvaluation driven by: US productivity outperformance (AI narrative), high carry (restrictive Fed), capital inflows (equity market premium)
- GSFEER also shows USD overvaluation, but less extreme — US CA deficit is large but partially justified by investment boom

**Implication:** structural USD depreciation is the long-run base case, but timing is highly uncertain. Convergence has been slow for years precisely because the drivers of overvaluation (productivity, carry, safe-haven) remain in place.

---

## Limitations of Both Models

1. **GSDEER** is sensitive to the productivity and ToT measures used — different deflators give different fair values
2. **GSFEER** CA norm is model-dependent and frequently revised
3. Neither model captures **risk premium** — currencies can be structurally cheap and stay cheap for years if risk premium is high
4. Convergence rates are empirically unstable — the 20%/yr rule of thumb has large standard errors
5. Neither model works well for currencies with capital controls, FX intervention regimes, or dollarized economies

---

## Connections in the bibliography

- [[Goldman 2023 - GSDEER A User's Manual]] — deeper technical treatment of the GSDEER methodology
- [[Dornbusch 1976]] — overshooting means fair value is a long-run concept; short-run deviations are rational
- [[Mundell 1963]] / [[Fleming 1962]] — GSFEER is implicitly a macro balance model in the M-F tradition
- [[verde_fx_mental_models]] — Verde letters treat GSDEER-type arguments as "structural" floor for BRL; skeptical of convergence without carry catalyst
- [[Sarno-Taylor]] — academic treatment of PPP-based equilibrium exchange rates and their empirical limitations
- [[Paiva 2006 - External Adjustment and Equilibrium Exchange Rate in Brazil]] — BEER model, the direct methodological ancestor applied to Brazil two decades earlier: same terms-of-trade/productivity/NFA/risk-premium fundamentals, cointegration instead of a cross-sectional regression
