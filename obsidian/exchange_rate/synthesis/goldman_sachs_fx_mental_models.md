# FX Mental Models — Goldman Sachs "Global FX Trader" (Jan 2025– )

## About this document

**Status: partial construction, in progress.** This document covers the first 25 of 80 weekly issues of Goldman Sachs' "Global FX Trader" series (`repository/mental_model/goldman_sachs/`), from 3 January 2025 ("Tariff Special") through 20 June 2025 ("Seven-Double-Oh, Look Out Below") — a span that runs from the Trump inauguration through the April 2025 "Liberation Day" reciprocal-tariff shock, its immediate aftermath, and the first two months of the resulting bearish-Dollar regime. It mirrors the format of the three existing manager documents in this folder (`kapitalo_fx_mental_models.md`, `verde_fx_mental_models.md`, `kinea_fx_mental_models.md`), but the source is different in kind, which changes what the document captures. The first 15 issues were processed as a pilot; the user approved its 9-cluster structure as-is before the next batch (issues 16-25, 17 Apr – 20 Jun 2025) was folded in.

**How GS differs from the asset-manager letters:**
- These are **sell-side strategy notes**, not a fund's own investor letters. Every issue carries live, numbered **trade recommendations** — explicit currency pairs with targets and stops that get opened, tightened, extended, and eventually closed for a stated realized return within the sample (e.g., short EUR/BRL opened mid-December 2024, tightened twice, closed in late February 2025 for "~6-7%"). Where a full lifecycle is visible, it is documented as such.
- GS runs a **standing quantitative toolkit** reused verbatim week to week — GSDEER (structural/PPP-style fair value), GSFEER (current-account/BOP-consistent fair value), and GSBEER-style cyclical regressions (fitted value from rate differentials, equities, credit spreads, commodities) — layered under the narrative reasoning. Two of GS's own methodology papers on GSDEER/GSFEER are already synthesized separately in this folder ("Goldman 2023 - GSDEER A User's Manual.md", "Goldman 2025 - GSDEER and GSFEER Models Primer.md"); **this document is about the tactical, week-to-week application of that toolkit (and the narrative frameworks layered on top of it), not the models' methodology**, which those two files already cover.
- The source language is English; per project convention, this document is **not translated**.

**Redistribution note:** these PDFs carry a Goldman Sachs research-distribution license whose terms restrict downstream use, including as AI input. This document was produced with the user's explicit go-ahead after that restriction was flagged; anyone reusing this file outside this project should be aware the underlying source PDFs are not freely redistributable.

The frameworks below are consolidated by theme, not by issue — where the same mechanism recurs (which is the norm; a handful of core frameworks like the CNY-fix-anchor argument or the rate-differential fitted-value model appear almost every week under different currencies), instances are unified into one entry with the evolution documented across dated examples. Cluster names and boundaries are provisional and will likely be revised as the remaining ~55 issues (June 2025 – July 2026) are processed.

---

# 1. Goldman Sachs' Standing Analytical Toolkit

Unlike the manager letters, nearly every GS currency call is run through one or more named, reusable quantitative instruments before (or instead of) a purely narrative argument. This cluster documents the toolkit itself, since it recurs underneath almost every other cluster below.

## 1.1 Rate-Differential / GSBEER Fitted-Value Decomposition ("is this move justified?")

**What it is:** GS's default diagnostic for any FX move: regress the currency's historical return on a small set of cyclical variables (typically some combination of rate differentials, equities, credit spreads, commodity prices, sovereign spreads) estimated over a long lookback, then compare the "fitted" value the model implies to the actual move. Agreement between actual and fitted is read as "the move is fundamentally justified"; a gap ("residual") is treated as a distinct, nameable driver (a narrative, a flow, a risk premium) that has to be independently identified, not just labeled "noise."

**Key variables:** Weighted-average rate differential (2y/5y/10y, nominal or real); equity indices (S&P 500, MSCI China); credit spreads; commodity prices (Brent, copper); sovereign spreads; estimation window (commonly since 2010 for European crosses, since 2000 for JPY regime studies).

**How Goldman Sachs applied it:**
- **31 Jan 2025 ("Tariff-fied"):** used to argue Dollar strength was mostly justified by rate differentials with "limited tariff premium... at this point," implying "the larger Dollar moves are likely to come to the upside if the tariffs are actually put in place."
- **7 Mar 2025 ("Schwarze Null No More"):** applied to the post-German-fiscal-announcement EUR rally — checked against 1-year growth-expectation beta, Bund-yield beta, and the broader GSBEER regression; found the simple betas alone couldn't explain the +4.6% weekly move, but the richer GSBEER regression said the move was "well-justified": "when we consider the signal from a broader set of cyclical assets using our refreshed GSBEER models, then the Euro strength looks well-justified."
- **14 Mar 2025 ("Less Bang for the Buck"):** used to flag SEK's rally as overdone — actual performance sat well above what the GSBEER fit implied, with the gap explained instead by a directly observed variable (Swedish vs. North American equity-fund flows), not left as an unexplained residual.
- **21 Mar 2025 ("Rhetoric vs Returns"):** formalized further for EUR/GBP — a four-factor GSBEER fit (US equities, EU sovereign spreads, credit spreads, nominal 2y differential) showed March's EUR/GBP rally had "outperformed its historic beta," a stronger and more specific claim than a simple one-variable beta check.
- **17 Apr 2025 ("The ResEURrection"):** the model's *limits* stated explicitly for the first time — "the Euro 'outperformed' its typical relationship captured in our GSBEER models by about 20pp... the recent rise in the Euro has clearly outstripped moves in rate differentials or relative equity prices," used to motivate a shift toward historical-analogue reasoning (1.3) rather than the fitted-value check itself for this particular move.
- **25 Apr 2025 ("Art of the Repeal"):** an explicit methodological scoping note on when GSBEER is/isn't useful — "while large directional flows across regions may limit the usefulness of the model signals for pairs like EUR/USD, we think these signals can still be more helpful when applied to more 'relative value' type crosses within regions," demonstrated on NOK/SEK (constant, nominal 2y differential, US 10y yields, credit spreads, crude prices) which had "seen sharp underperformance in early April vs rate differentials and other cyclical assets."
- **20 Jun 2025 ("Seven-Double-Oh, Look Out Below"):** two further applications same issue — EUR/GBP flagged as having "overshot our GSBEER model implied estimates slightly over the past few weeks, which could pose a tactical headwind for another leg higher"; NOK/SEK's rally attributed to "shifting rate differentials and a sharp increase in oil prices" via the same regression.

## 1.2 GSDEER and GSFEER as the Structural Valuation Backbone

**What it is:** Two complementary "fair value" estimates appear in a standing table (Return Forecasts & Valuations) at the back of every issue: GSDEER (an augmented PPP model — CPI, terms of trade, productivity differentials) and GSFEER (a current-account/BOP-consistent fair value). Both produce bilateral and trade-weighted misalignment percentages. Critically, GS's week-to-week tactical calls and this structural table frequently point in *different* directions without being reconciled in the prose — e.g. a tactically bullish JPY call sitting alongside a GSDEER estimate showing JPY ~25-41% undervalued (i.e., structurally cheap USD/JPY should fall further than even the bullish tactical call implies). The table functions as a standing cross-check investors can consult, not as the source of the week's directional call.

**Key variables:** Spot, GSDEER estimate + bilateral/trade-weighted misalignment %, GSFEER estimate + bilateral/trade-weighted misalignment %, PPP estimate, 12-month total return decomposition (spot + carry).

**How Goldman Sachs applied it:**
- **17 Jan 2025 ("Day One Deliberations"):** the one clear case in the pilot window where GSDEER drove the actual forecast, not just a background table — for ARS, GS explicitly overrode forward-curve pricing (which assumed a slow, linear crawl) with its own GSDEER-implied 12-month misalignment correction, because the crawl pace was running below inflation: "unlike forward pricing which is consistent with a slow depreciation of the currency until year-end, we incorporate a ~20% weakening of the currency in line with our GSDEER predictions."
- **14 Mar 2025 ("Less Bang for the Buck"):** used to separate two different questions about EUR — cheap vs. the Dollar bilaterally, but "roughly fair (or even slightly overvalued)" on a trade-weighted basis — concluding "the case for substantial appreciation therefore has to rest on the Dollar leg, which is a key reason why this is not our central case," a good example of the trade-weighted/bilateral split changing where the analytical burden of proof sits.
- **31 Jan 2025 / 7 Feb 2025:** BRL and MXN both show large GSDEER undervaluation (~-29% to -30% bilateral) even while the week's tactical call is a carry-driven short EUR/BRL or a range-bound MXN carry trade — illustrating that the structural table is consulted, but doesn't override the tactical carry/positioning framework running in parallel.
- **2 May 2025 ("Waiting on the World to Change"):** the clearest joint methodology statement in the sample, in a dedicated "How overvalued is the Dollar?" section reconciling both models: "GSDEER and GSFEER... approach the question from separate angles but currently provide similar signals: the Dollar is around 16% overvalued on a trade-weighted basis." GSFEER's definition given verbatim for the first time: "The FEER model links the currency to an economy's external and internal imbalances... a 17% Dollar depreciation would be consistent with the US current account deficit (currently over 4%) converging to its long-run 'norm' (around 2.6% on our estimates)."
- **17 Apr 2025 ("The ResEURrection"):** GSDEER re-applied to ARS post-devaluation to re-anchor fair value rather than assess a fresh move — "the overvaluation signal of our GSDEER model has been significantly reduced by the 6% weakening... we think the 12-month ahead GSDEER fair value of ~1,500... provides a useful indication of where the currency would need to go to maintain its competitiveness" (cf. the pilot's 17 Jan 2025 ARS entry, where GSDEER first overrode forward-curve pricing for the same currency).
- **25 Apr 2025 / 16 May 2025:** two further bilateral-misalignment flags — EUR/NOK "significantly above fair value and close to the top of its historical range" (25 Apr); Sterling "+22% overvaluation... on our GSDEER model" cited as a headwind to an otherwise constructive tactical GBP view (16 May) — another instance of the table pulling against, not confirming, the week's tactical lean.

## 1.3 Historical-Analogue Testing as a Falsifiable Method

**What it is:** GS repeatedly invokes historical episodes (2017 vs. 2018 tariff sequencing, the 2016 Mexican-election selloff, the 1985 Plaza Accord and 1971 Smithsonian Agreement, 2022 UK gilts, the 2020 and 2014 GPIF strategic-review cycles) — but distinctively, treats each analogy as a hypothesis to be checked against current data, not just a rhetorical flourish. Several entries below show GS explicitly running the falsification test and reporting when the current data does *not* yet confirm the historical pattern.

**Key variables:** Varies by analogy; the common thread is a named precedent plus an explicit "necessary condition" the analogy requires to hold.

**How Goldman Sachs applied it:**
- **21 Feb 2025 ("First Term Flashbacks"):** the 2017-vs-2018 template used to weight probability across the Dollar's own scenario distribution: "our baseline forecasts are more aligned with the 2018 parallels than 2017. But we continue to monitor the important downside risk... that the balance of US policy changes and the foreign response is different than we expect."
- **21 Feb 2025:** the GPIF repatriation story checked against 2020's weekly flow data — finding no confirming signal: "Last time around, there were signs of increased foreign bond buying even leading up to the announcement in March... However, the weekly data lack any clear sign of significant foreign bond repatriation so far" — an explicit "not yet confirmed" call rather than assuming the analogy already applies.
- **28 Feb 2025 ("Accord and Discord"):** the Plaza/Smithsonian "Mar-a-Lago Accord" narrative directly falsified against the necessary condition for historical FX pacts to work (official intervention succeeding only when private capital already pushes the same direction): "for FX intervention to be successful, it helps for market forces to be pushing in the same direction... That was the case before both of those seminal currency pacts; it is not the case now."
- **21 Mar 2025 ("Rhetoric vs Returns"):** the 2017 EUR flow-reversal analogy (first raised 14 Mar) stress-tested against a specific discriminating variable — the US-EA growth gap — and found only partially applicable: in 2017 "Euro area growth matched that of the US" by year-end; in the 2025 setup "we still expect US growth of more than double the Euro area this year," tempering (not abandoning) the analogy.
- **17 Apr 2025 / 2 May 2025:** the same 2017 EUR-rotation analogy re-invoked as reinforcement for the by-then-live bearish-Dollar thesis ("this is also consistent with what happened in 2017... There are also other episodes, like 2002-2004, when a significant shift in global return prospects also coincided with outsized Dollar moves"), then used a second way — bounding the *speed* of a valuation-gap close, not just its direction — via two fresh analogues: "GBP during Brexit and... EUR during the gas supply shock... it is not unusual for currencies to overshoot once fair value is reached."
- **23 May 2025 ("The Bond and the Beautiful"):** the pilot window's most rigorous instance — GS formalizes the analogue-testing method into an explicit regression: define "US fiscal episodes" as weeks with ≥15bp 5s30s steepening (2010–present sample), then regress FX moves in those weeks on average 10y yield level and beta to the S&P 500, reporting R² (0.28 and 0.55 historically; 0.01 and 0.56 for the live week). Conclusion drawn from the fit, not narrative: "weeks with a similar extent of 5s30s steepening... tend to see clearer underperformance in higher-yielding versus lower-yielding currencies, rather than purely just in high versus low beta currencies." The same issue applies a historical analogue to RON (the 2008-09 EU-IMF programme, "EUR/RON moved around 20% higher" as the current account deficit shrunk) as a discrete country precedent.
- **13-20 Jun 2025 ("And So It Flows" / "Seven-Double-Oh, Look Out Below"):** a CHF/gold historical-analogue table spanning the Gulf War, Second Intifada, 9/11, the Iraq invasion, Russia/Ukraine, and Israel-Gaza, comparing 2-week S&P500/gold/CHF/JPY returns across each episode — "looking across a number of relatively recent instances of conflict, we find that the Franc typically outperforms alongside gold" — plus a COP-specific analogue to the early-2022 Russia/Ukraine oil shock.

## 1.4 Options-Implied Probability vs. House-View Probability Gap

**What it is:** GS backs out the probability the options/forward market implicitly assigns to a discrete event (a tariff being imposed at a given size) from spot/forward pricing relative to a fundamental fair-value benchmark, then compares that implied probability to its own economists' subjective probability. A judged gap between the two becomes the basis for a hedge recommendation, independent of GS's own directional conviction on the event itself.

**Key variables:** Implied probability (back-solved from spot/forward gap to fair value or from options skew), house economists' probability estimate, historical episode used to benchmark magnitude.

**How Goldman Sachs applied it:**
- **3 Jan 2025 ("Tariff Special"):** "Our latest estimates of the tariff premium in USD/CAD suggest that markets may only be pricing about a 5% chance of a 25% tariff... we argue that markets are underestimating the macroeconomic risks."
- **17 Jan 2025 ("Day One Deliberations"):** the same CAD gap re-quantified a week later, now larger — "implied probability of a 25% tariff estimated at 10-20% (up from 5%)" — with an explicit historical adjustment: GS's economists argued the *appropriate* premium should be larger than in the 2017-18 NAFTA renegotiation ("5pp vs 2pp today"), even though the market-implied premium was smaller.
- **28 Feb 2025 ("Accord and Discord"):** used comparatively across two similarly-exposed currencies to generate a relative-value trade — "Canada faces a number of vulnerabilities that we think make CAD more susceptible to tariff risks than MXN... we think this highlights the unique appeal of long USD/CAD calls as a tariff hedge," alongside a vol-adjusted short CAD/MXN.
- **21 Feb 2025 ("First Term Flashbacks"):** the same instrument applied to UK rates rather than FX: GS's economists' "100bp of quarterly cuts this year" compared against "~73bp priced by the market," read as implying "a gradual headwind to Sterling, rather than an acute depreciation."

## 1.5 Trade-Recommendation Lifecycle Discipline

**What it is:** Distinct from the manager letters (which describe positions retrospectively), GS's notes carry live recommendations through an explicit lifecycle: open with a stated rationale, tighten or extend the stop/target as the thesis is confirmed or the market moves, and close with a stated realized return — sometimes purely on rising *tactical* risk even while the *structural* thesis is reaffirmed unchanged.

**Key variables:** Entry rationale, target, stop, realized return at close, whether the closing rationale is thesis-invalidation vs. pure risk-management.

**How Goldman Sachs applied it:**
- **Short EUR/BRL** (the fullest lifecycle documented in the pilot window): opened mid-December 2024 on Brazilian real-rate carry; stop tightened to 105 (24 Jan 2025) then to 100.5 (17 Jan 2025, ahead of a binary US policy event) then to 103/target 108 (31 Jan 2025, "trading close to target"); **closed 28 Feb 2025** purely on rising tactical fiscal-noise risk (2025 budget, income-tax exemption proposal) while the medium-term view stayed constructive: "Given these factors, we close our trade recommendation for a potential total return of around 6-7%... While tactical risks have risen, we still forecast positive total returns for the Real over the next year."
- **Short AUD/JPY:** opened around 14 Mar 2025 (target 90.5, stop 97) as the preferred vehicle for a long-JPY view (funded via a risk currency rather than shorting USD outright); reiterated 21 Mar 2025; target **extended** to 85.0 and stop **lowered** to 91.5 on 4 Apr 2025 (post-"Liberation Day") specifically to protect an accrued ~3% gain while raising conviction from tactical to structural.
- **Short CHF/CZK** (long CHF): closed 3 Jan 2025 for "a potential return of around 0.3% after hitting our revised stop" — an example of a small, unremarkable close included for completeness rather than a headline trade.
- **Short CZK and HUF vs. EUR:** opened 28 Feb 2025 on a valuation/tariff-exposure asymmetry (CE3 rally "well-reflected" growth optimism but not auto-tariff risk); reiterated 7 Mar 2025 with an explicit rationale check ("rates-led rather than a growth-led" European move justifying continued muted CE3 performance); **closed 4 Apr 2025** post-Liberation Day for "a potential total returns of around 0.6%" as the broader EUR/CE3 relationship was re-assessed under the new "exceptionalism erosion" regime.
- **Long BRL/MXN:** **opened 17 Apr 2025** (target 3.60, stop 3.30, "~4.3% carry over 12 months") on a divergent-central-bank-reaction-function rationale — BCB cautious/hiking (BRL tailwind) vs. Banxico cutting fast (MXN headwind), with MXN judged to have "outperformed its typical sensitivity to US equities, yields and oil prices" without macro justification; stop **tightened to 3.40** 25 Apr 2025 "to protect gains"; **closed 16 May 2025** for a **potential total return of 1.4%**, not on thesis invalidation but on a house-wide pivot from carry-neutral relative-value expressions toward **outright carry** longs as risk sentiment improved — a clean example of a trade closed purely to reallocate risk-budget to a higher-conviction expression, not because the original thesis failed.
- **Long NOK/SEK (3-month 0.9450/0.9700 call spread):** **opened 25 Apr 2025** on EUR/NOK being "significantly above fair value," NOK/SEK "near its historical low," and NOK's "lower sensitivity to global risk" vs. an outright short EUR/NOK; **closed/took profit 30 May 2025** for a **potential total return on initial premium paid of around +20%**, once "NOK... moved quite a long way to close the gap between actual and implied performance in our GSBEER model" — thesis fulfilled, not invalidated.
- **Short AUD/JPY (as a tactical hedge, not an outright USD short):** carried through the entire batch with a documented *conditionality* shift — reaffirmed 17 Apr, 25 Apr, and 2 May even as price action "challenged" it; by **23 May 2025** ("The Bond and the Beautiful") GS explicitly narrows *when* it prefers this vehicle over the alternative: "we continue to favor short AUD/JPY as a hedge for a period of sharper risk-off. But in a more benign risk backdrop, short USD/JPY should be the better trade" — the hedge vehicle itself becomes state-dependent, not just the JPY view underlying it.
- **Short THB/KRW:** live and explicitly maintained through 20 Jun 2025 ("we remain bearish on the Baht relative to peers and maintain our short THB/KRW trade recommendation"), tied to a Thai political-crisis narrative (coalition partner withdrawal, pressure on the PM to resign) — no open date or realized return given in this batch; opening issue not yet in the processed range.
- **Long Korean equities (in USD):** live and reiterated 6 Jun 2025 on the Democratic Party's decisive election win (unified government → fiscal stimulus, trade progress, governance reform) reversing 2024's persistent FII outflow trend — a rare non-FX (equity) recommendation carried in these notes for a currency-adjacent theme; opening issue and realized return not yet in the processed range.
- **CHF short — screened but explicitly NOT taken (2 May 2025):** a documented pass/no-go decision distinct from every other 1.5 entry (which all track live positions) — "given the extent of the outperformance versus our shorter-term GSBEER model estimates... the Swiss Franc screens as a potentially attractive short. However, we remain cautious on the scope for CHF reversal... we think risk-reward in CHF shorts is less appealing in an environment of elevated recession risks." Valuable as the clearest evidence that lifecycle discipline includes *not* opening a model-flagged trade, not just managing ones already open.

## 1.6 Options vs. Spot as an Instrument Choice, Not Just a Directional Call

**What it is:** In several issues GS explicitly separates "are we right about direction" from "what is the cheapest/best-risk-adjusted way to express it," recommending options over outright spot specifically when a view is judged correct but crowded, or when volatility is judged cheap relative to fundamentals.

**Key variables:** Level of implied volatility vs. model-implied "fair" volatility (from a macro-uncertainty regression); crowdedness of the spot positioning; cost of carry on the spot alternative.

**How Goldman Sachs applied it:**
- **21 Feb 2025 ("First Term Flashbacks"):** implied vol shown to have fallen further than a macro-uncertainty regression justified — "while EUR/USD implied vol has moved lower in recent weeks, our models suggest that implied vol has fallen further than the decline in macro uncertainty" — leading to a structural recommendation: "long FX vol expressions can be a useful hedge against tariffs going forward."
- **28 Feb 2025 / 7 Feb 2025:** long USD/CAD calls repeatedly preferred to outright long USD/CAD spot as the tariff hedge of choice ("Long USD/CAD has performed quite well as a hedge when tariff risks escalate; we continue to think that it is a good option for investors looking for protection").
- **14 Feb 2025 ("War and Peace"):** for EUR/CZK and EUR/HUF, options-vs-spot reasoning based on a *comparative correlation* argument — Frontier FX (EGP/KES/NGN/TRY) selected into a carry basket specifically because forward-rate correlation with DXY/VIX is measured lower than mainstream EM carry currencies, making the basket a diversifying rather than a levered risk-on bet.
- **25 Apr 2025 ("Art of the Repeal"):** a clean new instance — long NOK/SEK expressed via a 3-month 0.9450/0.9700 call spread rather than spot, explicitly because NOK's "lower sensitivity to global risk" made an options structure the better-suited vehicle for a relative-value view that still carried some correlation to broader risk appetite.
- **23 May 2025 ("The Bond and the Beautiful"):** the choice extended from *which instrument* to *which currency to fund with* — "for investors who aim to maximize carry and feel comfortable leaning into a pro-risk, lower vol backdrop, we prefer funding in CHF rather than JPY," derived directly from that issue's finding that USD's safe-haven correlations were breaking down (see 3.3/9.5) while JPY's hedge properties remained more state-dependent (see 4.2).

## 1.7 Terms-of-Trade / Commodity-Shock Sensitivity Scaling

**What it is:** A standing tool that scales the implied FX impact of a hypothetical commodity-price shock (e.g., a 20% Brent increase) by each currency's commodity trade share of GDP, producing a ranked list of gainers and losers independent of any single country's narrative — distinct from 2.4's tariff-specific scaling rule, and from 1.1's cyclical-asset regression (which uses realized, not hypothetical, commodity moves as one input among several).

**How Goldman Sachs applied it:**
- **20 Jun 2025 ("Seven-Double-Oh, Look Out Below"):** introduced directly in the context of a Middle East-linked oil-price spike — "our terms of trade framework suggests that NOK, CAD and COP could see the biggest gains, while other currencies in Asia and Europe (net energy importers) could see the greatest losses" — paired with a conditional bivariate-regime analysis for COP specifically (median/90th/10th-percentile weekly returns across oil-up/down × S&P-up/down quadrants, 2012-2025 sample): "COP returns are typically positive when oil prices move sharply higher, but this move can be more muted if equities are falling at the same time."

## 1.8 US Treasury Semiannual FX Manipulation Report Monitoring

**What it is:** The first instance in the sample of GS treating a *third-party regulatory output* — the US Treasury's semiannual currency report (the Monitoring List, criteria for a formal "currency manipulator" designation) — as a standing input it systematically tracks, rather than only its own proprietary models. Distinct from cluster 5 (which is about China's own CNY management), since the report's scope spans multiple countries at once.

**How Goldman Sachs applied it:**
- **6 Jun 2025 ("Sliding into Summer"):** flagged that "future reports will 'strengthen' analysis of currency practices... more 'intensive analysis' of intervention behavior and 'greater vigilance' of a wide array of government practices including purchases by sovereign wealth funds or state pension funds to determine whether they effectively constitute currency intervention—just carried out by other government entities," applied across the Monitoring List roster (China, Japan, Korea, Taiwan, Singapore, Vietnam, Germany, Ireland, Switzerland).

---

# 2. The Tariff Transmission Mechanism and Its 2025 Reversal

This is the single most-developed thread across the pilot window: GS's own causal model of how tariffs move FX evolves week to week as tariff *design* (narrow/negotiable vs. broad/unilateral) changes, culminating in an explicit reversal of the sign of the relationship after "Liberation Day."

## 2.1 "Not All Tariffs Are Equal": Elasticity of Substitution as the Key Variable

**What it is:** Tariff burden can fall on foreign producer prices, US importer margins, or US consumer inflation — which channel dominates depends on how substitutable the taxed good is. Goods with few substitutes ("critical imports") let foreign exporters keep pricing power, meaning less of the adjustment needs to happen via the exchange rate — and if the Fed "looks through" the resulting US inflation, the net effect can even turn Dollar-negative in real terms.

**Key variables:** Elasticity of substitution for the taxed good category; whether the tariff is revenue-motivated vs. concession-motivated; the Fed's inflation reaction function.

**How Goldman Sachs applied it:**
- **14 Feb 2025 ("War and Peace"):** "tariffs can be paid through some combination of lower producer prices, lower US firm profits, or higher US inflation. Tariffs on less-substitutable goods like so-called 'critical imports' create less of an impulse for FX to respond." An explicit country exception is carved out for Canada, where GS's commodity strategists expected crude *producers* (not consumers) to bear most of the burden — reversing the usual critical-import logic.
- **3 Jan 2025 ("Tariff Special"):** the same elasticity logic applied structurally to Switzerland's export basket (pharma/medical equipment, ~35-55% of exports to the US): "technologically intensive, relatively price-inelastic, non-cyclical and protected by patents... Switzerland is somewhat more insulated from trade policy shocks and would likely be able to pass a majority of the cost of tariffs back onto US consumers."

## 2.2 The CNY-Fix-Endogeneity Argument: Why Tariffs Can't Be Fully Priced Ex-Ante

**What it is:** A foundational, near-verbatim-repeated heuristic: FX markets cannot fully price a tariff threat in advance because the size and composition of the eventual FX reaction depends critically on how China manages the CNY fix in response — an endogenous policy variable that can't be forecast independently of the tariff announcement itself.

**How Goldman Sachs applied it:**
- **24 Jan 2025 ("A Brief Relief"):** "it is impossible for FX markets to fully 'price' tariff risks ahead of time, because China's currency response is an important input."
- **10 Jan 2025 ("More Bang for the Buck"):** "it is challenging—if not impossible—for FX markets to fully price tariff risks ahead of time because movements in the CNY fix will be critical for the size and composition of the broad market reaction."
- **31 Jan 2025 ("Tariff-fied"):** extended to a systemic-transmission claim — "potential tariffs on China open the possibility of a change in CNY management, which can have reverberations across the market," treating a CNY regime change as a trigger for volatility well beyond CNY itself.

## 2.3 "Day 1 Pledges" Discount and the Asymmetric Tariff-Outcome Payoff

**What it is:** GS argued markets were over-reading campaign/inauguration rhetoric literally, drawing on the pattern that Day-1 executive actions tend to be symbolic. Because current pricing embedded only limited tariff premium, the resulting payoff structure was explicitly asymmetric: real implementation should produce a large Dollar upside move (premium added from a low base), while a delay should produce only a small move lower (the market merely raising the odds of a 2017-style non-event, not unwinding a large premium it never built).

**How Goldman Sachs applied it:**
- **17 Jan 2025 ("Day One Deliberations"):** "We think investors are probably taking 'Day 1' pledges too literally... Rather than next week bringing clarity, we think the storm is just rolling in. We expect it will pay to be patient."
- **24 Jan 2025 ("A Brief Relief"):** the follow-through a week later, explicitly attributing the Dollar's dip to a *positioning reset* rather than a fundamental repricing, and cross-checking against rate differentials to rule out "double counting" the tariff premium: "we attribute the majority of the move this week to a positioning reset... rate differentials were little changed on the week, which gives us some comfort that the Dollar can outperform rate differentials similarly to last time if tariff expectations are realized." Flagged the explicit risk that a full 2017-style repeat (rhetoric without action) was "clearly higher now than it appeared a week ago."
- **31 Jan 2025 ("Tariff-fied"):** the payoff asymmetry stated directly — "if the February 1st deadline comes and goes with more words but without action... we would expect a limited move lower in the Dollar... But even in that episode [2018], tariffs did eventually materialize... and provide a bullish impulse."

## 2.4 Effective-Tariff-Rate Scaling as a Blunt but Standing FX Sensitivity Rule

**What it is:** GS periodically converts an expected change in the aggregate US effective tariff rate into an approximate broad-Dollar impact via a simple linear rule of thumb, explicitly caveated as a rough approximation with wide error bands — used to size how much of prospective Dollar strength is attributable to the tariff channel specifically, distinct from rates or growth channels.

**How Goldman Sachs applied it:**
- **3 Jan 2025 ("Tariff Special"):** the underlying event-study calibration — "the broad Dollar appreciated by around 2.5% for an unexpected $100bn in US tariff revenue from China" — explicitly flagged as trained on 2018-19 conditions and therefore likely mis-calibrated for a different-sized, differently-composed 2025 trade shock.
- **14 Mar 2025 ("Less Bang for the Buck"):** the rule restated with an updated scaling factor and an explicit uncertainty band: "the 10pp increase in the effective tariff rate we expect should be worth around 5% on the broad Dollar. However, there are wide error bands around that estimate... we think of it as a significant 'head start' for the Dollar, but not an insurmountable lead."
- **11 Apr 2025 ("Dollar Wreckoning"):** the same scaling logic revisited after Liberation Day, but now used to describe a shock "the sharpest rise in the US effective tariff rate in more than 100 years" — a case where the calibrated rule's historical range was explicitly exceeded, contributing to the framework's reversal (see 2.5).

## 2.5 The "Exceptionalism Erosion" Reversal

**What it is:** The pilot window's central regime shift. Through March 2025, GS's baseline held that a hawkish trade agenda should be Dollar-positive (tariffs force adjustment onto trading partners). After the April 2 "Liberation Day" reciprocal tariffs, GS explicitly reversed the *mechanism*, not just the forecast number: because these tariffs were broad and unilateral rather than narrowly targeted, foreign producers had less incentive to offer any accommodation — supply chains and consumers being relatively inelastic in the short term meant "US businesses and consumers become the price-takers, and it is the Dollar that needs to weaken to adjust."

**Key variables:** Breadth/unilateral design of the tariff (vs. targeted/negotiable); short-term elasticity of the affected supply chains; erosion of US institutional/governance credibility as a separate, compounding channel.

**How Goldman Sachs applied it:**
- **28 Mar 2025 ("Drawbacks of the Clawbacks"), pre-shock baseline still intact:** "our economists expect a high initial headline, but a relatively long implementation period with an expectation that the final tariff levied will be lower than the initial proposal—negotiation is a feature, not a bug."
- **4 Apr 2025 ("From Diminished to Finished"), the reversal:** "Rather than clearly targeted tariffs that allow precise room for negotiation, with such broad, unilateral tariffs there is less incentive for foreign producers to provide any accommodation... it is the Dollar that needs to weaken to adjust if supply chains and/or consumers are relatively inelastic in the short term... we are now making that our base case." EUR/USD forecast revised from 1.07/1.05/1.02 to **1.12/1.15/1.20** (3/6/12m); USD/JPY from 150/151/152 to **138/136/135**.
- **11 Apr 2025 ("Dollar Wreckoning"), conviction raised further:** the reversal reinforced with a distinct governance-credibility argument (see 3.4) — "the recent breakdown in usual correlations is a clear signal that markets are concerned about what recent policy actions imply about US governance and institutional credibility."
- **17 Apr – 13 Jun 2025, conviction held and explicitly defended against counterarguments as the quarter wore on:** 25 Apr ("Art of the Repeal") pre-empts a "positioning is stretched" objection by distinguishing tactical from structural conviction — "while tactical Dollar shorts have increased and moves have outstripped our short-term GSBEER models, the whole point is that structural positioning is still very long"; 16 May ("Some Things Change, Some Stay The Same") restates the thesis despite better US data specifically to show the reversal wasn't data-dependent — "Despite a somewhat brighter US outlook, we still expect the Dollar to weaken... Tariffs around here will still weigh on US consumers' real incomes and US firms' margins"; 13 Jun ("And So It Flows") frames this discipline explicitly as a defense against narrative drift — "it is important to keep this framework in mind to avoid 'drifting motivations' to match the market narrative of the day."

## 2.6 The Dollar Smile's Left Tail as the Risk to the New Bearish Base Case

**What it is:** The "Dollar smile" — USD strengthens at both extremes (strong US-relative growth, or acute global crisis) and is weakest in the "normal" middle — is invoked as the specific risk that could invalidate the new bearish-Dollar call: if tariff-driven disruption becomes severe enough to trigger a genuine global growth scare, the crisis/safe-haven leg of the smile could reassert Dollar strength even as the "exceptionalism erosion" mechanism argues for weakness.

**How Goldman Sachs applied it:**
- **4 Apr 2025 ("From Diminished to Finished"):** "it is possible that the rapid shift in tariff policy will create global disruptions sufficient to activate the 'left tail' of the Dollar smile that currently looks further away" — flagged as a risk to the base case, not a trade itself.

---

# 3. The Dollar Cycle, the Fed, and the De-Dollarization Debate

## 3.1 Rate Differentials as the Primary (and Testable) USD Driver

**What it is:** The single most repeated USD framework in the pilot window: shifts in US policy-rate expectations relative to the rest of the world are treated as the dominant, most easily quantified Dollar driver — tested directly against a fitted rate-differential series (see 1.1) rather than asserted qualitatively.

**How Goldman Sachs applied it:**
- **10 Jan 2025 ("More Bang for the Buck"):** "This has been largely on the back of a shift higher in US policy rate expectations, which tends to be the most supportive environment for the currency." The Fed's expected path had been revised twice in a month, "from 'skip' to 'pause'"; Dollar forecasts upgraded across the board.
- **10 Jan 2025:** a divergence between GS's own model assumptions and realized market behavior flagged as informative in its own right — GS's models had assumed tariffs would produce a negative US growth response, but markets instead upgraded US growth expectations post-election: "even if markets are already fully incorporating tariff risks, there is still some Dollar upside relative to our previous assumptions."

## 3.2 The "Balance of Opposing Forces" Framing

**What it is:** GS's recurring way of holding the USD/EUR view as a net of two simultaneously moving, opposing policy channels — US tariffs (Dollar-positive, via foreign-growth damage) vs. foreign (chiefly European) fiscal expansion (Dollar-negative, via better foreign investment opportunities) — explicitly re-weighted as facts evolve rather than treating either channel as fixed.

**How Goldman Sachs applied it:**
- **7 Mar 2025 ("Schwarze Null No More"):** "the European policy response has clearly been stronger than expected, which shifts the potential balance between the tariffs that are Dollar-positive, and foreign fiscal spending which should create more attractive investment opportunities elsewhere and weaken the Dollar." Concluded "risks have moved further in the direction of less Dollar strength" — a moderation, not a reversal, at this stage (the reversal itself comes three weeks later, see 2.5).
- **14 Mar 2025 ("Less Bang for the Buck"):** the framework explicitly generalized into a "value in both tails" positioning stance given both legs (US policy, foreign response) were moving simultaneously and could combine destructively or constructively.
- **30 May 2025 ("Tariff-ride"):** the two-channel decomposition given a cleaner empirical signature — tariff de-escalation-driven risk recovery showed up as "more TWI weakness against riskier DM and EM currencies and more DXY stability," i.e. the two forces were now visibly separable in *which* Dollar index moved, not just inferred narratively.

## 3.3 Conditional Dollar Safe-Haven Activation

**What it is:** The Dollar's safe-haven property is modeled as state-dependent, not constant — it activates specifically when there is no more room to price Fed cuts, or when growth fears are global rather than US-specific. Outside those conditions, bad US news can weaken rather than strengthen the Dollar, since it simply gets priced as more Fed easing.

**How Goldman Sachs applied it:**
- **7 Mar 2025 ("Schwarze Null No More"):** used to explain why the Dollar fell on tariff implementation news, decomposed into "disbelief and rate relief" (low perceived durability of the tariffs, plus falling US rate expectations on soft data) rather than "tariffs are Dollar-negative" per se: "the Dollar's safe-haven attributes are only activated when there is no room to price Fed cuts or the recession fears are more global, which is not the dynamic now."
- **16 May 2025 ("Some Things Change, Some Stay The Same"):** the state-dependency itself named as the bear case's own tail risk, not just an explanatory device — "we remain concerned about the 'right tail' risks for the Dollar. The currency's strength stems from a long period of better return prospects that has pulled in foreign investor capital... If the US can maintain that position, then there is one less reason for the Dollar to fall."
- **23 May 2025 ("The Bond and the Beautiful"):** the correlation breakdown made explicit and dated, in a standalone "Reassessing the Safest Havens" section — "One of the most meaningful shifts in markets in recent months has been the Dollar's diminished safe haven appeal. Not only has its positive relationship with rate differentials become less reliable, its more typical inverse correlation with equities—especially in sharper sell-offs—has also become challenged." This is also the point where GS first argues EUR has joined the safe-haven set (see new 9.5) and where USD becomes the *preferred* EM-carry funding currency specifically because its safe-haven correlation broke (feeding into 6.1's funder-selection logic and 1.6's currency-choice-of-funding-leg example).
- **30 May 2025 ("Tariff-ride"):** the same diminished-correlation finding applied to justify a *specific currency's* insulation from risk-off, generalizing the framework beyond USD/JPY/EUR to a Scandi cross — "USD/SEK in particular should be more insulated than usual from a risk-off episode given shifting cross-asset correlations and the Dollar's diminished safe haven appeal."

## 3.4 Governance-Credibility Repricing: The UK-2022 Analogy

**What it is:** GS's most striking framework in the sample: a specific, unusual co-movement signature (yields rising, equities falling, Dollar falling — simultaneously) is read as evidence markets are pricing a governance/institutional-credibility problem, not conventional growth/inflation dynamics, because it breaks the standard rates-support-the-Dollar relationship. Cross-checked with two further diagnostics: a rarity/percentile count of days combining a rising EUR with a falling S&P 500, and the explicit *absence* of a "dash for Dollars" (funding stress) that a generic risk-off episode would normally produce.

**Key variables:** Co-movement of yields/equities/Dollar; historical base rate of days with the same combination since 1980; presence/absence of Dollar funding stress.

**How Goldman Sachs applied it:**
- **11 Apr 2025 ("Dollar Wreckoning"):** "The recent breakdown in usual correlations is a clear signal that markets are concerned about what recent policy actions imply about US governance and institutional credibility, and the confluence of a steepening curve, lower equities and a weaker dollar point to worrying parallels to the UK in late 2022." Only five days since 1980 had shown a matching EUR-up/S&P-down combination of the stated magnitude. The absence of funding stress was read as confirming this was Dollar-specific weakness, not generic risk-off: "despite record-breaking market moves, there have been few signs of Dollar funding stress... this has not been a market that is scrambling for Dollars—if anything, it is the opposite."
- **23 May 2025 ("The Bond and the Beautiful"), the analogy escalated onto the US itself:** the same co-movement signature (yields up, bond market dislocation) reappears around the "One Big Beautiful Bill" fiscal episode, with GS explicitly naming this a fiscal/governance-credibility issue rather than a growth/inflation one — "the renewed focus on lingering fiscal concerns has seen a sharp bear steepening in the US curve, and long-end yields testing multi-decade highs... clear examples of fiscal-related rates market dislocations in the likes of Japan and Brazil. But the US-led bond market gyrations have important implications for FX markets in and of themselves." The same issue also runs a parallel version of the argument *for* Japan, concluding JGB fiscal fears should weigh less on JPY than on other currencies because "Japan is not as reliant on foreign buyers as are other markets... the MoF has already signaled a potential willingness to reduce supply at the long end of the curve" — a direct cross-country test of the same governance-credibility mechanism, with an opposite conclusion for the currency in question.

## 3.5 Official vs. Private Capital Flows and "Mar-a-Lago Accord" Skepticism

**What it is:** GS separates USD demand into official (central-bank reserve) flows and private (return-seeking) flows to argue two things: (a) any coordinated-devaluation "deal" narrative aimed at reserve managers misses the point, since reserve managers had reportedly already been net sellers of Dollars; and (b) the more plausible non-market channel for Dollar depreciation is not a Plaza-style accord but an organic shift in the US/foreign fiscal mix (US consolidation + foreign — especially European — expansion) that narrows growth/rate differentials without requiring any coordinated intervention.

**How Goldman Sachs applied it:**
- **21 Feb 2025 ("First Term Flashbacks"):** "USD demand has come from private investors, while reserve managers have already been selling Dollars, most likely in an effort to stabilize their currencies against the strong Dollar. We still think the more plausible... route to a currency 'deal' would involve increased foreign spending."
- **28 Feb 2025 ("Accord and Discord"):** the historical-pact test (1.3) applied directly to this debate — "for FX intervention to be successful, it helps for market forces to be pushing in the same direction... That was the case before both of those seminal currency pacts; it is not the case now. The strong Dollar of the last decade is not the product of official demand... but private capital from other developed markets chasing superior return prospects" — while still granting partial, real-world validation of the fiscal-mix channel (EU defense-spending pledges including "significant purchases of US equipment"): "we have to acknowledge that there has clearly been some halting progress in this direction."
- **28 Feb 2025:** a related "who's actually big enough to move the needle" filter applied to popular narratives — Japan, though often cited as central to a currency deal, dismissed as "only a marginal player in this theater" given its shrinking share of the US trade balance.
- **21 Mar 2025 ("Rhetoric vs Returns"):** the official/private distinction reiterated as a rebuttal to "de-dollarization" rhetoric: "the strong Dollar demonstrates that private sector flows have more than compensated for this change so far. To stem the recent outflows, returns not rhetoric will be the ultimate arbiter."
- **17 Apr 2025 ("The ResEURrection"):** extended with a specific reassurance against the "large disruptive unwind" fear, distinguishing private ownership growth from any active liquidation signal — "the private share of UST ownership has grown since at least 2012... our negative Dollar view is more aligned with a shift in where the future 'marginal' dollar will be allocated, rather than a large and disruptive unwind of current positions."
- **20 Jun 2025 ("Seven-Double-Oh, Look Out Below"):** the April TIC data reviewed against the same three-part lens GS has used throughout — net Treasury sales judged modest (consistent with the no-disruptive-unwind view), but with a notable composition shift: "it is notable that the private sector led the active outflows, which is a notable change from the recent trend... the Dollar outlook depends in large part on whether private sector demand will be persistently weaker," plus a Canada-specific investor-behavior angle tied to the trade dispute.

## 3.6 Portfolio Reallocation: Stock-vs-Flow Decomposition

**What it is:** A more granular successor to 3.5's official-vs-private lens, applied specifically to *private* portfolio flows: GS decomposes Dollar depreciation into a "stock" effect (the large, largely static pre-existing foreign overweight in US assets, which does not need to be liquidated for the Dollar to weaken) versus a "flow" effect (the marginal direction of *new* investment), and quantifies the flow-to-FX elasticity directly — an empirical anchor distinct from 3.5's more narrative TIC-data reassurance.

**How Goldman Sachs applied it:**
- **9 May 2025 ("Big Deal"):** the elasticity stated explicitly — "We expect this reallocation to show through a shift in marginal demand, rather than a disruptive sale of US assets... a portfolio inflow of about 1% of assets amounts to a 0.3% appreciation vs the Dollar."
- **13 Jun 2025 ("And So It Flows"), the issue's own title theme:** EPFR foreign-equity-fund-flow data invoked as leading evidence the flow-side thesis was becoming visible in hard data, cross-checked against the 2017 EUR-rotation analogue (1.3) — "In hindsight, it is clear that the move in 2017 coincided with a shift in capital flows back into the Euro area. We think something is happening now, and this is consistent with preliminary data on fund flows."

## 3.7 Fiscal and Tax-Policy Risk to US Asset Demand

**What it is:** A cluster of related, newer channels through which US fiscal/tax policy — not tariffs — could raise the cost of foreign capital funding the US current account deficit: a specific legislative provision (Section 899) that functions as a quasi-capital-control; a formal regression showing Treasury issuance has historically been Dollar-*positive* only for the US (via reliably rising foreign demand), a relationship GS flags as potentially eroding; and a taxonomy separating which EM/high-beta currencies are hit via the rates channel of a fiscal shock versus the credit channel.

**How Goldman Sachs applied it:**
- **30 May 2025 ("Tariff-ride"), precursor:** "if tariffs are impeded, attention may shift to other ways of raising revenues which may be even more negative for the Dollar... a potential change to tax rates on foreign individuals and companies in the draft fiscal bill."
- **6 Jun 2025 ("Sliding into Summer"), the mechanism named directly:** "A provision in the House-passed fiscal package (H.R. 1), would create a new Section 899 of the tax code, raising the US tax on many forms of passive income... changes like this move in the direction of making the US a less welcoming destination for foreign capital... we would expect that even an incremental move toward new capital controls is likely to lead foreign investors to demand more compensation than before to fund the growing current account deficit." The same issue runs the Treasury-issuance regression — "greater net Treasury issuance is a positive for the Dollar on average. That result does not apply to the US's G10 peers though, but instead is a function of the US-specific privilege in typically seeing foreign demand for Treasuries increase in step with higher net issuance... it is possible that the historical relationship... will eventually begin to look more like what we observe in other G10 economies" — and the rates-vs-credit transmission taxonomy: "a sharp steepening in US 5s30s tends to weigh more on high yielding currencies, such as BRL, MXN and INR... a sharp widening in US credit default swaps is typically associated with underperformance in more cyclical currencies such as ZAR, NOK and AUD."
- **13 Jun 2025 ("And So It Flows"):** the Section 899 logic tied back to the official/private-flow framework (3.5) — "most FX reserves are held in Dollars not because of superior prospective returns, but because the Dollar is the currency of intervention for most countries and the transaction currency for most trade... The question now... is whether private capital will follow the same pattern."

---

# 4. Yen and Safe-Haven Dynamics

## 4.1 "It's Not You (BoJ), It's Me (the US)" — US-Outlook Dominance for USD/JPY

**What it is:** GS's standing thesis that USD/JPY is driven overwhelmingly by the US macro/rates outlook, not BoJ policy surprises. A hawkish BoJ hike is treated as nearly irrelevant to the Yen if the US narrative is unchanged; conversely a US growth scare (even a false one) moves the Yen sharply. A companion, counter-intuitive causality claim: a weak Yen is what gives the BoJ room to keep hiking (via the inflation/import-price channel), so hawkish BoJ repricing shouldn't automatically be read as JPY-bullish.

**How Goldman Sachs applied it:**
- **31 Jan 2025 ("Tariff-fied"):** "The past week and a half served as a clear example of why we have long messaged that the US outlook matters most for USD/JPY" — the BoJ hiked with a hawkish inflation message and the Yen "still ended the NY trading day barely unchanged," while a subsequent US growth scare (DeepSeek) moved it sharply.
- **17 Jan 2025 ("Day One Deliberations"):** "gradual BoJ hikes are not an impediment to a weaker Yen and, in fact, a weak Yen allows for more sustained policy tightening" — the inverted-causality companion claim.
- **24 Jan 2025 ("A Brief Relief"):** the same thesis applied to a live BoJ hike — despite an upgraded inflation forecast and a hawkish tone, "it is difficult to see a path for sustained Yen appreciation" absent a change in the US growth/rates picture, because "the past 10 days have indeed seen a narrowing in the real 10-year rate differential... but the move lower was largely driven by the rally in US rates," not BoJ action.

## 4.2 JPY as a Conditional, Vol-Regime-Dependent Growth-Shock Hedge

**What it is:** JPY's safe-haven property is treated as conditional on the specific *signature* of the shock (equities and yields falling together — a genuine US growth scare, not generic volatility) and, more precisely, on the prevailing VIX regime: GS quantifies average USD/JPY returns across VIX buckets on days when bonds and equities sell off together, finding JPY's outperformance strengthens monotonically with the VIX level, including outright appreciation vs. USD at peak-VIX levels.

**Key variables:** Co-movement signature (equities + yields both falling); VIX bucket (unconditional, >20, >30, >40); comparability of the current episode to the historical distribution.

**How Goldman Sachs applied it:**
- **31 Jan 2025 ("Tariff-fied"):** "we have previously found that the Yen typically sees the biggest gains when there are rising concerns about the US economy that press both equities and yields lower together," citing the DeepSeek episode and "last August" as the two comparable prior triggers; explicit relative preference stated: "we would prefer being long CHF over JPY" at that specific moment, given upside inflation risk persistence.
- **14 Mar 2025 ("Less Bang for the Buck"):** the regime-conditioned cross-selection refinement — a long JPY position funded via a risk-sensitive currency (AUD or CAD) tested by regime and shown to produce a better Sharpe ratio than an outright short-USD expression specifically in the "yields down + equities down" quadrant: "long JPY paired with a riskier currency tends to produce the best returns in that backdrop... We prefer AUD over CAD given its lower vulnerability to better-than-expected news on tariffs." (Short AUD/JPY, target 90.5, stop 97 — see 1.5 for the full lifecycle.)
- **11 Apr 2025 ("Dollar Wreckoning"):** the VIX-bucket regression formalized directly — "when we calculate average USD/JPY returns since 2000 on days when bonds and equities are both selling off, we find that the Yen tends to increasingly outperform the broad USD when the VIX trades at higher levels—and it outright strengthens vs USD on days when the VIX is trading at peak levels."
- **25 Apr 2025 ("Art of the Repeal"):** the conditionality tested rigorously across four sub-episodes (auto tariffs, reciprocal tariffs, +1 week, +2 weeks) rather than asserted in general — "Being long the Japanese Yen versus the Dollar—or short USD/JPY—tends to be one of the most effective FX hedges against recession fears. But price action over the past month exhibits both its benefits and limits as a risk hedge... it 'failed to work' in late March around the auto tariffs announcement... A backdrop of higher yields tends to be the one case in which USD/JPY moves higher even alongside lower equities" — the cleanest, most falsifiable statement of the sub-cluster's conditionality found in the corpus so far.
- **2 May 2025 ("Waiting on the World to Change"):** a live instance where the hedge held up despite an unfavorable rates backdrop, with GS reasoning through why — "The fact that JPY rallied in spite of higher yields and also outperformed EUR—which typically occurs in a backdrop of greater growth concerns—suggests some demand for adding longs at more attractive levels."
- **23 May 2025 ("The Bond and the Beautiful"):** the conditionality extended from "does the hedge work" to "which JPY vehicle is the better hedge in which regime" — "we continue to favor short AUD/JPY as a hedge for a period of sharper risk-off. But in a more benign risk backdrop, short USD/JPY should be the better trade" (cross-reference 1.5).

## 4.3 GPIF Repatriation Speculation, Tested Against the Data Each Week

**What it is:** Japan's government pension fund (GPIF) undergoes a mechanical five-year strategic-allocation review, treated as a scheduled, semi-predictable flow catalyst — but distinctively, GS re-checks the *speculation* about this catalyst against actual weekly flow data each issue, rather than assuming the narrative is already validated, using the 2020 review cycle as the base-rate template.

**How Goldman Sachs applied it:**
- **14 Feb 2025 ("War and Peace"):** decomposed USD/JPY's move into a rates-explained component and a residual, attributing the residual specifically to repatriation/currency-deal speculation, and explicitly advising against trading it yet: "The GPIF is set to complete its strategy review by end of March... and there could be some broader repatriation flows if targets shift... But we think it is too early to be positioning for that outcome."
- **21 Feb 2025 ("First Term Flashbacks"):** the falsification test itself (see 1.3) — checking weekly flow data against the 2020 precedent and finding no confirming signal yet.
- **7 Feb 2025 ("From Tariff-fied to Tariff-fried"):** flagged the key unresolved mechanism question that would determine whether repatriation speculation even makes sense as a framework: "a question remains whether the reallocation would involve foreign bond sales or simply greater FX hedging" (real flow vs. hedging-ratio effect only) — and separately flagged a political catalyst (a Trump-Ishiba meeting) as a source of *speculative*, not fundamentals-driven, JPY moves, explicitly graded as unlikely to be tradeable near-term: "we are skeptical that markets can price either on a sustained basis in the very near-term."
- **9-23 May 2025, the same mechanism extended to non-Japan comparators for the first time:** Taiwan (9 May, "Big Deal") — "There are a number of parallels to Japan... Taiwan's foreign asset holdings (debt + equity based on the IIP data) totaled nearly $1.4tn as of end-2023. Meanwhile, Japan's holdings summed to over three times that, roughly $4.4tn," used to read Taiwan's own two-day 7-8% TWD rally as a preview of what a Japanese hedge-ratio shift could look like; and Korea's National Pension Service (23 May, "The Bond and the Beautiful") with the batch's first quantified flow estimate for this whole framework — "we think could be worth US$4bn of USD/KRW forward sales per month (on average), as they look to increase the FX hedge ratio on their overseas assets worth around US$500bn." 16 May ("Some Things Change, Some Stay The Same") groups all three under one sentence — "Japan—like Europe and Taiwan—has been a major source of increasingly unhedged US portfolio inflows in recent years."

## 4.4 Safe-Haven vs. High-Beta Cluster Analysis

**What it is:** Currencies are grouped into a "safe haven cluster" (JPY/USD/CHF) and a "high-beta cluster" (AUD/NZD/Scandi/CAD), and historical weekly returns for each cluster are measured across four macro-shock quadrants (growth up/down × policy hawkish/dovish) — used to justify upgrading a JPY view from tactical to structural conviction once the prevailing quadrant (negative growth shock) is identified as the one where the safe-haven cluster systematically outperforms.

**How Goldman Sachs applied it:**
- **4 Apr 2025 ("From Diminished to Finished"):** "Higher US recession risk and elevated policy uncertainty strengthens the case to own safer assets. We had already been recommending tactical longs in JPY but our shorter-term preference has now flipped to a structural one" — the cluster-return framework was the explicit justification for extending the short AUD/JPY target from 90.5 to 85.0 and lowering the stop from 97.0 to 91.5.

## 4.5 JPY-vs-CHF Safe-Haven Differentiation (Rate-Sensitive vs. Geopolitical/Inflation-Sensitive)

**What it is:** A distinction not present in the pilot window's framing of cluster 4: JPY and CHF are both "safe havens," but by a different mechanism, and can diverge or even move in opposite directions depending on the shock's nature. JPY is rate-sensitive — it can *weaken* against the Dollar during a risk-off episode if US yields are simultaneously rising. CHF behaves more like gold — appreciating specifically during geopolitical/inflation-driven turmoil, largely independent of the US rates backdrop. Which one is the better hedge in a given week therefore depends on diagnosing *which kind* of risk-off is underway, not just that one is underway (cross-reference 4.2, which covers JPY's own VIX-regime conditionality; 4.5 is about choosing between JPY and CHF, not about JPY alone).

**How Goldman Sachs applied it:**
- **31 Jan 2025 ("Tariff-fied"), pilot-era precursor:** "we would prefer being long CHF over JPY" at that specific moment, given upside inflation-risk persistence — recorded in the pilot under 4.2 but really an early instance of this distinction.
- **2 May 2025 ("Waiting on the World to Change"), the distinction stated and tested directly:** "the Yen is a particularly rate sensitive safe-haven and can *weaken* vs the Dollar in periods of risk-off if US yields are rising at the same time... the Franc, much like gold, tends to appreciate in times of geopolitical turmoil and escalating inflation fears, and both are a more prominent feature of the current backdrop than typical periods of recession fears" — backed by an exhibit conditioning CHF/JPY/USD returns jointly on VIX changes and US 10y yield direction, both since 1 April 2025 and since 2018 for robustness.
- **13-20 Jun 2025 ("And So It Flows" / "Seven-Double-Oh, Look Out Below"):** the geopolitical side of the distinction quantified across named historical conflict episodes (Gulf War, Second Intifada, 9/11, Iraq invasion, Russia/Ukraine, Israel-Gaza) — "Looking across a number of relatively recent instances of conflict we have found that the Franc typically performs similarly to gold... CHF should be the preferred safe-haven even over JPY, in our view, if the primary focus shifts from US recession risks to geopolitical risks."

---

# 5. China, CNY Management, and Asia FX

## 5.1 The CNY Fix as a Regional Anchor (Revealed Preference)

**What it is:** The PBoC's demonstrated behavior — holding the daily fix stable through repeated tariff escalations — is read as a revealed policy preference that can be extrapolated forward as an anchor for the entire USD/Asia complex, not just CNY itself. GS explicitly reads the *pattern* of fix-setting (not official communication) as the more reliable signal of intent.

**How Goldman Sachs applied it:**
- **21 Feb 2025 ("First Term Flashbacks"):** an early instance of the "expectation-anchoring" version of this argument — the initial 10% China tariff was smaller than the 60% pre-election threat, and the muted fix response ("the USD/CNY fix moved slightly stronger" rather than weaker) was read as a confidence signal reinforcing market relief: "The response to the 10% tariff imposition has been far less than proportional... and the USD/CNY fix moved slightly stronger."
- **24 Jan 2025 ("A Brief Relief"):** "policymakers have kept the fix relatively stable when tariff speculation is high... and make adjustments only after there are changes in trade policy... it is impossible for FX markets to fully 'price' tariff risks ahead of time, because China's currency response is an important input."
- **28 Mar 2025 ("Drawbacks of the Clawbacks"):** the anchor claim generalized explicitly to the whole regional bloc — "Given the PBoC's revealed preference for FX stability–the USD/CNY fix has stayed around 7.17 since inauguration day... this should provide an anchor for the rest of USD/Asia."
- **14 Mar 2025 ("Less Bang for the Buck"):** extended into a policy-substitution claim — stability in the fix is read as evidence the PBoC's reaction function favors *other* tools (monetary, fiscal, housing, credit) to absorb the tariff shock rather than FX: "we think Chinese policy makers will primarily rely on other tools... as opposed to relying heavily on the FX lever, with the risk that the Renminbi could even move stronger."
- **2-9 May 2025, the anchor turning from headwind to tailwind:** "the USD/CNY fix has drifted lower again in recent days, and both onshore and offshore spot CNY levels are essentially stable to stronger versus the Dollar... it could clear the way for swifter moves in other currencies in NJA such as KRW and TWD" (2 May); "we now forecast USD/CNY to gradually move lower through the year, shifting from a headwind to a tailwind to many EM currencies, for which the cross is an important anchor" (16 May, "Some Things Change, Some Stay The Same").
- **20 Jun 2025 ("Seven-Double-Oh, Look Out Below"):** the anchor thesis pushed further than any prior forecast — GS rolls its USD/CNY path through its own year-end target and below it: "these moves have now taken us through our 3m forecast of 7.20. So we are rolling our forecasts to 7.10, 7.00 and 6.90 in 3m, 6m, and 12m (from 7.20, 7.10 and 7.00 previously), retaining the 7.00 year-end target, but now expecting a move below that in the year ahead" — a standard forecast-roll-on-breach (1.5) applied to a round-number psychological level in USD/CNY, which the issue's own title ("Seven-Double-Oh") plays on.

## 5.2 The Counter-Cyclical Factor (CCF) as a Quantified Management Gauge

**What it is:** A refinement of 5.1: the fix-setting mechanism embeds a discretionary "counter-cyclical factor" (CCF) that GS tracks directly as a numeric gauge of how actively the PBoC is leaning against depreciation pressure — turning a qualitative "stable fix" read into a measurable, comparable-over-time series.

**How Goldman Sachs applied it:**
- **11 Apr 2025 ("Dollar Wreckoning"):** "The counter-cyclical factor (CCF) has remained around 1300 pips, compared to 700-800pips pre-tariff announcement. Taken together, this suggests that despite growing economic headwinds, policymakers are managing the pace of CNY depreciation against the Dollar, and avoiding a rapid move" — used alongside a revised, larger China growth hit (2025/26 GDP cut to 4%/3.5%) to argue depreciation, not absent, was simply being paced rather than blocked.
- **23 May – 13 Jun 2025:** the gauge tracked back down to neutral as the regime flipped from managed-depreciation to managed-appreciation — "With the countercyclical factor already at neutral levels and the appreciation in the rest of Asia leading to meaningful weakening on a basket basis, the key question will be whether policymakers now allow the CNY fix to grind stronger more consistently in coming days" (23 May, "The Bond and the Beautiful"); "with the counter-cyclical factor at neutral levels, a willingness to move the fix steadily stronger, we think investors should continue to focus on the potential for an appreciating Renminbi" (13 Jun, "And So It Flows").

## 5.3 Beta-to-CNH as a Cross-Sectional Risk-Ranking Tool

**What it is:** A regression-based ranking of each EM/Asia currency's sensitivity to a given move in USD/CNH, controlling for common global risk factors — used to identify which currencies are most exposed to a China-driven shock independent of their own carry or volatility profile, and to explain why Asia FX broadly screens more China-sensitive than LatAm FX (ex-CLP).

**How Goldman Sachs applied it:**
- **10 Jan 2025 ("More Bang for the Buck"):** "when focusing on betas to CNY moves – which will be a key input to the overall FX market reaction to tariffs – Asian currencies are more sensitive to moves in this anchor than their LatAm peers (outside of CLP)," with CZK, HUF, ZAR, PLN, MYR, KRW ranked highest and MXN, INR, PEN, BRL, COP lowest.
- **3 Jan 2025 ("Tariff Special"):** the same logic applied specifically to KRW, flagged as the single most CNY-sensitive currency historically: "our sensitivity analysis shows that KRW was the most sensitive currency to CNY over the last 10 years. Therefore, a move higher in USD/CNY towards 7.5 amid a US-China trade war could translate into a larger move for USD/KRW versus other Asian currencies" — but immediately offset by an itemized list of concrete official-sector buffers (swap-line expansion, NPS hedging-ratio increases) treated as a policy-capacity counterweight to the standalone beta exposure.
- **9 May 2025 ("Big Deal"):** the beta ranking reapplied once CNY turned tailwind (5.1) — "with USD/CNY also likely to drift lower, we think this clears the path for Asian FX to rally further in the coming months," differentiating TWD, KRW, MYR, THB, IDR, INR by beta and by repatriation-flow exposure (cross-reference 5.4).
- **23 May 2025 ("The Bond and the Beautiful"):** the Korea NPS repatriation flow already noted under 4.3's cross-reference here supplies the batch's only quantified beta-to-flow figure ($4bn/month), plus supplementary color on a "Value-Up" corporate-governance equity theme and "Korea discount" narrowing — noted as country-specific color rather than a separate framework.

## 5.4 Asia Exporter USD-Deposit Repatriation as an FX Catalyst

**What it is:** A distinct flow-mechanics channel from 5.1's fix-anchor and 5.2's CCF gauge: Asian exporters (Taiwan, Malaysia, Thailand, the Philippines) accumulated large USD deposit stocks during the Dollar-strength years, drawn by the rate differential; a Dollar-bearish, rate-cutting regime reverses that incentive, and the resulting conversion back to local currency becomes a self-standing catalyst for Asia FX strength independent of the CNY anchor or any single country's growth story.

**How Goldman Sachs applied it:**
- **2 May 2025 ("Waiting on the World to Change"):** the mechanism introduced with concrete stock data and a live example — "one of the key catalysts for a move lower in USD/Asia could be a repatriation of Dollar earnings, with exporters selling USDs... The largest increases in foreign currency deposits over the past 10 years were in Taiwan (up by USD 150bn or 115%) and Malaysia (up by USD 22bn or 111%). Hence, we believe TWD and MYR could benefit the most from FX conversion from foreign into local currency" — cited alongside a real-world data point, a >4% one-day TWD move ("equivalent to multiple standard deviations") attributed partly to this channel.
- **9 May 2025 ("Big Deal"):** extended into the cross-sectional EM-FX stock-picking rubric (see 6.1/6.2's updated four-part criteria) as one of four named selection factors — "where conversion of USD deposits can have large flow impacts" — applied across TWD, KRW, MYR, THB, IDR, INR.

## 5.5 Asia Idiosyncratic Political-Risk Case Studies (watch — one instance so far)

**What it is:** A candidate new sub-cluster, not yet confirmed as recurring: a country-specific political-crisis narrative driving one Asia currency's underperformance relative to its regional peers, independent of the CNY-anchor framework that otherwise dominates cluster 5. If this pattern recurs for other countries, it would parallel Brazil's dedicated cluster (7) and CAD/MXN's (8) as a single-country case study, but on current evidence (one issue) it is filed here as a sub-cluster rather than spun out on its own.

**How Goldman Sachs applied it:**
- **20 Jun 2025 ("Seven-Double-Oh, Look Out Below"):** Thailand's ruling coalition partner (Bhumjaithai) withdrew on 18 June, leaving Pheu Thai a thin 254/500-seat majority and pressure building on PM Paetongtarn Shinawatra to resign, against a Bank of Thailand judged likely to hold rates in a "wait and see" stance — "It has been a tumultuous week in Thai politics, which underpinned the Baht's underperformance versus NJA FX peers," expressed via a maintained short THB/KRW trade recommendation (cross-reference 1.5).

---

# 6. EM FX: Carry, Valuation, and Cross-Sectional Differentiation

## 6.1 Carry as the Key Differentiator Under "Dollar Stronger for Longer"

**What it is:** In a regime of persistent broad Dollar strength, GS argues *relative* performance within EM is better explained by carry (a Dollar-neutral, cross-sectional factor) than by directional Dollar calls — the core organizing idea for GS's entire EM FX section across the pilot window.

**How Goldman Sachs applied it:**
- **10 Jan 2025 ("More Bang for the Buck"):** "we think that in a world where the Dollar is 'stronger for longer' carry can be a key driver of relative performance... positive carry strategies that are Dollar-neutral can be resilient to tariff risk and yield positive total returns."
- **16 May 2025 ("Some Things Change, Some Stay The Same"), regime flip and canonical rubric:** with the Dollar now bearish rather than "stronger for longer," GS pivots the whole EM section from carry-neutral relative-value pairs (like the BRL/MXN trade, cross-reference 7.5) to **outright carry longs**, closing BRL/MXN for +1.4% (1.5) and giving the clearest four-part EM-FX selection rubric in the sample: "we think that the EM currencies that can benefit the most in this environment are those (i) with a larger undervaluation signal, (ii) with a positive beta to CNY and to risk more broadly, (iii) where conversion of USD deposits can have large flow impacts, and (iv) where carry contributes positively to total returns. We think BRL, ZAR, KRW and MYR are among the currencies that fit most of these criteria" — worth treating as the canonical statement of this whole cluster's logic going forward, superseding the looser "carry as differentiator" framing from January.
- **6 Jun 2025 ("Sliding into Summer"), the rubric operationalized into basket construction:** EM carry longs recommended "to be expressed outright versus the Dollar" (not as RV baskets), with BRL as top pick, diversified via MXN/INR/ZAR, and COP explicitly excluded ("higher sensitivity to oil prices makes COP a less attractive long"); funder selection also revisited given EUR's emerging safe-haven behavior (see new 9.5) — "shifting correlations... argue for [EUR being]... a less attractive funder than in the past," pointing instead to CNH/KRW, or to CLP/ILS/AUD/NZD specifically for risk-neutralizing (see 6.4 below).

## 6.2 Value + Carry Combined: Why LatAm Was Preferred Over Asia

**What it is:** A refinement of 6.1 adding a valuation layer — LatAm high-carry currencies were judged to already embed a large risk premium after 2024 underperformance, so the combination of cheap valuation + rising carry favored LatAm over Asia, where carry is a headwind for low-yielders even with Fed cuts, and where a high-yield/low-yield bifurcation produces a further relative-value trade within the region.

**How Goldman Sachs applied it:**
- **10 Jan 2025:** "LatAm high carry currencies enter 2025 embedding significant risk premium after their 2024 underperformance. This combination of value and carry means that these currencies should deliver positive total returns in 2025... and outperform those in Asia." Explicit follow-through trade: "long INR versus our Asia low-yielders basket."
- **By 16 May 2025, superseded rather than contradicted:** once the Dollar itself turned bearish, the LatAm-vs-Asia regional framing gave way to the cross-regional four-part rubric in 6.1 (undervaluation, CNY/risk beta, deposit-conversion potential, carry) — BRL, ZAR, KRW and MYR span both regions, showing the regional lens was a special case of the broader rubric under "Dollar stronger for longer," not a standing regional preference.

## 6.3 EM Equity Relative-Performance as an FX Cushion

**What it is:** A quantified empirical regularity: when US and EM equities sell off together, EM FX losses are meaningfully smaller when EM equities *outperform* the S&P 500 within that selloff than when EM underperforms — relative equity performance, not the level of the selloff, determines the FX damage. Two named exceptions (MXN, ILS) are carved out where US equity returns matter more than EM equity returns.

**How Goldman Sachs applied it:**
- **4 Apr 2025 ("From Diminished to Finished"), post-Liberation Day:** "when both US and EM equity indices are selling off, EM equity outperformance has tended to cushion EM FX from the fall in the S&P 500 to a significant extent... we consistently find that US equity returns screen as more important than EM equity returns for MXN and ILS and therefore think there is less scope for EM growth pricing resilience to support these currencies" — used to justify a relative preference for BRL within LatAm ("high carry and limited tariff exposure can cushion the Real") over a more cautious ZAR stance.

## 6.4 Orthogonality to Global Factors: The Frontier FX Carry Basket

**What it is:** Frontier currencies (EGP, KES, NGN, TRY) selected into a carry basket specifically because their correlation with global risk factors (DXY, VIX) is measured as lower than mainstream high-yield EM FX (BRL/COP/MXN/ZAR) — meaning the carry captured is diversifying and idiosyncratic rather than a levered bet on global risk appetite, which matters in a period of ongoing tariff/policy volatility. This logic generalizes beyond literal "frontier" currencies: the same low-correlation-without-giving-up-carry criterion is later applied to mainstream currencies (CLP, ILS, AUD, NZD) selected purely as *funders*, not as the carry-basket's long legs.

**How Goldman Sachs applied it:**
- **14 Feb 2025 ("War and Peace"):** "we recently initiated a trade recommendation to go long an equally weighted basket of Frontier currencies including EGP, KES, NGN and TRY, which has a 12-month nominal carry of ~18%... We view this trade recommendation mostly as a carry trade that can accrue returns without requiring material spot appreciation." KZT was explicitly excluded despite ruble-correlation-driven appreciation potential, on grounds of low real rates and unattractive GSDEER valuation — a reminder that the basket's selection criteria (orthogonality + valuation + real yield) are applied jointly, not just on carry alone.
- **6 Jun 2025 ("Sliding into Summer"), the same orthogonality criterion applied to funder selection instead of the long leg:** "other high-beta but low-carry currencies such as CLP, ILS, AUD and NZD can substantially lower the risk exposure of an EM carry basket without a significant reduction in carry" — CLP separately flagged as one of the most GSDEER-undervalued EM currencies (1.2), a valuation risk to using it as a funder ("this leaves long USD/CLP positions vulnerable to a sharp move lower," 13 Jun, "And So It Flows"), and ILS's low correlation attributed to a specific, named driver — its outsized sensitivity to US-specific (not EM-wide) growth pricing (cross-reference 4.4's safe-haven/high-beta clustering logic, reapplied here to ILS): "we have found ILS to be among the EM currencies most sensitive to US-specific growth pricing and a cross where the relative outperformance of EM growth does not have an offsetting impact... the Shekel could be an attractive low-yielding funder for more risk-neutral EM carry trades."

---

# 7. Brazil (BRL): A Case Study in Layered Frameworks

BRL receives the most sustained, multi-week treatment of any single EM currency in the pilot window, and illustrates how several of the frameworks above are combined for one country.

## 7.1 Testing Seasonality Against a Cyclical Fair-Value Model

**What it is:** GS explicitly tests two competing explanations for BRL's move — calendar/flow seasonality (derived from historical BCB FX-transaction data by month) vs. a cyclical fair-value model (country risk premium, terms of trade, US real yields, equity risk, CDS) — runs both, and reports that the cyclical model, not the calendar, does the explanatory work.

**How Goldman Sachs applied it:**
- **14 Feb 2025 ("War and Peace"):** "when modelling monthly seasonality more formally, we find a limited impact of monthly seasonality on BRL returns apart from a couple of months. Instead, our cyclical model based on other market variables tracks BRL returns since mid-December relatively closely and suggests that moves in country-specific risk premium and terms of trade have been the key drivers" — with a persistent ~10% BRL underperformance gap versus the cyclical model dating to April 2024.

## 7.2 Fiscal-Anchor Dependency Backstopped by BCB Intervention and Carry

**What it is:** GS frames BRL's near-term resilience as resting on two supports that can substitute for a genuine fiscal anchor in the near term — elevated real-rate carry compensating for fiscal risk, and active BCB FX intervention capping USD/BRL upside — while being explicit that a durable resolution of "fiscal dominance" fears still requires a real fiscal anchor that hasn't arrived.

**How Goldman Sachs applied it:**
- **10 Jan 2025 ("More Bang for the Buck"):** "While a clear fiscal anchor is needed for fears of 'fiscal dominance' in the currency to subside... for now, we think the BCB's actions can still guard against a sustained move higher in USD/BRL from current levels and support total returns through elevated carry in a period of limited fiscal news."
- **17 Jan 2025 ("Day One Deliberations"):** the same framework reiterated with an explicit asset-class-rotation caveat: "A genuine growth slowdown is also a risk and that would mean that the risk-reward would become more attractive for rates receivers rather than BRL longs. But it feels early for that transition" — an example of GS treating "which asset class expresses this view best" as itself a live, revisable question (see also 7.3).

## 7.3 The Short EUR/BRL Trade Lifecycle

**What it is:** The most completely documented single trade in the pilot window (see 1.5 for the general framework); tracked here for its BRL-specific rationale evolution.

**How Goldman Sachs applied it:**
- **10 Jan 2025:** opened on Brazilian real-rate carry ("continues to be a tailwind for the Real through the carry component and by guarding against significant depreciation moves").
- **17 Jan 2025:** stop tightened to 100.5 explicitly ahead of a binary US policy risk window, framed as pure risk management, not thesis change.
- **31 Jan 2025:** target/stop reset to 108/103 as the trade approached target, alongside an explicit political-economy tailwind (see 7.4).
- **28 Feb 2025:** closed for ~6-7% total return, explicitly on rising *tactical* fiscal-noise risk (2025 budget debate, income-tax exemption proposal, falling presidential approval reducing follow-through on spending cuts) while the medium-term constructive view was reaffirmed unchanged.

## 7.4 Political-Economy Overlay: Presidential Support for the BCB

**What it is:** A discrete input layered onto the carry/fiscal framework above: presidential public support for the central bank's hiking cycle is read as removing a historically important risk factor (a president publicly undermining BCB credibility/independence, as had weighed on BRL in prior cycles).

**How Goldman Sachs applied it:**
- **31 Jan 2025 ("Tariff-fied"):** "President Lula's comments after the rate decision imply there is policy support for the BCB's actions, in contrast to last year" — cited alongside the 100bp hike itself as a joint reason the carry trade remained attractive.

---

# 8. North America: CAD and MXN Under Tariff Threat

## 8.1 Options-Implied Tariff Probability vs. Economists' Probability

Documented in full under 1.4; the CAD/MXN pair is where this instrument is used most extensively and comparatively across the pilot window (3 Jan, 17 Jan, 28 Feb, 7 Feb issues).

## 8.2 Commodity-Leverage Retaliation as a Ceiling on Tariff Severity (CAD)

**What it is:** A structural, country-specific mechanism: Canada's position as a supplier of hard-to-substitute commodities (oil, uranium, potash) to the US gives it retaliatory leverage via export taxes, which raises the effective US inflation/cost risk of imposing the full threatened tariff — making the worst-case (25%) scenario an inflation-constrained, and therefore less likely, outcome.

**How Goldman Sachs applied it:**
- **3 Jan 2025 ("Tariff Special"):** ">60% of US oil imports from Canada; US Midwest refining specifically configured for heavy Canadian crude; Canada largest foreign uranium supplier to US nuclear plants; Russia/China are the only larger potash producers... Export taxes would force the US to pay up for essential energy and fertilizer supplies... This is the main reason we think a 25% tariff is ultimately unlikely, but brinksmanship and prolonged negotiations could keep tariff risks on the table for some time."

## 8.3 "Tariff Pre-Adjustment Already in Spot" (MXN)

**What it is:** A pure interest-rate-parity-style valuation argument: if in theory a 25% tariff could be exactly offset by a 25% currency depreciation, a currency that has already depreciated materially since a reference date has already "pre-paid" much of that adjustment, reducing the incremental FX move needed if the tariff materializes — reinforced by supply-chain-integration evidence (two-way trade flows across most major categories) suggesting both sides have strong incentives to avoid the worst outcome.

**How Goldman Sachs applied it:**
- **3 Jan 2025 ("Tariff Special"):** "if theoretically a 25% tariff could be fully offset by a 25% depreciation in the exchange rate, the depreciation since May 2024 already goes a long way in contributing to that adjustment."
- **24 Jan 2025 ("A Brief Relief"):** the same logic extended into an explicit list of resilience factors for the Peso even amid a hawkish tariff threat ("I expected to impose the proposed 25% tariff on February 1"): past unfulfilled threats during the first Trump administration, high supply-chain integration making a 25% tariff "highly disruptive to corporates on both sides of the border," and the pre-existing risk premium already embedded in spot and carry — concluding "it will continue to be difficult to fully price any tariff proposal ahead of time in MXN."
- **7 Feb 2025 ("From Tariff-fied to Tariff-fried"):** the range-bound implication drawn out explicitly into a carry-accrual reframing: "A range-bound USD/MXN makes MXN longs attractive from a carry accrual perspective," contrasted with Brazil's hiking-cycle-reinforced carry case (7.2) since Banxico was cutting, not hiking.

## 8.4 Relative Political-Institutional Risk Premium: Why CAD Priced Worse Than MXN

**What it is:** Even facing the same weekend tariff threat, GS argues Canada's domestic political fragility (a prorogued parliament, upcoming election, leadership transition) makes a durable US-Canada resolution less certain than the equivalent Mexican process, justifying a higher and more persistent tariff-premium assumption for CAD than for MXN — the basis for the CAD/MXN relative-value trade (see 1.4/1.5).

**How Goldman Sachs applied it:**
- **7 Feb 2025 ("From Tariff-fied to Tariff-fried"):** "Canada's parliamentary stand-still, upcoming election, and political transition make a longer-term resolution with the US less certain than with Mexico. We think these risks mean that markets need to price a higher and more lasting tariff premium in USD/CAD" — paired with a vol-adjusted short CAD/MXN recommendation.
- **17 Jan 2025 ("Day One Deliberations"):** a companion mechanism specific to Canada's policy paralysis — detailed parliamentary-procedure mapping (prorogation rules, confidence-vote mechanics) used to derive the probable window during which Canada could not formally respond to US tariff rhetoric, treated as an FX-relevant variable (capacity to respond) distinct from the tariff probability itself.
- **14 Mar 2025 ("Less Bang for the Buck"):** a further structural override specific to CAD — even under the general "weaker Dollar via diminished exceptionalism" thesis, CAD was singled out as the one G10 currency least likely to benefit, because Canadian and US growth are so tightly linked: "CAD tends to be vulnerable to weaker US growth pricing... CAD showed the least upside versus the Dollar last week out of the G10." Preferred expression given this override: short CAD vs. MXN, and long EUR/CAD.

---

# 9. Europe: Fiscal Regime Shift, CEE/Scandi Crosses, and Sterling

## 9.1 The German Fiscal Package and the "Unstable Equilibrium" Framing for EUR

**What it is:** Following Germany's March 2025 fiscal-expansion announcement (loosening the "Schwarze Null"/debt-brake orthodoxy), GS frames the resulting EUR/USD level as an "unstable equilibrium" that could resolve toward either extreme — stronger if fiscal delivery and growth optimism build further, weaker if implementation disappoints (with an explicit historical-analogy discount drawn from the EU's prior NGEU recovery-fund rollout, where initial optimism gave way to serial deployment disappointment) or if the Dollar side of the "balance of opposing forces" (3.2) reasserts.

**How Goldman Sachs applied it:**
- **7 Mar 2025 ("Schwarze Null No More"):** "it is possible the 'unstable equilibrium' we have described is resolving itself in the opposite direction of our current baseline" — flagged as a genuine two-sided risk to the still-standing Dollar-strength baseline, not a directional call in itself. The NGEU discount applied explicitly: "we are reminded of the discussion around the NGEU funds where there was initial optimism followed by serial disappointments on implementation and activity outcomes."
- **14 Mar 2025 ("Less Bang for the Buck"):** the valuation side of the same debate — EUR shown as roughly fair (even slightly overvalued) on a trade-weighted basis but undervalued bilaterally against the Dollar, redirecting the analytical burden onto the Dollar leg (see 1.2), with the 2017 flow-reversal analogy invoked as the explicit playbook for how the gap could close: "There is a clear playbook for this scenario, as it also played out in 2017... the currency rose from about 1.05 to 1.25 over the course of a year, which closed the valuation gap... We rarely use valuation as the primary metric for sizing cyclical trading views, but it makes sense in this case when a possible change in the underlying cause for that valuation gap is central to the thesis."
- **21 Mar 2025 ("Rhetoric vs Returns"):** the 2017 analogy immediately stress-tested (see 1.3) and found only partially applicable given the still-wide US-EA growth gap.

## 9.2 CEE as High-Beta Euro Satellites — With Sector-Specific Exceptions

**What it is:** CZK, HUF, and PLN are modeled as high-beta amplifiers of the Euro-area growth cycle — particularly strong when the shock is common to both the Euro area and CEE together (vs. idiosyncratic domestic shocks) — because of CEE's outsized manufacturing/auto exposure to the EU auto sector. GS then tests this beta assumption issue by issue against actual realized moves, sometimes finding the pass-through more muted than the historical beta would imply (evidence of a rates-led, not growth-led, move — see 1.1), and layers a sector-specific auto-tariff exposure screen on top that can override the general Euro-beta framework.

**How Goldman Sachs applied it:**
- **3 Jan 2025 ("Tariff Special"):** the base beta claim — "CEE currencies respond strongly to shifts in the relative activity outlook between Europe and the US and more so than the other Euro satellites. And, it is when the Euro Area and CEE economies face common growth shocks that the Euro 'beta' of CEE FX is the most prominent."
- **7 Mar 2025 ("Schwarze Null No More"):** the beta explicitly tested against the week's +4.6% EUR/USD move and found muted in EUR/CE3 crosses — "This more subdued CE3 FX performance would be consistent with a rates-led rather than a growth-led European re-rating" — used to justify maintaining a short CZK/HUF vs. EUR position rather than treating the German fiscal news as broadly CEE-positive.
- **28 Feb 2025 ("Accord and Discord") and 28 Mar 2025 ("Drawbacks of the Clawbacks"):** the sector-specific override — Czech/Hungarian GDP's outsized exposure to global auto exports (~15% and ~13% of GDP respectively, vs. Mexico's ~8%) used to argue the YTD CE3 rally had priced growth optimism but left auto-tariff downside risk unpriced, an asymmetry GS traded directly: "we think current spot levels in CEE FX... do not reflect these growth and tariff risks. Therefore, we initiate a new trade recommendation to be short CZK and HUF versus EUR." (Closed post-Liberation Day for ~0.6%, see 1.5.)

## 9.3 "Euro-Squared": SEK's Amplified Beta and the Defense-Spending Sector Channel

**What it is:** SEK is characterized as "Euro-squared" — an amplified-beta version of EUR's sensitivity to EA growth surprises, in either direction. Layered on top is a distinct sector-composition argument: Sweden's stock market has an unusually large industrial-sector weight (~34% of market cap vs. ~8% for the US), so a specific fiscal catalyst (coordinated European defense spending) can disproportionately benefit NOK/SEK independent of the general Euro-beta story, transmitted in part via measurable portfolio-fund-flow data.

**How Goldman Sachs applied it:**
- **28 Mar 2025 ("Drawbacks of the Clawbacks"):** "While the European satellites should be exposed to a tariff induced hit to EA growth, particularly SEK which has historically operated like 'Euro-squared,' we see room for continued outperformance vs EUR if Europe's response to tariffs is more coordinated defense spending which should disproportionately benefit the Scandis given their outsized concentration in the industrial sector."
- **14 Mar 2025 ("Less Bang for the Buck"):** the flow-based mechanism made concrete — a GSBEER-model divergence (SEK "outperforming its typical betas... and we think this looks overdone") explained by directly observed Swedish vs. North American equity-fund flow data rather than left as an unexplained residual: "Swedish funds recorded net inflows of 22.7 SEK bn, North American funds recorded net outflows of 13.7 SEK bn," with a rising rolling correlation between 3-month Swedish fund flows and USD/SEK cited as corroborating evidence.
- **11 Apr 2025 ("Dollar Wreckoning"):** the same Swedish fund-flow dataset revisited post-Liberation Day showing a "record rotation" out of North American and into European equity funds over the prior two months — used to argue the broader cross-border flow-rotation thesis (2.5/3.5) was becoming visible in hard data, not just narrative, while noting the accumulated *stock* of US-asset overweight built up over the past decade had "barely moved" yet.

## 9.4 Sterling: Decomposing Global vs. Domestic Drivers, and Discounting Noisy Data

**What it is:** GS repeatedly separates GBP's weekly move into a global component (risk sentiment, global yields, correlation to tariff-sensitive Dollar pairs) and a domestic component (UK fiscal risk, growth/inflation surprises) — explicitly tracking which factor is dominant *this specific week*, since the answer changes the correct response (fade vs. chase). A companion framework discounts the reliability of UK domestic data releases themselves when they're judged to be distorted by known measurement quirks.

**How Goldman Sachs applied it:**
- **10 Jan 2025 ("More Bang for the Buck"):** the fiscal-risk-premium signature identified via a specific co-movement diagnostic — currency weakness paired with long-end yield bear-steepening, also seen contemporaneously in CAD and EUR — read as the marker of an acute fiscal-risk (not generic risk-off) episode: "the bear steepening and underperformance in UK gilts alongside the currency sell-off characteristic of an acute rise in UK fiscal risk premia."
- **17 Jan 2025 ("Day One Deliberations"):** the driver-rotation diagnostic applied explicitly — "the source of weakness shifting from a widening fiscal risk premium on rising global yields last week, to downside surprises on the domestic growth and inflation data this week" — alongside the data-discount framework: "Inflation missed sharply, but was largely driven by a decline in the volatile airfares component. Meanwhile, wages surprised to the upside, but are likely being distorted by compositional effects."
- **31 Jan 2025 ("Tariff-fied"):** the global-attribution thesis reasserted for GBP's two-thirds recovery of its trade-weighted losses: "Just as global factors drove the initial Sterling weakness, so also the key contributors to that reversal of fortunes have been more global factors than domestic ones."
- **28 Mar 2025 / 11 Apr 2025:** the global-attribution thesis operationalized as a testable correlation — EUR/GBP's realized correlation with tariff-sensitive Dollar pairs (USD/CAD, USD/MXN) tracked explicitly, its year-to-date decline read as evidence GBP was decoupling from the broad tariff trade; and, post-Liberation Day, a formal GSBEER-style regression fit for EUR/GBP showing the pair had rallied *beyond* what even the richer factor model implied — a stronger, quantified version of the same "is this move justified" check applied throughout the document (see 1.1).

---

## Notes for the next processing pass

A few observations worth carrying forward when the remaining ~64 issues (mid-April 2025 – July 2026) are processed:

- **The toolkit (Cluster 1) is the highest-value/lowest-redundancy material.** Nearly every week reapplies the same 5-6 named instruments to a new currency; future extraction batches should flag *new* instruments as they appear (e.g. anything analogous to the VIX-bucket regression in 4.2) rather than re-deriving the ones already documented here.
- **The tariff-transmission thesis (Cluster 2) is clearly still evolving past this pilot's endpoint.** The "exceptionalism erosion" reversal (2.5) is dated 4 April 2025; by the time the series reaches mid-2026 (per titles like "A Window Into Debasement," "Currencies in Conflict," "The Gulf Between" — likely covering an Iran/Hormuz-related oil shock, consistent with the Kapitalo/Verde/Kinea documents' coverage of the same episode around March-April 2026) the framework will likely have moved through further stages worth documenting as their own cluster or sub-cluster.
- **Trade-recommendation lifecycles (1.5) are worth tracking as a dedicated index** (open date, adjustments, close date, realized return) as more issues are added — this is a distinctive, quantifiable feature of the GS source that the manager letters don't offer in the same form.
- This document was built independently from the three existing manager documents, without cross-referencing them for consistency of theme or terminology — as with those three, any eventual comparison across houses should be a separate, explicit exercise.
