---
aliases: ["Havranek 2013 - Transmission Lags of Monetary Policy: A Meta-Analysis"]
---

# Transmission Lags of Monetary Policy: A Meta-Analysis — Havranek & Rusnak 2013

**Type:** paper (meta-analysis)
**Tags:** #transmission-lags #monetary-transmission #meta-analysis #var #bayesian-model-averaging #financial-development #price-puzzle
**Source:** International Journal of Central Banking, December 2013 (JEL C83, E52)
**Language:** English
**Source file:** [[monetary_policy/clean_md/transmission_lags_meta_analysis (Havranek & Rusnak, 2013)]]

---

## Context and motivation

Policymakers need to know how long their actions take to transmit and what determines the speed. Transmission is commonly said to have "long and variable" lags (Friedman 1972; Batini & Nelson 2001; Goodhart 2001); most inflation-targeting central banks use a policy horizon between twelve and twenty-four months; models imply lags of similar length, but empirical estimates vary widely. Earlier cross-country work (Ehrmann 2000; Mojon & Peersman 2003; Cecchetti 1999; Elbourne & de Haan 2006) covered few countries at one point in time and said little about what drives transmission speed. The paper quantitatively reviews the VAR literature on the response of the price level to policy-rate shocks to give stylized facts on the average lag and on the sources of its variability.

## Core argument / thesis

Defining the transmission lag as the horizon at which the price level's fall after a monetary contraction is largest, the literature implies prices bottom out about two and a half years after a contraction once misspecifications are filtered out (29.2 months; the abstract rounds to twenty-nine), with a maximum fall of 0.9 percent on average after a 1-percentage-point hike. Lags are much longer in developed economies (roughly twenty-five to fifty months) than in post-transition economies (ten to twenty). The only robust country-level determinant is **financial development: greater financial development is associated with slower transmission**, which the authors read as financial institutions in developed systems having more ways to hedge against monetary surprises, so they need not react at once. Among method choices, monthly data give shorter lags and strictly decreasing impulse responses much longer ones.

## Key mechanisms / model

- **Sample (section 2, Table 1)**: published VAR studies with an impulse response of the price level (not inflation) to a policy-rate shock, normalizable to 1 percentage point, with confidence intervals. 198 impulse responses from sixty-seven studies, thirty countries (mostly developed and post-transition); search ended September 15, 2010.
- **Two response shapes (Figure 1)**: hump-shaped responses (100 estimates), where the lag is the month of the largest fall; strictly decreasing responses (98), where the lag is the last reported horizon (often five years) — such responses may signal a non-stationary VAR, and the lag then depends on the reporting window.
- **Explanatory variables (section 3, Table 4)**: thirty-three — country characteristics averaged over each study's sample (GDP per capita, growth, inflation, financial development as private credit/GDP, trade openness, central bank independence from Arnone et al. 2009), data characteristics (monthly frequency, observations, average year), specification (GDP deflator, single regime, lags, commodity prices, money, foreign variables, trend, seasonal dummies, number of variables, activity measure), estimation (BVAR, FAVAR, SVAR, sign restrictions) and publication characteristics (strictly decreasing, price puzzle, citations, impact factor, central-bank, policymaker and native co-authors, year).
- **Bayesian model averaging**: uniform model prior and unit information prior (Eicher, Papageorgiou & Raftery 2011), MCMC with 200 million iterations; a variable counts as effective when its posterior mean exceeds 1.3 posterior standard deviations (Masanjala & Papageorgiou 2008).
- **"Ideal study"**: plugging best-practice method choices and maximum publication quality into the BMA results to filter misspecification out of the average lag.
- **Robustness (section 4)**: country averages for hump-shaped responses only (Table 6) and responses without the price puzzle (Table 7); BMA on hump-shaped responses only (Figure 4); a Tobit with sixty months as the upper limit, general-to-specific (Tables 8 and 12); and an alternative response variable, the months until prices fall 0.1 percent (Figure 5; 173 of 198 responses reach it).

## Main results / findings

**Descriptive (Table 2).** Mean lag 33.5 months over all 198 estimates (median 37, standard deviation 19.4, range 1 to 60); 18.2 months for hump-shaped responses (median 15) and 49.1 for strictly decreasing ones (median 48). The average maximum price fall after a 1-percentage-point hike is 0.9 percent.

**Across countries (Table 3, at least five responses each).** Developed: United States 42.2, euro area 48.4, Japan 51.3, Germany 33.4, United Kingdom 40.4, France 51.3, Italy 26.6 months. Post-transition: Poland 18.7, Czech Republic 14.8, Hungary 17.9, Slovakia 10.7, Slovenia 17.6. The gap survives among responses without the price puzzle (Table 7) and narrows among hump-shaped responses (Table 6, where e.g. the United Kingdom is 10.0 and Italy 9.2), with fewer observations per country and developed-country studies more often reporting strictly decreasing responses.

**What explains the variation (Table 5, BMA).** Three effective variables: Financial Development (posterior inclusion probability 1.000, posterior mean 12.492, standard deviation 3.166), Monthly (0.730; -4.175, 3.036) and Strictly Decreasing (1.000; 26.122, 1.798 — about twenty-six months longer than hump-shaped). Central bank independence (0.705; 13.370, 10.412), time trend (0.472), impact factor (0.423) and price puzzle (0.383) have moderate inclusion probabilities but are not effective by the 1.3 criterion; GDP per capita, growth, inflation and openness are not robust.

**Corrected average.** The ideal study implies 29.2 months, about 4 months below the simple average; hardly changed if FAVAR or SVAR is chosen as best practice; 16.3 months if hump-shaped responses are preferred, and about another month less if responses without the price puzzle are preferred.

**Robustness.** Financial development keeps its sign and remains the most important country-level factor among hump-shaped responses (where other activity measures, the GDP deflator and foreign variables are associated with slower reported transmission). In the Tobit specific model (Table 8, 198 observations) financial development is 21.61 (5.375), significant at 1 percent; monthly data -12.04 (3.821); price puzzle 4.667 (2.343); central bank independence 29.38 (10.64); openness -12.67 (4.670); GDP per capita -11.48 (4.793); inflation -17.25 (8.739) — the authors do not stress the variables not confirmed elsewhere. With time to a 0.1 percent price fall as the outcome, financial development, central bank independence and trade openness matter, transmission being faster in more open economies and with more independent central banks, which "may point at the importance of the exchange rate and expectation channels"; higher-impact journals report faster transmission.

**Conclusion.** Monthly data shorten reported lags by about four months, consistent with Ghysels (2012) on mixed-frequency and temporal aggregation; monetary transmission "may slow down as the financial system of emerging countries develops, since financial innovations allow banks to protect better against surprise shocks in monetary policy."

## Limitations and caveats

- **The cleaner removed the end-of-paper References list** (about a quarter of the file), which includes the full citations of the sixty-seven primary studies; Table 1 still lists them by author and year. The argument, all results tables (2–8), the BMA diagnostics (Tables 9–11) and the general Tobit model (Table 12) survive.
- **Superscripts are lost in a few numbers**: the count of possible regressor combinations prints as "233" (the context — thirty-three variables, "several months" to enumerate — indicates a power of two), and Tables 9–11 print draws as "2 · 108" and model space as "8.6 · 109". The text gives the iterations as 200 million.
- **Figures 3–5 (the BMA model-inclusion charts) survive only as their captions**; which variables appear with which sign there is known only from the text. The bold typesetting that Table 5 uses for effective variables is lost.
- The introduction says section 3 links lags to "thirty country- and study-specific variables"; section 3 and Table 4 have thirty-three. Reported as written.
- The country groups are imperfect (the Czech Republic is classed post-transition although a developed economy for the World Bank since 2006, footnote 1); several country averages in Tables 6–7 rest on fewer than five responses.
- The lag for strictly decreasing responses depends on the reporting window chosen by authors; the Tobit cannot use Strictly Decreasing because it defines the censoring; the general-to-specific procedure is "far from perfect".

## Connections

- [[monetary_transmission_lags]] — the paper's subject: the average lag from monetary contraction to the price trough, its cross-country variation and its determinants (financial development, data frequency, response shape)
