Measuring the Natural Rate of Interest
Thomas Laubach
John C. Williams
Board of Governors of the Federal Reserve System(cid:3)
November 2001
Abstract
A key variable for the conduct of monetary policy is the natural rate of interest
{ the real interest rate consistent with output equaling potential and stable inflation.
Economic theory implies that the natural rate of interest varies over time and depends
on the trend growthrate of output. In this paper we apply the Kalman(cid:12)lter to jointly
estimate the natural rate of interest, potential output, and its trend growth rate, and
examine the empiricalrelationshipbetweenthese estimated unobservedseries. We (cid:12)nd
substantial variation in the natural rate of interest over the past four decades in the
United States. Our natural rate estimates vary about one-for-one with changes in the
trend growth rate. We show that policymakers’mismeasurement of the natural rate of
interest can cause a signi(cid:12)cant deterioration in macroeconomic stabilization.
JEL classi(cid:12)cation: C32, E43, E52, O40.
Keywords: natural rate of interest, interest rate rules, Kalman (cid:12)lter, trend growth,
potential output, equilibrium real interest rate.
(cid:3)Washington, D.C.20551, tlaubach@frb.gov,jwilliams@frb.gov. Theviews expressed hereinare thoseof
the authors and do not necessarily reflect those of the Board of Governors of the Federal Reserve System
or its sta(cid:11). We thank Adam Litwin for excellent research assistance. This research has bene(cid:12)tted from
discussions with Antulio Bom(cid:12)m, Bill English, Michael Kiley, Ed Nelson, John Roberts, Brian Sack, Bill
Whitesell, and participants at sessions at the Econometric Society North American Summer Meeting and
theInternational Conference of theSociety of Computational Economics.

1 Introduction
A key input into the conduct of monetary policy is a measure of the \neutral" stance of
policy, against which one can gauge policy’s stimulative or contractionary impetus. One
such measure, especially prominent in regimes in which the central bank explicitly targets
a monetary aggregate, is the growth rate of a monetary aggregate relative to some trend
or target rate of growth. In the United States and many other countries, however, the
short-term interest rate has become the primary policy instrument. In such regimes, the
\equilibrium" or \natural" interest rate provides a metric for the stance of policy. For this
purpose, it is useful to de(cid:12)ne the natural rate of interest to be the real short-term interest
rate consistent with output converging to potential, where potential is the level of output
consistent with stable inflation (Cf. Bom(cid:12)m (1997)). In this formulation, the natural
(cid:3)
rate of interest, hereafter referred to as r , represents a medium-run real rate \anchor" for
monetary policy and corresponds to the intercept term in feedback rules such as Taylor’s
(1993) Rule.
Economic theory implies that the natural rate of interest varies over time in response
1 (cid:3)
to shifts in preferences and technology. The relationship between r and fundamentals is
mostclearlyillustratedinthecontextofthestandardoptimalgrowthmodel. Theoptimality
condition for saving yields a balanced growth condition relating the real interest rate, r, to
preference and technology parameters:
1
r = q+n+(cid:18); (1)
(cid:27)
where (cid:27) denotes the intertemporal elasticity of substitution in consumption, n is the rate
of population growth, q is the rate of labor-augmenting technological change, and (cid:18) is the
2
rate of time preference. This (cid:12)nding that the real interest rate is positively related to
the rates of trend growth and time preference, holding other factors (cid:12)xed, holds in a wide
1If not for its time variation, estimation of the natural rate would be relatively straightforward. One
simple approach is to take the sample mean over a relatively long period when inflation shows no upward
or downward trend (Cf. Reifschneider and Williams (2000)). This method yields an estimate of r(cid:3) of
about3percent. Alternatively,onecanderiveanestimateof r(cid:3) usinganestimatedmacromodelwith(cid:12)xed
parameters (Cf. Taylor and Williams (1993), Orphanidesand Wieland (1998), and Rudebusch(2001)).
2Forthisexample,weassumeCRRApreferencesandthattheutilityofeachfuturegenerationisweighted
equally irrespective of size; if, instead, the utility of each generation is weighted according to its size, we
haver= 1q+(cid:18).
(cid:27)
1

3
variety of models. In light of the evidence of substantial shifts in the trend growth rate in
the United States and other countries over the past several decades (Cf. Maddison (1995),
Oliner and Sichel (2000), Roberts (2001)), the assumption of a constant natural rate of
interest appears untenable. Moreover, changes in other factors such as (cid:12)scal policy factors
may induce persistent changes in the natural rate of interest over time.
Our de(cid:12)nition of the natural rate is closely related to Wicksell’s verbal description:
There is a certain rate of interest on loans which is neutral in respect to com-
modity prices, and tends neither to raise nor to lower them.
Wicksell (1936, p. 102)
In characterizing the natural rate of interest, we focus on a medium-run concept of price
stability that abstracts from the e(cid:11)ects of short-run price and output fluctuations. In this
respect, our de(cid:12)nition di(cid:11)ers from that advanced recently by Woodford (2000), who de(cid:12)nes
the Wicksellian natural rate of interest to be the real rate that yields period-by-period
price stability. Woodford’s characterization of the natural rate does not correspond to the
intercept term in a monetary policyrulethat contains independentresponsesto outputand
inflation, but instead fully describes the optimal setting of policy for a particular objective
function(Cf. Woodford(2001)). Infact, existing estimates basedonthisde(cid:12)nitionabstract
(cid:3)
entirely from lower frequency components of r and potential output by using detrended
data (Cf. Rotemberg and Woodford (1997), Neiss and Nelson (2001)). Importantly, these
estimates are very sensitive to the structural assumptions of the particular model, and, as
a result, yield policy prescriptions that are unlikely to be robust to model uncertainty (Cf.
Levin, Wieland and Williams (1999)). In contrast, our goal is to provide a robust method
(cid:3)
of identifying lower-frequency movements in r that can beincluded in the kind of \simple"
policy rules that have been shown to perform well in a wide variety of models (Cf. Levin,
Wieland and Williams (2001)).
Because we de(cid:12)nethe natural rate of interest in relation to the deviation of outputfrom
(cid:3) 4
potential, estimation of r also entails estimation of potential output. Moreover, owing to
(cid:3)
thetheoretical linkagebetween r andthetrendgrowthrate, weareinterestedinestimating
3For example, if we follow Solow (1956) and assume that the saving rate is constant, then the real
interestratewillalsobepositivelyrelatedtotherateofgrowthandnegativelytothesavingrate(thelatter
presumably negatively related to the rate of time preference). Speci(cid:12)cally, r =(cid:11)(cid:14)+n+q −(cid:14), where s is the
s
saving rate out of output and(cid:14) is therate of depreciation.
4Analternativewouldbetospecifyareduced-formrelationshipbetweenthechangeintherateofinflation
2

both the level of potential output and its trend growth rate. We apply the Kalman (cid:12)lter
to these unobserved low frequency variables, modeling the cyclical dynamics of output and
inflation using a restricted VAR model that imposes relatively little structure on short-run
(cid:3)
dynamics. Because the innovation variances to r and the trend growth rate are small, we
use Stock and Watson’s (1998) median-unbiased estimates of these coe(cid:14)cients and apply
maximum likelihood to estimate the remaining model parameters.
(cid:3)
Time variation in r and in particular its real-time mismeasurement is potentially im-
portant for the conduct and performance of monetary policy. In a recent paper, however,
(cid:3)
Rudebusch (2001) (cid:12)nds that transitory shocks to r have only modest implications for the
conduct of monetary policy. In this paper, we reexamine this issue in the context of the
(cid:3)
estimated highly persistent movements in r over history and come to the conclusion that
(cid:3)
there are relatively large stabilization losses associated with r mismeasurement, and that
(cid:3)
these losses can be mitigated by timely updating of r estimates.
Theremainderofthepaperisorganizedasfollows. Thenextsectiondescribestheempir-
ical framework used for estimating the natural rate of interest, potential output, and trend
growth. Section three describes the estimation methodology and reports estimation results.
Sectionfourexaminestherobustnessoftheseresultstochanges intheestimates ofpotential
(cid:3)
output and trend growth. Section (cid:12)ve investigates the e(cid:11)ects of r mismeasurement on the
performance of monetary policy. Section six concludes.
2 An Empirical Framework for Measuring the Natural Rate
As noted, we apply the Kalman (cid:12)lter to estimate the natural rate of interest, the level of
potential output, and its trend growth rate. One alternative would be to use a univariate
(cid:3)
time-series method to estimate r . However, such an approach is problematic because it
does not control for the sustained periods of rising and declining inflation in the United
States during the past several decades. In particular, given that the natural rate of interest
and the deviation of the real interest rate from r(cid:3); however, this approach is likely to yield very weak
identi(cid:12)cation of r(cid:3). An altogether di(cid:11)erent approach is to use forward rates implied by the term structure
andameasureofinflation expectationstoestimatelow frequencymovementsin thenaturalrateof interest
(Cf. Brayton,Mauskopf,Reifschneider,TinsleyandWilliams(1997),KozickiandTinsley(2001)). Inrecent
work,Bom(cid:12)m(2001)usesforwardratesfromTreasuryinflation-indexedbondstoestimater(cid:3) overthethree
years that they have been issued. One di(cid:14)culty with this general approach is that one must account for
time-variation in theterm premium evident in thedata.
3

is related to medium-run inflation stability, such univariate methods are likely to underes-
(cid:3)
timate r during the 1960s and 1970s when inflation was rising, and overestimate it during
5
the disinflationary episodes of the early 1980s and the 1990s. For this reason, we estimate
the natural rate within a model consisting of inflation, output, and real interest rates.
(cid:3)
Econometricidenti(cid:12)cationofr isachievedbyspecifyingasimplereduced-formequation
relating the output gap (the percent deviation of real GDP from potential output) to its
own lags and a moving average of the lagged real funds rate gap (the di(cid:11)erence between
(cid:3) 6
the real funds rate and r ), and a serially uncorrelated error. Speci(cid:12)cally, we assume that
y~ t = A y (L)y~ t−1+A r (L)(r t−1 −r t (cid:3) −1 )+(cid:15)1t ; (2)
where y~ = 100 (cid:3) (y − y (cid:3) ) denotes the output gap, y is the logarithm of real GDP, y (cid:3)
t t t t t
is the logarithm of unobserved potential GDP, r is the ex ante real federal funds rate,
t
(cid:3)
and r is the unobserved natural rate of interest. (See the Appendix for details on data
t
construction.) The serially uncorrelated error and the lags of the output gap control for
transitory shocks and short-run dynamics, while highly persistent shifts in this relationship
(cid:3)
between the output gap and the real funds rate are ascribed to changes in r . Hence, we
P
(cid:3)
require a to be less than unity in order to identify changes in r with low frequency
y
shifts in the output gap{real rate relationship
Inflation, (cid:25) , is measured by the annualized growth rate of the price index for personal
t
consumption expenditures excluding food and energy { referred to hereafter as core PCE
inflation { and is assumed to be determined by its own lags, the output gap, relative prices,
x , and a serially uncorrelated error,
t
(cid:25)
t
= B
(cid:25)
(L)(cid:25) t−1+B
y
(L)y~ t−1+B
x
(L)x
t
+(cid:15)2t : (3)
5For example, the trend component of the real funds rate based on the Hodrick-Prescott (cid:12)lter rises
sharply during the period of the Volcker disinflation. This estimate of the natural rate of interest would
inappropriately ascribe a large portion of the disinflationary policy action to a shift in thenatural rate.
6Thebasicspeci(cid:12)cationofoutputgapdynamicsisverysimilartothatinRudebuschandSvensson(1999),
exceptthattheyassumeaconstantvalueofr(cid:3). Analternativespeci(cid:12)cationistoincludetherealbondrateas
inFuhrer(1997), instead oftherealfed fundsrate. This approachintroducestwoadditional complications.
First,inordertocomputetheexantereallongrate,oneneedstomeasuremulti-yearinflationexpectations,
whicharearguably morepronetomeasurement errorthannear-terminflation expectationsassociated with
the short-term interest rate. Second, in so far as we are seeking to estimate a natural rate useful for a
monetary policy rule, the term premium, itself a potentially time-varying process, would also need to be
estimated. Weleave this to furtherresearch.
4

Therelative pricevariables includemeasures of core importpriceandcrudeoilimportprice
inflation, bothmeasuredasdeviations fromcorePCEinflation. Potential GDP isde(cid:12)nedas
the level of GDP that is consistent with unchanged inflation in the absence of relative price
shocks, x
t
, and the serially uncorrelated disturbance, (cid:15)2t . Equations (2) and (3) constitute
the measurement equations of our state-space model.
(cid:3)
As noted, economic theory implies that the trend growth rate is one determinant of r .
Hence, we specify
(cid:3)
r = c g +z ; (4)
t t t
(cid:3)
where g is our estimate of trend growth and z captures other determinants of r , such as
t t
households’ rate of time preference. We assume that z follows an autoregressive process,
z t =D z (L) z t−1 +(cid:15)3t ; (5)
where (cid:15)3t is assumed to be a serially uncorrelated innovation. In principle, z may be
stationaryornonstationary;inthefollowingweconsidertwospeci(cid:12)ccases: (1)z isdescribed
by a stationary AR(2) process, and (2) z follows a random walk.
As noted, there is evidence for time variation in the trend growth rate, with a slowdown
occuring during the 1970s and a pickup during the late 1990s. We allow for shocks to both
the level of potential output { the I(1) component { and its trend growth rate { the I(2)
component. For reasons of parsimony, we specify a simple random walk model for both
components. Speci(cid:12)cally, potential output is assumed to evolve according to
(cid:3) (cid:3)
y
t
= y
t−1
+g t−1+(cid:15)4t ; (6)
g
t
= g t−1+(cid:15)5t ; (7)
where (cid:15)4t and (cid:15)5t are serially uncorrelated and mutually contemporaneously uncorrelated
with the innovation to z, (cid:15)3t . Assuming the standard deviation of the disturbance to the
growth rate component of potential output is positive, potential output is a second-order
integrated process. 7 If potential output is I(2) and c6= 0, then r (cid:3) is integrated of order one,
even if the z process is stationary. Equations (4){(7) constitute the transition equations of
our state-space model.
7The hypothesis that log real GDP is I(2) is typically rejected by an ADF test. However, as Stock and
Watson (1998) point out, when the disturbance to the growth rate component has small variance, such a
test statistic has a high false-rejection rate.
5

Several authorshaveusedvariants ofthemodel(2)-(7) toobtain trend-cycle decomposi-
tions of GDP, but none incorporate interest rates in their models. Watson (1986) considers
a model with constant trend growth g and an AR speci(cid:12)cation for the output gap. Clark
(1987) extends Watson’s model and allows for time variation in trend growth. Kuttner
(1994) explores the relationship between the cyclical component of GDP and inflation by
8
including a dynamic inflation equation. Roberts (2001) decomposes output growth into
growth in hours and labor productivity growth, and allows for time variation in the trend
growth rates of both of these series. As noted, none of these contributions include the e(cid:11)ect
of interest rates and, as a result, they do not address the issue of time variation in the
natural rate of interest.
3 Estimation
We estimate several variants of the model described above on quarterly U.S. data over the
period 1961:1 to 2000:4. Details on the data used are given in the Appendix. We allow the
lag lengths in the output gap and inflation equations, equations (2) and (3), respectively,
to be determined by the data. Speci(cid:12)cally, we include two lags each of the output gap
and the real rate gap in the output gap equation. The (cid:12)nding that the output gap is
well characterized by an AR(2) is consistent with the studies using unobserved components
models cited above. We impose the restriction that the coe(cid:14)cients on the two lags of the
real rate gap are the same, which is not rejected by the data for any of our speci(cid:12)cations.
We include eight lags of inflation in the inflation equation and impose the restriction,
not rejected by the data, that the coe(cid:14)cients sum to unity. For reasons of parsimony, we
restrict the coe(cid:14)cients on lags 2 to 4 of inflation to be equal, and the same for lags 5 to 8
(Cf. Gordon (1998), Brayton, Roberts and Williams (1999)). Including only the (cid:12)rst lag
of the output gap in this equation proved su(cid:14)cient. Finally, the relative price vector, x ,
t
consists of contemporaneous core import price inflation, and the (cid:12)rst lag of oil import price
inflation, both measured relative to core PCE inflation.
8Inarelatedpaper,Laubach(2001)identi(cid:12)esthenaturalrateofunemploymentusingamodelofinflation
dynamics.
6

3.1 Estimation Methodology
In principle, the model can be estimated by maximum likelihood using the Kalman (cid:12)lter.
However, the contributions from variation in trend growth and the natural rate of interest
to overall variability in the data are relatively small. As a result, the maximum likelihood
estimates of the standard deviations of the innovations to these processes, (cid:27)3 and (cid:27)5, are
likely to bebiased towards zero owing to the so-called \pile-up problem" discussedbyStock
(1994). Indeed, the maximum likelihood estimates of both of these parameters were zero.
We therefore useStockand Watson’s (1998) median-unbiasedestimator to obtain estimates
of the ratio (cid:21) (cid:17) (cid:27)5, and, in cases where z is nonstationary, (cid:21) (cid:17) (cid:27)3par . 9 We impose these
g (cid:27)4 z (cid:27)1 2
ratios whenestimating theremaining modelparameters (including(cid:27)1 and(cid:27)4)bymaximum
likelihood. Because the pile-up problem does not arise for stationary unobserved processes,
in cases where z is stationary, we estimate the standard deviation of its innovation, (cid:27)3, by
maximum likelihood simultaneously with the other model parameters.
We proceed in three steps. In the (cid:12)rst step, we generate a preliminary estimate of
potential output, which we use as an input in estimating (cid:21) . We follow Kuttner (1994)
g
and apply the Kalman (cid:12)lter to estimate potential output, omitting the real rate gap term
from equation (2) and assuming that the trend growth rate, g, is constant. We compute
the exponential Wald statistic of Andrews and Ploberger (1994) for a structural break
with unknown break date on this preliminary estimate of potential output. We then use
Stock and Watson’s results to convert the exponential Wald statistic into an estimate (cid:21)^ .
g
ApplyingStockandWatson’s methodtothepreliminaryestimateofpotentialGDP,instead
of directly to the GDP data, has the advantage that it is consistent with their assumption
that all shocks have a permanent e(cid:11)ect on the level of the series under consideration.
Correspondingly, when applying the method to our preliminary estimate of potential GDP
we do not correct the data for serial correlation in the level shocks, as Stock and Watson
suggest.
If the unobserved component of the natural rate of interest, z, is assumed to be station-
9This ratio is based on the assumption that the coe(cid:14)cients on the two lags of the real rate gap are the
same. Substituting(4) into (2), thelatter can be written as
a a
y~ t =A y (L)y~ t−1+ 2 r(r t−1+r t−2 −c(g t−1+g t−2))− 2 r(z t−1+z t−2)+(cid:15)1t
The ratio (cid:21) based on the test statistic for an intercept shift at unknown date in this equation is thus the
z p
ratio of a
r
(cid:27)3= 2 to (cid:27)1.
7

ary, weproceed directlyto thethirdand(cid:12)nalstep; otherwise, in thesecond step, weimpose
the estimated value of (cid:21) from the previous step and follow a similar process to generate
g
an estimate of (cid:21)
z
. We again estimate the (cid:12)ve model equations, imposing (cid:27)5 = (cid:21)^
g
(cid:27)4. We
now include the real interest rate gap in the output gap equation, but assume that z is
(cid:3)
constant; that is, we assume r = c g +constant. Using this speci(cid:12)cation, we compute the
t t
exponential Wald statistic for an intercept shift in the output gap equation at an unknown
break date, and use Stock and Watson’s results to obtain an estimate (cid:21)^ .
z
In the third and (cid:12)nal step, we impose the estimated values of (cid:21) from the (cid:12)rst step
g
and (cid:21) from the second step (assuming z is nonstationary), and estimate the remaining
z
10
model parameters by maximum likelihood. As noted, if z is assumed to be stationary,
we include (cid:27)3 in the parameters to be estimated by maximum likelihood. We compute
estimated con(cid:12)dence intervals and corresponding standard errors for the estimates of the
states using Hamilton’s (1986) Monte Carlo procedure, which accounts for both (cid:12)lter and
11
parameter uncertainty.
3.2 Estimation Results
The (cid:12)rst-stage estimation of potential output indicates that the trend growth rate exhibits
only a relatively modest amount of variation over time. The (cid:12)rst line in Table 1 reports the
value of the exponential Wald statistic testing for an intercept shift in the (cid:12)rst di(cid:11)erence
of potential GDP. This value of 1.51 is just below the 10 percent critical value of 1.55
given in Andrews and Ploberger (1994, Table 1, page 1399). Using Stock and Watson’s
median-unbiased estimator, this relatively weak evidence of a change in the growth rate
of potential GDP translates into an estimate of (cid:21) of about 0.04, shown in the second
g
column of the table. When multiplied by our third-stage estimate of (cid:27)4 reported below, the
implied standard deviation of trend growth changes is estimated to beabout 0.1 percentage
10Estimates of the conditional expectation and covariance matrix of the initial state are computed using
the GLS method discussed in Harvey (1989, p. 122). Because these estimates are functions of the model
parameters, for certain parameter values the covariance matrix may be ill conditioned. The conditional
expectation of theinitial valuesof y(cid:3) and g is thencomputed by(cid:12)ttinga segmented trendthrough log real
GDP, with z initialized at zero, and the covariance matrix is set to 0.2 times the identity matrix. During
the Monte Carlo simulations for computing the standard errors, this procedure is modi(cid:12)ed as discussed in
Laubach (2001, p. 222).
11Notethattheseestimated con(cid:12)denceintervalsholdtheimposed valuesof(cid:21) and(cid:21) (cid:12)xedbuttakeinto
g z
account theuncertainty regarding (cid:27)1, (cid:27)2, (cid:27)4, and,thus, implicitly (cid:27)3 and (cid:27)5.
8

Table 1: First- and Second-stage Estimation Results
Exponential Median-unbiased Estimate of (cid:21)
Variable Wald Point 90 % Con(cid:12)dence Interval
Statistic Estimate Low High
Trend growth (g) 1.51 .039 .000 .103
Natural rate (z) 4.28 .071 .015 .117
point (expressed at an annual rate), a (cid:12)gure almost identical to Stock and Watson’s (1998)
comparable estimate. The 90 percent con(cid:12)dence intervals for the estimate of (cid:21) , computed
g
12
by Monte Carlo simulations, are given in the (cid:12)nal two columns of the table. Note that
the lower end of the 90 percent con(cid:12)dence interval for the estimate of (cid:21) includes zero, the
g
case in which the trend growth rate is constant and potential output is integrated of order
one.
The results from the second-stage estimation indicate the presence of persistent time
(cid:3)
variation in z, the component of r not related to the trend growth rate. As seen in the
second line of Table 1, the value of the exponential Wald statistic testing for an intercept
shift in the output gap equation is 4.28, which is signi(cid:12)cant at the 1 percent level. The
impliedmedian-unbiasedestimateof(cid:21) is0.07. Incaseswhereweassumethattheprocessz
z
isnonstationary{andinparticular,describedbyarandomwalk{weimposethisestimated
value of (cid:21) in the third and (cid:12)nal estimation stage.
z
Turning to the (cid:12)nal-stage estimation, we begin by assuming that z follows a stationary
AR(2) process. The results from maximum likelihood estimation of this model are reported
in the (cid:12)rst column of Table 2. The estimated coe(cid:14)cients d are consistent with z being
z
stationary. The estimated sum of coe(cid:14)cients on the lagged output gap in the output gap
equation is below unity (and the unit sum hypothesis is rejected at conventional levels),
consistent with the identi(cid:12)cation assumptions described in Section 2. Finally, the real rate
gapenterstheoutputgapequationwiththecorrectsignandissigni(cid:12)cantattheonepercent
level.
The natural rate of interest is estimated to vary one-for-one with changes in the trend
12To computethiscon(cid:12)denceinterval, weuseparameter estimates based on thesecond-stage model with
a time-varying trend growth and a constant natural rate of interest to construct 10,000 simulated series of
fy(cid:3);g g. For each pair of simulated series we compute the exponential Wald statistic for an intercept shift
t t
in the(cid:12)rst di(cid:11)erence of y(cid:3).
t
9

Table 2: Parameter Estimates
Stationary Random Walk Model for z
Parameter z (cid:24) AR(2) Baseline Low (cid:21) High (cid:21)
z z
(cid:21) .045 .071 .015 .117
z
(.24)
P
a .924 .943 .942 .944
y
a -.117 -.104 -.091 -.114
r
(3.20) (3.67) (3.66) (3.63)
b .060 .040 .059 .030
y
(1.95) (1.57) (1.84) (1.37)
c .970 1.062 1.001 1.008
(3.89)
P
d .965 1 1 1
z
(cid:27)1 (y~) .263 .364 .406 .327
(cid:27)2 ((cid:25)) .719 .725 .721 .728
(cid:27)3 (z) .142 .352 .095 .475
(cid:27)4 (y(cid:3)) .655 .627 .610 .639
(cid:27)5 (g) .102 .098 .095 .100
p
(cid:27) r(cid:3) = c2(cid:27) 5 2+(cid:27) 3 2 .173 .367 .134 .485
Log Likelihood -360.5 -362.9 -362.2 -363.0
Standard Error (ave.)
r(cid:3) 2.58 1.98 1.09 2.38
g .42 .48 .42 .53
y(cid:3) 2.33 3.25 1.97 4.32
Notes: t statistics in parentheses. (cid:27)5 is expressed at annual rate.
Standard errors are sample averages for smoothed estimates of states.
10

growth rate of output, and this result is robust to changes in the process for z. For the case
of stationary z, c is estimated to be .97, with a standard error of .25. The second column
of Table 2 reports the estimation results for the case where z is modeled as a random walk
and (cid:21) is estimated using the median-unbiased estimator. The results are very similar to
z
those where z is assumed to follow an AR(2). In particular, the estimate of c is also near
(cid:3)
unity. However, owing to the existence of two nonstationary processes determining r {
g and z { this latter estimate must be treated with caution owing to the potential for
spurious correlation (Cf. Granger and Newbold (1974)). For this reason, in cases where z
is nonstationary, inference based on the standard errors is invalid and we therefore do not
report t-statistics for the estimates of the coe(cid:14)cient c.
The (cid:12)nal two columns of Table 2 indicate the estimation results when we impose values
for (cid:21) corresponding to the lower and upper limits of the 90 percent con(cid:12)dence intervals,
z
(cid:3)
instead of the median-unbiased point estimate. Again, the coe(cid:14)cient c relating r to the
trendgrowthrateisnearunity,consistentwiththepreviousresults. Exceptforthestandard
deviations of the innovations, the parameter estimates are little a(cid:11)ected by the choice of
(cid:3)
(cid:21) . The more variable the z process and therefore r , the lower the variance of the serially
z
uncorrelated innovations to the outputgap equation. Note that, based on thelog likelihood
values, the data are not able to discern between the alternative speci(cid:12)cations shown in the
table.
The smoothed (two-sided) estimates of the unobserved processes implied by our model
(cid:3)
estimates are shown in Figure 1. The r estimates in the model in which z follows a
stationary AR(2) (indicated by the dashed line) exhibit far larger short-duration swings
than those where z is assumed to follow a random walk (the solid line). For this reason, for
the remainder of the paper, we focus on the random walk speci(cid:12)cation, which appears to
correspond more closely to our middle- and low-frequency characterization of the natural
rate of interest. We refer to the speci(cid:12)cation given in the second column as the \baseline
model;" the restriction to the random walk speci(cid:12)cation for z is not rejected by the data
(cid:3)
at the 5 percent level. This estimate of r peaks at about 4-1/2 percent in the mid-1960s,
reaches a minimum of 1-1/4 percent in the early 1990s, and ends the sample period at just
above its sample average of 3 percent.
The estimates of the trend growth rate and the output gap are very similar across the
four estimates. As shown in the middle panel of the (cid:12)gure, the estimated trend growth
11

Figure 1: Smoothed Estimates of Unobserved States
Natural Rate of Interest (r*)
6 6
4 4
2 2
z:AR(2)
Baseline
Lower z variability
0 Higher z variability 0
1960 1965 1970 1975 1980 1985 1990 1995 2000
Trend Growth Rate (g)
5 5
4 4
3 3
2 2
1960 1965 1970 1975 1980 1985 1990 1995 2000
Output Gap
5 5
0 0
-5 -5
-10 -10
1960 1965 1970 1975 1980 1985 1990 1995 2000
rate peaks in the mid-1960s at about 3-3/4 percent, and then declines through the 1970s
and 1980s. From its low of about 3 percent in the early 1990s, the trend growth rate
increases by about one-half percentage point by the end of the sample. The broad outline
of the output gap estimate, shown in the lower panel, corresponds closely to the estimates
of Clark (1987) and Kuttner (1994) over the parts of the sample that are covered by their
estimates, although Kuttner’s estimate is more volatile than either ours or Clark’s.
The standard errors of the estimates of the unobserved states, shown at the bottom of
Table 2, are relatively large, as is typical for Kalman (cid:12)lter estimates. As a result, changes
in the natural rate of interest and the trend growth rate of output are not measured with
12

much precision. Across the speci(cid:12)cations reported in the table, the average standard error
(cid:3)
of r ranges from 1 to 2-1/2 percentage points, that for the trend growth rate is about
1/2 percentage point, and that for the level of potential output from 2 to 4-1/2 percentage
points.
4 Robustness Analysis
Wenowextendtheprecedingrobustnessanalysistoincludechangesinestimatesofpotential
outputandthetrendgrowth rate. Ourde(cid:12)nition ofthenaturalrateas therealinterest rate
at which real GDP equals potential, once the e(cid:11)ects of transitory shocks have dissipated,
implies that our natural rate estimates are sensitive to our estimate of potential GDP. We
(cid:12)rst consider alternative estimates based on the uncertainty surrounding our estimate of
(cid:21) ; we then examine the e(cid:11)ects of augmenting the model with a labor market indicator to
g
assist in the decomposition of GDP into trend and cyclical components.
If the trend growth rate is assumed to beconstant, then the estimate of the natural rate
of interest is signi(cid:12)cantly less variable than in the baseline estimates. The second column
of Table 3, labeled \Low (cid:21) ", reports results from estimating the baseline model under the
g
assumptionthat(cid:21) = 0, thelower endofits 90percentcon(cid:12)denceinterval. Forcomparison,
g
the (cid:12)rst column of the table repeats the baseline results from Table 2. With a constant
trend growth rate, c is not identi(cid:12)ed. The resulting estimate of (cid:21) is 0.026, well below that
z
(cid:3)
in the baseline speci(cid:12)cation. Evidently, when modeled as a pure random walk, r is poorly
identi(cid:12)ed. As a result, a signi(cid:12)cantly greater portion of output gap variability is ascribed
to serially uncorrelated shocks and less to permanent shocks. This is illustrated graphically
in the upper panel of Figure 2. Interestingly, the output gap estimates, shown in the lower
panel of the (cid:12)gure, di(cid:11)er relatively little between the constant growth rate and the baseline
estimates.
Increasingthevariabilityofthetrendgrowthrate, however, hasrelatively modeste(cid:11)ects
(cid:3)
on the estimated parameters and the estimates of r . The third column of the table reports
the results when (cid:21) takes the value 0.103, corresponding to the upper end of the 90 percent
g
con(cid:12)dence interval. In this case, the estimate of (cid:21) is .060, slightly lower than the baseline
z
estimate. Except for the greater variability of the trend growth rate itself, the parameter
estimates donotdi(cid:11)er substantially fromthe baselineestimates. Inparticular, theestimate
13

Table 3: Parameter Estimates under Di(cid:11)erent Potential Output Assumptions
Parameter Baseline Low (cid:21) High (cid:21) Hours
g g
(cid:21) .039 .000 .103 .046
g
(cid:21) .071 .026 .060 .039
z
P
a .943 .944 .946 .927
y
a -.104 -.087 -.124 -.076
r
(3.67) (3.66) (3.60) (3.09)
b .040 .055 .031 .096
y
(1.57) (1.88) (1.28) (3.02)
c 1.062 { .995 .886
(cid:27)1 .364 .397 .257 .497
(cid:27)2 .725 .722 .729 .714
(cid:27)3 .352 .168 .175 .359
(cid:27)4 .627 .622 .662 .547
(cid:27)5 .098 .000 .273 .101
(cid:27)6 { { { .245
p
(cid:27) r(cid:3) = c2(cid:27) 5 2+(cid:27) 3 2 .367 .168 .323 .370
Log Likelihood -362.9 -362.3 -363.5 -466.51
Standard Error (ave.)
r(cid:3) 1.98 1.28 1.63 2.65
g .48 .24 .74 .46
y(cid:3) 3.25 2.18 3.48 .59
Notes: t statistics in parentheses. (cid:27)4 is expressed at annual rate.
Standard errors are sample averages for smoothed estimates of states.
1. Log likelihhod for model augmented with equation for employee hours
is not comparable to others.
14

Figure 2: Sensitivity of Estimates to Assumptions Regarding Potential Output
Natural Rate of Interest (r*)
6 6
4 4
2 2
Baseline
Lower g variability
Higher g variability
Hours Model
0 0
1960 1965 1970 1975 1980 1985 1990 1995 2000
Trend Growth Rate (g)
5 5
4 4
3 3
2 2
1960 1965 1970 1975 1980 1985 1990 1995 2000
Output Gap
5 5
0 0
-5 -5
-10 -10
1960 1965 1970 1975 1980 1985 1990 1995 2000
of c is again nearly unity. As seen in the (cid:12)gure, although the estimated trend growth rate is
much more variable (shown by the dotted line in the middle panel), the resulting estimates
(cid:3)
of r di(cid:11)er relatively little from the baseline estimates.
4.1 Incorporating Information on Employment Hours
Our second alternative speci(cid:12)cation for potential GDP is based on the notion that employ-
menthours,aswellasinflation, contain informationaboutthecyclical stateoftheeconomy.
Speci(cid:12)cally, we follow Roberts (2001) and introduce the equation
~h t = f1y~ t +f2y~ t−1+f3h~ t−1 +(cid:15)6t (8)
15

into the model, where h~ denotes percent deviations of private nonfarm employee hours h
t t
from a trend h (cid:3) . We compute h~ as the deviation of hours from a simple log-linear time
t t
13
trend (Cf. Rotemberg and Woodford (1996)).
Estimation results forthis speci(cid:12)cation areshownin the(cid:12)nalcolumn of Table3, labeled
\Hours." The resulting estimate of (cid:21) is a little larger than the baseline value, but the
g
estimate of (cid:21) is considerably lower than the baseline value. However, because the variance
z
of the serially uncorrelated innovation to the output gap equation rises while that of the
level shock to potential GDP falls, the variability of both the trend growth rate and the
natural rate of interest are nearly the same as in the baseline speci(cid:12)cation. The estimate
of c is about 0.9, just a bit below the other estimates.
The uncertainty around the output gap estimate shown at the bottom of Table 3 is less
thanone(cid:12)fthofthatinthebaselinespeci(cid:12)cation. Thehighdegreeofprecisionregardingthe
estimate of the level of potential output results from the close (cid:12)t of equation (8), combined
with the absence of any unobserved states in the estimation of trend hours. A problematic
aspect of the estimation results for the model augmented with hours is that it appears to
bein conflict with evidence of low frequencychanges in thegrowth rate of labor supply(Cf.
Roberts (2001)). For this reason, the precision of the estimates may be spurious.
The close identi(cid:12)cation of the output gap with deviations of hours from a time trend
implies a di(cid:11)erent view of history compared to the baseline model where the output gap is
identi(cid:12)ed by the inflation equation alone. As shown in Figure 2, in the model augmented
(cid:3)
with the hours equation (the dashed line), both the output gap and r are estimated to
have been below their baseline counterparts in the (cid:12)rst half of the sample, and above
them in the second half. In particular, during the late 1990s, a period when core PCE
inflation was declining, the baseline estimate indicates that output was below potential
and therefore exerting downward pressure on inflation, while the model augmented with
the hours equation indicates output was above potential and therefore boosting inflation.
Evidently, the estimates of potential output in the baseline speci(cid:12)cation include the e(cid:11)ects
of omitted variables that influence inflation but are not captured by movements in hours.
13In principle, h(cid:3) could be speci(cid:12)ed as an I(2) process analogous to y(cid:3). However, tests for an intercept
t t
shift in the raw hours data over our sample show no evidence for such a shift. Moreover, when attempting
to construct a preliminary estimate of trend hours by estimating a trend-cycle decomposition based on a
constantdriftintrendhours,trendhoursareestimatedtobeasimpletimetrend. Theseresultsdi(cid:11)erfrom
those of Roberts (2001) who normalizes hours by population and (cid:12)ndsthis series to beI(2).
16

4.2 Overall Robustness of Estimates
Table 4: Properties of Unobserved Variables
z (cid:24) AR(2) Baseline Low (cid:21) High (cid:21) Low (cid:21) High (cid:21) Hours
z z g g
Natural Rate of Interest
Minimum .10 1.28 2.62 .42 2.55 1.38 1.91
(92:4) (92:4) (92:1) (92:4) (93:1) (92:3) (74:3)
Maximum 5.70 4.52 3.75 4.90 3.93 4.34 4.31
(65:4) (65:2) (65:2) (65:2) (65:2) (65:2) (83:4)
Ending Value 3.40 3.10 3.16 3.16 2.84 3.39 4.04
Trend Growth Rate
Minimum 2.91 2.96 2.91 2.99 3.32 1.99 2.98
(90:4) (91:3) (91:2) (91:3) { (92:2) (80:1)
Maximum 3.73 3.70 3.73 3.68 3.32 4.32 3.86
(65:1) (65:2) (65:2) (65:2) { (65:2) (65:2)
Ending Value 3.31 3.39 3.38 3.36 3.32 3.79 3.46
Output Gap
Minimum -8.04 -8.14 -7.82 -8.36 -7.48 -8.80 -5.77
(82:3) (82:3) (82:3) (82:3) (82:3) (82:3) (75:1)
Maximum 4.11 4.45 3.99 4.61 4.30 4.60 3.03
(66:2) (66:1) (65:4) (66:1) (73:1) (78:3) (66:1)
Ending Value .27 -1.03 -.30 -1.42 -1.69 -.92 .61
Despite the sizeable uncertainty around most of our estimates of the natural rate of
interest, the trend growth rate, and potential output, our point estimates of these processes
are qualitatively similar across the seven modelvariants describedabove. This is illustrated
in Table 4, which shows the minimum, maximum, and ending values of the smoothed
estimates of the natural rate of interest, the trend growth rate, and the output gap. In
(cid:3)
the six cases that exclude the hours equation, r peaked in 1965 and hit its sample low in
(cid:3)
1992 or 1993. In the model augmented with the hours equation, r hits its low in 1973 and
peaks in 1983. All estimates show the trend growth rate peaking in 1965 and the low point
occurringin theearly1990s (theaugmented modelhas two nearlyidentical minima, in1980
and in the early 1990s). The estimates of the output gap are generally similar, with the
peaks occurring in the late 1960s and the mid- and late-1970s; the minimum occurs in the
17

Figure 3: Estimates of the Stance of Monetary Policy
r*
1122 1122
Baseline r* Estimates
1100 Actual Real Funds Rate 1100
88 88
66 66
44 44
22 22
00 00
--22 --22
11996600 11996655 11997700 11997755 11998800 11998855 11999900 11999955 22000000
early 1980s (with the augmented model showing an equally large negative gap in 1975).
5 Monetary Policy and a Time-varying Natural Interest Rate
Allowing for time variation in the natural rate of interest can signi(cid:12)cantly change one’s
(cid:3)
view of the stance of monetary policy duringhistorical episodes in which r strayed from its
(cid:3)
historical average. Figure 3 shows the baseline r estimates (the solid lines), along with the
correspondingactual values of the real fed fundsrate (the dashed lines). The shaded region
(cid:3)
in the (cid:12)gure shows the 70 percent con(cid:12)dence intervals for the r estimates. The estimated
decline in the natural rate during the early 1990s suggests that the stance of policy during
theearly1990s maynothavebeenasexpansionaryasonewouldbelievebasedonaconstant
(cid:3)
value of r . Similarly, monetary policy appears much easier in the late 1960s, relative to
the assumption of a constant natural rate of interest, when one accounts for the boost to
(cid:3)
r resulting from relatively strong trend growth during that period.
(cid:3)
R mismeasurement interferes with the achievement of both inflation and output stabi-
lization goals. The achievement of a long-run inflation rate goal requires that estimates of
(cid:3)
r converge to the true value in expectation. Let policy be described by the interest rate
feedback rule,
i = (cid:25)e+r^ (cid:3) +(cid:11) ((cid:25) −(cid:25) (cid:3) )+(cid:11) y~; (9)
t t t (cid:25) t y t
wherer^ (cid:3) isthepolicymaker’sestimateofthenaturalrateofinterest, (cid:25)e isexpectedinflation,
t
18

Figure 4: Real-time Estimates of the Natural Rate of Interest
5 5
4 4
3 3
2 2
Smoothed (two-sided) r* Estimate
1 Filtered (one-sided) r* Estimate 1
1960 1965 1970 1975 1980 1985 1990 1995 2000
(cid:3)
and (cid:25) is the ((cid:12)xed) long-run inflation target. Absent shocks, if the policymaker’s estimate
converges to r^ (cid:3) , then the inflation rate converges to (cid:25) (cid:3) + 1 (r (cid:3) − r^ (cid:3) ). Hence, if r (cid:3) is
(cid:11)(cid:25)
subject to permanent shifts, then for the inflation rate to stabilize at the target level, the
policymaker’s estimate must converge in expectation to the true value.
(cid:3)
Mismeasurement of r also implies a deterioration in short-run macroeconomic stabi-
lization. In the absence of mismeasurement, a time-varying natural rate of interest has no
implications for the performance resulting from a policy rule of the form of equation (9)
(cid:3)
beyond greater variability of real interest rates. But, r mismeasurement introduces an
additional disturbance to the system, the magnitude of which depends on the variance of
(cid:3)
the r innovations and the persistence of which depends on the Kalman (cid:12)lter gain used in
(cid:3)
updating estimates of r .
(cid:3)
Comparing one-sided and two-sided estimates of r provides a measure of the likely
(cid:3)
magnitude and persistence of r mismeasurement. Figure 4 shows the baseline one-sided
(cid:12)lterestimates (thedashedline)andthetwo-sidedsmoothedestimates(thesolidline)ofthe
naturalrateofinterest. Forcomparison, thesamplemeanofthesmoothedestimate {about
3percent{isshownbythehorizontaldashedline. Theone-sided(cid:12)lterestimatescorrespond
(cid:3) 14
to a \real-time" estimate of r in that past data are used in estimating the state. Taking
the smoothed estimate as truth, the standard deviation of the measurement error using
the one-sided (cid:12)lter is about 0.9 percentage point over the sample; nearly 10 percent of
14The full sample is used toestimate themodel parameters, however, so theanalogy is not exact.
19

(cid:3)
Table 5: E(cid:11)ects of r Mismeasurement under the Taylor Rule
Standard Deviation Loss % Increase
Policymaker’s Estimate of r(cid:3) y~ (cid:25) (cid:1)i L in Loss
True value (r^(cid:3) =r(cid:3)) 1.1 1.4 .7 3.5 {
t t
One-sided KF estimate 1.5 1.4 1.0 4.7 34
Constant (r^(cid:3) =3:0) 1.6 1.6 .7 5.4 53
the existing measurement error is eliminated each quarter. For comparison, the sample
(cid:3)
standard deviation of the smoothed r estimate is 0.8 percentage point, and the (cid:12)rst-order
autocorrelation is 1.00.
(cid:3)
We use simulations of the estimated baseline model to assess the e(cid:11)ects of r mismea-
surement owing to time variation in the natural rate of interest. For these simulations, we
(cid:3)
assume the true values of potential output and r are given by the respective two-sided
Kalman (cid:12)lter estimates of our baseline model. We assume that policy is set according to
the Taylor Rule (that is, (cid:11) = (cid:11) = :5), and that the true value for potential output is
(cid:25) y
observed. We conduct three simulations. In one, the policymaker knows the true value of
(cid:3)
r each period. In the second, the policymaker uses the one-sided Kalman (cid:12)lter estimate,
(cid:3)
which corresponds to a \real-time" estimate of r . In the third, the policymaker assumes
(cid:3)
r is a constant 3 percent, equal to the mean value of the two-sided estimate. Note that
we are restricting the scope of mismeasurement to that resulting from the time variation
in the natural rate; we assume that the policymaker correctly knows the sample mean of
(cid:3)
r . Each simulation extends over 1961{2000; to mitigate the e(cid:11)ects of initial and terminal
conditions, the results are computed for 1964{1997 only.
We assumethe policymaker’s objective is tominimize the weighted sumof thevariances
of the output gap, the inflation rate, and the change in the nominal federal funds rate.
Speci(cid:12)cally, we follow Rudebusch and Svensson (1999) and Rudebusch (2001) and specify
the loss function:
1
L = Var((cid:25))+Var(y~)+ Var((cid:1)i); (10)
2
where Var(x) signi(cid:12)es the unconditional variance of variable x.
Model simulations indicate that mismeasurement of the natural rate of interest leads
to a signi(cid:12)cant deterioration in output stabilization, but has relatively modest e(cid:11)ects on
inflation stabilization. The (cid:12)rst three columns of Table 5 report the simulated standard de-
20

viations oftheoutputgap, theinflationrate, andthechange inthenominalfundsrate. The
fourth column reports the value of the loss given by equation (10); the (cid:12)nal column shows
(cid:3)
the percent increase in the loss relative to the case of no r mismeasurement. Assuming
(cid:3)
r is constant increases the loss by over 50 percent relative to the case of no mismea-
surement. Using the one-sided Kalman (cid:12)lter estimate signi(cid:12)cantly improves stabilization
15
performance.
6 Conclusion
In this paper, we have jointly estimated the natural rate of interest, potential output, and
the trend growth rate using the Kalman (cid:12)lter. We (cid:12)nd that the natural rate of interest
shows signi(cid:12)cant variation over the past forty years in the United States. These results
are robust to changes in speci(cid:12)cation. Variation in the trend growth rate is an important
determinant of changes in the natural rate, as predicted by theory. We show that time
variation of the natural rate has important implications for the design and implementation
ofmonetarypolicy. Adjustmenttochanges inthenaturalrateiscrucialfortheachievement
of long-run inflation and short-run stabilization goals. The periods of the late 1960s and
the early 1990s provide particularly acute examples where recognition of the time-varying
nature of the natural rate has a profound influence on the ability to stabilize inflation and
output.
This paper has focused on the postwar U.S. economy. The analytical apparatus can
easily be adapted to other countries and an interesting issue is whether factors can be
identi(cid:12)ed that a(cid:11)ect the long-run natural rate across countries. In addition, this approach
can be extended to estimate the underlying natural rates of other (cid:12)nancial variables, such
as the equity premium or the real exchange rate.
15Rudebusch (2001) claims relatively modest e(cid:11)ects of r(cid:3) mismeasurement based on model simulations
of transitory shocks to r(cid:3) around a known mean. That study implicitly assumes policymakers update
their r(cid:3) estimates, reducing the magnitude and persistence of mismeasurement relative to a constant r(cid:3)
assumption. Inaddition,thecoe(cid:14)cientsofthepolicyfeedbackrulearereoptimizedwhenr(cid:3)mismeasurement
is introduced, reducingthe implied e(cid:11)ects on macroeconomic stabilization.
21

Appendix
This appendix describes the data used in this study. The variable y refers to the log of
real chain-weighted GDP in billions of chained 1996 dollars. The federal funds rate is the
annualized nominal funds rate, with the quarterly (cid:12)gure computed as the average of the
monthly values. Because the federal funds rate frequently fell below the discount rate prior
to 1965, we use the Federal Reserve Bank of New York’s discount rate prior to 1965.
Our measure of inflation is the annualized quarterly growth rate of the price index for
personal consumption expenditures excluding food and energy, referred to as core PCE
inflation. To construct a series for the ex ante real federal funds rate, we compute the
expectation of average inflation over the four quarters ahead from a univariate AR(3) of
inflation estimated over the 40 quarters prior to the date at which expectations are being
formed. To compute these expectations for the early part of our sample, we need to use
inflation data prior to 1959:2, the start of the core PCE inflation series. For these dates we
splice overall PCE inflation to core PCE inflation. Our results do not change perceptibly if
inflation expectations are proxied by a four-quarter moving average of inflation instead of
the forecast from the univariate AR.
The relative price variables included in the inflation equation are core import price
and crude oil import price inflation. The core import price series is the implicit deflator
for imports of nonpetroleum goods. From 1968 on, this series also excludes the prices of
computers and semiconductors. Finally, the hours data are total hours of employees and
self-employed persons in the private nonfarm business sector.
22

References
Andrews,DonaldandWerner Ploberger,\OptimalTestsWhenaNuisanceParameter
Is Present Only Under the Alternative," Econometrica, 1994, 62, 1383{1414.
Bom(cid:12)m, Antulio, \The Equilibrium Fed Funds Rate and the Indicator Properties of
Term-Structure Spreads," Economic Inquiry, October 1997, 35 (4), 830{46.
, \Measuring Equilibrium Real Interest Rates: What can we learn from yields on in-
dexed bonds?," July 2001. manuscript, Board of Governors of the Federal Reserve
System.
Brayton, Flint, Eileen Mauskopf, David Reifschneider, Peter Tinsley, and John
Williams,\TheRoleofExpectationsintheFRB/US Macroeconomic Model,"Federal
Reserve Bulletin, 1997, 83 (4), 227{245.
, John Roberts, and John C. Williams, \What’s Happened to the Phillips
Curve?,"September1999. FEDSPaperNo.1999-49, BoardofGovernorsoftheFederal
Reserve System.
Clark, Peter, \The Cyclical Component of U.S. Economic Activity," Quarterly Journal
of Economics, November 1987, 102, 797{814.
Fuhrer, Je(cid:11)rey C., \Inflation/Output Variance Trade-O(cid:11)s and Optimal Monetary Pol-
icy," Journal of Money, Credit and Banking, May 1997, 29 (2), 214{34.
Gordon, Robert J., \Foundations of the Goldilocks Economy: Supply Shocks and the
Time-Varying NAIRU," Brookings Papers on Economic Activity, 1998, pp. 297{333.
Granger, Clive and Paul Newbold, \Spurious Regressions in Econometrics," Journal
of Econometrics, 1974, 2, 111{120.
Hamilton, James, \A Standard Error for the Estimated State Vector of a State-Space
Model," Journal of Econometrics, 1986, 33, 387{397.
Harvey, Andrew C., Forecasting, Structural Time Series Models and the Kalman Filter,
Cambridge, UK: Cambridge University Press, 1989.
23

Kozicki, SharonandP.A.Tinsley,\ShiftingEndpointsintheTermStructureofInterest
Rates," Journal of Monetary Economics, June 2001, 47 (3), 613{652.
Kuttner, Kenneth,\Estimating Potential OutputasaLatentVariable," Journal of Busi-
ness and Economic Statistics, July 1994, 12 (3), 361{368.
Laubach, Thomas, \Measuring the NAIRU: Evidence form Seven Economies," Review of
Economics and Statistics, May 2001, 83 (2), 218{231.
Levin, Andrew, Volker Wieland, and John C. Williams, \Robustness of Simple
Monetary Policy Rules under Model Uncertainty," in John B. Taylor, ed., Monetary
Policy Rules, Chicago: University of Chicago Press, 1999, pp. 263{299.
, , and , \The Performance of Forecast-Based Monetary Policy Rules under
Model Uncertainty," 2001. Board of Governors of the Federal Reserve System, FEDS
working paper 2001-39.
Maddison, Angus, Monitoring the World Economy, 1820{1992, Paris: Organization for
Economic Co-operation and Development, 1995.
Neiss, Katharine and Edward Nelson, \The Real Interest Rate Gap as an Inflation
Indicator," April 2001. Bank of England working paper No. 130.
Oliner, Stephen D. and Daniel E. Sichel, \The Resurgence of Growth in the Late
1990s: Is Information Technology the Story?," Journal of Economic Perspectives, Fall
2000, 14 (4), 3{22.
Orphanides, Athanasios and Volker Wieland, \Price Stability and Monetary Policy
E(cid:11)ectivenesswhenNominalInterestRatesareBoundedatZero,"1998. FEDSWorking
Paper 1998-35, Board of Governors of the Federal Reserve System.
Reifschneider, David and John C. Williams, \Three Lessons for Monetary Policy in
a Low Inflation Era," Journal of Money, Credit and Banking, November 2000, 32 (4),
936{966.
Roberts, John M., \Estimates of the Producivity Trend Using Time-Varying Parameter
Techniques," Contributions to Macroeconomics, 2001, 1 (1), 1{27.
24

Rotemberg, Julio J. and Michael Woodford, \Real Business-Cycle Models and the
Forecastable Movements in Output, Hours, and Consumption," American Economic
Review, March 1996, 86, 71{89.
and , \An Optimization-Based Econometric Framework for the Evaluation of
Monetary Policy," in \NBER Macroeconomics Annual 1997," Cambridge, MA: The
MIT Press, 1997, pp. 297{346.
Rudebusch, Glenn D., \Is theFed Too Timid?Monetary Policy in an Uncertain World,"
Review of Economics and Statistics, 2001, 83 (2), 203{17.
and Lars E. O. Svensson, \Policy Rules forInflationTargeting," inJohnB.Taylor,
ed., Monetary Policy Rules, Chicago: University of Chicago Press, 1999, pp. 203{253.
Solow, Robert M., \A Contribution to the Theory of Economic Growth," Quarterly
Journal of Economics, February 1956, 70, 65{94.
Stock, James,\UnitRoots,StructuralBreaksandTrends,"inR.EngleandD.McFadden,
eds., Handbook of Econometrics, Vol. 4, Amsterdam: Elsevier, 1994, pp. 2739{2841.
and Mark Watson,\MedianUnbiasedEstimationofCoe(cid:14)cientVarianceinaTime-
Varying Parameter Model," Journal of the American Statistical Association, March
1998, 93, 349{358.
Taylor, John B., \Discretion versus Policy Rules in Practice," Carnegie Rochester Con-
ference Series on Public Policy, 1993, 39, 195{214.
and John C. Williams, \Forecasting with Rational Expectations Models," Decem-
ber 1993. manuscript, Stanford University.
Watson, Mark, \Univariate Detrending Methods with Stochastic Trends," Journal of
Monetary Economics, 1986, 18, 49{75.
Wicksell, Knut,Interest and Prices,London:Macmillan, 1936. translation of1898 edition
by R.F. Kahn.
Woodford,Michael,\ANeo-WicksellianFrameworkfortheAnalysisofMonetaryPolicy,"
September 2000. manuscript, Princeton University.
25

, \The Taylor Rule and Optimal Monetary Policy," American Economic Association
Papers and Proceedings, May 2001, 91 (2), 232{237.
26