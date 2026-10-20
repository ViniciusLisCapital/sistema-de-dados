---
aliases: ["Adrian 2013 - Pricing the Term Structure with Linear Regressions"]
---

# Pricing the Term Structure with Linear Regressions — Adrian, Crump & Moench 2013

**Type:** paper (staff report version, with appendix)
**Tags:** #term-premium #affine-term-structure #yield-curve #bond-risk-premia #principal-components #treasuries
**Source:** Federal Reserve Bank of New York Staff Reports, no. 340, August 2008, revised April 2013 (JEL G10, G12) — the staff-report version of the article the tracker lists as *JFE*, 2013
**Language:** English
**Source file:** [[monetary_policy/clean_md/term_structure_linear_regressions (Adrian, Crump & Moench, 2013)]]

---

## Context and motivation

Affine term structure models assume an exponentially affine pricing kernel, prices of risk affine in the state variables and Gaussian shocks, which make yields affine in the states with cross-maturity restrictions. They are usually estimated by maximum likelihood, which is computationally heavy beyond three factors and, in the recent faster methods (Joslin, Singleton & Zhu 2011; Hamilton & Wu 2012), still needs numerical optimization and assumes serially uncorrelated yield pricing errors. The paper proposes estimating the same class of models with three ordinary least squares steps on bond *returns*, and uses it to settle how many factors price Treasuries, how risk premia vary, and how to split yields into expected short rates and term premia.

## Core argument / thesis

A three-step regression estimator (ACM) prices the time series and cross-section of Treasury yields fast, with analytical standard errors, without imposing the no-arbitrage recursions in estimation, without a zero-coupon curve, and with observable or unspanned factors. Specification tests favor **five principal components of yields** as pricing factors; fewer are rejected. In the five-factor model, practically all time variation in risk premia is a price of **level** risk, driven mainly by the second (slope) and fifth principal components — factors that barely move yields but strongly predict returns. The five-factor model and an unrestricted four-factor Cochrane–Piazzesi (CP) model give similar term premia, but the five-factor model wins out of sample and is the preferred specification.

## Key mechanisms / model

- **Model (section 2.1, equations 1–13)**: state variables follow a VAR(1) with Gaussian shocks (1–2); exponentially affine pricing kernel (4) with essentially affine prices of risk λt = Σ^(-1/2)(λ0 + λ1Xt) (5, Duffee 2002). One-month log excess returns then decompose into an expected return, a convexity adjustment, a priced return innovation and a return pricing error (12), with constant factor exposures β when the factors are linear combinations of yields.
- **Three-step estimator (section 2.2, equations 14–17)**: (1) OLS VAR of the factors to get innovations and Σ; (2) regress excess returns on a constant, factor innovations and lagged factors (14–15), giving exposures β, and a, c; (3) cross-sectional regressions of a and c on β give λ0 and λ1 (16–17). Asymptotic distribution with generated-regressor correction (19–20, Appendix); the variance of β depends only on σ² and Σ, so whether a factor prices returns can be tested without estimating the rest.
- **Affine yields and the term premium (section 2.4, equations 21–29)**: the standard recursions for An and Bn (25–26), plus a ½σ² term from the return pricing error; setting λ0 = λ1 = 0 gives risk-neutral yields equal to expected average future short rates, and the **term premium is the fitted yield minus the risk-neutral yield**. Equation (29) shows that i.i.d. yield errors imply serially correlated return errors — so likelihood methods that assume uncorrelated yield errors implicitly allow return predictability the factors miss; the return-based approach makes no such assumption.
- **Data (section 3.1)**: Gürkaynak, Sack & Wright (2007) zero-coupon yields for 3 to 120 months; excess returns for N = 12 maturities over the one-month yield; monthly sample 1987:01 – 2011:12, T = 300. A third specification uses H.15 constant-maturity yields and returns on Fama maturity-sorted CRSP portfolios of coupon bonds (N = 11).
- **Tests (section 3.2)**: Anderson (1951) rank test on β (31) and a Wald test that a factor's exposures are zero (32); Wald tests that a row of Λ or of λ1 is zero (33–34). Pricing-kernel variance decomposed by factor (35–36).
- **Extensions (section 4)**: unspanned factors with zero exposures (38–49); linear restrictions on prices of risk by minimum distance (50–52); maximal Sharpe ratio √(λt′λt) (53–54); daily estimation by applying monthly principal-component weights to daily yields; consistency of principal components as observed factors (55–57).

## Main results / findings

**Five factors are needed (Table 1).** Across four yield datasets (GSW; Fama–Bliss plus GSW as in Duffee; H.15; CRSP constant maturity) and two return datasets (GSW zero-coupon, Fama portfolios), Wald tests "overwhelmingly reject" that the fifth factor's exposures are zero and the rank tests "broadly support" five factors.

**Five-factor fit (Table 2, Figures 1–2, 4).** Average yield pricing errors do not exceed 0.4 basis points in absolute value and their standard deviation stays below 1 basis point; yield errors are strongly autocorrelated (first-order 0.793 to 0.936) while return errors are not — as equation (29) implies. Observed and fitted excess returns are almost indistinguishable, and expected excess returns vary substantially over time. The regression exposures β and the recursive pricing parameters Bn, never imposed to coincide, are visually indistinguishable for the first three factors — so imposing cross-equation constraints "provide[s] little or no gains" in fitting the curve.

**Prices of risk (Table 3).** Level risk is priced: a negative constant (-0.019, t = -2.566), varying significantly with the slope (-0.016, t = -2.160) and the fifth component (0.030, t = 3.987). A higher slope means higher expected excess returns, increasing with maturity (as in Campbell & Shiller); a one-standard-deviation decline in the fifth component increases the ten-year bond's annualized expected excess return by about 6%. **Slope risk is not priced** (Wald 7.097, p 0.312). Curvature risk is priced and varies with the level, curvature and fourth component. Expected returns load almost entirely on the second, fourth and fifth components, yields almost exclusively on the first three. All five prices of risk contribute to pricing-kernel volatility, but for the ten-year bond it is primarily the time variation of level risk that moves expected returns (Figure 3).

**Four-factor CP model (Tables 4–5).** The CP factor is the first principal component of fitted values from regressing monthly excess returns on ten GSW one-year forward rates (average R² 7.5%; the first component explains 94.65%), added to the first three principal components with unrestricted prices of risk. Fit is somewhat looser (average errors no larger than 2.9 basis points, standard deviations below 5). CP prices all risks except slope and is the only significant driver of level risk (-0.043: a one-standard-deviation CP shock raises the ten-year expected excess return by 8.7%). CP's restriction that only level risk is priced, and only by the CP factor, is rejected with a p-value of 10−6, and imposing it worsens the fit, especially at the long end. Even five principal components explain only 65.6% of the CP factor although they explain 99.99% of yields; CP's correlations with the five components are 5%, 45%, 19%, -17% and -62%.

**Five versus four factors (section 3.5, Figure 7).** In-sample ten-year term premia are very similar across five-factor, four-factor and unspanned variants. Out of sample (training 1987:01–1991:12, expanding window), the five-factor model beats a random walk in forecasting average short rates at all horizons up to five years, while the four-factor model has larger errors at longer horizons. Estimated on maturities up to ten years, the four-factor model implies yields at longer maturities "far below their realized values" (it understates risk-neutral persistence); the five-factor model slightly overstates them — so implausible long yields are "not a general feature of five-factor models", contrary to Joslin, Singleton & Zhu.

**No zero-coupon curve needed (section 3.6, Figure 8).** Five H.15 principal components and Fama portfolio returns produce a zero-coupon curve visually close to Fama–Bliss discount yields, although built very differently. Parameter stability: sup-LM of 31.70, below the 90% critical value; the over-ten-year portfolio, whose duration drifts, is dropped.

**Unspanned macro factors (section 4.1, Table 6).** In the Joslin, Priebsch & Singleton specification (three principal components plus unspanned core inflation and CFNAI factors), zero exposures are not rejected (p = 88.63 and 96.81), the cross-sectional fit is poorer, level-risk time variation is weaker, and **slope risk becomes priced** through a highly significant CFNAI coefficient — "time variation in the pricing kernel that is not spanned by the yield curve".

**Sharpe ratios, daily term premia, consistency (sections 4.3–4.5).** Maximal Sharpe ratios are reasonable — the five-factor peak is 2.30 with a sample average below one — contrary to Duffee's overfitting concern; treating the fourth and fifth components as unspanned lowers them slightly and leaves the term premium very similar. Daily estimation since August 2009 prices two-, five- and ten-year notes precisely, and the ten-year term premium is strongly correlated with the MOVE index of Treasury option volatility although no option data are used. Bootstrapping the pricing parameters 1,000 times puts the identity matrix within one standard deviation of the implied principal-component loadings, so treating principal components as observed is "numerically negligible" as a source of inconsistency.

## Limitations and caveats

- **Version**: the file is the New York Fed staff report (revised April 2013), not the *Journal of Financial Economics* article the tracker names; results may differ from the published version.
- **The reference list is not in the file**: it passes from the appendix straight to the tables.
- **Equations are damaged by layout**: hats, subscripts, under-braces and fraction bars are split across lines in (7)–(19), (23)–(29), (40)–(54) and throughout the appendix derivations (58)–(166); the structure is recoverable from the text, which is what is described above.
- Figures 1–11 survive only as captions and axis ticks; the term-premium paths, out-of-sample errors, Sharpe ratio series and MOVE comparison are known only from the text. Tables 1–6 are legible (one value per line).
- One passage could not be matched to the tables as printed: section 4.1 says the second principal component "significantly drives time variation in slope risk" "as in the five-factor specification", but in Table 3 the slope row is not significant (Wald p 0.312) and in Table 6 the PC2 row's own-factor coefficient has t = -1.837. Read that passage against the tables.
- Authors' own caveats: principal components are treated as observed, ignoring extraction error (shown negligible); the higher-order components are only weakly spanned, so their prices of risk are weakly identified; Fama portfolios change composition over time; extensions to inflation and credit risk are left for future work.

## Connections

- [[term_premium]] — the paper's central object: the term premium as the fitted yield minus the risk-neutral yield (expected average short rate), estimated by regression, with level risk carrying almost all of its time variation
- [[monetary_policy/synthesis/information_effect_hf_identification (Nakamura & Steinsson, 2018)]] — uses the affine term structure decomposition of Abrahams, Adrian, Crump & Moench, by an overlapping group of authors, to separate the response of risk-neutral rates and term premia to FOMC shocks
