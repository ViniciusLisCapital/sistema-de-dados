# Uncovered Interest Parity (UIP)

**Type:** Core arbitrage condition  
**Tags:** #uip #interest-parity #arbitrage #capital-mobility

---

## Statement

The expected return on domestic and foreign assets must be equal when expressed in the same currency:

```
r = r* + E[Δe]
```

where:
- `r` = domestic interest rate
- `r*` = foreign interest rate
- `E[Δe]` = expected rate of exchange rate depreciation (domestic per foreign)

**Implication:** If domestic rates exceed foreign rates, the domestic currency must be expected to depreciate by exactly the interest differential. The higher yield compensates for anticipated depreciation.

---

## Intuition

Capital is perfectly mobile and risk-neutral. Any domestic-foreign yield differential creates arbitrage flows until the differential is closed — either by rate adjustment or by exchange rate movement. UIP is the equilibrium condition where no arbitrage opportunity remains.

UIP is not a behavioral assumption. It is an **arbitrage-free pricing condition** for financial markets with free capital flows.

---

## Variants

| Variant | Assumption | Formula |
|---|---|---|
| Uncovered (UIP) | No exchange rate risk; rational expectations | `r = r* + E[Δe]` |
| Covered (CIP) | Forward rate locks in the exchange | `r = r* + f − e` (f = log forward rate) |
| UIP + risk premium | Risk-averse investors | `r = r* + E[Δe] + ρ` (ρ = risk premium) |



---

## How UIP appears in the bibliography

| Source                                                                                                      | Role                                                                                                                                  |
| ----------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| [[verde_fx_mental_models]]                                                                                  | Carry trade (section 3.1) is UIP expressed as investment strategy: collect `r − r*` for as long as depreciation does not materialize. |
| [[kapitalo_fx_mental_models]]                                                                               | 3.1, 5.1–5.2: growth/monetary-policy divergence as the persistent, recurring FX driver applied cross-country year after year. |
| [[monetary_policy/synthesis/fiscal_dominance_it_brazil (Blanchard, 2004)]] | Risk-adjusted parity with default risk: once the risk premium is controlled for, the Selic–Fed funds differential has no consistent effect on the exchange rate (Brazil 1999–2004). |
| [[monetary_policy/synthesis/trilemma_tradeoffs (Obstfeld, 2015)]] | Interest parity with a currency risk premium (1) links EME and US short rates; a long-term version (3) adds term premia, so a 10 basis point fall in a US two-year term premium requires a 20 basis point appreciation if EME long rates do not move |
| [[monetary_policy/synthesis/us_policy_international_risk_spillovers (Kalemli-Ozcan, 2019)]] | "Risk-adjusted UIP" with a country risk premium that rises with US rates; UIP deviations move with interest differentials in EMEs and with exchange rates in advanced economies; a 1 point US tightening raises the EME deviation by about 3 points |
| [[monetary_policy/synthesis/implementing_it_brazil (Bogdanski, Tombini & Werlang, 2000)]] | The exchange-rate block of the BCB's first structural model: UIP with a risk premium in first differences, the foreign rate from futures and the risk premium as the volatile exogenous (or fiscal-driven) term |
| [[exchange_rate/synthesis/equilibrium_exchange_brazil (Paiva, 2006)]] | The real interest rate differential (RINTDIFF) is the BEER model's direct UIP channel for Brazil: higher domestic real rates go with a stronger real exchange rate |
| [[exchange_rate/synthesis/fx_anomalies_survey (Froot & Thaler, 1990)]] | The unbiasedness test of UIP: the slope of realized depreciation on the interest differential (or forward discount) is reliably below one and often negative; the bias is traced to expectational errors rather than a risk premium |

---

## BRL/USD application

| Situation                              | UIP reading                                                                                                                                                                |
| -------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| BCB hikes Selic                        | UIP says BRL must be expected to depreciate by ≈ Δ(Selic − Fed Funds). Short-run: BRL appreciates (carry inflow). Long-run: BRL depreciates as the advantage is priced in. |
| Fed hikes Fed Funds                    | UIP says BRL must depreciate (or Brazilian rates must rise in parallel) to restore parity.                                                                                 |
| BRL risk premium rises (fiscal stress) | `ρ > 0` means Brazil must pay above UIP — Selic compensates for risk, not just for expected depreciation. BRL can weaken despite high rates.                               |

---

## See also

- [[risk_premium]] — the extended form of UIP; one of the two readings of the forward premium puzzle (the other, expectational errors, in forward_premium_puzzle)
- [[fiscal_dominance]] — when fiscal stress dominates, rate hikes raise ρ and break UIP carry logic entirely
- [[currency_regimes]] — the Impossible Trinity is UIP's "credibly fixed + fully convertible ⇒ zero independent monetary policy" logic restated as a policy trilemma
- [[monetary_policy/synthesis/monetary_policy_exchange_rates (BIS, 2026)]] — shows the simple "tightening → appreciation" intuition is unreliable in *magnitude*: prior carry positioning in the currency makes the same-size policy surprise produce a ~4-10x larger FX response, a state-dependence UIP alone doesn't predict
- [[monetary_policy/synthesis/fiscal_dominance_it_brazil (Blanchard, 2004)]] — capital-flow relation as a risk-adjusted interest parity; the interest differential is insignificant and often wrong-signed once default risk is priced
- [[monetary_policy/synthesis/trilemma_tradeoffs (Obstfeld, 2015)]] — short- and long-term interest parity as the channel through which US rates and term premia reach emerging markets
- [[monetary_policy/synthesis/us_policy_international_risk_spillovers (Kalemli-Ozcan, 2019)]] — UIP deviations as the footprint of US-driven risk spillovers, and why defending the currency with rates is costly when they are large
- [[monetary_policy/synthesis/implementing_it_brazil (Bogdanski, Tombini & Werlang, 2000)]] — UIP plus a risk premium as the exchange-rate equation of the BCB's policy models
- [[exchange_rate/synthesis/fx_anomalies_survey (Froot & Thaler, 1990)]] — survey of the forward discount bias, the empirical rejection of UIP with unbiased expectations
