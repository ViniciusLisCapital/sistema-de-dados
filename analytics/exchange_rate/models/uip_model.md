# UIP Model — USD/BRL

*Companion doc to `uip_model.py`. First model built in the `analytics/exchange_rate/models/` series — see `DATA_REQUIREMENTS.md` for the full model-by-model data inventory and `../referencia/fx_forecasting_theory_vs_practice.md` for the broader theory-vs-practice context this sits inside.*

## What it tests

Uncovered Interest Parity: does the Selic–Fed Funds interest-rate differential predict subsequent USD/BRL depreciation, with the coefficient UIP's no-arbitrage logic requires (β = 1)? Three increasingly refined estimators are fit on the same regression: plain OLS, GARCH(1,1)-error, and a 2-regime Markov-switching version that lets β and the error variance differ by (endogenously estimated) volatility regime.

## Literature

- **Fama (1984)**, *"Forward and Spot Exchange Rates"* — the original finding that the spot-change-on-forward-premium regression comes back with the wrong sign; established that most forward-premium variance is risk-premium variance, not genuinely expected depreciation. (`referencia/er_forecasting/`)
- **Araújo et al. (SciELO, 2000–2014, inflation-targeting era)** — the direct BRL precedent this model is checked against: GARCH coefficient of **−2.94** (wrong sign vs. UIP's β=1), with a Markov-switching extension finding **−2.94 in low-volatility months, flipping >+1.00 in high-volatility ones**. Documented in `../referencia/fx_forecasting_theory_vs_practice.md` Part I §2.
- **Bacchetta & van Wincoop (2004, 2009/2013)** and **Fratzscher (2011)** — the "scapegoat theory" motivating the *next* model in this series (driver attribution / time-varying importance of fundamentals); the UIP result here is also read partly as evidence for or against parameter instability in its own right (see Results below). (`referencia/er_forecasting/`)

## Data and variables

| Variable | Source | Transformation | Why |
|---|---|---|---|
| `ds` | `macro_brasil.cmb_ptax.ptax_venda` (SGS 1, daily PTAX) | Resampled to month-start (`MS`, last obs. in month) → log return × 100 | Monthly log return of the exchange rate, in %; positive = BRL depreciation. Matches the monthly grain of the interest-differential input (no reason to work at daily frequency when the regressor is monthly). |
| `diff_lag1_m` | `macro_international.diferenciais_juros.diferencial_nominal` (Selic − Fed Funds, % a.a.) | Resampled to month-start (last obs.) → ÷12 (annualized → monthly-equivalent) → lagged 1 month | **÷12** puts the regressor on the same horizon as `ds` — without this, a 1pp *annualized* differential would be compared to a *monthly* return, and UIP's β=1 benchmark would no longer mean anything. **Lag 1** so the differential is known before the return period it's meant to explain (avoids look-ahead / same-period simultaneity — the differential from month t−1 predicts the return realized during month t). |

**No forward FX rate exists in the database**, so — same substitution the literature above uses — the interest-rate differential stands in for the forward premium via covered interest parity (f − s ≈ i − i*).

**Sample: 1999-01 onward** (effective start 1999-04 once the lag is applied, n=327 months to 2026-06). Brazil's pre-1999 crawling-peg/band regime (Real Plan) used a different exchange-rate mechanism than the free float UIP describes; mixing the two regimes into one regression would conflate them.

**Nominal, not real, differential** — UIP is a nominal no-arbitrage condition by construction (it compares nominal currency returns; there's no inflation term in its derivation). Using the real differential instead would test real interest parity (UIP + PPP combined), which conflates the interest/risk-premium channel with the inflation channel that the PPP model — next in this series — is meant to isolate separately. See chat discussion 2026-07-17 for the full reasoning; a real-differential robustness pass is worth revisiting once the PPP model exists (see TODO).

## Methodology

```
ds(t) = α + β · diff_lag1_m(t) + ε(t)
```

1. **OLS**, HAC standard errors (`maxlags=3`) — baseline, `statsmodels.OLS`.
2. **GARCH(1,1)** on the same mean equation (`mean="LS"`, pure exogenous regression, no AR term on `ds` itself) — captures FX volatility clustering and gives more correct SEs than OLS under heteroskedasticity. Package: `arch` (`arch_model`), added to `pyproject.toml` for this model.
3. **2-regime Markov-switching regression** (`statsmodels.tsa.regime_switching.markov_regression.MarkovRegression`, `switching_exog=True, switching_variance=True`) — both β and the error variance are allowed to differ by regime, with regime membership estimated endogenously (not imposed via an external volatility threshold). This is what's checked against Araújo et al.'s low-vol/high-vol split.

All three reuse the `MySQLDataRequester` read pattern already established in `analytics/monetary_policy/model.py` — no new data-access abstraction introduced.

## Results

| Model | β | p-value | Note |
|---|---|---|---|
| OLS | −0.759 | 0.271 | R² = 0.004 |
| GARCH(1,1) | −0.572 | 0.714 | mean-eq. β, GARCH errors |
| Markov low-vol regime | −0.892 | 0.151 | σ² = 12.80 |
| Markov high-vol regime | −3.490 | 0.401 | σ² = 70.28 |

**Sign**: consistently negative across all three estimators — reproduces the general Fama-puzzle direction (wrong sign vs. UIP's β=1), consistent with the global and BRL literature.

**Magnitude vs. Araújo et al.**: the high-vol-regime β (−3.49) lands in the same ballpark as their reported GARCH coefficient (−2.94) — but assigned to the *opposite* regime. Their result: −2.94 in **low**-vol months, flipping to **>+1.00** in **high**-vol months. Ours: −0.89 in low-vol, −3.49 in high-vol — both negative, no sign flip. Also weaker throughout: nothing here clears conventional significance (all p > 0.15), vs. their apparently significant result.

**Plausible explanations, not adjudicated here**: (a) sample-period difference — Araújo et al. stop at 2014, this model runs 1999–2026, so more than a decade of additional regimes (2015–16 crisis, 2020 COVID, 2022) that they never saw; (b) a specification difference not fully recoverable from the bibliography summary alone; (c) taken at face value, this divergence is itself a small data point *for* the parameter-instability story motivating the next model in this series — if the "true" UIP coefficient isn't stable across sample windows, that's not a bug in this model, that's the scapegoat-theory thesis showing up empirically.

**Regime detection sanity check (passes)**: the smoothed high-volatility-regime probability spikes exactly at Brazil's known FX stress episodes — 2002 election crisis, 2008 GFC, 2011–12, the 2015–16 crisis, 2020 COVID, 2022 (see `reports/fx_models/uip_diagnostics.png`). The regimes being economically identifiable, even though the regime-specific β doesn't replicate the literature's exact pattern, is good evidence the Markov-switching fit is capturing something real rather than overfitting noise.

## Graphs produced

- `reports/fx_models/uip_diagnostics.png` — 3-panel: (1) `ds` monthly return series, (2) `diff_lag1_m` differential series, (3) smoothed high-volatility-regime probability (shaded).

## Graphs still needed (flag for when a report/PDF gets built)

None of these exist yet — noting them now so they aren't lost before this becomes a presentable deliverable:

1. **Scatter of `ds` vs. `diff_lag1_m`** with the OLS and GARCH fitted lines overlaid — makes the (weak) relationship, and how far off β=1 sits, visually direct in a way the time-series panels don't.
2. **PTAX *level* series (not just returns)** with the high-vol-regime periods shaded directly on the actual exchange-rate path — far more intuitive for a non-technical reader than a return series plus a separate probability panel.
3. **Side-by-side bar chart: our β estimates vs. Araújo et al.'s benchmark**, per regime — makes the sign-flip-vs-no-sign-flip divergence obvious at a glance, since right now that finding only lives in a text paragraph.
4. **Rolling-window (e.g. 36-month) OLS β plot** — cheap to add now, and doubles as a preview of the driver-attribution/scapegoat model later in this series; shows instability continuously rather than as two discrete regimes.
5. **Regime transition/duration summary** (from `p[0->0]`, `p[1->0]`) — expected duration in each regime, to give "how long does a high-vol episode typically last" a number rather than leaving it to eyeballing the shaded panel.
6. If this ever goes client-facing: a plain-language callout translating "β is negative" into "BRL's carry has historically *not* been offset by depreciation the way textbook UIP predicts" — the polished reports in this repo (`exchange_rate`, `inflation`, `monetary_policy`) all pair a chart with plain-language framing, and this model has none yet.

## TODO / next steps

- [ ] Re-run on Araújo et al.'s original 2000–2014 sub-sample specifically, to check whether the exact regime-flip pattern shows up in that narrower window (isolates "sample period" as the explanation for the divergence above).
- [ ] Once the PPP model exists: run the real-differential version of this same regression as an explicit robustness/decomposition check (not a replacement) — see the "nominal, not real" reasoning above for why that has to wait.
- [ ] Consider extending to multiple horizons (3m, 12m), matching the multi-horizon convention in the broader UIP literature (`fx_forecasting_theory_vs_practice.md` cites Bussière et al.'s "New Fama Puzzle" testing several horizons).
- [ ] Consider a GARCH-M (GARCH-in-mean) specification — puts the conditional variance directly into the mean equation as an explicit time-varying risk-premium term, rather than just using GARCH for correct standard errors.
- [ ] Add the rolling-β diagnostic (item 4 above) — lowest-effort of the flagged graphs, and directly useful groundwork for the scapegoat/driver-attribution model.
- [ ] Decide, once more models exist: fold into one consolidated FX-models report (reusing the `/*REPORT_DATA*/` + Plotly.js pattern from the other three repo reports), or keep as a standalone research-script deliverable.
