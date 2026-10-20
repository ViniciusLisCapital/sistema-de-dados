12
CHAPTER
How to Trade FX: The Framework
FX is a famously difficult asset class to trade as the link to the global business cycle
can be very tenuous. One reason is that FX is explicitly a relative price, and there-
fore, it is not enough to trade it in line with a view on accelerating or decelerating
global growth. Changes in relative growth differentials between countries are more
important, and it is generally harder to have a strong view on relative performance
than on the overall direction. Secondly, FX is traded by many different actors and for
many different reasons. Pursuing profits in FX trading is only one of the objectives of
market participants, as many other FX flows occur as a result of the normal business
of exporting or importing goods, or due to corporate hedging needs. This means that
flows can be less predictable, which makes FX a more frustrating asset class than most.
It is no coincidence that there are very few FX dedicated funds with a good long-term
record, which is different from bond, equity, or credit funds. It also means that there is a
cottage industry of consultants that aim to suss out FX flows. “Technical” analysts are
also most often found in FX space, given how poorly fundamentals are linked to FX
price action. However, a less clearly defined link to fundamentals does not stop lever-
aged funds from trading FX aggressively in the pursuit of alpha. The attraction is a
combination of cheap and plentiful leverage and low transaction costs, both of which
mean that FX lends itself well to short-term trading strategies. And alpha opportuni-
ties do present themselves. In this chapter, we share some frameworks that we found
helpful in the pursuit of FX alpha. For FX frameworks that are slightly more focused
on shorter time horizons, also see the excellent book by Donnelly (2019).
12.1 USD SMILE, SMIRK, OR CLOUD?
A popular framework for the USD is the USD smile, originally developed by Stephen
Jen. The framework explains the nonlinear relationship between the USD and the
growth of the US economy. The idea is that the USD tends to strengthen in two extreme
economic scenarios: when the US economy is performing exceptionally well or when
it is going into recession. The USD strength of the first type is driven by rising interest
rate differentials, while the USD strength of the second type is driven by risk aversion.
A trading model for the USD, therefore, needs to include both business cycle measures
to capture the USD strength that is correlated with strong US economic performance,
but also needs to include a risk aversion measure to capture the other side of the USD
smile. The “smile” is illustrated in Figure 12.1, which shows monthly DXY returns
269

270 TRADING GLOBAL MACRO MARKETS
15.0%
10.0%
5.0%
0.0%
–5.0%
–10.0%
35 40 45 50
PMI level
nruter
YXD
DXY vs. PMI since 1990
55 60 65
FIGURE 12.1 The USD smile is more of a smirk.
Source: Bloomberg and authors’ calculations.
dependent on the manufacturing PMI. For PMIs below 45, a weak USD is very rare.
The other side of the smile is not as pronounced, though. While the single largest PMI
print was associated with USD strength, the hit ratio of long USDs when the PMI is
above 60 is not good. It is therefore not fully surprising that most charts on the inter-
net that try to illustrate the famous USD smile rely on a schematic illustration rather
than on empirical data. Using GDP instead of PMIs, or US PMIs relative to the rest of
the world, or using the change of growth, or using quarterly returns, does not improve
results. We prefer the term USD smirk, but uncharitable commentators would proba-
bly call it the USD cloud. For almost all PMI outcomes, anything is possible in terms
of USD returns.
The more visible left-hand side of the USD smirk across currencies is illustrated
in Figure 12.2. The x-axis shows the average correlation of various currencies with
the SPX and the y-axis is the average one-month implied yield. A positive correlation
means that the currency in question appreciates with SPX strength. Data are from 2002
to 2024. The chart shows that there is usually a negative correlation between carry
and the correlation to the SPX. High carry currencies are typically vulnerable to SPX
pull-backs. The USD (here approximated by DXY) is the key currency not fitting this
pattern, as it typically has positive carry but is negatively correlated with the SPX. This
has made it an attractive hedge in the past, as other currencies that benefit during risk
aversion are typically negative carry. This is especially the case for the JPY, but also for
CHF. Of the remaining G10 currencies, the EUR came closest to having no significant
beta to risk aversion.
However, we also note that this pattern is not ironclad, as can be seen in
Figure 12.3. First of all, it was not really the case for long periods during the 1990s.
Furthermore, in the aftermath of the bursting US equity market bubble in 2001 and
2002, there were plenty of months where a weaker SPX coincided with a weaker USD.

How to Trade FX: The Framework 271
NZD
AUD
NOK
GBP
USD CAD
SEK
EUR
CHF
JPY
–0.3 –0.2 –0.1 0.0 0.1
Correlation to S&P500
dleiy
deilpmI
3.5%
3.0%
2.5%
2.0%
1.5%
1.0%
0.5%
0.0%
0.2 0.3 0.4 0.5
FIGURE 12.2 USD likes risk aversion.
Source: Bloomberg and authors’ calculations.
0.4
0.2
0.0
–0.2
–0.4
–0.6
DXY Correlation to S&P Equity
1980 1985 1990 1995 2000 2005 2010 2015 2020 2025
Start Date
FIGURE 12.3 USD usually negatively correlated to equities—but not always.
Source: Bloomberg and authors’ calculations.
The same has been playing out in early 2025 after “liberation day.” Both were periods
when the prevailing narrative of US exceptionalism was under pressure, which led to
a broad selling of US assets, including the USD.
Next, we investigate how to make the left-hand side of the “USD smirk” tradable.
When focusing on EUR, the risk aversion component is best measured by European
measures of risk aversion. There are two candidates. We can either use the spread of

272 TRADING GLOBAL MACRO MARKETS
BTP - Bunds EUR Rel Equity EUR Carry adj.
Return 3.82% 4.55% 0.16%
3.0
Volatility 9.12% 9.12% 9.13%
Risk/Reward 0.42 0.50 0.02
Max DD –20.62% –28.78% –45.26%
2.5
2.0
BTP - Bunds
1.5
EUR Rel Equity
1.0 EUR Carry adj.
2005 2010 2015 2020 2025
FIGURE 12.4 USD likes US equity outperformance.
Source: Bloomberg and authors’ calculations.
peripheral bonds against bunds. As a shortcut, we can take the spreads of BTPs against
Bunds, as Italy has been the country most consistently exposed to fiscal concerns and
therefore has seen spreads most closely correlate with VIX and other measures of risk
aversion. Trading the EUR in line with whether Italian spreads are below or above the
55dma creates significant alpha. Interestingly, this is not only true during the European
crisis in 2011 and 2012, but also more generally, likely because the spread captures
more general risk aversion, i.e., the right side of the USD smile.
An alternative version would be to use the relative equity performance of the
United States over Europe. This will not so much pick up risk aversion, per se, but
will pick up European-centric risk aversion, given that European equities will strongly
underperform in such a scenario. Furthermore, it also picks up periods when strong
US equity outperformance gives rise to large capital inflows into the United States, or
the subsequent unwind of such flows. We implement this rule by using the Eurostoxx
over the MSCI US, in local terms, and take our usual 55dma to generate a signal
(with a two-day lag, to account for the timezone differences). We find that this signal
works better than the risk aversion signal based on BTP-Bund spreads, as shown in
Figure 12.4. But overall information ratios are relatively modest, at around 0.5.
12.2 THE USD AND THE BUSINESS CYCLE
As just laid out, the link of the USD to US growth on the right-hand side of the smirk,
i.e., the strong US business cycle, is less clear-cut, or at least not as simple as just
observing US growth momentum. Having said that, the business cycle is very important
for the USD. Given that FX is about relative business cycles, we start the discussion
with a focus on relative data momentum. We focus on EURUSD, which is the main
component of the DXY index and has the advantage that we can more easily analyze

How to Trade FX: The Framework 273
relative data momentum than if we were trying to explain DXY. But we also discuss the
trade-weighted USD. We start our discussion with Citi’s data change indices (CECID)
for the United States and the Eurozone. Those indices essentially score new US data
releases against the levels of the previous 12 months. For a detailed description, see
Noual (2014), and for other interesting use cases, see Kasikov (2018). The trading
rule we are going to investigate is to go long EUR whenever the relative data change
index crosses above the zero line, i.e., when data changes in the Eurozone are stronger
than in the United States, and vice versa. Interestingly, rules based on the data change
indexes generally work better than rules based on the data surprise indexes (CESI,
which measure data releases against the Bloomberg consensus), even though the data
surprise indexes are moving faster and are oftentimes leading CECID. The results are
illustrated in Figure 12.5a for DXY and Figure 12.5b for EUR. The information ratio
DXY and US - RoW Spreads
CESI > 0 CESI > 0 CESI < 0 CESI < 0
∣ CECID > 0 ∣ CECID < 0 ∣ CECID > 0 ∣ CECID < 0
Return 1.44% –0.69% 1.11% –0.96%
1.4 Volatility 4.21% 3.29% 3.29% 4.25%
Risk/Reward 0.34 –0.21 0.34 –0.22
Max DD –13.26% –22.97% –9.43% –29.21%
1.3
Active IR 0.63 –0.47 0.84 –0.41
% on 29.18% 19.91% 16.23% 30.69%
1.2
1.1 CESI > 0 ∣ CECID > 0
CESI > 0 ∣ CECID < 0
1.0 CESI < 0 ∣ CECID > 0
CESI < 0 ∣ CECID < 0
0.9
0.8
2005 2010 2015 2020 2025
(a)
EUR and EU - US Spreads
CESI > 0 CESI > 0 CESI < 0 CESI < 0
∣ CECID > 0 ∣ CECID < 0 ∣ CECID > 0 ∣ CECID < 0
Return 1.45% –0.83% 1.63% –2.55%
1.6 Volatility 5.49% 3.45% 3.14% 5.59%
Risk/Reward 0.26 –0.24 0.52 –0.46
Max DD –12.87% –26.64% –5.83% –49.40%
Active IR 0.45 –0.61 1.25 –0.79
1.4 % on 33.63% 15.62% 17.33% 33.40%
CESI > 0 ∣ CECID > 0
1.2
CESI > 0 ∣ CECID < 0
CESI < 0 ∣ CECID > 0
1.0 CESI < 0 ∣ CECID < 0
0.8
0.6
(b) 2005 2010 2015 2020 2025
FIGURE 12.5 (a) Data change works better than surprises for DXY. (b) Model even better
for EUR.
Source: Bloomberg, Citi and authors’ calculations.

274 TRADING GLOBAL MACRO MARKETS
of EURUSD is negative if the CECID differential favors the United States and vice
versa. Adding the surprise index as a secondary variable does not add any value. The
results are similar for the broader USD. Trading the DXY only when the differential
in the data change index is positive results in an information ratio of 0.84, while the
information ratio is negative in the opposite case. It is often the case that models work
better against a basket of assets than against a single asset, given idiosyncratic shocks
that pack a smaller punch in baskets. Idiosyncratic shocks need to be adjusted for on
an ad hoc basis rather than in a rules-based framework.
Of course, the question is why we do not just focus on rate differentials rather than
on economic data. After all, typically stronger data should lead to a widening of rate
spreads. And if US data are outperforming but do not lead to higher rate differentials,
maybe it does not matter for FX. Interest rates could be the best summary statistics for
economic data releases concerning FX trading. To test this hypothesis, an important
question is which interest rate to use. There are several choices to make: real versus
nominal, front-end versus back-end, and spreads versus other countries, or outright
rates. To help us focus on the best interest rates expression, we start with an extremely
stylized model of perfect foresight. In particular, we build a trading strategy based on
realized changes in the rates in question and take a position each week based on the
sign of the interest rate change. Of course, the information ratios are unrealistically
high, relying on information not available in advance, but the results are instructive as
to which interest rate to focus on. As per Figure 12.6, it is clear that rate differentials
are more important than outright rates, but that US rates work better than European
rates, if just focusing on one side of the spread. The information ratio is the highest for
two-year nominal, though information ratios are also quite strong for the other parts
of the curve, as well as for real rates.
0.0
–0.5
–1.0
Relative
oitar
eprahS
Rate Differential
Govt 2-year
2.0
Govt 5-year
Govt 10-year
Real Rates 10-year
1.5
Equity
1.0
0.5
EUR Only US Only
Reference series
FIGURE 12.6 Front-end rates the driver.
Source: Bloomberg and authors’ calculations.

How to Trade FX: The Framework 275
Real Rates
Govt 2-year Govt 5-year Govt 10-year
2.50 10-year
Return 3.21% 3.98% 2.88% –1.65%
Volatility 9.13% 9.12% 9.13% 9.13%
2.25
Risk/Reward 0.35 0.44 0.32 –0.18
Max DD –27.34% –32.63% –28.02% –55.67%
2.00
1.75
1.50
1.25
Govt 2-year Govt 10-year
1.00 Govt 5-year Real Rates 10-year
0.75
0.50
2005 2010 2015 2020 2025
FIGURE 12.7 Rate differentials weak but positive signal.
Source: Bloomberg and authors’ calculations.
Of course, what matters is a realistic trading rule rather than the perfect fore-
sight analysis, which just informs what investors should focus on if they are willing to
engage in a rates forecasting exercise. To get us there, we run our usual tests, where
we show information ratios of strategies, where we trade FX in line with whether the
relevant rates are above or below the 55dma, lagged by two days. We find that for this
specification, the best rate driver is the five-year spread between the United States and
Germany, followed by the two-year spread. The performance using real rate is not
overly helpful. We would note, though, that even for the five-year spread, the informa-
tion ratio is not overly impressive, coming in only at 0.40, as s shown in Figure 12.7.
For our discussion of rates as a driver for FX, it is also important to investigate
the slope of the curve. Often, yield curve changes are driven by the front end. The
slope is therefore somewhat similar to using two-year rate differentials. However, it is
not quite the same, as we have discussed in the rates chapter. Next, we show a back-
test for the 2s/10s yield curve. We use our usual 55dma to distinguish between flat-
tening and steepening episodes, and then add a one-day lag. On the flattening side,
Figure 12.8a shows that bear flattening is somewhat USD bullish, as would be
expected, as it often goes hand in hand with a hawkish Fed. Bull flattening is USD
bearish. But the information ratios are not overly high. Figure 12.8b shows the same
analysis for the steepening side. The bull steepening is most USD bearish and is in line
with a dovish Fed. A bear steepening is most USD bullish. Here, the information ratios
are much stronger. Some of the flattening and steepening regimes achieve higher infor-
mation ratios than the simple rate differentials do, though this could partly be because
the rule on the slope are just lagged by one day, rather than by two, which is possi-
ble because there is no European leg to worry about. However, these models are less
frequently switched on, and we therefore keep our focus on rate differentials in our
composite model.

276 TRADING GLOBAL MACRO MARKETS
Bull Flatten Bear Flatten Twist Flatten Buy & Hold
Return –0.47% 0.15% 0.38% 0.66%
2.0 Volatility 4.11% 3.60% 2.30% 8.30%
Risk/Reward –0.11 0.04 0.16 0.08
Max DD –35.35% –29.70% –14.48% –56.70%
1.8 Active IR –0.24 0.10 0.55 0.08
% on 23.46% 19.52% 9.03% 100.00%
1.6
Buy & Hold
Twist Flatten
1.4
1.2
1.0
Bear Flatten
0.8
Bull Flatten
(a) 1985 1990 1995 2000 2005 2010 2015 2020 2025
Bull Steepen Bear Steepen Twist Steepen Buy & Hold
Return –0.83% 1.36% –0.04% 0.66%
Volatility 3.99% 3.60% 2.16% 8.30%
Risk/Reward –0.21 0.38 –0.02 0.08
2.0 Max DD –43.04% –14.36% –14.06% –56.70%
Active IR –0.47 0.86 –0.07 0.08
% on 19.15% 19.26% 6.37% 100.00%
1.8
1.6
Bear Steepen
1.4
Buy & Hold
1.2
1.0
0.8 Twist Steepen
Bull Steepen
0.6
(b) 1985 1990 1995 2000 2005 2010 2015 2020 2025
FIGURE 12.8 (a) USD likes bear flattening. (b) and likes bear steepening even more.
Source: Bloomberg and authors’ calculations.
12.3 A COMPOSITE MODEL
Having discussed both sides of the smirk, i.e., risk aversion, but also business cycles
(both through data releases and rate differentials), a good model would likely need to
cover both aspects of the smirk. We therefore put all four of our trading rules together:
BTP-Bund spreads, relative equity performance, data changes, and the five-year yield
differentials. Each model is either +1 or –1, and our aggregate model that only trades
when all four models point in the same direction, i.e., having a +4 or –4 read, has an
active information ratio of 1.75, compared to the unconditional Sharpe, which is just
long EUR (carry adjusted), which is flat at just 0.02. It is switched on around 16% of
the time. Trading all four models and aggregating them results in an information ratio
of 1.17. This model is switched on more frequently: around 66% of the time. This
is shown in Figure 12.9. For a similar version, see Miani et al. (2025), which includes

How to Trade FX: The Framework 277
Bund-BTP Equity Govt 5-year CECI All Combo
4.5 Return 3.82% 4.55% 3.98% 6.38% 2.52% 4.67%
Volatility 9.12% 9.12% 9.12% 9.12% 3.60% 4.91%
Risk/Reward 0.42 0.50 0.44 0.70 0.70 0.95
4.0 Max DD –20.62% –28.78% –32.63% –17.58% –7.52% –7.66%
Active IR 0.42 0.50 0.44 0.70 1.75 1.17
% on 100.00% 100.00% 100.00% 100.00% 16.08% 66.24%
3.5
3.0
2.5
2.0
1.5
1.0
Bund-BTP Govt 5-year All Combo
Equity CECI
0.5
2005 2010 2015 2020 2025
FIGURE 12.9 Aggregating all four models works best.
Source: Bloomberg, Citi and authors’ calculations.
terms of trade and finds strong performance across a range of G10 currencies. Japan
is the exception, which we discuss as special in a section later.
12.4 THE USD IN BUBBLY TIMES
We have written in the equity section that a simple technique to identify bubbles can
be helpful, not to get bearish equities, but to trade equities with better risk control.
Identifying equity bubbles is also useful for FX trading. It is probably not surprising
that periods of building US equity bubbles are typically USD bullish, before sometimes
becoming USD bearish late in the bubble, as shown in Figure 12.10. The USD bullish
move is partly because US rates also tend to move higher. Interestingly, even without
rates moving higher, like in the 1997–1998 episode, the USD nonetheless moved
strongly higher, in that instance because risk aversion. But more generally speaking,
it is the building of the bubble that sucks capital into the United States, both in the
form of portfolio investment and also in the form of FDI. US equity markets typically
outperform during these bubbles. This is often the case, even if other equity markets
around the world also do quite well. One reason may be that some of these bubbles
are driven by technological innovation, and the United States has been at the center
of the last episodes of that, as was especially the case during the internet revolution in
the 2000s, but also during the current AI-driven investment cycle. However, we note
that pullbacks in the DXY during those periods can be quite pronounced. The “bub-
ble regime” can therefore not be used as the main framework to trade the USD, even
though it may well determine the USD direction in the bigger picture.

278 TRADING GLOBAL MACRO MARKETS
DXY during equity bubbles
1997-Jul to 1998-Jun 2023-Jun to 2025-Apr
1.25 1998-Nov to 2001-Nov 2025-May to Oct 25 (time of writing)
2020-Oct to 2022-Jun
1.20
1.15
1.10 Current bubble
1.05
1.00
0.95
0 200 400 600 800 1000
FIGURE 12.10 USD rising in equity bubbles.
Source: Bloomberg and authors’ calculations.
3
2
1
0
–2
–2
Relative
oitar
eprahS
Rate Differential
Govt 2-year
Govt 5-year
Govt 10-year
Real Rates 10-year
Equity
JPY Only US Only
Reference series
FIGURE 12.11 US rates drive the yen.
Source: Bloomberg and authors’ calculations.
12.5 JPY IS SPECIAL
We have shown at the very outset of the chapter that the JPY is somewhat special, as
it appreciates with risk aversion, which the majority of the G10 currencies do not do.
However, when it comes to the rates factor, the JPY shows similar patterns to other
currencies, and the main difference is that the USD bullish impact of higher US rates
is much more consistent than for the trade-weighted USD. Figure 12.11 repeats our

How to Trade FX: The Framework 279
perfect foresight analysis that we have shown for the euro and TWI. Again, this is just
for illustrative purposes and can not be traded. The Sharpe ratio of positioning with
the direction of rate moves is higher for the JPY than for most other FX, coming in
at >3 for most sectors of the curve. There is little difference between two year, five
year, and ten year. Interestingly, the Sharpe ratio is slightly higher when just using US
rates rather than focusing on rate differentials with Japan. Just using the JGB direction
is negative, given that the correlation of JGBs with US rates is positive, but with the
volatility of JGBs being just a fraction of the US. Relative equity returns are much less
relevant, partly because Japanese equities benefit strongly from a weaker JPY.
One reason why the rates strategy has a higher Sharpe ratio than for other cur-
rencies is that JPY typically strengthens with rising risk aversion. Given that US
rates can fall quite sharply during periods of rising risk aversion, USDJPY retains its
directionality with US rates during such periods, which is not necessarily the case for
other FX. One reason for this trading behavior of USDJPY is that Japan has a very
strong net international investment position, i.e., a large surplus of external financial
assets over liabilities. This measure is aggregating both public and private sector assets
and is essentially the result of an accumulation of current account surpluses over time.
As a result, during a time of crisis, Japanese investors tend to repatriate foreign assets,
pushing USDJPY lower. Maybe as importantly, given that the JPY is typically a funder
of carry trades, during times of crisis, investors tend to unwind these types of trades,
given that carry trades thrive on low volatility, which is quickly upended by a crisis.
To unwind carry trades, investors have to buy back JPY, also contributing to upside
pressure on the JPY. The pure risk aversion channel for USDJPY has become weaker,
though. In the 2020 COVID crisis, USDJPY sold off hard, but only for around two
weeks, troughing before the peak in VIX. This trough did coincide with the trough in
US rates on March 6, though. As such, the US rates correlation has remained strongly
in place. Figure 12.12 shows the result of buying yen after the VIX is x standard devi-
ations above its three-year average, or higher. We lag buying until the close of the
VIX >0 VIX >1 VIX >1.5 VIX >2 VIX >3
Return –0.91% 0.58% 0.72% 1.10% 1.27%
Volatility 6.78% 5.46% 4.88% 4.39% 3.67%
1.5 Risk/Reward –0.13 0.11 0.15 0.25 0.35
Max DD –40.96% –17.16% –17.41% –16.39% –8.03%
1.4 Active IR –0.21 0.24 0.40 0.82 1.63
% on 40.45% 19.20% 13.61% 9.42% 4.53%
1.3
1.2
1.1
1.0
0.9
0.8 VIX >0σ VIX >2σ
VIX >1σ VIX >3σ
0.7 VIX >1.5σ
2005 2010 2015 2020 2025
FIGURE 12.12 Only extreme VIX levels still push USDJPY lower with follow-through.
Source: Bloomberg and authors’ calculations.

280 TRADING GLOBAL MACRO MARKETS
following day and hold the position for a week (five trading days). As can be seen in
Figure 12.12, the most profitable period for this strategy was during the GFC. Since
then, extreme moves, with VIX above 3 standard deviations, are still tradable, with
2 standard deviation moves less so.
However, if we operationalize the US rates strategy using our normal framework,
the results are not overly impressive. As can be seen in Figure 12.13, trading USDJPY
just in line with US rates is profitable, but barely so. Only being long USDJPY when US
rates are above their 55dma, and vice versa, with a one-day lag, leads to an information
ratio of 0.24, when using two-year US rates, which works best. That type of informa-
tion ratio is obviously not tradable. Analyzing Figure 12.13 more carefully suggests
two distinct regimes. Prior to mid-2012 and then again from 2021 onward, US rates
worked very well as a driver for USDJPY. However, for almost 10 years in between, it
did not. This interim period coincided with the rule of Japanese Prime Minister Shinzo
Abe, who was in office from December 2012 to September 2020. His reforms put local
Japanese factors into play rather than US rates. Furthermore, the initial part of Abe’s
reign coincided with US rates being glued to zero in the aftermath of the GFC. Without
any Fed action on the one hand and an aggressive policy of weakening the JPY by Abe
on the other, it is no surprise that the simple rates-based trading rule broke down. But,
in general, this was an opportunity for macro funds, not a problem. Periods of strong,
trending moves in a currency, especially when backed up by a fundamental story, are
often when returns of macro hedge funds excel, even when a regime change means that
some of the more quantitative models stop working.
Real Rates
2.25 Govt 2-year Govt 5-year Govt 10-year 10-year JPY
Return 2.34% 1.50% 0.57% 0.50% –2.41%
Volatility 9.88% 9.88% 9.89% 9.89% 9.89%
2.00 Risk/Reward 0.24 0.15 0.06 0.05 –0.24
Max DD –50.34% –40.75% –36.70% –34.23% –61.97%
1.75
1.50
1.25
1.00
0.75
Govt 2-year Real Rates 10-year
0.50 Govt 5-year JPY
Govt 10-year
2005 2010 2015 2020 2025
FIGURE 12.13 Rate differentials weak but Even for USDJPY, rate differentials do not always
work.
Source: Bloomberg and authors’ calculations.

How to Trade FX: The Framework 281
The Reign of Abe
PM Shinzo Abe launched Abenomics in 2012, as a response to Japan’s decades-
long regime of low growth and deflation. His economic agenda consisted of
“three arrows”: aggressive monetary easing, flexible fiscal policy, and structural
reforms. For FX, it was mostly the first arrow, monetary policy, which was
explicitly aimed at ending deflation and revitalizing growth, that was relevant.
In particular, the BoJ shifted to an ultra-loose monetary policy under Gover-
nor Kuroda. In early 2013, the BoJ launched a massive quantitative and qual-
itative easing (QQE) program, buying long-term government bonds as well as
equities (in ETF form) on a very significant scale. The monetary base expanded
from around 125rn JPY in late 2012 to 360trn in early 2016 and kept expand-
ing quickly thereafter. The BoJ’s overnight call rate was cut into negative terri-
tory in early 2016. Ten-year JGB yields fell from around 75bp in late 2012 to
around –25bp in early 2016. A weaker JPY was part of the desired outcome
of these policies, as it was seen as growth-supportive, with a focus on Japanese
exporters, but also was considered important in the fight against deflation,
both through higher import prices and generally higher inflation expectations.
USDJPY obliged, rallying from around 80 in late 2012 to 125 in 2015, as is
illustrated in Figure 12.14. In this process, JPY became a very popular funding
currency for the carry trade, further weakening the JPY. So far, so logical, and
broadly still in line with our overall macro framework, that interest rates are the
key driver, even if it was mostly on the Japanese side for a change. However,
in late 2015, the JPY abruptly changed direction and strengthened. The reason
was that the risk aversion angle took over again at that stage. Concerns about
China’s slowing economy, falling oil prices, and fears of a global recession caused
investors to pull back from riskier assets, giving a bid to the JPY. USDJPY started
to be more closely correlated with the Topix than with rates. On the Japanese side,
when the BoJ surprised the market by moving to negative interest rates on excess
reserves in January of 2016, it did not lead to renewed JPY weakness, as investors
were doubting how much room for additional policy support the BoJ would still
have, and whether monetary policy would be sufficiently supportive for growth
and inflation. The market started to doubt Abenomics, leading to JPY buying as
well. This tumultuous period in Japanese politics clearly overwhelmed the simple
one-factor JPY trading model.
(Continued)

282 TRADING GLOBAL MACRO MARKETS
(Continued)
120
110
100
90
80
2012 2013 2014 2015 2016 2017
neY/$
1.0 1800
0.8
1600
0.6
1400
0.4
1200
0.2
1000
0.0
800 –0.2
dleiy
BGJ
raey-01
xipoT
USD/JPY
Japan 10-year yield (right)
Topix
FIGURE 12.14 The reign of Abe.
Source: Bloomberg.
12.6 FACTORS FOR FX
Next, we go into a short discussion of the more important factors in FX space.
Table 12.1 shows the information ratios of the various strategies. Clearly, carry has
the best historical performance, followed by time series momentum (labeled TS Mom).
Cross-sectional momentum, economic surprises, and value (PPP) also generate signifi-
cant positive information ratios. The factors lean on work done at Citi, as, for example,
reported in Saunders et al. (2025a).
TABLE 12.1 Carry the Most Attractive FX Factor
Carry Eco Cross-sectional TS Mom PPP Model
to vol surprises Mom combination
Return 2.0% 0.8% 1.3% 2.5% 1.7% 1.7%
Volatility 2.2% 1.5% 2.1% 3.4% 3.1% 1.5%
Risk/Reward 0.89 0.56 0.64 0.71 0.55 1.20
Max drawdown –5.1% –4.8% –8.3% –5.9% –7.7% –2.6%
Source: Bloomberg, Citi, and authors’ calculations

How to Trade FX: The Framework 283
12.7 LIVING OFF CARRY
Given the inherent difficulty in translating macro fundamentals into successful FX
trades, there has been a significant focus on trading factors, most famously the carry
factor, but other factors are also making a showing in the literature. For us, the FX
trade with the highest success rate is the carry trade. We have already written about
the EM part in the emerging markets trading book. However, since that book was
published, a lot has happened to the carry trade, and we have some important addi-
tions to our original framework.
Our favorite expression of the carry trade is to rank currencies by implied yields
over implied volatility and then create a basket of the top five against the bottom
five, where we set the size for each currency in line with the volatility over the pre-
vious three months. The sizing is extremely important. First, if we rank carry in a
volatility-adjusted way, we also have to use volatility for the sizing, as we otherwise
do not “earn” enough of the high carry in the less volatile pairs. Second, and more
importantly, the volatility weighing typically results in a long USD position in notional
terms, as the high-yielders are usually more volatile than the low-yielders. A net long
USD position works well in terms of protecting returns when risk aversion leads to a
pull-back in the appetite for carry trades. As the low-yielders typically yield less than
the USD, increasing the position size of the low-yielders tends to add to the positive
carry of the basket and therefore adds to the appeal of the carry trade. As illustrated in
Figure 12.15, for a global basket that includes both EM and DM FX, the simple carry
(top five against bottom five) leads to an information ratio of 0.74. Adjusting the posi-
tioning sizing by volatility results in a slightly falling information ratio of 0.71. If we
rank the currencies based on carry to vol, the information ratio declines further to
Carry vol Carry
Carry
adj to vol vol adj
Return 2.82% 2.70% 3.39%
2.2
Volatility 3.79% 3.81% 3.80%
Risk/Reward 0.74 0.71 0.89
2.0 Max DD –8.36% –8.70% –8.68%
1.8 Carry to vol vol adj Carry
1.6
1.4
1.2
Carry vol adj
1.0
2005 2010 2015 2020 2025
FIGURE 12.15 Volatility adjustments are the key to carry.
Source: Bloomberg and authors’ calculations.

284 TRADING GLOBAL MACRO MARKETS
G10 Carry to EM Carry to COMB Carry to
vol vol. adj. vol vol. adj. vol vol. adj.
Return 1.04% 1.69% 1.95%
Volatility 3.94% 1.94% 2.19%
1.6 Risk/Reward 0.26 0.87 0.89
Max DD –14.83% –6.17% –5.08%
1.5
1.4 COMB Carry to vol vol. adj.
1.3 EM Carry to vol vol. adj.
1.2
1.1
G10 Carry to vol vol. adj.
1.0
2005 2010 2015 2020 2025
FIGURE 12.16 Carry works better for EM.
Source: Bloomberg and authors’ calculations.
0.66 (not shown) as low-yielding but low-volatility currencies reduce the carry of the
overall portfolio. However, adjusting also the position size of the carry to vol ranked
basket, raises the information ratio to 0.89.
The carry trade tends to work better in EM than in G10, as per Figure 12.16. One
reason is that low-yielders in EM space typically sell off during rising risk aversion,
while low-yielders in G10 space tend to rally, adding insult to injury, when the long
part of the carry trade is already bleeding. This is especially true for JPY, but also for
CHF. The other reason is obviously that carry in EM is just higher.
Having said that, we would note that even if JPY is not a direct component of our
EM carry trade, the direction of USDJPY matters more broadly and more so than the
directionality of the SPX, as is illustrated in Figure 12.17a, b. Only owning our carry
basket when USDJPY is below its 55dma results in an information ratio of 4.9 (no
lag, no transaction costs). Our basket returns an information ratio of –3.5 when the
opposite is true, creating a more decisive wedge than in the case of the SPX, where the
SPX trading below its 55dma only leads to a negative information ratio of –0.81 (and
above comes in at 2.15). Furthermore, the sensitivity to JPY remains clearly in place,
while using the SPX for timing carry has essentially stopped working post-COVID.
What determines how well the carry trade does? Interestingly, our version of the
carry trade does quite well in most environments. Long-lasting drawdowns are rare,
as the short leg works quite well when risk aversion spikes. Still, we found some con-
ditions when the carry trade does even better than normal. The first one is, somewhat
unsurprisingly, linked to the extent of carry that is on offer. Figure 12.18 shows the
carry inherent in our EMFX carry basket on January 2 of each year in relation to
the performance of the carry trade over the next 12 months. Clearly, high carry is
supportive of higher returns for this factor. If carry drops, initially returns are not

How to Trade FX: The Framework 285
COMB
USDJPY down USDJPY up
Carry to vol vol. adj.
Return –5.38% 7.26% 1.95%
Volatility 1.52% 1.47% 2.19%
5
Risk/Reward –3.55 4.92 0.89
Max DD –71.37% –1.81% –5.08%
4
3
USDJPY up
COMB Carry to vol vol. adj.
2
1 USDJPY down
(a) 2005 2010 2015 2020 2025
SPX down SPX up COMB
2.2 Carry to vol vol. adj.
Return –1.28% 3.23% 1.95%
Volatility 1.57% 1.50% 2.19%
2.0
Risk/Reward –0.81 2.15 0.89
Max DD –32.35% –4.12% –5.08%
1.8
SPX up
1.6
1.4
1.2
COMB Carry to vol vol. adj.
1.0
SPX down
0.8
(b) 2005 2010 2015 2020 2025
FIGURE 12.17 (a) Carry likes a weak USDJPY (b) ... and strong equities, but less so.
Source: Bloomberg and authors’ calculations.
necessarily falling, but once carry has fallen below 400bp, returns are much less attrac-
tive. Still, even at a carry level around 400bp it takes a crisis like 2008 or 2020 for the
factor to lose meaningful money.
Low volatility is also very helpful for the carry trade. Volatility is very difficult to
forecast. While it is broadly mean-reverting, a simple mean-reversion strategy does not
do overly well, given that volatility can remain depressed for a very long time before
moving higher again. Having said that, one regularity is that fixed income volatility
comes off late in the hiking cycle as well as during the time when the Fed is on hold.
With FX volatility and US rates volatility highly correlated, this makes the late hiking
cycle and the Fed pauses an attractive environment for carry trades.

286 TRADING GLOBAL MACRO MARKETS
vol. adj. basket EM Carry vs. Subsequent Returns by Year
2019
2024
2009
2014
4.0% 2007
2011 2005 2003
20042006
2016 2023
2.0% 2022 2012
2017
2013 2015
2010
2021
0.0%
2018
–2.0%
2020
2008
0.0% 2.0% 4.0% 6.0%
Carry (Annual)
)launnA(
snruteR
ygetartS
yrraC
Fit (R2=0.09)
8.0% 10.0%
FIGURE 12.18 Size of carry matters.
Source: Bloomberg and authors’ calculations.
While we already use volatility for the construction of our carry basket, we also like
to use volatility for further adjustments to the carry trades. This can be done by more
frequent re-weighting, where rising volatility leads to smaller positions. This is one
reason why the daily reweighted FX carry baskets display better performance than the
monthly reweighted portfolios, when abstracting from transaction costs. An alternative
approach to take volatility into account would be to cut the carry trade when volatility
rises by a certain extent. Periods of high volatility do not mean-revert particularly
fast. Therefore, spikes in volatility are usually good times to reduce risk, even after
the initial spike has already occurred. As already mentioned in the credit chapter, our
favorite volatility measure is to take the maximum of the one-year rolling z-score of
the implied volatilities of fixed income, FX equity, credit spreads, as well as oil. Taking
the maximum makes sure that most crises are captured, even if they take place in a
less central asset class. Using this measure to cut out of the carry trade when it spikes
above two significantly raises the active information ratio of the carry strategy, from
0.89 to 1.30. The 2 to 4 standard deviation range still has a positive information ratio,
but at 0.32, it is significantly lower. For outright negative information ratios, a spike to
four standard deviations is needed, which occurs around 3% of the time in our sample
(which is clearly not normally distributed, as illustrated in Figure 12.19. Of course,
with the information ratio of the strategy generally staying above zero, investors may

How to Trade FX: The Framework 287
Max Vol σ ≤ –1 –1 M < a xσ V ≤ ol 2 2 M < a σx V ≤ o l 4 Max Vol σ > 4 Hold if < 2σ ad F j. X C v a o r l ry
Return 0.05% 2.00% 0.14% –0.25% 2.06% 1.95%
Volatility 0.27% 1.76% 1.06% 0.71% 1.78% 2.19%
1.7
Risk/Reward 0.19 1.14 0.14 –0.35 1.15 0.89
Max DD –1.40% –3.08% –4.48% –6.35% –3.93% –5.08%
Active IR 1.20 1.30 0.32 –2.02 1.30 0.89
1.6 % on 2.50% 76.78% 17.65% 3.06% 79.27% 100.00%
1.5
Hold if < 2σ
1.4
Max Vol –1 < σ ≤ 2
1.3
1.2
FX vol adj. Carry
Max Vol 2 < σ ≤ 4 Max Vol σ ≤ –1 Max Vol σ > 4
1.1
1.0
2005 2010 2015 2020 2025
FIGURE 12.19 Carry likes low volatility.
Source: Bloomberg and authors’ calculations.
save themselves the transaction costs involved in trading our volatility signal. But at
the very least, a four sigma signal deserves to be taken seriously.
Positioning is also a factor that drives forward returns of the carry trade. While
positioning is not easy to measure in FX, we are tracking Citi’s proprietary flows into
and out of the EMFX carry basket. We use the methodology laid out by Saunders
et al. (2025b). We take into account both inflows into the long side of the basket and
outflows from the short side of the basket. As we prefer the volatility-weighted carry
basket, we also weigh inflows accordingly. Analyzing these net flows, we find that
forward Sharpe ratios do have a correlation with the percentile of inflows into the carry
trade for the previous few months. When inflows by leveraged accounts are above the
60th percentile in the previous month, forward Sharpe ratios fall significantly (though
stay positive). This is illustrated in Figure 12.20, and works especially well for one-
month forward returns, though in a weaker form, the pattern also holds for longer
holding periods. Again, information ratios stay positive, which suggests that investors
can also sit through some positioning signals. However, we also found that the worst
outcomes tend to occur when both these factors strike at the same time, i.e., when
volatility spikes at a time when positioning is heavy. Those events should be taken
seriously, even by investors who prefer not to react to every trading signal.
In summary, the carry trade is a true and tested strategy that has stood the test of
time. We would implement the trade in EM, with positioning size driven by risk instead
of using equal notionals. We would size the trade the largest when carry is high, the Fed
is in the low volatility part of its cycle, and inflows have been relatively more muted.
But the default case should be to have the trade on. It takes a combination of crowded
positioning and a volatility spike to undermine the carry trade more significantly.

288 TRADING GLOBAL MACRO MARKETS
Carry (vol adj)
1m Flow percentile 3m Flow percentile 6m Flow percentile
1.34
1.82
1.67
0.14
elitnecreP
swolF
degareveL
0–20 0.66 1.26
20–40 2.71 0.05
40–60 1.11 1.47
60–80 0.49 1.38
80–100 0.55 0.57 0.79
<80 1.17 1.17 1.09
Uncond 1.04 1.03 1.02
FIGURE 12.20 Carry works best if uncrowded.
Source: Bloomberg, Citi, and authors’ calculations.
12.8 VALUE WORKS TOO
Value is also an attractive factor in FX. Even a simple version of PPP works relatively
well. Here, we rank the deviation of FX from its PPP level and then take a z-score. The
factor goes long in proportion to the rank of each strategy, in line with the academic
literature; see for example, Asness et al. (2013). Restricting the holdings to the top and
bottom five currencies gives similar results. The factor is somewhat correlated with
carry unless we make Balassa-Samuelson adjustments (Balassa, 1964 and Samuelson,
1964) for higher productivity (via residualizing differences by GDP per capita), but we
find that strategy much less effective. Research by the Citi QIS FX team (Pickering and
Ismail, 2022) shows that different valuation measures work at different times, but in
general, we think it does not add too much value to make the simple PPP framework
much more complicated. The additional alpha is quite limited, and PPP works reason-
ably well for both the EM and the G10 universes. Figure 12.21 shows the results for a
broad universe of 22 countries using World Bank data. For FX, an information ratio of
0.48 is relatively strong, especially for a very simple model without much opportunity
to overfit.
Just like for carry, for the PPP strategy, crowding is also a headwind. As per
Figure 12.22, the forward one-month Sharpe ratio is above 1 when inflows from lever-
aged accounts were in the lower 60th percentile in the month prior but is negative if
inflows were stronger than that. The pattern is also in place for longer holding hori-
zons, but not as pronounced. This is one of the more important use cases for Citi’s
flow data, as is laid out, for example, by Saunders et al. (2025b).
Valuation is also useful for assessing times when a currency’s positioning might be
stretched or when intervention is (a) more likely or (b) can be successful—we discuss
this in the context of the yen and Swiss franc in a separate section later.

How to Trade FX: The Framework 289
PPP
1.5 Return 1.71%
Volatility 3.11%
Risk/Reward 0.55
1.4 Max DD –7.68%
1.3
1.2
1.1
1.0 PPP
2005 2010 2015 2020 2025
FIGURE 12.21 Valuation (PPP) can add value.
Source: Bloomberg, Citi, and authors’ calculations.
Value (PPP)
1m Flow percentile 3m Flow percentile 6m Flow percentile
0.97
1.03
1.19
–0.37
elitnecreP
swolF
degareveL
0–20 0.96 0.52
20–40 0.24 0.68
40–60 –0.05 –0.12
60–80 0.49 0.35
80–100 –0.60 –0.02 0.21
<80 0.58 0.39 0.33
Unconditional 0.32 0.31 0.30
FIGURE 12.22 PPP also better if uncrowded.
Source: Bloomberg, Citi, and authors’ calculations.
12.9 RIDING THE TREND
Given that macro-trading often has a trend following component, and given the pop-
ularity of FX in macro-trading, our prior expectation was that trend following should
work quite well in FX. However, the truth is more nuanced. Before the financial crisis,

290 TRADING GLOBAL MACRO MARKETS
XS Mom TS Mom
vol adjust vol adjust
Return 1.32% 2.45%
Volatility 2.05% 3.44%
1.8
Risk/Reward 0.64 0.71
Max DD –8.34% –5.93%
1.6
TS Mom vol adjust
1.4 XS Mom vol adjust
1.2
1.0
2005 2010 2015 2020 2025
FIGURE 12.23 Momentum trades weaker than during glory days of early 2000s.
Source: Bloomberg and authors’ calculations.
some relatively simple strategies worked well in FX, perhaps contributing to the popu-
larity of FX trading by macro and systematic funds at the time. Post the financial crisis,
some of the systematic strategies did not work as well, and the meager returns forced
a retracement in stand-alone FX strategies and, in particular, in systematic ones.
In Figure 12.23, we show the classic cross-sectional momentum from the aca-
demic literature (see Jegadeesh and Titman, 1993 for an equity-focused version or
Asness et al., 2013 for macro). We take a simple strategy where we normalize the last
three month total returns for each currency. We then cross-sectionally rank and fur-
ther volatility-adjust the positions. We implement the strategy weekly, given the high
potential turnover. Blending faster and slower, longer periods can also be helpful to
reduce transaction costs. This worked well up until 2009, but returns have been noisy
ever since. Part of the reason was likely the low dispersion in monetary policy, which
in turn was due to the slow recovery from the GFC, leading to fewer opportunities in
jumping on the bandwagon of a country or group of countries with a differential macro
backdrop. With higher interest rates came higher interest rate dispersion, and there-
fore, the strategy could make a comeback. Recent performance has been respectable,
with momentum clocking in a 0.96 Sharpe since 2022, when the Fed started a hiking
cycle in March of that year (with some other central banks ahead of the curve, includ-
ing in EM). Still, the increase in the availability of data, the easy implementation of
the strategy, and the ability for retail investors to take FX positions via brokerage and
other accounts mean that we are unlikely to see a comeback of the returns of momen-
tum strategies back to the glory days seen in the mid-2000s.
One area where returns have been more consistent in recent years is in trend
following i.e., dollar-directional strategies, which take a position based on the sign of
the most recent returns and typically use the dollar as a numeraire. We take the recent

How to Trade FX: The Framework 291
three-month performance versus the dollar and go long if it is positive, short if it is
negative—again, positions are sized based on volatility. The signal in Figure 12.23 is
implemented weekly, which gives very similar performance to a daily implementation.
Given that the correlation between exchange rates is typically high, the time series
momentum strategies tend to have quite a large long or short USD position. Correla-
tion with the cross-sectional version is quite high, and returns have also been much
weaker post the GFC, though overall the returns have been better than for the cross-
sectional version.
12.10 HIDE IN SURPRISE
Lastly, we show that Citi’s economic surprise index can be a useful diversifier to other
FX strategies. The methodology is exactly the same as for the other factors. This time
we sort currencies by the level of the Citi’s economic surprise indicator. Its stand-alone
information ratio comes in at 0.56. Empirically, it has done well in drawdown periods
for the carry strategy, as shown in Figure 12.24. This may be just luck, but it could also
be a more durable pattern if, in times of risk aversion, investors take solace in countries
that are performing relatively well. Combining all factors, despite volatility adjusted
carry’s superior stand-alone performance, is the route to more consistent returns. In
Figure 12.24, we show the performance of the combination of carry, value, trend, and
economic surprises, all constructed in a similar way. This combination has delivered an
information ratio of 1.20 (before transaction costs), an improvement over carry only.
Eco Surprises Carry to
vol adjust vol vol adj Model Combo
Return 0.84% 1.95% 1.74%
Volatility 1.52% 2.19% 1.45%
1.6 Risk/Reward 0.56 0.89 1.20
Max DD –4.82% –5.08% –2.60%
1.5
1.4
Carry to vol vol adj
1.3
Model Combo
1.2
1.1
Eco Surprises vol adjust
1.0
2005 2010 2015 2020 2025
FIGURE 12.24 Eco surprises a diversifier.
Source: Bloomberg and authors’ calculations.

292 TRADING GLOBAL MACRO MARKETS
12.11 SUMMARY
We start laying out the USD smirk theory. Focusing first on EURUSD, we find that rel-
ative equity performance is superior to other measures of risk aversion to capture the
left-hand side of the USD smirk. Our favorite way to implement the right-hand side is
to use Citi’s data change indexes in relative terms. Using rate differentials, we find that
five-year nominal spreads add the most value. Analyzing curves, bear steepening and
bear flattening are most USD positive. Combining the relative equity performance and
BTP-Bunds spreads, with the data change indexes and rates, results in a high infor-
mation ratio for trading EUR. JPY is special in that it relatively consistently appre-
ciates with risk aversion. This means that rate differentials are the key for USDJPY,
while relative equity performance is not as helpful. For the riskier currencies, our main
framework is the carry factor. Carry usually works, especially when both ranking and
position sizing are volatility adjusted. Warning signs are a strong JPY, rising volatility,
and heavy positioning. Outside of carry, valuation also works well as an FX factor.
Using Citi’s economic surprise indexes also adds alpha, while the performance of sim-
ple trend following strategies has deteriorated.