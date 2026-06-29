© CFA Institute. For candidate use only. Not for distribution.
L E A R N I N G M O D U L E
8
Exchange Rate Calculations
LEARNING OUTCOMES
Mastery The candidate should be able to:
calculate and interpret currency cross-rates
explain the arbitrage relationship between spot and forward
exchange rates and interest rates, calculate a forward rate using
points or in percentage terms, and interpret a forward discount or
premium
INTRODUCTION 1
The foreign exchange market facilitates international currency and trade flows, and it
is important to understand how currency exchange rates are calculated. Market par-
ticipants can also derive cross-rates to expand trading opportunities by determining
quotes for currencies not directly traded. Understanding the concept of arbitrage
relationships in the foreign exchange market provides a basis for understanding the
interrelationships between four key market inputs. Global entities trade currencies for
a wide variety of purposes and understanding the relationships between the market
factors affecting spot and forward rates is crucial. These interactions are reinforced
by the calculations in the second lesson.
LEARNING MODULE OVERVIEW
■ An exchange rate between two currencies that are not
expressly quoted on the market is known as a cross-rate and
can be calculated using conventional currency quotes.
■ Three conventional currency market quotes can be used with one
inversion to calculate a cross-rate.
■ Discrepancies in exchange rates can create arbitrage opportunities but
they are rare due to market efficiencies.
■ The premium of a forward exchange rate over a spot rate is quoted in
terms of forward points, which are also called swap points.
■ Forward rates are directly proportional to currency spot rates, the
interest rate differential, and the maturity of the forward contract.

© CFA Institute. For candidate use only. Not for distribution.
254 Learning Module 8 Exchange Rate Calculations
■ As a result of the interrelationship among these four variables, any
variable can be calculated by using the other three as inputs.
2 CROSS-RATE CALCULATIONS
calculate and interpret currency cross-rates
Global currencies are bought, sold, and exchanged in the foreign exchange (FX)
market. In this decentralized market, participants trade currencies utilizing exchange
rates, which typically reflect an efficient market. This section will cover the use of
cross exchange rate relationships (cross-rates) to calculate exchange rates between
two currencies using a third currency. It also will introduce calculations used in the
FX market to trade currencies.
Given two exchange rates involving three currencies, it is possible to back out the
cross-rate. For example, as we have seen in a prior lesson, the FX market convention
is to quote the exchange rate between the US dollar and the euro as euro–dollar
(USD/EUR). The FX market also quotes the exchange rate between the Canadian
dollar and US dollar as dollar–Canada (CAD/USD). Given these two exchange rates,
it is possible to back out the cross-rate between the euro and the Canadian dollar,
which according to market convention is quoted as euro–Canada (CAD/EUR). This
calculation is shown as follows:
_CAD _USD _CAD _ USD _CAD
× = × = .
USD EUR USD EUR EUR
Hence, to get a euro–Canada (CAD/EUR) quote, we must multiply the dollar–Canada
(CAD/USD) quote by the euro–dollar (USD/EUR) quote. For example, assume the
exchange rate for dollar–Canada is 1.3020 and the exchange rate for euro–dollar is
1.1701. Using these spot exchange rates, the euro–Canada cross-rate equals:
1.3020 × 1.1701 = 1.5235 CAD per EUR.
The professional FX market does not use the convention of direct or indirect quotes
because these conventions depend on one’s location to determine the domestic ver-
sus foreign currencies. Instead, the market uses rate quotes on defined conventional
currency pairs. Sometimes, to get a cross-rate using several currency quotes, it is
necessary to invert a quote to get an intermediary currency that can be canceled out
in the equation to obtain the cross-rate. For example, to get a Canada–yen (JPY/CAD)
quote, one typically uses the dollar–Canada (CAD/USD) rate and dollar–yen (JPY/
USD) rate, which are the market conventions. This Canada–yen calculation requires
that the dollar–Canada rate (CAD/USD) be inverted to a Canada–dollar (USD/CAD)
quote for the calculations to work, as follows:
−1
_CAD _JPY _USD _JPY _ USD _JPY _JPY
× = × = × = .
(USD) USD CAD USD CAD USD CAD
Hence, to get a Canada–yen (JPY/CAD) quote, we must first invert the dollar–Canada
(CAD/USD) quote before multiplying by the dollar–yen (JPY/USD) quote. Market
quotes for most currencies are quoted to four decimal places; however, the Japanese
yen exchange rate is quoted to two decimal places. For example, assume that we have
spot exchange rates of 1.3020 for dollar–Canada (CAD/USD) and 111.94 for dollar–yen
(JPY/USD). The dollar–Canada rate of 1.3020 inverts to 0.7680; multiplying this value
by the dollar–yen quote of 111.94 gives the following Canada–yen quote:

© CFA Institute. For candidate use only. Not for distribution.
Cross-Rate Calculations 255
0.7680 × 111.94 = 85.97 JPY per CAD.
Market participants asking for a quote in a cross-rate currency pair typically will not
need to do this calculation themselves: Either the dealer or the electronic trading
platform will provide a quote in the specified currency pair. (For example, a client
asking for a quote in Canada–yen will receive that quote from the dealer; he will not
be given separate dollar–Canada and dollar–yen quotes to do the calculation.) Dealers
providing the quotes often have to do this calculation themselves if only because the
dollar–Canada and dollar–yen currency pairs often trade on different trading desks
and involve different traders. Electronic dealing machines used in both the interbank
market and bank-to-client markets often provide this mathematical operation to
calculate cross-rates automatically.
Because market participants can receive both a cross-rate quote (e.g., Canada–yen)
as well as the component underlying exchange rate quotes (e.g., dollar–Canada and
dollar–yen), these cross-rate quotes must be consistent with the previous equation;
otherwise, the market will arbitrage the mispricing. Extending our example, we cal-
culate a Canada–yen (JPY/CAD) rate of 85.97 based on underlying dollar–Canada
(CAD/USD) and dollar–yen (JPY/USD) rates of 1.3020 and 111.94, respectively. Now
suppose that at the same time a misguided dealer quotes a Canada–yen rate of 86.20.
This is a different price in Canada–yen for an identical service—that is, converting
yen into Canadian dollars. Hence, any trader could buy CAD1 at the lower price of
JPY85.97and then turn around and sell CAD1 at JPY86.20 (recall our earlier discussion
of how price and base currencies are defined). The riskless arbitrage profit is JPY0.23
per CAD1. The arbitrage—called triangular arbitrage (we use “tri-” because it involves
three currencies—would continue until the price discrepancy was removed.
In reality, however, these discrepancies in cross-rates rarely occur because both
human traders and automatic trading algorithms are constantly on alert for any pric-
ing inefficiencies. In practice, and for the purposes of this lesson, we can consider
cross-rates as being consistent with their underlying exchange rate quotes and can
assume that given any two exchange rates involving three currencies, we can back
out the third cross-rate.
EXAMPLE 1
Cross-Rates and Percentage Changes
A research report produced by a dealer includes the following spot rate quotes:
Expected Spot Rate in One
Currency Spot Rate Year
USD/EUR 1.1701 1.1619
CHF/USD 0.9900 0.9866
USD/GBP 1.3118 1.3066
1. The spot CHF/EUR cross-rate is closest to:
A. 0.8461.
B. 0.8546.
C. 1.1584.
Solution:
C is correct:
_CHF _USD _CHF
= × = 1.1701 × 0.9900 = 1.1584
EUR EUR USD

© CFA Institute. For candidate use only. Not for distribution.
256 Learning Module 8 Exchange Rate Calculations
2. The spot GBP/EUR cross-rate is closest to:
A. 0.8920.
B. 1.1211.
C. 1.4653.
Solution:
A is correct:
−1
_GBP _USD _USD _USD _GBP _1.1701
= × = × = = 0.8920
EUR EUR (GBP) EUR USD 1.3118
3. Based on the research report, the euro is expected to appreciate by how
much against the US dollar over the next year?
A. –0.7 percent
B. +0.7 percent
C. +1.0 percent
Solution:
A is correct. The euro is the base currency in the USD/EUR quote, and
the expected decrease in the USD/EUR rate indicates that the euro is
depreciating. In one year, it will cost less, in US dollars, to buy one euro.
Mathematically:
_1.1619
− 1 = − 0.7%
1.1701
4. Based on the research report, how much is the US dollar expected to appre-
ciate against the British pound sterling over the next year?
A. +0.6 percent
B. –0.4 percent
C. +0.4 percent
Solution:
C is correct. The British pound is the base currency in the USD/GBP
quote, and the expected decrease in the USD/GBP rate means that the
British pound is expected to depreciate against the US dollar. Or equiva-
lently, the US dollar is expected to appreciate against the British pound.
Mathematically:
−1
_1.3066 _1.3118
− 1 = − 1 = + 0.4%
(1.3118) 1.3066
5. Over the next year, the Swiss franc is expected to:
A. depreciate against the British pound.
B. depreciate against the euro.
C. appreciate against the British pound, euro, and US dollar.
Solution:
C is correct: Because the question does not require calculating the magni-
tude of the appreciation or depreciation, we can use the Swiss franc as either
the price currency or the base currency. In this case, it is easier to use the
Swiss franc as the price currency. CHF/USD is expected to decline from
0.9900 to 0.9866, so the Swiss franc is expected to be stronger (i.e., it should
appreciate against the US dollar). CHF/EUR is currently 1.1584 (see the

© CFA Institute. For candidate use only. Not for distribution.
Cross-Rate Calculations 257
solution to problem 1) and is expected to be 1.1463 (= 0.9866 × 1.1619), so
the Swiss franc is expected to appreciate against the euro. CHF/GBP is cur-
rently 1.2987 (= 0.9900 × 1.3118) and is expected to be 1.2891 (= 0.9866 ×
1.3066), so the Swiss franc is also expected to appreciate against the British
pound.
Alternatively, we can derive this answer intuitively. According to the
research report, the CHF/USD rate is expected to decline: That is, the US
dollar is expected to depreciate against the Swiss franc, or alternatively, the
Swiss franc is expected to appreciate against the US dollar. The USD/EUR
and USD/GBP rates are also decreasing, meaning that the euro and British
pound are expected to depreciate against the US dollar, or alternatively, the
US dollar is expected to appreciate against the euro and British pound. If
the Swiss franc is expected to appreciate against the US dollar and the US
dollar is expected to appreciate against both the euro and British pound, it
follows that the Swiss franc is expected to appreciate against both the euro
and British pound.
6. Based on the research report, which of the following lists the three curren-
cies from strongest to weakest over the next year?
A. US dollar, British pound, euro
B. US dollar, euro, British pound
C. Euro, US dollar, British pound
Solution:
A is correct. USD/EUR is expected to decline from 1.1701 to 1.1619, while
USD/GBP is expected to decline from 1.3118 to 1.3066. So, the US dollar is
expected to be stronger than both the euro and British pound. GBP/EUR
is currently 0.8920 [= (1.3118)–1 × 1.1701] and is expected to be 0.8893 [=
(1.3066)–1 × 1.1619], so the British pound is expected to be stronger than
the euro.
7. Based on the research report, which of the following lists the three curren-
cies in order of appreciating the most to appreciating the least (in percent-
age terms) against the US dollar over the next year?
A. British pound, Swiss franc, euro
B. Swiss franc, British pound, euro
C. Euro, Swiss franc, British pound
Solution:
B is correct. The USD/EUR rate depreciates by –0.7 percent (=
[1.1619/1.1701] – 1), which is the depreciation of the base currency
euro against the US dollar. The USD/GBP rate declines –0.4 percent (=
[1.3066/1.3118] – 1), which is the depreciation of the British pound against
the US dollar. Inverting the CHF/USD rate to a USD/CHF convention shows
that the base currency Swiss franc appreciates by +0.35 percent against the
US dollar (= [1.0136/1.0101] – 1).

© CFA Institute. For candidate use only. Not for distribution.
258 Learning Module 8 Exchange Rate Calculations
3 FORWARD RATE CALCULATIONS
explain the arbitrage relationship between spot and forward
exchange rates and interest rates, calculate a forward rate using
points or in percentage terms, and interpret a forward discount or
premium
This lesson continues the previous discussion of the FX market by considering the
interactions between spot and forward rates, interest rates, and maturities, which
exist because of arbitrage relationships. The relationships among these four factors
are maintained because of market efficiencies, and any one factor can be determined
using the other three as inputs. In addition, this lesson covers the methods of calcu-
lating forward rates in point and percentage terms as well as forward discounts and
premiums for these rate relationships.
In professional FX markets, forward exchange rates typically are quoted in terms
of points (also sometimes referred to as “pips”). The points on a forward rate quote are
simply the difference between the forward exchange rate quote and the spot exchange
rate quote, with the points scaled so that they can be related to the last decimal in the
spot quote. When the forward rate is higher than the spot rate, the points are positive
and the base currency is said to be trading at a forward premium. Conversely, if the
forward rate is less than the spot rate, the points (forward rate minus spot rate) are
negative and the base currency is said to be trading at a forward discount. Of course, if
the base currency is trading at a forward premium, then the price currency is trading
at a forward discount, and vice versa.
This can best be explained by means of an example. Assume the spot euro–dollar
exchange rate (USD/EUR) is 1.15885 and the one-year forward rate is 1.19532. Hence,
the forward rate is trading at a premium to the spot rate (the forward rate is larger
than the spot rate) and the one-year forward points are quoted as +364.7. This +364.7
comes from the following calculation:
1.19532 – 1.15885 = +0.03647.
Recall that most non-yen exchange rates are quoted to four decimal places. In this
case, we would scale up by four decimal places (multiply by 10,000) so that this
+0.03647 would be represented as +364.7 points. Notice that the points are scaled to
the size of the last digit in the spot exchange rate quote—usually the fourth decimal
place. Notice as well that points typically are quoted to one (or more) decimal places,
meaning that the forward rate will typically be quoted to five or more decimal places.
The exception among the major currencies is the yen, which is typically quoted to
two decimal places for spot rates. Here, forward points are scaled up by two decimal
places—the last digit in the spot rate quote—by multiplying the difference between
forward and spot rates by 100.
Typically, quotes for forward rates are shown as the number of forward points at
each maturity, the time between spot settlement and the settlement of the forward
contract. These forward points are also called swap points because an FX swap con-
sists of simultaneous spot and forward transactions. In our example, a trader would
have faced a spot rate and forward points in the euro–dollar (USD/EUR) currency
pair similar to those in Exhibit 1,

© CFA Institute. For candidate use only. Not for distribution.
Forward Rate Calculations 259
Exhibit 1: Sample Spot and Forward Quotes
Maturity Spot Rate or Forward Points
Spot 1.15885
One week +5.6
One month +27.1
Three months +80.9
Six months +175.6
Twelve months +364.7
Notice that the absolute number of points generally increases with maturity. This is
because the number of points is proportional to the yield differential between the
two countries (the Eurozone and the United States, in this case) scaled by the term to
maturity. Given the interest rate differential, the longer the term to maturity, the greater
the absolute number of forward points. Similarly, given the term to maturity, a wider
interest rate differential implies a greater absolute number of forward points. (This
relationship will be explained and demonstrated in more detail later in this lesson.)
To convert any of these quoted forward points into a forward rate, one would
divide the number of points by 10,000 (to scale down to the fourth decimal place,
the last decimal place in the spot quote) and then add the result to the spot exchange
rate quote. (As mentioned previously, exchange rates for the Japanese yen, such as
the JPY/USD exchange rate, are quoted to two decimal places only, so forward points
for the dollar–yen currency pair are divided by 100.) For example, using the data in
Exhibit 1 for USD/EUR, the three-month forward rate in this case would be as follows:
_+ 80.9
1.15885 + = 1.15885 + 0.00809 = 1.16694 .
(10, 000)
Occasionally, one will see the forward rate or forward points represented as a percentage
of the spot rate rather than as an absolute number of points. Continuing the previous
example, the three-month forward rate for USD/EUR can be represented as follows:
_1_.1_5_8_8_5_ +_ 0_._0_0_8_09_ _1.16694
− 1 = − 1 = + 0.698% .
1.15885 (1.15885)
This shows that either the forward rate or the forward points can be used to calculate
the percentage discount (or premium) in the forward market—in this case, +0.698
percent rounding to three decimal places. To convert a spot quote into a forward
quote when the points are shown as a percentage, one simply multiplies the spot rate
by one plus the percentage premium or discount:
1.15885 × (1 + 0.698%) = 1.15885 × (1.0000 + 0.00698) ≈ 1.16694.
Note that, rounded to the fifth decimal place, this is equal to our previous calculation.
However, it is typically the case in professional FX markets that forward rates will be
quoted in terms of pips rather than percentages.
Arbitrage Relationships
We now turn to the interaction between spot rates, forward rates, and interest rates
and how their relationship is derived. Forward exchange rates are based on an arbi-
trage relationship that equates the investment return on two alternative but equivalent
investments. Consider the case of an investor with funds to invest. For simplicity, we
will assume that one unit of the investor’s domestic currency will be invested for one
period. One alternative is to invest for one period at the domestic risk-free rate (r );
d
at the end of the period, the amount of funds held is equal to (1 + r ). An alternative
d

© CFA Institute. For candidate use only. Not for distribution.
260 Learning Module 8 Exchange Rate Calculations
investment is to convert this one unit of domestic currency to foreign currency using
the spot rate of S (number of units of foreign currency per one unit of domestic
f/d
currency). This can be invested for one period at the foreign risk-free rate; at the end of
the period, the investor would have S (1 + r ) units of foreign currency. These funds
f/d f
must then be converted back to the investor’s domestic currency. If the exchange rate
to be used for this end-of-period conversion was pre-contracted at the start of the
period (i.e., a forward rate was used), it would eliminate any FX risk from converting
at a future, unknown spot rate. Given the assumed exchange rate convention (foreign/
domestic), the investor would obtain (1/F ) units of the domestic currency for each
f/d
unit of foreign currency sold forward. Note that this process of converting domestic
funds in the spot FX market, investing at the foreign risk-free rate, and then converting
back to the domestic currency with a forward rate is termed “swap financing.”
Hence, we have two alternative investments—both are risk free because both are
invested at risk-free interest rates and because any FX risk was eliminated (hedged)
by using a forward rate. Because these two investments are equal in risk character-
istics, they must have the same return. Bearing in mind that the currency quoting
convention is the number of foreign currency units per single domestic unit (f/d), this
relationship can be stated as follows:
_1
(1 + r ) = S 1 + r .
d f/d( f)( F f /d )
This is an arbitrage relationship because it describes two alternative investments
(one on either side of the equal sign) that should have equal returns. If they do not, a
riskless arbitrage opportunity exists because an investor can sell short the investment
with the lower return and invest the funds in the investment with the higher return;
the difference between the two returns is pure profit. It is because of this arbitrage
relationship that the all-in financing rate using swap financing is close to the domestic
interest rate.
This formula is perhaps the easiest and most intuitive way to remember the formula
for the forward rate because this formula is based directly on the underlying intuition
(the arbitrage relationship of two alternative but equivalent investments, one on either
side of the equal sign). Also, the right-hand side of the equation, for the hedged foreign
investment alternative, is arranged in proper time sequence: (1) convert domestic to
foreign currency; then (2) invest the foreign currency at the foreign interest rate; and
finally (3) convert the foreign currency back to the domestic currency. Recall that this
equation is based on an f/d exchange rate quoting convention. If the exchange rate
data were presented in d/f form, one could either invert these quotes back to f/d form
and use the previous equation or use the following equivalent equation:
(1 + r ) = (1/S )(1 + r)F .
d d/f f d/f
If this latter equation were used, remember that forward and spot exchange rates are
now being quoted on a d/f convention.
This arbitrage equation can be rearranged as needs require. For example, to get
the formula for the forward rate, the previous equation can be restated as follows:
1 + r
_f
F = S .
f/d f/d(1 + r )
d
Given the spot exchange rate and the domestic and foreign risk-free interest rates, the
forward rate is the value that completes this equation and eliminates any arbitrage
opportunity. For example, let’s assume that the spot exchange rate (S ) is 1.6535, the
f/d
domestic 12-month risk-free rate is 3.50 percent, and the foreign 12-month risk-free
rate is 5.00 percent. The 12-month forward rate (F ) must then be equal to:
f/d
_1.0500
1.6535 = 1.6775 .
(1.0350)

© CFA Institute. For candidate use only. Not for distribution.
Forward Rate Calculations 261
Suppose instead that, with the spot exchange rate and interest rates unchanged, you
were given a quote on the 12-month forward rate (F ) of 1.6900. Because this mis-
f/d
quoted forward rate does not agree with the arbitrage equation, it would present a
riskless arbitrage opportunity. This can be calculated by using the arbitrage equation
to compute the return on the two alternative investment strategies. The return on the
domestic-only investment approach is the domestic risk-free rate (3.50 percent). In
contrast, the return on the hedged foreign investment when this misquoted forward
rate is put into the arbitrage equation equals:
_1 _1
S 1 + r = 1.6535( 1.05) = 1.0273 .
f/d( f)( F f /d ) (1.6900)
This results in a return of 2.73 percent. Hence, the investor could make riskless
arbitrage profits by borrowing at the higher foreign risk-free rate, selling the foreign
currency at the spot exchange rate, hedging the currency exposure (buying the for-
eign currency back) at the misquoted forward rate, investing the funds at the lower
domestic risk-free rate, and thereby getting a profit of 77 basis points (3.50% – 2.73%)
for each unit of domestic currency involved—all with no upfront commitment of the
investor’s own capital. Any such opportunity in real-world financial markets would be
quickly “arbed” away. In this example, the investor actually borrows at the higher of
the two interest rates but makes a profit because the foreign currency is underpriced
in the forward market.
The underlying arbitrage equation can also be rearranged to show the forward
rate as a percentage of the spot rate:
F 1 + r
_f/d _f
= .
S (1 + r )
f/d d
This shows that, given an f/d quoting convention, the forward rate will be higher than
(be at a premium to) the spot rate if foreign interest rates are higher than domestic
interest rates. More generally, and regardless of the quoting convention, the currency
with the higher (lower) interest rate will always trade at a discount (premium) in the
forward market.
One context in which forward rates are quoted as a percentage of spot rates occurs
when forward rates are interpreted as expected future spot rates, as follows:
F = S .
t t+1
Substituting this expression into the previous equation and doing some rearranging
leads to the following:
_ S t + 1 − 1 = %Δ S = _ r f − r d .
S t+1 (1 + r )
t d
This shows that if forward rates are interpreted as expected future spot rates, the
expected percentage change in the spot rate is proportional to the interest rate dif-
ferential (r – r ).
f d
It is intuitively appealing to see forward rates as expected future spot rates. However,
this interpretation of forward rates should be used cautiously. The direction of the
expected change in spot rates is somewhat counterintuitive. All else being equal, an
increase in domestic interest rates (e.g., the central bank tightens monetary policy)
would typically be expected to lead to an increase in the value of the domestic currency.
In contrast, the previous equation indicates that, all else equal, a higher domestic inter-
est rate implies slower expected appreciation (or greater expected depreciation) of the
domestic currency (recall that this equation is based on an f/d quoting convention).
More important, historical data show that forward rates are poor predictors of
future spot rates. Although various econometric studies suggest that forward rates may
be unbiased predictors of future spot rates (i.e., they do not systematically over- or
under-estimate future spot rates), this is not particularly useful information because

© CFA Institute. For candidate use only. Not for distribution.
262 Learning Module 8 Exchange Rate Calculations
the margin of error for these forecasts is so large. As mentioned in the Introduction,
the FX market is far too complex and dynamic to be captured by a single variable,
such as the level of the yield differential between countries. Moreover, according to the
formula for the forward rate, forward rates are based on domestic and foreign interest
rates. This means that anything that affects the level and shape of the yield curve in
either the domestic or foreign market will also affect the relationship between spot
and forward exchange rates. In other words, FX markets do not operate in isolation
but rather reflect almost all factors affecting other markets globally; anything that
affects expectations or risk premia in these other markets will reverberate in forward
exchange rates as well. Although the level of the yield differential is one factor that
the market may look at in forming spot exchange rate expectations, it is only one of
many factors. (Many traders look to the trend in the yield differential rather than the
level of the differential.) Moreover, a lot of noise in FX markets makes almost any
model—no matter how complex—a relatively poor predictor of spot rates at any given
point in the future. In practice, FX traders and market strategists do not base either
their currency expectations or trading strategies solely on forward rates.
For the purposes of this lesson, it is best to understand forward exchange rates
simply as a product of the arbitrage equation outlined earlier and forward points as
being related to the (time-scaled) interest rate differential between the two countries.
Reading any more than that into forward rates or interpreting them as the “market
forecast” can be potentially misleading.
Forward Discounts and Premiums
We now continue our discussion of forward discounts and premiums based on spot
and interest rates and add the impact of maturity. To understand the relationship
between maturity and forward points, we need to generalize our arbitrage formula
slightly. Suppose the investment horizon is a fraction, τ, of the period for which
the interest rates are quoted. Then the interest earned in the domestic and foreign
markets would be (r τ) and (r τ), respectively. Substituting this into our arbitrage
d f
relationship and solving for the difference between the forward and spot exchange
rates gives the following:
r − r
_f d
F − S = S τ .
f/d f/d f/d(1 + r τ)
d
This equation shows that forward points (appropriately scaled) are proportional to
the spot exchange rate and to the interest rate differential and approximately (but not
exactly) proportional to the horizon of the forward contract.
For example, suppose that we wanted to determine the 30-day forward exchange
rate given a 30-day domestic risk-free interest rate of 2.00 percent per year, a 30-day
foreign risk-free interest rate of 3.00 percent per year, and a spot exchange rate (S )
f/d
of 1.6555. The risk-free assets used in this arbitrage relationship are typically bank
deposits quoted using the London Interbank Offered Rate (Libor) for the currencies
involved. The day count convention for Libor deposits is actual/360. Incorporating
the fractional period (τ) and inserting the data into the forward rate equation leads
to the following 30-day forward rate:
_30
1 + r τ 1 + 0.0300
_f ________[_3_6_0_]
F = S = 1.6555 = 1.6569 .
f/d f/d(1 + r
d
τ)
(1 + 0.0200
_30
)
[360]
This means that, for a 30-day term, forward rates are trading at a premium of 14 pips
(1.6569 – 1.6555). This can also be calculated using the previous formula for swap
points:
r − r
_f d _0_.0_3_0_0_ −_ 0_._0_2_00_ _30
F − S = S τ = 1.6555 = 0.0014 .
f/d f/d f/d(1 + r d τ) (1 + 0.0200 [ _ 3 3 6 0 0 ] ) [360]

© CFA Institute. For candidate use only. Not for distribution.
Forward Rate Calculations 263
As should be clear from this expression, the absolute number of swap points will be
closely related to the term of the forward contract (i.e., approximately proportional to τ
= actual/360). For example, leaving the spot exchange rate and interest rates unchanged,
and setting the term of the forward contract to 180 days, we obtain the following:
_0_.0_3_0_0_ −_ 0_._0_2_00_ _180
F − S = 1.6555 = 0.0082 .
f/d f/d _180 [360]
(1 + 0.0200 [ 360 ] )
This leads to the forward rate trading at a premium of 82 pips. The increase in the
number of forward points is approximately proportional to the increase in the term
of the contract (from 30 days to 180 days). Note that although the term of the 180-day
forward contract is six times longer than that of a 30-day contract, the number of
forward points is not exactly six times larger: 6 × 14 = 84.
Similarly, the number of forward points is proportional to the spread between
foreign and domestic interest rates (r – r ). For example, with reference to the original
f d
30-day forward contract, let’s set the foreign interest rate to 4.00 percent leaving the
domestic interest rate and spot exchange rate unchanged. This doubles the interest
rate differential (r – r ) from 1.00 percent to 2.00 percent; it also doubles the forward
f d
points (rounding to four decimal places), as follows:
_0_.0_4_0_0_ −_ 0_._0_2_00_ _30
F − S = 1.6555 = 0.0028 .
f/d f/d _30 [360]
(1 + 0.0200 [ 360 ] )
EXAMPLE 2
Forward Rate Calculations
A French company recently finalized a sale of goods to a UK-based client and
expects to receive a payment of GBP50 million in 32 days. The corporate trea-
surer at the French company wants to hedge the FX risk of this transaction and
receives the following exchange rate information from a dealer:
GBP/EUR spot rate 0.8752
One-month forward points –1.4
1. According to the exchange rate information, the treasurer could hedge the
FX risk by:
A. buying euro (selling British pounds) at a forward rate of 0.87380.
B. buying euro (selling British pounds) at a forward rate of 0.87506.
C. selling euro (buying British pounds) at a forward rate of 0.87506.
Solution:
B is correct. The French company would want to convert the British pound
to its domestic currency, the euro (it wants to sell British pounds and
buy euros). The forward rate would be equal to: 0.8752 + (–1.4/10,000) =
0.87506.
2. According to the exchange rate information, the best interpretation of the
forward discount shown is that:
A. the euro is expected to depreciate over the next 30 days.
B. one-month UK interest rates are higher than those in the Eurozone.

© CFA Institute. For candidate use only. Not for distribution.
264 Learning Module 8 Exchange Rate Calculations
C. one-month Eurozone interest rates are higher than those in the United
Kingdom.
Solution:
C is correct. A forward discount indicates that interest rates in the base
currency country (France, in this case, which uses the euro) are higher than
those in the price currency country (the United Kingdom).
3. According to the exchange rate information, if the 12-month forward rate is
0.87295 GBP/EUR, then the 12-month forward points are closest to:
A. –22.5.
B. –2.25.
C. –0.00225.
Solution:
A is correct. The number of forward points is equal to the scaled difference
between the forward rate and the spot rate. In this case: 0.87295 – 0.87520
= –0.00225. This is then multiplied by 10,000 to convert to the number of
forward points.
4. If a second dealer quotes GBP/EUR at a 12-month forward discount of 0.30
percent on the same spot rate, the French company could:
A. trade with either dealer because the 12-month forward quotes are
equivalent.
B. lock in a profit in 12 months by buying euros from the second dealer
and selling it to the original dealer.
C. lock in a profit in 12 months by buying euros from the original dealer
and selling it to the second dealer.
Solution:
B is correct. A 0.30 percent discount means that the second dealer will sell
euros 12 months forward at 0.8752 × (1 – 0.0030) = 0.87257, a lower price
per euro than the original dealer’s quote of 0.87295. Buying euros at the
cheaper 12-month forward rate (0.87257) and selling the same amount of
euros 12 months forward at the higher 12-month forward rate (0.87295)
means a profit of (0.87295 – 0.87257 = GBP0.00038) per euro transacted,
receivable when both forward contracts settle in 12 months.
5. If the 270-day Libor rates (annualized) for the euro and British pound
are 1.370 percent and 1.325 percent, respectively, and the spot GBP/EUR
exchange rate is 0.8489, then the number of forward points for a 270-day
forward rate (F ) is closest to:
GBP/EUR
A. –22.8.
B. –3.8.
C. –2.8.
Solution:
C is correct, because the forward rate is calculated as:

© CFA Institute. For candidate use only. Not for distribution.
Forward Rate Calculations 265
_Actual _270
1 + r 1 + 0.01325
____G_B_P_[__36_0__] _________[_3_6_0_]
F _GBP = S _GBP = 0.8489 = 0.84862 .
EUR EUR (1 + r _ Actua l ) (1 + 0.01370 _270 )
EUR[ 360 ] [360]
This shows that the forward points are at a discount of: 0.84862 – 0.84890
= –0.00028, or –2.8 points. This can also be seen using the swap points
formula:
_0_.0_1_3_2_5_ −_ 0_._0_1_3_70_ _270
F _G EU BP R − S _ E G U B R P = 0.8489 ( 1 + 0.013 70 [ _2 3 7 6 0 0 ] ) [ 360 ] = − 0.00028 .
The calculation of –3.8 points omits the day count (270/360), and –22.8
points gets the scaling wrong.