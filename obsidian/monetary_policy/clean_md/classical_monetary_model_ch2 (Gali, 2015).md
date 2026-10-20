Chapter 2
A CLASSICAL MONETARY MODEL
This chapter presents a simple model of a classical monetary economy,
featuring perfect competition and fully ﬂexible prices in all markets.
As stressed below, many of the model’s predictions are at odds with
the evidence reviewed in chapter 1. That notwithstanding, the analysis
of the classical economy provides a benchmark that will be useful in
subsequent chapters when some of its strong assumptions are relaxed. It
also allows for the introduction of some notation, as well as assumptions
on preferences and technology that are used throughout the book.
Following much of the recent literature, the baseline classical model
developed here attaches a very limited role to money. Thus, in the ﬁrst
four sections of this chapter, the only explicit role played by money is to
serve as a unit of account. In that case, and as shown below, whenever
monetary policy is speciﬁed in terms of an interest rate rule, no reference
whatsoever needs to be made to the quantity of money in circulation in
order to determine the economy’s equilibrium. When the speciﬁcation
of monetary policy involves the money supply, a “conventional” money
demand equation is postulated in order to close the model, without
taking a stand on its microfoundations. In section 2.5, an explicit role
for money is introduced, beyond that of serving as a unit of account.
In particular, a version of the classical monetary model is analyzed in
which real balances are assumed to generate utility to households, and
the implications for monetary policy of alternative assumptions on the
properties of that utility function are explored.
Independently of how money is introduced, the proposed framework
assumes a representative household solving a dynamic optimization
problem. That problem and the associated optimality conditions are
described in section 2.1. Section 2.2 introduces the representative ﬁrm’s
technology and determines its optimal behavior under the assumption of
price and wage taking. Section 2.3 characterizes the equilibrium, and
shows how real variables are uniquely determined, independently of
monetary policy. Section 2.4 discusses the determination of the price level
and other nominal variables under alternative monetary policy rules.
Finally, section 2.5 analyzes a version of the model with money in the
utility function, and discusses the extent to which the conclusions drawn
from the earlier analysis need to be modiﬁed under that assumption.

CHAPTER 2
2.1 HOUSEHOLDS
The economy is assumed to be inhabited by a large number of identical
households. The representative household seeks to maximize the objec-
tive function:
E0
∞

t=0
βtU(Ct, Nt; Zt)
(1)
where Ct is the quantity consumed of the single good available in
the economy, Nt denotes hours of work or employment, and Zt is an
exogenous preference shifter.1 Parameter β ∈(0, 1) is the discount factor.
Et{·} is the expectational operator, conditional on information at time t.
The period utility function, U(Ct, Nt; Zt), is assumed to be continu-
ous and twice differentiable. Letting Ut ≡U(Ct, Nt; Zt), it is assumed
that Uc,t ≡∂Ut
∂Ct > 0, Ucc,t ≡∂2Ut
∂C2
t ≤0, Un,t ≡∂Ut
∂Nt ≤0, and Unn,t ≡∂2Ut
∂N2
t ≤0. In
words, the marginal utility of consumption Uc,t is assumed to be positive
and nonincreasing, while the marginal disutility of labor, −Un,t, is posi-
tive and nondecreasing. In addition, it is assumed that Ucz,t ≡
∂2Ut
∂Ct∂Zt > 0,
that is, an increase in Zt raises the marginal utility of consumption.
Maximization of (1) is subject to a sequence of ﬂow budget constraints
given by
PtCt + QtBt ≤Bt−1 + WtNt + Dt
(2)
for t = 0, 1, 2, . . . Pt is the price of the consumption good, Wt denotes the
nominal wage (per hour or per worker, depending on the interpretation
of Nt), and Bt represents the quantity of one-period nominally riskless
discount bonds purchased in period t, and maturing in period t + 1.
Each bond pays one unit of money at maturity, and its price is Qt. In
order to keep the notation simple, the set of tradable assets is restricted
to that one-period nominally riskless debt. Given the assumption of
a representative household, this has no consequences for equilibrium
outcomes, since no assets would be traded in equilibrium anyway. Dt
represents dividends, accruing to households in their condition of ﬁrms’
owners. When solving the problem above, the household is assumed to
1 Note that Nt can be interpreted as the number of household members who are
employed, assuming a “large” household and ignoring integer constraints. In much of what
follows I use the term “employment” interchangeably as “number of individuals employed”
or “number of work hours employed.”

19
take as given the price of goods and bonds, as well as the wage and
dividends.
In addition to (2), it is assumed that the household is subject to a
solvency constraint that prevents it from engaging in Ponzi-type schemes.
The following constraint is assumed
lim
T→∞Et

t,T
BT
PT

≥0
(3)
for all t, where t,T ≡βT−tUc,T/Uc,t is the stochastic discount factor.2
The optimality conditions implied by the maximization of (1) subject
to (2) are given by
−Un,t
Uc,t
= Wt
Pt
(4)
Qt = βEt
Uc,t+1
Uc,t
Pt
Pt+1

(5)
as well as the transversality condition
lim
T→∞Et

t,T
BT
PT

= 0
(6)
for t = 0, 1, 2, . . ..
The previous optimality conditions can be derived using a simple
variational argument. Consider ﬁrst the impact on utility of a small
departure, in period t, from the household’s optimal plan. That departure
consists of an increase in consumption dCt and an increase in employ-
ment dNt, while keeping the remaining variables unchanged (including
consumption and employment in other periods). If the household is
following an optimal plan to begin with, it should not be possible to
raise utility by departing from that plan, without violating the budget
constraint. Formally, it must be the case that
Uc,tdCt + Un,tdNt = 0
2 See Woodford (2003; chap. 2) for a derivation of (3) under the assumption of complete
markets, as the constraint that guarantees that debt can be repaid at any point in time by
selling claims to future income.

CHAPTER 2
for any pair (dCt, dNt) satisfying
PtdCt = WtdNt
for otherwise it would be possible to raise utility by increasing (or
decreasing) consumption and employment, thus contradicting the as-
sumption that the household is on an optimal plan. Note that the
optimality condition (4) is obtained by combining both equations.
Similarly, consider the impact on expected utility as of time t of
a reallocation of consumption between periods t and t + 1, while
keeping consumption in any other period and employment in all periods
unchanged. If the household is optimizing it must be the case that
Uc,tdCt + βEt{Uc,t+1dCt+1} = 0
for any pair (dCt, dCt+1) satisfying
Pt+1dCt+1 = −Pt
Qt
dCt
where the latter equation determines the increase in consumption expen-
ditures in period t + 1 made possible by the additional savings −PtdCt
allocated into one-period bonds. Combining the two previous equations
yields the intertemporal optimality condition (5).
Finally, transversality condition (6) is also a requirement of an optimal
plan: It can be shown that if (3) were to hold with strict inequality, it
would be feasible for the household to increase its current consumption
by a discrete amount without the need to reduce it in the future,
which would be inconsistent with optimality, as long as utility is strictly
increasing in consumption (as assumed here).3
In much of what follows, it is assumed that the period utility takes the
form
U(Ct, Nt; Zt) =






C1−σ
t
−1
1−σ
−N1+ϕ
t
1+ϕ

Zt
for σ ̸= 1

log Ct −N1+ϕ
t
1+ϕ

Zt
for σ = 1
where σ
≥0 and ϕ ≥0 determine, respectively, the curvature of
the utility of consumption and the disutility of labor. The analysis is
3 The assumptions of a representative household and a zero net supply of one-period
debt, guarantee that (6) is always satisﬁed in equilibrium, since Bt = 0 for all t. That
observation allows us to ignore that condition in much of what follows.

21
considerably simpliﬁed by two properties of the above utility function:
(i) separability, that is, Ucn,t = 0, and (ii) the implied constancy of the
elasticities for the marginal utility of consumption and for the marginal
disutility of labor, which leads to simple log-linearized approximations
to the equilibrium conditions, as shown below. Furthermore, the way
the preference shifter Zt enters the utility function implies that it may be
interpreted as a shock to the effective discount factor (which becomes
Ztβt, for t = 0, 1, 2, . . .), whose effect will be restricted to intertemporal
choices (through its inﬂuence on Uc,t+k/Uc,t, the intertemporal marginal
rate of substitution), but with no impact on intratemporal ones (since it
does not affect Un,t/Uc,t, the intratemporal marginal rate of substitution).
In addition, it is assumed that zt ≡log Zt follows an exogenous AR(1)
process
zt = ρzzt−1 + εz
t
where ρz ∈[0, 1].
The consumer’s optimality conditions (4) and (5) thus become
Wt
Pt
= Cσ
t Nϕ
t
(7)
Qt = βEt

Ct+1
Ct

−σ 
 Zt+1
Zt

 Pt
Pt+1

(8)
Note, for future reference, that equation (7) can be rewritten in log-
linear form as
wt −pt = σct + ϕnt
(9)
where lowercase letters denote the (natural) logs of the corresponding
variable (e.g., wt ≡log Wt). The previous condition can be interpreted as
a competitive labor supply schedule, determining the quantity of labor
supplied as a function of the real wage, given the marginal utility of
consumption (which is a function of consumption only, under the above
assumption on utility). Parameter ϕ is the inverse (Frisch) labor supply
elasticity. Note that the position of the labor supply schedule is invariant
to shocks to the preference shifter zt.
As shown in appendix 2.1, a log-linear approximation of (8) around
a steady state with constant rates of inﬂation and consumption growth
yields
ct = Et{ct+1} −1
σ (it −Et{πt+1} −ρ) + 1
σ (1 −ρz)zt
(10)

CHAPTER 2
where it ≡−log Qt, ρ ≡−log β and πt+1 ≡pt+1 −pt is the rate of
inﬂation between t and t + 1 (having deﬁned pt ≡log Pt ). Notice that it
corresponds to the log of the gross bond yield; henceforth, it is referred
to as the nominal interest rate.4 Analogously, ρ can be interpreted as the
household’s discount rate.5
While the above framework does not explicitly introduce money as an
asset that households may hold (nor provides a motive for holding it), in
some cases it will be convenient to postulate a demand for real balances
with a log-linear form given by (up to an additive constant)
mt −pt = ct −ηit
(11)
where η ≥0 denotes the interest semielasticity of money demand. A
money demand equation similar to (11) can be derived under a variety
of assumptions. For instance, in section 2.5 it is derived as an optimality
condition for the household when real money balances yield utility.
2.2 FIRMS
A large number of identical ﬁrms are assumed to operate in the economy,
producing a homogeneous consumption good. The representative ﬁrm’s
technology is described by the production function
Yt = AtN1−α
t
(12)
where At represents the level of technology, and at ≡log At evolves over
time according to an exogenous AR(1) process
at = ρaat−1 + εa
t
where ρa ∈[0, 1].
Each period the ﬁrm maximizes proﬁts
PtYt −WtNt
(13)
subject to (12), taking the price and wage as given.
4 The gross yield It on the one-period bond is given by It ≡1/Qt . The nominal interest
rate is deﬁned here as it ≡log It. Thus, it is a monotonic functions of the net yield It −1,
and approximately equal to the latter for values close to zero.
5 Note that ρ ≡−log β ≃β−1 −1, which is the usual deﬁnition of the discount rate.

23
Maximization of (13) subject to (12) yields the optimality condition
Wt
Pt
= (1 −α)AtN−α
t
(14)
that is, the ﬁrm hires labor up to the point where its marginal product
equals the real wage. Equivalently, the marginal cost
Wt
(1−α)At N−α
t
must be
equated to the price Pt.
In log-linear terms,
wt −pt = at −αnt + log(1 −α)
(15)
which can be interpreted as a labor demand schedule, mapping the real
wage into the quantity of labor demanded, given the level of technology.
2.3 EQUILIBRIUM
The baseline model abstracts from sources of goods demand other than
consumption (like investment, government purchases, or net exports).
Accordingly, the goods market clearing condition is given by
yt = ct
(16)
that is, all output must be consumed.
By combining the optimality conditions of households and ﬁrms with
(16) and the log-linear aggregate production relationship
yt = at + (1 −α)nt
(17)
one can determine the equilibrium levels of employment and output:
nt = ψnaat + ψn
(18)
yt = ψyaat + ψy
(19)
where ψna ≡
1−σ
σ(1−α)+ϕ+α, ψn ≡
log(1−α)
σ(1−α)+ϕ+α, ψya ≡
1+ϕ
σ(1−α)+ϕ+α, and ψy ≡
(1 −α)ψn.
Furthermore, given the equilibrium process for output, (10) can be
used to determine the implied real interest rate, rt ≡it −Et{πt+1}, as
rt = ρ + (1 −ρz)zt + σ Et{
yt+1}
= ρ + (1 −ρz)zt −σ(1 −ρa)ψyaat
(20)

CHAPTER 2
Finally, the equilibrium real wage, ωt ≡wt −pt, is given by
ωt = at −αnt + log(1 −α)
= ψωaat + ψω
(21)
where ψωa ≡
σ+ϕ
σ(1−α)+ϕ+α and ψω ≡(σ(1−α)+ϕ) log(1−α)
σ(1−α)+ϕ+α
.
Notice that the equilibrium levels of employment, output, and the real
interest rate are determined independently of monetary policy. In other
words, monetary policy is neutral with respect to those real variables.
In the simple model, output, employment, and the real wage ﬂuctuate
in response to variations in technology, though they are invariant to
preference shocks. In particular, output always rises in the face of a
productivity increase, with the size of the increase being given by ψya > 0.
The same is true for the real wage. On the other hand, the sign of the
employment is ambiguous, depending on whether σ (which measures
the strength of the income effect on labor supply) is larger or smaller
than one. When σ < 1, the substitution effect on labor supply resulting
from a higher real wage dominates the negative effect caused by a smaller
marginal utility of consumption, leading to an increase in employment.
The converse is true whenever σ > 1. When the utility of consumption
is logarithmic (σ = 1), employment remains unchanged in the face of
technology variations, for substitution and income effects exactly cancel
one another. Finally, and under the assumptions on the processes
followed by at and zt, the real interest rate goes down in response
to a positive technology shock, but rises in the wake of an increase
in zt.
What about nominal variables, like inﬂation or the nominal interest
rate? Not surprisingly, and in contrast with real variables, their equilib-
rium values cannot be determined independently of monetary policy. To
illustrate how nominal variables are inﬂuenced by the way monetary pol-
icy is conducted, their equilibrium behavior under alternative monetary
policy rules will be considered next.
2.4 MONETARY POLICY AND PRICE LEVEL DETERMINATION
Let us start by examining the implications of some interest rate
rules. Rules that involve monetary aggregates will be introduced later.
Throughout use is made of the Fisherian equation
it = Et{πt+1} + rt
(22)

25
which implies that the nominal rate adjusts one-for-one with expected
inﬂation, given a real interest rate that is determined exclusively by real
factors, as in (20).
Equation (20) implies that in the steady state without growth r = ρ,
that is, the real interest rate corresponds to the household’s discount rate.
Thus it follows from (22) that in the perfect foresight steady state the
nominal rate and inﬂation will be related by
i = ρ + π
In what follows the analysis is restricted to nonexplosive equilibrium
paths for inﬂation and the nominal interest rate, that is, equilibrium
paths that remain within a bounded neighborhood of the steady state,
for sufﬁciently small ﬂuctuations in the exogenous driving forces.
2.4.1 An Exogenous Path for the Nominal Interest Rate
Let us ﬁrst consider the case of a monetary policy that implies an
exogenous path for the nominal interest rate. For concreteness, let us
assume the rule
it = i + vt
where {vt} is assumed to follow an exogenous AR(1) process
vt = ρvvt−1 + εv
t
(23)
Henceforth, the stochastic component {vt} in the policy rule under
consideration is referred to as a monetary policy shock. It should be
interpreted as a random, transitory deviation from the “usual” conduct
of monetary policy as anticipated by the public, due to a change in the
policymaker’s preferences, a response to an unusual unanticipated event,
or, simply, an error in the implementation of monetary policy.6 Even if
one views those shocks as empirically unimportant, the analysis of their
effects helps uncover how monetary policy interventions are transmitted
to the economy under different sets of assumptions about the structure
of the latter.
A particular case of this rule corresponds to a constant interest rate,
that is, it = i for all t. Note that π = i −ρ is the steady state inﬂation (or
the implicit long-run inﬂation target) associated with the rule above.
6 Note that in the particular case of the rule (23) considered here, the “usual” policy
consists in keeping the interest rate constant at level i.

CHAPTER 2
Using (22), write
Et{πt+1} = it −rt
= π + vt −rt
where rt ≡rt−ρ is determined independently of the monetary policy rule,
as shown above.
Note that expected inﬂation is pinned down uniquely by the previous
equation, since it can be written as a function of exogenous variables,
using (20). But actual inﬂation is not. Because there is no other condition
that can be used to determine inﬂation, it follows that any inﬂation path
that satisﬁes
πt = π + vt−1 −rt−1 + ξt
is consistent with equilibrium, where ξt is a shock, possibly unrelated to
economic fundamentals, satisfying Et−1{ξt} = 0 for all t. Equivalently,
the price level is given by
pt = π + pt−1 + vt−1 −rt−1 + ξt
Shocks such as ξt are often referred to in the literature as sunspot
shocks. An equilibrium in which such nonfundamental factors may cause
ﬂuctuations in one or more variables is referred to as an indeterminate
equilibrium. The example above shows how an exogenous nominal
interest rate leads to price level indeterminacy.
Notice that the equilibrium nominal wage is equal, in logs, to the
real wage, which is determined by (21), plus the price level, which is
indeterminate. Thus, the nominal wage inherits the indeterminacy of the
price level.
2.4.2 A Simple Interest Rate Rule
Suppose that the central bank adjusts the nominal interest rate in
response to deviations of inﬂation from a target π, according to the
interest rate rule
it = ρ + π + φπ(πt −π) + vt
where φπ ≥0 is a coefﬁcient determining the strength of the endogenous
response of monetary policy and {vt} is an exogenous monetary policy
shifter, as deﬁned above.

27
Combining the previous rule with the Fisherian equation (22) yields
φπ πt = Et{πt+1} + rt −vt
(24)
where πt ≡πt−π. A distinction is made between two cases, depending on
whether the inﬂation coefﬁcient in the above rule, φπ, is larger or smaller
than one.
If φπ > 1, the previous difference equation has only one nonexplosive
solution. That solution can be obtained by solving (24) forward, which
yields
πt =
∞

k=0
φ−(k+1)
π
Et{rt+k −vt+k}
(25)
The previous equation fully determines inﬂation (and, hence, the price
level) as a function of the path of the real interest rate, which in turn is a
function of exogenous real forces, as shown in (20). In particular, under
the assumed driving processes for technology and preference parameters,
inﬂation can be written as
πt = π −σ(1 −ρa)ψya
φπ −ρa
at + 1 −ρz
φπ −ρz
zt −
1
φπ −ρv
vt
Note that a central bank following a rule of the form considered
here can inﬂuence the degree of inﬂation volatility through its choice
of φπ. The larger that coefﬁcient is the smaller will be the impact of
real shocks on inﬂation. Monetary policy shocks, vt, are seen to generate
“unnecessary” ﬂuctuations in inﬂation.
Given equilibrium path for inﬂation, the price and nominal wage levels
are uniquely determined by the identities pt = pt−1+πt and wt = ωt + pt,
with the real wage ωt given by (21).
Note that an exogenous tightening of monetary policy (i.e., a positive
realization of vt) reduces inﬂation and, if persistent (i.e., ρv > 0), the
nominal interest rate as well, since
∂it
∂εv
t = −
ρv
φπ−ρv . Assuming a money
demand function of the form (11) the (contemporaneous) response of
the money supply to the same shock is given by ∂mt
∂εv
t = ηρv−1
φπ−ρv , which can
be positive or negative, depending on the values of η and ρv. Thus, under
the assumed interest rate rule, a liquidity effect will be present in response
to a monetary policy shock if and only if ηρv > 1, for in that case the
nominal rate will decline and the money supply will increase in response
to the shock. Yet, and in contrast with the evidence shown in chapter 1,
the previous responses will be accompanied by a decrease in prices (given
∂πt
∂εv
t = −
1
φπ−ρv ), and no effect on output or any other real variable.

CHAPTER 2
On the other hand, if φπ < 1, the forward solution (25) does not
converge. Instead, the stationary solution to (24) takes the form
πt = (1 −φπ)π + φππt−1 −rt−1 + vt−1 + ξt
(26)
where {ξt} is, again, an arbitrary sequence of shocks, related or unrelated
to fundamentals, satisfying Et−1{ξt} = 0 for all t.
Accordingly, any process {πt} satisfying (26) is consistent with equi-
librium, while remaining in a neighborhood of the steady state (for
sufﬁciently small shocks). So, as in the case of an exogenous nominal
rate, the price level (and, hence, inﬂation) are not determined uniquely
when the interest rate rule implies a weak response of the nominal rate
to deviations of inﬂation from target.7
More speciﬁcally, the condition for a determinate price level, φπ > 1,
requires that the central bank adjusts nominal interest rates more than
one-for-one in response to any change in inﬂation, a property known as
the Taylor principle. The previous result can be viewed as a particular
instance of the need to satisfy the Taylor principle in order for an interest
rate rule to bring about a determinate equilibrium.
2.4.3 An Exogenous Path for the Money Supply
The analysis above assumed that monetary policy can be described
by an interest rate rule. In that case, money supply does not play an
independent role in determining the equilibrium. Instead, it just adjusts
endogenously, in order to match money demand, given the path of
output, the price level, and the interest rate, as implied by an equation of
the form
mt = pt + yt −ηit
which corresponds to (11), after imposing the goods market clearing
condition.
Suppose instead that the central bank sets an exogenous path for the
money supply {mt}. Using (11) (with ct = yt) to eliminate the nominal
7 With no loss of generality one can write
ξt = τaεa
t + τzεz
t + τvεv
t + ξ∗
t
where τa, τz, and τv can take any value (i.e., are indeterminate) and ξ∗
t is a “pure sunspot,”
i.e., a martingale-difference process orthogonal to all fundamental shocks. Thus, the
response of inﬂation (and, as result, of any nominal variable) to any shock is indeterminate.

29
interest rate in (22), the following difference equation for the price level
can be derived
pt =

η
1 + η

Et{pt+1} +

1 + η

mt + ut
(27)
where ut ≡(1 + η)−1(ηrt −yt) evolves independently of {mt}, as shown in
(19) and (20).
Assuming η > 0 and solving forward obtains
pt =
1
1 + η
∞

k=0

η
1 + η

k
Et {mt+k} + ut
(28)
where ut ≡∞
k=0

η
1+η
	k
Et {ut+k} is, again, independent of monetary
policy.
Thus, when the monetary policy rule takes the form of an exogenous
path for the money supply, the equilibrium price level is always deter-
mined uniquely, as shown in (28).
It is often convenient to have an expression for the equilibrium price
level in terms of the expected future growth rate of money:8
pt = mt +
∞

k=1

η
1 + η

k
Et {
mt+k} + ut
(29)
Given (29), as determined above, money demand equation (11) can be
used to solve for the nominal interest rate
it = 1
η (yt −(mt −pt))
= 1
η
∞

k=1

η
1 + η

k
Et {
mt+k} + ut
where ut ≡η−1(ut + yt) is independent of monetary policy.
8 To derive (29), rewrite (27) as a difference equation in terms of pt ≡pt −mt, i.e.,
pt =

η
1 + η

Et{pt+1} +

η
1 + η

Et{
mt+1} + ut
which can be solved forward to yield (29).

CHAPTER 2
For concreteness, consider the case in which money growth follows an
AR(1) process

mt = ρm
mt−1 + εm
t
For simplicity, assume the absence of real shocks, thus implying a
constant output and a constant real rate. Without loss of generality, set
rt = yt = 0 for all t. Then, it follows from (29) that
pt = mt +
ηρm
1 + η(1 −ρm)
mt
Hence, in response to an exogenous monetary policy shock, and as
long as ρm > 0 (the empirically relevant case, given the observed positive
autocorrelation of money growth), the price level should respond more
than one-for-one with the increase in the money supply, a prediction that
contrasts starkly with the sluggish response of the price level observed in
empirical estimates of the effects of monetary policy shocks as discussed
in chapter 1.
The nominal interest rate is in turn given by
it =
ρm
1 + η(1 −ρm)
mt
that is, in response to an expansion of the money supply, and as long as
ρm > 0, the nominal interest rate is predicted to go up. In other words,
the model implies the absence of a liquidity effect, in contrast with the
evidence discussed in chapter 1.
2.4.4 Optimal Monetary Policy
The analysis of the baseline classical economy above has shown that
while real variables are independent of monetary policy, the latter can
have important implications for the behavior of nominal variables and,
in particular, of prices. Yet, and given that households’ utility is a
function of consumption and employment only—two real variables that
are invariant to the way monetary policy is conducted—it follows that
no policy rule is better than any other. Thus, in the classical model
above, a policy that generates large ﬂuctuations in inﬂation and other
nominal variables (perhaps as a consequence of following a policy rule
that does not guarantee a unique equilibrium for those variables) is
no less desirable from a welfare perspective than one that succeeds in
stabilizing prices in the face of the same shocks.
The previous result, which is clearly extreme and empirically unap-
pealing, can be overcome once versions of the classical monetary model

31
are considered in which a motive to keep part of households’ wealth in
the form of monetary assets is introduced explicitly. Section 2.5 discusses
one such model in which real balances are assumed to yield utility.
The overall assessment of the classical monetary model as a framework
to understand the observed behavior of nominal and real variables and
their connection to monetary policy cannot be a favorable one. The
model cannot explain the observed real effects of monetary policy on
real variables. Its predictions regarding the response of the price level,
the nominal rate, and the money supply to exogenous monetary policy
shocks are also in conﬂict with the empirical evidence. Those empirical
failures are the main motivation behind the introduction of nominal
frictions in the model, a task that will be undertaken in chapter 3.
2.5 MONEY IN THE UTILITY FUNCTION
In the model developed in the previous sections, and in much of the
recent monetary literature, the only role played by money is to serve
as a numéraire, that is, a unit of account in which prices, wages, and
securities payoffs are stated. Economies with that characteristic are often
referred to as cashless economies. Above, a simple log-linear money
demand function was occasionally postulated, but it was done in an
ad hoc manner and without an explicit justiﬁcation for why agents
would want to hold an asset that is dominated in return by bonds
while having identical risk properties. Even though in the analysis of
subsequent chapters the assumption of a cashless economy is maintained,
it is useful to understand how the basic framework can incorporate a
role for money other than that of a unit of account and, in particular,
how it can generate a demand for money. The discussion in this section
focuses on models that achieve the previous objective by assuming that
real money holdings are an argument of the utility function.9 The reader
can ﬁnd references to alternative “microfoundations” in the section on
the literature at the end of the chapter.
The assumption that real money holdings (or real balances), Mt/Pt,
enter the utility function is a convenient way of formalizing the notion
that, in contrast with other assets, money provides a “transactions
service” that households value. The service that any nominal amount
of money can yield is likely to depend on its purchasing power, thus
explaining why it is the real value of monetary holdings that enters the
utility function.
9 Readers not interested in this extension may skip this section and proceed to section
2.6 without any loss of continuity.

CHAPTER 2
The introduction of money in the utility function requires modifying
the representative household’s problem in two ways. First, preferences
are now given by
E0
∞

t=0
βtU

Ct, Mt
Pt
, Nt; Zt

(30)
where Mt denotes holdings of money in period t. It is assumed that period
utility is increasing and concave in real balances Mt/Pt. Second, the ﬂow
budget constraint incorporates monetary holdings explicitly, taking the
form
PtCt + QtBt + Mt ≤Bt−1 + Mt−1 + WtNt + Dt
(31)
Letting At ≡Bt + Mt denote total ﬁnancial wealth at the beginning
of period t (i.e., after bonds mature, but before consumption and
portfolio decisions are made), the previous ﬂow budget constraint can be
rewritten as
PtCt + QtAt + (1 −Qt)Mt ≤At−1 + WtNt + Dt
(32)
with the solvency constraint now taking the form
lim
T→∞Et

t,T
AT
PT

≥0
for all t.
The previous representation of the budget constraint can be thought
of as equivalent to that of an economy in which all ﬁnancial assets
(represented by At) yield a gross nominal return Q−1
t
( = exp{it}), and
where agents can “purchase” the utility-yielding services of money
balances at a unit price 1−Qt = 1−exp{−it} ≃it. Thus, the implicit price
for the services of money roughly corresponds to the nominal interest
rate, that is, the opportunity cost of holding ﬁnancial wealth in terms of
monetary assets, instead of interest-bearing bonds.
Consider next the household’s problem, which consists of maximizing
(30) subject to (32). Two of the implied optimality conditions are the
same as those obtained for the cashless model, namely, (4) and (5),
with the marginal utility terms being now deﬁned over (and evaluated
at) (Ct, Mt
Pt , Nt; Zt). In addition to (4) and (5), there is an additional
optimality condition given by
Um,t
Uc,t
= 1 −Qt
= 1 −exp{−it}
(33)
where Um,t ≡
∂Ut
∂(Mt/Pt) > 0.

33
Again, in order to derive that optimality condition a simple variational
argument can be used. Suppose that a household following an optimal
plan considers a deviation from the latter which consists in adjusting
consumption and money holdings in period t by amounts dCt and dMt,
respectively, while keeping all other variables unchanged at their optimal
values. Optimality of the initial plan requires that utility cannot rise as a
result of the deviation, which in turn requires
Uc,tdCt + Um,t
1
Pt
dMt = 0
for any pair (dCt, dMt) satisfying
PtdCt + (1 −Qt)dMt = 0
which guarantees that the budget constraint is met without the need to
adjust any other variables. Combining the previous two equations and
using the deﬁnition of the nominal rate it ≡−log Qt yields the optimality
condition (33).
In order to be able to make any statements about the consequences
of having money in the utility function, more speciﬁc assumptions are
needed about the way money balances interact with other variables in
yielding utility. In particular, whether the utility function is separable
or not in real balances determines the extent to which the neutrality
properties derived above for the cashless economy carry over to the
economy with money in the utility function. That point is illustrated
by considering, in turn, two example economies with separable and
nonseparable utility.
2.5.1 An Example with Separable Utility
Speciﬁcally, the household’s utility function is assumed to have the
functional form
U

Ct, Mt
Pt
, Nt; Zt

=

C1−σ
t
−1
1 −σ
+ (Mt/Pt)1−ν −1
1 −ν
−N1+ϕ
t
1 + ϕ

Zt
Note that, given the assumed separability, neither Uc,t nor Un,t depend
on the level of real balances. As a result, (7) and (8), as well as their log-
linear counterparts, (9) and (10), continue to hold unchanged. It follows
that the equilibrium values for output, employment, the real rate, and
the real wage can be determined by following the same steps as in the
previous section, without any reference to monetary policy.

CHAPTER 2
The introduction of money in the utility function allows a money
demand equation to be derived from the household’s optimal behavior.
Using the above speciﬁcation of utility, the optimality condition (33) can
be rewritten as
Mt
Pt
= Cσ/ν
t
(1 −exp{−it})−1/ν
(34)
which can be naturally interpreted as a demand for real balances. The
latter is increasing in consumption and inversely related to the nominal
interest rate, as in conventional speciﬁcations.
Using the ﬁrst-order Taylor expansion log(1 −exp{−it}) ≃const. +
1
exp{i}−1 it, (34) can be rewritten in approximate log-linear form (up to an
uninteresting constant) as
mt −pt = σ
ν ct −ηit
(35)
where η ≡
1
ν(exp{i}−1) ≃
1
νi is the implied interest semielasticity of money
demand.
The particular case of ν = σ is an appealing one in the present context,
because it implies a unit elasticity with respect to consumption. Under
that assumption, a conventional log-linear demand for real balances is
obtained as
mt −pt = ct −ηit
= yt −ηit
(36)
where the second equality holds under the assumption (made here) that
all output is consumed. The previous speciﬁcation is often maintained in
subsequent chapters, without the need to invoke its source explicitly.
As in the analysis of the cashless economy, the usefulness of (35),
or (36), is conﬁned to the determination of the equilibrium values
for inﬂation and other nominal variables whenever the description
of monetary policy involves the quantity of money in circulation.
Otherwise, the only use of the money demand equation is to determine
the quantity of money that the central bank will need to supply in order
to support, in equilibrium, the nominal interest rate implied by the policy
rule.
2.5.2 An Example with Nonseparable Utility
Let us consider an economy with period utility given by
U(Xt, Nt) = X1−σ
t
−1
1 −σ
−N1+ϕ
t
1 + ϕ

35
where Xt is a composite index of consumption and real balances
deﬁned by
Xt ≡

(1 −ϑ)C1−ν
t
+ ϑ

 Mt
Pt

1−ν
1
1−v
f or ν ̸= 1
≡C1−ϑ
t

 Mt
Pt

ϑ
f or ν = 1
with ν representing the (inverse) elasticity of substitution between con-
sumption and real balances, and ϑ the relative weight of real balances
in utility. Note that, in order to ease the algebra, preference shocks are
ignored for the remainder of this section.
Notice that the marginal utilities of consumption and real balances are
now given, respectively, by
Uc,t = (1 −ϑ)Xν−σ
t
C−ν
t
Um,t = ϑ Xν−σ
t

 Mt
Pt

−ν
whereas the marginal (dis)utility of labor is, as before, given by Un,t =
−Nϕ
t . The optimality conditions of the household’s problem, (4), (5), and
(33), can now be written as
Wt
Pt
= Nϕ
t Xσ−ν
t
Cν
t (1 −ϑ)−1
(37)
Qt = βEt

Ct+1
Ct

−ν 
 Xt+1
Xt

ν−σ 
 Pt
Pt+1

(38)
Mt
Pt
= Ct (1 −exp{−it})−1
ν

ϑ
1 −ϑ

ν
(39)
Notice that in the particular case in which the intertemporal and
intratemporal elasticities of substitution coincide (i.e., ν = σ), optimality
conditions (37) and (38) match exactly those obtained in the case of
separable utility, and thus lead to the same equilibrium implications
derived for that case and discussed in section 2.5.1.
In the general case, however, both the labor supply equation (37) and
the Euler equation (38) depend on the level of real balances through

CHAPTER 2
variable Xt. The level of real balances depends, in turn, on the nominal
interest rate, as implied by (39).10 Those features imply that monetary
policy is no longer neutral in the case of nonseparable utility considered
here. In particular, to the extent that different monetary policy rules have
different implications for the path of the nominal rate (as will generally
be the case), they will also have different effects on real balances and—
through the latter’s inﬂuence on the marginal utility of consumption—on
the position of the labor supply schedule and, hence, on employment and
output. This mechanism is analyzed formally below.
Notice that the implied money demand equation (39) can be rewritten
in log-linear form (and up to an additive constant) as in (36) above
mt −pt = ct −ηit
(40)
where, as above, η ≡
1
ν(exp{i}−1). Thus, the implied interest semielasticity
of money demand η is now proportional to the elasticity of substitution
between real balances and consumption ν−1.
On the other hand, (37) can be written in log-linear form as (up to an
additive constant):
wt −pt = σct + ϕnt + (ν −σ)(ct −xt)
For the remainder of this section the analysis is restricted to a
neighborhood of the zero inﬂation steady state.11 Log-linearizing the
deﬁnition of Xt around that steady state and combining the resulting
expression with (39), yields
wt −pt = σct + ϕnt + χ(ν −σ) (ct −(mt −pt))
= σct + ϕnt + ηχ(ν −σ)it
where χ ≡
ϑ
1ν (1−β)1−1ν
(1−ϑ)
1ν +ϑ
1ν (1−β)1−1ν
∈[0, 1), and where the second equality
makes use of (40).
For future reference, it is convenient to rewrite the previous optimality
conditions in terms of the steady state ratio km ≡M/P
C , that is, the inverse
consumption velocity. Using the money demand equation, evaluated at
the zero inﬂation steady state, we have km =

ϑ
(1−β)(1−ϑ)
	 1
ν . Noting that
10 Note that the present utility speciﬁcation guarantees a unit-elastic money demand with
respect to consumption, independently of the values of ν and σ.
11 This is largely for notational simplicity. It is straightforward to extend the analysis to
a neighborhood of a nonzero inﬂation steady state.

37
χ =
km(1−β)
1+km(1−β), and using the deﬁnition of η evaluated at the zero inﬂation
steady state, the optimality condition above can be rewritten as
wt −pt = σct + ϕnt + ϖit
(41)
where ϖ ≡
kmβ(1−σ
ν )
1+km(1−β). Thus, the sign of the effect of the nominal interest
rate on labor supply is determined by the sign of ν −σ. When ν > σ
(implying ϖ > 0), the reduction in real balances induced by an increase
in the nominal rate brings down the marginal utility of consumption (for
any given ct), lowering the quantity of labor supplied at any given real
wage. The opposite effect is obtained when ν < σ. Note, however, that
ν ≃
1
iη is likely to be larger than σ for any plausible values of i, η, and
σ. Thus, the case of Ucm > 0 (and, hence, ϖ > 0) appears as the most
plausible one, conditional on the speciﬁcation of preferences analyzed
here.
In order to reﬂect the changes implied by nonseparable utility, the
economy’s log-linearized equilibrium conditions need to be modiﬁed.
Thus, combining (41) with the labor demand schedule (15) yields the
labor market clearing condition
σct + ϕnt + ϖit = at −αnt + log(1 −α)
(42)
which can be rewritten, using the goods market clearing condition
(16), the log-linear production relationship (17), and up to an additive
constant, as:
yt = ψyaat + ψyiit
(43)
where ψyi ≡−
ϖ(1−α)
σ(1−α)+ϕ+α and, as before, ψya ≡
1+ϕ
σ(1−α)+ϕ+α.
Condition (43) points to a key implication of the nonseparability
property (i.e., ϖ ̸= 0): Equilibrium output is no longer invariant to
monetary policy, at least to the extent that the latter implies variations in
the nominal interest rate. In other words, monetary policy is not neutral.
As a result, equilibrium condition (43) does not sufﬁce to determine the
equilibrium level of output, in contrast to the economy with separable
utility analyzed above. Note that in the empirically plausible case of
ϖ > 0, ψyi < 0 implying that output is inversely related to the nominal
interest rate.
In order to assess the extent to which monetary policy may affect the
level of output it is useful to get a sense of the magnitude of the interest
rate multiplier ψyi. With that purpose, and in a way consistent with the
baseline calibration that will be introduced in chapter 3, the settings

CHAPTER 2
σ = 1, ϕ = 5, and α = 1/4 are chosen and taken to be “empirically
plausible.” Using the deﬁnition of ϖ, and the fact that ν = 1
ηi is “large”
for any reasonable values of η, it follows that ψyi ≃−km
8 , and so the
size of the inverse velocity km is a key determinant of the quantitative
importance of monetary non-neutralities in the model. The magnitude
of km, however, depends crucially on the deﬁnition of money one adopts.
Thus, and focusing on postwar U.S. data, km ≃0.3 if the monetary base is
taken to be the relevant measure of money.12 In that case ψyi ≃−0.04,
which implies a very small multiplier: A monetary policy intervention
that raised the nominal rate by one percentage point (expressed at an
annual rate) would generate a decrease in quarterly output of about 0.01
percent. Using M2 instead as the deﬁnition of money, km ≃3, and
hence ψyi ≃−0.4. Thus, an analogous monetary policy intervention
would lower output by 0.1 percent. The latter value, while still very
small, appears to be more in line with the estimated output effects of
monetary policy shock found in the literature, at least in terms of order
of magnitude. Yet, even in the latter case, there are other aspects of the
monetary transmission mechanism associated with the model above that
are clearly at odds with the evidence. The analysis below makes this point
by analyzing the joint response of output, inﬂation, and the interest rate
to a monetary policy shock.
Combining (40) and (43) (after setting at = 0 for all t, given the focus
on exogenous shifts to monetary policy), one obtains
yt = (mt −pt)
(44)
where  ≡
ϖ(1−α)
η[σ(1−α)+ϕ+α]+ϖ(1−α) ∈[0, 1) under the empirically plausible
assumption that ϖ ≥0 (which is maintained for the remainder of the
section). Also,
it = −(1/η)(1 −)(mt −pt)
(45)
Thus, in order for an exogenous tightening of monetary policy to
raise the nominal rate, while lowering output and the money supply (as
suggested by the evidence in chapter 1), it must also be associated with
a decline in real balances, that is, the price level should not decline more
than proportionally to the money supply. But the latter requirement is
inconsistent with the predictions of the model, as shown next, at least to
the extent that the policy tightening is associated with a persistent decline
in money supply growth, as found in the data.
12 This is the approach followed in Woodford (2003, chap. 2).

39
First, note that the corresponding log-linear approximation to (38) is
given by
ct = Et{ct+1}−1
σ (it −Et{πt+1}−(ν −σ)Et{(ct+1 −xt+1)−(ct −xt)}−ρ)
= Et{ct+1}−1
σ (it −Et{πt+1}−χ(ν −σ)Et{
ct+1 −
(mt+1 −pt+1)}−ρ)
= Et{ct+1} −1
σ (it −Et{πt+1} −ϖ Et{
it+1} −ρ)
(46)
where, again, the last equality makes use of (40). Thus, when ν > σ (and,
hence, ϖ > 0) the anticipation of a nominal rate increase (and, hence,
of a decline in real balances) lowers the expected one period ahead level
of the marginal utility of consumption (for any expected ct+1), which
induces an increase in current consumption (in order to smooth marginal
utility over time). Imposing the goods market clearing condition yt = ct
on (46), yields an equation relating output, to the nominal interest rate
and expected inﬂation:
yt = Et{yt+1} −1
σ (it −Et{πt+1} −ϖ Et{
it+1} −ρ)
(47)
Combining the previous equation with (44) and (45) one can obtain
(after some algebraic manipulation) an expression relating the price level
to current and expected money supply which generalizes (29) to the case
of nonseparable utility:
pt = mt +
η
η + ϖ
∞

k=1

η + ϖ
1 − + η + ϖ

k
Et{
mt+k}
(48)
where  ≡
η(α+ϕ)
η[σ(1−α)+ϕ+α]+ϖ(1−α) ∈[0, 1). Thus, in order for the price
level to decline less than the money supply in response to a tightening
of monetary policy involving a higher nominal rate and lower output,
the initial decline in the money supply would have to be followed by
persistently higher than average money growth. The latter implication is
at odds with the empirical evidence, as shown in chapter 1. Note that
the above implication is independent of the details of monetary policy
implementation (i.e., of the speciﬁc monetary policy rule).
The model also predicts that the real wage should move countercycli-
cally in response to an exogenous shift in monetary policy, to the extent
that the latter has an effect on output (i.e., if ϖ ̸= 0). The reason is
that the resulting change in employment is a consequence of a shift in

CHAPTER 2
the labor supply schedule, moving along a stable labor demand. That
prediction is also in conﬂict with the empirical evidence in Christiano,
Eichenbaum, and Evans (2005), which points to a mildly procyclical real
wage in response to an exogenous monetary policy shock.
The analysis above has revealed important weaknesses regarding the
empirical plausibility of the classical model’s monetary transmission
mechanism. A key concern has to do with the large and rapid price
adjustment that follows a monetary shock, with the price level changing
in the short run more than proportionally to the change in the money
supply. The previous assessment motivates the introduction of nominal
frictions in the models analyzed from the next chapter onward.
2.5.3 Optimal Monetary Policy in a Classical Economy with Money in
the Utility Function
This section derives the form of the optimal monetary policy in the
presence of money in the utility function. The problem of a hypothetical
social planner seeking to maximize the utility of the representative
household is presented and solved.
Note that, under the assumptions made above, the economy has no
aggregate intertemporal links: Even though each individual household
can reallocate its own consumption over time through ﬁnancial markets,
there are no mechanisms that make this possible for the economy as
a whole. Thus, a benevolent social planner solves a sequence of static
problems of the form
max U

Ct, Mt
Pt
, Nt; Zt

subject to the aggregate resource constraint
Ct = AtN1−α
t
The optimality conditions for that problem are given by
−Un,t
Uc,t
= (1 −α)AtN−α
t
(49)
Um,t = 0
(50)
Condition (49) requires that the marginal rate of substitution between
employment and consumption be equated to the marginal product of

41
labor. Condition (50) equates the marginal utility of real balances to the
“social” marginal cost of producing real balances, which is implicitly
assumed to be zero in the model.
Under what conditions does the equilibrium of the decentralized
economy satisfy efﬁciency conditions (49) and (50)? First note that
condition (49) is implied by the combined effect of proﬁt maximization
by ﬁrms (see equation (14), which equates the real wage to the marginal
product of labor) and the optimal labor supply choice by the household
(see equation (4), which equates the real wage to the marginal rate of
substitution between hours of work and consumption). Hence, (49) will
be satisﬁed independently of monetary policy. On the other hand, and as
shown in equation (33) above, the household’s optimal choice of money
balances requires
Um,t
Uc,t
= 1 −exp{−it}
Accordingly, efﬁciency condition (50) will be satisﬁed if and only if,
it = 0 for all t. This is the policy prescription known as the Friedman
rule. The rationale for that policy is quite intuitive: While the social cost
of producing real balances is zero, the private (opportunity) cost is given
by the nominal interest rate. As a result, only when the nominal interest
rate is zero are the private and social costs of holding money equated.
Note that such a policy implies an average (steady state) rate of inﬂation
π = −ρ < 0
that is, prices will decline on average at the rate of time preference.
In other words, under the Friedman rule the economy experiences
(moderate) steady state deﬂation, on average.
Implementation of the Friedman rule requires some discussion. First,
as was the case in the cashless model, a policy rule of the form it = 0
for all t leaves the price level indeterminate in the classical model with
money in the utility function. To see this note that, under that rule, (43)
and (47) imply that any inﬂation path that satisﬁes
πt+1 = −ρ −σψya Et{
at+1} + ξt+1
for an arbitrary martingale-difference sequence {ξt} is an equilibrium
path.13
13 That ﬁnding can be seen as a particular case of a more general result: Under a simple
interest rate rule of the form it = ρ + π + φπ(πt −π), with φπ ≥0, the condition for a
locally unique equilibrium is given by φπ > 1 (see exercise 6 below). Note that the rule
analyzed in the text corresponds to the particular case π = −ρ and φπ = 0.

CHAPTER 2
Even though that indeterminacy should not have any welfare con-
sequences (because consumption, employment, and real balances are
pinned down uniquely as a function of technology and the nominal
interest rate), a central bank could avoid nominal indeterminacy by
following a rule of the form
it = φ(rt−1 + πt)
for any φ > 1. Combined with (22), that rule implies the difference
equation
Et{it+1} = φit
whose only stationary solution is it = 0 for all t. Under that rule,
equilibrium inﬂation is fully predictable and given by
πt = −rt−1
More generally, any rule that makes the central bank adjust its policy
settings (e.g., the money supply) to guarantee that current inﬂation moves
one-for-one, but inversely, with the lagged real interest rate, will imply a
zero nominal interest rate and, thus, an optimal level of real balances.
2.6 NOTES ON THE LITERATURE
The modeling approach favored in much of the recent monetary litera-
ture, and the one adopted in this book (with the exception of section 2.5
of this chapter), does not incorporate money explicitly in the analysis.
Under that approach the main role played by money is that of a unit
of account. Such model economies can be viewed as a limiting case (the
so-called cashless limit) of an economy in which money is valued and
held by households, but in which the transaction services provided by
real balances are arbitrarily small relative to the size of the economy.
Woodford (2003) provides a detailed discussion and a forceful defense
of that approach.
Most models in the literature that introduce monetary assets explicitly
rely on one of two alternative formalisms in order to generate a demand
for an asset that—as is the case with money—is dominated in its rate
of return by alternative assets that have identical risk characteristics:
they assume that real balances either (i) generate (indirect) utility to
households or (ii) provide some “transaction services” which render

43
them necessary—or, at least, useful—when purchasing goods.14 The ﬁrst
approach can often be viewed as a reduced form of the second (exercises
7 and 9 below illustrate this point).
The ﬁrst of those approaches—money in the utility function—traces
back to Sidrauski (1967), who introduced that assumption in an other-
wise standard neoclassical growth model (with inelastic labor supply).
Woodford (2003) offers a detailed analysis of the implications of
alternative assumptions on the speciﬁcation of utility and, in particular,
of the likely degree of monetary non-neutralities arising from the nonsep-
arability of real balances. Walsh (2010, chap. 2) develops a model with
money in the utility function, and analyzes the equilibrium properties
of a calibrated version of that model. Both analyses conclude, in a way
consistent with the discussion above, that even under a utility that is
nonseparable in real balances, the real effects of monetary policy are
quantitatively very small for plausible calibrations of the models.
A common approach to the modeling of a transaction’s motive for
holding money builds on the assumption, originally due to Clower
(1967), that cash must be held in advance in order to purchase certain
goods. Early examples of classical monetary models in which a demand
for money is generated by postulating a cash-in-advance constraint can
be found in the work of Lucas (1982) and Svensson (1985). Cooley and
Hansen (1989) analyze an otherwise standard RBC model augmented
with a cash-in-advance constraint for consumption goods, showing that
monetary policy is nearly neutral for plausible calibrations of that
model. Walsh (2010, chap. 3) provides a detailed description of classical
monetary models with cash-in-advance constraints and their implications
for the role of monetary policy. Exercises 8 and 9 below ask the reader
to analyze economies with cash-in-advance constraints.
An alternative way of modeling the transaction services of money
consists in assuming that the time required to purchase goods (which
detracts from leisure and/or work time) is inversely related to the level
of real balances. See Walsh (2010, chap. 3) for a detailed analysis of a
“shopping time” model.
The practice, followed in this monograph, of appending a money
demand equation to a set of equilibrium conditions that have been
derived in the context of cashless economy is often found in the
literature. King and Watson (1995) constitutes an early example of that
practice.
14 A third approach, seldom found in the recent literature, emphasizes the function of
money as a store of value, i.e., as a way of transferring resources intertemporally. In the
absence of other services or dividends associated with money, the latter can be viewed as a
pure bubble under this approach. See, e.g., Samuelson (1958).

CHAPTER 2
The analysis of the form of the optimal monetary policy in a classical
economy goes back to Friedman (1969), where a case is made for a policy
that keeps the nominal interest rate constant at a zero level. More recent
treatments of the conditions under which that rule is optimal include
Woodford (1990) and Correia and Teles (1999).
In the present chapter, as well as in the rest of the book, the analysis
is restricted to local equilibrium dynamics, that is, to equilibrium paths
that remain within a neighborhood of the steady state. Accordingly,
the notion of uniqueness or indeterminacy used throughout the book
must be understood as referring to those bounded equilibria only. A
discussion of the conditions under which a classical monetary economy
may display global multiplicity of equilibria, coexisting with a locally
unique equilibrium, can be found in Benhabib, Schmitt-Grohé, and Uribe
(2001) and Woodford (2003, chap. 2), among others. The previous
authors also discuss alternative policies that guarantee that locally
unique equilibria around the desired steady state are also globally
unique.
Finally, the reader can ﬁnd two useful discussions of the notion of
monetary neutrality and its evolution in macroeconomic thinking in
Patinkin (1987) and Lucas (1996).
APPENDIX
2.1 LOG-LINEAR APPROXIMATION OF THE EULER EQUATION
The consumer’s Euler equation can be rewritten as
1 = Et{exp(it −σ
ct+1 −πt+1 −ρ + 
xt+1)}
(51)
In a perfect foresight steady state with constant inﬂation π and
constant growth γ
i = ρ + π + σγ
A ﬁrst-order Taylor expansion of exp(it −σ
ct+1 −πt+1 −ρ + 
xt+1)
around that steady state yields
exp(it −σ
ct+1 −πt+1 −ρ + 
xt+1)
≃1 + (it −i) −σ(
ct+1 −γ ) −(πt+1 −π) + 
xt+1
= 1 + it −σ
ct+1 −πt+1 −ρ + 
xt+1
which can be used in (51) to obtain, after some rearrangement of terms,
the log-linearized Euler equation
ct = Et{ct+1} −1
σ (it −Et{πt+1} −ρ −(1 −ρx)xt)

45
EXERCISES
2.1. Optimality conditions under nonseparable leisure
Derive the log-linearized optimality conditions of the household
problem under the following speciﬁcation of the period utility
function:
U(Ct, Nt) = [Ct(1 −Nt)ν]1−σ −1
1 −σ
2.2. Alternative interest rules for the classical economy
Consider the classical economy described in the text, with equi-
librium conditions
yt = Et{yt+1} −1
σ (it −Et{πt+1} −ρ)
and
rt ≡it −Et{πt+1}
= ρ + σ Et{
yt+1}
where yt and, hence, rt, are determined independently of mone-
tary policy. Analyze the implications of the following alternative
monetary policy rules. When relevant, assume that the money
demand function takes the form
mt −pt = yt −ηit + εm
t
where εm
t is a stochastic money demand disturbance.
a. Rule #1: Strict inﬂation targeting.
i. Derive an interest rate rule that guarantees full stabilization
of inﬂation, i.e., πt = π∗for all t where π∗is an inﬂation
target.
ii. Determine the behavior of money growth implied by that
rule.
iii. Explain why a policy characterized by a constant rate
of money growth 
mt = π∗will generally not succeed in
stabilizing inﬂation in that economy.
b. Rule #2: Price level targeting
i. Consider the interest rate rule
it = ρ + π∗+ φp(pt −p∗
t )

47
where φp > 0 and p∗
t = p∗
0 + π∗t is a time-varying target
for the (log) price level consistent with an average inﬂation
π∗. Determine the equilibrium behavior of the price level
under this rule. (Hint: you may ﬁnd it useful to introduce
a new variable pt ≡pt −p∗, the deviation of the price level
from target, to ease some of the algebraic manipulations.)
ii. Consider instead the money supply rule

mt = π∗
Determine the equilibrium behavior of the price level under
this rule, assuming that m0 = p∗
0.
iii. Show that the money supply rule considered in (ii) can be
combined with the money market clearing condition and
rewritten as a price level targeting rule of the form
it = ψ(pt −p∗
t ) + ut
for some constant ψ and stochastic process ut to be
determined.
iv. Suppose that the central bank wants to minimize the
volatility of the price level. Discuss the advantages and
disadvantages of the interest rate rule in (i) versus the
money supply rule in (ii) in light of your ﬁndings above.
2.3. Equilibrium indeterminacy and interest rate rules (based on
Woodford (2003))
Consider a classical economy with an exogenous real interest rate
process {rt}. Discuss the conditions under which the equilibrium
will be (locally) unique and solve for the equilibrium level of
inﬂation when the central bank follows the rules:
a. Rule #1: Partial adjustment
it = φiit−1 + (1 −φi)i∗
t
where φi ∈[0, 1] and i∗
t is a reference interest rate given by
i∗
t = ρ + φππt
b. Rule #2: Moving average inﬂation targeting
it = ρ + φππt

CHAPTER 2
where
πt = (1 −δ)
∞

k=0
δkπt−k
c. Show the equivalence between the two rules
2.4. On the welfare costs of inﬂation (based on Lucas (2000))
Consider an endowment economy where the representative con-
sumer’s period utility is given by
U

Ct, Mt
Pt

=

Ctψ

Mt/Pt
Ct
	1−σ
−1
1 −σ
where ψ (z) ≡z/(χ + z). The household’s budget constraint is
given by
PtCt + Qt Bt + Mt ≤Bt−1 + Mt−1 + PtYt
where {Yt} is an exogenous stochastic endowment, which is
nonstorable.
a. Derive the household’s optimality conditions, including the
demand for real balances.
b. Show that the Friedman rule is the welfare-maximizing mone-
tary policy
c. Focusing on a steady state with Y = 1, deﬁne the welfare cost
of inﬂation as the permanent percent increase in consumption
that would make the household indifferent between a steady
state inﬂation rate π and zero inﬂation.
d. Determine, up to a second order approximation, the welfare
losses resulting from ﬂuctuations in the nominal interest rate,
relative to a constant interest rate policy.
2.5. Optimal monetary policy in a classical economy with an exact
equilibrium representation
Consider a version of the classical economy with money in the
utility function, where the representative consumer maximizes
E0
∞
t=0 βtU(Ct, Mt
Pt , Nt) subject to the sequence of budget con-
straints
PtCt + Mt + QtBt ≤Mt−1 + Bt−1 + WtNt + Dt

49
Assume a period utility given by
U

Ct, Mt
Pt
, Nt

= log Ct + log Mt
Pt
−N 1+ϕ
t
1 + ϕ
(52)
Suppose there is a representative perfectly competitive ﬁrm,
producing the single consumption good. The ﬁrm has access to
the linear production function Yt(i) = AtNt(i), where productivity
evolves according to
At
At−1
= (1 + γa) exp{εa
t }
with {εa
t } an i.i.d. random process, normally distributed, with
mean 0 and variance σ 2
a .
The money supply varies exogenously according to the process
Mt
Mt−1
= (1 + γm) exp{εm
t }
(53)
where {εm
t } is an i.i.d., normally distributed process with mean 0
and variance σ 2
m. Assume that {εm
t } evolves exogenously, outside
the control of the monetary authority (e.g., could reﬂect shocks
in the monetary multiplier that prevent the monetary authority
from fully controlling the money supply). Finally, assume that all
output is consumed, so that in equilibrium Yt = Ct for all t.
a. Derive the optimality conditions for the problem of households
and ﬁrms.
b. Determine the equilibrium levels of aggregate employment,
output, and inﬂation (Hint: guess that the equilibrium involves
a constant velocity PtYt
Mt = V for all t).
c. Discuss how utility depends on the two parameters describing
monetary policy, γm and σ 2
m (recall that the nominal interest
rate is constrained to be non-negative, i.e., Qt ≤1 for all t).
Show that the optimal policy must satisfy the Friedman rule
(it = 0 for all t).
2.6. Equilibrium uniqueness in the classical model with money in the
utility function
Consider the classical model equilibrium, as described by condi-
tions (43), (47), and the simple interest rate rule
it = ρ + φππt
Show that the equilibrium is locally unique if and only if φπ > 1.

CHAPTER 2
2.7. A shopping time model
Assume that the transactions technology is such that consuming
Ct requires a quantity of shopping time Ns
t = S(Ct, Mt
Pt ), given real
balances Mt
Pt , where Sc > 0 and Sm ≤0. The period utility is given
by V(Ct, Lt) where Lt = 1 −Nt −Ns
t denotes leisure time and Nt
time at work.
a. Derive the implied utility function U(Ct, Mt
Pt , Nt), i.e., in terms
of consumption, hours, and real balances and discuss its
properties (sign of ﬁrst and second derivatives) as a function
of those of V and S
b. Using the ﬁnding in part a), derive the optimality conditions
of the household’s problem, under the sequence of budget
constraints (31), and show that under the optimal plan Wt
Pt sm ≃
it. Interpret the latter condition.
c. Derive the money demand function under the assumption that
V(Ct, Lt) = log Ct + χ log Lt and S

Ct, Mt
Pt

= Avt + B/vt −
2
√
AB where vt ≡PtCt/Mt (based on Schmitt-Grohé and Uribe
(2011))
2.8. A model with a cash-in-advance constraint
Consider a monetary economy where households’ maximize
∞
t=0 βt(log Ct −
1
1+ϕ N1+ϕ
t
) subject to the sequence of budget
constraints
PtCt + QtBt + Mt ≤Bt−1 + Mt−1 + WtNt + Tt
and the cash-in-advance (CIA) constraint PtCt ≤Mt−1 + Tt,
where Tt is a lump-sum monetary transfer to households. Output
is produced by a representative perfectly competitive ﬁrm with
technology Yt = Nt. The money supply grows at a constant
growth rate γm. There is no uncertainty.
a. Derive the household’s optimality conditions.
b. Determine how money growth affects equilibrium output.
c. What is the optimal rate of inﬂation?
2.9. A model with cash and credit goods
Assume that the utility of the representative household is given by
V(C1t, C2t, Nt)
(54)

51
where C1t denotes consumption of a “cash good” (i.e., a good
that requires cash in order to be purchased), C2t is consumption
of a “credit good” (which does not require cash), and Nt is labor
supply. For simplicity, assume that the price of the two goods is
identical and equal to Pt (this will be the case if the production
function of the representative ﬁrm is given by Y1t + Y2t = Nt and
there is perfect competition). Purchases of cash goods have to be
settled in cash, whereas credit goods can be ﬁnanced by issuing
one-period riskless nominal bonds.
The budget constraint is given by
Pt (C1t + C2t) + Qt Bt + Mt = Bt−1 + Mt−1 + WtNt + Tt
Finally, the cash-in-advance (CIA) constraint is given by
Pt C1t ≤Mt−1 + Tt
where, in equilibrium, Tt = 
Mt, i.e., transfers to households
correspond to money transfers made by the central bank, which
consumers take as given. For simplicity, assume no uncertainty.
a. Derive the ﬁrst-order conditions associated with the house-
hold’s problem
b. Note that whenever the CIA constraint is binding reduced form
period utility can be deﬁned as
U

Ct, Mt
Pt
, Nt

≡V

 Mt
Pt
, Ct −Mt
Pt
, Nt

where Ct = C1t + C2t. Show that Um ≥0, given the optimality
conditions derived in (a).