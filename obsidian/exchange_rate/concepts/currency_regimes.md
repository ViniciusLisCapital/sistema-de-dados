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

Under a **floating** rate, this tension resolves cleanly: a rate cut weakens the currency, which itself reinforces the expansionary policy (more exports, fewer imports) rather than fighting it — this is the same DD-AA logic as [[Krugman 2023 - Output and the Exchange Rate in the Short Run]], stated as a policy trilemma rather than derived from a diagram.

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
- **Bretton Woods** (1944–1973): fixed dollar parities with periodic realignment; broke down under chronic inflation and the reserve-currency asymmetry documented in [[Krugman 2023 - Fixed Exchange Rates and Foreign Exchange Intervention]].
- **Post-1973 float**: adopted expecting exchange rates to track goods/trade flows; instead, exchange rates proved to be dominated by asset-market/investment flows and were far more volatile than predicted — an early empirical hint at the asset-approach logic later formalized in [[uip]] and [[overshooting]].
- **European Exchange Rate Mechanism (1979) and its 1992 crisis**: the classic **self-fulfilling speculative attack** case — UK recession/low rates vs. German reunification-driven high rates pulled capital toward DM; Bank of England ran out of reserves defending sterling, forcing UK exit from the ERM in September 1992, only two years after joining. Same mechanics as the balance-of-payments-crisis model in [[Krugman 2023 - Fixed Exchange Rates and Foreign Exchange Intervention]].
- **Euro (1999)**: the "no separate legal tender" endpoint of the trilemma for its members — full currency credibility transfer, full loss of independent monetary policy, exposed as a real cost in the 2010 EMU sovereign debt crisis (monetary union confers credibility, not creditworthiness).

---

## Connections

- [[Krugman 2023 - Fixed Exchange Rates and Foreign Exchange Intervention]] — same core mechanics (fixing R=R* requires giving up Ms control) derived via the DD-AA/money-market model rather than stated as a trilemma; gold standard and reserve-currency-asymmetry history overlaps directly
- [[uip]] — the trilemma's "credibly fixed + convertible ⇒ one currency" logic is UIP with zero risk premium and zero expected depreciation
- [[overshooting]] — post-1973 float volatility being driven by asset flows rather than trade flows is the empirical seed for the asset-approach/overshooting framework
- [[CFA L1 2025 - Exchange Rate Calculations]] — companion reading in the same CFA learning module, covering the mechanics (cross-rates, forward points) that operate within whatever regime a currency is in
- [[kapitalo_fx_mental_models]] — 7.1–7.2: populist→orthodox government transitions as a repricing catalyst; Argentine currency-band liberalization and capital controls as a real-world regime-transition case study
