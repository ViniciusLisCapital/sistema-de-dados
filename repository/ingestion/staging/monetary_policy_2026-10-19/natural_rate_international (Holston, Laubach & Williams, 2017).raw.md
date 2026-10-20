FEDERAL RESERVE BANK OF SAN FRANCISCO
WORKING PAPER SERIES
Measuring the Natural Rate of Interest:
International Trends and Determinants
Kathryn Holston and Thomas Laubach
Board of Governors of the Federal Reserve System
John C. Williams
Federal Reserve Bank of San Francisco
December 2016
Working Paper 2016-11
http://www.frbsf.org/economic-research/publications/working-papers/wp2016-11.pdf
Suggested citation:
Holston, Kathryn, Thomas Laubach, John C. Williams. 2016. “Measuring the Natural Rate of
Interest: International Trends and Determinants.” Federal Reserve Bank of San Francisco
Working Paper 2016-11. http://www.frbsf.org/economic-research/publications/working-
papers/wp2016-11.pdf
The views in this paper are solely the responsibility of the authors and should not be interpreted as
reflecting the views of the Federal Reserve Bank of San Francisco or the Board of Governors of
the Federal Reserve System.

Measuring the Natural Rate of Interest:
International Trends and Determinants∗
Kathryn Holston Thomas Laubach
John C. Williams
December 15, 2016
Abstract
U.S. estimates of the natural rate of interest – the real short-term interest rate that
would prevail absent transitory disturbances – have declined dramatically since the
start of the global financial crisis. For example, estimates using the Laubach-Williams
(2003) model indicate the natural rate in the United States fell to close to zero during
the crisis and has remained there into 2016. Explanations for this decline include
shifts in demographics, a slowdown in trend productivity growth, and global factors
affecting real interest rates. This paper applies the Laubach-Williams methodology to
the United States and three other advanced economies – Canada, the Euro Area, and
the United Kingdom. We find that large declines in trend GDP growth and natural
rates of interest have occurred over the past 25 years in all four economies. These
country-by-countryestimatesarefoundtodisplayasubstantialamountofcomovement
over time, suggesting an important role for global factors in shaping trend growth and
natural rates of interest.
JEL classification: C32, E43, E52, O40.
Keywords: natural rate of output, monetary policy rules, Kalman filter, trend growth.
∗This paper has benefitted from comments by our discussants Emanuel Mo¨nch and Kenneth West and
other participants at the 2016 NBER ISOM conference as well as from discussions with Vasco Cu´rdia,
Marc Giannoni, Benjamin Johannsen, Oscar Jorda, Elmar Mertens, and Edward Nelson. We also thank
representatives from the European Central Bank for making available the Area-Wide Model database and
the Bank of England for sharing results from their DSGE model. The views expressed herein are those of
the authors and do not necessarily reflect those of the Board of Governors, or anyone else in the Federal
Reserve System.
Holston: Board of Governors of the Federal Reserve System, Kathryn.A.Holston@frb.gov.
Laubach: Board of Governors of the Federal Reserve System, Thomas.Laubach@frb.gov.
Williams: Federal Reserve Bank of San Francisco, John.C.Williams@sf.frb.org.

1 Introduction
Since Knut Wicksell introduced in 1898 the idea of the natural rate of interest– which we
definetobetherealshort-terminterestrateconsistentwithoutputequalingitsnaturalrate
and constant inflation – it has played a central role in macroeconomic and monetary theory
(Wicksell, 1936). The natural or “equilibrium” real interest rate provides a benchmark for
measuring the stance of monetary policy, with policy expansionary (contractionary) if the
short-term real interest rate lies below (above) the natural rate. This role is illustrated
clearly in monetary policy rules such as the Taylor (1993) rule, according to which the real
interest rate exceeds the natural rate when inflation exceeds its target rate and vice versa,
all else equal. It also provides an anchor for the behavior of interest rates more generally,
once cyclical or other factors have died out.
Althougheconomictheoryprovidesinsightsintothevariousfactorsaffectingthenatural
rateofinterest(see, forexample, CongressionalBudgetOffice2014; InternationalMonetary
Fund 2014; Council of Economic Advisers 2015; Eggertsson et al. 2015; Rachel and Smith
2015; Pescatori and Turunen 2015; Hall 2016; Gagnon et al. 2016), measurement of the
natural rate of interest has proven more challenging. This arises because the natural rate,
like other latent variables, must be inferred from the data rather than directly observed.
This is a particularly relevant topic today. Sustained extraordinarily low interest rates in
most advanced economies since the global financial crisis have heightened interest in the
question of whether the natural rate of interest has permanently declined and why.
Analysis based on U.S. data suggests that the natural rate of interest has moved sig-
nificantly lower over the past quarter century, with a sharp drop occurring over the past
decade (Williams 2015). This finding is robust to alternative methodologies (Hamilton et
al. 2015; Kiley 2015; Lubik and Matthes 2015; Laubach and Williams 2016; Johannsen
and Mertens 2016; Juselius et al. 2016). In this paper, we extend this analysis to other
advanced economies.1 We estimate a version of the Laubach and Williams (2003) model
of the natural rate of interest, originally developed for the U.S. economy, using data from
four economies: the United States, Canada, the Euro Area, and the United Kingdom. This
model applies the Kalman filter to data on real GDP, inflation, and the short-term interest
rate to extract highly persistent components of the natural rate of output, its trend growth
1For earlier studies on the natural rate of interest in the Euro Area, see Giammariou and Valla (2003),
and M´esonnier and Renne (2007).
1

rate, and the natural rate of interest.
Our approach contrasts with other research that has focused on short-term fluctuations
in the natural rate of interest, assuming the longer-run value is constant (Neiss and Nelson
2003, Woodford 2003, Andres et al., 2009, Barsky et al., 2014). Recent analysis using
dynamicstochasticgeneralequilibrium(DSGE)modelsalsofindsevidenceofalargedecline
in the natural rate of interest since the onset of the global financial crisis (Cu´rdia 2015;
Cu´rdia et al., 2015; Goldby et al., 2015). Although the definitions and methods differ
across studies, we view the shorter-term perspective in these studies to be complementary
to our longer-run approach.
Our analysis yields four key results. First, we find evidence of time-variation in the
naturalrateofinterestinallfoureconomies. Second,thereisadownwardtrendinestimated
natural rates of interest: Toward the end of our sample, the estimated natural rates of
interest in all four economies have fallen to historically low levels. This is in large part
explained in our model by a significant decline in the estimated trend growth rates found in
all four economies, but other highly-persistent factors also appear to be at work. We find
no evidence that the natural rates are moving back up recently. Third, although estimation
is done on a economy-by-economy basis, there is substantial comovement in the estimates
of the natural rates of interest and trend GDP growth across economies. This suggests
an important role for so-called global factors influencing the natural rates. Finally, the
estimates of the natural rate of interest are highly imprecise, reinforcing a key finding of
the original Laubach and Williams (2003) paper. In fact, the natural rate estimates for the
other three economies are more imprecise than those for the United States.
Ourfindingofsizabledeclinesinthenaturalrateofinterestinseveraladvancedeconomies
is consistent with the results of other studies that use various approaches to estimate the
natural rate. For example, Constˆancio (2016) reports sharp declines in estimates of the
natural rate in the Euro Area from three different models. Similarly, Mendes (2014) finds
evidence of a significant decline in the natural rate in Canada. Fujiwara et al. (2016) esti-
mate that the natural rate of interest has declined to close to zero in Japan. The coincident
decline in the estimated natural rate across all of these countries highlights the importance
of global factors in determining the natural rate.
Thepaperisorganizedasfollows. Thesecondsectionlaysoutthetheoreticalmodeland
its empirical counterpart. The third section reports the estimation results. The fourth sec-
2

tion analyzes the movements in the natural rates of interest over time and the comovement
across economies. The final section concludes.
2 An Empirical Framework for Estimating the Natural Rate
Our empirical approach to estimating the natural rate of interest draws on two separate
strands of literature. As discussed in the introduction, we follow Wicksell in defining the
natural rate as the real rate of interest consistent with stable inflation and output being at
its natural rate. This definition is akin to the one developed in the DSGE literature (e.g.
Woodford 2003), and hence we build on the New Keynesian framework of a Phillips curve
relationshipandanintertemporalISequationtodescribethedynamicsgoverningtheoutput
gap and inflation as a function of the real rate gap. However, we relax the assumptions
about the steady state that most DSGE models use to derive log-linear approximations of
the dynamics of inflation and the output gap. In particular, key parameters that are being
treatedasfixedinthatliterature, suchasthegrowthrateoftechnologyandtherateoftime
preference of the representative household, may in fact be subject to highly persistent, but
difficult-to-detect fluctuations (e.g. Stock and Watson 1998). Thus, whereas in the DSGE
literature the natural rate of interest is a stationary linear combination of transitory shocks
to preferences and technology, in our framework we explicitly allow for the natural rate to
be affected by low-frequency nonstationary processes.2
2.1 Description of the model
A useful starting point for modeling the natural rate of interest is the neoclassical growth
model. For a representative household with CES preferences, that model implies that
the natural rate of interest varies over time in response to shifts in preferences and the
growth rate of output. In a non-stochastic steady state, household intertemporal utility
maximization yields the relationship between the steady-state real one-period interest rate
r∗ and steady-state growth:
1
r∗ = g +θ, (1)
c
σ
2As discussed below, a further difference between our measure of the natural rate and that from DSGE
models is that we allow for shocks that have transitory effects on the output gap and inflation but that we
do not measure as part of the natural rate, so as to focus on the low-frequency determinants of that rate.
By contrast, the natural rate concept estimated in DSGE models is defined as the rate that achieves price
stability period-by-period.
3

whereσ denotestheintertemporalelasticityofsubstitutioninconsumption,g isthegrowth
c
rate of per capita consumption, and θ is the rate of time preference. This steady-state
relationship is shared by standard monetary DSGE models, and hence the value given by
(1) provides the appropriate intercept for simple interest rate rules in such models.
The purpose of our study is to model the natural rate of interest as a time-varying
process that is subject to potentially permanent changes and to provide estimates of this
process for several major economies. Roberts (2001), Edge et al. (2007), and Kahn and
Rich (2007) provide evidence of shifts in the trend growth rate of labor productivity in the
United States, suggesting one source of persistent movements in the natural rate of interest;
other potential sources of highly persistent changes in r∗ could be related to shifts in fiscal
policy (Laubach 2009) or changes in the global supply of savings (Bernanke 2005, Council
of Economic Advisers 2015).
Given our focus on the international dimension of influences and determinants of the
natural rate, we start from the inflation and output gap dynamics described by the open-
economyversionoftheNewKeynesianmodel(Gal´ı2008). Thesedynamicsaresummarized
by a Phillips curve
π = βE [π ]+κy˜ (2)
H,t t H,t+1 t
and an IS equation of the form
y˜ = E [y˜ ]−σ−1(i −E [π ]−rn). (3)
t t t+1 t t H,t+1 t
In these equations, π denotes the growth rate of prices of domestically produced goods, y˜
H,t t
theoutputgap, andi thesafeone-periodnominalinterestrate. Theparametersκandσ in
t
these equations are functions of underlying parameters describing households’ preferences
and technology, such as the intertemporal elasticity of substitution in consumption, the
substitutability of home and foreign goods in households’ preferences, the price adjustment
frictions etc.
It is worth noting two properties of the variable rn in (3). In the simple model (2)-(3),
t
this variable summarizes all shocks affecting inflation and the output gap, and setting the
real rate gap i −E [π ]−rn to zero period-by-period completely stabilizes these two
t t H,t+1 t
variables. Second, in contrast to a closed economy, the variable rn depends not only on
t
expected domestic output growth but in general also on expected world output growth.
4

While we will depart in the following from the first property, the dependence of the natural
rate of interest on global as well as domestic conditions is central to our analysis.
The equations we use for estimating the natural rate of interest relax the restrictions
imposed by the New Keynesian model along two dimensions. First, we work with reduced-
form equations that are somewhat agnostic about the precise lead-lag relationships among
the endogenous variables. Doing so reduces the risk that our natural rate estimates are
unduly affected by estimates of structural parameters based on potentially misspecified
output gap and inflation dynamics. Second, we allow for the presence of shocks that affect
the output gap and inflation but not the natural rate of interest, which we define as a
low-frequency concept. In particular, we estimate the following equations:
2
y˜ = a y˜ +a y˜ + a r (cid:88) (r −r∗ )+(cid:15) (4)
t y,1 t−1 y,2 t−2 2 t−j t−j y˜,t
j=1
π = b π +(1−b )π +b y˜ +(cid:15) . (5)
t π t−1 π t−2,4 y t−1 π,t
where y˜ = 100∗(y −y∗), y and y∗ are the logarithms of real GDP and the unobserved
t t t t t
natural rate of output, respectively, r is the real short-term interest rate, π denotes con-
t t
sumer price inflation, and π is the average of its second to fourth lags.3 The presence of
t−2,4
the stochastic terms (cid:15) and (cid:15) captures transitory shocks to the output gap and inflation,
y˜,t π,t
while movements in r∗ reflect persistent shifts in the relationship between the real short-
t
term interest rate and the output gap (Williams 2003). The distinction between shocks of
different persistence reflects our focus on a concept of the natural rate of interest as re-
flected in the intercept of simple interest rate rules; more transient shocks would leave this
intercept unchanged, as the monetary policy response to such shocks would be governed by
the response to output and inflation gaps prescribed by such a rule.
Based on the theoretical link between the natural rate of interest and output (or con-
sumption) growth noted above, we assume that the law of motion for the natural rate of
interest is given by:
r∗ = g +z , (6)
t t t
where g is the trend growth rate of the natural rate of output and z captures other
t t
3The open-economy version of the New Keynesian Phillips curve (2) describes a relationship for home-
goodsinflationπ . Intheabsenceofdataforsuchaconcept,weusemeasuresofconsumerpriceinflation
H,t
described in the Appendix.
5

determinants of r∗. Note that we assume a one-for-one relationship between the trend
growth rate of output and the natural rate of interest, which corresponds to assuming
σ = 1 in equation 1. In Laubach and Williams (2003), we estimated this relationship and
found a coefficient of close to unity. Because this relationship is not well identified in the
data, we chose to impose a coefficient of unity.4
We specify log potential output as a random walk with a stochastic drift g that itself
follows a random walk:
y∗ = y∗ +g +(cid:15) , (7)
t t−1 t−1 y∗,t
g = g +(cid:15) . (8)
t t−1 g,t
This specification implies that potential output is integrated of order 2. In particular, an
innovation(cid:15) hasapermanenteffectonthelevelofpotentialoutput,butonlyaone-period
y∗,t
effect on its rate of change, while an innovation (cid:15) permanently affects the growth rate of
g,t
potential output. Stock and Watson (1998) examine the hypothesis that U.S. log real GDP
over the post-WW II period is integrated of order 2 and find evidence in support of a slow-
moving and apparently nonstationary trend growth rate. We view the I(2) specification as
agnostic for the purpose of estimation, as it avoids having to estimate the unconditional
mean of real GDP growth. Finally, we assume that z also follows a random walk,
z = z +(cid:15) . (9)
t t−1 z,t
We assume (cid:15) ,(cid:15) , and (cid:15) are normally distributed with standard deviations σ , σ ,
y∗,t g,t z,t y∗ g
andσ respectivelyandareseriallyandcontemporaneouslyuncorrelated. Equations(7)–(9)
z
constitute the transition equations of our state-space model.
2.2 Empirical implementation
Given that the model is linear in the unobserved state variables, we apply the Kalman filter
to estimate, for each economy, the natural rate of output, its trend growth rate, and the
natural rate of interest (or alternatively the component z unrelated to trend growth). The
data and specifics of model variables are described in the Appendix.
The time series and survey evidence suggests that real GDP growth, labor productivity
4See Hamilton et al. (2015) and Laubach and Williams (2016) for further discussion.
6

growth, and real interest rates are subject to highly persistent changes masked by volatile
transitory shocks. Maximum likelihood estimates of the standard deviations of the innova-
tionstoz andthetrendgrowthrate,σ andσ ,arethereforelikelytobebiasedtowardszero
g z
owing to the so-called “pile-up problem” discussed in Stock (1994). We therefore use Stock
and Watson’s (1998) median unbiased estimator to obtain estimates of the ratio λ ≡
σg
g σ y∗
and λ ≡ arσz.5 We impose these ratios when estimating the remaining model parameters
z σy˜
(including σ and σ ) by maximum likelihood.
y˜ y∗
Our estimation method proceeds in sequential steps. In the first step, we follow Kuttner
(1994) and apply the Kalman filter to estimate the natural rate of output, omitting the real
rategaptermfromequation(4)andassumingthatthetrendgrowthrate,g,isconstant. We
compute the exponential Wald statistic of Andrews and Ploberger (1994) for a structural
break with unknown break date from the first difference of this preliminary estimate of the
natural rate of output to obtain the median unbiased estimate of λ . In the second step,
g
we impose the estimated value of λ from the first step and include the real interest rate
g
gap in the output gap equation under the assumption that z is constant. We estimate the
five model equations and apply the exponential Wald test for an intercept shift in the IS
equation at an unknown date to obtain an estimate of λ .
z
In the final step, we impose the estimated values of λ from the first step and λ from
g z
the second step and estimate the remaining model parameters by maximum likelihood
as described by Harvey (1989).6 Throughout, we impose the constraints that the slope
a of the IS equation is negative and the slope b of the Phillips curve is positive. We
r y
view these as minimal priors on the structure of the model that, in the event, facilitate
the convergence of the numerical optimization during estimation. We compute confidence
intervals and corresponding standard errors for the estimates of the states using Hamilton’s
5Substituting (6) into (4), the latter can be written as
a a
y˜ =a y˜ +a y˜ + r(r +r −(g +g ))− r(z +z )+(cid:15)
t y,1 t−1 y,2 t−2 2 t−1 t−2 t−1 t−2 2 t−1 t−2 y˜,t
The ratio λ based on the test statistic for an intercept shift at an unknown date in this equation is thus
z
the ratio of a σ to σ .
r z y˜
6The vector of unobserved states in the first-stage estimation includes three lags of potential output; in
thesecondstageitalsoincludesonelagofg;andinthethirdstage,asecondlagofg plustwolagsofz. We
compute the conditional expectation and covariance matrix of the initial state, key inputs for the Kalman
filter, as follows. For the lags of potential output, we apply the HP filter with λ=36,000 to log real GDP
data starting four quarters prior to our estimation sample and take the values of the HP trend component
for the three quarters prior to the sample start. For lags of g, we use the first difference of the HP trend.
The component z is initialized at 0. We compute the covariance matrix of these states from the gradients
of the likelihood function.
7

(1986) Monte Carlo procedure that accounts for both filter and parameter uncertainty.7
3 Estimation Results
In this section, we report the model estimation results for the four economies. We start
by discussing the parameter estimates and then turn to the resulting estimates of trend
growth. The estimates of the natural rate of interest are discussed in the following section.
3.1 Parameter Estimates
Table 1 reports the estimation results for the four economies. For three of the economies,
the sample spans 223 quarters from 1961:I to 2016:III, while data availability for the Euro
Area dictates a sample start in 1972:I.
Focusing first on the estimates for the United States, the values for λ and λ indicate
g z
substantial time variation in trend growth and the natural rate of interest over the 56-year
sample. For example, the estimates of the standard deviation of (cid:15) and the first difference
g
of r∗ imply that the standard deviations of g −g and r∗ −r∗ are on
2016:III 1961:I 2016:III 1961:I
the order of 1.8 percent and 2.9 percent, respectively (the results for both variables are
expressed at annual rate). The 90 percent confidence interval for λ , computed by Monte
g
Carlo simulations, ranges from 0.004 to 0.132.8
Theslopecoefficientsa andb fortheU.S.arereasonablylargeandpreciselyestimated,
r y
suggesting that both the output gap and the real rate gap are well identified. Nonetheless,
even with hindsight, the natural rate of interest is estimated imprecisely, with a sample
average standard error of 1.1 percentage points, as shown in the section of Table 1 labeled
“S.E. (sample ave.).” The imprecision in estimates of the natural rate of interest is even
greater when examining the one-sided estimates of r∗ that correspond more closely to “real-
7Wedrawtheparametervectorsfromanormaldistributionwiththecovariancematrixoftheparameter
vector computed as the outer product of the gradients. During these draws, we impose in addition to
the constraints a ≤ −0.0025 and b ≥ 0.025 the constraint that a +a < 1. Discarding draws that
r y y,1 y,2
violate either of these constraints reduces the width of the standard errors, substantially so for the Euro
Area and the UK. The initial value of the state vector is drawn from a normal distribution with the mean
and covariance given by the smoothed estimate of the initial state and its covariance matrix. Note that
these estimated confidence intervals hold the imposed values of λ and λ fixed but take into account the
g z
uncertainty regarding σ
y˜
, σ
π
, and σ y∗.
8To compute thisconfidenceinterval, weuseparameterestimatesbasedon thesecond-stagemodel with
a time-varying trend growth and a constant natural rate of interest to construct 10,000 simulated series of
{y∗,g }. For each pair of simulated series we compute the exponential Wald statistic for an intercept shift
t t
in the first difference of y∗.
t
8

time”estimates, inthat only currentandpastobservations areusedinestimatingthestate.
(Because the full sample is used in estimating the model parameters, the analogy, however,
isnotexact.) Thefinalobservationstandarderrorsshownatthebottomofthetable, which
provide a measure of the imprecision of one-sided estimates assuming the true values of λ
g
and λ are known, are even wider.
z
Comparing parameter estimates across countries, the estimates of λ indicate time vari-
g
ation in the trend growth rate, albeit at a smaller scale in the Euro Area and the UK. Even
though the estimates of λ are of similar magnitude across countries, the time variation of
z
r∗ is magnified for the Euro Area and the UK by the smaller values of the slope parameter
a for these economies. Moreover, it is evident that the uncertainty around the natural
r
rate estimates is closely related to the statistical significance of the slope parameters a
r
and b . For Canada, although a is of similar magnitude as in the U.S. and is statistically
y r
significant, the fact that b is both smaller and less precisely estimated implies that the
y
average standard errors around y∗ and r∗ are larger than in the U.S. For the Euro Area,
the slope of the IS equation is considerably flatter, and the average standard error for r∗ is
very large, primarily driven by draws of the parameter vector in which a is very close to
r
zero and hence r∗ is barely identified.9
The parameter estimates for the UK are in several respects quite different from those
for the other economies. Notably, the output gap is estimated to be much less persistent,
(cid:80)
as shown by the smaller value for a , but inflation responds very strongly to these more
y
transitory output gap fluctuations, with b being about ten times the size compared to its
y
value for the other three economies. By contrast, this output gap estimate seems to bear
little relation to the real rate gap, witha estimated to be close to zero. Inflation also seems
r
to be less well explained by its own lags and the lagged output gap, as shown by the very
large standard deviation σ .
π
It is important to stress that the estimates of the unobserved variables – the level of
potential output, the trend growth rate of potential output, and the natural rate of interest
–areimpreciselyestimated,asseeninthelowerportionofTable1. Thisimprecisionreflects
both the “standard” uncertainty associated with estimated parameters that would obtain
9The fact that more probability mass of the distributions of a and b is located close to zero is also
r y
reflected in the number of draws during the computation of the standard errors that are being rejected
becausetheyviolatetheconstraintsa ≤−0.0025andb ≥0.025. Whileonlyabout2percentofdrawsare
r y
rejectedfortheUS,about15percentarerejectedfortheUK,20percentfortheEuroArea,and25percent
are rejected for Canada.
9

even if these variables were assumed to be constant, as well as the uncertainty associated
with time-variation in these variables. The imprecision is particularly pronounced in the
cases of the natural rate of interest in the Euro Area and the United Kingdom, where the
error bands are very wide reflecting the imprecision of the estimate of the slope coefficient,
a , in the output gap equation.
r
3.2 Estimates of the Output Gap and Trend GDP Growth
The upper panels of Figure 1–4 show the filtered (one-sided) estimates of the output gap
for the four economies. The shaded regions indicate the periods of recessions for each
economy.10 With a few exceptions, large downward movements in estimated output gaps
generallyconformtothetimingofrecessions. Allfoureconomiesexperiencenegativeoutput
gaps following the global financial crisis. However, output gaps after the crisis are generally
less negative (or more positive) than some other estimates (for example, the International
Monetary Fund 2015). The subdued declines in estimated output gaps in our model likely
reflects the relatively modest falloff in core inflation in the four economies, which in the
context of the model is at odds with the presence of large negative output gaps (Laubach
and Williams 2016).
The upper panels of these four figures show the estimated real interest rate gap – the
difference between the ex ante real interest rate and the filtered estimate of the natural rate
of interest. Consistent with the model structure, following periods when the real rate gap is
positive, the estimated output gap tends to be declining; when real rate gaps are negative,
the output gap tends to be rising.
A striking finding common to all four economies is the secular downward trend in the
estimated trend growth rates of output over the past 25 years. This process appeared to
accelerate in the final part of the sample, with trend potential output growth slowing by a
percentage point on average over 2007–2016. Except for the Euro Area, these declines are
concentrated in the 2008-09 period of the global financial crisis and its aftermath, as shown
by the dashed lines in the lower panels of Figures 1–4. In these three regions, trend growth
hasremainedrelativelystableatitsnewlowerlevelsince2010. Incontrast, estimatedtrend
growthintheEuroAreafellbyarelativelymodestamountduringtheglobalfinancialcrisis,
10The following sources are used for recession dating in the figures United States: National Bureau of
Economic Research; Canada and the United Kingdom: Economic Cycle Research Institute; Euro Area:
CEPR Euro Area Business Cycle Dating Committee.
10

but has been on a steady downward trajectory following the onset of the Euro crisis.
TheestimateddeclinesintrendGDPgrowthoverthepastdecadearebroadlyconsistent
with, but often somewhat larger than, estimates by other economists. Table 2 reports the
estimated trend growth rate of potential output for the years 1990, 2007, and 2016, as
well as estimates of long-run growth from alternative sources. In the case of the United
States, our 2016 estimate of trend growth of 1.5 percent is lower than that of professional
forecasters, but in line with the estimates by the International Monetary Fund (2016) and
Fernald (2016). It is also close to the most recent median projection of 1.8 percent by
the Federal Open Market Committee (Board of Governors of the Federal Reserve System
2016). Our 2016 estimate for trend growth of 1.5 percent in Canada is essentially identical
to that from the Bank of Canada (Agopsowicz et al. 2016, Bank of Canada 2016), but
about 1/2 percentage point below estimates by the IMF and professional forecasters. Our
2016 estimate of trend growth for the Euro Area of only 1.1 percent is between 1/4 and 1/2
percentage points below the long-run forecasts from the IMF and professional forecasters.
Finally, our trend growth forecast for the United Kingdom of 1.9 percent is close to that of
the IMF and slightly below that of professional forecasters.
This pattern of declining trend GDP growth in advanced economies is consistent with
alternativeestimatesbasedonmethodologiesthatdecomposepotentialoutputintoitscom-
ponent parts (see Fleischman and Roberts, 2011; Congressional Budget Office, 2016; and
International Monetary Fund 2015). These analyses highlight the roles of slowing labor
force growth due to demographics and a slowdown in trend productivity growth. The pro-
ductivity slowdown in the United States is documented by Byrne et al. (2016), Fernald
(2016), and Gordon (2016), and the European productivity slowdown is analyzed in Cette
et al. (2016).
3.3 Estimated Natural Rates of Interest
Although the estimated natural rates of interest differ across economies owing to idiosyn-
cratic influences, all exhibit two phases of significant and sustained declines over the past
quarter century: First, a moderate secular decline over 1990-2007, and second, a more sub-
stantial decline since 2007. These are seen in the lower panels of Figures 1–4 and in Table
3, which reports the annual averages of the natural rate estimates for the three years 1990,
2007, and 2016. In 1990, the estimates range between about 2-1/2 and 3-1/2. In each
11

case, the estimates are lower in 2007, on the eve of the global financial crisis, ranging from
roughly 2 to 2-1/2 percent. In Canada and the Euro Area, this initial decline is more than
fully accounted for by the estimated decline in the trend growth rate of potential output, as
reported in Table 2. For the United States and the United Kingdom, declines in both trend
growth of potential output, g, and the random walk factor, z, contribute to the decline in
the estimated natural rate over this period.
Estimated natural rates of interest plummeted for all four regions in the immediate
aftermath of the global financial crisis (Figures 1-4). Estimates for Canada and the United
States then edged down further over 2010-2016, and are close to all-time lows at the end
of our sample. In contrast to the results for Canada and the United States, natural rate
estimates for the Euro Area and the United Kingdom rebounded in 2010, but then fell
sharply again following the Euro crisis. In Canada, the United States, and the United
Kingdom, most of the overall decline in the natural rate from 2007 to 2016 is accounted for
by a drop in the estimated trend growth rate. In the Euro Area, declining trend growth
accounts for less than half of the overall fall in the natural rate of interest.
This pattern of a secular decline in real interest rates is seen in market-based measures
and survey data as well. As discussed in Laubach and Williams (2016) and reported in
Table 3, yields on inflation-protected Treasury securities and surveys of economists display
a sustained downward trend in the United States. We do not have a consistent time series
of long-run forecasts for interest rates in the other regions. However, for Canada, the Euro
Area, and the United Kingdom, real yields five to ten years ahead show significant declines
aswell. Becausethesemarket-measuresembedtime-varyingriskandliquiditypremiums,we
caution against ascribing too much weight to the specific numbers and focus more broadly
on the overall direction.
3.4 Robustness
Estimates of the natural rate of interest are inherently imprecise and potentially sensitive
to model specification. A number of papers have explored the sensitivity of estimates of
the natural rate of interest to alternative specifications. Despite substantial differences in
model specification and methodology, this research consistently finds strong evidence of a
sizable decline in the natural rate of interest over the past 25 years, with estimates reaching
historically low levels in recent years.
12

Our natural rate estimates for the United States have been shown to be robust to alter-
nativespecificationsfortheinflationprocessandexpectedinflation(LaubachandWilliams;
2003, 2015). Lubik and Matthes (2015) explore a much more flexible specification of infla-
tion and output in their VAR model. Their model allows for time-variation in all model
parameters and thereby allows for shifts in monetary policy regimes and other structural
changes in the economy. Their estimates of the natural rate display a large decline over
the past decade, reaching roughly zero in 2016. Johannsen and Mertens (2016) develop
a model that combines macroeconomic data with data from the yield curve and also find
that the natural rate of interest has fallen significantly over the past decade, although their
point estimate for 2016 of 0.7 is slightly higher than ours. Estimates of the natural rate
from dynamic stochastic general equilibrium (DSGE) models that explicitly incorporate
forward-looking behavior in output and inflation display a marked decline over the past
decade and continuing very low levels. Although direct comparison between DSGE model
estimates and ours is complicated by the fact that the DSGE concept of the natural rate
is a period-by-period measure of the real rate that would occur absent nominal frictions,
while ours is a medium- or longer-run concept, one can usefully compare our estimates to
themedium-runforecastofrealnaturalratesratesgeneratedbyaDSGEmodel. Themodel
forecasts of the natural rate over the next five years from the DSGE model of Del Negro et
al. (2014) track our estimates reasonably closely over the past 30 years (see also Cu´rdia,
2015).
Although there has not been as much research assessing alternative estimates of the
natural rate of interest for the other three regions, the existing studies also find a significant
drop in the natural rate in recent years. Mendes (2014) examines a number of methods of
estimating the natural rate in Canada and places it in the range of 1-2 percent in 2015,
while the Bank of Canada (2016) reports a range of between 0.75 and 1.75 percent. Our
estimate is in the center of that range. Goldby et al. (2016) report estimates of the natural
rate in the United Kingdom using the Bank of England’s DSGE model. Similar to the
DSGE model evidence for the United States, they find a sizable decline in the natural rate
in the United Kingdom following the global financial crisis. Their DSGE model’s forecast
for the natural rate over the next five years is 1.6 percent in 2016, close to our estimate
of 1.5 percent. Constˆancio (2016) reports estimates of the natural rate in the Euro Area
based on M´esonnier and Renne’s (2007) version of the Laubach-Williams (2003) model, a
13

BayesianVAR,andaDSGEmodel. Allthreemodelsdisplaylargedeclinesintheestimated
natural rate, reaching levels near or below zero at the end of the sample, consistent with
our findings.
4 Global and Local Determinants of the Natural Rate
In this section, we investigate the interdependence of natural rates of interest across the
four economies we study. As discussed earlier, economic theory implies that movements in
natural rate of interest should be correlated across countries. Although such cross-country
linkages were not imposed in estimation, there is evidence of substantial comovement of the
estimates of both the natural rate of interest and the trend growth rate of output over time.
We explore this interdependence using vector error-correction (VECM) models.
4.1 Correlations of Natural Rates Across Regions
The preceding discussion highlighted the downward movements in natural rate estimates
over the past 25 years. In this section, we explore more formally the comovement of nat-
ural rate estimates over the full sample for which we have estimates for all four economies
(1972-2016). As discussed previously, natural rates are assumed to be nonstationary in our
model, and standard augmented Dickey-Fuller tests confirm this, as shown in the upper
part of Table 4. Given this nonstationarity, we cannot use methods that require station-
arity, such as correlations or principal components, to describe natural rate comovement
over time. Instead, we characterize the joint movement in natural rate estimates using a
simple VECM model. Because the natural rates are themselves generated regressors from
the estimated model, care should be taken in interpreting these results and their statistical
significance. Instead, this analysis should be viewed as a simple way to describe the co-
movementevidentintheestimates,withoutputtingmuchcredencetothespecificnumerical
results or inference.
With that caveat in mind, there is evidence of a single cointegrating vector linking the
four natural rates series based on a standard Johansen test. The estimated cointegrating
vectorisreportedinthemiddleportionofTable4. Basedonlagtests, aVECMmodelwith
eight lags is estimated and the key results are reported in the table. The VECM estimates
suggestthatnaturalratescomoveovertime, butarealsosubjecttoidiosyncraticinfluences.
14

Tosummarizetheinterdependenceinnaturalrates,Figure5showsvariancedecompositions
for each natural rate process in terms of shocks to the four natural rates, using a Cholesky
decomposition with ordering: Canada, UK, Euro Area, and the United States. Although
thespecificvaluesofthevariancedecompositionsaresensitivetotheorderingoftheregions,
the overall finding of substantial comovement in the estimated natural rates of interest is
robust.
The variance decompositions indicate the presence of a great deal of interdependence
in natural rates across economies. For example, shocks to the US natural rate contribute
about35percenttonaturalratevariationinCanadaata10-yearhorizon. Shockstonatural
rates in the Euro Area and the UK play a smaller role, but still have a nontrivial effect on
the natural rate in Canada at long horizons. A similar pattern is seen in the Euro Area,
where US natural rate shocks are a major source of natural rate variance at long horizons,
while shocks in the UK have a smaller, but still noticeable effect; in the UK, shocks to the
natural rates in the US and Euro Area are a substantial source of variance as well. The
estimated natural rate in the US is less dependent on those in other regions; however, it is
notcompletelyindependent, witharound20percentofthelong-horizonvarianceemanating
from other economies.
Because the divergences implied by our single cointegrating vector are somewhat puz-
zling in a world of high capital mobility, we also present results from a VECM in which we
impose three cointegrating vectors in the lower portion of Table 4. The variance decom-
positions for each natural rate process, shown in Figure 6, again indicate interdependence
in natural rates. For the Euro Area and the UK, variance in the natural rate of the home
economy is affected by shocks to the other three economies in similar magnitudes as to in
the model with a single cointegrating vector. Shocks to the natural rates in Canada and
the Euro Area are a larger source of natural rate variance in the US under the VECM
with three cointegrating vectors, but the US remains less dependent on other regions. The
variance decomposition for Canada indicates relatively less dependence on natural rates in
other economies.
We also find evidence of comovement in the estimates of trend output growth across the
four economies. Table 5 reports the results of augmented Dickey-Fuller and cointegration
tests for the model estimates of trend GDP growth, as well as results from a VECM with
a single cointegrating vector and one with three cointegrating vectors imposed. The results
15

from both of the estimated VECM models for trend growth rates indicate the presence of
interdependence across countries. The resulting patterns in variance decompositions are
shown in Figures 7 and 8. With the exception of the UK, they are similar to those for the
natural rates of interest. This finding is not entirely surprising since movements in trend
output growth are a major source of time variation in natural rates of interest in our model.
Overall, these results point to the potential for formally incorporating a global factor in
the analysis of trend output growth and the natural rate of interests across countries. Such
an approach is also supported by the evidence of a global factor influencing asset prices
across countries, described by Miranda-Agrippino and Rey (2015). We leave the explicit
modeling and estimation of global and local factors for trend growth rates and natural rates
of interest to future work.
5 Conclusion
In this paper, we estimated the natural rates of interest and output and the trend growth
rate of output in four economies – Canada, the Euro Area, the United Kingdom, and
the United States – using a version of the Laubach-Williams (2003) model. Our findings
mirror those for the United States from earlier research: estimated natural rates of interest
exhibitsignificantvariationovertime,movementsinthetrendgrowthrateareanimportant
determinant of changes in the natural rate, and natural rates of interest have declined over
thepastquartercentury,reachinghistoricallylowlevelsinthemostrecentpast. Inaddition,
and again consistent with past research, natural rate estimates tend to be highly imprecise.
These findings suggest that declining natural rates of interest are an international phe-
nomenon and therefore stem in large part from developments common to many countries,
rather than idiosyncratic national factors. This argues for more research that takes an in-
ternationalperspectiveinanalyzingnaturalrates,byincludingdatafromeconomiesbesides
the United States and by examining structural changes that influence natural rates across
the globe. In addition, research using alternative model specifications more suited for each
economy’s features may yield more precise estimates and insights into the robustness of our
results to alternative approaches.
Finally, as discussed in Laubach and Williams (2016), very low natural rate of inter-
est, if sustained into the future, have profound implications for monetary policy (see also
16

Blanchard, Dell’Ariccia, and Mauro, 2010; Summers 2014). All else equal, a lower average
real interest rate in turn implies that episodes of monetary policy being constrained at the
effective zero lower bound are likely to be more frequent and longer. Moreover, our finding
that natural rates have declined in a number of major advanced economies suggests that
this is not a problem unique to the United States, but has broader consequences globally.
For example, as discussed in Eggertsson et al. (2015), in an environment of a very low
natural rate of interest, the effects of the lower bound on interest rates are amplified and
internationalspilloversandthebenefitsfrominternationalpolicycoordinationmayincrease.
17

6 References
Agopsowicz, Andrew, Dany Brouillette, Shutao Cao, Natalia Kyui and Pierre St-Amant.
2016. “April 2016 Annual Reassessment of Potential Output in Canada,” Bank of
Canada Staff Analytical Note 2016-4, April 2016.
Andr´es, Javier, J. David L´opez-Salido and Edward Nelson. 2009. “Money and the natural
rate of interest: Structural estimates for the United States and the euro area,” Journal
of Economic Dynamics and Control, 33, 758-776.
Andrews,Donald,andWernerPloberger.1994.“OptimalTestsWhenaNuisanceParameter
Is Present Only Under the Alternative,” Econometrica, 62, 1383-1414.
Bank of Canada. 2016. “Monetary Policy Report,” April 2016.
Barsky, Robert, Alejandro Justiniano, and Leonardo Melosi. 2014. “The Natural Rate of
Interest and Its Usefulness for Monetary Policy,” American Economic Review: Papers
& Proceedings, 104(5), 37-43.
Bernanke, Ben S. 2005. “The Global Saving Glut and the U.S. Current Account Deficit,”
Board of Governors of the Federal Reserve System, April 14, 2005.
Blanchard, Olivier, Giovanni Dell’Ariccia, and Paolo Mauro. 2010. “Rethinking Macroeco-
nomic Policy,” IMF Staff Position Note SPN/10/03.
Board of Governors of the Federal Reserve System. 2016. “Minutes of the Federal Open
Market Committee, September 2021, 2016.”
Byrne, David M., Marshall B. Reinsdorf, and John G. Fernald. 2016. “Does the United
States have a Productivity Slowdown or a Measurement Problem?” Federal Reserve
Bank of San Francisco Working Paper 2016-03.
Cette, Gilbert, John G. Fernald, and Benoit Mojon. 2016. “The Pre-Great Recession Slow-
down in Productivity,” Federal Reserve Bank of San Francisco Working Paper 2016-08.
Congressional Budget Office. 2014. “The 2014 Long-Term Budget Outlook.” July 2014.
Congressional Budget Office. 2016. “The Budget and Economic Outlook: 2016 to 2026.”
January 2016.
18

Constˆancio, V´ıtor. 2016. “The challenge of low real interest rates for monetary policy,”
Macroeconomics Symposium at Utrecht School of Economics, 15 June 2016.
Council of Economic Advisers. 2015. “Long-Term Interest Rates: A Survey,” July 2015.
Cu´rdia, Vasco, Andrea Ferrero, Ging Cee Ng, and Andrea Tambalotti. 2015. “Has U.S.
Monetary Policy Tracked the Efficient Interest Rate?” Journal of Monetary Economics,
70, 72-83.
Cu´rdia,Vasco.2015.“WhySoSlow?AGradualReturnforInterestRates,”Federal Reserve
Bank of San Francisco Economic Letter, 2015-32, October 13, 2015.
Del Negro, Marco, Marc Giannoni, and Frank Schorfheide. 2015. “Inflation in the Great
Recession and New Keynesian Models”, American Economic Journal: Macroeconomics,
7(1), January, 168-96.
Edge, Rochelle M., Thomas Laubach, and John C. Williams. 2007. “Learning and Shifts
in Long-Run Productivity Growth,” Journal of Monetary Economics, November, 2421-
2438.
Eggertsson, Gauti B., Neil R. Mehrotra, Sanjay R. Singh, and Lawrence H. Summers. 2015.
“A Contagious Malady? Open Economy Dimensions of Secular Stagnation,” Brown
University, November 20, 2015.
Fagan, Gabriel, Jerome Henry, and Ricardo Mestre. 2001. “An Area-Wide Model (AWM)
for the Euro Area,” European Central Bank Working Paper Series No. 42, January.
Fernald, John G. 2016. “Reassessing Longer-Run U.S. Growth: How Low?” Federal Reserve
Bank of San Francisco Working Paper 2016-18, AUgust 2016.
Fleischman, Charles A., and John M. Roberts. 2011. “From Many Series, One Cycle: Im-
proved Estimates of the Business Cycle from a Multivariate Unobserved Components
Model,” Finance and Economics Discussion Series Divisions of Research & Statistics
and Monetary Affairs Federal Reserve Board, Washington, D.C. 2011-46.
Fujiwara, Shigeaki, Yuto Iwasaki, Ichiro Muto, Kenji Nishizaki, and Nao Sudo. 2016. “De-
velopmentsintheNaturalRateofInterestinJapan,”BankofJapanReview,2016-E-12,
October 2016.
19

Gagnon, Etienne, Benjamin K. Johannsen, and David Lopez-Salido. 2016. “Understanding
the New Normal: The Role of Demographics,” Finance and Economics Discussion Series
2016-080.Washington:BoardofGovernorsoftheFederalReserveSystem,October2016.
Gal´ı, Jordi. 2008. Monetary Policy, Inflation, and the Business Cycle: An Introduction to
the New Keynesian Framework, Princeton, NJ: Princeton University Press.
Giammariou, Nicola, and Natacha Valla. 2003. “The Natural real rate of Interest in the
Euro Area,” European Central Bank Working Paper Series No. 233, May.
Goldby, Mike, Lien Laureys and Kate Reinold. 2015. “An estimate of the UK’s natural rate
of interest,” Bank Underground (Bank of England blog), August 11, 2015.
Gordon, Robert J. 2016. The Rise and Fall of American Growth: The U.S. Standard of
Living since the Civil War, Princeton: Princeton University Press.
Hall, Robert E. 2016, “Understanding the Decline in the Safe Real Interest Rate,” Stanford
Univerity, April 20, 2016.
Hamilton, James D. 1986. “A Standard Error for the Estimated State Vector of a State-
Space Model,”Journal of Econometrics, 33, 387-397.
Hamilton, James D., Ethan S. Harris, Jan Hatzius, and Kenneth D. West. 2015. “The
EquilibriumRealFundsRate:Past,Present,andFuture,”presentedattheUSMonetary
Policy Forum, New York, February 27, 2015.
Harvey,AndrewC.1989.Forecasting,StructuralTimeSeriesModelsandtheKalmanFilter,
Cambridge: Cambridge University Press.
International Monetary Fund. 2014. World Economic Outlook: Recovery Strengthens, Re-
mains Uneven, Washington, DC, April.
International Monetary Fund. 2015. World Economic Outlook: Uneven Growth: Short- and
Long-Term Factors, Washington, DC, April.
International Monetary Fund. 2016. World Economic Outlook: Too SLow for Too Long,
Washington, DC, April.
Johannsen,BenjaminK.,andElmarMertens.2016.“ATimeSeriesModelofInterestRates
with the Effective Lower Bound,” Finance and Economics Discussion Series 2016-033.
Washington: Board of Governors of the Federal Reserve System, April 2016.
20

Juselius, Mikael, Claudio Borio, Piti Disyatat, and Mathias Drehmann. 2016. “Monetary
Policy, the Financial Cycle and Ultra-low Interest Rates,” Bank for International Set-
tlements Working Paper No. 569, July.
Kahn, James A., and Robert W. Rich. 2007. “Tracking the new economy: Using growth
theory to detect changes in trend productivity,” Journal of Monetary Economics, 54,
16701701.
Kiley, Michael T. 2015. “What Can the Data Tell Us About the Equilibrium Real Inter-
est Rate?” Finance and Economics Discussion Series 2015-077. Washington: Board of
Governors of the Federal Reserve System, August 2015.
Kuttner, Kenneth. 1994. “Estimating Potential Output as a Latent Variable,” Journal of
Business and Economic Statistics, 12(3), July, 361–368.
Laubach, Thomas. 2009. “New Evidence on the Interest Rate Effects of Budget Deficits and
Debt.” Journal of the European Economic Association, 7(4), 858-885.
Laubach, Thomas, and John C. Williams. 2003. “Measuring the Natural Rate of Interest,”
Review of Economics and Statistics, 85(4), November, 1063-1070.
Laubach, Thomas, and John C. Williams. 2016. “Measuring the Natural Rate of Interest
Redux,” Business Economics, 51, 257-267.
Lubik, Thomas A., and Christian Matthes. 2015. “Calculating the Natural Rate of Interest:
A Comparison of Two Alternative Approaches,” Federal Reserve Bank of Richmond
Economic Brief, October 2015, EB15-10.
Mendes, Rhys R. 2014.“The Neutral Rate of Interest in Canada,” Bank of Canada Discus-
sion Paper/Document danalyse 2014-5, September 2014.
M´esonnier, Jean-St´ephane, and Jean-Paul Renne. 2007. “A time-varying natural rate of
interest for the euro area,” European Economic Review, 51, 1768–1784.
Miranda-Agrippino, Silvia, and H´el`ene Rey. 2015. “World Asset Markets and the Global
Financial Cycle,” Bank of England, October 2015.
Neiss, Katherine S., and Edward Nelson. 2003. “The real interest-rate gap as an in?ation
indicator,” Macroeconomic Dynamics, 7, 239-262.
21

Pescatori, Andrea, and Jarkko Turunen. 2015. “Lower for Longer: Neutral Rates in the
United States,” IMF Working paper 15/135, June 2015.
Rachel, Lukasz, and Thomas D Smith. 2015. “Secular Drivers of the Global Real Interest
Rate,” Bank of England Staff Working Paper No. 571, December.
Roberts, John M. 2001. “Estimates of the Productivity Trend using Time-Varying Param-
eter Techniques,” Contributions to Macroeconomics, 1(1).
Stock, James H. 1994. “Unit Roots, Structural Breaks, and Trends,” in R. Engle and D.
MacFadden (eds.) ‘Handbook of Econometrics,’ Vol. 4, Amsterdam, Elsevier Science,
2739-2841.
Stock, James, and Mark Watson. 1998. “Median Unbiased Estimation of Coefficient Vari-
ance in a Time-Varying Parameter Model,” Journal of the American Statistical Associ-
ation, 93, March, 349–358.
Summers, Lawrence H. 2014. “U.S. Economic Prospects: Secular Stagnation, Hysteresis,
and the Zero Lower Bound,” Business Economics, 49(2), 65-73.
Taylor, John B. 1993. “Discretion versus Policy Rules in Practice,” Carnegie-Rochester
Conference Series on Public Policy, 39, December, 195–214.
Wicksell, Knut. 1936. Interest and Prices (tr. of 1898 edition by R.F. Kahn). London:
Macmillan.
Williams, John C. 2003. “The Natural Rate of Interest,” Federal Reserve Bank of San
Francisco Economic Letter, 2003-32, October 31, 2003.
Williams,JohnC.2015.“TheDeclineintheNaturalRateofInterest,”Business Economics,
50(2), 57-60, April.
Woodford,Michael.2003.Interest and Prices: Foundations of a Theory of Monetary Policy,
Princeton: Princeton University Press.
22

Table 1: Parameter Estimates
Parameter United States Canada Euro Area United Kingdom
Sample 1961-2016 1961-2016 1972-2016 1961-2016
λ 0.053 0.051 0.031 0.023
g
λ 0.030 0.025 0.040 0.024
z
(cid:80)
a 0.942 0.953 0.948 0.916
y
a −0.071 −0.067 −0.036 −0.009
r
(4.063) (2.874) (1.842) (1.682)
b 0.079 0.044 0.065 0.490
y
(3.136) (1.618) (1.760) (2.064)
σ 0.354 0.353 0.290 0.110
y˜
σ 0.791 1.413 1.001 2.737
π
σ 0.575 0.631 0.400 0.878
y∗
σ 0.122 0.129 0.050 0.082
g
σ 0.150 0.131 0.323 0.287
z
(cid:113)
σ = σ2+σ2 0.194 0.184 0.327 0.299
r∗ g z
S.E. (sample ave.)
r∗ 1.072 1.555 3.943 3.336
g 0.402 0.449 0.240 0.417
y∗ 1.504 2.383 1.676 0.876
S.E. (final obs.)
r∗ 1.528 2.193 6.038 4.804
g 0.548 0.600 0.335 0.537
y∗ 1.988 2.970 2.561 0.992
Notes: t statistics are in parentheses; σ is expressed at an annual rate.
g
23

Table 2: Trend Growth Estimates
Change
1990 2007 2016† 1990-2007 2007-2016
United States
HLW g estimates 3.3 2.8 1.5 −0.6 −1.3
Consensus Forecasts 2.4 2.9 2.2 0.5 −0.7
IMF World Economic Outlook 2.6 3.1 1.8 0.5 −1.3
Blue Chip Financial Forecasts 2.5 2.9 2.2 0.4 −0.7
Canada
HLW g estimates 3.5 2.5 1.5 −1.0 −1.0
Consensus Forecasts 2.8 2.5 1.9 −0.4 −0.6
IMF World Economic Outlook 3.2 2.7 2.0 −0.5 −0.7
Euro Area
HLW g estimates 2.7 2.1 1.1 −0.6 −1.0
Consensus Forecasts n/a 2.0 1.3 n/a −0.7
IMF World Economic Outlook n/a 2.0 1.5 n/a −0.6
United Kingdom
HLW g estimates 2.8 2.7 1.9 −0.1 −0.8
Consensus Forecasts 2.5 2.5 2.1 0.0 −0.5
IMF World Economic Outlook 2.5 2.7 2.0 0.2 −0.7
Notes:ConsensusForecastsdataarethemeanofpanellists’trendestimatesofexpectedGDPgrowthinthe
6to10yearsfollowing.IMFestimatesarethe5-yearaheadforecastforrealGDPgrowth.BlueChip
estimatesarethemeanlong-yearsaheadforecastforrealGDP.Foreachofthesethreeforecasts,numbers
aretheaverageoftheSpringandFallpublicationsforeachyear.HLWestimatesareyearlyaverages.
Numbers may not sum due to rounding.
Sources:ConsensusEconomicsInc,London;IMFWorldEconomicOutlook;BlueChipFinancialForecasts.
†2016 estimates are averages of the first three quarters.
24

Table 3: Natural Rate Estimates
Change
1990 2007 2016† 1990-2007 2007-2016
United States
HLW r∗ estimates 3.5 2.3 0.4 −1.2 −1.9
TIPS yields (5-10 years ahead) n/a 2.5 0.8 n/a −1.6
Blue Chip Financial Forecasts 3.1 2.4 0.9 −0.7 −1.6
Canada
HLW r∗ estimates 3.2 2.5 1.3 −0.7 −1.2
Real return bond yields (5-10 years ahead) n/a 2.0 0.4 n/a −1.6
Euro Area
HLW r∗ estimates 2.5 2.1 −0.3 −0.4 −2.4
French euro HICP-linked bond yields n/a n/a 0.0 n/a n/a
(5-10 years ahead)
United Kingdom
HLW r∗ estimates 2.9 2.6 1.5 −0.3 −1.1
Index-linked gilt yields (5-10 years ahead) 4.4 1.5 −0.9 −2.9 −2.4
Notes:Allnumbersareyearlyaverages.BlueChipestimatesarethedifferenceinthemeanlong-yearsahead
forecasts of the federal funds rate and CPI (average of the Spring and Fall publications). The Euro Area
securitiesareOATebondsissuedbyAgenceFranceTr´esorandlinkedtotheEuroAreaharmonizedinflation
index. Zero coupon yields are estimated for Canadian real return bonds. UK yields are calculated using
monthlyaverageyieldsfromthezerocouponrealyieldcurvepublishedbytheBankofEngland.Numbers
may not sum due to rounding.
†2016 estimates are averages of the first three quarters.
25

Table 4: Cointegration: Natural Rate Estimates
United States Canada Euro Area United Kingdom
ADF test (p-value)
1961-2016 0.72 0.81 n/a 0.16
1972-2016 0.90 0.68 0.80 0.18
Difference from US: r∗ −r∗
US Economy
Phillips-Perron test (p-value)
1961-2016 n/a < 0.01 n/a 0.28
1972-2016 n/a 0.06 0.03 0.63
VECM model with 1 cointegrating vector
Cointegrating vector 1.00 −0.48 −0.65 −0.10
(S.E.) (–) (0.12) (0.12) (0.15)
Error-correction coef. 0.01 0.04 0.13 0.09
(S.E.) (0.04) (0.03) (0.04) (0.03)
Granger lag test (p-value) 0.55 0.01 0.90 < 0.01
(8 lags)
VECM model with 3 cointegrating vectors
Cointegrating vectors 1.00 0.00 0.00 −1.54
(S.E.) (–) (–) (–) (0.18)
0.00 1.00 0.00 −1.38
(–) (–) (–) (0.15)
0.00 0.00 1.00 −1.18
(–) (–) (–) (0.21)
Error-correction coef., resp. < 0.01 0.04 0.14 0.09
(S.E.) (0.04) (0.03) (0.04) (0.03)
0.02 −0.01 −0.10 −0.06
(0.04) (0.02) (0.03) (0.02)
0.03 −0.04 −0.06 −0.03
(0.03) (0.02) (0.03) (0.02)
Granger lag test (p-value) 0.48 0.02 0.88 < 0.01
(8 lags)
26

Table 5: Cointegration: Trend Growth Estimates
United States Canada Euro Area United Kingdom
ADF test (p-value)
1961-2016 0.51 0.81 n/a 0.11
1972-2016 0.88 0.66 0.52 0.45
Difference from US: g −g
US Economy
Phillips-Perron test (p-value)
1961-2016 n/a < 0.01 n/a 0.14
1972-2016 n/a 0.45 0.07 0.69
VECM model with 1 cointegrating vector
Cointegrating vector 1.00 0.14 −1.59 0.04
(S.E.) (–) (0.16) (0.35) (0.23)
Error-correction coef. −0.03 0.04 0.05 0.01
(S.E.) (0.03) (0.02) (0.02) (0.02)
Granger lag test (p-value) 0.01 < 0.01 < 0.01 < 0.01
(8 lags)
VECM model with 3 cointegrating vectors
Cointegrating vectors 1.00 0.00 0.00 −1.30
(S.E.) (–) (–) (–) (0.08)
0.00 1.00 0.00 −1.48
(–) (–) (–) (0.16)
0.00 0.00 1.00 −1.02
(–) (–) (–) (0.06)
Error-correction coef., resp. −0.04 0.06 0.05 0.02
(S.E.) (0.03) (0.03) (0.02) (0.02)
0.08 −0.03 −0.08 0.02
(0.05) (0.04) (0.03) (0.03)
< 0.01 −0.01 0.01 −0.01
(0.02) (0.02) (0.01) (0.01)
Granger lag test (p-value) < 0.01 0.01 < 0.01 < 0.01
(8 lags)
27

Figure 1: Estimation Results for the US
Output Gap and Real Rate Gap
8
Output Gap
Real Rate Gap
4
0
−4
−8
1965 1970 1975 1980 1985 1990 1995 2000 2005 2010 2015
r* and Trend Growth
6
r*
Trend Growth (g)
5
4
3
2
1
0
1965 1970 1975 1980 1985 1990 1995 2000 2005 2010 2015
28

Figure 2: Estimation Results for Canada
Output Gap and Real Rate Gap
10
Output Gap
Real Rate Gap
5
0
−5
−10
1965 1970 1975 1980 1985 1990 1995 2000 2005 2010 2015
r* and Trend Growth
7
r*
Trend Growth (g)
6
5
4
3
2
1
0
1965 1970 1975 1980 1985 1990 1995 2000 2005 2010 2015
29

Figure 3: Estimation Results for the Euro Area
Output Gap and Real Rate Gap
8
Output Gap
Real Rate Gap
4
0
−4
−8
1975 1980 1985 1990 1995 2000 2005 2010 2015
r* and Trend Growth
4
r*
Trend Growth (g)
3
2
1
0
−1
1975 1980 1985 1990 1995 2000 2005 2010 2015
30

Figure 4: Estimation Results for the UK
Output Gap and Real Rate Gap
15 3
Output Gap
Real Rate Gap
10 2
5 1
0 0
−5 −1
−10 −2
−15 −3
1965 1970 1975 1980 1985 1990 1995 2000 2005 2010 2015
paG
etaR
laeR
Output
Gap
r* and Trend Growth
5
r*
Trend Growth (g)
4
3
2
1
0
1965 1970 1975 1980 1985 1990 1995 2000 2005 2010 2015
31

Figure 5: Variance Decompositions of Natural Rate Estimates:
VECM with One Cointegrating Vector
Canada UK
100 100
80 80
60 60
40 40
US r*
20 20
Euro Area r*
UK r*
Canada r*
0 0
0 10 20 30 40 0 10 20 30 40
Period Period
Euro Area US
100 100
80 80
60 60
40 40
20 20
0 0
0 10 20 30 40 0 10 20 30 40
Period Period
32

Figure 6: Variance Decompositions of Natural Rate Estimates:
VECM with Three Cointegrating Vectors
Canada UK
100 100
80 80
60 60
40 40
US r*
20 20
Euro Area r*
UK r*
Canada r*
0 0
0 10 20 30 40 0 10 20 30 40
Period Period
Euro Area US
100 100
80 80
60 60
40 40
20 20
0 0
0 10 20 30 40 0 10 20 30 40
Period Period
33

Figure 7: Variance Decompositions of Trend Growth Estimates:
VECM with One Cointegrating Vector
Canada UK
100 100
80 80
60 60
40 40
US r*
20 20
Euro Area r*
UK r*
Canada r*
0 0
0 10 20 30 40 0 10 20 30 40
Period Period
Euro Area US
100 100
80 80
60 60
40 40
20 20
0 0
0 10 20 30 40 0 10 20 30 40
Period Period
34

Figure 8: Variance Decompositions of Trend Growth Estimates:
VECM with Three Cointegrating Vectors
Canada UK
100 100
80 80
60 60
40 40
US r*
20 20
Euro Area r*
UK r*
Canada r*
0 0
0 10 20 30 40 0 10 20 30 40
Period Period
Euro Area US
100 100
80 80
60 60
40 40
20 20
0 0
0 10 20 30 40 0 10 20 30 40
Period Period
35

Appendix: Data
For each economy, we require data for real GDP, inflation, and the short-term nominal
interestrate,aswellasaproceduretocomputeinflationexpectationstocalculatetheexante
real short-term interest rate r .11 The variable y refers to the log of real GDP. The inflation
t
measure is theannualizedquarterly growth rate ofthe specified consumerprice series. With
theexceptionoftheUnitedStates,forwhichcorepersonalconsumptionexpenditure(PCE)
price data are available over the entire sample, the inflation series is constructed by splicing
the core price index with an all-items price index. We use a four-quarter moving average of
past inflation as a proxy for inflation expectations in constructing the ex ante real interest
rate. Short-term interest rates are expressed on a 365-day annualized basis.
US inflation is constructed using the price index for PCE excluding food and energy,
referred to as core PCE inflation. Real GDP and core PCE data are published by the BEA.
The short-term interest rate is the annualized nominal funds rate, available from the Board
of Governors, with the quarterly figure computed as the average of the monthly values.
Because the federal funds rate frequently fell below the discount rate prior to 1965, we use
the Federal Reserve Bank of New York’s discount rate prior to 1965, reported by the IMF.
Canadian real GDP data is taken from the IFS. The short-term nominal interest rate is
theBankofCanada’stargetfortheovernightrate,takenastheend-of-periodvalueforeach
month and aggregated to quarterly frequency. Since the Bank of Canada began treating the
target rate as its key interest rate in May 2001, we use the bank rate as the short-term
interest rate prior to that date. We use the Bank of Canada’s core Consumer Price Index
to construct our inflation series. Prior to 1984, we use CPI containing all items. With the
exception of real GDP, all data is from Statistics Canada.
UKrealGDPdataaretakenfromtheOfficeofNationalStatistics.Ourinflationmeasure
is CPI excluding food and energy; prior to 1970 we use all-items CPI. Both are from the
OECD. The short-term nominal interest rate is the Bank of England’s Official Lending
Rate, published by the Bank of England.
EuroAreadataisfromtheAreaWideModel(Faganetal.,2001).Theinflationmeasure
is HICP excluding energy; prior to 1988 we use overall HICP. The short-term interest rate
is the three-month rate. We update the three series through 2016 using data from the ECB.
11A detailed description of our data and programs, as well as replication materials, is available on the
Federal Reserve Bank of San Francisco’s website.
36

Figure 9: Comparison of Data across Economies
Inflation
30
Canada
Euro Area 25
UK
US 20
15
10
5
0
−5
1965 1970 1975 1980 1985 1990 1995 2000 2005 2010 2015
Log of Real GDP, HP Cycle Component
0.10
0.05
0.00
−0.05
−0.10
1965 1970 1975 1980 1985 1990 1995 2000 2005 2010 2015
Nominal Short−Term Interest Rate
25
20
15
10
5
0
1965 1970 1975 1980 1985 1990 1995 2000 2005 2010 2015
37

Appendix: Comparison to Laubach and Williams (2003)
In this appendix, we compare the estimates for the United States reported in this paper
with real-time estimates generated using the Laubach-Williams (2003) model, which are
reported on the Federal Reserve Bank of San Francisco’s website. Figure 10 displays the
filtered (one-sided) estimates of the output gap, trend growth of potential output, and
the natural rate of interest, as well as the real rate gap generated using the ex-ante real
short-term interest rate and the filtered natural rate estimates.
As shown in the upper panel, estimates of the output gap and real rate gap in this
paper largely resemble estimates from the LW (2003) model. In general, the trend growth
and natural rate estimates exhibit similar movements across both models, with the recent
decline in the natural rate occurring simultaneously across both sets of estimates. More of
the recent decline in the natural rate is accounted for by a decline in trend growth in the
estimates from this paper than in estimates from the Laubach-Williams model.
One departure in this paper from the Laubach-Williams (2003) methodology is the
method for calculating a measure of inflation expectations, which we use to determine
the real short-term interest rate as described in the Data Appendix. While the Laubach-
Williams (2003) model uses a univariate AR(3) of inflation estimated over the past 40
quarters to generate a forecast of four-quarter-ahead inflation, in this paper we proxy in-
flation expectations using an average of inflation over the prior four quarters. This change
is driven in part by data constraints; for the Euro Area, the estimation sample could not
start prior to 1983q1 if the former method were used. In Figure 11, we compare the two
measures of inflation expectations and find that they are close for the US.
38

Table 6: Comparison of HLW and LW (2003) Parameter Estimates
Parameter HLW: LW (2003): LW (2003):
US Current 2003 Vintage
Sample 1961q1-2016q3 1961q1-2016q3 1961q1-2002q2
λ 0.053 0.014 0.042
g
λ 0.030 0.042 0.058
z
(cid:80)
a 0.942 0.955 0.945
y
a −0.071 −0.057 −0.098
r
(4.063) (3.571) (3.81)
b 0.079 0.041 0.043
y
(3.136) (2.078) (1.63)
c 1.000 1.365 1.068
σ 0.354 0.351 0.387
y˜
σ 0.791 0.764 0.731
π
σ 0.575 0.603 0.605
y∗
σ 0.122 0.034 0.102
g
σ 0.150 0.260 0.323
z
(cid:113)
σ = c2σ2+σ2 0.194 0.264 0.340
r∗ g z
S.E. (sample ave.)
r∗ 1.072 1.886 1.88
g 0.402 0.219 0.48
y∗ 1.504 1.663 3.02
S.E. (final obs.)
r∗ 1.528 3.151 2.61
g 0.548 0.288 0.63
y∗ 1.988 2.925 4.23
Notes: t statistics are in parentheses; σ is expressed at an annual rate.
g
39

Figure 10: Comparison of HLW and LW (2003) Estimates
Output Gap and Real Rate Gap
10
HLW Output Gap
HLW Real Rate Gap
LW (2003) Output Gap
LW (2003) Real Rate Gap
5
0
−5
−10
1965 1970 1975 1980 1985 1990 1995 2000 2005 2010 2015
r* and Trend Growth
8
HLW r*
HLW Trend Growth (g)
LW (2003) r*
LW (2003) Trend Growth (g)
6
4
2
0
1965 1970 1975 1980 1985 1990 1995 2000 2005 2010 2015
40

Figure 11: Comparison of HLW and LW (2003) Measures of Inflation Expectations
12
HLW
LW (2003)
10
8
6
4
2
0
1965 1970 1975 1980 1985 1990 1995 2000 2005 2010 2015
41