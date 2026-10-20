Chapter 7
UNEMPLOYMENT IN THE NEW KEYNESIAN MODEL
The New Keynesian model with staggered price and wage setting
developed in chapter 6 remains a framework of reference for the analysis
of ﬂuctuations and stabilization policies1. Many central banks and policy
institutions have adopted medium-scale versions of that model as part of
their toolkit for the purpose of forecasting and simulation of alternative
policies.2
But like any other macroeconomic framework, the New Keynesian
model has many shortcomings. Among the latter, the lack of any
reference to unemployment is often pointed to as one of the model’s
main weaknesses. This is not surprising, given the central role of that
variable in the policy debate and in public perceptions of the costs
associated with business cycles. Furthermore, the conspicuous absence
of unemployment from the standard New Keynesian model could also
be interpreted as suggesting that there is no reason why central banks
should monitor or respond to it in a systematic way. It would seem as
if, through the lens of the New Keynesian model, unemployment and the
frictions underlying it were not essential for understanding ﬂuctuations in
nominal and real variables, nor a key ingredient in the design of monetary
policy.
Over the past few years a growing number of researchers have sought
to rectify that anomaly by developing frameworks that combine the
nominal rigidities and consequent monetary non-neutralities of the New
Keynesian model with labor market imperfections that give rise to
unemployment. Those frictions are generally introduced by embedding
a labor market with search and matching, in the tradition of Mortensen
and Pissarides (1994), into some version of the New Keynesian model.
1 The present chapter draws heavily from my Zeuthen lectures, published in Galí
(2011b).
2 See, e.g., Smets and Wouters (2003, 2007) and Christiano, Eichenbaum, and Evans
(2005) for examples of medium-scale versions of those models. For descriptions of versions
of those models developed at policy institutions, see Christoffel, Coenen, and Warne
(2008), Edge, Kiley, and Laforte (2007), and Erceg, Guerrieri, and Gust (2006), among
others.

CHAPTER 7
The resulting framework has been used in both positive and normative
applications, with and without the assumption of wage rigidities.3
In the present chapter a different approach is adopted to introduc-
ing unemployment in the New Keynesian framework. The proposed
approach, based on Galí (2011a, 2011b), involves a reinterpretation of
the labor market in the standard New Keynesian model with staggered
wage setting, as developed in chapter 6, rather than a modiﬁcation
or an extension of that model. The resulting framework preserves the
convenience of the representative household paradigm, and allows one
to determine the equilibrium levels of employment, the labor force,
and, hence, the unemployment rate (as well as other macro variables of
interest) conditional on the monetary policy rule in place. Unemployment
in the model results from the presence of market power in labor markets,
reﬂected in a positive average wage markup, that is, a positive gap
between the prevailing wage and the disutility of work (expressed in
terms of consumption) for the marginal worker employed. On the
other hand, ﬂuctuations in the unemployment rate are associated with
variations in that average wage markup due to the presence of nominal
wage rigidities.
One important advantage of the proposed approach lies in its com-
patibility with a variety of assumptions regarding aspects of the model
unrelated to unemployment, including the speciﬁc form of price and
wage rigidities, the speciﬁcation of the household utility, and the possible
presence of time-varying desired markups. Needless to say, the proposed
framework also has limitations of its own. In particular, it abstracts from
potential sources of unemployment other than noncompetitive wages,
including those associated with the costly reallocation of labor across
ﬁrms or sectors (in terms of time and other resources) which may give
rise to frictional unemployment. It is important to stress, however, that
the ﬁndings of much of the recent literature on labor market frictions
suggest that the latter are not enough in order to generate unemployment
ﬂuctuations of size and persistence similar to those observed in the data,
pointing to the need for some kind of wage rigidity.4
The chapter is organized as follows. First, the basic model of unem-
ployment is introduced and embedded in the standard New Keynesian
framework of chapter 6. Using a calibrated version of the model, its
predictions regarding the properties of unemployment in response to
technology, demand, and monetary policy shocks are derived, under
the assumption that the central bank follows a conventional Taylor
rule. The analysis puts special emphasis on the role played by nominal
3 See section 7.4 for some of the key contributions to that literature.
4 See, e.g., Hall (2005), Gertler and Trigari (2009), Galí (2011a), and Shimer (2005).

UNEMPLOYMENT AND MONETARY POLICY
201
wage rigidities in accounting for the volatility and persistence of un-
employment. The chapter then turns its focus to the relation between
unemployment and the design of monetary policy, by analyzing the
behavior of unemployment and several other macro variables under
the optimal monetary policy, and comparing it to that prevailing
under a standard Taylor rule. That analysis suggests the presence of
likely welfare gains from stabilizing the unemployment rate beyond
what is implied by the Taylor rule. This is conﬁrmed by the study
of the properties of a generalized Taylor rule, one that allows for a
systematic response to the unemployment rate, in addition to output
and price inﬂation. The chapter concludes with a note on the related
literature, with references to alternative approaches to the one presented
here.
7.1 INTRODUCING UNEMPLOYMENT IN THE
NEW KEYNESIAN MODEL
A reformulation of the standard New Keynesian model with staggered
wage and price setting developed in chapter 6 is described next. The
variant presented here, based on Galí (2011a, 2011b), assumes that labor
is indivisible, that is, in each period any given individual either works a
ﬁxed number of hours or does not work at all. As a result, all variations
in labor input take place at the extensive margin (i.e., in the form of
variations in employment). Since that margin is the one that dominates
observed variations in total hours of work, the assumption of indivisible
labor remains a good ﬁrst approximation. Most importantly, however,
that assumption leads to a deﬁnition of unemployment consistent with
its empirical counterpart.
As discussed below, the model’s equilibrium includes the same set of
equations as the model in chapter 6, to which an additional equation
describing the evolution of unemployment is added. Thus, the reader is
referred to chapter 6 for the details of many of the derivations.
7.1.1 Households, Wage Setting, and Unemployment
The economy is assumed to have a large number of identical households.
Each household has a continuum of members represented by the unit
square and indexed by a pair ( j, s) ∈[0, 1] × [0, 1]. The ﬁrst index,
j ∈[0, 1], represents the type of labor service that a given household
member is specialized in. The second index, s ∈[0, 1], determines
the disutility from work. The latter is given by χsϕ if he is employed
and zero otherwise, where χ > 0 and ϕ > 0 are exogenous parameters.

CHAPTER 7
As in Merz (1995) and much of the subsequent literature, full risk sharing
within the household is assumed. Given the separability of preferences,
this implies the same level of consumption for all household members,
independently of their work status. This is not an innocuous assumption,
especially from a welfare viewpoint, but one that I stick to in order to
preserve the model’s tractability. 5
The household’s period utility is given by the integral of its members’
utilities and can thus be written as follows
U(Ct, {Nt( j)}; Zt) ≡

C1−σ
t
−1
1 −σ
−χ
 1
0
 Nt( j)
0
sϕdsdj

Zt
=

C1−σ
t
−1
1 −σ
−χ
 1
0
Nt( j)1+ϕ
1 + ϕ
dj

Zt
where Ct ≡
 1
0 Ct(i)1−1
ϵp di

ϵp
ϵp−1 is a consumption index, Ct(i) is the
quantity consumed of good i, for i ∈[0, 1], and Nt( j) ∈[0, 1] is the
fraction of members specialized in type j labor who are employed in
period t. As in previous chapters below the preference shifter zt ≡log Zt
is assumed to follow the AR(1) process:
zt = ρzzt−1 + εz
t
where ρz ∈[0, 1] and εz
t is a white noise process with zero mean and
variance σ 2
z .
Each household seeks to maximize
E0
∞

t=0
βtU(Ct, {Nt( j)}; Zt)
subject to a sequence of ﬂow budget constraints given by
 1
0
Pt(i)Ct(i)di + QtBt ≤Bt−1 +
 1
0
Wt( j)Nt( j)dj + Dt
(1)
where Pt(i) is the price of good i, Wt( j) is the nominal wage for type j
labor, Bt represents purchases of a nominally riskless one-period discount
5 See Christiano, Trabandt, and Walentin (2010) for an unemployment model with
separable preferences but different levels of consumption for employed and un-employed
household members.

203
bond paying one monetary unit, Qt is the price of that bond, and Dt
is a lump-sum component of income (which may include, among other
items, dividends from the ownership of ﬁrms). As in previous chapters,
the above sequence of period budget constraints is supplemented with a
solvency condition that prevents the household from engaging in Ponzi
schemes.
Optimal demand for each good resulting from utility maximization
takes the familiar form:
Ct(i) =
 Pt(i)
Pt
	−ϵp
Ct
(2)
where Pt ≡
 1
0 Pt(i)1−ϵpdi

1
1−ϵp denotes the price index for ﬁnal goods.
Note also that (2) implies that total consumption expenditures can be
written as
 1
0 Pt(i)Ct(i)di = PtCt.
The household’s intertemporal optimality condition is given by
Qt = βEt

Ct+1
Ct
	−σ  Zt+1
Zt
	  Pt
Pt+1

(3)
As in the model of chapter 6, the wage for each type of la-
bor is set by a union representing all the workers specialized in it,
whereas the corresponding employment level Nt( j) is determined by the
aggregation of ﬁrms’ labor demand, assumed to be allocated uniformly
across households. Thus, both Wt( j) and Nt( j) are taken as given
by each household, for all j
∈
[0, 1]. More speciﬁcally, and fol-
lowing Calvo’s formalism (Calvo (1983)), it is assumed that work-
ers specialized in a given type of labor (or the union representing
them) reset their nominal wage with probability 1 −θw each period.
That probability is independent of the time elapsed since they last
reset their wage, in addition to being independent across labor types.
Thus, a fraction of workers θw keep their wage unchanged in any
given period, making that parameter a natural index of nominal wage
rigidities.
Optimal wage setting proceeds as in chapter 6, to which the reader
is referred. As in that chapter, the optimal wage setting decision can be
combined with the law of motion for the average nominal wage to derive
the following equation describing wage inﬂation dynamics:
πw
t = βEt{πw
t+1} −λw
µw
t
(4)

CHAPTER 7
where πw
t ≡wt −wt−1 is wage inﬂation, µw
t ≡wt −pt −mrst denotes
the (log) average wage markup, where mrst ≡σct + ϕnt + ξ deﬁnes
the economy’s average marginal rate of substitution (with ξ ≡log χ),

µw
t ≡µw
t −µw (with µw ≡log Mw), and λw ≡(1−θw)(1−βθw)
θw(1+ϵwϕ)
> 0. In words,
wage inﬂation depends positively on expected one-period-ahead wage
inﬂation and negatively on the deviation of the average wage markup
from its desired value.
Next, and following Galí (2011a, 2011b), unemployment is introduced
in the framework above, allowing the wage inﬂation equation (4) to be
reformulated in terms of the unemployment rate.
7.1.2 Introducing Unemployment
Consider individual ( j,s) specialized in type j labor and with disutility of
work χsϕ. Using the welfare of its household as a criterion, and taking
as given current labor market conditions (as summarized by the wage
prevailing in his trade) that individual will be willing to work (and thus
be part of the labor force) in period t if and only if
Wt( j)
Pt
≥χCσ
t sϕ
that is, if and only if the relevant real wage exceeds the disutility
from work, where the latter is expressed in terms of consumption by
dividing the disutility term χsϕ by the household’s marginal utility of
consumption C−σ
t
.
Thus, the marginal supplier of type j labor, denoted by Lt( j),
is given by
Wt( j)
Pt
= χCσ
t Lt( j)ϕ
(5)
Deﬁne
the
aggregate
labor
force
(or
participation
rate)
as
Lt ≡
 1
0 Lt( j)dj. Taking logs and integrating over j one can derive the
following approximate relation:
wt −pt = σct + ϕlt + ξ
(6)
where use is made of the ﬁrst order approximations around the
symmetric steady state wt ≃
 1
0 wt( j)dj and lt ≃
 1
0 lt( j)dj . Equation (6)
can be thought of as an aggregate labor supply or participation equation.

205
Figure 7.1. The Wage Markup and the Unemployment Rate.
Following Galí (2011a, 2011b), the unemployment rate ut is deﬁned
as the log difference between the labor force and employment:
ut ≡lt −nt
(7)
This deﬁnition of the unemployment rate is, for low values of that
variable, very close to the conventional one, that is, 1 −Nt
Lt .6 Combining
the deﬁnition of the average wage markup µw
t ≡(wt−pt)−(σct+ϕnt+ξ)
with (6) and (7), one can obtain the following simple linear relation
between the wage markup and the unemployment rate
µw
t = ϕut
(8)
Figure 7.1 represents graphically the above relationship between the
average wage markup and the unemployment rate, using a conventional
labor market diagram. The ﬁgure emphasizes the idea that employment is
6 Note that 1 −Nt
Lt = 1 −exp{−ut} ≃ut for unemployment rates near zero.

CHAPTER 7
demand determined, with labor demand given by the inverse production
function (in logs)
nt =
1
1 −α (yt −at)
(9)
and, hence, is not directly inﬂuenced by the wage.
The labor force, on the other hand, is determined by the labor supply
equation (6). The unemployment rate corresponds to the horizontal gap
between the labor supply and labor demand schedules, at the level of
the prevailing average real wage. The wage markup µw
t , on the other
hand, is represented in the ﬁgure by the vertical gap between the wage
and the labor supply, at the level of current employment nt. Given
the assumed linearity, the ratio between “the two gaps” is constant
and given by ϕ, the slope of the labor supply schedule, as implied
by (8 ).
I deﬁne the natural rate of unemployment, un
t , as the unemployment
rate that would prevail in the absence of nominal wage rigidities. It
follows from the assumption of a constant desired wage markup that
such a natural rate is constant and given by
un = µw
ϕ
(10)
Equations (8) and (10) reveal the nature of unemployment in the
present model. In particular, (10) shows that the presence of market
power in the labor market, reﬂected in the wage markup µw > 0,
accounts for the existence of positive unemployment, even in the absence
of wage rigidities. On the other hand, (8) implies that ﬂuctuations
in unemployment are associated with variations in the wage markup.
In the New Keynesian model of chapter 6, wage markup variations
are the result of nominal wage rigidities. Such rigidities are, accord-
ingly, a necessary ingredient for the model to display unemployment
ﬂuctuations.
Note, however, that the above conclusion hinges critically on the
assumption of a constant desired wage markup µw, an assumption
maintained below. But it should be clear that the analysis above can be
easily generalized to an environment in which the desired wage markup
itself varies over time. In that case the natural rate of unemployment
will ﬂuctuate in response to variations in the desired markup, whereas
ﬂuctuations in actual unemployment will have two components: a ﬁrst
one associated with changes in the natural rate (driven by changes in
the desired wage markup), and a second one linked to deviations of

207
wage markups from their desired levels resulting from nominal wage
rigidities.7
Finally, note that by combining (4), (8), and (10) one can derive
a simple relation between wage inﬂation and the unemployment gap,
ut −un:
πw
t = βEt{πw
t+1} −λwϕ(ut −un)
(11)
Galí (2011a) refers to the previous equation as the New Keynesian
Wage Phillips Curve, and provides some evidence in its support using
postwar U.S. data. Note that in contrast with Phillips’s original curve
(Phillips (1958)), which involved a simple static relation between wage
inﬂation and unemployment, (11) is a forward-looking relation, which
can be rewritten to express wage inﬂation as a function of current and
expected future unemployment gaps. Furthermore, while the original
Phillips curve was a purely empirical relation, without any theoretical
justiﬁcation, (11) is derived from ﬁrst principles, with its coefﬁcients
being a function of structural parameters.
7.2 EQUILIBRIUM
The remaining equilibrium conditions correspond to those of the New
Keynesian framework developed in chapter 6. Since they were derived
and analyzed in detail therein, they are only listed below, together with
(11), for convenience:

yt = −1
σ (it −Et{π p
t+1} −rn
t ) + Et{
yt+1}
(12)
π p
t = βEt{π p
t+1} + κp
yt + λp
ωt
(13)
πw
t = βEt{πw
t+1} −λwϕ
ut
(14)

ωt ≡
ωt−1 + πw
t −π p
t −ωn
t
(15)
7 The interested reader can ﬁnd an analysis of a medium-scale version of the present
model allowing for variations in the desired wage markup in Galí , Smets, and Wouters
(2012).

CHAPTER 7
to which one must add an equation relating the unemployment gap

ut ≡ut −un to the output and real wage gaps, namely:8
ϕ
ut = 
µw
t
= 
ωt −(σ
ct + ϕ
nt)
= 
ωt −

σ +
ϕ
1 −α

yt
(16)
The natural values of the real interest rate and the real wage are now
given by (ignoring constant terms):
rn
t = ρ −σ(1 −ρa)ψyaat + (1 −ρz)zt

ωn
t = ψwaat
where, as in chapter 6, ψya ≡
1+ϕ
σ(1−α)+ϕ+α and ψwa ≡1−αψya
1−α
> 0.
In addition, equations (7) and (9), together with the fact that yn
t = y +
ψyaat can be used to determine the equilibrium behavior of employment,
nt, and participation, lt.
Finally, and in order to close the model, one or more equations
describing monetary policy must be added. Below, the optimal policy
under commitment as well as some simple interest rate rules are analyzed.
7.3 MONETARY POLICY DESIGN AND
UNEMPLOYMENT FLUCTUATIONS
In this section the properties of the unemployment rate in the face of
different shocks are determined for a calibrated version of the model
developed above. One goal of the exercise is to assess the ability of
the New Keynesian model to account for the empirical properties of
unemployment ﬂuctuations. In doing so, it is important to recognize the
model’s inherent limitations to provide a full account of the observed
behavior of macro variables, since it lacks many of the bells and
whistles found in medium-scale DSGE models (habit formation, capital
8 Note that (14) and (16) can be combined to yield the wage inﬂation equation used in
chapter 6, namely:
πw
t = βEt{πw
t+1} + κwyt −λwωt
where κw ≡λw

σ +
ϕ
1−α

. Thus the extension described here introduces a new variable
(ut) and an extra equation (16).

Unemployment rate
Employment
Labor force
Real wage
–0.015
–0.01
–0.005
–0.02
Figure 7.2. Response of Labor Market Variables to a Monetary Policy Shock.
accumulation, indexation, etc.).9 Its advantage, on the other hand, lies in
its simplicity and transparency.
The baseline calibration underlying the quantitative results reported
below is identical to that used in chapter 6, so the reader is referred to
the description therein. An advantage of the framework above lies in
the discipline it provides in the choice of a setting for ϵw, the elasticity
of substitution among labor types in production. Thus, note that the
average wage markup is tied to the natural rate of unemployment
through the relation Mw ≡
ϵw
ϵw−1 = exp{ϕun}. The assumptions of ϕ = 5
used earlier and un = 0.05 (consistent with an average unemployment
rate of 5 percent), implies ϵw =4.5, which is in turn is associated with an
average wage markup of 28 percent.
7.3.1 The Effects of a Monetary Policy Shock on the Labor Market
Figure 7.2 plots the dynamic response of employment, nt, the unem-
ployment rate, ut, the labor force, lt, and the real wage wt −pt to an
9 See Galí, Smets, and Wouters (2012) for an analysis of the sources of unemployment
ﬂuctuations in an estimated medium-scale version of the present model.

CHAPTER 7
exogenous monetary policy shock, under the assumption that the central
bank follows a conventional Taylor rule of the form
it = 0.01 + 1.5π p
t + 0.125
yt + vt
(17)
As in earlier chapters, it is assumed an autoregressive coefﬁcient ρv =
0.5 in the AR(1) process followed by the monetary policy shifter vt, with
the size of the initial exogenous impulse being 0.25 (i.e., corresponding to
an increase in the nominal interest rate of 100 basis points, in annualized
terms). The responses are expressed in percentage deviations from the
initial steady state.
As the ﬁgure makes clear, the unemployment rate rises substantially,
and persistently, in response to the tightening of monetary policy. The
increase in the unemployment rate is largely due to the decline in
employment and only marginally to an increase in the labor force.
The latter is, in turn, a consequence of the negative wealth effect, as
reﬂected in the consumption decline (not shown), combined with a nearly
unchanged real wage.10 Finally, the real wage is shown to decline, albeit
by a small amount, due the downward pressure of unemployment on
nominal wages, which appears to dominate the effect of the decline in
price inﬂation.
The connection between wage rigidities and the properties of unem-
ployment ﬂuctuations is further explored next. For the sake of concrete-
ness, focus is restricted to ﬂuctuations driven by monetary shocks. One
may want to view those shocks as a stand-in for other aggregate demand
shocks.11
Table 7.1 reports measures of volatility, persistence, and cyclicality of
unemployment, conditioned on monetary policy shocks, for alternative
conﬁgurations of θw, the degree of wage stickiness, and ρv, the autore-
gressive coefﬁcient of the shock process. The standard deviation of the
shock σv is set to 0.25 percent (i.e., 1 percent in annualized terms). The
question posed here can be stated as follows: How does the degree of
nominal rigidities, indexed by θw , inﬂuence the volatility, persistence
and cyclicality of the unemployment rate?
10 Though small, the countercyclical response of the labor force to a monetary shock
appears to be at odds with the empirical evidence reported in Christiano, Trabandt, and
Walentin (2010). Galí, Smets, and Wouters (2012) modify the household’s utility function
along the lines of Jaimovich and Rebelo (2009), and show that a speciﬁcation of the latter
consistent with small wealth effects implies a procyclical (and small) response of the labor
force to a monetary shock, in a way consistent with the evidence.
11 In particular, shocks to the discount rate would have an identical effect on labor market
variables.

211
TABLE 7.1
Wage Rigidities and Unemployment Fluctuations
Volatility
Persistence
Cyclicality
θw :
0.1
0.5
0.75
0.1
0.5
0.75
0.1
0.5
0.75
ρv = 0.0
0.25
0.32
0.33
−0.14
−0.02
−0.01
−0.99
−0.99
−0.99
ρv = 0.5
0.36
0.60
0.67
0.24
0.44
0.48
−0.96
−0.99
−0.99
ρv = 0.9
0.31
1.24
2.47
0.51
0.80
0.87
−0.77
−0.98
−0.99
The statistics reported in table 7.1 seek to answer that question. First,
note that unemployment volatility, measured by the standard deviation
of the unemployment rate, increases with the degree of nominal wage
rigidities θw, for any given degree of persistence of the shock. Thus, other
things equal, more rigid wages imply more volatile unemployment. That
effect is particularly strong when the shock is more persistent.12
The second panel of table 7.1 displays the ﬁrst-order autocorrelation
of the unemployment rate, as a measure of persistence. Persistence is also
increasing in the degree of nominal wage rigidities (and, less surprisingly,
in the persistence of the shock). Note also that the autocorrelation
of unemployment always remains below the autocorrelation of the
shock process itself. Under the baseline calibration the persistence of
the unemployment rate is substantial (0.48), though still below the
persistence observed in the data.13 The latter is approximated, however,
when assuming ρv = 0.9. It is also interesting to note that for sufﬁciently
low values of ρv, the unemployment rate becomes negatively serially
correlated, a property inherited from employment.
Finally, the third panel of table 7.1 shows the correlation between
the unemployment rate and output, a measure of cyclicality. Like in
the data, that correlation is strongly negative for all calibrations. Thus,
the strong countercyclicality of unemployment in response of monetary
shocks seems to be a robust feature of the model, independently of the
degree of wage stickiness and the persistence of those shocks.
The simplicity of the underlying model notwithstanding, the above
ﬁndings suggest that a New Keynesian model with realistic levels of
nominal wage rigidities and persistence of monetary (or other demand
12 As discussed above, as θw →0 the volatility of unemployment converges to zero.
13 The autocorrelation of the (HP-detrended) unemployment rate is as high 0.90 in the
United States and 0.92 in the euro area. See Galí (2011b) for these and other labor market
statistics.

CHAPTER 7
shocks) can potentially generate unemployment ﬂuctuations with prop-
erties comparable to those observed in actual economies.
7.3.2 Optimal Monetary Policy
The economy’s behavior under the optimal policy can be represented
by equations (13), (14), (15), and (16) above, combined with the three
optimality conditions derived in chapter 6 and which are reproduced here
for convenience:

σ + ϕ + α
1 −α

yt + κpζ1,t + κwζ2,t = 0
(18)
ϵp
λp
π p
t −ζ1,t + ζ3,t = 0
(19)
ϵw(1 −α)
λw
πw
t −ζ2,t −ζ3,t = 0
(20)
λpζ1,t −λwζ2,t + ζ3,t −βEt{ζ3,t+1} = 0
(21)
for t = 0, 1, 2, ... where {ζ1,t}, {ζ2,t}, and {ζ3,t} denote the Lagrange
multipliers associated with the constraints of the optimal policy problem
(given by (13), (14), and (15) and (16) combined, respectively). Note that
the optimality conditions are identical to those derived in chapter 3 since
the slight reformulation of the households’ problem does not affect the
second order approximation to the welfare losses or the constraints of
the optimal policy problem.14
Figure 7.3 plots the responses of six macro variables (including the
unemployment rate) to a one percent positive technology shock under the
optimal policy (shown as a line with diamonds). The ﬁgure also shows
the corresponding responses under Taylor rule (17) (line with circles).
Both sets of responses assume that nonpolicy parameters are at their
baseline values.
Note that the optimal policy is more accommodative of the produc-
tivity improvement than the Taylor rule, with output increasing more,
and employment remaining largely unchanged (as opposed to declining,
14 See Galí (2011b) for details.

Output
Taylor rule
optimal
Unemployment
Employment
Labor force
Real wage
Price inflation
Figure 7.3. Optimal Policy vs. Taylor Rule: Technology Shocks.
as implied by the Taylor rule) under the optimal policy. Note also that
the response of those variables is very close to the efﬁcient one, which
involves a zero response of employment and participation and a one-
for-one adjustment of output to the change in technology under the
assumption made here that σ = 1.
The response of the unemployment rate is substantially different across
the two policies: it declines somewhat under the optimal policy, which
contrasts with the strong rise observed under the Taylor rule. Due to
the presence of rigidities in both prices and wages, the adjustment of
the real wage under the optimal policy is considerably muted relative to
its natural counterpart (which moves one-for-one with technology), but
is stronger than under the Taylor rule. This is due to a larger upward
adjustment of the nominal wage (facilitated by the lower unemployment
rate), despite a more muted deﬂation (associated with higher activity and,
hence, higher marginal costs, relative to the Taylor rule case).
Figure 7.4 displays the corresponding responses to a one percent
increase in the exogenous demand shifter, zt, under the optimal policy
and the Taylor rule. As discussed above, output, inﬂation, and all

CHAPTER 7
Output
Taylor rule
optimal
Unemployment
Employment
Labor force
–0.05
–0.15
Real wage
–0.01
Price inflation
Figure 7.4. Optimal Policy vs. Taylor Rule: Demand Shocks.
labor market variables are fully insulated from the shock under the
optimal policy. Only the nominal and real interest rates (not shown)
vary, responding one-for-one to the change in the natural rate. On the
other hand, under a Taylor rule the demand shock generates a persistent
increase in output and employment, a reduction in unemployment, and
positive inﬂation. In other words, the Taylor rule is not sufﬁciently
stabilizing in the face of demand shocks.
7.3.3 A Simple Interest Rate Rule with Unemployment
The explicit introduction of unemployment in the model makes it
possible to study the properties of simple interest rate rules that have
that variable as an argument. To illustrate that point, the equilibrium
of the New Keynesian economy developed above is analyzed under the
assumption that monetary policy is described by the simple rule:
it = 0.01 + 1.5π p
t −0.5
ut
(22)

Output
Taylor
simple
optimal
Unemployment
Employment
Labor force
Real wage
Price inflation
Figure 7.5. Optimal Policy vs. Simple Rule: Technology Shocks.
Galí (2011b) argues that such a rule provides a good account of the
Fed’s interest rate decisions during the 1987 to 2008 period, before
the federal funds rate hit the zero lower bound. In particular, the
empirical ﬁt of such a rule seems to improve on the standard Taylor
rule.
Figure 7.5 displays the responses of different macro variables to a one
percent positive innovation in technology under the above simple rule
(line with circles). The ﬁgure also show, for the sake of comparison, the
responses under both the optimal policy (line with diamonds) and the
Taylor rule (line with squares). Note that the responses to a technology
shock under simple rule (22) approximate pretty well the responses under
the optimal policy. For all variables considered the simple rule tracks
the optimal policy much better than the Taylor rule. A similar result
holds when demand shocks are the source of ﬂuctuations, as illustrated in
ﬁgure 7.6, which displays the responses to a positive demand shock under
the three rules.

CHAPTER 7
Output
Taylor
simple
optimal
Unemployment
Employment
Labor force
–0.05
–0.15
Real wage
–0.01
Price inflation
Figure 7.6. Optimal Policy vs. Simple Rule: Demand Shocks.
7.4 NOTES ON THE LITERATURE
The general approach to introducing unemployment in a macro model
underlying this chapter can be found in Galí (1996). The speciﬁc
application to the New Keynesian model was developed in Galí (2011a,
2011b) and, independently, in Casares (2010). Galí, Smets, and Wouters
(2012) use the same approach in order to introduce unemployment
in a version of Smets and Wouters’ (2003, 2007) medium-scale New
Keynesian model. Among other results, they show how the use of
unemployment data allows the separate identiﬁcation of wage markup
shocks and labor supply shocks, thus overcoming an earlier critique of
such models (Chari, Kehoe, and McGrattan (2009)).
Much of the literature on unemployment in the New Keynesian model
has followed an alternative approach, one that combines the nominal
rigidities that are the hallmark of the New Keynesian framework with
the labor market frictions of search and matching models (and which
are usually studied in the context of real models; see, e.g., Pissarides
(2000)). Walsh (2003, 2005) and Trigari (2009), which were among
the earliest contributions to that literature, analyzed the impact of

217
embedding labor market frictions into the basic New Keynesian model
with sticky prices but ﬂexible wages, with a focus on the size and
persistence of the effects of monetary policy shocks. Later contributions
have extended that work in two dimensions. Some have relaxed the
assumption of ﬂexible wages, and introduced different forms of nominal
and real wage rigidity. The work of Trigari (2006), Christoffel and
Linzert (2005), and Sveen and Weinke (2008) falls into that category.
Perhaps more interestingly, the focus of attention has gradually turned
to normative issues, and more speciﬁcally, to the implications of labor
market frictions and unemployment for the design of monetary policy.
See, For example the work of Blanchard and Galí (2010), Faia (2008,
2009), Ravenna and Walsh (2011), and Thomas (2008).15 Applications
using that approach to interpret U.S. postwar data include Gertler, Sala,
and Trigari (2008), who estimate a medium-scale New Keynesian model
with search and matching frictions, and Barnichon (2010), who examines
the model’s ability to account for the changing cyclical properties of labor
productivity.
Most of the work combining search and matching frictions with
nominal rigidities assumes some form of Nash bargaining of wages.
Wage stickiness is generally introduced by assuming that each period
only a fraction of ﬁrms engage in that bargaining with their workers
(Thomas (2008)), following the standard Calvo formalism. An alterna-
tive approach can be found in Christiano, Eichenbaum, and Trabandt
(2013), who embed the “alternating offers model” of Hall and Milgrom
(2008) in a New Keynesian model with search and matching frictions,
demonstrating its ability to generate endogenously a sluggish response of
aggregate nominal wages and a persistent response of unemployment to
various macro shocks.
Alternatives approaches include the work of Christiano, Trabandt,
and Walentin (2010), who have modiﬁed the New Keynesian model
by embedding in it an alternative model of unemployment, where
the probability of ﬁnding a job is increasing in search effort, and
where imperfect risk sharing among individuals is a consequence of the
unobservability of effort.
EXERCISES
7.1. Unemployment and monetary policy in a model with ﬂexible
prices
Consider a variation of the model developed in chapters 6 and 7,
with ﬁrms’ technology now being given by
Yt = Nt
where Nt is a CES function of the quantities hired of the different
types of labor. The elasticity of substitution among the latter is
ϵw. All ﬁrms reset their prices optimally each period (“ﬂexible
prices”). An optimal employment subsidy is assumed which
exactly offsets the monopolistic competition distortion in the
goods market.
a. Show that the dynamics of price inﬂation can be represented
by equation
π p
t = βEt{π p
t+1} −ϕλw(ut −un)
b. Taking the welfare loss function derived in chapter 6 as a
starting point, show that the welfare loss for the present
economy can be written (up to a multiplicative scalar) as
E0
∞

t=0
βk[αuu2
t + (π p
t )2]
where ut is the unemployment rate and π p
t ≡pt −pt−1 is price
inﬂation, and derive an expression for the weight αu as a
function of exogenous parameters.
c. Derive the optimal discretionary monetary policy and charac-
terize the implied equilibrium processes for unemployment and
price inﬂation. Show, in particular, that average price inﬂation
will be positive. Can you think of a way to eliminate that
inﬂationary bias?
d. Derive an interest rate rule that will guarantee the implemen-
tation of the optimal discretionary policy outcome.
e. Derive the optimal monetary policy under commitment and
characterize the implied equilibrium processes for unemploy-
ment and price inﬂation. Describe its main differences relative
to the optimal policy under discretion.

221
7.2. Wage inﬂation dynamics with wage markup and labor supply
shocks
Consider an extension of the model developed in the present chap-
ter in which labor disutility for household member ( j, s) is given
by χtsϕ, for all ( j, s) ∈[0, 1] × [0, 1], where ξt ≡log χt follows
an exogenous stationary stochastic process. In addition, a time-
varying elasticity of substitution between labor types is assumed,
{ϵw,t}, implying a variable desired wage markup µw
t ≡log
ϵw,t
ϵw,t−1.
a. Derive the equation describing wage inﬂation dynamics as a
function of the real wage, consumption, and employment, and
show how the two disturbances ξt and µw
t enter its error term
in a symmetric way thus creating an identiﬁcation problem
in attempts to estimate the model (remark: this is the basis
for the Chari, Kehoe, and McGrattan (2009) critique of New
Keynesian models).
b. Discuss how the reformulation of the wage equation in
terms of the unemployment rate overcomes the previous
shortcoming.
7.3. Taming the wealth effect on labor supply
Consider a modiﬁcation of the model developed in the present
chapter in which individual utility for household member
( j, s) ∈[0, 1] × [0, 1] is assumed to be given by:
log Ct( j, s) −1t( j, s)χtsϕ
where 1t( j, s) is an indicator function taking a value equal to one
if individual ( j, s) is employed in period t, and zero otherwise, and
t ≡Zt
Ct
where Ct denotes aggregate consumption, and Zt evolves over
time according to the difference equation
Zt = Z1−υ
t−1 Ct
υ
where υ
∈
[0, 1]. Full risk sharing of consumption among
household members is assumed.

CHAPTER 7
a. Show that the household’s period utility, deﬁned as the integral
over its members’ utilities, is given by:
log Ct −χtt
 1
0
Nt( j)1+ϕ
1 + ϕ
dj
where Nt( j) ∈[0, 1] denotes the employment rate in period t
among workers specialized in type j labor.
b. Derive the aggregate participation equation, and discuss how
υ will affect the response of the labor force to different shocks.