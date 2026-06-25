---
aliases: ["Fleming 1962"]
---

# Domestic Financial Policies Under Fixed and Under Floating Exchange Rates

**Author:** J. Marcus Fleming  
**Source:** Staff Papers — International Monetary Fund, vol. 9, no. 3 (November 1962), pp. 369–380  
**Type:** Foundational theoretical article  
**Tags:** #mundell-fleming #exchange-rate #fiscal-policy #monetary-policy #fixed-vs-floating #foundational

---

## Summary

Fleming develops, independently of Mundell (1963), the same open-economy model with capital mobility. The central contribution is a systematic comparison of the effectiveness of fiscal vs. monetary policy under fixed and floating exchange rates. The canonical result: **monetary policy is more powerful under floating rates; fiscal policy is more powerful (or at least not neutralized) under fixed rates.**

The paper predates Mundell's formal publication but both arrived at the model quasi-simultaneously while at the IMF.

---

## The Model

### Structure

Small open Keynesian economy. Three markets: goods, money, international capital.

**Goods market equilibrium (IS):**
```
Y = C(Y) + I(r) + G + X(e) − M(Y, e)
```
Net exports improve with depreciation (`e↑`). Output `Y` is endogenous.

**Money market equilibrium (LM):**
```
M_s = L(Y, r)
```
Money supply is exogenous (or endogenous under fixed rates). Interest rate `r` is endogenous.

**Capital mobility:**
```
BP = CA(Y, e) + KA(r − r*)
```
Capital account `KA` is increasing in the interest rate differential. Fleming tests two cases: partial and perfect mobility.

---

## Main Results

### 1. Fiscal expansion (↑G) under fixed exchange rates

| Effect | Mechanism |
|---|---|
| ↑Y | Direct spending multiplier |
| ↑r | IS shifts right, interest rate rises |
| ↑KA | Capital inflow attracted by higher r |
| Central bank buys FX | Defends the peg against appreciation pressure |
| ↑M_s (endogenous) | Endogenous money expansion amplifies the fiscal effect |

**Conclusion:** Fiscal policy **works** under fixed rates — the central bank validates the expansion with an endogenous increase in M.

---

### 2. Fiscal expansion (↑G) under floating exchange rates

| Effect | Mechanism |
|---|---|
| ↑Y (on impact) | Initial multiplier |
| ↑r | IS shifts right |
| ↑KA | Capital inflow |
| Exchange rate appreciates | Excess demand for domestic currency |
| ↓NX | Exports fall, imports rise |
| External crowding-out | NX decline offsets the ↑G |

**Conclusion:** Fiscal policy has a **weak or ambiguous effect** under floating rates. With perfect capital mobility, appreciation fully offsets the output effect (complete external crowding-out — Mundell formalizes this more sharply).

---

### 3. Monetary expansion (↑M) under fixed exchange rates

| Effect | Mechanism |
|---|---|
| ↓r | LM shifts right |
| ↓KA | Capital outflow (domestic rate < foreign rate) |
| Depreciation pressure | Balance of payments deficit |
| Central bank sells reserves | To defend the peg |
| ↓M_s (endogenous) | The original expansion reverses itself |

**Conclusion:** Monetary policy is **impotent** under fixed rates with capital mobility — the expansion is self-canceling via reserve loss.

---

### 4. Monetary expansion (↑M) under floating exchange rates

| Effect | Mechanism |
|---|---|
| ↓r | LM shifts right |
| Exchange rate depreciates | Capital outflow creates demand for foreign currency |
| ↑NX | Exports rise, imports fall |
| ↑Y additional | Depreciation stimulates demand for domestic goods |

**Conclusion:** Monetary policy is **powerful** under floating rates — the exchange rate channel amplifies the expansionary effect.

---

## Summary Table (Fleming)

| Instrument | Fixed exchange rates | Floating exchange rates |
|---|---|---|
| Fiscal policy (↑G) | **Effective** (endogenous M validates) | **Weak** (external crowding-out) |
| Monetary policy (↑M) | **Ineffective** (reserves self-cancel) | **Effective** (exchange rate channel amplifies) |

---

## The Speculative Element in Capital Flows

Fleming devotes a section to short-term capital with a speculative component: if a depreciation generates an expectation of further depreciation, the sensitivity of KA to the interest differential increases. The qualitative results survive, but the effects are amplified.

This is the seed of what Dornbusch (1976) will formalize as overshooting under rational expectations.

---

## Mathematical Appendix

Fleming derives formally the stability conditions and multipliers. The conditions revolve around trade elasticities (Marshall-Lerner) and the interest sensitivity of capital flows.

**Implicit Marshall-Lerner condition:** depreciation improves the trade balance (`∂NX/∂e > 0`), which is the prerequisite for the exchange rate channel to work in the right direction.

---

## Limitations of the model

1. **No dynamics** — everything is static; no adjustment path or explicit expectations
2. **Fixed prices** — no inflation or explicit price stickiness
3. **Perfect asset substitutability** — no risk premium, no asset differentiation
4. **Small country** — no feedback on the foreign interest rate `r*`
5. **No wealth or asset accumulation** — flow equilibrium only, no stock condition

---

## Connections in the bibliography

- [[Mundell 1963]] — parallel version; Mundell makes perfect capital mobility analysis cleaner and adds the inflation model
- [[Dornbusch 1976]] — extends with dynamic expectations and sticky prices → generates overshooting
- [[Obstfeld-Rogoff]] — microfoundation of the Mundell-Fleming model (Redux, General Equilibrium)
- [[Sarno-Taylor]] — critiques of M-F and extensions with risk premium and portfolio balance

---

## Relevance for BRL/USD today

| Situation | M-F reading |
|---|---|
| BCB cuts Selic (↓r) | BRL depreciates; NX improves; expansionary real effect via depreciation |
| Fiscal expansion without sterilization (Brazil 2023) | Under floating: r rises, partial appreciation, partial external crowding-out; but with Brazil risk premium, BRL may still depreciate |
| Fed hikes rates (↑r*) | ↓(r − r*) → capital outflow from Brazil → BRL depreciation → M-F predicts expansionary effect on Brazil via NX, but in practice imported inflation dominates |
| BCB FX intervention | Equivalent to trying to operate as a fixed rate in a high capital mobility environment — reserve loss predicted by M-F |
