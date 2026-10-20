Chapter 8
MONETARY POLICY IN THE OPEN ECONOMY
All the models analyzed in earlier chapters assumed a closed economy:
households and firms were not able to trade in goods or financial
assets with agents located in other economies. This chapter relaxes
that assumption by developing an open economy extension of the basic
NewKeynesianmodelanalyzedinchapter3.Theframeworkintroduces
explicitly the exchange rate, the terms of trade, exports and imports, as
wellasinternationalfinancialmarkets.Suchaframeworkcaninprinciple
beusedtoassesstheimplicationsofalternativemonetarypolicyrulesin
an open economy. Because the framework nests as a limiting case the
closed economy model of chapter 3, it allows one to assess the extent
to which the opening of the economy affects some of the conclusions
regarding monetary policy obtained for the closed economy and, in
particular,thedesirabilityofapolicythatseekstostabilizeinflation(see
chapter4).Itisalsoworthanalyzingwhatrole,ifany,theexchangerate
plays in the optimal design of monetary policy. Finally, the framework
can be used to determine the implications of alternative simple rules, as
wasdoneinchapter4fortheclosedeconomy.
The analysis of a monetary open economy raises a number of issues
that a modeler needs to confront. First, a choice needs to be made
between the modeling of a “large” or a “small” economy, that is,
between allowing or not, respectively, for repercussions in the rest of
the world of developments (including policy decisions) in the economy
being modeled. Second, the existence of two or more economies subject
to imperfectly correlated shocks makes room for cross-border trade in
assets,forrisksharingpurposesand/orinordertosmoothconsumption
over time. Hence, a decision must be made regarding the nature of
international asset markets and, more specifically, the set of securities
that can be traded in those markets, with possible assumptions ranging
from financial autarky to complete markets. Third, one needs to make
some assumption about firms’ ability to discriminate across countries in
the price they charge for the goods they produce (“pricing to market”
versus “law of one price”). Furthermore, whenever discrimination is
possibleandpricesarenotreadjustedcontinuously,anassumptionmust
be made regarding the currency in which the prices of exported goods
areset(“localcurrencypricing,”i.e.,pricesaresetinthecurrencyofthe

224 CHAPTER8
importing economy versus “producer currency pricing,” i.e., prices are
setinthecurrencyoftheproducer’scountry).Otherdimensionsofopen
economy modeling that require some choices include the allowance or
not for nontradable goods, the existence of trading costs, the possibility
ofinternationalpolicycoordination,andsoon.
Acomprehensiveanalysisoftherangeofpossiblemodelingdimensions
and how alternative assumptions may affect the design of monetary
policy would require a book of its own, thus it is clearly beyond the
scopeofthischapter.Themodestobjectivehereistopresentanexample
of a monetary open economy model to illustrate some of the issues that
emerge in the analysis of such economies and which are absent in their
closed economy counterparts. In particular, the small open economy
modeldevelopedbelowassumescompleteinternationalfinancialmarkets
as well as the law of one price. Then, in the discussion of the model’s
policy implications and in the notes on the literature at the end of the
chapter, reference is made to a number of papers that adopt different
assumptions, and the extent to which their findings differ from those
obtainedhereisbrieflydiscussed.
The framework developed below is a simplified version of the one
in Galí and Monacelli (2005). In order to focus on the issues brought
about by the openness of the economy, the presence of either cost-
push shocks or nominal wage rigidities is ignored. The assumptions
on preferences and technology, combined with a Calvo price-setting
structure and the assumption of complete financial markets, give rise
to a highly tractable model and to simple and intuitive log-linearized
equilibrium conditions. The latter can be reduced to a two-equation
dynamical system consisting of a New Keynesian Phillips curve and a
dynamic IS-type equation, whose form is identical to the system derived
in chapter 3 for the closed economy, though its coefficients depend on
parametersthatarespecifictotheopeneconomywhilethedrivingforces
are a function of world variables (that are taken as exogenous to the
small open economy). As in its closed economy counterpart, the two
equations must be complemented with a description of how monetary
policyisconducted.
After describing the model and deriving a simple representation
of its equilibrium dynamics, section 8.3 analyzes the transmission of
monetary policy shocks, emphasizing the role played by openness in
that transmission. Section 8.4 turns to the issue of optimal monetary
policy design, focusing on a particular case for which the flexible price
allocation is efficient. Under the same assumptions one can derive a
second-orderapproximationtotheconsumer’sutility,whichcanbeused
to evaluate alternative policy rules. Section 8.5 assesses the merits of
alternativesimplemonetarypolicyrules,includinganexchangeratepeg.

POLICYINTHEOPENECONOMY 225
Section8.6concludeswithabriefnoteontherelatedliterature.
8.1 ASMALL OPEN ECONOMYMODEL
The economy is modeled as being infinitesimally small (relative to the
worldeconomy),withitsperformancenothavinganyimpactontherest
of the world. Next, the problem facing households and firms located in
onesucheconomyisdescribedindetail.
8.1.1 Households
The small open economy is inhabited by a representative household
seekingtomaximize
(cid:1)∞
E βtU(C,N;Z) (1)
0 t t t
t=0
where N denotes employment (or work hours), C is a composite
t t
consumptionindexdefinedby1
(cid:2) (cid:3)
η
C t ≡ (1−υ) 1 ηC H,t 1−1 η +υ1 ηC F,t 1−1 η η−1 (2)
and C H,t is an index of consumption of domestic goods given by the
constantelasticityofconsumption(CES)function
(cid:4) (cid:6)
(cid:5) (cid:4)
1 (cid:4)−1
C H,t ≡ C H,t (i) (cid:4)− (cid:4) 1 di
0
where i ∈ [0,1] denotes the good variety. C F,t denotes the quantity
of imported goods consumed. Z is an exogenous preference shifter.
t
Parameter (cid:4) > 1 denotes the elasticity of substitution between varieties
produced domestically. Parameter υ ∈ [0,1] can be interpreted as a
measure of openness. Parameter η > 0 measures the substitutability
betweendomesticandforeigngoods.
1Asη→1theconsumptionindexisgivenby
Ct =
(1−υ)
1
(1−υ)υυ
CH,t 1−υ CF,t υ

226 CHAPTER8
Maximization of (1) is subject to a sequence of budget constraints of
theform
(cid:5)
1
P H,t (i)C H,t (i)di + P F,t C F,t +E t {Q t,t+1 D t+1 }≤ D t +W t N t (3)
0
fort =0,1,2,... P H,t (i)isthepriceofdomesticvarietyi ∈[0,1]. P F,t is
the price of imported goods. D t+1 is the nominal payoff in period t+1
of the portfolio held at the end of period t (possibly including shares in
firms), W is the nominal wage. The previous variables are all expressed
t
in units of domestic currency. Q t,t+1 is the stochastic discount factor
forone-period-aheadnominalpayoffs(tobederivedbelow).Households
haveaccesstoacompletesetofcontingentclaims,tradedinternationally.
As in the closed economy, the optimal allocation across varieties of
anygivenexpenditureondomesticgoodsyieldsthedemandfunctions
(cid:7) (cid:8)
−(cid:4)
C H,t (i)= P H,t (i) C H,t (4)
P H,t
(cid:2) (cid:3)
(cid:9) 1
for all i ∈ [0,1], where P H,t ≡
0
1 P H,t (i)1−(cid:4)di 1−(cid:4) is the domestic
price index (i.e., an index of prices of domestically produced goods).
Combi (cid:9) ning(4)withthedefinitionsof P H,t andC H,t yieldstheconvenient
result
0
1 P H,t (i)C H,t (i)di = P H,t C H,t .
On the other hand, the optimal allocation of expenditures between
domesticandimportedgoodsisgivenby
(cid:7) (cid:8) (cid:7) (cid:8)
−η −η
C H,t =(1−υ) P H,t C t ; C F,t =υ P F,t C t (5)
P P
t t
(cid:10) (cid:11)
where P t ≡ (1−υ)(P H,t )1−η+υ(P F,t )1−η 1− 1 η is the consumer price
index(CPI).2 Notethatundertheassumptionofη = 1or,alternatively,
when the price indexes for domestic and foreign goods are equal (as in
the steady state described below), parameter υ corresponds to the share
ofconsumptionexpendituresallocatedtoimportedgoods.
Using (5) and the definitions of indexes C and P it can be shown
t t
that total consumption expenditures by domestic households can be
2Intheparticularcaseofη=1,theCPItakestheform
.
Pt
=(PH,t)1−υ
(PF,t)
υ

POLICYINTHEOPENECONOMY 227
conveniently expressed as P H,t C H,t + P F,t C F,t = P t C t . Thus, the period
budgetconstraintsimplifiesto
P t C t +E t {Q t,t+1 D t+1 }≤ D t +W t N t (6)
As in chapter 3, the period utility function is specialized to be of the
form
(cid:4) (cid:6)
 C
t
1
1
−
−
σ −
σ
1
−
1
N
+
t
1+
ϕ
ϕ
Z
t
for σ (cid:6)=1
U(C,N;Z)= (cid:4) (cid:6)
t t t 
logC −
N
t
1+ϕ
Z for σ =1
t 1+ϕ t
withz ≡logZ followinganexogenous AR(1)process
t t
z t =ρ z z t−1 +ε t z
whereρ ∈[0,1).
z
Under the assumption of perfectly competitive labor markets (which
is maintained throughout this chapter), the intratemporal optimality
condition for the household’s problem takes the same form as in the
closedeconomymodelofchapter3,namely:
W
C σ N ϕ = t (7)
t t P
t
Inordertoderivetherelevantintertemporaloptimalityconditionnote
thatthefollowingrelationmustholdfortheoptimizinghouseholdinthe
smallopeneconomy
V t P ,t t +1 Z t C t −σ =ξ t,t+1 βZ t+1 C t − + σ 1 P t 1 +1 (8)
where V t,t+1 is the period t price (in domestic currency) of an Arrow
security, that is, a one-period security that yields one unit of domestic
currency if a specific state of nature is realized in period t + 1, and
nothing otherwise, and where ξ t,t+1 is the probability of that state of
naturebeingrealizedint+1(conditionalonthestateofnatureatt).C t+1 ,
Z t+1 , and P t+1 on the right side should be interpreted as representing
the values taken by those variables at t +1 conditional on the state of

228 CHAPTER8
nature in which the Arrow security generates a payoff. Thus, the left
side captures the utility loss resulting from the purchase of an Arrow
security considered (with the corresponding reduction in consumption),
whereas the right side measures the expected one-period-ahead utility
gain from the additional consumption made possible by the (eventual)
securitypayoff.Iftheconsumerisoptimizingtheexpectedutilitygain,it
mustexactlyoffsetthecurrentutilityloss.
ThepriceofthenominalArrowsecurityintroducedabovemustsatisfy
V t,t+1 =ξ t,t+1 Q t,t+1 .Thus,(8)canberewrittenas3
(cid:7) (cid:8) (cid:7) (cid:8)(cid:7) (cid:8)
−σ
β C t+1 Z t+1 P t = Q t,t+1 (9)
C t Z t P t+1
which is assumed to be satisfied for all possible states of nature at t and
t+1.
Taking conditional expectations on both sides of (9) and rearranging
terms,aconventionalstochasticEulerequationcanbederived
(cid:16)(cid:7) (cid:8) (cid:7) (cid:8)(cid:7) (cid:8)(cid:17)
−σ
Q =βE C t+1 Z t+1 P t (10)
t t
C t Z t P t+1
where Q t ≡ E t {Q t,t+1 } denotes the price of a one-period discount bond
payingoffoneunitofdomesticcurrencyinallstatesatt+1.
Equations (7) and (9) can be respectively written in log-linearized
formas
w − p =σc +ϕn
t t t t
1 1
c t = E t {c t+1 }− σ (i t −E t {π t+1 }−ρ)+ σ (1−ρ z )z t (11)
where lowercase letters denote the logs of the respective variables, i ≡
t
−logQ istheshort-termnominalrate,ρ ≡−logβ isthetimediscount
t
rate,andπ t ≡ p t − p t−1 isCPIinflation(with p t ≡logP t ).
3 Notethatundercompletemarketsasimplenoroomforarbitrageargumentimplies
thatthep(cid:1)riceofaone-periodasset(orportfolio)yieldingarandompayoff Dt+1 mustbe
givenby Vt,t+1Dt+1whe(cid:2)rethesumi(cid:3)soverallpossiblestatesatt+1.Equivalently,that
pricecanbewrittenas Et V ξ t t , , t t + + 1 1Dt+1 .Thus,theone-period stochastic discount factor
canbedefinedasQt,t+1 ≡ V ξ t t , , t t + + 1 1.

POLICYINTHEOPENECONOMY 229
8.1.1.1 DOMESTICINFLATION,CPIINFLATION,THEREALEXCHANGERATE,
ANDTHETERMSOFTRADE:SOMEIDENTITIES
Next,severalassumptionsanddefinitionsareintroduced,andanumber
of identities are derived that are extensively used below. The terms of
trade, denoted by S , is defined as the price of foreign goods relative to
t
domesticgoods.Formally,
S ≡ P F,t
t
P H,t
or,inlogs,s t ≡logS t = p F,t − p H,t .
Log-linearization of the CPI index around a symmetric steady state
withS =1yieldsthefollowingapproximaterelationbetweenconsumer
prices,domesticpricesandthetermsoftrade.4
p t =(1−υ)p H,t +υp F,t
= p H,t +υs t (12)
It follows that domestic inflation, defined as the rate of change in the
index of domestic goods prices, that is, π H,t ≡ p H,t − p H,t−1 , and CPI
inflation, arelinkedaccordingtotherelation
π t =π H,t +υ(cid:11)s t (13)
that is, the gap between the two measures of inflation is proportional
to the percentage change in the terms of trade, with the coefficient of
proportionalitygivenbytheopennessindexυ.
It is assumed that the law of one price holds for individual goods at
alltimes(bothforimportandexportprices).Inparticular, P F,t = E t P t ∗,
where E is the nominal exchange rate (defined as the price of foreign
t
currency in terms of domestic currency), and P∗ is the price of foreign
t
goods expressed in foreign currency. P∗ can also be interpreted as a
t
world price index, given that the size of the small open economy is
assumed to be negligible relative to the rest of the world. On the same
grounds, for the world as a whole there is no distinction between CPI
anddomesticpricelevel.
4 It is useful to note, for future reference, that the approximation (12) holds exactly
whenη=1.

230 CHAPTER8
The assumed law of one price, combined with the definition of the
termsoftrade,implies
s t =e t + p t ∗− p H,t (14)
wheree ≡E .
t t
The real exchange rate is defined as the ratio of world and domestic
CPI’s,bothexpressedindomesticcurrency
Q ≡ P F,t
t
P
t
Thus,inlogs:
q t = p F,t − p t
=s t + p H,t − p t
=(1−υ)s
t
wherethelastequalityholdsexactlyifη=1,butonlyuptoafirst-order
approximationwhenη(cid:6)=1.
8.1.1.2 INTERNATIONALRISKSHARING
Under the assumption of a complete set of state-contingent securities
traded internationally, a condition analogous to (8) must also hold for
householdsintherestoftheworld.Assumingautilityfunctionidentical
tothatofdomestichouseholdsthisconditiontakestheform:
V E t t , P t+ t ∗ 1 (C t ∗ ) −σ =ξ t,t+1 β(C t ∗ +1 ) −σ E t+1 1 P t ∗ +1
where C∗ denotes (per capita) consumption by foreign households. The
t
presence of the exchange rate terms reflects the fact that the Arrow
security considered has a price V t,t+1 and a unit payoff expressed in the
currency of the small open economy. For simplicity, it is assumed that
foreignhouseholdsarenotsubjecttopreferenceshocks.
The previous relation can be written in terms of our small open
economy’sstochasticdiscountfactoras
(cid:7) (cid:8) (cid:7) (cid:8)(cid:7) (cid:8)
C∗ −σ P∗ E
β C t+ t ∗ 1 P t ∗ + t 1 E t+ t 1 = Q t,t+1 (15)

POLICYINTHEOPENECONOMY 231
Combining (9) and (15), together with the definition of the real
exchangerateandthelawofoneprice,yields
C =ϑC ∗ Zσ 1Qσ 1 (16)
t t t t
forallt,andwhereϑ isaconstantwhichwillgenerallydependoninitial
conditionsregardingrelativenetassetpositions.Henceforth,andwithout
lossofgenerality,symmetricinitialconditionsareassumed(i.e.,zeronet
foreign asset holdings and an ex-ante identical environment), implying
ϑ =1.
Undertheassumptionthatthesmalleconomyhasaninfinitesimalsize
relative to the rest of the world, C∗ = Y∗ for all t, where Y∗ denotes
t t t
worldoutput(expressedinpercapitaterms).Imposingthatconditionon
(16)andtakinglogs,
1
c = y ∗+ (z +q) (17)
t t σ t t
(cid:7) (cid:8)
1 1−υ
= y ∗+ z + s
t σ t σ t
where the second equality holds only up to a first-order approximation
when η (cid:6)= 1. Thus, the assumption of a complete market for state-
contingent securities at the international level leads to a simple relation-
ship linking domestic consumption with world output and the terms of
trade.
8.1.1.3 ABRIEFDETOUR:UNCOVEREDINTERESTPARITYANDTHE
TERMSOFTRADE
Under the assumption of complete international financial markets, the
equilibrium price (in terms of the small open economy’s domestic
currency) of a bond which pays one unit of foreign currency is given
by E t Q∗ t = E t {Q t,t+1 E t+1 }, where Q∗ t is the price of the bond in terms of
foreign currency. The previous pricing equation can be combined with
thedomesticbondpricingequation, Q t = E t {Q t,t+1 }toobtainaversion
oftheuncoveredinterestparitycondition
E t {Q t,t+1 [exp{i t }−exp{i t ∗}(E t+1 /E t )]}=0

232 CHAPTER8
Log-linearizing around a perfect foresight steady state yields the
familiaruncoveredinterestparitycondition:
i t =i t ∗+E t {(cid:11)e t+1 } (18)
Combining(14)and(18)yieldsthestochasticdifferenceequation
s t =(i t ∗−E t {π t ∗ +1 })−(i t −E t {π H,t+1 })+E t {s t+1 } (19)
In a symmetric steady state the terms of trade take a unit value, that
is,S =1.Thatfact,combinedwiththeassumptionofstationarityinthe
model’sdrivingforces,impliesthatlim T→∞E
t
{s
T
}=0.5Hence,(19)can
besolvedforwardtoobtain
(cid:16) (cid:17)
(cid:1)∞
s t = E t [(i t ∗ +k −π t ∗ +k+1 )−(i t+k −π H,t+k+1 )] (20)
k=0
that is, the terms of trade are a function of current and anticipated real
interestratedifferentials.
It must be pointed out that while equations (19) and (20) provide a
convenient (and intuitive) way of representing the connection between
terms of trade and interest rate differentials, they do not constitute an
additional independent equilibrium condition. In particular, it is easy
to check that (19) can be derived by combining the consumption Euler
equations for both the domestic and world economies with the risk
sharingcondition(17)andequation(13).
Next,attentionisturnedtothesupplysideoftheeconomy.
8.1.2 Firms
8.1.2.1 TECHNOLOGY
Atypicalfirminthehomeeconomyproducesadifferentiatedgoodwith
atechnologyrepresentedbytheproductionfunction
Y(i)= AN(i)1−α
t t t
5Theassumptionregardingthesteadystateimpliesthattherealinterestratedifferential
willreverttoazeromean.Moregenerally,therealinterestratedifferentialwillreverttoa
constantmean,aslongasthetermsoftradearestationaryinfirstdifferences.Thatwould
bethecaseif,say,thetechnologyparameterhadadifferentaveragerateofgrowthrelative
totherestoftheworld.

POLICYINTHEOPENECONOMY 233
where a ≡ logA is a technology shifter common to all domestic firms
t t
followingtheAR(1)processa t =ρ a a t−1 +ε t a.
8.1.2.2 PRICESETTING
As in the basic model of chapter 3, it is assumed that domestic firms set
pricesinastaggeredfashion.Inparticular,ameasure1−θ of(randomly
selected) firms sets new prices each period, with an individual firm’s
probabilityofreoptimizinginanygivenperiodbeingindependentofthe
timeelapsedsinceitlastresetitsprice.Asshowninchapter3,theoptimal
price-settingstrategyforthetypicalfirmresettingitspriceinperiodtcan
beapproximatedbythe(log-linear)rule
(cid:1)∞
p H,t =µ+(1−βθ) (βθ)kE t {ψ t+k|t } (21)
k=0
where p H,t denotesthepricenewlysetbydomesticfirms(inlogs),ψ t+k|t
isthe(log)nominalmarginalcostinperiodt+kforafirmlastresetting
itspriceinperiodt,andµ≡log (cid:4) isthelogofthe(gross)steadystate
(cid:4)−1
markup.6
Asshowninchapter3,thepreviousoptimalpricesettingconditioncan
be combined with an equation describing the evolution of the domestic
pricelevel,togetherwitharelationlinkingtheconditionalmarginalcost
ψ t+k|t to the average marginal cost ψ t+k , to yield the following domestic
inflationequation:
π H,t =βE t {π H,t+1 }−λµ(cid:18) t (22)
whereµ(cid:18) t ≡ p H,t −ψ t+k −µisthemarkupgap,and
(cid:7) (cid:8)
(1−θ)(1−βθ)
λ≡ (cid:17)
θ
where(cid:17)≡ 1−α ∈[0,1].
1−α+α(cid:4)
Thus, it can be seen that in the open economy the relation between
domesticpriceinflationandthemarkupgapisnotaffectedbythedegree
ofopennessonthesubstitutabilitybetweendomesticandforeigngoods.
6 p H,t isusedtodenotenewlysetpricesinsteadofp t ∗(usedinchapter3),becauseinthis
chapterletterswithanasteriskrefertoworldeconomyvariables.

234 CHAPTER8
8.1.3 Exports
Thedemandforexportsofgoodi ∈[0,1]isassumedtobegivenby
(cid:7) (cid:8)
−(cid:4)
X(i)= P H,t (i) X
t t
P H,t
(cid:2) (cid:3)
(cid:9) (cid:4)
where X t ≡ 0 1 X t (i) (cid:4)− (cid:4) 1di (cid:4)−1 isanindexofaggregateexportsfromthe
small open economy to the rest of the world. Aggregate exports are, in
turn,assumedtobegivenby
(cid:7) (cid:8)
−η
X =υ P H,t Y ∗
t E P∗ t
t t
=υSη
Y
∗
t
The previous results hold under the assumption that the preferences
of households in the rest of the world are identical to those of domestic
households, combined with the fact that global goods market clearing
implies C∗ = Y∗.7 Thus, in the symmetric steady state with S = 1,
t t
X(i) = X = υY∗, for all i ∈ [0,1]. Moreover, given that in that steady
state C = υC, and that C = Y∗ (from the risk sharing condition) it
F
followsthattradeisbalancedatthesymmetricsteadystate.
8.2 EQUILIBRIUM
8.2.1 AggregateDemandandOutputDetermination
8.2.1.1 CONSUMPTIONANDOUTPUTINTHESMALLOPENECONOMY
Goodsmarketclearinginthehomeeconomyrequires
Y t (i)=C (cid:7) H,t (i)+ (cid:8) X t (i (cid:19) ) (cid:7) (cid:8) (cid:20) (23)
−(cid:4) −η
= P H,t (i) (1−υ) P H,t C +υSη Y ∗
P H,t P t t t
foralli ∈[0,1]andallt.
7 See Galí and Monacelli (2005) for a more careful derivation, under the assumption
thattheworldismadeupofacontinuumofsmalleconomiesliketheoneanalyzedhere.

POLICYINTHEOPENECONOMY 235
Plugging (23) into the definition of aggregate domestic output Y ≡
(cid:2) (cid:9) (cid:3) (cid:4) t
0
1 Y
t
(i)1−1 (cid:4)di (cid:4)−1 yields
(cid:7) (cid:8)
−η
Y =(1−υ) P H,t C +υSη Y ∗ (24)
t P t t t
t
whichcanbeapproximatedaroundthesymmetricsteadystateas
y =(1−υ)c +υ(2−υ)ηs +υy ∗ (25)
t t t t
Finally,combining(13)withtheEulerequation(11)gives
1 υ 1
c t = E t {c t+1 }− σ (i t −E t {π H,t+1 }−ρ)+ σ E t {(cid:11)s t+1 }+ σ (1−ρ z )z t (26)
Note that (17) and (25) can be combined to derive the following
expressionforthetermsoftrade:
s
t
=σ υ(y
t
−y
t
∗ )−(1−υ)(cid:18)z
t
(27)
where σ υ ≡ σ(cid:18) > 0 with (cid:18) ≡ 1+υ( 1 (cid:19)−1) > 0 and where (cid:19) ≡
ση+(1−υ)(ση−1).
Finally, combining (25), (26), and (27) yields (after some algebra)
aversionofthedynamicISequationforthesmallopeneconomy:
1
y t = E t {y t+1 }− σ (i t −E t {π H,t+1 }−ρ)+υ((cid:19) −1)E t {(cid:11)y t ∗ +1 }
υ
1−v
+ (1−ρ )z (28)
σ z t
Note that, in general, the degree of openness influences the sensitivity
ofoutputtoachangeinthedomesticrealinterestratei t −E t {π H,t+1 },as
measuredby1/σ υ.Inparticular,ifση>1anincreaseinopennessraises
thatsensitivity,sinceσ υ isdecreasinginυ underthatassumption.
As its closed economy counterpart, equation (28) can be rewritten in
termsoftheoutputandrealinterestrategapsas:
1
(cid:21)y t = E t {(cid:21)y t+1 }− σ (i t −E t {π H,t+1 }−r t n) (29)
υ
where
r t n =ρ+σ υE t {(cid:11)y t n +1 }+σ υ υ((cid:19) −1)E t {(cid:11)y t ∗ +1 }+(cid:18)(1−v)(1−ρ z )z t (30)

236 CHAPTER8
is the natural interest rate, with yn denoting the natural level of output,
t
determinedbelow.
Thus, it is seen that the small open economy’s equilibrium is charac-
terized by a forward-looking dynamic IS-type equation similar to that
found in the closed economy. Nevertheless, two differences are worth
pointingout.First,thedegreeofopennessinfluencesthesensitivityofthe
output gap to interest rate changes. Second, openness generally makes
the natural interest rate depend on expected world output growth, in
addition to domestic shocks (also because, as shown below, the natural
levelofoutputwillgenerallydependonworldoutput).
(cid:22) (cid:23)(cid:2) 8.2.1.2(cid:3)THETRADEBALANCE
Let nx ≡ 1 Y − Pt C denote net exports in terms of domestic
t Y t PH,t t
output,expressedasafractionofsteadystateoutputY.Notethatunder
theassumptionsmadeabovetradeisbalancedinthesteadystate.Afirst-
orderapproximationaroundthatsteadystateyieldsnx = y −c −υs ,
t t t t
whichcombinedwith(17)and(25)impliesasimplerelationbetweennet
exportsandthetermsoftrade
(cid:2) (cid:3)
(cid:19) υ
nx =υ −1 s − z (31)
t σ t σ t
Notethat,giventhetermsoftrade,apositivepreferenceshockinduces
a trade deficit in the small open economy. In the special case of σ =
η = 1, net exports are invariant to changes in the terms of trade: the
latter’spriceeffectsonthetradebalanceexactlyoffsetitsquantityeffects
in that case. More generally, the sign of the relationship between the
terms of trade and net exports is ambiguous, depending on the relative
sizes of υ, σ, and η. If υ and/or η are sufficiently large, a term of trade
depreciation(i.e.,anincreaseins )willimprovethetradebalance.
t
8.2.2 TheSupplySide:MarginalCostandInflationDynamics
8.2.2.1 AGGREGATEOUTPUTANDEMPLOYMENT
As in chapter 3, one can derive an approximate aggregate production
function relating aggregate domestic output to aggregate employment.
Noticethatequilibriuminthelabormarketrequires
(cid:5) (cid:7) (cid:8) (cid:5) (cid:7) (cid:8)
N ≡ 1 N(i)di = Y t 1− 1 α 1 P H,t (i) − 1− (cid:4) α di
t t
0 A t 0 P H,t

POLICYINTHEOPENECONOMY 237
(cid:2) (cid:3)
(cid:9) −(cid:4)
Asshowninchapter3,however,variationsind ≡log 1 PH,t(i) di
t 0 PH,t
around the perfect foresight steady state are of second order. Thus, and
up to a first-order approximation, the following relationship between
(log)aggregateoutputand(log)aggregateemploymentholds
y =a +(1−α)n (32)
t t t
8.2.2.2 MARKUPSANDINFLATIONDYNAMICSIN
THESMALLOPENECONOMY
Nextarelationbetweentheaveragepricemarkupanddomesticoutputis
derived.Thatrelationdifferssomewhatfromthatintheclosedeconomy,
due to the existence of a wedge between output and consumption, and
betweendomesticandconsumerprices.Thus,inthepresentmodel(and
ignoringconstantterms),
µ t = p H,t −(w t −a t +αn t )
=−(w t − p t )−(p t − p H,t )+a t −αn t
=−(σc +ϕn)−υs +a −αn
(cid:7) t t (cid:8) t t t (cid:7) (cid:8)
ϕ+α ϕ+α
=− σ + y +υ((cid:19) −1)s + 1+ a −υz (33)
1−α t t 1−α t t
where the last equality makes use of (17), (25), and (32). Note that, in
addition to domestic output and technology, the average markup is a
functionofthetermsoftradeandthepreferenceshifterz.Thisisdueto
t
theinfluenceofbothvariablesontherealwagethroughanincomeeffect
onlaborsupplyresultingfromtheirimpactondomesticconsumption.In
addition, changes in the terms of trade have a direct effect, captured by
thetermυs ,ontheproductwage,foranygivenconsumptionwage.The
t
influence of technology (through its direct effect on labor productivity)
andofdomesticoutput(throughitseffectonemploymentand,hence,on
the real wage for a given output level) is analogous to that observed in
theclosedeconomy.
Combining (33) with (22) (and ignoring constant terms) yields a
versionoftheNewKeynesianPhillipscurveforthesmallopeneconomy:
(cid:7) (cid:8)
ϕ+α
π H,t =βE t {π H,t+1 }+κy t −λυ((cid:19)−1)s t −λ 1+ 1−α a t +λυz t (34)
(cid:22) (cid:23)
whereκ ≡λ σ + ϕ+α ,asintheclosedeconomymodelofchapter3.
1−α

238 CHAPTER8
Next it is shown how a version of the New Keynesian Phillips
curve linking domestic inflation and the output gap can be derived.
Evaluating (33) at the flexible price equilibrium and subtracting the
resultingexpressionyields:
(cid:7) (cid:8)
ϕ+α
µ(cid:18) =− σ + (cid:21)y +υ((cid:19) −1)(cid:21)s
t 1−α t t
where(cid:21)y ≡ y −yn and(cid:21)s ≡s −sn denotetheoutputgapandtheterms
t t t t t t
oftradegap,respectively,wherethenaturallevelofoutputisgivenby
y
t
n =(cid:21)
a
a
t
+(cid:21)
z
z
t
+(cid:21) ∗y
t
∗ (35)
with (cid:21) a ≡ σ υ(1− 1 α + ) ϕ +ϕ+α > 0, (cid:21) ∗ ≡ −υ σ ( υ (cid:19) (1 − − 1 α )σ )+ υ( ϕ 1 + − α α) and (cid:21) z ≡ − σ υ υ ( (cid:19) 1− (cid:18) α ( ) 1 + − ϕ α + ) α
andwherethenaturaltermsoftradecanbedeterminedusing(27):
s
t
n =σ υ(y
t
n−y
t
∗ )−(1−υ)(cid:18)z
t
Note that the sign of the effect on the domestic natural output of
changes in world output and preference shock is ambiguous. In the
particular case of σ = η = 1, however, world output has no effect on
the domestic natural output ((cid:21) ∗ = 0), while preference shocks z t have
a negative effect ((cid:21) < 0). The latter effect of preference shocks was
z
absent in the closed economy,8 and is a consequence of the increase in
consumptionimpliedbyrisksharingwiththerestoftheworld.
Usingthefactthat(cid:21)s t =σ υ (cid:21)y t (asimpliedby(27)),thefollowingsimple
relationbetweentheaveragemarkupandtheoutputgapcanbederived:
(cid:7) (cid:8)
ϕ+α
µ(cid:18) t =− σ υ + 1−α (cid:21)y t (36)
where (cid:21)y ≡ y − yn. Plugging (36) into (22) yields a version of a
t t t
New Keynesian Phillips curve of identical form as its closed economy
counterpartderivedinchapter3:
π H,t =βE t {π H,t+1 }+κ υ (cid:21)y t (37)
(cid:22) (cid:23)
where κ υ ≡ λ σ υ + ϕ 1− + α α . For υ (cid:22) = 0 (or, (cid:23) alternatively, σ = η = 1)
the slope coefficient is given by λ σ + ϕ+α ≡ κ, as in the basic closed
1−α
8Notethat(cid:21)
z
=0whenυ=0.

POLICYINTHEOPENECONOMY 239
economy model of chapter 3. More generally, the degree of openness,
υ,andthesubstitutabilitybetweendomesticandforeigngoods,η,affect
thedynamicsofinflationthroughtheirinfluenceontheslopecoefficient
κ υ,whichdeterminestheinflationresponsetovariationsin(currentand
future) output gaps. In particular, if ση > 1 (and, hence, (cid:19) > 1),
an increase in openness lowers σ υ, reducing the sensitivity of domestic
inflation to the output gap due to the smaller effect of the latter on the
averagemarkup,asdiscussedabove.
Finally,notethatbycombining(30)with(35)aclosedformexpression
forthenaturalrateofinterestcannowbederived
r t n ≡ρ−σ υ (cid:21) a (1−ρ a )a t +(cid:22) ∗E t {(cid:11)y t ∗ +1 }+(cid:22) z (1−ρ z )z t (38)
is the small open economy’s natural rate of interest, with (cid:22) ∗ ≡
σ υ(υ((cid:19) −1)+(cid:21) ∗)and(cid:22) z ≡(1−υ)(cid:18)−σ υ (cid:21) z .Notethatlimυ→0 (cid:22) ∗ =0
andlimυ→0 (cid:22)
z
=1.
8.3 EQUILIBRIUM DYNAMICS UNDER AN INTERESTRATE RULE
In the previous two sections the equilibrium conditions making up the
nonpolicy block of the small open economy model have been derived.
Those conditions take the form of a set of equations involving all the
relevantendogenousvariables,withtechnologyandpreferenceshocksas
driving forces. As in previous chapters, in order to close the model, that
set of equations has to be supplemented with a description of monetary
policy.
Asanillustration,thepresentsectioncharacterizesthemodel’sequilib-
riumundertheassumptionthatthemonetaryauthorityfollowsaTaylor-
typeinterestraterulesimilartotheoneintroducedinchapter3,namely
i t =ρ+φ π π H,t +φ y (cid:18)y t +v t (39)
where φ π and φ y are non-negative coefficients chosen by the monetary
authority, and where v is an exogenous monetary policy shock that
t
evolvesaccordingtothe AR(1)process:
v =ρ v +εv
t v t−1 t
whereρ
v
∈[0,1).
Combining (29), (37), and (39), the equilibrium dynamics for the
output gap and domestic inflation can be represented by means of the

240 CHAPTER8
systemofdifferenceequations
(cid:19) (cid:20) (cid:19) (cid:20)
π
(cid:21)y
H
t
,t
=Aυ
E
E
t {
t
π
{(cid:21)y
H
t
,
+
t+
1 }
1 }
+Bυu
t
(40)
where
u ≡(cid:18)rn−φ (cid:18)yn−v
t t y t t
and
(cid:19) (cid:20) (cid:19) (cid:20)
σ υ 1−βφ π 1
Aυ ≡(cid:24) υ ; Bυ ≡(cid:24) υ
σ υ κ υ κ υ +β(σ υ +φ y ) κ υ
with(cid:24) υ ≡ σ +φ 1 +κ φ .Theprevioussystemhasthesameformastheone
υ y υ π
analyzed in chapter 3 for the closed economy, with the only difference
lyinginthefactthatsomeofthecoefficientsareafunctionofthe“open
economyparameters”υ andη,andthat(cid:18)yn and(cid:18)rn arenowgivenby(35)
t t
and (38), respectively. In particular, the condition for a locally unique
stationary equilibrium under rule (39) takes the same form as the one
introducedinchapter3,namely
κ υ(φ π −1)+(1−β)φ y >0 (41)
which is assumed to hold for the remainder of this section. Once the
equilibrium path for the output gap and inflation has been determined,
one can use the various equilibrium relations derived in the previous
two sections to determine the corresponding equilibrium values for the
remainingvariablesofinterest.
The previous framework is used below to examine the economy’s
response to an exogenous monetary policy shock, that is, an exogenous
change in v . Given the isomorphism with the closed economy model of
t
chapter3,manyoftheresultsderivedtherecanbeexploited.Theanalysis
of the effects of a technology shock, a preference shock, or a change in
worldoutputisnotpursuedhere,butanidenticalapproachcanbeused:
First,one should determine the implications of the shock considered for
(cid:18)rn and (cid:18)yn,and then proceed tosolve for the equilibrium response of the
t t
output gap and domestic inflation exactly as done next for the case of a
monetarypolicyshock.9
9Ofcourse,asinchapter3,itmustbetakenintoaccountthatatechnologyshockora
shocktoworldoutputalsoleadstoavariationinthenaturaloutputlevel,thusbreaking
theidentitybetweenoutputandtheoutputgap.

POLICYINTHEOPENECONOMY 241
8.3.1 TheEffectsofaMonetaryPolicyShock
Neither the natural rate of interest nor the natural level of output are
affected by a monetary policy shock, so (cid:18)rn = (cid:18)yn = 0 for all t for the
t t
purposes of this exercise. As in chapter 3, let us guess that the solution
takes the form (cid:21)y t = ψ yv v t and π t = ψ πv v t , where ψ yv and ψ πv are
coefficientstobedetermined.Imposingtheguessedsolutionon(40)and
usingthemethodofundeterminedcoefficients,
(cid:21)y
t
=−(1−βρ v)(cid:25)
v
v
t
and
π =−κ (cid:25) v
H,t υ v t
where (cid:25) v ≡ (1−βρ v)[σ υ(1−ρ v 1 )+φ y]+κ υ(φ π −ρ v) . It can be easily shown that as
long as (41) is satisfied, (cid:25) v > 0. Hence, as in the closed economy, an
exogenous increase in the interest rate leads to a persistent decline in
outputanddomesticinflation.Thesizeoftheeffectoftheshockrelative
to the closed economy benchmark depends on the values taken by a
number of parameters. More specifically, if ση > 1 then (cid:25) v can be
shown to be increasing in the degree of openness, thus implying that a
givenmonetarypolicyshockwillhavealargerimpactinthesmallopen
economythaninitsclosedeconomycounterpart.
Using interest rate rule (39), the response of the nominal rate can be
determined, taking into account the central bank’s endogenous reaction
tochangesininflationandtheoutputgap
(cid:10) (cid:11)
i t =ρ+ 1−(cid:25) v(φ π κ υ +φ y (1−βρ v)) v t
Note that as in the closed economy model, the full response of the
nominalratemaybepositiveornegative,dependingonparametervalues.
The response of the real interest rate (expressed in terms of domestic
goods)isgivenby
r t =i t − (cid:10) E t {π H,t+1 } (cid:11)
=ρ+ 1−(cid:25) v((φ π −ρ v)κ υ +φ y (1−βρ v)) v t
Thus the real rate increases unambiguously when v rises,because the
t
terminsquarebracketsisalwayspositive.
Using (27), the response of the terms of trade to the monetary policy
shockcanthenbeuncovered
s
t
=σ υy
t
=−σ υ(1−βρ v)(cid:25)
v
v
t

242 CHAPTER8
whilethechangeinthenominalexchangerateisgiveninturnby
(cid:11)e
t
=(cid:11)s
t
+π
H,t
=−(cid:25) v[σ υ(1−βρ v)+κ υ]v
t
+σ υ(1−βρ v)(cid:25)
v
v
t−1
Thus, a tightening of monetary policy leads to a persistent improve-
ment in the terms of trade (i.e., a decrease in the relative price of
foreign goods) as well as a nominal exchange rate appreciation, both
in the short run and in the long run. To understand the long-run
effect, note that the terms of trade revert back to their original level in
response to the monetary policy shock, which requires that the nominal
exchangerateappreciatebythesameamountasthepermanentdecrease
κ (cid:25)
in domestic price level, which is given by υ v (given an initial shock of
1−ρ
v
size normalized to unity). Hence, the exchange rate will overshoot its
long-runlevelinresponsetothemonetarypolicyshock,ifandonlyif,
σ υ(1−βρ v)(1−ρ v)>κ
υ
ρ
v
which requires that the shock is not too persistent. It can be easily
checked that the previous condition corresponds to that for an increase
inthenominalinterestrateinresponsetoapositivev shock.Notethat,
t
in that case, the subsequent exchange rate depreciation required by the
interestparitycondition(18)leadstoaninitialovershooting.
Figure8.1displaysthedynamicresponsesofseveralmacrovariablesto
anexogenoustighteningofmonetarypolicy.Fortheparameterscommon
withtheclosedeconomy,thebaselinecalibrationfromchapter3isused
here. Regarding the additional, open-economy-related, parameters, it is
assumed a unit elasticity of substitution between domestic and foreign
goods (η = 1) and a openness index υ of 0.4, following Galí and
Monacelli(2005).
As shown in the figure, both output (which equals the output gap
in this case) and domestic inflation decline persistently in response to
a tightening of monetary policy, due to the rise in both nominal and
(most importantly) real interest rates. The latter is also responsible
for the short-run appreciation of the terms of trade and the nominal
exchangerate,whichleadstoalargedeclineofCPIinflationonimpact.
The subsequent depreciation of the exchange rate helps bring CPI
inflation back close to its initial level despite the persistent response
of domestic inflation. In the long run, the responses of the CPI, the
domesticpricelevel,andthenominalexchangerateconvergetothesame
negativevalues,thoughtheirtrajectoriesduringtheadjustmentarerather

POLICYINTHEOPENECONOMY 243
0 0
–0.2 –0.2
–0.4 –0.4
0 5 10 15 0 5 10 15
Output gap Employment
0 1
–0.2 0
–0.4 –1
0 5 10 15 0 5 10 15
Domestic inflation CPI inflation
0 –0.15
–0.1
–0.2 –0.2
0 5 10 15 0 5 10 15
Domestic price level Consumer price level
0 0
–0.2 –0.2
–0.4 –0.4
0 5 10 15 0 5 10 15
Terms of trade Nominal exchange rate
0.4 1
0.2 0.5
0 0
0 5 10 15 0 5 10 15
Nominal rate Real rate
Figure8.1. DynamicResponsestoaMonetaryPolicyShock.
different. Note also that the analysis above implies that for the special
case considered here the size and pattern of the responses of output and
domesticinflationtothemonetarypolicyshocksdonotdifferfromthose
intheclosedeconomy.

244 CHAPTER8
8.4 OPTIMAL MONETARYPOLICY:ASPECIAL CASE
Thissectionderivesandcharacterizestheoptimalmonetarypolicyforthe
smallopeneconomydescribedabove,aswellastheimplicationsofthat
policy for a number of macroeconomic variables. The analysis, which
follows closely that of Galí and Monacelli (2005), is restricted to the
specialcaseforwhichasecond-orderapproximationtothewelfareofthe
representativeconsumercanbeeasilyderivedanalytically.Itsconclusions
should thus not be taken as applying to a more general environment.
Instead, this exercise is presented as an illustration of the approach to
optimalmonetarypolicydesigninanopeneconomyratherthanthebasis
forarobustpolicyprescription.
ThebasicNewKeynesianmodelofaclosedeconomyprovidesauseful
benchmark for the analysis here. As discussed in chapter 4, under the
assumption of a constant employment subsidy τ that neutralizes the
distortion associated with firms’ market power, the optimal monetary
policy in that model is the one that replicates the flexible price equilib-
riumallocation.Theintuitionforthatresultisstraightforward:Withthe
subsidyinplace,thereisonlyonedistortionleftatworkintheeconomy,
namely, sticky prices. By stabilizing markups at their frictionless level,
nominal rigidities cease to be binding, since firms do not feel any desire
to adjust prices. By construction, the resulting equilibrium allocation is
efficient,andthepricelevelremainsconstant.
In an open economy—and as noted, among others, by Corsetti and
Pesenti (2001)—an additional factor beyond the presence of market
power distorts the incentives of the monetary authority to deviate from
theflexiblepriceequilibriumallocation:thepossibilityofinfluencingthe
termsoftradeinawaybeneficialtodomesticconsumers.Thispossibility
is a consequence of the imperfect substitutability between domestic and
foreign goods (which makes the terms of trade a function of relative
supplies),combinedwithstickyprices(thatrendermonetarypolicynon-
neutral). Furthermore, the strength of the incentive to deviate from the
flexiblepriceequilibriumallocationisafunctionofthepreferenceshock.
As a result, and as shown below, the introduction of an employment
subsidy that exactly offsets firms’ market power distortion is in general
notenoughtorendertheflexiblepriceequilibriumallocationoptimalfor,
at the margin, the monetary authority has an incentive to deviate from
thatallocationinordertoimprovethetermsoftrade.10
However, as shown below, for the special parameter configuration
σ = η = 1, and in the absence of preference shocks (i.e., assuming
10SeealsothediscussioninBenignoandBenigno(2003)inthecontextofatwo-country
model.

POLICYINTHEOPENECONOMY 245
Z = 1, for all t), there is a constant employment subsidy that exactly
t
offsets the combined effects of market power and the terms of trade
distortions. Under the assumption that such a subsidy is in place, the
flexible price equilibrium allocation becomes optimal. The policy that
maximizes welfare in that case requires that domestic inflation be fully
stabilized, while allowing the nominal exchange rate (and, as a result,
CPIinflation)toadjustasneededinordertoreplicatetheresponseofthe
termsoftradethatwouldbeobservedunderflexibleprices.
One may wonder to what extent the desirability of strict domestic
inflation targeting is specific to the special case considered here or
whether it constitutes a good approximation for a more general case of
the model developed above. The optimal policy analysis undertaken in
Faia and Monacelli (2008), using a model nearly identical to the one
considered here, suggests that while the optimal policy involves some
variationinthedomesticpricelevel,thelatterisalmostnegligiblefroma
quantitativepointofview,thusmakingstrictdomesticinflationtargeting
a good approximation to the optimal policy (or at least conditional on
theproductivityshocks considered here).Usingadifferentapproach, de
Paoli(2009a)reachesasimilarconclusion,exceptwhenan(implausibly)
highelasticityofsubstitutionisassumed.11Buteveninthelattercase,the
losses that arise from following a domestic inflation targeting policy are
negligible.12 More generally, it is clear that there are several channels in
theopeneconomythatmaypotentiallyrenderastrictdomesticinflation
policysuboptimal,includinganonunitaryelasticityofsubstitution,local
currency pricing, incomplete financial markets, and so on, all of which
are unrelated to the sources of policy tradeoffs that may potentially
arise in the closed economy. Furthermore, the presence of sources of
fluctuationsotherthantechnology(e.g.,preferenceshocks)mayalsolead
toanoptimalpolicythatdeviatesfromstrictdomesticinflationtargeting.
The analysis of the quantitative significance of the effects of those
channels(individuallyorjointly)isbeyondthescopeofthischapter.
Withthatconsiderationinmind,letusnextturntotheanalysisofthe
optimalpolicyinthespecialcasementionedabove(i.e.,σ = η = 1,and
nopreferenceshocks).
11 Those results are conditional on productivity shocks being the driving force. Not
surprisingly, in the presence of cost-push shocks of the kind considered in chapter 5,
stabilizingdomesticinflationisnotoptimal(asintheclosedeconomy).
12 In solving the optimal policy problem for the general case, de Paoli (2009a) adopts
the linear-quadratic approach originally developed in Benigno and Woodford (2005),
which replaces the linear terms in the approximation to the households’ welfare losses
using a second-order approximation to the equilibrium conditions. Faia and Monacelli
(2008)solvefortheRamseypolicyusingtheoriginalnonlinearequilibriumconditionsas
constraintsofthepolicyproblem.

246 CHAPTER8
8.4.1 TheEfficientAllocationandItsDecentralization
Let us first characterize the optimal allocation from the viewpoint of
a social planner facing the same resource constraints to which the
small open economy is subject in equilibrium (in relation to the rest
of the world), given the assumption of complete markets. In that
case, the optimal allocation must maximize U(C,N;Z) subject to (i)
t t t
the technological constraint Y = AN1−α, (ii) a consumption/output
t t t
possibilities set implicit in the international risk sharing condition (16),
and(iii)themarketclearingcondition(24).
Under the special case of σ = η = 1, and Z = 1 for all t considered
t
here, (16) and (24) can be used to derive an exact consumption/output
possibilitiessetundercompletemarkets,whichtakestheform:
C
=Y1−υ
(Y
∗
)
υ
t t t
Note that, in contrast with the closed economy, the elasticity of
consumptionwithrespecttodomesticoutputisnotone,but1−υinstead.
The optimal allocation (from the viewpoint of the small open economy,
whichtakesworldoutputasgiven)mustsatisfytheoptimalityconditions
U (C,N) C
− n t t =(1−υ)(1−α) t
U (C,N) N
c t t t
which,undertheassumedpreferencesandgivenσ =1,canbewrittenas
C
C N ϕ =(1−υ)(1−α) t
t t N
t
thus implying a constant optimal level of employment N = [(1 − υ)
×(1−α)]1+ 1 ϕ.
Consider, on the other hand, the flexible price equilibrium allocation.
Inthelatterthegrosspricemarkupisconstantandsatisfies
M= P H,t
W/MPN
t t
(1−α)(Y/N)
= t t
(1−τ)C N ϕSυ
t t t
(1−α)
=
(1−τ)N1+ϕ
t
wherethethirdequalityholdsinthespecialcaseconsideredhere.

POLICYINTHEOPENECONOMY 247
Hence, by setting τ such that (1−τ)(1−υ)M = 1, the optimality
of the flexible price equilibrium allocation is guaranteed. Note that the
required subsidy is smaller than necessary to offset firms’ market power
distortion, in order to exploit the gains from a more favorable terms of
tradebroughtaboutbyasomewhatlowerdomesticoutput.
With the optimal subsidy in place, and as in the closed economy of
chapter3,theoptimalmonetarypolicyrequiresstabilizingtheoutputgap
(i.e.,(cid:21)y =0,forallt).Equation(37)thenimpliesthatdomesticpricesare
t
alsostabilizedunderthatoptimalpolicy(i.e.,π
H,t
=0forallt).Thus,in
the special case under consideration, (strict) domestic inflation targeting
(SDIT)isindeedtheoptimalpolicy.
8.4.2 ImplementationandMacroeconomicImplications
This section discusses the implementation of a strict domestic inflation
targeting policy and characterizes some of its equilibrium implications.
While that policy has been shown to be optimal only for the special
case considered above, its implications for the general case can also be
considered.
8.4.2.1 IMPLEMENTATION
Asdiscussedabove,fullstabilizationofdomesticpricesimplies
(cid:21)y
t
=π
H,t
=0
for all t. This in turn implies that y = yn and i = rn will hold in
t t t t
equilibrium for all t, with all the remaining variables matching their
naturallevelsatalltimes.
For the reasons discussed in chapter 4, an interest rate rule of the
form i = rn is associated with an indeterminate equilibrium, and
t t
hence, does not guarantee that the outcome of full price stability be
attained.Thatresultfollowsfromtheequivalencebetweenthedynamical
system describing the equilibrium of the small open economy and that
of the closed economy, as discussed in chapter 4. As shown there, the
indeterminacy problem can be avoided, and the uniqueness of the price
stability outcome restored by having the central bank follow a rule that
makes the interest rate respond with sufficient strength to deviations of
domestic inflation and/or the output gap from target. More precisely,
the central bank can guarantee that the desired outcome is attained by
committingtoaruleoftheform
i t =r t n+φ π π H,t (42)

248 CHAPTER8
whereφ
π
>1.Inequilibrium,thetermφ
π
π
H,t
vanishes(becauseπ
H,t
=0
forallt),implyingthati =rn,forallt.
t t
8.4.2.2 MACROECONOMICIMPLICATIONS
Under a strict domestic inflation targeting policy, the behavior of real
variables in the small open economy corresponds to the one that would
be observed in the absence of nominal rigidities. Hence, it is seen from
theinspectionofequation(35)thatdomesticoutputalwaysincreasesin
response to a positive technology shock at home. As discussed earlier,
thesignoftheresponsetoariseinworldoutputisambiguous,however,
anddependsonthesignof(cid:21) ∗,whichinturndependsontheelasticityof
substitutionηandtheriskaversionparameterσ.
Asshownabovethenaturallevelofthetermsoftradeisgivenby
s
t
n =σ υ(y
t
n−y
t
∗ )−(1−υ)(cid:18)z
t
=σ υ[(cid:21) a a t +(cid:21) z z t +((cid:21) ∗ −1)y t ∗ ]−(1−υ)(cid:18)z t
=σ υ (cid:21) a a t +σ υ((cid:21) ∗ −1)y t ∗+[σ υ (cid:21) z −(1−υ)(cid:18)]z t
Thus, given world output, an improvement in domestic technology
always leads to a real depreciation, through its expansionary effect on
domestic output. Positive preference shocks z generate a real apprecia-
t
tion, since σ υ (cid:21) z −(1−υ)(cid:18) < 0. On the other hand, changes in world
outputhaveaneffectonthetermsoftradeofambiguoussign.
Given that domestic prices are fully stabilized under DIT, it follows
that eDIT = sn − p∗ , that is, the nominal exchange rate moves one-
t t t
for-one with the (natural) terms of trade and (inversely) with the world
price level. Assuming constant world prices, the nominal exchange rate
will inherit all the statistical properties of the natural terms of trade.
In particular, in response to technology shocks, the nominal exchange
rateunderDITwillbeproportionaltothegapbetweenthenaturallevel
of domestic output (in turn related to productivity) and world output.
Thus, the volatility of the nominal exchange rate will tend to be high
(low) when domestic natural output displays a weak (strong) positive
comovementwithworldoutput.
TheimpliedequilibriumprocessfortheCPIcanalsobederived.Given
theconstancyofdomesticpricesitisgivenby
pDIT =υsn
t t
=υ(eDIT+ p ∗ )
t t

POLICYINTHEOPENECONOMY 249
Thus,itisseenthatundertheDITregime,theCPIlevelwillalsovary
withthe(natural)termsoftradeandwillinherititsstatisticalproperties.
If the economy is very open, and if domestic productivity (and hence,
the natural level of domestic output) is not much synchronized with
world output, CPI prices could potentially be highly volatile, even if the
domesticpricelevelisconstant.
An important lesson emerges from the previous analysis: Potentially
large and persistent fluctuations in the nominal exchange rate, as well
as in some inflation measures (like the CPI), are not necessarily un-
desirable, nor do they require a policy response aimed at dampening
such fluctuations. Instead, and especially for an economy that is very
open and subject to large idiosyncratic shocks, those fluctuations may
be an equilibrium consequence of the adoption of an optimal policy, as
illustratedbythemodelabove.
8.4.3 TheWelfareCostsofDeviationsfromtheOptimalPolicy
Under the particular assumptions under which strict domestic inflation
targeting has been shown to be optimal (i.e., log utility, a unit elasticity
of substitution between domestic and foreign goods and no preference
shocks),itisrelativelystraightforwardtoderiveasecond-orderapprox-
imation to the discounted utility losses of the domestic representative
consumer associated withdeviations fromtheoptimalpolicy.Asshown
in appendix 8.1, those losses, expressed as a fraction of steady state
consumption,canbewrittenas(ignoringtermsindependentofpolicy):
(cid:7)(cid:7) (cid:8) (cid:8)
(1−υ) (cid:1)∞ 1+ϕ (cid:4)
W= βt (cid:21)y2+ π2 (43)
2 1−α t λ H,t
t=0
The expected period welfare losses of any policy that deviates from
strict inflation targeting can be written in terms of the variances of
inflationandtheoutputgap
(cid:24)(cid:7) (cid:8) (cid:25)
(1−υ) 1+ϕ (cid:4)
V= 2 1−α var((cid:21)y t )+ λ var(π H,t ) (44)
Notethatthepreviousexpressionsforthewelfarelossesare,uptothe
multiplicative term (1−υ), identical to the ones derived for the closed
economyinchapter4,withdomesticinflationbeingtherelevantinflation
variable here. Below, (44) is used to assess the welfare implications of
alternative monetary policy rules and to rank those rules on welfare
grounds.

250 CHAPTER8
8.5 SIMPLE MONETARYPOLICY RULES FOR
THESMALL OPEN ECONOMY
This section analyzes the macroeconomic implications of alternative
monetarypolicyrulesforthesmallopeneconomy.Thefirstrule,already
analyzed in the previous section, is strict domestic inflation targeting
(SDIT,forshort),whichrequires
π
H,t
=0
for all t. Under the second rule considered, referred to as strict CPI
inflation targeting (SCIT, for short), consumer price inflation is fully
stabilized:
π =0
t
for all t. The third rule is an exchange rate peg (PEG, for short), which
canbeformallyrepresentedas
e =0
t
forallt (whichinturnrequiresthati =i∗,alsoforallt).
t t
In addition to the previous rules, two stylized Taylor-type rules
are considered, which can be thought of as flexible versions of the
inflation targeting rules specified above, allowing for some concern for
output fluctuations. The first has the domestic interest rate respond
systematically to domestic inflation and output, whereas the second
assumes that CPI inflation is the variable the domestic central bank
reactsto(inadditiontooutput).Formally,theflexibledomesticinflation
targeting(FDIT,forshort)isspecifiedas
i t =0.01+1.5π H,t +0.125(cid:18)y t
whereas the flexible CPI inflation targeting rule (FCIT, for short) is
givenby
i =0.01+1.5π +0.125(cid:18)y
t t t
forallt,wherethesizeofthecoefficientsisbasedontheoriginalTaylor
(1993)rule.
Below, a comparison is provided of the equilibrium properties of
several macroeconomic variables under the above simple rules for a
calibratedversionofthesmallopeneconomymodeldevelopedabove.13
13 SeeGalíandMonacelli(2005)forasimilaranalysis(thoughwithaslightlydifferent
calibration).

POLICYINTHEOPENECONOMY 251
TABLE8.1
PropertiesofSimplePolicyRules
SDIT SCIT PEG FDIT FCIT
σ(y) 2.29 1.92 1.72 1.85 1.76
σ((cid:1)y) 0 0.66 0.92 0.44 0.62
σ(π ) 0 0.19 0.35 0.69 0.58
H
σ(π) 0.41 0 0.21 0.70 0.52
σ(s) 2.29 1.92 1.72 1.85 1.76
σ((cid:11)e) 1.02 0.29 0 0.95 0.59
L 0 0.05 0.17 0.61 0.43
8.5.1 AQuantitativeAnalysisofAlternativeRules
8.5.1.1 CALIBRATION
This section presents some quantitative results based on a calibrated
version of the small open economy. The baseline calibration assumes
σ = η = 1 in a way consistent with the special case considered above.
A baseline value for υ (the degree of openness) is set at 0.4. The latter
correspondsroughlytotheimport/GDPratioinCanada,whichistaken
asaprototypesmallopeneconomy.Theremainingparametersaresetat
the values found in the baseline calibration of chapter 3. The analysis is
restrictedtotechnologyshocks.14
8.5.1.2 MACROECONOMICVOLATILITYANDWELFARELOSSES
Table 8.1 reports the standard deviations of several key variables under
thealternativemonetarypolicyrulesintroducedabove.Acriticalelement
that distinguishes each simple rule relative to the optimal policy is the
excess smoothness of both the terms of trade and the (first-differenced)
nominal exchange rate.15 This in turn is often reflected in too high a
volatilityoftheoutputgapanddomesticinflation.Inparticular,thePEG
regime is the one that amplifies both output gap and domestic inflation
volatility to the largest extent, with the CITR regime lying somewhere
in between. Note also that the terms of trade are more stable under
an exchange rate peg than under any other policy regime, but this is
not reflected in smaller welfare losses. That finding, which is consistent
with the evidence of Mussa (1986), points to the existence of “excess
smoothness” in the real exchange rate under a nominal exchange rate
14 Notethatunder theassumed calibration, changes inworld output donothaveany
effectonthedomesticeconomy.
15Statisticsarereportedforthenominaldepreciationrate,asopposedtothelevel,given
theunitrootinthenominalexchangerate.

252 CHAPTER8
peg. That feature is a consequence of the inability of prices (which are
sticky)tocompensatefortheconstancyofthenominalexchangerate.16
Thelastrowintable8.1reportsthewelfarelossesassociatedwiththe
alternative policy rules introduced above, expressed as a percentage of
steady state consumption. Under the baseline calibration all rules other
than SDIT are suboptimal because they involve nontrivial deviations
from the efficient/natural allocation. Note that both Taylor rules imply
substantially larger welfare losses than the other three rules considered,
largely due to their implied higher volatility in domestic inflation.
However,andasisusuallythecaseinwelfareexercisesofthissortfound
intheliterature,theimpliedwelfarelossesarequantitativelysmallunder
allpolicyregimes.
8.6 NOTES ON THELITERATURE
Earlierworkonoptimizingopeneconomymodelswithnominalrigidities
focused on the transmission of monetary policy shocks, typically repre-
sentedasdisturbancestoanexogenousstochasticprocessforthemoney
supply.17 AkeycontributioninthatareaisObstfeldandRogoff(1995),
who develop a two-country model where monopolistically competitive
firms set prices before the realization of the shocks (i.e., one period
in advance). The framework is used to analyze the dynamics of the
exchange rate and other variables in response to a change in the money
supply(andgovernmentspending)andthewelfareeffectsresultingfrom
that intervention. An earlier paper, by Svensson and van Wijnbergen
(1989) contains a related analysis under the assumption of full risk-
sharingamongconsumersfromdifferentcountries.
Corsetti and Pesenti (2001) develop a version of the Obstfeld-Rogoff
modelthatallowsforhomebiasinpreferences,leadingtotermsoftrade
effectsthatarearguedtohavepotentiallyimportantwelfareeffects.Betts
and Devereux (2000) revisit the analysis in Obstfeld and Rogoff (1995)
whiledepartingfromtheassumptionofthelawofonepricefoundinthe
latter paper. In particular, they allow firms to price discriminate across
marketsassumingtheysetprices(inadvance)intermsofthecurrencyof
theimportingcountry(“pricingtomarket”).
The effects of money supply shocks on the persistence and volatility
of nominal and real exchange rates are analyzed under the assump-
tion of staggered price setting in Kollmann (2001) and Chari, Kehoe,
16SeeMonacelli(2004)foradetailedanalysisoftheimplicationsoffixedexchangerates.
17SeeLane(1999)foranexcellentsurveyofthatliterature.

POLICYINTHEOPENECONOMY 253
and McGrattan (2002).18 The assumption of staggered price setting
(and staggered wage setting in Kollmann’s case) induces much richer
and more realistic dynamics than that of price setting one period in
advance.
Amorerecentstrandoftheliteraturehasattemptedtogobeyondthe
analysis of the transmission of exogenous monetary policy shocks, and
has focused instead on the implications of sticky price open economy
models for the design of optimal monetary policy, using a welfare
theoretic approach.19 Early examples of papers analyzing the properties
of alternative monetary policy arrangements in a two-country setting
assumedthatpricesaresetoneperiodinadvance.Theyincludethework
of Obstfeld and Rogoff (2002) and Benigno and Benigno (2003), both
using the assumption of producer currency pricing. Bacchetta and van
Wincoop (2000), Sutherland (2006), Devereux and Engel (2003), and
Corsetti and Pesenti (2005) use the same assumption in the context of
economieswithlocalcurrencypricing.
More recent frameworks have instead adopted the staggered price-
setting structure à la Calvo. Galí and Monacelli (2005), on which much
the analysis of the present chapter is built, is an illustration of work
along those lines for a small open economy. Their analysis uncovers
the assumptions under which replicating the flexible price equilibrium
allocation through full stabilization of domestic prices is optimal, in
what amounts to an open economy version of the “divine coincidence”
result discussed in chapter 4. Those assumptions include producer
currencypricing,completeassetmarkets,logutilityofconsumption,and
a unit elasticity of substitution between domestic and foreign goods.
An extension of that framework, incorporating cost-push shocks and
featuring tradeoffs similar to those analyzed in chapter 5 can be found
in Clarida, Galí, and Gertler (2001). Kollmann (2002) considers a
more general model of a small open economy with several sources of
shocks, and carries out a numerical analysis of the welfare implications
of alternative rules. Erceg, Gust, and López-Salido (2009) analyze the
role of openness in the transmission of shocks using a version of the
Galí-Monacellimodelthatincorporates staggeredwage settinginaway
analogous to the model in chapter 6. Galí and Monacelli (2014) study
thegains fromincreased wage flexibility insuch a framework, and their
dependenceontheexchangeratepolicy.
18Kollmann(2001)assumespricesandwagesaresetàlaCalvo—asinthemodelofthe
presentchapter—whereasChari,Kehoe,andMcGrattan(2002)assumepricesettingàla
Taylor,i.e.,withdeterministicpricedurations.
19 Ball (1999) and Svensson (2000) carry out an analysis similar in spirit, but in the
contextofnonoptimizingmodels.

254 CHAPTER8
Several papers have examined the consequences on optimal monetary
policy of departures from the benchmark assumptions of the Galí-
Monacelli model in closely related models. Faia and Monacelli (2008)
and de Paoli (2009a) study an environment with more general prefer-
ences, and show how the size of the elasticity of substitution between
domestic and foreign goods affects the extent to which the central bank
wantstostabilizetheexchangerate(thusdepartingfromstrictdomestic
inflationtargeting),inordertoimprovewelfare.DePaoli(2009b)shows
how the conclusions from that analysis need to be modified when the
assumption of complete markets is relaxed. Using a similar framework
as a starting point, Monacelli (2005) shows that the introduction of
imperfect pass-through generates a tradeoff between stabilization of
domesticinflationandtheoutputgap,leadingtogainsfromcommitment
similartothoseanalyzedinchapter5fortheclosedeconomy.Campolmi
(2014) introduces staggered wage setting in a small open economy
(coexisting with staggered price setting, as in the closed economy of
chapter 6). She shows that the presence of sticky wages generally
makes CPI inflation targeting more desirable than domestic inflation
targeting.
Incontrastwiththepreviousreferences,whichstudymonetarypolicy
in a small open economy, a number of papers have framed their
analysisofmonetarypolicydesigninthecontextoftwo-countrymodels
with staggered price setting à la Calvo. The papers by Clarida, Galí,
and Gertler (2002), Pappa (2004), and Benigno and Benigno (2006)
provide examples of that literature, with a special focus on the gains
from cooperation, and under the assumption of producer currency
pricing. Engel (2011) studies the implications for optimal monetary
policyofassuminglocalcurrencypricinginsteadinanotherwisesimilar
framework, showing how that modification warrants a focus on CPI—
rather than domestic price—stabilization. Benigno (2009) studies the
implications of incomplete asset markets and financial imbalances in a
similar environment, showing that those factors may justify a deviation
from a strict domestic inflation targeting policy. Woodford (2009)
uses a similar framework to study the challenges posed by trade and
financial integration on domestic monetary policy. Corsetti, Dedola,
and Leduc (2010) provide a unified treatment of the consequences
of deviations from the assumptions underlying the divine coincidence
result.
Finally, Galí and Gertler (2009) contains a number of contributions
that use related frameworks to understand different aspects of the
internationaldimensionofmonetarypolicy.

POLICYINTHEOPENECONOMY 255
APPENDIX
8.1 ASECOND-ORDERAPPROXIMATIONTOWELFARELOSSESINTHE
SMALLOPENECONOMY
This appendix derives a second-order approximation to the utility of
therepresentativehouseholdinthesmallopeneconomyanalyzedabove
for the special case of σ = η = 1, when the economy remains in a
neighborhoodofanefficientsteadystate(i.e.,whentheoptimalconstant
subsidyderivedinthemaintextisinplace).
Usingthesameapproachasinappendix4.1,thesecond-orderTaylor
expansion of U ≡ U(C,N;Z) around a steady state (C,N;1) can be
t t t t
writtenforthespecialcaseathandas
(cid:7) (cid:8)
1+ϕ
U −U (cid:8)U C(cid:18)c (1+z)+U N (cid:18)n(1+z)+ (cid:18)n2 +t.i.p.
t c t t n t t 2 t
(cid:7)
U N (cid:4)
=U c C (1−υ)(cid:18)y t (1+z t )+ 1− n α (cid:18)y t (1+z t )+ 2(cid:17) var i {p H,t (i)}
(cid:8)
1
+ (1+ϕ)(1−α)(cid:18)n2 +t.i.p.
2 t
wherethefacthasbeenusedthat(cid:18)c =(1−υ)(cid:18)y +υ(cid:18)y∗+ςz holdsforthe
t t t t
assumedspecialcase.
As shown in the main text, efficiency of the steady state implies
−Un =(1−υ)(1−α)Ct.Henceonecanwrite:
Uc Nt
(cid:26) (cid:27)
U −U 1−υ (cid:4)
U
t
C
(cid:8)−
2 (cid:17)
var
i
{p
H,t
(i)}+(1+ϕ)(1−α)(cid:18)n2
t
+t.i.p.
c
Accordingly,asecond-orderapproximationtotheconsumer’swelfare
losses can be written and expressed as a fraction of steady state
consumption(anduptoadditivetermsindependentofpolicy)as
(cid:7) (cid:8)
(cid:1)∞ U −U
W=−E βt t
0
U C
t=0 c
1−υ (cid:1)∞ (cid:2) (cid:4) (cid:3)
=− 2 E 0 βt (cid:17) var i {p H,t (i)}+(1+ϕ)(1−α)(cid:18)n2 t
t=0

256 CHAPTER8
The final step consists in rewriting the terms involving the price
dispersion variable as a function of inflation. In order to do so, make
useofthefollowinglemma,whichcarriesoverfromtheclosedeconomy
case
(cid:28) (cid:28)
Lemma2: ∞
t=0
βt var
i
{p
H,t
(i)}=
(1−βθ
θ
)(1−θ)
∞
t=0
βtπ
H
2
,t
Proof: Woodford(2003,chap.6)
Using the fact that λ ≡ (1−θ)(1−βθ) (cid:17), the previous lemma can be
θ
combinedwiththeexpressionforthewelfarelossesabovetoobtain
1−υ (cid:1)∞ (cid:26)(cid:2) (cid:4) (cid:3) (cid:27)
W=− E βt π2+(1+ϕ)(1−α)(cid:18)n2
2 0 λ t t
t=0
Notethatintheabsence ofpreferenceshocks, yn = a andnn = nfor
t t t
all t in the special case considered, thus implying (cid:21)y = (1−α)(cid:18)n, which
t t
allowsonetorewritethelossfunctionintermsofdomesticinflationand
theoutputgapas:
1−υ (cid:1)∞ (cid:24)(cid:2) (cid:4) (cid:3) (cid:7) 1+ϕ (cid:8) (cid:25)
W= E βt π2+ (cid:21)y2
2 0 λ t 1−α t
t=0
REFERENCES
Bacchetta, Philippe, and Eric van Wincoop (2000): “Does Exchange Rate
Stability Increase Trade and Welfare?,” American Economic Review 90(5),
1093–1109.
Ball,Laurence(1999):“PolicyRulesforOpenEconomies,”inJ.B.Taylor,ed.,
MonetaryPolicyRules,127–144,UniversityofChicagoPress,Chicago.
Benigno,Pierpaolo(2009):“PriceStabilitywithImperfectFinancialIntegration,”
JournalofMoneyCreditandBanking41(1),121–149.
Benigno, Gianluca, and Pierpaolo Benigno (2003): “Price Stability in Open
Economies,”ReviewofEconomicStudies70(4),743–764.
Benigno, Gianluca, and Pierpaolo Benigno (2006): “Designing Targeting Rules
for International Monetary Policy Cooperation,” Journal of Monetary Eco-
nomics53(3),473–506.
Benigno,Pierpaolo,andMichaelWoodford(2005):“InflationStabilizationand
Welfare: The Case of a Distorted Steady State,” Journal of the European
EconomicAssociation3(6),1185–1236.
Betts, Caroline, and Michael B. Devereux (2000): “Exchange Rate Dynamics
inaModelofPricing-to-Market,”JournalofInternationalEconomics50(1),
215–244.

POLICYINTHEOPENECONOMY 257
Campolmi,Alessia(2014):“WhichInflationtoTarget?ASmallOpenEconomy
withStickyWages,”MacroeconomicDynamics,18(1),145–174.
Chari,V.V.,PatrickKehoe,andEllenMcGrattan(2002):“MonetaryShocksand
RealExchangeRatesinStickyPriceModelsofInternationalBusinessCycles,”
ReviewofEconomicStudies69(3),533–563.
Clarida, Richard, Jordi Galí, and Mark Gertler (2001): “Optimal Monetary
Policy in Open vs. Closed Economies: An Integrated Approach,” American
EconomicReview91(2),248–252.
Clarida, Richard, Jordi Galí, and Mark Gertler (2002): “A Simple Framework
forInternationalMonetaryPolicyAnalysis,”JournalofMonetaryEconomics
49(5),879–904.
Corsetti,Giancarlo,LucaDedola,andSylvainLeduc(2010):“OptimalMonetary
Policy in Open Economies,” in B. Friedman and M. Woodford, eds., Hand-
bookofMonetaryEconomics,vol.3B,861–934,North-Holland,Amsterdam.
Corsetti, Giancarlo, and Paolo Pesenti (2001): “Welfare and Macro-
economic Interdependence,” Quarterly Journal of Economics 116(2),
421–446.
Corsetti, Giancarlo, and Paolo Pesenti (2005): “International Dimensions of
MonetaryPolicy,”JournalofMonetaryEconomics52(2),281–305.
de Paoli, Bianca (2009a): “Monetary Policy and Welfare in a Small Open
Economy,”JournalofInternationalEconomics77,11–22.
de Paoli, Bianca (2009b): “Monetary Policy under Alternative Asset Market
Structures: The Case of a Small Open Economy,” Journal of Money, Credit
andBanking41(7),1301–1330.
Devereux,MichaelB.,andCharlesEngel(2003):“MonetaryPolicyintheOpen
Economy Revisited: Exchange Rate Flexibility and Price Setting Behavior,”
ReviewofEconomicStudies70(4),765–783.
Engel,Charles(2011):“CurrencyMisalignmentsandOptimalMonetaryPolicy:
ARe-examination,”AmericanEconomicReview101(6),2796–2822.
Erceg, Christopher, Christopher Gust, and David López-Salido (2009): “The
Transmission of Domestic Shocks in Open Economies,” in J. Galí and
M. Gertler, eds., International Dimensions of Monetary Policy, 89–148,
UniversityofChicagoPress,Chicago.
Faia, Ester and Tommaso Monacelli (2008): “Optimal Monetary Policy in a
SmallOpenEconomywithHomeBias,”JournalofMoneyCreditandBanking
40,721–750.
Galí, Jordi, and Mark Gertler, eds. (2009): International Dimensions of Mone-
taryPolicy,UniversityofChicagoPress,Chicago.
Galí, Jordi, and Tommaso Monacelli (2005): “Monetary Policy and Exchange
RateVolatilityinaSmallOpenEconomy,”ReviewofEconomicStudies72(3),
707–734.
Galí, Jordi, and Tommaso Monacelli (2014): “Understanding the Gains from
WageFlexibility:TheExchangeRateConnection,”mimeo.
Kollmann, Robert (2001): “The Exchange Rate in a Dynamic Optimizing Cur-
rent Account Model with Nominal Rigidities: A Quantitative Investigation,”
JournalofInternationalEconomics55(2),243–262.

258 CHAPTER8
Kollmann,Robert(2002):“MonetaryPolicyRulesintheOpenEconomy:Effects
on Welfare and Business Cycles,” Journal of Monetary Economics 49(5),
989–1015.
Lane,PhilipR.(1999):“TheNewOpenEconomyMacroeconomics:ASurvey,”
JournalofInternationalEconomics54,235–266.
Monacelli,Tommaso(2004):“IntotheMussaPuzzle:MonetaryPolicyRegimes
andtheRealExchangeRateinaSmallOpenEconomy,”JournalofInterna-
tionalEconomics62(1),191–217.
Monacelli,Tommaso(2005):“MonetaryPolicyinaLowPass-ThroughEnviron-
ment,”JournalofMoney,CreditandBanking37(6),1048–1066.
Mussa,Michael(1986):“NominalExchangeRateRegimesandtheBehaviorof
RealExchangeRates,”Carnegie-RochesterConferenceSeriesonPublicPolicy
25,117–213.
Obstfeld, Maurice, and Kenneth Rogoff (1995): “Exchange Rate Dynamics
Redux,”JournalofPoliticalEconomy103(3),624–660.
Obstfeld, Maurice, and Kenneth Rogoff (2002): “Global Implications of Self-
OrientedNationalMonetaryRules,”QuarterlyJournalofEconomics117(2),
503–535.
Pappa,Evi(2004):“ShouldtheFedandtheECBCooperate?OptimalMonetary
Policy in a Two-Country World,” Journal of Monetary Economics 51(4),
753–780.
SutherlandAlan(2006):“TheExpenditureSwitchingEffect,WelfareandMon-
etaryPolicyinaSmallOpenEconomy,”JournalofEconomicDynamicsand
Control30,1159–1182.
Svensson,LarsE.O.(2000):“Open-EconomyInflationTargeting,”Journalof
InternationalEconomics50(1),155–183.
Svensson, Lars E. O., and Sweder van Wijnbergen (1989): “Excess Capacity,
MonopolisticCompetition,andInternationalTransmissionofMonetaryDis-
turbances,”EconomicJournal99,785–805.
Woodford, Michael (2003): Interest and Prices: Foundations of a Theory of
MonetaryPolicy,PrincetonUniversityPress,Princeton,NJ.
Woodford, Michael (2009): “Globalization and Monetary Control,” in J. Galí
and M. Gertler, eds., International Dimensions of Monetary Policy, 13–77
UniversityofChicagoPress,Chicago.
EXERCISES
8.1. Asmallopeneconomymodel
Consider a small open economy where no international trade in
assetsisallowed(implyingthattradeisalwaysbalanced).Hence,
p t +c t = p H,t +y t
where c t denotes consumption, y t is output, p H,t is the domestic
price level, and p is the CPI (all in logs). Assuming a constant
t

POLICYINTHEOPENECONOMY 259
pricelevelintherestoftheworld(p∗ =0),
t
p t =(1−υ)p H,t +υe t
wheree isthenominalexchangerate.
t
Let s t ≡ e t − p H,t denote the terms of trade. Under the
assumptionofaunitelasticityofsubstitutionbetweenforeignand
domesticgoods,
s = y −y ∗
t t t
where y∗ is (log) output in the rest of the world (assumed to
t
evolve exogenously). The domestic aggregate technology can be
writtenas
y =a +n
t t t
where a is an exogenous technology process. Assume perfect
t
competitioninbothgoodsandlabormarketswithflexibleprices
andwages.Thelaborsupplytakestheform
w − p =σc +ϕn
t t t t
Finally, assume a money demand function of the form
m − p =c .
t t t
a. Determinetheequilibriumprocessesforoutput,consumption,
thetermsoftrade,andthenominalexchangerateinthesmall
openeconomy,asafunctionofproductivitya ,foreignoutput
t
y∗,andthemoneysupplyundertheassumptionthatthelatter
t
evolvesexogenously.Discusstheimplicationsofassumingσ =
1.
b. Howwouldyouranswerhavetobemodifiedifafixednominal
exchangerateregimewereinplace?
c. Discuss,inwords,howsomeoftheresultsin(a)and(b)would
change qualitatively in the presence of imperfect competition
andstickyprices.
8.2. Theeffectsoftechnologyshocksintheopeneconomy
Considerthesmallopeneconomymodeldescribedinthischapter.
The equilibrium dynamics for domestic inflation π H,t and the
outputgap(cid:21)y aredescribedbytheequations
t
π H,t =β E t {π H,t+1 }+κ υ (cid:21)y t
1
(cid:21)y t = E t {(cid:21)y t+1 }− σ (i t −E t {π H,t+1 }−r t n)
υ

260 CHAPTER8
andwherern isgivenby
t
rn =ρ−ψ a
t ra t
Naturaloutputisinturngivenby
yn =ψ a
t ya t
ThetechnologyparameterfollowsastationaryAR(1)process
a t =ρ a a t−1 +ε t a
whereρ ∈[0,1).
a
Assumethatthemonetaryauthorityfollowsthesimpleinterest
raterule
i t =ρ+φ π π H,t
whereφ
π
>1.
a. Determinetheresponseofoutput,domesticinflation,theterms
oftrade,andthenominalexchangeratetoapositivedomestic
technology shock (note: for the purposes of this exercise
assume y∗ = p∗ =0forallt).
t t
b. Supposethatthecentralbankpegsthenominalexchange rate
sothate =0forallt.Characterizetheeconomy’sresponseto
t
atechnologyshockinthatcase.