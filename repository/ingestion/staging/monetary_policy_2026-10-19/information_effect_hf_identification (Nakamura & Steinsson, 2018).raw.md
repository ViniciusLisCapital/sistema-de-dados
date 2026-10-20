NBER WORKING PAPER SERIES
HIGH FREQUENCY IDENTIFICATION OF MONETARY NON-NEUTRALITY:
THE INFORMATION EFFECT
Emi Nakamura
Jón Steinsson
Working Paper 19260
http://www.nber.org/papers/w19260
NATIONAL BUREAU OF ECONOMIC RESEARCH
1050 Massachusetts Avenue
Cambridge, MA 02138
July 2013, Revised January 2018
We thank Miguel Acosta, Matthieu Bellon, Vlad Bouchouev, Nicolas Crouzet, Stephane Dupraz,
Michele Fornino, Jesse Garret, and Shaowen Luo, for excellent research assistance. We thank
Michael Abrahams, Tobias Adrian, Richard K. Crump, Matthias Fleckenstein, Michael Fleming,
Mark Gertler, Refet Gurkaynak, Peter Karadi, Hanno Lustig, Emanuel Moench, and Eric
Swanson for generously sharing data and programs with us. We thank Robert Barro, Marco
Bassetto, Gabriel Chodorow-Reich, Stephane Dupraz, Gauti Eggertsson, Mark Gertler, Refet
Gurkaynak, Samuel Hanson, Sophocles Mavroeidis, Emanuel Moench, Serena Ng, Roberto
Rigobon, Christina Romer, David Romer, Christoph Rothe, Eric Swanson, Ivan Werning,
Michael Woodford, Jonathan Wright and seminar participants at various institutions for valuable
comments and discussions. We thank the National Science Foundation (grant SES-1056107), the
Alfred P. Sloan Foundation, and the Columbia Business School Dean’s Office Summer Research
Assistance Program for financial support. The views expressed herein are those of the authors and
do not necessarily reflect the views of the National Bureau of Economic Research.
NBER working papers are circulated for discussion and comment purposes. They have not been
peer-reviewed or been subject to the review by the NBER Board of Directors that accompanies
official NBER publications.
© 2013 by Emi Nakamura and Jón Steinsson. All rights reserved. Short sections of text, not to
exceed two paragraphs, may be quoted without explicit permission provided that full credit,
including © notice, is given to the source.

High Frequency Identification of Monetary Non-Neutrality: The Information Effect
Emi Nakamura and Jón Steinsson
NBER Working Paper No. 19260
July 2013, Revised January 2018
JEL No. E30,E40,E50
ABSTRACT
We present estimates of monetary non-neutrality based on evidence from high-frequency
responses of real interest rates, expected inflation, and expected output growth. Our identifying
assumption is that unexpected changes in interest rates in a 30-minute window surrounding
scheduled Federal Reserve announcements arise from news about monetary policy. In response to
an interest rate hike, nominal and real interest rates increase roughly one-for-one, several years
out into the term structure, while the response of expected inflation is small. At the same time,
forecasts about output growth also increase—the opposite of what standard models imply about a
monetary tightening. To explain these facts, we build a model in which Fed announcements affect
beliefs not only about monetary policy but also about other economic fundamentals. Our model
implies that these information effects play an important role in the overall causal effect of
monetary policy shocks on output.
Emi Nakamura
Columbia Business School
3022 Broadway, Uris Hall 820
New York, NY 10027
and NBER
enakamura@columbia.edu
Jón Steinsson
Department of Economics
Columbia University
1026 International Affairs Building
420 West 118th Street
New York, NY 10027
and NBER
jsteinsson@columbia.edu

1 Introduction
Acentralquestioninmacroeconomicsishowmonetarypolicyaffectstheeconomy. Thekeyempir-
icalchallengeinansweringthisquestionisthatmostchangesininterestrateshappenforareason.
Forexample,theFedmightlowerinterestratestocounteracttheeffectsofanadverseshocktothe
financial sector. In this case, the effect of the Fed’s actions are confounded by the financial shock,
making it difficult to identify the effects of monetary policy. The most common approach to over-
coming this endogeneity problem is to attempt to control for confounding variables. This is the
approach to identification in VAR studies such as Christiano, Eichenbaum, and Evans (1999) and
Bernanke, Boivin, and Eliasz (2005), and also in the work of Romer and Romer (2004). The worry
with this approach is that despite efforts to control for important confounding variables, some en-
dogeneitybiasremains(see,e.g., Rudebusch,1998).
An alternative approach—the one we pursue in this paper—is to focus on movements in bond
pricesinanarrowwindowaroundscheduledFederalOpenMarketCommittee(FOMC)meetings.
This high frequency identification approach was pioneered by Cook and Hahn (1989), Kuttner
(2001), and Cochrane and Piazzesi (2002). It exploits the fact that a disproportionate amount of
monetarynewsisrevealedatthetimeoftheeightregularlyscheduledFOMCmeetingseachyear.
Thelumpywayinwhichmonetarynewsisrevealedallowsforadiscontinuity-basedidentification
scheme.
Weconstructmonetaryshocksusingunexpectedchangesininterestratesovera30-minutewin-
dowsurroundingscheduledFederalReserveannouncements. Allinformationthatispublicatthe
beginning of the 30-minute window is already incorporated into financial markets, and, therefore,
doesnotshowupasspuriousvariationinthemonetaryshock. Suchspuriousvariationisanimpor-
tant concern in VARs. For example, Cochrane and Piazzesi (2002) show that VAR methods (even
using monthly data) interpret the sharp drop in interest rates in September 2001 as a monetary
shockasopposedtoareactiontotheterroristattackson9/11/2001.
A major strength of the high-frequency identification approach we use is how cleanly it is able
toaddresstheendogeneityconcern. Asisoftenthecase,thiscomesatthecostofreducedstatistical
power. The monetary shocks we estimate are quite small (they have a standard deviation of only
about 5 basis points). This “power problem” precludes us from directly estimating their affect on
future output. Intuitively, output several quarters in the future is influenced by a myriad of other
shocks,renderingthesignal-to-noiseratioinsuchregressionstoosmalltoyieldreliableinference.
We can, however, measure the response of variables that respond contemporaneously such as
1

financialvariablesandsurveyexpectations. Sincethelate1990’sithasbeenpossibletoobservethe
response of real interest rates via the Treasury Inflation Protected Securities (TIPS) market. This is
important since the link between nominal interest rates and real interest rates is the distinguishing
feature of models in which monetary policy affects real outcomes. All models—Neoclassical and
New Keynesian—imply that real interest rates affect output. However, New Keynesian and Neo-
classicalmodelsdiffersharplyastowhethermonetarypolicyactionscanhavepersistenteffectson
real interest rates. In New Keynesian models, they do, while in Neoclassical models real interest
ratesaredecoupledfrommonetarypolicy. Byfocusingontheeffectsofmonetarypolicyshockson
realinterestrates,wearesheddinglightonthecoreempiricalissueinmonetaryeconomics.
WeusethetermstructureofinterestratesatthetimeofFOMCmeetingstoshowthatthemone-
taryshocksweidentifyhavelargeandpersistenteffectsonexpectedrealinterestratesasmeasured
by TIPS. Nominal and real interest rates respond roughly one-for-one several years out into the
termstructureinresponsetoourmonetaryshocks. Theeffectonrealratespeaksataround2years
and then falls monotonically to zero at 10 years. In sharp contrast, the response of break-even in-
flation (the difference between nominal and real rates from TIPS) is essentially zero at horizons
up to three years. At longer horizons, the response of break-even inflation becomes modestly, but
significantly, negative. A tightening of monetary policy therefore eventually reduces inflation—as
standardtheorywouldpredict. However,theresponseissmallandoccursonlyafteralonglag.
What can we conclude from these facts? Under the conventional interpretation of monetary
shocks, these facts imply a great deal of monetary non-neutrality. Intuitively, a monetary-policy-
induced increase in real interest rates leads to a drop in output relative to potential, which in turn
leadstoadropininflation. Theresponseofinflationrelativetothechangeintherealinterestratesis
determinedbytheslopeofthePhillipscurve(aswellastheintertemporalelasticityofsubstitution).
Iftheinflationresponseissmallrelativetothechangeintherealrates,theslopeofthePhillipscurve
mustbesmallimplyinglargenominalandrealrigiditiesand,therefore,largeamountsofmonetary
non-neutrality.
There is, however, an additional empirical fact that does not fit this interpretation. We docu-
ment that in response to an unexpected increase in the real interest rate (a monetary tightening),
survey estimates of expected output growth rise. Under the conventional interpretation of mone-
tary shocks, a tightening of policy should lead to a fall in output growth. Our empirical finding
regarding output growth expectations is therefore the opposite direction from what one would ex-
pectfromtheconventionalinterpretationofmonetaryshocks.
AnaturalinterpretationofthisevidenceisthatFOMCannouncementsleadtheprivatesectorto
2

updateitsbeliefsnotonlyaboutthefuturepathofmonetarypolicy,butalsoaboutothereconomic
fundamentals. For example, when the Fed Chair announces that the economy is strong enough
to withstand higher interest rates, market participants may react by reconsidering their own be-
liefs about the economy. Market participants may contemplate that perhaps the Fed has formed
a more optimistic assessment of the economic outlook than they have and that they may want to
reconsider their own assessments. Following Romer and Romer (2000), we refer to the effect of
FOMC announcements on private sector views of non-monetary economic fundamentals as “Fed
informationeffects.”
The Fed information effect calls for more sophisticated modeling of the effects of monetary
shocks than is standard. The main challenge is how to parsimoniously model these information
effects. Wepresentanewmodelinwhichmonetaryshocksaffectnotonlythetrajectoryofthereal
interestrate,butalsoprivatesectorbeliefsaboutthetrajectoryofthenaturalrateofinterest. Thisis
anaturalwayofmodelingtheinformationcontentofFedannouncementssinceoptimalmonetary
policycallsforinterestratestotrackthenaturalrateinsimplemodels. SincetheFedisattempting
totrackthenaturalrate,itisnaturaltoassumethatFedannouncementscontaininformationabout
thepathofthenaturalrate.
Our“Fedinformationmodel”implieslessmonetarynon-neutralitythroughconventionalchan-
nels than a model that ignores Fed information. The reason is that the response of inflation is de-
terminedbytheresponseoftherealinterestrategap—thegapbetweentheresponseofrealinterest
ratesandthenaturalrealrate—whichissmallerthantheresponseofrealinterestratesthemselves.
Intuitively, some of the increase of real rates is interpreted not as a tightening of policy relative to
the natural rate—which would push inflation down—but rather as an increase in the natural rate
itself—whichdoesnot.
If the Fed information effect is large, even a large response of real interest rates to a monetary
shock is consistent with the conventional channel of monetary non-neutrality being modest (since
the real interest rate movement is mostly due to a change in the natural real rate). However, this
does not mean that the Fed is powerless. To the contrary, if the Fed information effect is large, the
Fedhasagreatdealofpoweroverprivatesectorbeliefsabouteconomicfundamentals,whichmay
in turn have large effects on economic activity. If a Fed tightening makes the private sector more
optimistic about the future, this will raise current consumption and investment in models with
dynamiclinkages. DependingonthestrengthoftheFedinformationeffect,ourevidence,therefore,
suggestseitherthattheFedhasagreatdealofpowerovertheeconomythroughtraditionalchannels
or that the Fed has a great deal of power over the economy through non-traditional information
3

channels(orsomecombinationofthetwo).
To assess the extent of Fed information and the nature of Fed power over the economy, we
estimate our Fed information model using as target moments the responses of real interest rates,
expected inflation, and expected output growth discussed above. Here, we follow in the tradition
ofearlierquantitativeworksuchasRotembergandWoodford(1997)andChristiano,Eichenbaum,
and Evans (2005), with two important differences. First, our empirical targets are identified using
high-frequencyidentificationasopposedtoaVAR.Second,weallowforFedinformationeffectsin
ourmodel.
OurestimatesimplythattheFedinformationeffectislarge. Roughly2/3oftheresponseofreal
interestratestoFOMCannouncementsareestimatedtobearesponseofthenaturalrateofinterest
and only 1/3 a tightening of real rates relative to the natural rate. This large estimate of the Fed
informationeffectallowsustosimultaneouslymatchthefactthatbeliefsaboutoutputgrowthrise
followingamonetaryshockandinflationeventuallyfalls. Beliefsaboutoutputgrowthrisebecause
agents are more optimistic about the path for potential output. Inflation falls because a portion of
theshockisinterpretedasratesrisingrelativetothenaturalrate.
Once we allow for Fed information effects, the causal effect of monetary policy is much more
subtle to identify. Our estimates imply that surprise FOMC monetary tightenings have large posi-
tiveeffectsonexpectationsaboutoutputgrowth. Doesthisimplythatthemonetaryannouncements
cause output to increaseby large amounts? No, not necessarily. Much of thenews the Fed reveals
aboutnon-monetaryfundamentalswouldhaveeventuallybeenrevealedthroughothersources. To
correctly assess the causal effect of monetary policy, one must compare versus a counterfactual in
whichthechangesinfundamentalstheFedrevealsinformationaboutoccurevenintheabsenceof
the announcement. The causal effect of the Fed information is then limited to the effect on output
oftheFedannouncingthisinformationearlierthanitotherwisewouldhavebecomeknown.
Our model makes these channels precise. Recent discussions of monetary policy have noted
the Fed’s reluctance to lower interest rates for fear it might engender pessimistic expectations that
wouldfightagainstitsgoalofstimulatingtheeconomy. Ouranalysissuggeststhattheseconcerns
maybewell-foundedatleastatthezerolowerbound.1 Moreover,ourmodelsuggeststhattheim-
plicationsofsystematicmonetarypolicyactionsarequitedifferentfromthoseofmonetaryshocks.
Thereasonisthatsystematicmonetarypolicyactionsdon’tentailinformationeffectssince,bydef-
inition, they are not based on private information. In other words, there is an important external
1Revealinginformationaboutnaturalrates,evenbadnews,islikelytobewelfareimprovingaslongastheFedcan
varyinterestratestotrackthenaturalrate.Atthezerolowerbound,theFedhoweverloosesitsabilitytotrackthenatural
rate.Withholdingbadnewsmaythenbeoptimal.
4

validityproblemwheneverresearchersusemonetaryshockstotrytoinfertheeffectsofsystematic
monetarypolicy. Weuseastructuralmodeltosolvethisexternalvalidityproblem.
Ourmeasureofmonetaryshocksisbasednotonlyonsurprisechangesinthefederalfundsrate
but also changes in the path of future interest rates in response to FOMC announcements. This is
importantsinceoverthepast15yearsforwardguidancehasbecomeanincreasinglyimportanttool
intheconductofmonetarypolicy(Gurkaynak, Sack, andSwanson,2005). Thisalsoimpliesthatit
is important to focus on a narrow 30-minute window as opposed to the 1-day or 2-day windows
more commonly used in prior work. We make use of Rigobon’s (2003) heteroskedasticity-based
estimatortoshowthatOLSresultsbasedonmonetaryshocksconstructedfromlonger-terminterest
ratechangesoverone-daywindowsaroundFOMCannouncementsareconfoundedbysubstantial
“background noise” that lead to unreliable inference and in particular can massively overstate the
true statistical precision of the estimates. In contrast, OLS yields reliable results when a 30-minute
windowisused.
Animportantquestionaboutourempiricalestimatesiswhethersomeoftheeffectsofourmon-
etaryshocksonlonger-termrealinterestratesreflectchangesinriskpremiaasopposedtochanges
in expected future short-term real interest rates. We use three main approaches to analyze this is-
sue: directsurveyexpectationsofrealinterestrates,anaffinetermstructuremodel,andananalysis
of mean reversion. None of these pieces of evidence suggest that movements in risk premia at the
time of FOMC announcements play an important role in our results. In other words, our results
suggestthattheexpectationshypothesisofthetermstructureisagoodapproximationinresponse
toourmonetaryshocks, eventhoughitisnotagoodapproximationunconditionally. Thisiswhat
weneedforouranalysistobevalid.
Anotherimportant(andrelated)questioniswhethertheremightbeapredictablecomponentof
themonetaryshocksweanalyzeandhowthismightaffecttheinterpretationofourresults. Inour
analysis of real interest rates, the dependent variables are high frequency changes. The error terms
in these regressions, therefore, only contain information revealed in that narrow window, and the
identifying assumption is that our monetary shock is orthogonal to this limited amount of infor-
mation. This methodology has the advantage that we need not assume that our monetary shock
is orthogonal to macro shocks occurring on other days or to slow-moving confounding variables.
The identifying assumptions are stronger when we analyze the effects of our monetary shocks on
surveyexpectationsfrom theBlueChipdata. Inthatanalysisthedependentvariableisamonthly
change and the identifying assumption is that the monetary shock is orthogonal to confounders
overthewholemonth. Similar(stronger)assumptionsarerequiredwhenhighfrequencymonetary
5

shocks are used as external instruments in a VAR—as in Gertler and Karadi (2015)—since the out-
comevariablesarechangesoverseveralmonths. Additionally,predictabilityisdifficulttoestablish
convincinglyduetodataminingandpesoproblemconcerns.
Our paper relates to several strands of the literature in monetary economics. The seminal em-
pirical paper on Fed information is Romer and Romer (2000). Faust, Swanson, and Wright (2004)
present a critique of their findings. More recently, Campbell et al. (2012) show that an unexpected
tighteningleadssurveyexpectationsofunemploymenttofall. Thetheoreticalliteratureonthesig-
nalingeffectsofmonetarypolicyislarge. EarlycontributionsincludeCukiermanandMeltzer(1986)
and Ellingsen and Soderstrom (2001). Recent contributions include Berkelmans (2011), Melosi
(2017), Tang(2015), FrankelandKartik(2017), andAndradeetal. (2016). Thepriorliteraturetypi-
callyassumesthatthecentralbankmustcommunicateonlythroughitsactions(e.g.,changesinthe
fedfundsrate),whereasweallowtheFedtocommunicatethroughitswords(FOMCstatements).
Ourestimatesoftheeffectsofmonetaryannouncementsonrealinterestratesusinghigh-frequency
identificationarerelatedtorecentworkbyHansonandStein(2015)andGertlerandKaradi(2015).
We make different identifying assumptions than Hanson and Stein, use a different definition of
the monetary shock, and come to quite different conclusions about the long-run effects of mone-
tary policy.2 There are also important methodological differences between our work and that of
Gertler and Karadi (2015). They rely on a VAR to estimate the dynamic effects of monetary policy
shocks. They are therefore subject to the usual concern that the VAR they use may not accurately
describethedynamicresponseofkeyvariablestoamonetaryshock. Ouridentificationapproachis
entirelyVAR-free. Ourpaperisalsorelatedtoseveralrecentpapersthathaveusedhigh-frequency
identificationtostudytheeffectsofunconventionalmonetarypolicyduringtherecentperiodover
which short-term nominal interest rates have been at their zero lower bound (Gagnon et al., 2010;
KrishnamurthyandVissing-Jorgensen,2011;Wright,2012;Gilchristetal.,2015,Rosa,2012).
The paper proceeds as follows. Section 2 describes the data we use in our analysis. Section
3 presents our empirical results regarding the response nominal and real interest rates and TIPS
break-eveninflationtomonetarypolicyshocks. Section4presentsourempiricalevidenceonoutput
growthexpectations. Section5presentsourFedinformationmodel,describesourestimationmeth-
ods, and presents the results of our estimation of the Fed information model. Section 6 discusses
howtothinkaboutthecausaleffectofthemonetaryannouncementinthefaceofFedinformation.
Section7concludes.
2Inearlierwork,BeecheyandWright(2009)analyzetheeffectofunexpectedmovementsinthefederalfundsrateat
thetimeofFOMCannouncementsonnominalandreal5-yearand10-yearyieldsandthefive-to-tenyearforwardover
theperiodFebruary2004toJune2008.Theirresultsaresimilartooursforthe5-yearand10-yearyields.
6

2 Data
To construct our measure of monetary shocks, we use tick-by-tick data on federal funds futures
and eurodollar futures from the CME Group (owner of the Chicago Board of Trade and Chicago
MercantileExchange). Thesedatacanbeusedtoestimatechangesinexpectationsaboutthefederal
funds rate at different horizons after an FOMC announcement (see Appendix A). The tick-by-tick
data we have for federal funds futures and eurodollar futures is for the sample period 1995-2012.
Fortheperiodsince2012weusedataonchangesinthepricesofthesamefiveinterestratefutures
overthesame30-minutewindowsaroundFOMCannouncementsthatRefetGurkaynakgraciously
sharedwithus.
WeobtainthedatesandtimesofFOMCmeetingsupto2004fromtheappendixtoGurkaynak,
Sack,andSwanson(2005). WeobtainthedatesoftheremainingFOMCmeetingsfromtheFederal
Reserve Board website at http://www.federalreserve.gov/monetarypolicy/fomccale
ndars.htm. For the latter period, we verified the exact times of the FOMC announcements using
thefirstnewsarticleabouttheFOMCannouncementonBloomberg. Wecross-referencedthesedates
and times with data we obtained from Refet Gurkaynak and in a few cases used the time stamp
fromhisdatabase.
To measure the effects of our monetary shocks on interest rates, we use several daily interest
rateseries. TomeasuremovementsinTreasuriesathorizonsof1yearormore,weusedailydataon
zero-couponnominalTreasuryyieldsandinstantaneousforwardratesconstructedbyGurkaynak,
Sack,andSwanson(2007). ThesedataareavailableontheFed’swebsiteathttp://www.federa
lreserve.gov/pubs/feds/2006/200628/200628abs.html. We also use the yields on 3M
and6MTreasurybills. WeretrievethesefromtheFederalReserveBoard’sH.15datarelease.
Tomeasuremovementsinrealinterestrates,weusezero-couponyieldsandinstantaneousfor-
ward rates constructed by Gurkaynak, Sack, and Wright (2010) using data from the TIPS market.
These data are available on the Fed’s website at http://www.federalreserve.gov/pubs/
feds/2008/200805/200805abs.html. TIPS are “inflation protected” because the coupon and
principal payments are multiplied by the ratio of the reference CPI on the date of maturity to the
reference CPI on the date of issue.3 The reference CPI for a given month is a moving average of
the CPI two and three months prior to that month, to allow for the fact that the Bureau of Labor
Statisticspublishesthesedatawithalag.
TIPSwerefirstissuedin1997andwereinitiallysoldatmaturitiesof5,10and30years,butonly
3Thisholdsunlesscumulativeinflationisnegative,inwhichcasenoadjustmentismadefortheprinciplepayment.
7

the10-yearbondshavebeenissuedsystematicallythroughoutthesampleperiod. Othermaturities
have been issued more sporadically. While liquidity in the TIPS market was initially poor, TIPS
now represent a substantial fraction of outstanding Treasury securities. We start our analysis in
2000 to avoid relying on data from the period when TIPS liquidity was limited. For 2- and 3-year
yieldsandforwardswestartouranalysisin2004. Gurkaynak,Sack,andWright(2010)onlyreport
zero-couponyieldsforthesematuritiesfrom2004onward. Onereasonisthattoaccuratelyestimate
zero-couponyieldsatthismaturityitisnecessarytowaituntillongermaturityTIPSissuedseveral
years earlier have maturities in this range. To facilitate direct comparisons between nominal and
realinterestrates,werestrictoursampleperiodforthecorresponding2-and3-yearnominalyields
andforwardstothesametimeperiod.
Tomeasureexpectations,weusedataonexpectationsoffuturenominalinterestrates,inflation
andoutputgrowthfromtheBlueChipEconomicIndicators. BlueChipcarriesoutasurveyduringthe
firstfewdaysofeverymonthsolicitingforecastsofthesevariablesforuptothenext8quarters. We
usethemeanforecastforeachvariable. WealsousedataonGreenbookforecastsfromthePhiladel-
phiaFed. Thesedataarehostedandmaintainedonthedataset,https://www.philadelphiafe
d.org/research-and-data/real-time-center/greenbook-data/philadelphia-data-
set. WeusetherealGDPgrowthvariablefromthisdataset.
To assess the role of risk premia, we use a daily decomposition of nominal and real interest
rate movements into risk-neutral expected future rates and risk premia obtained from Abrahams,
Adrian,Crump,andMoench(2015). Toassesstherobustnessofourresultsregardingtheresponse
of real interest rates we use daily data on inflation swaps from Bloomberg. Finally, we estimate the
response of stock prices to monetary announcements using daily data on the level of the S&P500
stockpriceindexobtainedfromYahooFinance.
3 Response of Interest Rates and Expected Inflation
Ourgoalinthissectionistoidentifytheeffectofthemonetarypolicynewscontainedinscheduled
FOMC announcements on nominal and real interest rates of different maturities. Specifically, we
estimate
∆s = α+γ∆i +(cid:15) , (1)
t t t
where∆s isthechangeinanoutcomevariableofinterest(e.g.,theyieldonafiveyearzero-coupon
t
Treasurybond),∆i isameasureofthemonetarypolicynewsrevealedintheFOMCannouncement,
t
8

(cid:15) isanerrorterm,andαandγ areparameters. Theparameterofinterestisγ,whichmeasuresthe
t
effectoftheFOMCannouncementon∆s relativetoitseffectonthepolicyindicator∆i .
t t
To identify a pure monetary policy shock, we consider the change in our policy indicator (∆i )
t
ina30-minutewindowaroundscheduledFOMCannouncements.4 Theideaisthatchangesinthe
policyindicatorinthese30-minutewindowsaredominatedbytheinformationaboutfuturemon-
etarypolicycontainedintheFOMCannouncement. Undertheassumptionthatthisistrue,wecan
simplyestimateequation(1)byordinaryleastsquares. Wealsopresentresultsforaheteroskedastic-
itybasedestimationapproach(Rigobon,2003;RigobonandSack,2004)whichisbasedonaweaker
identifying assumption to verify that our baseline identifying assumption is reasonable. In our
baselineanalysis,wefocusononlyscheduledFOMCannouncements,sinceunscheduledmeetings
mayoccurinreactiontoothercontemporaneousshocks.
Thepolicyindicatorweuseisacompositemeasureofchangesininterestratesatdifferentmatu-
ritiesspanningthefirstyearofthetermstructure. Untilrecently,mostauthorsusedunanticipated
changes in the federal funds rate (or closely related changes in very short term interest rates) as
their policy indicator. The key advantage of our measure is that it captures the effects of “forward
guidance.” Forward guidance refers to announcements by the Fed that convey information about
future changes in the federal funds rate. Over the past 15 years, the Federal Reserve has made
greater and greater use of such forward guidance. In fact, changes in the federal funds rate have
often been largely anticipated by markets once they occur. Gurkaynak, Sack, and Swanson (2005)
convincingly argue that unanticipated changes in the federal funds rate capture only a small frac-
tion of the monetary policy news associated with FOMC announcements in recent years (see also,
Campbelletal.,2012).
Thespecificcompositemeasureweuseasourpolicyindicatoristhefirstprinciplecomponentof
theunanticipatedchangeoverthe30-minutewindowsdiscussedaboveinthefollowingfiveinterest
rates: thefederalfundsrateimmediatelyfollowingtheFOMCmeeting,theexpectedfederalfunds
rateimmediatelyfollowingthenextFOMCmeeting,andexpected3-montheurodollarinterestrates
at horizons of two, three and four quarters. We refer to this policy indicator as the “policy news
shock.” Weusedataonfederalfundsfuturesandeurodollarfuturestomeasurechangesinmarket
expectationsaboutfutureinterestratesatthetimeofFOMCannouncements. Thescaleofthepolicy
news shock is arbitrary. For convenience, we rescale it such that its effect on the 1-year nominal
Treasury yield is equal to one. Appendix A provides details about the construction of the policy
4Specifically, we calculate the monetary shock using a 30-minute window from 10 minutes before the FOMC an-
nouncementto20minutesafterit.
9

newsshock.5
3.1 BaselineEstimates
Table 1 presents our baseline estimates of monetary shocks on nominal and real interest rates and
break-even inflation. Each estimate in the table comes from a separate OLS regression of the form
discussed above—equation (1). In each case the independent variable is the policy news shock
measured over a 30-minute window around an FOMC announcement, while the change in the
dependentvariableismeasuredoveraone-daywindow.6
The first column of Table 1 presents the effects of the policy news shock on nominal Treasury
yieldsandforwards. Recallthatthepolicynewsshockisscaledsuchthattheeffectontheone-year
Treasury yield is 100 basis points. Looking across different maturities, we see that the effect of the
shockissomewhatsmallerforshortermaturities,peaksat110basispointsforthe2-yearyieldand
thendeclinesmonotonicallyto38basispointsforthe10-yearyield. Sincelonger-termyieldsreflect
expectations about the average short-term interest rate over the life of the long bond, it is easier
to interpret the time-path of the response of instantaneous forward rates. Abstracting from risk
premia,theserevealmarketexpectationsabouttheshort-terminterestratethatthemarketexpects
toprevailatcertainpointsintimeinthefuture.7 Theimpactofourpolicynewsshockonforward
rates is also monotonically declining in maturity from114 basis points at 2-years to -8 basis points
at 10-years. We show below that the negative effect on the 10-year nominal forward rate reflects a
declineinbreak-eveninflationatlonghorizons.8
ThesecondcolumnofTable1presentstheeffectsofthepolicynewsshockonrealinterestrates
measuredusingTIPS.Whilethepolicynewsshockaffectsnominalratesbyconstruction,thisisnot
thecaseforrealinterestrates. Inneoclassicalmodelsoftheeconomy,theFedcontrolsthenominal
interestratebuthasnoimpactonrealinterestrates. Insharpcontrasttothis,weestimatetheimpact
of our policy news shock on the 2-year real yield to be 106 basis points, and the impact on the 3-
yearrealyieldtobe102basispoints. Again,thetime-pathofeffectsiseasiertointerpretbyviewing
5Ourpolicynewsshockvariableiscloselyrelatedtothe“pathfactor”consideredbyGurkaynak,Sack,andSwan-
son (2005). The five interest rate futures that we use to construct our policy news shock are the same five futures as
Gurkaynak,Sack,andSwanson(2005)use. Theymotivatethechoiceoftheseparticularfuturesbyliquidityconsidera-
tions.TheyadvocatetheuseoftwoprinciplecomponentstocharacterizethemonetarypolicynewsatthetimeofFOMC
announcements—a“targetfactor”anda“pathfactor.” Wefocusonasinglefactorforsimplicity. SeealsoBarakchian
andCrowe(2013).
6Thelongerwindowforthedependentvariableaddsnoisetotheregressionwithoutbiasingthecoefficientofinterest.
7Forexample,theeffectonthe2-yearinstantaneousforwardrateistheeffectontheshort-terminterestratethatthe
marketexpectstoprevailin2yearstime.
8Our finding that long-term inflation expectations decline in response to contractionary monetary policy shock is
consistentwithBeechey,Johannsen,andLevin(2011)andGu¨rkaynak,Levin,andSwanson(2010).
10

TABLE 1
Table1R:eRspeospnsoen osef IonfteIrnetsetr ResatteRsa atneds aInnfdlatIinoflna ttoi othnet PootlhiceyP Noeliwcys SNheowcksShock
Nominal Real Inflation
3M Treasury Yield 0.67
(0.14)
6M Treasury Yield 0.85
(0.11)
1Y Treasury Yield 1.00
(0.14)
2Y Treasury Yield 1.10 1.06 0.04
(0.33) (0.24) (0.18)
3Y Treasury Yield 1.06 1.02 0.04
(0.36) (0.25) (0.17)
5Y Treasury Yield 0.73 0.64 0.09
(0.20) (0.15) (0.11)
10Y Treasury Yield 0.38 0.44 -0.06
(0.17) (0.13) (0.08)
2Y Treasury Inst. Forward Rate 1.14 0.99 0.15
(0.46) (0.29) (0.23)
3Y Treasury Inst. Forward Rate 0.82 0.88 -0.06
(0.43) (0.32) (0.15)
5Y Treasury Inst. Forward Rate 0.26 0.47 -0.21
(0.19) (0.17) (0.08)
10Y Treasury Inst. Forward Rate -0.08 0.12 -0.20
(0.18) (0.12) (0.09)
Each estimatecomesfroma separate OLS regression. The dependent variable in each regression is
the one day change in the variable stated in the left-most column. The independent variable is a
change in the policy news shock over a 30 minute window around the time of FOMC
announcements. The sample period is all regularly scheduled FOMC meetings from 1/1/2000 to
3/19/2014, except that we drop July 2008 through June 2009. For 2Y and 3Y yields and real
forwards,thesamplestartsinJanuary2004. Thesamplesizeforthe2Yand3Yyieldsandforwards
is 74. The sample size for all other regressions is 106. In all regressions, the policy news shock is
computed from these same 106 observations. Robust standard errors are in parentheses.
11

estimatesforinstantaneousforwardrates. Theeffectoftheshockonthe2-yearrealforwardrateis
99basispoints. Itfallsmonotonicallyatlongerhorizonsto88basispointsat3years,47basispoints
at5years,and12basispointat10years(whichisnotstatisticallysignificantlydifferentfromzero).
Evidently, monetary policy shocks can affect real interest rates for substantial amounts of time (or
at least markets believe it can). However, in the long-run, the effect of monetary policy shocks on
realinterestratesiszeroastheorywouldpredict.
ThethirdcolumnofTable1presentstheeffectofthepolicynewsshockonbreak-eveninflation
as measured by the difference between nominal Treasury rates and TIPS rates. The first several
rowsprovideestimatesbasedonbondyields,whichindicatethattheresponseofbreak-eveninfla-
tionissmall. Theshorterhorizonestimatesareactuallyslightlypositivebutthenbecomenegative
atlongerhorizons. Noneoftheseestimatesarestatisticallysignificantlydifferentfromzero. Again,
itishelpfultoconsiderinstantaneousforwardbreak-eveninflationratestogetestimatesofbreak-
even inflation at points in time in the future. The response of break-even inflation implied by the
2 year forwards is slightly positive, though statistically insignificant. The response is negative at
longer horizons: for maturities of 3, 5 and 10 years, the effect is -6, -21 and -20 basis points, re-
spectively. Itisonlytheresponsesat5and10yearsthatarestatisticallysignificantlydifferentfrom
zero. Ourevidencethuspointstobreak-eveninflationrespondingmodestlyandquitegraduallyto
monetaryshocksthathaveasubstantialeffectonrealinterestrates.
Table 1 presents results for a sample period from January 1st 2000 to March 19th 2014, except
that we drop the period spanning the height of the financial crisis in the second half of 2008 and
the first half of 2009.9 We choose to drop the height of the financial crisis because numerous well-
documentedassetpricinganomaliesaroseduringthiscrisisperiod,andwewishtoavoidthecon-
cern that our results are driven by these anomalies. However, similar results obtain for the full
sample including the crisis, as well as a more restrictive data sample ending in 2007, and for a
samplethatalsoincludesunscheduledFOMCmeetings(seeTableA.1). Theresultsforthesample
ending in 2007 show that our results are unaffected by dropping the entire period during which
thezero-lower-boundisbindingandtheFedisengagedinquantitativeeasing. TableA.2presents
results analogous to those of Table 1 but using the unexpected change in the fed funds rate as the
policyindicator.
Figure1presentsabinnedscatterplotoftherelationshipbetweenthepolicynewsshockandthe
5-yearrealyield(theaverageexpectedresponseoftheshort-termrealinterestratesoverthenext5
9The sample period for 2- and 3-year yields and forwards is somewhat shorter (it starts in 2004) because of data
limitations(seesection2fordetails).
12

Figure1: BinnedScatterPlotfor5-YearReal-YieldRegression
0.15
0.10
0.05
0.00
‐0.05
‐0.10
‐0.15
‐0.20
‐0.12 ‐0.08 ‐0.04 0.00 0.04 0.08 0.12
Policy News Shock
years). Thevariationinthepolicynewshockrangesfrom-11basispointsto+10basispoints. The
relationship between the change in the 5-year real yield and the policy news shock does not seem
tobedrivenbyafewoutliers.
3.2 BackgroundNoiseinInterestRates
A concern regarding the estimation approach we describe above is that other non-monetary news
might affect our monetary policy indicator during the window we consider around FOMC an-
nouncements. Ifthisisthecase,itwillcontaminateourmeasureofmonetaryshocks. Thisconcern
looms much larger if one considers longer event windows than our baseline 30-minute window.
It has been common in the literature on high frequency identification of monetary policy to con-
sideraone-ortwo-daywindowaroundFOMCannouncements(e.g., Kuttner,2001;Cochraneand
Piazzesi, 2002; Hanson and Stein, 2015). In these cases, the identifying assumption being made is
that no other shocks affect the policy indicator in question during these one or two days. Espe-
cially when the policy indicator is based on interest rates several quarters or years into the term
structure—as has recently become common to capture the effects of forward guidance—the as-
sumption that no other shocks affect this indicator over one or two days is a strong assumption.
Interest rates at these maturities fluctuate substantially on non-FOMC days, suggesting that other
13

shocks than FOMC announcements affect these interest rates on FOMC days. There is no way of
knowingwhethertheseothershocksaremonetaryshocksornon-monetaryshocks.
Toassesstheseverityofthisproblem,Table2comparesestimatesofequation(1)basedonOLS
regressions to estimates based on a heteroskedasticity-based estimation approach developed by
Rigobon(2003)andRigobonandSack(2004). Wedothisbothfora30-minutewindowandfora1-
daywindow. Theheteroskedasticity-basedestimatorisdescribedindetailinAppendixB. Itallows
for “background” noise in interest rates arising from other shocks during the event windows be-
ingconsidered. Theideaistocomparemovementsininterestratesduringeventwindowsaround
FOMCannouncementstootherequallylongandotherwisesimilareventwindowsthatdonotcon-
tainanFOMCannouncement. Theidentifyingassumptionisthatthevarianceofmonetaryshocks
increasesatthetimeofFOMCannouncements,whilethevarianceofothershocks(thebackground
noise)isunchanged.
ThetoppanelofTable2comparesestimatesbasedonOLStothosebasedontheheteroskedasticity-
basedestimator(Rigobonestimator)forasubsetoftheassetsweconsiderinTable1whentheevent
windowis30-minutesasinourbaselineanalysis. Thedifferencebetweenthetwoestimatorsisvery
small, both for the point estimates and the confidence intervals.10 This result indicates that there
is in fact very little background noise in interest rates over a 30-minute window around FOMC
announcementsandtheOLSidentifyingassumption—thatonlymonetaryshocksoccurwithinthe
30-minutewindow—thusyieldsapointestimateandconfidenceintervalsthatareclosetocorrect.
TableA.3presentsafullsetofresultsbasedontheRigobonestimatoranda30-minutewindow. It
confirmsthatOLSyieldsverysimilarresultstotheRigobonestimatorforalltheassetsweconsider
whentheeventwindowis30minutes.
Incontrast,theproblemofbackgroundnoiseisquiteimportantwhentheeventwindowbeing
used to construct our policy news shocks is one day. The second panel of Table 2 compares esti-
mates based on OLS to those based on the Rigobon estimator for policy news shocks constructed
using a one-day window. In this case, the differences between the OLS and Rigobon estimates are
substantial. The point estimates in some cases differ by dozens of basis points and have different
signs in three of the six cases considered. However, the most striking difference arises for the con-
fidence intervals. OLS yields much narrower confidence intervals than those generated using the
10The confidence intervals for the Rigobon estimator in Table 2 are constructed using a procedure that is robust to
inferenceproblemsthatarisewhentheamountofbackgroundnoiseislargeenoughthatthereisasignificantprobability
thatthedifferenceinthevarianceofthepolicyindicatorbetweenthesampleofFOMCannouncementsandthe“con-
trol”sampleisclosetozero. Inthiscase,theconventionalbootstrapapproachtoconstructingconfidenceintervalswill
yieldinaccurateresults. AppendixCdescribesthemethodweusetoconstructconfidenceintervalsindetail. Wethank
SophoclesMavroeidisforsuggestingthisapproachtous.
14

TABLE 2
TableA2:llAowlloinwg iFnogr fBoarcBkagcrokugnrdo uNnodisNe ioni sIentienreIsnt tReraetesstRates
2-Year Forward 5-Year Forward 10-Year Forward
Nominal Real Nominal Real Nominal Real
Policy News Shock, 30-Minute Window:
1.14 0.99 0.26 0.47 -0.08 0.12
OLS
[0.23, 2.04] [0.41, 1.57] [-0.12, 0.64] [0.14, 0.80] [-0.43, 0.28] [-0.12, 0.36]
1.10 0.96 0.22 0.46 -0.12 0.11
Rigobon
[0.31, 2.36] [0.45, 1.82] [-0.14, 0.64] [0.15, 0.84] [-0.46, 0.24] [-0.13, 0.35]
Policy News Shock, 1-Day Window:
1.24 1.00 0.44 0.48 0.05 0.15
OLS
[0.80, 1.69] [0.57, 1.43] [0.18, 0.70] [0.20, 0.76] [-0.20, 0.29] [-0.10, 0.39]
0.93 0.82 -0.11 0.33 -0.51 -0.04
Rigobon
[-0.64, 2.08] [0.38, 3.20] [-1.23, 0.33] [-0.07, 1.12] [-1.93, -0.08] [-0.51, 0.45]
2-Year Nominal Yield, 1-Day Window
1.23 0.94 0.64 0.54 0.18 0.20
OLS
[1.07, 1.38] [0.69, 1.20] [0.43, 0.84] [0.31, 0.76] [0.01, 0.35] [0.02, 0.38]
1.14 0.82 -0.11 0.33 -0.51 -0.04
Rigobon (90% CI)
[0.82, 1.82] [0.62, 2.98] [-7.94, 0.60] [-0.01, 7.48] [-10.00, -0.21] [-4.57, 0.38]
Eachestimatecomesfromaseparate"regression."Thedependentvariableineachregressionistheonedaychangeinthevariable
stated at the top of that column. The independent variable in the first panel of results is the 30-minute change in the policy news
shockaroundFOMCmeetingtimes,inthesecondpanelitisthe1-daychangeinthepolicynewsshock,andinthethirdpanelitis
the 1-day change in the 2-Year nominal yield. In each panel, we report results based on OLS and Rigobon's heteroskedasticity
based estimation approach. We report a point estimate and 95% confidence intervals except in the last row of Rigobon estimates
whichreports90%confidenceintervals.Thesampleof"treatment"daysfortheRigobonmethodisallregularlyscheduledFOMC
meeting days from 1/1/2000 to 3/19/2014—this is also the period for which the policy news shock is constructed in all
“regressions.” Thesampleof"control"daysfortheRigobonanalysisisallTuesdaysandWednesdaysthatarenotFOMCmeeting
daysoverthesameperiodoftime.Inboththe treatmentandcontrolsamples,wedropJuly2008throughJune2009and9/11/2001-
9/21/2001. For 2Y forwards, the sample starts in January 2004. Confidence intervals for the OLS results are based on robust
standard errors. Confidence intervals for the Rigobon method are calculated using the weak-IV robust approach discussed in the
appendix with 5000 iterations.
Rigobonmethod. AccordingtoOLS,theeffectsonthe5-yearnominalandrealforwardsarehighly
statistically significant, while the Rigobon estimator indicates that these effects are far from being
significant.
This difference between OLS and the Rigobon estimator indicates that there is a large amount
of background noise in the interest rates used to construct the policy news shock over a one day
window. TheRigobonestimatorisfilteringthisbackgroundnoiseout. Thefactthattheconfidence
intervalsfortheRigobonestimatoraresowideinthe1-daywindowcaseimpliesthatthereisvery
little signal left in this case. The OLS estimator, in contrast, uses all the variation in interest rates
(both the true signal from the announcement and the background noise). Clearly, this approach
15

massivelyoverstatesthetruestatisticalprecisionoftheeffectarisingfromtheFOMCannouncement
whena1-daywindowisused.
ThedifferencebetweenOLSandtheRigobonestimatorisevenlargerwhenalonger-terminter-
estrateisusedasthepolicyindicatorthatproxiesforthesizeofmonetaryshocks. Thethirdpanel
ofTable2comparesresultsbasedonOLStothosebasedontheRigobonestimatorwhenthepolicy
indicator is the change in the two-year nominal yield over a one day window. Again, the confi-
denceintervalsaremuchwiderusingtheRigobonestimatorthanOLS.Infact,herewereport90%
confidenceintervalsfortheRigobonestimatorsincethe95%confidenceintervalsareinsomecases
infinite(i.e.,wewereunabletofindanyvalueoftheparameterofinterestthatcouldberejectedat
thatsignificancelevel).
AnimportantsubstantivedifferencearisesbetweentheOLSandRigobonestimatesinthecase
ofthe10-yearrealforwardratewhenthe2-yearnominalyieldisusedasthepolicyindicator. Here,
OLSestimationyieldsastatisticallysignificanteffectofthemonetaryshockonforwardratesateven
a 10-year horizon. This result is emphasized by Hanson and Stein (2015). However, the Rigobon
estimatorwithappropriatelyconstructedconfidenceintervalsrevealsthatthisresultisstatistically
insignificant. Our baseline estimation approach using a 30-minute window and the policy news
shock as the proxy for monetary shocks yields a point estimate that is small and statistically in-
significant.11
3.3 RiskPremiaorExpectedFutureShort-TermRates?
One question that arises when interpreting our results is to what extent the movements in long-
terminterestratesweidentifyreflectmovementsinriskpremiaasopposedtochangesinexpected
future short-term interest rates. A large literature suggests that changes in risk premia do play an
important role in driving movements in long-term interest rates in general. Yet, for our analysis,
thekeyquestionisnotwhetherriskpremiamatteringeneral,butratherhowimportanttheyarein
explainingtheabruptchangesininterestratesthatoccurinthenarrowwindowsaroundtheFOMC
11HansonandStein(2015)alsopresentanestimatorbasedoninstrumentingthe2-daychangeinthe2-yearratewith
thechangeinthetwo-yearrateduringa60-minutewindowaroundtheFOMCannouncement.Thisyieldssimilarresults
totheirbaseline.Sincethisprocedureisnotsubjecttotheconcernsraisedabove,itsuggeststhatthereareothersourcesof
differencebetweenourresultsandthoseofHansonandSteinthaneconometricissues.Onepossiblesourceofdifference
isthatweusedifferentmonetaryshockindicators. Theirpolicyindicator(thechangeinthe2-yearyield)isfurtherout
inthetermstructureandmaybemoresensitivetoriskpremia. Aswediscussinsection3.3,ourmeasureofmonetary
shocksisuncorrelatedwiththeriskpremiaimpliedbytheaffinetermstructuremodelofAbrahamsetal.(2015),whereas
HansonandStein’smonetaryshocksareassociatedwithsubstantialmovementsinriskpremia.Thedifferencecouldalso
arisefromthefactthatHansonandSteinfocusona2-daychangeinlong-termrealforwards;whichcouldyielddifferent
resultsiftheresponseoflong-termbondstomonetaryshocksisinertial.
16

announcementsthatwefocuson.12
In Appendix D, we present three sets of results that indicate that risk premium effects are not
driving our empirical results. First, the impact of our policy news shock on direct measures of
expectations from the Blue Chip Economic Indicators indicate that our monetary shocks have large
effectsonexpectedshort-termnominalandrealrates. Second,theimpactofourpolicynewsshock
on risk-neutral expected short rates from the state-of-the-art affine term structure model of Abra-
hams et al. (2015) are similar to our baseline results. Third, the impact of our policy news shock
on interest rates over longer event windows do not suggest that the effects we estimate dissipate
quickly(althoughthestandarderrorsinthisanalysisarelarge).
Wealsoconsideranalternative,market-basedmeasureofinflationexpectationsbasedoninfla-
tion swap data.13 The sample period for this analysis is limited by the availability of swaps data
tobeginonJanuary1st2005. Unfortunately,duetotheshortsampleavailabletous,theresultsare
extremely noisy, and are therefore not particularly informative. As in our baseline analysis, there
is no evidence of large negative responses in inflation to our policy news shock (as would arise
in a model with flexible prices). Indeed the estimates from this approach (which are compared to
ourbaselineresultsinTableA.4)suggestasomewhatlarger“pricepuzzle”—i.e.,positiveinflation
response—atshorterhorizons,thoughthisisstatisticallyinsignificant.
4 The Fed Information Effect
Theresultsinsection3showthatvariationinnominalinterestratescausedbymonetarypolicyan-
nouncementshavelargeandpersistenteffectsonrealinterestrates. Theconventionalinterpretation
of these facts is that they imply that prices must respond quite sluggishly to shocks. We illustrate
this in a conventional business cycle model in Appendix E. This conventional view of monetary
shocks has the following additional prediction that we can test using survey data: A surprise in-
crease in interest rates should cause expected output to fall. To test this prediction, we run our
baselineempiricalspecification—equation(1)—atamonthlyfrequencywiththemonthlychangein
12PiazzesiandSwanson(2008)showthatfederalfundsfutureshaveexcessreturnsoverthefederalfundsrateand
thattheseexcessreturnsvarycounter-cyclicallyatbusinesscyclefrequencies. However,theyarguethathighfrequency
changesinfederalfundsfuturesarelikelytobevalidmeasuresofchangesinexpectationsaboutfuturefederalfunds
ratessincetheydifferenceoutriskpremiathatvaryprimarilyatlowerfrequencies.
13An inflation swap is a financial instrument designed to help investors hedge inflation risk. As is standard for
swaps,nothingisexchangedwhenaninflationswapisfirstexecuted. However,atthematuritydateoftheswap,the
counterpartiesexchangeR t x−Π t,whereR t x isthex-yearinflationswaprateandΠ t isthereferenceinflationoverthat
period. Ifagentswereriskneutral,therefore,R t wouldbeexpectedinflationoverthexyearperiod. SeeFleckenstein,
Longstaff,andLustig(2014)forananalysisofthedifferencesbetweenbreak-eveninflationfromTIPSandinflationswaps.
17

TABLE 3
ReTsapbolnes3e: oRf eEsxppoencsteedo GfrEoxwptehc otevderO Nuetxpt uYteGarr ofowr tDhifOfevreerntt hSeamNpelxe tPYeeriaords
1995-2014 2000-2014 2000-2007 1995-2000
Policy News Shock 1.01 1.04 0.95 0.79
(0.32) (0.35) (0.32) (0.63)
Observations 120 90 52 30
WeregresschangesfromonemonthtothenextinsurveyexpectationsaboutoutputgrowthoverthenextyearfromtheBlue
Chip Economic Indicators on the policy news shock that occurs in that month (except that we drop policy news shocks that
occur in the first week of the month since we do not know whether these occurred before or after the survey response).
Specifically,thedependentvariableisthechangeintheaverageforecastedvalueofoutputgrowthoverthenextthreequarters
(themaximumhorizonoverwhichforecastsareavailableforthefullsample).SeeAppendix Ffordetails.Wepresentresults
forfoursampleperiods.Thelongestsampleperiodwehavedataforis1995m1-2014m4;thisisalsotheperiodforwhichthe
policynewsshocksisconstructed.Wealsopresentresultsfor2000m1-2014m4(whichcorrespondstothesampleperiodused
in Table 1), 2000m1-2007m12 (a pre-crisis sample period), and 1995m1-1999m12. As in our other analysis, we drop data
from July 2008 through June 2009. Robust standard errors are in parentheses.
BlueChipsurveyexpectationsaboutoutputgrowthasthedependentvariableandthepolicynews
shockthatoccursinthatmonthastheindependentvariable.14
Table 3 reports the resulting estimates. The dependent variable is the monthly change in ex-
pected output growth over the next year (see Appendix F for details). In sharp contrast to the
conventional theory of monetary shocks, policy news shocks that raise interest rates lead expecta-
tionsaboutoutputgrowthtoriseratherthanfall.15 Wepresentresultsforfoursampleperiods. The
longestsampleperiodforwhichweareabletoconstructourpolicynewshockis1995-2014. Wealso
presentresultsforthesampleperiod2000-2014,whichcorrespondstothesampleperiodweusein
mostofourotheranalysis. Forrobustness,wealsopresentresultsfortwoshortersamplerperiods
(1995-2000and2000-2007). Theresultsaresimilaracrossallfoursampleperiods,butofcourseless
preciselyestimatedfortheshortersamplerperiods.
Figure 2 presents a binned scatter plot of the relationship between changes expected output
growth and our policy news shock over the 1995-2014 sample period. This scatter plot shows that
the results in Table 3 are not driven by outliers. Finally, Table A.5 presents the response of output
growth expectations separately for each quarter that the Blue Chip survey asks about. These are
noisierbutpaintthesamepictureastheresultsinTable3.
AnaturalinterpretationofthisevidenceisthatFOMCannouncementsleadtheprivatesectorto
updateitsbeliefsnotonlyaboutthefuturepathofmonetarypolicy,butalsoaboutothereconomic
14Weexcludepolicynewsshocksthatoccurinthefirstweekofthemonthbecauseinthosecaseswedonotknow
whethertheyoccurredbeforeorafterthesurveyresponse.
15Campbell et al. (2012) present similar evidence regarding the effect of surprise monetary shocks on Blue Chip
expectationsaboutunemployment.
18

Figure2: BinnedScatterPlotforExpectedOutputGrowthRegression
0.20
0.15
0.10
0.05
0.00
‐0.05
‐0.10
‐0.15
‐0.20
‐0.25
‐0.10 ‐0.06 ‐0.02 0.02 0.06 0.10
Policy News Shock
fundamentals. Forexample,whenanFOMCannouncementsignalshigherinterestratesthanmar-
kets had been expecting, market participants may view this as implying that the FOMC is more
optimisticabouteconomicfundamentalsgoingforwardthantheyhadthought,whichinturnmay
leadthemarketparticipantsthemselvestoupdatetheirownbeliefsaboutthestateoftheeconomy.
We refer to effects of FOMC announcements on private sector views of non-monetary economic
fundamentalsas“Fedinformationeffects.”
TheideathattheFedcanhavesuchinformationeffectsreliesonthenotionthattheFOMChas
some knowledge regarding the economy that the private sector doesn’t have or has formulated a
viewpointabouttheeconomythattheprivatesectorfindsvaluable. Isitreasonabletosupposethat
thisisthecase? Intermsofactualdata,theFOMChasaccesstothesameinformationastheprivate
sector with minor exceptions.16 However, the Fed does employ a legion of talented, well-trained
economists whose primary role is to process and interpret all the information being released about
theeconomy. ThismayimplythattheFOMC’sviewabouthowtheeconomywillevolvecontainsa
perspectivethataffectstheviewsofprivateagents. ThisistheviewRomerandRomer(2000)argue
16TheFOMCmayhavesomeadvanceknowledgeofindustrialproductiondatasincetheFederalReserveproduces
thesedata. Italsocollectsanecdotalinformationoncurrenteconomicconditionsfromreportssubmittedbybankdirec-
torsandthroughinterviewswithbusinesscontacts,economists,andmarketexperts. Thisinformationissubsequently
publishedinreportscommonlyknownastheBeigeBook.
19

forintheirclassicpaperonFederalReserveinformation.17
The idea that the Fed can influence private sector beliefs through its analysis of public data is
somewhat unconventional in macroeconomics. However, the finance literature on analyst effects
suggests this is not implausible. This literature finds that the most influential analyst announce-
mentscanhavequitelargeeffectsonthestockmarket(see,e.g.LohandStulz,2011). LohandStulz
note: “Kenneth Bruce from Merrill Lynch issued a recommendation downgrade on Countrywide
FinancialonAugust15,2007,questioningthegiantmortgagelendersabilitytocopewithaworsen-
ingcreditcrunch. Thereportsparkedasell-offinCountrywidesshares,whichfell13%onthatday.”
If Kenneth Bruce can affect the market’s views about Countrywide, perhaps it is not unreasonable
tobelievethattheFedcanaffectthemarket’sviewsaboutwheretheeconomyisheaded.
If Fed information is important, one might expect that contractionary monetary shocks would
disproportionatelyoccurwhentheFedismoreoptimisticthantheprivatesectoraboutthestateof
the economy. In Appendix G, we test this proposition using the Fed’s Greenbook forecast about
outputgrowthasameasureofitsoptimismabouttheeconomy.18 Wefindthat,indeed,ourpolicy
newsshockstendtobepositive(i.e.,indicateasurpriseincreaseininterestrates)whentheGreen-
book forecast about current and future real GDP growth is higher than the corresponding Blue
Chip forecast (panel A of Table G.1). We furthermore find that the difference between Greenbook
andBlueChipforecaststendstonarrowafterourpolicynewsshocksoccur(panelBofTableG.1).
This suggests that private sector forecasters may update their forecasts based on information they
gleamfromFOMCannouncements.
5 Characterizing Monetary Non-Neutrality with Fed Information
Theevidencewepresentinsection4callsformoresophisticatedmodelingoftheeffectsofmonetary
announcements than is standard in the literature. Rather than affecting beliefs only about current
and future monetary policy, FOMC announcements must also affect private sector beliefs about
othereconomicfundamentals.
An important consequence of this is that our evidence does not necessarily point to nominal
and real rigidities being large. It may be that the responses of real interest rates that we estimate
17ThisdoesnotnecessarilyimplythattheFedshouldbeabletoforecastthefutureevolutionoftheeconomybetter
thantheprivatesector. Theprivatesector, ofcourse, alsoprocessesandinterpretstheinformationreleasedaboutthe
economy. It may therefore also be able to formulate a view about the economy that the Fed finds valuable. In other
words,informationcanflowbothwayswithneithertheFednortheprivatesectorhavingaclearadvantage.
18TheGreenbookforecastisaninternalforecastproducedbythestaffoftheBoardofGovernorsandpresentedateach
FOMCmeeting.Greenbookforecastsaremadepublicwithafiveyearlag.
20

in response to FOMC announcements mostly reflect changes in private sector expectations about
the natural rate of interest. If this is the case, the fact that we find that our shocks have little effect
on inflationary expectations may be consistent with small nominal and real rigidities, since the
tighteningofpolicyrelativetothenaturalrateissmall.19
But even if this is true—that the responses of real interest rates that we estimate mostly reflect
changes in private sector expectations about the natural rate of interest—this does not imply that
the Fed is powerless. Quite to the contrary, in this case, the Fed has enormous power over beliefs
abouteconomicfundamentals,whichmayinturnhavelargeeffectsoneconomicactivity.
Our evidence on the response of real interest rates and expected inflation to a monetary an-
nouncement, therefore, implies that either 1) nominal and real rigidities are large, or 2) the Fed
can affect private sector beliefs about future non-monetary fundamentals by large amounts. In
otherwords,itimpliesthattheFedispowerful,eitherthroughtheconventionalchanneloranon-
conventionalchannel(orsomecombination).
To make these arguments precise, we now present a New Keynesian model of the economy
augmented with Fed information effects. We then estimate this model to match the responses of
interestrates,expectedinflation,andexpectedoutputgrowthtoFOMCannouncementscalculated
above. Finally,weusetheestimatedmodeltoassessthedegreeofmonetarynon-neutralityimplied
by our evidence and to assess how much of this monetary non-neutrality arises from traditional
channelsversusinformationeffects.
5.1 ANewModelwithFedInformationEffects
Mostearliertheoreticalworkonthesignalingeffectofmonetarypolicyhasmadetheveryrestrictive
assumptionthattheFedcanonlysignalthroughitsactions. Thefocusofmuchofthisliteraturehas
been on the limitations of what the Fed can signal with its actions. The recent empirical literature
onmonetarypolicyhas,however,convincinglydemonstratedthattheFedalsosignalsthroughits
statements(Gurkaynak,Sack,andSwanson,2005). ThisimpliesthattheFed’ssignalscanbemuch
richer;theycanincorporateforwardguidance,andtheycandistinguishbetweendifferenttypesof
shocks. With a much richer signal structure, the key question becomes: What information would
theFedliketoconvey?
WemodelFOMCannouncementsasaffectingprivatesectorbeliefsaboutthepathofthe“natu-
ralrateofinterest,”therealinterestratethatwouldprevailabsentpricingfrictions. Thisisanatural
19ThisideaisexplainedinmoredetailbelowandinAppendixE.
21

choicesincetrackingthenaturalrateisoptimalinthemodelweconsiderabsentinformationeffects.
If the Fed’s goal is to track the natural rate of interest, it seems natural that announcements by the
Fed about its current and future actions provide information about the future path of the natural
rateofinterest.
Apart from including a Fed information effect, the model we use differs in two ways from the
textbook New Keynesian model: households have internal habits, and we allow for a backward-
looking term in the Phillips curve. These two features allow the model to better fit the shapes of
the impulse responses we have estimated in the data. Detailed derivations of household and firm
behavior in this model are presented in Appendix H. There, we show that private sector behavior
in this model can be described by a log-linearized consumption Euler equation and Phillips curve
thattakethefollowingform:
λˆ = E λˆ +(ˆı −E πˆ −rˆn), (2)
xt t xt+1 t t t+1 t
∆πˆ = βE ∆πˆ +κωζ˜xˆ −κζ˜λˆ . (3)
t t t+1 t xt
Hatted variables denote percentage deviations from steady state. ∆πˆ = πˆ − πˆ . The variable
t t t−1
λˆ = λˆ − λˆn denotes the marginal utility gap (the difference between actual marginal utility of
xt t t
consumption
λˆ
and the “natural” level of marginal utility
λˆn
that would prevail if prices were
t t
flexible), xˆ = yˆ − yˆn denotes the “output gap”, πˆ denotes inflation, ˆı denotes the gross return
t t t t
on a one-period, risk-free, nominal bond, and rˆn denotes the “natural rate of interest,” which is a
t
functionofexogenousshockstotechnology. Theparameterβdenotesthesubjectivediscountfactor
of households, while κ, ω, and ζ˜ are composite parameters that determine the degree of nominal
andrealrigiditiesintheeconomy. Withinternalhabits,themarginalutilitygapis
λˆ = −(1+b2β)σ xˆ +bσ xˆ +bβσ E xˆ , (4)
xt c t c t−1 c t t+1
wherebgovernsthestrengthofhabitsandσ = −σ−1/((1−b)(1−bβ)),whereσistheintertemporal
c
elasticityofsubstitution.
Weassumethatthemonetaryauthoritysetsinterestratesaccordingtothefollowingsimplerule:
ˆı −E πˆ = r¯ +φ πˆ , (5)
t t t+1 t π t
22

withr¯ followinganAR(2)process
t
r¯ = (ρ +ρ )r¯ −ρ ρ r¯ +(cid:15) , (6)
t 1 2 t−1 1 2 t−2 t
whereρ andρ aretherootsofthelagpolynomialforr¯ and(cid:15) istheinnovationtother¯ process.
1 2 t t t
Here(cid:15) isthemonetaryshock. Noticethatitcanpotentiallyhavealong-lastingeffectonrealinterest
t
ratesthroughtheAR(2)processforr¯. Wechoosethisspecificationtobeabletomatchtheeffectsof
t
the monetary shocks we estimate in the data. The shocks we estimate in the data have a relatively
smalleffectoncontemporaneousinterestratesbutamuchlargereffectonfutureinterestrates(see
Table1)—i.e.,theyaremostlybutnotexclusivelyforwardguidanceshocks. TheAR(2)specification
forr¯ cancapturethisifρ andρ arebothlargeandpositiveleadingtoapronouncedhump-shape
t 1 2
intheimpulseresponseofr¯ (andthereforeapronouncedhump-shapeacrossthetermstructurein
t
thecontemporaneousresponseoflonger-terminterestratesasinTable1).20
As we discuss above, the way in which we model the Fed information effect is by assuming
thatFOMCannouncementsmayaffecttheprivatesector’sbeliefsaboutthepathofthenaturalrate
of interest. The simplest way to do this is to assume that private sector beliefs about the path of
the natural rate of interest shifts by some fraction ψ of the change in r¯. Formally, in response to a
t
monetaryannouncement
E rˆn = ψE r¯ . (7)
t t+j t t+j
Moreover, we assume that the shock to expectations about the current value of the natural rate of
outputisproportionaltotheshocktoexpectationsaboutthecurrentmonetarypolicywiththesame
factorofproportionality,i.e.,E yˆn = ψE r¯.21
t t t t
Heretheparameterψ governstheextenttowhichmonetaryannouncementshaveinformation
effectsversustraditionaleffects. Afractionψ oftheshockshowsupasaninformationeffect,while
afraction1−ψshowsupasatraditionalgapbetweenthepathforrealinterestratesandthe(private
sector’sbeliefsabout)thepathforthenaturalrateofinterest.22
20How should the monetary shocks (cid:15) t be interpreted? A natural interpretation is the following: The Fed seeks to
targetthenaturalrateofinterest. WhentheFedmakesanannouncement,itseekstocommunicatechangesinitsbeliefs
aboutthepathofthenaturalratetothepublic. Thechangesinbeliefssometimessurprisethepublicandthereforelead
toashock.
21HereweassumethattheFOMCmeetingoccursatthebeginningoftheperiod,beforethevalueofyˆn isrevealed
t
to the agents. In reality, uncertainty persists about output in period t until well after period t, due to heterogeneous
information.Weabstractfromthis.
22Thiswayofmodelingtheinformationeffecthasthecrucialadvantagethatitissimpleandparsimoniousenoughto
allowustoaccountfortheeffectsofFOMCannouncementsontheentirepathoffutureinterestrateexpectations—i.e.,
theroleofforwardguidance. Thisisadistinguishingfeatureversuspreviouswork. EllingsenandSoderstrom(2001)
presentamodelinwhichthesignalingeffectderivesfromannouncementsaboutthecurrentinterestrate.
23

5.2 EstimationMethod
We estimate four key parameters of the model using simulated method of moments. The four
parametersweestimatearethetwoautoregressiverootsoftheshockprocess(ρ andρ ),theinfor-
1 2
mation parameter (ψ) and the “slope of the Phillips curve” (κζˆ ). We fix the remaining parameters
at the following values: We choose a conventional value of β = 0.99 for the subjective discount
factor. Ourbaselinevaluefortheintertemporalelasticityofsubstitutionisσ = 0.5,butweexplore
robustnesstothischoice. WefixtheTaylorruleparametertoφ = 0.01. Thisisroughlyequivalent
π
toavalueof1.01forthemoreconventionalTaylorrulespecificationwithouttheE πˆ termonthe
t t+1
left-hand-sideofequation(5). Wechoosethisvaluetoensurethatthemodelhasauniquebounded
equilibrium but at the same time limit the amount of endogenous feedback from the policy rule.
Thishelpsensurethattheresponseoftherealinterestratediesoutwithin10yearsasweestimate
inthedata.23 Wesettheelasticityofmarginalcostwithrespecttoownoutputtoω = 2. Thisvalue
resultsfromaFrischlaborsupplyelasticityofoneandalaborshareof2/3. Finally,wesetthehabit
parametertob = 0.9,avalueveryclosetotheoneestimatedbySchmitt-Grohe´ andUribe(2012).
To ease the computational burden of the simulated method of moments estimation we use a
two stage iterative procedure. In the first stage, we estimate the two autoregressive roots of the
monetary shock process (ρ and ρ ) to fit the hump-shaped response of real interest rates to our
1 2
policy news shock. We do this for fixed values of the information parameter and the slope of the
Phillipscurve. Themomentsweuseinthissteparetheresponsesof2,3,5,and10yearrealyields
andforwardsreportedinTable1. Inthesecondstep,weestimatetheinformationparameter(ψ)and
the slope of the Phillips curve
(κζˆ
) for fixed values of the two autoregressive roots. The moments
we use in this step are the responses of 2, 3, 5, and 10 year break-even inflation (both yields and
forwards) reported in Table 1 as well as the responses of output growth expectations reported in
TableA.5. Wetheniteratebackandforthbetweenthesestepsuntilconvergence.
In both steps, we use a loss function that is quadratic in the difference between the moments
discussedaboveandtheirtheoreticalcounterpartsinthemodel.24 Weuseaweightingmatrixwith
the inverse standard deviations of the moments on the diagonal, and with the off-diagonal values
set to zero. We use a bootstrap procedure to estimate standard errors. Our bootstrap procedure is
23Recent work has shown that standard New Keynesian models such as the one we are using are very sensitive
tointerestratemovementsinthefarfuture(Carlstrom, Fuerst, andPaustian,2015;McKay, Nakamura, andSteinsson,
2016).
24Thetheoreticalcounterpartsaretheresponsesofthecorrespondingvariabletoamonetaryshockinthemodel.Since
themagnitudeoftheshockinoursimulationsisarbitrary,wemakesuretorescaleallresponsesfromthemodelinsucha
waythatthe3Yrealforwardrateisperfectlymatched.WeusethemethodsandcomputercodedescribedinSims(2001)
tocalculatetheequilibriumofourmodel.
24

to re-sample the data with replacement, estimate the empirical moments on the re-sampled data,
and then estimate the structural parameters as described above using a loss function based on the
estimated empirical moments for the re-sampled data.25 We repeat this procedure 1000 times and
reportthe2.5%and97.5%quantilesofthestatisticsofinterest. Importantly,thisprocedureforcon-
structingtheconfidenceintervalscapturesthestatisticaluncertaintyassociatedwithourempirical
estimatesinTables1andA.5.
5.3 ResultsandIntuition
Our primary interest is to assess the extent to which FOMC announcements contain Fed informa-
tion and how this affects inference about other key aspects of the economy such as the slope of
the Phillips curve. Table 4 presents our parameter estimates, while Figures 3-5 illustrate the fit of
the model. As in the data, the estimated model generates a persistent, hump-shaped response of
nominalandrealinterestrateswithasmallanddelayedeffectonexpectedinflation(seeFigure3).
Togeneratethistypeofresponse,weestimatethatbothoftheautoregressiverootsofthemonetary
shockprocessarelargeandpositive,andweestimateasmallslopeofthePhillipscurve.
Wealsoestimatethatthemonetaryshockleadstoapronouncedincreaseinexpectationsabout
output growth as in the data (see Figure 4). The model can match the increase in expected growth
followingasurpriseincreaseininterestratesbyestimatingalargeinformationeffect. Weestimate
that roughly 2/3 of the monetary shock is a shock to beliefs about future natural rates of interest
(seeFigure5).
AsFigure4illustrates,ourmonetaryshocksimultaneouslyleadstoanincreaseinexpectations
aboutoutputgrowthandadecreaseinoutputrelativetothenaturalrateofoutput(i.e.,adecrease
in the output gap). This is a consequence of the fact that the information effect is large but still
substantially smaller than the overall increase in interest rates. Output growth expectations rise
because the monetary shock is interpreted as good news about fundamentals. But since the Fed
increases interest rates by more than the private sector believes the natural rate of interest rose,
privatesectorexpectationsabouttheoutputgapfall.
Despite estimating a large information effect, we estimate a very flat Phillips curve. This is
consistent with prior empirical work. Mavroeidis, Plagborg-Moller, and Stock (2014) survey the
25There-samplingprocedureisstratifiedsincetheempiricalmomentsareestimatedfromdifferentdatasetanddif-
ferentsampleperiods. Thestratificationmakessurethateachre-sampleddatasetisconsistentwiththeoriginaldataset
alongthefollowingdimensions:Thenumberofobservationsfortheyieldsandforwardsbeforeandafter2004isthesame
asintheoriginaldataset(sincethesampleperiodforthe2Yand3Yyieldsandforwardsstartsin2004). Thenumberof
BlueChipobservationsthatdonotreport4-to7-quartersaheadexpectedGDPgrowtharethesameasintheoriginal
dataset,sinceBlueChiponlyasksforecasterstoforecastthecurrentandnextcalendaryear.
25

TABLE 4
TableE4s:tEimstaitmesa otef sSotrfuScttururaclt uPararalmPeatrearms eters
 x 



Baseline 0.68 11.2 0.9 0.79
[0.33, 0.84] [0.0, 60.2] [0.83, 0.96] [-0.69, 0.89]
No Information 0.00 3.4 0.9 0.79
(= 0) -- [0.0, 24.1] [0.83, 0.96] [-0.69, 0.89]
Full Information 0.99 563 0.9 0.79
(= 0.99) -- [0, 12538] [0.82, 0.96] [-0.67, 0.89]
Lower IES 0.67 13.7 0.9 0.79
( = 0.25) [0.25, 0.89] [0.0, 94.6] [0.83, 0.96] [-0.69, 0.89]
Higher IES 0.68 8.2 0.9 0.79
( = 1) [0.42, 0.81] [0.0, 44.0] [0.83, 0.96] [-0.69, 0.89]
No Habits 1 1000 0.9 0.79
(b = 0) [0.92, 1.00] [0, 43236] [0.83, 0.96] [-0.69, 0.89]
The table reports our estimates of the structural parameters of the model that we estimate. We report 95%
confidence intervals in square brackets below the point estimate for each parameter. These are based on the
bootstrap procedure described in the text. In the No Informationcase and theFull Informationcase, theslope
of the Phillips curve is estimated only off of inflation moments. In the other cases, the slope of the Phillips
curve and the information parameter are estimated off of both inflation and GDP growth moments.
Figure3: ResponsesofNominalandRealRatesandInflationtoaContractionaryShock
0.7
Real Interest Rate
0.6
Nominal Interest Rate
Inflation
0.5
0.4
0.3
0.2
0.1
0.0
‐0.1
‐0.2
0 4 8 12 16 20 24 28 32 36 40
Quarters
26

Figure4: ResponsesofExpectedOutputGrowthandOutputGaptoaContractionaryShock
0.8
Output Growth
0.6 Output Gap
0.4
0.2
0.0
‐0.2
‐0.4
‐0.6
‐0.8
0 4 8 12 16 20 24 28 32 36 40
Quarters
Figure5: DecompositionofRealRateinInterestRateGapandNaturalInterestRate
0.7
Natural Interest Rate
0.6 Real Interest Rate
0.5
0.4
0.3
0.2
0.1
0.0
0 4 8 12 16 20 24 28 32 36 40
Quarters
27

literaturethathasestimatedPhillipscurvesand,usingacommondataset,runahugenumberofa
priorireasonablespecificationswhichspandifferentchoicesmadeinthisliterature. Theyfindthat
theestimatedvaluesoftheslopeofthePhillipscurvevariessubstantiallyacrossspecificationsand
aresymmetricallydispersedaroundavalueofzero. OnereasonwhyourestimatedPhillipscurve
is very flat is that the shocks that we estimate are substantially more persistent than most other
identified monetary policy shocks (e.g., Christiano, Eichenbaum, and Evans, 2005). This means
that our shocks imply forward guidance about interest rates quite far in the future. It has recently
been shown that standard New Keynesian models implies that far future forward guidance has
large effects on current outcomes (Carlstrom, Fuerst, and Paustian, 2015; McKay, Nakamura, and
Steinsson,2016).
To illustrate how allowing for the information effect affects our estimates, we reestimate the
model setting the information effect to zero. In this case, we remove the expected output growth
momentsfromtheobjectivefunctionoftheestimationsincethesemomentsareimpossibletomatch
without an information effect. The second row in Table 4 presents the estimates for this case. We
see that ignoring the information effect yields a substantially flatter Phillips curve—implying a
substantialoverestimateofnominalandrealrigidities—relativetoourbaselineestimation. Wealso
reportacasewheretheinformationeffectissettoavalueclosetoone. Inthiscase,theslopeofthe
Phillipscurveisestimatedtobemuchsteeperthaninourbaselinecase.
Clearly,theinformationeffecthasanimportanteffectoninferenceabouttheslopeofthePhillips
curve. This arises because the effect of the monetary shock on the interest rate gap—the gap be-
tweentheinterestrateandthenaturalrateofinterest—ismuchsmallerwhentheinformationeffect
is estimated to be large than it is when the information effect is estimated to be small. It is the
responseoftheinterestrategapasopposedtotheresponseoftherealinterestrateitselfthatdeter-
mines the response of inflation (see equation (19) in Appendix E). The intuition is that, when the
Fedraisesrates,peopleperceivethisasgoodnewsabouteconomicfundamentals,andthiscounters
theconventionalchannelofmonetarypolicywherebyaninterestratehikelowersoutput.
Table4alsoreportsalternativeestimateswherewevarythevalueoftheintertemporalelasticity
of substitution (IES) and the habit formation parameter. Varying the IES does not affect our esti-
matesmuch. Thismayseemsurprising. AsmallervalueoftheIESimpliesthatlargermovements
inthenaturalrateofinterestareneededtomatchthemovementsinexpectedgrowthratesobserved
inthedata. ThiswouldsuggestthatalowervalueoftheIESwouldyieldalargervalueoftheinfor-
mationeffect. However,inourmodelwithsubstantialhabitformationtheIESandtheinformation
parametersalsoaffecttheshapeoftheresponseofoutputgrowth. Theseeffectsimplythatsimilar
28

Figure6: ResponseofActualandNaturalExpectedOutput
5.0
Output
4.0 Natural Output
Output Gap
3.0
2.0
1.0
0.0
‐1.0
0 4 8 12 16 20 24 28 32 36 40
Quarters
valuesoftheinformationparameterareestimatedforawiderangeofvaluesoftheIES.Incontrast,
when we set the habit parameter to zero, we estimate that the entire change in interest rates is an
informationeffect. Asaconsequence,wealsoestimateamuchsteeperPhillipscurve. However,the
fitofthemodeltotheoutputgrowthmomentsismuchworsewithouthabitformation.
6 The Causal Effect of Monetary Shocks
Thelargeinformationeffectweestimateinsection5fundamentallychangeshowweshouldinter-
pret the response of output and inflation to monetary policy announcements. Figure 6 plots the
response of private sector beliefs about output, the natural rate of output, and the output gap to
a monetary shock that increases interest rates in our estimated model from section 5. The figure
shows that this surprise monetary tightening leads to a large and permanent increase in expected
output.
How can this be? Can monetary policy really have such huge effects on output 10 years in the
future? Isn’t monetary policy neutral in the long run? Shouldn’t a monetary tightening decrease
output? Here it is crucial to recognize that the information the Fed reveals about economic funda-
mentals is in large part (perhaps mostly) information that the private sector would have learned
about eventually through other channels in the absence of the Fed’s announcement. This intro-
29

duces an important subtlety into the assessment of the effect of monetary policy that has, to our
knowledge,notbeendiscussedintheexistingliterature. Tocorrectlyassessthecausaleffectofmon-
etarypolicyonoutput,weneedtocompareversusareasonablecounterfactualthataccountsforthe
fact that the changes in fundamentals that the Fed’s announcement reveals would have occurred
even in the absence of the announcement. In other words, we want a counterfactual in which
the path of productivity—the exogenous fundamental we assume the Fed provides information
about—followsthesamepathasintheactualresponse.
To construct this counterfactual, we must take a stand on when the private sector would have
learnedaboutthechangesinfundamentalsrevealedbytheFedintheabsenceoftheFedannounce-
ment. We choose a particularly simple counterfactual. In this counterfactual, the private sector
learns about changes in productivity when they occur and it believes that productivity follows a
random walk. To be clear, this counterfactual represents our assumption about what would have
happened regarding private sector beliefs about economic fundamentals in the absence of the Fed
announcement. Onecouldconsiderothercounterfactuals. Wedon’thaveanydatatopreciselypin
downthecounterfactual. Butwethinkthatourchosencounterfactualisreasonableanditservesthe
purposeofillustratingthemainissuethatoneneedstouseacounterfactualinwhichthechangesin
economic fundamentals that the Fed provides information about would occur even in the absence
oftheFedannouncement.
Wemustalsomakeanassumptionabouthowmonetarypolicyreactstochangesinthenatural
rateofinterestinthecounterfactual. InkeepingwiththegeneralassumptionthattheFedseeksto
trackthenaturalrateofinterest,weassumethatmonetarypolicyvariestheinterestratetotrackthe
naturalrateofinterestinthecounterfactual.
Figure 7 presents actual and counterfactual output growth constructed in this way. The figure
reveals that most of the increase in output would have occurred anyway in the absence of the Fed
announcement. Giventhisnewcounterfactual,the“causaleffect”oftheFedonoutputgrowth—the
difference between what happens following the monetary shock, and what would have happened
asrepresentedbythecounterfactual—nolongerlookssoimplausible. Thisdifferenceismuchmore
modestthantheoverallchangeinbeliefsaboutthepathofoutput(whichincludestheeffectsofthe
productivityshockstheFedisinformingthepublicabout).
Figure 8 plots this measure of the causal effect of monetary shocks on output. The figure also
decomposesitintotwocomponents: theeffectontheoutputgap(whichfalls)andtheeffectonthe
natural rate of output (which rises). The effect on the output gap is the the conventional channel
of monetary policy: an interest rate increase relative to the natural rate of interest leads to a drop
30

Figure7: ResponseofActualandCounterfactualExpectedOutput
4.5
4.0
3.5
3.0
2.5
2.0
1.5
1.0
Actual Output
0.5
Counterfactual Output
0.0
0 4 8 12 16 20 24 28 32 36 40
Quarters
in output relative to the natural rate of output. The second component is a novel effect of Fed
information.
A positive shock to beliefs about economic fundamentals—which leads the future path of the
natural rate of interest to rise—has a positive causal effect on output even relative to the counter-
factual described above. Why is this? This effect arises because of the dynamic linkages in our
model. Inourmodelhabitformationbyhouseholdsisimportantandhouseholdsunderstandthis.
Whenconsumersexpectconsumptiontobehighinthefuture,theywanttoconsumemoretodayto
builduptheirhabit. Thisimpliesthatpositivenewsaboutthefutureraisesconsumptionandoutput
today. Other dynamic linkages would yield similar effects of Fed information. For example, in a
modelwithcapitalaccumulation,newsabouthighfutureproductivitywouldcauseanincreasein
investmentuponannouncementandtherebyaffectcurrentoutput.
6.1 PolicyImplications
The findings discussed above have important policy implications. The fact that the information
effect of surprise Fed tightenings stimulates output implies that the Fed is “fighting against itself”
whenitsurprisesmarkets. Figure8showsthatforourestimatedparameterstheoveralleffectofthe
twochannelsisforaninterestrateincreasetoraiseoutput—theoppositefromtheconventionalview
31

Figure8: CausalEffectofMonetaryShocksonExpectedOutput
0.8
0.6
0.4
0.2
0.0
‐0.2
‐0.4
Output
Natural Output
‐0.6
Output Gap
‐0.8
0 4 8 12 16 20 24 28 32 36 40
Quarters
Figure9: ExpectedOutputGrowthwithandwithouttheInformationEffect
1.0
0.5
0.0
‐0.5
‐1.0
‐1.5 No information effect
With information effect
‐2.0
0 4 8 12 16 20 24 28 32 36 40
Quarters
32

of how monetary policy works.26 If the Fed would like to stimulate economic activity, a surprise
policyeasingmaybecounter-productivebecausetheincreaseinpessimismthatitcausesitselfpulls
theeconomyfurtherdown.
This raises the question: Should the Fed withhold releasing bad news about the economy to
avoid the increased pessimism this information would cause? A full analysis of this question is
beyond the scope of this paper. But we would like to note two reasons why it may not be the case
thattheFedshouldwithholdbadnews. First,anattemptbytheFedtosystematicallybiasitssignals
is likely to be ineffective since the private sector will learn how to interpret what the Fed says and
adjust for the bias. Second, advance knowledge about changes in fundamentals allows agents to
prepare gradually for these changes, which is likely to improve welfare. A possible exception to
thisintuitionisacircumstancewhentheFedisnotabletorespondtotheinformationitisrevealing
by tracking the updated natural rate, e.g., when interest rates are at the zero-lower-bound. In that
case,itmaybeoptimalfortheFedtowithholdinformation.
The information effect also implies that there is an important distinction between interest rate
changes associated with the monetary policy rule and deviations from this rule. The systematic
response of monetary policy to public information—by definition—does not have information ef-
fects associated with it and therefore will not lead to the “perverse” effects on output discussed
above. Figure 9 contrasts the consequences of an unexpected monetary shock with its associated
informationeffectandtheeffectsofasimilarlysizedchangeininterestratesthatcomesaboutdue
tothesystematiccomponentofmonetarypolicyandthereforedoesnothaveaninformationeffect
associated with it.27 The contrast is stark. Since our estimates imply considerable nominal and
real rigidities, increases in interest rates associated with the monetary policy rule reduce output
substantially.
Thisanalysismakesclearthattheinformationcontentofamonetaryshockmattersindetermin-
ingitseffects. MostofwhattheFeddoesisanticipatedbymarketsexactlybecauseitdependsina
systematicwayonpublicinformation. Theeffectsofthissystematiccomponentofmonetarypolicy
are likely to be more conventionally Keynesian than the effects of monetary surprises that contain
significant information effects and are therefore a mix of the response to a conventional monetary
26RecallthatthisresultisnotsimplyanimplicationofthefactthattheFed’sannouncementisgoodnewsthatraises
outputexpectation.Wearesubtractingthecounterfactual.Theeffectwearetalkingabouthereistheeffectthatlearning
thegoodnewsearlierhasonthepathofoutput.
27Itisimportanttounderstandthatourempiricalresultscanbeusedtothinkaboutboththeeffectsofmonetarypolicy
shocksandchangesininterestratesthatcomeaboutduetothesystematiccomponentofpolicy.Inthelinearmodelswe
use,itdoesnotmatterwhyinterestrateschange(exceptfortheinformationeffect).Inotherwords,thecomparativestatic
ofagivenchangeininterestratesonothervariablesisthesameirrespectiveofthereasonfortheinterestratechange
(exceptfortheinformationeffect).
33

TABLE 5
TableR5e:sRpoensspeo onfs eStoofckS tPorcikcePsrices
Stock Prices
Response in the Data -6.5
(3.9)
Response in the Model
Baseline -6.8
[-11.5, -1.6]
No Fed Information Effect -11.1
[-19.4, -2.5]
shock and the response to the non-monetary news contained in the Fed surprise.28 The effects of
monetary surprises will also vary depending on the amount and nature of the information they
convey. InthecaseoftheVolckerdisinflation,forexample,thenarrativeevidencesuggeststhatfew
observersinterpretedVolckersdecisiontoraiseinterestratesasreflectinganoptimisticviewofthe
economicoutlook. TotheextentthattheVolckertighteningwasbroadlyinterpretedasreflectinga
different loss-function, or a greater degree of conservatism in dealing with inflation, then this too
wouldhaveasmallinformationeffect. Whilewedonotallowforanyheterogeneityofthisnature
inourmodel,thisstrikesusasaninterestingavenueforfutureresearch.
6.2 StockPriceEffects
Wefinishthepaperwithoneadditionalpieceofevidencethatshedslightontheinformationcontent
ofFOMCannouncements. Table5presentstheresponseofstockpricestoFOMCannouncements.
Apuretighteningofmonetarypolicyleadsstockpricestofallfortworeasons: higherdiscountrates
andloweroutput. However,goodnewsaboutfuturefundamentalscanraisestockprices(ifhigher
futurecash-flowsoutweighhigherfuturediscountrates). Inthedata,weestimatethattheS&P500
index falls by 6.5% in response to a policy news shock that raises the 2-year nominal forward by
1%.29 Thisestimateisrathernoisy,withastandarderrorof3.3%.
Table5alsopresentstheresponseofstockpricestoourmonetarypolicyshockinourestimated
model.30 In the calibration of our model where monetary policy announcements convey informa-
tionaboutbothfuturemonetarypolicyandfutureexogenouseconomicfundamentals,stockprices
28This distinction is analogous to the local average treatment effect versus average treatment effect distinction in
appliedmicroeconomics.
29EarlierworkbyBernankeandKuttner(2005)andRigobonandSack(2004)findslargeresponsesofthestockmarket
tosurprisemovementsinthefederalfundsrate.
30Forsimplicity,wemodelstocksasanunleveredclaimtotheconsumptionstreamintheeconomyasiscommonin
theassetpricingliterature.
34

fall by 6.8% in response to the FOMC announcement. In contrast, if monetary policy is assumed
not to convey information about future exogenous fundamentals, stock prices fall by 11%. The re-
sponseofstockpricesinthedataisthusanotherindicatorthatfavorstheviewthatmonetarypolicy
conveysinformationtothepublicaboutfutureexogenousfundamentals.
7 Conclusion
We use a high-frequency identification approach to estimate the causal effect of monetary shocks.
The monetary shocks that we identify have large and persistent effects on real interest rates. Real
rates move essentially one-for-one with nominal rates several years into the term structure. Con-
tractionarymonetaryshocksleadtonosignificanteffectoninflationintheshort-runandtheeffect
becomes significantly negative only several years into the term structure. However, in sharp con-
trast with the implications of standard monetary models, contractionary shocks raise expectations
aboutoutputgrowth.
Weinterprettheincreaseinexpectedoutputgrowthafteramonetarytighteningasevidenceofa
Fed“informationeffect.” WhentheFedraisesinterestrates,thisleadstoincreasedoptimismabout
economic fundamentals. We develop a model of this Fed information effect, in which the private
sectorinterpretspartofanunexpectedincreaseintheinterestrateasinformationaboutthenatural
rate. Weestimatethemodelandfindstrongevidenceforbothchannels: theconventionalmonetary
policy channel and the information effect. One implication of our analysis is that the information
contentofamonetaryshockmattersindeterminingitscausaleffects.
35

A Construction of the Policy News Shock
Thepolicynewsshockisconstructedasthefirstprinciplecomponentofthechangeinfiveinterest
rates. The first of these is the change in market expectations of the federal funds rate over the
remainder of the month in which the FOMC meeting occurs. To construct this variable we use
dataonthepriceofthefederalfundsfuturescontractforthemonthinquestion. Thefederalfunds
futurescontractforaparticularmonth(sayApril2004)tradesatpricepandpaysoff100−r¯where
r¯ is the average of the effective federal funds rate over the month.31 To construct the change in
expectations for the remainder of the month, we must adjust for the fact that a part of the month
hasalreadyelapsedwhentheFOMCmeetingoccurs. Supposethemonthinquestionhasm days
0
andtheFOMCmeetingoccursondayd . Letf1 denotethepriceofthecurrentmonth’sfederal
0 t−∆t
funds rate futures contract immediately before the FOMC announcement and f1 the price of this
t
contractimmediatelyfollowingtheFOMCannouncement. Letr denotetheaveragefederalfunds
−1
rate during the month up until the point of the FOMC announcement and r the average federal
0
fundsratefortheremainderofthemonth. Then
d m −d
f1 = 0 r + 0 0 E r ,
t−∆t m −1 m t−∆t 0
0 0
d m −d
f1 = 0 r + 0 0 E r .
t m −1 m t 0
0 0
Asaresult
m
E r −E r = 0 (f1−f1 ).
t 0 t−∆t 0 m −d t t−∆t
0 0
When the FOMC meeting occurs on a day when there are 7 days or less remaining in a month,
we instead use the change in the price of next month’s fed funds futures contract. This avoids
multiplyingf1−f1 byaverylargefactor.
t t−∆t
The second variable used in constructing the policy news shock is the change in the expected
federal funds rate at the time of the next scheduled FOMC meeting. Similar issues arise in con-
structing this variable as with the variable described above. Let m denote the number of days
1
in the month in which the next scheduled FOMC meeting occurs and let d denote the day of the
1
meeting. The next scheduled FOMC meeting may occur in the next month or as late as 3 months
31Fedfundsfutureshavebeentradedsince1988.TheeffectivefederalfundsrateistheratethatisquotedbytheFed-
eralReserveBankofNewYorkoneverybusinessday. SeetheChicagoBoardofTradeReferenceguidehttp://www.
jamesgoulding.com/Research_II/FedFundsFutures/FedFunds(FuturesReferenceGuide).pdf for a de-
taileddescriptionoffederalfundsfuturescontracts. OnatradingdayinMarch(say), theAprilfederalfundsfutures
contractislabeledas2ndexpirationnearbyandalsoas1stbeginningnearby,inreferencetothemonthoverwhichr¯is
computed.
36

afterthecurrentmeeting. Letfn denotethepriceofthefederalfundsratefuturescontractforthe
t−∆t
monthofthenextscheduledFOMCmeetingimmediatelybeforetheFOMCannouncementandfn
t
the price of this contract immediately following the FOMC announcement. Let r denote the fed-
1
eralfundsrateafterthenextscheduledFOMCmeeting. Analogouscalculationstowhatwepresent
aboveyield
(cid:20) (cid:21)
m d
E r −E r = 1 (fn−fn )− 1 (E r −E r ) .
t 1 t−∆t 1 m −d t t−∆t m t 0 t−∆t 0
1 1 1
As with the first variable, if the next scheduled FOMC meeting occurs on a day when there are 7
days or less remaining in a month, we instead use the change in the price of next month’s federal
fundsfuturescontract.
The last three variables used are the change in the price of three eurodollar futures at the time
of the FOMC announcements. A eurodollar futures contract expiring in a particular quarter (say
2ndquarter2004)isanagreementtoexchange,onthesecondLondonbusinessdaybeforethethird
Wednesday of the last month of the quarter (typically a Monday near the 15th of the month), the
price of the contract p for 100 minus the then current three-month US dollar BBA LIBOR interest
rate. Thecontractthusprovidesmarket-basedexpectationsofthethreemonthnominalinterestrate
ontheexpirationdate.32 Wemakeuseofeurodollarfuturesathorizonsofnquartersinthefuture
forn=2,3,4or,moreprecisely,theexpirationdateofthe“nquarter”eurodollarfutureisbetween
n−1andnquartersinthefutureatanygivenpointintime.
Weapproximatethechangeinthesevariablesovera30-minutewindowaroundFOMCbytak-
ing the difference between the price in the last trade that occurred more than 10 minutes before
the FOMC announcement and the first trade that occurred more than 20 minutes after the FOMC
announcement. On control days in the analysis using the heteroskedasticity based estimation ap-
proach,wetakethelasttradebefore2:05pmandthefirsttradeafter2:35pm(sinceFOMCannounce-
mentstendtooccurat2:15pm). Onsomedays(mostoftencontroldays),tradingisquitesparseand
theresometimesis notradebefore2:05orafter2:35. Tolimitthesizeofthewindowsweconsider,
we only consider trades on the trading day in question and until noon the next day. If we do not
findeligibletradestoconstructthepricechangeweareinterestedinwithinthiswindow,wesetthe
pricechangetozero(i.e.,weinterpretnotradingasnopricechange).
32Eurodollar futures began trading in the early 1980’s. See the CME Group eurodollar futures ref-
erenceguidehttp://www.cmegroup.com/trading/interest-rates/files/eurodollar-futures-refere
nce-guide.pdfformoredetailsabouthoweurodollarfuturesaredefined.
37

B Rigobon’s Heteroskedasticity-Based Estimator
Table2presentsresultsfromaheteroskedasticity-basedestimatorofthetypedevelopedbyRigobon
(2003)andRigobonandSack(2004). Theempiricalmodelweconsiderinthisanalysisisthefollow-
ing. Let (cid:15) denote a pure monetary shock and suppose that movements in the policy indicator ∆i
t t
weobserveinthedataisgovernedbothbymonetaryandnon-monetaryshocks:
∆i = α +(cid:15) +η , (8)
t i t t
where η is a vector of all other shocks that affect ∆i . Here α is a constant and we normalize
t t i
the impact of (cid:15) and η on ∆i to one. We wish to estimate the effects of the monetary shock (cid:15) on
t t t t
an outcome variable ∆s . This variable is also affected by both the monetary and non-monetary
t
shocks:
∆s = α +γ(cid:15) +βη . (9)
t s t t
The parameter of interest is γ, which should be interpreted as the impact of the pure monetary
shock(cid:15) on∆s relativetoitsimpacton∆i .
t t t
Our identifying assumption is that the variance of monetary shocks increases at the time of
FOMCannouncements,whilethevarianceofothershocksisunchanged. DefineR1asasampleof
narrowtimeintervalsaroundFOMCannouncements,anddefineR2asasampleofequallynarrow
timeintervalsthatdonotcontainFOMCannouncementsbutarecomparableonotherdimensions
(e.g., same time of day, same day of week, etc.). We refer to R1 as our “treatment” sample and R2
asour“control”sample. Ouridentifyingassumptioncanthenbewrittenas
σ > σ , whileσ = σ .
(cid:15),R1 (cid:15),R2 η,R1 η,R2
LetΩ denotethevariance-covariancematrixof[∆i ,∆s ]inregimeRi. ThenΩ isgivenby
Ri t t Ri
 
σ2 + (cid:80) σ2 γσ2 + (cid:80) β σ2
(cid:15),Ri j η,j (cid:15),Ri j s,j η,j
Ω Ri =  ,
γσ2 + (cid:80) β σ2 γ2σ2 + (cid:80) β2 σ2
(cid:15),Ri j s,j η,j (cid:15),Ri j s,j η,j
wherej indexestheelementsofη .
t
Noticethat
 
1 γ
∆Ω = Ω
R1
−Ω
R2
= (σ
(cid:15)
2
,R1
−σ
(cid:15)
2
,R2
) .
γ γ2
38

Thus,
∆Ω cov (∆i ,∆s )−cov (∆i ,∆s )
12 R1 t t R2 t t
γ = = . (10)
∆Ω var (∆i )−var (∆i )
11 R1 t R2 t
This is the estimator we use to construct the results in Table 2 and Table A.3. Notice that if we
set the variance of the “background noise” η to zero, then the heteroskedasticity-based estimator,
t
equation (10) reduces to the coefficient from an OLS regression of ∆s on ∆i . Intuitively, the full
t t
heteroskedasticity-basedestimatorcanbethoughtofasthesimpleOLSestimator, adjustedforthe
“normal”covariancebetween∆s and∆i andthe“normal”varianceof∆i .
t t t
C Weak Instruments Robust Confidence Intervals
TheconfidenceintervalsinTable2areconstructedusingamoresophisticatedbootstrapprocedure
thanisconventional. Thereasonisthattheconventionalbootstrapapproachtoconstructingconfi-
dence intervals yields inaccurate results in the case when there is a significant probability that the
differenceinthevarianceof∆i betweenthetreatmentandcontrolsampleisclosetozero.33 Figure
t
C.1illustratesthatthisisthecaseforthe1-daywindowestimationbutnotthe30-minutewindow.
Theproblemisessentiallyoneofweakinstruments. RigobonandSack(2004)showthattheestima-
tor in equation (10) can be formulated as an IV regression. When the difference in the variance of
∆i betweenthetreatmentandcontrolsampleissmall,theinstrumentinthisformulationisweak,
t
leadingtobiasedpointestimatesandconfidenceintervals.
In Table 2, we, therefore, employ a weak-instruments robust approach to constructing confi-
dence intervals. The approach we employ is a test inversion approach. A 95% confidence interval
for our parameter of interest γ can be constructed by performing a hypothesis test for all possi-
ble hypothetical true values of γ and including those values that are not rejected by the test in the
confidenceinterval.
Theteststatisticweuseis
g(γ) = ∆cov(∆i ,∆s )−γ∆var(∆i ), (11)
t t t
where ∆cov and ∆var denote the difference between the covariance and variance, respectively, in
thetreatmentandcontrolsamples.
33RecallthattheRigobonestimator—equation(10)—isaratiowiththedifferenceinthevarianceof∆i t betweenthe
treatmentsampleandthecontrolsampleinthedenominator.Ifthedistributionofthisdifferencehassignificantmassin
thevicinityofzero,thesamplingdistributionoftheestimatorwillhavesignificantmassatlargepositiveandnegative
values.
39

Dvar
0.0045
0.0040
0.0035
0.0030
0.0025
0.0020
0.0015
0.0010
0.0005
0.0000
-0.0005
-0.0010
-0.002 -0.001 0.000 0.001 0.002 0.003 0.004 0.005
Dcov
Panel A: 1-Day Window
Dvar
0.0025
0.0020
0.0015
0.0010
0.0005
0.0000
-0.0005 0.0000 0.0005 0.0010 0.0015 0.0020 0.0025
Dcov
Panel B: 30-Minute Window
FigureC.1:FSigcuartete Ar.o1f: JSocianttteDrpilsottrsi bouf tJiooinnto SfaDmcpolvinagn DdisDtrvibaurtifoonr o2f- YDecaorvN aonmd Dinvaalr Ffoorr w ardRate
2-Year Nominal Forward Rate
Notes:Eachpointinthefigureisadrawfromourbootstrap.Dvardenotesthedifferenceinvarianceofourpolicynews
shocEkacbhe tpwoeiennt itnh ethtere faitgmureen tisa na ddrcaownt rforolmsa mouprl eb.ooDtcsotrvapd.e Dnovtaers dtheneodteifsf etrheen cdeififnertehnecec oivna vriaarniacnecoef oofu orupro plioclyicnye ws
shocnkeswasn sdhtohcek2 b-yeetwareneno mthien atlrefoatrmweanrdt arantde cboentwtroeel nsathmeptlree.a Dtmcoenvt daenndottehse tchoen tdrioflfesraemnpcele i.n the covariance of our
policy news shocks and the 2-year nominal forward rate between the treatment and the control sample.
40

g(gamma)
0.008
Median
0.006 97.5% Quantile
2.5% Quantile
0.004
0.002
0.000
-0.002
-0.004
-0.006
-0.008
-2.0 -1.5 -1.0 -0.5 0.0 0.5 1.0 1.5 2.0 2.5
gamma
Figure A.2: Quantiles of the distribution of (cid:1859)(cid:4666)(cid:2011)(cid:4667) for different values of (cid:2011) when estimating effect on
Fthigeu 2r-eyeCa.r2 n:oQmuiannalt ifloerswoafrdth reatDe iusstirnibgu at i1o-ndaoyf wgi(nγd)ow
Notes: Quantiles of the distribution of g(γ) for different values of γ when estimating effect on the 2-year nominal
forwardrateusinga1-daywindow
Intuitively, g(γ) = 0 at the true value of γ. We estimate the distribution of g(γ) for each hypo-
thetical value of γ and include in our confidence interval values of γ for which g(γ) = 0 cannot be
rejected. FigureC.2plotsthe2.5%,50%and97.5%quantilesofthedistributionofg(γ)asafunction
of γ for the 2-year nominal forward in the one-day window case. Values of γ for which the 2.5%
quantileliesbelowzeroandand97.5%quantileliesabovezeroareincludedinthe95%confidence
interval. This method for constructing confidence intervals is referred to as the Fieller method by
Staiger, Stock, and Watson (1997) as it is an extension of an approach proposed by Fieller (1954).
We use a bootstrap to estimate the joint distribution of ∆cov and ∆var. Our approach is therefore
similartothegridbootstrapproposedbyHansen(1999)foradifferentapplication.
This more sophisticated procedure for constructing confidence intervals is not important for
ourbaselineestimatorbasedonchangesinthepolicynewsshockovera30-minutewindow. Inthis
case, the weak-IV robust confidence intervals coincide closely with the standard non-parametric
bootstrap confidence interval reported in Table A.3. However, this weak-IV robust procedure is
very important for the Rigobon estimator when the policy news shock is measured over a 1-day
window.
41

D Risk Premia or Expected Future Short Rates
Wepresentthreesetsofresultsthatindicatethatriskpremiumeffectsarenotdrivingourempirical
results: 1) the impact of our policy news shock on direct measures of expectations from the Blue
ChipEconomicIndicators;2)theimpactofourpolicynewsshockonrisk-neutralexpectedshortrates
from a state-of-the-art affine term structure model; and 3) the impact of our policy news shock on
interestratesoverlongereventwindowsthaninourbaselineresults.
Let us begin with our analysis of the Blue Chip forecast data. Blue Chip surveys professional
forecasters on their beliefs about macroeconomic variables over the next two years in the first few
daysofeverymonth. Fromthissurvey,itispossibletoobtaindirectmeasuresofexpectationsthat
are not contaminated by risk premium effects. We use expectations about future values of the 3-
monthT-Billrateasourmeasureofshort-termnominalinterestrateexpectationsandexpectations
aboutchangesintheGDPdeflatorasourmeasureofexpectationsaboutinflation(andthedifference
betweenthetwoasourmeasureofexpectationsaboutshort-termrealrates).
Weestimatetheimpactofmonetaryshocksonexpectationsbyrunningregressionsofthechange
from one month to the next in expectations regarding a particular forecast horizon on the policy
news shock that occurs over the month except for those that occur in the first week of the month
(because we do not know whether these occurred before or after the survey response). Unfor-
tunately, Blue Chip asks respondents only about the current and subsequent calendar year on a
monthly basis. So, fewer observations are available for longer-term expectations, leading to larger
standarderrors.34 ThesampleperiodforthisanalysisisJanuary1995toApril2014,exceptthatwe
excludetheapexofthe2008-2009financialcrisisaswedoinourbaselineanalysis.
TableD.1presentstheresultsfromthisanalysis. Thetableshowsthatthepolicynewsshockhas
a persistent impact on expected short-term interest rates, both nominal and real. The interest rate
effectsaresomewhatlargerthaninourbaselineresults, butrathernoisilyestimated. Theeffecton
expected inflation is small and statistically insignificant at all horizons. The much larger standard
errors in Table D.1 arise from the fact that the Blue Chip variables are available only at a monthly
frequency as opposed to a daily frequency. Overall, these estimates appear consistent with our
baselinefindingsthatmonetaryshockshavelargeeffectsonexpectedshort-termnominalandreal
rates.
34Forexample,towardstheendofeachyear,forecastersareonlyaskedabouttheirbeliefsalittlemorethan1-yearin
advance;whileinthefirstquartertheyareaskedabouttheirbeliefsforalmostthenextfull2-years. BlueChipalsoasks
forlonger-terminflationforecasts,butonlytwiceayear(MarchandOctober)implyingthattherearetoofewobservations
toobtainmeaningfulestimates.
42

TABLE D.1
TableDE.f1f:ecEtfsf eocf tMsoofneMtaoryn eSthaoryckSsh oonc SkusrovneyS EuxrvpeecytaEtxiopnesctations
Nominal Real Inflation
1 quarter 1.05 1.17 -0.12
(0.73) (0.78) (0.24)
2 quarters 1.18 1.63 -0.44
(0.75) (0.78) (0.31)
3 quarters 0.99 1.29 -0.30
(0.72) (0.77) (0.24)
4 quarters 0.86 1.17 -0.32
(0.71) (0.69) (0.23)
5 quarters 0.73 0.59 0.14
(0.89) (0.94) (0.21)
6 quarters 1.84 1.60 0.23
(0.89) (0.88) (0.24)
7 quarters 4.45 4.29 0.17
(1.91) (1.99) (0.27)
Each estimatecomes from a separate OLS regression. We regress changes in survey expectations from the Blue
Chip Economic Indicators on the policy news shock. Since the Blue Chip survey expectations are available at a
monthly frequency, we construct a corresponding monthly measure of our policy news shock. In particular, we
useanypolicynewsshockthatoccursoverthemonthexceptforthosethatoccurinthefirstweek(becausewedo
notknowwhethertheseoccurredbeforeorafterthesurveyresponse).Thedependentvariableisthechangeinthe
forecasted value of the variable listed at the top N quarters ahead, between this month's survey and last month's
survey. See Appendix F for details. We consider the effects on expected future 3-month T-Bill rates, short-term
realinterestratesandinflation,wheretheinflationrateistheGDPdeflatorandtheshort-termrealinterestrateis
calculated as the difference between the expected 3-month T-bill rate and the expected GDP deflator for agiven
quarter.ThesampleperiodisallregularlyscheduledmeetingsbetweenJanuary1995andApril2014, exceptthat
weexcludetheperiodfromJuly2008throughJune2009andtheaforementionedfirst-weekmeetings.Thepolicy
newsshockisconstructedonthissampleperiod.Thesamplesizeis120forthefirstfourrowsofthetable.Itthen
falls to 75, 45, and 13 for rows 5 through 7, respectively. Robust standard errors are in parentheses.
Our second approach is to regress estimates of changes in expected future short rates from a
state-of-the-artaffinetermstructuremodelonourmonetarypolicyshocks. Abrahamsetal. (2015)
employanaffinetermstructuremodeltodecomposechangesinbothnominalandrealinterestrates
at different maturities into changes in risk-neutral expected future short rates and changes in risk
premia.35 TableD.2presentsresultsbasedontheirdecomposition. Theresponseofmodel-implied
risk-neutral interest rates to our policy news shock is very similar to the response of raw interest
rates in our baseline results. This piece of evidence, thus, points to our monetary shocks having
large effects on future short-term nominal and real rates and small effects on expected inflation
35Whatwerefertoastheriskpremiahereisthedifferencebetweenrawinterestratechangesandchangesinmodel-
implied risk neutral interest rates. Abrahams et al. (2015) further decompose this difference into a term premium, a
liquiditypremium,andamodelerrorterm.
43

TABLE D.2
TableDR.2e:sRpoenspseo onfs eExopfeEcxtepde cFtuetdurFe uSthuorret SRhaoterst aRnadt eRsisakn PdreRmisikaPremia
Expected Future Short Rates Risk Premia
Nominal Real Nominal Real
2Y Treasury Yield 1.01 0.86 0.09 0.20
(0.27) (0.17) (0.10) (0.18)
3Y Treasury Yield 0.93 0.82 0.13 0.21
(0.26) (0.18) (0.15) (0.19)
5Y Treasury Yield 0.76 0.60 -0.04 0.04
(0.16) (0.12) (0.11) (0.14)
10Y Treasury Yield 0.50 0.40 -0.12 0.04
(0.11) (0.08) (0.14) (0.14)
2Y Treasury Forward Rate 0.79 0.73 0.35 0.26
(0.24) (0.22) (0.26) (0.21)
3Y Treasury Forward Rate 0.61 0.56 0.21 0.32
(0.19) (0.17) (0.29) (0.25)
5Y Treasury Forward Rate 0.36 0.33 -0.11 0.14
(0.08) (0.08) (0.17) (0.17)
10Y Treasury Forward Rat 0.10 0.09 -0.18 0.04
(0.02) (0.02) (0.18) (0.12)
EachestimatecomesfromaseparateOLSregression.Thedependentvariablesinthefirsttwocolumnsareone-day
changes in risk neutral yields and forwards from Abrahams et al. (2015) -- i.e., measures of expected future short
rates. The dependent variables in the later two columns are the difference between one-day changes in raw yields
andforwardsandone-daychangesintheriskneutralyieldsandforwardsfromAbrahamsetal.(2015).Wereferto
this difference as the risk premia. It corresponds to the term premium, liquidity premium and model error in
Abrahams et al. (2015). The independent variable is a change in the policy new shock over a 30 minute window
around the time of FOMC announcements. The forward rates are one-year forwards at different horizons. The
sample period is all regularly scheduled FOMC meetings from 1/1/2000 to 3/19/2014, except that we drop the
period from July 2008 through June 2009. For 2Y and 3Y yields and real forwards, the sample starts in January
2004. The sample size for the 2Y and 3Y yields and forwards is 74. The sample size for all other regressions is
106—the same observations from which the policy news shock is constructed. Robust standard errors are in
parentheses.
44

(evensmallerthaninourbaselineresults).
ItisimportanttostressthattheAbrahamsetal. (2015)modelbynomeansrulesoutthepotential
importance of risk premium effects. In fact, risk premia for long-term bonds are large and volatile
inthismodel. Whilethismodelpredictsthatalargefractionofinterestratevariationatothertimes
areassociatedwithriskpremia,thisisnotthecaseforinterestratemovementsatthetimeofFOMC
announcements. In this regard, our measure of the monetary shock appears to differ importantly
fromthatofHansonandStein(2015). Ourmonetaryshockshavevirtuallynoeffectonriskpremia,
as we describe above. In contrast, Hanson and Stein’s measure (based on the 2-day change in the
2-year nominal yield around FOMC announcements, as we describe in section 3.2) is associated
with large changes in risk premia (Abrahams et al., 2015). This suggests that Hanson and Stein’s
measureofmonetarypolicyshocksis—eitherduetogreaterbackgroundnoise,orbecauseitpicks
upvariationininterestratesfurtheroutintheyieldcurve—muchmoreassociatedwithmovements
inriskpremiaatthetimeofFOMCmeetingsthanourpolicynewsshock.
Ourthirdapproachtogaugingtheroleofriskpremiainourresultsistoconsiderlongerevent
windows for the outcome variables of interest. Some models of liquidity premia (such as the one
developedinHansonandStein(2015))predictthatweshouldseerealinterestrateeffectsdissipate
quicklyaftertheannouncement.36 TableD.3presentstheeffectsofourpolicynewsshockonnomi-
nalandrealinterestratesovereventwindowsof1,5,10,20,60,125,and250tradingdays.37 While
the estimates become very noisy as the event window becomes larger, there is little evidence that
the effects on interest rates tend to dissipate over time. Indeed, in most cases, the point estimates
appeartogrowovertime(though,again,thestandarderrorsarequitelarge).
E A Conventional Model of Monetary Shocks
What do the empirical estimates in section 3 tell us about the economy? The conventional view
of how monetary policy affects the economy can be decomposed into two parts. First, changes in
nominal interest rates affect real interest rates. Second, changes in real interest rates affect output.
The second of these components is a common feature of virtually all macroeconomic models and
hasnothingtodowithmonetarypolicyperse. Inparticular,bothNeoclassicalandNewKeynesian
models share the implication that changes in real interest rates affect output. In sharp contrast,
36HansonandStein(2015)presentabehavioralmodelinwhich“searchforyield”generatessignificantriskpremium
effectsofmonetaryshocksthatdissipateovertime.
37Inallcases,thepolicynewsshockismeasuredovera30-minuteeventwindow.Weonlyvarythelengthoftheevent
windowforthedependentvariables.
45

TABLE D.3
Mean Reversion
TableD.3: MeanReversion
Horizon Nominal Yields Real Yields
(Trading Days) 2-Year 3-Year 5-Year 2-Year 3-Year 5-Year
1 1.10 1.06 0.73 1.06 1.02 0.64
(0.34) (0.39) (0.21) (0.28) (0.31) (0.19)
5 2.24 2.06 0.85 1.01 0.93 0.52
(1.09) (1.07) (0.50) (0.64) (0.68) (0.38)
10 2.39 2.20 0.22 1.35 1.20 0.28
(1.07) (1.05) (0.80) (0.55) (0.57) (0.53)
20 0.60 0.29 -0.01 0.88 0.43 0.04
(1.22) (1.16) (1.11) (0.95) (0.94) (0.79)
60 3.41 2.80 -0.17 1.96 1.72 -0.10
(2.38) (2.17) (1.46) (2.13) (1.92) (1.13)
125 9.42 8.02 3.20 6.16 5.22 2.47
(1.78) (1.61) (1.98) (2.86) (2.50) (1.44)
250 13.52 11.56 4.72 9.58 8.22 4.13
(3.31) (3.08) (2.30) (2.92) (2.97) (1.84)
Each estimate comes from a separate OLS regression. We regress the cumulative change in yields between the day before the
FOMCannouncementand1,5,10,20,60,125and250tradingdaysaftertheannouncementonthepolicynewsshockinthe30
minute interval surrounding the FOMC announcement. The first three columns present results for nominal zero coupon yields,
and the next three columns present results for real zero coupon yields. The sample period is all regularly scheduled meetings
from1/1/2000to3/19/2014,exceptthatwedroptheperiodfromJuly2008throughJune2009.For2Yand3Yyields,thesample
startsinJanuary2004. Going downtherows,thesamplesizesforthe2Yand3Yyieldsare74, 73,73, 73,72, 69,and65. The
sample sizes for the 5Y yield are 106, 105, 105, 105, 104, 101, and 97. The policy news shock is constructe on the 2000-2014
sample used in Table 1. Newey-West standard errors with 4 lags are in parentheses.
Neoclassical and New Keynesian models have very different predictions regarding the extent to
whichchangesinnominalinterestratescausedbymonetarypolicycanaffectrealinterestrates. In
a Neoclassical model, variation in nominal interest rates caused by monetary policy have no effect
ontherealinterestrate,whileinNewKeynesianmodels,suchmovementsinnominalinterestrates
canhavelargeeffectsonrealratesifpricesaresufficientlysticky.
The evidence we present in section 3 shows that variation in nominal interest rates caused by
monetary policy announcements does have large and persistent effects on real interest rates. In a
conventionalmodelofhowmonetaryshocksaffecttheeconomy—i.e.,onewheremonetaryshocks
only convey information about the future path of policy and don’t change private sector views
about other fundamentals of the economy—this evidence identifies key parameters governing the
rigidityofprices. WecanillustratethisverysimplyusingthetextbookNewKeynesianmodel.
Consider a setting in which the behavior of households and firms can be described by the fol-
46

lowingEulerequationandPhillipscurve:
xˆ = E xˆ −σ(ˆı −E πˆ −rˆn), (12)
t t t+1 t t t+1 t
πˆ = βE πˆ +κζxˆ . (13)
t t t+1 t
Hattedvariablesdenotepercentagedeviationsfromsteadystate. Thevariablexˆ = yˆ −yˆn denotes
t t
the “output gap”—the difference between actual output yˆ and the “natural” level of output yˆn
t t
that would prevail if prices were flexible— πˆ denotes inflation, ˆı denotes the gross return on a
t t
one-period, risk-free, nominal bond, and rˆn denotes the “natural rate of interest.” The parameter
t
σ in the Euler equation denotes the intertemporal elasticity of substitution, while β denotes the
subjective discount factor of households, κ and ζ denote nominal and real rigidities, respectively.
Both the natural rate of output and the natural rate of interest are functions of exogenous shocks
totastesandtechnology. AppendixHpresentsadetailedderivationoftheseequationsfromprim-
itive assumptions about tastes and technology. Woodford (2003) and Gali (2008) present textbook
treatments.
Supposethiseconomystartsoffatazero-inflationsteadystateandisthendisturbedbyamon-
etary shock. Assuming that the monetary shock has no effect on output in the long run, we can
solve the Euler equation—equation (12)—forward and get that the response of the output gap to
themonetaryshockis,
∞
(cid:88)
xˆ = −σ E rˆ = −σrˆ(cid:96). (14)
t t t+j t
j=0
whererˆ denotestheresponseoftheshort-termrealinterestrateattimet+j—i.e.,rˆ =ˆı −
t+j t+j t+j
E πˆ —andrˆ(cid:96)denotestheresponseofthelong-runrealinterestrate. Noticethatrˆn = 0inthis
t+j t+j+1 t t
casesincethemonetaryshockhasnoeffectonthenaturalrateofinterest.
Similarly,wecansolveforwardthePhillipscurve—equation(13)—andgetthattheresponseof
inflationtothemonetaryshockis
∞
(cid:88)
πˆ = κζ βjE xˆ . (15)
t t t+j
j=0
Combiningequations(14)and(15),wegetarelationshipbetweentheresponseofinflationand
theresponseoftherealinterestratestothemonetaryshock:
∞
(cid:88)
πˆ = −κζσ βjE rˆ(cid:96) . (16)
t t t+j
j=0
47

Recallthatinsection3weestimatetheresponseofinflationandrealinterestratestoamonetary
shock. These are exactly the two responses that appear in equation (16). Equation (16) therefore
shows that in the textbook New Keynesian model the relative size of the response of inflation and
realinterest ratespins downthe magnitudeofthe parametertriplet κζσ. Viewed through the lens
of this model, the fact that we estimate a small response of inflation relative to the response of the
real interest rate implies that either: 1) the Phillips curve must be very flat (κζ small), implying a
lotofnominalandrealrigidities,or2)outputmustbeveryunresponsivetotherealinterestrate(σ
small),orboth.
Notice that in reaching these conclusions we do not need to fully specify the monetary policy
rule. Theonlyassumptionweneedtomakeaboutmonetarypolicyisthatmonetaryshocksdonot
have long-run effects on output. This is true of most common specifications of monetary policy
rulesusedintheliterature. Inthisrespect,theconclusionsreachedabovearequiterobust.
Evenso,let’sconsiderwhetherthisargumentcontinuestoholdevenifthemonetaryshockleads
to a shift in the long-run inflation target of the central bank (and therefore the long-run inflation
rate). Inthiscase,equation(16)becomes
∞
(cid:88)
πˆ = −κζσ βjE rˆ(cid:96) +πˆ , (17)
t t t+j ∞
j=0
where πˆ denotes the change in the long-run inflation rate. The case we consider above assumed
∞
that π = 0. Even if this term is non-zero, however, it is important to recognize that it affects
∞
inflation in every period after the shock. Hence, it would not change the slope of the response of
expected inflation. The extra term does have the potential to lead to a larger response of inflation
to a monetary shock than in our baseline model. Empirically, however, the response of expected
inflationtothemonetaryshockalreadyappearstobeverysmall. Addingthisfeaturetothemodel
wouldfurtherincreasethedegreeofrigiditiesweestimateinthedata,andtherefore,thedegreeof
monetarynon-neutrality.
In the analysis above, we did rely heavily on the conventional view of monetary shocks that
theyconveyinformationonlyaboutthefuturepathofpolicybutdon’tchangeprivatesectorviews
about other fundamentals of the economy. In this view, monetary shocks may occur because the
privatesectorislearningaboutthepreferencesofthepolicymakers,orbecausetheprivatesectoris
learningaboutthepolicymaker’smodeloftheworld,orbecausetheprivatesectorislearningabout
thepolicymaker’sviewsonthestateoftheeconomy. Crucially,however,theannouncementbythe
policymakercannotleadtheprivatesectortoupdateitsownviewsaboutthestateoftheeconomy
48

or the model of the world. If it does, the monetary shocks contains an additional “information
effect.”
If FOMC announcements affect not only beliefs about future monetary policy but also beliefs
about future natural rates of interest, the conclusions reached above regarding what we can learn
from the empirical evidence presented in section 3 can change dramatically. In this case, equation
(14)becomes
∞
(cid:88)
xˆ = −σ E (rˆ −rˆn ) = −σ(rˆ(cid:96)−rˆn(cid:96)), (18)
t t t+j t+j t t
j=0
where rˆn(cid:96) denotes the response to the monetary announcement of private sector beliefs about the
t
long-termnaturalrateofinterest,andequation(16)becomes
∞
(cid:88)
πˆ = −κζσ βjE (rˆ(cid:96) −rˆn(cid:96)). (19)
t t t+j t
j=0
Itisimportanttorecognizethatprivatesectorbehaviordependsonprivatesectorbeliefsaboutthe
future path of the natural rate. The variables rˆn and rˆn(cid:96) denote the response of private sector
t+j t
beliefs about natural rates, and rˆ and rˆ(cid:96) denote the response of private sector beliefs about
t+j t+j
actualrealrates.
Notice that allowing for information effects, the response of the output gap and inflation to a
monetary announcement is not determined by the response of real interest rates but rather by the
response of the real interest rate gap—i.e., the gap between real interest rates and the natural rate
of interest. This means that changes in real interest rates will not have as large effects on output
andinflationifFOMCannouncementshaveinformationeffectssincethemovementintheinterest
rate gap will be only some fraction of the overall movement in interest rates. It also means that
wewillestimatelargervaluesoftheparametertripletκζσ—i.e.,smallervaluesofnominalandreal
rigidities (for a given value of the IES)—since the sum on the right-hand-side of equation (19) will
besmallerthanifweignoredinformationeffects.
F Expected Output Growth Regressions
TheregressionsinTables3andA.5areoftheform
∆s = α+γ∆i +(cid:15) (20)
t,t−1 t−1 t
49

withthepolicynewsshockastheindependentvariable. InTable3,thedependentvariableis
gy +gy +gy gy +gy +gy
t,q(t)+1 t,q(t)+2 t,q(t)+3 t−1,q(t)+1 t−1,q(t)+2 t−1,q(t)+3
∆s = − (21)
t,t−1
3 3
wheregy denotestheaverageforecastmadeinmonthtaboutoutputgrowthinquarterq(t)+
t,q(t)+j
j, where q(t) is the quarter that month t belongs to. For example, t might be September 2008, in
which case q(t) is the third quarter of 2008, q(t)+2 is the first quarter of 2009, and gy is the
t,q(t)+2
average forecast made in September 2008 about the value of output growth in the first quarter of
2009. InTableA.5,thedependentvariableis
∆s = gy −gy (22)
t,t−1 t,q(t)+j t−1,q(t)+j
forj ∈ {0,1,...,7}.
G Greenbook Evidence
IfFedinformationisimportant,onemightexpectthatcontractionarymonetaryshockswoulddis-
proportionately occur when the Fed is more optimistic than the private sector about the state of
the economy. The top panel of Table G.1 tests this proposition using the Fed’s Greenbook forecast
aboutoutputgrowthasameasureofitsoptimismaboutthe economy.38 Wereportestimatesfrom
thefollowingregression:
policynewsshock = α+β (cid:0) ∆yGB −∆yBC(cid:1) +ε , (23)
t t,q t,q t
where ∆yGB is the Greenbook forecast of quarterly output growth (annualized) q quarters in the
t,q
future made in month t, and ∆yBC is the corresponding Blue Chip forecast. In words, we regress
t,q
our policy news shock on the contemporaneous difference between the Greenbook and Blue Chip
forecasts about real GDP growth at various horizons. The positive coefficients reported in the top
panelofTableG.1indicatethatourpolicynewsshockstendtobepositive(i.e., indicateasurprise
increase in interest rates) when the Greenbook forecast about current and future real GDP growth
ishigherthanthecorrespondingBlueChipforecast.
38ThestaffoftheBoardofGovernorshaspresentedtheFOMCwithanalysisandforecastsoftheUSeconomyinthe
Greenbook (now, the Tealbook) since 1965. Conveniently, both the Greenbook and Blue Chip datasets make forecasts
ofthesamevariable: annualizedrealGDPgrowth. TheGreenbookforecastsarefinalizedoneweekbeforeeachFOMC
meeting.
50

TABLE G.1
Greenbook versus Blue Chip Forecasts
TableG.1: IsFedInformationReflectedinGreenbookForecasts?
Horizon (q): -1 0 1 2 3 4 5 6 7
Does Fed Relative Optimism Explain Monetary Shocks?
β -- 1.19 1.01 1.21 1.00 1.20 1.89 3.10 1.88
-- (0.55) (0.74) (0.69) (0.77) (0.90) (1.10) (1.14) (1.64)
N -- 90 90 90 90 90 66 42 22
Does Fed Relative Optimism Reverse in Response to Monetary Shocks?
β -7.26 -4.07 -0.45 -0.87 -0.46 -1.66 -3.58 -1.34 -3.04
(3.63) (1.80) (1.53) (1.30) (1.08) (1.11) (1.31) (1.30) (2.44)
N 24 89 89 89 89 76 55 32 8
Each estimate comes from a separate OLS regression. In the first panel, we regress the policy news shock (scaled by
100)onthedifferenceinforecastsaboutoutputgrowthqquartersaheadbetweentheFed'sGreenbookforecastandthe
Blue Chip forecast. Since the Blue Chip forecasts are available at a monthlyfrequency, we construct a corresponding
monthly measure of our policy news shock. In particular, we use any policy news shock that occurs over the month
exceptforthosethatoccurinthefirstweek(becausewedonotknowwhethertheseoccurredbeforeorafterthesurvey
response).Inthesecondpanel,weregressthechangeinthedifferencebetweentheGreenbook andBlueChipforecast
ofoutputgrowthqquartersaheadonthenewspolicyshock.Thechangeisbetweenthemonthofthepolicyshockand
themonthofthesubsequentFOMCmeeting.SeeAppendix Ffordetails.Thesampleperiodisallregularlyscheduled
FOMC meetings from January 1995 to December 2009, except that we exclude the period from July 2008 through
June 2009 and the aforementioned first-week meetings. The policy news shocks are constructed over the 1995-2014
sample used in Table A.5. Robust standard errors are in parentheses.
We furthermore find that the difference between Greenbook and Blue Chip forecasts tends to
narrowafterourpolicynewsshocksoccur. Thissuggeststhatprivatesectorforecastersmayupdate
theirforecastsbasedoninformationtheygleamfromFOMCannouncements. Buildingonthework
ofRomerandRomer(2000),weestimatethefollowingregression:
(cid:2)(cid:0) ∆yGB −∆yBC (cid:1) − (cid:0) ∆yGB −∆yBC(cid:1)(cid:3) = α+βpolicynewsshock +ε , (24)
t+1,q t+1,q t,q t,q t t+1
wheretimet+1isthemonthofthenextFOMCmeeting. Inwords, weassesswhetherourpolicy
newsshocksforecastachangeinthedifferencebetweentheGreenbookandtheBlueChipforecasts
of output growth. The results of this regression are reported in the bottom panel of Table G.1. We
findthatapositivepolicynewsshockforecastsafallintheGreenbookforecastrelativetotheBlue
Chip forecast (or equivalently a rise in the Blue Chip forecast relative to the Greenbook forecast).
This change in statistically significant for the nowcast (q = 0) and for one of the longer-term fore-
casts(q = 5)butnotstatisticallysignificantfortheotherhorizons. Sincepositivemonetaryshocks
tendtobeassociatedwiththeGreenbookforecastbeingabovetheBlueChip,thefactthattheesti-
mates are negative in this regression indicates that, indeed, our policy news shocks are associated
51

withanarrowinginthediscrepancybetweenFedandprivatesectorviewsontheeconomy.
H Micro-Foundations for Our Model
Thissectionlaysoutmicro-foundationsfortheNewKeynesianbusinesscyclemodelweuseinthe
paper. We do this in two steps. First we present a version of the model without internal habit and
a backward-looking term in the Phillips curve. Then in sections H.4-H.6, we show how the model
is modified to include internal habit and a backward-looking term in the Phillips curve. We end
thisappendixwithadiscussionofthedeterminationofthenaturalrateofoutputandproductivity
in the full model. We note that none of the derivations in this section depend on whether there is
aninformationeffectofnot. SeeWoodford(2003)andGali(2008)forthoroughexpositionsofNew
Keynesianmodels.
H.1 Households
The economy is populated by a continuum of household types indexed by x. A household’s type
indicatesthetypeoflaborsuppliedbythathousehold. Householdsoftypexseektomaximizetheir
utilitygivenby
∞
(cid:88)
E βt[u(C ,ξ )−v(L (x),ξ )], (25)
0 t t t t
t=0
whereβ denotesthehousehold’ssubjectivediscountfactor,C denoteshouseholdconsumptionof
t
a composite consumption good, L (x) denotes household supply of differentiated labor input x,
t
and ξ denotes a vector of preference shocks. There are an equal (large) number of households of
t
eachtype. Thecompositeconsumptiongoodinexpression(25)isanindexgivenby
(cid:20)(cid:90) 1 θ−1 (cid:21) θ− θ 1
C t = c t (z) θ dz , (26)
0
wherec (z)denotesconsumptionofproductsofvarietyz. Theparameterθ > 1denotestheelastic-
t
ityofsubstitutionbetweendifferentvarieties.
Householdshaveaccesstocompletefinancialmarkets. Householdsoftypexfaceaflowbudget
constraintgivenby
(cid:90) 1
P C +E [M B (x)] ≤ B (x)+W (x)L (x)+ Ξ (z)dz−T , (27)
t t t t,t+1 t+1 t t t t t
0
52

whereP isapriceindexthatgivestheminimumpriceofaunitoftheconsumptiongoodC ,B (x)
t t t+1
isarandomvariablethatdenotesthestatecontingentpayoffoftheportfoliooffinancialsecurities
heldbyhouseholdsoftypexatthebeginningofperiodt+1,M isthestochasticdiscountfactor
t,t+1
thatpricesthesepayoffsinperiodt,39 W (x)denotesthewageratereceivedbyhouseholdsoftype
t
xinperiodt,Ξ (z)denotestheprofitsoffirmz inperiodt,andT isalump-sumtaxleviedbythe
t t
government. ToruleoutPonzischemes,householddebtcannotexceedthepresentvalueoffuture
incomeinanystateoftheworld.
Households face a decision in each period about how much to spend on consumption, how
many hours of labor to supply, how much to consume of each differentiated good produced in
the economy and what portfolio of assets to purchase. Optimal choice regarding the trade-off be-
tween current consumption and consumption in different states in the future yields the following
consumptionEulerequation:
u (C ,ξ ) M P
c t+j t+j t,t+j t+j
= (28)
u (C ,ξ ) βj P
c t t t
as well as a standard transversality condition. The notation u denotes the partial derivate of the
c
functionuwithrespecttoC . Weuseanalogousnotationforotherpartialderivativesbelow. Equa-
t
tion (28) holds state-by-state for all j > 0. Optimal choice regarding the intratemporal trade-off
betweencurrentconsumptionandcurrentlaborsupplyyieldsalaborsupplyequation:
v (L (x),ξ ) W (x)
(cid:96) t t t
= . (29)
u (C ,ξ ) P
c t t t
Households optimally choose to minimize the cost of attaining the level of consumption C . This
t
impliesthefollowingdemandcurvesforeachofthedifferentiatedproductsproducedintheecon-
omy:
(cid:18)
p (z)
(cid:19)−θ
t
c (z) = C , (30)
t t
P
t
wherep (z)denotesthepriceofproductz and
t
(cid:20)(cid:90) 1 (cid:21) 1− 1 θ
P = p (z)1−θdz . (31)
t t
0
39ThestochasticdiscountfactorM t,t+1isarandomvariableoverstatesinperiodt+1. Foreachsuchstateitequals
thepriceoftheArrow-Debreuassetthatpaysoffinthatstatedividedbytheconditionalprobabilityofthatstate. See
Cochrane(2005)foradetaileddiscussion.
53

H.2 Firms
Thereareacontinuumoffirmsindexedbyzintheeconomy. Firmzspecializesintheproductionof
differentiatedgoodz,theoutputofwhichwedenotey (z). Forsimplicity,laboristheonlyvariable
t
factor of production used by firms. Each firm is endowed with a fixed, non-depreciating stock of
capital. Theproductionfunctionoffirmz is
y (z) = A f(L (z)), (32)
t t t
where A denotes aggregate productivity. The function f is increasing and concave. It is concave
t
becausetherearediminishingmarginalreturntolaborgiventhefixedamountofotherinputsem-
ployed at the firm. We follow Woodford (2003) in introducing heterogeneous labor markets. Each
firm belongs to an industry x. There are many firms in each industry. The goods in industry x are
produced using labor of type x and all firms in industry x change prices at the same time. This
heterogeneouslabormarketstructureisastrongsourceofrealrigiditiesinpricesetting.
Firmz actstomaximizeitsvalue,
∞
(cid:88)
E M [p (z)y (z)−W (x)L (z)]. (33)
t t,t+j t+j t+j t+j t+j
j=0
Firmz mustsatisfydemandforitsproductgivenbyequation(30). Firmz isthereforesubjecttothe
followingconstraint:
(cid:18)
p (z)
(cid:19)−θ
t
C ≤ A f(L (z)). (34)
t t t
P
t
Firm z takes its industry wage W (x) as given. Optimal choice of labor demand by the firm is
t
givenby
W (x) = A f (L (z))S (z), (35)
t t (cid:96) t t
where S (z) denotes the firm’s nominal marginal cost (the Lagrange multiplier on equation (34) in
t
thefirm’sconstrainedoptimizationproblem).
Firm z can reoptimize its price with probability 1−α as in Calvo (1983). With probability α, it
must keep its price unchanged. Optimal price setting by firm z in periods when it can change its
priceimplies
θ (cid:88) ∞ αjM t,t+j y t+j (z)
p t (z) = θ−1 E t (cid:80)∞ αkM y (z) S t+j (z). (36)
j=0 k=0 t,t+k t+k
Intuitively, the firm sets its price equal to a constant markup over a weighted average of current
54

andexpectedfuturemarginalcost.
H.3 ALinearApproximationofPrivateSectorBehavior
We seek a linear approximation of the equation describing private sector behavior around a zero-
growth, zero-inflation steady state. We start by deriving a log-linear approximation for the con-
sumption Euler equation that related consumption growth and a one-period, riskless, nominal
bond. This equation takes the form E [M (1 + i )] = 1, where i denotes the yield on a one-
t t,t+1 t t
period, riskless, nominal bond. Using equation (28) to plug in for M and rearranging terms
t,t+1
yields
(cid:20) (cid:21)
P U (C ,ξ )
t c t t
E βU (C ,ξ ) = . (37)
t c t+1 t+1
P 1+i
t+1 t
The zero-growth, zero-inflation steady state of this equation is β(1 +¯ı) = 1. A first order Taylor
seriesapproximationofequation(37)aroundthissteadystateis
cˆ = E cˆ −σ(ˆı −E πˆ )−σE ∆ξˆ , (38)
t t t+1 t t t+1 t ct+1
where cˆ = (C −C)/C, πˆ = π −1,ˆı = (1+i −1−¯ı)/(1+¯ı), and ξˆ = (U /U )(ξ −1). The
t t t t t t ct ξc c t
parameterσ = −U /(U C)denotestheintertemporalelasticityofsubstitutionofhouseholds.
c cc
We next linearize labor demand, labor supply, and the production function and combine these
equations to get an expression for the marginal costs in period t+j of a firm that last changed its
priceinperiodt. Let(cid:96) (x)denotethepercentdeviationfromsteadystateinperiodt+j ofhours
t,t+j
workedforworkersinindustryxthatlastwasabletochangepricesinperiodt. Letotherindustry
levelvariablesbedefinedanalogously. Weassumethatf(L (x)) = La(x).
t t
Alinearapproximationoflabordemand—equation(35)—inperiodt+j forindustryxthatwas
lastabletochangeitspricesinperiodtisthen
wˆ (x) = aˆ −(1−a)(cid:96)ˆ (x)+sˆ (x), (39)
t,t+j t+j t,t+j t,t+j
wherewˆ (x)andsˆ (x)denotethepercentagedeviationofrealwagesandrealmarginalcosts,
t,t+j t,t+j
respectively,fromtheirsteadystatevalues.
Alinearapproximationoflaborsupply—equation(29)—inperiodt+j forindustryxthatwas
lastabletochangeitspricesinperiodtis
wˆ (x) = η−1(cid:96)ˆ (x)+σ−1cˆ +ξˆ −ξˆ , (40)
t,t+j t,t+j t+j (cid:96),t+j c,t+j
55

whereξˆ = (V /V )(ξ −1). Theparameterη = V /(V L)istheFrischelasticityoflaborsupply.
(cid:96),t+j (cid:96)ξ (cid:96) t (cid:96) (cid:96)(cid:96)
Alinearapproximationoftheproductionfunction—equation(32)—inperiodt+j forindustry
xthatwaslastabletochangeitspricesinperiodtis
yˆ (x) = aˆ +a(cid:96)ˆ (x). (41)
t,t+j t+j t,t+j
Combining labor demand and labor supply—equations (39) and (40)—to eliminate wˆ (x)
t,t+j
yields
sˆ (x) = (η−1+1−a)(cid:96)ˆ (x)+σ−1cˆ −aˆ +ξˆ −ξˆ .
t,t+j t,t+j t+j t+j (cid:96),t+j c,t+j
Usingtheproductionfunction—equation(41)—toeliminate(cid:96)ˆ (x)yields
t,t+j
sˆ (x) = ωyˆ (x)+σ−1cˆ −(ω+1)aˆ +ξˆ −ξˆ , (42)
t,t+j t,t+j t+j t+j (cid:96),t+j c,t+j
whereω = (η−1+1−a)/a.
Taking logs of consumer demand—equation (30)—in period t+j for industry x what was last
abletochangeitspricesinperiodtyields
j
(cid:88)
yˆ (z) = −θpˆ(x)+θ πˆ +yˆ , (43)
t,t+j t t+k t+j
k=1
whereweusethefactthatY = C andy (x) = c (x). Pluggingthisequationintoequation(42)and
t t t t
againusingthefactthatY = C yields
t t
j
(cid:88)
sˆ (x) = −ωθpˆ(x)+ωθ πˆ +(ω+σ−1)yˆ −(ω+1)aˆ +ξˆ −ξˆ (44)
t,t+j t t+k t+j t+j (cid:96),t+j c,t+j
k=1
It is useful to derive the level of output that would prevail if all prices were flexible. Since our
model does not have any industry specific shocks (other than the opportunity to change prices),
marginal costs of all firms are the same when prices are flexible. Firm price setting in this case
yieldsp (x) = µS ,whereµ = θ/(θ−1). ThisimpliesthatallpricesareequalandthatS /P = 1/µ.
t t t t
Sincerealmarginalcostisaconstant, wehavesˆ = 0. Theflexiblepriceversionofequation(44)is
t
then
(ω+σ−1)yˆn = (ω+1)aˆ −ξˆ +ξˆ , (45)
t t (cid:96),t c,t
whereweusethefactthatoutputinallindustriesisthesameunderflexiblepricesandyˆ = cˆ and
t t
56

denotetherateofoutputunderflexiblepricesasyn. Wewillrefertoynasthenaturalrateofoutput.
t t
Combiningequations(44)and(45)yields
j
(cid:88)
sˆ (x) = −ωθpˆ(x)+ωθ πˆ +(ω+σ−1)(yˆ −yˆn ) (46)
t,t+j t t+k t+j t+j
k=1
Wenextlinearizethepricesettingequation—equation(36). Thisyields:
∞ ∞ ∞ j
(cid:88) (cid:88) (cid:88) (cid:88)
(αβ)jpˆ(x)− (αβ)jE sˆ (x)− (αβ)j E πˆ = 0.
t t t,t+j t t+k
j=0 j=0 j=1 k=1
Manipulationofthisequationyields
∞ ∞
(cid:88) (cid:88)
pˆ(x) = (1−αβ) (αβ)jE sˆ (x)+αβ (αβ)j−1E πˆ . (47)
t t t,t+j t t+j
j=0 j=1
Usingequation(46)toeliminatesˆ (x)inequation(47)andmanipulatingtheresultingequation
t,t+j
yields
∞ ∞
(cid:88) (cid:88)
pˆ(x) = (1−αβ)ζ (αβ)jE (yˆ −yˆn )+αβ (αβ)j−1E πˆ , (48)
t t t+j t+j t t+j
j=0 j=1
whereζ = (ω+σ−1)/(1+ωθ).
Alinearapproximationoftheexpressionforthepriceindex—equation(31)—yields
1−α
πˆ = pˆ(x). (49)
t t
α
Usingthislastequationtoreplacepˆ(x)inequation(48)yields
t
∞ ∞
(cid:88) (cid:88)
πˆ = κζ (αβ)jE (yˆ −yˆn )+(1−α)β (αβ)j−1E πˆ ,
t t t+j t+j t t+j
j=0 j=1
whereκ = (1−α)(1−αβ)/α. Quasi-differencingtheresultingequationyields
πˆ −αβE πˆ = κζ(yˆ −yˆn)+(1−α)βE πˆ ,
t t t+1 t t t t+1
whichimplies
πˆ = βE πˆ +κζ(yˆ −yˆn). (50)
t t t+1 t t
57

Finally,werewritethehousehold’sEulerequation—equation(38)intermsoftheoutputgap:
yˆ −yˆn = E (yˆ −yˆn )−σ(ˆı −E πˆ −rn), (51)
t t t t+1 t+1 t t t+1 t
wherern denotesthe“naturalrateofinterest”asisgivenby
t
1
rn = E ∆ξ + E ∆yˆn . (52)
t t c,t+1 σ t t+1
H.4 HouseholdBehaviorwithInternalHabits
Wenowconsideracaseinwhichhouseholdsformhabits. Householdsoftypexseektomaximize
autilityfunctiongivenby
∞
(cid:88)
E βt[u(C −bC )−v(L (x))], (53)
0 t t−1 t
t=0
wheretheparameterbgovernsthestrengthofhouseholds’habit. Wemodelhouseholdutilityfrom
consumption in period t as being affected by the amount that same household consumed in the
previousperiod. Ourmodelisthereforeamodelof“internalhabit.” Noticealsothatrelativetothe
derivationsabove,wehaveeliminatedreferencetothepreferencesshocksξ sincetheyplaynorole
t
intheanalysisinthebodyofthepaper.
Households face the same budget constraint as in the simple model (equation (27)). They also
face the same no-Ponzi condition as in the simple model. Maximization of utility subject to these
constraintsyieldsthefollowingconsumptionEulerequationandlaborsupplyequation:
Λ M P
t+j t,t+j t+j
= , (54)
Λ βj P
t t
v (L (x),ξ ) W (x)
(cid:96) t t t
= , (55)
Λ P
t t
whereΛ denotesmarginalutilityfromconsumptionattimetandisgivenby
t
Λ = u (C −bC )−bβE u (C −bC ). (56)
t c t t−1 t c t+1 t
H.5 FirmPriceSettingwithInflationInertia
Inthesimplemodelpresentedabove,weassumethatpricesareeitherreoptimized(withprobability
1 − α), or remain fixed (with probability α). As is well-known, this formulation yields a Phillips
curve that implies that inflation reacts rapidly to news about future economic developments. Our
58

empiricalevidencesuggeststhatinflationrespondsverygraduallytonewsaboutfutureeconomic
conditions. Tobeabletomatchthisaspectofourevidence,wenowfollowChristiano,Eichenbaum,
andEvans(2005)inconsideringaformulationofpricesettinginwhichfirmsindexthepriceofthe
good they produce to past inflation whenever they don’t reoptimize the price. This formulation
makesinflationsluggish.
Firm z can reoptimize its price with probability 1−α as in Calvo (1983). With probability α, it
setsitspriceaccordingtothefollowingsimplerule
P
t−1
p (z) = p (z). (57)
t t−1
P
t−2
The firm’s optimization problem is otherwise the same as in section H.2. Optimal price setting by
firmz inperiodswhenitcanchangeitspriceimplies
θ (cid:88) ∞ αjM t,t+j y t+j (z)
p t (z) = θ−1 E t (cid:80)∞ αkM (P /P )y (z) S t+j (z). (58)
j=0 k=0 t,t+k t+j−1 t−1 t+k
Thefirm’slabordemandequationisthesameasinsectionH.2.
H.6 ALinearizationofPrivateSectorBehaviorintheAugmentedModel
We seek a linear approximation of the equations describing private sector behavior with internal
habits and price indexation. As before, we start by deriving a log-linear approximation for the
consumption Euler equation that related consumption growth and a one-period, riskless, nominal
bond. Thisequationmaybewritten
(cid:20) (cid:21)
P Λ
t t
E βΛ = . (59)
t t+1
P 1+i
t+1 t
The zero-growth, zero-inflation steady state of this equation is β(1 +¯ı) = 1. A first order Taylor
seriesapproximationofequation(37)aroundthissteadystateis
λˆ = E λˆ +(ˆı −E πˆ ), (60)
t t t+1 t t t+1
whereλˆ = (Λ −Λ)/Λ.
t
Alinearapproximationoflaborsupply—equation(55)—inperiodt+j forindustryxthatwas
59

lastabletochangeitspricesinperiodtis
wˆ (x) = η−1(cid:96)ˆ (x)−λˆ . (61)
t,t+j t,t+j t+j
Alinearapproximationofmarginalutilityofconsumption—equation(56)—isgivenby
λˆ = −(1+b2β)σ cˆ +bσ cˆ +bβσ E cˆ , (62)
t c t c t−1 c t t+1
whereσ = −σ−1/((1−b)(1−bβ)).
c
Combining equation (61) with equations (39) (without the preference shock) and equation (41)
yields
sˆ (x) = ωyˆ (x)−λˆ −(ω+1)aˆ . (63)
t,t+j t,t+j t+j t+j
With price indexation, consumer demand in period t+j in an industry x that last changed its
priceinperiodtis
(cid:18)
p (x)P
(cid:19)−θ
t t+j−1
y (x) = Y . (64)
t+j t+j
P P
t+j t−1
Alinearapproximationofthisequationis
j j−1
(cid:88) (cid:88)
yˆ (z) = −θpˆ(x)+θ πˆ −θ πˆ +yˆ . (65)
t,t+j t t+k t+k t+j
k=1 k=0
Pluggingthisintoequation(63)yields
j j−1
(cid:88) (cid:88)
sˆ (x) = −ωθpˆ(x)+ωθ πˆ −ωθ πˆ +ωyˆ −λˆ −(ω+1)aˆ . (66)
t,t+j t t+k t+k t+j t+j t+j
k=1 k=0
Asinthesimplemodelconsideredabove,itisusefultoderivearelationshipbetweenthenatural
level of output and marginal cost and the exogenous shocks in the model. With flexible prices all
firmssetthesameprice. Inthiscasewehavep (x) = µS andsˆ = 0. Thisimpliesthattheflexible
t t t
priceversionofequation(66)is
ωyˆn −λˆn = (ω+1)aˆ . (67)
t+j t+j t+j
60

Combiningequations(66)and(67)yields
j j−1
(cid:88) (cid:88)
sˆ (x) = −ωθpˆ(x)+ωθ πˆ −ωθ πˆ +ω(yˆ −yˆn )−(λˆ −λˆn ). (68)
t,t+j t t+k t+k t+j t+j t+j t+j
k=1 k=0
Wenextlinearizethepricesettingequation—equation(58). Thisyields:
∞ ∞ ∞ j ∞ j−1
(cid:88) (cid:88) (cid:88) (cid:88) (cid:88) (cid:88)
(αβ)jpˆ(x)− (αβ)jE sˆ (x)− (αβ)j E πˆ + (αβ)j E πˆ = 0.
t t t,t+j t t+k t t+k
j=0 j=0 j=1 k=1 j=1 k=0
Manipulationofthisequationyields
∞ ∞ ∞
(cid:88) (cid:88) (cid:88)
pˆ(x) = (1−αβ) (αβ)jE sˆ (x)+αβ (αβ)j−1E πˆ −αβ (αβ)jE πˆ . (69)
t t t,t+j t t+j t t+j
j=0 j=1 j=0
Usingequation(68)toeliminatesˆ (x)inequation(69)andmanipulatingtheresultingequation
t,t+j
yields
∞ ∞ ∞
(cid:88) (cid:88) (cid:88)
pˆ(x) = (1−αβ)ζˆ (αβ)jE [ωxˆ −λˆ ]+αβ (αβ)j−1E πˆ −αβ (αβ)jE πˆ , (70)
t t t+j xt+j t t+j t t+j
j=0 j=1 j=0
whereλˆ = λˆ −λˆn andζˆ= 1/(1+ωθ).
xt t t
A linear approximation of the expression for the price index—equation (31)—in the case with
indexationbetweenpricechangesyields
1−α
πˆ −πˆ = pˆ(x). (71)
t t−1 t
α
Usingthislastequationtoreplacepˆ(x)inequation(70)yields
t
∞ ∞ ∞
(cid:88) (cid:88) (cid:88)
πˆ −πˆ = κζˆ (αβ)jE [ωxˆ −λˆ ]+(1−α)β (αβ)j−1E πˆ −(1−α)β (αβ)jE πˆ .
t t−1 t t+j xt+j t t+j t t+j
j=0 j=1 j=0
Quasi-differencingthisequationyields
(πˆ −πˆ )−αβ(E πˆ −πˆ ) = κζˆ(ωxˆ −λˆ )+(1−α)β(E πˆ −πˆ ),
t t−1 t t+1 t t+j xt+j t t+1 t
whichimplies
∆πˆ = βE ∆πˆ +κζˆ(ωxˆ −λˆ ). (72)
t t t+1 t+j xt+j
61

Finally,werewritethehousehold’sEulerequation—equation(60)intermsofthemarginalutil-
itygap:
λˆ = E λˆ −σ(ˆı −E πˆ −rn), (73)
xt t xt+1 t t t+1 t
wherern denotesthe“naturalrateofinterest”asisgivenby
t
1
rn = E ∆λˆn . (74)
t σ t t+1
H.7 DeterminationofNaturalRateofOutputandProductivity
Sincethemonetaryshockaffectsprivatesectorbeliefsaboutthepathofthenaturalrateofinterest,
it also affects the private sector’s beliefs about the path of the natural rate of output. The solution
tothefollowingequation:
(1+bβ+b2β)yˆn = bβE yˆn +(1+b+b2β)yˆn−byˆn +σ−1ψr¯ (75)
t+1 t t+2 t t−1 c t
using our assumed initial response for the natural rate of output of yn = ψr¯ yields a path for the
0 0
natural rate of output that is consistent with the path of the natural rate of interest implied by our
assumption about Fed information, i.e., rn = ψr¯. This can be verified by using the resulting path
t t
for the natural rate of output to construct a path for the natural rate of marginal utility according
to equation (62) and then plugging the resulting path for the natural rate of marginal utility into
equation(74). Thiswillyieldrn = ψr¯.
t t
The logic for this construction of the path of the natural rate of output is easier to comprehend
inthetextbookNewKeynesianmodelwithouthabit. Supposern = ψr¯ andyn = ψr¯ inthatmodel
t t 0 0
and we are interested in constructing the path for the natural rate of output that is consistent with
theseassumptions. TheconsumptionEulerequationinthatmodelimpliesthatyˆn = E yˆn −σψr¯.
t t t+1 t
For this equation to hold, it must be that yˆn = yˆn + σψr¯. One can thus construct a path for
t+1 t t
the natural rate of output that is consistent with the desired path for the natural rate of interest by
iteratingforwardyˆn = yˆn +σψr¯ withtheinitialconditionyn = ψr¯ . Theargumentabove,isthe
t+1 t t 0 0
equivalentargumentwhenhouseholdshaveinternalhabit.
Given the path for the natural rate of output that we construct above, one can construct a path
for the response of private sector beliefs about productivity (the exogenous shock that we assume
isdrivingvariationinthenaturalrateofoutputandthenaturalrateofinterest)byusingequation
(67). Inthecounterfactual, weassumethatagentsbelieveproductivityisarandomwalkandthen
feed in a shock process for productivity that makes productivity follow the same path as in the
62

actualcaseofthemonetaryshock.
63

TABLE A.1
TableRAe.s1p:oRnsees poof nInsteeroefstI nRtaetreess ttoR tahtee PsotloicMy Noneewtsa rSyhoSchko cfokrs DfoifrfeDreifnfte SreanmtpSlae mPeprlieodPseriods
Baseline Sample Pre-Crisis (2000-2007) Full Sample Baseline w/ Unsched.
Nominal Real Nominal Real Nominal Real Nominal Real
3M Treasury Yield 0.67 0.76 0.73 0.76
(0.14) (0.13) (0.15) (0.11)
6M Treasury Yield 0.85 0.85 0.90 0.91
(0.11) (0.12) (0.12) (0.10)
1Y Treasury Yield 1.00 1.00 1.00 1.00
(0.14) (0.14) (0.13) (0.13)
2Y Treasury Yield 1.10 1.06 1.11 1.04 1.19 1.46 1.30 1.21
(0.33) (0.24) (0.36) (0.24) (0.29) (0.39) (0.37) (0.26)
3Y Treasury Yield 1.06 1.02 1.03 0.97 1.21 1.34 1.26 1.18
(0.36) (0.25) (0.39) (0.25) (0.31) (0.33) (0.40) (0.28)
5Y Treasury Yield 0.73 0.64 0.67 0.58 0.78 0.81 0.69 0.68
(0.20) (0.15) (0.20) (0.15) (0.18) (0.16) (0.16) (0.11)
10Y Treasury Yield 0.38 0.44 0.36 0.44 0.50 0.57 0.38 0.43
(0.17) (0.13) (0.18) (0.13) (0.17) (0.16) (0.13) (0.10)
2Y Tr. Inst. Forward Rate 1.14 0.99 1.07 0.90 1.31 0.97 1.34 1.15
(0.46) (0.29) (0.48) (0.27) (0.38) (0.30) (0.49) (0.31)
3Y Tr. Inst. Forward Rate 0.82 0.88 0.66 0.76 1.14 1.09 1.00 1.03
(0.43) (0.32) (0.43) (0.29) (0.41) (0.35) (0.46) (0.34)
5Y Tr. Inst. Forward Rate 0.26 0.47 0.20 0.47 0.44 0.61 0.27 0.45
(0.19) (0.17) (0.19) (0.16) (0.21) (0.21) (0.13) (0.12)
10Y Tr. Inst. Forward Rate -0.08 0.12 -0.01 0.21 0.05 0.10 -0.07 0.04
(0.18) (0.12) (0.19) (0.13) (0.17) (0.13) (0.12) (0.11)
EachestimatecomesfromaseparateOLSregression.Thedependentvariableineachregressionistheonedaychangeinthevariable
stated in the left-most column. The independent variable is a change in the policy news shock over a 30 minute windor around
regularlyscheduledFOMCannouncements,exceptthelasttwocolumnswhereweincludeunscheduledFOMCannouncements.The
baseline sample period is 1/1/2000 to 3/19/2014, except that we drop July 2008 through June 2009. The "Pre-Crisis" sample is
January 2000 through December 2007. The "Full Sample" is 1/1/2000 to 3/19/2014. In the last two columns, we exclude a 10 day
periodafter9/11/2001. For2Yand3Yyieldsandrealforwards, thesamplestartsin2004. For eachsampleperiod,weconstructthe
policynewshocksfromthesamesampleofobservationsastheregressionsarerunon—thatis,theresultsfromthedifferentsample
periods use slightly different policy news shock series. Robust standard errors are in parentheses.
64

TABLE A.2
ResponsTe aobfl IenAte.r2e:stR Reastpeos nasned tIonfalaFtieodn Ftou na dFsedR FautendSsh Rocakte Shock
Nominal Real Inflation
3M Treasury Yield 0.50
(0.16)
6M Treasury Yield 0.59
(0.10)
1Y Treasury Yield 0.41
(0.16)
2Y Treasury Yield 0.48 0.50 -0.02
(0.32) (0.20) (0.15)
3Y Treasury Yield 0.38 0.41 -0.03
(0.34) (0.19) (0.18)
5Y Treasury Yield 0.11 0.21 -0.10
(0.16) (0.12) (0.09)
10Y Treasury Yield -0.00 0.10 -0.10
(0.12) (0.09) (0.07)
2Y Treasury Inst. Forward Rate 0.29 0.30 -0.01
(0.40) (0.20) (0.25)
3Y Treasury Inst. Forward Rate 0.07 0.13 -0.06
(0.34) (0.19) (0.22)
5Y Treasury Inst. Forward Rate -0.09 0.07 -0.16
(0.13) (0.12) (0.07)
10Y Treasury Inst. Forward Rate -0.11 -0.02 -0.08
(0.16) (0.11) (0.09)
Each estimatecomes from a separate OLS regression. The dependent variable in each regression is
the one day change in the variable stated in the left-most column. The independent variable is a
change in the Fed Funds future over the remainder of the month over a 30 minute window around
the time of FOMC announcements. The sample period is all regularly scheduled meetings from
1/1/2000to3/19/2014,exceptthatwedropJuly2008throughJune2009. For2Yand3Yyieldsand
real forwards, the sample starts in January 2004. The sample size for the 2Y and 3Y yields and
forwards is 74. The samplesize for all other regressions is 106. In all regressions, the policy news
shock is computed from these same 106 observations. Robust standard errors are in parentheses.
65

TABLE A.3
Response of Interest Rates and Inflation to the Policy News Shock
TableA.3: ReRspigoonbsoens'st oHPetoelriocsykeNdeawstisciSthy-oBcakseUds EinsgtimRaigtoorbonEstimator
Nominal Real Inflation
3M Treasury Yield 0.69
(0.15)
6M Treasury Yield 0.85
(0.12)
1Y Treasury Yield 0.98
(0.15)
2Y Treasury Yield 1.07 1.03 0.05
(0.37) (0.29) (0.20)
3Y Treasury Yield 1.03 0.99 0.04
(0.42) (0.30) (0.19)
5Y Treasury Yield 0.69 0.62 0.07
(0.22) (0.16) (0.12)
10Y Treasury Yield 0.34 0.42 -0.08
(0.19) (0.14) (0.09)
2Y Treasury Inst. Forward Rate 1.10 0.96 0.14
(0.51) (0.34) (0.25)
3Y Treasury Inst. Forward Rate 0.78 0.86 -0.08
(0.49) (0.37) (0.17)
5Y Treasury Inst. Forward Rate 0.22 0.46 -0.24
(0.20) (0.18) (0.09)
10Y Treasury Inst. Forward Rate -0.12 0.11 -0.22
(0.19) (0.13) (0.10)
Each estimate comes from a separate "regression." The dependent variable in each regression is the one day
change in the variable stated in the left-most column. The independent variable is a change in the policy news
shock over a 30 minute window around the time of FOMC announcements. All results are based on Rigobon's
(2003) method of identification by heteroskedasticity. The sampleof "treatment"days for the Rigobon method is
all regularly scheduled FOMC meeting days from 1/1/2000 to 3/19/2014—this is also the period for which the
policynewsshockisconstructedinall"regressions." Thesampleof"control"daysfortheRigobonanalysisisall
Tuesdays and Wednesdays that are not FOMC meeting days over the sameperiod of time.In both the treatment
and control samples, we drop July 2008 through June 2009 and 9/11/2001-9/21/2001. For 2Y forwards, the
sample starts in January 2004. Standard errors are calculated using a non-parametric bootstrap with 5000
iterations.
66

TABLE A.4
TableAB.4re:aBkreevaekne IvneflnatIinofln avteirosnusv IenrfsluatsioInn flSawtaiopns Swaps
Breakeven Swaps
Inflation Over Next 2 Years -0.02 0.37
(0.18) (0.35)
Inflation Over Next 3 Years -0.03 0.41
(0.17) (0.32)
Inflation Over Next 5 Years -0.13 -0.02
(0.14) (0.15)
Inflation Over Next 10 Years -0.22 -0.17
(0.12) (0.16)
Each estimatecomesfrom a separate OLS regression. The dependent variable in each regression is
theonedaychangeinexpectedinflationmeasuredeitherbybreakeveninflationfromthedifference
between nominal Treasuries and TIPS (first column) or from inflation swaps (second column) for
the period stated in the left-most column. The independent variable is a change in the policy new
shock over a 30 minutewindow around the timeof FOMC announcements, where the policy news
shocks are constructed on the 2000-2014 sample used in Table 1. The sample is all regularly
scheduledFOMCmeetingdayfrom1/1/2005to11/14/2012,exceptthatwedropJuly2008through
June 2009. Robust standard errors are in parentheses.
67

TABLE A.5
TableAR.e5s:pRoensspe oonf sEexopfecEtxepd eOctuetpduOt GutrpowutthGrowth
Exp. Output Growth in Current Qr 1.38
(0.72)
Exp. Output Growth 1 Qr Ahead 1.56
(0.54)
Exp. Output Growth 2 Qr Ahead 0.66
(0.37)
Exp. Output Growth 3 Qr Ahead 0.82
(0.27)
Exp. Output Growth 4 Qr Ahead 0.51
(0.25)
Exp. Output Growth 5 Qr Ahead 0.54
(0.28)
Exp. Output Growth 6 Qr Ahead 0.48
(0.25)
Exp. Output Growth 7 Qr Ahead 0.90
(0.57)
Each estimate comes from a separate OLS regression. We regress changes in survey expectations
from the Blue Chip Economic Indicators on the policy news shock. Since the Blue Chip survey
expectationsareavailableatamonthlyfrequency,weconstructa corresponding monthlymeasureof
ourpolicynewsshock.Inparticular,weuseanypolicynewsshockthatoccursoverthemonthexcept
forthosethatoccurinthefirstweek(becausewedonotknowwhethertheseoccurredbeforeorafter
the surveyresponse). The dependent variable is the changein the forecasted value of output growth
N quarters ahead, between this month'ssurveyand last month'ssurvey.See Appendix F for details.
The sample period is all regularly scheduled FOMC meetingsbetweenJanuary 1995 to April 2014,
except that we drop July 2008 through June 2009 and the aforementioned first-weekmeetings.The
policy newsshock is constructed on the same sample period. Sample sizes are 120 for the first five
rows, then 75, 45, and 13. Robust standard errors are in parentheses.
68

References
ABRAHAMS, M., T. ADRIAN, R. K. CRUMP, AND E. MOENCH (2015): “Decomposing Real and
NominalYieldCurves,”JournalofMonetaryEconomics,84,182–200.
ANDRADE, P., G. GABALLO, E. MENGUS, AND B. MOJON (2016): “ForwardGuidanceandHetero-
geneousBeliefs,”WorkingPaper,BanquedeFrance.
BARAKCHIAN, S. M., AND C. CROWE(2013): “MonetaryPolicyMatters: NewEvidenceBasedona
NewShockMeasure,”JournalofMonetaryEconomics,60,950–966.
BEECHEY, M. J., B. K. JOHANNSEN, ANDA. T. LEVIN(2011): “AreLong-RunInflationExpectations
AnchoredMoreFirmlyintheEuroAreaThanintheUnitedStates?,” AmericanEconomicJournal:
Macroeconomics,3(2),104–129.
BEECHEY, M. J., AND J. H. WRIGHT (2009): “The High-Frequency Impact of News on Long-Term
YieldsandForwardRates: IsItReal?,”JournalofMonetaryEconomics,56,535–544.
BERKELMANS, L. (2011): “Imperfect Information, Multiple Shocks, and Policy’s Signaling Role,”
JournalofMonetaryEconomics,58(4),373–386.
BERNANKE, B. S., J. BOIVIN, AND P. ELIASZ (2005): “Measuring the Effects of Monetary Policy:
A Factor-Augmented Vector Autoregressive (FAVAR) Approach,” Quarterly Journal of Economics,
120(1),387–422.
BERNANKE, B. S., AND K. N. KUTTNER (2005): “What Explains the Stock Market’s Reaction to
FederalReservePolicy,”JournalofFinance,60(3),1221–1257.
CALVO, G. A. (1983): “Staggered Prices in a Utility-Maximizing Framework,” Journal of Monetary
Economics,12,383–398.
CAMPBELL, J. R., C. L. EVANS, J. D. FISHER, AND A. JUSTINIANO (2012): “MacroeconomicEffects
ofFederalReserveForwardGuidance,”BrookingsPapersonEconomicActivity,2012(1),1–80.
CARLSTROM, C. T., T. S. FUERST, AND M. PAUSTIAN (2015): “InflationandOutputinNewKeyne-
sianModelaTransientInterestRatePeg,”JournalofMonetaryEconomics,76,230–243.
CHRISTIANO, L. J., M. EICHENBAUM, AND C. L. EVANS (1999): “Monetary Policy Shocks: What
Have We Learned and to What End?,” in Handbook of Macroeconomics, ed. by J. B. Taylor, and
M.Woodford,pp.65–148,Amsterdam,Holland.Elsevier.
(2005): “NominalRigiditiesandtheDynamicEffectsofaShocktoMonetaryPolicy,”Journal
ofPoliticalEconomy,115,1–45.
COCHRANE, J. H.(2005): AssetPricing.PrincetonUniversityPress,Princeton,NJ,secondedn.
COCHRANE, J. H., AND M. PIAZZESI (2002): “TheFedandInterestRates: AHigh-FrequencyIden-
tification,”AmericanEconomicReview,92(2),90–95.
COOK, T., ANDT.HAHN(1989): “TheEffectofChangesintheFederalFundsRateTargetonMarket
InterestRatesinthe1970s,”JournalofMonetaryEconomics,24(3),331–351.
69

CUKIERMAN, A., AND A. H. MELTZER (1986): “A Theory of Ambiguity, Credibility, and Inflation
underDiscretionandAsymmetricInformation,”Econometrica,54(5),1099–1128.
ELLINGSEN, T., AND U. SODERSTROM(2001): “MonetaryPolicyandMarketInterestRates,”Ameri-
canEconomicReview,91(5),1594–1607.
FAUST, J., E. T. SWANSON, AND J. H. WRIGHT(2004): “DoFederalReservePolicySurprisesReveal
SuperiorInformationabouttheEconomy?,”ContributionstoMacroeconomics,4(1),1–29.
FIELLER, E. (1954): “Some Problems in Interval Estimation,” Journal of the Royal Statistical Society.
SeriesB(Methodological),16(2),175–185.
FLECKENSTEIN, M., F. A. LONGSTAFF, AND H. LUSTIG (2014): “The TIPS-Treasury Bond Puzzle,”
JournalofFinance,69,2151–2197.
FRANKEL, A., AND N. KARTIK (2017): “WhatKindofCentralBankCompetence?,”TheoreticalEco-
nomics,forthcoming.
GAGNON, J., M. RASKIN, J. REMACHE, AND B. SACK (2011): “Large-Scale Asset Purchases by the
FederalReserve: DidTheyWork?,”FederalReserveBankofNewYorkEconomicPolicyReview,May,
41–59.
GALI, J. (2008): MonetaryPolicy,Inflation,andtheBusinessCycle.PrincetonUniversityPress,Prince-
ton,NJ.
GERTLER, M., AND P. KARADI (2015): “Monetary Policy Surprises, Credit Costs, and Economic
Activity,”AmericanEconomicJournal: Macroeconomics,7(1),44–76.
GILCHRIST, S., D. LOPEZ-SALIDO, AND E. ZAKRAJSEK (2015): “MonetaryPolicyandRealBorrow-
ingCostsattheZeroLowerBound,”AmericanEconomicJournal: Macroeconomics,7(1),77–109.
GU¨RKAYNAK, R. S., A. LEVIN, AND E. SWANSON (2010): “Does Inflation Targeting Anchor Long-
Run Inflation Expectations? Evidence from the US, UK and Sweden,” Journal of the European
EconomicAssociation,8(6),1208–1242.
GURKAYNAK, R. S., B. SACK, ANDE. T. SWANSON(2005): “DoActionsSpeakLouderThanWords?
TheResponseofAssetPricestoMonetaryPolicyActionsandStatements,”InternationalJournalof
CentralBanking,1,55–93.
(2007): “Market-Based Measures of Monetary Policy Expectations,” Journal of Business and
EconomicStatistics,25(2),201–212.
GURKAYNAK, R. S., B. SACK, AND J. H. WRIGHT (2010): “The TIPS Yield Curve and Inflation
Compensation,”AmericanEconomicJournal: Macroeconomics,2(1),70–92.
HANSEN, B. E. (1999): “The Grid Bootstrap and the Autoregressive Model,” Review of Economics
andStatistics,81(4),594–607.
HANSON, S. G., AND J. C. STEIN (2015): “Monetary Policy and Long-Term Real Rates,” Journal of
FinancialEconomics,115(3),429–448.
KRISHNAMURTHY, A., AND A. VISSING-JORGENSEN (2011): “TheEffectsofQuantitativeEasingon
InterestRates: ChannelsandImplicationsforPolicy,”BrookingsPapersonEconomicActivity,2011,
215–265.
70

KUTTNER, K. N. (2001): “Monetary Policy Surprises and Interest Rates: Evidence from the Fed
FundsFuturesMarket,”JournalofMonetaryEconomics,47,523–544.
LOH, R. K., AND R. M. STULZ(2011): “WhenAreAnalystRecommendationChangesInfluential?,”
ReviewofFinancialStudies,24(2),593–627.
MAVROEIDIS, S., M. PLAGBORG-MOLLER, AND J. H. STOCK (2014): “Empirical Evidence on In-
flation Expectations in the New Keynesian Phillips Curve,” Journal of Economic Literature, 52(1),
124–188.
MCKAY, A., E. NAKAMURA, AND J. STEINSSON (2016): “The Power of Forward Guidance Revis-
ited,”AmericanEconomicReview,106(10),3133–3158.
MELOSI, L. (2017): “Signaling Effects of Monetary Policy,” Review of Economic Studies, 84(2), 853–
884.
PIAZZESI, M., AND E. T. SWANSON (2008): “FuturePricesasRisk-AdjustedForecastsofMonetary
Policy,”JournalofMonetaryEconomics,55,677–691.
RIGOBON,R.(2003): “IdentificationthroughHeteroskedasticity,”TheReviewofEconomicsandStatis-
tics,85(4),777–792.
RIGOBON, R., AND B. SACK (2004): “The Impact of Monetary Policy on Asset Prices,” Journal of
MonetaryEconomics,51,1553–1575.
ROMER,C.D.,ANDD.H.ROMER(2000): “FederalReserveInformationandtheBehaviorofInterest
Rates,”AmericanEconomicReview,90(3),429–457.
(2004): “A New Measure of Monetary Shocks: Derivation and Implications,” American
EconomicReview,94(4),1055–1084.
ROSA, C. (2012): “How“Unconventional”AreLarge-ScaleAssetPurchases? TheImpactofMone-
taryPolicyonAssetPrices,”FederalResrveBankofNewYorkStaffReportNo.560.
ROTEMBERG, J. J., AND M. WOODFORD (1997): “An Optimization-Based Econometric Frame-
work for the Evaluation of Monetary Policy,” in NBER Macroeconomics Annual 1997, ed. by B. S.
Bernanke,andJ.J.Rotemberg,pp.297–346,Cambridge,MA.MITPress.
RUDEBUSCH, G. D. (1998): “Do Measures of Monetary Policy in a VAR Make Sense,” International
EconomicReview,39(4),907–931.
SCHMITT-GROHE´,S.,ANDM.URIBE(2012): “What’sNewsinBusinessCycles,”Econometrica,80(6),
2733–2764.
SIMS, C. A. (2001): “Solving Linear Rational Expectations Model,” Journal of Computational Eco-
nomics,20,1–20.
STAIGER, D. O., J. H. STOCK, AND M. W. WATSON (1997): “HowPreciseAreEstimatesoftheNat-
ural Rate of Unemployment,” in Reducing Inflation: Motivation and Strategy, ed. by C. D. Romer,
andD.H.Romer,pp.195–246,Chicago,IL.UniversityofChicagoPress.
TANG, J.(2015): “UncertaintyandtheSignalingChannelofMonetaryPolicy,”WorkingPaper,Fed-
eralReserveBankofBoston.
71

WOODFORD, M.(2003): InterestandPrices.PrincetonUniversityPress,Princeton,NJ.
WRIGHT, J. H. (2012): “What Does Monetary Policy Do to Long-Term Interest Rates at the Zero
LowerBound,”EconomicJournal,122,F447–F466.
72