# Exchange Rate Pass-Through (ERPT)

**Type:** Empirical/theoretical mechanism — transmission channel
**Tags:** #pass-through #inflation #pricing-to-market #global-value-chains #depreciation #brl

---

## Definition

The degree to which a change in the nominal exchange rate is reflected in domestic prices. Formally, the percentage change in import (or domestic) prices per 1% change in the exchange rate. Pass-through = 1 means full transmission (a 10% depreciation raises import prices 10%); pass-through < 1 means incomplete transmission.

---

## Why pass-through is incomplete

| Mechanism | Effect |
|---|---|
| Pricing-to-market (import-competing firms protect market share) | Firms absorb part of the exchange rate move in their margins rather than passing it to price — historically ~half of a US dollar depreciation passes to import prices within a year |
| International market segmentation / imperfect competition | Same good priced differently across countries even with free trade (see [[ppp_balassa_samuelson]]'s law-of-one-price failures) |
| Global value chains — backward linkages | Depreciation raises the cost of imported inputs used in a country's own exports, muting the net export-price decline (Italy bicycle example: 50% imported content halves the effective pass-through to the export price) |
| Global value chains — forward linkages | Symmetric effect on the import side: a trading partner's depreciation can lower input costs embedded in what a country imports |
| High/volatile domestic inflation | Rapid pass-through to domestic prices erodes competitiveness gains before relative prices adjust — makes nominal depreciation a weak tool for changing the *real* exchange rate |

---

## Empirical estimates (Goldfajn & Werlang 2000, 71 countries, 1980–98)

Pass-through is not a fixed number — it rises sharply with the horizon measured, then flattens:

| Horizon | Pass-through coefficient |
|---|---|
| 1 month | 0.012 |
| 3 months | 0.170 |
| 6 months | 0.426 |
| 12 months | 0.732 (peak) |
| 18 months | ~0.70 |

A 10% depreciation raises inflation only ~1.2% within a month but ~7.3% over a year — most of the pass-through is *not* immediate, which is exactly why post-crisis inflation panic based on the first few months' data tends to be overstated.

**Key dampener — prior RER misalignment**: if the depreciation is correcting a pre-existing overvaluation (vs. an HP-filtered trend, not a PPP fair-value estimate) rather than moving the currency further from equilibrium, pass-through is much lower — a 10% prior overvaluation offsets an 11.8% inflation impact at the 12-month horizon, i.e., nearly one-for-one. This is the single most actionable finding: **a depreciation that corrects a known misalignment should not be expected to generate proportional inflation.**

**Cross-sectional pattern**: pass-through is highest in Latin America (12-month coefficient 0.69, rising to 1.24 at 18 months — explicit inflation-depreciation-spiral tendency) and lowest in Europe/Oceania; emerging markets show near-complete 12-month pass-through (0.91) vs. developed countries (0.61); non-OECD pass-through (0.75) is ~4× the OECD figure (0.19). But EM pass-through is also *more* sensitive to the misalignment dampener (−15.3% per 10pp overvaluation in EM vs. −7.9% in developed markets) — EM currencies pass through more on average, but a "warranted" EM depreciation is proportionally more forgiven than in developed markets.

See [[Goldfajn and Werlang 2000 - The Pass-through from Depreciation to Inflation]].

---

## Brazil-specific evidence (Belaisch 2003)

During the 1999–2002 floating/inflation-targeting period, Brazil's own pass-through was *below* the Latin American average, not above it — a notable exception to the "EM/LatAm has high pass-through" pattern:

| Horizon | Brazil consumer (IPCA) | LatAm average | Non-US G-7 |
|---|---|---|---|
| 12 months | 17% | 69% | 11% |

Brazil's pass-through was comparable in *magnitude* to developed markets, though faster in *speed* of transmission. The gap between wholesale/tradables pass-through (120% at 12 months — full and then some) and consumer pass-through (17%) shows most of a currency shock is absorbed via margin compression and distribution costs before reaching the CPI, not via a small elasticity throughout the chain. Brazil's own pass-through had also *fallen* sharply vs. earlier-period estimates (Schwartz and Rabanal 2001 found ~80% for 1995–2000, ~4-5x higher) — attributed to the credibility gain from inflation targeting, though not formally tested. See [[Belaisch 2003 - Exchange Rate Pass-Through in Brazil]].

---

## First-round vs. second-round pass-through

Distinguishing the two components matters for policy:
1. **First round**: mechanical rise in import prices from depreciation.
2. **Second round**: de-anchoring of inflation expectations — workers and firms respond to the first-round price rise by raising wage/price demands more broadly, making the effect on inflation permanent rather than one-off.

Central bank credibility (a well-anchored inflation-targeting regime) limits second-round pass-through — the IMF's Western Hemisphere Regional Economic Outlook (2016) found ERPT is smaller in inflation-targeting EM economies than in non-targeters. This is the theoretical link between monetary policy credibility and how costly currency depreciation is for inflation.

---

## Why it matters for Brazil / EM

Pass-through is the mechanism that ties BRL depreciation to `IPCA`, and is the reason BCB (and any EM central bank managing a floating currency) cares about currency weakness beyond its balance-of-payments implications. High or rising ERPT is a symptom of weak monetary credibility — it is the flip side of [[fiscal_dominance]]: when fiscal stress is driving depreciation (via the risk premium ρ), the same depreciation now also feeds inflation faster if the central bank's anchor is in doubt, compounding the original problem instead of just being a relative-price adjustment.

---

## Connections

- [[Krugman 2023 - Output and the Exchange Rate in the Short Run]] — canonical textbook definition (pass-through, pricing-to-market, backward/forward global-value-chain linkages)
- [[Krugman 2023 - Money, Interest Rates, and Exchange Rates]] — first-round vs. second-round pass-through distinction, in the EM inflation-targeting case study
- [[ppp_balassa_samuelson]] — incomplete pass-through is one of the mechanisms (alongside pricing-to-market and nontradables) behind the law-of-one-price/PPP failures documented there
- [[fiscal_dominance]] — under fiscal dominance, depreciation-driven pass-through compounds inflation instead of being absorbed as a one-off relative-price shift
- [[Goldfajn and Werlang 2000 - The Pass-through from Depreciation to Inflation]] — 71-country panel estimates by horizon, region, and development status; RER misalignment as the key dampener
- [[currency_crisis_indicators]] — this concept covers what happens to inflation *after* a crisis-driven depreciation; that one covers the pre-crisis warning signs
- [[Goldman 2026 - EM Food Inflation]] (obsidian/inflation vault) — dollar-invoicing/broad-USD channel as the dominant driver of a global food-inflation factor across 125 countries; pass-through operating through a specific traded CPI subcomponent rather than the aggregate basket
- [[kinea_fx_mental_models]] — 3.5: quantified transmission model, BRL commodity prices → inflation → BCB's room to cut, including a direct bps-of-IPCA estimate of a specific FX appreciation scenario
- [[kapitalo_fx_mental_models]] — 6.6: the 2024 fiscal-anchor credibility crisis and its pass-through to inflation, a practitioner-side case of pass-through rising precisely when credibility is in question
- [[Belaisch 2003 - Exchange Rate Pass-Through in Brazil]] — Brazil 1999–2002 VAR estimates by price basket (wholesale/tradables vs. consumer/nontradables); Brazil's pass-through was below the LatAm average and had fallen sharply from pre-inflation-targeting estimates
- [[Cortapasso 2023 - Padrões da Transmissão Cambial para a Taxa de Inflação no Brasil]] — extends Brazil's pass-through evidence to 2002–2021, arguing the coefficient is asymmetric between appreciation and depreciation regimes and that BCB's price control has become exacerbatedly dependent on currency appreciation specifically
