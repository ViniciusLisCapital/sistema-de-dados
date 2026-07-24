# Bayesian Deviation Model — USD/BRL (built and fit 2026-07-23)

*Companion doc to `bayesian_deviation_model.py`. Positioned as "attempt one" at explaining the PPP deviation from `ppp_equilibrium.py` — deliberately simpler than, and prior to, the Kalman-filter state-space model in `../referencia/state_space_equilibrium_model.md` ("attempt two"). See `DATA_REQUIREMENTS.md` for the broader model-by-model data inventory. Results below; design rationale sections below that are kept as originally written (pre-registered before any fitting) so the two can be compared honestly.*

## What it will test

Whether carry, terms-of-trade, long-term inflation expectations (bond breakeven), and fiscal risk (CDS) explain the gap between the actual USD/BRL rate and its relative-PPP equilibrium — i.e. whether the same three-to-four "pull variable" channels the state-space concept note proposes for its deviation equation actually show up as meaningful regressors in a plain regression, before investing in a full unobserved-state model. A Bayesian framing (vs. the OLS/GARCH/Markov-switching toolkit already used in `uip_model.py`/`carry_model.py`) is used here specifically to get posterior distributions and credible intervals on each coefficient, rather than point estimates and p-values — more directly comparable to how the eventual Kalman filter will report uncertainty, and a natural stepping stone toward it (same library, PyMC, would carry over).

## Dependent variable

```
D(t) = 100 * ln( ptax(t) / equilibrium(t; b) )
```

as already computed in `ppp_equilibrium.py`, `b` = the selected base month (dashboard default: 1994-07).

**Base-month choice doesn't matter for this regression.** Substituting the equilibrium formula in:

```
D(t; b) = g(t) - g(b),   where   g(x) = ln(ptax(x)) - ln(ipca_index(x)) + ln(cpi_index(x))
```

`g(b)` is a constant — it doesn't depend on `t`. So changing the base month only shifts `D(t)` up or down by a fixed amount; it never changes its shape, its month-to-month changes, or its correlation with anything else over time. Concretely: **whatever base month is used to build `D(t)`, every regression coefficient below (the βs) comes out identical — only the intercept (α) shifts.** This resolves the "which base month feeds the regression" question raised when the dashboard's base-month selector was built: it doesn't need resolving, any base month works, so the dashboard's default (1994-07) is fine to use as-is.

## Candidate regressors

All four already fetched (not yet regressed) by `ppp_equilibrium.py`, each left-joined onto the shared monthly index — null before its own start:

| Variable | Source | Available from | Expected sign on `D(t)` |
|---|---|---|---|
| `carry(t-1)` | `diferenciais_juros.diferencial_nominal` (Selic − Fed Funds, % p.a.) | 1999-03 | Ambiguous a priori — `uip_model.py`/`carry_model.py` both already found carry weak/wrong-signed against UIP directly; no strong reason to expect it behaves differently here. Included for completeness/comparability with the state-space concept note's own pull-variable list, not because prior work predicts a strong result. |
| `tot(t-1)` | `cmb_termos_troca.termos_de_troca_funcex` (Funcex PX/PM, 2018=100) | 1994-07 | Negative — an improving terms-of-trade (rising PX/PM) should pull the currency stronger than PPP alone implies, i.e. push `D(t)` down. |
| `breakeven(t-1)` | `base_mercado.interest_rates`, `PREJS − NTNBJS` @ 120M (10y bond-implied inflation expectation, % p.a.) | 2006-01 | Positive — rising long-term inflation expectations (an anchoring/credibility signal) should coincide with a weaker BRL than PPP implies. |
| `fiscal(t-1)` | `cmb_risco_pais.cds_5y_usd` (Brazil 5Y CDS, USD, bps) | 2007-12 | Positive — rising sovereign risk should coincide with a weaker BRL than PPP implies. |

All four lagged one month, matching the existing project convention (`uip_model.py`, `carry_model.py`): the regressor must be known before the return period it's meant to explain, avoiding look-ahead and same-period simultaneity.

**`breakeven` and `fiscal` are both risk/credibility proxies and will likely be correlated with each other** (CDS spreads and long-term breakevens tend to move together during stress episodes) — worth checking their pairwise correlation before fitting, and treating any weak/insignificant result on either one with the multicollinearity caveat in mind rather than concluding "channel X doesn't matter."

## Required pre-step: stationarity (run 2026-07-23 — see Results above for the table)

`state_space_equilibrium_model.md`'s own open threads already flag this as undone: order of integration (I(1) vs. I(0)) hasn't been tested on any of `D(t)`, `carry`, `tot`, `breakeven`, or `fiscal`. This matters here directly, not just for the state-space model:

- If `D(t)` and the regressors are all stationary (or the regressors are stationary predictors of a stationary `D(t)`), a **levels regression** (below) is valid as specified.
- If any are I(1) (e.g. `tot` and `breakeven` both plausibly trend over multi-decade windows) and not cointegrated with `D(t)`, a levels regression risks the classic spurious-regression problem (inflated R², coefficients that don't mean what they look like they mean).

**Before writing any model code**, run ADF and KPSS on `D(t)` and all four regressors (`carry`, `tot`, `breakeven`, `fiscal`), each over its own available window. If any look I(1), fit the **first-difference** specification instead (or alongside, as a robustness check):

```
level spec:      D(t) = α + Σ βᵢ · Xᵢ(t-1) + ε(t)
difference spec: ΔD(t) = α + Σ βᵢ · ΔXᵢ(t-1) + ε(t)
```

This is a cheap, mechanical step (a few lines with `statsmodels.tsa.stattools.adfuller`/`kpss`) that should happen first and will determine which of the two specs above is actually appropriate — don't skip straight to fitting the level spec on the assumption it's fine.

## Sample window

The joint model (all four regressors together) can only use their overlap: **`fiscal` (from 2007-12) is the binding constraint**, so the usable joint sample is roughly **2007-12 → today (~223 months)** — much shorter than `tot`'s own range (1994-07→today) or `carry`'s (1999-03→today).

Proposed approach, once the model is actually built:
1. **Primary spec**: all four regressors, fit on the 2007-12→today overlap.
2. **Robustness spec**: drop `breakeven` and `fiscal` (the two short series), fit `carry` + `tot` only on the much longer 1999-03→today window — checks whether the primary spec's conclusions about `carry`/`tot` hold up over a longer sample once the short-sample-only regressors are removed, or whether the shorter window is itself driving results.

## Proposed methodology

**Library**: PyMC (`uv add pymc`, not yet installed — install when this is actually built, not before).

**Likelihood**: start with Normal errors; if posterior predictive checks show fat tails (plausible for FX — large, infrequent depreciation episodes), switch to Student-t errors with an estimated degrees-of-freedom parameter, same robustness motivation as `uip_model.py`'s use of GARCH for volatility clustering, just handled via the error distribution instead of conditional variance.

**Priors**: standardize every regressor (subtract mean, divide by SD) before fitting, so a single weakly-informative prior shape works for all of them regardless of native units (% p.a., index points, bps):

```
α        ~ Normal(0, 10)                       # D(t) is in % already, wide enough to be uninformative
β_carry, β_tot, β_breakeven, β_fiscal
         ~ Normal(0, 2)                        # weakly informative on standardized regressors
σ        ~ HalfNormal(5)                       # or ν ~ Gamma(2, 0.1) + σ if Student-t
```

These are starting points, not final choices — revisit once real data is in hand and prior/posterior predictive checks are run.

**Sampling**: NUTS (PyMC's default), 4 chains, check `r_hat < 1.01` and adequate effective sample size (`arviz.summary`) before trusting any posterior. Posterior predictive check against the actual `D(t)` series as a first sanity pass.

**Reporting** (once fit): for each β, report the posterior mean, the 94% HDI (PyMC/ArviZ default credible interval), and the probability the coefficient has the expected sign — e.g. `P(β_fiscal > 0)` — which is the natural Bayesian analogue to a one-sided p-value and more directly answers "does fiscal risk push the currency weaker than PPP" than a two-sided frequentist test would.

## Relationship to the state-space model ("attempt two")

This model is explicitly the simpler, static-coefficient predecessor:

- **Same pull variables** (carry, terms-of-trade, fiscal/credibility) as the state-space concept note's deviation equation `deviation(t) = φ·deviation(t−1) + β₁·carry(t−1) + β₂·fiscal_risk(t−1) + ε(t)` — this model is close to a version of that equation *without* the `φ·deviation(t−1)` autoregressive term and without treating `equilibrium(t)` as a filtered latent state (it uses the already-fixed `ppp_equilibrium.py` construction instead).
- **No time-varying coefficients** — the state-space model's own open thread about whether β's importance changes over time (the Scapegoat Theory concern) is explicitly deferred, not addressed here. If this static model's residuals show structure (e.g. a rolling-window version of a coefficient drifts materially), that's itself evidence motivating the time-varying extension, same as `uip_model.py`'s rolling-β diagnostic (still unbuilt, flagged in that doc's TODO) would be.
- **PyMC as the shared tool** — building this first, in PyMC, means the tooling (data prep, priors-on-standardized-regressors pattern, ArviZ diagnostics workflow) carries over directly when the state-space model is eventually specified as a custom PyMC state-space model (or via `pymc-extras`' state-space module) rather than starting that from zero.

## Results

### Stationarity pre-check (ADF + KPSS, run before any model code was written)

| Series | Window | ADF stat | ADF p | KPSS stat | KPSS p | Verdict |
|---|---|---|---|---|---|---|
| `deviation` | 1994-07→2026-06 (n=383) | −1.695 | 0.434 | 0.666 | 0.017 | **I(1)** — both tests agree |
| `carry` | 1999-03→2026-06 (n=327) | −2.757 | 0.065 | 1.286 | 0.010 | **I(1)** (borderline on ADF, KPSS clearly rejects stationarity) |
| `tot` | 1994-07→2026-04 (n=381) | −2.219 | 0.199 | 1.736 | 0.010 | **I(1)** — both tests agree |
| `breakeven` | 2006-01→2026-06 (n=245) | −3.525 | 0.007 | 0.169 | 0.100 | **I(0)** — both tests agree |
| `breakeven_gap` | 2006-01→2026-06 (n=245) | −2.826 | 0.055 | 0.480 | 0.046 | borderline, leans I(1) |
| `fiscal` | 2007-12→2026-06 (n=222) | −3.538 | 0.007 | 0.183 | 0.100 | **I(0)** — both tests agree |

All six series' **first differences** are unambiguously stationary (ADF p<0.001, KPSS p=0.100, every series) — as expected. Per the pre-registered rule, since `deviation` itself (the dependent variable) and two of the four regressors (`carry`, `tot`) are I(1), the model below uses the **first-difference specification uniformly** rather than a mixed levels/differences spec — the simpler, safer choice for "attempt one", at the cost of not exploiting whatever long-run/cointegrating information a levels or error-correction spec might have captured for `breakeven`/`fiscal` (both already stationary in levels). That tradeoff is exactly the kind of thing a future ECM/cointegration pass (flagged below) would revisit.

### Correlation among candidate regressors (levels, pairwise, min 24 overlapping obs)

|  | carry | tot | breakeven | fiscal |
|---|---|---|---|---|
| **carry** | 1.00 | −0.55 | **0.68** | 0.35 |
| **tot** | −0.55 | 1.00 | 0.01 | −0.55 |
| **breakeven** | 0.68 | 0.01 | 1.00 | 0.36 |
| **fiscal** | 0.35 | −0.55 | 0.36 | 1.00 |

The pre-registered concern was `breakeven`/`fiscal` correlation (0.36 in levels, 0.47 in first differences — moderate, as expected for two credibility/risk proxies). **The actually-largest pairwise correlation turned out to be `carry`/`breakeven` at 0.68** — sensible in hindsight (a hawkish Selic and elevated long-term inflation expectations tend to move together, both reflecting the same underlying inflation regime), but not the pairing flagged in advance. Worth keeping in mind when reading `beta_carry` and `beta_breakeven` together in the primary spec below.

### Model fits

All four fits: NUTS, 4 chains, 1500 tune + 2000 draws, `target_accept=0.9`. **All r-hat = 1.00, all ESS > 5700** — clean convergence throughout, no divergences. Regressors standardized before fitting, so coefficients are in "per 1 SD of the (differenced, lagged) regressor" units, comparable across variables with different native units.

**Primary spec** — Δcarry + Δtot + Δbreakeven + Δfiscal, all lagged 1 month → Δdeviation. n=219, 2008-02→2026-05 (fiscal is the binding constraint on sample length):

| Coefficient | mean | sd | 94% HDI | P(expected sign) |
|---|---|---|---|---|
| α (intercept) | 0.219 | 0.298 | [−0.320, 0.792] | — |
| β_carry | 0.131 | 0.305 | [−0.434, 0.719] | no strong prior expectation |
| β_tot | −0.268 | 0.303 | [−0.852, 0.276] | P(β<0) = **0.816** |
| β_breakeven | −0.387 | 0.330 | [−1.017, 0.207] | P(β>0) = **0.122** |
| β_fiscal | 0.520 | 0.338 | [−0.115, 1.151] | P(β>0) = **0.940** |

**Primary spec, `breakeven_gap` instead of raw `breakeven`** — nearly identical to the above (β_gap = −0.362 vs. β_breakeven = −0.387; P(β>0) = 0.135 vs. 0.122). **The de-anchoring-gap construction turns out not to matter empirically once everything is differenced** — `inflc_meta` only steps once a year, so `Δbreakeven_gap ≈ Δbreakeven − Δtarget`, and `Δtarget` is zero except at year boundaries, making the two regressors nearly collinear in differenced form. This resolves the "raw level vs. gap" open question below: use raw `breakeven` (one fewer moving part, same result) unless a future levels/ECM spec revisits this, where the annual step would matter more.

**Primary spec, Student-t errors** (same 4 regressors) vs. **Normal errors** — LOO comparison:

| Model | rank | elpd_loo | p_loo | elpd_diff | dse |
|---|---|---|---|---|---|
| student_t | 0 | −639.47 | 6.75 | 0.00 | 0.00 |
| normal | 1 | −640.96 | 6.50 | 1.49 | 1.48 |

Student-t ranks slightly better, but `elpd_diff` (1.49) is essentially equal to its own standard error (`dse`=1.48) — **no real evidence favoring Student-t over Normal**. The fitted degrees-of-freedom (ν≈16.9, 94% HDI [3.6, 36.7]) is high enough that Student-t is behaving close to Normal anyway. Coefficients under Student-t are qualitatively the same as Normal, just somewhat attenuated (β_breakeven −0.264 vs. −0.387, β_fiscal 0.429 vs. 0.520) — plain Normal errors are an adequate, simpler choice for this model; no evidence of the fat-tailed residuals that motivated checking in the first place.

**Robustness spec** — Δcarry + Δtot only (no `breakeven`/`fiscal`), longer sample: n=324, 1999-05→2026-05:

| Coefficient | mean | sd | 94% HDI | P(expected sign) |
|---|---|---|---|---|
| α (intercept) | 0.059 | 0.264 | [−0.434, 0.547] | — |
| β_carry | −0.156 | 0.258 | [−0.659, 0.307] | (sign flips vs. primary's +0.131) |
| β_tot | −0.248 | 0.263 | [−0.724, 0.263] | P(β<0) = **0.828** |

### Interpretation

- **Terms of trade is the one consistently-signed, moderately-supported finding** — negative in both the primary spec (P=0.816) and the much-longer robustness spec (P=0.828), with nearly identical point estimates (−0.268 vs. −0.248) despite an 9-year-longer sample. An improving terms-of-trade does appear to pull USD/BRL stronger than PPP alone implies, and this doesn't depend on which sample window or which other regressors are included — the most trustworthy result here, though "moderately supported" (≈82% posterior probability of the expected sign, not a near-certain 99%) is the honest characterization, not "significant."
- **Fiscal risk (CDS) has the single strongest sign-probability in the primary spec (94%)**, matching the expected direction (higher sovereign risk → weaker BRL than PPP implies) — but this is **only tested in the short 2008-2026 sample**; there's no longer-sample robustness check for it (CDS data doesn't go back further), so unlike the terms-of-trade result, this one hasn't been cross-checked against a different window. Treat as suggestive, not confirmed.
- **Carry shows no reliable signal, and its sign isn't even stable across samples** (+0.131 in the primary/short spec vs. −0.156 in the robustness/long spec, both with wide HDIs straddling zero) — consistent with `uip_model.py` and `carry_model.py`'s own repeated finding that the Selic−Fed Funds differential doesn't robustly explain USD/BRL movements in this database, now extended to the PPP-deviation framing specifically, not just the strict-UIP one.
- **Breakeven inflation (raw or de-anchoring gap) came back with the *opposite* sign from what was pre-registered as expected** — posterior mean negative (rising long-term inflation expectations associated with the BRL getting *stronger* than PPP implies, not weaker), with ~88% posterior probability against the expected direction. This is the most surprising result and shouldn't be quietly reinterpreted as "breakeven doesn't matter" — it came back with a fairly clear *wrong-signed* posterior, not just a noisy null. Two candidate explanations, neither adjudicated here: (1) a **hawkish-response/credibility-premium channel** — if BCB tends to tighten (or is expected to tighten) when long-term expectations rise, and that response is itself currency-supportive, the net effect on `D(t)` could plausibly be negative even though the raw "de-anchoring is bad for the currency" intuition says positive; (2) **simultaneity that the 1-month lag doesn't fully clear** — if both breakeven and the exchange rate respond quickly to the same underlying shocks (e.g. a risk-off episode that simultaneously weakens BRL and — via pass-through expectations — this would push the correlation positive, not negative, so this explanation is weaker than (1) but not ruled out). Worth a dedicated look before leaning on this result for anything.
- **All HDIs are wide relative to the point estimates** — this is a small, noisy dataset (n=219–324 monthly observations, four barely-correlated-with-`deviation` macro series) and none of these results should be read as precise or highly confident. The sign-probability framing above is deliberately the most honest way to report them; resist the temptation to round "94%" up to "significant."

### Follow-up: testing the drift directly (2026-07-23, same day, later)

The primary spec's non-trivial α (0.219/month) compounds into a large chunk of the current PPP gap — in the nominal-level bridge (`bayesian_deviation_model.py`'s `level_decomposition`), "baseline (α + pre-sample anchor)" accounts for **+R$1.54 of the current ~R$1.58 gap between equilibrium (R$3.48) and actual PTAX (R$5.06)**, dwarfing all four named channels combined (which currently net to ≈R$0.00). The user pushed back on this directly: "the PPP should be the only directional systematic drift along the time" — prompting two follow-up tests, both revealing a genuine methodological lesson rather than settling the question outright.

**Test 1 — no-intercept spec** (`primary_no_alpha`, same 4 regressors, α forced to 0 via `fit_regression(..., no_intercept=True)`): the four betas came back **statistically unchanged** from the primary spec (β_carry 0.131→0.136, β_tot −0.268→−0.265, β_breakeven −0.387→−0.387 exact, β_fiscal 0.520→0.520 exact — all well within one posterior SD, i.e. just MCMC noise between independent runs). **The drift didn't disappear — it just relocated from "baseline" to "residual (unexplained)" in the decomposition.** Root cause, confirmed directly: standardizing (z-scoring) a regressor forces its sample mean to exactly 0 by construction; a mean-zero regressor is mathematically incapable of ever explaining a non-zero mean in the dependent variable (`mean(Δdeviation)` over the primary sample = **+0.222/month**, matching α almost exactly). None of the 4 channels has its own multi-decade one-directional trend (carry/tot/breakeven/fiscal all oscillate with their own cycles), so none of them *could* structurally absorb a persistent one-directional drift regardless of what the true relationship is — that mean can only ever land on the intercept, or, absent one, the residual.

**Test 2 — error-correction spec** (`primary_ecm`, "Option B", the user's own suggestion): adds `deviation_lag1` (the lagged deviation *level*, not a difference — `build_deltas()` now also returns this column) alongside the same 4 standardized channel deltas, α kept. Critically, `deviation_lag1` must be passed via the new `raw_cols=["deviation_lag1"]` argument to `fit_regression()` — kept in native units, NOT standardized — since its whole usefulness here is that its sample mean is genuinely non-zero (+14.7 over the primary sample, unlike the always-zero-mean standardized regressors). (First attempt at this spec wrongly standardized it too, reproducing Test 1's exact mistake — caught and fixed before reporting results; `fit_regression()`'s `raw_cols` mechanism exists specifically to prevent this class of bug going forward — don't standardize a variable whose non-zero mean is the point.)

Result:

| Coefficient | mean | sd | 94% HDI | note |
|---|---|---|---|---|
| α (intercept) | 0.424 | 0.341 | [−0.192, 1.087] | *increased* from 0.219, not decreased — see below |
| ρ (β_deviation_lag1, raw units) | −0.014 | 0.011 | [−0.034, 0.007] | P(ρ<0) = **89.2%** — suggestive, not "reliable" by this model's own 94%-HDI bar |
| β_carry | 0.157 | 0.309 | — | ≈unchanged from primary spec |
| β_tot | −0.275 | 0.300 | — | ≈unchanged |
| β_breakeven | −0.358 | 0.337 | — | ≈unchanged |
| β_fiscal | 0.522 | 0.340 | — | ≈unchanged |

Converting ρ into a half-life (among the 89.2% of posterior draws where ρ<0): **median ≈44 months (~3.7 years)**, P10–P90 range 24–160 months. This lines up almost exactly with Rogoff's classic "PPP puzzle" finding — real-exchange-rate deviations empirically take 3-5 years to halve, and are notoriously hard to pin down statistically even when the true effect is real, because the reversion is so slow relative to typical sample lengths. This model reproduced that exact signature (right magnitude, weak significance) without being told to.

**Why α went *up*, not down** (the counterintuitive part, worth remembering — not a bug): under this spec, α means "drift you'd expect if the currency were currently sitting exactly at PPP fair value (deviation=0)." The sample's average deviation was well above zero (+14.7), and with ρ (weakly) negative, some of what looked like "pure drift" in the primary spec is actually "starting from an above-average misalignment, slowly correcting" — a drag, not a push. Removing that (small) drag from the observed average pushes the model's implied zero-point intercept *up* to compensate. The algebra: OLS with an intercept always satisfies `α = mean(y) − ρ·mean(x)`; with `ρ<0` and `mean(x)>0`, `−ρ·mean(x) > 0`, so α exceeds `mean(y)`.

**Net honest read**: there is weak-but-real evidence of PPP-consistent mean-reversion, at a magnitude matching the standard literature — but even accounting for it, the model still wants a sizeable constant drift (0.42/month) at the hypothetical fair-value point that the ECM term alone doesn't explain away. This doesn't resolve "why a drift" so much as sharpen it: some of it is slow reversion (textbook-consistent, weakly detected), and a separate, still-unexplained piece survives regardless.

Neither `primary_no_alpha` nor `primary_ecm` has been folded into `build_dashboard_payload()`/the HTML dashboard or `export_excel_audit.py` yet — both are saved (`bayesian_results/primary_no_alpha_*`, `bayesian_results/primary_ecm_*`) but this was a discussion-only round; no downstream artifacts were regenerated against them.

### Technical note: compiler backend

Initial runs used PyTensor's pure-Python fallback (no C++ compiler present) and were slow enough (10+ minutes, not finishing) that a compiler was installed mid-session: MSYS2 + `mingw-w64-x86_64-gcc` via `winget install MSYS2.MSYS2` then `pacman -S mingw-w64-x86_64-gcc`, with `C:\msys64\mingw64\bin` added to the user `PATH` (persists across sessions/terminals; a shell open before the change won't see it without prefixing `PATH` explicitly for that command). This cut each model fit from 10+ minutes to ~35-40 seconds. `pytensor` still warns it can't link a BLAS library (falls back to a slower unoptimized linear-algebra path) — not a blocker for a model this small, but worth fixing (e.g. `conda`'s BLAS-linked numpy, or an OpenBLAS install) if a much larger PyMC model is ever built on this machine.

## Open design questions (not yet decided)

- ~~Should `breakeven` be used as a raw level, or as a **de-anchoring gap**~~ — **resolved empirically, see Results above**: in differenced form the two are nearly collinear (`inflc_meta` only steps annually), so raw `breakeven` is used going forward; the gap construction adds a fetch dependency (`inflc_meta`) without changing any conclusion. The conceptual classification discussion below is still worth keeping, for whenever a levels/ECM spec revisits this (there the annual step would matter more):
  - **Classification (resolved 2026-07-23)**: the de-anchoring gap is conceptually a **monetary credibility** variable (confidence the central bank will hit its own target) — not fiscal. But in Brazil specifically, the dominant channel by which de-anchoring happens is fiscal dominance (Sargent & Wallace 1981; Blanchard 2004 applies this directly to Brazil): a deteriorating fiscal trajectory raises the market-priced probability of future debt monetization or a fiscal-driven depreciation, which shows up as higher long-term inflation expectations even absent any change in the central bank's own reaction function. Since `fiscal` (CDS) is already a separate regressor, treat the gap as its own channel rather than folding it into "fiscal" — whatever it explains *net of* CDS is the more defensible monetary-credibility signal.
- ~~Should `tot` enter as a level or a change~~ — **resolved**: `tot` tested as I(1) (see Results), so it's differenced, same as the other four series.
- Does a **cointegration** framing (Engle-Granger or Johansen, `D(t)` and the I(1) regressors sharing a common stochastic trend) make more sense than the plain-differences spec actually fit? **Partially attempted 2026-07-23** — see the "Follow-up: testing the drift directly" subsection above: a single-equation error-correction spec (`primary_ecm`) tested `deviation_lag1` directly and found weak evidence of mean-reversion (P(ρ<0)=89%, implied half-life ~44 months, matching the Rogoff PPP-puzzle range) — but a full cointegration framework (Engle-Granger/Johansen, testing whether a genuine common stochastic trend exists) is still not attempted.
- **New, from the Results above**: the unexpected negative sign on `breakeven`/`breakeven_gap` — is it a hawkish-response/credibility-premium channel, or residual simultaneity the 1-month lag doesn't fully clear? Not adjudicated — see Interpretation above.

## TODO / next steps

Done (2026-07-23): ADF/KPSS stationarity pre-check; breakeven/fiscal (and full pairwise) correlation check; `uv add pymc arviz`; `bayesian_deviation_model.py` written and fit (primary ×2 breakeven variants, Student-t comparison, robustness spec); Results section written above; raw-vs-gap question resolved empirically; MSYS2/MinGW-w64 g++ installed for compiled (fast) PyTensor sampling.

Done (2026-07-23, later same day): tested whether the primary spec's α ("drift") survives without a free intercept (`primary_no_alpha` — it doesn't disappear, it relocates to the residual, since standardized regressors are mean-zero by construction — a real methodological lesson, see "Follow-up" subsection above) and via a single-equation error-correction spec (`primary_ecm` — weak, textbook-consistent mean-reversion evidence, ~44-month median half-life, but α survives at an even larger value once correctly interpreted at the zero-deviation point). Added `fit_regression()`'s `raw_cols` parameter for this (lets a named regressor skip standardization when its non-zero mean is the point).

Still open:
- [ ] Investigate the unexpected negative `breakeven` sign (hawkish-response-channel vs. simultaneity hypotheses above) — the most substantive open thread from this round of fitting.
- [ ] A longer-sample robustness check for `fiscal` isn't possible (CDS data doesn't go back further) — but consider whether a longer-history risk proxy (e.g. `cmb_reservas_bc`, or something EMBI-like if a source is ever found) could substitute for a robustness pass on that specific channel.
- [ ] A full cointegration/ECM framework (Engle-Granger or Johansen) is still not attempted — only the single-equation `primary_ecm` spec has been tried (see Follow-up above).
- [ ] Neither `primary_no_alpha` nor `primary_ecm` is wired into `build_dashboard_payload()`/the HTML dashboard or `export_excel_audit.py` yet — both were discussion-only tests this session.
- [ ] The `primary_ecm` half-life finding (~44 months median) is a concrete candidate input for calibrating the state-space model's equilibrium-pull speed — bring it into that design discussion (planned next session).
- [ ] Fix the "PyTensor could not link to a BLAS installation" warning (OpenBLAS or conda's BLAS-linked numpy) if a much larger PyMC model is ever built on this machine — not a blocker at this model's scale.
- [ ] Decide how/whether any of this feeds into the state-space model ("attempt two") — this doc's own "Relationship to the state-space model" section lays out the conceptual link, but no code has been shared between the two yet.
