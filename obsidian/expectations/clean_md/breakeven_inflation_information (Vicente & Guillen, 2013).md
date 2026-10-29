ISSN 1518-3548
CGC 00.038.166/0001-05
Working Paper Series Brasília n. 214 Oct. 2010 p. 1-30

Working Paper Series
Edited by Research Department (Depep) – E-mail: workingpaper@bcb.gov.br
Editor: Benjamin Miranda Tabak – E-mail: benjamin.tabak@bcb.gov.br
Editorial Assistant: Jane Sofia Moita – E-mail: jane.sofia@bcb.gov.br
Head of Research Department: Adriana Soares Sales – E-mail: adriana.sales@bcb.gov.br
The Banco Central do Brasil Working Papers are all evaluated in double blind referee process.
Reproduction is permitted only if source is stated as follows: Working Paper n. 214.
Authorized by Carlos Hamilton Vasconcelos Araújo, Deputy Governor for Economic Policy.
General Control of Publications
Banco Central do Brasil
Secre/Surel/Cogiv
SBS – Quadra 3 – Bloco B – Edifício-Sede – 1º andar
Caixa Postal 8.670
70074-900 Brasília – DF – Brazil
Phones: +55 (61) 3414-3710 and 3414-3565
Fax: +55 (61) 3414-3626
E-mail: editor@bcb.gov.br
The views expressed in this work are those of the authors and do not necessarily reflect those of the Banco Central or
its members.
Although these Working Papers often represent preliminary work, citation of source is required when used or reproduced.
As opiniões expressas neste trabalho são exclusivamente do(s) autor(es) e não refletem, necessariamente, a visão do Banco
Central do Brasil.
Ainda que este artigo represente trabalho preliminar, é requerida a citação da fonte, mesmo quando reproduzido
parcialmente.
Consumer Complaints and Public Enquiries Center
Banco Central do Brasil
Secre/Surel/Diate
SBS – Quadra 3 – Bloco B – Edifício-Sede – 2º subsolo
70074-900 Brasília – DF – Brazil
Fax: +55 (61) 3414-2553
Internet: http://www.bcb.gov.br/?english

Do inflation-linked bonds contain information
about future inflation?
Jos´e Valentim Machado Vicente∗
Osmani Teixeira de Carvalho Guillen †
The Working Papers should not be reported as representing the views
of the Banco Central do Brasil. The views expressed in the papers are
those of the author(s) and not necessarily reflect those of the Banco
Central do Brasil.
Abstract
There is a widespread belief that inflation-linked bonds are a di-
rect source of information about inflation expectations. In this paper
we address this issue by analyzing the relationship between break-
even inflation (the difference between nominal and real yields) and
future inflation. The dataset is extracted from Brazilian Treasury
bonds covering the period from April 2005 to July 2010. We find that
break-even inflation is an unbiased forecast only of the 3-month and
6-month ahead inflation. For medium horizons (12 and 18 months)
break-even inflation has weak explanatory power of future inflation.
Over long horizons (24 and 30 months), we report a significant, but
counterintuitive, negative relationship between the break-even and re-
alized inflations.
Keywords: inflation-linked bonds; real and nominal yields; term pre-
mia; break-even inflation
JEL Code: E31, E43, G12.
∗Central Bank of Brazil. E-mail: jose.valentim@bcb.gov.br.
†Central Bank of Brazil. E-mail: osmani.guillen@bcb.gov.br.
3

1 Introduction
Market participants and policymakers interpret break-even inflation (the
spread between nominal and real yields) as the main indicator of expected
inflation. According to the Federal Reserve chairman, inflation-linked bonds
appear to be the most important source of future inflation expectations
(Bernanke, 2004). However, it is well known that the break-even inflation
rate (BEIR) can be decomposed as an inflation expectation plus a risk pre-
mium term. This leads to the following questions: Does the BEIR efficiently
predict future inflation? In other words, is the inflation risk premium neg-
ligible? A more general formulation of these issues can be stated as: Do
inflation-linked bonds contain information about future prices? In this pa-
per we shed light on these questions through a model free procedure using
data on Brazilian Treasury yields.
Our analysis is based on a series of regressions between the realized in-
flation (dependent variable) and the BEIR (independent variable) for the
horizons of 3, 6, 12, 18, 24 and 30 months. The significance of the param-
eters and R2 provide a way to test the predictive ability and explanatory
power of the BEIR. To avoid specification problems such as autocorrelations
and endogeneity, we run these regressions using different approaches. First,
we consider an OLS procedure. Next, we employ instrumental variables, esti-
mating the model by TSLS and GMM techniques, with the covariance matrix
computed according to Newey and West (1987)1. The use of instrumental
variables aims to keep consistency when the regressor is correlated with the
error term, while the Newey-West method overcomes autocorrelation in the
residuals.
Many other studies have investigated the inflation risk premium and con-
sequently the relationship between break-even and realized inflations using
real and nominal interest rates. Among others we can cite D’Amico et al.
(2008), H¨ordahl (2008), Garcia and Werner (2010), Joyce et al. (2010),
and Grishchenko and Huang (2010). The first four papers work in an affine
arbitrage-free framework. D’Amico et al. (2008) show that although the U.S.
inflation-linked bond yields contain a liquidity premium and time-varying in-
flation risk premium, the Treasury Inflation-Protected Security (TIPS) rates
are a useful proxy for inflation expectations. Garcia and Werner (2010) ap-
ply a model similar to that used by D’Amico et al. (2008) in the euro area.
They find that the term structure of inflation risk premia is upward slop-
ing and varies from 7 to 25 basis points. Ho¨rdahl (2008) uses a structural
1TSLS and GMM stand for Two-Step Least Squares and Generalized Method of Mo-
ments, respectively.
4

macroeconomic model to estimate inflation risk premia in the United States
and the euro area. He shows that inflation risk premia have an increasing
pattern with respect to maturity for the euro area and a flatter one for the
United States. Joyce et al. (2010) estimate a joint model of UK nominal
and real term structures. They find that the Bank of England’s indepen-
dence to set interest rates in May 1997 decreased the inflation risk premium
and the inflation expectation embodied in the term structure. The article of
Grishchenko and Huang (2010) computes the inflation risk premium as the
difference between the TIPS break-even inflation and an estimation of future
inflation. They show that the inflation risk premium is time-varying with
negative values from 2000 to 2004 and positive from 2004 to 2008.
However, none of the above studies use the methodology proposed in
this work. Our procedure to assess the information content in the BEIR
has previously been applied in other contexts. For example, Campbell and
Shiller (1991) test whether the slope of the term structure predicts changes
in interest rates. To this end, they run regressions of future yields on forward
yields. Christensen and Prabhala (1998) regress the realized volatility on the
implied volatility of S&P 500 to evaluate the relationship between these two
volatilities. Our strategy is close in spirit to Campbell and Shiller (1989)
and Christensen and Prabhala (1998), except we replace yields and volatility
by inflation. That is an innovation of this paper: a model free approach to
measure the explanatory power of the BEIR. To the best of our knowledge,
there is no study using this procedure to addresses this question.
Some countries have issued real return government securities. For ex-
ample, the United Kingdom has issued index-linked bonds since 1981. On
the other hand, the United States made its first issue in 1997, so the trad-
ing history is more recent. Although we could carry out this study based
on data from these countries, we opt to use a Brazilian database for two
reasons. First, Brazil is one of the most important emerging economies. To-
gether with Russia, India and China, Brazil forms the so-called BRICs, a
group of the most promising emerging markets. However, there are no stud-
ies about BEIR applied to an important emerging country. Second, unlike
other markets, the indexation lag of Brazilian real bonds is very small (only
a half month). Moreover, Brazilian real bonds do not have protection against
deflation2.
Our main findings can be summarized as follows. First, the BEIR is an
unbiased estimate only of the 3-month and 6-month ahead inflation. Second,
for the horizons of 12 and 18 months, the BEIR has weak explanatory power
2The TIPS indexation lag is three months. Grishchenko and Huang (2010) point out
that ignoring the indexation lag results in an underestimate of the inflation risk premium.
5

for future inflation. On the other hand, the 24-month and 30-month break-
even inflations explain future inflation. However, for these two long horizons,
we obtain a surprising result: the relationship between the break-even and
realized inflations is negative. Of course these findings are not a puzzle. They
can be easily explained by a time-varying inflation risk premium, which is
not captured by our linear model. In other words, this suggests that the
expectations hypothesis fails for medium and long-term bonds. Finally, our
results are robust to a number of alternative econometric methods to estimate
the model.
The remainder of the paper is organized as follows. Section 2 presents
the data and stylized facts, while Section 3 discusses the methodology used
in this work. Section 4 presents the results and Section 5 concludes.
2 Model
Let yn(τ) and yr(τ) be the continuously compounded yields for nominal and
t t
real yields at t with time to maturity τ. The BEIR is defined as:
i (τ) = yn(τ) − yr(τ),
t t t
where i (τ) is the BEIR for period t and horizon τ.
t
Denote by h (1) the continuously compounded annual rate of change be-
t
tween two observations of a price index (from t to t + 1). Then, the accumu-
lated inflation rate between t and t + τ is given by
t+τ−1
1 (cid:88)
h (τ) = h (1).
t j
τ
j=t
The information content of the BEIR can be assessed by estimating a
regression of the form3
h (τ) = c i (τ) + c + (cid:15) . (1)
t 1 t 2 t
Using Eq. (1), we can test if the BEIR contains some information about
future inflation. If c is nonzero, the answer to this question is positive.
1
Moreover, we can verify if the BEIR is an unbiased forecast of realized infla-
tion. In this case, we should find that c = 1 and c = 0.
1 2
The BEIR can be decomposed as the sum of the expected inflation rate
plus a risk premium (see Grishchenko and Huang, 2010):
i (τ) = E (h (τ)) + IRP (τ), (2)
t t t t
3In fact, we should write cτ and cτ. However, we omit the superscript τ for brevity.
1 2
6

where E (·) denotes the mathematical expectation conditional on informa-
t
tion available at time t. The expectation hypothesis states that the term
premium is constant over time but possibly maturity-dependent, that is,
IRP (τ) does not depend on t. Under this hypothesis and using a further
t
assumption of rational expectations, the econometric specification of (2) is
given by (1). Therefore, Eq. (1) can also be used to test a BEIR version of
the expectation hypothesis.
3 Data and stylized facts
Our sample consists of a monthly series of real and nominal yields from
April 2005 to July 2010. This dataset is provided by the National Asso-
ciation of Financial Market Institutions (ANDIMA)4. The term structure
of nominal rates is extracted from plain vanilla (NTN-F) and zero-coupon
(LTN) Brazilian Treasury bonds using the Svensson interpolation model (see
Svensson, 1994). The face value of the NTN-F is R$ 1,000.00 (one thousand
Brazilian Reals) and it pays a bi-annual interest coupon of R$ 48.815. LTN
is a zero cupon bond with face value of R$ 1,000.00. The term structure of
real rates are also constructed by the Svensson model, however the curve is
fitted using NTN-B bonds, the leading Brazilian Treasury inflation-protected
security. The yield of the NTN-B is linked to the IPCA, a consumer price
index adopted in the inflation targeting regime of the Central Bank of Brazil.
NTN-B does not have the indexation lag problem present in the TIPS market,
since interest is paid based on the current level of the IPCA (available with
a maximum delay of 15 days). Although the NTN-B bonds have been issued
since 2001, we start our sample in April 2005 to avoid liquidity problems in
the NTN-B market between 2001 and 2005.
The Brazilian inflation-linked securities market is one of the largest in the
world with over US$ 200 billion of NTN-B bonds outstanding6. The average
term to maturity of NTN-B bonds is nearly six years. The Brazilian fixed-
rate market is also significant. The LTN and NTN-F bonds have around US$
155 billion and US$ 126 billion in bonds outstanding, with average terms to
maturity of 12 and 30 months, respectively7.
4ANDIMA is an association of Brazilian financial service providers. For more informa-
tion about ANDIMA, see the website http://www.andima.com.br/english/index.asp.
5The Brazilian Real/US Dollar exchange rate was around 1.75 in July 2010.
6For comparison purposes the TIPS market has US$ 500 billion outstanding.
7These data are for April 2010. For more information about the Brazil-
ian Treasury bonds market, see the website of the Central Bank of Brazil,
http://www.bcb.gov.br/?english.
7

i(3) i(6) i(12) i(18) i(24) i(30) IPCA
Mean 4.82% 4.63% 4.52% 4.55% 4.63% 4.73% 4.68%
Median 4.69% 4.46% 4.33% 4.38% 4.49% 4.64% 4.53%
Maximum 8.13% 6.79% 6.94% 7.31% 7.42% 7.40% 10.95%
Minimum 2.09% 2.61% 3.19% 3.19% 3.24% 3.31% -2.49%
Std. dev. 0.012 0.008 0.007 0.007 0.007 0.007 0.027
Skewness 0.70 0.36 0.88 1.16 1.17 1.04 0.07
Kurtosis 3.99 3.08 4.29 5.41 5.68 5.22 3.18
Jarque-Bera 7.75 1.37 12.67 29.86 33.67 24.64 0.14
Correlation 30.8% 35.1% 7.0% -25.3% -32.9% -62.9% -
Table 1: Descriptive statistics - BEIR and IPCA.
This table presents some descriptive statistics of the break-even inflation
(i(τ), τ = 3, 6, 12, 18, 24, 30) and the rate of change of the consumer
price index (IPCA). The skewness of a symmetric distribution is zero. Pos-
itive skewness means that the distribution has a long right tail and negative
skewness implies that the distribution has a long left tail. The kurtosis of
the normal distribution is 3. If the kurtosis exceeds 3, the distribution is
peaked (leptokurtic) relative to the normal; if the kurtosis is less than 3,
the distribution is flat (platykurtic) relative to the normal. Under the null
hypothesis of a normal distribution, the Jarque-Bera statistic is distributed
as chi-squared with 2 degrees of freedom. Boldface values mean signifi-
cance at a 95% confidence level. The bottom row shows the correlation
coefficients between the break-even inflation and the realized inflation.
Table 1 presents some descriptive statistics of the BEIR and IPCA. The
averages of the IPCA and BEIR for all horizons are around 4.5%. Both
the BEIR and the realized inflation are leptokurtic with a positive skewness
(long right tail). The Jarque-Bera statistic indicates that the 3-month and
6-month BEIR and the IPCA appear to be normally distributed. This is a
sign that the BEIR can better explain realized inflation over a short horizon
than a long horizon. This sign will be confirmed in the empirical exercise
presented in Section 4. The correlation coefficients between the BEIR and
realized inflation (the bottom row of Table 1) are positive for the horizons of
3, 6 and 12 months and negative for the horizons of 18, 24, and 36 months.
Figure 1 depicts the time evolution of the BEIR and the rate of change of
the IPCA from April 2005 to July 2010. Note that the BEIR term structure
is almost everywhere upwarding sloping. Moreover, the BEIR and IPCA
8

exhibit no trend.
Figure 1: BEIR and IPCA.
This figure contains time series of the 3-, 6-, 12-, 18-, 24-, 30- month BEIR
and the rate of change of the IPCA from April 2005 to July 2010. The
BEIR is the difference between the nominal and real yields. The IPCA is
the main Brazilian consumer price index.
4 Empirical results
In order to provide robust results, we estimate Eq. (1) using three different
methods. First we adopt an OLS procedure. Next, we introduce instrumental
variables to control for endogeneity. In this case, the model is estimated using
TSLS and GMM with the variance-covariance matrix computed as suggested
by Newey and West (1987). The instrument specification is i (τ) for TSLS
t−1
and i (τ), i (τ) and i (τ) for GMM (τ = 3, 6, 12, 18, 24, 30). Tables
t−1 t−2 t−3
2, 3 and 4 report the estimates of c and c , the standard deviations, the
1 2
corrected R2, and the F -statistic of the joint hypothesis c = 1 and c = 0
1 2
for the OLS, TSLS and GMM methods, respectively8.
8To check the consistency of OLS estimators, we perform the Durbin-Wu-Hausman
test (see, Ruud, 1984). We found no significant difference among OLS, TSLS and GMM.
Nevertheless, we opt to report the TSLS and GMM estimations in order to provide robust
results.
9

Horizon 3 6 12 18 24 30
c 0.49 0.58 0.08 -0.25 -0.25 -0.36
1
(0.20) (0.21) (0.17) (0.15) (0.12) (0.08)
c 0.02 0.02 0.04 0.06 0.06 0.06
2
(0.01) (0.01) (0.007) (0.006) (0.005) (0.004)
R2 9.50% 12.33% 0.49% 6.39% 10.81% 39.52%
c = 1 0.02 0.14 0.00 0.00 0.00 0.00
1
c = 0
2
Table 2: OLS results of h (τ) = c i (τ) + c + (cid:15) .
t 1 t 2 t
This table presents the OLS estimates of h (τ) = c i (τ) + c + (cid:15) (Eq. (1)
t 1 t 2 t
in the paper) for the horizons of 3, 6, 12, 18, 24 and 30 months. Here, i (τ)
t
denotes the BEIR at time t and horizon τ, and h (τ) denotes the consumer
t
price index (IPCA) accumulated between t and t + τ. The bottom row
shows the F -statistic of the joint hypothesis c = 1 and c = 0. Numbers
1 2
in parentheses denote standard errors. Boldface values mean significance
at a 95% confidence level.
Note first that the estimates are very similar across the different estima-
tion strategies, which indicates that our results are robust. The slope c is
1
significant for the horizons of 3, 6, 24 and 30 months9. Hence, in the short
and long term, the BEIR contains some information about future inflation.
However, moving from the short to the long horizon, we can easily observe
a distinct link between the BEIR and future inflation. For the horizons of 3
and 6 months, the F -statistic of the joint hypothesis c = 1 and c = 0 shows
1 2
that the BEIR is an unbiased estimator of future inflation. In other words,
we cannot reject the BEIR version of the expectation hypothesis10. On the
other hand, for the horizons of 24 and 30 months the relationship between the
BEIR and future inflation is negative11. Though peculiar, this finding simply
suggests that the expectation hypothesis fails over long horizons. Therefore,
the linear relation of Eq. (1) probably cannot accommodate the link between
9Apart from the estimate of c for the 24-month horizon calculated by GMM.
1
10The BEIR version of the expectation hypothesis states that the inflation risk premium
is constant over time.
11These results are consistent with correlation coefficients shown in Table 1.
10

Horizon 3 6 12 18 24 30
c 0.77 0.63 -0.18 -0.42 -0.43 -0.49
1
(0.30) (0.29) (0.25) (0.22) (0.15) (0.08)
c 0.008 0.017 0.05 0.06 0.065 0.068
2
(0.014) (0.014) (0.01) (0.01) (0.007) (0.004)
R2 6.35% 13.45% -2.59% 2.80% 6.31% 35.23%
c = 1 0.60 0.43 0.00 0.00 0.00 0.00
1
c = 0
2
Table 3: TSLS results of h (τ) = c i (τ) + c + (cid:15) .
t 1 t 2 t
This table presents the TSLS estimates of h (τ) = c i (τ) + c + (cid:15) (Eq.
t 1 t 2 t
(1) in the paper) for the horizons of 3, 6, 12, 18, 24 and 30 months. Here,
i (τ) denotes the BEIR at time t and horizon τ, and h (τ) denotes the
t t
consumer price index (IPCA) accumulated between t and t + τ. The in-
strument specification is i (τ) (τ = 3, 6, 12, 18, 24, 30) and standard
t−1
errors are computed by the Newey-West estimator. The bottom row shows
the F -statistic of the joint hypothesis c = 1 and c = 0. Numbers in
1 2
parentheses denote standard errors. Boldface values mean significance at a
95% confidence level.
the BEIR and future inflation. A more general specification is necessary in
this case. The assumption of constant risk premium can be relaxed, implying
a time-varying inflation risk premium for long horizons. This result is consis-
tent with previous empirical evidence. For example, Grishchenko and Huang
(2010) document that although the U.S. 10-year inflation risk premium is
around zero on average, it is time-varying.
For medium horizons the coefficient c is not significant and R2 is very
1
low. Moreover, the F -statistic rejects the joint hypothesis c = 1 and c = 0.
1 2
This means that the BEIR does not have information about the 12- and 18-
month ahead inflation. We have difficulties to interpret the constant c as an
2
inflation risk premium when c is statistically different from 1. Nevertheless,
1
since c is significant ranging between 400 to 700 basis points for medium
2
and long horizons we can conjecture that investors require a high reward to
hold inflation-linked bonds with maturities greater than one year.
In a nutshell, apart from the short horizon, we present evidence that the
11

Horizon 3 6 12 18 24 30
c 0.93 0.69 0.02 -0.08 -0.18 -0.54
1
(0.29) (0.26) (0.25) (0.22) (0.25) (0.15)
c 0.003 0.014 0.04 0.05 0.05 0.070
2
(0.014) (0.012) (0.01) (0.01) (0.01) (0.006)
J-statistic 0.11 0.20 0.20 0.31 0.14 0.15
c = 1 0.94 0.51 0.00 0.00 0.00 0.00
1
c = 0
2
Table 4: GMM results of h (τ) = c i (τ) + c + (cid:15) .
t 1 t 2 t
This table presents the GMM estimates of h (τ) = c i (τ)+c +(cid:15) (Eq. (1)
t 1 t 2 t
in the paper) for the horizons of 3, 6, 12, 18, 24 and 30 months. Here, i (τ)
t
denotes the BEIR at time t and horizon τ, and h (τ) denotes the consumer
t
price index (IPCA) accumulated between t and t + τ. The instrument
specification is i (τ), i (τ) and i (τ) (τ = 3, 6, 12, 18, 24, 30)
t−1 t−2 t−3
and standard errors are computed by the Newey-West estimator. The J-
statistic is the p-value of the test for over-identifying restrictions. The
bottom row shows the F -statistic of the joint hypothesis c = 1 and c = 0.
1 2
Numbers in parentheses denote standard errors. Boldface values mean
significance at a 95% confidence level.
BEIR fails to correctly predict subsequent movements in inflation. Although
the aim of this work is not to examine the causes of this failure, we can
imagine some reasons. First, we have only five years of data. Despite the
fact our sample size is compatible with that found in other empirical finance
studies of emerging economies (see, for instance, Pan and Singleton, 2008,
and Almeida and Vicente, 2009), we believe that a larger dataset would pro-
vide more accurate results. Second, the Brazilian market can actually be
risky, which would imply a high risk premium, explaining the weak rela-
tionship between the BEIR and future inflation. Third, the BEIR can be
affected by a “clientele effect”, which means that the NTN-B may attract
investors with preferences for specific maturities and strong aversion to in-
flation uncertainty12. The clientele effect would thus cause a distortion on
12The clientele effect is modeled within the preferred-habitat theory. Although this
theory was proposed more than a half century ago, there are few academic works dealing
12

the inflation expectation extracted from inflation-index bonds. In Brazil,
the typical clientele for inflation-index bonds are pension funds who aim to
hedge their inflation-linked liabilities. In July 2010, pension funds held 33%
of NTN-B outstanding and only 5% of LTN and NTN-F outstanding.
5 Conclusion
We proposed a model free procedure to assess the relationship between the
break-even and future inflations. We showed that the break-even inflation is
informative about future inflation over horizons of 3, 6, 24 and 30 months.
For the 3- and 6-month horizons, besides being informative, break-even infla-
tion is an unbiased estimator as well. However, over the horizons of 24 and
30 months, the relationship between the break-even and future inflations is
negative. On the other hand, for the horizons of 12 and 18 months, break-
even inflation has almost no power to explain future inflation. These results
indicate that policymakers and market participants should be very careful in
using break-even inflation as a proxy for future movements in price indexes.
with it. Nevertheless, Vayanos and Vila (2009) have recently revisited the preferred-habitat
theory through the lens of no-arbitrage models. Moreover Garbade and Rutherford (2007)
and Greenwood and Vayanos (2009) discuss episodes supporting the preferred-habitat
view.
13

196 The role of macroeconomic variables in sovereign risk Oct/2009
204 Fiscal and monetary policy interaction: a simulation based analysis Apr/2010
of a two-country New Keynesian DSGE model with heterogeneous
households
205 Model selection, estimation and forecasting in VAR models with Apr/2010
short-run and long-run restrictions