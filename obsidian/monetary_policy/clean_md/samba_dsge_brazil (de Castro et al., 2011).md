ISSN 1518-3548
4
ee
BANCO CENTRAL DO BRASIL
Working Paper Series
SAMBA: Stochastic Analytical Model with a Bayesian Approach
Marcos R. de Castro, Solange N. Gouvea, André Minella,
Rafael C. Santos and Nelson F. Souza-Sobrinho
April, 2011

ISSN 1518-3548
CGC 00.038.166/0001-05
Working Paper Series
Brasilia
n. 239
Apr.
2011
p. 1-138

Working Paper Series
Editor: Benjamin Miranda Tabak — E-mail: benjamin.tabak @bcb.gov.br
The Banco Central do Brasil Working Papers are all evaluated in double blind referee process.
Reproduction is permitted only if source is stated as follows: Working Paper n. 239.
Authorized by Carlos Hamilton Vasconcelos Aratijo, Deputy Governor for Economic Policy.
General Control of Publications
Banco Central do Brasil
Secre/Surel/Cogiv
SBS — Quadra 3 — Bloco B — Edificio-Sede — 1° andar
Caixa Postal 8.670
70074-900 Brasilia — DF — Brazil
The views expressed in this work are those of the authors and do not necessarily reflect those of the Banco Central or
its members.
Although these Working Papers often represent preliminary work, citation of source is required when used or reproduced.
As opinides expressas neste trabalho sGo exclusivamente do(s) autor(es) e ndo refletem, necessariamente, a visdo do Banco
Central do Brasil.
Ainda que este artigo represente trabalho preliminar, é requerida a citacGo da fonte, mesmo quando reproduzido parcialmente.
Consumer Complaints and Public Enquiries Center
Banco Central do Brasil
Secre/Surel/Diate
SBS — Quadra 3 — Bloco B — Edificio-Sede — 2° subsolo
70074-900 Brasilia — DF — Brazil

SAMBA: Stochastic Analytical Model
with a Bayesian Approach
Marcos R. de Castro, Solange N. Gouvea, André Minella,
Rafael C. Santos, Nelson F. Souza-Sobrinho*
This version: June 16, 2011
The Working Papers should not be reported as representing the views of the
Banco Central do Brasil. The views expressed in the papers are those of the
authors and do not necessarily reflect those of the Banco Central do Brasil.
Abstract
We develop and estimate a DSGE model for the Brazilian economy, to be used as part of the
macroeconomic modeling framework at the Central Bank of Brazil. The model combines the
building blocks of standard DSGE models (e.g., price and wage rigidities and adjustment costs)
with the following features that better describe the Brazilian economy: (i) a fiscal authority
pursuing an explicit target for the primary surplus; (ii) administered or regulated prices as
part of consumer prices; (iii) external finance for imports, amplifying the effects of changes in
external financial conditions on the economy; and (iv) imported goods used in the production
unction of differentiated goods. It also includes the presence of financially constrained house-
holds. We estimate the model with Bayesian techniques, using data starting in 1999, when
inflation targeting was implemented. Model evaluation, based on impulse response functions,
moment conditions, variance error decomposition and initial forecasting exercises, suggests that
the model can be a useful tool for policy analysis and forecasting.
Keywords: DSGE model; Bayesian estimation; inflation targeting; Brazil
JEL Classification: E17, E30, E52
*All authors: Research Department, Central Bank of Brazil. This project has benefited from the visits
of Jaromir Benes, Larry Christiano, Stephen Murchison, and Alessandro Rebucci, courses given by Fabio
Canova, Kai Christoffel, Michel Juillard, Tommaso Monacelli, Roberto Motto, and Carl Walsh, and a visit
to the Central Bank of Chile, to which we are very grateful. We are also grateful to Tomié Sugahara and
José R. da Costa e Silva for their participation in early stages of the project, and Angelo Fasolo for his
comments and suggestions.

1 Introduction
There is a considerable debate on the ability of dynamic stochastic general equilibrium
(DSGE) models to fit the data well and provide useful (potentially novel) insights to pol-
icymakers, despite the theoretical advantages of microfounded models. However, recent
advances in modeling and estimation techniques have improved the empirical coherence of
DSGE models. As a result, they are becoming an important policy tool for central banks
around the world.
In fact, in recent years, many central banks have put great effort on developing applied
DSGE models.'! In this paper, we build and estimate a DSGE model for the Brazilian
economy, which we call SAMBA — Stochastic Analytical Model with a Bayesian Approach.
The estimation uses Bayesian techniques, and the sample starts in 1999, when inflation
targeting was adopted. The model was developed to be used as part of the macroeconomic
modeling framework of the Central Bank of Brazil (BCB), providing support for policy
analysis and forecasting.
The model embeds prominent features of the Brazilian economy, such as (i) the fiscal
authority pursues an explicit target for the primary surplus-to-GDP ratio, in accordance
with the fiscal regime in place since 1999; and (ii) significant part of consumer prices is
regulated by the government (administered or regulated prices), following contract rules
or other non-market based procedures. The model also includes two other features that
are less usual in other DSGE models, but relevant in the case of the Brazilian economy.
First, in Brazil and many other countries with relatively large manufacturing sectors, most
of imports are inputs used in the production function rather than final consumption goods.
Hence, following McCallum and Nelson (2000) and Murchison and Rennison (2006), we treat
imports as inputs that are used to produce differentiated sectoral goods. As a consequence,
the local-currency price of imports are a key component of the marginal cost of domestic
‘For instance, the central banks of Canada (ToTEM), Chile (MAS), Colombia (PATACON), England
(BEQM), Euro Area (NAWM), New Zealand (KITT), Norway (NEMO), Peru (MEGA-D), and Sweden
(RAMSES).

firms that face price rigidity. Second, as in the data we assume that a fraction of imports
must be financed abroad so that shocks to external financial conditions — which can be
interpreted as innovations to trade credit — have an extra channel of transmission to the
domestic economy. In fact, this working capital constraint amplifies the effects of shifts in
the country risk premium on aggregate investment.
In developing the building blocks of our model, we have borrowed many insights from
Adolfson et al. (2007, 2008), Christiano et al. (2005), Christoffel et al. (2008), Medina and
Soto (2007), Murchison and Rennison (2006), and Smets and Wouters (2003, 2007). The fea-
tures of our small open economy model include wage and sectoral price rigidities, as well as
real frictions in the form of habit persistence in consumption and adjustment costs in invest-
ment, exports and imports. We have both monetary and fiscal authorities, whose behavior
is modeled according to the actual institutional arrangements, that is, inflation targeting
and targets for the primary fiscal balance. We also assume that a fraction of households
is financially constrained, which breaks up Ricardian equivalence, and is consistent with
the fact that a large proportion of Brazilians have no or limited access to credit. Further-
more, the country risk premium responds not only to domestic fundamentals (net external
debt-to-GDP ratio) but also to shifts in foreign investors’ preference for risk.
In terms of estimation procedures, Bayesian techniques have shown to be very suitable
for the estimation of DSGE models. These models often have a large number of parameters
— many of which are weakly identified — and the sample size is usually small. This is
particularly relevant for the case of Brazil whose sample size (1999Q3-2010Q2) is quite small
compared with the data span available in developed economies. Furthermore, Bayesian
techniques formally incorporate expert’s knowledge in the form of priors, which not only
complement the information available in the data but also help to estimate otherwise weakly
identifiable parameters. Judgment is put into practice by including beliefs to which some
level of accuracy is attached. This procedure is implemented in a coherent and clear-cut way
in the Bayesian estimation. Moreover, the resulting posterior distributions of the parameters

are used in the construction of confidence intervals for different exercises.
We assess the performance of the model through the behavior of the underlying impulse
response functions, moment conditions, variance error decomposition, and forecasting exer-
cises. Overall, the evaluation suggests that the model can be a useful tool for policy analysis
and forecasting at the BCB. In particular, it can be used to assess the impact of different
shocks to the economy. The impulse response functions generated by the model, even con-
sidering the whole set of shocks, are, in general, consistent with the theory and results for
other countries, as well as with the empirical evidence available for Brazil. We also conduct
initial forecasting exercises that seem promising.
The current macroeconomic modeling framework at the BCB uses a suite of models, in-
cluding small and medium-size semi-structural models, vector autoregression (VAR) models
and auxiliary structures that are used to answer specific policy issues. The DSGE model is
an important additional tool in that framework. It provides a theoretically consistent device
to deal with a broad range of issues.
Section 2 describes the model and equilibrium conditions. Section 3 provides the data
and estimation details. Section 4 presents the main results, and Section 5 concludes. The
appendix brings extra material, including the equilibrium conditions along the balanced
growth path, the steady state and log-linear version of the model.
2 Model Overview
SAMBA is a small open economy model that combines what are now standard features of
DSGE models — such as wage and price rigidities, habit persistence in consumption and
capital adjustment costs — with specific features of the Brazilian economy, such as firms
subject to regulated prices, imports in the production process, external finance of imports
and a country-specific fiscal rule.
In the model, there are several types of agents: households, domestic producers, im-
porting firms, and government. There are two types of households. Both have the same

endowment of time, which is allocated between labor and leisure, but differ with respect to
their participation in capital, asset and labor markets. The first type — optimizing house-
holds — owns the capital stock and all shares of the firms and are able to accumulate financial
assets. The second type — rule-of-thumb households — are financially constrained. They do
not have access to financial markets and simply consume whatever labor income they earn.
Domestic producers are classified into three groups: domestic input producers, interme-
diate good producers, and final good assemblers. Producers of intermediate goods, in turn,
are grouped into four different sectors, according to the final good supplied: private con-
sumption goods, government consumption goods, investment goods, and exported goods.
We assume different technologies for producing each good, and the production process in
each sector is carried out in three stages. In the first stage, a representative firm produces a
non-tradable domestic input using capital and labor. Still in the first stage, importing firms
buy differentiated goods from abroad and transform them into a homogeneous input to be
used in the production process. In the second stage, a large number of intermediate good
producers combine domestic and imported inputs and produce different varieties. The share
of domestic and imported inputs varies across sectors. In the third and final stage, sectoral
assemblers combine the intermediate varieties into sectoral homogeneous goods, which are
sold domestically and abroad.
Physical capital, domestic input and all final goods are traded in competitive markets.
On the other hand, workers, importers and domestic intermediate good producers are mo-
nopolistic competitors, facing wage or price rigidity a la Calvo (1983). Therefore, there are
two layers of nominal rigidity in the model. The first layer comprises stickiness of input
prices — wages and import prices. The second layer involves stickiness in the prices of the
intermediate varieties used to produce the four final goods. As in Christiano et al. (2007),
all prices are set in the currency of the buyer ("pricing to market"), including exports.
The government in the model is represented by fiscal and monetary authorities. The
fiscal authority levies lump-sum taxes on optimizing households, makes transfers to firms,

and consumes government goods. It also levies a net income tax on rule-of-thumbers, which
can also be considered as net out of government transfers. Most of the transfers in Brazil
are directed to lower income people, and therefore with less access to financial and credit
markets. For parsimony reasons, we preferred to keep the tax structure in the model as
simple as possible. Government also issues domestic bonds, which are held by optimizing
households. Decisions regarding government spending are subject to an empirical fiscal rule,
which is meant to describe the actual behavior of the fiscal authority, whereby it targets the
primary surplus-to-GDP ratio. The monetary authority, in turn, targets the CPI inflation
by setting the interest rate according to a forward-looking Taylor-type rule, in line with the
inflation targeting framework.
Agents in the domestic economy take as given the prices and allocations of the world
economy. For the sake of parsimony, we treat the variables describing the rest of the world
as exogenous stochastic processes. However, in the background and whenever necessary
we treat domestic and foreign economies as having analogous features, i.e., similar type of
agents and production structure. For instance, Brazil’s imports are inputs to the domestic
production, and exports are inputs to the production of foreign firms. The main linkages
between the domestic and the world economy arise from international trade in goods, asset
markets and loans. Domestic households issue foreign-currency bonds abroad — external
bonds for short — and domestic firms borrow from abroad through foreign-currency loans
to finance imports — external finance or loans for short. We assume that asset markets
are incomplete and the law of one price does not hold, so the model features imperfect risk
sharing and partial exchange rate pass-through in the short run.
In the following subsections we describe in detail the problems and constraints faced by
each economic agent, and derive the associated equilibrium conditions. For ease of exposi-
tion, we adopt the following conventions. We express the level of growing (non-stationary)
variables by upper-case letters, say X;, and the level of detrended (stationary) variables by
adding tilde, X;. The long-run (steady state) level of detrended or stationary variables are

expressed without subscript t, X, and the linear or log-linear deviations from the steady
state are represented by lower-case letters without tilde, x;. We use the letter 7 to denote
the level of the shock process S, and z? to denote its linear version. Innovations to the shock
processes are represented by ¢?. Additionally, we use Q! to denote the price of good H
relative to the price of consumption goods, which is used as numéraire in the model. We
index foreign variables by an asterisk ‘*’
, say X;*, nominal variables by the superscript ‘”’,
X;’, and optimally chosen prices by a star ‘*’, X/*. In our timing convention, flow variables
decided in period t are indexed by t, whereas stock variables (e.g., capital and bond holdings)
chosen at ¢ are index by t + 1. Whenever required we use subscript 7 to identify economic
agents and the subscript 2 to denote time window. In the model, time is equivalent to a
calendar quarter and is indexed by ¢t = 0,1, 2,... We ignore population growth.
2.1 Households
The economy is populated by a mass one of households indexed by j € [0,1]. Optimizing
households (O) account for a fraction 1 — wprr of the population, and rule-of-thumb house-
holds (RT) account for the remaining share. As mentioned before, optimizing households
are not financially constrained and choose their consumption, savings and investment in a
forward-looking manner. These households use three different assets or savings instruments
— physical capital, non-contingent one-period government bonds and non-contingent one-
period bonds issued abroad — to smooth their consumption overtime. On the other hand,
rule-of-thumb households have no access to credit, capital and asset markets and do not earn
firm dividends. They simply spend their entire labor income on consumption goods. We
also assume that both types of households supply differentiated labor services, setting their
wages in a monopolistically competitive labor market, subject to Calvo-type contracts.

2.1.1 Optimizing Households
Each optimizing household, indexed by 7 € O, chooses consumption, physical capital and
financial assets to maximize the expected discounted flow of utility,
max Eo Ss" BrulCya, Nj),
t=0
{Cj,eBy tr BF rg Ky tt1ly,eh
subject to the flow budget constraint
Byes SiBr ay
t “jt t “jt R,SP R: SB
WE Nie + RE” Ky + Big + SB, + DY, -— TO” ENV © O,
< (1)
and to the law of motion of capital
I.
Zi Lj t-1
where Eo is the expectations operator, 3 € (0,1) is the time discount factor, Cj, is the
consumption level, and N;, is differentiated labor. In the budget constraint, P© is the price
of consumption goods, J; is investment, P/ is the price of investment goods, B;, denotes
one-period government domestic bonds, R; is the domestic gross interest rate, S? is the
domestic risk premium, S; is the exchange rate (defined as units of domestic currency per
units of foreign currency), B=, represents one-period foreign-currency bonds issued abroad,
R* is the external gross interest rate, S?"is the country risk premium, W;', is the household-
specific nominal wage rate, RK ” is the net nominal rental rate of capital, Kj is physical
capital, D’, denotes nominal dividends received from the firms, Te is lump-sum nominal
net taxes, and =, are nominal state-contingent securities. We adopt the convention that
Bj, and B;, represent nominal bonds issued in ¢— 1 and maturing in t, and Kj, are capital
holdings from t — 1. So Bji41, Bjz4, and Aj,,1 are decided in t. In the law of motion of
capital, 6 is the depreciation rate of capital, 9(.) is a convex adjustment cost, and Z/ is an
investment-specific technology shock. The function S(.) satisfies S(Z7) = S’(Z7) = 0 and
S"(Z4) = 0; > 0, where Z% is the steady-state growth rate of the technology process Z;,
which we define in more details below.

We assume the following functional form for the instantaneous utility function, augmented
by external habit persistence:
(Cit — KC? 1)?
l-o
W
1+”
u(Cy, Nye) = Zp Zy* (Nie) , (3)
where C? is the average consumption of optimizing households, Z© is a shock to the house-
hold’s intertemporal preference, Z; is the level of technology, o is the inverse of the in-
tertemporal elasticity of substitution, ~ > 0 is a weight parameter, « € [0,1) is a parameter
governing the external habit persistence, and 7 is the inverse of labor supply elasticity. As
in Erceg et al. (2006), we assume that preferences over leisure shift with the level of technol-
ogy so that the model is consistent with balanced growth path, even when preferences over
consumption are not logarithmic.
The household purchases consumption goods Oj, at the price level P’, investment goods
Ij, at the price P/, buys or sells discounted values of one-period government bonds Bj44+1,
and buys or sells one-period foreign-currency bonds B, issued abroad. Government bonds
pay the risk-free interest rate R; (in gross terms), which is also the interest rate controlled by
the monetary authority. However, the effective return received by households also includes
an exogenous financial intermediation premium, denoted by S?, which we interpret as a
domestic risk premium (see Smets and Wouters (2007) and Christoffel et al. (2008)). It
represents a wedge between the interest paid by the government and the interest received by
the household. This premium is rebated in a lump-sum way to optimizing households, being
included in To". In practice, it can also be used as capturing changes in financial conditions
that affect both consumption and investment at the same direction. In fact, a positive shock
to S? reduces both consumption and investment, generating a positive co-movement between
those two aggregate demand components, in contrast to the intertemporal preference shock,
which generates a negative relationship.
The value in domestic currency of bonds issued abroad is given by S;Bj,,,. The effective
return on these bonds depends on a external premium over the riskless international interest
rate (hereafter, country risk premium), denoted by S?°. For simplicity, we assume that

households do not internalize the fact that their demand for foreign bonds may shift the
country risk premium.
Optimizing households have four sources of income. The first is labor income, which de-
pends on the household-specific nominal wage rate W;", and the amount jz of differentiated
labor services provided to firms. The second is capital income, from renting physical capital
Kj at the competitive net nominal rental rate of capital RK The third source of income
is the return accrued from bond holdings, and the last one is dividends D?, received from
firms. There are two remaining factors that also affect the nominal income of optimizing
households: a net lump-sum nominal tax To" levied by the government, which is the same
across optimizing households, and nominal state-contingent securities &’',. These securities
are traded amongst optimizing households and provide full insurance against labor income
risk. They are just a technical device to make aggregation tractable under wage rigidity.”
We assume that capital accumulation is costly and subject to investment-specific inno-
vations. As usual, the adjustment cost given by the function S(.) helps to replicate the
hump-shaped response of investment to monetary policy shocks.
For convenience, we split households’ decisions into two steps. In the first step, they take
the labor income as given and choose the optimal allocations of consumption, investment
and assets, and in the second stage they choose their desired wage. The first-order conditions
associated with the choices of Ch, By isi, Beiy1, Ajry1 and Ij, are, respectively:
Mig = ZE (Che — C24), 4
PE on op
Aja = BE, Ajeya Pc RS; ’ 3)
t+1
Ajt = BE, ( jt+1 — R* SP ) 5 6
J Jit Po, Si tt
Tn particular, they ensure that the equilibrium consumption of all optimizing households is the same,
regardless of their labor income. Otherwise, we would have to keep track of the wealth distribution arising
from agent heterogeneity. To simplify the model even further, we assume that physical and financial wealth
is equally distributed across optimizing households at the beginning of time and that dividends received from
firms in each period are also equally distributed across optimizing households.

Kyn
Rei
C
Pisa
AjQh = BE Aj t41 ( + Or i(l — | ) (7)
I
Fe
it pe
P;
I; 1 I; t+1 °
A. Q* S! ( Jitt+ ) ( Js Z!
WEI Zh alia Zh alia an
Tj4 Ti i
it Zi Tjia-1 Zi Tji-1 Zi Tj
where A;,/P° is the Lagrange multiplier associated with jth household’s budget constraint,
and QN is the Lagrange multiplier associated with the law of motion of capital. The former
is the real shadow price of the consumption good, whereas the latter is the real shadow value
of capital.
Along the symmetric equilibrium, all optimizing households make identical choices, thus
we can drop the subscript j from the equations above. With this in mind, the per capita
consumption of optimizing households, C?, implied by conditions (4) and (5) is given by the
following consumption Euler equation:
C (pO O \72 C ) o\-7 RSP
Z; (C; — KCY 1) = BE, |Z, (Cha — KC; ) ,
(9)
Me
where IIf,, = PS, /P£ is the gross CPI inflation rate between periods t and t + 1.
Combining (5) and (6) yields the uncovered interest rate parity (UIP) condition:
B * OB*
EL; (Fe Ae) = i, (= Fes Ave) ;
+1
We define the consumption-based real exchange rate as the price of the foreign consumption
good P@", expressed in local currency 5;P,°", relative to the price of the domestic consump-
tion good as
SPO
Q: = me ’
t
and plug it into the UIP condition in order to obtain a convenient expression for the real
(10)
exchange rate in terms of the real interest rate differential (UIP in real terms):
E A =F A 11
t ( me. t+1 t Q; me t+1 ]> ( )

where H@” = P@ /P©,. We assume that 52° depends only on aggregate variables describing
t t t-1 t
both domestic and external fundamentals as follows:
SP = 5 {exp [—yp (Br, — BY) + yy (Vi —V)]} Ze, (12)
where y%, and yj, are positive parameters, Bj, is net foreign assets-to-GDP ratio, V;* de-
scribes foreign investors’ risk aversion, and Z?" is a shock that captures movements in the
country risk premium associated with domestic exogenous factors, such as political uncer-
tainty and others. The variables S?", B*’and V are the corresponding steady-state values.
Net foreign assets-to-GDP ratio is defined as B;?,; = are, where P* is the GDP deflator
and Y; is real GDP. The equation describes what the literature calls pull and push factors,
corresponding respectively to domestic and external factors. The external debt-elastic coun-
try risk premium usually enters small open economy models as a technical device to render
net foreign assets stationary. Moreover, there is empirical evidence that the country risk
premium of emerging-market economies like Brazil reacts to the net foreign assets position
(pull factor). By the same token, the evidence suggests that movements in foreign investors’
attitude towards risk also shift the country risk premium (push factor). On the other hand,
we assume that the domestic risk premium follows an autoregressive process of order one -
AR(1):
SP (SB) Pe (52.,)°" exp {e?}. (13)
Turning to the wage setting, we can think of an "employment agency" that aggregates the
differentiated labor services provided by each household into a homogeneous labor input N;,
which is then supplied to domestic firms in competitive input markets (Erceg et al. (2000)).
We assume that the employment agency combines the differentiated labor services through
a Dixit-Stiglitz aggregator:
1 ep, -1 Wi
N= (/ (Nix) & ») ; (14)
0
where e!” > 1, Vt, is a time-varying elasticity of substitution that may shift the wage markup.
t

The optimization problem of the employment agency is given by:
Ww
“
max ¢ W; | (Nj) @ - | WiNG AG ?
N3j,t 0 0
where W,” is the aggregate nominal wage rate.
We assume that the employment agency makes deals with firms on behalf of all households
— optimizers and rule-of-thumbers. The solution to the problem faced by the employment
agency implies the following demand for the differentiated labor service of the jth household:
Ww
wr\~*
w= (Ge) NM, Vj € [0,1]. (15)
W}
The break-even condition for the competitive employment agency pins down the aggregate
wage index:
1
1 WV
we= (fom ta) (16)
We assume that optimizing households face Calvo lottery for wages. In each period,
with probability 1 — Oj, household 7 € O may be able to renegotiate its nominal wage
contract with the employment agency. With probability Oy, household 7 € O is unable
to optimally change its nominal wage, but it is permitted to updated the wage contract
taking into account past wage inflation, CPI inflation and productivity gains, according to
the following indexation rule:
Wee = ry jaa VI EO, (17)
J
where Y! is the indexation factor, given by:
w 1l-w
ri" = (11; ,) " (277, 11e,) ", (18)
where wy € [0,1] is an indexation parameter, HW” = W?/W,, is the gross inflation rate of
nominal wages, and 77 = Z;/Z,_, is the stochastic and time-varying gross growth rate of
technology (proxy for labor productivity growth). Since nominal wages embody productivity

growth, this indexation rule ensures that in steady state all nominal wages grow at the rate
Z“1II°. The rule considers the fact that workers try to keep the purchasing power of their
wages and, at the same time, take into account the behavior of aggregate wage, as an
indicator of labor market conditions or due to relative wage concerns.
Each optimizing household who is able to renegotiate optimally its wage contract eval-
uates the disutility of labor relative to the utility arising from the real labor income. The
optimal wage-setting problem is the following:
- j = W 1+ Wir .
E Oy By’ | -—Z9 Zk? —— (Nji3) 7" + Ae (| SEN: Vj EO
{wn} >a w) t Atri | ra jtti) + Mey PS, jtt+i}|> VI )
i=0
subject to the wage demand equation (15) and the wage indexation rule (17). The first-order
condition describing the optimal wage-setting decision is the following in the symmetric
equilibrium:
i njx\ ev, ti i
Et Ss" (OwB) | Neva (ef, — 1) (We) ( 7a ) pe Nizi| = (19)
1=0 ti ti
ioe) yw ef (+n)
a —o nk —el\, _ tte
Ee » (Ow 3) ZeiZiri ei (Wer) “ne ( on ) Ne ;
i=0
where
1, i=
w
Tete = Tins (Ma) (ZZ aaa) O02
is the wage indexation factor, accumulated between t and t +7, and W,"” is the optimal
wage.
Using equations (16) and (17) and the fact that the optimal wage is the same across
optimizing households, we obtain the law of motion for the wage rate of optimizing households
1
w 1-eW
wee = [are yh + ewe ym?
(20)
Thus, equilibrium conditions for optimizing households can be described by equations
(4), (7), (8), (9), (11), (18), (19), and (20), plus the law of motion of capital (2).

2.1.2. Rule-of-Thumb Households
Rule-of-thumb households just consume their disposable labor income as follows:
PEC = (1-7) WEN, Vi € RT,
where T/*” is the marginal net tax rate (out of transfers) levied by the government on the
labor income of rule-of-thumbers. As in Medina and Soto (2007), we assume that each rule-
of-thumber sets its wage equal to the average wage rate of optimizing households, that is,
ween = W". Since both types of households face the same labor demand schedule (15),
labor services provided by a typical rule-of-thumber are equal to the average provided by
optimizing households, Nj’ = N°. Therefore, wages and labor services of rule-of-thumbers
are equal to their average in the economy. As a result, we can write the consumption of a
typical rule-of-thumb household C?” as follows:
Cf = (1 TWN, (21)
where W; = W;?/P{ is the real wage rate.
2.2 Firms
As mentioned before, the production of sectoral goods in the SAMBA model is carried out in
three stages. In the first stage, there are domestic input producers and importers. The rep-
resentative domestic producer operates a standard constant returns-to-scale technology that
provides the combined services of capital and labor to sectoral intermediate good producers.
In parallel, importers buy differentiated inputs abroad and resell them to an assembler of im-
ported goods. In turn, the assembler transforms the differentiated goods into a homogeneous
imported input, which is sold to the sectoral intermediate good producers.
In the second stage, there is a continuum of intermediate good producers indexed by
j € [0,1] in each sector — private consumption goods, government consumption goods,
investment goods, and exports — that operate constant returns-to-scale technologies that

transform the imported input and the bundle of capital and labor into sectoral differentiated
goods. Lastly, in the third stage, sectoral assemblers combine the differentiated goods into
corresponding sectoral homogeneous goods.
The production in the second stage also requires the use of financial services. In par-
ticular, intermediate good producers must finance a fraction of their imported inputs with
working capital borrowed from abroad. These working capital requirements capture the fact
that a sizeable fraction of Brazilian imports is financed by foreign banks and suppliers. ‘The
requirements also help to account for the fact that financial crises may disrupt trade credit
and trade flows.
2.2.1 Sectoral Assemblers
For convenience, we start describing the behavior of home firms operating in the third stage
of production. In this stage, perfectly competitive sectoral goods assemblers combine the
sectoral intermediate varieties into a sectoral homogenous good through a standard Dixit-
Stiglitz aggregator:
1 “Ht
w=(fone a), (22)
0
where H = C,I,G,X denotes the corresponding sector (private consumption, investment,
government consumption, and exports, respectively), Y,” is the sectoral output and Yi is
the differentiated variety produced by intermediate good firm 7. eit > 1 is a time-varying
elasticity of substitution between the differentiated varieties. This time-dependent elasticity
will imply a time-varying markup in the goods market. We will interpret a shift in the
markup as a "cost-push" shock to sectoral inflation Phillips curves.
Sectoral goods assemblers choose the optimal amounts of each variety and break even in
equilibrium. The problem solved by the assembler in sector H is given by:
1
max preys - i Pay ja} , WHY © H,

subject to equation (22), where P/ is the aggregate price of home good H, and Pi is the
price of intermediate variety j. The assumption of pricing to market means that P and
PH
“+, for 7 = X, is expressed in foreign currency. The problem solution yields the following
optimal demand for the jth variety:
P
pH ~ ent
Y= Ppa Y,", VH,Vj € H. (23)
The break-even condition for the sectoral good assembler implies the following sectoral price
index: :
: 1-eF lacy
Pi = ( | (Pi) om ti) "WH. (24)
0
2.2.2 Domestic Input Producers
We now turn to the first production stage, starting with the representative domestic input
producer. This firm operates in perfectly competitive markets and produces the domestic
input Y,? through a standard Cobb-Douglas technology using capital and labor:
YP =ZPKe(Z%(N.—-N))*, (25)
where K; is physical capital, N; is total labor input, N is overhead labor, which we assume
constant over time, ZP is a domestic transitory technology shock, and Z is a stochastic
trend embodying permanent shifts in technology. The overhead labor helps to smooth the
rate of change of total labor input over the business cycle. The temporary technology shock
evolves according to an AR(1) process:
log (Z?) = Pp log (2721) + EP, (26)
where ¢? is the innovation. The growth rate of the stochastic trend is defined as 77 =
Z:/Zi-1, Which follows:
log(Z/’) = (1 — pz) 27 + pz log (2/24) + 7, (27)

where Z% is the long-run growth rate of technology, in gross terms, and ¢7 is the innovation.
The domestic input producer takes all prices as given and chooses the optimal amounts
of capital and labor services as to minimize total input costs, subject to the technology
constraint (25):
pin, {nf WEN, TP" + PP (VP —ZPKE (a (M—N))},
where Te" is a lump-sum transfer from the government, which is equal to the overhead
labor cost. The transfer is simply a technical device that ensures a well-defined solution
to the problem above. P? is the Lagrange multiplier associated with the technology con-
straint, which in equilibrium will be equal to the nominal marginal cost of the domestic input
producer. Cost minimization implies the following optimal demands for capital and labor,
respectively:
Kn bY?
RE" = oP PE (28)
yP
Wr = (1—a) PP—*=. 29
(= (1-0) PP (29)
Substituting (28) and (29) into the technology constraint (25) yields the following expression
for the unit cost associated with the choice of domestic inputs:
PP =(—=R*” t , 30
‘ (Lai) (24 Zp (30)
2.2.3. Importers
Now we look at the behavior of importing firms. We assume that there is a continuum
of importing firms indexed by j € [0,1] that buy differentiated goods from the rest of the
world. Each importing firm buys a distinct variety which is then sold in a monopolistically
competitive market to an assembler of imported goods. The assembler transforms the differ-
entiated inputs into a homogenous good, which is finally sold to domestic intermediate good
producers. Similar to the sectoral assemblers described above, the assembler of imported

goods also bundles the differentiated varieties through a Dixit-Stiglitz aggregator:
&M
1 ey—-l ey—-l
0
where M; is the homogenous imported good, M;, is the imported variety j, and ej, is the
elasticity of substitution across varieties. The problem of the imported goods assembler is
analogous to the home good assembler’s problem, that is,
1
max ¢ P’ M, — | PM M,1dj >,
{My} { t t F jt VAG, i
subject to (31), where pM is the local-currency price charged by importing firm j, and P“
is the local-currency aggregate import price. The first-order and zero-profit conditions imply
the following demand for the jth imported good and aggregate import price index:
pM —Ee€mM
it
Mit = ) M, (32)
t
1
PM = ( i “(payne ii) — (33)
Monopolistic importing firms face price rigidity a la Calvo when setting their prices. The
presence of price rigidity in the import sector helps to slow down the pass-through of the
exchange rate to domestic prices. In each period, each importing firm 7 faces a constant
probability 1 — 0), of resetting its prices according to market conditions. Otherwise, with
probability @), it simply updates the price considering past inflation of imported goods and
the CPI inflation target, according to the following indexation rule:
P= TE PM, (34)
where Y/ is the indexation factor, given by
wu poC\1—w
YH = (Ma) (i, e™, (35)
where w™ € [0,1] is an indexation parameter, I, is the CPI inflation target in gross terms,
and HT, is the gross inflation rate of imported goods, defined as I! = P“/P™,. In the
long run, the imported goods inflation (in local currency) converges to the inflation target.

The value of profits accrued to importing firm 7 is given by:
Pit Mj — (SeP0") Miu
where P” is the foreign-currency price of the jth imported variety. The importing firm
that receives the price signal in period t maximizes the real value of the expected discounted
flow of its profits along the paths over which its own price is not adjusted optimally:
[o@)
4 M M M*
max E; y (Or08)' Merri (VitreP ites — StaiPats ) Misi,
subject to the demand constraint (32) and the indexation rule (34), where
Aisi
Netti = rWiie
is optimizing households’ marginal rate of substitution between nominal income in periods
t and t +7, and
The | ay - a i=0
un T= (Mya, (Tl.«) 21
is the indexation factor accumulated between t and t+ 7%. Since all firms that are able to
change their prices face the same import cost, they choose the same optimal price along the
symmetric equilibrium. Taking the first-order condition yields the following expression for
the optimal price P.“":
Ex > (Ou B)' Neti ( pu ) SiiPe; Misi
M* _ __€&M i=0 te
< 7 €um — l ce i mM, l-em u , (36)
Ei; i (0173) Neti ( Si ) Pe Misi
From equation (33), we derive the following law of motion for the imported good price
index:
1
PM = |e (TH PM) + (= Ou) (PMY (37)
Therefore, conditions (34)-(37) determine the behavior of the price of imported goods.

2.2.4 Sectoral Intermediate Producers
The decisions of inputs and prices made by intermediated good producers can be broken
down into two problems.
Input Choices In the second production stage, there is a continuum of intermediate good
producers indexed by j € [0,1] in each sector. These firms combine domestic and imported
inputs through the following CES production function:
Yui = |(wn) (Ying) © + - en) (A -Ty (ri) Mia] en)
jit
where as before H = C,I,G,X, Myi is the imported input, I't/ (rit) is an adjustment
cost associated with the imported input, which is a function of the imports-to-output ratio
ry =M Fe / Yi , WH € [0,1] is the weight of the domestic input in the production function,
and €y > 0 is the elasticity of substitution between the two inputs. We assume the following
functional form for the adjustment cost:
2
where 377 > 0 and Z i; is a shock to the adjustment cost that shifts the demand for imports.
This formulation is based on Bayoumi et al. (2004) and Christoffel et al. (2008), and implies
that it is costly for the firm to adjust its current imports-to-output ratio relative to past
sectoral imports-to-output ratio. The above formulation satisfies P7/, = 7/ = 0 in the
steady state, where UH is the derivative of the adjustment cost function, and has two
convenient properties. First, it helps to slow down the response of the import share to
fluctuations in the relative price of imported inputs. Second, it allows imported inputs to
respond quickly to shifts in the demand for the home good. In other words, imports respond
more slowly to price movements induced by changes in the exchange rate or external prices
than to domestic demand fluctuations. This feature is consistent with the empirical evidence
for Brazil.

Each sectoral intermediate good producer takes as given the input prices and chooses the
combination of inputs that minimizes its total cost
min {PPY Py + [+e (RIS? --1)) PMME}, Vi eH,
BD
subject to the technology constraint (38). The parameter 1 is the fraction of the im-
ported input that must be financed abroad through intra-period loans at the net interest
rate R*SP° — 1. This working capital constraint captures some of the observed trade credit
frictions and helps to replicate the negative co-movement between investment and the coun-
try risk premium. It amplifies the effect of shocks to the country risk premium on imports.®
Let M cnn be the Lagrange multiplier (in nominal terms) associated with the technology
constraint and define PH = [1 + ly (Ri SB 1)| P™ as the effective import cost in sector
H. We assume that all firms in the same sector face the same technology and effective import
HT
cost and have adjustment costs that do not depend upon firm’s history. Thus rj, is the same
across firms and so is the real marginal cost. Therefore, we can drop the subscript 7 from ri
and M Cr. Taking into account these properties, the first-order conditions characterizing
the optimal choices of YP and M Fe can be written respectively as:
D PP a A
Yp,,=7n ( ) yi (39)
A, j,t MCF jit
M
1- P
1-TH, (1 Py, — rit) uch
where D1 (r?) = TM (r) MF. Note that PY! and PY" are also the same across firms. Lastly,
substituting the optimal input-output ratios into the technology constraint pins down the
nominal marginal cost in sector H:
l-ey l-ey
MO} = |wn (PP) + (L- wn) ( <a | ; (41)
3Using the estimated model, we observe that, in the case of a shock to the country risk premium, the
reduction in imports is around 30% higher (in the first two years) when compared to a model with 1747 = 0
(keeping all other parameters constant).

which is simply a weighted average of the costs of domestic and imported inputs. Note that
the share of imports varies across sectors. In particular, we assume that the production
of government goods does not use imported inputs, that is, @¢ = 1. Thus government
consumption is a purely non-tradable good whose nominal marginal cost of production is
given by MCP” = PP.
Price Setting in the Government Consumption and Investment Goods Sectors
We now describe the price choices of the intermediate good producers in the sectors that
produce government consumption and investment goods. As before, prices are set according
to Calvo contracts. In each period t, with probability 1 — 0, each intermediate good firm
j € H — where in this subsection H = G, I — sets its price optimally, and with probability
0 it adjusts the price according to the following indexation rule:
Pa=TiPi4, J€H=G,l, (42)
with the following indexation factor that weights past sectoral inflation and the inflation
target:
rH = (mit )°" (ee, (43)
where wy € [0,1] is sector H indexation parameter, and the gross inflation rate in sector
H =G,1 is given by II! = P#/P#,.
Intermediate good producers, when setting prices optimally, maximize the value of the
expected discounted flow of profits:
co
a Ayn H F
rape Be » (0118) Ness (ThysPf — MCR?) Vil... Wi € H= G.I,
subject to the demand constraint (23) and indexation rule (42), where the nominal marginal
cost M Cpe is given by equation (41) and
i a w = l—w :
tt+ Hint (17.1) H (Il.+4) H i >I]

is the indexation factor accumulated between t and t + 7.
The first-order condition with respect to the optimal price P//” = P#, along the sym-
metric equilibrium, is given by:
1—eP .
i; Ss" (O73) Netsi ( pi ) (Pr ) mee PY (Ga — 1) = (44)
__P
ES (948) Mets pH (P; ) mee MCy; Vieni:
Using equation (24), we derive the following law of motion for the sectoral price index
P# in sector H = G, I:
1
PH = [Oy (CEPI) + (1 Oar) (BI) | Fe (45)
Therefore, conditions (42)-(45) determine the behavior of the prices of government con-
sumption and investment goods.
Price Setting in the Consumption Goods Sector We have two types of intermediate
producers in the consumption goods sector. They have the same technology, solve the
same cost minimization problem and face similar downward-sloping demand curve for their
products. Nevertheless, they do differ with respect to their pricing policies. A fraction
1 — wy, of firms in the consumption goods sector choose their price in the same way the
intermediate good producers of the other three sectors do. We call this group freely-set price
firms, denoting this set by F’. In each period a firm j € F faces a constant probability 1— 6p
of choosing its price optimally and a probability 6; of adjusting its price according to an
indexation rule, which is similar to (43):
Pai Pia. WEF, (46)
where the indexation factor is a weighted average of past overall CPI inflation and the
inflation target:
rF = (me.,)°* (hr, (47)

with weight wy € [0,1]. To be more consistent with actual informal price indexation schemes,
the rule includes the inflation of the (overall) CPI instead of that of freely-set prices.
On the other hand, if the firm is allowed to choose its price optimally, it does so by
solving the usual price optimization problem:
(hy i; Ss" (0-3)' Nees (Thee - MC§") Yfiei VI EF,
jt i=0
subject to the demand constraint (23) and indexation rule (46), with the following indexation
factor accumulated between t and ¢ +72:
OL Ter ea)" (Teen) 2 1
and M Ona is the nominal marginal cost incurred in the production of consumption goods,
given by equation (41).
In the symmetric equilibrium, the optimal freely-set price P” is determined by the usual
pricing condition:
1-eF ,,.
= i Vhs on er
i=0 t+i
C
i=0 Pri
love) yr Citi Pp 1
i tt+t F*)—€o,t4+i— Cyny7C _P
Et 5 (Or) Nits (P, ) MCN; Yeti:
Using equation (24), we can find the law of motion for the freely-set price index:
1
P
PP = |Or (CP PE,) + (1 =p) (PP YO] Ee (49)
We now turn to the fraction @,4 of consumption good producers. A firm indexed by
j € [0,74] is not free to choose its own price and must follow an exogenous pricing policy.
Their prices are regulated or administered by the government. They include the prices of oil
by-products, public utilities (electricity, water, telephone), bus fares, medications etc., and

account for about a third of the overall CPI.4 Their prices are either set by the government or
follow contracts settled with government agencies. Administered prices are less sensitive to
demand conditions and are usually set in a backward-looking manner (Minella et al. (2003)).
We denote this set of firms by A, where AUF =C.
Let PA be the price of firm 7 € A. We assume that, in each period t, a fraction 04 of
firms are drawn randomly from the set A and are allowed to set their prices according to a
pre-specified rule YA. The remaining fraction 1 — 6, of firms that were not drawn by the
rule simply update their prices according to the inflation target Tl, . > Therefore,
PA=
jit _
Te P i 4-1 With probability 04
Il, PA 1, with probability 1 — 64.
In practice, administered prices are usually allowed to change once a year. So we set 64 =
1/4. Electricity and telephone rates explicitly follow contract-based rules, which mandate
price adjustments according to the past four-quarter CPI inflation, the past four-quarter
change in the General Price Index (IGP) — which is largely affected by the exchange rate®
— and past changes in costs. Since the model does not have an equivalent to the IGP, the
pricing rule will capture this factor through the CPI inflation and movements in the real
exchange rate. The majority of the other items of administered prices, in practice, follow
past four-quarter CPI inflation very closely. Taking this into account, we chose the following
functional form for the indexation factor YA:
(iin 7 (5 " (wey (QP)84) (Zaye, (50)
4To simplify the model we assume that all producers of consumption goods have identical technology and
only differ in their pricing decisions. Modeling administered price firms as belonging to a different sector
would add adittional undesired complexity. Our interest is in the differences in terms of price settting and
not in the particular behavior of the production of those groups. See Freitas and Bugarin (2007) for a
different approach, where they develop a multi-sector but simpler model to study the welfare and monetary
policy implications of administered prices.
°Since the long-run inflation rate is positive, this is simply a technical requirement in order to prevent
permanent distortion in relative prices.
SIGP is comprised of the Broad Producer Price Index (60%), Consumer Price Index (30%), and Civil
Construction Cost Index (10%).
yA=7Y4

= —co\l4xa , ; ; ;
where Y4 = (i ) is a constant ensuring that in steady state Y4 is equal to the steady-
state inflation target Il’, MCC =M cen /P£ is the real marginal cost of the consumption
goods sector, uv}, and v4, are positive weights (total weight is given by 1 + v), + v4), and
QF = PF /P® is the relative freely-set price, raised to the exponent (1 — y4), which ensures
that freely-set and administered prices do not diverge permanently. The term ZA is an AR(1)
process that captures shifts in the administered prices that are not modeled explicitly. Its
exponent is just a convenient normalization. The rule captures key features of the behavior
of administered prices in Brazil: i) backward-looking nature; ii) indexation has long lags
(up to five quarters); and iii) key role played by the CPI inflation, but also allowing for the
effects of changes in the exchange rate and production costs.
Because all administered price firms always update their prices randomly and since the
rule Y4 depends only upon aggregate variables, we can define the overall administered price
1
1 ar
Solving for the integral and simplifying further yields the law of motion for administered
index as follows:
prices, which in turn implies the following equation for the administered price inflation:
tA = Z (TA) bx + (1 — 84) (Ty ) ea] Ee (51)
where H# = P4/PA,. Note that, in the long run, Y4 = TI” and all administered price firms
will adjust their prices according to the steady-state inflation target.
Starting from equation (24), the aggregate CPI can be expressed as a weighted average
of the freely-set and administered price indices:
1
1-eR
pe = Ea (pA) es +(1—wa) (Pry | Ct (52)
We can then derive the (overall) CPI inflation, which is a weighted average of the inflation
rates of administered and freely-set prices:
— <P —P P
PA 1-eq , PF 1-04 l-eo 4
WA (1! ae) + (1-7a@,) (nr Fo") (53)
t-1 t-1

where II = P*/P#,. As in the data, the CPI inflation in the model displays a slow-moving
component with strong backward-looking dynamics (I), and a component that is more
susceptible to forward-looking behavior (II/’), although also affected by backward-looking
behavior (indexation parameter wy). These features help to replicate the actual Brazilian
inflation dynamics, which display relatively high persistence overtime and slow response to
changes in the monetary policy stance.
Therefore, the behavior of consumer prices is described by equations (48)-(51) and (53).
Price Setting in the Exported Goods Sector The price setting in the exported goods
sector is analogous to that in the previous subsection, except for the fact that exporting firms
set their prices in foreign currency. Let Ps be the foreign-currency price of the variety sold
by the jth intermediate producer of the exported good. In each period t, with probability
1 — 6x, each intermediate good firm 7 € X sets its price optimally, and with probability 0x
it adjusts the price according to the following indexation rule:
where the indexation factor combines past sectoral inflation in foreign currency and the CPI
inflation abroad:
YX = (S,)°* (i)h es, (55)
with indexation parameter wx € [0,1], and the gross inflation rate in the export goods sector
given by I = P*/PX,.
The producer of the intermediate exported good who sets its price optimally maximizes
the real value of the expected discounted flow of profits in local currency as follows:
oe)
max By S| (0x8)! Meri (THiSeiP' - Mc) Yirsin
jt G0
subject to the demand constraint (23) and indexation rule (54), where
+X { 1, i=0
aan Thai (pa) (IIz,,)°* 21,

and the nominal marginal cost is given by equation (41).
Along the symmetric equilibrium, Ps» = P*", so that the first-order condition with
respect to P* is given by:
l-e .
B,5> (0x3) sen ( a) (PX) SPX VS (Ba 1) = (56)
__P
~ i Visi a X*\ eK thi X,ny7X
i; Ss" (OxB) Nersi (P; )- M4; Vie. ti
The law of motion of the export price index P* is given by:
1
PX = [Ox (EPA) + (10x) (PRY Ee (57)
Therefore, the behavior of export good prices can be described by equations (54)-(57).
2.2.5 Foreign Importers
We assume that exports X; from Brazil is a homogeneous good before it leaves the dock, but
it is a differentiated good in the world market. By symmetry with the domestic economy,
the Brazilian exported good is used as a production input in the rest of the world (ROW).
The export assembler ships the Brazilian good abroad at the foreign-currency price P*’.
In turn, foreign producers combine imports from Brazil, M/;*, and inputs produced in the
ROW, Y,”’. By symmetry with the domestic economy, the foreign production function is
the following:
1 M* ost 2 ype] ot
ye = (=) (2-1) MF] = + (L— a") (¥,?") © | (58)
where, of course, M* = X;, €* > 0 is the elasticity of substitution between Brazilian exports
and the inputs produced in the ROW, a is the share of Brazilian exports in the ROW
output bundle, and I” is an import adjustment cost, given by:
pM — zM ~ ye fit) 59
ol

with 0" > 0.
The foreign producer chooses the optimal combination of Brazilian and ROW inputs as
to minimize its total cost:
sy {Pe + Po Xe} ’
subject to the technology constraint (58). The first-order condition with respect to X;
generates the world demand for Brazilian exports:
*
x= ( a ) i ys (60)
T!" is the derivative of the adjustment cost function, QX" = P*"/P, is
where as before
the relative price of Brazilian exports in foreign currency, and P;* is the Lagrange multiplier
associated with the constraint. Since we are not modeling the ROW in a full way, we assume
from now on that P* = P{", that is, the price of foreign final goods is equal to the price of
foreign consumption goods.
2.3 Government
Government comprises monetary and fiscal authorities. They follow rules that are meant to
describe in a concise way the modus operandi of the Brazilian monetary and fiscal policies,
given by explicit targets for inflation and for the public sector primary surplus-to-GDP ratio.
2.3.1 Monetary Policy
The goal of the monetary authority is to stabilize CPI inflation around the inflation target,
using as instrument the nominal interest rate, according to the following forward-looking
Taylor-type rule:

where yp € (0,1) is an interest-rate smoothing parameter, yy, > 1, yy > 0, Z} captures
monetary policy shocks, II¢,,, = [[j_, 0¢,, = P&,/P© is the four-quarter inflation rate,
and Tl, 14= Ts Tl; is the four-quarter inflation target. In Brazil, the actual target refers
to the inflation in the calendar year. It is set in June for the calendar year that starts
one year and a half later. Thus we assume the target is known by agents four quarters in
advance in the model. We use a four-quarter horizon for inflation in order to capture the
forward-looking nature of the conduct of monetary policy. The term (My 34 us) ‘ (Z 4 \’ /B
is the equilibrium nominal interest rate (or the nominal natural rate of interest).
The rule also allows for a direct role played by the output gap, which is defined as Y;,/Z,Y ,
where Z;Y is the output level along the balanced-growth path. In other words, the output
gap is the deviation of the actual output from the output in the balanced-growth path. Our
measure of the output gap is similar to those by Adolfson et al. (2007), Christoffel et al.
(2008), and Del Negro et al. (2007).’
We assume a time-varying inflation target as to capture the behavior of the inflation
target in Brazil, which varied from 1999 to 2005, and has been kept constant since then
at 4.5% per year. For the purposes of estimation and simulation, we assume that the CPI
inflation target is conveniently described by an AR(1) with a potentially high degree of
(Tess) ' ~ (n°) vine ((.,.) ‘) =“ exp {er } : (62)
2.3.2 Fiscal Policy
persistence:
The current fiscal regime in Brazil has been in place since 1999. The fiscal authority an-
nounces annual targets for the nonfinancial public sector primary surplus as a proportion of
GDP, which in general have been fulfilled. The government’s ultimate goal is to stabilize
"It differs from the output gap defined as deviations from the long-run output that would prevail under
full price/wage flexibility and no markup distortions (model-consistent output gap), as in Smets and Wouters
(2003, 2007), and Woodford (2003). The advantages of our output gap measure are that is does not require
the computation of the flexible price/wage equilibrium, seems to be preferred by the data, at least when
estimating DSGE closed economy models for the US (Del Negro et al. (2007)), and is closer to the usual
definition of output gap used by policymakers.

(or even reduce) the public sector net debt-to-GDP ratio. So the primary surplus is an
intermediate target.
Thus, we set up an equation where the actual primary surplus responds to the announced
targets, with a smoothing component,® as follows:
Si} = S" + bs (Si, — 8") + os (8) — 8") — se2y’, (63)
where ¢, € [0,1), ds > 0, S? is the (actual) primary surplus-to-GDP ratio (S"/PYY,), S”
is the nominal primary surplus, SY is the target for the primary surplus-to-GDP ratio, S”
is its long-run value, z© is a shock to the primary surplus, and sq = (Q°G)/(QYY) is the
steady-state share of government consumption in GDP (Q° = P%/P® and QY = P* /P°
are the corresponding relative price deflators, and G and Y are the stationary steady-state
values of government consumption and real GDP).°
As we will see shortly, since the tax rate is exogenous, the fiscal instrument implied by
the rule is government consumption. In other words, deviations of the primary surplus from
the target are corrected endogenously by changes in government spending. Thus we interpret
2 as unexpected shifts in government spending. Scaling the shock by sq is just a matter
of convenience. An exogenous change in government consumption by one percent will shift
the primary surplus-to-GDP ratio by sg. In other words, in order to reduce the primary
surplus-to-GDP ratio by one unit, government consumption should rise by 1/sq percent.
Since the primary surplus target in Brazil has been, in general, set to stabilize the public
sector net debt-to-GDP ratio, we assume that the primary surplus target evolves according
to the following rule:
SP = SY + pg (81.1 — S”) + bp (BY — BY) + &?, (64)
where pz € [0,1), dp > 0, BY = B,/P*.Y;-1 is government debt as a proportion of GDP!°,
8We also allowed a specification that included a countercyclical component in the rule. However, we have
not found robust results in the estimation. Note that, in the case of the countercyclical fiscal policy launched
in the end of 2008 and 2009 to respond to the global crisis, the primary surplus target was reduced.
°Valli and Carvalho (2010) also model fiscal policy in Brazil using a rule based on the primary surplus.
!0Remember that B;, is a pre-determined variable in period t, i.e., decided in t — 1.

BY is its long-run value, and eS is a shock to the primary surplus target. Technically, this
equation also guarantees that the government debt-to-GDP ratio is stationary.
The nominal primary surplus is defined as the difference between non-interest government
revenues and expenses, which in the model is given by the difference between nominal net
tax revenues and nominal government consumption:
S? = TAX? — PoC, (65)
where TAX)’ is aggregate nominal tax revenues in net terms:
TAX? = wprlT WEN, + (1 — wer) OC" — TP. (66)
For simplicity, we follow Medina and Soto (2007) and assume that total taxes are a
time-varying proportion of nominal GDP:
TAX? =T, (P/N), (67)
where 7; is the average tax rate, which we assume is exogenously determined:
T,=T +pp(—T) +22, (68)
where T is the steady-state average tax rate, and <7 is a shock to the average tax rate.
We further assume that the tax rate faced by rule-of-thumb households, 77, is equal to
the average tax rate of the economy, T;. Notice that because T? = W;"N, the lump-sum tax
levied on optimizing household must adjust as to ensure that condition (66) is satisfied in
each period. In other words, from the government’s point of view, (l—wprr)T°” is a residual
taxation given by 7; (PrY; — Wrrl, TWN) + WrNn. Alternatively, we could have assumed
in the model the presence of distortionary taxes rates on several margins (consumption,
labor income, capital income, profits, etc.). However, since our focus is on the business cycle
effects of government spending and not on the effects of different tax structures, we decided
to have a simpler formulation for aggregate taxes.

Using equations (65) and (67), the primary surplus-to-GDP ratio can be written as
T, — (PPG) / (Pry), which can be rearranged to express the behavior of government con-
sumption consistent with the primary surplus rule:
PYY,
Gi = £ =
Py
(T, — S?’). (69)
As mentioned before, for a given exogenous tax rate, changes in the primary surplus are
obtained through changes in government consumption. In the case of Brazil, adjustments in
spending tend to take place faster than changes in tax rates. For instance, large part of the
taxes are not allowed to be changed during the fiscal year. The equation also implies that,
given government goods relative price and the tax rate, changes in output require propor-
tional changes in government consumption in order to keep the primary surplus constant.
Thus, in this setup, fiscal policy is not countercyclical.
Now we derive the law of motion of the government debt. In each period t, the government
receives a flow of tax revenues and issues one-period non-contingent bonds at the interest rate
R,. The government uses these proceeds to pay for its expenditures and for the outstanding
debt. Therefore, the flow budget constraint for the government is given by:
P&G, + By = + T; (P Yi) - (70)
Dividing both sides by current nominal GDP and using identity (69), we obtain the expression
for the law of motion of government debt:
BY Y,_4
BY =n (Fe - st), 71
t+1 t TLY Y, t ( )
where II? = P’/P , is the gross GDP deflator inflation. Note that a rise in the interest rate
set by the monetary authority raises the government debt, which by equation (64) increases
the primary surplus target, and consequently by equations (63) and (69) leads to a reduction
in government consumption. Therefore, the model allows for direct effects of monetary policy
on fiscal policy.

2.4 Rest of the World
We do not model the rest-of-the-world economy, but instead assume that foreign variables
follow AR(1) processes, describing the dynamics of detrended world income Y,", foreign
inflation II@’, foreign investors’ risk aversion V,*, interest rate R*, and relative price of
imports in foreign currency QM” = P“"/P°’. The equations are described in Appendix A.
2.5 Shocks
The remaining variables affecting the domestic economy are the shock processes, which are
also modeled as AR(1) processes. They are the shocks to household preference (Z(), coun-
try risk premium (Z?"), transitory technology (Z?), permanent technology (trend growth
rate) (Z/), investment technology (Z/), import demand (Z/" = Zj',, H = C,1I,X), export
demand (Z;""), productivity differential (z/), price markup (e)),,, H = C,G,I,X), wage
markup (e'”), administered prices (ZA), monetary policy (Z/), and fiscal policy (govern-
ment consumption) (z@). Note that we assumed that the shock to import demand Lite is
the same across sectors. Additionally, because the UIP condition is known to have a very
poor fit to the data, we add the ad hoc shock ze to its log-linear version.
2.6 Aggregation
In the model, the aggregation of quantities of differentiated goods goes through the Dixit-
Stiglitz aggregator ("weighted" average), and the simple aggregation is basically an "un-
weighted" average. The difference between the two values arises from price or wage distor-
tions, which, because of full indexation, vanishes both in the steady state and when we take
first-order approximations around the steady state. We adopt the convention of expressing
unweighted variables with a hat, X;.
In the intermediate goods sectors, the unweighted aggregation over all firms 7 in each
sector H = C,I,G,X is given by y,7 = in Yt dj. Using equation (23), we can find the

relationship between weighted and unweighted output sectors:
—d,
yt — (Fit) Yi dj 72
t — ; PH t Q, ( )
which can be expressed more concisely as follows:
P
gu (BEY yn 73
to PH to ( )
t
where Y,” is the sectoral output based on the standard Dixit-Stiglitz aggregator (22), Yt is
the unweighted sectoral output, and PH is the unweighted sectoral price index, defined as:
1
1 P “e
irs ([ (ely ai)
measures the price distortion in sector H. It can be shown that in the
ay
vt
(74)
__P
ert
So (PH/PH)
steady state Y# = Y”, and after taking first-order approximations yf = g#,, which represent
log-deviations from the steady state. Similar relations are found in the import sector (just
replace Y,“, y,7 PE, pH and Pi by M;, M,, PM, pM and Pu , respectively).
When aggregating labor across households, we also find similar results. Defining N=
Serr NitG + fico Niedj, and using the fact that W?, = W/?", j € RT, we find the following
relationship:
sy Wel
A wr
N= |wrr+(1- @rr) ta Nt, (75)
Wt
where JN; is total labor based on the standard Dixit-Stiglitz aggregator (16), N;, is the
1
unweighted total labor, and W/ = (ts / (WwW?) e ti) is the unweighted wage.
Lastly, we assume that each type of household provides the same amount of overhead labor,
N jdj = wrrN and Sieo Nj4dj = (1 _ Drr) N.
so that in equilibrium J; RT
The aggregation of homogenous goods or assets is straightforward. Aggregate consump-
tion is the weighted average of the per capita consumption in each group:
Cy = wrrCf" + (1— wer) CP, (76)

where C? and Cf" are given by equations (9) and (21), respectively.
Since we assume that rule-of-thumbers’ wage rate is equal to the average wage rate of
optimizers, then per capita wage rate W,” is equal to wer, whose law of motion is given by
equation (20).
In equilibrium, the allocations of new capital goods, installed capital and bond holdings
are the same across all optimizing households, and the aggregate variables can be expressed,
respectively, as:
| Tad =f; / Kjudj = Kt; | Byidj = Bi; | Bj dj = Br; (77)
jeO jEO jcO jcO
where J;, K,, B, and Bf are the corresponding economy-wide counterparts. Note that G;
and X, already represent aggregate figures.
Finally, we derive the law of motion of net foreign assets. We aggregate the budget
constraints of all households, along the symmetric equilibrium. Using many of the previous
aggregation results, the government flow budget constraint (70), the definition of the real
exchange rate, and the facts that [ Bi .dj = 0 and that i D}},dj collects all profits, we can
write the law of motion of net foreign assets as a proportion of GDP as follows:
Bi ( Yin Q: Uy
Rsh ~ \IPY, Q4 0
where Bf’, = S,By,,/P; Y;, NX? is the net exports-to-GDP ratio (or trade balance-to-GDP
) Biv 4 NXY — Lt, (78)
ratio), given by
NX}! =
A —e€uM *
S,PXX, (Ee) S.P M, (79)
and L;” is defined as total payments of interests on external borrowing by firms as a pro-
portion of GDP:
* PMM#E
LY =S uy (RESP -1) 4. 80
Note that (Q,0 ) / (Q,017 ) = S,/S,-1. Therefore, the evolution of net foreign assets-
to-GDP depends on the trade balance, income account (interest on loans and bonds) and
"accounting terms", given by GDP growth and the difference between GDP deflator inflation
and nominal exchange rate change.

2.7 Market Clearing and GDP
We start by the market clearing conditions in the final goods sectors. In equilibrium, the
aggregate supply of sectoral good H is equal to the aggregate demand for that good:
Y°=C; Yi=h YO=G; YX =X. (81)
In the inputs market, total domestic input supplied by domestic input producers to sector
H =C,I,G,X is equal to the total demand for domestic inputs by all firms 7 operating
in sector H: ih YR AU = Yee The behavior of total sector demand for inputs, in turn, is
obtained by aggregating equation (39) and using condition (73):
P
PP en pH ~eH,t
Ye, = WH ( u ) (i Y,". (82)
t
Mc"
Aggregating across all sectors gives the market clearing condition for the domestic input:
YP =YR+FYG+VO+H YR. (83)
By the same token, total supply of imported inputs in sector H = C,/, X is equal to the total
demand for imports by all firms j operating in sector H: fo Mjidj = Mj. The behavior of
the total sector demand for imported inputs is obtained by aggregating equation (40) and
using condition (73):
en . -P,
t t >?
and aggregating across all relevant sectors yields the market clearing condition for the im-
ported input:
M,= ME + Mj + MX. (85)
In the case of stock variables, the aggregate demand for K,;, B;, and By (77) should be
equal to the corresponding aggregate supply.
AO

Finally, since we express real GDP as Y, and GDP deflator as PY, nominal GDP is
given by P* Y;, which is defined as the difference between total nominal values of domestic
production and imports:
.(Pu\™
PYY, = P&C, + Pil, + P°oG, + S,P* X, — 8,P! (Es) M,. (86)
Therefore, the definition is consistent with the nominal value-added concept used in National
Accounts. Note that we have to include the import price distortion term since we aggregate
over imported differentiated goods.
Because we do not have an equilibrium condition that pins down either real GDP or the
GDP deflator, we need an additional equation to determine one of these variables. We model
the GDP deflator in such a way that changes in relative prices (price of goods in equation
(86) relative to the GDP deflator) play no role in the real GDP dynamics. In other words,
in the linear version of the model, changes in the real GDP will depend only on changes in
the volumes of the aggregate demand variables and not directly on changes in the relative
prices of the corresponding goods. This means that, in the model, changes in the real GDP
are computed at constant weights.
This is equivalent to say that the level of the GDP deflator is given by:
ry = crey (reve cniyt(sesy™ [sie (Fa) |
t
: os : jipyH
where s; is the share of component j in nominal GDP so that s; Py CLG, I,
PYY
_ spxy* _ spM" _
Sx = “ayy SM = >pyy > and 8 =
2.8 Balanced Growth Path, Steady State and Log-Linear Model
The next step of model derivation is to put the model into the stationary form. SAMBA
has two stochastic trends or sources of unit roots, a real one whose stochastic growth rate
is ZZ, and a nominal one whose stochastic growth rate is II; . Along the balanced growth
path (BGP), all real variables in the model, except for labor, grow at the same rate Z7,
Al

whereas the levels of all nominal variables, except for nominal wages, grow at the same rate
Il, . Nominal wages embody the two unit roots.
Therefore, to cast the model in the stationary form, we divide all real variables by the
level of technology Z;. Similarly, we make all nominal variables stationary by dividing their
corresponding levels by the numéraire P°. As for nominal wages, we divide them by both
Z, and P“. Some variables, including labor, ratios to GDP and financial variables, such as
interest rates and foreign investors’ risk aversion, are already stationary.
Finally, as in Christoffel et al. (2008), we detrend foreign output by the level of technol-
ogy prevailing abroad, Z;, and assume that both Z7 and Z; share the same long-run growth,
but may differ in the short run due to asymmetric temporary shocks affecting the produc-
tivity level at home and abroad. Therefore, the productivity differential Z;'/Z; is stationary.
Foreign-currency prices of exports and imports are detrended by the consumer price abroad
P©". The details, including the list of the transformed equations, are presented in Appendix
A.
Next, we derive the deterministic steady state of the stationary model, whose details are
presented in Appendix B. We then log-linearize the BGP equilibrium conditions around the
deterministic steady state. Appendix C provides the list of the resulting linear equations,
which are used in the estimation stage.
3 Estimation
The model was estimated using Bayesian methods.!! This procedure allows the use of
available information, in the form of prior distributions, and the use of observed data to
update these priors, providing the calculation of the posterior distributions of the estimated
parameters. Technically, it also helps shaping the likelihood function, which is particularly
important for the estimation of large DSGE models. In the case of Brazil, the estimation
of such models by classical full information methods (e.g., maximum likelihood and GMM)
‘See, for instance, Canova (2007).

is even more difficult because the data sample span is very short. In practice, the Bayesian
approach is a bridge between calibration and classical estimation. Calibration methods do
not incorporate information from the likelihood, but likelihood estimation is not technically
possible. The Bayesian estimation makes possible to estimate otherwise weakly identified
parameters by incorporating prior knowledge or judgment.
Our model encompasses a total of 118 parameters, of which 37 are calibrated and 81 are
estimated (33 are structural and 48 are shock-related parameters). In the next subsections,
we describe the data set and the variable transformation used in the estimation, the calibra-
tion procedure, the setting of the prior distributions of the estimated parameters, and the
estimation results.
3.1 Data and Shocks
We estimated the model using quarterly data spanning from 1999Q3 to 2010Q2 (44 data
points). We use 23 model variables as observables — 18 domestic and five foreign variables.
We list below the series and the symbol of the correspondent model variables. ‘Table 1
provides additional details, including the source and treatment of each series.
e Domestic variables: GDP, Y;; households’ consumption, C;; investment, [;; government
consumption, G;; exports of goods and services, X;;_ imports of goods and services,
M,; number of employed people, N;; real wage, W;; real effective exchange rate, Q;;
country risk premium, $?"; inflation measured by the Broad National Consumer Price
Index (IPCA), T;; inflation target, H,; free price inflation, H’; administered price
inflation, HI; export price inflation, II; nominal policy interest rate, R;,; public sector
primary surplus-to-GDP ratio, $%; and public sector primary surplus-target-to-GDP
ay
ratio, S.
e Foreign variables: world imports, Y,;*; relative price of imports, Q/"; world (US) in-
flation, IIf; foreign investors’ risk aversion, V,*; and world (US) nominal interest rate,
Re.

We have chosen this set of observables taking into account data availability, their relevance
for policymarkers’ decisions, and their role in explaining the variables of higher interest.
Furthermore, a large set of observables reduces the problem of identification.
To prepare the data for the model estimation, we detrended non stationary series, and
demeaned the stationary ones. Figure 1 provides the graphs of the series after being trans-
formed. For the series corresponding to the variables Y;, C;, I:, Gi, X¢, Mi, Ni, Wi and
Y;*, we applied first log-difference. We then demeaned the transformed series to eliminate
differences in the trends across growing variables. Regarding S?", S/, St, Ix, Ut, V;* and
Ri, we subtract the sample mean from their corresponding levels. In the case of the real
effective exchange rate, Q;, we use percent difference from the sample mean. Since the price
of imports relative to world prices, Q”", has a trend over the sample period, we make it
stationary using a linear trend procedure.
For the CPI-related inflation rates — IT®, IY and IIA — we subtract the inflation target
from these series, but using the target value in place since 2005, 4.5%. The target values for
the previous period are considered as transitional values (the targets were set to 8.0% and
6.0% for 1999 and 2000, respectively). In fact, the economic period starting in 2005 is more
stable than the previous one. In particular, on average, inflation has been close to the target
since 2005 up to the end of the sample, whereas the inflation average in the previous years
was much higher. From 1999 to 2004, the economy experienced the impact of the exchange
rate crisis in 1999, the challenges of implementing inflation targeting and a new fiscal regime,
and the confidence crisis with the presidential elections in 2002. Similarly, we subtract 4.5%
from the inflation target series, Tl, . Since the targets are set for calendar years, we smoothed
the target trajectory using linear interpolation. In order to be consistent with the procedure
used for the inflation rates, we demean the domestic interest rate, R;, using the sample mean
for the period 2005Q1-2010Q2.
We add measurement errors in the equations for GDP growth and CPI inflation. In the
estimated linear model, CPI inflation is assumed to be a fixed weighted average between free

and administered prices, and the weights of GDP aggregate components are assumed to be
constant as well. The measurement errors capture the effect of changes of the actual weights
overtime (CPI weights change every month, and, in the case of GDP, the actual weights are
fixed only for each calendar year).
Besides those 23 series, we also construct a proxy for the implied contribution of inventory
investment to GDP growth, [/””. The Brazilian Institute of Geography and Statistics (IBGE)
provides the calculation of the volume of gross formation of fixed capital, but not of inventory
changes. When we calculate the actual weighted growth rate of the five modeled aggregate
components, it does not correspond exactly to the actual GDP growth rate, whose calculation
is based on the output method. In other words, there remains a wedge between the weighted
growth of the five aggregate demand components and the GDP growth in the data. We treat
this wedge as the implied contribution of inventory investment to the GDP growth, although
it may also be capturing measurement errors of the other aggregate demand components.
This term is added to equation (C.41).’” If we did not take into account this wedge, we
would have a larger estimated measurement error in the GDP growth equation — resulting
not from the model, but from the actual data — and distortions in the output gap estimation.
The measurement equations for the non stationary variables are the following:
Ay?’ = Ye — Yt-1 + x, (88)
where Ay?’s corresponds to the variables in first log-difference listed in Table 1, y% is the
corresponding model variable in log-deviation from the steady state, and 27 is the permanent
technology shock in the linear form. The latter only enters the measurement equations of
variables that have real unit roots in the model.
The number of shocks is equal to the number of observables. We have a total of 23
shocks, plus the shock to inventory investment:
!2Since this term is already in first difference (weighted by its contribution to the GDP growth), we add a
measurement equation for it, and the estimated deviation from the steady state enters the model equation
(C.41). Since it is a residual, we model it as an AR(1) process.

e 17 shocks are associated with domestic variables: domestic risk premium shock, ¢?;
investment adjustment cost shock, ¢/; household preference shock, <@; import adjust-
ment cost shock, ¢/’; administered price shock, ¢/; price markup shock, ¢/; inflation
target shock, a wage markup shock, <!”; export price markup shock, ¢? *. transitory
technology shock, ¢?; permanent technology shock, <7; UIP shock, ee ; country risk
premium shock, ¢?”, government consumption shock, ¢°; tax rate shock, ¢7; primary
surplus target shock, eS; monetary policy shock, ¢*.
e Five shocks are associated with foreign variables: foreign inflation shock, cl! ; foreign
interest rate shock, e’; world demand shock, ¢}"; imports relative price shock, ee ;
foreign investors’ risk aversion shock, ¢Y°; world imports demand shock , ¢/"".
In the linear version of the model, we have added a shock to the UIP equation with the
objective of capturing deviations from the UIP condition. Note that the risk premium in
the UIP equation is usually treated as an unobservable in many DSGE models; so in these
models the risk premium shock also captures deviations from the UIP condition. In contrast,
in our model, we treat it as an observable, warranting the inclusion of the shock ef 38
3.2 Calibrated Parameters
We calibrate 37 parameters — comprised of aggregate shares or ratios, steady-state values
that appear as parameters in the linear model, and some weakly identified parameters.
Table 2 presents the list of the calibrated parameters and the corresponding values used in
the estimation. We describe below the procedures used to find those values. In most cases,
we match the parameter values with their sample means.
The shares of aggregate demand components in GDP (sc, sc, sr, $x, 5m) are based
on sample average calculated from the National Accounts. We match the tax rate 7 with
‘3-The domestic risk premium is also an unobservable in the UIP equation, but it is subject to cross-equation
restrictions coming from the equilibrium conditions for consumption and investment.

the sample mean of the government tax revenues-to-GDP ratio. The share of rule-of thumb
households’ consumption in total consumption, @c, is set to 0.40.4
We calibrate two preference parameters. The time discount factor, 8 = 8 (Z 4 yo? =
0.989, is calculated taking into account the average GDP growth rate, the average domestic
interest rate (the policy Selic rate) over 2005Q1-2010Q2, and the 4.5% inflation target (equa-
tion B.9). The inverse of the elasticity of labor supply, 7, was not possible to be identified in
the estimation, and is set to 1, which is in the range commonly found in the business cycle
literature.
We calibrate twenty technology parameters. The gross growth rate, 7%, matches the
sample average GDP growth rate of 0.9% per quarter. We follow the literature in the cali-
bration of markups in inputs and goods markets. First, we set the elasticity of substitution
between differentiated labor, ey, to 3, which implies a wage markup of 50%. Second, the
elasticity of substitution between differentiated intermediate goods in each sector, ¢/,, where
H =C,I,G,X, and the elasticity of substitution between differentiated imported goods,
€y, are set to 11, implying a 10% price markup in goods market.
The weight of capital in the domestic Cobb-Douglas production function, a, matches the
average capital income share in GDP (0.448). In turn, the share of production labor in total
labor, ay, is set to 0.8. The depreciation rate of capital, 0, is calibrated to 0.015, meaning
6% per year.
We have four technology parameters describing the weights of imported inputs in sectoral
production, 1 — 7%, with H = C,G,I,X. First, we assume that government consumption
goods are produced without using imported inputs, that is, 74 = 1. Second, we calculate
the weights in the investment and exported goods using proxies for the share of imports
in these sectors. The value of imports of capital goods from the Balance of Payments
statistics are fully assigned to investment, and the value of imports of intermediate goods is
'4We assumed that workers that receive up to 2.5 minimum wages in Brazil behave as rule-of-thumb
consumers. We used data on income distribution from the National Household Sample Survey (PNAD).
‘This value is between the available estimations for the Brazilian economy, including those of Carvalho
(1996) and Bonelli and Fonseca (1998), and those commonly used in the literature.
AT

distributed among investment and exports according to their shares in GDP. In the case of
consumption goods, the weight was determined using the steady-state relationship (B.29),
so that it absorbs all remaining imported goods. Finally, using several calibrated parameters
listed in Table 2 and steady-state relations, we find the share of each sector in total demand
for domestic inputs (s%, 87, s4, 82) and in total demand for imported inputs (s?, 57”, 54°),
as well as the shares of sectoral imports in GDP (sy.c, $1, 8u,x).'°
We calibrate the sectoral working capital constraints, 1, for H = C,/,X, using data on
the value of imports that are funded by external financing. Since data does not allow us to
distinguish between sectors, we assume ty = 0.5 for all sectors.
We have two calibrated parameters related to administered prices. The weight of admin-
istered price inflation in overall CPI inflation, @4= 0.3, is set to the corresponding sample
average. The parameter governing the convergence of administered prices, y 4, is set to 0.8,
so in each quarter 0.2 of the relative price change is corrected.
Finally, we set the steady-state values affecting the law of motion of government and
external debt in the linear form. The net foreign assets-to-GDP ratio and the net government
debt-to-GDP ratio (B*”, BY) correspond to the sample average of the net foreign debt and
net debt of nonfinancial public sector, as a proportion of quarterly GDP. We also make
interest rate payments in the model consistent with debt maturity. Since the model has
only one-period bonds, changes in the interest rate affect immediately the cost of the whole
outstanding debt. However, the average maturity in the data is higher than one quarter, so
shifts in interest rates affect only partially the interest rate payments in the current quarter.
Thus, in order to prevent the model from overestimating the impact of interest rate changes
on the outstanding debt, we scale down the interest rate payments implied by the law of
motion of both debts. These scale or adjustment factors of external and domestic debts are
denoted by AF% and AF, respectively. We calibrate their values taking into account the
debt maturity and the share of debt that is indexed to the interest rate.
1©See equations (B.30), (B.31), (C.35) and (C.36).

The steady-state gross inflation target, I], matches the annual inflation rate of 4.5%, in
accordance with the target since 2005. The gross nominal interest rate, R, also matches the
sample average over 2005Q1-2010Q2. For the world gross inflation rate, II@”, we consider
the average US CPI inflation, and for the world gross nominal interest rate, R*, we use the
average Fed funds rate. The gross country risk premium, S?°, matches the average spread
of Brazilian bonds over US treasury bonds of equivalent maturities, and is measured by the
Emerging Markets Bond Index (EMBI) for Brazil.
3.3 Prior Distributions
Setting the priors for the estimated parameters involves choosing the type of the distribution,
its mean and variance. The type of the distribution was chosen to place theoretical or
convenient restrictions over the support of the parameters. For instance, beta distributions
are used for parameters restricted to be in the interval [0,1], and gamma and inverse gamma
for those restricted to be positive. Their variances were chosen according to our beliefs
regarding the probability mass that should be around the prior mean. In general, prior
information or judgment is surrounded by a large degree of uncertainty, so we avoided using
tight priors.
We estimated a total of 81 parameters, divided into two major groups: parameters related
to the endogenous transmission mechanism — preference, real frictions, nominal rigidities
and policy parameters — interpreted as structural parameters, and those related to the
shocks and AR(1) processes. We have used several procedures for setting the priors: studies
based on micro data, evidence for other countries, training sample, and specialists’ knowl-
edge. Table 3 provides a list of the prior distribution used for each parameter, and Figure 2
shows the shapes of the priors of the structural parameters and the corresponding posterior
distributions.
Four preference parameters were estimated. The prior of the inverse of intertemporal
elasticity of substitution, 0, is normal with mean equals to 1.3, consistent with the evidence

that this parameter is equal to or larger than 1.0. The habit persistence parameter, &, has a
beta distribution with a 0.85 mean, based on international evidence on the observed response
of domestic consumption to monetary policy shocks. Note that it implies a coefficient of 0.46
in the lagged consumption term in the linear Euler equation for consumption (&/ (1+ #)).
The priors for the elasticities of the country risk premium with respect to foreign investors’
risk aversion, Yy., and net foreign assets, yp., are inverse gamma whose mean are based on
regressions using data before the adoption of inflation targeting regime.
We have estimated nine technology parameters. We use gamma distributions with a
mean of 1.0 for the priors of the elasticity of substitution between domestic and imported
inputs (€c, €r, €x , €*), which imply Cobb-Douglas technologies. For the adjustment cost
parameters (vr, ve _ oY, oY, 0"), we set diffuse gamma, distributions because of the
uncertainty regarding their magnitude.
Regarding the priors for the twelve parameters governing nominal rigidity, we assume
beta distributions with a mean of 0.65 for the Calvo parameters (O07, 07, 0c, Ox, Ox),
implying that prices are optimally adjusted on average every three quarters.'’ We also set
beta distributions centered at 0.65 for the price indexation parameters (wp, wW7, Wa, Wx,
wy). They are relatively large because we believe there are important inertial mechanisms
in the Brazilian economy, although we use loose priors for this set of parameters.
Turning to wage dynamics, we believe nominal wages are more rigid than prices in Brazil.
Wage negotiations in each workers category usually take place once a year. The minimum
wage, which is earned by a large number of workers, is also adjusted annually. Additionally,
the international evidence that wages are more rigid than prices is quite robust.'® Thus,
‘Using Brazilian CPI micro data, Gouvéa (2007) found a frequency of price adjustment of 1.3 quarter.
However, the mapping from the results from micro studies to the parameters in macro models is not one-to-
one. This occurs for several reasons. The theory of cross-sectional aggregation of dynamic processes shows
that slow macroeconomic adjustments maybe consistent with much faster average speed of adjustments at
the micro level (Altissimo et al. (2007)). Also, when calculating frequency of price adjustments using micro
data, all price changes are considered (optimal changes and indexation-based changes); therefore, a direct
mapping to the value of parameter @ is not adequate. Furthermore, the parameter is somehow model
dependent. For instance, a model with firm-specific capital generates different values for this parameter.
'8See, for instance, Druant et al. (2009).

we assume prior beta distributions with mean of 0.75 for the Calvo parameter Oy, implying
optimal wage adjustment every three quarters. For the wage indexation parameter, we use a
beta distribution with mean 0.65, but slightly tighter than that for price indexation, because
we believe more firmly in the presence of (informal) indexation mechanisms for wages.
The priors for the parameters in the administered price rule (v}, and v%,) are based on
the information about the contracts governing electricity and telephone rates. The impact
of changes in the real exchange rate and real marginal cost is lower than that of the CPI
inflation.
Concerning the parameters of the Taylor rule, we chose relatively loose priors. We assume
beta prior distribution for the interest-rate smoothing parameter, yz, with mean of 0.6 and
standard deviation of 0.15, and normal distribution for the coefficient on expected inflation,
Yn, centered at 2.0, with a 0.35 standard deviation. For the coefficient on the output gap,
Yy, we use a relatively diffuse gamma distribution with mean equal to 0.25 and standard
deviation of 0.1.
The priors for the fiscal rule parameters (¢,, ¢g) were set considering that government
expenditure do react to primary surplus deviations from the target, but not as to meet
the target promptly. So, we use priors with mean at 0.4 and 0.35, respectively. The prior
distribution for the coefficient governing the reaction of the primary surplus target to debt
deviations, dp, was set taking account the fact that the coefficient has to be positive, but at
the same time should not provoke unduly volatility in the primary surplus target.
The parameters related to shocks and variables modeled as AR(1) processes are estimated
using diffuse priors. We use beta distributions for the autoregressive coefficients, except for
that in the inventory investment equation, with mean 0.5 and standard deviation 0.25. The
priors for the standard deviations of the 24 innovations are inverse gamma with mean equal
to 1.0. We also use diffuse priors for the standard deviations of the two measurement errors.

3.4 Estimation Results
We used the Dynare program for estimation (Stéphane et al. (2011)). Posterior distributions
for the parameters were computed using the Metropolis-Hastings algorithm, which relies on
the Monte Carlo Markov Chain (MCMC) procedure.'? Table 3 presents the mean and the
confidence interval (5 and 95" percentiles) for the estimated parameters. As mentioned
before, Figure 2 provides the graphs of the priors and posteriors of the structural parameters.
Observed data played an important role in determining the estimates for large part of
the parameters. In other words, the data was informative in the estimation process. Many
posteriors are tighter than their corresponding priors or are centered on different points of
the support. We can observe these patterns in most of the parameters related to rigidity
and indexation of price and wages, real frictions, and monetary and fiscal policies. The same
occurs for parameters of the AR(1) processes and innovations. The main exceptions are the
inverse of intertemporal elasticity of substitution, 0 — usually of difficult identification —
the elasticity of substitution between imported and domestic inputs in some sectors, and the
administered price rule parameters.
Some results emerge from the posteriors for which data was more informative. The
posterior mean for the habit persistent parameter (&) was smaller than that in the prior,
implying, for &/ (1+), a mean of 0.43, instead of 0.46. The estimated sensitivity of the
country risk premium to net foreign assets (vy) and foreign investors’ risk aversion (yj,) is
lower too.
In the consumption goods sector, the rigidity of freely-set prices is higher than the em-
bedded in the prior. As a matter of fact, the mean of the posterior of 07 is 0.74, which
implies that, in the model, prices would be adjusted optimally every four quarters instead of
three. The estimation was rather informative — the 90% confidence interval goes from 0.68
to 0.81. On the other hand, the posterior mean of the indexation parameter for those prices
!9We ran two blocks, with one million draws each. The resulting acceptance rates were 0.2366 and
0.2310. We disregarded the first 50% of the draws. The multivariate diagnosis indicates that the estimation
converged.

was lower than the prior mean (0.33 against 0.65). Note that its complement, 0.67, does
not mean that prices are not indexed, but they are so to the inflation target instead of the
past inflation. Concerning wages, the estimation confirmed the degree of wage rigidity, but
indicated a lower degree of indexation to the past inflation than the embedded in the priors.
On the other hand, the likelihood was not informative about the parameters governing the
prices of investment goods and imported inputs in domestic currency, which is related to the
fact that those variables are non observables in the estimation.
Regarding monetary policy parameters, the estimations indicate relatively high degree
of interest-rate smoothing (mean of 7p equal to 0.79) and response to inflation (mean of yq
equal to 2.43), and a response to the output gap lower than the one set in the prior (mean
of yy- equal to 0.15, which, for an annualized interest rate, corresponds to 0.60).?° For fiscal
policy, the means of the posteriors of ¢, and ¢g were a little higher than those in the priors,
but with a lower response of the targets to the debt level (parameter ¢,).
In terms of autoregressive parameters, we stress the high degree of persistence in the cases
of temporary shocks to technology and shocks to the domestic risk premium and exchange
rate. Concerning the standard deviation of the innovations, we should be careful about the
interpretation because, in some cases, the shock enters equilibrium conditions in the model
variables through a constant lower than one, implying in practice a lower volatility for the
variable.
4 Model Properties
In this section, we assess the empirical performance of the model. We report the impulse
response functions and evaluate how the transmission mechanisms of different shocks are
reproduced by the model. We also compare the sample moments with the model-implied
20The parameter means are higher than those found by Minella and Souza-Sobrinho (2009), which used a
single-equation estimation of the Taylor rule for Brazil, without including an output gap term. Their point
estimates for the interest-rate smoothing component and for the coefficient on expected inflation are 0.62
and 1.57, respectively.

moments, and calculate the variance error decomposition. Finally, we show forecasting
exercises.
4.1 Impulse Response Functions
We estimate impulse response functions for all shocks. In general, the responses are well
behaved, with the expected signs and hump-shaped paths. For the sake of parsimony, we as-
sess the responses to an interest rate shock, wage markup shock, investment shock, exchange
rate shock, fiscal shock, and permanent technology shock. Therefore, we are evaluating the
results of shocks of different nature — shocks to policy, aggregate supply, and aggregate de-
mand. Figures 3 to 8 present those responses. In Appendix D, we show the impulse response
functions to all remaining shocks. We record the path of the main macroeconomic variables
plus the shock of interest. The solid line is the mean and the shaded area represents the 90%
confidence interval, implied by the posterior distributions of the parameters. We present the
responses up to 12 quarters in order to focus on a more relevant horizon for monetary policy,
but they converge back to the steady state.
4.1.1 Interest Rate Shock
The economy is hit by an interest rate shock of 100 basis points (0.25% in quarterly terms)
(Figure 3). Household consumption and investment decrease, leading to a fall in output. The
presence of habit persistence in consumption and adjustment costs in investment makes their
responses hump-shaped, and so is the output response. Note that the response of investment
is stronger than that of consumption.
Due to the UIP condition, the higher domestic interest rate results in an appreciation of
the domestic currency (a drop in the exchange rate measured as units of domestic currency
per foreign currency). As a consequence, exports decline as expenditure-switching effects
push away the international demand from domestic goods towards foreign produced goods.
Since we assume pricing-to-market and price rigidity, the reduction in exports is not pro-
nounced though. In the case of imports, however, there are two transmission channels acting

in opposite directions. Due to the domestic currency appreciation, import prices fall, putting
an upward pressure on imports. On the other hand, the fall in output pushes imports down.
The income effect prevails, resulting in a negative net effect on imports. Furthermore, the
reduction in imports is higher than that in exports, so net exports become positive. In other
words, the contractionary effect of a monetary policy shock improves the trade balance,
which is consistent with the empirical evidence for Brazil.?!
The downturn in output leads to a reduction in tax revenues. In order to meet the
target for the primary surplus, government lowers its consumption. Moreover, since the
lower output and the higher interest payments make the government debt-to-GDP ratio
to deviate from its steady-state level, government also raises the primary surplus target to
bring debt back to its long-run level. As a consequence, in the fourth quarter, the fall in
government consumption surpasses the output contraction. Therefore, fiscal policy behaves
in a procyclical way.
Because of the output downturn, demand for labor goes down, leading to a reduction in
nominal wages (not shown). The response of real wages is smoother and delayed due to the
initial drop in inflation. The lower demand for capital also reduces the rental rate of capital
(not shown). The combination of lower economic activity and exchange rate appreciation
— both pushing marginal costs downwards — drives inflation below the target. Notice that
inflation also displays a hump-shaped response. Moreover, the response of administered
prices is slower and less strong than that of freely-set prices, but at the same time is more
persistent. The trough of the four-quarter inflation of administered prices occurs in the sixth
quarter and is 0.20 percentage points (p.p.), whereas that of freely-set prices takes place in
the fourth quarter and is 0.31 p.p. This delayed and more persistent response is due to
the backward indexation rule assumed for administered prices and helps to account for the
observed persistence of the overall CPI inflation in Brazil.
In terms of timing, most variables are nearly back to the steady state in two years. The
21Similar result is found by Minella and Souza-Sobrinho (2009), who estimated a semi-structural model
for Brazil, using similar sample period.

largest drop in the four-quarter CPI inflation occurs in the fourth quarter, and is around 0.25
p-p. Note that, since the monetary authority reacts to its own shock through the Taylor rule,
the interest rate in the first quarter is lower than 100 basis points and, more importantly,
is already close to zero in the fourth quarter. Keeping the interest rate fixed for one year
would generate a larger fall in inflation.
4.1.2 Wage Markup Shock
In this subsection we analyze here a domestic cost-push shock, which also has direct demand
implications. A positive shock to wage markup immediately raises real labor income and
consequently the marginal cost of consumption goods and, therefore, CPI inflation (Figure
4). Rule-of-thumb households spend their additional labor income on consumption goods,
which boosts private consumption. The monetary authority responds to the inflationary
pressures by raising the interest rate, which reduces investment and the consumption of
optimizing households. The reduction in optimizers’ consumption, however, is smaller than
the increase in the consumption of rule-of-thumb households in the first year; so aggregate
household consumption goes up.
As the interest rate rises the domestic currency appreciates, exerting an upward pressure
on imports and lowering exports, which results in a trade deficit. Exports also go down
because the higher production costs make them less competitive in world markets. Imports
are also boosted by the substitution between domestic and imported inputs arising from
the more expensive labor. The relative price of government consumption goods rises as the
relative contribution of wages to their production costs is higher than for the other goods.
As a result, the primary surplus-to-GDP ratio falls, triggering a reduction in government
consumption. Thus, government consumption, which in general tends to follow output, drops
more quickly, amplifying the contraction in aggregate demand.
In spite of the boost in private consumption, the reduction in investment, exports and
government consumption, together with the increase in imports, prevails, resulting in a
hump-shaped fall in output. In turn, the contraction in economic activity and the wage rise

push labor demand down, which also displays a hump-shaped path. The fall in employment
lowers the consumption of rule-of-thumb households, and aggregate private consumption
becomes negative in the second year.
Although the markup wage shock lasts basically only one period, the four-quarter CPI
inflation peaks in the fourth quarter. Note that, as before, the response of administered
prices is more delayed and persistent than that of freely-set prices. Thus, the wage also
exerts a persistent effect on relative prices and inflation.
In a nutshell, a cost-push shock originated in the labor market increases inflation, private
consumption and imports, and depresses investment, exports, government consumption, out-
put and employment. Even though the positive effect on private consumption is short-lived,
the shock has relatively persistent effects on output, employment and inflation. Note that
this persistent effect does not arise from the estimated persistence of the shock itself, which
is close to zero (py = 0.09), but results from the propagation mechanisms of the model.
4.1.3 Investment Technology Shock
A positive shock to investment technology (reduction in the adjustment cost) boosts the
demand for investment (Figure 5). It raises employment and consequently the consump-
tion of rule-of-thumb households. Following the fiscal rule, government consumption is also
expansionary. As a result, output rises as well.
The surge in demand for labor and capital increases nominal wages and the rental rate of
capital, putting upward pressures on production costs and inflation. The monetary authority
then reacts by raising the interest rate in order to cool down domestic demand and inflation.
Imports increase more than output, in spite of the real exchange rate depreciation. The
reason is that the share of imports used in the production of investment goods is higher than
in the other sectors. Thus the model implies that investment booms are accompanied by
higher imports and deterioration of the trade balance. This result is line with the evidence for
Brazil that large part of fluctuations in imports are associated with investment fluctuations.
As the shock dies out and monetary contraction becomes more effective, output gap

returns to zero and inflation goes back to target. However, the reduction of net foreign assets
due to the trade deficit leads to a relatively persistent depreciation of the real exchange rate,
which later will have a positive effect on exports.
Therefore, a positive innovation to investment technology boosts aggregate demand and
output, and puts upward pressure on inflation. It also leads to short-lived deficits in the
trade balance.
4.1.4 Exchange Rate Shock
An unexpected depreciation of the real exchange rate boosts exports and depresses imports
(Figure 6), generating a significant positive trade balance. Note that the 1% innovation
to the UIP condition increases the real exchange rate by about 9%. The rise in import
prices increases the marginal costs of consumption goods, pushing inflation upwards. The
monetary authority then reacts by raising the interest rate, which reduces the consumption
of optimizing households and depresses investment. Investment is also negatively affected
by the increase in the relative price of investment goods (more intensive in imports than
consumption goods).??. The higher inflation lowers real wages, and thus the consumption
of rule-of-thumb households. Both consumption and investment display a hump-shaped
response.
In the first year, the positive response of net exports offsets the contraction of the domestic
private components of aggregate expenditure so that output is relatively stable. In the second
year, however, the contractionary effect on domestic demand starts prevailing for the output
path.
The shock is very persistent and the deviation of the real exchange rate from its equi-
librium value approaches zero only at the end of the third year. The effects on the CPI
inflation are even more persistent. The four-quarter CPI inflation peaks in the fifth quarter.
The pass-through of the exchange rate to CPI inflation is around 7% in the first year and
14% in two years (calculated as the ratio of total CPI increase to the rise in the exchange
2For this effect in the Brazilian economy, see da Silva Filho (2007).

rate in the first period).
In summary, positive innovations to the exchange rate are associated with higher inflation
and exports, and lower consumption, investment, imports, and real wages. The initial effect
on output is around zero, but becomes significantly negative in the second year.
4.1.5 Fiscal Policy Shock
Here, we define the fiscal policy shock as a shock to government consumption, whose response
functions are shown in Figure 7. The positive innovation to government expenditure increases
GDP and the demand for labor and imports. The rise in employment, in turn, boosts the
consumption of rule-of-thumb households. As a result, aggregate private consumption goes
up in the first quarters.
The higher demand for production factors raises the marginal cost of consumption goods,
pushing inflation upwards. Monetary authority reacts by raising the interest rate. Conse-
quently, investment and the consumption of optimizing households both drop below their
long-run values in a hump-shaped manner. The trade balance initially deteriorates but the
ensuing depreciation of the real exchange rate tends to restore the equilibrium in external
accounts.
In the first quarters, the net effects on both private consumption and output are positive,
whose paths closely follow that of government consumption. This result is in line with the
empirical evidence on the effects of fiscal policy shocks.?? In terms of magnitude, a 1.0%
shock in government expenditure raises output by 0.3% on impact, and by 0.1% on average
over the first year. Given that the share of government consumption in GDP is 0.20 and
the fact that government consumption actually rises by 1.3% in the first period, the model
implies a government spending multiplier on output of 1.3 on impact (the multiplier says
how many units of output an increase of one unit in the government consumption generates).
Taking into account the total increase in output and government consumption in the first
year, the multiplier is 1.1. On impact, the multiplier on private consumption is 0.5. Note,
3See, for instance, Galf et al. (2007).

however, that the monetary authority reacted in a counter-cyclical way, reducing the value
of the multiplier. The latter would be higher if monetary policy was rather accommodative.
Therefore, the model suggests that a fiscal expansion leads to an increase in both output
and inflation, and negative results in the trade balance in the short run. Although the values
of fiscal multipliers vary across models and empirical studies for other countries, the values
found in this paper are in line with the range found in both approaches.”*
4.1.6 Permanent Technology Shock
A permanent technology shock affects positively all aggregate demand components and real
wage, permanently shifting their levels. In order to capture this feature, Figure 8 displays,
for those variables, the deviation from the balanced growth path that would prevail in the
absence of the permanent shock to technology. In other words, it records the permanent
change in levels plus temporary deviations.
Initially, the strongest responses are those of investment and exports. Capital becomes
more productive, encouraging capital accumulation. Exports are benefited by the fall in
marginal costs, which increases their competitiveness and generates a mild trade surplus on
impact. Also in the first quarter, the demand for labor drops as it is possible to produce
the same amount of goods with less inputs. Nevertheless, as aggregate demand rises in the
following quarters, more labor is required in the production process.
The higher productivity is translated into higher real wages and, in the short run, into
lower marginal costs. Later on, however, the increase in the return to capital raises produc-
tion costs and pushes inflation up. The monetary authority then responds by raising the
interest rate, which appreciates the domestic currency and boosts imports even further.
In the long run, inflation goes back to the target, but the levels of all variables containing
a real unit root remain permanently higher, in the new balanced-growth path.
24For a comparison of the fiscal multiplier accross different structural models, see Coenen et al. (2010).

4.2 Moment Conditions and Variance Error Decomposition
We simulate the model to generate second order moments, and compare them to those from
the data (Table 4). The results are mixed, as the model matches some empirical moments
but tends to overestimate others.
Regarding real variables, the model replicates fairly well the standard deviation of the
quarterly growth rates of investment, exports and imports. In contrast, the volatility gener-
ated by the model for the growth rates of consumption, government consumption, employ-
ment and GDP is higher than those from the data. The results in terms of relative volatility
are better. In accordance with the data, investment, exports and imports are substantially
more volatile than output, and consumption volatility is similar to that of output.
Concerning nominal and financial variables, the results are mixed as well. The implied
volatility for real wage change, real exchange rate, and administered prices are relatively
close to the empirical moments. However, for CPI inflation, freely-set prices, and nominal
interest rate, the model generates higher second order moments.
We also calculate the variance forecast error decomposition for the main variables. Table
5 presents the results for quarter-on-quarter GDP growth and quarterly CPI inflation, over
several horizons: one, four and eight quarters, as well as asymptotically. In the appendix,
tables Al to A4 show the results for other variables.
For GDP growth, in the short run, the bulk of the variance of forecast errors is related
to shocks to aggregate demand components — basically household preference shock, export
demand shock, and import demand shock, and to a less extent to investment shock and
fiscal policy shocks (government consumption and tax rate). At longer horizons, shocks to
transitory technology and domestic risk premium also gain relevance. In contrast, monetary
policy shocks were not important for the forecast errors. Note that we are referring to the
role played by the shock and not to the systematic component of the rule.
In the case of CPI inflation, the forecast error variance is dominated by price shocks,
although their importance diminishes at longer horizons. Shocks to price markup, adminis-

tered prices and wage markup account for 76% of the forecast error variance over one-quarter
horizon. In the eight-quarter horizon, they respond for 47%. At longer horizons, the shocks
to domestic risk premium, transitory technology and exchange rate gain relevance too.
4.3 Forecasting Exercises
In this subsection, we assess the forecasting performance of the model and analyze the
forecasts in two specific moments. We estimate the root-mean-squared errors (RMSE) of
the forecasts using SAMBA, and compare them to usual benchmarks, where the forecast is
given by the following: i) the last observed value; ii) the sample average; and iii) a Bayesian
vector autoregressive (BVAR) model. When available, we also compare the model forecasts
to those from a survey conducted by the BCB among professional forecasters.
For this forecasting exercise, we used the following procedures. We assess forecasts for
one to eight quarters ahead. The first forecast is made with data up to 2004Q4, and then we
update actual data sequentially until 2008Q4. Note that our sample size goes from 1999Q3
to 2010Q2, which implies that the number of periods for the estimation of the RMSE is
25 Thus, we should consider the results with some
relatively low — only 16 data points.
caution.
Due to the short size of the sample, the estimated parameters are based on information
for the entire sample period. Ideally, we should reestimate the parameters using only the
information up to the last quarter before the forecasting period. However, we did not pursue
this avenue as we would be using only 22 data points for estimating the parameters to be
used in the forecasting cycle starting in 2004Q4. On the other hand, we estimate all 58
non-observable variables using the information available only up to that data point. In other
words, in each forecasting cycle, we reestimate the non-observables. Furthermore, for that
estimation, we remove the average from the series based on the values up to that data point,
and add this average when making the forecast. Thus, we do not use the averages over the
5Tf we consider periods without any overlap, it is only five data points in the case of four-quarter horizon.

whole sample. Moreover, we conduct only unconditional forecasting. This means that, even
for foreign variables, their forecasted trajectories are given by the AR(1) processes built in
the model. The same is applied for domestic variables modeled as AR(1) processes.
The BVAR was estimated using four variables, which are also used as observables in the
estimation of SAMBA: GDP growth rate, CPI inflation, real effective exchange rate, and
Selic interest rate. As in SAMBA, we used quarterly data, starting in 1999Q3. In the case
of the BVAR, we reestimate the model every forecasting cycle.
We evaluate the forecasting performance for four-quarter CPI inflation (price level in
quarter 7 compared to price level in quarter i — 4), year-on-year GDP growth rate (GDP
volume in quarter 7 compared to the GDP volume in quarter i — 4), and the Selic rate
(measured as % per quarter). Figure 9 illustrates the results. In the case of the CPI inflation,
SAMBA forecasting performance is superior to those of the mean procedures at all horizons
and of the last observation at five- to eight-quarter horizons. However, when compared to
BVAR performance, the results are mixed. Up to five quarters, the point estimates of RMSE
generated by the BVAR are lower than those arising from SAMBA, but are higher for six- to
eight-quarter horizons. Considering the four-, six- and eight-quarter horizons, the RMSEs
for SAMBA are 1.74, 1.67 and 1.63, respectively, whereas for the BVAR are 1.34, 1.75 and
1.79, respectively. Note that those forecasts are made in a mechanical way.
For the year-on-year GDP growth rate, the results are less promising. The RMSE is
large for all models. Similarly to inflation, in terms of point values, SAMBA provides worse
results than the BVAR for horizons up to five quarters and better ones for longer horizons.
Finally, in terms of forecasting for the Selic rate, SAMBA provides better performance than
the other models for most of horizons. On the other hand, the RMSE seems large for all
methods.
Finally, we conduct two exercises in order to have a better sense of SAMBA projections.
We present the projections in two specific dates: 2004Q4, when most of the effects of the
2002-2003 confidence crisis had faded away, and 2008Q4, when GDP had plummeted as a

result of the global crisis. Figure 10 shows the forecasts and corresponding actual values for
four-quarter CPI inflation, year-on-year GDP growth, and Selic rate level (% per year). The
shaded areas represent 40%, 60% and 80% confidence intervals. They were estimated based
on both the variances of the shocks and parameter uncertainty.
In general, the forecasts are in line with the actual values, mainly for inflation and GDP
growth. In 2004Q4, the model predicted the fall in inflation and the increase in the GDP
growth in the medium run, although it did not anticipate the rise in the interest rate. For
the forecasts made in 2008Q4, the model predicted the fall in inflation, a further decrease in
the y-o-y GDP growth and its resumption later on. In this exercise, the model overpredicted
the Selic rate.
As mentioned earlier, all these exercises were unconditional ones and made in a me-
chanical way. Other countries’ experience indicate that the combination of a DSGE model
with specialists’ forecasts — for some domestic variables for the very short run and for for-
eign variables at all horizons — can significantly improve the forecasting performance of the
model.
5 Conclusions
We developed and estimated a DSGE model for the Brazilian economy. The model incor-
porates the usual features commonly found in standard DSGE models as well as specific
aspects of the Brazilian economy. In particular, SAMBA incorporates administered prices,
a fiscal rule in accordance with the fiscal regime in place, external finance of imports, and
imports used as inputs in the production function.
The model has reasonable properties. The impulse response functions generated by the
model are well behaved and consistent with available evidence. Therefore, we believe the
model can be used as a tool for assessing the impact of different shocks and scenarios for ex-
ogenous or even endogenous variables. We should stress the role played by structural models
in attaching economic interpretation, in a rigorous way, to economic developments, scenario

analysis and forecasting. In contrast with purely statistical models, structural models like
SAMBA can be successfully used as a story-telling device in the policymaking process.
In terms of forecasting, we compared the model performance with benchmark procedures
and with actual values in two specific moments. Those initial mechanical exercises are
promising. We believe, however, that a more thorough assessment of the model forecasting
properties will be possible only after the model is tested in real time for some period of time.
In particular, it should be used as part of a well defined forecasting cycle, which includes the
use of experts’ forecasts for the path of many domestic variables in the very short run and
for external variables at all horizons.
The fact that the model includes a large set of observables broadens the range of issues
that it may tackle. Nevertheless, we already anticipate that the current specification will
require further improvements, as is usual in modeling frameworks. For instance, financial
frictions have not been incorporated in the model yet. We recognize that currently there has
been an enormous effort to add those frictions in DSGE models”, and the BCB is engaged on
that project. Financial regulatory issues should also be part of the scope of the framework.?’
However, we believe this research agenda has not yet developed a consensus DSGE framework
that can be used with confidence to address the most pressing issues regarding financial
stability and monetary policies. As Gertler and Kiyotaki (2010) point out, large part of the
earlier macroeconomics literature on financial frictions emphasized credit market constrains
on nonfinancial borrowers and treated financial intermediaries largely as a veil, whereas the
global crisis featured a disruption of financial intermediation.
A.1 Households
The conditions describing household consumption are the following, derived from (9), (21),
and (76):
. Go. \ _[- CO\” RSP
t t+1 t+1
cpr =(1- T,) WLM, A.2
Cr = wearCP + (1 — wer) CP. A.3
The asset accumulation equations are derived from equations (11) and (7), as well as
from the economy-wide versions of (8) and (2):
RSP ox Resp ox
E, ( USE (22, Ast) =F, (Se FES (zZ,.) At) | (A)
t+1 t t+1

AQE = BE, (24,) ° Mua [RA + QB, (1 — 9)], (A.5)
1-Ss Bil s! ZEA Zi
Zila Aha) Zh
- ~ 2
-o x Zhaliwa\ ( Zaliv I
+BEt (27.1) NiQh 8" ae ee Lists
Zits Ziti
ZT ~
yg ( 24 I, (A.7)
Zi li
where Rf, = Riy/P&,, and the country risk premium and the domestic risk premium are
MQ? = A.Q* (A.6)
Risa = (1-8) (Ki/Z7) 4
given by equations (12) and (13), which we repeat here for convenience:
SP = S™ {exp [—vp (Bi — BY) +e) (Vi — VY] 2, (A.8)
1
SP = (5?) °? (S2.,)°® exp fe? } . (A.9)
In turn, the labor market conditions are obtained from equations (19) and (20), where
we used the fact that W? = Ww”:
Ww
t Ww tt+itrt+t TW Ww; t+i+Vtt+e \ epg
i=0 jtti
ee mo... w.,\ er”
E, S” (Ow8)! | Ze Zee (Fe | (Nig) |
where
and

A.2 Firms
The choices of the domestic input producer are based upon equations (28), (29) and (30):
Z2YP
RE =aQP, A.12
t aQ; K, ( )
- y,?
W, = (1—a) QP Nov’ (A.13)
RE\° (Ww, \'° 4
p_ (ff t
= ( 0 ) ( ") 2 (A.14)
The price setting by importing firms comes from conditions (36) and (37) and is given
by the following equations:
[oe] ri i —EM c et
EY (08) Zhe Aeess (GEE) (QM Qi Qh Mer
qs" — (A.15)
‘ eu — 1 l-o Tibi trem M\&M yy ,
BS (On18)' Z, pe, t+i (Fe =) (QM) Misi
i=0O t,t+i
1
yu’ tre s\l-ey |
QM = |Ou (Ze Qi) + (1-0) (Q?”) ; (A.16)
t
M
Ti’ = -4-Ilr, (A.17)
t-1
where -
- Nei
Ne tpi —_ i
and, as mentioned before, QM” = P"/P,“"is the foreign-currency relative price of imports,
QV = P™/P® is the domestic-currency relative price of imports, and Q,Q/"is obtained
from the convenient transformation of S;P“"/P° = (S,P° /P°)(P /P).
The real marginal cost and the optimal input choices by sectoral intermediate good
producers come from (41), (82) and (84), respectively:
(A.18)

where
_ gt gM ou ~ t t —] GM ol ~ t t
. (ca 0) THE 41) TF
and MCF = MC/"/PS.
The price setting by sectoral intermediate good producers, in the case of H = J,G, is
based upon conditions (44) and (45) and sectoral inflation definitions, and is given by the
following equations:
P
P
€ 1
; Qu ; ; H,t+i 2,
(ia Zhe Me, t+i ( a he (Q; ‘\ ee Ona (ety, t+ — 21)
t,t+0
P
P
(04) Zhe Mei (i (Q; ) mee MCE YE aaa
t,t+i
ll
3°
i}
rH 1—-eF; es ee 1-5
Qi = = (0 & Qe : + (1 — On) (Q; ) ue , (A.22)
Wt = “11°, (A.23)
The price setting in the consumption goods sector as well as the CPI inflation are based
on conditions (48)-(51) and (53) and on inflation definitions:
oo €Ot+i 1
Ey » (08) Zhe Masi ta (Q; ‘) “Ciets YG (eCrr4i _ 1) (A.24)

it = oa (Va) + (18a) (Ty) hee A.28
4
p= Qin (Te) A.29
1
P
1-eP 1-eP —e
Uf = [ora (TQHL) E+ (= a) (HF QR) EYE, A.30
The price setting in the export goods sector is described by conditions (56)-(57):
P
oo * x \ &xytivt
Be Q 1 (0x18) ZeakeMass | px (QP) Qui Qe (CxriABY)
i=0 aa
<P
lore) * x* X,t+i p
_ t ml—o KX tttiet+i Sk ey pi yol xX xX Pp
= F; 5 (Oxf) Zerit x (Q; ) ‘ MCR Aiex tsi
i=0 tt+i
xX* l-ex , P Xt
ax = lax (xs +) + (1-65) (QE) (A.32)
Ti* = mn. (A.33)
Finally, the stationary version of the world demand for Brazilian exports comes from
(60):
—eE
X, = et Yi", A.34
where

2 Xia/Ye
ret ag (gary aie ADE tint) ( (gary ate AE oa)
A.3 Government
Monetary policy is described by equations (61) and (62):
(Tm: Fi 1\ 70 IR
Ilys, :) E,TI’,..,)4 Yy, \’
ry = ris, | f ET a) ( L ) ZB (A.35)
B (ZZ) =c \4 LAY
(Tes) ‘= (Tm) ” ((..) ‘) exp {er } ) (A.36)
whereas the fiscal side is described by conditions (63), (64), (68), (69) and (71):
S} = 8" + dg (S_, — 8”) + 63 (S{ — 8”) — sez? A.37
SH = S" + ps (SL, — S”) + bp (BY — BY) +8, A.38
T,=T+pr(%-T) +e, A.39
Gy = a (T; — SY), A.40
Bier _ Bi Vina SY. A.41
R, It ZzY,
A.4 Resource Constraints and Identities
The description of the domestic economy is completed using conditions (81), (83), (85), (80),
(79), (78), (86), (87), and GDP deflator definition:

vxp = OE (2) QQ
Ty =. (A.53)
A.5 Rest of the World
The equations for the ROW variables are the following:
In Y;" =InY*+ Py» (In Yi*4 —In ¥*) + ex" A.54
nQ™ =nQ™ + pow (InQM, —nQ™’) +22", A.55
MO" = °° + py. (HS, — 0%") + A.56
Vi =V* 4+ py (ViiL-V*) Fer, A.57
Ri = RY + pp» (Ri, — RB’) + ef. A.58

B Appendix B Steady State
In this section we derive the deterministic steady state of the stationary model. First, we
find the steady-state prices and allocations, and then we derive the corresponding relations
that are used in the estimation.
B.1 Prices
It is possible to fully determine all steady-state prices — except QY — in terms of exogenous
variables and structural parameters, without any reference to allocations. Because the model
entails full indexation and taking into account that, in the steady state, the real exchange
rate Q and the relative price of foreign exports (domestic imports) Q™” are constant, in
the long run all prices in the domestic economy grow at the same and constant rate Tr’.
Therefore, all steady-state domestic inflation rates, including administered price inflation,
are equal to the inflation target, which in turn is exogenously given. The terms describing
price and wage distortion vanish in the long run.
Hence, in the case of consumptions goods, Q4 = Q” = Q*” = 1. It thus follows from
equation (A.24) that the marginal cost in the consumption goods sector is the inverse of the
price markup in the sector:
E
MCS =, (B.1)
€o
Given the real exchange rate and the relative price of foreign exports (domestic imports),
we calculate the domestic-currency price of imports using (A.15) and (A.16):
QY =Q! =—“_qq™". (B.2)
EM — 1
Next, we substitute (B.1) and (B.2) into the marginal cost for consumption goods (A.18)
and calculate the relative price of the domestic input:
1 Py l-ec 1— “eo 7
where QM = [1+ tc (R*S® -1)] Q™.

Now that we know Q”, and taking into account the fact that MC° = Q”, we calculate
the relative price of government consumption goods using (A.21):
Qo =Q% = 2-Q?, (B.4)
as well as the sectoral marginal costs MC’ and MC*, both based on (A.18):
1
MC! = [27 (Q”)' "+ 0-an (QM), (B.5)
1
MC* = [zx (Q?)* += ax) (Q¥) |, (B.6)
where QV = [1 +7 (Rs — 1)| Q™ and Q¥ = [1 + lx (Rs — 1)| Q™.
Using (A.21) and (A.31), we obtain the following sectoral relative prices:
P
Qi =Ql =—!— mc! (B.7)
e, -1
P x
_ — ; B.8
The consumption Euler equation (A.1) pins down the equilibrium nominal interest rate:
aC o
Il (27
per bo
where we normalize S? = 1.
The investment euler equation (A.6) implies that the shadow value of capital is equal to
the relative price of new capital good:
Q* =Q'. (B.10)
Knowing these two prices allows us to compute the rental rate of capital, using the capital
RX = (io —(1- ») Q*. (B.11)
Based on equation (A.14), we are able to express the (stationarized) real wage in terms
Euler equation (A.5):
of the domestic input price and the rental rate of capital:
W=W* =(1-a)(Q”)™ a)" . (B.12)

Finally, the UIP condition (A.4) pins down the country risk premium as a function of
the real interest rate differential:
—C
gn (R/T)
aia (B.13)
B.2 Allocations
We can use the market clearing conditions (A.42)-(A.45) to eliminate Y", for H = C,G,I,X.
Similarly, we also have that YP = G. Given the export price, the real exchange rate and
world income, we use (A.34) to obtain the level of exports:
Xaat (Qe yoy. (B.14)
Next, we notice that, from condition (A.37), the primary surplus-to-GDP ratio is equal to
the exogenous target S”, which in turn can be plugged into (A.41) to determine the domestic
debt-to-GDP ratio.
The model can be now reduced to a system of sixteen equations in the following unknowns:
nominal GDP and GDP components (QYY, C, G, I, M), the per capita consumption levels
in each household group (C°, C®"), and the production inputs (K, N,Y?,Y?, WM"). The
equations determining these allocations are nonstochastic variants of equations from the
subsystem (A.2), (A.3), (A.7), (A.10), (A.12), (A.13), (A.19), (A.20), (A.40), (A.46), (4.47)
and (A.51):
QY =C+Q'1+Q°G + QQ* X — QQ" M, B.15
C = wrrC™ + (1 -— wer) C?, B.16
: _,, (2°Y)
G=(T-S") Qa B.17
7=R(1-42), B.18
M = M°+M' + M%, B.19

Ww 7 _
G° = (“aes ) i (1-s) , B.20
CRT — (1-T)WN, B.21
. ZZQPYP
__ DyD
N=N+(1 a) eo B.23
W
YP=VP+VP+GH+Y¥, B.24
Y? = (2 oye H=C,1,X B.25
~ Qu oH
M" = (1—az) (247) Y", H=C,1,X. B.26
Once these sixteen variables are simultaneously determined, we are able to compute
L*’, NX¥ and B*Y using the nonstochastic versions of (A.48)-(A.50). Furthermore, we can
also back out the corresponding steady-state shares s;, 7 = C,G,1,X,M. Given the relative
prices and these shares, it is straightforward to obtain the relative price deflator using (A.52),
and then recover the real GDP, Y.28
However, in order to better replicate the data, we estimate the model conditional on the
values we calibrated for key steady-state relations, such as great ratios and shares, based
on the National Accounts and Balance of Payments. Namely, we calibrate the shares of the
aggregate demand components in GDP (sc, 87, 8g, $x, 8m), and the parameters w?, w¥ and
aw of the production function of sectoral intermediate producers. We can express the above
equations as a function of these and other calibrated values. We also calibrate steady-state
debt and primary surplus ratios (B;", BY, 8”) based on the data.
28The determinacy of the steady state depends on the normalization of Q and Q™". This amounts to say
that we are normalizing the objects SPC’ /P© and SP™” /P°. Notice that the price of the consumption good
is the numéraire, that the nominal exchange rate does not appear explicitly in the equilibrium conditions and
that the prices PC’ and P™" are determined abroad and thus are taken as given by the small open economy.
Therefore, our normalizations go through without loss of generality.

Based on the above steady-state conditions, we present below the resulting relations,
which enter in the log-linear model.”” We also calibrate the steady-state values for R*, S?°,
Lo, lr, bx, &&, ef, e&, e&, and €,7, which appear in those relations. Beforehand, we present
the following definitions:
C Qil Q°G Q* x QQ” M
So = aS) 81 Says) 86 = Fyps) 8x SF) 8M SS (B.27)
Qry Qry Qry Qry Qry
S = —;3 sur= =<} $SM.x =——}
M,C Ory MI Ory M,X Ory
_ QPy?. _ QPYe _ QPY? _ QPYe _ QPYe
SD = QYY > SDC= QYY > SDI= QYY > SDX = QYY > SDLX = QYY :
The value of sp, which gives a measure of the share of the domestic input in GDP, is
given by:
eh -1 ee -1
Sp = —P Sc FP SG... (B.28)
C G
| L+ic (R*S® -1 | P-1
(1 aw) | ( : )| aw? f p Si
[1 + or (RS — 1)] €]
(1 — w) [1 + 1c (R*S”" — 1) wP ek — le
X/ [1 +cx (R*S8* — 1)| Xl ek
— gy [1 tic (R*S® — 1).
Eu —
Since we calibrate w?, 78 and w¥, we are able to find the model-consistent value of @2
using the equation below:
1 & ep —] ce -1 ee 1
D_ C D&I D&G DEX
Wo= Pp Sp — Wf —p—S81 — WE p— 8a — We Sx | - (B.29)
The values of sizc, 5,7 and sjy,x are determined by the equation below:
cP] 1
4 py B.30
29Some of the steady-state relations do not affect the log-linear model; so they are not shown here. Further-
more, we do not use the derived relations sg = T—S” and s; = [27 — (1—4)] asp/ [(27)” e'-a- 6)
because of the measurement errors involved. For instance, in the data, S” is defined for the whole nonfinancial
public sector (including state-owned companies), whereas sq is resctrict to government consumption.

and those of spc, 8p,1, Sp,g and sp,x by
SD.H = WH p SH» (B.31)
Ht
where H = C,I,G,X.
In the linear version of the model, the parameters sp,7 and sp appear in the equation
of market clear condition of domestic inputs (C.35), sy,” in the equation of market clear
condition of imported inputs (C.36) and in the law of motion of external loans (C.37), and
oP is used in the equation of the marginal cost of producing consumption goods (C.15).

C Appendix C The Log-Linear Model
In this section we log-linearize the BGP equilibrium conditions around the deterministic
steady state. The linear equations presented below are the ones used during the estimation
stage. They are derived from the equations presented in Appendix B. Following our con-
ventions, we use lower-case letters to denote deviations and log-deviations from the steady
state. All variables are log-deviations, except for those expressed as ratios to GDP, as is the
case of b/, b;/,,nx/,l;", which correspond to deviations from the steady state.
As mentioned before, in order to facilitate identification in the estimation stage, and in
the sake of symmetry, we assume that the shock to import demand is the same across sectors
(zie = 7@, VH =C,I,X). For estimation purposes, we use the reduced-form versions of
the price markup shocks, and assume that they are equal across the sectors of consumption,
investment and government goods, but different for the export goods sector. We also ignore
any productivity differential between the Brazilian economy and the rest of the world, thus
assuming z/ = 0 in the export demand equation. Finally, since the UIP condition is known
to have a very poor fit to the data, we add the ad hoc shock ze to its linear version.
The equations are listed below. We present the number of the corresponding equation in
Appendix B between parentheses. In the notation used below, mrs; is the marginal rate of
substitution between consumption and leisure, z/ and 2!” denote the reduced form of price
and wage markup shocks, respectively, and v/ is the linear version of the sectoral indexation
rules, where in this case H = C,I,G,X,M.
C.1 Households
Consumption of optimizing households (A.1):
O_ Ki O | l E,.c2 l-k LB Ba? Pza hoz (1—pc)1-#) 6
Cy lpe + try a (1+) (ry + 8; iTew) 4 Rt o(1 +f) At
(C.1)
where
Ren (27)

Consumption of rule-of-thumb households (A.2):
T
cf = We + me = a
Tt.
Aggregate consumption (A.3):
Gq = aed? + (1— ae) &,
where
CRT
Wo = WrRr =
C
Real exchange rate - UIP condition (A.4):
B * * *
G = Eitesi — (r: + Ss — Eyre.) (r sP Eyre) + ze.
Shadow value of capital (A.5):
~(1—6 ~(1--6
where
Investment (A.6):
Law of motion of capital (A.7):
1-6 1—0\.
Country risk premium (A.8):
Ss = Ppt pyy + % -
Domestic risk premium (A.9):
Sp = PBsi_y t:
84
(C.2)
(C.3)
(C.4)
(C.5)
(C6)
(C.7)
(C.8)
(C9)

Real wage change (A.10)-(A.11):
Wy B Ww
Aw, = —>— Aw, + —>— Ey Awisi + Aw (mrsy — wz) +
t 1+ Buw t—1 1+ uw t t+1 w ( t t) t
1 1+ B
= (my %1) = (my x) = Et (mh + Za
where ~
he = (1 — Ow) (1 — Ow8)
w= = ’
Ow(1+ en) (1 + Bow)
Au, = Ww, — Wit,
oO ~
mrs, = 2 +n — Xe = NE + A [e? —f (C24 2/)| ,
Ww Wow
C.2 Firms
Rental rate of capital (A.12):
K
re =o typ —kht+ 2%.
Relative price of domestic input (A.13):
K
D_ D
G = ar,
+(l-a)w,- 7%.
Labor (A.13):
m = an (GP +4 — wr),
where _
N-—WN
N
Phillips curve for import prices (A.15)-(A.17):
<l.
an =
M
1 M
*
r Ot
AM (a qi) BE, (mM
where
M
— Vi
),
(C.10)
(C.11)
(C.12)
(C.13)
(C.14)

vl = wy, + (L—wm) iy,
M _=M M Cc
G =~Uitt™ —T,-
Marginal cost of sectoral goods (A.18) (H = C,G,I,X):
me! = aug + (L— an) [gM + wy (rf + 87°) + 07 [(mi? — yf") — (miZ, — vi) — a",
(C.15)
where
iy R* SP
l+ey (R*S8* -1)’
and remember that for H = G, wg = 1, so mc? = q?.
x
Oy =
Sectoral demand for domestic input (A.19):
Yne= Ye — en (a — me’). (C.16)
Sectoral demand for imported input (A.20):
rfl = ull — AB al ir (re +90) — melt] + A [it (lls — wl) +].
Phillips curve for the prices of investment and government consumption goods (A.21)-
(A.23) (H =G, 1):
nt ul = dy (mej! — qi’) + BE, (me — vtia) + 2, (C.18)
where
yp = O08) = 81)
Ox
H _C
vf = watt, +(l—-wa) FY,
Ent
€H — 1?
Gh = Gait me ~ Ty. (C.19)
Phillips curve for the price of consumption goods (A.24)-(A.26):
nh — uF = dp (mer — a ) + BE, (mh — vit) + 2, (C.20)

where
vy = wat, + (lL—wa) tr,
G = Gatm —T: (C.21)
Administered price inflation (A.28):
mA = Oavd + (1—64)r°. (C.22)
Rule for administered prices (A.27):
1
uf = X44 [teases + U4 (Ga — as) +04 (meh, — mef_s)] +(L-xa)af + 7,7 (C.23)
C _,C 1,0 1,0 | _¢
where Te 4-5 = Toy tot We 3g t Te 4.
CPI inflation (A.30):
nl = wank t+ (1—@a)a?. (C.24)
Phillips curve for the price of export goods (A.31)-(A.33):
* ~ x
T — Up = Ax (me; — Ge q) + BE (mA —~ Ups) +4, (C.25)
where
= (= 88) (1x)
x = ;
Ox
xX
U = WxT + (l—wx) 74,
Ge =Gaitm —T. (C.26)
y= yf + ae [0 (tra — ha) — +"). (C.27)

C.3 Government
Monetary policy rule — interest rate (A.35):
l_o l ¢ Cc
_ 1_
T= YrTt-1 + (1— Yr) qi t-3t+1 + Yk Gaze _ sa] + vw
-C 1 eC
=—C
where Thing = Tit The t+ 1h3 + TH
Inflation target (A.36):
1 1 We
=C _ =C TI
4 ltt+4 = Py AM t—4t +E;
Fiscal rule — primary surplus-to-GDP ratio (A.37):
st = bs8t_1 + 38) — saz’.
Target for the primary surplus-to-GDP ratio (A.38):
5 = pgSi_1 + Opt + ep.
Tax rate (A.39):
Tt = PrTt-1a + ef.
Government consumption (A.40):
1
n= (1-s/)+y+aq -@.
SG
Law of motion of the government debt (A.41):
—C _
bd = Apbid_, + BYr, — Rs} + \pBY (y—1 Ut Th a x
where
88
),
(C.28)
(C.29)
(C.30)
(C.31)
(C.32)
(C.33)
(C.34)

C.4 Resource Constraints and External Sector
Market clear conditions for final goods (A.52)-(A.45):
so we eliminate y’, H =C,G,I, X.
Market clear condition for domestic inputs (A.46):
D _ .D,D D,D D,D , .D,D
Ye = SCVCt Tt SAVE TST UT + SXUX
where
s2 = QUY? _ SD,H
u QPYP SD
Market clear condition for imported inputs (A.47):
M,C , .M,I . .M,)X
Mm = Sam, +87 mM, +s5ymM,_,
where
MysH
M Q M Su,Hem -1
H .
S =
Q’M SM  €M
External loans-to-GDP ratio (A.48):
[= Ss" tusun [R'S” (rf +87?°) + (R*S?” -1) (qi +m
H=C,1,X
Net exports-to-GDP ratio (A.49):
naj =sx(a+qGy +2) -—su (ata + mz) (sx su) (
Law of motion of net foreign assets-to-GDP ratio (A.50):
bY, = Aged + R*S” (nal — 17") + BY (rp +57") +...
— 4) ]-
t  &
Ape BY (4-1 — Ye Tm — 2 ta — Ga tT
where
Rs
Il* ZZ ©
AB* =
89
(C.35)
(C.36)
(C.37)
(C.38)
(C.39)

Real GDP (A.51):
Ye = S04 + $1t4 + SGH + SxT_ — SMM.
Relative GDP deflator (A.52):
“= sade +siqi +sx (at+aG@)-—su (ata )-
GDP deflator inflation (A.53):
YC y Y
T, =T™ +O — G-1-
C.5 Rest of the World
ROW output (A.54):
We = Py-Yater
Relative foreign-currency price of imports (A.55):
M* M* Qu’
% = Pom*hitée -
ROW inflation (A.56):
c* c* mo
Ty = PyotM 1 +e, -
International investors’ risk aversion (A.57):
*
* *
Up = Py Up Ey.
ROW interest rate (A.58):
x * R*
T, = Prep t+ -
C.6 Shocks - AR(1) Processes
e Household preference:
C _ C C
Zp = Poy at ef -
90
(C.40)
(C.41)
(C.42)
(C.43)
(C.44)
(C.45)
(C.46)
(C.47)
(C.48)

Real exchange rate:
Q_ Q Q
a = Port1 +e.
Country risk premium:
Transitory technology:
D_ D D
Zp = Ppo%_1 + Ef -
Permanent technology (trend growth rate):
Z_ Z Zz
Zp = Pz%y_1 Ft &,-
Investment technology:
I ol I
2 = Prat Ep.
Import demand:
M _ M M
Ze = Puy1t €, -
Export demand:
M* _ M* Eo
2 = Pur % 1 + Et
Wage markup:
Ww _ w Ww
2 = Pwrtrit et:
Price Markup:
P_ P P
2 = Pp%1t &-
Administered Prices:
A A A
= Parirt &-
Export price markup:
2 = Ppx%_4 + &
91
(C.49)
(C.50)
(C.51)
(C.52)
(C.53)
(C.54)
(C.55)
(C.56)
(C.57)
(C.58)
(C.59)

e Monetary policy:
x“ = PR + ef, (C.60)
where we set pp = 0.
e Fiscal policy (government consumption):
4 = patter, (C.61)
where we set pg = 0.

Table 1. Description of the data series used in the estimation
Description Source® Treatment?
Domestic Observable Variables
Y; GDP - volume (seasonally adjusted - s.a.) BGE fld
Ct Households’ consumption - volume (s.a.) BGE fld
I; nvestment: Gross formation of fixed capital - vol. (s.a.) BGE fld
Gi Government consumption - volume (s.a) BGE fld
Xt Exports of goods and services - volume (s.a.) BGE fld
M mports of goods and services - volume (s.a.) BGE fld
Ni umber of employed people (s.a.) © BGE fld
W, Real wage ("usual compensation" - s.a.) © BGE fld
ne CPI Inflation: IPCA (s.a. - % per quarter) BGE dam
Tl, CPI Inflation Target (% per quarter) BCB dam
A Administered price inflation (s.a. - % per quarter) BCB dam
ara Free price inflation (s.a. - % per quarter) BCB dam
Ix Export price inflation (s.a. - % per quarter) Funcex dm
Ry ominal interest rate - Selic (% per quarter) BCB dam
Se Primary surplus-to-GDP ratio - public sector (12 months) BCB dm
St Primary surplus target-to-GDP ratio - pub. sec. (12 mon.) BCB dm
Q: Real effective exchange rate BCB pd
SB . Country risk premium: EMBI Brazil (% per quarter) J.P.Morgan dm
Foreign Observable Variables
Y; World imports - volume (s.a.) CPB fld
Q; "| Relative price of imports (Brazil’s import prices/US CPI) Funcex It
Il; World inflation - US CPI AUCLS (% per quarter) Fed St. Louis | dm
Ve Foreign investors’ risk aversion - VIX CBOE dm
R; World nominal interest rate - Fed Funds rate (% p.q.) Fed St. Louis | dm
* Acronyms: IBGE - Brazilian Institute of Geography and Statistics; BCB - Central Bank of Brazil;
CPB - CPB Netherlands Bureau for |
Economic Policy Analysis; Funcex: Trade Studies Center Foundation;
CBOE - Chicago Board Options Exchange.
© Notation: fld: first log difference; dm: difference from the sample mean; dam: difference from the
adjusted mean (sample from 2005 onwards); pd: percentage deviation from the mean; It: linear trend
© Due to a methodology change in the employment and wage series in 2002, two time series were
combined: the current one, which started in March 2002, and the one that was discontinued that time. We
applied the growth rate of the discontinued series to obtain values for 1999Q3-2002Q1.

Table 2. Calibrated parameters
Symbol | Description Value
Shares
SC Households’ consumption-to-GDP ratio 0.62
SG Government consumption-to-GDP ratio 0.20
ST nvestment-to-GDP ratio 0.17
SX Exports-to-GDP ratio 0.13
SM mports-to-GDP ratio 0.12
T Average aggregate tax rate 0.35
Wo Share of rule-of-thumb households’ consumption in total consumption 0.40
Preference and Technology Parameters
B Time discount factor 0.989
n nverse of the elasticity of labor supply 1.00
Z4 Gross growth rate - BGP 1.009
ew Eos: differentiated labor 3
bh EoS: intermediate goods - consumption goods sector 11
ef EoS: intermediate goods - investment goods sector 11
eb EoS: intermediate goods - government goods sector 11
cb EoS: intermediate goods - export goods sector 11
€u EoS: intermediate goods - imported goods 11
a Cobb-Douglas production function - capital income share in GDP 0.448
QNn Share of production labor in total labor 0.8
() Depreciation rate of capital 0.015
we Weight of domestic input cost in the marginal cost of consumption goods 0.8418
w P Weight of domestic input cost in the marginal cost of investment goods 0.79
we Weight of domestic input cost in the marginal cost of gov. cons. goods 1.00
we Weight of domestic input cost in the marginal cost of exported goods 0.9
Shares of Imports that are Externally Financed
Lo Consumption goods sector 0.5
ly nvestment goods sector 0.5
ux Export goods sector 0.5

Table 2. Calibrated parameters (cont.)
Symbol | Description Value
Administered Prices
WA Weight of administered prices in CPI inflation 0.3
XA Adjustment factor of administered and free prices 0.8
Steady-State Parameters in the Law of Motion of Government and External Debts
BY Net foreign assets-to-GDP ratio (quarterly GDP) -0.68
BY Net government debt-to-GDP ratio (quarterly GDP) 2.00
AF B Adjustment factor in the law of motion of external debt 0.0397
AF pz Adjustment factor in the law of motion of domestic debt 0.53
ie Inflation target (quarterly gross rate) 1.011
R Domestic nominal interest rate (quarterly gross rate) 1.0314
II* World inflation (quarterly gross rate) 1.0064
R* World nominal interest rate (quarterly gross rate) 1.0074
SB Country risk premium (quarterly gross rate) 1.014

Table 3. Estimated parameters
Description Prior Distribution Posterior Distribution
Distribution | Mean | SD | Mean | Conf. Interval
Preference Parameters
K Habit persistence beta 0.85 0.05 0.74 0.65 0.84
oO nverse of intertemporal EoS Normal 1.30 0.05 1.30 1.22 1.38
vy Risk premium: investors’ aversion coef. Inv-gamma 0.05 0.15 0.03 0.02 0.04
YR Risk premium: NFA coef. Inv-gamma 0.05 0.15 0.02 0.01 0.03
Technology Parameters
EC EoS domestic imported inputs - cons. Gamma 0 0.5 1.09 0.64 1.55
€] EoS domestic imported inputs - invest. Gamma 0 0.5 0.83 0.18 1.47
€xX EoS domestic imported inputs - exports Gamma 1.0 0.5 0.95 0.23 1.63
€* EoS Brazil’s exports - ROW inputs Gamma 1.0 0.5 0.66 0.36 0.95
ye Adjustment cost in foreign imports Gamma 4.0 1.5 1.99 0.83 3.13
vr Adjustment cost of investment Gamma 4.0 1.5 3.42 1.30 5.38
ed Imports adjust. cost - consumption Gamma 4.0 1.5 0.76 0.44 1.09
oy Imports adjust. cost - investment Gamma 4.0 1.5 1.97 0.86 3.07
oy Imports adjust. cost - exports Gamma 4.0 1.5 3.12 128 4.88
Nominal Rigidity Parameters
Op Calvo - freely-set price Beta 0.65 0.1 0.74 0.68 0.81
Te: Calvo - government goods price Beta 0.65 0.1 0.47 0.32 0.62
Oy Calvo - investment goods price Beta 0.65 0.1 0.65 0.48 0.83
Ox Calvo - exports price Beta 0.65 0.1 0.77 0.68 0.86
Our Calvo - imports price Beta 0.65 0. 0.64 0.52 0.75
Ow Calvo parameter for wages Beta 0.75 0.1 0.75 0.66 0.84
WF Freely-set price indexation Beta 0.65 0.2 0.33 0.08 0.57
WG Government goods indexation Beta 0.65 0.2 0.49 0.14 0.82
WM mport price indexation Beta 0.65 0.2 0.65 0.35 0.97
Wy nvestment price indexation Beta 0.65 0.2 0.55 0.22 0.90
Wx Export price indexation Beta 0.65 0.2 0.35 0.08 0.60
Ww Wage indexation Beta 0.65 0.15 0.49 0.31 0.69

Table 3. Estimated parameters (cont.)
Distribution | Mean | SD | Mean | Conf. Interval
Administered Price Rule Parameters
vi Exchange rate coefficient Beta 0.05 0.03 0.05 0.01 0.09
v4 Marginal cost coefficient Beta 0.2 0.05 0.20 0.12 0.27
Policy Parameters - Taylor rule
YR Interest rate smoothing Beta 0.60 0.15 0.79 0.74 0.85
Yn Inflation coefficient ormal 2.0 0.35 2.43 1.98 2.89
Vy Output gap coefficient Gamma 0.25 0.1 0.16 0.06 0.25
Policy Parameters - Fiscal rule
dg Primary surplus reaction coef. Beta 0.4 0.05 0.49 0.42 0.56
og Primary surplus target coefficient Normal 0.35 0.05 0.41 0.34 0.49
op Government debt coefficient Inv-Gamma 0.05 0.15 0.02 0.01 0.02
Autoregressive Shocks
PB Domestic risk premium Beta 0.5 0.25 0.85 0.75 0.99
Pr nvestment adjustment cost Beta 0.5 0.25 0.33 0.05 0.56
Po Household preference Beta 0.5 0.25 0.13 0.00 0.27
Pu mport adjustment cost Beta 0.5 0.25 0.60 0.44 0.76
PA Administered prices Beta 0.5 0.25 0.37 0.19 0.56
Pp Price markup Beta 0.5 0.25 0.17 0.00 0.32
Tg nflation target Beta 0.5 0.25 0.84 0.70 0.99
Pw Wage markup Beta 0.5 0.25 0.09 0.00 0.18
Pp Transitory technology Beta 0.5 0.25 0.91 0.84 0.99
Pz Permanent technology Beta 0.5 0.25 0.25 0.01 0.46
Pa UIP Beta 0.5 0.25 0.94 0.89 0.99
Pp Country risk premium Beta 0.5 0.25 0.73 0.56 0.91
Pr Tax rate Beta 0.5 0.25 0.80 0.65 0.96
ps Primary surplus Beta 0.5 0.25 0.76 0.66 0.87
Pp Foreign price markup Beta 0.5 0.25 0.30 0.02 0.55
Pr Foreign inflation Beta 0.5 0.25 0.13 0.00 0.25
PR World nominal interest rate Beta 0.5 0.25 0.90 0.84 0.96
Py World demand Beta 0.5 0.25 0.93 0.86 0.99
Pagom* Import relative price Beta 0.5 0.25 0.88 0.80 0.97
Py Foreign investors’s risk aversion Beta 0.5 0.25 0.79 0.60 1.0
Pu World import demand Beta 0.5 0.25 0.13 0.00 0.25
Prest Inventory changes ormal 0.0 0.2 0.38 0.18 0.58

Table 3. Estimated parameters (cont.)
Distribution | Mean | SD | Mean | Conf. Interval
Exogenous Shocks
EB Domestic risk premium shock Inv-gamma_ 1.0 inf 0.57 0.29 0.85
Ey nvestment adjustment shock Inv-gamma 1.0 inf 3.54 1.81 5.30
EC Household preference shock Inv-gamma 1.0 inf 8.80 4.76 12.80
EM mport adjustment cost shock Inv-gamma 1.0 inf 9.01 6.54 11.32
EA Administered shock Inv-gamma_ 1.0 inf 1.40 1.15 1.64
Ep Price markup shock Inv-gamma_ 1.0 inf 0.79 0.57 1.00
Tle nflation target shock Inv-gamma 1.0 inf 0.14 0.12 0.16
Ew Wage markup shock Inv-gamma 1.0 inf 1.38 1.09 =: 1.68
Ep Transitory technology shock Inv-gamma 1.0 inf 1.18 0.93 1.33
EZ Permanent technology shock Inv-gamma 1.0 inf 0.17 0.14 0.20
EQ UIP. shock Inv-gamma 1.0 inf 0.80 0.41 1.18
E Bx Country risk premium shock Inv-gamma 1.0 inf 0.38 0.31 0.45
EG Government consumption shock Inv-gamma 1.0 inf 1.73 1.41 2.03
Ep Tax rate shock Inv-gamma 1.0 inf 0.48 0.40 0.56
EG Primary surplus target shock Inv-gamma 1.0 inf 0.29 0.24 0.34
ER onetary policy shock Inv-gamma 1.0 inf 0.32 0.25 0.38
E px Foreign price markup shock Inv-gamma_ 1.0 inf 3.89 2.67 5,08
eqy* Foreign inflation shock Inv-gamma 1.0 inf 0.85 0.70 = 1.00
ER* Foreign interest rate shock Inv-gamma 1.0 inf 0.19 0.15 0.22
Ey* World demand shock Inv-gamma 1.0 inf 2.87 2.38 3.35
Egnm* mports relative price shock Inv-gamma_ 1.0 inf 1.85 1.53 2.16
Evy« Foreign investors’s risk aversion shock Inv-gamma 1.0 inf 6.54 5.43 7.62
EM* World import demand shock Inv-gamma 1.0 inf 18.73 11.19 26.29
ETest nventories changes shock Inv-gamma_ 1.0 inf 0.69 0.57 0.81
Measurement Errors
ee GDP growth Inv-gamma 0.25 inf 0.08 0.06 0.11
ENG CPI Inflation Inv-gamma_ (0.25 inf 0.12 0.10 0.14

Table 4. Moment conditions
Variable Standard Deviation
Empirical Model-Implied
Domestic Observable Variables
Ayes GDP (quarter-on-quarter growth) 1.1914 2.8305
Aces Households’ consumption (q-o-q growth) 1.1931 2.5244
Aives nvestment (q-o-q growth) 4.2804 4.3137
Ag? bs Government consumption (q-o-q growth) 1.4773 5.1032
Ax9?s Exports of goods and services (q-o-q growth) 6.3540 6.9336
Am?s mports of goods and services (q-o-q growth) 5.7670 5.6441
Ans umber of employed people (q-o-q growth) 0.6323 4.4378
Aw??s | Real wage (q-o-q growth) 1.7699 1.9060
ne? CPI inflation (% per quarter) 1.0037 1.3403
Il, CPI inflation target. (% per quarter) 0.1428 0.2560
4 Administered price inflation (% per quarter) 1.6328 1.8093
ny Free price inflation (% per quarter) 0.9783 1.5016
Ix Export price inflation (% per quarter) 4.4661 5.099
R, ominal interest rate - Selic (% per quarter) 1.0659 1.2992
S? Primary surplus-to-GDP ratio (quarterly GDP) 0.7917 1.0817
SY Primary surplus target-to-GDP ratio (quarterly GDP) 0.6055 1.2647
Q: Real effective exchange rate (% per quarter) 19.9655 19.2850
Sp Country risk premium: EMBI Brazil (% per quarter) 1.0026 1.0515
Lest nventory investment (implied contribution to GDP) 0.7746 0.7499
Foreign Observable Variables
Ay; | World imports (q-o-q growth) 3.0082 2.9332
Qi Relative price of imports 4.3027 3.8927
Il; World inflation - US (% per quarter) 0.8361 0.8612
Vi Foreign investors’ risk aversion - VIX 9.0339 10.5997
R; World nominal interest rate - Fed Funds (% per quarter) | 0.5180 0.4284

Table 5. Forecast Error Variance Decomposition
Real GDP Growth CPI Inflation
Forecast Horizon
Shock lqtr 4qtr 8qtr Asympt. | lqtr 4qtr 8qtr Asympt.
Administered prices shock 0.39 61 0.96 1.06 23.58 17.56 12.22 11.18
Domestic risk premium shock 4.60 3.06 8.94 9.78 4.52 11.63 17.19 16.79
Country risk premium shock 0.01 0.03 0.05 0.07 0.06 O17 0.20 0.18
Household preference shock 17.29 1.52 12.93 11.85 1.50 1.97 1.64 1.53
Transitory technology shock 0.22 0.47 9.92 10.55 9.87 14.92 16.14 17.73
Government consumption shock 7.87 3.87 4.37 3.98 0.18 0.14 0.09 0.08
Investment shock 7.75 9.85 7.02 6.67 0.54 0.74 0.58 0.63
Import demand shock 15.29 9.47 5.09 14.33 3.98 4.37 3.03 2.73
Export demand shock 26.12 15.34 16.23 14.78 0.59 0.36 0.24 0.31
Price markup shock 0.85 0.61 0.63 0.60 37.99 14.54 844 7.33
Export price markup shock 0.01 040 0.49 0.66 0.04 0.15 0.24 0.35
Real exchange rate shock 0.27 0.34 0.97 2.26 1.19 5.01 9.63 12.38
Monetary policy shock 1.06 2.85 1.88 1.94 0.72 1.74 2.27 2.07
Wage markup shock 0.38 6.58 8.22 9.90 14.54 25.75 26.09 23.30
Permanent technology shock 0.06 060 0.39 0.37 0.00 0.00 0.02 0.07
Tax rate shock 9.98 640 6.24 5.75 0.36 0.36 0.26 0.25
Primary surplus target shock 0.64 0.80 0.82 0.80 0.07 O12 O12 0.12
Inflation target shock 0.20 0.70 0.61 0.72 0.03 0.03 0.75 ~~ 1.50
Foreign inflation shock 0.00 0.01 0.01 0.01 0.00 0.00 0.01 0.03
Import price in USD shock 0.17 0.13 O10 0.18 0.038 0.13 0.26 0.34
Foreign interest rate shock 0.00 0.00 0.03 0.07 0.06 0.20 0.34 0.36
World income shock 6.83 5.36 4.05 3.70 0.11 0.03 O11 0.63
Foreign investor risk aversion shock | 0.00 0.01 0.02 0.02 0.02 0.07 0.10 0.09

Figure 1. Data series (after transformation)
GDP
(growth rate - % p.q.)
OF
0 4
D+
-4 [, J
2000 2005 2010
Government Consumption
(growth rate - % p.q.)
4 ET T
2 L
0 1 I
2+
Gb n 14
2000 2005 2010
Exports
(growth rate - % p.q.)
2005 2010
Employment
(growth rate - % p.q.)
2010
2005
101
re
AONog
Private Consumption
(growth rate - % p.q.)
2005 2010
Investment - GFFC
(growth rate - % p.q.)
2000
2005 2010
Imports
(growth rate - % p.q.)
2000 2005 2010
Real Wages
(growth rate - % p.q.)
of
(0) L
-2
-4 f+
-6 +
2010
2005

Figure 1: Data series (after transformation) - cont.
CPI Inflation Administered Price Inflation
(% p.q.) (% p.q.)
4k
2 L
0
2000 2005 2010 2000 2005 2010
Free Price inflation Export Price Inflation
(% p.q.) (% p.q.)
T 10 FT T
2000 2005 2010 2000 2005 2010
CPI Inflation Target Nominal Interest Rate
(% p.q.) (% p.q.)
0.4\ | 3 |
0.2 ra
OPN fee Ob A
2000 2005 2010 2000 2005 2010
Public Sector Primary Surplus Public Sector Primary Surplus Target
(% of GDP) (% of GDP)
2000 2005 2010 2000 2005 2010

Figure 1: Data series (after transformation) - cont.
Real Effective Exchange Rate Country Risk Premium
(% deviation) (p.p.)
40} | | 3] |
20} ral
-20 ' -1 |
2000 2005 2000 2005
World Imports
(growth rate - % p.q.) Relative Import Prices
2000 2005 2010 2000 2005 2010
VIX Foreign (US) Interest Rate
(% p.q.)
1 FT T
0.5F
(0) Po. Qe Lf ee Qe eee
2000 2005 2010 2000 2005
Foreign (US) Inflation
(% p.q.)
ns
2+
-4 tL, 4
2000 2005 2010

Figure 2. Priors and posteriors of the parameters
~ *
kK 0 Yy
8 8
40
6 6
4 4 20
2 2
0 0 0
0.4 0.6 0.8 1.2 1.6 0.1 0.2
* € €
os I Cc
1.5,
80 1
60 1
40 0.5
20 oF
0 0 0 ae
€x €Me yl
F
0.6
2
0.4
0.5
1
0.2
a ot ue
2 0.4 0.6
0.4
1 0.2
0.2
0 OO 0 0

Figure 2. Priors and posteriors of the parameters (continued)
Op 9¢ Oy
0.4 0.6 0.8 1 0 0.5 0.2 0.4 06 0.8 1
Ox oy Ow
0.4 0.6 0.8 1 0 0.5 1 0.4 0.6 0.8 1
OP WG Yu
0 0.5 1 0 0.5 1 0 0.5 1
wx wy wy
0 0.5 1 0 0.5 1 0 0.5 1

10
Figure 2. Priors and posteriors of the parameters (continued)
10
v4 v4 o
8 0.3
8 0.2
4
a4
5 0
0 )
0 0.1 0.2 0.2 0.4 5 10
YR Vn wi
1.5)
6
1
4
0.5 2
wane ; ;
0.2 04 06 08 1 2 4 0.2 0.4 0.6
"8 Vg 1B
8 10d
6
4 50
2
0 ) :
0.3 04 05 06 0.7 0.2 0.4 0.6 0 0.4 0.2

Figure 3. Impulse Responses to a Monetary Policy Shock
Real GDP Private Consumption Government Consumption
0 0.5 0
-0.2 0 ——— -0.5
-0.4 -0.5 -1
Exports Imports Net exports (% of GDP)
0.1 0.5 0.1
-0.1 -0.5 -0.1
4-Q CPI Inflation 4-Q Free Inflation 4-Q Adm Inflation
0.5 0.5 0 ee
-0.5 -0.5 -0.4
Real Wage Employment Nom. Interest Rate (annualized)
0.2 0 2
~ 1
0 PSST Tr -0.5 \
@) KK — —
-0.2 -1 -1
107
Investment
0.5
ok —L—
-0.5
|
0 4 8 12
Real Exchange Rate
{
|
-2
0 4 8 12
4-Q Import Goods Inflation
0.5
0 I~ aa
-0.5
|
0 4 8 12
Mon. Policy Shock (annualized)
\

Figure 4. Impulse Responses to a Wage Markup Shock
Real GDP
0 4 8 12
Exports
0 4 8 12
4-Q CPI Inflation
0 4 8 12
Real Wage
0 4 8 12
Private Consumption Government Consumption Investment
1 1 0
-0.5 -2 -3
Imports Net exports (% of GDP) Real Exchange Rate
2 0.2 0.5
{
a, en
0 ee —
-1 -0.2 -0.5
4-Q Free Inflation 4-Q Adm Inflation 4-Q Import Goods Inflation
2 1 1
0----- >= 0-—----- = ORF --- 7-H
-1 -0.5 -0.5
Employment Nom. Interest Rate (annualized) Wage Markup Shock
0.5 1 2
o-“L---- 27s 0.5 o-_ ae 1}
-0.5 o.-----— 0
-1 -0.5 “|

Figure 5. Impulse Responses to an Investment Shock
Real GDP
0.4
0.2 ae
(@) fe
-0.2
0 4 8 12
Exports
0.1
-0.1
0 4 8 12
4-Q CPI Inflation
0.1
(0) Zo.
-0.1
0 4 8 12
Real Wage
0.05
|
-0.05
0 4 8 12
Private Consumption
0.2
(@) eee
-0.2
0 4 8 12
Imports
0.5
-0.5
0 4 8 12
4-Q Free Inflation
0.2
o-oo,
-0.2
0 4 8 12
Employment
0.5
0 > ee
-0.5
0 4 8 12
109
Government Consumption
0.5
0 4 8
Net exports (% of GDP)
12
0 4 8
-0.1
0 4 8 12
Nom. Interest Rate (annualized)
0.2
Investment
sb
0
0.2
4 8
Real Exchange Rate
st
12
4
8 12
4-Q Import Goods Inflation
) - 40 Ss
-0.2
0
4 8
Investment Shock
12
A

1.5
0.5
-0.5
-1.5
Figure 6: Impulse Responses to a Real Exchange Rate Shock
Real GDP
4 8 12
Exports
4 8 12
4-Q CPI Inflation
4 8 12
Real Wage
4 8 12
Private Consumption
0
-1
0 4 8 12
Imports
0
5 wu
-10
0 4 8 12
4-Q Free Inflation
1.5
1
0
0 4 8 12
Employment
0.5
Or — aS
-0.5
0 4 8 12
110
Government Consumption
1
4 8
Net exports (% of GDP)
y
A
4-Q Adm Inflation
12
0.5
0
0 4 8 12
Nom. Interest Rate (annualized)
1.5
1
0.5
0
Investment
0
-10
0 4 8 12
Real Exchange Rate
20
10 ee
0 fe
-10
0 4 8 12
4-Q Import Goods Inflation
10
5
Or ——_— — — << =
-5
0 4 8 12
RER Shock
2
1 a
(0) — —
0 4 8 12

Figure 7: Impulse Responses to a Government Consumption Shock
Real GDP
0.5
0 —. —~s_ a
-0.5
0 4 8 12
Exports
0.04
0.02
0 — a
-0.02
0 4 8 12
4-Q CPI Inflation
0.1
0 [a
-0.1
0 4 8 12
Real Wage
0.02
-0.02
0 4 8 12
Private Consumption
0.5
0 I
-0.5
0 4 8
Imports
0.5
-0.5
0 4 8
4-Q Free Inflation
0.1
Aha,
-0.1
0 4 8 12
Employment
{
0.5} \
0 — —
-0.5
0 4 8 12
111
Government Consumption
0.1 -
0 4 8 12
Nom. Interest Rate (annualized)
0.1
Investment
0.2
4 8 12
Real Exchange Rate
a
4 8 12
-Q Import Goods Inflation
=
0.1
0 4 8 12
Government Consumption Shock
A

Figure 8. Impulse Responses to a Permanent Technology Shock
Real GDP Private Consumption
1.5 2
0.5 o-~-------
0 = — -1
Exports Imports
1.5 4
0.5 O-7-------
0 = — 2
4-Q CPI Inflation 4-Q Free Inflation
0.5 0.5
-0.5 -0.5
Real Wage Employment
2 0.5
0 -0.5
“1 -1
112
3
2
1
Government Consumption
ae
0 —
0 4 8 12
Net exports (% of GDP)
0.2
\e----
-0.2
0 4 8 12
4-Q Adm Inflation
0.5
-0.5
0 4 8 12
Nom. Interest Rate (annualized)
0.5
Pe
-0.5
0 4 8 12
Investment
A
° | ——
(0) — —
0 4 8 12
Real Exchange Rate
0
-1 a
-2
0 4 8 12
4-Q Import Goods Inflation
{
0 Sf
4
-2
0 4 8 12
Permanent Technolog y Shock
2
A

Figure 9. Root Mean Squared Errors of Forecasts
(a) CPI Inflation (four quarter) (b) Real GDP Growth (year-on-year)
Samba
Last value
— —Average
BVAR
(c) Nominal Interest Rate (quarterly)
1.8
1.6 _—
1.4 a
1.2 -
0.8
0.6
0.4
0.2

Figure 10. Mean Forecast and Forecast Intervals for Two Episodes
(a) Forecast with data up to 2004Q4
Selic rate (%p-y.)
‘
‘ ' 4
----- pee------4e----- eb -ee
Hi '

Table A.1 - Forecast Error Variance Decomposition - 1 quarter ahead
. Free Admin.
Private Governm. Real . . Interest
Shock Investm. Exports Imports Employm. Price Price
Consump. Consump. Wage . . Rate
Inflation Inflation
115
Administered prices shock 1.43 0.07 0.08 0.00 0.20 0.26 6.65 0.10 99.99 2.40
Domestic risk premium shock 4.74 0.75 6.98 0.01 1.19 3.10 0.02 5.91 0.00 9.87
Country risk premium shock 0.00 0.00 0.08 0.00 0.22 0.01 0.01 0.08 0.00 0.12
Household preference shock 48.79 3.44 1.44 0.00 8.81 11.40 0.36 1.97 0.00 2.40
Transitory technology shock 6.67 0.03 2.60 0.01 7.02 21.62 1.80 12.90 0.00 6.88
Government consump. shock 2.33 28.19 0.11 0.00 0.89 5.42 0.01 0.24 0.00 0.43
Investment shock 1.79 1.55 66.55 0.00 5.06 5.05 0.03 0.71 0.00 0.97
Import demand shock 9.83 4.47 5.90 0.07 47.43 22.08 0.28 5.21 0.00 2.75
Export demand shock 7.92 5.62 0.13 75.87 9.63 17.43 0.00 0.78 0.00 1.10
Price markup shock 1.89 0.23 0.05 0.00 0.59 0.55 8.87 49.66 0.01 0.15
Export price markup shock 0.07 1.34 0.38 3.17 0.04 0.00 0.04 0.05 0.00 0.10
Real exchange rate shock 0.73 0.04 8.99 0.23 6.97 0.10 0.70 1.55 0.00 3.94
Monetary policy shock 1.07 0.18 1.76 0.00 0.31 0.71 0.00 0.94 0.00 53.34
Wage markup shock 7.98 0.07 3.48 0.01 5.27 0.17 80.05 19.01 0.00 12.09
Permanent technology shock 0.60 0.07 0.03 0.00 0.13 0.03 1.04 0.00 0.00 0.00
Tax rate shock 1.27 48.96 0.48 0.00 0.76 6.92 0.03 0.47 0.00 0.74
Primary surplus target shock 0.15 3.04 0.15 0.00 0.05 0.44 0.01 0.10 0.00 0.13
Inflation target shock 0.26 0.03 0.28 0.00 0.09 0.13 0.01 0.04 0.00 2.18
Import price in USD shock 0.11 0.44 0.21 0.00 0.53 0. 0.03 0.04 0.00 0.07
Foreign interest rate shock 0.01 0.00 0.25 0.01 0.27 0.0 0.02 0.07 0.00 0.15
World income shock 2.35 1.43 0.00 20.50 4.39 4.4 0.02 0.14 0.00 0.18
Foreign risk aversion shock 0.00 0.00 0.04 0.00 0.09 0.00 0.01 0.03 0.00 0.05

Table A.2 - Forecast Error Variance Decomposition - 4 quarters ahead
Private Governm. Real . . Interest
Shock Investm. Exports Imports Employm. Price Price
Consump. Consump. Wage . . Rate
Inflation Inflation
116
Administered prices shock 4.95 0.40 0.06 0.04 0.08 1.41 6.14 0.46 91.11 2.82
Domestic risk premium shock 14.58 1.83 4.06 0.05 1.01 10.78 0.17 14.15 1.09 28.27
Country risk premium shock 0.00 0.01 0.22 0.04 0.57 0.05 0.03 0.18 0.04 0.24
Household preference shock 42.22 2.06 3.31 0.02 3.61 9.68 0.45 2.28 0.27 3.25
Transitory technology shock 3.62 7.32 7.80 0.22 2.65 15.79 2.79 17.79 1.65 10.30
Government consump. shock 1.10 15.41 0.18 0.00 0.22 3.40 0.00 0.15 0.03 0.33
Investment shock 1.56 2.04 29.12 0.00 3.20 7.11 0.01 0.85 0.11 1.77
Import demand shock 6.45 3.70 12.33 1.21 27.60 18.29 0.12 5.17 0.55 2.39
Export demand shock 4.70 3.25 0.13 50.22 5.09 12.85 0.12 0.41 0.06 0.79
Price markup shock 1.49 0.17 0.11 0.00 0.24 0.49 2.97 18.92 0.98 0.05
Export price markup shock 0.09 2.97 1.09 21.77 0.13 0.45 0.18 0.18 0.02 0.41
Real exchange rate shock 3.56 0.09 26.19 4.40 38.24 0.15 3.58 5.24 1.09 11.37
Monetary policy shock 2.89 0.57 1.06 0.01 0.28 2.33 0.02 2.08 0.18 15.60
Wage markup shock 7.49 7.55 11.14 0.22 4.43 5.98 82.16 31.02 2.68 18.04
Permanent technology shock 0.60 0.05 0.02 0.01 0.04 0.02 0.39 0.00 0.00 0.00
Tax rate shock 0.64 45.00 1.00 0.02 0.26 5.71 0.02 0.42 0.05 0.87
Primary surplus target shock 0.15 5.88 0.35 0.00 0.03 0.72 0.00 0.14 0.01 0.29
Inflation target shock 1.17 0.09 0.17 0.00 0.19 0.55 0.12 0.03 0.01 2.37
Foreign inflation shock 0.05 0.02 0.05 0.08 0.19 0.01 0.02 0.00 0.00 0.01
Import price in USD shock 0.22 0.44 0.70 0.00 2.55 0.07 0.16 0.18 0.01 0.24
Foreign interest rate shock 0.07 0.00 0.72 0.10 1.19 0.01 0.10 0.22 0.04 0.41
World income shock 2.37 1.14 0.05 21.57 7.91 4.11 0.43 0.05 0.00 0.07
Foreign risk aversion shock 0.00 0.00 0.13 0.02 0.28 0.02 0.02 0.08 0.02 0.12

Table A.3 - Forecast Error Variance Decomposition - 8 quarters ahead
Shock
Private
Consump.
Governm.
Consump.
Investm.
Exports
Imports
Employm.
Real
Wage
Free Admin.
Price Price
Inflation Inflation
Interest
Rate
Administered prices shock
Domestic risk premium shock
Country risk premium shock
Household preference shock
Transitory technology shock
Government consump. shock
Investment shock
Import demand shock
Export demand shock
Price markup shock
Export price markup shock
Real exchange rate shock
Monetary policy shock
Wage markup shock
Permanent technology shock
Tax rate shock
Primary surplus target shock
Inflation target shock
Foreign inflation shock
Import price in USD shock
Foreign interest rate shock
World income shock
Foreign risk aversion shock
15.35
32.43
11.12
11.94
40.09
10.22
13.61
41.67
12.82
36.36
27.93
11.92
18.71
14.32
55.06
11.44
11.54
13.34
16.26
10.86
13.98
72.44
0.89 64.06 2.45
18.97 6.47 38.61
0.20 0.10 0.21
1.82 0.73 2.61
18.06 5.94 10.06
0.10 0.05 0.22
0.65 0.29 1.57
3.69 1.15 1.45
0.31 0.07 0.47
12.33 2.66 0.03
0.24 0.12 0.53
9.46 4.65 15.09
2.48 0.91 8.94
29.10 11.00 14.35
0.03 0.01 0.02
0.30 0.11 0.7
0.13 0.05 0.29
0.37 1.26 1.4
0.01 0.01 0.0
0.30 0.09 0.3
0.34 0.16 0.49
0.12 0.05 0.04
0.10 0.05 0.1

Table A.4 - Forecast Error Variance Decomposition - Asymptotic
Shock
Private
Consump.
Governm.
Consump.
Investm.
Exports
Imports
Employm.
Real
Wage
Free
Price
Inflation
Admin.
Price
Inflation
Interest
Rate
Administered prices shock
Domestic risk premium shock
Country risk premium shock
Household preference shock
Transitory technology shock
Government consump. shock
Investment shock
Import demand shock
Export demand shock
Price markup shock
Export price markup shock
Real exchange rate shock
Monetary policy shock
Wage markup shock
Permanent technology shock
Tax rate shock
Primary surplus target shock
Inflation target shock
Foreign inflation shock
Import price in USD shock
Foreign interest rate shock
World income shock
Foreign risk aversion shock
16.03
18.17
16.09
11.09
28.01
50.03
27.01
22.39
25.89
14.04
11.40
56.18
17.28
13.80
14.07
14.58
16.25
14.29
42.90
17.93
18.85
10.94
12.26
26.03
56.37
10.98
39.19
10.86
17.70
11.93

-0.2
-0.4
-0.2
-0.4
Figure Al. Impulse Responses to an Administered Price Shock
Real GDP Private Consumption
0
Ne oy
-0.5
“1
Exports Imports
es 0.5
0 | <a
-0.5
4-Q CPI Inflation 4-Q Free Inflation
0.5
7\__ »(-An l=
-0.5
Real Wage Employment
0 -
NEO
VS—osoooooe
-0.5
“1
119
Government Consumption Investment
0.4 0.5
0.2 EP_ 0--=s-s- -
0 — ~  -0.5
Net exports (% of GDP) Real Exchange Rate
0.04 0
0.02 > -0.5
ve eee
o- -- == = -
-0.02 -1.5
4-Q Adm Inflation 4-Q Import Goods Inflation
4 0.5
2
— 0 ee — —<—
0 —
-2 -0.5
Nom. Interest Rate (annualized) Adm Price Shock
0.4 1.5
1
0.2
0.5
0 — * 0

Figure A2. Impulse Responses to a Domestic Risk Premium Shock
1 1
-2 -2
Exports Imports Net exports (% of GDP)
2 0.5
a 0p tsa
-2
-4 -0.5
4-Q CPI Inflation 4-Q Free Inflation 4-Q Adm Inflation
2 2
ON °F SS
- SN -
-4 -4
Real Wage Employment Nom. Interest Rate (annualized)
2 0
-2 -4
-4 6
120
Investment
5
OL =
-5
0 4 8 12
Real Exchange Rate
5
O-  —
-5
-10
0 4 8 12
4-Q Import Goods Inflation
5
@) | Soe
-5
-10
0 4 8 12
Domestic Risk Premium Shock
2
—=
4
8 12

Figure A3. Impulse Responses to a Country Risk Premium Shock
0.5
ee
-0.5
Exports Imports
2
ie -2
-4
4-Q CPI Inflation 4-Q Free Inflation
1
0.5
———_ 0 La
-0.5
Real Wage Employment
0.5
en
-0.5
121
Government Consumption
0.5
OF SS ———
-0.5
0 4 8 12
Net exports (% of GDP)
0.5
—
@) ——_— —
-0.5
0 4 8 12
4-Q Adm Inflation
0.5
0 | 4
-0.5
0 4 8 12
Nom. Interest Rate (annualized)
{
0.5
oh. oS
-0.5
0 4 8 12
Investment
2
°/ SO
-2
-4
0 4 8 12
Real Exchange Rate
10
5
(0) Se
5
0 4 8 12
4-Q Import Goods Inflation
A
2
0 i
-2
0 4 8 12
Country Risk Premium Shock
1.5
1
0.5

Figure A4. Impulse Responses to a Household Preference Shock
Real GDP
0.2
OF _ — ——
-0.2
0 4 8 12
Exports
0.02
0.01
iS
-0.01
0 4 8 12
4-Q CPI Inflation
0.1
. Sarr
-0.1
0 4 8 12
Real Wage
0.02
-0.02
-0.04
0 4 8 12
Private Consumption Government Consumption Investment
0.2 0.2 0.2
0 [f 0 |Z 0.1 fo~
-0.2 -0.2 0 — *
Imports Net exports (% of GDP) Real Exchange Rate
0.2 0.04 0.05
0.02
0- -ses > a OF -— >So >
@) — _ —
-0.2 -0.02 -0.05
4-Q Free Inflation 4-Q Adm Inflation 4-Q Import Goods Inflation
0.1 0.02 0.05
@) fe eee ee
O- = - p=  —
0.02 ee
-0.1 -0.04 -0.05
Employment Nom. Interest Rate (annualized) Household Preference Shock
0.2 0 2
-0.02
0O--Z 1
VA -0.04 \
-0.2 -0.06 0

Figure A5. Impulse Responses to a Transitory Technology Shock
2 1 2
1 1
F22 \ Fe PZ
0-— ------ o-f-----—™—
5 “1 “|
Exports Imports Net exports (% of GDP)
1 1 0.2
0O+---s > ee
0.5 i
y .
4-Q CPI Inflation 4-Q Free Inflation 4-Q Adm Inflation
0 0 0
0.5 ee 0.5 \
-0.5
5 “1
-1.5 -1.5 -1
Real Wage Employment Nom. Interest Rate (annualized)
1 1 0
0- - ZF eo
0.5 -0.5
aan -1
123
Investment
3
2
_,
ou — —
0 4 8 12
Real Exchange Rate
{
0.5
a
@) i
-0.5
0 4 8 12
4-Q Import Goods Inflation
0.5
| Si
-0.5
-1
0 4 8 12
Transitory Technolog y Shock
1.5
1
0.5
0

Figure A6. Impulse Responses to an Import Demand Shock
Real GDP
4 8
4 8
Private Consumption
0 4 8 12
Imports
0 4 8 12
4-Q Free Inflation
0 4 8 12
Employment
0 4 8 12
124
Government Consumption
0.2
0 4 8
0 4 8
0 4 8 12
Nom. Interest Rate (annualized)
0.1
Investment
0.5
0 a
-0.5
0 4 8 12
Real Exchange Rate
0.4
0.2 ——
0 Le — "
0 4 8 12
4-Q Import Goods Inflation
0.2
0 i. ae
-0.2
0 4 8 12
Import Demand Shock
1.5
1
0.5
0
0 4 8 12

Figure A7. Impulse Responses to an Export Demand Shock
Real GDP
4 8
-0.02
0 4 8 12
Real Wage
0.02
0 _ ———
-0.02
0 4 8 12
Private Consumption Government Consumption Investment
0.05 0.1 0.05
0 | Qo 0 In OK- = - —
-0.05 -0.1 -0.05
Imports Net exports (% of GDP) Real Exchange Rate
0.1 0.05 0------7-
Vine. 0 LS 0.05 a
0 — ~ -0.05 -0.1
4-Q Free Inflation 4-Q Adm Inflation 4-Q Import Goods Inflation
0.02 0.01 0.1
-0.02 -0.01 -0.1
Employment Nom. Interest Rate (annualized) Exports Demand Shock
0.1 0.02 2
0 KO 0 [Sa {
-0.1 -0.02 0 \

Figure A8. Impulse Responses to a Price Markup Shock
Real GDP Private Consumption Government Consumption Investment
0.5 1 1
07S TSS
0- - == == Of - == O- ye -----
, a 4
-0.5 -1 -2
Exports Imports Net exports (% of GDP) Real Exchange Rate
0.5 0.1 0.5
0 [ = oO aS.
(a — o---= = 0
0.5 J a=
-1 -0.1 -0.5
4-Q CPI Inflation 4-Q Free Inflation 4-Q Adm Inflation 4-Q Import Goods Inflation
2 1 1
1 “A 0.5 Awe 0.5 AY
@) ae @) ——<— — — @) SS S| @) Se
-1 -0.5 -0.5
Real Wage Employment Nom. Interest Rate (annualized) Price Markup Shock
0.5 0.5 2
LL 0 | =
-0.5 \
-1 -0.5 0'-—

Figure A9. Impulse Responses to an Export Price Markup Shock
Real GDP
Private Consumption
Government Consumption
0.1 0.1 0.4
_ ee —™”
0S OF => - 7-H: 0.2 ~~
-0.1 -0.1 0- — *
Exports Imports Net exports (% of GDP)
0 - 0.5 0.2
0O-=------ Op — ee
|
-1.5 -0.5 -0.2
4-Q CPI Inflation 4-Q Free Inflation 4-Q Adm Inflation
0.05 0.05 0.02
0 fee ees
tl — i ———S
No 0.02
-0.05 -0.05 -0.04
Real Wage Employment Nom. Interest Rate (annualized)
0.1 0.1 0 j
OrN - 7S _
0.05 -0.05
lS -0.1
0- — *~ -0.2 -0.1
127
Investment
0.4
ou _ .
0 4 8 12
Real Exchange Rate
0.5
0 _
aE
-0.5
0 4 8 12
4-Q Import Goods Inflation
0.5
a
0.5
0 4 8 12
Export Price Markup Shock
2

Figure A10: Impulse Responses to a Tax Rate Shock
Real GDP
Private Consumption
0 4 8 12
4 8
-0.5
Real Wage Employment
4
2
+ a — — SS 0.5
—..~___ @) _-_ TS Tre SS
-2
12
128
Government Consumption
10
5 es
@) fe
5
0 4 8 12
Net exports (% of GDP)
0.2
@) —— ——
-0.2
0 4 8 12
4-Q Adm Inflation
0.5
oA ee An obs
0 4 8 12
Nom. Interest Rate (annualized)
1
0 —
Investment
0
-2
0 4 8 12
Real Exchange Rate
{
07
-1
-2
0 4 8 12
0.5
OF
-0.5
4-Q Import Goods Inflation
1
0
1.5
4 8 12
Tax Rate Shock
4 8 12

Figure All. Impulse Responses to a Primary Surplus Target Shock
2
{ /o™~
@) —
Exports Imports Net exports (% of GDP) Real Exchange Rate
0.5 0.5 0.1 0.5
@) ty --
0 L=_ OorK-—-— _ 0 — —_——
-0.5
-0.5 -1 -0.1 -0.5
4-Q CPI Inflation 4-Q Free Inflation 4-Q Adm Inflation 4-Q Import Goods Inflation
0.5 0.5 0.5 0.5
0 a 0 ae 0 [MS 0 > =
-0.5 -0.5 -0.5 -0.5
Real Wage Employment Nom. Interest Rate (annualized) Fiscal Target Shock
0.1 1 0.5 2
Ce O---s == OF ----~s >= 1
O--- = i ee Se
-1 -0.5 o----= =
-0.1 -2 4 “1

Figure A12: Impulse Responses to an Inflation Target Shock
130
Real GDP Private Consumption Government Consumption
4 3
2 2
LS = 0 |S 1 >
-2 0 — —
0 4 8 12 0 4 8 12 0) 4 8 12
Exports Imports Net exports (% of GDP)
4 0.5
[ Se *
@) —_——
-2 -0.5
0 4 8 12 0 4 8 12 0) 4 8 12
4-Q CPI Inflation 4-Q Free Inflation 4-Q Adm Inflation
4 5
2 a a
wh _ 0-—WC--- +
——— $$ os i i @) ————— i
-2 -5
0 4 8 12 0 4 8 12 0) 4 8 12
Real Wage Employment Nom. Interest Rate (annualized)
4 2
2 OF -af-- 7-H
0 | -2
-2 -4
0 4 8 12 0 4 8 12 0) 4 8 12
Investment
0 Se
0 4 8
Real Exchange Rate
12
op Aye - -
-5
0 4 8 12
4-Q Import Goods Inflation
2
0 | So —
-2
0 4 8 12
Inflation Target Shock
1.5
1
0.5 _
0 —
0 4 8 12

Figure A13. Impulse Responses to a Foreign Inflation Shock
1 1
0.5
4N 0.5
@) I ———
-0.5 0 — _
Exports Imports
5 6
A
0
2
5 0 — —
4-Q CPI Inflation 4-Q Free Inflation
0.5 0.5
-0.5 -0.5
Real Wage Employment
1 1
0.5
0 — — -0.5
131
0.5
0 4 8 12
Net exports (% of GDP)
0 4 8 12
4-Q Adm Inflation
-0.5 -10
0 4 8 12
Nom. Interest Rate (annualized)
5
 ——
20
Government Consumption Investment
1 4
@) eH — ———_—— —
2
“1
-2 0 —
0 4 8 12
Real Exchange Rate
——
0 4 8 12
4-Q Import Goods Inflation
0 4 8 12
Foreign Inflation Shock

Figure A1l4. Impulse Responses to an Import Relative Price Shock
0 0 0 0
VI 0.5} -2
-0.5 -1
“1 -4
-1 -1.5 -2 -6
Exports Imports Net exports (% of GDP) Real Exchange Rate
1 0 1 2
@) ee — — =——j—— —
=> 5 (e) HH —_—__—__— — —
4
-1 -10 -2 -2
4-Q CPI Inflation 4-Q Free Inflation 4-Q Adm Inflation
1 1 1
0.5 0.5
V owe -—---- == OhK—= - - -
0 -0.5 -0.5 5
Real Wage Employment Nom. Interest Rate (annualized) Import Price in USD Shock
0 0.5 1 15
0.5 NL 0+} -s==--- 08
4 0.5 P= 0 = 5 Sa
-1.5 -1 -0.5 0 — —

Figure A15. Impulse Responses to a Foreign Interest Rate Shock
0 0.5 0
-0.5 -4
1 | -6
Exports Imports Net exports (% of GDP) Real Exchange Rate
5 1 20
OF - --- sae 10
i 5 A ~~ 9+ --—- >=
-10 0. —— -10
4-Q CPI Inflation 4-Q Free Inflation 4-Q Adm Inflation 4-Q Import Goods Inflation
1 1 10
-0.5 -0.5 -5
Real Wage Employment Nom. Interest Rate (annualized) International Interest Rate Shock
0.5 1.5 1.5
0 Se
0.5 Vg 0.5
-0.5 o-—— — 0 — =

0.4
0.2
-0.1
0.2
-0.2
Figure A16. Impulse Responses to a World Income Shock
Real GDP
0 4 8 12
0 4 8 12
0.2
0.1
1.5
0.5
0.1
Private Consumption
0 4 8 12
0 4 8 12
Employment
134
Government Consumption
0.4
0 4 8 12
0 4 8 12
0 4 8 12
Nom. Interest Rate (annualized)
0.05
Investment
4 8 12
Real Exchange Rate
__
4 8 12
4-Q Import Goods Inflation
on
0
1.5
0.5
4 8 12
World Income Shock
~~
12
» |

Figure A17. Impulse Responses to Foreign Investors’ Risk Aversion Shock
0.02 0.1 0.05 0.5
1 = Saar
0-—== = > > = 0-——Ss TT 0-—Sa TTT:
-0.02
-0.04 -0.1 -0.05 -0.5
Exports Imports Net exports (% of GDP) Real Exchange Rate
0.2 0.5 0.05 1
0.5
Orr ---T- Oe Oe —___
0 — ———
-0.2 -0.5 -0.05 -0.5
4-Q CPI Inflation 4-Q Free Inflation 4-Q Adm Inflation 4-Q Import Goods Inflation
0.04 0.04 0.04 0.5
0.02 0.02 0.02
eee 0-~----- =: 0 ee
-0.02 -0.02 -0.02 -0.5
Real Wage Employment Nom. Interest Rate (annualized) Foreign Investor Risk Aversion Shock
0.1 0.02 0.05 1.5
a _ 1
-_ 0 0------ =>
0.5
-0.1 -0.02 -0.05 0

Banco Central do Brasil
Trabalhos para Discussao
Os Trabalhos para Discussdo do Banco Central do Brasil estado disponiveis para download no website
203
204
205
206
207
208
209
210
211
212
Working Paper Series
The Working Paper Series of the Central Bank of Brazil are available for download at
Hiato do Produto e PIB no Brasil: uma Andlise de Dados em
Tempo Real
Rafael Tiecher Cusinato, André Minella e Sabino da Silva Porto Junior
Fiscal and monetary policy interaction: a simulation based analysis
of a two-country New Keynesian DSGE model with heterogeneous
households
Marcos Valli and Fabia A. de Carvalho
Model selection, estimation and forecasting in VAR models with
short-run and long-run restrictions
George Athanasopoulos, Osmani Teixeira de Carvalho Guillén,
Jodo Victor Issler and Farshid Vahid
Fluctuation Dynamics in US interest rates and the role of monetary
policy
Daniel Oliveira Cajueiro and Benjamin M. Tabak
Brazilian Strategy for Managing the Risk of Foreign Exchange Rate
Exposure During a Crisis
Antonio Francisco A. Silva Jr.
Correlacao de default: uma investigacéo empirica de créditos de varejo
no Brasil
Antonio Carlos Magalhdes da Silva, Arnildo da Silva Correa, Jaqueline
Terra Moura Marins e Myrian Beatriz Eiras das Neves
Producao Industrial no Brasil: uma andalise de dados em tempo real
Rafael Tiecher Cusinato, André Minella e Sabino da Silva Porto Junior
Determinants of Bank Efficiency: the case of Brazil
Patricia Tecles and Benjamin M. Tabak
Pessimistic Foreign Investors and Turmoil in Emerging Markets: the
case of Brazil in 2002
Sandro C. Andrade and Emanuel Kohlscheen
The Natural Rate of Unemployment in Brazil, Chile, Colombia and
Venezuela: some results and challenges
Tito Nicias Teixeira da Silva
136
Abr/2010
Apr/2010
Apr/2010
Apr/2010
Apr/2010
Maio/2010
Maio/2010
May/2010
Aug/2010
Sep/2010

214
215
216
217
218
219
220
221
222
223
224
225
226
227
228
229
Estimation of Economic Capital Concerning Operational Risk in a
Brazilian banking industry case
Helder Ferreira de Mendonga, Délio José Cordeiro Galvdo and
Renato Falci Villela Loures
Do Inflation-linked Bonds Contain Information about Future Inflation?
José Valentim Machado Vicente and Osmani Teixeira de Carvalho Guillen
The Effects of Loan Portfolio Concentration on Brazilian Banks’ Return
and Risk
Benjamin M. Tabak, Dimas M. Fazio and Daniel O. Cajueiro
Cyclical Effects of Bank Capital Buffers with Imperfect Credit Markets:
international evidence
A.R. Fonseca, F. Gonzdlez and L. Pereira da Silva
Financial Stability and Monetary Policy — The case of Brazil
Benjamin M. Tabak, Marcela T. Laiz and Daniel O. Cajueiro
The Role of Interest Rates in the Brazilian Business Cycles
Nelson F. Souza-Sobrinho
The Brazilian Interbank Network Structure and Systemic Risk
Edson Bastos e Santos and Rama Cont
Eficiéncia Bancaria e Inadimpléncia: testes de Causalidade
Benjamin M. Tabak, Giovana L. Craveiro e Daniel O. Cajueiro
Financial Instability and Credit Constraint: evidence from the cost of
bank financing
Bruno S. Martins
O Comportamento Ciclico do Capital dos Bancos Brasileiros
R. A. Ferreira, A. C. Noronha, B. M. Tabak e D. O. Cajueiro
Forecasting the Yield Curve with Linear Factor Models
Marco Shinobu Matsumura, Ajax Reynaldo Bello Moreira and José Valentim
Machado Vicente
Emerging Floaters: pass-throughs and (some) new commodity
currencies
Emanuel Kohlscheen
Expectativas Inflacionarias e Inflacaéo Implicita no Mercado Brasileiro
Flavio de Freitas Val, Claudio Henrique da Silveira Barbedo e
Marcelo Verdini Maia
A Macro Stress Test Model of Credit Risk for the Brazilian Banking
Sector
Francisco Vazquez, Benjamin M.Tabak and Marcos Souto
Uma Nota sobre Erros de Previsdo da Inflagao de Curto Prazo
Emanuel Kohlscheen
Forecasting Brazilian Inflation Using a Large Data Set
Francisco Marcos Rodrigues Figueiredo
Financial Fragility in a General Equilibrium Model: the Brazilian case
Benjamin M. Tabak, Daniel O. Cajueiro and Dimas M. Fazio
137
Oct/2010
Oct/2010
Oct/2010
Oct/2010
Oct/2010
Oct/2010
Oct/2010
Out/2010
Nov/2010
Nov/2010
Nov/2010
Nov/2010
Nov/2010
Nov/2010
Nov/2010
Dec/2010
Dec/2010

231
232
233
234
235
236
237
238
Is Inflation Persistence Over?
Fernando N. de Oliveira and Myrian Petrassi
Capital Requirements and Business Cycles with Credit Market
Imperfections
P. R. Agénor, K. Alper and L. Pereira da Silva
Modeling Default Probabilities: the case of Brazil
Benjamin M. Tabak, Daniel O. Cajueiro and A. Luduvice
Emerging Floaters: pass-throughs and (some) new commodity
currencies
Emanuel Kohlscheen
Cyclical Effects of Bank Capital Requirements with Imperfect Credit
Markets
Pierre-Richard Agénor and Luiz A. Pereira da Silva
Revisiting bank pricing policies in Brazil: Evidence from loan and
deposit markets
Leonardo S. Alencar
Optimal costs of sovereign default
Leonardo Pio Perez
Capital Regulation, Monetary Policy and Financial Stability
P.R. Agénor, K. Alper, and L. Pereira da Silva
Choques nao Antecipados de Politica Monetaria e a Estrutura a Termo
das Taxas de Juros no Brasil
Fernando N. de Oliveira e Leonardo Ramos
138
Dec/2010
Jan/2011
Jan/2011
Jan/2011
Jan/2011
Mar/2011
Apr/2011
Apr/2011
Abr/2011