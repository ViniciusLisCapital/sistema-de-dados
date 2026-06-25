# Purchasing Power Parity (PPP) and the Balassa-Samuelson Effect

**Type:** Exchange rate theory / empirical regularity  
**Tags:** #ppp #balassa-samuelson #reer #fair-value #inflation #gsdeer

---

## Purchasing Power Parity (PPP)

### Statement

The exchange rate adjusts to equalize the price levels of two countries when expressed in the same currency.

**Absolute PPP:**
```
e = P_domestic / P_foreign
```
If a basket costs BRL 600 in Brazil and USD 100 in the US, the PPP exchange rate is 6.00 BRL/USD.

**Relative PPP:**
```
Δe = π_domestic − π_foreign
```
The rate of currency depreciation equals the inflation differential. Brazil inflating 5% above the US → BRL depreciates ~5%/year.

---

### When PPP holds — and when it doesn't

| Context | PPP validity |
|---|---|
| Long run, traded goods | Generally holds (law of one price in tradables) |
| Short run | **Fails** — exchange rates are far more volatile than price differentials (Dornbusch overshooting) |
| Non-traded goods (haircuts, housing) | **Fails** — Balassa-Samuelson effect |
| EM vs. DM comparison | **Fails systematically** — richer countries are structurally "expensive" even in equilibrium |

In Dornbusch (1976), PPP is only the *long-run* equilibrium condition (`ē = p̄ − p̄*`). The paper's entire contribution is explaining why the exchange rate can deviate from PPP in the short run while still being on an equilibrium path.

---

## The Balassa-Samuelson Effect

### What it is

Richer, more productive countries have **higher price levels** than raw PPP predicts. Their real effective exchange rates (REER) are systematically stronger than their absolute PPP level would imply.

### Mechanism

1. In the tradable sector, productivity is high in developed countries → wages are high.
2. Wages equalize across sectors within a country (labor mobility).
3. High wages flow into the non-tradable sector → high prices for services, housing, haircuts.
4. The country appears expensive on absolute PPP, even though its *tradable* prices are globally competitive.

**Implication for EM:** A simple PPP comparison makes EM currencies look perpetually "cheap" — but the cheapness is structural (development gap), not misalignment. Fair value models must **correct for Balassa-Samuelson** to identify true deviations.

---

## GSDEER as Augmented PPP

Goldman's GSDEER corrects raw PPP for the systematic drivers of PPP deviations:

```
REER_fair = f(inflation differential vs US, terms of trade, productivity differential vs US)
```

| Driver | Direction | Why |
|---|---|---|
| Relative inflation | Negative | Higher domestic inflation → REER depreciates toward PPP |
| Terms of trade | Positive | Better ToT → equilibrium REER is stronger |
| Relative productivity (Balassa-Samuelson) | Positive | Faster TFP growth in tradables → equilibrium REER appreciates |

The fitted value from this regression is GSDEER fair value. The residual (actual − fair) is the misalignment.

### BRL on GSDEER (November 2025)

BRL is **undervalued** on GSDEER — after correcting for Brazil's productivity level and terms of trade, BRL is trading below the structural equilibrium. However:
- The undervaluation is not sufficient as a buy signal alone (see [[risk_premium]])
- Convergence to GSDEER fair value is slow (~20%/year, 3–5 years to beat random walk in G10)
- For EM, convergence is even slower because carry and risk premium dominate medium-term positioning

---

## Connections

- [[Dornbusch 1976 - Expectations and Exchange Rate Dynamics]] — long-run PPP (`ē = p̄ − p̄*`) is the anchor; the model explains short-run deviations
- [[Goldman 2025 - GSDEER and GSFEER Models Primer]] — GSDEER as augmented PPP correcting for Balassa-Samuelson; BRL undervalued on GSDEER
- [[Goldman 2023 - GSDEER A User's Manual]] — empirical PPP convergence: ~20%/yr, 3–5yr to beat random walk; BRL convergence blocked by high risk premium
- [[verde_fx_mental_models]] — Verde uses relative PPP as baseline for BRL trend (inflation differential vs US); carry is the deviation from the PPP path
- [[risk_premium]] — even with GSDEER undervaluation, BRL may not converge if the risk premium is high enough to block carry flows
