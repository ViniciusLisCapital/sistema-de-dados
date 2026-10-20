A Model of Unconventional Monetary Policy
Mark Gertler and Peter Karadi
NYU
April 2009
Abstract
This paper develops a quantitative monetary DSGE model that
allows for ﬁnancial intermediaries that face endogenous balance sheet
constraints. We use the model to simulate a crisis that has some basic
features of the current economic downturn. We then use the model to
quantitatively assess the eﬀect of direct central bank intermediation of
private lending, which is the essence of the unconventional monetary
policy that the Federal Reserve has developed to combat the subprime
crisis. We show numerically how central bank credit policy might help
moderate the simulated crisis. We then compute the optimal degree
of central bank credit intervention in this scenario and also compute
the welfare gains.
1

1
Introduction
Over most of the post-war the Federal Reserve has conducted monetary pol-
icy by manipulating the Federal Funds rate in order to aﬀect market interest
rates.. It has avoided lending directly in private credit markets, other than
to supply discount window loans to commercial banks. Even then, it limited
discount window activity to loans secured by government Treasury Bills
Since the onset of the subprime crisis in August 2007, the situation has
changed dramatically. To address the deterioration in both ﬁnancial and real
activity, the Fed has directly injected credit into private markets. It began
in the fall of 2007 by expanding the range of eligible collateral for discount
window loans to include agency debt and high grade private debt,. It did so
in conjunction with extending the maturity of these types of loans and with
extending eligibility to investment banks. Since that time, the Fed has set up
a myriad of lending facilities. For example, it has provided backstop funding
to help revive the commercial paper market. It has also intervened heavily in
mortgage markets by directly purchasing agency debt and mortgage-backed
securities.
(That mortgage rates have fallen signiﬁcantly since the onset
of this program is perhaps the strongest evidence of a payoﬀto the Fed’s
overall new strategy.) Plans are in the works to extend central bank credit
to securitized consumer loans.
The Fed’s balance sheet provides the most concrete measure of its credit
market intervention:.Since August 2007 the quantity of private assets it has
held has increased from virtually nothing to nearly a trillion and half. Ef-
fectively, over this period the Fed has attempted to oﬀset the decline of a
considerable fraction of private ﬁnancial intermediation by expanding central
bank intermediation. Now that the short term interest rate is at the zero
lower bound, the Fed is unable to stimulate.the economy using conventional
means. For time being, it must rely exclusively on its new unconventional
balance sheet operations.
At the same time, operational models of monetary policy have not kept
pace with the dramatic changes in actual practice. There is of a course a
lengthy contemporary literature on quantitative modeling of conventional
monetary policy, beginning with Christiano, Eichenbaum and Evans (2005)
and Smets and Wouters (2007.) The baseline versions of these models, how-
ever, assume frictionless ﬁnancial markets. They are thus unable to capture
ﬁnancial market disruptions that could motivate the kind of central bank
interventions in loan markets that are currently in play. Similarly, models
2

which do incorporate ﬁnancial market frictions, such as Bernanke, Gertler
and Gilchrist (1999) or Christiano, Motto and Rostagno (2005), have not yet
explicitly considered direct central bank intermediation as a tool of monetary
policy. Work that has tried to capture this phenomenon has been mainly
qualitative as opposed to quantitative (e.g., Kiyotaki and Moore (2008),
Adrian and Shin (2008).).
Accordingly, the objective of this paper is to
try to ﬁll in this gap in the literature: The speciﬁc goal is develop a quan-
titative macroeconomic model where it is possible to analyze the eﬀects of
unconventional monetary policy in the same general manner that existing
frameworks are able to study conventional monetary policy.
To be clear, we do not attempt to explicitly model the sub-prime cri-
sis. However, we do try to capture the key elements relevant to analyzing
the Fed’s credit market interventions. In particular, the current crisis has
featured a sharp deterioration in the balance sheets of many key ﬁnancial
intermediaries. As many observers argue, the deterioration in the ﬁnancial
positions of these institutions has had the eﬀect of disrupting the ﬂow of
funds between lenders and borrowers. Symptomatic of this disruption has
been a sharp rise in various key credit spreads as well as a signiﬁcant tight-
ening of lending standards This tightening of credit, in turn, has raised the
cost of borrowing and thus enhanced the downturn. The story does not end
here: The contraction of the real economy has reduced asset values through-
out, further weakening intermediary balance sheets, and so on. It is in this
kind of climate, that the central bank has embarked on its direct lending
programs.
To capture this kind of scenario, accordingly we incorporate ﬁnancial in-
termediaries within an otherwise standard macroeconomic framework. To
motivate why the condition of intermediary balance sheets inﬂuences the
overall ﬂow of credit, we introduce a simple agency problem between inter-
mediaries and their respective depositors. The agency problem introduces
endogenous constraints on intermediary leverage ratios, which have the ef-
fect of tieing overall credit ﬂows to the equity capital in the intermediary
sector. As in the current crisis, a deterioration of intermediary capital will
disrupt lending and borrowing in a way that raises credit costs.
To capture unconventional monetary policy in this environment, we allow
the central bank to act as intermediary by borrowing funds from savers and
then lending them to investors. Unlike, private intermediaries, the central
bank does not face constraints on its leverage ratio. (There is no agency
problem between the central bank and its creditors because it can commit
3

to always honoring its debt.) Thus, in a period of ﬁnancial distress that has
disrupted private intermediation, the central bank can intervene to support
credit ﬂows. On the other hand, we allow for the fact that, everything else
equal, public intermediation is likely to be less eﬃcient the private interme-
diation. When we use the model to evaluate these credit interventions, we
take into account this trade-oﬀ,
Section 2 presents the baseline model. The framework is closely related
to ﬁnancial accelerator model developed by Bernanke, Gertler and Gilchrist
(BGG, 1999).
That approach emphasized how balance sheet constraints
could limit the ability of non-ﬁnancial ﬁrms to obtain investment funds.
Firms eﬀectively borrowed directly from households and ﬁnancial interme-
diaries were simply a veil. Here ﬁnancial intermediaries, as we discussed,
ﬁnancial intermediaries are may be subject to endogenously determined bal-
ance sheet constraints. In addition, we allow for the central bank to lend
directly private credit markets.
Another diﬀerence from BGG is that, we use as a baseline framework the
conventional monetary business cycle framework developed by Christiano,
Eichenbaum and Evans (CEE, 2005), Smets and Wouters (SW, 2007) and
others. We adopt this approach because this framework has proven to have
reasonable empirical properties. Here we use it to study not only conventional
interest policy but also unconventional credit market interventions by the
central bank.
Section 3 presents a quantitative analysis of the model. We illustrate how
ﬁnancial factors may amplify and propagate some conventional disturbances.
We also consider a disturbance to the underlying quality of intermediary
assets and then show how this kinds of disturbance could create a contraction
in real activity that mirrors some of the basic features of the current crisis. We
then illustrate the extent to which central credit interventions could moderate
the downturn.
In section 4, we undertake a normative analysis of credit policy. We ﬁrst
solve for the optimal central credit intervention in crisis scenario considered in
section 3. We do so under diﬀerent assumptions about the eﬃciency costs of
central bank intermediation. We then compute for each case the net welfare
gains from the optimal credit market intervention. We ﬁnd that so long as
the eﬃciency costs are quite modest, the gains may be quite signiﬁcant. As
we discuss in the concluding remarks in section 5, this ﬁnding suggests a way
to think about the central bank’s choice between direct credit interventions
versus alternatives such as equity injections to private intermediaries.
4

2
The Baseline Model
The core framework is the monetary DSGE model with nominal rigidities de-
veloped by CEE and SW. To this we add ﬁnancial intermediaries that trans-
fer funds between households and non-ﬁnancial ﬁrms. An agency problem
constrains the ability of ﬁnancial intermediaries to obtain from households.
Another new feature is a disturbance to the quality of capital. Absent ﬁ-
nancial frictions, this shock introduces only a modest decline in output, as
the economy works to replenish the eﬀective capital stock. With frictions in
the intermediation process, however, the shock creates a signiﬁcant capital
loss in the ﬁnancial sector, which in turn induces tightening of credit and a
signiﬁcant downturn. As we show, it is in this kind of environment that the
is a potential role for central bank credit interventions.
There are ﬁve types of agents in the model: Households, ﬁnancial inter-
mediaries, non-ﬁnancial goods producers, capital producers, and monopolis-
tically competitive retailers. The latter are in the model only to introduce
nominal price rigidities. In addition, there is a central bank that conducts
both conventional and unconventional monetary policy. Without ﬁnancial
intermediaries the model is isomorphic to CEE and SW. As we show, though
addition of ﬁnancial intermediaries adds only a modest degree of complexity.
It has, however, a substantially on model dynamics and associated policy
implications..
We now proceed to characterize the basic ingredients of the model.
2.1
Households
There a continuum of identical households of measure unity. Each household
consumes, saves and supplies labor. Households save by lending funds to
competitive ﬁnancial intermediaries and possibly also by lending funds to
the government.
Within each household there are two types of members: workers and
bankers. Workers supply labor and return the wages they earn to the house-
hold. Each banker manages a ﬁnancial intermediary and similarly transfers
any earnings back to household. The household thus eﬀectively owns the
intermediaries that its bankers manage. The deposits it holds, however, are
in intermediaries that is does not own. Finally, within the family there is
perfect consumption insurance. As we make clear in the next section, this
simple form of heterogeneity within the family allows us to introduce ﬁnan-
5

cial intermediation in a meaningful way within an otherwise representative
agent framework.
At any moment in time the fraction 1 −f of the household members are
workers and the fraction f are bankers. Over time an individual can switch
between the two occupations. In particular, a banker this period stays banker
next period with probability θ, which is independent history (i.e., of how long
the person has been a banker.) The average survival time for a banker in any
given period is thus
1
1−θ. As will become clear, we introduce a ﬁnite horizon
for bankers to insure that over time they do not reach the point where they
can fund all investment from their own capital. Thus every period (1 −θ)f
bankers exit and become workers. A similar number of workers randomly
become bankers, keeping the relative proportion of each type ﬁxed. Bankers
who exit give their retained earnings to their respective household.
The
household, though, provides its new bankers with some start up funds, as we
describe in the next sub-section.
Let Ct be consumption and Lt family labor supply.
Then households
preferences are given by
max Et
∞
X
i=0
βi[ln(Ct+i −hCt+i−1) −
χ
1 + ϕL1+ϕ
t+i ]
(1)
with 0 < β < 1, 0 < h < 1 and χ, ϕ > 0. As in CEE and SW we allow for
habit formation to capture consumption dynamics. As in Woodford (2003)
we consider the limit of the economy as it become cashless, and thus ignore
the convenience yield to household’s from real money balances.
Both intermediary deposits and government debt are one period real
bonds that pay the gross real return Rt from t−1 to t. In the equilibrium we
consider, the instruments are both riskless and are thus perfect substitutes.
Thus, we impose this condition from the outset. Thus let Bt be the total
quantity of short term debt the household acquires, Wt, be the real wage, Πt
net payouts to the household from ownership of both non-ﬁnancial and ﬁ-
nancial ﬁrms and, Tt lump sum taxes. Then the household budget constraint
is given by
Ct = WtLt + Πt + Tt + RtBt −Bt+1
(2)
Note that Πt is net the transfer the household gives to its members that enter
banking at t.
6

Let (t denote the marginal utility of consumption. Then the household’s
ﬁrst order conditions for labor supply and consumption/saving are standard:
(tWt = χLϕ
t
(3)
with
(t = Ct −hCt−1)−1 −βhEt(Ct+1 −hCt)−1
and
EtβΛt,t+1Rt+1 = 1
(4)
with
Λt,t+1 ≡λt+1
λt
2.2
Financial Intermediaries
Financial intermediaries lend funds obtained from households to non-ﬁnancial
ﬁrms. Let Njt be the amount of wealth - or net worth - that a banker/intermediary
j has at the end of period t; Bjt the deposits the intermediary obtains from
households, Sjt the quantity of ﬁnancial claims on non-ﬁnancial ﬁrms that the
intermediary holds and Qt the relative price of each claim. The intermediary
balance sheet is then given by
QtSjt = Njt + Bjt
(5)
For the time being, we ignore the possibility of the central bank supplying
funds to the intermediary.
As we noted earlier, household deposits with the intermediary at time
t, pay the non-contingent real gross return Rt+1 at t + 1. Thus Bjt may be
thought of as the intermediary’s debt and Njt as its equity capital. Interme-
diary assets earn the stochastic return Rkt+1 over this period. Both Rkt+1
and Rt+1 will be determined endogenously.
Over time, the banker’s equity capital evolves as the diﬀerence between
earnings on assets and interest payments on liabilities:
Njt+1
=
Rkt+1QtSjt −Rt+1Bjt
(6)
=
(Rkt+1 −Rt+1)QtSjt + Rt+1Njt
(7)
7

Any growth in equity above the riskless return depends on the premium
Rkt+1 −Rt+1 the banker earns on his assets, as well as his total quantity of
assets, QtSjt .
Let βΛt,t+i be the stochastic discount the the banker at t applies to earn-
ings at t + i. Since the banker will not fund assets with a discounted return
less than the discounted cost of borrowing, for the intermediary to operate
the following inequality must apply:
EtβΛt,t+1+i(Rkt+1+i −Rt+1+i) ≥0
∀i ≥0
With perfect capital markets, the relation always holds with equality: The
risk-adjusted premium is zero. With imperfect capital markets, however, the
premium may be positive due to limits on the intermediary’s ability to obtain
funds.
So long as the intermediary can earn a risk adjusted return that is greater
than or equal to the return the household can earn on its deposits, it pays for
the banker to keep building assets until exiting the industry. Accordingly,
the banker’s objective is to maximize expected terminal wealth, given by
Vjt
=
max Et
X
i
(1 −θ)θiβiΛt,t+i(Njt+1+i)
(8)
=
max Et
X
i
(1 −θ)θiβiΛt,t+i[(Rkt+1+i −Rt+1+i)Qt+iSjt+i + Rt+1+iNjt+i]
To the extent the discounted risk adjusted premium in any period, βiΛt,t+i[(Rkt+1+i−
Rt+1+i), is positive, the intermediary will want to expand its assets indeﬁ-
nitely by borrowing additional funds from households. To motivate a limit
on its ability to do so, we introduce the following moral hazard/costly en-
forcement problem: At the beginning of the period the banker can choose to
divert the fraction λ of available funds from the project and instead transfer
them back to the household of which he or she is a member. The cost to the
banker is that the depositors can force the intermediary into bankruptcy and
recover the remaining fraction 1 −λ of assets.. However, it is too costly for
the depositors recover the fraction of funds that the banker diverted.
Accordingly for lenders to be willing to supply funds to the banker, the
following incentive constraint must be satisﬁed:
Vjt ≥λQtSjt
(9)
8

The left side is what the banker would lose by diverting a fraction of assets.
The right side is the gain from doing so.
We can express Vjt as follows:
Vjt = vt · QtSjt + ηtNjt
(10)
with
vt
=
Et{(1 −θ)βΛt,t+1(Rkt+1 −Rt+1) + βΛt,t+1θxt,t+1vt+1}
(11)
ηt
=
Et{(1 −θ) + βΛt,t+1θzt,t+1ηt+1}
where xt,t+i ≡Qt+iSjt+i/QtSjt, is the gross growth rate in assets between t
and t + i, and zt,t+i ≡Njt+i/Njt is the gross growth rate of net worth. The
variable vt has the interpretation of the expected discounted marginal gain
to the banker of expanding assets QtSjt by a unit, holding net worth Njt con-
stant, and while ηt is the expected discounted value of having another unity
of Njt,holding Sjt constant.
With frictionless competitive capital markets,
intermediaries will expand borrowing to the point where rates of return will
adjust to ensure vt is zero. The agency problem we have introduced, however,
may place limits on the arbitrage. In particular, as we next show, when the
incentive constraints is binding, the intermediary’s assets are constrained by
its equity capital.
Note ﬁrst that we can express the incentive constraints as
ηtNjt + vtQtSjt ≥λQtSjt
(12)
If this constraint binds, then the assets the banker can acquire will depend
positively on his/her equity capital:
QtSjt
=
ηt
λ −vt
Njt
(13)
=
φtNjt
where φt ratio of privately intermediated assets to equity, which we will
refer to as the (private) leverage ratio.. Holding constant Njt, expanding
Sjt raises the bankers’ incentive to divert funds. The constraint (13) limits
the intermediaries leverage ratio to the point where the banker’s incentive
to cheat is exactly balanced by the cost. In this respect the agency problem
9

leads to an endogenous capital constraint on intermediary’s ability to acquire
assets.
Given Njt > 0, the constraint binds only if 0 < vt < λ. In this instance,
it is proﬁtable for the banker to expand assets (since vt > 0). Note that in
this circumstance the leverage ratio that depositors will tolerate is increasing
in vt. The larger is vt, the greater is the cost to the banker from being forced
into bankruptcy. If vt increases above λ, the incentive constraint does not
bind: the franchise value of the intermediary always exceed the gain from
diverting funds. In the equilibrium we construct below, under reasonable
parameter values the constraint always binds.
We can now express the evolution of the banker’s net worth as
Njt+1 = [(Rkt+1 −Rt+1)φt + Rt+1]Njt
(14)
Note that the sensitivity of Njt+1 to the ex post realization of the excess
return Rkt+1 −Rt+1 is increasing in the leverage ratio φt. In addition, it
follows that
zt,t+1 = Njt+1/Njt = (Rkt+1 −Rt+1)φt + Rt+1
xt,t+1 = Qt+1Sjt+2/QtSt+1 = (φt+1/φt)(Njt+1/Nt) = (φt+1/φt)zt,t+1
Importantly, all the components of φt do not depend on ﬁrm-speciﬁc
factors. Thus to determine total intermediary demand for assets we can sum
across individual demands to obtain:
QtSIt = φtNt
(15)
where SIt reﬂects the aggregate quantity of intermediary assets and Nt de-
notes aggregate intermediary capital. In the general equilibrium of our model,
variation in Nt, will induce ﬂuctuations in overall asset demand by interme-
diaries. Indeed, a crisis will feature a sharp contraction in Nt.
We can derive an equation of motion for Nt, by ﬁrst recognizing that it
is the sum of the net worth of existing banker/intermediaries, Net, and the
net worth of entering (or "new") bankers, Nnt.
Nt = Net + Nnt
(16)
10

Since the fraction θ of bankers at t −1 survive until t, Net is given by
Net = θ[(Rkt −Rt)φt + Rt]Nt−1
(17)
Observe that the main source of variation in Net will be ﬂuctuations in the
ex post return on assets Rkt. Further, the impact on Net is increasing in the
leverage ratio φt.
As we noted earlier, newly entering bankers receive "start up" funds from
their respective households. We suppose that the startup money the house-
hold gives its new banker a transfer equal to a small fraction of the value of
assets that exiting bankers had intermediated in their ﬁnal operating period.
The rough idea is that how much the household feels that is new bankers
need to start, depends on the scale of the assets that the exiting bankers
have been intermediating. Given that the exit probability is i.i.d., the total
ﬁnal period assets of exiting bankers at t is (1 −θ)QtSt−1. Accordingly we
assume that each period the household transfers the fraction ξ/(1−θ) of this
value to its entering bankers. Accordingly, in the aggregate,
Nnt = ξQtSt−1
(18)
Combining (17) and (18) yields the following equation of motion for Nt.
Nt = θ[(Rkt −Rt)φt + R]Nt−1 + ξQtSt−1
Observe that ξ helps pin down the steady state leverage ratio QS/N. Indeed,
in the next section we calibrate ξ to match this evidence. The resulting value,
as we show, is quite small.
2.3
Credit Policy
In the previous section we characterized how the total value of privately inter-
mediated assets, QtSpt, is determined. We now suppose that the central bank
is willing to facilitate lending. Let QtSgt be the value of assets intermediated
via government assistance and let QtSt be the total value of intermediated
assets: i.e.,
QtSt = QtSpt + QtSgt
(19)
To conduct credit policy, the central bank issues government debt to
households that pays the riskless rate Rt+1 and then lends the funds to non-
ﬁnancial ﬁrms at the market lending rate Rkt+1. We suppose that government
11

intermediation involves eﬃciency costs: In particular, the central bank credit
involves an eﬃciency cost of τ per unit supplied. This deadweight loss could
reﬂect the costs of raising funds via government debt. It might also reﬂect
costs to the central bank of identifying preferred private sector investments.
On the other hand, the government always honors its debt: Thus, unlike the
case with private ﬁnancial institutions ,is no agency conﬂict than inhibits the
government from obtaining funds from households. Put diﬀerently, unlike
private ﬁnancial intermediation, government intermediation is not balance
sheet constrained.
An equivalent formulation of credit policy involves having the central
bank channel funds to non-ﬁnancial borrowers via private ﬁnancial interme-
diaries, as has occurred in practice. Here we assume that the government has
an advantage over private households in enforcing in enforcing payment of
debts by private intermediaries. In particular, it is not possible for an inter-
mediary to walk away from a ﬁnancial obligation to the federal government,
the same way it can a private entity. Unlike private creditors, the federal
government has various means to track down and recover debts. It follows
that In this instance, the balance sheets constraints that limit intermediaries
ability to obtain private credit do not constrain their ability to obtain cen-
tral bank credit. Accordingly, in this scenario, after obtaining funds from
households at the rate Rt+1, the central bank lends freely to private ﬁnan-
cial intermediaries at the rate Rkt, which in turn lend to non-ﬁnancial ﬁrms
at the same rate. Private intermediaries earn zero proﬁts on this activity:
the liabilities to the central bank perfectly oﬀset the value of the claims on
non-ﬁnancial ﬁrms, implying that there is no eﬀect on intermediary balance
sheets. The behavior of the model is thus exactly same as if the central
bank directly lends to non-ﬁnancial ﬁrms. Note that in this instance, the
eﬃciency cost τ is interpretable as the cost of publicly channeling funds to
private intermediaries as opposed to directly to non-ﬁnancial ﬁrms.
Accordingly, suppose the central bank is willing to fund the fraction ψt
of intermediated assets: i.e.,
QtSgt = ψtQtSt
(20)
It issues amount of government bonds Bgt, equal to ψtQtSt to funds this
activity. It’s net earnings from intermediation in any period t thus equal
(Rkt+1−Rt+1)Bgt. These net earnings provide a source of government revenue
and must be accounted for in the budget constraint, as we discuss later.
12

Since privately intermediated funds are constrained by intermediary net
worth, we can rewrite equation (19) to obtain
QtSt
=
φtNt + ψtQtSt
=
φctNt
where φt is the leverage ratio for privately intermediated funds (see equations
(13) and (15), and where φct is the leverage ratio for total intermediated
funds, public as well as well private.
φct =
1
1 −ψt
φt
Observe that φct depends positively on the intensity of credit policy, as mea-
sured by ψt. Later how describe how the central might choose ψt to combat
a ﬁnancial crisis.
2.4
Intermediate Goods Firms
We next turn to the production and investment side of the model economy.
Competitive non-ﬁnancial ﬁrms produce intermediate goods that are even-
tually sold to retail ﬁrms. The timing is as follows: At the end of period t,
an intermediate goods producer acquires capital Kt+1 for use in production
in the subsequent period. After production in period t + 1, the ﬁrm has the
option of selling to capital on the open market. There are no adjustment
costs at the ﬁrm level. Thus, the ﬁrm’s capital choice problem is always
static, as we discuss below.
The ﬁrm ﬁnances its capital acquisition each period by obtaining funds
from intermediaries. To acquire the funds to buy capital, the ﬁrm issues St
claims equal to the number of units of capital acquired Kt+1 and prices each
claim at the price of a unit of capital Qt. That is, QtKt+1 is the value of
capital acquired and QtSt is the value of claims against this capital. Then
by arbitrage:
QtKt+1 = QtSt
(21)
We assume that there are no frictions in the process of non-ﬁnancial
ﬁrms obtaining funding from intermediaries. The intermediary has perfect
information about the ﬁrm and has no problem enforcing payoﬀs. This con-
trasts with the process of the intermediary obtaining funding from house-
holds. Thus, within our model, only intermediaries face capital constraints
13

on obtaining funds. These constraints, however, aﬀect the supply of funds
available to non-ﬁnancial ﬁrms and hence the required rate of return on cap-
ital these ﬁrms must pay. Conditional on this required return, however, the
ﬁnancing process is frictionless for non-ﬁnancial ﬁrms.
At time t+1 the ﬁrm produces output Yt+1, using capital and labor Lt+1,
and by varying the utilization rate of capital, Ut+1. Let At+1 denote total
factor productivity. Then production is given by:
Yt+1 = At+1(Ut+1Kt+1)αL1−α
t+1
(22)
What the ﬁrm earns in t + 1 is the value of output plus the value of its
capital stock left over net ﬁnancing and labor costs. Let Pmt be the price of
intermediate goods output. Then from the vantage of period t, where the
ﬁrm makes its’ capital decision for t + 1, its objective is given by:
max EtβΛt,t+1[Pmt+1Yt+1 +(Qt+1 −δ(Ut))ξt+1Kt+1 −Rt+1QtKt+1 −Wt+1Lt+1]
where as before βΛt,t+1 is the ﬁrm’s stochastic discount factor, δ(Ut) is the
capital depreciation rate, which is increasing and convex in Ut, Wt+1 is the
real wage, and Rt+1 is the state-contingent required return on capital. In
addition ψt+1 is an exogenous factor that aﬀects the eﬀective quantity of
capital. That is, after production in t + 1, the number of units of capital left
over is (1 −δ(Ut))ψt+1Kt+1. Assuming that capital that replacement price of
capital that has depreciated is unity, then the value of the capital stock that
is left over is given by (Qt+1 −δ(Ut))ψt+1Kt+1. Finally, ψt+1 may be thought
of as a measure of the quality of the existing.
Maximizing with respect to Kt+1 yields
EtβΛt,t+1Rt+1 = Et{βΛt,t+1
Pmt+1α Yt+1
Kt+1 + (Qt+1 −δ(Ut+1))ξt+1
Qt
}
(23)
At an interior optimum, the discounted cost of capital must equal the dis-
counted return.
At t+1, the ﬁrm chooses the utilization rate and labor demand as follows:
Pmt+1αYt+1
Ut+1
= δ
0(Ut+1)
(24)
Pmt+1αYt+1
Lt+1
= Wt+1
(25)
14

2.5
Capital Producing Firms
At the end of period t, competitive capital producing ﬁrms buy capital from
intermediate goods producing ﬁrms and then repair depreciated capital and
builds new capital. They then sell both the new and re-furbished capital. As
we noted earlier, the cost of replacing worn out capital is unity. The value of
a unit of new capital is Qt, as is the value of a unit of re-furbished capital.
If It is total investment by a capital producing ﬁrm, then the ﬁrms proﬁts at
t are given by.
QtKt+1 −(Qt −δ(Ut))ξtKt −It
Let Int ≡It −δ(Ut))ξtKt, be the ﬁrm’s objective. Then we can express is
maximization problem, as to choose Int, Kt+1 and Kt to solve
max Qt(Kt+1 −ξtKt) −Int
(26)
subject to
Kt+1 −ξtKt = Int −S
µ Int + Iss
Int−1 + Iss
¶
(Int + Iss)
(27)
where Iss is steady state investment, which consists only of replacement in-
vestment. As in CEE, we allow for ﬂow adjustment costs of investment, but
restrict these costs to modify the net investment ﬂow.
The ﬁrst order condition for investment gives the follow ”Q” relation for
net investment:
Qt = [1−S
µ Ia
nt
Ia
nt−1
¶
−S 0
µ Ia
nt
Ia
nt−1
¶ µ Ia
nt
Ia
nt−1
¶
]−1[1−βEtΛt,t+1Qt+1S 0
µIa
nt+1
Ia
nt
¶ µIa
nt+1
Ia
nt
¶2
]
(28)
where Ia
nt ≡Int + Iss may be thought of as "adjusted" net investment.
2.6
Retail Firms
Final output Yt is a CES composite of a continuum of mass unity of diﬀeren-
tiated retail ﬁrms, that use intermediate output as the sole input. The ﬁnal
output composite is given by
15

Yt = [
Z 1
0
Yft
ε−1
ε−df]
ε
ε−1
(29)
where Yft is output by retailer f. From cost minimization by users of ﬁnal
output:
Yft = (Pft
Pt
)−εYt
(30)
Pt = [
Z 1
0
Pft
1
1−ε df]1−ε
(31)
Retailers simply re-package intermediate output.
It takes one unit of
intermediate output to make a unit of retail output.
The marginal cost
is thus the relative intermediate output price Pmt.
We introduce nominal
rigidities following CEE. In particular, each ﬁrm period a ﬁrm is able to
freely adjusts price with probability 1 −ς.
In between these periods, the
ﬁrm is able to index its price to the lagged rate of inﬂation. The retailers
pricing problem then is to choose the optimal reset price P ∗
t to solve
max
∞
X
i=0
θiβiΛt,t+i[ P ∗
t
Pt+i
iY
k=0
(1 + πt+i−1) −Pmt+i]Yft
(32)
where πt is the rate of inﬂation from t −i to t. The ﬁrst order necessary
conditions are given by:
∞
X
i=0
θiβiΛt,t+i[ P ∗
t
Pt+i
iY
k=0
(1 + πt+i−1) −μPmt+i]Yft = 0
(33)
with
μ =
1
1 −1/ε
From the law of large numbers, the following relation for the evolution of the
price level emerges.
Pt = [(1 −θ)(P ∗
t )
1
1−ε + θ(Πt−1Pt−1)
1
1−ε]1−ε
(34)
16

2.7
Resource Constraint and Government Policy:
Output is divided between consumption, investment, government consump-
tion, Gt and expenditures on government intermediation, τψtQtKt+1. We
suppose further that government expenditures are exogenously ﬁxed at the
level G. The economy-wide resource constraint is thus given by
Yt = Ct + It + G + τψtQtKt+1
(35)
Government expenditures, further, are ﬁnanced by lump sum taxes and
government intermediation:
G = Tt + (Rkt −Rt)Bgt−1
where government bonds, Bgt−1, ﬁnance total government intermediated as-
sets, Qtψt−1St−1.
We suppose monetary policy is characterized by a simple Taylor rule with
interest-rate smoothing. Let it be the net nominal interest rate, i the steady
state nominal rate, and Y ∗
t the natural (ﬂexible price equilibrium) lever of
output. Then:
it = (1 −ρ)[i + ιππt + ιy(log Y ∗
t −log Yt) + ρit−1 + t
(36)
where the smoothing parameter ρ lies between zero and unity, and where t is
an exogenous shock to monetary policy, and where the link between nominal
and real interest rates is given by the following Fisher relation
1 + it = Rt+1
Pt+1
Pt
(37)
Finally, we also introduce a feedback role for credit policy.
We sup-
pose that the central bank injects credit in response to movements in credit
spreads, according to the following feedback rule:
ψt = ψ + ν[(Rkt+1 −Rt+1) −(Rk −R)]
(38)
where ψ is the steady state fraction of publicly intermediated assets and
Rk −R is the steady state premium. In addition, the feedback parameter
exceeds unity. According to this rule, the central bank expands credit as the
spread increase relative to its steady state value.
This completes the description of the model.
17

3
Model Analysis
3.1
Calibration
Table 1 list the choice of parameter values for our baseline model. Overall
there are eighteen parameters. Fifteen are conventional. Three (λ, ξ, θ) are
speciﬁc to our model.
We begin with the conventional parameters. For the discount factor β, the
depreciation rate δ, the capital share α, the elasticity of substitution between
goods, ε, and the government expenditure share, we choose conventional
values. Also, we normalize the steady state utilization rate u at unity. We use
estimates from Justinano, Primiceri and Tambalotti (2009) to obtain values
for the following preference and technology parameters: the habit parameter
h, the elasticity of marginal depreciation with respect to the utilization rate,
ζ, and the inverse elasticity of net investment to the price of capital ηi. We
pick the relative utility weight on labor χ to ﬁx hours worked at one third of
available time. Finally, we choose a Frisch elasticity of labor supply equal to
3. Because, unlike most of the existing quantitative models. we do not allow
for wage rigidity, we choose a relatively high labor supply elasticity, though
one that is not inconsistent with the evidence if we interpret this elasticity
as applying to the extensive margin.
We the price rigidity parameter, γ, to have prices ﬁxed on average for
a year. We choose a high value to compensate for not including real price
rigidities in the model. Our parametrization leads to a slope coeﬃcient in
the Phillips curve that is consistent with the evidence. In addition, we set
indexing parameter γp at .5, following CEE. Finally, the feedback coeﬃcients
in the monetary policy rule, κπ and κy obey a conventional Taylor rule, with
a smoothing parameter ρ. This rule is consistent with the evidence for post-
1984.
Our choice of the ﬁnancial sector parameters - the fraction of capital that
can be divertedλ, the proportional transfer to entering bankers ξ, and the
survival probability θ - is meant to be suggestive. We pick these parame-
ters to hit the following three targets: a steady state interest rate spread
of one hundred basis points; a steady state leverage ratio of four; and an
average horizon of bankers of a decade. We base the steady state target for
the spread on the pre-2007 spreads between mortgage rates and government
bonds and between BAA corporate vs. government bonds. The choice of the
leverage ratio is a rough guess of a reasonable economy-wide mortgage. For
18

the mortgage sector, which was about one third of total assets in 2007, this
ratio was between twenty and thirty to one. It was obviously much smaller
in other sectors.
3.2
Experiments
We begin with several experiments designed to illustrate how the model be-
haves. We then consider a "crisis" experiment that mimics some of the basic
features of the current downturn. We then consider the role of central bank
credit policy in moderating the crisis.
Figure 1 shows the response of the model economy to three disturbances:
a technology shock, a monetary shock, and shock to intermediary net worth.
In each case, the direction of the shock is set to produce a downturn. The
ﬁgure then shows the responses of three key variables: output, investment
and the premium. In each case the solid shows the response of the baseline
model. The dotted line gives the response of the same model, but with the
ﬁnancial frictions removed.
The technology shock is a negative one percent innovation in TFP, with a
quarterly autoregressive factor of 0.95. The intermediary balance mechanism
produces a modest ampliﬁcation of the decline in output the baseline model
relative to the conventional DSGE model. The ampliﬁcation is mainly the
product of substantially enhanced decline investment:on the order of ﬁfty
percent relative to the frictionless model. The enhanced response of invest-
ment in the balance model is a product of the rise in the premium, plotted
in the last panel on the right. The unanticipated decline in investment re-
duces asset prices, which produces a deterioration an intermediary balance
sheets, pushing up the premium. The increase in the cost of capital, further
reduces capital demand by non-ﬁnancial ﬁrms, which enhances the downturn
in investment and asset prices. In the conventional model without ﬁnancial
frictions, of course, the premium is ﬁxed at zero.
The monetary shock is an unanticipated twenty-ﬁve basis point increase in
the short term interest rate. The eﬀect on the short term interest rate persists
due to interest rate smoothing by the central bank. Financial frictions lead
to greater ampliﬁcation relative to the case of the technology shock. This
enhanced ampliﬁcation is due to he fact that, everything else equal, the
monetary policy shock has a relatively large eﬀect on investment and asset
prices. The latter triggers the ﬁnancial accelerator mechanism.
To illustrate how at the core of the ampliﬁcation mechanism in the ﬁrst
19

two experiments is procyclical variation in intermediary balance sheets, we
consider a redistribution of wealth from intermediaries to households.
In
particular, we suppose that intermediary net worth declines by one percent
and is transferred to households. In the model with no ﬁnancial frictions, this
redistribution has no eﬀect (it is just a transfer of wealth within the family.)
The decline in intermediary in our baseline model, however, produces a rise
in the premium, leading to a subsequent decline in output and investment.
We now turn to the crisis experiment. The initiating disturbance is a
decline in capital quality. What we are trying to capture, is a shock to the
quality of intermediary assets that produce a enhanced decline in the capital
of these institutions, due to their high degree of leverage. In this rough way,
we capture the broad dynamics of the sub-prime crises. We ﬁx the size of
the shock so that the downturn is of broadly similar magnitude to the one
we have recently experienced.
We ﬁrst consider the disturbance to the economy without credit policy
and then illustrate the eﬀects of credit policy. The initiating shock is a ﬁve
percent decline in capital quality, with a quarterly autoregressive factor of
0.66. Absent any changes in investment, the shock produces a roughly ten
percent decline in eﬀective capital stock over a two year period. The loss
in value of the housing stock relative to the total capital stock was in this
neighborhood.
In the model without ﬁnancial frictions, then shock produces only a mod-
est decline in output. Output falls a bit initially due to the reduced eﬀective
capital stock. Because capital is below its steady state, however, investment
picks up. Individuals consume less and eventually work more.
By contrast, in the model with frictions in the intermediation process,
there is a sharp recession.
The deterioration in asset quality produces a
magniﬁed decline in intermediary capital. The interest rate spread skyrockets
as a consequence, and output tanks. Output initially falls about three percent
relative to trend and then decreases to about six percent relative to trend.
Though the model does not capture the details of the recession, it does
produce an output decline of similar magnitude. Recovery of output to trend
does not occur until roughly ﬁve years until after the shock.
This slow
recovery is also in line with current projections. Contributing to the slow
recovery is the delayed movement of intermediary capital back to trend. It is
mirrored in persistently above trend movement in the spread. Note that over
this period the intermediary sector is eﬀectively deleveraging: It is building
up equity relative to assets. Thus the model captures formally the informal
20

notion of how the need for ﬁnancial institutions to deleverage can slow the
recovery of the economy.
We now consider credit interventions by the central bank. Figure 3 con-
siders several diﬀerent intervention intensities. In the ﬁrst case, the feedback
parameter ν in the policy rule given by equation (38) equals 50. At this value,
the credit intervention is roughly of similar magnitude to what has occurred
in proactive. The solid line portrays this case. In the second, the feedback
parameter is raised to 500, which increases the intensity of the response.
The dashed line portrays this case. Finally, for comparison, the dashed and
dotted line portrays the case with no credit market intervention.
In each instance, the credit policy signiﬁcantly moderates the contrac-
tion. The prime reason is that central intermediation dampens the rise in
the spread, which in turn dampens the investment decline. The moderate
intervention (ν = 50) produces an increase in the central bank balance sheet
equal to approximately ten percent of the value of the capital stock. This
is roughly in accord with the degree of intervention that has occurred in
practice. The aggressive intervention further moderates the decline, though
the gain relative to the moderated intervention is small. In this case, central
bank lending increases to approximately twenty percent of the value of the
capital stock.
3.3
Optimal Policy and Welfare
We now consider the welfare gains from central bank credit policy and also
compute the optimal degree of intervention. We take as the objective the
household’s utility function.
We start with the crisis scenario of the previous section.
We take as
given the Taylor rule for setting interest rates. This rule may be thought of
as describing monetary policy in normal times. We suppose that it is credit
policy that adjusts to the crisis. We then ask what is the optimal choice
of the feedback parameter ν in the wake of the capital quality shock. In
doing the experiment, we take into account the eﬃciency costs of central
bank intermediation, as measured by the parameter τ. We consider a range
of values for τ.
Following Faia and Monacelli (2007), we begin by writing the household
utility function in recursive form:
Ωt = U(Ct, Lt) + βEtΩt+1
(39)
21

We then take a second order approximation of this function about the steady
state. We next take a second order approximation of the whole model about
the steady state and then use this approximation to express the objective
as a second order function of the predetermined variables and shocks to the
system. In doing this approximation, we take as given the policy-parameters,
including the feedback credit policy parameter ν. We then search numerically
for the value of ν that optimizes Ωt as a response to the capital quality shock.
To compute the welfare gain from the optimal credit policy we also com-
pute the value of Ωt under no credit policy. We then take the diﬀerence in
Ωt in the two cases to ﬁnd out how much welfare increases under the opti-
mal credit policy. To convert to consumption equivalents, we ask how much
the individuals consumption would have to increase each period in the no
credit policy case to be indiﬀerent with the case under the optimal credit
policy. Because we are just analyzing a single crisis and not an on-going se-
quence, we simply cumulate to the present value of consumption-equivalent
beneﬁts and normalize by one year’s steady state consumption. Put diﬀer-
ently, we suppose the economy is hit with a crisis and then ask what are the
consumption-equivalent beneﬁts from credit policy in moderating this single
event. Since we are analyzing a single event, it makes sense to us to cumu-
late up the beneﬁts instead of presenting them as an indeﬁnite annuity ﬂow,
where most of the ﬂow is received after the crisis is over.
Figure 4 presents the results for a range of values of the steady state
markup and also a range of values of the eﬃciency cost τ. In the baseline
case of with a ﬁfteen percent markup and no eﬃciency cost (τ = 0), the
beneﬁt from credit policy of moderating the recession is worth 6.50 percent of
one years recession. At reasonable levels of the eﬃciency cosy (e.g. ten basis
points), the gain is on the order of 5.0 percent of steady state consumption.
It decreases to zero, as the eﬃciency costs goes to forty basis points, as fairly
large number. Though we do not report the results here, for τ less than forty
basis points the optimal credit policy comes closely to fully stabilizing the
markup
The welfare loss is increasing in the steady state distortion. If we interpret
this distortion from the markup as also capturing distortionary tax eﬀects,
then a much high value may be justiﬁed. For for example, average eﬀective
labor taxes are in the range of thirty to thirty ﬁve percent. Assuming the
price markup is in the neighborhood of ﬁfteen to twenty percent, then a
steady state distortion up to ﬁfty percent is reasonable. Accordingly, we
consider two alternatives to our baseline: one involving a thirty-three percent
22

markup and the other a ﬁfty percent markup. As the ﬁgure illustrates, the
gains to the optimal credit policy increase substantially, increasing to over
fourteen percent of one year’s consumption for the tau equals zero case and
remaining above ten percent as tau reaches twenty basis points.
One factor moderating the welfare loss is that the marginal disutility of
labor declines during the downturn. It could be that the simple preference
structure we use to pin down labor supply gives a misleading read on the
utility gains from increased leisure during recession. Accordingly, we redo
the exercise, this time considering the case of perfectly elastic labor supply.
In this case individuals only care about consumption ﬂuctuations. As ﬁgure
6 illustrates, in this case the beneﬁts from the optimal credit policy increase
roughly twenty percent across the board.
4
Concluding Remarks
We developed a quantitative monetary DSGE model with ﬁnancial intermedi-
aries that face endogenously determined balance sheet constraints. We then
used the model to evaluate the eﬀect of expanding central bank credit inter-
mediation to combat a simulated ﬁnancial crisis. We ﬁnd that the welfare
beneﬁts may be substantial if the eﬃciency costs of government intervention
are modest.
If we abstract from the issue of eﬃciency costs, an equivalent type of credit
intervention in our model would be direct equity injections into ﬁnancial
intermediaries. Expanding intermediaries equity would of course expand the
volume of assets that they can intermediate. In our view, a key factor in
choosing between these two policies involves the eﬃciency costs of the policy
action. For certain types of lending, e.g. securitized high grade assets such as
mortgaged=backed securities, the costs of central bank intermediation might
be relatively low. In this case, direct central bank intermediation may be
justiﬁed. In other cases, e.g. C&I loans that requires constant monitoring
of borrowers, central bank intermediation may be highly ineﬃcient. In this
instance, capital injections may be the preferred route. By expanding our
model to allow for asset heterogeneity we can address this issue.
Finally, we consider a one time crisis and evaluated the policy response.
In subsequent work we plan to model to the phenomenon as an infrequently
occurring rare disaster in spirit of Barro (2009) and others. In this literature
the disaster is taking as a purely exogenous event. Within our framework we
23

can evaluate the gains from various policy responses, using the same tools as
applied in this literature to compute welfare.
24

Table 1: Parameter Values for Baseline Model
Households
β
0.995
Discount rate
h
0.700
Habit parameter
χ
5.584
Relative utility weight of labor
ϕ
0.333
Inverse Frisch elasticity of labor supply
Financial Intermediaries
λ
0.383
Fraction of capital that can be diverted
ξ
0.003
Proportional transfer to the entering bankers
θ
0.972
Survival rate of the bankers
Intermediate good ﬁrms
α
0.330
Eﬀective capital share
u
1.000
Steady state utilization rate
δ(u)
0.025
Steady state depreciation rate
ζ
1.000
Elasticity of marginal depreciation with respect to utilization rate
Capital Producing Firms
ηi
2.500
Inverse elasticity of net investment to the price of capital
Retail ﬁrms
ε
11.000
Elasticity of substitution
γ
0.750
Probability of keeping prices ﬁxed
γP
0.500
Measure of price indexation
Government
κπ
1.500
Inﬂation coeﬃcient of the Taylor rule
κX
-0.500
Output gap coeﬃcient of the Taylor rule
G
Y
0.200
Steady state proportion of government expenditures
27

Figure 1: Responses to Technology (a) , Monetary (m) and Wealth (w) Shocks
0
20
40
−0.015
−0.01
−0.005
0
Y
a
 
 
0
20
40
−0.1
−0.05
0
0.05
I
0
20
40
−1
0
1
2
x 10
−3
Rk−R
0
20
40
−10
−5
0
5
x 10
−3
Y
m
0
20
40
−0.06
−0.04
−0.02
0
0.02
I
0
20
40
−5
0
5
10
15
x 10
−4
Rk−R
0
20
40
−4
−2
0
2
x 10
−3
Y
N
0
20
40
−0.02
−0.01
0
0.01
I
0
20
40
−5
0
5
10
x 10
−4
Rk−R
FA
SDGE
1

Figure 2: Responses to a Capital Quality Shock
0
20
40
−0.04
−0.02
0
s
 
 
0
20
40
−5
0
5 x 10
−3
R
0
20
40
−0.02
0
0.02
Rk−R
0
20
40
−0.1
0
0.1
Y
0
20
40
−0.04
−0.02
0
C
0
20
40
−0.5
0
0.5
I
0
20
40
−0.2
−0.1
0
K
0
20
40
−0.05
0
0.05
L
0
20
40
−0.2
0
0.2
Q
0
20
40
−1
−0.5
0
N
0
20
40
−2
0
2 x 10
−3
π
0
20
40
−5
0
5 x 10
−3
i
FA
SDGE
2

Figure 3: Responses to a Capital Quality Shock with Credit Policy
0
20
40
−0.04
−0.02
0
s
 
 
0
20
40
−5
0
5
x 10
−3
R
0
20
40
−0.02
0
0.02
Rk−R
0
20
40
−0.1
0
0.1
Y
0
20
40
−0.04
−0.02
0
C
0
20
40
−0.5
0
0.5
I
0
20
40
−0.2
−0.1
0
K
0
20
40
−0.05
0
0.05
L
0
20
40
−0.2
0
0.2
Q
0
20
40
−1
−0.5
0
N
0
20
40
−2
0
2
x 10
−3
π
0
20
40
−5
0
5
x 10
−3
i
0
20
40
0
0.2
0.4
ψ
CP
CP ν=500
CP ν=0
3

Figure 4: One year consumption equivalent welfare gains from optimal credit policy as a
function of eﬃciency costs tau and steady state markup
0
0.002
0.004
0.006
0.008
0.01
0.012
0
0.02
0.04
0.06
0.08
0.1
0.12
0.14
0.16
τ
Ω
 
 
CP X=15%
CP X=33%
CP X=50%
4

Figure 5: One year consumption equivalent welfare gains from optimal credit policy as a
function of eﬃciency costs tau and steady state markup with high labor supply elasticity
0
0.002
0.004
0.006
0.008
0.01
0.012
0
0.02
0.04
0.06
0.08
0.1
0.12
0.14
0.16
0.18
τ
Ω
 
 
CP X=15%
CP X=33%
CP X=50%
5

Figure 6: Credit vs. premium policy
0
20
40
−0.04
−0.02
0
s
 
 
0
20
40
−5
0
5
x 10
−3
R
0
20
40
−0.02
0
0.02
Rk−R
0
20
40
−0.1
0
0.1
Y
0
20
40
−0.04
−0.02
0
C
0
20
40
−0.5
0
0.5
I
0
20
40
−0.2
−0.1
0
K
0
20
40
−0.05
0
0.05
L
0
20
40
−0.2
0
0.2
Q
0
20
40
−1
−0.5
0
N
0
20
40
−2
0
2
x 10
−3
π
0
20
40
−5
0
5
x 10
−3
i
Premium policy
Credit policy
6