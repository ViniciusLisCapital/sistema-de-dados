Chapter 3
THE BASIC NEW KEYNESIAN MODEL
Thepresentchapterdescribesthekeyelementsofthebaselinemodelthat
willbeusedasareferenceframeworkintheremainderofthebook.The
modelinvolvestwomaindeparturesfromtheassumptionsoftheclassical
monetary economy developed in chapter 2. First, imperfect competition
inthegoodsmarketisintroducedbyassumingthateachfirmproducesa
differentiatedgoodforwhichitsetstheprice(insteadoftakingtheprice
asgiven),givenademandconstraint.Second,aformofpricestickinessis
introducedbyassumingthatonlyafractionoffirmscanresettheirprices
inanygivenperiod.Inparticular,andfollowingmuchoftheliterature,a
modelofstaggeredpricesettingduetoCalvo(1983)andcharacterizedby
randompricedurationsisadopted.1 Theresultingframeworkisreferred
to as the basic New Keynesian model. As discussed in chapter 1, that
model has become in recent years the workhorse for the analysis of
monetarypolicy,fluctuations,andwelfare.
The introduction of differentiated goods requires that the household
problem be modified slightly relative to the one considered in the
previous chapter. That modification is discussed before turning to the
firms’optimalprice-settingproblemandtheimpliedinflationdynamics.
3.1 HOUSEHOLDS
Onceagain,assumearepresentativeinfinitelylivedhouseholdseekingto
maximize
(cid:1)∞
E βtU(C,N;Z)
0 t t t
t=0
whereC isnowaconsumptionindexgivenby
t
(cid:2) (cid:4)
(cid:3) (cid:2)
1 (cid:2)−1
C
t
≡ C
t
(i)1−1 (cid:2)di
0
1Theresultinginflationdynamicscanalsobederivedundertheassumptionofquadratic
costsofpriceadjustment.See,e.g.,Rotemberg(1982).

THEBASICNEWKEYNESIANMODEL 53
with C(i) denoting the quantity of good i consumed by the household
t
in period t. A continuum of goods represented by the interval [0,1] is
assumed.Theperiodbudgetconstraintnowtakestheform
(cid:3)
1
P t (i)C t (i)di +Q t B t ≤ B t−1 +W t N t +D t
0
for t = 0,1,2..., where P(i) is the price of good i, and where the
t
remaining variables are defined as in chapter 2: N denotes employment
t
or hours worked, W is the nominal wage, B represents purchases of
t t
one-period discount bonds (at a price Q), and D denotes dividends
t t
from the ownership of firms. The above sequence of period budget
constraints(cid:5)is supp(cid:6)lemented with a solvency constraint of the form
lim T→∞E t (cid:3) t,T B PT T ≥ 0 for all t, where (cid:3) t,T ≡ βT−tU c,T /U c,t . Note
that monetary holdings are not modeled explicitly, so one can think of
the present framework as the cashless limit of an economy with money
intheutilityfunction,withthelatterbeingadditivelyseparable.2
In addition to the consumption/savings and labor supply decisions
alreadyanalyzedinchapter2,thehouseholdnowmustdecidehowtoal-
locateitsconsumptionexpendituresamongthedifferentgoods.Optimal
behavior requires that the consumption index C be maximized for any
(cid:7) t
1
given level of expenditures P(i)C(i)di. As shown in appendix 3.1,
0 t t
thesolutiontothatproblemyieldsthesetofdemandequations
(cid:8) (cid:9)
−(cid:2)
P(i)
C(i)= t C (1)
t t
P
t
(cid:10) (cid:11)
(cid:7) 1
for all i ∈ [0,1], where P ≡ 1 P(i)1−(cid:2)di 1−(cid:2) is an aggregate price
t 0 t
index.Furthermore,andconditionalonsuchoptimalbehavior
(cid:3)
1
P(i)C(i)di = PC
t t t t
0
i.e.,totalconsumptionexpenditurescanbewrittenastheproductofthe
price index times the quantity index. Plugging the previous expression
intothebudgetconstraintyields
P t C t +Q t B t ≤ B t−1 +W t N t +D t
2Seesection5ofchapter2foradiscussion.

54 CHAPTER3
which is formally identical to the constraint facing households in
the single good economy analyzed in chapter 2. Hence, the optimal
consumption/savingsandlaborsupplydecisionsareidenticaltotheones
derivedtherein,anddescribedbytheconditions
− U n,t = W t
U c,t P t
(cid:12) (cid:13)
Q =βE U c,t+1 P t
t t
U c,t P t+1
As in chapter 2, it is assumed that the household’s period utility is
givenby
(cid:10) (cid:11)
 C t 1−σ−1 − N t 1+ϕ Z forσ (cid:7)=1
1−σ 1+ϕ t
U(C,N;Z)= (cid:10) (cid:11)
t t t 
logC − N t
1+ϕ
Z forσ =1
t 1+ϕ t
wherez ≡logZ followsanexogenous AR(1)process
t t
z t =ρ z z t−1 +ε t z
withρ ∈[0,1).
z
As shown in chapter 2, the resulting log-linear versions of the above
optimalityconditionstaketheform
w − p =σc +ϕn (2)
t t t t
1 1
c t = E t {c t+1 }− σ (i t −E t {π t+1 }−ρ)+ σ (1−ρ z )z t (3)
where i ≡ −logQ is the short-term nominal interest rate and ρ ≡
t t
−logβ is the discount rate, and where lowercase letters are used
to denote the logs of the original variables. As before, the previous
conditions are supplemented, when necessary, with an ad hoc log-linear
moneydemandequationoftheform
m − p = y −ηi (4)
t t t t
wherem denotes(log)nominalmoneyholdings.
t

THEBASICNEWKEYNESIANMODEL 55
3.2 FIRMS
Assumeacontinuumoffirmsindexedbyi ∈[0,1].Eachfirmproducesa
differentiatedgood,buttheyalluseanidenticaltechnology,represented
bytheproductionfunction
Y(i)= AN(i)1−α (5)
t t t
where A represents the level of technology, assumed to be common to
t
allfirmsandtoevolveexogenouslyovertimeaccordingtotheprocess
a t =ρ a a t−1 +ε t a (6)
withρ ∈[0,1].
a
Allfirmsfaceanidenticalisoelasticdemandschedulegivenby(1),and
take the aggregate price level P and aggregate consumption indexC as
t t
given.
Following the formalism proposed in Calvo (1983), each firm may
resetitspriceonlywithprobability1−θ inanygivenperiod,independent
ofthetimeelapsed sinceitlastadjusted itsprice.Thus,ineach perioda
measure1−θ ofproducersresettheirprices,whileafractionθ keeptheir
pricesunchanged.Asaresult,theaveragedurationofapriceisgivenby
1 .Inthiscontext,θ becomesanaturalindexofpricestickiness.
1−θ
3.2.1 AggregatePriceDynamics
As shown in appendix 3.2, the above environment implies that the
aggregatepricedynamicsaredescribedbytheequation
(cid:8) (cid:9)
P∗ 1−(cid:2)
(cid:12)1−(cid:2) =θ +(1−θ) t (7)
t P t−1
where(cid:12) ≡ Pt isthegrossrateofinflationbetweent−1andt,and P∗
t Pt−1 t
isthepricesetinperiodtbyfirmsreoptimizingtheirpriceinthatperiod.
Notice that, as shown below, all firms resetting their price in any given
periodwillchoosethesamepricebecausetheyfaceanidenticalproblem.
It follows from (7) that in a steady state with zero inflation ((cid:12) = 1),
P t ∗ = P t−1 = P t forallt.Furthermore,alog-linearapproximationtothe
aggregatepriceindexaroundthatsteadystateyields
π t =(1−θ)(p t ∗− p t−1 ) (8)

56 CHAPTER3
or,equivalently,afterrearrangingterms:
p t =θp t−1 +(1−θ)p t ∗
i.e., the current price level is a weighted average of last period’s price
level and the newly set price, all in logs, with the weights given by the
fractionoffirmsthatdonotanddoadjustprices,respectively.
Thepreviousequationsmakeclearthat,inthepresentsetup,variations
inthepricelevelresultfromthefactthatfirmsreoptimizinginanygiven
period choose a price that differs from the economy’s average price in
the previous period. Hence, and in order to understand the evolution of
inflation over time, one needs to analyze the factors underlying firms’
pricesettingdecisions,aquestionwhichisdiscussednext.
3.2.2 OptimalPriceSetting
A firm reoptimizing in period t will choose the price P∗ that maximizes
t
thecurrentmarketvalueoftheprofitsgeneratedwhilethatpriceremains
effective. As shown in appendix 3.3, this corresponds to solving the
followingproblem:
(cid:1)∞ (cid:18) (cid:19) (cid:20)(cid:21)
m P a ∗ x θkE t (cid:3) t,t+k (1/P t+k ) P t ∗ Y t+k|t −C t+k (Y t+k|t )
t k=0
subjecttothesequenceofdemandconstraints
(cid:8) (cid:9)
P∗ −(cid:2)
Y t+k|t = t C t+k (9)
P t+k
fork= 0,1,2,...where(cid:3) t,t+k ≡ βkU c,t+k /U c,t isthestochasticdiscount
factor, C t (·) is the (nominal) cost function, and Y t+k|t denotes output in
period t+kfor a firm that last reset its price in period t. Note that it is
implicitly assumed that the firm always meets the demand for its good
at the current price. That assumption, which is maintained throughout
the analysis below, requires, in turn, that the average price markup is
sufficientlylargeand/orthattheshiftsindemandresultingfromavariety
ofshocksarenottoolarge.
Theoptimalityconditionassociatedwiththeproblemabovetakesthe
form
(cid:1)∞ (cid:18) (cid:19) (cid:20)(cid:21)
θkE t (cid:3) t,t+k Y t+k|t (1/P t+k ) P t ∗−M(cid:13) t+k|t =0 (10)
k=0

THEBASICNEWKEYNESIANMODEL 57
where(cid:13) t+k|t ≡C t (cid:9) +k (Y t+k|t )denotesthe(nominal)marginalcostinperiod
t+kforafirmwhichlastresetitspriceinperiodt andM≡ (cid:2) .
(cid:2)−1
Notethatinthelimitingcaseofnopricerigidities(θ =0),theprevious
condition collapses to the familiar optimal price setting condition for a
monopolisticcompetitorunderflexibleprices
P t ∗ =M(cid:13) t|t
whichallowsustointerpretMastheoptimalmarkupintheabsenceof
constraintsonthefrequencyofpriceadjustment.Henceforth,Misoften
referred to as the “desired,” “natural,” or “frictionless” markup. That
markupisconstantgiventheassumptionofatime-invariantelasticityof
substitution(cid:2).
Next,theoptimalpricesettingcondition(10)islog-linearizedaround
the perfect foresight zero inflation steady state. Note that the latter is
characterizedby(cid:3) t,t+k =βkand P t ∗/P t−k = P t /P t−k =1.Thus,allfirms
produce the same quantity of output, and face the same marginal cost,
thatis,Y t+k|t =Y,and(cid:13) t+k|t =(cid:13) t+k =(cid:13) t forallt andk=0,1,2,3,...
Thus,(10)impliesthat P =M(cid:13) foralltinthatsteadystate,i.e.,actual
t t
markups,commontoallfirms,coincidewiththefrictionlessmarkup.
Afirst-orderTaylorexpansionof(10)aroundthezeroinflationsteady
stateyields,aftersomemanipulation,
(cid:1)∞
p t ∗ =µ+(1−βθ) (βθ)kE t {ψ t+k|t } (11)
k=0
where ψ t+k|t ≡ log(cid:13) t+k|t is the (log) marginal cost and µ ≡ logM
is the log of the desired gross markup (which, for M close to one, is
approximatelyequaltothenetmarkupM−1).Hence,andtotheextent
thatpricesaresticky(θ >0),firmssetpricesinaforward-lookingway.In
particular, they choose a price that corresponds to their desired markup
overaweightedaverageoftheircurrentandexpected(nominal)marginal
costs,withtheweightsbeingproportionaltotheprobabilityoftheprice
remaining effective at each horizon, θk, times the cumulative discount
factor,βk.
3.3 EQUILIBRIUM
Marketclearinginthegoodsmarketrequiresthatthequantityproduced
of each good matches the quantity demanded. In the stylized model
analyzed here consumption is the only source of demand for goods.

58 CHAPTER3
Thus,inequilibrium,
Y(i)=C(i)
t t
foralli ∈[0,1]andallt.
(cid:10) (cid:11)
(cid:7) (cid:2)
Letting aggregate output be defined as Y
t
≡
0
1 Y
t
(i)1−1 (cid:2)di (cid:2)−1 it
followsthat
Y =C (12)
t t
mustholdforallt.
Aggregate consumption C (which corresponds to aggregate demand
t
in the present model) is in turn determined by the consumer’s Euler
equation (3). Combining the latter with (12) yields an expression for
current (log) output as a function of the latter’s expected one-period-
aheadvalue,therealinterestrate,andthedemandshifter:
1 1
y t = E t {y t+1 }− σ (i t −E t {π t+1 }−ρ)+ σ (1−ρ z )z t (13)
Notethat(13)canbesolvedforwardtoyield
(cid:1)∞
1 1
y t = σ z t − σ E t {i t+k −E t {π t+1+k }−ρ}+ T l → im ∞ E t {y t+T }
k=0
Thus,anexogenousshockwillimpactoutputonlytotheextentthatit
meetsoneormoreofthefollowingconditions:(i)itshiftsthepreference
parameter z,(ii)ithasapermanenteffectonthelevelofoutput,or(iii)
t
it leads to a deviation of the real interest rate from the discount rate,
currentoranticipated.
Aggregate employment is given by the sum of employment across
firms:
(cid:3)
1
N = N(i)di
t t
0

THEBASICNEWKEYNESIANMODEL 59
Using(5)
(cid:3) (cid:8) (cid:9)
N =
1 Y
t
(i) 1− 1 α
di
t
A
0 t
(cid:8) (cid:9) (cid:3) (cid:8) (cid:9)
=
Y
t
1− 1 α 1 P
t
(i) − 1− (cid:2) α
di
A P
t 0 t
wherethesecondequalityfollowsfrom(1)andthegoodsmarketclearing
condition.Takinglogs,
(1−α)n = y −a +d
t t t t
(cid:7)
where d t ≡ (1 − α)log 0 1 (P t (i)/P t ) − 1− (cid:2) α di is a measure of price (and,
hence, output) dispersion across firms. In appendix 3.4 it is shown that,
in a neighborhood of the zero inflation steady state, d is equal to zero
t
up to a first-order approximation. Hence, one can write the following
approximaterelation
1
n = (y −a ) (14)
t 1−α t t
which can be thought of as determining aggregate employment, given
aggregateoutputandtechnology.
Notethatthe(log)marginalcostforanindividualfirmthatlastsetits
priceinperiodt isgivenby:3
ψ
t+k|t
=w
t+k
−mpn
t+k|t
=w
t+k
−(a
t+k
−αn
t+k|t
+log(1−α))
where mpn t+k|t and n t+k|t respectively denote the (log) marginal product
oflaborand(log)employmentinperiodt+kforafirmthatlastresetits
priceinperiodt.
3 Marginal cost equals the labor needed to produce an additional unit of output,
1/MPNt+k|t, times the cost of each unit of that labor, i.e., the wage Wt+k. Formally,
(cid:13)
t+k|t
=Wt+k /MPNt+k|t.

60 CHAPTER3
(cid:7)
Letting ψ ≡ 1ψ (i)di represent the (log) average marginal cost, it
t 0 t
followsthat
(cid:1)∞
ψ
t
=(1−θ) θkψ
t|t−k
k=0
=w −(a −αn +log(1−α))
t t t
(cid:7)
where the second equality makes use of the relation n = 1 n(i)di,
t 0 t
which holds up to a first order approximation about a symmetric
equilibrium.
Thusthefollowingrelationholdsbetweenfirm-specificandeconomy-
widemarginalcosts:
ψ t+k|t =ψ t+k +α(n t+k|t −n t+k )
α
=ψ t+k + 1−α (y t+k|t −y t+k )
α(cid:2)
=ψ t+k − 1−α (p t ∗− p t+k ) (15)
where the second equality follows from (14) and the third equality
results from combining demand schedule (9) and goods market clearing
condition (12) (after taking logs). Notice that under the assumption
of constant returns to scale (α = 0), marginal cost is independent of
the level of production and, hence, it is common across firms, that is,
ψ t+k|t =ψ t+k .
Substituting(15)into(11)andrearrangingtermsyields
(cid:1)∞ (cid:18) (cid:21)
p t ∗ =(1−βθ) (βθ)kE t p t+k −(cid:15)µ(cid:22) t+k
k=0
where µ(cid:22) ≡ µ − µ is the deviation between the average and desired
t t
markups,withµ ≡ p −ψ and(cid:15)≡ 1−α ∈(0,1].
t t t 1−α+α(cid:2)
Theaboveexpressionfor p∗ canberewrittenasarecursiveequation:
t
p ∗ =βθE{p ∗ }+(1−βθ)(p −(cid:15)µ(cid:22) ) (16)
t t t+1 t t
Finally,combining(8)and(16)yieldstheinflationequation
π t =βE t {π t+1 }−λµ(cid:22) t (17)

THEBASICNEWKEYNESIANMODEL 61
where
(1−θ)(1−βθ)
λ≡ (cid:15)
θ
is strictly decreasing in the index of price stickiness θ, in the measure of
decreasingreturnsα,andinthedemandelasticity(cid:2).4 Notethat(cid:15)=1in
theparticularcaseofconstantreturnstolabor(α =0).
Solving (17) forward, inflation is expressed as the discounted sum of
current and expected future deviations of average markups from their
desiredlevels:
(cid:1)∞
π
t
=−λ βkE
t
{µ(cid:22)
t+k
}
k=0
Thus, inflation will be positive when firms expect average markups
to be below their desired level µ, for in that case firms that have the
opportunity to reset prices will, on average, choose a price above the
economy’s average price level in order to realign their markup closer to
itsdesiredlevel.
It is worth emphasizing here that the mechanism underlying fluctua-
tionsintheaggregatepricelevelandinflationlaidoutabovehaslittlein
commonwiththeoneatworkintheclassicalmonetaryeconomy.Thus,
in the present model, inflation results from the aggregate consequences
of purposeful price-setting decisions by firms, which adjust their prices
in light of current and anticipated cost conditions. By contrast, in
the classical monetary economy analyzed in chapter 2, inflation is a
consequence of the changes in the aggregate price level that, given
the monetary policy rule in place, are consistent with an equilibrium
allocationthatisindependentoftheevolutionofnominalvariables,with
noaccountgivenofthemechanism(otherthanan“invisiblehand”)that
willbringaboutthosepricelevelchanges.
Next, a relation is derived between the economy’s average price
markup and aggregate output. Notice that independently of the nature
4Analternativerepresentationofthesameequationintermsoftherealmarginalcostis
oftenfoundintheliterature(see,e.g.,GalíandGertler(1999)).Definingthe(log)average
realmarginalcostasmct =ψ t −ptandnotingthatmct =−µ twecanwrite(17)as:
π
t
=βEt {π
t+1
}+λm(cid:1)ct

62 CHAPTER3
ofpricesetting,theaveragepricemarkupcanbeexpressedas
µ = p −ψ
t t t
=−(w − p)+(a −αn +log(1−α))
t t t t
=−(σy +ϕn)+(a −αn +log(1−α))
(cid:8) t t (cid:9) t (cid:8) t (cid:9)
ϕ+α 1+ϕ
=− σ + y + a +log(1−α) (18)
1−α t 1−α t
where derivation of the second and third equalities make use of the
household’soptimalitycondition(2)andtherelationbetweenaggregate
employmentandoutput(14).
As discussed above, under flexible prices (θ = 0) the average markup
isconstantandequaltothedesiredone,µ.Definingthenatural levelof
output, denoted by yn, as the equilibrium level of output under flexible
t
prices,andevaluating(18)attheflexiblepriceequilibriumyields:
(cid:8) (cid:9) (cid:8) (cid:9)
ϕ+α 1+ϕ
µ=− σ + yn+ a +log(1−α) (19)
1−α t 1−α t
thusimplying
yn =ψ a +ψ (20)
t ya t y
where ψ ≡ −(1−α)(µ−log(1−α)) > 0 and ψ ≡ 1+ϕ . Notice that
y σ(1−α)+ϕ+α ya σ(1−α)+ϕ+α
whenµ=0(perfectcompetition)thenaturallevelofoutputcorresponds
to the equilibrium level of output in the baseline classical monetary
economy analyzed in chapter 2. The presence of market power by firms
has the effect of lowering the average level of output, without affecting
its response to changes in technology. Note also that the natural level
ofoutputisindependentofmonetarypolicy,andinvarianttopreference
shocks{z},twopropertiesthatalsocharacterizedtheequilibriumofthe
t
baselineclassicalmonetarymodelofchapter2.
Subtracting(19)from(18)yields
(cid:8) (cid:9)
ϕ+α
µ(cid:22) =− σ + (y −yn) (21)
t 1−α t t
that is, the markup gap is proportional to the log deviation of output
from its flexible price counterpart. Following convention, the latter
deviationisreferredtoastheoutputgap,anddenotedby(cid:23)y ≡ y −yn.
t t t

THEBASICNEWKEYNESIANMODEL 63
By combining (21) with (17) one can obtain an equation relating
inflationtoitsoneperiodaheadforecastandtheoutputgap
π t =βE t {π t+1 }+κ(cid:23)y t (22)
(cid:19) (cid:20)
where κ ≡ λ σ + ϕ+α . Equation (22) is often referred to as the New
1−α
KeynesianPhillipscurve(orNKPC,forshort),andconstitutesoneofthe
keybuildingblocksofthebasicNewKeynesianmodel.
The second key equation describing the equilibrium of the New
Keynesianmodelcanbeobtainedbyrewriting(13)intermsoftheoutput
gapas
1
(cid:23)y t =− σ (i t −E t {π t+1 }−r t n)+E t {(cid:23)y t+1 } (23)
where rn is the natural rate of interest, that is, the real interest rate
t
that would prevail in the flexible price equilibrium. Under the assumed
processesfor{z}and{a }itisgivenby
t t
rn =ρ−σ(1−ρ )ψ a +(1−ρ )z (24)
t a ya t z t
Henceforth (23) is referred to as the dynamic IS equation (or DIS,
for short). Under the assumption that the effects of nominal rigidities
vanishasymptotically,lim T−→∞E t {(cid:23)y t+T } = 0.Inthatcaseonecansolve
equation(23)forwardtoyieldtheexpression
(cid:1)∞
1
(cid:23)y t =− σ E t {r t+k −r t n +k } (25)
k=0
where r t ≡ i t − E t {π t+1 } is the expected real return on a one period
bond (i.e., the real interest rate). The previous expression emphasizes
the fact that the output gap is inversely related to the sum of current
and anticipated deviations between the real interest rate and its natural
counterpart.
Equations (22) and (23), together with an equilibrium process for
the natural rate rn (given by (24) under the assumptions made above),
t
constitute the nonpolicy block of the basic New Keynesian model. That
block has a simple structure: The NKPC determines inflation given a
pathfortheoutputgap,whereastheDISequationdeterminestheoutput
gap given a path for the (exogenous) natural rate and the actual real
rate, with the latter being a function of the nominal rate and (expected)
inflation.

64 CHAPTER3
Inordertoclosethemodel,thosetwoequationsmustbesupplemented
withoneormoreequationsdetermininghowthenominalinterestratei
t
evolves over time, that is, with a description of how monetary policy
is conducted. Thus, and in contrast with the baseline classical model
analyzed in chapter 2, the presence of sticky prices implies that the
equilibrium path of real variables cannot be determined independently
ofmonetarypolicy.Inotherwords,monetarypolicyisnon-neutral.
In order to illustrate the workings of the basic model just developed,
twoalternativespecificationsofmonetarypolicyareconsideredandtheir
equilibriumimplicationsareanalyzed.
3.4 EQUILIBRIUM DYNAMICS UNDER ALTERNATIVEMONETARY
POLICY RULES
3.4.1 EquilibriumunderaSimpleInterestRateRule
The equilibrium is first analyzed under a simple interest rate rule of the
form
i t =ρ+φ π π t +φ y (cid:22)y t +v t (26)
where (cid:22)y ≡ y − y denotes the deviation of output from its steady
t t
state value, and v is an exogenous monetary policy shock that evolves
t
accordingtothe AR(1)process:
v =ρ v +εv
t v t−1 t
where ρ v ∈ [0,1). A positive (negative) realization of ε t v should be
interpreted as a contractionary (expansionary) monetary policy shock,
leadingtoarise(decline)inthenominalinterestrate,giveninflationand
output.
Coefficients φ π and φ y are chosen by the monetary authority, and
assumedtobenon-negative.Notethatthechoiceoftheinterceptρmakes
theruleconsistentwithazeroinflationsteadystate.Thespecificationof
interest rate rule (26) is broadly consistent with the rule proposed by
Taylor(1993,1999)asagooddescriptionofFedmonetarypolicyunder
the tenure of Chairman Greenspan, and widely known as the “Taylor
rule.”5
5Taylor’soriginalruletakestheform:
i t F =4+1.5(π t −2)+0.5(yt −y t ∗ )
wherei
t
F isthe(annualized)federalfundsrate,π tisyear-on-yearinflation,andy
t
∗istrend
(log)GDP,fittedbymeansofanestimatedlinearfunctionoftime.NotethattheTaylor

THEBASICNEWKEYNESIANMODEL 65
Notethat(26)canberewrittenintermsoftheoutputgapasfollows:
i t =ρ+φ π π t +φ y (cid:23)y t +φ y (cid:22)y t n+v t
where(cid:22)yn ≡ yn−y.
t t
After combining (22), (23), and (26), the equilibrium conditions can
berepresentedbymeansofthefollowingsystemofdifferenceequations,
(cid:24) (cid:25) (cid:24) (cid:25)
(cid:23)y t =A E t {(cid:23)y t+1 } +B u (27)
π t T E t {π t+1 } T t
where
u ≡(cid:22)rn−φ (cid:22)yn−v
t t y t t
=−ψ (φ +σ(1−ρ ))a +(1−ρ )z −v
ya y a t z t t
and
(cid:24) (cid:25) (cid:24) (cid:25)
A ≡(cid:19) σ 1−βφ π ; B ≡(cid:19) 1
T σκ κ +β(σ +φ ) T κ
y
with(cid:19)≡ 1 .
σ+φ +κφ
y π
Given that both the output gap and inflation are non-predetermined
variables,thesolutionto(27)islocallyunique,ifandonlyif,A hasboth
T
eigenvalueswithintheunitcircle.6Undertheassumptionofnon-negative
coefficients (φ π ,φ y ) it can be shown that a necessary and sufficient
conditionforuniquenessisgivenby7
κ(φ π −1)+(1−β)φ y >0 (28)
whichisassumedtohold,unlessstatedotherwise.Aneconomicinterpre-
tationtothepreviousconditionwillbeofferedinchapter4.
Themethodofundeterminedcoefficientscanbeusedinordertosolve
for the economy’s response to different exogenous shocks, under the
assumption of a unique equilibrium. Assume that u follows an AR(1)
t
ruleaboveimplicitlyassumedan2percentannualinflationtargetanda2percentsteady
staterealinterestrate.
6See,e.g.,BlanchardandKahn(1980).
7SeeBullardandMitra(2002)foraproof.

66 CHAPTER3
process, with autoregressive coefficient ρ ∈ [0,1) (this assumption is
u
relaxed below, when the different shocks are analyzed separately). The
stationarysolutionto(27)isconjecturedtobeoftheform(cid:23)y =ψ u and
t y t
π
t
= ψ πu
t
. Imposing the conjectured relations into (27) allows one to
solvefortheundeterminedcoefficientsψ
y
andψ π:
ψ =(1−βρ )(cid:3) (29)
y u u
ψ π =κ(cid:3) u (30)
where(cid:3) ≡ 1 >0.
u (1−βρ u)[σ(1−ρ u)+φ y]+κ(φ π −ρ u)
The following sections make use of the previous result to analyze the
economy’s equilibrium response to different types of exogenous shocks,
whenthecentralbankfollowstheinterestraterule(26).
3.4.1.1 THEEFFECTSOFAMONETARYPOLICYSHOCK
The focus is here on the economy’s response to a shift in v , with
t
a = z = 0 for all t. Note first that neither the natural rate of interest,
t t
rn, nor the natural level of output, yn, depends on the monetary policy
t t
shock,v .Using(29)and(30)andthefactthat ∂ut =−1,itfollowsthat
t ∂v
t
y t =(cid:23)y t =−(1−βρ v)(cid:3) v v t
and
π =−κ(cid:3) v
t v t
where (cid:3) v takes the same form as (cid:3) u above, with ρ u replaced by ρ v (a
similarruleappliesinthedefinitionof(cid:3) below).Thus,bothoutputand
a
inflationdeclineinresponsetoanexogenousincreaseintheinterestrate.
Thesameistrueforemployment,given(14),andtherealwage,given(2).
Onecanuse(23)toobtainanexpressionfortherealinterestrateasa
functionofthemonetarypolicyshock
(cid:22)r
t
=σ(1−ρ v)(1−βρ v)(cid:3)
v
v
t
which is thus shown to increase unambiguously in response to an
exogenousincreaseinthenominalrate.
The response of the nominal interest rate combines both the direct
effectofv andthevariationinducedbyloweroutputandinflation.Itis
t

THEBASICNEWKEYNESIANMODEL 67
givenby
(cid:22) i t =(cid:22)r t +E t {π t+1 }=[σ(1−ρ v)(1−βρ v)−ρ v κ](cid:3) v v t
Note that if the persistence of the monetary policy shock ρ v is
sufficiently high, the nominal rate will decline in response to a rise in
v .Inthatcasethedownwardadjustmentinthenominalrateinducedby
t
the decline in inflation and output more than offsets the direct effect of
ahigherv .Buteveninthatcase,theincreaseinv hasacontractionary
t t
effect on output, because the latter is inversely related to the real rate,
whichgoesupunambiguously,asseenabove.
Finally, one can use (4) to determine the change in the money supply
requiredtobringaboutthedesiredchangeintheinterestrate:
m = p +y −ηi
t t t t
= p t−1 −(cid:3) v[(1−βρ v)(1+ησ(1−ρ v))+(1−ηρ v)κ]v t
The sign of the change in the money supply that is needed to support
the exogenous policy intervention is, in principle, ambiguous. Note,
however,thatdi /dv >0isasufficientconditionforacontractioninthe
t t
money supply in response to an exogenous monetary policy tightening.
It is also a sufficient condition for the presence of a liquidity effect (i.e.,
a negative short-run comovement of the nominal rate and the money
supplyinresponsetoanexogenousmonetarypolicyshock).
The previous analysis can be used to quantify the effects of a mon-
etary policy shock, given numerical values for the model’s parameters.
Abaselinecalibrationofthemodelispresentednext.
Allquantitativeresultsthroughoutthebookarebasedoncalibrations
that take each period in the model to correspond to a quarter. In the
baseline calibration of the model’s preference parameters it is assumed
β = 0.99, which implies a steady state real (annualized) return on
financial assets of about 4 percent. It is also assumed σ = 1 (log utility)
and ϕ = 5 (which implies a Frisch elasticity of labor supply of 0.2),
α = 1/4, and (cid:2) = 9 (implying M = 1.125, i.e., a steady state markup
ofa12.5percent).Thesearevaluesbroadlysimilartothosefoundinthe
business cycle literature. The interest semielasticity of money demand,
η, is set to equal 4.8 In addition it is assumed θ = 3/4, which implies
8ThecalibrationofηisbasedontheestimatesofanOLSregressionof(log)M2inverse
velocityonthe3monthTreasuryBillrate(quarterlyrate,perunit),usingquarterlydata
overtheperiod1960:1–1988:1.Thefocusisonthatperiodbecauseitischaracterizedbya
highlystablerelationshipbetweenvelocityandthenominalrate,asimpliedbythemodel.

68 CHAPTER3
anaveragepricedurationoffourquarters,avalueconsistentwithmuch
of the empirical evidence.9 As to the interest rate rule coefficients, it is
assumed φ π = 1.5 and φ y = 0.5/4, in a way consistent with Taylor’s
original rule.10 Finally, ρ v = 0.5, a setting associated with a moderately
persistentshock.
Figure3.1illustratesthedynamiceffectsofacontractionarymonetary
policyshockonanumber ofmacrovariables.Theshocktakestheform
ofanincreaseof25basispointsinεv,which,intheabsenceofafurther
t
change induced by the response of inflation or the output gap, would
implyanincreaseof100basispointsintheannualizednominalrate,on
impact. The responses of inflation and the two interest rates shown in
figure 3.1 (and in all subsequent figures) are expressed in annual terms,
thatis,theyareobtainedbymultiplyingby4theresponsesofπ ,i ,and
t t
r impliedbythequarterlymodel.
t
Inawayconsistentwiththeanalyticalresultsaboveitisseenthatthe
policy shock generates a decrease in inflation, output (whose response
correspondstothatoftheoutputgap,becausethenaturallevelofoutput
is not affected by the monetary policy shock), employment, and the real
wage. Note that under the baseline calibration the nominal rate goes
up, though by less than its exogenous component—as a result of the
downward adjustment induced by the decline in inflation and output.
Note also that the increase in the real rate is larger than that of the
nominal rate as a result of the decrease in expected inflation. That
persistent increase in the real rate is the factor behind the decline of
consumption and output, as implied by (25), and given the constancy
ofthenaturalrate.
In order to bring about the observed rise in the nominal interest
rate, the central bank must engineer a large short-run reduction in the
moneysupply.Thecalibratedmodelthusdisplaysaliquidityeffect.Note
also that the negative response of the price level to the tightening of
monetary policy builds up gradually, and is much more muted in the
short run than that of the money supply, which instead overshoots its
new permanent plateau. In the long run, however, the price level and
the money experience a permanent decline of identical size, since real
balancesrevertbacktotheirinitiallevel.
Overall, the dynamic responses to a monetary policy shock shown in
figure 3.1 are similar, at least in a qualitative sense, to those estimated
9See,inparticular,theestimatesinGalí,Gertler,andLópez-Salido(2001)andSbordone
(2002),basedonaggregatedataandthediscussionofthemicroevidenceinchapter1.
10See,e.g.,Taylor(1999).Notethatempiricalinterestraterulesaregenerallyestimated
using inflationandinterestratedataexpressedinannualrates.Conversiontoquarterly
ratesrequiresthattheoutputgapcoefficientbedividedby4.

THEBASICNEWKEYNESIANMODEL 69
0 0
–0.1 –0.1
–0.2 –0.2
–0.3 –0.3
–0.4 –0.4
0 5 10 15 0 5 10 15
Output gap Inflation
0 0
–0.1 –0.1
–0.2 –0.2
–0.3 –0.3
–0.4 –0.4
0 5 10 15 0 5 10 15
Output Employment
0 0
–0.5 –0.05
–1 –0.1
–1.5 –0.15
–2 –0.2
0 5 10 15 0 5 10 15
Real wage Price level
0.4 0.8
0.3 0.6
0.2 0.4
0.1 0.2
0 0
0 5 10 15 0 5 10 15
Nominal rate Real rate
0 0.4
–0.2 0.3
–0.4 0.2
–0.6 0.1
–0.8 0
0 5 10 15 0 5 10 15
Money supply v
Figure3.1. DynamicResponsestoaMonetaryPolicyShock:InterestRateRule.
using structural vector autoregressive (VAR) methods, as described in
chapter 1. Nevertheless, and as emphasized in Christiano, Eichenbaum,
and Evans (2005), among others, matching some of the quantitative
features of the empirical impulse responses requires that the basic New
Keynesianmodelbeenrichedinavarietyofdimensions.

70 CHAPTER3
0 0
–0.1 –0.1
–0.2 –0.2
–0.3 –0.3
–0.4 –0.4
0 5 10 15 0 5 10 15
Output gap Inflation
0 0
–0.1 –0.1
–0.2 –0.2
–0.3 –0.3
–0.4 –0.4
0 5 10 15 0 5 10 15
Output Employment
0 0
–0.5 –0.05
–1 –0.1
–1.5 –0.15
–2 –0.2
0 5 10 15 0 5 10 15
Real wage Price level
0 0
–0.2 –0.2
–0.4 –0.4
–0.6 –0.6
–0.8 –0.8
0 5 10 15 0 5 10 15
Nominal rate Real rate
0.6 0
0.4 –0.2
0.2 –0.4
0 –0.6
–0.2 –0.8
0 5 10 15 0 5 10 15
Money supply z
Figure3.2. DynamicResponsestoaDiscountRateShock:InterestRateRule.
3.4.1.2 THEEFFECTSOFADISCOUNTRATESHOCK
Figure3.2displaysthedynamicresponsesofdifferentmacrovariablesto
adiscountfactorshock,intheformofadecreaseinz.Likeinthecaseof
t
the monetary policy shock, the corresponding autoregressive coefficient
is set to ρ = 0.5. The size of the initial shock εz is normalized to −0.5
z t

THEBASICNEWKEYNESIANMODEL 71
percentagepoints,sothat ∂r t n =(1−ρ )εz =−0.25,implyinganincrease
∂εz z t
t
on impact of one percentage point in the (annualized) natural rate of
interest.Adeclineinz shouldbeinterpretedasareductionintheweight
t
thathouseholdsgivetocurrentutilityrelativetofutureutility.Thatshift
in preferences induces a decline in consumption and hence in aggregate
demand.
As shown in figure 3.2, the decline in z leads to a contraction in
t
output, employment, inflation, and the real wage. In fact, and given the
normalization of the size of the shock, the response of those variables is
identical to that describing the effects of a monetary policy tightening,
as shown in figure 3.1. Formally, the reason for this is that (1−ρ )z
z t
and v enter symmetrically (though with opposite sign) in the system
t
(27)describingtheequilibriumdynamicsforinflationandtheoutputgap
under the interest rate rule considered here. Given that z doesn’t affect
t
thenaturallevelofoutputeither,theeffectsonoutput,employment,and
therealwagearealsoidentical.
Discount rate shocks and monetary policy shocks differ in two
respects, however: (i) shifts in the discount factor have an effect on the
natural rate of interest rn, whereas monetary policy shocks don’t (see
t
(24)), and (ii) monetary policy shocks lead to changes in the nominal
interest rate, for any given levels of inflation and output, whereas
discount factor shocks don’t (see (26)). As a result, the effects of the
two shocks on the nominal and real interest rates are very different,
as a comparison of figures 3.1 and 3.2 makes clear. In particular, the
nominal rate falls in response to a negative discount factor shock, due
to the decline in inflation and output. The decline in the nominal rate
dragstherealratedown,giventhesluggishchangeinexpectedinflation.
Thedeclineintherealinterestrate,however,isnotsufficienttoprevent
theoverallcontractionineconomicactivity.Notealsothatthedifferent
responseofthenominalrateisassociatedwithaverydifferentpatternin
theresponseofthemoneysupply,whichnowrisesintheshortrun(due
to the dominant effect of a lower nominal rate), before it declines and
settlesatapermanentlylowerlevel(thesameasthepricelevel,whichin
turncorrespondstothatimpliedbythemonetarypolicyshock).
3.4.1.3 THEEFFECTSOFATECHNOLOGYSHOCK
Next, the effects of exogenous changes in a are considered. Given (27)
t
andtheanalysisofitssolutionabove,itfollowsthat
(cid:23)y =−ψ (φ +σ(1−ρ ))(1−βρ )(cid:3) a
t ya y a a a t

72 CHAPTER3
and
π =−ψ (φ +σ(1−ρ ))κ(cid:3) a
t ya y a a t
where (cid:3) is equal to (cid:3) above, with ρ replacing ρ . Thus, a positive
a u a u
technologyshockhasanunambiguousnegativeeffectontheoutputgap
andinflation.
Outputisnowgivenby
y = (cid:23)y +yn
t t t
=ψ ya κ(φ π −ρ a )(cid:3) a a t
It is easy to check that κ(φ π − ρ a )(cid:3) a ∈ (0,1). Thus, a positive
technology shock always increases output, but by less than its natural
counterpart, thus generating a negative output gap, as seen above. The
responseofemploymentisgivenby
(cid:8) (cid:9)
1
n = (y −a )
t 1−α t t
(cid:24) (cid:25)
= (1−σ)κ(φ π −ρ a ) −(φ +σ(1−ρ ))(1−βρ ) (cid:3) a
σ(1−α)+ϕ+α y a a a t
Hence,thesignoftheresponseofemploymenttoapositivetechnology
shock is in general ambiguous, depending on the configuration of
parameter values, including the interest rate rule coefficients. Note,
however, that σ ≥ 1 is a sufficient condition for a technological
improvement to cause a decline in employment. The same is true if φ
y
is sufficiently large, that is, if the central bank puts enough weight on
output stabilization, even in the face of fluctuations in natural output
resultingfromchangesintechnology.Sucharesponseofemploymentis
consistent with much of the recent empirical evidence on the effects of
technologyshocks.11
Figure 3.3 shows the dynamic response of several macro variables
to a one percent increase in technology, under the baseline calibration
described above, and the assumption of ρ = 0.9. In a way consistent
a
withtheanalysisabove,theoutputgapandinflationareshowntodecline
persistently in response to the positive technology shocks, even though
output itself expands.12 Under the baseline calibration employment
11See,e.g.,Galí(1999)andBasu,Fernald,andKimball(2004),amongothers.Galíand
Rabanal(2004)provideasurveyofthatempiricalevidence.
12Undertheassumedcalibrationϕ
ya
=1,implyingthattheresponseofthenaturallevel
ofoutputcorrespondstothatoftechnology,at.Notethattheresponseofoutputfallsshort
ofthetechnologyresponse.

THEBASICNEWKEYNESIANMODEL 73
0 0
–0.05
–0.5
–0.1
–1
–0.15
–0.2 –1.5
0 5 10 15 0 5 10 15
Output gap Inflation
0.8 0
–0.1
0.6 –0.2
–0.3
0.2 –0.4
0 5 10 15 0 5 10 15
Output Employment
0 0
–0.2
–1
–0.4
–2
–0.6
–0.8 –3
0 5 10 15 0 5 10 15
Real wage Price level
0 0
–0.1
–0.5
–0.2
–1
–0.3
–1.5 –0.4
0 5 10 15 0 5 10 15
Nominal rate Real rate
2 1.5
0 1
–2 0.5
–4 0
0 5 10 15 0 5 10 15
Money supply a
Figure3.3. DynamicResponsestoaTechnologyShock:InterestRateRule.
experiences a large and persistent decline. Thus, technology shocks
generateanegativecomovementbetweenoutputandemployment,which
contrasts with the large and positive unconditional correlation between
the cyclical components of output and employment (or work hours)

74 CHAPTER3
observedinthedata,butisconsistentwiththenegativeestimatesofthat
correlationconditionalontechnologyshocks.13
Thenominalinterestrategoesdownsubstantially,duetothedominant
influence of lower inflation in shaping the central bank’s response. As a
result, the real rate also declines, but given the response of the output
gap (and (25)) we can infer that such decline is not sufficient to match
that of its natural rate counterpart. Finally, note that the money supply
increasesintheshortruninordertosupportthelowernominalrateand
to accommodate the increase in money demand resulting from higher
output. Over time, however, those two requirements vanish, while the
permanently lower price level requires a permanent reduction in the
quantityofmoneyincirculation,asshowninfigure3.3.
3.4.2 EquilibriumunderanExogenousMoneySupply
Next the equilibrium dynamics of the basic New Keynesian model are
analyzed under the assumption of an exogenous path for the growth
rate of the money supply, (cid:21)m. As discussed in chapter 2, the fact that
t
the policy rule is specified in terms of the money supply requires that
the money demand equation (4) is included in the set of conditions
needed to solve for the model’s equilibrium (i.e., beyond its usefulness
to back out the quantity of money that supports a given interest rate
policy,asintheprevioussubsection).
As a preliminary step, it is useful to rewrite money demand condition
intermsoftheoutputgap
l =(cid:23)y −ηi +yn (31)
t t t t
wherel ≡m −p denotesrealbalances.Substitutingthelatterequation
t t t
into(23)toeliminatetheinterestrateyields
(1+ση)(cid:23)y t =σηE t {(cid:23)y t+1 }+(cid:22) l t +ηE t {π t+1 }+η(cid:22)r t n−(cid:22)y t n (32)
where,asusual,a“^”symbolontopofavariablereferstodeviationsof
thelatterfromsteadystate.
Notealsothatrealbalancesarerelatedtoinflationandmoneygrowth
throughtheidentity
(cid:22) l t−1 =(cid:22) l t +π t −(cid:21)m t (33)
13SeeGalí(1999).

THEBASICNEWKEYNESIANMODEL 75
Hence, the equilibrium dynamics for real balances, output gap, and
inflation are described by equations (32) and (33) together with the
NKPCequation(22).Theycanbesummarizedcompactlybythesystem
     
(cid:23)y t E t {(cid:23)y t+1 } (cid:22)r t n
     
A M,0  π t =A M,1 E t {π t+1 }+B M  (cid:22)y t n  (34)
(cid:22) l t−1 (cid:22) l t (cid:21)m t
where
     
1+ση 0 0 ση η 1 η −1 0
A M,0 ≡ −κ 1 0  ; A M,1 ≡ 0 β 0  ; B M ≡ 0 0 0 
0 −1 1 0 0 1 0 0 −1
and with (cid:22)rn and (cid:22)yn defined as in (24) and (20) as a function of the
t t
exogenoustechnologyanddiscountfactorshocks.
Thesystemabovehasonepredeterminedvariable(l t−1 )andtwonon-
predetermined variables ((cid:23)y and π ). Accordingly, a stationary solution
t t
will exist and be unique, if and only if, A M ≡ A − M 1 ,0 A M,1 has two
eigenvalues inside and one outside (or on) the unit circle. The latter
condition can be shown to be always satisfied so, in contrast with the
interest rate rule discussed above, the equilibrium is always determined
underanexogenouspathforthemoneysupply.14
Nexttheequilibriumresponsesoftheeconomytodifferentexogenous
shocksareexamined.
3.4.2.1 THEEFFECTSOFAMONETARYPOLICYSHOCK
In order to illustrate how the economy responds to an exogenous shock
tothemoneysupply,assumethatitsgrowthrate(cid:21)m followstheAR(1)
t
process
(cid:21)m t =ρ m (cid:21)m t−1 +ε t m (35)
whereρ ∈[0,1)and{εm}iswhitenoise.
m t
The economy’s response to a monetary policy shock can be obtained
bydeterminingthestationarysolutiontothedynamicalsystemconsisting
of (34) and (35) tracing the effects of a shock to εm (while setting
t
(cid:22)rn = (cid:22)yn = 0, for all t).15 In doing so, it is assumed that ρ = 0.5,
t t m
14 That result is based on numerical analysis of the eigenvalues for a broad range of
calibrationsofthemodel’sparametervalues.
15See,e.g.,BlanchardandKahn(1980)foradescriptionofasolutionmethod.

76 CHAPTER3
0.4 0.8
0.3 0.6
0.2 0.4
0.1 0.2
0 0
0 5 10 15 0 5 10 15
Output gap Inflation
0.4 0.4
0.3 0.3
0.2 0.2
0.1 0.1
0 0
0 5 10 15 0 5 10 15
Output Employment
3 0.5
0.4
2
0.3
1
0.2
0 0.1
0 5 10 15 0 5 10 15
Real wage Price level
0.2 0
0.15 –0.1
0.1 –0.2
0.05 –0.3
0 –0.4
0 5 10 15 0 5 10 15
Nominal rate Real rate
0.5 1.5
0.4 1
0.3 0.5
0.2 0
0 5 10 15 0 5 10 15
Money supply dm
Figure3.4. DynamicResponsestoaMonetaryPolicyShock:MoneySupply
Rule.
a value roughly consistent with the first-order autocorrelation of money
growthinpostwarU.S.data.
Figure 3.4 displays the dynamic responses of several variables of
interest to an expansionary monetary policy shock that takes the form
of a positive realization of εm of size 0.25. That impulse corresponds
t

THEBASICNEWKEYNESIANMODEL 77
to a one percent increase, on impact, in the annualized rate of money
growth.Thesluggishadjustmentofpricesimpliesthatrealbalancesrise
in response to the increase in the money supply. As a result, clearing
of the money market requires either a rise in output and/or a decline in
thenominalrate.Underthecalibrationconsideredhere,output(andthe
outputgap,sincenaturaloutputisunaffected)increasesbyaboutathird
ofapercentagepointonimpact,afterwhichitslowlyrevertsbacktoits
initial level. The nominal rate, however, shows a slight increase. Hence,
andincontrastwiththecaseoftheinterestrateruleconsideredabove,a
liquidityeffectdoesnotemergehere.Note,however,thattheriseinthe
nominal rate does not prevent the real rate from declining persistently
(due to higher expected inflation), leading in turn to an expansion in
aggregate demand and output, as implied by (25), and, as a result, a
persistentriseininflation,whichfollowsfrom(22).
Itisworthnotingthattheabsenceofaliquidityeffectisnotanecessary
feature of the exogenous money supply regime considered here, but
instead a consequence of the calibration used. To see this, note that one
cancombineequations(4)and(23)toobtainthedifferenceequation
η ρ σ −1
i t = 1+η E t {i t+1 }+ 1+ m η (cid:21)m t + 1+η E t {(cid:21)y t+1 }
whoseforwardsolutionyields
(cid:8) (cid:9)
ρ σ −1 (cid:1)∞ η k
i t = 1+η(1 m −ρ ) (cid:21)m t + 1+η 1+η E t {(cid:21)y t+1+k }
m k=0
Note that when σ = 1, as in the assumed baseline calibration, the
nominal rate always comoves positively with money growth. Neverthe-
less,andgiventhatquitegenerallythesummationtermontheright-hand
side will be negative (since for most calibrations output tends to adjust
monotonically to its original level after the initial increase), a liquidity
effect emerges given a value for σ sufficiently above one combined with
asufficientlylowvalueforρ .16
m
3.4.2.2 THEEFFECTSOFADISCOUNTRATESHOCK
Figure 3.5 displays the effects of a contractionary discount rate shock,
identicaltotheoneanalyzedabove,butnowundertheassumptionofan
exogenousmoneygrowthrule,implyingtheabsenceofaresponseinthe
moneysupplytotheshock,thatis,(cid:21)m =0forallt.
t
16SeeGalí(2003)foradetailedanalysis.

78 CHAPTER3
0.1 0.1
0 0
–0.1 –0.1
–0.2 –0.2
–0.3 –0.3
0 5 10 15 0 5 10 15
Output gap Inflation
0.1 0.4
0 0.2
–0.1 0
–0.2 –0.2
–0.3 –0.4
0 5 10 15 0 5 10 15
Output Employment
1 0
0 –0.02
–1 –0.04
–2 –0.06
–3 –0.08
0 5 10 15 0 5 10 15
Real wage Price level
0 0
–0.1 –0.1
–0.2 –0.2
–0.3 –0.3
–0.4 –0.4
0 5 10 15 0 5 10 15
Nominal rate Real rate
1 0
0.5 –0.2
0 –0.4
–0.5 –0.6
–1 –0.8
0 5 10 15 0 5 10 15
Money supply z
Figure3.5. DynamicResponsestoaDiscountRateShock:MoneySupplyRule
Note that the dynamic effects on output and employment are, at first
sight, qualitatively similar to those derived under an interest rate rule.
But this is not the case, strictly speaking. The reason is simple: under
monetary targeting the price level returns to its original value, which
requiresthatinflationeventuallyturnspositiveafteritsinitialdecline,as
showninfigure3.5.Itfollowsthatoutput(aswellasemploymentandthe

THEBASICNEWKEYNESIANMODEL 79
realwage,asaresult)mustalsoovershootitsinitiallevel,whichinturn
requires that the real rate eventually stays below its natural counterpart
(noneoftheseeffectscanbeeasilyseenintheFigure,however).
Intuitively, the reason for the different effects of the discount rate
shock under the monetary targeting rule is that the latter is effectively
equivalent to an interest rate rule that targets the price level (as op-
posed to inflation). To see this, note that we can rewrite (4) (ignoring
constants)as
(cid:8) (cid:9) (cid:8) (cid:9)
1 1
i t = η (p t −m t−1 )+ η (cid:22)y t +v t
(cid:8) (cid:9) (cid:8) (cid:9) (cid:8) (cid:9)
1 1 1
= η (p t−1 −m t−1 )+ η π t + η (cid:22)y t +v t
where v ≡ −(1/η)(cid:21)m. Note that the previous rule is of the same
t t
formas(26),withtheadditionalterminvolving(p t−1 −m t−1 )appended.
Thus, and in the absence of a change in the money supply, the interest
rate will adjust endogenously to (lagged) deviations between the price
level from the implicit price level target which is given by m t−1 . That
systematic response guarantees the stationarity of the price level in
response to any shock (other than a shock to the growth rate of money
itself).
3.4.2.3 THEEFFECTSOFATECHNOLOGYSHOCK
Finally, the effects of a technology shock under an exogenous money
supplyareanalyzednext.Onceagain,assumethetechnologyparameter
a follows the stationary process given by (6). In a way consistent with
t
theassumptionofexogenousmoney,itisassumedthat(cid:21)m =0forallt
t
forthepurposeofthepresentexercise.
Figure3.6displaysthedynamicresponsestoaonepercentincreasein
the technology. A comparison with the responses shown in figure 3.2
(corresponding to the analogous exercise under an interest rate rule)
reveals some similarities: In both cases the output gap (and, hence,
inflation) displays a negative response to the technology improvement,
as a result of output failing to increase as much as its natural level.
Note, however, that in the case of exogenous money the gap between
output and its natural level is much larger, which also explains the
larger decline in employment. This is due to the upward response of
the real rate implied by the unchanged money supply, which contrasts
withitsdecline(inresponsetothenegativeresponseofinflationandthe
output gap) under the interest rate rule. Because the natural real rate
also declines in response to the positive technology shock (in order to

80 CHAPTER3
supportthetransitoryincreaseinoutputandconsumption),theresponse
of interest rates generated under the exogenous money regime becomes
highly contractionary, relative to the equilibrium under flexible prices.
As in the case of a discount rate shock analyzed above (but in contrast
with the response to a technology shock under the simple interest rate
rule) the price level is stationary and returns gradually to its original
levelafteritsinitialdecline,whichrequiresthatinflationeventuallyturn
positive.
The previous simulations have served several goals. First, they have
helped illustrate the workings of the New Keynesian model, that is,
how the model can be used to answer some specific questions about
the behavior of the economy under different assumptions regarding the
monetary policy rule in place. Second, under a plausible calibration, it
was seen how the simulated responses to some shocks (monetary policy
shocks, in particular) display notable similarities (at least qualitative)
with the empirical evidence on their effects. Third, the previous analysis
has made clear that monetary policy in the New Keynesian model can
havelargeandpersistenteffectsonbothrealandnominalvariables.The
latter feature leads one to raise a natural question, which is the focus of
thenextchapter:Howshouldmonetarypolicybeconducted?
3.5 NOTES ON THELITERATURE
Early examples of microfounded monetary models with monopolistic
competitionandstickypricescanbefoundinAkerlofandYellen(1985),
Mankiw (1985), Blanchard and Kiyotaki (1987), and Ball and Romer
(1990).
An early version and analysis of the baseline New Keynesian model
can be found in Yun (1996), which used a discrete-time version of the
staggeredprice-settingmodeloriginallydevelopedinCalvo(1983).King
and Wolman (1996) provide a detailed analysis of the steady state and
dynamic properties of that model. King and Watson (1996) compare its
predictionsregardingthecyclicalpropertiesofmoney,interestrates,and
priceswiththoseofflexiblepricemodels.Woodford(1996)incorporates
a fiscal sector in the model and analyzes its properties under a non-
Ricardianfiscalpolicyregime.
AninflationequationidenticaltotheNewKeynesianPhillipscurvecan
be derived under the assumption of quadratic costs of price adjustment,
as shown in Rotemberg (1982). Hairault and Portier (1993) developed
andanalyzedanearlyversionofamonetarymodelwithquadraticcosts
of price adjustment and compared its second-moment predictions with
thoseoftheFrenchandU.S.economies.

THEBASICNEWKEYNESIANMODEL 81
0.5 0.5
0
0
–0.5
–0.5
–1
–1 –1.5
0 5 10 15 0 5 10 15
Output gap Inflation
0.8 0.5
0.6 0
0.4 –0.5
0.2 –1
0 5 10 15 0 5 10 15
Output Employment
2 –0.2
0 –0.3
–2 –0.4
–4 –0.5
–6 –0.6
0 5 10 15 0 5 10 15
Real wage Price level
5 1
0
0.5
–5
0
–10
–15 –0.5
0 5 10 15 0 5 10 15
Nominal rate Real rate
1 1.5
0.5
1
0
0.5
–0.5
–1 0
0 5 10 15 0 5 10 15
Money supply a
Figure3.6. DynamicResponsestoaTechnologyShock:MoneySupplyRule.
The New Keynesian Phillips curve derived in the main text is based
on a log-linearization of the optimal price setting condition and the law
of motion for the aggregate price level around the zero inflation steady
state.Ascari(2004),AscariandRopele(2009),andCogleyandSbordone
(2008)analyzetheconsequencesforinflationdynamicsofasteadystate
withnonzeroinflation.

82 CHAPTER3
Two main alternatives to the Calvo random price duration model
can be found in the literature. The first one is given by staggered
price-setting models with a deterministic price duration, originally pro-
posed by Taylor (1980) in the context of a non-microfounded model.
AmicrofoundedversionoftheTaylormodelcanbefoundinChari,Kehoe,
and McGrattan (2000), who analyzed the output effects of exogenous
monetary policy shocks. An alternative price-setting structure is given
by state dependent models in which the timing of price adjustments is
influencedbythestateoftheeconomy.Aquantitativeanalysisofastate
dependent pricing model can be found in Dotsey, King, and Wolman
(1999) and, more recently, in Golosov and Lucas (2007), Gertler and
Leahy (2008), and Midrigan (2011). Klenow and Kryvtsov (2008) and
Nakamura and Steinsson (2008) examine the ability of state dependent
modelstoaccountforthepricepatternsfoundinthemicroevidence.
The empirical performance of the New Keynesian Phillips curve
has always been controversial. An early critical assessment can be
found in Fuhrer and Moore (1995). Mankiw and Reis (2002) give a
quantitative review of the perceived shortcomings of the NKPC and
propose an alternative price-setting structure based on the assumption
of sticky information. Galí and Gertler (1999), Sbordone (2002), and
Galí, Gertler, and López-Salido (2001) provide favorable evidence of
the empirical fit of the equation relating inflation to marginal costs,
and discuss the difficulties in estimating or testing the NKPC given the
unobservability of the output gap. Mavroeidis, Plagborg-Moller, and
Stock (2013) overview the empirical literature on the NKPC, focusing
ontheproblemofweakidentificationanditsconsequences.
Taylor (1993, 1999) put forward the notion that a simple interest
rate rule that responds systematically to inflation and detrended output
approximates fairly well, when its coefficients are chosen appropriately,
the path of the federal funds rate in the Greenspan years. Empirical
evidenceonthestabilityoftheTaylorruleovertimeandacrossdifferent
countries can be found in Clarida, Galí, and Gertler (1998, 2000) and
Orphanides(2003),amongothers.
Rotemberg and Woodford (1999) and Christiano, Eichenbaum, and
Evans(1999,2005)provideempiricalevidenceontheeffectsofmonetary
policyshocks,anddiscussanumberofmodificationsofthebaselineNew
Keynesian model aimed at improving the model’s ability to match the
estimatedimpulseresponses.
Evidence on the effects of technology shocks and their implications
for the relevance of alternative models can be found in Galí (1999)
and Basu, Fernald, and Kimball (2004), among others. Recent evidence
as well as alternative interpretations are surveyed in Galí and Rabanal
(2004).

THEBASICNEWKEYNESIANMODEL 83
APPENDIX
3.1 OPTIMALALLOCATIONOFCONSUMPTIONEXPENDITURES
TheproblemofmaximizationofC foranygivenexpenditurelevel
t
(cid:3)
1
X ≡ P(i)C(i)di
t t t
0
canbeformalizedbymeansoftheLagrangian
(cid:2) (cid:4) (cid:2) (cid:4)
(cid:3) (cid:2) (cid:3)
1 (cid:2)−1 1
L= C
t
(i)1−1 (cid:2)di −λ P
t
(i)C
t
(i)di −X
t
0 0
Theimpliedfirst-orderconditionsare
C t (i) −1 (cid:2)C t 1 (cid:2) =λP t (i)
foralli ∈[0,1].Thus,foranytwogoods(i, j),
(cid:8) (cid:9)
−(cid:2)
P(i)
C(i)=C(j) t
t t
P(j)
t
which can be substituted into the expression for consumption expendi-
turestoyield
(cid:8) (cid:9)
−(cid:2)
P(i) X
C(i)= t t
t
P P
t t
for all i ∈ [0,1]. The latter condition can then be substituted into the
definitionofC toobtain
t
(cid:3)
1
P(i)C(i)di = PC
t t t t
0
Combiningthetwopreviousequationsyieldsthedemandschedule
(cid:8) (cid:9)
−(cid:2)
P(i)
C(i)= t C
t t
P
t

84 CHAPTER3
3.2 AGGREGATEPRICELEVELDYNAMICS
Let S(t) ⊂ [0,1] represent the set of firms not reoptimizing their posted
priceinperiodt.Usingthedefinitionoftheaggregatepricelevelandthe
factthatallfirmsresettingpriceswillchooseanidenticalprice P∗,
t
(cid:24)(cid:3) (cid:25)
1
P t = P t−1 (i)1−(cid:2) di +(1−θ)(P t ∗ )1−(cid:2)
1−(cid:2)
S(t)
!
= θ(P
t−1
)1−(cid:2) +(1−θ)(P
t
∗ )1−(cid:2) 1− 1 (cid:2)
where the second equality follows from the fact that the distribution
of prices among firms not adjusting in period t corresponds to the
distribution of effective prices in period t −1, though with total mass
reducedtoθ.
Dividingbothsidesby P t−1 ,
(cid:8) (cid:9)
P∗ 1−(cid:2)
(cid:12)1−(cid:2) =θ +(1−θ) t (36)
t P t−1
3.3 FIRM’SOBJECTIVEFUNCTION
Thevalueofafirminperiodt,expressedintermsofcurrentconsumption
isgivenby
(cid:1)∞
V t (i)= E t {(cid:3) t,t+k (D t+k (i)/P t+k )}
k=0
where D(i)≡ P(i)Y(i)−C (Y(i)).
t t t t t
Notethatforafirmresettingitspriceinperiodt,
E t {(cid:3) t,t+k (D t+k (i)/P t+k )}=θkE t {(cid:3) t,t+k (D t+k|t /P t+k )}
(cid:1)k
+(1−θ) θk−hE t {(cid:3) t,t+k (D t+k|t+h /P t+k )}
h=1
(37)
where D t+k|t ≡ P t ∗Y t+k|t − C t+k (Y t+k|t ) denotes period t + k dividends
conditional on the price having been last reset in period t. Note that
thesecondtermontheright-handsideof(37)isindependentof P∗ since
t

THEBASICNEWKEYNESIANMODEL 85
itinvolvesstatesofnatureforwhichthepricehasbeenresetatleastonce
afterperiodt.
Thus,thevalueofafirmresettingitspriceinperiodt isgivenby
(cid:1)∞
V t|t = θkE t {(cid:3) t,t+k (D t+k|t /P t+k )}+ϒ t
k=0
where ϒ is a term independent of P∗ and hence can be ignored when
t t
choosingthelatter,asreflectedintheobjectivefunctioninthemaintext.
3.4 PRICEDISPERSION
Let (cid:22)p(i)≡ p(i)− p.Noticethat,
t t t
(cid:8) (cid:9)
P(i)
1−(cid:2)
t =exp[(1−(cid:2))(cid:22)p(i)]
t
P
t
(1−(cid:2))2
=1+(1−(cid:2))(cid:22)p(i)+ (cid:22)p(i)2
t t
2
(cid:10) (cid:11)
(cid:7) 1−(cid:2)
Note that from the definition of P, 1 = 1 Pt(i) di. A second-
t 0 Pt
orderapproximationtothisexpressionthusimplies
(cid:2)−1
E{(cid:22)p(i)}= E{(cid:22)p(i)2}
i t i t
2
(cid:10) (cid:11)
− (cid:2)
Inaddition,asecond-orderapproximationto Pt(i) 1−α yields
Pt
(cid:8) (cid:9) (cid:8) (cid:9)
P
t
(i) − 1− (cid:2) α
=1−
(cid:2)
(cid:22)p(i)+
1 (cid:2) 2
(cid:22)p(i)2
P 1−α t 2 1−α t
t
Combiningthetwopreviousresults,itfollowsthat
(cid:3) (cid:8) (cid:9) (cid:8) (cid:9)
1 P
t
(i) − 1− (cid:2) α
di =1+
1 (cid:2) 1
E{(cid:22)p(i)2}
P 2 1−α (cid:15) i t
0 t
(cid:8) (cid:9)
1 (cid:2) 1
=1+ var {p(i)}
2 1−α (cid:15) i t

86 CHAPTER3
where (cid:15) ≡ 1−α , and where the last equality follows from the
1−α+α(cid:2)
observationthat,uptosecondorder,
(cid:3) (cid:3)
1 1
(p(i)− p)2 di (cid:11) (p(i)−E{p(i)})2 di
t t t i t
0 0
≡var {p(i)}
i t
Finally, using the definition of d and up to a second-order
t
approximation,
(cid:3) (cid:8) (cid:9)
d ≡(1−α)log
1 P
t
(i) − 1− (cid:2) α
di (cid:11)
(cid:2)
var {p(i)}
t P 2(cid:15) i t
0 t
REFERENCES
Akerlof, George, and Janet Yellen (1985): “A Near-Rational Model of the
BusinessCyclewithWageandPriceInertia,”QuarterlyJournalofEconomics
100(Supplement),823–838.
Ascari,Guido(2004):“StaggeredPricesandTrendInflation:SomeNuisances,”
ReviewofEconomicDynamics7(3),642–667.
Ascari, Guido, and Tiziano Ropele (2009): “Trend Inflation, the Taylor Prin-
ciple and Indeterminacy,” Journal of Money, Credit and Banking 41(8),
1557–1584.
Ball, Laurence, and David Romer (1990): “Real Rigidities and the Non-
NeutralityofMoney,”ReviewofEconomicStudies57,183–203.
Basu, Susanto, John Fernald, and Miles Kimball (2004): “Are Technol-
ogy Improvements Contractionary?,” American Economic Review 96(5),
1418–1448.
Blanchard, Olivier J., and Charles Kahn (1980): “The Solution of Linear
Difference Equations under Rational Expectations,” Econometrica 48(5),
1305–1311.
Blanchard, Olivier J., and Nobuhiro Kiyotaki (1987): “Monopolistic Competi-
tionandtheEffectsofAggregateDemand,”AmericanEconomicReview77(4),
647–666.
Bullard, James, and Kaushik Mitra (2002): “Learning about Monetary Policy
Rules,”JournalofMonetaryEconomics49(6),1005–1129.
Calvo,Guillermo(1983):“StaggeredPricesinaUtilityMaximizingFramework,”
JournalofMonetaryEconomics12(3),383–398.
Chari, V. V., Patrick J. Kehoe, and Ellen R. McGrattan (2000): “Sticky Price
ModelsoftheBusinessCycle:CantheContractMultiplierSolvethePersistence
Problem?,”Econometrica68(5),1151–1180.
Christiano, Lawrence J., Martin Eichenbaum, and Charles L. Evans (1999):
“Monetary Policy Shocks: What Have We Learned and to What End?,” in
J.B.TaylorandM.Woodford,eds.,HandbookofMacroeconomics,vol.1A,
65–148.Elsevier-NorthHolland(Amsterdam).

THEBASICNEWKEYNESIANMODEL 87
Christiano, Lawrence J., Martin Eichenbaum, and Charles L. Evans (2005):
“NominalRigiditiesandtheDynamicEffectsofaShocktoMonetaryPolicy,”
JournalofPoliticalEconomy113(1),1–45.
Clarida,Richard,JordiGalí,andMarkGertler(1998):“MonetaryPolicyRules
in Practice: Some International Evidence,” European Economic Review 42,
1033–1067.
Clarida,Richard,JordiGalí,andMarkGertler(2000):“MonetaryPolicyRules
andMacroeconomicStability:EvidenceandSomeTheory,”QuarterlyJournal
ofEconomics105(1),147–180.
Cogley, Timothy, and Argia Sbordone (2008): “Trend Inflation, Indexation
and Inflation Persistence in the New Keynesian Phillips Curve,” American
EconomicReview98(5),2101–2126.
Dotsey, Michael, Robert G. King, and Alexander L. Wolman (1999): “State
Dependent Pricing and the General Equilibrium Dynamics of Money and
Output,”QuarterlyJournalofEconomics114(2),655–690.
Fuhrer,JeffreyC.,andGeorgeR.Moore(1995):“InflationPersistence,”Quar-
terlyJournalofEconomics440(2),127–159.
Galí, Jordi (1999): “Technology, Employment, and the Business Cycle: Do
Technology Shocks Explain Aggregate Fluctuations?,” American Economic
Review89(1),249–271.
Galí, Jordi (2003): “New Perspectives on Monetary Policy, Inflation, and the
Business Cycle,” in M. Dewatripont, L. Hansen, and S. Turnovsky, eds.,
Advances in Economics and Econometrics, vol. 3, 151–197, Cambridge
UniversityPress,Cambridge.
Galí, Jordi, and Mark Gertler (1999): “Inflation Dynamics: A Struc-
tural Econometric Analysis,” Journal of Monetary Economics 44(2),
195–222.
Galí,Jordi,MarkGertler,andDavidLópez-Salido(2001):“EuropeanInflation
Dynamics,”EuropeanEconomicReview45(7),1237–1270.
Galí, Jordi, and Pau Rabanal (2004): “Technology Shocks and Aggregate
Fluctuations:HowWellDoestheRBCModelFitPostwarU.S.Data?,”NBER
MacroeconomicsAnnual2004,225–288.
Gertler, Mark, and John Leahy (2008): “A Phillips Curve with an Ss Founda-
tion,”JournalofPoliticalEconomy116(3),533–572.
Golosov, Mikhail, and Robert E. Lucas (2007): “Menu Costs and Phillips
Curves,”JournalofPoliticalEconomy115(2),171–199.
Hairault, Jean-Olivier, and Franck Portier (1993): “Money, New Keynesian
Macroeconomics,andtheBusinessCycle,”EuropeanEconomicReview37(8),
33–68.
King,RobertG.,andMarkWatson(1996):“Money,Prices,InterestRates,and
theBusinessCycle,”ReviewofEconomicsandStatistics58(1),35–53.
King,RobertG.,andAlexanderL.Wolman(1996):“InflationTargetinginaSt.
LouisModelofthe21stCentury,”FederalReserveBankofSt.LouisReview
78(3),83–107.
Klenow, Peter J., and Oleksiy Kryvtsov (2008): “Time-Dependent or State-
Dependent Pricing: Does It Matter for Recent U.S. Inflation?,” Quarterly
JournalofEconomics123(3),863–904.

88 CHAPTER3
Mankiw, Gregory (1985): “Small Menu Costs and Large Business Cycles:
A Macroeconomic Model of Monopoly,” Quarterly Journal of Economy
100(2),529–539.
Mankiw, N. Gregory, and Ricardo Reis (2002): “Sticky Information vs. Sticky
Prices: A Proposal to Replace the New Keynesian Phillips Curve,” Quarterly
JournalofEconomics117(4),1295–1328.
Mavroeidis, Sophocles, Mikkel Plagborg-Moller, and James Stock (2013):
“EmpiricalEvidenceonInflationExpectationsintheNewKeynesianPhillips
curve,”unpublishedmanuscript.
Midrigan, Virgiliu (2011): “Menu Costs, Multi-product Firms, and Aggregate
Fluctuations,”Econometrica79(4),1139–1180.
Nakamura,Emi,andJónSteinsson(2008):“FiveFactsaboutPrices:AReeval-
uation of Menu Cost Models,” Quarterly Journal of Economics 123(4),
1415–1464.
Orphanides, Athanasios (2003): “The Quest for Prosperity without Inflation,”
JournalofMonetaryEconomics50(3),633–663.
Rotemberg, Julio (1982): “Monopolistic Price Adjustment and Aggregate Out-
put,”ReviewofEconomicStudies49,517–531.
Rotemberg, Julio, and Michael Woodford (1999): “Interest Rate Rules in an
Estimated Sticky Price Model,” in J. B. Taylor, ed., Monetary Policy Rules,
57–119,UniversityofChicagoPress,Chicago.
Sbordone,Argia(2002):“PricesandUnitLaborCosts:TestingModelsofPricing
Behavior,”JournalofMonetaryEconomics45(2),265–292.
Taylor,John(1980):“AggregateDynamicsandStaggeredContracts,”Journalof
PoliticalEconomy88(1),1–24.
Taylor, John B. (1993): “Discretion versus Policy Rules in Practice,” Carnegie-
RochesterSeriesonPublicPolicy39,195–214.
Taylor,JohnB.(1999):“AHistoricalAnalysisofMonetaryPolicyRules,”inJ.B.
Taylor,ed.,MonetaryPolicyRules,317–341,UniversityofChicago,Chicago.
Woodford,Michael(1996):“ControlofthePublicDebt:ARequirementforPrice
Stability,”NBERworkingpaper#5684.
Yun, Tack (1996): “Nominal Price Rigidity, Money Supply Endogeneity, and
BusinessCycles,”JournalofMonetaryEconomics37(2),345–370.
EXERCISES
3.1. Interpreting discrete-time records of data on price adjustment
frequency
Suppose firms operate in continuous time, with the pdf for
the duration of the price of an individual good being f(t) =
φexp(−φt),wheret ∈R+ isexpressedinmonthunits.
a. Show that the implied instantaneous probability of a price
changeisconstantovertimeandgivenbyφ.

THEBASICNEWKEYNESIANMODEL 89
b. What is the mean duration of a price? What is the median
duration?Whatistherelationshipbetweenthetwo?
c. Suppose that the prices of individual goods are recorded once
a month (say, on the first day, for simplicity). Let λ denote
t
the fraction of items in a given goods category whose price in
month t is different from that recorded in month t−1 (Note:
of course, the price may have changed more than once since
the previous record.) How would you go about estimating
parameterφ?
d. Giveninformationonmonthlyfrequenciesofpriceadjustment,
howwouldyougoaboutcalibratingparameterθ inaquarterly
Calvomodel?
3.2. Introducing government purchases in the basic New Keynesian
model
Assume that the government purchases quantity G(i) of good i,
(cid:10) (cid:7) (cid:11) (cid:2) t
for all i ∈ [0,1]. Let G t ≡ 0 1 G t (i)1−1 (cid:2) di (cid:2)−1 denote an index
ofpublicconsumption,whichthegovernmentseekstomaximize
(cid:7)
1
foranylevelofexpenditures P(i)G(i)di.Assumegovernment
0 t t
expendituresarefinancedbymeansoflump-sumtaxes.
a. Deriveanexpressionfortotaldemandfacingfirmi.
b. Derive a log-linear aggregate goods market clearing condition
that is valid around a steady state with a constant public
consumptionshare S ≡ G.
G Y
c. Derivethecorrespondingexpressionforaveragerealmarginal
costasafunctionofaggregateoutput,governmentpurchases,
and technology and provide some intuition for the effect of
governmentpurchases.
d. How is the equilibrium relationship linking interest rates
to current and expected output affected by the presence of
governmentpurchases?
3.3. Governmentpurchasesandstickyprices
Consider a model economy with the following equilibrium con-
ditions. The household’s log-linearized Euler equation takes the
form
1
c t =− σ (i t −E t {π t+1 }−ρ)+E t {c t+1 }
where c t is consumption, i t is the nominal rate, and π t+1 ≡
p t+1 − p t is the rate of inflation between t and t+1 (Note: as in

90 CHAPTER3
thetext,lowercaselettersdenotethelogsoftheoriginalvariable.)
Thehousehold’slog-linearizedlaborsupplyisgivenby
w − p =σc +ϕn
t t t t
wherew denotesthenominalwage, p isthepricelevel,andn is
t t t
employment.
Firms’technologyisgivenby
y =n
t t
Thetimebetweenpriceadjustmentsfollowsageometricdistribu-
tion,whichgivesrisetoaninflationequation
π
t
=βE
t
{π
t+1
}+κ(cid:23)y
t
where (cid:23)y ≡ y − yn is the output gap (with yn representing the
t t t t
naturallevelofoutput).Assumethatintheabsenceofconstraints
on price adjustment firms would set a price equal to a constant
markupovermarginalcostgivenbyµ(inlogs).
Suppose that the government purchases a fraction τ of the
t
output of each good, with τ varying exogenously. Government
t
purchasesarefinancedthroughlump-sumtaxes.
a. Derive a log-linear version of the goods market clearing
conditionoftheform y =c +g ,whereg ≡−log(1−τ ).
t t t t t
b. Determine the behavior of the natural level of output yn as
t
a function of g and discuss the mechanism through which a
t
fiscalexpansionleadstoanincreaseinoutputwhenpricesare
flexible.
c. Assume that {g } follows a simple AR(1) process with autore-
t
gressivecoefficientρ ∈[0,1).DerivethedynamicISequation
g
1
(cid:23)y t = E t {(cid:23)y t+1 }− σ (i t −E t {π t+1 }−r t n)
togetherwithanexpressionforthenaturalraternasafunction
t
ofg .
t

THEBASICNEWKEYNESIANMODEL 91
d. Determinetheeconomy’sresponsetoanexogenousincreasein
g whenthecentralbankfollowsaninterestraterulegivenby
t
i t =ρ+φ π π t
3.4. IndexationandtheNewKeynesianPhillipscurve
Consider the Calvo model of staggered price setting with the
following modification: In the periods between price reoptimiza-
tions firms mechanically adjust their prices according to some
indexation rule. Formally, a firm that reoptimizes its price in
periodt (aneventthatoccurswithprobability1−θ)setsaprice
P∗ inthatperiod.Insubsequent periods(i.e.,untilitreoptimizes
t
prices again), its price is adjusted according to the following
indexationrule:
P t+k|t = P t+k−1|t ((cid:12) t+k−1 ) ω(cid:12)1−ω
fork=1,2,3,...and
P t,t = P t ∗
where P t+k|t denotes the price effective in period t + k for a
firm that last reoptimized its price in period t, (cid:12) ≡ Pt is the
aggregategrossinflationrate,(cid:12)thelatter’ssteadys t tatev P a t− l 1 ue,and
ω ∈[0,1]isanexogenousparameterthatmeasuresthedegreeof
indexationtolaggedinflation.
Supposethatallfirmshaveaccesstothesameconstantreturns
to scale technology and face a demand schedule with a constant
priceelasticity(cid:2).
The objective function for a firm reoptimizing its price in
periodt (i.e.,choosing P∗)isgivenby
t
(cid:1)∞ (cid:18) (cid:19) (cid:20)(cid:21)
m P a ∗ x θkE t (cid:3) t,t+k (1/P t+k ) P t+k|t Y t+k|t −C t+k (Y t+k|t )
t k=0
subject to a sequence of demand constraints (9), and the indexa-
tionruledescribedabove.Allvariablesaredefinedasinthemain
text.
a. Using the definition of the price level index P ≡
(cid:10) (cid:11) t
(cid:7) 1
1 P(i)1−(cid:2)di 1−(cid:2) , derive a log-linear expression for the evo-
0 t
lutionofinflationπ asafunctionofthenewlysetprice p∗.
t t

92 CHAPTER3
b. Derive the first-order condition for the firm’s problem that
determinestheoptimalprice P∗.
t
c. Log-linearize the first-order condition around the correspond-
ing steady state and derive an expression for p∗ (i.e., the
t
approximatelog-linearprice-settingrule).
d. Combine the results of (a) and (c) to derive an inflation
equationoftheform
π(cid:22) t =γ b π(cid:22) t−1 +γ f E t {π(cid:22) t+1 }−λµ(cid:22) t
whereπ(cid:22) ≡π −π.
t t
3.5. Optimal price setting and equilibrium dynamics in the Taylor
model
Assume a continuum of firms indexed by i ∈ [0,1]. Each firm
producesadifferentiatedgood,withatechnology
Y(i)= AN(i)
t t t
where A represents the level of technology, and a ≡ logA
t t t
evolves exogenously according to some stationary stochastic
process.
During each period a fraction 1 of firms reset their prices,
N
whichthenremaineffectivefor Nperiods.Hence,afirmi setting
anewprice P∗ inperiodt willseektomaximize
t
(cid:1)N−1 (cid:18) (cid:19) (cid:20)(cid:21)
m P a ∗ x E t (cid:3) t,t+k (1/P t+k ) P t ∗ Y t+k|t −C t+k (Y t+k|t )
t k=0
subjectto
Y t+k|t =(P t ∗/P t+k ) −(cid:2) C t+k
(cid:10) (cid:11)
−σ
where(cid:3) t,t+k ≡βk C
C
t+
t
k
a. Showthat P∗ mustsatisfythefirst-ordercondition
t
(cid:1)N−1 (cid:18) (cid:21)
E t (cid:3) t,t+k Y t+k|t (P t ∗−M(cid:13) t+k =0
k=0
where(cid:13) ≡C(cid:9)(·)isthenominalmarginalcostandM≡ (cid:2) .
t t (cid:2)−1

THEBASICNEWKEYNESIANMODEL 93
b. Derive the following log-linearized optimal price-setting rule
(aroundazeroinflationsteadystate)
(cid:1)N−1
p t ∗ =µ+ ω k E t {ψ t+k }
k=0
whereω ≡ βk(1−β),ψ ≡log(cid:13) andµ≡logM.Showthatin
k 1−βN t t
thelimitingcaseofβ =1(nodiscounting)theaboveequation
canberewrittenas
(cid:1)N−1
1
p t ∗ =µ+ N E t {ψ t+k }
k=0
Howdoesthepreviousprice-settingruledifferfromtheone
generatedbytheCalvomodel?
c. Recalling the expression for the aggregate price index P ≡
(cid:10) (cid:11) t
(cid:7) 1
1 P(i)1−(cid:2) di 1−(cid:2) , show that around a zero inflation steady
0 t
statethe(log)pricelevelwillsatisfy
(cid:8) (cid:9)
(cid:1)N−1
1
p = p ∗
t
N
t−k
k=0
d. Consider the particular case of N= 2 and β = 1 and assume
thattheconsumer’s(log)marginalrateofsubstitutionbetween
laborandconsumptionisgivenbyσc +ϕn.Assumealsothat
t t
alloutputisconsumed.Showthat:
1 1
p t ∗ = 2 p t ∗ −1 + 2 E t {p t ∗ +1 }+δ((cid:23)y t +E t {(cid:23)y t+1 })
whereδ ≡σ +ϕ.
e. Assumethatmoneydemandtakesthesimpleformm −p = y
t t t
and that both m and a follow (independent) random walks,
t t
withinnovationsεmandεa,respectively.Deriveaclosed-form
t t
expressionfortheoutputgap,employment,andthepricelevel
asafunctionoftheexogenousshocks.
f. Discuss the influence of δ on the persistence of the effects
of a monetary shock, and provide some intuition for that
result.

94 CHAPTER3
3.6. The Mankiw-Reis model: Inflation dynamics under predeter-
minedprices
Supposethateachperiodafractionoffirms1−θ getstochoose
apathoffuturepricesfortheirrespectivegoods(a“priceplan”),
while the remaining fraction θ keeps their current price plans.
Let {P t,t+k }∞ k=0 denote the price plan chosen by firms that get
to revise√that plan in period t. Firm’s technology is given by
Y(i) = AN(i). Consumer’s period utility is assumed to take
t t t (cid:10) (cid:7) (cid:11) (cid:2)
the form U(C
t
,N
t
) = C
t
− N
2
t 2 , where C
t
≡
0
1 C
t
(i)1−1 (cid:2)di (cid:2)−1.
Thedemandforrealbalancesisassumedtobegivenby Mt =C.
Pt t
Alloutputisconsumed.
(cid:10) (cid:11)
(cid:7) 1
a. Let P ≡ 1 P(i)1−εdi 1−ε denote the aggregate price index.
t 0 t
Showthat,uptoafirst-orderapproximation,
(cid:1)∞
p t =(1−θ) θjp t−j,t (38)
j=0
b. Afirmi,revisingitspriceplaninperiodtwillseektomaximize
(cid:12) (cid:8) (cid:9)(cid:13)
(cid:1)∞
θkE t (cid:3) t,t+k (1/P t+k )Y t+k (i) P t,t+k − √ W t+k
k=0
A t+k
Derive the first-order condition associated with that problem,
and show that it implies the following approximate log-linear
ruleforthepriceplan
p t,t+k =µ+E t {ψ t+k } (39)
for k = 0,1,2,... and where ψ = w − 1a is the nominal
t t 2 t
marginalcost.
c. Usetheoptimalityconditionsfortheconsumer’sproblem,and
thelabormarketclearingconditiontoshowthat(i)thenatural
level of output satisfies yn = −µ+a , and (ii) the (log) real
t t
marginal cost (in deviation from its perfect foresight steady
statevalue)equalstheoutputgap,i.e.,
m"c =(cid:23)y
t t
forallt,where(cid:23)y ≡ y −yn.
t t t

THEBASICNEWKEYNESIANMODEL 95
d. Using (38) and (39), show how one can derive the following
equationforinflation
1−θ 1−θ (cid:1)∞
π t = θ (cid:23)y t + θ θjE t−j {(cid:21)(cid:23)y t +π t } (40)
j=1
e. Supposethatthemoneysupplyfollowsarandomwalkprocess
m t = m t−1 +u t , where m t ≡ logM t and {u t } is white noise.
Determine the dynamic response of output, employment, and
inflation to a money supply shock. Compare the implied re-
sponsetotheoneobtainedunderthestandardNewKeynesian
Phillips curve, where π t = βE t {π t+1 }+κ(cid:23)y t (Hint: use the fact
that in equilibrium y = m − p, substitute for (cid:23)y in (40)
t t t t
in order to obtain a difference equation for the (log) price
level.)
f. Suppose that technology is described by the random walk
processa t =a t−1 +ε t ,wherea t ≡logA t ,and{ε t }iswhitenoise.
Determine the dynamic response of output, the output gap,
employment, and inflation to a technology shock. Compare
theimpliedresponsetooneobtainedunderthestandardNew
Keynesian Phillips curve, where π t = β E t {π t+1 }+κ (cid:23)y t (Hint:
sameas(e)above).
3.7. TechnologyshocksandtheTaylorrule
Consider an economy with Calvo-type staggered price setting,
where a continuum of monopolistically competitive firms have
access to a technology Y = AN, where Y is output, N denotes
t t t t t
hoursofwork,and A isanexogenoustechnologyparameter.The
t
representativeconsumerhasaperiodutilityU(C,N)=logC −
t t t
N t
1+ϕ
, where C is a CES function of the quantities consumed
1+ϕ t
of the different types of goods. The technology parameter a ≡
t
logA is assumed to follow a random walk process, i.e. a =
t t
a t−1 +ε t , where {ε t } is white noise. Firms’ desired markups are
constant. All output is consumed. The labor market is perfectly
competitive.
Theimpliedequilibriumconditionstaketheform
(cid:23)y t = E t {(cid:23)y t+1 }−(i t −E t {π t+1 }−ρ) (41)
π t =βE t {π t+1 }+κ(cid:23)y t (42)

96 CHAPTER3
where (cid:23)y ≡ y − yn is the output gap, y is (log) output, yn is the
t t t t t
(log)naturallevelofoutput,π t ≡ p t −p t−1 istherateofinflation,
andi istheshort-termnominalrate.
t
a. Determine the natural level of output yn as a function of the
t
technologyparameter.
b. Suppose that the monetary authority adopts a simple interest
rateruleoftheform
i t =ρ+φ π π t (43)
whereφ
π
>1.Determinetheequilibriumpathofinflation,the
outputgap,andoutput.
c. How would your answer to (b) change if the technology
processwasinsteadgivenbya t =ρ a a t−1 +ε t withρ a ∈(0,1)?
Deriveyourresultanalyticallyandexplainitintuitively.
3.8. ANewKeynesianeconomywithlinearutility
Consider an economy with Calvo-type staggered price setting,
where a continuum of monopolistically competitive firms have
access to a technology Y = AN, where Y is output, N denotes
t t t t t
employment, and A
t
is an exogenous tech(cid:18)n#ology parameter(cid:21).
The representative consumer maximizes E ∞ βtU(C,N)
0 t=0 t t
wheretheperiodutilityisgivenbyU(C,N) = C − N t
1+ϕ
,where
t t t 1+ϕ
C is a CES function of the quantities consumed of the different
t
types of goods. Firms’ desired markup is constant. All output is
consumed.Thelabormarketisperfectlycompetitive.
(cid:19) (cid:20)
a. Determ(cid:19)ine(cid:20)the (log) natural level of employment nn
t
and
output yn asafunctionoftechnology.
t
b. Explain, using a labor market diagram, why natural employ-
ment always rises in response to a positive technology shock
undertheassumptionsabove.
c. Derivetheconsumer’sEulerequationandshowthatitimplies
aconstantrealinterestrate.Givesomeintuitionforthatresult.
d. Write down a simple interest rate rule (with finite coefficients
and a function of observables only) which will replicate the
natural (i.e., flexible price) allocation. Explain why (short
proof).
3.9. ANKPCwithbackward-lookingfirms(basedonGalíandGertler
(1999)).
Consider the following modification to the basic New Keynesian
model developed in the text: a fraction ω ∈ [0,1] of firms set

THEBASICNEWKEYNESIANMODEL 97
pricesaccordingtothefollowingbackward-lookingrule:
p t b = p t ∗ −1 +π t−1
where
p ∗ =ωpb+(1−ω)pf
t t t
is the average newly set (log) price in period t, with pf denoting
t
the(log)pricesetbyforward-lookingfirms.Thelatterisgivenas
inthestandardmodelby:
(cid:1)∞
p t f =µ+(1−βθ) (βθ)kE t {ψ t+k }
k=0
where, for simplicity, constant returns have been assumed
(α =0).
Both backward- and forward-looking firms can reset their
priceswithprobability1−θ eachperiod.Thus,theaverage(log)
priceevolvesaccordingto:
p t =θp t−1 +(1−θ)p t ∗
Assume,asinthestandardmodel,thatthefollowingrelationship
betweentheaveragemarkupandtheoutputgapholds:
µ(cid:22) =−(σ +ϕ)(cid:23)y
t t
a. ShowthattheNewKeynesianPhillipscurvewillnowtakethe
form
π t =γ b π t−1 +γ f E t {π t+1 }+κ(cid:23)y t
and determine the values of coefficients γ , γ , and κ as a
b f
functionofthemodel’sparameters.
b. Discusstheimplicationsforthecostsofdisinflation,compared
tothestandardNewKeynesianPhillipscurve.