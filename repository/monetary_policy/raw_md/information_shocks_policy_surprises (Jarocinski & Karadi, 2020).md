Working Paper Series 
Deconstructing monetary policy 
surprises:  
the role of information shocks 
Revised June 2018 
 
Marek Jarociński, Peter Karadi 
Disclaimer: This paper should not be reported as representing the views of the European Central Bank 
(ECB). The views expressed are those of the authors and do not necessarily reflect those of the ECB. 
No 2133 / February 2018

Abstract
Central bank announcements simultaneously convey information about monetary policy and
the central bank’s assessment of the economic outlook. This paper disentangles these two
components and studies their eﬀect on the economy using a structural vector autoregression.
It relies on the information inherent in high-frequency comovement of interest rates and stock
prices around policy announcements: a surprise policy tightening raises interest rates and
reduces stock prices, while the complementary positive central bank information shock raises
both. These two shocks have intuitive and very diﬀerent eﬀects on the economy. Ignoring the
central bank information shocks biases the inference on monetary policy non-neutrality. We
make this point formally and oﬀer an interpretation of the central bank information shock
using a New Keynesian macroeconomic model with ﬁnancial frictions.
Keywords: Central Bank Private Information, Monetary Policy Shock, High-Frequency
Identiﬁcation, Structural VAR
JEL codes: E32, E52, E58
ECB Working Paper Series No 2133 / February 2018
1

Non-technical summary
This paper studies the impact of central bank policy decisions and communication on the
economy. A growing literature uses ﬁnancial market responses to central bank announcements to
identify monetary policy shocks. However, central bank announcements simultaneously convey
information both about monetary policy and the central bank’s assessment of the economic
outlook. The paper disentangles monetary policy shocks from a contemporaneous information
shock by analysing the high-frequency co-movement of interest rates and stock prices in a narrow
window around the policy announcement. This co-movement is informative, because a pure
monetary policy tightening unambiguously lowers stock market valuation. The reason is simple:
the present value of future payoﬀs declines because, ﬁrst, the discount rate increases with higher
real interest rates and rising risk premia and, second, the expected payoﬀs decline with the
deteriorating outlook caused by the policy tightening. So we identify a monetary policy shock
through a negative high-frequency co-movement between interest rate and stock price changes.
If, instead, stock markets and interest rates co-move positively, we read it as an indication for
the presence of an accompanying information shock.
We assess the dynamic impact of the monetary policy shocks and the central bank informa-
tion shocks using a Bayesian structural vector autoregression (VAR). In the VAR on US data,
we augment a standard set of monthly variables, such as interest rates, the price level, economic
activity and ﬁnancial indicators, with high-frequency ﬁnancial-market surprise variables. Our
aim is twofold. First, we set out to obtain impulse responses to monetary policy shocks that
are purged from the eﬀects of the information shocks. These purged monetary policy shocks
are directly comparable to shocks to monetary policy rules in standard macroeconomic models.
Second, we set out to analyse the impact of the central bank information shocks on ﬁnancial
markets and the macroeconomy. This sheds light on the presence of any asymmetric information
between the central bank and the public.
We ﬁnd that the direction of the stock market response within half an hour of the policy
announcement is highly informative about the response of the economy in the months to come.
The macroeconomic impact is substantially diﬀerent depending on whether the high-frequency
co-movement of interest rates and stock prices is negative or positive. A monetary policy tight-
ening (negative co-movement shock) leads to a signiﬁcant contraction in output and a tightening
of ﬁnancial conditions. The price-level decline is faster, and the impact on ﬁnancial conditions
is stronger than in a standard high-frequency identiﬁcation that does not purge the eﬀects of
the information shocks. By contrast, the central bank information shock (positive co-movement
shock) leads to persistently higher short-term interest rates, a signiﬁcantly higher price level
and real activity and improving ﬁnancial conditions. The fact that the information shock has a
signiﬁcant impact on many economic variables is notable, because it rejects the ineﬀectiveness
of central bank communication. We argue that the observed responses are consistent with the
central bank revealing private information about current and future demand conditions and
tightening its policy to counteract its impact on the macroeconomy.
ECB Working Paper Series No 2133 / February 2018
2

We assess the predictions of our methodology also in the euro area. We ﬁnd results that
are broadly consistent with our US results. A monetary tightening leads to a downturn and a
declining price level. A central bank information shock leads to an improvement in economic
activity, a somewhat higher price level, better ﬁnancial conditions, and an oﬀsetting monetary
policy tightening, similarly to the US. We also ﬁnd that the importance of central bank infor-
mation shocks relative to pure monetary policy shocks is higher in the euro area than in the
US (they explain around 50 percent of high frequency variation versus 33 percent in the US).
This is in line with the more transparent communication policy of the European Central Bank
relative to the Federal Reserve Board throughout our sample period.
A New Keynesian macroeconomic model can rationalize our results by assigning a role to
both nominal rigidities and to ﬁnancial frictions in the transmission of monetary policy shocks.
These features match the fast price-level decline accompanying nonnegligible real eﬀects, and
the responses of ﬁnancial conditions that we ﬁnd. In the model, central bank information shocks
are consistent with an asset-valuation shock.
The lesson from this work is that central bank communication about the economy has non-
negligible eﬀects on ﬁnancial and macroeconomic variables. Furthermore, for assessing the eﬀect
of a monetary policy announcement on the economy it is important to look at the response of
the stock prices in addition to the response of interest rates.
ECB Working Paper Series No 2133 / February 2018
3

1
Introduction
The extent of monetary policy non-neutrality is a classic question in macroeconomics (Chris-
tiano, Eichenbaum and Evans, 2005).
To measure the causal eﬀect of policy, one needs to
control for the variation in economic fundamentals that the policy endogenously responds to.
Central bank announcements can help overcome this identiﬁcation challenge. They provide an
opportunity to isolate unexpected variation in policy and, hence, can be used to assess the
impact of monetary policy on real activity and prices (Gertler and Karadi, 2015; Nakamura
and Steinsson, 2013). However, these announcements reveal information not just about policy,
but also about the central bank’s assessment of the economic outlook. In this paper, we ask
whether the surprises in these assessments, ‘central bank information shocks,’ have a sizable
macroeconomic impact.
If they do, this provides evidence on the relevance of central bank
communication, and implies that disregarding these shocks can lead to biased measurements of
monetary non-neutrality.
Consider a revealing example. On January 22, 2008 during the early phase of the 2007-2009
US ﬁnancial crisis, the US Federal Open Market Committee (FOMC) surprised the market with
a larger-than-expected, 75 basis point federal funds rate cut. The S&P 500 stock market index,
however, instead of appreciating as standard theory would predict, showed a sizable decline
within 30 minutes of the announcement. Such an event is not unique: around one third of
FOMC announcements since 1990 are accompanied by such a positive co-movement of interest
rate and stock market changes.
The observation is less surprising, if we notice that in the
accompanying statement, the FOMC explained that it “took this action in view of a weakening
of the economic outlook and increasing downside risks to growth.” In our view, this pessimistic
communication depreciated stock valuations independently of the policy easing. In this paper,
we disentangle variation caused by policy changes from that caused by central bank information
and assess their impact on asset prices and the macroeconomy.
We propose to separate monetary policy shocks from contemporaneous information shocks
by analysing the high-frequency co-movement of interest rates and stock prices in a narrow
window around the policy announcement. This co-movement is informative, because standard
theory has unambiguous prediction on its direction after a policy change. According to a broad
range of models, a pure monetary policy tightening leads to lower stock market valuation.1 The
reason is simple: the present value of future dividends declines because, ﬁrst, the discount rate
increases and, second, the expected dividends decline with the deteriorating outlook caused by
the policy tightening. So we identify a monetary policy shock through a negative co-movement
between interest rate and stock price changes. If, instead, interest rates and stock prices co-move
positively, we read it as a reﬂection of an accompanying information shock. This way, we use
market prices to learn the content of the signal inherent in central bank announcements, which
would not be otherwise readily available to the econometrician.
1Our focus is on the fundamental value. The contemporaneous impact of the policy tightening of any bubble
component of the stock valuation is indeterminate (see e.g. Gal´ı, 2014).
ECB Working Paper Series No 2133 / February 2018
4

We assess the dynamic impact of the policy shocks and the central bank information shocks
using a Bayesian structural vector autoregression (VAR). In our baseline VAR on US data,
we supplement standard monthly variables – interest rates, the price level, economic activity
and ﬁnancial indicators – with variables reﬂecting high-frequency ﬁnancial-market surprises at
monetary policy announcements. The methodology is closely related to proxy VARs (Stock
and Watson, 2012; Mertens and Ravn, 2013) that use high-frequency interest rate surprises
as external instruments to identify monetary policy shocks (Gertler and Karadi, 2015). Our
contribution is to use sign restrictions on multiple high-frequency surprises and identify multiple
contemporaneous shocks. In particular, we use the 3-month fed funds futures to measure changes
in expectations about short term interest rates and the S&P 500 index to measure changes in
stock valuation within a half-hour window around FOMC announcements. We assume that
within this narrow window only two structural shocks, a monetary policy shock and a central
bank information shock, inﬂuence systematically the ﬁnancial-market surprises. We disentangle
the two shocks based on their high-frequency co-movement, as explained above, and track the
dynamic response of key macroeconomic variables. Our aim is twofold. First, we set out to obtain
impulse responses to monetary policy shocks that are purged from the eﬀects of the information
shock.
These purged shocks are directly comparable to shocks to monetary policy rules in
standard models. Second, we set out to analyse the impact of the central bank information
shocks on ﬁnancial markets and the macroeconomy. This sheds light on the presence and the
nature of any information transfer between the central bank and the public.
Our key empirical ﬁnding is that the direction of the stock market response within half
an hour of the policy announcement is highly informative about the response of the economy
in the months to come.
The eﬀects of an unanticipated interest rate increase accompanied
by a stock price decline are very diﬀerent from the eﬀects of an unanticipated interest rate
increase accompanied by a stock price increase. An interest rate increase accompanied by a
stock price decline leads to a signiﬁcant contraction in output and a tightening of ﬁnancial
conditions (higher corporate bond spreads).
This looks like the eﬀect of a monetary policy
shock in standard models. A key diﬀerence from the standard high-frequency identiﬁcation of
monetary policy shocks that fails to control for the information content of the announcements
is that our purged monetary policy shock induces a more pronounced price-level decline. We
hypothesize that the bias caused by the information eﬀects might account for the presence of
the price puzzle in some relevant subsamples (see e.g. Barakchian and Crowe, 2013).
By contrast, an interest rate increase accompanied by a stock price increase leads to sig-
niﬁcantly higher price level and real activity and an improvement in ﬁnancial conditions. We
call this shock a central bank information shock. It is notable that, although the interest rates
increase unexpectedly, the responses of many other variables are opposite to their responses to
the monetary policy shock. This rules out the ineﬀectiveness of central bank communication. If
the stock prices were not responding to central bank communication, and instead varied after
announcements just due to random noise, the responses to negative and positive co-movement
ECB Working Paper Series No 2133 / February 2018
5

shocks that we identify would not diﬀer systematically. We argue that the observed responses
are consistent with the central bank revealing private information about current and future
demand conditions and tightening its policy to counteract their impact on the macroeconomy.
We apply the same identiﬁcation to the euro area and the ﬁndings are similar, so our points
are not speciﬁc to the US. We ﬁrst build a dataset of euro area high-frequency surprises as-
sociated with the European Central Bank’s (ECB) policy announcements.
We estimate the
high-frequency responses of the European swap rates based on bid and ask quotes. We ﬁnd
that almost half of the ECB policy announcements are accompanied by a positive co-movement
of stock prices and interest rates, compared with one third in the US. This is in line with the
more transparent communication policy of the ECB relative to the Fed throughout our sample
period. Next, we run the same VAR as in the US. In the euro area our identiﬁcation is crucial,
because here the standard high-frequency identiﬁcation leads to a puzzle: ﬁnancial conditions
improve signiﬁcantly after a monetary policy tightening, contradicting standard theory. With
our identiﬁcation the puzzle disappears. A monetary tightening leads to an output contraction,
a decline in the price level and an insigniﬁcant response of ﬁnancial conditions. A central bank
information shock leads to an increase in output, a somewhat higher price level, a signiﬁcant
improvement in ﬁnancial conditions, and an oﬀsetting monetary policy tightening, similarly to
the US.
We oﬀer a structural interpretation of our results through the lens of a New Keynesian
macroeconomic model. The model is a version of Gertler and Karadi (2011), in which mon-
etary policy impacts economic activity through both nominal rigidities and ﬁnancial frictions.
Monetary policy inﬂuences output, because output is partly demand determined as a standard
consequence of sticky prices. Financial frictions, in turn, amplify the impact of the policy shock
through a ﬁnancial accelerator mechanism. We introduce a simple central bank communication
policy into the model. In particular, we assume that the central bank has information advan-
tage about a future shock, and it reveals this private information to the public in a statement.
The communication is exact and credible. We estimate key parameters of the model through
matching the impulse responses of our US VAR to those of the model.
We ﬁnd that purging the monetary policy shock from impact of the central bank information
shock inﬂuences the conclusions on the relative importance of nominal versus ﬁnancial frictions.
If one naively disregarded the impact of central bank information shocks, the excessively sticky
price-level response would imply high nominal stickiness. This, in turn, would generate output
responses suﬃcient to match those observed in the data, so no further ﬁnancial ampliﬁcation
would be necessary. As a result, ﬁnancial frictions would be estimated to be small, and the
model would not be able to match the observed response of corporate bond spreads.
If, instead, monetary policy shocks are purged from the impact of central bank information
shocks, the price-level response is stronger, implying a more moderate level of nominal rigidities.
Financial frictions, in contrast, are estimated to be sizable. This helps the model to match both
the large output response and the observed increase in corporate bond spreads. We conclude
ECB Working Paper Series No 2133 / February 2018
6

that ﬁnancial frictions play a prominent role in the transmission of monetary policy shocks.
We also use the model to learn about the nature of the central bank information shocks. In
particular, we ask which single shock would imply impacts consistent with those observed in
our VAR. We ﬁnd that a ﬁnancial asset-valuation shock is broadly consistent with the observed
responses. Unlike the other shocks in our model, it matches both the increase in price level,
output and stock prices, and the decline in corporate spreads.
Related literature Our paper contributes to the long line of research that assesses the impact
of high-frequency ﬁnancial-market surprises around key monetary policy announcements on asset
prices (Kuttner, 2001; G¨urkaynak, Sack and Swanson, 2005a; Bernanke and Kuttner, 2005) and
the macroeconomy (Campbell, Evans, Fisher and Justiniano, 2012; Gertler and Karadi, 2015;
Nakamura and Steinsson, 2013; Paul, 2017; Corsetti, Duarte and Mann, 2018). Similarly to
classic approaches (Bernanke and Blinder, 1992; Christiano, Eichenbaum and Evans, 1996), this
literature assesses the causal impact of policy by identifying unexpected variation in monetary
policy. However, policy announcements come systematically with central bank communication
about the economic outlook. So long as this communication moves private sector expectations
about the macroeconomy and interest rates, its presence can bias the estimated eﬀects of mon-
etary policy. Our contribution is to use multiple high-frequency variables to separate monetary
policy shocks from concurrent central bank information shocks and track their dynamic impact
on ﬁnancial variables and the macroeconomy.
Our paper is related to the empirical research that assesses the extent of information asym-
metry about the economy between the central bank and the public. Romer and Romer (2000)
presents evidence that the US Federal Reserve staﬀprocesses publicly available information more
eﬀectively than the public when forming forecasts. Furthermore, the public can use FOMC pol-
icy actions to learn about these forecasts. Barakchian and Crowe (2013) and Campbell, Fisher,
Justiniano and Melosi (2016) conﬁrm the latter ﬁnding.2 Our paper tests the existence of private
information revelation indirectly. We identify information shocks that hit the economy simul-
taneously with monetary policy shocks. We ﬁnd that the subsequent behavior of the economy
is consistent with the central bank revealing private information that indeed materializes, on
average.
Our paper complements recent research that aims to quantify the impact of central bank
information revelation on expectations and the macroeconomy. Instead of using private infor-
mation proxies created from analysing the language of announcements (Hansen and McMahon,
2016) or obtained from diﬀerences between the FRB staﬀand private sector forecasts (Camp-
bell, Fisher, Justiniano and Melosi, 2016; Miranda-Agrippino, 2016; Lakdawala and Schaﬀer,
2016b), our approach uses the information-processing power of the markets and identify central
bank information shocks from the high-frequency co-movement of interest rate and stock market
surprises. We track the dynamic impact of expectations and realized macroeconomic variables
2With this, they challenge the contrary ﬁndings of Faust, Swanson and Wright (2004) based on a shorter
sample.
ECB Working Paper Series No 2133 / February 2018
7

as a response to such shocks in a VAR framework. Our paper is most closely related to the
approach used in Andrade and Ferroni (2016), which we discovered recently. Similarly to us,
they use sign restrictions and high frequency data to separately identify information and policy
shocks. Diﬀerently from us, however, they concentrate on forward guidance shocks in the euro
area and they use the co-movement of breakeven inﬂation rates and interest rates to distinguish
between the shocks. Notably, we show that the information revealed by breakeven rates is al-
ready included in our identiﬁcation, in the sense that adding sign restrictions on breakeven rates
does not materially change our results.
Nakamura and Steinsson (2013) and Melosi (2017) show that central bank private information
about economic fundamentals helps their structural models to ﬁt the data. Diﬀerently from
these papers, we consider central bank communication about the economy as an additional tool
with which the central bank can guide expectations potentially independently from its interest
rate setting. Our empirical evidence conﬁrms this, especially after 1994 when the US Federal
Reserve started to accompany its policy announcements with a press statement on its views
about the economic outlook. As a further contrast to Nakamura and Steinsson (2013), we use
a VAR to track the dynamic response of inﬂation, while they use event study regressions on
the contemporaneous responses of market-based inﬂation expectations. Our evidence leads us
to draw somewhat diﬀerent conclusions from them. On the one hand, we also ﬁnd that central
bank information shocks explain a non-negligible fraction of monetary policy surprises. On the
other hand, however, our evidence suggests that moderate nominal stickiness can explain the
dynamic responses to monetary policy shocks, while they ﬁnd high nominal stickiness based on
the contemporaneous response of inﬂation expectations.
The remainder of the paper proceeds as follows. In Section 2 we describe the data on FOMC
announcement surprises. Section 3 presents our econometric approach. Section 4 reports the the
US results, followed by evidence on the euro area in Section 5. Section 6 presents a structural
interpretation of our results. Section 7 concludes.
2
Interest rate and stock price surprises
In this section we describe our data on FOMC announcement surprises and present the stylized
fact that motivates our subsequent analysis: that many positive interest rate surprises are
accompanied by stock price increases and many negative interest rate surprises are accompanied
by stock price declines.
Throughout the paper, we refer to ﬁnancial asset price changes around FOMC monetary
policy announcements as ‘surprises.’ This is because, if we assume that prices reﬂect expecta-
tions, they only change to the extent the announcement surprises the markets. Following much
of the related literature we measure the surprises in a half-hour window starting 10 minutes
before and ending 20 minutes after the announcement (G¨urkaynak, Sack and Swanson, 2005b).
ECB Working Paper Series No 2133 / February 2018
8

2.1
The US dataset
We study asset-price changes around 239 FOMC announcements from 1990 to 2016. Our dataset
is an updated version of the G¨urkaynak, Sack and Swanson (2005b) dataset. Since 1994, the
FOMC issues a regular press release about its policy decisions and its assessment of the state
of the ﬁnancial markets and the economy. The surprises are measured around the time of the
press release, which is in most cases at 14:00 on the day of the meeting. Before 1994, the FOMC
did not explicitly announce its policy decisions. Instead, the markets learned about them from
the open-market operations conducted around 11:15 am the day following the FOMC meeting.
Consequently, this is when the surprises are measured before 1994.
Our baseline measure of the interest rate surprise is the change in the 3-month fed funds
future. These contracts exchange a constant interest for the average federal funds rate over the
course of the third calendar month from the contract. During most of our sample, around 6
weeks elapse between regular policy meetings, so the 3-month future conveniently reﬂects the
shift in the expected federal funds rate following the next policy meeting.
This horizon has
two advantages. First, changes in these futures combine surprises about actual rate-setting and
near-term forward guidance, so they constitute a broad measure of the overall monetary policy
stance. Second, they are insensitive to ‘timing surprises’ (i.e., a short-term advancement or post-
ponement of a widely expected policy decision, occasionally announced during an unscheduled
policy meeting). Such ‘timing surprises’ can be expected to have minor impact on macroeco-
nomic outcomes, but can have a large impact on futures contracts shorter than three months.
Federal funds futures are traded on the Chicago Board of Trade. Our surprises are based on a
tick-by-tick dataset of actual futures trades.
Our baseline measure of the stock price surprise is the change in the S&P500, an index
based on 500 large companies. As mentioned above, we take the change in the index between
10 minutes before and 20 minutes after the announcement. This narrow window makes sure
that the ‘pre-FOMC announcement drift’ documented by Lucca and Moench (2015) has no
discernible impact on our measurement. Lucca and Moench show that, puzzlingly, the S&P500
index tends to increase substantially in the 24 hours prior to scheduled FOMC announcements
(by 49 basis points on average between 1994 and 2011). However, the average return after the
announcement until market close is approximately zero. Furthermore, they also show that the
‘drift’ is uncorrelated with the responses of either the fed funds futures or the S&P500 to the
announcements within the half-hour windows that we study here. We conﬁrm that in our sample
the average 30-minutes S&P500 return is less than 2 basis points with the standard deviation
of 60 basis points. So our sample contains no discernible drift.
2.2
‘Wrong-signed’ responses of stock prices to interest rate surprises
We now document a notable stylized fact about the surprises. Namely, many positive interest
rate surprises are accompanied by positive stock market surprises, and many negative interest
ECB Working Paper Series No 2133 / February 2018
9

rate surprises are accompanied by negative stock market surprises. This can be puzzling at ﬁrst
glance, because, as discussed in the Introduction, textbook economics implies that an interest
rate surprise should move stock prices in the opposite direction.
Figure 1: Scatter plot of interest rate and stock price surprises. The 3-month fed funds futures
and the S&P500 index.
surprise in 3m FF futures
-0.3
-0.2
-0.1
0
0.1
0.2
0.3
surprise in S&P500
-1
0
1
2
3
4
I: 17
II: 65
III: 41
IV: 50
1/22/2008
Note: Black ﬁlled circles highlight the data points where both surprises have the same sign. The number in each quadrant
is the number of data points in the quadrant (not counting the data points for which one of the surprises is zero).
Figure 1 shows the scatter plot of the surprises in the 3-month fed funds futures and in
the S&P500 stock index. Empty circles stand for announcements with a negative co-movement
between interest rates and stock prices (as predicted by textbook economics, quadrants II and
IV), while ﬁlled circles highlight announcements with a counterintuitive positive co-movement
(quadrants I and III). We report the number of data points in each quadrant (66 data points
are uncounted, because they lie exactly on one of the borders).
The ﬁgure shows that the
outcome observed on January 22, 2008 and discussed earlier is not unique, there are more
examples of ‘wrong-signed’ stock market responses to announcements.
Overall, 34% of the
internal data points are in quadrants I and III, with ‘wrong-signed’ stock market responses.
They are not limited to any particular period, but occur throughout our sample (see Section
4.4). The proportion and sizes of ‘wrong-signed’ stock market responses remain similar also for
alternative measures of surprises.3
3In the Appendix we replace the 3-month fed funds futures with the ﬁrst principal component of surprises in
the current month and 3-month fed funds futures and 2-, 3-, and 4- quarters ahead 3-month eurodollar futures.
ECB Working Paper Series No 2133 / February 2018
10

Another observation based on Figure 1 is that even when the stock prices move in the
opposite direction to the interest rates, the strength of these stock price responses varies widely.
There are both announcements triggering large interest rate and small stock price surprises, as
well as announcements triggering large stock price and small interest rate surprises.
There are two possible ways to account for the ‘wrong-signed’ stock market responses to
the FOMC announcements and for the widely varying strength of the stock market responses.
One way is to attribute them to random noise in the stock market (the stock market is indeed
very volatile).
Another way is to attribute them to some shock that occurs systematically
at the time of the central bank policy announcements, but that is diﬀerent from the standard
monetary policy shock. Below we present evidence in favor of the latter explanation. We start by
designing an econometric framework for decomposing surprises into distinct shocks and tracking
their eﬀects on the economy.
3
The econometric approach
In this section we explain how we estimate a joint econometric model of FOMC announcement
surprises and standard macroeconomic and ﬁnancial variables and how we identify structural
shocks in this model. The model enables us to combine two approaches to shock identiﬁcation
familiar from structural VARs: high-frequency identiﬁcation and sign restrictions.
A useful
practical feature of our approach is that it can handle missing data on announcement surprises.
Our estimation is Bayesian. This is ﬁrst, because standard Bayesian inference accounts for
estimation uncertainty in a nonstandard setup like ours, which features partial identiﬁcation
due to sign restrictions, and accommodates missing data. Second, we follow the large Bayesian
VAR literature that uses the priors of Litterman (1979) to prevent overﬁtting of a model with
many free parameters.
3.1
Estimation of a VAR with FOMC announcement surprises
Let yt be a vector of Ny macroeconomic and ﬁnancial variables observed in month t. Let mt be
a vector of surprises in Nm ﬁnancial instruments observed in month t. To construct mt we add
up the intra-day surprises occurring in month t on the days with FOMC announcements. Our
baseline model is a VAR with mt and yt and a restriction that mt does not depend on the lags
of either mt or yt and has zero mean,
 
mt
yt
!
=
P
X
p=1
 
0
0
Bp
Y M
Bp
Y Y
!  
mt−p
yt−p
!
+
 
0
cY
!
+
 
um
t
uy
t
!
,
 
um
t
uy
t
!
∼N(0, Σ),
(1)
where N denotes the normal distribution. As long as the ﬁnancial market surprises are unpre-
dictable, the above zero restrictions are plausible. In the Appendix, we show that our results
We also replace the S&P500 surprise with the ﬁrst principal component of three stock indices.
ECB Working Paper Series No 2133 / February 2018
11

are unaﬀected by relaxing these zero restrictions.
We choose priors that are standard in the Bayesian VAR literature.
Let B collect the
coeﬃcients of the VAR, B = (B1
Y M, B1
Y Y , ..., BP
Y M, BP
Y Y , cY )′. We introduce a Minnesota-type
prior speciﬁed as an independent normal-inverted Wishart prior, p(B, Σ) = p(B)p(Σ), where
p(Σ|S, v) = IW (S, v) ,
(2)
p(vec B|B, Q) = N(vec B, Q),
(3)
IW denotes the Inverted Wishart distribution. We set the prior parameters B, Q, S, v following
Litterman (1979) and the ensuing literature. Namely, in B the coeﬃcient of the ﬁrst own lag
of each variable is 1 and the remaining entries are zero. Q is a diagonal matrix implying that
the standard deviation of lag p of variable j in equation i is λ1σi/σjp−λ3. We use the standard
values of all the hyperparameters. So, we take λ1 = 0.2, λ3 = 1. σi (σj) is the standard error in
the autoregression of order P of variable i (j). S is a diagonal matrix with σ2
i , i = 1, ..., Nm +Ny
on the diagonal. v = N + 2.
We generate draws from the posterior using the Gibbs sampler, at the same time taking
care of the missing values in mt. In the Gibbs sampler we draw in turn from three conditional
posteriors: i) p(Σ|Y, M, B), ii) p(B|Y, M, Σ) and iii) we draw the missing observations in M,
where M is a T × Nm matrix collecting observations on mt for t = 1, ..., T and Y is a T × Ny
matrix collecting observations on yt for t = 1, ..., T. The conditional posterior of Σ in i) is
inverted Wishart, and the conditional posteriors of B and of the missing observations of m in
ii) and iii) are normal. See the Appendix for the (standard) derivations of these conditional
posterior densities.
3.2
Identiﬁcation: combining high-frequency identiﬁcation and sign restric-
tions
This subsection explains how we combine high-frequency identiﬁcation and sign restrictions in
order to identify the structural shocks of interest in our baseline VAR model.
We identify two structural shocks transmitted through the central bank announcements. For
the time being, let us call them a negative co-movement shock and a positive co-movement shock.
We use two assumptions on the announcement surprises to isolate these shocks. Unless indicated
otherwise, we impose no restrictions on any monthly macroeconomic and ﬁnancial variables.
1. (High-frequency identiﬁcation) Announcement surprises mt are aﬀected only by the two
announcement shocks (the negative co-movement shock and the positive co-movement
shock), and not by other shocks.
2. (Sign restrictions) A negative co-movement shock is associated with an interest rate in-
crease and a drop in stock prices. A positive co-movement shock is the complementary
ECB Working Paper Series No 2133 / February 2018
12

shock, i.e. the orthogonal shock that is associated with an increase in both interest rates
and stock prices.
The ﬁrst assumption is justiﬁed, because variables mt are measured in a narrow time window
around monetary policy announcements. Hence, it is unlikely that shocks unrelated to central
bank announcement systematically occur at the same time.
The second assumption separates two central bank announcement shocks. Their orthogo-
nality is a standard requirement of structural shocks. We now consider their interpretation.
Most models suggest that a monetary policy tightening implies a decline in stock prices. First,
the monetary tightening generates a contraction that reduces the expected value of future divi-
dends. Second, the higher interest rates raise the discount rate with which these dividends are
discounted. As a result, the stock price, which in the standard asset pricing theory is the present
discounted value of future dividends, declines. Therefore, the negative co-movement shock is
consistent with news being revealed about monetary policy, so, to a ﬁrst approximation, we will
think about it as a monetary policy shock. By contrast, a positive co-movement must reﬂect
something in the central bank’s announcement that is not news about monetary policy. We will
call the positive co-movement shock a central bank information shock. We will show that the
empirical results support the proposed interpretation. We will also consider some reﬁnements
of this simple identiﬁcation later.
Table 1: Identifying restrictions in the baseline VAR model
shock
variable
Monetary policy
CB information
other
(negative co-movement)
(positive co-movement)
mt, high frequency
interest rate
+
+
0
stock index
–
+
0
yt, low frequency . . .
•
•
•
Note: Restrictions on the contemporaneous responses of variables to shocks. +, –, 0 and • denote the respective
sign restrictions, zero restrictions, and unrestricted responses.
Table 1 summarizes the identifying restrictions.
The restrictions partition each month’s
announcement surprise into a monetary policy shock component and a central bank information
shock component.
The above framework, in which the surprises mt are linear combinations of structural shocks,
is the simplest one that allows us to make our points on the signs and shapes of impulse responses
of yt to diﬀerent shocks present in the FOMC announcements. It is an additional issue that
the surprises mt do not capture all of the exogenous variation in monetary policy and central
bank communication, as some of it is also reﬂected on other occasions, such as speeches by
ECB Working Paper Series No 2133 / February 2018
13

FOMC members. Hence, it would be more precise to call our shocks ‘monetary policy shock in
the FOMC announcements’ and ‘central bank information shock in the FOMC announcements,’
but we do not do it for brevity.4
To compute the posterior draws of the shocks and the associated impulse responses we
proceed as follows.
We note that the ﬁrst assumption (with the resulting zero restrictions)
implies a block-Choleski structure on the shocks, with the ﬁrst two shocks forming the ﬁrst
block. Next, we impose the sign restrictions on the contemporaneous responses to the ﬁrst two
shocks following Rubio-Ramirez, Waggoner and Zha (2010). For each draw of model parameters
from the posterior we ﬁnd a rotation of the ﬁrst two Choleski shocks that satisﬁes the sign
restrictions. The prior on the rotations is uniform in the subspace where the sign restrictions
are satisﬁed.
More in detail, for each draw of Σ from the posterior we compute its lower-
triangular Choleski decomposition, C. Then we postmultiply C by a matrix Q =
 
Q∗
0
0
I
!
,
where Q∗is a 2 × 2 orthogonal matrix obtained from the QR decomposition of a 2 × 2 matrix
with elements drawn from the standard normal distribution. We repeat this until ﬁnding a
Q such that CQ satisﬁes the sign restrictions. Then CQ is a draw of the contemporaneous
impulse responses from the posterior, and the other quantities of interest can be computed in the
standard way. The above procedure, with the QR decomposition of a randomly drawn matrix,
implies a uniform prior on the space of rotations Q∗(Rubio-Ramirez, Waggoner and Zha, 2010).
The point to note here is that our restrictions only provide set identiﬁcation, i.e. conditionally
on each draw of B and Σ there are multiple values of shocks and impulse responses that are
consistent with the restrictions. When computing uncertainty bounds we take all these values
into account weighting them according to the uniform prior on rotations. Having a uniform prior
on rotations is less restrictive than imposing sign restrictions by means of a penalty function
approach as e.g. in Uhlig (2005). Moreover, in the Appendix we also report the robustness to
other priors on rotations following Giacomini and Kitagawa (2015).
4
Empirical results
4.1
Variables in the baseline VAR
Our baseline VAR includes seven variables: two high-frequency surprise variables in mt and ﬁve
low-frequency macroeconomic variables in yt. mt consists of the surprises in the 3-month fed
funds futures and in the S&P 500 stock market index. yt includes a monthly interest rate, a
stock price index, indicators of real activity, the price level, and ﬁnancial conditions.
More in detail, we use the monthly average of the 1-year constant-maturity Treasury yield
4In this paper we do not study questions like: “How much of the variance of yt is due to exogenous monetary
policy shocks or exogenous variation in central bank communication?” Such questions require an appropriate
rescaling of the VAR impulse responses by means of instrumental variables techniques (a VAR with external
instruments, see e.g. Stock and Watson, 2012; Mertens and Ravn, 2013; Gertler and Karadi, 2015; Stock and
Watson, 2017; Paul, 2017).
ECB Working Paper Series No 2133 / February 2018
14

as our low frequency monetary policy indicator. The advantage of using a rate longer than the
targeted federal funds rate is that it incorporates the impact of forward guidance and therefore
remains a valid measure of monetary policy stance also during the period when the federal funds
rate is constrained by the zero lower bound (Gertler and Karadi, 2015). As our stock price
index, we use the monthly average of the S&P 500 in log levels. Our baseline measures of real
activity and the price level are the real GDP and the GDP deﬂator in log levels. We interpolate
real GDP and GDP deﬂator to monthly frequency following Stock and Watson (2010). This
methodology uses a Kalman ﬁlter to distribute the quarterly GDP and GDP deﬂator series
across months using a dataset of monthly variables that are closely related to economic activity
and prices. In the Appendix, we show that most of our results are robust to using industrial
production and the consumer price index. Finally, as an indicator of ﬁnancial conditions we
include the excess bond premium (EBP, Gilchrist and Zakrajsek, 2012; Favara, Gilchrist, Lewis
and Zakrajsek, 2016). This is the average corporate bond spread that is purged from the impact
of default compensation. As the authors show, this variable aggregates high-quality forward-
looking information about the economy. Therefore, it improves the reliability and the forecasting
performance of small-scale VARs (Caldara and Herbst, 2016).
The VAR has 12 lags. The sample is monthly, from July 1979 to December 2016. The two
variables in mt are unavailable before February 1990. Moreover, the S&P500 surprise is missing
in September 2001, when the FOMC press statement took place before the opening of the US
market.
We report the results based on 2000 draws from the Gibbs sampler, obtained after discarding
the ﬁrst 2000 draws and keeping every fourth of the subsequent 8000. We obtain the same results
also when the chain is 10 times longer. For every draw of B and Σ we ﬁnd a random rotation
matrix Q that delivers the sign restrictions. It is easy to show that for the restrictions in Table
1 such a matrix exists for every nonsingular Σ.
4.2
Impulse responses
Figure 2 presents the impulse responses to the monetary policy and central bank information
shocks, respectively, in panel A, in the ﬁrst and the second column. The plots make two points
obvious. First, our sign restriction on the high-frequency co-movement of interest rates and stock
prices separates two very diﬀerent economic shocks. If, contrary to our hypotheses, the stock
market response in the half-hour window around the policy announcement were uninformative
about the eﬀect of the announcement on the economy, the impulse responses of macroeconomic
and ﬁnancial variables yt would have been the same in the two columns. This is clearly not
the case if one looks at, for example, the striking diﬀerences between the responses of prices
and the excess bond premium in the two columns. This is all the more notable given that we
impose no restrictions on the responses of any low frequency variables yt. Second, monetary
policy announcements generate not only monetary policy shocks. The second column clearly
shows that the positive co-movement of interest rates and stock prices around monetary policy
ECB Working Paper Series No 2133 / February 2018
15

announcements, which is inconsistent with monetary policy shocks, has low frequency conse-
quences. For example, a high-frequency increase in stock prices and interest rate foretells a
persistent increase in the future price level. We next discuss the impulse responses in detail.
Figure 2: Impulse responses to one standard deviation shocks, baseline VAR. Median (line),
percentiles 16-84 (darker band), percentiles 5-95 (lighter band).
A. Sign restrictions
B. Standard HFI
Monetary policy
CB information
(negative co-movement)
(positive co-movement)
Monetary policy
(Choleski, 3m ﬀf ﬁrst)
0
10
20
30
0
0.05
  surprise in
3m ff futures
0
10
20
30
0
0.05
0
10
20
30
-0.4
-0.2
0
0.2
0.4
surprise in
S&P500
0
10
20
30
-0.4
-0.2
0
0.2
0.4
0
10
20
30
0
0.1
0.2
1y govt. bond
   yield (%)
0
10
20
30
0
0.1
0.2
0
10
20
30
-2
-1
0
1
S&P500
(100 x log)
0
10
20
30
-2
-1
0
1
0
10
20
30
-0.2
0
0.2
Real GDP
(100 x log)
0
10
20
30
-0.2
0
0.2
0
10
20
30
-0.1
0
0.1
GDP deflator
(100 x log)
0
10
20
30
-0.1
0
0.1
0
10
20
30
-0.05
0
0.05
EBP
(%)
0
10
20
30
-0.05
0
0.05
0
10
20
30
0
0.05
  surprise in
3m ff futures
0
10
20
30
-0.2
-0.1
0
surprise in
S&P500
0
10
20
30
0
0.1
0.2
1y govt. bond
   yield (%)
0
10
20
30
-1.5
-1
-0.5
0
S&P500
(100 x log)
0
10
20
30
-0.2
0
0.2
Real GDP
(100 x log)
0
10
20
30
-0.1
0
0.1
GDP deflator
(100 x log)
0
10
20
30
0
0.02
0.04
EBP
(%)
months
months
months
The ﬁrst column shows the responses to a monetary policy shock. Due to the coeﬃcient
restrictions in our VAR (1), the announcement surprises in mt are iid. They only respond to
ECB Working Paper Series No 2133 / February 2018
16

Table 2: Impact responses of announcement surprises to shocks. Baseline VAR.
A. Sign restrictions
B. Standard HFI
Monetary policy
CB information
Monetary policy
mean
(5pct,95pct)
mean
(5pct,95pct)
mean
(5pct,95pct)
3-m f.f. futures
5
(
3,
6)
3
(
0,
5)
6
(
6,
7)
S&P500
-44
( -54, -23)
28
(
4,
47)
-21
( -27, -15)
Note: Posterior means and posterior percentiles 5 and 95. In basis points.
shocks on impact, and their impulse response function is zero in all other periods. Table 2 reports
their impact responses. By construction, the impact responses satisfy the sign restrictions. A
monetary policy shock is associated with a 3 to 6 basis points increase of the 3-month fed
funds futures and a 23 to 54 basis points drop in the S&P500 index in the 30 minutes window.
The response of low-frequency variables are qualitatively in line with previous results in the
literature. The 1-year government bond yield increases by around 10 basis points and reverts
to zero in about a year. Financial conditions tighten, the stock prices drop by about 1 percent,
and the excess bond premium increases by about 5 basis points. Real GDP and the price level
both decline persistently by about 10 basis points and 8 basis points respectively. The main
quantitative novelty in these responses is the fairly low persistence of the interest rate response
and the vigorous price-level decline. We come back to this result in Section 6 and analyze its
relevance within a structural model.
The second column shows the responses to the central bank information shock. They are new
in the literature. The shock is associated with an up to 5 basis points increase in the 3-month
fed funds futures and a 4 to 47 basis points increase in the S&P500 index in the 30 minutes
window. The 1-year government bond yield increases by about 20 basis points and reverts back
to zero in about two years, much slower than after a monetary policy shock. The shock has a
mild positive impact on the stock prices with wide uncertainty bands at the monthly frequency,5
and it signiﬁcantly reduces the excess bond premium by about 3 basis points. The impact on
output and price-level is very diﬀerent than after a monetary policy shock: here the price-level
increases by about 5 basis points, rather than declining as after a monetary policy shock. The
increase is very persistent and prices revert to the baseline only after around 3 years. Output
increases slightly, rather than declining as after a monetary policy shocks, though this eﬀect
reverses after about a year.6 In our view, these responses are consistent with the scenario in
5As we show in the appendix, the estimated stock market eﬀects are larger and more persistent if we exclude
the pre-1994 sample from the identiﬁcation, when the FOMC did not accompanied its policy decisions with press
statements.
The stock market eﬀects are also signiﬁcantly larger in Europe (see Section 5), where the ECB
followed a more transparent communication throughout our sample period.
6The reversal of the output response can be a side eﬀect of monetary policy tightening aimed at stabilizing
inﬂation volatility. We do not observe this reversal in our estimates on euro area data (see Section 5).
ECB Working Paper Series No 2133 / February 2018
17

which the central bank communicates good news about the economy and tightens monetary
policy, consistently with its reaction function, to partly oﬀset the eﬀect of the news and prevent
overheating of the economy. The persistent increase in the 1-year government bond yield is in
line with such a systematic reaction of the central bank. The policy fails to completely oﬀset
the initial eﬀect of the news, but it is successful in neutralizing it within a few years.
Figure 2 illustrates also how the presence of central bank information shocks biases the stan-
dard high-frequency identiﬁcation (HFI) of monetary policy shocks. The standard identiﬁcation
takes all the surprises in the fed funds futures as proxies for monetary policy shocks (and ignores
the accompanying stock price movements). This is what we reproduce in panel B of Figure 2.
Speciﬁcally, this panel shows the impulse responses to the 3-month fed funds futures surprise,
ordered ﬁrst, in the VAR identiﬁed with the Choleski decomposition. By the properties of the
Choleski decomposition, the identifying restrictions in this case are
cov(mff
t , ϵMP
t
) > 0 and cov(mff
t , ϵi
t) = 0 for all ϵi
t other than ϵMP
t
,
(4)
where mff
t
denotes the fed funds futures surprise and ϵMP
t
the monetary policy shock. Identifying
restrictions (4) are used among others in Gertler and Karadi (2015) and Barakchian and Crowe
(2013).7
The ﬁgure shows that the standard high-frequency identiﬁcation mixes the monetary policy
shocks with central bank information shocks. The responses in Panel B are qualitatively similar
to the ‘pure’ responses in the ﬁrst column of panel A, which are purged from the impact of central
bank information shocks. But there are notable quantitative diﬀerences. First, the response of
the price level is muted, because the central bank information shocks, which have positive price-
level impact, obfuscate the vigorous price-level decline observed after a pure monetary policy
shock.
Second, the impact on the excess bond premium is underestimated.
This is, again,
because the central bank information shocks, which reduce the excess bond premium, attenuate
the estimated increase of this variable after a monetary policy shock. An additional bias in the
standard high-frequency identiﬁcation is that the interest rate responses in panel B are larger
and more persistent. This is because of the presence of the central bank information shocks,
which have higher and more persistent interest rate eﬀect. As the peak impact on output is
similar in both identiﬁcations, this bias leads to underestimating the extent of monetary non-
neutrality. Summing up, the standard high-frequency identiﬁcation produces a picture with
very rigid prices and a smaller role for ﬁnancial frictions. However, once we purge the monetary
policy shock from its contamination with the central bank information shock, we obtain impulse
responses of an economy with less rigid prices but more role for ﬁnancial frictions. We make
these points formally in Section 6.
7The speciﬁc implementations of these restrictions diﬀer across papers.
For example, Gertler and Karadi
(2015) use the external instruments approach, i.e. they do not introduce mff
t
into the VAR and instead use it in
auxiliary regressions outside the VAR. Caldara and Herbst (2016) and Paul (2017) discuss the relation between
the Choleski factorization and the external instruments approach. We veriﬁed that in our application the ﬁndings
are very similar when using both approaches.
ECB Working Paper Series No 2133 / February 2018
18

4.3
‘Poor man’s’ sign restrictions and other robustness checks
We now show that a simpler exercise can lead to similar impulse responses as those obtained
with our sign restrictions. In particular, we use the fed funds futures surprises in the months
when the stock price surprise had the opposite sign to the fed funds futures surprise as the
proxy for monetary policy shocks (the proxy is zero otherwise). We use the fed funds futures
surprises in the remaining months as the proxy for central bank information shocks (again, the
proxy is zero otherwise). The implicit assumption in this exercise is that each month can be
classiﬁed either as hit by a pure monetary policy shock or by a pure central bank information
shock. By contrast, in the sign restrictions approach in each month we observe a combination
of the two shocks with diﬀerent, generally non-zero shares. The identifying assumptions behind
this exercise are stronger than those of our baseline sign restrictions, but it is also easier to
implement. For lack of a better name, we dub this exercise as ‘poor man’s sign restrictions.’
Figure 3 reports the impulse responses to these proxies (we place the proxies ﬁrst and use the
Choleski decomposition to identify the VAR). The impulse responses are strikingly similar to
those obtained with sign restrictions.
The correlation between the posterior mean of the monetary policy shock identiﬁed with
sign restrictions and the shock from the poor man’s procedure is 88%. For the central bank
information shock this correlation is 54%. So the sign restrictions and the ‘poor man’s’ sign
restrictions do not yield the same shocks, but they do yield shocks with very similar impulse
responses.
The impulse responses are also robust when we stop the sample in December 2008 (when
the fed funds rate hit the zero lower bound); when we drop the pre-1994 surprises, which were
not accompanied by announcements; when we replace the interpolated real GDP and GDP
deﬂator with the Industrial Production Index and Consumer Price Index (except that Industrial
Production fails to increase after the central bank information shock); and when we replace the
surprises in the 3-month fed funds rate and S&P500 with factors extracted from several interest
rate and stock market surprises. Finally, we continue to obtain similar lessons when we replace
the uniform prior on rotations with the ‘multiple priors’ approach of Giacomini and Kitagawa
(2015). We show these detailed results in the Appendix.
4.4
The shocks over time
At which occasions were the central bank information shocks particularly large? To answer this
question Figure 4 plots the monetary policy and central bank information shocks over time.
The shocks are scaled in terms of the 3-month fed funds futures surprises, in basis points, and
summarized by their posterior means. The upper panel reports the shocks obtained with the
sign restrictions. The lower panel plots the ‘poor man’s proxies.’
Figure 4 shows that the largest central bank information shock was the one discussed in the
Introduction, which happened on January 22, 2008. Other central bank information shocks are
ECB Working Paper Series No 2133 / February 2018
19

Figure 3: Impulse responses to one standard deviation shocks, baseline VAR with ‘poor man’s’
sign restrictions. Median (line), percentiles 16-84 (darker band), percentiles 5-95 (lighter band).
Monetary policy
CB information
(poor man’s proxy)
(poor man’s proxy)
0
10
20
30
0
0.1
0.2
1y govt. bond
   yield (%)
0
10
20
30
0
0.1
0.2
0
10
20
30
-2
-1
0
1
S&P500
(100 x log)
0
10
20
30
-2
-1
0
1
0
10
20
30
-0.2
-0.1
0
0.1
Real GDP
(100 x log)
0
10
20
30
-0.2
-0.1
0
0.1
0
10
20
30
-0.1
-0.05
0
0.05
GDP deflator
(100 x log)
0
10
20
30
-0.1
-0.05
0
0.05
0
10
20
30
-0.04
-0.02
0
0.02
0.04
0.06
EBP
(%)
0
10
20
30
-0.04
-0.02
0
0.02
0.04
0.06
months
months
not particularly clustered, but occur all over our sample. One episode worth highlighting is a
sequence of negative information shocks from the end of 2000 until the end of 2002, in the wake
of the burst of the dot-com bubble. Over this period, the FOMC cut the fed funds rate from over
6% to close to 1%, to oﬀset the worsening demand conditions brought about by the negative
stock-market wealth shock and geopolitical risks related to the 2001 September terrorist attack
and the run up to the March 2003 Iraq war. The initial major cuts up until the end of 2001
were in line with the predictions of standard historical interest rate rules (Taylor, 2007) and
the persistence of easy policy later can be explained by the moderate pace and ‘jobless’ nature
of the recovery (Bernanke, 2010), but we still observe many negative surprises in the fed funds
futures. The FOMC statements during this period consistently linked the easy stance of policy to
weak demand conditions and high economic uncertainty with down-side risks.8 The positive co-
8For example, in August 2001, the FOMC explained that it reduced the target rate by 25 basis points in light
of the facts that “Household demand has been sustained, but business proﬁts and capital spending continue to
weaken and growth abroad is slowing, weighing on the U.S. economy,” and announced that “risks are weighted
mainly toward conditions that may generate economic weakness in the foreseeable future.” In March 2002, the
ECB Working Paper Series No 2133 / February 2018
20

Figure 4: Contributions of shocks to the surprises in the 3-month fed funds futures, aggregated to the monthly frequency. Basis points
1990 1991 1992 1993 1994 1995 1996 1997 1998 1999 2000 2001 2002 2003 2004 2005 2006 2007 2008 2009 2010 2011 2012 2013 2014 2015 2016 2017
-35
-30
-25
-20
-15
-10
-5
0
5
10
15
Monetary Policy (sign restrictions)
Central Bank Information (sign restrictions)
1990 1991 1992 1993 1994 1995 1996 1997 1998 1999 2000 2001 2002 2003 2004 2005 2006 2007 2008 2009 2010 2011 2012 2013 2014 2015 2016 2017
-35
-30
-25
-20
-15
-10
-5
0
5
10
15
Monetary Policy (poor man`s proxy)
Central Bank Information (poor man`s proxy)
ECB Working Paper Series No 2133 / February 2018
21

movement of interest rates and stock market changes after the majority of these announcements
suggest that the worse-than-expected outlook of the FOMC led agents to update downwards
their views about the economic prospects.
Another interesting observation is that the central bank information and monetary policy
shocks are roughly proportional to each other in the pre-1994 period. The pre-1994 period is
diﬀerent from the rest of the sample because until February 1994 the FOMC did not issue a press
release (the surprises are measured around the ﬁrst open market operation after a decision). All
that the market participants were observing was the fed funds rate, and based on that they
made inference about the monetary policy shock and about the central bank information shock.
Theoretical models of central bank information predict that in this case the agents perceive the
two shocks as proportional (see Melosi, 2017; Nakamura and Steinsson, 2013). Our estimated
shocks in this period are consistent with this prediction.
4.5
Responses of other variables
Figure 5 reports the responses of low frequency variables that we add, one by one, to the baseline
model. We can see that the two shocks that we identify by sign restrictions have opposite eﬀects
on a number of important variables. When discussing these results we focus on the responses
to central bank information shocks and what we learn about the nature of these shocks.
The central bank information shock generates an increase in both growth and inﬂation
expectations (see the ﬁrst two rows of Figure 5). The expectations respond gradually, with
most of the eﬀect materializing after a few months, as is often found empirically (Coibion and
Gorodnichenko, 2012).9 The real GDP growth and CPI expectations in these plots come from
Consensus Economics. We transform the current-year and next-year average expectations into
constant-horizon 1-year expectations.10 Due to data availability we start the sample in 1990,
but this does not change much the other impulse responses (see the Appendix). The fact that
growth and inﬂation expectations move in the same direction conﬁrms the notion that central
bank information shocks convey information about demand pressures.
The third row shows the response of a longer-term market-based inﬂation compensation
measure: the ﬁve-year breakeven inﬂation rate.11
The central bank information shock leads
to an increase in inﬂation expectations even at this long horizon. The ﬁgures also highlight
FOMC announced that it kept its target rate constant despite of the “signiﬁcant pace” of expansion. It explained
that “the degree of the strengthening in ﬁnal demand over coming quarters, an essential element in sustained
economic expansion, is still uncertain.” In both of these instances, our methodology assigns overwhelming majority
of the interest rate surprise to central bank information shocks.
9Notably, controlling for the central bank information channel eliminates the counterintuitive positive eﬀect of
a monetary policy shock on expected GDP growth on impact, as emphasized by Nakamura and Steinsson (2013).
10Our expectation measure (EXP12m) is a weighted average of the current-year EXPCY and next-year EXPNY
expectations reported by Consensus Economics: EXP12m = 1−(i−1)
12
EXPCY + i−1
12 EXPNY , where the weights are
determined by share of the current and the next calendar years in the following 12 months period (i is the current
calendar month).
11This variable is available since 1999. The two-year breakeven inﬂation rate, available only since 2004, responds
almost identically (not shown) as the 1-year survey-based measure shown in the second row.
ECB Working Paper Series No 2133 / February 2018
22

Figure 5: Impulse responses of other low frequency variables to monetary policy and central bank
information shocks. Median (line), percentiles 16-84 (darker band), percentiles 5-95 (lighter
band).
A. Sign restrictions
B. Standard HFI
Monetary policy
CB information
(negative co-movement)
(positive co-movement)
Monetary policy
(Choleski, 3m ﬀf ﬁrst)
0
10
20
30
Expected GDP
  growth (%)
-0.1
0
0.1
0
10
20
30
-0.1
0
0.1
0
10
20
30
Expected GDP
  growth (%)
-0.1
0
0.1
0
10
20
30
Expected
inflation (%)
-0.1
0
0.1
0
10
20
30
-0.1
0
0.1
0
10
20
30
Expected
inflation (%)
-0.1
0
0.1
0
10
20
30
5y break-even
inflation rate (%)
-0.1
-0.05
0
0.05
0
10
20
30
-0.1
-0.05
0
0.05
0
10
20
30
5y break-even
inflation rate (%)
-0.1
-0.05
0
0.05
0
10
20
30
10y govt. bond
   yield (%)
-0.05
0
0.05
0.1
0
10
20
30
-0.05
0
0.05
0.1
0
10
20
30
10y govt. bond
   yield (%)
-0.05
0
0.05
0.1
0
10
20
30
5y-5y forward
   rate (%)
-0.05
0
0.05
0
10
20
30
-0.05
0
0.05
0
10
20
30
5y-5y forward
   rate (%)
-0.05
0
0.05
months
months
months
that after a monetary policy shock the peak eﬀect on the breakeven rates is not immediate
and is only reached in a couple of months after the impact. The delayed response, therefore, is
a characteristic of market-based inﬂation measures and not only of the survey-based measure
presented before. The delayed response implies that the contemporaneous responses of breakeven
rates across the maturity spectrum do not reﬂect the full dynamics of inﬂation expectations after
a monetary policy impulse. Our results show that even though the contemporaneous response
of the breakeven yield curve would be consistent with high price stickiness as in Nakamura and
Steinsson (2013), the dynamics of inﬂation expectations tracked by our VAR suggests a sizable
peak response of inﬂation expectations. This large peak response of expectations corroborates
the ﬂexible inﬂation response in our baseline VAR, and suggests moderate nominal stickiness.
We address this issue more formally in Section 6.
The last two rows show that the central bank information shock does not raise the term
ECB Working Paper Series No 2133 / February 2018
23

premium. By contrast, the premium temporarily increases after a monetary policy shock (Gertler
and Karadi, 2015). We conclude this from the observation that even though the 10-year bond
yield increases after both shocks, the ﬁve-year forward rate ﬁve years ahead only increases after
the monetary policy shock. Since the eﬀect of the monetary policy shock on the 1-year bond
yield is only temporary, the increase in the forward rate must reﬂect a rise in the term premium.
By contrast, the forward rate does not respond much to the central bank information shock.
4.6
Interest rates hikes accompanied by bad news
This section reﬁnes the identiﬁcation to address a possible critique. Namely, our baseline sign
restriction scheme is prone to misclassify as monetary policy shocks the events where the central
bank announces adverse news about the outlook while hiking the interest rate. It is an empirical
question whether such events occur in our sample, but they are a theoretical possibility. For
example, consider news about an adverse supply shock. The stock market declines as a result
of lower expected ﬁrm proﬁtability, but as the shock is inﬂationary, the central bank might still
choose to increase rates. For another example, consider a negative revision of the potential
output. Growth prospects look worse, so the stock market tanks, but inﬂationary pressures are
stronger than believed before, so the central bank might increase rates anyway. For both these
kinds of information shocks the co-movement between the interest rate surprise and the stock
price surprise is negative, so our baseline VAR classiﬁes them as monetary policy shocks. To
redress this problem, we reﬁne the identiﬁcation scheme by adding an additional high-frequency
variable to vector mt and an additional set of restrictions, as in Table 3.
The variable we add is the change in the 2 years ahead breakeven inﬂation rate on the day
of the FOMC announcement. We construct this variable by taking the diﬀerence between the
2-year constant-maturity yields of nominal and real (inﬂation-protected) Treasuries (G¨urkaynak,
Sack and Wright, 2007, 2010).
Table 3: Identifying restrictions in the VAR with central bank information about supply
Shock
Variable
Monetary
CB information
CB information
other
policy
about demand
about supply
mt, high frequency
interest rate surprise (30m window)
+
+
+
0
stock index surprise (30m window)
–
+
–
0
breakeven inﬂation surprise (daily)
–
+
+
0
yt, low frequency . . .
•
•
•
•
After a monetary policy shock inﬂation is expected to fall and after favorable news about
ECB Working Paper Series No 2133 / February 2018
24

Table 4: Impact responses of high-frequency surprises to shocks. Separating central bank infor-
mation about demand from central bank information about supply.
Monetary policy
CB information
CB information
about demand
about supply
mean
(5pct,95pct)
mean
(5pct,95pct)
mean
(5pct,95pct)
3-m f.f. futures
5
(
2,
6)
2
(
0,
5)
2
(
0,
5)
S&P500
-21
( -42,
-3)
27
(
5,
45)
-34
( -48,
-8)
2-year breakeven inﬂation
-4
( -5,
-1)
2
(
0,
4)
2
(
0,
4)
Note: Posterior means and posterior percentiles 5 and 95. In basis points.
demand inﬂation is expected to rise, so we require inﬂation compensation to do the same, as
Table 3 shows.12 Next, we isolate a new shock associated with an increase in the interest rate,
a fall in the stock prices and an increase in the breakeven inﬂation. It is the response of the
breakeven inﬂation that distinguishes this new shock from the monetary policy shock. We will
refer to this new shock as ‘central bank information about supply.’ Table 4 reports the impact
responses that reﬂect these assumptions. We can see modest changes of breakeven inﬂation on
the day of the FOMC announcements.
Figure 6 reports the responses of low frequency variables to the three shocks we now identify.
Two lessons stand out.
First, the responses to monetary policy and central bank demand
information shocks are robust to adding a new high-frequency observable and a third shock. The
main diﬀerence is that inﬂation responses become somewhat more pronounced and that this time
the low frequency stock market response to central bank information about demand is positive
(though not very signiﬁcant). Second, the new shock we added does not account for much of the
variability of the macroeconomic and ﬁnancial variables, as witnessed by the near-zero impulse
responses. These results suggest that interest rate and stock market surprises, which we use in
our baseline identiﬁcation, are suﬃciently informative to identify monetary policy and central
bank information shocks, and high-frequency surprises in breakeven inﬂation rates (utilized in
Andrade and Ferroni (2016)) add only minimal independent information. Overall, we conclude
that our previous conclusions remain robust also under this more reﬁned identiﬁcation.
12These assumptions are not completely innocuous. Inﬂation compensation is driven both by expected inﬂation
and by inﬂation risk premium. We have shown that the shocks we identify lead to changes in ﬁnancial conditions,
and this can inﬂuence the required inﬂation risk premium independently from the expected inﬂation. If we assume
that inﬂation risk premium moves in the same direction as the excess bond premium, then our assumptions are
conservative: expected inﬂation necessarily declines if inﬂation compensation declines after a monetary policy
shock, and expected inﬂation necessarily increases if inﬂation compensation increases after a news-about-demand
shock.
ECB Working Paper Series No 2133 / February 2018
25

Figure 6: Impulse responses to one standard deviation shocks. Median (line), percentiles 16-84
(darker band), percentiles 5-95 (lighter band). VAR with central bank information about supply.
Monetary policy
CB information
about demand
CB information
about supply
0
20
-0.1
0
0.1
0.2
1y govt. bond
   yield (%)
0
20
-0.1
0
0.1
0.2
0
20
-0.1
0
0.1
0.2
0
20
-2
-1
0
1
S&P500
(100 x log)
0
20
-2
-1
0
1
0
20
-2
-1
0
1
0
20
-0.2
0
0.2
Real GDP
(100 x log)
0
20
-0.2
0
0.2
0
20
-0.2
0
0.2
0
20
-0.1
0
0.1
GDP deflator
(100 x log)
0
20
-0.1
0
0.1
0
20
-0.1
0
0.1
0
20
-0.05
0
0.05
EBP
(%)
0
20
-0.05
0
0.05
0
20
-0.05
0
0.05
months
months
months
5
Euro area evidence
In this section, we analyze the robustness of our baseline US results by applying our methodology
to euro area data. This application deserves particular attention, because, as we show below,
standard high-frequency identiﬁcation of monetary policy shocks here leads to results that are
inconsistent with theoretical predictions. Our methodology resolves this issue.
5.1
The euro area dataset
We have constructed a novel dataset of euro area high-frequency ﬁnancial-market surprises along
similar lines as the G¨urkaynak, Sack and Swanson (2005b) data for the US. This dataset contains
284 ECB policy announcements from 1999 to 2016.
Most of these announcements happen
after the ECB Governing Council monetary policy meeting and consist of a press statement
at 13:45 followed by an hour-long press conference at 14:30. Analogously to the US, we use
30-minute windows around press statements and 90-minute windows around press conferences,
ECB Working Paper Series No 2133 / February 2018
26

both starting 10 minutes before and ending 20 minutes after the event. Whenever there is a
press conference after a press statement our surprise measure is the sum of the responses in the
two windows.13
The narrow windows that we use minimize the chances that unrelated regular news an-
nouncements bias our measure, which may be more of an issue in Europe than in the US. For
example, our window around regular press statements by the ECB at 13:45 CET excludes mon-
etary policy announcements of the Bank of England released at 12:00 CET the same day in a
sizable part of our sample.14
Figure 7: Scatter plot of the surprises in the 3-month Eonia swaps and in the EuroStoxx50 index
surprise in 3m Eonia swaps
-0.3
-0.2
-0.1
0
0.1
0.2
0.3
surprise in Euro Stoxx 50
-3
-2
-1
0
1
2
I: 57
II: 64
III: 69
IV: 83
Note: Filled circles highlight the data points where both surprises have the same sign. The number in each quadrant is the
number of data points in the quadrant.
In the euro area dataset, we record surprises in the Eonia interest rate swaps with maturities
1 month up to 2 years, and the Euro Stoxx 50, a market capitalization-weighted stock-market
index including 50 blue-chip companies from 11 Eurozone countries.
The ‘wrong-signed’ responses of stock prices are even more of an issue in the euro area than
in the US. In the following analysis, we focus on the 3-month Eonia swap and on the Euro Stoxx
13The dataset contains 275 announcements and 9 speeches of the ECB president: the ‘whatever it takes’ speech
in London on July 26, 2012, as well as 8 speeches announcing various aspects of the ECB’s nonstandard monetary
policies. We report the results without the speeches, but they are similar when we include them.
14US initial jobless claims data releases systematically coincide with the start of the press conferences. We check
whether these releases contaminate our interest rate surprise measure by regressing it on the surprise component
in the data releases (relative to Bloomberg consensus).
The regression explains less than 0.1 percent of the
variability of the surprise. We conclude that we can ignore the impact of the US data release.
ECB Working Paper Series No 2133 / February 2018
27

50. Figure 7 shows the scatter plot of the surprises. This time 46% of the data points are in
quadrants I and III with ‘wrong-signed’ reactions of stock prices to interest rate surprises, even
more than in the US.15 This is in line with the more transparent communication policy of the
ECB. For example, the ECB organizes press conferences since 1999, while the Fed introduced
them only in 2011. Furthermore, the ECB publishes staﬀforecasts promptly after they are
produced, while the Fed does this with a 5 year delay.
5.2
Euro area impulse responses
Our main lesson extends to euro area data: The immediate stock market response to a mone-
tary policy announcement is informative about the announcement’s longer-run economic conse-
quences. In addition, we obtain a number of new ﬁndings.
The VAR we estimate for the euro area is similar to the US VAR. In the euro area VAR
we use the German 1-year government bond yield to capture the safest one-year interest rate.
Furthermore, we use the BBB bond spread to capture ﬁnancial conditions, as no excess bond
premium measure is available for the euro area. The other variables are analogous: we use the
blue-chip STOXX50 index and an interpolated real GDP and GDP deﬂator series. The sample
is from January 1998 to December 2016.
Figure 8 presents the impulse responses for three
identiﬁcations: a standard high-frequency identiﬁcation, sign restrictions and poor man’s sign
restrictions.
In the euro area the standard high-frequency identiﬁcation of monetary policy shocks (Panel
A) yields responses that are inconsistent with predictions of standard theory. In particular, ﬁrst,
stock prices increase, and second, corporate bond spreads fall in response to this shock. Hence,
in the euro area it is obvious that one needs to decompose the monetary policy surprises further,
as we do in this paper.
The baseline sign restrictions deliver a more plausible monetary policy shock, except for one
issue: the response of the 1-year bond yield is insigniﬁcant. Therefore, we add one more sign
restriction to the identiﬁcation: we postulate that the 1-year bond yield increases on impact by
at least 1 basis point. The resulting impulse responses are in Panel B of Figure 8. Two diﬀerences
from the US stand out. First, the stock market response to the central bank information shock
is large and positive, while it was insigniﬁcant in the US. Second, the response of output to
the central bank information shock is stronger, and the response of prices is weaker than in
the US. Many of the responses are not signiﬁcant, but overall, like in the US, they leave no
doubt that the two shocks are very diﬀerent. A positive monetary policy shock is a conventional
policy tightening. A positive central bank information shock looks like positive news about the
economy to which the central bank responds to mitigate its impact on prices.
The poor man’s sign restriction identiﬁcation is implemented analogously as in the US and
again delivers similar impulse responses as the sign restrictions. The main diﬀerence is that
15Recall that in the US 34% of the datapoints with non-zero surprises were in quadrants I and III. This
proportion is 32% in the US sample starting in 1999, like in the euro area.
ECB Working Paper Series No 2133 / February 2018
28

this time the impact increase in the 1-year government bond yield is signiﬁcant and of similar
magnitude for both shocks.
5.3
Euro area shocks over time
Figure 9 plots the euro area shocks over time. As in the US, the central bank information shocks
occur throughout the sample. We comment on four major events. One of the largest central
bank information shocks took place in August 2011 during the European sovereign debt crisis.
On August 4, the Governing Council of the ECB decided to keep its policy rates unchanged after
increasing them twice in April and July the same year. This came as an easing surprise to the
markets that anticipated a further policy tightening. Despite the easing surprise, the Stoxx50
blue chip stock market index dropped signiﬁcantly, in line with the message of the accompanying
statement, which emphasized that uncertainty, especially on ﬁnancial markets, is “particularly
high.” In July 2012, the Governing Council reduced the policy rates by 25 basis points and
explained that “some of the previously identiﬁed downside risks to the euro area growth outlook
have materialised.” The stock market depreciated by more than 2 percent. Another notable
example came in September 2001 after the terrorist attack on the US. The net eﬀect of the
three press statements issued over this month was a large decline in both the interest rates
and the stock index. On September 13, the Governing Council kept its policy rate unchanged,
but announced that “while the expectation is that normal market conditions will prevail in the
period ahead, the Eurosystem will continue to monitor developments in ﬁnancial markets and
take action if necessary.” On September 17, in a coordinated move with other major central
banks, it cut its policy rate and announced that “recent events in the US are likely to weigh
adversely on conﬁdence in the euro area, reducing the short-term outlook for domestic growth.”
In its last scheduled policy meeting in the month it kept its rate unchanged. There is also a
notable negative central bank information shock in October 1999, when the ECB announced an
increase in the size of its longer term reﬁnancing operations “to contribute to a smooth transition
to the year 2000” in light of the then widespread concerns about the ‘Millenium bug.’ The four
events are picked up both by the sign restrictions and their ‘poor man’s’ version.
6
A structural interpretation
In this section, we look at our empirical results through the lens of a New Keynesian macroeco-
nomic model. The model closely follows Gertler and Karadi (2011), which is a workhorse New
Keynesian framework with balance sheet constrained ﬁnancial intermediaries. The framework
is well suited to analyse the quantitative impact of monetary policy shocks, which are modelled
as temporary deviations from a systematic interest rate rule. To obtain an analogue of central
bank information shocks, we introduce central bank communication policy to the model. In
particular, we assume that the central bank has private information about a future disturbance
and reveals this information in advance to the public. Even though news shocks are revealed
ECB Working Paper Series No 2133 / February 2018
29

Figure 8: Impulse responses to one standard deviation shocks, euro area VAR. Median (line), percentiles 16-84 (darker band), percentiles
5-95 (lighter band). Months on the horizontal axis. *The sign restriction identiﬁcation includes also a restriction that the impact response
of the 1-year bond yield is positive.
A. Standard HFI
B. Sign restrictions
C. Poor man’s sign restrictions
Monetary policy
(Choleski, 3m OIS ﬁrst)
Monetary policy
CB information
(negative co-movement*)
(positive co-movement*)
Monetary policy
CB information
(poor man’s proxy)
(poor man’s proxy)
0
10
20
30
-0.05
0
0.05
1y govt. bond
yield DE (%)
0
10
20
30
-1
0
1
STOXX50
(100 x log)
0
10
20
30
-0.1
0
0.1
Real GDP
(100 x log)
0
10
20
30
-0.05
0
0.05
GDP deflator
(100 x log)
0
10
20
30
-0.4
-0.2
0
0.2
BBB bond
spread (%)
0
10
20
30
-0.05
0
0.05
0.1
1y govt. bond
yield DE (%)
0
10
20
30
-0.05
0
0.05
0.1
0
10
20
30
-1
0
1
2
STOXX50
(100 x log)
0
10
20
30
-1
0
1
2
0
10
20
30
-0.1
0
0.1
Real GDP
(100 x log)
0
10
20
30
-0.1
0
0.1
0
10
20
30
-0.05
0
0.05
GDP deflator
(100 x log)
0
10
20
30
-0.05
0
0.05
0
10
20
30
-0.4
-0.2
0
0.2
BBB bond
spread (%)
0
10
20
30
-0.4
-0.2
0
0.2
0
10
20
30
-0.1
0
0.1
1y govt. bond
yield DE (%)
0
10
20
30
-0.1
0
0.1
0
10
20
30
-2
0
2
STOXX50
(100 x log)
0
10
20
30
-2
0
2
0
10
20
30
-0.2
0
0.2
Real GDP
(100 x log)
0
10
20
30
-0.2
0
0.2
0
10
20
30
-0.1
0
0.1
GDP deflator
(100 x log)
0
10
20
30
-0.1
0
0.1
0
10
20
30
-0.5
0
0.5
BBB bond
spread (%)
0
10
20
30
-0.5
0
0.5
months
months
months
months
months
ECB Working Paper Series No 2133 / February 2018
30

Figure 9: Contribution of shocks to the surprise in the 3-month Eonia swap. Basis points
1999
2000
2001
2002
2003
2004
2005
2006
2007
2008
2009
2010
2011
2012
2013
2014
2015
2016
2017
-30
-25
-20
-15
-10
-5
0
5
10
15
Monetary Policy (sign restrictions)
Central Bank Information (sign restrictions)
1999
2000
2001
2002
2003
2004
2005
2006
2007
2008
2009
2010
2011
2012
2013
2014
2015
2016
2017
-30
-25
-20
-15
-10
-5
0
5
10
15
Monetary Policy (poor man`s proxy)
Central Bank Information (poor man`s proxy)
ECB Working Paper Series No 2133 / February 2018
31

contemporaneously with monetary policy shocks, they are independent from each other, in line
with our empirical framework.
In the model, monetary policy inﬂuences real allocations because of two key frictions: nom-
inal rigidities and ﬁnancial frictions. We ask two questions. First, how does the relative impor-
tance of the two key frictions change, if the model matches responses to an estimated monetary
policy shock that is purged from the eﬀects of central bank information shocks (our baseline
monetary policy shock) versus when it matches unpurged impulse responses (monetary policy
shock identiﬁed with the standard high-frequency identiﬁcation). Second, which single struc-
tural shock in the model can best approximate the macroeconomic impact of a central bank
information shock.
We structure the description of the model below along the lines of the transmission of mon-
etary and central bank information shocks.
To conserve space, we describe key equilibrium
conditions of the model and we refer the reader to the original paper for their derivations.
The framework has 7 agents.
There are representative households, ﬁnancial intermediaries,
intermediate-good and capital-good producers, retailers, a ﬁscal authority and a central bank.
The representative households consume a basket of diﬀerentiated goods, work and save. Finan-
cial intermediaries collect deposits and lend to intermediate good ﬁrms. Intermediate good ﬁrms
use capital and labor to produce intermediate goods. They borrow from ﬁnancial intermediaries
and from the household to ﬁnance capital acquisitions. Capital-good producers use ﬁnal goods
to generate new capital. Retailers purchase intermediate goods, diﬀerentiate them and sell them
to the households. Fiscal policy ﬁnances its exogenous expenditures with lump sum taxes. The
central bank sets interest rates and conducts a communication policy.
6.1
Central bank
The central bank sets the nominal interest rate (it) following a Taylor rule.
it = κππt + κxxt + εt,
(5)
where πt stands for the inﬂation rate, xt is a measure of economic slack. We proxy the economic
slack with the log deviation of marginal cost of the intermediate good from its steady state. This
proxy is proportional to conventional output gap measures. κπ > 1 and κx > 0 are parameters.
The policy temporarily deviates from its systematic component because of monetary policy
shocks (εt). The shock follows a ﬁrst-order autoregressive process εt = ρMP εt−1 + ϵMP
t
.
Central bank also conducts a communication policy. Since 1994, the US FOMC has accom-
panied its policy announcements with an explanation of its views about the economic outlook.
This communication gave an explicit channel for the central bank to inﬂuence private expecta-
tions, potentially independently from its rate setting decisions. We assume that the central bank
can move markets with communication not because it has any advantage in collecting data, but
because it employs a large number of analysts and researchers giving it an edge in processing
ECB Working Paper Series No 2133 / February 2018
32

economic information. We model the central bank’s information advantage simply by assuming
that it learns in period t about a future shock (ϵt+2) well before it materializes. The information
shock (ϵt+2) is independent of the monetary policy shock (εt).16 We assume that the central
bank shares its knowledge about the future shock with the public. This communication policy
(ψt) is exact and credible.17 The communication policy is our way of introducing central bank
information shocks to the model.
ψt = ϵt+2
(6)
This policy assumes truth-telling, which we consider to be a reasonable ﬁrst approximation to
a systematic communication policy. It is not worse than alternative linear rules. Maintaining
any constant bias in communication (a constant multiplying the future shock) by understating
the size of the disturbance, for example, would be learnt over time. Noisy communication (an
additive i.i.d. error term) would also be undesirable, because this would only reduce the eﬀec-
tiveness of policy. Importantly, communication policy here is an additional tool to interest rate
policy: Central bank inﬂuences agents’ perceptions not only through changing its policy instru-
ments, but also through publishing statements. The statements can credibly convey information
and move expectations, because the central bank has incentives to maintain the reputation of
its communication policy. When reading the statement, the public updates their expectations
about the future shock. The shock then indeed materializes in period t + 2. The advantage of
central bank communication is to inform the public about an upcoming disturbance that they
would only realize later.
At this stage, we do not determine the nature of the shock that the central bank has infor-
mation advantage about. One of our goals in this section is to identify which single shock would
best describe macroeconomic responses to a central bank information shock that we identiﬁed
in the data.
6.2
Nominal rigidities
The real interest rate (rt) is determined by the Fisher equation
it = rt + Etπt+1.
(7)
Monetary policy inﬂuences the real rates temporarily as a result of nominal rigidities. Nominal
wages are ﬂexible, nominal rigidities are the consequence of staggered price setting of retailers.
Their behavior implies a standard New Keynesian Phillips curve with a backward-looking term.
16This does not mean that interest rates do not respond systematically and contemporaneously to central bank
information shocks, as we explain below.
17If the announcements were not exact, the public would need to infer the underlying economic and monetary
policy disturbances from its observations on the interest rate and communication signals.
The public would
then optimally allocate some weight to both disturbances based on the relative variance of the shocks. In this
realistic framework, no pure monetary policy or central bank information shocks would ever materialize, only some
combination of the two. Our empirical method, however, would still identify the two extreme building blocks of
the observed shocks. We leave the analysis of this environment for future research.
ECB Working Paper Series No 2133 / February 2018
33

It is of the form:
πt −γP πt−1 = β(Et {πt+1} −γP πt) + (1 −γ)(1 −βγ)
γ
xt,
(8)
where β is the steady state discount factor of the representative household, γ ∈[0, 1] is the
probability of unchanged prices (the ‘Calvo parameter’) and γP ∈[0, 1] is the share of prices
that are indexed to the previous period inﬂation rate. The relationship has two key parameters
(γ and γP ) that jointly determine the rigidity of prices. The Calvo parameter determines the
sensitivity of inﬂation to the marginal cost (xt). A high parameter translates into low sensitivity
and implies that the price level responds sluggishly to monetary policy disturbances that change
the marginal costs. Indexation inﬂuences how backward looking the relationship is. High γP
implies high persistence in the inﬂation rate.
6.3
Real eﬀects of monetary policy
Real interest rate inﬂuences aggregate demand through its impact on consumption, on invest-
ment and, indirectly, on government expenditures. Consumption in the model is governed by
the representative households’ Euler equation:
Et {Λt,t+1Rt+1} = 1,
(9)
where the Rt = exp(rt) is the gross real interest rate, and Λt,t+1 is the stochastic discount factor.
The stochastic discount factor is given by
Λt,t+1 = βt
ϱt+1
ϱt
,
(10)
where βt is a potentially time-varying discount factor, and ϱt is the marginal utility of the
consumption. The marginal utility of consumption is given by
ϱt = (Ct −hCt−1)−1 −βthEt(Ct+1 −hCt)−1,
(11)
where h ∈[0, 1] is a parameter governing the strength of consumption habits.
A persistent increase in the real rate following a monetary policy shock raises the opportunity
cost of current consumption relative to future consumption. This reduces consumption, and the
impulse response takes an empirically realistic hump-shaped form as a consequence of habits.
Investment is determined by capital good producers. They transform consumption goods
into capital goods subject to an investment adjustment cost function (f) and sell them to
intermediate good ﬁrms for a price Qt.
Qt = 1 + f
 It
It−1

+
It
It−1
f′
 It
It−1

−EtΛt,t+1
It+1
It
2
f′
It+1
It

(12)
ECB Working Paper Series No 2133 / February 2018
34

An increase in real rates reduces the value of capital Qt.
This value equals the present
discounted value of future capital returns. It declines, because ﬁrst, higher real rates cause a
downturn and reduce the marginal product value of capital. Second, higher interest rates increase
the discount rate, which these future dividends are discounted with. Low price of capital reduces
the incentives to invest, and generates a realistic hump-shaped decline in investment, thanks to
the functional form of adjustment costs.
Aggregate capital (Kt+1) evolves according to the
following law of motion: Kt+1 = Ξt+1 [It + (1 −δ)Kt], where Ξt = exp(ξt) is a shock to capital
quality. It follows a ﬁrst order autoregressive process ξt = ρξξt−1 + ϵξt. The shock is a reduced
form way to introduce variation in the ex post return and the price of capital, and thus it can
be interpreted as an asset-valuation shock.
Government expenditure is assumed to be a fraction of aggregate output Gt = exp(gt)Yt,
where gt = ¯g+ρtgt−1+ϵgt is an autoregressive process. A downturn in output, therefore, reduces
government expenditures. Aggregate demand net of investment adjustment costs equals the sum
of consumption, investment and government expenditures.
The aggregate demand is fulﬁlled through the supply of intermediate good producers that
serve the retailers. Intermediate goods producers combine capital and labor in a constant returns
to scale technology
Ymt = AtKα
t L1−α
t
,
(13)
where Ymt is the intermediate good production, At = exp(at) is a measure of aggregate technol-
ogy, which follows an autoregressive process at = ρaat−1 + ϵat, Lt is labor and α is the capital
income share. We denote the price of the intermediate good Pmt. Marginal product value of
capital is Zt = Pmtα Yt
Kt . Equilibrium in the labor market requires Pmt(1 −α)Ymt
Lt = χϱ−1
t Lϕ
t ,
where χ is the relative utility weight of leisure and ϕ is the inverse Frisch elasticity of labor
supply.
6.4
Financial frictions
We now turn to describe how ﬁnancial frictions are introduced into the model. Intermediate-
good ﬁrms issue state-contingent corporate bonds St that they use to ﬁnance purchases of capital
(Kt+1) from capital producers. They supply corporate bonds at the value
QtSt = QtKt+1,
(14)
where Qt is the real value of capital. The corporate bonds pay the marginal product value of
capital (Zt) every period and decay geometrically with a parameter 1 −δ, where δ is capital
depreciation rate. Therefore, their value (Qt) equals to the value of the capital.18 The (gross)
18The corporate bonds can be understood as equity.
Firms operate a constant returns to scale technology
without proﬁts. So the value of the ﬁrm comes only from the value of their capital holdings.
ECB Working Paper Series No 2133 / February 2018
35

corporate bond return is
Rkt = Ξt
Zt + (1 −δ)Qt
Qt−1
.
(15)
The demand for corporate bonds comes both from ﬁnancial intermediaries (or bank(er)s)
and from households.
St = Sbt + Sht.
(16)
Bankers are part of a household with perfect consumption insurance.
They continue as
a banker each period with probability σ ∈[0, 1], and exit and return their net worth to the
household with the complementary probability 1 −σ. The share of bankers is kept constant by
assuming that some workers become bankers every period. New bankers receive startup funds
from the households. The aggregate startup funds amount to ω. Banks collect deposits from
households and pay them the gross real return Rt. They combine deposits with their net worth
and invest them into corporate bonds.
Financial intermediaries face an agency friction. In particular, we assume that they can
abscond with a ﬁxed fraction of the assets under their management.
If they did this, they
would lose the franchise value of their banking licence. To avoid such outcome, households limit
the amount of deposits they place in ﬁnancial intermediaries and eﬀectively set an endogenous
leverage (φt) constraint. The leverage constraint ensures that the bank has enough ‘skin in the
game’ such that it has no incentive to abscond with the assets. The constraint limits the amount
of corporate lending that the ﬁnancial intermediaries can supply (Sbt):
QtSbt = φtNt,
(17)
where Nt is the aggregate net worth of the banking system.
The ﬁnancial intermediaries build net worth from retained earnings and from start-up funds.
Aggregate net worth evolves according to the following law of motion:
Nt = σ [(Rkt −Rt)φt−1 + Rt] Nt−1 + ω.
(18)
The ﬁrst term on the right hand side captures the net worth from the retained earnings of
surviving bankers, while the second term comes from the start-up funds of the new bankers.
Retained earnings are scaled by the survival probability of bankers (σ), because exiting bankers
repay their net worth as dividends. The retained earnings of surviving bankers come from two
terms. Banks earn the gross real return Rt on their net worth and an excess return Rkt −Rt on
their corporate bond holdings. The latter amounts to the product of their net worth and their
leverage φt−1.
How do ﬁnancial frictions amplify the impact of a monetary policy shock on real activity?
As mentioned above, a temporary increase in the nominal rate translates into a higher real
rate rt because of nominal rigidities. Higher real rates reduce consumption through a standard
ECB Working Paper Series No 2133 / February 2018
36

intertemporal substitution mechanism. Furthermore, higher real rates raise the funding costs
of banks, and make them raise the required return on corporate bonds (EtRkt+1).
Higher
discount rate on existing capital reduces its value Qt, which lowers incentives for investment.
This channel is active even without any ﬁnancial frictions (lax bank balance sheet constraints).
Binding leverage constraints of ﬁnancial intermediaries amplify the impact of the shock through
standard ﬁnancial accelerator mechanisms. Lower value of corporate debt reduces the value
of the banking sector assets, and leads to a deterioration in their balance sheet condition.
In particular, the asset price drop leads to an ampliﬁed decline in their net worth, with a
multiplicative factor that is equal to their leverage. The deteriorating balance sheet condition
of the banking sector further increases the cost of credit and worsens credit conditions with a
further negative impact on investment. The deteriorating outlook further reduces asset prices
adding another negative feedback loop.
We assume that households also lend directly to the corporate sector, subject to a portfolio
adjustment cost as in Gertler and Karadi (2013). In particular, we assume that the household
needs to pay κ(Sht −¯Sh)2 if it purchases corporate bonds in excess of ¯Sh, where κ ≥0 is a
portfolio adjustment cost parameter. The household demand for corporate bonds is determined
by
Sht = ¯Sh + 1
κEtΛt,t+1 (Rkt+1 −Rt+1) ,
(19)
where Λt,t+1 is the household’s stochastic discount factor. The demand function posits that
household respond to increases in corporate bond spreads by increasing their corporate bond
holdings. The parameter κ determines the sensitivity of their response. Importantly, as κ →0
the households are ready to increase their holdings without limits for any positive premium. In
doing so, they issue credit to the intermediate good ﬁrms without constraints and fully replace
the constrained banking sector. As κ approaches zero, the predictions of the model approaches
those of a model without ﬁnancial frictions. Therefore, we use this parameter to measure of the
extent of ﬁnancial frictions in our model.
6.5
Pricing additional assets
Our baseline VAR includes a 1-year government bond yield and the excess bond premium. The
latter is a yield spread between corporate and government bonds with an average duration
of around 7 years. In order to obtain analogous long-term yields in our model, we introduce
multiple long-term bonds as perpetuities with geometrically decaying coupons. We calibrate the
rate of decay of their coupons (ςx) to match their duration. The assets are priced through no-
arbitrage conditions, but are not held in positive quantities in equilibrium. Government bonds
are priced by households, who are assumed to trade them without portfolio adjustment costs.
Corporate bonds, by contrast, are traded by the banks, which require excess return.
We denote by qxt the nominal price of a government bond with duration x. It pays ςi
x unit
in each quarter i = 0, 1, 2, . . . . Its steady state (yearly) duration is 1/[4(1 −ςx/R)], where R
ECB Working Paper Series No 2133 / February 2018
37

is the steady state gross real rate (and steady state inﬂation is 0). Its (gross) nominal yield to
maturity is Yxt = 1/qxt + ςx. The no arbitrage condition requires that
Rt+1Πt+1 = 1 + ςxqxt+1
qxt
.
(20)
Analogously, we denote by Qxt the nominal price of a corporate bond with duration x. It
pays ςi
kx units in periods i = 0, 1, 2, . . . . Its steady state duration is 1/[4(1 −ςkx/Rk)], where
Rk is the steady state corporate bond return. Its gross yield to maturity is Ykxt = 1/Qxt + ςkx.
The no arbitrage condition implies that
Rkt+1Πt+1 = 1 + ςkxQxt+1
Qxt
.
(21)
The (gross) excess bond premium in our model is measured as EBPt = Ykxt/Yxt.
6.6
Calibration
We solve the model through ﬁrst-order perturbation around a non-stochastic steady state. We
estimate key parameters of the model through a standard impulse response matching exercise
(Christiano, Eichenbaum and Evans, 2005). In particular, we estimate three parameters: (i) the
Calvo parameter γ, (ii) the inﬂation indexation parameter γP and (iii) the household portfolio
adjustment cost parameter κ together with the size and persistence of the monetary policy
shock (σi, ρi) to match the impulse responses to a monetary policy shock in the model and
in the VAR. The ﬁrst two parameters determine the level of nominal frictions, and the third
parameter inﬂuences the level of ﬁnancial frictions in the model. Other model parameters are
standard and borrowed from Gertler and Karadi (2011) (the appendix includes a table with a
list of parameters). We then assess which shock can best approximate the impulse responses
to a central bank information shock. We compare news about 2 quarters ahead disturbance in
technology (ϵat+2), in discount rate (ϵβt+2), in government expenditures (ϵgt+2), or in capital
quality (ϵξt+2). We estimate the size and persistence of the disturbances that best approximates
our central bank information shock identiﬁed in the VAR.
Our baseline impulse responses include 5 variables: the 1-year government bond yield, the
GDP and the GDP deﬂator, the S&P500 stock market index and the excess bond premium. In
the model, we match these with the deviations of the following 5 variables from their steady
state values: yield to maturity of a 1-year government bond (ˆy1t), the output ˆyt, the price level
ˆpt = Pt
s=1 ˆπs, the net worth of ﬁnancial intermediaries19 (ˆnt) and the excess bond premium
( ˆ
ebpt).
19Arguably, the equity value of ﬁnancial intermediaries (Nt) in the model better reﬂects the equity value of
companies measured by the S&P500 than the value of capital (Qt). The two variables move in tandem in the
model, but the former gets ampliﬁed by the calibrated leverage, similarly to how S&P500 valuations are ampliﬁed
by the average leverage of the ﬁnancial and non-ﬁnancial ﬁrms it incorporates. Our results are robust to using
Qt as a measure of stock market valuations.
ECB Working Paper Series No 2133 / February 2018
38

We transform monthly VAR impulse responses into quarterly impulse responses by taking
simple averages over each quarter. This gives us 12 moments for each observables. We simulate
impulse responses from the model and stack the 5 times 12 diﬀerences of the VAR and model
moments into a vector V . We estimate our model parameters to minimize V ′ΩV scalar, where
Ωis a weighting matrix. Following Christiano, Eichenbaum and Evans (2005), Ωcontains the
diagonal elements of the inverse of the variance-covariance matrix of the moments from the
VAR.
Figure 10: Matched impulse responses to monetary policy and central bank information shocks,
sign restrictions and standard high-frequency identiﬁcation, Model (black line), VAR median
(blue dashed line), percentiles 5-95 (band).
Standard HFI
Sign restrictions
Monetary policy
Monetary policy
CB information
2
4
6
8
10 12
-0.2
0
0.2
0.4
Percent
1-year rate
2
4
6
8
10 12
-2
0
2
Percent
S&P500
2
4
6
8
10 12
-0.2
0
0.2
Percent
GDP
2
4
6
8
10 12
-0.2
0
0.2
Percent
GDP deflator
2
4
6
8
10 12
Quarters
-0.1
0
0.1
Percent
EBP
VAR
Model
2
4
6
8
10 12
-0.2
0
0.2
0.4
Percent
1-year rate
2
4
6
8
10 12
-2
0
2
Percent
S&P500
2
4
6
8
10 12
-0.2
0
0.2
Percent
GDP
2
4
6
8
10 12
-0.2
0
0.2
Percent
GDP deflator
2
4
6
8
10 12
Quarters
-0.1
0
0.1
Percent
EBP
VAR
Model
Model,κ=0
2
4
6
8
10 12
-0.2
0
0.2
0.4
Percent
1-year rate
2
4
6
8
10 12
-2
0
2
Percent
S&P500
2
4
6
8
10 12
-0.2
0
0.2
Percent
GDP
2
4
6
8
10 12
-0.2
0
0.2
Percent
GDP deflator
2
4
6
8
10 12
Quarters
-0.1
0
0.1
Percent
EBP
VAR
Model
ECB Working Paper Series No 2133 / February 2018
39

Table 5: Estimated parameters
Parameters
Label
Standard HFI
Sign restrictions
Calvo parameter
γ
0.94
0.88
Inﬂation indexation
γP
0.91
0.00
Portfolio adjustment cost
κ
0.0025
0.0245
Stdev of monpol shock
σMP
0.001
0.001
Persistence of monpol shock
ρMP
0.67
0.67
Stdev of info shock
σξ
0.0002
Persistence of info shock
ρξ
0.83
Table 5 lists the estimated parameter values. Figure 10 shows the model implied impulse
responses and compares them to the impulse responses from the VAR. We ﬁrst conduct the exer-
cise using the impulse responses to the monetary policy shock from the standard high-frequency
identiﬁcation, which disregards central bank information shocks. The ﬁrst column of Table 5
and Figure 10 show the results. The price level response is unreasonably sticky in this case, and
the model requires extreme price-stickiness and indexation parameters to capture the impact.
These parameters would imply that prices are reset on average every 4 years, way longer than
micro-data evidence would suggest. With such a high nominal stickiness, the interest rate shock
causes an output decline that severely overestimates the responses predicted by the VAR, espe-
cially in the early years. This happens, even though the size and the persistence of the monetary
policy shock underestimates the observed yield responses. Relatedly, the ﬁnancial frictions are
estimated to be tiny: the model predicts close to zero corporate bond spread response, incon-
sistently with the VAR evidence. If it had estimated higher ﬁnancial ampliﬁcation, the model
would have fare even worse in matching the observed output response.
Next, we conduct the same exercise using our baseline identiﬁcation. This monetary policy
shock is purged from the impact of the central bank information shock. The second column of
Table 5 and Figure 10 show the results. The persistence of the monetary policy shock is now
estimated to be signiﬁcantly lower, and it is able to come close to the observed yield response.
The price stickiness is now estimated to be smaller and the model does not need any backward
indexation to match the observed price level response. The Calvo parameter is still high: prices
are estimated to be reset somewhat more frequently than once in every two years, which is still
higher than evidence from microdata evidence, but not unreasonable if one takes into account
that our simple model does not take into account wage stickiness. The more moderate price
stickiness, however, is insuﬃcient to explain the output response, so the model estimates a sizable
ﬁnancial friction parameter; an order of magnitude larger than in the standard high-frequency
identiﬁcation. This way, it also gets closer to match the observed reaction of the excess bond
premium.
The red dotted lines on the ﬁgure show the impulse responses if we switch oﬀﬁnancial fric-
ECB Working Paper Series No 2133 / February 2018
40

tions by setting the portfolio adjustment cost to zero (κ = 0). Notably, the output response
becomes substantially more muted, suggesting that ﬁnancial ampliﬁcation plays a key role in
capturing the extent of real eﬀects of monetary shocks. We conclude that our baseline identiﬁ-
cation would give substantial weight to ﬁnancial frictions, and smaller role to nominal frictions
in explaining the real eﬀects of monetary policy shocks.
In our last exercise, we ask which single news shock in the model would be broadly consistent
with the central bank information shock we identiﬁed in the data (see the last column of Figure
10). We ﬁnd that news about a 2-quarters-ahead capital quality shock is consistent with our
observations. The shock is a positive asset-valuation shock. Higher asset prices raise investment
and improve the balance sheets of ﬁnancial intermediaries. They, in turn, ease credit conditions,
which leads to a decline in corporate bond spreads, in line with our observations. This further
improves demand conditions which leads to additional increases in output and prices. Monetary
policy tightens to partially oﬀset the impact of this ﬁnancial demand shock. The model some-
what underestimates the yield responses, suggesting that monetary policy in practice responds
more forcefully to the information shocks than as predicted by the model. Modifying the Taylor
rule to allow additional response to corporate bond spreads would help the model come closer
to the observed yield responses (not shown).
Other popular news shocks would have trouble matching the impulse responses not just
quantitatively, but also qualitatively. Technology shocks (ϵat+2) would have trouble capturing
the fact that prices and output move in the same direction after the central bank information
shock.
Other popular demand shocks, like a shock to government expenditure (ϵgt+2) and
household preferences (ϵβt+2) would not work in this particular model either. The shocks increase
some aggregate demand components so they raise output and prices as in the data, but they
actually ‘crowd out’ investment in equilibrium. As a result, the value of capital and net worth
declines and corporate spreads increase, inconsistently with the observed patterns.
7
Conclusion
We argued that systematic central bank communication released jointly with policy announce-
ments can bias high-frequency identiﬁcation of monetary policy shocks, but creates an oppor-
tunity to empirically assess the impact of central bank communication on the macroeconomy.
We have separated monetary policy shocks from central bank information shocks in a structural
VAR and tracked the dynamic response of key macroeconomic variables. We have found that
the presence of information shocks can bias the results of the standard high-frequency monetary
policy identiﬁcation. We have also found that a representative central bank information shock
is similar to news about an upcoming demand shock that the central bank partly oﬀsets.
Our results on the quantitative response to monetary policy shocks can be used to improve
the calibration of models used for monetary policy analysis. We take the ﬁrst step and show
that our baseline monetary policy shock gives a prominent role to ﬁnancial frictions in monetary
ECB Working Paper Series No 2133 / February 2018
41

transmission. Our results on the impact of central bank communication about the real economy
gives support to models that assume that the central bank has some advantage in processing
information about the economy over the private sector, especially about (ﬁnancial) demand
conditions.
Our evidence can contribute to formulating realistic models that could be used
to draw normative conclusions about central bank communication. We leave this for future
research.
ECB Working Paper Series No 2133 / February 2018
42

Appendix
Appendix A
Bayesian estimation
This section explains how we estimate the VAR in (1). This VAR has two non-standard features.
First, a subset of variables mt is assumed to be i.i.d. which implies that the corresponding VAR
parameters are restricted to 0. Second, due to data limitations some of the observations on mt
are missing.
It is convenient to introduce some notation: a) write down the VAR in (1) in matrix notation,
b) partition the variance matrix Σ and c) introduce notation for the missing values of mt.
a) The VAR in (1) in matrix notation is

M
Y

= X

0
B

+

Um
Uy
.
(A.1)
where M = (m1, ..., mT )′, Y = (y1, ..., yT )′, X is a matrix that collects the right-hand-side vari-
ables, with a typical row x′
t = (m′
t−1 y′
t−1 ... m′
t−P y′
t−P 1), B =
 B1
Y M, B1
Y Y , ..., BP
Y M, BP
Y Y , cy
′,
Um = (um
1 , ..., um
T )′, and Uy =
 uy
1, ..., uy
T
′.
b) We partion Σ as follows
Σ =
 
ΣMM
ΣMY
ΣY M
ΣY Y
!
.
(A.2)
c) We introduce notation for missing observations on mt. In some periods all of mt or its
subset is unobserved. Let (τ1, ..., τT ∗) denote the time periods in which all or part of mt is
unobservable. Let m∗
t , t ∈(τ1, ..., τT ∗), denote the unobserved mt. Let M∗be the set of the
unobserved m∗
t and let Mo be the set of the observed mt.
The likelihood function of M, Y is
p(Y, M|B, Σ) ∝|Σ|−T/2
exp

−1
2 tr

M
Y

−X

0
B
′ 
M
Y

−X

0
B

Σ−1

.
(A.3)
We introduce an independent normal-inverted Wishart prior, p(B, Σ) = p(B)p(Σ), where
p(Σ|S, v) = IW (S, v) ∝|Σ|−v/2 exp

−1
2 tr SΣ−1

,
(A.4)
p(vec B|B, Q) = N(vec B, Q) ∝exp

−1
2 vec(B −B)′Q−1 vec(B −B)

,
(A.5)
IW denotes the Inverted Wishart distribution and N denotes the normal distribution.
The prior about the unobserved surprises is noninformative,
p(m∗
t ) ∝1 for all t ∈(τ1, ..., τT ∗)
(A.6)
ECB Working Paper Series No 2133 / February 2018
43

and therefore we ignore it further.
The posterior is obtained as the product of the likelihood and the prior,
p(B, Σ, M∗|Y, Mo) ∝p(Y, M|B, Σ)p(B)p(Σ).
(A.7)
We use a Gibbs sampler to compute posterior.
The Gibbs sampler consists of drawing
in turn Σ, B and m∗
t for t = τ1, ..., τT ∗from their conditional posteriors until the sampler
converges.
Convergence means that the obtained sequence of draws approximates a sample
from the posterior (A.7).
A.1
The conditional posteriors
The conditional posteriors are as follows.
• The conditional posterior of Σ:
p(Σ|Y, M, B) = IW
 S, v

(A.8)
where
S =

M
Y

−X

0
B
′ 
M
Y

−X

0
B

+ S,
(A.9)
v = T + v.
(A.10)
• The conditional posterior of B:
p(vec B|Y, M, Σ) = N
 B, Q

(A.11)
where
Q =
 Q−1 + Σ−1
Y Y.1 ⊗X′X
−1 ,
(A.12)
vec B = Q
 Q−1 vec B +
 Σ−1
Y Y.1 ⊗X′
vec
 Y + MΣ−1
MMΣMY

(A.13)
and ΣY Y.1 = ΣY Y −ΣY MΣ−1
MMΣMY . The computation of matrix Q involves an inverse of
a large matrix. To reduce the computational cost, we follow Clark et al. (2016) and draw
coeﬃcients B equation by equation, sequentially.
• The conditional posterior of m∗
t :
p(m∗
t |Mt−1, Y, B, Σ) = N
 ΣMY Σ−1
Y Y ut, ΣMM.1

,
(A.14)
where ΣMM.1 = ΣMM −ΣMY Σ−1
Y Y ΣY M, Mt−1 denotes the matrix (mt−1, ..., m0)′ and
ut = yt −B′xt.
Note that xt contains elements from Mt−1, that’s why we make the
ECB Working Paper Series No 2133 / February 2018
44

conditioning on Mt−1 explicit.
A.2
Derivation of the conditional posteriors
The conditional posterior of Σ is standard.
To obtain the conditional posterior of B decompose the likelihood as follows:
p(Y, M|B, Σ) = p(Y |M, B, Σ)p(M|B, Σ)
(A.15)
where
p(M|B, Σ) = p(M|ΣMM) ∝|ΣMM|−T/2 exp

−1
2 tr M′MΣ−1
MM

(A.16)
and
p(Y |M, B, Σ) ∝|ΣY Y.1|−T/2
exp

−1
2 tr
 Y −XB + MΣ−1
MMΣMY
′  Y −XB + MΣ−1
MMΣMY

Σ−1
Y Y.1

(A.17)
with ΣY Y.1 = ΣY Y −ΣY MΣ−1
MMΣMY . See e.g. Bauwens et al. (1999) Section A.2.3.
We notice that the second term in the likelihood does not involve B, i.e. the only terms in
the posterior that involve B are p(Y |M, B, Σ)p(B). We do the product and collect the terms
involving B in the standard way.
To obtain the conditional posterior of M∗decompose the likelihood as follows:
p(Y, M|B, Σ) = p(M|Y, B, Σ)p(Y |B, Σ)
(A.18)
where
p(Y |B, Σ) = MN (XB, ΣY Y ⊗IT ) ∝|ΣMM|−T/2 exp

−1
2 tr (Y −XB)′ (Y −XB) Σ−1
Y Y

(A.19)
and
p(M|Y, B, Σ) = MN
 (Y −XB)Σ−1
Y Y ΣY M, ΣMM.1 ⊗IT

(A.20)
with ΣMM.1 = ΣMM −ΣMY Σ−1
Y Y ΣY M. MN is the matricvariate normal distribution as deﬁned
in Bauwens et al. (1999) Section A.2.
We notice that the only term in the posterior that involves M is p(M|Y, B, Σ). Moreover,
we notice that a term involving m∗
t depends only on the earlier values of m∗, Mt−1 and does
not depend on the future values m∗
τ for τ > t. This justiﬁes drawing m∗
t sequentially over time,
using (A.14).
ECB Working Paper Series No 2133 / February 2018
45

Appendix B
Additional results for the US
B.1
Relaxing the restrictions on the dynamics of mt
In this subsection we show that our results are robust to relaxing the restrictions on the dynamics
of mt in the VAR. The unrestricted VAR is
 
mt
yt
!
=
P
X
p=1
 
Bp
MM
Bp
MY
Bp
Y M
Bp
Y Y
!  
mt−p
yt−p
!
+
 
cM
cY
!
+
 
um
t
uy
t
!
.
(B.1)
For the comparison of the restricted and the unrestricted VAR we use the sample without the
missing values in mt, i.e.
starting in February 1990.
Furthermore, we replace the missing
observation in September 2001 with zero. This is because handling missing data on mt becomes
more involved when the dynamics of mt is unrestricted. Panel A of Figure B.1 reports the
impulse responses obtained with the restricted VAR given in equation (1). We can see that they
are quite similar to the impulse responses in Figure 2, so starting the sample in 1990 does not
change the conclusions. Panel B of Figure B.1 reports the impulse responses obtained with the
unrestricted VAR given in equation (B.1). We can see that relaxing the zero restrictions in the
VAR hardly aﬀects the impulse responses.
B.2
Results on other subsamples
Figure B.1 showed that the ﬁndings hardly change when we start the sample in February 1990
instead of July 1979. Figure B.2 shows that the ﬁndings continue to be similar when we estimate
the VAR on a sample that starts in July 1979 but ends on December 2008, i.e. before the interest
rates hit the zero lower bound (ZLB) in January 2009 (Panel A). Furthermore, the ﬁndings
continue to be similar when we omit the high-frequency surprises before February 1994 (Panel
B). The motivation to omit these surprises is that the Fed did not issue a press release about
FOMC decisions until February 1994, so the earlier surprises might be coming from a diﬀerent
regime.
B.3
Results with Industrial Production and CPI
Figure B.3 shows that when we replace the real GDP and GDP deﬂator with the industrial
production and the CPI index, the standard high-frequency identiﬁcation yields a small price
puzzle, and our sign restrictions eliminate it.
ECB Working Paper Series No 2133 / February 2018
46

Figure B.1: Impulse responses in the restricted and in the unrestricted VAR. Sample January
1990 to December 2016.
Impulse responses to one standard deviation monetary policy and
central bank information shocks. Median (line), percentiles 16-84 (darker band), percentiles
5-95 (lighter band).
A. Restricted VAR given in equation (1)
B. Unrestricted VAR given in equation (B.1)
Monetary policy
CB information
(negative co-movement)
(positive co-movement)
Monetary policy
CB information
(negative co-movement)
(positive co-movement)
0
10
20
30
0
0.05
  surprise in
3m ff futures
0
10
20
30
0
0.05
0
10
20
30
-0.4
-0.2
0
0.2
0.4
surprise in
S&P500
0
10
20
30
-0.4
-0.2
0
0.2
0.4
0
10
20
30
-0.05
0
0.05
0.1
1y govt. bond
   yield (%)
0
10
20
30
-0.05
0
0.05
0.1
0
10
20
30
-2
-1
0
1
S&P500
(100 x log)
0
10
20
30
-2
-1
0
1
0
10
20
30
-0.2
-0.1
0
0.1
Real GDP
(100 x log)
0
10
20
30
-0.2
-0.1
0
0.1
0
10
20
30
-0.05
0
0.05
GDP deflator
(100 x log)
0
10
20
30
-0.05
0
0.05
0
10
20
30
-0.05
0
0.05
EBP
(%)
0
10
20
30
-0.05
0
0.05
0
10
20
30
0
0.02
0.04
  surprise in
3m ff futures
0
10
20
30
0
0.02
0.04
0
10
20
30
-0.4
-0.2
0
0.2
0.4
surprise in
S&P500
0
10
20
30
-0.4
-0.2
0
0.2
0.4
0
10
20
30
-0.05
0
0.05
0.1
1y govt. bond
   yield (%)
0
10
20
30
-0.05
0
0.05
0.1
0
10
20
30
-1
0
1
S&P500
(100 x log)
0
10
20
30
-1
0
1
0
10
20
30
-0.2
-0.1
0
0.1
Real GDP
(100 x log)
0
10
20
30
-0.2
-0.1
0
0.1
0
10
20
30
-0.08
-0.06
-0.04
-0.02
0
0.02
0.04
GDP deflator
(100 x log)
0
10
20
30
-0.08
-0.06
-0.04
-0.02
0
0.02
0.04
0
10
20
30
-0.05
0
0.05
EBP
(%)
0
10
20
30
-0.05
0
0.05
months
months
months
months
ECB Working Paper Series No 2133 / February 2018
47

Figure B.2: Impulse responses of yt to monetary policy and central bank information shocks:
results for subsamples. Median (line), percentiles 16-84 (darker band), percentiles 5-95 (lighter
band).
A. No ZLB (July 1979 - December 2008)
B. Drop mt before Feb. 1994
Monetary policy
CB information
(negative co-movement)
(positive co-movement)
Monetary policy
CB information
(negative co-movement)
(positive co-movement)
0
10
20
30
-0.2
0
0.2
1y govt. bond
   yield (%)
0
10
20
30
-0.2
0
0.2
0
10
20
30
-6
-4
-2
0
2
S&P500
(100 x log)
0
10
20
30
-6
-4
-2
0
2
0
10
20
30
-0.6
-0.4
-0.2
0
0.2
Real GDP
(100 x log)
0
10
20
30
-0.6
-0.4
-0.2
0
0.2
0
10
20
30
-0.2
-0.1
0
0.1
GDP deflator
(100 x log)
0
10
20
30
-0.2
-0.1
0
0.1
0
10
20
30
-0.05
0
0.05
EBP
(%)
0
10
20
30
-0.05
0
0.05
0
10
20
30
-0.1
0
0.1
1y govt. bond
   yield (%)
0
10
20
30
-0.1
0
0.1
0
10
20
30
-2
-1
0
1
S&P500
(100 x log)
0
10
20
30
-2
-1
0
1
0
10
20
30
-0.2
-0.1
0
0.1
Real GDP
(100 x log)
0
10
20
30
-0.2
-0.1
0
0.1
0
10
20
30
-0.1
-0.05
0
0.05
GDP deflator
(100 x log)
0
10
20
30
-0.1
-0.05
0
0.05
0
10
20
30
-0.05
0
0.05
EBP
(%)
0
10
20
30
-0.05
0
0.05
months
months
months
months
ECB Working Paper Series No 2133 / February 2018
48

Figure B.3: Impulse responses of yt to monetary policy and central bank information shocks,
model with Industrial Production and Consumer Price Index. Median (line), percentiles 16-84
(darker band), percentiles 5-95 (lighter band).
A. Sign restrictions
B. Standard HFI
Monetary policy
CB information
(negative co-movement)
(positive co-movement)
Monetary policy
(Choleski, 3m ﬀf ﬁrst)
0
10
20
30
0
0.1
0.2
1y govt. bond
   yield (%)
0
10
20
30
0
0.1
0.2
0
10
20
30
-2
-1
0
1
S&P500
(100 x log)
0
10
20
30
-2
-1
0
1
0
10
20
30
-0.8
-0.6
-0.4
-0.2
0
0.2
Ind. Prod.
(100 x log)
0
10
20
30
-0.8
-0.6
-0.4
-0.2
0
0.2
0
10
20
30
-0.2
0
0.2
CPI
(100 x log)
0
10
20
30
-0.2
0
0.2
0
10
20
30
-0.05
0
0.05
EBP
(%)
0
10
20
30
-0.05
0
0.05
0
10
20
30
0
0.1
0.2
1y govt. bond
   yield (%)
0
10
20
30
-2
-1
0
S&P500
(100 x log)
0
10
20
30
-0.8
-0.6
-0.4
-0.2
0
Ind. Prod.
(100 x log)
0
10
20
30
-0.1
0
0.1
CPI
(100 x log)
0
10
20
30
0
0.02
0.04
0.06
EBP
(%)
months
months
months
ECB Working Paper Series No 2133 / February 2018
49

B.4
VAR with factors of high-frequency surprises
This section shows the robustness of our results to alternative measures of surprises.
B.4.1
Factors of high-frequency surprises
We start by showing that the proportion and sizes of ‘wrong-signed’ responses of stock prices to
monetary policy surprises remain similar when we use alternative measures of surprises.
As an alternative measure of the interest rate surprises we compute the ‘policy indicator’
constructed as in Nakamura and Steinsson (2013) (who build on G¨urkaynak, Sack and Swanson,
2005b). Namely, this is the ﬁrst principal component of the surprises in fed funds futures and
eurodollar futures with one year or less to expiration. Five indicators enter into it: the current-
month fed funds future, the 3-month fed funds future, and the eurodollar futures at the horizons
of two, three and four quarters. The advantage of the policy indicator is that it captures even
more of the forward guidance. The disadvantage is that it relies on the eurodollar futures which
are not as liquid as the federal funds futures.
As an alternative measure of the stock price surprises we take the ﬁrst principal component
of the surprises in the S&P500, Nasdaq Composite and Wilshire 5000. Nasdaq Composite is
based on about 4000 stocks skewed towards the technology sector, and Wilshire 5000 is based
on 7000 stocks of essentially all publicly listed companies headquartered in the US. All three
indices are market capitalization-weighted. Our dataset has many missing values for Nasdaq and
Wilshire, so we use the alternating least squares (ALS) algorithm that simultaneously estimates
the missing values while computing principal components.
Table B.1 reports the correlations between the 3-month fed funds futures surprises, S&P500
surprises and the two alternative measures of surprises just discussed. The correlation between
the surprises in the 3-month fed funds futures and the policy index is 0.89. The correlation
between S&P500 and the ﬁrst principal component of the three stock indices is higher, 0.96.
The correlations between interest surprises and stock price surprises are between -0.4 and -0.5.
Table B.1: Correlations between surprises
3-m ﬀf
SP500
Policy indicator
1st p.c. of stocks
3-m ﬀf
1.00
SP500
-0.46
1.00
Policy indicator
0.89
-0.53
1.00
1st p.c. of stocks
-0.40
0.96
-0.47
1.00
Figure B.4 shows that when we use the alternative measures of surprises, the lessons on
the ‘wrong-signed’ responses of stock prices to interest rates hold. Still, in 33% of the cases
the co-movement between interest rates and stock price surprises is positive. This conﬁrms the
ECB Working Paper Series No 2133 / February 2018
50

lessons from Figure 1.
Figure B.4: Scatter plot of interest rate and stock price surprises. The policy indicator and the
1st principal component of stock indices.
surprise in the policy indicator
-10
-5
0
5
10
surprise in the 1st pc of stocks
-4
-2
0
2
4
6
8
I: 51
II: 55
III: 28
IV: 105
1/22/2008
Note: Black ﬁlled circles highlight the data points where both surprises have the same sign. The number in each
quadrant is the number of data points in the quadrant (not counting the data points for which one of the surprises
is zero).
B.4.2
Impulse responses
Now we use the factors extracted from multiple interest rate and stock market surprises as mt
in the VAR. Figure B.5 shows that using factors changes very little in the impulse responses.
The main diﬀerence is that the monthly S&P500 index now responds positively to the central
bank information shock.
B.5
Robust error bands of Giacomini and Kitagawa (2015)
This section shows that the impulse responses to the two shocks we identify continue to be very
diﬀerent from each other irrespective of the prior on the rotation matrices Q. We make this
point using the ‘multiple priors’ approach of Giacomini and Kitagawa (2015).
The prior on Q might be important, because the sign restrictions in Table 1 provide only a
set identiﬁcation, not a sharp identiﬁcation. That is, for every nonsingular variance matrix Σ
there is a continuum of rotation matrices Q that are consistent with the sign restrictions. Since
ECB Working Paper Series No 2133 / February 2018
51

Figure B.5: Impulse responses to one standard deviation shocks, VAR with factors of surprises. Median (line), percentiles 16-84 (darker
band), percentiles 5-95 (lighter band). Months on the horizontal axis.
A. Standard HFI
B. Sign restrictions
C. Poor man’s sign restrictions
Monetary policy
(Choleski, pol.ind. ﬁrst)
Monetary policy
CB information
(negative co-movement)
(positive co-movement)
Monetary policy
CB information
(poor man’s proxy)
(poor man’s proxy)
0
10
20
30
0
0.1
0.2
1y govt. bond
   yield (%)
0
10
20
30
-1.5
-1
-0.5
0
0.5
S&P500
(100 x log)
0
10
20
30
-0.2
-0.1
0
Real GDP
(100 x log)
0
10
20
30
-0.1
-0.05
0
GDP deflator
(100 x log)
0
10
20
30
-0.02
0
0.02
0.04
EBP
(%)
0
10
20
30
0
0.1
0.2
1y govt. bond
   yield (%)
0
10
20
30
0
0.1
0.2
0
10
20
30
-2
-1
0
1
S&P500
(100 x log)
0
10
20
30
-2
-1
0
1
0
10
20
30
-0.2
-0.1
0
0.1
Real GDP
(100 x log)
0
10
20
30
-0.2
-0.1
0
0.1
0
10
20
30
-0.1
-0.05
0
0.05
GDP deflator
(100 x log)
0
10
20
30
-0.1
-0.05
0
0.05
0
10
20
30
-0.05
0
0.05
EBP
(%)
0
10
20
30
-0.05
0
0.05
0
10
20
30
-0.05
0
0.05
0.1
0.15
1y govt. bond
   yield (%)
0
10
20
30
-0.05
0
0.05
0.1
0.15
0
10
20
30
-1
0
1
S&P500
(100 x log)
0
10
20
30
-1
0
1
0
10
20
30
-0.2
-0.1
0
0.1
Real GDP
(100 x log)
0
10
20
30
-0.2
-0.1
0
0.1
0
10
20
30
-0.1
-0.05
0
GDP deflator
(100 x log)
0
10
20
30
-0.1
-0.05
0
0
10
20
30
-0.05
0
0.05
EBP
(%)
0
10
20
30
-0.05
0
0.05
ECB Working Paper Series No 2133 / February 2018
52

the sample carries no information about Q, the weights on diﬀerent values of Q are determined
by the prior.
As most of the literature, we use the uniform prior on the space of rotation
matrices, conditionally on satisfying the sign restrictions (Rubio-Ramirez, Waggoner and Zha,
2010). How much could the impulse responses change if we used some other, non-uniform prior
on Q?
To answer this question we compute the ‘robust’ uncertainty bounds following Giacomini
and Kitagawa (2015). In this approach, the posterior mean bounds delineate the range of the
posterior means of the impulse responses across all possible priors on Q that satisfy the sign
restrictions. The X% robustiﬁed region is a range of values of the impulse responses that has
the posterior probability of at least X% under every possible prior on Q that satisﬁes the sign
restrictions.
Figure B.6: Impulse responses to one standard deviation shocks, baseline VAR, with ‘robust’
error bands of Giacomini and Kitagawa (2015). Posterior mean bounds (line), 68% robustiﬁed
region (darker band), 90% robustiﬁed region (lighter band).
Monetary policy
CB information
(negative co-movement)
(positive co-movement)
0
10
20
30
-0.1
0
0.1
0.2
1y govt. bond
   yield (%)
0
10
20
30
-0.1
0
0.1
0.2
0
10
20
30
-2
-1
0
1
S&P500
(100 x log)
0
10
20
30
-2
-1
0
1
0
10
20
30
-0.2
-0.1
0
0.1
Real GDP
(100 x log)
0
10
20
30
-0.2
-0.1
0
0.1
0
10
20
30
-0.1
0
0.1
GDP deflator
(100 x log)
0
10
20
30
-0.1
0
0.1
0
10
20
30
-0.05
0
0.05
EBP
(%)
0
10
20
30
-0.05
0
0.05
months
months
Figure B.6 reports the robust bounds for the impulse responses of all variables yt at all
horizons.
The bounds are wider and include zero more often than the bounds in Figure 2,
ECB Working Paper Series No 2133 / February 2018
53

but the diﬀerent nature of the monetary policy and central bank information shocks remains
clear. Furthermore, let us make two comments related to the width of the bounds. First, the
robust bounds are conservative because they account for the ‘worst-case’ prior on Q for each
variable, shock and horizon separately. Any single prior on Q will produce narrower bands.
Second, there are many ways to reﬁne the sign restriction identiﬁcation by postulating further
reasonable restrictions on the impulse responses. Our point in this paper is that the simple sign
restriction we propose is enough to separate two shocks of very diﬀerent nature.
Appendix C
Surprises and proxies for Fed’s private information
In this section we study the relation between a popular proxy for the private information available
to the FOMC members and the central bank information shocks we identify. We ﬁnd mixed
results.
Empirical proxies for the FOMC private information used in the literature are based on the
diﬀerences between the Fed staﬀforecasts and private forecasts. For every scheduled FOMC
meeting, the Fed staﬀprepares nowcasts and forecasts of the price level and economic activity.
These forecasts do not directly inﬂuence private forecasts, because they are made public only
with a 5 year delay. However, they are made available to the FOMC members, who can take
them into account when setting the course of policy and formulating oﬃcial communication. The
staﬀforecasts have been shown to have superior forecasting ability relative to private forecasts
(Romer and Romer, 2000). The diﬀerence between the staﬀforecasts and forecasts of private
forecasters, therefore, is a popular proxy for the private information of the FOMC. Controlling
for private information using these proxies has been shown to inﬂuence predictions about the
eﬀects of monetary policy shocks (Gertler and Karadi, 2015; Campbell et al., 2016).
It is far from clear, however, how much of the FOMC private information is actually revealed
through a policy change and the accompanying communication. FOMC decision makers might
not share the views of the staﬀabout the economy, and even if they do their communication
might not be detailed enough to explain all the assumptions behind their choices. Therefore,
instead of using such proxies, we use market-price reactions to the announcements to learn about
the information content of the FOMC statements in our baseline regressions. Changes in asset
prices provide more ﬁrst-hand signal about the extent of new information in the statement as
assessed by market participants (and not just by economic forecasters), who can be expected to
have key inﬂuence on market prices that drive economic fundamentals. Still, it is worthwhile to
assess how well our measures line up with private information proxies.
To this end, we regress the surprises in the 3-month fed funds futures and our two identiﬁed
shocks on proxies for the FOMC private information. The variables are at the monthly fre-
quency. As measures of the two shocks we take the posterior medians of the respective shocks’
contributions to the surprises in the 3-month fed funds futures. The proxy for the FOMC private
information is standard in the literature. In particular, we link the staﬀforecasts on scheduled
ECB Working Paper Series No 2133 / February 2018
54

Table C.1: Surprises and proxies for Fed private information
(1)
(2)
(3)
Variables
Surprise in
3m ﬀf
Monetary
policy shock
CB information
shock
πt
0.00203
0.00209
0.000288
(0.330)
(0.383)
(0.0660)
πt+1
0.00623
0.00163
0.00497
(0.474)
(0.201)
(0.776)
πt+2
-0.00799
-0.00514
-0.00363
(-0.835)
(-0.849)
(-0.717)
dyt
0.0181***
0.0183***
-0.00141
(2.893)
(3.119)
(-0.388)
dyt+1
0.0140
0.000733
0.0143***
(1.379)
(0.0886)
(3.078)
dyt+2
-0.00758
-0.00220
-0.00671
(-0.891)
(-0.341)
(-1.643)
ut
-0.0279
-0.0256
-0.00629
(-0.630)
(-0.796)
(-0.296)
Observations
180
180
180
R-squared
0.117
0.116
0.070
Robust t-statistics in parentheses
*** p<0.01, ** p<0.05, * p<0.1
FOMC meetings with the last preceding forecasts surveyed by the Blue Chip Economic Indica-
tors. We use the current, and the one- and two-quarters ahead GDP deﬂator (πt, πt+1, πt+2) and
real GDP growth (dyt, dyt+1, dyt+2) forecasts and the current month unemployment forecasts
(ut). We take a simple diﬀerence between the staﬀand private forecasts for each variable. The
regression results are shown in Table C.1.
The results are mixed. We ﬁnd that private information about the one-quarter-ahead real
GDP growth inﬂuences the central bank information shocks signiﬁcantly. At the same time,
we do not ﬁnd that private information about prices or the unemployment rate would inﬂuence
the same shock; and we also ﬁnd that private information about the current-quarter real GDP
growth inﬂuences our monetary policy shock.
Appendix D
High-frequency euro area data
We use high-frequency data on euro area asset prices to build a dataset of high-frequency asset
price responses to the ECB policy announcements, analogous to the G¨urkaynak et al. (2005b)
ECB Working Paper Series No 2133 / February 2018
55

dataset for the US. We take the high-frequency asset price data from the Thomson Reuters Tick
History database. Our dataset has two kinds of assets: interest rate swaps and stock prices.
Stock prices. For the stock prices it is straightforward to obtain high-frequency data, since
stocks are traded in centralized markets. The stock index we use is Euro Stoxx 50. The Thomson
Reuters includes its price multiple times a second.
Interest rate swaps. In the euro area we use the interest rate swaps instead of the futures,
as the swap market is more liquid and has a longer history. We use the Overnight Indexed
Swaps (OIS) based on the Eonia rate. In this swap contract the parties exchange the variable,
overnight Eonia rate for the ﬁxed swap rate. We focus on the 3-month swap.
Measuring the Eonia OIS rate is more diﬃcult than measuring stock prices, because these
swaps are traded in over-the-counter markets. We do not observe the prices. Thomson Reuters
only provides the quotes posted by individual traders. The quotes consist of a bid rate and an
ask rate, and the trades are concluded over the phone. The database includes bid and ask quotes
with time stamps (at the millisecond level) and with the identity of the posting institution. Some
quotes are outliers that cannot reasonably reﬂect actual trades (e.g. they diﬀer from the other
quotes at that time by orders of magnitude). To clean the data from the outliers, for each
day, we exclude the lowest and highest 1 percents of bid and ask quotes. In some instances,
we eliminate further outliers if they are very far from the outstanding quotes (sometimes 5-6
standard deviations away) making it unreasonable to assume that any trade was conducted at
the quoted price.
We measure the market price as the average of the highest bid and lowest ask prices out
of the most recent ﬁve quotes made by distinct institutions. Furthermore, we disregard quotes
posted more than 15 minutes ago, even if this reduces the number of available quotes below 5.
In the instances when the highest bid price is higher than the lowest ask price we go for the
second-highest and second-lowest or third-highest and third-lowest if necessary. Our choices are
informed by our aim to obtain an accurate and timely proxy for market valuation. Choosing the
ﬁve latest quotes balances timeliness with accuracy: if after a market news 5 institutions modiﬁed
their quotes, we would like our measure to reﬂect the change, even if some still outstanding quotes
(possibly posted before the news) suggest diﬀerent valuations. We disregard quotes older than
15 minutes altogether, because quotes can not be directly traded on. They are indicative of the
valuation of the posting institution only when they were made, and can lose their actuality over
time. The 15 minutes limit guarantees that our baseline surprise measure, which reads the asset
price 20 minutes after the monetary policy news, does not include quotes made before the news.
Figure D.1 shows two examples illustrating how we process the data on quotes. Each quote
is represented by a pair of dots: a blue dot, showing the bid rate, and a red dot, showing the ask
rate. The outliers are already removed, as they would distort the scale of the picture. The black
line shows the midquote, which is our measure of the market rate. The ﬁrst panel presents the
market for the 3-month Eonia OIS (EUREON3M) on May 10th, 2001. On that day the ECB
announced a 25 basis point cut in its policy rates. The press release was issued at 13:45. We
ECB Working Paper Series No 2133 / February 2018
56

Figure D.1: Construction of high-frequency surprises for the 3-month Eonia swap rate.
4.5
4.55
4.6
4.65
4.7
08:00
09:00
10:00
11:00
12:00
13:00
14:00
15:00
16:00
17:00
18:00
Bid Price
Ask Price
midquote
EUREON3M 2001-05-10
.8
.85
.9
.95
1
08:00
09:00
10:00
11:00
12:00
13:00
14:00
15:00
16:00
17:00
18:00
Bid Price
Ask Price
midquote
EUREON3M 2011-03-03
can see that around 13:45 the quotes drop by about 20 basis points. The midquote we compute
drops with the quotes. The second panel shows the data for March 3rd, 2011. The activity
in the market is higher in 2011 than in 2001, as witnessed by a much larger number of quotes
posted. On this particular day the ECB Governing Council decided to keep the policy rates
unchanged. This was anticipated, so the press release at 13:45 did not contain any surprises.
However, during the press conference that started at 14:30 and lasted about an hour, the ECB
President Jean-Claude Trichet delivered a hawkish message. He highlighted the upwards risks
to inﬂation coming from an increase in commodity prices, and concerns about second-round
ECB Working Paper Series No 2133 / February 2018
57

eﬀects (i.e. the price increases fuelling wage increases). By the end of the press conference the
3-month Eonia OIS was about 10 basis points higher, reﬂecting expectations of future interest
rate increases.
Appendix E
Calibrated model parameters
Table E.1: Calibrated model parameters
Households
β
0.990
Discount rate
h
0.815
Habit parameter
χ
3.411
Relative utility weight of labor
ϕ
0.276
Inverse Frisch elasticity of labor supply
¯Sh/S
0.500
Relative steady state direct HH holding of debt
ϱk,x
0.974
Rate of geometric decline of a corporate bond with duration x
Financial Intermediaries
θ
0.343
Fraction of capital that can be diverted
ω
0.0019
Start-up fund for the entering bankers
σ
0.972
Survival rate of the bankers
Intermediate good ﬁrms
α
0.330
Capital share
δ
0.025
Depreciation rate
Capital Producing Firms
ηi
1.728
Inverse elasticity of net investment to the price of capital
Retail Firms
ϵ
4.167
Elasticity of substitution
Government
G
Y
0.200
Steady state proportion of government expenditures
κπ
1.500
Inﬂation coeﬃcient in the Taylor rule
κx
-0.125
Markup coeﬃcient in the Taylor rule
ECB Working Paper Series No 2133 / February 2018
58

References
Andrade, Philippe and Filippo Ferroni (2016) “Delphic and Odyssean Monetary Policy Shocks:
Evidence from the Euro-Area,” Discussion Paper 12-16, University of Surrey.
Barakchian, S. Mahdi and Christopher Crowe (2013) “Monetary Policy Matters: Evidence from
New Shocks Data,” Journal of Monetary Economics, Vol. 60, pp. 950–966.
Bauwens, Luc, Michel Lubrano, and Jean-Francois Richard (1999) Bayesian Inference in Dy-
namic Econometric Models, Oxford: Oxford University Press.
Bernanke, Ben S. (2010) “Monetary policy and the housing bubble: a speech at the Annual
Meeting of the American Economic Association, Atlanta, Georgia, January 3, 2010,” Speech
499, Board of Governors of the Federal Reserve System (U.S.).
Bernanke, Ben S. and Alan S. Blinder (1992) “The Federal Funds Rate and the Channels of
Monetary Transmission,” American Economic Review, Vol. 82, pp. 901–921.
Bernanke, Ben S. and Kenneth N. Kuttner (2005) “What Explains the Stock Market’s Reaction
to Federal Reserve Policy?” The Journal of Finance, Vol. 60, pp. 1221–1257.
Caldara, Dario and Edward Herbst (2016) “Monetary Policy, Real Activity, and Credit Spreads:
Evidence from Bayesian Proxy SVARs,” Finance and Economics Discussion Series 2016-049,
Board of Governors of the Federal Reserve System.
Campbell, Jeﬀrey R., Charles L. Evans, Jonas D. M. Fisher, and Alejandro Justiniano (2012)
“Macroeconomic Eﬀects of Federal Reserve Forward Guidance,” Brookings Papers on Eco-
nomic Activity, pp. 1–80.
Campbell, Jeﬀrey R., Jonas D. M. Fisher, Alejandro Justiniano, and Leonardo Melosi (2016)
“Forward Guidance and Macroeconomic Outcomes Since the Financial Crisis,” in NBER
Macroeconomics Annual 2016, Volume 31: University of Chicago Press.
Christiano, Lawrence J., Martin Eichenbaum, and Charles Evans (1996) “The Eﬀects of Mone-
tary Policy Shocks: Evidence from the Flow of Funds,” The Review of Economics and Statis-
tics, pp. 16–34.
Christiano, Lawrence J., Martin Eichenbaum, and Charles L. Evans (2005) “Nominal Rigidities
and the Dynamic Eﬀects of a Shock to Monetary Policy,” The Journal of Political Economy,
Vol. 113, pp. 1–45.
Clark, Todd E., Andrea Carriero, and Massimiliano Marcellino (2016) “Large Vector Autore-
gressions with Stochastic Volatility and Flexible Priors,” Working Paper 1617, Federal Reserve
Bank of Cleveland.
ECB Working Paper Series No 2133 / February 2018
59

Coibion, Olivier and Yuriy Gorodnichenko (2012) “What Can Survey Forecasts Tell Us About
Information Rigidities?” Journal of Political Economy, Vol. 120, pp. 116–159.
Corsetti, Giancarlo, Joao B. Duarte, and Samuel Mann (2018) “One Money, Many Markets: A
Factor Model Approach to Monetary Policy in the Euro Area with High-Frequency Identiﬁ-
cation,” Working Paper, University of Cambridge.
Faust, Jon, Eric T. Swanson, and Jonathan H. Wright (2004) “Do Federal Reserve Policy Sur-
prises Reveal Superior Information about the Economy,” Contributions to Macroeconomics,
Vol. 4, pp. 1–29.
Favara, Giovanni, Simon Gilchrist, Kurt F. Lewis, and Egon Zakrajsek (2016) “Updating the Re-
cession Risk and the Excess Bond Premium,” FEDS Notes. Washington: Board of Governors
of the Federal Reserve System, October 6.
Gal´ı, Jordi (2014) “Monetary Policy and Rational Asset Price Bubbles,” The American Eco-
nomic Review, Vol. 104, pp. 721–752.
Gertler, Mark and Peter Karadi (2011) “A Model of Unconventional Monetary Policy,” Journal
of Monetary Economics, Vol. 58, pp. 17–34.
(2013) “QE 1 vs. 2 vs. 3...: A Framework for Analyzing Large-Scale Asset Purchases
as a Monetary Policy Tool,” International Journal of Central Banking, Vol. 9, pp. 5–53.
(2015) “Monetary Policy Surprises, Credit Costs, and Economic Activity,” American
Economic Journal: Macroeconomics, Vol. 7, pp. 44–76.
Giacomini, Rafaella and Toru Kitagawa (2015) “Robust inference about partially identiﬁed
SVARs,” mimeo, University College London.
Gilchrist, Simon and Egon Zakrajsek (2012) “Credit Spreads and Business Cycle Fluctuations,”
The American Economic Review, Vol. 102, pp. 1692–1720.
G¨urkaynak, Refet S., Brian Sack, and Eric Swanson (2005a) “The Sensitivity of Long-Term
Interest Rates to Economic News: Evidence and Implications for Macroeconomic Models,”
American Economic Review, pp. 425–436.
G¨urkaynak, Refet S., Brian Sack, and Eric Swanson (2005b) “Do Actions Speak Louder Than
Words? The Response of Asset Prices to Monetary Policy Actions and Statements,” Interna-
tional Journal of Central Banking, Vol. 1, pp. 55–93.
G¨urkaynak, Refet S., Brian Sack, and Jonathan H. Wright (2007) “The US Treasury Yield
Curve: 1961 to the Present,” Journal of Monetary Economics, Vol. 54, pp. 2291–2304.
(2010) “The TIPS Yield Curve and Inﬂation Compensation,” American Economic Jour-
nal: Macroeconomics, Vol. 2, pp. 70–92.
ECB Working Paper Series No 2133 / February 2018
60

Hansen, Stephen and Michael McMahon (2016) “Shocking Language:
Understanding the
Macroeconomic Eﬀects of Central Bank Communication,” Journal of International Eco-
nomics, Vol. 99, pp. S114–S133.
Kuttner, Kenneth N. (2001) “Monetary Policy Surprises and Interest Rates: Evidence from the
Fed Funds Futures Market,” Journal of Monetary Economics, Vol. 47, pp. 523–544.
Lakdawala, Aeimit and Matthew Schaﬀer (2016b) “Federal Reserve Private Information and the
Stock Market,” MPRA Paper, University Library of Munich, Germany.
Litterman, Robert B. (1979) “Techniques of Forecasting Using Vector Autoregressions,” Federal
Reserve Bank of Minneapolis Working Paper number 115.
Lucca, David O. and Emanuel Moench (2015) “The Pre-FOMC Announcement Drift,” Journal
of Finance, Vol. 70, pp. 329–371.
Melosi, Leonardo (2017) “Signalling Eﬀects of Monetary Policy,” The Review of Economic Stud-
ies, Vol. 84, pp. 853–884.
Mertens, Karel and Morten O. Ravn (2013) “The Dynamic Eﬀects of Personal and Corporate
Income Tax Changes in the United States,” The American Economic Review, Vol. 103, pp.
1212–1247.
Miranda-Agrippino, Silvia (2016) “Unsurprising shocks: information, premia, and the monetary
transmission,” Bank of England working papers 626, Bank of England.
Nakamura, Emi and J´on Steinsson (2013) “High Frequency Identiﬁcation of Monetary Non-
Neutrality: The Information Eﬀect,” Working Paper 19260, National Bureau of Economic
Research, updated 2017.
Paul, Pascal (2017) “The Time-Varying Eﬀect of Monetary Policy on Asset Prices,” Working
Paper Series 2017-9, Federal Reserve Bank of San Francisco.
Romer, David H. and Christina D. Romer (2000) “Federal Reserve Information and the Behavior
of Interest Rates,” American Economic Review, Vol. 90, pp. 429–457.
Rubio-Ramirez, Juan F., Daniel F. Waggoner, and Tao Zha (2010) “Structural Vector Au-
toregressions: Theory of Identiﬁcation and Algorithms for Inference,” Review of Economic
Studies, Vol. 77, pp. 665–696.
Stock, James H. and Mark W. Watson (2010) “Monthly GDP and GNI - Research Memoran-
dum,” manuscript.
(2012) “Disentangling the Channels of the 2007–09 Recession,” Brookings Papers on
Economic Activity, Vol. 2012, pp. 81–135.
ECB Working Paper Series No 2133 / February 2018
61

(2017) “Identiﬁcation and Estimation of Dynamic Causal Eﬀects in Macroeconomics,”
Working Paper.
Taylor, John B. (2007) “Housing and monetary policy,” in Proceedings - Economic Policy Sym-
posium - Jackson Hole, pp. 463–476.
Uhlig, Harald (2005) “What are the eﬀects of monetary policy on output? Results from an
agnostic identiﬁcation procedure,” Journal of Monetary Economics, Vol. 52, pp. 381–419.
ECB Working Paper Series No 2133 / February 2018
62

Acknowledgements 
All opinions expressed are personal and do not necessarily represent the view of the European Central Bank. An earlier version of this 
paper was circulated under the title "Central Bank Information Shocks." We thank Refet Gürkaynak for sharing his data. For comments 
and suggestions, we thank Marco Del Negro, Peter Hoffmann, Giovanni Lombardo, Giorgio Primiceri, Paolo Surico, Oreste Tristani, 
Johannes Wieland, Srecko Zimic and numerous seminar and conference participants. Maria Dimou, Cinzia Guerrieri and Andras 
Lengyel provided outstanding research assistance. 
 
Marek Jarociński 
European Central Bank, Frankfurt am Main, Germany; email: marek.jarocinski@ecb.europa.eu 
 
Peter Karadi 
European Central Bank, Frankfurt am Main, Germany; email: peter.karadi@ecb.europa.eu 
 
 
© European Central Bank, 2018 
Postal address 60640 Frankfurt am Main, Germany 
Telephone 
+49 69 1344 0 
Website 
www.ecb.europa.eu 
All rights reserved. Any reproduction, publication and reprint in the form of a different publication, whether printed or produced 
electronically, in whole or in part, is permitted only with the explicit written authorisation of the ECB or the authors.  
This paper can be downloaded without charge from www.ecb.europa.eu, from the Social Science Research Network electronic library or 
from RePEc: Research Papers in Economics. Information on all of the papers published in the ECB Working Paper Series can be found 
on the ECB’s website. 
PDF 
ISBN 978-92-899-3238-7 
ISSN 1725-2806 
doi:10.2866/306683,  
QB-AR-18-013-EN-N