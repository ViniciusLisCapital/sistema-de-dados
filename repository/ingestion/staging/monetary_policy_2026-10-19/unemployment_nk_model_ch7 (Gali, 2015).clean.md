Chapter 7
UNEMPLOYMENT IN THE NEW KEYNESIAN MODEL
The New Keynesian model with staggered price and wage setting
developedinchapter6remainsaframeworkofreferencefortheanalysis
offluctuationsandstabilizationpolicies1.Manycentralbanksandpolicy
institutionshaveadoptedmedium-scaleversionsofthatmodelaspartof
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
if,throughthelensoftheNewKeynesianmodel,unemploymentandthe
frictionsunderlyingitwerenotessentialforunderstandingfluctuationsin
nominalandrealvariables,norakeyingredientinthedesignofmonetary
policy.
Overthepastfewyearsagrowingnumberofresearchershavesought
to rectify that anomaly by developing frameworks that combine the
nominalrigiditiesandconsequentmonetarynon-neutralitiesoftheNew
Keynesian model with labor market imperfections that give rise to
unemployment. Those frictions are generally introduced by embedding
alabor market withsearch and matching, inthetradition of Mortensen
and Pissarides (1994), into some version of the New Keynesian model.
1 The present chapter draws heavily from my Zeuthen lectures, published in Galí
(2011b).
2 See, e.g., Smets and Wouters (2003, 2007) and Christiano, Eichenbaum, and Evans
of those models developed at policy institutions, see Christoffel, Coenen, and Warne
others.

200 CHAPTER7
The resulting framework has been used in both positive and normative
applications,withandwithouttheassumptionofwagerigidities.3
In the present chapter a different approach is adopted to introduc-
ing unemployment in the New Keynesian framework. The proposed
approach, based on Galí (2011a, 2011b), involves a reinterpretation of
the labor market in the standard New Keynesian model with staggered
wage setting, as developed in chapter 6, rather than a modification
or an extension of that model. The resulting framework preserves the
convenience of the representative household paradigm, and allows one
to determine the equilibrium levels of employment, the labor force,
and, hence, the unemployment rate (as well as other macro variables of
interest)conditionalonthemonetarypolicyruleinplace.Unemployment
inthemodelresultsfromthepresenceofmarketpowerinlabormarkets,
reflected in a positive average wage markup, that is, a positive gap
between the prevailing wage and the disutility of work (expressed in
terms of consumption) for the marginal worker employed. On the
other hand, fluctuations in the unemployment rate are associated with
variations in that average wage markup due to the presence of nominal
wagerigidities.
One important advantage of the proposed approach lies in its com-
patibility with a variety of assumptions regarding aspects of the model
unrelated to unemployment, including the specific form of price and
wagerigidities,thespecificationofthehouseholdutility,andthepossible
presenceoftime-varyingdesiredmarkups.Needlesstosay,theproposed
frameworkalsohaslimitationsofitsown.Inparticular,itabstractsfrom
potential sources of unemployment other than noncompetitive wages,
including those associated with the costly reallocation of labor across
firms or sectors (in terms of time and other resources) which may give
rise to frictional unemployment. It is important to stress, however, that
the findings of much of the recent literature on labor market frictions
suggestthatthelatterarenotenoughinordertogenerateunemployment
fluctuationsofsizeandpersistencesimilartothoseobservedinthedata,
pointingtotheneedforsomekindofwagerigidity.4
The chapter is organized as follows. First, the basic model of unem-
ployment is introduced and embedded in the standard New Keynesian
framework of chapter 6. Using a calibrated version of the model, its
predictions regarding the properties of unemployment in response to
technology, demand, and monetary policy shocks are derived, under
the assumption that the central bank follows a conventional Taylor
rule. The analysis puts special emphasis on the role played by nominal
3Seesection7.4forsomeofthekeycontributionstothatliterature.
4See,e.g.,Hall(2005),GertlerandTrigari(2009),Galí(2011a),andShimer(2005).

wage rigidities in accounting for the volatility and persistence of un-
employment. The chapter then turns its focus to the relation between
unemployment and the design of monetary policy, by analyzing the
behavior of unemployment and several other macro variables under
the optimal monetary policy, and comparing it to that prevailing
under a standard Taylor rule. That analysis suggests the presence of
likely welfare gains from stabilizing the unemployment rate beyond
what is implied by the Taylor rule. This is confirmed by the study
of the properties of a generalized Taylor rule, one that allows for a
systematic response to the unemployment rate, in addition to output
and price inflation. The chapter concludes with a note on the related
literature,withreferencestoalternativeapproachestotheonepresented
here.
7.1 INTRODUCINGUNEMPLOYMENT IN THE
NEW KEYNESIANMODEL
A reformulation of the standard New Keynesian model with staggered
wage and price setting developed in chapter 6 is described next. The
variantpresentedhere,basedonGalí(2011a,2011b),assumesthatlabor
is indivisible, that is, in each period any given individual either works a
fixednumberofhoursordoesnotworkatall.Asaresult,allvariations
in labor input take place at the extensive margin (i.e., in the form of
variations in employment). Since that margin is the one that dominates
observedvariationsintotalhoursofwork,theassumptionofindivisible
labor remains a good first approximation. Most importantly, however,
that assumption leads to a definition of unemployment consistent with
itsempiricalcounterpart.
As discussed below, the model’s equilibrium includes the same set of
equations as the model in chapter 6, to which an additional equation
describing the evolution of unemployment is added. Thus, the reader is
referredtochapter6forthedetailsofmanyofthederivations.
7.1.1 Households,WageSetting,andUnemployment
Theeconomyisassumedtohavealargenumberofidenticalhouseholds.
Each household has a continuum of members represented by the unit
square and indexed by a pair (j,s) ∈ [0,1] × [0,1]. The first index,
j ∈ [0,1], represents the type of labor service that a given household
member is specialized in. The second index, s ∈ [0,1], determines
the disutility from work. The latter is given by χsϕ if he is employed
and zero otherwise, where χ>0 and ϕ>0 are exogenous parameters.

202 CHAPTER7
AsinMerz(1995)andmuchofthesubsequentliterature,fullrisksharing
within the household is assumed. Given the separability of preferences,
this implies the same level of consumption for all household members,
independentlyoftheirworkstatus.Thisisnotaninnocuousassumption,
especially from a welfare viewpoint, but one that I stick to in order to
preservethemodel’stractability.5
The household’s period utility is given by the integral of its members’
utilitiesandcanthusbewrittenasfollows
U(C,{N(j)};Z)≡
C
t
1−σ −1
−χ
1 N t(j)
s ϕ dsdj Z
0 0
(cid:2)
C1−σ −1 1 N (j)1+ϕ
1−σ 1+ϕ t
(cid:5) (cid:4)p
where C
t
≡
1 C
t
(i) 1− (cid:4) 1 pdi (cid:4)p−1 is a consumption index, C
t
(i) is the
quantity consumed of good i, for i ∈ [0,1], and N (j) ∈ [0,1] is the
t
fraction of members specialized in type j labor who are employed in
periodt.Asinpreviouschaptersbelowthepreferenceshifter z ≡logZ
t t
isassumedtofollowtheAR(1)process:
where ρ ∈ [0,1] and εz is a white noise process with zero mean and
z t
varianceσ2.
z
Eachhouseholdseekstomaximize
(cid:7)∞
E βtU(C,{N (j)};Z)
0 t t t
t=0
subjecttoasequenceofflowbudgetconstraintsgivenby
1 1
0 0
where P(i) is the price of good i, W(j) is the nominal wage for type j
t t
labor,B representspurchasesofanominallyrisklessone-perioddiscount
t
5 See Christiano, Trabandt, and Walentin (2010) for an unemployment model with
separablepreferencesbutdifferentlevelsofconsumptionforemployedandun-employed
householdmembers.

bond paying one monetary unit, Q is the price of that bond, and D
t t
is a lump-sum component of income (which may include, among other
items, dividends from the ownership of firms). As in previous chapters,
the above sequence of period budget constraints is supplemented with a
solvency condition that prevents the household from engaging in Ponzi
schemes.
Optimal demand for each good resulting from utility maximization
takesthefamiliarform:
−(cid:4)
P(i) p
C(i)= t C (2)
t t
P
t
(cid:5) 1
where P
t
≡
1 P
t
(i)1−(cid:4) pdi 1−(cid:4)p denotes the price index for final goods.
Note also that (2) implies that total consumption expenditures can be
(cid:5)
writtenas 1 P(i)C(i)di = PC.
Thehousehold’sintertemporaloptimalityconditionisgivenby
(cid:10)(cid:8) (cid:9) (cid:8) (cid:9)(cid:8) (cid:9)(cid:11)
−σ
Q =βE C t+1 Z t+1 P t (3)
t t
As in the model of chapter 6, the wage for each type of la-
bor is set by a union representing all the workers specialized in it,
whereas thecorresponding employment levelN (j)isdetermined bythe
t
aggregation of firms’ labor demand, assumed to be allocated uniformly
across households. Thus, both W(j) and N (j) are taken as given
t t
by each household, for all j ∈ [0,1]. More specifically, and fol-
lowing Calvo’s formalism (Calvo (1983)), it is assumed that work-
ers specialized in a given type of labor (or the union representing
them) reset their nominal wage with probability 1 − θ w each period.
That probability is independent of the time elapsed since they last
reset their wage, in addition to being independent across labor types.
Thus, a fraction of workers θ w keep their wage unchanged in any
given period, making that parameter a natural index of nominal wage
rigidities.
Optimal wage setting proceeds as in chapter 6, to which the reader
is referred. As in that chapter, the optimal wage setting decision can be
combinedwiththelawofmotionfortheaveragenominalwagetoderive
thefollowingequationdescribingwageinflationdynamics:

204 CHAPTER7
the (log) average wage markup, where mrs ≡σc + ϕn + ξ defines
t t t
the economy’s average marginal rate of substitution (with ξ ≡logχ),
wage inflation depends positively on expected one-period-ahead wage
inflation and negatively on the deviation of the average wage markup
fromitsdesiredvalue.
Next,andfollowingGalí(2011a,2011b),unemploymentisintroduced
in the framework above, allowing the wage inflation equation (4) to be
reformulatedintermsoftheunemploymentrate.
7.1.2 IntroducingUnemployment
Considerindividual(j,s)specializedintype j laborandwithdisutilityof
work χsϕ. Using the welfare of its household as a criterion, and taking
as given current labor market conditions (as summarized by the wage
prevailing in his trade) that individual will be willing to work (and thus
bepartofthelaborforce)inperiodt ifandonlyif
W(j)
P t
t
that is, if and only if the relevant real wage exceeds the disutility
from work, where the latter is expressed in terms of consumption by
dividing the disutility term χsϕ by the household’s marginal utility of
consumptionC−σ.
t
Thus, the marginal supplier of type j labor, denoted by L(j),
t
isgivenby
W(j)
t =χC σ L(j) ϕ (5)
P t t
t
Define the aggregate labor force (or participation rate) as
(cid:5)
L ≡ 1 L(j)dj. Taking logs and integrating over j one can derive the
t 0 t
followingapproximaterelation:
w − p =σc +ϕl +ξ (6)
t t t t
where use is made of the first order approximations around the
symmetricsteadystatew (cid:6) 1w (j)dj andl (cid:6) 1 l (j)dj .Equation(6)
canbethoughtofasanaggregatelaborsupplyorparticipationequation.

Figure7.1. TheWageMarkupandtheUnemploymentRate.
Following Galí (2011a, 2011b), the unemployment rate u is defined
t
asthelogdifferencebetweenthelaborforceandemployment:
u ≡l −n (7)
t t t
This definition of the unemployment rate is, for low values of that
variable,veryclosetotheconventionalone,thatis,1− Nt.6 Combining
thedefinitionoftheaveragewagemarkupµw ≡(w −p)−
Lt
(σc +ϕn +ξ)
with (6) and (7), one can obtain the following simple linear relation
betweenthewagemarkupandtheunemploymentrate
µw =ϕu (8)
t t
Figure 7.1 represents graphically the above relationship between the
averagewagemarkupandtheunemploymentrate,usingaconventional
labormarketdiagram.Thefigureemphasizestheideathatemploymentis
6Notethat1− N
Lt
t =1−exp{−ut }(cid:6)utforunemploymentratesnearzero.

206 CHAPTER7
demanddetermined,withlabordemandgivenbytheinverseproduction
function(inlogs)
t 1−α t t
and,hence,isnotdirectlyinfluencedbythewage.
The labor force, on the other hand, is determined by the labor supply
equation (6).Theunemployment ratecorresponds tothehorizontal gap
between the labor supply and labor demand schedules, at the level of
the prevailing average real wage. The wage markup µw, on the other
t
hand, is represented in the figure by the vertical gap between the wage
and the labor supply, at the level of current employment n. Given
t
the assumed linearity, the ratio between “the two gaps” is constant
and given by ϕ, the slope of the labor supply schedule, as implied
by(8).
I define the natural rate of unemployment, un, as the unemployment
t
rate that would prevail in the absence of nominal wage rigidities. It
follows from the assumption of a constant desired wage markup that
suchanaturalrateisconstantandgivenby
µw
un = (10)
ϕ
Equations (8) and (10) reveal the nature of unemployment in the
present model. In particular, (10) shows that the presence of market
power in the labor market, reflected in the wage markup µw>0,
accountsfortheexistenceofpositiveunemployment,evenintheabsence
of wage rigidities. On the other hand, (8) implies that fluctuations
in unemployment are associated with variations in the wage markup.
In the New Keynesian model of chapter 6, wage markup variations
are the result of nominal wage rigidities. Such rigidities are, accord-
ingly, a necessary ingredient for the model to display unemployment
fluctuations.
Note, however, that the above conclusion hinges critically on the
assumption of a constant desired wage markup µw, an assumption
maintained below. But it should be clear that the analysis above can be
easily generalized to an environment in which the desired wage markup
itself varies over time. In that case the natural rate of unemployment
will fluctuate in response to variations in the desired markup, whereas
fluctuations in actual unemployment will have two components: a first
one associated with changes in the natural rate (driven by changes in
the desired wage markup), and a second one linked to deviations of

wage markups from their desired levels resulting from nominal wage
rigidities.7
Finally, note that by combining (4), (8), and (10) one can derive
a simple relation between wage inflation and the unemployment gap,
u −un:
t
π t w =βE t {π t w +1 }−λ w ϕ(u t −un) (11)
Galí (2011a) refers to the previous equation as the New Keynesian
Wage Phillips Curve, and provides some evidence in its support using
postwar U.S. data. Note that in contrast with Phillips’s original curve
(Phillips (1958)), which involved a simple static relation between wage
inflation and unemployment, (11) is a forward-looking relation, which
can be rewritten to express wage inflation as a function of current and
expected future unemployment gaps. Furthermore, while the original
Phillips curve was a purely empirical relation, without any theoretical
justification, (11) is derived from first principles, with its coefficients
beingafunctionofstructuralparameters.
7.2 EQUILIBRIUM
The remaining equilibrium conditions correspond to those of the New
Keynesian framework developed in chapter 6. Since they were derived
and analyzed in detail therein, they are only listed below, together with
(11),forconvenience:
πp =βE{πp }+κ (cid:13)y +λ ω(cid:13) (13)
ω(cid:13) t ≡ω(cid:13) t−1 +π t w−π t p−(cid:14)ω t n (15)
7 The interested reader can find an analysis of a medium-scale version of the present
modelallowingforvariationsinthedesiredwagemarkupinGalí,Smets,andWouters

208 CHAPTER7
to which one must add an equation relating the unemployment gap
(cid:12)u ≡u −un totheoutputandrealwagegaps,namely:8
t t
ϕ(cid:12)u =µ(cid:12)w
t t
=ω(cid:13) −(σ(cid:13)c +ϕ(cid:13)n)
t (cid:8) t t (cid:9)
ϕ
=ω(cid:13) − σ + (cid:13)y (16)
t 1−α t
The natural values of the real interest rate and the real wage are now
givenby(ignoringconstantterms):
rn =ρ−σ(1−ρ )ψ a +(1−ρ )z
Inaddition,equations(7)and(9),togetherwiththefactthat yn = y+
t
ψ a canbeusedtodeterminetheequilibriumbehaviorofemployment,
ya t
n,andparticipation,l .
t t
Finally, and in order to close the model, one or more equations
describing monetary policy must be added. Below, the optimal policy
undercommitmentaswellassomesimpleinterestraterulesareanalyzed.
7.3 MONETARYPOLICY DESIGN AND
UNEMPLOYMENTFLUCTUATIONS
In this section the properties of the unemployment rate in the face of
different shocks are determined for a calibrated version of the model
developed above. One goal of the exercise is to assess the ability of
the New Keynesian model to account for the empirical properties of
unemployment fluctuations.Indoingso,itisimportanttorecognizethe
model’s inherent limitations to provide a full account of the observed
behavior of macro variables, since it lacks many of the bells and
whistles found in medium-scale DSGE models (habit formation, capital
8Notethat(14)and(16)canbecombinedtoyieldthewageinflationequationusedin
chapter6,namely:
π
t
w=βEt {π
t
w
+1
}+κ
w
(cid:1)yt −λ
w
ω(cid:1)
t
((cid:4)ut)andanextraequation(16).

0.6 0.1
0.5 0
0.4 –0.1
0.3 –0.2
0.2 –0.3
0.1 –0.4
0 –0.5
–0.1 –0.6
Unemployment rate Employment
0.4 0
0.2 –0.005
0 –0.01
–0.2 –0.015
–0.4 –0.02
Labor force Real wage
Figure7.2. ResponseofLaborMarketVariablestoaMonetaryPolicyShock.
accumulation,indexation,etc.).9 Itsadvantage,ontheotherhand,liesin
itssimplicityandtransparency.
The baseline calibration underlying the quantitative results reported
below is identical to that used in chapter 6, so the reader is referred to
the description therein. An advantage of the framework above lies in
the discipline it provides in the choice of a setting for (cid:4) w, the elasticity
of substitution among labor types in production. Thus, note that the
average wage markup is tied to the natural rate of unemployment
throughtherelationMw ≡ (cid:4) w =exp{ϕun}.Theassumptionsofϕ =5
(cid:4)
w
−1
used earlier and un = 0.05 (consistent with an average unemployment
rateof5percent),implies(cid:4)
w
=4.5,whichisinturnisassociatedwithan
averagewagemarkupof28percent.
7.3.1 TheEffectsofaMonetaryPolicyShockontheLaborMarket
Figure 7.2 plots the dynamic response of employment, n, the unem-
t
ployment rate, u , the labor force, l , and the real wage w − p to an
t t t t
9 SeeGalí,Smets,andWouters(2012)forananalysisofthesourcesofunemployment
fluctuationsinanestimatedmedium-scaleversionofthepresentmodel.

210 CHAPTER7
exogenousmonetarypolicyshock,undertheassumptionthatthecentral
bankfollowsaconventionalTaylorruleoftheform
i =0.01+1.5πp+0.125(cid:12)y +v (17)
t t t t
As in earlier chapters, it is assumed an autoregressive coefficient ρ v =
0.5intheAR(1)processfollowedbythemonetarypolicyshifterv ,with
t
thesizeoftheinitialexogenousimpulsebeing0.25(i.e.,correspondingto
anincreaseinthenominalinterestrateof100basispoints,inannualized
terms). The responses are expressed in percentage deviations from the
initialsteadystate.
As the figure makes clear, the unemployment rate rises substantially,
and persistently, in response to the tightening of monetary policy. The
increase in the unemployment rate is largely due to the decline in
employment and only marginally to an increase in the labor force.
The latter is, in turn, a consequence of the negative wealth effect, as
reflectedintheconsumptiondecline(notshown),combinedwithanearly
unchangedrealwage.10 Finally,therealwageisshowntodecline,albeit
by a small amount, due the downward pressure of unemployment on
nominal wages, which appears to dominate the effect of the decline in
priceinflation.
The connection between wage rigidities and the properties of unem-
ploymentfluctuationsisfurtherexplorednext.Forthesakeofconcrete-
ness, focus is restricted to fluctuations driven by monetary shocks. One
maywanttoviewthoseshocksasastand-inforotheraggregatedemand
shocks.11
Table7.1reportsmeasuresofvolatility,persistence,andcyclicalityof
unemployment, conditioned on monetary policy shocks, for alternative
configurations of θ w, the degree of wage stickiness, and ρ v, the autore-
gressive coefficient of the shock process. The standard deviation of the
shock σ v is set to 0.25 percent (i.e., 1 percent in annualized terms). The
question posed here can be stated as follows: How does the degree of
nominal rigidities, indexed by θ w , influence the volatility, persistence
andcyclicalityoftheunemploymentrate?
10 Though small, the countercyclical response of the labor force to a monetary shock
appearstobeatoddswiththeempiricalevidencereportedinChristiano,Trabandt,and
Walentin(2010).Galí,Smets,andWouters(2012)modifythehousehold’sutilityfunction
alongthelinesofJaimovichandRebelo(2009),andshowthataspecificationofthelatter
consistentwithsmallwealtheffectsimpliesaprocyclical(andsmall)responseofthelabor
forcetoamonetaryshock,inawayconsistentwiththeevidence.
11Inparticular,shockstothediscountratewouldhaveanidenticaleffectonlabormarket
variables.

TABLE7.1
WageRigiditiesandUnemploymentFluctuations
Volatility Persistence Cyclicality
θ w : 0.1 0.5 0.75 0.1 0.5 0.75 0.1 0.5 0.75
ρ
v
=0.0 0.25 0.32 0.33 −0.14 −0.02 −0.01 −0.99 −0.99 −0.99
ρ
v
=0.5 0.36 0.60 0.67 0.24 0.44 0.48 −0.96 −0.99 −0.99
ρ
v
=0.9 0.31 1.24 2.47 0.51 0.80 0.87 −0.77 −0.98 −0.99
Thestatisticsreportedintable7.1seektoanswerthatquestion.First,
note that unemployment volatility, measured by the standard deviation
of the unemployment rate, increases with the degree of nominal wage
rigiditiesθ w,foranygivendegreeofpersistenceoftheshock.Thus,other
thingsequal,morerigidwagesimplymorevolatileunemployment.That
effectisparticularlystrongwhentheshockismorepersistent.12
The second panel of table 7.1 displays the first-order autocorrelation
oftheunemploymentrate,asameasureofpersistence.Persistenceisalso
increasinginthedegreeofnominalwagerigidities(and,lesssurprisingly,
in the persistence of the shock). Note also that the autocorrelation
of unemployment always remains below the autocorrelation of the
shock process itself. Under the baseline calibration the persistence of
the unemployment rate is substantial (0.48), though still below the
persistenceobservedinthedata.13 Thelatterisapproximated,however,
whenassumingρ
v
=0.9.Itisalsointerestingtonotethatforsufficiently
low values of ρ v, the unemployment rate becomes negatively serially
correlated,apropertyinheritedfromemployment.
Finally, the third panel of table 7.1 shows the correlation between
the unemployment rate and output, a measure of cyclicality. Like in
the data, that correlation is strongly negative for all calibrations. Thus,
the strong countercyclicality of unemployment in response of monetary
shocks seems to be a robust feature of the model, independently of the
degreeofwagestickinessandthepersistenceofthoseshocks.
The simplicity of the underlying model notwithstanding, the above
findings suggest that a New Keynesian model with realistic levels of
nominal wage rigidities and persistence of monetary (or other demand
12Asdiscussedabove,asθ
w
→0thevolatilityofunemploymentconvergestozero.
13 Theautocorrelationofthe(HP-detrended)unemploymentrateisashigh0.90inthe
UnitedStatesand0.92intheeuroarea.SeeGalí(2011b)fortheseandotherlabormarket
statistics.

212 CHAPTER7
shocks) can potentially generate unemployment fluctuations with prop-
ertiescomparabletothoseobservedinactualeconomies.
7.3.2 OptimalMonetaryPolicy
The economy’s behavior under the optimal policy can be represented
by equations (13), (14), (15), and (16) above, combined with the three
optimalityconditionsderivedinchapter6andwhicharereproducedhere
forconvenience:
ϕ+α
σ + 1−α (cid:13)y t +κ p ζ 1,t +κ w ζ 2,t =0 (18)
(cid:4)
λ p π t p−(cid:14)ζ 1,t +ζ 3,t =0 (19)
p
(cid:4) w(1
λ
−α)
π t w−(cid:14)ζ 2,t −ζ 3,t =0 (20)
w
λ p ζ 1,t −λ w ζ 2,t +ζ 3,t −βE t {ζ 3,t+1 }=0 (21)
for t = 0,1,2,... where {ζ 1,t }, {ζ 2,t }, and {ζ 3,t } denote the Lagrange
multipliersassociatedwiththeconstraintsoftheoptimalpolicyproblem
(givenby(13),(14),and(15)and(16)combined,respectively).Notethat
theoptimalityconditionsareidenticaltothosederivedinchapter3since
the slight reformulation of the households’ problem does not affect the
second order approximation to the welfare losses or the constraints of
theoptimalpolicyproblem.14
Figure 7.3 plots the responses of six macro variables (including the
unemploymentrate)toaonepercentpositivetechnologyshockunderthe
optimal policy (shown as a line with diamonds). The figure also shows
the corresponding responses under Taylor rule (17) (line with circles).
Both sets of responses assume that nonpolicy parameters are at their
baselinevalues.
Note that the optimal policy is more accommodative of the produc-
tivity improvement than the Taylor rule, with output increasing more,
and employment remaining largely unchanged (as opposed to declining,
14SeeGalí(2011b)fordetails.

1 1
Taylor rule
optimal 0.5
0.5
0 –0.5
0.5 0.2
0.1
–0.5
–0.1
–1 –0.2
0.4 0.5
0.3
0.2
–0.5
0.1
0 –1
Figure7.3. OptimalPolicyvs.TaylorRule:TechnologyShocks.
as implied by the Taylor rule) under the optimal policy. Note also that
the response of those variables is very close to the efficient one, which
involves a zero response of employment and participation and a one-
for-one adjustment of output to the change in technology under the
assumptionmadeherethatσ =1.
Theresponseoftheunemploymentrateissubstantiallydifferentacross
the two policies: it declines somewhat under the optimal policy, which
contrasts with the strong rise observed under the Taylor rule. Due to
the presence of rigidities in both prices and wages, the adjustment of
the real wage under the optimal policy is considerably muted relative to
its natural counterpart (which moves one-for-one with technology), but
is stronger than under the Taylor rule. This is due to a larger upward
adjustmentofthenominalwage(facilitatedbythelowerunemployment
rate),despiteamoremuteddeflation(associatedwithhigheractivityand,
hence,highermarginalcosts,relativetotheTaylorrulecase).
Figure 7.4 displays the corresponding responses to a one percent
increase in the exogenous demand shifter, z, under the optimal policy
t
and the Taylor rule. As discussed above, output, inflation, and all

214 CHAPTER7
1 0.5
Taylor rule
0.5 optimal
–0.5
–1
–0.5 –1.5
1.5 0.05
1 0
0.5 –0.05
0 –0.1
–0.5 –0.15
0.03
0.06
0.02
0.04
0.01
0.02
–0.01
Figure7.4. OptimalPolicyvs.TaylorRule:DemandShocks.
labor market variables are fully insulated from the shock under the
optimal policy. Only the nominal and real interest rates (not shown)
vary, responding one-for-one to the change in the natural rate. On the
otherhand,underaTaylorrulethedemandshockgeneratesapersistent
increase in output and employment, a reduction in unemployment, and
positive inflation. In other words, the Taylor rule is not sufficiently
stabilizinginthefaceofdemandshocks.
7.3.3 ASimpleInterestRateRulewithUnemployment
The explicit introduction of unemployment in the model makes it
possible to study the properties of simple interest rate rules that have
that variable as an argument. To illustrate that point, the equilibrium
of the New Keynesian economy developed above is analyzed under the
assumptionthatmonetarypolicyisdescribedbythesimplerule:
i =0.01+1.5πp−0.5(cid:12)u (22)
t t t

1 1
simple
Taylor
0.5
optimal
0.5
0 –0.5
0.5 0.2
0.1
–0.5
–0.1
–1 –0.2
0.4 0.5
0.3
0.2
–0.5
0.1
0 –1
Figure7.5. OptimalPolicyvs.SimpleRule:TechnologyShocks.
Galí (2011b) argues that such a rule provides a good account of the
Fed’s interest rate decisions during the 1987 to 2008 period, before
the federal funds rate hit the zero lower bound. In particular, the
empirical fit of such a rule seems to improve on the standard Taylor
rule.
Figure7.5displaystheresponsesofdifferentmacrovariablestoaone
percent positive innovation in technology under the above simple rule
(line with circles). The figure also show, for the sake of comparison, the
responses under both the optimal policy (line with diamonds) and the
Taylor rule (line with squares). Note that the responses to a technology
shockundersimplerule(22)approximateprettywelltheresponsesunder
the optimal policy. For all variables considered the simple rule tracks
the optimal policy much better than the Taylor rule. A similar result
holdswhendemandshocksarethesourceoffluctuations,asillustratedin
figure7.6,whichdisplaystheresponsestoapositivedemandshockunder
thethreerules.

216 CHAPTER7
1 0.5
simple
Taylor 0
0.5
optimal
–0.5
–1
–0.5 –1.5
1.5 0.05
1 0
0.5 –0.05
0 –0.1
–0.5 –0.15
0.03
0.06
0.02
0.04
0.01
0.02
–0.01
Figure7.6. OptimalPolicyvs.SimpleRule:DemandShocks.
7.4 NOTES ON THELITERATURE
The general approach to introducing unemployment in a macro model
underlying this chapter can be found in Galí (1996). The specific
application to the New Keynesian model was developed in Galí (2011a,
2011b)and,independently,inCasares(2010).Galí,Smets,andWouters
in a version of Smets and Wouters’ (2003, 2007) medium-scale New
Keynesian model. Among other results, they show how the use of
unemployment data allows the separate identification of wage markup
shocks and labor supply shocks, thus overcoming an earlier critique of
suchmodels(Chari,Kehoe,andMcGrattan(2009)).
MuchoftheliteratureonunemploymentintheNewKeynesianmodel
has followed an alternative approach, one that combines the nominal
rigidities that are the hallmark of the New Keynesian framework with
the labor market frictions of search and matching models (and which
are usually studied in the context of real models; see, e.g., Pissarides
the earliest contributions to that literature, analyzed the impact of

embedding labor market frictions into the basic New Keynesian model
with sticky prices but flexible wages, with a focus on the size and
persistence of the effects of monetary policy shocks. Later contributions
have extended that work in two dimensions. Some have relaxed the
assumptionofflexiblewages,andintroduceddifferentformsofnominal
and real wage rigidity. The work of Trigari (2006), Christoffel and
Linzert (2005), and Sveen and Weinke (2008) falls into that category.
Perhaps more interestingly, the focus of attention has gradually turned
to normative issues, and more specifically, to the implications of labor
market frictions and unemployment for the design of monetary policy.
See, For example the work of Blanchard and Galí (2010), Faia (2008,
2009), Ravenna and Walsh (2011), and Thomas (2008).15 Applications
usingthatapproachtointerpretU.S.postwardataincludeGertler,Sala,
andTrigari(2008),whoestimateamedium-scaleNewKeynesianmodel
withsearchandmatchingfrictions,andBarnichon(2010),whoexamines
themodel’sabilitytoaccountforthechangingcyclicalpropertiesoflabor
productivity.
Most of the work combining search and matching frictions with
nominal rigidities assumes some form of Nash bargaining of wages.
Wage stickiness is generally introduced by assuming that each period
only a fraction of firms engage in that bargaining with their workers
(Thomas (2008)), following the standard Calvo formalism. An alterna-
tive approach can be found in Christiano, Eichenbaum, and Trabandt
demonstratingitsabilitytogenerateendogenouslyasluggishresponseof
aggregate nominal wages and a persistent response of unemployment to
variousmacroshocks.
Alternatives approaches include the work of Christiano, Trabandt,
and Walentin (2010), who have modified the New Keynesian model
by embedding in it an alternative model of unemployment, where
the probability of finding a job is increasing in search effort, and
where imperfect risk sharing among individuals is a consequence of the
unobservabilityofeffort.
Gertler, Mark, Luca Sala, and Antonella Trigari (2008): “An Estimated Mon-
etary DSGE Model with Labor Market Frictions,” Journal of Money, Credit
andBanking40(8),1713–1764.
Gertler,Mark,andAntonellaTrigari(2009):“UnemploymentFluctuationswith
Staggered Nash Wage Bargaining,” Journal of Political Economy 117(1),
38–86.
Hall,Robert(2005):“EmploymentFluctuationswithEquilibriumWageSticki-
ness,”AmericanEconomicReview95(1),50–64.
Hall, Robert E., and Paul R. Milgrom (2008): “The Limited Influence of
Unemployment on the Wage Bargain,” American Economic Review 98(4),
1653–1674.
Jaimovich, Nir, and Sergio Rebelo (2009): “Can News about the Future Drive
theBusinessCycle?,”AmericanEconomicReview99(4),1097–1118.
Merz, Monica (1995): “Search in the Labor Market and the Real Business
Cycle,”JournalofMonetaryEconomics36,269–300.
Mortensen,DaleT.,andChristopherA.Pissarides(1994):“JobCreationandJob
Destruction in the Theory of Unemployment,” Review of Economic Studies
61(3),397–415.
Phillips, A. W. (1958): “The Relation between Unemployment and the Rate
of Change of Money Wage Rates in the United Kingdom, 1861–1957,”
Economica25,283–299.
Pissarides,Christopher(2000):EquilibriumUnemploymentTheory,MITPress,
CambridgeMA.
Ravenna,Federico,andCarlWalsh(2011):“Welfare-BasedOptimalMonetary
Policy with Unemployment and Sticky Prices,” American Economic Journal:
Macroeconomics3,130–162.
Shimer, Robert (2005): “The Cyclical Behavior of Equilibrium Unemployment
andVacancies,”AmericanEconomicReview95(1),25–49.
Smets, Frank, and Rafael Wouters (2003): “An Estimated Dynamic Stochastic
General Equilibrium Model of the Euro Area,” Journal of the European
EconomicAssociation1(5),1123–1175.
Smets,Frank,andRafaelWouters(2007):“ShocksandFrictionsinUSBusiness
Cycles: A Bayesian DSGE Approach,” American Economic Review 97(3),
586–606.
Sveen,Tommy,andLutzWeinke(2008):“NewKeynesianPerspectivesonLabor
MarketDynamics,”JournalofMonetaryEconomics55(5),921–930.
Thomas,Carlos(2008):“SearchandMatchingFrictionsandOptimalMonetary
Policy,”JournalofMonetaryEconomics55(5),936–956.
Trigari, Antonella (2006): “The Role of Search Frictions and Bargaining in
InflationDynamics,”mimeo.
Trigari,Antonella(2009):“EquilibriumUnemployment,JobFlows,andInflation
Dynamics,”JournalofMoney,CreditandBanking41(1),1–33.
Walsh,Carl(2003):“LaborMarketSearchandMonetaryShocks,”inS.Altug,J.
Chadha,andC.Nolan,eds.,ElementsofDynamicMacroeconomicAnalysis,
CambridgeUniversityPress,451–486.
Walsh, Carl (2005): “Labor Market Search, Sticky Prices, and Interest Rate
Rules,”ReviewofEconomicDynamics8,829–849.

220 CHAPTER7
EXERCISES
7.1. Unemployment and monetary policy in a model with flexible
prices
Consideravariationofthemodeldevelopedinchapters6and7,
withfirms’technologynowbeinggivenby
Y = N
t t
where N isaCESfunctionofthequantitieshiredofthedifferent
t
types of labor. The elasticity of substitution among the latter is
(cid:4) w. All firms reset their prices optimally each period (“flexible
prices”). An optimal employment subsidy is assumed which
exactly offsets the monopolistic competition distortion in the
goodsmarket.
a. Show that the dynamics of price inflation can be represented
byequation
π
t
p =βE
t
{π
t
p
+1
}−ϕλ w(u
t
−un)
b. Taking the welfare loss function derived in chapter 6 as a
starting point, show that the welfare loss for the present
economycanbewritten(uptoamultiplicativescalar)as
(cid:7)∞
E βk[α u2+(πp)2]
0 u t t
t=0
where u t is the unemployment rate and π t p≡p t −p t−1 is price
inflation, and derive an expression for the weight α as a
u
functionofexogenousparameters.
c. Derive the optimal discretionary monetary policy and charac-
terizetheimpliedequilibriumprocessesforunemploymentand
priceinflation.Show,inparticular,thataveragepriceinflation
will be positive. Can you think of a way to eliminate that
inflationarybias?
d. Derive an interest rate rule that will guarantee the implemen-
tationoftheoptimaldiscretionarypolicyoutcome.
e. Derive the optimal monetary policy under commitment and
characterize the implied equilibrium processes for unemploy-
ment and price inflation. Describe its main differences relative
totheoptimalpolicyunderdiscretion.

7.2. Wage inflation dynamics with wage markup and labor supply
shocks
Consideranextensionofthemodeldevelopedinthepresentchap-
ter in which labor disutility for household member (j,s) is given
by χ sϕ, for all (j,s) ∈ [0,1]×[0,1], where ξ ≡ logχ follows
t t t
an exogenous stationary stochastic process. In addition, a time-
varying elasticity of substitutionbetween labor types is assumed,
{(cid:4) w,t },implyingavariabledesiredwagemarkupµw t ≡log (cid:4) w (cid:4) , w t − ,t 1 .
a. Derive the equation describing wage inflation dynamics as a
functionoftherealwage,consumption,andemployment,and
show how the two disturbances ξ and µw enter its error term
t t
in a symmetric way thus creating an identification problem
in attempts to estimate the model (remark: this is the basis
for the Chari, Kehoe, and McGrattan (2009) critique of New
Keynesianmodels).
b. Discuss how the reformulation of the wage equation in
terms of the unemployment rate overcomes the previous
shortcoming.
7.3. Tamingthewealtheffectonlaborsupply
Consider a modification of the model developed in the present
chapter in which individual utility for household member
(j,s)∈[0,1]×[0,1]isassumedtobegivenby:
logC(j,s)−1 (j,s)χ(cid:17) s ϕ
t t t
where1 (j,s)isanindicatorfunctiontakingavalueequaltoone
t
ifindividual(j,s)isemployedinperiodt,andzerootherwise,and
Z
(cid:17) ≡ t
t
C
t
where C denotes aggregate consumption, and Z evolves over
t t
timeaccordingtothedifferenceequation
t t−1 t
where υ ∈ [0,1]. Full risk sharing of consumption among
householdmembersisassumed.

222 CHAPTER7
a. Showthatthehousehold’speriodutility,definedastheintegral
overitsmembers’utilities,isgivenby:
(cid:2)
1 N(j)1+ϕ
logC −χ (cid:17) t dj
t t t 1+ϕ
where N(j) ∈ [0,1] denotes the employment rate in period t
t
amongworkersspecializedintype j labor.
b. Derive the aggregate participation equation, and discuss how
υ willaffecttheresponseofthelaborforcetodifferentshocks.