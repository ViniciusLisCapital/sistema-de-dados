8
CHAPTER
How to Trade Equities: A Framework
Equities are an interesting macro-asset. On the one hand, they are clearly impacted
by macro cycles, by central banks, and by the USD. At times, equities are the key
driver of the business cycle, like during the dot.com bubble or during the AI boom.
On the other hand, for any given equity, the bottom-up picture is likely much more
important than the overall macro, at least for medium-term returns. Therefore, we
mostly focus on overall equity indexes, though we would note that macro is extremely
important for many industries, and subindustry baskets, like banks. Moving to an
industry level is also helpful in order to get around the fact that the SPX is constantly
changing its composition, complicating historical comparisons. But that is a story for
another book. For us, this changing industry composition of the SPX mostly means
that we take the more recent performance of our backtests more seriously than the
more distant past.
8.1 EQUITIES IN THE BIG PICTURE: THE ONLY WAY IS UP
The US equity market has been one of the best-performing long-term asset classes of
recent decades. Even when starting in 1929, just before the onset of the deepest bear
market on record, average annualized returns still amount to 7.9% (using monthly
Shiller data excess of T-bill yields, 6.9% geometric returns). However, 10-year returns
are highly dependent on the starting point and on the valuation at that point in time,
as shown in Chapter 1. The other point to make is that the US market is some-
what unique. Sharpe ratios are significantly lower for many other equity markets (but
not all).
To illustrate US exceptionalism, we use the underlying data in Jorda et al. (2019),
which gives a very long-term history for a number of equity (and housing) markets,
going back as far as the 1870s. In Figure 8.1 we show long-term, real (i.e., adjusted
for CPI) returns for equity markets and their volatility, calculated using annual returns
(see Jorda et al., 2017 for more details on the dataset). We start the study in 1901
such that each country has the same history, including a number of stress periods that
have meaningfully reduced returns (especially in the case of France and Portugal) or
increased volatility, like for Germany during the hyper-inflationary 1920s. We find that
the United States, Australia, and a couple of the smaller Nordic countries stand out for
their higher returns relative to volatilities. In absolute returns, Germany and Finland
159

160 TRADING GLOBAL MACRO MARKETS
Germany
9.0% Japan
Finland
Australia USA
Sweden
8.0% Denmark
Netherlands
7.0% UK
Switzerland
6.0% Norway Belgium Italy
Spain
5.0%
4.0% Portugal
France
16.0% 18.0% 20.0% 22.0% 24.0%
Volatility
nruteR
laeR
26.0% 28.0% 30.0% 32.0%
FIGURE 8.1 The US with strong, but not singular returns.
Source: www.macrohistory.net and authors’ calculations.
score well over the very long term. Interestingly, in spite of its recent successes and the
fact that World War II was much less devastating for the United States, it is not the
single best performing large market.
In Figure 8.2 we show Sharpe ratios calculated using T-bill rates from the same
database. On this basis, the United States is more exceptional, with only the much
smaller Australia delivering higher risk-adjusted returns over the very long term. The
United States has indeed been exceptional among large equity markets.
The question is whether the good fortune of the US equity market can persist.
Until 2007, the US housing market had never turned down on a national level, even
though it had happened frequently in other countries. Too narrow a focus on US his-
toric performance could therefore create overconfidence. It is therefore important to
understand why the US may be exceptional. To us, there are several factors at play.
The single biggest one is that US EPS growth has also outpaced international markets.
This could be a combination of higher GDP growth, maybe driven by more activist
policymaking from both the US Treasury and the Fed, though the correlation between
GDP growth and EPS growth is not as high as one would expect. Or it could be due
to lighter regulation, potentially leading to more innovation, due to more oligopolistic
industry structures, or due to more shareholder-friendly policies. The list of candidates
is long. As some of these factors are structural, the good fortune of the United States
may well persist. But we also note that a Sharpe ratio of 0.5 is not a lot of fun to trade,
as drawdowns are relatively frequent and deep. We therefore investigate next how to
actively trade equities from a top-down perspective.

How to Trade Equities: A Framework 161
ailartsuA
0.40
0.35
0.30
0.25
0.20
0.15
0.10
0.05
0.00
oitar
eprahS
ASU napaJ dnalniF nedewS dnalreztiwS kramneD sdnalrehteN KU niapS yawroN muigleB ylatI ecnarF lagutroP ynamreG
FIGURE 8.2 And a superior Sharpe ratio.
Source: www.macrohistory.net (use data since 1901) and authors’ calculations.
8.2 EQUITIES AND THE BUSINESS CYCLE
Given the long-term track record, the default position on equities has to be long unless
there is a compelling reason not to be. We have already shown in Chapter 3 that a com-
ing recession is one reason not to be long equities, but here we broaden the approach
by taking SPX drawdowns as a starting point for the analysis, rather than starting with
recessions. Figure 8.1 shows all the episodes in which the SPX total return index had
a drawdown of at least 20%, where a new drawdown can only start after a 25% rally
from the lows (to get us back to where we came from). We check performance over
T-bills. We start the analysis in the 1950s, as the 1930s and 1940s were a much more
volatile time with a very different market micro-structure. We find that recessions are
part of the problem. Of the 14 episodes where the SPX had a drawdown of more than
20%, seven were either coincident or directly preceding a recession, as is shown in
Table 8.1. However, several recessions only led to downturns of the order of 15% and
are therefore not listed here.
Avoiding recessions is only half the game, as is shown by Figure 8.3. The sec-
ond most severe drawdown category was deflating bubbles (driven by the 2000–2002
event, as the 1961–1962 one was smaller). The 2000 event also had a (shallow) reces-
sion associated with it. Some drawdowns were financial market accidents/crises that
did not lead to a recession: the 1987 crash, blamed partly on portfolio insurance exac-
erbating volatility, and the 1998 episode, driven by LTCM. More recently, the SPX
experienced a sell-off of 25% in 2022. This sell-off probably coincided with a manu-
facturing recession, but more importantly, it coincided with an aggressive hiking cycle
by the Fed, which was seen as likely to trigger a recession down the road, even though

162 TRADING GLOBAL MACRO MARKETS
TABLE 8.1 Bear Market Events
CPI
Length FF change 10Y
Peak Trough Max DD (trough) change (trough) change Reason
Jul-1957 Oct-1957 –21.2% 3.3 –1.2 Recession
Dec-1961 Jun-1962 –28.7% 6.4 0.0 0.6 Deflating bubble
Feb-1966 Oct-1966 –22.9% 7.9 0.0 1.2 0.3 Stagflation
Nov-1968 May-1970 –42.6% 17.8 0.3 1.6 2.4 Recession
Jan-1973 Oct-1974 –54.3% 20.7 2.1 8.2 1.6 Recession/
Stagflation
Nov-1980 Aug-1982 –35.6% 20.7 –2.0 –6.7 1.0 Recession
Jun-1983 Jul-1984 –21.5% 13.1 –0.6 1.8 2.5 Stagflation
Aug-1987 Dec-1987 –34.2% 3.3 2.4 0.0 0.2 Financial accident
Oct-1989 Oct-1990 –24.9% 12.1 –2.8 1.8 0.9 Recession
Jul-1998 Oct-1998 –22.8% 2.7 –0.5 –0.3 –1.0 Financial accident
Mar-2000 Oct-2002 –54.1% 30.5 –4.8 –1.7 –2.6 Deflating bubble
Jul-2007 Mar-2009 –55.8% 19.9 –5.0 –2.8 –2.2 Recession
Feb-2020 Mar-2020 –34.4% 1.1 –1.5 –0.8 –0.8 Recession
Nov-2021 Oct-2022 –26.0% 11.2 5.0 0.9 2.5 Stagflation
Mean –34.2% 12.2 –0.6 0.3 0.4
Median –31.4% 11.6 –0.6 0.6 0.6
Source: Bloomberg and authors’ calculations
that broader recession never happened. We label it stagflation, as high inflation was
an important characteristic of this bear market, which triggered the Fed hikes. 1966
was also based on stagflationary vibes, as those years saw the first inflation scare in the
post-war period, even though it was on a smaller scale than 2022. 1984 saw an aggres-
sive hiking cycle by Volcker, also due to rising inflation fears. We label the 1973–1974
episode recession, but it came with very high inflation too. Overall, the labels are not
always clear-cut, but the lesson is that while it is crucial to avoid recessions, other fac-
tors can lead to major downturns as well. Environments of high inflation and weak
growth can be very equity negative, even if a recession can be avoided. And the after-
math of bursting equity bubbles can see protracted bear markets. Financial market
accidents are the other problematic regime, but those can rarely ever be anticipated.
As we had already discussed in Chapter 3, the good news is that the equity market
is not overly forward-looking with respect to recessions. The bad news is that it is
very difficult to forecast a recession even shortly before the recession starts—partly
because the market is still close to the highs, and Wall Street feels like a happy place.

How to Trade Equities: A Framework 163
0%
–10%
–20%
–30%
–40%
–50%
nwodwarD
xaM
7591-tcO 2691-nuJ 6691-tcO 0791-yaM 4791-tcO 2891-guA 4891-luJ 7891-ceD 0991-tcO 8991-tcO 2002-tcO 9002-raM 0202-raM 2202-tcO )elbbub
gnitalfeD(
naideM
)tnedicca
laicnaniF(
naideM
)noisseceR(
naideM
)noitalfgatS(
naideM
Max Drawdown by Event and Median by Reason
FIGURE 8.3 Recession and deflating bubbles the worst regime.
Source: Bloomberg and authors’ calculations.
So what should investors do? As per Chapter 3, some promising indicators are the soft
data versus hard data indicator, even though the sample size is quite small. We also
commented on the yield curve and the long and varying lags between inversions and
recessions, as well as on disinversions and recessions. In the end, we think that when
any of these indicators suggests an increased probability of a recession, investors should
trade more carefully, for example, by taking breaks of the 200dma more seriously as
a risk management tool rather than necessarily reducing risk in a wholesale manner.
8.3 EQUITIES AND THE FED
The relationship between the Fed and equity markets is not obvious. A Fed cut itself
is a positive factor as it lowers the discount rate for future profits. However, if the Fed
cuts because of a coming recession, it often is not a sufficiently positive factor to detract
from the overall recession dynamic, even though a recession without Fed cuts would
likely be even worse. Given that it is not trivial to figure out whether a recession is
indeed coming or whether it is a soft landing, at least early on, we analyze the empirical
evidence. We focus here on the first and last cut, as well as the first and last hike, since
a change in the overall strategy of the Fed should be the most meaningful.
First, we study the median performance of equities around first Fed cuts. As illus-
trated in Figure 8.4, the SPX pulls back three months before the first cut, probably as
the first growth clouds appear, but then rallies into the cut the month before, likely
expecting Fed relief. It then chops around the unconditional performance line, before
eventually taking off again around two months later. The skew is to the downside, as
the moderately higher median is the result of cases where the economy was still in rel-
atively good shape at the time of the cut, and cases where the cuts were happening in

164 TRADING GLOBAL MACRO MARKETS
S&P 500 into first cut
15.0%
10.0%
5.0%
0.0%
–5.0%
median
–10.0% mean
–15.0%
–100 –75 –50 –25 0 25 50 75 100
FIGURE 8.4 US equity returns strong just before first cut.
Source: Bloomberg and authors’ calculations.
reaction to severe economic weakness, when market stress was starting to move sub-
stantially higher into very severe recessions.
When the Fed stops cutting, the opposite logic holds. Clearly, no more easing
by itself is equity negative. But if it is done because of strong growth, these effects
will likely outweigh the negative impact of the Fed’s action. We studied how the SPX
behaves around the last cut in Figure 8.5. We find that equities bottom around two
months before the last cut, then rally into the last cut, and, after a month of sideways
price action, do quite well again. The reason may be that it is often not fully clear
whether the last cut occurred or not. A month later, when the next Fed meeting occurs,
it becomes more obvious whether the last cut indeed has already occurred. The first
meeting when the Fed pauses is a better entry point to buy the dip in US equities than
the last cut, as by then less Fed stimulus is priced in.
If we focus on soft landings only, the number of sample points drastically
decreases. We would consider easing cycles beginning in July 1995 (driven by rising
US unemployment and falling inflation in the aftermath of an aggressive hiking cycle,
with the Tequila crisis possibly contributing), September 1998 (fallout from Russian
crisis and LTCM), and 2024 (inflation normalizing after an aggressive hiking cycle) as
easing cycles coinciding with soft landings, as there was no imminent recession. 1987
could be seen as a candidate, but we exclude it as the equity crash triggering the cut
was somewhat unique. Interestingly, all three soft landing cycles resulted in cumulative
Fed cuts of 75bp, clearly less than the average Fed cutting cycle. The duration of those
short cycles was not as uniform, though, ranging from two months in 1998 to seven
months in 1995. In those three episodes, US equity returns were mixed into the first
cut (driven by 1998, which was essentially financial market accidents). However, after

How to Trade Equities: A Framework 165
S&P 500 into last cut
30.0%
20.0%
10.0%
0.0%
–10.0% mean
median
–100 –75 –50 –25 0 25 50 75 100
FIGURE 8.5 Best entry point is in Fed meeting after last cut.
Source: Bloomberg and authors’ calculations.
S&P 500 into first cut (soft landing)
1995-07-06 2024-09-18
20.0% 1998-09-29 unconditional
15.0%
10.0%
5.0%
0.0%
–5.0%
–10.0%
–15.0%
–100 –50 0 50 100
FIGURE 8.6 Fed cuts into soft landings very equity market friendly.
the first cuts, the returns were very strong, as can be seen in Figure 8.6. Cuts without
a recession are the best-case outcome for equities.
What about the hiking side? Here, the same logic holds as during cuts. Although
hikes per se are obviously not a positive, if they are driven by strong growth, they

166 TRADING GLOBAL MACRO MARKETS
S&P 500 into first hike
15.0%
10.0%
5.0%
0.0%
–5.0%
mean
–10.0% median
–100 –75 –50 –25 0 25 50 75 100
FIGURE 8.7 SPX pulls back after first hike.
Source: Bloomberg and authors’ calculations.
are unlikely to end a bull market. Eventually, the Fed may well overtighten, hurt-
ing equities, but that is unlikely to be the case early in the hiking cycle. Still, as per
Figure 8.7 there is a pullback after the first hike, in the median case, worth around 5%,
which is quickly recovered. Interestingly, the skew is to the upside. Into the first hike,
there is no clear pattern, and the median performance is close to the unconditional
performance.
The same analysis for the last hike, and again starting in 1986, shows that equities
have done well following the last hike, after a brief period of indigestion, as can be seen
in Figure 8.8. In the 2023 episode, the equity market had rallied strongly into it but
then had a longer-lasting and deeper pullback than usual after the cut, before restarting
the bull market. The reason is likely that the Fed skipped a hike in June of 2023, before
squeezing in one last hike in July. This is highly unusual, and a pause so late in the cycle
is typically mistaken for the end of the cycle. Indeed, after the penultimate hike in
May, the SPX rallied strongly. Last hikes are generally bullish after just a few days of
indigestion.
Focusing on rates, rather than on Fed actions, we find that it is quite normal that, at
various points during the hiking cycle, the equity market becomes jittery when rates are
rising. Theoretically, rising rates due to higher inflation should be a bigger headwind
than higher rates that are more driven by higher growth (though higher inflation will
also be helpful to EPS growth, as EPS is a nominal number and, to some extent, price
pressures are passed through to the consumer). We study this question below. First, we
are interested in whether there is an absolute level of real rates that has historically been
problematic for equity markets. The answer to this question is illustrated in Figure 8.9,
where we split the level of 10-year real rates since the inception of the TIPS market
into quintiles. The results are somewhat mixed. The first observation is that every

How to Trade Equities: A Framework 167
S&P 500 into the last hike (1986 onward)
15.0%
10.0%
5.0%
0.0%
–5.0%
median
–10.0%
mean
–15.0%
–100 –75 –50 –25 0 25 50 75 100
FIGURE 8.8 SPX likes last hikes.
Source: Bloomberg and authors’ calculations.
10-year Real rates
–1.21 to 0.24 0.24 to 0.88 0.88 to 1.82 1.82 to 2.74 2.74 to 4.4
Return 4.30% 1.67% 1.85% 0.37% 0.23%
3.0 Volatility 9.06% 6.34% 8.59% 8.29% 10.44%
Risk/Reward 0.47 0.26 0.22 0.04 0.02
Max DD –29.66% –25.88% –29.69% –47.30% –53.94%
Active IR 1.06 0.59 0.48 0.10 0.05
% on 20.01% 20.00% 20.00% 19.98% 20.01%
2.0
1.0
0.9
0.8
–1.21 to 0.24 0.24 to 0.88 0.88 to 1.82 1.82 to 2.74 2.74 to 4.4
2000 2005 2010 2015 2020 2025
FIGURE 8.9 Real rates above 1.8% a yellow light.
Source: Bloomberg and authors’ calculations.
quintile has a positive active information ratio, though it is true that the ratio is lower,
the higher the real rates are, and it deteriorates quite sharply when real rates exceed
1.8%. However, even the worst quintile included very meaningful bull markets, and
the two worst quintiles are as negative as they are due to the aftermath of the Nasdaq

168 TRADING GLOBAL MACRO MARKETS
10-year Real rates 1m change
–1.05 to –0.16 –0.16 to –0.05 –0.05 to 0.02 0.02 to 0.14 0.14 to 1.35
Return 3.10% 2.00% –0.00% 3.46% –0.16%
Volatility 10.02% 7.78% 7.88% 7.76% 9.55%
Risk/Reward 0.31 0.26 –0.00 0.45 –0.02
Max DD –21.66% –38.43% –36.38% –29.48% –47.78%
2.0 Active IR 0.69 0.58 –0.00 1.00 –0.04
% on 20.00% 20.00% 19.99% 20.00% 20.00%
1.0
0.9
0.8
0.7 –1.05 to –0.16 –0.16 to –0.05 –0.05 to 0.02 0.02 to 0.14 0.14 to 1.35
2000 2005 2010 2015 2020 2025
FIGURE 8.10 Large real rates move higher a clear equity negative.
Source: Bloomberg and authors’ calculations.
bubble and the 2008 episode, respectively. We would therefore not make too much of
the danger level of 1.8%, setting our warning light at best to amber.
Second, we investigate changes in real rates, focusing on the 10-year point.
Changes are more highly correlated with equity performance but are, of course, not
known ex ante. Using the same split into quintiles, the top quintile, when real rates
increase by more than 14bp per month, is the worst performing and has a negative
active information ratio, as is shown in Figure 8.10. The only big rally in that bracket
is the sharp bounce back after the 2008 debacle. This move up in real rates back then
started from negative territory, with real rates only becoming positive in Q2 of 2013,
in the so-called “taper tantrum.” A move toward positive rates was not harmful to
the SPX (though, perhaps somewhat surprisingly, the SPX continued to ignore rising
real rates until late 2014, i.e., even after rates had already moved to more reasonable
levels). Since late 2014, sell-offs of more than 14bp per month have been relatively
consistently negative for US equities. Although this rule of thumb may not be overly
useful as those sell-offs are hard to anticipate, it is still helpful to know what type of
sell-off is required before we have to worry about equity risk.
What about the split between growth and inflation as a driver? Re-running the
study for one month changes in 10-year breakevens does not support the contention
that rising inflation expectations are significantly worse than rising real rates, as is
shown in Figure 8.11a. Here, all quintiles have positive active information ratios.
Again, the highest quintile has the lowest ratio, but performance in this quintile has
largely been positive since the end of the GFC in 2009 and is very slightly above the
performance for real rates in that quintile. Although there are differences for the other
quintiles, the overall conclusion from the study is that it is not that important whether
a big sell-off in rates is driven by real rates or break evens. We also re-run the same
exercise for the term premium, shown in Figure 8.11b. Here, we pick the Kim Wright

How to Trade Equities: A Framework 169
10-year Breakevens 1m change
–1.14 to –0.11 –0.11 to –0.03 –0.03 to 0.04 0.04 to 0.12 0.12 to 1.04
Return 2.37% 3.21% 1.10% 1.32% 0.16%
Volatility 12.92% 7.46% 6.63% 6.83% 7.90%
2.0 Risk/Reward 0.18 0.43 0.17 0.19 0.02
Max DD –48.04% –16.58% –25.45% –25.60% –52.69%
Active IR 0.41 0.96 0.37 0.43 0.05
% on 20.02% 19.99% 20.01% 19.98% 19.99%
1.0
0.9
0.8
0.7
0.6
–1.14 to –0.11 –0.11 to –0.03 –0.03 to 0.04 0.04 to 0.12 0.12 to 1.04
2000 2005 2010 2015 2020 2025
(a)
Kim-Wright term-premium 1m change
–0.62 to –0.11 –0.11 to –0.04 –0.04 to 0.02 0.02 to 0.1 0.1 to 0.57
3.0 Return 2.78% 3.28% 1.37% 2.27% –0.75%
Volatility 9.78% 7.97% 6.65% 7.39% 8.21%
Risk/Reward 0.28 0.41 0.21 0.31 –0.09
Max DD –26.87% –29.16% –29.95% –19.25% –55.20%
Active IR 0.64 0.92 0.46 0.69 –0.20
2.0 % on 20.03% 19.98% 19.99% 20.01% 20.00%
1.0
0.9
0.8
0.7
0.6 –0.62 to –0.11 –0.11 to –0.04 –0.04 to 0.02 0.02 to 0.1 0.1 to 0.57
1995 2000 2005 2010 2015 2020 2025
(b)
FIGURE 8.11 (a) Performance with rising break evens not that different from rising real rates.
(b) Large 1m term premia increases more equity negative.
Source: Bloomberg and authors’ calculations.
model, which incorporates survey data to improve the measurement of the term pre-
mium. We find that the top quintile of changes has a more meaningful negative active
information ratio than our previous two studies. A rise of more than 10bp in this mea-
sure of the term premium has resulted in a negative active information ratio of –0.20.
While a significant part of this result is due to the GFC period, this measure has started
to work well again since 2015.
Related to moves in term premia and real rates is what the curve is doing at the
same time. In this section, we analyze equity performance in bull and bear steepen-
ing environments. There are many ways to measure the behavior of the curve. In this

170 TRADING GLOBAL MACRO MARKETS
study, we use daily rolling 1m changes in both 2-year and 10-year US interest rates. If
the long-end yield is rising and rising by more than the short-end, we classify it as bear
steepening. If the short-end rises more, we label it bear flattening. We do the same for
bull (10-year rate falling) steepening or flattening. As usual, we lag the SPX returns by
one day to make it, in theory, tradable. As per Figure 8.12, bull flattening is the pre-
ferred environment, where the large majority of SPX gains accrue. The most negative
regime is bear flattening, which typically occurs during Fed hiking cycles. However,
the negative performance is really concentrated during only two episodes: the 1987
crash and the 2022 inflation-induced hiking cycle. Bear steepening is, somewhat sur-
prisingly, not as negative as widely believed.
We now turn the question of how rates impact equities on its head and ask whether
equity market sell-offs generate Fed cuts, i.e., whether the mythical “Fed put” exists
and how to find out where it sits. We do this by showing what pullback from the one-
year high in the SPX (reached on day zero in Figure 8.13a) is needed for the median
Fed Funds to drop around day zero. It turns out that the answer to this exercise is
25%. After a 25% drawdown from the one-year high, the Fed is cutting rates in the
median case. If we analyze episode by episode, Figure 8.13b illustrates that even a
20% drawdown usually is consistent with Fed cuts, though only if inflation is low.
This 20% number coincides with the view that many of the corrections that are 20%
or larger coincide with recessions, where the Fed cuts rates for other reasons than just
equity market weakness. During high inflation episodes (1973, 2022), hikes continue
for longer, which is why the median is a larger 25% drawdown. We would also note
that other market factors also play a role, and maybe an even bigger one than equities
per se. In particular, the Fed is very attuned to credit markets, liquidity conditions, and
any market malfunction. Although these often coincide with equity weakness, these
Bull Bull Bear Bear
steepening flattening steepening flattening
Return 1.63% 5.17% 1.96% –0.43%
Volatility 9.42% 9.41% 8.68% 7.25%
10 Risk/Reward 0.17 0.55 0.23 –0.06
Max DD –51.64% –27.17% –52.06% –59.03%
Active IR 0.38 0.99 0.44 –0.12
% on 20.59% 30.78% 25.91% 22.72%
8
6 Bull steepening
Bull flattening
Bear steepening
Bear flattening
4
2
0
1980 1985 1990 1995 2000 2005 2010 2015 2020
FIGURE 8.12 Bull flattening is the best environment.
Source: Bloomberg and authors’ calculations.

How to Trade Equities: A Framework 171
–3
–200
–20.0% May-74 Mar-01 Jul-08 Jul-02 Sep- J 2 u 2 n-22
Dec-73
–25.0%
Mar-20
–30.0%
Oct-87
–35.0%
–4 –3 –2 –1 0 1
tuc
dnuora
nwodwarD
Fed funds after 25% drawdowns (day =0)
2
1 median
0
–1
mean
–2
–150 –100 –50 0 50 100 150 200
(a)
0.0%
–5.0%
–10.0%
–15.0%
(b) Change in FF next 3m
FIGURE 8.13 (a) 25% drawdown needed for immediate Fed Put activation. (b) In low-inflation
environments 20% drawdown is often enough.
Source: Bloomberg and authors’ calculations.
factors can certainly incentivize the Fed to move earlier or later than our equity-centric
rule of thumb suggests.
8.4 EQUITIES AND EARNINGS
In our discussion about China and India, we highlighted that GDP is not necessarily a
good predictor of equity performance in a cross-sectional setting. The exceptions are
recessions, which are almost always equity negative, and extremely high growth of

172 TRADING GLOBAL MACRO MARKETS
60%
40%
20%
0%
–20%
β = 2.104
t-stat = 6.29
R2 = 0.1154
–40%
–5.0% 0.0% 5.0%
real GDP YoY
YoY
nruter
ssecxe
P&S
10.0%
FIGURE 8.14 US equity returns and GDP only correlated at extremes.
Source: Bloomberg and authors’ calculations.
more than 10%, which is often associated with a bounce back from a deep recession,
and which is very equity positive. But outside of the extremes, real GDP growth is not
overly correlated with equity performance. The equivalent correlation using nominal
GDP is insignificant. This is illustrated in Figure 8.14.
The analysis is more interesting once we take leads and lags into account.
Figure 8.15a shows the lead-lag relationship between nominal GDP changes and equi-
ties for up to eight quarters. We use the Shiller dataset and nominal GDP data from
1947 onward (starting later does not change the results). The bars are centered around
the contemporaneous relationship (zero lag), which is weak (0.02) and insignificant.
For negative lags, where a positive number would indicate GDP growth leads equity
returns, we find a negative correlation, i.e., low quarterly GDP growth portends higher
equity returns two quarters later. For the positive lags, i.e., equities leading GDP, we
see a positive relationship; high equity returns tend to mean higher GDP growth one
or two quarters in the future. With respect to earnings, we find a stronger contempora-
neous relationship with GDP, with a significant correlation coefficient of 0.125, as per
Figure 8.15b. And just like for equity returns, weak GDP leads to higher EPS growth
with a three to five quarter lag.
Earnings are highly correlated with equity performance. As would be expected,
equity prices are leading EPS. In Figure 8.16, we show the results of a regression of
excess equity returns, with various monthly lags, on earnings. The coincident beta
comes in at just over 0.1. The correlation is overall relatively high from zero to six
months, with the highest correlation being the two-month lag. The publication lag
would add to the lag, as earnings are only published a few weeks after the quarter end.
Again, equity prices are forward-looking by around one to two quarters. Interestingly,

How to Trade Equities: A Framework 173
0.2
0.1
0.0
–0.1
–8 –6 –4
0.10
0.05
0.00
–0.05
–0.10
–0.15
–0.20
noitalerroC
noitalerroC
Cross-correlation between S&P excess return QoQ and GDP QoQ
Peak correlation: 0.261 at lag 1
({Equity} leads {GDP})
–2 0 2 4 6 8
(a) Lag (negative = GDP QoQ leads, positive = S&P excess return QoQ leads)
Cross-correlation between EPS growth QoQ and GDP QoQ
Peak correlation: −0.199 at lag −4 (GDP QoQ leads EPS growth QoQ)
–8 –6 –4 –2 0 2 4 6 8
(b) Lag (negative = GDP QoQ leads, positive = EPS growth QoQ leads)
FIGURE 8.15 (a) High equity returns = higher future GDP growth. (b) Weak GDP means future
higher earnings growth.
Source: Bloomberg, shillerdata.com, and authors’ calculations.

174 TRADING GLOBAL MACRO MARKETS
0.125
0.100
0.075
0.050
0.025
0.000
–0.025
–0.050
–20 –15 –10 –5 0 5 10 15 20
noitalerroC
Cross-correlation between S&P excess return MoM and EPS growth MoM
Peak correlation: 0.139 at lag 2 (S&P excess return MoM leads EPS growth MoM)
Lag (negative = EPS growth MoM leads, positive = S&P excess return MoM leads)
FIGURE 8.16 US equities lead earnings by one to two quarters.
Source: Bloomberg and authors’ calculations.
at lags of more than one year, the relationship is negative, suggesting some of the price
increases in earnings tend to come from overoptimism.
When observing how equities behave during earnings season, i.e., whether they go
up or down on an earnings print, typically depends on whether the forward (full-year)
earnings estimates are raised by analysts in the aftermath of the earnings call. Earnings
estimates are, therefore, crucial to understanding the equity market.
There is a clear seasonal pattern when it comes to earnings estimates. We illustrate
this in Figure 8.17, using Citi’s earnings revision index (ERI). For the full year, earnings
revisions are typically falling slightly. For more details, see Manthey et al. (2025). On
a quarterly time frame, it is usually the case that earnings are revised lower during the
pre-reporting season, only to rise during the reporting season itself. This is because
corporates cut their estimates gradually going into the earnings call, lowering the bar. In
particular, in the last month of the quarter, negative warnings come in from companies,
where fundamentals deteriorated. On average, there are not enough positive warnings
to offset those, as corporates are less incentivized to get the good news out ahead of the
quarterly report. Therefore, earnings estimates typically move lower into the earnings
release, only to go up after earnings are announced, as more corporates beat than miss.
The key question is whether the ERI is useful in generating alpha in equity mar-
kets. We find that earnings revisions are both valuable as a trend indicator and as
a counter-indicator. In particular, buying equities when the earnings revisions break

How to Trade Equities: A Framework 175
0.25
0.00
–0.25
–0.50
–0.75
–1.00
–1.25
–1.50
1
naJ
morf
egnahC
evitalumuC
Seasonality of Earnings Revisions
Median
Mean
Reporting season
Pre-reporting
0 50 100 150 200 250 300 350
Day of Year
FIGURE 8.17 Earnings revisions lower in pre-reporting.
Source: Citi research and authors’ calculations.
4.0
3.0
2.0
1.0
0.9
0.8
0.7
0.6
0.5
0.4
2000 2005 2010 2015 2020 2025
1$
htworg
elacs
gol
S&P and Earnings Revisions
ERI > 0 ERI < 0 Buy & Hold GbI ERI > 0 GbI ERI < 0
Return 2.94% 4.20% 7.12% 4.95% 2.19%
Volatility 9.87% 16.66% 19.36% 9.05% 17.12%
Risk/Reward 0.30 0.25 0.37 0.55 0.13
Max DD –21.93% –55.74% –60.75% –16.28% –65.23%
Active IR 0.45 0.34 0.37 0.87 0.17
% on 43.81% 56.16% 100.00% 40.01% 59.96%
ERI > 0
ERI < 0
Buy & Hold
GbI ERI > 0
GbI ERI < 0
FIGURE 8.18 Positive ERI helpful, mostly by avoiding bear markets.
Source: Bloomberg, Citi research and authors’ calculations.
above zero is typically a good signal. The information ratio of equities with a positive
earnings revision index is higher than with a negative earnings revision index. Interest-
ingly, using global earnings revisions indices is superior to using US earnings revisions,
even for US equities. The ERI is adding alpha mostly by avoiding major bear markets
(2000, 2008). It also misses long bull markets, though, and would have kept investors
largely out of the market from 2012 to 2016! The details of the study are illustrated in
Figure 8.18.

176 TRADING GLOBAL MACRO MARKETS
12.00
9.0
8.0
7.00
6.0
5.0
4.00
3.0
2.00
1.00 0.9 0.8
0.70
0.6
0.5
0.4
0.30
2000 2005
1$
htworg
elacs
gol
S&P and Earnings Revisions and 200d MA
ERI +ve E or R 2 I 0 + 0 v d e E & R 2 I 0 – 0 v d e Buy & Hold
Return 4.95% 7.05% 0.22% 7.11%
Volatility 9.05% 11.62% 15.30% 19.36%
Risk/Reward 0.55 0.61 0.01 0.37
Max DD –16.28% –19.15% –66.07% –60.75%
Active IR 0.87 0.71 0.03 0.37
% on 40.02% 73.80% 25.03% 100.00%
ERI +ve or 200d
ERI +ve
Buy & Hold
ERI –ve & 200d
2010 2015 2020 2025
FIGURE 8.19 Using ERI in combination with 200dma.
Source: Bloomberg, Citi research and authors’ calculations.
We therefore also investigate how the ERI interacts with the 200dma in
Figure 8.19. We find that the active information ratio is higher for positive global ERI
only, rather than for a strategy that goes long if either the ERI is positive, or the mar-
ket is above its 200dma. Having said that, the total return is better if we implement the
either-or condition. Interestingly, insisting on both conditions on the downside (ERI
negative and SPX below its 200dma) has a worse active information ratio than only a
negative ERI and results in lower (but still slightly positive) returns. We would there-
fore use the ERI as a trend signal only if it is in line with the 200dma.
Interestingly, the ERI can also be a countersignal if the ERI is too oversold. As per
Figure 8.20, the ERI is highly correlated with forward EPS estimates. Given that it is a
breadth measure, it tends to move early but is also more volatile. We found that buying
the market when the ERI is depressed is a superior countersignal to buying the market
when the forward EPS is depressed.
In Figure 8.21, we show that buying the SPX when the global ERI is moving into
the fifth lowest percentile is a good strategy. This is true for short holding periods of
one month and for longer holding periods up to 12 months, where the active IR is still
meaningfully higher than the unconditional one. This ERI indicator mostly buys after
meaningful pull-backs in equities, given that equities react to lower earnings expec-
tations. Sometimes the rule triggers too early, as in the deflating 2000 bubble or the
2008 crisis, and sometimes the trigger is close to perfect, occurring very close to the
actual bottom of the market. It is interesting that such a simple rule, which is only in
the market 32% of the time, comes relatively close in terms of total returns. This rule
is likely just one example of a rule that buys a pull-back and holds it for one year. Our
findings have a major caveat, though. Because our data only starts in 2000, i.e., right
at the start of a major bear market, we cannot use an expanding window and instead
use the full sample ERI for this exercise, something that we typically avoid like the
plague. Here, it means that the model is unreliable as it essentially incorporates future

How to Trade Equities: A Framework 177
0.6
0.4
0.2
0.0
–0.2
–0.4
–0.6
–0.8
)AM
w4(
xednI
IRE
SU
5.0%
0.0%
–5.0%
–10.0%
–15.0%
2000 2004 2008 2012 2016 2020 2024
egnahc
m1
SPE
dwf
raey-1
US ERI vs. S&P 1-year fwd EPS 1m chg
US ERI 4w MA
1-year fwd EPS 1m change (right)
FIGURE 8.20 A depressed ERI is a buying signal.
Source: Bloomberg, Citi research and authors’ calculations.
S&P when Earnings Revisions are extreme
ERI <5th 22d Hold 66d Hold 126d Hold 252d Hold Buy & Hold
Return 1.59% 2.24% 2.75% 4.16% 5.93% 7.30%
Volatility 9.37% 9.99% 10.66% 11.50% 13.07% 19.34%
Risk/Reward 0.17 0.22 0.26 0.36 0.45 0.38
Max DD –38.57% –39.77% –43.68% –40.79% –45.01% –60.75%
Active IR 0.76 0.82 0.73 0.83 0.80 0.38
% on 4.97% 7.57% 12.69% 19.09% 32.26% 100.00%
252d Hold
126d Hold
100 66d Hold
22d Hold
ERI <5th
Buy & Hold
2005 2010 2015 2020 2025
FIGURE 8.21 ERI as a counter indicator.
Source: Bloomberg, Citi research and authors’ calculations.
information. However, with both 2008 and 2020 now in the data, we imagine that
going forward, the parameters should be more stable.
Using the ERI as a counter-indicator also works well internationally for most mar-
kets. This is in part true due to the high positive correlation of the various equity
markets. The strategy works best for Asia x Japan and EM. For the United Kingdom

178 TRADING GLOBAL MACRO MARKETS
0.75
0.50
0.25
0.00
eprahS
evitcA
1.50
1.25
1.00
0.5
0.0
eprahS
evitcA
2.0
1.5
1.0
ASU eporuE KU napaJ napaJ
xe
aisA
ME
Long when Local ERI < 5th percentile
ERI <5th ERI <5th 126d hold
ERI <5th 22d hold ERI <5th 252d hold
ERI <5th Buy & Hold
66d hold
Long when Global ERI < 5th percentile
ERI <5th ERI <5th 126d hold
ERI <5th 22d hold ERI <5th 252d hold
ERI <5th 66d hold Buy & Hold
ASU eporuE KU napaJ napaJ
xe
aisA
ME
(a)
(b)
FIGURE 8.22 (a) ERI works as counter-indicator across regions. (b) Global revisions work
better than local ERIs.
Source: Bloomberg, Citi research and authors’ calculations.
and Japan, it largely depends on the holding period, but it works in most cases, as per
Figure 8.22a. Once more, the global ERI works better than the local one, as can be
seen in Figure 8.22b, probably because some regions do not have sufficient breadth of
analyst coverage. Overall, this is evidence that the global business cycle may be more
important for many equity markets than the local one. The same important caveat that
we mentioned for the United States also applies here: we use the full sample ERI.

How to Trade Equities: A Framework 179
Another interesting question is how much information there is in the price action
on earnings day. That stock prices have follow-through after the price action on the
date of the earnings release was documented in the early 1980s by Rendleman et al.
(1982), who found that stocks with the highest positive earnings surprises continue
to outperform the market, while those with the highest negative earnings surprises
continue to underperform. The most likely reason for this effect is behavioral biases,
like conservatism, where investors just find it difficult to bid up a stock by too much on
the basis of one strong quarter. Possibly, investors underestimate the autocorrelation
of earnings, which is significant. Some may be hoping for a pull-back in a given stock
after a large jump higher, but if this pull-back never comes, they may be forced to chase
the stock higher regardless. The effect is larger for small caps, suggesting that liquidity
and trading costs may also play a role. However, there is some evidence that the extent
of the post-earnings drift has been falling over time. A related question is whether
there is any information about the trading behavior of the aggregate index depending
on how well the earnings season went, as measured by equities gapping higher after
earnings results. We have, sadly, not been able to find a profitable rule that uses the
aggregate outcome of the earnings season to trade SPX. While this remains an ongoing
research project, for now, it appears that earnings drift is more easily expressed on a
single stock basis.
8.5 EQUITIES AND LIQUIDITY
In the context of macro-trading, liquidity means the availability of cash and cash-like
instruments in a sufficient quantity to facilitate economic activity and to meet short-
term obligations. Liquidity is a very important concept for equity markets. It is no
coincidence that before financial innovation made monetary aggregates less reliable,
major central banks like the Bundesbank were targeting monetary aggregates. More
recently, during the GFC in 2008, when central banks attempted to enhance mone-
tary policy with quantitative easing (QE) and later by tightening (QT), liquidity made
a comeback as a factor driving markets. Liquidity provided by the Fed is the key
globally, even as other central banks have also been engaged in that game. We first
loosely demonstrate the relevance of global liquidity for equities. This is achieved by
Figure 8.23, which plots one-year changes of global USD reserves at the important
central banks next to a detrended version of the SPX. The fit is surprisingly good
for such a simple approach, as frequently discussed by Matt King (see, for example,
King, 2023).
Next, we investigate the Fed balance sheet in more detail. The liability side of
the Fed balance sheet basically consists of bank reserves, the checking account of the
Treasury (Treasury General Account, TGA), the reverse repos, where money market
funds keep balances at the Fed, and the currency in circulation. Interestingly, when
investigating the various components of the Fed balance sheet, it turns out that the
change of the overall balance sheet does not have a strong relationship with either
risky assets or with US Treasuries. This is the case even on a coincident basis, not
just in terms of using the balance sheet to forecast asset performance. Investigating
the subcomponents, we find that bank reserves are the part of the Fed’s balance sheet

180 TRADING GLOBAL MACRO MARKETS
2500 20.0%
Total
2000 15.0%
EUR Securities,
Swiss, UK $ Reserves
1500
10.0%
1000
5.0%
500
0.0%
0
–5.0%
–500 CNY $ Reserves JPY $
Reserves –10.0%
USD $ Reserves
–1000
–15.0%
–1500
2011 2013 2015 2017
Start Date
egnahc
nb$
AM
d002
ved
005
P&S
Deviation of the SPX
from the 200dma
2019 2021 2023
FIGURE 8.23 Global liquidity correlated with risky assets.
Source: Bloomberg and authors’ calculations.
that is most reliably correlated with market performance. This is true not only on a
coincident basis, which requires forecasting the behavior of bank reserves to generate
trading rules, but also on a forward-looking basis. Both reverse repos and TGA have
very little to do with equity returns.
This is illustrated in Figure 8.24, where we use the four-week moving average of
weekly changes in bank reserves to forecast weekly returns for the SPX, bonds, and
DXY. Long SPX after the four-week ma is positive, has an information ratio of just
above 1, while it is roughly zero following a negative reading. US bonds also trade bet-
ter following rising reserves, even though the improvement is not as stark, probably
due to the bid that can result from weak equities. Following rising bank reserves, US
bonds have an information ratio of 0.61, compared to 0.22 when falling. The diver-
gence between the two return streams has mostly occurred since the bear market of
2022. For the USD, the difference is similarly stark as in the case for equities and quite
consistent: When reserves are falling, the active IR to be long DXY is 0.84, compared
to –0.18 in the opposite case. Falling reserves suggest a USD shortage, and rising risk
aversion may also be supportive for the USD, in most cases.
8.6 EQUITIES AND BUBBLES
Bubbles can and do occur in any asset class. However, nothing captures the imagina-
tion of the investing public more than a bubble in equities. Clearly, bond yields close to
zero or even negative could also qualify as bubbles, but an ever-rising equity market is

How to Trade Equities: A Framework 181
DXY Index DXY Index S&P 500 S&P 500 US 10-year Bond US 10-year
Res. down Res. up Res. down Res. up Res. down Bond Res. up
Return 2.91% –0.76% 0.04% 10.55% 0.56% 1.98%
7 Volatility 5.07% 5.81% 11.55% 14.41% 3.75% 4.43%
Risk/Reward 0.57 –0.13 0.00 0.73 0.15 0.45
6
Max DD –9.81% –28.04% –35.16% –38.19% –21.16% –10.04%
5 Active IR 0.84 –0.18 0.01 1.01 0.22 0.61
% on 46.54% 53.46% 46.42% 53.46% 46.42% 53.46%
4
3 DXY Index Res. down S&P 500 Res. up
DXY Index Res. up US 10-year Bond Res. down
S&P 500 Res. down US 10-year Bond Res. up
2
1
0.9
0.8
0.7
0.6
2010 2012 2014 2016 2018 2020 2022 2024
FIGURE 8.24 Global liquidity helps with timing.
Source: Bloomberg and authors’ calculations.
without doubt more fascinating. We therefore study bubbles in an equity market con-
text. In terms of defining a bubble, we lean on the work of Jeremy Grantham at GMO
(see Grantham, 2021), who suggested that a bubble is something where prices rise by
more than two standard deviations above the long-term real trend, as illustrated in
Figure 8.25. The alternative would be to define bubbles with valuations moving above
the two standard deviation real trend, as not every large move in prices is necessarily
a bubble. However, the price-based approach also picks up a bubble in fundamentals.
What tends to happen is that bubbles usually have an underlying economic reason,
which is often linked to some scarce resource. This was bandwidth during the internet
revolution of the 1990s and is advanced computing power at the time of writing dur-
ing the AI revolution. Scarcity and perceived scarcity lead to double and triple ordering
and inflated prices for the goods in question, resulting in inflated earnings projections.
This can lead to a bubble in earnings, and as a result, a purely valuation-based frame-
work may not capture that. We therefore use the price-based GMO approach for bub-
ble detection, but we certainly use valuation as an additional tool to understand how
long the bubble may continue. In terms of exiting the bubble, we use a dual condi-
tion of either the market falling by 15% from the peak or exiting the two-standard-
deviation condition, as we have previously discussed at Citi (see Willer et al., 2024e).
The reason for the twofold condition is that after a 15% drop, we are getting close to
what investors label a bear market. At times when the SPX is close to entering a bear
market, we clearly have left bubble territory, even if the two-standard deviation rule
should not have triggered yet.
Using these rules, we find nine bubbles in the SPX, starting with the first one in
1929, and with the last two linked to the current AI-driven bubble (interrupted by
liberation day), as can be seen in Figure 8.26. The internet bubble, peaking in 2000, also
shows up as two bubbles, interrupted by the EM and LTCM crisis of 1998. The first
observation is that, after entering bubble territory (Figure 8.25), bubbles continued to

182 TRADING GLOBAL MACRO MARKETS
9
Long-term trend real price
real price index
8
Bubble enter
Bubble exit
7
6
5
Deviation of price from long-term trend
2.5
0.0
–2.5
resid
1919 1944 1969 1994 2019
FIGURE 8.25 Bubble blown: at time of writing we were in bubble territory.
Source: Bloomberg and authors’ calculations.
expand for quite some time. For example, the second leg of the internet bubble started
in November 1998 and then lasted for more than 470 trading days, i.e., longer than
a year, as per Figure 8.26. The only exception was September 1929, when the market
turned down in very short order. This is likely the case, as 1929 was probably used as
the episode to determine how to define a bubble. The trading rule is therefore not to sell
equities when they enter bubble territory but to buy them. Some of the most explosive
returns occur after the bubble warnings go off. Selling a bubble becomes safer after
the exit of the bubble (shown as dotted red lines in the chart). Given how difficult it
is to find any condition where the SPX reliably sells off, we find it noteworthy that in
almost all the cases that our rule identified as bubbles, the large majority of the full
rally that happened after entering bubble territory was eventually reversed, either while
still in bubble territory or afterward. The only exception was 1958, when the market
just went sideways for a prolonged time. This suggests to us that our bubble definition
captures an important phenomenon.
As our bubble framework is not overly helpful in calling for a peak, the question
is what to focus on to know that a peak is close. Fed hikes are typically part and parcel
of a bubble, and eventually, those rate hikes contribute to the market’s demise. It is
very rare that the Fed eases into a bubble that is already extended. During the second
leg of the internet bubble, the Fed hiked by 175bp, accelerating the pace of hikes at
the end of the cycle. True, in 1998, the Fed cut rates in response to the Asian crisis
that had spilled over into Russia and LTCM. But it took a crisis to get us there, and,
according to our definition, we had already left bubble territory given the severe fall in
equity markets at that time. Overall, we would treat an aggressive Fed hiking cycle as

How to Trade Equities: A Framework 183
1.6
1.4
Current bubble
1.2
1.0
Liberation day
cleanse
0.8
0.6
0.4
0.2
1929-Sep to 1929-Dec 1998-Nov to 2001-Nov
1958-Feb to 1959-Nov 2020-Oct to 2022-Jun
0.0 1961-May to 1962-Jul 2023-Jun to 2025-Apr
1964-Feb to 1966-Jul 2025-May to Oct 25 (time of writing)
1997-Jul to 1998-Jun
–0.2
0 200 400 600 800 1000
FIGURE 8.26 Bubbles reverse.
Source: Bloomberg and authors’ calculations.
an early warning sign for an expanding bubble. Hikes have often been necessary but
by no means sufficient to bring a bubble to an end. Other warning signs include falling
liquidity (discussed later in the context of the 2000 episode), and extreme sentiment,
for example, proxied by the individual investor bull-bear survey, which became very
extreme in late 1999, as is shown in Figure 8.27.
Further signs of “peak bubble” have also been discussed by Ray Dalio (see Dalio,
2021) He has suggested screening for a high participation of retail investors (retail net
purchases as percent of market capitalization), extended IPO activity (as percentage
of GDP), and, very importantly, the use of leverage to finance equity positions (US
household margin debt as percentage of GDP). As is often the case in markets, greed
triggers the use of leverage. Without leverage, the risks of a bubble bursting are often
not as extreme, as investors typically do not get forced out of positions unless they
use leverage. Google trend searches with respect to the bubble narrative of the day
can also help, though they suffer from the problem that there is no sufficiently long
time series that gives a sense of just how extreme this indicator could become before
peaking. In Figures 8.28a and b, we show margin leverage and IPOs as a percentage of
market capitalization. It is not that obvious at what levels these measures of exuberance
typically peak. But a quick move higher seems to be a condition that makes it more
likely that we are in the late phase of a bubble.
One additional timing tool for the top of the bubble may be that the “generals”
have to fail, where the generals are the large-cap stocks that drive most of the gains in
a sharply narrowing market. This is somewhat speculative, as the analysis is grounded

184 TRADING GLOBAL MACRO MARKETS
Jul-97 to Jun-98
60 Nov-98 to Sep-00
Nov-22 to Mar-24 Dec 99
y
e
ur v 40
s
ar
e
b
ull-
20
b
or
st
e
v
n
al i 0
u
d
vi
di
n
I
–20
0 20 40 60 80
FIGURE 8.27 Peak bubble also means sentiment bubble.
Source: Bloomberg and authors’ calculations.
very much in the specifics of the 2024 bull market, dominated by the Mag7. Although
we can easily make comparisons to the 2000 bubble, a larger sample that can be for-
mally backtested is harder to come by. Still, as the concept makes sense to us, we want
to mention it here in the hope that history rhymes sufficiently going forward. The anal-
ysis is based on Willer et al. (2024f). Going into the 2000 peak, the seven largest cap
stocks that drove the index higher were Microsoft, Cisco, GE, Walmart, Intel, Nokia,
and Pfizer. Interestingly, Microsoft is the only company from the 2000 peak that made
it into the Mag7. Furthermore, it is noteworthy that in 2000, the top stocks were less
tech-heavy, which could make an eventual tech bust more problematic for SPX perfor-
mance this time around than it was in 2000. For the sake of this study, we measure
generals as “failing” when they break below their 200dma, and to reduce noise, we
require them to stay there for at least five days. In 2000, it took three of the seven gen-
erals to put the bull market on notice, but four had to fall below the 200dma to call
conclusively for the end of the bull market, as is shown in Figure 8.29.
Given that the “generals rule” is a tool for risk management during bubbles, we
backtest this rule during our bubble periods only, but added one year after bubble exit,
to make sure we capture deflating bubbles at least partially in the study, unless the SPX
made it back above the 200dma faster than that. We find that the best information
ratio is achieved if investors cut equity risk when the fourth general falls below its
200dma. This rule results in the information ratio moving from 0.67 (unconditional)
to 1.04. For the case where four or more generals have fallen below their 200dmas, the
information ratio is –0.6. This is superior to using the 200dma as a risk management
tool on the SPX (which also leads to improvements). This is illustrated in Figure 8.30.
Of course, there are also false positives. Still, if in a bubble, we think it pays to have

How to Trade Equities: A Framework 185
3.50%
Lines are market tops
3.25%
3.00%
2.75%
2.50%
2.25%
2.00%
1.75%
1.50%
1999 2004 2009 2014
Year-Month
0.06%
0.05%
0.04%
0.03%
0.02%
0.01%
0.00%
1994 1999 2004 2009 2014 2019 2024
Date
ARNIF
secnalaB
tibeD
AMM21
paC
tkM
%
sa
OPI
2019 2024
(a)
(b)
FIGURE 8.28 (a) Rising margin debt as a warning signal. (b) Rising IPOs a less reliable sign of
exuberance.
Source: Bloomberg and authors’ calculations.
an aggressive risk management, as downside risks are elevated. We therefore take the
“generals” rule seriously during bubble times.
The “generals rule” is a highly specific version of market breadth. More broadly,
market breadth indicators require that more equities are rising than falling. Typically,
falling breadth is seen as a negative for markets, as market advances carried by only
a few stocks are seen as vulnerable. However, we do not find breadth overly use-
ful for timing reversals. In Figure 8.31a, we can see that most often low breadth is
happening at market bottoms, while high breadth happens during various points of a

186 TRADING GLOBAL MACRO MARKETS
7
SPX Index
6
1400
5
1200 4
3
No. of 7 generals
1000 above 200dMA (right) 2
1
800
0
Jan Jul Jan Jul Jan Jul Jul
1999 2000 2001
Start Date
xednI
P&S
AM
d002
evoba
slareneg
#
Jan
2002
FIGURE 8.29 It takes four generals to fail.
Source: Bloomberg and authors’ calculations.
S&P > 200d S&P < 200d S&P <=4 Gen S&P >4 Gen G S e & n P < < 2 = 0 4 0d
3.5
Return 3.15% 0.04% –0.89% 4.07% –1.02%
Volatility 7.57% 5.99% 5.66% 7.82% 5.37%
3.0 Risk/Reward 0.42 0.01 –0.16 0.52 –0.19
Max DD –29.08% –36.87% –36.49% –19.63% –34.88%
Active IR 0.84 0.02 –0.62 1.04 –0.86
2.5 % on 24.60% 6.69% 6.30% 24.98% 4.89%
S&P >4 Gen
2.0
S&P > 200d
1.5
S&P < 200d
S&P <=4 Gen S&P <=4 Gen < 200d
1.0
2000 2005 2010 2015 2020 2025
FIGURE 8.30 Generals rule performed well in 2000.
Source: Bloomberg and authors’ calculations.
bull market. Just glancing at the chart suggests that there have been episodes where
breadth deteriorated well ahead of a market top. We look at those tops in more detail in
Figure 8.31b.
Of the major tops over the last 25 years, the only top with a fairly weak breadth
was 2000. However, it is important to point out that breadth had been narrowing for a
long time before that bubble eventually popped. Also, interestingly, breadth had started

How to Trade Equities: A Framework 187
40
20
0
AM
d002
evoba
P&S
%
100
80
60
103
1992 1996 2000 2004 2008 2012 2016 2020 2024
xednI
005
P&S
SPX Index
S&P 500 Index (log scale)
40
20
0
d002
evoba
srebmem
XPS
%
(a)
Breadth around market tops
2000-03-24 2015-07-20
80 2007-10-11 2018-09-20
2020-02-19 2022-01-03
60
(b) –100 –75 –50 –25 0 25 50 75 100
FIGURE 8.31 (a) Poor breadth at a market top is rare. (b) But not easy to use breadth to time
market top.
Source: Bloomberg and authors’ calculations.
to improve (from very low levels) about a month before the market peak. The second
worst breadth was going into the 2007 top, but again, breadth had actually improved
into the top, this time for two months. Overall, we do not find breadth overly helpful,
even though breadth on par with the 2000 extremes may be worthwhile to take more
seriously, understanding that a sample size of one will never make the concept overly
compelling.

188 TRADING GLOBAL MACRO MARKETS
The Mother of All Bubbles
The internet bubble of the late 1990s was a time of intense speculation and
investment in internet-based companies. Fueled by the widespread adoption of
the internet and the emergence of online businesses, investors poured money into
startups, many of which lacked viable business models and sustainable (or at
times any) revenues. The Fed was broadly leaning against the expansion of the
bubble by hiking aggressively. However, in the last quarter of 1999, the Fed did
ramp up the supply of liquidity, mostly to counter fears of the Y2K bug. The
underlying concern was that computer systems would fail to correctly process
dates beyond December 31, 1999, as many programs were representing four-digit
years with only the final two digits. Given fears that IT failures cause havoc in
markets, the Fed increased its balance sheet by 19% in the last quarter of 1999,
the largest increase on record at that time, which was only bested subsequently
during the 2008 GFC and the 2020 COVID crisis. Adding so much oil to the
fire unsurprisingly led to the Nasdaq having its best quarter ever, up 53% in Q4
of 1999, further helped in early 2000 by the fact that the Y2K bug came and
went without major hiccups, as corporates had invested in patches ahead of time.
When the Fed started to pull back that liquidity aggressively after the first of Jan-
uary, the NDX peaked a few months later at the end of March, at a trailing PE
of around 200. This episode is illustrated in Figure 8.32. Interestingly, the SPX,
which initially sold off with the NDX, recovered by September 2000 almost to its
level in late March, partly as the Fed had concluded its hiking cycle in the after-
math of the April sell-off. But the NDX did not come even close to the March
levels, and with such underperformance of the previous leaders, the writing was
on the wall for the market more broadly. By August, it had become very clear
that the bursting tech bubble would pull both tech companies and the overall
economy lower, and the manufacturing ISM quickly fell below 50. In Novem-
ber, the CEO of HPQ, Carly Fiorina, suggested on an earnings call that “the
lights went out” in answering an analyst question on how the quarter was going.
By that time, fundamentals had clearly deteriorated, which was much less obvi-
ous at the time of the market peak. This is also interesting. Equities are not that
forward-looking. The time between the equity peak and a peak in fundamentals,
proxied by semiconductor sales, was only seven months (though we would note
that there is a lot of reflexivity at work: the falling share prices contributed to
semi sales peaking out). Subsequently, both NDX and SPX continued to fall as
the bubble deflated until October 2002. We use the 2000 episode frequently to
compare other bubbles to it. However, we note that it is not guaranteed that the
next bubble will come close in size or sheer craziness, as the 2000 episode was
very extreme, even by bubble standards. To our mind, the 2000 episode is there-
fore more a ceiling of where valuations can go, rather than a great analog to use
for the average bubble.

How to Trade Equities: A Framework 189
4500
0.15
4000
3500
0.10
3000
2500 0.05
2000
1500 0.00
1000
–0.05
1998 1999 2000
xednI
qadsaN
YoY Fed bank
reserves (right)
Nasdaq
sevreser
knab
deF
ni
htworg
YoY
2001 2002
FIGURE 8.32 Last leg in NDX was liquidity driven.
Source: Bloomberg and authors’ calculations.
8.7 VALUATION NOT VERY VALUABLE
Coming fresh from a discussion of bubbles, we now generalize the discussion of val-
uation and whether it is useful for equity trading. The short answer is that valuation
is barely working: traditional market timing measures based on valuation have not
generated alpha for the last 20 years. We start investigating valuation with a focus on
the CAPE ratio. In Campbell and Shiller (1998), the authors use cyclically adjusted
P/E ratios by taking a moving average of earnings over long time periods to adjust for
the vagaries of the business cycle. They also adjust for inflation. Figure 8.33a shows
the CAPE over time. Scatter plots of CAPE levels versus 10-year real forward returns
show a clear correlation, as per Figure 8.33b, but are difficult to operationalize into
an effective trading tool in real time, as we show next.
We use Professor Shiller’s data to perform a backtest using the following rule: we
calculate the CAPE yield (1/CAPE) and size our position based on the rolling 30-year
percentile of that yield. In particular, we move the position size to 50% when the yield
is in the lowest percentile and to 150% when it is in the highest. In theory, the average
and median exposure should be fully invested, and we therefore compare the strategy
to the excess returns (which are leverage-agnostic) of a buy-and-hold strategy. We show
results from 1950 to avoid the war periods, though the precise starting point makes
little difference to the results. The results are shown in Figure 8.34. It turns out that
our version of the CAPE model underperforms not only in terms of actual returns but
also with respect to the information ratio. If we modify the CAPE ratio to be seven
years instead of the standard ten, we find a small benefit, in terms of the information

190 TRADING GLOBAL MACRO MARKETS
45
CAPE
CAPE 10-year mean
40
35
30
25
20
15
10
5
(a) 1894 1919 1944 1969 1994 2019
20.0%
CAPE vs. 10-year real returns
CAPE vs. 10-year real returns 2000 onward
15.0%
10.0%
5.0%
0.0%
–5.0%
5 10 15 20 25
(b) Starting CAPE ratio
nruter
ytiuqe
laer
raey-01
30 35 40 45
FIGURE 8.33 (a) CAPE levels may have moved structurally higher. (b) CAPE negatively
correlated with future long run returns.
Source: Bloomberg, shillerdata.com, and authors’ calculations.
ratio, but returns still lag the buy-and-hold strategy. This is because investors would
tend to be under-invested as the CAPE ratio has moved upward over time. This can be
clearly seen in Figure 8.33a. Ever since the 2008 financial crisis, markets have barely
traded below the rolling 10-year average. For the strategy we test, this means that the
rule is on average only 85% invested, instead of the expected 100%.
There have been extensions of the original work on CAPE, and some researchers
have employed different earnings measures (see Siegel, 2016), though this has only

How to Trade Equities: A Framework 191
CAPE yield Buy & Hold
Return 5.68% 6.44%
Volatility 12.08% 12.30%
Risk/Reward 0.47 0.52
Max DD –53.53% –53.27%
Buy & Hold
101
CAPE yield
100
1959 1969 1979 1989 1999 2009 2019
FIGURE 8.34 Using CAPE underperformed buy-and-hold.
Source: Bloomberg, shillerdata.com, and authors’ calculations.
resulted in marginal improvements. Overall, conventional wisdom remains that struc-
tural changes over long horizons make valuation difficult to use (see also Asness et al.,
2017).
8.8 WINNERS KEEP WINNING
Just like valuation, momentum is also an intuitively attractive strategy for equities.
After all, a bull market can lead to a virtuous cycle. Higher stock prices generate a
wealth effect and also higher CEO confidence, leading to better economic growth out-
comes, and therefore to higher earnings, reinforcing the equity bullishness. In our expe-
rience, investors tend to self-select themselves into a more valuation-centric or more
momentum-centric investment style. Although the two strategies are not necessarily the
opposite of each other and most investors take both aspects into account, it typically
makes a big difference whether investors put a bigger weight on changes (momentum)
or levels (including valuation).
We are unashamedly favoring momentum, mostly because momentum is perform-
ing better in our backtests. For a fair comparison, we use the same methodology that
we used for valuation. In particular, we use the x-month return as our momentum
variable and invest 150% when it is above the 50th percentile and only 50% when it
is below. Figure 8.35 shows that this methodology outperforms buy and hold in terms
of both the information ratio and the absolute returns. This is the case for all shorter
horizon momentum measures (3 months, 6 months, and 12 months), and only gets
weaker for a very long one (84 months). The best version is the one using 3-month and
6-month returns, which is 5% overinvested over the backtested period.

192 TRADING GLOBAL MACRO MARKETS
MoM 3 MoM 6 MoM 12 MoM 84 Buy & Hold
Return 8.08% 7.91% 7.30% 6.97% 6.44%
Volatility 11.69% 11.42% 11.59% 12.27% 12.30%
Risk/Reward 0.69 0.69 0.63 0.57 0.52
Max DD –40.03% –36.84% –35.28% –55.16% –53.27%
102
101
MoM 3 MoM 84
MoM 6 Buy & Hold
100 MoM 12
1959 1969 1979 1989 1999 2009 2019
FIGURE 8.35 Momentum has outperformed buy-and-hold.
Source: Bloomberg and authors’ calculations.
MoM 6M CAPE 7-year Cheap Mom
8.0 Return 1.41% 0.39% 2.13%
7.0 Volatility 5.08% 11.06% 4.27%
Risk/Reward 0.28 0.04 0.50
6.0
Max DD –15.95% –72.78% –19.14%
5.0 Active IR 0.80 0.06 1.51
% on 12.56% 35.48% 12.73%
4.0
3.0
2.0
1.0
0.9
0.8
0.7 MoM 6M
0.6 CAPE 7-year
Cheap Mom
0.5
1929 1939 1949 1959 1969 1979 1989 1999 2009 2019
FIGURE 8.36 Extreme momo beats extreme valuation.
Source: Bloomberg, shillerdata.com, and authors’ calculations.
For the tactical trader, momentum very frequently trumps valuation. In
Figure 8.36, we use a very long monthly history to test trading momentum and val-
uation at the extremes. In particular, we only trade the top and bottom percentiles,
positioning for mean reversion with respect to valuation, and for trend following with
respect to very strong or weak momentum. As can be seen in Figure 8.36, the value
strategy leads to shorting bubbles, which can inflate much longer than a macro man-
ager can stay solvent. Buying strength, on the other hand, has been rewarded. Of
course, having both value and momentum in your favor is the sort of A-trade that can

How to Trade Equities: A Framework 193
Above 200d Below 200d Buy & Hold
Return 6.28% 1.31% 7.55%
Volatility 10.96% 13.25% 17.19%
Risk/Reward 0.57 0.10 0.44
Max DD –32.60% –60.56% –60.75%
Active IR 0.69 0.18 0.44
% on 69.23% 30.76% 100.00%
101
Buy & Hold
Above 200d
Below 200d
100
1980 1990 2000 2010 2020
FIGURE 8.37 Using a simple 200d MA avoids the worst drawdowns.
Source: Bloomberg and authors’ calculations.
build generational wealth. Unfortunately, this seems to happen only once a genera-
tion. We see a strong active Sharpe of around 1.5 if both momentum and value signals
are above the 50th percentile at the same time, but it happens only 13% of times and
occurs only every 20 years or so. The last event happened in the aftermath of the GFC.
Another strategy, which is broadly in line with momentum, is using moving aver-
ages, which many CTA models are based on. We found much use over the years in the
200d MA. Although it can be frustrating whenever the market is gyrating around its
200d MA, giving many false alarms, respecting 200d MA makes sure that investors are
on the right side of the market. Using the 200d MA for the SPX significantly improves
the information ratio from 0.44 to 0.69, as per Figure 8.37. Although the total return
is slightly less, the maximum drawdown is around half. The 200d moving average
basically works by avoiding very nasty tail events. We always caution against the buy-
and-hold strategy, even if it has higher returns. The reason is that very few investors
are able to truly endure large drawdowns. Bear markets end when almost every mar-
ket participant has given up on the market and sold, and investors who do not even-
tually throw in the towel are very rare. The best reason to stop out when the market
breaks the 200dma is that it prevents investors from stopping out at even lower lev-
els. If investors are comfortable with a 17% volatility that the SPX has to offer, they
should just respect the 200d MA and lever up the SPX by 55% whenever the SPX is
above the 200d MA.
8.9 SMALL, NOT OFTEN BEAUTIFUL
Although this book does not go into detail on sectors, we do want to investigate small
caps, partly because there has been much written about the so-called small-cap effect.
This effect was first documented in the early 1980s (for example, Banz, 1981, and later

194 TRADING GLOBAL MACRO MARKETS
Fama and French, 1992b) and posits that small-cap stocks generate higher returns,
although often with higher volatility. The fundamental underpinnings for small-cap
outperformance are that small caps have more room for growth, allowing them to
expand more quickly. The limited analyst coverage and resulting lower market effi-
ciency are also mentioned as a possible reason for the effect. Additionally, small caps
may need to incorporate a higher risk premium due to the higher volatility, which is
because small caps are more sensitive to the economic cycle, have less diversified rev-
enue streams, and may have more difficulties accessing capital during market down-
turns, which can raise the default rate. Lower liquidity, resulting in higher transaction
costs, may also have contributed.
However, time has not been kind to the small-cap effect, as can be seen in
Figure 8.38. The all-time peak of the Russell 2000 over the SPX occurred in July of
1983, not too long after the original Banz study. Small caps then underperformed by
a total of almost 50% into the recession of the early 1990s. While the post-recession
recovery was sharp, the relative performance made new lows during the tech bubble
of the second half of the 1990s, troughing around 60% off the peak in early 1999
(interestingly, almost one year ahead of the peak of the Nasdaq bubble, maybe because
the Nasdaq bubble of the late 1990s also had small caps being swept up in it). Still,
the bursting tech bubble was broadly positive for small-cap outperformance, largely
because the recession it generated was very mild. These patterns have continued since
then. The 2008 GFC led to small-cap underperformance, followed by a recovery, and
the same was true for the COVID recession. Since March 2021, small caps have under-
performed again, with a new tech bubble forming. This suggests that small-cap outper-
formance requires two ingredients: a positive economic cycle, preferably coming out
of a US recession, and/or a deflating tech bubble.
To operationalize this trading rule, we check how small caps relative to the SPX
perform when the Manufacturing ISM is below 50, but above its 3mm, to find episodes
Ratio of Russell 2000 / S&P 500 total return indices
0.40
Small caps
underperform
0.35
0.30
0.25
Small caps
0.20 outperform
0.15
0.10
1980 1985 1990 1995 2000 2005 2010 2015 2020 2025
FIGURE 8.38 Small caps hate recessions and tech bubbles.
Source: Bloomberg and authors’ calculations.

How to Trade Equities: A Framework 195
SPX Index
1.25%
RTY Index
1.00%
0.75%
0.50%
0.25%
0.00%
nruteR
ylhtnoM
egarevA
05<
IMP
05>
IMP
gnillaf
&
05<
gnisir
&
05<
gnillaf
&
05>
gnisir
&
05>
FIGURE 8.39 Small caps do well exiting recessions.
Source: Bloomberg and authors’ calculations.
when the economy comes out of recession. Figure 8.39 shows that RTY mostly out-
performs when the PMI is below 50 and rising (i.e., above its 3mma). It also outper-
forms somewhat when the PMI is above 50, and rising, but much less so. With the
PMI below 50 it does much worse, driven by the regime of PMI below 50 and falling.
This pattern is consistent with what we find in credit: coming out of the recession, it
pays to buy “junk,” i.e., the lower-rated credits. Information ratios of trading this pat-
tern are quite weak, though, maybe because the framework does not take bubbles into
account, which are often large-cap bubbles.
We therefore also investigate how RTY/SPX trades in relation to recent bubbles.
Given that the most recent bubbles were tech-driven (which is probably more a feature
than a bug), we investigate what happens when the Nasdaq is well above its 200dma. In
particular, we use a deviation above the 85th percentile as a simple indicator of bubbly
conditions in the tech-heavy index. Figure 8.40 shows the results. Small caps on average
outperform when the NDX is in the bottom 15th percentile (which also captures some
of the post-recession periods) and underperform when it is in the top 85th percentile,
i.e., when the bubble is getting extreme. Having said that, more recently, small caps
have not done well even when NDX was relatively weak.
8.10 SUMMARY
US equities have had a tremendous long-term performance, with a Sharpe ratio since
1926 using monthly data of 0.51. The default position, therefore, has to be long. How-
ever, drawdowns have been relatively frequent, with the ones above 20% often linked
to recessions, but also to deflating bubbles, stagflationary episodes, and financial acci-
dents. We discuss the interaction of the equity market with the Fed and find that equi-
ties rally shortly before the first cut. They also rally into and after the last cut. They

196 TRADING GLOBAL MACRO MARKETS
Nasdaq Nasdaq SPX vs.
well above well below Russell
200d MA 200d MA 200
3.5 Return –1.90% 0.95% 1.51%
Volatility 4.67% 5.80% 10.92%
Risk/Reward –0.41 0.16 0.14
Max DD –61.65% –33.01% –61.52%
3.0 Active IR –1.04 0.44 0.14
% on 15.27% 13.94% 100.00%
2.5
Nasdaq well below 200d MA
2.0
1.5
SPX vs. Russell 200
1.0
Nasdaq well above 200d MA
0.5
1980 1985 1990 1995 2000 2005 2010 2015 2020 2025
Start Date
FIGURE 8.40 Small caps dislike bubbles.
Source: Bloomberg and authors’ calculations.
underperform in the aftermath of the first hike and rally strongly in the aftermath of
the last hike. The level of rates is not strongly related to equity markets, but large
increases in the term premium are negative. The Fed put, on average, gets triggered
around 25% off the highs of the equity market. On the growth side, equities are lead-
ing GDP by around two quarters. Using EPS, the coincident effect is larger, but there
are also strong leading patterns for the next two quarters. We study earnings revisions
(ERIs) and find that very negative revisions are a strong buy signal, but outside of
excessive downgrades, US equities trade much better when the ERI is positive. On the
liquidity side, we find a positive correlation with the change in bank reserves on the
Fed balance sheet, one week forward. We also share some thoughts on equity bubbles:
how to spot them and how to trade them. We demonstrate that momentum is a better
strategy than value.