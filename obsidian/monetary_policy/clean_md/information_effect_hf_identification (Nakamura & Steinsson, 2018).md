NBER WORKING PAPER SERIES
HIGH FREQUENCY IDENTIFICATION OF MONETARY NON-NEUTRALITY:
THE INFORMATION EFFECT
Emi Nakamura
Jón Steinsson
Working Paper 19260
NATIONAL BUREAU OF ECONOMIC RESEARCH
1050 Massachusetts Avenue
Cambridge, MA 02138
July 2013, Revised January 2018
We thank Miguel Acosta, Matthieu Bellon, Vlad Bouchouev, Nicolas Crouzet, Stephane Dupraz, 
Michele Fornino, Jesse Garret, and Shaowen Luo, for excellent research assistance. We thank 
Michael Abrahams, Tobias Adrian, Richard K. Crump, Matthias Fleckenstein, Michael Fleming, 
Mark Gertler, Refet Gurkaynak, Peter Karadi, Hanno Lustig, Emanuel Moench, and Eric 
Swanson for generously sharing data and programs with us. We thank Robert Barro, Marco 
Bassetto, Gabriel Chodorow-Reich, Stephane Dupraz, Gauti Eggertsson, Mark Gertler, Refet 
Gurkaynak, Samuel Hanson, Sophocles Mavroeidis, Emanuel Moench, Serena Ng, Roberto 
Rigobon, Christina Romer, David Romer, Christoph Rothe, Eric Swanson, Ivan Werning, 
Michael Woodford, Jonathan Wright and seminar participants at various institutions for valuable 
comments and discussions. We thank the National Science Foundation (grant SES-1056107), the 
Alfred P. Sloan Foundation, and the Columbia Business School Dean’s Office Summer Research 
Assistance Program for financial support. The views expressed herein are those of the authors and 
do not necessarily reflect the views of the National Bureau of Economic Research.
NBER working papers are circulated for discussion and comment purposes. They have not been 
peer-reviewed or been subject to the review by the NBER Board of Directors that accompanies 
official NBER publications.
exceed two paragraphs, may be quoted without explicit permission provided that full credit, 
including © notice, is given to the source.

High Frequency Identification of Monetary Non-Neutrality: The Information Effect 
Emi Nakamura and Jón Steinsson
NBER Working Paper No. 19260
July 2013, Revised January 2018
JEL No. E30,E40,E50
ABSTRACT
We present estimates of monetary non-neutrality based on evidence from high-frequency 
responses of real interest rates, expected inflation, and expected output growth. Our identifying 
assumption is that unexpected changes in interest rates in a 30-minute window surrounding 
scheduled Federal Reserve announcements arise from news about monetary policy. In response to 
an interest rate hike, nominal and real interest rates increase roughly one-for-one, several years 
out into the term structure, while the response of expected inflation is small. At the same time, 
forecasts about output growth also increase—the opposite of what standard models imply about a 
monetary tightening. To explain these facts, we build a model in which Fed announcements affect 
beliefs not only about monetary policy but also about other economic fundamentals. Our model 
implies that these information effects play an important role in the overall causal effect of 
monetary policy shocks on output.
Emi Nakamura
Columbia Business School
3022 Broadway, Uris Hall 820
New York, NY 10027
and NBER
Jón Steinsson
Department of Economics
Columbia University
1026 International Affairs Building
420 West 118th Street
New York, NY 10027
and NBER

Introduction
A central question in macroeconomics is how monetary policy affects the economy. The key empir-
ical challenge in answering this question is that most changes in interest rates happen for a reason.
For example, the Fed might lower interest rates to counteract the effects of an adverse shock to the
ﬁnancial sector. In this case, the effect of the Fed’s actions are confounded by the ﬁnancial shock,
making it difﬁcult to identify the effects of monetary policy. The most common approach to over-
coming this endogeneity problem is to attempt to control for confounding variables. This is the
approach to identiﬁcation in VAR studies such as Christiano, Eichenbaum, and Evans (1999) and
Bernanke, Boivin, and Eliasz (2005), and also in the work of Romer and Romer (2004). The worry
with this approach is that despite efforts to control for important confounding variables, some en-
dogeneity bias remains (see, e.g., Rudebusch, 1998).
An alternative approach—the one we pursue in this paper—is to focus on movements in bond
prices in a narrow window around scheduled Federal Open Market Committee (FOMC) meetings.
This high frequency identiﬁcation approach was pioneered by Cook and Hahn (1989), Kuttner
(2001), and Cochrane and Piazzesi (2002). It exploits the fact that a disproportionate amount of
monetary news is revealed at the time of the eight regularly scheduled FOMC meetings each year.
The lumpy way in which monetary news is revealed allows for a discontinuity-based identiﬁcation
scheme.
We construct monetary shocks using unexpected changes in interest rates over a 30-minute win-
dow surrounding scheduled Federal Reserve announcements. All information that is public at the
beginning of the 30-minute window is already incorporated into ﬁnancial markets, and, therefore,
does not show up as spurious variation in the monetary shock. Such spurious variation is an impor-
tant concern in VARs. For example, Cochrane and Piazzesi (2002) show that VAR methods (even
using monthly data) interpret the sharp drop in interest rates in September 2001 as a monetary
shock as opposed to a reaction to the terrorist attacks on 9/11/2001.
A major strength of the high-frequency identiﬁcation approach we use is how cleanly it is able
to address the endogeneity concern. As is often the case, this comes at the cost of reduced statistical
power. The monetary shocks we estimate are quite small (they have a standard deviation of only
about 5 basis points). This “power problem” precludes us from directly estimating their affect on
future output. Intuitively, output several quarters in the future is inﬂuenced by a myriad of other
shocks, rendering the signal-to-noise ratio in such regressions too small to yield reliable inference.
We can, however, measure the response of variables that respond contemporaneously such as

ﬁnancial variables and survey expectations. Since the late 1990’s it has been possible to observe the
response of real interest rates via the Treasury Inﬂation Protected Securities (TIPS) market. This is
important since the link between nominal interest rates and real interest rates is the distinguishing
feature of models in which monetary policy affects real outcomes. All models—Neoclassical and
New Keynesian—imply that real interest rates affect output. However, New Keynesian and Neo-
classical models differ sharply as to whether monetary policy actions can have persistent effects on
real interest rates. In New Keynesian models, they do, while in Neoclassical models real interest
rates are decoupled from monetary policy. By focusing on the effects of monetary policy shocks on
real interest rates, we are shedding light on the core empirical issue in monetary economics.
We use the term structure of interest rates at the time of FOMC meetings to show that the mone-
tary shocks we identify have large and persistent effects on expected real interest rates as measured
by TIPS. Nominal and real interest rates respond roughly one-for-one several years out into the
term structure in response to our monetary shocks. The effect on real rates peaks at around 2 years
and then falls monotonically to zero at 10 years. In sharp contrast, the response of break-even in-
ﬂation (the difference between nominal and real rates from TIPS) is essentially zero at horizons
up to three years. At longer horizons, the response of break-even inﬂation becomes modestly, but
signiﬁcantly, negative. A tightening of monetary policy therefore eventually reduces inﬂation—as
standard theory would predict. However, the response is small and occurs only after a long lag.
What can we conclude from these facts? Under the conventional interpretation of monetary
shocks, these facts imply a great deal of monetary non-neutrality. Intuitively, a monetary-policy-
induced increase in real interest rates leads to a drop in output relative to potential, which in turn
leads to a drop in inﬂation. The response of inﬂation relative to the change in the real interest rates is
determined by the slope of the Phillips curve (as well as the intertemporal elasticity of substitution).
If the inﬂation response is small relative to the change in the real rates, the slope of the Phillips curve
must be small implying large nominal and real rigidities and, therefore, large amounts of monetary
non-neutrality.
There is, however, an additional empirical fact that does not ﬁt this interpretation. We docu-
ment that in response to an unexpected increase in the real interest rate (a monetary tightening),
survey estimates of expected output growth rise. Under the conventional interpretation of mone-
tary shocks, a tightening of policy should lead to a fall in output growth. Our empirical ﬁnding
regarding output growth expectations is therefore the opposite direction from what one would ex-
pect from the conventional interpretation of monetary shocks.
A natural interpretation of this evidence is that FOMC announcements lead the private sector to

update its beliefs not only about the future path of monetary policy, but also about other economic
fundamentals. For example, when the Fed Chair announces that the economy is strong enough
to withstand higher interest rates, market participants may react by reconsidering their own be-
liefs about the economy. Market participants may contemplate that perhaps the Fed has formed
a more optimistic assessment of the economic outlook than they have and that they may want to
reconsider their own assessments. Following Romer and Romer (2000), we refer to the effect of
FOMC announcements on private sector views of non-monetary economic fundamentals as “Fed
information effects.”
The Fed information effect calls for more sophisticated modeling of the effects of monetary
shocks than is standard. The main challenge is how to parsimoniously model these information
effects. We present a new model in which monetary shocks affect not only the trajectory of the real
interest rate, but also private sector beliefs about the trajectory of the natural rate of interest. This is
a natural way of modeling the information content of Fed announcements since optimal monetary
policy calls for interest rates to track the natural rate in simple models. Since the Fed is attempting
to track the natural rate, it is natural to assume that Fed announcements contain information about
the path of the natural rate.
Our “Fed information model” implies less monetary non-neutrality through conventional chan-
nels than a model that ignores Fed information. The reason is that the response of inﬂation is de-
termined by the response of the real interest rate gap—the gap between the response of real interest
rates and the natural real rate—which is smaller than the response of real interest rates themselves.
Intuitively, some of the increase of real rates is interpreted not as a tightening of policy relative to
the natural rate—which would push inﬂation down—but rather as an increase in the natural rate
itself—which does not.
If the Fed information effect is large, even a large response of real interest rates to a monetary
shock is consistent with the conventional channel of monetary non-neutrality being modest (since
the real interest rate movement is mostly due to a change in the natural real rate). However, this
does not mean that the Fed is powerless. To the contrary, if the Fed information effect is large, the
Fed has a great deal of power over private sector beliefs about economic fundamentals, which may
in turn have large effects on economic activity. If a Fed tightening makes the private sector more
optimistic about the future, this will raise current consumption and investment in models with
dynamic linkages. Depending on the strength of the Fed information effect, our evidence, therefore,
suggests either that the Fed has a great deal of power over the economy through traditional channels
or that the Fed has a great deal of power over the economy through non-traditional information

channels (or some combination of the two).
To assess the extent of Fed information and the nature of Fed power over the economy, we
estimate our Fed information model using as target moments the responses of real interest rates,
expected inﬂation, and expected output growth discussed above. Here, we follow in the tradition
of earlier quantitative work such as Rotemberg and Woodford (1997) and Christiano, Eichenbaum,
and Evans (2005), with two important differences. First, our empirical targets are identiﬁed using
high-frequency identiﬁcation as opposed to a VAR. Second, we allow for Fed information effects in
our model.
Our estimates imply that the Fed information effect is large. Roughly 2/3 of the response of real
interest rates to FOMC announcements are estimated to be a response of the natural rate of interest
and only 1/3 a tightening of real rates relative to the natural rate. This large estimate of the Fed
information effect allows us to simultaneously match the fact that beliefs about output growth rise
following a monetary shock and inﬂation eventually falls. Beliefs about output growth rise because
agents are more optimistic about the path for potential output. Inﬂation falls because a portion of
the shock is interpreted as rates rising relative to the natural rate.
Once we allow for Fed information effects, the causal effect of monetary policy is much more
subtle to identify. Our estimates imply that surprise FOMC monetary tightenings have large posi-
tive effects on expectations about output growth. Does this imply that the monetary announcements
cause output to increase by large amounts? No, not necessarily. Much of the news the Fed reveals
about non-monetary fundamentals would have eventually been revealed through other sources. To
correctly assess the causal effect of monetary policy, one must compare versus a counterfactual in
which the changes in fundamentals the Fed reveals information about occur even in the absence of
the announcement. The causal effect of the Fed information is then limited to the effect on output
of the Fed announcing this information earlier than it otherwise would have become known.
Our model makes these channels precise. Recent discussions of monetary policy have noted
the Fed’s reluctance to lower interest rates for fear it might engender pessimistic expectations that
would ﬁght against its goal of stimulating the economy. Our analysis suggests that these concerns
may be well-founded at least at the zero lower bound.1 Moreover, our model suggests that the im-
plications of systematic monetary policy actions are quite different from those of monetary shocks.
The reason is that systematic monetary policy actions don’t entail information effects since, by def-
inition, they are not based on private information. In other words, there is an important external
1Revealing information about natural rates, even bad news, is likely to be welfare improving as long as the Fed can
vary interest rates to track the natural rate. At the zero lower bound, the Fed however looses its ability to track the natural
rate. Withholding bad news may then be optimal.

validity problem whenever researchers use monetary shocks to try to infer the effects of systematic
monetary policy. We use a structural model to solve this external validity problem.
Our measure of monetary shocks is based not only on surprise changes in the federal funds rate
but also changes in the path of future interest rates in response to FOMC announcements. This is
important since over the past 15 years forward guidance has become an increasingly important tool
in the conduct of monetary policy (Gurkaynak, Sack, and Swanson, 2005). This also implies that it
is important to focus on a narrow 30-minute window as opposed to the 1-day or 2-day windows
more commonly used in prior work. We make use of Rigobon’s (2003) heteroskedasticity-based
estimator to show that OLS results based on monetary shocks constructed from longer-term interest
rate changes over one-day windows around FOMC announcements are confounded by substantial
“background noise” that lead to unreliable inference and in particular can massively overstate the
true statistical precision of the estimates. In contrast, OLS yields reliable results when a 30-minute
window is used.
An important question about our empirical estimates is whether some of the effects of our mon-
etary shocks on longer-term real interest rates reﬂect changes in risk premia as opposed to changes
in expected future short-term real interest rates. We use three main approaches to analyze this is-
sue: direct survey expectations of real interest rates, an afﬁne term structure model, and an analysis
of mean reversion. None of these pieces of evidence suggest that movements in risk premia at the
time of FOMC announcements play an important role in our results. In other words, our results
suggest that the expectations hypothesis of the term structure is a good approximation in response
to our monetary shocks, even though it is not a good approximation unconditionally. This is what
we need for our analysis to be valid.
Another important (and related) question is whether there might be a predictable component of
the monetary shocks we analyze and how this might affect the interpretation of our results. In our
analysis of real interest rates, the dependent variables are high frequency changes. The error terms
in these regressions, therefore, only contain information revealed in that narrow window, and the
identifying assumption is that our monetary shock is orthogonal to this limited amount of infor-
mation. This methodology has the advantage that we need not assume that our monetary shock
is orthogonal to macro shocks occurring on other days or to slow-moving confounding variables.
The identifying assumptions are stronger when we analyze the effects of our monetary shocks on
survey expectations from the Blue Chip data. In that analysis the dependent variable is a monthly
change and the identifying assumption is that the monetary shock is orthogonal to confounders
over the whole month. Similar (stronger) assumptions are required when high frequency monetary

shocks are used as external instruments in a VAR—as in Gertler and Karadi (2015)—since the out-
come variables are changes over several months. Additionally, predictability is difﬁcult to establish
convincingly due to data mining and peso problem concerns.
Our paper relates to several strands of the literature in monetary economics. The seminal em-
pirical paper on Fed information is Romer and Romer (2000). Faust, Swanson, and Wright (2004)
present a critique of their ﬁndings. More recently, Campbell et al. (2012) show that an unexpected
tightening leads survey expectations of unemployment to fall. The theoretical literature on the sig-
naling effects of monetary policy is large. Early contributions include Cukierman and Meltzer (1986)
and Ellingsen and Soderstrom (2001).
Recent contributions include Berkelmans (2011), Melosi
(2017), Tang (2015), Frankel and Kartik (2017), and Andrade et al. (2016). The prior literature typi-
cally assumes that the central bank must communicate only through its actions (e.g., changes in the
fed funds rate), whereas we allow the Fed to communicate through its words (FOMC statements).
Our estimates of the effects of monetary announcements on real interest rates using high-frequency
identiﬁcation are related to recent work by Hanson and Stein (2015) and Gertler and Karadi (2015).
We make different identifying assumptions than Hanson and Stein, use a different deﬁnition of
the monetary shock, and come to quite different conclusions about the long-run effects of mone-
tary policy.2 There are also important methodological differences between our work and that of
Gertler and Karadi (2015). They rely on a VAR to estimate the dynamic effects of monetary policy
shocks. They are therefore subject to the usual concern that the VAR they use may not accurately
describe the dynamic response of key variables to a monetary shock. Our identiﬁcation approach is
entirely VAR-free. Our paper is also related to several recent papers that have used high-frequency
identiﬁcation to study the effects of unconventional monetary policy during the recent period over
which short-term nominal interest rates have been at their zero lower bound (Gagnon et al., 2010;
Krishnamurthy and Vissing-Jorgensen, 2011; Wright, 2012; Gilchrist et al., 2015, Rosa, 2012).
The paper proceeds as follows. Section 2 describes the data we use in our analysis. Section
3 presents our empirical results regarding the response nominal and real interest rates and TIPS
break-even inﬂation to monetary policy shocks. Section 4 presents our empirical evidence on output
growth expectations. Section 5 presents our Fed information model, describes our estimation meth-
ods, and presents the results of our estimation of the Fed information model. Section 6 discusses
how to think about the causal effect of the monetary announcement in the face of Fed information.
Section 7 concludes.
2In earlier work, Beechey and Wright (2009) analyze the effect of unexpected movements in the federal funds rate at
the time of FOMC announcements on nominal and real 5-year and 10-year yields and the ﬁve-to-ten year forward over
the period February 2004 to June 2008. Their results are similar to ours for the 5-year and 10-year yields.

Data
To construct our measure of monetary shocks, we use tick-by-tick data on federal funds futures
and eurodollar futures from the CME Group (owner of the Chicago Board of Trade and Chicago
Mercantile Exchange). These data can be used to estimate changes in expectations about the federal
funds rate at different horizons after an FOMC announcement (see Appendix A). The tick-by-tick
data we have for federal funds futures and eurodollar futures is for the sample period 1995-2012.
For the period since 2012 we use data on changes in the prices of the same ﬁve interest rate futures
over the same 30-minute windows around FOMC announcements that Refet Gurkaynak graciously
shared with us.
We obtain the dates and times of FOMC meetings up to 2004 from the appendix to Gurkaynak,
Sack, and Swanson (2005). We obtain the dates of the remaining FOMC meetings from the Federal
ndars.htm. For the latter period, we veriﬁed the exact times of the FOMC announcements using
the ﬁrst news article about the FOMC announcement on Bloomberg. We cross-referenced these dates
and times with data we obtained from Refet Gurkaynak and in a few cases used the time stamp
from his database.
To measure the effects of our monetary shocks on interest rates, we use several daily interest
rate series. To measure movements in Treasuries at horizons of 1 year or more, we use daily data on
zero-coupon nominal Treasury yields and instantaneous forward rates constructed by Gurkaynak,
lreserve.gov/pubs/feds/2006/200628/200628abs.html. We also use the yields on 3M
and 6M Treasury bills. We retrieve these from the Federal Reserve Board’s H.15 data release.
To measure movements in real interest rates, we use zero-coupon yields and instantaneous for-
ward rates constructed by Gurkaynak, Sack, and Wright (2010) using data from the TIPS market.
feds/2008/200805/200805abs.html. TIPS are “inﬂation protected” because the coupon and
principal payments are multiplied by the ratio of the reference CPI on the date of maturity to the
reference CPI on the date of issue.3 The reference CPI for a given month is a moving average of
the CPI two and three months prior to that month, to allow for the fact that the Bureau of Labor
Statistics publishes these data with a lag.
TIPS were ﬁrst issued in 1997 and were initially sold at maturities of 5, 10 and 30 years, but only
3This holds unless cumulative inﬂation is negative, in which case no adjustment is made for the principle payment.

the 10-year bonds have been issued systematically throughout the sample period. Other maturities
have been issued more sporadically. While liquidity in the TIPS market was initially poor, TIPS
now represent a substantial fraction of outstanding Treasury securities. We start our analysis in
2000 to avoid relying on data from the period when TIPS liquidity was limited. For 2- and 3-year
yields and forwards we start our analysis in 2004. Gurkaynak, Sack, and Wright (2010) only report
zero-coupon yields for these maturities from 2004 onward. One reason is that to accurately estimate
zero-coupon yields at this maturity it is necessary to wait until longer maturity TIPS issued several
years earlier have maturities in this range. To facilitate direct comparisons between nominal and
real interest rates, we restrict our sample period for the corresponding 2- and 3-year nominal yields
and forwards to the same time period.
To measure expectations, we use data on expectations of future nominal interest rates, inﬂation
and output growth from the Blue Chip Economic Indicators. Blue Chip carries out a survey during the
ﬁrst few days of every month soliciting forecasts of these variables for up to the next 8 quarters. We
use the mean forecast for each variable. We also use data on Greenbook forecasts from the Philadel-
d.org/research-and-data/real-time-center/greenbook-data/philadelphia-data-
set. We use the real GDP growth variable from this dataset.
To assess the role of risk premia, we use a daily decomposition of nominal and real interest
rate movements into risk-neutral expected future rates and risk premia obtained from Abrahams,
Adrian, Crump, and Moench (2015). To assess the robustness of our results regarding the response
of real interest rates we use daily data on inﬂation swaps from Bloomberg. Finally, we estimate the
response of stock prices to monetary announcements using daily data on the level of the S&P500
stock price index obtained from Yahoo Finance.
3
Response of Interest Rates and Expected Inﬂation
Our goal in this section is to identify the effect of the monetary policy news contained in scheduled
FOMC announcements on nominal and real interest rates of different maturities. Speciﬁcally, we
estimate
∆st = α + γ∆it + ϵt,
(1)
where ∆st is the change in an outcome variable of interest (e.g., the yield on a ﬁve year zero-coupon
Treasury bond), ∆it is a measure of the monetary policy news revealed in the FOMC announcement,

ϵt is an error term, and α and γ are parameters. The parameter of interest is γ, which measures the
effect of the FOMC announcement on ∆st relative to its effect on the policy indicator ∆it.
To identify a pure monetary policy shock, we consider the change in our policy indicator (∆it)
in a 30-minute window around scheduled FOMC announcements.4 The idea is that changes in the
policy indicator in these 30-minute windows are dominated by the information about future mon-
etary policy contained in the FOMC announcement. Under the assumption that this is true, we can
simply estimate equation (1) by ordinary least squares. We also present results for a heteroskedastic-
ity based estimation approach (Rigobon, 2003; Rigobon and Sack, 2004) which is based on a weaker
identifying assumption to verify that our baseline identifying assumption is reasonable. In our
baseline analysis, we focus on only scheduled FOMC announcements, since unscheduled meetings
may occur in reaction to other contemporaneous shocks.
The policy indicator we use is a composite measure of changes in interest rates at different matu-
rities spanning the ﬁrst year of the term structure. Until recently, most authors used unanticipated
changes in the federal funds rate (or closely related changes in very short term interest rates) as
their policy indicator. The key advantage of our measure is that it captures the effects of “forward
guidance.” Forward guidance refers to announcements by the Fed that convey information about
future changes in the federal funds rate. Over the past 15 years, the Federal Reserve has made
greater and greater use of such forward guidance. In fact, changes in the federal funds rate have
often been largely anticipated by markets once they occur. Gurkaynak, Sack, and Swanson (2005)
convincingly argue that unanticipated changes in the federal funds rate capture only a small frac-
tion of the monetary policy news associated with FOMC announcements in recent years (see also,
Campbell et al., 2012).
The speciﬁc composite measure we use as our policy indicator is the ﬁrst principle component of
the unanticipated change over the 30-minute windows discussed above in the following ﬁve interest
rates: the federal funds rate immediately following the FOMC meeting, the expected federal funds
rate immediately following the next FOMC meeting, and expected 3-month eurodollar interest rates
at horizons of two, three and four quarters. We refer to this policy indicator as the “policy news
shock.” We use data on federal funds futures and eurodollar futures to measure changes in market
expectations about future interest rates at the time of FOMC announcements. The scale of the policy
news shock is arbitrary. For convenience, we rescale it such that its effect on the 1-year nominal
Treasury yield is equal to one. Appendix A provides details about the construction of the policy
4Speciﬁcally, we calculate the monetary shock using a 30-minute window from 10 minutes before the FOMC an-
nouncement to 20 minutes after it.

news shock.5
3.1
Baseline Estimates
Table 1 presents our baseline estimates of monetary shocks on nominal and real interest rates and
break-even inﬂation. Each estimate in the table comes from a separate OLS regression of the form
discussed above—equation (1). In each case the independent variable is the policy news shock
measured over a 30-minute window around an FOMC announcement, while the change in the
dependent variable is measured over a one-day window.6
The ﬁrst column of Table 1 presents the effects of the policy news shock on nominal Treasury
yields and forwards. Recall that the policy news shock is scaled such that the effect on the one-year
Treasury yield is 100 basis points. Looking across different maturities, we see that the effect of the
shock is somewhat smaller for shorter maturities, peaks at 110 basis points for the 2-year yield and
then declines monotonically to 38 basis points for the 10-year yield. Since longer-term yields reﬂect
expectations about the average short-term interest rate over the life of the long bond, it is easier
to interpret the time-path of the response of instantaneous forward rates. Abstracting from risk
premia, these reveal market expectations about the short-term interest rate that the market expects
to prevail at certain points in time in the future.7 The impact of our policy news shock on forward
rates is also monotonically declining in maturity from 114 basis points at 2-years to -8 basis points
at 10-years. We show below that the negative effect on the 10-year nominal forward rate reﬂects a
decline in break-even inﬂation at long horizons.8
The second column of Table 1 presents the effects of the policy news shock on real interest rates
measured using TIPS. While the policy news shock affects nominal rates by construction, this is not
the case for real interest rates. In neoclassical models of the economy, the Fed controls the nominal
interest rate but has no impact on real interest rates. In sharp contrast to this, we estimate the impact
of our policy news shock on the 2-year real yield to be 106 basis points, and the impact on the 3-
year real yield to be 102 basis points. Again, the time-path of effects is easier to interpret by viewing
5Our policy news shock variable is closely related to the “path factor” considered by Gurkaynak, Sack, and Swan-
son (2005). The ﬁve interest rate futures that we use to construct our policy news shock are the same ﬁve futures as
Gurkaynak, Sack, and Swanson (2005) use. They motivate the choice of these particular futures by liquidity considera-
tions. They advocate the use of two principle components to characterize the monetary policy news at the time of FOMC
announcements—a “target factor” and a “path factor.” We focus on a single factor for simplicity. See also Barakchian
and Crowe (2013).
6The longer window for the dependent variable adds noise to the regression without biasing the coefﬁcient of interest.
7For example, the effect on the 2-year instantaneous forward rate is the effect on the short-term interest rate that the
market expects to prevail in 2 years time.
8Our ﬁnding that long-term inﬂation expectations decline in response to contractionary monetary policy shock is
consistent with Beechey, Johannsen, and Levin (2011) and G¨urkaynak, Levin, and Swanson (2010).

Table 1: Response of Interest Rates and Inﬂation to the Policy News Shock
Nominal 
Real 
Inflation
3M Treasury Yield
0.67
(0.14)
6M Treasury Yield
0.85
(0.11)
1Y Treasury Yield
1.00
(0.14)
2Y Treasury Yield
1.10
1.06
0.04
(0.33)
(0.24)
(0.18)
3Y Treasury Yield
1.06
1.02
0.04
(0.36)
(0.25)
(0.17)
5Y Treasury Yield
0.73
0.64
0.09
(0.20)
(0.15)
(0.11)
10Y Treasury Yield
0.38
0.44
-0.06
(0.17)
(0.13)
(0.08)
2Y Treasury Inst. Forward Rate
1.14
0.99
0.15
(0.46)
(0.29)
(0.23)
3Y Treasury Inst. Forward Rate
0.82
0.88
-0.06
(0.43)
(0.32)
(0.15)
5Y Treasury Inst. Forward Rate
0.26
0.47
-0.21
(0.19)
(0.17)
(0.08)
10Y Treasury Inst. Forward Rate
-0.08
0.12
-0.20
(0.18)
(0.12)
(0.09)
Each estimate comes from a separate OLS regression. The dependent variable in each regression is
the one day change in the variable stated in the left-most column. The independent variable is a
change in the policy news shock over a 30 minute window around the time of FOMC
announcements. The sample period is all regularly scheduled FOMC meetings from 1/1/2000 to
3/19/2014, except that we drop July 2008 through June 2009. For 2Y and 3Y yields and real
forwards, the sample starts in January 2004. The sample size for the 2Y and 3Y yields and forwards
is 74. The sample size for all other regressions is 106. In all regressions, the policy news shock is
computed from these same 106 observations. Robust standard errors are in parentheses.

estimates for instantaneous forward rates. The effect of the shock on the 2-year real forward rate is
99 basis points. It falls monotonically at longer horizons to 88 basis points at 3 years, 47 basis points
at 5 years, and 12 basis point at 10 years (which is not statistically signiﬁcantly different from zero).
Evidently, monetary policy shocks can affect real interest rates for substantial amounts of time (or
at least markets believe it can). However, in the long-run, the effect of monetary policy shocks on
real interest rates is zero as theory would predict.
The third column of Table 1 presents the effect of the policy news shock on break-even inﬂation
as measured by the difference between nominal Treasury rates and TIPS rates. The ﬁrst several
rows provide estimates based on bond yields, which indicate that the response of break-even inﬂa-
tion is small. The shorter horizon estimates are actually slightly positive but then become negative
at longer horizons. None of these estimates are statistically signiﬁcantly different from zero. Again,
it is helpful to consider instantaneous forward break-even inﬂation rates to get estimates of break-
even inﬂation at points in time in the future. The response of break-even inﬂation implied by the
2 year forwards is slightly positive, though statistically insigniﬁcant. The response is negative at
longer horizons: for maturities of 3, 5 and 10 years, the effect is -6, -21 and -20 basis points, re-
spectively. It is only the responses at 5 and 10 years that are statistically signiﬁcantly different from
zero. Our evidence thus points to break-even inﬂation responding modestly and quite gradually to
monetary shocks that have a substantial effect on real interest rates.
Table 1 presents results for a sample period from January 1st 2000 to March 19th 2014, except
that we drop the period spanning the height of the ﬁnancial crisis in the second half of 2008 and
the ﬁrst half of 2009.9 We choose to drop the height of the ﬁnancial crisis because numerous well-
documented asset pricing anomalies arose during this crisis period, and we wish to avoid the con-
cern that our results are driven by these anomalies. However, similar results obtain for the full
sample including the crisis, as well as a more restrictive data sample ending in 2007, and for a
sample that also includes unscheduled FOMC meetings (see Table A.1). The results for the sample
ending in 2007 show that our results are unaffected by dropping the entire period during which
the zero-lower-bound is binding and the Fed is engaged in quantitative easing. Table A.2 presents
results analogous to those of Table 1 but using the unexpected change in the fed funds rate as the
policy indicator.
Figure 1 presents a binned scatter plot of the relationship between the policy news shock and the
5-year real yield (the average expected response of the short-term real interest rates over the next 5
9The sample period for 2- and 3-year yields and forwards is somewhat shorter (it starts in 2004) because of data
limitations (see section 2 for details).

Figure 1: Binned Scatter Plot for 5-Year Real-Yield Regression
‐0.20
‐0.15
‐0.10
‐0.05
0.00
0.05
0.10
0.15
‐0.12
‐0.08
‐0.04
0.00
0.04
0.08
0.12
Policy News Shock
years). The variation in the policy new shock ranges from -11 basis points to +10 basis points. The
relationship between the change in the 5-year real yield and the policy news shock does not seem
to be driven by a few outliers.
3.2
Background Noise in Interest Rates
A concern regarding the estimation approach we describe above is that other non-monetary news
might affect our monetary policy indicator during the window we consider around FOMC an-
nouncements. If this is the case, it will contaminate our measure of monetary shocks. This concern
looms much larger if one considers longer event windows than our baseline 30-minute window.
It has been common in the literature on high frequency identiﬁcation of monetary policy to con-
sider a one- or two-day window around FOMC announcements (e.g., Kuttner, 2001; Cochrane and
Piazzesi, 2002; Hanson and Stein, 2015). In these cases, the identifying assumption being made is
that no other shocks affect the policy indicator in question during these one or two days. Espe-
cially when the policy indicator is based on interest rates several quarters or years into the term
structure—as has recently become common to capture the effects of forward guidance—the as-
sumption that no other shocks affect this indicator over one or two days is a strong assumption.
Interest rates at these maturities ﬂuctuate substantially on non-FOMC days, suggesting that other

shocks than FOMC announcements affect these interest rates on FOMC days. There is no way of
knowing whether these other shocks are monetary shocks or non-monetary shocks.
To assess the severity of this problem, Table 2 compares estimates of equation (1) based on OLS
regressions to estimates based on a heteroskedasticity-based estimation approach developed by
Rigobon (2003) and Rigobon and Sack (2004). We do this both for a 30-minute window and for a 1-
day window. The heteroskedasticity-based estimator is described in detail in Appendix B. It allows
for “background” noise in interest rates arising from other shocks during the event windows be-
ing considered. The idea is to compare movements in interest rates during event windows around
FOMC announcements to other equally long and otherwise similar event windows that do not con-
tain an FOMC announcement. The identifying assumption is that the variance of monetary shocks
increases at the time of FOMC announcements, while the variance of other shocks (the background
noise) is unchanged.
The top panel of Table 2 compares estimates based on OLS to those based on the heteroskedasticity-
based estimator (Rigobon estimator) for a subset of the assets we consider in Table 1 when the event
window is 30-minutes as in our baseline analysis. The difference between the two estimators is very
small, both for the point estimates and the conﬁdence intervals.10 This result indicates that there
is in fact very little background noise in interest rates over a 30-minute window around FOMC
announcements and the OLS identifying assumption—that only monetary shocks occur within the
30-minute window—thus yields a point estimate and conﬁdence intervals that are close to correct.
Table A.3 presents a full set of results based on the Rigobon estimator and a 30-minute window. It
conﬁrms that OLS yields very similar results to the Rigobon estimator for all the assets we consider
when the event window is 30 minutes.
In contrast, the problem of background noise is quite important when the event window being
used to construct our policy news shocks is one day. The second panel of Table 2 compares esti-
mates based on OLS to those based on the Rigobon estimator for policy news shocks constructed
using a one-day window. In this case, the differences between the OLS and Rigobon estimates are
substantial. The point estimates in some cases differ by dozens of basis points and have different
signs in three of the six cases considered. However, the most striking difference arises for the con-
ﬁdence intervals. OLS yields much narrower conﬁdence intervals than those generated using the
10The conﬁdence intervals for the Rigobon estimator in Table 2 are constructed using a procedure that is robust to
inference problems that arise when the amount of background noise is large enough that there is a signiﬁcant probability
that the difference in the variance of the policy indicator between the sample of FOMC announcements and the “con-
trol” sample is close to zero. In this case, the conventional bootstrap approach to constructing conﬁdence intervals will
yield inaccurate results. Appendix C describes the method we use to construct conﬁdence intervals in detail. We thank
Sophocles Mavroeidis for suggesting this approach to us.

Table 2: Allowing for Background Noise in Interest Rates
Nominal 
Real 
Nominal 
Real 
Nominal 
Real 
Policy News Shock, 30-Minute Window:
1.14
0.99
0.26
0.47
-0.08
0.12
[0.23, 2.04]
[0.41, 1.57]
[-0.12, 0.64]
[0.14, 0.80]
[-0.43, 0.28]
[-0.12, 0.36]
1.10
0.96
0.22
0.46
-0.12
0.11
[0.31, 2.36]
[0.45, 1.82]
[-0.14, 0.64]
[0.15, 0.84]
[-0.46, 0.24]
[-0.13, 0.35]
Policy News Shock, 1-Day Window:
1.24
1.00
0.44
0.48
0.05
0.15
[0.80, 1.69]
[0.57, 1.43]
[0.18, 0.70]
[0.20, 0.76]
[-0.20, 0.29]
[-0.10, 0.39]
0.93
0.82
-0.11
0.33
-0.51
-0.04
[-0.64, 2.08]
[0.38, 3.20]
[-1.23, 0.33]
[-0.07, 1.12]
[-1.93, -0.08]
[-0.51, 0.45]
2-Year Nominal Yield, 1-Day Window
1.23
0.94
0.64
0.54
0.18
0.20
[1.07, 1.38]
[0.69, 1.20]
[0.43, 0.84]
[0.31, 0.76]
[0.01, 0.35]
[0.02, 0.38]
1.14
0.82
-0.11
0.33
-0.51
-0.04
[0.82, 1.82]
[0.62, 2.98]
[-7.94, 0.60]
[-0.01, 7.48]
[-10.00, -0.21]
[-4.57, 0.38]
2-Year Forward
5-Year Forward
10-Year Forward
Rigobon (90% CI)
OLS
Rigobon
OLS
Rigobon
OLS
Each estimate comes from a separate "regression." The dependent variable in each regression is the one day change in the variable
stated at the top of that column. The independent variable in the first panel of results is the 30-minute change in the policy news
shock around FOMC meeting times, in the second panel it is the 1-day change in the policy news shock, and in the third panel it is
the 1-day change in the 2-Year nominal yield. In each panel, we report results based on OLS and Rigobon's heteroskedasticity
based estimation approach. We report a point estimate and 95% confidence intervals except in the last row of Rigobon estimates
which reports 90% confidence intervals. The sample of "treatment" days for the Rigobon method is all regularly scheduled FOMC
meeting days from 1/1/2000 to 3/19/2014—this is also the period for which the policy news shock is constructed in all
“regressions.” The sample of "control" days for the Rigobon analysis is all Tuesdays and Wednesdays that are not FOMC meeting
days over the same period of time. In both the treatment and control samples, we drop July 2008 through June 2009 and 9/11/2001-
9/21/2001. For 2Y forwards, the sample starts in January 2004. Confidence intervals for the OLS results are based on robust
standard errors. Confidence intervals for the Rigobon method are calculated using the weak-IV robust approach discussed in the
appendix with 5000 iterations. 
Rigobon method. According to OLS, the effects on the 5-year nominal and real forwards are highly
statistically signiﬁcant, while the Rigobon estimator indicates that these effects are far from being
signiﬁcant.
This difference between OLS and the Rigobon estimator indicates that there is a large amount
of background noise in the interest rates used to construct the policy news shock over a one day
window. The Rigobon estimator is ﬁltering this background noise out. The fact that the conﬁdence
intervals for the Rigobon estimator are so wide in the 1-day window case implies that there is very
little signal left in this case. The OLS estimator, in contrast, uses all the variation in interest rates
(both the true signal from the announcement and the background noise). Clearly, this approach

massively overstates the true statistical precision of the effect arising from the FOMC announcement
when a 1-day window is used.
The difference between OLS and the Rigobon estimator is even larger when a longer-term inter-
est rate is used as the policy indicator that proxies for the size of monetary shocks. The third panel
of Table 2 compares results based on OLS to those based on the Rigobon estimator when the policy
indicator is the change in the two-year nominal yield over a one day window. Again, the conﬁ-
dence intervals are much wider using the Rigobon estimator than OLS. In fact, here we report 90%
conﬁdence intervals for the Rigobon estimator since the 95% conﬁdence intervals are in some cases
inﬁnite (i.e., we were unable to ﬁnd any value of the parameter of interest that could be rejected at
that signiﬁcance level).
An important substantive difference arises between the OLS and Rigobon estimates in the case
of the 10-year real forward rate when the 2-year nominal yield is used as the policy indicator. Here,
OLS estimation yields a statistically signiﬁcant effect of the monetary shock on forward rates at even
a 10-year horizon. This result is emphasized by Hanson and Stein (2015). However, the Rigobon
estimator with appropriately constructed conﬁdence intervals reveals that this result is statistically
insigniﬁcant. Our baseline estimation approach using a 30-minute window and the policy news
shock as the proxy for monetary shocks yields a point estimate that is small and statistically in-
signiﬁcant.11
3.3
Risk Premia or Expected Future Short-Term Rates?
One question that arises when interpreting our results is to what extent the movements in long-
term interest rates we identify reﬂect movements in risk premia as opposed to changes in expected
future short-term interest rates. A large literature suggests that changes in risk premia do play an
important role in driving movements in long-term interest rates in general. Yet, for our analysis,
the key question is not whether risk premia matter in general, but rather how important they are in
explaining the abrupt changes in interest rates that occur in the narrow windows around the FOMC
11Hanson and Stein (2015) also present an estimator based on instrumenting the 2-day change in the 2-year rate with
the change in the two-year rate during a 60-minute window around the FOMC announcement. This yields similar results
to their baseline. Since this procedure is not subject to the concerns raised above, it suggests that there are other sources of
difference between our results and those of Hanson and Stein than econometric issues. One possible source of difference
is that we use different monetary shock indicators. Their policy indicator (the change in the 2-year yield) is further out
in the term structure and may be more sensitive to risk premia. As we discuss in section 3.3, our measure of monetary
shocks is uncorrelated with the risk premia implied by the afﬁne term structure model of Abrahams et al. (2015), whereas
Hanson and Stein’s monetary shocks are associated with substantial movements in risk premia. The difference could also
arise from the fact that Hanson and Stein focus on a 2-day change in long-term real forwards; which could yield different
results if the response of long-term bonds to monetary shocks is inertial.

announcements that we focus on.12
In Appendix D, we present three sets of results that indicate that risk premium effects are not
driving our empirical results. First, the impact of our policy news shock on direct measures of
expectations from the Blue Chip Economic Indicators indicate that our monetary shocks have large
effects on expected short-term nominal and real rates. Second, the impact of our policy news shock
on risk-neutral expected short rates from the state-of-the-art afﬁne term structure model of Abra-
hams et al. (2015) are similar to our baseline results. Third, the impact of our policy news shock
on interest rates over longer event windows do not suggest that the effects we estimate dissipate
quickly (although the standard errors in this analysis are large).
We also consider an alternative, market-based measure of inﬂation expectations based on inﬂa-
tion swap data.13 The sample period for this analysis is limited by the availability of swaps data
to begin on January 1st 2005. Unfortunately, due to the short sample available to us, the results are
extremely noisy, and are therefore not particularly informative. As in our baseline analysis, there
is no evidence of large negative responses in inﬂation to our policy news shock (as would arise
in a model with ﬂexible prices). Indeed the estimates from this approach (which are compared to
our baseline results in Table A.4) suggest a somewhat larger “price puzzle”—i.e., positive inﬂation
response—at shorter horizons, though this is statistically insigniﬁcant.
4
The Fed Information Effect
The results in section 3 show that variation in nominal interest rates caused by monetary policy an-
nouncements have large and persistent effects on real interest rates. The conventional interpretation
of these facts is that they imply that prices must respond quite sluggishly to shocks. We illustrate
this in a conventional business cycle model in Appendix E. This conventional view of monetary
shocks has the following additional prediction that we can test using survey data: A surprise in-
crease in interest rates should cause expected output to fall. To test this prediction, we run our
baseline empirical speciﬁcation—equation (1)—at a monthly frequency with the monthly change in
12Piazzesi and Swanson (2008) show that federal funds futures have excess returns over the federal funds rate and
that these excess returns vary counter-cyclically at business cycle frequencies. However, they argue that high frequency
changes in federal funds futures are likely to be valid measures of changes in expectations about future federal funds
rates since they difference out risk premia that vary primarily at lower frequencies.
13An inﬂation swap is a ﬁnancial instrument designed to help investors hedge inﬂation risk. As is standard for
swaps, nothing is exchanged when an inﬂation swap is ﬁrst executed. However, at the maturity date of the swap, the
counterparties exchange Rx
t −Πt, where Rx
t is the x-year inﬂation swap rate and Πt is the reference inﬂation over that
period. If agents were risk neutral, therefore, Rt would be expected inﬂation over the x year period. See Fleckenstein,
Longstaff, and Lustig (2014) for an analysis of the differences between break-even inﬂation from TIPS and inﬂation swaps.

Table 3: Response of Expected Output Growth Over the Next Year
1995-2014
2000-2014
2000-2007
1995-2000
Policy News Shock
1.01
1.04
0.95
0.79
(0.32)
(0.35)
(0.32)
(0.63)
Observations
120
90
52
30
We regress changes from one month to the next in survey expectations about output growth over the next year from the Blue
Chip Economic Indicators on the policy news shock that occurs in that month (except that we drop policy news shocks that
occur in the first week of the month since we do not know whether these occurred before or after the survey response).
Specifically, the dependent variable is the change in the average forecasted value of output growth over the next three quarters
(the maximum horizon over which forecasts are available for the full sample). See Appendix F for details. We present results
for four sample periods. The longest sample period we have data for is 1995m1-2014m4; this is also the period for which the
policy news shocks is constructed. We also present results for 2000m1-2014m4 (which corresponds to the sample period used
in Table 1), 2000m1-2007m12 (a pre-crisis sample period), and 1995m1-1999m12. As in our other analysis, we drop data
from July 2008 through June 2009. Robust standard errors are in parentheses.
Blue Chip survey expectations about output growth as the dependent variable and the policy news
shock that occurs in that month as the independent variable.14
Table 3 reports the resulting estimates. The dependent variable is the monthly change in ex-
pected output growth over the next year (see Appendix F for details). In sharp contrast to the
conventional theory of monetary shocks, policy news shocks that raise interest rates lead expecta-
tions about output growth to rise rather than fall.15 We present results for four sample periods. The
longest sample period for which we are able to construct our policy new shock is 1995-2014. We also
present results for the sample period 2000-2014, which corresponds to the sample period we use in
most of our other analysis. For robustness, we also present results for two shorter sampler periods
(1995-2000 and 2000-2007). The results are similar across all four sample periods, but of course less
precisely estimated for the shorter sampler periods.
Figure 2 presents a binned scatter plot of the relationship between changes expected output
growth and our policy news shock over the 1995-2014 sample period. This scatter plot shows that
the results in Table 3 are not driven by outliers. Finally, Table A.5 presents the response of output
growth expectations separately for each quarter that the Blue Chip survey asks about. These are
noisier but paint the same picture as the results in Table 3.
A natural interpretation of this evidence is that FOMC announcements lead the private sector to
update its beliefs not only about the future path of monetary policy, but also about other economic
14We exclude policy news shocks that occur in the ﬁrst week of the month because in those cases we do not know
whether they occurred before or after the survey response.
15Campbell et al. (2012) present similar evidence regarding the effect of surprise monetary shocks on Blue Chip
expectations about unemployment.

Figure 2: Binned Scatter Plot for Expected Output Growth Regression
‐0.25
‐0.20
‐0.15
‐0.10
‐0.05
0.00
0.05
0.10
0.15
0.20
‐0.10
‐0.06
‐0.02
0.02
0.06
0.10
Policy News Shock
fundamentals. For example, when an FOMC announcement signals higher interest rates than mar-
kets had been expecting, market participants may view this as implying that the FOMC is more
optimistic about economic fundamentals going forward than they had thought, which in turn may
lead the market participants themselves to update their own beliefs about the state of the economy.
We refer to effects of FOMC announcements on private sector views of non-monetary economic
fundamentals as “Fed information effects.”
The idea that the Fed can have such information effects relies on the notion that the FOMC has
some knowledge regarding the economy that the private sector doesn’t have or has formulated a
viewpoint about the economy that the private sector ﬁnds valuable. Is it reasonable to suppose that
this is the case? In terms of actual data, the FOMC has access to the same information as the private
sector with minor exceptions.16 However, the Fed does employ a legion of talented, well-trained
economists whose primary role is to process and interpret all the information being released about
the economy. This may imply that the FOMC’s view about how the economy will evolve contains a
perspective that affects the views of private agents. This is the view Romer and Romer (2000) argue
16The FOMC may have some advance knowledge of industrial production data since the Federal Reserve produces
these data. It also collects anecdotal information on current economic conditions from reports submitted by bank direc-
tors and through interviews with business contacts, economists, and market experts. This information is subsequently
published in reports commonly known as the Beige Book.

for in their classic paper on Federal Reserve information.17
The idea that the Fed can inﬂuence private sector beliefs through its analysis of public data is
somewhat unconventional in macroeconomics. However, the ﬁnance literature on analyst effects
suggests this is not implausible. This literature ﬁnds that the most inﬂuential analyst announce-
ments can have quite large effects on the stock market (see, e.g. Loh and Stulz, 2011). Loh and Stulz
note: “Kenneth Bruce from Merrill Lynch issued a recommendation downgrade on Countrywide
Financial on August 15, 2007, questioning the giant mortgage lenders ability to cope with a worsen-
ing credit crunch. The report sparked a sell-off in Countrywides shares, which fell 13% on that day.”
If Kenneth Bruce can affect the market’s views about Countrywide, perhaps it is not unreasonable
to believe that the Fed can affect the market’s views about where the economy is headed.
If Fed information is important, one might expect that contractionary monetary shocks would
disproportionately occur when the Fed is more optimistic than the private sector about the state of
the economy. In Appendix G, we test this proposition using the Fed’s Greenbook forecast about
output growth as a measure of its optimism about the economy.18 We ﬁnd that, indeed, our policy
news shocks tend to be positive (i.e., indicate a surprise increase in interest rates) when the Green-
book forecast about current and future real GDP growth is higher than the corresponding Blue
Chip forecast (panel A of Table G.1). We furthermore ﬁnd that the difference between Greenbook
and Blue Chip forecasts tends to narrow after our policy news shocks occur (panel B of Table G.1).
This suggests that private sector forecasters may update their forecasts based on information they
gleam from FOMC announcements.
5
Characterizing Monetary Non-Neutrality with Fed Information
The evidence we present in section 4 calls for more sophisticated modeling of the effects of monetary
announcements than is standard in the literature. Rather than affecting beliefs only about current
and future monetary policy, FOMC announcements must also affect private sector beliefs about
other economic fundamentals.
An important consequence of this is that our evidence does not necessarily point to nominal
and real rigidities being large. It may be that the responses of real interest rates that we estimate
17This does not necessarily imply that the Fed should be able to forecast the future evolution of the economy better
than the private sector. The private sector, of course, also processes and interprets the information released about the
economy. It may therefore also be able to formulate a view about the economy that the Fed ﬁnds valuable. In other
words, information can ﬂow both ways with neither the Fed nor the private sector having a clear advantage.
18The Greenbook forecast is an internal forecast produced by the staff of the Board of Governors and presented at each
FOMC meeting. Greenbook forecasts are made public with a ﬁve year lag.

in response to FOMC announcements mostly reﬂect changes in private sector expectations about
the natural rate of interest. If this is the case, the fact that we ﬁnd that our shocks have little effect
on inﬂationary expectations may be consistent with small nominal and real rigidities, since the
tightening of policy relative to the natural rate is small.19
But even if this is true—that the responses of real interest rates that we estimate mostly reﬂect
changes in private sector expectations about the natural rate of interest—this does not imply that
the Fed is powerless. Quite to the contrary, in this case, the Fed has enormous power over beliefs
about economic fundamentals, which may in turn have large effects on economic activity.
Our evidence on the response of real interest rates and expected inﬂation to a monetary an-
nouncement, therefore, implies that either 1) nominal and real rigidities are large, or 2) the Fed
can affect private sector beliefs about future non-monetary fundamentals by large amounts. In
other words, it implies that the Fed is powerful, either through the conventional channel or a non-
conventional channel (or some combination).
To make these arguments precise, we now present a New Keynesian model of the economy
augmented with Fed information effects. We then estimate this model to match the responses of
interest rates, expected inﬂation, and expected output growth to FOMC announcements calculated
above. Finally, we use the estimated model to assess the degree of monetary non-neutrality implied
by our evidence and to assess how much of this monetary non-neutrality arises from traditional
channels versus information effects.
5.1
A New Model with Fed Information Effects
Most earlier theoretical work on the signaling effect of monetary policy has made the very restrictive
assumption that the Fed can only signal through its actions. The focus of much of this literature has
been on the limitations of what the Fed can signal with its actions. The recent empirical literature
on monetary policy has, however, convincingly demonstrated that the Fed also signals through its
statements (Gurkaynak, Sack, and Swanson, 2005). This implies that the Fed’s signals can be much
richer; they can incorporate forward guidance, and they can distinguish between different types of
shocks. With a much richer signal structure, the key question becomes: What information would
the Fed like to convey?
We model FOMC announcements as affecting private sector beliefs about the path of the “natu-
ral rate of interest,” the real interest rate that would prevail absent pricing frictions. This is a natural
19This idea is explained in more detail below and in Appendix E.

choice since tracking the natural rate is optimal in the model we consider absent information effects.
If the Fed’s goal is to track the natural rate of interest, it seems natural that announcements by the
Fed about its current and future actions provide information about the future path of the natural
rate of interest.
Apart from including a Fed information effect, the model we use differs in two ways from the
textbook New Keynesian model: households have internal habits, and we allow for a backward-
looking term in the Phillips curve. These two features allow the model to better ﬁt the shapes of
the impulse responses we have estimated in the data. Detailed derivations of household and ﬁrm
behavior in this model are presented in Appendix H. There, we show that private sector behavior
in this model can be described by a log-linearized consumption Euler equation and Phillips curve
that take the following form:
ˆλxt = Etˆλxt+1 + (ˆıt −Etˆπt+1 −ˆrn
t ),
(2)
∆ˆπt = βEt∆ˆπt+1 + κω˜ζˆxt −κ˜ζˆλxt.
(3)
Hatted variables denote percentage deviations from steady state. ∆ˆπt = ˆπt −ˆπt−1. The variable
ˆλxt = ˆλt −ˆλn
t denotes the marginal utility gap (the difference between actual marginal utility of
consumption ˆλt and the “natural” level of marginal utility ˆλn
t that would prevail if prices were
ﬂexible), ˆx = ˆyt −ˆyn
t denotes the “output gap”, ˆπt denotes inﬂation, ˆıt denotes the gross return
on a one-period, risk-free, nominal bond, and ˆrn
t denotes the “natural rate of interest,” which is a
function of exogenous shocks to technology. The parameter β denotes the subjective discount factor
of households, while κ, ω, and ˜ζ are composite parameters that determine the degree of nominal
and real rigidities in the economy. With internal habits, the marginal utility gap is
ˆλxt = −(1 + b2β)σcˆxt + bσcˆxt−1 + bβσcEtˆxt+1,
(4)
where b governs the strength of habits and σc = −σ−1/((1−b)(1−bβ)), where σ is the intertemporal
elasticity of substitution.
We assume that the monetary authority sets interest rates according to the following simple rule:
ˆıt −Etˆπt+1 = ¯rt + φπˆπt,
(5)

with ¯rt following an AR(2) process
¯rt = (ρ1 + ρ2)¯rt−1 −ρ1ρ2¯rt−2 + ϵt,
(6)
where ρ1 and ρ2 are the roots of the lag polynomial for ¯rt and ϵt is the innovation to the ¯rt process.
Here ϵt is the monetary shock. Notice that it can potentially have a long-lasting effect on real interest
rates through the AR(2) process for ¯rt. We choose this speciﬁcation to be able to match the effects of
the monetary shocks we estimate in the data. The shocks we estimate in the data have a relatively
small effect on contemporaneous interest rates but a much larger effect on future interest rates (see
Table 1)—i.e., they are mostly but not exclusively forward guidance shocks. The AR(2) speciﬁcation
for ¯rt can capture this if ρ1 and ρ2 are both large and positive leading to a pronounced hump-shape
in the impulse response of ¯rt (and therefore a pronounced hump-shape across the term structure in
the contemporaneous response of longer-term interest rates as in Table 1).20
As we discuss above, the way in which we model the Fed information effect is by assuming
that FOMC announcements may affect the private sector’s beliefs about the path of the natural rate
of interest. The simplest way to do this is to assume that private sector beliefs about the path of
the natural rate of interest shifts by some fraction ψ of the change in ¯rt. Formally, in response to a
monetary announcement
Etˆrn
t+j = ψEt¯rt+j.
(7)
Moreover, we assume that the shock to expectations about the current value of the natural rate of
output is proportional to the shock to expectations about the current monetary policy with the same
factor of proportionality, i.e., Etˆyn
t = ψEt¯rt.21
Here the parameter ψ governs the extent to which monetary announcements have information
effects versus traditional effects. A fraction ψ of the shock shows up as an information effect, while
a fraction 1−ψ shows up as a traditional gap between the path for real interest rates and the (private
sector’s beliefs about) the path for the natural rate of interest.22
20How should the monetary shocks ϵt be interpreted? A natural interpretation is the following: The Fed seeks to
target the natural rate of interest. When the Fed makes an announcement, it seeks to communicate changes in its beliefs
about the path of the natural rate to the public. The changes in beliefs sometimes surprise the public and therefore lead
to a shock.
21Here we assume that the FOMC meeting occurs at the beginning of the period, before the value of ˆyn
t is revealed
to the agents. In reality, uncertainty persists about output in period t until well after period t, due to heterogeneous
information. We abstract from this.
22This way of modeling the information effect has the crucial advantage that it is simple and parsimonious enough to
allow us to account for the effects of FOMC announcements on the entire path of future interest rate expectations—i.e.,
the role of forward guidance. This is a distinguishing feature versus previous work. Ellingsen and Soderstrom (2001)
present a model in which the signaling effect derives from announcements about the current interest rate.

5.2
Estimation Method
We estimate four key parameters of the model using simulated method of moments. The four
parameters we estimate are the two autoregressive roots of the shock process (ρ1 and ρ2), the infor-
mation parameter (ψ) and the “slope of the Phillips curve” (κˆζ). We ﬁx the remaining parameters
at the following values: We choose a conventional value of β = 0.99 for the subjective discount
factor. Our baseline value for the intertemporal elasticity of substitution is σ = 0.5, but we explore
robustness to this choice. We ﬁx the Taylor rule parameter to φπ = 0.01. This is roughly equivalent
to a value of 1.01 for the more conventional Taylor rule speciﬁcation without the Etˆπt+1 term on the
left-hand-side of equation (5). We choose this value to ensure that the model has a unique bounded
equilibrium but at the same time limit the amount of endogenous feedback from the policy rule.
This helps ensure that the response of the real interest rate dies out within 10 years as we estimate
in the data.23 We set the elasticity of marginal cost with respect to own output to ω = 2. This value
results from a Frisch labor supply elasticity of one and a labor share of 2/3. Finally, we set the habit
parameter to b = 0.9, a value very close to the one estimated by Schmitt-Groh´e and Uribe (2012).
To ease the computational burden of the simulated method of moments estimation we use a
two stage iterative procedure. In the ﬁrst stage, we estimate the two autoregressive roots of the
monetary shock process (ρ1 and ρ2) to ﬁt the hump-shaped response of real interest rates to our
policy news shock. We do this for ﬁxed values of the information parameter and the slope of the
Phillips curve. The moments we use in this step are the responses of 2, 3, 5, and 10 year real yields
and forwards reported in Table 1. In the second step, we estimate the information parameter (ψ) and
the slope of the Phillips curve (κˆζ) for ﬁxed values of the two autoregressive roots. The moments
we use in this step are the responses of 2, 3, 5, and 10 year break-even inﬂation (both yields and
forwards) reported in Table 1 as well as the responses of output growth expectations reported in
Table A.5. We then iterate back and forth between these steps until convergence.
In both steps, we use a loss function that is quadratic in the difference between the moments
discussed above and their theoretical counterparts in the model.24 We use a weighting matrix with
the inverse standard deviations of the moments on the diagonal, and with the off-diagonal values
set to zero. We use a bootstrap procedure to estimate standard errors. Our bootstrap procedure is
23Recent work has shown that standard New Keynesian models such as the one we are using are very sensitive
to interest rate movements in the far future (Carlstrom, Fuerst, and Paustian, 2015; McKay, Nakamura, and Steinsson,
2016).
24The theoretical counterparts are the responses of the corresponding variable to a monetary shock in the model. Since
the magnitude of the shock in our simulations is arbitrary, we make sure to rescale all responses from the model in such a
way that the 3Y real forward rate is perfectly matched. We use the methods and computer code described in Sims (2001)
to calculate the equilibrium of our model.

to re-sample the data with replacement, estimate the empirical moments on the re-sampled data,
and then estimate the structural parameters as described above using a loss function based on the
estimated empirical moments for the re-sampled data.25 We repeat this procedure 1000 times and
report the 2.5% and 97.5% quantiles of the statistics of interest. Importantly, this procedure for con-
structing the conﬁdence intervals captures the statistical uncertainty associated with our empirical
estimates in Tables 1 and A.5.
5.3
Results and Intuition
Our primary interest is to assess the extent to which FOMC announcements contain Fed informa-
tion and how this affects inference about other key aspects of the economy such as the slope of
the Phillips curve. Table 4 presents our parameter estimates, while Figures 3-5 illustrate the ﬁt of
the model. As in the data, the estimated model generates a persistent, hump-shaped response of
nominal and real interest rates with a small and delayed effect on expected inﬂation (see Figure 3).
To generate this type of response, we estimate that both of the autoregressive roots of the monetary
shock process are large and positive, and we estimate a small slope of the Phillips curve.
We also estimate that the monetary shock leads to a pronounced increase in expectations about
output growth as in the data (see Figure 4). The model can match the increase in expected growth
following a surprise increase in interest rates by estimating a large information effect. We estimate
that roughly 2/3 of the monetary shock is a shock to beliefs about future natural rates of interest
(see Figure 5).
As Figure 4 illustrates, our monetary shock simultaneously leads to an increase in expectations
about output growth and a decrease in output relative to the natural rate of output (i.e., a decrease
in the output gap). This is a consequence of the fact that the information effect is large but still
substantially smaller than the overall increase in interest rates. Output growth expectations rise
because the monetary shock is interpreted as good news about fundamentals. But since the Fed
increases interest rates by more than the private sector believes the natural rate of interest rose,
private sector expectations about the output gap fall.
Despite estimating a large information effect, we estimate a very ﬂat Phillips curve. This is
consistent with prior empirical work. Mavroeidis, Plagborg-Moller, and Stock (2014) survey the
25The re-sampling procedure is stratiﬁed since the empirical moments are estimated from different dataset and dif-
ferent sample periods. The stratiﬁcation makes sure that each re-sampled dataset is consistent with the original dataset
along the following dimensions: The number of observations for the yields and forwards before and after 2004 is the same
as in the original dataset (since the sample period for the 2Y and 3Y yields and forwards starts in 2004). The number of
Blue Chip observations that do not report 4- to 7-quarters ahead expected GDP growth are the same as in the original
dataset, since Blue Chip only asks forecasters to forecast the current and next calendar year.

Table 4: Estimates of Structural Parameters

x


Baseline
0.68
11.2
0.9
0.79
[0.33, 0.84]
[0.0, 60.2]
[0.83, 0.96]
[-0.69, 0.89]
No Information
0.00
3.4
0.9
0.79
 (= 0) 
--
[0.0, 24.1]
[0.83, 0.96]
[-0.69, 0.89]
Full Information
0.99
563
0.9
0.79
 (= 0.99) 
--
[0, 12538]
[0.82, 0.96]
[-0.67, 0.89]
Lower IES
0.67
13.7
0.9
0.79
( = 0.25)
[0.25, 0.89]
[0.0, 94.6]
[0.83, 0.96]
[-0.69, 0.89]
Higher IES
0.68
8.2
0.9
0.79
( = 1)
[0.42, 0.81]
[0.0, 44.0]
[0.83, 0.96]
[-0.69, 0.89]
No Habits
1
1000
0.9
0.79
(b = 0)
[0.92, 1.00]
[0, 43236]
[0.83, 0.96]
[-0.69, 0.89]
The table reports our estimates of the structural parameters of the model that we estimate. We report 95%
confidence intervals in square brackets below the point estimate for each parameter. These are based on the
bootstrap procedure described in the text. In the No Information case and the Full Information case, the slope
of the Phillips curve is estimated only off of inflation moments. In the other cases, the slope of the Phillips
curve and the information parameter are estimated off of both inflation and GDP growth moments.
Figure 3: Responses of Nominal and Real Rates and Inﬂation to a Contractionary Shock
‐0.2
‐0.1
0.0
0.1
0.2
0.3
0.4
0.5
0.6
0.7
0
4
8
12
16
20
24
28
32
36
40
Quarters
Real Interest Rate
Nominal Interest Rate
Inflation

Figure 4: Responses of Expected Output Growth and Output Gap to a Contractionary Shock
‐0.8
‐0.6
‐0.4
‐0.2
Quarters
Output Growth
Output Gap
Figure 5: Decomposition of Real Rate in Interest Rate Gap and Natural Interest Rate
Quarters
Natural Interest Rate
Real Interest Rate

literature that has estimated Phillips curves and, using a common data set, run a huge number of a
priori reasonable speciﬁcations which span different choices made in this literature. They ﬁnd that
the estimated values of the slope of the Phillips curve varies substantially across speciﬁcations and
are symmetrically dispersed around a value of zero. One reason why our estimated Phillips curve
is very ﬂat is that the shocks that we estimate are substantially more persistent than most other
identiﬁed monetary policy shocks (e.g., Christiano, Eichenbaum, and Evans, 2005). This means
that our shocks imply forward guidance about interest rates quite far in the future. It has recently
been shown that standard New Keynesian models implies that far future forward guidance has
large effects on current outcomes (Carlstrom, Fuerst, and Paustian, 2015; McKay, Nakamura, and
Steinsson, 2016).
To illustrate how allowing for the information effect affects our estimates, we reestimate the
model setting the information effect to zero. In this case, we remove the expected output growth
moments from the objective function of the estimation since these moments are impossible to match
without an information effect. The second row in Table 4 presents the estimates for this case. We
see that ignoring the information effect yields a substantially ﬂatter Phillips curve—implying a
substantial overestimate of nominal and real rigidities—relative to our baseline estimation. We also
report a case where the information effect is set to a value close to one. In this case, the slope of the
Phillips curve is estimated to be much steeper than in our baseline case.
Clearly, the information effect has an important effect on inference about the slope of the Phillips
curve. This arises because the effect of the monetary shock on the interest rate gap—the gap be-
tween the interest rate and the natural rate of interest—is much smaller when the information effect
is estimated to be large than it is when the information effect is estimated to be small. It is the
response of the interest rate gap as opposed to the response of the real interest rate itself that deter-
mines the response of inﬂation (see equation (19) in Appendix E). The intuition is that, when the
Fed raises rates, people perceive this as good news about economic fundamentals, and this counters
the conventional channel of monetary policy whereby an interest rate hike lowers output.
Table 4 also reports alternative estimates where we vary the value of the intertemporal elasticity
of substitution (IES) and the habit formation parameter. Varying the IES does not affect our esti-
mates much. This may seem surprising. A smaller value of the IES implies that larger movements
in the natural rate of interest are needed to match the movements in expected growth rates observed
in the data. This would suggest that a lower value of the IES would yield a larger value of the infor-
mation effect. However, in our model with substantial habit formation the IES and the information
parameters also affect the shape of the response of output growth. These effects imply that similar

Figure 6: Response of Actual and Natural Expected Output
‐1.0
0.0
1.0
2.0
3.0
4.0
5.0
0
4
8
12
16
20
24
28
32
36
40
Quarters
Output
Natural Output
Output Gap
values of the information parameter are estimated for a wide range of values of the IES. In contrast,
when we set the habit parameter to zero, we estimate that the entire change in interest rates is an
information effect. As a consequence, we also estimate a much steeper Phillips curve. However, the
ﬁt of the model to the output growth moments is much worse without habit formation.
6
The Causal Effect of Monetary Shocks
The large information effect we estimate in section 5 fundamentally changes how we should inter-
pret the response of output and inﬂation to monetary policy announcements. Figure 6 plots the
response of private sector beliefs about output, the natural rate of output, and the output gap to
a monetary shock that increases interest rates in our estimated model from section 5. The ﬁgure
shows that this surprise monetary tightening leads to a large and permanent increase in expected
output.
How can this be? Can monetary policy really have such huge effects on output 10 years in the
future? Isn’t monetary policy neutral in the long run? Shouldn’t a monetary tightening decrease
output? Here it is crucial to recognize that the information the Fed reveals about economic funda-
mentals is in large part (perhaps mostly) information that the private sector would have learned
about eventually through other channels in the absence of the Fed’s announcement. This intro-

duces an important subtlety into the assessment of the effect of monetary policy that has, to our
knowledge, not been discussed in the existing literature. To correctly assess the causal effect of mon-
etary policy on output, we need to compare versus a reasonable counterfactual that accounts for the
fact that the changes in fundamentals that the Fed’s announcement reveals would have occurred
even in the absence of the announcement. In other words, we want a counterfactual in which
the path of productivity—the exogenous fundamental we assume the Fed provides information
about—follows the same path as in the actual response.
To construct this counterfactual, we must take a stand on when the private sector would have
learned about the changes in fundamentals revealed by the Fed in the absence of the Fed announce-
ment. We choose a particularly simple counterfactual. In this counterfactual, the private sector
learns about changes in productivity when they occur and it believes that productivity follows a
random walk. To be clear, this counterfactual represents our assumption about what would have
happened regarding private sector beliefs about economic fundamentals in the absence of the Fed
announcement. One could consider other counterfactuals. We don’t have any data to precisely pin
down the counterfactual. But we think that our chosen counterfactual is reasonable and it serves the
purpose of illustrating the main issue that one needs to use a counterfactual in which the changes in
economic fundamentals that the Fed provides information about would occur even in the absence
of the Fed announcement.
We must also make an assumption about how monetary policy reacts to changes in the natural
rate of interest in the counterfactual. In keeping with the general assumption that the Fed seeks to
track the natural rate of interest, we assume that monetary policy varies the interest rate to track the
natural rate of interest in the counterfactual.
Figure 7 presents actual and counterfactual output growth constructed in this way. The ﬁgure
reveals that most of the increase in output would have occurred anyway in the absence of the Fed
announcement. Given this new counterfactual, the “causal effect” of the Fed on output growth—the
difference between what happens following the monetary shock, and what would have happened
as represented by the counterfactual—no longer looks so implausible. This difference is much more
modest than the overall change in beliefs about the path of output (which includes the effects of the
productivity shocks the Fed is informing the public about).
Figure 8 plots this measure of the causal effect of monetary shocks on output. The ﬁgure also
decomposes it into two components: the effect on the output gap (which falls) and the effect on the
natural rate of output (which rises). The effect on the output gap is the the conventional channel
of monetary policy: an interest rate increase relative to the natural rate of interest leads to a drop

Figure 7: Response of Actual and Counterfactual Expected Output
0.0
0.5
1.0
1.5
2.0
2.5
3.0
3.5
4.0
4.5
0
4
8
12
16
20
24
28
32
36
40
Quarters
Actual Output
Counterfactual Output
in output relative to the natural rate of output. The second component is a novel effect of Fed
information.
A positive shock to beliefs about economic fundamentals—which leads the future path of the
natural rate of interest to rise—has a positive causal effect on output even relative to the counter-
factual described above. Why is this? This effect arises because of the dynamic linkages in our
model. In our model habit formation by households is important and households understand this.
When consumers expect consumption to be high in the future, they want to consume more today to
build up their habit. This implies that positive news about the future raises consumption and output
today. Other dynamic linkages would yield similar effects of Fed information. For example, in a
model with capital accumulation, news about high future productivity would cause an increase in
investment upon announcement and thereby affect current output.
6.1
Policy Implications
The ﬁndings discussed above have important policy implications. The fact that the information
effect of surprise Fed tightenings stimulates output implies that the Fed is “ﬁghting against itself”
when it surprises markets. Figure 8 shows that for our estimated parameters the overall effect of the
two channels is for an interest rate increase to raise output—the opposite from the conventional view

Figure 8: Causal Effect of Monetary Shocks on Expected Output
‐0.8
‐0.6
‐0.4
‐0.2
Quarters
Output
Natural Output
Output Gap
Figure 9: Expected Output Growth with and without the Information Effect
‐2.0
‐1.5
‐1.0
‐0.5
Quarters
No information effect
With information effect

of how monetary policy works.26 If the Fed would like to stimulate economic activity, a surprise
policy easing may be counter-productive because the increase in pessimism that it causes itself pulls
the economy further down.
This raises the question: Should the Fed withhold releasing bad news about the economy to
avoid the increased pessimism this information would cause? A full analysis of this question is
beyond the scope of this paper. But we would like to note two reasons why it may not be the case
that the Fed should withhold bad news. First, an attempt by the Fed to systematically bias its signals
is likely to be ineffective since the private sector will learn how to interpret what the Fed says and
adjust for the bias. Second, advance knowledge about changes in fundamentals allows agents to
prepare gradually for these changes, which is likely to improve welfare. A possible exception to
this intuition is a circumstance when the Fed is not able to respond to the information it is revealing
by tracking the updated natural rate, e.g., when interest rates are at the zero-lower-bound. In that
case, it may be optimal for the Fed to withhold information.
The information effect also implies that there is an important distinction between interest rate
changes associated with the monetary policy rule and deviations from this rule. The systematic
response of monetary policy to public information—by deﬁnition—does not have information ef-
fects associated with it and therefore will not lead to the “perverse” effects on output discussed
above. Figure 9 contrasts the consequences of an unexpected monetary shock with its associated
information effect and the effects of a similarly sized change in interest rates that comes about due
to the systematic component of monetary policy and therefore does not have an information effect
associated with it.27 The contrast is stark. Since our estimates imply considerable nominal and
real rigidities, increases in interest rates associated with the monetary policy rule reduce output
substantially.
This analysis makes clear that the information content of a monetary shock matters in determin-
ing its effects. Most of what the Fed does is anticipated by markets exactly because it depends in a
systematic way on public information. The effects of this systematic component of monetary policy
are likely to be more conventionally Keynesian than the effects of monetary surprises that contain
signiﬁcant information effects and are therefore a mix of the response to a conventional monetary
26Recall that this result is not simply an implication of the fact that the Fed’s announcement is good news that raises
output expectation. We are subtracting the counterfactual. The effect we are talking about here is the effect that learning
the good news earlier has on the path of output.
27It is important to understand that our empirical results can be used to think about both the effects of monetary policy
shocks and changes in interest rates that come about due to the systematic component of policy. In the linear models we
use, it does not matter why interest rates change (except for the information effect). In other words, the comparative static
of a given change in interest rates on other variables is the same irrespective of the reason for the interest rate change
(except for the information effect).

Table 5: Response of Stock Prices
Stock Prices
-6.5
(3.9)
Response in the Model
Baseline
-6.8
[-11.5, -1.6]
No Fed Information Effect
-11.1
[-19.4, -2.5]
Response in the Data
shock and the response to the non-monetary news contained in the Fed surprise.28 The effects of
monetary surprises will also vary depending on the amount and nature of the information they
convey. In the case of the Volcker disinﬂation, for example, the narrative evidence suggests that few
observers interpreted Volckers decision to raise interest rates as reﬂecting an optimistic view of the
economic outlook. To the extent that the Volcker tightening was broadly interpreted as reﬂecting a
different loss-function, or a greater degree of conservatism in dealing with inﬂation, then this too
would have a small information effect. While we do not allow for any heterogeneity of this nature
in our model, this strikes us as an interesting avenue for future research.
6.2
Stock Price Effects
We ﬁnish the paper with one additional piece of evidence that sheds light on the information content
of FOMC announcements. Table 5 presents the response of stock prices to FOMC announcements.
A pure tightening of monetary policy leads stock prices to fall for two reasons: higher discount rates
and lower output. However, good news about future fundamentals can raise stock prices (if higher
future cash-ﬂows outweigh higher future discount rates). In the data, we estimate that the S&P500
index falls by 6.5% in response to a policy news shock that raises the 2-year nominal forward by
1%.29 This estimate is rather noisy, with a standard error of 3.3%.
Table 5 also presents the response of stock prices to our monetary policy shock in our estimated
model.30 In the calibration of our model where monetary policy announcements convey informa-
tion about both future monetary policy and future exogenous economic fundamentals, stock prices
28This distinction is analogous to the local average treatment effect versus average treatment effect distinction in
applied microeconomics.
29Earlier work by Bernanke and Kuttner (2005) and Rigobon and Sack (2004) ﬁnds large responses of the stock market
to surprise movements in the federal funds rate.
30For simplicity, we model stocks as an unlevered claim to the consumption stream in the economy as is common in
the asset pricing literature.

fall by 6.8% in response to the FOMC announcement. In contrast, if monetary policy is assumed
not to convey information about future exogenous fundamentals, stock prices fall by 11%. The re-
sponse of stock prices in the data is thus another indicator that favors the view that monetary policy
conveys information to the public about future exogenous fundamentals.
7
Conclusion
We use a high-frequency identiﬁcation approach to estimate the causal effect of monetary shocks.
The monetary shocks that we identify have large and persistent effects on real interest rates. Real
rates move essentially one-for-one with nominal rates several years into the term structure. Con-
tractionary monetary shocks lead to no signiﬁcant effect on inﬂation in the short-run and the effect
becomes signiﬁcantly negative only several years into the term structure. However, in sharp con-
trast with the implications of standard monetary models, contractionary shocks raise expectations
about output growth.
We interpret the increase in expected output growth after a monetary tightening as evidence of a
Fed “information effect.” When the Fed raises interest rates, this leads to increased optimism about
economic fundamentals. We develop a model of this Fed information effect, in which the private
sector interprets part of an unexpected increase in the interest rate as information about the natural
rate. We estimate the model and ﬁnd strong evidence for both channels: the conventional monetary
policy channel and the information effect. One implication of our analysis is that the information
content of a monetary shock matters in determining its causal effects.

A
Construction of the Policy News Shock
The policy news shock is constructed as the ﬁrst principle component of the change in ﬁve interest
rates. The ﬁrst of these is the change in market expectations of the federal funds rate over the
remainder of the month in which the FOMC meeting occurs. To construct this variable we use
data on the price of the federal funds futures contract for the month in question. The federal funds
futures contract for a particular month (say April 2004) trades at price p and pays off 100 −¯r where
¯r is the average of the effective federal funds rate over the month.31 To construct the change in
expectations for the remainder of the month, we must adjust for the fact that a part of the month
has already elapsed when the FOMC meeting occurs. Suppose the month in question has m0 days
and the FOMC meeting occurs on day d0. Let f1
t−∆t denote the price of the current month’s federal
funds rate futures contract immediately before the FOMC announcement and f1
t the price of this
contract immediately following the FOMC announcement. Let r−1 denote the average federal funds
rate during the month up until the point of the FOMC announcement and r0 the average federal
funds rate for the remainder of the month. Then
f1
t−∆t = d0
m0
r−1 + m0 −d0
m0
Et−∆tr0,
f1
t = d0
m0
r−1 + m0 −d0
m0
Etr0.
As a result
Etr0 −Et−∆tr0 =
m0
m0 −d0
(f1
t −f1
t−∆t).
When the FOMC meeting occurs on a day when there are 7 days or less remaining in a month,
we instead use the change in the price of next month’s fed funds futures contract. This avoids
multiplying f1
t −f1
t−∆t by a very large factor.
The second variable used in constructing the policy news shock is the change in the expected
federal funds rate at the time of the next scheduled FOMC meeting. Similar issues arise in con-
structing this variable as with the variable described above. Let m1 denote the number of days
in the month in which the next scheduled FOMC meeting occurs and let d1 denote the day of the
meeting. The next scheduled FOMC meeting may occur in the next month or as late as 3 months
31Fed funds futures have been traded since 1988. The effective federal funds rate is the rate that is quoted by the Fed-
jamesgoulding.com/Research_II/FedFundsFutures/FedFunds(FuturesReferenceGuide).pdf for a de-
tailed description of federal funds futures contracts. On a trading day in March (say), the April federal funds futures
contract is labeled as 2nd expiration nearby and also as 1st beginning nearby, in reference to the month over which ¯r is
computed.

after the current meeting. Let fn
t−∆t denote the price of the federal funds rate futures contract for the
month of the next scheduled FOMC meeting immediately before the FOMC announcement and fn
t
the price of this contract immediately following the FOMC announcement. Let r1 denote the fed-
eral funds rate after the next scheduled FOMC meeting. Analogous calculations to what we present
above yield
Etr1 −Et−∆tr1 =
m1
m1 −d1

(fn
t −fn
t−∆t) −d1
m1
(Etr0 −Et−∆tr0)

.
As with the ﬁrst variable, if the next scheduled FOMC meeting occurs on a day when there are 7
days or less remaining in a month, we instead use the change in the price of next month’s federal
funds futures contract.
The last three variables used are the change in the price of three eurodollar futures at the time
of the FOMC announcements. A eurodollar futures contract expiring in a particular quarter (say
2nd quarter 2004) is an agreement to exchange, on the second London business day before the third
Wednesday of the last month of the quarter (typically a Monday near the 15th of the month), the
price of the contract p for 100 minus the then current three-month US dollar BBA LIBOR interest
rate. The contract thus provides market-based expectations of the three month nominal interest rate
on the expiration date.32 We make use of eurodollar futures at horizons of n quarters in the future
for n = 2, 3, 4 or, more precisely, the expiration date of the “n quarter” eurodollar future is between
n −1 and n quarters in the future at any given point in time.
We approximate the change in these variables over a 30-minute window around FOMC by tak-
ing the difference between the price in the last trade that occurred more than 10 minutes before
the FOMC announcement and the ﬁrst trade that occurred more than 20 minutes after the FOMC
announcement. On control days in the analysis using the heteroskedasticity based estimation ap-
proach, we take the last trade before 2:05pm and the ﬁrst trade after 2:35pm (since FOMC announce-
ments tend to occur at 2:15pm). On some days (most often control days), trading is quite sparse and
there sometimes is no trade before 2:05 or after 2:35. To limit the size of the windows we consider,
we only consider trades on the trading day in question and until noon the next day. If we do not
ﬁnd eligible trades to construct the price change we are interested in within this window, we set the
price change to zero (i.e., we interpret no trading as no price change).
32Eurodollar futures began trading in the early 1980’s.
See the CME Group eurodollar futures ref-
nce-guide.pdf for more details about how eurodollar futures are deﬁned.

B
Rigobon’s Heteroskedasticity-Based Estimator
Table 2 presents results from a heteroskedasticity-based estimator of the type developed by Rigobon
(2003) and Rigobon and Sack (2004). The empirical model we consider in this analysis is the follow-
ing. Let ϵt denote a pure monetary shock and suppose that movements in the policy indicator ∆it
we observe in the data is governed both by monetary and non-monetary shocks:
∆it = αi + ϵt + ηt,
(8)
where ηt is a vector of all other shocks that affect ∆it. Here αi is a constant and we normalize
the impact of ϵt and ηt on ∆it to one. We wish to estimate the effects of the monetary shock ϵt on
an outcome variable ∆st. This variable is also affected by both the monetary and non-monetary
shocks:
∆st = αs + γϵt + βηt.
(9)
The parameter of interest is γ, which should be interpreted as the impact of the pure monetary
shock ϵt on ∆st relative to its impact on ∆it.
Our identifying assumption is that the variance of monetary shocks increases at the time of
FOMC announcements, while the variance of other shocks is unchanged. Deﬁne R1 as a sample of
narrow time intervals around FOMC announcements, and deﬁne R2 as a sample of equally narrow
time intervals that do not contain FOMC announcements but are comparable on other dimensions
(e.g., same time of day, same day of week, etc.). We refer to R1 as our “treatment” sample and R2
as our “control” sample. Our identifying assumption can then be written as
σϵ,R1 > σϵ,R2, while ση,R1 = ση,R2.
Let ΩRi denote the variance-covariance matrix of [∆it, ∆st] in regime Ri. Then ΩRi is given by
ΩRi =


σ2
ϵ,Ri + P
j σ2
η,j
γσ2
ϵ,Ri + P
j βs,jσ2
η,j
γσ2
ϵ,Ri + P
j βs,jσ2
η,j
γ2σ2
ϵ,Ri + P
j β2
s,jσ2
η,j

,
where j indexes the elements of ηt.
Notice that
∆Ω= ΩR1 −ΩR2 = (σ2
ϵ,R1 −σ2
ϵ,R2)

1
γ
γ
γ2

.

Thus,
γ = ∆Ω12
∆Ω11
= covR1(∆it, ∆st) −covR2(∆it, ∆st)
varR1(∆it) −varR2(∆it)
.
(10)
This is the estimator we use to construct the results in Table 2 and Table A.3. Notice that if we
set the variance of the “background noise” ηt to zero, then the heteroskedasticity-based estimator,
equation (10) reduces to the coefﬁcient from an OLS regression of ∆st on ∆it. Intuitively, the full
heteroskedasticity-based estimator can be thought of as the simple OLS estimator, adjusted for the
“normal” covariance between ∆st and ∆it and the “normal” variance of ∆it.
C
Weak Instruments Robust Conﬁdence Intervals
The conﬁdence intervals in Table 2 are constructed using a more sophisticated bootstrap procedure
than is conventional. The reason is that the conventional bootstrap approach to constructing conﬁ-
dence intervals yields inaccurate results in the case when there is a signiﬁcant probability that the
difference in the variance of ∆it between the treatment and control sample is close to zero.33 Figure
C.1 illustrates that this is the case for the 1-day window estimation but not the 30-minute window.
The problem is essentially one of weak instruments. Rigobon and Sack (2004) show that the estima-
tor in equation (10) can be formulated as an IV regression. When the difference in the variance of
∆it between the treatment and control sample is small, the instrument in this formulation is weak,
leading to biased point estimates and conﬁdence intervals.
In Table 2, we, therefore, employ a weak-instruments robust approach to constructing conﬁ-
dence intervals. The approach we employ is a test inversion approach. A 95% conﬁdence interval
for our parameter of interest γ can be constructed by performing a hypothesis test for all possi-
ble hypothetical true values of γ and including those values that are not rejected by the test in the
conﬁdence interval.
The test statistic we use is
g(γ) = ∆cov(∆it, ∆st) −γ∆var(∆it),
(11)
where ∆cov and ∆var denote the difference between the covariance and variance, respectively, in
the treatment and control samples.
33Recall that the Rigobon estimator—equation (10)—is a ratio with the difference in the variance of ∆it between the
treatment sample and the control sample in the denominator. If the distribution of this difference has signiﬁcant mass in
the vicinity of zero, the sampling distribution of the estimator will have signiﬁcant mass at large positive and negative
values.

Panel A: 1-Day Window 

Panel B: 30-Minute Window 
-0.0010
-0.0005
0.0000
0.0005
0.0010
0.0015
0.0020
0.0025
0.0030
0.0035
0.0040
0.0045
-0.002
-0.001
0.000
0.001
0.002
0.003
0.004
0.005
Dvar
Dcov
0.0000
0.0005
0.0010
0.0015
0.0020
0.0025
-0.0005
0.0000
0.0005
0.0010
0.0015
0.0020
0.0025
Dvar
Dcov
Figure C.1: Scatter of Joint Distribution of Dcov and Dvar for 2-Year Nominal Forward Rate
Notes: Each point in the ﬁgure is a draw from our bootstrap. Dvar denotes the difference in variance of our policy news
shock between the treatment and control sample. Dcov denotes the difference in the covariance of our policy news
shocks and the 2-year nominal forward rate between the treatment and the control sample.

-0.008
-0.006
-0.004
-0.002
0.000
0.002
0.004
0.006
0.008
-2.0
-1.5
-1.0
-0.5
0.0
0.5
1.0
1.5
2.0
2.5
g(gamma)
gamma
Median
97.5% Quantile
2.5% Quantile
Figure C.2: Quantiles of the Distribution of g(γ)
Notes: Quantiles of the distribution of g(γ) for different values of γ when estimating effect on the 2-year nominal
forward rate using a 1-day window
Intuitively, g(γ) = 0 at the true value of γ. We estimate the distribution of g(γ) for each hypo-
thetical value of γ and include in our conﬁdence interval values of γ for which g(γ) = 0 cannot be
rejected. Figure C.2 plots the 2.5%, 50% and 97.5% quantiles of the distribution of g(γ) as a function
of γ for the 2-year nominal forward in the one-day window case. Values of γ for which the 2.5%
quantile lies below zero and and 97.5% quantile lies above zero are included in the 95% conﬁdence
interval. This method for constructing conﬁdence intervals is referred to as the Fieller method by
Staiger, Stock, and Watson (1997) as it is an extension of an approach proposed by Fieller (1954).
We use a bootstrap to estimate the joint distribution of ∆cov and ∆var. Our approach is therefore
similar to the grid bootstrap proposed by Hansen (1999) for a different application.
This more sophisticated procedure for constructing conﬁdence intervals is not important for
our baseline estimator based on changes in the policy news shock over a 30-minute window. In this
case, the weak-IV robust conﬁdence intervals coincide closely with the standard non-parametric
bootstrap conﬁdence interval reported in Table A.3. However, this weak-IV robust procedure is
very important for the Rigobon estimator when the policy news shock is measured over a 1-day
window.

D
Risk Premia or Expected Future Short Rates
We present three sets of results that indicate that risk premium effects are not driving our empirical
results: 1) the impact of our policy news shock on direct measures of expectations from the Blue
Chip Economic Indicators; 2) the impact of our policy news shock on risk-neutral expected short rates
from a state-of-the-art afﬁne term structure model; and 3) the impact of our policy news shock on
interest rates over longer event windows than in our baseline results.
Let us begin with our analysis of the Blue Chip forecast data. Blue Chip surveys professional
forecasters on their beliefs about macroeconomic variables over the next two years in the ﬁrst few
days of every month. From this survey, it is possible to obtain direct measures of expectations that
are not contaminated by risk premium effects. We use expectations about future values of the 3-
month T-Bill rate as our measure of short-term nominal interest rate expectations and expectations
about changes in the GDP deﬂator as our measure of expectations about inﬂation (and the difference
between the two as our measure of expectations about short-term real rates).
We estimate the impact of monetary shocks on expectations by running regressions of the change
from one month to the next in expectations regarding a particular forecast horizon on the policy
news shock that occurs over the month except for those that occur in the ﬁrst week of the month
(because we do not know whether these occurred before or after the survey response). Unfor-
tunately, Blue Chip asks respondents only about the current and subsequent calendar year on a
monthly basis. So, fewer observations are available for longer-term expectations, leading to larger
standard errors.34 The sample period for this analysis is January 1995 to April 2014, except that we
exclude the apex of the 2008-2009 ﬁnancial crisis as we do in our baseline analysis.
Table D.1 presents the results from this analysis. The table shows that the policy news shock has
a persistent impact on expected short-term interest rates, both nominal and real. The interest rate
effects are somewhat larger than in our baseline results, but rather noisily estimated. The effect on
expected inﬂation is small and statistically insigniﬁcant at all horizons. The much larger standard
errors in Table D.1 arise from the fact that the Blue Chip variables are available only at a monthly
frequency as opposed to a daily frequency. Overall, these estimates appear consistent with our
baseline ﬁndings that monetary shocks have large effects on expected short-term nominal and real
rates.
34For example, towards the end of each year, forecasters are only asked about their beliefs a little more than 1-year in
advance; while in the ﬁrst quarter they are asked about their beliefs for almost the next full 2-years. Blue Chip also asks
for longer-term inﬂation forecasts, but only twice a year (March and October) implying that there are too few observations
to obtain meaningful estimates.

Table D.1: Effects of Monetary Shocks on Survey Expectations
Nominal
Real
Inflation
1 quarter
1.05
1.17
-0.12
(0.73)
(0.78)
(0.24)
2 quarters 
1.18
1.63
-0.44
(0.75)
(0.78)
(0.31)
3 quarters
0.99
1.29
-0.30
(0.72)
(0.77)
(0.24)
4 quarters
0.86
1.17
-0.32
(0.71)
(0.69)
(0.23)
5 quarters
0.73
0.59
0.14
(0.89)
(0.94)
(0.21)
6 quarters
1.84
1.60
0.23
(0.89)
(0.88)
(0.24)
7 quarters
4.45
4.29
0.17
(1.91)
(1.99)
(0.27)
Each estimate comes from a separate OLS regression. We regress changes in survey expectations from the Blue 
Chip Economic Indicators on the policy news shock. Since the Blue Chip survey expectations are available at a
monthly frequency, we construct a corresponding monthly measure of our policy news shock. In particular, we
use any policy news shock that occurs over the month except for those that occur in the first week (because we do
not know whether these occurred before or after the survey response). The dependent variable is the change in the
forecasted value of the variable listed at the top N quarters ahead, between this month's survey and last month's
survey. See Appendix F for details. We consider the effects on expected future 3-month T-Bill rates, short-term
real interest rates and inflation, where the inflation rate is the GDP deflator and the short-term real interest rate is
calculated as the difference between the expected 3-month T-bill rate and the expected GDP deflator for a given
quarter. The sample period is all regularly scheduled meetings between January 1995 and April 2014, except that
we exclude the period from July 2008 through June 2009 and the aforementioned first-week meetings. The policy
news shock is constructed on this sample period. The sample size is 120 for the first four rows of the table. It then
falls to 75, 45, and 13 for rows 5 through 7, respectively. Robust standard errors are in parentheses.
Our second approach is to regress estimates of changes in expected future short rates from a
state-of-the-art afﬁne term structure model on our monetary policy shocks. Abrahams et al. (2015)
employ an afﬁne term structure model to decompose changes in both nominal and real interest rates
at different maturities into changes in risk-neutral expected future short rates and changes in risk
premia.35 Table D.2 presents results based on their decomposition. The response of model-implied
risk-neutral interest rates to our policy news shock is very similar to the response of raw interest
rates in our baseline results. This piece of evidence, thus, points to our monetary shocks having
large effects on future short-term nominal and real rates and small effects on expected inﬂation
35What we refer to as the risk premia here is the difference between raw interest rate changes and changes in model-
implied risk neutral interest rates. Abrahams et al. (2015) further decompose this difference into a term premium, a
liquidity premium, and a model error term.

Table D.2: Response of Expected Future Short Rates and Risk Premia
Nominal 
Real 
Nominal 
Real 
2Y Treasury Yield
1.01
0.86
0.09
0.20
(0.27)
(0.17)
(0.10)
(0.18)
3Y Treasury Yield
0.93
0.82
0.13
0.21
(0.26)
(0.18)
(0.15)
(0.19)
5Y Treasury Yield
0.76
0.60
-0.04
0.04
(0.16)
(0.12)
(0.11)
(0.14)
10Y Treasury Yield
0.50
0.40
-0.12
0.04
(0.11)
(0.08)
(0.14)
(0.14)
2Y Treasury Forward Rate
0.79
0.73
0.35
0.26
(0.24)
(0.22)
(0.26)
(0.21)
3Y Treasury Forward Rate
0.61
0.56
0.21
0.32
(0.19)
(0.17)
(0.29)
(0.25)
5Y Treasury Forward Rate
0.36
0.33
-0.11
0.14
(0.08)
(0.08)
(0.17)
(0.17)
10Y Treasury Forward Rat
0.10
0.09
-0.18
0.04
(0.02)
(0.02)
(0.18)
(0.12)
Expected Future Short Rates
Risk Premia
Each estimate comes from a separate OLS regression. The dependent variables in the first two columns are one-day
changes in risk neutral yields and forwards from Abrahams et al. (2015) -- i.e., measures of expected future short
rates. The dependent variables in the later two columns are the difference between one-day changes in raw yields
and forwards and one-day changes in the risk neutral yields and forwards from Abrahams et al. (2015). We refer to
this difference as the risk premia. It corresponds to the term premium, liquidity premium and model error in
Abrahams et al. (2015). The independent variable is a change in the policy new shock over a 30 minute window
around the time of FOMC announcements. The forward rates are one-year forwards at different horizons. The
sample period is all regularly scheduled FOMC meetings from 1/1/2000 to 3/19/2014, except that we drop the
period from July 2008 through June 2009. For 2Y and 3Y yields and real forwards, the sample starts in January
2004. The sample size for the 2Y and 3Y yields and forwards is 74. The sample size for all other regressions is
106—the same observations from which the policy news shock is constructed. Robust standard errors are in
parentheses.

(even smaller than in our baseline results).
It is important to stress that the Abrahams et al. (2015) model by no means rules out the potential
importance of risk premium effects. In fact, risk premia for long-term bonds are large and volatile
in this model. While this model predicts that a large fraction of interest rate variation at other times
are associated with risk premia, this is not the case for interest rate movements at the time of FOMC
announcements. In this regard, our measure of the monetary shock appears to differ importantly
from that of Hanson and Stein (2015). Our monetary shocks have virtually no effect on risk premia,
as we describe above. In contrast, Hanson and Stein’s measure (based on the 2-day change in the
2-year nominal yield around FOMC announcements, as we describe in section 3.2) is associated
with large changes in risk premia (Abrahams et al., 2015). This suggests that Hanson and Stein’s
measure of monetary policy shocks is—either due to greater background noise, or because it picks
up variation in interest rates further out in the yield curve—much more associated with movements
in risk premia at the time of FOMC meetings than our policy news shock.
Our third approach to gauging the role of risk premia in our results is to consider longer event
windows for the outcome variables of interest. Some models of liquidity premia (such as the one
developed in Hanson and Stein (2015)) predict that we should see real interest rate effects dissipate
quickly after the announcement.36 Table D.3 presents the effects of our policy news shock on nomi-
nal and real interest rates over event windows of 1, 5, 10, 20, 60, 125, and 250 trading days.37 While
the estimates become very noisy as the event window becomes larger, there is little evidence that
the effects on interest rates tend to dissipate over time. Indeed, in most cases, the point estimates
appear to grow over time (though, again, the standard errors are quite large).
E
A Conventional Model of Monetary Shocks
What do the empirical estimates in section 3 tell us about the economy? The conventional view
of how monetary policy affects the economy can be decomposed into two parts. First, changes in
nominal interest rates affect real interest rates. Second, changes in real interest rates affect output.
The second of these components is a common feature of virtually all macroeconomic models and
has nothing to do with monetary policy per se. In particular, both Neoclassical and New Keynesian
models share the implication that changes in real interest rates affect output. In sharp contrast,
36Hanson and Stein (2015) present a behavioral model in which “search for yield” generates signiﬁcant risk premium
effects of monetary shocks that dissipate over time.
37In all cases, the policy news shock is measured over a 30-minute event window. We only vary the length of the event
window for the dependent variables.

Table D.3: Mean Reversion
2-Year
3-Year
5-Year
2-Year
3-Year
5-Year
1
1.10
1.06
0.73
1.06
1.02
0.64
(0.34)
(0.39)
(0.21)
(0.28)
(0.31)
(0.19)
5
2.24
2.06
0.85
1.01
0.93
0.52
(1.09)
(1.07)
(0.50)
(0.64)
(0.68)
(0.38)
10
2.39
2.20
0.22
1.35
1.20
0.28
(1.07)
(1.05)
(0.80)
(0.55)
(0.57)
(0.53)
20
0.60
0.29
-0.01
0.88
0.43
0.04
(1.22)
(1.16)
(1.11)
(0.95)
(0.94)
(0.79)
60
3.41
2.80
-0.17
1.96
1.72
-0.10
(2.38)
(2.17)
(1.46)
(2.13)
(1.92)
(1.13)
125
9.42
8.02
3.20
6.16
5.22
2.47
(1.78)
(1.61)
(1.98)
(2.86)
(2.50)
(1.44)
250
13.52
11.56
4.72
9.58
8.22
4.13
(3.31)
(3.08)
(2.30)
(2.92)
(2.97)
(1.84)
Each estimate comes from a separate OLS regression. We regress the cumulative change in yields between the day before the
FOMC announcement and 1, 5, 10, 20, 60, 125 and 250 trading days after the announcement on the policy news shock in the 30
minute interval surrounding the FOMC announcement. The first three columns present results for nominal zero coupon yields,
and the next three columns present results for real zero coupon yields. The sample period is all regularly scheduled meetings
from 1/1/2000 to 3/19/2014, except that we drop the period from July 2008 through June 2009. For 2Y and 3Y yields, the sample
starts in January 2004. Going down the rows, the sample sizes for the 2Y and 3Y yields are 74, 73, 73, 73, 72, 69, and 65. The
sample sizes for the 5Y yield are 106, 105, 105, 105, 104, 101, and 97. The policy news shock is constructe on the 2000-2014
sample used in Table 1. Newey-West standard errors with 4 lags are in parentheses.
Horizon 
(Trading Days)
Nominal Yields
Real Yields
Neoclassical and New Keynesian models have very different predictions regarding the extent to
which changes in nominal interest rates caused by monetary policy can affect real interest rates. In
a Neoclassical model, variation in nominal interest rates caused by monetary policy have no effect
on the real interest rate, while in New Keynesian models, such movements in nominal interest rates
can have large effects on real rates if prices are sufﬁciently sticky.
The evidence we present in section 3 shows that variation in nominal interest rates caused by
monetary policy announcements does have large and persistent effects on real interest rates. In a
conventional model of how monetary shocks affect the economy—i.e., one where monetary shocks
only convey information about the future path of policy and don’t change private sector views
about other fundamentals of the economy—this evidence identiﬁes key parameters governing the
rigidity of prices. We can illustrate this very simply using the textbook New Keynesian model.
Consider a setting in which the behavior of households and ﬁrms can be described by the fol-

lowing Euler equation and Phillips curve:
ˆxt = Etˆxt+1 −σ(ˆıt −Etˆπt+1 −ˆrn
t ),
(12)
ˆπt = βEtˆπt+1 + κζˆxt.
(13)
Hatted variables denote percentage deviations from steady state. The variable ˆx = ˆyt −ˆyn
t denotes
the “output gap”—the difference between actual output ˆyt and the “natural” level of output ˆyn
t
that would prevail if prices were ﬂexible— ˆπt denotes inﬂation, ˆıt denotes the gross return on a
one-period, risk-free, nominal bond, and ˆrn
t denotes the “natural rate of interest.” The parameter
σ in the Euler equation denotes the intertemporal elasticity of substitution, while β denotes the
subjective discount factor of households, κ and ζ denote nominal and real rigidities, respectively.
Both the natural rate of output and the natural rate of interest are functions of exogenous shocks
to tastes and technology. Appendix H presents a detailed derivation of these equations from prim-
itive assumptions about tastes and technology. Woodford (2003) and Gali (2008) present textbook
treatments.
Suppose this economy starts off at a zero-inﬂation steady state and is then disturbed by a mon-
etary shock. Assuming that the monetary shock has no effect on output in the long run, we can
solve the Euler equation—equation (12)—forward and get that the response of the output gap to
the monetary shock is,
ˆxt = −σ
∞
X
j=0
Etˆrt+j = −σˆrℓ
t.
(14)
where ˆrt+j denotes the response of the short-term real interest rate at time t + j—i.e., ˆrt+j = ˆıt+j −
Et+jˆπt+j+1—and ˆrℓ
t denotes the response of the long-run real interest rate. Notice that ˆrn
t = 0 in this
case since the monetary shock has no effect on the natural rate of interest.
Similarly, we can solve forward the Phillips curve—equation (13)—and get that the response of
inﬂation to the monetary shock is
ˆπt = κζ
∞
X
j=0
βjEtˆxt+j.
(15)
Combining equations (14) and (15), we get a relationship between the response of inﬂation and
the response of the real interest rates to the monetary shock:
ˆπt = −κζσ
∞
X
j=0
βjEtˆrℓ
t+j.
(16)

Recall that in section 3 we estimate the response of inﬂation and real interest rates to a monetary
shock. These are exactly the two responses that appear in equation (16). Equation (16) therefore
shows that in the textbook New Keynesian model the relative size of the response of inﬂation and
real interest rates pins down the magnitude of the parameter triplet κζσ. Viewed through the lens
of this model, the fact that we estimate a small response of inﬂation relative to the response of the
real interest rate implies that either: 1) the Phillips curve must be very ﬂat (κζ small), implying a
lot of nominal and real rigidities, or 2) output must be very unresponsive to the real interest rate (σ
small), or both.
Notice that in reaching these conclusions we do not need to fully specify the monetary policy
rule. The only assumption we need to make about monetary policy is that monetary shocks do not
have long-run effects on output. This is true of most common speciﬁcations of monetary policy
rules used in the literature. In this respect, the conclusions reached above are quite robust.
Even so, let’s consider whether this argument continues to hold even if the monetary shock leads
to a shift in the long-run inﬂation target of the central bank (and therefore the long-run inﬂation
rate). In this case, equation (16) becomes
ˆπt = −κζσ
∞
X
j=0
βjEtˆrℓ
t+j + ˆπ∞,
(17)
where ˆπ∞denotes the change in the long-run inﬂation rate. The case we consider above assumed
that π∞= 0. Even if this term is non-zero, however, it is important to recognize that it affects
inﬂation in every period after the shock. Hence, it would not change the slope of the response of
expected inﬂation. The extra term does have the potential to lead to a larger response of inﬂation
to a monetary shock than in our baseline model. Empirically, however, the response of expected
inﬂation to the monetary shock already appears to be very small. Adding this feature to the model
would further increase the degree of rigidities we estimate in the data, and therefore, the degree of
monetary non-neutrality.
In the analysis above, we did rely heavily on the conventional view of monetary shocks that
they convey information only about the future path of policy but don’t change private sector views
about other fundamentals of the economy. In this view, monetary shocks may occur because the
private sector is learning about the preferences of the policymakers, or because the private sector is
learning about the policymaker’s model of the world, or because the private sector is learning about
the policymaker’s views on the state of the economy. Crucially, however, the announcement by the
policymaker cannot lead the private sector to update its own views about the state of the economy

or the model of the world. If it does, the monetary shocks contains an additional “information
effect.”
If FOMC announcements affect not only beliefs about future monetary policy but also beliefs
about future natural rates of interest, the conclusions reached above regarding what we can learn
from the empirical evidence presented in section 3 can change dramatically. In this case, equation
(14) becomes
ˆxt = −σ
∞
X
j=0
Et(ˆrt+j −ˆrn
t+j) = −σ(ˆrℓ
t −ˆrnℓ
t ),
(18)
where ˆrnℓ
t
denotes the response to the monetary announcement of private sector beliefs about the
long-term natural rate of interest, and equation (16) becomes
ˆπt = −κζσ
∞
X
j=0
βjEt(ˆrℓ
t+j −ˆrnℓ
t ).
(19)
It is important to recognize that private sector behavior depends on private sector beliefs about the
future path of the natural rate. The variables ˆrn
t+j and ˆrnℓ
t
denote the response of private sector
beliefs about natural rates, and ˆrt+j and ˆrℓ
t+j denote the response of private sector beliefs about
actual real rates.
Notice that allowing for information effects, the response of the output gap and inﬂation to a
monetary announcement is not determined by the response of real interest rates but rather by the
response of the real interest rate gap—i.e., the gap between real interest rates and the natural rate
of interest. This means that changes in real interest rates will not have as large effects on output
and inﬂation if FOMC announcements have information effects since the movement in the interest
rate gap will be only some fraction of the overall movement in interest rates. It also means that
we will estimate larger values of the parameter triplet κζσ—i.e., smaller values of nominal and real
rigidities (for a given value of the IES)—since the sum on the right-hand-side of equation (19) will
be smaller than if we ignored information effects.
F
Expected Output Growth Regressions
The regressions in Tables 3 and A.5 are of the form
∆st,t−1 = α + γ∆it−1 + ϵt
(20)

with the policy news shock as the independent variable. In Table 3, the dependent variable is
∆st,t−1 = gyt,q(t)+1 + gyt,q(t)+2 + gyt,q(t)+3
3
−gyt−1,q(t)+1 + gyt−1,q(t)+2 + gyt−1,q(t)+3
3
(21)
where gyt,q(t)+j denotes the average forecast made in month t about output growth in quarter q(t)+
j, where q(t) is the quarter that month t belongs to. For example, t might be September 2008, in
which case q(t) is the third quarter of 2008, q(t) + 2 is the ﬁrst quarter of 2009, and gyt,q(t)+2 is the
average forecast made in September 2008 about the value of output growth in the ﬁrst quarter of
2009. In Table A.5, the dependent variable is
∆st,t−1 = gyt,q(t)+j −gyt−1,q(t)+j
(22)
for j ∈{0, 1, ..., 7}.
G
Greenbook Evidence
If Fed information is important, one might expect that contractionary monetary shocks would dis-
proportionately occur when the Fed is more optimistic than the private sector about the state of
the economy. The top panel of Table G.1 tests this proposition using the Fed’s Greenbook forecast
about output growth as a measure of its optimism about the economy.38 We report estimates from
the following regression:
policy news shockt = α + β
 ∆yGB
t,q −∆yBC
t,q

+ εt,
(23)
where ∆yGB
t,q is the Greenbook forecast of quarterly output growth (annualized) q quarters in the
future made in month t, and ∆yBC
t,q is the corresponding Blue Chip forecast. In words, we regress
our policy news shock on the contemporaneous difference between the Greenbook and Blue Chip
forecasts about real GDP growth at various horizons. The positive coefﬁcients reported in the top
panel of Table G.1 indicate that our policy news shocks tend to be positive (i.e., indicate a surprise
increase in interest rates) when the Greenbook forecast about current and future real GDP growth
is higher than the corresponding Blue Chip forecast.
38The staff of the Board of Governors has presented the FOMC with analysis and forecasts of the US economy in the
Greenbook (now, the Tealbook) since 1965. Conveniently, both the Greenbook and Blue Chip datasets make forecasts
of the same variable: annualized real GDP growth. The Greenbook forecasts are ﬁnalized one week before each FOMC
meeting.

Table G.1: Is Fed Information Reﬂected in Greenbook Forecasts?
Horizon (q): 
-1
0
1
2
3
4
5
6
7
Does Fed Relative Optimism Explain Monetary Shocks?
β
--
1.19
1.01
1.21
1.00
1.20
1.89
3.10
1.88
--
(0.55)
(0.74)
(0.69)
(0.77)
(0.90)
(1.10)
(1.14)
(1.64)
N
--
90
90
90
90
90
66
42
22
β
-7.26
-4.07
-0.45
-0.87
-0.46
-1.66
-3.58
-1.34
-3.04
(3.63)
(1.80)
(1.53)
(1.30)
(1.08)
(1.11)
(1.31)
(1.30)
(2.44)
N
24
89
89
89
89
76
55
32
8
Does Fed Relative Optimism Reverse in Response to Monetary Shocks?
Each estimate comes from a separate OLS regression. In the first panel, we regress the policy news shock (scaled by
100) on the difference in forecasts about output growth q quarters ahead between the Fed's Greenbook forecast and the
Blue Chip forecast. Since the Blue Chip forecasts are available at a monthly frequency, we construct a corresponding
monthly measure of our policy news shock. In particular, we use any policy news shock that occurs over the month
except for those that occur in the first week (because we do not know whether these occurred before or after the survey
response). In the second panel, we regress the change in the difference between the Greenbook and Blue Chip forecast
of output growth q quarters ahead on the news policy shock. The change is between the month of the policy shock and
the month of the subsequent FOMC meeting. See Appendix F for details. The sample period is all regularly scheduled
FOMC meetings from January 1995 to December 2009, except that we exclude the period from July 2008 through
June 2009 and the aforementioned first-week meetings. The policy news shocks are constructed over the 1995-2014
sample used in Table A.5. Robust standard errors are in parentheses.   
We furthermore ﬁnd that the difference between Greenbook and Blue Chip forecasts tends to
narrow after our policy news shocks occur. This suggests that private sector forecasters may update
their forecasts based on information they gleam from FOMC announcements. Building on the work
of Romer and Romer (2000), we estimate the following regression:
 ∆yGB
t+1,q −∆yBC
t+1,q

−
 ∆yGB
t,q −∆yBC
t,q

= α + βpolicy news shockt + εt+1,
(24)
where time t + 1 is the month of the next FOMC meeting. In words, we assess whether our policy
news shocks forecast a change in the difference between the Greenbook and the Blue Chip forecasts
of output growth. The results of this regression are reported in the bottom panel of Table G.1. We
ﬁnd that a positive policy news shock forecasts a fall in the Greenbook forecast relative to the Blue
Chip forecast (or equivalently a rise in the Blue Chip forecast relative to the Greenbook forecast).
This change in statistically signiﬁcant for the nowcast (q = 0) and for one of the longer-term fore-
casts (q = 5) but not statistically signiﬁcant for the other horizons. Since positive monetary shocks
tend to be associated with the Greenbook forecast being above the Blue Chip, the fact that the esti-
mates are negative in this regression indicates that, indeed, our policy news shocks are associated

with a narrowing in the discrepancy between Fed and private sector views on the economy.
H
Micro-Foundations for Our Model
This section lays out micro-foundations for the New Keynesian business cycle model we use in the
paper. We do this in two steps. First we present a version of the model without internal habit and
a backward-looking term in the Phillips curve. Then in sections H.4-H.6, we show how the model
is modiﬁed to include internal habit and a backward-looking term in the Phillips curve. We end
this appendix with a discussion of the determination of the natural rate of output and productivity
in the full model. We note that none of the derivations in this section depend on whether there is
an information effect of not. See Woodford (2003) and Gali (2008) for thorough expositions of New
Keynesian models.
H.1
Households
The economy is populated by a continuum of household types indexed by x. A household’s type
indicates the type of labor supplied by that household. Households of type x seek to maximize their
utility given by
E0
∞
X
t=0
βt[u(Ct, ξt) −v(Lt(x), ξt)],
(25)
where β denotes the household’s subjective discount factor, Ct denotes household consumption of
a composite consumption good, Lt(x) denotes household supply of differentiated labor input x,
and ξt denotes a vector of preference shocks. There are an equal (large) number of households of
each type. The composite consumption good in expression (25) is an index given by
Ct =
Z 1
0
ct(z)
θ−1
θ dz

θ
θ−1
,
(26)
where ct(z) denotes consumption of products of variety z. The parameter θ > 1 denotes the elastic-
ity of substitution between different varieties.
Households have access to complete ﬁnancial markets. Households of type x face a ﬂow budget
constraint given by
PtCt + Et[Mt,t+1Bt+1(x)] ≤Bt(x) + Wt(x)Lt(x) +
Z 1
0
Ξt(z)dz −Tt,
(27)

where Pt is a price index that gives the minimum price of a unit of the consumption good Ct, Bt+1(x)
is a random variable that denotes the state contingent payoff of the portfolio of ﬁnancial securities
held by households of type x at the beginning of period t+1, Mt,t+1 is the stochastic discount factor
that prices these payoffs in period t,39 Wt(x) denotes the wage rate received by households of type
x in period t, Ξt(z) denotes the proﬁts of ﬁrm z in period t, and Tt is a lump-sum tax levied by the
government. To rule out Ponzi schemes, household debt cannot exceed the present value of future
income in any state of the world.
Households face a decision in each period about how much to spend on consumption, how
many hours of labor to supply, how much to consume of each differentiated good produced in
the economy and what portfolio of assets to purchase. Optimal choice regarding the trade-off be-
tween current consumption and consumption in different states in the future yields the following
consumption Euler equation:
uc(Ct+j, ξt+j)
uc(Ct, ξt)
= Mt,t+j
βj
Pt+j
Pt
(28)
as well as a standard transversality condition. The notation uc denotes the partial derivate of the
function u with respect to Ct. We use analogous notation for other partial derivatives below. Equa-
tion (28) holds state-by-state for all j > 0. Optimal choice regarding the intratemporal trade-off
between current consumption and current labor supply yields a labor supply equation:
vℓ(Lt(x), ξt)
uc(Ct, ξt)
= Wt(x)
Pt
.
(29)
Households optimally choose to minimize the cost of attaining the level of consumption Ct. This
implies the following demand curves for each of the differentiated products produced in the econ-
omy:
ct(z) = Ct
pt(z)
Pt
−θ
,
(30)
where pt(z) denotes the price of product z and
Pt =
Z 1
0
pt(z)1−θdz

1
1−θ
.
(31)
39The stochastic discount factor Mt,t+1 is a random variable over states in period t + 1. For each such state it equals
the price of the Arrow-Debreu asset that pays off in that state divided by the conditional probability of that state. See
Cochrane (2005) for a detailed discussion.

H.2
Firms
There are a continuum of ﬁrms indexed by z in the economy. Firm z specializes in the production of
differentiated good z, the output of which we denote yt(z). For simplicity, labor is the only variable
factor of production used by ﬁrms. Each ﬁrm is endowed with a ﬁxed, non-depreciating stock of
capital. The production function of ﬁrm z is
yt(z) = Atf(Lt(z)),
(32)
where At denotes aggregate productivity. The function f is increasing and concave. It is concave
because there are diminishing marginal return to labor given the ﬁxed amount of other inputs em-
ployed at the ﬁrm. We follow Woodford (2003) in introducing heterogeneous labor markets. Each
ﬁrm belongs to an industry x. There are many ﬁrms in each industry. The goods in industry x are
produced using labor of type x and all ﬁrms in industry x change prices at the same time. This
heterogeneous labor market structure is a strong source of real rigidities in price setting.
Firm z acts to maximize its value,
Et
∞
X
j=0
Mt,t+j[pt+j(z)yt+j(z) −Wt+j(x)Lt+j(z)].
(33)
Firm z must satisfy demand for its product given by equation (30). Firm z is therefore subject to the
following constraint:
Ct
pt(z)
Pt
−θ
≤Atf(Lt(z)).
(34)
Firm z takes its industry wage Wt(x) as given. Optimal choice of labor demand by the ﬁrm is
given by
Wt(x) = Atfℓ(Lt(z))St(z),
(35)
where St(z) denotes the ﬁrm’s nominal marginal cost (the Lagrange multiplier on equation (34) in
the ﬁrm’s constrained optimization problem).
Firm z can reoptimize its price with probability 1 −α as in Calvo (1983). With probability α, it
must keep its price unchanged. Optimal price setting by ﬁrm z in periods when it can change its
price implies
pt(z) =
θ
θ −1Et
∞
X
j=0
αjMt,t+jyt+j(z)
P∞
k=0 αkMt,t+kyt+k(z)St+j(z).
(36)
Intuitively, the ﬁrm sets its price equal to a constant markup over a weighted average of current

and expected future marginal cost.
H.3
A Linear Approximation of Private Sector Behavior
We seek a linear approximation of the equation describing private sector behavior around a zero-
growth, zero-inﬂation steady state. We start by deriving a log-linear approximation for the con-
sumption Euler equation that related consumption growth and a one-period, riskless, nominal
bond. This equation takes the form Et[Mt,t+1(1 + it)] = 1, where it denotes the yield on a one-
period, riskless, nominal bond. Using equation (28) to plug in for Mt,t+1 and rearranging terms
yields
Et

βUc(Ct+1, ξt+1) Pt
Pt+1

= Uc(Ct, ξt)
1 + it
.
(37)
The zero-growth, zero-inﬂation steady state of this equation is β(1 + ¯ı) = 1. A ﬁrst order Taylor
series approximation of equation (37) around this steady state is
ˆct = Etˆct+1 −σ(ˆıt −Etˆπt+1) −σEt∆ˆξct+1,
(38)
where ˆct = (Ct −C)/C, ˆπt = πt −1, ˆıt = (1 + it −1 −¯ı)/(1 + ¯ı), and ˆξct = (Uξc/Uc)(ξt −1). The
parameter σ = −Uc/(UccC) denotes the intertemporal elasticity of substitution of households.
We next linearize labor demand, labor supply, and the production function and combine these
equations to get an expression for the marginal costs in period t + j of a ﬁrm that last changed its
price in period t. Let ℓt,t+j(x) denote the percent deviation from steady state in period t+j of hours
worked for workers in industry x that last was able to change prices in period t. Let other industry
level variables be deﬁned analogously. We assume that f(Lt(x)) = La
t (x).
A linear approximation of labor demand—equation (35)—in period t+j for industry x that was
last able to change its prices in period t is then
ˆwt,t+j(x) = ˆat+j −(1 −a)ˆℓt,t+j(x) + ˆst,t+j(x),
(39)
where ˆwt,t+j(x) and ˆst,t+j(x) denote the percentage deviation of real wages and real marginal costs,
respectively, from their steady state values.
A linear approximation of labor supply—equation (29)—in period t + j for industry x that was
last able to change its prices in period t is
ˆwt,t+j(x) = η−1ˆℓt,t+j(x) + σ−1ˆct+j + ˆξℓ,t+j −ˆξc,t+j,
(40)

where ˆξℓ,t+j = (Vℓξ/Vℓ)(ξt −1). The parameter η = Vℓ/(VℓℓL) is the Frisch elasticity of labor supply.
A linear approximation of the production function—equation (32)—in period t + j for industry
x that was last able to change its prices in period t is
ˆyt,t+j(x) = ˆat+j + aˆℓt,t+j(x).
(41)
Combining labor demand and labor supply—equations (39) and (40)—to eliminate ˆwt,t+j(x)
yields
ˆst,t+j(x) = (η−1 + 1 −a)ˆℓt,t+j(x) + σ−1ˆct+j −ˆat+j + ˆξℓ,t+j −ˆξc,t+j.
Using the production function—equation (41)—to eliminate ˆℓt,t+j(x) yields
ˆst,t+j(x) = ωˆyt,t+j(x) + σ−1ˆct+j −(ω + 1)ˆat+j + ˆξℓ,t+j −ˆξc,t+j,
(42)
where ω = (η−1 + 1 −a)/a.
Taking logs of consumer demand—equation (30)—in period t + j for industry x what was last
able to change its prices in period t yields
ˆyt,t+j(z) = −θˆpt(x) + θ
j
X
k=1
ˆπt+k + ˆyt+j,
(43)
where we use the fact that Yt = Ct and yt(x) = ct(x). Plugging this equation into equation (42) and
again using the fact that Yt = Ct yields
ˆst,t+j(x) = −ωθˆpt(x) + ωθ
j
X
k=1
ˆπt+k + (ω + σ−1)ˆyt+j −(ω + 1)ˆat+j + ˆξℓ,t+j −ˆξc,t+j
(44)
It is useful to derive the level of output that would prevail if all prices were ﬂexible. Since our
model does not have any industry speciﬁc shocks (other than the opportunity to change prices),
marginal costs of all ﬁrms are the same when prices are ﬂexible. Firm price setting in this case
yields pt(x) = µSt, where µ = θ/(θ −1). This implies that all prices are equal and that St/Pt = 1/µ.
Since real marginal cost is a constant, we have ˆst = 0. The ﬂexible price version of equation (44) is
then
(ω + σ−1)ˆyn
t = (ω + 1)ˆat −ˆξℓ,t + ˆξc,t,
(45)
where we use the fact that output in all industries is the same under ﬂexible prices and ˆyt = ˆct and

denote the rate of output under ﬂexible prices as yn
t . We will refer to yn
t as the natural rate of output.
Combining equations (44) and (45) yields
ˆst,t+j(x) = −ωθˆpt(x) + ωθ
j
X
k=1
ˆπt+k + (ω + σ−1)(ˆyt+j −ˆyn
t+j)
(46)
We next linearize the price setting equation—equation (36). This yields:
∞
X
j=0
(αβ)j ˆpt(x) −
∞
X
j=0
(αβ)jEtˆst,t+j(x) −
∞
X
j=1
(αβ)j
j
X
k=1
Etˆπt+k = 0.
Manipulation of this equation yields
ˆpt(x) = (1 −αβ)
∞
X
j=0
(αβ)jEtˆst,t+j(x) + αβ
∞
X
j=1
(αβ)j−1Etˆπt+j.
(47)
Using equation (46) to eliminate ˆst,t+j(x) in equation (47) and manipulating the resulting equation
yields
ˆpt(x) = (1 −αβ)ζ
∞
X
j=0
(αβ)jEt(ˆyt+j −ˆyn
t+j) + αβ
∞
X
j=1
(αβ)j−1Etˆπt+j,
(48)
where ζ = (ω + σ−1)/(1 + ωθ).
A linear approximation of the expression for the price index—equation (31)—yields
ˆπt = 1 −α
α
ˆpt(x).
(49)
Using this last equation to replace ˆpt(x) in equation (48) yields
ˆπt = κζ
∞
X
j=0
(αβ)jEt(ˆyt+j −ˆyn
t+j) + (1 −α)β
∞
X
j=1
(αβ)j−1Etˆπt+j,
where κ = (1 −α)(1 −αβ)/α. Quasi-differencing the resulting equation yields
ˆπt −αβEtˆπt+1 = κζ(ˆyt −ˆyn
t ) + (1 −α)βEtˆπt+1,
which implies
ˆπt = βEtˆπt+1 + κζ(ˆyt −ˆyn
t ).
(50)

Finally, we rewrite the household’s Euler equation—equation (38) in terms of the output gap:
ˆyt −ˆyn
t = Et(ˆyt+1 −ˆyn
t+1) −σ(ˆıt −Etˆπt+1 −rn
t ),
(51)
where rn
t denotes the “natural rate of interest” as is given by
rn
t = Et∆ξc,t+1 + 1
σEt∆ˆyn
t+1.
(52)
H.4
Household Behavior with Internal Habits
We now consider a case in which households form habits. Households of type x seek to maximize
a utility function given by
E0
∞
X
t=0
βt[u(Ct −bCt−1) −v(Lt(x))],
(53)
where the parameter b governs the strength of households’ habit. We model household utility from
consumption in period t as being affected by the amount that same household consumed in the
previous period. Our model is therefore a model of “internal habit.” Notice also that relative to the
derivations above, we have eliminated reference to the preferences shocks ξt since they play no role
in the analysis in the body of the paper.
Households face the same budget constraint as in the simple model (equation (27)). They also
face the same no-Ponzi condition as in the simple model. Maximization of utility subject to these
constraints yields the following consumption Euler equation and labor supply equation:
Λt+j
Λt
= Mt,t+j
βj
Pt+j
Pt
,
(54)
vℓ(Lt(x), ξt)
Λt
= Wt(x)
Pt
,
(55)
where Λt denotes marginal utility from consumption at time t and is given by
Λt = uc(Ct −bCt−1) −bβEtuc(Ct+1 −bCt).
(56)
H.5
Firm Price Setting with Inﬂation Inertia
In the simple model presented above, we assume that prices are either reoptimized (with probability
1 −α), or remain ﬁxed (with probability α). As is well-known, this formulation yields a Phillips
curve that implies that inﬂation reacts rapidly to news about future economic developments. Our

empirical evidence suggests that inﬂation responds very gradually to news about future economic
conditions. To be able to match this aspect of our evidence, we now follow Christiano, Eichenbaum,
and Evans (2005) in considering a formulation of price setting in which ﬁrms index the price of the
good they produce to past inﬂation whenever they don’t reoptimize the price. This formulation
makes inﬂation sluggish.
Firm z can reoptimize its price with probability 1 −α as in Calvo (1983). With probability α, it
sets its price according to the following simple rule
pt(z) = Pt−1
Pt−2
pt−1(z).
(57)
The ﬁrm’s optimization problem is otherwise the same as in section H.2. Optimal price setting by
ﬁrm z in periods when it can change its price implies
pt(z) =
θ
θ −1Et
∞
X
j=0
αjMt,t+jyt+j(z)
P∞
k=0 αkMt,t+k(Pt+j−1/Pt−1)yt+k(z)St+j(z).
(58)
The ﬁrm’s labor demand equation is the same as in section H.2.
H.6
A Linearization of Private Sector Behavior in the Augmented Model
We seek a linear approximation of the equations describing private sector behavior with internal
habits and price indexation. As before, we start by deriving a log-linear approximation for the
consumption Euler equation that related consumption growth and a one-period, riskless, nominal
bond. This equation may be written
Et

βΛt+1
Pt
Pt+1

=
Λt
1 + it
.
(59)
The zero-growth, zero-inﬂation steady state of this equation is β(1 + ¯ı) = 1. A ﬁrst order Taylor
series approximation of equation (37) around this steady state is
ˆλt = Etˆλt+1 + (ˆıt −Etˆπt+1),
(60)
where ˆλ = (Λt −Λ)/Λ.
A linear approximation of labor supply—equation (55)—in period t + j for industry x that was

last able to change its prices in period t is
ˆwt,t+j(x) = η−1ˆℓt,t+j(x) −ˆλt+j.
(61)
A linear approximation of marginal utility of consumption—equation (56)—is given by
ˆλt = −(1 + b2β)σcˆct + bσcˆct−1 + bβσcEtˆct+1,
(62)
where σc = −σ−1/((1 −b)(1 −bβ)).
Combining equation (61) with equations (39) (without the preference shock) and equation (41)
yields
ˆst,t+j(x) = ωˆyt,t+j(x) −ˆλt+j −(ω + 1)ˆat+j.
(63)
With price indexation, consumer demand in period t + j in an industry x that last changed its
price in period t is
yt+j(x) =
pt(x)
Pt+j
Pt+j−1
Pt−1
−θ
Yt+j.
(64)
A linear approximation of this equation is
ˆyt,t+j(z) = −θˆpt(x) + θ
j
X
k=1
ˆπt+k −θ
j−1
X
k=0
ˆπt+k + ˆyt+j.
(65)
Plugging this into equation (63) yields
ˆst,t+j(x) = −ωθˆpt(x) + ωθ
j
X
k=1
ˆπt+k −ωθ
j−1
X
k=0
ˆπt+k + ωˆyt+j −ˆλt+j −(ω + 1)ˆat+j.
(66)
As in the simple model considered above, it is useful to derive a relationship between the natural
level of output and marginal cost and the exogenous shocks in the model. With ﬂexible prices all
ﬁrms set the same price. In this case we have pt(x) = µSt and ˆst = 0. This implies that the ﬂexible
price version of equation (66) is
ωˆyn
t+j −ˆλn
t+j = (ω + 1)ˆat+j.
(67)

Combining equations (66) and (67) yields
ˆst,t+j(x) = −ωθˆpt(x) + ωθ
j
X
k=1
ˆπt+k −ωθ
j−1
X
k=0
ˆπt+k + ω(ˆyt+j −ˆyn
t+j) −(ˆλt+j −ˆλn
t+j).
(68)
We next linearize the price setting equation—equation (58). This yields:
∞
X
j=0
(αβ)j ˆpt(x) −
∞
X
j=0
(αβ)jEtˆst,t+j(x) −
∞
X
j=1
(αβ)j
j
X
k=1
Etˆπt+k +
∞
X
j=1
(αβ)j
j−1
X
k=0
Etˆπt+k = 0.
Manipulation of this equation yields
ˆpt(x) = (1 −αβ)
∞
X
j=0
(αβ)jEtˆst,t+j(x) + αβ
∞
X
j=1
(αβ)j−1Etˆπt+j −αβ
∞
X
j=0
(αβ)jEtˆπt+j.
(69)
Using equation (68) to eliminate ˆst,t+j(x) in equation (69) and manipulating the resulting equation
yields
ˆpt(x) = (1 −αβ)ˆζ
∞
X
j=0
(αβ)jEt[ωˆxt+j −ˆλxt+j] + αβ
∞
X
j=1
(αβ)j−1Etˆπt+j −αβ
∞
X
j=0
(αβ)jEtˆπt+j,
(70)
where ˆλxt = ˆλt −ˆλn
t and ˆζ = 1/(1 + ωθ).
A linear approximation of the expression for the price index—equation (31)—in the case with
indexation between price changes yields
ˆπt −ˆπt−1 = 1 −α
α
ˆpt(x).
(71)
Using this last equation to replace ˆpt(x) in equation (70) yields
ˆπt −ˆπt−1 = κˆζ
∞
X
j=0
(αβ)jEt[ωˆxt+j −ˆλxt+j] + (1 −α)β
∞
X
j=1
(αβ)j−1Etˆπt+j −(1 −α)β
∞
X
j=0
(αβ)jEtˆπt+j.
Quasi-differencing this equation yields
(ˆπt −ˆπt−1) −αβ(Etˆπt+1 −ˆπt) = κˆζ(ωˆxt+j −ˆλxt+j) + (1 −α)β(Etˆπt+1 −ˆπt),
which implies
∆ˆπt = βEt∆ˆπt+1 + κˆζ(ωˆxt+j −ˆλxt+j).
(72)

Finally, we rewrite the household’s Euler equation—equation (60) in terms of the marginal util-
ity gap:
ˆλxt = Etˆλxt+1 −σ(ˆıt −Etˆπt+1 −rn
t ),
(73)
where rn
t denotes the “natural rate of interest” as is given by
rn
t = 1
σEt∆ˆλn
t+1.
(74)
H.7
Determination of Natural Rate of Output and Productivity
Since the monetary shock affects private sector beliefs about the path of the natural rate of interest,
it also affects the private sector’s beliefs about the path of the natural rate of output. The solution
to the following equation:
(1 + bβ + b2β)ˆyn
t+1 = bβEtˆyn
t+2 + (1 + b + b2β)ˆyn
t −bˆyn
t−1 + σ−1
c ψ¯rt
(75)
using our assumed initial response for the natural rate of output of yn
0 = ψ¯r0 yields a path for the
natural rate of output that is consistent with the path of the natural rate of interest implied by our
assumption about Fed information, i.e., rn
t = ψ¯rt. This can be veriﬁed by using the resulting path
for the natural rate of output to construct a path for the natural rate of marginal utility according
to equation (62) and then plugging the resulting path for the natural rate of marginal utility into
equation (74). This will yield rn
t = ψ¯rt.
The logic for this construction of the path of the natural rate of output is easier to comprehend
in the textbook New Keynesian model without habit. Suppose rn
t = ψ¯rt and yn
0 = ψ¯r0 in that model
and we are interested in constructing the path for the natural rate of output that is consistent with
these assumptions. The consumption Euler equation in that model implies that ˆyn
t = Etˆyn
t+1 −σψ¯rt.
For this equation to hold, it must be that ˆyn
t+1 = ˆyn
t + σψ¯rt. One can thus construct a path for
the natural rate of output that is consistent with the desired path for the natural rate of interest by
iterating forward ˆyn
t+1 = ˆyn
t + σψ¯rt with the initial condition yn
0 = ψ¯r0. The argument above, is the
equivalent argument when households have internal habit.
Given the path for the natural rate of output that we construct above, one can construct a path
for the response of private sector beliefs about productivity (the exogenous shock that we assume
is driving variation in the natural rate of output and the natural rate of interest) by using equation
(67). In the counterfactual, we assume that agents believe productivity is a random walk and then
feed in a shock process for productivity that makes productivity follow the same path as in the

actual case of the monetary shock.

Table A.1: Response of Interest Rates to Monetary Shocks for Different Sample Periods
Nominal 
Real 
Nominal 
Real 
Nominal 
Real 
Nominal 
Real 
3M Treasury Yield
0.67
0.76
0.73
0.76
(0.14)
(0.13)
(0.15)
(0.11)
6M Treasury Yield
0.85
0.85
0.90
0.91
(0.11)
(0.12)
(0.12)
(0.10)
1Y Treasury Yield
1.00
1.00
1.00
1.00
(0.14)
(0.14)
(0.13)
(0.13)
2Y Treasury Yield
1.10
1.06
1.11
1.04
1.19
1.46
1.30
1.21
(0.33)
(0.24)
(0.36)
(0.24)
(0.29)
(0.39)
(0.37)
(0.26)
3Y Treasury Yield
1.06
1.02
1.03
0.97
1.21
1.34
1.26
1.18
(0.36)
(0.25)
(0.39)
(0.25)
(0.31)
(0.33)
(0.40)
(0.28)
5Y Treasury Yield
0.73
0.64
0.67
0.58
0.78
0.81
0.69
0.68
(0.20)
(0.15)
(0.20)
(0.15)
(0.18)
(0.16)
(0.16)
(0.11)
10Y Treasury Yield
0.38
0.44
0.36
0.44
0.50
0.57
0.38
0.43
(0.17)
(0.13)
(0.18)
(0.13)
(0.17)
(0.16)
(0.13)
(0.10)
2Y Tr. Inst. Forward Rate
1.14
0.99
1.07
0.90
1.31
0.97
1.34
1.15
(0.46)
(0.29)
(0.48)
(0.27)
(0.38)
(0.30)
(0.49)
(0.31)
3Y Tr. Inst. Forward Rate
0.82
0.88
0.66
0.76
1.14
1.09
1.00
1.03
(0.43)
(0.32)
(0.43)
(0.29)
(0.41)
(0.35)
(0.46)
(0.34)
5Y Tr. Inst. Forward Rate
0.26
0.47
0.20
0.47
0.44
0.61
0.27
0.45
(0.19)
(0.17)
(0.19)
(0.16)
(0.21)
(0.21)
(0.13)
(0.12)
10Y Tr. Inst. Forward Rate
-0.08
0.12
-0.01
0.21
0.05
0.10
-0.07
0.04
(0.18)
(0.12)
(0.19)
(0.13)
(0.17)
(0.13)
(0.12)
(0.11)
Each estimate comes from a separate OLS regression. The dependent variable in each regression is the one day change in the variable
stated in the left-most column. The independent variable is a change in the policy news shock over a 30 minute windor around
regularly scheduled FOMC announcements, except the last two columns where we include unscheduled FOMC announcements. The
baseline sample period is 1/1/2000 to 3/19/2014, except that we drop July 2008 through June 2009. The "Pre-Crisis" sample is
January 2000 through December 2007. The "Full Sample" is 1/1/2000 to 3/19/2014. In the last two columns, we exclude a 10 day
period after 9/11/2001. For 2Y and 3Y yields and real forwards, the sample starts in 2004. For each sample period, we construct the
policy new shocks from the same sample of observations as the regressions are run on—that is, the results from the different sample
periods use slightly different policy news shock series. Robust standard errors are in parentheses. 
Baseline Sample
Pre-Crisis (2000-2007)
Full Sample
Baseline w/ Unsched.

Table A.2: Response to a Fed Funds Rate Shock
Nominal 
Real 
Inflation
3M Treasury Yield
0.50
(0.16)
6M Treasury Yield
0.59
(0.10)
1Y Treasury Yield
0.41
(0.16)
2Y Treasury Yield
0.48
0.50
-0.02
(0.32)
(0.20)
(0.15)
3Y Treasury Yield
0.38
0.41
-0.03
(0.34)
(0.19)
(0.18)
5Y Treasury Yield
0.11
0.21
-0.10
(0.16)
(0.12)
(0.09)
10Y Treasury Yield
-0.00
0.10
-0.10
(0.12)
(0.09)
(0.07)
2Y Treasury Inst. Forward Rate
0.29
0.30
-0.01
(0.40)
(0.20)
(0.25)
3Y Treasury Inst. Forward Rate
0.07
0.13
-0.06
(0.34)
(0.19)
(0.22)
5Y Treasury Inst. Forward Rate
-0.09
0.07
-0.16
(0.13)
(0.12)
(0.07)
10Y Treasury Inst. Forward Rate
-0.11
-0.02
-0.08
(0.16)
(0.11)
(0.09)
Each estimate comes from a separate OLS regression. The dependent variable in each regression is
the one day change in the variable stated in the left-most column. The independent variable is a
change in the Fed Funds future over the remainder of the month over a 30 minute window around
the time of FOMC announcements. The sample period is all regularly scheduled meetings from
1/1/2000 to 3/19/2014, except that we drop July 2008 through June 2009. For 2Y and 3Y yields and
real forwards, the sample starts in January 2004. The sample size for the 2Y and 3Y yields and
forwards is 74. The sample size for all other regressions is 106. In all regressions, the policy news
shock is computed from these same 106 observations. Robust standard errors are in parentheses.

Table A.3: Responses to Policy News Shock Using Rigobon Estimator
Nominal 
Real 
Inflation
3M Treasury Yield
0.69
(0.15)
6M Treasury Yield
0.85
(0.12)
1Y Treasury Yield
0.98
(0.15)
2Y Treasury Yield
1.07
1.03
0.05
(0.37)
(0.29)
(0.20)
3Y Treasury Yield
1.03
0.99
0.04
(0.42)
(0.30)
(0.19)
5Y Treasury Yield
0.69
0.62
0.07
(0.22)
(0.16)
(0.12)
10Y Treasury Yield
0.34
0.42
-0.08
(0.19)
(0.14)
(0.09)
2Y Treasury Inst. Forward Rate
1.10
0.96
0.14
(0.51)
(0.34)
(0.25)
3Y Treasury Inst. Forward Rate
0.78
0.86
-0.08
(0.49)
(0.37)
(0.17)
5Y Treasury Inst. Forward Rate
0.22
0.46
-0.24
(0.20)
(0.18)
(0.09)
10Y Treasury Inst. Forward Rate
-0.12
0.11
-0.22
(0.19)
(0.13)
(0.10)
Each estimate comes from a separate "regression." The dependent variable in each regression is the one day
change in the variable stated in the left-most column. The independent variable is a change in the policy news
shock over a 30 minute window around the time of FOMC announcements. All results are based on Rigobon's
(2003) method of identification by heteroskedasticity. The sample of "treatment" days for the Rigobon method is
all regularly scheduled FOMC meeting days from 1/1/2000 to 3/19/2014—this is also the period for which the
policy news shock is constructed in all "regressions." The sample of "control" days for the Rigobon analysis is all
Tuesdays and Wednesdays that are not FOMC meeting days over the same period of time. In both the treatment
and control samples, we drop July 2008 through June 2009 and 9/11/2001-9/21/2001. For 2Y forwards, the
sample starts in January 2004. Standard errors are calculated using a non-parametric bootstrap with 5000
iterations. 

Table A.4: Breakeven Inﬂation versus Inﬂation Swaps
Breakeven
Swaps
Inflation Over Next 2 Years
-0.02
0.37
(0.18)
(0.35)
Inflation Over Next 3 Years
-0.03
0.41
(0.17)
(0.32)
Inflation Over Next 5 Years
-0.13
-0.02
(0.14)
(0.15)
Inflation Over Next 10 Years
-0.22
-0.17
(0.12)
(0.16)
Each estimate comes from a separate OLS regression. The dependent variable in each regression is
the one day change in expected inflation measured either by breakeven inflation from the difference
between nominal Treasuries and TIPS (first column) or from inflation swaps (second column) for
the period stated in the left-most column. The independent variable is a change in the policy new
shock over a 30 minute window around the time of FOMC announcements, where the policy news
shocks are constructed on the 2000-2014 sample used in Table 1. The sample is all regularly
scheduled FOMC meeting day from 1/1/2005 to 11/14/2012, except that we drop July 2008 through
June 2009. Robust standard errors are in parentheses.

Table A.5: Response of Expected Output Growth
Exp. Output Growth in Current Qr
1.38
(0.72)
Exp. Output Growth 1 Qr Ahead
1.56
(0.54)
Exp. Output Growth 2 Qr Ahead
0.66
(0.37)
Exp. Output Growth 3 Qr Ahead
0.82
(0.27)
Exp. Output Growth 4 Qr Ahead
0.51
(0.25)
Exp. Output Growth 5 Qr Ahead
0.54
(0.28)
Exp. Output Growth 6 Qr Ahead
0.48
(0.25)
Exp. Output Growth 7 Qr Ahead
0.90
(0.57)
Each estimate comes from a separate OLS regression. We regress changes in survey expectations
from the Blue Chip Economic Indicators on the policy news shock. Since the Blue Chip survey
expectations are available at a monthly frequency, we construct a corresponding monthly measure of
our policy news shock. In particular, we use any policy news shock that occurs over the month except
for those that occur in the first week (because we do not know whether these occurred before or after
the survey response). The dependent variable is the change in the forecasted value of output growth
N quarters ahead, between this month's survey and last month's survey. See Appendix F for details.
The sample period is all regularly scheduled FOMC meetings between January 1995 to April 2014,
except that we drop July 2008 through June 2009 and the aforementioned first-week meetings. The
policy news shock is constructed on the same sample period. Sample sizes are 120 for the first five
rows, then 75, 45, and 13. Robust standard errors are in parentheses.