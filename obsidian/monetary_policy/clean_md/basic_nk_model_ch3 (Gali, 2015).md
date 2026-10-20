Chapter 3
THE BASIC NEW KEYNESIAN MODEL
The present chapter describes the key elements of the baseline model that
will be used as a reference framework in the remainder of the book. The
model involves two main departures from the assumptions of the classical
monetary economy developed in chapter 2. First, imperfect competition
in the goods market is introduced by assuming that each ﬁrm produces a
differentiated good for which it sets the price (instead of taking the price
as given), given a demand constraint. Second, a form of price stickiness is
introduced by assuming that only a fraction of ﬁrms can reset their prices
in any given period. In particular, and following much of the literature, a
model of staggered price setting due to Calvo (1983) and characterized by
random price durations is adopted.1 The resulting framework is referred
to as the basic New Keynesian model. As discussed in chapter 1, that
model has become in recent years the workhorse for the analysis of
monetary policy, ﬂuctuations, and welfare.
The introduction of differentiated goods requires that the household
problem be modiﬁed slightly relative to the one considered in the
previous chapter. That modiﬁcation is discussed before turning to the
ﬁrms’ optimal price-setting problem and the implied inﬂation dynamics.
3.1 HOUSEHOLDS
Once again, assume a representative inﬁnitely lived household seeking to
maximize
E0
∞

t=0
βtU(Ct, Nt; Zt)
where Ct is now a consumption index given by
Ct ≡
 1
0
Ct(i)1−1
ϵ di

ϵ
ϵ−1
1 The resulting inﬂation dynamics can also be derived under the assumption of quadratic
costs of price adjustment. See, e.g., Rotemberg (1982).

53
with Ct(i) denoting the quantity of good i consumed by the household
in period t. A continuum of goods represented by the interval [0, 1] is
assumed. The period budget constraint now takes the form
 1
0
Pt(i)Ct(i)di + QtBt ≤Bt−1 + WtNt + Dt
for t = 0, 1, 2..., where Pt(i) is the price of good i, and where the
remaining variables are deﬁned as in chapter 2: Nt denotes employment
or hours worked, Wt is the nominal wage, Bt represents purchases of
one-period discount bonds (at a price Qt), and Dt denotes dividends
from the ownership of ﬁrms. The above sequence of period budget
constraints is supplemented with a solvency constraint of the form
limT→∞Et

t,T
BT
PT

≥0 for all t, where t,T ≡βT−tUc,T/Uc,t. Note
that monetary holdings are not modeled explicitly, so one can think of
the present framework as the cashless limit of an economy with money
in the utility function, with the latter being additively separable.2
In addition to the consumption/savings and labor supply decisions
already analyzed in chapter 2, the household now must decide how to al-
locate its consumption expenditures among the different goods. Optimal
behavior requires that the consumption index Ct be maximized for any
given level of expenditures
 1
0 Pt(i)Ct(i)di. As shown in appendix 3.1,
the solution to that problem yields the set of demand equations
Ct(i) =
 Pt(i)
Pt
	−ϵ
Ct
(1)
for all i ∈[0, 1], where Pt ≡

 1
0 Pt(i)1−ϵdi

1−ϵ is an aggregate price
index. Furthermore, and conditional on such optimal behavior
 1
0
Pt(i)Ct(i)di = PtCt
i.e., total consumption expenditures can be written as the product of the
price index times the quantity index. Plugging the previous expression
into the budget constraint yields
PtCt + QtBt ≤Bt−1 + WtNt + Dt
2 See section 5 of chapter 2 for a discussion.

CHAPTER 3
which is formally identical to the constraint facing households in
the single good economy analyzed in chapter 2. Hence, the optimal
consumption/savings and labor supply decisions are identical to the ones
derived therein, and described by the conditions
−Un,t
Uc,t
= Wt
Pt
Qt = βEt

Uc,t+1
Uc,t
Pt
Pt+1

As in chapter 2, it is assumed that the household’s period utility is
given by
U(Ct, Nt; Zt) =






C1−σ
t
−1
1−σ
−N1+ϕ
t
1+ϕ

Zt
for σ ̸= 1

log Ct −N1+ϕ
t
1+ϕ

Zt
for σ = 1
where zt ≡log Zt follows an exogenous AR(1) process
zt = ρzzt−1 + εz
t
with ρz ∈[0, 1).
As shown in chapter 2, the resulting log-linear versions of the above
optimality conditions take the form
wt −pt = σct + ϕnt
(2)
ct = Et{ct+1} −1
σ (it −Et{πt+1} −ρ) + 1
σ (1 −ρz)zt
(3)
where it ≡−log Qt is the short-term nominal interest rate and ρ ≡
−log β is the discount rate, and where lowercase letters are used
to denote the logs of the original variables. As before, the previous
conditions are supplemented, when necessary, with an ad hoc log-linear
money demand equation of the form
mt −pt = yt −ηit
(4)
where mt denotes (log) nominal money holdings.

55
3.2 FIRMS
Assume a continuum of ﬁrms indexed by i ∈[0, 1]. Each ﬁrm produces a
differentiated good, but they all use an identical technology, represented
by the production function
Yt(i) = AtNt(i)1−α
(5)
where At represents the level of technology, assumed to be common to
all ﬁrms and to evolve exogenously over time according to the process
at = ρaat−1 + εa
t
(6)
with ρa ∈[0, 1].
All ﬁrms face an identical isoelastic demand schedule given by (1), and
take the aggregate price level Pt and aggregate consumption index Ct as
given.
Following the formalism proposed in Calvo (1983), each ﬁrm may
reset its price only with probability 1−θ in any given period, independent
of the time elapsed since it last adjusted its price. Thus, in each period a
measure 1−θ of producers reset their prices, while a fraction θ keep their
prices unchanged. As a result, the average duration of a price is given by
1
1−θ . In this context, θ becomes a natural index of price stickiness.
3.2.1 Aggregate Price Dynamics
As shown in appendix 3.2, the above environment implies that the
aggregate price dynamics are described by the equation

1−ϵ
t
= θ + (1 −θ)
 P∗
t
Pt−1
	1−ϵ
(7)
where 
t ≡
Pt
Pt−1 is the gross rate of inﬂation between t −1 and t, and P∗
t
is the price set in period t by ﬁrms reoptimizing their price in that period.
Notice that, as shown below, all ﬁrms resetting their price in any given
period will choose the same price because they face an identical problem.
It follows from (7) that in a steady state with zero inﬂation (
 = 1),
P∗
t = Pt−1 = Pt for all t. Furthermore, a log-linear approximation to the
aggregate price index around that steady state yields
πt = (1 −θ)(p∗
t −pt−1)
(8)

CHAPTER 3
or, equivalently, after rearranging terms:
pt = θpt−1 + (1 −θ)p∗
t
i.e., the current price level is a weighted average of last period’s price
level and the newly set price, all in logs, with the weights given by the
fraction of ﬁrms that do not and do adjust prices, respectively.
The previous equations make clear that, in the present setup, variations
in the price level result from the fact that ﬁrms reoptimizing in any given
period choose a price that differs from the economy’s average price in
the previous period. Hence, and in order to understand the evolution of
inﬂation over time, one needs to analyze the factors underlying ﬁrms’
price setting decisions, a question which is discussed next.
3.2.2 Optimal Price Setting
A ﬁrm reoptimizing in period t will choose the price P∗
t that maximizes
the current market value of the proﬁts generated while that price remains
effective. As shown in appendix 3.3, this corresponds to solving the
following problem:
max
P∗
t
∞

k=0
θkEt

t,t+k(1/Pt+k)

P∗
t Yt+k|t −Ct+k(Yt+k|t)

subject to the sequence of demand constraints
Yt+k|t =
 P∗
t
Pt+k
	−ϵ
Ct+k
(9)
for k = 0, 1, 2, ... where t,t+k ≡βkUc,t+k/Uc,t is the stochastic discount
factor, Ct(·) is the (nominal) cost function, and Yt+k|t denotes output in
period t + k for a ﬁrm that last reset its price in period t. Note that it is
implicitly assumed that the ﬁrm always meets the demand for its good
at the current price. That assumption, which is maintained throughout
the analysis below, requires, in turn, that the average price markup is
sufﬁciently large and/or that the shifts in demand resulting from a variety
of shocks are not too large.
The optimality condition associated with the problem above takes the
form
∞

k=0
θkEt

t,t+kYt+k|t(1/Pt+k)

P∗
t −M
t+k|t

= 0
(10)

57
where 
t+k|t ≡C′
t+k(Yt+k|t) denotes the (nominal) marginal cost in period
t + k for a ﬁrm which last reset its price in period t and M ≡
ϵ
ϵ−1.
Note that in the limiting case of no price rigidities (θ = 0), the previous
condition collapses to the familiar optimal price setting condition for a
monopolistic competitor under ﬂexible prices
P∗
t = M
t|t
which allows us to interpret M as the optimal markup in the absence of
constraints on the frequency of price adjustment. Henceforth, M is often
referred to as the “desired,” “natural,” or “frictionless” markup. That
markup is constant given the assumption of a time-invariant elasticity of
substitution ϵ.
Next, the optimal price setting condition (10) is log-linearized around
the perfect foresight zero inﬂation steady state. Note that the latter is
characterized by t,t+k = βk and P∗
t /Pt−k = Pt/Pt−k = 1. Thus, all ﬁrms
produce the same quantity of output, and face the same marginal cost,
that is, Yt+k|t = Y, and 
t+k|t = 
t+k = 
t for all t and k = 0, 1, 2, 3, . . .
Thus, (10) implies that Pt = M
t for all t in that steady state, i.e., actual
markups, common to all ﬁrms, coincide with the frictionless markup.
A ﬁrst-order Taylor expansion of (10) around the zero inﬂation steady
state yields, after some manipulation,
p∗
t = µ + (1 −βθ)
∞

k=0
(βθ)kEt{ψt+k|t}
(11)
where ψt+k|t ≡log 
t+k|t is the (log) marginal cost and µ ≡log M
is the log of the desired gross markup (which, for M close to one, is
approximately equal to the net markup M−1). Hence, and to the extent
that prices are sticky (θ > 0), ﬁrms set prices in a forward-looking way. In
particular, they choose a price that corresponds to their desired markup
over a weighted average of their current and expected (nominal) marginal
costs, with the weights being proportional to the probability of the price
remaining effective at each horizon, θk, times the cumulative discount
factor, βk.
3.3 EQUILIBRIUM
Market clearing in the goods market requires that the quantity produced
of each good matches the quantity demanded. In the stylized model
analyzed here consumption is the only source of demand for goods.

CHAPTER 3
Thus, in equilibrium,
Yt(i) = Ct(i)
for all i ∈[0, 1] and all t.
Letting aggregate output be deﬁned as Yt ≡

 1
0 Yt(i)1−1
ϵ di

ϵ
ϵ−1 it
follows that
Yt = Ct
(12)
must hold for all t.
Aggregate consumption Ct (which corresponds to aggregate demand
in the present model) is in turn determined by the consumer’s Euler
equation (3). Combining the latter with (12) yields an expression for
current (log) output as a function of the latter’s expected one-period-
ahead value, the real interest rate, and the demand shifter:
yt = Et{yt+1} −1
σ (it −Et{πt+1} −ρ) + 1
σ (1 −ρz)zt
(13)
Note that (13) can be solved forward to yield
yt = 1
σ zt −1
σ
∞

k=0
Et{it+k −Et{πt+1+k} −ρ} + lim
T→∞Et{yt+T}
Thus, an exogenous shock will impact output only to the extent that it
meets one or more of the following conditions: (i) it shifts the preference
parameter zt, (ii) it has a permanent effect on the level of output, or (iii)
it leads to a deviation of the real interest rate from the discount rate,
current or anticipated.
Aggregate employment is given by the sum of employment across
ﬁrms:
Nt =
 1
0
Nt(i)di

59
Using (5)
Nt =
 1
0
Yt(i)
At

1−α
di
=
 Yt
At

1−α  1
0
 Pt(i)
Pt
	−
ϵ
1−α
di
where the second equality follows from (1) and the goods market clearing
condition. Taking logs,
(1 −α)nt = yt −at + dt
where dt ≡(1 −α) log
 1
0 (Pt(i)/Pt)−
ϵ
1−α di is a measure of price (and,
hence, output) dispersion across ﬁrms. In appendix 3.4 it is shown that,
in a neighborhood of the zero inﬂation steady state, dt is equal to zero
up to a ﬁrst-order approximation. Hence, one can write the following
approximate relation
nt =
1
1 −α (yt −at)
(14)
which can be thought of as determining aggregate employment, given
aggregate output and technology.
Note that the (log) marginal cost for an individual ﬁrm that last set its
price in period t is given by:3
ψt+k|t = wt+k −mpnt+k|t
= wt+k −(at+k −αnt+k|t + log(1 −α))
where mpnt+k|t and nt+k|t respectively denote the (log) marginal product
of labor and (log) employment in period t + k for a ﬁrm that last reset its
price in period t.
3 Marginal cost equals the labor needed to produce an additional unit of output,
1/MP Nt+k|t, times the cost of each unit of that labor, i.e., the wage Wt+k. Formally,

t+k|t = Wt+k/MP Nt+k|t.

CHAPTER 3
Letting ψt ≡
 1
0 ψt(i)di represent the (log) average marginal cost, it
follows that
ψt = (1 −θ)
∞

k=0
θkψt|t−k
= wt −(at −αnt + log(1 −α))
where the second equality makes use of the relation nt =
 1
0 nt(i)di,
which holds up to a ﬁrst order approximation about a symmetric
equilibrium.
Thus the following relation holds between ﬁrm-speciﬁc and economy-
wide marginal costs:
ψt+k|t = ψt+k + α(nt+k|t −nt+k)
= ψt+k +
α
1 −α (yt+k|t −yt+k)
= ψt+k −
αϵ
1 −α (p∗
t −pt+k)
(15)
where the second equality follows from (14) and the third equality
results from combining demand schedule (9) and goods market clearing
condition (12) (after taking logs). Notice that under the assumption
of constant returns to scale (α = 0), marginal cost is independent of
the level of production and, hence, it is common across ﬁrms, that is,
ψt+k|t = ψt+k.
Substituting (15) into (11) and rearranging terms yields
p∗
t = (1 −βθ)
∞

k=0
(βθ)kEt

pt+k −µt+k

where µt ≡µt −µ is the deviation between the average and desired
markups, with µt ≡pt −ψt and  ≡
1−α
1−α+αϵ ∈(0, 1].
The above expression for p∗
t can be rewritten as a recursive equation:
p∗
t = βθ Et{p∗
t+1} + (1 −βθ)(pt −µt)
(16)
Finally, combining (8) and (16) yields the inﬂation equation
πt = βEt{πt+1} −λµt
(17)

61
where
λ ≡(1 −θ)(1 −βθ)
θ

is strictly decreasing in the index of price stickiness θ, in the measure of
decreasing returns α, and in the demand elasticity ϵ.4 Note that  = 1 in
the particular case of constant returns to labor (α = 0).
Solving (17) forward, inﬂation is expressed as the discounted sum of
current and expected future deviations of average markups from their
desired levels:
πt = −λ
∞

k=0
βkEt{µt+k}
Thus, inﬂation will be positive when ﬁrms expect average markups
to be below their desired level µ, for in that case ﬁrms that have the
opportunity to reset prices will, on average, choose a price above the
economy’s average price level in order to realign their markup closer to
its desired level.
It is worth emphasizing here that the mechanism underlying ﬂuctua-
tions in the aggregate price level and inﬂation laid out above has little in
common with the one at work in the classical monetary economy. Thus,
in the present model, inﬂation results from the aggregate consequences
of purposeful price-setting decisions by ﬁrms, which adjust their prices
in light of current and anticipated cost conditions. By contrast, in
the classical monetary economy analyzed in chapter 2, inﬂation is a
consequence of the changes in the aggregate price level that, given
the monetary policy rule in place, are consistent with an equilibrium
allocation that is independent of the evolution of nominal variables, with
no account given of the mechanism (other than an “invisible hand”) that
will bring about those price level changes.
Next, a relation is derived between the economy’s average price
markup and aggregate output. Notice that independently of the nature
4 An alternative representation of the same equation in terms of the real marginal cost is
often found in the literature (see, e.g., Galí and Gertler (1999)). Deﬁning the (log) average
real marginal cost as mct = ψt −pt and noting that mct = −µt we can write (17) as:
πt = βEt{πt+1} + λ
mct

CHAPTER 3
of price setting, the average price markup can be expressed as
µt = pt −ψt
= −(wt −pt) + (at −αnt + log(1 −α))
= −(σ yt + ϕnt) + (at −αnt + log(1 −α))
= −

σ + ϕ + α
1 −α

yt +
1 + ϕ
1 −α

at + log(1 −α)
(18)
where derivation of the second and third equalities make use of the
household’s optimality condition (2) and the relation between aggregate
employment and output (14).
As discussed above, under ﬂexible prices (θ = 0) the average markup
is constant and equal to the desired one, µ. Deﬁning the natural level of
output, denoted by yn
t , as the equilibrium level of output under ﬂexible
prices, and evaluating (18) at the ﬂexible price equilibrium yields:
µ = −

σ + ϕ + α
1 −α

yn
t +
1 + ϕ
1 −α

at + log(1 −α)
(19)
thus implying
yn
t = ψyaat + ψy
(20)
where ψy ≡−(1−α)(µ−log(1−α))
σ(1−α)+ϕ+α
> 0 and ψya ≡
1+ϕ
σ(1−α)+ϕ+α. Notice that
when µ = 0 (perfect competition) the natural level of output corresponds
to the equilibrium level of output in the baseline classical monetary
economy analyzed in chapter 2. The presence of market power by ﬁrms
has the effect of lowering the average level of output, without affecting
its response to changes in technology. Note also that the natural level
of output is independent of monetary policy, and invariant to preference
shocks {zt}, two properties that also characterized the equilibrium of the
baseline classical monetary model of chapter 2.
Subtracting (19) from (18) yields
µt = −

σ + ϕ + α
1 −α

(yt −yn
t )
(21)
that is, the markup gap is proportional to the log deviation of output
from its ﬂexible price counterpart. Following convention, the latter
deviation is referred to as the output gap, and denoted by yt ≡yt −yn
t .

63
By combining (21) with (17) one can obtain an equation relating
inﬂation to its one period ahead forecast and the output gap
πt = βEt{πt+1} + κyt
(22)
where κ ≡λ

σ + ϕ+α
1−α

. Equation (22) is often referred to as the New
Keynesian Phillips curve (or NKPC, for short), and constitutes one of the
key building blocks of the basic New Keynesian model.
The second key equation describing the equilibrium of the New
Keynesian model can be obtained by rewriting (13) in terms of the output
gap as
yt = −1
σ (it −Et{πt+1} −rn
t ) + Et{yt+1}
(23)
where rn
t is the natural rate of interest, that is, the real interest rate
that would prevail in the ﬂexible price equilibrium. Under the assumed
processes for {zt} and {at} it is given by
rn
t = ρ −σ(1 −ρa)ψyaat + (1 −ρz)zt
(24)
Henceforth (23) is referred to as the dynamic IS equation (or DIS,
for short). Under the assumption that the effects of nominal rigidities
vanish asymptotically, limT−→∞Et{yt+T} = 0. In that case one can solve
equation (23) forward to yield the expression
yt = −1
σ
∞

k=0
Et{rt+k −rn
t+k}
(25)
where rt ≡it −Et{πt+1} is the expected real return on a one period
bond (i.e., the real interest rate). The previous expression emphasizes
the fact that the output gap is inversely related to the sum of current
and anticipated deviations between the real interest rate and its natural
counterpart.
Equations (22) and (23), together with an equilibrium process for
the natural rate rn
t (given by (24) under the assumptions made above),
constitute the nonpolicy block of the basic New Keynesian model. That
block has a simple structure: The NKPC determines inﬂation given a
path for the output gap, whereas the DIS equation determines the output
gap given a path for the (exogenous) natural rate and the actual real
rate, with the latter being a function of the nominal rate and (expected)
inﬂation.

CHAPTER 3
In order to close the model, those two equations must be supplemented
with one or more equations determining how the nominal interest rate it
evolves over time, that is, with a description of how monetary policy
is conducted. Thus, and in contrast with the baseline classical model
analyzed in chapter 2, the presence of sticky prices implies that the
equilibrium path of real variables cannot be determined independently
of monetary policy. In other words, monetary policy is non-neutral.
In order to illustrate the workings of the basic model just developed,
two alternative speciﬁcations of monetary policy are considered and their
equilibrium implications are analyzed.
3.4 EQUILIBRIUM DYNAMICS UNDER ALTERNATIVE MONETARY
POLICY RULES
3.4.1 Equilibrium under a Simple Interest Rate Rule
The equilibrium is ﬁrst analyzed under a simple interest rate rule of the
form
it = ρ + φππt + φyyt + vt
(26)
where yt ≡yt −y denotes the deviation of output from its steady
state value, and vt is an exogenous monetary policy shock that evolves
according to the AR(1) process:
vt = ρvvt−1 + εv
t
where ρv ∈[0, 1). A positive (negative) realization of εv
t should be
interpreted as a contractionary (expansionary) monetary policy shock,
leading to a rise (decline) in the nominal interest rate, given inﬂation and
output.
Coefﬁcients φπ and φy are chosen by the monetary authority, and
assumed to be non-negative. Note that the choice of the intercept ρ makes
the rule consistent with a zero inﬂation steady state. The speciﬁcation of
interest rate rule (26) is broadly consistent with the rule proposed by
Taylor (1993, 1999) as a good description of Fed monetary policy under
the tenure of Chairman Greenspan, and widely known as the “Taylor
rule.”5
5 Taylor’s original rule takes the form:
i F
t = 4 + 1.5(πt −2) + 0.5(yt −y∗
t )
where i F
t is the (annualized) federal funds rate, πt is year-on-year inﬂation, and y∗
t is trend
(log) GDP, ﬁtted by means of an estimated linear function of time. Note that the Taylor

65
Note that (26) can be rewritten in terms of the output gap as follows:
it = ρ + φππt + φyyt + φyyn
t + vt
where yn
t ≡yn
t −y.
After combining (22), (23), and (26), the equilibrium conditions can
be represented by means of the following system of difference equations,
 yt
πt

= AT

Et{yt+1}
Et{πt+1}

+ BTut
(27)
where
ut ≡rn
t −φyyn
t −vt
= −ψya(φy + σ(1 −ρa))at + (1 −ρz)zt −vt
and
AT ≡

σ
1 −βφπ
σκ
κ + β(σ + φy)

;
BT ≡

1
κ

with  ≡
1
σ+φy+κφπ .
Given that both the output gap and inﬂation are non-predetermined
variables, the solution to (27) is locally unique, if and only if, AT has both
eigenvalues within the unit circle.6 Under the assumption of non-negative
coefﬁcients (φπ, φy) it can be shown that a necessary and sufﬁcient
condition for uniqueness is given by 7
κ(φπ −1) + (1 −β)φy > 0
(28)
which is assumed to hold, unless stated otherwise. An economic interpre-
tation to the previous condition will be offered in chapter 4.
The method of undetermined coefﬁcients can be used in order to solve
for the economy’s response to different exogenous shocks, under the
assumption of a unique equilibrium. Assume that ut follows an AR(1)
rule above implicitly assumed an 2 percent annual inﬂation target and a 2 percent steady
state real interest rate.
6 See, e.g., Blanchard and Kahn (1980).
7 See Bullard and Mitra (2002) for a proof.

CHAPTER 3
process, with autoregressive coefﬁcient ρu ∈[0, 1) (this assumption is
relaxed below, when the different shocks are analyzed separately). The
stationary solution to (27) is conjectured to be of the form yt = ψyut and
πt = ψπut. Imposing the conjectured relations into (27) allows one to
solve for the undetermined coefﬁcients ψy and ψπ:
ψy = (1 −βρu)u
(29)
ψπ = κu
(30)
where u ≡
1
(1−βρu)[σ(1−ρu)+φy]+κ(φπ−ρu) > 0.
The following sections make use of the previous result to analyze the
economy’s equilibrium response to different types of exogenous shocks,
when the central bank follows the interest rate rule (26).
3.4.1.1 THE EFFECTS OF A MONETARY POLICY SHOCK
The focus is here on the economy’s response to a shift in vt, with
at = zt = 0 for all t. Note ﬁrst that neither the natural rate of interest,
rn
t , nor the natural level of output, yn
t , depends on the monetary policy
shock, vt. Using (29) and (30) and the fact that ∂ut
∂vt = −1, it follows that
yt = yt = −(1 −βρv)vvt
and
πt = −κvvt
where v takes the same form as u above, with ρu replaced by ρv (a
similar rule applies in the deﬁnition of a below). Thus, both output and
inﬂation decline in response to an exogenous increase in the interest rate.
The same is true for employment, given (14), and the real wage, given (2).
One can use (23) to obtain an expression for the real interest rate as a
function of the monetary policy shock
rt = σ(1 −ρv)(1 −βρv)vvt
which is thus shown to increase unambiguously in response to an
exogenous increase in the nominal rate.
The response of the nominal interest rate combines both the direct
effect of vt and the variation induced by lower output and inﬂation. It is

67
given by
it = rt + Et{πt+1} = [σ(1 −ρv)(1 −βρv) −ρvκ]vvt
Note that if the persistence of the monetary policy shock ρv is
sufﬁciently high, the nominal rate will decline in response to a rise in
vt. In that case the downward adjustment in the nominal rate induced by
the decline in inﬂation and output more than offsets the direct effect of
a higher vt. But even in that case, the increase in vt has a contractionary
effect on output, because the latter is inversely related to the real rate,
which goes up unambiguously, as seen above.
Finally, one can use (4) to determine the change in the money supply
required to bring about the desired change in the interest rate:
mt = pt + yt −ηit
= pt−1 −v[(1 −βρv)(1 + ησ(1 −ρv)) + (1 −ηρv)κ]vt
The sign of the change in the money supply that is needed to support
the exogenous policy intervention is, in principle, ambiguous. Note,
however, that dit/dvt > 0 is a sufﬁcient condition for a contraction in the
money supply in response to an exogenous monetary policy tightening.
It is also a sufﬁcient condition for the presence of a liquidity effect (i.e.,
a negative short-run comovement of the nominal rate and the money
supply in response to an exogenous monetary policy shock).
The previous analysis can be used to quantify the effects of a mon-
etary policy shock, given numerical values for the model’s parameters.
A baseline calibration of the model is presented next.
All quantitative results throughout the book are based on calibrations
that take each period in the model to correspond to a quarter. In the
baseline calibration of the model’s preference parameters it is assumed
β = 0.99, which implies a steady state real (annualized) return on
ﬁnancial assets of about 4 percent. It is also assumed σ = 1 (log utility)
and ϕ = 5 (which implies a Frisch elasticity of labor supply of 0.2),
α = 1/4, and ϵ = 9 (implying M = 1.125, i.e., a steady state markup
of a 12.5 percent). These are values broadly similar to those found in the
business cycle literature. The interest semielasticity of money demand,
η, is set to equal 4.8 In addition it is assumed θ = 3/4, which implies
8 The calibration of η is based on the estimates of an OLS regression of (log) M2 inverse
velocity on the 3 month Treasury Bill rate (quarterly rate, per unit), using quarterly data
over the period 1960:1–1988:1. The focus is on that period because it is characterized by a
highly stable relationship between velocity and the nominal rate, as implied by the model.

CHAPTER 3
an average price duration of four quarters, a value consistent with much
of the empirical evidence.9 As to the interest rate rule coefﬁcients, it is
assumed φπ = 1.5 and φy = 0.5/4, in a way consistent with Taylor’s
original rule.10 Finally, ρv = 0.5, a setting associated with a moderately
persistent shock.
Figure 3.1 illustrates the dynamic effects of a contractionary monetary
policy shock on a number of macro variables. The shock takes the form
of an increase of 25 basis points in εv
t , which, in the absence of a further
change induced by the response of inﬂation or the output gap, would
imply an increase of 100 basis points in the annualized nominal rate, on
impact. The responses of inﬂation and the two interest rates shown in
ﬁgure 3.1 (and in all subsequent ﬁgures) are expressed in annual terms,
that is, they are obtained by multiplying by 4 the responses of πt, it, and
rt implied by the quarterly model.
In a way consistent with the analytical results above it is seen that the
policy shock generates a decrease in inﬂation, output (whose response
corresponds to that of the output gap, because the natural level of output
is not affected by the monetary policy shock), employment, and the real
wage. Note that under the baseline calibration the nominal rate goes
up, though by less than its exogenous component—as a result of the
downward adjustment induced by the decline in inﬂation and output.
Note also that the increase in the real rate is larger than that of the
nominal rate as a result of the decrease in expected inﬂation. That
persistent increase in the real rate is the factor behind the decline of
consumption and output, as implied by (25), and given the constancy
of the natural rate.
In order to bring about the observed rise in the nominal interest
rate, the central bank must engineer a large short-run reduction in the
money supply. The calibrated model thus displays a liquidity effect. Note
also that the negative response of the price level to the tightening of
monetary policy builds up gradually, and is much more muted in the
short run than that of the money supply, which instead overshoots its
new permanent plateau. In the long run, however, the price level and
the money experience a permanent decline of identical size, since real
balances revert back to their initial level.
Overall, the dynamic responses to a monetary policy shock shown in
ﬁgure 3.1 are similar, at least in a qualitative sense, to those estimated
9 See, in particular, the estimates in Galí, Gertler, and López-Salido (2001) and Sbordone
(2002), based on aggregate data and the discussion of the micro evidence in chapter 1.
10 See, e.g., Taylor (1999). Note that empirical interest rate rules are generally estimated
using inﬂation and interest rate data expressed in annual rates. Conversion to quarterly
rates requires that the output gap coefﬁcient be divided by 4.

Output gap
Inflation
Output
Employment
Real wage
Price level
Nominal rate
Real rate
Money supply
v
–0.15
–0.05
Figure 3.1. Dynamic Responses to a Monetary Policy Shock: Interest Rate Rule.
using structural vector autoregressive (VAR) methods, as described in
chapter 1. Nevertheless, and as emphasized in Christiano, Eichenbaum,
and Evans (2005), among others, matching some of the quantitative
features of the empirical impulse responses requires that the basic New
Keynesian model be enriched in a variety of dimensions.

CHAPTER 3
Output gap
Inflation
Output
Employment
Real wage
Price level
Nominal rate
Real rate
Money supply
z
–0.15
–0.05
Figure 3.2. Dynamic Responses to a Discount Rate Shock: Interest Rate Rule.
3.4.1.2 THE EFFECTS OF A DISCOUNT RATE SHOCK
Figure 3.2 displays the dynamic responses of different macro variables to
a discount factor shock, in the form of a decrease in zt. Like in the case of
the monetary policy shock, the corresponding autoregressive coefﬁcient
is set to ρz = 0.5. The size of the initial shock εz
t is normalized to −0.5

71
percentage points, so that ∂rn
t
∂εz
t = (1−ρz)εz
t = −0.25, implying an increase
on impact of one percentage point in the (annualized) natural rate of
interest. A decline in zt should be interpreted as a reduction in the weight
that households give to current utility relative to future utility. That shift
in preferences induces a decline in consumption and hence in aggregate
demand.
As shown in ﬁgure 3.2, the decline in zt leads to a contraction in
output, employment, inﬂation, and the real wage. In fact, and given the
normalization of the size of the shock, the response of those variables is
identical to that describing the effects of a monetary policy tightening,
as shown in ﬁgure 3.1. Formally, the reason for this is that (1 −ρz)zt
and vt enter symmetrically (though with opposite sign) in the system
(27) describing the equilibrium dynamics for inﬂation and the output gap
under the interest rate rule considered here. Given that zt doesn’t affect
the natural level of output either, the effects on output, employment, and
the real wage are also identical.
Discount rate shocks and monetary policy shocks differ in two
respects, however: (i) shifts in the discount factor have an effect on the
natural rate of interest rn
t , whereas monetary policy shocks don’t (see
(24)), and (ii) monetary policy shocks lead to changes in the nominal
interest rate, for any given levels of inﬂation and output, whereas
discount factor shocks don’t (see (26)). As a result, the effects of the
two shocks on the nominal and real interest rates are very different,
as a comparison of ﬁgures 3.1 and 3.2 makes clear. In particular, the
nominal rate falls in response to a negative discount factor shock, due
to the decline in inﬂation and output. The decline in the nominal rate
drags the real rate down, given the sluggish change in expected inﬂation.
The decline in the real interest rate, however, is not sufﬁcient to prevent
the overall contraction in economic activity. Note also that the different
response of the nominal rate is associated with a very different pattern in
the response of the money supply, which now rises in the short run (due
to the dominant effect of a lower nominal rate), before it declines and
settles at a permanently lower level (the same as the price level, which in
turn corresponds to that implied by the monetary policy shock).
3.4.1.3 THE EFFECTS OF A TECHNOLOGY SHOCK
Next, the effects of exogenous changes in at are considered. Given (27)
and the analysis of its solution above, it follows that
yt = −ψya(φy + σ(1 −ρa))(1 −βρa)aat

CHAPTER 3
and
πt = −ψya(φy + σ(1 −ρa))κaat
where a is equal to u above, with ρa replacing ρu. Thus, a positive
technology shock has an unambiguous negative effect on the output gap
and inﬂation.
Output is now given by
yt = yt + yn
t
= ψyaκ(φπ −ρa)aat
It is easy to check that κ(φπ −ρa)a
∈(0, 1). Thus, a positive
technology shock always increases output, but by less than its natural
counterpart, thus generating a negative output gap, as seen above. The
response of employment is given by
nt =

1
1 −α

(yt −at)
=
(1 −σ)κ(φπ −ρa)
σ(1 −α) + ϕ + α −(φy + σ(1 −ρa))(1 −βρa)

aat
Hence, the sign of the response of employment to a positive technology
shock is in general ambiguous, depending on the conﬁguration of
parameter values, including the interest rate rule coefﬁcients. Note,
however, that σ
≥1 is a sufﬁcient condition for a technological
improvement to cause a decline in employment. The same is true if φy
is sufﬁciently large, that is, if the central bank puts enough weight on
output stabilization, even in the face of ﬂuctuations in natural output
resulting from changes in technology. Such a response of employment is
consistent with much of the recent empirical evidence on the effects of
technology shocks.11
Figure 3.3 shows the dynamic response of several macro variables
to a one percent increase in technology, under the baseline calibration
described above, and the assumption of ρa = 0.9. In a way consistent
with the analysis above, the output gap and inﬂation are shown to decline
persistently in response to the positive technology shocks, even though
output itself expands.12 Under the baseline calibration employment
11 See, e.g., Galí (1999) and Basu, Fernald, and Kimball (2004), among others. Galí and
Rabanal (2004) provide a survey of that empirical evidence.
12 Under the assumed calibration ϕya = 1, implying that the response of the natural level
of output corresponds to that of technology, at. Note that the response of output falls short
of the technology response.

Output gap
Inflation
Output
Employment
Real wage
Price level
Nominal rate
Real rate
Money supply
a
–0.15
–0.05
Figure 3.3. Dynamic Responses to a Technology Shock: Interest Rate Rule.
experiences a large and persistent decline. Thus, technology shocks
generate a negative comovement between output and employment, which
contrasts with the large and positive unconditional correlation between
the cyclical components of output and employment (or work hours)

CHAPTER 3
observed in the data, but is consistent with the negative estimates of that
correlation conditional on technology shocks.13
The nominal interest rate goes down substantially, due to the dominant
inﬂuence of lower inﬂation in shaping the central bank’s response. As a
result, the real rate also declines, but given the response of the output
gap (and (25)) we can infer that such decline is not sufﬁcient to match
that of its natural rate counterpart. Finally, note that the money supply
increases in the short run in order to support the lower nominal rate and
to accommodate the increase in money demand resulting from higher
output. Over time, however, those two requirements vanish, while the
permanently lower price level requires a permanent reduction in the
quantity of money in circulation, as shown in ﬁgure 3.3.
3.4.2 Equilibrium under an Exogenous Money Supply
Next the equilibrium dynamics of the basic New Keynesian model are
analyzed under the assumption of an exogenous path for the growth
rate of the money supply, mt. As discussed in chapter 2, the fact that
the policy rule is speciﬁed in terms of the money supply requires that
the money demand equation (4) is included in the set of conditions
needed to solve for the model’s equilibrium (i.e., beyond its usefulness
to back out the quantity of money that supports a given interest rate
policy, as in the previous subsection).
As a preliminary step, it is useful to rewrite money demand condition
in terms of the output gap
lt = yt −ηit + yn
t
(31)
where lt ≡mt −pt denotes real balances. Substituting the latter equation
into (23) to eliminate the interest rate yields
(1 + ση) yt = σηEt{yt+1} +lt + ηEt{πt+1} + ηrn
t −yn
t
(32)
where, as usual, a “^” symbol on top of a variable refers to deviations of
the latter from steady state.
Note also that real balances are related to inﬂation and money growth
through the identity
lt−1 = lt + πt −mt
(33)
13 See Galí (1999).

75
Hence, the equilibrium dynamics for real balances, output gap, and
inﬂation are described by equations (32) and (33) together with the
NKPC equation (22). They can be summarized compactly by the system
AM,0


yt
πt
lt−1

= AM,1


Et{yt+1}
Et{πt+1}
lt

+ BM


rn
t
yn
t
mt


(34)
where
AM,0 ≡


1 + ση
0
0
−κ
1
0
0
−1 1

;
AM,1 ≡


ση η 1
0
β 0
0
0 1

;
BM ≡


η −1
0
0
0
0
0
0
−1


and with rn
t and yn
t deﬁned as in (24) and (20) as a function of the
exogenous technology and discount factor shocks.
The system above has one predetermined variable (lt−1) and two non-
predetermined variables (yt and πt). Accordingly, a stationary solution
will exist and be unique, if and only if, AM ≡A−1
M,0AM,1 has two
eigenvalues inside and one outside (or on) the unit circle. The latter
condition can be shown to be always satisﬁed so, in contrast with the
interest rate rule discussed above, the equilibrium is always determined
under an exogenous path for the money supply.14
Next the equilibrium responses of the economy to different exogenous
shocks are examined.
3.4.2.1 THE EFFECTS OF A MONETARY POLICY SHOCK
In order to illustrate how the economy responds to an exogenous shock
to the money supply, assume that its growth rate mt follows the AR(1)
process
mt = ρmmt−1 + εm
t
(35)
where ρm ∈[0, 1) and {εm
t } is white noise.
The economy’s response to a monetary policy shock can be obtained
by determining the stationary solution to the dynamical system consisting
of (34) and (35) tracing the effects of a shock to εm
t
(while setting
rn
t
= yn
t = 0, for all t).15 In doing so, it is assumed that ρm = 0.5,
14 That result is based on numerical analysis of the eigenvalues for a broad range of
calibrations of the model’s parameter values.
15 See, e.g., Blanchard and Kahn (1980) for a description of a solution method.

CHAPTER 3
Output gap
Inflation
Output
Employment
Real wage
Price level
Nominal rate
Real rate
Money supply
dm
Figure 3.4. Dynamic Responses to a Monetary Policy Shock: Money Supply
Rule.
a value roughly consistent with the ﬁrst-order autocorrelation of money
growth in postwar U.S. data.
Figure 3.4 displays the dynamic responses of several variables of
interest to an expansionary monetary policy shock that takes the form
of a positive realization of εm
t
of size 0.25. That impulse corresponds

77
to a one percent increase, on impact, in the annualized rate of money
growth. The sluggish adjustment of prices implies that real balances rise
in response to the increase in the money supply. As a result, clearing
of the money market requires either a rise in output and/or a decline in
the nominal rate. Under the calibration considered here, output (and the
output gap, since natural output is unaffected) increases by about a third
of a percentage point on impact, after which it slowly reverts back to its
initial level. The nominal rate, however, shows a slight increase. Hence,
and in contrast with the case of the interest rate rule considered above, a
liquidity effect does not emerge here. Note, however, that the rise in the
nominal rate does not prevent the real rate from declining persistently
(due to higher expected inﬂation), leading in turn to an expansion in
aggregate demand and output, as implied by (25), and, as a result, a
persistent rise in inﬂation, which follows from (22).
It is worth noting that the absence of a liquidity effect is not a necessary
feature of the exogenous money supply regime considered here, but
instead a consequence of the calibration used. To see this, note that one
can combine equations (4) and (23) to obtain the difference equation
it =
η
1 + η Et{it+1} +
ρm
1 + ηmt + σ −1
1 + η Et{yt+1}
whose forward solution yields
it =
ρm
1 + η(1 −ρm) mt + σ −1
1 + η
∞

k=0

η
1 + η
	k
Et{yt+1+k}
Note that when σ = 1, as in the assumed baseline calibration, the
nominal rate always comoves positively with money growth. Neverthe-
less, and given that quite generally the summation term on the right-hand
side will be negative (since for most calibrations output tends to adjust
monotonically to its original level after the initial increase), a liquidity
effect emerges given a value for σ sufﬁciently above one combined with
a sufﬁciently low value for ρm.16
3.4.2.2 THE EFFECTS OF A DISCOUNT RATE SHOCK
Figure 3.5 displays the effects of a contractionary discount rate shock,
identical to the one analyzed above, but now under the assumption of an
exogenous money growth rule, implying the absence of a response in the
money supply to the shock, that is, mt = 0 for all t.
16 See Galí (2003) for a detailed analysis.

CHAPTER 3
Output gap
Inflation
Output
Employment
Real wage
Price level
Nominal rate
Real rate
Money supply
z
–0.08
–0.06
–0.04
–0.02
Figure 3.5. Dynamic Responses to a Discount Rate Shock: Money Supply Rule
Note that the dynamic effects on output and employment are, at ﬁrst
sight, qualitatively similar to those derived under an interest rate rule.
But this is not the case, strictly speaking. The reason is simple: under
monetary targeting the price level returns to its original value, which
requires that inﬂation eventually turns positive after its initial decline, as
shown in ﬁgure 3.5. It follows that output (as well as employment and the

79
real wage, as a result) must also overshoot its initial level, which in turn
requires that the real rate eventually stays below its natural counterpart
(none of these effects can be easily seen in the Figure, however).
Intuitively, the reason for the different effects of the discount rate
shock under the monetary targeting rule is that the latter is effectively
equivalent to an interest rate rule that targets the price level (as op-
posed to inﬂation). To see this, note that we can rewrite (4) (ignoring
constants) as
it =
1
η

(pt −mt−1) +
1
η

yt + vt
=
1
η

(pt−1 −mt−1) +
1
η

πt +
1
η

yt + vt
where vt ≡−(1/η)mt. Note that the previous rule is of the same
form as (26), with the additional term involving (pt−1 −mt−1) appended.
Thus, and in the absence of a change in the money supply, the interest
rate will adjust endogenously to (lagged) deviations between the price
level from the implicit price level target which is given by mt−1. That
systematic response guarantees the stationarity of the price level in
response to any shock (other than a shock to the growth rate of money
itself).
3.4.2.3 THE EFFECTS OF A TECHNOLOGY SHOCK
Finally, the effects of a technology shock under an exogenous money
supply are analyzed next. Once again, assume the technology parameter
at follows the stationary process given by (6). In a way consistent with
the assumption of exogenous money, it is assumed that mt = 0 for all t
for the purpose of the present exercise.
Figure 3.6 displays the dynamic responses to a one percent increase in
the technology. A comparison with the responses shown in ﬁgure 3.2
(corresponding to the analogous exercise under an interest rate rule)
reveals some similarities: In both cases the output gap (and, hence,
inﬂation) displays a negative response to the technology improvement,
as a result of output failing to increase as much as its natural level.
Note, however, that in the case of exogenous money the gap between
output and its natural level is much larger, which also explains the
larger decline in employment. This is due to the upward response of
the real rate implied by the unchanged money supply, which contrasts
with its decline (in response to the negative response of inﬂation and the
output gap) under the interest rate rule. Because the natural real rate
also declines in response to the positive technology shock (in order to

CHAPTER 3
support the transitory increase in output and consumption), the response
of interest rates generated under the exogenous money regime becomes
highly contractionary, relative to the equilibrium under ﬂexible prices.
As in the case of a discount rate shock analyzed above (but in contrast
with the response to a technology shock under the simple interest rate
rule) the price level is stationary and returns gradually to its original
level after its initial decline, which requires that inﬂation eventually turn
positive.
The previous simulations have served several goals. First, they have
helped illustrate the workings of the New Keynesian model, that is,
how the model can be used to answer some speciﬁc questions about
the behavior of the economy under different assumptions regarding the
monetary policy rule in place. Second, under a plausible calibration, it
was seen how the simulated responses to some shocks (monetary policy
shocks, in particular) display notable similarities (at least qualitative)
with the empirical evidence on their effects. Third, the previous analysis
has made clear that monetary policy in the New Keynesian model can
have large and persistent effects on both real and nominal variables. The
latter feature leads one to raise a natural question, which is the focus of
the next chapter: How should monetary policy be conducted?
3.5 NOTES ON THE LITERATURE
Early examples of microfounded monetary models with monopolistic
competition and sticky prices can be found in Akerlof and Yellen (1985),
Mankiw (1985), Blanchard and Kiyotaki (1987), and Ball and Romer
(1990).
An early version and analysis of the baseline New Keynesian model
can be found in Yun (1996), which used a discrete-time version of the
staggered price-setting model originally developed in Calvo (1983). King
and Wolman (1996) provide a detailed analysis of the steady state and
dynamic properties of that model. King and Watson (1996) compare its
predictions regarding the cyclical properties of money, interest rates, and
prices with those of ﬂexible price models. Woodford (1996) incorporates
a ﬁscal sector in the model and analyzes its properties under a non-
Ricardian ﬁscal policy regime.
An inﬂation equation identical to the New Keynesian Phillips curve can
be derived under the assumption of quadratic costs of price adjustment,
as shown in Rotemberg (1982). Hairault and Portier (1993) developed
and analyzed an early version of a monetary model with quadratic costs
of price adjustment and compared its second-moment predictions with
those of the French and U.S. economies.

Output gap
Inflation
Output
Employment
Real wage
Price level
Nominal rate
Real rate
Money supply
a
Figure 3.6. Dynamic Responses to a Technology Shock: Money Supply Rule.
The New Keynesian Phillips curve derived in the main text is based
on a log-linearization of the optimal price setting condition and the law
of motion for the aggregate price level around the zero inﬂation steady
state. Ascari (2004), Ascari and Ropele (2009), and Cogley and Sbordone
(2008) analyze the consequences for inﬂation dynamics of a steady state
with nonzero inﬂation.

CHAPTER 3
Two main alternatives to the Calvo random price duration model
can be found in the literature. The ﬁrst one is given by staggered
price-setting models with a deterministic price duration, originally pro-
posed by Taylor (1980) in the context of a non-microfounded model.
A microfounded version of the Taylor model can be found in Chari, Kehoe,
and McGrattan (2000), who analyzed the output effects of exogenous
monetary policy shocks. An alternative price-setting structure is given
by state dependent models in which the timing of price adjustments is
inﬂuenced by the state of the economy. A quantitative analysis of a state
dependent pricing model can be found in Dotsey, King, and Wolman
(1999) and, more recently, in Golosov and Lucas (2007), Gertler and
Leahy (2008), and Midrigan (2011). Klenow and Kryvtsov (2008) and
Nakamura and Steinsson (2008) examine the ability of state dependent
models to account for the price patterns found in the micro evidence.
The empirical performance of the New Keynesian Phillips curve
has always been controversial. An early critical assessment can be
found in Fuhrer and Moore (1995). Mankiw and Reis (2002) give a
quantitative review of the perceived shortcomings of the NKPC and
propose an alternative price-setting structure based on the assumption
of sticky information. Galí and Gertler (1999), Sbordone (2002), and
Galí, Gertler, and López-Salido (2001) provide favorable evidence of
the empirical ﬁt of the equation relating inﬂation to marginal costs,
and discuss the difﬁculties in estimating or testing the NKPC given the
unobservability of the output gap. Mavroeidis, Plagborg-Moller, and
Stock (2013) overview the empirical literature on the NKPC, focusing
on the problem of weak identiﬁcation and its consequences.
Taylor (1993, 1999) put forward the notion that a simple interest
rate rule that responds systematically to inﬂation and detrended output
approximates fairly well, when its coefﬁcients are chosen appropriately,
the path of the federal funds rate in the Greenspan years. Empirical
evidence on the stability of the Taylor rule over time and across different
countries can be found in Clarida, Galí, and Gertler (1998, 2000) and
Orphanides (2003), among others.
Rotemberg and Woodford (1999) and Christiano, Eichenbaum, and
Evans (1999, 2005) provide empirical evidence on the effects of monetary
policy shocks, and discuss a number of modiﬁcations of the baseline New
Keynesian model aimed at improving the model’s ability to match the
estimated impulse responses.
Evidence on the effects of technology shocks and their implications
for the relevance of alternative models can be found in Galí (1999)
and Basu, Fernald, and Kimball (2004), among others. Recent evidence
as well as alternative interpretations are surveyed in Galí and Rabanal
(2004).

83
APPENDIX
3.1 OPTIMAL ALLOCATION OF CONSUMPTION EXPENDITURES
The problem of maximization of Ct for any given expenditure level
Xt ≡
 1
0
Pt(i)Ct(i)di
can be formalized by means of the Lagrangian
L =
 1
0
Ct(i)1−1
ϵ di

ϵ
ϵ−1
−λ
 1
0
Pt(i)Ct(i) di −Xt

The implied ﬁrst-order conditions are
Ct(i)−1
ϵ Ct
1
ϵ = λPt(i)
for all i ∈[0, 1]. Thus, for any two goods (i, j),
Ct(i) = Ct( j)
 Pt(i)
Pt( j)
	−ϵ
which can be substituted into the expression for consumption expendi-
tures to yield
Ct(i) =
 Pt(i)
Pt
	−ϵ Xt
Pt
for all i ∈[0, 1]. The latter condition can then be substituted into the
deﬁnition of Ct to obtain
 1
0
Pt(i)Ct(i)di = PtCt
Combining the two previous equations yields the demand schedule
Ct(i) =
 Pt(i)
Pt
	−ϵ
Ct

CHAPTER 3
3.2 AGGREGATE PRICE LEVEL DYNAMICS
Let S(t) ⊂[0, 1] represent the set of ﬁrms not reoptimizing their posted
price in period t. Using the deﬁnition of the aggregate price level and the
fact that all ﬁrms resetting prices will choose an identical price P∗
t ,
Pt =

S(t)
Pt−1(i)1−ϵdi + (1 −θ)(P∗
t )1−ϵ

1
1−ϵ
=

θ(Pt−1)1−ϵ + (1 −θ)(P∗
t )1−ϵ!
1
1−ϵ
where the second equality follows from the fact that the distribution
of prices among ﬁrms not adjusting in period t corresponds to the
distribution of effective prices in period t −1, though with total mass
reduced to θ.
Dividing both sides by Pt−1,

1−ϵ
t
= θ + (1 −θ)
 P∗
t
Pt−1
	1−ϵ
(36)
3.3 FIRM’S OBJECTIVE FUNCTION
The value of a ﬁrm in period t, expressed in terms of current consumption
is given by
Vt(i) =
∞

k=0
Et{t,t+k(Dt+k(i)/Pt+k)}
where Dt(i) ≡Pt(i)Yt(i) −Ct(Yt(i)).
Note that for a ﬁrm resetting its price in period t,
Et{t,t+k(Dt+k(i)/Pt+k)} = θkEt{t,t+k(Dt+k|t/Pt+k)}
+(1 −θ)
k

h=1
θk−hEt{t,t+k(Dt+k|t+h/Pt+k)}
(37)
where Dt+k|t ≡P∗
t Yt+k|t −Ct+k(Yt+k|t) denotes period t + k dividends
conditional on the price having been last reset in period t. Note that
the second term on the right-hand side of (37) is independent of P∗
t since

85
it involves states of nature for which the price has been reset at least once
after period t.
Thus, the value of a ﬁrm resetting its price in period t is given by
Vt|t =
∞

k=0
θkEt{t,t+k(Dt+k|t/Pt+k)} + ϒt
where ϒt is a term independent of P∗
t and hence can be ignored when
choosing the latter, as reﬂected in the objective function in the main text.
3.4 PRICE DISPERSION
Let pt(i) ≡pt(i) −pt. Notice that,
 Pt(i)
Pt
	1−ϵ
= exp [(1 −ϵ)pt(i)]
= 1 + (1 −ϵ)pt(i) + (1 −ϵ)2
2
pt(i)2
Note that from the deﬁnition of Pt, 1 =
 1

Pt(i)
Pt

1−ϵ
di. A second-
order approximation to this expression thus implies
Ei{pt(i)} = ϵ −1
2
Ei{pt(i)2}
In addition, a second-order approximation to

Pt(i)
Pt

−
ϵ
1−α yields
 Pt(i)
Pt
	−
ϵ
1−α
= 1 −
ϵ
1 −α pt(i) + 1
2

ϵ
1 −α
	2
pt(i)2
Combining the two previous results, it follows that
 1
0
 Pt(i)
Pt
	−
ϵ
1−α
di = 1 + 1
2

ϵ
1 −α
	 1
 Ei{pt(i)2}
= 1 + 1
2

ϵ
1 −α
	 1
 vari{pt(i)}

CHAPTER 3
where  ≡
1−α
1−α+αϵ , and where the last equality follows from the
observation that, up to second order,
 1
0
(pt(i) −pt)2 di ≃
 1
0
(pt(i) −Ei{pt(i)})2 di
≡vari{pt(i)}
Finally, using the deﬁnition of dt
and up to a second-order
approximation,
dt ≡(1 −α) log
 1
0
 Pt(i)
Pt
	−
ϵ
1−α
di ≃
ϵ
2vari{pt(i)}
EXERCISES
3.1. Interpreting discrete-time records of data on price adjustment
frequency
Suppose ﬁrms operate in continuous time, with the pdf for
the duration of the price of an individual good being f (t) =
φ exp(−φt), where t ∈R+ is expressed in month units.
a. Show that the implied instantaneous probability of a price
change is constant over time and given by φ.

89
b. What is the mean duration of a price? What is the median
duration? What is the relationship between the two?
c. Suppose that the prices of individual goods are recorded once
a month (say, on the ﬁrst day, for simplicity). Let λt denote
the fraction of items in a given goods category whose price in
month t is different from that recorded in month t −1 (Note:
of course, the price may have changed more than once since
the previous record.) How would you go about estimating
parameter φ?
d. Given information on monthly frequencies of price adjustment,
how would you go about calibrating parameter θ in a quarterly
Calvo model?
3.2. Introducing government purchases in the basic New Keynesian
model
Assume that the government purchases quantity Gt(i) of good i,
for all i ∈[0, 1]. Let Gt ≡

 1
0 Gt(i)1−1
ϵ di

ϵ
ϵ−1 denote an index
of public consumption, which the government seeks to maximize
for any level of expenditures
 1
0 Pt(i)Gt(i)di. Assume government
expenditures are ﬁnanced by means of lump-sum taxes.
a. Derive an expression for total demand facing ﬁrm i.
b. Derive a log-linear aggregate goods market clearing condition
that is valid around a steady state with a constant public
consumption share SG ≡G
Y .
c. Derive the corresponding expression for average real marginal
cost as a function of aggregate output, government purchases,
and technology and provide some intuition for the effect of
government purchases.
d. How is the equilibrium relationship linking interest rates
to current and expected output affected by the presence of
government purchases?
3.3. Government purchases and sticky prices
Consider a model economy with the following equilibrium con-
ditions. The household’s log-linearized Euler equation takes the
form
ct = −1
σ (it −Et{πt+1} −ρ) + Et{ct+1}
where ct is consumption, it is the nominal rate, and πt+1 ≡
pt+1 −pt is the rate of inﬂation between t and t + 1 (Note: as in

CHAPTER 3
the text, lowercase letters denote the logs of the original variable.)
The household’s log-linearized labor supply is given by
wt −pt = σct + ϕnt
where wt denotes the nominal wage, pt is the price level, and nt is
employment.
Firms’ technology is given by
yt = nt
The time between price adjustments follows a geometric distribu-
tion, which gives rise to an inﬂation equation
πt = βEt{πt+1} + κyt
where yt ≡yt −yn
t is the output gap (with yn
t representing the
natural level of output). Assume that in the absence of constraints
on price adjustment ﬁrms would set a price equal to a constant
markup over marginal cost given by µ (in logs).
Suppose that the government purchases a fraction τt of the
output of each good, with τt varying exogenously. Government
purchases are ﬁnanced through lump-sum taxes.
a. Derive a log-linear version of the goods market clearing
condition of the form yt = ct + gt, where gt ≡−log(1 −τt).
b. Determine the behavior of the natural level of output yn
t as
a function of gt and discuss the mechanism through which a
ﬁscal expansion leads to an increase in output when prices are
ﬂexible.
c. Assume that {gt} follows a simple AR(1) process with autore-
gressive coefﬁcient ρg ∈[0, 1). Derive the dynamic IS equation
yt = Et{yt+1} −1
σ (it −Et{πt+1} −rn
t )
together with an expression for the natural rate rn
t as a function
of gt.

91
d. Determine the economy’s response to an exogenous increase in
gt when the central bank follows an interest rate rule given by
it = ρ + φππt
3.4. Indexation and the New Keynesian Phillips curve
Consider the Calvo model of staggered price setting with the
following modiﬁcation: In the periods between price reoptimiza-
tions ﬁrms mechanically adjust their prices according to some
indexation rule. Formally, a ﬁrm that reoptimizes its price in
period t (an event that occurs with probability 1 −θ) sets a price
P∗
t in that period. In subsequent periods (i.e., until it reoptimizes
prices again), its price is adjusted according to the following
indexation rule:
Pt+k|t = Pt+k−1|t(
t+k−1)ω
1−ω
for k = 1, 2, 3, ... and
Pt,t = P∗
t
where Pt+k|t denotes the price effective in period t + k for a
ﬁrm that last reoptimized its price in period t, 
t ≡
Pt
Pt−1 is the
aggregate gross inﬂation rate, 
 the latter’s steady state value, and
ω ∈[0, 1] is an exogenous parameter that measures the degree of
indexation to lagged inﬂation.
Suppose that all ﬁrms have access to the same constant returns
to scale technology and face a demand schedule with a constant
price elasticity ϵ.
The objective function for a ﬁrm reoptimizing its price in
period t (i.e., choosing P∗
t ) is given by
max
P∗
t
∞

k=0
θkEt

t,t+k(1/Pt+k)

Pt+k|tYt+k|t −Ct+k(Yt+k|t)

subject to a sequence of demand constraints (9), and the indexa-
tion rule described above. All variables are deﬁned as in the main
text.
a. Using
the
deﬁnition
of
the
price
level
index
Pt
≡

 1
0 Pt(i)1−ϵdi

1−ϵ , derive a log-linear expression for the evo-
lution of inﬂation πt as a function of the newly set price p∗
t .

CHAPTER 3
b. Derive the ﬁrst-order condition for the ﬁrm’s problem that
determines the optimal price P∗
t .
c. Log-linearize the ﬁrst-order condition around the correspond-
ing steady state and derive an expression for p∗
t (i.e., the
approximate log-linear price-setting rule).
d. Combine the results of (a) and (c) to derive an inﬂation
equation of the form
πt = γbπt−1 + γ f Et{πt+1} −λµt
where πt ≡πt −π.
3.5. Optimal price setting and equilibrium dynamics in the Taylor
model
Assume a continuum of ﬁrms indexed by i ∈[0, 1]. Each ﬁrm
produces a differentiated good, with a technology
Yt(i) = AtNt(i)
where At represents the level of technology, and at ≡log At
evolves exogenously according to some stationary stochastic
process.
During each period a fraction
1
N of ﬁrms reset their prices,
which then remain effective for N periods. Hence, a ﬁrm i setting
a new price P∗
t in period t will seek to maximize
max
P∗
t
N−1

k=0
Et

t,t+k(1/Pt+k)

P∗
t Yt+k|t −Ct+k(Yt+k|t)

subject to
Yt+k|t = (P∗
t /Pt+k)−ϵCt+k
where t,t+k ≡βk 
Ct+k
Ct

−σ
a. Show that P∗
t must satisfy the ﬁrst-order condition
N−1

k=0
Et

t,t+kYt+k|t(P∗
t −M
t+k

= 0
where 
t ≡C′
t(·) is the nominal marginal cost and M ≡
ϵ
ϵ−1.

93
b. Derive the following log-linearized optimal price-setting rule
(around a zero inﬂation steady state)
p∗
t = µ +
N−1

k=0
ωkEt {ψt+k}
where ωk ≡βk(1−β)
1−β N , ψt ≡log 
t and µ ≡log M. Show that in
the limiting case of β = 1 (no discounting) the above equation
can be rewritten as
p∗
t = µ + 1
N
N−1

k=0
Et {ψt+k}
How does the previous price-setting rule differ from the one
generated by the Calvo model?
c. Recalling the expression for the aggregate price index Pt ≡

 1
0 Pt(i)1−ϵ di

1−ϵ , show that around a zero inﬂation steady
state the (log) price level will satisfy
pt =
 1
N
	 N−1

k=0
p∗
t−k
d. Consider the particular case of N = 2 and β = 1 and assume
that the consumer’s (log) marginal rate of substitution between
labor and consumption is given by σct + ϕnt. Assume also that
all output is consumed. Show that:
p∗
t = 1
2 p∗
t−1 + 1
2 Et{p∗
t+1} + δ(yt + Et{yt+1})
where δ ≡σ + ϕ.
e. Assume that money demand takes the simple form mt −pt = yt
and that both mt and at follow (independent) random walks,
with innovations εm
t and εa
t , respectively. Derive a closed-form
expression for the output gap, employment, and the price level
as a function of the exogenous shocks.
f. Discuss the inﬂuence of δ on the persistence of the effects
of a monetary shock, and provide some intuition for that
result.

CHAPTER 3
3.6. The Mankiw-Reis model: Inﬂation dynamics under predeter-
mined prices
Suppose that each period a fraction of ﬁrms 1 −θ gets to choose
a path of future prices for their respective goods (a “price plan”),
while the remaining fraction θ keeps their current price plans.
Let {Pt,t+k}∞
k=0 denote the price plan chosen by ﬁrms that get
to revise that plan in period t. Firm’s technology is given by
Yt(i) = √AtNt(i). Consumer’s period utility is assumed to take
the form U(Ct, Nt) = Ct −N2
t
2 , where Ct ≡

 1
0 Ct(i)1−1
ϵ di

ϵ
ϵ−1 .
The demand for real balances is assumed to be given by Mt
Pt = Ct.
All output is consumed.
a. Let Pt ≡

 1
0 Pt(i)1−εdi

1−ε denote the aggregate price index.
Show that, up to a ﬁrst-order approximation,
pt = (1 −θ)
∞

j=0
θ j pt−j,t
(38)
b. A ﬁrm i, revising its price plan in period t will seek to maximize
∞

k=0
θkEt

t,t+k(1/Pt+k)Yt+k(i)

Pt,t+k −Wt+k
√At+k

Derive the ﬁrst-order condition associated with that problem,
and show that it implies the following approximate log-linear
rule for the price plan
pt,t+k = µ + Et{ψt+k}
(39)
for k = 0, 1, 2, ... and where ψt = wt −1
2at is the nominal
marginal cost.
c. Use the optimality conditions for the consumer’s problem, and
the labor market clearing condition to show that (i) the natural
level of output satisﬁes yn
t = −µ + at, and (ii) the (log) real
marginal cost (in deviation from its perfect foresight steady
state value) equals the output gap, i.e.,
"
mct = yt
for all t, where yt ≡yt −yn
t .

95
d. Using (38) and (39), show how one can derive the following
equation for inﬂation
πt = 1 −θ
θ
yt + 1 −θ
θ
∞

j=1
θ j Et−j{yt + πt}
(40)
e. Suppose that the money supply follows a random walk process
mt = mt−1 + ut, where mt ≡log Mt and {ut} is white noise.
Determine the dynamic response of output, employment, and
inﬂation to a money supply shock. Compare the implied re-
sponse to the one obtained under the standard New Keynesian
Phillips curve, where πt = βEt{πt+1} + κyt (Hint: use the fact
that in equilibrium yt = mt −pt, substitute for yt in (40)
in order to obtain a difference equation for the (log) price
level.)
f. Suppose that technology is described by the random walk
process at = at−1+εt, where at ≡log At, and {εt} is white noise.
Determine the dynamic response of output, the output gap,
employment, and inﬂation to a technology shock. Compare
the implied response to one obtained under the standard New
Keynesian Phillips curve, where πt = β Et{πt+1} + κ yt (Hint:
same as (e) above).
3.7. Technology shocks and the Taylor rule
Consider an economy with Calvo-type staggered price setting,
where a continuum of monopolistically competitive ﬁrms have
access to a technology Yt = AtNt, where Yt is output, Nt denotes
hours of work, and At is an exogenous technology parameter. The
representative consumer has a period utility U(Ct, Nt) = log Ct −
N1+ϕ
t
1+ϕ , where Ct is a CES function of the quantities consumed
of the different types of goods. The technology parameter at ≡
log At is assumed to follow a random walk process, i.e. at =
at−1 + εt, where {εt} is white noise. Firms’ desired markups are
constant. All output is consumed. The labor market is perfectly
competitive.
The implied equilibrium conditions take the form
yt = Et{yt+1} −(it −Et{πt+1} −ρ)
(41)
πt = βEt{πt+1} + κyt
(42)

CHAPTER 3
where yt ≡yt −yn
t is the output gap, yt is (log) output, yn
t is the
(log) natural level of output, πt ≡pt −pt−1 is the rate of inﬂation,
and it is the short-term nominal rate.
a. Determine the natural level of output yn
t as a function of the
technology parameter.
b. Suppose that the monetary authority adopts a simple interest
rate rule of the form
it = ρ + φππt
(43)
where φπ > 1. Determine the equilibrium path of inﬂation, the
output gap, and output.
c. How would your answer to (b) change if the technology
process was instead given by at = ρaat−1 + εt with ρa ∈(0, 1)?
Derive your result analytically and explain it intuitively.
3.8. A New Keynesian economy with linear utility
Consider an economy with Calvo-type staggered price setting,
where a continuum of monopolistically competitive ﬁrms have
access to a technology Yt = AtNt, where Yt is output, Nt denotes
employment, and At
is an exogenous technology parameter.
The representative consumer maximizes E0
#∞
t=0 βtU(Ct, Nt)

where the period utility is given by U(Ct, Nt) = Ct −N1+ϕ
t
1+ϕ , where
Ct is a CES function of the quantities consumed of the different
types of goods. Firms’ desired markup is constant. All output is
consumed. The labor market is perfectly competitive.
a. Determine the (log) natural level of employment

nn
t

and
output

yn
t

as a function of technology.
b. Explain, using a labor market diagram, why natural employ-
ment always rises in response to a positive technology shock
under the assumptions above.
c. Derive the consumer’s Euler equation and show that it implies
a constant real interest rate. Give some intuition for that result.
d. Write down a simple interest rate rule (with ﬁnite coefﬁcients
and a function of observables only) which will replicate the
natural (i.e., ﬂexible price) allocation. Explain why (short
proof).
3.9. A NKPC with backward-looking ﬁrms (based on Galí and Gertler
(1999)).
Consider the following modiﬁcation to the basic New Keynesian
model developed in the text: a fraction ω ∈[0, 1] of ﬁrms set

97
prices according to the following backward-looking rule:
pb
t = p∗
t−1 + πt−1
where
p∗
t = ωpb
t + (1 −ω)p f
t
is the average newly set (log) price in period t, with p f
t denoting
the (log) price set by forward-looking ﬁrms. The latter is given as
in the standard model by:
p f
t = µ + (1 −βθ)
∞

k=0
(βθ)kEt{ψt+k}
where, for simplicity, constant returns have been assumed
(α = 0).
Both backward- and forward-looking ﬁrms can reset their
prices with probability 1 −θ each period. Thus, the average (log)
price evolves according to:
pt = θpt−1 + (1 −θ)p∗
t
Assume, as in the standard model, that the following relationship
between the average markup and the output gap holds:
µt = −(σ + ϕ)yt
a. Show that the New Keynesian Phillips curve will now take the
form
πt = γbπt−1 + γ f Et{πt+1} + κyt
and determine the values of coefﬁcients γb, γ f , and κ as a
function of the model’s parameters.
b. Discuss the implications for the costs of disinﬂation, compared
to the standard New Keynesian Phillips curve.