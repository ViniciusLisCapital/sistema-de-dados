# Currency Exchange Rates: Understanding Equilibrium Value

## Learning Outcomes

The candidate should be able to:

- Calculate and interpret the bid–offer spread on a spot or forward currency quotation and describe the factors that affect the bid–offer spread
- Identify a triangular arbitrage opportunity and calculate its profit, given the bid–offer quotations for three currencies
- Explain spot and forward rates and calculate the forward premium/discount for a given currency
- Calculate the mark-to-market value of a forward contract
- Explain international parity conditions (covered and uncovered interest rate parity, forward rate parity, purchasing power parity, and the international Fisher effect)
- Describe relations among the international parity conditions
- Evaluate the use of the current spot rate, the forward rate, purchasing power parity, and uncovered interest parity to forecast future spot exchange rates
- Explain approaches to assessing the long-run fair value of an exchange rate
- Describe the carry trade and its relation to uncovered interest rate parity and calculate the profit from a carry trade
- Explain how flows in the balance of payment accounts affect currency exchange rates
- Explain the potential effects of monetary and fiscal policy on exchange rates
- Describe objectives of central bank or government intervention and capital controls and describe the effectiveness of intervention and capital controls
- Describe warning signs of a currency crisis

## Introduction

Exchange rates are well known to follow a random walk, whereby fluctuations from one day to the next are unpredictable. The business of currency forecasting can be a humbling experience. Alan Greenspan, former chair of the US Federal Reserve Board, famously noted that "having endeavored to forecast exchange rates for more than half a century, I have understandably developed significant humility about my ability in this area."

Hence, our discussion is not about predicting exchange rates but about the tools the reader can use to better understand long-run equilibrium value. This outlook helps guide the market participant's decisions with respect to risk exposures, as well as whether currency hedges should be implemented and, if so, how they should be managed. After discussing the basics of exchange rate transactions, we present the main theories for currency determination—starting with the international parity conditions—and then describe other important influences, such as current account balances, capital flows, and monetary and fiscal policy.

Although these fundamentals-based models usually perform poorly in predicting future exchange rates in the short run, they are crucial for understanding long-term currency value. Thus, we proceed as follows:

- We review the basic concepts of the foreign exchange market covered in the CFA Program Level I curriculum and expand this previous coverage to incorporate more material on bid–offer spreads.
- We then begin to examine determinants of exchange rates, starting with longer-term interrelationships among exchange rates, interest rates, and inflation rates embodied in the international parity conditions. These parity conditions form the key building blocks for many long-run exchange rate models.
- We also examine the foreign exchange (FX) carry trade, a trading strategy that exploits deviations from uncovered interest rate parity and discuss the relationship between a country's exchange rate and its balance of payments.
- We then examine how monetary and fiscal policies can indirectly affect exchange rates by influencing the various factors described in our exchange rate model.
- The subsequent section focuses on direct public sector actions in foreign exchange markets, both through capital controls and by foreign exchange market intervention (buying and selling currencies for policy purposes).
- The last section examines historical episodes of currency crisis and some leading indicators that may signal the increased likelihood of a crisis.

## Foreign Exchange Market Concepts

### Exchange Rate Notation and Pricing

We begin with a brief review of some of the basic conventions of the FX market that were covered in the CFA Program Level I curriculum. In this section, we cover (1) the basics of exchange rate notation and pricing, (2) arbitrage pricing constraints on spot rate foreign exchange quotes, and (3) forward rates and covered interest rate parity.

An exchange rate is the price of the base currency expressed in terms of the price currency. For example, a USD/EUR rate of 1.1650 means the euro, the base currency, costs 1.1650 US dollars (an appendix defines the three-letter currency codes). The exact notation used to represent exchange rates can vary widely between sources, and occasionally the same exchange rate notation will be used by different sources to mean completely different things. The reader should be aware that the notation used here may not be the same as that encountered elsewhere. To avoid confusion, we will identify exchange rates using the convention of "P/B," referring to the price of the base currency, "B," expressed in terms of the price currency, "P."

### Notation Conventions

Notation is generally not standardized in global foreign exchange markets, and there are several common ways of expressing the same currency pair (e.g., JPY/USD, USD:JPY, $/¥). What is common in FX markets, however, is the concept of a "base" and a "price" currency when setting exchange rates. We will sometimes switch to discussing a "domestic" and a "foreign" currency, quoted as foreign/domestic (f/d). This is only an illustrative device for more easily explaining various theoretical concepts. The candidate should be aware that currency pairs are not described in terms of "foreign" and "domestic" currencies in professional FX markets. This is because what is the "foreign" and what is the "domestic" currency depend on where one is located, which can lead to confusion. For instance, what is "foreign" and what is "domestic" for a Middle Eastern investor trading CHF against GBP with the New York branch of a European bank, with the trade ultimately booked at the bank's headquarters in Paris?

The spot exchange rate is usually used for settlement on the second business day after the trade date, referred to as T + 2 settlement (the exception being CAD/USD, for which standard spot settlement is T + 1). In foreign exchange markets—as in other financial markets—market participants are presented with a two-sided price in the form of a bid price and an offer price (also called an ask price) quoted by potential counterparties. The bid price is the price, defined in terms of the price currency, at which the counterparty is willing to buy one unit of the base currency. Similarly, the offer price is the price, in terms of the price currency, at which that counterparty is willing to sell one unit of the base currency. For example, given a price request from a client, a dealer might quote a two-sided price on the spot USD/EUR exchange rate of 1.1648/1.1652. This means that the dealer is willing to pay USD 1.1648 to buy one EUR and that the dealer is willing to sell one EUR for USD 1.1652.

There are two points to bear in mind about bid–offer quotes:

1. The offer price is always higher than the bid price. The bid–offer spread—the difference between the offer price and the bid price—is the compensation that counterparties seek for providing foreign exchange to other market participants.

2. The party in the transaction who requests a two-sided price quote has the option (but not the obligation) to deal at either the bid (to sell the base currency) or the offer (to buy the base currency) quoted by the dealer. If the party chooses to trade at the quoted prices, the party is said to have either "hit the bid" or "paid the offer." If the base currency is being sold, the party is said to have hit the bid. If the base currency is being bought, the party is said to have paid the offer.

### The Interbank Market and Client Pricing

We will distinguish here between the bid–offer pricing a client receives from a dealer and the pricing a dealer receives from the interbank market. Dealers buy and sell foreign exchange among themselves in what is called the interbank market. This global network for exchanging currencies among professional market participants allows dealers to adjust their inventories and risk positions, distribute foreign currencies to end users who need them, and transfer foreign exchange rate risk to market participants who are willing to bear it. The interbank market is typically for dealing sizes of at least 1 million units of the base currency. Of course, the dealing amount can be larger than 1 million units; indeed, interbank market trades generally are measured in terms of multiples of a million units of the base currency. Please note that many non-bank entities can now access the interbank market. They include institutional asset managers and hedge funds.

The bid–offer spread a dealer provides to most clients typically is slightly wider than the bid–offer spread observed in the interbank market. Most currencies, except for the yen, are quoted to four decimal places. The fourth decimal place (0.0001) is referred to as a "pip." The yen is typically quoted to just two decimal places; in yen quotes, the second decimal place (0.01) is referred to as a pip.

For example, if the quote in the interbank USD/EUR spot market is 1.1649/1.1651 (two pips wide), the dealer might quote a client a bid–offer of 1.1648/1.1652 (four pips wide) for a spot USD/EUR transaction. When the dealer buys (sells) the base currency from (to) a client, the dealer is typically expecting to quickly turn around and sell (buy) the base currency in the interbank market. This offsetting transaction allows the dealer to divest the risk exposure assumed by providing a two-sided price to the client and to hopefully make a profit. Continuing our example, suppose the dealer's client hits the dealer's bid and sells EUR to the dealer for USD 1.1648. The dealer is now long EUR (and short USD) and wants to cover this position in the interbank market. To do this, the dealer sells the EUR in the interbank market by hitting the interbank bid. As a result, the dealer bought EUR from the client at USD 1.1648 and then sold the EUR in the interbank for USD 1.1649. This gives the dealer a profit of USD 0.0001 (one pip) for every EUR transacted. This one pip translates into a profit of USD 100 per EUR million bought from the client. If, instead of hitting his bid, the client paid the offer (1.1652), then the dealer could pay the offer in the interbank market (1.1651), earning a profit of one pip.

### Factors Affecting Bid–Offer Spreads

The size of the bid–offer spread quoted to dealers' clients in the FX market can vary widely across exchange rates and is not constant over time, even for a single exchange rate. The size of this spread depends primarily on three factors:

- the bid–offer spread in the interbank foreign exchange market for the two currencies involved,
- the size of the transaction, and
- the relationship between the dealer and the client.

We examine each factor in turn.

#### Liquidity and Currency Pair

The size of the bid–offer spread quoted in the interbank market depends on the liquidity in this market. Liquidity is influenced by several factors:

1. The currency pair involved. Market participation is greater for some currency pairs than for others. Liquidity in the major currency pairs—for example, USD/EUR, JPY/USD, and USD/GBP—can be quite high. These markets are almost always deep, with multiple bids and offers from market participants around the world. In other currency pairs, particularly some of the more obscure currency cross rates (e.g., MXN/CHF), market participation is much thinner and consequently the bid–offer spread in the interbank market will be wider.

2. The time of day. The interbank FX markets are most liquid when the major FX trading centers are open. Business hours in London and New York—the two largest FX trading centers—overlap from approximately 8:00 a.m. to 11:00 a.m. New York time. The interbank FX market for most currency pairs is typically most liquid during these hours. After London closes, liquidity is thinner through the New York afternoon. The Asian session starts when dealers in Tokyo, Singapore, and Hong Kong SAR open for business, typically by 7:00 p.m. New York time. For most currency pairs, however, the Asian session is not as liquid as the London and New York sessions. Although FX markets are open 24 hours a day on business days, between the time New York closes and the time Asia opens, liquidity in interbank markets can be very thin because Sydney, Australia, tends to be the only active trading center during these hours. For reference, the chart below shows a 24-hour period from midnight (00:00) to midnight (24:00) London time, corresponding standard times in Tokyo and New York, and, shaded in grey, the approximate hours of the most liquid trading periods in each market.

**Standard Time and Approximate FX Trading Hours in Major Markets: Midnight to Midnight (London Time)**

| Tokyo | 09:00 | 13:00 | 17:00 | 21:00 | 01:00 | 05:00 | 09:00 |
|-------|-------|-------|-------|-------|-------|-------|-------|
|       |       |       |       |       | Day+1 | Day+1 | Day+1 |
| London | 00:00 | 04:00 | 08:00 | 12:00 | 16:00 | 20:00 | 24:00 |
| New York | 19:00 | 23:00 | 03:00 | 07:00 | 11:00 | 15:00 | 19:00 |
|       | Day−1 | Day−1 |       |       |       |       |       |

3. Market volatility. As in any financial market, when major market participants have greater uncertainty about the factors influencing market pricing, they will attempt to reduce their risk exposures and/or charge a higher price for taking on risk. In the FX market, this response implies wider bid–offer spreads in both the interbank and broader markets. Geopolitical events (e.g., war, civil strife), market crashes, and major data releases (e.g., US non-farm payrolls) are among the factors that influence spreads and liquidity.

#### Transaction Size

The size of the transaction can also affect the bid–offer spread shown by a dealer to clients. Typically, the larger the transaction, the further away from the current spot exchange rate the dealing price will be. Hence, a client who asks a dealer for a two-sided spot CAD/USD price on, for example, USD 50 million will be shown a wider bid–offer spread than a client who asks for a price on USD 1 million. The wider spread reflects the greater difficulty the dealer faces in offsetting the foreign exchange risk of the position in the interbank FX market. Smaller dealing sizes can also affect the bid–offer quote shown to clients. "Retail" quotes are typically for dealing sizes smaller than 1 million units of the base currency and can range all the way down to foreign exchange transactions conducted by individuals. The bid–offer spreads for these retail transactions can be very large compared with those in the interbank market.

#### Client Relationship

The relationship between the dealer and the client can also affect the size of the bid–offer spread shown by the dealer. For many clients, the spot foreign exchange business is only one business service among many that a dealer provides to that client. For example, the dealer firm might also transact in bond and/or equity securities with the same client. In a competitive business environment, in order to win the client's business for these other services, the dealer might provide a tighter (i.e., smaller) bid–offer spot exchange rate quote. The dealer might also give tighter bid–offer quotes in order to win repeat FX business. A client's credit risk can also be a factor. A client with a poor credit profile may be quoted a wider bid–offer spread than one with good credit. Given the short settlement cycle for spot FX transactions (typically two business days), however, credit risk is not the most important factor in determining the client's bid–offer spread on spot exchange rates.

## Arbitrage Constraints on Spot Exchange Rate Quotes

The bid–offer quotes a dealer shows in the interbank FX market must respect two arbitrage constraints; otherwise the dealer creates riskless arbitrage opportunities for other interbank market participants. We will confine our attention to the interbank FX market because arbitrage presumes the ability to deal simultaneously with different market participants and in different markets, the ability to access "wholesale" bid–offer quotes, and the market sophistication to spot arbitrage opportunities.

First, the bid shown by a dealer in the interbank market cannot be higher than the current interbank offer, and the offer shown by a dealer cannot be lower than the current interbank bid. If the bid–offer quotes shown by a dealer are inconsistent with the then-current interbank market quotes, other market participants will buy from the cheaper source and sell to the more expensive source. This arbitrage will eventually bring the two prices back into line. For example, suppose that the current spot USD/EUR price in the interbank market is 1.1649/1.1651. If a dealer showed a misaligned price quote of 1.1652/1.1654, then other market participants would pay the offer in the interbank market, buying EUR at a price of USD 1.1651, and then sell the EUR to the dealer by hitting the dealer's bid at USD 1.1652—thereby making a riskless profit of one pip on the trade. This arbitrage would continue as long as the dealer's bid–offer quote violated the arbitrage constraint.

Second, the cross-rate bids (offers) posted by a dealer must be lower (higher) than the implied cross-rate offers (bids) available in the interbank market. A currency dealer located in a given country typically provides exchange rate quotations between that country's currency and various foreign currencies. If a particular currency pair is not explicitly quoted, it can be inferred from the quotes for each currency in terms of the exchange rate with a third nation's currency. For example, given exchange rate quotes for the currency pairs A/B and C/B, we can back out the implied cross rate of A/C. This implied A/C cross rate must be consistent with the A/B and C/B rates. This again reflects the basic principle of arbitrage: If identical financial products are priced differently, then market participants will buy the cheaper one and sell the more expensive one until the price difference is eliminated. In the context of FX cross rates, there are two ways to trade currency A against currency C: (1) using the cross rate A/C or (2) using the A/B and C/B rates. Because, in the end, both methods involve selling (buying) currency C in order to buy (sell) currency A, the exchange rates for these two approaches must be consistent. If the exchange rates are not consistent, the arbitrageur will buy currency C from a dealer if it is undervalued (relative to the cross rate) and sell currency A. If currency C is overvalued by a dealer (relative to the cross rate), it will be sold and currency A will be bought.

### Triangular Arbitrage Calculation

To illustrate this triangular arbitrage among three currencies, suppose that the interbank market bid–offer in USD/EUR is 1.1649/1.1651 and that the bid–offer in JPY/USD is 105.39/105.41. We need to use these two interbank bid–offer quotes to calculate the market-implied bid–offer quote on the JPY/EUR cross rate.

Begin by considering the transactions required to sell JPY and buy EUR, going through the JPY/USD and USD/EUR currency pairs. We can view this process intuitively as follows:

Sell JPY / Buy EUR = (Sell JPY / Buy USD) × (Sell USD / Buy EUR)

Note that "Buy USD" and "Sell USD" in the expressions on the right-hand side of the equal sign will cancel out to give the JPY/EUR cross rate. In equation form, we can represent this relationship as follows:

(JPY/EUR) = (JPY/USD) × (USD/EUR)

Now, let's incorporate the bid–offer rates in order to do the JPY/EUR calculation. A rule of thumb is that when we speak of a bid or offer exchange rate, we are referring to the bid or offer for the currency in the denominator (the base currency).

i. The left-hand side of the above equal sign is "Sell JPY, Buy EUR." In the JPY/EUR price quote, the EUR is in the denominator (it is the base currency). Because we want to buy the currency in the denominator, we need an exchange rate that is an offer rate. Thus, we will be calculating the offer rate for JPY/EUR.

ii. The first term on the right-hand side of the equal sign is "Sell JPY, Buy USD." Because we want to buy the currency in the denominator of the quote, we need an exchange rate that is an offer rate. Thus, we need the offer rate for JPY/USD.

iii. The second term on the right-hand side of the equal sign is "Sell USD, Buy EUR." Because we want to buy the currency in the denominator of the quote, we need an exchange rate that is an offer rate. Thus, we need the offer rate for USD/EUR.

Combining all of this conceptually and putting in the relevant offer rates leads to a JPY/EUR offer rate of

(JPY/EUR)offer = (JPY/USD)offer × (USD/EUR)offer = 105.41 × 1.1651 = 122.81

Perhaps not surprisingly, calculating the implied JPY/EUR bid rate uses the same process as above but with "Buy JPY, Sell EUR" for the left-hand side of the equation, which leads to

(JPY/EUR)bid = (JPY/USD)bid × (USD/EUR)bid = 105.39 × 1.1649 = 122.77

As one would expect, the implied cross-rate bid (122.77) is less than the offer (122.81).

This simple formula seems relatively straightforward: To get the implied bid cross rate, simply multiply the bid rates for the other two currencies. However, depending on the quotes provided, it may be necessary to invert one of the quotes in order to complete the calculation.

This is best illustrated with an example. Consider the case of calculating the implied GBP/EUR cross rate if you are given USD/GBP and USD/EUR quotes. Simply using the provided quotes will not generate the desired GBP/EUR cross rate:

(GBP/EUR) ≠ (USD/GBP) × (USD/EUR)

Instead, because the USD is in the numerator in both currency pairs, we will have to invert one of the pairs to derive the GBP/EUR cross rate.

The following equation represents the cross-rate relationship we are trying to derive:

(GBP/EUR) = (GBP/USD) × (USD/EUR)

But we don't have the GBP/USD quote. We can, however, invert the USD/GBP quote and use that in our calculation. Let's assume the bid–offer quote provided is for USD/GBP and is 1.2302/1.2304. With this quote, if we want to buy GBP (the currency in the denominator), we will buy GBP at the offer and the relevant quote is 1.2304. We can invert this quote to arrive at the needed GBP/USD quote: 1 ÷ 1.2304 = 0.81274.

Note that, in this example, when we buy the GBP, we are also selling the USD. When we invert the provided USD/GBP offer quote, we obtain 0.81274 GBP/USD. This is the price at which we sell the USD—that is, the GBP/USD bid. It may help here to remember our rule of thumb from above: When we speak of a bid or offer exchange rate, we are referring to the bid or offer for the currency in the denominator (the base currency).

Similarly, to get a GBP/USD offer, we use the inverse of the USD/GBP bid of 1.2302:

1 ÷ 1.2302 = 0.81288

(Note that we extended the calculated GBP/USD 0.81274/0.81288 quotes to five decimal places to avoid truncation errors in subsequent calculations.)

We can now finish the calculation of the bid and offer cross rates for GBP/EUR. Using the previously provided 1.1649/1.1651 as the bid–offer in USD/EUR, we calculate the GBP/EUR bid rate as follows:

(GBP/EUR)bid = (GBP/USD)bid × (USD/EUR)bid = 0.81274 × 1.1649 = 0.9468

Similarly, the implied GBP/EUR offer rate is

(GBP/EUR)offer = (GBP/USD)offer × (USD/EUR)offer = 0.81288 × 1.1651 = 0.9471

Note that the implied bid rate is less than the implied offer rate, as it must be to prevent arbitrage.

### Observations on Arbitrage Constraints

We conclude this section on arbitrage constraints with some simple observations:

- The arbitrage constraint on implied cross rates is similar to that for spot rates (posted bid rates cannot be higher than the market's offer; posted offer rates cannot be lower than the market's bid). The only difference is that this second arbitrage constraint is applied across currency pairs instead of involving a single currency pair.
- In reality, any violations of these arbitrage constraints will quickly disappear. Both human traders and automatic trading algorithms are constantly on alert for any pricing inefficiencies and will arbitrage them away almost instantly. If Dealer 1 is buying a currency at a price higher than the price at which Dealer 2 is selling it, the arbitrageur will buy the currency from Dealer 2 and resell it to Dealer 1. As a result of buying and selling pressures, Dealer 2 will raise his offer prices and Dealer 1 will reduce her bid prices to the point where arbitrage profits are no longer available.
- Market participants do not need to calculate cross rates manually because electronic dealing machines (which are essentially just specialized computers) will automatically calculate cross bid–offer rates given any two underlying bid–offer rates.

### Example 1: Bid–Offer Rates

The following are spot rate quotes in the interbank market:

| Pair | Quote |
|------|-------|
| USD/EUR | 1.1649/1.1651 |
| JPY/USD | 105.39/105.41 |
| CAD/USD | 1.3199/1.3201 |
| SEK/USD | 9.6300/9.6302 |

**Question 1: What is the bid–offer on the SEK/EUR cross rate implied by the interbank market?**

A. 0.1209/0.1211
B. 8.2656/8.2668
C. 11.2180/11.2201

**Solution:** C is correct. Using the provided quotes and setting up the equations so that the cancellation of terms results in the SEK/EUR quote,

(SEK/EUR) = (SEK/USD) × (USD/EUR)

Hence, to calculate the SEK/EUR bid (offer) rate, we multiply the SEK/USD and USD/EUR bid (offer) rates to get the following:

Bid: 11.2180 = 9.6300 × 1.1649
Offer: 11.2201 = 9.6302 × 1.1651

**Question 2: What is the bid–offer on the JPY/CAD cross rate implied by the interbank market?**

A. 78.13/78.17
B. 79.85/79.85
C. 79.84/79.86

**Solution:** C is correct. Using the intuitive equation-based approach,

(JPY/CAD) = (JPY/USD) × (USD/CAD) = (JPY/USD) × (USD/CAD)^(−1)

This equation shows that we have to invert the CAD/USD quotes to get the USD/CAD bid–offer rates of 0.75752/0.75763. That is, given the CAD/USD quotes of 1.3199/1.3201, we take the inverse of each and interchange bid and offer, so that the USD/CAD quotes are (1/1.3201)/(1/1.3199), or 0.75752/0.75763. Multiplying the JPY/USD and USD/CAD bid–offer rates then leads to the following:

Bid: 79.84 = 105.39 × 0.75752
Offer: 79.86 = 105.41 × 0.75763

**Question 3: If a dealer quoted a bid–offer rate of 79.81/79.83 in JPY/CAD, then a triangular arbitrage would involve buying:**

A. CAD in the interbank market and selling it to the dealer, for a profit of JPY 0.01 per CAD.
B. JPY from the dealer and selling it in the interbank market, for a profit of CAD 0.01 per JPY.
C. CAD from the dealer and selling it in the interbank market, for a profit of JPY 0.01 per CAD.

**Solution:** C is correct. The implied interbank cross rate for JPY/CAD is 79.84/79.86 (the answer to Question 2). Hence, the dealer is offering to sell the CAD (the base currency in the quote) too cheaply, at an offer rate that is below the interbank bid rate (79.83 versus 79.84, respectively). Triangular arbitrage would involve buying CAD from the dealer (paying the dealer's offer) and selling CAD in the interbank market (hitting the interbank bid), for a profit of JPY 0.01 (79.84 − 79.83) per CAD transacted.

**Question 4: If a dealer quoted a bid–offer of 79.82/79.87 in JPY/CAD, then you could:**

A. not make any arbitrage profits.
B. make arbitrage profits buying JPY from the dealer and selling it in the interbank market.
C. make arbitrage profits buying CAD from the dealer and selling it in the interbank market.

**Solution:** A is correct. The arbitrage relationship is not violated: The dealer's bid (offer) is not above (below) the interbank market's offer (bid). The implied interbank cross rate for JPY/CAD is 79.84/79.86 (the solution to Question 2).

**Question 5: A market participant is considering the following transactions:**

- Transaction 1: Buy CAD 100 million against the USD at 15:30 London time.
- Transaction 2: Sell CAD 100 million against the KRW at 21:30 London time.
- Transaction 3: Sell CAD 10 million against the USD at 15:30 London time.

Given the proposed transactions, what is the most likely ranking of the bid–offer spreads, from tightest to widest, under normal market conditions?

A. Transactions 1, 2, 3
B. Transactions 2, 1, 3
C. Transactions 3, 1, 2

**Solution:** C is correct. The CAD/USD currency pair is most liquid when New York and London are both in their most liquid trading periods at the same time (approximately 8:00 a.m. to 11:00 a.m. New York time, or about 13:00 to 16:00 London time). Transaction 3 is for a smaller amount than Transaction 1. Transaction 2 is for a less liquid currency pair (KRW/CAD is traded less than CAD/USD) and occurs outside of normal dealing hours in all three major centers (London, North America, and Asia); the transaction is also for a large amount.

## Forward Markets

### Spot and Forward Rates

Outright forward contracts (often referred to simply as forwards) are agreements to exchange one currency for another on a future date at an exchange rate agreed upon today. Any exchange rate transaction that has a settlement date longer than T + 2 is a forward contract.

Forward exchange rates must satisfy an arbitrage relationship that equates the investment return on two alternative but equivalent investments. To simplify the explanation of this arbitrage relationship and to focus on the intuition behind forward rate calculations, we will ignore the bid–offer spread on exchange rates and money market instruments. In addition, we will alter our exchange rate notation from price/base currency (P/B) to "foreign/domestic currency" (f/d), making the assumption that the domestic currency for an investor is the base currency in the exchange rate quotation.

Using this (f/d) notation will make it easier to illustrate the choice an investor faces between domestic and foreign investments, as well as the arbitrage relationships that equate the returns on these investments when their risk characteristics are equivalent.

### Covered Interest Rate Parity

Consider an investor with one unit of domestic currency to invest for one year. The investor faces two alternatives:

A. One alternative is to invest cash for one year at the domestic risk-free rate (i_d). At the end of the year, the investment would be worth (1 + i_d).

B. The other alternative is to convert the domestic currency to foreign currency at the spot rate of S_f/d and invest for one year at the foreign risk-free rate (i_f). At the end of the period, the investor would have S_f/d × (1 + i_f) units of foreign currency. These funds then must be converted back to the investor's domestic currency. If the exchange rate to be used for this end-of-year conversion is set at the start of the period using a one-year forward contract, then the investor will have eliminated the foreign exchange risk associated with converting at an unknown future spot rate. If we let F_f/d denote the forward rate, the investor would obtain (1/F_f/d) units of the domestic currency for each unit of foreign currency sold forward. Hence, in domestic currency, at the end of the year, the investment would be worth S_f/d × (1 + i_f) × (1/F_f/d).

The two investment alternatives above (A and B) are risk free and therefore must offer the same return. If they did not offer the same return, investors could earn a riskless arbitrage profit by borrowing in one currency, lending in the other, and using the spot and forward exchange markets to eliminate currency risk. Equating the returns on these two investment alternatives—that is, putting investments A and B on opposite sides of the equal sign—leads to the following relationship:

(1 + i_d) = S_f/d × (1 + i_f) × (1/F_f/d)