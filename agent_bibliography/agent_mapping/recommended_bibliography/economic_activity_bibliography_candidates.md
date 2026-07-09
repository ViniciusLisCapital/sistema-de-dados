# Economic Activity — Bibliography Candidates

**Purpose:** first-pass candidate literature list for the economic activity agent, built following `BIBLIOGRAPHY_METHODOLOGY.md`. Nothing here has been acquired yet — this is the pre-acquisition step. Once a source is sourced into `agent_bibliography/economic_activity/` (naming convention: `topic_description (Author, Year).pdf`), process it into a new `economic_activity_conceptual_map.md`, one source at a time, following the same pattern used for `exchange_rate_conceptual_map.md`.

**Scope — deliberately excludes labor market theory.** The user is considering splitting labor market into its own future agent, separate from economic activity. This file covers **the business cycle and growth side only**: what drives aggregate output up and down over the short run (business cycle theory), what drives it higher over the long run (growth theory), how "how much slack is there" gets measured (output gap/potential output), and how Brazil's own activity is tracked and dated. It deliberately does **not** cover search/matching models, the Beveridge curve, or NAIRU estimation — those stay reserved for the future labor market agent, even though output gap and NAIRU are close conceptual cousins.

**Scope boundary with `monetary_policy_bibliography_candidates.md`:** monetary policy's `#new_keynesian_transmission` and `#transmission_channels_financial_frictions` clusters already own the monetary transmission mechanism (Calvo pricing, the credit channel, the financial accelerator) — this file covers business cycles from the *real/output* side (RBC theory, growth theory) rather than how monetary policy transmits into them. Cluster 2 below (`#modern_dsge_business_cycles`) is the one place the two files sit closest together — Smets & Wouters (2007) and the CEE (2005) model are joint output-inflation-policy frameworks — included here because the lens is business-cycle *propagation*, not the policy-rule side already covered in monetary policy's bibliography.

**Scope boundary with `inflation_bibliography_candidates.md`:** Phillips curve theory and estimation (the *use* of the output gap as a slack measure) stays in the inflation file's cluster 1 — this file owns the *theory and measurement of the output gap itself*, which the inflation and monetary policy agents both already list as a Tier 2 dependency they need from a future activity agent.

**Scope boundary with `exchange_rate_policy/` and inflation's cost-push cluster:** commodity-price pass-through to consumer prices stays with inflation (cluster 3); this file's commodity cluster (8) covers the structural growth/Dutch-disease channel — how a commodity cycle reshapes potential output and industrial competitiveness — not the price-transmission channel.

**Foundational score:** 1-5, defined in `BIBLIOGRAPHY_METHODOLOGY.md` §c.

36 literature candidates across 9 clusters. As with monetary policy and inflation, one cluster (7) is unusually Brazil-specific — IBC-Br is a genuinely distinctive piece of applied central-bank infrastructure (a monthly GDP proxy built specifically because Brazil, unlike most economies with monthly industrial-production data, lacked *any* single monthly activity gauge before 2010) — and cluster 6 includes CODACE, Brazil's own FGV/IBRE-run business cycle dating committee, as an ongoing primary-source reference rather than a single paper.

**2026-07 verification pass:** eight sources were added after a web search grounded specifically in "what material exists on Brazilian growth, business-cycle metrics, and productivity" — confirmed by fetching and reading the actual PDFs rather than relying on memory. Three are current-methodology BCB Estudos Especiais: the financial conditions index (EE076/2020), the economic-policy-uncertainty study (EE065/2019), and the labor-productivity study (EE027/2018). A follow-up pass added FGV/IBRE's own aggregate-TFP series for Brazil (Veloso, Matos & Peruchetti, 2020a/b) once BCB material alone turned out not to cover aggregate TFP — the two together close what was flagged as an open gap in the first pass. This pass also added a new cluster (9) specifically for Brazilian productivity, since productivity (the growth-accounting decomposition) is conceptually distinct from output-gap measurement (cluster 5) even though both feed into a potential-output read.

---

## 1. `#business_cycle_theory_foundations` — the impulse-propagation framework and its two founding schools

| Source | Type | Score / Year | Why | Suggested filename |
|---|---|---|---|---|
| Frisch, R. (1933), "Propagation Problems and Impulse Problems in Dynamic Economics," in *Economic Essays in Honour of Gustav Cassel* | Paper (book chapter) | 5 / 1933 | The founding impulse-propagation distinction — nearly a century later, every business cycle model (RBC, NK-DSGE) is still organized around "what are the shocks" and "what is the propagation mechanism" exactly as Frisch framed it | `propagation_impulse_problems (Frisch, 1933).pdf` |

| Slutsky, E. (1937), "The Summation of Random Causes as the Source of Cyclic Processes," *Econometrica* | Paper | 4 / 1937 | Companion founding result: shows that summing purely random shocks can generate apparently cyclical behavior — the statistical counterpart to Frisch's conceptual framework, and an early warning against reading business cycles as necessarily driven by a single recurring cause | `summation_random_causes (Slutsky, 1937).pdf` |

| Burns, A. & Mitchell, W. (1946), *Measuring Business Cycles*, National Bureau of Economic Research | Book | 5 / 1946 | The empirical/dating tradition — defines a business cycle as a recurring but not periodic sequence of expansion/contraction phases across many series, not a single output series crossing a threshold. Directly the methodological ancestor of NBER's own dating committee and of CODACE (cluster 6), Brazil's equivalent | `measuring_business_cycles (Burns & Mitchell, 1946).pdf` |

| Lucas, R. (1977), "Understanding Business Cycles," *Carnegie-Rochester Conference Series on Public Policy* | Paper | 5 / 1977 | Lucas's own manifesto for equilibrium business cycle theory — argues cycles should be explained as the equilibrium response of rational agents to shocks, not as market failure; the direct theoretical setup for Kydland-Prescott below. Distinct from Lucas's 1976 policy-evaluation critique already cited in the monetary policy and inflation bibliographies | `understanding_business_cycles (Lucas, 1977).pdf` |

| Kydland, F. & Prescott, E. (1982), "Time to Build and Aggregate Fluctuations," *Econometrica* | Paper | 5 / 1982 | THE founding Real Business Cycle (RBC) paper — shows technology shocks propagated through a time-to-build investment structure can generate realistic-looking business cycles without any nominal rigidity or policy failure | `time_to_build_aggregate_fluctuations (Kydland & Prescott, 1982).pdf` |

| Long, J. & Plosser, C. (1983), "Real Business Cycles," *Journal of Political Economy* | Paper | 4 / 1983 | The other founding RBC paper, published almost simultaneously with Kydland-Prescott — a multi-sector real model showing comovement across sectors from a common technology shock, without any money or nominal rigidity | `real_business_cycles (Long & Plosser, 1983).pdf` |

## 2. `#modern_dsge_business_cycles` — the medium-scale estimated models central banks actually run

| Source | Type | Score / Year | Why | Suggested filename |
|---|---|---|---|---|

| King, R. & Rebelo, S. (1999), "Resuscitating Real Business Cycles," in *Handbook of Macroeconomics*, Vol. 1B | Paper (handbook chapter) | 4 / 1999 | Standard survey/defense/critique of the pure RBC program after a decade of challenges — the natural bridge chapter between cluster 1's founding papers and the hybrid RBC-plus-nominal-rigidity models below | `resuscitating_rbc (King & Rebelo, 1999).pdf` |

| Christiano, L., Eichenbaum, M. & Evans, C. (2005), "Nominal Rigidities and the Dynamic Effects of a Shock to Monetary Policy," *Journal of Political Economy* | Paper | 5 / 2005 | The "CEE model" — habit formation, investment adjustment costs, variable capital utilization, and Calvo pricing combined into the workhorse medium-scale DSGE framework most later estimated models (including Smets-Wouters below) build on | `nominal_rigidities_dynamic_effects (Christiano, Eichenbaum & Evans, 2005).pdf` |

| Smets, F. & Wouters, R. (2007), "Shocks and Frictions in US Business Cycles: A Bayesian DSGE Approach," *American Economic Review* | Paper | 5 / 2007 | THE estimated DSGE model — the direct template for the "small-scale semi-structural models" BCB itself runs and periodically updates (see the RPM box "Atualização dos modelos semiestruturais de pequeno porte," June 2024) to jointly project output and inflation | `shocks_frictions_us_business_cycles (Smets & Wouters, 2007).pdf` |

## 3. `#growth_theory_neoclassical_and_endogenous` — what drives output higher over the long run

| Source | Type | Score / Year | Why | Suggested filename |
|---|---|---|---|---|

| Solow, R. (1956), "A Contribution to the Theory of Economic Growth," *Quarterly Journal of Economics* | Paper | 5 / 1956 | THE founding neoclassical growth model — diminishing returns to capital accumulation implies growth converges to a rate set by technology and population growth alone, not savings; still the baseline every later growth model is measured against | `contribution_theory_economic_growth (Solow, 1956).pdf` |

| Swan, T. (1956), "Economic Growth and Capital Accumulation," *Economic Record* | Paper | 4 / 1956 | Independent co-discoverer of the same model, published the same year — conventionally cited alongside Solow ("the Solow-Swan model") | `economic_growth_capital_accumulation (Swan, 1956).pdf` |

| Cass, D. (1965), "Optimum Growth in an Aggregative Model of Capital Accumulation," *Review of Economic Studies* | Paper | 4 / 1965 | Endogenizes the savings rate via intertemporal utility maximization (with Ramsey 1928 and Koopmans 1965) — the "Ramsey-Cass-Koopmans" model, the standard optimal-growth extension of Solow still taught in every graduate macro sequence | `optimum_growth_aggregative_model (Cass, 1965).pdf` |

| Romer, P. (1986), "Increasing Returns and Long-Run Growth," *Journal of Political Economy* | Paper | 5 / 1986 | The founding endogenous growth paper — knowledge/technology as an input with increasing returns, breaking Solow's diminishing-returns conclusion and making sustained growth from investment/R&D possible in the model itself | `increasing_returns_long_run_growth (Romer, 1986).pdf` |

| Lucas, R. (1988), "On the Mechanics of Economic Development," *Journal of Monetary Economics* | Paper | 5 / 1988 | The other founding endogenous growth paper — human capital accumulation as the engine of sustained growth, and the paper that popularized asking "why doesn't capital flow from rich to poor countries" (directly setting up cluster 4) | `mechanics_economic_development (Lucas, 1988).pdf` |

| Barro, R. & Sala-i-Martin, X. (2004, 2nd ed.), *Economic Growth*, MIT Press — **book, get relevant chapters** | Book | 5 / 2004 | The standard graduate growth textbook. Recommended: Ch. 1-2 (Solow model and its empirical fit) plus the endogenous growth chapters (Ch. 4-5) — confirm exact chapter numbers against the table of contents on acquisition | `economic_growth_selected_chapters (Barro & Sala-i-Martin, 2004).pdf` |

## 4. `#convergence_middle_income_trap_and_em_growth` — does growth converge, and why Brazil's own growth has repeatedly stalled

| Source | Type | Score / Year | Why | Suggested filename |
|---|---|---|---|---|

| Barro, R. (1991), "Economic Growth in a Cross Section of Countries," *Quarterly Journal of Economics* | Paper | 5 / 1991 | The founding cross-country growth regression — establishes "conditional convergence" (poorer countries grow faster only after controlling for human capital, institutions, etc.) as the standard empirical framework for comparing growth across countries | `economic_growth_cross_section (Barro, 1991).pdf` |

| Pritchett, L. (1997), "Divergence, Big Time," *Journal of Economic Perspectives* | Paper | 5 / 1997 | The essential counterpoint to naive convergence optimism — documents that the dominant historical pattern across the last century is *divergence* in absolute income levels, not convergence; a necessary corrective before reading any convergence-framed argument about Brazil | `divergence_big_time (Pritchett, 1997).pdf` |

| Eichengreen, B., Park, D. & Shin, K. (2012), "When Fast-Growing Economies Slow Down: International Evidence and Implications for China," *Asian Economic Papers* (also NBER Working Paper 16919) | Paper | 4 / 2012 | The empirical middle-income-trap/growth-slowdown paper — identifies the income level and conditions under which fast-growing economies systematically decelerate, directly applicable to reading Brazil's own post-2010 growth deceleration | `fast_growing_economies_slow_down (Eichengreen, Park & Shin, 2012).pdf` |

| Rodrik, D. (2013), "Unconditional Convergence in Manufacturing," *Quarterly Journal of Economics* | Paper | 4 / 2013 | Shows manufacturing productivity converges across countries even without aggregate convergence — a useful, more optimistic counter-lens for Brazil's industrial-competitiveness debates specifically, as opposed to the economy-wide pessimism of the middle-income-trap literature | `unconditional_convergence_manufacturing (Rodrik, 2013).pdf` |

## 5. `#output_gap_and_potential_output_measurement` — how "how much slack is there" actually gets estimated

| Source | Type | Score / Year | Why | Suggested filename |
|---|---|---|---|---|
| Okun, A. (1962), "Potential GNP: Its Measurement and Significance," Cowles Foundation Paper 190 | Paper | 5 / 1962 | The founding statement of the output gap concept itself (alongside Okun's Law, the unemployment-output relationship) — everything in this cluster is downstream of this paper's basic framing | `potential_gnp_measurement (Okun, 1962).pdf` |

| Hodrick, R. & Prescott, E. (1997), "Postwar U.S. Business Cycles: An Empirical Investigation," *Journal of Money, Credit and Banking* (circulated as a working paper since 1980) | Paper | 5 / 1997 | The canonical citation for the HP filter — the single most-used (and most-criticized, see the well-known "spurious cycle" critique) trend-extraction tool for separating potential output from the cycle; essential to read before using or critiquing any HP-filtered output gap, including the Brazil-specific ones in the local database | `postwar_us_business_cycles (Hodrick & Prescott, 1997).pdf` |

| Blanchard, O. & Quah, D. (1989), "The Dynamic Effects of Aggregate Demand and Supply Disturbances," *American Economic Review* | Paper | 5 / 1989 | Structural VAR decomposition into permanent (supply) and transitory (demand) shocks — a theory-disciplined alternative to purely statistical filters like HP, and the standard reference for that whole class of output gap methodology | `dynamic_effects_demand_supply_disturbances (Blanchard & Quah, 1989).pdf` |

| Kuttner, K. (1994), "Estimating Potential Output as a Latent Variable," *Journal of Business & Economic Statistics* | Paper | 4 / 1994 | Unobserved-components/Kalman-filter approach to potential output — the direct methodological ancestor of the Harvey-Clark method used in the Brazil-specific paper below | `estimating_potential_output_latent_variable (Kuttner, 1994).pdf` |

| Cusinato, R.T., Minella, A. & Pôrto Júnior, S. (2010), "Output Gap and GDP in Brazil: A Real-Time Data Analysis," Banco Central do Brasil Working Paper No. 203 | Paper | 5 / 2010 | The definitive Brazil-specific output-gap methodology comparison — tests HP filter, linear/quadratic trend, and the Harvey-Clark unobserved-components model against real-time (not just final-revision) Brazilian GDP data, finding substantial revision uncertainty across all methods. Directly informs the "no output-gap estimate exists" gap already flagged in `monetary_policy_data_inventory.md` §4 | `output_gap_gdp_brazil_real_time (Cusinato, Minella & Porto Junior, 2010).pdf` |

| Souza Júnior, J.R.C. (2005), "Produto Potencial: Conceitos, Métodos de Estimação e Aplicação à Economia Brasileira," IPEA Texto para Discussão No. 1130 | Paper | 4 / 2005 | The broadest Brazil-specific potential-output survey — combines the production-function method with the HP filter and finds the 2003+ recovery wasn't matched by equivalent potential-output growth; complements Cusinato-Minella-Pôrto Júnior's narrower methodology-comparison focus with a fuller conceptual treatment and a production-function angle that connects directly to cluster 9's productivity work | `produto_potencial_brasil (Souza Junior, 2005).pdf` |

## 6. `#business_cycle_dating_and_coincident_indicators` — turning many series into one cycle signal, and dating its turning points

| Source | Type | Score / Year | Why | Suggested filename |
|---|---|---|---|---|

| Stock, J. & Watson, M. (1989), "New Indexes of Coincident and Leading Economic Indicators," *NBER Macroeconomics Annual* | Paper | 5 / 1989 | The dynamic-factor-model methodology underlying most modern monthly activity indices — conceptually the ancestor of any single-index approach to summarizing many partial activity signals into one series, including IBC-Br (cluster 7) | `coincident_leading_indicators (Stock & Watson, 1989).pdf` |

| Mariano, R. & Murasawa, Y. (2003), "A New Coincident Index of Business Cycles Based on Monthly and Quarterly Series," *Journal of Applied Econometrics* | Paper | 4 / 2003 | Mixed-frequency dynamic factor model blending monthly proxies with quarterly GDP — the more direct technical ancestor of a monthly-GDP-proxy index like IBC-Br, which faces exactly this monthly/quarterly blending problem | `new_coincident_index_mixed_frequency (Mariano & Murasawa, 2003).pdf` |

| Duarte, A., Issler, J.V. & Spacov, A. (2004), "Indicadores Coincidentes de Atividade Econômica e uma Cronologia de Recessões para o Brasil," FGV EPGE Economics Working Paper No. 527 | Paper | 5 / 2004 | Builds Brazil's coincident/leading indicator system directly in the Conference Board/NBER tradition (Burns & Mitchell, Stock & Watson methodology) and shows the resulting composite index closely tracks CODACE's own recession chronology — written by Issler, one of CODACE's own architects, making this the direct methodological bridge between the international theory above and Brazil's dating committee | `indicadores_coincidentes_recessoes_brasil (Duarte, Issler & Spacov, 2004).pdf` |

| Banco Central do Brasil (2020), "Indicador de Condições Financeiras," Estudo Especial nº 76/2020 (originally a box in *Relatório de Inflação*, março/2020) | Paper (report box / special study) | 4 / 2020 | A daily financial-conditions index (26 domestic/external variables across 7 groups — BR rates, foreign rates, risk, currencies, oil, commodities, capital markets — combined via principal components) built specifically as a forward-looking leading indicator of activity, filling the "leading indicator" half of cluster 6 that Duarte-Issler-Spacov's coincident index doesn't cover | `indicador_condicoes_financeiras (BCB, 2020).pdf` |

| Banco Central do Brasil (2019), "Incerteza e Atividade Econômica," Estudo Especial nº 65/2019 (originally a box in *Relatório de Inflação*, setembro/2019) | Paper (report box / special study) | 3 / 2019 | Applies the Baker, Bloom & Davis (2016) economic policy uncertainty methodology to Brazilian data, estimating how uncertainty shocks delay consumption/investment/employment decisions — a distinct driver-side complement to the composite indicators above, not itself a coincident/leading index | `incerteza_atividade_economica (BCB, 2019).pdf` |

**Ongoing primary source, not a single paper:** Comitê de Datação de Ciclos Econômicos (CODACE), maintained by FGV/IBRE — Brazil's own NBER-style business cycle dating committee, publishing recession/expansion turning-point calls and methodology notes on an ongoing basis rather than a fixed calendar (unlike COPOM's ~8/year cadence in the monetary policy bibliography's §8). Retention window and ingestion approach not yet decided — flagged here rather than left undocumented, following the precedent set for COPOM materials.

## 7. `#brazil_activity_measurement` — IBC-Br and the national accounts it approximates

| Source | Type | Score / Year | Why | Suggested filename |
|---|---|---|---|---|

| Banco Central do Brasil (2010), "Índice de Atividade Econômica do Banco Central (IBC-Br)," box in *Relatório de Inflação*, março/2010 | Paper (report box) | 5 / 2010 | IBC-Br's original launch methodology — built specifically because Brazil, unlike most economies with monthly industrial-production data, lacked any single monthly aggregate activity gauge before this | `ibc_br_indice_atividade_original (BCB, 2010).pdf` |

| Banco Central do Brasil (2016), "Índice de Atividade Econômica do Banco Central (IBC-Br) – Revisão Metodológica," box in *Relatório de Inflação*, março/2016 | Paper (report box) | 4 / 2016 | First major methodology revision to IBC-Br since launch — necessary to understand before comparing pre-2016 and post-2016 IBC-Br readings | `ibc_br_revisao_metodologica (BCB, 2016).pdf` |

| Banco Central do Brasil (2018), "Aspectos Metodológicos e Comparações dos Comportamentos do IBC-Br e do PIB," Estudo Especial nº 3/2018 (originally a box in *Relatório de Inflação*, março/2018) | Paper (report box / special study) | 4 / 2018 | Directly documents where and why IBC-Br and GDP diverge (short-horizon volatility, supply-side-only construction with no demand-side balancing, seasonal-adjustment differences) — essential caveats before treating IBC-Br as a clean monthly GDP proxy | `ibc_br_pib_comparacao (BCB, 2018).pdf` |

| IBGE, "Sistema de Contas Nacionais Trimestrais: Notas Metodológicas" (current edition — confirm latest version on acquisition) | Paper (official methodology note) | 4 / n/a | The official Quarterly National Accounts methodology that IBC-Br is itself calibrated against (per the 2018 Estudo Especial above) — the necessary baseline reference for the `atv_pib`, `atv_pim`, `atv_pmc`, and `atv_pms` tables already in `macro_brasil` | `contas_nacionais_trimestrais_notas_metodologicas (IBGE).pdf` |

## 8. `#commodity_cycles_dutch_disease_and_growth` — the structural growth channel of Brazil's commodity exposure

**Scope note:** covers the growth/industrial-structure channel only — commodity price pass-through into consumer prices is inflation's territory (cluster 3 there); this cluster is about how a commodity cycle reshapes potential output and competitiveness.

| Source | Type | Score / Year | Why | Suggested filename |
|---|---|---|---|---|

| Corden, W.M. & Neary, J.P. (1982), "Booming Sector and De-Industrialisation in a Small Open Economy," *The Economic Journal* | Paper | 5 / 1982 | The founding Dutch disease model — a commodity/resource boom that appreciates the real exchange rate and reallocates resources away from tradable manufacturing, formalizing a concern raised repeatedly in Brazilian industrial-policy debates | `booming_sector_deindustrialisation (Corden & Neary, 1982).pdf` |

| Frankel, J. (2010), "The Natural Resource Curse: A Survey," NBER Working Paper 15836 | Paper | 4 / 2010 | Comprehensive survey of the resource-curse literature and its various channels (Dutch disease, volatility, institutional/political-economy effects, the "voracity effect") — situates Corden-Neary's specific mechanism within the broader debate | `natural_resource_curse_survey (Frankel, 2010).pdf` |

| Fernández, A., Schmitt-Grohé, S. & Uribe, M. (2017), "World Shocks, World Prices, and Business Cycles: An Empirical Investigation," *Journal of International Economics* | Paper | 4 / 2017 | Quantifies how much of emerging-market business cycle variance is explained by common world/commodity-price shocks versus country-specific factors — a direct empirical framework for asking how much of Brazil's own cycle is "the commodity cycle" versus domestic policy | `world_shocks_world_prices_business_cycles (Fernandez, Schmitt-Grohe & Uribe, 2017).pdf` |

## 9. `#brazil_productivity_and_potential_growth` — measuring productivity itself, not just the output gap it feeds into

**Distinct from cluster 5:** cluster 5 covers *output gap* measurement (actual output vs. potential, cyclical); this cluster covers *productivity* directly — the growth-accounting decomposition of potential output itself into capital, labor, and the residual (total factor productivity), which is the slower-moving trend cluster 5's methods are trying to extract in the first place.

| Source | Type | Score / Year | Why | Suggested filename |
|---|---|---|---|---|
| Solow, R. (1957), "Technical Change and the Aggregate Production Function," *The Review of Economics and Statistics* | Paper | 5 / 1957 | The founding growth-accounting paper — introduces the "Solow residual," decomposing output growth into capital, labor, and an unexplained residual (total factor productivity). Distinct from Solow (1956, cluster 3), which is the theoretical growth model; this is the empirical measurement companion that everything in this cluster, including the Brazil-specific studies below, is built on | `technical_change_aggregate_production_function (Solow, 1957).pdf` |
| Souza Júnior, J.R.C. (2005), IPEA Texto para Discussão No. 1130 — **cross-listed from cluster 5** | Paper | 4 / 2005 | Its production-function approach to Brazilian potential output is, in growth-accounting terms, already half a TFP decomposition — read alongside this cluster rather than only cluster 5 | *(see cluster 5 for filename)* |
| Banco Central do Brasil (2018), "Evolução da Produtividade e do Rendimento do Trabalho," Estudo Especial nº 27/2018 (originally a box in *Relatório de Inflação*, dezembro/2018) | Paper (report box / special study) | 4 / 2018 | BCB's own labor-productivity study — measures value-added per worker (VAB/PO) for 2012Q1-2018Q3 in the sectors most tied to the business cycle, finds a 9.5% cumulative decline driven mostly by within-sector (not reallocation) effects, and compares it against real labor income growth | `evolucao_produtividade_rendimento_trabalho (BCB, 2018).pdf` |
| Veloso, F., Matos, S. & Peruchetti, P. (2020a), "Nota Metodológica dos Indicadores Anuais de Produtividade Total dos Fatores no Brasil desde a Década de 1980," IBRE/FGV, Observatório da Produtividade Regis Bonelli | Paper (methodological note) | 5 / 2020 | **This closes the gap flagged in the previous pass** — the actual aggregate-TFP-for-Brazil methodology note, filling exactly the hole BCB's own material (labor productivity only, EE027/2018 above) doesn't cover. Built to address a specific problem the authors identify explicitly: existing Brazilian TFP estimates were often not public or not documented in enough detail to replicate | `ptf_brasil_nota_metodologica (Veloso, Matos & Peruchetti, 2020a).pdf` |
| Veloso, F., Matos, S. & Peruchetti, P. (2020b), "Produtividade Total dos Fatores no Brasil: Uma Visão de Longo Prazo," IBRE/FGV, Observatório da Produtividade Regis Bonelli | Paper (results note) | 5 / 2020 | The companion results note — presents the actual annual Brazilian TFP series from 1981, finding average TFP growth of only 0.3%/year over 1981-2019, with a *negative* -0.1%/year in 2010-2019 that diverges sharply from labor productivity per hour (+0.4%/year same period) — precisely the kind of concrete, decade-by-decade breakdown (1981-90, 90-00, 00-10, 10-19) useful for a Brazil growth narrative | `ptf_brasil_visao_longo_prazo (Veloso, Matos & Peruchetti, 2020b).pdf` |

**Ongoing primary source, not a single paper:** the **Observatório da Produtividade Regis Bonelli** (ibre.fgv.br/observatorio-produtividade), FGV/IBRE's dedicated productivity-tracking portal — publishes the annual TFP and labor-productivity series above on an ongoing basis, plus further reports/notes (e.g. Veloso, Matos & Peruchetti's companion piece specifically on labor productivity as the long-run growth engine). Treat similarly to CODACE in cluster 6: an ongoing feed to monitor, not a one-time acquisition.

**Noted but not yet verified:** both 2020 notes above cite an earlier survey, Veloso et al. (2013), reviewing the several competing Brazilian TFP estimates that predated this IBRE series — worth tracking down and adding if a fuller historical/comparative view of Brazilian TFP methodologies is wanted, but exact venue/co-authors weren't confirmed in this pass.

---

## Suggested acquisition order

1. **Okun (1962)** and **Cusinato, Minella & Pôrto Júnior (2010)** — cheapest high-value pair: one closes the conceptual foundation for "output gap," the other is the single most load-bearing Brazil-specific reference, directly answering a gap already flagged in the monetary policy data inventory.
2. **Solow (1956)** and **Kydland & Prescott (1982)** — the two single most-cited papers in this entire bibliography; nothing else here makes full sense without these two frameworks (long-run growth, short-run real cycles) as background.
3. **Banco Central do Brasil (2010, 2016, 2018) IBC-Br boxes** — read together as a set; they're short, and the methodology only makes sense read as a sequence (launch → revision → comparison-to-GDP).
4. **Corden & Neary (1982)** — closes the Dutch disease gap cheaply; short, frequently invoked in Brazilian industrial-policy commentary, worth having early.
5. **Solow (1957)**, **Banco Central do Brasil (2018), Estudo Especial nº 27**, and **Veloso, Matos & Peruchetti (2020a/b)** — the full productivity set; read the growth-accounting theory first, then BCB's labor-productivity-only application, then FGV/IBRE's fuller aggregate-TFP series, so the progression from theory → partial Brazilian application → complete Brazilian application is visible.
6. **Duarte, Issler & Spacov (2004)** — read alongside Burns & Mitchell and Stock & Watson (cluster 1/6) once those are acquired, since it's the direct Brazilian application of both.
7. Everything else, roughly in cluster order — the Barro & Sala-i-Martin (2004) textbook chapters, the IBGE national accounts methodology note, and the two 2019-2020 BCB Estudos Especiais (uncertainty, financial conditions) are lower urgency, useful thickening rather than foundational.

## Status

No sources acquired yet. This file is the pre-acquisition candidate list; once processing begins, create `economic_activity_conceptual_map.md` (Sources table + `#cluster` concept bullets, one source processed at a time) and demote acquired/processed rows out of this file into that map, following the same lifecycle as `monetary_policy_bibliography_candidates.md` and `inflation_bibliography_candidates.md`. The IBGE national accounts methodology note (cluster 7) needs its exact current edition confirmed before acquisition. A data inventory (`economic_activity_data_inventory.md`) should follow this file once the literature pass is far enough along, per the standard workflow in `BIBLIOGRAPHY_METHODOLOGY.md`.
