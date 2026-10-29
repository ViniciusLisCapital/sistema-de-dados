---
aliases: ["Vicente & Guillen 2010 - Do inflation-linked bonds contain information about future inflation?"]
---

# Do inflation-linked bonds contain information about future inflation? — José Valentim Machado Vicente & Osmani Teixeira de Carvalho Guillen 2010

**Type:** paper (BCB Working Paper; empirical)
**Tags:** #breakeven-inflation #inflation-expectations #inflation-risk-premium #ntn-b #expectations-hypothesis #brazil
**Source:** Banco Central do Brasil, Working Paper Series n. 214, Oct. 2010, p. 1-30
**Language:** English
**Source file:** [[expectations/clean_md/breakeven_inflation_information (Vicente & Guillen, 2013)]]

---

## Context and motivation

Market participants and central bankers read break-even inflation (the BEIR, nominal minus real yield) as the main market measure of expected inflation; the paper quotes Bernanke calling inflation-linked bonds the most important source of inflation expectations. But the BEIR is an expectation plus an inflation risk premium, so it is a clean forecast only if that premium is negligible or constant. The paper asks whether the BEIR actually predicts realized inflation, using Brazil's NTN-B market: large (over US$ 200 billion outstanding), with an indexation lag of only half a month (against three months for TIPS) and no deflation floor, which removes two distortions that complicate US studies. Unlike the affine-model literature it surveys, it uses a "model free" forecasting regression in the spirit of Campbell–Shiller and of Christensen–Prabhala's test of implied against realized volatility.

## Core argument / thesis

If the inflation risk premium is constant over time (a BEIR version of the expectations hypothesis) and expectations are rational, regressing realized inflation on the BEIR should give a slope of one and a zero constant. The test shows this holds only at short horizons. At 3 and 6 months the BEIR is an unbiased forecast; at 12 and 18 months it has almost no explanatory power; at 24 and 30 months it is significant but negatively related to realized inflation. The authors read the medium and long-horizon failure not as a puzzle but as evidence of a time-varying inflation risk premium, which the linear regression cannot absorb, and warn that the BEIR should be used "very careful[ly]" as a proxy for future inflation.

## Key mechanisms / model

**Definitions (Section 2, equations 1–2).** The BEIR at horizon τ is the nominal minus the real continuously compounded yield of that maturity. Realized inflation over τ is the average of annualized one-period inflation rates from t to t + τ. Equation (1) regresses realized inflation on the BEIR with a constant: a nonzero slope means the BEIR carries information; slope one and zero constant means it is an unbiased forecast. Equation (2) decomposes the BEIR into the conditional expectation of inflation plus an inflation risk premium.

**What carries the test.** Two assumptions turn (2) into (1): the risk premium does not depend on t (it may depend on maturity), and expectations are rational. If the premium varies over time and is correlated with the BEIR, the slope is biased away from one, and can even turn negative, without the BEIR being uninformative about expectations. The constant then cannot be read as the premium when the slope differs from one, which the authors acknowledge.

**Data (Section 3).** Monthly nominal and real zero curves from ANDIMA, April 2005 to July 2010, fitted with the Svensson model: nominal from LTN and NTN-F, real from NTN-B (IPCA-linked). The sample starts in 2005 to avoid NTN-B liquidity problems between 2001 and 2005. Horizons: 3, 6, 12, 18, 24 and 30 months.

**Estimation (Section 4).** OLS, then two-stage least squares (instrument: the lagged BEIR) and GMM (three lags) with Newey–West covariance, to deal with endogeneity and with the autocorrelation that overlapping horizons create. A Durbin–Wu–Hausman test finds no significant difference among the three (footnote 8).

**Why the BEIR may fail (Section 4, end).** Three candidate reasons, not tested: a short sample (five years); a genuinely risky market with a high premium; and a clientele (preferred-habitat) effect, since NTN-B attract investors with strong aversion to inflation uncertainty. In July 2010 pension funds, hedging inflation-linked liabilities, held 33% of NTN-B outstanding and only 5% of LTN and NTN-F.

## Main results / findings

- **Short horizons: unbiased.** At 3 and 6 months the slope is positive and significant and the joint hypothesis of unit slope and zero constant is not rejected under TSLS and GMM (Tables 3–4). Under OLS the 3-month joint test reads 0.02 (Table 2), which, if it is a p-value, would reject unbiasedness at the 95% confidence level the tables use; the text does not discuss this, and states unbiasedness at 3 and 6 months without qualification.
- **Medium horizons: no information.** At 12 and 18 months the slope is insignificant, the R² very low and the joint hypothesis rejected: the BEIR does not inform about 12- and 18-month-ahead inflation.
- **Long horizons: significant but negative.** At 24 and 30 months the slope is significant and negative in all three methods except GMM at 24 months (footnote 9); the 30-month OLS slope is -0.36 (Table 2). Simple correlations already show the sign switch: positive up to 12 months, negative beyond (Table 1).
- **A large constant.** For medium and long horizons the constant is significant, which the authors place between 400 and 700 basis points and read, cautiously, as investors requiring a high reward to hold inflation-linked bonds beyond one year.
- **Robustness.** Estimates are similar across OLS, TSLS and GMM, and the over-identification test does not reject (Table 4).

## Limitations and caveats

- By the authors' account: five years of data; the causes of the failure are conjectured, not tested; the linear model assumes a constant premium, which the results themselves reject at long horizons; the constant cannot be interpreted as a premium when the slope differs from one.
- What the text shows: realized inflation over a horizon of up to 30 months overlaps heavily across monthly observations, so the effective number of independent observations at long horizons is small; the sample covers one disinflation and the 2008 crisis only. The test conflates three things that could each bend the slope (a time-varying risk premium, liquidity, and non-rational expectations); it cannot tell them apart. The 3-month OLS joint test is in tension with the unbiasedness claim (above). Two internal slips: the text describes negative correlations "for the horizons of 18, 24, and 36 months" where Table 1 reports 18, 24 and 30; and the Campbell–Shiller reference is dated 1991 in one sentence and 1989 in the next.
- Damaged passages: equations (1) and (2) and the realized-inflation formula are spread over several lines, with subscripts detached and the summation and error symbols printed as "(cid:88)" and "(cid:15)"; the note describes them in words. In Tables 2–4 the coefficient subscripts sit on separate lines and the boldface that marks significance at 95% is lost, so significance cannot be read from the tables alone; the row of the joint test is labelled only by the hypothesis. Figure 1 survives only as its caption. The file's date (Oct. 2010, the working-paper date) differs from the year in its file name. The reference list is not in the file, and the file ends with three stray entries of the BCB working-paper catalogue.

## Connections

- [[breakeven_inflation]] — defines the BEIR, decomposes it into expected inflation plus an inflation risk premium, and tests its forecasting power by horizon on Brazilian NTN-B, April 2005 to July 2010
- [[expectations/synthesis/brazil_taming_inflation_expectations (Bevilaqua, Mesquita & Minella, 2007)]] — written when the NTN-B market was judged too illiquid at policy-relevant horizons to extract expectations (footnote 3); this paper starts its sample in 2005 for the same reason and finds the BEIR informative only at short horizons
