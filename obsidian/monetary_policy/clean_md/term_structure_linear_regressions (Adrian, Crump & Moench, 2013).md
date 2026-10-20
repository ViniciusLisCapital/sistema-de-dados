This paper presents preliminary findings and is being distributed to economists 
and other interested readers solely to stimulate discussion and elicit comments. 
The views expressed in this paper are those of the authors and are not necessarily 
reflective of views at the Federal Reserve Bank of New York or the Federal 
Reserve System. Any errors or omissions are the responsibility of the authors. 
Federal Reserve Bank of New York 
Staff Reports 
 
 
Pricing the Term Structure  
with Linear Regressions 
 
Tobias Adrian 
Richard K. Crump 
Emanuel Moench 
 
 
 
 
 
 
Staff Report No. 340 
August 2008 
Revised April 2013

Pricing the Term Structure with Linear Regressions 
Tobias Adrian, Richard K. Crump, and Emanuel Moench 
Federal Reserve Bank of New York Staff Reports, no. 340 
August 2008; revised April 2013 
JEL classification: G10, G12 
 
 
 
 
 
 
 
 
 
 
 
 
Abstract 
 
We show how to price the time series and cross-section of the term structure of interest rates 
using a three-step linear regression approach. Our method allows computationally fast estimation 
of term structure models with a large number of pricing factors. We present specification tests 
favoring a model using five principal components of yields as factors. We demonstrate that this 
model outperforms the Cochrane and Piazzesi (2008) four-factor specification in out-of-sample 
exercises but generates similar in-sample term premium dynamics. Our regression approach can 
also incorporate unspanned factors and allows estimation of term structure models without 
observing a zero-coupon yield curve. 
 
Key words: term structure of interest rates, Fama-MacBeth regressions, dynamic asset pricing 
estimation, empirical finance 
 
 
 
 
 
 
 
 
 
 
 
 
_________________ 
Adrian, Crump, Moench: Federal Reserve Bank of New York (e-mail: tobias.adrian@ny.frb.org, 
richard.crump@ny.frb.org, emanuel.moench@ny.frb.org). The authors thank Greg Duffee, 
Darrell Duffie, Arturo Estrella, Eric Ghysels, Paul Glasserman, Scott Joslin, Don Kim, Monika 
Piazzesi, Joshua Rosenberg, Ken Singleton, Jonathan Wright, Hao Wu, and seminar participants 
at the Federal Reserve Bank of New York, the Stanford Institute for Theoretical Economics 
Workshop at Stanford University, and New York University for helpful comments and 
discussions. Michael Abrahams provided outstanding research assistance. The views expressed in 
this paper are those of the authors and do not necessarily reflect the position of the Federal 
Reserve Bank of New York or the Federal Reserve System.

1.
Introduction
Aﬃne models of the term structure of interest rates are a popular tool for the analysis of
bond pricing. The models typically start with three assumptions: (1) the pricing kernel is
exponentially aﬃne in the shocks that drive the economy, (2) prices of risk are aﬃne in the
state variables, and (3) innovations to state variables and log yield observation errors are
conditionally Gaussian (For examples, see Chen and Scott, 1993; Dai and Singleton, 2000;
Collin-Dufresne and Goldstein, 2002; Duﬀee, 2002; and Kim and Wright, 2005). These
assumptions give rise to yields that are aﬃne in the state variables and whose coeﬃcients
on the state variables are subject to constraints across maturities (For overviews, see
Duﬃe and Kan, 1996; Piazzesi, 2003; and Singleton, 2006). Empirically, the aﬃne term
structure literature has primarily used maximum likelihood (ML) methods to estimate
coeﬃcients and pricing factors, thus exploiting the distributional assumptions as well as
the no-arbitrage constraints.
In this paper, we propose an alternative, regression-based approach to the pricing
of interest rates.
We start with observable pricing factors and develop a three-step
ordinary least squares (OLS) estimator. In the ﬁrst step, we decompose pricing factors
into predictable components and factor innovations by regressing factors on their lagged
levels.
In the second step, we estimate exposures of Treasury returns with respect
to lagged levels of pricing factors and contemporaneous pricing factor innovations. In
the third step, we obtain the market price of risk parameters from a cross-sectional
regression of the exposures of returns to the lagged pricing factors onto exposures to
contemporaneous pricing factor innovations. We provide analytical standard errors that
adjust for the generated regressor uncertainty. We also discuss the advantages of our
method with respect to the recently suggested approaches by Joslin, Singleton and Zhu
(2011) and Hamilton and Wu (2012). In particular, we point out that the assumption of
serially uncorrelated yield pricing errors underlying these likelihood-based methods imply
1

excess return predictability not captured by the pricing factors. In contrast, because our
approach is based on return regressions, we do not need to make assumptions about serial
correlation in yield pricing errors.
We report a speciﬁcation with ﬁve principal components of zero coupon yields as
pricing factors. We show that models with fewer factors are rejected in speciﬁcation tests.
The pricing errors in the ﬁve-factor speciﬁcation are remarkably small and return pricing
errors do not exhibit autocorrelation. We further ﬁnd that level risk is priced and that
the time variation of level risk is best captured by the second (the slope factor) and ﬁfth
principal components. The ﬁve-factor speciﬁcation exhibits substantial variation in risk
premiums and at the same time gives reasonable maximal Sharpe ratios.
We next present a four-factor speciﬁcation following Cochrane and Piazzesi (2008,
CP) which includes the ﬁrst three principal components of Treasury yields and a linear
combination of forward rates designed to predict Treasury returns (the CP factor) as
pricing factors. Unlike Cochrane and Piazzesi (2008), we allow for unconstrained prices
of risk and ﬁnd that the CP factor signiﬁcantly prices all factors except slope.
The
magnitude and time pattern of the price of risk speciﬁcation of the four-factor CP model
is akin to that of the ﬁve-factor model, indicating that the two models capture term
premium dynamics in a similar way. However, in-sample yield pricing errors are somewhat
larger in the four-factor model.
To compare the four- and ﬁve-factor models, we perform two out-of-sample exercises.
In the ﬁrst, we use the model-implied term premiums to infer the future path of average
short-term interest rates. In the second, we estimate the models using returns on bonds
maturing in less than or equal to ten years and then impute the model-implied yields of
bonds with longer maturities. In both of these exercises, the ﬁve-factor model outperforms
the four-factor speciﬁcation. Hence, we choose the ﬁve-factor model to be our preferred
speciﬁcation.
Our procedure can potentially be applied to any set of ﬁxed income securities. In this
2

paper, we use our approach to estimate an aﬃne term structure model from returns on
maturity-sorted portfolios of coupon-bearing Treasury securities. The availability of a zero
coupon term structure is, therefore, not necessary to estimate the model. Yet, estimation
from the returns on maturity sorted bond portfolios with pricing factors extracted from
coupon bearing yields generates a zero coupon curve that is very similar to the Fama and
Bliss discount bond yields.
We present a number of extensions. First, we show how to estimate the model in the
presence of unspanned factors. Such factors do not improve the cross-sectional ﬁt of yields
but do aﬀect the time variation of prices of risk through their predictive power for the
yield curve factors. In contrast to the four- and ﬁve-factor speciﬁcations, incorporating
an unspanned real activity factor produces a signiﬁcant price of slope risk. Second, we
show how to impose linear restrictions on risk exposures and market prices of risk in the
estimation of the model. Third, we show that the maximal Sharpe ratios implied by the
four- and ﬁve-factor speciﬁcations are very reasonable, with an average level below one
and peaks below 2.5. Fourth, we explain how the model can be used to ﬁt the yield curve
at the daily frequency. Finally, we show that the implied principal component loadings
from the term structure model are statistically indistinguishable from the actual principal
component loadings.
Our paper is organized as follows.
In Section 2, we present the model and our
three-step estimator, and we show how to obtain model-implied yields from the estimated
parameters. We further discuss the relation between our approach and other estimation
methods in the literature. In Section 3, we present our main empirical ﬁndings. Section
4 discusses extensions and robustness checks. Section 5 concludes.
3

2.
The model
In this section, we derive the data generating process for arbitrage-free excess holding
period returns from a dynamic asset pricing model with an exponentially aﬃne pricing
kernel. We then show how to estimate the model parameters via three-step linear regressions,
present their asymptotic distributions, and derive the no-arbitrage cross equation constraints
for bond yields.
2.1
State variables and expected returns
We assume that the dynamics of a K × 1 vector of state variables Xt evolve according to
the following vector autoregression (VAR):
Xt+1 = µ + ΦXt + vt+1.
(1)
This speciﬁcation of the dynamic evolution of the state variables can be interpreted as
a discrete time analog to the intertemporal capital asset pricing model (ICAPM) state
variable dynamics of Merton (1973) or the general equilibrium setup of Cox, Ingersoll and
Ross 1985. We assume that the shocks vt+1 conditionally follow a Gaussian distribution
with variance-covariance matrix Σ:
vt+1| {Xs}t
s=0 ∼N (0, Σ) ,
(2)
where {Xs}t
s=0 denotes the history of Xt. We denote P (n)
t
the zero coupon Treasury bond
price with maturity n at time t. The assumption of no-arbitrage implies (see Dybvig and
Ross, 1987) that there exists a pricing kernel Mt such that
P (n)
t
= Et
h
Mt+1P (n−1)
t+1
i
.
(3)
4

We assume that the pricing kernel Mt+1 is exponentially aﬃne:
Mt+1 = exp

−rt −1
2λ′
tλt −λ′
tΣ−1/2vt+1

,
(4)
where rt = ln P (1)
t
is the continuously compounded risk-free rate. We further assume that
market prices of risk are of the essentially aﬃne form as suggested in Duﬀee (2002):
λt = Σ−1/2 (λ0 + λ1Xt) .
(5)
We denote rx(n−1)
t+1
the log excess holding return of a bond maturing in n periods:
rx(n−1)
t+1
= ln P (n−1)
t+1
−ln P (n)
t
−rt.
(6)
Using Eq. (4) and Eq. (6) in Eq. (3) yields
1 = Et

exp

rx(n−1)
t+1
−1
2λ′
tλt −λ′
tΣ−1/2vt+1

.
(7)
Assuming that
n
rx(n−1)
t+1 , vt+1
o
are jointly normally distributed, we then ﬁnd
Et
h
rx(n−1)
t+1
i
= Covt
h
rx(n−1)
t+1 , v′
t+1Σ−1/2λt
i
−1
2V art
h
rx(n−1)
t+1
i
.
(8)
We denote
β(n−1)′
t
= Covt
h
rx(n−1)
t+1 , v′
t+1
i
Σ−1,
(9)
and using Eq. (5) we obtain
Et
h
rx(n−1)
t+1
i
= β(n−1)′
t
(λ0 + λ1Xt) −1
2V art
h
rx(n−1)
t+1
i
.
(10)
5

We can decompose the unexpected excess return into a component that is correlated with
vt+1 and another component that is conditionally orthogonal. Then we ﬁnd
rx(n−1)
t+1
−Et
h
rx(n−1)
t+1
i
= γ(n−1)′
t
vt+1 + e(n−1)
t+1 .
(11)
It is straightforward to show that γ(n−1)
t
= β(n−1)
t
using Eq. (9). We assume that the
return pricing errors e(n−1)
t+1
are conditionally independently and identically distributed
(i.i.d.) with variance σ2.
In our baseline speciﬁcations, we use linear combinations of log yields (such as principal
components) as observable factors Xt and estimate the model parameters using holding
period returns based on the same set of yields. Per construction, this implies that βt = β
∀t. We thus proceed with the assumption that β is constant.
The return generating process for log excess holding period returns is then
rx(n−1)
t+1
= β(n−1)′ (λ0 + λ1Xt)
|
{z
}
Expected
return
−1
2
 β(n−1)′Σβ(n−1) + σ2
|
{z
}
Convexity
adjustment
+
β(n−1)′vt+1
|
{z
}
Priced return
innovation
+
e(n−1)
t+1
| {z }
Return pricing
error
(12)
Stacking this system across maturities and time periods, we rewrite it as
rx = β′(λ0ι′
T + λ1X−) −1
2(B⋆vec (Σ) + σ2ιN)ι′
T+β′V + E
(13)
where rx is a N ×T matrix of excess returns, β = [β(1) β(2) · · · β(N)] is a K× N matrix of
factor loadings, ιT and ιN are a T ×1 and N ×1 vectors of ones, X−= [X0 X1 · · · XT−1]
is a K × T matrix of lagged pricing factors, B⋆=

vec
 β(1)β(1)′
· · · vec
 β(N)β(N)′′ is
an N × K2 matrix, V is a K × T matrix, and E is an N × T matrix.
6

2.2
Estimation
Based on Eq. (13), we propose the following simple three-step regression-based estimator
for the parameters of the model.1
1. We begin by estimating Eq. (1) via ordinary least squares. This allows the decomposition
of Xt+1 into a predictable component and an estimate of the innovation ˆvt+1. We
stack these innovations into the matrix ˆV and construct an estimator of the state
variable variance-covariance matrix ˆΣ = ˆV ˆV ′.
T.
2. Next we regress excess returns on a constant, lagged pricing factors and contemporaneous
pricing factor innovations according to
rx = aι′
T + β′ ˆV + cX−+ E.
(14)
Collecting the regressors into the (2K + 1) × T matrix ˜Z = [ιT ˆV ′ X′
−]′ , our
estimators become
h
ˆa ˆβ
′ ˆc
i
= rx ˜Z′ 
˜Z ˜Z′−1
.
(15)
We collect the residuals from this regression into the N × T matrix ˆE. We then
estimate ˆσ2 = trace

ˆE ˆE′.
NT. We construct ˆB⋆from ˆβ.
3. We estimate the price of risk parameters λ0 and λ1 via cross-sectional regression.
We know from Eq. (13) that a = β′λ0 −1
2 (B⋆vec (Σ) + σ2ιN) and c = β′λ1. We
use these expressions to obtain the following estimators for λ0 and λ1:
bλ0 =

ˆβ ˆβ
′−1 ˆβ

ˆa + 1
2

ˆB⋆vec

ˆΣ

+ ˆσ2ιN

(16)
1For a regression-based approach using a linear pricing kernel speciﬁcation, see Adrian, Crump and
Moench (2012).
7

and
bλ1 =

ˆβ ˆβ
′−1 ˆβˆc.
(17)
2.3
Inference
Denoting the matrix Λ = [λ0 λ1], we can write the price of risk estimator in the single
expression
ˆΛ =

ˆβ ˆβ
′−1 ˆβ

rx + 1
2
ˆB⋆vec(ˆΣ)ι′
T + 1
2 ˆσ2ιNι′
T

M ˆV Z−
 Z−M ˆV Z′
−
−1 ,
(18)
where Z−= [ιT X′
−]′ and M ˆV = IT −ˆV ′ 
ˆV ˆV ′−1 ˆV . The equivalence of Eq. (18) with
Eq. (16) and Eq. (17) follows from observing that ι′
TM ˆV Z−
 Z−M ˆV Z′
−
−1 = ϱ′
1, where ϱ1
is a (K + 1) × 1 vector with ﬁrst element equal to one and zeros elsewhere and because
[ˆa ˆc] = rxM ˆV Z−
 Z−M ˆV Z′
−
−1.
We show in the Appendix that β and Λ have the joint limiting distribution:
√
T


vec

ˆβ −β

vec

ˆΛ −Λ



d
−→N



0
0

,


Vβ
C′
Λ,β
CΛ,β
VΛ




,
(19)
with
Vβ = σ2  I ⊗Σ−1
.
(20)
We provide the analytical expressions for VΛ and CΛ,β in the Appendix. The asymptotic
variance of the factor risk exposures β depends only on the variance of the return pricing
errors in the regression of excess returns on lagged factors and factor innovations as well
as on the variance of the VAR innovations of the pricing factors, but not on β or Λ.
This implies that we could conduct inference about whether a given pricing factor is a
signiﬁcant explanatory variable for bond returns without estimating the full set of model
parameters.
8

2.4
Aﬃne yields
From the estimated model parameters, we can generate a zero coupon yield curve. Under
the assumptions we have made so far, we can show that bond prices are exponentially
aﬃne in the vector of state variables:
ln P (n)
t
= An + B′
nXt + u(n)
t .
(21)
By substituting Eq. (21) into Eq. (6), we see that
rx(n−1)
t+1
= An−1 + B′
n−1Xt+1 + u(n−1)
t+1
−An −B′
nXt −u(n)
t
+ A1 + B′
1Xt + u(1)
t .
(22)
Equating this expression for excess returns with the return generating expression in Eq.
(12), we ﬁnd
An−1+B′
n−1 (µ+ΦXt+vt+1)+u(n−1)
t+1
−An−B′
nXt−u(n)
t
+A1+B′
1Xt+u(1)
t
(23)
=β(n−1)′ (λ0+λ1Xt+vt+1)−1
2
 β(n−1)′Σβ(n−1)+σ2
+e(n−1)
t+1 .
(24)
This equation has to hold state by state.
Let A1 = −δ0 and B1 = −δ1.
Matching
terms, we obtain the following system of recursive linear restrictions for the bond pricing
parameters:
An
=
An−1 + B′
n−1 (µ −λ0) + 1
2
 B′
n−1ΣBn−1 + σ2
−δ0,
(25)
B′
n
=
B′
n−1 (Φ −λ1) −δ′
1,
(26)
A0
=
0, B′
0 = 0,
(27)
9

and
β(n)′
=
B′
n.
(28)
We also obtain the following expression for the log bond pricing errors:
u(n−1)
t+1
−u(n)
t
+ u(1)
t
|
{z
}
Log yield
pricing error
=
e(n−1)
t+1
| {z }
return pricing
error
(29)
Several remarks are in order. First, the derivation of log bond prices is exact, provided
that β(n)′ = B′
n. Second, the recursions in Eq. (25) and Eq. (26) are the standard linear
diﬀerence equations for aﬃne term structure models with homoskedastic shocks. The only
diﬀerence with respect to the standard formulation is the appearance of the term 1
2σ2 in
Eq. (25). This arises due to the fact that we allow for a maturity-speciﬁc return ﬁtting
error that is conditionally orthogonal to the state variable innovations. Our approach
thus incorporates pricing errors explicitly into the no-arbitrage recursions.
Eq. (29) implies that if yield pricing errors are i.i.d., then return pricing errors are
cross-sectionally and serially correlated. Likelihood-based estimation approaches for aﬃne
term structure models typically assume serially uncorrelated yield pricing errors and, thus,
implicitly assume return pricing errors to be serially correlated.
Setting the price of risk parameters λ0 and λ1 to zero in the recursions in Eq. (25)
and Eq. (26) generates the risk-adjusted bond pricing parameters ARF
n
and BRF
n . These
parameters have the property that −1
n
 ARF
n
+ BRF′
n
Xt

equals the time t expectation
of average future short rates over the next n periods. These risk-neutral yields are of
independent economic interest, as the term premium can be calculated as the diﬀerence
between the risk neutral yield and model-implied ﬁtted yield.
10

2.5
Discussion of related literature
While Gaussian aﬃne term structure models have historically been estimated using computationally
intensive maximum likelihood techniques, Joslin, Singleton and Zhu (2011, JSZ) and
Hamilton and Wu (2012, HW) have recently proposed alternative, faster, estimation
approaches. We now brieﬂy compare these approaches with the method introduced here.
A crucial diﬀerence between our method and the approaches in JSZ and HW is that
we do not impose the bond pricing recursions given in Subsection 2.4 in our estimation
procedure.
This allows us to derive simple regression-based estimators for all model
parameters whereas both JSZ and HW require numerical optimization for a subset of the
parameters in their models. We show in Subsection 3.3 that the risk exposures estimated
via the regression approach satisfy these additional restrictions to a very high degree of
precision without imposing them in the estimation. Moreover, because we do not impose
these restrictions, our approach does not require the availability of a zero-coupon yield
curve, but can instead be readily used in applications with returns on coupon-bearing
bond portfolios as we discuss in Subsection 3.6. Another important diﬀerence between
our approach and those in JSZ and HW is that we do not impose the constraint that
principal components (or other linear combinations of yields) must be priced perfectly.
As a consequence, there is a potential inconsistency between actual and model-implied
principal components. However, we show in Subsection 4.5 that any such inconsistency
is numerically negligible in our preferred ﬁve-factor speciﬁcation.
Joslin, Singleton and Zhu (2011) show that Gaussian aﬃne dynamic term structure
models which impose these constraints imply additional restrictions across parameters.
Under certain assumptions, linear combinations of yields can be used as observable
pricing factors and the model parameters can be split into two subsets. The ﬁrst subset
summarizes the parameters governing the evolution of the pricing factors under the
historical measure.
JSZ show that for this subset, the ML estimator coincides with
11

the OLS estimator of a VAR(1) of the pricing factors. Hence, they suggest a two step
estimation approach. In the ﬁrst step, they estimate the parameters of the VAR(1) via
OLS. Then, in the second step, they estimate the remaining model parameters which
govern the evolution of pricing factors under the risk-neutral measure, via numerical
solution of the likelihood function taking as given the OLS estimates of the ﬁrst step.
We see several advantages of our method with respect to that of JSZ. First, JSZ
assume that the yield pricing errors are conditionally independent of lagged values of
yield pricing errors. This assumption allows them to reduce the computational complexity
of the estimation. Eq. (29) above shows that in aﬃne models where bond prices are
exponentially aﬃne functions of the pricing factors, serially uncorrelated yield pricing
errors give rise to autocorrelation of the return pricing errors. Serially correlated return
pricing errors, in turn, generate excess return predictability not captured by the pricing
factors.
We think that this is an undesirable assumption and indeed our empirical
results suggest that there is a strong level of serial correlation in yield ﬁtting errors
while there is little to no autocorrelation in return pricing errors. Second, the estimation
approach suggested by JSZ is tailored to aﬃne models that use linear combinations of
yields (such as principal components) as pricing factors. In contrast, our approach does
not require pricing factors to be linear combinations of yields but can also be readily
applied to models that use observable (and economically interpretable) pricing factors
such as macroeconomic variables. Third, while the approach in JSZ estimates a subset of
parameters via OLS, it still requires estimation of a subset of parameters via numerical
methods. These could be prone to issues related to the convergence to the global maximum
of the likelihood function. By contrast, our approach relies exclusively on linear regressions
which greatly alleviates such concerns.
Hamilton and Wu (2012) have recently proposed another multi-step estimation method
for aﬃne models which combines OLS regressions with numerical optimization. While
their method does not require a particular normalization of the model, it is also based
12

on the assumption that exactly K linear combinations of yields are observed and priced
without error while the remaining yields are observed with error. Based on this assumption,
HW ﬁrst run an OLS regression of the vector of observed yields on their contemporaneous
and lagged values. In further estimation steps, they then back out the remaining model
parameters by numerically minimizing a chi-squared objective function which summarizes
the deviations of the structural from the reduced form parameters, an approach which
is asymptotically equivalent to full information maximum likelihood. As in JSZ, HW
require that yield ﬁtting errors are not serially correlated, which as we discuss above
has strong implications for the properties of the return pricing errors. Indeed, Hamilton
and Wu (2011) show that popular aﬃne term structure models feature serially correlated
yield ﬁtting errors. Moreover, it does not appear that the HW method can be readily
applied to speciﬁcations which feature unspanned factors in the term structure of interest
rates which we show is easy in our setup. Finally, the HW approach requires numerical
optimization which our method avoids.
3.
Empirical results
In this section, we provide estimation results from our regression approach for diﬀerent
speciﬁcations of aﬃne term structure models.
We start by testing for the number of
factors necessary to explain the time series and cross section of Treasury returns. To
demonstrate the robustness of these results with respect to the choice of data, we do so
using diﬀerent combinations of Treasury yield and return data that have previously been
employed in the literature. The results of this analysis, discussed in Subsection 3.2, show
that the ﬁrst ﬁve principal components of Treasury yields are needed to explain Treasury
returns. We, therefore, choose a K = 5 factor speciﬁcation as our baseline example and
discuss its properties and implications in Subsection 3.3. We also estimate a model with
K = 4 factors in the style of Cochrane and Piazzesi (2008), which employs the ﬁrst three
13

principal components of Treasury yields and a return forecasting factor as pricing factors.
This model is presented in Subsection 3.4. We compare the two model speciﬁcations in
Subsection 3.5 and ﬁnd that the ﬁve-factor model outperforms the four-factor model in
economically important dimensions.
Both models use bond returns inferred from ﬁtted zero coupon yield curves. However, a
distinguishing feature of our estimation approach is that it does not require the availability
of zero coupon yield data. Instead, given a risk-free short-term rate as well as a set of
pricing factors that span the cross section of bond yields, we can obtain estimates of ﬁtted
zero coupon yield curves without observing these curves. To illustrate this capability, our
third speciﬁcation combines excess returns obtained from maturity-sorted portfolios of
coupon bearing bonds with the ﬁrst ﬁve principal components extracted from the set
of Treasury yields published in the Federal Reserve Board’s H.15 release. We discuss
estimation results for this speciﬁcation in Subsection 3.6.
3.1
Data
We estimate our baseline four- and ﬁve-factor speciﬁcations using the zero coupon yield
data constructed by Gurkaynak, Sack and Wright (2007, GSW).2 These data are based
on ﬁtted Nelson-Siegel-Svensson curves, the parameters of which are published along with
the estimated zero coupon curve. We use these parameters to back out the cross section
of yields for maturities n = 3, . . . , 120 months. From these yields we extract principal
components. Taking as the risk-free rate the n = 1 month yield, we calculate excess
returns for n = 6, 18, 24, . . . , 60, 84, and 120 month zero coupon bonds directly from Eq.
(6), giving a cross section of N = 12 maturities.
Our third speciﬁcation uses factors extracted from the constant maturity yields from
the Federal Reserve Board’s H.15 release and excess returns of Fama maturity-sorted bond
2We thank the authors for making these data available for download, on the website http://www.
federalreserve.gov/Pubs/feds/2006/200628/feds200628.xls
14

portfolios and the Fama one-month risk-free rate, available from the Center for Research
in Security Prices (CRSP). The Fama bond portfolios are sorted into six-month maturity
buckets with n = 1 −6, 7 −12, . . . , 55 −60 months in addition to a portfolio grouping
maturities 61 −120 months, for a total of N = 11 maturity groups. From the Fama
risk-free rate Rf
t and the monthly portfolio returns R(n−1)
t+1 , we calculate log excess returns
according to
rx(n−1)
t+1
= log

1 + R(n−1)
t+1

−log(1 + Rf
t ).
(30)
We estimate all models over the sample period 1987:01 – 2011:12, which provides
a total of T = 300 monthly observations.
Taken as given the set of pricing factors,
we estimate the parameters (Φ, Σ, σ, β, λ0, λ1) using our three-step estimation approach.
We further obtain estimates of the short rate parameters δ0 and δ1 by regressing the
one-month T-bill on the pricing factors. We then feed all parameter estimates into Eq.
(25) and Eq. (26) to obtain the recursive pricing parameters and use the latter to compute
model-implied yields of the maturities of interest.
3.2
Model speciﬁcation tests and identiﬁcation
We start by testing for the number of pricing factors. While early research by Scheinkman
and Litterman (1991) and Garbade (1996, Chapter 16) pointed out that three factors
are enough to explain the cross-sectional variation of yields, more recent papers such
as Cochrane and Piazzesi (2005, 2008) and Duﬀee (2011) emphasize the importance of
additional factors to explain Treasury returns.
Our estimation approach uses return regressions to ﬁt the cross section of yields and
allows for direct tests of the number of pricing factors. Whether the pricing factors explain
return variation is important for the identiﬁcation of the price of risk parameters. This
is easy to see in the three-step regression approach. Recall from Eq. (16) and Eq. (17)
that the market price of risk parameters are obtained via regressions onto the matrix of
15

factor risk exposures. Identiﬁcation of prices of risk thus requires that the stacked factor
loadings β′ are of full column rank.3
Because the asymptotic variance of β is of a simple OLS form [see Eq. (20)], we can
apply standard tools to assess the rank of β. We test for the possible rank deﬁciency using
the Anderson (1951) canonical correlations test. We denote the sample partial canonical
correlation between V and rx conditional on X−by ρi for i = 1, ..., K factors. Then,
under the null hypothesis that rank(β) ≤r < K, the Anderson test statistic is
rkr = −T
K
X
i=r+1
ln(1 −ρ2
i )
a∼χ2((K −r)(N −r)).
(31)
We can also test for the presence of unspanned or useless factors by checking whether
particular columns of β′ are equal to zero. This is straightforward to do based on the
asymptotic distribution of the factor risk exposures β from Eq. (20). Let βi be the ith
column of β′. Then, under the null that βi = 0N×1, the Wald statistic is
Wβi = ˆβ′
i ˆV−1
βi ˆβi
a∼χ2(N).
(32)
Table 1 displays the results of both test statistics for model speciﬁcations with three to
ﬁve factors using various combinations of Treasury return and yield data. In particular, we
report the Anderson test for the hypothesis that the rank of β in a K factor model is less
than or equal to K −1 (denoted rkK−1) and the Wald statistic for the null that the Kth
column of β′ is equal to zero. In Panel A of Table 1, we provide the test statistics for our
benchmark speciﬁcation, which uses both GSW returns and yields. Panel B reports tests
for the number of factors using the same yield data as Duﬀee (2010), who merges Fama
and Bliss yields of n = 3, 12, 24, ..., 60 months with GSW yields of maturities n = 72 and
n = 120 months. Panel C uses principal components extracted from the Federal Reserve
3See Kleibergen (2009) and Burnside (2012) for a related discussion in the context of static Fama and
MacBeth equity pricing models.
16

H.15 release, selecting maturities n = 6, 12, 24, 36, 60, 84, and 120 months.4 Finally, the
Panel D extracts factors from the CRSP constant maturity Treasury yield database using
maturities n = 12, 24, 60, 84, and 120 to which we append the three-month and six-month
T-bill from the CRSP Fama and Bliss discount bond yield data. The speciﬁcations on the
left-hand side are estimated using excess returns on zero coupon bonds calculated from
the GSW data set. The speciﬁcations on the right hand side are estimated using excess
returns on Fama maturity-sorted Treasury portfolios.
The tests unanimously support a ﬁve-factor speciﬁcation across the diﬀerent data
sets. The Wald tests overwhelmingly reject that the last column of β′ equals zero in the
ﬁve-factor speciﬁcation. The Anderson rank statistics also broadly support a ﬁve-factor
model. We conclude from these results that a ﬁve-factor speciﬁcation of an aﬃne term
structure model is likely to provide a better ﬁt of bond returns and, hence, bond risk
premiums than speciﬁcations with fewer factors. Importantly, this result is obtained for
the diﬀerent combinations of US Treasury yield and return data that have been used in
the extant literature and is, therefore, not driven by the particular data set we use in our
preferred ﬁve-factor speciﬁcation.
3.3
Estimation of a ﬁve factor model
Following the evidence in favor of a ﬁve-factor model from the tests above, we use it
as our baseline speciﬁcation. We now show that this speciﬁcation ﬁts the yield curve
close to perfectly and gives rise to substantial time variation in the prices of risk. Because
traditional term structure models are estimated imposing nonlinear cross-equation restrictions,
estimation of these models with more than three factors becomes computationally demanding.
In contrast, adding factors to the regression-based approach comes at no computational
cost.
4Joslin, Singleton and Zhu (2011) also use H.15 yields but ﬁrst extract the implied zero coupon yield
curve. Our estimation procedure does not require this additional step.
17

Table 2 reports the time series properties of the yield pricing errors implied by the
ﬁve-factor speciﬁcation of the model. We set µ = 0 because principal components are
extracted from demeaned yields. The average yield pricing errors are very small, not
exceeding 0.4 basis points in absolute value. Moreover, the standard deviation of the
yield pricing errors is tiny, remaining below 1 basis point for all maturities.
Finally,
consistent with our decomposition of yield pricing errors in Eq. (29), we ﬁnd evidence
of strong serial correlation in yield pricing errors while the return pricing errors have
essentially no autocorrelation.
The upper two panels of Fig. 1 show the time series of observed and ﬁtted yields for
the two- and ten-year Treasury notes. These plots show that the ﬁve-factor speciﬁcation
provides an extremely tight ﬁt to yields. It is worth emphasizing that the model has
been ﬁtted to returns. All parameters have been obtained via linear regressions, without
imposing the cross-equation recursions in Eq. (25) and Eq. (26). These equations have
been used only ex post, to allow the computation of all maturities of the yield curve.
Our results, therefore, suggest that traditional estimation approaches in which latent
pricing factors are jointly estimated with the model parameters by explicitly imposing
the cross-equation constraints provide little or no gains in terms of ﬁtting the yield curve.
The bottom two charts in Fig.
1 show the observed and ﬁtted one-month excess
holding returns on the same two maturities.
The actual excess returns are shown as
solid lines. The ﬁtted excess returns are given by the expression ˆB′
n−1

ˆλ0 + ˆλ1Xt

−
1
2

ˆB′
n−1 ˆΣ ˆBn−1 + ˆσ2
+ ˆB′
n−1ˆvt+1 and are shown as dashed lines. Both are almost indistinguishable
from one another, suggesting that the dynamics of excess bond returns are close to
perfectly captured by the ﬁve-factor model. We superimpose as dash-dotted lines the
expected excess return component ˆB′
n−1

ˆλ0 + ˆλ1Xt

−1
2

ˆB′
n−1 ˆΣ ˆBn−1 + ˆσ2
, which captures
the risk premium investors demand for holding a bond with n months to maturity for
one month. The charts show that risk premiums in the ﬁve-factor speciﬁcation exhibit
substantial time variation.
18

We now investigate the role of each of the factors in pricing the various components of
interest rate risk in the ﬁve-factor model. To that end, Table 3 reports the estimated
elements of λ0 and λ1 as well as the corresponding t-statistics.
Note that here and
throughout, the standard errors are calculated under the assumption that µ is unknown
to accommodate the sampling uncertainty from using demeaned yields. The price of level
risk has a signiﬁcant negative constant component (the top element in the vector λ0).
Excess return betas are negative multiples of the yield loadings bn = −1
nBn, implying
that investors on average require a positive expected excess return for holding the level
portfolio. In addition to level risk being nonzero unconditionally, we ﬁnd that it varies
signiﬁcantly as a function of the slope and the ﬁfth factor.
The loading of level risk
on the slope factor has a negative sign.
The model, therefore, implies that a higher
slope is associated with higher expected excess returns.
As can be seen in the lower
right-hand panel of Fig. 2, expected excess returns load positively on the slope factor
with coeﬃcients more or less linearly increasing in maturity. This is in line with prior
evidence on the predictive power of yield spreads for bond returns as, e.g., in Campbell
and Shiller (1991). We further ﬁnd that the ﬁfth principal component enters the price of
level risk with a strongly signiﬁcant positive coeﬃcient. This underscores that factors with
negligible contemporaneous eﬀects on the yield curve can have strong predictive power
for future excess returns, consistent with the ﬁndings of, e.g., Cochrane and Piazzesi
(2008) and Duﬀee (2011). The estimated price of risk coeﬃcients are also economically
important. For example, the coeﬃcient of the ﬁfth principal component in the price of
level risk is estimated to be 0.03. This implies that a 1 standard deviation decline in the
ﬁfth principal component increases the annualized expected excess return on the ten-year
Treasury bond by about 6%.
We can conveniently summarize the pricing implications of the model by testing the
null hypothesis that the diﬀerent rows of Λ (which combines λ0 and λ1) are equal to zero.
Given the asymptotic distribution of the estimator derived in Subsection 2.3, a Wald test
19

can be used to that eﬀect. In particular, let λ′
i· be the ith row of Λ. Then, under the null
that λ′
i· = 01×(K+1), the Wald statistic
WΛi· = ˆλ′
i· ˆV−1
λi· ˆλi·
a∼χ2(K + 1)
(33)
has an asymptotic chi-square distribution with K+1 degrees of freedom. In a similar vein,
we can test whether the price of risk associated with a given factor features signiﬁcant
time variation by testing if the corresponding row of λ1 is jointly equal to zero. Let λ′
1i·
be the ith row of λ1. Then, under the null that λ′
1i· = 01×K, the Wald statistic
Wλ1i· = ˆλ′
1i· ˆV−1
λ1i·ˆλ1i·
a∼χ2(K)
(34)
has an asymptotic chi-square distribution with K degrees of freedom.
The last two
columns in Table 3 provide these Wald statistics as well as the corresponding p−values
for the rows of Λ and λ1, respectively. In line with the individual signiﬁcance of the price
of risk parameters, these Wald statistics show that level risk is priced signiﬁcantly both
unconditionally and conditionally.
Slope risk is not priced in the ﬁve-factor model. None of the individual elements of
the second row of Λ is signiﬁcantly diﬀerent from zero, and both Wald statistics indicate
that these coeﬃcients are also jointly indistinguishable from zero. This result appears
surprising given that slope captures the second largest share of the cross-sectional variation
of yields. We return to this issue in Subsection 4.1.
While slope risk is not priced in the ﬁve-factor model, curvature risk, as measured
by the exposure to the third principal component of Treasury yields, carries a signiﬁcant
price of risk. The level factor, the curvature factor itself, as well as the fourth principal
component of yields all signiﬁcantly aﬀect the price of curvature risk over time. The
coeﬃcient of the price of curvature risk on the level factor is negative, indicating that
20

expected excess returns on a portfolio that is long in short-term and long-term government
bonds and short in intermediate maturities tend to be increasing in the level of rates.
While the price of level risk is signiﬁcantly determined by the ﬁfth principal component,
the price of curvature risk strongly varies with the fourth principal component, which
again highlights the role of higher-order principal components for expected bond returns.
The upper two panels of Fig.
2 provide a plot of unconditional ﬁrst and second
moments of yields across maturities as observed and ﬁtted by the ﬁve-factor model. The
charts show that the speciﬁcation ﬁts both moments very well. The lower left panel of
Fig. 2 provides a plot of the estimated yield loadings bn. While these graphs reinforce
the common interpretation of the ﬁrst three principal components of yields as level, slope,
and curvature, they also highlight why higher order principal components of yields have
been given much less attention in the literature. The lower left panel of Fig. 2 shows
that the loadings of yields on the fourth and ﬁfth principal components are very small.
This is in sharp contrast to the the lower right panel of Fig. 2, which shows the loadings
B′
nλ1 of expected excess returns on all model factors. The loadings on the fourth and ﬁfth
principal components exhibit strong variation across maturities. In fact, expected returns
are explained nearly entirely by the second, fourth, and ﬁfth principal components, while
yields are explained almost exclusively by the ﬁrst three principal components.
We can assess the economic signiﬁcance of the various risk prices by computing their
contribution to the variability of the pricing kernel. Recalling that
ln Mt+1 = −rt −1
2λ′
tλt −λ′
tΣ−1/2νt+1,
(35)
it is straightforward to decompose the conditional volatility of the pricing kernel into the
contributions due to each price of risk according to
Vart (ln Mt+1) = λ′
tλt =
K
X
j=1
λ2
jt.
(36)
21

Doing so, we ﬁnd that risk prices of all ﬁve factors contribute to the time variation of the
pricing kernel (see the upper left chart in Fig. 3). However, given that the exposure of
long term bonds to risks other than level risk is fairly small, the statistical signiﬁcance
of their market prices of risk does not translate into a sizable impact on expected excess
returns on those bonds. As the lower left chart in Fig. 3 shows, it is primarily, but
not exclusively, the time variation of level risk that contributes to time-varying expected
excess returns on the ten-year Treasury bond. This time variation in turn is largely, but
not exclusively, driven by movements in the slope and the ﬁfth principal component, as
shown in the lower right chart of Fig. 2.
We derive the recursive pricing formulas in Eq. (25) and Eq. (26) by equating our
return generating process in Eq. (12) with the deﬁnition of excess returns in Eq. (6) under
the assumption that log bond prices are linear in the state variables X. The matching
of terms implies that our recursive bond pricing parameters Bn, which are functions of
the parameters Φ, Σ, σ, δ0, δ1, λ0, and λ1, must be equal to the coeﬃcients β(n) from the
time series regressions of excess returns on the estimated factor innovations ˆv for all
maturities n. The restriction is not imposed in the estimation. The diﬀerence between
the imputed recursive pricing parameters ˆBn and the regression coeﬃcients ˆβ(n) can serve
as a diagnostic of how well the aﬃne model can replicate Treasury return dynamics.
Fig. 4 provides plots of the two sets of coeﬃcients. They are visually indistinguishable
for all maturities for the ﬁrst three factors. While they diﬀer slightly for the fourth and
ﬁfth factors, that diﬀerence is economically negligible. Analytic standard error bands for
β are plotted in gray. The tight intervals indicate that these elements are estimated very
precisely. To summarize, the ﬁve-factor speciﬁcation of our aﬃne term structure model
appears to be able to replicate the dynamics of Treasury yields and returns very well.
22

3.4
Four-factor speciﬁcation
The results above show that the predominant share of the variation of expected excess
bond returns in the ﬁve-factor speciﬁcation is driven by the second, fourth, and ﬁfth
principal components of Treasury yields. However, Cochrane and Piazzesi (2008, CP)
ﬁnd that a single return forecasting factor is able to explain the bulk of the predictability
in excess returns. They augment this factor with the ﬁrst three principal components
of orthogonalized yields and estimate an aﬃne term structure model, positing a highly
restricted form for the price of risk matrix Λ. In their model, only the upper element of
λ0 and the loading of level risk on the return forecasting factor are allowed to be nonzero.
These restrictions eﬀectively imply that only level is allowed to be a priced risk factor and
only the return forecasting factor drives time variation in bond risk premiums.
We estimate a four-factor model similar to the one in Cochrane and Piazzesi (2008)
within our regression-based framework. This allows us to directly assess the statistical
and economic evidence toward such a speciﬁcation. We compare the results obtained from
the four-factor model with that obtained from our baseline ﬁve-factor model and discuss
the interpretation of the price of risk estimates.
To generate a factor that summarizes one-month excess return predictability optimally
in-sample among linear combinations of bond yields, we calculate our version of the CP
factor by regressing monthly GSW excess returns onto the vector of ten one month lagged
GSW one-year forward rates Ft according to
rxt+1 = γ0 + ΓFt + ηt+1.
(37)
The average R2 across these individual predictive return regressions is 7.5%. Following
Cochrane and Piazzesi (2008), we deﬁne the CP factor xt to be the ﬁrst principal component
of the ﬁtted values ˆΓFt, standardized to zero mean and unit variance. The ﬁrst principal
23

component explains 94.65% of the cross-sectional variance of all ﬁtted one-month excess
returns. We estimate the model by augmenting this factor with the ﬁrst three principal
components extracted from the cross section of Treasury yields.
Our approach diﬀers in a few regards from that employed by Cochrane and Piazzesi
(2008). Most important, their factor is constructed by placing one-year excess holding
period returns on the left hand side of the regression. However, because the speciﬁcation
in Eq. (12) holds exactly only for monthly excess returns, we prefer to extract a factor
that best predicts returns at this frequency. Also in contrast to CP, we use ten annual
GSW forward rates instead of ﬁve Fama and Bliss annual forward rates. This is because
we ﬁnd that the GSW data provide a better in-sample ﬁt for excess returns at the monthly
frequency. Finally, unlike CP, we do not orthogonalize yields with respect to the return
forecasting factor before extracting principal components. Instead, we deﬁne level, slope,
and curvature as the ﬁrst three principal components of the Treasury yields in our data set.
We do so to guarantee that the three factors are identical across the model speciﬁcations
that we compare.
Table 4 reports summary statistics for the yield and return pricing errors of the
four-factor model. These indicate that the in-sample ﬁt is somewhat less precise in the
four-factor model than in the ﬁve-factor model, but with average pricing errors no larger
than 2.9 basis points in absolute value, and standard deviations of these errors of less than
5 basis points, the ﬁt is good. The return pricing errors continue to display little serial
correlation, whereas yield pricing errors are highly autocorrelated. The upper panels of
Fig. 5 plot the observed and ﬁtted values of the two- and ten-year Treasuries, showing
that the ﬁtting error is economically negligible.
The lower panels of Fig.
5 plot the
observed and ﬁtted excess returns as well as the predicted excess returns. The predicted
excess returns display signiﬁcant time variation, comparable to the dynamics observed in
the ﬁve-factor model.
Table 5 shows that the CP factor is a signiﬁcant determinant of the prices of risk
24

of all pricing factors except for slope. In fact, for level risk, the CP factor is the only
signiﬁcant pricing factor, driving out the signiﬁcance of the slope factor that had been
present in the ﬁve-factor speciﬁcation. This is in line with the speciﬁcation in Cochrane
and Piazzesi (2008), who restrict this coeﬃcient to be the only nonzero element in λ1. As
in the ﬁve-factor model, the estimated price of risk coeﬃcients are economically important
in the four-factor speciﬁcation. In particular, the −0.043 coeﬃcient of the CP factor in
the price of level risk implies that a positive 1 standard deviation shock to the CP factor
increases the annualized expected excess return on the ten-year Treasury bond by 8.7%.
The slope factor is not signiﬁcant for any of the price of risk parameters in the four-factor
speciﬁcation, also in line with CP. However, the level and curvature factors continue to
remain signiﬁcant determinants of the price of curvature risk. This implies that the CP
factor does not entirely subsume the variation of expected bond returns that is captured
by the principal components in the ﬁve-factor speciﬁcation.
These results suggest that the parameterization chosen by Cochrane and Piazzesi
(2008) for the price of risk dynamics might be overly restrictive. Using a Wald statistic
akin to Eq. (33), we can explicitly test for the joint signiﬁcance of the elements of Λ
that CP restrict to be zero. We overwhelmingly reject the null that these elements are
jointly equal to zero with a p-value of 10−6. Hence, we ﬁnd that the tight restrictions
imposed by Cochrane and Piazzesi (2008) on the price of risk dynamics are clearly not
supported in the model on statistical terms. Moreover, imposing the CP restriction on
Λ using the minimum distance estimator discussed in Subsection 4.2, we ﬁnd that the
ﬁt of the four-factor model deteriorates, with yield pricing errors increasing substantially
across all maturities but especially at the long end of the yield curve.
That being said, the predictability in excess returns is clearly dominated by the CP
factor within the four-factor speciﬁcation. As can be seen in the lower right panel of
Fig. 6, the CP factor predicts positive excess returns across the yield curve in a manner
increasing in maturity. This closely matches the pattern shown by Cochrane and Piazzesi
25

(2008) for one-year excess returns.
Given these ﬁndings and the results from the ﬁve-factor model, it is instructive to
study the relation between the CP factor and the principal components of Treasury
yields. Interestingly, we ﬁnd that even ﬁve principal components fail to entirely span
the CP factor: A regression of xt on the ﬁve PCs from our benchmark model yields an
R2 of only 65.6%. This is especially striking given that 99.99% of variation in yields
are explained by the ﬁrst ﬁve principal components, considering that xt is constructed
as a linear combination of these yields. The pairwise correlations between the return
forecasting factor and the ﬁrst ﬁve principal components of Treasury yields in our data
set are 5%, 45%, 19%, -17%, and -62%, respectively. This corroborates the ﬁndings of
Subsection 3.3 where we show that the ﬁfth principal component is a predominant driver
of risk premiums in the ﬁve-factor speciﬁcation, followed by the second, third, and fourth
principal components.
Finally, the curvature and CP factors are both found to be priced in the four-factor
speciﬁcation, as indicated by the corresponding Wald statistics. This is in contrast to the
restrictions imposed by Cochrane and Piazzesi (2008), who force these risk prices to be
zero.
We again assess the economic signiﬁcance of the various risk prices by computing
their contribution to the variability of the pricing kernel. We ﬁnd that risk prices of all
four factors contribute to the volatility of the pricing kernel (see the upper right chart in
Fig. 3). Yet, as in the ﬁve-factor model, only the exposure of long term bonds to level
risk is sizable. Hence, the market prices of risk of the remaining factors have a modest
impact, at best, on expected excess returns. As Fig. 3 shows, it is primarily the time
variation of level risk that contributes to time varying expected excess returns on the
ten-year Treasury bond. This time variation, in turn, is largely but not exclusively driven
by movements in the CP factor, as highlighted in the lower right panel of Fig. 6.
To summarize, the results in this subsection have shown that strong support exists for
26

the importance of a Cochrane and Piazzesi-type return forecasting factor in explaining
Treasury return dynamics. However, the tight parametric restrictions that CP impose on
risk price dynamics are statistically not supported by our estimates. Finally, comparing
the term premium implied by the four-factor speciﬁcation with that of the ﬁve-factor
model, we conclude that the unrestricted four-factor CP speciﬁcation captures similar
term premium dynamics as the ﬁve principal component speciﬁcation but implies somewhat
larger in-sample yield ﬁtting errors.
3.5
Comparing the ﬁve- and four-factor speciﬁcations
The evidence presented thus far does not appear suﬃcient to designate which of the
two models provides a better representation of the data. In this subsection, we consider
their out-of-sample performance both in the cross section and in the time series. We
ﬁnd that the ﬁve-factor model outperforms the four-factor model across both dimensions.
To provide an additional benchmark, we report results for a four-factor model with CP
treated as an unspanned factor and a ﬁve-factor model with PC4 and PC5 treated as
unspanned factors (Subsection 4.1 explains how to impose the unspanning restriction in
the estimation). The upper-left panel of Fig. 7 shows that the in-sample term premium
dynamics are very similar across all speciﬁcations. In particular, the ﬁve-factor models
and the four-factor models exhibit closely aligned term premiums. Term premiums are of
economic interest because they allow inference of risk-adjusted expectations of the path
of future short-term interest rates. Thus, a natural way to compare the diﬀerent models
is to investigate their ability to predict future short-term interest rates. To generate these
forecasts, we begin by using the period 1987:01–1991:12 as a training sample and then
proceed to reestimate each model at monthly intervals with an expanding estimation
window and compare their average short-rate predictions up to ﬁve years ahead with
the realized data.
For comparison, we also include the average forecast error from a
simple random walk of the one-month T-bill. In the upper-right panel of Fig. 7, we
27

display the root mean square prediction error of average short rates at forecast horizons
from one month through ﬁve years. The chart shows that the ﬁve-factor model and the
model with PC4 and PC5 treated as unspanned factors outperform the random walk
across all horizons. In contrast, the four-factor model and the model with CP treated
as an unspanned factor display somewhat larger forecast errors, most notably at longer
horizons.
This short rate prediction exercise thus suggests that the ﬁve-factor model
provides a better forecast performance in the time series than the four-factor model.
To assess the cross-sectional performance of the diﬀerent model speciﬁcations we
perform the following exercise. We continue to estimate each model using returns on
bonds with maturities up to ten years. We then compare the model-implied yields on
bonds with maturities up to 20 years relative to their actual values. In the lower-left
panel of Fig. 7 we plot the results from this analysis. Although the four-factor model
produces a good in-sample ﬁt to maturities up to ten years, the chart shows that the
model-implied yields for longer maturities are far below their realized values. This is not
the case for the ﬁve-factor speciﬁcation, which produces slightly higher average yields
than in the realized data, but closer to the realized data than either of the speciﬁcations
using unspanned factors. This suggests that the four-factor model strongly understates
the degree of persistence of the pricing factors under the risk-neutral measure, whereas
the ﬁve-factor model only slightly overstates it. Interestingly, Joslin, Singleton and Zhu
(2011), using their likelihood-based estimation approach, ﬁnd that a model using all of
the ﬁrst ﬁve principal components of yields as pricing factors and estimated without
observations on longer maturity bonds produces implausible average bond yields on very
long maturity bonds. Here we show, using our methodology, that this is not a general
feature of ﬁve-factor models.
As a robustness check, the lower-right panel of Fig.
7
displays the in-sample ﬁt when each model is estimated using returns on bonds with
maturities up to 20 years. In this case, the ﬁve-factor model is very close to the observed
yields, whereas the four-factor model exhibits more pronounced deviations.
28

In sum, the results presented in this subsection suggest that relative to the four-factor
model with three principal components of yields and the CP factor, the ﬁve-factor model
produces better out-of-sample forecasts of future short rates and is more robust to the
choice of maturities used in estimation. While all of these speciﬁcations capture term
premium dynamics in similar ways, the superior out-of-sample performance of the ﬁve-factor
model leads us to designate it as our preferred speciﬁcation.
3.6
Estimation using maturity-sorted portfolios
So far, we have seen that diﬀerent speciﬁcations of multi-factor aﬃne models estimated
using our regression-based approach are able to tightly match data obtained from a smooth
zero coupon yield curve. However, an important feature of our estimation approach is
that the availability of a wide cross section of zero coupon bonds is not necessary for the
estimation of the term structure. The only data required for our procedure are a panel of
excess returns and a corresponding set of return spanning factors. Our third benchmark
speciﬁcation highlights this attractive feature of the regression-based approach. Here, we
generate a no-arbitrage zero coupon yield curve from a cross section of K = 5 principal
components extracted from the Federal Reserve’s H.15 Treasury yield data and N = 11
excess returns on Fama maturity sorted bond portfolios from CRSP. Both sets of data
are constructed from coupon bearing bonds. This reduces estimation error with respect
to the standard practice of ﬁtting term structure models to zero coupon yields.
Given the excess holding period returns as well as the pricing factors, we estimate the
model parameters (Φ, Σ, σ, λ0, λ1) using our three-step estimation approach. We further
estimate δ0 and δ1 by regressing the log Fama one-month T-bill on the pricing factors.
Based on these parameters, we can then use Eq.
(25) and Eq.
(26) to compute the
loadings An and Bn, which, along with the pricing factors X, allow us to impute zero
coupon yields for bonds of any maturity.
The upper panels of Fig.
8 plot the two-year and ﬁve-year maturities implied by
29

the model against the corresponding Fama and Bliss discount bond yields, displaying
a visually close ﬁt.
It is important to note that this is not by construction, as the
two sets of zero coupon yields have been estimated using diﬀerent methodologies. The
Fama and Bliss discount bond yields are ﬁtted to the cross section of Treasury bonds
period by period. Instead, our estimated zero curve is directly implied by a no-arbitrage
term structure model, which imposes internal consistency between the time series and
the crosssection of yields. The lower panels of Fig. 8 show that the model-implied excess
returns for zero coupon bonds closely match the observed excess returns of Fama maturity
sorted portfolios. In sum, we see it as a particular strength of our estimation approach to
generate a model-based zero coupon yield curve from returns on coupon-bearing securities.
The use of excess returns from maturity-sorted portfolios could cause problems due
to the changing composition of underlying securities. To address this concern, we ﬁrst
employ the test of parameter stability described by Andrews (1993). The generalized
method of moments (GMM) framework of Andrews (1993) is easily applied to the OLS
regression in Eq. (15). We obtain a value of 31.70 for the sup −LM statistic [we choose
a standard calculation window of π = (15%, 85%)], which is well below the corresponding
90% critical value.
In addition to assessing the stability of estimated betas for each
portfolios’ return, we approximate the portfolios’ betas at every point by the weighted
average of the betas corresponding to the individual cash ﬂows of the underlying securities
(principal and coupon payments). Doing so, we see that the betas at the portfolio level
are very stable for maturities up to ten years but exhibit pronounced time variation for
the portfolio containing bonds that mature in ten years or more. This latter result is not
surprising as large diﬀerences exist in duration between the diﬀerent securities in that
portfolio and, hence, the interest rate sensitivity of that portfolio can vary considerably
over time. Consequently, we use the maturity-sorted portfolios up to ten years and drop
the Fama portfolio with maturities above ten years in the estimation.
30

4.
Extensions
In this section we present a number of extensions and further results. First, we explain
how to estimate the model in the presence of unspanned factors. Second, we show how
to impose linear restrictions on risk exposures and market prices of risk in the estimation
of the model. Third, we show that the maximal Sharpe ratios implied by the four- and
ﬁve-factor speciﬁcations are very reasonable, with an average level below one and peaks
below 2.5. Fourth, we explain how the model can be used to ﬁt the yield curve at the daily
frequency. Finally, we show that the implied principal component loadings from the term
structure model are statistically indistinguishable from the actual principal component
loadings.
4.1
Unspanned factors
Recent models of the yield curve have featured unspanned factors that not aﬀect the
dynamics of bonds under the pricing measure, but do aﬀect them under the historical
measure (see Joslin, Priebsch and Singleton, 2012; Duﬀee, 2011; and Wright, 2011). The
predictability under the historical measure is consistent with previous work that ﬁnds that
macroeconomic factors have forecasting power for the term structure (see, e.g., Moench,
2008; and Ludvigson and Ng, 2009). The assumption that a given factor does not aﬀect
bond yields under the pricing measure can be implemented by imposing the restriction
that the corresponding elements of {Bn, n = 1, . . . , N} be exactly equal to zero.
This restriction can be readily incorporated in our regression-based setting. Partition
the factors into spanned factors Xs
t with nonzero risk exposures and unspanned factors
Xu
t , which have zero risk exposures. The factors continue to follow a joint VAR process
31

under the historical measure


Xs
t
Xu
t

= µ + Φ


Xs
t−1
Xu
t−1

+


vs
t
vu
t

,
(38)
where Xs
t is of dimension Ks ×1, Xu
t is of dimension Ku ×1, and µ and Φ are partitioned
accordingly. The spanning restriction is that the risk exposures of the unspanned factors
are equal to zero, i.e. β(n) = [β(n)′
s
0]′ for all n = 1 . . . N. Using Eq. (26) and Eq. (28),
this restriction implies δ′
1 = [δs′
1 0], so that the short rate does not load on any unspanned
factors. It further implies that the upper right Ks×Ku block of the risk-neutral transition
matrix Φ⋆= (Φ −λ1) is zero, i.e.
Φ⋆=


Φss −λss
1
0
Φus −λus
1
Φuu −λ1
uu

.
(39)
With this restriction, the return generating process can be rewritten as
rx(n−1)
t+1
=β(n−1)′  λ0
s+λ1Xt+vt+1

−1
2
 β(n−1)′Σβ(n−1)+σ2
+e(n−1)
t+1
(40)
=β(n−1)′  λ0+λ1Xt+Xt+1−ΦXt−µ

−1
2
 β(n−1)′Σβ(n−1)+σ2
+e(n−1)
t+1
(41)
=−β(n−1)′
s
(µ⋆
s+Φ⋆
ssXs
t)−1
2

β(n−1)′
s
Σssβ(n−1)
s
+σ2
+β(n−1)′
s
Xs
t+1+e(n−1)
t+1 ,
(42)
where µ⋆
s denotes the upper Ks × 1 subvector of the risk-neutral mean µ⋆= (µ −λ0), Φ⋆
ss
denotes the upper left Ks×Ks block of Φ⋆, and Σss is equal to the upper left Ks×Ks block
of Σ. Estimation of this model proceeds with only a slight modiﬁcation of the three-step
procedure. As before, we obtain estimates of the VAR parameters and innovations in
Eq. (38) ˆvt+1 using OLS. Denote Xs
−and Xs as the stacked lagged and contemporaneous
values of spanned factors. We then estimate the regression
rx = asι′
T + csXs
−+ β′
sXs + E,
(43)
32

where as is an N × 1 vector and β′
s and cs are N × Ks matrices. We see from Eq. (40)
that now as = −β′
sµ⋆
s −1
2 (B⋆svec (Σss) + σ2ιN) with B⋆s the ﬁrst K2
s columns of B⋆.
We can also see that cs = −β′
s Φ⋆
ss. We can then estimate the parameters governing the
risk-neutral dynamics of the pricing factors according to
ˆµ⋆
s = −

ˆβsˆβ′
s
−1 ˆβs

ˆas + 1
2

ˆB⋆svec

ˆΣss

+ ˆσ2ιN

(44)
and
ˆΦ⋆
ss = −

ˆβsˆβ′
s
−1 ˆβsˆcs.
(45)
Denoting ˆΨ⋆
ss =
h
ˆµ⋆
s
ˆΦ⋆
ss
i
, we can write these estimators in the single expression
ˆΨ⋆
ss =−

ˆβsˆβ′
s
−1 ˆβs

rx+ 1
2

ˆB⋆svec

ˆΣss

+ˆσ2ιN

ι′
T

M s
xZs′
−
 Zs
−M s
xZs′
−
−1 ,
(46)
where Zs
−=

ιT Xs′
−
′ and M s
x = IT −Xs′ (XsXs′)−1 Xs. We then obtain
ˆΛss = ˆΨss −ˆΨ⋆
ss
(47)
We further set
ˆλsu
1 = ˆΦsu
(48)
in accordance with the spanning restriction in Eq. (39). The parameters µ⋆
u and Φ⋆
u·
are not identiﬁed in this model. They do not matter for bond pricing, so we adopt the
convention of setting the corresponding prices of risk ˆλu
0 and ˆλu·
1 equal to zero. This is
equivalent to setting the risk neutral parameters equal to the physical VAR estimates ˆµu
and ˆΦu.
We can see from Eq. (47) and Eq. (48) above that the estimator of market prices
of risk in the unspanned factor case is a linear combination of estimated parameters
governing the historical and risk-neutral dynamics of pricing factors. We show that the
33

two estimators have the joint limiting distribution
√
T


vec

ˆΛss −Λss

vec

ˆλsu
1 −λsu
1



d
−→N



0
0

,


Vss
Λ
Css,su
Λ,λ1
Css,su′
Λ,λ1
Vsu
λ1




,
(49)
where Vss
Λ , Vsu
λ1 and Css,su
Λ,λ1 are provided in the Appendix.
We illustrate estimation of an aﬃne model with unspanned macroeconomic factors by
using the speciﬁcation in Joslin, Priebsch and Singleton (2012). Their model features as
pricing factors the ﬁrst three principal components of Treasury yields as well as the ﬁrst
principal component of monthly core consumer price index inﬂation and monthly core
personal consumption expenditures inﬂation and the Federal Reserve Bank of Chicago
National Activity Index (CFNAI) as unspanned macroeconomic factors. According to
a Wald test of the signiﬁcance of columns of beta obtained by including the additional
factors in the regression in Eq. (15), we do not reject the null that the inﬂation factor has
zero betas with p = 88.63. Similarly, we do not reject that the betas for the exponentially
smoothed CFNAI equal zero with p = 96.81. These ﬁndings, thus, justify the assumption
of treating these macroeconomic factors as unspanned in a speciﬁcation that also features
the ﬁrst three principal components of Treasury yields.
Unreported results show that the unspanned macro factor speciﬁcation provides a
somewhat poorer ﬁt to the cross section of Treasury yields than the four- and ﬁve-factor
speciﬁcations. Estimates of the market prices of risk and the corresponding test statistics
are provided in Table 6. They diﬀer in some ways from the ones already discussed. As
in the ﬁve-factor speciﬁcation, the second principal component signiﬁcantly drives time
variation in slope risk. Nonetheless, we can reject only that the ﬁrst row of λ1 is equal
to zero at a 10% level. This is at odds with the implications of the ﬁve- and four-factor
models which show substantial amounts of time variation in level risk that are largely due
to movements in higher order principal components or the CP factor, respectively. This
34

suggests that the speciﬁcation proposed by Joslin, Priebsch and Singleton (2012), which
uses the ﬁrst three principal components of yields and two macroeconomic variables as
pricing factors, does not fully capture the dynamics of the price of level risk implied
by the yield factor-based speciﬁcations.
Furthermore, the coeﬃcient of the price of
slope risk on the CFNAI series is highly statistically signiﬁcant and, as a consequence,
slope risk is priced in this model speciﬁcation.
This is consistent with the results of
Joslin, Priebsch and Singleton (2012) but is in contrast to the pricing implications of the
four- and ﬁve-factor models. This can be interpreted as indicating that the information
contained in the yield curve is insuﬃcient to completely characterize the time variation
in the price of slope risk. Due to the ease of estimation of the term structure model in
the regression-based approach, alternative speciﬁcations with other unspanned factors are
straightforward to estimate.
4.2
Restricted market prices of risk
Numerous authors have considered aﬃne term structure models in which certain elements
of Λ are set equal to zero. These models could be easily estimated in our framework using a
minimum distance procedure as follows. Let θ =
 vec (Λ)′ , vec (β)′ , vec (Φ)′ , σ2, vech (Σ)
′
and ˆθ similarly, where vech (·) is the vector-half operator.
Let H be a q × p known
matrix with full row rank, where p = (K (K + 1) + NK + K2 + 1 + K (K + 1)/ 2). This
matrix contains the linear restrictions we would like to place on Λ.
For example, if we
wanted to impose a linear restriction only on the second element of λ0, we would choose
H = [0 1 0 · · · 0].
Under these restrictions, the minimum distance estimator solves
min
θ
T ·

ˆθ −θ
′
WT

ˆθ −θ

s.t.
Hθ = 0,
(50)
where WT is a p × p positive deﬁnite weighting matrix. Because the restrictions on θ are
35

linear, the solution to this optimization problem is
ˆθmd = ˆθ −W −1
T H′  HW −1
T H′−1 H ˆθ.
(51)
Then, by construction H ˆθmd = 0, so we have new estimators for the parameters that
satisfy the desired restrictions. The optimal choice of weighting matrix is a consistent
estimator of the inverse of the asymptotic variance of the unconstrained estimator ˆθ (i.e.,
if Vθ is the asymptotic variance of ˆθ, then WT →p V−1
θ ). In the Appendix we provide the
elements of Vθ. Under this choice of weighting matrix,
√
T

ˆθmd −θ

d
−→N

0, Vθ −VθH′ (HVθH′)−1 HVθ

.
(52)
4.3
Sharpe ratios
From Eq. (8), the conditional Sharpe ratio can be expressed as
Et
h
rx(n−1)
t+1
i
+ 1
2V art
h
rx(n−1)
t+1
i
r
V art
h
rx(n−1)
t+1
i
=
Covt
h
rx(n−1)
t+1 , ln Mt+1
i
r
V art
h
rx(n−1)
t+1
i
.
(53)
The Sharpe ratio in Eq. (53) is maximized for a hypothetical return to a portfolio of bonds
that replicates the payoﬀto the log pricing kernel exactly. The model-implied maximal
Sharpe ratio is, therefore,
p
V art [ln Mt+1] =
p
λ′
tλt.
(54)
The maximal Sharpe ratio provides a useful diagnostic of the validity of the stochastic
discount factor. Duﬀee (2010) argues that ﬁve-factor aﬃne models of the term structure
can give rise to excessively high maximal Sharpe ratios due to overﬁtting. However, we
do not ﬁnd unreasonable maximal Sharpe ratios in our four- and ﬁve-factor speciﬁcations,
as can be seen in Fig. 9. For the ﬁve-factor speciﬁcation, the peak in the maximal Sharpe
36

ratio is 2.30, with a sample average maximal Sharpe ratio below one.
As Eq. (54) shows, the maximal Sharpe ratio implied by an aﬃne term structure
model depends on the inner product of the market prices of risk and, hence, on the price
of risk parameters λ0 and λ1. As discussed in Subsection 4.1, a subset of the latter is not
identiﬁed in the presence of unspanned factors. We know that the fourth and ﬁfth principal
components are weakly spanned only by bond yields because level, slope, and curvature
explain almost all of the cross-sectional variation of yields. Accordingly, the rows of λ0 and
λ1 corresponding to the fourth and ﬁfth principal component in the ﬁve-factor speciﬁcation
of the model could only be weakly identiﬁed, thus potentially resulting in somewhat higher
maximal conditional Sharpe ratios than what one can perceive as reasonable.
To assess whether this weak spanning of the fourth and ﬁfth principal component
is a potential concern in the model, we perform the following robustness check.
We
make the extreme assumption that the fourth and ﬁfth principal components are entirely
unspanned and, hence, the corresponding market price of risk parameters is unidentiﬁed.
We then reestimate the ﬁve-factor speciﬁcation of the model by imposing the spanning
restrictions outlined above to the fourth and ﬁfth principal components, eﬀectively setting
to zero the lower two rows of λ0 and λ1 and ﬁxing the upper right block of λ1 to be equal
to the respective block of ˆΦ.
As can be seen in the lower left panel of Fig.
9, the
resulting Sharpe ratio is estimated at slightly lower values. However, as in Subsection
3.5, the term premium implied by the restricted ﬁve-factor model is very similar when
the fourth and ﬁfth principal components are treated as unspanned.
In unreported
results, we also computed the maximal Sharpe ratio of the ﬁve-factor model in which we
impose the restriction that the second and fourth principal components are not priced.
Consistent with our ﬁnding that the prices of risk of these two factors are statistically
indistinguishable from zero in the full ﬁve-factor model, this speciﬁcation produces a very
similar time series of the maximal Sharpe ratio as in the upper left panel of Fig. 9.
We also show the Sharpe ratio of the four-factor CP speciﬁcation in the upper right
37

panel of Fig. 9. While it is comparable in magnitude to that of the ﬁve-factor model,
the time series patterns of the two Sharpe ratios do at times diﬀer substantially. For
example, during the ﬁnancial crisis, the Sharpe ratio implied by the four-factor model
tends to be higher than that of the ﬁve-factor model, while that of the ﬁve-factor model
is higher during the late 1980s. The lower right-hand panel of Fig. 9 shows the Sharpe
ratios of the unspanned macro factor model. This time series of maximal Sharpe ratios is
somewhat smoother than the ones implied by the ﬁve- and four-factor speciﬁcations but
otherwise shows similar dynamics.
4.4
Term structure estimation in real time
As we ﬁt the model using simple linear regressions, estimation is extremely fast. This
is in sharp contrast to traditional likelihood-based estimation of such models subject to
nonlinear cross-equation restrictions, which typically require a long numerical optimization
process.
The simplicity and the speed at which it is estimated makes our approach
particularly appealing for the real time analysis of term structure dynamics.
In this
subsection, we show how we ﬁt an aﬃne model to the US Treasury yield curve at the
daily frequency. This allows us to interpret yield curve movements in terms of risk-neutral
yield versus term premiums dynamics in real time.
Estimation at the daily frequency requires a slight modiﬁcation of the empirical
approach outlined so far. In the daily application of the model, we use the daily yields of
maturities from n = 3, . . . , 120 months obtained from Gurkaynak, Sack and Wright (2007).
We aggregate the daily yields to the monthly frequency by selecting end-of-month values
and extract principal components from these monthly yields. We then apply the weights
from the monthly principal components to the daily yields to obtain daily estimates of
our pricing factors.5
5Because we extract the principal components from demeaned monthly yields, we need to make an
adjustment to the daily factors.
We apply the monthly principal components weights to the sample
average of the monthly yields and then substract this vector from the daily factors obtained as described
38

We continue to compute log excess holding period returns at the monthly frequency
and obtain estimates of the parameters of the model as outlined in Subsections 2.2 and
2.4.
Finally, we use the estimated parameters and the daily yield factors to impute
model-implied yields and term premiums at the daily frequency. To illustrate the ability
of the model to ﬁt daily term structures, Fig. 10 shows for the K = 5 factor speciﬁcation
the daily observed and model-implied yields for the two-year, ﬁve-year, and ten-year
Treasury notes since August 2009. The model prices all three maturities precisely.
Perhaps more interesting is an analysis of term premiums over this sample period. As
discussed in Subsection 2.4, we can use the model to achieve a decomposition of interest
rates into risk neutral yields and term premiums. The lower right panel of Fig. 10 displays
the estimated term premium for the ten-year Treasury along with the one-month Merrill
lynch Option Volatility Estimate (MOVE) index.
The latter is a measure of implied
volatilities from options on Treasury futures. The plot shows that our term premium
estimate and the MOVE index exhibit a strong correlation. This is striking because the
model is estimated without using any option data. We interpret the correlation between
the two time series as evidence that our term premium estimate reﬂects the risk of holding
Treasury securities.
4.5
Consistency of principal components as observable factors
Traditional estimation methods for aﬃne term structure models typically treat pricing
factors as latent variables that are backed out from observed yields using ﬁltering or
observation equation inversion techniques. Our estimation approach is diﬀerent in that it
requires the pricing factors X to be observed. We treat principal components extracted
from yields as observed, thus ignoring the ﬁtting error associated with the principal
component extraction.
This potentially gives rise to an inconsistency between actual
and model-implied principal components. However, this inconsistency is negligible.
before.
39

Let X be the K × T matrix of principal components of yields y. We can write
X = PyMι.
(55)
where Mι = IT×T −1
T ιTι′
T is the T × T time series demeaning operator and P is the
K×N matrix of principal component loadings. Actual observed yields can be decomposed
into ﬁtted yields and ﬁtting errors: y(n)
t
= ˆy(n)
t
+ ˆε(n)
t .
Then, because model-implied
yields are assumed to be aﬃne in the pricing factors X, we have y(n)
t
= ˆan + ˆb′
nXt + ˆε(n)
t
= −1
n

ˆAn + ˆB′
nXt + ˆu(n)
t

. We can thus expand Eq. (55) to ﬁnd
X = PyMι = P(ˆa · ι′
T + ˆb′X + ˆε)Mι = Pˆb′X + P ˆεMι,
(56)
where we have used the fact that ι′
TMι = 0 and that X is mean zero by construction. For
equality to hold over arbitrary values of X, the model must thus satisfy the consistency
conditions
Pˆb′ = IK,
and
P ˆεMι = 0.
(57)
We ﬁnd that P ˆεMι is extremely close to zero because the yield ﬁtting error ˆε is tiny,
as shown in Table 2. Moreover, the condition Pˆb′ = IK is satisﬁed to a high degree of
precision in the ﬁve-factor speciﬁcation of the model.
We reach this conclusion using the following Monte Carlo procedure. Because their
standard errors do not have a simple closed form, we compute bootstrapped distributions
of the recursive pricing parameters Bn. We construct the bootstrap by saving the residuals
ˆv and ˆe from the three-step regression estimation of the model parameters as well as
the residuals from the regression of the one-month T-bill on the pricing factors.
We
resample all three sets of residuals using the same random time indexation to obtain
an artiﬁcial sample of pricing factors and log excess holding period returns. Based on
these, we reestimate the model parameters using the three-step regression approach and
40

compute recursive pricing parameters Bn from Eq.
(26).
We repeat this procedure
one thousand times.
We ﬁnd that the identity matrix is well within the 1 standard
deviation conﬁdence interval around the mean of the empirical distribution of Pˆb′. To
illustrate this graphically, Fig. 11 plots the ﬁve principal components used as pricing
factors along with the bootstrapped 95% conﬁdence interval of the quantity Pˆb′X. As
the plots show, these distributions are extremely tight. The principal components are
visually almost indistinguishable from their model-implied 95% conﬁdence intervals. The
sampling error of the principal components is comparable in magnitude to the error that
arises due to ﬁtting zero coupon curves to actual bond data. We, therefore, believe that
the inconsistency that is implied by treating pricing factors as observed is numerically
negligible. These results suggest that deviations from Eq. (56) in the model are fully
explained by observation error in yields and excess returns.
5.
Conclusion
We outline an empirical approach to the estimation of dynamic term structure models.
Our approach is computationally fast, gives rise to small pricing errors, and provides
asymptotic standard errors for the model parameters of interest. Our method can be
used for applications with observable factors and allows for unspanned factors.
Our empirical analysis uncovers a number of new results and revisits certain controversies.
First of all, we show in speciﬁcation tests that the ﬁrst three principal components of
Treasury yields are not suﬃcient to span the cross section of Treasury returns.
We,
therefore, study a baseline speciﬁcation that uses the ﬁrst ﬁve principal components as
pricing factors.
Second, we show that the ﬁve-factor model gives rise to similar risk
premiums and pricing kernel dynamics as a speciﬁcation with three principal components
and the Cochrane and Piazzesi (2008) forecasting factor. In both speciﬁcations, we ﬁnd
that practically all of the time variation in risk premiums is associated with level risk.
41

However, the dynamics of the risk premium are mainly explained by the second and ﬁfth
principal component in the ﬁve-factor model and by the CP factor in the four-factor
model. Nevertheless, we reject the restriction that the CP factor inﬂuences only the price
of risk of the level shock and ﬁnd that it signiﬁcantly prices other sources of risk as well.
For both the ﬁve-factor and the four-factor speciﬁcations, we ﬁnd that slope risk is not
priced. When comparing the two models based on out-of-sample predictions, we ﬁnd that
the ﬁve-factor model outperforms the four-factor model. We, therefore, designate it as
our preferred speciﬁcation.
We also allow for certain factors to be unspanned and provide asymptotic standard
errors in this case. Once we add unspanned macroeconomic factors to a model with the
ﬁrst three principal components as pricing factors, we ﬁnd that slope risk is signiﬁcantly
time varying as a function of a real activity indicator. This result suggests that there is
time variation in the pricing kernel that is not spanned by the yield curve.
Our estimation method can be easily adapted and extended, as it solely relies on
linear regressions. We present several examples of such extensions in the paper. First,
we demonstrate that aﬃne term structure models can be estimated even if zero coupon
yields are not available. We estimate such a model by using ﬁve principal components of
coupon bearing yields to price the cross section of maturity sorted returns. The resulting
zero coupon yield curve is very similar to the Fama and Bliss discount curve, even though
the estimation methods are vastly diﬀerent. We furthermore present estimation results
at the daily frequency, which are readily computed due to the ease of our estimation
method. We leave it to future work to adapt the model to further applications, such as
the estimation of inﬂation risk premiums, or to credit risk models.
42

Appendix
A.1. Asymptotic variance: no unspanned factors
Here we derive explicit expressions for VΛ, Vβ and CΛ,β given in Eq. (19) and the remaining variances
and covariances required for the minimum distance estimator of Subsection 4.2. Before proceeding, we
require some deﬁnitions. Let f = [a c] and deﬁne the NK × N matrix Aβ as Aβ = diag(β(1), . . . , β(N)).
Also, deﬁne Υzz = plimT →∞
 Z−Z′
−

T

and Υxx = plimT →∞
 X−X′
−

T

.
For a m × n matrix A
the mn × mn commutation matrix κm,n satisﬁes vec (A′) = κm,nvec (A). For a symmetric n × n matrix
A, the n2 × (n (n + 1)/ 2) duplication matrix Gn satisﬁes vec (A) = Gnvech (A). Finally, denote the
Moore-Penrose inverse of Gn by G+
n .
We ﬁrst focus on VΛ. We could decompose the estimator as
√
T ˆΛ = T1 + T2 + T3,
(58)
where
T1 =
√
T

ˆβ ˆβ
′−1 ˆβ

rx + 1
2
 B⋆vec (Σ) + σ2ιN

ι′
T

M ˆV Z′
−
 Z−M ˆV Z′
−
−1 ,
(59)
T2 = 1
2 ·

ˆβ ˆβ
′−1 ˆβ
h√
T

ˆB⋆vec

ˆΣ

−B⋆vec (Σ)
i
ϱ′
1,
(60)
and
T3 = 1
2 ·

ˆβ ˆβ
′−1 ˆβ
h√
T
 ˆσ2 −σ2i
ιNϱ′
1.
(61)
Let us ﬁrst consider T1. We could further decompose T1 as
T1 = T1,1 + T1,2 + T1,3 + T1,4 + T1,5,
(62)
where
T1,1 =
√
TΛ,
(63)
T1,2 =
√
TV M ˆV Z′
−
 Z−M ˆV Z′
−
−1 ,
(64)
T1,3 =
√
T

ˆβ ˆβ
′−1 ˆβEM ˆV Z′
−
 Z−M ˆV Z′
−
−1 ,
(65)
T1,4 = −
√
T

ˆβ ˆβ
′−1 ˆβ

ˆβ −β
′
Λ,
(66)
and
T1,5 = −
√
T

ˆβ ˆβ
′−1 ˆβ

ˆβ −β
′
V M ˆV Z′
−
 Z−M ˆV Z′
−
−1 .
(67)
T1,1 is already simpliﬁed.
The properties of T1,2 depend on whether the assumption that µ = 0 is
imposed. When the assumption is not imposed, then M ˆV Z′
−= Z′
−and
T1,2,µ =

V Z′
−
 √
T

Υ−1
zz + op (1) .
(68)
When the assumption that µ = 0 is imposed, we have
T1,2,0 =
h
0K×1

V X′
−
 √
T
i
Υ−1
zz + op (1) .
(69)
43

This follows because

V M ˆV Z′
−
 √
T

=

V Z′
−
 √
T

−

V ˆV ′.
T
 
ˆV ˆV ′.
T
−1 
ˆV Z′
−
. √
T

(70)
=
h
0K×1

V X′
−
 √
T
i
+ op (1)
(71)
and
 Z−M ˆV Z′
−

T

=
 ZZ′
−

T

−

Z ˆV ′.
T
 
ˆV ˆV ′.
T
−1 
ˆV Z′
−
.
T

(72)
= Υzz + op (1) .
(73)
Next,
T1,3 =

ˆβ ˆβ
′−1 ˆβ

EM ˆV Z′
−
 √
T
  Z−M ˆV Z′
−

T
−1 =
 ββ′−1 β
h√
T

ˆf −f
i
+ op (1) ,
(74)
by our assumptions. Similarly,
T1,4 = −
√
T

ˆβ ˆβ
′−1 ˆβ

ˆβ −β
′
Λ = −
 ββ′−1 β
h√
T

ˆβ −β
i′
Λ + op (1) .
(75)
Finally, it is straightforward to show that T1,5 = op (1).
We now consider T2. First, note that
√
T

ˆB⋆vec

ˆΣ

−B⋆vec (Σ)

(76)
=
√
T

ˆB⋆vec

ˆΣ

−ˆB⋆vec (Σ) + ˆB⋆vec (Σ) −B⋆vec (Σ)

,
(77)
= B⋆√
T (vec (V V ′/ T) −vec (Σ))

+
√
T

ˆB⋆−B⋆
vec (Σ) + op (1) ,
(78)
because ˆV ˆV ′/T = V V ′/ T + Op
 T −1
under our assumptions. Thus,
T2 = 1
2 ·

ˆβ ˆβ
′−1 ˆβ
h√
T

ˆB⋆vec

ˆΣ

−B⋆vec (Σ)
i
ϱ′
1,
(79)
= 1
2 ·
 ββ′−1 β
h√
T

ˆB⋆vec

ˆΣ

−B⋆vec (Σ)
i
ϱ′
1 + op (1) ,
(80)
= T2,1 + T2,2 + op (1) ,
(81)
where
T2,1 = 1
2 ·
 ββ′−1 β
h√
T

ˆB⋆−B⋆
vec (Σ)
i
ϱ′
1,
(82)
and
T2,2 = 1
2 ·
 ββ′−1 βB⋆√
T (vec (V V ′/ T) −vec (Σ))

ϱ′
1.
(83)
The ith element of the interior matrix of T2,1 is
√
T

ˆβ(i)′ ˆΣˆβ(i) −β(i)′Σβ(i)
= 2
√
Tβ(i)′Σ

ˆβ(i) −β(i)
+ op (1) .
(84)
Thus,
√
T

ˆB⋆−B⋆
vec (Σ) = 2A′
β (IN ⊗Σ) vec
√
T

ˆβ −β

+ op (1)
(85)
and
T2,1 =
 ββ′−1 βA′
β (IN ⊗Σ) vec
√
T

ˆβ −β

ϱ′
1 + op (1) .
(86)
44

T2,2 does not require any further simpliﬁcation.
Finally, consider T3.
Because ˆE ˆE′/T = EE′/ T +
Op
 T −1
,
T3 = 1
2 ·

ˆβ ˆβ
′−1 ˆβ
h√
T
 ˆσ2 −σ2i
ιNϱ′
1
(87)
= 1
2 ·
 ββ′−1 β
h√
T
 ˆσ2 −σ2i
ιNϱ′
1 + op (1)
(88)
= 1
2 ·
 ββ′−1 β
h√
T
 tr (EE′)/ NT −σ2i
ιNϱ′
1 + op (1) .
(89)
Combining these results, we have
√
T

vec

ˆΛ

−vec (Λ)

= vec (T1,2 + T1,3 + T1,4 + T2,1 + T2,2 + T3) + op (1) ,
(90)
where
vec (T1,2,µ) =
 Υ−1
zz ⊗IK

vec

V Z′
−
 √
T

+ op (1) ,
(91)
vec (T1,2,0) =
 Υ−1
zz ⊗IK

vec
h
0K×1

V X′
−/
√
T
i
+ op (1) ,
(92)
vec (T1,3) =

IK+1 ⊗
 ββ′−1 β

vec
√
T

ˆf −f

+ op (1) ,
(93)
vec (T1,4) = −

Λ′ ⊗
 ββ′−1 β

κK,Nvec
√
T

ˆβ −β

+ op (1) ,
(94)
vec (T2,1) =

ϱ1 ⊗
 ββ′−1 βA′
β (IN ⊗Σ)

vec
√
T

ˆβ −β

+ op (1) ,
(95)
vec (T2,2) = 1
2 ·

ϱ1 ⊗
 ββ′−1 βB⋆ h√
Tvec ((V V ′/ T) −Σ)
i
+ op (1) ,
(96)
and
vec (T3) = 1
2

ϱ1 ⊗
 ββ′−1 β

ιN ·
√
T
 tr (EE′)/ NT −σ2
+ op (1) .
(97)
Note next that under our assumptions vec

V Z′
−
 √
T

→d N (0, Υzz ⊗Σ),
√
Tvec ((V V ′/ T) −Σ) →d
N (0, (IK2 + κK,K) (Σ ⊗Σ)), and
√
T
 tr (EE′)/ NT −σ2
→d N
 0, 2σ4
. These are all asymptotically
independent of


vec
√
T

ˆf −f

vec
√
T

ˆβ −β
′

→d N

0, σ2 ·
Υ−1
zz
0
0
Σ−1

⊗IN

,
(98)
because
plimT →∞
 ˜Z ˜Z′
T
!
=
Υzz
0
0
Σ

.
(99)
Thus, the only asymptotic covariance term we need to consider is between T1,4 and T2,1, which implies
that
√
Tvec

ˆΛ −Λ

→d N (0, VΛ), where VΛ = VΛ,T + CΛ,T + C′
Λ,T ,
CΛ,T = asycovT →∞(T1,4, T2,1) ,
(100)
= −

Λ′ ⊗
 ββ′−1 β

κK,N

σ2 ·
 IN ⊗Σ−1 
ϱ1 ⊗
 ββ′−1 βA′
β (IN ⊗Σ)
′
,
(101)
and VΛ,T = VΛ,T ,1 + VΛ,T ,2 + VΛ,T ,3 + VΛ,T ,4 + VΛ,T ,5 + VΛ,T ,6. If µ = 0 is imposed, then
VΛ,T ,1 = asyvarT →∞(T1,2,0) =
 Υ−1
zz ⊗IK
 
0
01×K
0K×1
Υxx

⊗Σ
  Υ−1
zz ⊗IK
′
(102)
45

and otherwise
VΛ,T ,1 = asyvarT →∞(T1,2,µ) =
 Υ−1
zz ⊗IK

(Υzz ⊗Σ)
 Υ−1
zz ⊗IK
′ =
 Υ−1
zz ⊗Σ

.
(103)
The other terms are
VΛ,T ,2 = asyvarT →∞(T1,3) = σ2 ·

Υ−1
zz ⊗
 ββ′−1
,
(104)
VΛ,T ,3 = asyvarT →∞(T1,4) = σ2 ·

Λ′Σ−1Λ ⊗
 ββ′−1
,
(105)
VΛ,T ,4 = asyvarT →∞(T2,1) = σ2 ·

ϱ1ϱ′
1 ⊗
 ββ′−1 βA′
β (IN ⊗Σ) Aββ′  ββ′−1
,
(106)
VΛ,T ,5 = asyvarT →∞(T2,2)
(107)
= 1
4 ·

ϱ1ϱ′
1 ⊗
 ββ′−1 βB⋆(IK2 + κK,K) (Σ ⊗Σ) B⋆′β′  ββ′−1
,
(108)
and
VΛ,T ,6 = asyvarT →∞(T3) = σ4
2 ·

ϱ1ϱ′
1 ⊗
 ββ′−1 βιNι′
Nβ′  ββ′−1
.
(109)
It is clear from Eq. (98) that Vβ = σ2 ·
 IN ⊗Σ−1
. Finally, we need only calculate CΛ,β. From our
above results we have that the only asymptotic covariance term between ˆΛ and ˆβ comes from T1,4 and
T2,1. Thus,
asycovT →∞

vec (T1,4) , vec

ˆβ

= −

Λ′ ⊗
 ββ′−1 β

κK,N

σ2 ·
 IN ⊗Σ−1
,
(110)
= −σ2 · κK+1,K
 ββ′−1 β ⊗Λ′Σ−1
,
(111)
and
asycovT →∞

vec (T2,1) , vec

ˆβ

=

ϱ1 ⊗
 ββ′−1 βA′
β (IN ⊗Σ)
 
σ2 ·
 IN ⊗Σ−1
,
(112)
= σ2 ·

ϱ1 ⊗
 ββ′−1 βA′
β

.
(113)
Thus,
CΛ,β = asycovT →∞

vec

ˆΛ

, vec

ˆβ

,
(114)
= −σ2 · κK+1,K
 ββ′−1 β ⊗Λ′Σ−1
+ σ2 ·

ϱ1 ⊗
 ββ′−1 βA′
β

.
(115)
Finally, we provide the remaining asymptotic variances and covariances necessary to construct Vθ from
Section 4.2. Let CΛ,σ2 and Vσ2 be the asymptotic covariance between ˆΛ and ˆσ2 and the asymptotic
variance of ˆσ2, respectively, and similarly for the other parameters. Cβ,Ψ, Cβ,σ2, Cβ,Σ, CΨ,σ2, CΨ,Σ, and
Cσ2,Σ are all equal to the zero matrix of the appropriate dimensions. Because we impose the assumption
that µ = 0 when estimating the VAR but not when we calculate the asymptotic variance of ˆΛ, then
√
Tvec

ˆΦ −Φ

=
 Υ−1
xx ⊗IK

vec

V X′
−
 √
T

+ op (1)
(116)
and
CΛ,Φ = asycovT →∞

vec

ˆΛ

, vec

ˆΦ

=
 Υ−1
zz ⊗IK

[(Υzz ⊗Σ)]2
 Υ−1
xx ⊗IK

,
(117)
where [(Υzz ⊗Σ)]2 is the K (K + 1)×K2 sub-matrix formed by extracting the last K2 columns from the
46

matrix (Υzz ⊗Σ). Next, we have that
CΛ,σ2 = asycovT →∞

vec

ˆΛ

, vec
 ˆσ2
= σ4 
ϱ1 ⊗
 ββ′−1 β

ιN,
(118)
and
CΛ,Σ = asycovT →∞

vec

ˆΛ

, vech

ˆΣ

(119)
= 1
2 ·

ϱ1 ⊗
 ββ′−1 βB⋆
GKG+
K (IK2 + κK,K) (Σ ⊗Σ)
 G+
K
′
(120)
=

ϱ1 ⊗
 ββ′−1 βB⋆
GKG+
K (Σ ⊗Σ)
 G+
K
′ ,
(121)
by properties of the duplication matrix. Because the assumption that µ = 0 is imposed when we estimate
the VAR, then, VΦ,0 =
 Υ−1
xx ⊗Σ

. As given above, Vσ2 = 2σ4 and by properties of the duplication
matrix, VΣ = 2G+
K (Σ ⊗Σ)
 G+
K
′.
A.2. Asymptotic variance: unspanned factors
Here we will derive explicit expressions for Vss
Λ , Vsu
λ1 and Css,su
Λ,λ1 given in Eq. (49). In the unspanned
case, we can write the equation as
rx = fsZs
−+ β′
sXs + E,
fs = [as cs] ,
(122)
where Zs
−=

ιT
Xs′
−
′. Under our assumptions, the OLS estimators of fs and β′
s satisfy
√
T


vec

ˆfs −fs

vec

ˆβs −βs
′


d
−→N
 0, Vs
fβ

,
(123)
where
Vs
fβ = σ2 ·

plimT →∞

˜Zs ˜Zs′.
T
−1
⊗IN

,
˜Zs =

Zs′
−Xs′′ .
(124)
Our estimator is
ˆΨ⋆
ss = −

ˆβs ˆβ′
s
−1 ˆβs

rx + 1
2

ˆB⋆svec

ˆΣss

+ ˆσ2ιN

ι′
T

M s
xZs′
−
 Zs
−M s
xZs′
−
−1 ,
(125)
which could be decomposed as
√
T ˆΨ⋆
ss = T s
1 + T s
2 ,
(126)
where
T s
1 = −
√
T

ˆβs ˆβ′
s
−1 ˆβs

rx + 1
2
 B⋆svec (Σss) + σ2ιN

ι′
T

M s
xZs′
−
 Zs
−M s
xZs′
−
−1
(127)
and
T s
2 = −
√
T

ˆβs ˆβ′
s
−1 ˆβs
1
2

ˆB⋆svec

ˆΣss

−B⋆svec (Σss) +
 ˆσ2 −σ2
ιN

ϱs′
1 ,
(128)
where ϱs
1 = (1, 0, . . . , 0)′ is (Ks + 1) × 1. Then, T s
1 could be further decomposed as
T s
1 = T s
1,1 + T s
1,2 + T s
1,3,
(129)
where
T s
1,1 =
√
TΨ⋆
ss,
(130)
47

T s
1,2 = −
√
T

ˆβs ˆβ′
s
−1 ˆβs

ˆβs −βs
′
Ψ⋆
ss,
(131)
and
T s
1,3 = −
√
T

ˆβs ˆβ′
s
−1 ˆβsEM s
xZs′
−
 Zs
−M s
xZs′
−
−1 .
(132)
T s
1,1 requires no further simpliﬁcation. Next,
T s
1,2 = −
√
T

ˆβs ˆβ′
s
−1 ˆβs

ˆβs −βs
′
Ψ⋆
ss = −(βsβ′
s)−1 βs
h√
T

ˆβs −βs
i′
Ψ⋆
ss + op (1) ,
(133)
and
T s
1,3 = −
√
T

ˆβs ˆβ′
s
−1 ˆβsEM s
xZs′
−
 Zs
−M s
xZs′
−
−1 = −(βsβ′
s)−1 βs
h√
T

ˆfs −fs
i
+ op (1) .
(134)
T s
2 could be decomposed as
T s
2 = T s
2,1 + T s
2,2 + op (1) ,
(135)
where
T s
2,1 = −1
2 · (βsβ′
s)−1 βs
√
T

ˆB⋆svec

ˆΣss

−B⋆svec (Σss)

ϱs′
1
(136)
and
T s
2,2 = −1
2 · (βsβ′
s)−1 βs
√
T
 ˆσ2 −σ2
ιN

ϱs′
1 .
(137)
Similar to the derivation in Subsection 5, we can show that T s
2,1 = T s
2,1,1 + T s
2,1,2 + op (1), where
T s
2,1,1 = (βsβ′
s)−1 βsA′
βs (IN ⊗Σss) vec
√
T

ˆβs −βs

ϱs′
1 ,
(138)
T s
2,1,2 = −1
2 · (βsβ′
s)−1 βsB⋆s h√
T (vec (V sV s′/ T) −vec (Σss))
i
ϱs′
1 ,
(139)
and
T s
2,2 = −1
2 · (βsβ′
s)−1 βs
√
T
 tr (EE′/ (NT)) −σ2
ϱs′
1 + op (1) .
(140)
Putting all these results together, we have
√
Tvec

ˆΨ⋆
ss −Ψ⋆
ss

= vec
 T s
1,2 + T s
1,3 + T s
2,1,1 + T s
2,1,2 + T s
2,2

,
(141)
where
vec
 T s
1,2

=−

Ψ⋆′
ss ⊗(βsβ′
s)−1 βs

κKs,Nvec
√
T

ˆβs −βs

+ op (1) ,
(142)
vec
 T s
1,3

=−

I(Ks+1) ⊗(βsβ′
s)−1 βs

vec
√
T

ˆfs −fs

+ op (1) ,
(143)
vec
 T s
2,1,1

=−

ϱs
1 ⊗(βsβ′
s)−1 βsA′
βs (IN ⊗Σss)

vec
√
T

ˆβs −βs

+ op (1) ,
(144)
vec
 T s
2,1,2

=−1
2 ·

ϱs
1 ⊗(βsβ′
s)−1 βsB⋆s h√
T (vec (V sV s′/ T) −vec (Σss))
i
+ op (1) ,
(145)
and
vec
 T s
2,2

=−1
2 ·

ϱs
1 ⊗(βsβ′
s)−1 βs

ιN ·
√
T
 tr (EE′/ (NT)) −σ2
+ op (1) .
(146)
Then,
√
Tvec

ˆΨ⋆
ss −Ψ⋆
ss

→d N
 0, VΨ⋆ss

,
(147)
where
VΨ⋆
ss =
X5
j=1 VΨ⋆ss,T ,j +CΨ⋆ss,T ,1 +
 CΨ⋆ss,T ,1
′ +CΨ⋆ss,T ,2 +
 CΨ⋆ss,T ,2
′ +CΨ⋆ss,T ,3 +
 CΨ⋆ss,,T ,3
′ . (148)
48

Let us partition Vs
fβ conformably
Vs
fβ =
Vs
fβ,11
Vs
fβ,12
Vs′
fβ,12
Vs
fβ,22

,
(149)
and
VΨ⋆ss,T ,1 =asyvarT →∞
 T s
1,2

=

Ψ⋆′
ss ⊗(βsβ′
s)−1 βs

Vs
fβ,22

Ψ⋆′
ss ⊗(βsβ′
s)−1 βs
′
,
(150)
VΨ⋆ss,T ,2 =asyvarT →∞
 T s
1,3

,
(151)
=

I(Ks+1) ⊗(βsβ′
s)−1 βs

Vs
fβ,11

I(Ks+1) ⊗(βsβ′
s)−1 βs
′
,
(152)
VΨ⋆ss,T ,3 =asyvarT →∞
 T s
2,1,1

,
(153)
=

ϱs
1 ⊗(βsβ′
s)−1 βsA′
βs (IN ⊗Σss)

κN,KsVs
fβ,22κ′
N,Ks×
(154)

ϱs
1 ⊗(βsβ′
s)−1 βsA′
βs (IN ⊗Σss)
′
,
(155)
VΨ⋆ss,T ,4 =asyvarT →∞
 T s
2,1,2

,
(156)
= 1
4 ·

ϱs
1ϱs′
1 ⊗(βsβ′
s)−1 βsB⋆s  IK2s + κKs,Ks

(Σss ⊗Σss) B⋆s′β′
s (βsβ′
s)−1
,
(157)
VΨ⋆ss,T ,5 =asyvarT →∞
 T s
2,2

= σ4
2 ·

ϱs
1ϱs′
1 ⊗(βsβ′
s)−1 βsιNι′
Nβ′
s (βsβ′
s)−1
,
(158)
and
CΨ⋆ss,T ,1 =asycovT →∞
 T s
1,2, T s
1,3

,
(159)
=

Ψ⋆′
ss ⊗(βsβ′
s)−1 βs

Vs′
fβ,12

I(Ks+1) ⊗(βsβ′
s)−1 βs
′
,
(160)
CΨ⋆ss,T ,2 =asycovT →∞
 T s
1,2, T s
2,1,1

,
(161)
=

Ψ⋆′
ss ⊗(βsβ′
s)−1 βs

Vs
fβ,22κ′
N,Ks

ϱs
1 ⊗(βsβ′
s)−1 βsA′
βs (IN ⊗Σss)
′
,
(162)
CΨ⋆ss,T ,3 =asycovT →∞
 T s
1,3, T s
2,1,1

,
(163)
=

I(Ks+1) ⊗(βsβ′
s)−1 βs

Vs
fβ,12κ′
N,Ks

ϱs
1 ⊗(βsβ′
s)−1 βsA′
βs (IN ⊗Σss)
′
.
(164)
Recall that our estimators are ˆΛss = ˆΨss −ˆΨ⋆
ss and ˆλsu
1
= ˆΦsu. Under our assumptions, ˆΨ⋆
ss and ˆΨ are
asymptotically independent and so
asyvarT →∞

vec

ˆΛss

vec

ˆλsu
1



(165)
=


VΨ⋆ss + asyvarT →∞vec

ˆΨss

−asycovT →∞

vec

ˆΨss

, vec

ˆΦsu

−asycovT →∞

vec

ˆΦsu

, vec

ˆΨss

asyvarT →∞vec

ˆΦsu


.
(166)
Thus we require only VΨ = asyvarT →∞(ˆΨ) =
 Υ−1
zz ⊗Σ

.
When µ = 0 is imposed, then (ˆΛss, ˆλsu
1 )
should be adjusted accordingly and VΦ,0 =
 Υ−1
xx ⊗Σ

should be used for the analogous result to Eq.
(166).
49

Table 1 Identiﬁcation Tests
This table reports the results of the identiﬁcation tests described in Subsection 3.2. rkk−1 is the Anderson (1951)
statistic for the hypothesis that the rank of
β in a K
factor model is K −1 or smaller. Wβ is the Wald statistic for
the hypothesis that the last row of β equals zero. These test statistics follow χ2 (N −K + 1) and χ2 (N) distributions,
respectively. Corresponding p-values are reported in parentheses. The four panels present alternative models estimated
using diﬀerent numbers of yield principal components as pricing factors. Panel A reports test results for speciﬁcations using
Gurkaynak, Sack and Wright (2007, GSW) yields to extract principal components. Panel B is based on a combination
of Fama and Bliss and GSW yields, as in Duﬀee (2010). Panel C uses Federal Reserve H.15 yields. Panel D uses Center
for Research in Security Prices (CRSP) constant-maturity Treasury yields. Speciﬁcations in the left column are estimated
using excess returns from GSW zero coupon yields. Speciﬁcations in the right column are estimated using excess returns
on Fama maturity-sorted portfolios.
GSW returns
CRSP Fama returns
Number of Factors
rkk−1
Wβ
rkk−1
Wβ
Panel A: GSW yields
K = 3
577.580
11216.622
333.092
2176.506
(p-value)
(0.000)
(0.000)
(0.000)
(0.000)
K = 4
629.077
4643.528
104.281
231.140
(p-value)
(0.000)
(0.000)
(0.000)
(0.000)
K = 5
885.261
21831.991
34.991
25.139
(p-value)
(0.000)
(0.000)
(0.000)
(0.009)
Panel B: Fama and Bliss yields + GSW six- and ten-year
K = 3
228.202
9105.729
103.634
2090.322
(p-value)
(0.000)
(0.000)
(0.000)
(0.000)
K = 4
155.195
6194.862
86.344
889.096
(p-value)
(0.000)
(0.000)
(0.000)
(0.000)
K = 5
34.348
166.716
32.952
86.717
(p-value)
(0.000)
(0.000)
(0.000)
(0.000)
Panel C: H.15 yields
K = 3
242.768
384.954
189.816
454.848
(p-value)
(0.000)
(0.000)
(0.000)
(0.000)
K = 4
61.473
279.181
101.817
44.675
(p-value)
(0.000)
(0.000)
(0.000)
(0.000)
K = 5
18.845
55.866
63.757
68.442
(p-value)
(0.009)
(0.000)
(0.000)
(0.000)
Panel D: CRSP constant-maturity yields
K = 3
164.237
1154.031
68.376
1328.303
(p-value)
(0.000)
(0.000)
(0.000)
(0.000)
K = 4
152.737
462.968
61.836
728.340
(p-value)
(0.000)
(0.000)
(0.000)
(0.000)
K = 5
22.550
72.438
23.945
188.009
(p-value)
(0.002)
(0.000)
(0.001)
(0.000)
52

Table 2 Five-factor model: ﬁt diagnostics
This table summarizes the time series properties of the pricing errors implied by the ﬁve-factor speciﬁcation. The
sample period is 1987:01–2011:12. Reported are the sample mean, standard deviation, skewness, and kurtosis of the errors;
ρ(1), ρ(6) denote their autocorrelation coeﬃcients of order one and six. Panel A reports properties of the yield pricing errors
ˆu, and Panel B reports properties of the return pricing errors ˆe. n = 12, . . . , 120 denotes the maturity in months.
Summary Statistics
n = 12
n = 24
n = 36
n = 60
n = 84
n = 120
Panel A: Yield pricing errors
mean
-0.001
0.000
-0.001
-0.003
-0.003
-0.004
standard deviation
0.004
0.006
0.006
0.004
0.004
0.008
skewness
-0.342
0.420
-0.086
-0.069
0.305
-0.133
kurtosis
3.245
2.932
2.414
2.205
2.545
2.726
ρ(1)
0.793
0.803
0.879
0.936
0.853
0.818
ρ(6)
0.565
0.526
0.745
0.718
0.657
0.442
Panel B: Return pricing errors
mean
0.000
-0.002
-0.007
-0.007
-0.003
-0.026
standard deviation
0.081
0.092
0.151
0.132
0.179
0.617
skewness
4.183
1.000
3.016
1.310
0.396
0.248
kurtosis
46.489
9.708
40.674
12.555
5.685
7.981
ρ(1)
-0.001
0.175
-0.140
0.001
-0.162
-0.157
ρ(6)
0.104
0.098
0.083
-0.014
0.015
0.012
Table 3 Five-factor model: market prices of risk
This table summarizes the estimates of the market price of risk parameters λ0 and λ1 for the ﬁve factor speciﬁcation.
t-statistics are reported in parentheses. The standard errors have been computed according to the formulas from Subsection
2.3. Wald statistics for tests of the rows of Λ and of λ1 being diﬀerent from zero are reported along each row, with the
corresponding p-values in parentheses below. PC1, . . . , PC5 denote the ﬁrst through ﬁfth principal components of Treasury
yields. Bolded coeﬃcients represent signiﬁcance at the 5% level.
Factor
λ0
λ1.1
λ1.2
λ1.3
λ1.4
λ1.5
WΛ
Wλ1
PC1
-0.019
-0.003
-0.016
-0.005
0.012
0.030
30.367
23.705
(t-statistic)
(-2.566)
(-0.443)
(-2.160)
(-0.648)
(1.605)
(3.987)
(0.000)
(0.000)
PC2
0.013
0.027
-0.011
-0.003
-0.011
0.015
7.097
6.167
(t-statistic)
(0.951)
(1.914)
(-0.818)
(-0.213)
(-0.792)
(1.077)
(0.312)
(0.290)
PC3
-0.030
-0.077
-0.001
-0.093
-0.132
-0.056
37.170
36.277
(t-statistic)
(-0.951)
(-2.466)
(-0.029)
(-2.987)
(-4.244)
(-1.783)
(0.000)
(0.000)
PC4
0.042
0.064
-0.007
0.015
-0.058
-0.086
10.444
9.374
(t-statistic)
(1.062)
(1.594)
(-0.189)
(0.367)
(-1.461)
(-2.147)
(0.107)
(0.095)
PC5
0.005
-0.105
0.012
-0.004
-0.073
-0.324
45.691
45.688
(t-statistic)
(0.097)
(-2.028)
(0.243)
(-0.070)
(-1.431)
(-6.287)
(0.000)
(0.000)
53

Table 4 Four-factor model: ﬁt diagnostics
This table summarizes the time series properties of the pricing errors implied by the four factor speciﬁcation. The
sample period is 1987:01–2011:12. Reported are the sample mean, standard deviation, skewness, and kurtosis of the errors;
ρ(1), ρ(6) denote their autocorrelation coeﬃcients of order one and six. Panel A reports properties of the yield pricing errors
ˆu, and Panel B reports properties of the return pricing errors ˆe. n = 12, . . . , 120 denotes the maturity in months.
Summary Statistics
n = 12
n = 24
n = 36
n = 60
n = 84
n = 120
Panel A: Yield pricing errors
mean
0.028
0.010
-0.013
-0.029
-0.018
0.015
standard deviation
0.048
0.030
0.026
0.029
0.021
0.028
skewness
0.653
0.179
-0.358
-0.995
-0.399
0.662
kurtosis
6.540
2.638
2.842
4.282
3.605
3.718
ρ(1)
0.769
0.843
0.912
0.858
0.877
0.748
ρ(6)
0.612
0.532
0.780
0.606
0.630
0.478
Panel B: Return pricing errors
mean
0.025
-0.041
-0.074
-0.037
0.024
0.142
standard deviation
0.539
0.509
0.382
0.896
0.924
2.445
skewness
2.042
0.384
0.566
0.126
0.592
-0.308
kurtosis
18.013
5.534
5.386
4.411
5.144
6.829
ρ(1)
-0.073
-0.055
0.027
-0.147
-0.128
-0.337
ρ(6)
0.228
0.142
0.171
0.057
0.072
-0.017
Table 5 Four-factor model: market prices of risk
This table summarizes the estimates of the market price of risk parameters λ0 and λ1 for the four factor speciﬁcation.
t-statistics are reported in parentheses. The standard errors have been computed according to the formulas from Subsection
2.3. Wald statistics for tests of the rows of Λ and of λ1 being diﬀerent from zero are reported along each row, with the
corresponding p-values in parentheses below. PC1, . . . , PC5 denote the ﬁrst through ﬁfth principal components of Treasury
yields. Bolded coeﬃcients represent signiﬁcance at the 5% level.
Factor
λ0
λ1.1
λ1.2
λ1.3
λ1.4
WΛ
Wλ1
PC1
-0.019
-0.001
0.003
0.003
-0.043
37.239
30.393
(t-statistic)
(-2.597)
(-0.195)
(0.325)
(0.420)
(-5.002)
(0.000)
(0.000)
PC2
0.012
0.026
0.000
0.002
-0.025
6.746
5.981
(t-statistic)
(0.865)
(1.801)
(0.005)
(0.113)
(-1.524)
(0.240)
(0.201)
PC3
-0.015
-0.063
-0.051
-0.109
0.111
18.326
18.110
(t-statistic)
(-0.454)
(-1.862)
(-1.366)
(-3.186)
(2.861)
(0.003)
(0.001)
CP
-0.087
0.019
0.098
-0.010
-0.291
27.851
25.546
(t-statistic)
(-1.728)
(0.374)
(1.753)
(-0.188)
(-4.872)
(0.000)
(0.000)
54

Table 6 Macro factor model: market prices of risk
This table summarizes the estimates of the market price of risk parameters λ0 and λ1 for the unspanned macro
speciﬁcation. t-statistics are reported in parentheses. Standard errors have been computed according to the formulas from
Subsection 4.1.
Wald statistics for tests of the rows of Λ and of λ1 being diﬀerent from zero are reported along each
row, with the corresponding p-values in parentheses. PC1, . . . , PC5 denote the ﬁrst through ﬁfth principal components of
Treasury yields. Bolded coeﬃcients represent signiﬁcance at the 5% level.
Factor
λ0
λ1.1
λ1.2
λ1.3
λ1.4
λ1.5
WΛ
Wλ1
PC1
-0.019
-0.028
-0.018
-0.005
-0.022
0.017
15.746
9.423
(t-statistic)
(-2.492)
(-1.719)
(-2.062)
(-0.541)
(-1.360)
(1.835)
(0.015)
(0.093)
PC2
0.010
0.025
-0.028
-0.030
-0.028
-0.057
18.764
18.264
(t-statistic)
(0.700)
(0.850)
(-1.837)
(-1.853)
(-0.975)
(-3.412)
(0.005)
(0.003)
PC3
0.000
-0.093
-0.019
-0.099
-0.057
-0.030
9.972
9.972
(t-statistic)
(0.000)
(-1.373)
(-0.528)
(-2.621)
(-0.865)
(-0.797)
(0.126)
(0.076)
55

1990
1995
2000
2005
2010
−2
0
2
4
6
8
10
Percent
Yield fitting and term premium estimates of maturity n = 24 months
 
 
Observed
Fitted
Term premium
1990
1995
2000
2005
2010
0
1
2
3
4
5
6
7
8
9
10
Percent
Yield fitting and term premium estimates of maturity n = 120 months
 
 
Observed
Fitted
Term premium
1990
1995
2000
2005
2010
−20
−15
−10
−5
0
5
10
15
20
25
Observed and model−implied one−month holding return for n = 24 months
1990
1995
2000
2005
2010
−150
−100
−50
0
50
100
150
Observed and model−implied one−month holding return for n = 120 months
Fig. 1 Five-factor model: observed and model-implied time series
This ﬁgure provides plots of the yields and excess one-month holding returns for the two-year and ten-year maturities
as observed and implied by the ﬁve factor speciﬁcation. The observed yields and returns are plotted by solid lines, and
dashed lines correspond to model-implied yields and returns. Dash-dotted lines show model-implied term premiums in the
upper two charts and expected excess holding period returns in the lower two charts.
56

0
20
40
60
80
100
120
4.2
4.4
4.6
4.8
5
5.2
5.4
5.6
5.8
6
Cross sectional fit, average observed and model−implied yields
Maturity (in months)
Percent
 
 
Observed
Fitted
0
20
40
60
80
100
120
1.7
1.8
1.9
2
2.1
2.2
2.3
2.4
2.5
Unconditional standard deviation of observed and model−implied yields
Maturity (in months)
Percent
 
 
Observed
Fitted
0
20
40
60
80
100
120
−1
−0.5
0
0.5
1
1.5
2
2.5
Yield loadings, model−implied factor loadings
Maturity (in months)
 
 
PC1
PC2
PC3
PC4
PC5
0
20
40
60
80
100
120
−0.5
−0.4
−0.3
−0.2
−0.1
0
0.1
0.2
0.3
0.4
Expected excess return loadings, model−implied return factor loadings
Maturity (in months)
 
 
PC1
PC2
PC3
PC4
PC5
Fig. 2 Five-factor model: cross-sectional diagnostics
This ﬁgure provides graphs exhibiting the cross-sectional ﬁt and interpretation of the factors in the ﬁve factor
speciﬁcation.
The upper two panels plot unconditional means and standard deviations of yields against those implied
by the model. The lower left panel plots the implied yield loadings −1
nBn. These coeﬃcients can be interpreted as the
response of the n-month yield to a contemporaneous shock to the respective factor. The lower right panel plots the expected
return loadings B′
nλ1. These coeﬃcients can be interpreted as the response of the expected one-month excess holding return
on an n-month bond to a contemporaneous shock to the respective factor. PC1, . . . , PC5 denote the ﬁrst through ﬁfth
principal components of Treasury yields.
57

1990
1995
2000
2005
2010
0
1
2
3
4
5
6
Decomposition of pricing kernel variance, five−factor model
 
 
PC1
PC2
PC3
PC4
PC5
1990
1995
2000
2005
2010
0
1
2
3
4
5
6
Decomposition of pricing kernel variance, four−factor model
 
 
PC1
PC2
PC3
CP
1990
1995
2000
2005
2010
−0.015
−0.01
−0.005
0
0.005
0.01
0.015
0.02
0.025
0.03
Decomposition of expected ten−year excess returns, five−factor model
 
 
λ1
λ2
λ3
λ4
λ5
1990
1995
2000
2005
2010
−0.02
−0.01
0
0.01
0.02
0.03
0.04
Decomposition of expected ten−year excess returns, four−factor model
 
 
λ1
λ2
λ3
λ4
Fig. 3 Pricing Kernel Variance Decomposition
This ﬁgure shows decompositions of the conditional volatility of the pricing kernel and the expected excess return
in the four- and ﬁve-factor speciﬁcation for the ten-year Treasury note. The upper two panels decompose λ′
tλt into its K
components. The lower panels decompose expected excess returns, β′ΛZt = (βi1Λ1 + · · · + βiKΛk) Zt, where βij is the
jth element of βi and Λk denotes the kth row of Λ. PC1, . . . , PC5 denote the ﬁrst through ﬁfth principal components of
Treasury yields. CP denotes the Cochrane and Piazzesi (2008) return forecasting factor.
58

0
20
40
60
80
100
120
−0.18
−0.16
−0.14
−0.12
−0.1
−0.08
−0.06
−0.04
−0.02
0
 β versus B for Factor 1
Maturity (in months)
0
20
40
60
80
100
120
−0.05
−0.04
−0.03
−0.02
−0.01
0
0.01
 β versus B for Factor 2
Maturity (in months)
0
20
40
60
80
100
120
−8
−6
−4
−2
0
2
4
x 10
−3
 β versus B for Factor 3
Maturity (in months)
0
20
40
60
80
100
120
−3
−2.5
−2
−1.5
−1
−0.5
0
0.5
1
1.5
x 10
−3
 β versus B for Factor 4
Maturity (in months)
0
20
40
60
80
100
120
−2
−1.5
−1
−0.5
0
0.5
1
x 10
−3
 β versus B for Factor 5
Maturity (in months)
Fig. 4 Regression Coeﬃcients β(n) versus recursive pricing parameters Bn
This ﬁgure provides plots of the coeﬃcients ˆβ(n) from the regression Eq. (15) of log excess holding period returns
on the state variable innovations versus the recursive pricing parameters Bn used to generate ﬁtted yields given in Eq.
(26) for the ﬁve factor speciﬁcation. The diamonds represent the former, and the solid lines correspond to the latter. The
conﬁdence intervals for ˆβ(n) are plotted as shaded bands.
59

1990
1995
2000
2005
2010
−2
0
2
4
6
8
10
Percent
Yield fitting and term premium estimates of maturity n = 24 months
 
 
Observed
Fitted
Term premium
1990
1995
2000
2005
2010
0
1
2
3
4
5
6
7
8
9
10
Percent
Yield fitting and term premium estimates of maturity n = 120 months
 
 
Observed
Fitted
Term premium
1990
1995
2000
2005
2010
−20
−15
−10
−5
0
5
10
15
20
25
Percent
Observed and model−implied one−month holding return, n = 24 months
1990
1995
2000
2005
2010
−150
−100
−50
0
50
100
150
Percent
Observed and model−implied one−month holding return, n = 120 months
Fig. 5 Four-factor model: observed and model-implied time series
This ﬁgure provides plots of the yields and excess one-month holding returns for the two-year and ten-year zero
coupon maturities as observed and implied by the four-factor speciﬁcation. The observed yields and returns are plotted by
solid lines, and dashed lines correspond to model-implied yields and returns. Dash-dotted lines show model-implied term
premiums in the upper two charts and expected excess holding period returns in the lower two charts.
60

0
20
40
60
80
100
120
4.2
4.4
4.6
4.8
5
5.2
5.4
5.6
5.8
6
Cross sectional fit, average observed and model−implied yields
Maturity (in months)
Percent
 
 
Observed
Fitted
0
20
40
60
80
100
120
1.7
1.8
1.9
2
2.1
2.2
2.3
2.4
2.5
Unconditional standard deviation of observed and model−implied yields
Maturity (in months)
Percent
 
 
Observed
Fitted
0
20
40
60
80
100
120
−1
−0.5
0
0.5
1
1.5
2
2.5
Yield loadings, model−implied factor loadings
Maturity (in months)
 
 
PC1
PC2
PC3
CP
0
20
40
60
80
100
120
−0.1
0
0.1
0.2
0.3
0.4
0.5
0.6
0.7
Expected excess return loadings, model−implied return factor loadings
Maturity (in months)
 
 
PC1
PC2
PC3
CP
Fig. 6 Four-factor model: cross-sectional diagnostics
This ﬁgure provides graphs exhibiting the cross-sectional ﬁt and interpretation of the factors in the four factor
speciﬁcation. The upper two panels plot the unconditional means and standard deviations of observed yields against those
implied by the model. The lower left panel plots the implied yield loadings −1
nBn. These coeﬃcients can be interpreted
as the response of the n-month yield to a contemporaneous shock to the respective factor. The lower right panel plots the
expected return loadings B′
nλ1. These coeﬃcients can be interpreted as the response of the expected one-month excess
holding return on an n-month bond to a contemporaneous shock to the respective factor. PC1, . . . , PC5 denote the ﬁrst
through ﬁfth principal components of Treasury yields. CP denotes the Cochrane and Piazzesi (2008) return forecasting
factor.
61

1990
1995
2000
2005
2010
0
0.5
1
1.5
2
2.5
3
3.5
4
4.5
Time
Ten−year term premium comparison
 
 
Five factors
Four factors
PC4, PC5 unspanned
CP unspanned
5
10
15
20
25
30
35
40
45
50
55
60
0
0.2
0.4
0.6
0.8
1
1.2
1.4
1.6
1.8
2
Horizon (months)
Root mean square average short rate forecast error
 
 
Five factors
Four factors
PC4, PC5 unspanned
CP unspanned
Random walk
0
50
100
150
200
250
4
4.5
5
5.5
6
6.5
7
Maturity (in months)
Out−of−sample cross−sectional fit, fitted and model−implied yields for n=1−240 months
 
 
Five factors
Four factors
PC4, PC5 unspanned
CP unspanned
Observed
0
50
100
150
200
250
4
4.5
5
5.5
6
6.5
Maturity (in months)
In−sample cross−sectional fit, fitted and model−implied yields for n=1−240 months
 
 
Five factors
Four factors
PC4, PC5 unspanned
CP unspanned
Observed
Fig. 7 Model Comparison
This ﬁgure shows the model comparison diagnostics discussed in Subsection 3.5. The upper left panel plots the ten-year
Treasury term premium implied by the ﬁve-factor model, the four-factor model, a ﬁve-factor model in which PC4, PC5 are
restricted to be unspanned, and a four-factor model in which the CP factor is restricted to be unspanned. The upper right
panel shows the out-of-sample root mean squared forecast error (RMSE) for average future short rates up to ﬁve years in
the future as implied by the four model speciﬁcations. It also provides the RMSE for a simple random walk model of the
short rate. The lower left panel shows the average yields implied by the four models for maturities up to 20 years, where the
models have been estimated using only maturities up to ten years. The lower right chart shows the average yields implied
by the four models when maturities up to 20 years have been used in the estimation. PC1, . . . , PC5 denote the ﬁrst through
ﬁfth principal components of Treasury yields. CP denotes the Cochrane and Piazzesi (2008) return forecasting factor.
62

1990
1995
2000
2005
2010
0
1
2
3
4
5
6
7
8
9
Annualized percent
Two−year fitted versus two−Year Fama−Bliss
1990
1995
2000
2005
2010
1
2
3
4
5
6
7
8
9
Annualized percent
Five−year fitted versus five−Year Fama−Bliss
1990
1995
2000
2005
2010
−20
−15
−10
−5
0
5
10
15
20
Percent
Observed and model−implied one−month holding return, n = 24 months
1990
1995
2000
2005
2010
−60
−40
−20
0
20
40
60
Percent
Observed and model−implied one−month holding return, n = 60 months
Fig. 8 Fama maturity-sorted portfolio model: observed and model-implied time series
This ﬁgure provides plots of the model-implied yields for the two-year and ﬁve-year maturities from the Fama
maturity-sorted portfolio speciﬁcation detailed in Subsection 3.6. Excess returns on maturity-sorted Fama bond portfolios
are regressed on a set of spanning factors extracted from principal components of Federal Reserve H.15 bond yields. The
top two panels plot the ﬁtted yields from this speciﬁcation against the Fama and Bliss zero coupon yields. The bottom two
panels plot the observed excess returns on Fama maturity-sorted Treasury portfolios (solid lines) against the model-implied
ﬁtted returns (dashed lines).
The dash-dotted lines show model-implied term premiums in the upper two charts and
expected excess holding period returns in the lower two charts.
63

1990
1995
2000
2005
2010
0
0.5
1
1.5
2
2.5
3
Five−factor model, model−implied maximal Sharpe ratio
1990
1995
2000
2005
2010
0
0.5
1
1.5
2
2.5
3
Four−factor model, model−implied maximal Sharpe ratio
1990
1995
2000
2005
2010
0
0.5
1
1.5
2
2.5
3
Five−factor model, PC4 and PC5 unspanned, model−implied maximal Sharpe ratio
1990
1995
2000
2005
2010
0
0.5
1
1.5
2
2.5
3
Unspanned macro factor model, model−implied maximal Sharpe ratio
Fig. 9 Model-implied maximal Sharpe ratios
This ﬁgure provides plots of the time series of the Sharpe ratio diagnostic
p
λ′
tλt as described in Subsection 4.3. The
upper left panel plots the Sharpe ratio for the standard ﬁve factor speciﬁcation and the upper right panel plots the Sharpe
ratio for the four factor speciﬁcation. The lower left panel plots the Sharpe ratio for a speciﬁcation using ﬁve principal
components as factors but with the fourth and ﬁfth principal components estimated as unspanned factors. The lower right
panel plots the Sharpe ratio for the unspanned macro factor speciﬁcation. PC1, . . . , PC5 denote the ﬁrst through ﬁfth
principal components of Treasury yields. CP denotes the Cochrane and Piazzesi (2008) return forecasting factor.
64

January 2009
January 2010
January 2011
January 2012
0
0.2
0.4
0.6
0.8
1
1.2
1.4
Observed and model−implied daily yield for n = 24 Months
 
 
Actual yield
Fitted yield
January 2009
January 2010
January 2011
January 2012
0.5
1
1.5
2
2.5
3
Observed and model−implied daily yield for n = 60 Months
 
 
Actual yield
Fitted yield
January 2009
January 2010
January 2011
January 2012
1.5
2
2.5
3
3.5
4
4.5
Observed and model−implied daily yield for n = 120 Months
 
 
Actual yield
Fitted yield
1997
2000
2002
2005
2007
2010
−3
−2
−1
0
1
2
3
4
5
Standardized ten−year treasury term premium and MOVE Index
 
 
Term premium
MOVE Index
Fig. 10 Five-factor model: observed and model-implied daily yields
This ﬁgure provides plots of daily yields for the two-, ﬁve- and ten-year maturities as outlined in Subsection 4.4
ﬁtted by the ﬁve-factor speciﬁcation. Loadings from monthly principal components are applied to daily yields to obtain
daily factors. Solid lines plot observed yields, and dashed lines plot yields as implied by the model. The lower right panel
compares the standardized ﬁve-factor model-implied ten-year term premium to the standardized one-month Merrill lynch
Option Volatility Estimate (MOVE) index.
65

1990
1995
2000
2005
2010
−2.5
−2
−1.5
−1
−0.5
0
0.5
1
1.5
2
2.5
First factor, PC1: bootstrapped confidence interval
1990
1995
2000
2005
2010
−2.5
−2
−1.5
−1
−0.5
0
0.5
1
1.5
2
2.5
Second factor, PC2: bootstrapped confidence interval
1990
1995
2000
2005
2010
−3
−2
−1
0
1
2
3
4
5
Second factor, PC3: bootstrapped confidence interval
1990
1995
2000
2005
2010
−4
−3
−2
−1
0
1
2
3
4
5
Second factor, PC4: bootstrapped confidence interval
1990
1995
2000
2005
2010
−6
−4
−2
0
2
4
6
Second factor, PC5: bootstrapped confidence interval
Fig. 11 Consistency of Observed Factors
This ﬁgure provides plots of bootstrapped 95% conﬁdence intervals around the yield principal components. Principal
components from the ﬁtted yields are constructed according to the bootstrap procedure in Subsection 4.5. PC1, . . . , PC5
denote the ﬁrst through ﬁfth principal components of Treasury yields.
66