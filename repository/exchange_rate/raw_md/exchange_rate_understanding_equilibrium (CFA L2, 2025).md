© CFA Institute. For candidate use only. Not for distribution.
L E A R N I N G M O D U L E
1
Currency Exchange Rates:
Understanding Equilibrium Value
by Michael R. Rosenberg, and William A. Barker, PhD, CFA.
Michael R. Rosenberg (USA). William A. Barker, PhD, CFA (Canada).
LEARNING OUTCOMES
Mastery The candidate should be able to:
calculate and interpret the bid–offer spread on a spot or forward
currency quotation and describe the factors that affect the bid–offer
spread
identify a triangular arbitrage opportunity and calculate its profit,
given the bid–offer quotations for three currencies
explain spot and forward rates and calculate the forward premium/
discount for a given currency
calculate the mark-to-market value of a forward contract
explain international parity conditions (covered and uncovered
interest rate parity, forward rate parity, purchasing power parity, and
the international Fisher effect)
describe relations among the international parity conditions
evaluate the use of the current spot rate, the forward rate,
purchasing power parity, and uncovered interest parity to forecast
future spot exchange rates
explain approaches to assessing the long-run fair value of an
exchange rate
describe the carry trade and its relation to uncovered interest rate
parity and calculate the profit from a carry trade
explain how flows in the balance of payment accounts affect
currency exchange rates
explain the potential effects of monetary and fiscal policy on
exchange rates
describe objectives of central bank or government intervention and
capital controls and describe the effectiveness of intervention and
capital controls
describe warning signs of a currency crisis

© CFA Institute. For candidate use only. Not for distribution.
4 Learning Module 1 Currency Exchange Rates: Understanding Equilibrium Value
1 INTRODUCTION
Exchange rates are well known to follow a random walk, whereby fluctuations from
one day to the next are unpredictable. The business of currency forecasting can be
a humbling experience. Alan Greenspan, former chair of the US Federal Reserve
Board, famously noted that “having endeavored to forecast exchange rates for more
than half a century, I have understandably developed significant humility about my
ability in this area.”
Hence, our discussion is not about predicting exchange rates but about the tools
the reader can use to better understand long-run equilibrium value. This outlook
helps guide the market participant’s decisions with respect to risk exposures, as well
as whether currency hedges should be implemented and, if so, how they should be
managed. After discussing the basics of exchange rate transactions, we present the
main theories for currency determination—starting with the international parity
conditions—and then describe other important influences, such as current account
balances, capital flows, and monetary and fiscal policy.
Although these fundamentals-based models usually perform poorly in predicting
future exchange rates in the short run, they are crucial for understanding long-term
currency value. Thus, we proceed as follows:
■ We review the basic concepts of the foreign exchange market covered in
the CFA Program Level I curriculum and expand this previous coverage to
incorporate more material on bid–offer spreads.
■ We then begin to examine determinants of exchange rates, starting with
longer-term interrelationships among exchange rates, interest rates, and
inflation rates embodied in the international parity conditions. These parity
conditions form the key building blocks for many long-run exchange rate
models.
■ We also examine the foreign exchange (FX) carry trade, a trading strategy
that exploits deviations from uncovered interest rate parity and discuss the
relationship between a country’s exchange rate and its balance of payments.
■ We then examine how monetary and fiscal policies can indirectly affect
exchange rates by influencing the various factors described in our exchange
rate model.
■ The subsequent section focuses on direct public sector actions in foreign
exchange markets, both through capital controls and by foreign exchange
market intervention (buying and selling currencies for policy purposes).
■ The last section examines historical episodes of currency crisis and some
leading indicators that may signal the increased likelihood of a crisis.
2 FOREIGN EXCHANGE MARKET CONCEPTS
calculate and interpret the bid–offer spread on a spot or forward
currency quotation and describe the factors that affect the bid–offer
spread

© CFA Institute. For candidate use only. Not for distribution.
Foreign Exchange Market Concepts 5
We begin with a brief review of some of the basic conventions of the FX market that
were covered in the CFA Program Level I curriculum. In this section, we cover (1) the
basics of exchange rate notation and pricing, (2) arbitrage pricing constraints on spot
rate foreign exchange quotes, and (3) forward rates and covered interest rate parity.
An exchange rate is the price of the base currency expressed in terms of the price
currency. For example, a USD/EUR rate of 1.1650 means the euro, the base currency,
costs 1.1650 US dollars (an appendix defines the three-letter currency codes). The
exact notation used to represent exchange rates can vary widely between sources,
and occasionally the same exchange rate notation will be used by different sources to
mean completely different things. The reader should be aware that the notation used
here may not be the same as that encountered elsewhere. To avoid confusion, we will
identify exchange rates using the convention of “P/B,” referring to the price of the
base currency, “B,” expressed in terms of the price currency, “P.”
NOTATION CONVENTIONS
Notation is generally not standardized in global foreign exchange markets, and
there are several common ways of expressing the same currency pair (e.g., JPY/
USD, USD:JPY, $/¥). What is common in FX markets, however, is the concept of
a “base” and a “price” currency when setting exchange rates. We will sometimes
switch to discussing a “domestic” and a “foreign” currency, quoted as foreign/
domestic (f/d). This is only an illustrative device for more easily explaining vari-
ous theoretical concepts. The candidate should be aware that currency pairs are
not described in terms of “foreign” and “domestic” currencies in professional
FX markets. This is because what is the “foreign” and what is the “domestic”
currency depend on where one is located, which can lead to confusion. For
instance, what is “foreign” and what is “domestic” for a Middle Eastern investor
trading CHF against GBP with the New York branch of a European bank, with
the trade ultimately booked at the bank’s headquarters in Paris?
The spot exchange rate is usually used for settlement on the second business day
after the trade date, referred to as T + 2 settlement (the exception being CAD/USD,
for which standard spot settlement is T + 1). In foreign exchange markets—as in other
financial markets—market participants are presented with a two-sided price in the
form of a bid price and an offer price (also called an ask price) quoted by potential
counterparties. The bid price is the price, defined in terms of the price currency, at
which the counterparty is willing to buy one unit of the base currency. Similarly, the
offer price is the price, in terms of the price currency, at which that counterparty is
willing to sell one unit of the base currency. For example, given a price request from
a client, a dealer might quote a two-sided price on the spot USD/EUR exchange rate
of 1.1648/1.1652. This means that the dealer is willing to pay USD 1.1648 to buy one
EUR and that the dealer is willing to sell one EUR for USD 1.1652.
There are two points to bear in mind about bid–offer quotes:
1. The offer price is always higher than the bid price. The bid–offer spread—the
difference between the offer price and the bid price—is the compensation
that counterparties seek for providing foreign exchange to other market
participants.
2. The party in the transaction who requests a two-sided price quote has the
option (but not the obligation) to deal at either the bid (to sell the base cur-
rency) or the offer (to buy the base currency) quoted by the dealer. If the party
chooses to trade at the quoted prices, the party is said to have either “hit the

© CFA Institute. For candidate use only. Not for distribution.
6 Learning Module 1 Currency Exchange Rates: Understanding Equilibrium Value
bid” or “paid the offer.” If the base currency is being sold, the party is said
to have hit the bid. If the base currency is being bought, the party is said to
have paid the offer.
We will distinguish here between the bid–offer pricing a client receives from a
dealer and the pricing a dealer receives from the interbank market. Dealers buy and
sell foreign exchange among themselves in what is called the interbank market. This
global network for exchanging currencies among professional market participants
allows dealers to adjust their inventories and risk positions, distribute foreign curren-
cies to end users who need them, and transfer foreign exchange rate risk to market
participants who are willing to bear it. The interbank market is typically for dealing
sizes of at least 1 million units of the base currency. Of course, the dealing amount can
be larger than 1 million units; indeed, interbank market trades generally are measured
in terms of multiples of a million units of the base currency. Please note that many
non-bank entities can now access the interbank market. They include institutional
asset managers and hedge funds.
The bid–offer spread a dealer provides to most clients typically is slightly wider
than the bid–offer spread observed in the interbank market. Most currencies, except
for the yen, are quoted to four decimal places. The fourth decimal place (0.0001) is
referred to as a “pip.” The yen is typically quoted to just two decimal places; in yen
quotes, the second decimal place (0.01) is referred to as a pip.
For example, if the quote in the interbank USD/EUR spot market is 1.1649/1.1651
(two pips wide), the dealer might quote a client a bid–offer of 1.1648/1.1652 (four pips
wide) for a spot USD/EUR transaction. When the dealer buys (sells) the base currency
from (to) a client, the dealer is typically expecting to quickly turn around and sell (buy)
the base currency in the interbank market. This offsetting transaction allows the dealer
to divest the risk exposure assumed by providing a two-sided price to the client and
to hopefully make a profit. Continuing our example, suppose the dealer’s client hits
the dealer’s bid and sells EUR to the dealer for USD 1.1648. The dealer is now long
EUR (and short USD) and wants to cover this position in the interbank market. To
do this, the dealer sells the EUR in the interbank market by hitting the interbank bid.
As a result, the dealer bought EUR from the client at USD 1.1648 and then sold the
EUR in the interbank for USD 1.1649. This gives the dealer a profit of USD 0.0001
(one pip) for every EUR transacted. This one pip translates into a profit of USD 100
per EUR million bought from the client. If, instead of hitting his bid, the client paid
the offer (1.1652), then the dealer could pay the offer in the interbank market (1.1651),
earning a profit of one pip.
The size of the bid–offer spread quoted to dealers’ clients in the FX market can
vary widely across exchange rates and is not constant over time, even for a single
exchange rate. The size of this spread depends primarily on three factors:
■ the bid–offer spread in the interbank foreign exchange market for the two
currencies involved,
■ the size of the transaction, and
■ the relationship between the dealer and the client.
We examine each factor in turn.
The size of the bid–offer spread quoted in the interbank market depends on the
liquidity in this market. Liquidity is influenced by several factors:
1. The currency pair involved. Market participation is greater for some cur-
rency pairs than for others. Liquidity in the major currency pairs—for
example, USD/EUR, JPY/USD, and USD/GBP—can be quite high. These
markets are almost always deep, with multiple bids and offers from market
participants around the world. In other currency pairs, particularly some of

© CFA Institute. For candidate use only. Not for distribution.
Foreign Exchange Market Concepts 7
the more obscure currency cross rates (e.g., MXN/CHF), market participa-
tion is much thinner and consequently the bid–offer spread in the interbank
market will be wider.
2. The time of day. The interbank FX markets are most liquid when the major
FX trading centers are open. Business hours in London and New York—the
two largest FX trading centers—overlap from approximately 8:00 a.m. to
11:00 a.m. New York time. The interbank FX market for most currency pairs
is typically most liquid during these hours. After London closes, liquid-
ity is thinner through the New York afternoon. The Asian session starts
when dealers in Tokyo, Singapore, and Hong Kong SAR open for business,
typically by 7:00 p.m. New York time. For most currency pairs, however,
the Asian session is not as liquid as the London and New York sessions.
Although FX markets are open 24 hours a day on business days, between
the time New York closes and the time Asia opens, liquidity in interbank
markets can be very thin because Sydney, Australia, tends to be the only
active trading center during these hours. For reference, the chart below
shows a 24-hour period from midnight (00:00) to midnight (24:00) London
time, corresponding standard times in Tokyo and New York, and, shaded
in grey, the approximate hours of the most liquid trading periods in each
market.
Standard Time and Approximate FX Trading Hours in Major Markets: Midnight to
Midnight (London Time)
Tokyo 09:00 13:00 17:00 21:00 01:00 05:00 09:00
Day+1 Day+1 Day+1
London 00:00 04:00 08:00 12:00 16:00 20:00 24:00
New York 19:00 23:00 03:00 07:00 11:00 15:00 19:00
Day−1 Day−1
3. Market volatility. As in any financial market, when major market partici-
pants have greater uncertainty about the factors influencing market pricing,
they will attempt to reduce their risk exposures and/or charge a higher price
for taking on risk. In the FX market, this response implies wider bid–offer
spreads in both the interbank and broader markets. Geopolitical events (e.g.,
war, civil strife), market crashes, and major data releases (e.g., US non-farm
payrolls) are among the factors that influence spreads and liquidity.
The size of the transaction can also affect the bid–offer spread shown by a dealer
to clients. Typically, the larger the transaction, the further away from the current
spot exchange rate the dealing price will be. Hence, a client who asks a dealer for a
two-sided spot CAD/USD price on, for example, USD 50 million will be shown a wider
bid–offer spread than a client who asks for a price on USD 1 million. The wider spread
reflects the greater difficulty the dealer faces in offsetting the foreign exchange risk
of the position in the interbank FX market. Smaller dealing sizes can also affect the
bid–offer quote shown to clients. “Retail” quotes are typically for dealing sizes smaller
than 1 million units of the base currency and can range all the way down to foreign
exchange transactions conducted by individuals. The bid–offer spreads for these retail
transactions can be very large compared with those in the interbank market.
The relationship between the dealer and the client can also affect the size of the
bid–offer spread shown by the dealer. For many clients, the spot foreign exchange
business is only one business service among many that a dealer provides to that client.
For example, the dealer firm might also transact in bond and/or equity securities with
the same client. In a competitive business environment, in order to win the client’s
business for these other services, the dealer might provide a tighter (i.e., smaller)

© CFA Institute. For candidate use only. Not for distribution.
8 Learning Module 1 Currency Exchange Rates: Understanding Equilibrium Value
bid–offer spot exchange rate quote. The dealer might also give tighter bid–offer quotes
in order to win repeat FX business. A client’s credit risk can also be a factor. A client
with a poor credit profile may be quoted a wider bid–offer spread than one with
good credit. Given the short settlement cycle for spot FX transactions (typically two
business days), however, credit risk is not the most important factor in determining
the client’s bid–offer spread on spot exchange rates.
3 ARBITRAGE CONSTRAINTS ON SPOT EXCHANGE RATE
QUOTES
identify a triangular arbitrage opportunity and calculate its profit,
given the bid–offer quotations for three currencies
The bid–offer quotes a dealer shows in the interbank FX market must respect two
arbitrage constraints; otherwise the dealer creates riskless arbitrage opportunities for
other interbank market participants. We will confine our attention to the interbank FX
market because arbitrage presumes the ability to deal simultaneously with different
market participants and in different markets, the ability to access “wholesale” bid–offer
quotes, and the market sophistication to spot arbitrage opportunities.
First, the bid shown by a dealer in the interbank market cannot be higher than
the current interbank offer, and the offer shown by a dealer cannot be lower than the
current interbank bid. If the bid–offer quotes shown by a dealer are inconsistent with
the then-current interbank market quotes, other market participants will buy from the
cheaper source and sell to the more expensive source. This arbitrage will eventually
bring the two prices back into line. For example, suppose that the current spot USD/
EUR price in the interbank market is 1.1649/1.1651. If a dealer showed a misaligned
price quote of 1.1652/1.1654, then other market participants would pay the offer in
the interbank market, buying EUR at a price of USD 1.1651, and then sell the EUR to
the dealer by hitting the dealer’s bid at USD 1.1652—thereby making a riskless profit
of one pip on the trade. This arbitrage would continue as long as the dealer’s bid–offer
quote violated the arbitrage constraint.
Second, the cross-rate bids (offers) posted by a dealer must be lower (higher) than
the implied cross-rate offers (bids) available in the interbank market. A currency dealer
located in a given country typically provides exchange rate quotations between that
country’s currency and various foreign currencies. If a particular currency pair is
not explicitly quoted, it can be inferred from the quotes for each currency in terms
of the exchange rate with a third nation’s currency. For example, given exchange rate
quotes for the currency pairs A/B and C/B, we can back out the implied cross rate
of A/C. This implied A/C cross rate must be consistent with the A/B and C/B rates.
This again reflects the basic principle of arbitrage: If identical financial products are
priced differently, then market participants will buy the cheaper one and sell the more
expensive one until the price difference is eliminated. In the context of FX cross rates,
there are two ways to trade currency A against currency C: (1) using the cross rate
A/C or (2) using the A/B and C/B rates. Because, in the end, both methods involve
selling (buying) currency C in order to buy (sell) currency A, the exchange rates for
these two approaches must be consistent. If the exchange rates are not consistent,
the arbitrageur will buy currency C from a dealer if it is undervalued (relative to the
cross rate) and sell currency A. If currency C is overvalued by a dealer (relative to the
cross rate), it will be sold and currency A will be bought.

© CFA Institute. For candidate use only. Not for distribution.
Arbitrage Constraints on Spot Exchange Rate Quotes 9
To illustrate this triangular arbitrage among three currencies, suppose that the
interbank market bid–offer in USD/EUR is 1.1649/1.1651 and that the bid–offer in
JPY/USD is 105.39/105.41. We need to use these two interbank bid–offer quotes to
calculate the market-implied bid–offer quote on the JPY/EUR cross rate.
Begin by considering the transactions required to sell JPY and buy EUR, going
through the JPY/USD and USD/EUR currency pairs. We can view this process intu-
itively as follows:
Sell JPY Sell JPY Sell USD
= then
Buy EUR Buy USD Buy EUR
Note that “Buy USD” and “Sell USD” in the expressions on the right-hand side of the
equal sign will cancel out to give the JPY/EUR cross rate. In equation form, we can
represent this relationship as follows:
_JPY _JPY _ USD
= .
(EUR) ( USD )(EUR)
Now, let’s incorporate the bid–offer rates in order to do the JPY/EUR calculation. A
rule of thumb is that when we speak of a bid or offer exchange rate, we are referring
to the bid or offer for the currency in the denominator (the base currency).
i. The left-hand side of the above equal sign is “Sell JPY, Buy EUR.” In the
JPY/EUR price quote, the EUR is in the denominator (it is the base cur-
rency). Because we want to buy the currency in the denominator, we need
an exchange rate that is an offer rate. Thus, we will be calculating the offer
rate for JPY/EUR.
ii. The first term on the right-hand side of the equal sign is “Sell JPY, Buy
USD.” Because we want to buy the currency in the denominator of the
quote, we need an exchange rate that is an offer rate. Thus, we need the
offer rate for JPY/USD.
iii. The second term on the right-hand side of the equal sign is “Sell USD, Buy
EUR.” Because we want to buy the currency in the denominator of the
quote, we need an exchange rate that is an offer rate. Thus, we need the
offer rate for USD/EUR.
Combining all of this conceptually and putting in the relevant offer rates leads to
a JPY/EUR offer rate of
_JPY _JPY _ USD
= = 105.41 × 1.1651 = 122.81.
(EUR) offer ( USD ) offer (EUR) offer
Perhaps not surprisingly, calculating the implied JPY/EUR bid rate uses the same
process as above but with “Buy JPY, Sell EUR” for the left-hand side of the equation,
which leads to
_JPY _JPY _ USD
= = 105.39 × 1.1649 = 122.77.
(EUR) ( USD ) (EUR)
bid bid bid
As one would expect, the implied cross-rate bid (122.77) is less than the offer (122.81).
This simple formula seems relatively straightforward: To get the implied bid cross
rate, simply multiply the bid rates for the other two currencies. However, depending
on the quotes provided, it may be necessary to invert one of the quotes in order to
complete the calculation.
This is best illustrated with an example. Consider the case of calculating the implied
GBP/EUR cross rate if you are given USD/GBP and USD/EUR quotes. Simply using
the provided quotes will not generate the desired GBP/EUR cross rate:
_GBP _USD _USD
≠ .
EUR (GBP)(EUR)

© CFA Institute. For candidate use only. Not for distribution.
10 Learning Module 1 Currency Exchange Rates: Understanding Equilibrium Value
Instead, because the USD is in the numerator in both currency pairs, we will have to
invert one of the pairs to derive the GBP/EUR cross rate.
The following equation represents the cross-rate relationship we are trying to derive:
_GBP _GBP _USD
= .
EUR (USD)(EUR)
But we don’t have the GBP/USD quote. We can, however, invert the USD/GBP quote
and use that in our calculation. Let’s assume the bid–offer quote provided is for USD/
GBP and is 1.2302/1.2304. With this quote, if we want to buy GBP (the currency in
the denominator), we will buy GBP at the offer and the relevant quote is 1.2304. We
can invert this quote to arrive at the needed GBP/USD quote: 1 ÷ 1.2304 = 0.81274.
Note that, in this example, when we buy the GBP, we are also selling the USD. When
we invert the provided USD/GBP offer quote, we obtain 0.81274 GBP/USD. This is
the price at which we sell the USD—that is, the GBP/USD bid. It may help here to
remember our rule of thumb from above: When we speak of a bid or offer exchange
rate, we are referring to the bid or offer for the currency in the denominator (the
base currency).
Similarly, to get a GBP/USD offer, we use the inverse of the USD/GBP bid of 1.2302:
1 ÷ 1.2302 = 0.81288. (Note that we extended the calculated GBP/USD 0.81274/0.81288
quotes to five decimal places to avoid truncation errors in subsequent calculations.)
We can now finish the calculation of the bid and offer cross rates for GBP/EUR.
Using the previously provided 1.1649/1.1651 as the bid–offer in USD/EUR, we cal-
culate the GBP/EUR bid rate as follows:
_GBP _GBP _ USD
= = 0.81274 × 1.1649 = 0.9468.
(EUR) ( USD ) (EUR)
bid bid bid
Similarly, the implied GBP/EUR offer rate is
_GBP _GBP _ USD
= = 0.81288 × 1.1651 = 0.9471.
(EUR) offer ( USD ) offer (EUR) offer
Note that the implied bid rate is less than the implied offer rate, as it must be to
prevent arbitrage.
We conclude this section on arbitrage constraints with some simple observations:
■ The arbitrage constraint on implied cross rates is similar to that for spot
rates (posted bid rates cannot be higher than the market’s offer; posted offer
rates cannot be lower than the market’s bid). The only difference is that
this second arbitrage constraint is applied across currency pairs instead of
involving a single currency pair.
■ In reality, any violations of these arbitrage constraints will quickly disap-
pear. Both human traders and automatic trading algorithms are constantly
on alert for any pricing inefficiencies and will arbitrage them away almost
instantly. If Dealer 1 is buying a currency at a price higher than the price
at which Dealer 2 is selling it, the arbitrageur will buy the currency from
Dealer 2 and resell it to Dealer 1. As a result of buying and selling pressures,
Dealer 2 will raise his offer prices and Dealer 1 will reduce her bid prices to
the point where arbitrage profits are no longer available.
■ Market participants do not need to calculate cross rates manually because
electronic dealing machines (which are essentially just specialized comput-
ers) will automatically calculate cross bid–offer rates given any two underly-
ing bid–offer rates.

© CFA Institute. For candidate use only. Not for distribution.
Arbitrage Constraints on Spot Exchange Rate Quotes 11
EXAMPLE 1
Bid–Offer Rates
The following are spot rate quotes in the interbank market:
USD/EUR 1.1649/1.1651
JPY/USD 105.39/105.41
CAD/USD 1.3199/1.3201
SEK/USD 9.6300/9.6302
1. What is the bid–offer on the SEK/EUR cross rate implied by the interbank
market?
A. 0.1209/0.1211
B. 8.2656/8.2668
C. 11.2180/11.2201
Solution
C is correct. Using the provided quotes and setting up the equations so that
the cancellation of terms results in the SEK/EUR quote,
_SEK _SEK _USD
= × .
EUR USD EUR
Hence, to calculate the SEK/EUR bid (offer) rate, we multiply the SEK/USD
and USD/EUR bid (offer) rates to get the following:
Bid: 11.2180 = 9.6300 × 1.1649.
Offer: 11.2201 = 9.6302 × 1.1651.
2. What is the bid–offer on the JPY/CAD cross rate implied by the interbank
market?
A. 78.13/78.17
B. 79.85/79.85
C. 79.84/79.86
Solution
C is correct. Using the intuitive equation-based approach,
−1
_JPY _JPY _CAD _JPY _ USD
= × = × .
CAD USD (USD) USD CAD
This equation shows that we have to invert the CAD/USD quotes to get
the USD/CAD bid–offer rates of 0.75752/0.75763. That is, given the CAD/
USD quotes of 1.3199/1.3201, we take the inverse of each and interchange
bid and offer, so that the USD/CAD quotes are (1/1.3201)/(1/1.3199), or
0.75752/0.75763. Multiplying the JPY/USD and USD/CAD bid–offer rates
then leads to the following:
Bid: 79.84 = 105.39 × 0.75752.
Offer: 79.86 = 105.41 × 0.75763.

© CFA Institute. For candidate use only. Not for distribution.
12 Learning Module 1 Currency Exchange Rates: Understanding Equilibrium Value
3. If a dealer quoted a bid–offer rate of 79.81/79.83 in JPY/CAD, then a trian-
gular arbitrage would involve buying:
A. CAD in the interbank market and selling it to the dealer, for a profit of
JPY 0.01 per CAD.
B. JPY from the dealer and selling it in the interbank market, for a profit
of CAD 0.01 per JPY.
C. CAD from the dealer and selling it in the interbank market, for a profit
of JPY 0.01 per CAD.
Solution
C is correct. The implied interbank cross rate for JPY/CAD is 79.84/79.86
(the answer to Question 2). Hence, the dealer is offering to sell the CAD
(the base currency in the quote) too cheaply, at an offer rate that is below
the interbank bid rate (79.83 versus 79.84, respectively). Triangular arbitrage
would involve buying CAD from the dealer (paying the dealer’s offer) and
selling CAD in the interbank market (hitting the interbank bid), for a profit
of JPY 0.01 (79.84 − 79.83) per CAD transacted.
4. If a dealer quoted a bid–offer of 79.82/79.87 in JPY/CAD, then you could:
A. not make any arbitrage profits.
B. make arbitrage profits buying JPY from the dealer and selling it in the
interbank market.
C. make arbitrage profits buying CAD from the dealer and selling it in
the interbank market.
Solution
A is correct. The arbitrage relationship is not violated: The dealer’s bid
(offer) is not above (below) the interbank market’s offer (bid). The implied
interbank cross rate for JPY/CAD is 79.84/79.86 (the solution to Question
2).
5. A market participant is considering the following transactions:
Transaction 1 Buy CAD 100 million against the USD at 15:30 London time.
Transaction 2 Sell CAD 100 million against the KRW at 21:30 London time.
Transaction 3 Sell CAD 10 million against the USD at 15:30 London time.
Given the proposed transactions, what is the most likely ranking of the bid–
offer spreads, from tightest to widest, under normal market conditions?
A. Transactions 1, 2, 3
B. Transactions 2, 1, 3
C. Transactions 3, 1, 2
Solution
C is correct. The CAD/USD currency pair is most liquid when New York
and London are both in their most liquid trading periods at the same time
(approximately 8:00 a.m. to 11:00 a.m. New York time, or about 13:00 to
16:00 London time). Transaction 3 is for a smaller amount than Transaction
1. Transaction 2 is for a less liquid currency pair (KRW/CAD is traded less
than CAD/USD) and occurs outside of normal dealing hours in all three
major centers (London, North America, and Asia); the transaction is also for
a large amount.

© CFA Institute. For candidate use only. Not for distribution.
Forward Markets 13
FORWARD MARKETS 4
explain spot and forward rates and calculate the forward premium/
discount for a given currency
Outright forward contracts (often referred to simply as forwards) are agreements to
exchange one currency for another on a future date at an exchange rate agreed upon
today. Any exchange rate transaction that has a settlement date longer than T + 2 is
a forward contract.
Forward exchange rates must satisfy an arbitrage relationship that equates the
investment return on two alternative but equivalent investments. To simplify the expla-
nation of this arbitrage relationship and to focus on the intuition behind forward rate
calculations, we will ignore the bid–offer spread on exchange rates and money market
instruments. In addition, we will alter our exchange rate notation from price/base
currency (P/B) to “foreign/domestic currency” (f/d), making the assumption that the
domestic currency for an investor is the base currency in the exchange rate quotation.
Using this (f/d) notation will make it easier to illustrate the choice an investor faces
between domestic and foreign investments, as well as the arbitrage relationships that
equate the returns on these investments when their risk characteristics are equivalent.
Consider an investor with one unit of domestic currency to invest for one year.
The investor faces two alternatives:
A. One alternative is to invest cash for one year at the domestic risk-free rate
(i ). At the end of the year, the investment would be worth (1 + i ).
d d
B. The other alternative is to convert the domestic currency to foreign cur-
rency at the spot rate of S and invest for one year at the foreign risk-free
f/d
rate (i). At the end of the period, the investor would have S (1 + i) units of
f f/d f
foreign currency. These funds then must be converted back to the investor’s
domestic currency. If the exchange rate to be used for this end-of-year con-
version is set at the start of the period using a one-year forward contract,
then the investor will have eliminated the foreign exchange risk associated
with converting at an unknown future spot rate. If we let F denote the for-
f/d
ward rate, the investor would obtain (1/F ) units of the domestic currency
f/d
for each unit of foreign currency sold forward. Hence, in domestic currency,
at the end of the year, the investment would be worth S (1 + i)(1/F ).
f/d f f/d
The two investment alternatives above (A and B) are risk free and therefore must
offer the same return. If they did not offer the same return, investors could earn a
riskless arbitrage profit by borrowing in one currency, lending in the other, and using
the spot and forward exchange markets to eliminate currency risk. Equating the
returns on these two investment alternatives—that is, putting investments A and B
on opposite sides of the equal sign—leads to the following relationship:
_1
(1 + i ) = S 1 + i .
d f/d( f)( F f /d )
To see the intuition behind forward rate calculations, note that the right-hand
side of the expression (for investment B) also shows the chronological order of this
investment: Convert from domestic to foreign currency at the spot rate (S ); invest
f/d
this foreign currency amount at the foreign risk-free interest rate (1 + i); and then at
f
maturity, convert the foreign currency investment proceeds back into the domestic
currency using the forward rate (1/F ).
f/d

© CFA Institute. For candidate use only. Not for distribution.
14 Learning Module 1 Currency Exchange Rates: Understanding Equilibrium Value
For simplicity, we assumed a one-year horizon in the preceding example. However,
the argument holds for any investment horizon. The risk-free assets used in this arbi-
trage relationship are typically bank deposits quoted using the appropriate Market
Reference Rate for each currency involved. The day count convention MRR deposits
may be Actual/360 or Actual/365. The notation Actual/360 means that interest is cal-
culated as if there were 360 days in a year. The notation Actual/365 means interest is
calculated as if there were 365 days in a year. The main exception to the Actual/360 day
count convention is the GBP, for which the convention is Actual/365. For the purposes
of our discussion, we will use Actual/360 consistently in order to avoid complication.
Incorporating this day count convention into our arbitrage formula leads to
_Actual _Actual _1
1 + i = S 1 + i .
( d[ 360 ]) f/d( f[ 360 ])( F f /d )
This equation can be rearranged to isolate the forward rate:
_Actual
1 + i
_f[ 360 ]
F = S . (1)
f/d f/d _Actual
(1 + i )
d[ 360 ]
Equation 1 describes covered interest rate parity. Our previous work shows that
covered interest rate parity is based on an arbitrage relationship among risk-free inter-
est rates and spot and forward exchange rates. Because of this arbitrage relationship
between investment alternatives, Equation 1 can also be described as saying that the
covered (i.e., currency-hedged) interest rate differential between the two markets is
zero.
The covered interest rate parity equation can also be rearranged to give an expres-
sion for the forward premium or discount:
_Actual
_[ 360 ]
F − S = S i − i .
f/d f/d f/d _Actual (f d)
(1 + i )
d[ 360 ]
The domestic currency will trade at a forward premium (F > S ) if, and only if,
f/d f/d
the foreign risk-free interest rate exceeds the domestic risk-free interest rate (i > i ).
f d
Equivalently, in this case, the foreign currency will trade at a lower rate in the forward
contract (relative to the spot rate), and we would say that the foreign currency trades
at a forward discount. In other words, if it is possible to earn more interest in the
foreign market than in the domestic market, then the forward discount for the foreign
currency will offset the higher foreign interest rate. Otherwise, covered interest rate
parity would not hold and arbitrage opportunities would exist.
When the foreign currency is at a higher rate in the forward contract, relative to
the spot rate, we say that the foreign currency trades at a forward premium. In the
case of a forward premium for the foreign currency, the foreign risk-free interest rate
will be less than the domestic risk-free interest rate. Additionally, as can be seen in
the equation above, the premium or discount is proportional to the spot exchange
rate (S ), proportional to the interest rate differential (i − i ) between the markets,
f/d f d
and approximately proportional to the time to maturity (Actual/360).
Although we have illustrated the covered interest rate parity equation (Equation
1) in terms of foreign and domestic currencies (using the notation f/d), this equation
can also be expressed in our more standard exchange rate quoting convention of price
and base currencies (P/B):
_Actual
1 + i
_P[ 360 ]
F = S .
P/B P/B _Actual
(1 + i )
B[ 360 ]

© CFA Institute. For candidate use only. Not for distribution.
Forward Markets 15
When dealing in professional FX markets, it may be more useful to think of the
covered interest rate parity equation and the calculation of forward rates in this P/B
notation rather than in foreign/domestic (f/d) notation. Domestic and foreign are
relative concepts that depend on where one is located, and because of the potential for
confusion, these terms are not used for currency quotes in professional FX markets.
EXAMPLE 2
Calculating the Forward Premium (Discount)
The following table shows the mid-market rate (i.e., the average of the bid and
offer) for the current CAD/AUD spot exchange rate as well as for AUD and
CAD 270-day MRR (annualized):
Spot (CAD/AUD) 0.9000
270-day MRR (AUD) 1.47%
270-day MRR (CAD) 0.41%
1. The forward premium (discount) for a 270-day forward contract for CAD/
AUD would be closest to:
A. −0.0094.
B. −0.0071.
C. +0.0071.
Solution
B is correct. The equation to calculate the forward premium (discount) is as
follows:
_Actual
_[ 360 ]
F − S = S ( i − i ) .
P/B P/B P/B _Actual P B
(1 + i )
B[ 360 ]
Because AUD is the base currency in the CAD/AUD quote, putting in the
information from the table gives us
_270
_____[3_6_0_]____
F − S = 0.9000 (0.0041 − 0.0147) = − 0.0071.
P/B P/B _270
(1 + 0.0147 )
[360]
In professional FX markets, forward exchange rates are typically quoted in terms of
points—the difference between the forward exchange rate quote and the spot exchange
rate quote, scaled so that the points can be directly related to the last decimal place
in the spot quote. Thus, the forward rate quote is typically shown as the bid–offer on
the spot rate and the number of forward points at each maturity, as shown in Exhibit
1 (“Maturity” is defined in terms of the time between spot settlement—usually T +
2—and the settlement of the forward contract).

© CFA Institute. For candidate use only. Not for distribution.
16 Learning Module 1 Currency Exchange Rates: Understanding Equilibrium Value
Exhibit 1: Sample Spot and Forward Quotes (Bid–Offer)
Maturity Spot Rate
Spot (USD/EUR) 1.1649/1.1651
Forward Points
1 month −5.6/−5.1
3 months −15.9/−15.3
6 months −37.0/−36.3
12 months −94.3/−91.8
Note the following:
■ As always, the offer in the bid–offer quote is larger than the bid. In this
example, the forward points are negative (i.e., the forward rate for the EUR
is at a discount to the spot rate) but the bid is a smaller number (−5.6 versus
−5.1 at the one-month maturity).
■ The absolute number of forward points is a function of the term of the for-
ward contract: A longer contract term results in a larger number of points.
■ Because this is an OTC market, a client is not restricted to dealing only at
the dates/maturities shown. Dealers typically quote standard forward dates,
but forward deals can be arranged for any forward date the client requires.
The forward points for these non-standard (referred to as “broken”) forward
dates will typically be interpolated on the basis of the points shown for the
standard settlement dates.
■ The quoted points are already scaled to each maturity—they are not
annualized—so there is no need to adjust them.
To convert any of these quoted forward points into a forward rate, divide the num-
ber of points by 10,000 (to scale it down to the same four decimal places in the USD/
EUR spot quote) and then add the result to the spot exchange rate quote (because the
JPY/USD exchange rate is quoted to only two decimal places, forward points for the
dollar–yen currency pair are divided by 100). Be careful, however, about which side of
the market (bid or offer) is being quoted. For example, suppose a market participant
is selling the EUR forward against the USD and is given a USD/EUR quote. The EUR
is the base currency; thus, the market participant must use the bid rates (i.e., hit the
bid). Using the data in Exhibit 1, the three-month forward bid rate in this case would
be based on the spot bid and the forward points bid and hence would be
1.1649 + (−15.9/10,000) = 1.16331.
The market participant would be selling EUR three months forward at a price of
USD 1.16331 per EUR.
5 THE MARK-TO-MARKET VALUE OF A FORWARD
CONTRACT
calculate the mark-to-market value of a forward contract

© CFA Institute. For candidate use only. Not for distribution.
The Mark-to-Market Value of a Forward Contract 17
Next, we consider the mark-to-market value of forward contracts. As with other
financial instruments, the mark-to-market value of forward contracts reflects the
profit (or loss) that would be realized from closing out the position at current market
prices. To close out a forward position, we must offset it with an equal and opposite
forward position using the spot exchange rate and forward points available in the
market when the offsetting position is created. When a forward contract is initiated,
the mark-to-market value of the contract is zero, and no cash changes hands. From
that moment onward, however, the mark-to-market value of the forward contract
will change as the spot exchange rate changes and as interest rates change in either
of the two currencies.
Let’s look at an example. Suppose that a market participant bought GBP 10 million
for delivery against the AUD in six months at an “all-in” forward rate of 1.8100 AUD/
GBP. (The all-in forward rate is simply the sum of the spot rate and the scaled forward
points.) Three months later, the market participant wants to close out this forward
contract. This would require selling GBP 10 million three months forward using
the AUD/GBP spot exchange rate and forward points in effect at that time. Before
looking at this exchange rate, note that the offsetting forward contract is defined in
terms of the original position taken. The original position in this example was “long
GBP 10 million,” so the offsetting contract is “short GBP 10 million.” However, there is
ambiguity here: To be long GBP 10 million at 1.8100 AUD/GBP is equivalent to being
short AUD 18,100,000 (10,000,000 × 1.8100) at the same forward rate. To avoid this
ambiguity, for the purposes of this discussion, we will state what the relevant forward
position is for mark-to-market purposes. The net gain or loss from the transaction
will be reflected in the alternate currency.
Assume the bid–offer quotes for spot and forward points three months prior to
the settlement date are as follows:
Spot rate (AUD/GBP) 1.8210/1.8215
Three-month points 130/140
To sell GBP (the base currency in the AUD/GBP quote), we will be calculating the bid
side of the market. Hence, the appropriate all-in three-month forward rate to use is
1.8210 + 130/10,000 = 1.8340.
This means that the market participant originally bought GBP 10 million at an AUD/
GBP rate of 1.8100 and subsequently sold that amount at a rate of 1.8340. These GBP
amounts will net to zero at the settlement date (GBP 10 million both bought and sold),
but the AUD amounts will not, because the forward rate has changed. The AUD cash
flow at the settlement date will be
(1.8340 − 1.8100) × 10,000,000 = +AUD 240,000.
This is a cash inflow because the market participant was long the GBP with the original
forward position and the GBP subsequently appreciated (the AUD/GBP rate increased).
This cash flow will be paid at the settlement day, which is still three months away.
To calculate the mark-to-market value of the dealer’s position, we must discount this
cash flow to the present. The present value of this amount is found by discounting the
settlement day cash flow by the three-month discount rate. Because this amount is in
AUD, we use the three-month AUD discount rate. Suppose that three-month AUD
MRR is 2.40% (annualized). The present value of this future AUD cash flow is then
_A__U_D_ _2_4_0_,0_0_0_
= AUD 238,569.
_90
1 + 0.024
(360)
This result is the mark-to-market value of the original long GBP 10 million
six-month forward when it is closed out three months prior to settlement.

© CFA Institute. For candidate use only. Not for distribution.
18 Learning Module 1 Currency Exchange Rates: Understanding Equilibrium Value
To summarize, the process for marking to market a forward position is relatively
straightforward:
1. Create an offsetting forward position that is equal to the original forward
position. (In the example above, the market participant was long GBP 10
million forward, so the offsetting forward contract would be to sell GBP 10
million.)
2. Determine the appropriate all-in forward rate for this new, offsetting for-
ward position. If the base currency of the exchange rate quote is being sold
(bought), then use the bid (offer) side of the market.
3. Calculate the cash flow at the settlement day. This amount will be based on
the original contract size times the difference between the original forward
rate and that calculated in Step 2. If the currency the market participant was
originally long (short) subsequently appreciated (depreciated), then there
will be a cash inflow (outflow). (In the above example, the market participant
was long the GBP, which subsequently appreciated, leading to a cash inflow
at the settlement day.)
4. Calculate the present value of this cash flow at the future settlement date.
The currency of the cash flow and the discount rate must match. (In the
example above, the cash flow at the settlement date was in AUD, so an AUD
MRR was used to calculate the present value.)
The factors that affect the bid–offer spread for forward points are the same as
those we discussed for spot bid–offer rates: the interbank market liquidity of the
underlying currency pair, the size of the transaction, and the relationship between
the client and the dealer. For forward bid–offer spreads, we can also add a fourth
factor: the term of the forward contract. Generally, the longer the term of the forward
contract, the wider the bid–offer spread. This relationship holds because as the term
of the contract increases,
■ liquidity in the forward market tends to decline,
■ the exposure to counterparty credit risk increases, and
■ the interest rate risk of the contract increases (forward rates are based on
interest rate differentials, and a longer duration means greater price sensitiv-
ity to movements in interest rates).
EXAMPLE 3
Forward Rates and the Mark-to-Market Value of Forward
Positions
A dealer is contemplating trade opportunities in the CHF/GBP currency pair.
The following are the current spot rates and forward points being quoted for
the CHF/GBP currency pair:
Spot rate (CHF/GBP) 1.2939/1.2941
One month −8.3/−7.9
Two months −17.4/−16.8
Three months −25.4/−24.6
Four months −35.4/−34.2
Five months −45.9/−44.1
Six months −56.5/−54.0

© CFA Institute. For candidate use only. Not for distribution.
The Mark-to-Market Value of a Forward Contract 19
1. The current all-in bid rate for delivery of GBP against the CHF in three
months is closest to:
A. 1.29136.
B. 1.29150.
C. 1.29164.
Solution
A is correct. The current all-in three-month bid rate for GBP (the base cur-
rency) is equal to 1.2939 + (−25.4/10,000) = 1.29136.
2. The all-in rate that the dealer will be quoted today by another dealer to sell
the CHF six months forward against the GBP is closest to:
A. 1.28825.
B. 1.28835.
C. 1.28870.
Solution
C is correct. The dealer will sell CHF against the GBP, which is equivalent
to buying GBP (the base currency) against the CHF. Hence, the offer side of
the market will be used for forward points. The all-in forward price will be
1.2941 + (−54.0/10,000) = 1.28870.
3. Some time ago, Laurier Bay Capital, an investment fund based in Los An-
geles, hedged a long exposure to the New Zealand dollar by selling NZD 10
million forward against the USD; the all-in forward price was 0.7900 (USD/
NZD). Three months prior to the settlement date, Laurier Bay wants to
mark this forward position to market. The bid–offer for the USD/NZD spot
rate, the three-month forward points, and the three-month MRRs (annual-
ized) are as follows:
Spot rate (USD/NZD) 0.7825/0.7830
Three-month points −12.1/−10.0
Three-month MRR (NZD) 3.31%
Three-month MRR (USD) 0.31%
The mark-to-market value for Laurier Bay’s forward position is closest to:
A. −USD 87,100.
B. +USD 77,437.
C. +USD 79,938.
Solution
C is correct. Laurier Bay sold NZD 10 million forward to the settlement
date at an all-in forward rate of 0.7900 (USD/NZD). To mark this position
to market, the fund would need an offsetting forward transaction involving
buying NZD 10 million three months forward to the settlement date. The
NZD amounts on the settlement date net to zero. For the offsetting forward
contract, because the NZD is the base currency in the USD/NZD quote,
buying NZD forward means paying the offer for both the spot rate and the
forward points. This scenario leads to an all-in three-month forward rate
of 0.7830 − 0.0010 = 0.7820. On the settlement day, Laurier Bay will receive
USD 7,900,000 (NZD 10,000,000 × 0.7900 USD/NZD) from the original for-
ward contract and pay out USD 7,820,000 (NZD 10,000,000 × 0.7820 USD/

© CFA Institute. For candidate use only. Not for distribution.
20 Learning Module 1 Currency Exchange Rates: Understanding Equilibrium Value
NZD) based on the offsetting forward contract. The result is a net cash flow
on the settlement day of 10,000,000 × (0.7900 − 0.7820) = +USD 80,000.
This is a cash inflow because Laurier Bay sold the NZD forward and the
NZD depreciated against the USD. This USD cash inflow will occur in three
months. To calculate the mark-to-market value of the original forward po-
sition, we need to calculate the present value of this USD cash inflow using
the three-month USD discount rate (we use USD MRR for this purpose):
__U_S_D__ 8_0_, 0_0_0__
= + USD 79, 938.
_90
1 + 0.0031
(360)
4. Now, suppose that instead of having a long exposure to the NZD, Laurier
Bay Capital had a long forward exposure to the USD, which it hedged by
selling USD 10 million forward against the NZD at an all-in forward rate of
0.7900 (USD/NZD). Three months prior to settlement date, it wants to close
out this short USD forward position.
Using the above table, the mark-to-market value for Laurier Bay’s short USD
forward position is closest to:
A. −NZD 141,117.
B. −NZD 139,959.
C. −NZD 87,100.
Solution
B is correct. Laurier Bay initially sold USD 10 million forward, and it will
have to buy USD 10 million forward to the same settlement date (i.e., in
three months’ time) in order to close out the initial position. Buying USD
using the USD/NZD currency pair is the same as selling the NZD. Because
the NZD is the base currency in the USD/NZD quote, selling the NZD
means calculating the bid rate:
0.7825 + (−12.1/10,000) = 0.78129.
At settlement, the USD amounts will net to zero (USD 10 million both
bought and sold). The NZD amounts will not net to zero, however, because
the all-in forward rate changed between the time Laurier Bay initiated the
original position and the time it closed out this position. At initiation, Lau-
rier Bay contracted to sell USD 10 million and receive NZD 12,658,228 (i.e.,
10,000,000/0.7900) on the settlement date. To close out the original forward
contract, Laurier Bay entered into an offsetting forward contract to receive
USD 10 million and pay out NZD 12,799,345 (i.e., 10,000,000/0.78129) at
settlement. The difference between the NZD amounts that Laurier Bay will
receive and pay out on the settlement date equals
NZD 12,658,228 − NZD 12,799,345 = −NZD 141,117.
This is a cash outflow for Laurier Bay because the fund was short the USD
in the original forward position and the USD subsequently appreciated (i.e.,
the NZD subsequently depreciated, because the all-in forward rate in USD/
NZD dropped from 0.7900 to 0.78129). This NZD cash outflow occurs in
three months’ time, and we must calculate its present value using the three-
month NZD MRR:
_−_ N_Z__D_ 1_4_1_, 1_1_7_
= − NZD 139, 959.
_90
1 + 0.0331
(360)

© CFA Institute. For candidate use only. Not for distribution.
International Parity Conditions 21
INTERNATIONAL PARITY CONDITIONS 6
explain international parity conditions (covered and uncovered
interest rate parity, forward rate parity, purchasing power parity, and
the international Fisher effect)
Having reviewed the basic tools of the FX market, we now turn our focus to how they
are used in practice. At the heart of the trading decision in FX markets lies a view on
equilibrium market prices. An understanding of equilibrium pricing will assist the
investor in framing decisions regarding risk exposures and how they should be managed.
In this and the following sections, we lay out a framework for developing a view on
equilibrium exchange rates. We begin by examining international parity conditions,
which describe the inter-relationships that jointly determine long-run movements
in exchange rates, interest rates, and inflation. These parity conditions are the basic
building blocks for describing long-term equilibrium levels for exchange rates. In
subsequent sections, we expand beyond the parity conditions by discussing other
factors that influence a currency’s value.
Always keep in mind that exchange rate movements reflect complex interactions
among multiple forces. In trying to untangle this complex web of interactions, we
must clearly delineate the following concepts:
1. Long run versus short run: Many of the factors that determine exchange rate
movements exert subtle but persistent influences over long periods of time.
Although a poor guide for short-term prediction, longer-term equilibrium
values act as an anchor for exchange rate movements.
2. Expected versus unexpected changes: In reasonably efficient markets, prices
will adjust to reflect market participants’ expectations of future develop-
ments. When a key factor—say, inflation—is trending gradually in a partic-
ular direction, market pricing will eventually come to reflect expectations
that this trend will continue. In contrast, large, unexpected movements in
a variable (for example, a central bank intervening in the foreign exchange
market) can lead to immediate, discrete price adjustments. This concept is
closely related to risk. For example, a moderate but steady rate of inflation
will not have the same effect on market participants as an inflation rate that
is very unpredictable. The latter clearly describes a riskier financial environ-
ment. Market pricing will reflect risk premiums—that is, the compensation
that traders and investors demand for being exposed to unpredictable out-
comes. Whereas expectations of long-run equilibrium values tend to evolve
slowly, risk premiums—which are closely related to confidence and reputa-
tion—can change quickly in response to unexpected developments.
3. Relative movements: An exchange rate represents the relative price of one
currency in terms of another. Hence, for exchange rate determination, the
level or variability of key factors in any particular country is typically much
less important than the differences in these factors across countries. For
example, knowing that inflation is increasing in Country A may not give
much insight into the direction of the A/B exchange rate without also know-
ing what is happening with the inflation rate in Country B.
As a final word of caution—and this cannot be emphasized enough—there is no
simple formula, model, or approach that will allow market participants to precisely
forecast exchange rates. Models that work well in one period may fail in others. Models
that work for one set of exchange rates may fail to work for others.

© CFA Institute. For candidate use only. Not for distribution.
22 Learning Module 1 Currency Exchange Rates: Understanding Equilibrium Value
Nonetheless, market participants must have a market view to guide their decisions,
even if this view requires significant revision as new information becomes available.
The following sections provide a framework for understanding FX markets, a guide
for thinking through the complex forces driving exchange rates. As with all theory,
however, it does not eliminate the need for insightful analysis of actual economic and
market conditions.
International Parity Conditions
International parity conditions form the building blocks of most models of exchange
rate determination. The key international parity conditions are as follows:
1. covered interest rate parity,
2. uncovered interest rate parity,
3. forward rate parity,
4. purchasing power parity, and
5. the international Fisher effect.
Parity conditions show how expected inflation differentials, interest rate differen-
tials, forward exchange rates, current spot exchange rates, and expected future spot
exchange rates would be linked in an ideal world. These conditions typically make
simplifying assumptions, such as zero transaction costs, perfect information that is
available to all market participants, risk neutrality, and freely adjustable market prices.
Although empirical studies have found that the parity conditions rarely hold in
the short term, they do help form a broadly based, long-term view of exchange rates
and accompanying risk exposures. The exception to the rule that parity conditions
do not hold in the short term is covered interest rate parity, which is the only parity
condition that is enforced by arbitrage. We examine this parity condition first.
7 COVERED AND UNCOVERED INTEREST RATE PARITY
AND FORWARD RATE PARITY
explain international parity conditions (covered and uncovered
interest rate parity, forward rate parity, purchasing power parity, and
the international Fisher effect)
describe relations among the international parity conditions
evaluate the use of the current spot rate, the forward rate,
purchasing power parity, and uncovered interest parity to forecast
future spot exchange rates
We have already discussed covered interest rate parity in our examination of forward
exchange rates. Under this parity condition, an investment in a foreign money market
instrument that is completely hedged against exchange rate risk should yield exactly
the same return as an otherwise identical domestic money market investment. Given
the spot exchange rate and the domestic and foreign yields, the forward exchange
rate must equal the rate that gives these two alternative investment strategies—invest
either in a domestic money market instrument or in a fully currency-hedged foreign
money market instrument—exactly the same holding period return. If one strategy
gave a higher holding period return than the other, then an investor could short-sell

© CFA Institute. For candidate use only. Not for distribution.
Covered and Uncovered Interest Rate Parity and Forward Rate Parity 23
the lower-yielding approach and invest the proceeds in the higher-yielding approach,
earning riskless arbitrage profits in the process. In real-world financial markets,
such a disparity will be quickly arbitraged away so that no further arbitrage profits
are available. Covered interest rate parity is thus said to be a no-arbitrage condition.
For covered interest rate parity to hold exactly, it must be assumed that there are
zero transaction costs and that the underlying domestic and foreign money market
instruments being compared are identical in terms of liquidity, maturity, and default
risk. Where capital is permitted to flow freely, spot and forward exchange markets
are liquid, and financial market conditions are relatively stress free, covered interest
rate differentials are generally found to be close to zero and covered interest rate
parity holds.
Uncovered Interest Rate Parity
According to the uncovered interest rate parity condition, the expected return on
an uncovered (i.e., unhedged) foreign currency investment should equal the return
on a comparable domestic currency investment. Uncovered interest rate parity states
that the change in spot rate over the investment horizon should, on average, equal the
differential in interest rates between the two countries. That is, the expected apprecia-
tion/depreciation of the exchange rate will just offset the yield differential.
To explain the intuition behind this concept, let’s switch, as we did with the exam-
ples for covered interest rate parity, from the standard price/base currency notation
(P/B) to foreign/domestic currency notation (f/d) in order to emphasize the choice
between foreign and domestic investments. As before, we also will assume that for the
investor, the base currency is the domestic currency. (In covered interest rate parity,
we assumed the investor transacted at a forward rate that was locked in at strategy
initiation. In uncovered interest rate parity, the investor is assumed to transact at a
future spot rate that is unknown at the time the strategy is initiated and the investor’s
currency position in the future is not hedged—that is, uncovered.)
For our example, assume that this investor has a choice between a one-year domestic
money market instrument and an unhedged one-year foreign-currency-denominated
money market investment. Under the assumption of uncovered interest rate parity,
the investor will compare the known return on the domestic investment with the
expected all-in return on the unhedged foreign-currency-denominated investment
(which includes the foreign yield as well as any movements in the exchange rate, in
S terms). The choice between these two investments will depend on which market
f/d
offers the higher expected return on an unhedged basis.
For example, assume that the return on the one-year foreign money market instru-
ment is 10% while the return on the one-year domestic money market instrument is
4%. From the investor’s perspective, the 4% expected return on the one-year domestic
investment in domestic currency terms is known with complete certainty. This is not the
case for the uncovered investment in the foreign currency money market instrument.
In domestic currency terms, the investment return on an uncovered (or unhedged)
foreign-currency-denominated investment is equal to ( 1 + i f ) (1 − %Δ S f /d ) − 1.
Intuitively, the formula says that the investor’s return on a foreign investment is
a function of both the foreign interest rate and the change in the spot rate, whereby
a depreciation in the foreign currency reduces the investor’s return. The percentage
change in S enters with a minus sign because an increase in S means the foreign
f/d f/d
currency declines in value, thereby reducing the all-in return from the domestic cur-
rency perspective of our investor. This all-in return depends on future movements in
the S rate, which cannot be known until the end of the period. This return can be
f/d
approximated by ≅ i − % Δ S .
f f/d

© CFA Institute. For candidate use only. Not for distribution.
24 Learning Module 1 Currency Exchange Rates: Understanding Equilibrium Value
Note that this approximate formula holds because the product (i × %ΔS) is small
compared with the interest rate (i) and the percentage change in the exchange rate
(%ΔS). For simplicity of exposition, we will use the ≅ symbol when we introduce an
approximation but will subsequently treat the relationship as an equality (=) unless
the distinction is important for the issue being discussed.
Using the previous example, consider three cases:
1. The S rate is expected to remain unchanged.
f/d
2. The domestic currency is expected to appreciate by 10%.
3. The domestic currency is expected to appreciate by 6%.
In the first case, the investor would prefer the foreign-currency-denominated
money market investment because it offers a 10% (= 10% − 0%) expected return,
while the comparable domestic investment offers only 4%. In the second case, the
investor would prefer the domestic investment because the expected return on the
foreign-currency-denominated investment is 0% (= 10% − 10%). In the third case,
uncovered interest rate parity holds because both investments offer a 4% (for the
foreign investment, 10% − 6%) expected return. In this case, the risk-neutral investor
is assumed to be indifferent between the alternatives.
Note that in the third case, in which uncovered interest rate parity holds, while the
expected return over the one-year investment horizon is the same for both instruments,
that expected return is just a point on the distribution of possible total return outcomes.
The all-in return on the foreign money market instrument is uncertain because the
future S rate is uncertain. Hence, when we say that the investor would be indifferent
f/d
between owning domestic and foreign investments because they both offer the same
expected return (4%), we are assuming that the investor is risk neutral (risk-neutral
investors base their decisions solely on the expected return and are indifferent to the
investments’ risk). Thus, uncovered interest rate parity assumes that there are enough
risk-neutral investors to force equality of expected returns.
Using our example’s foreign/domestic (f/d) notation, uncovered interest rate parity
says the expected change in the spot exchange rate over the investment horizon should
be reflected in the interest rate differential:
%Δ S e = i − i , (2)
f/d f d
where ∆Se indicates the change in the spot rate expected for future periods.
Note that Equation 2 cannot hold simultaneously for S/ and S / (= 1/S/ ) because
f d d f f d
their percentage changes are not of exactly equal magnitude. This reflects our earlier
approximation. Using the exact return on the unhedged foreign instrument would
alleviate this issue but would produce a less intuitive equation.
In our example, if the yield spread between the foreign and domestic investments is
6% (i − i = 6%), then this spread implicitly reflects the expectation that the domestic
f d
currency will strengthen versus the foreign currency by 6%.
Uncovered interest rate parity assumes that the country with the higher interest
rate or money market yield will see its currency depreciate. The depreciation of the
currency offsets the initial higher yield so that the (expected) all-in return on the two
investment choices is the same. Hence, if the uncovered interest rate parity condition
held consistently in the real world, it would rule out the possibility of earning excess
returns from going long a high-yield currency and going short a low-yield currency:
The depreciation of the high-yield currency would exactly offset the yield advantage
that the high-yield currency offers. Taking this scenario to its logical conclusion, if
uncovered interest rate parity held at all times, investors would have no incentive to
shift capital from one currency to another because expected returns on otherwise
identical money market investments would be equal across markets and risk-neutral
investors would be indifferent among them.

© CFA Institute. For candidate use only. Not for distribution.
Covered and Uncovered Interest Rate Parity and Forward Rate Parity 25
Most studies have found that over short- and medium-term periods, the rate
of depreciation of the high-yield currency is less than what would be implied by
uncovered interest rate parity. In many cases, high-yield currencies have been found
to strengthen, not weaken. There is, however, evidence that uncovered interest rate
parity works better over very long-term horizons.
Such findings have significant implications for foreign exchange investment strat-
egies. If high-yield currencies do not depreciate in line with the path predicted by the
uncovered interest rate parity condition, then high-yield currencies should exhibit a
tendency to outperform low-yield currencies over time. If so, investors could adopt
strategies that overweight high-yield currencies at the expense of low-yield currencies
and generate attractive returns in the process. Such approaches are known as FX carry
trade strategies. We will discuss them in greater detail later.
Forward Rate Parity
Forward rate parity states that the forward exchange rate will be an unbiased predictor
of the future spot exchange rate. It does not state that the forward rate will be a perfect
forecast, just an unbiased one; the forward rate may overestimate or underestimate
the future spot rate from time to time, but on average, it will equal the future spot
rate. Forward rate parity builds upon two other parity conditions, covered interest
rate parity and uncovered interest rate parity.
The covered interest rate parity condition describes the relationship among the
spot exchange rate, the forward exchange rate, and interest rates. Let’s keep using
the foreign/domestic exchange rate notation (f/d) to simplify the explanation. The
arbitrage condition that underlies covered interest rate parity (illustrated earlier) can
be rearranged to give an expression for the forward premium or discount:
_Actual
_[ 360 ]
F − S = S i − i .
f/d f/d f/d _Actual (f d)
(1 + i )
d[ 360 ]
The domestic currency will trade at a forward premium (F > S ) if, and only if,
f/d f/d
the foreign risk-free interest rate exceeds the domestic risk-free interest rate (i > i ).
f d
For the sake of simplicity, we assume that the investment horizon is one year, so that
i − i
_f d
F − S = S .
f/d f/d f/d(1 + i )
d
Because the 1 + i denominator will be close to 1, we can approximate the above
d
equation as follows:
F f /d − S f /d ≅ S f /d ( i f − i d ) .
This covered interest rate parity equation can be rearranged to show the forward
discount or premium as a percentage of the spot rate:
F − S
_f/d f/d
S ≅ i f − i d .
f/d
We have also shown that if uncovered interest rate parity holds, then the expected
change in the spot rate is equal to the interest rate differential:
%Δ S e = i − i .
f/d f d
We can link the covered interest rate parity and uncovered interest rate parity
equations as follows:
F − S
_ f/d f/d = %Δ S e = i − i .
S f/d f d
f/d

© CFA Institute. For candidate use only. Not for distribution.
26 Learning Module 1 Currency Exchange Rates: Understanding Equilibrium Value
Thus, the forward premium (discount) on a currency, expressed in percentage
terms, equals the expected percentage appreciation (depreciation) of the domestic
currency (assuming that the uncovered interest rate parity condition holds).
In theory, then, the forward exchange rate will be an unbiased forecast of the future
spot exchange rate if both covered and uncovered interest rate parity hold:
F = S e .
f/d f/d
This condition is often referred to as forward rate parity.
We know covered interest rate parity must hold because it is enforced by arbitrage.
The question of whether forward rate parity holds is thus dependent upon whether
uncovered interest rate parity holds.
How might uncovered interest rate parity be enforced? It is not enforced by arbi-
trage because there is no combination of trades that will lock in a (riskless) profit.
It could, however, hold if speculators willing to take risk enter the market. If the
forward rate is above (below) speculators’ expectations of the future spot rate, then
risk-neutral speculators will buy the domestic currency in the spot (forward) market
and simultaneously sell it in the forward (spot) market. These transactions would
push the forward premium into alignment with the consensus expectation of the
future spot rate. If the speculators’ expectations are correct, they will make a profit.
Note, however, that spot exchange rates are volatile and determined by a complex
web of influences: Interest rate differentials are only one among many factors. So,
speculators can also lose. Because speculators are rarely, if ever, truly risk neutral
and without an arbitrage relationship to enforce it, uncovered interest rate parity is
often violated. As a result, we can conclude that forward exchange rates are typically
poor predictors of future spot exchange rates in the short run. Over the longer term,
uncovered interest rate parity and forward rate parity have more empirical support.
EXAMPLE 4
Covered and Uncovered Interest Rate Parity: Predictors of
Future Spot Rates
An Australia-based fixed-income asset manager is deciding how to allocate money
between Australia and Japan. Note that the base currency in the exchange rate
quote (AUD) is the domestic currency for the asset manager.
JPY/AUD spot rate (mid-market) 71.78
One-year forward points (mid-market) −139.4
One-year Australian deposit rate 3.00%
One-year Japanese deposit rate 1.00%
1. Based on uncovered interest rate parity, over the next year, the expected
change in the JPY/AUD rate is closest to a(n):
A. decrease of 6%.
B. decrease of 2%.
C. increase of 2%.
Solution
B is correct. The expected depreciation of the Australian dollar (decline in
the JPY/AUD rate) is equal to the interest rate differential between Australia
and Japan (3% − 1%).

© CFA Institute. For candidate use only. Not for distribution.
Covered and Uncovered Interest Rate Parity and Forward Rate Parity 27
2. The best explanation of why this prediction may not be very accurate is that:
A. covered interest rate parity does hold in this case.
B. the forward points indicate that a riskless arbitrage opportunity exists.
C. there is no arbitrage condition that forces uncovered interest rate
parity to hold.
Solution
C is correct. There is no arbitrage condition that forces uncovered interest
rate parity to hold. In contrast, arbitrage virtually always ensures that cov-
ered interest rate parity holds. This is the case for our table, where the −139
point discount is calculated from the covered interest rate parity equation.
3. Using the forward points to forecast the future JPY/AUD spot rate one year
ahead assumes that:
A. investors are risk neutral.
B. spot rates follow a random walk.
C. it is not necessary for uncovered interest rate parity to hold.
Solution
A is correct. Using forward rates (i.e., adding the forward points to the
spot rate) to forecast future spot rates assumes that uncovered interest rate
parity and forward rate parity hold. Uncovered interest rate parity assumes
that investors are risk neutral. If these conditions hold, then movements in
the spot exchange rate, although they approximate a random walk, will not
actually be a random walk because current interest spreads will determine
expected exchange rate movements.
4. Forecasting that the JPY/AUD spot rate one year from now will equal 71.78
assumes that:
A. investors are risk neutral.
B. spot rates follow a random walk.
C. it is necessary for uncovered interest rate parity to hold.
Solution
B is correct. Assuming that the current spot exchange rate is the best pre-
dictor of future spot rates assumes that exchange rate movements follow a
random walk. If uncovered interest rate parity holds, the current exchange
rate will not be the best predictor unless the interest rate differential hap-
pens to be zero. Risk neutrality is needed to enforce uncovered interest rate
parity, but it will not make the current spot exchange rate the best predictor
of future spot rates.
5. If the asset manager completely hedged the currency risk associated with a
one-year Japanese deposit using a forward rate contract, the one-year all-in
holding return, in AUD, would be closest to:
A. 0%.
B. 1%.
C. 3%.
Solution
C is correct. A fully hedged JPY investment would provide the same return
as the AUD investment: 3%. This represents covered interest rate parity, an
arbitrage condition.

© CFA Institute. For candidate use only. Not for distribution.
28 Learning Module 1 Currency Exchange Rates: Understanding Equilibrium Value
6. The fixed-income manager collects the following information and uses it,
along with the international parity conditions, to estimate investment re-
turns and future exchange rate movements.
Today’s One-Year MRR Currency Pair Spot Rate Today
JPY 0.10% JPY/USD 105.40
USD 0.10% USD/GBP 1.2303
GBP 3.00% JPY/GBP 129.67
If covered interest rate parity holds, the all-in one-year investment return to
a Japanese investor whose currency exposure to the GBP is fully hedged is
closest to:
A. 0.10%.
B. 0.17%.
C. 3.00%.
Solution
A is correct. If covered interest rate parity holds (and it very likely does,
because this is a pure arbitrage relationship), then the all-in investment
return to a Japanese investor in a one-year, fully hedged GBP MRR position
would be identical to a one-year JPY MRR position: 0.10%. No calculations
are necessary.
7. If uncovered interest rate parity holds, today’s expected value for the JPY/
GBP currency pair one year from now would be closest to:
A. 126.02.
B. 129.67.
C. 130.05.
Solution
A is correct. If uncovered interest rate parity holds, then forward rate parity
will hold and the expected spot rate one year forward is equal to the one-
year forward exchange rate. This forward rate is calculated in the usual
manner, given the spot exchange rates and MRRs:
Se = F = 129.67(1.001/1.03) = 126.02.
8. If uncovered interest rate parity holds, between today and one year from
now, the expected movement in the JPY/USD currency pair is closest to:
A. −1.60%.
B. +0.00%.
C. +1.63%.
Solution
B is correct. Given uncovered interest rate parity, the expected change in a
spot exchange rate is equal to the interest rate differential. At the one-year
term, there is no difference between USD MRR and JPY MRR.

© CFA Institute. For candidate use only. Not for distribution.
Purchasing Power Parity 29
PURCHASING POWER PARITY 8
explain international parity conditions (covered and uncovered
interest rate parity, forward rate parity, purchasing power parity, and
the international Fisher effect)
describe relations among the international parity conditions
evaluate the use of the current spot rate, the forward rate,
purchasing power parity, and uncovered interest parity to forecast
future spot exchange rates
So far, we have looked at the relationship between exchange rates and interest rate
differentials. Now, we turn to examining the relationship between exchange rates and
inflation differentials. The basis for this relationship is known as purchasing power
parity (PPP).
Various versions of PPP exist. The foundation for all of the versions is the law
of one price. According to the law of one price, identical goods should trade at the
same price across countries when valued in terms of a common currency. To simplify
the explanation, as we did with our examples for covered and uncovered interest rate
parity, let’s continue to use the foreign/domestic currency quote convention (f/d) and
the case where the base currency in the P/B notation is the domestic currency for the
investor in the f/d notation.
x
The law of one price asserts that the foreign price of good x, P , should equal the
f
x
exchange rate–adjusted price of the identical good in the domestic country, P :
d
P x = S × P x .
f f/d d
For example, for a euro-based consumer, if the price of good x in the euro area is EUR
100 and the nominal exchange rate stands at 1.15 USD/EUR, then the price of good
x in the United States should equal USD 115.
The absolute version of PPP simply extends the law of one price to the broad
range of goods and services that are consumed in different countries. Expanding our
example above to include all goods and services, not just good x, the broad price level
of the foreign country (P) should equal the currency-adjusted broad price level in
f
the domestic country (P ):
d
P = (S )(P ).
f f/d d
This equation implicitly assumes that all domestic and foreign goods are tradable and
that the domestic and foreign price indexes include the same bundle of goods and
services with the same exact weights in each country. Rearranging this equation and
solving for the nominal exchange rate (S ), the absolute version of PPP states that
f/d
the nominal exchange rate will be determined by the ratio of the foreign and domestic
broad price indexes:
S = P/P .
f/d f d
The absolute version of PPP asserts that the equilibrium exchange rate between two
countries is determined entirely by the ratio of their national price levels. However, it
is highly unlikely that this relationship actually holds in the real world. The absolute
version of PPP assumes that goods arbitrage will equate the prices of all goods and
service across countries, but if transaction costs are significant and/or not all goods
and services are tradable, then goods arbitrage will be incomplete. Hence, sizable and
persistent departures from absolute PPP are likely.

© CFA Institute. For candidate use only. Not for distribution.
30 Learning Module 1 Currency Exchange Rates: Understanding Equilibrium Value
However, if it is assumed that transaction costs and other trade impediments are
constant over time, it might be possible to show that changes in exchange rates and
changes in national price levels are related, even if the relationship between exchange
rate levels and national price levels does not hold. According to the relative version
of PPP, the percentage change in the spot exchange rate (%ΔS ) will be completely
f/d
determined by the difference between the foreign and domestic inflation rates (π − π ):
f d
%Δ S f /d ≅ π f − π d . (3)
Intuitively, the relative version of PPP implies that the exchange rate changes to offset
changes in competitiveness arising from inflation differentials. For example, if the
foreign inflation rate is assumed to be 9% while the domestic inflation rate is assumed
to be 5%, then the S exchange rate must rise by 4% (%ΔS = 9% − 5% = 4%) in
f/d f/d
order to maintain the relative competitiveness of the two regions: The currency of the
high-inflation country should depreciate relative to the currency of the low-inflation
country. If the S exchange rate remained unchanged, the higher foreign inflation rate
f/d
would erode the competitiveness of foreign companies relative to domestic companies.
Conversion from Absolute Levels to a Rate of Change
We will occasionally need to convert from a relationship expressed in levels of
the relevant variables to a relationship among rates of change. If X = (Y × Z), then
(1 + %ΔX) = (1 + %ΔY)(1 + %ΔZ)
and
%ΔX ≈ %ΔY + %ΔZ
because (%ΔY × %ΔZ) is “small.” Similarly, it can be shown that if X = (Y/Z), then
(1 + %ΔX) = (1 + %ΔY)/(1 + %ΔZ)
and
%ΔX ≈ %ΔY − %ΔZ.
Applying this conversion to the equation for absolute PPP gives Equation 3.
Whereas the relative version of PPP focuses on actual changes in exchange rates
being driven by actual differences in national inflation rates, the ex ante version of
PPP asserts that the expected changes in the spot exchange rate are entirely driven
by expected differences in national inflation rates. Ex ante PPP tells us that countries
that are expected to run persistently high inflation rates should expect to see their
currencies depreciate over time, while countries that are expected to run relatively low
inflation rates on a sustainable basis should expect to see their currencies appreciate
over time. Ex ante PPP can be expressed as
%Δ S e = π e − π e , (4)
f/d f d
where it is understood that the use of expectations (the superscript e) indicates
e
that we are now focused on future periods. That is, % Δ S represents the expected
f/d
e e
percentage change in the spot exchange rate, while π and π represent the expected
d f
domestic and foreign inflation rates over the same period.
Studies have found that while over shorter horizons nominal exchange rate move-
ments may appear random, over longer time horizons nominal exchange rates tend to
gravitate toward their long-run PPP equilibrium values.

© CFA Institute. For candidate use only. Not for distribution.
Purchasing Power Parity 31
Exhibit 2 illustrates the success, or lack thereof, of the relative version of PPP at
different time horizons: 1 year, 5 years, 10 years, and 15 years for a selection of coun-
tries over the period 1990-2020. Each chart plots the inflation differential (vertical
axis) against the percentage change in the exchange rate (horizontal axis). If PPP
holds, the points should fall along an upward-sloping diagonal line. The first panel
of Exhibit 2 indicates no clear relationship between changes in exchange rates and
inflation differentials at the one-year time horizon. As the time horizon is lengthened
to five years and beyond, however, a strong positive relationship becomes apparent.
Hence, PPP appears to be a valid framework for assessing long-run fair value in the
FX markets, even though the path to PPP equilibrium may be slow.
Exhibit 2: Effect of Relative Inflation Rates on Exchange Rates at Different
Time Horizons
A. 1-Year Intervals B. 6-Year Intervals
Average Annual Average Annual
Inflation Differential Inflation Differential
50 50
40 40
30 30
20 20
10 10
0 0
–10 –10
–20 –20
–30 –30
–40 –40
–50 –50
–50–40–30–20–10 0 10 20 30 40 50 –50–40–30–20–10 0 10 20 30 40 50
Annual Change in Exchange Rate (%) Annual Change in Exchange Rate (%)
C. 12-Year Intervals D. 24-Year Intervals
Average Annual Average Annual
Inflation Differential Inflation Differential
50 50
40 40
30 30
20 20
10 10
0 0
–10 –10
–20 –20
–30 –30
–40 –40
–50 –50
–50–40–30–20–10 0 10 20 30 40 50 –50–40–30–20–10 0 10 20 30 40 50
Annual Change in Exchange Rate (%) Annual Change in Exchange Rate (%)
Exhibit 3 illustrates the success of the relative version of PPP even in the short run
when differences in inflation rates between countries are large. Note that the Brazilian
Real-USD exchange rate changes rapidly in the period 1980-1993, mirroring the very
large differences in relative inflation between hyperinflationary Brazil and low infla-
tion rate United States. It also indicates that the majority countries did not have large

© CFA Institute. For candidate use only. Not for distribution.
32 Learning Module 1 Currency Exchange Rates: Understanding Equilibrium Value
inflation differentials with the United States, and so 1-year changes in exchange rates
cluster near the origin. This mirrors the upper left panel in Exhibit 2 above, which
excludes Brazil from the sample of countries.
Exhibit 3: Effect of Large Differences in Inflation Rates on Exchange Rates
over 1-Year Time Horizons
REAL/USD Differences in Inflation Rates
3.5 600
400
3.0
200
2.5
0
–200
2.0
Exchange Rate –400
(left axis)
1.5 Differential
(right axis) –600
1.0 –800
77 78 79 80 81 82 83 84 85 86 87 88 89 90
9 THE FISHER EFFECT, REAL INTEREST RATE PARITY,
AND INTERNATIONAL PARITY CONDITIONS
explain international parity conditions (covered and uncovered
interest rate parity, forward rate parity, purchasing power parity, and
the international Fisher effect)
describe relations among the international parity conditions
evaluate the use of the current spot rate, the forward rate,
purchasing power parity, and uncovered interest parity to forecast
future spot exchange rates
explain approaches to assessing the long-run fair value of an
exchange rate
So far, we have examined the relationships between exchange rates and interest rate
differentials and between exchange rates and inflation differentials. Now, we will begin
to bring these concepts together by examining how exchange rates, interest rates, and
inflation rates interact.
According to what economists call the Fisher effect, one can break down the
nominal interest rate (i) in a given country into two parts: (1) the real interest rate
(r) in that particular country and (2) the expected inflation rate (πe) in that country:

© CFA Institute. For candidate use only. Not for distribution.
The Fisher Effect, Real Interest Rate Parity, and International Parity Conditions 33
i = r + πe.
To relate this concept to exchange rates, we can write the Fisher equation for both
the domestic country and a foreign country. If the Fisher effect holds, the nominal
interest rates in both countries will equal the sum of their respective real interest rates
and expected inflation rates:
i = r + π e .
d d d
i = r + π e .
f f f
Let’s take a closer look at the macroeconomic forces that drive the trend in nominal
yield spreads. Subtracting the top equation from the bottom equation shows that
the nominal yield spread between the foreign and domestic countries (i − i ) equals
f d
the sum of two parts: (1) the foreign–domestic real yield spread (r − r ) and (2) the
f d
e e
foreign–domestic expected inflation differential ( π − π ):
f d
i f − i d = ( r f − r d ) + ( π f e − π d e ) .
We can rearrange this equation to solve for the real interest rate differential instead
of the nominal interest rate differential:
( r f − r d ) = ( i f − i d ) − ( π f e − π d e ) .
To tie this material to our previous work on exchange rates, recall our expression for
uncovered interest rate parity:
%Δ S e = i − i .
f/d f d
The nominal interest rate spread (i − i ) equals the expected change in the exchange
f d
e
rate (% Δ S ).
f/d
Recall also the expression for ex ante PPP:
%Δ S e = π e − π e .
f/d f d
The difference in expected inflation rates equals the expected change in the exchange
rate. Combining these two expressions, we derive the following:
i − i = π e − π e .
f d f d
The nominal interest rate spread is equal to the difference in expected inflation rates.
We can therefore conclude that if uncovered interest rate parity and ex ante PPP hold,
(r − r ) = 0.
f d
The real yield spread between the domestic and foreign countries (r − r ) will be zero,
f d
and the level of real interest rates in the domestic country will be identical to the level
of real interest rates in the foreign country.
The proposition that real interest rates will converge to the same level across
different markets is known as the real interest rate parity condition.
Finally, if real interest rates are equal across markets, then it also follows that the
foreign–domestic nominal yield spread is determined solely by the foreign–domestic
expected inflation differential:
i − i = π e − π e .
f d f d
This is known as the international Fisher effect. The reader should be aware that
some authors refer to uncovered interest rate parity as the “international Fisher effect.”
We reserve this term for the relationship between nominal interest rate differentials
and expected inflation differentials because the original (domestic) Fisher effect is a
relationship between interest rates and expected inflation.

© CFA Institute. For candidate use only. Not for distribution.
34 Learning Module 1 Currency Exchange Rates: Understanding Equilibrium Value
The international Fisher effect and, by extension, real interest rate parity assume
that currency risk is the same throughout the world. However, not all currencies carry
the same risk. For example, an emerging country may have a high level of indebtedness,
which could result in an elevated level of currency risk (i.e., likelihood of currency
depreciation). In this case, because the emerging market currency has higher risk,
subtracting the expected inflation rate from the nominal interest rate will result in a
calculated real interest rate that is higher than in other countries. Economists typically
separate the nominal interest rate into the real interest rate, an inflation premium,
and a risk premium. The emerging country’s investors will require a risk premium
for holding the currency, which will be reflected in nominal and real interest rates
that are higher than would be expected under the international Fisher effect and real
interest rate parity conditions.
EXAMPLE 5
PPP and the International Fisher Effect
An Australia-based fixed-income investment manager is deciding how to allocate
her portfolio between Australia and Japan. (As before, the AUD is the domestic
currency.) Australia’s one-year deposit rate is 3%, considerably higher than Japan’s
1% rate, but the Australian dollar is estimated to be roughly 10% overvalued
relative to the Japanese yen based on purchasing power parity. Before making her
asset allocation, the investment manager considers the implications of interest
rate differentials and PPP imbalances.
1. All else equal, which of the following events would restore the Australian
dollar to its PPP value?
A. The Japanese inflation rate increases by 2%.
B. The Australian inflation rate decreases by 10%.
C. The JPY/AUD exchange rate declines by 10%.
Solution
C is correct. If the Australian dollar is overvalued by 10% on a PPP basis,
with all else held equal, a depreciation of the JPY/AUD rate by 10% would
move the Australian dollar back to equilibrium.
2. If real interest rates in Japan and Australia were equal, then under the
international Fisher effect, the inflation rate differential between Japan and
Australia would be closest to:
A. 0%.
B. 2%.
C. 10%.
Solution
B is correct. If the real interest rates were equal, then the difference in nomi-
nal yields would be explained by the difference in inflation rates (3% − 1%).
3. According to the theory and empirical evidence of purchasing power parity,
which of the following would not be true if PPP holds in the long run?
A. An exchange rate’s equilibrium path should be determined by the
long-term trend in domestic price levels relative to foreign price levels.

© CFA Institute. For candidate use only. Not for distribution.
The Fisher Effect, Real Interest Rate Parity, and International Parity Conditions 35
B. Deviations from PPP might occur over short- and medium-term peri-
ods, but fundamental forces should eventually work to push exchange
rates toward their long-term PPP path.
C. High-inflation countries should tend to see their currencies appreciate
over time.
Solution
C is correct. According to PPP, high-inflation countries should see their cur-
rencies depreciate (at least, over the longer term) in order to re-equilibrate
real purchasing power between countries.
4. Which of the following would best explain the failure of the absolute version
of PPP to hold?
A. Inflation rates vary across countries.
B. Real interest rates are converging across countries.
C. Trade barriers exist, and different product mixes are consumed across
countries.
Solution
C is correct. The absolute version of PPP assumes that all goods and ser-
vices are tradable and that the domestic and foreign price indexes include
the same bundle of goods and services with the same exact weights in each
country.
International Parity Conditions: Tying All the Pieces Together
As noted above, the various parity relationships usually do not hold over short time
horizons. However, studies show that over longer time periods, there is a discern-
ible interaction among nominal interest rates, exchange rates, and inflation rates
across countries, such that the international parity conditions serve as an anchor for
longer-term exchange rate movements. We now summarize the key international
parity conditions and describe how they are all linked.
1. According to covered interest rate parity, arbitrage ensures that nominal
interest rate spreads equal the percentage forward premium (or discount).
2. According to uncovered interest rate parity, the expected percentage change
of the spot exchange rate should, on average, be reflected in the nominal
interest rate spread.
3. If both covered and uncovered interest rate parity hold—that is, the nom-
inal yield spread equals both the forward premium (or discount) and the
expected percentage change in the spot exchange rate—then the forward
exchange rate will be an unbiased predictor of the future spot exchange rate.
4. According to the ex ante PPP approach to exchange rate determination, the
expected change in the spot exchange rate should equal the expected differ-
ence between domestic and foreign inflation rates.
5. Assuming the Fisher effect holds in all markets—that is, the nominal inter-
est rate in each market equals the real interest rate plus the expected infla-
tion rate—and also assuming that real interest rates are broadly the same
across all markets (real interest rate parity), then the nominal yield spread
between domestic and foreign markets will equal the domestic–foreign
expected inflation differential, which is the international Fisher effect.

© CFA Institute. For candidate use only. Not for distribution.
36 Learning Module 1 Currency Exchange Rates: Understanding Equilibrium Value
6. If ex ante PPP and the international Fisher effect hold, then expected infla-
tion differentials should equal both the expected change in the exchange
rate and the nominal interest rate differential. This relationship implies that
the expected change in the exchange rate equals the nominal interest rate
differential, which is uncovered interest rate parity.
In sum, if all the key international parity conditions held at all times, then the
expected percentage change in the spot exchange rate would equal
■ the forward premium or discount (expressed in percentage terms),
■ the nominal yield spread between countries, and
■ the difference between expected national inflation rates.
In other words, if all these parity conditions held, it would be impossible for a global
investor to earn consistent profits on currency movements. If forward exchange rates
accurately predicted the future path of spot exchange rates, there would be no way
to make money in forward exchange speculation. If high-yield currencies fell in value
versus low-yield currencies exactly in line with the path implied by nominal interest
rate spreads, all markets would offer the same currency-adjusted total returns over
time. Investors would have no incentive to shift funds from one market to another
based solely on currency considerations.
EXAMPLE 6
The Relationships among the International Parity
Conditions
1. Which of the following is a no-arbitrage condition?
A. Real interest rate parity
B. Covered interest rate parity
C. Uncovered interest rate parity
Solution
B is correct. Covered interest rate parity is enforced by equating the invest-
ment return on two riskless investments (domestic and currency-hedged
foreign).
2. Forward rates are unbiased predictors of future spot rates if two parity con-
ditions hold. Which of the following is not one of these conditions?
A. Real interest rate parity
B. Covered interest rate parity
C. Uncovered interest rate parity
Solution
A is correct. Both covered and uncovered interest rate parity must hold for
the forward rate to be an unbiased predictor of the future spot rate. Real
interest rate parity is not required.
3. The international Fisher effect requires all but which of the following to
hold?
A. Ex ante PPP
B. Absolute PPP

© CFA Institute. For candidate use only. Not for distribution.
The Carry Trade 37
C. Real interest rate parity
Solution
B is correct. The international Fisher effect is based on real interest rate
parity and ex ante PPP (not absolute PPP).
4. The forward premium/discount is determined by nominal interest rate dif-
ferentials because of:
A. the Fisher effect.
B. covered interest parity.
C. real interest rate parity.
Solution
B is correct. The forward premium/discount is determined by covered inter-
est rate arbitrage.
5. If all of the key international parity conditions held at all times, then the
expected percentage change in the spot exchange rate would equal all except
which of the following?
A. The real yield spread
B. The nominal yield spread
C. The expected inflation spread
Solution
A is correct. If all the international parity conditions held, the real yield
spread would equal zero, regardless of expected changes in the spot ex-
change rate.
THE CARRY TRADE 10
describe the carry trade and its relation to uncovered interest rate
parity and calculate the profit from a carry trade
According to uncovered interest rate parity, high-yield currencies are expected to
depreciate in value, while low-yield currencies are expected to appreciate in value. If
uncovered interest rate parity held at all times, investors would not be able to profit
from a strategy that undertook long positions in high-yield currencies and short posi-
tions in low-yield currencies. The change in spot rates over the tenor of the forward
contracts would cancel out the interest rate differentials locked in at the inception
of the position.
Uncovered interest rate parity is one of the most widely tested propositions in
international finance. The evidence suggests that uncovered interest rate parity does
not hold over short and medium time periods. Studies have generally found that
high-yield currencies, on average, have not depreciated and low-yield currencies have
not appreciated to the levels predicted by interest rate differentials.
These findings underscore the potential profitability of a trading strategy known
as the FX carry trade, which involves taking long positions in high-yield currencies
and short positions in low-yield currencies. The latter are often referred to as “funding
currencies.” As a simplified example of the carry trade, assume a trader can borrow

© CFA Institute. For candidate use only. Not for distribution.
38 Learning Module 1 Currency Exchange Rates: Understanding Equilibrium Value
Canadian dollars at 1% and earn 9% on an investment in Brazilian reals for one year.
To execute the trade to earn 8% from the interest rate differential, the trader will do
the following:
1. Borrow Canadian dollars at t = 0.
2. Sell the dollars and buy Brazilian reals at the spot rate at t = 0.
3. Invest in a real-denominated investment at t = 0.
4. Liquidate the Brazilian investment at t = 1.
5. Sell the reals and buy dollars at the spot rate at t = 1.
6. Pay back the dollar loan.
If the real appreciates, the trader’s profits will be greater than 8% because the stron-
ger real will buy more dollars in one year. If the real depreciates, the trader’s profits
will be less than 8% because the weaker real will buy fewer dollars in the future. If the
real falls in value by more than 8%, the trader will experience losses. The carry trader’s
return consists of the intermarket yield spread, the currency appreciation/deprecia-
tion, and the foreign investment appreciation/depreciation. Typically, a carry trade is
executed using an investment in highly rated government debt so as to mitigate credit
risk. In this simplified example, we use an additive approach to determine the trader’s
returns (i.e., we ignore the currency gain or loss on the 8% interest rate differential).
Historical evidence shows that carry trade strategies have generated positive returns
over extended periods (see for example Dimson, Marsh, McGinnie, Staunton, and
Wilmot 2012). One argument for the persistence of the carry trade is that the yields in
higher interest rate countries reflect a risk premium due to a more unstable economy,
while low-yield currencies represent less risky markets. Although small increases in
financial market and/or FX volatility are unlikely to materially affect carry strategy
profits, elevated levels of volatility and/or perceived risk in the financial markets can
quickly turn these profits into substantial losses. That is, during turbulent periods,
the returns on long high-yield currency positions will tend to decline dramatically,
while the losses on short low-yield currency positions will tend to rise dramatically.
To understand why, we need to understand the nature of the risk and reward in
the carry trade. The reward is the gradual accrual of the interest rate differential—
income that is unrelated to exchange rate volatility. The risk arises from the potential
for sudden adverse exchange rate movements that result in instantaneous capital
losses. During periods of low turbulence, investors may feel relatively confident that
exchange rate movements will not jeopardize the gradual accrual of the interest rate
differential. Because low-volatility regimes have tended to be the norm and often last
for extended periods, investors can become complacent, taking on larger carry trade
positions in a search for yield but increasing their risk exposures. When volatility in
the currency markets spikes, however, the risk of an adverse exchange rate move-
ment rises sharply relative to the gradual flow of income. As the trade moves toward
unprofitability, investors may rush to unwind the carry trade, selling high-yielding
currencies and re-purchasing low-yielding currencies. These carry trades are often
large-scale trades initiated by trading firms and other opportunistic investors, such as
hedge funds. Traders often have stop-loss orders in place that are triggered when price
declines reach a certain level. When they all attempt to unwind the trades at once,
the selling pressure adds to the losses on the long position currency and the buying
pressure on the short position currency drives that currency higher, exacerbating
the loss. The “flight to quality” during turbulent times and the leverage inherent in
the carry trade further compound the losses. The upshot is that during periods of low
volatility, carry trades tend to generate positive returns, but they are prone to significant
crash risk in turbulent times.

© CFA Institute. For candidate use only. Not for distribution.
The Carry Trade 39
The tendency for carry trades to experience periodic crashes results in a non-normal
distribution of returns for both developed and emerging market (EM) carry trades.
Relative to a normal distribution, the distributions tend to be more peaked, with
fatter tails and negative skewness. The more peaked distribution around the mean
implies that carry trades have typically generated a larger number of trades with small
gains/losses than would occur with the normal distribution. Although carry trades
have generated positive returns on average in the past, the negative skew and fat tails
indicate that carry trades have tended to have more frequent and larger losses than
would have been experienced had the return distribution been normal.
EXAMPLE 7
Carry Trade Strategies
A currency fund manager is considering allocating a portion of her FX portfolio
to carry trade strategies. The fund’s investment committee asks the manager a
number of questions about why she has chosen to become involved in FX carry
trades and how she will manage the risk of potentially large downside moves
associated with the unwinding of carry trades. Which of the following would
be her best responses to the investment committee’s questions?
1. Carry trades can be profitable when:
A. covered interest rate parity does not hold.
B. uncovered interest rate parity does not hold.
C. the international Fisher effect does not hold.
Solution
B is correct. The carry trade is based on the supposition that uncovered
interest rate parity does not hold.
2. Over time, the return distribution of the fund’s FX carry trades is most likely
to resemble a:
A. normal distribution with fat tails.
B. distribution with fat tails and a negative skew.
C. distribution with thin tails and a positive skew.
Solution
B is correct. The “crash risk” of carry trades implies a fat-tailed distribution
skewed toward a higher probability of large losses (compared with a normal
distribution).
3. The volatility of the fund’s returns relative to its equity base is best explained
by:
A. leverage.
B. low deposit rates in the funding currency.
C. the yield spread between the high- and low-yielding currencies.
Solution
A is correct. Carry trades are leveraged trades (borrow in the funding cur-
rency, invest in the high-yield currency), and leverage increases the volatility
in the investor’s return on equity.

© CFA Institute. For candidate use only. Not for distribution.
40 Learning Module 1 Currency Exchange Rates: Understanding Equilibrium Value
4. A Tokyo-based asset manager enters into a carry trade position based on
borrowing in yen and investing in one-year Australian MRR.
Spot Rate Spot Rate One
Today’s One-Year MRR Currency Pair Today Year Later
JPY 0.10% JPY/USD 105.40 104.60
AUD 1.70% USD/AUD 0.6810 0.6850
After one year, the all-in return to this trade, measured in JPY terms, would
be closest to:
A. +0.03%.
B. +1.53%.
C. +1.63%.
Solution
B is correct. To calculate the all-in return for a Japanese investor in a one-
year AUD MRR deposit, we must first calculate the current and one-year-
later JPY/AUD cross rates. Because USD 1.0000 buys JPY 105.40 today
and AUD 1.0000 buys USD 0.6810 today, today’s JPY/AUD cross rate is the
product of these two numbers: 105.40 × 0.6810 = 71.78 (rounded to two
decimal places). Similarly, one year later, the observed cross rate is 104.60 ×
0.6850 = 71.65 (rounded to two decimal places).
Accordingly, measured in yen, the investment return for the unhedged Aus-
tralian MRR deposit is
(1/71.78)(1 + 1.70%)71.65 − 1 = 0.0152.
Against this 1.52% gross return, however, the manager must charge the
borrowing costs to fund the carry trade investment (one-year JPY MRR was
0.10%). Hence, the net return on the carry trade is 1.52% − 0.10% = 1.42%.
We can also calculate the profit using a transactional approach. Assuming
an initial position of, for example, 100 yen (JPY 100), the investor will obtain
JPY 100 × 1/JPY 71.78 = AUD 1.3931. After one year, the investment will
be worth AUD 1.3931 × 1.017 = AUD 1.4168. Converting back to yen in
one year results in AUD 1.4168 × JPY 71.65/AUD = JPY 101.51. Paying off
the yen loan results in a profit of JPY 101.51 − (JPY 100 × 1.001) = JPY 1.41.
This is equivalent to the 1.42% profit calculated previously (slight difference
arising due to rounding).
11 THE IMPACT OF BALANCE OF PAYMENTS FLOWS
explain how flows in the balance of payment accounts affect
currency exchange rates
As noted earlier, the parity conditions may be appropriate for assessing fair value for
currencies over long horizons, but they are of little use as a real-time gauge of value.
There have been many attempts to find a better framework for determining a curren-
cy’s short- or long-run equilibrium value. In this section, we examine the influence
of trade and capital flows.

© CFA Institute. For candidate use only. Not for distribution.
The Impact of Balance of Payments Flows 41
A country’s balance of payments consists of its current account as well as its capital
and financial account. The official balance of payments accounts make a distinction
between the “capital account” and the “financial account” based on the nature of the
assets involved. For simplicity, we will use the term “capital account” here to reflect
all investment/financing flows. Loosely speaking, the current account reflects flows
in the real economy, which refers to that part of the economy engaged in the actual
production of goods and services (as opposed to the financial sector). The capital
account reflects financial flows. Decisions about trade flows (the current account)
and investment/financing flows (the capital account) are typically made by different
entities with different perspectives and motivations. Their decisions are brought into
alignment by changes in market prices and/or quantities. One of the key prices—
perhaps the key price—in this process is the exchange rate.
Countries that import more than they export will have a negative current account
balance and are said to have current account deficits. Those with more exports than
imports will have a current account surplus. A country’s current account balance must
be matched by an equal and opposite balance in the capital account. Thus, countries
with current account deficits must attract funds from abroad in order to pay for the
imports (i.e., they must have a capital account surplus).
When discussing the effect of the balance of payments components on a country’s
exchange rate, one must distinguish between short- and intermediate-term influences
on the one hand and longer-term influences on the other. Over the long term, countries
that run persistent current account deficits (net borrowers) often see their currencies
depreciate because they finance their acquisition of imports through the continued
use of debt. Similarly, countries that run persistent current account surpluses (net
lenders) often see their currencies appreciate over time.
However, investment/financing decisions are usually the dominant factor in deter-
mining exchange rate movements, at least in the short to intermediate term. There
are four main reasons for this:
■ Prices of real goods and services tend to adjust much more slowly than
exchange rates and other asset prices.
■ Production of real goods and services takes time, and demand decisions
are subject to substantial inertia. In contrast, liquid financial markets allow
virtually instantaneous redirection of financial flows.
■ Current spending/production decisions reflect only purchases/sales of
current production, while investment/financing decisions reflect not only
the financing of current expenditures but also the reallocation of existing
portfolios.
■ Expected exchange rate movements can induce very large short-term capital
flows. This tends to make the actual exchange rate very sensitive to the cur-
rency views held by owners/managers of liquid assets.
In this section, we first examine the impact of current account imbalances on
exchange rates. Then, we take a closer look at capital flows.
Current Account Imbalances and the Determination of
Exchange Rates
Current account trends influence the path of exchange rates over time through several
mechanisms:
■ The flow supply/demand channel
■ The portfolio balance channel
■ The debt sustainability channel

© CFA Institute. For candidate use only. Not for distribution.
42 Learning Module 1 Currency Exchange Rates: Understanding Equilibrium Value
We briefly discuss each of these mechanisms next.
The Flow Supply/Demand Channel
The flow supply/demand channel is based on a fairly simple model that focuses on the
fact that purchases and sales of internationally traded goods and services require the
exchange of domestic and foreign currencies in order to arrange payment for those
goods and services. For example, if a country sold more goods and services than it
purchased (i.e., the country was running a current account surplus), then the demand
for its currency should rise, and vice versa. Such shifts in currency demand should
exert upward pressure on the value of the surplus nation’s currency and downward
pressure on the value of the deficit nation’s currency.
Hence, countries with persistent current account surpluses should see their cur-
rencies appreciate over time, and countries with persistent current account deficits
should see their currencies depreciate over time. A logical question, then, would be
whether such trends can go on indefinitely. At some point, domestic currency strength
should contribute to deterioration in the trade competitiveness of the surplus nation,
while domestic currency weakness should contribute to an improvement in the trade
competitiveness of the deficit nation. Thus, the exchange rate responses to these sur-
pluses and deficits should eventually help eliminate—in the medium to long run—the
source of the initial imbalances.
The amount by which exchange rates must adjust to restore current accounts to
balanced positions depends on a number of factors:
■ The initial gap between imports and exports
■ The response of import and export prices to changes in the exchange rate
■ The response of import and export demand to changes in import and export
prices
If a country imports significantly more than it exports, export growth would need
to far outstrip import growth in percentage terms in order to narrow the current
account deficit. A large initial deficit may require a substantial depreciation of the
currency to bring about a meaningful correction of the trade imbalance.
A depreciation of a deficit country’s currency should result in an increase in import
prices in domestic currency terms and a decrease in export prices in foreign currency
terms. However, empirical studies often find limited pass-through effects of exchange
rate changes on traded goods prices. For example, many studies have found that for
every 1% decline in a currency’s value, import prices rise by only 0.5%—and in some
cases by even less—because foreign producers tend to lower their profit margins in an
effort to preserve market share. In light of the limited pass-through of exchange rate
changes into traded goods prices, the exchange rate adjustment required to narrow a
trade imbalance may be far larger than would otherwise be the case.
Many studies have found that the response of import and export demand to
changes in traded goods prices is often quite sluggish, and as a result, relatively long
lags, lasting several years, can occur between (1) the onset of exchange rate changes,
(2) the ultimate adjustment in traded goods prices, and (3) the eventual impact of
those price changes on import demand, export demand, and the underlying current
account imbalance.
The Portfolio Balance Channel
The second mechanism through which current account trends influence exchange rates
is the so-called portfolio balance channel. Current account imbalances shift financial
wealth from deficit nations to surplus nations. Countries with trade deficits will finance
their trade with increased borrowing. This behavior may lead to shifts in global asset
preferences, which in turn could influence the path of exchange rates. For example,

© CFA Institute. For candidate use only. Not for distribution.
The Impact of Balance of Payments Flows 43
nations running large current account surpluses versus the United States might find
that their holdings of US dollar–denominated assets exceed the amount they desire
to hold in a portfolio context. Actions they might take to reduce their dollar holdings
to desired levels could then have a profound negative impact on the dollar’s value.
The Debt Sustainability Channel
The third mechanism through which current account imbalances can affect exchange
rates is the so-called debt sustainability channel. According to this mechanism, there
should be some upper limit on the ability of countries to run persistently large current
account deficits. If a country runs a large and persistent current account deficit over
time, eventually it will experience an untenable rise in debt owed to foreign investors.
If such investors believe that the deficit country’s external debt is rising to unsustain-
able levels, they are likely to reason that a major depreciation of the deficit country’s
currency will be required at some point to ensure that the current account deficit
narrows significantly and that the external debt stabilizes at a level deemed sustainable.
The existence of persistent current account imbalances will tend to alter the market’s
notion of what exchange rate level represents the true, long-run equilibrium value. For
deficit nations, ever-rising net external debt levels as a percentage of GDP should give
rise to steady (but not necessarily smooth) downward revisions in market expectations
of the currency’s long-run equilibrium value. For surplus countries, ever-rising net
external asset levels as a percentage of GDP should give rise to steady upward revisions
of the currency’s long-run equilibrium value. Hence, one would expect currency values
to move broadly in line with trends in debt and/or asset accumulation.
PERSISTENT CURRENT ACCOUNT DEFICITS: THE US CURRENT ACCOUNT
AND THE US DOLLAR
The historical record indicates that the trend in the US current account has been
an important determinant of the long-term swings in the US dollar’s value but
also that there can be rather long lags between the onset of a deterioration in
the current account balance and an eventual decline in the dollar’s value. For
example, the US current account balance deteriorated sharply in the first half
of the 1980s, yet the dollar soared over that period. The reason for the dollar’s
strength over that period was that high US real interest rates attracted large
inflows of capital from abroad, which pushed the dollar higher despite the large
US external imbalance. Eventually, however, concerns regarding the sustainability
of the ever-widening US current account deficit triggered a major dollar decline
in the second half of the 1980s.
History repeated itself in the second half of the 1990s, with the US current
account balance once again deteriorating while the dollar soared over the same
period. This time, the dollar’s strength was driven by strong foreign direct
investment, as well as both debt- and equity-related flows into the United States.
Beginning in 2001, however, the ever-widening US current account deficit, cou-
pled with a decline in US interest rates, made it more difficult for the United
States to attract the foreign private capital needed to finance its current account
deficit. The dollar eventually succumbed to the weight of ever-larger trade and
current account deficits and began a multi-year slide, starting in 2002–2003.
Interestingly, the US dollar has undergone three major downward cycles since
the advent of floating exchange rates: 1977–1978, 1985–1987, and 2002–2008.
In each of those downward cycles, the dollar’s slide was driven in large part by
concerns over outsized US current account deficits coupled with relatively low
nominal and/or real short-term US interest rates, which made it difficult to
attract sufficient foreign capital to the United States to finance those deficits.

© CFA Institute. For candidate use only. Not for distribution.
44 Learning Module 1 Currency Exchange Rates: Understanding Equilibrium Value
EXCHANGE RATE ADJUSTMENT IN SURPLUS NATIONS: JAPAN AND CHINA
Japan and, for a number of years, China represent examples of countries with
large current account surpluses and illustrate the pressure that those surpluses
can bring to bear on currencies. In the case of Japan, its rising current account
surplus has exerted persistent upward pressure on the yen’s value versus the
dollar over time. Part of this upward pressure simply reflected the increase in
demand for yen to pay for Japan’s merchandise exports. But some of the upward
pressure on the yen might also have stemmed from rising commercial tensions
between the United States and Japan.
Protectionist sentiment in the United States rose steadily with the rising bilat-
eral trade deficit that the United States ran with Japan in the postwar period. US
policymakers contended that the yen was undervalued and needed to appreciate.
With the increasing trade imbalance between the two countries contributing
to more heated protectionist rhetoric, Japan felt compelled to tolerate steady
upward pressure on the yen. As a result, the yen’s value versus the dollar has
tended to move in sync with the trend in Japan’s current account surplus.
12 CAPITAL FLOWS
explain how flows in the balance of payment accounts affect
currency exchange rates
Greater financial integration of the world’s capital markets and greater freedom of
capital to flow across national borders have increased the importance of global financial
flows in determining exchange rates, interest rates, and broad asset price trends. One
can cite many examples in which global financial flows either caused or contributed
to extremes in exchange rates, interest rates, or asset prices.
In numerous cases, global capital flows have helped fuel boom-like conditions
in emerging market economies for a while before, suddenly and often without ade-
quate warning, those flows reversed. The reversals often caused a major economic
downturn, sovereign default, a serious banking crisis, and/or significant currency
depreciation. Excessive emerging market capital inflows often plant the seeds of a
crisis by contributing to:
1. an unwarranted appreciation of the emerging market currency,
2. a huge buildup in external indebtedness,
3. an asset bubble,
4. a consumption binge that contributes to explosive growth in domestic credit
and/or the current account deficit, or
5. an overinvestment in risky projects and questionable activities.
Governments in emerging markets often resist currency appreciation from excessive
capital inflows by using capital controls or selling their currency in the FX market. An
example of capital controls is the Brazilian government 2016 tax on foreign exchange
transactions to control capital flows and raise government revenue. In general, gov-
ernment control of the exchange rate will not be completely effective because even if

© CFA Institute. For candidate use only. Not for distribution.
Capital Flows 45
a government prohibits investment capital flows, some capital flows will be needed
for international trade. In addition, the existence or emergence of black markets for
the country’s currency will inhibit the ability of the government to fully control the
exchange rates for its own currency.
Sometimes, capital flows due to interest rate spreads have little impact on the
trend in exchange rates. Consider the case of the Turkish lira. The lira attracted a
lot of interest on the part of global fund managers over the 2002–10 period, in large
part because of its attractive yields. Turkish–US short-term yield spreads averaged
over 1,000 bps during much of this period. As capital flowed into Turkey, the Turkish
authorities intervened in the foreign exchange market in an attempt to keep the lira
from appreciating. The result was that international investors were not able to reap
the anticipated currency gains over this period. While the return from the movement
in the spot exchange rate was fairly small, a long Turkish lira/short US dollar carry
trade position generated significant long-run returns, mostly from the accumulated
yield spread.
One-sided capital flows can persist for long periods. Consider the case of a
high-yield, inflation-prone emerging market country that wants to promote price
stability and long-term sustainable growth. To achieve price stability, policymakers
in the high-yield economy will initiate a tightening in monetary policy by gradually
raising the level of domestic interest rates relative to yield levels in the rest of the world.
If the tightening in domestic monetary policy is sustained, inflation expectations for
the high-yield economy relative to other economies should gradually decline. The
combination of sustained wide nominal yield spreads and a steady narrowing in rela-
tive inflation expectations should exert upward pressure on the high-yield currency’s
value, resulting in carry trade profits over long periods.
Policymakers in high-yield markets can also pursue policies which attract foreign
investment; such policies might include tighter fiscal policies, liberalization of financial
markets, fewer capital flow restrictions, privatization, and/or a better business envi-
ronment. Such policies should encourage investors to gradually require a lower risk
premium to hold the high-yield currency’s assets and revise upward their assessment
of the long-run equilibrium value of that country’s currency.
The historical evidence suggests that the impact of nominal interest rate spreads
on the exchange rate tends to be gradual. Monetary policymakers tend to adjust their
official lending rates slowly over time—in part because of the uncertainty that policy-
makers face and in part because the authorities do not want to disrupt the financial
markets. This very gradual change in rates implies a very gradual narrowing of the
spread between high-yield and low-yield countries. Similarly, the downward trends
in inflation expectations and risk premiums in the higher-yield market also tend to
unfold gradually. It often takes several years to determine whether structural economic
changes will take root and boost the long-run competitiveness of the higher-yield
country. Because these fundamental drivers tend to reinforce each other over time,
there may be persistence in capital flows and carry trade returns.
Equity Market Trends and Exchange Rates
Increasing equity prices can also attract foreign capital. Although exchange rates and
equity market returns sometimes exhibit positive correlation, the relationship between
equity market performance and exchange rates is not stable. The long-run correlation
between the US equity market and the dollar, for example, is very close to zero, but
over short to medium periods, correlations tend to swing from being highly positive
to being highly negative, depending on market conditions. For instance, between 1990
and 1995, the US dollar fell while the US equity market was strong and the Japanese
yen soared while Japanese stocks were weak. In contrast, between 1995 and early
2000, the US dollar soared in tandem with a rising US equity market while the yen

© CFA Institute. For candidate use only. Not for distribution.
46 Learning Module 1 Currency Exchange Rates: Understanding Equilibrium Value
weakened in tandem with a decline in the Japanese equity market. Such instability in
the correlation between exchange rates and equity markets makes it difficult to form
judgments on possible future currency moves based solely on expected equity market
performance.
Since the global financial crisis, there has been a decidedly negative correlation
between the US dollar and the US equity market. Market observers attribute this
behavior of the US dollar to its role as a safe haven asset. When investors’ appetite
for risk is high—that is, when the market is in “risk-on” mode—investor demand for
risky assets, such as equities, tends to rise, which drives up their prices. At the same
time, investor demand for safe haven assets, such as the dollar, tends to decline, which
drives their values lower. The opposite has occurred when the market has been in
“risk-off” mode.
EXAMPLE 8
Capital Flows and Exchange Rates
Monique Kwan, a currency strategist at a major foreign exchange dealer, is
responsible for formulating trading strategies for the currencies of both devel-
oped market (DM) and emerging market (EM) countries. She examines two
countries—one DM and one EM—and notes that the DM country has what
is considered a low-yield safe haven currency while the EM country has a
high-yield currency whose value is more exposed to fluctuations in the global
economic growth rate. Kwan is trying to form an opinion about movements in
the exchange rate for the EM currency.
1. All else equal, the exchange rate for the EM currency will most likely depre-
ciate if the:
A. long-run equilibrium value of the high-yield currency is revised
upward.
B. nominal yield spread between the EM and DM countries increases
over time.
C. expected inflation differential between the EM and DM countries is
revised upward.
Solution
C is correct. All else equal, an increase in the expected inflation differential
should lead to depreciation of the EM currency.
2. An increase in safe haven demand would most likely:
A. increase the risk premium demanded by international investors to
hold assets denominated in the EM currency.
B. raise the return earned on carry trade strategies.
C. exert upward pressure on the value of the EM currency.
Solution
A is correct. During times of intense risk aversion, investors will crowd into
the safe haven currency. This tendency implies an increased risk premium
demanded by investors to hold the EM currency.
3. Kwan notes that the DM country is running a persistent current account
deficit with the EM country. To isolate the influence of this chronic im-
balance on exchange rates, she focuses only on the bilateral relationship
between the EM and DM countries and makes the simplifying assumption

© CFA Institute. For candidate use only. Not for distribution.
Capital Flows 47
that the external accounts of these two countries are otherwise balanced
(i.e., there are no other current account deficits).
Over time and all else equal, the persistent current account deficit with the
EM country would most likely lead to:
A. a large buildup of the EM country’s assets held by the DM country.
B. an increase in the trade competitiveness of the EM country.
C. an upward revision in the long-run equilibrium EM currency value.
Solution
C is correct. Over time, the DM country will see its level of external debt
rise as a result of the chronic current account imbalance. Eventually, this
trend should lead to a downward revision of the DM currency’s long-run
equilibrium level (via the debt sustainability channel). This is equivalent
to an increase in the EM currency’s long-run exchange rate. A is incorrect
because the DM country’s current account deficit is likely to lead to a build-
up in DM country assets held by the EM country. B is incorrect because,
at some point, the currency strength should contribute to deterioration in
the trade competitiveness of the country with the trade surplus (the EM
country).
4. Kwan notes that because of the high yield on the EM country’s bonds,
international investors have recently been reallocating their portfolios more
heavily toward this country’s assets. As a result of these capital inflows, the
EM country has been experiencing boom-like conditions.
Given the current boom-like conditions in the EM economy, in the near
term, these capital inflows are most likely to lead to:
A. a decrease in inflation expectations in the EM.
B. an increase in the risk premium for the EM.
C. an increase in the EM currency value.
Solution
C is correct. Given the current investor enthusiasm for the EM country’s
assets and the boom-like conditions in the country, it is most likely that in
the near term, the EM currency will appreciate. At the same time, expected
inflation in the EM country is also likely increasing and—given the enthusi-
asm for EM assets—the risk premium is likely decreasing.
5. If these capital inflows led to an unwanted appreciation in the real value of
its currency, the EM country’s government would most likely:
A. impose capital controls.
B. decrease taxes on consumption and investment.
C. buy its currency in the foreign exchange market.
Solution
A is correct. To reduce unwanted appreciation of its currency, the EM coun-
try would be most likely to impose capital controls to counteract the surging
capital inflows. Because these inflows are often associated with overinvest-
ment and consumption, the EM government would not be likely to encour-
age these activities through lower taxes. Nor would the EM country be likely
to encourage further currency appreciation by intervening in the market to
buy its own currency.

© CFA Institute. For candidate use only. Not for distribution.
48 Learning Module 1 Currency Exchange Rates: Understanding Equilibrium Value
6. If government actions were ineffective and the EM country’s bubble eventu-
ally burst, this would most likely be reflected in an increase in:
A. the risk premium for the EM.
B. the EM currency value.
C. the long-run equilibrium EM currency value.
Solution
A is correct. Episodes of surging capital flows into EM countries have often
ended badly (with a rapid reversal of these inflows as the bubble bursts).
This is most likely to be reflected in an increase in the EM risk premium. It
is much less likely that a bursting bubble would be reflected in an increase in
either the EM currency value or its long-term equilibrium value.
7. Finally, Kwan turns to examining the link between the value of the DM
country’s currency and movements in the DM country’s main stock market
index. One of her research associates tells her that, in general, the correla-
tion between equity market returns and changes in exchange rates has been
found to be highly positive over time.
The statement made by the research associate is:
A. correct.
B. incorrect, because the correlation is highly negative over time.
C. incorrect, because the correlation is not stable and tends to converge
toward zero in the long run.
Solution
C is correct. Correlations between equity returns and exchange rates are
unstable in the short term and tend toward zero in the long run.
13 MONETARY AND FISCAL POLICIES
explain the potential effects of monetary and fiscal policy on
exchange rates
As the foregoing discussion indicates, government policies can have a significant
impact on exchange rate movements. We now examine the channels through which
government monetary and fiscal policies are transmitted.
The Mundell–Fleming Model
The Mundell–Fleming model describes how changes in monetary and fiscal policy
within a country affect interest rates and economic activity, which in turn leads to
changes in capital flows and trade and ultimately to changes in the exchange rate. The
model focuses only on aggregate demand and assumes there is sufficient slack in the
economy to allow increases in output without price level increases.
In this model, expansionary monetary policy affects growth, in part, by reducing
interest rates and thereby increasing investment and consumption spending. Given
flexible exchange rates and expansionary monetary policy, downward pressure on

© CFA Institute. For candidate use only. Not for distribution.
Monetary and Fiscal Policies 49
domestic interest rates will induce capital to flow to higher-yielding markets, putting
downward pressure on the domestic currency. The more responsive capital flows are
to interest rate differentials, the greater the depreciation of the currency.
Expansionary fiscal policy—either directly through increased spending or indirectly
via lower taxes—typically exerts upward pressure on interest rates because larger
budget deficits must be financed. With flexible exchange rates and mobile capital,
the rising domestic interest rates will attract capital from lower-yielding markets,
putting upward pressure on the domestic currency. If capital flows are highly sensitive
to interest rate differentials, then the domestic currency will tend to appreciate sub-
stantially. If, however, capital flows are immobile and very insensitive to interest rate
differentials, the policy-induced increase in aggregate demand will increase imports
and worsen the trade balance, creating downward pressure on the currency with no
offsetting capital inflows to provide support for the currency.
The specific mix of monetary and fiscal policies in a country can have a profound
effect on its exchange rate. Consider first the case of high capital mobility. With floating
exchange rates and high capital mobility, a domestic currency will appreciate given a
restrictive domestic monetary policy and/or an expansionary fiscal policy that results
in higher real interest rates. Similarly, a domestic currency will depreciate given an
expansionary domestic monetary policy and/or a restrictive fiscal policy that results
in lower real interest rates. In Exhibit 4, we show that the combination of a restrictive
monetary policy and an expansionary fiscal policy (higher real rates) is extremely
bullish for a currency when capital mobility is high; likewise, the combination of
an expansionary monetary policy and a restrictive fiscal policy (lower real rates) is
bearish for a currency. The effect on the currency of monetary and fiscal policies that
are both expansionary or both restrictive is indeterminate under conditions of high
capital mobility.
Exhibit 4: Monetary–Fiscal Policy Mix and the Determination of Exchange
Rates under Conditions of High Capital Mobility
DEM/USD US Less German Real Interest Rates (bps)
1.9 200
1.8 Differential (right axis)
100
1.7
0
1.6
Exchange Rate
(left axis) –100
1.5
–200
1.4
1.3 –300
93 94 95 96 97 98
Source: Rosenberg (1996, p. 132).
When capital mobility is low, the effects of monetary and fiscal policy on exchange
rates will operate primarily through trade flows rather than capital flows. The com-
bination of expansionary monetary and fiscal policy will be bearish for a currency.

© CFA Institute. For candidate use only. Not for distribution.
50 Learning Module 1 Currency Exchange Rates: Understanding Equilibrium Value
Earlier we said that expansionary fiscal policy will increase imports and hence the
trade deficit, creating downward pressure on the currency. Layering on an expansive
monetary policy will further boost spending and imports, worsening the trade balance
and exacerbating the downward pressure on the currency.
The combination of restrictive monetary and fiscal policy will be bullish for a
currency. This policy mix will tend to reduce imports, leading to an improvement in
the trade balance.
The impact of expansionary monetary and restrictive fiscal policies (or restric-
tive monetary and expansionary fiscal policies) on aggregate demand and the trade
balance, and hence on the exchange rate, is indeterminate under conditions of low
capital mobility. Exhibit 5 summarizes these results.
Exhibit 5: Monetary–Fiscal Policy Mix and the Determination of Exchange
Rates under Conditions of Low Capital Mobility
Expansionary Restrictive
Monetary Monetary
Policy Policy
Domestic
Expansionary
currency Indeterminate
Fiscal Policy
depreciates
Domestic
Restrictive Indeterminate
currency
Fiscal Policy
appreciates
Source: Adapted from Rosenberg (1996, p. 133).
Exhibit 4 is more relevant for the G–10 countries because capital mobility tends to
be high in developed economies. Exhibit 5 is more relevant for emerging market
economies that restrict capital movement.
A classic case in which a dramatic shift in the policy mix caused dramatic changes
in exchange rates was that of Germany in 1990–1992. During that period, the German
government pursued a highly expansionary fiscal policy to help facilitate German
unification. At the same time, the Bundesbank pursued an extraordinarily restrictive
monetary policy to combat the inflationary pressures associated with unification. The
expansive fiscal/restrictive monetary policy mix drove German interest rates sharply
higher, eventually causing the German currency to appreciate.
Monetary Models of Exchange Rate Determination
In the Mundell–Fleming model, monetary policy is transmitted to the exchange rate
through its impact on interest rates and output. Changes in the price level and/or the
inflation rate play no role. Monetary models of exchange rate determination generally
take the opposite perspective: Output is fixed and monetary policy affects exchange
rates primarily through the price level and the rate of inflation. In this section, we briefly
describe two variations of the monetary approach to exchange rate determination.

© CFA Institute. For candidate use only. Not for distribution.
Monetary and Fiscal Policies 51
The monetary approach asserts that an X percent rise in the domestic money
supply will produce an X percent rise in the domestic price level. Assuming that pur-
chasing power parity holds—that is, that changes in exchange rates reflect changes
in relative inflation rates—a money supply–induced increase (decrease) in domestic
prices relative to foreign prices should lead to a proportional decrease (increase) in
the domestic currency’s value.
One of the major shortcomings of the pure monetary approach is the assumption
that purchasing power parity holds in both the short and long runs. Because purchas-
ing power parity rarely holds in either the short or medium run, the pure monetary
model may not provide a realistic explanation of the impact of monetary forces on
the exchange rate.
To rectify that problem, Dornbusch (1976) constructed a modified monetary model
that assumes prices have limited flexibility in the short run but are fully flexible in the
long run. The long-run flexibility of the price level ensures that any increase in the
domestic money supply will give rise to a proportional increase in domestic prices
and thus contribute to a depreciation of the domestic currency in the long run, which
is consistent with the pure monetary model. If the domestic price level is assumed
to be inflexible in the short run, however, the model implies that the exchange rate is
likely to overshoot its long-run PPP path in the short run. With inflexible domestic
prices in the short run, any increase in the nominal money supply results in a decline
in the domestic interest rate. Assuming that capital is highly mobile, the decline in
domestic interest rates will precipitate a capital outflow, which in the short run will
cause the domestic currency to depreciate below its new long-run equilibrium level.
In the long run, once domestic nominal interest rates rise, the currency will appreciate
and move into line with the path predicted by the conventional monetary approach.
Monetary Policy and Exchange Rates: The Historical
Evidence
Historically, changes in monetary policy have had a profound impact on exchange
rates. In the case of the US dollar, the Federal Reserve’s policy of quantitative
easing after the global financial crisis resulted in dollar depreciation from mid-
2009 to 2011. The subsequent ending of quantitative easing in 2014, along with
the anticipation that the United States would raise interest rates before many
other countries, played a key role in driving the dollar higher.
Beginning in 2013, Abenomics—fiscal stimulus, monetary easing, and struc-
tural reforms—and the use of quantitative easing in Japan led to a steady decline
in interest rates and eventually to negative interest rates in 2016. From 2013 to
2015, the value of the yen changed from roughly JPY 90/USD to JPY 120/USD.
Likewise, the use of quantitative easing by the European Central Bank in 2015
led to declines in the value of the euro.
Excessively expansionary monetary policies by central banks in emerging
markets have often planted the seeds of speculative attacks on their currencies.
In the early 1980s, exchange rate crises in Argentina, Brazil, Chile, and Mexico
were all preceded by sharp accelerations in domestic credit expansions. In 2012,
Venezuela began a period of triple-digit inflation, followed by a massive currency
depreciation and an economic crisis.

© CFA Institute. For candidate use only. Not for distribution.
52 Learning Module 1 Currency Exchange Rates: Understanding Equilibrium Value
EXAMPLE 9
Monetary Policy and Exchange Rates
Monique Kwan, the currency strategist at a major foreign exchange dealer, is
preparing a report on the outlook for several currencies that she follows. She
begins by considering the outlook for the currency of a developed market country
with high capital mobility across its borders and a flexible exchange rate. This
DM country also has low levels of public and private debt.
Given these conditions, Kwan tries to assess the impact of each of the fol-
lowing policy changes.
1. For the DM currency, increasing the degree of monetary easing (reducing
interest rates and increasing money supply) will most likely:
A. cause the currency to appreciate.
B. cause the currency to depreciate.
C. have an indeterminate effect on the currency.
Solution
B is correct. A decrease in the policy rate would most likely cause capi-
tal to re-allocate to higher-yielding markets. This would lead to currency
depreciation.
2. The pursuit of an expansionary domestic fiscal policy by the DM country
will, in the short run, most likely:
A. cause the domestic currency’s value to appreciate.
B. cause the domestic currency’s value to depreciate.
C. have an indeterminate effect on the domestic currency’s value.
Solution
A is correct. An expansionary fiscal policy will lead to higher levels of
government debt and interest rates, which will attract international capital
flows. (In the long run, however, an excessive buildup in debt may eventually
cause downward pressure on the domestic currency.)
3. Next, Kwan turns her attention to an emerging market country that has low
levels of public and private debt. Currently, the EM country has a fixed ex-
change rate but no controls over international capital mobility. However, the
country is considering replacing its fixed exchange rate policy with a policy
based on capital controls. These proposed controls are meant to reduce
international capital mobility by limiting short-term investment flows (“hot
money”) in and out of its domestic capital markets.
To maintain the exchange rate peg while increasing the degree of monetary
easing, the EM country will most likely have to:
A. tighten fiscal policy.
B. decrease interest rates.
C. buy its own currency in the FX market.
Solution
C is correct. The looser monetary policy will lead to exchange rate deprecia-
tion. To counter this effect and maintain the currency peg, the central bank
will have to intervene in the FX market, buying the country’s own currency.

© CFA Institute. For candidate use only. Not for distribution.
Monetary and Fiscal Policies 53
A is incorrect because tighter fiscal policy is associated with lower interest
rates and is therefore likely to increase rather than mitigate the downward
pressure on the domestic currency. Similarly, B is incorrect because a move
to lower interest rates would exacerbate the downward pressure on the cur-
rency and hence the pressure on the peg.
4. After the EM country replaces its currency peg with capital controls, would
its exchange rate be unaffected by a tightening in monetary policy?
A. Yes.
B. No, the domestic currency would appreciate.
C. No, the domestic currency would depreciate.
Solution
B is correct. In general, capital controls will not completely eliminate capital
flows but will limit their magnitude and responsiveness to investment incen-
tives such as interest rate differentials. At a minimum, flows directly related
to financing international trade will typically be allowed. The exchange rate
will still respond to monetary policy. With limited capital mobility, however,
monetary policy’s main influence is likely to come through the impact on
aggregate demand and the trade balance. A tighter domestic monetary pol-
icy will most likely lead to higher interest rates and less domestic demand,
including less demand for imported goods. With fewer imports and with ex-
ports held constant, there will be modest upward pressure on the currency.
5. After the EM country replaces its currency peg with capital controls, the
simultaneous pursuit of a tight monetary policy and a highly expansionary
fiscal policy by the EM country will most likely:
A. cause the currency to appreciate.
B. cause the currency to depreciate.
C. have an indeterminate effect on the currency.
Solution
C is correct because (1) capital mobility is low, so the induced increase in
interest rates is likely to exert only weak upward pressure on the currency;
(2) the combined impact on aggregate demand is indeterminate; and (3) if
aggregate demand increases, the downward pressure on the currency due to
a worsening trade balance may or may not fully offset the upward pressure
exerted by capital flows.
The Portfolio Balance Approach
In this section, we re-examine the role fiscal policy plays in determining exchange
rates. The Mundell–Fleming model is essentially a short-run model of exchange rate
determination. It makes no allowance for the long-term effects of budgetary imbal-
ances that typically arise from sustained fiscal policy actions. The portfolio balance
approach to exchange rate determination remedies this limitation. In our previous
discussion of the portfolio balance channel, we stated that the currencies of countries
with trade deficits will decline over time. We expand that discussion here to more
closely examine how exchange rates change over the long term.
In the portfolio balance approach, global investors are assumed to hold a diver-
sified portfolio of domestic and foreign assets, including bonds. The desired allocation
is assumed to vary in response to changes in expected return and risk considerations.

© CFA Institute. For candidate use only. Not for distribution.
54 Learning Module 1 Currency Exchange Rates: Understanding Equilibrium Value
In this framework, a growing government budget deficit leads to a steady increase
in the supply of domestic bonds outstanding. These bonds will be willingly held only
if investors are compensated in the form of a higher expected return. Such a return
could come from (1) higher interest rates and/or a higher risk premium, (2) immediate
depreciation of the currency to a level sufficient to generate anticipation of gains from
subsequent currency appreciation, or (3) some combination of these two factors. The
currency adjustments required in the second mechanism are the core of the portfolio
balance approach.
One of the major insights one should draw from the portfolio balance model is
that in the long run, governments that run large budget deficits on a sustained basis
could eventually see their currencies decline in value.
The Mundell–Fleming and portfolio balance models can be combined into a single
integrated framework in which expansionary fiscal policy under conditions of high
capital mobility may be positive for a currency in the short run but negative in the
long run. Exhibit 6 illustrates this concept. A domestic currency may rise in value
when the expansionary fiscal policy is first put into place. As deficits mount over time
and the government’s debt obligations rise, however, market participants will begin
to wonder how that debt will be financed. If the volume of debt rises to levels that are
believed to be unsustainable, market participants may believe that the central bank
will eventually be pressured to “monetize” the debt—that is, to buy the government’s
debt with newly created money. Such a scenario would clearly lead to a rapid reversal
of the initial currency appreciation. Alternatively, the market may believe that the
government will eventually have to shift toward significant restraint to implement a
more restrictive, sustainable fiscal policy over the longer term.
Exhibit 6: The Short- and Long-Run Response of Exchange Rates to Changes
in Fiscal Policy
Expansionary Restrictive
Monetary Monetary
Policy Policy
Domestic
Expansionary
currency Indeterminate
Fiscal Policy
depreciates
Domestic
Restrictive
Indeterminate currency
Fiscal Policy
appreciates
Source: Rosenberg (2003).
EXAMPLE 10
Fiscal Policy and Exchange Rates
Monique Kwan is continuing her analysis of the foreign exchange rate outlook
for selected countries. She examines a DM country that has a high degree of
capital mobility and a floating-rate currency regime. Kwan notices that although

© CFA Institute. For candidate use only. Not for distribution.
Monetary and Fiscal Policies 55
the current outstanding volume of government debt is low, as a percentage of
GDP, it is rising sharply as a result of expansionary fiscal policy. Moreover,
projections for the government debt-to-GDP ratio point to further increases
well into the future.
Kwan uses the Mundell–Fleming and portfolio balance models to form an
opinion about both the short-run and long-run implications for the DM coun-
try’s exchange rate.
1. Over the short run, Kwan is most likely to expect:
A. appreciation of the DM’s currency.
B. an increase in the DM’s asset prices.
C. a decrease in the DM’s risk premium.
Solution
A is correct. The DM country currently has a low debt load (as a percent-
age of GDP), and in the short run, its expansionary fiscal policy will lead to
higher interest rates and higher real rates relative to other countries. This
path should lead to currency appreciation. The higher domestic interest
rates will (all else equal) depress local asset prices (so B is incorrect), and the
rising debt load is likely to increase rather than decrease the risk premium
(so C is incorrect).
2. Over the medium term, as the DM country’s government debt becomes
harder to finance, Kwan would be most likely to expect that:
A. fiscal policy will turn more accommodative.
B. the mark-to-market value of the debt will increase.
C. monetary policy will become more accommodative.
Solution
C is correct. As government debt becomes harder to finance, the govern-
ment will be tempted to monetize the debt through an accommodative
monetary policy. A is incorrect because an inability to finance the debt will
make it hard for fiscal policy to become more accommodative. B is incorrect
because as investors demand a higher risk premium (a higher return) for
holding the DM country’s debt, the mark-to-market value of the debt will
decline (i.e., bond prices will decrease and bond yields will increase).
3. Assuming that the DM country’s government debt becomes harder to
finance and there is no change in monetary policy, Kwan is most likely to
expect that over the longer term, there will be a fiscal policy response that
will lead to:
A. currency appreciation as yields rise.
B. currency depreciation as yields decline.
C. an indeterminate impact on the currency, depending on which effect
prevails.
Solution
B is correct. As the DM country’s debt ratio deteriorates, foreign investors
will demand a higher rate of return to compensate them for the increased
risk. Assuming that the central bank will not accommodate (monetize) the
rising government debt, the most likely fiscal response is an eventual move
toward fiscal consolidation—reducing the public deficit and debt levels that
were causing the debt metrics to deteriorate. This policy adjustment would

© CFA Institute. For candidate use only. Not for distribution.
56 Learning Module 1 Currency Exchange Rates: Understanding Equilibrium Value
involve issuing fewer government bonds. All else equal, bond yields would
decrease, leading to a weaker domestic currency over the longer term.
A is incorrect because currency appreciation is not likely to accompany
rising yields when the government is having difficulty financing its deficit.
There would be a rising risk premium (a deteriorating investor appetite) for
holding DM assets, and hence a currency appreciation would be unlikely de-
spite high DM yields. To avoid paying these high yields on its debt, the DM
government would eventually have to take measures to reduce its deficit
spending. This approach would eventually help reduce investor risk aversion
and DM yields. C is incorrect because given the deterioration in the DM’s
debt metrics, a depreciation of its exchange rate is likely to be an important
part of the restoration of financial market equilibrium.
14 EXCHANGE RATE MANAGEMENT: INTERVENTION
AND CONTROLS
describe objectives of central bank or government intervention and
capital controls and describe the effectiveness of intervention and
capital controls
Capital flows can be both a blessing and a curse. Capital inflows can be a blessing when
they increase domestic investment, thereby increasing a country’s economic growth
and asset values. Currency appreciation often follows, which increases returns to global
investors. Capital inflows can be a curse, however, if they fuel boom-like conditions,
asset price bubbles, and overvaluation of a country’s currency. If capital inflows then
reverse, the result may be a major economic downturn, a significant decline in asset
prices, and a large depreciation of the currency. Capital inflows often are driven by
a combination of “pull” and “push” factors. Pull factors represent a favorable set of
developments that encourage foreign capital inflows. These factors may stem from
both the public and private sectors. Examples of better economic management by a
government include
■ a decrease in inflation and inflation volatility,
■ more-flexible exchange rate regimes,
■ improved fiscal positions,
■ privatization of state-owned entities,
■ liberalization of financial markets, and
■ lifting of foreign exchange regulations and controls.
Ideally, these changes will facilitate strong economic growth in the private sector,
which will attract further foreign investment. A healthy export sector will generate
improvement in the current account balance and an increase in FX reserves, which can
be used by the government as a buffer against future speculative attacks. The returns
from the currency and assets should increase, increasing the foreign investor’s return.
Push factors driving foreign capital inflows are not determined by the domestic
policies but arise from the primary sources of internationally mobile capital, notably
the investor base in industrial countries. For example, the pursuit of low interest rate
policies in industrial countries since the 2008 financial crisis has encouraged global
investors to seek higher returns abroad.

© CFA Institute. For candidate use only. Not for distribution.
Exchange Rate Management: Intervention and Controls 57
Another important push factor is the long-run trend in asset allocation by industrial
country investors. For example, many fund managers have traditionally had under-
weight exposures to emerging market assets, but with the weight of emerging market
equities in broad global equity market indexes on the rise (as of 2019 the EM share
of world GDP at current prices is over 40%, up from 17% in the 1960s, according to
the IMF), capital flows to EM countries, in the form of increased allocations to EM
equities, are likely to rise.
Private capital inflows to emerging markets go through significant changes over
time. For example, they rose steadily between 2003 and 2007, posting nearly a six-fold
increase over the period. Both push and pull factors contributed to that surge in cap-
ital flows. Net private capital flows to emerging markets tumbled in 2008 and 2009
as heightened risk aversion during the global financial crisis prompted investors to
unwind some of their EM exposures in favor of US assets. In 2010, capital flows to
emerging markets rose as many EM economies weathered the global financial crisis
better than many industrial economies. In addition, the pursuit of ultra-low interest
rate policies in the United States, the euro area, and Japan encouraged global investors
to invest in higher-yielding EM assets.
However beneficial foreign capital is, policymakers must guard against excessive
capital inflows that could quickly be reversed. Capital flow surges planted the seeds of
three major currency crises in the 1990s—the European Exchange Rate Mechanism
(ERM) crisis in 1992–1993, the Mexican peso crisis in late 1994, and the Asian cur-
rency and financial crisis in 1997–1998. Each crisis episode was preceded by a surge
in capital inflows and a buildup of huge, highly leveraged speculative positions by
local as well as international investors in currencies that eventually came under heavy
speculative attack. In the run-up to the ERM crisis, investors—believing that European
yield convergence would occur as European monetary union approached—took on
highly leveraged long positions in the higher-yielding European currencies financed by
short positions in the lower-yielding European currencies. Likewise, in the run-up to
the Mexican peso crisis, investors and banks were highly leveraged and made exten-
sive use of derivative products in taking on speculative long Mexican peso/short US
dollar positions. And in the run-up to the Asian financial crisis, Asian companies and
banks were highly leveraged as they took on a huge volume of short-term dollar- and
yen-denominated debt to fund local activities. In each case, the sudden unwinding
of those leveraged long speculative positions triggered the attacks on the currencies.
Governments resist excessive inflows and currency bubbles by using capital con-
trols and direct intervention (selling their currency) in the foreign exchange market.
Capital controls can take many forms. In the Asian financial crisis, many countries,
such as Malaysia, prevented their banks from offering currency transactions in which
their currency was sold. As mentioned earlier, Brazil has used a tax to limit currency
transactions. In 2006, Thailand required a one-year, non-interest-bearing deposit of
30% of an investment’s value to reduce new foreign inflows, which had been appre-
ciating the Thai baht. Vietnam has limited the foreign ownership of local financial
institutions. In 2015, Ukraine was removed from the MSCI Frontier Markets equity
index after its central bank prevented foreign investors from repatriating funds from
the sale of Ukrainian stocks. By 2016, Venezuela had instituted capital controls in
the form of four different exchange rates, whereby the rate for selling Venezuelan
bolivars for US dollars depended on what the dollars were used for. As a result, many
Venezuelans used the black market to obtain dollars. Venezuela’s capital controls were
subsequently loosened in 2018 and 2019.
At one time, capital controls were frowned on as a policy tool for curbing undesired
surges in capital inflows. It was generally felt that such controls tended to generate
distortions in global trade and finance and that, in all likelihood, market participants
would eventually find ways to circumvent the controls. Furthermore, many thought
that capital controls imposed by one country could deflect capital flows to other

© CFA Institute. For candidate use only. Not for distribution.
58 Learning Module 1 Currency Exchange Rates: Understanding Equilibrium Value
countries, which could complicate monetary and exchange rate policies in those
economies. Despite such concerns, the IMF has said that the benefits associated
with capital controls may exceed the associated costs. Given the painful lessons that
EM policymakers have learned from previous episodes of capital flow surges, some
believe that under certain circumstances, capital controls may be needed to prevent
exchange rates from overshooting, asset bubbles from forming, and future financial
conditions from deteriorating.
Although a case can be made for government intervention and capital controls to
limit the potential damage associated with unrestricted inflows of overseas capital, the
key issue for policymakers is whether intervention and capital controls will actually
work in terms of (1) preventing currencies from appreciating too strongly, (2) reducing
the aggregate volume of capital inflows, and (3) enabling monetary authorities to pursue
independent monetary policies without having to worry about whether changes in
policy rates might attract too much capital from overseas. As an example of the last
issue, if a central bank increases interest rates to slow inflation, then capital controls
might prevent foreign capital inflows from subsequently depressing interest rates.
Evidence on the effectiveness of direct government intervention suggests that,
in the case of industrial countries, the volume of intervention is often quite small
relative to the average daily turnover of G–10 currencies in the foreign exchange
market. Hence, most studies have concluded that the effect of intervention in devel-
oped market economies is limited. For most developed market countries, the ratio of
official FX reserves held by the respective central banks to the average daily turnover
of foreign exchange trading in that currency is negligible. Most industrial countries
hold insufficient reserves to significantly affect the supply of and demand for their
currency. Note that if a central bank is intervening in an effort to weaken, rather
than strengthen, its own currency, it could (at least in principle) create and sell an
unlimited amount of its currency and accumulate a correspondingly large quantity of
FX reserves. However, persistent intervention in the FX market can undermine the
efficacy of domestic monetary policy.
The evidence on the effectiveness of government intervention in emerging market
currencies is more mixed. Intervention appears to contribute to lower EM exchange
rate volatility, but no statistically significant relationship has emerged between the
level of EM exchange rates and intervention. Some studies have found, however, that
EM policymakers might have greater success in controlling exchange rates than their
industrial country counterparts because the ratio of EM central bank FX reserve hold-
ings to average daily FX turnover in their domestic currencies is actually quite sizable.
With considerably greater firepower in their reserve arsenals, emerging market central
banks appear to be in a stronger position than their developed market counterparts
to influence the level and path of their exchange rates. What’s more, with emerging
market central banks’ FX reserve holdings expanding at a near-record clip in the past
decade, the effectiveness of intervention may be greater now than in the past.
15 WARNING SIGNS OF A CURRENCY CRISIS
describe warning signs of a currency crisis
If capital inflows come to a sudden stop, the result may be a financial crisis, in which
the economy contracts, asset values plummet, and the currency sharply depreciates.
History is filled with examples of currencies that have come under heavy selling pres-
sure within short windows of time. For example, between August 2008 and February

© CFA Institute. For candidate use only. Not for distribution.
Warning Signs of a Currency Crisis 59
2009, 23 currencies dropped by 25% or more against the US dollar. These included the
developed market currencies of Australia, Sweden, and the United Kingdom, which
dropped by 35% or more, and the emerging market currencies of Brazil, Russia, and
South Korea, which fell by more than 50%.
Currency crises often occur suddenly, with many investors caught by surprise.
Once a wave of selling begins, investors and borrowers must immediately reposition
their portfolios to avoid excessive capital losses. For example, assume a carry trader
had gone long the Brazilian real and borrowed US dollars. Upon an initial depreciation
of the real, the trader would be inclined to exit the trade by selling reals and buying
dollars. Or consider a Brazilian public or private borrower that had financed in US
dollars. The borrower would also be selling reals to buy dollars in order to cover future
repayment of the dollar debt. Either of these actions will intensify selling pressure on
the depreciated currency. It is this massive liquidation of vulnerable positions, often
reinforced by speculative offshore selling, that is largely responsible for the excessive
exchange rate movements that occur during currency crises.
Because most crisis episodes have not been adequately anticipated, a great deal
of effort has been spent developing early warning systems. One of the problems in
developing an early warning system is that views on the underlying causes of currency
crises differ greatly. One school of thought contends that currency crises tend to be
precipitated by deteriorating economic fundamentals, while a second school contends
that currency crises can occur out of the blue, with little evidence of deteriorating
fundamentals preceding them.
If, according to the first school of thought, deteriorating economic fundamentals
often precede crises and if those economic fundamentals tend to deteriorate steadily
and predictably, then it should be possible to construct an early warning system to
anticipate when a currency might be vulnerable.
The second school of thought argues that, although evidence of deteriorating
economic fundamentals might explain a relatively large number of currency collapses,
there might be cases in which economies with relatively sound fundamentals have their
currencies come under attack. Clearly, these currency crises would be more difficult to
predict. Events that are largely unrelated to domestic economic fundamentals include
sudden adverse shifts in market sentiment that become self-fulfilling prophecies and
contagion from crises in other markets. A crisis may spread to a country when, for
example, the country devalues its currency to keep its exports competitive with those
of another country that devalued.
Recognizing that no single model can correctly anticipate the onset of all crisis
episodes, an early warning system might nevertheless be useful in assisting investors
in structuring and/or hedging their global portfolios. An ideal early warning system
would need to incorporate a number of important features. First, it should have
a strong record of predicting actual crises but also should not issue false alarms.
Second, it should include macroeconomic indicators whose data are available on
a timely basis. If data arrive with a long lag, a crisis could be under way before the
early warning system starts flashing red. Third, because currency crises tend to be
triggered in countries with a number of economic problems, not just one, an ideal
early warning system should be broad based, incorporating a wide range of symptoms
that crisis-prone currencies might exhibit.
Many studies have been conducted to develop an early warning system for currency
crises, typically by constructing a model in which a number of variables constitute the
early warning system. Various definitions of currency crises have been used. Although
the variables and methodologies differ from one study to the next, the following con-
ditions were identified in one or more studies (Babecký, Havránek, Matějů, Rusnák,
Šmídková, and Vašíček 2013 and 2014; Daniels and VanHoose 2018):
1. Prior to a currency crisis, the capital markets have been liberalized to allow
the free flow of capital.

© CFA Institute. For candidate use only. Not for distribution.
60 Learning Module 1 Currency Exchange Rates: Understanding Equilibrium Value
2. There are large inflows of foreign capital (relative to GDP) in the period
leading up to a crisis, with short-term funding denominated in a foreign
currency being particularly problematic.
3. Currency crises are often preceded by (and often coincide with) banking
crises.
4. Countries with fixed or partially fixed exchange rates are more susceptible
to currency crises than countries with floating exchange rates.
5. Foreign exchange reserves tend to decline precipitously as a crisis
approaches.
6. In the period leading up to a crisis, the currency has risen substantially rela-
tive to its historical mean.
7. The ratio of exports to imports (known as “the terms of trade”) often deteri-
orates before a crisis.
8. Broad money growth and the ratio of M2 (a measure of money supply) to
bank reserves tend to rise prior to a crisis.
9. Inflation tends to be significantly higher in pre-crisis periods compared with
tranquil periods.
These factors are usually interrelated and often feed off one another. For example,
in the case of the first five factors, large inflows of foreign capital occur because the
financial markets have been liberalized and domestic banks have borrowed abroad. If
the borrowing is denominated in a foreign currency and the domestic currency initially
depreciates, the bank may have trouble servicing its debt, especially when the debt
is of shorter maturity. This scenario may cause foreign investors to withdraw capital
and speculators to short the currency, with their actions causing further declines in
the currency. If the government is trying to maintain the currency’s value, it could
increase interest rates to stem capital outflows or defend its currency using direct
intervention. The former action may worsen the banking industry’s condition and
slow down the economy. In the latter approach, the government will have to spend
down its foreign currency reserves to buy its own currency in the foreign exchange
markets. If the government appears unwilling or unable to defend its currency, then
capital outflows and speculative attacks will increase.
The fifth through seventh factors are related because an overvalued currency may
make the country’s exports less competitive. With fewer exports, the country is not
able to earn as much foreign currency. Other interrelationships occur because these
factors often coincide.
Models cannot predict every crisis, and they sometimes generate false alarms.
Nevertheless, an early warning system can be useful in assessing and preparing for
potential negative tail risks. As with any analytical tool, the implementation of an early
warning system requires integration with other analysis and judgment that cannot be
easily quantified or conceptualized.
ICELAND’S CURRENCY CRISIS OF 2008
Iceland, a country with a population of 320,000, had traditionally relied on the
fishing, energy, and aluminum industries for economic growth. That began to
change in 2001, when the banking industry was liberalized. Three banks domi-
nated the Icelandic banking industry: Glitnir, Kaupthing, and Landsbanki. Given
Iceland’s small population, these banks sought growth by offering short-term,
internet-based deposit accounts to foreign investors. These accounts offered
attractive interest rates and were denominated in foreign currencies. In partic-
ular, many of the depositors were British, Dutch, and other European citizens
who held deposit accounts denominated in pounds and euros.

© CFA Institute. For candidate use only. Not for distribution.
Warning Signs of a Currency Crisis 61
With government guarantees on their deposit accounts, the banking industry
grew rapidly. The largest bank, Kaupthing, experienced asset growth of 30 times
between 2000 and 2008. The three banks increased lending rapidly, with many
of their loans being long term, resulting in a maturity mismatch of assets and
liabilities. The banks’ assets were more than 14 times the country’s GDP, while
foreign debt was five times GDP. The three banks constituted more than 70%
of the national stock market capitalization.
The economy expanded at a real growth rate above 20% annually between
2002 and 2005, and many Icelanders left traditional industries to work in the
banks. Iceland earned the nickname “Nordic Tiger” as per capita GDP approached
USD 70,000 in 2007. The Icelandic krona increased in value against the US dollar
by 40% between 2001 and 2007. By 2007, the unemployment rate was less than
1%. Icelanders went on a shopping spree for consumer goods, in part by using
loans tied to the value of foreign currencies, motivated by lower interest rates
abroad. A 2002 trade surplus turned into a trade deficit in the years 2003–2007.
Iceland’s external debt in 2008 was more than 7 times its GDP and 14 times its
export revenue. Broad-based monetary aggregates grew at a rate of 14%–35%
annually from 2002 to 2007. By the fall of 2008, inflation had reached 14%.
As the global financial crisis unfolded in 2008, interbank lending declined
and Icelandic banks were unable to roll over their short-term debt. Anxious
foreign depositors began withdrawing their funds. In the first half of 2008, the
krona depreciated by more than 40% against the euro. As the Icelandic currency
declined in value, it became more difficult for the banks to meet depositors’
liquidity demands, while at the same time the banks’ depreciating krona-de-
nominated assets could not be used for collateral financing.
The three banks collapsed in 2008. Unfortunately for foreign depositors,
because of the relative size of the banks, the government guaranteed only
domestic deposits. Iceland’s central bank became technically insolvent, as its
EUR 2 billion in assets was dwarfed by Iceland’s debt to foreign banks of EUR
50 billion. Trading in the stock market was suspended in October 2008. When it
reopened several days later, the Icelandic Stock Market Index fell by more than
77% as a result of the elimination of the three banks’ equity value.
The government attempted to peg the krona to the euro in October 2008 but
abandoned the peg one day later. When trading in the currency was resumed
later that month, the currency value fell by more than 60% and trading was
eventually suspended. Iceland increased interest rates to 18% to stem outflows of
krona and imposed capital controls on the selling of krona for foreign currency.
The Icelandic economy contracted, and per capita GDP fell 9.2% in 2009. By
the spring of 2009, unemployment was 9%. The country subsequently required
a bailout from the IMF and its neighbors of USD 4.6 billion.
Source: Federal Reserve Bank of St. Louis database; Bekaert and Hodrick 2018; Matsangou 2015;
Daniels and VanHoose 2017.
EXAMPLE 11
Currency Crises
Monique Kwan now turns her attention to the likelihood of crises in various
emerging market currencies. She discusses this matter with a research associ-
ate, who tells her that the historical record of currency crises shows that most
of these episodes were not very well anticipated by investors (in terms of their

© CFA Institute. For candidate use only. Not for distribution.
62 Learning Module 1 Currency Exchange Rates: Understanding Equilibrium Value
positioning), by the bond markets (in terms of yield spreads between countries),
or by major credit rating agencies and economists (in terms of the sovereign
credit ratings and forecasts, respectively).
1. The research associate is most likely:
A. correct.
B. incorrect, because most credit rating agencies and economists typi-
cally change their forecasts prior to a crisis.
C. incorrect, because investor positioning and international yield differ-
entials typically shift prior to a crisis.
Solution
A is correct. Currency crises often catch most market participants and ana-
lysts by surprise.
2. Kwan delves further into the historical record of currency crises. She con-
cludes that even countries with relatively sound economic fundamentals
can fall victim to these crisis episodes and that these attacks can occur when
sentiment shifts for reasons unrelated to economic fundamentals.
Kwan’s conclusion is most likely:
A. correct.
B. incorrect, because there are few historical crises involving currencies
of countries with sound economic fundamentals.
C. incorrect, because there are few historical episodes in which a sudden
adverse shift in market sentiment occurs that is unrelated to economic
fundamentals.
Solution
A is correct. Even countries with sound economic fundamentals can be sub-
ject to a currency crisis, including instances when market sentiment shifts
for non-economic reasons.
3. To better advise the firm’s clients on the likelihood of currency crises, Kwan
tries to formulate an early warning system for these episodes. She recogniz-
es that a typical currency crisis tends to be triggered by a number of eco-
nomic problems, not just one.
Kwan’s early warning system is least likely to indicate an impending crisis
when there is:
A. an expansionary monetary policy.
B. an overly appreciated exchange rate.
C. a rising level of foreign exchange reserves at the central bank.
Solution
C is correct. A high level of foreign exchange reserves held by a country
typically decreases the likelihood of a currency crisis.
4. Kwan’s early warning system would most likely be better if it:
A. had a strong record of predicting actual crises, even if it generates a lot
of false signals.

© CFA Institute. For candidate use only. Not for distribution.
Warning Signs of a Currency Crisis 63
B. included a wide variety of economic indicators, including those for
which data are available only with a significant lag.
C. started flashing well in advance of an actual currency crisis to give
market participants time to adjust or hedge their portfolios before the
crisis hits.
Solution
C is correct. Early warnings are a positive factor in judging the effectiveness
of the system, whereas false signals and the use of lagged data would be
considered negative factors.
SUMMARY
Exchange rates are among the most difficult financial market prices to understand and
therefore to value. There is no simple, robust framework that investors can rely on in
assessing the appropriate level and likely movements of exchange rates.
Most economists believe that there is an equilibrium level or a path to that equilib-
rium value that a currency will gravitate toward in the long run. Although short- and
medium-term cyclical deviations from the long-run equilibrium path can be sizable
and persistent, fundamental forces should eventually drive the currency back toward
its long-run equilibrium path. Evidence suggests that misalignments tend to build up
gradually over time. As these misalignments build, they are likely to generate serious
economic imbalances that will eventually lead to correction of the underlying exchange
rate misalignment.
We have described how changes in monetary policy, fiscal policy, current account
trends, and capital flows affect exchange rate trends, as well as what role government
intervention and capital controls can play in counteracting potentially undesirable
exchange rate movements. We have made the following key points:
■ Spot exchange rates apply to trades for the next settlement date (usually T
+ 2) for a given currency pair. Forward exchange rates apply to trades to be
settled at any longer maturity.
■ Market makers quote bid and offer prices (in terms of the price currency) at
which they will buy or sell the base currency.
● The offer price is always higher than the bid price.
● The counterparty that asks for a two-sided price quote has the option
(but not the obligation) to deal at either the bid or offer price quoted.
● The bid–offer spread depends on (1) the currency pair involved, (2) the
time of day, (3) market volatility, (4) the transaction size, and (5) the rela-
tionship between the dealer and the client. Spreads are tightest in highly
liquid currency pairs, when the key market centers are open, and when
market volatility is relatively low.
■ Absence of arbitrage requires the following:
● The bid (offer) shown by a dealer in the interbank market cannot be
higher (lower) than the current interbank offer (bid) price.
● The cross-rate bids (offers) posted by a dealer must be lower (higher)
than the implied cross-rate offers (bids) available in the interbank mar-
ket. If they are not, then a triangular arbitrage opportunity arises.

© CFA Institute. For candidate use only. Not for distribution.
64 Learning Module 1 Currency Exchange Rates: Understanding Equilibrium Value
■ Forward exchange rates are quoted in terms of points to be added to the
spot exchange rate. If the points are positive (negative), the base currency
is trading at a forward premium (discount). The points are proportional to
the interest rate differential and approximately proportional to the time to
maturity.
■ International parity conditions show us how expected inflation, interest rate
differentials, forward exchange rates, and expected future spot exchange
rates are linked. In an ideal world,
● relative expected inflation rates should determine relative nominal inter-
est rates,
● relative interest rates should determine forward exchange rates, and
● forward exchange rates should correctly anticipate the path of the future
spot exchange rate.
■ International parity conditions tell us that countries with high (low)
expected inflation rates should see their currencies depreciate (appreciate)
over time, that high-yield currencies should depreciate relative to low-yield
currencies over time, and that forward exchange rates should function as
unbiased predictors of future spot exchange rates.
■ With the exception of covered interest rate parity, which is enforced by arbi-
trage, the key international parity conditions rarely hold in either the short
or medium term. However, the parity conditions tend to hold over relatively
long horizons.
■ According to the theory of covered interest rate parity, a
foreign-currency-denominated money market investment that is com-
pletely hedged against exchange rate risk in the forward market should yield
exactly the same return as an otherwise identical domestic money market
investment.
■ According to the theory of uncovered interest rate parity, the expected
change in a domestic currency’s value should be fully reflected
in domestic–foreign interest rate spreads. Hence, an unhedged
foreign-currency-denominated money market investment is expected to
yield the same return as an otherwise identical domestic money market
investment.
■ According to the ex ante purchasing power parity condition, expected
changes in exchange rates should equal the difference in expected national
inflation rates.
■ If both ex ante purchasing power parity and uncovered interest rate parity
held, real interest rates across all markets would be the same. This result is
real interest rate parity.
■ The international Fisher effect says that the nominal interest rate differential
between two currencies equals the difference between the expected inflation
rates. The international Fisher effect assumes that risk premiums are the
same throughout the world.
■ If both covered and uncovered interest rate parity held, then forward rate
parity would hold and the market would set the forward exchange rate equal
to the expected spot exchange rate: The forward exchange rate would serve
as an unbiased predictor of the future spot exchange rate.
■ Most studies have found that high-yield currencies do not depreciate and
low-yield currencies do not appreciate as much as yield spreads would sug-
gest over short to medium periods, thus violating the theory of uncovered
interest rate parity.

© CFA Institute. For candidate use only. Not for distribution.
Warning Signs of a Currency Crisis 65
■ Carry trades overweight high-yield currencies at the expense of low-yield
currencies. Historically, carry trades have generated attractive returns in
benign market conditions but tend to perform poorly (i.e., are subject to
crash risk) when market conditions are highly volatile.
■ According to a balance of payments approach, countries that run persistent
current account deficits will generally see their currencies weaken over time.
Similarly, countries that run persistent current account surpluses will tend
to see their currencies appreciate over time.
■ Large current account imbalances can persist for long periods of time before
they trigger an adjustment in exchange rates.
■ Greater financial integration of the world’s capital markets and greater free-
dom of capital to flow across national borders have increased the impor-
tance of global capital flows in determining exchange rates.
■ Countries that institute relatively tight monetary policies, introduce struc-
tural economic reforms, and lower budget deficits will often see their cur-
rencies strengthen over time as capital flows respond positively to relatively
high nominal interest rates, lower inflation expectations, a lower risk pre-
mium, and an upward revision in the market’s assessment of what exchange
rate level constitutes long-run fair value.
■ Monetary policy affects the exchange rate through a variety of channels. In
the Mundell–Fleming model, it does so primarily through the interest rate
sensitivity of capital flows, strengthening the currency when monetary pol-
icy is tightened and weakening it when monetary policy is eased. The more
sensitive capital flows are to the change in interest rates, the greater the
exchange rate’s responsiveness to the change in monetary policy.
■ In the monetary model of exchange rate determination, monetary policy is
deemed to have a direct impact on the actual and expected path of inflation,
which, via purchasing power parity, translates into a corresponding impact
on the exchange rate.
■ Countries that pursue overly easy monetary policies will see their currencies
depreciate over time.
■ In the Mundell–Fleming model, an expansionary fiscal policy typically
results in a rise in domestic interest rates and an increase in economic
activity. The rise in domestic interest rates should induce a capital inflow,
which is positive for the domestic currency, but the rise in economic activity
should contribute to a deterioration of the trade balance, which is negative
for the domestic currency. The more mobile capital flows are, the greater the
likelihood that the induced inflow of capital will dominate the deterioration
in trade.
■ Under conditions of high capital mobility, countries that simultaneously
pursue expansionary fiscal policies and relatively tight monetary policies
should see their currencies strengthen over time.
■ The portfolio balance model of exchange rate determination asserts that
increases in government debt resulting from a rising budget deficit will be
willingly held by investors only if they are compensated in the form of a
higher expected return. The higher expected return could come from (1)
higher interest rates and/or a higher risk premium, (2) depreciation of the
currency to a level sufficient to generate anticipation of gains from subse-
quent currency appreciation, or (3) some combination of the two.
■ Surges in capital inflows can fuel boom-like conditions, asset price bubbles,
and currency overvaluation.

© CFA Institute. For candidate use only. Not for distribution.
66 Learning Module 1 Currency Exchange Rates: Understanding Equilibrium Value
■ Many consider capital controls to be a legitimate part of a policymaker’s
toolkit. The IMF believes that capital controls may be needed to prevent
exchange rates from overshooting, asset price bubbles from forming, and
future financial conditions from deteriorating.
■ The evidence indicates that government policies have had a significant
impact on the course of exchange rates. Relative to developed countries,
emerging markets may have greater success in managing their exchange
rates because of their large foreign exchange reserve holdings, which appear
sizable relative to the limited turnover of FX transactions in many emerging
markets.
■ Although each currency crisis is distinct in some respects, the following
factors were identified in one or more studies:
1. Prior to a currency crisis, the capital markets have been liberalized to
allow the free flow of capital.
2. There are large inflows of foreign capital (relative to GDP) in the period
leading up to a crisis, with short-term funding denominated in a foreign
currency being particularly problematic.
3. Currency crises are often preceded by (and often coincide with) banking
crises.
4. Countries with fixed or partially fixed exchange rates are more suscepti-
ble to currency crises than countries with floating exchange rates.
5. Foreign exchange reserves tend to decline precipitously as a crisis
approaches.
6. In the period leading up to a crisis, the currency has risen substantially
relative to its historical mean.
7. The terms of trade (exports relative to imports) often deteriorate before
a crisis.
8. Broad money growth and the ratio of M2 (a measure of money supply)
to bank reserves tend to rise prior to a crisis.
9. Inflation tends to be significantly higher in pre-crisis periods compared
with tranquil periods.
16 APPENDIX
Currency Codes Used
USD US dollar
EUR euro
GBP UK pound
JPY Japanese yen
MXN Mexican peso
CHF Swiss franc
CAD Canadian dollar
SEK Swedish krona
AUD Australian dollar

© CFA Institute. For candidate use only. Not for distribution.
Appendix 67
KRW Korean won
NZD New Zealand dollar

© CFA Institute. For candidate use only. Not for distribution.
68 Learning Module 1 Currency Exchange Rates: Understanding Equilibrium Value
REFERENCES
Babecký, Jan, Tomáš Havránek, Jakub Matějů, Marek Rusnák, Kateřina Šmídková, and Bořek
Vašíček. 2013. “Leading Indicators of Crisis Incidence: Evidence from Developed Countries.”
Journal of International Money and Finance 35 (June): 1–19. 10.1016/j.jimonfin.2013.01.001
Babecký, Jan, Tomáš Havránek, Jakub Matějů, Marek Rusnák, Kateřina Šmídková, and Bořek
Vašíček. 2014. “Banking, Debt, and Currency Crises in Developed Countries: Stylized Facts
and Early Warning Indicators.” Journal of Financial Stability 15 (December): 1–17. 10.1016/j.
jfs.2014.07.001
Bekaert, Geert and Robert Hodrick. 2018. International Financial Management. 3rd ed.Cam-
bridge, UK: Cambridge University Press.
Daniels, Joseph P. and David D. VanHoose. 2017. Global Economic Issues and Policies. 4th
ed.London: Routledge.
Dimson, Elroy, Paul Marsh, Paul McGinnie, Mike Staunton, and Jonathan Wilmot. 2012. Credit
Suisse Global Investment Returns Yearbook 2012. Zurich: Credit Suisse Research Institute.
Dornbusch, Rudiger. 1976. “Expectations and Exchange Rate Dynamics.” Journal of Political
Economy 84 (6): 1161–76. 10.1086/260506
Matsangou, Elizabeth. 2015. “Failing Banks, Winning Economy: The Truth about Iceland’s
Recovery.” World Finance (15 September).
Rosenberg, Michael R. 1996. Currency Forecasting: A Guide to Fundamental and Technical
Models of Exchange Rate Determination. Chicago: Irwin Professional Publishing.
Rosenberg, Michael R. 2003. Exchange Rate Determination: Models and Strategies for Exchange
Rate Forecasting. New York: McGraw-Hill.

© CFA Institute. For candidate use only. Not for distribution.
Practice Problems 69
PRACTICE PROBLEMS
The following information relates to questions
1-5
Ed Smith is a new trainee in the foreign exchange (FX) services department of a
major global bank. Smith’s focus is to assist senior FX trader Feliz Mehmet, CFA.
Mehmet mentions that an Indian corporate client exporting to the United King-
dom wants to estimate the potential hedging cost for a sale closing in one year.
Smith is to determine the premium/discount for an annual (360-day) forward
contract using the exchange rate data presented in Exhibit 1.
Exhibit 1: Select Currency Data for GBP and INR
Spot (INR/GBP) 79.5093
Annual (360-day) MRR (GBP) 5.43%
Annual (360-day) MRR (INR) 7.52%
Mehmet is also looking at two possible trades to determine their profit potential.
The first trade involves a possible triangular arbitrage trade using the Swiss, US,
and Brazilian currencies, to be executed based on a dealer’s bid/offer rate quote
of 0.2355/0.2358 in CHF/BRL and the interbank spot rate quotes presented in
Exhibit 2.
Exhibit 2: Interbank Market Quotes
Currency Pair Bid/Offer
CHF/USD 0.9799/0.9801
BRL/USD 4.1699/4.1701
Mehmet is also considering a carry trade involving the USD and the EUR. He
anticipates it will generate a higher return than buying a one-year domestic note
at the current market quote due to low US interest rates and his predictions of
exchange rates in one year. To help Mehmet assess the carry trade, Smith pro-
vides Mehmet with selected current market data and his one-year forecasts in
Exhibit 3.
Exhibit 3: Spot Rates and Interest Rates for Proposed Carry Trade
Today’s One-Year Currency Pair (Price/ Spot Rate Projected Spot Rate
MRR Base) Today in One Year
USD 0.80% CAD/USD 1.3200 1.3151
CAD 1.71% EUR/CAD 0.6506 0.6567
EUR 2.20%

© CFA Institute. For candidate use only. Not for distribution.
70 Learning Module 1 Currency Exchange Rates: Understanding Equilibrium Value
Finally, Mehmet asks Smith to assist with a trade involving a US multinational
customer operating in Europe and Japan. The customer is a very cost-conscious
industrial company with an AA credit rating and strives to execute its currency
trades at the most favorable bid–offer spread. Because its Japanese subsidiary is
about to close on a major European acquisition in three business days, the client
wants to lock in a trade involving the Japanese yen and the euro as early as possi-
ble the next morning, preferably by 8:05 a.m. New York time.
At lunch, Smith and other FX trainees discuss how best to analyze currency mar-
ket volatility from ongoing financial crises. The group agrees that a theoretical
explanation of exchange rate movements, such as the framework of the interna-
tional parity conditions, should be applicable across all trading environments.
They note such analysis should enable traders to anticipate future spot exchange
rates. But they disagree on which parity condition best predicts exchange rates,
voicing several different assessments. Smith concludes the discussion on parity
conditions by stating to the trainees,
I believe that in the current environment both covered and uncovered interest
rate parity conditions are in effect.
1. Based on Exhibit 1, the forward premium (discount) for a 360-day INR/GBP
forward contract is closest to:
A. –1.546.
B. 1.546.
C. 1.576.
2. Based on Exhibit 2, the most appropriate recommendation regarding the triangu-
lar arbitrage trade is to:
A. decline the trade, because no arbitrage profits are possible.
B. execute the trade, buy BRL in the interbank market, and sell BRL to the
dealer.
C. execute the trade, buy BRL from the dealer, and sell BRL in the interbank
market.
3. Based on Exhibit 3, the potential all-in USD return on the carry trade is closest to:
A. 0.83%.
B. 1.23%.
C. 1.63%.
4. The factor least likely to lead to a narrow bid–offer spread for the industrial com-
pany’s needed currency trade is the:
A. timing of its trade.
B. company’s credit rating.
C. pair of currencies involved.
5. If Smith’s statement on parity conditions is correct, future spot exchange rates are
most likely to be forecast by:
A. current spot rates.

© CFA Institute. For candidate use only. Not for distribution.
Practice Problems 71
B. forward exchange rates.
C. inflation rate differentials.
The following information relates to questions
6-13
Anna Goldsworthy is the chief financial officer of a manufacturing firm head-
quartered in the United Kingdom. She is responsible for overseeing exposure to
price risk in both the commodity and currency markets. Goldsworthy is settling
her end-of-quarter transactions and creating reports. Her intern, Scott Under-
wood, assists her in this process.
The firm hedges input costs using forward contracts that are priced in US dollars
(USD) and Mexican pesos (MXN). Processed goods are packaged for sale under
licensing agreements with firms in foreign markets. Goldsworthy is expecting to
receive a customer payment of JPY 225,000,000 (Japanese yen) that she wants to
convert to pounds sterling (GBP). Underwood gathers the exchange rates from
Dealer A in Exhibit 1.
Exhibit 1: Dealer A’s Spot Exchange Rates
Spot Exchange Rates
Currency Pair (Price/Base) Bid Offer Midpoint
JPY/GBP 129.65 129.69 129.67
MXN/USD 20.140 20.160 20.150
GBP/EUR 0.9467 0.9471 0.9469
USD/EUR 1.1648 1.1652 1.1650
USD/GBP 1.2301 1.2305 1.2303
The firm must also buy USD to pay a major supplier. Goldsworthy calls Deal-
er A with specific details of the transaction and asks to verify the USD/GBP
quote. Dealer A calls her back later with a revised USD/GBP bid–offer quote of
1.2299/1.2307.
Goldsworthy must purchase MXN 27,000,000 to pay an invoice at the end of the
quarter. In addition to the quotes from Dealer A, Underwood contacts Dealer
B, who provides a bid–offer price of GBP/MXN 0.0403/0.0406. To check wheth-
er the dealer quotes are reflective of an efficient market, Underwood examines
whether the prices allow for an arbitrage profit.
In three months, the firm will receive EUR 5,000,000 from another customer. Six
months ago, the firm sold EUR 5,000,000 against the GBP using a nine-month
forward contract at an all-in price of GBP/EUR 0.9526. To mark the position to
market, Underwood collects the GBP/EUR forward rates in Exhibit 2.

© CFA Institute. For candidate use only. Not for distribution.
72 Learning Module 1 Currency Exchange Rates: Understanding Equilibrium Value
Exhibit 2: GBP/EUR Forward Rates
Maturity Forward Points
One month 4.40/4.55
Three months 14.0/15.0
Six months 29.0/30.0
Goldsworthy also asks for the current 90-day MRRs for the major currencies.
Selected three-month MRRs (annualized) are shown in Exhibit 3. Goldsworthy
studies Exhibit 3 and says, “We have the spot rate and the 90-day forward rate for
GBP/EUR. As long as we have the GBP 90-day MRR, we will be able to calculate
the implied EUR 90-day MRR.”
Exhibit 3: 90-Day MRR
Currency Annualized Rate
GBP 0.5800%
JPY 0.0893%
USD 0.3300%
After reading a draft report, Underwood notes, “We do not hedge the incoming
Japanese yen cash flow. Your report asks for a forecast of the JPY/GBP exchange
rate in 90 days. We know the JPY/GBP spot exchange rate.” He asks, “Does the
information we have collected tell us what the JPY/GBP exchange rate will be in
90 days?”
Goldsworthy replies, “The JPY/GBP exchange rate in 90 days would be a valuable
piece of information to know. An international parity condition can be used to
provide an estimate of the future spot rate.”
6. Using the quotes in Exhibit 1, the amount received by Goldsworthy from con-
verting JPY 225,000,000 will be closest to:
A. GBP 1,734,906.
B. GBP 1,735,174.
C. GBP 1,735,442.
7. Using Exhibit 1, which of the following would be the best reason for the revised
USD/GBP dealer quote of 1.2299/1.2307?
A. A request for a much larger transaction
B. A drop in volatility in the USD/GBP market
C. A request to trade when both New York and London trading centers are
open
8. Using the quotes from Dealer A and B, the triangular arbitrage profit on a trans-
action of MXN 27,000,000 would be closest to:
A. GBP 0.
B. GBP 5,400.

© CFA Institute. For candidate use only. Not for distribution.
Practice Problems 73
C. GBP 10,800.
9. Based on Exhibits 1, 2, and 3, the mark-to-market gain for Goldsworthy’s forward
position is closest to:
A. GBP 19,971.
B. GBP 20,500.
C. GBP 21,968.
10. Based on Exhibit 2, Underwood should conclude that three-month EUR MRR is:
A. below three-month GBP MRR.
B. equal to three-month GBP MRR.
C. above three-month GBP MRR.
11. Based on the exchange rate midpoint in Exhibit 1 and the rates in Exhibit 3, the
90-day forward premium (discount) for the USD/GBP would be closest to:
A. –0.0040.
B. –0.0010.
C. +0.0010.
12. Using Exhibits 1, 2, and 3, which international parity condition would Goldswor-
thy most likely use to calculate the EUR MRR?
A. Real interest rate parity
B. Covered interest rate parity
C. Uncovered interest rate parity
13. The international parity condition Goldsworthy will use to provide the estimate
of the future JPY/GBP spot rate is most likely:
A. covered interest rate parity.
B. uncovered interest rate parity.
C. relative purchasing power parity.
The following information relates to questions
14-20
Connor Wagener, a student at the University of Canterbury in New Zealand, has
been asked to prepare a presentation on foreign exchange rates for his interna-
tional business course. Wagener has a basic understanding of exchange rates
but would like a practitioner’s perspective, and he has arranged an interview
with currency trader Hannah McFadden. During the interview, Wagener asks
McFadden,
Could you explain what drives exchange rates? I’m curious as to why our New

© CFA Institute. For candidate use only. Not for distribution.
74 Learning Module 1 Currency Exchange Rates: Understanding Equilibrium Value
Zealand dollar was affected by the European debt crisis in 2011 and what other
factors impact it.
In response, McFadden begins with a general discussion of exchange rates. She
notes that international parity conditions illustrate how exchange rates are linked
to expected inflation, interest rate differences, and forward exchange rates as
well as current and expected future spot rates. McFadden makes the following
statement:
Statement 1: “Fortunately, the international parity condition most relevant for
FX carry trades does not always hold.”
McFadden continues her discussion:
FX carry traders go long (i.e., buy) high-yield currencies and fund their position
by shorting—that is, borrowing in—low-yield currencies. Unfortunately, crashes
in currency values can occur which create financial crises as traders unwind their
positions. For example, in 2008, the New Zealand dollar was negatively impact-
ed when highly leveraged carry trades were unwound. In addition to investors,
consumers and business owners can also affect currency exchange rates through
their impact on their country’s balance of payments. For example, if New Zealand
consumers purchase more goods from China than New Zealand businesses sell
to China, New Zealand will run a trade account deficit with China.
McFadden further explains,
Statement 2: “A trade surplus will tend to cause the currency of the country in
surplus to appreciate, while a deficit will cause currency depreciation. Exchange
rate changes will result in immediate adjustments in the prices of traded goods as
well as in the demand for imports and exports. These changes will immediately
correct the trade imbalance.”
McFadden next addresses the influence of monetary and fiscal policy on ex-
change rates:
Countries also exert significant influence on exchange rates both through the
initial mix of their fiscal and monetary policies and by subsequent adjustments to
those policies. Various models have been developed to identify how these policies
affect exchange rates. The Mundell–Fleming model addresses how changes in
both fiscal and monetary policies affect interest rates and ultimately exchange
rates in the short term.
McFadden describes monetary models by stating,
Statement 3: “Monetary models of exchange rate determination focus on the
effects of inflation, price level changes, and risk premium adjustments.”
McFadden continues her discussion:
So far, we’ve touched on balance of payments and monetary policy. The portfolio
balance model addresses the impacts of sustained fiscal policy on exchange rates.
I must take a client call but will return shortly. In the meantime, here is some
relevant literature on the models I mentioned along with a couple of questions
for you to consider:
Question 1: Assume an emerging market (EM) country has restrictive monetary
and fiscal policies under low capital mobility conditions. Are these policies likely
to lead to currency appreciation or currency depreciation or to have no impact?
Question 2: Assume a developed market (DM) country has an expansive fiscal
policy under high capital mobility conditions. Why is its currency most likely to
depreciate in the long run under an integrated Mundell–Fleming and portfolio
balance approach?
Upon her return, Wagener and McFadden review the questions. McFadden
notes that capital flows can have a significant impact on exchange rates and have
contributed to currency crises in both EM and DM countries. She explains that
central banks, such as the Reserve Bank of New Zealand, use FX market inter-

© CFA Institute. For candidate use only. Not for distribution.
Practice Problems 75
vention as a tool to manage exchange rates. McFadden states,
Statement 4: “Some studies have found that EM central banks tend to be more
effective in using exchange rate intervention than DM central banks, primarily
because of one important factor.”
McFadden continues her discussion:
Statement 5: “I mentioned that capital inflows could cause a currency crisis,
leaving fund managers with significant losses. In the period leading up to a cur-
rency crisis, I would predict that an affected country’s:
Prediction 1: foreign exchange reserves will increase.
Prediction 2: broad money growth will increase.
Prediction 3: exchange rate will be substantially higher than its mean level
during tranquil periods.”
After the interview, McFadden agrees to meet the following week to discuss more
recent events on the New Zealand dollar.
14. The international parity condition McFadden is referring to in Statement 1 is:
A. purchasing power parity.
B. covered interest rate parity.
C. uncovered interest rate parity.
15. In Statement 2, McFadden is most likely failing to consider the:
A. initial gap between the country’s imports and exports.
B. effect of an initial trade deficit on a country’s exchange rates.
C. lag in the response of import and export demand to price changes.
16. The least appropriate factor used to describe the type of models mentioned in
Statement 3 is:
A. inflation.
B. price level changes.
C. risk premium adjustments.
17. The best response to Question 1 is that the policies will:
A. have no impact.
B. lead to currency appreciation.
C. lead to currency depreciation.
18. The most likely response to Question 2 is a(n):
A. increase in the price level.
B. decrease in risk premiums.
C. increase in government debt.
19. The factor that McFadden is most likely referring to in Statement 4 is:
A. FX reserve levels.

© CFA Institute. For candidate use only. Not for distribution.
76 Learning Module 1 Currency Exchange Rates: Understanding Equilibrium Value
B. domestic demand.
C. the level of capital flows.
20. Which of McFadden’s predictions in Statement 5 is least likely to be correct?
A. Prediction 1
B. Prediction 2
C. Prediction 3

© CFA Institute. For candidate use only. Not for distribution.
Solutions 77
SOLUTIONS
1. C is correct. The equation to calculate the forward premium (discount) is:
_Actual
_[ 360 ]
F − S = S i − i .
f/d f/d f/d _Actual (f d)
(1 + i )
d[ 360 ]
S is the spot rate with GBP the base currency or d and INR the foreign curren-
f/d
cy or f. S per Exhibit 1 is 79.5093, i is equal to 7.52%, and i is equal to 5.43%.
f/d f d
With GBP as the base currency (i.e., the “domestic” currency) in the INR/GBP
quote, substituting in the relevant base currency values from Exhibit 1 yields the
following:
_360
_____[3_6_0_]____
F − S = 79.5093 (0.0752 − 0.0543) .
f/d f/d _360
(1 + 0.0543 )
[360]
_1
F − S = 79.5093 (0.0752 − 0.0543) .
f/d f/d (1.0543)
F − S = 1.576.
f/d f/d
2. B is correct. The dealer is posting a bid rate to buy BRL at a price that is too high.
This overpricing is determined by calculating the interbank implied cross rate for
the CHF/BRL using the intuitive equation-based approach:
CHF/BRL = CHF/USD × (BRL/USD)–1, or
CHF/BRL = CHF/USD × USD/BRL.
Inverting the BRL/USD given the quotes in Exhibit 2 determines the USD/BRL
bid–offer rates of 0.23980/0.23982. (The bid of 0.23980 is the inverse of the BRL/
USD offer, calculated as 1/4.1702; the offer of 0.23982 is the inverse of the BRL/
USD bid, calculated as 1/4.1698.) Multiplying the CHF/USD and USD/BRL bid–
offer rates then leads to the interbank implied CHF/BRL cross rate:
Bid: 0.9799 × 0.23980 = 0.2349.
Offer: 0.9801 × 0.23982 = 0.23505.
Since the dealer is willing to buy BRL at 0.2355 but BRL can be purchased from
the interbank market at 0.23505, there is an arbitrage opportunity to buy BRL in
the interbank market and sell BRL to the dealer for a profit of 0.0045 CHF (0.2355
– 0.23505) per BRL transacted.
3. A is correct. The carry trade involves borrowing in a lower-yielding currency to
invest in a higher-yielding one and netting any profit after allowing for borrow-
ing costs and exchange rate movements. The relevant trade is to borrow USD
and lend in EUR. To calculate the all-in USD return from a one-year EUR MRR
deposit, first determine the current and one-year-later USD/EUR exchange rates.
Because one USD buys CAD 1.3200 today and one CAD buys EUR 0.6506 today,
today’s EUR/USD rate is the product of these two numbers: 1.3200 × 0.6506 =
0.8588. The projected rate one year later is 1.3151 × 0.6567 = 0.8636. Accordingly,
measured in dollars, the investment return for the unhedged EUR MRR deposit
is equal to

© CFA Institute. For candidate use only. Not for distribution.
78 Learning Module 1 Currency Exchange Rates: Understanding Equilibrium Value
(1.3200 × 0.6506) × (1 + 0.022) × [1/(1.3151 × 0.6567)] – 1
= 0.8588 × (1.022)(1/0.8636) – 1 = 1.01632 – 1
= 1.632%.
However, the borrowing costs must be charged against this gross return to fund
the carry trade investment (one-year USD MRR was 0.80%). The net return on
the carry trade is therefore 1.632% – 0.80% = 0.832%.
4. B is correct. While credit ratings can affect spreads, the trade involves spot
settlement (i.e., two business days after the trade date), so the spread quoted to
this highly rated (AA) firm is not likely to be much tighter than the spread that
would be quoted to a somewhat lower-rated (but still high-quality) firm. The
relationship between the bank and the client, the size of the trade, the time of day
the trade is initiated, the currencies involved, and the level of market volatility are
likely to be more significant factors in determining the spread for this trade.
5. B is correct. By rearranging the terms of the equation defining covered interest
rate parity and assuming that uncovered interest rate parity is in effect, the
forward exchange rate is equal to the expected future spot exchange rate—F =
f/d
e
S —with the expected percentage change in the spot rate equal to the interest
f/d
rate differential. Thus, the forward exchange rate is an unbiased forecast of the
future spot exchange rate.
6. A is correct. Goldsworthy has been given a bid–offer spread. Because she is
buying the base currency—in this case, GBP—she must pay the offer price of JPY
129.69 per GBP.
_JP_Y_ _2_2_5,_0_0_0,_0_0_0
= GBP 1,734,906.
129.69 JPY/GBP
7. A is correct. Posted quotes are typically for transactions in 1 million units of the
base currency. Larger transactions may be harder for the dealer to sell in the in-
terbank market and would likely require the dealer to quote a wider spread (lower
bid price and higher offer price).
8. A is correct. Using quotes from Dealer A, she can find
_MXN _MXN _USD
= × .
GBP USD GBP
The bid from Dealer A for MXN/GBP is effectively
_MXN _MXN _USD
= ×
(GBP)
b id
(US D)
bid
( G BP)
bid
= 20.140 × 1.2301 = 24.7742.
The offer from Dealer A is
_MXN _MXN _USD
= ×
(GBP)
o ffer
(US D)
offer
( GBP)
offe r
= 20.160 × 1.2305 = 24.8069.
To compare with Dealer B’s quote, she must take the inverse of MXN/GBP, so she
has an offer to sell MXN at a rate of 1/24.7742 = GBP 0.0404 and a bid to pur-
chase MXN at a rate of 1/24.8069 = GBP 0.0403. Dealer A is effectively quoting
GBP/MXN at 0.0403/0.0404. Although she can effectively buy MXN more cheap-
ly from Dealer A (GBP 0.0404 from Dealer A, versus GBP 0.0406 from Dealer B),
she cannot resell them to Dealer B for a higher price than GBP 0.0403. There is
no profit from triangular arbitrage.
9. A is correct. Marking her nine-month contract to market six months later

© CFA Institute. For candidate use only. Not for distribution.
Solutions 79
requires buying GBP/EUR three months forward. The GBP/EUR spot rate
is 0.9467/0.9471, and the three-month forward points are 14.0/15.0. The
three-month forward rate to use is 0.9471 + (15/10000) = 0.9486. Goldswor-
thy sold EUR 5,000,000 at 0.9526 and bought at 0.9486. The net cash flow at
the settlement date will equal EUR 5,000,000 × (0.9526 – 0.9486) GBP/EUR =
GBP 20,000. This cash flow will occur in three months, so we discount at the
three-month GBP MRR of 58 bps:
__G__B_P_ 2_0_,0_0_0__
= GBP 19,971.04.
_90
1 + 0.0058
(360)
10. A is correct. The positive forward points for the GBP/EUR pair shown in Exhibit
2 indicate that the EUR trades at a forward premium at all maturities, including
three months. Covered interest rate parity,
_Actual
1 + i
_f[ 360 ]
F = S ,
f/d f/d _Actual
(1 + i )
d[ 360 ]
suggests a forward rate greater than the spot rate requires a non-domestic
risk-free rate (in this case, the GBP MRR) greater than the domestic risk-free rate
(EUR MRR). When covered interest rate parity is violated, traders can step in and
conduct arbitrage.
11. B is correct. Using covered interest rate parity, the forward rate is
_Actual
1 + i
_f[ 360 ]
F = S
f/d f/d _Actual
(1 + i )
d[ 360 ]
_90
1 + 0.0033
________[_3_6_0_]
= 1.2303 = 1.2295.
_90
(1 + 0.0058 )
[360]
Because the domestic MRR is higher than the non-domestic MRR, the forward
rate will be less than the spot rate, giving a forward discount of
F − S = 1.2295 − 1.2303 = − 0.0008.
f/d f/d
12. B is correct. The covered interest rate parity condition,
_Actual
1 + i
_f[ 360 ]
F = S , (Equation 1)
f/d f/d _Actual
(1 + i )
d[ 360 ]
specifies the forward exchange rate that must hold to prevent arbitrage given the
spot exchange rate and the risk-free rates in both countries. If the forward and
spot exchange rates, as well as one of the risk-free rates, are known, the other
risk-free rate can be calculated.
13. B is correct. According to uncovered interest rate parity,
%Δ S e = i − i , (Equation 2)
f/d f d
the expected change in the spot exchange rate should reflect the interest rate
spread between the two countries, which can be found in Exhibit 3. Given the
spot exchange rate (from Exhibit 1) and the expected future change, she should
be able to estimate the future spot exchange rate.
14. C is correct. The carry trade strategy is dependent on the fact that uncovered in-
terest rate parity does not hold in the short or medium term. If uncovered inter-
est rate parity held, it would mean that investors would receive identical returns

© CFA Institute. For candidate use only. Not for distribution.
80 Learning Module 1 Currency Exchange Rates: Understanding Equilibrium Value
from either an unhedged foreign currency investment or a domestic currency
investment because the appreciation/depreciation of the exchange rate would
offset the yield differential. However, during periods of low volatility, evidence
shows that high-yield currencies do not depreciate enough and low-yield curren-
cies do not appreciate enough to offset the yield differential.
15. C is correct. McFadden states that exchange rates will immediately correct
the trade imbalance. She is describing the flow supply/demand channel, which
assumes that trade imbalances will be corrected as the deficit country’s currency
depreciates, causing its exports to become more competitive and its imports to
become more expensive. Studies indicate that there can be long lags between
exchange rate changes, changes in the prices of traded goods, and changes in
the trade balance. In the short run, exchange rates tend to be more responsive to
investment and financing decisions.
16. C is correct. Risk premiums are more closely associated with the portfolio bal-
ance approach. The portfolio balance approach addresses the impact of a coun-
try’s net foreign asset/liability position. Under the portfolio balance approach,
investors are assumed to hold a diversified portfolio of assets including foreign
and domestic bonds. Investors will hold a country’s bonds as long as they are
compensated appropriately. Compensation may come in the form of higher inter-
est rates and/or higher risk premiums.
17. B is correct. The currency is likely to appreciate. The emerging market country
has both a restrictive monetary policy and a restrictive fiscal policy under con-
ditions of low capital mobility. Low capital mobility indicates that interest rate
changes induced by monetary and fiscal policy will not cause large changes in
capital flows. Implementation of restrictive policies should result in an improve-
ment in the trade balance, which will result in currency appreciation.
18. C is correct. Expansionary fiscal policies result in currency depreciation in the
long run. Under a portfolio balance approach, the assumption is that investors
hold a mix of domestic and foreign assets including bonds. Fiscal stimulus poli-
cies result in budget deficits, which are often financed by debt. As the debt level
rises, investors become concerned as to how the ongoing deficit will be financed.
The country’s central bank may need to create more money in order to purchase
the debt, which would cause the currency to depreciate. Or the government
could adopt a more restrictive fiscal policy, which would also depreciate the
currency.
19. A is correct. EM countries are better able to influence their exchange rates
because their reserve levels as a ratio of average daily FX turnover are generally
much greater than those of DM countries. This means that EM central banks
are in a better position to affect currency supply and demand than DM coun-
tries, where the ratio is negligible. EM policymakers use their foreign exchange
reserves as a kind of insurance to defend their currencies, as needed.
20. A is correct. Prediction 1 is least likely to be correct. Foreign exchange reserves
tend to decline precipitously, not increase, as a currency crisis approaches. Broad
money growth tends to rise in the period leading up to a currency crisis, and the
exchange rate is substantially higher than its mean level during tranquil periods.