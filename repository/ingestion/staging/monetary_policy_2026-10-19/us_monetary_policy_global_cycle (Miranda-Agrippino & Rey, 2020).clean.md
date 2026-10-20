US Monetary Policy and
the Global Financial Cycle
Silvia Miranda-Agrippino∗ H´el`ene Rey†
Bank of England London Business School
CEPR and CfM(LSE) CEPR and NBER
Revised March 28, 2020
Abstract
US monetary policy shocks induce comovements in the international financial
variables that characterize the ‘Global Financial Cycle.’ A single global factor that
explains an important share of the variation of risky asset prices around the world
decreases significantly after a US monetary tightening. Monetary contractions in
the US lead to significant deleveraging of global financial intermediaries, a decline
in the provision of domestic credit globally, strong retrenchments of international
credit flows, and tightening of foreign financial conditions. Countries with floating
exchange rate regimes are subject to similar financial spillovers.
Keywords: Monetary Policy; Global Financial Cycle; International spillovers; Identifica-
tion with External Instruments
JEL Classification: E44, E52, F33, F42
∗Monetary Analysis, Bank of England, Threadneedle Street, London EC2R 8AH, UK.
†Department of Economics, London Business School, Regent’s Park, London NW1 4SA, UK.
A former version of this paper was circulated under the title “World Asset Markets and the Global Financial Cy-
cle”. We are very grateful to the Editor Veronica Guerrieri and to four anonymous referees for helpful suggestions
that greatly helped improve the paper. We also thank our discussants John Campbell, Marcel Fratzscher and Refet
Gu¨rkaynak as well as Stefan Avdjiev, Ben Bernanke, Kristin Forbes, Marc Giannoni, Domenico Giannone, Pierre-Olivier
Gourinchas, Alejandro Justiniano, Matteo Maggiori, Marco del Negro, Richard Portes, Hyun Song Shin, Mark Watson,
Mike Woodford and seminar participants at the NBER Summer Institute, the ECB-BIS Workshop on “Global Liquidity
anditsInternationalRepercussions”,theASSAmeetings,theNewYorkFed,CREIBarcelona,BankofEngland,Sciences
Po, LBS, Harvard and Princeton for comments. Rey thanks the ERC for financial support (ERC grant 695722). The
views expressed in this paper are those of the authors and do not represent those of the Bank of England or any of its
Committees.

1 Introduction
Observers of balance of payment statistics and international investment positions all
agree: the international financial landscape has undergone massive transformations since
the 1990s. Financial globalization is upon us in a historically unprecedented way, and we
have probably surpassed the pre-WWI era of financial integration celebrated by Keynes
in “The Economic Consequences of the Peace.” At the same time, the role of the United
States as the hegemon of the international monetary system has largely remained un-
changed, and has long outlived the end of Bretton Woods, as emphasized in e.g. Farhi
and Maggiori (2018) and Gourinchas and Rey (2017). The rising importance of cross-
border financial flows and holdings has been documented in the literature.1 What has not
been explored as much, however, are the consequences of financial globalization for the
workings of national financial markets, and for the transmission of US monetary policy
beyond the domestic border. How do international capital flows affect the international
transmission of monetary policy? What are the effects of global banking on fluctuations
in risky asset prices, and on credit growth and leverage in different economies? Using
monthly data since 1980, we study how the existence of a ‘Global Financial Cycle’ (Rey,
2013) shapes the global financial spillovers of US monetary policy.
Monetary policy operates though multiple, complementary channels. In a standard
Keynesian or neo-Keynesian world, output is demand determined in the short-run, and
monetary policy stimulates aggregate consumption and investment (see Woodford, 2003
and Gali, 2008 for classic discussions). In models with frictions in capital markets, ex-
pansionary monetary policy also leads to an increase in the net worth of borrowers, either
financial intermediaries or firms, which in turn boosts lending. This is the credit channel
of monetary policy (Bernanke and Gertler, 1995). Other papers have instead analyzed
the risk-taking channel of monetary policy in which it is the risk profile of financial in-
termediaries that plays a key role, and loose monetary policy relaxes leverage constraints
(Borio and Zhu, 2012; Bruno and Shin, 2015a; Coimbra and Rey, 2017). In this paper, we
exploreempiricallytheinternational transmissionofmonetarypolicythatoccursthrough
financial intermediation and global asset prices, an area that has been largely neglected
1See e.g. Lane and Milesi-Ferretti, 2007 and, for a recent survey, Gourinchas and Rey (2014).

by the literature.2
Using a dynamic factor model, we first document the existence of a unique global
factor in international risky asset prices that explains over 20% of the variance in the
data. With a global Bayesian VAR, we then study the international transmission of US
monetary policy that is mediated through the reaction of asset prices, of global credit and
capital inflows, and of the leverage of financial intermediaries; these are the variables that
characterize the Global Financial Cycle. Our analysis is motivated by the US dollar being
an important funding currency for intermediaries, and by the fact that a large portion
of portfolios worldwide are denominated in dollars.3 We identify US monetary policy
shocks using an external instrument constructed from high-frequency price adjustments
in the federal funds futures market around FOMC announcements, following the lead
of Gu¨rkaynak, Sack and Swanson (2005) and Gertler and Karadi (2015). At the same
time, the use of a rich-information VAR ensures that we control for a wealth of other
shocks, both domestic and international, to which the Fed endogenously reacts, above
and beyond what is anticipated by market participants.4
We find evidence of powerful financial spillovers of US monetary policy to the rest of
the world. When the Federal Reserve tightens, domestic demand contracts, as do prices.
The domestic financial transmission is visible through the rise of corporate spreads, the
contraction of lending, and the sharp fall in the prices of assets, such as housing and the
stock market. But, importantly, we also document significant variations in the Global
Financial Cycle, that is, the shock induces significant fluctuations in financial activity
on a global scale. Risky asset prices, summarized by the single global factor, contract
very significantly. This is accompanied by a deleveraging of global banks both in the
US and Europe, and a surge in aggregate risk aversion in global asset markets. The
supply of global credit contracts, and there is an important retrenchment of international
credit flows that is particularly pronounced for the banking sector. International corpo-
rate bond spreads also rise on impact, and significantly so. These results are consistent
2See Rey (2016), Bernanke (2017) and Jorda, Schularick, Taylor and Ward (2018) for longer discus-
sions.
3For a recent study of the international reserve currency role of the dollar see Farhi and Maggiori
and Stein (2017) the synergies between some of those roles.
4For more detailed discussions see Miranda-Agrippino (2016) and Miranda-Agrippino and Ricco

with a powerful transmission channel of US monetary policy across borders, via financial
conditions. The contraction of domestic credit and international liquidity that follows
the US monetary policy tightening is confirmed also for the subset of countries that have
a floating exchange rate regime.
The importance of international monetary spillovers and of the world interest rate in
drivingcapitalflowshasbeenpointedoutintheclassicworkofCalvoetal.(1996).5 Some
recent papers have fleshed out the role of intermediaries in channeling those spillovers.6
Our empirical results on the transmission mechanism of monetary policy via its impact
on risk premia, spreads, and volatility, are related to those of Gertler and Karadi (2015)
and Bekaert, Hoerova and Duca (2013) obtained in the domestic US context.7 A small
number of papers have analyzed the effect of US monetary policy on leverage and on the
VIX (see e.g. Passari and Rey, 2015; Bruno and Shin, 2015b).8 Using a rich-information
Bayesian VAR permits, we believe for the first time, to jointly evaluate the response of
financial, monetary and real variables, in the US and abroad. Moreover, by relying on an
instrumentalvariablefortheidentificationofUSmonetarypolicyshocks, wecandispense
from making implausible timing restrictions on the response of our variables of interest.
The paper is organized as follows. In Section 2, we estimate a dynamic factor model
on world asset prices and show that one global factor explains a large part of the common
variation of the data. In Section 3, we estimate a Bayesian VAR identified using external
instruments to analyze the interaction between US monetary policy and the Global Fi-
nancial Cycle. Section 4 presents a simple theoretical framework featuring heterogeneous
investors to interpret some of our results (Section 4.1), and microeconomic data on global
5Fratzscher (2012) and Forbes and Warnock (2012) have extended these findings significantly.
6CetorelliandGoldberg(2012)usebalancesheetdatatostudytheroleofglobalbanksintransmitting
liquidity conditions across borders. Using firm-bank loan data, Morais, Peydro and Ruiz (2015) find
that a softening of foreign monetary policy increases the supply of credit of foreign banks to Mexican
firms. Using credit registry data combining firm-bank level loans and interest rates data for Turkey,
Baskaya, di Giovanni, Kalemli-Ozcan and Ulu (2017) show that increased capital inflows, instrumented
by movements in the VIX, lead to a large decline in real borrowing rates, and to a sizeable expansion in
credit supply. They find that the increase in credit creation goes mainly through a subset of the biggest
banks.
7For a discussion on the transmission of unconventional US monetary policy on global risk premia
see Rogers, Scotti and Wright (2018).
8These studies all rely on limited-information VARs (four to seven variables) and on recursive iden-
tification schemes to study the transmission of monetary policy shocks, it is therefore unclear whether
their results survive a more robust identification of monetary policy shocks. The problem of omitted
variables is also an important issue in small scale VARs (see Caldara and Herbst, 2019).

banks to give evidence of their risk-taking behavior (Section 4.2). Section 5 concludes.
Details on data and procedures, and additional results are in Appendices at the end of
the paper.
2 One Global Factor in World Risky Asset Prices
In order to summarize fluctuations in global financial markets we specify a Dynamic
Factor Model for a large and heterogeneous panel of risky asset prices traded around the
globe. The econometric specification, fully laid out in Appendix B, is very general, and
allows for different global, regional and, in some specifications, sector specific factors.9
The panel includes asset prices traded on all the major global markets, a collection of
corporate bond indices, and commodities price series (excluding precious metals). The
geographical areas covered are North America, Latin America, Europe, Asia Pacific, and
Australia, and we use monthly data from 1990 to 2012, yielding a total of 858 different
prices series.10 Despite the heterogeneity of the asset markets considered, we find that
the data support the existence of a single common global factor; moreover, this factor
alone accounts for over 20% of the common variation in the price of risky assets from all
continents.11 The factor is plotted in Figure 1, solid line.
While in this instance we prefer cross-sectional heterogeneity over time length, we are
conscious of the limitations that a short time span may introduce in the VAR analysis
we perform in the next section. To allow more flexibility in that respect, we repeat the
factor extraction on a smaller set, where only the US, Europe, Japan and commodity
prices are included, but the time series go back to 1975. In this case the sample counts
303series. TheestimatedglobalfactorforthelongersampleisthedashedlineinFigure1.
Similar to the benchmark case, for this narrower panel too we find evidence of one global
9AsimilarspecificationhasbeenadoptedbyKoseetal.(2003)andKoseetal.(2012)forrealvariables;
they test the hypothesis of the existence of a world business cycle and discuss the relative importance of
world, region and country specific factors in determining domestic business cycle fluctuations.
10All the details on the construction and composition of the panels, shares of explained variance, and
test and criteria used to inform the parametrization of the model (Table B.2) are reported in Appendix
B. We fit to the data a Dynamic Factor Model (Stock and Watson, 2002a,b; Bai and Ng, 2002; Forni
et al., 2000, among others) where each price series is modelled as the sum of a global, a regional, and an
asset-specific component. All price series are taken at monthly frequency using end of month figures.
11We formally test for the numbers of factors in our large panel of asset prices and find that the data
support one common global factor. Results are reported in Table B.2 in the Appendix.

Figure 1: global factor in risky asset prices
Global Common Factor
100 100
50 50
0 0
−50 −50
−100 −100
1990:2012
1975:2010
11997755 11998800 11998855 11999900 11999955 22000000 22000055 22001100
Note: TheFigureplotstheestimatesoftheglobalfactorforthe1975:2010sample(dottedline)together
with the estimates on the wider, shorter sample 1990:2012 (solid line). Shaded areas denote NBER
recession dates.
factor. In this case, however, the factor accounts for about 60% of the common variation
in the data (see Table B.2). For both samples, factors are obtained via cumulation of
those estimated on the stationary, first-differenced (log) price series, and are therefore
consistently estimated only up to a scale and an initial value (see Bai and Ng, 2004, and
Appendix B).12 As a way of normalization, we rotate the factor such that it correlates
positively with the major stock market indices in our sample, i.e. an increase in the index
is interpreted as an increase in global asset prices.
Figure1showsthatmovementsinthefactorsareconsistentwithboththeUSrecession
periods as identified by the NBER (shaded areas), and with major worldwide events.
The index declines with all the recession episodes but remains relatively stable until
the beginning of the nineties, when a sharp and sustained increase is recorded. The
increase lasts until 1997-1998 when major global events like the Russian default, the
LTCM bailout, the East Asian Crisis and finally the burst of the dot-com bubble reverse
the increasing path. Starting from the beginning of 2003 the index increases again until
the beginning of the third quarter of 2007. At that point, with the collapse of the
12This implies that positive and negative values displayed in the chart do not convey any specific
information per se. Rather, it is the overall shape and the turning points that are of interest.

Figure 2: global factor and volatility indices
0 0
VIX −100 VSTOXX
11999900 22000000 22001100 11999900 22000000 22001100
0 0 50
VFTSE VNKY
11999900 22000000 22001100 11999900 22000000 22001100
Note: Clockwise from top-left panel, the global factor (solid line) together with major volatility indices
(dotted lines): VIX (US), VSTOXX (EU), VNKY (JP) and VFTSE (UK). Shaded grey areas highlight
NBER recession times.
subprime market, the first signals of increased vulnerability in financial markets become
visible. This led to an unprecedented plunge.
Inordertoprovidesomeinterpretationforourestimatedglobalfactor, wenotethatin
a large class of asset pricing models, including in the stylized framework that we present
in Section 4, the common component of risky asset prices is a function of aggregate
volatility, and of the degree of aggregate risk aversion in the market. In particular, in the
simple model of Section 4 with heterogeneous financial intermediaries that differ in their
propensity to take on risk, the evolving distribution of wealth between different types
of intermediaries gives rise to a time-varying degree of aggregate risk aversion. This
interpretation of the factor, as reflecting volatility and aggregate risk aversion, is closely
related to that of indices of implied volatility. In Figure 2 we highlight the comovement
of our factor with the VIX, the VSTOXX, the VFTSE and the VNKY, which represent
the markets included in our sample. These indices capture both the price and quantity
of risk, and hence reflect both expectations about future volatility, and risk aversion.
Because of our chosen normalization, we expect our factor to correlate negatively with

Figure 3: global factor decomposition
Global Realized Variance
1990 1992 1994 1996 1998 2000 2002 2004 2006 2008 2010 2012
3 Aggregate Risk Aversion Proxy
-1
-2
-3
1990 1992 1994 1996 1998 2000 2002 2004 2006 2008 2010 2012
Note: [top panel] Monthly global realized variance measured using daily returns of the MSCI Index.
[bottom panel] Index of aggregate risk aversion calculated as (the inverse of) the residual of the
projection of the global factor onto the realized variance. Shaded grey areas highlight NBER recession
times. Source: Global Financial Data and authors calculations.
the implied volatility indices. Indeed, this is clearly visible in the charts of Figure 2;
the factor and the implied volatility indices display a remarkable common behaviour and
peaks consistently coincide within the overlapping samples.13
Based on the intuition offered by our simple model, we separate the aggregate risk
aversion and volatility components in our global factor. We first estimate a monthly
series of realized global volatility using daily returns of the global MSCI Index.14 Second,
we calculate a proxy for aggregate risk aversion as the inverse of the centred residuals of
the projection of the global factor on the realized variance.15 The results of this exercise
13While the comparison with the VIX is somehow facilitated by the length of the CBOE index, the
same considerations extend to all other indices analyzed. Comparison with other ‘risk indices’ such as
the GZ-spread ofGilchrist and Zakrajˇsek (2012) and theBaa-Aaa corporate bond spread (not reported)
showthattheseindicesalsodisplaysomecommonalities,evenifthesynchronicityisslightlylessobvious.
14Weworkundertheassumptionthatmonthlyrealizedvariancescalculatedsummingoverdailyreturns
provide a sufficiently accurate proxy of realized variance at monthly frequency (see Andersen et al.
15Specifically, the proxy for aggregate risk aversion is recovered from the following regression:
GFAC = α + βln(GRVAR ) + ε , where GFAC is the global factor expressed in log units, and
t t t t
GRVAR istherealizedvarianceoftheglobalMSCIIndex. Theconstructionofourproxyforaggregate
t
risk aversion is modelled along the lines of e.g. Bekaert et al. (2013), that estimate variance risk premia

Figure 4: aggregate capital flows
Portfolio
60 FDI
Debt
50 Bank
-10
1992 1994 1996 1998 2000 2002 2004 2006 2008 2010
Note: Global flows as a percentage of world GDP. Annual moving averages. Source: IFS Statistics.
are summarized in Figure 3. Our monthly measure of global realized variance is in the
top panel, while our index of aggregate risk aversion is in the bottom panel. Interestingly,
the degree of market risk aversion that we recover from this simple decomposition is in
continuous decline between 2003 and 2007. It decreases to very low levels at a time
when volatility was low, global banks were prevalent and may have been the ‘marginal
buyers’ in international financial markets. Indeed, Shin (2012) documents the large and
increasing share of banks in international financial markets over that period and until
2007; subsequently, both as a consequence of the crisis and of the changes in regulation,
their relative importance has declined. For illustrative purposes, we report data relative
todifferenttypesofcapitalflowsasapercentageofworldGDPinFigure4, andwefurther
explore the connection between the sharp increase in banking flows and the decline in
global risk aversion in Section 4. After end-2007, aggregate risk aversion starts increasing
to jump sharply during the financial crisis and the bankruptcy of Lehman Brothers, and
remains persistently at high levels.
In more complex models than the one reported in Section 4, the common component
of asset prices is not only a function of realized variances and of risk aversion but also
asthedifferencebetweenameasureoftheimpliedvariance(thesquaredVIX)andanestimatedphysical
expected variance, which is primarily a function of realized volatilities.

of discount rates and of expected cash-flow growth. We explore this more general case
in detail in Appendix E and show that this alternative specification delivers an index of
aggregate risk aversion very similar to our baseline index in Figure 3.16
3 US Monetary Policy and Global Financial Cycle
With the US dollar being the currency of global banking, monetary actions in the US may
directly influence the Global Financial Cycle (GFC) by altering the cost of funding for
major global banks, and hence their leverage decisions. US monetary policy also affects
the pricing of dollar assets, both in the US and abroad, through a direct discount rate
channel and/or by changing the type of marginal investors in international asset mar-
kets.17 Furthermore, monetary conditions of the centre country can also be transmitted
through cross-border capital flows, or through the internal pricing of liquidity by global
banks, and influence the provision of credit outside US borders (see the corroborative
evidence in Morais et al., 2015 for Mexico, and in Baskaya et al., 2017 for Turkey).
To study the effects of US monetary policy on the GFC, we use rich-information
VARs that provide us with a unique framework to analyze the transmission of monetary
policy beyond national borders.18 There are a number of advantages that come with
this choice. Most obviously, relying on a unique specification permits addressing the
effects of US monetary policy on the GFC against the background of the response of
the domestic business cycle. This acts both as a complement to the analysis, and as a
disciplining device to ensure that the identified shock is in fact inducing responses that
do not deviate from the standard channels of domestic monetary transmission. Moreover,
the dimensionality and composition of the set of variables included in the VAR greatly
reduce the problem of omitted variables that generally plagues smaller systems and is
16Precisely, we extract risk aversion by projecting the factor on realized variances, on discount rates
in the US, Germany, the UK and Japan, and on survey forecasts for output growth 12-month-ahead in
the same four countries in order to proxy for expected cash flow growth. Results are very similar. For
thorough discussions on estimation of price of risk versus quantity of risk, see Bekaert et al. (2019) and
Zhou(2018). WealsoconsiderinAppendixEotherindicesofriskaversionthathavebeenindependently
developed in the literature, and show our results carry through regardless of the particular proxy used.
17Security-levelevidenceprovidedbySchregeretal.(2017)showsthatfirmswhofinancethemselvesin
dollars are by and large the only ones able to attract a worldwide investors base. For a model where low
funding costs lower aggregate effective risk aversion and increase leverage see Coimbra and Rey (2017).
18Technical details on priors and estimation of the Bayesian VAR are reported in Appendix C.

likely to invalidate the identification of the structural shocks.19
We start by looking at how US monetary policy affects domestic real and financial
conditions in a ‘closed economy VAR’. Then, we augment a small set of core domestic
variables with those that characterize the GFC; namely, global credit and capital inflows,
the global factor in asset prices and risk aversion, and the leverage of US and European
global banks. In this first version of our empirical framework, global variables are world
aggregates, and bundle together countries with different exchange rate regimes. To eval-
uate to what extent a floating exchange rate can provide some insulation against foreign
shocks, we then repeat the analysis by specifically focusing only on the subset of ‘floaters’,
following the IMF’s de-facto classification.
3.1 Identification of US Monetary Policy Shocks
We identify US monetary policy shocks using an external instrument (Stock and Watson,
2012,2018;MertensandRavn,2013). Theintuitionbehindthisapproachtoidentification
is that the mapping between the VAR innovations and the structural shock of interest
can be estimated using only moments of observables, provided that a valid instrument for
such shock exists. The contemporaneous transmission coefficients are a function of the
regression coefficients of the VAR residuals onto the instrument, up to a normalization.
Hence,giventheinstrument,thismethodensuresthatwecanisolatethecausaleffectsofa
US monetary policy shock on the dynamics of our large set of variables without imposing
any timing restrictions on the responses. Intuitively, if the instrument correlates with
the VAR innovations only via the contemporaneous monetary policy shocks, a projection
of the VAR innovations on the instrument isolates variations in the variables which are
solely due to this shock (Miranda-Agrippino and Ricco, 2018).
The crucial step of this identification strategy is, naturally, the choice of the instru-
ment. We rely on high-frequency movements in federal funds futures markets around
FOMC announcements to identify the monetary policy shocks, following the lead of
19Ban´buraetal.(2010)showthatamedium-scaleVARofcomparablesizeandcompositiontotheone
usedinthispaperisabletocorrectlyrecovertheshocksandreproduceresponsesthatmatchtheoretical
ones. Intuitively, the large degree of comovement among macroeconomic variables makes it possible for
VARs of such size to effectively summarize the information contained in large VARs typically counting
over hundred variables.

Gu¨rkaynak et al. (2005) and Gertler and Karadi (2015). Specifically, we use 30-minutes
price revisions (or surprises) around FOMC announcements in the fourth federal funds
futures contracts (FF4), and we construct a monthly instrument by summing up the
high-frequency surprises within each month. Because these futures have an average ma-
turity of three months, the price revision that surrounds the FOMC monetary policy
announcements captures revisions in market participants expectations about the future
monetary policy stance up to a quarter ahead. As observed in Miranda-Agrippino (2016)
and Miranda-Agrippino and Ricco (2017), market-based monetary surprises such as the
ones we use map into the shocks only under the assumption that market participants
can correctly and immediately disentangle the systematic component of policy from any
observable policy action. In the presence of information asymmetries, the high-frequency
surprises are also a function of the information about economic fundamentals that the
central bank implicitly discloses at the time of the policy announcements.20 Failure to
account for this effect may hinder the correct identification of the shocks, resulting in
severe price and real activity puzzles, particularly in small VARs. Here we address this
issue by relying on the rich information in our VARs. The information set in our VARs
controls for a wealth of other shocks, both domestic and international, to which the
Fed endogenously reacts, and allows identification of monetary policy shocks above and
beyond what is expected by market participants.
In Table 1, we report first stage IV statistics of the projection of the VAR innovation
for the policy interest rate (1 year rate in our case) on our instrument (FF4). For
comparison, we also include first-stage statistics obtained with the narrative instrument
of Romer and Romer (2004), that we have extended up to the end of 2007 (MPN). A
fist-stage F statistic below 10 is an indication of potentially weak instruments (Stock
et al., 2002). The three VARs in the table are (1) a closed economy 13-variable VAR that
includes only US variables; (2) a global 15-variable VAR that includes GFC variables as
world aggregates; (3) and a global 15-variable VAR that focuses on the subset of countries
with floating exchange rates.21
20This implicit disclosure of information is referred to as the Fed information effect in Nakamura and
Steinsson (2018), and the signalling channel of monetary policy in Melosi (2017). The concept is similar
totheDelphiccomponentofforwardguidanceannouncementsinCampbell,Evans,FisherandJustiniano
21All VARs are monthly and estimated with 12 lags over the sample 1980-201. Details on the compo-

Table 1: Tests for Instruments Relevance
Domestic VAR (1) F-stat 90% posterior ci reliability 90% posterior ci
Global VAR (2)
Global VAR (3)
Note: First-stage F statistics, statistical reliability and 90% posterior coverage intervals. Candidate
instruments are surprises in the three-months-ahead (FF4) federal fund futures and an extension to
the narrative instrument of Romer and Romer (2004) up to 2007. VAR innovations are from monthly
BVAR(12) estimated from 1980 to 2010. First-stage regressions are run on the overlapping sample
between the VAR innovations and each instrument.
Results in Table 1 show that in a domestic context either instrument attains satisfac-
tory levels of relevance. As we discuss in the next subsection, the two instruments also
retrieve relatively similar dynamic responses to a monetary policy shock in the domestic
VAR. The relevance of the narrative series deteriorate dramatically in both open econ-
omy global VARs with F statistics dropping well below 10. In contrast, the first stage
IV statistics associated to the high-frequency based identification are only marginally
altered in the three cases. This confirms the strong informative content of our preferred
instrument.22
3.2 The International Transmission of US Monetary Policy through
the Global Financial Cycle
We present our results in the form of dynamic responses to a US monetary policy shock
that is normalized to increase the policy rate by 1% on impact. We use the 1-year rate as
monetary policy variable; this, coupled with the 3-month horizon embedded in the exter-
nal instrument implies that we capture standard monetary policy shocks that affect the
sition of each VAR are reported in Table 2 in the next subsection.
22AnotherpaperusinghighfrequencyexternalinstrumentsfortheidentificationofUSmonetarypolicy
shocks and their effects on financial markets is Ha (2016).

Table 2: Variables in VARs
VariableName Source Model
(1) (2) (3) (4) (5) (6)
CapacityUtilization FRED-MD •
UnemploymentRate FRED-MD •
HousingStarts FRED-MD •
CPIAll FRED-MD •
TermSpread(10Y-1Y) FRED-MD •
GZExcessBondPremium GilchristandZakrajˇsek(2012) •
MortgageSpread GertlerandKaradi(2015) •
HousePriceIndex Shiller(2015) •
S&P500 FRED-MD •
GlobalRealEconomicActivityExUS BaumeisterandHamilton(2019)&OC • • • •
GlobalDomesticCredit IMF-IFS∗ • •
GlobalDomesticCreditExUS IMF-IFS∗ •
USTotalNonrevolvingCredit FRED-MD • •
GlobalInflowsAllSectors BIS∗ • •
GlobalInflowstoBanks BIS∗ •
GlobalInflowstoNon-Banks BIS∗ •
FloatersDomesticCredit BIS∗ • •
FloatersInflowsAllSectors BIS∗ •
FloatersInflowstoBanks BIS∗ •
FloatersInflowstoNon-Banks BIS∗ •
GZCreditSpread GilchristandZakrajˇsek(2012) • • •
LeverageUSBrokers&Dealers FRBFlowofFunds∗ • • • •
LeverageEUGlobalBanks Bankscope∗ • • • •
LeverageUSBanks Bankscope∗ • • • •
LeverageEUBanks Bankscope∗ • • • •
FTSEAllShares GlobalFinancialData •
GBPto1USD GlobalFinancialData •
UKCorporateSpread GlobalFinancialData&OC •
UKPolicyRate BankofEngland •
DAXIndex GlobalFinancialData •
EURto1USD GlobalFinancialData •
GERCorporateSpread GlobalFinancialData&OC •
ECBPolicyRate GlobalFinancialData&OC •
Figures 5 6,7,8 7 9 10
D.1 D.3 D.4 D.5 D.7
D.2
Note: The table lists the variables included in the baseline domestic and global BVARs. Models cor-
respond to (1) domestic VAR; (2) & (3) global VARs with world aggregates for GFC; (4) & (5) global
VAR on subset of countries with a floating exchange rate; (6) global VAR with focus on UK and EA
monetary policy and financial conditions. Variables enter the VARs in (log) levels with the exception of
interestratesandspreads. OCdenotesowncalculations,∗ denotesmonthlyinterpolationofthequarterly
original variables.
fedfundsrate, butalsoimplicitandexplicitFedcommunicationandactionsthataffectin-
terest rates at longer maturities. All VARs are estimated using standard macroeconomic
priors, with 12 lags at monthly frequency over the sample 1980:1 - 2010:12. Following
Mertens and Ravn (2013) and Gertler and Karadi (2015), the identification step (i.e. the
projection of the VAR innovations on the instrument) is run over the common sample
sets of IRFs are reported in Appendix D. The variables that we include in our baseline
VARs are listed in Table 2, together with the composition of all the VARs we estimate
for the results collected in the reminder of the section. Details on the construction of the
23In the appendix we report IRFs from a VAR also estimated from 1990:01 for comparison.

data are reported in the Appendix that also collects robustness tests. We report median
IRFs together with 68% and 90% posterior coverage bands.
Domestic Responses We start our empirical exploration by looking at the response of
thedomesticfinancialmarketsandmacroeconomicaggregates. Togivefurthermotivation
for the choice of our instrument, Figure 5 compares the IRFs obtained with the high-
frequency IV (FF4, solid lines) and the narrative IV (MPN, dashed lines). The VAR is
the same in the two cases.
A contractionary monetary policy shock depresses prices and economic activity in line
withthestandardtransmissionchannels. Productionandcapacityutilizationcontract, as
do housing investments, while the unemployment rate rises significantly; these effects are
not sudden, but build up over the horizons. Similarly, prices adjust downward. We note
here that the MPN IV recovers responses that display a pronounced price puzzle. This is
in contrast to our preferred identification: following an initial downward revision, prices
continue to slide into negative territory, consistent with the presence of price rigidities.
The shock also has important consequences for domestic financial markets. The mone-
tary tightening at the short end decreases the term spread and induces a sudden rise in
the excess bond premium variable of Gilchrist and Zakrajˇsek (2012) that measures cor-
porate bond spreads net of default considerations. The response also implies increased
costs of funding in the corporate market, and provides evidence of a powerful financial
amplification mechanism of monetary policy shocks that operates at the domestic level.
Expectations of lower economic activity and changes in discount rate are immediately
priced-in in the stock market that registers a strong and sudden drop. Household finance
also deteriorates substantially, with house prices falling and mortgage spreads increasing
significantly.24 Finally, the monetary contraction results in a significant appreciation of
the dollar against a basket of foreign currencies.
The system of domestic dynamic responses highlights a powerful transmission of mon-
etarypolicyshocksthroughthedomesticfinancialmarkets. Inthereminderofthissection
we will explore how monetary policy shocks spill over across borders through their effect
on global financial conditions.
24We use the 30-year conventional mortgage spread calculated in excess of the 10-year government
bond rate. We take this variable from Gertler and Karadi (2015).

Figure 5: responses of domestic business & financial cycle
Industrial Production Capacity Utilization Unemployment Rate
0.5 0.6
0 0.4
s
t n i -1 -0.5 0.2
o
p
%-2 -1 0
-1.5
-3 -0.2
Housing Starts CPI All PCE Deflator
0.5
s 5 0 0
t
n i o 0 -0.5 -0.5
p
-5
% -1
-10 -1
-1.5
1Y Treasury Rate Term Spread 10Y-1Y BIS Real EER
1 0.4 5
0.2 4
n
i o -0.2 2
p
0 -0.4 1
%
-0.6 0
-0.5 -0.8 -1
GZ Excess Bond Premium Mortgage Spread House Price Index
0.8
0.6 0.4
s -1
t n 0.4 0.2
i o -2
p 0.2
% 0 -3
-0.2 -4
-0.2
S&P 500
s
t
n i -5
o
p
%-10 FF4
NARRATIVE
-15
horizon
Note: Closed economy responses to a contractionary US monetary policy shock that induces a 1%
increase in the policy rate. [blue solid lines and grey areas] IV is the surprise in FF4 contracts,
68% & 90% posterior coverage bands. [green dashed lines and yellow areas] IV is an extension
of the narrative series of Romer and Romer (2004), 68% & 90% posterior coverage bands.
Global Financial Cycle: World Aggregates We start by analyzing the responses
of global asset markets, as summarized by the global factor in risky asset prices, and the

implied degree of aggregate risk aversion estimated in Section 2.25 Second, we move on to
study the responses of global domestic credit and international capital flows. Our global
credit variables are world aggregates that encompass countries with different exchange
rate regimes.26 Global inflows are defined as direct cross-border credit flows provided by
foreign banks to both banks and non-banks in the recipient country (see Avdjiev et al.,
2012). Finally, we look at banks’ leverage. Here we separate US brokers/dealers and
European global banks from the aggregate banking sector, due to their different risk tak-
ing behavior. Data for credit, international inflows, and leverage are originally available
at quarterly frequency (see data Appendix). We convert them to monthly frequency by
interpolation.27 Full sets of responses are collected in Figures D.1 to D.3 in the Appendix.
Results are robust to starting the estimation sample in January 1990.
A contractionary US monetary policy shock impacts global asset markets (Figure 6).
Upon realization of the monetary contraction, global risky asset prices, as summarized
by the global factor, contract abruptly. While the factor has no meaningful measurement
unit, we can quantify the effects on global stock markets by looking at its contribution
to the overall fluctuations in the major indices. The factor explains about 20% of the
common variation in our panel of international asset prices. If we assume that all asset
prices loaded equally on the factor, the 40% impact fall would roughly translate into a
8% impact decrease in the local stock market. This number is consistent with both the
response of the local US stock market (Figure 5), and European markets discussed at the
end of the section (Figure 10). Aggregate risk aversion – i.e. the component of our factor
25The responses of alternative measures of risk aversion, including one that controls for discount rates
and expected output (cash-flows) growth are collected in Figure E.3 in the Appendix.
26The countries included in our study are Argentina, Australia, Austria, Belarus, Belgium, Bolivia,
Brazil, Bulgaria, Canada, Chile, Colombia, Costa Rica, Croatia, Cyprus, Czech Republic, Denmark,
Ecuador, Finland, France, Germany, Greece, Hong Kong, Hungary, Iceland, Indonesia, Ireland, Italy,
Japan, Latvia, Lithuania, Luxembourg, Malaysia, Malta, Mexico, Netherlands, New Zealand, Norway,
Poland, Portugal, Romania, Russia, Serbia, Singapore, Slovakia, Slovenia, South Africa, South Korea,
Spain, Sweden, Switzerland, Thailand, Turkey, United Kingdom and the United States.
27The quarterly level data are interpolated using a shape-preserving piecewise cubic interpolation;
MatLab command: y1 = interp1(t0,y0,t1,‘pchip’);. Original quarterly and interpolated monthly
data used in the paper are made available in the Supporting Material accompanying the paper. Results
computed using alternative monthly variables (private sector liquidity instead of IMF-IFS domestic
credit, and cross-border flows instead of BIS inflows, both distributed by CrossBorder Capital Ltd.) are
equivalent to those discussed below and available upon request.

Figure 6: Responses of Global Asset Prices & Risk Aversion
10 80
n
i o -20
p
% -30 20
0 -40
-50 0
-60
-70 -20
-5
that is orthogonal to global realized variance – rises sharply.28 The rise is consistent
with the heightened levels of domestic measures of risk premia. Importantly, altering
the degree of risk aversion of international investors constitutes a powerful channel for
the global transmission of US monetary policy. We explore this point further when we
discuss the response of global banks’ leverage below. Quantifying the rise in risk aversion
is less straightforward; but the shock substantially raises it by over 50% above its average
trend.
Figure 7 collects the responses of global economic activity, global domestic credit,
and global credit inflows. The Figure combines together responses extracted from the
VARs (2) and (3) in Table 2. The US monetary policy contraction leaves global growth
unchanged on impact. The inclusion of global growth here serves two purposes. First,
it allows us to consider changes in global financial conditions once we have controlled
for economic activity on a global scale. Second, it helps ensure that we are not con-
founding the effects of a US monetary policy shock with other global shocks that affect
credit through their effects on growth.29 Following a US monetary policy contraction we
28This result is robust to using alternative measures of risk aversion, see Appendix E.
29We compute global growth excluding US (Global Real Economic Activity Ex US) by using the
component of the world production index of Baumeister and Hamilton (2019) that is orthogonal to the
UScycle, calculatedasthecyclicalcomponentofUSIP.BaumeisterandHamilton(2019)useameasure
of global real activity that is constructed as a weighted average of the IP indices of the OECD countries

Figure 7: Responses of Global Credit & Capital Flows
4 4
2.5
2 2
1.5 0 0
s 1 -2 -2
t
p 0
-6
% -6
-0.5
-8
-1 -8
-10
-1.5
-10
-2 -12
-12
Global Credit Ex US Global Inflows Banks Global Inflows Non-Banks
0 0
-2 -2
-4 -4
-2
-6
-6
-4
-8
s t -6 -8
n -10
i o -8 -10
p -12
%-10 -12
-14
-12 -14
-16
-14
-18 -16
-16
-20 -18
-18
register a sharp decrease in credit provision and a strong retrenchment of global capital
inflows. The contraction in global domestic credit is not driven by US domestic credit,
as shown in the lower left panel of the figure. Global capital inflows respond in a similar
fashion: following an initial contraction, international funding flows continue to decrease
to rebound at larger horizons. In the lower section of the figure we report the responses of
capitalinflows splitby recipient type. The overall pictureis consistentwith areduction of
flows directed to both banking and private sectors. The decline in credit, both domestic
and cross-border, whether we look at flows to banks or to non-banks, is in the order of
several percentage points and thus economically significant.
+ 6 Emerging Market Economies, as an extension of a series originally maintained and distributed by
theOECD.Additionaldetailsandresponsesofalternativemeasuresofglobalgrowth/globalrealactivity
are reported in Figure E.1 in the Appendix.

Figure 8: Responses of Leverage of Global Banks
Leverage US Brokers & Dealers Leverage EU Global Banks Leverage US Banks Leverage EU Banks
15 5 0
0 10 -1
-5
5 -2
s 2
t-10
n
i -3
o p-15 0 1
% -20 0 -4
-5
-25 -1 -5
-30 -10 -2
-6
-35 -3
months months months months
Lastly, we collect the responses of banks’ leverage in Figure 8. We use data on the
leverageofUSSecurityBrokersandDealers(USBD)andGloballySystemicallyImportant
Banks (GSIBs) operating in the Euro Area and the UK. Data on total financial assets
and liabilities for USBD are from the Flow of Funds of the Federal Reserve Board, while
the aggregate leverage ratios for global banks in the EA and the UK are constructed
using bank-level balance sheet data (details are reported in Appendix A).30
Consistent with declining asset prices that alter the value of banks’ balance sheets,
the financial leverage of global investors contracts, both among US Brokers & Dealers,
and European global banks. Again, the responses are in the order of several percentage
points, and hence economically relevant. The responses appear to be more delayed and
more muted for the total balance sheet of the banking sector. Domestically oriented
retail banks take longer to adjust, so that broader banking aggregates only react with a
delay to monetary policy shocks, which instead affects more immediately the large banks
with important capital market operations. The effect of US monetary policy on the
whole banking sector is also less precisely estimated, and there is some variation across
specifications.
30AdrianandShin(2010)presentevidenceontheprocyclicalityofleverageinthedomesticUScontext.
In Section 4.2 we extend these results to an international sample of banks.

Figure 9: Responses of Global Credit & Capital Flows: Floaters
Global Real Economic Activity Ex US Floaters Domestic Credit Floaters Inflows All Sectors
5 5
2 0
s t 1 -5
n
i o -5
p 0
% -10
-1 -10
-15
-2
-15
Takentogether, theresponsescollectedinFigures6to8provideevidenceofapowerful
channelofinternationaltransmissionofUSmonetarypolicythatoperatesmainlythrough
global financial actors, and besides the more standard channels related to international
trade. By being able to generate comovements in asset prices, credit creation and credit
flows, risk appetite and financial leverage of global investors, US monetary policy can
influence fluctuations in the Global Financial Cycle. This is likely the joint outcome of
the dollar being the dominant currency in international financial transactions, and of the
interconnectedness of global financial intermediaries.
GFC: Floaters An important question regarding Figure 7 is whether the global con-
traction in credit is in fact driven by countries that have a fixed or pegged exchange rate
regime vis-a`-vis the US dollar. In order to address this concern we restrict our sample
to include only ‘independently floating’ countries, which we identify using use the IMF’s
de-facto classification.31 We construct aggregates as the cross-sectional sum of the levels
of domestic credit and capital inflows, using the same definitions as before. Full sets of
31Independently floating countries in our sample are Australia, Austria, Belgium, Brazil, Canada,
Chile, Cyprus, Czech Republic, Finland, France, Germany, Greece, Hungary, Iceland, Ireland, Italy,
Japan, Luxembourg, Malta, Mexico, Netherlands, New Zealand, Norway, Poland, Portugal, Slove-
external/np/mfd/er/2008/eng/0408.htm.

responses are collected in Figures D.4 and D.5 in the Appendix.
Figure 9 shows the responses of credit and capital inflows for the subset of floaters.
The IRFs are obtained by replacing world aggregates with these newly constructed series
inthesameVARasbefore(seeTable2). Againinthiscasewecontrolforglobaleconomic
activity. The IRFs in Figure 9 show that countries that adopt a floating exchange rate
regime seem to be equally exposed to US monetary policy shocks. In fact, the magnitude
of the contraction in the credit variables is very similar to that obtained over the full
sample. It should be clear that these results do not imply that exchange rate regimes
are equivalent. However, they do indicate that a floating exchange rate regime is not
successful in providing a protective shield against US monetary policy shocks, and that
fluctuations in the Global Financial Cycle can affect in a significant way all countries.
We explore this point further in the next paragraph.
GFC: Currencies, Credit, and Monetary Independence We finally turn to eval-
uating more in detail how financial conditions transmit across borders by restricting our
attentiontothecaseoftheUKandEuroArea, twoimportantcurrencyareaswithflexible
exchange rates. Full set of responses are in Figures D.6 and D.7 in the Appendix.
Figure 10 collects the responses of the local stock market indices, bilateral exchange
ratesvis-`a-visthedollar,corporatebondspreads,andpolicyinterestratesfortheUK(top
row of the figure) and the Euro Area (bottom row of the figure).32 We note that for all
these variables the responses across the two countries are remarkably similar. Consistent
with the fall in the global factor in risky asset prices, the local stock market indices
plummet on impact to a very similar degree. The dollar appreciates significantly against
both currencies. The exchange rate is in both cases measured as units of the foreign
currency per one US dollar, such that a positive reading corresponds to an appreciation
of the dollar. The appreciation is relatively short-lived in both cases, and reverts in
the span of one to three quarters after the shock hits. The US monetary policy shock
alters funding costs in both the UK and Euro Area, with corporate bond spreads rising
very significantly and on impact in both cases. Finally, the responses of the policy rates
32ForperiodsprecedingtheintroductionoftheEuro,weusetheGermanMarkastherelevantEuropean
benchmark currency and convert it using the fixed exchange rate with the Euro chosen at the time of
introduction of the common currency.

Figure 10: Cross-Border Financial Conditions & Monetary Policy
FTSE All Share GBP to 1 USD UK Corporate Spread UK Policy Rate
10 8 1 1
0.8
5 6
0.6
0.5
4 0.4
s
t 2 0.2
n 0
i
o -5 0
p 0
% -0.2
-10 -2 -0.5
-0.4
-4 -0.6
-15 -1
-6 -0.8
DAX Stock Market EUR to 1 USD GER Corporate Spread EA Policy Rate
15 6 0.8 0.2
10 4
0.6 0
s 0 0.4 -0.2
p
%
-5 -4
-0.6
-6 0
-10 -8 -0.8
-0.2
-15 -10 -1
-12 -0.4
months months months months
suggest that a US contractionary monetary policy shock is likely to be followed by an
endogenous easing in both the UK and the Euro Area, potentially as a response to the
deterioration of the local financial conditions. While estimated with a higher degree of
uncertainty in the case of the Euro area, the magnitude of the responses is very similar
in the two cases, and implies an endogenous monetary easing of about 30bps. This also
implies that the tightening of financial conditions in the UK and the Euro Area cannot
be ascribed to a domestic monetary policy tightening, and is instead a consequence of
the US monetary policy spillover.

4 Interpretation of the Results
4.1 A Simple Model with Heterogeneous Investors
The empirical results show that US monetary policy affects global banks’ leverage, risky
asset prices and global risk aversion. In this section, we present a stylized framework
to help with the interpretation of our empirical findings; the model builds directly on
the work of Zigrand et al. (2010).33 Our illustrative model of international asset pricing
features investors with heterogeneous propensities to take risk, in order to make sense of
a time-varying degree of aggregate effective risk aversion.34 The risk premium depends
on the wealth distribution between leveraged global banks on the one hand, and asset
managers, such as insurance companies or sovereign wealth funds, on the other hand. As
therelativewealthofthetwotypesofinvestorsfluctuates,assetpricingwillbedetermined
mostly by one type of investors or the other.
We consider a world with two types of investors: global banks and asset managers.
Global banks and asset managers account for a large part of cross-border flows, as shown
in Figure 4. Global banks are leveraged entities that fund themselves in dollars for their
operations in capital markets. They can borrow at the US risk-free rate and lever to
buy a portfolio of world risky securities, whose returns are in dollars. They are risk-
neutral investors and subject to a Value-at-Risk (VaR) constraint, which is imposed by
regulation.35 We present microeconomic evidence pertaining to the leverage and risk tak-
ing behaviour of banks in Section 4.2. The second type of investors are asset managers
who, like global banks, acquire risky securities in world markets and can borrow at the
US risk-free rate. Asset managers also hold a portfolio of regional assets (for example
regional real estate) which is not traded in financial markets, perhaps because of infor-
mation asymmetries. Asset managers are standard mean-variance investors and exhibit
33See also Etula (2013) and Adrian and Shin (2014).
34Foramorerealisticdynamicstochasticgeneralequilibriummodelofassetpricingwithheterogeneous
investorsandmonetarypolicyseeCoimbraandRey(2017). Othertypesofmodelswhichgeneratetime-
varying risk aversion are, for example, models with habits in consumption (see Campbell and Cochrane
35Their risk neutrality is an assumption which may be justified by the fact that they benefit from an
implicit bailout guarantee, either because they are universal banks, and are therefore part of a deposit
guarantee scheme, or because they are too systemic to fail. Whatever the microfoundations, the crisis
has provided ample evidence that global banks have taken on large amounts of risk and that this risk
was not priced by creditors.

a positive degree of risk aversion that limits their desire to leverage.36
Global Banks
Global banks maximize the expected return of their portfolio of world risky assets subject
to a Value-at-Risk (VaR) constraint.37 The VaR imposes an upper limit on the amount
a bank is predicted to lose on a portfolio with a certain probability. We denote by R
t
the vector of excess returns of all traded risky assets in the world (in dollars). We denote
by xB the portfolio shares of a global bank, and by wB the equity of the bank. The
t t
maximization problem of a global bank is
maxE (cid:0) xB(cid:48)R (cid:1)
t t t+1
xB
t
subject to VaR ≤ wB,
t t
where VaR is defined as a multiple α of the standard deviation of the bank portfolio
t
VaR = αwB
(cid:2)Var (cid:0)
xB(cid:48)R
(cid:1)(cid:3)1
2.
Taking the first order condition, and using the fact that the constraint is binding
(since banks are risk neutral) gives the following solution for the vector of asset demands:
xB = [Var (R )]−1E (R ), (1)
t αλ t t+1 t t+1
t
where we use Var to denote the variance. This is formally similar to the portfolio allo-
cation of a mean-variance investor. In Eq. (1), λ is the Lagrange multiplier: the VaR
t
constraint plays the same role as risk aversion.38
Asset Managers
Asset managers are standard mean-variance investors with a constant degree of risk aver-
36Thefactthatonlyassetmanagers,andnottheglobalbanks,havearegionalportfolioisnonessential;
global banks could be allowed to hold a portfolio of regional loans or assets as well. The asymmetry
in risk aversion (risk neutral banks with VaR constraint and risk averse asset managers), however, is
important for the results.
37VaR constraints have been used internally for the risk management of large banks for a long time
and have entered the regulatory sphere with Basel II and III. For a microfoundation of VaR constraints,
see Adrian and Shin (2014).
38It is possible to solve out for the Lagrange multiplier using the binding VaR constraint (see Zigrand
et al., 2010). We find λ =[E (R )(cid:48)[Var (R )]−1E (R )]−1/2.
t t t+1 t t+1 t t+1

sion equal to σ. They have access to the same set of traded assets as global banks. We
call xI the vector of portfolio weights of the asset managers in tradable risky assets. Asset
t
managers also invest in local (regional) non-traded assets. We denote by yI the fraction
t
of their wealth invested in those regional assets (their net supply is y ). The vector of
t
excess returns on these non tradable investments is RN. Finally, we call wI the equity of
t t
asset managers. An asset manager chooses his portfolio of risky assets by maximizing
σ
maxE (cid:0) xI(cid:48)R +yI(cid:48)RN (cid:1) − Var (cid:0) xI(cid:48)R +yI(cid:48)RN (cid:1) .
xI t t t+1 t t+1 2 t t t+1 t t+1
t
The optimal portfolio choice in risky tradable securities for an asset manager will be
xI = [Var (R )]−1(cid:2)E (R )−σCov (R ,RN )yI (cid:3) . (2)
t σ t t+1 t t+1 t t+1 t+1 t
Market clearing conditions
The market clearing condition for risky traded securities is xB w t B + xI w t I = s
t wB+wI twB+wI t
t t t t
where s is a world vector of net asset supplies for traded assets.
t
Proposition 1 (Risky Asset Returns) Using Eq. (1) and (2) and the market clear-
ing conditions, the expected excess returns on tradable risky assets can be rewritten as the
sum of a global component and a regional component:
t t+1 t t t+1 t t t t+1 t+1 t
where Γ ≡
(cid:104)
(cid:105)−1(cid:0)
wB +wI (cid:1) . The global component of risky asset prices is equal
to the aggregate variance scaled by the aggregate degree of effective risk aversion Γ .
t
Γ is the wealth-weighted average of the ‘risk aversions’ of the asset managers and the
t
global banks. It can be interpreted as the aggregate degree of effective risk aversion of
the market. If all the wealth were in the hands of asset managers, for example, aggregate
risk aversion would be equal to σ. Using Eq. (3) as a guiding framework, in Section 2
we extracted the global factor in world risky asset prices by writing each price series as
the sum of a global, a regional and an asset specific component. We then used Eq. (3) to

extract our empirical proxy for aggregate risk aversion Γ .39 One possible interpretation
t
of the decline in the measure of aggregate risk aversion observed between 2003 and 2007
in Figure 3 is therefore that it was driven by risk-neutral global banks becoming large
and important for the pricing of risky assets, sustaining an increase in risky asset prices
on a global scale. This trend reversed after the crisis, when instead more risk-averse asset
managers became relatively bigger (see Figure 4).
Proposition 2 (Global Banks Returns) The expected excess return of a global bank
portfolio in our economy is given by
E (xB(cid:48)R ) = Γ Cov (xB(cid:48)R ,s(cid:48)R )+Γ Cov (xB(cid:48)R ,y(cid:48)RN )
t t t+1 t t t t+1 t t+1 t t t t+1 t t+1
= βBWΓ Var (s(cid:48)R )+Γ Cov (xB(cid:48)R ,y(cid:48)RN ), (4)
where βBW is the beta of a global bank with the world market portfolio.
t
The higher the correlation of a global bank portfolio with the world portfolio (i.e. high-
βBW), the more the bank loads on world risk, the higher the expected asset return, ceteris
t
paribus.
4.2 Evidence on Global Banks
In this section we use balance sheet data to provide some evidence on the risk taking
behavior of banks, in line with our simple model. Adrian and Shin (2010) show that the
leverage of US brokers-dealers is procyclical. Using balance sheet data for a large sample
of international financial institutions (see Table A.4), we find that the positive association
between leverage growth and balance sheet growth goes well beyond US borders. We
report these results in Figure A.3 in the Appendix.40 The procyclicality of leverage tends
to be a stronger feature of the behavior of financial institutions that engage in global
39As mentioned earlier, in general our empirical proxy for aggregate risk aversion could also reflect
expected dividend growth and discount rates. We control for these additional factors, estimate a more
general aggregate degree of risk aversion and check that all our results go through in Appendix E.
40We calculate leverage along the lines of Kalemli-Ozcan et al. (2012). We use a panel 166 financial
institutions in 20 countries from 2000 to 2010. We identify a subset of 21 large banks who have been
classified as Globally Systemically Important Banks (GSIBs). A complete list of institutions included in
our set is in Table A.4.

Figure 11: Correlation between banks’ returns and loading on the
global factor
D:CBK
3 W:NFD:ASGE
−0.5 0 0.5 1
nruter
egareva
sisirc
erp
Full Sample (162)
(a)
LLOY −4 D:CBK B:DEX
−6 RBS
−8
−10
−12
−0.5 0 0.5 1
average β pre crisis
nruter
egareva
sisirc
tsop
G−SIBs (20)
(c)
D:CBK
W:NDA F:SGE
2.5 F:BNP D:DBK S:CSGN U:GS E:SCH 2 I:UCG BARC S:UBSNB:DEX
1.5 U:JPM LLOUY:MS
HSBA
RBS U:BKU:STT
1U:BAC
0.2 0.4 0.6 0.8 1 1.2
(b) (d)
U:JPMW:NDA
HSBA U:UB:KG UES ::SSTCTH −1 F:BNP S:CSGN
−2 U:MS D:DBK
−3 U:BAC I:UCG BARC F: S S : G U E BSN
LLOY
−4 D:CBK
−5 B:DEX
−6
RBS
0.2 0.4 0.6 0.8 1 1.2
average β pre crisis
Note: In each subplot, the x axis reports the average βBW in the three years preceding the onset of
the financial crisis (August 2007), while the y axis records average returns in percentage points. Filled
blue circles highlight GSIBs within the broader population of banks (hollow circles); the sign of the
correlation is visualized by a red regression line in each plot. Panels (a) and (b): banks average returns
pre (2003-2007) and post (2007-2010) crisis as a function of their pre-crisis betas. Panels (c) and (d)
GSIBs subsample. Source: Datastream, authors calculations.
capital markets operations, a subset which included in particular the former stand-alone
investment banks. The same holds true for the large European (UK, Euro Area and
Switzerland) universal banks, whose investment departments played a central role in
channellingUSdollarliquidityworldwideintheyearsimmediatelyprecedingthefinancial
crisis (see Shin, 2012). Many of those large European Banks are GSIBs.
Figure 11 is the empirical counterpart of Eq. (4), and reports the correlation between
thereturnsofeachbankandtheirloading(βBW)onourglobalfactorofSection2. Results
t
in panels (a) and (b) are calculated over the entire population of banks, while panels (c)
and (d) refer to the GSIBs subsample, and we use August 2007 to distinguish between
pre and post crisis periods. Results confirm a positive association between high βBW and
t
high returns in the pre crisis sample. Panels (a) and (c) show that, relative to the larger
population, GSIBs tend to have both higher average betas, and larger returns. This

suggests that global banks were systematically loading more on world risk in the run-up
to the financial crisis, and that their behaviour was delivering larger average returns,
compared to the average bank in our sample. The higher loadings on risk are consistent
with the build-up of leverage in the years prior to the crisis documented in Figure A.2.
Panels (b) and (d) sort the banks on the x-axis according to their pre-crisis betas, but
report their post crisis returns on the y axis: institutions that were loading more on
global risk pre crisis suffered the largest losses after the systemic meltdown began.
5 Conclusions
This paper establishes the importance of US monetary policy as one of the drivers of the
Global Financial Cycle. First, we show that a single global factor explains an impor-
tant share of the common variation of a large cross section of risky asset prices around
the world. Using a simple model of international asset pricing with heterogeneous in-
termediaries, we interpret this global factor as reflecting market volatility and aggregate
risk aversion in global markets. Second, we show that US monetary policy shocks in-
duce strong comovements in the international financial variables that characterize the
Global Financial Cycle. Monetary contractions are followed by a significant deleveraging
of global financial intermediaries, a rise in aggregate risk aversion, a contraction in the
global factor in asset prices and a decline in global credit, a widening of corporate bond
spreads and retrenchments of gross capital flows. These results also hold for the countries
of our sample with floating exchange rates. This is an important result, as it challenges
the degree of monetary policy sovereignty of open economies, and echoes the claim of
Rey (2013) that the Mundellian trilemma may have morphed into a dilemma: as long as
capital flows across borders are free, and macroprudential tools are not used, monetary
conditions in any country, even one with a flexible exchange rate, are partly dictated by
themonetarypolicyofthehegemon(theUS).Thisofcoursedoesnotmeanthatexchange
rate regimes do not matter, as Klein and Shambaugh (2013) and Obstfeld (2015) rightly
point out.41 This international transmission mechanism of monetary policy is a priori
41Forinterestingmodelsofthechallengesofthetrilemmainstandardneo-Keynesianmodels,seeFarhi
and Werning, 2012, 2013.

consistent with models where financial market imperfections play an important role, e.g.
via Value-at-Risk constraints, and where heterogeneous financial intermediaries price as-
sets. It still remains to be seen whether open economy extensions of these models would
be able to generate a Global Financial Cycle whose features would match the empirical
regularities uncovered in this paper.42
42For a more detailed discussion of the theoretical challenges when modelling international monetary
policy transmission channels, see Bernanke (2017) Rey (2016) and Coimbra and Rey (2017) .

DOMESTIC CREDIT CROSS BORDER CREDIT
80000 35000
GLOBAL TO ALL SECTORS
EXCLUDING US TO BANKS
70000 30000 TO NON−BANKS
60000
25000
50000
20000
40000
15000
30000
10000
20000
10000
0 0
1980 1990 2000 2010 1980 1990 2000 2010
Note: Global Domestic Credit and Global Cross-Border Inflows constructed as the cross sectional sum
of country-specific credit variables. The unit in both plots is Billion USD.
Following Gourinchas and Obstfeld (2012) we construct National Domestic Credit for
each country as the difference between Domestic Claims to All Sectors and Net Claims
to Central Government reported by each country’s financial institutions; however, we
only consider claims of depository corporations excluding central banks. Specifically,
we refer to the Other Depository Corporation Survey available within the IFS database
and construct Claims to All Sectors as the sum of Claims On Private Sector, Claims
on Public Non Financial Corporations, Claims on Other Financial Corporations and
Claims on State And Local Government; while Net Claims to Central Government are
calculated as the difference between Claims on and Liabilities to Central Government.
This classification was adopted starting from 2001, prior to that date we refer to the
DepositMoneyBanksSurvey. Rawdataarequarterlyandexpressedinnationalcurrency,
we convert them in Billion USD equivalents using end of period exchange rates again
available within the IFS. Whenever there exists a discontinuity between data available
under the old and new classifications we interpolate the missing observations. Global

Table A.1: List of Countries Included
North Latin Central and Western Emerging Asia Africa and
America America Eastern Europe Europe Asia Pacific Middle East
Canada Argentina Belarus Austria China Australia Israel
US Bolivia Bulgaria Belgium Indonesia Japan South Africa
Brazil Croatia Cyprus Malaysia Korea
Chile Czech Republic Denmark Singapore New Zealand
Colombia Hungary Finland Thailand
Costa Rica Latvia France
Ecuador Lithuania Germany
Mexico Poland Greece*
Romania Iceland
Russian Federation Ireland
Slovak Republic Italy
Slovenia Luxembourg
Turkey Malta
Netherlands
Norway
Portugal
Spain
Sweden
Switzerland
UK
Note: Countries included in the construction of the Domestic Credit and Cross-Border Credit variables
used throughout the paper. Greece is not included in the computation of Global Domestic Credit due
to poor quality of original national data.
DomesticCreditisfinallyconstructedasthecross-sectionalsumoftheNationalDomestic
Credit variables.
To construct the Cross-Border Capital Inflows measures used within the paper we
adopt the definition of Direct Cross-Border Credit in Avdjiev et al. (2012). We use
original data available at the BIS Locational Banking Statistics Database and collected
under External Positions of Reporting Banks vis-`a-vis Individual Countries (Table 6).
Data refer to the outstanding amount of Claims to All Sectors and Claims to Non-Bank
Sector in all currencies, all instruments, declared by all BIS reporting countries with
counterparty location being the individual countries in Table A.1. We then construct
Claims to the Banking Sector as the difference between the two categories available.
Original data are available at quarterly frequency in Million USD. Global Inflows are

finally calculated as the cross-sectional sum of the national variables. Global domestic
credit and global cross-border capital inflows are plotted in Figure A.1.
A.2 Banking Sector and Individual Banks Leverage data
To construct an aggregate country-level measure of banking sector leverage we follow
Forbes(2012) andbuild it asthe ratio between Claims onPrivateSector and Transferable
plusOtherDepositsincludedinBroadMoneyofdepositorycorporationsexcludingcentral
banks. Original data are in national currencies and are taken from the Other Depository
Corporations Survey; Monetary Statistics, International Financial Statistics database.
The classification of deposits within the former Deposit Money Banks Survey corresponds
to Demand, Time, Savings and Foreign Currency Deposits. Using these national data as
a reference, we construct the European Banking Sector Leverage variable as the median
leverage ratio among Austria, Belgium, Denmark, Finland, France, Germany, Greece,
Ireland, Italy, Luxembourg, Netherlands, Portugal, Spain and United Kingdom.
Figure A.2: European Banks Leverage
36 1.6
G−SIBs BANKS BANKING SECTOR
34 EUR BANKS
GBP BANKS 1.5
30 1.4
1.3
1.2
22 1.1
16 0.9
1980 1990 2000 2010 1980 1990 2000 2010
Note: [left panel] Leverage ratio calculated for the European GSIBs with a detail on EUR and GBP
banksusingtheinstitutionsandclassificationinTableA.2. [rightpanel]AggregatedEuropeanbanking
sector leverage ratio measured as the median of European countries banking sector leverage variables
following Forbes (2012).
The aggregate Leverage Ratios (defined as Total Assets over Equity) for the Global
Systemic Important Banks in the Euro-Area and United-Kingdom used in the BVAR are
constructed as weighted averages of individual banks data. Balance sheet Total Assets
(DWTA) and Shareholders’ Equity (DWSE) are from the Thomson Reuter Worldscope

Table A.2: European G-SIBs.
name isin gics industry country ea lev uk lev
BNP Paribas FR0000131104 Commercial Banks France •
Credit Agricole FR0000045072 Commercial Banks France •
Societe Generale FR0000130809 Commercial Banks France •
Commerzbank DE0008032004 Commercial Banks Germany •
Deutsche Bank DE0005140008 Capital Markets Germany •
Unicredit IT0004781412 Commercial Banks Italy •
ING Bank NL0000113892 Commercial Banks Netherlands •
BBVA ES0113211835 Commercial Banks Spain •
Banco Santander ES0113900J37 Commercial Banks Spain •
Nordea Group SE0000427361 Commercial Banks Sweden
Credit Suisse Group CH0012138530 Capital Markets Switzerland
UBS CH0024899483 Capital Markets Switzerland
Royal Bank of Scotland GB00B7T77214 Commercial Banks UK •
Barclays GB0031348658 Commercial Banks UK •
HSBC Holdings GB0005405286 Commercial Banks UK •
Lloyds Banking Group GB0008706128 Commercial Banks UK •
Standard Chartered GB0004082847 Diversified Fin’l UK •
Note: European Global Systemically Important Banks included in the construction of GSIBs Leverage
Ratios; the last two columns highlight the components of EUR and GDP Leverage respectively.
Datastream database and available at quarterly frequency. Weights are proportional to
Market Capitalisation (WC08001) downloaded from the same source. Details on the
banks included and their characteristics are summarised in Table A.2 below. The aggre-
gated banking sector leverage and the leverage ratio of the European GSIBs are plotted
in Figure A.2.
Figures 11 and A.3 are built using data on individual banks total return indices
excluding dividends taken from Thomson Reuters Worldscope database at quarterly fre-
quency. Data are collected directly from banks balance sheets and Leverage Ratios are
computed as the ratio between Total Assets (DWTA) and Common/Shareholders’ Equity
(DWSE).TotalAssetsincludecashandduefrombanks, totalinvestments, netloans, cus-
tomer liability on acceptances (if included in total assets), investment in unconsolidated
subsidiaries, real estate assets, net property, plant and equipment, and other assets. De-
scriptive statistics for bank level data and a complete list of the institutions included in
the sample are provided in Tables A.3 and A.4 respectively. Although the data source is
different, the calculation follows Kalemli-Ozcan et al. (2012).

Table A.3: Bank Data Summary Statistics.
(a)
All (155) GSIBs (25) CommB (123)
min 0.3 0.0 1.113 60.9 2.7 6.353 0.4 0.0 4.887
max 3880.6 219.8 327.2 3880.6 219.8 163.5 3880.6 219.8 327.2
mean 251.7 12.9 18.73 1121.2 53.4 24.59 258.4 13.5 19.86
median 54.8 3.9 15.92 1108.3 39.1 22.76 55.0 3.6 17
(b)
CapM (18) T&MF (5) Other Fin’l(9)
min 0.3 0.2 1.113 1.9 0.1 2.989 5.5 0.6 2.242
max 3595.1 76.9 136.2 61.2 5.7 19.5 310.0 42.8 65.13
mean 364.5 15.4 16.06 21.7 2.5 9.933 63.1 6.7 13.65
median 90.2 7.3 12.98 21.7 1.3 7.978 26.9 3.3 7.259
Note: Summary statistics for bank-level data used in the analysis. (A) Total Assets, (E) Sharehold-
ers’ Equity, (L) Leverage Ratio. [panel (a)] full sample (All), Global Systemically Important Banks
(GSIBs), Commercial Banks (CommB). [panel (b)] Capital Markets (CapM), Thrifts & Mortgage Fi-
nance (T&MF), Other Financial (Other Fin’l, includes Diversified Financial Services and Consumer
Finance). Total assets and common equity are in Billion USD. Numbers in parentheses denote the
number of banks in each category.
Table A.4: List of Financial Institutions included
AT0000606306 RAIFFEISENBANKINTL. EU Austria CommercialBanks
AT0000625108 OBERBANK EU Austria CommercialBanks
AT0000652011 ERSTEGROUPBANK EU Austria CommercialBanks
BE0003565737 KBCGROUP EU Belgium CommercialBanks
GB0005405286 HSBCHOLDING EU GreatBritain CommercialBanks •
GB0008706128 LLOYDSBANKINGGROUP EU GreatBritain CommercialBanks •
GB0031348658 BARCLAYS EU GreatBritain CommercialBanks •
GB00B7T77214 ROYALBANKOFSCTL.GP. EU GreatBritain CommercialBanks •
DK0010274414 DANSKEBANK EU Denmark CommercialBanks
DK0010307958 JYSKEBANK EU Denmark CommercialBanks
FR0000045072 CREDITAGRICOLE EU France CommercialBanks •
FR0000031684 PARISORLEANS EU France CapitalMarkets
FR0000120685 NATIXIS EU France CommercialBanks
FR0000130809 SOCIETEGENERALE EU France CommercialBanks •
FR0000131104 BNPPARIBAS EU France CommercialBanks •
DE0008001009 DEUTSCHEPOSTBANK EU Germany CommercialBanks
DE0005140008 DEUTSCHEBANK EU Germany CapitalMarkets •

DE000CBK1001 COMMERZBANK EU Germany CommercialBanks •
IE0000197834 ALLIEDIRISHBANKS EU Ireland CommercialBanks
IE0030606259 BANKOFIRELAND EU Ireland CommercialBanks
IE00B59NXW72 PERMANENTTSBGHG. EU Ireland CommercialBanks
IT0005002883 BANCOPOPOLARE EU Italy CommercialBanks
IT0003487029 UNIONEDIBANCHEITALIAN EU Italy CommercialBanks
IT0000062957 MEDIOBANCABC.FIN EU Italy CapitalMarkets
IT0000064482 BANCAPOPOLAREDIMILANO EU Italy CommercialBanks
IT0000072618 INTESASANPAOLO EU Italy CommercialBanks
IT0001005070 BANCODISARDEGNARSP EU Italy CommercialBanks
IT0004984842 BANCAMONTEDEIPASCHI EU Italy CommercialBanks
IT0004781412 UNICREDIT EU Italy CommercialBanks •
NO0006000801 SPAREBANK1NORD-NORGE EU Norway CommercialBanks
NO0006000900 SPAREBANKENVEST EU Norway CommercialBanks
PTBCP0AM0007 BANCOCOMR.PORTUGUESR EU Portugal CommercialBanks
PTBES0AM0007 BANCOESPIRITOSANTO EU Portugal CommercialBanks
PTBPI0AM0004 BANCOBPI EU Portugal CommercialBanks
ES0113860A34 BANCODESABADELL EU Spain CommercialBanks
ES0113211835 BBV.ARGENTARIA EU Spain CommercialBanks •
ES0113679I37 BANKINTERR EU Spain CommercialBanks
ES0113790226 BANCOPOPULARESPANOL EU Spain CommercialBanks
ES0113900J37 BANCOSANTANDER EU Spain CommercialBanks •
SE0000148884 SEBA EU Sweden CommercialBanks
SE0000193120 SVENSKAHANDBKN.A EU Sweden CommercialBanks
SE0000242455 SWEDBANKA EU Sweden CommercialBanks
SE0000427361 NORDEABANK EU Sweden CommercialBanks •
CH0012138530 CREDITSUISSEGROUPN EU Switzerland CapitalMarkets •
CH0012335540 VONTOBELHOLDING EU Switzerland CapitalMarkets
CH0018116472 BANKCOOP EU Switzerland CommercialBanks
CH0024899483 UBSR EU Switzerland CapitalMarkets •
CA0636711016 BANKOFMONTREAL AM Canada CommercialBanks
CA0641491075 BK.OFNOVASCOTIA AM Canada CommercialBanks
CA1360691010 CANADIANIMP.BK.COM. AM Canada CommercialBanks
CA13677F1018 CANADIANWESTERNBANK AM Canada CommercialBanks
CA51925D1069 LAURENTIANBK.OFCANADA AM Canada CommercialBanks
CA6330671034 NAT.BK.OFCANADA AM Canada CommercialBanks
CA7800871021 ROYALBANKOFCANADA AM Canada CommercialBanks
CA8911605092 TORONTO-DOMINIONBANK AM Canada CommercialBanks
US0258161092 AMERICANEXPRESS AM UnitedStates DiversifiedFin’l
US0454871056 ASSOCIATEDBANC-CORP AM UnitedStates CommercialBanks
US0462651045 ASTORIAFINL. AM UnitedStates Thrifts&Mortgage
US0549371070 BB&T AM UnitedStates CommercialBanks
US05561Q2012 BOKFINL. AM UnitedStates CommercialBanks
US0596921033 BANCORPSOUTH AM UnitedStates CommercialBanks
US0605051046 BANKOFAMERICA AM UnitedStates CommercialBanks •
US0625401098 BANKOFHAWAII AM UnitedStates CommercialBanks
US0640581007 BANKOFNEWYORKMELLON AM UnitedStates CapitalMarkets •
US14040H1059 CAPITALONEFINL. AM UnitedStates DiversifiedFin’l
US1491501045 CATHAYGEN.BANCORP AM UnitedStates CommercialBanks
US1729674242 CITIGROUP AM UnitedStates CommercialBanks •
US1785661059 CITYNATIONAL AM UnitedStates CommercialBanks
US2003401070 COMERICA AM UnitedStates CommercialBanks
US2005251036 COMMERCEBCSH. AM UnitedStates CommercialBanks
US2298991090 CULLENFO.BANKERS AM UnitedStates CommercialBanks

US2692464017 E*TRADEFINANCIAL AM UnitedStates CapitalMarkets
US27579R1041 EASTWESTBANCORP AM UnitedStates CommercialBanks
US3167731005 FIFTHTHIRDBANCORP AM UnitedStates CommercialBanks
US31946M1036 FIRSTCTZN.BCSH.A AM UnitedStates CommercialBanks
US3205171057 FIRSTHORIZONNATIONAL AM UnitedStates CommercialBanks
US33582V1089 FIRSTNIAGARAFINL.GP. AM UnitedStates CommercialBanks
US3379151026 FIRSTMERIT AM UnitedStates CommercialBanks
US3546131018 FRANKLINRESOURCES AM UnitedStates CapitalMarkets
US3602711000 FULTONFINANCIAL AM UnitedStates CommercialBanks
US38141G1040 GOLDMANSACHSGP. AM UnitedStates CapitalMarkets •
US4436831071 HUDSONCITYBANC. AM UnitedStates Thrifts&Mortgage
US4461501045 HUNTINGTONBCSH. AM UnitedStates CommercialBanks
US4508281080 IBERIABANK AM UnitedStates CommercialBanks
US4590441030 INTERNATIONALBCSH. AM UnitedStates CommercialBanks
US46625H1005 JPMORGANCHASE&CO. AM UnitedStates CommercialBanks •
US4932671088 KEYCORP AM UnitedStates CommercialBanks
US55261F1049 M&TBANK AM UnitedStates CommercialBanks
US55264U1088 MBFINANCIAL AM UnitedStates CommercialBanks
US6174464486 MORGANSTANLEY AM UnitedStates CapitalMarkets •
US6494451031 NEWYORKCOMMUNITYBANC. AM UnitedStates Thrifts&Mortgage
US6658591044 NORTHERNTRUST AM UnitedStates CapitalMarkets
US6934751057 PNCFINL.SVS.GP. AM UnitedStates CommercialBanks
US7127041058 PEOPLESUNITEDFINANCIAL AM UnitedStates Thrifts&Mortgage
US7429621037 PRIVATEBANCORP AM UnitedStates CommercialBanks
US7547301090 RAYMONDJAMESFINL. AM UnitedStates CapitalMarkets
US7591EP1005 REGIONSFINL.NEW AM UnitedStates CommercialBanks
US78442P1066 SLM AM UnitedStates DiversifiedFin’l
US78486Q1013 SVBFINANCIALGROUP AM UnitedStates CommercialBanks
US8085131055 CHARLESSCHWAB AM UnitedStates CapitalMarkets
US8574771031 STATESTREET AM UnitedStates CapitalMarkets •
US8679141031 SUNTRUSTBANKS AM UnitedStates CommercialBanks
US8690991018 SUSQUEHANNABCSH. AM UnitedStates CommercialBanks
US87161C5013 SYNOVUSFINANCIAL AM UnitedStates CommercialBanks
US8722751026 TCFFINANCIAL AM UnitedStates CommercialBanks
US87236Y1082 TDAMERITRADEHOLDING AM UnitedStates CapitalMarkets
US9027881088 UMBFINANCIAL AM UnitedStates CommercialBanks
US9029733048 USBANCORP AM UnitedStates CommercialBanks
US9042141039 UMPQUAHOLDINGS AM UnitedStates CommercialBanks
US9197941076 VALLEYNATIONALBANCORP AM UnitedStates CommercialBanks
US9388241096 WASHINGTONFEDERAL AM UnitedStates Thrifts&Mortgage
US9478901096 WEBSTERFINANCIAL AM UnitedStates CommercialBanks
US9497461015 WELLSFARGO&CO AM UnitedStates CommercialBanks •
US97650W1080 WINTRUSTFINANCIAL AM UnitedStates CommercialBanks
US9897011071 ZIONSBANCORP. AM UnitedStates CommercialBanks
JP3902900004 MITSUBISHIUFJFINL.GP. AS Japan CommercialBanks •
JP3890350006 SUMITOMOMITSUIFINL.GP. AS Japan CommercialBanks •
JP3429200003 SHINKINCENTRALBANKPF. AS Japan CommercialBanks
JP3805010000 FUKUOKAFINANCIALGP. AS Japan CommercialBanks
JP3842400008 HOKUHOKUFINL.GP. AS Japan CommercialBanks
JP3105040004 AIFUL AS Japan DiversifiedFin’l
JP3107600003 AKITABANK AS Japan CommercialBanks
JP3108600002 ACOM AS Japan DiversifiedFin’l
JP3152400002 BANKOFIWATE AS Japan CommercialBanks
JP3175200009 OITABANK AS Japan CommercialBanks

JP3194600007 BANKOFOKINAWA AS Japan CommercialBanks
JP3200450009 ORIX AS Japan DiversifiedFin’l
JP3207800008 KAGOSHIMABANK AS Japan CommercialBanks
JP3271400008 CREDITSAISON AS Japan DiversifiedFin’l
JP3276400003 GUNMABANK AS Japan CommercialBanks
JP3351200005 SHIZUOKABANK AS Japan CommercialBanks
JP3352000008 77BANK AS Japan CommercialBanks
JP3388600003 JACCS AS Japan DiversifiedFin’l
JP3392200006 EIGHTEENTHBANK AS Japan CommercialBanks
JP3392600007 JUROKUBANK AS Japan CommercialBanks
JP3394200004 JOYOBANK AS Japan CommercialBanks
JP3441600008 TAIKOBANK AS Japan CommercialBanks
JP3502200003 DAIWASECURITIESGROUP AS Japan CapitalMarkets
JP3511800009 CHIBABANK AS Japan CommercialBanks
JP3520000005 CHUKYOBANK AS Japan CommercialBanks
JP3521000004 CHUGOKUBANK AS Japan CommercialBanks
JP3587000005 TOKYOTOMINBANK AS Japan CommercialBanks
JP3601000007 TOHOBANK AS Japan CommercialBanks
JP3630500001 TOMATOBANK AS Japan CommercialBanks
JP3653400006 NANTOBANK AS Japan CommercialBanks
JP3762600009 NOMURAHDG. AS Japan CapitalMarkets
JP3769000005 HACHIJUNIBANK AS Japan CommercialBanks
JP3783800000 HIGOBANK AS Japan CommercialBanks
JP3786600001 HITACHICAPITAL AS Japan DiversifiedFin’l
JP3841000007 HOKUETSUBANK AS Japan CommercialBanks
JP3881200004 MIEBANK AS Japan CommercialBanks
JP3888000001 MICHINOKUBANK AS Japan CommercialBanks
JP3905850008 MINATOBANK AS Japan CommercialBanks
JP3942000005 YAMANASHICHUOBK. AS Japan CommercialBanks
JP3955400001 BANKOFYOKOHAMA AS Japan CommercialBanks
Notes: In the first column are the ISIN identification codes followed by the institution’s name, ge-
ographical location and country of reference. The last column highlights the subset of institutions
which have been classified as Global Systemically Important Banks (G-SIBs) previously known as
G-SIFIs (Systemically Important Financial Institutions); the classification has been adopted by the
Financial Stability Board starting from November 2011 and lastly updated in November 2013.

Figure A.3: Quarterly asset growth over quarterly leverage growth
across different global financial institutions
G−SIBs (25)
Q1−06
15 Q1−08
−10
−20 −10 0 10 20
ylretrauQ
htworG
tessA
Commercial Banks (122)
15 Q1−06
QQ11−−0085
10 Q3−09 Q1−Q017−Q034−0Q33Q−40−61 Q
3−07 Q1−09
−10
−20 −15 −10 −5 0 5 10
Capital Markets (18) Other Financial (14)
30 20
25 Q1−07
20 Q2−07 Q2−12 Q2−10
Q3−08 Q2−09
−10 −10
Quarterly Leverage Growth
Note: he red line in each subplot is the 45 degree line. Clockwise, from top left panel, the relationship
between balance sheet size and leverage for GISBs, commercial banks, institutions operating in capital
markets and other financial institutions. The classification matches GICS industry codes for each entry
in the sample. Source: Datastream, authors calculations.

B Dynamic Factor Model for World Risky Asset Prices
– For Online Publication
Let p be an n-dimensional vector collecting monthly (log) asset price series p , where
t i,t
p denotes the price for asset i at date t. We assume
i,t
t t t
F is an (r ×1) vector of common factors (F = [f ,...,f ](cid:48)) that capture systematic
t t 1,t r,t
sources of variation among prices and are loaded via the coefficients in Λ that determine
how each price series reacts to the common shocks. ξ is a (n × 1) vector of idiosyn-
t
cratic shocks ξ that capture series-specific variability or measurement errors. We allow
i,t
elements in ξ to display some degree of autocorrelation while we rule out pairwise corre-
t
lation between assets assuming that all the co-variation is accounted for by the common
component. Both the common factors and the idiosyncratic terms are assumed to be zero
mean processes.
The factors are assumed to follow a VAR process of order p
t 1 t−1 p t−p t
where the autoregressive coefficients are collected in the p matrices Φ ,...,Φ , each of
1 p
which is (r×r); the error term ε is a normally distributed zero mean process with covari-
t
ance matrix Q. Any residual autocorrelation is captured by the idiosyncratic component
which we assume being a collection of independent univariate autoregressive processes.
In order to distinguish between comovements at different levels of aggregation we
model asset prices such that each series is a function of a global factor, a regional factor
and an idiosyncratic term. We do so by allowing the vector of common shocks to include
both aggregate shocks that affect all series in y , and shocks that affect many but not all
t
of them:
i,t i,g t i,m t i,t
In Eq. (B.3) the common component ΛF is separated into a global factor (fg) and a
t t
regional or market-specific factor (fm) which is meant to capture commonalities among
t
many but not all price series. Each p is thus a function of a global factor loaded by
i,t
all the variables in p , a regional or market-specific factor only loaded by those series in
t
p that belong to the (geographical or sector-specific) market m, and of a series-specific
t
factor.
Such hierarchical structure is imposed via zero restrictions on some of the elements in

Λ. In particular, we assume the common component to be partitioned into a global and
several regional factors. To this aim, let the variables in y be such that it is possible to
t
univocally allocate them in B different blocks or regions and, without loss of generality,
assume that they are ordered according to the specific block they refer to such that
y = [y1,y2,...,yB](cid:48). Eq. (B.1) can be rewritten as
t t t t
 
  fg
1,g 1,1  
 . 
f1

. t
p =  2,g 2,2  f2 +ξ . (B.4)
t 

. .
.
. .
.
...



 .
t 

t
.
  . 
B,g B,B fB
t
Moreover, further restrictions are imposed on the coefficient matrices in Eq. (B.2) such
that Φ (i,...,p) and Q are block diagonal.
i
The model in Eq. (B.1-B.2) can be cast in state space form and the unknowns con-
sistently estimated via Maximum Likelihood (Doz et al., 2011; Engle and Watson, 1981;
Reis and Watson, 2010; Ban´bura et al., 2011). The algorithm is initialized using principal
component estimates of the factors that are proven to provide a good approximation of
the common factors when the cross sectional dimension is large.43 We estimate the model
on the price series in (log) difference and obtain the factors via cumulation.44 We set
the number of lags in the factors VAR (p) to be equal to 1. We fit to the data a model
with one global and one factor per block/market; the parametrization is motivated by
the results in Table B.2.
Wefitthemodeltoavastcollectionofpricesofdifferentriskyassets. Thegeographical
areas covered are North America (US and Canada), Latin America (Brazil, Chile, Colom-
bia, and Mexico), Europe (Euro Area, UK, Switzerland and the Scandinavian Countries),
Asia Pacific (Japan, Hong Kong, Singapore, Korea, Taiwan), and Australia. The set of
commodities considered does not include precious metals. The time span covered is from
January 1990 to December 2012. In order to select the series that are included in the
global set we proceed as follows: first, for each market, we pick a representative market
index (i.e. S&P) and all of its components as of the end of 2012, we then select those
that allow us to cover at least 80% of the cross sectional observations by the beginning of
1990, and such that by 1995 we reach a 95% coverage.45 The procedure allows us to build
43Forni et al. (2000); Bai and Ng (2002); Stock and Watson (2002b,a) among others.
44Letx˜ ≡∆x denotethefirstdifferenceforanyvariablex ,thenconsistentestimatesofthecommon
t t t
factors in F can be obtained by cumulating the factors estimated from the stationary, first-differenced
t
model: p˜ =ΛF˜ +ξ˜. In particular, Fˆ = (cid:80)t F ˆ˜ and ξˆ = (cid:80)t ξ ˆ˜. Bai and Ng (2004) show that Fˆ
is a consistent estimate of F up to a scale and an initial condition F .
t 0
45While estimating the Dynamic Factor Model using Maximum Likelihood does not constrain us to

Table B.1: Composition of asset price panels
NorthAmerica LatinAmerica Europe AsiaPacific Australia Cmdy Corporate Total
1975:2010 114 – 82 68 – 39 – 303
1990:2012 364 16 200 143 21 57 57 858
Note: Composition of the panels of asset prices used for the estimation of the global factor. Columns
denote blocks/markets in each set, while the number in each cell corresponds to the number of elements
in each block.
a final dataset with an overall cross-sectional dimension of n = 858. The composition is
reported in Table B.1, where each category (in columns) corresponds to one of the blocks
(m) within the structure imposed.
Although all series included in the set are priced in US dollars, we verify that the
shape of the global factor is not influenced by this choice by estimating the same model
on price series in their local currencies (i.e. the currency in which the assets are originally
traded). The resulting global factor (not shown) is very similar to the one constructed
from the dollar-denominated set both in terms of overall shape and of peaks and troughs
thatperfectlycoincidethroughoutthetimespanconsidered. Intuitively, therobustnessof
the estimate of the global factor with respect to currency transformations comes directly
from the structure imposed in Eq. (B.3). The blocks/markets structure imposed roughly
coincides with currency areas, therefore this aspect is likely to be largely captured by the
regional factors (see Table B.1).
B.1 The Number of Factors
To choose the number of global factors we use a number of criteria and tests, collected
in Table B.2. The table reports the percentage of variance that is explained by the i-th
eigenvalue (in decreasing order) of both the covariance matrix and the spectral density
matrix, the information criteria in Bai and Ng (2002), where the residual variance of the
idiosyncratic component is minimized subject to a penalty function increasing in r, and
the test developed in Onatski (2009), where the null of r − 1 factors is tested against
the alternative of r common factors. The largest eigenvalue alone, in both the time and
frequency domain, accounts for about 60% of the variability in the data in the longer set
and about a fourth of the variation in the shorter, but more heterogeneous set; similarly,
the IC criteria reach their minimum when one factor is used, and the overall picture is
confirmed by the the p-values for the Onatski test.
work with a fully balanced panel, we want to ensure that none of the categories included in the set is
overrepresented at any point in time.

Table B.2: Number of Global Factors.
p p p
Matrix Density (2009) Test
(a) 1975:2010
1 0.662 0.579 -0.207 -0.204 -0.217 0.015
2 0.117 0.112 -0.179 -0.173 -0.198 0.349
3 0.085 0.075 -0.150 -0.142 -0.179 0.360
4 0.028 0.033 -0.121 -0.110 -0.160 0.658
5 0.020 0.024 -0.093 -0.079 -0.142 0.195
(b) 1990:2012
1 0.215 0.241 -0.184 -0.183 -0.189 0.049
2 0.044 0.084 -0.158 -0.156 -0.169 0.064
3 0.036 0.071 -0.133 -0.129 -0.148 0.790
4 0.033 0.056 -0.107 -0.102 -0.128 0.394
5 0.025 0.049 -0.082 -0.075 -0.108 0.531
Note: For both sets and each value of r the table shows the % of variance explained by the r-th
eigenvalue (in decreasing order) of the covariance matrix of the data, the % of variance explained by
the r-th eigenvalue (in decreasing order) of the spectral density matrix of the data, the value of the IC
p
criteriainBaiandNg(2002)andthep-valuefortheOnatski(2009)testwherethenullofr−1common
factors is tested against the alternative of r common factors.
C Bayesian VAR – For Online Publication
Let Y denote a set of n endogenous variables, Y = [y ,...,y ](cid:48), with n potentially
t t 1t Nt
large, and consider for it the following VAR(p):
Y = c+A Y +...+A Y +u . (C.1)
t 1 t−1 p t−p t
In Eq. (C.1) c is an (n × 1) vector of intercepts, the n-dimensional A (i = 1,...,p)
i
matrices collect the autoregressive coefficients, and u is a normally distributed error
t
term with zero mean and variance E(u u(cid:48)) = Σ. We estimate the VAR using standard
t t
macroeconomic priors (Litterman, 1986; Kadiyala and Karlsson, 1997; Sims and Zha,
1998; Doan et al., 1983; Sims, 1993); in particular, we use a Normal-Inverse Wishart
prior for the VAR coefficients. The Normal-Inverse Wishart prior takes the following

form:
Σ ∼ W−1(Ψ,ν) (C.2)
β|Σ ∼ N(b,Σ⊗Ω) (C.3)
where β is a vector collecting all the VAR parameters, i.e. β ≡ vec([c,A ,...,A ](cid:48)). The
1 p
degrees of freedom of the Inverse-Wishart are set such that the mean of the distribution
exists and are equal to ν = n+2, Ψ is diagonal with elements ψ which are chosen to be
i
a function of the residual variance of the regression of each variable onto its own first p
lags. More specifically, the parameters in Eq. (C.2) and Eq. (C.3) are chosen to match
the moments for the distribution of the coefficients in Eq. (C.1) defined by the Minnesota
priors:
 
i jk
0 otherwise
i jk λ2σ
k
otherwise,
i2 σ2
j
where (A ) denotes the element in row (equation) j and column (variable) k of the
i jk
coefficients matrix A at lag i (i = 1,...,p). When δ = 1 the random walk prior is
j
strictly imposed on all variables; however, for those variables for which this prior is not
suitable we set δ = 0 as in Ban´bura et al. (2010). On the right hand side of Eq. (C.4),
j
the variance of the elements in A is assumed to be proportional to the (inverse of the)
i
square of the lag (i2), and to the relative variance of the variables.
λ is the hyperparameter that governs the overall tightness of the priors. We follow
Giannone et al. (2015) and treat the λ as an additional model parameter which we
estimate in the spirit of hierarchical modelling.

D Other Charts – For Online Publication
Figure D.1: Global VAR (1) - World Aggregates
2 -0.5
i 0
o p
%
-2 -1.5
-0.5
-4
-2
-1
-6
10 20 80
s 0
t n 5 40
i -20
o
p 20
% 0 -40
-60
-20
-5
0 0
s
t 1
n
%-1
-10
-10
-2
1 15
0 10
0.5
s
o 0
p -0.5 -20
% -5
-1 -30 -10
-1
s t 2 -2
n
i -3
o
p 0 -4
%
-5
-2
-6

Figure D.2: Global VAR (1) - World Aggregates, 1990-2010
1 1
0.5 0.5
i
o p -2 -0.5 -0.5
% -1
-4 -1
-1.5
5 80
s t 0
n 0 40
%-5 -40 0
-60 -20
4 10
s 2 5 5
t
n
i 1
o
p 0 0 0
%
-1
-2 -5 -5
20 10
s 0.5 0 0
t
n i 0 -5
o p -20 -10
-0.5
% -15
-1 -40 -20
4 3
s 2
t 1
n
i o 0 0
p -1
%-2
-2
-4 -3

Figure D.3: Global VAR (1b) - World Aggregates
0 1
-0.5 0.5
0 0
s t n-2 -1 -0.5
i o -1.5 -1
p-4
% -2 -1.5
-6 -2
-8 -2.5 -2.5
20 80
n i -20 40
o
p -40 20
%
-60 0
-80 -20
-5
Global Real Economic Activity Ex US Total Nonrevolving Credit Global Credit Ex US
1 2 0
s 0
t n -2 -5
i-1
o -4
p
%-2 -6 -10
-3 -8
-4 -10 -15
Global Inflows Banks Global Inflows Non-Banks Leverage US Brokers & Dealers
0 0
-5 -5
s -10
t
n
i o-10 -10 -20
p
% -30
-15 -15 -40
Leverage EU Global Banks Leverage US Banks Leverage EU Banks
5 2
0 0
i o -2
p
%
-10 -4
-3
-15 -6 -4
-20 -8

Figure D.4: Global VAR (2) - FX Floaters Aggregates
4 1.5
-0.5
2 1
-4 -2.5
-1
-6 -3
10 80
s
i
o p -20 20
% 0 -40 0
-60 -20
-5
Global Real Economic Activity Ex US Floaters Domestic Credit Floaters Inflows All Sectors
3 5 5
2 0 0
s
t n 1 -5
i -5
o p 0 -10
%-1 -10
-15
-2 -15
-20
1 10
0.5 0 10
s
i
o p-0.5 -20 0
% -1 -30 -5
-10
-1.5 -40 -15
s t -2
n 2
i
o p 0 -4
%
-2 -6

Figure D.5: Global VAR (2b) - FX Floaters Aggregates
0 1
0.5
s-2 -0.5 0
t
n -0.5
%-6 -1.5
-2
-8 -1.5
6 20 100
4 0 80
n
p
%-2 -60 20
-4 -80 0
-6
Global Real Economic Activity Ex US Total Nonrevolving Credit Floaters Domestic Credit
s 0
t
p
-1
% -4 -5
-2
-6
Floaters Inflows Banks Floaters Inflows Non-Banks Leverage US Brokers & Dealers
0 0
-2
s t -4 -10
n
p -8
% -10 -30
-10
-12 -40
Leverage EU Global Banks Leverage US Banks Leverage EU Banks
0 0
n
i o-10 -2 -2
p
%-15 -4 -3
-20 -6 -4

Figure D.6: EA-Focus VAR - Euro Area Aggregates
0.5
s
t n i-2 -0.5 0
o
p -0.5
-1
%-4
-1
-1.5
Global Factor Global Risk Aversion Global Real Economic Activity Ex US
80 2
s 60
o
p -40 20 0
%
-60 0
-1
EA Domestic Credit EA Inflows Banks EA Inflows Non-Banks
5 0 0
s -5
t -5
p -10
%-5 -15
-15 -20
GER Corporate Spread EA Policy Rate DAX Stock Market
s 0.5 -0.5
t n 0
i
%
-0.5 -1.5 -20
EUR to 1 USD Leverage US Brokers & Dealers Leverage EU Global Banks
5 5
s 0
t n 0
i 0
o p -10 -5
%-5
-20 -10
s t 0 -2
n
i-1
o
p -2 -4
%
-3
-6

Figure D.7: Global VAR (1c) - World Aggregates, Focus on Responses
of EA and UK Financial Conditions and Monetary Policy
0.2
s 0 0 0.5
t
% -0.6 -0.5
-4
-0.8
Global Factor Global Real Economic Activity Ex US Global Domestic Credit
s 0 1.5 6
t
n-20 1 4
i
o p-40 0.5 2
% 0 0
-60
-0.5
-2
Global Inflows All Sectors GZ Credit Spread UK Policy Rate
10 1 1
s 0.5
o
p
0 -0.5
% 0
-1
-0.5
FTSE All Share GBP to 1 USD UK Corporate Spread
10 1
s 5 0.5
t 0
n
p
-10
% -0.5
-15 -5
EA Policy Rate DAX Stock Market EUR to 1 USD
10 5
s
t 0
n i 0
o-0.5
p -5
% -10
-1 -10
GER Corporate Spread
0.8
0.6
s
t 0.4
n
i o 0.2
p
%
-0.2
-0.4
horizon

E Robustness: Global Growth and Global Risk Aver-
sion – For Online Publication
E.1 Global Growth
Figure E.1 reports IRFs to a contractionary US monetary policy shock of a variety of
global growth measures. The IRFs are obtained by sequentially substituting a different
growth variable in the same VAR, the composition of which is equal to that of Figure D.1
(our benchmark global VAR). All VARs are estimated over the sample 1980:01-2010:12
with the exception of the one that includes the World Production (CPB-NBEPA) which
is only available from 1990:01.
The measures reported in the figure are:
• World industrial production measured as the weighted average of the IP of OECD
countries + 6 EMEs (originally distributed by the OECD, updated in Baumeister
research;
• Global real activity as measured in Kilian (2009) updated and corrected in Kilian
data-sets;
• World industrial production as weighted average of IP indices of both AEs and
EMEs, measured by the CPB Netherlands Bureau for Economic Policy Analysis
and distributed in their World Trade Monitor publication, available at https://
• IP for the EA, fixed composition. The variable is NSA at source (ECB data series
ID: STS.M.I8.W.PROD.NS0020.3.000), we have seasonally adjusted it prior to its
inclusion in the VAR;
• UK Index of Production as distributed by the UK Office for National Statistics;
• Global real economic activity Ex US constructed as the component of the Baumeis-
ter and Hamilton (2019) series that is orthogonal to the US cycle. This is our
benchmark variable used in Section 3.
Results indicate that global production seems to contract following a US monetary
tightening mostly as a result of the US slowdown. While the two global IP measures
decline significantly, the component that is orthogonal to the US cycle (last panel) is not
affected in a significant way. Kilian’s measure that is based on nominal shipping costs

Figure E.1: Alternative Measures of Global Growth
OECD + 6 IP (Baumeister & Hamilton) Index of Global Real Activity (Kilian) World Production (CPB-NBEPA)
2 30 4
1 20 2
s 0 10 0
t
n
i 0
o -2
p-1
% -10
-4
-2
-20
-6
-3 -30
EA Industrial Production UK Industrial Production Global Real Economic Activity Ex US
2 2 3
1 2.5
1 2
1.5
s -1 0 1
t-2
n i o-3 -1 0.5
p 0
%-4 -2 -0.5
-5 -1
-6 -3 -1.5
-7 -2
-4
Note: Responses of alternative measures of global growth to a US contractionary monetary policy shock
that induces a 1% increase in the policy interest rate. Median IRFs with posterior coverage bands at
68%and90%levels. Theshockisidentifiedusingahigh-frequencyexternalinstrument. CombinesIRFs
estimatedfromdifferentVARsallestimatedoverthesample1980-2010withtheexceptionoftheonethat
includes the World Production (CPB-NBEPA) which is only available from 1990. With the exception of
the global growth variable the composition is identical to that of Figure D.1.
is only marginally affected. On the other hand, production indices in the UK and the
EA do contract with some delay. Figure 10 in the paper however also shows that the US
monetary contraction significantly affects financial conditions in both the UK and EA,
which in turn may be detrimental for real activity.
E.2 Global Risk Aversion
In general asset pricing models, the residuals of the projection of asset prices on realized
variance can be decomposed into news about future expected GDP growth, changes in
risk-free discount rates, and changes in risk aversion (see e.g. Zhou, 2018).46
46Some papers which posit a constant level of risk aversion add another term, time-varying macroeco-
nomic uncertainty. Instead, we allow for time-varying risk aversion as in Bekaert et al. (2013); Bekaert
and Hoerova (2014). We rationalize the time variation using a model where fluctuations in risk aversion
reflect the time-varying importance of different financial intermediaries in international markets (see

Our benchmark risk aversion proxy ignores fluctuations in contemporaneous discount
rates and future expected GDP growth, in line with the simple model of Section 4.47 It
is computed from the centered residuals of the following regression:
GFAC = α+βln(GRVAR )+ε ,
t t t
where GFAC is our global factor (in log units) and GRVAR is the measure of realized
t t
variance obtained from the returns of the Global MSCI Index.
In order to account for these more general models, we construct an alternative aggre-
gate global risk aversion proxy by regressing the global factor on global realized variance,
and also on discount rates and survey forecasts of GDP growth for four countries which
we take to be representative of our global set: the US, the UK, Germany and Japan.
Specifically, we recover a refined proxy for risk aversion as the centered residual of the
following regression:
(cid:88) (cid:88)
GFAC = α+βln(GRVAR )+ γ DR + δ E [GDP ]+ε ,
j j
where j denotes the following 4 countries: US, GER, UK, JP; DR are discount rates (av-
t
eragesofdailyfigures)obtainedfromtheStLouisFedFREDdatabase,andE [GDP ]
t j,t+12
are monthly survey forecasts for GDP growth a year (12 months) ahead, constructed from
the calendar-year forecasts distributed by Consensus Economics. Both regressions are es-
timated at monthly frequency.
The two proxies are plotted in the bottom panel of Figure E.2 as a solid and dashed
line respectively. The new series shares many similarities with our original one, with some
small differences; there is for example a quicker reversal to a low-perceived-risk regime
following the global financial crisis, and higher risk-aversion in the early 2000s.
Figure E.3 reports IRFs to a contractionary US monetary policy shock of a variety of
riskaversionmeasures. TheIRFsareobtainedbysequentiallysubstitutingadifferentrisk
aversionvariableinthesameVAR,thecompositionofwhichisequaltothatofFigureD.1
(our benchmark global VAR). All VARs are estimated over the sample 1990:01-2010:12.
The measures reported in the figure are:
• Our benchmark proxy for aggregate risk aversion;
• A more general proxy for aggregate risk aversion that also controls for discount
rates and GDP growth forecasts in the 4 countries listed;
Section 4).
47We note that our BVAR controls for past discount rates and past GDP growth.

Figure E.2: global factor decomposition (including controls)
Global Realized Variance
1990 1992 1994 1996 1998 2000 2002 2004 2006 2008 2010 2012
3 baseline
with controls
-1
-2
-3
1990 1992 1994 1996 1998 2000 2002 2004 2006 2008 2010 2012
Note: [top panel] Monthly global realized variance measured using daily returns of the MSCI Index.
[bottom panel] Index of aggregate risk aversion calculated as (the inverse of) the residual of the
projection of the global factor onto the realized variance. Solid line: baseline estimate of Section 2;
Dashed line: includes controls for discount rates and expected growth. Shaded grey areas highlight
NBER recession times. Source: Global Financial Data and authors calculations.
• The risk aversion index for the US market constructed in Bekaert et al. (2019)
• The risk aversion index for the US market constructed in Bekaert et al. (2013) as
a variance risk premium along the lines of our benchmark aggregate risk aversion
• A measure of risk appetite distributed by CrossBorder Capital Ltd and calculated
as the difference between the Equity Exposure Index (based on the balance sheet
exposure of all investors (by type) in the asset class) and the Bond Exposure Index
(equivalent of the equity exposure index for bonds);
vix-options-and-futures/vix-index/vix-historical-data).
ThechartconfirmsthataUSmonetarycontractiontriggersanincreaseinriskaversion
(decline in risk appetite), regardless of the specific measure that is used.

Figure E.3: Alternative Measures of Risk Aversion
Benchmark Risk Aversion Proxy Benckmark RAP + Controls RA Index (Bekaert Engstrom & Xu)
80 30
60 20
s t 40 10
n
i o 20
p 20 0
%
0 -10
-20
-20 -20
RA Index (Bekaert Hoerova & Lo Duca) Risk Appetite (CrossBorder Capital Ltd) CBOE VIX Index
40 40 15
20 10
s 20
t
p
% 0 -20
-10
-40
-20 -5
-60
Note: Responses of alternative measures of risk aversion to a US contractionary monetary policy shock
that induces a 1% increase in the policy interest rate. Median IRFs with posterior coverage bands at
68%and90%levels. Theshockisidentifiedusingahigh-frequencyexternalinstrument. CombinesIRFs
estimatedfromdifferentVARsallestimatedoverthesample1990-2010: withtheexceptionoftheglobal
growth variable the composition is identical to that of Figure D.1.