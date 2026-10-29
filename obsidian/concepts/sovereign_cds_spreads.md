# Sovereign CDS Spreads

**Type:** Market indicator of sovereign credit risk
**Tags:** #sovereign-risk #cds #credit-risk #risk-premium

---

## Definition

The periodic premium paid for protection against the default of a government. The protection buyer pays the spread; on a credit event — failure to pay, moratorium or restructuring, as defined in the contract — the buyer either delivers an eligible bond and receives its face value (physical settlement) or receives the difference between face value and market value (cash settlement). The spread rises with the expected loss on the reference bonds, typically the sovereign's senior dollar-denominated external debt; the linked source works with the 5-year contract.

## Mechanism

The spread combines the market's assessment of default probability and loss with a risk premium for bearing that risk. Because it trades continuously, it updates far more often than ratings and is used to gauge market perception of a government's debt sustainability. Its short-term moves can be driven less by the country's own fundamentals than by global risk appetite: in weekly data, a common global factor — proxied by the U.S. equity market — explains much of the co-movement across sovereigns, with emerging markets more sensitive (Takami, 2018).

## When it applies / when it fails

- **Weekly moves are mostly global.** Local variables (exchange rate, short-term local yield, bank CDS) add explanatory power only for some countries; for many, none does (Takami, 2018).
- **Fiscal fundamentals do not show up at high frequency.** Debt, deficits and reserves are published monthly at best, so short-horizon models of the spread cannot test them; the spread's link to fiscal policy has to be assessed at lower frequency.
- **Banking-to-sovereign spillovers arrive as breaks.** Bank distress was not priced gradually into sovereign spreads before the 2010–2012 euro crisis; the transmission looks discontinuous.
- **The relations are sample-dependent.** Estimated in a period of abundant global liquidity and carry, they may not hold in other regimes.
- **The exchange-rate link runs both ways.** Depreciation raises the burden of dollar debt, but a rising spread can also cause depreciation through capital outflows, so contemporaneous estimates need instruments.

## How it appears across sources

| Source | Role |
|---|---|
| [[fiscal_policy/synthesis/short_term_drivers_sovereign_cds (Takami, 2018)]] | Defines the contract and tests global and local determinants of weekly 5-year CDS changes for 35 sovereigns, July 2005–July 2016, with GMM model search: the S&P 500 is significant for 22 of 35, with larger coefficients for emerging markets; no local variable matters for 16, Brazil included |

## BRL / application to the current analysis

The linked source includes Brazil in its 2005–2016 sample: Brazil's weekly CDS changes load on the S&P 500 with one of the larger coefficients in the sample, and no local variable is selected as a significant driver.

## Connections

- [[global_financial_cycle]] — the common global factor that dominates short-term moves in sovereign spreads
- [[debt_sustainability]] — what the spread is meant to price over longer horizons
- [[risk_premium]] — the FX counterpart: country risk demanded to hold the currency
- [[fiscal_policy/synthesis/short_term_drivers_sovereign_cds (Takami, 2018)]] — definition of the instrument and its short-term determinants across 35 sovereigns
