# Exchange Rate Forecasting: Theory vs. Practice

*LIS Capital — Macro Research Note*

How well do PPP, UIP, and the other canonical FX models survive contact with the data — and what do banks, central banks, and quants actually use instead? Two questions, one synthesis, USD/BRL called out throughout.

*Research compiled 2026-07-16 · companion to exchange_rate_conceptual_map.md · not a bibliography acquisition*

---

## Scope

**Part I** asks how well the canonical theoretical models of exchange rate determination hold up empirically, drawing on general EM/DM evidence with USD/BRL called out wherever direct studies exist. **Part II** asks what actually gets used to forecast FX in practice — academic forecast-accuracy literature, institutional/practitioner methodology, and quant/systematic/ML approaches.

*All citations verified to exist via web search at research time, not recalled from memory. Two-agent research pass — see confidence note in chat, not adversarially cross-verified.*

---

## Part I — Empirical Adherence of Exchange Rate Determination Theories

Five models, one question each: does the theory's prediction actually show up in the data?

### 1 · Purchasing Power Parity — *Holds only slowly*

*Prediction: Absolute PPP: a currency's exchange rate should equal the ratio of price levels. Relative PPP: the change in the exchange rate should track the inflation differential, keeping the real rate constant.*

*Note: relative PPP and BEER (behavioral equilibrium exchange rate) are related, not equivalent — both need an assumed "correctly valued" base period to anchor the comparison, but relative PPP anchors purely on relative price levels, while BEER anchors on a wider set of fundamentals (terms of trade, productivity, net foreign assets) estimated via cointegration. BEER generalizes the PPP logic rather than restating it.*

**Absolute PPP is rejected essentially everywhere** — goods heterogeneity, non-tradables, trade costs, and capital flows (not goods arbitrage) dominating short-run turnover mean price levels diverge persistently.

**Relative PPP shows real, but glacially slow, mean reversion.** Rogoff (1996), *"The Purchasing Power Parity Puzzle"* (JEL), found a **3–5 year half-life** for PPP deviations (~13–20%/year reversion) across long-horizon studies — far too slow for nominal price stickiness alone to explain, and inconsistent with how volatile real exchange rates are month to month. That mismatch *is* the puzzle. [Rogoff 1996 ↗](https://www.uh.edu/~cmurray/papers/The%20PPP%20Puzzle%20is%20Worse%20Than%20You%20Think.pdf)

**Frankel & Rose (1996)**, 150 countries × 45 annual observations, independently found deviations erode at **~15%/year, ~4-year half-life** — corroborating the time-series consensus with panel data. [SSRN ↗](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=225785)

Follow-on literature argues the puzzle is **even worse than Rogoff's framing** once sampling/specification biases are corrected. [ResearchGate ↗](https://www.researchgate.net/publication/24055083_The_Purchasing_Power_Parity_Puzzle_Is_Worse_Than_You_Think)

> **USD/BRL evidence.** Mixed and version-dependent. A BRICS nonlinear-stationarity study (1993–2015) found the real exchange rate stationary — PPP holding — for **Brazil and South Africa** but not Russia, India, China. Other Brazil-specific work confirms **only relative PPP**, rejecting the absolute version, surviving structural-break tests. [PEP VŠE ↗](https://pep.vse.cz/pdfs/pep/2018/04/03.pdf)

### 2 · Uncovered Interest Rate Parity — *Fails, regime-dependent*

*Prediction: The interest-rate differential between two currencies should equal the expected depreciation of the higher-yielding one — no arbitrage profit from just holding the high-rate currency.*

**Fama (1984)** found the regression slope of spot changes on the forward premium **reliably negative** across nine major currencies — a forward premium predicts further appreciation, the opposite of UIP's sign. His deeper point: **most forward-premium variance is risk-premium variance**, not genuinely expected depreciation. Engel (1996) calls the joint UIP + rational-expectations failure **"one of the most robust empirical regularities"** in international finance. [NYU Stern ↗](https://pages.stern.nyu.edu/~rwhitela/papers/FwdPremPuzz_2013_06_12.pdf)

**The puzzle is not universal.** Bansal & Dahlquist (2000) found it concentrated in **high-income countries when US rates exceed foreign rates** — **UIP works better in emerging markets than developed ones.** Bussière, Chinn, Ferrara & Heipertz's *"New Fama Puzzle"* (NBER 2018) show the coefficient flips positive in the post-crisis near-zero-rate decade, and using **survey-based expectations instead of realized rates gives much stronger UIP support**. [NBER ↗](https://www.nber.org/system/files/working_papers/w24342/w24342.pdf)

> **USD/BRL evidence.** Araújo et al. (SciELO, 2000–2014, inflation-targeting era) confirm UIP failure with a GARCH coefficient of **‑2.94** — wrong sign vs. UIP's β=1. A Markov-switching extension finds regime dependence: **‑2.94** in low-volatility months, flipping **>+1.00** in high-volatility ones — the same sign-flip pattern as the global "New Fama Puzzle." [SciELO ↗](http://www.scielo.br/j/ecos/a/kcqb5xFhHPBnGPqYQHtdHKc/?lang=pt)

### 3 · Monetary / Asset Models — *Fails out-of-sample*

*Prediction: The exchange rate is priced as an asset, driven by relative money supply, income, and rate expectations. Dornbusch's sticky-price version says the rate must overshoot on impact, then partially reverse as goods prices catch up.*

**Meese & Rogoff (1983)** tested flexible-price monetary, sticky-price monetary, and portfolio-balance-augmented models on 1973–1981 USD data. **None beat a naive random walk** out-of-sample, at any horizon — even given the unfair advantage of realized future fundamentals. Never decisively overturned in its original MSE form. [ResearchGate ↗](https://www.researchgate.net/publication/304879268_The_Meese-Rogoff_Puzzle)

Cheung, Chinn & Garcia Pascual (2005) reran the horse race on the 1990s: **still no model consistently beats the random walk on MSE.** Obstfeld & Rogoff (2000) formalized the gap as the **"exchange rate disconnect puzzle"** — rates are far more volatile than, and disconnected from, the fundamentals that should drive them.

> **USD/BRL evidence.** No dedicated Meese-Rogoff-style BRL horse race surfaced. The BEER/GSDEER-style valuation tools already in the bibliography are the closest local analogue — multi-year convergence tools, not short-horizon forecasts, which is consistent with (not a contradiction of) random-walk dominance.

### 4 · Current Account / Balance of Payments — *Holds, weakly*

*Prediction: A current-account deficit needs a weaker real exchange rate to correct itself; persistent deficits/surpluses should predict depreciation/appreciation.*

Rogoff & Kuttner-adjacent estimates put the effect at roughly **0.7–1.0%** depreciation per **1pp** rise in the CA-deficit-to-GDP ratio. Obstfeld & Rogoff (2005) treat CA imbalances as a first-order factor in 50 years of USD movement — but the link is low-frequency, regime-dependent, and causality runs both ways (J-curve dynamics). [Berkeley PDF ↗](https://eml.berkeley.edu/~obstfeld/global_current.pdf)

> **USD/BRL evidence — strongest of all five models.** Not via the textbook CA-deficit channel, but via **terms-of-trade/commodities**: Souza, Mattos & de Lima (2021, IJFE) find a **robust relationship between world commodity prices and the BRL real exchange rate** under the floating-rate regime, with strength depending on trade openness (long run) and country risk (short run). [Wiley ↗](https://onlinelibrary.wiley.com/doi/abs/10.1002/ijfe.1955)

### 5 · Portfolio Balance — *Weak in DM, relevant in EM*

*Prediction: Domestic and foreign bonds are imperfect substitutes; the exchange rate equilibrates portfolios given the relative supply of each — distinct from UIP's perfect-substitutability assumption.*

Classic sterilized-intervention tests find effects that are real but small (~0.05% spot move per 1% change in cumulated current account) in DM contexts. **EM is where the model earns its keep**: sterilized intervention is argued most effective in developing countries, where imperfect substitutability is a far better assumption. [Princeton ↗](https://ies.princeton.edu/pdf/SP18.pdf)

Its modern reincarnation — **Evans & Lyons' (2002) order-flow model** — replaces asset-supply shocks with demand-side heterogeneity via signed order flow, and explains **R² above 50–60%** of daily FX changes: far outperforming the fundamentals models that failed Meese-Rogoff. [Georgetown PDF ↗](https://faculty.georgetown.edu/evansm1/wpapers_files/orderflow.pdf)

> **USD/BRL evidence.** No classical bond-supply-shock test found for BRL directly. The closest local analogue is the BCB's own *posição de câmbio*/FX-swap toolkit (2019: selling spot while repurchasing swaps to cushion the banking system's short FX position) — an applied instance of the same mechanism.

### 6 · The Scapegoat Theory — *why the fundamental-FX relationship keeps flipping*

*Not a sixth determination model — a theory of why any of the five above can dominate at one moment and go quiet the next.*

**Bacchetta & van Wincoop (2004)**, *"A Scapegoat Model of Exchange-Rate Fluctuations"* (NBER WP 10245 / AER Papers & Proceedings), argue that under **parameter uncertainty**, market participants don't hold fixed weights on fundamentals. When the exchange rate moves in a way the "usual" driver can't explain, they rationally revise which fundamental currently matters most — attaching extra weight to whichever one had an unusually large realization at that moment, even though the true structural relationship between fundamentals and the rate hasn't changed. That fundamental becomes the market's temporary "scapegoat." Their follow-up, **Bacchetta & van Wincoop (2009 NBER WP 15008; published *Journal of International Economics*, 2013)**, *"On the Unstable Relationship between Exchange Rates and Macroeconomic Fundamentals,"* formalizes why this produces **large, frequent swings in the estimated exchange-rate/fundamentals relationship** — instability generated by rational updating of *expectations about parameters investors can't observe directly*, not by the underlying structural parameters themselves changing.

**Fratzscher (2011)**, *"The Scapegoat Theory of Exchange Rates: The First Tests,"* ran the first direct empirical test on daily G10 rates and found supportive evidence: the fundamental that "explains" a given episode of currency moves changes over time in a way consistent with scapegoat switching rather than a fixed-weight model.

This gives the time-varying-driver pattern already documented throughout Part I — UIP's Markov-switching sign flip, the terms-of-trade channel's strength depending on country risk, carry's regime-dependence — a candidate *mechanism* for *why* it happens, distinct from (but compatible with) the purely statistical time-varying-parameter/model-averaging literature also in `referencia/er_forecasting/` (Hauzenberger & Huber, 2019; Beckmann & Schüssler, 2015), which detects *that* weights shift without committing to a causal story for why.

> **Practical read.** If USD/BRL looks like it's "trading off" interest differentials most of the time and then abruptly starts trading off fiscal deterioration instead, scapegoat theory says this need not mean the market's underlying model of BRL changed — it can simply mean fiscal news became the most *informative* (least explained-away) signal available, and the market rationally shifted its attention there. The practical implication: don't read a shift in the apparent dominant driver as proof of a regime change in the *true* price-formation model — check whether it's better explained as a scapegoat switch first.

### Part I takeaway — for USD/BRL forecasting

None of these five models works as a stand-alone, mechanical short-horizon signal — Meese-Rogoff's verdict, replicated for decades, still stands, and BRL's own UIP tests show the same regime-flipping instability seen globally. The literature earns its keep at the two extremes: relative PPP and BEER/GSDEER-style tools as slow (~3–5 year) valuation anchors, and terms-of-trade/commodity prices as the one channel with real, direct BRL support — weight that above textbook CA-deficit or UIP reasoning for medium-term calls. Carry is real on average but regime-dependent — condition it on the volatility regime, don't treat it as constant.

---

## Part II — Forecasting Models Used in Practice

Three lenses: what the academic accuracy literature finds, how institutions actually build forecasts, and what systematic/ML strategies show in their track record.

### (a) Academic literature on forecast accuracy

**Meese & Rogoff (1983)** established the canonical result: structural exchange-rate models can't outperform a random walk out-of-sample at 1–12 month horizons, even given realized future values of their own explanatory variables. [Springer ↗](https://link.springer.com/chapter/10.1057/9781137452481_1)

#### Has anything reliably beaten it since?

Forty-plus years on: **not reliably, and not on MSE; occasionally yes on direction-of-change or at longer horizons, fragile to sample and data vintage.** Mark (1995, AER) found long-horizon predictability for DM and Yen — but Kilian (1999) showed it didn't survive a longer sample, and later work traced the favorable result to a narrow data-vintage window. Cheung, Chinn, Garcia Pascual & Zhang (2017, NBER WP 23267), with an expanded model set (Taylor-rule fundamentals, yield-curve factors, shadow rates, BEER models) across 1/4/20-quarter horizons: **"No model consistently outperforms a random walk, by a mean-squared-error measure."** Winning model/currency pairs don't repeat across periods. Rossi's 2013 JEL survey sums it up: predictability "depends — on predictor, horizon, sample, model, evaluation method." [NBER ↗](https://www.nber.org/system/files/working_papers/w23267/w23267.pdf)

Engel & West's (2005, JPE) theoretical account explains *why*: if fundamentals are I(1) and the discount factor is near 1, the rational-expectations present-value solution is near-random-walk almost by construction — not an anomaly to solve, a mechanical consequence of discounting.

#### What do professional forecasters actually condition on?

Frankel & Froot: forecasters split into "fundamentalists" and "chartists" — **extrapolating recent trends at short horizons**, **forecasting mean-reversion at long horizons**. Eun & Sabherwal's (2002) bank-level study found a majority of banks show some RW-beating ability outside yen pairs, mostly behaving as momentum/"bandwagon" extrapolators, with **home-country banks forecasting their own currency better** (information asymmetry). [ScienceDirect ↗](https://www.sciencedirect.com/science/article/abs/pii/S1044028302000479)

### (b) Institutional / practitioner methodology

The **Boletim Focus / Sistema de Expectativas de Mercado (BCB)** surveys ~140 institutions weekly for USD/BRL, inflation, Selic, and more — reporting the **median**, specifically to reduce outlier influence. [BCB ↗](https://www3.bcb.gov.br/expectativas2/) BCB has itself published research questioning FX predictability with its own data — squarely in the Meese-Rogoff tradition, applied to BRL by the central bank itself.

**Consensus Economics** surveys 250+ forecasters across 90+ currencies at 1/3/12/24-month horizons, aggregating as a **mean** (contrast with BCB's median), with special surveys collecting scenario probabilities rather than just point forecasts. [Consensus Economics ↗](https://www.consensuseconomics.com/publications/foreign-exchange-consensus-forecasts/)

Practitioner process descriptions (CFA curriculum, bank methodology notes) combine relative-PPP/REER anchors for long-run fair value, rate-differential/carry logic for shorter horizons, BOP/flow analysis, and technical overlays — with judgmental overrides layered on for events no model captures. [CFA Institute ↗](https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/currency-exchange-rates-understanding-equilibrium-value)

**Bottom line —** no institution, public or private, claims a structural model reliably beats the random walk. The entire survey-aggregation infrastructure exists to combine heterogeneous *judgment*, not to certify one validated model.

### (c) Quant / systematic approaches

**Carry** has a long record — ~5.4%/year, Sharpe ≈ **0.57** (1996–2014) — but with well-documented, non-tail crash risk: Brunnermeier, Nagel & Pedersen (2009) show negatively skewed returns from funding-liquidity unwinds, with carry losing up to **~20%** of capital in 2008. A 200+ year extension finds carry surprisingly robust across two centuries. [Princeton ↗](https://markus.scholar.princeton.edu/sites/g/files/toruqf2651/files/carry_trades_currency_crashes.pdf)

**Momentum** (Menkhoff, Sarno, Schmeling & Schrimpf, 2012) generates up to **~10%/year**, strongest at ~1-month horizons, uncorrelated with standard risk factors or carry. **Value/PPP** (Asness, Moskowitz & Pedersen, 2013) shows a genuine modern-sample premium, but the 200-year dataset finds it flat-to-negative pre-1980 — the most fragile of the three to sample-period choice.

**Machine learning** evidence is not favorable to a durable edge: a 2026 arXiv study on CAD/USD found results "largely consistent with the canonical Meese-Rogoff puzzle" — only linear regression beat the random walk, and every ensemble ML model tested (Random Forest, Gradient Boosting, XGBoost, AdaBoost) failed to. A 2025 Fed FEDS paper on model complexity found only modest, localized gains from complexity — no broad complexity premium. [arXiv ↗](https://arxiv.org/abs/2606.15058)

**Bottom line —** carry is the deepest, most mechanistically understood factor: a real premium, compensation for real crash risk, not free. Momentum and value are real in the modern sample but less robust historically. ML has not been shown to reliably beat simple linear models or the random walk.

### Part II takeaway — for USD/BRL forecasting

Four decades of evidence say plainly: nobody — bank, central bank, or ML researcher — has found a model that reliably beats a random walk for short-horizon FX levels, and BRL gets no exemption; EM adds fiscal/political-risk and liquidity dimensions that make it harder, not easier. The practical implication is to treat the *process* as the deliverable: PPP/REER and terms-of-trade as slow valuation anchors, carry and cambial-flow/BOP data as the standard short-run building blocks (with explicit awareness of carry's crash risk), BCB Focus and sell-side consensus as a positioning signal rather than a validated forecast, and real skepticism toward any ML/complexity pitch for FX levels specifically.

---

## Overall Synthesis

Theory and practice converge from opposite directions on the same conclusion: the clean structural models don't survive contact with the data, and nobody forecasting for a living has found a durable way around that — which is exactly why a fundamentals/flows/positioning dashboard, not a single point forecast, is the right shape for this work.

---

*Compiled via two independent research agents (theory / practice), each with direct web search and citation extraction — not adversarially cross-verified between agents. Treat citations as "found in a credible source," verify anything load-bearing before acting on it.*
