# Currency Exchange Rates: Understanding Equilibrium Value

## 1. Introduction

Exchange rates are well known to follow a random walk, whereby fluctuations from one day to the next are unpredictable. The business of currency forecasting can be a humbling experience. Alan Greenspan, former chair of the US Federal Reserve Board, famously noted that "having endeavored to forecast exchange rates for more than half a century, I have understandably developed significant humility about my ability in this area."

Hence, our discussion is not about predicting exchange rates but about the tools the reader can use to better understand long-run equilibrium value. This outlook helps guide the market participant's decisions with respect to risk exposures, as well as whether currency hedges should be implemented and, if so, how they should be managed. After discussing the basics of exchange rate transactions, we present the main theories for currency determination—starting with the international parity conditions—and then describe other important influences, such as current account balances, capital flows, and monetary and fiscal policy.

Although these fundamentals-based models usually perform poorly in predicting future exchange rates in the short run, they are crucial for understanding long-term currency value. Thus, we proceed as follows:

- We review the basic concepts of the foreign exchange market covered in the CFA Program Level I curriculum and expand this previous coverage to incorporate more material on bid–offer spreads.
- We then begin to examine determinants of exchange rates, starting with longer-term interrelationships among exchange rates, interest rates, and inflation rates embodied in the international parity conditions. These parity conditions form the key building blocks for many long-run exchange rate models.
- We also examine the foreign exchange (FX) carry trade, a trading strategy that exploits deviations from uncovered interest rate parity, and discuss the relationship between a country's exchange rate and its balance of payments.
- We then examine how monetary and fiscal policies can indirectly affect exchange rates by influencing the various factors described in our exchange rate model.
- The subsequent section focuses on direct public sector actions in foreign exchange markets, both through capital controls and by foreign exchange market intervention (buying and selling currencies for policy purposes).
- The last section examines historical episodes of currency crisis and some leading indicators that may signal the increased likelihood of a crisis.

---

## 2. Foreign Exchange Market Concepts

We begin with a brief review of some of the basic conventions of the FX market that were covered in the CFA Program Level I curriculum. In this section, we cover (1) the basics of exchange rate notation and pricing, (2) arbitrage pricing constraints on spot rate foreign exchange quotes, and (3) forward rates and covered interest rate parity.

An exchange rate is the price of the base currency expressed in terms of the price currency. For example, a USD/EUR rate of 1.1650 means the euro, the base currency, costs 1.1650 US dollars (an appendix defines the three-letter currency codes). The exact notation used to represent exchange rates can vary widely between sources, and occasionally the same exchange rate notation will be used by different sources to mean completely different things. The reader should be aware that the notation used here may not be the same as that encountered elsewhere. To avoid confusion, we will identify exchange rates using the convention of "P/B," referring to the price of the base currency, "B," expressed in terms of the price currency, "P."

The spot exchange rate is usually used for settlement on the second business day after the trade date, referred to as T + 2 settlement (the exception being CAD/USD, for which standard spot settlement is T + 1). In foreign exchange markets—as in other financial markets—market participants are presented with a two-sided price in the form of a bid price and an offer price (also called an ask price) quoted by potential counterparties. The bid price is the price, defined in terms of the price currency, at which the counterparty is willing to buy one unit of the base currency. Similarly, the offer price is the price, in terms of the price currency, at which that counterparty is willing to sell one unit of the base currency. For example, given a price request from a client, a dealer might quote a two-sided price on the spot USD/EUR exchange rate of 1.1648/1.1652. This means that the dealer is willing to pay USD 1.1648 to buy one EUR and that the dealer is willing to sell one EUR for USD 1.1652.

There are two points to bear in mind about bid–offer quotes:

1. The offer price is always higher than the bid price. The bid–offer spread—the difference between the offer price and the bid price—is the compensation that counterparties seek for providing foreign exchange to other market participants.

2. The party in the transaction who requests a two-sided price quote has the option (but not the obligation) to deal at either the bid (to sell the base currency) or the offer (to buy the base currency) quoted by the dealer. If the party chooses to trade at the quoted prices, the party is said to have either "hit the bid" or "paid the offer." If the base currency is being sold, the party is said to have hit the bid. If the base currency is being bought, the party is said to have paid the offer.

We will distinguish here between the bid–offer pricing a client receives from a dealer and the pricing a dealer receives from the interbank market. Dealers buy and sell foreign exchange among themselves in what is called the interbank market. This global network for exchanging currencies among professional market participants allows dealers to adjust their inventories and risk positions, distribute foreign currencies to end users who need them, and transfer foreign exchange rate risk to market participants who are willing to bear it. The interbank market is typically for dealing sizes of at least 1 million units of the base currency. Of course, the dealing amount can be larger than 1 million units; indeed, interbank market trades generally are measured in terms of multiples of a million units of the base currency. Please note that many non-bank entities can now access the interbank market. They include institutional asset managers and hedge funds.

The bid–offer spread a dealer provides to most clients typically is slightly wider than the bid–offer spread observed in the interbank market. Most currencies, except for the yen, are quoted to four decimal places. The fourth decimal place (0.0001) is referred to as a "pip." The yen is typically quoted to just two decimal places; in yen quotes, the second decimal place (0.01) is referred to as a pip.

For example, if the quote in the interbank USD/EUR spot market is 1.1649/1.1651 (two pips wide), the dealer might quote a client a bid–offer of 1.1648/1.1652 (four pips wide) for a spot USD/EUR transaction. When the dealer buys (sells) the base currency from (to) a client, the dealer is typically expecting to quickly turn around and sell (buy) the base currency in the interbank market. This offsetting transaction allows the dealer to divest the risk exposure assumed by providing a two-sided price to the client and to hopefully make a profit.

Continuing our example, suppose the dealer's client hits the dealer's bid and sells EUR to the dealer for USD 1.1648. The dealer is now long EUR (and short USD) and wants to cover this position in the interbank market. To do this, the dealer sells the EUR in the interbank market by hitting the interbank bid. As a result, the dealer bought EUR from the client at USD 1.1648 and then sold the EUR in the interbank for USD 1.1649. This gives the dealer a profit of USD 0.0001 (one pip) for every EUR transacted. This one pip translates into a profit of USD 100 per EUR million bought from the client. If, instead of hitting his bid, the client paid the offer (1.1652), then the dealer could pay the offer in the interbank market (1.1651), earning a profit of one pip.

### Factors Affecting the Bid–Offer Spread

The size of the bid–offer spread quoted to dealers' clients in the FX market can vary widely across exchange rates and is not constant over time, even for a single exchange rate. The size of this spread depends primarily on three factors:

- the bid–offer spread in the interbank foreign exchange market for the two currencies involved,
- the size of the transaction, and
- the relationship between the dealer and the client.

We examine each factor in turn.

The size of the bid–offer spread quoted in the interbank market depends on the liquidity in this market. Liquidity is influenced by several factors:

1. **The currency pair involved.** Market participation is greater for some currency pairs than for others. Liquidity in the major currency pairs—for example, USD/EUR, JPY/USD, and USD/GBP—can be quite high. These markets are almost always deep, with multiple bids and offers from market participants around the world. In other currency pairs, particularly some of the more obscure currency cross rates (e.g., MXN/CHF), market participation is much thinner and consequently the bid–offer spread in the interbank market will be wider.

2. **The time of day.** The interbank FX markets are most liquid when the major FX trading centers are open. Business hours in London and New York—the two largest FX trading centers—overlap from approximately 8:00 a.m. to 11:00 a.m. New York time. The interbank FX market for most currency pairs is typically most liquid during these hours. After London closes, liquidity is thinner through the New York afternoon. The Asian session starts when dealers in Tokyo, Singapore, and Hong Kong SAR open for business, typically by 7:00 p.m. New York time. For most currency pairs, however, the Asian session is not as liquid as the London and New York sessions. Although FX markets are open 24 hours a day on business days, between the time New York closes and the time Asia opens, liquidity in interbank markets can be very thin because Sydney, Australia, tends to be the only active trading center during these hours.

   For reference, the table below shows a 24-hour period from midnight (00:00) to midnight (24:00) London time, with corresponding standard times in Tokyo and New York, and the approximate hours of the most liquid trading periods in each market (shaded):

   | Market   | Times (London reference)                             |
   |----------|------------------------------------------------------|
   | Tokyo    | 09:00 · 13:00 · 17:00 · 21:00 · 01:00+1 · 05:00+1 · 09:00+1 |
   | London   | 00:00 · 04:00 · 08:00 · 12:00 · 16:00 · 20:00 · 24:00 |
   | New York | 19:00−1 · 23:00−1 · 03:00 · 07:00 · 11:00 · 15:00 · 19:00 |

3. **Market volatility.** As in any financial market, when major market participants have greater uncertainty about the factors influencing market pricing, they will attempt to reduce their risk exposures and/or charge a higher price for taking on risk. In the FX market, this response implies wider bid–offer spreads in both the interbank and broader markets. Geopolitical events (e.g., war, civil strife), market crashes, and major data releases (e.g., US non-farm payrolls) are among the factors that influence spreads and liquidity.

The size of the transaction can also affect the bid–offer spread shown by a dealer to clients. Typically, the larger the transaction, the further away from the current spot exchange rate the dealing price will be. Hence, a client who asks a dealer for a two-sided spot CAD/USD price on, for example, USD 50 million will be shown a wider bid–offer spread than a client who asks for a price on USD 1 million. The wider spread reflects the greater difficulty the dealer faces in offsetting the foreign exchange risk of the position in the interbank FX market. Smaller dealing sizes can also affect the bid–offer quote shown to clients. "Retail" quotes are typically for dealing sizes smaller than 1 million units of the base currency and can range all the way down to foreign exchange transactions conducted by individuals. The bid–offer spreads for these retail transactions can be very large compared with those in the interbank market.

The relationship between the dealer and the client can also affect the size of the bid–offer spread shown by the dealer. For many clients, the spot foreign exchange business is only one business service among many that a dealer provides to that client. For example, the dealer firm might also transact in bond and/or equity securities with the same client. In a competitive business environment, in order to win the client's business for these other services, the dealer might provide a tighter (i.e., smaller) bid–offer spot exchange rate quote. The dealer might also give tighter bid–offer quotes in order to win repeat FX business. A client's credit risk can also be a factor. A client with a poor credit profile may be quoted a wider bid–offer spread than one with good credit. Given the short settlement cycle for spot FX transactions (typically two business days), however, credit risk is not the most important factor in determining the client's bid–offer spread on spot exchange rates.

---

## 3. Arbitrage Constraints on Spot Exchange Rate Quotes

The bid–offer quotes a dealer shows in the interbank FX market must respect two arbitrage constraints; otherwise the dealer creates riskless arbitrage opportunities for other interbank market participants. We will confine our attention to the interbank FX market because arbitrage presumes the ability to deal simultaneously with different market participants and in different markets, the ability to access "wholesale" bid–offer quotes, and the market sophistication to spot arbitrage opportunities.

**First**, the bid shown by a dealer in the interbank market cannot be higher than the current interbank offer, and the offer shown by a dealer cannot be lower than the current interbank bid. If the bid–offer quotes shown by a dealer are inconsistent with the then-current interbank market quotes, other market participants will buy from the cheaper source and sell to the more expensive source. This arbitrage will eventually bring the two prices back into line. For example, suppose that the current spot USD/EUR price in the interbank market is 1.1649/1.1651. If a dealer showed a misaligned price quote of 1.1652/1.1654, then other market participants would pay the offer in the interbank market, buying EUR at a price of USD 1.1651, and then sell the EUR to the dealer by hitting the dealer's bid at USD 1.1652—thereby making a riskless profit of one pip on the trade. This arbitrage would continue as long as the dealer's bid–offer quote violated the arbitrage constraint.

**Second**, the cross-rate bids (offers) posted by a dealer must be lower (higher) than the implied cross-rate offers (bids) available in the interbank market. A currency dealer located in a given country typically provides exchange rate quotations between that country's currency and various foreign currencies. If a particular currency pair is not explicitly quoted, it can be inferred from the quotes for each currency in terms of the exchange rate with a third nation's currency. For example, given exchange rate quotes for the currency pairs A/B and C/B, we can back out the implied cross rate of A/C. This implied A/C cross rate must be consistent with the A/B and C/B rates.

This again reflects the basic principle of arbitrage: If identical financial products are priced differently, then market participants will buy the cheaper one and sell the more expensive one until the price difference is eliminated. In the context of FX cross rates, there are two ways to trade currency A against currency C: (1) using the cross rate A/C or (2) using the A/B and C/B rates. Because, in the end, both methods involve selling (buying) currency C in order to buy (sell) currency A, the exchange rates for these two approaches must be consistent. If the exchange rates are not consistent, the arbitrageur will buy currency C from a dealer if it is undervalued (relative to the cross rate) and sell currency A. If currency C is overvalued by a dealer (relative to the cross rate), it will be sold and currency A will be bought.

### Triangular Arbitrage

To illustrate this triangular arbitrage among three currencies, suppose that the interbank market bid–offer in USD/EUR is 1.1649/1.1651 and that the bid–offer in JPY/USD is 105.39/105.41. We need to use these two interbank bid–offer quotes to calculate the market-implied bid–offer quote on the JPY/EUR cross rate.

Begin by considering the transactions required to sell JPY and buy EUR, going through the JPY/USD and USD/EUR currency pairs. We can view this process intuitively as follows:

> Sell JPY / Buy EUR = (Sell JPY / Buy USD) then (Sell USD / Buy EUR)

Note that "Buy USD" and "Sell USD" cancel out to give the JPY/EUR cross rate. In equation form:

> (JPY/EUR) = (JPY/USD) × (USD/EUR)

Now, incorporating the bid–offer rates, a rule of thumb applies: when we speak of a bid or offer exchange rate, we are referring to the bid or offer for the currency in the denominator (the base currency).

- **Step i.** The left-hand side is "Sell JPY, Buy EUR." The EUR is in the denominator (it is the base currency). Because we want to buy the base currency, we need the **offer** rate for JPY/EUR.
- **Step ii.** The first term on the right-hand side is "Sell JPY, Buy USD." Because we want to buy the base currency (USD), we need the **offer** rate for JPY/USD.
- **Step iii.** The second term is "Sell USD, Buy EUR." Because we want to buy the base currency (EUR), we need the **offer** rate for USD/EUR.

Combining these:

> (JPY/EUR) offer = (JPY/USD) offer × (USD/EUR) offer = 105.41 × 1.1651 = **122.81**

Similarly, the implied JPY/EUR **bid** rate uses "Buy JPY, Sell EUR":

> (JPY/EUR) bid = (JPY/USD) bid × (USD/EUR) bid = 105.39 × 1.1649 = **122.77**

As expected, the implied cross-rate bid (122.77) is less than the offer (122.81).

This formula is relatively straightforward: to get the implied bid cross rate, multiply the bid rates for the other two currencies. However, depending on the quotes provided, it may be necessary to invert one of the quotes in order to complete the calculation.

This is best illustrated with an example. Consider the case of calculating the implied GBP/EUR cross rate when given USD/GBP and USD/EUR quotes. Simply using the provided quotes will not generate the desired GBP/EUR cross rate:

> (GBP/EUR) ≠ (USD/GBP) × (USD/EUR)

Instead, because USD appears in the numerator of both currency pairs, one must be inverted:

> (GBP/EUR) = (GBP/USD) × (USD/EUR)

Because the GBP/USD quote is not directly provided, we invert the USD/GBP quote. Assuming the USD/GBP bid–offer is 1.2302/1.2304:

- To buy GBP at the offer: 1.2304. Inverting gives **GBP/USD bid** = 1 ÷ 1.2304 = **0.81274**.
- To get GBP/USD offer: invert the USD/GBP bid of 1.2302: 1 ÷ 1.2302 = **0.81288**.

(Note that calculated GBP/USD quotes are extended to five decimal places to avoid truncation errors.)

Using the USD/EUR bid–offer of 1.1649/1.1651:

> (GBP/EUR) bid = (GBP/USD) bid × (USD/EUR) bid = 0.81274 × 1.1649 = **0.9468**

> (GBP/EUR) offer = (GBP/USD) offer × (USD/EUR) offer = 0.81288 × 1.1651 = **0.9471**

The implied bid rate (0.9468) is less than the implied offer rate (0.9471), as required to prevent arbitrage.

### Summary Observations on Arbitrage Constraints

- The arbitrage constraint on implied cross rates is similar to that for spot rates: posted bid rates cannot be higher than the market's offer; posted offer rates cannot be lower than the market's bid. The only difference is that this second arbitrage constraint is applied across currency pairs instead of involving a single currency pair.
- In reality, any violations of these arbitrage constraints will quickly disappear. Both human traders and automatic trading algorithms are constantly on alert for any pricing inefficiencies and will arbitrage them away almost instantly.
- Market participants do not need to calculate cross rates manually because electronic dealing machines will automatically calculate cross bid–offer rates given any two underlying bid–offer rates.

### Example 1: Bid–Offer Rates

The following are spot rate quotes in the interbank market:

| Currency Pair | Bid      | Offer    |
|---------------|----------|----------|
| USD/EUR       | 1.1649   | 1.1651   |
| JPY/USD       | 105.39   | 105.41   |
| CAD/USD       | 1.3199   | 1.3201   |
| SEK/USD       | 9.6300   | 9.6302   |

**Question 1.** What is the bid–offer on the SEK/EUR cross rate implied by the interbank market?

- A. 0.1209/0.1211
- B. 8.2656/8.2668
- C. 11.2180/11.2201

**Solution:** C is correct. Setting up the equations so that terms cancel to yield SEK/EUR:

> (SEK/EUR) = (SEK/USD) × (USD/EUR)

- Bid: 9.6300 × 1.1649 = **11.2180**
- Offer: 9.6302 × 1.1651 = **11.2201**

---

**Question 2.** What is the bid–offer on the JPY/CAD cross rate implied by the interbank market?

- A. 78.13/78.17
- B. 79.85/79.85
- C. 79.84/79.86

**Solution:** C is correct. Using the equation-based approach:

> (JPY/CAD) = (JPY/USD) × (USD/CAD)

The CAD/USD quotes of 1.3199/1.3201 must be inverted and bid/offer interchanged to obtain USD/CAD quotes: (1/1.3201)/(1/1.3199) = **0.75752/0.75763**.

- Bid: 105.39 × 0.75752 = **79.84**
- Offer: 105.41 × 0.75763 = **79.86**

---

**Question 3.** If a dealer quoted a bid–offer rate of 79.81/79.83 in JPY/CAD, then a triangular arbitrage would involve buying:

- A. CAD in the interbank market and selling it to the dealer, for a profit of JPY 0.01 per CAD.
- B. JPY from the dealer and selling it in the interbank market, for a profit of CAD 0.01 per JPY.
- C. CAD from the dealer and selling it in the interbank market, for a profit of JPY 0.01 per CAD.

**Solution:** C is correct. The implied interbank cross rate for JPY/CAD is 79.84/79.86 (from Question 2). The dealer is offering to sell CAD (the base currency) too cheaply, at an offer rate (79.83) below the interbank bid rate (79.84). Triangular arbitrage would involve buying CAD from the dealer (paying the dealer's offer) and selling CAD in the interbank market (hitting the interbank bid), for a profit of JPY 0.01 (79.84 − 79.83) per CAD transacted.

---

**Question 4.** If a dealer quoted a bid–offer of 79.82/79.87 in JPY/CAD, then you could:

- A. not make any arbitrage profits.
- B. make arbitrage profits buying JPY from the dealer and selling it in the interbank market.
- C. make arbitrage profits buying CAD from the dealer and selling it in the interbank market.

**Solution:** A is correct. The arbitrage relationship is not violated: the dealer's bid (offer) is not above (below) the interbank market's offer (bid). The implied interbank cross rate for JPY/CAD is 79.84/79.86 (from Question 2).

---

**Question 5.** A market participant is considering the following transactions:

| Transaction   | Description                                             |
|---------------|---------------------------------------------------------|
| Transaction 1 | Buy CAD 100 million against the USD at 15:30 London time |
| Transaction 2 | Sell CAD 100 million against the KRW at 21:30 London time |
| Transaction 3 | Sell CAD 10 million against the USD at 15:30 London time |

Given the proposed transactions, what is the most likely ranking of the bid–offer spreads, from tightest to widest, under normal market conditions?

- A. Transactions 1, 2, 3
- B. Transactions 2, 1, 3
- C. Transactions 3, 1, 2

**Solution:** C is correct. The CAD/USD currency pair is most liquid when New York and London overlap (approximately 13:00–16:00 London time). Transaction 3 is for a smaller amount than Transaction 1, giving it the tightest spread. Transaction 1 is for a larger amount in the same liquid period. Transaction 2 involves a less liquid currency pair (KRW/CAD), occurs outside normal dealing hours in all three major centers, and is also for a large amount—giving it the widest spread.

---

## 4. Forward Markets

Outright forward contracts (often referred to simply as forwards) are agreements to exchange one currency for another on a future date at an exchange rate agreed upon today. Any exchange rate transaction that has a settlement date longer than T + 2 is a forward contract.

Forward exchange rates must satisfy an arbitrage relationship that equates the investment return on two alternative but equivalent investments. To simplify the explanation of this arbitrage relationship and to focus on the intuition behind forward rate calculations, we will ignore the bid–offer spread on exchange rates and money market instruments. In addition, we will alter our exchange rate notation from price/base currency (P/B) to "foreign/domestic currency" (f/d), making the assumption that the domestic currency for an investor is the base currency in the exchange rate quotation. Using this (f/d) notation will make it easier to illustrate the choice an investor faces between domestic and foreign investments, as well as the arbitrage relationships that equate the returns on these investments when their risk characteristics are equivalent.

Consider an investor with one unit of domestic currency to invest for one year. The investor faces two alternatives:

**A.** Invest cash for one year at the domestic risk-free rate (i_d). At the end of the year, the investment would be worth (1 + i_d).

**B.** Convert the domestic currency to foreign currency at the spot rate S_(f/d) and invest for one year at the foreign risk-free rate (i_f). At the end of the period, the investor would have S_(f/d)(1 + i_f) units of foreign currency. These funds then must be converted back to the investor's domestic currency. If the exchange rate to be used for this end-of-year conversion is set at the start of the period using a one-year forward contract, then the investor will have eliminated the foreign exchange risk associated with converting at an unknown future spot rate. If we let F_(f/d) denote the forward rate, the investor would obtain (1/F_(f/d)) units of the domestic currency for each unit of foreign currency sold forward. Hence, in domestic currency, at the end of the year, the investment would be worth S_(f/d)(1 + i_f)(1/F_(f/d)).

The two investment alternatives (A and B) are risk free and therefore must offer the same return. If they did not offer the same return, investors could earn a riskless arbitrage profit by borrowing in one currency, lending in the other, and using the spot and forward exchange markets to eliminate currency risk. Equating the returns on these two alternatives leads to the following relationship:

> (1 + i_d) = S_(f/d) · (1 + i_f) · (1 / F_(f/d))

The right-hand side shows the chronological order of investment B: convert from domestic to foreign currency at the spot rate (S_(f/d)); invest at the foreign risk-free rate (1 + i_f); and at maturity, convert back using the forward rate (1/F_(f/d)).

For simplicity, a one-year horizon was assumed above, but the argument holds for any investment horizon. The risk-free assets used in this arbitrage relationship are typically bank deposits quoted using the appropriate Market Reference Rate (MRR) for each currency. The day count convention for MRR deposits may be Actual/360 or Actual/365. The main exception to Actual/360 is GBP, for which the convention is Actual/365. For the purposes of this discussion, we use Actual/360 consistently.

Incorporating this day count convention into the arbitrage formula:

> (1 + i_d · [Actual/360]) = S_(f/d) · (1 + i_f · [Actual/360]) · (1 / F_(f/d))

Rearranging to isolate the forward rate yields **Equation 1**:

> **F_(f/d) = S_(f/d) · (1 + i_f · [Actual/360]) / (1 + i_d · [Actual/360])**   *(Covered Interest Rate Parity)*

Equation 1 describes **covered interest rate parity**. It is based on an arbitrage relationship among risk-free interest rates and spot and forward exchange rates. Because of this arbitrage relationship, Equation 1 can also be described as saying that the covered (i.e., currency-hedged) interest rate differential between the two markets is zero.

The covered interest rate parity equation can also be rearranged to give an expression for the **forward premium or discount**:

> F_(f/d) − S_(f/d) = S_(f/d) · (i_f − i_d) · [Actual/360] / (1 + i_d · [Actual/360])

The domestic currency will trade at a forward premium (F_(f/d) > S_(f/d)) if, and only if, the foreign risk-free interest rate exceeds the domestic risk-free interest rate (i_f > i_d). Equivalently, the foreign currency will trade at a forward discount. In other words, if it is possible to earn more interest in the foreign market than in the domestic market, then the forward discount for the foreign currency will offset the higher foreign interest rate. Otherwise, covered interest rate parity would not hold and arbitrage opportunities would exist.

When the foreign currency is at a higher rate in the forward contract relative to the spot rate, we say that the foreign currency trades at a forward premium. In this case, the foreign risk-free interest rate will be less than the domestic risk-free interest rate. Additionally, the premium or discount is proportional to the spot exchange

## Covered and Uncovered Interest Rate Parity and Forward Rate Parity

the lower-yielding approach and invest the proceeds in the higher-yielding approach, earning riskless arbitrage profits in the process. In real-world financial markets, such a disparity will be quickly arbitraged away so that no further arbitrage profits are available. Covered interest rate parity is thus said to be a no-arbitrage condition.

For covered interest rate parity to hold exactly, it must be assumed that there are zero transaction costs and that the underlying domestic and foreign money market instruments being compared are identical in terms of liquidity, maturity, and default risk. Where capital is permitted to flow freely, spot and forward exchange markets are liquid, and financial market conditions are relatively stress free, covered interest rate differentials are generally found to be close to zero and covered interest rate parity holds.

### Uncovered Interest Rate Parity

According to the uncovered interest rate parity condition, the expected return on an uncovered (i.e., unhedged) foreign currency investment should equal the return on a comparable domestic currency investment. Uncovered interest rate parity states that the change in spot rate over the investment horizon should, on average, equal the differential in interest rates between the two countries. That is, the expected appreciation/depreciation of the exchange rate will just offset the yield differential.

To explain the intuition behind this concept, let's switch, as we did with the examples for covered interest rate parity, from the standard price/base currency notation (P/B) to foreign/domestic currency notation (f/d) in order to emphasize the choice between foreign and domestic investments. As before, we also will assume that for the investor, the base currency is the domestic currency. (In covered interest rate parity, we assumed the investor transacted at a forward rate that was locked in at strategy initiation. In uncovered interest rate parity, the investor is assumed to transact at a future spot rate that is unknown at the time the strategy is initiated and the investor's currency position in the future is not hedged—that is, uncovered.)

For our example, assume that this investor has a choice between a one-year domestic money market instrument and an unhedged one-year foreign-currency-denominated money market investment. Under the assumption of uncovered interest rate parity, the investor will compare the known return on the domestic investment with the expected all-in return on the unhedged foreign-currency-denominated investment (which includes the foreign yield as well as any movements in the exchange rate, in S(f/d) terms). The choice between these two investments will depend on which market offers the higher expected return on an unhedged basis.

For example, assume that the return on the one-year foreign money market instrument is 10% while the return on the one-year domestic money market instrument is 4%. From the investor's perspective, the 4% expected return on the one-year domestic investment in domestic currency terms is known with complete certainty. This is not the case for the uncovered investment in the foreign currency money market instrument.

In domestic currency terms, the investment return on an uncovered (or unhedged) foreign-currency-denominated investment is equal to (1 + i_f)(1 − %ΔS(f/d)) − 1.

Intuitively, the formula says that the investor's return on a foreign investment is a function of both the foreign interest rate and the change in the spot rate, whereby a depreciation in the foreign currency reduces the investor's return. The percentage change in S(f/d) enters with a minus sign because an increase in S(f/d) means the foreign currency declines in value, thereby reducing the all-in return from the domestic currency perspective of our investor. This all-in return depends on future movements in the S(f/d) rate, which cannot be known until the end of the period. This return can be approximated by:

≅ i_f − %ΔS(f/d)

## Learning Module 1 — Currency Exchange Rates: Understanding Equilibrium Value

Note that this approximate formula holds because the product (i × %ΔS) is small compared with the interest rate (i) and the percentage change in the exchange rate (%ΔS). For simplicity of exposition, we will use the ≅ symbol when we introduce an approximation but will subsequently treat the relationship as an equality (=) unless the distinction is important for the issue being discussed.

Using the previous example, consider three cases:

1. The S(f/d) rate is expected to remain unchanged.
2. The domestic currency is expected to appreciate by 10%.
3. The domestic currency is expected to appreciate by 6%.

In the first case, the investor would prefer the foreign-currency-denominated money market investment because it offers a 10% (= 10% − 0%) expected return, while the comparable domestic investment offers only 4%. In the second case, the investor would prefer the domestic investment because the expected return on the foreign-currency-denominated investment is 0% (= 10% − 10%). In the third case, uncovered interest rate parity holds because both investments offer a 4% (for the foreign investment, 10% − 6%) expected return. In this case, the risk-neutral investor is assumed to be indifferent between the alternatives.

Note that in the third case, in which uncovered interest rate parity holds, while the expected return over the one-year investment horizon is the same for both instruments, that expected return is just a point on the distribution of possible total return outcomes. The all-in return on the foreign money market instrument is uncertain because the future S(f/d) rate is uncertain. Hence, when we say that the investor would be indifferent between owning domestic and foreign investments because they both offer the same expected return (4%), we are assuming that the investor is risk neutral (risk-neutral investors base their decisions solely on the expected return and are indifferent to the investments' risk). Thus, uncovered interest rate parity assumes that there are enough risk-neutral investors to force equality of expected returns.

Using our example's foreign/domestic (f/d) notation, uncovered interest rate parity says the expected change in the spot exchange rate over the investment horizon should be reflected in the interest rate differential:

**%ΔS^e(f/d) = i_f − i_d** (Equation 2)

where ΔS^e indicates the change in the spot rate expected for future periods.

Note that Equation 2 cannot hold simultaneously for S(f/d) and S(d/f) (= 1/S(f/d)) because their percentage changes are not of exactly equal magnitude. This reflects our earlier approximation. Using the exact return on the unhedged foreign instrument would alleviate this issue but would produce a less intuitive equation.

In our example, if the yield spread between the foreign and domestic investments is 6% (i_f − i_d = 6%), then this spread implicitly reflects the expectation that the domestic currency will strengthen versus the foreign currency by 6%.

Uncovered interest rate parity assumes that the country with the higher interest rate or money market yield will see its currency depreciate. The depreciation of the currency offsets the initial higher yield so that the (expected) all-in return on the two investment choices is the same. Hence, if the uncovered interest rate parity condition held consistently in the real world, it would rule out the possibility of earning excess returns from going long a high-yield currency and going short a low-yield currency: the depreciation of the high-yield currency would exactly offset the yield advantage that the high-yield currency offers. Taking this scenario to its logical conclusion, if uncovered interest rate parity held at all times, investors would have no incentive to shift capital from one currency to another because expected returns on otherwise identical money market investments would be equal across markets and risk-neutral investors would be indifferent among them.

Most studies have found that over short- and medium-term periods, the rate of depreciation of the high-yield currency is less than what would be implied by uncovered interest rate parity. In many cases, high-yield currencies have been found to strengthen, not weaken. There is, however, evidence that uncovered interest rate parity works better over very long-term horizons.

Such findings have significant implications for foreign exchange investment strategies. If high-yield currencies do not depreciate in line with the path predicted by the uncovered interest rate parity condition, then high-yield currencies should exhibit a tendency to outperform low-yield currencies over time. If so, investors could adopt strategies that overweight high-yield currencies at the expense of low-yield currencies and generate attractive returns in the process. Such approaches are known as FX carry trade strategies. We will discuss them in greater detail later.

### Forward Rate Parity

Forward rate parity states that the forward exchange rate will be an unbiased predictor of the future spot exchange rate. It does not state that the forward rate will be a perfect forecast, just an unbiased one; the forward rate may overestimate or underestimate the future spot rate from time to time, but on average, it will equal the future spot rate. Forward rate parity builds upon two other parity conditions, covered interest rate parity and uncovered interest rate parity.

The covered interest rate parity condition describes the relationship among the spot exchange rate, the forward exchange rate, and interest rates. Keeping the foreign/domestic exchange rate notation (f/d), the arbitrage condition that underlies covered interest rate parity can be rearranged to give an expression for the forward premium or discount:

$$F_{f/d} - S_{f/d} = S_{f/d} \cdot \frac{i_f - i_d}{\left(1 + i_d \cdot \frac{\text{Actual}}{360}\right)}$$

The domestic currency will trade at a forward premium (F(f/d) > S(f/d)) if, and only if, the foreign risk-free interest rate exceeds the domestic risk-free interest rate (i_f > i_d).

For the sake of simplicity, we assume that the investment horizon is one year, so that:

$$F_{f/d} - S_{f/d} = S_{f/d} \cdot \frac{i_f - i_d}{1 + i_d}$$

Because the 1 + i_d denominator will be close to 1, we can approximate the above equation as follows:

$$F_{f/d} - S_{f/d} \approx S_{f/d}(i_f - i_d)$$

This covered interest rate parity equation can be rearranged to show the forward discount or premium as a percentage of the spot rate:

$$\frac{F_{f/d} - S_{f/d}}{S_{f/d}} \approx i_f - i_d$$

We have also shown that if uncovered interest rate parity holds, then the expected change in the spot rate is equal to the interest rate differential:

$$\%\Delta S^e_{f/d} = i_f - i_d$$

We can link the covered interest rate parity and uncovered interest rate parity equations as follows:

$$\frac{F_{f/d} - S_{f/d}}{S_{f/d}} = \%\Delta S^e_{f/d} = i_f - i_d$$

Thus, the forward premium (discount) on a currency, expressed in percentage terms, equals the expected percentage appreciation (depreciation) of the domestic currency (assuming that the uncovered interest rate parity condition holds).

In theory, then, the forward exchange rate will be an unbiased forecast of the future spot exchange rate if both covered and uncovered interest rate parity hold:

**F(f/d) = S^e(f/d)**

This condition is often referred to as **forward rate parity**.

We know covered interest rate parity must hold because it is enforced by arbitrage. The question of whether forward rate parity holds is thus dependent upon whether uncovered interest rate parity holds.

How might uncovered interest rate parity be enforced? It is not enforced by arbitrage because there is no combination of trades that will lock in a (riskless) profit. It could, however, hold if speculators willing to take risk enter the market. If the forward rate is above (below) speculators' expectations of the future spot rate, then risk-neutral speculators will buy the domestic currency in the spot (forward) market and simultaneously sell it in the forward (spot) market. These transactions would push the forward premium into alignment with the consensus expectation of the future spot rate. If the speculators' expectations are correct, they will make a profit.

Note, however, that spot exchange rates are volatile and determined by a complex web of influences: interest rate differentials are only one among many factors. So, speculators can also lose. Because speculators are rarely, if ever, truly risk neutral and without an arbitrage relationship to enforce it, uncovered interest rate parity is often violated. As a result, we can conclude that forward exchange rates are typically poor predictors of future spot exchange rates in the short run. Over the longer term, uncovered interest rate parity and forward rate parity have more empirical support.

### Example 4: Covered and Uncovered Interest Rate Parity — Predictors of Future Spot Rates

An Australia-based fixed-income asset manager is deciding how to allocate money between Australia and Japan. Note that the base currency in the exchange rate quote (AUD) is the domestic currency for the asset manager.

| | |
|---|---|
| JPY/AUD spot rate (mid-market) | 71.78 |
| One-year forward points (mid-market) | −139.4 |
| One-year Australian deposit rate | 3.00% |
| One-year Japanese deposit rate | 1.00% |

**Question 1.** Based on uncovered interest rate parity, over the next year, the expected change in the JPY/AUD rate is closest to a(n):

- A. decrease of 6%.
- B. decrease of 2%.
- C. increase of 2%.

**Solution:** B is correct. The expected depreciation of the Australian dollar (decline in the JPY/AUD rate) is equal to the interest rate differential between Australia and Japan (3% − 1%).

**Question 2.** The best explanation of why this prediction may not be very accurate is that:

- A. covered interest rate parity does hold in this case.
- B. the forward points indicate that a riskless arbitrage opportunity exists.
- C. there is no arbitrage condition that forces uncovered interest rate parity to hold.

**Solution:** C is correct. There is no arbitrage condition that forces uncovered interest rate parity to hold. In contrast, arbitrage virtually always ensures that covered interest rate parity holds. This is the case for our table, where the −139 point discount is calculated from the covered interest rate parity equation.

**Question 3.** Using the forward points to forecast the future JPY/AUD spot rate one year ahead assumes that:

- A. investors are risk neutral.
- B. spot rates follow a random walk.
- C. it is not necessary for uncovered interest rate parity to hold.

**Solution:** A is correct. Using forward rates (i.e., adding the forward points to the spot rate) to forecast future spot rates assumes that uncovered interest rate parity and forward rate parity hold. Uncovered interest rate parity assumes that investors are risk neutral. If these conditions hold, then movements in the spot exchange rate, although they approximate a random walk, will not actually be a random walk because current interest spreads will determine expected exchange rate movements.

**Question 4.** Forecasting that the JPY/AUD spot rate one year from now will equal 71.78 assumes that:

- A. investors are risk neutral.
- B. spot rates follow a random walk.
- C. it is necessary for uncovered interest rate parity to hold.

**Solution:** B is correct. Assuming that the current spot exchange rate is the best predictor of future spot rates assumes that exchange rate movements follow a random walk. If uncovered interest rate parity holds, the current exchange rate will not be the best predictor unless the interest rate differential happens to be zero. Risk neutrality is needed to enforce uncovered interest rate parity, but it will not make the current spot exchange rate the best predictor of future spot rates.

**Question 5.** If the asset manager completely hedged the currency risk associated with a one-year Japanese deposit using a forward rate contract, the one-year all-in holding return, in AUD, would be closest to:

- A. 0%.
- B. 1%.
- C. 3%.

**Solution:** C is correct. A fully hedged JPY investment would provide the same return as the AUD investment: 3%. This represents covered interest rate parity, an arbitrage condition.

**Question 6.** The fixed-income manager collects the following information and uses it, along with the international parity conditions, to estimate investment returns and future exchange rate movements.

| Today's One-Year MRR | Currency Pair | Spot Rate Today |
|---|---|---|
| JPY 0.10% | JPY/USD | 105.40 |
| USD 0.10% | USD/GBP | 1.2303 |
| GBP 3.00% | JPY/GBP | 129.67 |

If covered interest rate parity holds, the all-in one-year investment return to a Japanese investor whose currency exposure to the GBP is fully hedged is closest to:

- A. 0.10%.
- B. 0.17%.
- C. 3.00%.

**Solution:** A is correct. If covered interest rate parity holds (and it very likely does, because this is a pure arbitrage relationship), then the all-in investment return to a Japanese investor in a one-year, fully hedged GBP MRR position would be identical to a one-year JPY MRR position: 0.10%. No calculations are necessary.

**Question 7.** If uncovered interest rate parity holds, today's expected value for the JPY/GBP currency pair one year from now would be closest to:

- A. 126.02.
- B. 129.67.
- C. 130.05.

**Solution:** A is correct. If uncovered interest rate parity holds, then forward rate parity will hold and the expected spot rate one year forward is equal to the one-year forward exchange rate. This forward rate is calculated in the usual manner, given the spot exchange rates and MRRs:

S^e = F = 129.67 × (1.001 / 1.03) = 126.02.

**Question 8.** If uncovered interest rate parity holds, between today and one year from now, the expected movement in the JPY/USD currency pair is closest to:

- A. −1.60%.
- B. +0.00%.
- C. +1.63%.

**Solution:** B is correct. Given uncovered interest rate parity, the expected change in a spot exchange rate is equal to the interest rate differential. At the one-year term, there is no difference between USD MRR and JPY MRR.

---

## Purchasing Power Parity

So far, we have looked at the relationship between exchange rates and interest rate differentials. Now, we turn to examining the relationship between exchange rates and inflation differentials. The basis for this relationship is known as **purchasing power parity (PPP)**.

Various versions of PPP exist. The foundation for all of the versions is the **law of one price**. According to the law of one price, identical goods should trade at the same price across countries when valued in terms of a common currency. To simplify the explanation, as we did with our examples for covered and uncovered interest rate parity, let's continue to use the foreign/domestic currency quote convention (f/d) and the case where the base currency in the P/B notation is the domestic currency for the investor in the f/d notation.

The law of one price asserts that the foreign price of good x, P^x_f, should equal the exchange rate–adjusted price of the identical good in the domestic country, P^x_d:

**P^x_f = S(f/d) × P^x_d**

For example, for a euro-based consumer, if the price of good x in the euro area is EUR 100 and the nominal exchange rate stands at 1.15 USD/EUR, then the price of good x in the United States should equal USD 115.

### Absolute PPP

The **absolute version of PPP** simply extends the law of one price to the broad range of goods and services that are consumed in different countries. Expanding the above to include all goods and services, not just good x, the broad price level of the foreign country (P_f) should equal the currency-adjusted broad price level in the domestic country (P_d):

**P_f = S(f/d) × P_d**

This equation implicitly assumes that all domestic and foreign goods are tradable and that the domestic and foreign price indexes include the same bundle of goods and services with the same exact weights in each country. Rearranging and solving for the nominal exchange rate S(f/d), the absolute version of PPP states that the nominal exchange rate will be determined by the ratio of the foreign and domestic broad price indexes:

**S(f/d) = P_f / P_d**

The absolute version of PPP asserts that the equilibrium exchange rate between two countries is determined entirely by the ratio of their national price levels. However, it is highly unlikely that this relationship actually holds in the real world. The absolute version of PPP assumes that goods arbitrage will equate the prices of all goods and services across countries, but if transaction costs are significant and/or not all goods and services are tradable, then goods arbitrage will be incomplete. Hence, sizable and persistent departures from absolute PPP are likely.

### Relative PPP

However, if it is assumed that transaction costs and other trade impediments are constant over time, it might be possible to show that changes in exchange rates and changes in national price levels are related, even if the relationship between exchange rate levels and national price levels does not hold. According to the **relative version of PPP**, the percentage change in the spot exchange rate (%ΔS(f/d)) will be completely determined by the difference between the foreign and domestic inflation rates (π_f − π_d):

**%ΔS(f/d) ≅ π_f − π_d** (Equation 3)

Intuitively, the relative version of PPP implies that the exchange rate changes to offset changes in competitiveness arising from inflation differentials. For example, if the foreign inflation rate is assumed to be 9% while the domestic inflation rate is assumed to be 5%, then the S(f/d) exchange rate must rise by 4% (%ΔS(f/d) = 9% − 5% = 4%) in order to maintain the relative competitiveness of the two regions: the currency of the high-inflation country should depreciate relative to the currency of the low-inflation country. If the S(f/d) exchange rate remained unchanged, the higher foreign inflation rate would erode the competitiveness of foreign companies relative to domestic companies.

#### Conversion from Absolute Levels to a Rate of Change

We will occasionally need to convert from a relationship expressed in levels of the relevant variables to a relationship among rates of change. If X = (Y × Z), then:

(1 + %ΔX) = (1 + %ΔY)(1 + %ΔZ)

and

%ΔX ≈ %ΔY + %ΔZ

because (%ΔY × %ΔZ) is "small." Similarly, it can be shown that if X = (Y/Z), then:

(1 + %ΔX) = (1 + %ΔY) / (1 + %ΔZ)

and

%ΔX ≈ %ΔY − %ΔZ.

Applying this conversion to the equation for absolute PPP gives Equation 3.

### Ex Ante PPP

Whereas the relative version of PPP focuses on actual changes in exchange rates being driven by actual differences in national inflation rates, the **ex ante version of PPP** asserts that the expected changes in the spot exchange rate are entirely driven by expected differences in national inflation rates. Ex ante PPP tells us that countries that are expected to run persistently high inflation rates should expect to see their currencies depreciate over time, while countries that are expected to run relatively low inflation rates on a sustainable basis should expect to see their currencies appreciate over time. Ex ante PPP can be expressed as:

**%ΔS^e(f/d) = π^e_f − π^e_d** (Equation 4)

where it is understood that the use of expectations (the superscript e) indicates that we are now focused on future periods. That is, %ΔS^e(f/d) represents the expected percentage change in the spot exchange rate, while π^e_d and π^e_f represent the expected domestic and foreign inflation rates over the same period.

Studies have found that while over shorter horizons nominal exchange rate movements may appear random, over longer time horizons nominal exchange rates tend to gravitate toward their long-run PPP equilibrium values.

Exhibit 2 illustrates the success, or lack thereof, of the relative version of PPP at different time horizons: 1 year, 5 years, 10 years, and 15 years for a selection of countries over the period 1990–2020. Each chart plots the inflation differential (vertical axis) against the percentage change in the exchange rate (horizontal axis). If PPP holds, the points should fall along an upward-sloping diagonal line. The first panel of Exhibit 2 indicates no clear relationship between changes in exchange rates and inflation differentials at the one-year time horizon. As the time horizon is lengthened to five years and beyond, however, a strong positive relationship becomes apparent. Hence, PPP appears to be a valid framework for assessing long-run fair value in the FX markets, even though the path to PPP equilibrium may be slow.

**Exhibit 2: Effect of Relative Inflation Rates on Exchange Rates at Different Time Horizons**

**A. 1-Year Intervals**

*Axes: Average Annual Inflation Differential (vertical, −50 to 50) vs. Annual Change in Exchange Rate % (horizontal, −50 to 50)*

**B. 6-Year Intervals**

*Axes: Average Annual Inflation Differential (vertical, −50 to 50) vs. Annual Change in Exchange Rate % (horizontal, −50 to 50)*

**C. 12-Year Intervals**

*Axes: Average Annual Inflation Differential (vertical, −50 to 50) vs. Annual Change in Exchange Rate % (horizontal, −50 to 50)*

**D. 24-Year Intervals**

*Axes: Average Annual Inflation Differential (vertical, −50 to 50) vs. Annual Change in Exchange Rate % (horizontal, −50 to 50)*

Exhibit 3 illustrates the success of the relative version of PPP even in the short run when differences in inflation rates between countries are large. Note that the Brazilian Real–USD exchange rate changes rapidly in the period 1980–1993, mirroring the very large differences in relative inflation between hyperinflationary Brazil and the low-inflation United States. It also indicates that the majority of countries did not have large inflation differentials with the United States, and so 1-year changes in exchange rates cluster near the origin. This mirrors the upper left panel in Exhibit 2 above, which excludes Brazil from the sample of countries.

**Exhibit 3: Effect of Large Differences in Inflation Rates on Exchange Rates over 1-Year Time Horizons**

*Dual-axis chart (1977–1990): REAL/USD exchange rate (left axis, 1.0–3.5) and Differences in Inflation Rates (right axis, −800 to 600). Exchange Rate (left axis) and Differential (right axis) are plotted as separate series.*

---

## The Fisher Effect, Real Interest Rate Parity, and International Parity Conditions

So far, we have examined the relationships between exchange rates and interest rate differentials and between exchange rates and inflation differentials. Now, we will begin to bring these concepts together by examining how exchange rates, interest rates, and inflation rates interact.

### The Fisher Effect

According to what economists call the **Fisher effect**, one can break down the nominal interest rate (i) in a given country into two parts: (1) the real interest rate (r) in that particular country and (2) the expected inflation rate (π^e) in that country:

**i = r + π^e**

To relate this concept to exchange rates, we can write the Fisher equation for both the domestic country and a foreign country. If the Fisher effect holds, the nominal interest rates in both countries will equal the sum of their respective real interest rates and expected inflation rates:

i_d = r_d + π^e_d

i_f = r_f + π^e_f

Let's take a closer look at the macroeconomic forces that drive the trend in nominal yield spreads. Subtracting the top equation from the bottom equation shows that the nominal yield spread between the foreign and domestic countries (i_f − i_d) equals the sum of two parts: (1) the foreign–domestic real yield spread (r_f − r_d) and (2) the foreign–domestic expected inflation differential (π^e_f − π^e_d):

**i_f − i_d = (r_f − r_d) + (π^e_f − π^e_d)**

We can rearrange this equation to solve for the real interest rate differential instead of the nominal interest rate differential:

**(r_f − r_d) = (i_f − i_d) − (π^e_f − π^e_d)**

To tie this material to our previous work on exchange rates, recall our expression for uncovered interest rate parity:

%ΔS^e(f/d) = i_f − i_d

The nominal interest rate spread (i_f − i_d) equals the expected change in the exchange rate (%ΔS^e(f/d)).

Recall also the expression for ex ante PPP:

%ΔS^e(f/d) = π^e_f − π^e_d

The difference in expected inflation rates equals the expected change in the exchange rate. Combining these two expressions, we derive the following:

**i_f − i_d = π^e_f − π^e_d**

The nominal interest rate spread is equal to the difference in expected inflation rates. We can therefore conclude that if uncovered interest rate parity and ex ante PPP hold:

**(r_f − r_d) = 0**

The real yield spread between the domestic and foreign countries (r_f − r_d) will be zero, and the level of real interest rates in the domestic country will be identical to the level of real interest rates in the foreign country.

### Real Interest Rate Parity

The proposition that real interest rates will converge to the same level across different markets is known as the **real interest rate parity condition**.

### The International Fisher Effect

Finally, if real interest rates are equal across markets, then it also follows that the foreign–domestic nominal yield spread is determined solely by the foreign–domestic expected inflation differential:

**i_f − i_d = π^e_f − π^e_d**

This is known as the **international Fisher effect**. The reader should be aware that some authors refer to uncovered interest rate parity as the "international Fisher effect." We reserve this term for the relationship between nominal interest rate differentials and expected inflation differentials because the original (domestic) Fisher effect is a relationship between interest rates and expected inflation.

The international Fisher effect and, by extension, real interest rate parity assume that currency risk is the same throughout the world. However, not all currencies carry the same risk. For example, an emerging country may have a high level of indebtedness, which could result in an elevated level of currency risk (i.e., likelihood of currency depreciation). In this case, because the emerging market currency has higher risk, subtracting the expected inflation rate from the nominal interest rate will result in a calculated real interest rate that is higher than in other countries. Economists typically separate the nominal interest rate into the real interest rate, an inflation premium, and a risk premium. The emerging country's investors will require a risk premium for holding the currency, which will be reflected in nominal and real interest rates that are higher than would be expected under the international Fisher effect and real interest rate parity conditions.

### Example 5: PPP and the International Fisher Effect

An Australia-based fixed-income investment manager is deciding how to allocate her portfolio between Australia and Japan. (As before, the AUD is the domestic currency.) Australia's one-year deposit rate is 3%, considerably higher than Japan's 1% rate, but the Australian dollar is estimated to be roughly 10% overvalued relative to the Japanese yen based on purchasing power parity. Before making her asset allocation, the investment manager considers the implications of interest rate differentials and PPP imbalances.

**Question 1.** All else equal, which of the following events would restore the Australian dollar to its PPP value?

- A. The Japanese inflation rate increases by 2%.
- B. The Australian inflation rate decreases by 10%.
- C. The JPY/AUD exchange rate declines by 10%.

**Solution:** C is correct. If the Australian dollar is overvalued by 10% on a PPP basis, with all else held equal, a depreciation of the JPY/AUD rate by 10% would move the Australian dollar back to equilibrium.

**Question 2.** If real interest rates in Japan and Australia were equal, then under the international Fisher effect, the inflation rate differential between Japan and Australia would be closest to:

- A. 0%.
- B. 2%.
- C. 10%.

## The Impact of Balance of Payments Flows

Nations running large current account surpluses versus the United States might find that their holdings of US dollar–denominated assets exceed the amount they desire to hold in a portfolio context. Actions they might take to reduce their dollar holdings to desired levels could then have a profound negative impact on the dollar's value.

### The Debt Sustainability Channel

The third mechanism through which current account imbalances can affect exchange rates is the so-called debt sustainability channel. According to this mechanism, there should be some upper limit on the ability of countries to run persistently large current account deficits. If a country runs a large and persistent current account deficit over time, eventually it will experience an untenable rise in debt owed to foreign investors. If such investors believe that the deficit country's external debt is rising to unsustainable levels, they are likely to reason that a major depreciation of the deficit country's currency will be required at some point to ensure that the current account deficit narrows significantly and that the external debt stabilizes at a level deemed sustainable.

The existence of persistent current account imbalances will tend to alter the market's notion of what exchange rate level represents the true, long-run equilibrium value. For deficit nations, ever-rising net external debt levels as a percentage of GDP should give rise to steady (but not necessarily smooth) downward revisions in market expectations of the currency's long-run equilibrium value. For surplus countries, ever-rising net external asset levels as a percentage of GDP should give rise to steady upward revisions of the currency's long-run equilibrium value. Hence, one would expect currency values to move broadly in line with trends in debt and/or asset accumulation.

### Persistent Current Account Deficits: The US Current Account and the US Dollar

The historical record indicates that the trend in the US current account has been an important determinant of the long-term swings in the US dollar's value, but also that there can be rather long lags between the onset of a deterioration in the current account balance and an eventual decline in the dollar's value. For example, the US current account balance deteriorated sharply in the first half of the 1980s, yet the dollar soared over that period. The reason for the dollar's strength over that period was that high US real interest rates attracted large inflows of capital from abroad, which pushed the dollar higher despite the large US external imbalance. Eventually, however, concerns regarding the sustainability of the ever-widening US current account deficit triggered a major dollar decline in the second half of the 1980s.

History repeated itself in the second half of the 1990s, with the US current account balance once again deteriorating while the dollar soared over the same period. This time, the dollar's strength was driven by strong foreign direct investment, as well as both debt- and equity-related flows into the United States. Beginning in 2001, however, the ever-widening US current account deficit, coupled with a decline in US interest rates, made it more difficult for the United States to attract the foreign private capital needed to finance its current account deficit. The dollar eventually succumbed to the weight of ever-larger trade and current account deficits and began a multi-year slide, starting in 2002–2003.

Interestingly, the US dollar has undergone three major downward cycles since the advent of floating exchange rates: 1977–1978, 1985–1987, and 2002–2008. In each of those downward cycles, the dollar's slide was driven in large part by concerns over outsized US current account deficits coupled with relatively low nominal and/or real short-term US interest rates, which made it difficult to attract sufficient foreign capital to the United States to finance those deficits.

### Exchange Rate Adjustment in Surplus Nations: Japan and China

Japan and, for a number of years, China represent examples of countries with large current account surpluses and illustrate the pressure that those surpluses can bring to bear on currencies. In the case of Japan, its rising current account surplus has exerted persistent upward pressure on the yen's value versus the dollar over time. Part of this upward pressure simply reflected the increase in demand for yen to pay for Japan's merchandise exports. But some of the upward pressure on the yen might also have stemmed from rising commercial tensions between the United States and Japan.

Protectionist sentiment in the United States rose steadily with the rising bilateral trade deficit that the United States ran with Japan in the postwar period. US policymakers contended that the yen was undervalued and needed to appreciate. With the increasing trade imbalance between the two countries contributing to more heated protectionist rhetoric, Japan felt compelled to tolerate steady upward pressure on the yen. As a result, the yen's value versus the dollar has tended to move in sync with the trend in Japan's current account surplus.

## Capital Flows

Greater financial integration of the world's capital markets and greater freedom of capital to flow across national borders have increased the importance of global financial flows in determining exchange rates, interest rates, and broad asset price trends. One can cite many examples in which global financial flows either caused or contributed to extremes in exchange rates, interest rates, or asset prices.

In numerous cases, global capital flows have helped fuel boom-like conditions in emerging market economies for a while before, suddenly and often without adequate warning, those flows reversed. The reversals often caused a major economic downturn, sovereign default, a serious banking crisis, and/or significant currency depreciation. Excessive emerging market capital inflows often plant the seeds of a crisis by contributing to:

1. an unwarranted appreciation of the emerging market currency,
2. a huge buildup in external indebtedness,
3. an asset bubble,
4. a consumption binge that contributes to explosive growth in domestic credit and/or the current account deficit, or
5. an overinvestment in risky projects and questionable activities.

Governments in emerging markets often resist currency appreciation from excessive capital inflows by using capital controls or selling their currency in the FX market. An example of capital controls is the Brazilian government 2016 tax on foreign exchange transactions to control capital flows and raise government revenue. In general, government control of the exchange rate will not be completely effective because even if a government prohibits investment capital flows, some capital flows will be needed for international trade. In addition, the existence or emergence of black markets for the country's currency will inhibit the ability of the government to fully control the exchange rates for its own currency.

Sometimes, capital flows due to interest rate spreads have little impact on the trend in exchange rates. Consider the case of the Turkish lira. The lira attracted a lot of interest on the part of global fund managers over the 2002–10 period, in large part because of its attractive yields. Turkish–US short-term yield spreads averaged over 1,000 bps during much of this period. As capital flowed into Turkey, the Turkish authorities intervened in the foreign exchange market in an attempt to keep the lira from appreciating. The result was that international investors were not able to reap the anticipated currency gains over this period. While the return from the movement in the spot exchange rate was fairly small, a long Turkish lira/short US dollar carry trade position generated significant long-run returns, mostly from the accumulated yield spread.

One-sided capital flows can persist for long periods. Consider the case of a high-yield, inflation-prone emerging market country that wants to promote price stability and long-term sustainable growth. To achieve price stability, policymakers in the high-yield economy will initiate a tightening in monetary policy by gradually raising the level of domestic interest rates relative to yield levels in the rest of the world. If the tightening in domestic monetary policy is sustained, inflation expectations for the high-yield economy relative to other economies should gradually decline. The combination of sustained wide nominal yield spreads and a steady narrowing in relative inflation expectations should exert upward pressure on the high-yield currency's value, resulting in carry trade profits over long periods.

Policymakers in high-yield markets can also pursue policies which attract foreign investment; such policies might include tighter fiscal policies, liberalization of financial markets, fewer capital flow restrictions, privatization, and/or a better business environment. Such policies should encourage investors to gradually require a lower risk premium to hold the high-yield currency's assets and revise upward their assessment of the long-run equilibrium value of that country's currency.

The historical evidence suggests that the impact of nominal interest rate spreads on the exchange rate tends to be gradual. Monetary policymakers tend to adjust their official lending rates slowly over time—in part because of the uncertainty that policymakers face and in part because the authorities do not want to disrupt the financial markets. This very gradual change in rates implies a very gradual narrowing of the spread between high-yield and low-yield countries. Similarly, the downward trends in inflation expectations and risk premiums in the higher-yield market also tend to unfold gradually. It often takes several years to determine whether structural economic changes will take root and boost the long-run competitiveness of the higher-yield country. Because these fundamental drivers tend to reinforce each other over time, there may be persistence in capital flows and carry trade returns.

### Equity Market Trends and Exchange Rates

Increasing equity prices can also attract foreign capital. Although exchange rates and equity market returns sometimes exhibit positive correlation, the relationship between equity market performance and exchange rates is not stable. The long-run correlation between the US equity market and the dollar, for example, is very close to zero, but over short to medium periods, correlations tend to swing from being highly positive to being highly negative, depending on market conditions. For instance, between 1990 and 1995, the US dollar fell while the US equity market was strong and the Japanese yen soared while Japanese stocks were weak. In contrast, between 1995 and early 2000, the US dollar soared in tandem with a rising US equity market while the yen weakened in tandem with a decline in the Japanese equity market. Such instability in the correlation between exchange rates and equity markets makes it difficult to form judgments on possible future currency moves based solely on expected equity market performance.

Since the global financial crisis, there has been a decidedly negative correlation between the US dollar and the US equity market. Market observers attribute this behavior of the US dollar to its role as a safe haven asset. When investors' appetite for risk is high—that is, when the market is in "risk-on" mode—investor demand for risky assets, such as equities, tends to rise, which drives up their prices. At the same time, investor demand for safe haven assets, such as the dollar, tends to decline, which drives their values lower. The opposite has occurred when the market has been in "risk-off" mode.

## Monetary and Fiscal Policies

As the foregoing discussion indicates, government policies can have a significant impact on exchange rate movements. We now examine the channels through which government monetary and fiscal policies are transmitted.

### The Mundell–Fleming Model

The Mundell–Fleming model describes how changes in monetary and fiscal policy within a country affect interest rates and economic activity, which in turn leads to changes in capital flows and trade and ultimately to changes in the exchange rate. The model focuses only on aggregate demand and assumes there is sufficient slack in the economy to allow increases in output without price level increases.

In this model, expansionary monetary policy affects growth, in part, by reducing interest rates and thereby increasing investment and consumption spending. Given flexible exchange rates and expansionary monetary policy, downward pressure on domestic interest rates will induce capital to flow to higher-yielding markets, putting downward pressure on the domestic currency. The more responsive capital flows are to interest rate differentials, the greater the depreciation of the currency.

Expansionary fiscal policy—either directly through increased spending or indirectly via lower taxes—typically exerts upward pressure on interest rates because larger budget deficits must be financed. With flexible exchange rates and mobile capital, the rising domestic interest rates will attract capital from lower-yielding markets, putting upward pressure on the domestic currency. If capital flows are highly sensitive to interest rate differentials, then the domestic currency will tend to appreciate substantially. If, however, capital flows are immobile and very insensitive to interest rate differentials, the policy-induced increase in aggregate demand will increase imports and worsen the trade balance, creating downward pressure on the currency with no offsetting capital inflows to provide support for the currency.

The specific mix of monetary and fiscal policies in a country can have a profound effect on its exchange rate. Consider first the case of high capital mobility. With floating exchange rates and high capital mobility, a domestic currency will appreciate given a restrictive domestic monetary policy and/or an expansionary fiscal policy that results in higher real interest rates. Similarly, a domestic currency will depreciate given an expansionary domestic monetary policy and/or a restrictive fiscal policy that results in lower real interest rates.

As shown in Exhibit 4, the combination of a restrictive monetary policy and an expansionary fiscal policy (higher real rates) is extremely bullish for a currency when capital mobility is high; likewise, the combination of an expansionary monetary policy and a restrictive fiscal policy (lower real rates) is bearish for a currency. The effect on the currency of monetary and fiscal policies that are both expansionary or both restrictive is indeterminate under conditions of high capital mobility.

**Exhibit 4: Monetary–Fiscal Policy Mix and the Determination of Exchange Rates under Conditions of High Capital Mobility**

*DEM/USD and US Less German Real Interest Rates (bps), 1993–1998. Source: Rosenberg (1996, p. 132).*

When capital mobility is low, the effects of monetary and fiscal policy on exchange rates will operate primarily through trade flows rather than capital flows. The combination of expansionary monetary and fiscal policy will be bearish for a currency. Earlier we said that expansionary fiscal policy will increase imports and hence the trade deficit, creating downward pressure on the currency. Layering on an expansive monetary policy will further boost spending and imports, worsening the trade balance and exacerbating the downward pressure on the currency.

The combination of restrictive monetary and fiscal policy will be bullish for a currency. This policy mix will tend to reduce imports, leading to an improvement in the trade balance.

The impact of expansionary monetary and restrictive fiscal policies (or restrictive monetary and expansionary fiscal policies) on aggregate demand and the trade balance, and hence on the exchange rate, is indeterminate under conditions of low capital mobility. Exhibit 5 summarizes these results.

**Exhibit 5: Monetary–Fiscal Policy Mix and the Determination of Exchange Rates under Conditions of Low Capital Mobility**

|  | Expansionary Monetary Policy | Restrictive Monetary Policy |
|---|---|---|
| **Expansionary Fiscal Policy** | Domestic currency depreciates | Indeterminate |
| **Restrictive Fiscal Policy** | Indeterminate | Domestic currency appreciates |

*Source: Adapted from Rosenberg (1996, p. 133).*

Exhibit 4 is more relevant for the G–10 countries because capital mobility tends to be high in developed economies. Exhibit 5 is more relevant for emerging market economies that restrict capital movement.

A classic case in which a dramatic shift in the policy mix caused dramatic changes in exchange rates was that of Germany in 1990–1992. During that period, the German government pursued a highly expansionary fiscal policy to help facilitate German unification. At the same time, the Bundesbank pursued an extraordinarily restrictive monetary policy to combat the inflationary pressures associated with unification. The expansive fiscal/restrictive monetary policy mix drove German interest rates sharply higher, eventually causing the German currency to appreciate.

### Monetary Models of Exchange Rate Determination

In the Mundell–Fleming model, monetary policy is transmitted to the exchange rate through its impact on interest rates and output. Changes in the price level and/or the inflation rate play no role. Monetary models of exchange rate determination generally take the opposite perspective: output is fixed and monetary policy affects exchange rates primarily through the price level and the rate of inflation. In this section, we briefly describe two variations of the monetary approach to exchange rate determination.

The monetary approach asserts that an X percent rise in the domestic money supply will produce an X percent rise in the domestic price level. Assuming that purchasing power parity holds—that is, that changes in exchange rates reflect changes in relative inflation rates—a money supply–induced increase (decrease) in domestic prices relative to foreign prices should lead to a proportional decrease (increase) in the domestic currency's value.

One of the major shortcomings of the pure monetary approach is the assumption that purchasing power parity holds in both the short and long runs. Because purchasing power parity rarely holds in either the short or medium run, the pure monetary model may not provide a realistic explanation of the impact of monetary forces on the exchange rate.

To rectify that problem, Dornbusch (1976) constructed a modified monetary model that assumes prices have limited flexibility in the short run but are fully flexible in the long run. The long-run flexibility of the price level ensures that any increase in the domestic money supply will give rise to a proportional increase in domestic prices and thus contribute to a depreciation of the domestic currency in the long run, which is consistent with the pure monetary model. If the domestic price level is assumed to be inflexible in the short run, however, the model implies that the exchange rate is likely to overshoot its long-run PPP path in the short run. With inflexible domestic prices in the short run, any increase in the nominal money supply results in a decline in the domestic interest rate. Assuming that capital is highly mobile, the decline in domestic interest rates will precipitate a capital outflow, which in the short run will cause the domestic currency to depreciate below its new long-run equilibrium level. In the long run, once domestic nominal interest rates rise, the currency will appreciate and move into line with the path predicted by the conventional monetary approach.

### Monetary Policy and Exchange Rates: The Historical Evidence

Historically, changes in monetary policy have had a profound impact on exchange rates. In the case of the US dollar, the Federal Reserve's policy of quantitative easing after the global financial crisis resulted in dollar depreciation from mid-2009 to 2011. The subsequent ending of quantitative easing in 2014, along with the anticipation that the United States would raise interest rates before many other countries, played a key role in driving the dollar higher.

Beginning in 2013, Abenomics—fiscal stimulus, monetary easing, and structural reforms—and the use of quantitative easing in Japan led to a steady decline in interest rates and eventually to negative interest rates in 2016. From 2013 to 2015, the value of the yen changed from roughly JPY 90/USD to JPY 120/USD. Likewise, the use of quantitative easing by the European Central Bank in 2015 led to declines in the value of the euro.

Excessively expansionary monetary policies by central banks in emerging markets have often planted the seeds of speculative attacks on their currencies. In the early 1980s, exchange rate crises in Argentina, Brazil, Chile, and Mexico were all preceded by sharp accelerations in domestic credit expansions. In 2012, Venezuela began a period of triple-digit inflation, followed by a massive currency depreciation and an economic crisis.

### The Portfolio Balance Approach

In this section, we re-examine the role fiscal policy plays in determining exchange rates. The Mundell–Fleming model is essentially a short-run model of exchange rate determination. It makes no allowance for the long-term effects of budgetary imbalances that typically arise from sustained fiscal policy actions. The portfolio balance approach to exchange rate determination remedies this limitation. In our previous discussion of the portfolio balance channel, we stated that the currencies of countries with trade deficits will decline over time. We expand that discussion here to more closely examine how exchange rates change over the long term.

In the portfolio balance approach, global investors are assumed to hold a diversified portfolio of domestic and foreign assets, including bonds. The desired allocation is assumed to vary in response to changes in expected return and risk considerations. In this framework, a growing government budget deficit leads to a steady increase in the supply of domestic bonds outstanding. These bonds will be willingly held only if investors are compensated in the form of a higher expected return. Such a return could come from (1) higher interest rates and/or a higher risk premium, (2) immediate depreciation of the currency to a level sufficient to generate anticipation of gains from subsequent currency appreciation, or (3) some combination of these two factors. The currency adjustments required in the second mechanism are the core of the portfolio balance approach.

One of the major insights one should draw from the portfolio balance model is that in the long run, governments that run large budget deficits on a sustained basis could eventually see their currencies decline in value.

The Mundell–Fleming and portfolio balance models can be combined into a single integrated framework in which expansionary fiscal policy under conditions of high capital mobility may be positive for a currency in the short run but negative in the long run. Exhibit 6 illustrates this concept. A domestic currency may rise in value when the expansionary fiscal policy is first put into place. As deficits mount over time and the government's debt obligations rise, however, market participants will begin to wonder how that debt will be financed. If the volume of debt rises to levels that are believed to be unsustainable, market participants may believe that the central bank will eventually be pressured to "monetize" the debt—that is, to buy the government's debt with newly created money. Such a scenario would clearly lead to a rapid reversal of the initial currency appreciation. Alternatively, the market may believe that the government will eventually have to shift toward significant restraint to implement a more restrictive, sustainable fiscal policy over the longer term.

**Exhibit 6: The Short- and Long-Run Response of Exchange Rates to Changes in Fiscal Policy**

|  | Expansionary Monetary Policy | Restrictive Monetary Policy |
|---|---|---|
| **Expansionary Fiscal Policy** | Domestic currency depreciates | Indeterminate |
| **Restrictive Fiscal Policy** | Indeterminate | Domestic currency appreciates |

*Source: Rosenberg (2003).*

## Warning Signs of a Currency Crisis

With government guarantees on their deposit accounts, the banking industry grew rapidly. The largest bank, Kaupthing, experienced asset growth of 30 times between 2000 and 2008. The three banks increased lending rapidly, with many of their loans being long term, resulting in a maturity mismatch of assets and liabilities. The banks' assets were more than 14 times the country's GDP, while foreign debt was five times GDP. The three banks constituted more than 70% of the national stock market capitalization.

The economy expanded at a real growth rate above 20% annually between 2002 and 2005, and many Icelanders left traditional industries to work in the banks. Iceland earned the nickname "Nordic Tiger" as per capita GDP approached USD 70,000 in 2007. The Icelandic krona increased in value against the US dollar by 40% between 2001 and 2007. By 2007, the unemployment rate was less than 1%. Icelanders went on a shopping spree for consumer goods, in part by using loans tied to the value of foreign currencies, motivated by lower interest rates abroad. A 2002 trade surplus turned into a trade deficit in the years 2003–2007. Iceland's external debt in 2008 was more than 7 times its GDP and 14 times its export revenue. Broad-based monetary aggregates grew at a rate of 14%–35% annually from 2002 to 2007. By the fall of 2008, inflation had reached 14%.

As the global financial crisis unfolded in 2008, interbank lending declined and Icelandic banks were unable to roll over their short-term debt. Anxious foreign depositors began withdrawing their funds. In the first half of 2008, the krona depreciated by more than 40% against the euro. As the Icelandic currency declined in value, it became more difficult for the banks to meet depositors' liquidity demands, while at the same time the banks' depreciating krona-denominated assets could not be used for collateral financing.

The three banks collapsed in 2008. Unfortunately for foreign depositors, because of the relative size of the banks, the government guaranteed only domestic deposits. Iceland's central bank became technically insolvent, as its EUR 2 billion in assets was dwarfed by Iceland's debt to foreign banks of EUR 50 billion. Trading in the stock market was suspended in October 2008. When it reopened several days later, the Icelandic Stock Market Index fell by more than 77% as a result of the elimination of the three banks' equity value.

The government attempted to peg the krona to the euro in October 2008 but abandoned the peg one day later. When trading in the currency was resumed later that month, the currency value fell by more than 60% and trading was eventually suspended. Iceland increased interest rates to 18% to stem outflows of krona and imposed capital controls on the selling of krona for foreign currency. The Icelandic economy contracted, and per capita GDP fell 9.2% in 2009. By the spring of 2009, unemployment was 9%. The country subsequently required a bailout from the IMF and its neighbors of USD 4.6 billion.

---

## Summary

Exchange rates are among the most difficult financial market prices to understand and therefore to value. There is no simple, robust framework that investors can rely on in assessing the appropriate level and likely movements of exchange rates.

Most economists believe that there is an equilibrium level or a path to that equilibrium value that a currency will gravitate toward in the long run. Although short- and medium-term cyclical deviations from the long-run equilibrium path can be sizable and persistent, fundamental forces should eventually drive the currency back toward its long-run equilibrium path. Evidence suggests that misalignments tend to build up gradually over time. As these misalignments build, they are likely to generate serious economic imbalances that will eventually lead to correction of the underlying exchange rate misalignment.

We have described how changes in monetary policy, fiscal policy, current account trends, and capital flows affect exchange rate trends, as well as what role government intervention and capital controls can play in counteracting potentially undesirable exchange rate movements. We have made the following key points:

- Spot exchange rates apply to trades for the next settlement date (usually T+2) for a given currency pair. Forward exchange rates apply to trades to be settled at any longer maturity.

- Market makers quote bid and offer prices (in terms of the price currency) at which they will buy or sell the base currency.
  - The offer price is always higher than the bid price.
  - The counterparty that asks for a two-sided price quote has the option (but not the obligation) to deal at either the bid or offer price quoted.
  - The bid–offer spread depends on (1) the currency pair involved, (2) the time of day, (3) market volatility, (4) the transaction size, and (5) the relationship between the dealer and the client. Spreads are tightest in highly liquid currency pairs, when the key market centers are open, and when market volatility is relatively low.

- Absence of arbitrage requires the following:
  - The bid (offer) shown by a dealer in the interbank market cannot be higher (lower) than the current interbank offer (bid) price.
  - The cross-rate bids (offers) posted by a dealer must be lower (higher) than the implied cross-rate offers (bids) available in the interbank market. If they are not, then a triangular arbitrage opportunity arises.

- Forward exchange rates are quoted in terms of points to be added to the spot exchange rate. If the points are positive (negative), the base currency is trading at a forward premium (discount). The points are proportional to the interest rate differential and approximately proportional to the time to maturity.

- International parity conditions show us how expected inflation, interest rate differentials, forward exchange rates, and expected future spot exchange rates are linked. In an ideal world,
  - relative expected inflation rates should determine relative nominal interest rates,
  - relative interest rates should determine forward exchange rates, and
  - forward exchange rates should correctly anticipate the path of the future spot exchange rate.

- International parity conditions tell us that countries with high (low) expected inflation rates should see their currencies depreciate (appreciate) over time, that high-yield currencies should depreciate relative to low-yield currencies over time, and that forward exchange rates should function as unbiased predictors of future spot exchange rates.

- With the exception of covered interest rate parity, which is enforced by arbitrage, the key international parity conditions rarely hold in either the short or medium term. However, the parity conditions tend to hold over relatively long horizons.

- According to the theory of covered interest rate parity, a foreign-currency-denominated money market investment that is completely hedged against exchange rate risk in the forward market should yield exactly the same return as an otherwise identical domestic money market investment.

- According to the theory of uncovered interest rate parity, the expected change in a domestic currency's value should be fully reflected in domestic–foreign interest rate spreads. Hence, an unhedged foreign-currency-denominated money market investment is expected to yield the same return as an otherwise identical domestic money market investment.

- According to the ex ante purchasing power parity condition, expected changes in exchange rates should equal the difference in expected national inflation rates.

- If both ex ante purchasing power parity and uncovered interest rate parity held, real interest rates across all markets would be the same. This result is real interest rate parity.

- The international Fisher effect says that the nominal interest rate differential between two currencies equals the difference between the expected inflation rates. The international Fisher effect assumes that risk premiums are the same throughout the world.

- If both covered and uncovered interest rate parity held, then forward rate parity would hold and the market would set the forward exchange rate equal to the expected spot exchange rate: the forward exchange rate would serve as an unbiased predictor of the future spot exchange rate.

- Most studies have found that high-yield currencies do not depreciate and low-yield currencies do not appreciate as much as yield spreads would suggest over short to medium periods, thus violating the theory of uncovered interest rate parity.

- Carry trades overweight high-yield currencies at the expense of low-yield currencies. Historically, carry trades have generated attractive returns in benign market conditions but tend to perform poorly (i.e., are subject to crash risk) when market conditions are highly volatile.

- According to a balance of payments approach, countries that run persistent current account deficits will generally see their currencies weaken over time. Similarly, countries that run persistent current account surpluses will tend to see their currencies appreciate over time.

- Large current account imbalances can persist for long periods of time before they trigger an adjustment in exchange rates.

- Greater financial integration of the world's capital markets and greater freedom of capital to flow across national borders have increased the importance of global capital flows in determining exchange rates.

- Countries that institute relatively tight monetary policies, introduce structural economic reforms, and lower budget deficits will often see their currencies strengthen over time as capital flows respond positively to relatively high nominal interest rates, lower inflation expectations, a lower risk premium, and an upward revision in the market's assessment of what exchange rate level constitutes long-run fair value.

- Monetary policy affects the exchange rate through a variety of channels. In the Mundell–Fleming model, it does so primarily through the interest rate sensitivity of capital flows, strengthening the currency when monetary policy is tightened and weakening it when monetary policy is eased. The more sensitive capital flows are to the change in interest rates, the greater the exchange rate's responsiveness to the change in monetary policy.

- In the monetary model of exchange rate determination, monetary policy is deemed to have a direct impact on the actual and expected path of inflation, which, via purchasing power parity, translates into a corresponding impact on the exchange rate.

- Countries that pursue overly easy monetary policies will see their currencies depreciate over time.

- In the Mundell–Fleming model, an expansionary fiscal policy typically results in a rise in domestic interest rates and an increase in economic activity. The rise in domestic interest rates should induce a capital inflow, which is positive for the domestic currency, but the rise in economic activity should contribute to a deterioration of the trade balance, which is negative for the domestic currency. The more mobile capital flows are, the greater the likelihood that the induced inflow of capital will dominate the deterioration in trade.

- Under conditions of high capital mobility, countries that simultaneously pursue expansionary fiscal policies and relatively tight monetary policies should see their currencies strengthen over time.

- The portfolio balance model of exchange rate determination asserts that increases in government debt resulting from a rising budget deficit will be willingly held by investors only if they are compensated in the form of a higher expected return. The higher expected return could come from (1) higher interest rates and/or a higher risk premium, (2) depreciation of the currency to a level sufficient to generate anticipation of gains from subsequent currency appreciation, or (3) some combination of the two.

- Surges in capital inflows can fuel boom-like conditions, asset price bubbles, and currency overvaluation.

- Many consider capital controls to be a legitimate part of a policymaker's toolkit. The IMF believes that capital controls may be needed to prevent exchange rates from overshooting, asset price bubbles from forming, and future financial conditions from deteriorating.

- The evidence indicates that government policies have had a significant impact on the course of exchange rates. Relative to developed countries, emerging markets may have greater success in managing their exchange rates because of their large foreign exchange reserve holdings, which appear sizable relative to the limited turnover of FX transactions in many emerging markets.

- Although each currency crisis is distinct in some respects, the following factors were identified in one or more studies:
  1. Prior to a currency crisis, the capital markets have been liberalized to allow the free flow of capital.
  2. There are large inflows of foreign capital (relative to GDP) in the period leading up to a crisis, with short-term funding denominated in a foreign currency being particularly problematic.
  3. Currency crises are often preceded by (and often coincide with) banking crises.
  4. Countries with fixed or partially fixed exchange rates are more susceptible to currency crises than countries with floating exchange rates.
  5. Foreign exchange reserves tend to decline precipitously as a crisis approaches.
  6. In the period leading up to a crisis, the currency has risen substantially relative to its historical mean.
  7. The terms of trade (exports relative to imports) often deteriorate before a crisis.
  8. Broad money growth and the ratio of M2 (a measure of money supply) to bank reserves tend to rise prior to a crisis.
  9. Inflation tends to be significantly higher in pre-crisis periods compared with tranquil periods.

---

## Appendix: Currency Codes Used

| Code | Currency |
|------|----------|
| USD | US dollar |
| EUR | Euro |
| GBP | UK pound |
| JPY | Japanese yen |
| MXN | Mexican peso |
| CHF | Swiss franc |
| CAD | Canadian dollar |
| SEK | Swedish krona |
| AUD | Australian dollar |
| KRW | Korean won |
| NZD | New Zealand dollar |