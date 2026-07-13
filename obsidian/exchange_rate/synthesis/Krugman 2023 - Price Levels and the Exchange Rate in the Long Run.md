# Krugman 2023 — Price Levels and the Exchange Rate in the Long Run

**Type:** Textbook chapter (International Economics, 12th ed., Ch. 16)
**Tags:** #textbook #ppp #law-of-one-price #balassa-samuelson #real-exchange-rate #fisher-effect #monetary-approach
**Source:** Krugman, Obstfeld & Melitz, *International Economics: Theory and Policy*, 12th ed. (2023), Part Three
**Language:** English
**Raw file:** [[price_levels_exchange_rate_lr (Krugman, 2023)_raw]]

---

## Context and motivation

Completes the long-run half of the textbook's exchange rate model (Ch. 14 UIP + Ch. 15 money market) by supplying the theory of long-run price levels: purchasing power parity (PPP). The chapter's real payoff is showing PPP fails badly in the data, then building the more general "real exchange rate" framework that survives that failure — this generalized model is the anchor for market expectations used in every later short-run chapter (explicitly flagged as feeding into Ch. 17's short-run output/exchange-rate analysis).

## Core argument / thesis

Absolute PPP (`E = P_US/P_E`) and its corollary relative PPP (`ΔE = π_US − π_E`) follow from the law of one price applied to a general price basket, but empirically both fail badly — the real exchange rate is not constant. The chapter's resolution: generalize to `E = q · (P_US/P_E)`, where `q` (the real exchange rate) is itself determined by relative demand/supply in goods markets, not just relative money supplies. Monetary disturbances still move the *nominal* rate in line with PPP; real (output-market) disturbances move the nominal rate in ways PPP cannot predict.

## Key mechanisms / model

- **Law of one price → absolute PPP → relative PPP**: absolute PPP is the price-level analogue of the law of one price; relative PPP (`ΔE = π − π*`) is more useful empirically since it doesn't require identical reference baskets across countries.
- **Monetary approach** (combines PPP with Ch. 15's money-market equation): `E = Ms_US·L(R_E,Y_E) / [Ms_E·L(R_US,Y_US)]` — the exchange rate is fully pinned down by relative money supplies/demands. Yields three comparative statics: ↑Ms_US depreciates $ proportionally; ↑R_US *depreciates* $ (paradoxically, because higher R lowers real money demand → higher P_US); ↑Y_US appreciates $ (higher transactions demand → lower P_US).
- **Fisher effect**: combining PPP with UIP gives `R − R* = π^e − π*^e` — nominal rate differentials reflect expected inflation differentials, not real return differentials. Resolves the apparent Ch.14-vs-Ch.16 paradox (higher R depreciates the currency here, but appreciates it in Ch. 14) by noting *why* R rose matters: a sticky-price interest-rate rise (Ch. 15, tight money) signals disinflation → appreciation; a flexible-price interest-rate rise via the Fisher effect (higher expected inflation) → depreciation.
- **PPP's empirical failure**: absolute PPP fails (transport costs, trade barriers, nontradables, imperfect competition/pricing-to-market — VW Polo priced $4,000 apart in Ireland vs. Austria despite shared currency and free trade). Relative PPP fails too (JPY/USD vs. relative CPI ratio, 1980–2019, show decades-long divergences). Deviations are larger and more persistent under floating than fixed regimes (Mussa 1986).
- **Balassa-Samuelson effect**: richer countries have systematically higher price levels (Fig. 16-3, cross-country plot). Two competing explanations: (1) Balassa/Samuelson — higher tradables-sector productivity in rich countries → higher wages → spills into nontradables via labor mobility → higher nontradables prices → higher overall price level; (2) Bhagwati-Kravis-Lipsey — higher capital/labor ratios in rich countries raise the marginal product of labor (hence wages) directly, without needing a productivity *differential* concentrated in tradables.
- **Real exchange rate** `q = (E·P_E)/P_US`: the relative price of the foreign consumption basket in domestic terms. Long-run `q` is set by relative demand (RD, upward-sloping in q) and relative supply (RS, vertical at full-employment relative output) — a rise in relative demand for US output → real dollar appreciation; a rise in US relative output supply → real dollar depreciation.
- **Real interest parity**: combining nominal UIP with the real-exchange-rate decomposition gives `r_US^e − r_E^e = E[Δq]` — expected real interest rate differentials across countries equal the expected real exchange rate change, not zero. Real rates need not equalize across countries even in the long run if real exchange rate trends (e.g., ongoing Balassa-Samuelson-driven appreciation) are expected.

## Main results / findings

- PPP and the law of one price are poor short-run and even poor long-run empirical descriptions, but remain the right *organizing* framework once generalized to allow the real exchange rate to move.
- Nontradables (services, construction; ~75% of US GDP) are the primary wedge between the law of one price and observed price levels.
- The chapter explicitly separates "exchange rate movements consistent with PPP" (all monetary disturbances) from "exchange rate movements PPP cannot explain" (all real/output-market disturbances) — Table 16-1 is the full comparative-statics summary.

## Limitations and caveats

- The demand/supply real-exchange-rate model (Fig. 16-4) is a reduced-form diagram, not a microfounded general equilibrium model — useful for comparative statics, not for quantification.
- Balassa-Samuelson and Bhagwati-Kravis-Lipsey are presented as competing, not nested, explanations — the chapter does not adjudicate between them, only notes both predict the same qualitative cross-country pattern.
- The chapter's PPP empirics (Fig. 16-2, yen/dollar vs. relative CPI, 1980–2019) is descriptive, not a formal statistical test — treat as illustrative of the magnitude of PPP deviations, not as an estimate of a specific model.

## Connections

- [[ppp_balassa_samuelson]] — this chapter is the fullest textbook derivation of both PPP (absolute/relative, monetary approach) and the Balassa-Samuelson effect, including the competing Bhagwati-Kravis-Lipsey capital-endowment explanation not previously in this vault; also introduces the real exchange rate and real interest parity as PPP's generalization
- [[uip]] — Fisher effect and real interest parity are UIP's nominal condition split into inflation-expectations and real-exchange-rate-expectations components
- [[overshooting]] — this chapter's long-run real exchange rate model is explicitly the "anchor" Krugman uses for expectations in the short-run (overshooting) chapters
- [[Dornbusch 1976 - Expectations and Exchange Rate Dynamics]] — shares the same long-run PPP anchor (`ē = p̄ − p̄*`) that Dornbusch takes as given before deriving short-run overshooting around it
