---
aliases: ["Takami 2018 - Short-Term Drivers of Sovereign CDS Spreads"]
---

# Short-Term Drivers of Sovereign CDS Spreads — Marcelo Yoshio Takami 2018

**Type:** paper
**Tags:** #sovereign-risk #cds #global-factors #emerging-markets #credit-risk
**Source:** Banco Central do Brasil, Working Paper Series no. 475, April 2018
**Language:** English
**Source file:** [[fiscal_policy/clean_md/short_term_drivers_sovereign_cds (Takami, 2018)]]

---

## Context and motivation

Sovereign CDS spreads are a timely, market-based read on default risk — more frequent than rating changes and, in crises, arguably more accurate — and matter to a central bank managing the credit risk of its reserves. The literature disagrees on which determinants matter and tends to test one specification. The paper asks which combination of commonly used global and local drivers best explains **weekly changes** in 5-year sovereign CDS spreads, country by country, for 35 sovereigns (advanced and emerging), and whether the answer differs between the two groups. It is explicitly about statistical relationships for short-term risk assessment, not about the economic content of each variable, and not about predicting crises.

## Core argument / thesis

Short-term movements in sovereign credit spreads are driven mainly by global factors, above all the U.S. equity market: the S&P 500 is contemporaneously and negatively related to CDS spreads for most countries, and the sensitivity is larger for emerging markets than for advanced economies. Local variables matter only for some countries — the exchange rate in several commodity- or flow-dependent emerging markets, the local 2-year yield where rollover or credit risk was high. Contemporaneous-factor models fit and forecast better than pure time-series (ARMA) models, and lagged-factor models do worse than both.

## Key mechanisms / model

**The instrument.** The protection buyer pays a periodic spread; on a credit event (failure to pay, moratorium, restructuring) it can sell the bond at face value (physical settlement) or receive face value minus market value (cash settlement). The spread rises with the bond's expected loss. Reference obligation: senior dollar-denominated external debt.

**Candidate drivers and their expected signs (Table 3).** Global: S&P 500 (state of the global economy, negative), VIX (risk aversion, positive), U.S. 10y–3m slope (growth outlook, negative), Brent (global activity, negative). Local: stock index (negative), exchange rate (ambiguous — depreciation raises the burden of dollar debt but helps competitiveness), 2-year local yield (positive — weak growth prospects, difficulty attracting funding), local slope (negative), and the average CDS of domestic banks (positive — banking distress as a contingent liability of the sovereign). The lagged spread enters for persistence.

**Selection engine.** Weekly first differences, July 2005–July 2016; estimation to October 2012, the last 45 months held out. VIX, oil and the local stock index are orthogonalized to the S&P 500. Granger-causality tests classify each local variable as weakly exogenous, endogenous (feedback both ways — e.g., a rising CDS can itself cause depreciation through capital outflows) or ineligible; endogenous ones are instrumented with their first lag in GMM. The engine then tests every permutation of eligible variables (255 models for Italy) and keeps, per country, the model with at least one correctly signed variable significant at 10%, the highest adjusted R², and statistical superiority to every nested model.

**What carries the result:** the weekly frequency (which excludes fiscal fundamentals such as debt/GDP, deficits and reserves, available at best monthly), the orthogonalization (which credits the common global movement to the S&P 500 rather than to VIX or oil), and a sample dominated by "excess global liquidity, prevalence of carry trades and reaching for yield" (Longstaff et al., quoted by the author).

## Main results / findings

- **The S&P 500 is the pervasive driver:** significant in 22 out of 35 countries (Table 6), with larger coefficients for emerging markets. Reading the Italy coefficient of -0.025: a 1% weekly rise in the S&P 500 is consistent with a 2.5 bp fall in Italy's CDS. Brazil's coefficient is -0.048 (Table 6), among the larger ones.
- **Other global variables barely matter** once orthogonalized: VIX and the local slope are significant for no country; oil and the local stock index only for Austria and Australia (oil) and Russia (stock).
- **Local factors are secondary:** no local variable is a significant driver for 16 of the 35 countries, Brazil among them. The exchange rate is significant for Israel, Malaysia, South Africa, Mexico, Peru, Chile and Colombia, consistent with EM debt risk tied to capital flows and commodity prices; the local 2-year yield for Portugal, Italy, Russia, Poland, Hungary, Turkey and Colombia — rollover risk in the euro crisis, credit risk in the others.
- **Banking distress transmits as a break, not gradually.** Bank CDS is significant only for Hong Kong, Korea and China, where governments are seen as backstopping big banks; elsewhere the author conjectures that spillover from banks to the sovereign happens as a structural break, and that markets underpriced it before 2010–2012 expecting monetization, bail-in or bail-out by stronger sovereigns.
- **Fit is better for emerging markets** in-sample and out-of-sample (Theil's U1, U2, percent hit misses). Contemporaneous models beat ARMA and lagged-variable models almost everywhere; lagged models are even worse than ARMA.
- **Robustness:** dropping the sign criterion, replacing adjusted R² by forecast statistics, a 5% Granger cutoff and six sub-periods leave the two main claims standing, though coefficients, significance and country rankings move; no S&P 500 coefficient is significant in the two overlapping post-2010 sub-periods ("After Jul 2010", "Euro Crisis").

## Limitations and caveats

- **The author's:** the models need one-week-ahead forecasts of the global inputs to be used for prediction; the 2005–2016 sample reflects abundant global liquidity and carry, so the relations may not hold outside it; historical models may miss relationships "under unusual circumstances"; changing the instrument set has "unintended consequences" for which model is chosen.
- **What the text shows:** fiscal fundamentals are excluded by construction, so the paper says nothing about how debt or deficits price into spreads — only about weekly co-movement. The engine is a data-mining search with no economic restriction beyond expected signs, and the S&P 500's dominance is partly built in by orthogonalizing its competitors to it. Several selected models rest on few observations (Russia 96, Mexico 86, Chile 84 in Table 6). Rating column (Moody's, Sep/2016) and spread statistics describe that sample only.
- **Damaged passages:** equation (1) and the Granger and Ljung-Box equations are spread over lines with Greek letters and subscripts lost; the model count in footnote 5 is garbled. The column headers of Tables 6–12 and 14 (adjusted R², Theil's U, PHM) are broken into single characters, and because blank cells were collapsed, the column of each coefficient in rows with few entries cannot be read with certainty. In Tables 15–16 the same collapse leaves rows with fewer values than the six sub-period columns, so values cannot be assigned to sub-periods; the text's range for Russia (-0.073 to -0.028) does not match the Russia row as extracted (the -0.073 sits in the Turkey row). Figure 1 is a title only.

## Connections

- [[global_financial_cycle]] — weekly sovereign CDS changes across 35 countries load mainly on a global factor proxied by the S&P 500, with emerging markets more sensitive than advanced economies; local variables matter for fewer than half of the countries
- [[sovereign_cds_spreads]] — defines the contract (credit events, settlement, link to expected loss) and tests the candidate global and local short-term determinants with GMM, country by country
