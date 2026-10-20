Chapter 2
A CLASSICAL MONETARY MODEL
This chapter presents a simple model of a classical monetary economy,
featuring perfect competition and fully flexible prices in all markets.
As stressed below, many of the model’s predictions are at odds with
the evidence reviewed in chapter 1. That notwithstanding, the analysis
of the classical economy provides a benchmark that will be useful in
subsequentchapterswhensomeofitsstrongassumptionsarerelaxed.It
alsoallowsfortheintroductionofsomenotation,aswellasassumptions
onpreferencesandtechnologythatareusedthroughoutthebook.
Following much of the recent literature, the baseline classical model
developed here attaches a very limited role to money. Thus, in the first
foursectionsofthischapter,theonlyexplicitroleplayedbymoneyisto
serve as a unit of account. In that case, and as shown below, whenever
monetarypolicyisspecifiedintermsofaninterestraterule,noreference
whatsoever needs to be made to the quantity of money in circulation in
order to determine the economy’s equilibrium. When the specification
ofmonetary policyinvolves themoney supply,a“conventional” money
demand equation is postulated in order to close the model, without
taking a stand on its microfoundations. In section 2.5, an explicit role
for money is introduced, beyond that of serving as a unit of account.
In particular, a version of the classical monetary model is analyzed in
which real balances are assumed to generate utility to households, and
the implications for monetary policy of alternative assumptions on the
propertiesofthatutilityfunctionareexplored.
Independently of how money is introduced, the proposed framework
assumes a representative household solving a dynamic optimization
problem. That problem and the associated optimality conditions are
described in section 2.1. Section 2.2 introduces the representative firm’s
technologyanddeterminesitsoptimalbehaviorundertheassumptionof
price and wage taking. Section 2.3 characterizes the equilibrium, and
shows how real variables are uniquely determined, independently of
monetarypolicy.Section2.4discussesthedeterminationofthepricelevel
and other nominal variables under alternative monetary policy rules.
Finally, section 2.5 analyzes a version of the model with money in the
utilityfunction,anddiscussestheextenttowhichtheconclusionsdrawn
fromtheearlieranalysisneedtobemodifiedunderthatassumption.

18 CHAPTER2
2.1 HOUSEHOLDS
The economy is assumed to be inhabited by a large number of identical
households. The representative household seeks to maximize the objec-
tivefunction:
(cid:1)∞
E βtU(C,N;Z) (1)
0 t t t
t=0
where C is the quantity consumed of the single good available in
t
the economy, N denotes hours of work or employment, and Z is an
t t
exogenouspreferenceshifter.1Parameterβ∈(0,1)isthediscountfactor.
E{·}istheexpectationaloperator,conditionaloninformationattimet.
t
The period utility function, U(C,N;Z), is assumed to be continu-
t t t
ous and twice differentiable. Letting U ≡U(C,N;Z), it is assumed
t t t t
thatU c,t ≡∂ ∂ U Ct t >0,U cc,t ≡∂ ∂ 2 C U t 2 t ≤0,U n,t ≡ ∂ ∂U N t t ≤0,andU nn,t ≡∂ ∂ 2 N U t 2 t ≤0.In
words,themarginalutilityofconsumptionU c,t isassumedtobepositive
and nonincreasing, while the marginal disutility of labor, −U n,t , is posi-
tiveandnondecreasing.Inaddition,itisassumedthatU cz,t ≡ ∂C ∂2
t
U ∂Z t
t
>0,
thatis,anincreasein Z raisesthemarginalutilityofconsumption.
t
Maximizationof(1)issubjecttoasequenceofflowbudgetconstraints
givenby
P t C t +Q t B t ≤ B t−1 +W t N t +D t (2)
fort =0,1,2, ... P isthepriceoftheconsumptiongood,W denotesthe
t t
nominal wage (per hour or per worker, depending on the interpretation
of N), and B represents the quantity of one-period nominally riskless
t t
discount bonds purchased in period t, and maturing in period t + 1.
Each bond pays one unit of money at maturity, and its price is Q. In
t
order to keep the notation simple, the set of tradable assets is restricted
to that one-period nominally riskless debt. Given the assumption of
a representative household, this has no consequences for equilibrium
outcomes, since no assets would be traded in equilibrium anyway. D
t
represents dividends, accruing to households in their condition of firms’
owners. When solving the problem above, the household is assumed to
1 Note that Nt can be interpreted as the number of household members who are
employed,assuminga“large”householdandignoringintegerconstraints.Inmuchofwhat
followsIusetheterm“employment”interchangeablyas“numberofindividualsemployed”
or“numberofworkhoursemployed.”

ACLASSICALMONETARYMODEL 19
take as given the price of goods and bonds, as well as the wage and
dividends.
In addition to (2), it is assumed that the household is subject to a
solvencyconstraintthatpreventsitfromengaginginPonzi-typeschemes.
Thefollowingconstraintisassumed
(cid:2) (cid:3)
B
lim E t (cid:3) t,T T ≥0 (3)
T→∞ P
T
forallt,where(cid:3)
t,T
≡βT−tU
c,T
/U
c,t
isthestochasticdiscountfactor.2
The optimality conditions implied by the maximization of (1) subject
to(2)aregivenby
− U n,t = W t (4)
U c,t P t
(cid:2) (cid:3)
Q =βE U c,t+1 P t (5)
t t
U c,t P t+1
aswellasthetransversalitycondition
(cid:2) (cid:3)
B
lim E t (cid:3) t,T T =0 (6)
T→∞ P
T
fort =0,1,2, ....
The previous optimality conditions can be derived using a simple
variational argument. Consider first the impact on utility of a small
departure,inperiodt,fromthehousehold’soptimalplan.Thatdeparture
consists of an increase in consumption dC and an increase in employ-
t
ment dN, while keeping the remaining variables unchanged (including
t
consumption and employment in other periods). If the household is
following an optimal plan to begin with, it should not be possible to
raise utility by departing from that plan, without violating the budget
constraint.Formally,itmustbethecasethat
U c,t dC t +U n,t dN t =0
2SeeWoodford(2003;chap.2)foraderivationof(3)undertheassumptionofcomplete
markets,astheconstraintthatguaranteesthatdebtcanberepaidatanypointintimeby
sellingclaimstofutureincome.

20 CHAPTER2
foranypair(dC,dN)satisfying
t t
PdC = WdN
t t t t
for otherwise it would be possible to raise utility by increasing (or
decreasing) consumption and employment, thus contradicting the as-
sumption that the household is on an optimal plan. Note that the
optimalitycondition(4)isobtainedbycombiningbothequations.
Similarly, consider the impact on expected utility as of time t of
a reallocation of consumption between periods t and t + 1, while
keepingconsumptioninanyotherperiodandemploymentinallperiods
unchanged.Ifthehouseholdisoptimizingitmustbethecasethat
U c,t dC t +βE t {U c,t+1 dC t+1 }=0
foranypair(dC t ,dC t+1 )satisfying
P
P t+1 dC t+1 =− t dC t
Q
t
wherethelatterequationdeterminestheincreaseinconsumptionexpen-
ditures in period t +1 made possible by the additional savings −PdC
t t
allocatedintoone-periodbonds.Combiningthetwopreviousequations
yieldstheintertemporaloptimalitycondition(5).
Finally,transversalitycondition(6)isalsoarequirementofanoptimal
plan: It can be shown that if (3) were to hold with strict inequality, it
would be feasible for the household to increase its current consumption
by a discrete amount without the need to reduce it in the future,
whichwouldbeinconsistentwithoptimality,aslongasutilityisstrictly
increasinginconsumption(asassumedhere).3
Inmuchofwhatfollows,itisassumedthattheperiodutilitytakesthe
form
(cid:8) (cid:9)
 C t 1−σ−1 − N t 1+ϕ Z forσ (cid:7)=1
1−σ 1+ϕ t
U(C,N;Z)= (cid:8) (cid:9)
t t t 
logC − N t
1+ϕ
Z forσ =1
t 1+ϕ t
where σ ≥ 0 and ϕ ≥ 0 determine, respectively, the curvature of
the utility of consumption and the disutility of labor. The analysis is
3 Theassumptions ofarepresentative household andazeronetsupplyofone-period
debt, guarantee that (6) is always satisfied in equilibrium, since Bt =0 for all t. That
observationallowsustoignorethatconditioninmuchofwhatfollows.

ACLASSICALMONETARYMODEL 21
considerably simplified by two properties of the above utility function:
(i) separability, that is, U cn,t = 0, and (ii) the implied constancy of the
elasticities for the marginal utility of consumption and for the marginal
disutility of labor, which leads to simple log-linearized approximations
to the equilibrium conditions, as shown below. Furthermore, the way
thepreferenceshifter Z enterstheutilityfunctionimpliesthatitmaybe
t
interpreted as a shock to the effective discount factor (which becomes
Zβt,fort =0,1,2, ...),whoseeffectwillberestrictedtointertemporal
t
choices (through its influence onU c,t+k /U c,t , the intertemporal marginal
rate of substitution), but with no impact on intratemporal ones (since it
doesnotaffectU n,t /U c,t ,theintratemporalmarginalrateofsubstitution).
Inaddition,itisassumedthatz ≡logZ followsanexogenous AR(1)
t t
process
z t =ρ z z t−1 +ε t z
whereρ ∈[0,1].
z
Theconsumer’soptimalityconditions(4)and(5)thusbecome
W
t =C σ N ϕ (7)
P t t
t
(cid:10)(cid:11) (cid:12) (cid:11) (cid:12)(cid:11) (cid:12)(cid:13)
−σ
Q =βE C t+1 Z t+1 P t (8)
t t
C t Z t P t+1
Note, for future reference, that equation (7) can be rewritten in log-
linearformas
w − p =σc +ϕn (9)
t t t t
where lowercase letters denote the (natural) logs of the corresponding
variable(e.g.,w ≡logW).Thepreviousconditioncanbeinterpretedas
t t
a competitive labor supply schedule, determining the quantity of labor
supplied as a function of the real wage, given the marginal utility of
consumption(whichisafunctionofconsumptiononly,undertheabove
assumption on utility). Parameter ϕ is the inverse (Frisch) labor supply
elasticity.Notethatthepositionofthelaborsupplyscheduleisinvariant
toshockstothepreferenceshifterz.
t
As shown in appendix 2.1, a log-linear approximation of (8) around
a steady state with constant rates of inflation and consumption growth
yields
1 1
c t = E t {c t+1 }− σ (i t −E t {π t+1 }−ρ)+ σ (1−ρ z )z t (10)

22 CHAPTER2
where i t ≡ −logQ t , ρ ≡ −logβ and π t+1 ≡ p t+1 − p t is the rate of
inflationbetweent andt+1(havingdefined p ≡logP ).Noticethati
t t t
corresponds to the log of the gross bond yield; henceforth, i is referred
t
toasthenominalinterestrate.4 Analogously,ρ canbeinterpretedasthe
household’sdiscountrate.5
Whiletheaboveframeworkdoesnotexplicitlyintroducemoneyasan
assetthathouseholdsmayhold(norprovidesamotiveforholdingit),in
somecasesitwillbeconvenient topostulateademand forrealbalances
withalog-linearformgivenby(uptoanadditiveconstant)
m − p =c −ηi (11)
t t t t
where η≥0 denotes the interest semielasticity of money demand. A
money demand equation similar to (11) can be derived under a variety
ofassumptions.Forinstance,insection2.5itisderivedasanoptimality
conditionforthehouseholdwhenrealmoneybalancesyieldutility.
2.2 FIRMS
Alargenumberofidenticalfirmsareassumedtooperateintheeconomy,
producing a homogeneous consumption good. The representative firm’s
technologyisdescribedbytheproductionfunction
Y = AN1−α (12)
t t t
where A representstheleveloftechnology,anda ≡logA evolvesover
t t t
timeaccordingtoanexogenous AR(1)process
a t =ρ a a t−1 +ε t a
whereρ ∈[0,1].
a
Eachperiodthefirmmaximizesprofits
PY −WN (13)
t t t t
subjectto(12),takingthepriceandwageasgiven.
4ThegrossyieldI tontheone-periodbondisgivenbyI
t
≡1/Qt.Thenominalinterest
rateisdefinedhereasit ≡logI t.Thus,it isamonotonicfunctionsofthenetyieldI t −1,
andapproximatelyequaltothelatterforvaluesclosetozero.
5Notethatρ≡−logβ(cid:8)β−1−1,whichistheusualdefinitionofthediscountrate.

ACLASSICALMONETARYMODEL 23
Maximizationof(13)subjectto(12)yieldstheoptimalitycondition
W
t =(1−α)AN −α (14)
P t t
t
that is, the firm hires labor up to the point where its marginal product
equals the real wage. Equivalently, the marginal cost Wt must be
(1−α)AtN
t
−α
equatedtotheprice P.
t
Inlog-linearterms,
w − p =a −αn +log(1−α) (15)
t t t t
which can be interpreted as a labor demand schedule, mapping the real
wageintothequantityoflabordemanded,giventheleveloftechnology.
2.3 EQUILIBRIUM
The baseline model abstracts from sources of goods demand other than
consumption (like investment, government purchases, or net exports).
Accordingly,thegoodsmarketclearingconditionisgivenby
y =c (16)
t t
thatis,alloutputmustbeconsumed.
By combining the optimality conditions of households and firms with
(16)andthelog-linearaggregateproductionrelationship
y =a +(1−α)n (17)
t t t
onecandeterminetheequilibriumlevelsofemploymentandoutput:
n =ψ a +ψ (18)
t na t n
y =ψ a +ψ (19)
t ya t y
where ψ ≡ 1−σ , ψ ≡ log(1−α) , ψ ≡ 1+ϕ , and ψ ≡
na σ(1−α)+ϕ+α n σ(1−α)+ϕ+α ya σ(1−α)+ϕ+α y
(1−α)ψ .
n
Furthermore, given the equilibrium process for output, (10) can be
usedtodeterminetheimpliedrealinterestrate,r t ≡i t −E t {π t+1 },as
r t =ρ+(1−ρ z )z t +σE t {(cid:12)y t+1 }
=ρ+(1−ρ )z −σ(1−ρ )ψ a (20)
z t a ya t

24 CHAPTER2
Finally,theequilibriumrealwage,ω ≡w − p,isgivenby
t t t
ω =a −αn +log(1−α)
t t t
=ψ ωa a t +ψ ω (21)
whereψ
ωa
≡
σ(1−
σ
α
+
)+
ϕ
ϕ+α
andψ
ω
≡(σ(1
σ
−
(
α
1−
)+
α
ϕ
)+
)l
ϕ
og
+
(
α
1−α).
Noticethattheequilibriumlevelsofemployment,output,andthereal
interest rate are determined independently of monetary policy. In other
words, monetary policy is neutral with respect to those real variables.
In the simple model, output, employment, and the real wage fluctuate
in response to variations in technology, though they are invariant to
preference shocks. In particular, output always rises in the face of a
productivityincrease,withthesizeoftheincreasebeinggivenbyψ >0.
ya
The same is true for the real wage. On the other hand, the sign of the
employment is ambiguous, depending on whether σ (which measures
the strength of the income effect on labor supply) is larger or smaller
than one. When σ < 1, the substitution effect on labor supply resulting
fromahigherrealwagedominatesthenegativeeffectcausedbyasmaller
marginal utility of consumption, leading to an increase in employment.
The converse is true whenever σ > 1. When the utility of consumption
is logarithmic (σ=1), employment remains unchanged in the face of
technologyvariations,forsubstitutionandincomeeffectsexactlycancel
one another. Finally, and under the assumptions on the processes
followed by a and z, the real interest rate goes down in response
t t
to a positive technology shock, but rises in the wake of an increase
inz.
t
What about nominal variables, like inflation or the nominal interest
rate? Not surprisingly, and in contrast with real variables, their equilib-
riumvaluescannotbedeterminedindependentlyofmonetarypolicy.To
illustratehownominalvariablesareinfluencedbythewaymonetarypol-
icy is conducted, their equilibrium behavior under alternative monetary
policyruleswillbeconsiderednext.
2.4 MONETARYPOLICY ANDPRICE LEVEL DETERMINATION
Let us start by examining the implications of some interest rate
rules. Rules that involve monetary aggregates will be introduced later.
ThroughoutuseismadeoftheFisherianequation
i t = E t {π t+1 }+r t (22)

ACLASSICALMONETARYMODEL 25
which implies that the nominal rate adjusts one-for-one with expected
inflation, given a real interest rate that is determined exclusively by real
factors,asin(20).
Equation (20) implies that in the steady state without growth r = ρ,
thatis,therealinterestratecorrespondstothehousehold’sdiscountrate.
Thus it follows from (22) that in the perfect foresight steady state the
nominalrateandinflationwillberelatedby
i =ρ+π
In what follows the analysis is restricted to nonexplosive equilibrium
paths for inflation and the nominal interest rate, that is, equilibrium
paths that remain within a bounded neighborhood of the steady state,
forsufficientlysmallfluctuationsintheexogenousdrivingforces.
2.4.1 AnExogenousPathfortheNominalInterestRate
Let us first consider the case of a monetary policy that implies an
exogenous path for the nominal interest rate. For concreteness, let us
assumetherule
i =i +v
t t
where{v }isassumedtofollowanexogenous AR(1)process
t
v t =ρ v v t−1 +ε t v (23)
Henceforth, the stochastic component {v } in the policy rule under
t
consideration is referred to as a monetary policy shock. It should be
interpreted as a random, transitory deviation from the “usual” conduct
of monetary policy as anticipated by the public, due to a change in the
policymaker’spreferences,aresponsetoanunusualunanticipatedevent,
or, simply, an error in the implementation of monetary policy.6 Even if
one views those shocks as empirically unimportant, the analysis of their
effectshelpsuncoverhowmonetarypolicyinterventionsaretransmitted
to the economy under different sets of assumptions about the structure
ofthelatter.
A particular case of this rule corresponds to a constant interest rate,
thatis,i =i forallt.Notethatπ =i−ρ isthesteadystateinflation(or
t
theimplicitlong-runinflationtarget)associatedwiththeruleabove.
6 Notethatintheparticularcaseoftherule(23)consideredhere,the“usual”policy
consistsinkeepingtheinterestrateconstantatleveli.

26 CHAPTER2
Using(22),write
E t {π t+1 }=i t −r t
=π +v −(cid:14)r
t t
where(cid:14)r ≡r −ρisdeterminedindependentlyofthemonetarypolicyrule,
t t
asshownabove.
Note that expected inflation is pinned down uniquely by the previous
equation, since it can be written as a function of exogenous variables,
using(20).Butactualinflationisnot.Becausethereisnoothercondition
thatcanbeusedtodetermineinflation,itfollowsthatanyinflationpath
thatsatisfies
π
t
=π +v
t−1
−(cid:14)r
t−1
+ξ
t
isconsistentwithequilibrium,where ξ isashock,possiblyunrelatedto
t
economic fundamentals, satisfying E t−1 {ξ t } = 0 for all t. Equivalently,
thepricelevelisgivenby
p t =π + p t−1 +v t−1 −(cid:14)r t−1 +ξ t
Shocks such as ξ are often referred to in the literature as sunspot
t
shocks.Anequilibriuminwhichsuchnonfundamentalfactorsmaycause
fluctuations in one or more variables is referred to as an indeterminate
equilibrium. The example above shows how an exogenous nominal
interestrateleadstopricelevelindeterminacy.
Notice that the equilibrium nominal wage is equal, in logs, to the
real wage, which is determined by (21), plus the price level, which is
indeterminate.Thus,thenominalwageinheritstheindeterminacyofthe
pricelevel.
2.4.2 ASimpleInterestRateRule
Suppose that the central bank adjusts the nominal interest rate in
response to deviations of inflation from a target π, according to the
interestraterule
i
t
=ρ+π +φ π(π
t
−π)+v
t
whereφ
π
≥0isacoefficientdeterminingthestrengthoftheendogenous
response of monetary policy and {v } is an exogenous monetary policy
t
shifter,asdefinedabove.

ACLASSICALMONETARYMODEL 27
CombiningthepreviousrulewiththeFisherianequation(22)yields
φ π π(cid:14) t = E t {π(cid:14) t+1 }+(cid:14)r t −v t (24)
whereπ(cid:14) ≡π −π.Adistinctionismadebetweentwocases,dependingon
t t
whethertheinflationcoefficientintheaboverule,φ π,islargerorsmaller
thanone.
Ifφ π > 1,thepreviousdifferenceequationhasonlyonenonexplosive
solution. That solution can be obtained by solving (24) forward, which
yields
(cid:1)∞
π(cid:14) t = φ π −(k+1)E t {(cid:14)r t+k −v t+k } (25)
k=0
Thepreviousequationfullydeterminesinflation(and,hence,theprice
level)asafunctionofthepathoftherealinterestrate,whichinturnisa
functionofexogenousrealforces,asshownin(20).Inparticular,under
theassumeddrivingprocessesfortechnologyandpreferenceparameters,
inflationcanbewrittenas
σ(1−ρ )ψ 1−ρ 1
π =π − a ya a + z z − v
t φ −ρ t φ −ρ t φ −ρ t
π a π z π v
Note that a central bank following a rule of the form considered
here can influence the degree of inflation volatility through its choice
of φ π. The larger that coefficient is the smaller will be the impact of
realshocksoninflation.Monetarypolicyshocks,v ,areseentogenerate
t
“unnecessary”fluctuationsininflation.
Givenequilibriumpathforinflation,thepriceandnominalwagelevels
areuniquelydeterminedbytheidentities p t = p t−1 +π t andw t =ω t +p t ,
withtherealwageω givenby(21).
t
Note that an exogenous tightening of monetary policy (i.e., a positive
realization of v t ) reduces inflation and, if persistent (i.e., ρ v > 0), the
nominal interest rate as well, since
∂
∂
ε
itv = −
φ
ρ
−
v
ρ
. Assuming a money
t π v
demand function of the form (11) the (contemporaneous) response of
the money supply to the same shock is given by ∂
∂
m εvt =
φ
ηρ v
−
−
ρ
1, which can
bepositiveornegative,dependingonthevaluesofηt and π ρ v. v Thus,under
theassumedinterestraterule,aliquidityeffectwillbepresentinresponse
to a monetary policy shock if and only if ηρ v > 1, for in that case the
nominalratewilldeclineandthemoneysupplywillincreaseinresponse
totheshock.Yet,andincontrastwiththeevidenceshowninchapter1,
thepreviousresponseswillbeaccompaniedbyadecreaseinprices(given
∂
∂
π εvt =−
φ −
1
ρ
),andnoeffectonoutputoranyotherrealvariable.
t π v

28 CHAPTER2
On the other hand, if φ π <1, the forward solution (25) does not
converge.Instead,thestationarysolutionto(24)takestheform
π t =(1−φ π)π +φ π π t−1 −(cid:14)r t−1 +v t−1 +ξ t (26)
where{ξ }is,again,anarbitrarysequenceofshocks,relatedorunrelated
t
tofundamentals,satisfying E t−1 {ξ t }=0forallt.
Accordingly, any process {π }satisfying (26) is consistent with equi-
t
librium, while remaining in a neighborhood of the steady state (for
sufficiently small shocks). So, as in the case of an exogenous nominal
rate, the price level (and, hence, inflation) are not determined uniquely
when the interest rate rule implies a weak response of the nominal rate
todeviationsofinflationfromtarget.7
More specifically, the condition for a determinate price level, φ π > 1,
requires that the central bank adjusts nominal interest rates more than
one-for-one inresponsetoany change ininflation,aproperty known as
the Taylor principle. The previous result can be viewed as a particular
instanceoftheneedtosatisfytheTaylorprincipleinorderforaninterest
rateruletobringaboutadeterminateequilibrium.
2.4.3 AnExogenousPathfortheMoneySupply
The analysis above assumed that monetary policy can be described
by an interest rate rule. In that case, money supply does not play an
independent role in determining the equilibrium. Instead, it just adjusts
endogenously, in order to match money demand, given the path of
output,thepricelevel,andtheinterestrate,asimpliedbyanequationof
theform
m = p +y −ηi
t t t t
which corresponds to (11), after imposing the goods market clearing
condition.
Suppose instead that the central bank sets an exogenous path for the
money supply {m}. Using (11) (with c = y) to eliminate the nominal
t t t
7Withnolossofgeneralityonecanwrite
ξ =τ εa+τ εz+τ εv+ξ∗
t a t z t v t t
whereτ
a
,τ z,andτ vcantakeanyvalue(i.e.,areindeterminate)andξ
t
∗isa“puresunspot,”
i.e., a martingale-difference process orthogonal to all fundamental shocks. Thus, the
responseofinflation(and,asresult,ofanynominalvariable)toanyshockisindeterminate.

ACLASSICALMONETARYMODEL 29
interest rate in (22), the following difference equation for the price level
canbederived
(cid:11) (cid:12) (cid:11) (cid:12)
η 1
p t = 1+η E t {p t+1 }+ 1+η m t +u t (27)
whereu ≡(1+η)−1(ηr −y)evolvesindependentlyof{m},asshownin
t t t t
(19)and(20).
Assumingη>0andsolvingforwardobtains
(cid:11) (cid:12)
1 (cid:1)∞ η k
p t = 1+η 1+η E t {m t+k }+u t (28)
k=0
(cid:8) (cid:9)
(cid:15)
where u t ≡ ∞ k=0 1+ η η k E t {u t+k } is, again, independent of monetary
policy.
Thus, when the monetary policy rule takes the form of an exogenous
path for the money supply, the equilibrium price level is always deter-
mineduniquely,asshownin(28).
It is often convenient to have an expression for the equilibrium price
levelintermsoftheexpectedfuturegrowthrateofmoney:8
(cid:11) (cid:12)
(cid:1)∞ η k
p t =m t + 1+η E t {(cid:12)m t+k }+u t (29)
k=1
Given(29),asdeterminedabove,moneydemandequation(11)canbe
usedtosolveforthenominalinterestrate
1
i = (y −(m − p))
t η t t t
(cid:11) (cid:12)
1 (cid:1)∞ η k
= η 1+η E t {(cid:12)m t+k }+u t
k=1
whereu ≡η−1(u +y)isindependentofmonetarypolicy.
t t t
8Toderive(29),rewrite(27)asadifferenceequationintermsof(cid:1)pt ≡ pt −mt,i.e.,
(cid:2) (cid:3) (cid:2) (cid:3)
η η
(cid:1)pt =
1+η
Et {(cid:1)pt+1 }+
1+η
Et {(cid:12)mt+1 }+ut
whichcanbesolvedforwardtoyield(29).

30 CHAPTER2
Forconcreteness,considerthecaseinwhichmoneygrowthfollowsan
AR(1)process
(cid:12)m
t
=ρ
m
(cid:12)m
t−1
+ε
t
m
For simplicity, assume the absence of real shocks, thus implying a
constant output and a constant real rate. Without loss of generality, set
r = y =0forallt.Then,itfollowsfrom(29)that
t t
ηρ
p =m + m (cid:12)m
t t 1+η(1−ρ ) t
m
Hence, in response to an exogenous monetary policy shock, and as
longasρ >0(theempiricallyrelevantcase,giventheobservedpositive
m
autocorrelation of money growth), the price level should respond more
thanone-for-onewiththeincreaseinthemoneysupply,apredictionthat
contrastsstarklywiththesluggishresponseofthepricelevelobservedin
empiricalestimatesoftheeffectsofmonetarypolicyshocksasdiscussed
inchapter1.
Thenominalinterestrateisinturngivenby
ρ
i = m (cid:12)m
t 1+η(1−ρ ) t
m
thatis,inresponsetoanexpansionofthemoneysupply,andaslongas
ρ > 0, the nominal interest rate is predicted to go up. In other words,
m
the model implies the absence of a liquidity effect, in contrast with the
evidencediscussedinchapter1.
2.4.4 OptimalMonetaryPolicy
The analysis of the baseline classical economy above has shown that
while real variables are independent of monetary policy, the latter can
have important implications for the behavior of nominal variables and,
in particular, of prices. Yet, and given that households’ utility is a
function of consumption and employment only—two real variables that
are invariant to the way monetary policy is conducted—it follows that
no policy rule is better than any other. Thus, in the classical model
above, a policy that generates large fluctuations in inflation and other
nominal variables (perhaps as a consequence of following a policy rule
that does not guarantee a unique equilibrium for those variables) is
no less desirable from a welfare perspective than one that succeeds in
stabilizingpricesinthefaceofthesameshocks.
The previous result, which is clearly extreme and empirically unap-
pealing, can be overcome once versions of the classical monetary model

ACLASSICALMONETARYMODEL 31
are considered in which a motive to keep part of households’ wealth in
theformofmonetaryassetsisintroducedexplicitly.Section2.5discusses
onesuchmodelinwhichrealbalancesareassumedtoyieldutility.
Theoverallassessmentoftheclassicalmonetarymodelasaframework
to understand the observed behavior of nominal and real variables and
their connection to monetary policy cannot be a favorable one. The
model cannot explain the observed real effects of monetary policy on
real variables. Its predictions regarding the response of the price level,
the nominal rate, and the money supply to exogenous monetary policy
shocks are also in conflict with the empirical evidence. Those empirical
failures are the main motivation behind the introduction of nominal
frictionsinthemodel,ataskthatwillbeundertakeninchapter3.
2.5 MONEY IN THEUTILITY FUNCTION
In the model developed in the previous sections, and in much of the
recent monetary literature, the only role played by money is to serve
as a numéraire, that is, a unit of account in which prices, wages, and
securitiespayoffsarestated.Economieswiththatcharacteristicareoften
referred to as cashless economies. Above, a simple log-linear money
demand function was occasionally postulated, but it was done in an
ad hoc manner and without an explicit justification for why agents
would want to hold an asset that is dominated in return by bonds
while having identical risk properties. Even though in the analysis of
subsequentchapterstheassumptionofacashlesseconomyismaintained,
it is useful to understand how the basic framework can incorporate a
role for money other than that of a unit of account and, in particular,
how it can generate a demand for money. The discussion in this section
focuses on models that achieve the previous objective by assuming that
realmoneyholdingsareanargumentoftheutilityfunction.9 Thereader
can find references to alternative “microfoundations” in the section on
theliteratureattheendofthechapter.
The assumption that real money holdings (or real balances), M/P,
t t
enter the utility function is a convenient way of formalizing the notion
that, in contrast with other assets, money provides a “transactions
service” that households value. The service that any nominal amount
of money can yield is likely to depend on its purchasing power, thus
explaining why it is the real value of monetary holdings that enters the
utilityfunction.
9 Readersnotinterestedinthisextensionmayskipthissectionandproceedtosection
2.6withoutanylossofcontinuity.

32 CHAPTER2
The introduction of money in the utility function requires modifying
the representative household’s problem in two ways. First, preferences
arenowgivenby
(cid:11) (cid:12)
(cid:1)∞
M
E βtU C, t,N;Z (30)
0 t t t
P
t=0 t
whereM denotesholdingsofmoneyinperiodt.Itisassumedthatperiod
t
utilityisincreasingandconcaveinrealbalances M/P.Second,theflow
t t
budget constraint incorporates monetary holdings explicitly, taking the
form
P t C t +Q t B t +M t ≤ B t−1 +M t−1 +W t N t +D t (31)
Letting A ≡B + M denote total financial wealth at the beginning
t t t
of period t (i.e., after bonds mature, but before consumption and
portfoliodecisionsaremade),thepreviousflowbudgetconstraintcanbe
rewrittenas
P t C t +Q t A t +(1−Q t )M t ≤A t−1 +W t N t +D t (32)
withthesolvencyconstraintnowtakingtheform
(cid:2) (cid:3)
A
lim E t (cid:3) t,T T ≥0
T→∞ P
T
forallt.
The previous representation of the budget constraint can be thought
of as equivalent to that of an economy in which all financial assets
(represented by A ) yield a gross nominal return Q−1 (= exp{i }), and
t t t
where agents can “purchase” the utility-yielding services of money
balancesataunitprice1−Q =1−exp{−i }(cid:8)i .Thus,theimplicitprice
t t t
for the services of money roughly corresponds to the nominal interest
rate,thatis,theopportunitycostofholdingfinancialwealthintermsof
monetaryassets,insteadofinterest-bearingbonds.
Considernextthehousehold’sproblem,whichconsistsofmaximizing
(30) subject to (32). Two of the implied optimality conditions are the
same as those obtained for the cashless model, namely, (4) and (5),
with the marginal utility terms being now defined over (and evaluated
at) (C, Mt,N;Z). In addition to (4) and (5), there is an additional
t Pt t t
optimalityconditiongivenby
U m,t =1−Q
t
U c,t
=1−exp{−i } (33)
t
whereU m,t ≡ ∂(M ∂U t / t Pt) >0.

ACLASSICALMONETARYMODEL 33
Again,inordertoderivethatoptimalityconditionasimplevariational
argument can be used. Suppose that a household following an optimal
plan considers a deviation from the latter which consists in adjusting
consumption and money holdings in period t by amounts dC and dM,
t t
respectively,whilekeepingallothervariablesunchangedattheiroptimal
values.Optimalityoftheinitialplanrequiresthatutilitycannotriseasa
resultofthedeviation,whichinturnrequires
1
U c,t dC t +U m,t dM t =0
P
t
foranypair(dC,dM)satisfying
t t
PdC +(1−Q)dM =0
t t t t
which guarantees that the budget constraint is met without the need to
adjust any other variables. Combining the previous two equations and
usingthedefinitionofthenominalratei ≡−logQ yieldstheoptimality
t t
condition(33).
In order to be able to make any statements about the consequences
of having money in the utility function, more specific assumptions are
needed about the way money balances interact with other variables in
yielding utility. In particular, whether the utility function is separable
or not in real balances determines the extent to which the neutrality
properties derived above for the cashless economy carry over to the
economy with money in the utility function. That point is illustrated
by considering, in turn, two example economies with separable and
nonseparableutility.
2.5.1 AnExamplewithSeparableUtility
Specifically, the household’s utility function is assumed to have the
functionalform
(cid:11) (cid:12) (cid:16) (cid:17)
M C1−σ −1 (M/P)1−ν −1 N1+ϕ
U C, t,N;Z = t + t t − t Z
t P t t 1−σ 1−ν 1+ϕ t
t
Notethat,giventheassumedseparability,neitherU c,t norU n,t depend
onthelevelofrealbalances.Asaresult,(7)and(8),aswellastheirlog-
linearcounterparts,(9)and(10),continuetoholdunchanged.Itfollows
that the equilibrium values for output, employment, the real rate, and
the real wage can be determined by following the same steps as in the
previoussection,withoutanyreferencetomonetarypolicy.

34 CHAPTER2
The introduction of money in the utility function allows a money
demand equation to be derived from the household’s optimal behavior.
Usingtheabovespecificationofutility,theoptimalitycondition(33)can
berewrittenas
M t =C σ/ν (1−exp{−i }) −1/ν (34)
P t t
t
which can be naturally interpreted as a demand for real balances. The
latter is increasing in consumption and inversely related to the nominal
interestrate,asinconventionalspecifications.
Using the first-order Taylor expansion log(1−exp{−i }) (cid:8) const.+
t
1 i ,(34)canberewritteninapproximatelog-linearform(uptoan
exp{i}−1 t
uninterestingconstant)as
σ
m − p = c −ηi (35)
t t ν t t
where η≡ 1 (cid:8) 1 is the implied interest semielasticity of money
ν(exp{i}−1) νi
demand.
Theparticularcaseofν =σ isanappealingoneinthepresentcontext,
because it implies a unit elasticity with respect to consumption. Under
that assumption, a conventional log-linear demand for real balances is
obtainedas
m − p =c −ηi
t t t t
= y −ηi (36)
t t
where the second equality holds under the assumption (made here) that
alloutputisconsumed.Thepreviousspecificationisoftenmaintainedin
subsequentchapters,withouttheneedtoinvokeitssourceexplicitly.
As in the analysis of the cashless economy, the usefulness of (35),
or (36), is confined to the determination of the equilibrium values
for inflation and other nominal variables whenever the description
of monetary policy involves the quantity of money in circulation.
Otherwise, the only use of the money demand equation is to determine
thequantityofmoneythatthecentralbankwillneedtosupplyinorder
tosupport,inequilibrium,thenominalinterestrateimpliedbythepolicy
rule.
2.5.2 AnExamplewithNonseparableUtility
Letusconsideraneconomywithperiodutilitygivenby
X1−σ −1 N1+ϕ
U(X,N)= t − t
t t 1−σ 1+ϕ

ACLASSICALMONETARYMODEL 35
where X is a composite index of consumption and real balances
t
definedby
(cid:18) (cid:11) M (cid:12) 1−ν (cid:19) 1− 1 v
X ≡ (1−ϑ)C1−ν +ϑ t for ν (cid:7)=1
t t P
t
(cid:11) (cid:12)
ϑ
M
≡C1−ϑ t for ν =1
t P
t
with ν representing the (inverse) elasticity of substitution between con-
sumption and real balances, and ϑ the relative weight of real balances
in utility. Note that, in order to ease the algebra, preference shocks are
ignoredfortheremainderofthissection.
Noticethatthemarginalutilitiesofconsumptionandrealbalancesare
nowgiven,respectively,by
U c,t =(1−ϑ)X t ν−σ C t −ν
(cid:11) (cid:12)
−ν
M
U m,t =ϑX t ν−σ P t
t
whereas the marginal (dis)utility of labor is, as before, given by U n,t =
−N ϕ .Theoptimalityconditionsofthehousehold’sproblem,(4),(5),and
t
(33),cannowbewrittenas
W
t = N ϕ X σ−ν C ν (1−ϑ) −1 (37)
P t t t
t
(cid:10)(cid:11) (cid:12) (cid:11) (cid:12) (cid:11) (cid:12)(cid:13)
−ν ν−σ
Q =βE C t+1 X t+1 P t (38)
t t
C t X t P t+1
(cid:11) (cid:12)
M t =C (1−exp{−i }) −1 ν ϑ 1 ν (39)
P t t 1−ϑ
t
Notice that in the particular case in which the intertemporal and
intratemporalelasticitiesofsubstitutioncoincide(i.e.,ν =σ),optimality
conditions (37) and (38) match exactly those obtained in the case of
separable utility, and thus lead to the same equilibrium implications
derivedforthatcaseanddiscussedinsection2.5.1.
Inthegeneralcase,however,boththelaborsupplyequation(37)and
the Euler equation (38) depend on the level of real balances through

36 CHAPTER2
variable X. The level of real balances depends, in turn, on the nominal
t
interest rate, as implied by (39).10 Those features imply that monetary
policy isnolonger neutral inthecaseof nonseparable utilityconsidered
here.Inparticular,totheextentthatdifferentmonetarypolicyruleshave
different implications for the path of the nominal rate (as will generally
be the case), they will also have different effects on real balances and—
throughthelatter’sinfluenceonthemarginalutilityofconsumption—on
thepositionofthelaborsupplyscheduleand,hence,onemploymentand
output.Thismechanismisanalyzedformallybelow.
Noticethattheimpliedmoneydemandequation(39)canberewritten
inlog-linearform(anduptoanadditiveconstant)asin(36)above
m − p =c −ηi (40)
t t t t
where, as above, η≡ 1 . Thus, the implied interest semielasticity
ν(exp{i}−1)
of money demand η is now proportional to the elasticity of substitution
betweenrealbalancesandconsumptionν−1.
Ontheotherhand,(37)canbewritteninlog-linearformas(uptoan
additiveconstant):
w − p =σc +ϕn +(ν−σ)(c −x)
t t t t t t
For the remainder of this section the analysis is restricted to a
neighborhood of the zero inflation steady state.11 Log-linearizing the
definition of X around that steady state and combining the resulting
t
expressionwith(39),yields
w − p =σc +ϕn +χ(ν−σ)(c −(m − p))
t t t t t t t
=σc +ϕn +ηχ(ν−σ)i
t t t
where χ≡ ϑ1ν(1−β)1−1ν ∈ [0,1), and where the second equality
(1−ϑ) 1ν+ϑ1ν(1−β)1−1ν
makesuseof(40).
Forfuturereference,itisconvenienttorewritethepreviousoptimality
conditionsintermsofthesteadystateratiok ≡ M/P,thatis,theinverse
m C
consumption velocity. Using the money demand equation, evaluated at
(cid:8) (cid:9)
1
the zero inflation steady state, we have k = ϑ ν . Noting that
m (1−β)(1−ϑ)
10Notethatthepresentutilityspecificationguaranteesaunit-elasticmoneydemandwith
respecttoconsumption,independentlyofthevaluesofνandσ.
11Thisislargelyfornotationalsimplicity.Itisstraightforwardtoextendtheanalysisto
aneighborhoodofanonzeroinflationsteadystate.

ACLASSICALMONETARYMODEL 37
χ = km(1−β) ,andusingthedefinitionofηevaluatedatthezeroinflation
1+km(1−β)
steadystate,theoptimalityconditionabovecanberewrittenas
w − p =σc +ϕn +(cid:20)i (41)
t t t t t
where (cid:20)≡ km β(1−σ ν) . Thus, the sign of the effect of the nominal interest
rate on labo 1 r +k s m u (1 p − p β l ) y is determined by the sign of ν −σ. When ν > σ
(implying (cid:20) > 0), the reduction in real balances induced by an increase
inthenominalratebringsdownthemarginalutilityofconsumption(for
any given c ), lowering the quantity of labor supplied at any given real
t
wage. The opposite effect is obtained when ν < σ. Note, however, that
ν (cid:8) 1 is likely to be larger than σ for any plausible values of i, η, and
iη
σ. Thus, the case of U > 0 (and, hence, (cid:20) > 0) appears as the most
cm
plausible one, conditional on the specification of preferences analyzed
here.
In order to reflect the changes implied by nonseparable utility, the
economy’s log-linearized equilibrium conditions need to be modified.
Thus, combining (41) with the labor demand schedule (15) yields the
labormarketclearingcondition
σc +ϕn +(cid:20)i =a −αn +log(1−α) (42)
t t t t t
which can be rewritten, using the goods market clearing condition
(16), the log-linear production relationship (17), and up to an additive
constant,as:
y =ψ a +ψ i (43)
t ya t yi t
whereψ ≡ − (cid:20)(1−α) and,asbefore,ψ ≡ 1+ϕ .
yi σ(1−α)+ϕ+α ya σ(1−α)+ϕ+α
Condition (43) points to a key implication of the nonseparability
property (i.e., (cid:20) (cid:7)= 0): Equilibrium output is no longer invariant to
monetarypolicy,atleasttotheextentthatthelatterimpliesvariationsin
thenominalinterestrate.Inotherwords,monetarypolicyisnotneutral.
As a result, equilibrium condition (43) does not suffice to determine the
equilibrium level of output, in contrast to the economy with separable
utility analyzed above. Note that in the empirically plausible case of
(cid:20) > 0, ψ < 0 implying that output is inversely related to the nominal
yi
interestrate.
In order to assess the extent to which monetary policy may affect the
level of output it is useful to get a sense of the magnitude of the interest
rate multiplier ψ . With that purpose, and in a way consistent with the
yi
baseline calibration that will be introduced in chapter 3, the settings

38 CHAPTER2
σ = 1, ϕ = 5, and α = 1/4 are chosen and taken to be “empirically
plausible.”Usingthedefinitionof(cid:20),andthefactthatν = 1 is“large”
ηi
for any reasonable values of η, it follows that ψ (cid:8) −km, and so the
yi 8
size of the inverse velocity k is a key determinant of the quantitative
m
importance of monetary non-neutralities in the model. The magnitude
ofk ,however,dependscruciallyonthedefinitionofmoneyoneadopts.
m
Thus,andfocusingonpostwarU.S.data,k (cid:8)0.3ifthemonetarybaseis
m
taken to be the relevant measure of money.12 In that case ψ (cid:8) −0.04,
yi
which implies a very small multiplier: A monetary policy intervention
that raised the nominal rate by one percentage point (expressed at an
annualrate)wouldgenerateadecreaseinquarterlyoutputofabout0.01
percent. Using M2 instead as the definition of money, k (cid:8) 3, and
m
hence ψ (cid:8) −0.4. Thus, an analogous monetary policy intervention
yi
would lower output by 0.1 percent. The latter value, while still very
small, appears to be more in line with the estimated output effects of
monetary policy shock found in the literature, at least in terms of order
of magnitude. Yet, even in the latter case, there are other aspects of the
monetarytransmissionmechanismassociatedwiththemodelabovethat
areclearlyatoddswiththeevidence.Theanalysisbelowmakesthispoint
byanalyzingthejointresponseofoutput,inflation,andtheinterestrate
toamonetarypolicyshock.
Combining(40)and(43)(aftersettinga =0forallt,giventhefocus
t
onexogenousshiftstomonetarypolicy),oneobtains
y =(cid:21)(m − p) (44)
t t t
where (cid:21)≡ (cid:20)(1−α) ∈ [0,1) under the empirically plausible
η[σ(1−α)+ϕ+α]+(cid:20)(1−α)
assumption that (cid:20) ≥ 0 (which is maintained for the remainder of the
section).Also,
i =−(1/η)(1−(cid:21))(m − p) (45)
t t t
Thus, in order for an exogenous tightening of monetary policy to
raise the nominal rate, while lowering output and the money supply (as
suggested by the evidence in chapter 1), it must also be associated with
adeclineinrealbalances,thatis,thepricelevelshouldnotdeclinemore
than proportionally to the money supply. But the latter requirement is
inconsistentwiththepredictionsofthemodel,asshownnext,atleastto
theextentthatthepolicytighteningisassociatedwithapersistentdecline
inmoneysupplygrowth,asfoundinthedata.
12ThisistheapproachfollowedinWoodford(2003,chap.2).

ACLASSICALMONETARYMODEL 39
First, note that the corresponding log-linear approximation to (38) is
givenby
1
c t = E t {c t+1 }− σ (i t −E t {π t+1 }−(ν−σ)E t {(c t+1 −x t+1 )−(c t −x t )}−ρ)
1
= E t {c t+1 }− σ (i t −E t {π t+1 }−χ(ν−σ)E t {(cid:12)c t+1 −(cid:12)(m t+1 −p t+1 )}−ρ)
1
= E t {c t+1 }− σ (i t −E t {π t+1 }−(cid:20)E t {(cid:12)i t+1 }−ρ) (46)
where,again,thelastequalitymakesuseof(40).Thus,whenν >σ (and,
hence, (cid:20) > 0) the anticipation of a nominal rate increase (and, hence,
ofadeclineinrealbalances) lowerstheexpected oneperiodaheadlevel
of the marginal utility of consumption (for any expected c t+1 ), which
inducesanincreaseincurrentconsumption(inordertosmoothmarginal
utility over time). Imposing the goods market clearing condition y = c
t t
on (46), yields an equation relating output, to the nominal interest rate
andexpectedinflation:
1
y t = E t {y t+1 }− σ (i t −E t {π t+1 }−(cid:20)E t {(cid:12)i t+1 }−ρ) (47)
Combining the previous equation with (44) and (45) one can obtain
(aftersomealgebraicmanipulation)anexpressionrelatingthepricelevel
tocurrentandexpectedmoneysupplywhichgeneralizes(29)tothecase
ofnonseparableutility:
(cid:11) (cid:12)
η (cid:1)∞ η+(cid:20)(cid:3) k
p t =m t + η+(cid:20)(cid:3) 1−(cid:21)+η+(cid:20)(cid:3) E t {(cid:12)m t+k } (48)
k=1
where (cid:3)≡ η(α+ϕ) ∈ [0,1). Thus, in order for the price
η[σ(1−α)+ϕ+α]+(cid:20)(1−α)
level to decline less than the money supply in response to a tightening
of monetary policy involving a higher nominal rate and lower output,
the initial decline in the money supply would have to be followed by
persistentlyhigherthanaveragemoneygrowth.Thelatterimplicationis
at odds with the empirical evidence, as shown in chapter 1. Note that
the above implication is independent of the details of monetary policy
implementation(i.e.,ofthespecificmonetarypolicyrule).
The model also predicts that the real wage should move countercycli-
callyinresponsetoanexogenousshiftinmonetarypolicy,totheextent
that the latter has an effect on output (i.e., if (cid:20) (cid:7)= 0). The reason is
that the resulting change in employment is a consequence of a shift in

40 CHAPTER2
the labor supply schedule, moving along a stable labor demand. That
prediction is also in conflict with the empirical evidence in Christiano,
Eichenbaum,andEvans(2005),whichpointstoamildlyprocyclicalreal
wageinresponsetoanexogenousmonetarypolicyshock.
The analysis above has revealed important weaknesses regarding the
empirical plausibility of the classical model’s monetary transmission
mechanism. A key concern has to do with the large and rapid price
adjustmentthatfollowsamonetaryshock,withthepricelevelchanging
in the short run more than proportionally to the change in the money
supply. The previous assessment motivates the introduction of nominal
frictionsinthemodelsanalyzedfromthenextchapteronward.
2.5.3 OptimalMonetaryPolicyinaClassicalEconomywithMoneyin
theUtilityFunction
This section derives the form of the optimal monetary policy in the
presenceofmoneyintheutilityfunction.Theproblemofahypothetical
social planner seeking to maximize the utility of the representative
householdispresentedandsolved.
Note that, under the assumptions made above, the economy has no
aggregate intertemporal links: Even though each individual household
canreallocateitsownconsumptionovertimethroughfinancialmarkets,
there are no mechanisms that make this possible for the economy as
a whole. Thus, a benevolent social planner solves a sequence of static
problemsoftheform
(cid:11) (cid:12)
M
maxU C, t,N;Z
t t t
P
t
subjecttotheaggregateresourceconstraint
C = AN1−α
t t t
Theoptimalityconditionsforthatproblemaregivenby
− U n,t =(1−α)AN −α (49)
U c,t t t
U m,t =0 (50)
Condition(49)requiresthatthemarginalrateofsubstitutionbetween
employment and consumption be equated to the marginal product of

ACLASSICALMONETARYMODEL 41
labor.Condition(50)equatesthemarginalutilityofrealbalancestothe
“social” marginal cost of producing real balances, which is implicitly
assumedtobezerointhemodel.
Under what conditions does the equilibrium of the decentralized
economy satisfy efficiency conditions (49) and (50)? First note that
condition (49) is implied by the combined effect of profit maximization
byfirms(seeequation(14),whichequatestherealwagetothemarginal
product of labor) and the optimal labor supply choice by the household
(see equation (4), which equates the real wage to the marginal rate of
substitutionbetweenhoursofworkandconsumption).Hence,(49)will
besatisfiedindependentlyofmonetarypolicy.Ontheotherhand,andas
showninequation(33)above,thehousehold’soptimalchoiceofmoney
balancesrequires
U m,t =1−exp{−i }
t
U c,t
Accordingly, efficiency condition (50) will be satisfied if and only if,
i = 0 for all t. This is the policy prescription known as the Friedman
t
rule.Therationaleforthatpolicyisquiteintuitive:Whilethesocialcost
ofproducingrealbalancesiszero,theprivate(opportunity)costisgiven
bythenominalinterestrate.Asaresult,onlywhenthenominalinterest
rate is zero are the private and social costs of holding money equated.
Notethatsuchapolicyimpliesanaverage(steadystate)rateofinflation
π =−ρ <0
that is, prices will decline on average at the rate of time preference.
In other words, under the Friedman rule the economy experiences
(moderate)steadystatedeflation,onaverage.
Implementation of the Friedman rule requires some discussion. First,
as was the case in the cashless model, a policy rule of the form i = 0
t
for all t leaves the price level indeterminate in the classical model with
moneyintheutilityfunction.Toseethisnotethat,underthatrule,(43)
and(47)implythatanyinflationpaththatsatisfies
π t+1 =−ρ−σψ ya E t {(cid:12)a t+1 }+ξ t+1
for an arbitrary martingale-difference sequence {ξ } is an equilibrium
t
path.13
13Thatfindingcanbeseenasaparticularcaseofamoregeneralresult:Underasimple
interestrateruleoftheformit = ρ+π+φ π(π t −π),withφ π ≥ 0,theconditionfora
locallyuniqueequilibriumisgivenbyφ π > 1(seeexercise6below).Notethattherule
analyzedinthetextcorrespondstotheparticularcaseπ =−ρandφ
π
=0.

42 CHAPTER2
Even though that indeterminacy should not have any welfare con-
sequences (because consumption, employment, and real balances are
pinned down uniquely as a function of technology and the nominal
interest rate), a central bank could avoid nominal indeterminacy by
followingaruleoftheform
i t =φ(r t−1 +π t )
for any φ > 1. Combined with (22), that rule implies the difference
equation
E t {i t+1 }=φi t
whose only stationary solution is i = 0 for all t. Under that rule,
t
equilibriuminflationisfullypredictableandgivenby
π
t
=−r
t−1
Moregenerally, any rulethat makes the central bank adjust itspolicy
settings(e.g.,themoneysupply)toguaranteethatcurrentinflationmoves
one-for-one,butinversely,withthelaggedrealinterestrate,willimplya
zeronominalinterestrateand,thus,anoptimallevelofrealbalances.
2.6 NOTES ON THELITERATURE
The modeling approach favored in much of the recent monetary litera-
ture,andtheoneadoptedinthisbook(withtheexceptionofsection2.5
of this chapter), does not incorporate money explicitly in the analysis.
Under that approach the main role played by money is that of a unit
of account. Such model economies can be viewed as a limiting case (the
so-called cashless limit) of an economy in which money is valued and
held by households, but in which the transaction services provided by
real balances are arbitrarily small relative to the size of the economy.
Woodford (2003) provides a detailed discussion and a forceful defense
ofthatapproach.
Mostmodelsintheliteraturethatintroducemonetaryassetsexplicitly
relyononeoftwoalternativeformalismsinordertogenerateademand
for an asset that—as is the case with money—is dominated in its rate
of return by alternative assets that have identical risk characteristics:
they assume that real balances either (i) generate (indirect) utility to
households or (ii) provide some “transaction services” which render

ACLASSICALMONETARYMODEL 43
themnecessary—or,atleast,useful—whenpurchasinggoods.14 Thefirst
approachcanoftenbeviewedasareducedformofthesecond(exercises
7and9belowillustratethispoint).
The first of those approaches—money in the utility function—traces
back to Sidrauski (1967), who introduced that assumption in an other-
wise standard neoclassical growth model (with inelastic labor supply).
Woodford (2003) offers a detailed analysis of the implications of
alternative assumptions on the specification of utility and, in particular,
ofthelikelydegreeofmonetarynon-neutralitiesarisingfromthenonsep-
arability of real balances. Walsh (2010, chap. 2) develops a model with
money in the utility function, and analyzes the equilibrium properties
of a calibrated version of that model. Both analyses conclude, in a way
consistent with the discussion above, that even under a utility that is
nonseparable in real balances, the real effects of monetary policy are
quantitativelyverysmallforplausiblecalibrationsofthemodels.
A common approach to the modeling of a transaction’s motive for
holding money builds on the assumption, originally due to Clower
(1967), that cash must be held in advance in order to purchase certain
goods. Early examples of classical monetary models in which a demand
for money is generated by postulating a cash-in-advance constraint can
befoundintheworkofLucas(1982)andSvensson(1985).Cooleyand
Hansen (1989) analyze an otherwise standard RBC model augmented
with a cash-in-advance constraint for consumption goods, showing that
monetary policy is nearly neutral for plausible calibrations of that
model.Walsh(2010,chap.3)providesadetaileddescriptionofclassical
monetarymodelswithcash-in-advanceconstraintsandtheirimplications
for the role of monetary policy. Exercises 8 and 9 below ask the reader
toanalyzeeconomieswithcash-in-advanceconstraints.
An alternative way of modeling the transaction services of money
consists in assuming that the time required to purchase goods (which
detracts from leisure and/or work time) is inversely related to the level
of real balances. See Walsh (2010, chap. 3) for a detailed analysis of a
“shoppingtime”model.
The practice, followed in this monograph, of appending a money
demand equation to a set of equilibrium conditions that have been
derived in the context of cashless economy is often found in the
literature. King and Watson (1995) constitutes an early example of that
practice.
14 A third approach, seldom found in the recent literature, emphasizes the function of
moneyasastoreofvalue,i.e.,asawayoftransferringresourcesintertemporally.Inthe
absenceofotherservicesordividendsassociatedwithmoney,thelattercanbeviewedasa
purebubbleunderthisapproach.See,e.g.,Samuelson(1958).

44 CHAPTER2
The analysis of the form of the optimal monetary policy in a classical
economygoesbacktoFriedman(1969),whereacaseismadeforapolicy
thatkeepsthenominalinterestrateconstantatazerolevel.Morerecent
treatments of the conditions under which that rule is optimal include
Woodford(1990)andCorreiaandTeles(1999).
In the present chapter, as well as in the rest of the book, the analysis
is restricted to local equilibrium dynamics, that is, to equilibrium paths
that remain within a neighborhood of the steady state. Accordingly,
the notion of uniqueness or indeterminacy used throughout the book
must be understood as referring to those bounded equilibria only. A
discussion of the conditions under which a classical monetary economy
may display global multiplicity of equilibria, coexisting with a locally
uniqueequilibrium,canbefoundinBenhabib,Schmitt-Grohé,andUribe
(2001) and Woodford (2003, chap. 2), among others. The previous
authors also discuss alternative policies that guarantee that locally
unique equilibria around the desired steady state are also globally
unique.
Finally, the reader can find two useful discussions of the notion of
monetary neutrality and its evolution in macroeconomic thinking in
Patinkin(1987)andLucas(1996).
APPENDIX
2.1 LOG-LINEARAPPROXIMATIONOFTHEEULEREQUATION
Theconsumer’sEulerequationcanberewrittenas
1= E t {exp(i t −σ(cid:12)c t+1 −π t+1 −ρ+(cid:12)x t+1 )} (51)
In a perfect foresight steady state with constant inflation π and
constantgrowthγ
i =ρ+π +σγ
Afirst-orderTaylorexpansionofexp(i t −σ(cid:12)c t+1 −π t+1 −ρ+(cid:12)x t+1 )
aroundthatsteadystateyields
exp(i t −σ(cid:12)c t+1 −π t+1 −ρ+(cid:12)x t+1 )
(cid:8)1+(i
t
−i)−σ((cid:12)c
t+1
−γ)−(π
t+1
−π)+(cid:12)x
t+1
=1+i
t
−σ(cid:12)c
t+1
−π
t+1
−ρ+(cid:12)x
t+1
whichcanbeusedin(51)toobtain,aftersomerearrangementofterms,
thelog-linearizedEulerequation
1
c t = E t {c t+1 }− σ (i t −E t {π t+1 }−ρ−(1−ρ x )x t )

ACLASSICALMONETARYMODEL 45
REFERENCES
Benhabib, Jess, Stephanie Schmitt-Grohé, and Martin Uribe (2001):
“Monetary Policy and Multiple Equilibria,” American Economic Review
91(1),167–186.
Chari,V.V.,LawrenceJ.Christiano,andPatrickJ.Kehoe(1996):“Optimalityof
theFriedmanRuleinEconomieswithDistortingTaxes,”JournalofMonetary
Economics37,203–223.
Christiano, Lawrence J., Martin Eichenbaum, and Charles L. Evans (2005):
“NominalRigiditiesandtheDynamicEffectsofaShocktoMonetaryPolicy,”
JournalofPoliticalEconomy113(1),1–45.
Clower,Robert(1967):“AReconsiderationoftheMicroeconomicFoundations
ofMonetaryTheory,”WesternEconomicJournal6,1–8.
Cooley, Thomas F., and Gary D. Hansen (1989): “Inflation Tax in a Real
BusinessCycleModel,”AmericanEconomicReview79(4),733–748.
Correia,Isabel,andPedroTeles(1999):“TheOptimalInflationTax,”Reviewof
EconomicDynamics2(2),325–346.
Friedman,Milton(1969):TheOptimumQuantityofMoneyandOtherEssays,
Aldine,Chicago.
King,RobertG.,andMarkWatson(1995):“Money,Prices,InterestRates,and
theBusinessCycle,”ReviewofEconomicsandStatistics58(1),35–53.
Lucas,RobertE.(1982):“InterestRatesandCurrencyPricesinaTwo-Country
World,”JournalofMonetaryEconomics10(3),335–359.
Lucas, Robert E. (1996): “Nobel Lecture: Monetary Neutrality,” Journal of
PoliticalEconomy104(4),661–682.
Lucas, Robert E. (2000): “Inflation and Welfare,” Econometrica 68(4),
247–274.
Patinkin, Don (1987): “Neutrality of Money,” in J. Eatwell, M. Milgate, and
P. Newman, eds., The New Palgrave: A Dictionary of Economics, 273–287,
Norton,NewYork.
Samuelson, Paul A. (1958): “An Exact Consumption-Loan Model of Interest
with or without the Social Contrivance of Money,” Journal of Political
Economy66(6),467–482.
Schmitt-Grohé, Stephanie, and Martin Uribe (2011): “The Optimal Rate of
Inflation,” in B. M. Friedman and Michael Woodford, eds., Handbook of
MonetaryEconomics,vol.3B,653–722,Elsevier,NewYork.
Sidrauski,Miguel(1967):“InflationandEconomicGrowth,”JournalofPolitical
Economy75,796–816.
Svensson, Lars E. O. (1985): “Money and Asset Prices in a Cash in Advance
Economy,”JournalofPoliticalEconomy93(5),919–944.
Walsh, Carl E. (2010): Monetary Theory and Policy, 3rd ed., MIT Press,
Cambridge,MA.
Woodford, Michael (1990): “The Optimum Quantity of Money,” in B. M.
Friedman and F. H. Hahn, eds., Handbook of Monetary Economics vol. 2,
1067–1152,Elsevier,NewYork.
Woodford, Michael (2003): Interest and Prices: Foundations of a Theory of
MonetaryPolicy,PrincetonUniversityPress,Princeton,NJ.

46 CHAPTER2
EXERCISES
2.1. Optimalityconditionsundernonseparableleisure
Derive the log-linearized optimality conditions of the household
problem under the following specification of the period utility
function:
[C(1−N)ν]1−σ −1
U(C,N)= t t
t t 1−σ
2.2. Alternativeinterestrulesfortheclassicaleconomy
Consider the classical economy described in the text, with equi-
libriumconditions
1
y t = E t {y t+1 }− σ (i t −E t {π t+1 }−ρ)
and
r t ≡i t −E t {π t+1 }
=ρ+σE
t
{(cid:12)y
t+1
}
where y and, hence, r , are determined independently of mone-
t t
tary policy. Analyze the implications of the following alternative
monetary policy rules. When relevant, assume that the money
demandfunctiontakestheform
m − p = y −ηi +εm
t t t t t
whereεmisastochasticmoneydemanddisturbance.
t
a. Rule#1:Strictinflationtargeting.
i. Deriveaninterestraterulethatguaranteesfullstabilization
of inflation, i.e., π = π∗ for all t where π∗ is an inflation
t
target.
ii. Determine the behavior of money growth implied by that
rule.
iii. Explain why a policy characterized by a constant rate
of money growth (cid:12)m =π∗ will generally not succeed in
t
stabilizinginflationinthateconomy.
b. Rule#2:Priceleveltargeting
i. Considertheinterestraterule
i =ρ+π∗+φ (p − p ∗ )
t p t t

ACLASSICALMONETARYMODEL 47
where φ > 0 and p∗ = p∗ +π∗t is a time-varying target
p t 0
forthe(log)pricelevelconsistentwithanaverageinflation
π∗. Determine the equilibrium behavior of the price level
under this rule. (Hint: you may find it useful to introduce
anewvariable (cid:14)p ≡p − p∗,thedeviationofthepricelevel
t t
fromtarget,toeasesomeofthealgebraicmanipulations.)
ii. Considerinsteadthemoneysupplyrule
(cid:12)m =π∗
t
Determinetheequilibriumbehaviorofthepricelevelunder
thisrule,assumingthatm = p∗.
0 0
iii. Show that the money supply rule considered in (ii) can be
combined with the money market clearing condition and
rewrittenasapriceleveltargetingruleoftheform
i =ψ(p − p ∗ )+u
t t t t
for some constant ψ and stochastic process u to be
t
determined.
iv. Suppose that the central bank wants to minimize the
volatility of the price level. Discuss the advantages and
disadvantages of the interest rate rule in (i) versus the
moneysupplyrulein(ii)inlightofyourfindingsabove.
2.3. Equilibrium indeterminacy and interest rate rules (based on
Woodford(2003))
Consideraclassicaleconomywithanexogenousrealinterestrate
process {r }. Discuss the conditions under which the equilibrium
t
will be (locally) unique and solve for the equilibrium level of
inflationwhenthecentralbankfollowstherules:
a. Rule#1:Partialadjustment
i t =φ i i t−1 +(1−φ i )i t ∗
whereφ ∈[0,1]andi∗ isareferenceinterestrategivenby
i t
i t ∗ =ρ+φ π π t
b. Rule#2:Movingaverageinflationtargeting
i t =ρ+φ π π t

48 CHAPTER2
where
(cid:1)∞
π
t
=(1−δ) δkπ
t−k
k=0
c. Showtheequivalencebetweenthetworules
2.4. Onthewelfarecostsofinflation(basedonLucas(2000))
Consider an endowment economy where the representative con-
sumer’speriodutilityisgivenby
(cid:20) (cid:8) (cid:9)(cid:21)
U (cid:11) C, M t (cid:12) = C t ψ M C t / t Pt 1−σ −1
t P 1−σ
t
where ψ(z) ≡z/(χ + z). The household’s budget constraint is
givenby
P t C t +Q t B t +M t ≤ B t−1 +M t−1 + P t Y t
where {Y} is an exogenous stochastic endowment, which is
t
nonstorable.
a. Derive the household’s optimality conditions, including the
demandforrealbalances.
b. ShowthattheFriedmanruleisthewelfare-maximizingmone-
tarypolicy
c. Focusing on a steady state with Y = 1, define the welfare cost
of inflation as the permanent percent increase in consumption
that would make the household indifferent between a steady
stateinflationrateπ andzeroinflation.
d. Determine, up to a second order approximation, the welfare
losses resulting from fluctuations in the nominal interest rate,
relativetoaconstantinterestratepolicy.
2.5. Optimal monetary policy in a classical economy with an exact
equilibriumrepresentation
Consider a version of the classical economy with money in the
util(cid:15)ity function, where the representative consumer maximizes
E
0
∞
t=0
βtU(C
t
, M
Pt
t,N
t
) subject to the sequence of budget con-
straints
P t C t +M t +Q t B t ≤ M t−1 +B t−1 +W t N t +D t

ACLASSICALMONETARYMODEL 49
Assumeaperiodutilitygivenby
(cid:11) (cid:12)
M M
N1+ϕ
U C, t,N =logC +log t − t (52)
t P t t P 1+ϕ
t t
Suppose there is a representative perfectly competitive firm,
producing the single consumption good. The firm has access to
thelinearproductionfunctionY(i)= AN(i),whereproductivity
t t t
evolvesaccordingto
A
t =(1+γ )exp{εa}
A t−1 a t
with {εa} an i.i.d. random process, normally distributed, with
t
mean0andvarianceσ2.
a
Themoneysupplyvariesexogenouslyaccordingtotheprocess
M
t =(1+γ )exp{εm} (53)
M t−1 m t
where {εm} is an i.i.d., normally distributed process with mean 0
t
and variance σ2. Assume that {εm} evolves exogenously, outside
m t
the control of the monetary authority (e.g., could reflect shocks
in the monetary multiplier that prevent the monetary authority
fromfullycontrollingthemoneysupply).Finally,assumethatall
outputisconsumed,sothatinequilibriumY =C forallt.
t t
a. Derivetheoptimalityconditionsfortheproblemofhouseholds
andfirms.
b. Determine the equilibrium levels of aggregate employment,
output,andinflation(Hint:guessthattheequilibriuminvolves
aconstantvelocity PtYt = V forallt).
Mt
c. Discusshow utilitydepends on thetwo parameters describing
monetary policy, γ and σ2 (recall that the nominal interest
m m
rate is constrained to be non-negative, i.e., Q ≤ 1 for all t).
t
Show that the optimal policy must satisfy the Friedman rule
(i =0forallt).
t
2.6. Equilibrium uniqueness in the classical model with money in the
utilityfunction
Consider the classical model equilibrium, as described by condi-
tions(43),(47),andthesimpleinterestraterule
i t =ρ+φ π π t
Showthattheequilibriumislocallyuniqueifandonlyifφ
π
>1.

50 CHAPTER2
2.7. Ashoppingtimemodel
Assume that the transactions technology is such that consuming
C requiresaquantityofshoppingtime Ns = S(C, Mt),givenreal
t t t Pt
balances Mt,where S >0and S ≤0.Theperiodutilityisgiven
by V(C,L
Pt
)where L
c
=1−N −
m
Ns denotesleisuretimeand N
t t t t t t
timeatwork.
a. Derive the implied utility function U(C, Mt,N), i.e., in terms
t Pt t
of consumption, hours, and real balances and discuss its
properties (sign of first and second derivatives) as a function
ofthoseof V and S
b. Using the finding in part a), derive the optimality conditions
of the household’s problem, under the sequence of budget
constraints(31),andshowthatundertheoptimalplan Wts (cid:8)
Pt m
i .Interpretthelattercondition.
t
c. Derivethemoneydemandfunctionu(cid:8)nderth(cid:9)eassumptionthat
V(C,L) = logC +χlogL and S C, Mt = Av + B/v −
√ t t t t t Pt t t
2 ABwherev ≡PC/M (basedonSchmitt-GrohéandUribe
t t t t
(2011))
2.8. Amodelwithacash-in-advanceconstraint
Consider a monetary economy where households’ maximize
(cid:15)
∞ βt(logC − 1 N1+ϕ ) subject to the sequence of budget
t=0 t 1+ϕ t
constraints
P t C t +Q t B t +M t ≤ B t−1 +M t−1 +W t N t +T t
and the cash-in-advance (CIA) constraint P t C t ≤ M t−1 + T t ,
where T isalump-summonetarytransfertohouseholds.Output
t
is produced by a representative perfectly competitive firm with
technology Y = N. The money supply grows at a constant
t t
growthrateγ .Thereisnouncertainty.
m
a. Derivethehousehold’soptimalityconditions.
b. Determinehowmoneygrowthaffectsequilibriumoutput.
c. Whatistheoptimalrateofinflation?
2.9. Amodelwithcashandcreditgoods
Assumethattheutilityoftherepresentativehouseholdisgivenby
V(C ,C ,N) (54)
1t 2t t

ACLASSICALMONETARYMODEL 51
where C denotes consumption of a “cash good” (i.e., a good
1t
that requires cash in order to be purchased), C is consumption
2t
ofa“creditgood”(whichdoesnotrequirecash),and N islabor
t
supply. For simplicity, assume that the price of the two goods is
identical and equal to P (this will be the case if the production
t
functionoftherepresentativefirmisgivenbyY +Y = N and
1t 2t t
there is perfect competition). Purchases of cash goods have to be
settled in cash, whereas credit goods can be financed by issuing
one-periodrisklessnominalbonds.
Thebudgetconstraintisgivenby
P t (C 1t +C 2t )+Q t B t +M t = B t−1 +M t−1 +W t N t +T t
Finally,thecash-in-advance(CIA)constraintisgivenby
P t C 1t ≤ M t−1 +T t
where, in equilibrium, T =(cid:12)M, i.e., transfers to households
t t
correspond to money transfers made by the central bank, which
consumerstakeasgiven.Forsimplicity,assumenouncertainty.
a. Derive the first-order conditions associated with the house-
hold’sproblem
b. NotethatwhenevertheCIAconstraintisbindingreducedform
periodutilitycanbedefinedas
(cid:11) (cid:12) (cid:11) (cid:12)
M M M
U C, t,N ≡V t,C − t,N
t t t t
P P P
t t t
whereC =C +C .ShowthatU ≥0,giventheoptimality
t 1t 2t m
conditionsderivedin(a).