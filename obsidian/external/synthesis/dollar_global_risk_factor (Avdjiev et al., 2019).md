---
aliases: ["Avdjiev 2019 - The Dollar Exchange Rate as a Global Risk Factor"]
---

# The Dollar Exchange Rate as a Global Risk Factor: Evidence from Investment — Stefan Avdjiev, Valentina Bruno, Catherine Koch & Hyun Song Shin 2018

**Type:** paper
**Tags:** #dollar #financial-channel #exchange-rates #cross-border-bank-lending #investment #emerging-markets #panel-var
**Source:** BIS Working Papers No 695, Monetary and Economic Department, Bank for International Settlements (January 2018); paper prepared for the IMF 18th Jacques Polak Annual Research Conference
**Language:** English
**Source file:** [[external/clean_md/dollar_global_risk_factor (Avdjiev et al., 2019)]]

---

## Context and motivation

Open-economy macro models carry one channel from the exchange rate to activity: net exports, under which a weaker domestic currency stimulates output. With deeper financial integration a second channel has become prominent — exchange rate moves change the value of balance sheets and the risk-taking capacity of lenders — and it often points the other way. The empirical regularity behind it: when the dollar depreciates against a country's currency, residents of that country borrow more in dollars. Earlier BIS work documented the price side (sovereign spreads fall when a currency appreciates) and part of the quantity side (a stronger dollar contracts dollar cross-border bank lending). The open question this paper addresses is whether the chain reaches the real economy: does a stronger dollar lower **real investment** in emerging market economies (EMEs), and which exchange rate — trade-weighted, bilateral against the dollar, or the broad dollar index — matters for it?

## Core argument / thesis

There is a "triangular" relationship between (i) the strength of the dollar, (ii) dollar-denominated cross-border bank flows and (iii) real investment in EMEs. A stronger dollar weakens currency-mismatched borrowers, which shrinks dollar bank credit to them, which lowers investment. The financial channel therefore runs opposite to the trade channel: a stronger dollar "dampens economic activity, rather than stimulating it". And the exchange rate that matters most is the **broad dollar index**, not the bilateral rate, because what drives the effect is mainly the supply of dollar credit by global banks, which depends on the dollar's value against all borrowers at once, rather than the demand for credit by any one country's borrowers.

## Key mechanisms / model

Three exchange rate concepts, each with its own channel:

1. **Trade-weighted rate** — the Mundell-Fleming net-exports channel.
2. **Bilateral rate against the dollar** — imports priced in dollars (the dominant-currency literature), and **credit demand**: a borrower with local-currency assets and dollar liabilities loses net worth when the dollar strengthens, and demands less credit (the EME-crisis literature). This holds even if assets yield dollar cash flows, because debt service rises (the authors' example: oil firms).
3. **Broad dollar index** — **credit supply** (the "risk-taking channel of currency appreciation" of Bruno and Shin): a stronger dollar worsens the credit position of all currency-mismatched dollar borrowers at once, raising tail risk in global banks' diversified dollar loan books. With a fixed exposure limit (value-at-risk or economic capital constraint), the bank has less capacity to lend. A weaker dollar works in reverse, flattering borrowers' balance sheets and freeing lending capacity.

On the demand side the regularity has a second source: exporters with dollar receivables, or asset managers with dollar assets and local-currency obligations, hedge more aggressively — borrowing in dollars — when they expect the dollar to depreciate.

What carries the result is **currency mismatch** on borrowers' balance sheets and a **risk-sensitive lending constraint** at global banks. Without mismatch, the dollar's value would not move borrowers' net worth; without the value-at-risk constraint, banks would not cut supply when tail risk rises. A third condition matters for the sign at the firm level: the firm must depend on external finance and not earn the competitiveness gain of a weaker local currency (the tradable sector does).

**Empirical design.**
- **Macro:** a structural panel VAR (SPVAR) for 34 EMEs, quarterly, Q2 2001–Q3 2016, with country fixed effects, estimated in first differences by Arellano-Bond GMM. Five endogenous variables in Cholesky order: US interest rate (Fed funds, then Krippner's shadow rate from 2008), dollar cross-border bank flows (BIS locational banking statistics), gross fixed capital formation, the dollar exchange rate, and the VIX. Cross-border lending is ordered ahead of the dollar, which rules out a contemporaneous effect of the dollar on lending and so "tilt[s] the odds against" the hypothesis.
- **Micro:** OLS panel of firm capital expenditure over total assets for non-financial firms in 32 EMEs, annual, 2000–2015 (Capital IQ), on the change in the bilateral dollar rate and on the component of the broad dollar index orthogonal to it, each interacted with the Rajan-Zingales industry index of external financial dependence (FINDEP), with firm controls and country, year, industry or country-year fixed effects. The sharpest tests use firms in non-tradable sectors in countries with floating regimes, where the trade channel should be absent.

## Main results / findings

The evidence supports the chain at each link and the sign reversal relative to the trade channel.

- **Macro, three links.** A dollar appreciation lowers dollar cross-border bank lending; more such lending raises investment; and a dollar appreciation lowers investment. Full sample: a one-standard-deviation dollar appreciation against the local currency lowers the growth of gross capital formation by five percentage points in the next quarter, significant for more than two years (Figure 1). US tightening and VIX spikes also cut both lending and investment, with longer contractions after US tightening (Figure 2), which the authors read as further evidence of the channel since US policy moves the dollar more persistently.
- **Supply beats demand.** With the broad dollar index in place of the bilateral rate, the investment response is similar, but the effect of cross-border lending on investment lasts much longer instead of being significant only on impact (Figure 3 vs Figure 1) — read as the global credit-supply channel being stronger and more persistent than the local credit-demand channel.
- **Stable over time.** The investment response appears in every subsample, somewhat larger and longer before the crisis (peak about -6%, roughly two years) than after (peak about -4.5%, about a year); after 2012 still about -4% and significant for several quarters (Figure 4).
- **Firm level, two exchange rates with opposite signs.** Full sample, 2000–2015 (Table 2): a dollar appreciation against the local currency **raises** capex (0.0168) — the textbook competitiveness channel — while the orthogonal broad-dollar component **lowers** it (-0.1598); both hold when entered together. In non-tradable firms in floating-regime countries (Table 3), the bilateral rate turns insignificant, the broad-dollar component stays negative (-0.3043), and the bilateral rate interacted with FINDEP is negative (-0.0208): a one percentage point bilateral dollar appreciation lowers the capex ratio by 0.003 (5.5% of the sample mean) more at the 66th than at the 33rd percentile of FINDEP. Run one at a time without year effects, the broad index's coefficient is about four times the bilateral rate's (-0.09 vs -0.021, footnote 6). The authors' reading: on average the global supply effect dominates, and the local demand effect shows up among firms that need outside funds.
- **Where the firm-level effect lives** (Table 4): the FINDEP interaction is driven by the post-2011 period, when EME corporate dollar borrowing rose (-0.0219, significant; pre-2011 insignificant), and by emerging Asia (-0.0591), not emerging Europe (0.0250, insignificant).
- **Robustness.** Adding a Bloomberg EME carry-trade index ordered second — the alternative story in which carry trades both weaken the dollar and push flows into EMEs — leaves the three links intact (Figure 5). Ordering the dollar ahead of lending and investment makes the lending contraction deeper and more persistent (Figures 6–7). Alternative dollar indices (Fed EME index, correlation 0.87 with the NEER; own GDP-weighted EME index, 0.44), the micro-study and floating-regime country sets, end-of-quarter rates, and global GDP in place of the VIX (smaller but still significant and persistent) all keep the result (Figures 8–13). Firm-level results survive controls for gross savings, external loans, US rates and VIX interacted with FINDEP, bank debt, a finer financial-dependence index, country-year and industry-year effects, excluding the crisis, and Tobin's Q (Tables 5–6).
- **Net effect on output.** Replacing investment with GDP growth, a dollar appreciation against the local currency sharply lowers GDP growth; after a one-quarter reversal the effect is negative and significant for at least another year (Figure 14). This is the basis for the claim that the financial channel dominates the trade channel in overall activity.
- **What does not fit.** The savings channel works opposite to the financial channel among externally dependent firms (Table 5), and footnote 5 reports, without showing it, that tradable-sector firms invest more after a dollar appreciation.

## Limitations and caveats

- Identification rests on recursive (Cholesky) orderings and Arellano-Bond GMM; the authors address reverse causality through carry trades and through reordering, not through an external instrument for dollar shocks.
- The bilateral-vs-broad split is inferred: demand and supply channels are mapped to the two indices, not measured separately. The broad-dollar effect at the firm level uses the component orthogonal to the bilateral rate, and its interaction with FINDEP is insignificant (Table 3), so the supply effect is not shown to vary with firms' financing needs.
- The firm-level result is concentrated in post-2011 and in emerging Asia; it is not significant in emerging Europe or before 2011. It needs currency mismatch: the mechanism predicts nothing for borrowers that hedge or borrow in local currency, and the opposite sign for tradable-sector firms.
- The claim that the financial channel dominates the trade channel in overall activity rests on one figure (Figure 14, GDP growth instead of investment, 29 EMEs), with a one-quarter reversal; the tradable-sector result (footnote 5) and the full broad-dollar specification (footnote 4) are "available upon request" and not in the file.
- Date and metadata: the file is BIS Working Paper No 695, dated January 2018; the file name and tracker give 2019. The text says the macro data run to Q4 2016, while every figure and Table 1 say Q3 2016. Table 6's header labels column 3 "Excl 2008–2011", while its note says it excludes 2008-2010.
- Damaged passages: equations (1)–(8) (the SPVAR, its first-difference and moving-average forms, the impulse responses, and the three firm-level regressions) are OCR'd into unreadable glyphs; the models are described above only from the surrounding text. Figures 1–14 survive as captions and axis tick values only, so impulse-response magnitudes come from the text, not the charts. In Table 1, CAPEX/TA shows a mean (0.620) above its own 99th percentile (0.419), so that row is not usable as printed. Table 6 column 2's constant has a standard error of 234.6837. The page numbering jumps from 37 (Annex A) to 41, so the reference list is not in the file; the BIS series list at the end remains.

## Connections

- [[financial_channel_exchange_rate]] — the source's subject: the balance-sheet and lender risk-taking channel through which a stronger dollar contracts dollar credit and EME investment, opposite to net exports
- [[global_financial_cycle]] — US policy and the VIX as drivers of cross-border bank lending and EME investment; the dollar's value as the price that transmits global bank risk-taking to EMEs
- [[carry_trade]] — tested as the alternative explanation (carry flows both weakening the dollar and feeding EME credit) and found not to overturn the result
- [[exchange_rate/synthesis/us_policy_international_risk_spillovers (Kalemli-Ozcan, 2019)]] — the same balance-sheet effect of depreciation on dollar debt, there as one term of a framework for US spillovers through EME risk premia
- [[monetary_policy/synthesis/trilemma_tradeoffs (Obstfeld, 2015)]] — offshore dollar credit as a transmission of US funding conditions to non-dollar balance sheets; this source measures its effect on investment
- [[monetary_policy/synthesis/dilemma_not_trilemma (Rey, 2013)]] — the global cycle in cross-border credit and the VaR-constrained global bank that this source puts at the end of a dollar shock
- [[exchange_rate/synthesis/output_exchange_rates_sr (Krugman, 2023)]] — the textbook trade channel (depreciation raises demand) whose sign this source finds reversed for EME investment and GDP
- [[verde_fx_mental_models]] — §4.2 (Fed cycle drives the global dollar cycle and capital to EM): the source traces the same US-rate and dollar shocks to cross-border lending and EME investment
