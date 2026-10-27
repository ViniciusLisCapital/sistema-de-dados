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

CIP holds empirically (enforced by arbitrage). **UIP fails empirically** — the "forward premium puzzle": high-yield currencies tend to *appreciate* rather than depreciate as UIP predicts. A common reading is that a time-varying risk premium partially explains this failure; Froot and Thaler find no positive evidence for it and, from survey data, trace the bias to expectational errors. Both readings are kept: see [[forward_premium_puzzle]].


---

## How UIP appears in the bibliography

| Source                                                                                                      | Role                                                                                                                                  |
| ----------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| [[verde_fx_mental_models]]                                                                                  | Carry trade (section 3.1) is UIP expressed as investment strategy: collect `r − r*` for as long as depreciation does not materialize. |
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

- [[carry_trade]] — the carry trade is a bet on the empirical failure of UIP
- [[overshooting]] — overshooting is driven by UIP: the exchange rate must be far out of equilibrium so the return path satisfies UIP
- [[risk_premium]] — the extended form of UIP; one of the two readings of the forward premium puzzle (the other, expectational errors, in [[forward_premium_puzzle]])
- [[fiscal_dominance]] — when fiscal stress dominates, rate hikes raise ρ and break UIP carry logic entirely
- [[ppp_balassa_samuelson]] — real interest parity is UIP's real-terms analogue, linking interest differentials to expected real exchange rate change instead of nominal depreciation
- [[currency_regimes]] — the Impossible Trinity is UIP's "credibly fixed + fully convertible ⇒ zero independent monetary policy" logic restated as a policy trilemma
- [[monetary_policy/synthesis/monetary_policy_exchange_rates (BIS, 2026)]] — shows the simple "tightening → appreciation" intuition is unreliable in *magnitude*: prior carry positioning in the currency makes the same-size policy surprise produce a ~4-10x larger FX response, a state-dependence UIP alone doesn't predict
- [[exchange_rate/synthesis/fx_anomalies_survey (Froot & Thaler, 1990)]] — survey of the forward discount bias, the empirical rejection of UIP with unbiased expectations
