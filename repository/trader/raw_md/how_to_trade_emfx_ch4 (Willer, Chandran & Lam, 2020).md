CHAPTER4
How to Trade EMFX
EMFX trading has gained market share from G10 FX trading over the last decade,
as briefly discussed in Chapter 1. And it is plausible that EMFX is even more impor-
tant for alpha generation than its rising market share suggests. This is likely the case
because one of the more popular strategies to extract alpha in FX is the carry strategy.
With carry in G10 having collapsed in the aftermath of the financial crisis, EMFX has
become more important for carry-hungry currency investors, even though carry in EM
has admittedly also fallen for some time now. While to our mind, EMFX is a very macro
asset class, there are also micro features that can be exploited to generate alpha. This
chapter outlines how we propose to go about doing that.1
4.1
ONLY THE JPY IS SPECIAL
We start off with a quick discussion of how to define what an emerging market is for
the sake of FX trading.2 It turns out that it is actually very hard to find a dividing
line that neatly separates EMFX from G10 FX. In Chapter 2, we found that EMFX
is driven to a large degree by global macro factors, and in particular by equities/risk
aversion, US credit, commodities, and, in some periods, US rates. When analysing the
correlation patterns of both G10 FX (where we ignore CHF, as it is mostly driven by
EUR) and EMFX with these major macro drivers in more detail, as we do in Table 4.1,
it turns out that the only currency that is “special” is the Japanese Yen, because it
appreciates relatively reliably with rising risk aversion and to some extent, for the same
reason, rallies when US rates are falling. No other currency (again excluding CHF) has
a consistently strongly positive correlation with risk aversion, be it a G10 or an EM
currency. The EUR comes relatively close, though. It also has a positive beta to the
US HY index, a slight negative beta to VIX, and a positive beta to the SPX. But the
betas are much smaller than for the JPY, and the relationship is less consistent. But for
1We would also point the reader to Donnelly (2019) for a very worthwhile discussion of FX
trading. Donnelly is more focused on technicals than we are but also lays out the fundamental
principles of FX trading extremely well.
2As we are interested in the trading behaviour of the various assets, rather than in a unified theory
of what constitutes an emerging market, we think that the definition should be asset-class-specific.
58
Trading Fixed Income and FX in Emerging Markets: A Practitioner's Guide, First Edition.
Dirk Willer, Ram Bala Chandran and Kenneth Lam.
© John Wiley & Sons, Inc. Published by John Wiley & Sons, Inc.

How to Trade EMFX
59
TABLE 4.1
It is Hard to Distinguish Between EMFX and G10 FX.
UST 10yr
SPX
US HY
VIX
BBG commodity
USD-BRL
4%
−28%
−82%
2%
−39%
USD-MXN
8%
−25%
−79%
2%
−26%
USD-CLP
3%
−21%
−58%
2%
−28%
USD-COP
0%
−44%
−125%
3%
−48%
USD-KRW
3%
−19%
−58%
2%
−22%
USD-TWD
1%
−8%
−25%
1%
−10%
USD-INR
3%
−10%
−31%
1%
−9%
USD-CNY
1%
−1%
−5%
0%
−6%
USD-MYR
3%
−16%
−67%
1%
−19%
USD-IDR
1%
−17%
−53%
1%
−14%
USD-SGD
5%
−6%
−25%
0%
−15%
USD-PHP
2%
−4%
−24%
1%
−5%
USD-THB
4%
−8%
−29%
1%
−14%
EUR-PLN
2%
−12%
−31%
1%
−7%
EUR-CZK
0%
0%
−2%
0%
−1%
EUR-HUF
2%
−9%
−16%
1%
−5%
USD-RUB
−7%
−48%
−135%
5%
−62%
USD-TRY
5%
−20%
−36%
2%
−17%
USD-ZAR
9%
−36%
−84%
3%
−38%
Median EM
3%
−16%
−36%
1%
−15%
USD-JPY
16%
26%
27%
−3%
−4%
USD-EUR
6%
5%
2%
−1%
−19%
EUR-NOK
1%
−21%
−66%
2%
−18%
EUR-SEK
−1%
−10%
−26%
1%
−4%
USD-CAD
1%
−17%
−51%
1%
−35%
USD-AUD
4%
−25%
−64%
2%
−32%
USD-NZD
8%
−12%
−42%
0%
−23%
Median G10
4%
−12%
−42%
1%
−19%
Note: Betas of FX to US rates, SPX, US HY, BBG commodities, and VIX.
Source: Bloomberg, authors’ calculations.
any G10 currency other than the JPY and maybe the EUR, the betas are very similar
to the betas of their EM peers. On the EM side, the one currency that comes closest
to behaving like a risk-free currency is EUR-CZK, followed by CNY (given that it is
highly managed). And if we create a basket of the G10 commodity currencies (NOK,
AUD, NZD, and CAD) and compare its correlation structure to an EM commodity
basket (RUB, ZAR, CLP, COP, BRL, PEN, IDR, and MYR), the betas to those global
macro market drivers are very similar and at times even lower for the EM commodity
basket than for the G10 commodity basket. We conclude that when it comes to their
trading behaviour with respect to global macro, G10 and EM commodity currencies are
more similar than different in most respects. Therefore, it is more helpful to distinguish
between commodity producers and commodity consumers rather than between G10
and EM currencies.

60
TRADING FIXED INCOME AND FX IN EMERGING MARKETS: A PRACTITIONER’S GUIDE
But when abstracting from global macro correlations, we do find important dif-
ferences between G10 and EM currencies that become obvious on closer inspection.
One distinction is that the institutional framework is often weaker in poorer countries
than in richer countries (and the classical delineating feature between EM versus G10
is, of course, GDP per head). While on most trading days this difference is irrelevant, it
becomes episodically very important, especially during election time. A lot more dam-
age can be caused if a market-unfriendly candidate wins in the average emerging market
than when this happens in the average G10 country, presumably because personalities
often are able to dominate institutions in EM more easily than they can in DM, where
checks and balances are more pronounced. EM currencies take such risks into account
to a larger extent than G10 currencies do – but only when elections are close. Weaker
institutions also make policies like capital controls more likely. Later in this book, we
are going to illustrate how these events can be traded in EMFX.
4.2
NO HELPING HAND FROM EM RATES
Another key difference between EMFX and G10 FX is that interest rate spreads explain
an important part of the trading behaviour of G10 FX, but such spreads explain very
little for EMFX. In particular, for G10, more hawkish central banks typically lead to
widening spreads of interest rates versus the US, which then results in a stronger cur-
rency. This is not true for EMFX, where local rates often move higher with weaker
FX. We illustrate this pattern in Figure 4.1. The chart shows a simulated P&L for
a strategy that assumes perfect foresight on two-year interest rates. When spreads of
FIGURE 4.1
And This is What Makes EMFX Different from G10 FX.
Note: P&L of a perfect-foresight strategy for EM and G10 FX using two-year swap
rates.
Source: Bloomberg, authors’ calculations.

How to Trade EMFX
61
domestic interest rates against US rates rise, the strategy goes long the currency in ques-
tion against the USD. The opposite trade is put on when the interest rates fall versus US
rates. We apply this strategy to G10 FX and to EMFX, where we distinguish between
low-volatility and high-volatility EMFX. The argument for making this distinction is
that low-volatility EMFX is unlikely to sell off by enough to generate inflation fears and
rate hike expectations, cutting off one of the possible channels that tie higher rates to
weaker FX. As can be seen, the results vary drastically for the three classes of curren-
cies. For G10 currencies, the simulated P&L moves higher, almost in a straight line and
without major pullbacks. In EMFX, however, the P&L is heading slowly but consis-
tently lower, also with little reprieve. The downward slope is more pronounced for the
high-volatility EMFX, but even low-volatility EMFX loses money when traded in line
with interest rate differentials. As it turns out, even for low-volatility EMFX, rising risk
aversion can lead to a strengthening USD, which then also pushes up EM rates, mostly
in a coincident fashion.
And even controlling for risk aversion and USD directionality more directly, G10
FX and EMFX behave differently when it comes to interest rates. This becomes clear
when we implement the same strategy once more, but this time apply our trading rule
separately to EMFX and to G10 relative value crosses. In this exercise, we make sure
that both currencies for a given cross are similarly volatile. This approach largely strips
out the impact from rising risk aversion given that it removes any USD directionality.
With this exercise, we obtain results for G10 FX that are very similar to before. If
we had perfect foresight on rate differentials in G10 space, the P&L when going long
the currency where rate spreads are rising, and vice versa, is consistently positive. The
pattern for EMFX is different, though. Instead of pointing straight down, the P&L chart
goes mostly sideways, neither making nor losing much money. This is an important
finding. It suggests that even once we have controlled for episodes of rising risk aversion,
it is still the case that more hawkish central banks are not necessarily bullish for EM
currencies. One reason is that many EMs are attracting large capital inflows when local
bonds are in a bull market, which is often the case when central banks are cutting rates.
Such bond inflows can lead to currency strength in spite of lower rate differentials.
The correlation of FX with their domestic interest rate is for us the key distinction
between EMFX and G10 FX. Either rates differentials are important to trade FX, in
which case the currency quacks like a G10 FX, or they are not, in which case we should
treat that currency like an EM currency, even if the country is not categorized that way
by more traditional definitions.
Using this approach, we can identify the “true” EM currencies, at least from a
currency trading perspective. Table 4.2 shows the mean returns, volatilities, and infor-
mation ratios (IRs) by currency resulting from the perfect-foresight strategy of the USD
crosses. The true EM currencies are the ones that have negative IRs. The results are
mostly as one would intuitively have expected. In Latam, the BRL, MXN, COP, and
PEN all behave like true EM currencies, while the CLP does not. In CEEMEA, the TRY,
RUB, ZAR, and HUF behave like EM currencies, while the PLN, CZK, and ILS do not.
In Asia, most currencies behave like G10 currencies. Here the results are less intuitive,
as the currencies that trade like EM currencies are the TWD and, to a lesser extent, the
SGD, which are not the typical high yielders that appear in Latam and CEEMEA.

62
TRADING FIXED INCOME AND FX IN EMERGING MARKETS: A PRACTITIONER’S GUIDE
TABLE 4.2
Some EM Currencies Behave like G10, Mostly in Asia.
FX
Mean
Volatility
IR
AUD
18.1%
12.9%
1.41
CAD
11.9%
9.4%
1.26
CHF
13.7%
11.6%
1.18
EUR
11.5%
9.5%
1.21
JPY
10.1%
9.9%
1.01
NOK
15.7%
12.2%
1.29
SEK
15.9%
12.0%
1.33
CNY
2.5%
3.0%
0.83
INR
0.7%
8.0%
0.09
KRW
3.6%
12.0%
0.30
MYR
3.9%
7.2%
0.54
SGD
−0.4%
5.4%
(0.08)
THB
1.6%
6.8%
0.23
TWD
−7.2%
4.9%
(1.48)
CZK
10.3%
12.0%
0.86
HUF
−13.3%
14.4%
(0.93)
ILS
0.4%
7.9%
0.05
PLN
4.4%
13.7%
0.32
RUB
−12.4%
15.0%
(0.83)
TRY
−20.7%
14.5%
(1.43)
ZAR
−20.5%
16.9%
(1.21)
BRL
−10.6%
16.0%
(0.67)
CLP
5.2%
10.3%
0.51
COP
−6.6%
11.8%
(0.56)
MXN
−7.9%
11.3%
(0.70)
PEN
−4.8%
5.9%
(0.81)
Note: Mean returns, volatility, and IRs for a perfect-foresight strategy for two-year swaps.
Source: Bloomberg, authors’ calculations.
4.3
CARRY WORKS – IF YOU ARE JAPANESE
For now, we have only established that rising or falling interest rates, i.e. interest rate
changes, do not act as a systematic driver for EMFX. But maybe the level of rates does
work: after all, buying a basket of high-yielding currencies is the classic carry trade that
often attracts investors to EM in the first place.3 From a practitioner’s point of view,
there are a few ways to investigate this question. First, investors could try (and have
tried) to buy the top yielders outright, often against the USD, but also against the EUR
or JPY, depending on the relevant home currency. These strategies have done well
in the heydays of EM currencies, but their performance has been mostly uninspiring
3For some academic studies, see also Brunnermeier et al. (2008), Gilmore and Hayashi (2011),
Burnside et al. (2007), McCauley and Scatigna (2011), and Heath et al. (2007).

How to Trade EMFX
63
FIGURE 4.2
Carry Returns Funded in JPY Outperform Over the Cycle.
Note: Carry returns of the top four highest ranked carry currencies in
USD, EUR, and JPY terms.
Source: Bloomberg, authors’ calculations.
since 2012. Against the USD, peak performance was reached in 2011. This is not
surprising, as 2011 marked the beginning of the broad USD bull market. While the
carry trade funded in USD returned to its peak performance levels in late 2017, it faded
again in 2018. The EM carry trade has left USD-based investors without any profits
since 2011, as can be seen in Figure 4.2. Investors funding EMFX in EUR or JPY are
obviously performing much better in the recent USD bull market. When considering
performance during the earlier USD bear market, the advantage of EUR or JPY funding
is no longer clear. Still, while the cumulative returns for USD- and EUR-funded carry
trades are almost identical between 2003 to 2018, the EUR-funded trade has a much
higher Sharpe ratio. And the JPY-funded cumulative returns are significantly higher
than EMFX returns funded in either USD or EUR. The popularity of the carry trade
in Japan is therefore not overly surprising. Still, with USD-funded EMFX trades being
prevalent in markets, we conclude that the carry trade in its simplest form has been
eaten up by the USD bull market. We encourage even investors not based in the
Eurozone or Japan to consider diversifying the funding for EM carry plays.
One (slight) improvement can be implemented by taking volatility into account.4
If we rank currencies by carry over realized volatility and then go long the top four
versus the bottom four in a volatility-adjusted way (where the weight of each cur-
rency in the basket depends on how volatile it has been over the previous year), the
P&L improves (slightly), as demonstrated in Figure 4.3. Trading EMFX pairs on a
volatility-adjusted basis is actually something that we find improves alpha opportu-
nities more broadly, also in a single currency pair setting, as has been demonstrated by
Willer and Dabholkar (2019a).
One obvious culprit for the degradation of the simplest carry strategy could be that
the level of carry has fallen, also in risk-adjusted terms. This would be in line with
4See also Moreira and Muir (2017) and Menkhoff et al. (2012) for a more academic treatment.

64
TRADING FIXED INCOME AND FX IN EMERGING MARKETS: A PRACTITIONER’S GUIDE
FIGURE 4.3
Taking Volatility into Account Helps.
Note: Rank of carry adjusted by volatility, and positions weighted by
volatility.
Source: Bloomberg, authors’ calculations.
the outperformance of the JPY-funded strategy, given that carry over the period under
study was highest when funded in JPY. However, Figure 4.4 suggests that this is not
the full story. True, carry was meaningfully higher in the early 2000s, when the carry
strategy was doing well. It was again meaningfully higher than it has been more recently
following the 2008–2009 crisis, when the carry strategy also did well. But since the
carry strategy largely stopped working in 2011, carry has been at times meaningfully
higher than it was during the good old days of either 2007 or 2010. As such, lower
carry offers only a partial explanation for the degradation of the performance of the
carry strategy. Adjusting carry for (realized) volatility is not suggestive of carry being
FIGURE 4.4
Lower Rates Alone are Not To Blame.
Note: Average carry of the carry strategy outright and adjusted by realized
volatility.
Source: Bloomberg, authors’ calculations.

How to Trade EMFX
65
extremely low, either. It is plausible that we need yields for EM currencies to rise quite
substantially, maybe to the levels of the glory days of 2004, for the carry strategy to
come back into favour. But this is unlikely in a global low interest rate environment.
We therefore conclude that the carry strategy in its simplest form no longer provides
sufficiently attractive returns, at least unless the DXY turns.
Investors have been trying several approaches to improve on the simple carry strat-
egy. One early attempt was to strip out the USD directionality by converting it into a
long-short strategy, where investors short the lowest-yielding EM currencies against the
highest yielders. Picking the four top ranked against the four bottom ranked curren-
cies survived the 2008 risk-aversion spike relatively well (performance not shown in a
chart). However, the overall performance is directionally very similar to the long-only
carry strategy, and the high watermark of 2011 had not been reached again by the end
of 2018. And cumulative performance is considerably worse than it is without the short
leg of the basket. But just as with the long-only version, volatility adjustments improve
performance. Figure 4.5 illustrates the P&L when longs and shorts are picked from a
ranking of volatility-adjusted carry. The sizes of the positions are then normalized by
volatility as well. This strategy makes new highs after 2011 and, for now, peaks out
in 2016. It performs better than the long-only strategy that picks only the top four
currencies with the highest volatility-adjusted carry.
In the end, all of these strategies need to be judged by focusing on the IRs. We sum-
marize these ratios for the various USD-funded carry strategies in Table 4.3. While the
long-short setup lowers the volatility of the strategy, this comes at the price of lowering
returns, too. In terms of IRs, a long-short carry strategy beats the EMFX index but does
slightly worse than the long-only carry strategy. Volatility-adjusting the long-short carry
strategy again leads to improvements. But, once more, the IR is actually lower than it
is for the volatility-adjusted long-only strategy, as returns fall by more than volatil-
ity. With the volatility-adjusted long-short strategy making new highs in P&L terms in
2016, it is premature to claim that carry is dead. But at the very least, returns have
clearly deteriorated during recent years.
FIGURE 4.5
Long-Short is Expensive, But Volatility-Adjusted is Less So.
Source: Bloomberg, authors’ calculations.

66
TRADING FIXED INCOME AND FX IN EMERGING MARKETS: A PRACTITIONER’S GUIDE
TABLE 4.3
Volatility Adjustments Are a Good Idea!.
Strategy
Mean
Vol
IR
Long carry
8.7%
10.6%
0.83
Vol-adjusted long carry
8.6%
7.4%
1.16
long-short carry
6.9%
8.8%
0.78
Vol-adjusted long-short carry
7.2%
6.8%
1.05
EMFX benchmark
4.8%
6.2%
0.79
Note: Mean, Vol, and IR calculated from 2003 to 2018.
Source: Bloomberg, authors’ calculations.
FIGURE 4.6
Finding the Best Hedges.
Note: As of December 2018.
Source: Bloomberg, authors’ calculations.
In spite of having demonstrated the high costs of hedging/running a long-short strat-
egy, it is an important concept that there are currencies that are volatile, have a strong
correlation with global risk, and are low positive or at times even negative carry. Such
currencies offer the best hedging opportunities. As an illustration, Figure 4.6 shows
the state of affairs as of the end of December 2018. The three most interesting curren-
cies, with a beta greater than one and negative carry, were the HUF and SEK. To be
less dependent on idiosyncratic country developments, the EUR and CZK may also be
added to such a hedge basket.
The subsequent average spot performance of those four currencies in 2019 was
−3.4%. The volatility-adjusted spot performance of our EMFX index over the same
time was −0.4%. 2019 was therefore a banner year for such hedges, given that the spot
performance does not even account for the positive carry of the basket.
The strategy to use the cheapest hedge actually works relatively well when applied
systematically. We illustrate this point by always finding the cheapest hedge for our

How to Trade EMFX
67
FIGURE 4.7
Low-Cost Hedges At Work.
Source: Bloomberg, authors’ calculations.
EMFX index by comparing the carry of each potential hedge after adjusting for the
beta to the EMFX index. We then pick a basket of the three cheapest hedges to reduce
the impact of idiosyncratic shocks. We go long our EMFX index and hedge with this
hedging basket. Figure 4.7 illustrates the resulting P&L. The hedged EMFX index either
goes sideways (2010 to 2013, and then again 2015 to 2018) or makes money (2013 to
2015). While being long a hedged version of the EMFX index clearly is not making
anyone rich, the hedge works relatively well.
Other refinements of the carry strategy are to time the onset of risk aversion, which
is usually carry negative, and to reduce carry strategies at those times.5 Rising risk
aversion is typically identified by rising implied volatilities. But which risk the market
cares about can be different in every cycle. It can be equity risk, as in 2001–2002; it can
be US rates risk, as in 2013; or it can be risk from oil, as in 2015. FX volatility, for both
G10 and EMFX, can also be a useful warning indicator. Even though the volatilities
for different asset classes are often highly correlated, we believe it is most relevant to
focus on the maximum of such volatilities, rather than on the median or average. This
is the case because EMFX reacts poorly even if only one important global macro driver
starts to deteriorate. To be precise, we define our risk index as the maximum z-score
(with a two-year lookback), of the implied volatilities for EMFX, G10 FX, US rates,
the S&P 500, and oil. The risk index cuts out the long EMFX exposure whenever the
index moves above two standard deviations, and re-enters the long EMFX index when
it falls back below two. The analysis only starts in 2010 because the implied volatility
index for oil begins in April 2009, and we found that implied volatilities are clearly
5For an academic treatment, see also Menkhoff et al. (2012), Egbers and Swinkels (2015), and
Mulder and Tims (2018).

68
TRADING FIXED INCOME AND FX IN EMERGING MARKETS: A PRACTITIONER’S GUIDE
FIGURE 4.8
EMFX: Afraid of its Own Shadow.
Source: Bloomberg, authors’ calculations.
superior to realized volatilities for signalling danger. Figure 4.8 shows that this risk
overlay significantly improves the return even when compared to our volatility-ranked
and volatility-adjusted EMFX long-only carry index.6
4.4
CURRENT ACCOUNTS: MEASURING RISK
THE OLD-FASHIONED WAY
Given that the carry strategy has recently been, at best, a qualified success, we now
investigate the second most important fundamental factor (after interest rates) for a
country when it comes to FX: the current account. Large current account deficits are
negative for currencies during episodes of rising risk aversion, as such deficits have to
be financed, which is increasingly difficult when investors start to flee for the safety
of their home markets. On the other hand, countries with a current account surplus
benefit during crisis times as capital outflows stop (or even reverse), leading to appreci-
ation pressures thanks to a strong current account. Therefore, a positive current account
makes a country safer at times of rising risk aversion. The problem is that the perfor-
mance of the current account factor, here expressed as top four versus bottom four
currencies, ranked by current account balances, is overall money losing. As illustrated
by Figure 4.9, the main episodes of outperformance were the 2008 crisis, the 2013 taper-
ing episode, and, to a lesser extent, the collapse in crude oil in 2014–2015. In 2018, the
strategy also performed well, largely due to idiosyncratic country issues that came to the
fore in both Argentina and Turkey. But those episodes of stress have not been enough to
make the current account factor a profitable strategy unless it is coupled with a strong
view on when risk aversion is going to rise.
6See also Gill (2018). Gill proposes to be long EM only when an EM risk index containing
global economic surprises and data momentum, an EM sovereign bond index, implied volatility
of EMFX options, change in assets in EM ETFs, and EM high beta to low beta correlations is in
its lower 50 percentile.

How to Trade EMFX
69
FIGURE 4.9
Playing It Safe Does Not Pay.
Note: P&L of a strategy that is long four best current account balances versus short
the four worst. We assume zero slippage and transaction costs.
Source: Bloomberg, authors’ calculations.
The problem with the current account factor is that countries with a current account
surplus often have low (real) rates. This is the case because such countries do not need
high rates to compensate investors for the additional risk inherent in a weak external
balance. Therefore, the current account strategy is often exactly the opposite of the
carry strategy. This is why the current account strategy does not perform well during
good times, when money is flooding into higher interest rate countries.7 Figure 4.10
loosely illustrates this relationship for the end of 2018, where real rates are calculated
as (nominal) FX implied interest rates minus current CPI. Countries with a current
account deficit of more than 3% of GDP all offer high real rates. The current account
surplus crowd can get away with much less. Exceptions are few, even though a country
like Russia, for example, chooses to have high real interest rates in spite of the fact
that the market would likely give the central bank room to adjust rates lower without
undermining its currency.
The case of Russia raises the somewhat obvious question of whether those two
factors can be combined into a strategy where high carry plus a decent balance of pay-
ments would make up the longs, while countries with low carry with a poor balance of
payments would constitute the shorts. Of course, to get large carry with a strong bal-
ance of payments position is very rare – and at times can signal other issues (elections,
fiscal, etc). But to illustrate the concept, we test a strategy where we rank countries by
current account balances as well as by carry and then add those two ranks. We then go
long the top four versus the bottom four. However, the results are not overly encourag-
ing (no chart shown). One issue is that the current account numbers move very slowly,
and as such, the rankings are very sticky and do not react much to either improvement
7We note that some of the academic literature also focuses on factors other than current accounts,
such as low FDI, credit buildup, low reserves, and currency overvaluation, that are associated
with large currency crashes (Frankel and Rose 1996). But the basic idea that such risk factors are
usually more than compensated for by carry still often holds.

70
TRADING FIXED INCOME AND FX IN EMERGING MARKETS: A PRACTITIONER’S GUIDE
FIGURE 4.10
Only Risky Borrowers Pay High Rates.
Note: Real rates calculated as three-month FX implieds minus current
CPIs, Dec 2018.
Source: Bloomberg, authors’ calculations.
or deterioration on a timely basis. We therefore also investigate whether an improv-
ing current account is helpful, as long as carry is sufficiently high. For improvements,
we analyse changes in the trade balance. While the trade balance is a much narrower
concept than the current account, the majority of the variation in the current account
usually comes from the trade balance. Furthermore, publication lags are much shorter
for most countries. We define an improvement or deterioration as a six-month change
in the trade balance as percent of GDP. We rank currencies by both this trade improve-
ment and carry, add those two ranks, and then construct a basket that is long the top
four currencies against the bottom four. Figure 4.11 shows the P&L, which is much
better than the one with a static current account focus. Our conclusion is that the best
FIGURE 4.11
Carry Combined with Trade Improvement Works Better.
Note: top 4 against bottom 4 currencies when adding ranks for carry and 6 m
change in trade balance.
Source: Bloomberg, authors’ calculations.

How to Trade EMFX
71
way to use current accounts is to look for improvements, rather than for levels, and
that carry needs to be taken into account together with any current account model to
generate alpha.
INDIA ESCAPES THE CLUB OF THE FRAGILE FIVE
2013 was the year of tapering by the Fed. As usual, the onset of tightening by the
Fed had significant negative spillover effects on EM. Morgan Stanley is credited
with coining the term Fragile Five for the group of countries that were going to
feel the impact of the liquidity withdrawal in the most acute fashion. Those five
fragile countries were Indonesia, South Africa, Brazil, Turkey, and India. As is
typical when worrying about quickly disappearing liquidity, those countries were
largely chosen based on the size of their current account deficits. The five countries
sported current account deficits ranging from -3.2% in Indonesia to -6.7% in
Turkey. India certainly fit well into the group, with a current account deficit of
around 5% of GDP (and a consolidated fiscal deficit of around 7% of GDP). The
currencies of the Fragile Five were the worst performers in spot terms in 2013,
and again, India fit in well, with the INR weakening by almost 12% that year.
But then external balances started to improve in India. The 12-month rolling
trade balance bottomed out in June 2013, an event that became obvious by
September 2013. The improvement was initially driven by general government
belt-tightening measures and by lower gold imports (due to the government
imposing a 10% import tariff on gold, which is important in India: it accounted
for around 25% of India’s trade deficit at the time). In July 2013, the INR
started to meaningfully outperform IDR (which we use as a funding currency to
remove the overall directionality of USD-Asia). As can be seen in Figure 4.12, the
FIGURE 4.12
INR Changes Trend with Improving Trade Balances.
Note: Twelve-month MA of Indian trade balance versus INR-IDR.
Source: Bloomberg.
(Continued)

72
TRADING FIXED INCOME AND FX IN EMERGING MARKETS: A PRACTITIONER’S GUIDE
INR outperformance started at a time when the current account deficit was still
reasonably large. But the change in trend, combined with continued intervention
by the RBI, was enough to convince the market that India was on its way to becom-
ing less fragile. In a second leg, falling oil imports also contributed to the current
account adjustment as oil prices started their large sell-off in the second half of
2014 – a lucky occurrence that the Indian government used to lower subsidies for
fuel prices, cutting oil demand on a more permanent basis. By 2015, the current
account deficit stood at -1.3%: fragile no more.
4.5
GOING FOR GROWTH
Other than carry and external position, the other major attraction of EM has been
that growth tends to be higher than in DM, as EM are catching up with the living
standards and know-how of developed countries (although we note that recently, not
much catch-up has been in evidence). Historically, periods of strong EM growth have
on average been good for the performance of EMFX. But the correlation is not as strong
as a naive discussion would suggest. The reason is that at times of high global growth,
the Fed typically hikes rates. Such rate hikes often undermine the positive impact of
strong EM growth. The most beneficial part of the growth cycle is early on, when
growth differentials start to improve in favour of EM but the Fed is still in the ini-
tial phase of its hiking cycle where monetary policy is still relatively easy. This interplay
between growth differentials and the Federal Reserve is illustrated in Figure 4.13. The
2004 to 2006 Fed tightening cycle is a case in point. Initially, EMFX performed well
as growth differentials between EM and G3 started to increase, even though the Fed
also started its tightening process. But then, from 2005 onward, EMFX started to go
sideways in spite of a continued rise in growth differentials. The Fed hikes had started
to bite. Only when the Fed moved on hold in 2006 did EMFX begin to rally again.
The peak in EMFX performance came just as growth differentials reached a peak of
around 7%, which happened during the Great Recession in the US. EMFX then fell
hard when growth differentials subsequently narrowed. But interestingly, EMFX then
FIGURE 4.13
High EM Growth Differentials and Easy Money are Bullish for
EMFX.
Source: Bloomberg.

How to Trade EMFX
73
recovered and largely range traded even as growth differentials moved lower. Only when
growth differentials entered a new range of around 1.5 to 3%, did EMFX start to sell
off more significantly. The story was the same during the Fed hiking cycle that started
in December 2015. The early part of the Fed hiking cycle was tolerable for EMFX, as
growth differentials started to improve again. It was the latter part of the Fed hikes that
began to undermine EMFX at a time when growth differentials stopped rising.
A more precise and higher-frequency approach to analyse the importance of the
growth factor is to focus on the economic indexes: for example, those produced by
Citi’s excellent quant FX group. Those indexes are constructed as a MA of the eco-
nomic growth surprises vis-a-vis Bloomberg expectations, with a weighting that is in
line with the importance of the indicator for the FX markets. While we found that
bottoming economic surprise indexes for EM are not overly supportive for EMFX, we
note that whenever the EM economic surprise index starts to move more strongly into
positive territory, the likelihood for EMFX to put in a short-term bottom, followed
by a significant EMFX rally, rises significantly. This finding makes intuitive sense to us
because those surprise indexes are by construction moving to zero over time, even if
nothing really changes, just as previous negative (or positive) surprises drop out. And
moving to zero does not appear to move the needle for EMFX. It takes actual positive
growth surprises to get the index into positive territory, and that does move the needle
for EMFX.8 Noual has demonstrated the utility of the surprise indexes for G10 FX
trading more broadly (Noual 2015).
Figure 4.14 illustrates the performance of a strategy that goes long EMFX
when Citi’s EM economic surprises cross the zero line from below and short EMFX
when surprises cross back below zero. The P&L is meaningfully positive and relatively
FIGURE 4.14
EMFX Likes Growth.
Note: P&L of a strategy that uses crossovers over the zero line of the Citi
EM economic surprise index. We assume zero slippage and transaction
costs.
Source: Citi, Bloomberg, authors’ calculations.
8This has also been demonstrated for the EMFX asset class by Willer, Costa, and Garg (Willer
et al. 2019). Kasikov has demonstrated that the strategy also works in a cross-sectional context
where the currencies with the volatility-adjusted highest surprise indexes outperform (Kasikov
2018).

74
TRADING FIXED INCOME AND FX IN EMERGING MARKETS: A PRACTITIONER’S GUIDE
consistent. Interestingly, the strategy performs less well when the spread against the US
economic surprise index is used. At the end of 2018, the growth factor was the most
consistently profitable factor for EMFX trading. We conclude that growth does play
an important role for trading EMFX, even as the focus on surprises suggests a more
subtle relationship than the classical focus on growth differentials.
4.6
MODEST VALUE IN VALUATION
For most asset classes, valuation is an important aspect of trading, as it often can serve
as an anchor for how far asset prices can move. The bad news in the case of FX is
that valuation means very little. While there are a few classical concepts for how to
value FX, they are, in our view, not overly compelling. Maybe this is why chartists are
especially prevalent in the FX business. Without a valuation anchor, a focus on charts
and technical analysis can become irresistible. In spite of the difficulties in applying
valuation concepts to FX, extreme readings should be taken into consideration in the
investment process, and we therefore go through some simple concepts of valuation
for FX.
The most straightforward way to think about valuation is to generate a long history
of real effective exchange rates (REERs) and analyse how cheap a currency is compared
to its past. Here, the “real” aspect of the REER concept corrects exchange rates for infla-
tion differentials, which can be done using PPIs, CPIs, or unit labour costs (Harberger
2004). The “effective” aspect takes the composition of the export and import desti-
nations into account. But all other fundamentals are assumed to stay constant, which
clearly is an oversimplification that is rarely reflective of reality. The other problem with
the REER concept is that the indexes were at some stage arbitrarily set to a predeter-
mined initial value before they started to move in line with spot FX moves and inflation.
But as the initial starting point was not necessarily set to a time period when the cur-
rency was fairly valued, it is very hard to interpret the level of the REER index. Still,
investors use deviations from the REERs, partly because the view is that the concept of
valuation can only work when valuations are very significantly out of whack. At such
extremes, simple valuation models, like REER-based ones, often give the same answers
as more complicated models.
One straightforward way to implement REER models is to calculate deviations
from a rolling MA. These deviations are then translated into z-scores. The model goes
long the highest z-scores and short the lowest ones. In theory, this approach should work
principally for very long lookback windows to be able to focus on the more extreme
readings. In Figure 4.15, we use a lookback window for the z-scores of 10 years and,
as usual, choose the top four z-scores against the bottom four on a volatility-adjusted
basis. However, as can be clearly seen, the results are far from impressive.9
9In the academic literature, it is also demonstrated that for G10 FX, simple valuation measures
like REER and HP-filtered REER do not generate alpha, though filtering currencies included in a
carry strategy for extreme over- or under-valuations has proved to be more useful (Nozaki 2010).

How to Trade EMFX
75
FIGURE 4.15
Valuation: Focus on PPP.
Source: Bloomberg, IMF, authors’ calculations.
The second strategy plotted in Figure 4.15 uses the same ranking approach, but for
purchasing power parity (PPP) rather than REER. The PPP approach was popularized
to get around the fact that REER depends on arbitrary initial conditions. The PPP valu-
ation measure suggests that similar goods should cost similar amounts of money across
countries. If they do not, free trade should go into overdrive, quickly correcting such
arbitrage opportunities. Of course, for many goods, transaction costs can be substan-
tial. Still, given that in the last 20 years, the US outsourced the bulk of its manufacturing
capacity to China, it does not seem to be the case that transaction costs are large enough
for the PPP concept to break down. There is a question of which basket of goods to apply
the PPP concept to. The Economist magazine popularized one version of the PPP: the
Big Mac index. This is almost certainly too narrow a measure. We use PPP indicators
from the IMF, which are much broader, though we imagine that in the age of big data
and web scraping, much more reliable PPP measures can be constructed going forward.
But given that we mostly care about big picture, glaring misvaluations, the marginal
effort to improve FX trading should be exerted elsewhere. Interestingly, the P&L of the
PPP strategy is overall much stronger than that of the REER-based strategy. While the
two P&Ls behave similarly during most periods, PPP outperformed significantly in both
2005–2006 and then again in 2018. We have the sense that currently, REER has more
mind share with investors than PPP does, maybe because it is updated more frequently.
This is a mistake, and we urge investors to focus more on PPP than on REER.
We don’t think that our finding of better returns from PPP is very model-specific.
Table 4.4 shows the IRs for both strategies in relation to the lookback window for deter-
mining the z-score. PPP is superior across all look-back windows. Another interesting
finding is that for both strategies, there is a relatively consistent improvement, the longer
the lookback period. In both cases, the 10-year window offers the best IR (data avail-
ability prevents us from testing even longer time horizons). To the extent that valuation
adds any alpha, it does more so for investors who have a very long-term perspective on
valuation.

76
TRADING FIXED INCOME AND FX IN EMERGING MARKETS: A PRACTITIONER’S GUIDE
TABLE 4.4
The Longer, The Better.
Lookback (years)
IR – REER
IR – PPP
1
−0.41
0.0
3
−0.24
−0.01
5
−0.26
0.19
7
−0.18
0.29
10
−0.06
0.35
Note: IRs for valuation strategies going long the four cheapest against the four most expensive
currencies. We assume zero slippage and transaction costs.
Source: IMF, Bloomberg, authors’ calculations.
4.7
TERMS OF TRADE
A slightly more sophisticated version of a valuation strategy aims to take account of
the fact that a country’s competitive position does not remain constant over time. In
particular, REERs should get more expensive if the productivity growth of the country
in question outpaces the rest of the world, or if the terms of trade (ToT: Export prices
divided by import prices) of the relevant country improve significantly.10 With pro-
ductivity being relatively stable over short horizons (and also being notoriously hard
to measure), changes in ToT are more relevant for short-term trading horizons. Sig-
nificant changes of the ToT over a short period of time are typically due to changes
in the prices of commodities that a country imports or exports, largely because com-
modity prices are much more volatile than prices of manufactured goods or services.
For that reason, our focus is on commodity ToT, which assumes implicitly that the
prices of non-commodity imports and exports remains constant in relation to each
other. In this discussion, we use Citi’s commodity terms of trade (CTOT), also pro-
duced by the Citi FX quants, to adjust our simple REER framework.11 In particular,
we run a five-year rolling regression of the log of the REER of the relevant currency on
its CTOT. We then calculate z-scores of the residuals with a two-year lookback win-
dow. While a longer lookback window would likely be preferable, given Table 4.4,
the more limited history of the CTOT indicator forces us to shorten the window. Two
years is a good trade-off between data availability and model fit. As the next step, we
volatility-adjust the currencies and create a top four against bottom four basket accord-
ing to the z-scores. The result is shown in Figure 4.16 for the period from 2008 to 2018.
The strategy has an IR of 0.4, a significant improvement over the (full sample) period
IRs for the simple REER strategy, as well as for the IR of the simple REER strategy for
10See also Coudert et al. (2008) and Cashin et al. (2004).
11Stephens demonstrates that momentum in the CTOT indicator results in profitable trading
strategies, but only for commodity currencies in Latam and CEEMEA. Those results were better
than using momentum in the currencies. The strategy worked particularly well during time of
high commodity volatility (Stephens 2010).

How to Trade EMFX
77
FIGURE 4.16
ToT are Helpful for FX Valuation.
Note: P&L of a strategy that adjusts REER by CTOT. We assume zero slippage
and transaction costs.
Source: Citi, Bloomberg, authors’ calculations.
the period from 2008 to 2018. Our conclusion is that adjusting valuation for changes in
the CTOT is helpful. Even so, an IR of 0.4 likely means that valuation is not tradable as a
standalone strategy.
4.8
TECHNICALS TO THE RESCUE
Given that the IRs of some of the classic fundamental rules for FX trading are at times
quite low, considerable effort has been placed on technicals. The absence of a strong
valuation anchor has made technicals even more relevant for FX than for other asset
classes. This book will not go through all the various technicals that have been proposed
over the decades. Our view is generally that we need a precise trading rule for how to use
a specific technical. Many technicals are not precisely defined, especially with respect to
exit conditions, but are used by practitioners as an art form rather than a science. This
reminds us of astrology before astronomy came along! Today, astronomy – in the form
of increased computing power – arrived for FX, and we can backtest proposed technicals
more carefully. Doing this leads both to discarding many popular technicals and to
false discoveries of new technicals due to overfitting. While this research is evolving, we
think there are three very basic concepts on which most technicals rely in one way or
another: momentum, mean reversion, and breadth. Obviously, the first two concepts
are the opposite of each other; but they can both be helpful, largely because they can
work on different time horizons. Here, we discuss one basic technique that is helpful in
generating alpha for each category of technicals. While there are more refined techniques
that can work better, we illustrate the basic concepts and capture the main sources of

78
TRADING FIXED INCOME AND FX IN EMERGING MARKETS: A PRACTITIONER’S GUIDE
alpha that can be generated by purely technical rules. If those simple rules completely
break down, more sophisticated ones may also struggle.
We start with momentum. There are many different ways to implement
momentum-based trading rules. In its simplest form, a momentum strategy sug-
gests that investors buy the currencies that went up the most over a certain period and
sell the ones that fell the most over the same time. The behavioural foundation for
momentum is that investors tend to follow herding behaviour. And there is nothing
better than quickly rising prices to create greed (or quickly falling prices to trigger
fear) and to lead investors to buy (or sell). There are absolute and relative momentum
strategies. Absolute momentum invests in assets that go up more than a certain
threshold, while relative momentum ranks all FX pairs based on momentum and then
goes long the top momentum pairs against the lowest-ranked momentum pairs. Most
CTAs (commodity trading advisors, who typically have a fast trading mindset) combine
several strategies across relative and absolute momentum with varying performance
windows that measure momentum.
Table 4.5 shows the IRs for the various relative momentum strategies in EMFX.
We show results for long-only momentum (top four currencies) and for long-short
momentum (top four versus bottom four). We also show the volatility-adjusted ver-
sion for both strategies. Volatility adjustment is done in two respects. First, the actual
momentum is volatility-adjusted; and second, the weight of the currencies in the bas-
ket is adjusted for volatility. We also add a (volatility-adjusted) absolute momentum
strategy. The absolute momentum strategy could be long four currencies, short four
currencies, or long two and short two, for example, depending on how many longs or
shorts appear in the top four currencies ranked by absolute momentum. We have a few
observations. First, for all specifications, using short-term momentum works best. For
four out of the five strategies, one-month momentum displays the strongest returns,
while for one strategy, three-month momentum is slightly better than one month. Sec-
ond, volatility-adjusted momentum is superior for all strategies and time horizons. This
is similar to the improvements we found when using volatility adjustments for the carry
strategies. And finally, the long-only momentum strategy creates higher IRs than the
long-short version, both outright and volatility-adjusted.
Figure 4.17 shows the one-month, volatility-adjusted P&L for the long-only and
long-short momentum strategies over time. While an IR of 0.86 should be tradable,
TABLE 4.5
Momo Works, in the Short Term.
Long-only
Long-short
Absolute
momentum
Vol-adj. mom.
momentum
Vol-adj. mom.
momentum
1M
0.64
0.86
0.38
0.62
0.75
3M
0.37
0.56
0.07
0.27
0.79
6M
0.35
0.60
0.20
0.36
0.55
12M
0.20
0.42
0.06
0.33
0.30
Note: IRs, assuming zero slippage and transaction costs.
Source: Bloomberg, authors’ calculations.

How to Trade EMFX
79
FIGURE 4.17
Momentum: Not Bad, But Not the Good Old Days, Either.
Note: One-month momentum, volatility-adjusted. We assume zero
slippage and transaction costs.
Source: Bloomberg, authors’ calculations.
we point out that there are meaningful drawdowns. Furthermore, it does appear that
the heydays of the strategy were prior to the Great Recession of 2008, rather than
during the last 10 years. More encouragingly, the long-only and long-short momentum
strategies display negative correlation, especially during drawdowns of the long-only
strategy in 2008 and 2014. Combining both strategies should therefore improve results.
For mean reversion, the basic idea is that assets can go in one direction for only
so long. At some stage, no potential sellers (or buyers) are left, causing the asset to
reverse from such oversold conditions. For mean reversion, we tend to focus on longer
time horizons: not so much because there cannot be mean reversion on shorter horizons
(there likely is), but because we are not overly interested in daily returns and therefore
prefer to focus on overbought or oversold conditions in the bigger picture. The simplest
way to analyse mean reversion is to just extend our momentum study further out in
time. Figure 4.18 shows the case of a momentum strategy for three-year momentum.
The long-only strategy becomes reliably negative, suggesting mean reversion setting in
on a three-year horizon. But this variety of mean reversion clearly is not tradable on a
standalone basis, as the P&L indicates. And the long-short version of the strategy still
ekes out positive returns for momentum. In practice, long-term mean reversion needs
to be combined with short-term momentum to improve results.12
Breadth is the third important technical concept that we need to discuss, as we found
it useful for EMFX trading purposes. The idea of breadth is that a healthy market is
characterized by most assets with similar characteristics going up together. If gains for
an asset class are driven by only a few exceptional assets, the rally is at risk of coming
to an end. This could happen as soon as those few leading assets are hit by a negative
12This has been studied by various authors, including Serban (2018). See also Gill and Dingman
(2019). The authors have some success in finding mean reversion on shorter horizons and are
able to improve on returns by focusing on currency pairs that have similar drivers.

80
TRADING FIXED INCOME AND FX IN EMERGING MARKETS: A PRACTITIONER’S GUIDE
FIGURE 4.18
In the Long Run, Momentum is Dead.
Note: Three-year momentum with zero slippage and transaction costs.
Source: Bloomberg, authors’ calculations.
shock, or when the gains of the leading assets come to an end as valuation differences
conpared to the laggards become too extreme.
We focus on an expression of breadth in EMFX where we count the number of up
days over different time periods for all the EMFX currencies under consideration. It
turns out that when breadth is improving, it pays to be on the long side of EMFX. The
opposite is true when the indicator deteriorates. We show the P&L of a simple version
of this rule in Figure 4.19. The breadth rule is not very early or helpful in calling turns
for the EMFX market. But it does keep investors on the right side of the market, even
though the 2010 to 2016 performance was only sideways.
FIGURE 4.19
The Importance of Good Breadth.
Note: P&L of the MA of up minus down days. We assume zero slippage
and transaction costs.
Source: Bloomberg, authors’ calculations.

How to Trade EMFX
81
4.9
FLOWS FOLLOW; DON’T FOLLOW THE FLOWS
The other tool market participants focus on to a larger extent in FX than in other
asset classes is flows. Again, this is because fundamentals in general and valuation in
particular are much less clearly defined than in some other asset classes. There is also
some fundamental justification for this sharp focus on flows, because in FX markets
many players transact for reasons that are not, strictly speaking, profit maximizing.
Important examples are governments intervening for financial stability reasons or to
fight inflation. Furthermore, corporate hedging behaviour can lead to FX flows even
when those corporates don’t necessarily expect the outcome they hedge against to mate-
rialize as a base case. As a result, research on flow has become a cottage industry in the
FX world. A lot of this flow research just takes publicly disseminated flow data – for
example, from an equity exchange – and aggregates the flows, sometimes with a bit
of data-mining on top, to determine which flows are more relevant in terms of setting
prices. For longer-term flows, such an aggregation also uses balance of payments data
disseminated by international or national statistics agencies. Many banks essentially
engage in the same exercise, and a few are able to add their own proprietary FX flows.
Recently, more and more flow data has become available, as web scraping of investor
filings leads to more data along those lines.
We are broadly sceptical that flows are very useful for forward-looking analysis. To
our mind, flows largely follow, or are at best coincident with, price action, rather than
leading prices. We illustrate this point first with equity flows and then with FX flows.
Focusing on equity flows has the advantage that the data are timely and of relatively
high frequency, given that equities are mostly exchange traded. For fixed income, we
don’t usually have similarly rich data sets. Equity investors also typically do not FX
hedge their shares, or at best do so partially; while in fixed income, the inflows from
crossover investors are often FX hedged. Given that Asia is characterized by significant
equity flows, while Latam and CEEMEA are more driven by significant fixed-income
flows, we focus here on Asia FX and how it relates to equity inflows into Asia. We use
deviations from the 200-day MA for both flows and FX to de-trend the series. As can
be seen in Figure 4.20, at almost all the bottoms and tops, Asia FX is leading or is, at
best, co-incident with the flows into Asian equity markets. Such flows are therefore not
very useful to trade Asia FX. Having said that, there is one interesting observation to be
made in Figure 4.20: the strong performance in Asia FX in 2017 was never corroborated
by strong inflows into the Asian equity markets. In the end, equity flows were correct.
Growth in Asia never recovered sufficiently to be supportive for Asia FX, and 2018
turned out to be a very poor year for Asia FX in particular but also EMFX more broadly.
On the FX flow side, we show the z-score of Citi’s FX flows into and out of EMFX
by leveraged accounts, next to the z-score of the EMFX index. We concentrate here
on flows from leveraged investors, given that correlation with price action is higher
for such flows, and given the perception that leveraged investors move faster than real
money investors. As such, if flows were leading, we would expect this to manifest itself
mostly on the leveraged investor side. But once again, as can be seen in Figure 4.21, at
most times flows are coincident or lagging at both peaks or bottoms. What does happen
from time to time, though, is that leveraged flows accelerate post turning points, and

82
TRADING FIXED INCOME AND FX IN EMERGING MARKETS: A PRACTITIONER’S GUIDE
FIGURE 4.20
Asia FX Leads Equity Flows.
Source: Bloomberg, authors’ calculations.
FIGURE 4.21
FX Flows are a Lagging Indicator.
Source: Citi, Bloomberg, authors’ calculations.
those accelerations can be leading price action. This happened in early 2016 and then
again in late 2018. As such, while we don’t focus too much on flows, we do keep an
eye open for surges in leveraged inflows that are not immediately coincident with too
much EMFX strength (i.e. the z-score of flows moving above one, while the z-score for
EMFX stays below one).
While the idea that large inflows from hedge funds are indicative of positive for-
ward returns is not overly intuitive, especially if there is no instant gratification for such
funds, the CitiFX quants have also had some success generating alpha using flows from
leveraged accounts. They have found that momentum in leveraged flows on a three- to

How to Trade EMFX
83
four-week basis tends to be a positive signal for the relevant currency. Flow momentum
is most likely correlated with the price momentum strategy, given that flows for lever-
aged money are highly correlated with price action. But the CitiFX quants were able
to refine the strategy by also integrating flows from real money investors. Real money
investor flows are also positively correlated with price action, but to a lesser extent than
flows from leveraged accounts (while flows from banks and corporate flows have no sig-
nificant positive correlations with price action). CitiFX quants focus on events where
momentum in flows from leveraged accounts is going in the opposite direction as the
momentum of flows from real money accounts. The idea is that leveraged accounts are
often moving first, and, in the end, real money will more often than not follow, creating
some persistence to the overall flows. CitiFX Quants have had some success with such
a trading strategy (Dingman and Gill 2018).
The other way to use FX flows is to think of them as a proxy for positioning,
especially for currencies where no reliable positioning data exists. We mostly consult
FX flow data for this purpose when we observe news that seems to change the prevail-
ing consensus narrative for that particular currency. Extreme positioning, as proxied by
flows, is relevant in determining whether investors should take the other side of consen-
sus on the first sign that the consensus story may be changing. Using flows this way does
not lend itself to any easy back-testing. We therefore remain careful when it comes to
using flows in this manner and see it mostly as one additional reason to engage in a cer-
tain trade, but rarely a particularly important one. The following box illustrates a use
case of flows for MXN.
WHICH PRESIDENT IS THE BIGGER MXN FOE: TRUMP OR AMLO?
The Mexican peso, one of the most liquid emerging market currencies, had a rough
few years. First it became the most popular way to position for a Trumpian trade
war, which initially was directed against the NAFTA treaty rather than against
China. Therefore, the election of President Trump in November 2016 was a major
hit for the MXN. Mexico stood out in the NAFTA context because investors were
initially less concerned with Canada due to the more balanced trade flows between
Canada and the US. The other pivotal event for the MXN in recent years was
the election of President Andrés Manuel López Obrador (AMLO) in Mexico in
July 2018. Prior to the election, AMLO had been perceived as a leftist politician
who would likely be quite market unfriendly and, in particular, would aim to
reverse the all important energy reform of the previous market-friendly admin-
istration. From a fundamental point of view, it would not have been obvious
which of the two new presidents, Trump or AMLO, would undermine Mexi-
can fundamentals more. If President Trump had pulled the US out of NAFTA
without a quick replacement agreement, the damage to Mexican exports would
have been substantial, given that the US administration would likely have levied
major tariffs on Mexican goods in that case. But AMLO reversing the energy
reform would have meant that Pemex’s oil output would likely continue on a
(Continued)

84
TRADING FIXED INCOME AND FX IN EMERGING MARKETS: A PRACTITIONER’S GUIDE
one-way street lower, substantially undermining the external and fiscal position
of Mexico. Ex ante, these fears would have suggested to investors that they keep
buying USD-MXN after both the Trump election as well as after the AMLO elec-
tion. In the event, the day after the AMLO election, the MXN swung widely but
ended the day only slightly weaker. The next day, USD-MXN started to move
lower aggressively, though, and the MXN kept rallying for a month. After the
Trump election, on the other hand, USD-MXN exploded higher and then kept
going for two more days, only peaking out two months later. The right answer,
therefore, would have been to buy USD-MXN after the Trump election but to sell
USD-MXN after the AMLO election, even though both elections were arguably
a negative shock for Mexican fundamentals. Clearly, expectations matter, and
AMLO was largely expected to win while Trump was not. But this is not the full
explanation for the differing market reaction. After all, there was still a question
mark regarding whether investors were really positioned for an AMLO victory,
given that USD-MXN had moved lower into the election, suggesting that some
investors had at the very least taken off their bearish positions. In this situa-
tion, analysing the flows would have helped. Figure 4.22 shows that leveraged
money went very long MXN into the US election, with the z-score of cumu-
lative positioning close to three. Real money investors also went long into the
US election, but inflows into the MXN from real money had been on a smaller
scale. With everyone long, no wonder the MXN sold off very viciously on the
Trump election, and entering USD longs even after the event would have been
profitable. On the other hand, going into the AMLO election leveraged money
was also long MXN, but to a much lesser extent, having reduced long positions
FIGURE 4.22
Is Trump Really Worse for Mexico than AMLO?
Source: Citi and Bloomberg.
(Continued)

How to Trade EMFX
85
into the event. And real money had been short MXN. These flows into the event
explain why the up move in USD-MXN on the day after the election was small,
and why the USD turned lower very fast. It is also noteworthy that leveraged
money reduced MXN longs after the Trump election but added to MXN longs
after the AMLO election. Real money investors, on the other hand, added to MXN
longs after the Trump election, but kept selling the MXN after the AMLO election,
again highlighting the earlier point that leveraged money flows are more highly
correlated with price action (though they may be following price action more than
creating the price action).
4.10
POSITIONING WITH POSITIONS
Flows lead to positions, but depending on the choice of starting point, positioning can
be very different from flows. Furthermore, when focusing on flows from real money
investors, it is unknown whether flows result from inflows into the fund, and therefore
do not lead to an off benchmark position, or whether flows are due to the fund man-
ager implementing a new position against their benchmark based on a country call, for
example. Therefore, we examine positioning separately from flows. The most widely
available positioning data are the CFTC data, which the CFTC publishes for its traded
future products. Sadly, for EM, only the MXN is traded in that fashion with any liquid-
ity, though other currencies are starting to become more liquid in futures space. While
there are a multitude of other positioning data around, often survey-based, we will use
the MXN CFTC position as an illustrative example of how to think about positioning.
Table 4.6 buckets positioning of investors in USD-MXN into percentiles. The 90th
percentile is very long MXN, while the 10th percentile is very long USD. For this
TABLE 4.6
Consensus is Good For You!
Positioning
USD-MXN
Excess
percentile
3m forward
returns
[0.0, 0.1]
2.4
1.0
(0.1, 0.2]
2.7
1.3
(0.2, 0.3]
1.1
−0.3
(0.3, 0.4]
0.1
−1.2
(0.4, 0.5]
4.1
2.8
(0.5, 0.6]
−1.3
2.7
(0.6, 0.7]
3.2
−1.9
(0.7, 0.8]
−1.8
3.2
(0.8, 0.9]
0.4
1.0
(0.9, 1.0]
1.2
0.2
Note: USD-MXN three-month forward returns and excess returns by percentile of speculative
CFTC positioning.
Source: Bloomberg, authors’ calculations.

86
TRADING FIXED INCOME AND FX IN EMERGING MARKETS: A PRACTITIONER’S GUIDE
exercise, we first translate CFTC contract data into USD numbers. After all, presumably
most of the trading on the exchange is done by offshore investors, who mostly think
about the risk they are taking in USD terms, rather than in MXN terms. When choosing
the lookback windows to calculate the percentiles, the main consideration should be
what type of moves in USD-MXN we are trying to capture. If we choose a long look-
back window that includes the Great Recession, extreme readings will be very hard to
come by. But too short a window creates the perception of extreme positioning much too
early. We chose a lookback window of three years for this exercise, which appears to be
a good compromise. We then show three-months forward returns of USD-MXN given
that for our purposes, three months is a realistic time horizon to judge whether a trade
“worked” or not. We also calculate excess returns, which are the return for the given
percentile minus the average return over the period under study, adjusted for whether
investors are long or short. From 0.0 to 0.5, a larger move up in USD-MXN than aver-
age is a positive excess return. From 0.5 to 1.0, a larger move up in USD-MXN than
average is a negative excess return.
To us, the most interesting finding is that consensus usually works. For 7 of the
10 percentiles, excess returns are positive; and the average excess return is positive and
relatively large at 0.9%. Furthermore, it is not obvious that more extended positioning
leads to worse returns. While the 0.0 to 0.1 percentile does not generate the very best
excess returns for being long USD, it does generate excess returns that are positive and
considerably higher than returns for some of the lower brackets. The same is true, to a
lesser extent, on the other end of the distribution. The 0.9 to 1.0 percentile also generates
positive excess returns, as do several other brackets where investors are short USD, even
though in absolute terms those trades are money losing, given that the period under
study (post crisis: 2010 to 2018) was more often than not a USD bull market. There
is no indication in the data that positioning works as a counter-indicator. If anything,
going with consensus tends to make it more likely for a trade to work. We therefore
would use positioning more as a momentum indicator than a contrarian indicator.
One other interesting study focuses on the EM bond index overall. In Willer and
Dabholkar (2019a), it is shown that when most real money EM funds outperform in a
bull market, it is typically not a counter-trend signal. Forward returns remain positive
on a three-months basis. However, when most real money EM funds underperform in
a bear market, there is usually follow-through in terms of additional negative perfor-
mance. Three-months forward returns are reliably negative in that case. The reason is
that real money funds are forced by price action to exit large money-losing long posi-
tions, prolonging the downmove. But they are not selling long positions when they are
outperforming the index. This is in line with the famous finding by Kahnemann that
a loss of one USD hurts twice as much as the pleasure gained by a gain of one USD
(Kahnemann 2011). As a result, losses beget losses, and shorting EMFX in periods
when the EM fund industry broadly loses money being overweight is a money-making
strategy.
4.11
GOING WITH THE SEASONS
Seasonals are also given relatively high importance in FX trading. In particular, the
subset of FX flows that are not driven by purely economic reasons may be partially
calendar dependent. Examples are dividend payments by important corporates,
year-end liquidity requirements by corporates and banks (partly for accounting

How to Trade EMFX
87
FIGURE 4.23
Respect the Seasons.
Note: P&L of positioning for weekly seasonals with excess returns of more than
1%, volatility-adjusted (rolling 1yr). We assume zero slippage and transaction
costs.
Source: Bloomberg, authors’ calculations.
purposes), and others. Famously, remittance flows into Mexico surge in May for
Mother’s Day – though this is a case where flows are too small and too well understood
to impact price action much. Still, when having a choice of positioning in line with
seasonal patterns that come with a fundamental explanation versus patterns that
do not have an underlying logic we can fathom, we prefer to position for and with
flows that we fundamentally understand. We find that such flows are often not fully
arbitraged. But we have an open mind for trading seasonals even where we do not fully
understand the underlying reason for the seasonal behaviour.
To study seasonals in a more methodical fashion, we use a 10-year lookback win-
dow to estimate weekly seasonals (rather than the more typical monthly seasonals). We
define a week as any five weekdays, irrespective of the starting day of the week. This con-
trols for the fact that just numbering the weeks in the year would lead to significant shifts
over the years that make comparisons with respect to the same calendar days more diffi-
cult. Seasonals are defined as the median return for any given week minus the average of
all weekly medians. We run this study for all of the liquid EMFX. A long-short position
for our strategy is triggered when the seasonals are more than 1% higher/lower than the
median. We then volatility-adjust the P&L streams for all the currencies and add them
up. The results of our study are illustrated in Figure 4.23. Clearly, in aggregate, season-
als add alpha with an IR of 1.0. For individual currencies, the strategies are not quite as
good; but 15 out of 21 currencies tested have a positive IR, with the highest IR achieved
by the ZAR at 0.95 and the lowest by TRY at -0.4. Outside of the ZAR, other tradable
seasonal strategies are found for the ILS, CLP, SGD, KRW, and THB, in that order.
4.12
VOLATILITY: FOE, NOT FRIEND
While volatility has, over the last decade, become its own asset class, in this chapter
we are more interested in considering how to use volatility for directional FX trading.

88
TRADING FIXED INCOME AND FX IN EMERGING MARKETS: A PRACTITIONER’S GUIDE
To our mind, there is some confusion about what volatility means for trading. This is
illustrated by the fact that banks often blame weak trading results on a lack of volatility,
only to blame losses at other times on specific high-volatility events. Volatility appears to
be a positive, but only when you happen to be on the right side of it. For EM investors,
low volatility is seen as a major positive because, usually, investing in EMFX means
investors are long carry. If volatility is low, investors are able to accrue the carry without
heightened risk of capital losses. Furthermore, when investors conclude that they are
in a low-volatility regime, they tend to add to carry trades, which often leads to an
appreciation of the high-carry currencies in question – generating capital gains on top
of the gains from carry. Often, investors rank the attractiveness of currencies by carry
over volatility, where volatility can be either realized or implied.
However, it also is well established that rising volatility is a negative for carry trades,
while falling volatility is a positive. Volatility is highly directional. Given that volatility
is broadly mean reverting and can fall the most when it is high and rise the most when
it is low, one could argue that periods of very high volatility are good entry points for
carry trades, while periods of low volatility are inherently dangerous.
To analyse whether investors should be more bullish when volatility is (very) high
or (very) low, we analyse the following trading rule. We go long EMFX whenever the
implied volatility enters into the top fifth percentile over the last two years. We keep the
holding period a relatively short six weeks, to not be at the mercy of the general bull
or bear market in EMFX. We also show the P&L of the opposite strategy: going long
EMFX for two weeks whenever implied volatility drops into the bottom five percentile.
As is demonstrated in Figure 4.24, going long EMFX, even at volatility levels that are
already very high, is still a money loser. On the other hand, buying EMFX, even at
volatility levels that are already extremely low, not only makes money, but does slightly
better than the index. Low volatility can stay low for a very long time and therefore
is not a compelling signal of danger. The few instances where low volatility leads to
compelling short opportunities are just occurring too rarely. Still, we feel that if low
volatility is the main rationale to buy EMFX, it is important to make use of this low
volatility by using options to express an EMFX bullish view. This also means that when
ranking EMFX, using implied volatility is superior to using realized volatility.
On the other end of the spectrum, fading unusually high volatility appears to be
more art than science. True, predicting volatility one month forward is slightly easier at
high volatility levels, as volatility is typically not able to sustain high levels for very long.
Fall it will. But as we demonstrated, simple rules to understand when to start fading the
rise in volatility are difficult to come by. Furthermore, in high-volatility regimes, every
minute counts. Being just one day early to fade the volatility spike (or, at times, just
one minute early) can incur major losses. This means position size needs to be adjusted
under the assumption that high volatility lasts longer. It is therefore difficult to catch the
good entry points offered by volatility spikes in any size, as risk management dictates
small sizing.
4.13
SUMMARY
This chapter demonstrates that EMFX generally behaves very similarly to G10 FX
(excluding the JPY, the CHF, and, to a lesser extent, EUR, which are truly different).

How to Trade EMFX
89
FIGURE 4.24
Low Volatility is Good for You.
Note: Strategy returns with entry upon entering the top and bottom fifth
percentile of implied volatility calculated over the last two years, respectively, with
a six-week holding period. We assume zero slippage and transaction costs.
Source: Bloomberg, authors’ calculations.
Having said that, EMFX tends to be much less responsive to interest rate differentials
than their G10 counterparts, which is important to keep in mind when trading EMFX.
Sadly for FX traders, the carry strategy, which has been the go-to strategy for EM
investors for many years, has deteriorated over the last decade. But the chapter
demonstrates that carry still works reasonably well when expressed against the JPY
and/or when implemented with volatility adjustments. Another way to improve carry
strategies in EMFX is to cut positions when implied volatilities for global macro asset
classes are moving higher.
Rules based on strong current accounts are overall money losing, even though
improvement in trade balances can complement a pure carry strategy nicely. Valuation
also is not generating easily tradable strategies, though we note that PPP clearly outper-
form REER-based strategies. REER strategies improve, though, once REER is adjusted
for ToT shocks. But by far the best performing strategy is based on EM growth surprises
rather than on valuation, external accounts, or carry.
Technicals are very important, too, and we warn against trading FX with too funda-
mental a view. Short-term momentum works well, especially when volatility-adjusted,
while mean reversion takes over on a longer horizon. Breadth is also generating
profitable signals. Furthermore, seasonals continue to generate alpha. The use of both
positioning and flows, on the other hand, is much more an art than a science. On
balance, we think positioning should be used as a trend indicator rather than as a
contrarian indicator. But large long positions in a falling market lead to selling pressure
that is tradable. Similarly, the true power of flows comes to the fore when they are used
as a tool in combination with positive or negative shocks that upend consensus.