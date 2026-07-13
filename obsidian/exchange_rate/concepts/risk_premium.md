# FX Risk Premium

**Type:** Concept / empirical regularity  
**Tags:** #risk-premium #uip #carry #fair-value #brl #emerging-markets #fiscal

---

## Definition

The **FX risk premium** is the extra return demanded by investors to hold a risky currency beyond what UIP alone would require.

Extended UIP with risk premium:
```
r = r* + E[Δe] + ρ
```

where `ρ` is the risk premium. If `ρ > 0`, investors demand a return above the expected depreciation — the currency must offer a higher yield than pure UIP requires to attract and retain capital.

---

## Why it exists

Investors are risk-averse and face several dimensions of currency risk:

1. **Depreciation risk** — sudden collapses (currency crises, sudden stops)
2. **Sovereign/political risk** — government may default, impose capital controls, or monetize debt
3. **Liquidity risk** — thin EM markets amplify losses during stress
4. **Correlated risk** — EM currencies crash together in global risk-off (undiversifiable)

For bearing these risks, investors require a premium. The currency must carry *more* than the pure UIP condition to attract capital.

---

## The key implication: a currency can stay "cheap"

**The most important consequence:** a currency can be structurally undervalued on PPP or GSDEER and still fail to appreciate if its risk premium is high enough to deter the inflows that would drive convergence.

Goldman explicitly flags this for both GSDEER and GSFEER:
> "Neither model captures risk premium — currencies can be structurally cheap and stay cheap for years if risk premium is high."

For BRL specifically (Goldman, November 2025): BRL is undervalued on GSDEER, but convergence is unlikely without a carry or terms-of-trade catalyst, because the risk premium absorbs the yield advantage before it can drive structural inflows.

---

## Sources of BRL risk premium

| Source | Mechanism |
|---|---|
| Fiscal uncertainty | Investors price probability of debt crisis, monetization, or primary deficit blow-out |
| Political risk | Institutional deterioration, attacks on BCB independence, discretionary policy |
| Sub-investment grade rating | Mandatory exclusion from investment-grade mandates permanently reduces demand |
| Carry unwind correlation | BRL is high-beta EM — crash risk is priced into the premium |
| Fiscal dominance | When fiscal constraints bind monetary policy, the real return on BRL assets is uncertain |

---

## Risk premium vs. carry: the operative trade-off

| Concept | Definition | When it dominates |
|---|---|---|
| Carry (`r − r*`) | Nominal interest differential | Stable macro, global risk-on, low political noise |
| Risk premium (`ρ`) | Extra return for risk-bearing | Fiscal deterioration, political stress, global risk-off |
| Effective carry | `(r − r*) − ρ` | The actual return to holding BRL |

**The Verde observation (May 2024):** Brazilian real rates hit their highest level since the tightening cycle began — and BRL still weakened. The risk premium had risen faster than the carry, making the effective carry negative. This is the proof of concept that nominal yield is an insufficient statistic.

---

## Risk premium and overshooting

When risk premium spikes (fiscal shock, political crisis), the BRL can depreciate well beyond any equilibrium level implied by fundamentals — this is "risk-premium overshooting" distinct from the Dornbusch monetary overshooting. The mechanism:

1. `ρ` rises suddenly → effective carry collapses → carry unwind
2. BRL depreciates sharply → overshoots new equilibrium
3. If the source of `ρ` resolves (new fiscal rule, hawkish BCB signal), BRL mean-reverts

Verde's "ruído vs. sinal" framework (section 1.6 in [[verde_fx_mental_models]]) is about distinguishing transient risk premium spikes (fade them) from permanent regime shifts in `ρ` (stay short).

---

## A microfoundation: relative bond supply (Krugman)

Krugman's textbook treatment of imperfect asset substitutability gives `ρ` a specific formal driver: `ρ = ρ(B − A)`, where `B` is the stock of domestic government debt the private market must hold and `A` is the central bank's own domestic asset holdings. More debt for the market to absorb (higher `B − A`) raises the risk premium; central bank purchases of domestic assets (higher `A`, e.g., QE-style operations) lower it. This is a narrower, balance-sheet-specific version of the qualitative "fiscal uncertainty" channel below — it's also the mechanism that makes **sterilized FX intervention** effective: swapping central bank foreign for domestic assets changes `B − A` and thus `ρ`, moving the exchange rate even with the money supply unchanged. See [[Krugman 2023 - Fixed Exchange Rates and Foreign Exchange Intervention]].

---

## Connections

- [[uip]] — risk premium is the extension of UIP: `r = r* + E[Δe] + ρ`; it explains the forward premium puzzle
- [[Krugman 2023 - Fixed Exchange Rates and Foreign Exchange Intervention]] — formal microfoundation `ρ(B−A)`; sterilized intervention as a risk-premium (not money-supply) channel; Swiss franc 2011–2015 case study
- [[balance_of_payments_approach]] — the portfolio balance approach is the qualitative version of this same debt-stock-driven risk premium: sustained fiscal deficits require compensation via rates, risk premium, or depreciation
- [[currency_crisis_indicators]] — a currency crisis is the discontinuous, extreme realization of a risk premium spike
- [[Cortapasso 2023 - Padrões da Transmissão Cambial para a Taxa de Inflação no Brasil]] — Brazil's 2003–2012 BRL appreciation is described as interest-rate arbitrage enabled by falling country risk premium, the same carry-inflow-driven appreciation mechanism as this page's carry/risk-premium framework
- [[Paiva 2006 - External Adjustment and Equilibrium Exchange Rate in Brazil]] — RELDEBT (relative public debt/GDP) as a formal country-risk-premium proxy in a BEER model; documents the 2002–06 EMBI collapse (2,700bp→300bp) that is the historical mirror image of the fiscal-deterioration case in [[Itaú 2025 - Fiscal Dominance in Brazil]]
- [[BIS 2026 - Monetary Policy Transmission to Exchange Rates via Carry Trades]] — the carry-to-risk ratio (interest differential ÷ implied vol) is a risk-adjusted carry measure that flags when carry positioning is crowded and fragile to a policy shock
- [[carry_trade]] — the average carry premium is compensation for bearing the crash risk embedded in `ρ`; carry fails precisely when `ρ` spikes
- [[verde_fx_mental_models]] — sections 1.1–1.11 (fiscal credibility), 1.7 (BCB independence), 1.8 (fiscal dominance), 3.1 (carry overridden by risk premium), 4.8 (Stein's Law)
- [[kinea_fx_mental_models]] — cluster 1 entirely (fiscal credibility, fiscal dominance, electoral cycle as risk-premium drivers); 2.6 (BRL as a high-beta currency); 4.5 (the US "reacting like an EM")
- [[kapitalo_fx_mental_models]] — 6.1, 6.3, 6.8 (domestic fiscal/political risk as the BRL's thermometer; extreme technical positioning as a contrarian valuation signal)
- [[Goldman 2025 - GSDEER and GSFEER Models Primer]] — key omission from both models; blocks BRL GSDEER convergence
- [[Goldman 2023 - GSDEER A User's Manual]] — EM currencies with high risk premia show slower, noisier GSDEER convergence
- [[ppp_balassa_samuelson]] — GSDEER undervaluation is structural; risk premium is why it doesn't correct
- [[overshooting]] — risk-premium overshooting (fiscal shock) vs. monetary overshooting (Dornbusch) are distinct mechanisms with similar price pattern
- [[fiscal_dominance]] — the extreme manifestation of fiscal risk premium; when fiscal dominance materializes, ρ dominates r and effective carry inverts
- [[Itaú 2025 - Fiscal Dominance in Brazil]] — formalizes the fiscal deterioration → ↑ρ → BRL depreciation channel (Blanchard 2004); Brazil 2025 empirical assessment
