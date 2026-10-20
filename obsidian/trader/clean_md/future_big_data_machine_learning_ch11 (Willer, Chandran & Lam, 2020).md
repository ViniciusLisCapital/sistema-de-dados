CHAPTER11
The (Near) Future: Big Data, Machine
Learning, and What if There Are No
Emerging Markets Left
The investment industry is currently in the middle of a gold rush. Big data, machine
learning (ML) and artificial intelligence (AI) are the topics du jour, and fund manage-
ment companies expect salvation from the onslaught of passive investment by investing
in big data and ML. Of course, even though the two topics are often used in the same
sales pitch, the two concepts are very different. Big data is almost certainly real, but not
revolutionary. ML may be revolutionary, but the pitfalls are legendary. Here we discuss
the application of these concepts to EM fixed-income investing and where we see the
field developing.
Another topic we address is whether one day, all EM will be developed, leading to
an extinction event for EM.
11.1
BIG DATA IS COMING TO FIXED INCOME
In our view, big data is largely an arms race where only the first mover earns rents for
some time before those rents get competed away. For late movers, all that happens is
that they incur additional costs to implement the innovation that the leaders already
implemented. And by then, the additional alpha is gone. Of course, not implement-
ing big data solutions may mean deteriorating performance, and our characterization
certainly does not mean that organizations can afford to not implement big data solu-
tions. They clearly have to do it, and doing it earlier is better than doing it later, to
at least participate in the alpha generation that is available to the early movers. But in
steady state, big data is unlikely to be the salvation many seek, especially after taking
into account the considerable costs to buy data and reinvent investment processes. The
longer-lasting benefit may accrue to the providers of the infrastructure for the big data
bonanza, rather than to the investment firms who use those tools. Think selling shovels
rather than digging for gold.
223
Trading Fixed Income and FX in Emerging Markets: A Practitioner's Guide, First Edition.
Dirk Willer, Ram Bala Chandran and Kenneth Lam.
© John Wiley & Sons, Inc. Published by John Wiley & Sons, Inc.

224
TRADING FIXED INCOME AND FX IN EMERGING MARKETS: A PRACTITIONER’S GUIDE
Given this backdrop, investment professionals in fixed income have been lucky.
Or, to be more precise, organizations that typically do not have it in their DNA to be
first movers have been lucky. The reason is that big data has so far been much more
impactful for the equity business and much less so for fixed income. After all, at this
stage it is much easier to crawl the web to forecast the earnings for a company with a
large digital footprint than it is to forecast the NFP number with web crawlers. One
reason is that for many firms, everything they do is online – and online is easier to dig-
itally measure than the offline part of the economy. Furthermore, for equities, earnings
are presumably doing a relatively good job of describing the underlying fundamentals
(though in the world of non-GAAP (generally accepted accounting principles) earnings
this is not quite as clear as it should be). Whether most government statistics are a fair
characterization of the underlying fundamentals is much less clear. The NFP number,
for example, gets heavily adjusted. Not just seasonality adjustments, but also the infa-
mous birth-death adjustment, can lead to very large swings in the published number
that would be impossible to pick up by, for example, running a large survey of firms
in order to estimate the likely NFP number. And even if someone designed a superior
survey to the NFP, it would not matter: the market has been trained to trade the NFP
number, not an arguably superior private sector estimate – which is currently already
provided by ADP, the largest payroll processor in the US. In our view, all these argu-
ments help to explain why big data has not yet been as impactful in fixed income as
it has been in equities. Having said that, big data has arrived in fixed income markets,
too, and will likely keep gaining mind and wallet share relatively fast. One accelerator
could be that government statistics itself will rely more on big data over time to improve
accuracy. It therefore behooves fixed income investors to get ready!
Whether big data is coming earlier for EM fixed income or DM fixed income is less
clear. Some EM are woefully behind in online and sensor penetration, which makes
the generation of big data more difficult. But some EM leapfrog the classic offline
infrastructure and go straight to an online setup. And some countries have natural
advantages in terms of the generation of big data. China not only has 1.4 billion
people; it also has far fewer constraints in terms of privacy laws, which makes it much
easier to harness big data. At the same time, given the fact that Chinese government
data is notoriously unreliable, even more so than is the case in the US, there is a higher
likelihood that the market reacts to privately generated economic statistics – which
is not necessarily true for the US. As such, traditional EM fixed-income managers are
only half lucky. Yes, they have been more shielded than equity fund managers; but big
data usage is accelerating in EM fixed income, and maybe even faster than in DM fixed
income, at least for some countries.
So where should investors start? To our mind, there are two important investments
that managers must make. First, investment managers have to acquire the data. The
data acquisition can happen in house, for example, by creating a unit that engages in
web scraping. Alternatively, the data can be bought from outside vendors, either in
a form that has already been processed or in its original form. Unless the data has
been already processed by the vendor, the next step for investment managers is then to
process the data. The goal of this processing is to move from unstructured and/or big
data to “small” data that can be fed into the existing models. Once that step has been
accomplished, it is straightforward to analyse whether model performance improves

The (Near) Future: Big Data, Machine Learning, and What if There Are No Emerging Markets Left
225
thanks to the new data. Traditional investors who rely less on quantitative models will
find it harder to ascertain whether there is value in the new data source. In determining
whether to build or buy, there is an important trade-off. Building will almost certainly
result in higher costs. On the other hand, if alpha is found through an in-house analysis,
it will be a more significant and longer-lasting source of alpha, as the data will not be
replicated as easily by competing investment managers.
One problem with this approach can be that new data sources may not necessarily
have a long back history. That means it will take some time until a sufficiently long data
series has been acquired to be able to trust the backtests when feeding the new data into
the models. This is a very important problem, especially for pure quants who aim to add
big-data-generated indicators to their models. In this sense, more fundamentally minded
investors may actually have an edge, because they can be more open to implementing
models even with data series that are too short for significant backtests as long as the
new indicator is in line with solid fundamental principles.
So what indicators should EM investors focus on? We think the focus to acquire
and process big data should obviously be where the money is. For EM fixed income,
we think the key is to improve CPI estimates. The reason is that local rates are the
EM asset class that is mostly driven by local factors, while FX and credit are much
more globally driven. As such, the focus has to be on local rates when investigating
which local data to focus on. With most central banks targeting (headline) inflation,
the obvious number to spend resources on predicting is inflation. Luckily, forecasting
inflation numbers with big data is also more promising than using big data for labour
market or activity data, for example, because as more retailing activity moves online,
web scraping is becoming a better way to understand price behaviours. Of course, the
trick is to try to forecast the government inflation print, rather than the true behaviour
of inflation. This requires some institutional knowledge about how statistical agencies
process the data in the various countries. At Citi, we had some success improving CPI
forecasts for Mexico with web-scraped data.1
Outside of the CPI space, the most important indicator that would be extremely use-
ful is alternative data regarding Chinese activity. The reason is, of course, that Chinese
growth has very significant implications for global macro and therefore also impacts
the more globally driven EM asset classes, i.e. EMFX and credit, not just Chinese rates.
Given how much the Chinese government seems to smooth at least the GDP statistics,
we think that in the case of China, it is more relevant to try to model “the truth” rather
than try to forecast the relevant government statistics. To the extent that we are mostly
interested in the spillover from Chinese growth to other EM, a focus on trade will be
helpful. Promising approaches relate to tracking data of cargo ships using satellite data,
for example. Finally, we also note that data to measure sentiment based on polls can
also be helpful. While such polls are clearly small data rather than big data, the fact that
polls have become more efficient to administer through technology makes them part of
the new data landscape.
For investment managers who plan to outsource data acquisition, there is a mush-
rooming industry catering to big data and its applications. For a list of providers,
1See also Willer et al. (2019d).

226
TRADING FIXED INCOME AND FX IN EMERGING MARKETS: A PRACTITIONER’S GUIDE
TABLE 11.1
What Investors Want in the Big Data World.
Category
Interest level
Consumer transactions
12%
Geolocation
12%
Business insights
11%
Pricing
11%
Reviews and ratings
7%
Web-crawled data
7%
Data aggregators
6%
App usage and web traffic
6%
Consumer insights
6%
Public sector
4%
Online search
4%
Store locations
3%
Social media
3%
Sentiment
3%
Employment
3%
Advertising
3%
Trade
1%
Open data
1%
Satellite and weather
1%
B2B datasets
1%
Source: Citi, Eagle Alpha.
see Montagu et al. (2017). In this piece, the authors also highlight an interesting chart
from Eagle Alpha, an aggregator of AI and big data services, which highlights the level of
customer interest. We replicate the information in Table 11.1. The highest interest was
in customer transactions and geolocation, while the lowest was in satellite/weather as
well as B2B datasets. The table illustrates that equity investors are likely heavier users
of big data than fixed income clients, as the top categories are more geared toward
equity investing. But pricing data also scores highly, and that is, as we have outlined,
very relevant for fixed-income investing. Interestingly, social media and sentiment are
not in the top group, even though there must be some promise in measuring and trading
sentiment. Employment is also not overly popular: from a fixed income point of view,
it is hard to measure on a national level; and from a corporate point of view, it is not
as good an indicator for revenues or profits as pricing. Satellite data also does not score
highly. We feel that satellite data must be important in getting the all-important trade
flows to and from China right. While processing satellite data is very complex, we see
big room for improvement here, especially for fixed income.
While the new data sources that are likely to develop are very exciting, exploring
and using such data is unlikely to be revolutionary. All that will happen is that combing
through big data sources will create new small data sources, which will then be fed into
trading models. Early movers will benefit from such new small data sources until they
are broadly adopted, after which the alpha will disappear. But as mentioned earlier, if

The (Near) Future: Big Data, Machine Learning, and What if There Are No Emerging Markets Left
227
anything this means investment managers should aim to be early movers, as sitting it
out will not be feasible.
11.2
MACHINE LEARNING: SUPERVISION IS NEEDED FOR
SUPERVISED LEARNING
ML is the other concept that the investment management industry has to incorporate in
its business models. Of course, ML as a technique is really not that different from the
old regression models. The main difference is that a lot more regressions can be fit very
efficiently, including allowing for quadratic and higher moments. This clearly raises
the potential for overfitting, which brings with it high risks of a sharp deterioration
of performance out of sample. This suggests to us that the best use cases for ML are
when researchers have truly big data for the machines to learn from, in order to avoid
overfitting. This is very rare in financial markets unless investors care about intraday
data. On our time horizon, we mostly care about daily data; and for a collection of
daily data to qualify as big data is extremely rare in financial markets. Furthermore,
time series data in general are not well suited for ML, given the auto-correlation in the
data. It is therefore not too surprising that the big successes of ML are in cross-sectional
data (like Netflix video recommendations) rather than in financial markets. And in a
cross-sectional context, sovereign fixed income is not an obvious place to apply ML, as
there are only a few dozen tradable countries. Equities are a better bet, given the number
of equities that are traded is much higher, though even there the data may not qualify
as big data. While the Eureka ML index suggests good performance, it is difficult to
know what is driving this. Our guess is that the most successful strategies use intraday
strategies and are more biased to equities rather than fixed income. The main public
ML fund, AIEQ, uses IBM’s Watson with the goal of outperforming the SPX, but its
performance has so far been relatively weak.
Having said that, one way to use ML is to stick with techniques that allow
researchers to observe which features are the main drivers for the relevant outcomes
(which most deep neural networks do not allow investors to do). If the features
that are observed as significant make fundamental sense to the researchers, they add
those features to their existing models. Without a fundamental justification for why
something should matter, they will not add that factor. This is again an example where
fundamental researchers may have an edge over pure quants who are less interested
in using ML this way. This is similar to the idea that a human with a chess computer
beats a chess computer: human supervision is necessary for supervised ML. And
again, it requires a tremendous amount of data to be available in order for ML to add
much to an existing investment process. Eventually, it is of course plausible that the
fundamental knowledge of the human expert can be added to the ML code, making
human intervention superfluous: i.e. there could be code that tells the machine when
to listen to its results and when not to. This is indeed likely to happen, and the only
question is how quickly we generate sufficient data to make this a feasible proposition.
Having warned about the dangers of overfitting, we are of course as keen to test out
ML models as the next financial market participant. Here we offer some early results of

228
TRADING FIXED INCOME AND FX IN EMERGING MARKETS: A PRACTITIONER’S GUIDE
TABLE 11.2
An AI Horse Race.
Method
IR
Parameters
Mean of trading signals
1.04
ESI for EM, BRL, and EUR, MA signals 4,10, 20 wk
Random forest (RF)
1.24
No. of trees = 10
Logistic regression (LR)
0.54
Default
SVM classifier
0.91
Linear kernel
Gradient boosting (GB)
1.2
Default
K nearest neighbours (KNN)
1.04
Default
Voting classifier
1.26
RF, LR, SVM, GB, and KNN
Source: Bloomberg, authors’ calculations.
a horse race of the various ML techniques. We focus on EMFX as an asset class where
we have the longest history and where humans may benefit the most from the help of
AI, given how difficult it is to generate alpha in FX. To the extent that regime changes
happen more often in EM than in DM, researchers must be even more careful about
interpreting results in EM than in DM. But then again, it is far from obvious that mushy
(human) brains do well with regime switches, either.
We run several popular ML learning/classification algorithms and stick to super-
vised learning models. We then feed the outcomes of various classifiers into a voting clas-
sifier to see if the combination of ML algorithms improves the IR ratio. This approach
is similar to the one described in Banga and Brorsen (2019), where the authors demon-
strate some success in trading JPY using ML approaches on both a daily and monthly
horizon. To be precise, here we aim to predict the weekly performance of the BRL. We
take three economic surprise indices and three technical indicators to generate a trading
signal from each. Trading signals are either long or short. We run various ML classi-
fiers to predict whether the subsequent week’s return is positive or negative. Table 11.2
presents the results.
The table shows that the IRs of RF and GB are higher than a simple equal weighted
allocation to the underlying signals. The voting classifier also performs better than a
simple equal weighted allocation to the various ML signals. We think that for a funda-
mental EM manager, using classifiers to combine fundamental driven views/signals with
technical/quant signals may work well. This approach has the potential to outperform
smart beta strategies. More work is needed; in particular, data logging will be required
for some time before ML is able to run on a combination of fundamental signal and
systematic signals.
11.3
NO DISAPPEARING ACT FOR EMERGING MARKETS
There is also a more pedestrian topic to address when thinking about the future of
emerging market trading. And that is whether one day, all the EM will become DM. In
theory, there should be a way for EM to “graduate” to developed market status. After
all, the US, for example, was at some stage in its history a developing country. As such,

The (Near) Future: Big Data, Machine Learning, and What if There Are No Emerging Markets Left
229
there must be a development path to reach developed market status. More specifically, in
a rates context, for example, there is a path to, over time, lower the positive correlation
between VIX and EM interest rates, which characterizes true EM. With rising wealth
and increasing formalization of the economy, the service sector usually expands, both as
a percentage of a country’s GDP and as a fraction of the consumption basket for which
inflation is calculated. This leads to lower FX inflation pass-through over time, which
eventually should also impact the psychology of linking inflation to the exchange rate.
The reduction of debt denominated in foreign currencies is also a typical development as
EM increase the size of their local financial systems over time, creating a natural demand
for local currency-denominated assets. Therefore, we would expect local currency bonds
in EM to trade less with the exchange rate (which is the transmission mechanism from
risk aversion to rates) and behave more like developed market rates.
Some of this has already happened. In the 1997–1998 Asian financial crisis, not
a single country was able to cut interest rates before FX stabilized, despite very deep
recessions. This is because inflation shot up due to large currency devaluations (which
were exaggerated by several countries coming off FX pegs). Central banks were forced
to stand idly by or even hike rates into a recession. A decade later, during the 2008
global financial crisis, most EM were able to cut interest rates before the worst was
over in terms of FX depreciation, as can be seen in Figure 11.1. The key reason was
that pass-through from FX to inflation seemed to have come down for many EM since
the late 1990s. Consequently, investment managers made large profits in the aftermath
of the 2008 crisis by betting on lower emerging market rates. Ex post, that seems like
a very obvious trade. However, it is worthwhile to remember that at the time, it took
FIGURE 11.1
EM Rates Decouple Earlier from FX Than in the 1990s.
Source: Bloomberg.

230
TRADING FIXED INCOME AND FX IN EMERGING MARKETS: A PRACTITIONER’S GUIDE
TABLE 11.3
Commodity Prices Were Much More
Deflationary in 2008 Than in 1998–1999.
Energy prices (Bloomberg Energy Index)
1997–1998
2008–2009
MYR
−20%
−73%
KRW
34%
−64%
MYR
3%
−70%
PHP
−4%
−71%
SGD
−11%
−70%
TWD
−6%
−70%
THB
20%
−71%
IDR
193%
−65%
Food prices (Bloomberg AG index)
1997–1998
2008–2009
MYR
1%
−43%
KRW
70%
−24%
MYR
31%
−36%
PHP
22%
−38%
SGD
13%
−36%
TWD
19%
−36%
THB
52%
−39%
IDR
272%
−27%
Source: Bloomberg, EIA, FAO.
some bravery to bet on the unknown, given that EM central banks had not been able
to implement monetary stimulus early in the previous crisis.
From the point of view of policy makers, the 2008–2009 episode is a heartening
outcome, as it shows that EM have come a long way since the 1990s and were able to
use a G3-like policy mix to fight potential recessions. But there are some caveats. First,
2008–2009 was an environment of sharply falling US rates, which was not the case
in the late 1990s. This must have been a positive force for EM rates. But, more impor-
tantly, there was one major difference between the 1997–1998 crisis and the 2008–2009
crisis: in the more recent crisis, commodity prices fell much more significantly than a
decade earlier, as per Table 11.3. Commodity prices fell so drastically in 2008–2009
that they were lower for EM even after taking currency depreciation into account. This
might have led to an exaggerated impression of a weaker pass-through effect of FX to
emerging market inflation, as the impacts of FX and commodities on inflation are hard
to distinguish from one an other, given how highly correlated commodity and FX price
moves are.
Furthermore, it has to be pointed out that moving toward DM status is not a one
way street for EM. Accidents happen on a country level. For example, elections can
have consequences and can throw countries back on their development trajectory. Just
because this has rarely happened in the last 10 years does not mean it won’t happen

The (Near) Future: Big Data, Machine Learning, and What if There Are No Emerging Markets Left
231
FIGURE 11.2
Progress Toward G10 Status is Not a One-Way Street.
Note: Two-year rolling correlation between Greece 10-year bond yield and VIX.
Source: Bloomberg.
more frequently going forward. The most recent example is Greece, where bonds traded
like an almost risk-free G3 asset until the 2008 crisis. Since then, the correlation between
rates and risk aversion has steadily risen and was strongly positive in late 2018, as illus-
trated in Figure 11.2. Chile also comes to mind, as the protests that began in late 2019
may undermine Chile’s status as the Switzerland of Latin America for years to come.
More generally, whenever the global business cycle turns down and the world goes
into a recession, it usually reverberates to EM and often results in severe setbacks to
some countries’ development plans. Just as the gods punished Sisyphus by having the
boulder he was pushing continually roll back down the hill, global recessions tend to
push EM back to the foot of the mountain. Unlike the case of Sisyphus, the task for
EM is difficult but not hopeless. The key for EM is to “arrive” at the peak before
the global climate turns hostile again. A few countries have made it so far. Many of
those that reached developed market status did so with strong institutional support
from the developed world, for example, as part of the European Union. Overwhelming
institutional support can keep the boulder at the top of the mountain. While we are
very optimistic about the long-run development potential for many EM we also believe
that we will be left with enough true EM to enjoy trading them for some time to come.
11.4
SUMMARY
We finished the book with a discussion of the future of the asset class. Big data will
move more and more from equity markets to fixed income markets, including EM.
The arms race has, of course, already started. We advise focusing on CPI estimates for
various countries and tracking Chinese activity. Early movers will generate alpha for a
time. When it comes to AI, the scarcity of price data for financial instruments that we are

232
TRADING FIXED INCOME AND FX IN EMERGING MARKETS: A PRACTITIONER’S GUIDE
trying to forecast, and the resulting high likelihood of overfitting is an important hurdle.
However, we find promise in random forest and gradient boosting models for trading
EMFX. This area will remain an important part of the research agenda going forward.
We also addressed the question of whether we could run out of EM. We doubt that
this is likely. Even if some countries succeed in achieving developed market status, new
countries will make it from the frontier into the main benchmarks. As such, we look
forward to many more decades of happy EM trading, AI enhanced or with a mushy
brain at the controls. Thanks for reading!