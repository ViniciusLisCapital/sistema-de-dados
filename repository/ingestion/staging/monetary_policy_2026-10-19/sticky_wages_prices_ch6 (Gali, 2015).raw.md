Chapter 6
A MODEL WITH STICKY WAGES AND PRICES
Throughoutthepreviouschaptersthelabormarkethasbeenmodeledas
a perfectly competitive market, in which households and firms take the
wageasgiven.Thischapterdepartsfromthatassumptionbyintroducing
someimperfectionsinthelabormarketandanalyzingtheirconsequences
formonetarypolicy.Inparticular,itisassumedthathouseholds/workers
have some monopoly power, which allows them to set the wage for the
differentiatedlaborservicestheysupply.Furthermore,aswasdonewith
the price-setting firms in chapter 3, the assumption here is that workers
faceCalvo-typeconstraintsonthefrequencywithwhichtheycanadjust
nominalwages.
A key result emerges from the analysis of the model with sticky
wages and prices: fully stabilizing price inflation is no longer optimal.
Instead, the central bank should be concerned about both price and
wage stability, because fluctuations in both price and wage inflation, as
well as in the output gap, are a source of inefficiencies in the allocation
of resources that result in welfare losses for households. Accordingly,
the optimal policy seeks to strike a balance between three different
objectives, with the relative weights attached to them being a function
oftheunderlyingparametervalues.
Thechapterisorganizedasfollows.Section6.1describesabenchmark
model in which both sticky wages and sticky prices coexist. Section 6.2
derives the model’s log-linearized equilibrium conditions. Section 6.3
discusses the welfare-based criterion and analyzes the limiting cases of
full price flexibility and full wage flexibility. Section 6.4 derives and
characterizes the optimal monetary policy, while section 6.5 studies
the performance of alternative simple rules and their merits as an
approximation to the optimal policy. Section 6.6 concludes with some
bibliographicalnotes.
6.1 AMODEL WITH STAGGEREDWAGE ANDPRICE SETTING
Thissectionlaysoutamodelofaneconomyinwhichnominalwages,as
wellasprices,aresticky.FollowingErceg,Henderson,andLevin(2000),
wage stickiness is introduced in a way analogous to price stickiness, as

164 CHAPTER6
modeled in chapter 3. In particular, a continuum of differentiated labor
servicesisassumed,allofwhichareusedbyeachfirm.Eachperiodonly
theworkersspecializedina(randomlydrawn)subsetoflabortypescan
adjust their posted nominal wage. As a result, the aggregate nominal
wage responds sluggishly to shocks, generating inefficient variations in
theaveragewagemarkup.Inaddition,wageinflation,combinedwiththe
staggering of wage adjustments, brings about relative wage distortions
and an inefficient allocation of labor in a way symmetric to the relative
pricedistortionsgeneratedbypriceinflationinthepresenceofstaggered
pricesetting.
Next, the problem facing firms and households in this environment is
described.
6.1.1 Firms
As in chapter 3, a continuum of firms is assumed, indexed by i ∈ [0,1].
Each firm produces a differentiated good with a technology represented
bytheproductionfunction
Y(i)= AN(i)1−α (1)
t t t
whereY(i)denotestheoutputofgoodi, A isanexogenoustechnology
t t
parametercommontoallfirms,and N(i)isanindexoflaborinputused
t
byfirmi anddefinedby
(cid:1) (cid:3)
(cid:2) (cid:2)w
1 (cid:2)w−1
N t (i)≡ N t (i,j)1− (cid:2) 1 wdj (2)
0
where N(i, j)denotesthequantityoftype-j laboremployedbyfirmi in
t
period t. Note that parameter (cid:2) w represents the elasticity of substitution
amonglaborvarieties.Notealsotheassumptionofacontinuumoflabor
types,indexedby j ∈[0,1].
Let W(j) denote the nominal wage for type-j labor prevailing in
t
periodt,forall j ∈[0,1].Asdiscussedbelow,nominalwagesaresetby
workers of each type (or a union representing them) and taken as given
by firms. Given the wages effective at any point in time for the different
types of labor services, cost minimization yields a corresponding set of
demandschedulesforeachfirmi andlabortype j,giventhefirm’stotal
employment N(i)
t
(cid:4) (cid:5)
−(cid:2)
W(j) w
N(i, j)= t N(i) (3)
t t
W
t

STICKYWAGESANDPRICES 165
foralli, j ∈[0,1],where
(cid:1) (cid:3)
(cid:2) 1
1 1−(cid:2)w
W ≡ W(j)1−(cid:2) wdj (4)
t t
0
is an aggregate wage index. Substituting (3) into the definition of N(i),
t
onecanobtaintheconvenientaggregationresult
(cid:2)
1
W(j)N(i,j)dj = WN(i)
t t t t
0
thatis,thewagebillofanygivenfirmcanbeexpressedastheproductof
thewageindex W andthatfirm’semploymentindex N(i).
t t
Hence, and conditional on an optimal allocation of the wage bill
among the different types of labor implied by (3), a firm adjusting its
price in period t will solve the following problem, which is identical to
theoneanalyzedinchapter3,namely:
(cid:6)∞ (cid:7) (cid:8) (cid:9)(cid:10)
m P a ∗ x θ p kE t (cid:4) t,t+k (1/P t+k ) P t ∗ Y t+k|t −C t+k (Y t+k|t )
t k=0
subjecttothesequenceofdemandconstraints
(cid:4) (cid:5)
P∗ −(cid:2)
p
Y t+k|t = t C t+k (5)
P t+k
fork=0,1,2, ...where(cid:4) t,t+k ≡βkU c,t+k /U c,t isthestochasticdiscount
factor, C t (·) is the (nominal) cost function, and Y t+k|t denotes output in
period t +k for a firm that last reset its price in period t. Note that a
subscript/superscript p is added to price-related variables, to distinguish
themfromtheirwage-relatedcounterparts.
As shown in chapter 3, the aggregation of the resulting price-setting
rules yields, to a first-order approximation and in a neighborhood of
the zero inflation steady state, the following equation for price inflation
π t p ≡ p t − p t−1 ,
πp =βE{πp }−λ µ(cid:11)p (6)
t t t+1 p t
where, as in chapter 3, µ(cid:11)p≡µp − µp is the deviations of the av-
t t
erage (log) price markup from its flexible price counterpart, and

166 CHAPTER6
λ ≡(1−θ p)(1−βθ p) 1−α . Hence, and as discussed in chapter 3, the
p θ
p
1−α+α(cid:2)
p
presence (or anticipation) of average price markups below their desired
levels(i.e.,anegativeµ(cid:11)p)leadsfirmsthatcurrentlyadjustpricestoraise
t
thelatter,thusgeneratingpositiveinflation.
6.1.2 Households
The economy is populated by a large number of identical households.
Eachhouseholdismadeupofacontinuumofmembers,eachspecialized
in a different labor service, and indexed by j ∈ [0,1]. Income is pooled
within each household, which thus acts as risk sharing mechanism.
Atypicalhouseholdseekstomaximize
(cid:6)∞
E βtU(C,{N (j)};Z)
0 t t t
t=0
subjecttoasequenceofperiodbudgetconstraints
(cid:2) (cid:2)
1 1
P t (i)C t (i)di +Q t B t ≤ B t−1 + W t (j)N t (j)di +D t
0 0
for t = 0,1,2 ..., where N (j) is employment (or work hours) of type-
t (cid:12) (cid:14)
(cid:13) (cid:2)p
j labor (with W
t
(j) the corresponding wage), C
t
≡
0
1 C
t
(i) 1− (cid:2) 1 pdi (cid:2)p−1
is the consumption index, and the remaining variables are defined as
in chapter 3. In contrast with the model in that chapter, however,
(cid:13)
hereeachhouseholdtakesasgivenlaborincome 1 W(j)N (j)dj,since,
0 t t
individually,ithasnoinfluenceonwages(setbyunions)oremployment
(determined by firms). Thus, the only decisions made by households
involve the optimal allocation of consumption expenditures among
different good varieties and the optimal intertemporal allocation of
consumption. As in chapter 3, those decisions give rise, respectively, to
theoptimalityconditions
(cid:4) (cid:5)
−(cid:2)
P(i) p
C(i)= t C (7)
t t
P
t
foralli ∈[0,1],and
(cid:15) (cid:16)
Q =βE U c,t+1 P t (8)
t t
U c,t P t+1

STICKYWAGESANDPRICES 167
Theperiodutilityisassumedtobegivenby:
(cid:1) (cid:3)
(cid:2)
 C
t
1
1
−
−
σ −
σ
1
−
1 N
1
t
(
+
j)1
ϕ
+ϕ
dj Z
t
forσ (cid:6)=1
U(C t ,{N t (j)};Z t )=  (cid:4)
logC −
(cid:13)
1
0
N
t
(j)1+ϕ
dj
(cid:5)
Z forσ =1
t 0 1+ϕ t
wherez ≡ logZ followsanexogenous AR(1)process
t t
z t =ρ z z t−1 +ε t z
Hencetheintertemporaloptimalityconditioncanberewrittenas:
(cid:21)(cid:4) (cid:5) (cid:4) (cid:5)(cid:4) (cid:5)(cid:22)
−σ
Q =βE C t+1 Z t+1 P t
t t
C t Z t P t+1
whichcanberepresentedinlog-linearizedformas:
1 1
c t = E t {c t+1 }− σ (i t −E t {π t p +1 }−ρ)+ σ (1−ρ z )z t (9)
usingthenotationintroducedinchapters2and3.
Nexttheproblemofwagesettingisdescribed.
6.1.2.1 WAGESETTING
Let us first consider how workers specialized in a given type of labor
(or the union representing them) set their wage. Wage rigidities are
introducedinawayanalogoustothegoodsmarket.Specifically,workers
specializedinanygivenlabortypecanresettheirnominalwageonlywith
probability 1−θ w each period, independently of the time elapsed since
theylastadjustedtheirwage.Equivalently,eachperiodthenominalwage
forworkersofanygiventyperemainsunchangedwithprobabilityθ w.
Consider thus a union resetting its members’ wage in period t, and
let W∗ denote the newly set wage. The union chooses W∗ in a way
t t
consistent with utility maximization of its members’ households, taking
asgiventhedecisionsofotherunionsaswellasallthepathforaggregate
consumptionandprices.Specifically,theunionwillseektomaximize
(cid:1) (cid:3)
E t (cid:6) k ∞ =0 (βθ w)k C t − + σ kP W t+ t ∗ k N t+k|t − 1 N t + 1 + + k ϕ ϕ |t Z t+k (10)

168 CHAPTER6
subjecttothesequenceoflabordemandschedules
(cid:4) (cid:5) (cid:1) (cid:2) (cid:3)
W∗ −(cid:2) w 1
N t+k|t = t N t (i)di
W t+k 0
for k=0,1,2,3, ... where N t+k|t denotes the level of employment in
periodt+kamongworkersthatlastresettheirwageinperiodt.
The first-order condition associated with the problem above is
givenby
(cid:15) (cid:4) (cid:5)(cid:16)
(cid:6)
k
∞
=0
(βθ w)kE t N t+k|t Z t+k C t − + σ kP W
t+
t ∗
k
+M wN t ϕ +k|t =0
wh L e e r t e ti M ng w M ≡ R (cid:2) S w (cid:2) t − w + 1 k . |t ≡C t σ +k N t ϕ +k|t denotethemarginalrateofsubstitution
betweenhouseholdconsumptionandemploymentinperiodt+krelevant
to the workers resetting their wage in period t, the optimality condition
abovecanberewrittenas
(cid:15) (cid:4) (cid:5)(cid:16)
(cid:6)∞ W∗
k=0 (βθ w)kE t N t+k|t Z t+k C t − + σ k P t+ t k −M wMRS t+k|t =0 (11)
Notethatinthelimitingcaseoffullwageflexibility(θ
w
=0),
W∗ W
t = t =M wMRS t|t
P P
t t
forallt.Thus,M w isthewedgebetweentherealwageandthemarginal
rateofsubstitutionthatprevailsintheabsenceofwagerigidities,thatis,
thedesiredorfrictionlessgrosswagemarkup.
Notealsothatinaperfectforesightzeroinflationsteadystate
W∗ W
= =M wMRS
P P
Log-linearizing (11) around that steady state yields, after some alge-
braicmanipulation,thefollowingapproximatewagesettingrule
(cid:6)∞ (cid:7) (cid:10)
w t ∗ =µw+(1−βθ w) (βθ w)kE t mrs t+k|t + p t+k (12)
k=0
whereµw≡ logM w andmrs t+k|t ≡σc t+k +ϕn t+k|t .

STICKYWAGESANDPRICES 169
The intuition behind wage setting rule (12) is straightforward. First,
w∗ isincreasinginexpectedfutureprices,becausehouseholdscareabout
t
thepurchasingpoweroftheirnominalwage.Second,w∗ isincreasingin
t
theexpectedaveragemarginaldisutilityoflabor(intermsofgoods)over
the life of the wage, because households want to adjust their expected
averagerealwageaccordingly.
Lettingmrs t+k ≡σc t+k +ϕn t+k definet (cid:13) he (cid:13) economy’saveragemarginal
rate of substitution, where n t+k ≡ log 0 1 0 1 N t (i, j)d j d i denotes (log)
aggegrateemployment.Then,anduptoafirstorderapproximation:
mrs t+k|t =mrs t+k +ϕ(n t+k|t −n t+k )
=mrs t+k −(cid:2) w ϕ(w t ∗−w t+k )
Hence,(12)canbewrittenas
w t ∗ = 1 1 − + β (cid:2) w θ ϕ w (cid:6)∞ (βθ w)kE t {µ w +mrs t+k +(cid:2) w ϕw t+k + p t+k }
k=0
= 1 1 − + β (cid:2) w θ ϕ w (cid:6)∞ (βθ w)k E t (cid:7) (1+(cid:2) w ϕ)w t+k −µ(cid:11)w t+k (cid:10)
k=0
(cid:8) (cid:9)
=βθ wE t {w t ∗ +1 }+(1−βθ w) w t −(1+(cid:2) w ϕ) −1µ(cid:11)w t (13)
where µ(cid:11)w≡µw − µw denotes the deviations of the economy’s (log)
t t
average wage markup µw≡(w − p)−mrs from its steady state level
t t t t
µw.
6.1.2.2 WAGEINFLATIONDYNAMICS
Giventheassumedwagesettingstructure,theevolutionoftheaggregate
wageindex(4)isgivenby
(cid:12) (cid:14)
1
W
t
= θ wW
t
1
−
−
1
(cid:2) w +(1−θ w)(W
t
∗ )1−(cid:2) w 1−(cid:2)w
The previous equation can be log-linearized around the zero (wage)
inflationsteadystatetoyield
w t =θ w w t−1 +(1−θ w)w t ∗ (14)
Combining (13) and (14), and letting π t w = w t − w t−1 denote
wage inflation yields, after some manipulation, the baseline wage

170 CHAPTER6
inflationequation
π t w =βE t {π t w +1 }−λ w µ(cid:11)w t (15)
where λ w ≡(1− θ w θ ( w 1 ) + (1 (cid:2) − w β ϕ θ ) w). Note that this wage inflation equation has a
form analogous to (6), the equation describing the dynamics of price
inflation. The intuition behind it is identical: When the average wage in
theeconomyisbelowthelevelconsistentwithmaintaining(onaverage)
thedesiredmarkup,workersreadjustingtheirnominalwagewilltendto
increasethelatter,thusgeneratingpositivewageinflation.
Inthismodelwageinflationequation(15)replacesconditionw −p =
t t
mrs , one of the optimality conditions associated with the household’s
t
problemusedextensivelyinpreviouschapters.Theimperfectadjustment
of nominal wages implies that, in response to shocks, the average real
wage will not move one-for-one with the average marginal rate of
substitution, leading to variations in the average wage markup and in
wageinflation,asimpliedby(15).
6.2 EQUILIBRIUM
AsinthebasicNewKeynesianmodelofchapter3,goodsmarketclearing
requiresY(i)=C(i)forallt andi ∈[0,1].ThisinturnimpliesY =C
t t (cid:12) (cid:14) t t
(cid:13) (cid:2)p
forallt,whereY
t
≡
0
1 Y
t
(i) 1− (cid:2) 1 pdi (cid:2)p−1 isanindexofaggregateoutput.
Inlogs,
y =c
t t
forallt.Aggregateemploymentisgivenby
(cid:2) (cid:2)
1 1
N ≡ N(i, j)djdi
t t
0 0
(cid:2) (cid:2)
1 1 N(i, j)
= N(i) t djdi
t
N(i)
0 0 t
(cid:2)
1
=(cid:12) w,t N t (i)di
0

STICKYWAGESANDPRICES 171
(cid:4) (cid:5) (cid:2) (cid:4) (cid:5)
=(cid:12) w,t
Y
t
1− 1 α 1 Y
t
(i) 1− 1 α
di
A Y
t 0 t
(cid:4) (cid:5)
1
=(cid:12) (cid:12)
Y
t
1−α
w,t p,t
A
t
(cid:13) (cid:8) (cid:9) (cid:13) (cid:8) (cid:9)
where (cid:12) w,t ≡
0
1 W
W
t(
t
j) −(cid:2) wdj and (cid:12) p,t ≡
0
1 P
P
t(
t
i) − 1− (cid:2)p αdi. Thus, the fol-
lowing relation between (log) aggregate output and (log) aggregate
employmentholds
(1−α)n t = y t −a t +dw,t +d p,t
(cid:13) (cid:8) (cid:9)
w × 2 (cid:2) (cid:13) p h (cid:13) e 0 1 v re a (cid:8) r P i P t { ( t i d p ) w (cid:9) t ( , − 1 t i − (cid:2) ) ≡ p α } d . ( i 1 U . s A i − n s g s α a h n ) o l w o a g n n a 0 l 1 i o n g W o a W u t p ( t s j p ) e d − n e (cid:2) d r w i i d v x a j t 4 io .1 a n n , d o o f ne c d h p c a , a t p n ≡ te ( s r 1 ho 4 w − , d d p w α ,t , ) t lo (cid:7) (cid:7) g
(1−α)(cid:2) w var {w (j)}. Hence, and up to a first order approximation, one
2 j t
canwrite:
(1−α)n = y −a
t t t
which can be thought of as a labor demand equation, determining
employmentasafunctionofoutput,giventechnology.
Nextaversionoftheequationsforpriceandwageinflationintermsof
theoutputgap(cid:23)y ≡y −ynisderived.Importantly,theconceptofnatural
t t t
output yn used in this chapter is to be understood as referring to the
t
equilibriumlevelofoutputwhenbothpricesandwagesarefullyflexible.
A new variable, the real wage gap, is introduced and denoted by ω(cid:23) and
t
formallydefinedas
ω(cid:23) ≡ω −ωn
t t t
whereω ≡w −p denotestherealwage,andwhereωnisthenaturalreal
t t t t
wage,thatis,therealwagethatwouldprevailintheabsenceofnominal
rigidities,andwhichisgivenby
ωn =log(1−α)+(a −αnn)−µp
t t t
=log(1−α)+ψ wa a t −µp (16)
whereψ wa ≡1− 1 α − ψ α ya >0andψ ya ≡ σ(1− 1 α + )+ ϕ ϕ+α (asderivedinchapter3).

172 CHAPTER6
First, the average price markup is related to the output and real wage
gaps.Usingthefactthatµp =mpn −ω ,
t t t
µ(cid:11)p =(mpn −ω )−µp
t t t
=((cid:23)y −(cid:23)n)−ω(cid:23)
t t t
α
=− (cid:23)y −ω(cid:23) (17)
1−α t t
Hence,combining(6)and(17)yieldsthefollowingequationforprice
inflationasafunctionoftheoutputandrealwagegaps
πp =βE{πp }+κ (cid:23)y +λ ω(cid:23) (18)
t t t+1 p t p t
whereκ ≡ αλ p.
p 1−α
Similarly,
µ(cid:11)w =ω −mrs −µw
t t t
=ω(cid:23) −(σ(cid:23)y +ϕ(cid:23)n)
t t t
(cid:4) (cid:5)
ϕ
=ω(cid:23) − σ + (cid:23)y (19)
t 1−α t
Combining (15) and (19) yields an analogous version of the wage
inflationequationintermsoftheoutputandrealwagegaps
π t w =βE t {π t w +1 }+κ w (cid:23)y t −λ w ω(cid:23) t (20)
(cid:8) (cid:9)
whereκ w ≡λ w σ + 1− ϕ α .
Inaddition,thereisanidentityrelatingthechangesinthewagegapto
priceinflation,wageinflation,andthenaturalwage
ω(cid:23) t ≡ω(cid:23) t−1 +π t w−π t p−(cid:12)ω t n (21)
In order to complete the nonpolicy block of the model, equilibrium
conditions (18), (20), and (21) must be supplemented with a dynamic
IS equation familiar from earlier chapters, and which can be derived
by combining the goods market clearing condition y =c with the
t t
Euler equation (9). The resulting expression is rewritten in terms of the

STICKYWAGESANDPRICES 173
outputgapas
1
(cid:23)y t =− σ (i t −E t {π t p +1 }−r t n)+E t {(cid:23)y t+1 } (22)
wherethenaturalinterestratern≡ρ−σ(1−ρ )ψ a +(1−ρ )z,derived
t a ya t z t
as in chapter 3, should now be understood as the prevailing real rate in
anequilibriumwithflexiblewagesandflexibleprices.
Finally, and in order to close the model, how the interest rate is
determinedmustbespecified.Thisisdonebypostulatinganinterestrate
ruleoftheform
i t =ρ+φ p π t p+φ w π t w+φ y (cid:11)y t +v t (23)
wherev isanexogenouscomponentnormalizedtohavezeromean.
t
Plugging(23)into(22)toeliminatetheinterestrate,theresultingequa-
tion and the remaining conditions (18), (20), and (21), the equilibrium
dynamicscanberepresentedbymeansofasystemoftheform
A w 0 x t =A w 1 E t {x t+1 }+B w 0 u t (24)
wherex t ≡[(cid:23)y t ,π t p,π t w,ω(cid:23) t−1 ](cid:8),u t ≡[(cid:11)r t n−v t −φ y (cid:11)y t n,(cid:12)ω t n](cid:8),
 
σ +φ y φ p φ w 0
 
 −κ 1 0 0
A
w≡ 

p 

0  −κ w 0 1 0
0 −1 1 1
 
σ 1 0 0  
  1 0
A
w≡  

0 β 0 λ p  
; B
w≡  

0 0  

1 0 0 β −λ w  0 0 0
0 1
0 0 0 1
Note that {u } can in turn be expressed as a linear transformation
t
of the exogenous technology, preference, and monetary policy shifters
{a ,z,v }.
t t t
An important property of (24) is worth emphasizing at this point: In
general,thesystemdoesnothaveasolutionsatisfying(cid:23)y =πp =πw =0
t t t
forallt.Thisisthecaseevenundertheassumptionthattheinterceptof

174 CHAPTER6
theinterestrateruleadjustsone-for-onetovariationsinthenaturalrate
ofinterest(v =(cid:11)rn,forallt)combinedwithφ =0,incontrastwiththe
t t y
basic model analyzed in chapters 3 and 4. An implication of that result
isthattheallocationassociatedwiththeequilibriumwithflexibleprices
andwagescannotbeattainedinthepresenceofnominalrigiditiesinboth
goods and labor markets. The intuition for the previous result rests on
theideathatinorderfortheconstraintsonpriceandwagesettingnotto
bebinding(andhence,nottodistorttheequilibriumallocation)allfirms
and workers should view their current prices and wages as the desired
ones. This makes any adjustment unnecessary and leads to constant
aggregate price and wage levels, that is, zero inflation in both markets.
Note, however, that such an outcome implies a constant real wage,
which will generally be inconsistent with the flexible price/flexible wage
allocation.Onlywhenthenaturalwageisconstant(sothat(cid:12)ωn =0for
t
allt)andφ =0,andaslongasthecentralbankadjuststhenominalrate
y
one-for-one with changes in the natural rate (i.e., v = (cid:11)rn for all t) the
t t
outcome (cid:23)y = πp = πw = 0 for all t is a solution to (24) and, hence, is
t t t
consistent with equilibrium. Note, however, that the natural wage will
not be constant as long as technology shocks are present (as (16) makes
clear).
A second question of interest relates to the conditions that the rule
(23) must satisfy to guarantee a unique stationary equilibrium or,
equivalently, a unique stationary solution to the system of difference
equations (24). Given that vector x contains three non-predetermined
t
variables and one predetermined variable, (local) uniqueness requires
that three eigenvalues of Aw≡(Aw)−1Aw lie inside, and one outside, the
0 1
unitcircle.1 Undertheassumptionofnon-negativevaluesforcoefficients
(φ
p
,φ w,φ
y
),theconditionforuniquenessisgivenby:2
(cid:1) (cid:3)(cid:4) (cid:5)
1−β 1 1
φ
p
+φ
w
+φ
y σ + α+ϕ λ
+
λ
>1
1−α p w
Note that in the special case of φ = 0 the previous condition
y
simplifiesto
φ
p
+φ
w
>1
or, what is equivalent, the central bank must adjust the nominal rate
morethanone-for-oneinresponsetovariationsinanyarbitraryweighted
1SeeBlanchardandKahn(1980).
2SeeFlaschel,FrankeandProaño(2008)andBlasselleandPoissonier(2013)foraproof.

STICKYWAGESANDPRICES 175
2.5
2
Determinacy
1.5
1
0.5
Indeterminacy
0
0 0.5 1 1.5 2 2.5
Figure6.1. DeterminacyandIndeterminacyRegions.
average of price and wage inflation. The previous condition can be
viewedasextendingtheTaylorprinciplerequirementdiscussedinearlier
chapters to the case where the central bank is allowed to respond
to wage inflation in addition to price inflation. As φ increases, the
y
lower bound on φ p +φ w consistent with a unique equilibrium declines,
as illustrated in figure 6.1, using the baseline calibration introduced
below.
6.2.1 DynamicResponsestoaMonetaryPolicyShock
Not surprisingly, the presence of staggered wage setting influences the
economy’sequilibriumresponsetodifferentshocks.Figure6.2illustrates
this point by displaying the responses of the output gap, price inflation,
wage inflation, and real wages to a monetary policy shock. Both
the policy intervention (a persistent increase in the interest rate rule

176 CHAPTER6
0.1 0.2
0.1
0
0
–0.1 –0.1
–0.2 –0.2
baseline –0.3
–0.3 flexible wages
–0.4
flexible prices
–0.4 –0.5
0 2 4 6 8 10 12 14 16 0 2 4 6 8 10 12 14 16
Output gap Price inflation
4 0.5
2
0
0
–2 –0.5
–4 –1
–6
–1.5
–8
–10 –2
0 2 4 6 8 10 12 14 16 0 2 4 6 8 10 12 14 16
Wage inflation Real wage
Figure6.2. DynamicResponsestoaMonetaryPolicyShock.
shifter v ) and the model’s calibration are identical to the analogous
t
experiment described in chapter 3. In particular, a simple policy rule
of the form (23) is assumed with φ =1.5 and φ =0.125. The only
p y
difference here is to allow for sticky wages, introduced as described
above. In order to disentangle the role played by each type of rigidity,
resultsareshownforthreealternativecalibrationsofθ
p
andθ w.Thefirst
calibrationcorrespondstoaneconomyinwhichpriceandwagerigidities
coexist.Asinourbaselinemodelofchapter3,itisassumedthatθ =3/4.
p
In addition, θ w =3/4 is set, which implies an average duration of wage
spells of four quarters. The latter assumption seems to accord with the
empirical evidence.3 The second calibration assumes sticky prices and
flexible wages (θ p =3/4, θ w =0) and, hence, corresponds to the basic
modelintroducedinchapter3.Finally,thethirdcalibrationcorresponds
to an economy with flexible prices and sticky wages (θ p =0, θ w =3/4).
Thepolicyinterventionconsistsofanincreaseof0.25percentagepoints
intheexogenouscomponentoftheinterestraterule.Thatchangewould
lead, in the absence of an endogenous component in the interest rate
3See,e.g.,Barattieri,Basu,andGottschalk(2014).

STICKYWAGESANDPRICES 177
rule, to an impact increase of one percentage point in the (annualized)
nominalinterestrate.Inaddition,weset(cid:2)
w
=4.5,avaluethatisjustified
in the next chapter as being consistent with an average unemployment
rateof5percent.Asintheanalogousexperimentofchapter3,assumean
autoregressive coefficient ρ v =0.5 in the AR(1) process followed by the
interest rate shifter. The remaining parameters are set at their baselines
values,asintroducedinchapter3.
Inordertointerprettheresultsshowninfigure6.2,itisusefultotake
the responses under sticky prices and flexible wages—already discussed
in chapter 3 and represented here by the lines with diamonds—as a
benchmark. The presence of both sticky wages and prices (responses
shown by the lines with circles) generates, not surprisingly, a more
mutedresponseofwageinflation.Thelatterpartlyexplainsthesluggish
responseoftherealwage,whichinturnreducestheimpactofthedecline
in activity on price markups and, hence, the limited size of the inflation
response. As a result, there is only a moderate endogenous response of
themonetaryauthoritytothelowerinflation,thusimplyingpersistently
higher interest rates, which in turn account for the larger decline in
output. By contrast, in the flexible wage economy the decline in activity
leadstoan(implausibly)largeandpersistentreductionintherealwage,
which amplifies the size of the price inflation drop and the endogenous
reactionofthemonetaryauthority,leadingtoamoremutedresponseof
output.
Consider next the consequences of assuming the coexistence of sticky
wagesandflexibleprices(impulseresponsesrepresentedbythelineswith
squares). Again, the presence of sticky wages dampens the response of
wage inflation to the contractionary monetary policy shock. But now,
and given the absence of constraints on price adjustment, price inflation
falls considerably in response to the decline in activity and the ensuing
lowermarginalcosts.Thelargedeclineinpricesinturnleadstoarisein
the average real wage that, in turn, dampens (and eventually overturns)
theeffectsoftheactivitydeclineonpriceinflation.
Neither the large negative response of wage inflation and the real
wage in the sticky price/flexible wage model, nor the large initial
decline in price inflation in the sticky wage/flexible price model appears
to be consistent with existing estimates of the dynamic effects of
exogenousmonetarypolicyshocks.Thelatterestimatesareinsteadmore
in line with the predictions of the model with both sticky prices and
wages.4
4See,e.g.,Christiano,Eichenbaum,andEvans(2005).

178 CHAPTER6
6.3 MONETARYPOLICY DESIGN WITH STICKY WAGES ANDPRICES
This section explores some of the normative implications of the coex-
istence of sticky prices and sticky wages, as modeled in the framework
above, for the conduct of monetary policy. In so doing, and in order
to keep the analysis as simple as possible, necessary assumptions are
made to guarantee that the natural allocation, that is, the equilibrium
allocation in the absence of nominal rigidities, is also the efficient
allocation.Giventheabsenceofmechanisms(e.g.,capitalaccumulation)
for the economy as a whole to transfer resources across periods, the
efficient allocation corresponds to the solution of a sequence of static
socialplannerproblemsoftheform
maxU(C,{N (j)};Z)
t t t
(cid:12) (cid:14)
(cid:13) (cid:2)p
where C
t
≡
0
1 C
t
(i) 1− (cid:2) 1 pdi (cid:2)p−1, subject to (1) and (2), as well as the
usual market clearing conditions. The optimality conditions for that
problemaregivenby
C(i)=C, alli ∈[0,1] (25)
t t
N(i, j)=N (j)= N(i)= N, alli, j ∈[0,1] (26)
t t t t
− U n,t = MPN (27)
t
U c,t
whereMPN ≡(1−α)AN−α.Notethatdemandshocks{Z}donotaffect
t t t t
theefficientallocation.
In the decentralized economy, if all firms and households reoptimize
their prices each period they will all choose the same prices and wages
and, hence, (25) and (26) will be satisfied. On the other hand, optimal
priceandwagesettingintheabsenceofnominalrigiditiesimplies
W t =− U n,t M
w
P t U c,t
and
(1−τ)W
P =M t
t p
MPN
t

STICKYWAGESANDPRICES 179
where τ is an employment subsidy, funded through lump sum taxes.
Notethatbysettingτ =1− 1 ,condition(27)isalsosatisfied,thus
M M
p w
guaranteeingtheefficiencyoftheflexibleprice/flexiblewageequilibrium
allocation. The latter property is assumed to hold for the remainder of
thischapter.
Appendix 6.1 derives a second-order approximation to households’
discountedutilityintheeconomywithstickywagesandprices,resulting
from fluctuations around a steady state with zero wage and price
inflation. When the latter is efficient, as is the case under the optimal
subsidy derived above, welfare losses, expressed as a fraction of steady
stateconsumption,aregivenby
(cid:30)(cid:4) (cid:5) (cid:31)
W=
1
E
(cid:6)∞
βt σ +
ϕ+α
(cid:23)y2+
(cid:2)
p (πp)2+
(cid:2) w(1−α)
(πw )2 +t.i.p.
2 0 t=0 1−α t λ p t λ w t
(28)
where t.i.p. collects various terms that are independent of policy. Thus,
by ignoring the latter terms, the average period welfare loss can be
writtenasalinearcombinationofthevariancesoftheoutputgap,price
inflation,andwageinflationgivenby
(cid:30)(cid:4) (cid:5) (cid:31)
L=
1
σ +
ϕ+α
var((cid:23)y)+
(cid:2)
p var(πp)+
(cid:2) w(1−α)
var(πw )
2 1−α t λ p t λ w t
(29)
Note that the relative weight of each of the variances is a function
of the underlying parameter values. The weights associated with output
gap and price inflation fluctuations are identical to those derived and
discussed in chapter 4 for a version of the model economy with
sticky prices and flexible wages. The presence of sticky wages implies
an additional source of welfare losses, associated with wage inflation
fluctuations. The contribution of wage inflation volatility to the welfare
losses is increasing in (i) the elasticity of substitution among labor types
((cid:2) w),(ii)theelasticityofoutputwithrespecttolaborinput1−α,and(iii)
the degree of wage stickiness θ w (which is inversely related to λ w). Note
that (i) and (ii) amplify the negative effect on aggregate productivity of
any given dispersion of wages across labor types, while (iii) raises the
degreeofwagedispersionresultingfromanygivenrateofwageinflation
differentfromzero.
In general, and as argued above, the lower bound of zero welfare
losses that characterizes an allocation where (cid:23)y =πp=πw=0 for all
t t t

180 CHAPTER6
t is not attainable. The optimal policy will thus have to strike a balance
instabilizingthethreeabovementionedvariables.
Inthelimitingcaseofflexiblewages,λ
w
−→+∞,andtheterminthe
lossfunctionassociatedwithwageinflationvolatilityvanishes(i.e.,wage
inflation is no longer costly). Note that in that case the wage markup is
constantandhence,
ω(cid:23) =σ(cid:23)c +ϕ(cid:23)n
t (cid:4) t t (cid:5)
ϕ
= σ + (cid:23)y
1−α t
which, substituted into (18), yields a New Keynesian Phillips curve
identicaltothatderivedinchapter3,namely,
πp =βE{πp }+κ (cid:23)y
t t t+1 p t
(cid:8) (cid:9)
whereκ ≡λ σ + ϕ+α .Accordingly,andasshowninchapter3,there
p p 1−α
is no longer a tradeoff between stabilization of price inflation and
stabilization of the output gap with the optimal policy requiring that
πp =(cid:23)y =0forallt.
t t
Similarly, in the limiting case of flexible prices (but sticky wages),
λ −→ +∞ so that only the terms associated with fluctuations in the
p
output gap and wage inflation remain a source of welfare losses. In that
case,andusingthefactthatpricemarkupswillbeconstant,
ω(cid:23) = (cid:23)y −(cid:23)n
t t t
α
=− (cid:23)y
1−α t
which,substitutedinto(20),yieldsthewage-inflationequation
π
t
w =βE
t
{π
t
w
+1
}+κ
w
(cid:23)y
t
(cid:8) (cid:9)
whereκ w ≡λ w σ + ϕ 1− + α α .Inthatcase,theoptimalpolicywillattainthe
zero lower bound for the welfare losses by fully stabilizing the output
gapandwageinflation,i.e.,πw =(cid:23)y =0forallt.
t t
Thus,withtheexceptionofthelimitingcaseoffullwageflexibility,a
policythatseekstostabilizepriceinflationcompletely(i.e.,astrictprice
inflationtargetingpolicy)willbesuboptimal.Thesameistrueforastrict
wage inflation targeting policy, with the exception of an economy with
fullyflexibleprices.

STICKYWAGESANDPRICES 181
6.4 OPTIMAL MONETARYPOLICY
Next, the optimal monetary policy is characterized in the economy in
which both prices and wages are sticky. For concreteness, the analysis
is restricted to the case of full commitment. The central bank seeks to
minimize(28)subjectto(18),(20),and(21)fort =0,1,2, ...Let{ζ 1,t },
{ζ
2,t
},and{ζ
3,t
}denotethesequenceLagrangemultipliersassociatedwith
the previous constraints, respectively. The optimality conditions for the
optimalpolicyproblemarethusgivenby
(cid:4) (cid:5)
ϕ+α
σ + 1−α (cid:23)y t +κ p ζ 1,t +κ w ζ 2,t =0 (30)
(cid:2)
λ p π t p−(cid:12)ζ 1,t +ζ 3,t =0 (31)
p
(cid:2) w(1
λ
−α)
π t w−(cid:12)ζ 2,t −ζ 3,t =0 (32)
w
λ p ζ 1,t −λ w ζ 2,t +ζ 3,t −βE t {ζ 3,t+1 }=0 (33)
for t = 0,1,2, ... which, together with the constraints (18), (20), and
(21)givenζ 1,−1 =ζ 2,−1 =0andaninitialconditionforω(cid:23) −1 ,characterize
the solution to the optimal policy problem. The equilibrium under the
optimalpolicyisrepresentedinacompactwayasthestationarysolution
tothedynamicalsystem
A ∗ 0 x t =A ∗ 1 E t {x t+1 }+B ∗ 0 (cid:12)a t
wherex t ≡[(cid:23)y t , π t p, π t w,ω(cid:23) t−1 ,ζ 1,t−1 , ζ 2,t−1 , ζ 3,t ](cid:8) andwhereA∗ 0 ,A∗ 1 ,and
B∗ aredefinedinappendix6.2.
0
6.4.1 TheCaseofDemandShocks
The optimal policy when demand shocks are the only source of fluc-
tuations is considered first. Note that in that case the equilibrium
correspondstothestationarysolutiontothesystem
A ∗ 0 x t =A ∗ 1 E t {x t+1 }
Thus, starting from a steady state (i.e., under the assumption that
ω(cid:23) −1 =0), the optimal policy requires full stabilization of the output and
wage gaps, price inflation, and wage inflation at a zero level, that is,
x =0forallt.5 Sinceneitherthenaturallevelofoutputnorthenatural
t
5Inthecaseω(cid:1)
−1
(cid:6)=0theoptimalpolicyimpliessometransitionaldynamics(neededto
bringbacktherealwagetoitssteadystatelevel),withxt =0holdingonlyasymptotically.

182 CHAPTER6
0.1 1
0
0.05
–1
0
–2
–0.05 baseline
flexible wages –3
flexible prices
–0.1 –4
0 2 4 6 8 10 12 14 16 0 2 4 6 8 10 12 14 16
Output gap Price inflation
4 1
3 0.8
2 0.6
1 0.4
0 0.2
–1 0
0 2 4 6 8 10 12 14 16 0 2 4 6 8 10 12 14 16
Wage inflation Real wage
Figure6.3. DynamicResponsestoaTechnologyShockundertheOptimal
MonetaryPolicy.
wage is affected by demand shocks, that outcome is associated with a
constantrealwageandoutput.
Inordertoimplementtheoptimalpolicy,thecentralbankcanfollow
arulethatadjuststhenominalrateone-for-onetochangesinthenatural
rate(whichisaffectedbythedemandshocks).Thus,therule
i =rn+φ πp
t t p t
where rn=ρ + (1 − ρ )z, and φ > 1 would implement the optimal
t z t p
policy under demand shocks, with the second term on the right-hand
side included in order to guarantee a unique equilibrium. The optimal
policy’soutcomewouldcorrespondtotheefficientallocation.
6.4.2 TheCaseofTechnologyShocks
Figure 6.3 displays the responses of the output gap, price and wage
inflation, and the real wage to a positive technology shock under the
optimal policy, for the three parameter calibrations considered earlier.
Note that, as shown in chapter 4, with sticky prices but flexible wages
(lines with diamonds) the optimal policy implies full stabilization of the

STICKYWAGESANDPRICES 183
price level and thus no effect on price inflation. Because that policy
replicates the flexible price/flexible wage equilibrium allocation, the
responses of both output and the real wage correspond to their natural
counterparts, with the necessary adjustment of the real wage attained
through large and persistent wage inflation that, given the assumed
flexibilityofwages,causesnodistortions.
Whenpricesareflexiblebutwagesaresticky(representedbythelines
with squares), and in a way consistent with the discussion in section
6.3, the natural allocation can also be attained, though now it requires
full stabilization of nominal wages and, hence, zero wage inflation. The
latterrequirementinturnimpliesthattheadjustmentintherealwagebe
achieved through negative price inflation that, given the assumption of
flexibleprices,isnolongercostlyintermsofwelfare.
When both prices and wages are sticky the natural allocation can no
longer be attained. In that case, the optimal policy strikes a balance
between attaining the output and real wage adjustments warranted by
the rise in productivity and, on the other hand, keeping wage and price
inflation close to zero to avoid the distortions associated with nominal
instability. As a result, and in response to a positive technology shock,
the real wage rises but not as much as the natural wage (note that the
latter coincides with the response under the two previous calibrations).
Given the convexity of welfare losses in price and wage inflation, it is
optimaltoraisetherealwagesmoothly,throughamixofnegativeprice
inflation and positive wage inflation. Note finally that the output gap
deviates from zero in response to the shock, though such deviations are
quantitativelyverysmall.
Next, a particular configuration of parameter values is examined for
which the optimal policy takes a simple form that can be characterized
analytically.
6.4.3 ASpecialCasewithanAnalyticalSolution
Consider the special case with κ p = κ w ≡κ and (cid:2) p = (cid:2) w(1 − α)≡(cid:2).
In that case optimality conditions (30), (31), and (32) in the monetary
policyproblemcanberewrittenas:6
1
π =− (cid:12)(cid:23)y (34)
t (cid:2) t
6 The derivation of that result makes(cid:2)use of t(cid:3)he fact, obtained by combining the
definitionsofκ wandκ p,thatκ=
λ
λ
p
p
+
λ
λ
w
w
σ+ϕ
1−
+
α
α .

184 CHAPTER6
fort =1,2,3, ...aswellas
1
π =− (cid:23)y (35)
0 (cid:2) 0
where
λ λ
π ≡ w πp+ p πw
t λ +λ t λ +λ t
p w p w
is a weighted average of price and wage inflation, henceforth referred
to as composite inflation, in which the relative weight associated
with wage (price) inflation is increasing in the degree of wage (price)
rigidities.
Note also that, independent of parameter values, one can always
combine the wage and price inflation equations (18) and (20) to obtain
the following version of the New Keynesian Phillips curve in terms of
compositeinflation
π t =βE t {π t+1 }+κ(cid:23)y t (36)
Thus, (36) implies that there is no tradeoff between stabilization of
the output gap and stabilization of the particular composite measure of
inflationintroducedabove.Thusitispossibletofullystabilizecomposite
inflationandtheoutputgapatzero,thatis,
π =0
t
and
(cid:23)y =0
t
for t=0,1,2, ... But under the special case considered here, such a
policy it is not only feasible but also optimal, since it satisfies the
optimalityconditions(34)and(35).
Thus, in the particular case considered here, the optimal policy takes
asimpleform:The central bank should focus uniquely on targeting and
fullystabilizingaweightedaverageofpriceandwageinflation,withthe
weights determined by underlying parameters. In particular, the relative
weightofprice(wage)inflationisincreasinginthedegreeofprice(wage)
stickiness.
A nice feature of the optimal policy in the particular case analyzed
above is that its implementation by the monetary authority does not
rely on the output gap being observable: It suffices that the monetary

STICKYWAGESANDPRICES 185
authority keeps track of the composite inflation measure, and responds
(aggressively)toanydeviationfromzeroofthatmeasure.Thisisthusan
instance in which the divine coincidence result introduced in chapter 4
obtains.
Of course, and as seen above for the general case, the optimal policy
does not have such a simple characterization, requiring instead that the
centralbankfollowsamuchmorecomplicatedtargetrulesatisfying(18),
(20), (30), (31), (32), and (33) simultaneously. In that context, it is of
interest to know to what extent different simple monetary policy rules
maybeabletoapproximatetheoptimalpolicy,anissuethatisattended
tointhefollowingsection.
6.5 EVALUATION OF SIMPLE RULES UNDERSTICKY
WAGES ANDPRICES
This section considers a number of simple monetary policy rules and
provides a quantitative evaluation of their impact on welfare. That
evaluation is based on the average period losses implied by each simple
rule,givenby(29).
Sixdifferentsimplerulesareanalyzed.Thefirstrule,whichisreferred
to as strict price inflation targeting, requires that price inflation be zero
at all times (πp=0 for all t). Also assumed is an analogous rule for
t
wage inflation, that is, a strict wage inflation targeting rule (πw=0
t
for all t). The third rule stabilizes the weighted average of price and
wage inflation introduced in the previous section. That rule is referred
to as a strict composite inflation targeting rule. As shown above, that
rule is optimal only under a very specific configuration of the model’s
parameters (which is not the case for the baseline calibration). But even
when those conditions are not satisfied, that rule has a special interest
because, as implied by (36), it is equivalent to a rule that fully stabilizes
theoutputgap.
Theremainingthreerulesconsideredtaketheformofasimpleinterest
raterule
i =0.01+1.5π
t t
where π refers, respectively, to price inflation, wage inflation, or com-
t
posite inflation. These rules are referred to as flexible (price, wage, or
composite)inflationtargetingrules.
The top panel of table 6.1 reports the main findings of that exercise
when variations in the technology shifter a are the only source of
t

186 CHAPTER6
TABLE6.1
EvaluationofSimpleRules
Optimal StrictTargeting FlexibleTargeting
Price Wage Composite Price Wage Composite
Technologyshocks
σ(πp) 0.11 0 0.13 0.12 0.29 0.24 0.24
σ(πw) 0.03 0.26 0 0.02 0.23 0.16 0.16
σ((cid:1)y) 0.04 3.38 0.20 0 0.84 1.18 1.11
L 0.0330 0.78 0.039 0.0337 0.47 0.305 0.307
Demandshocks
σ(πp) 0 0 0 0 0.02 0.04 0.03
σ(πw) 0 0 0 0 0.05 0.06 0.06
σ((cid:1)y) 0 0 0 0 1.08 1.05 1.06
L 0 0 0 0 0.061 0.067 0.066
fluctuations. That variable is assumed to follow an AR(1) process with
an autoregressive coefficient ρ = 0.9 and a standard deviation of 0.01
a
for its innovation. The remaining parameters are set at their baseline
values. For each simple rule, the implied standard deviation of price
inflation, wage inflation, and the output gap is reported, as well as the
corresponding average period welfare loss. In addition to the simple
rules, the table also reports the corresponding statistics for the optimal
policy,whichprovidesausefulbenchmark.
Anumberofresultsareworthhighlighting.Theoptimalpolicyimplies
near-constancy of the output gap, and a standard deviation of wage
inflationthatisaboutathirdthatofpriceinflation.Theimpliedwelfare
losses (relative to the unattainable first-best allocation) are very small,
about1/30ofapercentofsteadystateconsumption.Amongthesimple
rules, the one that fully stabilizes composite inflation does, for practical
purposes,aswellastheoptimalpolicy,generatingaverysimilarpattern
of volatilities of the three welfare-relevant variables. Given that, under
thebaselinecalibration,wageinflationhasaweightof0.85incomposite
inflation, it is perhaps not surprising that strict wage inflation targeting
ranks second among the simple rules considered, with implied losses
only slightly above those of the optimal policy. Interestingly, under this
baseline calibration, strict price inflation targeting rules are the worst,
largelyduetothelargefluctuationsinwageinflationandtheoutputgap
thatresultfromfollowingthoserules.Amongtheflexibletargetingrules,
the one that responds to price inflation does worse, though it improves
on its strict targeting counterpart. Both wage and composite inflation
targeting,intheirflexibleform,performworsethantheirstricttargeting
counterparts.

STICKYWAGESANDPRICES 187
The bottom panel of table 6.1 reports the corresponding results
conditional on demand shocks. Specifically, z is assumed to follow
t
an AR(1) process with autoregressive coefficient 0.5 and a standard
deviation of 0.01 for its innovation. As discussed above, the optimal
policy is consistent with the efficient allocation in this case, implying
no welfare losses. That policy can be implemented by fully stabilizing
any of the three inflation measures considered, implying in turn the full
stabilization of the output gap and hence a form of divine coincidence.
The flexible targeting policies, on the other hand, fall short of attaining
theefficientallocation,generatinganon-negligiblevolatilityintheoutput
gap.
Overall, the message conveyed by the exercise of this section can be
viewedastwofold.First,inthepresenceofstickywages(coexistingwith
stickyprices),policiesthatfocusexclusivelyonstabilizingpriceinflation
are clearly suboptimal, especially in the presence of technology shocks.
Second,whentechnologyshocksarepresentandintheabsenceoffurther
imperfections, a policy that responds aggressively to an appropriate
weightedaverageofpriceandwageinflationemergesasamostdesirable
one. Of course, choosing the appropriate weights remains a challenge.
A policy that gives a slightly dominant weight to wage inflation in the
definitionofthatcompositeperformsaswellastheoptimalpolicyforall
practical purposes. Interestingly, that conclusion appears at odds with
the practice of most central banks, which seem to attach little weight
to wage inflation as a target variable, with the interest in that variable
oftenlimitedtoitsabilitytoinfluence(andthushelppredict)currentand
futurepriceinflationdevelopments.
6.6 NOTES ON THE LITERATURE
Early examples of nonoptimizing rational expectations models with
nominal wage rigidities can be found in the work of Fischer (1977) and
Taylor(1980).CooleyandCho(1995)andBénassy(1995)wereamong
the first papers that embedded the assumption of sticky nominal wages
in a dynamic stochastic general equilibrium model, and examined its
implications for the properties of a number of variables in the presence
ofbothrealandmonetaryshocks.
Erceg, Henderson, and Levin (2000) developed the New Keynesian
modelwithbothstaggeredpriceandstaggeredwagecontractsàlaCalvo
that has become the framework of reference in the literature, and on
which much of this chapter builds. The focus of their paper was, like
this chapter, on the derivation of the implications for monetary policy.
A similar focus, including a discussion of the special case in which

188 CHAPTER6
targeting a weighted average of wage and price inflation is optimal, can
be found in Woodford (2003, chap. 6) and Giannoni and Woodford
(2003).Otherworkhasfocusedinsteadontheimpactofstaggeredwage
setting on the persistence of the effects of monetary policy shocks. See,
for example, Huang and Liu (2002) and, especially, Woodford (2003,
chap. 3) for a detailed discussion of the role of wage stickiness in that
regard.
Staggered wage setting is also a common feature of medium-scale
models like those of Kim (2000), Smets and Wouters (2003, 2007), and
Christiano,Eichenbaum,andEvans(2005).Thosemodelsalsoallowfor
some degree of wage indexation to prices. An analysis of the optimal
implementable rules in a medium-scale model can be found in Schmitt-
GrohéandUribe(2006).
APPENDIX
6.1 ASECOND-ORDERAPPROXIMATIONTOWELFARELOSSESWITHPRICE
ANDWAGESTICKINESS
A second-order Taylor expansion to the representative household’s
period t utility around the steady state, combined with a goods market
clearingcondition,yields:
(cid:4) (cid:5) (cid:2) (cid:4) (cid:5)
C −C 1 N (j)−N
U −U (cid:7)U C t +U N t dj
t c n
C N
0
(cid:4) (cid:5) (cid:2) (cid:4) (cid:5)
1 C −C 2 1 1 N (j)−N 2
+ U C2 t + U N2 t dj
cc nn
2 C 2 N
0
(cid:4) (cid:5)(cid:4) (cid:5)
C −C Z −Z
+U C t t
c
C Z
(cid:4) (cid:5)(cid:2) (cid:4) (cid:5)
Z −Z 1 N (j)−N
+U N t t dj +t.i.p.
n
Z N
0
wheret.i.p.standsfortermsindependentofpolicy.Equivalently,
(cid:4) (cid:5)
1−σ
U −U (cid:7)U C (1+z)(cid:11)y + (cid:11)y2
t c t t 2 t
(cid:1) (cid:3)
(cid:2) (cid:2)
1 1+ϕ 1
−U N (1+z) (cid:11)n(j)dj + (cid:11)n(j)2dj
n t t t
2
0 0

STICKYWAGESANDPRICES 189
where σ≡ − UccC and ϕ≡UnnN, and where use of the market clearing
condition(cid:11)c t = U (cid:11)y c t wasmade. Un (cid:13)
Define aggregate employment as N ≡ 1N (j)dj , or, in terms of log
t 0 t
deviationsfromsteadystateanduptoasecond-orderapproximation
(cid:2) (cid:2)
1 1 1 1
(cid:11)n + (cid:11)n2 (cid:7) (cid:11)n(j)dj + (cid:11)n(j)2dj
t 2 t t 2 t
0 0
Notealsothat
(cid:2) (cid:2)
1 1
(cid:11)n(j)2dj = ((cid:11)n(j)−(cid:11)n +(cid:11)n)2dj
t t t t
0 0
(cid:2) (cid:2)
1 1
=(cid:11)n2 t −2(cid:11)n t (cid:2) w w(cid:11) t (j)dj +(cid:2) w 2 w(cid:11) t (j)2dj
0 0
(cid:7)(cid:11)n2+(cid:2)2 var {w (j)}
t w j t
whereuseofthelabord (cid:13) emandequation(cid:11)n t (j)−(cid:11)n t =−(cid:2) w w(cid:11) t (j)hasbeen
madeandthefactthat 1w(cid:11) (j)dj = ((cid:2) w −1)var {w (i)}isofsecondorder,
0 t 2 i t
aresultanalogoustothatobtainedforprices.
Thus, period utility can be written up to a second order
approximationas
(cid:4) (cid:5)
1−σ
U −U (cid:7)U C (1+z)(cid:11)y + (cid:11)y2
t c t t 2 t
(cid:4) (cid:5)
1+ϕ (cid:2)2ϕ
−U N (1+z)(cid:11)n + (cid:11)n2+ w var {w (j)}
n t t 2 t 2 j t
Next,derivearelationshipbetweenaggregateemploymentandoutput
(cid:2) (cid:2)
1 1
N = N(i,j)djdi
t t
0 0
(cid:2) (cid:2)
1 1 N(i,j)
= N(i) t djdi
t
N(i)
0 0 t
(cid:2)
1
=(cid:12) w,t N t (i)di
0

190 CHAPTER6
(cid:4) (cid:5) (cid:2) (cid:4) (cid:5)
=(cid:12) w,t
Y
t
1− 1 α 1 Y
t
(i) 1− 1 α
di
A Y
t 0 t
(cid:4) (cid:5)
1
=(cid:12) (cid:12)
Y
t
1−α
w,t p,t
A
t
(cid:12) (cid:14) (cid:12) (cid:14)
(cid:13) −(cid:2) (cid:13) −(cid:2)p
where(cid:12) w,t ≡
0
1 W
W
t(
t
j) w dj and(cid:12) p,t ≡
0
1 P
P
t(
t
i) 1−α di.Thus,thefol-
lowing relation between (log) aggregate output and (log) aggregate
employmentholds
(1−α)(cid:11)n
t
=(cid:11)y
t
−a
t
+dw,t +d
p,t
(cid:13) (cid:8) (cid:9)
w × h lo er g e (cid:13) 1 (cid:8) d P w t( , i t ) ≡ (cid:9) − 1− ( (cid:2) 1 p αdi. − α)log 0 1 W W t( t j) −(cid:2) wdj and d p,t ≡(1 − α)
As sh
0
own
Pt
in appendix 4.1, d p,t (cid:7) 2 (cid:2) (cid:13) p var i {p t (i)}. Using an analogous
derivation,onecanshowdw,t (cid:7) (1−
2
α)(cid:2) w var
j
{w
t
(j)}.
Hence, deviations of period utility from steady state can be
rewrittenas
(cid:4) (cid:5)
1−σ
U −U (cid:7)U C (1+z)(cid:11)y + (cid:11)y2
t c t t 2 t
(cid:1)
U N (cid:2) ϒ
− n (1+z)(cid:11)y + p var {p(i)}+ var {w (j)}
(1−α) t t 2(cid:13) i t 2 j t
(cid:3)
(cid:2)
1+ϕ 1
+ ((cid:11)y −a )2 dj +t.i.p.
2(1−α) t t
0
whereϒ≡(cid:2) w(1−α)(1+(cid:2)
w
ϕ)andwheret.i.p.standsfortermsindepen-
dentofpolicy.
Let (cid:21) denote the size of the steady state distortion, implicitly defined
by−Un = MPN(1−(cid:21)).Usingthefactthat MPN=(1−α)(Y/N),
Uc
U −U 1−σ
t =(1+z)(cid:11)y + (cid:11)y2
U C t t 2 t
c (cid:4)
(cid:2) ϒ
−(1−(cid:21)) (1+z)(cid:11)y + p var {p(i)}+ var {w (j)}
t t 2(cid:13) i t 2 j t
(cid:5)
1+ϕ
+ ((cid:11)y −a )2 +t.i.p.
2(1−α) t t

STICKYWAGESANDPRICES 191
Under the “small distortion” assumption (so that the product of (cid:21)
with a second-order term is taken to be negligible) and ignoring t.i.p.
terms,
(cid:12)
U −U 1 (cid:2)
t dj =(cid:21)(cid:11)y − p var {p(i)}+ϒvar {w (j)}−(1−σ)(cid:11)y2
U C t 2 (cid:13) i t j t t
c
(cid:5)
1+ϕ
+ ((cid:11)y −a )2
1−α t t
(cid:12)
1 (cid:2)
=(cid:21)(cid:11)y − pvar {p(i)}+ϒ var {w (j)}
t 2 (cid:13) i t j t
(cid:4) (cid:5) (cid:4) (cid:5) (cid:5)
ϕ+α 1+ϕ
+ σ + (cid:11)y2−2 (cid:11)ya
1−α t 1−α t t
(cid:12)
1 (cid:2)
=(cid:21)(cid:11)y − pvar {p(i)}+ϒ var {w (j)}
t 2 (cid:13) i t j t
(cid:4) (cid:5) (cid:5)
ϕ+α
+ σ + ((cid:11)y2−2(cid:11)y(cid:11)ye)
1−α t t t
(cid:12)
1 (cid:2)
=(cid:21)(cid:11)y − p var {p(i)}+ϒ var {w (j)}
t 2 (cid:13) i t j t
(cid:4) (cid:5) (cid:5)
ϕ+α
+ σ + ((cid:11)y −(cid:11)ye)2
1−α t t
where (cid:11)ye≡ye − ye, and where the fact has been used that (cid:11)ye =
t t t
1+ϕ a .
σ(1−α)+ϕ+α t
Accordingly,asecond-orderapproximationtotheconsumer’swelfare
losses can be written as follows (expressed as a fraction of steady state
consumptionanduptoadditivetermsindependentofpolicy):
(cid:4) (cid:5)
(cid:6)∞ U −U
W=−E βt t
0
U C
t=0 c
(cid:30) (cid:4)
(cid:6)∞ 1 (cid:2)
=−E βt (cid:21)(cid:11)y − pvar {p(i)}+ϒ var {w (j)}
0 t 2 (cid:13) i t j t
t=0
(cid:4) (cid:5) (cid:5)(cid:31)
ϕ+α
+ σ + ((cid:11)y −(cid:11)ye)2
1−α t t

192 CHAPTER6
Using lemma 2 in appendix 4.1, rewrite the welfare
lossesas
(cid:30) (cid:4)
W=−E
(cid:6)∞
βt (cid:21)(cid:11)y −
1 (cid:2)
p (πp)2+
(cid:2) w(1−α)
(πw )2
0 t=0 t 2 λ p t λ w t
(cid:4) (cid:5) (cid:5)(cid:31)
ϕ+α
+ σ + ((cid:11)y −(cid:11)ye)2
1−α t t
Note that in the particular case of an efficient steady state (cid:21) = 0. In
addition,themodelsatisfies yn = ye forallt,thusimplying(cid:11)y −(cid:11)ye =(cid:23)y.
t t t t t
DefinitionofA∗,A∗ andB∗
0 1
 
−κ 1 0 0 0 0 0
p
 
 
  −κ w 0 1 0 0 0 0  
 
  0 −1 1 1 0 0 0  
 
 
A ∗ ≡ σ + ϕ+α 0 0 0 0 0 0 
0  1−α 
 
 (cid:2) 
 0 λ p 0 0 1 0 1 
 p 
 
 0 0 (cid:2) w(1−α) 0 0 1 −1 
 λ 
w
0 0 0 0 0 0 1
 
0 β 0 λ 0 0 0
p
 
 
 0 0 β −λ w 0 0 0 
 
 
 0 0 0 1 0 0 0 
 
 
A ∗ 1 ≡   0 0 0 0 −κ p −κ w 0   
 
 0 0 0 0 1 0 0 
 
 
 0 0 0 0 0 1 0 
 
0 0 0 0 −λ p λ w β
B ∗ 0 ≡[0,0,ψ wa ,0,0,0,0] (cid:8)

STICKYWAGESANDPRICES 193
REFERENCES
Barattieri, Alessandro, Susanto Basu, and Peter Gottschalk (2014): “Some
Evidence on the Importance of Sticky Wages,” American Economic Journal:
Macroeconomics6(1),70–101.
Bénassy, Jean-Pascal (1995): “Money and Wage Contracts in an Optimiz-
ing Model of the Business Cycle,” Journal of Monetary Economics 35(2),
303–316.
Blanchard, Olivier J., and Lawrence W. Summer (1986): “Hysteresis and the
EuropeanUnemploymentProblem,”inS.Fischer,ed.,NBERMacroeconomic
Annual1986,15–78.
Blasselle,Alexis,andAurélienPoissonier(2013):“TheFrontierofIndeterminacy
in a Neo-Keynesian Model with Staggered Prices and Wages,” unpublished
manuscript.
Christiano, Lawrence J., Martin Eichenbaum, and Charles L. Evans (2005):
“NominalRigiditiesandtheDynamicEffectsofaShocktoMonetaryPolicy,”
JournalofPoliticalEconomy113(1),1–45.
Cooley,ThomasF.,andJang-OkCho(1995):“TheBusinessCyclewithNominal
Contracts,”EconomicTheory6(1),12–33.
Erceg, Christopher J., Dale W. Henderson, and Andrew T. Levin (2000):
“OptimalMonetaryPolicywithStaggeredWageandPriceContracts,”Journal
ofMonetaryEconomics46(2),281–314.
Fischer,Stanley(1977):“Long-TermContracts,RationalExpectations,andthe
OptimalMoneySupply,”JournalofPoliticalEconomy85(1),191–206.
Flaschel,Peter,andReinerFranke(2008):“OnEquilibriumDeterminacyinNew
Keynesian Models with Staggered Wage and Price Setting,” B.E. Journal of
Macroeconomics8(1),1–10.
Giannoni,MarcP.,andMichaelWoodford(2003):“OptimalInflationTargeting
Rules,” in B. Bernanke, and M. Woodford, eds., The Inflation Targeting
Debate,93–162,ChicagoUniversityPress,Chicago.
Huang, Kevin X. D., and Zheng Liu (2002): “Staggered Price-setting, Stag-
gered Wage-Setting, and Business Cycle Persistence,” Journal of Monetary
Economics49(2),405–433.
Kim, Jinill (2000): “Constructing and Estimating a Realistic Optimizing Model
ofMonetaryPolicy,”JournalofMonetaryEconomics45(2),329–359.
Schmitt-Grohé, Stephanie, and Martin Uribe (2006): “Optimal Inflation Sta-
bilization in a Medium Scale Macroeconomic Model,” Duke University,
Durham,NC,unpublishedmanuscript.
Smets, Frank, and Rafael Wouters (2003): “An Estimated Dynamic Stochastic
General Equilibrium Model of the Euro Area,” Journal of the European
EconomicAssociation1(5),1123–1175.
Smets,Frank,andRafaelWouters(2007):“ShocksandFrictionsinUSBusiness
Cycles: A Bayesian DSGE Approach,” American Economic Review 97(3),
586–606.
Taylor,John(1980):“AggregateDynamicsandStaggeredContracts,”Journalof
PoliticalEconomy88(1),1–24.

194 CHAPTER6
Taylor,JohnB.(1999):“StaggeredPriceandWageSettinginMacroeconomics,”
inJ.B.Taylor,andM.Woodford,eds.,HandbookofMacroeconomics,1341–
1397,Elsevier,NewYork.
Woodford, Michael (2003): Interest and Prices: Foundations of a Theory of
MonetaryPolicy,PrincetonUniversityPress,Princeton,NJ.
EXERCISES
6.1. OptimalMonetaryPolicyinaStickyWageEconomy
Assumearepresentativefirmthatisperfectlycompetitiveandhas
accesstoatechnologydescribedby
y =a +n
t t t
where y, n, and a denote the logs of output, employment, and
t t t
productivity,respectively.Pricesareflexible.Assume
a t =ρa t−1 +ε t
The representative household’s optimal labor supply is
givenby
w − p =ϕn
t t t
where w and p denote the log of the wage and price levels,
t t
respectively.
a. Derive the equilibrium behavior of employment and output
undertheassumptionofflexiblewagesandprices.
b. Next, sticky wages are introduced. For each period, half the
workers set the (log) nominal wage, which remains constant
fortwoperiods,accordingto
1 ϕ
w t ∗ = 2 (p t +E t {p t+1 })+ 2 (n t +E t {n t+1 })
The average effective (log) wage paid by the firm in period
t isthus
1
w = (w∗+w∗ )
t 2 t t−1

STICKYWAGESANDPRICES 195
Showthatinflationevolvesaccordingto
π t = E t {π t+1 }+ϕn t +u t
where n t ≡n t−1 + E t−1 {n t }+n t + E t {n t+1 } and u t ≡ −4a t −
(p t −E t−1 {p t }).
c. SupposethataggregatedemandisgivenbybytheISequation
1
y t =− σ (i t −E t {π t+1 }−ρ)+E t {y t+1 }
and assume that the optimal policy requires that the flexible
wageallocationbereplicated.Describetheequilibriumbehav-
ioroftheinterestrate,wageinflation,andpriceinflationunder
theoptimalpolicy.
6.2. OptimalMonetaryPolicywithWagesSetinAdvance
Therepresentative firmisperfectlycompetitiveandhas access to
atechnologydescribedby
y =a +n
t t t
where y, n, and a denote the logs of output, employment, and
productivity,respectively.Pricesareflexible.Assume
a t =ρ a a t−1 +ε t a
Theoptimallaborsupplysatisfies
w − p =ϕn
t t t
where w and p denote the log of the (nominal) wage and price
levels,respectively.
AggregatedemandisgivenbythedynamicISequation
1
y t =− σ (i t −E t {π t+1 }−ρ)+E t {y t+1 }
wherei t denotesthenominalinterestrateandπ t ≡p t −p t−1 isthe
inflationrate.
a. Derive the equilibrium behavior of employment, output, and
the real interest rate under the assumption of flexible wages

196 CHAPTER6
and prices. Can one determine the corresponding equilibrium
valuesforthenominalrateandinflation?Explain.
b. Next, wage stickiness is introduced by assuming that nominal
wages are set in advance (i.e., at the end of the previous
period),accordingtotherule
w t = E t−1 {p t }+ϕE t−1 {n t }
c. Characterizetheequilibriumbehaviorofoutput,employment,
inflation, and the real wage under the assumption that the
centralbankfollowsthesimplerule
i t =ρ+φ π π t
d. Characterize the optimal policy and its associated equilibrium
in the presence of sticky wages, and suggest an interest rate
rule that would implement it. (Note: Assume efficiency of the
equilibriumallocationintheabsenceofstickywages.)
6.3. LaborMarketInstitutionsasaSourceofLong-RunMoneyNon-
neutrality
AsshowninBlanchardandSummers(1986),aperfectlycompet-
itiverepresentativefirmmaximizesprofitseachperiod
PY −WN
t t t t
subjecttoatechnologyY = N1−α.Assumethatthedesiredlabor
t t
supply is inelastic and equal to one. Equilibrium in the goods
marketisgivenby
M
Y = t
t
P
t
with the nominal money supply following an AR(1) process (in
logs)
m t =ρ m m t−1 +ε t
Derive the equilibrium process for (the log) of output y,
t
employment n, prices p, and real wages w − p under each of
t t t t
thealternativeassumptionsonthewagesettingprocess:
a. Nominalwagesarefullyflexibleanddeterminedcompetitively.
b. Nominal wages are set in advance, so that the labor market
clearsinexpectation(i.e., E t−1 {n t }=0).

STICKYWAGESANDPRICES 197
c. Nominal wages are set in advance by a union, so that in
expectation only currently employed workers are employed
(i.e., E t−1 {n t }=n t−1 ).
d. Discusstheempiricalrelevanceofthethreeprecedingscenarios
in light of their implied properties (comovements, persistence)
forrealwages,employment,andoutput.
6.4. MonetaryPolicyandRealWageRigidities
Ass ume that the representative household’s utility is given by
E ∞ βtU(C,N) with U(C,N) = C − 1N2, where C
0 t=0 t t t t t 2 t t
denotes consumption and N denotes hours worked. Let firms’
t
technologybegivenbytheproductionfunctionY = AN,where
t t t
Y denotes output and A is an exogenous technology parameter.
t t
Alloutputisconsumed.
FirmssetpricesinastaggeredfashionàlaCalvo,whichresults
intheinflationdynamicsequation
π
t
=βE
t
{π
t+1
}−λµ(cid:11)
t
where µ(cid:11) ≡µ − µ represents the deviation of average price
t t
markupfromitsconstantdesiredlevel.
a. Deriveanexpressionforthe(log)oftheefficientlevelofoutput
(which is denoted by ye) as a function of (log) productivity a
t t
(i.e.,thelevelofoutputthatabenevolentsocialplannerwould
choose,givenpreferencesandconstraints).
b. Assume that the (log) nominal wage w is set each period
t
according to the schedule w =p + 1 n, where δ>0 (the
t t 1+δ t
same assumption is maintained for parts (c), (d), and (e)
below). Compare the behavior of the equilibrium real wage
underthatschedulewiththeonethatwouldbeobservedunder
competitive labor markets. In what sense can the condition
δ >0beinterpretedasa“realrigidity”?
c. Derivetheimplied(log)naturallevelofoutput(denotedby yn)
t
definedastheequilibriumlevelofoutputunderflexibleprices
(whenallfirmskeepaconstant(log)markupµ).
d. Derive an expression for the markup gap µ(cid:11) as a function of
t
theoutputgap(cid:23)y ≡y −yn.
t t t
e. Derive the inflation equation in terms of the welfare-relevant
output gap y − ye. Show how the presence of real wage
t t
rigidities (δ>0) generates a tradeoff between stabilization of
inflation and stabilization of the welfare-relevant employment
gap.

198 CHAPTER6
f. Suppose that the monetary authority has a loss function
givenby
(cid:6)∞ (cid:8) (cid:9)
E βt α (y −y ∗ )2+π2
0 y t t t
t=0
Solvefortheequilibriumprocessforinflationandoutputunder
the optimal monetary policy under discretion (time-consistent
solution),undertheassumptionofani.i.d.technologyprocess
a . Explain the difference with the case of perfect competition
t
in the labor market. (Note: For simplicity, assume that the
frictionless markup µ is infinitesimally small when answering
thisquestion.)