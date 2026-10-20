# Currency Regimes and the Impossible Trinity

**Type:** Policy framework / taxonomy
**Tags:** #impossible-trinity #trilemma #currency-regimes #fixed-exchange-rate #gold-standard #bretton-woods #currency-board #crawling-peg

---

## The Impossible Trinity (Trilemma)

A country cannot simultaneously have all three of:
1. A credibly fixed exchange rate
2. Full capital account convertibility (free capital flows)
3. Independent monetary policy

**Why not:** if 1 and 2 both hold, there is effectively only one currency in the world — any attempt to set domestic rates below foreign rates triggers unlimited capital outflow, forcing the central bank to sell reserves until domestic rates are bid back up to parity (and symmetrically for a rate cut attempt). Independent monetary policy is only possible by giving up one of the other two legs.

Under a **floating** rate, this tension resolves cleanly: a rate cut weakens the currency, which itself reinforces the expansionary policy (more exports, fewer imports) rather than fighting it — this is the same DD-AA logic as [[exchange_rate/synthesis/output_exchange_rates_sr (Krugman, 2023)]], stated as a policy trilemma rather than derived from a diagram.

Every currency regime below is a different choice of which corner(s) of the trilemma to sacrifice, and by how much.

---

## Taxonomy of regimes (IMF classification, ~8 categories)

Ordered from least to most exchange-rate flexibility — equivalently, from "monetary policy fully sacrificed" to "monetary policy fully retained":

| Regime | Mechanism | Monetary independence | Example |
|---|---|---|---|
| **No separate legal tender** (dollarization / monetary union) | Foreign currency used directly as domestic money | None | Ecuador, Panama (USD); EMU members (EUR) |
| **Currency board (CBS)** | Legislated 100%-reserve backing of the monetary base; no discretion | None (no lender-of-last-resort capacity) | Hong Kong SAR (HKD/USD, since 1983) |
| **Fixed parity** | Peg to a currency/basket, ±1% band, discretionary reserves, no legal commitment | Very limited | historically common in Latin America |
| **Target zone** | Fixed parity, wider band (~±2%) | Somewhat more | Denmark (DKK/EUR, ±2.5%) |
| **Crawling peg** (passive/active) | Rate adjusted on a schedule to track inflation (passive) or pre-announced to *shape* inflation expectations (active) | Limited but growing | Brazil, Argentina, Chile, Uruguay in the 1980s |
| **Fixed parity with crawling bands** | Fixed central rate + a band that pre-announced widens over time | Gradually increasing | used as an exit ramp from a hard peg |
| **Managed float ("dirty float")** | No explicit target; discretionary intervention toward internal/external goals | Substantial | many EM currencies |
| **Independent float** | Market-determined; central bank retains full domestic-policy latitude, intervenes rarely | Full | USD, JPY, most G10 |

Key nuance: even "independent floats" intervene occasionally (Plaza Accord 1985; concerted G5 EUR support, September 2000) — the taxonomy is a spectrum of *typical behavior*, not a hard legal distinction, and countries do switch (e.g., South Korea moves between independent float and managed float).

**Currency board vs. dollarization**: a CBS lets the monetary authority earn seigniorage (near-zero interest paid on the monetary base liability, market rate earned on FX reserve assets); dollarization hands that seigniorage to the anchor country.

---

## Historical evolution

- **Classical gold standard** (~1870–WWI): price-specie-flow mechanism — trade surplus → gold inflow → money supply expansion → prices rise → exports fall (self-correcting, but tied domestic monetary policy to trade flows regardless of domestic conditions).
- **Bretton Woods** (1944–1973): fixed dollar parities with periodic realignment; broke down under chronic inflation and the reserve-currency asymmetry documented in [[exchange_rate/synthesis/fixed_exchange_rate_intervention (Krugman, 2023)]].
- **Post-1973 float**: adopted expecting exchange rates to track goods/trade flows; instead, exchange rates proved to be dominated by asset-market/investment flows and were far more volatile than predicted — an early empirical hint at the asset-approach logic later formalized in [[uip]] and [[overshooting]].
- **European Exchange Rate Mechanism (1979) and its 1992 crisis**: the classic **self-fulfilling speculative attack** case — UK recession/low rates vs. German reunification-driven high rates pulled capital toward DM; Bank of England ran out of reserves defending sterling, forcing UK exit from the ERM in September 1992, only two years after joining. Same mechanics as the balance-of-payments-crisis model in [[exchange_rate/synthesis/fixed_exchange_rate_intervention (Krugman, 2023)]].
- **Euro (1999)**: the "no separate legal tender" endpoint of the trilemma for its members — full currency credibility transfer, full loss of independent monetary policy, exposed as a real cost in the 2010 EMU sovereign debt crisis (monetary union confers credibility, not creditworthiness).

---

## Connections

- [[exchange_rate/synthesis/capital_flow_fx_market (CFA L1, 2025)]] — primary source; this concept page (Impossible Trinity framework and the full IMF regime taxonomy) was created from that reading
- [[exchange_rate/synthesis/fixed_exchange_rate_intervention (Krugman, 2023)]] — same core mechanics (fixing R=R* requires giving up Ms control) derived via the DD-AA/money-market model rather than stated as a trilemma; gold standard and reserve-currency-asymmetry history overlaps directly
- [[uip]] — the trilemma's "credibly fixed + convertible ⇒ one currency" logic is UIP with zero risk premium and zero expected depreciation
- [[overshooting]] — post-1973 float volatility being driven by asset flows rather than trade flows is the empirical seed for the asset-approach/overshooting framework
- [[exchange_rate/synthesis/exchange_rate_calculation (CFA L1, 2025)]] — companion reading in the same CFA learning module, covering the mechanics (cross-rates, forward points) that operate within whatever regime a currency is in
- [[kapitalo_fx_mental_models]] — 7.1–7.2: populist→orthodox government transitions as a repricing catalyst; Argentine currency-band liberalization and capital controls as a real-world regime-transition case study
- [[monetary_policy/synthesis/taylor_rule (Taylor, 1993)]] — G-7 policy-rule simulations: fixed exchange rates raise output and price volatility relative to flexible rates with domestic interest-rate rules
- [[monetary_policy/synthesis/open_economy_monetary_policy_ch8 (Gali, 2015)]] — an exchange rate peg evaluated as a monetary rule in a New Keynesian small open economy: the most stable terms of trade but a larger welfare loss than strict inflation targeting (Table 8.1)
- [[monetary_policy/synthesis/nk_small_open_economy (Gali & Monacelli, 2005)]] — a peg vs. domestic and CPI inflation targeting in a New Keynesian small open economy: the most stable real exchange rate but the most volatile output gap and inflation, and the largest welfare loss, costlier the less open the economy (Tables 1–2)
- [[monetary_policy/synthesis/dilemma_not_trilemma (Rey, 2013)]] — challenges the trilemma: with free capital mobility a global financial cycle driven partly by US monetary policy reaches floaters too, so monetary independence requires managing the capital account (a "dilemma")
- [[monetary_policy/synthesis/trilemma_tradeoffs (Obstfeld, 2015)]] — defends the trilemma against the "dilemma": non-pegs keep substantial short-term rate independence while pegs import base-country rates, but long-term rates co-move whatever the regime
- [[monetary_policy/synthesis/us_policy_international_risk_spillovers (Kalemli-Ozcan, 2019)]] — managed vs. free floats under US-driven risk shocks: free floats show little co-movement of rate differentials with the VIX and little growth loss, managed floats a large one (Chart 13, Table 6)
- [[monetary_policy/synthesis/us_monetary_policy_global_cycle (Miranda-Agrippino & Rey, 2020)]] — independently floating countries see credit and capital-flow contractions after a US tightening of similar size to the full sample: floating is no shield against the global financial cycle, though regimes still matter
- [[monetary_policy/synthesis/inflation_targeting_em (Mishkin, 2000)]] — inflation targeting as the alternative nominal anchor after the 1990s peg crises in emerging markets; heavy intervention risks making the exchange rate the anchor again, so smoothing should be transparent and short-run
