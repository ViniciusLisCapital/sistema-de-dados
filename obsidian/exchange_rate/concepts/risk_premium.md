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

## Connections

- [[uip]] — risk premium is the extension of UIP: `r = r* + E[Δe] + ρ`; it explains the forward premium puzzle
- [[carry_trade]] — the average carry premium is compensation for bearing the crash risk embedded in `ρ`; carry fails precisely when `ρ` spikes
- [[verde_fx_mental_models]] — sections 1.1–1.11 (fiscal credibility), 1.7 (BCB independence), 1.8 (fiscal dominance), 3.1 (carry overridden by risk premium), 4.8 (Stein's Law)
- [[Goldman 2025 - GSDEER and GSFEER Models Primer]] — key omission from both models; blocks BRL GSDEER convergence
- [[Goldman 2023 - GSDEER A User's Manual]] — EM currencies with high risk premia show slower, noisier GSDEER convergence
- [[ppp_balassa_samuelson]] — GSDEER undervaluation is structural; risk premium is why it doesn't correct
- [[overshooting]] — risk-premium overshooting (fiscal shock) vs. monetary overshooting (Dornbusch) are distinct mechanisms with similar price pattern
- [[fiscal_dominance]] — the extreme manifestation of fiscal risk premium; when fiscal dominance materializes, ρ dominates r and effective carry inverts
- [[Itaú 2025 - Fiscal Dominance in Brazil]] — formalizes the fiscal deterioration → ↑ρ → BRL depreciation channel (Blanchard 2004); Brazil 2025 empirical assessment
