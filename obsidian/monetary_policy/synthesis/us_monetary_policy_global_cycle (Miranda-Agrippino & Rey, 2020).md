---
aliases: ["Miranda-Agrippino 2020 - US Monetary Policy and the Global Financial Cycle"]
---

# US Monetary Policy and the Global Financial Cycle — Silvia Miranda-Agrippino & Hélène Rey 2020

**Type:** paper
**Tags:** #global-financial-cycle #us-monetary-policy #spillovers #dynamic-factor-model #bayesian-var #external-instrument #risk-aversion #global-banks #leverage
**Source:** Working version "Revised March 28, 2020" (JEL E44, E52, F33, F42); the text names no journal. Previously circulated as "World Asset Markets and the Global Financial Cycle".
**Language:** English
**Source file:** [[monetary_policy/clean_md/us_monetary_policy_global_cycle (Miranda-Agrippino & Rey, 2020)]]

---

## Context and motivation

Financial globalization has reached historically unprecedented levels while the US remains the hegemon of the international monetary system. Little work had examined how financial globalization changes the transmission of US monetary policy abroad through financial intermediation and global asset prices, as opposed to trade. Building on Rey (2013)'s "Global Financial Cycle", the paper asks whether US monetary policy drives the cycle, using monthly data since 1980, and whether floating exchange rates protect other countries.

## Core argument / thesis

"US monetary policy shocks induce comovements in the international financial variables that characterize the 'Global Financial Cycle.'" A US tightening lowers a single global factor in risky asset prices, raises aggregate risk aversion, deleverages global banks, contracts domestic credit worldwide, cuts cross-border credit flows and tightens foreign financial conditions — and "Countries with floating exchange rate regimes are subject to similar financial spillovers." This "challenges the degree of monetary policy sovereignty of open economies" and echoes Rey (2013): while capital is free and macroprudential tools are not used, monetary conditions everywhere "are partly dictated by the monetary policy of the hegemon (the US)", though "this of course does not mean that exchange rate regimes do not matter".

## Key mechanisms / model

- **Global factor (2, Appendix B)**: a dynamic factor model in which each monthly (log) price is the sum of a global factor, a regional/market factor and an idiosyncratic term, estimated by maximum likelihood on first differences and cumulated (identified only up to scale and initial value). Panel: 858 risky asset prices (equities across North America, Latin America, Europe, Asia Pacific and Australia, corporate bond indices, non-precious commodities), 1990–2012; a narrower 303-series panel goes back to 1975. The factor co-moves negatively with the VIX, VSTOXX, VFTSE and VNKY.
- **Risk aversion proxy**: the factor is projected on global realized variance (from daily MSCI returns); the inverse of the residual is aggregate risk aversion (robust to also controlling for discount rates and growth forecasts of the US, Germany, UK and Japan, Appendix E). It declines continuously from 2003 to 2007 and jumps in the crisis.
- **Identification (3.1)**: rich-information Bayesian VARs (12 lags, monthly, 1980:1–2010:12, Minnesota-type priors with estimated tightness), with the US monetary shock identified by an external instrument: 30-minute surprises in the fourth federal funds futures contract (FF4) around FOMC announcements, summed by month, following Gürkaynak, Sack and Swanson (2005) and Gertler and Karadi (2015); no timing restrictions are needed. The large information set is meant to absorb the Fed information effect that can contaminate high-frequency surprises. The policy variable is the 1-year Treasury rate and the shock raises it by 1% on impact.
- **VARs (Table 2)**: (1) a 13-variable closed-economy VAR; (2)–(3) global VARs adding the global factor, risk aversion, global real activity ex US, global domestic credit, cross-border inflows (to banks and non-banks), the GZ credit spread and the leverage of US broker-dealers, EU global banks, US banks and EU banks; (4)–(5) the same with aggregates for "independently floating" countries only (IMF de facto classification); (6) a version with UK and euro area financial conditions and policy rates.
- **Interpretation (4.1)**: a two-investor asset-pricing model (building on Zigrand et al.) with risk-neutral global banks that fund in dollars under a Value-at-Risk constraint and risk-averse mean-variance asset managers. Expected excess returns have a global component equal to aggregate variance times aggregate effective risk aversion Γ, a wealth-weighted average of the two investor types' risk aversions (Proposition 1). When leveraged global banks grow relative to asset managers, effective risk aversion falls and asset prices rise; a bank's expected return rises with its beta on the world portfolio (Proposition 2).

## Main results / findings

- **Global factor**: one global factor is supported by information criteria and the Onatski test; it explains over 20% of the variance of the 858-series panel (Table B.2: 0.215 for the first eigenvalue) and about 60% for the 1975–2010 panel (0.662). It tracks NBER recessions and global events (Russian default, LTCM, the Asian crisis, the dot-com bust, the rise from 2003 to mid-2007 and the plunge after).
- **Instrument relevance (Table 1)**: FF4 first-stage F statistics are 17.930 (domestic VAR), 14.788 and 14.901 (global VARs); the extended Romer-Romer narrative instrument falls from 10.947 to 2.278 and 2.756 in the global VARs, and yields a pronounced price puzzle domestically.
- **Domestic transmission (Figure 5)**: a US tightening lowers production, capacity utilization and housing starts, raises unemployment, lowers prices (no puzzle with FF4), narrows the term spread, raises the Gilchrist-Zakrajšek excess bond premium and mortgage spreads, drops stock and house prices, and appreciates the dollar.
- **Global asset markets (Figure 6)**: the global factor falls abruptly; assuming equal loadings, the 40% impact fall "would roughly translate into a 8% impact decrease in the local stock market". Aggregate risk aversion rises "by over 50% above its average trend"; the result holds across alternative risk-aversion measures (Figure E.3).
- **Credit and flows (Figure 7)**: global domestic credit falls (not driven by US credit) and cross-border inflows retrench, to banks and non-banks alike, by "several percentage points"; global real activity ex US is unchanged on impact and, in Appendix E.1, not significantly affected, while global IP measures fall mainly through the US slowdown.
- **Leverage (Figure 8)**: leverage of US broker-dealers and European global banks contracts by several percentage points; the broader banking sector responds later and less precisely. Bank-level data (4.2) show leverage growth moving with balance-sheet growth beyond the US, especially for capital-market-oriented banks and G-SIBs; G-SIBs had higher pre-crisis betas on the global factor and higher returns, and the highest-beta banks lost most after August 2007 (Figure 11).
- **Floaters (Figure 9)**: for independently floating countries the contraction in credit and inflows is "very similar" in magnitude — a floating regime "is not successful in providing a protective shield against US monetary policy shocks".
- **UK and euro area (Figure 10)**: stock markets fall, the dollar appreciates (reverting within one to three quarters), corporate spreads rise on impact, and policy rates ease endogenously by about 30bps — so the tightening of their financial conditions is a US spillover, not a domestic tightening.

## Limitations and caveats

- **Figures are not in the file**: Figures 1–11 and D.1–E.3 survive only as axis ticks and panel titles (Figure 11's bank labels are scrambled); impulse-response magnitudes are known only where the text states them (the 40% factor fall, over 50% risk aversion, about 30bps easing, "several percentage points").
- **Garbled notation**: model equations in 4.1 and Appendices B–C print with "(cid:…)" glyphs and split subscripts; described in words here, not restored.
- **Truncations and inconsistencies as printed**: footnote 21 gives the sample as "1980-201"; footnote 31's list of floating countries breaks off mid-word, with a stray URL fragment; bank-sample counts differ across places (footnote 40: 166 institutions in 20 countries, 21 G-SIBs; Table A.3: 155 banks and 25 G-SIBs; Figure 11: 162 and 20).
- The authors note the VAR sample is limited in time for the wider factor panel, that quarterly credit, flow and leverage data are interpolated to monthly, that US policy is "only one" possible driver, and that open-economy models matching these regularities remain to be built.

## Connections

- [[global_financial_cycle]] — the paper establishes US monetary policy as a driver of the cycle: one global factor in 858 risky asset prices, which falls, with risk aversion rising, credit and cross-border flows retrenching and global banks deleveraging after a US tightening
- [[currency_regimes]] — independently floating countries suffer credit and flow contractions of similar size, so floating does not shield them; supports the trilemma-to-"dilemma" claim while granting that regimes matter
- [[monetary_policy/synthesis/dilemma_not_trilemma (Rey, 2013)]] — formalizes Rey's global factor (the same 858-series panel) and replaces her recursive VAR with high-frequency external-instrument identification
- [[monetary_policy/synthesis/us_policy_international_risk_spillovers (Kalemli-Ozcan, 2019)]] — same risk-aversion channel of US policy; Kalemli-Özcan finds free floats much better insulated than managed floats, whereas this paper finds floaters equally exposed in credit and flows
- [[monetary_policy/synthesis/trilemma_tradeoffs (Obstfeld, 2015)]] — cited as rightly stressing that exchange rate regimes still matter
- [[monetary_policy/synthesis/information_effect_hf_identification (Nakamura & Steinsson, 2018)]] — the Fed information effect that can bias high-frequency surprises; this paper addresses it with a rich-information VAR
- [[verde_fx_mental_models]] — sections 5.4–5.5: global risk appetite and the BRL as "passenger" of global conditions
