---
aliases: ["Albagli 2018 - Channels of US Monetary Policy Spillovers to International Bond Markets"]
---

# Channels of US Monetary Policy Spillovers to International Bond Markets — Elias Albagli, Luis Ceballos, Sebastian Claro & Damian Romero 2018

**Type:** paper
**Tags:** #us-monetary-policy #spillovers #term-premium #bond-yields #fx-intervention #emerging-markets #event-study
**Source:** BIS Working Papers No 719, Monetary and Economic Department, Bank for International Settlements (May 2018); paper for the BIS Consultative Council for the Americas research conference "Low interest rates, monetary policy and international spillovers"
**Language:** English
**Source file:** [[external/clean_md/us_mp_spillovers_bond_markets (Albagli et al., 2018)]]

---

## Context and motivation

After the global financial crisis the Fed and other central banks turned to long-term yields (forward guidance, asset purchases), the world bond market grew fast and foreign investors took a larger share of domestic bond markets, most visibly in emerging markets. That raises whether the cost of funds outside the core can stay independent of US policy. Three questions were open: identification (causal spillover or common shocks?), coverage (few studies of EMEs, for lack of long-dated yield curves), and channels — do foreign long yields move because markets expect foreign policy rates to follow the Fed, or because risk compensation changes through portfolio rebalancing and risk-taking? The authors are from the Central Bank of Chile.

## Core argument / thesis

US monetary policy shocks move long-term bond yields abroad by large amounts — after October 2008 at least as much as domestic monetary policy — and through different channels in developed and emerging economies. In developed countries the spillover runs through the risk-neutral component (expected future policy rates); in emerging markets it runs mostly through term premia. The difference is not an information effect: FOMC meetings do not appear to reveal US fundamentals that markets then extrapolate abroad. It is an **exchange rate channel** shaped by the policy response: each central bank faces a trade-off between narrowing the rate differential with the US and letting its currency move. Developed countries float — partly moving expected policy rates, partly the exchange rate. Emerging markets intervene in the FX market, which cushions the currency but **reinforces** the capital flows, and the flows show up in long-term yields as term-premium moves. So FX intervention does not insulate the economy: it "deflect[s] the burden of adjustment into long term yields".

## Key mechanisms / model

**Identification.** The US shock is the change in the 2-year Treasury yield from the close of the day before to the close of the day after each FOMC meeting (after Hanson & Stein): Fed funds changes are rare and anticipated, and the 2-year yield captures news about the medium-term path. Panel regressions, run separately for 12 developed (DEV) and 12 emerging (EME) countries, January 2003–December 2016, split at October 2008, regress the change in each country's 2- and 10-year yields (and the 10-year risk-neutral and term-premium components) on the US shock, controlling for domestic policy meetings and US and domestic CPI, activity and unemployment releases, each measured as the 2-year yield change in a two-day window, with year and month fixed effects. Brazil is not in the EME sample (Chile, Colombia, Hungary, India, Indonesia, Israel, Korea, Mexico, Poland, South Africa, Taiwan, Thailand).

The design rests on two premises: FOMC days matter for rate volatility (2-year yields are more volatile around meetings, significantly so after 2008), and they are not contaminated by other news (overlap with all other events is about 7%).

**Decomposition.** Each country's yields are split into risk-neutral (RN) and term-premium (TP) components with the Adrian, Crump & Moench affine model, with the Bauer–Rudebusch–Wu small-sample bias correction, which otherwise understates the persistence of short rates and so overstates the volatility of the term premium.

**The model (Appendix A, extending Blanchard, Adler & Carvalho Filho).** US policy lowers a global "risk-taking factor" when it eases, which compresses US term premia. Foreign investors allocate to a country's short and long bonds in proportion to the yield differential with the US net of expected depreciation (imperfect substitutability). The domestic central bank sets its short rate against the exchange rate (pass-through or trade-balance motives) with strength d, and may sterilize-intervene against private flows with offset φ. Domestic investors hold long bonds by yield alone. The balance of payments closes the model. Two comparative statics carry the interpretation, for an expansionary US shock:
- **Proposition 1** — a policy rate more sensitive to the exchange rate (higher d): weaker appreciation, weaker inflows, a larger RN response, an ambiguous TP response.
- **Proposition 2** — more FX intervention (higher φ): weaker appreciation, **stronger** inflows (because intervention removes the appreciation and expected depreciation that would deter them), a smaller RN response, and a larger TP response.

A weak RN response in EMEs is consistent with either. What separates them is the exchange rate and flows: low d would give *more* currency movement in EMEs; high φ gives less currency movement and more flows.

**Contrast with Mundell-Fleming.** In the standard model, sterilized intervention can stabilize both the short rate and the currency at no apparent cost. With a long-bond market, intervention cannot control long yields, and if demand depends on the whole curve the economy is not insulated.

## Main results / findings

- **Size and timing.** A 100 bp US shock raises 10-year yields by 43 bp in DEV and 56 bp in EME after October 2008 (0.429 and 0.557, Table 2), up from smaller elasticities before, particularly for EME. In DEV the effect on 2-year yields fell between the subsamples while the effect on 10-year yields rose.
- **Channel.** Full sample, Table 2: in DEV the RN component carries virtually the whole 10-year effect (0.331) and the TP effect is not different from zero (0.005); in EME the TP carries most of it (0.239) and the RN estimate is not significant (0.054). After 2008 the TP becomes significant in DEV and the RN marginally significant in EME, but the split holds.
- **Relative importance.** In DEV the US effect on 10-year yields is about the same as that of domestic policy; in EME after 2008 domestic policy's effect (0.325, Table 3) is significantly smaller than the US effect. Domestic policy tightening raises RN rates by more than yields, with a falling TP, consistent with a tightening reducing inflation risk premia. Domestic macro releases move long yields by amounts comparable to US policy.
- **Information channel rejected.** Long yields abroad comove less with the US 2-year yield on US macro release days (more macro news) than on FOMC days (Table 5); in EME the release-day effects are mostly insignificant. Following Hanson & Stein's logic, the comovement on FOMC days is not driven by revealed US fundamentals. In monthly regressions, the FOMC component of the US 2-year change is followed by lower activity and inflation abroad (Table 6) — the contractionary sign, not the positive one a signaling story would produce.
- **Exchange rate channel confirmed.** A 1 bp US shock depreciates DEV currencies by 7.50 bp and EME currencies by 3.52 bp in the full sample (Table 7) — roughly half as much in EME; both effects grow after 2008. There is virtually no movement before the event window, so the shock is not anticipated. Normalized by GDP or by government debt outstanding, the response of fixed-income flows (post-2008 only, weekly EPFR data) is larger in EME (Table 8), especially per unit of debt.
- **Robustness.** Dropping one country at a time (Table 13), alternative fixed effects and clustering (Table 14), the Joslin–Singleton–Zhu decomposition instead of ACM (Table 15), a one-day window (Table 16), the 1-year Treasury (Table 17, larger elasticities because its standard deviation is about 60% of the 2-year's after 2008) and 1-year-ahead Fed funds futures, directly or as an instrument (Table 18), all keep the result: larger spillovers after 2008, RN-tilted in DEV, TP-tilted in EME.

## Limitations and caveats

- The policy mechanism is inferred, not measured: the FXI interpretation rests on the joint pattern of weak currency moves, strong flows and TP-heavy yields, plus a survey of FX regimes (Table 12) that the authors say underestimates intervention because many countries do not disclose it. No country-level intervention data enter the regressions.
- The term premium is model-dependent (ACM with bias correction; JSZ as check), and in EMEs it may also carry default and liquidity risk; the authors cannot separate real from nominal premia for lack of inflation-linked bond data.
- Flows are weekly and the identification there is "less clean"; flows are not normalized by market liquidity, which the authors argue would strengthen the result.
- The monthly test of the information channel is weaker than the text suggests: the negative responses are clearest before October 2008; after it, the FOMC component's coefficients for DEV activity and for EME inflation are mostly positive and not significant (Table 6).
- A tension with the forward premium puzzle is acknowledged: low US rates are associated with higher foreign-currency risk premia (Lustig, Roussanov & Verdelhan). The authors argue that a policy surprise beyond fundamentals differs from a low-rate environment, and that their result needs only that fixed-income flows follow yield differentials, not that UIP holds.
- The model is partial: no aggregate demand, US policy as an exogenous AR(1), domestic policy shocks with zero variance.
- Damaged passages: Equation (1) and the affine-model equations (2)–(4) have subscripts scattered across lines; the closed-form solutions (A.13)–(A.17) and condition (A.18) have their fractions collapsed into single lines and cannot be read; Table 14 is printed rotated, with every number and label reversed character by character, so its entries are not usable; Figures 1 and 2 survive as captions only; Table 6's caption refers to "equation (??)" and promises standard errors that the table does not show; Table 7's columns are labelled "Nov. 2008" while the text and other tables split at October 2008. The reference list is not in the file (pages 27–30 are missing).

## Connections

- [[term_premium]] — the margin through which US policy reaches EME long yields; the source decomposes 24 countries' curves with ACM and shows the TP carrying EME spillovers
- [[fx_intervention]] — the source's key policy result: sterilized intervention cushions the currency but strengthens inflows and moves term premia, so it shifts rather than removes the adjustment
- [[global_financial_cycle]] — US policy as the driver of a risk-taking factor and of capital flows into foreign bond markets, after 2008 at least as strong as domestic policy
- [[monetary_policy_shocks]] — high-frequency identification of US policy surprises from the 2-year Treasury in a two-day window around FOMC meetings
- [[information_effect]] — tested and rejected as the explanation of international yield comovement on FOMC days
- [[forward_premium_puzzle]] — the source's results do not require UIP; it reconciles a dollar that depreciates on an easing surprise with the puzzle
- [[mundell_fleming_policy_mix]] — the source's model breaks the Mundell-Fleming result that sterilized intervention can stabilize both the short rate and the currency
- [[monetary_policy/synthesis/term_structure_linear_regressions (Adrian, Crump & Moench, 2013)]] — the decomposition the source applies to every country's yield curve
- [[exchange_rate/synthesis/us_policy_international_risk_spillovers (Kalemli-Ozcan, 2019)]] — the companion argument that EME policies limiting exchange rate volatility are counterproductive; here the cost shows up in term premia
- [[external/synthesis/us_monetary_policy_global_cycle (Miranda-Agrippino & Rey, 2020)]] — the macro-financial counterpart: US shocks drive global risk appetite and flows; here the same shocks priced in foreign bond curves
- [[monetary_policy/synthesis/information_effect_hf_identification (Nakamura & Steinsson, 2018)]] — the information effect at home; this source asks whether it explains effects abroad and finds it does not
