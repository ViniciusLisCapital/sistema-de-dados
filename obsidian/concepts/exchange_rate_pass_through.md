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

Pass-through is not a fixed number: it rises with the horizon measured and then stops rising. In the baseline panel (Table 2) the coefficient on accumulated depreciation goes from 0.0124 at one month to 0.1704 at three, 0.426 at six and 0.732 at twelve; in the total column of Table 3 the eighteen-month figure (0.701) is no higher than the twelve-month one, and the authors read it as "the pass-through coefficient reaches a limit after 12 months, and its magnitude is smaller than 1". Their own reading of the short end: "a 10% depreciation will only cause a 1.24% inflation in the following month". Most of the effect is therefore not immediate, and an inflation reading taken in the first months after a depreciation shows only a small part of it.

**Key dampener — prior RER misalignment**: misalignment is the deviation of the real exchange rate from a Hodrick-Prescott trend, not from a PPP fair value. A depreciation that corrects a prior overvaluation is a relative-price adjustment rather than a price-level shock: "in 12 months, a 10% of overvaluation decreases inflation by 11.8%" (Table 2), so "a nominal devaluation that does not overshoot its required adjustment would not have severe consequences in terms of inflation". This is the most actionable finding: **a depreciation that corrects a known misalignment should not be expected to generate proportional inflation.**

**Cross-sectional pattern** (12-month coefficients): by region (Table 3), America 0.692 and Asia 0.712 against Europe 0.360 and Oceania 0.158; by development (Table 4), emerging markets "almost complete (0.912)" against 0.605 for developed countries; by OECD membership (Table 4), 0.754 for non-members against 0.188 for members. The authors attribute America's high pass-through to "the spiral inflation-depreciation in several Latin American countries". The misalignment dampener is also stronger where pass-through is higher: "a 10% overvaluation reduces inflation by 15.34% versus 7.9% in developed economies". EM currencies pass through more on average, but a "warranted" EM depreciation is more forgiven.

Damaged or inconsistent in the source: the text calls America's coefficient "the highest (1.24 in 12 months)", while Table 3 prints 1,240 in the 18-month row and 0,692 in the 12-month row; the twelve-month table figure is the one used above. The extracted text also stops inside Section IV, so the forecast and robustness sections are not available.

See [[inflation/synthesis/depreciation_pass_through (Goldfajn, 2000)]].

---

## Brazil-specific evidence (Belaisch 2003)

During the 1999–2002 floating/inflation-targeting period, Brazil's own pass-through was *below* the Latin American average, not above it — a notable exception to the "EM/LatAm has high pass-through" pattern:

| Horizon | Brazil consumer (IPCA) | LatAm average | Non-US G-7 |
|---|---|---|---|
| 12 months | 17% | 69% | 11% |

Brazil's pass-through was comparable in *magnitude* to developed markets, though faster in *speed* of transmission. The gap between wholesale/tradables pass-through (120% at 12 months — full and then some) and consumer pass-through (17%) shows most of a currency shock is absorbed via margin compression and distribution costs before reaching the CPI, not via a small elasticity throughout the chain. Brazil's own pass-through had also *fallen* sharply vs. earlier-period estimates (Schwartz and Rabanal 2001 found "almost 80 percent" for 1995-2000, "about four times more than in the recent sample") — attributed to the credibility gain from inflation targeting, though not formally tested. See [[inflation/synthesis/depreciation_pass_through (Belaisch, 2003)]].

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

## How it appears across sources

| Source | Role |
|---|---|
| [[exchange_rate/synthesis/output_exchange_rates_sr (Krugman, 2023)]] | Textbook definition: pass-through, pricing-to-market, backward and forward global-value-chain linkages |
| [[exchange_rate/synthesis/money_interest_rate_exchange_rates (Krugman, 2023)]] | First-round vs. second-round pass-through, in the EM inflation-targeting case study |
| [[inflation/synthesis/depreciation_pass_through (Goldfajn, 2000)]] | 71-country panel: pass-through by horizon, region and development status; prior RER misalignment as the main dampener |
| [[inflation/synthesis/depreciation_pass_through (Belaisch, 2003)]] | Brazil 1999–2002 VAR: consumer pass-through low by international standards, wholesale close to complete; lower than earlier-period Brazilian estimates |
| [[inflation/synthesis/padrao_transmissao_cambial (Cortapasso, 2023)]] | Brazil 2002–2021: pass-through asymmetric between appreciation and depreciation regimes |
| [[monetary_policy/synthesis/implementing_it_brazil (Bogdanski, Tombini & Werlang, 2000)]] | The BCB's linear and non-linear pass-through specifications; in the short sample the non-linear ones were close to the linear |
| [[monetary_policy/synthesis/it_lessons_and_challenges (Minella et al., 2002)]] | Brazil 1994–2002: higher pass-through to administered than to market prices; the size of the 2001–2002 depreciation, not the coefficient, drove inflation |
| [[monetary_policy/synthesis/it_credibility_fx_volatility (Minella et al., 2003)]] | Brazil: administered-price pass-through above market-price pass-through; recursive estimates fall after the 1999 float |
| [[inflation/synthesis/administered_prices_projection_pass_through (Alves et al., 2013)]] | BCB revision of administered-price pass-through coefficients, which fall to about zero as Petrobras smoothed prices and contracts changed indexers |
| [[inflation/synthesis/targets_inflation_dynamics (Alves & Areosa, 2005)]] | Short-run pass-through inside a target-indexed open-economy Phillips curve for Brazil; a credible target removes current exchange-rate changes from expected inflation |
| [[inflation/synthesis/em_food_inflation (Goldman, 2026)]] | Pass-through through a traded CPI subcomponent: dollar invoicing as a driver of a global food-inflation factor |
| [[expectations/synthesis/brazil_taming_inflation_expectations (Bevilaqua, Mesquita & Minella, 2007)]] | Exchange-rate changes in Brazilian survey expectations, falling in recent windows; depreciation reaches expectations through IGP-indexed managed prices |
| [[expectations/synthesis/market_forecasts_brazil_performance (Carvalho & Minella, 2012)]] | Brazilian survey inflation forecast errors move with exchange-rate forecast errors; the exchange-rate coefficient in 12-month expectations falls over time |

---

## Connections

- [[exchange_rate/synthesis/output_exchange_rates_sr (Krugman, 2023)]] — canonical textbook definition (pass-through, pricing-to-market, backward/forward global-value-chain linkages)
- [[exchange_rate/synthesis/money_interest_rate_exchange_rates (Krugman, 2023)]] — first-round vs. second-round pass-through distinction, in the EM inflation-targeting case study
- [[ppp_balassa_samuelson]] — incomplete pass-through is one of the mechanisms (alongside pricing-to-market and nontradables) behind the law-of-one-price/PPP failures documented there
- [[fiscal_dominance]] — under fiscal dominance, depreciation-driven pass-through compounds inflation instead of being absorbed as a one-off relative-price shift
- [[inflation/synthesis/depreciation_pass_through (Goldfajn, 2000)]] — 71-country panel estimates by horizon, region, and development status; RER misalignment as the key dampener
- [[currency_crisis_indicators]] — this concept covers what happens to inflation *after* a crisis-driven depreciation; that one covers the pre-crisis warning signs
- [[inflation/synthesis/em_food_inflation (Goldman, 2026)]] (obsidian/inflation vault) — dollar-invoicing/broad-USD channel as the dominant driver of a global food-inflation factor across 125 countries; pass-through operating through a specific traded CPI subcomponent rather than the aggregate basket
- [[kinea_fx_mental_models]] — 3.5: quantified transmission model, BRL commodity prices → inflation → BCB's room to cut, including a direct bps-of-IPCA estimate of a specific FX appreciation scenario
- [[kapitalo_fx_mental_models]] — 6.6: the 2024 fiscal-anchor credibility crisis and its pass-through to inflation, a practitioner-side case of pass-through rising precisely when credibility is in question
- [[inflation/synthesis/depreciation_pass_through (Belaisch, 2003)]] — Brazil 1999–2002 VAR estimates by price basket (wholesale/tradables vs. consumer/nontradables); Brazil's pass-through was below the LatAm average and had fallen sharply from pre-inflation-targeting estimates
- [[inflation/synthesis/padrao_transmissao_cambial (Cortapasso, 2023)]] — extends Brazil's pass-through evidence to 2002–2021, arguing the coefficient is asymmetric between appreciation and depreciation regimes and that BCB's price control has become exacerbatedly dependent on currency appreciation specifically
- [[monetary_policy/synthesis/implementing_it_brazil (Bogdanski, Tombini & Werlang, 2000)]] — the BCB's four pass-through specifications (constant, quadratic in the change, level-dependent, quadratic in the level); in the short quarterly sample the non-linear ones were close to the linear
- [[monetary_policy/synthesis/it_lessons_and_challenges (Minella et al., 2002)]] — Brazil 1994–2002: low consumer pass-through but more than twice as high for administered as for market prices (Table 7); the size of the 2001–2002 depreciation, not the coefficient, drove the inflation; a supply-curve estimate attributes the lower pass-through under inflation targeting to lower inflation persistence
- [[monetary_policy/synthesis/it_credibility_fx_volatility (Minella et al., 2003)]] — Brazil through 2002: administered-price pass-through about twice market-price pass-through (Table 7), rising when the crisis months are added; recursive estimates show a fall in pass-through after the January 1999 float
- [[inflation/synthesis/administered_prices_projection_pass_through (Alves et al., 2013)]] — BCB revision of administered-price pass-through coefficients: gasoline and LPG fall to about zero in 2006-2011 (Tables 10, 12) as Petrobras smoothed prices and contracts changed indexers; all four coefficients set to zero
- [[inflation/synthesis/targets_inflation_dynamics (Alves & Areosa, 2005)]] — Brazil 1996Q1–2004Q4: short-run pass-through to consumer inflation estimated at 0.053 in a target-indexed open-economy NKPC (Table 1); a credible target removes current exchange-rate changes from expected inflation
- [[expectations/synthesis/brazil_taming_inflation_expectations (Bevilaqua, Mesquita & Minella, 2007)]] — Brazil 2000:1–2006:8: the six-month exchange-rate change enters 12-month-ahead survey expectations with 0.06 (Table 1), falling in recent rolling windows; depreciation feeds expectations through managed prices indexed to the IGP-DI
- [[expectations/synthesis/market_forecasts_brazil_performance (Carvalho & Minella, 2012)]] — Brazil 2002–2007: inflation and exchange-rate forecast errors correlate at 0.90 (Figure 4.1), survey forecasts inefficient in exchange-rate information before 2004 (Table 3.3), and a falling exchange-rate coefficient in 12-month survey expectations (Figure 7.1)
