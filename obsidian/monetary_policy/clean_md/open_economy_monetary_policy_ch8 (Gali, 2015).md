Chapter 8
MONETARY POLICY IN THE OPEN ECONOMY
All the models analyzed in earlier chapters assumed a closed economy:
households and ﬁrms were not able to trade in goods or ﬁnancial
assets with agents located in other economies. This chapter relaxes
that assumption by developing an open economy extension of the basic
New Keynesian model analyzed in chapter 3. The framework introduces
explicitly the exchange rate, the terms of trade, exports and imports, as
well as international ﬁnancial markets. Such a framework can in principle
be used to assess the implications of alternative monetary policy rules in
an open economy. Because the framework nests as a limiting case the
closed economy model of chapter 3, it allows one to assess the extent
to which the opening of the economy affects some of the conclusions
regarding monetary policy obtained for the closed economy and, in
particular, the desirability of a policy that seeks to stabilize inﬂation (see
chapter 4). It is also worth analyzing what role, if any, the exchange rate
plays in the optimal design of monetary policy. Finally, the framework
can be used to determine the implications of alternative simple rules, as
was done in chapter 4 for the closed economy.
The analysis of a monetary open economy raises a number of issues
that a modeler needs to confront. First, a choice needs to be made
between the modeling of a “large” or a “small” economy, that is,
between allowing or not, respectively, for repercussions in the rest of
the world of developments (including policy decisions) in the economy
being modeled. Second, the existence of two or more economies subject
to imperfectly correlated shocks makes room for cross-border trade in
assets, for risk sharing purposes and/or in order to smooth consumption
over time. Hence, a decision must be made regarding the nature of
international asset markets and, more speciﬁcally, the set of securities
that can be traded in those markets, with possible assumptions ranging
from ﬁnancial autarky to complete markets. Third, one needs to make
some assumption about ﬁrms’ ability to discriminate across countries in
the price they charge for the goods they produce (“pricing to market”
versus “law of one price”). Furthermore, whenever discrimination is
possible and prices are not readjusted continuously, an assumption must
be made regarding the currency in which the prices of exported goods
are set (“local currency pricing,” i.e., prices are set in the currency of the

224
CHAPTER 8
importing economy versus “producer currency pricing,” i.e., prices are
set in the currency of the producer’s country). Other dimensions of open
economy modeling that require some choices include the allowance or
not for nontradable goods, the existence of trading costs, the possibility
of international policy coordination, and so on.
A comprehensive analysis of the range of possible modeling dimensions
and how alternative assumptions may affect the design of monetary
policy would require a book of its own, thus it is clearly beyond the
scope of this chapter. The modest objective here is to present an example
of a monetary open economy model to illustrate some of the issues that
emerge in the analysis of such economies and which are absent in their
closed economy counterparts. In particular, the small open economy
model developed below assumes complete international ﬁnancial markets
as well as the law of one price. Then, in the discussion of the model’s
policy implications and in the notes on the literature at the end of the
chapter, reference is made to a number of papers that adopt different
assumptions, and the extent to which their ﬁndings differ from those
obtained here is brieﬂy discussed.
The framework developed below is a simpliﬁed version of the one
in Galí and Monacelli (2005). In order to focus on the issues brought
about by the openness of the economy, the presence of either cost-
push shocks or nominal wage rigidities is ignored. The assumptions
on preferences and technology, combined with a Calvo price-setting
structure and the assumption of complete ﬁnancial markets, give rise
to a highly tractable model and to simple and intuitive log-linearized
equilibrium conditions. The latter can be reduced to a two-equation
dynamical system consisting of a New Keynesian Phillips curve and a
dynamic IS-type equation, whose form is identical to the system derived
in chapter 3 for the closed economy, though its coefﬁcients depend on
parameters that are speciﬁc to the open economy while the driving forces
are a function of world variables (that are taken as exogenous to the
small open economy). As in its closed economy counterpart, the two
equations must be complemented with a description of how monetary
policy is conducted.
After describing the model and deriving a simple representation
of its equilibrium dynamics, section 8.3 analyzes the transmission of
monetary policy shocks, emphasizing the role played by openness in
that transmission. Section 8.4 turns to the issue of optimal monetary
policy design, focusing on a particular case for which the ﬂexible price
allocation is efﬁcient. Under the same assumptions one can derive a
second-order approximation to the consumer’s utility, which can be used
to evaluate alternative policy rules. Section 8.5 assesses the merits of
alternative simple monetary policy rules, including an exchange rate peg.

POLICY IN THE OPEN ECONOMY
225
Section 8.6 concludes with a brief note on the related literature.
8.1 A SMALL OPEN ECONOMY MODEL
The economy is modeled as being inﬁnitesimally small (relative to the
world economy), with its performance not having any impact on the rest
of the world. Next, the problem facing households and ﬁrms located in
one such economy is described in detail.
8.1.1 Households
The small open economy is inhabited by a representative household
seeking to maximize
E0
∞

t=0
βtU(Ct, Nt; Zt)
(1)
where Nt denotes employment (or work hours), Ct is a composite
consumption index deﬁned by1
Ct ≡

(1 −υ)
1
η CH,t
1−1
η + υ
1
η CF,t
1−1
η

η
η−1
(2)
and CH,t is an index of consumption of domestic goods given by the
constant elasticity of consumption (CES) function
CH,t ≡
 1
0
CH,t(i)
ϵ−1
ϵ di

ϵ
ϵ−1
where i ∈[0, 1] denotes the good variety. CF,t denotes the quantity
of imported goods consumed. Zt is an exogenous preference shifter.
Parameter ϵ > 1 denotes the elasticity of substitution between varieties
produced domestically. Parameter υ ∈[0, 1] can be interpreted as a
measure of openness. Parameter η > 0 measures the substitutability
between domestic and foreign goods.
1 As η →1 the consumption index is given by
Ct =
1
(1 −υ)(1−υ)υυ CH,t1−υCF,tυ

226
CHAPTER 8
Maximization of (1) is subject to a sequence of budget constraints of
the form
 1
0
PH,t(i)CH,t(i)di + PF,tCF,t + Et{Qt,t+1Dt+1} ≤Dt + WtNt
(3)
for t = 0, 1, 2, ... PH,t(i) is the price of domestic variety i ∈[0, 1]. PF,t is
the price of imported goods. Dt+1 is the nominal payoff in period t + 1
of the portfolio held at the end of period t (possibly including shares in
ﬁrms), Wt is the nominal wage. The previous variables are all expressed
in units of domestic currency. Qt,t+1 is the stochastic discount factor
for one-period-ahead nominal payoffs (to be derived below). Households
have access to a complete set of contingent claims, traded internationally.
As in the closed economy, the optimal allocation across varieties of
any given expenditure on domestic goods yields the demand functions
CH,t(i) =
 PH,t(i)
PH,t
−ϵ
CH,t
(4)
for all i ∈[0, 1], where PH,t ≡
	 1
0 PH,t(i)1−ϵdi

1
1−ϵ is the domestic
price index (i.e., an index of prices of domestically produced goods).
Combining (4) with the deﬁnitions of PH,t and CH,t yields the convenient
result
	 1
0 PH,t(i)CH,t(i) di = PH,tCH,t.
On the other hand, the optimal allocation of expenditures between
domestic and imported goods is given by
CH,t = (1 −υ)
 PH,t
Pt
−η
Ct
;
CF,t = υ
 PF,t
Pt
−η
Ct
(5)
where Pt ≡

(1 −υ)(PH,t)1−η + υ(PF,t)1−η

1
1−η is the consumer price
index (CPI).2 Note that under the assumption of η = 1 or, alternatively,
when the price indexes for domestic and foreign goods are equal (as in
the steady state described below), parameter υ corresponds to the share
of consumption expenditures allocated to imported goods.
Using (5) and the deﬁnitions of indexes Ct and Pt it can be shown
that total consumption expenditures by domestic households can be
2 In the particular case of η = 1, the CPI takes the form
Pt = (PH,t)1−υ(PF,t)υ
.

POLICY IN THE OPEN ECONOMY
227
conveniently expressed as PH,tCH,t + PF,tCF,t = PtCt. Thus, the period
budget constraint simpliﬁes to
PtCt + Et{Qt,t+1 Dt+1} ≤Dt + WtNt
(6)
As in chapter 3, the period utility function is specialized to be of the
form
U(Ct, Nt; Zt) =














C1−σ
t
−1
1 −σ
−N1+ϕ
t
1 + ϕ

Zt
for σ ̸= 1

log Ct −N1+ϕ
t
1 + ϕ

Zt
for σ = 1
with zt ≡log Zt following an exogenous AR(1) process
zt = ρzzt−1 + εz
t
where ρz ∈[0, 1).
Under the assumption of perfectly competitive labor markets (which
is maintained throughout this chapter), the intratemporal optimality
condition for the household’s problem takes the same form as in the
closed economy model of chapter 3, namely:
Cσ
t Nϕ
t = Wt
Pt
(7)
In order to derive the relevant intertemporal optimality condition note
that the following relation must hold for the optimizing household in the
small open economy
Vt,t+1
Pt
ZtC−σ
t
= ξt,t+1βZt+1C−σ
t+1
1
Pt+1
(8)
where Vt,t+1 is the period t price (in domestic currency) of an Arrow
security, that is, a one-period security that yields one unit of domestic
currency if a speciﬁc state of nature is realized in period t + 1, and
nothing otherwise, and where ξt,t+1 is the probability of that state of
nature being realized in t+1 (conditional on the state of nature at t). Ct+1,
Zt+1, and Pt+1 on the right side should be interpreted as representing
the values taken by those variables at t + 1 conditional on the state of

228
CHAPTER 8
nature in which the Arrow security generates a payoff. Thus, the left
side captures the utility loss resulting from the purchase of an Arrow
security considered (with the corresponding reduction in consumption),
whereas the right side measures the expected one-period-ahead utility
gain from the additional consumption made possible by the (eventual)
security payoff. If the consumer is optimizing the expected utility gain, it
must exactly offset the current utility loss.
The price of the nominal Arrow security introduced above must satisfy
Vt,t+1 = ξt,t+1Qt,t+1. Thus, (8) can be rewritten as3
β
Ct+1
Ct
−σ  Zt+1
Zt
  Pt
Pt+1

= Qt,t+1
(9)
which is assumed to be satisﬁed for all possible states of nature at t and
t + 1.
Taking conditional expectations on both sides of (9) and rearranging
terms, a conventional stochastic Euler equation can be derived
Qt = βEt
Ct+1
Ct
−σ  Zt+1
Zt
  Pt
Pt+1

(10)
where Qt ≡Et{Qt,t+1} denotes the price of a one-period discount bond
paying off one unit of domestic currency in all states at t + 1.
Equations (7) and (9) can be respectively written in log-linearized
form as
wt −pt = σct + ϕnt
ct = Et{ct+1} −1
σ (it −Et{πt+1} −ρ) + 1
σ (1 −ρz)zt
(11)
where lowercase letters denote the logs of the respective variables, it ≡
−log Qt is the short-term nominal rate, ρ ≡−log β is the time discount
rate, and πt ≡pt −pt−1 is CPI inﬂation (with pt ≡log Pt).
3 Note that under complete markets a simple no room for arbitrage argument implies
that the price of a one-period asset (or portfolio) yielding a random payoff Dt+1 must be
given by  Vt,t+1Dt+1 where the sum is over all possible states at t + 1. Equivalently, that
price can be written as Et
 Vt,t+1
ξt,t+1 Dt+1

. Thus, the one-period stochastic discount factor
can be deﬁned as Qt,t+1 ≡Vt,t+1
ξt,t+1 .

POLICY IN THE OPEN ECONOMY
229
8.1.1.1 DOMESTIC INFLATION, CPI INFLATION, THE REAL EXCHANGE RATE,
AND THE TERMS OF TRADE: SOME IDENTITIES
Next, several assumptions and deﬁnitions are introduced, and a number
of identities are derived that are extensively used below. The terms of
trade, denoted by St, is deﬁned as the price of foreign goods relative to
domestic goods. Formally,
St ≡PF,t
PH,t
or, in logs, st ≡log St = pF,t −pH,t.
Log-linearization of the CPI index around a symmetric steady state
with S = 1 yields the following approximate relation between consumer
prices, domestic prices and the terms of trade.4
pt = (1 −υ)pH,t + υpF,t
= pH,t + υst
(12)
It follows that domestic inﬂation, deﬁned as the rate of change in the
index of domestic goods prices, that is, πH,t ≡pH,t −pH,t−1, and CPI
inﬂation, are linked according to the relation
πt = πH,t + υ
st
(13)
that is, the gap between the two measures of inﬂation is proportional
to the percentage change in the terms of trade, with the coefﬁcient of
proportionality given by the openness index υ.
It is assumed that the law of one price holds for individual goods at
all times (both for import and export prices). In particular, PF,t = Et P∗
t ,
where Et is the nominal exchange rate (deﬁned as the price of foreign
currency in terms of domestic currency), and P∗
t is the price of foreign
goods expressed in foreign currency. P∗
t can also be interpreted as a
world price index, given that the size of the small open economy is
assumed to be negligible relative to the rest of the world. On the same
grounds, for the world as a whole there is no distinction between CPI
and domestic price level.
4 It is useful to note, for future reference, that the approximation (12) holds exactly
when η = 1.

230
CHAPTER 8
The assumed law of one price, combined with the deﬁnition of the
terms of trade, implies
st = et + p∗
t −pH,t
(14)
where et ≡Et.
The real exchange rate is deﬁned as the ratio of world and domestic
CPI’s, both expressed in domestic currency
Qt ≡PF,t
Pt
Thus, in logs:
qt = pF,t −pt
= st + pH,t −pt
= (1 −υ)st
where the last equality holds exactly if η = 1, but only up to a ﬁrst-order
approximation when η ̸= 1.
8.1.1.2 INTERNATIONAL RISK SHARING
Under the assumption of a complete set of state-contingent securities
traded internationally, a condition analogous to (8) must also hold for
households in the rest of the world. Assuming a utility function identical
to that of domestic households this condition takes the form:
Vt,t+1
Et P∗t
(C∗
t )−σ = ξt,t+1β(C∗
t+1)−σ
1
Et+1P∗
t+1
where C∗
t denotes (per capita) consumption by foreign households. The
presence of the exchange rate terms reﬂects the fact that the Arrow
security considered has a price Vt,t+1 and a unit payoff expressed in the
currency of the small open economy. For simplicity, it is assumed that
foreign households are not subject to preference shocks.
The previous relation can be written in terms of our small open
economy’s stochastic discount factor as
β
C∗
t+1
C∗t
−σ  P∗
t
P∗
t+1
  Et
Et+1

= Qt,t+1
(15)

POLICY IN THE OPEN ECONOMY
231
Combining (9) and (15), together with the deﬁnition of the real
exchange rate and the law of one price, yields
Ct = ϑC∗
t Z
1
σt Q
1
σt
(16)
for all t, and where ϑ is a constant which will generally depend on initial
conditions regarding relative net asset positions. Henceforth, and without
loss of generality, symmetric initial conditions are assumed (i.e., zero net
foreign asset holdings and an ex-ante identical environment), implying
ϑ = 1.
Under the assumption that the small economy has an inﬁnitesimal size
relative to the rest of the world, C∗
t = Y∗
t for all t, where Y∗
t denotes
world output (expressed in per capita terms). Imposing that condition on
(16) and taking logs,
ct = y∗
t + 1
σ (zt + qt)
(17)
= y∗
t + 1
σ zt +
1 −υ
σ

st
where the second equality holds only up to a ﬁrst-order approximation
when η ̸= 1. Thus, the assumption of a complete market for state-
contingent securities at the international level leads to a simple relation-
ship linking domestic consumption with world output and the terms of
trade.
8.1.1.3 A BRIEF DETOUR: UNCOVERED INTEREST PARITY AND THE
TERMS OF TRADE
Under the assumption of complete international ﬁnancial markets, the
equilibrium price (in terms of the small open economy’s domestic
currency) of a bond which pays one unit of foreign currency is given
by EtQ∗
t = Et{Qt,t+1Et+1}, where Q∗
t is the price of the bond in terms of
foreign currency. The previous pricing equation can be combined with
the domestic bond pricing equation, Qt = Et{Qt,t+1} to obtain a version
of the uncovered interest parity condition
Et{Qt,t+1[exp{it} −exp{i∗
t }(Et+1/Et)]} = 0

232
CHAPTER 8
Log-linearizing around a perfect foresight steady state yields the
familiar uncovered interest parity condition:
it = i∗
t + Et{
et+1}
(18)
Combining (14) and (18) yields the stochastic difference equation
st = (i∗
t −Et{π∗
t+1}) −(it −Et{πH,t+1}) + Et{st+1}
(19)
In a symmetric steady state the terms of trade take a unit value, that
is, S = 1. That fact, combined with the assumption of stationarity in the
model’s driving forces, implies that limT→∞Et{sT} = 0.5 Hence, (19) can
be solved forward to obtain
st = Et
 ∞

k=0
[(i∗
t+k −π∗
t+k+1) −(it+k −πH,t+k+1)]

(20)
that is, the terms of trade are a function of current and anticipated real
interest rate differentials.
It must be pointed out that while equations (19) and (20) provide a
convenient (and intuitive) way of representing the connection between
terms of trade and interest rate differentials, they do not constitute an
additional independent equilibrium condition. In particular, it is easy
to check that (19) can be derived by combining the consumption Euler
equations for both the domestic and world economies with the risk
sharing condition (17) and equation (13).
Next, attention is turned to the supply side of the economy.
8.1.2 Firms
8.1.2.1 TECHNOLOGY
A typical ﬁrm in the home economy produces a differentiated good with
a technology represented by the production function
Yt(i) = AtNt(i)1−α
5 The assumption regarding the steady state implies that the real interest rate differential
will revert to a zero mean. More generally, the real interest rate differential will revert to a
constant mean, as long as the terms of trade are stationary in ﬁrst differences. That would
be the case if, say, the technology parameter had a different average rate of growth relative
to the rest of the world.

POLICY IN THE OPEN ECONOMY
233
where at ≡log At is a technology shifter common to all domestic ﬁrms
following the AR(1) process at = ρaat−1 + εa
t .
8.1.2.2 PRICE SETTING
As in the basic model of chapter 3, it is assumed that domestic ﬁrms set
prices in a staggered fashion. In particular, a measure 1 −θ of (randomly
selected) ﬁrms sets new prices each period, with an individual ﬁrm’s
probability of reoptimizing in any given period being independent of the
time elapsed since it last reset its price. As shown in chapter 3, the optimal
price-setting strategy for the typical ﬁrm resetting its price in period t can
be approximated by the (log-linear) rule
pH,t = µ + (1 −βθ)
∞

k=0
(βθ)kEt{ψt+k|t}
(21)
where pH,t denotes the price newly set by domestic ﬁrms (in logs), ψt+k|t
is the (log) nominal marginal cost in period t + k for a ﬁrm last resetting
its price in period t, and µ ≡log
ϵ
ϵ−1 is the log of the (gross) steady state
markup.6
As shown in chapter 3, the previous optimal price setting condition can
be combined with an equation describing the evolution of the domestic
price level, together with a relation linking the conditional marginal cost
ψt+k|t to the average marginal cost ψt+k, to yield the following domestic
inﬂation equation:
πH,t = βEt{πH,t+1} −λµt
(22)
where µt ≡pH,t −ψt+k −µ is the markup gap, and
λ ≡
(1 −θ)(1 −βθ)
θ


where  ≡
1−α
1−α+αϵ ∈[0, 1].
Thus, it can be seen that in the open economy the relation between
domestic price inﬂation and the markup gap is not affected by the degree
of openness on the substitutability between domestic and foreign goods.
6 pH,t is used to denote newly set prices instead of p∗
t (used in chapter 3), because in this
chapter letters with an asterisk refer to world economy variables.

234
CHAPTER 8
8.1.3 Exports
The demand for exports of good i ∈[0, 1] is assumed to be given by
Xt(i) =
 PH,t(i)
PH,t
−ϵ
Xt
where Xt ≡
	 1
0 Xt(i)
ϵ−1
ϵ di

ϵ
ϵ−1 is an index of aggregate exports from the
small open economy to the rest of the world. Aggregate exports are, in
turn, assumed to be given by
Xt = υ
 PH,t
Et P∗t
−η
Y∗
t
= υSηY∗
t
The previous results hold under the assumption that the preferences
of households in the rest of the world are identical to those of domestic
households, combined with the fact that global goods market clearing
implies C∗
t
= Y∗
t .7 Thus, in the symmetric steady state with S = 1,
X(i) = X = υY∗, for all i ∈[0, 1]. Moreover, given that in that steady
state CF = υC, and that C = Y∗(from the risk sharing condition) it
follows that trade is balanced at the symmetric steady state.
8.2 EQUILIBRIUM
8.2.1 Aggregate Demand and Output Determination
8.2.1.1 CONSUMPTION AND OUTPUT IN THE SMALL OPEN ECONOMY
Goods market clearing in the home economy requires
Yt(i) = CH,t(i) + Xt(i)
(23)
=
 PH,t(i)
PH,t
−ϵ 
(1 −υ)
 PH,t
Pt
−η
Ct + υSηY∗
t

for all i ∈[0, 1] and all t.
7 See Galí and Monacelli (2005) for a more careful derivation, under the assumption
that the world is made up of a continuum of small economies like the one analyzed here.

POLICY IN THE OPEN ECONOMY
235
Plugging (23) into the deﬁnition of aggregate domestic output Yt ≡
	 1
0 Yt(i)1−1
ϵ di

ϵ
ϵ−1 yields
Yt = (1 −υ)
 PH,t
Pt
−η
Ct + υSη
t Y∗
t
(24)
which can be approximated around the symmetric steady state as
yt = (1 −υ)ct + υ(2 −υ)ηst + υy∗
t
(25)
Finally, combining (13) with the Euler equation (11) gives
ct = Et{ct+1} −1
σ (it −Et{πH,t+1} −ρ) + υ
σ Et{
st+1} + 1
σ (1 −ρz)zt (26)
Note that (17) and (25) can be combined to derive the following
expression for the terms of trade:
st = συ(yt −y∗
t ) −(1 −υ)zt
(27)
where συ ≡σ > 0 with  ≡
1
1+υ(ϖ−1)
> 0 and where ϖ
≡
ση + (1 −υ) (ση −1).
Finally, combining (25), (26), and (27) yields (after some algebra)
a version of the dynamic IS equation for the small open economy:
yt = Et{yt+1} −1
συ
(it −Et{πH,t+1} −ρ) + υ(ϖ −1)Et{
y∗
t+1}
+1 −v
σ
(1 −ρz)zt
(28)
Note that, in general, the degree of openness inﬂuences the sensitivity
of output to a change in the domestic real interest rate it −Et{πH,t+1}, as
measured by 1/συ. In particular, if ση > 1 an increase in openness raises
that sensitivity, since συ is decreasing in υ under that assumption.
As its closed economy counterpart, equation (28) can be rewritten in
terms of the output and real interest rate gaps as:
yt = Et{yt+1} −1
συ
(it −Et{πH,t+1} −rn
t )
(29)
where
rn
t = ρ + συ Et{
yn
t+1} + συυ(ϖ −1)Et{
y∗
t+1} + (1 −v)(1 −ρz)zt (30)

236
CHAPTER 8
is the natural interest rate, with yn
t denoting the natural level of output,
determined below.
Thus, it is seen that the small open economy’s equilibrium is charac-
terized by a forward-looking dynamic IS-type equation similar to that
found in the closed economy. Nevertheless, two differences are worth
pointing out. First, the degree of openness inﬂuences the sensitivity of the
output gap to interest rate changes. Second, openness generally makes
the natural interest rate depend on expected world output growth, in
addition to domestic shocks (also because, as shown below, the natural
level of output will generally depend on world output).
8.2.1.2 THE TRADE BALANCE
Let nxt ≡
 1
Y
 
Yt −
Pt
PH,t Ct

denote net exports in terms of domestic
output, expressed as a fraction of steady state output Y. Note that under
the assumptions made above trade is balanced in the steady state. A ﬁrst-
order approximation around that steady state yields nxt = yt −ct −υst,
which combined with (17) and (25) implies a simple relation between net
exports and the terms of trade
nxt = υ
ϖ
σ −1

st −υ
σ zt
(31)
Note that, given the terms of trade, a positive preference shock induces
a trade deﬁcit in the small open economy. In the special case of σ =
η = 1, net exports are invariant to changes in the terms of trade: the
latter’s price effects on the trade balance exactly offset its quantity effects
in that case. More generally, the sign of the relationship between the
terms of trade and net exports is ambiguous, depending on the relative
sizes of υ, σ, and η. If υ and/or η are sufﬁciently large, a term of trade
depreciation (i.e., an increase in st) will improve the trade balance.
8.2.2 The Supply Side: Marginal Cost and Inﬂation Dynamics
8.2.2.1 AGGREGATE OUTPUT AND EMPLOYMENT
As in chapter 3, one can derive an approximate aggregate production
function relating aggregate domestic output to aggregate employment.
Notice that equilibrium in the labor market requires
Nt ≡
 1
0
Nt(i)di =
 Yt
At

1
1−α  1
0
 PH,t(i)
PH,t
−
ϵ
1−α
di

POLICY IN THE OPEN ECONOMY
237
As shown in chapter 3, however, variations in dt ≡log
	 1
0

PH,t(i)
PH,t
−ϵ
di
around the perfect foresight steady state are of second order. Thus, and
up to a ﬁrst-order approximation, the following relationship between
(log) aggregate output and (log) aggregate employment holds
yt = at + (1 −α)nt
(32)
8.2.2.2 MARKUPS AND INFLATION DYNAMICS IN
THE SMALL OPEN ECONOMY
Next a relation between the average price markup and domestic output is
derived. That relation differs somewhat from that in the closed economy,
due to the existence of a wedge between output and consumption, and
between domestic and consumer prices. Thus, in the present model (and
ignoring constant terms),
µt = pH,t −(wt −at + αnt)
= −(wt −pt) −(pt −pH,t) + at −αnt
= −(σct + ϕnt) −υst + at −αnt
= −

σ + ϕ + α
1 −α

yt + υ(ϖ −1)st +

1 + ϕ + α
1 −α

at −υzt
(33)
where the last equality makes use of (17), (25), and (32). Note that, in
addition to domestic output and technology, the average markup is a
function of the terms of trade and the preference shifter zt. This is due to
the inﬂuence of both variables on the real wage through an income effect
on labor supply resulting from their impact on domestic consumption. In
addition, changes in the terms of trade have a direct effect, captured by
the term υst, on the product wage, for any given consumption wage. The
inﬂuence of technology (through its direct effect on labor productivity)
and of domestic output (through its effect on employment and, hence, on
the real wage for a given output level) is analogous to that observed in
the closed economy.
Combining (33) with (22) (and ignoring constant terms) yields a
version of the New Keynesian Phillips curve for the small open economy:
πH,t = βEt{πH,t+1}+κyt−λυ(ϖ −1)st−λ

1 + ϕ + α
1 −α

at+λυzt
(34)
where κ ≡λ

σ + ϕ+α
1−α

, as in the closed economy model of chapter 3.

238
CHAPTER 8
Next it is shown how a version of the New Keynesian Phillips
curve linking domestic inﬂation and the output gap can be derived.
Evaluating (33) at the ﬂexible price equilibrium and subtracting the
resulting expression yields:
µt = −

σ + ϕ + α
1 −α

yt + υ(ϖ −1)st
where yt ≡yt −yn
t and st ≡st −sn
t denote the output gap and the terms
of trade gap, respectively, where the natural level of output is given by
yn
t = aat + zzt + ∗y∗
t
(35)
with a ≡
1+ϕ
συ(1−α)+ϕ+α > 0, ∗≡−υ(ϖ−1)συ(1−α)
συ(1−α)+ϕ+α and z ≡−
υϖ(1−α)
συ(1−α)+ϕ+α
and where the natural terms of trade can be determined using (27):
sn
t = συ(yn
t −y∗
t ) −(1 −υ)zt
Note that the sign of the effect on the domestic natural output of
changes in world output and preference shock is ambiguous. In the
particular case of σ = η = 1, however, world output has no effect on
the domestic natural output (∗= 0), while preference shocks zt have
a negative effect (z < 0). The latter effect of preference shocks was
absent in the closed economy,8 and is a consequence of the increase in
consumption implied by risk sharing with the rest of the world.
Using the fact that st = συyt (as implied by (27)), the following simple
relation between the average markup and the output gap can be derived:
µt = −

συ + ϕ + α
1 −α

yt
(36)
where yt ≡yt −yn
t . Plugging (36) into (22) yields a version of a
New Keynesian Phillips curve of identical form as its closed economy
counterpart derived in chapter 3:
πH,t = βEt{πH,t+1} + κυyt
(37)
where κυ ≡λ

συ + ϕ+α
1−α

. For υ = 0 (or, alternatively, σ = η = 1)
the slope coefﬁcient is given by λ

σ + ϕ+α
1−α

≡κ, as in the basic closed
8 Note that z = 0 when υ = 0.

POLICY IN THE OPEN ECONOMY
239
economy model of chapter 3. More generally, the degree of openness,
υ, and the substitutability between domestic and foreign goods, η, affect
the dynamics of inﬂation through their inﬂuence on the slope coefﬁcient
κυ, which determines the inﬂation response to variations in (current and
future) output gaps. In particular, if ση > 1 (and, hence, ϖ > 1),
an increase in openness lowers συ, reducing the sensitivity of domestic
inﬂation to the output gap due to the smaller effect of the latter on the
average markup, as discussed above.
Finally, note that by combining (30) with (35) a closed form expression
for the natural rate of interest can now be derived
rn
t ≡ρ −συa(1 −ρa)at + ∗Et{
y∗
t+1} + z(1 −ρz)zt
(38)
is the small open economy’s natural rate of interest, with ∗
≡
συ (υ(ϖ −1) + ∗) and z ≡(1 −υ) −συz. Note that limυ→0 ∗= 0
and limυ→0 z = 1.
8.3 EQUILIBRIUM DYNAMICS UNDER AN INTEREST RATE RULE
In the previous two sections the equilibrium conditions making up the
nonpolicy block of the small open economy model have been derived.
Those conditions take the form of a set of equations involving all the
relevant endogenous variables, with technology and preference shocks as
driving forces. As in previous chapters, in order to close the model, that
set of equations has to be supplemented with a description of monetary
policy.
As an illustration, the present section characterizes the model’s equilib-
rium under the assumption that the monetary authority follows a Taylor-
type interest rate rule similar to the one introduced in chapter 3, namely
it = ρ + φππH,t + φyyt + vt
(39)
where φπ and φy are non-negative coefﬁcients chosen by the monetary
authority, and where vt is an exogenous monetary policy shock that
evolves according to the AR(1) process:
vt = ρvvt−1 + εv
t
where ρv ∈[0, 1).
Combining (29), (37), and (39), the equilibrium dynamics for the
output gap and domestic inﬂation can be represented by means of the

240
CHAPTER 8
system of difference equations

yt
πH,t

= Aυ

Et{yt+1}
Et{πH,t+1}

+ Bυut
(40)
where
ut ≡rn
t −φyyn
t −vt
and
Aυ ≡υ

συ
1 −βφπ
συκυ
κυ + β(συ + φy)

;
Bυ ≡υ

1
κυ

with υ ≡
1
συ+φy+κυφπ . The previous system has the same form as the one
analyzed in chapter 3 for the closed economy, with the only difference
lying in the fact that some of the coefﬁcients are a function of the “open
economy parameters” υ and η, and that yn
t and rn
t are now given by (35)
and (38), respectively. In particular, the condition for a locally unique
stationary equilibrium under rule (39) takes the same form as the one
introduced in chapter 3, namely
κυ(φπ −1) + (1 −β)φy > 0
(41)
which is assumed to hold for the remainder of this section. Once the
equilibrium path for the output gap and inﬂation has been determined,
one can use the various equilibrium relations derived in the previous
two sections to determine the corresponding equilibrium values for the
remaining variables of interest.
The previous framework is used below to examine the economy’s
response to an exogenous monetary policy shock, that is, an exogenous
change in vt. Given the isomorphism with the closed economy model of
chapter 3, many of the results derived there can be exploited. The analysis
of the effects of a technology shock, a preference shock, or a change in
world output is not pursued here, but an identical approach can be used:
First, one should determine the implications of the shock considered for
rn
t and yn
t , and then proceed to solve for the equilibrium response of the
output gap and domestic inﬂation exactly as done next for the case of a
monetary policy shock.9
9 Of course, as in chapter 3, it must be taken into account that a technology shock or a
shock to world output also leads to a variation in the natural output level, thus breaking
the identity between output and the output gap.

POLICY IN THE OPEN ECONOMY
241
8.3.1 The Effects of a Monetary Policy Shock
Neither the natural rate of interest nor the natural level of output are
affected by a monetary policy shock, so rn
t = yn
t = 0 for all t for the
purposes of this exercise. As in chapter 3, let us guess that the solution
takes the form yt = ψyvvt and πt = ψπvvt, where ψyv and ψπv are
coefﬁcients to be determined. Imposing the guessed solution on (40) and
using the method of undetermined coefﬁcients,
yt = −(1 −βρv)vvt
and
πH,t = −κυvvt
where v ≡
1
(1−βρv)[συ(1−ρv)+φy]+κυ(φπ−ρv). It can be easily shown that as
long as (41) is satisﬁed, v > 0. Hence, as in the closed economy, an
exogenous increase in the interest rate leads to a persistent decline in
output and domestic inﬂation. The size of the effect of the shock relative
to the closed economy benchmark depends on the values taken by a
number of parameters. More speciﬁcally, if ση > 1 then v can be
shown to be increasing in the degree of openness, thus implying that a
given monetary policy shock will have a larger impact in the small open
economy than in its closed economy counterpart.
Using interest rate rule (39), the response of the nominal rate can be
determined, taking into account the central bank’s endogenous reaction
to changes in inﬂation and the output gap
it = ρ +

1 −v(φπκυ + φy(1 −βρv))

vt
Note that as in the closed economy model, the full response of the
nominal rate may be positive or negative, depending on parameter values.
The response of the real interest rate (expressed in terms of domestic
goods) is given by
rt = it −Et{πH,t+1}
= ρ +

1 −v((φπ −ρv)κυ + φy(1 −βρv))

vt
Thus the real rate increases unambiguously when vt rises, because the
term in square brackets is always positive.
Using (27), the response of the terms of trade to the monetary policy
shock can then be uncovered
st = συ yt
= −συ(1 −βρv)vvt

242
CHAPTER 8
while the change in the nominal exchange rate is given in turn by

et = 
st + πH,t
= −v[συ(1 −βρv) + κυ]vt + συ(1 −βρv)vvt−1
Thus, a tightening of monetary policy leads to a persistent improve-
ment in the terms of trade (i.e., a decrease in the relative price of
foreign goods) as well as a nominal exchange rate appreciation, both
in the short run and in the long run. To understand the long-run
effect, note that the terms of trade revert back to their original level in
response to the monetary policy shock, which requires that the nominal
exchange rate appreciate by the same amount as the permanent decrease
in domestic price level, which is given by κυv
1−ρv (given an initial shock of
size normalized to unity). Hence, the exchange rate will overshoot its
long-run level in response to the monetary policy shock, if and only if,
συ(1 −βρv)(1 −ρv) > κυρv
which requires that the shock is not too persistent. It can be easily
checked that the previous condition corresponds to that for an increase
in the nominal interest rate in response to a positive vt shock. Note that,
in that case, the subsequent exchange rate depreciation required by the
interest parity condition (18) leads to an initial overshooting.
Figure 8.1 displays the dynamic responses of several macro variables to
an exogenous tightening of monetary policy. For the parameters common
with the closed economy, the baseline calibration from chapter 3 is used
here. Regarding the additional, open-economy-related, parameters, it is
assumed a unit elasticity of substitution between domestic and foreign
goods (η = 1) and a openness index υ of 0.4, following Galí and
Monacelli (2005).
As shown in the ﬁgure, both output (which equals the output gap
in this case) and domestic inﬂation decline persistently in response to
a tightening of monetary policy, due to the rise in both nominal and
(most importantly) real interest rates. The latter is also responsible
for the short-run appreciation of the terms of trade and the nominal
exchange rate, which leads to a large decline of CPI inﬂation on impact.
The subsequent depreciation of the exchange rate helps bring CPI
inﬂation back close to its initial level despite the persistent response
of domestic inﬂation. In the long run, the responses of the CPI, the
domestic price level, and the nominal exchange rate converge to the same
negative values, though their trajectories during the adjustment are rather

POLICY IN THE OPEN ECONOMY
243
Output gap
Employment
Domestic inflation
CPI inflation
Domestic price level
Consumer price level
Terms of trade
Nominal exchange rate
Nominal rate
Real rate
0
5
10
15
0
5
10
15
0
5
10
15
0
5
10
15
0
5
10
15
0
5
10
15
0
5
10
15
0
5
10
15
0
5
10
15
0
5
10
15
–0.4
–0.2
0
–0.4
–0.2
0
–0.2
–0.1
0
–0.2
–0.15
0
0.5
1
0
0.2
0.4
–0.4
–0.2
0
–0.4
–0.2
0
–1
0
1
–0.4
–0.2
0
Figure 8.1. Dynamic Responses to a Monetary Policy Shock.
different. Note also that the analysis above implies that for the special
case considered here the size and pattern of the responses of output and
domestic inﬂation to the monetary policy shocks do not differ from those
in the closed economy.

244
CHAPTER 8
8.4 OPTIMAL MONETARY POLICY: A SPECIAL CASE
This section derives and characterizes the optimal monetary policy for the
small open economy described above, as well as the implications of that
policy for a number of macroeconomic variables. The analysis, which
follows closely that of Galí and Monacelli (2005), is restricted to the
special case for which a second-order approximation to the welfare of the
representative consumer can be easily derived analytically. Its conclusions
should thus not be taken as applying to a more general environment.
Instead, this exercise is presented as an illustration of the approach to
optimal monetary policy design in an open economy rather than the basis
for a robust policy prescription.
The basic New Keynesian model of a closed economy provides a useful
benchmark for the analysis here. As discussed in chapter 4, under the
assumption of a constant employment subsidy τ that neutralizes the
distortion associated with ﬁrms’ market power, the optimal monetary
policy in that model is the one that replicates the ﬂexible price equilib-
rium allocation. The intuition for that result is straightforward: With the
subsidy in place, there is only one distortion left at work in the economy,
namely, sticky prices. By stabilizing markups at their frictionless level,
nominal rigidities cease to be binding, since ﬁrms do not feel any desire
to adjust prices. By construction, the resulting equilibrium allocation is
efﬁcient, and the price level remains constant.
In an open economy—and as noted, among others, by Corsetti and
Pesenti (2001)—an additional factor beyond the presence of market
power distorts the incentives of the monetary authority to deviate from
the ﬂexible price equilibrium allocation: the possibility of inﬂuencing the
terms of trade in a way beneﬁcial to domestic consumers. This possibility
is a consequence of the imperfect substitutability between domestic and
foreign goods (which makes the terms of trade a function of relative
supplies), combined with sticky prices (that render monetary policy non-
neutral). Furthermore, the strength of the incentive to deviate from the
ﬂexible price equilibrium allocation is a function of the preference shock.
As a result, and as shown below, the introduction of an employment
subsidy that exactly offsets ﬁrms’ market power distortion is in general
not enough to render the ﬂexible price equilibrium allocation optimal for,
at the margin, the monetary authority has an incentive to deviate from
that allocation in order to improve the terms of trade.10
However, as shown below, for the special parameter conﬁguration
σ = η = 1, and in the absence of preference shocks (i.e., assuming
10 See also the discussion in Benigno and Benigno (2003) in the context of a two-country
model.

POLICY IN THE OPEN ECONOMY
245
Zt = 1, for all t), there is a constant employment subsidy that exactly
offsets the combined effects of market power and the terms of trade
distortions. Under the assumption that such a subsidy is in place, the
ﬂexible price equilibrium allocation becomes optimal. The policy that
maximizes welfare in that case requires that domestic inﬂation be fully
stabilized, while allowing the nominal exchange rate (and, as a result,
CPI inﬂation) to adjust as needed in order to replicate the response of the
terms of trade that would be observed under ﬂexible prices.
One may wonder to what extent the desirability of strict domestic
inﬂation targeting is speciﬁc to the special case considered here or
whether it constitutes a good approximation for a more general case of
the model developed above. The optimal policy analysis undertaken in
Faia and Monacelli (2008), using a model nearly identical to the one
considered here, suggests that while the optimal policy involves some
variation in the domestic price level, the latter is almost negligible from a
quantitative point of view, thus making strict domestic inﬂation targeting
a good approximation to the optimal policy (or at least conditional on
the productivity shocks considered here). Using a different approach, de
Paoli (2009a) reaches a similar conclusion, except when an (implausibly)
high elasticity of substitution is assumed.11 But even in the latter case, the
losses that arise from following a domestic inﬂation targeting policy are
negligible.12 More generally, it is clear that there are several channels in
the open economy that may potentially render a strict domestic inﬂation
policy suboptimal, including a nonunitary elasticity of substitution, local
currency pricing, incomplete ﬁnancial markets, and so on, all of which
are unrelated to the sources of policy tradeoffs that may potentially
arise in the closed economy. Furthermore, the presence of sources of
ﬂuctuations other than technology (e.g., preference shocks) may also lead
to an optimal policy that deviates from strict domestic inﬂation targeting.
The analysis of the quantitative signiﬁcance of the effects of those
channels (individually or jointly) is beyond the scope of this chapter.
With that consideration in mind, let us next turn to the analysis of the
optimal policy in the special case mentioned above (i.e., σ = η = 1, and
no preference shocks).
11 Those results are conditional on productivity shocks being the driving force. Not
surprisingly, in the presence of cost-push shocks of the kind considered in chapter 5,
stabilizing domestic inﬂation is not optimal (as in the closed economy).
12 In solving the optimal policy problem for the general case, de Paoli (2009a) adopts
the linear-quadratic approach originally developed in Benigno and Woodford (2005),
which replaces the linear terms in the approximation to the households’ welfare losses
using a second-order approximation to the equilibrium conditions. Faia and Monacelli
(2008) solve for the Ramsey policy using the original nonlinear equilibrium conditions as
constraints of the policy problem.

246
CHAPTER 8
8.4.1 The Efﬁcient Allocation and Its Decentralization
Let us ﬁrst characterize the optimal allocation from the viewpoint of
a social planner facing the same resource constraints to which the
small open economy is subject in equilibrium (in relation to the rest
of the world), given the assumption of complete markets. In that
case, the optimal allocation must maximize U(Ct, Nt; Zt) subject to (i)
the technological constraint Yt = AtN1−α
t
, (ii) a consumption/output
possibilities set implicit in the international risk sharing condition (16),
and (iii) the market clearing condition (24).
Under the special case of σ = η = 1, and Zt = 1 for all t considered
here, (16) and (24) can be used to derive an exact consumption/output
possibilities set under complete markets, which takes the form:
Ct = Y1−υ
t
(Y∗
t )υ
Note that, in contrast with the closed economy, the elasticity of
consumption with respect to domestic output is not one, but 1−υ instead.
The optimal allocation (from the viewpoint of the small open economy,
which takes world output as given) must satisfy the optimality conditions
−Un(Ct, Nt)
Uc(Ct, Nt) = (1 −υ)(1 −α)Ct
Nt
which, under the assumed preferences and given σ = 1, can be written as
CtNϕ
t = (1 −υ)(1 −α)Ct
Nt
thus implying a constant optimal level of employment N = [(1 −υ)
× (1 −α)]
1
1+ϕ .
Consider, on the other hand, the ﬂexible price equilibrium allocation.
In the latter the gross price markup is constant and satisﬁes
M =
PH,t
Wt/MPNt
= (1 −α)(Yt/Nt)
(1 −τ)CtNϕ
t Sυt
=
(1 −α)
(1 −τ)N1+ϕ
t
where the third equality holds in the special case considered here.

POLICY IN THE OPEN ECONOMY
247
Hence, by setting τ such that (1 −τ)(1 −υ)M = 1, the optimality
of the ﬂexible price equilibrium allocation is guaranteed. Note that the
required subsidy is smaller than necessary to offset ﬁrms’ market power
distortion, in order to exploit the gains from a more favorable terms of
trade brought about by a somewhat lower domestic output.
With the optimal subsidy in place, and as in the closed economy of
chapter 3, the optimal monetary policy requires stabilizing the output gap
(i.e., yt = 0, for all t). Equation (37) then implies that domestic prices are
also stabilized under that optimal policy (i.e., πH,t = 0 for all t). Thus, in
the special case under consideration, (strict) domestic inﬂation targeting
(SDIT) is indeed the optimal policy.
8.4.2 Implementation and Macroeconomic Implications
This section discusses the implementation of a strict domestic inﬂation
targeting policy and characterizes some of its equilibrium implications.
While that policy has been shown to be optimal only for the special
case considered above, its implications for the general case can also be
considered.
8.4.2.1 IMPLEMENTATION
As discussed above, full stabilization of domestic prices implies
yt = πH,t = 0
for all t. This in turn implies that yt = yn
t and it = rn
t will hold in
equilibrium for all t, with all the remaining variables matching their
natural levels at all times.
For the reasons discussed in chapter 4, an interest rate rule of the
form it
= rn
t
is associated with an indeterminate equilibrium, and
hence, does not guarantee that the outcome of full price stability be
attained. That result follows from the equivalence between the dynamical
system describing the equilibrium of the small open economy and that
of the closed economy, as discussed in chapter 4. As shown there, the
indeterminacy problem can be avoided, and the uniqueness of the price
stability outcome restored by having the central bank follow a rule that
makes the interest rate respond with sufﬁcient strength to deviations of
domestic inﬂation and/or the output gap from target. More precisely,
the central bank can guarantee that the desired outcome is attained by
committing to a rule of the form
it = rn
t + φππH,t
(42)

248
CHAPTER 8
where φπ > 1. In equilibrium, the term φππH,t vanishes (because πH,t = 0
for all t), implying that it = rn
t , for all t.
8.4.2.2 MACROECONOMIC IMPLICATIONS
Under a strict domestic inﬂation targeting policy, the behavior of real
variables in the small open economy corresponds to the one that would
be observed in the absence of nominal rigidities. Hence, it is seen from
the inspection of equation (35) that domestic output always increases in
response to a positive technology shock at home. As discussed earlier,
the sign of the response to a rise in world output is ambiguous, however,
and depends on the sign of ∗, which in turn depends on the elasticity of
substitution η and the risk aversion parameter σ.
As shown above the natural level of the terms of trade is given by
sn
t = συ(yn
t −y∗
t ) −(1 −υ)zt
= συ[aat + zzt + (∗−1)y∗
t ] −(1 −υ)zt
= συaat + συ(∗−1)y∗
t + [συz −(1 −υ)]zt
Thus, given world output, an improvement in domestic technology
always leads to a real depreciation, through its expansionary effect on
domestic output. Positive preference shocks zt generate a real apprecia-
tion, since συz −(1 −υ) < 0. On the other hand, changes in world
output have an effect on the terms of trade of ambiguous sign.
Given that domestic prices are fully stabilized under DIT, it follows
that eDIT
t
= sn
t −p∗
t , that is, the nominal exchange rate moves one-
for-one with the (natural) terms of trade and (inversely) with the world
price level. Assuming constant world prices, the nominal exchange rate
will inherit all the statistical properties of the natural terms of trade.
In particular, in response to technology shocks, the nominal exchange
rate under DIT will be proportional to the gap between the natural level
of domestic output (in turn related to productivity) and world output.
Thus, the volatility of the nominal exchange rate will tend to be high
(low) when domestic natural output displays a weak (strong) positive
comovement with world output.
The implied equilibrium process for the CPI can also be derived. Given
the constancy of domestic prices it is given by
pDIT
t
= υsn
t
= υ(eDIT
t
+ p∗
t )

POLICY IN THE OPEN ECONOMY
249
Thus, it is seen that under the DIT regime, the CPI level will also vary
with the (natural) terms of trade and will inherit its statistical properties.
If the economy is very open, and if domestic productivity (and hence,
the natural level of domestic output) is not much synchronized with
world output, CPI prices could potentially be highly volatile, even if the
domestic price level is constant.
An important lesson emerges from the previous analysis: Potentially
large and persistent ﬂuctuations in the nominal exchange rate, as well
as in some inﬂation measures (like the CPI), are not necessarily un-
desirable, nor do they require a policy response aimed at dampening
such ﬂuctuations. Instead, and especially for an economy that is very
open and subject to large idiosyncratic shocks, those ﬂuctuations may
be an equilibrium consequence of the adoption of an optimal policy, as
illustrated by the model above.
8.4.3 The Welfare Costs of Deviations from the Optimal Policy
Under the particular assumptions under which strict domestic inﬂation
targeting has been shown to be optimal (i.e., log utility, a unit elasticity
of substitution between domestic and foreign goods and no preference
shocks), it is relatively straightforward to derive a second-order approx-
imation to the discounted utility losses of the domestic representative
consumer associated with deviations from the optimal policy. As shown
in appendix 8.1, those losses, expressed as a fraction of steady state
consumption, can be written as (ignoring terms independent of policy):
W = (1 −υ)
2
∞

t=0
βt
1 + ϕ
1 −α

y2
t + ϵ
λπ2
H,t

(43)
The expected period welfare losses of any policy that deviates from
strict inﬂation targeting can be written in terms of the variances of
inﬂation and the output gap
V = (1 −υ)
2
1 + ϕ
1 −α

var(yt) + ϵ
λ var(πH,t)

(44)
Note that the previous expressions for the welfare losses are, up to the
multiplicative term (1 −υ), identical to the ones derived for the closed
economy in chapter 4, with domestic inﬂation being the relevant inﬂation
variable here. Below, (44) is used to assess the welfare implications of
alternative monetary policy rules and to rank those rules on welfare
grounds.

250
CHAPTER 8
8.5 SIMPLE MONETARY POLICY RULES FOR
THE SMALL OPEN ECONOMY
This section analyzes the macroeconomic implications of alternative
monetary policy rules for the small open economy. The ﬁrst rule, already
analyzed in the previous section, is strict domestic inﬂation targeting
(SDIT, for short), which requires
πH,t = 0
for all t. Under the second rule considered, referred to as strict CPI
inﬂation targeting (SCIT, for short), consumer price inﬂation is fully
stabilized:
πt = 0
for all t. The third rule is an exchange rate peg (PEG, for short), which
can be formally represented as
et = 0
for all t (which in turn requires that it = i∗
t , also for all t).
In addition to the previous rules, two stylized Taylor-type rules
are considered, which can be thought of as ﬂexible versions of the
inﬂation targeting rules speciﬁed above, allowing for some concern for
output ﬂuctuations. The ﬁrst has the domestic interest rate respond
systematically to domestic inﬂation and output, whereas the second
assumes that CPI inﬂation is the variable the domestic central bank
reacts to (in addition to output). Formally, the ﬂexible domestic inﬂation
targeting (FDIT, for short) is speciﬁed as
it = 0.01 + 1.5πH,t + 0.125yt
whereas the ﬂexible CPI inﬂation targeting rule (FCIT, for short) is
given by
it = 0.01 + 1.5πt + 0.125yt
for all t, where the size of the coefﬁcients is based on the original Taylor
(1993) rule.
Below, a comparison is provided of the equilibrium properties of
several macroeconomic variables under the above simple rules for a
calibrated version of the small open economy model developed above.13
13 See Galí and Monacelli (2005) for a similar analysis (though with a slightly different
calibration).

POLICY IN THE OPEN ECONOMY
251
TABLE 8.1
Properties of Simple Policy Rules
SDIT
SCIT
PEG
FDIT
FCIT
σ(y)
2.29
1.92
1.72
1.85
1.76
σ(y)
0
0.66
0.92
0.44
0.62
σ(πH)
0
0.19
0.35
0.69
0.58
σ(π)
0.41
0
0.21
0.70
0.52
σ(s)
2.29
1.92
1.72
1.85
1.76
σ(
e)
1.02
0.29
0
0.95
0.59
L
0
0.05
0.17
0.61
0.43
8.5.1 A Quantitative Analysis of Alternative Rules
8.5.1.1 CALIBRATION
This section presents some quantitative results based on a calibrated
version of the small open economy. The baseline calibration assumes
σ = η = 1 in a way consistent with the special case considered above.
A baseline value for υ (the degree of openness) is set at 0.4. The latter
corresponds roughly to the import/GDP ratio in Canada, which is taken
as a prototype small open economy. The remaining parameters are set at
the values found in the baseline calibration of chapter 3. The analysis is
restricted to technology shocks.14
8.5.1.2 MACROECONOMIC VOLATILITY AND WELFARE LOSSES
Table 8.1 reports the standard deviations of several key variables under
the alternative monetary policy rules introduced above. A critical element
that distinguishes each simple rule relative to the optimal policy is the
excess smoothness of both the terms of trade and the (ﬁrst-differenced)
nominal exchange rate.15 This in turn is often reﬂected in too high a
volatility of the output gap and domestic inﬂation. In particular, the PEG
regime is the one that ampliﬁes both output gap and domestic inﬂation
volatility to the largest extent, with the CITR regime lying somewhere
in between. Note also that the terms of trade are more stable under
an exchange rate peg than under any other policy regime, but this is
not reﬂected in smaller welfare losses. That ﬁnding, which is consistent
with the evidence of Mussa (1986), points to the existence of “excess
smoothness” in the real exchange rate under a nominal exchange rate
14 Note that under the assumed calibration, changes in world output do not have any
effect on the domestic economy.
15 Statistics are reported for the nominal depreciation rate, as opposed to the level, given
the unit root in the nominal exchange rate.

252
CHAPTER 8
peg. That feature is a consequence of the inability of prices (which are
sticky) to compensate for the constancy of the nominal exchange rate.16
The last row in table 8.1 reports the welfare losses associated with the
alternative policy rules introduced above, expressed as a percentage of
steady state consumption. Under the baseline calibration all rules other
than SDIT are suboptimal because they involve nontrivial deviations
from the efﬁcient/natural allocation. Note that both Taylor rules imply
substantially larger welfare losses than the other three rules considered,
largely due to their implied higher volatility in domestic inﬂation.
However, and as is usually the case in welfare exercises of this sort found
in the literature, the implied welfare losses are quantitatively small under
all policy regimes.
8.6 NOTES ON THE LITERATURE
Earlier work on optimizing open economy models with nominal rigidities
focused on the transmission of monetary policy shocks, typically repre-
sented as disturbances to an exogenous stochastic process for the money
supply.17 A key contribution in that area is Obstfeld and Rogoff (1995),
who develop a two-country model where monopolistically competitive
ﬁrms set prices before the realization of the shocks (i.e., one period
in advance). The framework is used to analyze the dynamics of the
exchange rate and other variables in response to a change in the money
supply (and government spending) and the welfare effects resulting from
that intervention. An earlier paper, by Svensson and van Wijnbergen
(1989) contains a related analysis under the assumption of full risk-
sharing among consumers from different countries.
Corsetti and Pesenti (2001) develop a version of the Obstfeld-Rogoff
model that allows for home bias in preferences, leading to terms of trade
effects that are argued to have potentially important welfare effects. Betts
and Devereux (2000) revisit the analysis in Obstfeld and Rogoff (1995)
while departing from the assumption of the law of one price found in the
latter paper. In particular, they allow ﬁrms to price discriminate across
markets assuming they set prices (in advance) in terms of the currency of
the importing country (“pricing to market”).
The effects of money supply shocks on the persistence and volatility
of nominal and real exchange rates are analyzed under the assump-
tion of staggered price setting in Kollmann (2001) and Chari, Kehoe,
16 See Monacelli (2004) for a detailed analysis of the implications of ﬁxed exchange rates.
17 See Lane (1999) for an excellent survey of that literature.

POLICY IN THE OPEN ECONOMY
253
and McGrattan (2002).18 The assumption of staggered price setting
(and staggered wage setting in Kollmann’s case) induces much richer
and more realistic dynamics than that of price setting one period in
advance.
A more recent strand of the literature has attempted to go beyond the
analysis of the transmission of exogenous monetary policy shocks, and
has focused instead on the implications of sticky price open economy
models for the design of optimal monetary policy, using a welfare
theoretic approach.19 Early examples of papers analyzing the properties
of alternative monetary policy arrangements in a two-country setting
assumed that prices are set one period in advance. They include the work
of Obstfeld and Rogoff (2002) and Benigno and Benigno (2003), both
using the assumption of producer currency pricing. Bacchetta and van
Wincoop (2000), Sutherland (2006), Devereux and Engel (2003), and
Corsetti and Pesenti (2005) use the same assumption in the context of
economies with local currency pricing.
More recent frameworks have instead adopted the staggered price-
setting structure à la Calvo. Galí and Monacelli (2005), on which much
the analysis of the present chapter is built, is an illustration of work
along those lines for a small open economy. Their analysis uncovers
the assumptions under which replicating the ﬂexible price equilibrium
allocation through full stabilization of domestic prices is optimal, in
what amounts to an open economy version of the “divine coincidence”
result discussed in chapter 4. Those assumptions include producer
currency pricing, complete asset markets, log utility of consumption, and
a unit elasticity of substitution between domestic and foreign goods.
An extension of that framework, incorporating cost-push shocks and
featuring tradeoffs similar to those analyzed in chapter 5 can be found
in Clarida, Galí, and Gertler (2001). Kollmann (2002) considers a
more general model of a small open economy with several sources of
shocks, and carries out a numerical analysis of the welfare implications
of alternative rules. Erceg, Gust, and López-Salido (2009) analyze the
role of openness in the transmission of shocks using a version of the
Galí-Monacelli model that incorporates staggered wage setting in a way
analogous to the model in chapter 6. Galí and Monacelli (2014) study
the gains from increased wage ﬂexibility in such a framework, and their
dependence on the exchange rate policy.
18 Kollmann (2001) assumes prices and wages are set à la Calvo—as in the model of the
present chapter—whereas Chari, Kehoe, and McGrattan (2002) assume price setting à la
Taylor, i.e., with deterministic price durations.
19 Ball (1999) and Svensson (2000) carry out an analysis similar in spirit, but in the
context of nonoptimizing models.

254
CHAPTER 8
Several papers have examined the consequences on optimal monetary
policy of departures from the benchmark assumptions of the Galí-
Monacelli model in closely related models. Faia and Monacelli (2008)
and de Paoli (2009a) study an environment with more general prefer-
ences, and show how the size of the elasticity of substitution between
domestic and foreign goods affects the extent to which the central bank
wants to stabilize the exchange rate (thus departing from strict domestic
inﬂation targeting), in order to improve welfare. De Paoli (2009b) shows
how the conclusions from that analysis need to be modiﬁed when the
assumption of complete markets is relaxed. Using a similar framework
as a starting point, Monacelli (2005) shows that the introduction of
imperfect pass-through generates a tradeoff between stabilization of
domestic inﬂation and the output gap, leading to gains from commitment
similar to those analyzed in chapter 5 for the closed economy. Campolmi
(2014) introduces staggered wage setting in a small open economy
(coexisting with staggered price setting, as in the closed economy of
chapter 6). She shows that the presence of sticky wages generally
makes CPI inﬂation targeting more desirable than domestic inﬂation
targeting.
In contrast with the previous references, which study monetary policy
in a small open economy, a number of papers have framed their
analysis of monetary policy design in the context of two-country models
with staggered price setting à la Calvo. The papers by Clarida, Galí,
and Gertler (2002), Pappa (2004), and Benigno and Benigno (2006)
provide examples of that literature, with a special focus on the gains
from cooperation, and under the assumption of producer currency
pricing. Engel (2011) studies the implications for optimal monetary
policy of assuming local currency pricing instead in an otherwise similar
framework, showing how that modiﬁcation warrants a focus on CPI—
rather than domestic price—stabilization. Benigno (2009) studies the
implications of incomplete asset markets and ﬁnancial imbalances in a
similar environment, showing that those factors may justify a deviation
from a strict domestic inﬂation targeting policy. Woodford (2009)
uses a similar framework to study the challenges posed by trade and
ﬁnancial integration on domestic monetary policy. Corsetti, Dedola,
and Leduc (2010) provide a uniﬁed treatment of the consequences
of deviations from the assumptions underlying the divine coincidence
result.
Finally, Galí and Gertler (2009) contains a number of contributions
that use related frameworks to understand different aspects of the
international dimension of monetary policy.

POLICY IN THE OPEN ECONOMY
255
APPENDIX
8.1 A SECOND-ORDER APPROXIMATION TO WELFARE LOSSES IN THE
SMALL OPEN ECONOMY
This appendix derives a second-order approximation to the utility of
the representative household in the small open economy analyzed above
for the special case of σ = η = 1, when the economy remains in a
neighborhood of an efﬁcient steady state (i.e., when the optimal constant
subsidy derived in the main text is in place).
Using the same approach as in appendix 4.1, the second-order Taylor
expansion of Ut ≡U(Ct, Nt; Zt) around a steady state (C, N; 1) can be
written for the special case at hand as
Ut −U ≃UcC ct(1 + zt) + UnN

nt(1 + zt) + 1 + ϕ
2
n2
t

+ t.i.p.
= UcC (1 −υ)yt(1 + zt) + UnN
1 −α

yt(1 + zt) + ϵ
2 vari{pH,t(i)}
+ 1
2(1 + ϕ)(1 −α) n2
t

+ t.i.p.
where the fact has been used that ct = (1 −υ)yt + υy∗
t + ςzt holds for the
assumed special case.
As shown in the main text, efﬁciency of the steady state implies
−Un
Uc = (1 −υ)(1 −α) Ct
Nt . Hence one can write:
Ut −U
UcC
≃−1 −υ
2
 ϵ
 vari{pH,t(i)} + (1 + ϕ)(1 −α) n2
t

+ t.i.p.
Accordingly, a second-order approximation to the consumer’s welfare
losses can be written and expressed as a fraction of steady state
consumption (and up to additive terms independent of policy) as
W = −E0
∞

t=0
βt
Ut −U
UcC

= −1 −υ
2
E0
∞

t=0
βt  ϵ
 vari{pH,t(i)} + (1 + ϕ) (1 −α)n2
t


256
CHAPTER 8
The ﬁnal step consists in rewriting the terms involving the price
dispersion variable as a function of inﬂation. In order to do so, make
use of the following lemma, which carries over from the closed economy
case
Lemma 2: 
∞
t=0 βt vari{pH,t(i)} =
θ
(1−βθ)(1−θ)

∞
t=0 βtπ2
H,t
Proof: Woodford (2003, chap. 6)
Using the fact that λ ≡
(1−θ)(1−βθ)
θ
, the previous lemma can be
combined with the expression for the welfare losses above to obtain
W = −1 −υ
2
E0
∞

t=0
βt ϵ
λ

π2
t + (1 + ϕ) (1 −α)n2
t

Note that in the absence of preference shocks, yn
t = at and nn
t = n for
all t in the special case considered, thus implying yt = (1 −α)nt, which
allows one to rewrite the loss function in terms of domestic inﬂation and
the output gap as:
W = 1 −υ
2
E0
∞

t=0
βt
ϵ
λ

π2
t +
1 + ϕ
1 −α

y2
t

EXERCISES
8.1. A small open economy model
Consider a small open economy where no international trade in
assets is allowed (implying that trade is always balanced). Hence,
pt + ct = pH,t + yt
where ct denotes consumption, yt is output, pH,t is the domestic
price level, and pt is the CPI (all in logs). Assuming a constant

POLICY IN THE OPEN ECONOMY
259
price level in the rest of the world (p∗
t = 0),
pt = (1 −υ)pH,t + υet
where et is the nominal exchange rate.
Let st ≡et −pH,t denote the terms of trade. Under the
assumption of a unit elasticity of substitution between foreign and
domestic goods,
st = yt −y∗
t
where y∗
t is (log) output in the rest of the world (assumed to
evolve exogenously). The domestic aggregate technology can be
written as
yt = at + nt
where at is an exogenous technology process. Assume perfect
competition in both goods and labor markets with ﬂexible prices
and wages. The labor supply takes the form
wt −pt = σct + ϕnt
Finally,
assume
a
money
demand
function
of
the
form
mt −pt = ct.
a. Determine the equilibrium processes for output, consumption,
the terms of trade, and the nominal exchange rate in the small
open economy, as a function of productivity at, foreign output
y∗
t , and the money supply under the assumption that the latter
evolves exogenously. Discuss the implications of assuming σ =
1.
b. How would your answer have to be modiﬁed if a ﬁxed nominal
exchange rate regime were in place?
c. Discuss, in words, how some of the results in (a) and (b) would
change qualitatively in the presence of imperfect competition
and sticky prices.
8.2. The effects of technology shocks in the open economy
Consider the small open economy model described in this chapter.
The equilibrium dynamics for domestic inﬂation πH,t and the
output gap yt are described by the equations
πH,t = β Et{πH,t+1} + κυyt
yt = Et{yt+1} −1
συ
(it −Et{πH,t+1} −rn
t )

260
CHAPTER 8
and where rn
t is given by
rn
t = ρ −ψraat
Natural output is in turn given by
yn
t = ψyaat
The technology parameter follows a stationary AR(1) process
at = ρaat−1 + εa
t
where ρa ∈[0, 1).
Assume that the monetary authority follows the simple interest
rate rule
it = ρ + φππH,t
where φπ > 1.
a. Determine the response of output, domestic inﬂation, the terms
of trade, and the nominal exchange rate to a positive domestic
technology shock (note: for the purposes of this exercise
assume y∗
t = p∗
t = 0 for all t).
b. Suppose that the central bank pegs the nominal exchange rate
so that et = 0 for all t. Characterize the economy’s response to
a technology shock in that case.