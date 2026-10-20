Measuring the Natural Rate of Interest
Thomas Laubach
John C. Williams
Board of Governors of the Federal Reserve System∗
November 2001
Abstract
A key variable for the conduct of monetary policy is the natural rate of interest
– the real interest rate consistent with output equaling potential and stable inﬂation.
Economic theory implies that the natural rate of interest varies over time and depends
on the trend growth rate of output. In this paper we apply the Kalman ﬁlter to jointly
estimate the natural rate of interest, potential output, and its trend growth rate, and
examine the empirical relationship between these estimated unobserved series. We ﬁnd
substantial variation in the natural rate of interest over the past four decades in the
United States. Our natural rate estimates vary about one-for-one with changes in the
trend growth rate. We show that policymakers’ mismeasurement of the natural rate of
interest can cause a signiﬁcant deterioration in macroeconomic stabilization.
JEL classiﬁcation: C32, E43, E52, O40.
Keywords: natural rate of interest, interest rate rules, Kalman ﬁlter, trend growth,
potential output, equilibrium real interest rate.
∗Washington, D.C. 20551, tlaubach@frb.gov, jwilliams@frb.gov. The views expressed herein are those of
the authors and do not necessarily reﬂect those of the Board of Governors of the Federal Reserve System
or its staﬀ. We thank Adam Litwin for excellent research assistance. This research has beneﬁtted from
discussions with Antulio Bomﬁm, Bill English, Michael Kiley, Ed Nelson, John Roberts, Brian Sack, Bill
Whitesell, and participants at sessions at the Econometric Society North American Summer Meeting and
the International Conference of the Society of Computational Economics.

1
Introduction
A key input into the conduct of monetary policy is a measure of the “neutral” stance of
policy, against which one can gauge policy’s stimulative or contractionary impetus. One
such measure, especially prominent in regimes in which the central bank explicitly targets
a monetary aggregate, is the growth rate of a monetary aggregate relative to some trend
or target rate of growth. In the United States and many other countries, however, the
short-term interest rate has become the primary policy instrument. In such regimes, the
“equilibrium” or “natural” interest rate provides a metric for the stance of policy. For this
purpose, it is useful to deﬁne the natural rate of interest to be the real short-term interest
rate consistent with output converging to potential, where potential is the level of output
consistent with stable inﬂation (Cf.
Bomﬁm (1997)).
In this formulation, the natural
rate of interest, hereafter referred to as r∗, represents a medium-run real rate “anchor” for
monetary policy and corresponds to the intercept term in feedback rules such as Taylor’s
(1993) Rule.
Economic theory implies that the natural rate of interest varies over time in response
to shifts in preferences and technology.1 The relationship between r∗and fundamentals is
most clearly illustrated in the context of the standard optimal growth model. The optimality
condition for saving yields a balanced growth condition relating the real interest rate, r, to
preference and technology parameters:
r = 1
σq + n + θ,
(1)
where σ denotes the intertemporal elasticity of substitution in consumption, n is the rate
of population growth, q is the rate of labor-augmenting technological change, and θ is the
rate of time preference.2
This ﬁnding that the real interest rate is positively related to
the rates of trend growth and time preference, holding other factors ﬁxed, holds in a wide
1If not for its time variation, estimation of the natural rate would be relatively straightforward. One
simple approach is to take the sample mean over a relatively long period when inﬂation shows no upward
or downward trend (Cf.
Reifschneider and Williams (2000)).
This method yields an estimate of r∗of
about 3 percent. Alternatively, one can derive an estimate of r∗using an estimated macro model with ﬁxed
parameters (Cf. Taylor and Williams (1993), Orphanides and Wieland (1998), and Rudebusch (2001)).
2For this example, we assume CRRA preferences and that the utility of each future generation is weighted
equally irrespective of size; if, instead, the utility of each generation is weighted according to its size, we
have r = 1
σ q + θ.
1

variety of models.3 In light of the evidence of substantial shifts in the trend growth rate in
the United States and other countries over the past several decades (Cf. Maddison (1995),
Oliner and Sichel (2000), Roberts (2001)), the assumption of a constant natural rate of
interest appears untenable. Moreover, changes in other factors such as ﬁscal policy factors
may induce persistent changes in the natural rate of interest over time.
Our deﬁnition of the natural rate is closely related to Wicksell’s verbal description:
There is a certain rate of interest on loans which is neutral in respect to com-
modity prices, and tends neither to raise nor to lower them.
Wicksell (1936, p. 102)
In characterizing the natural rate of interest, we focus on a medium-run concept of price
stability that abstracts from the eﬀects of short-run price and output ﬂuctuations. In this
respect, our deﬁnition diﬀers from that advanced recently by Woodford (2000), who deﬁnes
the Wicksellian natural rate of interest to be the real rate that yields period-by-period
price stability. Woodford’s characterization of the natural rate does not correspond to the
intercept term in a monetary policy rule that contains independent responses to output and
inﬂation, but instead fully describes the optimal setting of policy for a particular objective
function (Cf. Woodford (2001)). In fact, existing estimates based on this deﬁnition abstract
entirely from lower frequency components of r∗and potential output by using detrended
data (Cf. Rotemberg and Woodford (1997), Neiss and Nelson (2001)). Importantly, these
estimates are very sensitive to the structural assumptions of the particular model, and, as
a result, yield policy prescriptions that are unlikely to be robust to model uncertainty (Cf.
Levin, Wieland and Williams (1999)). In contrast, our goal is to provide a robust method
of identifying lower-frequency movements in r∗that can be included in the kind of “simple”
policy rules that have been shown to perform well in a wide variety of models (Cf. Levin,
Wieland and Williams (2001)).
Because we deﬁne the natural rate of interest in relation to the deviation of output from
potential, estimation of r∗also entails estimation of potential output.4 Moreover, owing to
the theoretical linkage between r∗and the trend growth rate, we are interested in estimating
3For example, if we follow Solow (1956) and assume that the saving rate is constant, then the real
interest rate will also be positively related to the rate of growth and negatively to the saving rate (the latter
presumably negatively related to the rate of time preference). Speciﬁcally, r = α δ+n+q
s
−δ, where s is the
saving rate out of output and δ is the rate of depreciation.
4An alternative would be to specify a reduced-form relationship between the change in the rate of inﬂation
2

both the level of potential output and its trend growth rate. We apply the Kalman ﬁlter
to these unobserved low frequency variables, modeling the cyclical dynamics of output and
inﬂation using a restricted VAR model that imposes relatively little structure on short-run
dynamics. Because the innovation variances to r∗and the trend growth rate are small, we
use Stock and Watson’s (1998) median-unbiased estimates of these coeﬃcients and apply
maximum likelihood to estimate the remaining model parameters.
Time variation in r∗and in particular its real-time mismeasurement is potentially im-
portant for the conduct and performance of monetary policy. In a recent paper, however,
Rudebusch (2001) ﬁnds that transitory shocks to r∗have only modest implications for the
conduct of monetary policy. In this paper, we reexamine this issue in the context of the
estimated highly persistent movements in r∗over history and come to the conclusion that
there are relatively large stabilization losses associated with r∗mismeasurement, and that
these losses can be mitigated by timely updating of r∗estimates.
The remainder of the paper is organized as follows. The next section describes the empir-
ical framework used for estimating the natural rate of interest, potential output, and trend
growth. Section three describes the estimation methodology and reports estimation results.
Section four examines the robustness of these results to changes in the estimates of potential
output and trend growth. Section ﬁve investigates the eﬀects of r∗mismeasurement on the
performance of monetary policy. Section six concludes.
2
An Empirical Framework for Measuring the Natural Rate
As noted, we apply the Kalman ﬁlter to estimate the natural rate of interest, the level of
potential output, and its trend growth rate. One alternative would be to use a univariate
time-series method to estimate r∗. However, such an approach is problematic because it
does not control for the sustained periods of rising and declining inﬂation in the United
States during the past several decades. In particular, given that the natural rate of interest
and the deviation of the real interest rate from r∗; however, this approach is likely to yield very weak
identiﬁcation of r∗. An altogether diﬀerent approach is to use forward rates implied by the term structure
and a measure of inﬂation expectations to estimate low frequency movements in the natural rate of interest
(Cf. Brayton, Mauskopf, Reifschneider, Tinsley and Williams (1997), Kozicki and Tinsley (2001)). In recent
work, Bomﬁm (2001) uses forward rates from Treasury inﬂation-indexed bonds to estimate r∗over the three
years that they have been issued. One diﬃculty with this general approach is that one must account for
time-variation in the term premium evident in the data.
3

is related to medium-run inﬂation stability, such univariate methods are likely to underes-
timate r∗during the 1960s and 1970s when inﬂation was rising, and overestimate it during
the disinﬂationary episodes of the early 1980s and the 1990s.5 For this reason, we estimate
the natural rate within a model consisting of inﬂation, output, and real interest rates.
Econometric identiﬁcation of r∗is achieved by specifying a simple reduced-form equation
relating the output gap (the percent deviation of real GDP from potential output) to its
own lags and a moving average of the lagged real funds rate gap (the diﬀerence between
the real funds rate and r∗), and a serially uncorrelated error.6 Speciﬁcally, we assume that
˜yt = Ay(L)˜yt−1 + Ar(L)(rt−1 −r∗
t−1) + ϵ1t,
(2)
where ˜yt = 100 ∗(yt −y∗
t ) denotes the output gap, yt is the logarithm of real GDP, y∗
t
is the logarithm of unobserved potential GDP, rt is the ex ante real federal funds rate,
and r∗
t is the unobserved natural rate of interest. (See the Appendix for details on data
construction.) The serially uncorrelated error and the lags of the output gap control for
transitory shocks and short-run dynamics, while highly persistent shifts in this relationship
between the output gap and the real funds rate are ascribed to changes in r∗. Hence, we
require P ay to be less than unity in order to identify changes in r∗with low frequency
shifts in the output gap–real rate relationship
Inﬂation, πt, is measured by the annualized growth rate of the price index for personal
consumption expenditures excluding food and energy – referred to hereafter as core PCE
inﬂation – and is assumed to be determined by its own lags, the output gap, relative prices,
xt, and a serially uncorrelated error,
πt = Bπ(L)πt−1 + By(L)˜yt−1 + Bx(L)xt + ϵ2t.
(3)
5For example, the trend component of the real funds rate based on the Hodrick-Prescott ﬁlter rises
sharply during the period of the Volcker disinﬂation. This estimate of the natural rate of interest would
inappropriately ascribe a large portion of the disinﬂationary policy action to a shift in the natural rate.
6The basic speciﬁcation of output gap dynamics is very similar to that in Rudebusch and Svensson (1999),
except that they assume a constant value of r∗. An alternative speciﬁcation is to include the real bond rate as
in Fuhrer (1997), instead of the real fed funds rate. This approach introduces two additional complications.
First, in order to compute the ex ante real long rate, one needs to measure multi-year inﬂation expectations,
which are arguably more prone to measurement error than near-term inﬂation expectations associated with
the short-term interest rate. Second, in so far as we are seeking to estimate a natural rate useful for a
monetary policy rule, the term premium, itself a potentially time-varying process, would also need to be
estimated. We leave this to further research.
4

The relative price variables include measures of core import price and crude oil import price
inﬂation, both measured as deviations from core PCE inﬂation. Potential GDP is deﬁned as
the level of GDP that is consistent with unchanged inﬂation in the absence of relative price
shocks, xt, and the serially uncorrelated disturbance, ϵ2t. Equations (2) and (3) constitute
the measurement equations of our state-space model.
As noted, economic theory implies that the trend growth rate is one determinant of r∗.
Hence, we specify
r∗
t = c gt + zt,
(4)
where gt is our estimate of trend growth and zt captures other determinants of r∗, such as
households’ rate of time preference. We assume that z follows an autoregressive process,
zt = Dz(L) zt−1 + ϵ3t,
(5)
where ϵ3t is assumed to be a serially uncorrelated innovation.
In principle, z may be
stationary or nonstationary; in the following we consider two speciﬁc cases: (1) z is described
by a stationary AR(2) process, and (2) z follows a random walk.
As noted, there is evidence for time variation in the trend growth rate, with a slowdown
occuring during the 1970s and a pickup during the late 1990s. We allow for shocks to both
the level of potential output – the I(1) component – and its trend growth rate – the I(2)
component. For reasons of parsimony, we specify a simple random walk model for both
components. Speciﬁcally, potential output is assumed to evolve according to
y∗
t
=
y∗
t−1 + gt−1 + ϵ4t,
(6)
gt
=
gt−1 + ϵ5t,
(7)
where ϵ4t and ϵ5t are serially uncorrelated and mutually contemporaneously uncorrelated
with the innovation to z, ϵ3t. Assuming the standard deviation of the disturbance to the
growth rate component of potential output is positive, potential output is a second-order
integrated process.7 If potential output is I(2) and c ̸= 0, then r∗is integrated of order one,
even if the z process is stationary. Equations (4)–(7) constitute the transition equations of
our state-space model.
7The hypothesis that log real GDP is I(2) is typically rejected by an ADF test. However, as Stock and
Watson (1998) point out, when the disturbance to the growth rate component has small variance, such a
test statistic has a high false-rejection rate.
5

Several authors have used variants of the model (2)-(7) to obtain trend-cycle decomposi-
tions of GDP, but none incorporate interest rates in their models. Watson (1986) considers
a model with constant trend growth g and an AR speciﬁcation for the output gap. Clark
(1987) extends Watson’s model and allows for time variation in trend growth. Kuttner
(1994) explores the relationship between the cyclical component of GDP and inﬂation by
including a dynamic inﬂation equation.8 Roberts (2001) decomposes output growth into
growth in hours and labor productivity growth, and allows for time variation in the trend
growth rates of both of these series. As noted, none of these contributions include the eﬀect
of interest rates and, as a result, they do not address the issue of time variation in the
natural rate of interest.
3
Estimation
We estimate several variants of the model described above on quarterly U.S. data over the
period 1961:1 to 2000:4. Details on the data used are given in the Appendix. We allow the
lag lengths in the output gap and inﬂation equations, equations (2) and (3), respectively,
to be determined by the data. Speciﬁcally, we include two lags each of the output gap
and the real rate gap in the output gap equation.
The ﬁnding that the output gap is
well characterized by an AR(2) is consistent with the studies using unobserved components
models cited above. We impose the restriction that the coeﬃcients on the two lags of the
real rate gap are the same, which is not rejected by the data for any of our speciﬁcations.
We include eight lags of inﬂation in the inﬂation equation and impose the restriction,
not rejected by the data, that the coeﬃcients sum to unity. For reasons of parsimony, we
restrict the coeﬃcients on lags 2 to 4 of inﬂation to be equal, and the same for lags 5 to 8
(Cf. Gordon (1998), Brayton, Roberts and Williams (1999)). Including only the ﬁrst lag
of the output gap in this equation proved suﬃcient. Finally, the relative price vector, xt,
consists of contemporaneous core import price inﬂation, and the ﬁrst lag of oil import price
inﬂation, both measured relative to core PCE inﬂation.
8In a related paper, Laubach (2001) identiﬁes the natural rate of unemployment using a model of inﬂation
dynamics.
6

3.1
Estimation Methodology
In principle, the model can be estimated by maximum likelihood using the Kalman ﬁlter.
However, the contributions from variation in trend growth and the natural rate of interest
to overall variability in the data are relatively small. As a result, the maximum likelihood
estimates of the standard deviations of the innovations to these processes, σ3 and σ5, are
likely to be biased towards zero owing to the so-called “pile-up problem” discussed by Stock
(1994). Indeed, the maximum likelihood estimates of both of these parameters were zero.
We therefore use Stock and Watson’s (1998) median-unbiased estimator to obtain estimates
of the ratio λg ≡σ5
σ4 , and, in cases where z is nonstationary, λz ≡σ3
σ1
ar
√
2.9 We impose these
ratios when estimating the remaining model parameters (including σ1 and σ4) by maximum
likelihood. Because the pile-up problem does not arise for stationary unobserved processes,
in cases where z is stationary, we estimate the standard deviation of its innovation, σ3, by
maximum likelihood simultaneously with the other model parameters.
We proceed in three steps.
In the ﬁrst step, we generate a preliminary estimate of
potential output, which we use as an input in estimating λg. We follow Kuttner (1994)
and apply the Kalman ﬁlter to estimate potential output, omitting the real rate gap term
from equation (2) and assuming that the trend growth rate, g, is constant. We compute
the exponential Wald statistic of Andrews and Ploberger (1994) for a structural break
with unknown break date on this preliminary estimate of potential output. We then use
Stock and Watson’s results to convert the exponential Wald statistic into an estimate ˆλg.
Applying Stock and Watson’s method to the preliminary estimate of potential GDP, instead
of directly to the GDP data, has the advantage that it is consistent with their assumption
that all shocks have a permanent eﬀect on the level of the series under consideration.
Correspondingly, when applying the method to our preliminary estimate of potential GDP
we do not correct the data for serial correlation in the level shocks, as Stock and Watson
suggest.
If the unobserved component of the natural rate of interest, z, is assumed to be station-
9This ratio is based on the assumption that the coeﬃcients on the two lags of the real rate gap are the
same. Substituting (4) into (2), the latter can be written as
˜yt = Ay(L)˜yt−1 + ar
2 (rt−1 + rt−2 −c(gt−1 + gt−2)) −ar
2 (zt−1 + zt−2) + ϵ1t
The ratio λz based on the test statistic for an intercept shift at unknown date in this equation is thus the
ratio of arσ3/
√
2 to σ1.
7

ary, we proceed directly to the third and ﬁnal step; otherwise, in the second step, we impose
the estimated value of λg from the previous step and follow a similar process to generate
an estimate of λz. We again estimate the ﬁve model equations, imposing σ5 = ˆλgσ4. We
now include the real interest rate gap in the output gap equation, but assume that z is
constant; that is, we assume r∗
t = c gt + constant. Using this speciﬁcation, we compute the
exponential Wald statistic for an intercept shift in the output gap equation at an unknown
break date, and use Stock and Watson’s results to obtain an estimate ˆλz.
In the third and ﬁnal step, we impose the estimated values of λg from the ﬁrst step
and λz from the second step (assuming z is nonstationary), and estimate the remaining
model parameters by maximum likelihood.10 As noted, if z is assumed to be stationary,
we include σ3 in the parameters to be estimated by maximum likelihood. We compute
estimated conﬁdence intervals and corresponding standard errors for the estimates of the
states using Hamilton’s (1986) Monte Carlo procedure, which accounts for both ﬁlter and
parameter uncertainty.11
3.2
Estimation Results
The ﬁrst-stage estimation of potential output indicates that the trend growth rate exhibits
only a relatively modest amount of variation over time. The ﬁrst line in Table 1 reports the
value of the exponential Wald statistic testing for an intercept shift in the ﬁrst diﬀerence
of potential GDP. This value of 1.51 is just below the 10 percent critical value of 1.55
given in Andrews and Ploberger (1994, Table 1, page 1399). Using Stock and Watson’s
median-unbiased estimator, this relatively weak evidence of a change in the growth rate
of potential GDP translates into an estimate of λg of about 0.04, shown in the second
column of the table. When multiplied by our third-stage estimate of σ4 reported below, the
implied standard deviation of trend growth changes is estimated to be about 0.1 percentage
10Estimates of the conditional expectation and covariance matrix of the initial state are computed using
the GLS method discussed in Harvey (1989, p. 122). Because these estimates are functions of the model
parameters, for certain parameter values the covariance matrix may be ill conditioned. The conditional
expectation of the initial values of y∗and g is then computed by ﬁtting a segmented trend through log real
GDP, with z initialized at zero, and the covariance matrix is set to 0.2 times the identity matrix. During
the Monte Carlo simulations for computing the standard errors, this procedure is modiﬁed as discussed in
Laubach (2001, p. 222).
11Note that these estimated conﬁdence intervals hold the imposed values of λg and λz ﬁxed but take into
account the uncertainty regarding σ1, σ2, σ4, and, thus, implicitly σ3 and σ5.
8

Table 1: First- and Second-stage Estimation Results
Exponential
Median-unbiased Estimate of λ
Variable
Wald
Point
90 % Conﬁdence Interval
Statistic
Estimate
Low
High
Trend growth (g)
1.51
.039
.000
.103
Natural rate (z)
4.28
.071
.015
.117
point (expressed at an annual rate), a ﬁgure almost identical to Stock and Watson’s (1998)
comparable estimate. The 90 percent conﬁdence intervals for the estimate of λg, computed
by Monte Carlo simulations, are given in the ﬁnal two columns of the table.12 Note that
the lower end of the 90 percent conﬁdence interval for the estimate of λg includes zero, the
case in which the trend growth rate is constant and potential output is integrated of order
one.
The results from the second-stage estimation indicate the presence of persistent time
variation in z, the component of r∗not related to the trend growth rate. As seen in the
second line of Table 1, the value of the exponential Wald statistic testing for an intercept
shift in the output gap equation is 4.28, which is signiﬁcant at the 1 percent level. The
implied median-unbiased estimate of λz is 0.07. In cases where we assume that the process z
is nonstationary – and in particular, described by a random walk – we impose this estimated
value of λz in the third and ﬁnal estimation stage.
Turning to the ﬁnal-stage estimation, we begin by assuming that z follows a stationary
AR(2) process. The results from maximum likelihood estimation of this model are reported
in the ﬁrst column of Table 2. The estimated coeﬃcients dz are consistent with z being
stationary. The estimated sum of coeﬃcients on the lagged output gap in the output gap
equation is below unity (and the unit sum hypothesis is rejected at conventional levels),
consistent with the identiﬁcation assumptions described in Section 2. Finally, the real rate
gap enters the output gap equation with the correct sign and is signiﬁcant at the one percent
level.
The natural rate of interest is estimated to vary one-for-one with changes in the trend
12To compute this conﬁdence interval, we use parameter estimates based on the second-stage model with
a time-varying trend growth and a constant natural rate of interest to construct 10,000 simulated series of
{y∗
t , gt}. For each pair of simulated series we compute the exponential Wald statistic for an intercept shift
in the ﬁrst diﬀerence of y∗
t .
9

Table 2: Parameter Estimates
Stationary
Random Walk Model for z
Parameter
z ∼AR(2)
Baseline
Low λz
High λz
λz
.045
.071
.015
.117
(.24)
P ay
.924
.943
.942
.944
ar
-.117
-.104
-.091
-.114
(3.20)
(3.67)
(3.66)
(3.63)
by
.060
.040
.059
.030
(1.95)
(1.57)
(1.84)
(1.37)
c
.970
1.062
1.001
1.008
(3.89)
P dz
.965
1
1
1
σ1 (˜y)
.263
.364
.406
.327
σ2 (π)
.719
.725
.721
.728
σ3 (z)
.142
.352
.095
.475
σ4 (y∗)
.655
.627
.610
.639
σ5 (g)
.102
.098
.095
.100
σr∗=
p
c2σ2
5 + σ2
3
.173
.367
.134
.485
Log Likelihood
-360.5
-362.9
-362.2
-363.0
Standard Error (ave.)
r∗
2.58
1.98
1.09
2.38
g
.42
.48
.42
.53
y∗
2.33
3.25
1.97
4.32
Notes: t statistics in parentheses. σ5 is expressed at annual rate.
Standard errors are sample averages for smoothed estimates of states.
10

growth rate of output, and this result is robust to changes in the process for z. For the case
of stationary z, c is estimated to be .97, with a standard error of .25. The second column
of Table 2 reports the estimation results for the case where z is modeled as a random walk
and λz is estimated using the median-unbiased estimator. The results are very similar to
those where z is assumed to follow an AR(2). In particular, the estimate of c is also near
unity. However, owing to the existence of two nonstationary processes determining r∗–
g and z – this latter estimate must be treated with caution owing to the potential for
spurious correlation (Cf. Granger and Newbold (1974)). For this reason, in cases where z
is nonstationary, inference based on the standard errors is invalid and we therefore do not
report t-statistics for the estimates of the coeﬃcient c.
The ﬁnal two columns of Table 2 indicate the estimation results when we impose values
for λz corresponding to the lower and upper limits of the 90 percent conﬁdence intervals,
instead of the median-unbiased point estimate. Again, the coeﬃcient c relating r∗to the
trend growth rate is near unity, consistent with the previous results. Except for the standard
deviations of the innovations, the parameter estimates are little aﬀected by the choice of
λz. The more variable the z process and therefore r∗, the lower the variance of the serially
uncorrelated innovations to the output gap equation. Note that, based on the log likelihood
values, the data are not able to discern between the alternative speciﬁcations shown in the
table.
The smoothed (two-sided) estimates of the unobserved processes implied by our model
estimates are shown in Figure 1.
The r∗estimates in the model in which z follows a
stationary AR(2) (indicated by the dashed line) exhibit far larger short-duration swings
than those where z is assumed to follow a random walk (the solid line). For this reason, for
the remainder of the paper, we focus on the random walk speciﬁcation, which appears to
correspond more closely to our middle- and low-frequency characterization of the natural
rate of interest. We refer to the speciﬁcation given in the second column as the “baseline
model;” the restriction to the random walk speciﬁcation for z is not rejected by the data
at the 5 percent level. This estimate of r∗peaks at about 4-1/2 percent in the mid-1960s,
reaches a minimum of 1-1/4 percent in the early 1990s, and ends the sample period at just
above its sample average of 3 percent.
The estimates of the trend growth rate and the output gap are very similar across the
four estimates. As shown in the middle panel of the ﬁgure, the estimated trend growth
11

Figure 1: Smoothed Estimates of Unobserved States
0
2
4
6
1960
1965
1970
1975
1980
1985
1990
1995
2000
0
2
4
6
Natural Rate of Interest (r*)
z:AR(2)
Baseline
Lower z variability
Higher z variability
2
3
4
5
1960
1965
1970
1975
1980
1985
1990
1995
2000
2
3
4
5
Trend Growth Rate (g)
-10
 -5
  0
  5
1960
1965
1970
1975
1980
1985
1990
1995
2000
-10
 -5
  0
  5
Output Gap
rate peaks in the mid-1960s at about 3-3/4 percent, and then declines through the 1970s
and 1980s.
From its low of about 3 percent in the early 1990s, the trend growth rate
increases by about one-half percentage point by the end of the sample. The broad outline
of the output gap estimate, shown in the lower panel, corresponds closely to the estimates
of Clark (1987) and Kuttner (1994) over the parts of the sample that are covered by their
estimates, although Kuttner’s estimate is more volatile than either ours or Clark’s.
The standard errors of the estimates of the unobserved states, shown at the bottom of
Table 2, are relatively large, as is typical for Kalman ﬁlter estimates. As a result, changes
in the natural rate of interest and the trend growth rate of output are not measured with
12

much precision. Across the speciﬁcations reported in the table, the average standard error
of r∗ranges from 1 to 2-1/2 percentage points, that for the trend growth rate is about
1/2 percentage point, and that for the level of potential output from 2 to 4-1/2 percentage
points.
4
Robustness Analysis
We now extend the preceding robustness analysis to include changes in estimates of potential
output and the trend growth rate. Our deﬁnition of the natural rate as the real interest rate
at which real GDP equals potential, once the eﬀects of transitory shocks have dissipated,
implies that our natural rate estimates are sensitive to our estimate of potential GDP. We
ﬁrst consider alternative estimates based on the uncertainty surrounding our estimate of
λg; we then examine the eﬀects of augmenting the model with a labor market indicator to
assist in the decomposition of GDP into trend and cyclical components.
If the trend growth rate is assumed to be constant, then the estimate of the natural rate
of interest is signiﬁcantly less variable than in the baseline estimates. The second column
of Table 3, labeled “Low λg”, reports results from estimating the baseline model under the
assumption that λg = 0, the lower end of its 90 percent conﬁdence interval. For comparison,
the ﬁrst column of the table repeats the baseline results from Table 2. With a constant
trend growth rate, c is not identiﬁed. The resulting estimate of λz is 0.026, well below that
in the baseline speciﬁcation. Evidently, when modeled as a pure random walk, r∗is poorly
identiﬁed. As a result, a signiﬁcantly greater portion of output gap variability is ascribed
to serially uncorrelated shocks and less to permanent shocks. This is illustrated graphically
in the upper panel of Figure 2. Interestingly, the output gap estimates, shown in the lower
panel of the ﬁgure, diﬀer relatively little between the constant growth rate and the baseline
estimates.
Increasing the variability of the trend growth rate, however, has relatively modest eﬀects
on the estimated parameters and the estimates of r∗. The third column of the table reports
the results when λg takes the value 0.103, corresponding to the upper end of the 90 percent
conﬁdence interval. In this case, the estimate of λz is .060, slightly lower than the baseline
estimate. Except for the greater variability of the trend growth rate itself, the parameter
estimates do not diﬀer substantially from the baseline estimates. In particular, the estimate
13

Table 3: Parameter Estimates under Diﬀerent Potential Output Assumptions
Parameter
Baseline
Low λg
High λg
Hours
λg
.039
.000
.103
.046
λz
.071
.026
.060
.039
P ay
.943
.944
.946
.927
ar
-.104
-.087
-.124
-.076
(3.67)
(3.66)
(3.60)
(3.09)
by
.040
.055
.031
.096
(1.57)
(1.88)
(1.28)
(3.02)
c
1.062
–
.995
.886
σ1
.364
.397
.257
.497
σ2
.725
.722
.729
.714
σ3
.352
.168
.175
.359
σ4
.627
.622
.662
.547
σ5
.098
.000
.273
.101
σ6
–
–
–
.245
σr∗=
p
c2σ2
5 + σ2
3
.367
.168
.323
.370
Log Likelihood
-362.9
-362.3
-363.5
-466.51
Standard Error (ave.)
r∗
1.98
1.28
1.63
2.65
g
.48
.24
.74
.46
y∗
3.25
2.18
3.48
.59
Notes: t statistics in parentheses. σ4 is expressed at annual rate.
Standard errors are sample averages for smoothed estimates of states.
1. Log likelihhod for model augmented with equation for employee hours
is not comparable to others.
14

Figure 2: Sensitivity of Estimates to Assumptions Regarding Potential Output
0
2
4
6
1960
1965
1970
1975
1980
1985
1990
1995
2000
0
2
4
6
Natural Rate of Interest (r*)
Baseline
Lower g variability
Higher g variability
Hours Model
2
3
4
5
1960
1965
1970
1975
1980
1985
1990
1995
2000
2
3
4
5
Trend Growth Rate (g)
-10
 -5
  0
  5
1960
1965
1970
1975
1980
1985
1990
1995
2000
-10
 -5
  0
  5
Output Gap
of c is again nearly unity. As seen in the ﬁgure, although the estimated trend growth rate is
much more variable (shown by the dotted line in the middle panel), the resulting estimates
of r∗diﬀer relatively little from the baseline estimates.
4.1
Incorporating Information on Employment Hours
Our second alternative speciﬁcation for potential GDP is based on the notion that employ-
ment hours, as well as inﬂation, contain information about the cyclical state of the economy.
Speciﬁcally, we follow Roberts (2001) and introduce the equation
˜ht = f1˜yt + f2˜yt−1 + f3˜ht−1 + ϵ6t
(8)
15

into the model, where ˜ht denotes percent deviations of private nonfarm employee hours ht
from a trend h∗
t . We compute ˜ht as the deviation of hours from a simple log-linear time
trend (Cf. Rotemberg and Woodford (1996)).13
Estimation results for this speciﬁcation are shown in the ﬁnal column of Table 3, labeled
“Hours.” The resulting estimate of λg is a little larger than the baseline value, but the
estimate of λz is considerably lower than the baseline value. However, because the variance
of the serially uncorrelated innovation to the output gap equation rises while that of the
level shock to potential GDP falls, the variability of both the trend growth rate and the
natural rate of interest are nearly the same as in the baseline speciﬁcation. The estimate
of c is about 0.9, just a bit below the other estimates.
The uncertainty around the output gap estimate shown at the bottom of Table 3 is less
than one ﬁfth of that in the baseline speciﬁcation. The high degree of precision regarding the
estimate of the level of potential output results from the close ﬁt of equation (8), combined
with the absence of any unobserved states in the estimation of trend hours. A problematic
aspect of the estimation results for the model augmented with hours is that it appears to
be in conﬂict with evidence of low frequency changes in the growth rate of labor supply (Cf.
Roberts (2001)). For this reason, the precision of the estimates may be spurious.
The close identiﬁcation of the output gap with deviations of hours from a time trend
implies a diﬀerent view of history compared to the baseline model where the output gap is
identiﬁed by the inﬂation equation alone. As shown in Figure 2, in the model augmented
with the hours equation (the dashed line), both the output gap and r∗are estimated to
have been below their baseline counterparts in the ﬁrst half of the sample, and above
them in the second half. In particular, during the late 1990s, a period when core PCE
inﬂation was declining, the baseline estimate indicates that output was below potential
and therefore exerting downward pressure on inﬂation, while the model augmented with
the hours equation indicates output was above potential and therefore boosting inﬂation.
Evidently, the estimates of potential output in the baseline speciﬁcation include the eﬀects
of omitted variables that inﬂuence inﬂation but are not captured by movements in hours.
13In principle, h∗
t could be speciﬁed as an I(2) process analogous to y∗
t . However, tests for an intercept
shift in the raw hours data over our sample show no evidence for such a shift. Moreover, when attempting
to construct a preliminary estimate of trend hours by estimating a trend-cycle decomposition based on a
constant drift in trend hours, trend hours are estimated to be a simple time trend. These results diﬀer from
those of Roberts (2001) who normalizes hours by population and ﬁnds this series to be I(2).
16

4.2
Overall Robustness of Estimates
Table 4: Properties of Unobserved Variables
z ∼AR(2)
Baseline
Low λz
High λz
Low λg
High λg
Hours
Natural Rate of Interest
Minimum
.10
1.28
2.62
.42
2.55
1.38
1.91
(92:4)
(92:4)
(92:1)
(92:4)
(93:1)
(92:3)
(74:3)
Maximum
5.70
4.52
3.75
4.90
3.93
4.34
4.31
(65:4)
(65:2)
(65:2)
(65:2)
(65:2)
(65:2)
(83:4)
Ending Value
3.40
3.10
3.16
3.16
2.84
3.39
4.04
Trend Growth Rate
Minimum
2.91
2.96
2.91
2.99
3.32
1.99
2.98
(90:4)
(91:3)
(91:2)
(91:3)
–
(92:2)
(80:1)
Maximum
3.73
3.70
3.73
3.68
3.32
4.32
3.86
(65:1)
(65:2)
(65:2)
(65:2)
–
(65:2)
(65:2)
Ending Value
3.31
3.39
3.38
3.36
3.32
3.79
3.46
Output Gap
Minimum
-8.04
-8.14
-7.82
-8.36
-7.48
-8.80
-5.77
(82:3)
(82:3)
(82:3)
(82:3)
(82:3)
(82:3)
(75:1)
Maximum
4.11
4.45
3.99
4.61
4.30
4.60
3.03
(66:2)
(66:1)
(65:4)
(66:1)
(73:1)
(78:3)
(66:1)
Ending Value
.27
-1.03
-.30
-1.42
-1.69
-.92
.61
Despite the sizeable uncertainty around most of our estimates of the natural rate of
interest, the trend growth rate, and potential output, our point estimates of these processes
are qualitatively similar across the seven model variants described above. This is illustrated
in Table 4, which shows the minimum, maximum, and ending values of the smoothed
estimates of the natural rate of interest, the trend growth rate, and the output gap. In
the six cases that exclude the hours equation, r∗peaked in 1965 and hit its sample low in
1992 or 1993. In the model augmented with the hours equation, r∗hits its low in 1973 and
peaks in 1983. All estimates show the trend growth rate peaking in 1965 and the low point
occurring in the early 1990s (the augmented model has two nearly identical minima, in 1980
and in the early 1990s). The estimates of the output gap are generally similar, with the
peaks occurring in the late 1960s and the mid- and late-1970s; the minimum occurs in the
17

Figure 3: Estimates of the Stance of Monetary Policy
-2
 0
 2
 4
 6
 8
10
12
1960
1965
1970
1975
1980
1985
1990
1995
2000
-2
 0
 2
 4
 6
 8
10
12
-2
 0
 2
 4
 6
 8
10
12
1960
1965
1970
1975
1980
1985
1990
1995
2000
-2
 0
 2
 4
 6
 8
10
12
r*
Baseline r* Estimates
Actual Real Funds Rate
early 1980s (with the augmented model showing an equally large negative gap in 1975).
5
Monetary Policy and a Time-varying Natural Interest Rate
Allowing for time variation in the natural rate of interest can signiﬁcantly change one’s
view of the stance of monetary policy during historical episodes in which r∗strayed from its
historical average. Figure 3 shows the baseline r∗estimates (the solid lines), along with the
corresponding actual values of the real fed funds rate (the dashed lines). The shaded region
in the ﬁgure shows the 70 percent conﬁdence intervals for the r∗estimates. The estimated
decline in the natural rate during the early 1990s suggests that the stance of policy during
the early 1990s may not have been as expansionary as one would believe based on a constant
value of r∗. Similarly, monetary policy appears much easier in the late 1960s, relative to
the assumption of a constant natural rate of interest, when one accounts for the boost to
r∗resulting from relatively strong trend growth during that period.
R∗mismeasurement interferes with the achievement of both inﬂation and output stabi-
lization goals. The achievement of a long-run inﬂation rate goal requires that estimates of
r∗converge to the true value in expectation. Let policy be described by the interest rate
feedback rule,
it = πe
t + ˆr∗
t + απ(πt −π∗) + αy˜yt,
(9)
where ˆr∗
t is the policymaker’s estimate of the natural rate of interest, πe is expected inﬂation,
18

Figure 4: Real-time Estimates of the Natural Rate of Interest
1
2
3
4
5
1960
1965
1970
1975
1980
1985
1990
1995
2000
1
2
3
4
5
Smoothed (two-sided) r* Estimate
Filtered (one-sided) r* Estimate
and π∗is the (ﬁxed) long-run inﬂation target. Absent shocks, if the policymaker’s estimate
converges to ˆr∗, then the inﬂation rate converges to π∗+
1
απ (r∗−ˆr∗).
Hence, if r∗is
subject to permanent shifts, then for the inﬂation rate to stabilize at the target level, the
policymaker’s estimate must converge in expectation to the true value.
Mismeasurement of r∗also implies a deterioration in short-run macroeconomic stabi-
lization. In the absence of mismeasurement, a time-varying natural rate of interest has no
implications for the performance resulting from a policy rule of the form of equation (9)
beyond greater variability of real interest rates. But, r∗mismeasurement introduces an
additional disturbance to the system, the magnitude of which depends on the variance of
the r∗innovations and the persistence of which depends on the Kalman ﬁlter gain used in
updating estimates of r∗.
Comparing one-sided and two-sided estimates of r∗provides a measure of the likely
magnitude and persistence of r∗mismeasurement. Figure 4 shows the baseline one-sided
ﬁlter estimates (the dashed line) and the two-sided smoothed estimates (the solid line) of the
natural rate of interest. For comparison, the sample mean of the smoothed estimate – about
3 percent – is shown by the horizontal dashed line. The one-sided ﬁlter estimates correspond
to a “real-time” estimate of r∗in that past data are used in estimating the state.14 Taking
the smoothed estimate as truth, the standard deviation of the measurement error using
the one-sided ﬁlter is about 0.9 percentage point over the sample; nearly 10 percent of
14The full sample is used to estimate the model parameters, however, so the analogy is not exact.
19

Table 5: Eﬀects of r∗Mismeasurement under the Taylor Rule
Standard Deviation
Loss
% Increase
Policymaker’s Estimate of r∗
˜y
π
∆i
L
in Loss
True value (ˆr∗
t = r∗
t )
1.1
1.4
.7
3.5
–
One-sided KF estimate
1.5
1.4
1.0
4.7
34
Constant (ˆr∗= 3.0)
1.6
1.6
.7
5.4
53
the existing measurement error is eliminated each quarter. For comparison, the sample
standard deviation of the smoothed r∗estimate is 0.8 percentage point, and the ﬁrst-order
autocorrelation is 1.00.
We use simulations of the estimated baseline model to assess the eﬀects of r∗mismea-
surement owing to time variation in the natural rate of interest. For these simulations, we
assume the true values of potential output and r∗are given by the respective two-sided
Kalman ﬁlter estimates of our baseline model. We assume that policy is set according to
the Taylor Rule (that is, απ = αy = .5), and that the true value for potential output is
observed. We conduct three simulations. In one, the policymaker knows the true value of
r∗each period. In the second, the policymaker uses the one-sided Kalman ﬁlter estimate,
which corresponds to a “real-time” estimate of r∗. In the third, the policymaker assumes
r∗is a constant 3 percent, equal to the mean value of the two-sided estimate. Note that
we are restricting the scope of mismeasurement to that resulting from the time variation
in the natural rate; we assume that the policymaker correctly knows the sample mean of
r∗. Each simulation extends over 1961–2000; to mitigate the eﬀects of initial and terminal
conditions, the results are computed for 1964–1997 only.
We assume the policymaker’s objective is to minimize the weighted sum of the variances
of the output gap, the inﬂation rate, and the change in the nominal federal funds rate.
Speciﬁcally, we follow Rudebusch and Svensson (1999) and Rudebusch (2001) and specify
the loss function:
L = V ar(π) + V ar(˜y) + 1
2V ar(∆i),
(10)
where V ar(x) signiﬁes the unconditional variance of variable x.
Model simulations indicate that mismeasurement of the natural rate of interest leads
to a signiﬁcant deterioration in output stabilization, but has relatively modest eﬀects on
inﬂation stabilization. The ﬁrst three columns of Table 5 report the simulated standard de-
20

viations of the output gap, the inﬂation rate, and the change in the nominal funds rate. The
fourth column reports the value of the loss given by equation (10); the ﬁnal column shows
the percent increase in the loss relative to the case of no r∗mismeasurement. Assuming
r∗is constant increases the loss by over 50 percent relative to the case of no mismea-
surement. Using the one-sided Kalman ﬁlter estimate signiﬁcantly improves stabilization
performance.15
6
Conclusion
In this paper, we have jointly estimated the natural rate of interest, potential output, and
the trend growth rate using the Kalman ﬁlter. We ﬁnd that the natural rate of interest
shows signiﬁcant variation over the past forty years in the United States. These results
are robust to changes in speciﬁcation. Variation in the trend growth rate is an important
determinant of changes in the natural rate, as predicted by theory. We show that time
variation of the natural rate has important implications for the design and implementation
of monetary policy. Adjustment to changes in the natural rate is crucial for the achievement
of long-run inﬂation and short-run stabilization goals. The periods of the late 1960s and
the early 1990s provide particularly acute examples where recognition of the time-varying
nature of the natural rate has a profound inﬂuence on the ability to stabilize inﬂation and
output.
This paper has focused on the postwar U.S. economy. The analytical apparatus can
easily be adapted to other countries and an interesting issue is whether factors can be
identiﬁed that aﬀect the long-run natural rate across countries. In addition, this approach
can be extended to estimate the underlying natural rates of other ﬁnancial variables, such
as the equity premium or the real exchange rate.
15Rudebusch (2001) claims relatively modest eﬀects of r∗mismeasurement based on model simulations
of transitory shocks to r∗around a known mean.
That study implicitly assumes policymakers update
their r∗estimates, reducing the magnitude and persistence of mismeasurement relative to a constant r∗
assumption. In addition, the coeﬃcients of the policy feedback rule are reoptimized when r∗mismeasurement
is introduced, reducing the implied eﬀects on macroeconomic stabilization.
21

Appendix
This appendix describes the data used in this study. The variable y refers to the log of
real chain-weighted GDP in billions of chained 1996 dollars. The federal funds rate is the
annualized nominal funds rate, with the quarterly ﬁgure computed as the average of the
monthly values. Because the federal funds rate frequently fell below the discount rate prior
to 1965, we use the Federal Reserve Bank of New York’s discount rate prior to 1965.
Our measure of inﬂation is the annualized quarterly growth rate of the price index for
personal consumption expenditures excluding food and energy, referred to as core PCE
inﬂation. To construct a series for the ex ante real federal funds rate, we compute the
expectation of average inﬂation over the four quarters ahead from a univariate AR(3) of
inﬂation estimated over the 40 quarters prior to the date at which expectations are being
formed. To compute these expectations for the early part of our sample, we need to use
inﬂation data prior to 1959:2, the start of the core PCE inﬂation series. For these dates we
splice overall PCE inﬂation to core PCE inﬂation. Our results do not change perceptibly if
inﬂation expectations are proxied by a four-quarter moving average of inﬂation instead of
the forecast from the univariate AR.
The relative price variables included in the inﬂation equation are core import price
and crude oil import price inﬂation. The core import price series is the implicit deﬂator
for imports of nonpetroleum goods. From 1968 on, this series also excludes the prices of
computers and semiconductors. Finally, the hours data are total hours of employees and
self-employed persons in the private nonfarm business sector.
22