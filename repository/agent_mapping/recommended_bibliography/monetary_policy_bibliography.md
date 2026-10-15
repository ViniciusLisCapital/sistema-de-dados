# Monetary Policy — Consolidated Bibliography

**Purpose:** the consolidated list of the technical literature the monetary-policy agent needs —
every source, acquired or not, with what it contributes to the agent and whether it has reached the
vault. It is the curation file the vault points to (`obsidian/CLAUDE.md`, "The conceptual map is a
contract"): what exists, what was ingested, what is still missing.

**Relation to the neighbour file:** `monetary_policy_bibliography_candidates.md` is the
*acquisition tracker* — only what is still to be sourced, with priority, suggested filename and where
to get it, plus the extraction quirks of the PDFs already in hand. This file is the *list*. A source
appears here whether or not its PDF exists; the `PDF` column says which.

**Scope:** technical literature only (papers, handbook chapters, selected textbook chapters). The
Copom's own documents (comunicados, atas, RPM) are a separate track — §8 of the candidates file —
already in `obsidian/monetary_policy/clean_md/central_bank/`, refreshed by the Copom ETL, and not
listed here.

**Cluster numbering follows the candidates file**, which other areas cite by number (e.g. the fiscal
bibliography's boundary note on cluster 7). Clusters 9-13 were added on 2026-10-07, after a review of
what the agent has to answer every memo (see below); cluster 8 is the Copom track and has no rows
here.

**Foundational score:** 1-5, as defined in `BIBLIOGRAPHY_METHODOLOGY.md` §c — canonicity, not
recency.

**Status columns:** `PDF` — ✓ in `repository/monetary_policy/raw_pdf/theorical_literature/`, ✗ not
acquired. `Vault` — ✓ when `clean_md` exists in `obsidian/monetary_policy/clean_md/`. A ⚠ in either
column points to a note in the candidates file (bad text layer, manual download needed).

**Count (2026-10-07):** 55 sources across 12 literature clusters, plus 3 primary legal sources.
40 acquired (46 PDF files — Galí 2015 is 7 chapter files), 1 in the vault (BIS 2026), 15 still to
be acquired.

---

## What the agent has to answer, and which clusters answer it

The review that produced clusters 9-13 started from the agent's job rather than from the field's
table of contents. The memo horizons are the next meeting, year-end, 1 year and 2-3 years
(`SISTEMA_AGENTES.md` I.III), and the exchange-rate map already asks the agent for four outputs:

| Agent question | Clusters |
|---|---|
| S1 — expected Selic path and balance of risks; how far it sits from the curve and from the Focus | 9, 12, 13 |
| S2 — is a hike read as credibility or as validation of higher inflation? | 10, 7 |
| S3 — how the Copom described the exchange rate | 11 (reading the documents themselves is §8) |
| S4 — reaction function to a depreciation, and with which instrument | 9, 6 |
| How restrictive is the Selic today? | 12, 7 |
| How, and how fast, does the Selic reach activity and inflation in Brazil? | 4, 7 |

Clusters 1-3 and 5 are the theoretical floor under all of these. Before 2026-10-07 the base was
strong there and thin on every row of the table above; the Brazil cluster stopped in 2006.

---

## 1. `#policy_rules_and_credibility` — rules vs. discretion, time inconsistency, institutional design

| Source | Type | Score / Year | What it gives the agent | PDF | Vault |
|---|---|---|---|---|---|
| Friedman, M. (1968), "The Role of Monetary Policy," *AER* | Paper | 5 / 1968 | Natural rate; what monetary policy can and cannot do | ✓ | ✗ |
| Kydland, F. & Prescott, E. (1977), "Rules Rather than Discretion," *JPE* | Paper | 5 / 1977 | Time inconsistency: discretion produces inflation bias | ✓ | ✗ |
| Barro, R. & Gordon, D. (1983), "A Positive Theory of Monetary Policy in a Natural Rate Model," *JPE* | Paper | 5 / 1983 | The workhorse inflation-bias model | ✓ | ✗ |
| Rogoff, K. (1985), "The Optimal Degree of Commitment to an Intermediate Monetary Target," *QJE* | Paper | 5 / 1985 | The conservative central banker | ✓ | ✗ |
| Taylor, J. (1993), "Discretion versus Policy Rules in Practice," *Carnegie-Rochester* | Paper | 5 / 1993 | The Taylor rule | ✓ | ✗ |
| Walsh, C. (1995), "Optimal Contracts for Central Bankers," *AER* | Paper | 5 / 1995 | Inflation bias solved by a performance contract | ✓ ⚠ | ✗ |

## 2. `#new_keynesian_transmission` — the modern theoretical backbone

| Source | Type | Score / Year | What it gives the agent | PDF | Vault |
|---|---|---|---|---|---|
| Calvo, G. (1983), "Staggered Prices in a Utility-Maximizing Framework," *JME* | Paper | 5 / 1983 | The microfoundation of price stickiness | ✓ | ✗ |
| Clarida, R., Galí, J. & Gertler, M. (1999), "The Science of Monetary Policy," *JEL* | Paper | 5 / 1999 | The 3-equation NK model as the standard framework | ✓ ⚠ | ✗ |
| Galí, J. (2015), *Monetary Policy, Inflation, and the Business Cycle*, 2nd ed., ch. 2-8 | Textbook chapters | 5 / 2015 | Ch. 3-4 are the core (basic NK model, policy design); ch. 5 discretion vs. commitment; ch. 8 open economy; ch. 2, 6, 7 are supporting | ✓ (7 files) | ✗ |
| Galí, J. & Monacelli, T. (2005), "Monetary Policy and Exchange Rate Volatility in a Small Open Economy," *REStud* | Paper | 5 / 2005 | The open-economy NK model; bridge to exchange rate | ✓ | ✗ |

## 3. `#inflation_targeting_regimes`

| Source | Type | Score / Year | What it gives the agent | PDF | Vault |
|---|---|---|---|---|---|
| Svensson, L. (1997), "Inflation Forecast Targeting," *EER* | Paper | 5 / 1997 | Forecast targeting — the Copom's own logic: the projection at the relevant horizon decides the rate | ✓ | ✗ |
| Mishkin, F. (2000), "Inflation Targeting in Emerging Market Countries," NBER WP 7618 | Paper | 4 / 2000 | IT under EM conditions (pass-through, weaker institutions) | ✓ | ✗ |
| Svensson, L. (2010), "Inflation Targeting," *Handbook of Monetary Economics* vol. 3B | Handbook chapter | 4 / 2010 | The mature version of the 1997 paper: flexible IT, horizon, communication of the projected path | ✗ | ✗ |

## 4. `#transmission_channels_financial_frictions`

| Source | Type | Score / Year | What it gives the agent | PDF | Vault |
|---|---|---|---|---|---|
| Bernanke, B. & Blinder, A. (1988), "Credit, Money, and Aggregate Demand," *AER* | Paper | 4 / 1988 | The bank-lending channel | ✓ | ✗ |
| Bernanke, B. & Gertler, M. (1995), "Inside the Black Box," *JEP* | Paper | 5 / 1995 | The credit channel, accessible statement | ✓ | ✗ |
| Bernanke, B., Gertler, M. & Gilchrist, S. (1999), "The Financial Accelerator in a Quantitative Business Cycle Framework," *Handbook of Macroeconomics* 1C | Handbook chapter | 5 / 1999 | Balance-sheet amplification of policy | ✓ ⚠ | ✗ |
| Havranek, T. & Rusnak, M. (2013), "Transmission Lags of Monetary Policy: A Meta-Analysis," *IJCB* | Paper | 3 / 2013 | How long the Selic takes to reach prices — the basis for the "relevant horizon" and the memo's 1-year and 2-3-year horizons | ✗ | ✗ |

## 5. `#unconventional_policy_zlb`

Lowest processing priority of the base: Brazil came near the floor only in 2020.

| Source | Type | Score / Year | What it gives the agent | PDF | Vault |
|---|---|---|---|---|---|
| Krugman, P. (1998), "It's Baaack," *BPEA* | Paper | 5 / 1998 | The liquidity trap revived | ✓ | ✗ |
| Eggertsson, G. & Woodford, M. (2003), "The Zero Bound on Interest Rates and Optimal Monetary Policy," *BPEA* | Paper | 5 / 2003 | Optimal policy at the ZLB; origin of forward guidance as a tool | ✓ | ✗ |
| Bernanke, B., Reinhart, V. & Sack, B. (2004), "Monetary Policy Alternatives at the Zero Bound," *BPEA* | Paper | 4 / 2004 | The menu of alternatives later used in 2008-15 | ✓ | ✗ |
| Gertler, M. & Karadi, P. (2011), "A Model of Unconventional Monetary Policy," *JME* | Paper | 4 / 2011 | Central-bank balance-sheet policy | ✓ | ✗ |

## 6. `#global_spillovers_em_autonomy`

| Source | Type | Score / Year | What it gives the agent | PDF | Vault |
|---|---|---|---|---|---|
| Rey, H. (2013), "Dilemma not Trilemma," Jackson Hole | Paper | 5 / 2013 | The global financial cycle limits EM autonomy even under a float | ✓ | ✗ |
| Obstfeld, M. (2015), "Trilemmas and Trade-offs," BIS WP 480 | Paper | 4 / 2015 | The counterpoint: floating plus tools still buys autonomy | ✓ | ✗ |
| Miranda-Agrippino, S. & Rey, H. (2020), "U.S. Monetary Policy and the Global Financial Cycle," *REStud* | Paper | 4 / 2020 | Quantifies the Fed's spillover | ✓ | ✗ |
| Kalemli-Özcan, Ş. (2019), "U.S. Monetary Policy and International Risk Spillovers," Jackson Hole | Paper | 4 / 2019 | The Fed reaches EMs through the risk premium, not the rate differential — the channel that makes UIP fail in the BRL | ✗ | ✗ |
| Ostry, J., Ghosh, A. & Chamon, M. (2012), "Two Targets, Two Instruments," IMF SDN 12/01 | Paper | 4 / 2012 | Rate vs. FX intervention under IT: the instrument choice in S4. Coordinate with the exchange-rate bibliography, which owns the capital-controls side | ✗ | ✗ |
| Tambakis, D. & Tarashev, N. (2012), "Systematic Monetary Policy and the Forward Premium Puzzle," BIS WP 396 | Paper | 3 / 2012 | The policy rule as an explanation of UIP failure — shared with exchange rate | ✓ | ✗ |
| Bank for International Settlements (2026), "Monetary policy transmission to exchange rates: the role of currency carry trades," BIS Bulletin 124 | Paper | 3 / 2026 | Policy → FX through carry positioning | ✓ | ✓ |

## 7. `#brazil_monetary_policy`

| Source | Type | Score / Year | What it gives the agent | PDF | Vault |
|---|---|---|---|---|---|
| Bogdanski, J., Tombini, A. & Werlang, S. (2000), "Implementing Inflation Targeting in Brazil," BCB WP 1 | Paper | 5 / 2000 | The regime's founding design | ✓ | ✗ |
| Minella, A. et al. (2002), "Inflation Targeting in Brazil: Lessons and Challenges," BCB WP 53 | Paper | 4 / 2002 | The regime's early progress report | ✓ | ✗ |
| Minella, A. et al. (2003), "Inflation Targeting in Brazil: Constructing Credibility under Exchange Rate Volatility," *JIMF* | Paper | 5 / 2003 | Credibility built through the 2002 FX shock; an early estimated reaction function | ✓ | ✗ |
| Blanchard, O. (2004), "Fiscal Dominance and Inflation Targeting: Lessons from Brazil," NBER WP 10389 | Paper | 5 / 2004 | When a hike depreciates the BRL through the fiscal/risk channel | ✓ | ✗ |
| Favero, C. & Giavazzi, F. (2004), "Inflation Targeting and Debt: Lessons from Brazil," NBER WP 10390 | Paper | 4 / 2004 | The empirical companion to Blanchard | ✓ | ✗ |
| Arida, P., Bacha, E. & Lara-Resende, A. (2005), "Credit, Interest, and Jurisdictional Uncertainty: Conjectures on the Case of Brazil," in Giavazzi, Goldfajn & Herrera (eds.), *Inflation Targeting, Debt, and the Brazilian Experience*, MIT Press | Book chapter | 4 / 2005 | The classic thesis on why Brazil's rates are so high. Same volume holds the published versions of Blanchard and Favero-Giavazzi | ✗ | ✗ |
| Muinhos, M. & Nakane, M. (2006), "Comparing Equilibrium Real Interest Rates," BCB WP 101 | Paper | 3 / 2006 | Early Brazil neutral-rate estimates; superseded on the level by cluster 12 | ✓ | ✗ |
| de Castro, M., Gouvea, S., Minella, A., Santos, R. & Souza-Sobrinho, N. (2011), "SAMBA: Stochastic Analytical Model with a Bayesian Approach," BCB WP 239 (+ the updated version, BCB WP 578) | Paper | 4 / 2011 | The BCB's own DSGE: fiscal surplus target, administered prices, external finance | ✗ | ✗ |
| Minella, A. & Souza-Sobrinho, N. (2013), "Monetary Policy Channels in Brazil through the Lens of a Semi-Structural Model," *Economic Modelling* (BCB WP 181, 2009) | Paper | 4 / 2013 | Splits Brazil's transmission into household rate, firm rate and FX channels; same family as the model `analytics/brasil/structural_model/` replicates | ✓ | ✗ |
| Kohlscheen, E. (2014), "The Impact of Monetary Policy on the Exchange Rate: A High Frequency Exchange Rate Puzzle in Emerging Economies," *JIMF* (BCB WP 259, 2011) | Paper | 3 / 2014 | Brazil's own evidence for S2: on decision days a hike does not appreciate the BRL | ✓ | ✗ |
| Bonomo, M. & Martins, B. (2016), "The Impact of Government-Driven Loans in the Monetary Transmission Mechanism," BCB WP 419 | Paper | 3 / 2016 | Earmarked credit weakens the credit channel — the "half-power" of the Selic | ✗ | ✗ |

## 9. `#reaction_function_and_gradualism` — estimating what the central bank responds to, and how fast

| Source | Type | Score / Year | What it gives the agent | PDF | Vault |
|---|---|---|---|---|---|
| Brainard, W. (1967), "Uncertainty and the Effectiveness of Policy," *AER P&P* | Paper | 5 / 1967 | Parameter uncertainty makes the optimal response smaller — the root of gradualism | ✗ | ✗ |
| Clarida, R., Galí, J. & Gertler, M. (2000), "Monetary Policy Rules and Macroeconomic Stability: Evidence and Some Theory," *QJE* | Paper | 5 / 2000 | The template for estimating a forward-looking reaction function with smoothing; the Taylor principle as a stability condition (S4) | ✓ ⚠ | ✗ |
| Orphanides, A. (2001), "Monetary Policy Rules Based on Real-Time Data," *AER* | Paper | 5 / 2001 | A rule evaluated with revised data is not the rule the central bank followed; real-time output-gap error. The BCB-vs-market gap divergence in the QPC | ✓ ⚠ | ✗ |
| Woodford, M. (2003), "Optimal Interest-Rate Smoothing," *REStud* | Paper | 4 / 2003 | Why moving in small, predictable steps is optimal under commitment — the Copom's step sizes | ✗ | ✗ |

## 10. `#policy_surprises_and_information_effect` — what a decision tells the market

| Source | Type | Score / Year | What it gives the agent | PDF | Vault |
|---|---|---|---|---|---|
| Christiano, L., Eichenbaum, M. & Evans, C. (1999), "Monetary Policy Shocks: What Have We Learned and to What End?," *Handbook of Macroeconomics* 1A | Handbook chapter | 5 / 1999 | VAR identification of policy shocks; the benchmark impulse responses | ✗ | ✗ |
| Romer, C. & Romer, D. (2004), "A New Measure of Monetary Shocks: Derivation and Implications," *AER* | Paper | 5 / 2004 | Separating the policy decision from the central bank's forecast | ✗ | ✗ |
| Gürkaynak, R., Sack, B. & Swanson, E. (2005), "Do Actions Speak Louder Than Words?," *IJCB* | Paper | 5 / 2005 | Two factors in a decision's surprise: the rate and the path signalled. Template for reading the DI curve on a Copom day | ✗ | ✗ |
| Nakamura, E. & Steinsson, J. (2018), "High-Frequency Identification of Monetary Non-Neutrality: The Information Effect," *QJE* | Paper | 5 / 2018 | A hike can carry news about the central bank's view of the economy — the theory behind S2 | ✓ | ✗ |
| Jarociński, M. & Karadi, P. (2020), "Deconstructing Monetary Policy Surprises — The Role of Information Shocks," *AEJ: Macro* | Paper | 4 / 2020 | Separates pure policy shocks from information shocks by the sign of the stock-market reaction — a method the agent can apply to S2 | ✓ | ✗ |

## 11. `#communication_and_forward_guidance`

| Source | Type | Score / Year | What it gives the agent | PDF | Vault |
|---|---|---|---|---|---|
| Blinder, A., Ehrmann, M., Fratzscher, M., de Haan, J. & Jansen, D.-J. (2008), "Central Bank Communication and Monetary Policy: A Survey of Theory and Evidence," *JEL* | Paper | 5 / 2008 | Why and how communication moves expectations; what evidence there is | ✓ | ✗ |
| Campbell, J., Evans, C., Fisher, J. & Justiniano, A. (2012), "Macroeconomic Effects of Federal Reserve Forward Guidance," *BPEA* | Paper | 5 / 2012 | Delphic (forecast) vs. Odyssean (commitment) guidance — the distinction for reading the Copom's guidance language | ✓ | ✗ |

## 12. `#neutral_rate` — how restrictive is the policy rate?

| Source | Type | Score / Year | What it gives the agent | PDF | Vault |
|---|---|---|---|---|---|
| Laubach, T. & Williams, J. (2003), "Measuring the Natural Rate of Interest," *REStat* | Paper | 5 / 2003 | The canonical r* estimation method (Kalman filter on IS and Phillips curve) | ✓ | ✗ |
| Holston, K., Laubach, T. & Williams, J. (2017), "Measuring the Natural Rate of Interest: International Trends and Determinants," *JIE* | Paper | 4 / 2017 | The same method across countries; the global r* decline | ✓ | ✗ |
| Segura-Ubiergo, A. (2012), "The Puzzle of Brazil's High Interest Rates," IMF WP 12/62 | Paper | 3 / 2012 | Why Brazil's neutral rate is so high: savings, fiscal position, credit segmentation, indexation | ✗ ⚠ | ✗ |
| Perrelli, R. & Roache, S. (2014), "Time-Varying Neutral Interest Rate — The Case of Brazil," IMF WP 14/84 | Paper | 3 / 2014 | A time-varying neutral for Brazil from several models, and what getting it wrong does to the policy prescription | ✗ ⚠ | ✗ |

## 13. `#term_structure_and_market_pricing` — separating the expected path from the premium

| Source | Type | Score / Year | What it gives the agent | PDF | Vault |
|---|---|---|---|---|---|
| Adrian, T., Crump, R. & Moench, E. (2013), "Pricing the Term Structure with Linear Regressions," *JFE* | Paper | 4 / 2013 | Term-premium decomposition; without it, the Selic path implied by the DI curve carries the premium (S1) | ✗ | ✗ |

---

## Primary legal sources (institutional framework)

Not literature, and therefore outside the clusters, but they define the target the reaction function
responds to. Same treatment as the legal sources in the fiscal bibliography.

| Source | What it gives the agent | PDF |
|---|---|---|
| Decreto nº 3.088/1999 | Adoption of the inflation-targeting regime | ✗ |
| Lei Complementar nº 179/2021 | BCB autonomy, fixed mandates, and the secondary mandate (smooth activity, foster full employment) | ✗ |
| Decreto nº 12.079/2024 | The continuous target (from 2025): breach means six consecutive months outside the band | ✗ |

---

## Deliberately out of this list

- **Woodford (2003) *Interest and Prices*, Cukierman (1992) and Bernanke, Laubach, Mishkin & Posen
  (1999)** — the three books the candidates file used to carry. Their content for this agent is
  already covered: Woodford by Galí and Clarida-Galí-Gertler, Cukierman by Rogoff, Walsh and
  Barro-Gordon, Bernanke et al. by Svensson, Mishkin and the Brazil papers. Dropped 2026-10-07.
- **Phillips curve, expectation formation, fiscal theory of the price level, output-gap filters** —
  owned by the inflation, fiscal and activity bibliographies. Expectations are not this agent's
  (`SISTEMA_AGENTES.md` I.III.xii); duplicating them here would blur the agents.
</content>
