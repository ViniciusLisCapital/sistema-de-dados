# Break-even Inflation

**Type:** Market-based measure of inflation expectations
**Tags:** #breakeven-inflation #inflation-expectations #inflation-risk-premium #inflation-linked-bonds

---

## Definition

Break-even inflation (BEIR) at a given maturity is the nominal yield minus the real (inflation-linked) yield of that maturity: the inflation rate at which the two bonds pay the same. In Brazil it is the spread between the nominal curve (LTN, NTN-F) and the IPCA-linked curve (NTN-B). Market participants and central bankers treat it as the main market reading of expected inflation (Vicente & Guillen).

## Mechanism

The BEIR is not the expectation itself: it equals the expected inflation over the horizon plus an inflation risk premium, the compensation investors in nominal bonds require for bearing inflation uncertainty (Vicente & Guillen, equation 2). It is an unbiased forecast of realized inflation only if that premium is constant over time and expectations are rational; then a regression of realized inflation on the BEIR has slope one and zero constant. A premium that varies over time and co-moves with the BEIR biases the slope away from one, and can turn it negative, even if the BEIR still contains the market's expectation. Liquidity and the investor base also enter the spread: a clientele with a preferred habitat (in Brazil, pension funds hedging inflation-linked liabilities) can distort it.

## When it applies / when it fails

- **Short horizons work, long horizons do not** (Vicente & Guillen, Brazil April 2005 to July 2010): at 3 and 6 months the BEIR is an unbiased forecast; at 12 and 18 months it has almost no explanatory power; at 24 and 30 months it is significant but negatively related to realized inflation, which the authors attribute to a time-varying inflation risk premium.
- **Market liquidity is a precondition.** Brazil's NTN-B were judged too illiquid at policy-relevant horizons to extract expectations before the mid-2000s (Bevilaqua, Mesquita & Minella, footnote 3); Vicente & Guillen start their sample in 2005 for the same reason.
- **Contract design matters.** An indexation lag (three months for TIPS, half a month for NTN-B) and a deflation floor (absent in NTN-B) change what the spread measures (Vicente & Guillen).

## How it appears across sources

| Source | Role |
|---|---|
| [[expectations/synthesis/breakeven_inflation_information (Vicente & Guillen, 2013)]] | Model-free test of the BEIR as a forecast by horizon on Brazilian Treasury curves, April 2005 to July 2010: unbiased at 3 and 6 months, uninformative at 12 and 18, negative at 24 and 30 (Tables 2–4) |
| [[expectations/synthesis/brazil_taming_inflation_expectations (Bevilaqua, Mesquita & Minella, 2007)]] | Inflation-linked bonds set aside as a source of expectations because of low liquidity at policy-relevant horizons; the survey is used instead |
| [[expectations/synthesis/empirical_findings_expectations_brazil (Gaglianone, 2017)]] | Decomposition into expected inflation, inflation risk premium, liquidity premium and convexity (Vicente and Graminho, Jan/2006–Sep/2013: the last two below 1 basis point at 12 months); mixed record against Focus as a forecast; smoother survey series attributed to the risk premium in the market one |
| [[expectations/synthesis/formation_expectations_phillips_curve (Coibion, Gorodnichenko & Kamdar, 2018)]] | US market measures (TIPS break-evens, inflation swaps): high frequency, but confounded by inflation risk and liquidity premia, short histories and the TIPS three-month indexation lag |

## BRL / application to the current analysis

The sources are about Brazil: the NTN-B market in 2005–2010, where the BEIR forecast inflation well only at horizons of 6 months or less, with a large constant at longer horizons that the authors read as a high reward for holding inflation-linked bonds. Whether this holds in a later, deeper market, the sources do not say.

## Connections

- [[term_premium]] — the inflation risk premium inside the BEIR is a component of the compensation for risk in nominal yields
- [[inflation_expectations_anchoring]] — long-horizon break-even inflation is one of the measures used to test anchoring (its de-linking from news)
- [[expectations/synthesis/breakeven_inflation_information (Vicente & Guillen, 2013)]] — the forecasting test of the BEIR on Brazilian data
- [[expectations/synthesis/brazil_taming_inflation_expectations (Bevilaqua, Mesquita & Minella, 2007)]] — why the BCB relied on the survey rather than on inflation-linked bonds in the early 2000s
- [[expectations/synthesis/empirical_findings_expectations_brazil (Gaglianone, 2017)]] — the decomposition of break-even inflation and its forecasting record in Brazilian studies
- [[expectations/synthesis/formation_expectations_phillips_curve (Coibion, Gorodnichenko & Kamdar, 2018)]] — why market measures are a weak substitute for firms' expectations in Phillips curves
