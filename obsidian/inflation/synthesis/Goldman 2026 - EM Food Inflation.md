# Goldman 2026 — EM Food Inflation: Upside Pressures Globally, But Heterogeneous Local Exposure

**Type:** Sell-side research note (EM Macro Themes)
**Tags:** #food-inflation #emerging-markets #pca-factor-model #commodities #exchange-rate-pass-through
**Source:** Goldman Sachs, EM Macro Themes, 23 June 2026
**Language:** English
**Raw file:** [[em_food_inflation (goldamn, 2026)]]

---

## Context and motivation

Written amid a live upside-risk scenario: an Iran war driving oil, diesel, and fertilizer prices up 50–60% y/y, plus forecast El Niño conditions threatening 2026–27 harvests — asking which countries are actually exposed given that food supply chains are a mix of globally-traded and locally-sourced goods. The report's contribution is a clean statistical decomposition (not a commodity-basket model) that separates global, regional, and country-specific drivers of food inflation across 125 countries, then maps that decomposition onto forward-looking vulnerability.

## Core argument / thesis

Food inflation is structurally more important and more volatile in EM than DM (28% vs. 15% of the CPI basket) because of Engel's-law income effects, thinner/less diversified domestic supply chains, and greater currency-driven pass-through on internationally-sourced inputs. A PCA-based decomposition into global/regional/local factors shows this exposure is highly heterogeneous by region: Europe and North America are dominated by the global factor; Asia and Latin America split roughly evenly between regional and global; Africa is overwhelmingly local; the Middle East is idiosyncratic (subsidy/price-control driven). Given current soft-commodity, fertilizer, diesel, and USD dynamics, the model implies ~2pp of upward pressure on global food inflation in H2 2026, concentrated in countries with both high global-factor sensitivity and high food CPI weights (Ethiopia, Pakistan, Senegal, Malaysia, Ghana, Morocco flagged as most exposed).

## Key mechanisms / model

- **Structural EM/DM food-inflation gap**: three reinforcing channels — (1) Engel's law (poorer countries spend proportionally more on food, mechanically raising its CPI weight); (2) less diversified EM supply chains (more exposed to localized weather/disease shocks); (3) currency volatility (EM currencies more volatile vs. USD, and key inputs — fertilizer, diesel, grains — are USD-invoiced, so FX pass-through amplifies imported food costs). This third channel is the direct link to [[exchange_rate_pass_through]] — food inflation is one of the specific CPI subcomponents through which currency depreciation transmits to headline inflation, and the USD-invoicing structure means it's the *dollar's* strength broadly, not just any one country's bilateral rate, that matters.
- **PCA-based three-layer decomposition** (Box 1): sequential PCA — extract a single global factor from the full 125-country panel, regress each country on it, then run PCA on the *within-region residuals* to extract a regional factor, leaving a local residual. Advantages: agnostic (no pre-committed commodity basket or transmission channel), and the three layers are orthogonal by construction, giving a clean variance decomposition.
- **Global-factor regression** (Box 2): the extracted global factor is itself explained by four observables — FAO soft-commodities index, fertilizer (urea/DAP), diesel, and broad USD — each with its own lag (fertilizer ~3 quarters, since pre-bought a season or two ahead; soft commodities ~2 quarters; diesel with a longer lag and smaller contribution). **The dollar-invoicing/broad-USD channel is the single dominant contributor** to the global food factor — a stronger dollar mechanically raises local-currency import costs for food and fuel across the whole panel simultaneously, independent of any single country's bilateral exchange rate.
- **Regional heterogeneity** (Exhibit 7): Western Europe most globally synchronized (global factor explains >50% of variance, 81% of the regional aggregate) — deep supply-chain integration, common currency, low administered-price share. CEE and North America similar profile. Asia/Latin America: global and regional roughly equal, with local still most informative (weather + idiosyncratic factors). Africa: local factor dominates (domestic harvest cycles, sharp FX moves, conflict disruption, price administration break the link to global commodity prices). Middle East: mixed/idiosyncratic — heavy subsidy/price-control regimes (Saudi flour/bread, UAE strategic reserves, Israeli price controls) plus negligible intra-regional trade (virtually all staples sourced from Black Sea/EU/North America/Asia) leave only global and local as systematic drivers, no regional cycle.
- **El Niño findings** (distinct from the main global/regional/local framework): no clear *aggregate* EM food inflation effect historically (rainfall increases in some regions offset decreases elsewhere), but pronounced *localized* effects in Southern Africa and South/East Asia in the two most significant recent episodes (2015–16, 2023–24) — vulnerability concentrated in countries that are both geographically exposed to drier conditions and have consumption baskets weighted toward historically-disrupted soft commodities.

## Main results / findings

- Current elasticities (fertilizer, soft commodities, diesel, broad USD all moving unfavorably post-Iran-war) point to ~2pp of upward pressure on the *global* food inflation factor in H2 2026 — but the pass-through to any given country depends on that country's estimated global-factor loading and its food CPI weight, not on the global number alone.
- Highest-risk countries by the paper's own screen: Ethiopia, Pakistan, Senegal, Malaysia, Ghana, Morocco (high global-factor sensitivity × high food CPI weight).
- The 2022 shock is flagged as a methodological warning: realized food CPI inflation in that episode exceeded what the FAO soft-commodities index alone would have predicted, because it was simultaneously a fertilizer/energy-input shock (Russia's invasion disrupting European gas flows) — a reminder that single-commodity-index models can badly underpredict when multiple channels move together.

## Limitations and caveats

- Regional classification (7 blocs: Europe, CEE, Africa, Middle East, North America, South America, Asia) is acknowledged by the authors as a modeling simplification — meaningful sub-regional variation likely exists within Africa and Asia specifically that this classification cannot capture.
- El Niño analysis is explicitly flagged as outside the report's main scope — "two high-level points," not a rigorous model; the aggregate null result masks the paper's own finding of significant localized effects.
- PCA factors are latent/unitless by construction and require a secondary OLS projection step to be reinterpreted in inflation-percentage terms — the global/regional factors are statistical constructs, not directly observable "the" global food inflation rate.

## Connections

- [[exchange_rate_pass_through]] — the USD-invoicing/dollar-strength channel is the dominant driver of the report's global food-inflation factor, and currency volatility is one of the three structural reasons EM food inflation exceeds DM; this is exchange-rate pass-through operating through a specific, globally-traded CPI subcomponent rather than the aggregate basket
- [[Belaisch 2003 - Exchange Rate Pass-Through in Brazil]] — that paper's tradables/nontradables IPCA decomposition (Belaisch finds tradables/wholesale prices show much faster, larger FX pass-through than the aggregate CPI) is methodologically analogous to this report's global/regional/local decomposition, both isolating the internationally-traded component of a price basket to find where currency effects actually bite
