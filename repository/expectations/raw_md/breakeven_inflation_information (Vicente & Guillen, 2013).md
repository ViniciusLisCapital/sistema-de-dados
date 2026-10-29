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

References
[1] Almeida, C. and J. Vicente (2009). Identifying volatility risk premia
from fixed income Asian options. Journal of Banking & Finance, 33,
pp. 652-661.
[2] Bernanke, B. (2004). What policymakers can learn
from asset prices, Speech Before the Investment An-
alyst Society of Chicago, April 15, available at
http://www.federalreserve.gov/boarddocs/speeches/2004/20040415/default.htm.
[3] Campbell, J. and R. Shiller (1991). Yield spreads and interest rate move-
ments: A bird’s eye view, Review of Economic Studies, 58, pp. 495-514.
[4] Christensen, B. J. and N. R. Prabhala (1998). The relation between
implied and realized volatility. Journal of Financial Economics, 50, pp.
125-150.
[5] D’Amico, S., D. Kim and M. Wei (2008). Tips from TIPS: The infor-
mational content of Treasury Inflation-Protected Security prices, BIS
Working Papers, 248.
[6] Garbade, K. and M. Rutherford (2007). Buybacks in Treasury cash and
debt management, Staff Report 304, Federal Reserve Bank of New York.
[7] Garc´ıa, J. and T. Werner (2010). Inflation risks and inflation risk premia,
Working Paper 1162, European Central Bank.
[8] Greenwood, R. and D. Vayanos (2009). Price pressure in the bond mar-
ket, working paper, Harvard University.
[9] Grishchenko, O. and J. Huang (2010). Inflation risk premium: Evidence
from the TIPS market, Working Paper.
[10] Ho¨rdahl, P. (2008). The inflation risk premium in the term structure of
interest rates, BIS Quarterly Review.
[11] Joyce, M., P. Lildholdt, and S. Sorensen (2010), Extracting inflation
expectations and inflation risk premia from the term structure: a joint
model of the UK nominal and real yield curves, Journal of Banking &
Finance, 34, pp. 281-294.
[12] Newey, W. K. and K. D. West (1987). A simple, positive semi-definite,
heteroskedasticity and autocorrelation consistent covariance matrix,
Econometrica, 55, pp. 703-708.
14

[13] Pan, J. and K. Singleton (2008). Default and recovery implicit in the
term structure of sovereign CDS spreads. Journal of Finance, 63, pp.
2345-2384.
[14] Ruud, P. A. (1984). Tests of specification in econometrics. Econometric
Reviews, 3, pp. 211-242.
[15] Svensson L. (1994). Monetary policy with flexible exchange rates and
forward interest rates as indicators, Institute for International Economic
Studies, Stockholm University.
[16] Vayanos, D. and J. Vila (2009). A preference-habitat model of term
structure of interest rates. Working Paper.
15

Banco Central do Brasil
Trabalhos para Discussão
Os Trabalhos para Discussão podem ser acessados na internet, no formato PDF,
no endereço: http://www.bc.gov.br
Working Paper Series
Working Papers in PDF format can be downloaded from: http://www.bc.gov.br
1 Implementing Inflation Targeting in Brazil Jul/2000
Joel Bogdanski, Alexandre Antonio Tombini and Sérgio Ribeiro da Costa
Werlang
2 Política Monetária e Supervisão do Sistema Financeiro Nacional no Jul/2000
Banco Central do Brasil
Eduardo Lundberg
Monetary Policy and Banking Supervision Functions on the Central Jul/2000
Bank
Eduardo Lundberg
3 Private Sector Participation: a Theoretical Justification of the Brazilian Jul/2000
Position
Sérgio Ribeiro da Costa Werlang
4 An Information Theory Approach to the Aggregation of Log-Linear Jul/2000
Models
Pedro H. Albuquerque
5 The Pass-Through from Depreciation to Inflation: a Panel Study Jul/2000
Ilan Goldfajn and Sérgio Ribeiro da Costa Werlang
6 Optimal Interest Rate Rules in Inflation Targeting Frameworks Jul/2000
José Alvaro Rodrigues Neto, Fabio Araújo and Marta Baltar J. Moreira
7 Leading Indicators of Inflation for Brazil Sep/2000
Marcelle Chauvet
8 The Correlation Matrix of the Brazilian Central Bank’s Standard Model Sep/2000
for Interest Rate Market Risk
José Alvaro Rodrigues Neto
9 Estimating Exchange Market Pressure and Intervention Activity Nov/2000
Emanuel-Werner Kohlscheen
10 Análise do Financiamento Externo a uma Pequena Economia Mar/2001
Aplicação da Teoria do Prêmio Monetário ao Caso Brasileiro: 1991–1998
Carlos Hamilton Vasconcelos Araújo e Renato Galvão Flôres Júnior
11 A Note on the Efficient Estimation of Inflation in Brazil Mar/2001
Michael F. Bryan and Stephen G. Cecchetti
12 A Test of Competition in Brazilian Banking Mar/2001
Márcio I. Nakane
16

13 Modelos de Previsão de Insolvência Bancária no Brasil Mar/2001
Marcio Magalhães Janot
14 Evaluating Core Inflation Measures for Brazil Mar/2001
Francisco Marcos Rodrigues Figueiredo
15 Is It Worth Tracking Dollar/Real Implied Volatility? Mar/2001
Sandro Canesso de Andrade and Benjamin Miranda Tabak
16 Avaliação das Projeções do Modelo Estrutural do Banco Central do Mar/2001
Brasil para a Taxa de Variação do IPCA
Sergio Afonso Lago Alves
Evaluation of the Central Bank of Brazil Structural Model’s Inflation Jul/2001
Forecasts in an Inflation Targeting Framework
Sergio Afonso Lago Alves
17 Estimando o Produto Potencial Brasileiro: uma Abordagem de Função Abr/2001
de Produção
Tito Nícias Teixeira da Silva Filho
Estimating Brazilian Potential Output: a Production Function Approach Aug/2002
Tito Nícias Teixeira da Silva Filho
18 A Simple Model for Inflation Targeting in Brazil Apr/2001
Paulo Springer de Freitas and Marcelo Kfoury Muinhos
19 Uncovered Interest Parity with Fundamentals: a Brazilian Exchange May/2001
Rate Forecast Model
Marcelo Kfoury Muinhos, Paulo Springer de Freitas and Fabio Araújo
20 Credit Channel without the LM Curve May/2001
Victorio Y. T. Chu and Márcio I. Nakane
21 Os Impactos Econômicos da CPMF: Teoria e Evidência Jun/2001
Pedro H. Albuquerque
22 Decentralized Portfolio Management Jun/2001
Paulo Coutinho and Benjamin Miranda Tabak
23 Os Efeitos da CPMF sobre a Intermediação Financeira Jul/2001
Sérgio Mikio Koyama e Márcio I. Nakane
24 Inflation Targeting in Brazil: Shocks, Backward-Looking Prices, and Aug/2001
IMF Conditionality
Joel Bogdanski, Paulo Springer de Freitas, Ilan Goldfajn and
Alexandre Antonio Tombini
25 Inflation Targeting in Brazil: Reviewing Two Years of Monetary Policy Aug/2001
1999/00
Pedro Fachada
26 Inflation Targeting in an Open Financially Integrated Emerging Aug/2001
Economy: the Case of Brazil
Marcelo Kfoury Muinhos
27 Complementaridade e Fungibilidade dos Fluxos de Capitais Set/2001
Internacionais
Carlos Hamilton Vasconcelos Araújo e Renato Galvão Flôres Júnior
17

28 Regras Monetárias e Dinâmica Macroeconômica no Brasil: uma Nov/2001
Abordagem de Expectativas Racionais
Marco Antonio Bonomo e Ricardo D. Brito
29 Using a Money Demand Model to Evaluate Monetary Policies in Brazil Nov/2001
Pedro H. Albuquerque and Solange Gouvêa
30 Testing the Expectations Hypothesis in the Brazilian Term Structure of Nov/2001
Interest Rates
Benjamin Miranda Tabak and Sandro Canesso de Andrade
31 Algumas Considerações sobre a Sazonalidade no IPCA Nov/2001
Francisco Marcos R. Figueiredo e Roberta Blass Staub
32 Crises Cambiais e Ataques Especulativos no Brasil Nov/2001
Mauro Costa Miranda
33 Monetary Policy and Inflation in Brazil (1975-2000): a VAR Estimation Nov/2001
André Minella
34 Constrained Discretion and Collective Action Problems: Reflections on Nov/2001
the Resolution of International Financial Crises
Arminio Fraga and Daniel Luiz Gleizer
35 Uma Definição Operacional de Estabilidade de Preços Dez/2001
Tito Nícias Teixeira da Silva Filho
36 Can Emerging Markets Float? Should They Inflation Target? Feb/2002
Barry Eichengreen
37 Monetary Policy in Brazil: Remarks on the Inflation Targeting Regime, Mar/2002
Public Debt Management and Open Market Operations
Luiz Fernando Figueiredo, Pedro Fachada and Sérgio Goldenstein
38 Volatilidade Implícita e Antecipação de Eventos de Stress: um Teste para Mar/2002
o Mercado Brasileiro
Frederico Pechir Gomes
39 Opções sobre Dólar Comercial e Expectativas a Respeito do Mar/2002
Comportamento da Taxa de Câmbio
Paulo Castor de Castro
40 Speculative Attacks on Debts, Dollarization and Optimum Currency Apr/2002
Areas
Aloisio Araujo and Márcia Leon
41 Mudanças de Regime no Câmbio Brasileiro Jun/2002
Carlos Hamilton V. Araújo e Getúlio B. da Silveira Filho
42 Modelo Estrutural com Setor Externo: Endogenização do Prêmio de Jun/2002
Risco e do Câmbio
Marcelo Kfoury Muinhos, Sérgio Afonso Lago Alves e Gil Riella
43 The Effects of the Brazilian ADRs Program on Domestic Market Jun/2002
Efficiency
Benjamin Miranda Tabak and Eduardo José Araújo Lima
18

44 Estrutura Competitiva, Produtividade Industrial e Liberação Comercial Jun/2002
no Brasil
Pedro Cavalcanti Ferreira e Osmani Teixeira de Carvalho Guillén
45 Optimal Monetary Policy, Gains from Commitment, and Inflation Aug/2002
Persistence
André Minella
46 The Determinants of Bank Interest Spread in Brazil Aug/2002
Tarsila Segalla Afanasieff, Priscilla Maria Villa Lhacer and Márcio I. Nakane
47 Indicadores Derivados de Agregados Monetários Set/2002
Fernando de Aquino Fonseca Neto e José Albuquerque Júnior
48 Should Government Smooth Exchange Rate Risk? Sep/2002
Ilan Goldfajn and Marcos Antonio Silveira
49 Desenvolvimento do Sistema Financeiro e Crescimento Econômico no Set/2002
Brasil: Evidências de Causalidade
Orlando Carneiro de Matos
50 Macroeconomic Coordination and Inflation Targeting in a Two-Country Sep/2002
Model
Eui Jung Chang, Marcelo Kfoury Muinhos and Joanílio Rodolpho Teixeira
51 Credit Channel with Sovereign Credit Risk: an Empirical Test Sep/2002
Victorio Yi Tson Chu
52 Generalized Hyperbolic Distributions and Brazilian Data Sep/2002
José Fajardo and Aquiles Farias
53 Inflation Targeting in Brazil: Lessons and Challenges Nov/2002
André Minella, Paulo Springer de Freitas, Ilan Goldfajn and
Marcelo Kfoury Muinhos
54 Stock Returns and Volatility Nov/2002
Benjamin Miranda Tabak and Solange Maria Guerra
55 Componentes de Curto e Longo Prazo das Taxas de Juros no Brasil Nov/2002
Carlos Hamilton Vasconcelos Araújo e Osmani Teixeira de Carvalho de
Guillén
56 Causality and Cointegration in Stock Markets: Dec/2002
the Case of Latin America
Benjamin Miranda Tabak and Eduardo José Araújo Lima
57 As Leis de Falência: uma Abordagem Econômica Dez/2002
Aloisio Araujo
58 The Random Walk Hypothesis and the Behavior of Foreign Capital Dec/2002
Portfolio Flows: the Brazilian Stock Market Case
Benjamin Miranda Tabak
59 Os Preços Administrados e a Inflação no Brasil Dez/2002
Francisco Marcos R. Figueiredo e Thaís Porto Ferreira
60 Delegated Portfolio Management Dec/2002
Paulo Coutinho and Benjamin Miranda Tabak
19

61 O Uso de Dados de Alta Freqüência na Estimação da Volatilidade e Dez/2002
do Valor em Risco para o Ibovespa
João Maurício de Souza Moreira e Eduardo Facó Lemgruber
62 Taxa de Juros e Concentração Bancária no Brasil Fev/2003
Eduardo Kiyoshi Tonooka e Sérgio Mikio Koyama
63 Optimal Monetary Rules: the Case of Brazil Feb/2003
Charles Lima de Almeida, Marco Aurélio Peres, Geraldo da Silva e Souza
and Benjamin Miranda Tabak
64 Medium-Size Macroeconomic Model for the Brazilian Economy Feb/2003
Marcelo Kfoury Muinhos and Sergio Afonso Lago Alves
65 On the Information Content of Oil Future Prices Feb/2003
Benjamin Miranda Tabak
66 A Taxa de Juros de Equilíbrio: uma Abordagem Múltipla Fev/2003
Pedro Calhman de Miranda e Marcelo Kfoury Muinhos
67 Avaliação de Métodos de Cálculo de Exigência de Capital para Risco de Fev/2003
Mercado de Carteiras de Ações no Brasil
Gustavo S. Araújo, João Maurício S. Moreira e Ricardo S. Maia Clemente
68 Real Balances in the Utility Function: Evidence for Brazil Feb/2003
Leonardo Soriano de Alencar and Márcio I. Nakane
69 r-filters: a Hodrick-Prescott Filter Generalization Feb/2003
Fabio Araújo, Marta Baltar Moreira Areosa and José Alvaro Rodrigues Neto
70 Monetary Policy Surprises and the Brazilian Term Structure of Interest Feb/2003
Rates
Benjamin Miranda Tabak
71 On Shadow-Prices of Banks in Real-Time Gross Settlement Systems Apr/2003
Rodrigo Penaloza
72 O Prêmio pela Maturidade na Estrutura a Termo das Taxas de Juros Maio/2003
Brasileiras
Ricardo Dias de Oliveira Brito, Angelo J. Mont'Alverne Duarte e Osmani
Teixeira de C. Guillen
73 Análise de Componentes Principais de Dados Funcionais – uma Maio/2003
Aplicação às Estruturas a Termo de Taxas de Juros
Getúlio Borges da Silveira e Octavio Bessada
74 Aplicação do Modelo de Black, Derman & Toy à Precificação de Opções Maio/2003
Sobre Títulos de Renda Fixa
Octavio Manuel Bessada Lion, Carlos Alberto Nunes Cosenza e César das
Neves
75 Brazil’s Financial System: Resilience to Shocks, no Currency Jun/2003
Substitution, but Struggling to Promote Growth
Ilan Goldfajn, Katherine Hennings and Helio Mori
20

76 Inflation Targeting in Emerging Market Economies Jun/2003
Arminio Fraga, Ilan Goldfajn and André Minella
77 Inflation Targeting in Brazil: Constructing Credibility under Exchange Jul/2003
Rate Volatility
André Minella, Paulo Springer de Freitas, Ilan Goldfajn and Marcelo Kfoury
Muinhos
78 Contornando os Pressupostos de Black & Scholes: Aplicação do Modelo Out/2003
de Precificação de Opções de Duan no Mercado Brasileiro
Gustavo Silva Araújo, Claudio Henrique da Silveira Barbedo, Antonio
Carlos Figueiredo, Eduardo Facó Lemgruber
79 Inclusão do Decaimento Temporal na Metodologia Out/2003
Delta-Gama para o Cálculo do VaR de Carteiras
Compradas em Opções no Brasil
Claudio Henrique da Silveira Barbedo, Gustavo Silva Araújo,
Eduardo Facó Lemgruber
80 Diferenças e Semelhanças entre Países da América Latina: Out/2003
uma Análise de Markov Switching para os Ciclos Econômicos
de Brasil e Argentina
Arnildo da Silva Correa
81 Bank Competition, Agency Costs and the Performance of the Jan/2004
Monetary Policy
Leonardo Soriano de Alencar and Márcio I. Nakane
82 Carteiras de Opções: Avaliação de Metodologias de Exigência de Capital Mar/2004
no Mercado Brasileiro
Cláudio Henrique da Silveira Barbedo e Gustavo Silva Araújo
83 Does Inflation Targeting Reduce Inflation? An Analysis for the OECD May/2004
Industrial Countries
Thomas Y. Wu
84 Speculative Attacks on Debts and Optimum Currency Area: a Welfare May/2004
Analysis
Aloisio Araujo and Marcia Leon
85 Risk Premia for Emerging Markets Bonds: Evidence from Brazilian May/2004
Government Debt, 1996-2002
André Soares Loureiro and Fernando de Holanda Barbosa
86 Identificação do Fator Estocástico de Descontos e Algumas Implicações Maio/2004
sobre Testes de Modelos de Consumo
Fabio Araujo e João Victor Issler
87 Mercado de Crédito: uma Análise Econométrica dos Volumes de Crédito Dez/2004
Total e Habitacional no Brasil
Ana Carla Abrão Costa
88 Ciclos Internacionais de Negócios: uma Análise de Mudança de Regime Dez/2004
Markoviano para Brasil, Argentina e Estados Unidos
Arnildo da Silva Correa e Ronald Otto Hillbrecht
89 O Mercado de Hedge Cambial no Brasil: Reação das Instituições Dez/2004
Financeiras a Intervenções do Banco Central
Fernando N. de Oliveira
21

90 Bank Privatization and Productivity: Evidence for Brazil Dec/2004
Márcio I. Nakane and Daniela B. Weintraub
91 Credit Risk Measurement and the Regulation of Bank Capital and Dec/2004
Provision Requirements in Brazil – a Corporate Analysis
Ricardo Schechtman, Valéria Salomão Garcia, Sergio Mikio Koyama and
Guilherme Cronemberger Parente
92 Steady-State Analysis of an Open Economy General Equilibrium Model Apr/2005
for Brazil
Mirta Noemi Sataka Bugarin, Roberto de Goes Ellery Jr., Victor Gomes
Silva, Marcelo Kfoury Muinhos
93 Avaliação de Modelos de Cálculo de Exigência de Capital para Risco Abr/2005
Cambial
Claudio H. da S. Barbedo, Gustavo S. Araújo, João Maurício S. Moreira e
Ricardo S. Maia Clemente
94 Simulação Histórica Filtrada: Incorporação da Volatilidade ao Modelo Abr/2005
Histórico de Cálculo de Risco para Ativos Não-Lineares
Claudio Henrique da Silveira Barbedo, Gustavo Silva Araújo e Eduardo
Facó Lemgruber
95 Comment on Market Discipline and Monetary Policy by Carl Walsh Apr/2005
Maurício S. Bugarin and Fábia A. de Carvalho
96 O que É Estratégia: uma Abordagem Multiparadigmática para a Ago/2005
Disciplina
Anthero de Moraes Meirelles
97 Finance and the Business Cycle: a Kalman Filter Approach with Markov Aug/2005
Switching
Ryan A. Compton and Jose Ricardo da Costa e Silva
98 Capital Flows Cycle: Stylized Facts and Empirical Evidences for Aug/2005
Emerging Market Economies
Helio Mori e Marcelo Kfoury Muinhos
99 Adequação das Medidas de Valor em Risco na Formulação da Exigência Set/2005
de Capital para Estratégias de Opções no Mercado Brasileiro
Gustavo Silva Araújo, Claudio Henrique da Silveira Barbedo,e Eduardo
Facó Lemgruber
100 Targets and Inflation Dynamics Oct/2005
Sergio A. L. Alves and Waldyr D. Areosa
101 Comparing Equilibrium Real Interest Rates: Different Approaches to Mar/2006
Measure Brazilian Rates
Marcelo Kfoury Muinhos and Márcio I. Nakane
102 Judicial Risk and Credit Market Performance: Micro Evidence from Apr/2006
Brazilian Payroll Loans
Ana Carla A. Costa and João M. P. de Mello
103 The Effect of Adverse Supply Shocks on Monetary Policy and Output Apr/2006
Maria da Glória D. S. Araújo, Mirta Bugarin, Marcelo Kfoury Muinhos and
Jose Ricardo C. Silva
22

104 Extração de Informação de Opções Cambiais no Brasil Abr/2006
Eui Jung Chang e Benjamin Miranda Tabak
105 Representing Roommate’s Preferences with Symmetric Utilities Apr/2006
José Alvaro Rodrigues Neto
106 Testing Nonlinearities Between Brazilian Exchange Rates and Inflation May/2006
Volatilities
Cristiane R. Albuquerque and Marcelo Portugal
107 Demand for Bank Services and Market Power in Brazilian Banking Jun/2006
Márcio I. Nakane, Leonardo S. Alencar and Fabio Kanczuk
108 O Efeito da Consignação em Folha nas Taxas de Juros dos Empréstimos Jun/2006
Pessoais
Eduardo A. S. Rodrigues, Victorio Chu, Leonardo S. Alencar e Tony Takeda
109 The Recent Brazilian Disinflation Process and Costs Jun/2006
Alexandre A. Tombini and Sergio A. Lago Alves
110 Fatores de Risco e o Spread Bancário no Brasil Jul/2006
Fernando G. Bignotto e Eduardo Augusto de Souza Rodrigues
111 Avaliação de Modelos de Exigência de Capital para Risco de Mercado do Jul/2006
Cupom Cambial
Alan Cosme Rodrigues da Silva, João Maurício de Souza Moreira e Myrian
Beatriz Eiras das Neves
112 Interdependence and Contagion: an Analysis of Information Jul/2006
Transmission in Latin America's Stock Markets
Angelo Marsiglia Fasolo
113 Investigação da Memória de Longo Prazo da Taxa de Câmbio no Brasil Ago/2006
Sergio Rubens Stancato de Souza, Benjamin Miranda Tabak e Daniel O.
Cajueiro
114 The Inequality Channel of Monetary Transmission Aug/2006
Marta Areosa and Waldyr Areosa
115 Myopic Loss Aversion and House-Money Effect Overseas: an Sep/2006
Experimental Approach
José L. B. Fernandes, Juan Ignacio Peña and Benjamin M. Tabak
116 Out-Of-The-Money Monte Carlo Simulation Option Pricing: the Join Sep/2006
Use of Importance Sampling and Descriptive Sampling
Jaqueline Terra Moura Marins, Eduardo Saliby and Joséte Florencio dos
Santos
117 An Analysis of Off-Site Supervision of Banks’ Profitability, Risk and Sep/2006
Capital Adequacy: a Portfolio Simulation Approach Applied to Brazilian
Banks
Theodore M. Barnhill, Marcos R. Souto and Benjamin M. Tabak
118 Contagion, Bankruptcy and Social Welfare Analysis in a Financial Oct/2006
Economy with Risk Regulation Constraint
Aloísio P. Araújo and José Valentim M. Vicente
23

119 A Central de Risco de Crédito no Brasil: uma Análise de Utilidade de Out/2006
Informação
Ricardo Schechtman
120 Forecasting Interest Rates: an Application for Brazil Oct/2006
Eduardo J. A. Lima, Felipe Luduvice and Benjamin M. Tabak
121 The Role of Consumer’s Risk Aversion on Price Rigidity Nov/2006
Sergio A. Lago Alves and Mirta N. S. Bugarin
122 Nonlinear Mechanisms of the Exchange Rate Pass-Through: a Phillips Nov/2006
Curve Model With Threshold for Brazil
Arnildo da Silva Correa and André Minella
123 A Neoclassical Analysis of the Brazilian “Lost-Decades” Nov/2006
Flávia Mourão Graminho
124 The Dynamic Relations between Stock Prices and Exchange Rates: Nov/2006
Evidence for Brazil
Benjamin M. Tabak
125 Herding Behavior by Equity Foreign Investors on Emerging Markets Dec/2006
Barbara Alemanni and José Renato Haas Ornelas
126 Risk Premium: Insights over the Threshold Dec/2006
José L. B. Fernandes, Augusto Hasman and Juan Ignacio Peña
127 Uma Investigação Baseada em Reamostragem sobre Requerimentos de Dec/2006
Capital para Risco de Crédito no Brasil
Ricardo Schechtman
128 Term Structure Movements Implicit in Option Prices Dec/2006
Caio Ibsen R. Almeida and José Valentim M. Vicente
129 Brazil: Taming Inflation Expectations Jan/2007
Afonso S. Bevilaqua, Mário Mesquita and André Minella
130 The Role of Banks in the Brazilian Interbank Market: Does Bank Type Jan/2007
Matter?
Daniel O. Cajueiro and Benjamin M. Tabak
131 Long-Range Dependence in Exchange Rates: the Case of the European Mar/2007
Monetary System
Sergio Rubens Stancato de Souza, Benjamin M. Tabak and Daniel O.
Cajueiro
132 Credit Risk Monte Carlo Simulation Using Simplified Creditmetrics’ Mar/2007
Model: the Joint Use of Importance Sampling and Descriptive Sampling
Jaqueline Terra Moura Marins and Eduardo Saliby
133 A New Proposal for Collection and Generation of Information on Mar/2007
Financial Institutions’ Risk: the Case of Derivatives
Gilneu F. A. Vivan and Benjamin M. Tabak
134 Amostragem Descritiva no Apreçamento de Opções Européias através Abr/2007
de Simulação Monte Carlo: o Efeito da Dimensionalidade e da
Probabilidade de Exercício no Ganho de Precisão
Eduardo Saliby, Sergio Luiz Medeiros Proença de Gouvêa e Jaqueline Terra
Moura Marins
24

135 Evaluation of Default Risk for the Brazilian Banking Sector May/2007
Marcelo Y. Takami and Benjamin M. Tabak
136 Identifying Volatility Risk Premium from Fixed Income Asian Options May/2007
Caio Ibsen R. Almeida and José Valentim M. Vicente
137 Monetary Policy Design under Competing Models of Inflation May/2007
Persistence
Solange Gouvea e Abhijit Sen Gupta
138 Forecasting Exchange Rate Density Using Parametric Models: May/2007
the Case of Brazil
Marcos M. Abe, Eui J. Chang and Benjamin M. Tabak
139 Selection of Optimal Lag Length inCointegrated VAR Models with Jun/2007
Weak Form of Common Cyclical Features
Carlos Enrique Carrasco Gutiérrez, Reinaldo Castro Souza and Osmani
Teixeira de Carvalho Guillén
140 Inflation Targeting, Credibility and Confidence Crises Aug/2007
Rafael Santos and Aloísio Araújo
141 Forecasting Bonds Yields in the Brazilian Fixed income Market Aug/2007
Jose Vicente and Benjamin M. Tabak
142 Crises Análise da Coerência de Medidas de Risco no Mercado Brasileiro Ago/2007
de Ações e Desenvolvimento de uma Metodologia Híbrida para o
Expected Shortfall
Alan Cosme Rodrigues da Silva, Eduardo Facó Lemgruber, José Alberto
Rebello Baranowski e Renato da Silva Carvalho
143 Price Rigidity in Brazil: Evidence from CPI Micro Data Sep/2007
Solange Gouvea
144 The Effect of Bid-Ask Prices on Brazilian Options Implied Volatility: a Oct/2007
Case Study of Telemar Call Options
Claudio Henrique da Silveira Barbedo and Eduardo Facó Lemgruber
145 The Stability-Concentration Relationship in the Brazilian Banking Oct/2007
System
Benjamin Miranda Tabak, Solange Maria Guerra, Eduardo José Araújo
Lima and Eui Jung Chang
146 Movimentos da Estrutura a Termo e Critérios de Minimização do Erro Out/2007
de Previsão em um Modelo Paramétrico Exponencial
Caio Almeida, Romeu Gomes, André Leite e José Vicente
147 Explaining Bank Failures in Brazil: Micro, Macro and Contagion Effects Oct/2007
(1994-1998)
Adriana Soares Sales and Maria Eduarda Tannuri-Pianto
148 Um Modelo de Fatores Latentes com Variáveis Macroeconômicas para a Out/2007
Curva de Cupom Cambial
Felipe Pinheiro, Caio Almeida e José Vicente
149 Joint Validation of Credit Rating PDs under Default Correlation Oct/2007
Ricardo Schechtman
25

150 A Probabilistic Approach for Assessing the Significance of Contextual Oct/2007
Variables in Nonparametric Frontier Models: an Application for
Brazilian Banks
Roberta Blass Staub and Geraldo da Silva e Souza
151 Building Confidence Intervals with Block Bootstraps for the Variance Nov/2007
Ratio Test of Predictability
Eduardo José Araújo Lima and Benjamin Miranda Tabak
152 Demand for Foreign Exchange Derivatives in Brazil: Dec/2007
Hedge or Speculation?
Fernando N. de Oliveira and Walter Novaes
153 Aplicação da Amostragem por Importância Dez/2007
à Simulação de Opções Asiáticas Fora do Dinheiro
Jaqueline Terra Moura Marins
154 Identification of Monetary Policy Shocks in the Brazilian Market Dec/2007
for Bank Reserves
Adriana Soares Sales and Maria Tannuri-Pianto
155 Does Curvature Enhance Forecasting? Dec/2007
Caio Almeida, Romeu Gomes, André Leite and José Vicente
156 Escolha do Banco e Demanda por Empréstimos: um Modelo de Decisão Dez/2007
em Duas Etapas Aplicado para o Brasil
Sérgio Mikio Koyama e Márcio I. Nakane
157 Is the Investment-Uncertainty Link Really Elusive? The Harmful Effects Jan/2008
of Inflation Uncertainty in Brazil
Tito Nícias Teixeira da Silva Filho
158 Characterizing the Brazilian Term Structure of Interest Rates Feb/2008
Osmani T. Guillen and Benjamin M. Tabak
159 Behavior and Effects of Equity Foreign Investors on Emerging Markets Feb/2008
Barbara Alemanni and José Renato Haas Ornelas
160 The Incidence of Reserve Requirements in Brazil: Do Bank Stockholders Feb/2008
Share the Burden?
Fábia A. de Carvalho and Cyntia F. Azevedo
161 Evaluating Value-at-Risk Models via Quantile Regressions Feb/2008
Wagner P. Gaglianone, Luiz Renato Lima and Oliver Linton
162 Balance Sheet Effects in Currency Crises: Evidence from Brazil Apr/2008
Marcio M. Janot, Márcio G. P. Garcia and Walter Novaes
163 Searching for the Natural Rate of Unemployment in a Large Relative May/2008
Price Shocks’ Economy: the Brazilian Case
Tito Nícias Teixeira da Silva Filho
164 Foreign Banks’ Entry and Departure: the recent Brazilian experience Jun/2008
(1996-2006)
Pedro Fachada
165 Avaliação de Opções de Troca e Opções de Spread Européias e Jul/2008
Americanas
Giuliano Carrozza Uzêda Iorio de Souza, Carlos Patrício Samanez e
Gustavo Santos Raposo
26

166 Testing Hyperinflation Theories Using the Inflation Tax Curve: a case Jul/2008
study
Fernando de Holanda Barbosa and Tito Nícias Teixeira da Silva Filho
167 O Poder Discriminante das Operações de Crédito das Instituições Jul/2008
Financeiras Brasileiras
Clodoaldo Aparecido Annibal
168 An Integrated Model for Liquidity Management and Short-Term Asset Jul/2008
Allocation in Commercial Banks
Wenersamy Ramos de Alcântara
169 Mensuração do Risco Sistêmico no Setor Bancário com Variáveis Jul/2008
Contábeis e Econômicas
Lucio Rodrigues Capelletto, Eliseu Martins e Luiz João Corrar
170 Política de Fechamento de Bancos com Regulador Não-Benevolente: Jul/2008
Resumo e Aplicação
Adriana Soares Sales
171 Modelos para a Utilização das Operações de Redesconto pelos Bancos Ago/2008
com Carteira Comercial no Brasil
Sérgio Mikio Koyama e Márcio Issao Nakane
172 Combining Hodrick-Prescott Filtering with a Production Function Aug/2008
Approach to Estimate Output Gap
Marta Areosa
173 Exchange Rate Dynamics and the Relationship between the Random Aug/2008
Walk Hypothesis and Official Interventions
Eduardo José Araújo Lima and Benjamin Miranda Tabak
174 Foreign Exchange Market Volatility Information: an investigation of Aug/2008
real-dollar exchange rate
Frederico Pechir Gomes, Marcelo Yoshio Takami and Vinicius Ratton
Brandi
175 Evaluating Asset Pricing Models in a Fama-French Framework Dec/2008
Carlos Enrique Carrasco Gutierrez and Wagner Piazza Gaglianone
176 Fiat Money and the Value of Binding Portfolio Constraints Dec/2008
Mário R. Páscoa, Myrian Petrassi and Juan Pablo Torres-Martínez
177 Preference for Flexibility and Bayesian Updating Dec/2008
Gil Riella
178 An Econometric Contribution to the Intertemporal Approach of the Dec/2008
Current Account
Wagner Piazza Gaglianone and João Victor Issler
179 Are Interest Rate Options Important for the Assessment of Interest Dec/2008
Rate Risk?
Caio Almeida and José Vicente
180 A Class of Incomplete and Ambiguity Averse Preferences Dec/2008
Leandro Nascimento and Gil Riella
181 Monetary Channels in Brazil through the Lens of a Semi-Structural Apr/2009
Model
André Minella and Nelson F. Souza-Sobrinho
27

182 Avaliação de Opções Americanas com Barreiras Monitoradas de Forma Abr/2009
Discreta
Giuliano Carrozza Uzêda Iorio de Souza e Carlos Patrício Samanez
183 Ganhos da Globalização do Capital Acionário em Crises Cambiais Abr/2009
Marcio Janot e Walter Novaes
184 Behavior Finance and Estimation Risk in Stochastic Portfolio Apr/2009
Optimization
José Luiz Barros Fernandes, Juan Ignacio Peña and Benjamin
Miranda Tabak
185 Market Forecasts in Brazil: performance and determinants Apr/2009
Fabia A. de Carvalho and André Minella
186 Previsão da Curva de Juros: um modelo estatístico com variáveis Maio/2009
macroeconômicas
André Luís Leite, Romeu Braz Pereira Gomes Filho e José Valentim
Machado Vicente
187 The Influence of Collateral on Capital Requirements in the Brazilian Jun/2009
Financial System: an approach through historical average and logistic
regression on probability of default
Alan Cosme Rodrigues da Silva, Antônio Carlos Magalhães da Silva,
Jaqueline Terra Moura Marins, Myrian Beatriz Eiras da Neves and Giovani
Antonio Silva Brito
188 Pricing Asian Interest Rate Options with a Three-Factor HJM Model Jun/2009
Claudio Henrique da Silveira Barbedo, José Valentim Machado Vicente and
Octávio Manuel Bessada Lion
189 Linking Financial and Macroeconomic Factors to Credit Risk Jul/2009
Indicators of Brazilian Banks
Marcos Souto, Benjamin M. Tabak and Francisco Vazquez
190 Concentração Bancária, Lucratividade e Risco Sistêmico: uma Set/2009
abordagem de contágio indireto
Bruno Silva Martins e Leonardo S. Alencar
191 Concentração e Inadimplência nas Carteiras de Empréstimos dos Set/2009
Bancos Brasileiros
Patricia L. Tecles, Benjamin M. Tabak e Roberta B. Staub
192 Inadimplência do Setor Bancário Brasileiro: uma avaliação de Set/2009
suas medidas
Clodoaldo Aparecido Annibal
193 Loss Given Default: um estudo sobre perdas em operações prefixadas no Set/2009
mercado brasileiro
Antonio Carlos Magalhães da Silva, Jaqueline Terra Moura Marins e
Myrian Beatriz Eiras das Neves
194 Testes de Contágio entre Sistemas Bancários – A crise do subprime Set/2009
Benjamin M. Tabak e Manuela M. de Souza
195 From Default Rates to Default Matrices: a complete measurement of Oct/2009
Brazilian banks' consumer credit delinquency
Ricardo Schechtman
28

196 The role of macroeconomic variables in sovereign risk Oct/2009
Marco S. Matsumura and José Valentim Vicente
197 Forecasting the Yield Curve for Brazil Nov/2009
Daniel O. Cajueiro, Jose A. Divino and Benjamin M. Tabak
198 Impacto dos Swaps Cambiais na Curva de Cupom Cambial: uma análise Nov/2009
segundo a regressão de componentes principais
Alessandra Pasqualina Viola, Margarida Sarmiento Gutierrez, Octávio
Bessada Lion e Cláudio Henrique Barbedo
199 Delegated Portfolio Management and Risk Taking Behavior Dec/2009
José Luiz Barros Fernandes, Juan Ignacio Peña and Benjamin Miranda
Tabak
200 Evolution of Bank Efficiency in Brazil: A DEA Approach Dec/2009
Roberta B. Staub, Geraldo Souza and Benjamin M. Tabak
201 Efeitos da Globalização na Inflação Brasileira Jan/2010
Rafael Santos e Márcia S. Leon
202 Considerações sobre a Atuação do Banco Central na Crise de 2008 Mar/2010
Mário Mesquita e Mario Torós
203 Hiato do Produto e PIB no Brasil: uma Análise de Dados em Abr/2010
Tempo Real
Rafael Tiecher Cusinato, André Minella e Sabino da Silva Pôrto Júnior
204 Fiscal and monetary policy interaction: a simulation based analysis Apr/2010
of a two-country New Keynesian DSGE model with heterogeneous
households
Marcos Valli and Fabia A. de Carvalho
205 Model selection, estimation and forecasting in VAR models with Apr/2010
short-run and long-run restrictions
George Athanasopoulos, Osmani Teixeira de Carvalho Guillén,
João Victor Issler and Farshid Vahid
206 Fluctuation Dynamics in US interest rates and the role of monetary Apr/2010
policy
Daniel Oliveira Cajueiro and Benjamin M. Tabak
207 Brazilian Strategy for Managing the Risk of Foreign Exchange Rate Apr/2010
Exposure During a Crisis
Antonio Francisco A. Silva Jr.
208 Correlação de default: uma investigação empírica de créditos de varejo Maio/2010
no Brasil
Antonio Carlos Magalhães da Silva, Arnildo da Silva Correa, Jaqueline
Terra Moura Marins e Myrian Beatriz Eiras das Neves
209 Produção Industrial no Brasil: uma análise de dados em tempo real Maio/2010
Rafael Tiecher Cusinato, André Minella e Sabino da Silva Pôrto Júnior
210 Determinants of Bank Efficiency: the case of Brazil May/2010
Patricia Tecles and Benjamin M. Tabak
29

211 Pessimistic Foreign Investors and Turmoil in Emerging Markets: the Aug/2010
case of Brazil in 2002
Sandro C. Andrade and Emanuel Kohlscheen
212 The Natural Rate of Unemployment in Brazil, Chile, Colombia and Sep/2010
Venezuela: some results and challenges
Tito Nícias Teixeira da Silva
213 Estimation of Economic Capital Concerning Operational Risk in a Oct/2010
Brazilian Banking Industry Case
Helder Ferreira de Mendonça, Délio José Cordeiro Galvão and
Renato Falci Villela Loures
30