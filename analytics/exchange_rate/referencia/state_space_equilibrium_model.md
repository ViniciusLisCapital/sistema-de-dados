# A State-Space Equilibrium Model for USD/BRL

*LIS Capital — Macro Research Note*

*Concept note, not yet implemented. Companion to `fx_forecasting_theory_vs_practice.md` and to the model-by-model work in `analytics/exchange_rate/models/` (`uip_model.py`, `carry_model.py`, and the planned `terms_of_trade_model.py` / `fiscal_credibility_model.py`). Written 2026-07-22, following chat discussion the same day.*

---

## Scope

Everything built in `models/` so far asks one question at a time: does *this* variable (an interest differential, a terms-of-trade shift, a fiscal-risk proxy) explain USD/BRL moves, on its own. This note describes a different, integrating question: **can the three be combined into one model where an unobserved "equilibrium" exchange rate drifts over time, and carry, the balance of goods, and fiscal credibility explain the gap between the actual rate and that equilibrium?**

This is deliberately scoped as a **later** step. It only makes sense once each of the three channels has been explored on its own — their individual signal-to-noise properties (already looking weak for carry, per `carry_model.py`'s results) are exactly the inputs a combined model needs, and are cheaper to learn about one at a time.

---

## The idea in plain terms

Instead of treating "fair value" as a single fixed number (e.g. a static PPP-implied rate), treat it as a **state variable** — something that exists, moves over time, but is never directly observed. What *is* observed is the actual exchange rate, which is the equilibrium plus a deviation. The deviation isn't random noise — it's pulled around by a small number of forces (carry, trade flows, fiscal risk), and it's pulled *back toward* the equilibrium over time, at some speed.

This is the standard structure behind an **equilibrium-correction model**, estimated here via a **Kalman filter** rather than a static regression, because a Kalman filter is exactly the tool for "there's a hidden state I can't observe directly, but I can write down how it evolves and how it relates to what I *can* observe."

---

## Theoretical grounding

This isn't a new idea — it's a variant of the **BEER (Behavioral Equilibrium Exchange Rate)** framework already flagged in `fx_forecasting_theory_vs_practice.md` Part I §1: *"BEER anchors on a wider set of fundamentals (terms of trade, productivity, net foreign assets) estimated via cointegration [...] BEER generalizes the PPP logic rather than restating it."* The Kalman-filter version of BEER simply makes the equilibrium an explicit unobserved state rather than a fitted cointegrating relationship — the same underlying idea (fundamentals-implied fair value, deviations that correct over time), a different estimation mechanism. Related lineage: **NATREX** models (Stein and successors) build the same "slow-moving fundamentals-driven equilibrium" idea directly into a state-space structure, which is closer in spirit to what's proposed here than a static cointegrating-vector BEER.

What the existing literature review already tells us about each candidate pull variable, directly relevant to how this model should be built:

- **Terms-of-trade/commodities is BRL's single strongest empirically-supported channel** of the five models surveyed (`fx_forecasting_theory_vs_practice.md` Part I §4, citing Souza, Mattos & de Lima 2021) — stronger justification for including it than the textbook current-account-deficit channel.
- **Carry (UIP) is real on average but regime-dependent**, not a stable constant relationship (Part I §2; Araújo et al.'s BRL-specific Markov-switching sign flip) — and this session's own `carry_model.py` results reproduce that same weak, sign-flipping-adjacent pattern directly (all four specs: negative β, p > 0.27, R² ≈ 0.002-0.004). Any pull term built from carry should expect to contribute *little* on its own, consistent with everything found so far, not a strong signal to lean on.
- **The Scapegoat Theory** (Part I §6, Bacchetta & van Wincoop) is a direct challenge to this whole approach if taken at face value: it argues the *relative importance* of each fundamental shifts over time based on which one currently has the most "unexplained" news in it, not because the true structural relationship changed. A state-space model with **fixed** loadings on carry/terms-of-trade/fiscal-risk would miss this entirely. The honest fix is a **time-varying-parameter** extension (the project's own `referencia/er_forecasting/` already holds directly relevant literature on this: Hauzenberger & Huber 2019, Beckmann & Schüssler 2015) — flagged here as a natural second iteration, not attempted in the first pass.
- **Nobody has found a model that reliably beats a random walk at short horizons** (Part II, Meese-Rogoff, replicated for BRL). This model should be framed as a **valuation/diagnostic tool** — "how far is BRL from where these fundamentals say it should be, and how fast does that gap tend to close" — not a short-horizon forecasting signal. That's the same honest framing the existing literature review already applies to BEER/GSDEER-style tools generally.

---

## Proposed model structure

Three equations. Two design choices below are flagged as open judgment calls, not settled facts.

### 1. Measurement equation
```
rer(t) = equilibrium(t) + deviation(t)
```
`rer` should be the **real** effective exchange rate, not nominal PTAX — `macro_international.cmb_reer` already exists in the database for exactly this purpose (BIS REER for Brazil), so this equation's observed side needs no new data collection.

>> Can we construct a absolute PPP equation as the equilibrium value? 

### 2. Transition equation (how the unobserved equilibrium moves)
```
equilibrium(t) = equilibrium(t-1) + gamma * terms_of_trade_shift(t) + eta(t)
```
**Open design question #1**: which of the three pull variables belongs *here* (permanently shifting fair value) vs. in the deviation equation (temporarily pulling the rate away from a fair value that hasn't itself moved)? Terms-of-trade is the strongest candidate for the transition equation — a persistent commodity-price shift plausibly represents a genuine change in Brazil's structural trade position, not just a transitory premium (this is the classic Balassa-Samuelson-adjacent argument, and matches terms-of-trade being the one channel with real, direct BRL support in the literature review). `eta(t)` is the state noise — how much the equilibrium itself is allowed to drift unexplained per period; this variance is one of the parameters the Kalman filter estimates (or that gets fixed via a signal-to-noise assumption if the estimation is poorly identified with it free).

### 3. Deviation equation (error correction)
```
deviation(t) = phi * deviation(t-1) + beta_1 * carry(t-1) + beta_2 * fiscal_risk(t-1) + epsilon(t)
```
`phi` is the mean-reversion speed (how fast a deviation closes on its own, independent of the pull variables); `beta_1`/`beta_2` let carry and fiscal risk explain *additional* short-run pull beyond pure reversion.

**Open design question #2**: fiscal risk is a genuinely disputed case in the literature between "permanent equilibrium-shifter" (NATREX-style treatments sometimes put sustained fiscal deterioration here) and "temporary risk-premium pull" (treated here, provisionally, as a deviation-side variable). Worth testing both specifications empirically rather than assuming one is correct.

---

## Mapping to the three models already underway

| Pull variable | Owning model (this project) | What's been learned so far |
|---|---|---|
| Carry | `carry_model.py` (built 2026-07-22) | Weak on its own across all 4 specs tested (level and change, short-term and 2y, nominal and real) — expect a small, likely insignificant `beta_1` here too. |
| Terms-of-trade / balance of goods | `terms_of_trade_model.py` (not yet built) | Not yet quantified in this project's own data, but independently the strongest-supported channel in the external literature (`fx_forecasting_theory_vs_practice.md` Part I §4) — the best-motivated candidate for the *transition* equation specifically, per design question #1 above. |
| Fiscal credibility | `fiscal_credibility_model.py` (not yet built) | CDS Brasil 5Y confirmed unavailable anywhere on this server (checked live, 2026-07-22). Market-implied breakeven inflation (`PREJS - NTNBJS` at the 60M/120M tenor, `base_mercado.interest_rates`) built and charted this session as a working proxy — clean series once a confirmed data bug (`PREJS`@120M, two bad windows in early 2010) was masked and interpolated. |

> In this, fix the bug in production for now

---

## Data mapping (what exists today vs. what's still missing)

| Ingredient | Status | Source |
|---|---|---|
| Real effective exchange rate (`rer`, the measurement equation's observed side) | **Have** | `macro_international.cmb_reer` |
| Carry (all 4 flavors already built) | **Have** | `macro_international.diferenciais_juros` + `base_mercado.interest_rates` (`PREJS`/`US_TREASURY`) — see `carry_model.py` |
| Terms of trade | **Have** | `macro_brasil.cmb_termos_troca` |
| Balance of goods / cambial flow | **Have** | `macro_brasil.cmb_balanco_pagmt`, `cmb_fluxo_cambial`, `cmb_comex_*` |
| Fiscal risk (CDS 5Y) | **Gap, confirmed** | Checked live across every schema on the server — nothing found. No free source previously identified either. |
| Fiscal risk (breakeven proxy) | **Have, built this session** | `base_mercado.interest_rates` (`PREJS - NTNBJS` @ 60M/120M) — needs the 2010 data-quality fix carried into any real model script, not just the throwaway plotting script used to find it |

No new data collection is required to build a first version of this model — every ingredient either already exists or has a working proxy, which is itself a useful, non-obvious finding from this session's data-mapping work.

---

## Estimation

`statsmodels.tsa.statespace` supports this directly, but the specific structure above (a state with an exogenous driver in the transition equation, plus exogenous regressors in a stationary AR(1) deviation) needs a **custom `MLEModel` subclass** — `UnobservedComponents` alone covers simpler local-level/trend cases but not this exact combination of an exogenous-driven state plus an exogenous-driven stationary component together. The variance parameters (state noise `eta`, deviation noise `epsilon`) are what the Kalman filter estimates via maximum likelihood; a poorly-identified model (too much flexibility, too little data) will show up as one of these variances collapsing to near-zero or exploding — a concrete diagnostic to check before trusting any fitted result, not just a theoretical risk.

---

## Honest caveats

- **This is a valuation/diagnostic framework, not a trading signal** — consistent with how the existing literature review frames every BEER/GSDEER-style tool it discusses. The deliverable is "how far from fair value, and how fast does that close," not a short-horizon directional call.
- **Fixed loadings on the three pull variables is a real, named limitation** (scapegoat theory, above) — worth stating explicitly in any output of this model, not just in this reference note.
>> Can we implement moving average parameters? Or better modeling that separatedly, because I want to test the hypothesis that the "important" fundamental change over time.
- **Identification risk is real** in any state-space model with a genuinely unobserved (not just missing-data) latent state — more parameters than a simple OLS regression, estimated from the same or fewer effective data points. Validate the fitted equilibrium path against something a person can sanity-check (does it look like a plausible, smooth "fair value" path, not a noisy replica of the actual rate) before trusting the pull-variable coefficients.
- **Sequencing matters**: this should come after `terms_of_trade_model.py` and `fiscal_credibility_model.py` exist as standalone pieces, per the Scope section — building the integrated model first would mean debugging three new data pipelines and a state-space estimator simultaneously.

---

## Suggested build sequence

1. Finish `terms_of_trade_model.py` and `fiscal_credibility_model.py` as standalone OLS-style models, matching `carry_model.py`'s pattern — understand each channel's own signal/noise first.
2. Build the real effective exchange rate series from `cmb_reer` and inspect it directly (levels, trend, any structural breaks) before writing any state-space code.
3. Start with the simplest viable version: terms-of-trade only in the transition equation, carry only in the deviation equation, fiscal risk left out — get a working, diagnosable two-variable model running before adding the third.
4. Add fiscal risk to the deviation equation; separately test it in the transition equation instead (design question #2) and compare.
5. Only once all of the above is working and sanity-checked: consider the time-varying-parameter extension that would address the scapegoat-theory caveat directly.
