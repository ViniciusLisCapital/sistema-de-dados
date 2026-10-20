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

**Empirical horizon-dependence (CFA L2):** plotting inflation differentials against exchange rate changes shows no relationship at a 1-year horizon but a clear positive (PPP-consistent) one at 5+ years — PPP's signal is swamped by noise at short horizons, not absent. The clearest confirming case is Brazil 1977–1993: the BRL/USD rate tracked the Brazil-US inflation differential almost exactly even at a 1-year horizon, because the inflation gap was so large (hyperinflationary) it dominated all the usual short-horizon noise. See [[exchange_rate/synthesis/exchange_rate_understanding_equilibrium (CFA L2, 2025)]].

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

### A competing explanation: Bhagwati-Kravis-Lipsey

Krugman's textbook treatment (Ch. 16) notes the Balassa-Samuelson productivity story is not the only explanation for why rich countries have higher price levels. Bhagwati-Kravis-Lipsey attributes it to **capital-labor ratios** instead of a tradables-specific productivity gap: rich countries have more capital per worker, which raises the marginal product (and hence wage) of labor directly; since nontradables are labor-intensive, higher wages raise nontradables prices — same cross-country prediction, different mechanism (no need for productivity growth to be *concentrated* in tradables). The two theories are not nested and the textbook does not adjudicate between them.

### Real exchange rate and real interest parity

Krugman formalizes the real exchange rate as `q = (E · P_foreign) / P_domestic` — the relative price of the foreign consumption basket in domestic terms — and shows its long-run level is set by relative demand/supply for output, not by money (a rise in relative demand for domestic output → real appreciation; a rise in domestic relative output supply → real depreciation). Combining this with UIP gives **real interest parity**: `r_domestic^e − r_foreign^e = E[Δq]` — countries' expected real interest rates need not converge even in the long run if a real exchange rate trend (e.g., ongoing Balassa-Samuelson appreciation) is expected. See [[exchange_rate/synthesis/price_levels_exchange_rate_lr (Krugman, 2023)]].

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

- [[exchange_rate/synthesis/expectations_and_exchange_rate_dynamics (Dornbusch, 1976)]] — long-run PPP (`ē = p̄ − p̄*`) is the anchor; the model explains short-run deviations
- [[exchange_rate/synthesis/primer_gsdeer_gsfeer (Goldman, 2025)]] — GSDEER as augmented PPP correcting for Balassa-Samuelson; BRL undervalued on GSDEER
- [[exchange_rate/synthesis/gsdeer_manual_guide (Goldman, 2023)]] — empirical PPP convergence: ~20%/yr, 3–5yr to beat random walk; BRL convergence blocked by high risk premium
- [[verde_fx_mental_models]] — Verde uses relative PPP as baseline for BRL trend (inflation differential vs US); carry is the deviation from the PPP path
- [[kapitalo_fx_mental_models]] — 2.1–2.2: explicit PPP/REER valuation model with a Balassa-Samuelson/relative-unit-labor-cost component, laid out as a formal table ("Vetores e Indicadores Econômicos para Câmbio de Moedas") in the fund's inaugural 2019 letter and applied implicitly ever since
- [[risk_premium]] — even with GSDEER undervaluation, BRL may not converge if the risk premium is high enough to block carry flows
- [[exchange_rate/synthesis/price_levels_exchange_rate_lr (Krugman, 2023)]] — fullest textbook derivation of absolute/relative PPP, the monetary approach, the real exchange rate, real interest parity, and the Bhagwati-Kravis-Lipsey alternative to Balassa-Samuelson
- [[uip]] — Fisher effect and real interest parity split nominal UIP into an inflation-expectations component and a real-exchange-rate-expectations component
- [[exchange_rate_pass_through]] — pricing-to-market and market segmentation (this page's PPP-failure mechanisms) are the same forces behind incomplete pass-through
- [[exchange_rate/synthesis/output_exchange_rates_sr (Krugman, 2023)]] — uses this page's real exchange rate `q = EP*/P` as the operative variable in the current-account/DD-AA model
- [[exchange_rate/synthesis/capital_flow_fx_market (CFA L1, 2025)]] — same real exchange rate definition with a clean worked example (India 2018 INR/USD); reinforces PPP's weak predictive track record from the practitioner side
- [[currency_regimes]] — Impossible Trinity and IMF regime taxonomy built from this reading's companion source
- [[exchange_rate/synthesis/exchange_rate_understanding_equilibrium (CFA L2, 2025)]] — real interest rate parity via ex ante PPP + UIP; horizon-dependent empirical PPP evidence; Brazil 1977–93 hyperinflation as cleanest confirming case
- [[balance_of_payments_approach]] — complementary long-run channel: PPP explains price-level-driven trend, BOP/portfolio-balance explain debt/flow-driven trend
- [[exchange_rate/synthesis/equilibrium_exchange_brazil (Paiva, 2006)]] — BEER model direct methodological ancestor of GSDEER; NTT (CPI/PPI ratio) as an empirical Balassa-Samuelson proxy explaining Brazil's 2003–05 REER appreciation
