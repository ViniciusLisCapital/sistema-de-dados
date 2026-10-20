2
CHAPTER
Global Macro Rules
Global macro-trading traces its roots to the 1970s, when the collapse of Bretton
Woods and the rise of floating exchange rates created a fertile ground for cross-
border speculation. More recently, macro-trading benefited from the rise in volatility
on the back of the Asian financial crisis, the Great Financial Crisis (GFC), and the
COVID pandemic. This chapter outlines the more recent performance of macro funds
and makes the case for a profitable future.
2.1 LONG-TERM PERFORMANCE OF MACRO FUNDS IS STRONG
Macro funds have recently made a comeback, both in terms of returns but also in terms
of mind share among asset allocators. Although this has been partly a function of the
rise of the pod aggregators, which successfully dampen volatility for their investors, it
was also helped by what happened in 2022. That year saw a rise in inflation, which
decimated long only 60–40 portfolios. Although inflation has been in retreat since then,
we think there is a more durable case to be made for the return of macro investing into
the limelight.
In Figure 2.1, we analyze returns of macro hedge funds from 1997 to mid-2025.
We use BarclayHedge as our source, which may underestimate returns, as some of
the largest and most successful funds have not been included in the index due to data
availability. For the whole period, annual geometric returns were 6.8%, less than the
S&P returns of 9.4%. Returns have been strong before and during the financial crisis,
but then were more meager for a period, before accelerating again in the aftermath
of COVID. Adjusting for volatility, macro hedge funds have outperformed, though,
clocking in a risk/reward of 1.23 (which is calculated as annualized returns over volatil-
ity), compared to the S&P at 0.65. Given that managers typically invest excess cash
in Treasuries, we also calculate the excess performance over T-bills, analogous to a
Sharpe ratio. The macro hedge fund index comes in at 0.83 versus S&P at 0.51 over
the same period. Given that macro manager returns can generally be levered up, this
Sharpe ratio is in many ways more meaningful for asset allocators than returns.
7

8 TRADING GLOBAL MACRO MARKETS
Macro HF
Returns
6 × 100 Return 6.82%
Volatility 5.55%
Risk/Reward 1.23
Max DD –8.07%
4 × 100
3 × 100
Macro HF Returns
2 × 100
QE1 QE2QE3
100
1999 2004 2009 2014 2019 2024
FIGURE 2.1 Macro hedge fund returns strong outside of QE.
Source: BarclayHedge.com and authors’ calculations.
2.2 HOW DO MACRO FUNDS MAKE MONEY?
Before setting out to show various frameworks to macro traders, it is important to
understand how macro hedge funds make their money. To this end, we regress macro
fund returns on the various asset classes (equities, bonds, commodities, and DXY), as
well as on Barclay’s commodity trading advisor (CTA) index. CTAs are, in some sense,
the original macro hedge funds and typically employ mostly trend-following strategies.
This is illustrated in Figure 2.2. We find that the various asset classes and CTA variable
explain between 5% and 95% of returns (the R2 of a rolling 18m regression), with the
average running at 70%. The only beta that is reasonably stable is that for the CTA
index, which is, as expected, almost always positive and explains, on average, 20% of
the macro hedge fund returns. The equity factor swings between positive and negative,
suggesting that hedge funds really do hedge, in the sense that they do position for bear
markets. The average explanatory power of equities for the overall returns is 36% in
univariate regressions. Bonds, surprisingly, given that many of these funds were created
by what were originally fixed income and FX traders, are less important for macro
hedge funds in a directional sense, with an average R2 of 8%. Given that we are using
a monthly dataset, it may also be the case that traders are trading rates more tactically
than the regressions can pick up. As with equities, the beta swings from positive to
negative, as macro hedge funds can and do position for bear markets in bonds. FX
exposure is even more tactical; the absolute exposure to FX (using the DXY index) is
low over the full sample. In fact, it is the only asset class with an insignificant coefficient
when estimated over the total 1997 to 2024 period, but it is highly time-varying. The
average absolute t-statistic for rolling periods comes in above 2. Commodities add to
returns in a similar fashion and tend to be traded from the long side.
Going forward, there are several reasons to remain optimistic on the asset class.

Global Macro Rules 9
1.00 S&P 500 BarclayHedge CTA Index
US 7–10-year bond DXY Index
0.75
s BBG Commodities
n
ur
0.50
et
F
r
0.25
H
a
of
0.00
et
b –0.25
–0.50
1999 2004 2009 2014 2019 2024
1.0
0.5
r-squared
1999 2004 2009 2014 2019 2024
FIGURE 2.2 Hedge fund returns mostly explained by a blend of the big four asset classes and
more than a dash of CTA returns.
Source: Barclayhedge.com, Bloomberg, and authors’ calculations.
2.3 A BRIGHT FUTURE 1: EQUITIES ARE EXPENSIVE
During powerful equity bull markets, macro investing typically takes a back seat, as
it is quite rare that macro managers outperform the SPX in a raging bull market.
Even though the SPX is rarely an explicit benchmark for any macro fund, implicitly,
investors only have limited patience for multi-year underperformance versus equity
markets. Fortunately, for macro investors, at the time of writing, equities are relatively
expensive, suggesting subpar returns in the long term. This can be seen by focusing
on the cyclically adjusted price earnings (CAPE) ratio, popularized by Campbell and
Shiller (1988), which is currently very elevated. To be precise, the current reading is
not that different from the peak we have seen during the last days of the dot.com bub-
ble. Expected future long-term returns are typically negative when the ratio is close to
these extreme levels. This is illustrated in Figures 2.3a and b, which shows the CAPE
ratio and subsequent 10-year real excess returns (calculated, as per Shiller’s methodol-
ogy, subtracting 10Y bond returns from the S&P and adjusting both for inflation and
T-bill returns). Although it is difficult to use this ratio as a real-time market timing tool,
partly because we may still be in the middle of a powerful AI bubble (more on this
later), eventually markets are likely to reverse (see also Asness et al., 2015), suggesting
a positive operating environment for macro traders over the next decade.
To go one step further, we also investigate the beta of the BarclayHedge index to the
SPX. We find a positive, but relatively small beta of 0.17 in our monthly data sample.
Furthermore, there is some evidence that global macro funds tend to have positive
convexity. Macro hedge funds tend to perform much better, in relative terms, at times
when equities are falling, as shown in Figure 2.4 (though they may also not be able
to keep up with very strong equity returns on the right-hand side of the distribution).
Using the Barclay index data is likely underestimating this effect, as anecdotally, many
macro hedge funds have made their mark during bear markets.

10 TRADING GLOBAL MACRO MARKETS
10.0 β = –0.3x + 0.1
R2 = 0.193 7.5
5.0
2.5
1880 5 10 15 20 25 30 35 40 45
CAPE
dleiy
EPAC
snruter
ssecxe
laer
raey-01
snruter
ssecxe
laer
raey-01
20.0 20 0.20
10-year real excess 17.5 returns (RHS) 15 0.15
15.0 0.10 10
12.5
5 0.05
0 0.00
–5 –0.05
1/CAPE ratio –10 –0.10
1900 1920 1940 1960 1980 2000 2020
(a) (b)
FIGURE 2.3 (a) High valuations today mean lower equity returns over the long term.
(b) Current CAPE levels are associated with negative long-term equity returns.
Source: Bloomberg and authors’ calculations.
8.0%
6.0%
4.0%
2.0%
Cubic Fit
0.0%
–2.0%
Quadratic Fit
–4.0%
–20.0% –15.0% –10.0% –5.0% 0.0%
S&P return
nruter
FH
orcaM
5.0% 10.0% 15.0%
FIGURE 2.4 Hedge funds have a positive beta to equities but outperform on a relative basis
when equities decline source Barclay.
Source: Bloomberg, BarclayHedge.com, and authors’ calculations.
2.4 A BRIGHT FUTURE 2: VOLATILITY RISES DURING QT
The macro strategy tends to do well during periods of high volatility. The lack of
dispersion in interest rates and suppression of volatility in the quantitative easing
(QE) period led to a lack of opportunity, given that short-term fixed income and FX
trading is a staple of macro investing. Figure 2.5 shows the impact of QE on the
rolling annual return of macro hedge funds. The average in the post-GFC period,
which brought QE to the forefront, was markedly lower than pre-financial crisis.

Global Macro Rules 11
1e6
5
4
3
5.0% 2
0.0%
1
–5.0%
1996
snruter
FH
orcaM
m21
gnilloR
stessa
latot
teehS
ecnalaB
deF
Rolling 12m HF returns Macro HF 2009–2019
Fed Balance Sheet Macro HF 2020–
Macro HF 1997–2008
20.0%
15.0%
10.0%
2000 2004 2008 2012 2016 2020 2024
FIGURE 2.5 Hedge fund returns were lower in the post-GFC period of QE and anchored
short-term rates.
Source: Bloomberg, BarclayHedge, and authors’ calculations.
Quantitative tightening (QT) then coincided with the volatility from the COVID shock
to lead to better returns again. We expect that the current episode of QT (or at least
absence of QE) will again be helpful for the returns of macro hedge funds.
2.5 A BRIGHT FUTURE 3: RATES BETS WITH HIGHEST SHARPE RATIO
AND MORE PROFITABLE WITH RATES SUBSTANTIALLY ABOVE ZERO
Rates are typically an area where macro fixed-income measures can gain alpha. When
short rates were pinned to zero or below in the aftermath of the financial crisis, and
back ends were depressed by QE, there was less opportunity for fixed-income trading.
This is illustrated in Figure 2.6, where we use a simple trend-following strategy to proxy
hedge fund returns by asset class. To be precise, the strategy goes long or short based
on the 200d MA across asset classes, and positions are volatility adjusted. Each asset
class strategy is adjusted to target 10% ex ante volatility. Fixed-income has delivered
the strongest risk-adjusted returns over time but has not been as profitable when US
rates were glued to zero.
2.6 A BRIGHT FUTURE 4: PERFORMANCE CUSHION FROM NON-ZERO
SOFR
Global macro investors typically use leverage to gain exposure to investment themes
and global markets. Futures and swaps are liquid and cheap to trade, and margin
requirements are a fraction of the market exposure gained. This capital efficiency
means that many managers will maintain relatively large allocations to cash-like

12 TRADING GLOBAL MACRO MARKETS
Trend Trend Trend 200d
200d equity 200d Bonds Commods Trend 200d FX
Return 1.91% 4.61% 5.74% 4.65%
Volatility 10.85% 8.80% 10.87% 11.22%
Risk/Reward 0.18 0.52 0.53 0.41
10.0 Max DD –30.20% –38.92% –31.48% –28.79%
9
8
7
6
Trend 200d Commods
5
4
Trend 200d Bonds
3
2 Trend 200d FX
ZIRP Period
Trend 200d equity
1.0
1
1
1990 1995 2000 2005 2010 2015 2020 2025
FIGURE 2.6 Rates trend-following struggled in zero rates period.
Source: Bloomberg and authors’ calculations.
8.0%
6.0%
4.0%
2.0%
0.0%
US 3m t-bill level
snruter
FH
orcaM
.a.p
%
egarevA
)2.6
,9.4(
)9.4
,7.3(
)7.3
,5.2(
)5.2
,2.1(
)2.1
,400.0(
12.0%
10.0%
FIGURE 2.7 Hedge funds returns are higher at higher cash rates.
Source: Bloomberg, BarclayHedge.com, and authors’ calculations.
instruments and will earn higher returns from these balances when short rates are
high. Figure 2.7 illustrates this regularity by plotting the average returns (annualized)
by quintile of short-term US T-bill yields. At the highest quintiles (close to levels seen
today but more often observed in the 1990s), average annualized returns were over

Global Macro Rules 13
12% compared to the post-GFC period of zero rates, low macroeconomic volatility,
and barely 2% annualized macro fund returns. The effect may be compounded by two
other aspects. First, higher rates typically do not stay high for long, and macro funds
often are able to benefit from a period of high but falling rates. Second, there is a nexus
between risk-taking abilities and T-bill yields. When T-bills are high, the income from
T-bills can be used to leverage macro bets. After all, it can be very difficult to be an
aggressive trader when in a drawdown, and to the extent that higher T-bill income
can cushion drawdowns, it is helpful for keeping risk appetite high. Of course, not all
hedge funds are judged against the zero line, and some may be judged against T-bill
returns, which makes the last point moot for that subset of funds. But it is typically
good to be a hedge fund when returns on cash are high.
2.7 A NOTE ON PROCESS AND DOES HISTORY REALLY RHYME?
The basic methodology of the book is to analyze economic history. This can be event
studies that analyze past events and circumstances and apply them to the new events
in question. Or it can be an investigation of which financial factors have historically
worked in which macro regimes. The implicit assumption is that developments will
unfold in a similar way to how they always have. The key criticism is, of course, that
the future is the future, and lessons from the past may be somewhat limited, maybe
especially in financial markets, where rewards for learning from past mistakes can be
exorbitant. We acknowledge that there are limitations to the historical analysis, as
history rarely repeats itself (despite allegedly rhyming). Still, in our minds, a thorough
study of the past is crucial to building an adaptable framework to be ready for the
challenges of the future.
This is true for several reasons. First, there is a tendency for analysts, especially
specialists in one particular asset class, to adopt an “every time is different” view,
based on the specific circumstances and their deep knowledge of the nuances of a given
situation. This sometimes misses the forest for the trees. The second point, eloquently
made by Kahneman (2011), is that we often neglect to get our priors right. We may
mistakenly think that a person we know to be a Greenpeace activist is more likely to
be a librarian than to work in finance, even though in the United States, 9 million
people work in finance, compared to less than 150,000 in libraries. At the very least,
the frameworks we lay out in this book will help to get the priors right, which must be
the right starting point to explore what could be different this time around. Lastly, there
is no alternative. As Yogi Berra observed, “It is tough to make predictions, especially
about the future,” which, by the way, was another case of history rhyming, as Nils
Bohr had said something to this effect much earlier, possibly himself rehashing an old
Danish proverb. Maybe there is nothing new under the sun, after all. While the future
is the future, humans are humans, and many human biases, like overconfidence or a
recency bias, for example, will likely remain in play in human history in general, as
well as in financial markets in particular.
Furthermore, we often focus on the relationship of one variable with one or two
other variables. Of course, in reality, processes are much more complex, and there
may be many instances of omitted variables at play. Still, we find that even simple

14 TRADING GLOBAL MACRO MARKETS
frameworks can be quite useful because the market is typically only trading two or
three stories at a time, and for short periods, it is often the case that there is just one
factor at play. While one of the authors can rightfully call himself a quant, this book
is not overly quantitative. Our backtests do not necessarily have to be statistically
significant, and we are willing to live with small samples. As long as results are in line
with economic logic and make sense intuitively, we are willing to run with them.
In summary, while the inherent difficulty of forecasting will not stop people from
making predictions, we should be modest with respect to our own forecasting abilities.
Therefore, a lot of our work focuses on establishing the base-rate or typical path,
or expected path under common circumstances. Once established, useful analysis can
be done on why this time may be different or segmenting the previous history to a
specific scenario or circumstance. We found in our own trading that having a strong
framework increases the ability to withstand drawdowns. Trades based on predictions
without a framework will lead to second-guessing of the predictions much faster, and
often as quickly as prices start moving against the view. We hope that this book will
help readers create strong frameworks for their macro-trade.
2.8 WHAT IS GOOD PERFORMANCE?
Throughout most of this book, we analyze returns as excess returns over cash (typ-
ically US T-bills). This enables comparison across different periods of time with dif-
ferent inflation and cash rates and, in certain periods, approximates real returns, as
higher inflation episodes usually have higher T-Bill rates. It also has the benefit of repli-
cating the return available to a leveraged macro-investor who, via swaps, futures, or
other derivatives, implicitly or explicitly (through repos) finances positions at close to
the risk-free short-end rate. In addition, we typically analyze investments through the
lens of the information ratio, i.e., the ratio of the excess return on an investment (or
strategy) to its volatility (which is very similar to the Sharpe ratio). There are many
criticisms and alternative measures to assess performance, but none have been able to
replace the Sharpe ratio. To our mind, the Sharpe ratio is a simple and efficient mea-
sure of the relative attractiveness of an investment using leverage, and we continue to
use it as a first-order measure to compare performance. Of course, the path of returns
matters, as do the timing, depth, and duration of drawdowns and (conditional) cor-
relations with other asset classes. Lo (2002) describes useful adjustments to account
for various non-normal statistical properties such as skew and kurtosis. In our expe-
rience, implementing these modifications makes little difference in practical applica-
tions. López de Prado et al. (2025) provide several extensions for conducting formal
statistical inference and correcting for multiple tests. In any case, a simple timeseries
plot of cumulative performance gives a much richer starting point to investigate the
properties and relative attractiveness of a strategy. We rely heavily on intuition and
economic priors and tend to use consistent parametrization (55d moving averages fea-
ture prominently for example) to avoid some of these pitfalls. This book will show
many such simulated return series. For some strategies that have relatively short hold-
ing periods, we often report active information ratios. Active means that they are only
calculated for the time period when the strategy has an active position. Lastly, our

Global Macro Rules 15
purpose is to build frameworks to generate insights on how to think about a given
asset in a given circumstance. We do not aim to provide off-the-shelf trading strate-
gies per se. We therefore typically do not adjust for transaction costs. We also do not
formally distinguish in and out-of-sample periods. But we have been using many of
the strategies for many years, which implies that the more recent decades are approxi-
mating an out-of-sample test. Still, we do expect that some of the strategies will break
down going forward, and we hope to still spend many years researching, fine-tuning,
and, yes, discarding the various frameworks in this book. History rules, but flexibility
dominates.
2.9 SUMMARY
This chapter makes the case for macro-trading. From the late 1990s, macro hedge
funds have had a strong information ratio of 1.23. After a period of worse-than-usual
performance during the QE and low-interest rate years, returns have recently started
to improve again. We expect that to continue, as volatility should remain high with
QE firmly in the rearview mirror. Furthermore, rates well above zero also favor the
macro strategy, with short-term interest rate trading being an important contributor to
PNL. In relative terms, the fact that US equities are expensive positions macro-trading
well for the medium term. The chapter closes with some remarks on the methodologies
applied.