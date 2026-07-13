# Belaisch 2003 — Exchange Rate Pass-Through in Brazil

**Type:** Empirical paper (VAR analysis)
**Tags:** #pass-through #brazil #var #ipca #ipa #tradables #brl #inflation-targeting
**Source:** Agnès Belaisch, IMF Working Paper, 2003
**Language:** English
**Raw file:** [[depreciation_passtrought (Belaisch, 2003)]]

---

## Context and motivation

Written right after the 2001–02 BRL depreciation (real lost 80% of its value against USD over the period) and the second consecutive year BCB missed its inflation target — asking directly whether Brazil's exchange-rate pass-through had structurally risen after such a prolonged depreciation, since a Q4-2002 inflation pickup coincided with (in fact, lagged) the worst of the currency move. This is the Brazil-specific empirical companion to [[Goldfajn and Werlang 2000 - The Pass-through from Depreciation to Inflation]], directly citing and building on it.

## Core argument / thesis

Brazil's pass-through to consumer prices (IPCA) is low by both historical Brazilian and Latin American standards — comparable to G-7 countries in magnitude, though faster in timing. The bulk of a currency shock is absorbed further up the supply chain (wholesale/tradable prices), with margin compression, distribution costs, and consumer substitution toward domestic goods explaining why so little reaches the CPI. However, the paper flags — with some but inconclusive statistical support — that the pass-through may have started rising by late 2002 as the depreciation persisted and firms ran out of margin to compress.

## Key mechanisms / model

- **Price basket disaggregation is the paper's central methodological contribution**: rather than one aggregate pass-through number, it decomposes IPCA into free vs. administered prices, and free prices into tradables (40% of IPCA) vs. nontradables (33%), plus the wholesale price index (IPA, ~90% tradables) and the general price index (IGP-DI).
- **VAR methodology** (following McCarthy 1999): monthly data, July 1999–December 2002 (the inflation-targeting/floating-BRL period only), variables in log-differences (nonstationary in levels, no cointegration), ordered by Granger-causality exogeneity — oil price (supply shock proxy) and industrial production (demand proxy) and the exchange rate ordered before price variables.
- **Stylized facts before the VAR**: exchange rate volatility (HP-filtered) is ~3× wholesale price volatility and ~15× consumer price volatility; exchange rate fluctuations lead price fluctuations by 1–2 months generally, up to 5 months for tradables specifically — direct evidence prices are sensitive to the *trend* component of FX moves, not to noise.
- **Pass-through by horizon and basket** (cumulative, % of shock reflected in prices):

| Horizon | General (IGP-DI) | Wholesale (IPA) | Consumer (IPCA) | Free | Administered | Tradables | Nontradables |
|---|---|---|---|---|---|---|---|
| 1 month | 8 | 12 | 2 | 3 | 1 | 5 | 0 |
| 3 months | 27 | 34 | 6 | 7 | 3 | 12 | 4 |
| 12 months | 53 | 120 | 17 | 15 | 5 | 15 | 12 |
| Long term | 71 | 165 | 23 | 15 | 5 | 15 | 13 |

  Wholesale/tradables pass-through is fast and eventually *exceeds* 100% (i.e., overshoots the initial shock in level terms over time — consistent with ~90% tradables content); consumer-price pass-through is an order of magnitude smaller and essentially completes within two quarters.
- **International comparison**: Brazil's 12-month consumer-price pass-through (17%) is far below the Latin American average (69%, per [[Goldfajn and Werlang 2000 - The Pass-through from Depreciation to Inflation]]) and close to non-US G-7 economies (11% at 12 months, 19% long-term) — though Brazil's *speed* of adjustment is faster than G-7's.
- **Explanations for low pass-through** (literature review, Section III): (1) openness correlation (McCarthy 1999) — Brazil's trade/GDP (~30%) is low; (2) distribution costs dilute tradables' effective import content in the CPI (Burstein et al. 2001/2002); (3) local-currency price stickiness (Betts and Devereux 2000); (4) "flight from quality" — consumers substitute toward lower-quality domestic goods when imports get expensive (Burstein et al. 2002); (5) procyclicality — pass-through falls in recessions as firms compress margins rather than raise prices, directly citing Goldfajn and Werlang (2000)'s GDP-gap finding.
- **Evidence of a possible structural break (Q4 2002)**: Chow forecast test rejects "no structural break" at the F-statistic level (p=0.023) though less decisively by chi-square (p≈0.10); one-step-ahead recursive forecast tests also point to a pass-through increase around October–November 2002. The paper is explicit this is suggestive, not conclusive — "too early to make definitive statements."
- **Own pass-through fell over time**: comparing to earlier Brazil-specific studies — Schwartz and Rabanal (2001, sample 1995–2000) found ~80% 12-month consumer-price pass-through, roughly 4–5× this paper's 17% for 1999–2002. Kfoury (2001, structural Phillips-curve approach, 1998–2000) also found materially higher short-term pass-through than this paper. The decline is attributed to the shift to inflation targeting/floating BRL improving credibility (fewer episodes are read as permanent regime shifts) though this causal claim isn't formally tested here.

## Main results / findings

- Brazil-specific pass-through (17% at 12 months for IPCA, this paper's central estimate) is dramatically lower than the LatAm-wide average from [[Goldfajn and Werlang 2000 - The Pass-through from Depreciation to Inflation]] (69% at 12 months) — Brazil in 1999–2002 behaved more like a developed economy than like its regional peers on this metric, a notable divergence from the "EM/LatAm has high pass-through" cross-sectional pattern in that paper.
- Nontradables pass-through (12%, 12-month) is small but the *most persistent* — still adjusting at 12 months, consistent with a genuine second-round (not just first-round import-price) effect working through wages/costs rather than direct import content.

## Limitations and caveats

- Sample is short (July 1999–December 2002, ~42 monthly observations) — the paper is explicit this limits its ability to confirm the suspected late-2002 structural break; treat the "pass-through may be rising" conclusion as a flagged hypothesis, not an established finding.
- VAR ordering/identification (Cholesky-style recursive scheme) assumes oil prices, industrial production, and the exchange rate are contemporaneously exogenous to domestic prices — a standard but restrictive assumption; the paper notes robustness to reordering *within* each exogeneity group, not across groups.
- Findings are specific to the July 1999–December 2002 floating/inflation-targeting regime — explicitly not comparable to the earlier fixed/crawling-peg Real Plan period, where Schwartz and Rabanal's higher estimates apply.

## Connections

- [[Goldfajn and Werlang 2000 - The Pass-through from Depreciation to Inflation]] — direct empirical predecessor and comparison benchmark; this paper's central finding (Brazil's pass-through is *below* the LatAm average that source documents) is itself a striking result relative to that paper's regional pattern
- [[exchange_rate_pass_through]] — Brazil-specific numbers (by price basket: wholesale/tradables vs. consumer/nontradables) and the procyclicality/distribution-cost/local-currency-pricing/quality-substitution explanations
- [[Krugman 2023 - Output and the Exchange Rate in the Short Run]] — same pricing-to-market and incomplete-pass-through mechanisms (Betts-Devereux local-currency pricing ≈ Krugman's pricing-to-market), here estimated specifically for Brazil's 1999–2002 float
- [[currency_crisis_indicators]] / [[risk_premium]] — the 2001–02 BRL depreciation (80% loss vs. USD) sits in the same macro-stress episode later analyzed for fiscal-risk-premium dynamics in [[Itaú 2025 - Fiscal Dominance in Brazil]] and [[fiscal_dominance]]
