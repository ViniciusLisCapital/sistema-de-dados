# Goldfajn and Werlang 2000 — The Pass-through from Depreciation to Inflation: A Panel Study

**Type:** Empirical paper (panel econometrics)
**Tags:** #pass-through #real-exchange-rate #currency-crisis #emerging-markets #brazil #panel-data
**Source:** Ilan Goldfajn (PUC-Rio / Deputy Governor, Banco Central do Brasil) and Sergio R.C. Werlang, working paper, 2000
**Language:** English
**Raw file:** [[depreciation_pass_through (Goldfajn, 2000)]]

---

## Context and motivation

Written in the aftermath of the 1990s emerging-market currency crises (Mexico 1994, Asia 1997–98, and implicitly Brazil's own 1999 float) to answer a policy-urgent question: after a large devaluation, how much of it actually becomes inflation, and how fast? The paper's motivating stylized fact — that observed post-crisis inflation was systematically *lower* than conventional wisdom (and, this paper shows, even the paper's own estimated model) predicted — is directly relevant to how BCB and any EM central bank should calibrate inflation forecasts after a large depreciation.

## Core argument / thesis

Pass-through is not a fixed structural parameter — it rises with the horizon measured (peaking around 12 months, then flattening/declining slightly by 18), and its cross-sectional determinants are systematic: it is higher where the real exchange rate was *not* overvalued beforehand (i.e., where the depreciation is a genuine relative-price correction rather than an excess/overshooting move), higher where initial inflation is already high (inertia/credibility channel), and higher in emerging/non-OECD economies than in developed ones.

## Key mechanisms / model

- **Panel setup**: 71 countries, monthly data 1980–1998, ~14,000 observations. Dependent variable: accumulated CPI inflation over horizon j; key regressor: accumulated nominal effective exchange rate depreciation over the same horizon (lagged by at least one month).
- **Four determinants, each with a theoretical rationale**:
  1. **GDP gap** (HP-filtered deviation from trend) — firms pass costs through more easily when demand is strong; recessions dampen pass-through.
  2. **RER misalignment** (actual RER vs. HP-filtered trend, not a PPP-equilibrium benchmark) — a depreciation that merely corrects prior overvaluation is a relative-price adjustment (tradables/nontradables), not a generalized price-level shock, so it dampens inflation; conversely, "excess" depreciation not warranted by misalignment either becomes inflation or reverses via later appreciation (cites the authors' own related finding, Goldfajn and Gupta 1998).
  3. **Initial inflation** — higher current inflation signals more persistence/inertia, raising the perceived permanence of a cost shock and thus the pass-through (cites Taylor 1999 on the inflation-persistence–pass-through link).
  4. **Openness** (exports+imports/GDP) — a larger tradables sector mechanically means a given depreciation moves a bigger share of the CPI basket; theoretically distinguished from openness's separate, well-known *negative* effect on the *level* of inflation via reduced incentive for inflationary finance (Romer 1993, Barro-Gordon-style).
- **Headline results (baseline, no cross-terms)**: pass-through coefficient by horizon — 1 month: 0.012; 3 months: 0.170; 6 months: 0.426; 12 months: 0.732 (peak); 18 months: ~0.70 (slight decline). A 10% depreciation therefore raises inflation by only ~1.2% within a month but ~7.3% over a year — most of the effect is *not* immediate.
- **RER overvaluation dampens pass-through substantially**: at the 12-month horizon, a 10% prior overvaluation reduces subsequent inflation by 11.8% — nearly one-for-one offsetting a matched-size depreciation. This is the paper's central practical message: *a depreciation that corrects a known misalignment should not be expected to generate proportional inflation.*
- **Regional/development breakdown**: pass-through highest in the Americas (12-month coefficient 0.692, rising to 1.24 at 18 months — the paper attributes this explicitly to Latin American inflation-depreciation spiral tendencies) and Asia (0.712 at 12 months); lowest in Europe (0.360) and Oceania (0.158). Emerging markets show near-complete 12-month pass-through (0.912) vs. 0.605 for developed countries; non-OECD 12-month pass-through (0.754) is roughly 4× the OECD figure (0.188). But the *dampening* effect of overvaluation is also stronger in emerging markets (−15.34% per 10% overvaluation vs. −7.9% in developed countries) — EM pass-through is higher on average, but also more sensitive to whether the move is "warranted."

## Main results / findings

- Pass-through is horizon-dependent, not a single number — comparing 1-month vs. 12-month coefficients without noting the horizon is a category error the paper explicitly warns against (Figure 1 shows this pattern held across the 1990s crisis episodes: Mexico 1994 stands out as the exception with unusually high, rapid pass-through).
- The paper's own forecasting exercise (flagged in the abstract, not present in this extracted text) finds the estimated model *over-predicts* inflation in known large-depreciation episodes, even correcting for survey-based exchange rate expectations — i.e., even a properly estimated, determinant-rich pass-through model errs on the side of predicting too much inflation after a crisis, not too little.

## Limitations and caveats

- **This extraction is incomplete** — the raw text available cuts off mid-sentence partway through Section IV (the cross-term/interaction specification that lets each determinant affect the pass-through coefficient itself, not just the inflation level directly). Sections V (forecast fit in known crisis cases), VI (survey-expectations robustness), VII (further robustness checks), and VIII (conclusion) are referenced in the abstract/intro but not present in this source file — do not cite specific findings from those sections without sourcing the full paper.
- RER misalignment is measured against an HP-filtered trend, not a PPP-equilibrium benchmark — the authors are explicit this is a deliberate choice (citing their own Goldfajn and Valdes 1999), but it means "overvaluation" here is a statistical/cyclical concept, not a structural fair-value estimate like GSDEER.
- Openness's coefficient sign flips across specifications (positive in some, negative in others) — the paper itself flags this variable as "more sensitive to the horizon and sample chosen" than RER misalignment or initial inflation.

## Connections

- [[exchange_rate_pass_through]] — this is the empirical/econometric backbone for the pass-through concept, complementing Krugman's qualitative textbook treatment with panel-data coefficients by horizon, region, and development status
- [[Krugman 2023 - Output and the Exchange Rate in the Short Run]] — same "pass-through" term and definition, here estimated rather than theorized; the RER-misalignment-dampens-pass-through finding is the empirical analogue of Krugman's pricing-to-market discussion
- [[ppp_balassa_samuelson]] — RER misalignment (vs. HP trend) as a determinant of *future* inflation is the mirror image of PPP's usual framing (misalignment predicting future *depreciation*) — here misalignment predicts how much of a *given* depreciation becomes inflation
- [[currency_crisis_indicators]] — direct empirical companion: this paper is about what happens to inflation *after* a crisis-driven depreciation, complementing that concept's pre-crisis leading indicators
