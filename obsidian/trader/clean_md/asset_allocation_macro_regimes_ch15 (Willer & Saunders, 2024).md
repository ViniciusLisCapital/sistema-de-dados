15
CHAPTER
How to Allocate
Having studied the most relevant public asset markets individually, we now want
to share an overarching framework for asset allocation across macro-regimes, fol-
lowed by views on how to put it all together in a portfolio.
15.1 A REGIME INVESTING APPROACH
Regime investing has gained popularity and increased prominence in recent years. The
prevailing wisdom over the great moderation period from the early 1980s to the late
1990s was to implement a 60/40 portfolio of equities and bonds, as declining macroe-
conomic volatility and inflation helped both equities and bonds to deliver positive
returns, which were negatively correlated when it mattered most, i.e., when stocks
sold off into recessions. However, the perception that policymakers had acquired the
necessary tools to dampen the impact of such economic shocks was mostly a pipe
dream. The financial crisis of 2008, subsequent European sovereign debt concerns, and
the global pandemic provided clear evidence that macro volatility had not been tamed.
On the contrary, investors quickly discovered the important insights of the economist
Hyman Minsky, who suggested that in a financial market (and financial crisis) context,
stability breeds instability. Not only had macro volatility not been tamed, but maybe
it was structurally not possible to tame it, as investors react to a perception of reduced
risk by increasing leverage. One innovation that improved on the 60/40 model was risk
parity, which allocates risk based on volatility rather than with fixed weights. Those
models beat 60/40 as the use of leverage allowed for larger bond positions, which pro-
tected investors better during the GFC. However, both 60/40 and risk-parity portfolios
had ignored the lessons of the stagflationary 1970s and were therefore not suitable for
the inflation episodes post-COVID. This was the latest reminder that it is quite crucial
to identify the relevant macro-regime.
Early approaches to regime investing tended to fall into two camps. The first
emphasizes simple discrete classification, usually using the level of growth and infla-
tion to arrive at four distinct states of the world. This has the benefit of clear economic
intuition, but ignores the uncertainty and potential for transition to a different regime.
This can be seen in Figure 15.1, which shows monthly observations of this standard
approach split into quadrants. When growth or inflation is close to the long-term trend
level, the precise categorization of a period in a specific regime at times is somewhat
337

338 TRADING GLOBAL MACRO MARKETS
2
0
–2
–4
Apr-20
–6
–3 –2
z-score of CPI
htworg
cimonoce
gnidael
erocs-z
srotacidni
Oct-72 Nov-72
Aug-72 Dec-72 Apr-21 Dec-97Jan-98 Sep-72 Jul-21 May-21
Feb-98 Jun-21
Mar-98 Nov-21
Dec-08 May-20 Oct-08
Nov-08
–1 0 1 2 3 4
FIGURE 15.1 Regimes using only inflation and growth can result in arbitrary regime clustering.
Source: Bloomberg, Citi research, and authors’ calculations.
random and can just depend on a rounding error. In addition, in this framework, it
is very difficult to generalize beyond just growth and inflation, which misses other
important dimensions of the macroeconomic environment. The second approach is
very statistical and data-intensive, using hidden Markov models to detect regimes and
transition probabilities. These models can lose intuition on which regimes are being
detected and can struggle to estimate out-of-sample or across training windows.
The limitation of the quadrant approach also becomes evident in recession peri-
ods. Contrary to economic intuition, both equities and bonds (and credit) have similar
above-average Sharpe ratios in times when both inflation and growth are below aver-
age. The reason for this counterintuitive result is that the levels of growth and infla-
tion do not fully characterize the macro environment. Recessions come in two distinct
phases. The first is “early recession” or the contraction phase, when growth is below
average and weakening, resulting in a classic risk-off, when bonds outperform equi-
ties. Secondly, there is also a late recession or recovery phase, when risk assets have
already sold off and central banks are stimulating. Here, markets are forward-looking
and can see the light at the end of the tunnel. These tend to be a very strong environ-
ment for equity and credit investments. The simple rule to capture these effects is to
split recessions into early and late, by checking if growth indicators are above or below
their 3mma. The main findings are illustrated in Figure 15.2 across asset classes, where
all data start in the early 1970s except the EM indices, which start in 1988 for equities
and 1993 for sovereign bonds (shown for illustrative purposes). The returns are not
FX hedged due to data availability, even though we usually prefer to separate FX and
asset performance.
Late recessions are the best macro regime for equities, which is also unsurprisingly
true for credit. More risky markets like EM do better than their developed counter-
parts. Overall, the worst macro regime for risky assets is early recession, although for
US equities, stagflation is even worse. Early recession is where the 60/40 allocation

How to Allocate 339
oitar
eprahS
2.5
Overheat Recession
Goldilocks Recession Early
2.0
Stagflation Recession Late
1.5
1.0
0.5
0.0
–0.5
–1.0
SPX Bonds Credit Commodity DXY EAFE EM EM
USD USD Bond Equity
FIGURE 15.2 Equities do well in recessions but only after they have posted significant declines.
Source: Bloomberg, Citi research, and authors’ calculations.
comes in, because bonds have their strongest returns in that regime before it peters out
in the late recession regime. As mentioned earlier, stagflation (weaker than average
growth, higher than average inflation) is the other regime equities struggle with, as do
other asset classes. We will discuss this case in more detail later. During the overheating
regime (higher growth, higher inflation than average), commodities do the best, and
EM markets also tend to outperform. During Goldilocks (higher than normal growth,
with lower than normal inflation), equities perform the best once more, and interna-
tional equities outperform the United States as the dollar tends to weaken. Regimes
clearly matter for macro returns.
15.1.1 A Playbook for the Future
Given the limitations listed earlier, our preferred approach is to characterize the
macroeconomic environment using a wider range of variables drawn from asset pric-
ing theory, following the early work of Rosemary Macedo and published in Saunders
and Willer (2021). We use statistical tools to take a broader approach, effectively ask-
ing the question, which periods in the past are most relevant to determining the likely
forward returns for asset classes (or factors, sectors, or strategies). Effectively, this
jointly estimates the regimes, their characteristics, and transition probabilities, which
are embedded in forward returns from the most comparable starting points in history.
We use the nearest-neighbor algorithm to answer this question and gain insight into
the forward-looking implications of current macroeconomic readings. Thus, we can
incorporate additional relevant macro drivers without losing the economic intuition
from regime investing.
Figure 15.3 illustrates the approach. The top panel shows four of the seven vari-
ables we think are important for characterizing the macro-investing environment.

340 TRADING GLOBAL MACRO MARKETS
)%(
yadot
ot
ssenesolC
erocs-z
elbairav
orcaM
5
0
zCPI zFin conditions
–5 zLEI zRisk Appetite
4.0%
2.0%
0.0%
1979 1984 1989 1994 1999 2004 2009 2014 2019 2024
FIGURE 15.3 Playbook for the future. Which periods look like today?
Source: Bloomberg, Citi research, and authors’ calculations.
Growth and inflation levels, financial conditions, and risk appetites (proxied by
implied or realized volatility). We also incorporate changes in growth, inflation, and
financial conditions as variables likely to affect either expected cash flows or investor
discount rates. The bottom panel shows the weights on the most similar periods in
September 2025, where we have picked Five years (60 months) of data. The macro-
environment as of September 2025 had inflation below 10-year averages after a surge,
growth close to trend, financial conditions loose, and volatility subdued. This rhymes
with 1976 to 1977 (easy monetary policies, eventually leading to higher inflation), the
mid-1980s, and the 2010 to 2012 jobless recovery. Generally, those were positive envi-
ronments for equities, and that has played out at the time of writing.
15.1.2 If You Like It, Then You Better Put a Label on It
The nearest-neighbor approach is effective but is not always easy to interpret in terms
of standard economic theory. There is also a need for scenario analysis and to generate
asset class expectations based on economists’ or portfolio managers’ forecasts of the
future regime rather than just the data at hand. In response, we developed a clustering
approach in Saunders et al. (2024a), based on the cross-correlations of our macroeco-
nomic variables. This enables us to classify the recession quadrant effectively, and we
find that the approach gives a richer mapping than the discrete quadrant classifications.
We use a k-Means clustering algorithm and find 10 macro environment clusters that
follow a natural 80/20 rule. Eighty percent of the data fall into common clusters,
and these map well to intuitive definitions. The other 20% are risk or unusual

How to Allocate 341
Macro Regime Clusters
Normal (n=124) –0.08 0.38 –0.19 0.03 –1.02 –0.59 –0.04
Recovery (n=84) –1.08 –0.23 –0.18 0.16 –1.46 –1.37 –0.02
Goldilocks (n=94) –0.96 0.82 0.21 0.19 0.18 –0.1 0.06
Growth shock (n=53) 0.58 –1.78 –0.05 –0.29 0.1 –0.19 –0.34
Tightening Fin Cond (n=46) 1.31 0.04 0.0 –0.4 0.31 1.54 0.56
Stagflation (loose) (n=23) 1.92 –0.98 0.19 –0.55 2.42 2.19 –0.26
Stagflation (n=10) –1.13 –2.87 –1.67 –1.61 2.75 4.09 2.76
Inflationary boom (n=63) 1.57 0.97 0.64 0.02 –0.47 –0.05 –0.02
Recession (n=48) –1.75 –1.3 –0.16 0.4 1.05 0.76 –0.77
Fin Mkt shock/crisis (n=48) –0.91 0.6 –0.04 0.12 1.96 0.69 0.24
zG7
CPI
zG7
LEI
zG7
CPI
diff
zG7
LEI
diff
zRisk
Appetite
zFin
conditions
zFCI
diff
FIGURE 15.4 Grouping periods into the top 10 clusters.
Source: Bloomberg, Citi research, and authors’ calculations.
clusters. Figure 15.4 illustrates the median z-scores across the top 10 clusters with our
stylized names.
We show how assets perform in each environments in Figure 15.5, which delivers
a few key insights. First, there is a normal environment, when growth and inflation
do not deviate wildly from their long-term trends. All assets tend to deliver positive
returns. The Goldilocks regime maps similarly to the traditional quadrant approach,
growth shock maps to early recession, and recovery to late recession. There is an addi-
tional macroeconomic cluster where inflation is above average and growth is close to
trend, which is less benign, as the tightening of financial conditions (either from mon-
etary policy or from credit spread widening) means that stocks, bonds, and credit can
all sell-off. This regime can lead to stagflationary conditions like in 2022–2023. Of
the less common environments, which we use more for stress-testing of portfolios, we
see two flavors of stagflation. There is one where central banks and markets expect
“transitory” inflation e.g., 2022, and one where financial conditions have to tighten
meaningfully and inflation hedges do not work (see discussion and Table 15.1). Reces-
sionary times are actually one of the best times to invest; economic data is at its nadir,
and asset valuations have cheapened. Markets anticipate a recovery in the data and
tend to rally, especially risk-sensitive equity and credit positions. Equities see a change
in leadership and momentum strategies, especially in equities, which tend to see violent
reversals as the laggards become leaders. One example is financials in March 2009 or
cruise ship/travel companies in April 2020.
With stagflation and tightening financial conditions, which can lead to stagflation,
showing the most negative Sharpe ratios, we investigate next how asset allocators can
protect against stagflationary outcomes.

342 TRADING GLOBAL MACRO MARKETS
2.0
Normal Growth shock
Tightening Fin Cond
oitar
eprahS
Recovery
1.5 Goldilocks
1.0
0.5
0.0
–0.5
(a)
(b)
oitar
eprahS
SPX Bonds Credit Commodity DXY EAFE EM EM
USD USD Equity
Bond
3 Stagflation (loose) Recession
Stagflation Fin Mkt shock/crisis
Inflationary boom unconditional
2
1
0
–1
–2
–3
SPX Bonds Credit Commodity DXY EAFE EM EM
USD USD Equity
Bond
FIGURE 15.5 (a) Tightening financial conditions as the most difficult cluster. (b) Stagflation also
a painful cluster.
Source: Bloomberg, OECD and authors’ calculations.
15.2 HOW TO PROTECT AGAINST STAGFLATION
As mentioned previously, the workhorse for asset allocation for many decades has been
the 60/40 portfolio, where 60% was invested in equities, and 40% in fixed income,
mostly government bonds. The key feature of that allocation was the negative corre-
lation between bonds and equities during early recession periods. In the late 1990s,
Bridgewater popularized the concept of risk parity, which is also largely based on the
negative correlation between returns from government bonds and equities. The inno-
vation, based on the portfolio optimization work of the 1950s and 1960s, was that the
use of leverage allowed for allocating the same amount of risk to bonds, commodities,

How to Allocate 343
TABLE 15.1 During Fed Hikes, Not Many Inflation Hedges Work
Levels Returns since Jan 2001
CPI start FF start Gold Bitcoin TIPS DXY CTA SPX
Jan-21 1.3 0.25
Mar-22 7.9 0.50 3.7% 36.4% 2.7% 8.0% 6.9% 25.9%
Jul-22 8.4 2.50 –6.0% –31.0% 0.1% 16.9% 13.3% 13.4%
Source: Bloomberg, and authors’ calculations.
12
10
8
Difference
(RP − 60/40) 6
4
2
0
1980 1990 2000 2010 2020
ecnereffiD
Risk
60/40
Parity
Return 6.21% 5.15%
Volatility 10.53% 10.51%
Risk/Reward 0.59 0.49
Max DD –31.38% –34.73%
101
60/40
Risk Parity
100
FIGURE 15.6 Risk parity outperformed post-GFC, but not during inflation post-COVID.
Source: Bloomberg and authors’ calculations.
and to equities, irrespective of notional weights. This technique improves diversifica-
tion, as it allows investors to allocate the same amount of risk across different asset
classes, moving away from focusing too heavily on equities. Figure 15.6 shows that
for long periods of time, risk parity portfolios have had superior returns to the classic
60/40 benchmark.
However, in the post-COVID period, risk parity has underperformed. The reason
is that the best of all worlds for risk parity is when the correlation between bonds and
stocks is negative and when the cost of leverage is low. This was the case for most of
the aftermath of the 2008 crisis, where the world remained mainly concerned about
further deflationary shocks. However, in the aftermath of COVID, that changed, as
the policy response to COVID resulted in an extremely inflationary shock. The post-
COVID inflation led to a change in the correlation between bond and equity returns,
which became positive, as can be seen in Figure 15.7a. This was especially the case in
2022, when inflation was high, and the Fed reacted aggressively to higher inflation,

344 TRADING GLOBAL MACRO MARKETS
14.0%
12.0%
10.0%
8.0%
6.0%
4.0%
2.0%
0.0%
1980 1990 2000 2010 2020
)%(
YoY
IPC
CPI & equity/bond correlation
0.6
0.4
0.2
0.0
–0.2
–0.4
–0.6
noitalerroC
CPI Core YoY
SPX vs. US bonds 1-year (daily) corr
SPX vs. US bonds 3-year (monthly) corr
0.8
0.6
0.4
UURTTAUL
.sv
XPS
:rroC
raey-1
(a)
Bond equity correlation and inflation
y = 7.43x + –0.23
0.2
0.0
–0.2
–0.4
–0.6 OLS fit (R2=0.22)
All observations
Inflation < 2.5%
0.0% 2.0% 4.0% 6.0% 8.0% 10.0% 12.0% 14.0%
(b) CPI Core YoY (%)
FIGURE 15.7 (a) CPI important for stock-bond correlation. (b) For CPIs below 2.5%.
stock–bond correlation mostly negative.
Source: Bloomberg, FRED, and authors’ calculations.
after initially dragging its feet, wrongly assuming that inflation would be transitory.
Eventually, the inflation spike did turn out to be transitory, allowing the Fed to cut
interest rates in 2024, and leading to the correlation at least stabilizing, with a down-
ward bias. While the correlation between the US core CPI and the equity/bond correla-
tion is not as stable as we would like, Figure 15.7b shows that for inflation levels below
2.5%, the equity/bond correlation is predominantly negative, while above 2.5%, it is
mostly positive.

How to Allocate 345
In the future, the important question to ask is whether inflationary or deflation-
ary shocks are more likely. Unfortunately, there are some important contenders for
inflationary shocks. The most important challenges that could generate inflationary
shocks are the costs of the energy transition, which may generate “greenflation,” the
costs of structurally higher defense spending, as we exit pax Americana, and the gen-
eral idea that governments have to a large extent socialized risks like COVID, creat-
ing an expectation among voters that the next shock would again be absorbed by the
government rather than the private sector, at a time when government debt is already
extremely high. There are clearly also deflationary shocks in our future, which include
most plain-vanilla recessions, but also the unstoppable march forward of AI, which
means that government bonds will likely remain a part of well-diversified portfolios.
However, if inflationary shocks are more likely than they were in the past, a significant
part of the bond allocation should instead be invested in inflation hedges rather than
just in deflation hedges. This is before we even consider the problem of the bond glut,
where debt issuance may be too high for back ends to participate as much in central
bank cutting cycles as they did in the past.
The problem with inflation hedges is that they are much less plentiful than defla-
tion hedges. This is especially true for episodes where the Fed is actually addressing
inflation with rate hikes. An interesting case study in this regard is 2022. When infla-
tion was rising, while the Fed was still dragging its feet, there were several classic infla-
tion hedges that worked well, including gold, bitcoin, TIPS, and even equities. This
was the case from January 2021 to March 2022. However, when the Fed started to
hike rates in March 2022, even with inflation still going up until peaking in June 2022
(published in July), those hedges stopped working. As illustrated in Table 15.1, which
shows the cumulative returns for some of the traditional inflation hedges, gold, Bit-
coin, and SPX all had meaningfully negative returns between the start of the Fed hiking
cycle in March 2022, and peak headline inflation in June 2022. Even TIPS had nega-
tive returns, as the negative impact of the Fed hiking cycle more than offset the higher
carry from higher inflation. Equities did well between the start of Fed hikes and peak
inflation, but that happened to be a bear market rally in a fairly pronounced bear mar-
ket. Within public markets, the USD was the only asset that consistently performed
well both when inflation was rising and was not being addressed by the Fed, and when
inflation was rising, with the Fed hiking to belatedly address inflation. Given that the
USD also performs well during most deflationary shocks, as risk aversion tends to drive
up the USD, it may be an interesting hedge, especially when it is also positive carry.
We would also note, though, that given that FX is a relative price, the strong USD per-
formance in 2022 was helped by the fact that the inflationary shock was somewhat
US-centric, given the strong US fiscal response. If this is not the case, the USD may not
work as well as in 2022. As always in FX, many other considerations will also play a
role, as we have discussed in the FX chapter.
We therefore extend our search for inflation hedges to factors and macro strategies.
We find that trend-following and momentum strategies (in FX, and also in equities)
work well. The same is true for the carry factor, also a favorite macro hedge fund strat-
egy, though in FX carry, the high stagflation case is not profitable, as is illustrated in
Figure 15.8. Value works in fixed income and FX, but not so much in equities. Over-
all, CTAs and macro hedge funds are therefore likely the best inflation and stagflation

346 TRADING GLOBAL MACRO MARKETS
oitar
eprahS
Overheat Recession
Goldilocks Recession Early
Stagflation Recession Late
1.5
Hi Stagflation
1.0
0.5
0.0
–0.5
Eq Eq Eq Eq FI FI FX FX FX Comm CTA Macro
Value Mom Quality Low Carry Value Carry Value Mom Carry funds
Risk
FIGURE 15.8 Several macro factors work well during stagflation.
Source: Citi Research, AQR, Barclay, Bloomberg.
hedges for investors. This is likely to remain the case going forward as bear markets
driven by inflation are typically relatively slow-moving and longer-lasting. This suits
CTAs much better than environments like 2020, when the bear market was very sharp
and short-lived. Within the equity market, the quality factor performs very well. Carry
also tends to work well, especially in fixed income.
15.3 STRATEGIC ASSET ALLOCATION FOR REGIME AGNOSTICS
Strategic asset allocation is its own field and beyond the scope of this book, as most
of our tools and models are much more tactical in nature. However, we would be
amiss to not point out that the regime approach is also extremely useful for strategic
asset allocation. We address this topic in Saunders et al. (2022). The main argument
is that, in the long run, portfolios should be regime-agnostic. Compared to the 60/40
portfolio, this means partly adding assets that can do well in the stagflation regime,
which is the blind spot of the 60/40 portfolio. As discussed earlier in this chapter,
this means adding real assets, trend-following, quality equities, and carry strategies to
reduce regime dependence. Of course, the optimal strategic asset allocation depends
on how much investors are willing to trade-off in terms of returns for regime stability.
But for most preference structures, the prescription is to move an allocation away from
equities and/or bonds and to those alternative asset classes. For example, a portfolio
that is 50% equities (property or other real assets can also be included here), 30%
bonds, 10% CTAs, and 5% quality and carry (each) results in positive performance
across all regimes. Of course, stagflation still performs worse than other regimes, but
returns are now (barely) positive. As per Figure 15.9, the simulated information ratio

How to Allocate 347
S&P 500 US Treasury 60/40 Regime
Stable
Return 7.55% 1.87% 5.28% 5.34%
20.0 Volatility 15.41% 5.11% 9.67% 7.83%
Risk/Reward 0.49 0.37 0.55 0.68
Max DD –56.50% –24.11% –32.47% –25.80%
10.0
5.0
2.0
1.0
S&P 500 US Treasury 60/40 Regime Stable
1979 1989 1999 2009 2019
FIGURE 15.9 Regime-agnostic portfolio outperforms 60/40.
Source: Bloomberg, AQR, Barclay, authors’ calculations Source: Bloomberg and authors’
calculations.
is now 0.68, up from (also fixes 0.61 to 0.68). 0.55 for the 60/40 portfolio. Returns
come in at 5.3%, slightly beating 60/40, but not equities.
The previous discussion was set in a long-only context. However, it is also possible,
of course, to use shorts to hedge portfolios. An interesting aspect is whether credit can
hedge equities or vice versa. We investigate that next.
15.4 THE CHOICE OF EQUITY VERSUS CREDIT RISK
One way to answer the question of how to choose between equity and credit is to cal-
culate the ex post optimal Sharpe ratio portfolios across bonds, equities, and credit.
We do this using rolling 10 years of data on returns, correlations, and volatilities.
Figure 15.10 shows that in the 1970s, corporate bonds made up a significant propor-
tion of the optimal Sharpe portfolio, at times running at 100%, as equities and bonds
struggled with supply-induced inflationary shocks. However, this changed in the late
1990s as both fixed income and equities took larger weights in the portfolio. As an
aside, we would note that this is also when higher-quality duration-matched data on
credit excess returns became available, which may exaggerate the change in the optimal
weight for credit. Since the GFC of 2008, credit’s role in the portfolio has been greatly
diminished, averaging just 12%, and currently is not sitting far from zero. Still, even
since 2008, having corporate bonds as part of the optimal portfolio has increased the
Sharpe ratio in our hypothetical exercise. However, for trading purposes, this analysis
is too big picture. We go into more detail next.
In order to understand the predictors of credit versus equity performance on a
vol-adjusted basis, we run a regression on the likely candidates: volatility (equity and
bond), credit spread levels and recent changes, equity momentum and fundamental
factors, the shape of the yield-curve, recent (i.e., US 2yr note) changes, and inflation.

348 TRADING GLOBAL MACRO MARKETS
100%
Corp bond excess
US Govt Bonds
S&P 500
80%
g
ht
60%
ei
w
o
oli
ortf
40%
P
20%
0%
1979 1989 1999 2009 2019
FIGURE 15.10 The ex post optimal share of credit has fallen sharply.
Source: Bloomberg and authors’ calculations.
The results are in line with intuition; significant factors for choosing equities are a
high VIX and recent equity outperformance. High spreads are more positive for credit.
Credit spread changes are subsumed by the equity moves, however. High inflation
favors credit, other things being equal, but it is not statistically significant. Interest-
ingly, these factors can be captured in a real-time strategy, where we use the candidate
variables in a ridge regression with an expanding window and then take positions on
volatility-adjusted credit versus equity in proportion to the percentile of the forecasts.
We adjust the volatility multiplier monthly. Typically, markets are range trading in rel-
ative terms, except during credit events, when credit will underperform, as can be seen
in Figure 15.11. The backtest picks up those periods, as a rising VIX in the face of still
relatively low credit pushes the model forecasts to meaningfully favor equities. Given
the subpar liquidity profile of the investment-grade index, we also show results for
CDX versus equity and find lower returns and Sharpe ratios. The PNLs have a similar
profile of outperformance around credit events, but the Sharpe using the CDX is likely
too low to trade it.
15.5 THE CHOICE OF GOVERNMENT BONDS VERSUS EQUITIES
While the choice of credit versus equities is extremely important in a hedging con-
text, the main question in asset allocation is much more whether to favor government
bonds over equities or vice versa. For longer-term investors, valuation is the obvious
starting point for this investigation. As illustrated in the equity chapter, using valua-
tion to time equity markets at the extremes usually leads to shorting a bubble, which
is painful. Charts of long-term returns and starting valuations for equities do show

How to Allocate 349
IG CDX vs.
credit xs vs. equities equities
Return 1.16% 0.43%
1.3
Volatility 1.24% 1.35%
Risk/Reward 0.94 0.32
1.2 Max DD –2.83% –4.32%
1.2
CDX vs.
1.2 equities
IG credit xs
vs. equities
1.1
1.1
1.0
2005 2010 2015 2020 2025
FIGURE 15.11 Equities are favored during rising VIX and with low credit spreads.
Source: Bloomberg and authors’ calculations.
mean-reversion, but overlapping data makes it difficult to draw clean statistical infer-
ences. Still, there is a question of whether focusing on cross-asset class valuation is
more promising. To investigate this, we focus on the earnings yield gap, which can
be expressed as earnings yields versus government bond yields. Operationalizing such
a framework and accounting for structural changes (ever richer bond yields from the
1980s) is challenging. We therefore focus on a rolling three-year z-score of this mea-
sure. For long-term investors, we study the question by looking at extremes in the val-
uation of equities versus bonds and by imposing a long one-year holding period. We
use earnings data from Bloomberg and lag it by three months to account for delays in
earnings releases. We couple this with the level of the S&P to get a real-time measure
of E/P, and we subtract 10-year government yields. The resulting z-score is shown in
Figure 15.12. EYG is nicely mean-reverting. So far so good.
However, the backtest is less promising. Figure 15.13 shows the PNL of taking
opposite positions when equities are particularly expensive relative to bonds, i.e., the
z-score is –2 or lower. This strategy has added value at the tail end of the dot.com era
and ahead of the 1987 crash. Recent signals would have been shorting an equity bull
market, though. Overall, the information ratio is similar to buy and hold. On the other
side, buying equities relative to bonds when the ratio was cheap has not been help-
ful. After the 2000 bubble burst, investors would have entered equities much too early
during a bear market, where falling earnings kept equities cheap. The same happened
in 2007, as declining bond yields pushed equities into the cheap zone before the finan-
cial crisis. The results are similar for longer-term z-score calculations up to 10 years.
Broadly speaking, this analysis strengthens our view that valuation is a poor timing tool
not only for equities outright, but also for the allocation between bonds and equities.
While extremes in relative pricing versus bonds can help to highlight bubbles or unusu-
ally frothy conditions, there are many false alarms, and bullish equity signals tend to
arrive in the midst of earnings deterioration or recessions, leaving investors exposed

350 TRADING GLOBAL MACRO MARKETS
US earnings yield relative to bonds
6 Earnings Yield Equities cheap
Earnings less 10-year Govt Yield (vs. bonds)
4
2
0
–2
–4
Equities expensive,
Bonds cheap
–6
1980 1990 2000 2010 2020
3-year z-score
FIGURE 15.12 Earnings yield gap is mean-reverting.
Source: Bloomberg and authors’ calculations.
σ < –2 σ > 2 Buy & Hold
Return –0.03% 1.47% 5.45%
Volatility 9.01% 12.48% 19.50%
9.0 Risk/Reward –0.00 0.12 0.28
8.0 Max DD –60.71% –72.19% –75.11%
7.0 Active IR –0.01 0.24 0.28
6.0 % on 20.60% 23.18% 100.00%
5.0
4.0
3.0 σ > 2
Buy & Hold
2.0
σ < –2
1.00
0.9
0.8
0.7
0.6
0.5
1980 1990 2000 2010 2020
FIGURE 15.13 Using earnings yield premium not a great timing tool.
Source: Bloomberg and authors’ calculations.
to drawdowns. Valuation, therefore, works better as a risk-management overlay—a
warning flag at expensive extremes—than as a systematic buy/sell signal. For long-
horizon investors, it may guide expectations of future returns, but it is a risk gauge,
not a trading signal.
So what are investors supposed to do if valuation is unreliable? As usual, the
answer is momentum. Historically, the simplest rule to allocate between bonds and
equities is just to use the 200dma. If equities are above their 200dma, be long equities.
If not, check if bonds are above their 200dma. If they are, buy bonds, risk-adjusted to

How to Allocate 351
have the same risk as was the case when fully invested in equities. If neither asset is
above its 200dma, buy T-Bills. This simple rule results in an information ratio of 0.59,
above the SPX of 0.46 and 60/40 of 0.53, as highlighted in Figure 15.14. Of course, the
hope would be that our rules discussed in the equity chapter on how to buy bottoms
would allow investors to not wait until the moving average breaks above the 200dma,
but to move back into risk earlier.
In addition to the valuation or technical-driven frameworks, there are also struc-
tural developments to discuss, which are broadly a headwind for government bonds.
First, the market capitalization of government debt has been rising very sharply, as
governments have reacted to various crises (GFC, COVID), as well as plain vanilla
recessions by protecting the private sector and socializing losses. It appears likely that
this behavior will continue, suggesting that the market capitalization of public debt
jumps significantly higher during a crisis, followed by stabilization, only to jump again
when the next crisis hits. Presumably, this process will continue until markets become
a binding constraint. The equity market, on the other hand, has been shrinking with
negative net issuance due to a combination of strong buyback activity and a sluggish
IPO market. Although market capitalization has increased, this is due to price appre-
ciation, not issuance, as can be seen in Figure 15.15.
Second, the way in which debt indexes are constructed adds to the problem of too
much debt supply. Most indexes use market capitalization to determine the weights.
This means that the bonds of countries that are prolific issuers are getting a higher and
higher weight. Given that credit risk is correlated with the size of outstanding debt,
this means that indexes force investors to have exaggerated weights in countries that
have the worst credit profile. Credit risk in government bond markets of developed
markets has so far only been tested for brief periods, and most famously during the Liz
Truss moment in the United Kingdom, but over the next decade, credit risk inherent
in government bonds could be a more important factor. Although equities will not be
Eq|Bond|Cash
S&P 500 US 7–10-year bond 60/40
200d MA
Return 6.79% 8.04% 2.25% 5.72%
20.0 Volatility 11.53% 17.55% 7.47% 10.77%
Risk/Reward 0.59 0.46 0.30 0.53
Max DD –28.39% –60.75% –37.49% –33.54%
10.0
5.0
2.0
1.0
Eq|Bond|Cash 200d MA S&P 500 US 7−10-year bond 60/40
1980 1990 2000 2010 2020
FIGURE 15.14 A simple 200dma system works much better.
Source: Bloomberg and authors’ calculations.

352 TRADING GLOBAL MACRO MARKETS
600
400
200
0
–200
)nb$(
ecnaussI
teN
Net Issuance US Treasury Notes, Bonds, TIPS, &FRNs
Net Equity Issuance of Domestic Non-Financial Corporations
1996-Dec 1998-Jun 1999-Dec 2001-Jun 2002-Dec 2004-Jun 2005-Dec 2007-Jun 2008-Dec 2010-Jun 2011-Dec 2013-Jun 2014-Dec 2016-Jun 2017-Dec 2019-Jun 2020-Dec 2022-Jun 2023-Dec
FIGURE 15.15 Net issuance favors equities over bonds. Source: Citi Research
Source: Bloomberg and authors’ calculations.
immune if credit fears in the government bond market were to rise, it is noteworthy
that equity market indexes do the opposite to debt indexes in that successful companies
enter the indexes and increase their weighting, while unsuccessful ones do the opposite.
The index weightings are therefore broadly favorable for investors in equity land and
unfavorable in debt land.
15.6 DON’T RISK YOUR BUDGET, BUDGET YOUR RISK
Volatility is an important tool for asset allocation. Given the uncertainty surrounding
future returns, it is notable that volatility tends to be persistent. In the FX chapter, we
use this persistence to size positions across currencies with different risk characteris-
tics. However, volatility does not just live in the cross-section (i.e., across assets) but
also changes through time and environments (the time-series). This is something we
explored before for the FX carry strategy with our volatility warning indicator. Here,
we broaden the discussion. The main academic work on how time-varying volatility
affects assets was Moreira and Muir (2017) but, as is often the case, was well known
by practitioners for many years before.
To study time-varying volatility, we group each month by realized volatility using
the last 22 trading sessions and group those into quintiles. We then calculate volatility,
returns, and information ratios for the subsequent month and repeat the process. Our
findings are illustrated by Figure 15.16, where the first panel shows volatility in the
subsequent month in relation to the z-score of the volatility of the preceding month.
Volatility is quite persistent. If it was high in the previous month, it tends to realize high
again, while low readings beget low readings. Importantly, returns do not seem to fol-
low such a strong pattern; the second panel shows that they remain around the same

How to Allocate 353
Volatility Return Risk/Reward
2.00%
12.0% 0.30
1.75%
10.0% 0.25
1.50%
8.0% 0.20
1.25%
6.0% 1.00% 0.15
0.75%
4.0% 0.10
0.50%
2.0% 0.05
0.25%
0.0% 0.00% 0.00
0
<
z
<
0
0
.2
.2
<
z
<
0
0
.4
.4
<
z
<
0
0
.6
.6
<
z
<
0.8
z
>
0.8
0
<
z
<
0
0
.2
.2
<
z
<
0
0
.4
.4
<
z
<
0
0
.6
.6
<
z
<
0.8
z
>
0.8
0
<
z
<
0
0
.2
.2
<
z
<
0
0
.4
.4
<
z
<
0
0
.6
.6
<
z
<
0.8
z
>
0.8
FIGURE 15.16 Higher risk, higher reward.
Source: Bloomberg and authors’ calculations.
level, except for an uptick in the higher volatility quintile. This uptick is interesting
and suggests that when realized volatility remains high for a second month, it can be in
the context of upside volatility. Still, the increased returns do not compensate for the
jump in volatility, resulting in lower information ratios even in the high volatility quin-
tile. When maximizing information ratio, it pays to reduce positions when volatility
strikes. We would note, though, that this is slightly different with implied volatility. On
a tactical basis, a higher VIX delivers a slightly higher information ratio than uncon-
ditional, although lower implied volatility periods are even stronger, as discussed in
Chapter 9, and shown in Figure 9.3b, where the difference between realized and
implied is significant.
Applying the same framework to rates, inference for fixed-income markets can be
fraught, given that daily data only starts in 1988, when bonds were already in a struc-
tural bull market. Earlier studies using yield data to proxy returns show a structural
change in bond volatility in the mid-1980s (see Harvey et al., 2018). With these caveats
out of the way, our study is illustrated by Figure 15.17, which shows the returns in each
quintile of volatility over time. Interestingly, bonds do not have high returns following
a period of high volatility. On the contrary, here returns are well sub par for the high-
est quintile, resulting in a very low (but still positive) information ratio. However, the
pattern is not as nicely monotonically increasing as it is for equities, in that the second
most volatile quintile has the highest information ratio. It takes extreme volatility to
hurt bonds. This finding is mostly driven by the recent period, as the post-COVID rates
bear-market features prominently. Even though investors should not put too much
weight on one single episode, to us the 2022 episode is important, partly because the
1970s downturns are not always captured in historical analysis and because changes

354 TRADING GLOBAL MACRO MARKETS
Volatility Return Risk/Reward
4.00% 1.00%
0.40
3.50%
0.35
0.80%
3.00%
0.30
2.50% 0.60% 0.25
2.00% 0.20
1.50% 0.40% 0.15
1.00% 0.10
0.20%
0.50% 0.05
0.00% 0.00% 0.00
0
<
z
<
0
0
.
.
2
2
<
z
<
0
0
.4
.4
<
z
<
0
0
.6
.6
<
z
<
0.8
z
>
0.8
0
<
z
<
0
0
.
.
2
2
<
z
<
0
0
.4
.4
<
z
<
0
0
.6
.6
<
z
<
0.8
z
>
0.8
0
<
z
<
0
0
.
.
2
2
<
z
<
0
0
.4
.4
<
z
<
0
0
.6
.6
<
z
<
0.8
z
>
0.8
FIGURE 15.17 Higher risk without the reward.
Source: Bloomberg and authors’ calculations.
in market structure since then make the 1970s less relevant today. We therefore prefer
to reduce sizing in fixed income markets when volatility is moving up.
Finally, we broaden our analysis across other asset classes to understand in which
assets volatility targeting is helpful. In particular, we analyze popular asset classes and
scale positions to target the long-term volatility of each asset class. Each month, we
examine the last month’s realized volatility and then lever our hypothetical portfolio
up if it has come in lower than the long-term average or down if it is higher in order to
target a constant volatility through time. In equity and fixed-income markets, we see
a benefit to scaling up risk in tranquil times and de-levering when realized volatility
is higher than average, as shown by the volatility-targeted Sharpe ratios being higher
than unlevered, as can be seen in Figure 15.18. The advantage in equities is highest
for the United states, but still present in Germany (though not in Japan). We do not
find a benefit for credit spread returns or commodity futures. Here, volatility targeting
detracts value.
Overall, volatility targeting is a popular strategy, which tends to improve infor-
mation ratios, at least for the more important asset classes, even though it does not
necessarily improve total returns. As also discussed in the equity chapter, this strat-
egy can lead to some momentum in markets—for example, when equity volatility falls
from high levels, there tends to be a persistent bid as investors who reduced sizing have
to ramp up their positions again.
15.7 TACTICAL, TACTICAL, ASSET ALLOCATION
So far, most of this chapter is firmly in the realm of tactical asset allocation, rather
than strategic asset allocation. To get even more tactical, we analyze the role of quanti-
tative funds in markets and whether there are any shorter-term signals for the various

How to Allocate 355
0.6 Unlevered
Vol targeted
0.5
0.4
0.3
0.2
0.1
0.0
S&P
500
oitar
eprahS
Topix DAX US BBG IG Crude Copper Gold
(Japan) (Germany) 7–10-year US Credit (WTI) Future Future
Future Future bond Corporate spread Future
ret
FIGURE 15.18 Targeting volatility works in some, but not all, markets.
Source: Bloomberg and authors’ calculations.
asset classes. We focus on commodity trading advisors (CTAs), which have become an
important player. Barclay Hedge estimates that as of mid-2024, CTAs had around 360
billion under management. With relatively high turnover, this suggests that CTAs are
an important force in many markets. CTAs typically trade futures across asset classes
and geographies and mostly employ trend following systems, based on moving aver-
ages. Next, we simulate a simple version of such a system by employing the 22-, 66-,
200-, and 252-day moving averages. We assume that for each moving average crossed,
the CTA model adds one unit of risk, up to a max range of –4 (max short) to +4
(max long). This simple model does quite well to approximate publicly available PNL
streams of CTA indexes. As a cross-check, we also use regressions of a CTA index on 12
of the most liquid futures contracts to infer current positioning. Given high turnover,
we use the previous 22 trading days of return data (one month) to estimate exposures.
When we use both simulated positions to forecast CTA returns, we find that the simple
model using four moving averages does better than the one that infers positions from
futures contracts. We then plot monthly forward returns for the moving average mea-
sure, depending on the inferred positioning (see Figure 15.19, left panel). We find that
when using the moving average-based model, trend following basically works. This is
especially true for commodities, where returns for the max short bucket are very neg-
ative, while the ones for the max long bucket are positive. FX and bonds also have the
lowest returns in the max short bucket, which are roughly flat, and have decent returns
in the max long bucket. For equities, there is no clear pattern, though, as the max short
bucket has small positive returns. It is the second-lowest bucket, which actually has
negative returns. While far from perfect, our moving average model is likely money-
making. This would suggest that the value of CTA positioning as a counter-indicator
is really extremely limited. Investors are better off going with the trend.
When hunting for counter-indicators, CFTC data does a better job than mov-
ing average CTA models, at least for equities. The right panel of Figure 15.19 shows
monthly forward returns by z-score of the CFTC non-commercial positions, mapped

356 TRADING GLOBAL MACRO MARKETS
CTA Returns and positioning CFTC (AM) Positioning and monthly returns
1.50%
Equity Equity
Bonds Bonds
1.25% Commods Commods
FX FX
1.00%
0.75%
n
ur
et
d r 0.50%
w
hly
f
nt 0.25%
o
M
0.00%
–0.25%
–0.50%
M
ax
S
h
ort
S
h
ort
N
e
utr
al
L
o n
g
M
ax
L
o n
g
M
ax
S
h
ort
S
h
ort
N
e
utr
al
L
o n
g
M
ax
L
o n
g
FIGURE 15.19 The trend is your friend, mostly.
Source: Bloomberg and authors’ calculations.
to the equivalent positioning of our trend-following rules. A z-score of 2 or above
is max long, 0.5 to 2 long, less than –0.5 is short, and less than –2 is max short.
We look at month-end numbers for asset manager/managed money categories. Fad-
ing extremes works for equities (see also 9 using a daily signal). However, bonds and
commodities show follow-through, and investors should go with the trend. FX is nei-
ther here nor there. For commodities, we would note, though, that the reality is highly
contract-specific (see also Willer et al., 2023). Investors should therefore take extremes
in CFTC data seriously when trading equities and certain commodities, but for other
asset classes, it is not a good reversal indicator.
15.8 SUMMARY
In this chapter, we describe the regime investing approach in some detail and lay out
how to improve upon the traditional four-quadrant approach. We focus on stagflation
as a regime in which most public assets do not work well. Instead, trend-following and
momentum strategies are attractive, as are carry strategies. These patterns are useful for
regime-agnostic allocation. When deciding whether to buy equity or bonds, valuation
measures are not overly compelling. Simple moving average rules tend to work better.
Volatility targeting adds alpha in the most important asset classes, but not everywhere.
More tactically, our data shows that trend following works and that CTA positioning
should not be faded. CFTC positioning is also more often a trend signal than a mean
reversion signal, with the exception of equities.