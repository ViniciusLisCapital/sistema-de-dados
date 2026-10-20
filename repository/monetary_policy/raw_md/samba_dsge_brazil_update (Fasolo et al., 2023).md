Brazilian Macroeconomic Dynamics Redux: Shocks, 
Frictions, and Unemployment in SAMBA Model
Angelo Marsiglia Fasolo, Eurilton Araújo, Marcos Valli Jorge, Alexandre 
Kornelius, Leonardo Sousa Gomes Marinho
578
ISSN 1518-3548
March 2023

ISSN 1518-3548 
CGC 00.038.166/0001-05 
Working Paper Series 
Brasília 
no. 578 
Março 
2023 
p. 3-91

Working Paper Series 
Edited by the Research Department (Depep) – E-mail: workingpaper@bcb.gov.br 
Editor: Rodrigo Barbone Gonzalez
Co-editor: Eurilton Alves Araujo Jr
Head of the Research Department: André Minella 
Deputy Governor for Economic Policy: Diogo Abry Guillen
The Banco Central do Brasil Working Papers are evaluated in double-blind referee process. 
Although the Working Papers often represent preliminary work, citation of source is required when used or reproduced. 
The views expressed in this Working Paper are those of the authors and do not necessarily reflect those of the Banco Central 
do Brasil.  
As opiniões expressas neste trabalho são exclusivamente do(s) autor(es) e não refletem, necessariamente, a visão do Banco 
Central do Brasil. 
Citizen Service Division 
Banco Central do Brasil 
Deati/Diate 
SBS – Quadra 3 – Bloco B – Edifício-Sede – 2º subsolo 
70074-900 Brasília – DF – Brazil 
Toll Free: 0800 9792345 
Fax: +55 (61) 3414-2553 
Internet: http//www.bcb.gov.br/?CONTACTUS

Non-technical Summary
This paper describes extensions to the structure of the SAMBA model1. These additional
developments include a reformulation of the labor-market block that allows for involuntary un-
employment, the direct introduction of imported goods in the ﬁnal consumption bundle, and a
new speciﬁcation for the rest-of-the-world block based on vector autoregressions (VAR). In this
foreign block speciﬁcation, shocks are identiﬁed by sign-restrictions and have a precise economic
interpretation. These changes demand the inclusion of new observable variables and the use
of a new method for estimation, which can cope with the increased number of parameters and
equations. In this context, we estimate the model by Sequential Monte Carlo (SMC) Methods,
leading to posterior distributions that are more stable to small perturbations of the speciﬁcation
of prior distributions.
The paper focuses on the dynamic properties of the model and evaluates its ability to generate
moments that are close to the ones coming from the data. In addition, the paper documents
the responses of important macroeconomic variables to a monetary policy shock, to a shock to
the uncovered interest parity equation, and, ﬁnally, to the identiﬁed foreign shocks in the VAR
speciﬁcation. We compare the macro-variable responses with the ones reported in similar papers
in the literature, providing economic intuition for our results. The ﬁnal exercise is a historical
decomposition of economic time series and concerns how the model interprets the evolution of
macroeconomic variables as a combination of its structural shocks.
Summing up, the dynamic properties of the model seem reasonable and consistent economic
narratives support the behavior of the impulse response functions and the results from the histor-
ical decompositions. Therefore, the model displays the essential preconditions to be employed in
policy analysis and forecasting exercises, with the additional beneﬁt of having structural features
designed to analyze unemployment ﬂuctuations in small-open economies.
1This model belongs to the class of Dynamic Stochastic General Equilibrium (DSGE) models and was developed
by staﬀmembers at the Research Department of the Banco Central do Brasil. Indeed, SAMBA is an acronym
for “Stochastic Analytical Model with a Bayesian Approach” and refers to the famous Brazilian music genre.
3

Sum´ario N˜ao T´ecnico
O artigo descreve extens˜oes feitas `a estrutura do modelo SAMBA2. Essas mudan¸cas incluem
a reformula¸c˜ao do bloco que descreve o mercado de trabalho, permitindo o surgimento de desem-
prego involunt´ario, a introdu¸c˜ao de bens importados na cesta de consumo ﬁnal como tamb´em na
fun¸c˜ao de produ¸c˜ao como insumo intermedi´ario, al´em de uma nova especiﬁca¸c˜ao para o bloco do
setor externo, baseado em vetores autorregressivos (VAR). Nessa nova especiﬁca¸c˜ao, os choques
s˜ao identiﬁcados a partir de restri¸c˜oes de sinais para as respostas ao impulso. Essa metodologia
permite atribuir a esses choques uma interpreta¸c˜ao econˆomica precisa. Por conta dessas mu-
dan¸cas, ´e preciso considerar novas vari´aveis observadas e um novo algoritmo no procedimento
de estima¸c˜ao. Nesse contexto, empregamos o m´etodo de Monte Carlo Sequencial, pois este al-
goritmo consegue ter bons resultados para um n´umero crescente de parˆametros e equa¸c˜oes no
novo modelo. Com efeito, as distribui¸c˜oes a posteriori s˜ao mais est´aveis a qualquer perturba¸c˜ao
inicial que altere as distribui¸c˜oes a priori.
O foco do artigo ´e o estudo das propriedades dinˆamicas do modelo, avaliando a sua ca-
pacidade em reproduzir os momentos diretamente computados a partir dos dados. Adicional-
mente, documenta-se o comportamento das fun¸c˜oes de resposta ao impulso associadas `as vari´aveis
macroeconˆomicas relativamente aos seguintes choques: um choque de pol´ıtica monet´eria, um
choque `a equa¸c˜ao que descreve a paridade de juros e, por ﬁm, aos choques externos identiﬁcados
na estima¸c˜ao do VAR que caracteriza o setor externo. Um ´ultimo exerc´ıcio apresenta a decom-
posi¸c˜ao hist´orica das vari´aveis macroeconˆomicas, ou seja, descreve como o modelo interpreta a
trajet´oria dessas vari´aveis como combina¸c˜ao de seus choques estruturais.
Em resumo, os resultados sugerem que as propriedades dinˆamicas do modelo s˜ao razo´aveis.
O comportamento das respostas ao impulso e o exerc´ıcio de decomposi¸c˜ao hist´orica podem ser
racionalizados por narrativas econˆomicas coerentes. Desse modo, o modelo apresenta os requisitos
b´asicos que o habilitam a ser empregado para responder quest˜oes de pol´ıtica econˆomica e em
exerc´ıcios de previs˜ao de vari´aveis macroeconˆomicas, com o benef´ıcio adicional de possuir novas
estruturas que permitem uma an´alise mais fundamentada das ﬂutua¸c˜oes no desemprego em
pequenas economias abertas.
2O modelo pertence `a fam´ılia dos modelos dinˆamicos e estoc´asticos de equil´ıbrio geral e foi desenvolvido por
pesquisadores do Departamento de Estudos e Pesquisas do Banco Central do Brasil. O acrˆonimo SAMBA se
refere, em inglˆes, ao termo “Stochastic Analytical Model with a Bayesian Approach”, al´em de ser uma alus˜ao a
um importante gˆenero musical brasileiro.
4

Brazilian Macroeconomic Dynamics Redux: Shocks,
Frictions, and Unemployment in SAMBA Model
Angelo M Fasolo, Eurilton Araujo, Marcos Valli Jorge
Alexandre Kornelius, Leonardo Sousa Gomes Marinho‡
March 31, 2023
The views expressed in this paper are those of the authors and
should not be interpreted as representing the positions of the Banco
Central do Brasil or its board members.
Abstract
This paper documents the recent changes in the structure and estimation procedures of
the SAMBA model, providing a complete description of the decision problems that each
economic agent faces, the ﬁrst order conditions that solve those problems, and the new
techniques employed to estimate the model. This updated version of the model incorporates
new features, such as involuntary unemployment, imported goods in the consumption bun-
dle and a new identiﬁed vector auto-regressive process for the rest of the world. Reﬂecting
these changes, the set of observables was expanded to include, for instance, participation
rates in the labor market and an exogenous measure of output gap. In face of increased
complexity and the large number of observables, the model was estimated using Sequential
Monte Carlo (SMC) methods, allowing for a smaller sensitivity to the choice of priors.
JEL Codes: E24, E32, E52
Keywords: DSGE models; Small Open Economies; Monetary Policy; Unemployment
‡The authors would like to thank Carla Tito Fernandes for her support and suggestions on early versions of
this paper. Corresponding Address: Banco Central do Brasil, Research Department. Setor Banc´ario Sul (SBS),
Quadra 3, Bloco B, Edif´ıcio-Sede, Bras´ılia-DF 70074-900, Brazil. Email: angelo.fasolo@bcb.gov.br. Dedicated to
the memory of our dear colleague Leonardo Sousa Gomes Marinho.
5

1
Introduction
In recent years, many central banks have put continuing eﬀort on developing and improving
applied dynamic stochastic general equilibrium (DSGE) models as a tool for policy analysis
and medium-term forecasting. For instance, in the European Central Bank, as in Coenen et al.
(2018)[20], and in the Central Bank of Canada, as in Corrigan et al. (2021)[22], updated versions
of their main DSGE models aiming at expanding the range of the economic issues analyzed and
improving the models’ ability to explain macroeconomic data. Banco Central do Brasil (BCB)
has developed a DSGE model for the Brazilian economy: the SAMBA model1. This model,
ﬁrst documented in Castro et al. (2011, 2015)[17][18], is an open-economy DSGE model with
a large set of nominal and real rigidities, such as wage and price stickiness, habit persistence
in consumption, rule-of-thumb households and capital adjustment costs. The estimation used
Bayesian techniques based on the Metropolis-Hastings (MH) algorithm, and the sample covered
the period in which inﬂation targeting was adopted.
This paper outlines the description and main results of the SAMBA model, extended to
address three notable features. First, to highlight the dynamics of exogenous shocks on labor
market, the new speciﬁcation incorporates unemployment following Gal´ı, Smets and Wouters
(2011)[28]. Their model reinterprets the staggered wage setting formulation in Erceg, Henderson
and Levin (2000)[27], allowing for the emergence of involuntary unemployment while addressing
the absence of economic microfoundations for unemployment in models with a conventional
household speciﬁcation.
Second, in contrast to the original version in which only ﬁrms use
imports as intermediate goods in production, households can also directly buy imported goods
to compose their aggregate consumption bundle.
The new structure allows for an eﬀect of
real exchange rate not only on the supply, but also on the demand of goods.
Finally, the
model replaces the exogenous univariate autoregressive processes characterizing the rest of the
world with a structural vector autoregressive (VAR) model with sign-restricted identiﬁed shocks.
The structural VAR allows for an ampliﬁcation of the eﬀects of foreign shocks in the domestic
economy, alleviating the problems of small-open economy models documented in Justiniano and
Preston (2010)[31].
The extended version of the model structure also aﬀected the selection of observed variables
and the estimation of the model. With respect to observed variables, the new description of the
labor market allows for the inclusion of information about labor supply, measured by participation
rates, while the structural VAR for the rest of the world allows for a stylized role for commodity
prices to aﬀect the domestic economy. The unbalanced growth observed in the Brazilian economy
after 2014 also suggested the use of an exogenous measure of the output gap as an additional
observed variable. This paper provides details on how the output gap is estimated, combining a
structure like the traditional HP ﬁlter with the exogenous process of the DSGE model describing
the evolution of non-stationary productivity.
1SAMBA is an acronym for “Stochastic Analytical Model with a Bayesian Approach” and refers to the famous
Brazilian music genre.
6

With respect to estimation, the increased complexity of the model and the number of parame-
ters to estimate, combined with the inclusion of more observed variables, required a new strategy
to explore the posterior distribution of parameters. The conventional MH algorithm proved very
sensitive to the choice of priors, while, at the same time, not properly handling discontinuities
and multiple modes found in the posterior distribution. The paper will provide an example based
on the distribution of parameters characterizing the cost of investment, and how it aﬀects the
inference about the eﬀects of monetary policy shocks on investment. The model is estimated
using Sequential Monte Carlo (SMC) methods, described in details in Cai et al. (2021)[14]. The
use of bridge distributions, starting from a set of independent prior distributions for structural
parameters, but now augmented with the so-called “system priors”, to make inference about the
posterior distribution brought stability across small changes in the prior distribution and allowed
for a more complete assessment of the uncertainty with respect to important moments generated
by the model.
The paper is organized as follows: the next section reviews the main structure of the model,
with the primitive problems solved by households and ﬁrms, the characterization of monetary
and ﬁscal policy, and the evolution of macroeconomic variables for the rest of the world; section
3 presents the changes in the estimation procedure, highlighting the main properties of the SMC
methodology; and section 4 discusses some properties of the estimated model. Appendixes at
the end summarize equations and present the computation of the steady state, data treatment,
additional results and computational details.
2
The model
This section outlines the structure of the model that introduces unemployment and imported
consumption goods into a standard small-open economy medium-scale DSGE framework for
emerging economies. Because this extension of the original version of SAMBA retains most of
its basic equations, the building blocks already reported in Castro et al. (2011, 2015)[17][18] are
less discussed. Speciﬁcally, we focus on the mechanism that gives rise to unemployment and the
intra-temporal choice between domestic and imported consumption, as well as on describing the
new structural VAR process for the rest of the world.
The model comprises the following blocks: households, ﬁrms, monetary and ﬁscal policies, and
a parsimonious description of the rest of the world. As in the original SAMBA, each component
of aggregate demand corresponds to a speciﬁc sector in the economy. Monetary and ﬁscal policies
are described as linear rules connecting a given policy instrument to the variables it responds
to. Finally, the rest of the world corresponds to an identiﬁed structural VAR model, combining
important foreign variables.
7

2.1
Households
There are two types of households in the economy: optimizing households (indexed by O) and
“rule-of-thumb” households (indexed by RT, corresponding to ϖRT percentage of the popula-
tion). A representative household of type O is a forward-looking agent that chooses optimal
paths for consumption, savings, and investment. To smooth consumption over time, this agent
uses three diﬀerent assets as savings instruments: physical capital, non-contingent one-period
government bonds and non-contingent one-period international bonds. By contrast, a represen-
tative household of type RT cannot access credit, capital and asset markets and does not earn
dividends. This agent only spends the total amount of labor income on consumption goods.
Both types of households supply diﬀerentiated labor services. For optimizing households,
monopoly unions set wages optimally according to a standard Calvo contract, while we assume
RT households accept to receive the average wage of the type O households.
2.1.1
Optimizing Households
A representative optimizing household chooses consumption, physical capital, and ﬁnancial assets
to maximize the expected discounted ﬂow of utility. The decision problem of a type O household
is given by:
max
{Ct,Bt+1,B∗
t+1,Kt+1,It} E0
∞
X
t=0
βtu(CO
t , N O
t (i))
The optimization problem is subject to the following ﬂow budget constraint:
P C
t CO
t + P I
t It + Bt+1
SB
t Rt
+ StB∗
t+1
R∗
t SB∗
t
≤
(1 −τ N
t )W O,n
t
(i)N O
t (i) + RK,n
t
Kt + Bt + StB∗
t + Dn
t −T Lump,n
t
−T D,n
t
+ Ξn
t
where E0 is the expectation operator as of time zero, u(.) is the instantaneous utility function,
β ∈(0, 1) is the time discount factor, CO
t is the consumption level, P C
t is the price of consumption
goods (used as a num´eraire in the model), It is investment, P I
t is the price of investment goods, Bt
denotes government bonds, Rt is the domestic gross interest rate, St is the exchange rate (deﬁned
as units of domestic currency per units of foreign currency), B∗
t represents foreign-currency bonds
issued abroad, R∗
t is the foreign interest rate, W O,n
t
(i) is the household-speciﬁc nominal wage
rate for the type of labor i, N O
t (i) is diﬀerentiated labor, τ N
t
is the tax rate on labor income,
RK,n
t
is the gross nominal rental rate of capital, Kt is physical capital, Dn
t denotes nominal
dividends received from the ﬁrms, T Lump,n
t
is lump-sum nominal net taxes, T D,n
t
is a lump-sum
transfer to ﬁrms and Ξn
t are nominal state-contingent securities. As a timing convention, Bt and
B∗
t represent bonds issued in t −1 and maturing in t, and Kt are capital holdings from t −1.
Thus, variables Bt+1, B∗
t+1 and Kt+1 are decided in t.
The model contains two diﬀerent measures of risk premium, associated, respectively, with
8

domestic and foreign issued bonds: SB
t and SB∗
t
. While SB
t is an exogenous AR(1) process, SB∗
t
depends on aggregate variables describing both domestic and external fundamentals:
SB∗
t
= SB∗h
exp

−ϕ∗
B

B∗x
t+1 −B∗x
+ ϕ∗
V (V ∗
t −V ) + ZB∗
t
i
(1)
where SB∗is the country risk premium in steady state, ϕ∗
B and ϕ∗
V are positive parameters, B∗x
t+1
is net foreign assets-to-exports ratio2, V ∗
t represents foreign investor’s attitude towards risk, and
ZB∗
t
is a shock associated with movements in the country risk related to exogenous factors. The
variables B∗xand V correspond to steady state values for B∗x
t+1 and V ∗
t . B∗x
t+1 is the ratio between
the nominal foreign debt in local currency and the nominal exports3. The net foreign assets as a
proportion to exports, a new feature introduced in this updated version of the SAMBA model,
is not common in DSGE models, but it is frequently considered in studies of debt sustainability.
See, for instance, Reinhart et al. (2003)[37] and Kraay and Nehru (2006)[32]. In the context of
the model, the country risk premium based on the net foreign assets as a proportion to exports,
combined with the structural VAR characterizing the rest of the world, resulted in impulse
response functions more consistent with the theory.
From Gal´ı, Smets and Wouters (2011)[28], the optimizing representative household has a
continuum of members indexed by (i, j) ∈[0, 1]×[0, 1]. Index i represents the type of labor service
in which a given member of the household specializes, while the second index, j, characterizes
the disutility from work for a particular member. Parameter η controls the intensity of this
disutility. The time discount factor, the coeﬃcient of relative risk aversion and the external
habit persistence parameter are β, σ and κ, respectively. Also, there is full risk-sharing among
members of the representative optimizing household, implying that CO
t (i, j) = CO
t . Deﬁne the
expected discounted ﬂow of utility for the optimizing household:
E0
∞
X
t=0
βtZC
t
"
(CO
t (i, j) −κC
O
t−1)1−σ
1 −σ
−Z1−σ
t
1t(i, j)ZL
t ϕS
t ψjη
#
(2)
In equation (2), the indicator function 1t(i, j) equals one if the individual (i, j) is employed
at time t, zero otherwise. There is a labor supply shock ZL
t , a general preference shock ZC
t and
it is assumed that preferences over leisure ﬂuctuate with the permanent technology shock Zt, in
order to keep the model consistent with balanced growth path.
Combined with the scale factor ψ, ϕS
t is an endogenous preference shifter, depending on
aggregate consumption C
O
t
for optimizing households and CS
t , which one can interpret as a
smooth trend for C
O
t . This trend is designed to limit the size of the short-run wealth eﬀect on
labor supply according to the size of parameter v. Weakening the wealth eﬀect is important to
2The presence of B∗x
t+1 characterizes the “debt-elastic interest rate” described in Schmitt-Groh´e and Uribe
(2003)[39]. This speciﬁcation is necessary to induce stationarity in small-open economy models.
3Deﬁning B∗y
t+1 =
 StB∗
t+1

/
 P Y
t Yt

as the net foreign assets-to-GDP ratio, in mathematical notation B∗x
t+1 =

B∗y
t+1QY
t Yt

/
 QtQX
t Xt

, where Qt is the real exchange rate, QY
t and QX
t are the relative prices of GDP deﬂator
and exports with respect to the CPI, and Yt and Xt are real GDP and exports.
9

ensure that employment and the labor force ﬂuctuate procyclically as shocks disturb the economy.
The limit on the size of the wealth eﬀect on labor supply approximates the behavior of the utility
function to a model with GHH preferences4, with the advantage of allowing for a balanced growth
path due to the presence of separable utility in consumption and labor. Variables ϕS
t and CS
t
evolve according to equations:
ϕS
t =
CS
t
(C
O
t −κC
O
t−1)σ
(3)
CS
t =
 CS
t−1
1−v h
(C
O
t −κC
O
t−1)σiv
The mechanics of labor supply for the representative optimizing household goes as follows.
Monopoly unions of each type of labor service i determine W O,n
t
(i) to satisfy labor demand N O
t (i).
There are members of the household specialized on type i labor, but they are heterogeneous in
terms of disutilities, j, associated with providing that type of labor. The household follows a
protocol that lines up workers of type i, in increasing order according to their disutilities j, to
supply the employment level N O
t (i). The resulting employment level associated with workers
of type i can be interpreted as labor at the extensive margin. According to this narrative, the
aggregated version of equation (2), associated to a representative household, can be represented
by:
E0
∞
X
t=0
βtZC
t
"
(CO
t −κC
O
t−1)1−σ
1 −σ
−Z1−σ
t
ZL
t ϕS
t ψ
Z 1
0
N O
t (i)1+η
1 + η
di
#
The last expression inside brackets is a consequence of the aggregation of disutility related to
workers selected to satisfy employment level for type i service, N O
t (i),
R N O
t (i)
0
jηdj = NO
t (i)1+η
1+η
.
Then, the disutility is aggregated for a household across every type i service
R 1
0
NO
t (i)1+η
1+η
di =
R 1
0
R NO
t (i)
0
jηdjdi.
A member of the optimizing household specialized on type i has an incentive to provide labor
if the beneﬁt of receiving the real wage for that work, which is Uc(CO
t )(1 −τ N
t )W O,n
t
(i)/P C
t ,
where W O,n
t
(i)/P C
t
is the real wage for work of type i and Uc(CO
t ) is the marginal utility of
consumption, compensates her disutility from work. Therefore, the following condition holds for
a member with disutility index j willing to provide labor:
Uc(CO
t )(1 −τ N
t )W O,n
t
(i)
P C
t
≥ZC
t Z1−σ
t
ZL
t ϕS
t ψjη
For the marginal supplier of type i labor, denoted by LO
t (i), the participation condition is:
4See Greenwood et al.
(1988)[29].
GHH preferences are often used in models characterizing small open
economies, like Schmitt-Groh´e and Uribe (2003)[39], as they stress the interaction between capital accumulation
and foreign bonds in the household’s savings decision.
10

Uc(CO
t )(1 −τ N
t )W O,n
t
(i)
P C
t
= ZC
t Z1−σ
t
ZL
t ϕS
t ψLO
t (i)η
Use equation (3) and the equilibrium condition CO
t = C
O
t to obtain:
(1 −τ N
t )W O,n
t
(i)
P C
t
= Z1−σ
t
ZL
t ψCS
t LO
t (i)η
After transforming variables to render the model stationary and aggregating across labor
type i, the ﬁnal expression becomes:
(1 −τ N
t ) ˜W O,n
t
= ZL
t ψ eCS
t (LO
t )η
(4)
2.1.2
Rule-of-Thumb Households and Labor Supply Aggregation
The RT representative household has the same preferences as a representative optimizing house-
hold and also has a continuum of members indexed by a pair (i, j) ∈[0, 1] × [0, 1], representing
the type of labor and the disutility from work for a particular member, respectively. Again,
there is full risk-sharing among members of the representative rule-of-thumb household, thus
CRT (i, j) = CRT
t
.
This paper follows the original structure of the model in Castro et al. (2011, 2015)[17][18]
and Medina and Soto (2007)[34], assuming that RT households follow the average wage set for
optimizing households. Hence, for each labor type i in the representative RT household, we
have W RT,n
t
(i) = W O,n
t
. Moreover, we postulate that the endogenous preference shifter follows
ϕRS
t
=
CS
t
(C
RT
t
−κC
RT
t−1)σ . By assumption, CS
t depends only on aggregate consumption for optimizing
households. Since the marginal supplier of type i compares the utility gains associated with the
average real wage of the representative optimizing household with the disutility from work, in
equilibrium, all labor types have the marginal supplier with the same index j = LRT
t
. These
considerations lead to the equation below, after render the model stationary:
(1 −τ N
t ) ˜W O,n
t
= ZL
t ψ eCS
t (LRT
t
)η
(5)
Comparing equations (4) and (5), we have LO
t
= LRT
t
. Thus, one of the consequences of
these simplifying assumptions under the context of a Gal´ı, Smets and Wouters (2011)[28] labor
market is that RT households are strict followers of optimizer households, including labor supply
decisions. On the other hand, in labor market negotiations, optimizer households do take into
account the changes in labor supply originated from the marginal RT household. As a result,
the expression for the consumption of a representative RT household is given by:
CRT
t
= (1 −τ N
t )W O,n
t
P C
t
N RT
t
For each type of household, in equilibrium, we have the following aggregation:
11

C
O
t =
Z 1
ϖRT
1
1 −ϖRT
CO
t ds = CO
t
C
RT
t
=
Z ϖRT
0
1
ϖRT
CRT
t
ds = CRT
t
Moreover, aggregate consumption Ct follows the equation:
Ct = (1 −ϖRT )CO
t + ϖRT CRT
t
(6)
Concerning aggregate labor supply, a household-speciﬁc employment agency uses a Dixit-
Stiglitz function to aggregate diﬀerentiated labor services provided by a speciﬁc household type
deﬁned by the ability to access asset markets. In eﬀect, assume there is a continuum of uniformly
distributed employment agencies. This setting results in the following demands for labor type i
for each household, mapping N O
t to each optimizing household in the interval [ϖRT , 1] and N RT
t
for all RT agents in the interval [0, ϖRT ]:
N O
t (i) =
 
W O,n
t
(i)
W O,n
t
!−ϵW
N O
t ,
∀i ∈[0, 1]
(7)
N RT
t
(i) =
 
W RT,n
t
(i)
W RT,n
t
!−ϵW
N RT
t
,
∀i ∈[0, 1]
(8)
Indeed, each optimizing household in the interval [ϖRT , 1] has its own employment agency,
which produces N O
t . Analogously, each rule-of-thumb household in the interval [0, ϖRT ] also has
its speciﬁc employment agency that generates as output N RT
t
. These agencies, in the interval
[0, 1], then supply N O
t
and N RT
t
to a third employment agency in a competitive market to
produce an aggregate labor Nt according to the following technology:
Nt = Min
Z ϖRT
0
1
ϖRT
N RT
t
ds,
Z 1
ϖRT
1
1 −ϖRT
N O
t ds

where the index s refers to a given household-speciﬁc agency in the unit interval.
Since optimizing households are identical, their agencies produce the same amount of labor.
This reasoning also applies to rule-of-thumb households.
The ﬁrst integral emerges because
each employment agency for optimizing household is uniformly distributed and produces the
same amount of labor N O
t . For the same reason, the second integral is associated with speciﬁc
agencies producing the amount of labor N RT
t
from rule-of-thumb households. Each integral can
be interpreted as the mean labor for a given type of household deﬁned by the ability to access
asset markets.
Because agencies within the two classes of households produce the same amount of labor,
these means collapse to these two values. The Leontief technology indicates that the types of
12

labor are complementary in ﬁxed proportions to produce the aggregate labor used as input in
the ﬁrst stage of production. The speciﬁcation of a third employment agency is a necessary
step because, in contrast to the original version of the model that assumes a single employment
agency that acts on behalf of all households, we consider a continuum of employment agencies
for optimizers and another continuum set for the rule-of-thumb households.
The optimal input choice implies Nt = N O
t = N RT
t
. Unemployment is deﬁned as:
U L
t = Lt −Nt
Lt
(9)
As the technology exhibits constant returns to scale, the aggregate wage compatible with
strictly positive aggregate labor supply leads to zero proﬁts for the employment agency. Hence:
W n
t =
Z ϖRT
0
W RT,n
t
ds +
Z 1
ϖRT
W O,n
t
ds = ϖRT W RT,n
t
+ (1 −ϖRT )W O,n
t
According to the wage-setting rule for RT households, W RT,n
t
= W O,n
t
. As a consequence,
W n
t = W RT,n
t
= W O,n
t
.
2.1.3
Nominal Wage Setting for Optimizing Households
Monopoly unions representing optimizing households can sign forward-looking wage contracts
with the household-speciﬁc agency for those who can access asset markets. A representative
optimizing household faces a Calvo lottery for wages. In each period and with probability 1−θW ,
on behalf of a given optimizing household, the monopoly union may renegotiate its nominal wage
contract with the employment agency, in which case the optimal wage chosen is W O,n,⋆
t
. With
probability θW , the household’s union cannot optimally change its nominal wage, but update
the wage contract according to the indexation rule:
W O,n
t
(i) = ΥW
t−1W n
t−1(i)
where ΥW
t
is a weighted geometric average of wage inﬂation, CPI inﬂation, and labor productivity
growth:
ΥW
t
=
 ΠW
t−1
ωW  ZZC
t−1
4 Π4C
t−1
 1−ωW
4
 1
ZZ
t

where ωW ∈[0, 1] is an indexation parameter, ΠW
t
≡W n
t /W n
t−1 is the gross nominal wage
inﬂation, ZZ
t
= Zt/Zt−1 is the stochastic and time-varying gross growth rate of permanent
technology shocks, and ZZC
t
is the cyclical component of ZZ
t , as described in section 2.2. In this
expression for ΥW
t , we have Π4C
t
= ΠC
t ΠC
t−1ΠC
t−2ΠC
t−3.
Because W O,n
t
= W n
t , we write the indexation rule and wage inﬂation for a representative
optimizing household as functions of the aggregate wage W n
t . Notation is simpliﬁed by writing
13

W O,n
t
(i) = W n
t (i) and W O,n,⋆
t
= W n,⋆
t
. Finally, setting N O
t = Nt reﬂects the optimal choice of
inputs for the aggregate employment agency.
On behalf of a representative optimizing household that provides labor services of type i, the
monopoly union can optimally choose its wage, gauging changes in the disutility of labor relative
to changes in the real labor income. The optimal wage-setting problem is the following:
max
W n
t (i) Et
∞
X
h=0
(θW β)j
(
−ZC
t+hZ1−σ
t+h ZL
t+jϕS
t+hψ
Z 1
0
N O
t+h(i)1+η
1 + η
di + Λt+h
"
(1 −τ N
t )W n
t (i)
P C
t+h
Nt+h(i)
#)
subject to: N O
t (i) =

W n
t (i)
W n
t
−ϵW
Nt, given the simpliﬁed notation for wages in equation (7).
In the problem, Λt+h stands for the Lagrange multiplier from the consumer’s problem of a
representative optimizing household.
Since each union solves the same wage-setting problem for a speciﬁc type of labor service i
provided by an optimizing household, there is a W n,⋆
t
unique for all optimizing households in
the interval [ϖRT , 1]. Moreover, W n,⋆
t
is the same across types of labor services i, because the
ﬁrst-order condition for the wage-setting problem associated with the variety i is such that the
optimal wage depends only on aggregate variables.
In short, given W n
t , W n,⋆
t
, the indexation rule and the wage index derived from the Dixit-
Stiglitz aggregator of labor, the ﬁrst-order condition regarding the optimal wage choice leads to
a traditional wage Phillips curve describing the dynamic evolution of wage inﬂation ΠW
t .
2.1.4
Demand for Imported Goods and Consumer Price Index
In a departure from the original version of the model, households are allowed to buy imported
goods directly from the rest of the world. In the previous version of the model, imported goods
only mattered for price setting as an input to produce the ﬁnal good. A consequence of this
assumption is the crucial role of real exchange rate level in explaining domestic inﬂation, as the
level of the real exchange rate sets the level of marginal costs in the Phillips curve. With the
possibility of replacing domestically produced with imported goods, changes in real exchange
rates also plays a role in domestic inﬂation for consumption goods.
Formally, total consumption Ci
t, i = {O, RT}, combines domestic consumption (CD,i
t
) with
imported consumption (CM,i
t
) according to a CES (constant elasticity of substitution) aggregator,
with parameters oC and vC, the elasticity of substitution, describing how households bundle
domestic and imported consumption:
Ci
t =
h
(oC)
1
vC (CD,i
t
)
vC −1
vC
+ (1 −oC)
1
vC (CM,i
t
)
vC −1
vC
i
vC
vC −1
Prices for these goods are P CD
t
and P M
t , respectively. Given Ci
t, the choice of CD,i
t
and
CM,i
t
results from the minimization of total expenditure P CD
t
CD,i
t
+ P M
t CM,i
t
subject to the
14

CES aggregator constraint. Hence, the ﬁrst order conditions are:
CD,i
t
= oC

QCD
t
−vC
Ci
t
CM,i
t
= (1 −oC)
 QM
t
−vC Ci
t
where QCD
t
= P CD
t
/P C
t and QM
t
= P M
t /P C
t are relative prices. Variable P C
t deﬁnes the consumer
price index (CPI), given by the following expression:
P C
t =
h
oC(P CD
t
)1−vC + (1 −oC)(P M
t )1−vCi
1
1−vC
Using the relative prices deﬁned above, the CPI inﬂation rate (ΠC
t ) is:
ΠC
t =
h
oC(ΠCD
t
QCD
t−1)1−vC + (1 −oC)(ΠM
t QM
t−1)1−vCi
1
1−vC
(10)
where ΠC
t = P C
t /P C
t−1, ΠCD
t
= P CD
t
/P CD
t−1 and ΠM
t
= P M
t /P M
t−1. Notice that the change in
real exchange rates is important in setting the inﬂation of imported goods measured in domestic
currency. The presence of nominal rigidities in price-setting of imported goods avoids an imme-
diate complete pass-through from changes in real exchange rate to CPI inﬂation, as it will be
discussed in section 2.2.2.
2.2
Firms
The production of sectoral goods comprises three stages. The ﬁrst stage involves a domestic
input producer and importers. The domestic producer blends capital and labor services in its
production process. Importers purchase diﬀerentiated raw materials from the rest of the world to
sell to an import-speciﬁc assembler. Next, this assembler bundles the diﬀerentiated commodities
into a homogeneous imported good. The output of the assembler and the domestic input producer
is used as intermediate inputs in the next stage.
In the second stage, a continuum of intermediate good producers converts imported and
domestic inputs into sectoral diﬀerentiated goods. These intermediate good producers require
the use of ﬁnancial services since they ﬁnance a fraction of their imported raw material with
working capital borrowed abroad.
Finally, in the third stage, sectoral assemblers transform the diﬀerentiated goods into four
sectoral homogeneous goods. The ﬁrst three sectoral goods are non-tradable goods aimed at the
domestic market, corresponding to private consumption, government consumption and invest-
ment. The last good is a tradable commodity that is exported to the rest of the world.
15

2.2.1
First Stage: Domestic Input Producers
A representative domestic producer supplies an input, Y D
t , to sectoral intermediate good pro-
ducers. This ﬁrm operates a constant returns-to-scale technology, based in a CES technology,
blending capital and labor services in its production process in a perfectly competitive market:
Y D
t
= ZD
t

αK
ϵD−1
ϵD
t
+ (1 −α)
 Zt
 Nt −N
 ϵD−1
ϵD

ϵD
ϵD−1
, ϵD > 0
(11)
where Kt is physical capital, Nt is the total labor input, N is overhead labor, which we assume
constant over time. Parameters α and ϵD, the elasticity of substitution, describe this technology.
In the context of a Cobb-Douglas production function, Castro et al. (2011)[17] show the presence
of overhead labor reduces the coeﬃcient relating labor demand and production of the domestic
input. Overhead labor generates a convexity in the production function similar, when the model
is linearized, to the assumption of a ﬁxed cost in production, as described in Rotemberg and
Woodford (1999)[38].
There are two technology shocks in the production function.
Variable ZD
t
is a domestic
transitory technology shock, and Zt is a labor-augmenting stochastic trend, representing per-
manent shifts in technology. The temporary technology shock evolves according to a ﬁrst-order
autoregressive process:
log
 ZD
t

= ρD log
 ZD
t−1

+ εD
t
(12)
The evolution of the stochastic trend follows two components, trying to accommodate the dif-
ferent degrees of wealth eﬀects generated when changes in the level of labor productivity can be
at least partially anticipated. Similar decompositions of labor productivity are adopted in the
recent version of the DSGE model of the Federal Reserve of New York and the NAWN II model
of the European Central Bank5. To be clear, both components alter the labor productivity level,
but the evolution of the growth rate of productivity is diﬀerent in each of the two cases:
log
 Zt
Zt−1

= log(ZZ
t ) = log ZZ
ss + log(ZZC
t
) + log(ZZT
t
)
(13)
log
ZZC
t
ZZ
ss

= ρZ log
ZZC
t−1
ZZ
ss

+ εZC
t
(14)
log(ZZT
t
) = εZT
t
(15)
In the equations above, ZZ
ss is the steady state for the long-run growth rate of technology,
measured in gross terms, ZZC
t
is the partially anticipated, or cyclical, component of the stochastic
trend, and ZZT
t
is the unanticipated, or transitory, movement of the stochastic trend.
The domestic input producer takes input prices as given and chooses capital and labor services
5See the FRBNY DSGE Model Documentation, version 1002 (December, 2021)[1] and Coenen et al. (2018)[20].
The model in Coenen et al. (2018)[20] follows closely the solution in Edge, Laubach and Williams (2007)[26],
assuming that agents follow a Kalman Filter process of learning about the evolution of productivity in the model.
16

to minimize total input costs, subject to the technology constraint (11):
min
Kt−1,Nt





RK,n
t
Kt−1 + W n
t Nt −T D,n
t
+P D
t
(
Y D
t
−ZD
t

αK
ϵD−1
ϵD
t−1
+ (1 −α)
 Zt
 Nt −N
 ϵD−1
ϵD

ϵD
ϵD−1 )





where T D,n
t
is a lump-sum transfer from optimizing households which is equal to the overhead
labor cost.
The transfer ensures a well-deﬁned solution to the optimization problem above.
P D
t
is the Lagrange multiplier associated with the technology constraint, which is equal to the
nominal marginal cost of changing the use of the domestic inputs. Cost minimization yields
the demands for capital and labor. Substituting equations deﬁning factors demands into the
technology constraint (11) results in an expression for the marginal cost as function of factor
prices for capital and labor.
2.2.2
First Stage: Importers
Consistent with the evidence on deviations of the Law of One Price, the model has nominal
rigidities expressed in terms of local currency pricing of imported and exported goods.
The
inclusion of local currency pricing helps matching relevant moments of real exchange rates and
foreign prices. In fact, the literature has shown nominal rigidities are responsible for a signiﬁcant
share of exchange rate ﬂuctuations.
In Adolfson et al.
(2007)[4], foreign shocks, including
those in export and import markups, explain almost all exchange rate ﬂuctuations in Europe.
Furthermore, the model with correlated import and export markup shocks has a signiﬁcantly
better match with unconditional second moments of the real exchange rate, compared with a
version of the model with iid shocks.
In this subsection, the problem of importing ﬁrms is
detailed, with the problem of exporting ﬁrms presented later.
A continuum of importing ﬁrms indexed by j ∈[0, 1] choose ﬁrst the amount of imported
varieties they need to produce a homogeneous good sold in a monopolistically competitive market
to imports assembler in the second stage. Importing ﬁrms set their prices according to a Calvo
scheme. The homogeneous good produced by the assembler is used as an input to produce sectoral
diﬀerentiated goods. The assembler converts the diﬀerentiated inputs into a homogenous good,
bundling the diﬀerentiated varieties according to a Dixit-Stiglitz aggregator:
Mt =
Z 1
0
(Mj,t)
ϵM −1
ϵM
dj

ϵM
ϵM −1
, ϵM > 1
(16)
where Mt is the homogenous imported good, Mj,t is the imported variety j, and ϵM is the
elasticity of substitution across varieties. P M
j,t is the local-currency price charged by importing
ﬁrm j and P M
t
is the local-currency aggregate import price. The choice problem of the import
goods assembler, subject to equation (16), yields the following demand for the jth imported
17

commodity and the following import price index:
Mj,t =
 
P M
j,t
P M
t
!−ϵM
Mt
(17)
P M
t
=
Z 1
0
 P M
j,t
1−ϵM dj

1
1−ϵM
(18)
Importing ﬁrms are price makers in domestic markets and operate under price rigidity ac-
cording to the Calvo scheme. Deﬁne the sectoral inﬂation ΠM
t
= P M
t /P M
t−1. In each period, an
importing ﬁrm j faces a constant probability 1 −θM of choosing its prices according to current
market conditions. On the other hand, with probability θM, it updates the price according to
past sectoral inﬂation:
P M
j,t = ΥM
t P M
j,t−1
(19)
ΥM
t
= ΠM
t−1
(20)
Deﬁne P M ∗
t
as the foreign-currency price of imported varieties. The value of proﬁts accrued
to ﬁrm j is given by:
P M
j,t Mj,t −

StP M ∗
t

Mj,t
At period t, importing ﬁrms allowed to optimally set prices maximize the real value of the
expected discounted ﬂow of their proﬁts along the paths over which their own price is not
adjusted optimally. From the deﬁnition of the value of proﬁts and the demand constraint (17),
the ﬁrm solves:
max
P M
j,t
Et
∞
X
i=0
(θMβ)i Λt,t+i


 
ΥM
t,t+iP M
j,t
P M
t+i
!1−ϵM
P M
t+i −
 
ΥM
t,t+iP M
j,t
P M
t+i
!−ϵM
St+iP M ∗
t+i

Mt+i
Since all ﬁrms able to change their prices face the same costs, they choose the same optimal
price. The ﬁrst-order condition implies the following expression for optimal price P M
⋆
t
:
P M ⋆
t
=
ϵM
ϵM −1
Et
∞
P
i=0
(θMβ)i Λt,t+i

ΥM
t,t+i
P M
t+i
−ϵM
St+iP M ∗
t+i Mt+i
Et
∞
P
i=0
(θMβ)i Λt,t+i
 ΥM
t,t+i
P M
t+i
1−ϵM
P M
t+iMt+i
(21)
According to this expression, the ﬁrm sets its optimal price as the ratio of their expected
discounted sum of marginal cost to their expected discounted sum of marginal revenues. In the
absence of nominal rigidity, the optimal price is the usual markup over the marginal cost, with
the markup being ϵM/(ϵM −1). From expression (18), the following equation characterizes the
18

imported good price index:
P M
t
=
"
θM
 ΥM
t P M
t−1
1−ϵM + (1 −θM)

P M
⋆
t
1−ϵM #
1
1−ϵM
(22)
One can write the expression above in terms of relative prices QM
t
= P M
t /P C
t
and QM
⋆
t
=
P M
⋆
t
/P C
t , where P C
t
is the consumer price index (CPI) deﬁned in the household problem.
QM
t
=

θM

ΥM
t
QM
t−1
ΠC
t

1−ϵM + (1 −θM)

QM
⋆
t

1−ϵM

1
1−ϵM
(23)
Lastly, the gross inﬂation rate of imported goods can also be expressed in terms of relative
prices:
ΠM
t
= P M
t
P M
t−1
= QM
t
QM
t−1
ΠC
t
(24)
Conditions (19)-(24) lead to the formulation of a New Keynesian Phillips curve describing
the evolution of ΠM
t .
2.2.3
Second Stage: Sectoral Intermediate Producers
In the second stage, four sectors in the economy are speciﬁed, based on the components of the
domestic demand of goods: domestic private consumption (CD), government consumption (G),
investment (I) and exports (X). Each sector is characterized by a particular price-setting behav-
ior, based on variations of the Calvo setup. In each sector, there is a continuum of intermediate
good producers indexed by j ∈[0, 1]. Each intermediate good producer operates a constant
returns-to-scale technology that converts imported and domestic inputs into sectoral diﬀerenti-
ated goods. Moreover, intermediate good producers require the use of ﬁnancial services since
they must ﬁnance a fraction of their imported input with working capital borrowed abroad.
Intermediate good producers combine the domestic input with imported goods according
to a CES production function to manufacture diﬀerentiated intermediate goods that sectoral
assemblers use in the third stage:
Y H
j,t =

(ϖH)
1
ϵH (Y D
H,j,t)
ϵH −1
ϵH
+ (1 −ϖH)
1
ϵH
" 
1 −ΓM
H
 
M H
j,t
M H
t−1
!!
M H
j,t
# ϵH −1
ϵH


ϵH
ϵH −1
(25)
where H = {CD, G, I, X}, M H
j,t is the imported good, ΓM
H (.) is an adjustment associated with
the imported input as a function of the sectoral level of imports, M H
j,t/M H
t−1, ϖH ∈[0, 1] is
the weight of the domestic input in the production, and ϵH > 0 is the elasticity of substitution
between the two inputs. The following functional form for the adjustment cost satisﬁes in the
19

steady state ΓM′
H,t = ΓM
H = 0:
ΓM
H
 
M H
j,t
M H
t−1
!
= ϑM
H
2
 
 ZM
H,t
−
1
ϑM
H
M H
j,t
M H
t−1
−1
!2
where ϑM
H > 0 and ZM
H,t is an import demand shock.
Each sectoral intermediate good producer takes as given input prices and decides the combi-
nation of inputs that minimizes its total cost:
min
Y D
j,t,M H
j,t
n
P D
t Y D
H,j,t + P M
t
h
1 + ιH

R∗
t SB∗
t
−1
i
M H
j,t
o
,
∀j ∈H
subject to the technology constraint (25). Parameter ιH deﬁnes the fraction of the imported good
that must be ﬁnanced abroad, by signing intra-period loans contracts at the net interest rate
R∗
t SB∗
t
−1. The working capital constraint captures some of the observed trade credit frictions
in small-open economies.
Deﬁne MCH,n
j,t
as the Lagrange multiplier (in nominal terms) related to the technology con-
straint and let P M
H,t ≡

1 + ιH
 R∗
t SB∗
t
−1

P M
t
be the eﬀective import cost in sector H and
ΓM†
H
 M H
j,t/M H
t−1

= ΓM′
H
 M H
j,t/M H
t−1

M H
j,t. Given that all ﬁrms face the same technology, same
input prices and have adjustment costs that do not depend on history – thus, in equilibrium
M H
j,t/M H
t−1 is the same across ﬁrms – and same real marginal cost, the ﬁrst-order conditions
describing the optimal choices of inputs Y D
j,t and M H
j,t result in the following two conditions:
Y D
H,j,t = ϖH
 P D
t
MCH
t
−ϵH
Y H
j,t
(26)
M H
j,t =
 
1 −ϖH
1 −ΓM
H,t
! 

P M
H,t

1 −ΓM
H,t −ΓM†
H,t

MCH,n
t


−ϵH
Y H
j,t
(27)
After substituting the optimal input-output ratio into the technology constraint, the following
equation describes the nominal marginal cost in sector H:
MCH,n
t
=

ϖH
 P D
t
1−ϵH + (1 −ϖH)
 
P M
H,t
1 −ΓM
H,t −ΓM†
H,t
!1−ϵH

1
1−ϵH
(28)
which is a weighted average of the cost of the domestic and imported inputs. For the purpose
of the estimated model, we assume the production of government goods does not use imported
inputs, i.e., ϖG = 1. Hence, government consumption is a non-tradable good whose real marginal
cost of production is equal to P D
t , that is, MCG,n
t
= P D
t .
20

2.2.4
Second Stage: Domestic Consumption Sector
Two types of intermediate producers compose the domestic consumption good sector. Firms
use the same technology, face the same cost minimization problem and take into account similar
downward-sloping demand curves for their products. However, they diﬀer regarding their pricing
strategies: the set of administered prices identiﬁes ﬁrms that are less sensitive to demand and
supply conditions or prices that are in some way regulated by public agencies. A ﬁrm indexed by
j ∈[0, ϖA] is not free to choose its own price and must follow an exogenous pricing rule, speciﬁed
by the government. The letter A denotes the set of ﬁrms that have their prices monitored or
administered by the government, while the letter F denotes the set of freely-set price ﬁrms, where
A ∪F = CD.
In this respect, a fraction 1 −ϖA of ﬁrms in the domestic consumption good sector choose
their prices according to the Calvo setup: whenever possible, these ﬁrms set their prices freely,
responding to current market conditions. In each period, a ﬁrm j ∈F faces a constant probability
θF of adjusting its price according to the indexation rule:
P F
j,t = ΥF
t P F
j,t−1,
∀j ∈F
(29)
ΥF
t = ΠC
t−1
(30)
The expression for ΥF
t
includes the overall CPI inﬂation (ΠC
t ) with a lag, instead of the
freely-set price inﬂation. In this way, as usual in private contracts, the ﬁrms that update prices
take into account overall inﬂation in the economy. On the other hand, if the ﬁrm is allowed to
choose its prices optimally, it solves the following price optimization problem:
max
P F
j,t
Et
∞
X
i=0
(θF β)i Λt,t+i

ΥF
t,t+iP F
j,t −MCCD,n
t+i

Y F
j,t+i,
∀j ∈F
subject to the demand faced by the ﬁrm, given by:
Y F
j,t+i =
 
ΥF
t,t+iP F
j,t
P CD
t+i
!−ϵP
CD
Y CD
t+i , ∀i ≥0
The variable MCCD,n
t+i
denotes the nominal marginal cost incurred in the production of the
domestic consumption good is similar to (28). After substituting the demand constraint into the
objective function, the optimal freely-set price P F
⋆
t
is determined by the pricing condition:
P F
⋆
t
=
ϵP
CD
ϵP
CD −1
Et
∞
P
i=0
(θF β)i Λt,t+i

ΥF
t,t+i
P CD
t+i
−ϵP
CD
MCCD,n
t+i
Y CD
t+i
Et
∞
P
i=0
(θF β)i Λt,t+i

ΥF
t,t+i
P CD
t+i
1−ϵP
CD
P CD
t+i Y CD
t+i
(31)
21

We deﬁne the freely-set price index as follows:
P F
t ≡

1
1 −ϖA
Z
j∈F
(P CD
j,t )1−ϵP
CD dj

1
1−ϵP
CD
=
 
θF
 ΥF
t P F
t−1
1−ϵP
CD + (1 −θF )

P F
⋆
t
1−ϵP
CD !
1
1−ϵP
CD
(32)
One can write the expression above in terms of relative prices QF
t = P F
t /P C
t
and QF
⋆
t
=
P F
⋆
t
/P C
t , where P C
t
is the consumer price index (CPI) deﬁned in the household problem:
QF
t =

θF

ΥF
t
QF
t−1
ΠC
t

1−ϵP
CD + (1 −θF )

QF
⋆
t

1−ϵP
CD

1
1−ϵP
CD
(33)
Also, by deﬁnition, the gross free price inﬂation rate is:
ΠF
t = P F
t
P F
t−1
= QF
t
QF
t−1
ΠC
t
(34)
Conditions (29)-(34) lead to the formulation of a New Keynesian Phillips curve describing
the evolution of ΠF
t .
We now discuss the set of administered prices in domestic consumption-good producers. A
ﬁrm indexed by j ∈[0, ϖA] is not free to choose its own price and must follow an exogenous
pricing rule. Let P A
j,t be the price of ﬁrm j ∈A. In each period t, a fraction θA of ﬁrms are
randomly selected from the set A and are allowed to set their prices following the rule ΥA
t , which
is a function of overall CPI inﬂation, real exchange rate, commodity-price inﬂation and a price-
speciﬁc shock ZA
t . The remaining fraction 1 −θA of ﬁrms update their prices by choosing P A⋆
t
,
according to a conventional Calvo scheme:
P A
j,t =
(
ΥA
t P A
j,t−1, with probability θA
P A⋆
t
, with probability 1 −θA
The novelty in the formulation is that, for estimation purposes, parameter θA assumes a value
arbitrarily close to one. Thus, almost all ﬁrms set prices based on a rule capturing changes in
domestic factors through CPI inﬂation as well as through movements in the real exchange rate
and commodity price inﬂation. Deﬁne P co,∗
t
as commodity price index and Πco,∗
t
= P co,∗
t
/P co,∗
t−1
as commodity price inﬂation. The functional form deﬁning indexation factor ΥA
t is given by:
ΥA
t =
(
 Π4C
t−1
 1
4
 Qt
Qt−1
υ1
A  Qt
Qt−1
Πco,∗
t
υ2
A)
ZA
t
(35)
In the expression above, Π4C
t
= ΠC
t ΠC
t−1ΠC
t−2ΠC
t−3. Parameters υ1
A and υ2
A are positive weights
and Qt denotes the real exchange rate. The term ZA
t is a stochastic exogenous process capturing
22

shifts in these prices that are not explicitly modeled.
The overall administered price index is deﬁned as follows:
P A
t ≡
 1
ϖA
Z
j∈A
(P CD
j,t )1−ϵP
CD dj

1
1−ϵP
CD
We rewrite the index as:
P A
t =

θA
 ΥA
t P A
t−1
 1−ϵP
CD + (1 −θA)

P A
⋆
t

1−ϵP
CD

1
1−ϵP
CD
(36)
The relative price QA
t = P A
t /P C
t
is:
QA
t =

θA

ΥA
t
QA
t−1
ΠC
t

1−ϵP
CD + (1 −θA)

QA
⋆
t

1−ϵP
CD

1
1−ϵP
CD
(37)
The following identity describes the law of motion for the administered price index:
ΠA
t = QA
t
QA
t−1
ΠC
t
(38)
Even with the arbitrary indexation rule, it is still valid that all administered price ﬁrms will
still converge their price changes to the steady-state inﬂation, ΠA = Π
C. Domestic consumption
price index is expressed as a weighted average of freely-set and administered price indices:
P CD
t
=
Z 1
0
(P CD
j,t )1−ϵP
CD dj

1
1−ϵP
CD =
Z
j∈A
(P CD
j,t )1−ϵP
CD dj +
Z
j∈F
(P CD
j,t )1−ϵP
CD dj

1
1−ϵP
CD
Combining the deﬁnition of P F
t
and P A
t , an expression for domestic consumption price index
follows:
P CD
t
=

ϖA
 P A
t
1−ϵP
CD + (1 −ϖA)
 P F
t
1−ϵP
CD

1
1−ϵP
CD
(39)
Finally, the following equation describes the relative domestic consumption price QCD
t
= P CD
t
/P C
t :
QCD
t
=

ϖA
 QA
t
1−ϵP
CD + (1 −ϖA)
 QF
t
1−ϵP
CD

1
1−ϵP
CD
(40)
Inﬂation rate for domestic consumption is:
ΠCD
t
= QCD
t
QCD
t−1
ΠC
t
23

2.2.5
Second Stage: Government Consumption and Investment Sectors
Each sector intermediate good producer in the government consumption and investment sectors
faces a downward-sloping demand curve for its good and set prices following a conventional
Calvo scheme. In each period t, with probability 1 −θH, each intermediate good ﬁrm j ∈H,
for H = {G, I}, sets its price optimally. Deﬁne sectoral inﬂation as ΠH
t
= P H
t /P H
t−1. With
probability θH intermediate good ﬁrm j follows the indexation rule:
P H
j,t = ΥH
t P H
j,t−1,
j ∈H = {G, I}
(41)
ΥH
t = ΠH
t−1
(42)
Unlike the previous version of the model in Castro et al. (2011, 2015)[17][18], the indexation
mechanism of these prices, and also for freely-set prices, is strictly conventional in the Calvo
scheme, without the current value of the inﬂation target playing a role in inﬂation indexation.
Estimation of the model with the inﬂation target as an explicit piece of the indexation mechanism
generated very similar results compared with the model with conventional Calvo scheme of
pricing. Thus, the option for a model with a smaller number of parameters to be estimated
was preferred. Intermediate good producer setting prices maximizes expected discounted proﬁts’
ﬂow:
max
P H
j,t
Et
∞
X
i=0
(θHβ)i Λt,t+i

ΥH
t,t+iP H
j,t −MCH,n
t+i

Y H
j,t+i,
∀j ∈H = {G, I}
subject to the respective demand constraint:
Y H
j,t+i =
 
ΥH
t,t+iP H
j,t
P H
t+i
!−ϵP
H
Y H
t+i,
∀j ∈H = {G, I}
The ﬁrst-order condition with respect to P H
j,t, considering that marginal cost follows equation
(28), and that P H
j,t = P H
⋆
t
for H = {G, I}, is:
P H
⋆
t
=
ϵP
H
ϵP
H −1
Et
∞
P
i=0
(θHβ)i Λt,t+i

ΥH
t,t+i
P H
t+i
−ϵP
H
MCH,n
t+i Y H
t+i
Et
∞
P
i=0
(θHβ)i Λt,t+i
 ΥH
t,t+i
P H
t+i
1−ϵP
H P H
t+iY H
t+i
(43)
The sectoral price index P H
t
in sector H = {G, I}:
P H
t
=
 
θH
 ΥH
t P H
t−1
1−ϵP
H + (1 −θH)

P H
⋆
t
1−ϵP
H!
1
1−ϵP
H
(44)
The price index above leads to an expression for the relative prices QH
t
= P H
t /P C
t
that
depends on QH
⋆
t
= P H
⋆
t
/P C
t , where P C
t
is the consumer price index (CPI) deﬁned in the
24

household problem.
QH
t =

θH

ΥH
t
QH
t−1
ΠC
t

1−ϵP
H + (1 −θH)

QH
⋆
t

1−ϵP
H

1
1−ϵP
H
(45)
Lastly, we deﬁne the gross inﬂation rate as:
ΠH
t = P H
t
P H
t−1
= QH
t
QH
t−1
ΠC
t
(46)
Summing up, prices that are adjusted without considering current market conditions and
ﬁrm forward-looking behavior are set according to (41), whereas optimal sectoral prices follow
equation (43). Lastly, expression (44) determines the sectoral price index. These equations,
combined with the deﬁnition of sectoral gross inﬂation rate in equations (45) and (46), considered
jointly deﬁne New Keynesian Phillips curves for sectors G and I6.
2.2.6
Second Stage: Export Sector
The price setting in the export good sector follows the Calvo framework, with exporting ﬁrms
setting their prices in foreign currency. Let P X
j,t be the foreign-currency price of the variety sold
by the jth intermediate producer of sector X. In each period t, with probability 1 −θX, each
intermediate good ﬁrm j ∈X sets its price optimally, and with probability θX it adjusts the
price according to an indexation rule that combines past sectoral inﬂation in foreign currency
and commodity-price inﬂation7, with indexation parameter ωX ∈[0, 1]:
P X
j,t = ΥX
t P X
j,t−1
(47)
ΥX
t =
 ΠX
t−1
ωX (Π∗
ssΠco,∗
t
)1−ωX
(48)
Compared to the model in Castro et al. (2011, 2015)[17][18], the inclusion of commodity-price
inﬂation on the indexation mechanism for export prices is another simple change to allow for the
eﬀect of such prices in the economy.
The producer of the intermediate export good who sets its price optimally maximizes the real
value of the expected discounted ﬂow of proﬁts in local currency as follows:
max
P X
j,t
Et
∞
X
i=0
(θXβ)i Λt,t+i

ΥX
t,t+iSt+iP X
j,t −MCX,n
t+i

Y X
j,t+i
6Appendix A shows the recursive formulation of the Phillips curve for sectors G and I used in the model.
7Commodity-price inﬂation is expressed here as a gap with respect to its mean. Thus, the indexation mecha-
nism must be normalized by foreign inﬂation, as described in equation (47).
25

subject to the demand constraint:
Y X
j,t+i =
 
ΥX
t,t+iP X
j,t
P X
t+i
!−ϵP
X
Y X
t+i
The ﬁrst-order condition with respect to P X
j,t, considering the nominal marginal cost deﬁned
in (28) and that, in equilibrium, P X
j,t = P X
⋆
t
, is given by:
P X
⋆
t
=
ϵP
X
ϵP
X −1
Et
∞
P
i=0
(θXβ)i Λt,t+i

ΥX
t,t+i
P X
t+i
−ϵP
X
MCX,n
t+i Y X
t+i
Et
∞
P
i=0
(θXβ)i Λt,t+i
 ΥX
t,t+i
P X
t+i
1−ϵP
X St+1P X
t+iY X
t+i
(49)
The law of motion for the export price index P X
t
is:
P X
t
=
 
θX
 ΥX
t P X
t−1
1−ϵP
X + (1 −θX)

P X
⋆
t
1−ϵP
X!
1
1−ϵP
X
(50)
An expression that relates the relative prices QX
t = P X
t /P C
t
and QX
⋆
t
= P X
⋆
t
/P C
t
obtains
from the export price index above. The variable P C
t
is the consumer price index (CPI) deﬁned
in the household problem.
QX
t =

θX

ΥX
t
QX
t−1
ΠC
t

1−ϵP
X + (1 −θX)

QX
⋆
t

1−ϵP
X

1
1−ϵP
X
(51)
Finally, the expression for the gross inﬂation rate of the export good sector is given by:
ΠX
t = P X
t
P X
t−1
= QX
t
QX
t−1
ΠC
t
(52)
Equations (47)-(52) describe a New Keynesian Phillips curve governing the dynamics of ΠX
t
8.
2.2.7
Third Stage:
Firms operating in the third stage of production transform sectoral intermediate varieties into a
sectoral homogenous good in a perfectly competitive market. Aggregation is based in a Dixit-
Stiglitz function:
Y H
t
=
 Z 1
0
 Y H
j,t

ϵP
H −1
ϵP
H
dj
!
ϵP
H
ϵP
H −1
(53)
8Appendix A shows the recursive formulation of the Phillips curve for export prices used in the model.
26

where H = {CD, I, G, X} denotes the four corresponding sectors (private consumption, invest-
ment, government consumption, and exports), Y H
t
is the sectoral ﬁnal output and Y H
j,t is the
input associated with intermediate ﬁrm j. The variable ϵP
H > 1 is the elasticity of substitution
between the diﬀerentiated intermediate varieties.
In each sector H, sectoral goods assemblers choose the optimal quantities of each variety by
solving the following problem:
max
Y H
j,t

P H
t Y H
t
−
Z 1
0
P H
j,tY H
j,tdj

, ∀H, ∀j ∈H
subject to (53). P H
t
denotes the aggregate price of home good H, and P H
j,t stands for the price
of a speciﬁc intermediate variety j. In particular, for H = X, P H
t
and P H
j,t are expressed in
foreign currency because it is assumed the presence of pricing to market. After substituting the
Dixit-Stiglitz aggregator into the objective function, the ﬁrst-order condition with respect to Y H
j,t
engenders the following demand for the jth variety:
Y H
j,t =
 
P H
j,t
P H
t
!−ϵP
H
Y H
t , ∀H, ∀j ∈H
(54)
The zero-proﬁt condition for sectoral good assembler yields the sectoral price index:
P H
t
=
Z 1
0
 P H
j,t
1−ϵP
H dj

1
1−ϵP
H , ∀H
(55)
2.3
Monetary and Fiscal Policies
Monetary policy follows a simple Taylor rule in which monetary authority sets nominal interest
rates based on expected inﬂation and the growth rate of output. It also considers interest rate
inertia and a time-varying target, based on changes of the inﬂation target and the expected value
of the cyclical component of non-stationary productivity9. Monetary policy shocks, described
by ZR
t follow an MA(1) process, in order to capture the short-run dynamics in monetary policy
decision process. The Taylor rule and the evolution of the inﬂation target are given by:
Rt = Rγr
t−1
"
Π
C
t Rnat
t
 
EtΠC
t+1
EtΠ
C
t+1
!γπ  YtZZ
t
Yt−1ZZ
ss
γy#(1−γr)
eZR
t
(56)
Π
C
t =

Π
C
ss
1−ρΠC 
Π
C
t−1
ρΠC
+ exp(ϵΠ,0
t
+ ϵΠ,2
t−2 + ϵΠ,6
t−6 + ϵΠ,10
t−10)
(57)
Rnat
t
= 1
β
 EtZZC
t+1
σ
(58)
9Note that the steady state of nominal interest rates, derived from the consumption Euler equation, is given
by Rss = ΠC
ss
β ZZ
ss.
27

The structure of the equation describing the inﬂation target has a few distinctive features.
First, we assume the inﬂation target follows a very persistent process that evolves according to
the parameter ρΠ
C arbitrarily close to one. Second, there is a set of exogenous and independent
shocks describing anticipated changes in the inﬂation target over two, six and ten quarters. The
timing of the anticipated shocks is consistent with the Brazilian experience, matching the timing
of new target implementations over time.
Compared to the previous version of the model in Castro et al. (2011, 2015)[17][18], ﬁscal
policy is more detailed, now characterized by two rules describing labor taxes and the primary
surplus target, completed with an exogenous process for lump sum taxation. One of the taxes
is distortionary, aﬀecting labor income, as described in section 2.1. Government chooses the
primary surplus target based on past primary results and the expected debt level with respect
to its magnitude in the steady state of the model. The rule, thus, generates a smooth transition
of the current values of the primary result to the one required to stabilize debt. In Castro et al.
(2011, 2015)[17][18], the target for the primary result is set as a function of the contemporaneous
level of government debt, which generates signiﬁcant volatility in a model with distortionary
taxation. Labor taxes are set based on the deviation between the current and the target level of
the primary result.
Sy
t = Tt −P G
t Gt
P Y
t Yt
= τ N
t WtNt + T Lump
t
P Y
t Yt
−P G
t Gt
P Y
t Yt
(59)
By
t+1 = Rt
 By
t
ΠY
t
Yt−1
Yt
−Sy
t

(60)
S
y
t = S
y
ss + ρS

S
y
t−1 −S
y
ss

+ (1 −ρS)γB
 EtBy
t+1 −By
ss

+ ϵS
t
(61)
τ N
t
= τ N
ss + γT
 τ N
t−1 −τ N
ss

+ γS

S4,y
t
−S
y
t

+ ϵT
t
(62)
T Lump
t
P C
t Zt
= eT Lump
t
= eT Lump
ss
+ γT L

eT Lump
t−1
−eT Lump
ss

+ ϵT L
t
(63)
S4,y
t
= 0.25(Sy
t + Sy
t−1 + Sy
t−2 + Sy
t−3)
(64)
In the equations above, By
t is the debt-to-GDP ratio, Sy
t and S
y
t are the primary surplus and
its target (both as a proportion of GDP), Gt is exogenous government spending, τ N
t
are labor
taxes, as mentioned in the section on households, and T Lump
t
is nominal lump sum taxation.
Equation (59) also deﬁnes an overall tax rate over nominal GDP and equation (63) describes
the evolution of T Lump
t
. Finally, the last equation speciﬁes a smoothed version for the primary
surplus (Sy
t ).
28

2.4
Demand for Brazilian Exports and Rest of the World
Export goods Xt from Brazil are homogeneous goods before they leave the dock. Nevertheless,
they become diﬀerentiated commodities in international markets. Analogously to the domestic
economy, the rest of the world (ROW) uses the Brazilian exported good as a productive input.
The exports assembler ships the Brazilian good abroad at the price P X∗
t
, in foreign currency.
Next, foreign producers combine the Brazilian good with the goods produced elsewhere, which
we label Y D∗
t
. In parallel with the domestic economy, the foreign output is a composite between
Y D∗
t
and imported inputs from Brazil. The following expression summarizes this technology:
Y ∗
t =
 
(ϖ∗)
1
ϵ∗h
1 −ΓM ∗
t

M ∗
t
i ϵ∗−1
ϵ∗
+ (1 −ϖ∗)
1
ϵ∗
Y D∗
t
 ϵ∗−1
ϵ∗
!
ϵ∗
ϵ∗−1
where M ∗
t = Xt holds, with ϵ∗> 0 being the elasticity of substitution between Brazilian exports
and the goods produced elsewhere. The parameter ϖ∗is the share of Brazilian exports in the
ROW output bundle and ΓM ∗
t
is an import adjustment cost with ϑM ∗≥0:
ΓM ∗
t
= ϑM ∗
2

ZM ∗
t
−
1
ϑM∗
Xt/Y ∗
t
Xt−1/Y ∗
t−1
−1
2
(65)
The foreign good producer chooses the optimal combination of the Brazilian input and the
inputs from elsewhere, so as to minimize its total cost:
min
Xt,Y D∗
t
n
P D∗
t
Y D∗
t
+ P X
t Xt
o
subject to the production function for Y ∗
t . Denoting P ∗
t as the Lagrange multiplier related to the
technology constraint, ΓM ∗†
t
as the derivative of the adjustment cost function, and QX∗
t
≡P X
t /P
∗
t
as the relative price of Brazilian exports in foreign currency, the ﬁrst-order condition with respect
to Xt results in the following expression for the world demand for Brazilian exports:
Xt =

ϖ∗
1 −ΓM ∗
t
  
QX∗
t
 1 −ΓM ∗
t
−ΓM ∗†
t

!−ϵ∗
Y ∗
t
(66)
One of the main changes of this version of the model is related to the world’s economy
and the evolution of imported prices in foreign currency.
Instead of using AR(1) shocks to
characterize these variables, the world’s economy is described by a vector autoregressive (VAR)
model including ﬁve variables: GDP, interest rates, inﬂation, risk aversion and commodity prices.
An additional auxiliary equation links changes in import prices, denominated in foreign currency,
with changes in commodity prices. The VAR, combined with the auxiliary equation for import
prices, allows for not only an improvement in terms of policy analysis, but also provides a simple
approach to include commodity prices in the model without a complete structural description
29

of a commodity sector in the economy. The estimation of the VAR is made apart from the
structural model for Brazil, using a Gibbs-sampler with sign restrictions and two lags. From
a theoretical perspective, estimating the VAR apart from the rest of the structural model is
possible because of the small-open economy hypothesis for Brazil, postulating that shocks in the
domestic economy do not inﬂuence the rest of the world10. From a practical perspective, the
procedure also signiﬁcantly reduces the complexity of the SMC procedure due to the smaller
number of parameters.
Deﬁne Z∗
t = [Y ∗
t ; R∗
t ; Π∗
t ; V ∗
t ; P co,∗
t
] as the vector stacking foreign variables, Ai as the matrix
of coeﬃcients for lag i and ϵ∗
t as the vector of structural shocks with covariance matrix B. The
VAR is presented in the following form:
Z∗
t = A1Z∗
t−1 + (...) + AnZ∗
t−n + ϵ∗
t ,
ϵ∗
t ∼N(0, B)
(67)
Sign restrictions identify four structural foreign shocks in the VAR: demand, supply, ﬁnancial
and monetary policy. The sign restrictions imposed are summarized in table 1.
Table 1: Sign Restrictions for VAR Identiﬁcation
Interest Rates
GDP
Inﬂation
Risk
Commodities
Monetary Policy
+
-
Supply Shock
-
+
-
Demand Shock
+
+
+
Financial Shock
-
+
As mentioned before, a new equation provides a link between the relative import prices in
foreign currency and commodity prices. The equation augments the AR(1) process used in Castro
et al. (2011, 2015)[17][18] with a lag of the commodity price index as an additional term. Thus,
commodity prices have an indirect eﬀect to the domestic economy, through the transmission of
changes in these prices to the variables of the rest of the world. It also has a direct link from
commodity prices to the domestic economy. The equation is deﬁned as:
log(QM∗
t
/QM∗
ss ) = ρQMlog(QM∗
t−1/QM∗
ss ) + γClog(P co∗
t−1/P co∗
ss ) + ϵQM∗
t
(68)
2.5
Market Clearing Conditions and GDP
Starting at the ﬁrst stage of production, ﬁrms operate under ﬂexible prices. Thus, the total
domestic input supplied by the domestic producer to sector H = {CD, I, G, X} matches the
total input demand by all ﬁrms j operating in sector H. Also, the supply of the imported input
in sector H = {CD, I, X} equals the total demand for imports by all ﬁrms j operating in sector
H.
Aggregating across all sectors, the market clearing condition for domestic and imported
10See, for instance, Canova (2005)[15] with a discussion and an application of such procedure for VAR models.
30

inputs is:
Y D
t
= Y D
CD,t + Y D
I,t + Y D
G,t + Y D
X,t
(69)
Mt = M CD
t
+ M I
t + M X
t + CM
t
(70)
Total sectoral inputs result from the aggregation of equations (26) and (27):
Y D
H,t = ϖH
 
P D
t
MCH,n
t
!−ϵH
ˆY H
t
(71)
M H
t
=
 
1 −ϖH
1 −ΓM
H,t
! 

P M
H,t

1 −ΓM
H,t −ΓM†
H,t

MCH,n
t


−ϵH
ˆY H
t
(72)
The aggregation of diﬀerentiated goods in the context of a Calvo pricing mechanism and a
Dixit-Stiglitz technology generates a distortion associated with the price dispersion across goods’
varieties. However, in the context of linearization of the equilibrium conditions, the distortion
resulting from price dispersion disappears from the model. Formally, aggregating across all ﬁrms
j in each sector H = CD, I, G, X yields:
ˆY H
t
=
Z 1
0
Y H
j,tdj = Y H
t
Z 1
0
 
P H
j,t
P H
t
!−ϵP
H
dj = Y H
t vH
t
The integral vH
t
=
R 1
0
 P H
j,t/P H
t
−ϵP
H dj represents the price dispersion eﬀect.
In a linear
approximation around the steady state, vH
t = 1. Also, the following equalities hold:
Y CD
t
= CD
t , Y I
t = It, Y G
t
= Gt and Y X
t
= Xt
The Calvo mechanism also generates a distortion in labor supply, as a consequence of wage
dispersion across labor types. However, again, in a ﬁrst-order approximation around the steady
state of the model, labor supply from households will be the same as the labor eﬀectively provided
by the aggregate employment agency.
Market clearing in labor markets, combined with the
adopted hypothesis about wage-setting for rule-of-thumb consumers, results in the following
equation:
b
Nt
=
Z
s∈RT
Z 1
0
N RT
t
(i)dids +
Z
s∈O
Z 1
0
N O
t (i)dids
=
N RT
t
Z
s∈RT
Z 1
0
 
W RT,n
t
(i)
W RT,n
t
!−ϵW
dids + N O
t
Z
s∈O
Z 1
0
 
W O,n
t
(i)
W O,n
t
!−ϵW
dids
=
ϖRT N RT
t
+ (1 −ϖRT )N O
t
Z 1
0
 
W O,n
t
(i)
W O,n
t
!−ϵW
di
=
Nt

ϖRT + (1 −ϖRT )vO
t

31

Again, after deﬁning vO
t =
R 1
0

W O,n
t
(i)
W O,n
t
−ϵW
di, the wage dispersion eﬀect is given by: vW
t
=
ϖRT + (1 −ϖRT )vO
t , which equals one if the equilibrium conditions of the model are linearized
around the steady state.
With respect to households, equation (6) describes aggregate consumption. Because each
household member has full consumption insurance, asset accumulation is a household decision,
not an individual one. Therefore:
R
s∈O Is,tds = It;
R
s∈O Ks,tds = Kt;
R
s∈O Bs,tds = Bt and
R
s∈O B∗
s,tds = B∗
t
where It, Kt, Bt and B∗
t are the corresponding economy-wide counterparts.
2.5.1
GDP Deﬁnition and Law of Motion for Net Foreign Assets
It is important to discuss the deﬁnition of nominal and real GDP for market clearing and ag-
gregation purposes. In conventional models with a single sector, real GDP is deﬁned during
aggregation, clearing markets with the equations deﬁning supply and demand of goods. In the
model described above, where every component of aggregate demand is deﬁned as a unique sec-
tor, with a unique price-setting behavior, it is not possible to pin down real GDP. Denote real
GDP as Yt and GDP deﬂator as P Y
t . Using the nominal value-added concept, nominal GDP
P Y
t Yt satisﬁes the following National Accounts identity:
P Y
t Yt = P C
t Ct + P I
t It + P G
t Gt + StP X
t Xt −StP M ∗
t
MtvM
t
(73)
The last expression vM
t
deﬁned the price dispersion in imports, and, as it was the case with
other sectors of the economy adopting the Calvo pricing mechanism, a linear approximation
around the steady state of the equilibrium conditions results in vM
t
= 1.
Because the model contains only sectoral outputs, there is no equilibrium conditions to pin
down real GDP: it is only possible to characterize nominal GDP. Thus, it is necessary to introduce
an additional equation to determine this variable. Deﬁne the Laspeyres quantity index as follows,
with the subscript ss identifying steady state variables:
Yt =
P C
ssCt + P I
ssIt + P G
ssGt + SssP X
ssXt −SssP M ∗
ss MtvM
t
P C
ssCss + P IssIss + P G
ssGss + SssP X
ssXss −SssP M ∗
ss MssvM
ss
(74)
In the numerator of the expression above, weights on quantities are the base-year prices,
considered equal to steady state prices. The denominator displays the nominal value added in
steady state.
After normalizing real GDP in steady state, Yss = 1, the denominator of the
Laspeyres index is P Y
ssYss = P Y
ss. Using P Y
ss in the denominator of the quantity index, and the
fact that vM
t
= 1, divide the numerator and the denominator of equation (74) by P C
ss to obtain:
QY
ssYt = Ct + QI
ssIt + QG
ssGt + QssQX
ssXt −QssQM∗
ss MtvM
t
(75)
32

where Qss = SssP ∗
ss/P C
ss is the real exchange rate in the steady state, QY
ss = P Y
ss/P C
ss, QI
ss =
P I
ss/P C
ss, QG
ss = P G
ss/P C
ss, QX
ss = P X
ss/P ∗
ss, QM∗
ss
= P M ∗
ss /P ∗
ss and P ∗
ss denotes the steady-state
value for the general price index in the rest of the world.
Under the strategy described above, real GDP is determined in equation (75) and the model
pin down GDP deﬂator according to equation (73). An alternative strategy, used in the original
version of the model, is to deﬁne a geometric mean price index for P Y
t
and use the expression
(73) to determine real GDP. Both strategies are equivalent in a linear approximation around the
steady state.
Finally, equation describing the evolution of net foreign assets is obtained by combining the
budget constraints of all households in the economy with the previous aggregations results, as
well as the government budget constraint. The ﬁnal equation for net foreign assets is given by:
B∗y
t+1
R∗
t SB∗
t
=
 Yt−1
ΠY
t Yt
Qt
Qt−1
ΠC
t
ΠC∗
t

B∗y
t
+ NXy
t −L∗y
t
where B∗y
t+1 = StB∗
t+1/P Y
t Yt, NXy
t is the net exports-to-GDP ratio and L∗y
t
is the total payments
of interests on external borrowing due to working capital restrictions, measured as a proportion
of nominal GDP. Expressions for NXy
t and L∗y
t
are:
NXy
t = StP X
t Xt
P Y
t Yt
−StP M ∗
t
Mt
P Y
t Yt
vM
t
L∗y
t
=
X
H
ιH

R∗
t SB∗
t
−1
 P M
t M H
t
P Y
t Yt
2.6
Shocks
This section presents a brief discussion on the functional form of the structural shocks in the
model. The model has four technology shocks: transitory productivity (ZD
t , presented in equa-
tion (11)), cyclical component of permanent technology growth rate (ZZC
t
, equation (14)), tempo-
rary component of permanent technology growth rate (ZZT
t
, equation (15)), and an investment-
speciﬁc one (ZI
t ). The investment-speciﬁc shock aﬀects the functional form describing the adjust-
ment cost of investment growth. These shocks follow an AR(1) process, except for the temporary
component of permanent technology growth rate, which is a white noise. The evolution of non-
stationary productivity is discussed in detail in subsection 3.2.
Households are directly aﬀected by ﬁve shocks. The intertemporal Euler equation for domes-
tic consumption, in equilibrium for optimizing households, shows a preference shock (ZC
t ) and
domestic risk premium shock (SB
t ). The UIP (uncovered interest rate parity) condition, derived
from the ﬁrst order condition of foreign bonds has a country risk premium shock (ZB∗
t
) and an
ad hoc disturbance (ZQ
t ). Finally, the labor-leisure choice described by the intratemporal Euler
condition is aﬀected by a labor supply shock (ZL
t ). Again, these shocks follow an AR(1) process.
The model also includes ad hoc cost-push shocks associated with New Keynesian Phillips
33

curves. We do not impose time-varying elasticities of substitution for Dixit-Stiglitz aggregators
as the source of markup shocks in order to preserve the recursive formulation derived from the
non-linear equations describing the ﬁrst-order conditions with respect to wages and prices11.
Following Smets and Wouters (2007)[40], cost-push shocks are characterized by an ARMA(1,1)
process, in order to accommodate both short- and long-lived movements in prices. Moreover, the
sign of the MA(1) component is negative, characterizing the exogenous high-frequency move-
ments of the price level as partially mean reverting. The model contains shocks to the wage
Phillips curve (ZW
t ) and the same cost-push shocks (ZP
t ) for the Phillips curves in sectors G, I
and for the equation describing inﬂation dynamics associated with ﬁrms that choose prices freely
in sector CD12. Also concerning sector CD, there are speciﬁc shocks driving the pricing rule
followed by ﬁrms with administered prices (ZA
t ). Lastly, distinct shocks (ZP X
t
), diﬀerent from
ZP
t , drive the Phillips curve for export sector.
The policy block comprises ﬁscal and monetary rules. Regarding ﬁscal policy, government
consumption (Gt) and lump sum taxes are characterized as an AR(1) process and specify two
white noise disturbances associated with ﬁscal rules for two variables: targets for government
surpluses and labor tax rates. Monetary policy follows a Taylor rule with a monetary policy
shock (ZR
t ) described by a MA(1) process. In addition, we model the inﬂation target (Π
C
t ) as a
random walk with one unanticipated disturbance and three uncorrelated news shocks associated
with the horizons of two, six and ten quarters.
Concerning the dynamics between the domestic and the foreign economy, the VAR relating the
rest of the world observed variables and the equation characterizing the dynamics of import price
goods measured in foreign currency, described in section 2.4, associate six observed variables with
six exogenous shocks. Shocks in these equations are white noise. There are also shocks aﬀecting
the Brazilian demand for imported goods13 (ZM
H,t, for H = {CD, G, I, X}), and the demand from
the rest of the world for Brazilian exports (ZM ∗
t
). These shocks follow an AR(1) speciﬁcation.
2.7
Transformations to induce stationarity
The model has two stochastic trends, a nominal one whose stochastic growth rate is Π
C
t and a
real one whose stochastic growth rate is ZZ
t . Along the balanced growth path, all real variables,
except for labor, grow at the same rate ZZ
t , whereas levels of all nominal variables, except for
nominal wages, grow at the same rate Π
C
t . Nominal wages incorporate the two stochastic trends.
Regarding notation, we denote all detrended variables dv with a tilde (f
dv). In order to write
down the model in its stationary form, all real variables are divided by the level of technology
Zt. Analogously, all variables describing nominal price levels become stationary by dividing their
corresponding levels by the price P C
t . To cast wages in their stationary form, we divide them
by both Zt and P C
t . The same approach is used for T Lump,n
t
. Finally, we detrend the smooth
11Writing the non-linear system allows for the use of non-linear solution methods to compute the equilibrium
conditions, which is essential to carry out welfare evaluations with the model.
12Subsection 3.3 also discusses a few motives for this simpliﬁcation considering the estimation process.
13Subsection 3.3 discusses a simpliﬁcation imposed in the structure of these shocks for estimation purposes.
34

trend for consumption (CS
t ) as follows:
eCS
t = CS
t
Zσ
t . Some variables, including labor, ratios to
GDP and ﬁnancial variables such as interest rates and foreign investor’s risk aversion are already
stationary. Finally, a variable with the subscript ss represents its steady-state value.
3
Estimation
3.1
Data
Compared to the model described in Castro et al. (2011, 2015)[17][18], there are both changes
in the number of variables observed and also in the treatment of these series in this version of
the model14. Most of the changes in data treatment, as it will be later discussed, are related to
the extended sample size used for estimation. With respect to the number of variables observed,
there is a trend in the literature, especially in models designed for policy analysis, of including
data that is considered relevant to characterize new features added to old models, or to better
characterize the dynamics of the economy. As examples, Corrigan et al. (2021)[22] expanded the
number of observed variables in ToTEM III to 50, as the model now incorporates information
on exports of commodity goods and a detailed housing market. Following the same line, the
evolution of the original model described for Sweden in Adolfson et al.
(2013)[3], “Ramses
II”, includes three additional observed variables: unemployment, interest rate spreads and the
interest rates to non-ﬁnancial corporations15. In Coenen et al. (2018)[20], the new model for the
Euro Area includes 6 additional variables to characterize the new ﬁnancial frictions incorporated
in the model. It also includes information on long-term GDP growth and inﬂation expectations.
The model includes 30 observed variables, incorporating information on prices, economic
activity, labor market, ﬁscal and monetary policy, and the foreign sector. Sample starts in 2001Q4
and ﬁnishes in 2019Q4, for a total of 73 observations in the time dimension. However, the ﬁrst
eight observations are used to initialize the Kalman ﬁlter. This is particularly important for the
current version of SAMBA, where the non-stationary inﬂation target and the unit root generated
from the functional form of monitored prices play a signiﬁcant role. Information before 2001Q4
was not available for all observed variables, and information after 2019Q4 includes the Covid-19
pandemic period, where inference based on the linear-Gaussian framework of the Kalman ﬁlter
is inappropriate. Note that the time span includes almost the whole period under an inﬂation
targeting regime, thus avoiding signiﬁcant breaks in the functional forms characterizing monetary
policy.
Data on domestic prices remain the same as in Castro et al. (2011, 2015)[17][18], with CPI
inﬂation, freely-set price inﬂation, and administered price inﬂation all detrended by the steady
state inﬂation – annual inﬂation of 4.5%, consistent with the most frequent value of the inﬂation
14Table 6 in the appendix summarizes data treatment for each time series used for estimation.
15A new model for policy analysis in Sweden, “MAJA”, described in Corbo and Strid (2020)[21], incorporates
a larger number of observed variables describing the international economy, but reduces the number of observed
domestic variables, as the new model includes a detailed structural block describing the foreign economy, but
simpliﬁes the ﬁnancial sector described in “Ramses II”.
35

target in the sample. Data on inﬂation expectations, from the survey conducted by the Banco
Central do Brasil, is included to provide model discipline in terms of short-term responses of
prices to exogenous shocks. With respect to National Accounts data, the demographic transition
observed in Brazil justiﬁes the use of information measured in per capita terms. Combined with
the information on GDP growth, a measure of the Brazilian output gap is informed to the model.
Details on the computation of the output gap are provided in subsection 3.2.
With respect to labor market, the growth rate of occupied population used in Castro et
al. (2011, 2015)[17][18] is replaced by the unemployment rate, detrended by the sample mean.
Information on the participation rate is also included. Due to signiﬁcant methodological changes
in the employment survey for data starting in 2012, time series on unemployment, participation
rate, and the growth rate of wages were simulated for the period between 1999 and 2011 using
mixed-frequency VAR models based on the procedure in Alves and Fasolo (2015)[5]. Simulations
combine information from other surveys and the General Registry of Employed and Unemployed
Persons (CAGED, in Portuguese), of the Ministry of Labor and Social Security (MTP)16.
For the structural VAR describing the rest of the world, the Fed Funds rate and the CPI still
measure world’s interest rates and inﬂation, respectively. Output gap is the cyclical component of
weighted real GDP measure of the main trade partners detrended by the one-sided HP ﬁlter. The
last two elements of the VAR, risk aversion and commodity prices, are measured as the principal
component of a set of normalized variables related to each element. For risk aversion, variables
include the VIX (S&P 500, CBOE), MOVE (Treasuries, Merrill Lynch), VXY (currencies, JP
Morgan) and the spread between the Moody’s corporate yields for BAA bonds and US Treasury
10-year yield. For the commodity prices, variables include Banco Central do Brasil’s Commodity
Index (IC-BR), Brent oil prices, and CRB and CRY Indexes.
Concerning other external variables, the relative price of imports is still measured as the
gap between index of imported good and foreign inﬂation. However, the observed variable now
is the demeaned growth rate of the relative price of imports. The larger sample now includes
the reversion of the commodity boom observed in the early 2000’s, allowing for the growth rate
of the relative price to be representative of the evolution of such variable17. Also, in terms of
country risk premium, the credit default swap (CDS) for Brazilian debt of 5 years replaces the
JP Morgan’s Emerging Market Bond Index (EMBI) Brazil.
With respect to monetary policy, nominal interest rates are demeaned from an exogenous
target of 8.5%. Combined with the inﬂation steady state of 4.5% and an international real interest
rate of 1% (nominal rates of 3% and inﬂation of 2%), these assumptions imply a country risk
premium of 300 basis points. Data also includes the announced changes in the inﬂation target,
consistent with the historical Brazilian experience and the description of shocks in equation (57).
Combining all the details described above, there is a total of 30 observed variables informed
16Data from CAGED can not be used as a standard indicator for labor market conditions, as it only considers
information from the formal labor market.
17In Castro et al. (2011, 2015)[17][18], the relative price of imports is detrended using a linear trend. The
sample covers the period between 1999Q3 and 2010Q2.
36

to the model. In order to improve the model’s ﬁt to the data and reduce the estimated volatility
of structural shocks, measurement errors were included in equations describing a few observed
variables. Speciﬁcally, the output gap and the growth rates of nominal wages and GDP compo-
nents have measurement errors characterized by an MA(1) process. The volatility of the MA(1)
process is estimated in the model under speciﬁc restrictions discussed in section 3.4. Deﬁne Xt as
a generic observed variable of the model where measurement errors are included, xt as the model
(endogenous) representation of such observed variable, and ϵme,x
t
as the measurement error in
period t for the observed variable. Equations characterizing Xt have the following form:
Xt = xt + σxσx(ϵme,x
t
+ µme,xϵme,x
t−1 )/((1 + µ2
me,x)0.5)
(76)
with the following parameters: σx is the volatility of the observed variable; σx is a cap for the
maximum value of the volatility of the measurement error; and µme,x is a parameter deﬁning the
MA(1) process.
3.2
Estimating the output gap
Inference with respect to the output gap, used as an observable in the model, is made outside
the estimation procedure. There are a few reasons to adopt this approach. First, as described
in ﬁgure 1, it is hard to consider the existence of a clear balanced growth path in the Brazilian
economy, as imports and exports per capita seem to grow at a faster pace compared to aggregate
GDP per capita and its domestic components18. The increase in the degree of openness, espe-
cially considering the short samples available for Emerging Economies, and the consequences for
macroeconomic modeling are discussed in Brazdik et al. (2020)[13] in the context of a review of
the main structural model of the Czech Republic National Bank.
Figure 1: Log per capita GDP and components – Index 2001Q3 = 100
2002Q1
2004Q1
2006Q1
2008Q1
2010Q1
2012Q1
2014Q1
2016Q1
2018Q1
4.4
4.6
4.8
5
5.2
5.4
GDP
Consumption
Government
Investment
Exports
Imports
18Other approaches try to make inference about joint trend in data. For Brazil, Costa (2016)[23] provides an
uniﬁed framework using Brazilian data, but does not include exports and imports in his model.
37

A second reason to use the output gap as an observable in the model is the lack of data on
productivity for the Brazilian economy available in real time. It has become common practice,
especially among models designed for policy analysis, to incorporate information about the pro-
ductivity growth, either by a direct or proxy measurements of this variable19. The approach for
estimation here is closer to the model used by the Bank of Canada, described in Corrigan et al.
(2021)[22]. Speciﬁcally for the model described here, the central role played by non-stationary
productivity shocks forced the inclusion of an indirect measurement in order to discipline the
dynamics of the economy, especially during crisis periods20. Historical decompositions in versions
of the model that did not include the output gap usually consider extreme events, as the 2008
Global Financial Crisis, as a permanent change in productivity, resulting in an implied output
gap close to zero during that period.
One ﬁnal reason to use the output gap as an observable is the ability to compare the inputs
of the model with other available estimates of the output gap calculated by other ﬁlters or
produced by the Banco Central do Brasil staﬀ. The procedure also does not preclude, as a policy
exercise, to inform the model with these other estimates, thus generating alternative paths for
productivity growth in Brazil.
The estimation of the output gap is based on the procedure described in Andrle (2013)[6] as
a modiﬁed HP ﬁlter, where it is assumed that the growth rate of the trend has a steady state.
The modiﬁed equations describing the ﬁlter are speciﬁed in state-space form to perform Bayesian
evaluation of the posterior distribution of parameters. The hypothesis of a steady state for the
growth rate of the trend makes the evolution of potential output coincide with the one described
in equations (13)-(15). Deﬁne Y obs
t
as the demeaned log-level of real GDP per capita. The ﬁlter
is characterized by the following set of equations:
Y obs
t
= yt + log(Zt)
yt = α1yt−1 + (α2 −α1) yt−2 + σyϵy
t
log
 Zt
Zt−1

= log(ZZ
t ) = log ZZ
ss + log(ZZC
t
) + log(ZZT
t
)
log
ZZC
t
ZZ
ss

= ρZ log
ZZC
t−1
ZZ
ss

+
 1 −ρ2
Z
0.5 σZCεZC
t
log(ZZT
t
) =
 1 −ρ2
Z
0.5 σZT εZT
t
ϵy
t ∼N(0, 1),
εZT
t
∼N(0, 1),
εZC
t
∼N(0, 1)
Note that the model normalizes the standard deviation of shocks in productivity by the
19See the documentation of the latest version of the FED-NY DSGE model[1], which incorporates total factor
productivity for the US economy as an observable for the model. The estimation in Coenen et al. (2018)[20]
includes long term growth expectations for the Euro Area as a proxy for productivity growth.
20We describe the inclusion of the output gap as an indirect measurement of productivity because the combi-
nation of GDP per capita growth and the output gap as observed variables in the model provides an inference
about the growth rate of per capita non-stationary productivity, adjusted by measurement errors included in the
output gap equation described in (76).
38

autoregressive parameter of the cyclical component of productivity. Also, the combination of
parameters in the cyclical component of output, yt, combined with a proper choice of prior
distribution, ensures that this term is stationary. In order to estimate the model, it is necessary
to specify prior distributions for α1, α2, ρZ, the standard deviation σZT , and the ratio of the
standard deviations σZC/σZT and (σZT +σZC)/σy. The use of priors on the ratio of the volatility
of shocks simulates a similar role played in the HP ﬁlter by the parameter characterizing the
signal-to-noise ratio of the trend. It is also important to take a stance on the steady state growth
of potential output, characterized by log ZZ
ss, given the signiﬁcant decrease in average GDP per
capita growth after 2014. It is assumed here that the decrease in GDP growth after 2014 is the
result of a very persistent change in productivity growth, with a slow convergence towards the
long run growth average (log ZZ
ss) observed between the end of 2001 and 2013Q4. Table 4 shows
the deﬁnition of the priors and the posterior evaluated with the last half of 200,000 draws using
the Metropolis-Hastings algorithm.
Table 2: Estimated Parameters
Param.
Prior
Prior
Prior
Posterior
Posterior
90% HPD
90% HPD
Distribution
Mean
StD
Mean
StD
Inf. Limit
Sup. Limit
α1
Beta
0.8
0.1
0.836
0.085
0.708
0.967
α2
Beta
0.5
0.2
0.841
0.103
0.693
0.981
ρZ
Beta
0.9
0.01
0.931
0.009
0.917
0.945
σZT
Inv.Gamma
5
inf
0.495
0.043
0.421
0.560
σZC/σZT
Gamma
20
1
16.903
0.914
15.337
18.320
(σZT + σZC)/σy
Gamma
10
1
4.308
0.602
3.305
5.286
Figure 2 shows the evolution of potential output with conﬁdence sets based on moments of
the posterior distribution and the estimated output gap. Notice that the conﬁdence sets around
the potential output and the output gap are quite small.
Figure 2: Log per capita output trend and gap – Median and conﬁdence sets (68% and 95%)
Additional exercises based on recursive estimation of the output gap, available upon request,
39

shows that the volatility of the output gap at the end of the sample used for estimation is
signiﬁcantly smaller than the one observed when using the HP ﬁlter. This is a very important
property of the estimated output gap considering the use of the model for forecasting exercises.
3.3
Additional restrictions for the estimated model
The model, as described in subsection 2.2, is characterized by ﬁrms in diﬀerent sectors manufac-
turing goods in order to satisfy speciﬁc demand for goods. A complete characterization of these
sectors would require the existence of data, both in cross-section and in time series dimensions, to
pin down all the sector-speciﬁc parameters. The lack of sector-speciﬁc data resulted in parameter
identiﬁcation problems during the model estimation. In order to minimize these problems, a few
simpliﬁcations were made imposing additional restrictions on parameters of the model.
First, the lack of information on the share of imports to produce speciﬁc goods resulted in a
simpliﬁcation of the demand for imports in ﬁrms in the second stage of production. It is assumed
that the functional form characterizing the aggregation of domestic and imported goods is the
same across sectors. Consequently, the proportion of domestic goods, the elasticity of substitution
across imported and domestic goods, and the function characterizing the adjustment cost related
to imports, are all the same across sectors:
ϖI = ϖCD = ϖX,
ϵI = ϵCD = ϵX,
ϑM
I
= ϑM
CD = ϑM
X
Also, with respect to the demand of imported goods, the sectoral adjustment costs for imports
is completed with a single common shock ZM
t , resulting in the following restrictions:
ZM
I,t = ZM
CD,t = ZM
X,t = ZM
t
The lack of references with respect to working capital constraints faced by ﬁrms in Brazil op-
erating in international markets, combined with parameter identiﬁcation problems in estimation,
suggests another simpliﬁcation of the model, setting the constraint the same across all sectors:
ιI = ιCD = ιX
With respect to price-setting, in order to ensure convergence, the elasticity of substitution
across diﬀerentiated goods for sectors supplying goods for domestic economy is the same. This
simpliﬁcation results in the same markup over prices in steady state across sectors. For the sake
of convenience, assume prices for ﬁrms trading goods with the rest of the world also face the
same markup over prices:
ϵP
CD = ϵP
I = ϵP
G = ϵP
X = ϵM
Also related to the price setting process, it is assumed that price-setting in sectors supplying
goods for domestic economy faces the same exogenous markup shifts. This assumption avoids an
40

excessive number of ad-hoc cost-push shocks aﬀecting the model, especially considering that only
one of the sectoral prices is observed during estimation. Therefore, ZP
t
is the same for sectors
CD, I and G.
3.4
Priors, posteriors and SMC estimation
The model uses SMC methods to infer about the posterior distribution of the parameters. The
estimation is based on Cai et al. (2021)[14]. The use of the MH algorithm proved diﬃcult given
the size of the model, both in terms of the number of state variables and the number of observed
variables. The posterior distribution showed signiﬁcant irregularities, leading to very sensitive
results after small changes in the priors under the MH algorithm. The ability of the SMC method
proposed in Cai et al. (2021)[14] to slowly incorporate information from the dataset, resulting
in a more complete evaluation of the posterior distribution of parameters, helped in stabilizing
the results, even in the presence of a very irregular posterior distribution.
The main idea of the method described in Cai et al. (2021)[14] is to slowly incorporate infor-
mation to the estimation, starting from a known distribution, using bridge distributions to reach
a complete characterization of the objective function – here, the posterior distribution of param-
eters. The estimation starts with 30,000 independent draws from the prior distribution, adding
more weight to the likelihood as the independent draws move towards the relevant regions of the
tempered posterior distribution. The independent draws move on the tempered likelihood based
on MH draws, but the move does not depend on the computation of modes of the distribution.
Once the weight of the likelihood equals the prior weight, the resulting draws characterize the
posterior distribution. Note that, since each draw is independent of each other, a signiﬁcant
degree of parallelization of the algorithm can be achieved21.
In order to discuss the prior distributions used in estimation, it is useful to split the set of
parameters in the model in four groups: calibrated parameters and ratios – not estimated in
the model; steady state parameters, related to average moments on data that parameters should
match; endogenous parameters, related to the dynamics of the model; and exogenous parameters,
associated with the volatility and persistence of exogenous shocks. This classiﬁcation and the
procedure for estimation is closely related to Del Negro and Schorfheide (2008)[25]. The prior
distributions are completed by a set of the so-called “system priors”, discussed in Andrle and
Benes (2013)[7] and Andrle and Plaˇsil (2018)[8].
Calibrated parameters not estimated in the model include the inﬂation target, the long run
nominal interest rate and productivity growth. It also includes long run shares of GDP compo-
nents and the average unemployment and participation rates in sample. The inclusion of labor
taxes in the model demands an additional restriction, calibrating the share of labor taxes rev-
enues on total taxation. This number is available in Azevedo and Fasolo (2015)[10]. Also, the
share of monitored prices on the CPI, weightA, is not the same as parameter ϖA, which is the
21For this paper, likelihood computation of the draws was performed with signiﬁcant gains on a GPU, while
the model solution was distributed across the diﬀerent CPU cores available.
41

share of monitored ﬁrms on the domestic production of the consumption good. Parameter ϖA
is computed given the share of monitored prices on the CPI, weightA, and the share of domestic
input in production, ϖH. The share of ﬁrms in sector A not allowed to optimize prices, θA, is
set during estimation to a value arbitrarily close to 1, as the calibrated value creates a unit root
in the structural model. Table 3 summarizes the calibrated parameters.
Table 3: Calibrated Parameters and Steady State Values
Parameter
Value
Description
Parameter
Value
Description
ΠC
ss
1.0450.25
Inﬂation
UL
ss
0.095
Unemployment
Rss
1.0850.25
Interest rates
Lss
0.62
Participation rate
Π∗
ss
1.0200.25
Foreign inﬂation
N
0.3
Overhead labor
R∗
ss
1.0300.25
Foreign interest rate
ϖRT
0.2
Share of RT households
ZZ
ss
1.0200.25
Productivity growth
ϵP
11
EoS across goods
σ
1.0001
Intertemporal substitution
weightA
0.27
Share monitored prices on CPI
sI
0.183
Investment/GDP
Sy
ss
0.016
Primary Result/GDP
sG
0.171
Government spending/GDP
σ(ϵΠ,0
t
)
0.0005
Vol. Inﬂation Target, t
sM
0.107
Imports/GDP
σ(ϵΠ,2
t−2)
0.0524
Vol. Inﬂation Target, t −2
ι
0.50
Working capital constraint
σ(ϵΠ,6
t−6)
0.0240
Vol. Inﬂation Target, t −6
ϖH
0.883
Share of domestic input
σ(ϵΠ,10
t−10)
0.0114
Vol. Inﬂation Target, t −10
τN
ss ˜
WssNss
Tss
0.335
Share of labor taxes
A few extra parameters are calibrated in the model, related to inﬂation target process and
the calibration of measurement errors in some observed variables equations. First, given that
the inﬂation target is completely exogenous to the rest of the model, the volatility of the the
shocks describing the anticipated announcement of the inﬂation target is estimated apart from
the DSGE model. This procedure allows us to estimate the volatility of the shocks assuming the
non-stationary structure of the inﬂation target (ρΠ
C = 1), which is not possible during the SMC
procedure as the second moments of the distribution of endogenous variables are necessary to
implement the “system priors”.
With respect to measurement errors in observed variables, presented in equation (76), it is
assumed the output gap, nominal wages, and the GDP components are measured with errors
following an MA(1) process. The volatility of the measurement error for the output gap, nominal
wages, and domestic components of GDP (consumption, investment, and government spending)
is estimated with a restriction that its maximum value (σx in equation (76)) is equal to 50% of
the volatility of the observed variable. Measurement errors for imports and exports are estimated
with the restriction that its maximum value is equal to the volatility of the observed variable.
Steady state parameters are parameters of the structural model closely associated with rele-
vant moments of the economy in steady state. The usual strategy is to use long run averages to
compute statistics like the labor share in the production function, the government debt-to-output
ratio or the foreign debt-to-output ratio – the “great ratios” of the economy. The procedure here
is to impose a distribution around these moments, with ﬂat priors on the structural parameters,
allowing for the structural parameters to match these moments. In the case of the estimation of
42

SAMBA, a prior is imposed for the labor share of the economy and the nominal trade balance-
to-output ratio. For the ﬁrst prior, note that the production function in equation (11) is now
characterized by a CES aggregator, instead of the special case of the Cobb-Douglas function used
in Castro et al. (2011, 2015)[17][18]. Combined with a loose prior for the elasticity of substitution
between labor and capital, the prior on the labor share helps to pin down the value of parameter
α during estimation. For the second prior, the nominal trade balance-to-output ratio helps to
pin down the foreign debt-to-output ratio in steady state, which is a critical component of the
equation describing the risk premium in foreign bonds, presented in equation (1).
Priors for endogenous parameters are fairly standard in the literature. Among the signiﬁcant
diﬀerences, parameters characterizing adjustment costs in investment, Brazilian exports, and
Brazilian imports (ϑI , ϑM and ϑM ∗) have a higher prior mean, mostly due to the signiﬁcant
gaps generated after detrending data in this observed variables. However, the estimation allows
for signiﬁcant ﬂuctuation of these parameters, as the prior standard deviation is quite large.
Prior for the inverse of the Frisch elasticity of labor supply, η, is based on the survey of micro
results in Chetty (2012)[19] Also, the parameter describing the eﬀects of net foreign assets as
a proportion to exports on the country risk premium has a very low mean, in order to avoid
excessive ﬂuctuations of the country risk premium due to shocks aﬀecting the domestic economy.
Priors for exogenous parameters follow closely the procedure in Del Negro and Schorfheide
(2008)[25], with the use of a matrix characterizing volatility and ﬁrst-order correlation of a subset
of observed variables. Priors for the volatility of exogenous shocks are not informative, while the
priors for autoregressive (AR) and moving average (MA) processes for shocks are constrained
in a tight interval22. The matrix with information on volatility and ﬁrst-order correlation of
observed variables provides targets for the volatility of shocks. At the same time, the matrix
creates a tension for the estimation of the persistence of exogenous processes: on the one hand,
the tight priors for AR and MA parameters restricts the persistence of shocks; on the other
hand, the matrix provides information about observed variables with potentially high autocorre-
lation. It is up to the information provided in the data to choose a highly persistent exogenous
shock or to ﬁt the model with an endogenous dynamics that generates the correlation in data
while keeping the exogenous process with low autocorrelation. The matrix contains information
on interest rates, real exchange rates, participation and unemployment rates, consumption, in-
vestment and government consumption growth, inﬂation of freely-set and monitored prices and
inﬂation expectations.
Finally, the “system priors” used in estimation draw on the impulse response functions (IRFs)
of a monetary policy shock from other models of Banco Central do Brasil. Speciﬁcally, IRFs of
22The exceptions for this procedure are the volatility of the measurement errors for CPI and GDP aggregation,
the process for the non-stationary productivity, and the volatility of imports’ adjustment shocks. On the non-
stationary productivity, the prior for the AR process for the shock has a higher mean and standard deviation,
while the volatility of the cyclical and temporary components are tied in a single prior, specifying a prior for the
volatility of the cyclical component and the ratio between the cyclical and temporary volatility. The volatility
of imports’ adjustment shocks was constrained in order to avoid an exaggerated role of this shock in historical
decompositions.
43

monetary policy shocks of the semi-structural models used for forecasting purposes and published
in the Inﬂation Report23 are used as a benchmark to set priors for the impact of monetary policy
shocks on inﬂation in diﬀerent periods. The priors impose independent Gaussian distributions
for three periods of the IRFs: the immediate impact of a monetary policy shock on inﬂation and
the impact of a monetary policy shock on inﬂation after one and ﬁve years. While the ﬁrst two
priors are relatively loose, providing only a benchmark for the path of monetary policy shocks,
the prior for the impact of monetary policy after ﬁve years is very tight, consistent with the
idea of policy neutrality in the long run. This conﬁguration for “system priors” is less restrictive
than the proposal from Lombardi and Nicoletti (2012)[33], who summarize the IRF in a single
quadratic function and impose a single prior on the whole proﬁle of the IRF. Here, each of the
three periods selected is associated with a single, independent prior. The set of “system priors”
here is also related to the use in Coenen et al. (2018)[20] for the ECB NAWN II model. The
authors impose a prior on the combination of parameters representing the slope of the Phillips
curve, in order to avoid very small responses from prices after a monetary policy shock. Here,
the prior is imposed directly on the IRF, allowing for a larger set of parameters to be inﬂuenced
to match these moments.
Table 4 presents the main results of estimation, in terms of the prior and posterior distribu-
tions of parameters. Figures 13 and 14 in Appendix D show the histogram of the distribution
for each parameter and the density of the marginal prior distribution used for estimation24. The
rest of this section details a few results highlighted by the choice of priors and the estimation
method.
Table 4: Estimated Parameters – Priors and Posterior Moments
Param.
Description
Prior
Posterior
Posterior
90% HPD
90% HPD
Distribution
Mean
StD
Inf.Limit
Sup.Limit
Endogenous parameters
ϵD
EoS between capital and labor
G(1.00, 0.40)
0.954
0.106
0.784
1.138
δ
Depreciation rate of capital
G(0.02, 0.005)
0.027
0.003
0.023
0.032
κ
Habit persistence
B(0.60, 0.05)
0.784
0.022
0.749
0.819
η
(Inverse) labor supply elasticity
N(1.852, 0.90)
4.481
0.304
4.006
5.001
v
Weight labor supply wealth effect
B(0.50, 0.20)
0.093
0.009
0.079
0.108
ϵCD
EoS: domestic input and imported goods
G(1.00, 0.40)
1.575
0.314
1.067
2.114
ϕ∗
V
Country risk: Risk aversion
G(0.10, 0.01)
0.035
0.004
0.028
0.042
ϕ∗
B
Country risk: NFA
G(0.002, 0.001)
0.001
0.000
0.000
0.001
ϵM
EoS: across import varieties
G(1.00, 0.40)
1.911
0.241
1.528
2.324
ϵM∗
EoS: exports and foreign inputs
G(1.00, 0.40)
0.762
0.165
0.504
1.045
ϑI
Investment adjustment cost
G(12.0, 1.00)
11.88
0.594
10.91
12.86
ϑM
Import adjustment cost
G(25.0, 2.00)
24.48
1.393
22.18
26.79
ϑM∗
Foreign import adjustment cost
G(25.0, 2.00)
25.15
1.223
23.12
27.19
θF
Calvo: freely-set price
B(0.60, 0.20)
0.573
0.021
0.533
0.603
θG
Calvo: government goods price
B(0.60, 0.20)
0.665
0.087
0.514
0.803
θI
Calvo: investment goods price
B(0.60, 0.20)
0.580
0.211
0.265
1.000
θM
Calvo: imports prices
B(0.70, 0.20)
0.632
0.048
0.552
0.709
θX
Calvo: exports prices
B(0.70, 0.20)
0.819
0.019
0.787
0.848
ωX
Export price indexation
B(0.50, 0.20)
0.442
0.035
0.384
0.500
(Continued on next page)
23See, for instance, the September-2020 Inﬂation Report box “New small-scale aggregate model with Bayesian
estimation”, the March-2021 Inﬂation Report box “New small-scale disaggregate model”, and, notably, the
December-2021 Inﬂation Report box “Revision of the small-scale aggregate model”.
24We refer to “marginal priors” as the marginal densities of the prior distribution of individual parameters in
the absence of “system priors”. It is not the same as the priors eﬀectively used in the model, as the presence of
“system priors” breaks the usual independence assumed for prior distributions across parameters
44

Table 4 (continued from previous page)
Param.
Description
Prior
Posterior
Posterior
90% HPD
90% HPD
Distribution
Mean
StD
Inf.Limit
Sup.Limit
υ1,A
Elast: monitored prices to RER
G(0.20, 0.10)
0.034
0.008
0.021
0.048
υ2,A
Elast: monitored prices to commodities
G(0.20, 0.10)
0.021
0.005
0.012
0.03
θW
Calvo: wages
B(0.60, 0.20)
0.784
0.012
0.764
0.802
ωW
Wage indexation
B(0.60, 0.20)
0.815
0.044
0.744
0.888
γR
Taylor rule: inertial parameter
B(0.50, 0.25)
0.804
0.010
0.788
0.820
γπ
Taylor rule: inflation
G(1.50, 0.75)
2.211
0.204
1.875
2.552
γY
Taylor rule: output growth
G(0.50, 0.25)
0.120
0.034
0.066
0.178
γT
AR labor taxes
B(0.30, 0.10)
0.404
0.042
0.334
0.474
γS
Elast.: labor taxes to prim. surplus
G(0.50, 0.20)
0.474
0.055
0.389
0.571
γB
Elast.: prim. surplus target to debt
G(0.02, 0.01)
0.012
0.001
0.010
0.014
γC
Elast.: import prices to commodity
G(10.0, 4.00)
15.641
1.453
13.25
18.069
“Big Ratios” – Steady state values
LS
Labor share from CES function
N(0.42, 0.02)
0.417
0.013
0.396
0.438
TB-GDP
(Minus) Trade Balance-to-GDP
G(0.01, 0.003)
0.007
0.001
0.005
0.009
ARMA structure of exogenous shocks
ρC
AR Household preference
B(0.30, 0.05)
0.581
0.043
0.509
0.651
ρI
AR Investment adj. cost
B(0.30, 0.05)
0.274
0.027
0.229
0.318
ρL
AR Labor supply
B(0.30, 0.05)
0.374
0.052
0.291
0.465
ρM
AR Import adj. cost
B(0.30, 0.05)
0.298
0.033
0.242
0.354
ρQ
AR UIP shocks
B(0.30, 0.05)
0.728
0.021
0.694
0.764
ρP
AR Price markup
B(0.30, 0.05)
0.283
0.026
0.241
0.326
µP
MA Price markup
B(0.30, 0.05)
0.310
0.024
0.269
0.350
ρW
AR Wage markup
B(0.30, 0.05)
0.301
0.030
0.252
0.350
µW
MA Wage markup
B(0.30, 0.05)
0.280
0.028
0.233
0.326
ρA
AR Monitored prices
B(0.30, 0.05)
0.269
0.025
0.229
0.310
µA
MA Monitored prices
B(0.30, 0.05)
0.338
0.024
0.297
0.378
ρD
AR Stationary productivity
B(0.30, 0.05)
0.428
0.030
0.378
0.478
ρZ
AR Perm. tech. - cyclical
B(0.95, 0.02)
0.956
0.005
0.947
0.965
µR
MA Monetary policy shocks
B(0.30, 0.05)
0.421
0.035
0.363
0.479
ρB
AR Domestic risk premium
B(0.30, 0.05)
0.293
0.034
0.237
0.350
ρB∗
AR Country risk premium
B(0.30, 0.05)
0.535
0.040
0.470
0.603
ρT L
AR Lump sum taxation
B(0.30, 0.05)
0.405
0.041
0.341
0.478
ρG
AR Government spending
B(0.30, 0.05)
0.262
0.029
0.215
0.310
ρS
AR Primary surplus target
B(0.30, 0.05)
0.684
0.041
0.618
0.753
ρP ∗
AR Export price markup
B(0.30, 0.05)
0.299
0.032
0.248
0.352
µP ∗
MA Export price markup
B(0.30, 0.05)
0.297
0.029
0.251
0.346
ρQM
AR Import price
B(0.30, 0.05)
0.538
0.034
0.484
0.596
ρM∗
AR World import demand
B(0.30, 0.05)
0.295
0.032
0.241
0.349
Volatility of exogenous shocks
σC
St.D. Household preference
Uniform
5.393
0.428
4.745
6.071
σI
St.D. Investment adj. cost
Uniform
3.244
0.177
2.957
3.537
σL
St.D. Labor supply
Uniform
0.962
0.296
0.477
1.457
σM
St.D. Import adj. cost
IG(0.20, 0.10)
0.173
0.039
0.116
0.243
σQ
St.D. UIP shocks
Uniform
2.419
0.158
2.159
2.678
σP
St.D. Price markup
Uniform
3.625
0.424
2.869
4.308
σW
St.D. Wage markup
Uniform
74.46
8.562
60.60
89.56
σA
St.D. Monitored prices
Uniform
1.495
0.062
1.395
1.598
σD
St.D. Stationary productivity
Uniform
0.662
0.040
0.597
0.728
σZC /σZT
Ratio Perm. tech. shocks
G(1.00, 0.20)
0.481
0.061
0.380
0.584
σZC
St.D. Perm. tech. - cyclical
IG(0.20, Inf)
0.296
0.021
0.262
0.332
σR
St.D. Monetary policy shocks
Uniform
0.225
0.011
0.207
0.244
σB
St.D. Domestic risk premium
Uniform
0.321
0.179
0.054
0.636
σB∗
St.D. Country risk premium
Uniform
0.982
0.151
0.729
1.232
σG
St.D. Government spending
Uniform
0.922
0.052
0.838
1.009
σT
St.D. Labor taxation
Uniform
1.093
0.144
0.856
1.319
σT L
St.D. Lump sum taxation
Uniform
16.51
1.340
14.34
18.75
σS
St.D. Primary surplus target
Uniform
1.714
0.140
1.479
1.945
σP ∗
St.D. Export price markup
Uniform
93.51
18.35
65.08
127.5
σQM
St.D. Import price
Uniform
5.156
0.369
4.556
5.790
σM∗
St.D. World import demand
Uniform
60.17
7.697
47.00
73.30
σCP I
St.D. CPI aggregation shock
IG(0.05, Inf)
0.113
0.007
0.102
0.124
σagg,Y
St.D. GDP aggregation shock
IG(0.05, Inf)
0.480
0.052
0.396
0.568
Observed variables: Measurement error
µme,Y
MA(1) - M.E. Output gap
B(0.50, 0.25)
0.722
0.129
0.495
0.920
µme,C
MA(1) - M.E. Consumption
B(0.50, 0.25)
0.453
0.046
0.376
0.528
µme,G
MA(1) - M.E. Gov. spending
B(0.50, 0.25)
0.543
0.089
0.410
0.702
µme,I
MA(1) - M.E. Investment
B(0.50, 0.25)
0.713
0.067
0.607
0.830
µme,X
MA(1) - M.E. Exports
B(0.50, 0.25)
0.316
0.055
0.227
0.408
µme,M
MA(1) - M.E. Imports
B(0.50, 0.25)
0.514
0.034
0.456
0.571
µme,W
MA(1) - M.E. Nominal wages
B(0.50, 0.25)
0.558
0.017
0.530
0.586
σY
St.D. M.E. Output gap
B(0.50, 0.25)
0.014
0.006
0.004
0.025
σC
St.D. M.E. Consumption
B(0.50, 0.25)
0.938
0.032
0.882
0.985
σG
St.D. M.E. Gov. spending
B(0.50, 0.25)
0.731
0.095
0.569
0.892
(Continued on next page)
45

Table 4 (continued from previous page)
Param.
Description
Prior
Posterior
Posterior
90% HPD
90% HPD
Distribution
Mean
StD
Inf.Limit
Sup.Limit
σI
St.D. M.E. Investment
B(0.50, 0.25)
0.975
0.014
0.950
0.995
σX
St.D. M.E. Exports
B(0.50, 0.25)
0.650
0.056
0.558
0.744
σM
St.D. M.E. Imports
B(0.50, 0.25)
0.899
0.037
0.836
0.961
σW
St.D. M.E. Nominal wages
B(0.50, 0.25)
0.986
0.008
0.972
0.997
Note: Prior distribution described as “Prior(mean, std)”, where “Prior” is the distribution used, “(mean, std)” are the first two moments. List
of distributions: B – Beta distribution; G – Gamma distribution; IG – Inverse-Gamma distribution; N – Gaussian distribution; Unif –
Uniform (positive values);
As it is usual in the estimation of DSGE models, a few parameters presented identiﬁcation
issues, where the surface of the likelihood around these parameters is essentially ﬂat, resulting in
signiﬁcant weight to the prior deﬁnition in order to compute the posterior distribution. Notably,
some of the parameters characterizing the AR(1) process of exogenous shocks and the parameters
characterizing adjustment costs in investment, Brazilian exports, and Brazilian imports (ϑI ,
ϑM and ϑM ∗) seem to be highly inﬂuenced by the prior choice, as the central moment of each
distribution is close to the mode of the marginal prior distribution. However, in all these cases,
measures of dispersion of the posterior distribution seem to be more concentrated, compared
to the marginal prior, showing the likelihood still is capable to provide some information about
structural parameters.
Compared to Castro et al.
(2011, 2015)[17][18], estimates for the mean of the posterior
of habit persistence (κ) is slightly higher in this version of the model.
On the other hand,
parameters on interest rate inertia (γR) and the sensitivity to inﬂation in the Taylor rule (γπ)
are quite similar. These are processes quite comparable across the diﬀerent versions of the model,
using the same dataset with updated samples. Parameters characterizing the wage Phillips curve
– Calvo wages (θW ) and wage indexation (ωW ) – have a higher posterior. However, not only
the labor market structure diﬀers, but also data on labor market is now based on a new survey
provided by IBGE, as discussed before. It is also hard to make inference about Calvo parameters
characterizing prices, as the model here adopts a conventional indexation mechanism, based on
past inﬂation and not on the inﬂation target, as in the original model.
The strategy of choosing tight priors for the autoregressive process, and combining it with
a matrix with information on moments of observed variables, resulted in only ﬁve exogenous
processes with AR(1) coeﬃcient above 0.5, not counting the estimate for the cyclical component
of non-stationary productivity, whose prior has a mean of 0.95. Two of those processes were
expected to have a high AR(1) process, as they are associated with observed ﬁnancial variables:
UIP shocks (ZQ
t ) and country risk premium shocks (ZB∗
t
). The other shocks with relatively
high persistence are household preference shocks, import price shocks, and the primary surplus
target shock. It is a stark contrast to Castro et al. (2011, 2015)[17][18], where eleven shocks
(not counting the shock to the inﬂation target, which is calibrated here) have estimated AR(1)
coeﬃcient above 0.5. Thus, compared to the original model, it is expected that the match of
persistence observed in data becomes more based on the endogenous dynamic of the model, and
not on exogenous disturbances.
46

One critical feature for the dynamics of the model exposed by the estimation procedure is re-
lated to the evolution of investment prices. The SMC procedure captured a bi-modal distribution
for the Calvo parameter of the Phillips curve of investment prices: one peak of the distribution
associated with a low value of θI combined with another peak of θI very close to one. As it will
be described in section 4, this posterior distribution aﬀects the evaluation of the transmission of
monetary policy and exchange rate shocks to investment. Figure 3 presents the surface ﬁgure
relating θI and the parameter characterizing the adjustment cost of investment, ϑI, together
with the marginal densities of each parameter. It highlights the importance of the SMC method
to bring stability to the estimation, as the conventional Metropolis-Hastings algorithm could
potentially target only one of the modes, instead of showing the entire posterior distribution.
Figure 3: Estimation: Prior and Joint Posterior Distribution of Parameters
-3.83
-3.828
16
-3.826
104
Posterior
14
-3.824
0.8
I
-3.822
0.6
12
I
0.4
10
0.2
0.5
1
1.5
Prior Density
I
0.2
0.4
0.6
0.8
0
500
1000
1500
Histogram - Posterior
0
0.1
0.2
0.3
0.4
0.5
Prior Density
I
5
10
15
20
0
1000
2000
3000
4000
Histogram - Posterior
The ﬁgure shows the joint posterior distribution of parameters θI and ϑI in the left panel, together with the
marginal histogram and the prior density for each parameter in the right panel.
It is important also to understand the role of “system priors” in model estimation. Figure
4 shows, for a few parameters, the histogram of the simulated marginal prior distribution, the
histogram of the prior distribution assuming the presence of “system priors”25, and the histogram
of the posterior distribution. The ﬁrst row of plots presents parameters characterizing the Taylor
rule. While the marginal prior suggests a large variance for the distribution of the parameter
25In order to simulate the parameter distribution under “system priors”, the SMC method used in estimation
is applied again, but without the computation of the likelihood. Thus, the SMC integrates the set of independent
marginal priors for each parameter with the “system priors” imposed on large ratios, exogenous processes and
IRFs of monetary policy.
47

describing interest rate inertia (γr), the use of “system priors” provides a signiﬁcant support
for high interest rate inertia in the model. “System priors” also provide more weight to higher
interest rate sensitivity to inﬂation expectations (γπ), while they are neutral with respect to the
response of interest rates to output growth (γy). The second row of plots presents parameters
associated with the pricing mechanism of the CPI, both for freely-set and monitored prices. For
all cases, the use of “system priors” concentrated the support of the prior distribution closer
to the mode of the marginal density, reducing the probability of extreme values allowed by
marginal density. The third row of plots shows that the eﬀects of “system priors” over the prior
distribution of parameters governing the ARMA process of exogenous shocks for freely-set prices
and interest rates are quite small. The simulated distribution is very similar to the density of the
marginal prior, both in terms of the mode and the dispersion. Thus, the use of “system priors”
helped shaping the posterior distribution of endogenous parameters of the model in terms of CPI
pricing and monetary policy.
Figure 4: Estimation: Marginal Priors, “System Priors” and Posterior Distribution
0.2
0.4
0.6
0.8
1
1.2
0.2
0.4
0.6
0.8
0
1000
2000
Histograms
0.1
0.2
0.3
0.4
0.5
1
2
3
4
5
6
0
500
1000
1500
2000
0.5
1
1.5
Prior Density
0.5
1
1.5
2
0
500
1000
1500
2000
0.5
1
1.5
0.2
0.4
0.6
0.8
0
1000
2000
3000
Histograms
1
2
3
4
0.2
0.4
0.6
0.8
0
500
1000
1500
2000
1
2
3
4
Prior Density
0.2
0.4
0.6
0.8
0
500
1000
1500
2000
2
4
6
0.2
0.3
0.4
0.5
0
500
1000
1500
2000
Histograms
2
4
6
0.2
0.3
0.4
0.5
0
500
1000
1500
2000
2
4
6
Prior Density
0.2
0.3
0.4
0.5
0
500
1000
1500
2000
Posterior
System Prior
Marginal Prior
The ﬁgure shows the marginal prior density and the simulated posterior distribution and “system prior” distri-
bution of selected parameters.
4
Moments, IRFs and Shock Decomposition
This section presents the main properties of the model in terms of relevant moments, impulse
response functions, and shock decompositions, given the estimated parameters from the previous
section. It is worth noting that the use of Sequential Monte Carlo methods, as described before,
provides a signiﬁcant improvement in the assessment of uncertainty with respect to results. As it
48

will become clear ahead, SMC methods helped highlighting how the irregularities of the posterior
distribution translated in higher uncertainty with respect to some characteristics of the model.
4.1
Moments
Table 5 compares the second moments (standard deviation and ﬁrst-order autocorrelation) of the
model with the data used in estimation. Considering the number of observed variables included
in the model, results can be considered good in terms of second moments. The table highlights
the information on domestic variables (thus, the ﬁt of the structural VAR and the exogenous
equation for the inﬂation target are not included in the table) and the data associated with
nominal variables is detrended by the inﬂation target. In a general perspective, the model does a
good job matching second moments of GDP and its components and also the volatility of prices.
The model has mixed results in terms of labor market variables but misses the volatility of ﬁscal
variables.
Table 5: Moments of Observed Variables
Observed Variable
Standard Dev.
Autocorrelation
Data
Model
95% CI
Data
Model
95% CI
CPI inﬂation
0.90
0.60
[0.56 0.65]
0.62
0.39
[0.34 0.44]
Monitored prices inﬂation
1.58
1.45
[1.35 1.57]
0.41
0.03
[-0.02 0.10]
Free prices inﬂation
0.88
0.72
[0.67 0.79]
0.56
0.26
[0.22 0.32]
Inﬂation expectations
1.18
0.87
[0.78 0.99]
0.77
0.78
[0.75 0.81]
Output gap
1.32
5.18
[4.15 15.7]
0.73
0.98
[0.96 1.00]
Output growth
1.17
1.13
[1.04 1.24]
0.34
0.01
[-0.08 0.10]
Consumption growth
1.20
1.15
[1.05 1.28]
0.30
0.27
[0.21 0.32]
Investment growth
3.89
3.36
[3.13 3.63]
0.30
0.27
[0.21 0.32]
Government spending growth
1.25
1.25
[1.14 1.37]
-0.42
-0.24
[-0.29 -0.17]
Imports growth
5.17
4.80
[4.40 5.17]
0.19
0.08
[-0.05 0.21]
Exports growth
4.60
3.96
[3.50 4.49]
-0.28
-0.09
[-0.21 0.06]
Export prices
4.94
4.85
[4.48 5.30]
0.43
0.48
[0.42 0.53]
Import prices inﬂation
3.03
5.14
[4.32 6.06]
0.45
-0.16
[-0.21 -0.10]
Unemployment rate
1.68
1.76
[1.60 1.94]
0.97
0.83
[0.80 0.85]
Participation rate
0.41
2.08
[1.60 2.82]
0.89
0.99
[0.99 1.00]
Nominal wage growth
0.84
0.77
[0.74 0.80]
0.10
0.41
[0.36 0.46]
Real exchange rate
18.7
31.9
[28.5 35.7]
0.94
0.98
[0.97 0.98]
Interest rates
4.24
2.56
[2.38 2.80]
0.94
0.91
[0.90 0.92]
Risk premium
0.95
1.67
[1.23 2.06]
0.91
0.78
[0.73 0.83]
Primary result target
2.37
22.0
[10.4 59.4]
0.96
1.00
[0.99 1.00]
Primary result
2.36
8.31
[4.03 23.1]
0.82
0.96
[0.81 0.99]
Note: nominal variables presented as deviation from the inﬂation target. Interest rates are annualized.
Observing the ﬁrst four lines of the table, describing the second moments of prices, the model
underestimates the autocorrelation of domestic prices. The volatility of CPI and its components
is overall well matched, despite a small underestimation of the volatility of freely-set prices.
Consistent with the underestimation of the volatility of CPI inﬂation, nominal interest rates and
inﬂation expectations also have lower volatility in the model compared to data, but a very good
match in terms of autocorrelation.
The model does a good job matching second moments of GDP and its components. Notably,
49

it does a very good job approximating the negative autocorrelation of exports and government
spending growth. It should be noted that the model representation of these observed variables
includes measurement errors. However, for both exports and government spending growth, mea-
surement errors do not have the same volatility of the observed variable. Thus, measurement
errors do not seem to heavily inﬂuence the matching of the negative autocorrelation.
With
respect to the output gap, it is curious that the model misses on both the volatility and the
autocorrelation, but it also did not rely on the measurement error to improve model ﬁt, as seen
in section 3.4.
In terms of labor market variables, the model has a good ﬁt on the second moments of
unemployment. The autocorrelation of wages in the model is overestimated. Given that wage
markups have the same ARMA(1,1) process used in the markup of domestic prices, it was
expected a better ﬁt of the sample autocorrelation. However, given that wage markups play a
key role in explaining unemployment in the Gal´ı, Smets and Wouters (2011)[28] framework, it is
possible that the estimation process faced some tension between matching the autocorrelation of
wages and unemployment. The model misses on moments of participation rate. The near unit
root observed in simulated moments is a direct consequence of the two non-stationary processes
included in the inﬂation target equation and the monitored prices’ Calvo mechanism. The non-
stationary mechanism in monitored prices, speciﬁcally, results in a very slow convergence of
the relative price of these goods, altering households’ aggregate consumption decisions and, by
consequence, the labor supply26.
4.2
IRFs: Monetary Policy and Exchange Rate Pass-Through
Figure 5 shows the impulse response functions (IRFs) of a monetary policy shock. As expected,
prices fall immediately, with maximum eﬀects on CPI inﬂation reached after one year. Also,
consistent with the price sectoral dynamics proposed in the model, eﬀects on freely-set prices
are more signiﬁcant and react faster to the monetary policy shock, when compared to monitored
prices. Domestic GDP falls and unemployment increases almost at the same proportion. Worth
also noting that, despite a signiﬁcant share of RT households in the model, consumption falls
proportionally less than output after the shock.
Quantitatively, there is a small impact of monetary policy on inﬂation, which is apparently
in line with the so-called “ﬂat Phillips Curve” hypothesis. The hypothesis states that inﬂation
in the last 30 years has become less responsive to measures of economic activity usually included
in the New Keynesian Phillips Curve. See empirical evidence in Del Negro et al. (2020)[24],
Hazell et al. (2022)[30], among others. In Coenen et al. (2018)[20], there is a “system prior”
imposed on the non-linear combination of structural parameters representing the slope of the
Phillips Curve. The posterior implies a coeﬃcient around 0.007, slightly higher than the value
obtained (0.005) in the previous version of the ECB model27.
26Preliminary tests using the same Calvo parameter estimated for freely-set prices in monitored prices resulted
in autocorrelation for participation rate closer to the observed in data.
27Obviously, other structural changes in the model might also have aﬀected the estimate of this parameter,
50

Figure 5: IRF: Monetary Policy Shock
The ﬁgure shows the median impulse response functions (black line), the 95% credible intervals (CI, shaded area)
for the DSGE model.
There is, however, a disconnection between the estimated parameters of the model for Brazil
and the slope of the Phillips Curve for freely-set price ﬁrms in Brazil. Linearization of conditions
(29)-(33) results in the following expression for the slope of the Phillips Curve (SPCF ):
SPCF = (1 −θF β(ZZ
ss)1−σ)(1 −θF )/θF
Figure 6 shows the histogram of the slope of the Phillips curve, based on the estimation of the
model, comparing with the central value of the estimation in Coenen et al. (2018)[20] and the
histogram of the estimate of both the VAR and the DSGE models in Del Negro et al. (2020)[24]
for the period before 199028. It is clear that the Phillips Curve for freely-set price ﬁrms is much
more responsive to changes in economic activity, but the eﬀects of a monetary policy shock on
inﬂation are in line with the literature.
compared to NAWN I.
28Histograms for both VAR and DSGE models for the period after 1990 showed very little variance around
zero, making diﬃcult any comparison.
51

Figure 6: Histogram: Slope of Phillips Curve – Freely-Set Price Firms
The key to understand this apparent disconnection is the impact of monetary policy shock
on economic activity. Domestic GDP, household consumption, and specially investment, show
signiﬁcantly smaller responses to monetary policy shocks, compared to other papers. It is well
known from the literature that credit and ﬁnancial markets in the Brazilian economy are distorted
by the existence of earmarked credit, where the government provides loans to ﬁrms based on
criteria that are almost totally insensitive to the short-run interest rates set by the Central Bank.
Indeed, Bonomo and Martins (2016)[12] provided empirical evidence using ﬁrm-level data. They
documented that changes in the policy rate have smaller eﬀects on the level of employment for
ﬁrms with more access to earmarked and government-owned banks loans.
Exchange rate pass-through is evaluated based on the IRFs from the shock included in the
uncovered interest parity (UIP) condition of the model, derived from the ﬁrst order condition of
optimizing households with respect to foreign bonds. The UIP shock should be interpreted as an
exogenous intervention that temporarily moves the real exchange rate away from its fundamental
value based on the states of the economy. Figure 7 shows the impact of a deviation of 100bps
of the real exchange rate from the UIP condition and the impacts on the domestic economy.
The estimated pass-through to CPI inﬂation is immediate, but quite low. The propagation of
the shock results in higher inﬂation, reaching 3.5bps over 12 months. The impact on economic
activity is also quite small, and quite uneven across diﬀerent components of aggregate demand:
considering the 95% credible intervals, impact on GDP is not signiﬁcant. However, household
consumption reduces in the short run, while exports grow almost in the same proportion. Imports
are quite sensitive to the shock, with a strong fall over one year, almost four times the size of the
change in exports. Unemployment shows a small reduction over the ﬁrst year after the shock.
Compared to Castro et al. (2011, 2015)[17][18], the eﬀects of real exchange rate shocks as
52

Figure 7: IRF: Real Exchange Rate Shock
The ﬁgure shows the median impulse response functions (black line), the 95% credible intervals (CI, shaded area)
for the DSGE model.
discussed here are more muted, both in terms of prices and economic activity. The same shock
would result in an increase in CPI around 7bps over 12 months. The response of output is muted
here over the whole horizon, while in Castro et al. (2011, 2015)[17][18] GDP falls in the long
term.
Related to the response of investment to a monetary policy shock, Castro et al.
(2011,
2015)[17][18] ﬁnd a slightly higher response for output, consumption and inﬂation, compared to
results here, but a signiﬁcantly higher response for investment. The eﬀect on economic activity
is ampliﬁed in other estimated DSGE models for Brazil with ﬁnancial frictions29. However, all
these models use data for the period before the 2014 crisis. Indeed, Bonomo et al. (2015)[11]
showed that government-driven credit had an important role in countervailing the private credit
crunch in Brazil during the ﬁnancial crisis and that government credit concessions continued
to expand after the economy recovered. This behavior has the potential to reduce the eﬀect
29See, for instance, Carvalho, Castro and Costa (2014)[16], among others.
53

of monetary policy shocks on economic activity in recent years because interest rates on ear-
marked loans are lower than market interest rates, which tend to closely follow the policy rate.
Ramos-Tallada (2015)[36] reached a similar conclusion concerning supply-driven credit responses
to monetary shocks. The relationship between changes in the economic environment and the in-
ﬂation sensitivity to monetary policy is not a feature of emerging markets since Pancrazi and
Vukoti´c (2019)[35] showed similar behavior for the US economy.
4.3
IRFs: Foreign Shocks
One of the signiﬁcant changes of this version of the model, compared with Castro et al. (2011,
2015)[17][18], is the use of a structural VAR to characterize shocks from the rest of the world
to the domestic economy. This section compares the IRFs for domestic variables of the model
using the structural VAR with IRFs using an exogenous AR(1) process calibrated to match the
persistence of shocks estimated in Castro et al. (2011, 2015)[17][18]. Considering the diﬀerent
samples used in the estimation here and in Castro et al. (2011, 2015)[17][18], the calibration
adopted for the exercise keeps for each observed variable the variance estimated in the structural
VAR, but eliminates the covariance and the cross-terms for other variables across equations. The
objective of the exercise is to understand the gains in using a structural VAR to estimate the
transmission process of foreign shocks to the domestic economy. It is well documented in Justini-
ano and Preston (2010)[31] the diﬃculties of small open-economy models to generate signiﬁcant
impact from foreign shocks to the domestic economy. Though structural models have a hard time
in matching international co-movement, a multivariate approach to the foreign block considers
the interaction between demand, supply, and monetary policy in the world economy.
More-
over, a structural VAR leads to the identiﬁcation of shocks with a clear economic interpretation
compared with simple autoregressions, in which a particular shock does not propagate to other
international variables of interest. The exercise here provides some evidence on the importance
of second round eﬀects to amplify the impact of foreign shocks on the Brazilian economy. In this
context, a particular shock contemporaneously aﬀects all international variables that interact
with the domestic economy, enriching the propagation mechanism of that shock.
The ﬁrst example on the diﬀerence of representing the rest of the world as a VAR is presented
in ﬁgure 8, with the IRF of a monetary policy shock from the rest of the world. A contractionary
shock of 100bps generates, by the feedback rule estimated in the structural VAR, a persistent
process where nominal interest rates increase 300bps after six periods. Consequently, the output
gap of the rest of the world moves to negative values. This is in sharp contrast with the AR(1)
process, where, by construction, the increase in nominal interest rates does not aﬀect the world’s
output gap. The impact in the domestic economy, in both cases, starts with a real exchange rate
depreciation, but the expectations of further nominal interest rates increase generate a larger
depreciation on impact in the model with the VAR. According to Azad and Serletis (2019)[9],
this pattern of exchange rate change after a foreign monetary policy shock is common to other
emerging economies with inﬂation targeting regimes. The exchange rate depreciation combined
54

with a negative output gap in the rest of the world generates a tension for domestic monetary
policy: on the one hand, the pass-through of the exchange rate tends to increase inﬂation; on the
other hand, the negative world’s output gap combined with the increase in production costs from
the exchange rate devaluation reduces domestic output. The estimated Taylor rule suggests an
initial reduction in nominal exchange rates. However, with the increase in inﬂation, real interest
rates rise to stabilize prices.
Figure 8: IRF: Foreign Monetary Policy Shock
The ﬁgure shows the median impulse response functions (black line), the 95% credible intervals (CI, shaded area)
for the DSGE model, and the impulse response function for the model without the structural VAR (blue line).
Parameters of the structural VAR are kept constant across SMC particles.
Results with the AR(1) process follow the expected proﬁle of ﬁrst round eﬀects in the model:
the exchange rate depreciation increases domestic prices, reducing domestic demand and resulting
in an increase of domestic nominal interest rates.
However, the magnitude of the responses
suggests the second-order eﬀects are relevant to characterize a signiﬁcant transmission of foreign
monetary policy shocks to the Brazilian economy.
The second example, in ﬁgure 9, shows the IRF of an increase in world’s demand, represented
by an exogenous shock that increases the world’s output gap by 100bps. In the model with the
55

structural VAR, the increase in demand is followed by an increase in foreign interest rates.
The response of foreign interest rates creates a new tension for domestic variables, as the real
exchange rates depreciates. It is a stark contrast with the responses from the AR(1) process,
where the increase in world’s demand generates a trade surplus, followed by real exchange rate
appreciation. The exchange rate depreciation in the model with the structural VAR ampliﬁes the
impact on domestic inﬂation, forcing domestic interest rates to increase. The estimated Taylor
rule suggests the increase in interest rates is enough to generate a small contraction of domestic
real GDP, oﬀsetting the increase in foreign demand for Brazilian exports.
Figure 9: IRF: Foreign Demand Shock
The ﬁgure shows the median impulse response functions (black line), the 95% credible intervals (CI, shaded area)
for the DSGE model, and the impulse response function for the model without the structural VAR (blue line).
Parameters of the structural VAR are kept constant across SMC particles.
Eﬀects of the model with the AR(1) diﬀer not only quantitatively, but also with respect to the
sign of responses, especially for domestic economic activity. This is a consequence of the missing
tension generated from the real exchange rate depreciation in the model with the structural
VAR. Without the exchange rate depreciation, domestic interest rates do not show a signiﬁcant
increase, allowing for the business cycle of the domestic economy closely follow the rest of the
56

world, with increases in GDP and consumption and a fall in unemployment rate.
4.4
Shock Decomposition
This subsection presents the shock decomposition of three observed variables of the model: out-
put growth, CPI inﬂation and unemployment.
All variables are measured as deviation with
respect to their steady state, except CPI inﬂation, that is expressed as a deviation from the
inﬂation target at the period. Inﬂation and output are measured in annual terms. For sim-
plicity, shocks are aggregated in the following groups: demand, supply, price markups, labor
market, monetary policy, foreign shocks, and “others”. Demand shocks include the preference
shock (εC
t ), investment-speciﬁc technology shock (εI
t ), government spending shock (εG
t ), import
demand shock (εM
t ), and export demand shock (εM∗
t
). Supply shocks include all changes in ag-
gregate productivity: both shocks describing the non-stationary productivity (εZT
t
and εZC
t
) and
the stationary productivity shock (εD
t ). Price markups comprise shocks in the sectoral Phillips
curves of freely-set (εP
t ) and administered price ﬁrms (εA
t ), import prices (εQM∗
t
) and export
prices (εP ∗
t ). Labor market shocks include the labor supply shock (εL
t ) and the wage markup
shock (εW
t ). Wage markup shocks are included here due to the importance of such shocks in
characterizing the dynamics of unemployment in the Gal´ı, Smets and Wouters (2011)[28] frame-
work. Monetary policy shocks (εR
t ) characterize the deviations of interest rates from the path
projected by the Taylor rule of the model. Foreign shocks comprise all shocks from the structural
VAR (εY ∗
t , εR∗
t , εP ∗
t , εV ∗
t
, and εCO∗
t
), and the shocks to the foreign risk premium (εB∗
t ) and real
exchange rate (εQ
t ).
The ﬁrst panel of ﬁgure 10 characterizes the shock decomposition of annual GDP growth based
on the groups described above. From the supply side, it shows the change in productivity growth
observed after 2014 and highlighted before in ﬁgure 1. Overall, external shocks, monetary policy
and markup shocks play a small role in GDP growth. The ﬁrst panel also shows the increase in
GDP volatility during and after the Great Financial Crisis, in 2008. With respect to the crisis, the
model describes both the recession and the recovery as mostly demand-driven events. However,
the second panel provides more clarity about the drivers of the recession and the recovery: the
recession was characterized by negative shocks in exports and investment, while the recovery
was based on the recuperation of these components, combined with signiﬁcant positive shocks on
household consumption. With respect to the role of exports, the negative shock is a consequence
of a mismatch in data between world GDP and domestic exports: world GDP gap reached a peak
around 2003 and was in a sharp reversal even before the crisis, while Brazilian exports was still
showing signiﬁcant growth before 2008Q3. The role of the investment shock during 2008 is an
issue for models without ﬁnancial frictions, as the lack of endogenous propagation mechanisms
forces the model to give a signiﬁcant weight to the shock in order to match data.
Beyond the recovery after the Great Financial Crisis, between 2010 and 2012, the disaggrega-
tion of demand shocks in the second panel also captures other periods where exogenous stimuli
increased household consumption. In 2014, several government policies tried to stimulate credit
57

Figure 10: Shock Decomposition: Annual GDP – Deviation from Steady State
2002Q1
2004Q1
2006Q1
2008Q1
2010Q1
2012Q1
2014Q1
2016Q1
2018Q1
-8
-6
-4
-2
0
2
4
Demand
Supply
Price Markup
Labor Market
Monetary Policy
Foreign Shocks
Other
2002Q1
2004Q1
2006Q1
2008Q1
2010Q1
2012Q1
2014Q1
2016Q1
2018Q1
-2
0
2
Household Preference
Government Consumption
Investment
Demand for Imports
Demand for BRA Exports
The ﬁrst panel shows the shock decomposition of annual GDP based on the groups of shocks. The second panel
shows demand shocks from the ﬁrst panel disaggregated by their components.
markets, including lowering reserve requirements ratios for deposits that banks must hold at the
Banco Central do Brasil, both for ﬁrms and households. Another important period is the ﬁrst
semester of 2017, when the federal government allowed workers to make early withdrawals from
inactive accounts of a severance fund (FGTS, in Portuguese).
Figure 11 shows the shock decomposition of annual CPI inﬂation. Demand shocks play a
signiﬁcant role, as expected, as they include unexpected changes in both the domestic demand
for goods and the external demand for Brazilian goods. Supply shocks have a large role after 2014,
just like GDP. However, the eﬀects of the supply shocks on prices move to the usual contribution
after 2017, the opposite of GDP growth, where these shocks are still relevant. Monetary policy
was clearly in a contractionary stance from 2006 until the end of 2009, which includes the Great
Financial Crisis30. Monetary policy was expansionary between 2012 and 2014, moving back to
the contractionary stance after a signiﬁcant change in economic policy in 2015, right before the
30It is worth noting that the Monetary Policy Committee raised nominal interest rates from 11.25% to 13.75%
between March and September 2008, while acknowledging that “a severe ﬁnancial crisis in the USA and, to
a minor extent, in Europe, must be added to this adverse scenario”, according to the September 2008 MPC
meeting’s minutes.
58

2016 political crisis. Labor market shocks pressure inﬂation in both periods when unemployment
is high, at the beginning and at the very end of the sample, after 2014 (see ﬁgure 12), suggesting
wages have had problems in clearing labor markets speciﬁcally when labor demand is low –
assuming a relative stability of labor supply, observed in data on participation rate.
Figure 11: Shock Decomposition: Annual CPI Inﬂation – Deviation from Inﬂation Target
2002Q1
2004Q1
2006Q1
2008Q1
2010Q1
2012Q1
2014Q1
2016Q1
2018Q1
-4
-2
0
2
4
6
8
10
12
Demand
Supply
Price Markup
Labor Market
Monetary Policy
Foreign Shocks
Other
2002Q1
2004Q1
2006Q1
2008Q1
2010Q1
2012Q1
2014Q1
2016Q1
2018Q1
-4
-2
0
2
4
6
Price Markup
Adm Price
Real Exchange Rate
The ﬁrst panel shows the shock decomposition of annual CPI inﬂation based on the groups of shocks. The second
panel shows speciﬁc shocks from the ﬁrst panel.
Price markups move in the way proposed in the description of priors for estimation, char-
acterizing unexpected short-lived movements in prices, usually associated with unique episodes,
like unexpected changes in monitored prices, food prices and other events.
The lower panel
of ﬁgure 11 highlights the role of markups of freely-set and administered prices, and exchange
rate shocks. Again, the decomposition is consistent with well-documented episodes of temporary
price changes discussed in oﬃcial documents. As an example, the lower panel shows the unex-
pected rapid fall in inﬂation during 2003-04, considering the severe crisis that hit the economy
before the 2002 elections. The lower panel also shows the increase in administered price markups
in 2015Q1, combined with an unexpected real exchange rate devaluation, consistent with the
change in economic policy during that period. Markups of administered price remained negative
between 2012 and 2014, quickly increasing at the beginning of 2015. Another episode worth
59

noting is the sequence of positive shocks in food prices that reduced freely-set prices between
2017 and 2018.
Figure 12: Shock Decomposition: Unemployment Rate – Deviation from Steady State
2002Q1
2004Q1
2006Q1
2008Q1
2010Q1
2012Q1
2014Q1
2016Q1
2018Q1
-6
-4
-2
0
2
4
6
Demand
Supply
Price Markup
Labor Market
Monetary Policy
Foreign Shocks
Other
2002Q1
2004Q1
2006Q1
2008Q1
2010Q1
2012Q1
2014Q1
2016Q1
2018Q1
0
2
4
6
Labor Supply
Wage Markup
The ﬁrst panel shows the shock decomposition of unemployment rate based on the groups of shocks. The second
panel shows labor market shocks from the ﬁrst panel disaggregated by their components.
Figure 12 shows the decomposition of unemployment rate. It is interesting to observe, in
the higher panel, that, as expected, labor market shocks play a signiﬁcant role in unemployment
dynamics.
However, the importance of these shocks is highlighted in periods of high unem-
ployment. Other shocks usually dominate the decomposition in periods of low unemployment.
Notably, demand shocks in unemployment pretty much mirror the behavior in the decomposition
of CPI inﬂation presented before. Just as expected, periods where demand shocks raise inﬂation
are the same periods where these shocks reduce unemployment. It is remarkable, however, that
the relative importance of demand shocks in both observed variables is very similar, even in
terms of dynamics. It is interesting that the supply shocks that reduced GDP growth after 2014
took some time in aﬀecting unemployment, with most of the increase in unemployment due to
low productivity beeing observed after 2016. Foreign shocks and monetary policy shocks have a
small contribution in the decomposition. From the lower panel, of ﬁgure 12, it is worth noting
that the labor supply shocks are dominated by the wage markup shocks among the labor market
shocks. The relative stability of labor supply in the sample supports the small role of labor
60

supply shocks, especially compared to the high variance of unemployment rate.
The shock decomposition of unemployment shows the importance of the Gal´ı, Smets and
Wouters (2011)[28] in interpreting periods of high unemployment in the economy. First, in the
early part of the sample, the model is forced to reconcile low economic growth, high inﬂation,
and high unemployment. The shock decomposition suggests a combination of positive demand
shocks (focused on household consumption and investment, according to the lower panel of ﬁgure
10) with negative wage markup shocks. While both sets of shocks generate high inﬂation, wage
markup shocks are set to generate low economic activity and high unemployment between 2001
and 2006. In the second period, between 2016 and 2019 (end of the sample), the model must
adjust itself to a situation of high unemployment and low growth again, but now with declining
inﬂation. In this case, the shock decomposition suggests wage markup shocks provide inﬂation
persistence that would not be observed in an environment of low GDP growth. For both episodes,
it is worth noting that wage markups play a more prominent, truly structural role instead of
simply matching moments of wage growth in the Phillips curve.
5
Conclusion
This paper presented the current version of the SAMBA model, a DSGE model developed at the
Banco Central do Brasil. Compared to the original version, the current model presents signiﬁcant
innovations both in terms of modeling choices and estimation procedures. The new framework
characterizing the labor market, based on Gal´ı, Smets and Wouters (2011)[28], allowed for a
better description of the labor market dynamics, more appropriate when compared to the basic
framework for labor supply based on the representative agent oﬀering hours of work to ﬁrms.
Under the new framework, it is possible to incorporate information on the labor supply, in line
with the conventional information on wages and unemployment rate.
The use of a structural VAR to characterize the rest of the world also allows for an ampli-
ﬁcation of the transmission mechanism of foreign shocks to the domestic economy. It helps in
alleviating the concerns raised in Justiniano and Preston (2010)[31], as it ampliﬁes the eﬀects
from foreign observed variables in small open economy models like SAMBA. The exercises with
IRFs show a clear improvement, compared to a simple AR(1) speciﬁcation for foreign shocks.
However, the total impact of foreign shocks still seems small, especially during stress periods,
like the Great Financial Crisis, as shown in the shock decomposition.
Finally, the use of Sequential Monte Carlo methods, together with the adoption of “system
priors” not only provided stability for the estimation of the structural parameters in a large model
like SAMBA, but also oﬀered the tools for understanding the trade-oﬀs faced when matching
data moments in a complex theoretical environment. From a practical perspective, these methods
also allowed for a better use of technological resources, like GPU computing, as it improved the
possibilities of parallel implementations optimizing the estimation procedure.
The model presented here is continually developed, with several possible improvements for
61

policy analysis. With respect to estimation, it is still a challenge to incorporate information
related to the Covid-19 pandemic crisis. The usual linear-Gaussian framework for likelihood
inference based on the Kalman Filter does not seem capable of handling the extreme variations
of observed variables during 2020. With respect to model ﬁt, the structural VAR characterizing
the rest of the world provides a good benchmark for the analysis of the transmission of foreign
shocks to the domestic economy. However, the model is muted with respect to possible policy
changes associated with the lower bound of nominal interest rates observed in major economies.
Models with ﬁnancial frictions should also be considered in order to improve the model ﬁt during
crises episodes.
References
[1] FRBNY DSGE Model Documentation.
Technical report, Federal Reserve Bank of New
York, Dec. 2021.
[2] S. Adjemian, H. Bastani, M. Juillard, F. Karam´e, F. Mihoubi, W. Mutschler, J. Pfeifer,
M. Ratto, N. Rion, and S. Villemot. Dynare: Reference manual version 5. Dynare Working
Papers 72, CEPREMAP, 2022.
[3] M. Adolfson, S. Laseen, L. J. Christiano, M. Trabandt, and K. Walentin. Ramses II – Model
Description. Occasional Paper Series 12, Sveriges Riksbank, 2013.
[4] M. Adolfson, S. Laseen, J. Linde, and M. Villani. Bayesian Estimation of an Open Econ-
omy DSGE Model with Incomplete Pass-Through.
Journal of International Economics,
72(2):481–511, 2007.
[5] S. A. L. Alves and A. M. Fasolo. Not Just Another Mixed Frequency Paper. Working Paper
Series 400, Banco Central do Brasil, Research Department, 2015.
[6] M. Andrle.
What Is in Your Output Gap?
Uniﬁed Framework & Decomposition into
Observables. IMF Working Papers 2013/105, International Monetary Fund, 2013.
[7] M. Andrle and J. Benes. System Priors: Formulating Priors about DSGE Models System
Properties. IMF Working Papers 2013/257, International Monetary Fund, 2013.
[8] M. Andrle and M. Plaˇsil. Econometrics with system priors. Economics Letters, 172:134–137,
2018.
[9] N. F. Azad and A. Serletis. Monetary Policy Spillovers in Emerging Economies. International
Journal of Finance & Economics, 25(4):664–683, 2020.
[10] C. F. Azevedo and A. M. Fasolo. Eﬀective Tax Rates on Consumption and Factor Incomes:
a Quarterly Frequency Estimation for Brazil. Working Paper Series 398, Banco Central do
Brasil, Research Department, 2015.
62

[11] M. Bonomo, R. D. Brito, and B. Martins.
The After Crisis Government-Driven Credit
Expansion in Brazil: A Firm Level Analysis. Journal of International Money and Finance,
55:111–134, 2015.
[12] M. Bonomo and B. Martins. The Impact of Government-Driven Loans in the Monetary
Transmission Mechanism: What Can We Learn from Firm-Level Data?
Working Paper
Series 419, Banco Central do Brasil, Research Department, 2016.
[13] F. Brazdik, T. Hledik, Z. Humplova, I. Martonosi, K. Musil, J. Rysanek, T. Sestorad,
J. Tonner, S. Tvrz, and J. Zacek. The g3+ Model: An Upgrade of the Czech National
Bank’s Core Forecasting Framework. Technical Report 2020/7, Czech National Bank, 2020.
[14] M. Cai, M. Del Negro, E. Herbst, E. Matlin, R. Sarfati, and F. Schorfheide. Online Esti-
mation of DSGE Models. The Econometrics Journal, 24(1):C33–C58, 2021.
[15] F. Canova. The Transmission of US Shocks to Latin America. Journal of Applied Econo-
metrics, 20(2):229–251, 2005.
[16] F. A. Carvalho, M. R. Castro, and S. M. A. Costa. Traditional and Matter-of-Fact Finan-
cial Frictions in a DSGE Model for Brazil: the Role of Macroprudential Instruments and
Monetary Policy. Bank for International Settlements Working Papers 460, 2014.
[17] M. R. Castro, S. N. Gouvea, A. Minella, R. Santos, and N. F. Souza-Sobrinho. SAMBA:
Stochastic Analytical Model with a Bayesian Approach. Working Paper Series 239, Banco
Central do Brasil, Research Department, 2011.
[18] M. R. Castro, S. N. Gouvea, A. Minella, R. Santos, and N. F. Souza-Sobrinho. SAMBA:
Stochastic Analytical Model with a Bayesian Approach. Brazilian Review of Econometrics,
35(2):103–170, 2015.
[19] R. Chetty. Bounds on Elasticities with Optimization Frictions: A Synthesis of Micro and
Macro Evidence on Labor Supply. Econometrica, 80(3):969–1018, 2012.
[20] G. Coenen, P. Karadi, S. Schmidt, and A. Warne.
The New Area-Wide Model II: an
Extended Version of the ECB’s Micro-Founded Model for Forecasting and Policy Analysis
with a Financial Sector. Working Paper Series 2200, European Central Bank, 2018.
[21] V. Corbo and I. Strid. MAJA: A Two-Region DSGE Model for Sweden and its Main Trading
Partners. Working Paper Series 391, Sveriges Riksbank, 2020.
[22] P. Corrigan, H. Desgagn´es, J. Dorich, V. Lepetyuk, W. Miyamoto, and Y. Zhang. ToTEM
III: The Bank of Canada’s Main DSGE Model for Projection and Policy Analysis. Technical
Reports 119, Bank of Canada, 2021.
[23] S. M. A. Costa. Structural Trends and Cycles in a DSGE Model for Brazil. Working Paper
Series 434, Banco Central do Brasil, Research Department, 2016.
63

[24] M. Del Negro, M. Lenza, G. E. Primiceri, and A. Tambalotti. What’s Up with the Phillips
Curve? Brookings Papers on Economic Activity, 2020(1):301–373, 2020.
[25] M. Del Negro and F. Schorfheide. Forming Priors for DSGE Models (and How it Aﬀects
the Assessment of Nominal Rigidities). Journal of Monetary Economics, 55(7):1191–1208,
2008.
[26] R. M. Edge, T. Laubach, and J. C. Williams. Learning and Shifts in Long-Run Productivity
Growth. Journal of Monetary Economics, 54(8):2421–2438, 2007.
[27] C. J. Erceg, D. W. Henderson, and A. T. Levin. Optimal Monetary Policy with Staggered
Wage and Price Contracts. Journal of Monetary Economics, 46(2):281–313, 2000.
[28] J. Gal´ı, F. Smets, and R. Wouters. Unemployment in an Estimated New Keynesian Model.
In NBER Chapters, volume 26 of NBER Macroeconomics Annual 2011, pages 329–360.
NBER, 2011.
[29] J. Greenwood, Z. Hercowitz, and G. W. Huﬀman. Investment, Capacity Utilization, and
the Real Business Cycle. American Economic Review, 78(3):402–17, 1988.
[30] J. Hazell, J. Herre˜no, E. Nakamura, and J. Steinsson. The Slope of the Phillips Curve:
Evidence from U.S. States. The Quarterly Journal of Economics, 137(3):1299–1344, 2022.
[31] A. Justiniano and B. Preston. Can Structural Small Open-Economy Models Account for
the Inﬂuence of Foreign Disturbances?
Journal of International Economics, 81(1):61–74,
2010.
[32] A. Kraay and V. Nehru. When is External Debt Sustainable? The World Bank Economic
Review, 20(3):341–365, 2006.
[33] M. J. Lombardi and G. Nicoletti. Bayesian Prior Elicitation in DSGE Models: Macro- vs
Micropriors. Journal of Economic Dynamics and Control, 36(2):294–313, 2012.
[34] J. P. Medina and C. Soto. The Chilean Business Cycles Through the Lens of a Stochastic
General Equilibrium Model. Working Papers 457, Central Bank of Chile, Dec. 2007.
[35] R. Pancrazi and M. Vukoti´c. Inﬂation Sensitivity to Monetary Policy: What Has Changed
since the Early 1980s? Oxford Bulletin of Economics and Statistics, 81(2):412–436, 2019.
[36] J. Ramos-Tallada. Bank Risks, Monetary Shocks and the Credit Channel in Brazil: Iden-
tiﬁcation and Evidence from Panel Data. Journal of International Money and Finance,
55:135–161, 2015.
[37] C. M. Reinhart, K. S. Rogoﬀ, and M. A. Savastano. Debt Intolerance. Brookings Papers on
Economic Activity, 34(1):1–74, 2003.
64

[38] J. J. Rotemberg and M. Woodford. The Cyclical Behavior of Prices and Costs. In Handbook
of Macroeconomics, volume 1B, pages 1051–1135. 1999.
[39] S. Schmitt-Groh´e and M. Uribe. Closing Small Open Economy Models. Journal of Inter-
national Economics, 61(1):163–185, 2003.
[40] F. Smets and R. Wouters. Shocks and Frictions in US Business Cycles: A Bayesian DSGE
Approach. The American Economic Review, 97(3):586–606, 2007.
65

Appendices
A
The Equilibrium System
Households
1. Aggregate Consumption
˜Ct = ϖRT ˜CRT
t
+ (1 −ϖRT ) ˜CO
t
2. Aggregate Intratemporal conditions
˜CD
t = oC

QCD
t
−vC ˜Ct
eCM
t
= (1 −oC)
 QM
t
−vC eCt
3. CPI Inﬂation
ΠC
t =
h
oC(ΠCD
t
QCD
t−1)1−vC + (1 −oC)(ΠM
t QM
t−1)1−vCi
1
1−vC
4. Consumption for Rule-of-Thumb Households
˜CRT
t
= (1 −τ N
t ) ˜WtNt
5. Marginal Utility of Consumption for Optimizing Households
˜Λt = ZC
t
 
˜CO
t −κ
˜CO
t−1
ZZ
t
!−σ
6. The Euler Equation for Optimizing Households
ZC
t
 
˜CO
t −κ
˜CO
t−1
ZZ
t
!−σ
= βEtZC
t+i
 ZZ
t+1
−σ
 
˜CO
t+1 −κ
˜CO
t
ZZ
t+1
!−σ
RtSB
t
ΠC
t+1
7. Uncovered Interest Rate Parity Condition
Et
RtSB
t
ΠC
t+1
 ZZ
t+1
−σ ˜Λt+1

= Et
Qt+1
Qt
R∗
t SB∗
t
ΠC∗
t+1
 ZZ
t+1
−σ ˜Λt+1ZQ
t

8. Capital and Investment Decisions
˜ΛtQK
t = βEt
 ZZ
t+1
−σ ˜Λt+1

RK
t+1 + QK
t+1(1 −δ)

66

1
=
QK
t
QI
t

1 −ϑI
2
 
ZZ
t ˜It
ZI
t ˜It−1
−ZZ
ss
!2
−ϑI
 
ZZ
t ˜It
ZI
t ˜It−1
−ZZ
ss
!
ZZ
t ˜It
ZI
t ˜It−1


+
β
˜ΛtQI
t
Et
 ZZ
t+1
−σ ˜Λt+1QK
t+1ϑI
 
ZZ
t+1 ˜It+1
ZI
t+1 ˜It
−ZZ
ss
!  
ZZ
t+1 ˜It+1
ZI
t+1 ˜It
!2
ZI
t+1
˜Kt+1 = (1 −δ)

˜Kt/ZZ
t

+

1 −ϑI
2
 
ZZ
t ˜It
ZI
t ˜It−1
−ZZ
ss
!2
˜It
9. Country Risk Premium (SB∗
t
)
SB∗
t
= SB∗h
exp

−ϕ∗
B

B∗x
t+1 −B∗x
+ ϕ∗
V (V ∗
t −V ) + ZB∗
t
i
10. Non-Linear Wage Phillips Curve
SW 1
t = ˜Λt(1 −τ N
t ) ˜W
ϵW
t
Nt(ϵW −1) + θW βEt

 ZZ
t+1
1−σ ΠC
t+1
ΥW
t+1
ϵW −1
SW 1
t+1


SW 2
t = ZC
t ZW
t ZL
t ψϕS
t ˜W
ϵW (1+η)
t
N
(1+η)
t
ϵW + θW βEt

 ZZ
t+1
1−σ ΠC
t+1
ΥW
t+1
ϵW (1+η)
SW 2
t+1



˜W
⋆
t
1+ηϵW
SW 1
t = SW 2
t
11. Wage Indexation Rule
ΥW
t
=
 ΠW
t−1
ωW  ZZC
t−1
4 Π4C
t−1
 1−ωW
4
 1
ZZ
t

Π4C
t
= ΠC
t ΠC
t−1ΠC
t−2ΠC
t−3
12. Wage Index
˜Wt =

θW
 
ΥW
t
˜Wt−1
ΠC
t
!1−ϵW
+ (1 −θW )

˜W
⋆
t
1−ϵW


1
1−ϵW
13. Wage Inﬂation
67

ΠW
t
=
 
˜Wt
˜Wt−1
!
ΠC
t ZZ
t
14. Wage Dispersion and Adjusted Labor
vO
t = (1 −θW )
 ˜W
⋆
t
˜Wt
!−ϵW
+ θW
 
ΥW
t
˜Wt−1
˜WtΠC
t
!−ϵW
vO
t−1
vW
t
= ϖRT + (1 −ϖRT )vO
t
ˆNt = NtvW
t
15. Additional Equations from the GSW speciﬁcation for Labor Markets
ϕS
t =
eCS
t ˜Λt
ZC
t
eCS
t =
 ZZ
t
−(1−v)σ 
eCS
t−1
1−v ZC
t
˜Λt
v
(1 −τ N
t ) ˜Wt = ZL
t ψ eCS
t Lη
t
U L
t = Lt −Nt
Lt
Firms - Domestic Input Producers
16. Capital Demand
RK
t = αQD
t
 ZD
t
 ϵD−1
ϵD
 
ZZ
t ˜Y D
t
˜Kt−1
!
1
ϵD
17. Labor Demand
˜Wt = (1 −α) QD
t
 ZD
t
 ϵD−1
ϵD
 
˜Y D
t
Nt −N
!
1
ϵD
18. Domestic Input Supply
QD
t =

α
RK
t
α
1−ϵD
+ (1 −α)
 
˜Wt
1 −α
!1−ϵD

1
1−ϵD
1
ZD
t
Firms - Importers
68

19. Non-Linear Phillips Curve
SM 1
t =
 QM
t
εM c
f
M t + θMβEt

 ZZ
t+1
1−σ
 ˜Λt+1
˜Λt
! ΠC
t+1
ΥM
t+1
ϵM
SM 1
t+1


SM 2
t =
 QM
t
εM
QtQM∗
t
c
f
M t = θMβEt

 ZZ
t+1
1−σ
 ˜Λt+1
˜Λt
! ΠC
t+1
ΥM
t+1
−(1−ϵM)
SM 2
t+1


QM ⋆
t
=
εM
εM −1
SM 2
t
SM 1
t

20. Imported Input Indexation Rule
ΥM
t
= ΠM
t−1
21. Imported Input Price Index
QM
t
=

θM
ΥM
t QM
t−1
ΠC
t
1−ϵM
+ (1 −θM)

QM ⋆
t
1−ϵM


1
1−ϵM
22. Imported Input Inﬂation
ΠM
t
= QM
t
QM
t−1
ΠC
t
23. Price Dispersion and Adjusted Imports
vM
t
= (1 −θM)
 
QM ⋆
t
QM
t
!−ϵM
+ θM
ΥM
t
ΠM
t
−ϵM
vM
t−1
c
f
M t = f
MtvM
t
Firms - Sectoral Intermediate Producers: Investment Good
24. Real Marginal Cost
69

MCI
t =

ϖI
 QD
t
1−ϵI + (1 −ϖI)
 
QM
I,t
1 −ΓM
I,t −ΓM†
I,t
!1−ϵI

1
1−ϵI
25. Domestic Input Demand
˜Y D
I,t = ϖI
 QD
t
MCI
t
−ϵI
˜Y I
t vI
t
26. Imported Input Demand
˜
M I
t =
 
1 −ϖI
1 −ΓM
I,t
! 

QM
I,t

1 −ΓM
I,t −ΓM†
I,t

MCI
t


−ϵI
˜Y I
t vI
t
27. Eﬀective Import Cost
QM
I,t =
h
1 + ιI

R∗
t SB∗
t
−1
i
QM
t
28. Adjustment Cost for Imports (ΓM
I,t) and its ﬁrst derivative (ΓM†
I,t )
ΓM
I,t = ϑM
I
2
 
 ZM
I,t
−
1
ϑM
I
˜
M I
t
˜
M I
t−1
ZZ
t −ZZ
ss
!2
ΓM†
I,t = ϑM
I
 
 ZM
I,t
−
1
ϑM
I
˜
M I
t
˜
M I
t−1
ZZ
t −ZZ
ss
!  
 ZM
I,t
−
1
ϑM
I
˜
M I
t
˜
M I
t−1
ZZ
t
!
29. Non-Linear Phillips Curve
SI1
t =
 QI
t
εP
I eY I
t + (θIβ)Et


 eΛt+1
eΛt
!
 ZZ
t+1
1−σ ΠC
t+1
ΥI
t+1
εP
I −1
SI1
t+1


SI2
t =
 QI
t
εP
I eY I
t MCI
t ZP
t + (θIβ)Et


 eΛt+1
eΛt
!
 ZZ
t+1
1−σ ΠC
t+1
ΥI
t+1
εP
I
SI2
t+1


QI⋆
t
=
εP
I
εP
I −1
SI2
t
SI1
t

30. Sectoral Indexation Rule
ΥI
t = ΠI
t−1
31. Sectoral Price Index
70

QI
t =

θI
ΥI
t QI
t−1
ΠC
t
1−ϵP
I
+ (1 −θI)

QI⋆
t
1−ϵP
I


1
1−ϵP
I
32. Sectoral Inﬂation
ΠI
t =
QI
t
QI
t−1
ΠC
t
33. Price Dispersion
vI
t = (1 −θI)
 
QI⋆
t
QI
t
!−ϵP
I
+ θI
ΥI
t
ΠI
t
−ϵP
I
vI
t−1
Firms - Sectoral Intermediate Producers: Government Consumption Good
34. Real Marginal Cost
MCG
t = QD
t
35. Domestic Input Demand
˜Y D
G,t = ˜Y G
t vG
t
36. Non-Linear Phillips Curve
SG1
t =
 QG
t
εP
G eY G
t
+ (θGβ)Et


 eΛt+1
eΛt
!
 ZZ
t+1
1−σ ΠC
t+1
ΥG
t+1
εP
G−1
SG1
t+1


SG2
t =
 QG
t
εP
G eY G
t MCG
t ZP
t + (θGβ)Et


 eΛt+1
eΛt
!
 ZZ
t+1
1−σ ΠC
t+1
ΥG
t+1
εP
G
SG2
t+1


QG⋆
t
=
εP
G
εP
G −1
SG2
t
SG1
t

37. Sectoral Indexation Rule
ΥG
t = ΠG
t−1
38. Sectoral Inﬂation
ΠG
t = QG
t
QG
t−1
ΠC
t
39. Sectoral Index
71

QG
t =

θG
ΥG
t QG
t−1
ΠC
t
1−ϵP
G
+ (1 −θG)

QG⋆
t
1−ϵP
G


1
1−ϵP
G
40. Price Dispersion
vG
t = (1 −θG)
 
QG⋆
t
QG
t
!−ϵP
G
+ θG
ΥG
t
ΠG
t
−ϵP
G
vG
t−1
Firms - Sectoral Intermediate Producers: Consumption Good
41. Real Marginal Cost
MCCD
t
=

ϖCD
 QD
t
1−ϵCD + (1 −ϖCD)
 
QM
CD,t
1 −ΓM
CD,t −ΓM†
CD,t
!1−ϵCD 

1
1−ϵCD
42. Domestic Input Demand
˜Y D
CD,t = ϖCD

QD
t
MCCD
t
−ϵCD
˜Y CD
t
vCD
t
43. Imported Input Demand
˜
M CD
t
=
 
1 −ϖCD
1 −ΓM
CD,t
! 

QM
CD,t

1 −ΓM
CD,t −ΓM†
CD,t

MCCD
t


−ϵCD
˜Y CD
t
vCD
t
44. Eﬀective Import Cost
QM
CD,t =
h
1 + ιCD

R∗
t SB∗
t
−1
i
QM
t
45. Adjustment Cost for Imports (ΓM
CD,t) and its ﬁrst derivative (ΓM†
CD,t)
ΓM
CD,t = ϑM
CD
2
 
ZM
CD,t
−
1
ϑM
CD
˜
M CD
t
˜
M CD
t−1
ZZ
t −ZZ
ss
!2
ΓM†
CD,t = ϑM
CD
 
ZM
CD,t
−
1
ϑM
CD
˜
M CD
t
˜
M CD
t−1
ZZ
t −ZZ
ss
!  
ZM
CD,t
−
1
ϑM
CD
˜
M CD
t
˜
M CD
t−1
ZZ
t
!
46. Non-Linear Phillips Curve for goods with freely-set prices
SF 1
t = (QCD
t
)ϵP
CD eY CD
t
+ (θF β)Et


 eΛt+1
eΛt
!
 ZZ
t+1
1−σ ΠC
t+1
ΥF
t+1
εP
CD −1
SF 1
t+1


72

SF 2
t = (QCD
t
)ϵP
CD eY CD
t
MCCD
t
ZP
t + (θF β)Et


 eΛt+1
eΛt
!
 ZZ
t+1
1−σ ΠC
t+1
ΥF
t+1
εP
CD
SF 2
t+1


QF ⋆
t
=
εP
CD
εP
CD −1
SF 2
t
SF 1
t

47. Indexation Rule for goods with freely set prices
ΥF
t = ΠC
t−1
48. Price Index for goods with freely set prices
QF
t =

θF
ΥF
t QF
t−1
ΠC
t
1−ϵP
CD
+ (1 −θF )

QF ⋆
t
1−ϵP
CD


1
1−ϵP
CD
49. Inﬂation for goods with freely set prices
ΠF
t = QF
t
QF
t−1
ΠC
t
50. Non-Linear Phillips Curve for goods with administered prices
SA1
t = (QCD
t
)ϵP
CD eY CD
t
+ (θAβ)Et


 eΛt+1
eΛt
!
 ZZ
t+1
1−σ ΠC
t+1
ΥA
t+1
εP
CD −1
SA1
t+1


SA2
t = (QCD
t
)ϵP
CD eY CD
t
MCCD
t
ZP
t + (θAβ)Et


 eΛt+1
eΛt
!
 ZZ
t+1
1−σ ΠC
t+1
ΥA
t+1
εP
CD
SA2
t+1


QA⋆
t
=
εP
CD
εP
CD −1
SA2
t
SA1
t

51. Price Setting for goods with administered prices
QA
t =

θA

ΥA
t
QA
t−1
ΠC
t

1−ϵP
CD + (1 −θA)

QA⋆
t

1−ϵP
CD

1
1−ϵP
CD
52. Indexation Rule for goods with administered prices
ΥA
t =
(
 Π4C
t−1
 1
4
 Qt
Qt−1
υ1
A  Qt
Qt−1
Πco,∗
t
υ2
A)
ZA
t
53. Inﬂation for goods with administered prices
73

ΠA
t = QA
t
QA
t−1
ΠC
t
54. Relative price for domestic consumption
QCD
t
=

ϖA
 QA
t
1−ϵP
CD + (1 −ϖA)
 QF
t
1−ϵP
CD

1
1−ϵP
CD
55. Inﬂation for domestic consumption
ΠCD
t
= QCD
t
QCD
t−1
ΠC
t
56. Price Dispersion
vF
t = (1 −θF )
 
QF ⋆
t
QF
t
!−ϵP
CD
+ θF
ΥF
t
ΠF
t
−ϵP
CD
vF
t−1
vA
t = (1 −θA)
 
QA⋆
t
QA
t
!−ϵP
CD
+ θA
ΥA
t
ΠA
t
−ϵP
CD
vA
t−1
vCD
t
= ϖA
 QA
t
QCD
t
−ϵP
CD
vA
t + (1 −ϖA)
 QF
t
QCD
t
−ϵP
CD
vF
t
Firms - Sectoral Intermediate Producers: Export Good
57. Real Marginal Cost
MCX
t
=

ϖX
 QD
t
1−ϵX + (1 −ϖX)
 
QM
X,t
1 −ΓM
X,t −ΓM†
X,t
!1−ϵX

1
1−ϵX
58. Domestic Input Demand
˜Y D
X,t = ϖX
 QD
t
MCX
t
−ϵX
˜Y X
t vX
t
59. Imported Input Demand
˜
M X
t
=
 
1 −ϖX
1 −ΓM
X,t
! 

QM
X,t

1 −ΓM
X,t −ΓM†
X,t

MCX
t


−ϵX
˜Y X
t vX
t
60. Eﬀective Import Cost
QM
X,t =
h
1 + ιX

R∗
t SB∗
t
−1
i
QM
t
61. Adjustment Cost for Imports (ΓM
X,t) and its ﬁrst derivative (ΓM†
X,t)
74

ΓM
X,t = ϑM
X
2
 
 ZM
X,t
−
1
ϑM
X
˜
M X
t
˜
M X
t−1
ZZ
t −ZZ
ss
!2
ΓM†
X,t = ϑM
X
 
 ZM
X,t
−
1
ϑM
X
˜
M X
t
˜
M X
t−1
ZZ
t −ZZ
ss
!  
 ZM
X,t
−
1
ϑM
X
˜
M X
t
˜
M X
t−1
ZZ
t
!
62. Non-Linear Phillips Curve
SX1
t =
 QX
t
εP
X Qt eY X
t
+ (θXβ)Et
" eΛt+1
eΛt
!
 ZZ
t+1
1−σ Π∗
t+1
ΥX
t+1
εP
X−1
SX1
t+1
#
SX2
t =
 QX
t
εP
X eY X
t MCX
t ZP ∗
t
+ (θXβ)Et
" eΛt+1
eΛt
!
 ZZ
t+1
1−σ Π∗
t+1
ΥX
t+1
εP
X
SX2
t+1
#
QX⋆
t
=
εP
X
εP
X −1
SX2
t
SX1
t

63. Sectoral Indexation Rule
ΥX
t =
 ΠX
t−1
ωX
P co∗
t
P co∗
t−1
Π∗
ss
1−ωX
64. Sectoral Price Index
QX
t =

θX
ΥX
t QX
t−1
Π∗
t
1−ϵP
X
+ (1 −θX)

QX⋆
t
1−ϵP
X


1
1−ϵP
X
65. Sectoral Inﬂation
ΠX
t = QX
t
QX
t−1
Π∗
t
66. Price Dispersion
vX
t = (1 −θX)
 
QX⋆
t
QX
t
!−ϵP
X
+ θX
ΥX
t
ΠX
t
−ϵP
X
vX
t−1
Demand For Brazilian Exports
67. Imported Input Demand concerning foreign production
˜Xt =

ϖ∗
1 −ΓM ∗
t
  
QX
t
 1 −ΓM ∗
t
−ΓM ∗†
t

!−ϵ∗
˜Y ∗
t
68. Adjustment Cost for Imports (ΓM ∗
t
) and its ﬁrst derivative (ΓM∗†
t
) concerning foreign
75

production
ΓM ∗
t
= ϑM ∗
2
 
ZM ∗
t
−
1
ϑM∗
˜Xt/ ˜Y ∗
t
˜Xt−1/ ˜Y ∗
t−1
−1
!2
ΓM ∗†
t
= ϑM ∗
 
ZM ∗
t
−
1
ϑM∗
˜Xt/ ˜Y ∗
t
˜Xt−1/ ˜Y ∗
t−1
−1
!  
ZM ∗
t
−
1
ϑM∗
˜Xt/ ˜Y ∗
t
˜Xt−1/ ˜Y ∗
t−1
!
Government - Monetary Policy
69. Taylor Rule
Rt = Rγr
t−1
"
Π
C
t Rnat
t
 
EtΠC
t+1
EtΠ
C
t+1
!γπ  YtZZ
t
Yt−1ZZ
ss
γy#(1−γr)
eϵR
t
70. The natural rate of interest
Rnat
t
= 1
β
 ZZC
t
σ
71. Law of motion for the Inﬂation Target
Π
C
t =

Π
C
ss
1−ρΠC 
Π
C
t−1
ρΠC
+ exp(ϵΠ,0
t
+ ϵΠ,2
t−2 + ϵΠ,6
t−6 + ϵΠ,10
t−10)
Government - Fiscal Policy
72. Government Spending to GDP Ratio
GY
t =
˜
Gt
˜Yt
73. Primary Surplus
Sy
t = Tt −P G
t Gt
P Y
t Yt
= Tt
QG
t
QY
t
GY
t
74. Law of motion for Government Debt
By
t+1 = Rt
 By
t
ΠY
t
Yt−1
Yt
−Sy
t

75. Tax Rule
τ N
t
= τ N
ss + γT
 τ N
t−1 −τ N
ss

+ γS

S4,y
t
−S
y
t

+ ϵT
t
76. Tax Revenue
τ N
t
˜WtNt + eT Lump
t
= TtQY
t eYt
77. Lump-Sum Taxation
76

T Lump
t
P C
t Zt
= eT Lump
t
= eT Lump
ss
+ γT L

eT Lump
t−1
−eT Lump
ss

+ ϵT L
t
78. Targeted and Smoothed Primary Surplus
S
y
t = S
y
ss + ρS

S
y
t−1 −S
y
ss

+ (1 −ρS)γB
 EtBy
t+1 −By
ss

+ ϵS
t
S4,y
t
= 0.25(Sy
t + Sy
t−1 + Sy
t−2 + Sy
t−3)
Resources Constraints and Identities
79. Sectoral Resource Constraints
˜Y CD
t
= ˜CD
t
˜Y I
t = ˜It
˜Y G
t
= ˜Gt
˜Y X
t
= ˜Xt
80. Market Clearing for Domestic Intermediate Inputs
˜Y D
t
= ˜Y D
CD,t + ˜Y D
I,t + ˜Gt + ˜Y D
X,t
81. Market Clearing for Imported Goods
˜
Mt = ˜
M CD
t
+ ˜
M I
t + ˜
M X
t + ˜CM
t
82. Interest on External Borrowing to GDP Ratio
L∗y
t
=
X
H∈{CD,I,X}
ιH

R∗
t SB∗
t
−1
 QM
t
˜
M H
t
QY
t ˜Yt
83. Net Exports to GDP Ratio
NXy
t = QtQX∗
t
˜Xt
QY
t ˜Yt
−QtQM ∗
t
˜
Mt
QY
t ˜Yt
vM
t
84. Law of Motion for Net Foreign Assets to GDP Ratio
B∗y
t+1
R∗
t SB∗
t
=
 
˜Yt−1
ΠY
t ZZ
t ˜Yt
Qt
Qt−1
ΠC
t
Π
∗
t
!
B∗y
t
+ NXy
t −L∗y
t
77

85. Nominal GDP Identity
QY
t ˜Yt = ˜Ct + QI
t ˜It + QG
t ˜Gt + QtQX∗
t
˜Xt −QtQM ∗
t
˜
MtvM
t
86. Real GDP according to a Laspeyres Quantity Index
QY
ss ˜Yt = ˜Ct + QI
ss ˜It + QG
ss ˜Gt + QssQX
ss ˜Xt −QssQM∗
ss
˜
MtvM
t
87. Inﬂation based on the GDP deﬂator
ΠY
t = QY
t
QY
t−1
ΠC
t
Rest of the World - VAR System and Import Price dynamics
We specify the VAR as follows:
Z∗
t = A1Z∗
t−1 + (...) + AnZ∗
t−n + ϵ∗
t ,
ϵ∗
t ∼N(0, B)
The vector Z∗
t = [Y ∗
t ; R∗
t ; Π∗
t ; V ∗
t ; P co,∗
t
] stacks the foreign variables, Ai as the matrix of
coeﬃcients for lag i and ϵ∗
t as the vector of structural shocks with covariance matrix B.
Finally, the equation bellow connects import prices (QM∗
t
) to commodity prices (P co∗
t
):
log(QM∗
t
/QM∗
ss ) = ρQMlog(QM∗
t−1/QM∗
ss ) + γClog(P co∗
t−1/P co∗
ss ) + ϵQM∗
t
Shocks - AR(1) or ARMA(1,1) Speciﬁcations
The shocks ZZC
t
, ZM
t , ZC
t , ZB∗
t
, SB
t , ZD
t , ZM
t , eGt, ZI
t , ZM ∗, ZL
t , ZQ
t follow an AR(1) process.
ZZT
t
is white noise, while ZA
t , ZR
t , ZW
t and ZP ∗
t
follow an ARMA(1,1) process.
78

B
Steady State
Analytical computation of the steady state
Given the parametric restrictions previously discussed, we normalize some variables and then
use ﬁrst order conditions to compute the steady state according to the following steps:
1. Ad hoc Calibration: required values from other data sources
• ZZ
ss,
U L
ss,
Lss,
N,
Π
C
ss,
¯ΥA = Π
C
ss,
Π∗
ss,
ϖRT
• S
y
ss,
Sy
ss = S
y
ss,
Rss,
Rnat
ss
= Rss
Π
C
ss ,
R∗
ss
• QF
ss = 1,
Qss = 1,
P co∗
ss
= 1,
˜Yss = 1,
eY ∗
ss = 1,
V ∗
ss = 0,
QCD
ss
= 1,
QM
ss = 1
• δ,
σ,
weight A (weight of administered prices in CPI)
• ϵP
CD = ϵP
I = ϵP
G = ϵP
X = ϵM
• ϵI = ϵCD = ϵX
• ιI = ιCD = ιX
• ϖI = ϖCD = ϖX
• Share of labor tax in total government revenues: sT L = τ N
ss ˜
WssNss
Tss
2. Shocks
ZM
ss = ZC
ss = ZB∗
ss = SB
ss = ZD
ss = ZM
ss = ZI
ss = ZM ∗
ss
= ZL
ss = ZQ
ss = ZA
ss = ZR
ss = ZW
ss = ZP ∗
ss = 1
3. Adjustment Costs
ΓM
Iss = ΓM
CD
ss = ΓM
Xss = ΓM ∗
Gss = ΓM†
Iss = ΓM†
CD
ss = ΓM†
Xss = ΓM ∗†
ss
= 0
4. Price Dispersion
vO
ss = vW
ss = vM
ss = vI
ss = vG
ss = vF
ss = vA
ss = vCD
ss
= vX
ss = 1
5. Inﬂation Rates
ΠC
ss = ΠCD
ss
= ΠM
ss = ΠI
ss = ΠG
ss = ΠF
ss = ΠA
ss = ΠY
ss = Π
C
ss, Π4C
ss =

Π
C
ss
4
, ΠX
ss = Π∗
ss, ΠW
ss =
Π
C
ssZZ
ss
6. Indexation Factors
ΥW
ss = ΥM
ss = ΥI
ss = ΥG
ss = ΥF
ss = ΥA
ss = Π
C
ss, ΥX
ss = Π∗
ss
7. Calibrated GDP shares and sectoral import shares
Based on the sample used for estimation, we compute the following ratios:
79

sC,
sI,
sG,
sX,
sM
8. GDP Components
˜Css = sC ˜Yss,
˜Iss = sI ˜Yss,
eGss = sG ˜Yss,
˜Xss = sX ˜Yss,
˜
Mss = sM ˜Yss
9. Calibration based on Dynamic Equations
β =
 ZZ
ss
σ Π
C
ss
Rss , SB∗
ss =

Rss
Π
C
ss
 
Π∗
ss
R∗
ss

, By
ss =
Sy
ss
−
ZZ
ss
ΠC
ss
−
1
Rss
10. Sector Sectoral Marginal Costs and Relative Prices
MCCD
ss
= ϵP
CD −1
ϵP
CD
QF
ss
MCI
ss = MCCD
ss
MCX
ss = MCCD
ss
QM∗
ss
=
εM
εM −1
QM
ss
Qss

QD
ss =

(MCCD
ss )1−ϵCD −(1 −ϖCD) (QM
CD
ss)1−ϵCD
ϖCD


1
1−ϵCD
QM
CD
ss = 1 + ιC

R∗
ssSB∗
ss −1

QM
ss
QM
Iss =
h
1 + ιI

R∗
ssSB∗
ss −1
i
QM
ss
QM
Xss =
h
1 + ιX

R∗
ssSB∗
ss −1
i
QM
ss
MCG
ss = QD
ss
11. Sectoral Relative Prices
QI
ss =
ϵP
I
ϵP
I −1MCI
ss
QX
ss =
ϵP
X
ϵP
X −1MCX
ss
80

QG
ss =
ϵP
G
ϵP
G −1MCG
ss
12. Household consumption of domestic and imported goods
oC =
(1 −sM
sC ) +
"
( sI+sX
sC
)(1 −ϖCD)

QM
CD
ss
MCCD
ss
−ϵCD #
1 −
"
(1 −ϖCD)
 QM
CD
ss
MCCD
ss
−ϵCD #
ϖA = peso A
oC
˜CD
ss = oC ˜Css
˜CM
ss = (1 −oC) ˜Css
13. Demand for goods
˜Y CD
ss
= ˜CD
ss, ˜Y I
ss = ˜Iss, ˜Y G
ss = eGss, ˜Y X
ss = ˜Xss
14. Sectoral Imports
˜
M CD
ss
= (1 −ϖCD)
 QM
CD
ss
MCCD
ss
!−ϵCD
˜Y CD
ss
˜
M I
ss = (1 −ϖI)
 
QM
Iss
MCIss
!−ϵI
˜Y I
ss
˜
M X
ss = (1 −ϖX)
 
QM
Xss
MCX
ss
!−ϵX
˜Y X
ss
c
f
M ss = ˜
M CD
ss
+ ˜
M I
ss + ˜
M X
ss + ˜CM
ss
15. Demand for Domestic Intermediate Goods
˜Y D
CD
ss = ϖCD

QD
ss
MCCD
ss
−ϵCD
˜Y CD
ss
˜Y D
Iss = ϖI
 QD
ss
MCIss
−ϵI
˜Y I
ss
81

˜Y D
Gss = ˜Y G
ss
˜Y D
Xss = ϖX
 QD
ss
MCX
ss
−ϵX
˜Y X
ss
˜Y D
ss = ˜Y D
CD
ss + ˜Y D
Iss + ˜Gss + ˜Y D
Xss
16. Additional Relative Prices
QF ⋆
ss = QF
ss,
QA
ss = QF
ss,
QA⋆
ss = QA
ss,
QI⋆
ss = QI
ss,
QG⋆
ss = QG
ss,
QX⋆
ss
= QX
ss,
QM ⋆
ss
=
QM
ss
17. GDP Deﬂator
QY
ss = ˜Css + QI
ss ˜Iss + QG
ss ˜Gss + QssQX
ss ˜Xss −QssQM∗
ss
˜
Mss
18. Capital Stock and Domestic Intermediate Good Supply
Nss = Lss(1 −U L
ss)
˜Kss =
˜IssZZ
ss
ZZ
ss −(1 −δ)
QK
ss = QI
ss
RK
ss = QK
ss
Rss
ΠC
ss
−(1 −δ)

αaux =


 
QD
ss ˜Y D
ss
RK
ss ˜Kss/ZZ
ss
−1
! 

RK
ss

QD
ss ˜Y D
ss −RK
ss ˜Kss/ZZ
ss
  Nss
 1 −N



1−ϵD
+ 1


−1
;
α = 1/[(1/αaux −1)1/ϵD + 1];
˜Wss = (1 −α)
"
1
1 −α
 QD
ss
ZD
ss
1−ϵD
−

α
1 −α
 RK
ss
α
1−ϵD#
1
1−ϵD
˜W
⋆
ss = ˜Wss and b
Nss = Nss
82

19. Variables expressed as GDP ratios
Tss = Sy
ss + QG
ssg
Gss
QYss f
Yss
GY
ss =
g
Gss
f
Yss
NXy
ss = QssQX∗
ss ˜Xss
QYss ˜Yss
−QssQM ∗
ss
˜
Mss
QYss ˜Yss
L∗y
ss =
X
H∈{CD,I,X}
ιH

R∗
ssSB∗
ss −1
 QM
ss ˜
M H
ss
QYss ˜Yss
B∗y
ss =
NXy
ss −L∗y
ss

1
R∗
t SB∗
t

−

1
ZZ
ssΠ∗
ss

20. Demand for Exports
ϖ∗=
˜Xss
˜Y ∗
ss (QX
ss)−ϵ∗
21. Households
eT Lump
ss
= (1 −sT L)TssQY
ss f
Yss
τ N
ss = TssQY
ss f
Yss −eT Lump
ss
˜WssNss
˜CRT
ss
= (1 −τ N
ss) ˜WssNss
˜CO
ss =
˜Css −ϖRT ˜CRT
ss
(1 −ϖRT )
˜Λss =
 
˜CO
ss −κ
˜CO
ss
ZZ
ss
!−σ
22. Labor Market: GSW
eCS
ss =
ZC
ss
˜Λss
  ZZ
ss
−(1−v)σ
v
ϕS
ss =
eCS
t ˜Λss
ZC
ss
83

ψ = (1 −τ N
ss) ˜Wss
ZL
ss eCS
ssLη
ss
ϵW =
1
1 −

ZC
ssZW
ss ZL
ssψϕS
ss
˜Λss(1−τ N
ss) ˜
WssN−η
ss

23. Nominal Rigidities
SW 1
ss =
˜Λss(1 −τ N
ss) ˜W
ϵW
ss Nss(ϵW −1)
1 −
h
θW β (ZZ
ss)1−σi
SW 2
ss = ZC
ssZW
ss ZL
ssψϕS
ss ˜W
ϵW (1+η)
ss
N
(1+η)
ss
ϵW
1 −
h
θW β (ZZ
ss)1−σi
SM 1
ss =
 QM
ss
εM c
f
M ss
1 −
h
θMβ (ZZ
ss)1−σi
SM 2
ss =
 QM
ss
εM
QssQM∗
ss
c
f
M ss
1 −
h
θMβ (ZZ
ss)1−σi
SI1
ss =
 QI
ss
εP
I eY I
ss
1 −
h
θIβ (ZZ
ss)1−σi
SI2
ss =
 QI
ss
εP
I eY I
ssMCI
ssZP
ss
1 −
h
θIβ (ZZ
ss)1−σi
SG1
ss =
 QG
ss
εP
G eY G
ss
1 −
h
θGβ (ZZ
ss)1−σi
SG2
ss =
 QG
ss
εP
G eY G
ssMCG
ssZP
ss
1 −
h
θGβ (ZZ
ss)1−σi
SF 1
ss =
(QCD
ss )ϵP
CD eY CD
ss
1 −
h
θF β (ZZ
ss)1−σi
SF 2
ss = (QCD
ss )ϵP
CD eY CD
ss MCCD
ss ZP
ss
1 −
h
θF β (ZZ
ss)1−σi
84

SA1
ss =
(QCD
ss )ϵP
CD eY CD
ss
1 −
h
θAβ (ZZ
ss)1−σi
SA2
ss = (QCD
ss )ϵP
CD eY CD
ss MCCD
ss ZP
ss
1 −
h
θAβ (ZZ
ss)1−σi
SX1
ss =
 QX
ss
εP
X Qss eY X
ss
1 −
h
θXβ (ZZ
ss)1−σi
SX2
ss =
 QX
ss
εP
X eY X
ss MCX
ssZP ∗
ss
1 −
h
θXβ (ZZ
ss)1−σi
85

C
Data Treatment
Observed variables measured in per capita terms use the interpolated trend from the HP ﬁlter
applied to annual population estimates provided by IBGE. These estimates are published for
years where Census data is not available, and the use of the trend from the HP ﬁlter eliminates
signiﬁcant jumps in data when new information is considered to compute new estimates.
Table 6: Data used in estimation
Variable
Model representation
Description
Source
Treatment
Observation
∆yt
100 ×
"
log

Yt
Yt−1

+ log
 
ZZ
t
ZZ
ss
!#
Growth
rate,
GDP
per
capita
IBGE
I-L-D
National
Ac-
counts:
GDP
seas. adj.
∆ct
100 ×
"
log

Ct
Ct−1

+ log
 
ZZ
t
ZZ
ss
!#
+ m.e.
Growth
rate,
Consumption
per capita
IBGE
I-L-D
National
Accounts:
Consumption
seas. adj.
∆it
100 ×
"
log

It
It−1

+ log
 
ZZ
t
ZZ
ss
!#
+ m.e.
Growth
rate,
Investment per
capita
IBGE
I-L-D
National
Accounts:
Investment
seas. adj.
∆gt
100 ×
"
log

Gt
Gt−1

+ log
 
ZZ
t
ZZ
ss
!#
+ m.e.
Growth
rate,
Gov.
spending
per capita
IBGE
I-L-D
National
Ac-
counts:
Gov.
spending seas.
adj.
∆xt
100 ×
"
log

Xt
Xt−1

+ log
 
ZZ
t
ZZ
ss
!#
+ m.e.
Growth
rate,
Exports
per
capita
IBGE
I-L-D
National
Accounts:
Exports
seas.
adj.
∆mt
100 ×
"
log

Mt
Mt−1

+ log
 
ZZ
t
ZZ
ss
!#
+ m.e.
Growth
rate,
Imports
per
capita
IBGE
I-L-D
National
Accounts:
Imports
seas.
adj.
yt
100 × log

Yt
Yss

+ m.e
Output
gap,
GDP
per
capita
IBGE
&
BCB
I-L-G
National
Ac-
counts:
GDP
seas. adj.; See
3.2
∆wnt
100 ×
"
log

Wt
Wt−1

+ log
 
ZZ
t
ZZ
ss
!
+ log
 
ΠC
t
ΠC
ss
!#
+ m.e.
Growth
rate,
Nominal wages
IBGE
&
MF-VAR
S-L-D
PNAD-C Sur-
vey
lt
100 × (Lt −Lss)
Participation
rate
IBGE
&
MF-VAR
S-L-G
PNAD-C Sur-
vey
ut
100 × (UL
t
−UL
ss)
Unemployment
rate
IBGE
&
MF-VAR
S-L-G
PNAD-C Sur-
vey
pC
t
100 × (ΠC
t
−ΠC
ss)
CPI
Inflation
rate
IBGE
S-L-G
IPCA
pA
t
100 × (ΠA
t
−ΠC
ss)
Inflation
rate,
Administered
prices
IBGE
&
BCB
S-L-G
pF
t
pC
t −weightApA
t −ϵme,CP I
t
1−weightA
Inflation
rate,
Free prices
IBGE
&
BCB
S-L-G
pC
t
100 × (ΠC
t
−ΠC
ss)
Inflation target
(IT)
CMN
L-G
(Continued on next page)
86

Table 6 (continued from previous page)
Variable
Model representation
Description
Source
Treatment
Observation
eΠ,2
t−2
ϵΠ,2
t−2
Change
in
IT:
two-quarters
ahead
CMN
L-G
eΠ,6
t−6
ϵΠ,6
t−6
Change
in
IT:
six-quarters
ahead
CMN
L-G
eΠ,10
t−10
ϵΠ,10
t−10
Change
in
IT:
ten-quarters
ahead
CMN
L-G
EtpC
t
pC
t+1 + pC
t+2 + pC
t+3 + pC
t+4
Inflation
ex-
pectations
BCB
L-G
Focus Survey
rt
100 × (Rt −Rss)
Interest rate
BCB
L-G
SGS:
Selic
rate
sy
t
100 × (Sy
t −Sy
ss)
Primary
result
– quarterly
BCB
S-G
SGS
sy
t
100 × (Sy
t −Sy
ss)
Primary
result
target
BCB
G
SGS
qt
100 × (log Qt −log Qss)
Real
exchange
rate
BCB
L-G
SGS
∆qM∗
t
100 × (log QM∗
t
−log QM∗
t−1)
Import
price
inflation
Funcex
I-S-L-D
pX
t
100 × (ΠX
t
−ΠX
ss)
Export prices
Funcex
L-G
pco∗
t
pco∗
t
−pco∗
ss
Commodity
prices
BCB
G
See 3.1
r∗
t
100 × (R∗
t −R∗
ss)
Foreign
inter-
est rates
St
Louis
Fed
L-HP-G
FRED
p∗
t
100 × (Π∗
t −Π∗
ss)
Foreign
infla-
tion
St
Louis
Fed
G
FRED
y∗
t
100 × log(Y ∗
t /Y ∗
ss)
Foreign output
gap
BCB
L-OHP-G
sB∗
t
100 × (SB∗
t
−SB∗
ss )
Country
risk
premium
Bloomberg
G
CDS
v∗
t
V ∗
t
−V ∗
ss
Foreign
risk
aversion
BCB
G
See 3.1
Note: In column “Model representation”, “m.e.” is the representation for measurement error described in equation (76). Legend for column
“Treatment”: “I” is new index combining two raw indexes (as in per capita variables combining the raw information with population data,
or real variables combining raw data with a deflator); “L” is the natural logarithm of an index or rate; “G” is the gap with respect to
steady state value; “D” is the first difference of an index; “OHP” is the one-sided HP Filter; “HP” is the two-sided HP Filter; “S” is seasonal
adjustment based on ARIMA X-12 procedure.
87

D
Priors and Histogram of Posterior Distribution
Figure 13: Prior and Posterior Distribution – 1
5
10
15
0.35
0.4
0.45
0.5
0
1000
2000
Posterior Histogram
0.2
0.4
0.6
0.8
1
1
2
3
0
1000
2000
20
40
60
80
0.01
0.02
0.03
0.04
0
1000
20
40
60
80
100
120
Prior Density
0.01
0.02
0.03
0
1000
2
4
6
0.4
0.5
0.6
0.7
0.8
0
1000
2000
Posterior Histogram
0.2
0.4
2
4
6
0
1000
2000
0.5
1
1.5
0.2
0.4
0.6
0.8
0
1000
2000
0.2
0.4
0.6
0.8
1
Prior Density
1
2
3
0
1000
2000
20
40
0.02 0.04 0.06 0.08 0.1 0.12 0.14
0
1000
Posterior Histogram
200
400
2
4
6
8
10-3
0
1000
2000
0.2
0.4
0.6
0.8
1
1
2
3
0
1000
2000
0.2
0.4
0.6
0.8
1
Prior Density
1
2
3
4
0
1000
0.1
0.2
0.3
10
12
14
16
0
1000
2000
Posterior Histogram
0.1
0.2
20
25
30
0
1000
2000
0.05
0.1
0.15
20
25
30
0
1000
2000
0.5
1
1.5
Prior Density
0.2
0.4
0.6
0.8
0
1000
2000
0.5
1
1.5
0.2
0.4
0.6
0.8
0
1000
Posterior Histogram
0.5
1
1.5
0.2
0.4
0.6
0.8
0
1000
0.5
1
1.5
2
0.2
0.4
0.6
0.8
0
1000
2000
0.5
1
1.5
2
Prior Density
0.2
0.4
0.6
0.8
0
1000
0.5
1
1.5
0.2
0.4
0.6
0.8
0
1000
Posterior Histogram
2
4
0.2
0.4
0.6
0.8
0
1000
2000
2
4
0.2
0.4
0.6
0.8
0
1000
2000
0.5
1
1.5
Prior Density
0.2
0.4
0.6
0.8
0
1000
2000
0.5
1
1.5
0.2
0.4
0.6
0.8
0
1000
2000
Posterior Histogram
0.2
0.4
0.6
0.8
1
1.2
0.2
0.4
0.6
0.8
0
1000
2000
0.1
0.2
0.3
0.4
0.5
2
4
6
0
1000
2000
0.5
1
1.5
Prior Density
0.5
1
1.5
2
0
1000
2
4
6
0.2
0.3
0.4
0.5
0.6
0
1000
Posterior Histogram
0.5
1
1.5
2
0.5
1
1.5
0
1000
2000
20
40
0.02
0.04
0.06
0.08
0
1000
2000
0.02
0.04
0.06
0.08
0.1
Prior Density
10
20
30
0
1000
2000
2
4
6
0.2
0.4
0.6
0
1000
2000
Posterior Histogram
2
4
6
0.2
0.3
0.4
0.5
0
1000
2
4
6
0.2
0.3
0.4
0.5
0.6
0
1000
2
4
6
Prior Density
0.2
0.3
0.4
0.5
0
1000
2000
2
4
6
0.2
0.4
0.6
0.8
0
1000
Posterior Histogram
2
4
6
0.2
0.3
0.4
0.5
0
1000
2000
2
4
6
0.2
0.3
0.4
0.5
0
1000
2000
2
4
6
Prior Density
0.2
0.3
0.4
0.5
0
1000
2000
2
4
6
0.2
0.3
0.4
0.5
0
1000
Posterior Histogram
2
4
6
0.2
0.3
0.4
0.5
0
1000
2
4
6
0.2
0.3
0.4
0.5
0
1000
2
4
6
Prior Density
0.2
0.3
0.4
0.5
0
1000
2
4
6
0.2
0.3
0.4
0.5
0
1000
2000
Posterior Histogram
2
4
6
0.2
0.4
0.6
0.8
0
1000
2
4
6
0.2
0.3
0.4
0.5
0
1000
2
4
6
Prior Density
0.2
0.4
0.6
0
1000
88

Figure 14: Prior and Posterior Distribution – 2
2
4
6
0.2
0.3
0.4
0.5
0.6
0
1000
Posterior Histogram
2
4
6
0.2
0.3
0.4
0.5
0
1000
2000
2
4
6
0.2
0.3
0.4
0.5
0
1000
2
4
6
Prior Density
0.2
0.3
0.4
0.5
0
1000
2000
2
4
6
0.2
0.3
0.4
0.5
0
1000
2000
Posterior Histogram
5
10
15
20
0.85
0.9
0.95
0
1000
2000
2
4
6
0.2
0.3
0.4
0.5
0
1000
1.4
1.6
1.8
0
1000
2000
0.5
1
1.5
0
500
1000
1500
Posterior Histogram
0.5
1
1.5
0
500
1000
1500
0.5
0.6
0.7
0.8
0
1000
2000
0.8
1
1.2
0
1000
2000
3
4
5
6
0
1000
2000
Posterior Histogram
2
2.5
3
0
1000
2000
0.2
0.25
0.3
0
1000
2000
0.5
1
1.5
0
1000
2000
12
14
16
18
20
22
0
500
1000
1500
Posterior Histogram
40
60
80
0
500
1000
1500
1.5
2
2.5
0
1000
2000
40
60
80
100
120
140
0
500
1000
2.5
3
3.5
4
0
1000
Posterior Histogram
4
6
8
10
0
2000
0.5
1
1.5
2
0
1000
4
5
6
7
0
1000
30
40
50
60
70
0
500
1000
Posterior Histogram
2
4
6
0.5
1
1.5
2
0
1000
0.5
1
1.5
2
0.5
1
1.5
2
0
1000
2000
0.2
0.4
0.6
Prior Density
5
10
15
0
1000
2000
0.1
0.2
0.3
2
4
6
8
10
0
1000
2000
Posterior Histogram
0.5
1
1.5
2
2.5
1
2
3
4
5
0
1000
2000
0.2
0.4
0.6
0.8
1
1.2
0.2
0.4
0.6
0.8
0
500
1000
1500
0.2
0.4
0.6
0.8
1
1.2
Prior Density
0.2
0.4
0.6
0.8
0
1000
2000
0.2
0.4
0.6
0.8
1
1.2
0.2
0.4
0.6
0.8
0
500
1000
1500
Posterior Histogram
0.2
0.4
0.6
0.8
1
1.2
0.2
0.4
0.6
0.8
0
500
1000
1500
0.2
0.4
0.6
0.8
1
1.2
0.2
0.4
0.6
0.8
0
500
1000
1500
0.2
0.4
0.6
0.8
1
1.2
Prior Density
0.2
0.4
0.6
0.8
0
500
1000
1500
0.2
0.4
0.6
0.8
1
1.2
0.2
0.4
0.6
0.8
0
500
1000
1500
Posterior Histogram
0.2
0.4
0.6
0.8
1
1.2
0.2
0.4
0.6
0.8
0
500
1000
1500
0.2
0.4
0.6
0.8
1
1.2
0.2
0.4
0.6
0.8
0
1000
2000
0.2
0.4
0.6
0.8
1
1.2
Prior Density
0.2
0.4
0.6
0.8
0
500
1000
0.2
0.4
0.6
0.8
1
1.2
0.2
0.4
0.6
0.8
0
1000
Posterior Histogram
0.2
0.4
0.6
0.8
1
1.2
0.2
0.4
0.6
0.8
0
1000
2000
0.2
0.4
0.6
0.8
1
1.2
0.2
0.4
0.6
0.8
0
1000
0.2
0.4
0.6
0.8
1
1.2
Prior Density
0.2
0.4
0.6
0.8
0
1000
89

E
Computational details
The SMC estimation procedure characterizes the posterior distribution as a set of “particles”,
where each particle is a vector representing a complete set of estimated parameter values. As
detailed in Cai et al. (2021)[14], these particles are initially sampled from the prior distribu-
tion and then gradually updated to increasingly better approximate the posterior distribution.
The procedure includes several steps, but computational time is dominated by the likelihood
evaluation.
A critical property of SMC estimation is the independence of particle updating for each
step of the algorithm. This property facilitates parallel implementations of the algorithm across
particles. The likelihood evaluation, which is the focus of the discussion here, can be broken into
two main parts: solving the model for each particle to obtain its decision rules and running the
Kalman ﬁlter algorithm to obtain the likelihood for each particle. The algorithm for likelihood
evaluation works dividing the cloud of particles in n chunks of s particles each31. Then, each
chunk is co-distributed across all CPU cores, each core receiving roughly d = s/C particles,
where C is the number of cores in the CPU. All CPU cores available compute decision rules in
parallel (inside each core the computation is sequential), and after this step each core runs the
Kalman ﬁlter algorithm with the help of a GPU.
The GPU computation of the Kalman ﬁlter is carried out by all cores simultaneously calling
the GPU. The data sample available for estimation has size T and each call sends C separated
blocks of d particles to the GPU. Each block is converted to a GPU array32. Blocks are processed
in GPU for each time slice of the sample following the traditional log-likelihood evaluation
through Kalman ﬁltering. In other words, for a given period t < T of the data sample, GPU
cores evaluate the density of particle i for the whole block of d particles before moving to the
next period, t + 1.
Our computational resources comprises a workstation with a C = 10 cores CPU combined
with a 32 Gb dedicated memory GPU and 256 Gb RAM. The following pseudo-code summarizes
the procedure executed by each core:
Algorithm 1 Log-likelihood evaluation
procedure LogLikelihood(P)
▷P is a d particles block
for i ←1 to d do
D(i) ←ComputeDecisionRules(P(i))
end for
for t ←1 to T do
Loglikelihood(t) ←ComputeLogLikelihoodGPU(D, t)
end for
end procedure
In Algorithm 1, LogLikelihood has T log-likelihood evaluations for each particle. Summing
31The last chunk may have size less than s.
32All code is written using MATLAB Parallel Computing ToolboxTMavailable for MATLAB R
⃝.
90

over t gives the log-likelihood for each particle. The ﬁnal result is obtained combining the outputs
of each core.
An important point to be observed is that the function ComputeDecisionRules was not
implemented on GPU. It uses standard compiled code from Dynare[2]. Performance tests carried
out for serial, parallel CPU and GPU computing of the Kalman ﬁlter are summarized in Table 7.
The size for the set of “particles” in Table 7 approximates the full capacity of the GPU memory
for the model presented in this paper. The ﬁnal estimation of the model included 30,000 particles.
Table 7: Performance Tests – Kalman Filter
Time(s)
Particles
Device
Gain relative to serial code
3,516
8,000
CPU Serial
1.0x
686
8,000
CPU 10 cores
5.1x
236
8,000
GPU
14.9x
91