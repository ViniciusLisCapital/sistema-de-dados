# BCB Small-Scale Model — Replication Plan

Source material: `modelo_agregado.pdf` (Relatório de Inflação, Dec/2021 — aggregate model revision) and `modelo_desagregado.pdf` (Relatório de Inflação, Mar/2021 — disaggregated model) in this folder. Both are BCB "boxes" describing the semi-structural small-scale models that feed Copom's decision process.

## Scope decision (2026-07-13)

Building the **aggregate model only** for now (single Phillips curve for free prices — not the 3-sector disaggregated version).

Intended use: **short-horizon conditional IPCA scenarios / decomposition** — i.e. reproducing the kind of exercise in the box's "Funções de resposta ao impulso" and "Choques de commodities e política monetária" sections, conditional on our own assumptions for Selic/FX/commodities/fiscal paths. Not a standing real-time nowcast.

## Key simplifications vs. a full replication

1. **Fixed parameters, no re-estimation.** We use BCB's own published posterior-mode coefficients (Table 1 of the Dec/2021 box) as given, instead of re-running the Bayesian estimation (priors + MCMC over 2003Q4–2019Q4). This removes the hardest part of the exercise entirely.
2. **Seeded latent states, no Kalman filter.** The output gap (`h_t`) and neutral rate (`r^eq_t`) are *not* re-derived from the 4-indicator dynamic factor block (PIB, Nuci, desocupação, Caged). Instead we seed them from BCB's own most recently disclosed point estimates and let the IS curve's own recursion (`h_t = β1 h_{t-1} - β2 r̂_t - ...`) propagate them forward using observed/assumed exogenous drivers.
   - **Tradeoff accepted:** this is an open-loop forward simulation, not a self-correcting filter — the simulated path will drift from BCB's own re-estimated truth the further out it runs without re-anchoring to a fresh disclosed value. Acceptable for short-horizon conditional scenarios; would need periodic re-seeding (whenever a new box/RPM comes out) if used over a long stretch.
   - **Consequence:** Nuci (FGV capacity utilization) — a genuine data gap otherwise — is no longer needed at all.

## Data map

| Variable | Equation | Status | Source | DB placement |
|---|---|---|---|---|
| IPCA livres, IPCA administrado | Phillips curve (LHS + weights) | ✅ have | `macro_brasil.inflc_agregados` (SGS 11428 / 4449) | existing |
| Selic realizada | Taylor rule, IS curve | ✅ have | `macro_international.diferenciais_juros` (raw `selic`, SGS 432) | existing |
| Fed Funds | UIP | ✅ have | `macro_international.diferenciais_juros` (raw `fed_funds`) | existing |
| USD/BRL spot (PTAX) | UIP, FX gap | ✅ have | `macro_brasil.cmb_ptax` (`ptax_venda`) | existing |
| Focus IPCA 12m/24m | inflation expectations eq. | ✅ have | `macro_brasil.expc_focus` | existing (used as proxy for `π^e_{t,t+4\|t}`) |
| Focus Selic EOP | IS curve real-rate gap | ⚠️ have, needs check | `macro_brasil.expc_focus` | existing — confirm it covers the multi-horizon path needed for `i^e_{t,t+4\|t}` (0.5/1/1/1/0.5 weighted average across next 4 quarters), extend horizons if not |
| IC-Br agro/metal/energia | Phillips curve, imported commodity inflation | ❌ gap | BCB SGS (codes to confirm) | new table, new `comm_` theme in `macro_brasil` (e.g. `comm_icbr`) |
| Meta de inflação (+ banda) | Taylor rule target, PPP long-run FX | ❌ gap | BCB SGS / CMN | new table `inflc_meta` in `macro_brasil` |
| Brent (USD) | commodity shock scenarios | ❌ gap | FRED (`DCOILBRENTEU`) | new table in `macro_international`, new `comm_` theme there (Brazil-agnostic global price — doesn't fit either schema rule cleanly, but closer to `macro_international` since it's not Brazil-specific) |
| ONI (El Niño/La Niña) | Phillips curve climate shock | ❌ gap | NOAA public CSV | new standalone table `clima_oni` in `macro_brasil` |
| CDS 5y Brasil | UIP risk premium | ❌ gap, **deferred** | no known free/open source | — |
| IIE-Br (incerteza) | IS curve | ❌ gap, **deferred** | FGV/IBRE portal, no open API | — |
| Hiato do produto mundial | IS curve (β5, smallest coefficient) | ❌ gap, **deferred** | needs trade-partner GDP + export weights | — |
| Resultado primário (ciclicamente ajustado) | IS curve fiscal term | ❌ gap, **deferred for v1** | raw series exists (Tesouro/BCB SGS); cyclical adjustment method undisclosed by BCB, would be our own | — |

### Deferred items (explicit decision, 2026-07-13)

CDS 5y Brasil, IIE-Br, and the world output gap are **deferred** — not needed to get a first working conditional-scenario version running. Revisit once the core simulation works and it's clear whether omitting them materially changes the results. Fiscal (cyclically-adjusted primary result) deferred for v1 for the same reason, though the raw series is easy to fetch whenever we pick it back up.

## Model-internal artifacts (new domain)

The model's own fixed parameters and seed states aren't raw macro data — they're artifacts of this specific model. New theme in `macro_brasil`: **`pm_`** (política monetária).

- **`pm_parametros`** — BCB's published posterior-mode coefficients (Table 1, Dec/2021 box), versioned by source box/vintage so future re-estimations by BCB can be tracked without overwriting history.
- **`pm_hiato_seed`** — seeded values for `h_t` (output gap) and `r^eq_t` (neutral rate), with as-of date and source citation (these come from manually reading BCB's published boxes/charts, not a structured feed). **Note:** the Dec/2021 box's own numbers (`r^eq_t` = 3.6% at 2021Q4) are now ~4.5 years stale — need a fresher print from a recent Relatório de Política Monetária before seeding the live model.

## Placement decisions confirmed with user (2026-07-13)

- **Brent → `macro_international`** (new `comm_` theme there).
- **CDS, IIE-Br, world output gap → deferred**, not built for v1.

## Progress log (2026-07-13)

- **SGS/FRED codes verified live** (direct API calls, not guessed from memory — practice adopted after a wrong-SGS-code bug in `cmb_balanco_pagmt`):
  - IC-Br: 27574 (geral), 27575 (agropecuária), 27576 (metal), 27577 (energia) — monthly, confirmed live through 2026-06.
  - Meta de inflação: SGS 13521 — confirmed live (3.50/2022 → 3.25/2023 → 3.00/2024–2026, matches known target path).
  - NOAA ONI: `https://www.cpc.ncep.noaa.gov/data/indices/oni.ascii.txt` — confirmed, columns `SEAS/YR/TOTAL/ANOM`.
- **`clima_oni` placed in `macro_international`, not `macro_brasil`** — same reasoning as Brent: it's a global Pacific SST index, not Brazil-specific, so it doesn't satisfy the `macro_brasil` criterion any better than Brent does. Applied the same placement logic the user confirmed for Brent, for consistency (not re-asked, since it's a low-stakes/reversible empty-table decision).
- **Tables created and populated:**
  - `macro_brasil.comm_icbr` (4 series, 1998-01 → 2026-06)
  - `macro_brasil.inflc_meta` (1999 → 2026)
  - `macro_international.comm_brent` (FRED `DCOILBRENTEU`, 1990 → 2026-07)
  - `macro_international.clima_oni` (1950 → 2026-04, filtered to the 4 calendar-aligned seasons JFM/AMJ/JAS/OND)
  - `macro_brasil.pm_parametros` — all 22 coefficients from Table 1 of the Dec/2021 box transcribed and inserted, vintage `RI_2021T4_agregado`.
  - `macro_brasil.pm_hiato_seed` — `output_gap` seeded at **0.4% for 2026Q2**, sourced from press coverage of the Jun/2026 RPM (BCB's own model estimate revised from 0.1%→0.5% for 1Q26, 0.4% for 2Q26). **Not verified against the primary RPM PDF** (WebFetch couldn't parse it) — flagged for confirmation when convenient.
- **`neutral_rate` seed NOT inserted — unresolved conflict.** Web search returned two contradictory figures for BCB's current neutral-rate estimate: 3.3% (attributed to the Mar/2026 RPM) and 5.0% (attributed to the Jun/2026 RPM, "stable since Jun/2025"). These are too far apart to be the same concept reported at two different dates — at least one is a search-synthesis error. Needs primary-source confirmation before seeding (e.g. reading the actual RPM box, not press/search summaries) — this number anchors the entire IS curve, so seeding it wrong silently corrupts every downstream projection.

## Resolution (2026-07-13)

Neutral rate confirmed by user: **5.0%** (RPM jun/2026, stable since jun/2025). Seeded in `pm_hiato_seed`.

## Model built: `analytics/monetary_policy/model.py`

Implements all 5 equations (Phillips curve for livres, IS curve, Taylor rule, UIP, climate/commodity terms) as a forward recursion from the seeded state, reading parameters/seed/history from MySQL. `load_history()`, `simulate(n_quarters, scenario)`, `decompose_last_quarter()`.

**Validation performed:** replayed the box's own IRF experiment (Selic +1pp for 4 quarters) through the engine and compared the 4-quarter-accumulated pi_livres response against the box's published result (Grafico 2b: -0.33pp at quarter 6, full IPCA). Result: sign and rough timing match; **magnitude is ~4-5x too large** (peak ~-1.5pp around quarter 9). Root cause documented in the module docstring: the engine approximates the expected future Selic path with the current/simulated rate itself (no forward curve available), so it doesn't discount for the market anticipating the shock's reversal the way BCB's real model-consistent expectations would — a direct, expected consequence of skipping equation 5 (deliberate scope decision, see above). **Treat this engine's magnitudes as directionally useful, not point-precise**, until/unless that gap is revisited.

## HTML report (2026-07-13)

`analytics/monetary_policy/generate_report.py` + `report.html` — same self-contained, `/*REPORT_DATA*/`-injection pattern as `analytics/exchange_rate/` and `analytics/inflation/`. Runs `simulate()` for a baseline (Selic endogenous via Taylor rule) and a shock scenario (Selic +1pp for 4 quarters, the box's own IRF experiment), plus KPI tiles from the latest history/seed. Output: `reports/bcb_model.html` (renamed from `monetary_policy_latest.html` per user request). The known calibration gap (magnitude overstated ~4-5x on the real-rate channel) is surfaced as a visible callout on the report itself, not just in this doc. Report now has two tabs: **Cenários** (the above) and **Sobre o Modelo** (beginner-oriented intro: what the model is, a flow diagram, one card per equation in plain language, a glossary, and the data-sources table) — added 2026-07-13 per user request.

```powershell
uv run python -c "from analytics.monetary_policy.generate_report import run; run()"
```

## Inflation-expectations equation (eq. 5) — investigated 2026-07-13, unresolved

Discussed why the engine skips eq. 5 (model-consistent/rational expectations) and uses the raw Focus survey instead: `E_t[π_{t,t+4}]` isn't a data series, it's "what the model itself predicts inflation will be 4 quarters out" — computing it requires solving the whole system's forward path jointly (a fixed-point problem: expectations at t depend on the simulated path t..t+4, which itself depends on expectations at each of those quarters). This is the direct cause of the ~4-5x IRF overstatement (both via pi_e not reacting to the simulated scenario in the Phillips curve, and via the `i^e_{t,t+4|t}` Selic-path proxy in `r_hat` not discounting for the market anticipating a shock's reversal).

**Tried: `simulate_consistent()` (extended-path / Fair-Taylor fixed-point iteration, damped).** Bootstrapped with the naive pass, then iteratively recomputed pi_e/i^e from the model's own simulated path each round, updating the guess only partway (relaxation=0.3) each time. **Diverged even with damping** — traced to a genuine instability, not a tuning problem: `r_hat = i^e - pi_e - r_eq`, and `i^e` (tied to Taylor's heavily-smoothed reaction, θ1+θ2≈0.91) can't move nearly as fast as an assumed `pi_e` path can within an iteration, so the gap between them widens every round instead of settling — the loop gain exceeds 1 in that direction, which no amount of positive damping fixes (mathematically: damping only helps when the raw loop gain is already <1). Removed from the codebase (would have produced NaN/garbage if left in) — a real fix would need the full linear rational-expectations solve (Blanchard-Kahn/Klein's method, matching what BCB's own Kalman-filter/state-space setup effectively does), not a lightweight iteration.

**Implemented instead: `simulate_forward_pi_e()`.** A single, non-iterated refinement — bootstrap with the naive pass, then re-simulate ONCE using that bootstrap's own accumulated `pi_livres` over `[t, t+3]` as `pi_e` (instead of holding it flat). Can't diverge (no loop). Re-ran the same IRF check:
- Peak 4Q-accumulated response improved from **-1.47pp (naive) to -0.43pp**, much closer to the box's published **-0.33pp**.
- **New artifact**: the sign flips after ~quarter 5, showing a spurious inflationary overshoot peaking at **+1.45pp around quarter 11** — not present in the box's own published chart (which decays smoothly to zero). Root cause: the bootstrap pass still carries the full naive overstatement, and feeding that overstated (too-deep) disinflation forward as "the expectation" makes the Taylor rule in the final pass ease too aggressively once the policy-override window ends, producing a rebound that's an artifact of the approximation rather than a genuine model property. `i^e` (Selic-path proxy) is untouched in this version — only `pi_e` was fixed.

**Status: on hold, left on record for future work (user is thinking through how to proceed, 2026-07-13).** `simulate_forward_pi_e()` exists in `model.py` and is validated (numbers above), but is **not wired into `generate_report.py`** — the report still uses plain `simulate()`. Options on the table when picked back up:
1. Ship `simulate_forward_pi_e()` in the report as-is, with the overshoot artifact disclosed.
2. Ship it but only display/trust the first ~4-5 quarters, before the artifact appears.
3. Leave the report on the naive `simulate()` and treat this as a documented-but-unshipped improvement.
4. Invest in the full rational-expectations solve (Blanchard-Kahn/Klein) — the only way to fix both channels (`pi_e` and `i^e`) without the overshoot artifact.

## Next steps (if picked back up)

1. **Decide on the inflation-expectations fix above** — the main open thread.
2. Confirm the output-gap seed (0.4%, 2026Q2) against the primary RPM PDF when convenient — currently sourced from press coverage only, not the primary document (WebFetch couldn't parse the RPM PDF).
3. Revisit deferred terms (CDS, IIE-Br, world output gap, cyclically-adjusted fiscal) if their omission turns out to matter empirically for real scenarios.
4. Commodity weights (w_a/w_m/w_e) are equal-weighted by assumption (not disclosed by BCB) — could be refined by regressing IC-Br geral on its three sub-indices if more precision is wanted.
5. Focus Selic EOP horizon coverage (item flagged in the data map above) — still not confirmed to cover the multi-horizon path eq. (2.2) wants; moot for now since `r_hat` currently uses `i_t` directly, but relevant again if a proper multi-horizon Selic expectation is ever built.
