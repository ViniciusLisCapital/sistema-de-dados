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

CIP holds empirically (enforced by arbitrage). **UIP fails empirically** — the "forward premium puzzle": high-yield currencies tend to *appreciate* rather than depreciate as UIP predicts. This failure is partially explained by a time-varying risk premium.

CIP itself broke down persistently after the 2007–08 crisis and has not fully re-normalized since — not explained by counterparty default risk (Du, Tepper & Verdelhan 2018); the leading explanation is that post-crisis balance-sheet/collateral constraints limit arbitrageurs' capacity to close the gap, even though the arbitrage is riskless in principle. See [[exchange_rate/synthesis/exchange_rate_foreign_exchange_market (Krugman, 2023)]].

---

## How UIP appears in the bibliography

| Source                                                                                                      | Role                                                                                                                                  |
| ----------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| [[exchange_rate/synthesis/expectations_and_exchange_rate_dynamics (Dornbusch, 1976)]]                                                | Central equation: with rational expectations, `ε = θ(ē − e)`. UIP + sticky prices → overshooting.                                     |
| [[exchange_rate/synthesis/capital_mobility_exchange_rates_regimes (Mundell, 1963)]] and [[Fleming 1962 - Domestic Financial Policies Under Fixed and Floating Exchange Rates]] | Implicit: perfect capital mobility collapses UIP to `r = r*` at all times. This is the mechanism behind policy impotence.             |
| [[exchange_rate/synthesis/primer_gsdeer_gsfeer (Goldman, 2025)]]                                                          | Carry (UIP-derived) is what drives positioning in the short run, overriding structural GSDEER signals.                                |
| [[verde_fx_mental_models]]                                                                                  | Carry trade (section 3.1) is UIP expressed as investment strategy: collect `r − r*` for as long as depreciation does not materialize. |
| [[kinea_fx_mental_models]]                                                                                  | 2.1–2.2: rate differential and the "FX channel" (`vs. US`) as the practical transmission mechanism, an explicit real-world echo of UIP's empirical failure. |
| [[kapitalo_fx_mental_models]]                                                                               | 3.1, 5.1–5.2: growth/monetary-policy divergence as the persistent, recurring FX driver applied cross-country year after year. |
| [[exchange_rate/synthesis/exchange_rate_foreign_exchange_market (Krugman, 2023)]]                       | Formal derivation of the UIP equilibrium diagram (interest-rate schedule vs. expected-return schedule); documents the CIP variant and its post-2008 breakdown. |
| [[monetary_policy/synthesis/fiscal_dominance_it_brazil (Blanchard, 2004)]] | Risk-adjusted parity with default risk: once the risk premium is controlled for, the Selic–Fed funds differential has no consistent effect on the exchange rate (Brazil 1999–2004). |

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
- [[risk_premium]] — the extended form of UIP that explains the forward premium puzzle
- [[fiscal_dominance]] — when fiscal stress dominates, rate hikes raise ρ and break UIP carry logic entirely
- [[fiscal_policy/synthesis/fiscal_dominance (itau, 2025)]] — Blanchard (2004) mechanism: fiscal stress raises ρ faster than r, causing BRL depreciation despite rate hikes
- [[exchange_rate/synthesis/exchange_rate_foreign_exchange_market (Krugman, 2023)]] — textbook derivation of UIP/CIP and the post-2008 CIP breakdown puzzle
- [[exchange_rate/synthesis/money_interest_rate_exchange_rates (Krugman, 2023)]] — supplies the missing piece (national money-market equilibrium) that pins down R in the UIP condition
- [[exchange_rate/synthesis/price_levels_exchange_rate_lr (Krugman, 2023)]] — decomposes nominal UIP into the Fisher effect (inflation-expectations component) and real interest parity (real-exchange-rate-expectations component)
- [[ppp_balassa_samuelson]] — real interest parity is UIP's real-terms analogue, linking interest differentials to expected real exchange rate change instead of nominal depreciation
- [[exchange_rate/synthesis/fixed_exchange_rate_intervention (Krugman, 2023)]] — imperfect asset substitutability extends UIP with a risk premium `ρ(B−A)` tied to central bank balance sheet composition; this is what makes sterilized FX intervention effective
- [[exchange_rate/synthesis/exchange_rate_calculation (CFA L1, 2025)]] — practitioner-side CIP derivation via swap financing, forward points/pips mechanics, and day-count-scaled maturity arithmetic underlying the covered variant in the table above
- [[currency_regimes]] — the Impossible Trinity is UIP's "credibly fixed + fully convertible ⇒ zero independent monetary policy" logic restated as a policy trilemma
- [[exchange_rate/synthesis/exchange_rate_understanding_equilibrium (CFA L2, 2025)]] — full CIP→UIP→forward-rate-parity chain; real interest rate parity via ex ante PPP + UIP; the risk-neutral-speculation mechanism explaining why UIP holds at all absent arbitrage
- [[mundell_fleming_policy_mix]] — the high-capital-mobility channel of Mundell-Fleming is UIP-driven capital flow response to rate differentials
- [[monetary_policy/synthesis/monetary_policy_exchange_rates (BIS, 2026)]] — shows the simple "tightening → appreciation" intuition is unreliable in *magnitude*: prior carry positioning in the currency makes the same-size policy surprise produce a ~4-10x larger FX response, a state-dependence UIP alone doesn't predict
- [[monetary_policy/synthesis/fiscal_dominance_it_brazil (Blanchard, 2004)]] — capital-flow relation as a risk-adjusted interest parity; the interest differential is insignificant and often wrong-signed once default risk is priced
