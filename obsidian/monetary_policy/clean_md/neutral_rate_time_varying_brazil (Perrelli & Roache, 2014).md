WP/14/84
Time-Varying Neutral Interest
Rate—The Case of Brazil
Roberto Perrelli and Shaun K. Roache

IMF Working Paper
Strategy, Policy, and Review and Monetary and Capital Markets Departments
Time-Varying Neutral Interest Rate—The Case of Brazil
Prepared by Roberto Perrelli and Shaun K. Roache1
Authorized for distribution by Thanos Arvanitis and Matthew Jones
May 2014
This Working Paper should not be reported as representing the views of the IMF.
The views expressed in this Working Paper are those of the author(s) and do not necessarily
represent those of the IMF or IMF policy. Working Papers describe research in progress by the
author(s) and are published to elicit comments and to further debate.
Abstract
Emerging markets have experienced a sizeable decline in their neutral real interest rates
until recently. In this paper we try to identify the main factors that contributed to it, with a
focus on Brazil. We estimate an interval for Brazil’s time-varying neutral rate based on a
range of structural and econometric models. We assess the implications of incorrectly
estimating a time-varying neutral rate using a small structural model with a simple
monetary policy instrument rule. We find that policy prescriptions are very different when
facing uncertainty of neutral rate and of output gap. Our result contrasts sharply with
Orphanides (2002), suggesting that the best response to neutral rate uncertainty is to
ensure policy remains highly sensitive to inflation and output variations.
JEL Classification Numbers: E1; E4; E5
Keywords: Natural rate of interest; small monetary model; inflation targeting regime.
1 We would like to express our special thanks to Andrew Berg and Miguel Savastano for their insightful
comments and strong support to pursue this research. Vikram Haksar offered superb guidance in the early days
of this project. Marcos Chamon, Olivier Basdevant, Mercedes Garcia-Escribano, and Tommaso Mancini
Griffoli, along with seminar participants at the Brazilian National Treasury, Brazilian Central Bank, and the
IMF, added tremendous value to the discussion in this paper. The usual disclaimers apply.

Contents Page
I. Introduction ................................................................................................................... 4
II. Stylized Facts About Neutral Rates in Emerging Markets ........................................... 5
III. A Brief Review of the Literature on Estimating Neutral Rates ................................... 7
IV. Structural Estimates of the Neutral Real Interest Rate in Brazil .................................. 8
V. Econometric Estimates of Neutral Rate in Brazil ....................................................... 11
A. Statistical Filters ............................................................................................... 11
B. Yield Curve Models ......................................................................................... 13
C. State Space Models .......................................................................................... 15
D. Fundamentals-based Regression Models ......................................................... 16
VI. Insights From a Small Monetary Model ..................................................................... 22
VII. Concluding Remarks ................................................................................................... 28
Tables
1. Estimates of the Neutral Rate Based on Consumption Models .................................. 11
2. Emerging Markets: Estimates of the Ex-Post Neutral Rate From Statistical Filters .. 12
3. State Space Estimates of the Neutral Real Interest Rate, 2006–13 ............................. 15
4. Determinants of Long-Run Equilibrium Real Interest Rate, 2003–13 ....................... 19
5. Determinants of Short-Run Equilibrium Real Interest Rate, 2005–13 ....................... 20
Figures
1. Emerging Markets: Declines in Neutral Real Interest Rates, 2005–13 ........................ 6
2. Emerging Markets: PCA Decomposition of Real Policy Rates, 2002–13 .................... 7
3. Filter-based Real Policy Rate and Real Interest Gap, 2003–13 .................................. 13
4. Slope of the Yield Curve, 2006–13............................................................................. 14
5. Neutral Real Interest Rate Based on State Space Model, 2006–13 ............................ 16
6. Determinants of Long-Run Equilibrium Real Interest Rate, 2005–13 ....................... 18
7. Inflation Surprise and Inflation Gap, 2005–13 ........................................................... 18
8. Short- and Long-Run Equilibrium Real Interest Rates, 2005–13 ............................... 21
9. Small Model: Scenarios for Neutral Rates .................................................................. 24
10. Falling Neutral Real Interest Rates in a Small Monetary Model: Scenarios .............. 25
11. Scenario 3: Actual Real Interest Rate Gaps Under Different Policy Rules ............... 26
References ............................................................................................................................... 29

I. INTRODUCTION
Knut Wicksell (1898) was probably the first economist to try and define the neutral real
interest rate (henceforth the “neutral rate”). His interpretation was that “[it] is a certain rate of
interest on loans which is neutral in respect to commodity prices, and tends neither to raise
nor lower them.” The profession still thinks of the neutral rate in a similar way as the interest
rate consistent with output at potential and inflation remaining stable. This is not just a
theoretical curiosity; the neutral rate is an important operational benchmark against which to
measure the stance of monetary policy, playing a pivotal function in some rules-based
regimes (Laubach and Williams, 2003).
Policymakers that use some concept of the neutral rate in setting policies face considerable
challenges, however. First, the neutral rate cannot be seen nor measured and instead has to be
estimated, often with a low degree of confidence. Second, while often thought to reflect slow
moving structural factors, notably saving and investment behavior over the medium- to long-
run, neutral rates can and do change. In particular, emerging market economies undergoing
rapid structural change may experience large shifts in the neutral rate, further complicating
their use as a benchmark for monetary policy.
Our definition of the neutral rate in this paper is based on the nominal policy rate or the
targeted interest rate—for some countries, the overnight interbank rate—deflated by expected
inflation. In other words, we typically focus on the neutral “ex-ante” short-term real rate,
recognising that that there is likely to be something of a maturity mismatch between an
overnight interest rate and inflation expectations that are often expressed for the coming
12 months. 2 It is possible to think of the neutral rate as a short-, medium- or long-run
concept (Archibald and Hunter, 2001). We define the neutral rate here to be invariant to both
the cycle and factors that do not alter long-term saving and investment patterns. As such, we
consider it to be a slow moving benchmark against which to set monetary policy through the
business cycle.
In this paper, we infer some stylized facts about neutral rates across a large sample of
emerging markets and identify factors that may have caused their decline. Our analysis has a
broad focus, but we highlight the challenges facing Brazil, which has experienced one of the
largest decreases in the neutral real interest rate over the last decade—due to both domestic
and external reasons—but continues to present one of the highest rates of interest among
emerging market economies. In particular, we identify an interval for Brazil’s neutral rate
based on a range of structural and econometric models. Our innovation is to contrast these
approaches and discuss their suitability for an economy undergoing rapid structural changes.
A second contribution is to assess the implications of incorrectly estimating a time-varying
neutral rate using a small structural model with a simple monetary policy instrument rule.
This is a topic that has attracted scant attention in the literature, with much of the focus
previously turned to uncertainty regarding potential output (e.g. Erhmann and Smets, 2003)
2 For a few emerging markets, the paucity of data requires the use of actual (instead of expected) inflation.

or the natural rate of unemployment. We recognise that neutral rates and potential output
growth are linked, but we find that the policy prescriptions are very different when facing
uncertainty of either variety.
The plan of this paper is as follows: Section II highlights some stylized facts about the
declining neutral rates in emerging markets. Section III offers a concise review of the
relevant literature. Section IV presents estimates of the neutral real interest rate from
consumption-based models calibrated for Brazil. Section V explores several econometric
techniques used to generate time-varying estimates of Brazil’s neutral real interest rate. To
assess whether these estimates are consistent with theory, section VI compares them to those
from Section IV and discusses the implications for monetary policy based on a small macro
model calibrated for Brazil. Concluding remarks are provided in section VII.
II. STYLIZED FACTS ABOUT NEUTRAL RATES IN EMERGING MARKETS
Actual real interest rates are typically thought to fluctuate around the unobservable neutral
rate—i.e., the real interest rate compatible with a closed output gap and with stable inflation.
In this section, we use this assumption to infer some facts about neutral rates in emerging
markets, in terms of how they might have changed, how they co-move, and what might be
the common factors that explain such comovement. We use the terms “trend rate” and
“neutral rate” interchangeably in this section.
Our first observation is that neutral rates appeared to decline across most emerging markets
(henceforth “EMs”) between 2002 and 2011. This is suggested by the steady drop in trend
real policy rates (henceforth “trend rates”) obtained from the application of statistical filters.
In Figure 1 (left panel), the trend is filtered from nominal policy interest rates deflated by
prevailing consumer price inflation—hence, this is by construction an “ex post” proxy for the
neutral rate that allows us to use a larger sample of countries (some of which do not have a
long history of inflation expectation surveys). Brazil’s trend rate has dropped near 500 basis
points (bps) between 2010 and 2013 compared with the average of the previous 4-year
period. The only country with a larger drop in the sample was Turkey (around 800 bps).
After reaching near 10 percent during the currency crisis of 2002–03, Brazil’s strong track
record of macroeconomic stabilization, underpinned by successful inflation targeting and
fiscal policy frameworks, have surely played a key part in allowing trend rates to fall
substantially, including by reducing sovereign risk premia and raising domestic savings.
Notwithstanding this sizeable decline, Brazil’s trend real rate remains the highest in our EM
sample. This is illustrated in the right panel of Figure 1, which plots the level of the trend real
rate (2010–13 average, in percent) against the change in the trend real rate between the two
four-year periods surrounding the global financial crisis (2005–08 vs. 2010–13).
Assuming less than perfect global financial integration, trend real rates in EMs should be
determined, in part, by domestic factors, including saving and investment demand, as well as
the level of the “world neutral rate” which reflects common factors like “excess” global

savings and unconventional monetary policies in the US and Europe.3 To disentangle these
effects, we carried out a principal components decomposition of actual (i.e., unfiltered) de-
meaned real short-term interest rates for the countries in our sample and find that two factors
explain about 45 percent of the common variation in real rates.
Figure 1. Emerging Markets: Declines in Neutral Real Interest Rates, 2005–13 1/
(In basis points, based on Hodrick-Prescott trend real policy rates)
200 200
4 4
100 Average 2010-2013 minus average 2005-2008 100 Brazil Trend real rates
(y-axis, in percent)
0 0 3 China 3
-100 -100 2 Philippines 2
-200 -200 Hungary Chile
-300 -300 1 Mexico Pola C n P o d e lo ru mb T i a a iwan R M I u n a s d l s a o i y a n s e ia sia 1
-400 -400 0 Change in trend real rates South Africa Korea Uruguay 0
-500 -500 (x-axis, in basis points) Israel Thailand
Egypt
-600 -600 -1 -1
-700 -700 Turkey Czech Rep
-2 -2
-800 -800
-900 -900 -3 India -3
ye kruT lizarB o cixe M a id n I le arsI acirfA h tu o d n a lo P a ib m o lo C p eR h ce zC a ero K se n ip p ilih P u reP yrag n u H n aw iaT a n ih C d n a lia h T tp yg E a isya la M a ise n o d n I ya u g u rU a issu R e lih C -4 -900 -800 -700 -600 -500 -400 -300 -200 -100 0 100 200 -4
S
Sources: Thomson Datastream, Haver, and authors’ calculations
1/ For Turkey, the neutral rate is based on overnight rates until May 2010, and on 1-week repo rates afterwards.
Figure 2 shows the extracted principal components (PCs), with the first PC—accounting for
about ¼ of the common variance and labeled as the “common trend”—showing a clear
declining tendency between 2002–10 indicative of global factors exerting persisting
downward pressure on emerging market interest rates. This common trend component has
been broadly stable since 2010. The second PC accounted for a further 1/ of variance and
5
appears to be cyclical as it shows a tendency to fluctuate around zero. This “common cycle”
component declined during 2011–12 but started rising during Q2 2013 at about the same time
that markets began to price-in an unwinding by the the U.S. Federal Reserve of quantitative
easing.4 This suggests that, while domestic factors surely play a role in neutral rate formation
in emerging markets, common global factors, both trend and cyclical, are likely to have
exerted an important influence in recent years.
We conclude from this statistical overview that neutral real interest rates did indeed decline
substantially, particularly between 2002–11. Country-specific explanations may account for
declines in many cases, but common global factors have also contributed importantly to this
outcome. These common factors have been both persistent and transient, with cyclical factors
3 Gourinchas and Jeanne (2012) argue that the excess demand for safe assets has resulted in a decline in the
world neutral real interest rate.
4 Perrelli, Roache, and Góes (2014) discuss the impact of the tapering tantrum on the slope of the yield curves
of emerging market economies.

appearing to have been more important recently. However, these mechanical approaches can
only bring us so far in helping us understand how and why neutral rates may have changed
and what, as a consequence, might be the implications for monetary policy. In the next
section, we briefly survey the existing literature to provide the foundation for a more
comprehensive analytical framework.
Principal Components of EM Real Interest Rates
Figure( 2n.o Ermmaelrizgeidngw Mitha rstkaentsd:a PrdC dAe vDiaectioomn p=o 1si)tion of Real Policy Rates, 2002–13 1/
(normalized with standard deviation = 1)
PC1 - 'common trend'
4
PC2 - 'common cycle'
3
Average demeaned real interest rate
2
1
0
-1
-2
-3
-4
-5
2002 2004 2006 2008 2010 2012
Source: Authors' calculations.
Sources: Thomson Datastream, Haver, and authors’ calculations
1/ Calculated from a sample of 17 emerging markets that had
1/ Calculated from a sample of 17 emerging markets that had available real ex-post overnight interbank interest rate data
available real interest rate data from January 2001 - September 2012.
from January 2001-December 2013.
III. A BRIEF REVIEW OF THE LITERATURE ON ESTIMATING NEUTRAL RATES
Notwithstanding Wicksell’s (1898) seminal theoretical work and the pivotal role played by
the neutral rate in Taylor’s (1993) celebrated monetary policy rule, the econometric literature
on this topic has flourished only recently.
Early estimates of the U.S. neutral rate date back to Bonfim (1997, 2001), and Kozicki and
Tinsley (2001)—the latter based on forward rates from U.S. Treasury bonds. Laubach and
Williams’ (2003) Kalman filtered estimates of the U.S. neutral rate spurred widespread
applications of statistical filters and state space models among central banks, while
highlighting the inherent statistical uncertaintites from these approaches. Tao (2005)
provided real time estimates for the U.S. neutral rate. An early review of these methods is
presented in Giammarioli Valla (2004). Basdevant, Björksten, and Karagedikli’s (2004)
insightful approach combines the slope of the yield curve with a state space framework to
estimate New Zealand’s neutral interest rate. Bernhardsen and Gerdrup (2007) discusses the

estimation of short- and long-run equilibrium interest rates on the determination of the
Norwegian neutral rate.5
For Brazil, Miranda and Muinhos (2003) and Muinhos and Nakane (2006) provide early
estimates of the neutral rate, while Neto and Portugal (2009) consider the intial years of the
inflation target regime (1999–2005) —a period marked by elevated economic and financial
volatility, very high nominal interest rates, widespread indexation of wages and contracts,
and developing inflation expectations surveys. Since then the Brazilian economy has changed
substantially, and so did its neutral interest rate. Perrelli (2012) provides an early attempt to
model Brazil’s neutral real interest rate in the post-global financial crisis era.
Several academic works have attempted to explain Brazilian persistently high levels of
interest rates. Arida, Bacha, and Resende (2005), Gonçalves, Holland, and Spacov (2007),
and Bacha, Holland, and Gonçalves (2009), worked with the hypothesis that jurisdictional
uncertainty on long term contracts has led to high interest rates—to certain extent, as a
substitute for dollarization—in the Brazilian economy. Barbosa (2006) highlights the role of
public indebtedness, while Segura-Ubiergo (2012) discusses the low level of domestic
savings as one of the key factors behind Brazil’s high interest rates.
IV. STRUCTURAL ESTIMATES OF THE NEUTRAL REAL INTEREST RATE IN BRAZIL
In this section, we use structural models to assess Brazil’s neutral real interest rate. Our
estimates are based on the calibration of the first-order condition for optimal inter-temporal
consumption of a representative agent. Our calibrations use Brazil’s actual growth rate of per
capita income and its volatility, along with a range of behavioral parameters typically
adopted in this literature. One important source is Issler and Piqueira (2000) which provides
estimates of behavioral parameters in the problem of consumption optimization in Brazil,
using different types of utility functions.
We begin by assuming that the representative individual has a constant relative risk aversion
(CRRA) utility function given by:
with (1)
where C is per capita consumption, γ is the coefficient of relative risk aversion, and t is a
time indicator. The consumer maximizes her lifetime utility discounting future consumption
by β, subject to a budget constraint where financial assets B grow as a function of per capita
income (Y), consumption (C), and the real return on assets (1+r):
5 Applications to Latin American countries include Fuentes and Gredig (2008) and Magud and Tsounta (2012).

(2)
In the steady state, for all t such that the first order condition can be rewritten simply
as
(3)
As equation (3) suggests, the first order condition can be written in terms of the steady state
growth rate of per capita income (g), since . Assuming log normal g, the
Euler equation can be approximated as follows:
(4)
where r* is the neutral rate and var(g) is the variance of per capita growth.
Equation (4) indicates a positive relationship between the neutral rate and the expected rate
of growth of per capita income, consistent with the stylized fact that trend interest rates in
advanced economies are lower than in faster growing emerging markets. But while
estimating and is a relatively easy task, pinning down values for behavioral
parameters like β and γ in rapidly changing emerging markets is more challenging and
subject to considerable uncertainty.
In the case of Brazil, we consider the average growth rate of per capita income in two sub-
periods (2005-2008 versus 2010-2013), estimated respectively at 3.5 percent and 2.5 percent
per annum. We also compute the standard deviation of the per capita income growth for the
two sub-periods, which printed 1.4 percent and 2.8 percent, respectively, highlighting the
higher volatility of the recent period. For the discount factor β we use values typically
adopted in the calibration of Ramsey models—in the range of 0.97 to 0.99—and also used in
the literature of other emerging markets (e.g., Fuentes and Gredig (2008) uses a similar
approach for the case of Chile). For risk aversion γ, the literature suggests a value in the
range of 1 to 2. This exercise then suggests a neutral rate in a wide percent range, which
averaged across parameters yields a NRIR of about 7¼ percent for the period 2005-2008 and
5¾ percent for the 2010–13 years (Text Tables).

Brazil: NRIR from consumption model, 2005-2008 Brazil: NRIR from consumption model, 2010-2013
\gamma \gamma
\beta 1.0 1.5 2.0 Avg \beta 1.0 1.5 2.0 Avg
0.970 6.5 8.3 10.0 8.3 0.970 5.5 6.7 7.9 6.7
0.975 6.0 7.8 9.5 7.8 0.975 5.0 6.2 7.4 6.2
0.980 5.5 7.2 9.0 7.2 0.980 4.5 5.7 6.9 5.7
0.985 5.0 6.7 8.5 6.7 0.985 4.0 5.2 6.4 5.2
0.990 4.5 6.2 8.0 6.2 0.990 3.5 4.7 5.8 4.7
Avg 5.5 7.3 9.0 7.2 Avg 4.5 5.7 6.9 5.7
Per capita growth (2005-2008): 3.5% Per capita growth (2010-2013): 2.5%
Std dev of pc growth (2005-2008): 1.4% Std dev of pc growth (2010-2013): 2.8%
If consumer behavior is subject to habit persistence, then our estimates of the neutral rate
may need to be lowered. The intuition is that consumption today is determined, in part, by
consumption in past periods; in other words, consumption may be a slow-moving process
(see Fuhrer (2000)). To satisfy (4), which predicts rising consumption in line with per capita
income growth, the real interest rate needs to be higher to encourage consumers to save more
in the current period and consume more in the future. This consideration may be particularly
relevant for Brazil where historically high real interest rates would imply implausibly
impatient (small β) and/or very risk averse households (large γ) in equation (4). Hence we
incorporate habit persistence through the parameter θ in the first-order condition:
γ (5)
We estimate (5) for Brazil using the same parameters as above and calibrate the coefficient
of habit formation θ to roughly approximate the estimates of the trend real interest rate from
the statistical filters discussed above, as a proxy for the neutral real interest rate. This results
in a habit parameter (θ) of about 0.97 for the period 2010-2013, compared to a habit
parameter close to one for the former period.6 This model suggests that a decline in habit
persistence may have played some role in lowering neutral rate, although it cannot fully
explain the decline in Brazil’s neutral real interest rate between these two periods. Under
such framework, the neutral real interest rate ranges between 3 and 7 percent, with an
average of 5 percent—very close to the empirical findings discussed next (Text Tables).
6 Note that when approaches one, the impact of habit formation on the CRRA utility function vanishes, and
this model delivers a NRIR of approximately 7¼ percent—similar to the case we presented earlier. Therefore,
the trend rate experienced by Brazil in 2005-2008 (8¾ percent) cannot be fully explained by habit persistence.

Brazil: NRIR from consumption with habit, 2005-2008 Brazil: NRIR from consumption with habit, 2010-2013
\gamma \gamma
\beta 1.0 1.5 2.0 Avg \beta 1.0 1.5 2.0 Avg
0.970 6.5 8.2 9.9 8.2 0.970 4.0 4.5 5.0 4.5
0.975 6.0 7.7 9.4 7.7 0.975 3.5 4.0 4.5 4.0
0.980 5.5 7.2 8.9 7.2 0.980 3.0 3.5 4.0 3.5
0.985 5.0 6.7 8.4 6.7 0.985 2.5 3.0 3.5 3.0
0.990 4.5 6.2 7.9 6.2 0.990 2.0 2.5 3.0 2.5
Avg 5.5 7.2 8.9 7.2 Avg 3.0 3.5 4.0 3.5
Per capita growth (2005-2008): 3.5% Per capita growth (2010-2013): 2.5%
Coefficient of habit formation: 0.999 Coefficient of habit formation: 0.970
Structural consumption models are appealing in the sense that they provide a solid bridge
between theory and practice and deliver somewhat plausible results for Brazil. These models
can also inform important policy discussions regarding economic growth in emerging
economies—faster growth is expected to be matched by higher neutral rates unless
behavioral changes provide offseting effects. In turn, this is related to the patterns of saving
and investment— neutral rates in low-saving countries (such as Brazil, Turkey, and South
Africa) are typically higher than in high-saving peers (like Indonesia and Malaysia).
Therefore, increasing household savings in Brazil would contribute to a lower neutral rate.
Table 1. Brazil: Estimates of the Neutral Rate Based on Consumption Models
Model Average 2005–08 Average 2010–13
Basic CRRA utility function (Ramsey) 7¼ percent 5¾ percent
CRRA utility with habit formation 7¼ percent 3½ percent
Source: Authors’ calculations
Last, but not least, the careful calibration of consumption models can deliver results close to
those found empirically through the application of model-free methods, such as statistical
filters, as we discuss in the next section.
V. ECONOMETRIC ESTIMATES OF NEUTRAL RATE IN BRAZIL
One important drawback of the structural models explored in the previous section is that their
key parameters are not directly observable, while estimates are often subject to considerable
uncertainty. An alternative approach is to apply a range of econometric techniques to
evaluate the likely range for neutral rates across a sample of emerging markets and over time,
with a particular focus on Brazil.
A. Statistical Filters
Standard filters are useful for disentangling the real interest rate cycle from its secular trend.
We apply a range of filters—including the Hodrick-Prescott, Ravn-Uhlig, and Christiano-
Fitzgerald time-varying filters—to the ex-post real interest rates in a sample of 24 emerging

markets. Table 2 presents the average from these filters for each country, and contrasts the
rates across different sub-periods.
A simple average of the neutral real interest rates for this sample suggests a drop of more
than 200 basis points, from about 2.9 percent early in the previous decade to approximately
¾ percent in the four-year period after the global financial crisis. For Brazil, specifically,
neutral rates have declined significantly during the sample period, from an average
9¼ percent to an average of 3½ percent—a 575 basis points decline. In spite of this
remarkable progress towards international standards, Brazil so far remains with the highest
neutral real interest rate in our sample of emerging markets (Figure 3).
Table 2. Emerging Markets: Estimates of the Ex-Post Neutral Rate from Statistical Filters
Change from 2002-2004 to
Country 2002-2004 2005-2008 2010-2013 2010-2013 (in basis points)
Brazil 9.3 8.8 3.5 -575
Chile 0.8 0.4 1.7 89
China 4.3 2.8 2.8 -150
Colombia 0.1 2.1 1.2 101
Czech Rep 1.2 -0.5 -1.4 -259
Egypt 4.9 -0.7 -0.6 -552
Hungary 3.8 2.3 1.8 -204
India n.a. -0.3 -2.9 n.a.
Indonesia 2.0 0.1 0.9 -113
Israel 3.9 2.1 -0.4 -425
Korea 0.7 1.0 0.1 -57
Malaysia 0.6 0.1 0.8 19
Mexico 2.2 3.2 0.5 -176
Pakistan 3.2 -0.3 1.1 -212
Peru -0.1 1.5 0.7 80
Philippines n.a. 2.9 2.1 n.a.
Poland 4.7 2.1 0.8 -386
Russia 3.7 0.3 1.1 -255
South Africa 4.5 2.7 0.3 -422
Taiwan 1.3 0.8 0.6 -69
Thailand -0.1 -0.3 -0.3 -16
Turkey 6.8 6.5 -1.6 -840
Ukraine 3.2 -4.4 3.1 -5
Uruguay n.a. -0.5 0.3 n.a.
Simple EM Average 2.9 1.4 0.7 -211
Sources: Haver and authors’ calculations

Figure 3. Brazil: Filter-based Real Policy Rate and Real Interest Gap, 2003–13
(In percent; gap equals actual minus trend real rate; negative gap implies monetary easing)
5 16
Gap (Selic deflated by expected inflation minus HP trend, left axis)
Hodrick-Prescott trend of Selic deflated by expected inflation (right axis)
4
Ravn-Uhlig trend of Selic deflated by expected inflation (right axis) 14
3 Christiano-Fitzgerald trend of Selic deflated by expected inflation (right axis)
12
2
10
1
0 8
-1
6
-2
4
-3
2
-4
Turning point
-5 0
Sources: BCB Focus Survey, Thomson Datastream, Haver, and authors’ calculations
There are two main drawbacks to estimating neutral rates using statistical filters. Most filters
are unable to reliably disentangle permanent (or very persistent) and temporary fluctuations.
In the case of interest rates, the filtered trend may be identifying extended cyclical variation
that may not be driven by an underlying structural shift in saving-investment balances,
potential output growth, or consumer preferences. Additional information and structure may
be required to identify such cases, including, for example, the behavior of inflation. A second
issue is that many two-sided filters suffer from end-point bias, which serves only to reinforce
the effect of the current period’s actual interest rate—which may be strongly affected by
cyclical conditions—on estimates of the neutral. For these reasons we present a range of
alternative econometric methods in the following sub-sections.
B. Yield Curve Models
Interest rates at different maturities across the yield curve add more information to the
estimation process, particularly by incorporating market expectations of the path of short-
term rates.With “well-anchored” inflation expectations, the average slope of the yield curve
should mainly reflect the term premium. When computed over a sufficiently long horizon
and between cyclically-equivalent end-points, the average term premium can be considered
neutral with respect to the business cycle.7
7 For further discussion, see for example Basdevant et al, 2004.

Yields on Brazil’s long-term 10-year local currency sovereign bonds and short-term 3-month
interest rates (extracted from swap contracts) have trended lower during most of the sample
period. We estimate the average term premium in Brazil during 2006–13, i.e. the difference
in yields between long-term bonds and short-term swaps—to be about 140 basis points with
significant cyclical variation (Figure 4).
In this framework, a proxy for the NRIR can be backed out by adding the “excess” term
premium—defined as the current term premium minus the sample average—to the trend real
short-term interest rate. In the second half of 2013, for example, the trend real interest rate in
Brazil floated around 3.4 percent, while its “excess” term premium averaged 110 basis
points. Hence, this approach suggests an estimate of Brazil’s neutral real interest rate around
4½ percent during that reference period.
Figure 4. Brazil: Slope of the Yield Curve, 2006–13
(Yields in percent; slope of the yield curve in basis points)
500 18
400 16
300 14
200 12
100 10
0 8
Slope (term premium, left axis)
-100 Average slope (2006-2012, left axis) 6
ST yield (DI swap 3-month, right axis)
LT yield (DI swap 10-year, right axis)
-200 4
ra
M
- n
u
-
J
p
e S
- c
e D
- ra
M
- n
u
-
J
p
e S
- c
e D
- ra
M
- n
u
-
J
p
e S
- c
e D
- ra
M
- n
u
-
J
p
e S
- c
e D
- ra
M
- n
u
-
J
p
e S
- c
e D
- ra
M
- n
u
-
J
p
e S
- c
e D
- ra
M
- n
u
-
J
p
e S
- c
e D
- ra
M
- n
u
-
J
p
e S
- c
e D
-
Sources: BCB, Thomson Datastream, Haver, and authors’ calculations
This methodology relies on the identification of cyclically-neutral positions to anchor the
computation of the average term premium, which may be difficult to verify in such a short
sample period. Given the the limited experience of emerging market economies with the
duration of business cycles under inflation target regimes, the results are subject to elevated
uncertainty.8 Another complicating factor is the possibly sizeable divergence between market
participants’ expectations for the path of interest rates extracted from surveys (e.g. Brazil’s
central bank’s Focus survey) and the path priced in futures contracts.
8 Moreover, there is also some potential circularity in this approach as the term structure of the interest rate
could, in principle, reflect market expectations about future monetary policy decisions—for instance, when
futures contracts on interest rate swaps “price in” hikes on policy rates throughout the medium term.

C. State Space Models
The state space framework is well-suited to estimating neutral rates since they explicitly take
account of the existence of latent variables. In the most simple application, it is assumed that
short-term and long-term nominal interest rates are determined by a common unobservable
time-varying neutral rate, inflation expectations, and idiosyncratic shocks. The long-term rate
is also explained by a term premium.
We apply this approach to Brazil by estimating a system of four equations: two signal
(observable) equations, and two state (latent) equations. The signal equations for the short-
term rate (6) and the long-term rate (7) are estimated as functions of the 12-month ahead
expected inflation , Brazil’s output gap , the 3-month ) and 10-
year ) yields on U.S. Treasury securities (to capture interest rate parity issues), the
Brazilian 5-year CDS ) spreads (as a gauge for shifts in sovereign risks), and the
neutral real interest rate . The output gap is calculated as as the difference between the
central bank’s Economic Activity Index (IBC-Br)—a high-frequency real-time gauge of
GDP—and an estimate of its trend using a standard filter. We use the yields on Brazil’s 10-
year local currency sovereign bonds for the long-term interest rate and the 3-month swap rate
for the short-term rate. We also control for the time-varying term premium in the long-
term rate equation:
(6)
(7)
State equation (8) models r* as a random walk, while state equiation (9) assumes the term
premium follows a stationary AR(1) process with a drift:
(8)
(9)
A Kalman filtered neutral rate calculated from the estimates of this model (Table 3 and
Figure 5) has declined over the past decade, albeit with significant cyclical variation, ranging
between 3 and 5 percent over the last two years. The model estimates are determined mainly
by expected inflation, long-term U.S. Treasury yields, and Brazil’s CDS spreads:
Table 3. Brazil: State Space Estimates of the Neutral Real Interest Rate, 2006–13
Signal Expected Output gap U.S. 3-month U.S. 10-year CDS spreads
equation: inflation yields yields
Short-term rate 0.721 0.028 0.112
(0.24)*** (0.04) (0.14)
Long-term rate 1.421 0.779 0.490
(0.56)*** (0.22)*** (0.17)***
Sources: BCB, Thomson Datastream, Haver, and authors’ calculations
1/ Standard errors in parenthesis: * significant at 10 percent; ** significant at 5 percent; and *** significant at 1 percent.

Figure 5. Brazil: Neutral Real Interest Rate based on State Space Model, 2006–13
(In percent)
14 14
NRIR from state space model
12 12
10 10
8 8
6 6
4 4
2 2
ra
M
- n
u
-
J
p
e S
- c
e D
- ra
M
- n
u
-
J
p
e S
- c
e D
- ra
M
- n
u
-
J
p
e S
- c
e D
- ra
M
- n
u
-
J
p
e S
- c
e D
- ra
M
- n
u
-
J
p
e S
- c
e D
- ra
M
- n
u
-
J
p
e S
- c
e D
- ra
M
- n
u
-
J
p
e S
- c
e D
- ra
M
- n
u
-
J
p
e S
- c
e D
-
Sources: BCB, Thomson Datastream, Haver, and authors’ calculations
D. Fundamentals-based Regression Models
Stronger macroeconomic fundamentals may help to explain the decline in Brazil’s neutral
real interest rate over the past decade suggested by various statistical methods. In this section
we estimate two parsimonoius models that try to decompose changes in the neutral rate by
fundamental determinants. Our approach follows Bernhardsen and Gerdrup (2007) and
Goldfajn and Bicalho (2011), and constitutes a natural extension to the state space system
presented in the previous section.
Long-run Equilibrium Real Interest Rate
The long-run equilibrium real interest rate is estimated as a function of productivity, inflation
outcomes, external vulnerability, sovereign creditworthness, and financial deepening.
Specifically, the control variables are:
Productivity growth: Annual growth rate of output per employed person;
Inflation gap: Difference between the actual 12-month consumer’s inflation rate (IPCA) and
the center of the Brazilian Central Bank’s (BCB) inflation target band;
Inflation surprise: Difference between the one-year ahead expected inflation (from the BCB
Focus survey) and the actual inflation outcome;

Sovereign risk: 5-year credit default swap (CDS) spreads;
Public indebtedness: Ratio of net public debt to GDP;
Financial deepening: Domestic credit to the private sector as a percent of GDP;
Global interest rates: 3-month and 10-year yields on U.S. Treasury securities.
The coefficient on private credit-to-GDP ratio should be positive because financial deepening
that reflects increased supply of savings (whether foreign or domestic) should lower the
neutral rate. The coefficients on sovereign risk and public indebtedness are expected to be
negative. The interest parity condition implies a positive coefficient on global interest rates.
Better inflation performance—smaller inflation gaps and inflation surprises—should lower
the neutral rate. Higher productivity growth should increase the demand for funds and raise
the neutral rate. Our econometric estimates are largely consistent with these priors, fit the
data well, and pass the usual diagnostic tests (Table 4).
We find three main domestic reasons for the fall in the neutral rate: lower public debt,
reduced sovereign risk, and an increased supply of saving that has translated into financial
deepening (together, the green bars in Figure 6). In contrast, inflation performance has not
made a major contribution to a lower neutral rate, at least since 2007. This reflects, in part,
that the inflation gap has not narrowed over recent years, while inflation surprises have been
largely asymmetric (on the upside), as shown in Figure 7.9
Lower global interest rate contributed about 200 basis points to the decline in Brazil’s neutral
rate during 2010–13 relative to their average contribution in 2005–08. According to this
approach, the long-run equilibrium real interest rate in Brazil was running between 2½ and
3 percent by mid-2013. The limited sample size and inherent model uncertainty suggest a
wide confidence interval around these figures.
9 This asymmetry has also been highlighted in Roache (2014).

Figure 6. Brazil: Determinants of Long-Run Equilibrium Real Interest Rate, 2005–13
(Contributions to the equilibrium real interest rate, in percentage points, excluding the intercept)
12 12
Global rates
10 10
Inflation gap and surprise
8 Other domestic factors 8
6 6
4 4
2 2
0 0
-2 -2
-4 -4
Sources: BCB, Thomson Datastream, Haver, and authors’ calculations
Figure 7. Brazil: Inflation Surprise and Inflation Gap, 2005–13
(Period average in percent; surprise is actual inflation minus 12-month ahead expected inflation;
gap is actual inflation minus the mid-point of the inflation target band)
4 4
Inflation gap Inflation surprise
3 3
2 2
1 1
0 0
-1 -1
-2 -2
-3 -3
-4 -4

Table 4. Brazil: Determinants of Long-Run Equilibrium Real Interest Rate, 2003–13
Table: Brazil: Fundamentals-based Cointegrating Regressions, 2003-2013 1/
Dependent variable: Real policy rate deflated by 12-month ahead expected inflation 2/ 3/
(A) (B) (C) (D) (E) (F) (G) (H) (I) (J) (K) (L)
Linear trend -0.274 -0.227 -0.223 -0.097 -0.134 -0.288 -0.228
s.e. (0.03)*** (0.02)*** (0.02)*** (0.11) (0.05)** (0.03)*** (0.03)***
Global short-term interest rate_t 1.486 0.481 0.503 0.365
s.e. (0.41)*** (0.02)*** (0.00)*** (0.00)***
Global long-term interest rate_t 3.011 0.724 0.910 0.413
s.e. (0.63)*** (0.07)*** (0.01)*** (0.01)***
Inflation gap_t-1 0.026 0.575 1.045 0.678
s.e. (0.07) (0.03)*** (0.00)*** (0.01)***
Inflation surprise_t-1 0.094 0.524 0.431 0.645
s.e. (0.110) (0.03)*** (0.01)*** (0.01)***
Private credit/GDP_t-1 -0.210 -0.134 -0.086 -0.178
s.e. (0.15) (0.01)*** (0.00)*** (0.00)***
Public debt/GDP_t-4 0.235 0.111 0.141 0.163
s.e. (0.09)*** (0.01)*** (0.00)*** (0.00)***
Productivity growth_t-4 -0.106 0.245
s.e. (0.18) (0.00)***
Sovereign risk_t-4 0.731 0.038
s.e. (0.20)*** (0.00)***
Constant 13.549 5.354 -3.030 12.240 12.035 16.704 -0.330 14.157 10.988 2.637 -1.790 3.092
s.e. (0.76)*** (0.96)*** (2.31) (0.46)*** (0.61)*** (2.62)*** (5.08) (0.91)*** (1.08)*** (1.02)*** (0.13)*** (0.07)***
Adjusted R2 0.83 0.28 0.51 0.79 0.80 0.82 0.82 0.82 0.84 0.94 0.95 0.97
Long-run variance n.a. 22.77 16.30 1.44 3.29 2.28 1.60 3.68 1.96 0.02 0.00 0.00
Engle-Granger coint. test (prob) 4/n.a. 0.01 0.00 0.02 0.11 0.00 0.00 0.12 0.03 0.03 0.08 0.03
Sample size 44 43 43 42 42 42 39 36 35 39 36 35
1/ Standard errors in parenthesis: * significant at 10%; ** significant at 5%; and *** significant at 1%.
2/ Models B thru L are cointegrating regressions (Fully Modified Least Squares).
3/ Long-run covariance estimates use prewhitening with lags based on AIC, Bartlett kernel, and Newey-West automatic bandwidth selection.
4/ Probability of rejecting the null hypothesis of no cointegration when the null hypothesis is true.
Source: BCB, Thomson Datastream, Haver, and authors’ calculations
Short-Run Equilibrium Real Interest Rate
The short-run equilibrium rate can diverge substantially from our notion of the long-run
neutral rate, factor that clearly should be taken into account by policymakers. Following
seminal work by Rudebusch and Svensson (1999), adapted by Bernhardsen and Gerdrup
(2007) for Norway, and by Goldfajn and Bicalho (2011) for Brazil, we estimate a simplified
IS model that helps to disentagle short-term interest rate movements from its long-term
(neutral) trajectory.
Our model is novel in the sense that it incorporates the impact of the public sector on the
financial deepening process—via the the Brazilian Development Bank (Banco Nacional de
Desenvolvimento Econômico e Social, BNDES)—in the gap equation:
=α( )+β( +γ( +
(10)
δ(

where:
 is the Brazilian output gap (actual minus potential output);
 is the world’s output gap (actual minus potential output);
 is the real interest rate gap (actual minus the long-run equilibrium
interest rate estimated by the authors using model J in Table 4);
 is the exchange rate gap (actual minus its long-term trend estimated
by the authors using statistical filters);
 is the gap of the central government consumption (actual minus its
long-term trend estimated by the authors using statistical filters); and
 is the gap of BNDES lending (actual minus its long-term trend
estimated by the authors using statistical filters).
The estimated coefficient on the global output gap is positive and the coefficients on the real
interest rate gap and the exchange rate gap are both negative, as expected (Table 5). The
government consumption gap is not statistically significant but the effect of BNDES lending
is positive and significant, suggesting a procyclical role of public sector lending during the
sample period considered in this paper.
Table 5. Brazil: Determinants of Short-Run Equilibrium Real Interest Rate, 2005–13
Dep. variable: Lagged World Interest rate Exchange BNDES Government
output gap output gap output gap gap rate gap lending gap consumption gap
Adj. R2=0.74
Point estimate 0.358 0.208 -0.453 -4.885 0.060 0.006
Std. error (0.02)*** (0.07)*** (0.14)*** (1.55)*** (0.03)** (0.06)
Sources: BCB, Thomson Datastream, Haver, and authors’ calculations
1/ Standard errors in parenthesis: * significant at 10 percent; ** significant at 5%; and *** significant at 1 percent.
3/ HAC standard errors and covariance estimates use prewhitening with 4 lags, Bartlett kernel, and Newey-West automatic
bandwidth selection.
Using the estimates from Table 5, we solve equation (10) for at each period of time to
obtain a path for the short-run equilibrium real interest rate.10 At the steady state, all gaps
close. As a corollary, the short-run and the long-run equilibrium real interest rates are equal,
suggesting a locus for the neutral rate. This situation is illustrated in Figure 8, which shows
that early in 2012 both rates met around 4 percent in Brazil, and after that the short-run
equilibrium rate was lower than the long-run equilibrium rate until late 2013.
10 In order to do it, we rewrite the IS model such that the short-run equilibrium real interest rate equals the long-
run equilibrium real interest rate plus the sum of all other gap variables at each point in time.

Figure 8. Brazil: Short- and Long-Run Equilibrium Real Interest Rates, 2005–13
(In percent)
16 16
Real_Selic_Short-term
14 14
Real_Selic_Long-term
Poly. (Real_Selic_Long-term)
12 12
10 10
8 8
6 6
4 4
2 Matching 2
Point
0 0
2005Q2 2006Q2 2007Q2 2008Q2 2009Q2 2010Q2 2011Q2 2012Q2 2013Q2
Sources: BCB, Thomson Datastream, Haver, and authors’ calculations
These estimates provide very strong evidence that the short-run and long-run equilibrium real
rates can diverge substantially, reflecting both domestic and external factors and the stance of
monetary policy.11
11 A possible topic of discussion in this context is the impact of macroprudential (MaPs) measures on estimates
of the IS curve for Brazil. While MaPs are not expected to affect the steady state of the model variables, they
may influence their actual prints (and thus their gaps). MaPs may also interfere on the transmission mechanism
of the monetary policy, expediting or delaying the convergence of short-run rates towards a neutral stance, like
it happened in the segment of car loans in Brazil recently. For a deeper examination of Brazil’s experience with
MaPs, see Pereira da Silva and Harris (2012), and Tovar, Garcia-Escribano, and Vera-Martin (2012).

VI. INSIGHTS FROM A SMALL MONETARY MODEL
In this section we use a small rational expectations model to better understand the policy
implications of a changing neutral rate. The aim is to identify how monetary policy settings
might respond to a changing neutral rate, but also to assess what happens if policymakers
“get it wrong”; in other words, the implications of a policy error made on the basis of an
incorrect assessment of the neutral rate.
Previous research has focused more on incorrect estimates of potential output. Orphanides
(2002) suggests that when policymakers make systematic errors estimating potential output,
activist policy rules can lead to worse outcomes, notably higher output gap and inflation
variability. Uncertain neutral rates have also been shown to affect macroeconomic outcomes
and optimal monetary policy design. Orphanides and Williams (2007) show that, like
potential output, uncertainty about neutral rates and resulting (unintentional) policy errors
using Taylor-type rules increase growth and inflation variability. They suggest that the
optimal policy rule, in the face of such uncertainty, should exhibit more sensitivity to
inflation and output than if the neutral rate was known with certainty. They also suggest that
a difference rule in which policy responds to changes in inflation and output (or
unemployment) can remove the feedback of policymaker misperceptions of the neutral rate
to the economy. Taylor and Williams (2010) also advocate a rule that removes the influence
of the estimated neutral rate on policy rate settings. Specifically, they suggest that optimal
policy should show greater inertia with the interest rate from the previous period serving as
the “steady state” benchmark (in place of an estimate of the neutral rate), while still
responding to inflation and output gaps.
Our model is based on the framework described by Berg, Karam, and Laxton (2006) and
includes four structural equations that link output, inflation, and policy interest rates.
Specifically, the four equations include: (1) an aggregate demand or IS curve that relates the
level of real activity to expected and past real activity, the real interest rate, and the real
exchange rate; (2) a price-setting or Phillips curve that relates inflation to past and expected
inflation, the output gap, and the exchange rate; (3) an uncovered interest parity condition for
the exchange rate, with some allowance for backward-looking expectations; and (4) a rule for
setting the policy interest rate as a function of the output gap and expected inflation.
y  y*   ygap   y  y*    r  r*    z  z*  y (11)
t t ld t1 lag t1 t1 r t1 t1 z t1 t1 t
  4  1 4   y  y*   z  z   (12)
t ld t1 ld t1 ygap t1 t1 z t t1 t
z  ze  1  r  rUS   z (13a)
ze  z  1  z (13b)
t1 z t1 z t1
i  i   1  r** 4   4 *    y  y*  i (14)
t lag t1 lag  t t  t4 t4 ygap t t  t

Where:
y ≡ log output in period t
t
y * ≡ log potential output in period t
t
y - y * ≡ output gap in period t
t t
π ≡ annualized quarter-on-quarter change in the log price index in period t
t
π * ≡ inflation target in period t+4
t+4
π4 ≡ year-on-year change in the log price index in period t
t
z ≡ log real bilateral exchange rate versus the U.S. dollar (+ = depreciation) in period t
t
z * ≡ log equilibrium real bilateral exchange rate versus the U.S. dollar in period t
t
ze ≡ expected (model consistent) real exchange rate in period t+1
t+1
r US ≡ United States short-term real interest rate in period t
t
ρ ≡ country-specific risk premium in period t
t
r * ≡ “true” neutral real interest rate in period t
t
r ** ≡ policymakers estimate of the neutral real interest rate in period t
t
i ≡ nominal policy rate in period t
t
ε y ≡ idiosyncratic output shock in period t
t
ε π ≡ idiosyncratic inflation shock in period t
t
ε z ≡ idiosyncratic exchange rate shock in period t
t
ε z ≡ idiosyncratic policy interest rate shock in period t
t
We start the model in its steady state, when policymakers accurately identify the constant
neutral rate (i.e., r** = r*), the output gap is closed (y = y*), and inflation is at the target
(π=π*). The parameters for the model β , β , β , β , α , α , α , δ , γ γ and γ have
lead lag r z lead ygap z z lag, π, ygap
been approximately calibrated to Brazil over the 2000Q1 to 2012Q2 period and are provided
in the appendix. The inflation target is equal to the mid-point of the Central Bank of Brazil’s
target range of 4½ percent ± 2 percent.
Our focus is on a changing neutral rate and our first scenario considers an unanticipated
decline in the neutral rate r* that is correctly identified by policymakers. Throughout this
period, all other shocks are set to zero to isolate the impact of the change in r*. In particular,
we consider a gradual 3½ percentage point decline in the neutral rate to 3 percent over a
period of eight years, keeping r*=r**. We contrast this with two alternative scenarios in
which policymakers “get it wrong”. We implement a change in the neutral rate without
changing any of the other steady-state values in the model, including potential output. As the
Euler condition shows, there is a strong link between the neutral rate and potential output
growth. We justify our focus only on a changing neutral rate in two ways: r* can change for
a constant potential growth rate due to consumer preferences; and we want to ease the
comparison with the previous literature (e.g., on potential output uncertainty) which largely
kept the assumed neutral rate unchanged.
In the second scenario, we assume that policymaker beliefs are lagging. Specifically, we
assume that policymakers believe the neutral rate is following the same downward trajectory
as the true neutral rate, but with a two year lag. This seems a reasonable assumption.

Policymakers will often change their beliefs about important structural variables such as the
neutral rate and subsequent policy settings only slowly over time (see for example Sack and
Wieland, 2000). At the same time, the neutral rate itself is likely to change only gradually,
suggesting long lags in learning. We do not model policymaker beliefs explicitly—as done in
Orphanides and Williams, 2007—and instead adopt the heuristic approach to their formation
of simply assuming that they decline gradually over time.
In our third and final scenario, we assume that policymakers believe that the neutral rate is
falling at a faster rate than is actually occurring. At some point, at least in the simple model
above, this error will be recognized—it is easy to show that at a steady state with r** < r*
inflation will be persistently above target by the quantity γ (π - π*), implying that a rational
π
inflation-targeting central bank will eventually fully learn about the neutral rate.
Figure 9. Small Model: Scenarios for Neutral Rates
Scenario 1: Neutral Real Interest Scenario 2: Neutral Real Interest Scenario 3: Neutral Real Interest
(percent)
Rate Rate Rate
(percent) (percent) (percent)
7.00 7.00 7.00
6.00 6.00 6.00
5.00 5.00 5.00
4.00 4.00 4.00
3.00 3.00 3.00
2.00 Actual and policymaker 2.00 2.00
Difference r**-r*
1.00 estimate r**=r* 1.00 1.00 Actual r*
Policymaker estimate r**
0.00 0.00 0.00
Difference r**-r*
-1.00 -1.00 Actual r* -1.00
-2.00 -2.00 Policymaker estimate r** -2.00
Years before/ after start of NIR decline Years before/ after start of NIR decline Years before/ after start of NIR decline
Source: Authors’ calculations
To implement the two scenarios in which policymakers hold mistaken beliefs, we need to
break the link between the policymaker’s expected inflation (π4 ) that is determined by (11)
t+4
and (12) and current policy settings in (14). The standard model (11)-(14) would imply
inconsistent behavior on the part of policymakers as they set policy on the basis of r** and
project future inflation on the basis of r*, where r**>r*. In other words, they would
recognize, yet ignore, their own mistake. One way to achieve this is to assume that the
policymakers’ horizon, in an environment of higher neutral rate uncertainty, shrinks to the
point that they act only on the basis of observable variables. We implement this assumption
by setting the policy rule to target the gap between current (observable) inflation and the
inflation target. This means the policy rule (14) becomes:
i  i   1  r** 4   4 *    y  y*  i (15)
t lag t1 lag  t t  t t4 ygap t t  t

The results of these simulations are shown in Figure 10. In the first scenario, where
r** = r*, a small negative output gap emerges and inflation falls slightly below the target
mid-point. This outcome is due to policy inertia causing the policy interest rate to move
sluggishly, with the speed of policy adjustment reflected in the value of γ in (15).
lag
Outcomes are worse when policymakers make mistakes. In the second scenario, the
immediate effective tightening in monetary policy caused by inertia is now compounded by
policy being set on the basis of an incorrect neutral rate r** > r*. Over the first year, the real
interest rate gap r - r* rises by about 50 basis points and this inadvertent monetary tightening
results in a modestly negative output gap. The interest rate gap increases by a further 50 basis
points in the second year, while the output gap continues to widen modestly. At the same
time, inflation falls persistently, but modestly, below the target. The interest rate gap peaks at
about 110 basis points during the third year of the mistake, before r** begins to converge to
r*.
In the third scenario, policy loosens as policymakers mistakenly set r** < r*. Over the first
year of the mistake, the interest rate gap declines by about 20 basis points and the output gap
rises, but very modestly. The interest rate gap peaks during the fifth year of the mistake at
about 130 basis points reflecting, in part, the very gradual nature of the change in neutral
rates.
Figure 10. Falling Neutral Real Interest Rates in a Small Monetary Model: Scenarios 1/
(percent)
Scenario 1: Output Gap Scenario 2: Output Gap Scenario 3: Output Gap
(percent) (percent) (percent)
0.50 0.50 0.50
0.40 0.40 0.40
0.30 0.30 0.30
0.20 0.20 0.20
0.10 0.10 0.10
0.00 0.00 0.00
-0.10 -0.10 -0.10
-0.20 -0.20 -0.20
-0.30 -0.30 -0.30
-0.40 -0.40 -0.40
-0.50 -0.50 -0.50
Years before/ after start of NIR decline Years before/ after start of NIR decline Years before/ after start of NIR decline
Scenario 1: Inflation Scenario 2: Inflation Scenario 3: Inflation
(percent) (percent) (percent)
5.40 5.40 5.40
5.20 5.20 5.20
5.00 5.00 5.00
4.80 4.80 4.80
4.60 4.60 4.60
4.40 4.40 4.40
4.20 4.20 4.20
4.00 4.00 4.00
3.80 3.80 3.80
Years before/ after start of NIR decline Years before/ after start of NIR decline Years before/ after start of NIR decline
Source: Authors’ calculations.1/

The striking aspect of these results is that the adverse outcomes are modest given the size of
the mistake (measured as r** - r*). In scenarios two and three, the output gap peaks at about
-0.5 and 0.5 percentage points, respectively. Similarly, inflation diverges from the target by
about 0.7 percentage points (in opposite directions) in both scenarios. The reason is that
policymakers are continuing to follow their own rules at the same time as mistakenly
estimating the neutral rate. This means that policymakers are partly correcting their own
mistake in each quarter.
To illustrate, consider the third scenario where r** < r*. As the monetary policy becomes
stimulative, the output gap widens, and inflation rises above target; policymakers will
perceive this to be a positive output shock (i.e., in equation (10), ε y > 0). In response, they
t
will partially undo the policy rate reductions triggered by their downward revision of r*, with
the strength of the policy reaction condition by the parameters in the policy rule (15). Over
time, policymakers will likely learn that their estimate r** is incorrect. So long as they retain
their initial estimate r**, the ongoing policy response to perceived output shocks will prevent
the actual interest rate gap (defined as the actual real interest rate r less the true neutral rate
r* or r – r*) from diverging too far away from zero.
Figure 11 shows real interest rate gaps from policy rules with different parameters.
Policymakers with loss functions that are highly sensitive to both output and inflation gaps
(in Figure 11 this is policy rule 1 with very high values for γ and γ ) will react sharply to
π ygap
the outcomes of their mistaken estimate r**. In turn, this results in an interest rate gap that
hardly diverges from zero. In contrast, policymakers that attach a much lower weight to
output and inflation gaps (in Figure 11 this is policy rule 2 with low values for γ and γ )
π ygap
instead implicitly attach a much higher weight to their estimate of the neutral. (Note that the
interest rate gap r – r* in this case is somewhat different from the neutral rate estimate gap
r** - r* because actual real rates are calculated using one quarter ahead inflation.)
Real Interest Rate Gaps: Scenario 3
Figure 11. Sc(epneracerniot) 3: Actual Real Interest Rate Gaps Under Different Policy Rules 1/
1.00 Neutral rate mistake (r** - r*)
'Actual' real rate gap (r - r*) - policy rule 1
0.50 Actual real rate gap (r - r*) - policy rule 2
0.00
-0.50
-1.00
-1.50
-2.00
Years before/ after start of NIR decline
Source: Authors’ calculations.
1/ Policy rule 1 assigns coefficients γ =0, γ =3 and γ =3. Policy rule 2 assigns coefficients γ =0, γ =0.01 and γ =0.01.
lag π ygap lag π ygap

This analysis clearly highlights the inherent risks for policymakers when the neutral rate
appears to be shifting significantly. The most important risk is that policymakers attach a
higher weight to anchoring current policy settings on the basis of their estimate of the neutral
and less weight on output and inflation gap outcomes. This is consistent with the findings of
Orphanides and Williams (2007) and Taylor and Williams (2010). It is well known that
uncertainty about state variables (in this case the neutral rate) does not affect the optimal
policy feedback rule—see Smets (2002) for an exposition.
However, a simple linear decision rule of the form i = -Fx , where x is a vector of state
t t t
variables (such as output gaps and inflation) is not certainty equivalent as shown by
Söderlind (1999). This means that the efficient policy rule coefficients will depend on the
covariance of the predetermined variables in the model, including r*. In other words, if
uncertainty about r* increases during its transition to a new steady state, policymakers should
maintain their current rule or even increase their activism and respond more forcefully to
output and inflation gaps, thereby reinforcing the self-correcting mechanism.

VII. CONCLUDING REMARKS
A battery of empirical and semi-structural techniques suggest that neutral rates in emerging
markets have declined over the past decade. In Brazil, where real interest rates have
traditionally been (and remain) high, there is particularly strong evidence of a large fall in the
neutral rate.
The secular decline in Brazil’s neutral rate is deeply rooted into its experience as an inflation-
tergeting economy. As highlighted in Mishkin and Savastano (2001), Brazil’s move to
targeting inflation in July 1999 was “clearly the first comprehensive attempt to establish a
regime of this type in Latin America”. Also impressive were the speed of implementation
and the degree of transparency and accountability embedded in the framework, with
immediate impact on inflation expectations and the neutral rate.
For the sample period covered in this paper, our econometric results suggest that global real
interest rates have pushed down Brazil’s neutral rate but domestic factors have also been
important, particularly: an increase in the supply of saving (reflected in swift financial
deepening); declining public debt; and lower sovereign risk. At the same time, we find that
there has been substantial cyclical variation in the estimates of equilibrium (or neutral) short-
term interest rates, reflecting factors such as domestic and world output gaps.
The good news is that high levels of uncertainty regarding the true neutral rate need not
complicate policymaking too much. On the basis of small macromodel simulations calibrated
for Brazil, we find that the costs of incorrectly estimating the neutral rate, in isolation, are
likely to be low. This is because standard monetary policy instrument rules provide a self-
correcting mechanism that ensures mistakes are partly corrected. The intuition is clear—an
activist policy rule will ensure that policymakers respond symmetrically to observable
outcomes, whether they are due to output and inflation shocks or incorrectly estimated
neutral rates. This guarantees that actual real interest rates are never too far away from the
“true” neutral rate, thereby minimizing the variability of output and inflation gaps.
Our result contrasts sharply with Orphanides (2002) who showed that, in the presence of an
incorrectly estimated level of potential output, activist policy rules can exacerbate output and
inflation gap variability. However, it is consistent with Orphanides and Williams (2007) and
Taylor and Williams (2010) in that the best response to neutral rate uncertainty is to ensure
policy remains highly sensitive to inflation and output variations. The main risk in updating
assumptions about the neutral rate is that policy becomes less activist and more focused on
“targeting the neutral rate,” which would amplify the costs of mistakes.