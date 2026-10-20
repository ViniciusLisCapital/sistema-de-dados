Chapter 2
MONETARY POLICY SHOCKS: WHAT HAVE WE LEARNED
AND TO WHAT END?
LAWRENCE J. CHRISTIANO
Northwestern University, NBER and the Federal Reserve Bank of Chicago
MARTIN EICHENBAUM
Northwestern University, NBER and the Federal Reserve Bank of Chicago
CHARLES L. EVANS
Federal Reserve Bank of Chicago
Contents
Abstract 66
Keywords 66
1. Introduction 67
2. Monetary policy shocks: some possible interpretations 71
3. Vector autoregressions and identification 73
4. The effects of a monetary policy shock: a recursiveness assumption 78
4.1. The recursiveness assumption and VARs 78
4.2. Three benchmark identification schemes 83
4.2.1. The benchmark policy shocks displayed 84
4.2.2. What happens after a benchmark policy shock? 85
4.2.2.1. Results for some major economic aggregates 85
4.3. Results for other economic aggregates 91
4.3.1. US domestic aggregates 91
4.3.1.1. Aggregate real variables, wages and profits 91
4.3.1.2. Borrowing and lending activities 93
4.3.2. Exchange rates and monetary policy shocks 94
4.4. Robustness of the benchmark analysis 96
4.4.1. Excluding current output and prices from £2t 97
4.4.2. Excluding commodity prices from g2~: The price puzzle 97
4.4.3. Equating the policy instrument, St, with M0, M1 or M2 100
4.4.4. Using information from the federal funds futures market 104
4.4.5. Sample period sensitivity 108
4.5. Discriminating between the benchmark identification schemes 114
4.5.1. The Coleman, Gilles and Labadie identification scheme 114
Handbook of Macroeconomics, Volume 1, Edited by J.B. Taylor and M. Woodford
65

66 L.J. Christiano et aL
4.5.2. The Bernanke-Mihov critique 115
4.5.2.1. A model of the federal funds market 116
4.5.2.2. Identifying the parameters of the model 117
4.5.2.3. The Bernanke-Mihov test 119
4.5.2.4. Empirical results 121
4.6. Monetary policy shocks and volatility 123
5. The effects of monetary policy shocks: abandoning the recursiveness
approach 127
5.1. A fully simultaneous system 128
5.1.1. Sims-Zha: model specification and identification 128
5.1.2. Empirical results 131
6. Some pitfalls in interpreting estimated monetary policy rules 134
7. The effects of a monetary policy shock: the narrative approach 136
8. Conclusion 143
References 145
Abstract
This chapter reviews recent research that grapples with the question: What happens
after an exogenous shock to monetary policy? We argue that this question is interesting
because it lies at the center of a particular approach to assessing the empirical
plausibility of structural economic models that can be used to think about systematic
changes in monetary policy institutions and rules.
The literature has not yet converged on a particular set of assumptions for
identifying the effects of an exogenous shock to monetary policy. Nevertheless, there
is considerable agreement about the qualitative effects of a monetary policy shock in
the sense that inference is robust across a large subset of the identification schemes
that have been considered in the literature. We document the nature of this agreement
as it pertains to key economic aggregates.
Keywords
monetary policy shocks, recursiveness assumption, benchmark analysis

Ch. 2: Monetary Policy Shocks: What Have we Learned and to What End? 67
1. Introduction
In the past decade there has been a resurgence of interest in developing quantitative,
monetary general equilibrium models of the business cycle. In part, this reflects the
importance of ongoing debates that center on monetary policy issues. What caused
the increased inflation experienced by many countries in the 1970s? What sorts of
monetary policies and institutions would reduce the likelihood of it happening again?
How should the Federal Reserve respond to shocks that impact the economy? What
are the welfare costs and benefits of moving to a common currency area in Europe?
To make fundamental progress on these types of questions requires that we address
them within the confines of quantitative general equilibrium models.
Assessing the effect of a change in monetary policy institutions or rules could be
accomplished using purely statistical methods. But only if we had data drawn from
otherwise identical economies operating under the monetary institutions or rules we
are interested in evaluating. We don't. So purely statistical approaches to these sorts of
questions aren't feasible. And, real world experimentation is not an option. The only
place we can perform experiments is in structural models.
But we now have at our disposal a host of competing models, each of which
emphasizes different frictions and embodies different policy implications. Which
model should we use for conducting policy experiments? This chapter discusses a
literature that pursues one approach to answering this question. It is in the spirit of a
suggestion made by R.E. Lucas (1980). He argues that economists
%.. need to test them (models) as useful imitations of reality by subjecting them to shocks for
which we are fairly certain how actual economies or parts of economies would react. The more
dimensions on which the model mimics the answers actual economies give to simple questions,
the more we trust its answers to harder questions." R.E. Lucas (I980)
The literature we review applies the Lucas program using monetary policy shocks.
These shocks are good candidates for use in this program because different models
respond very differently to monetary policy shocks see Christiano, Eichenbaum and
Evans (1997a). 1 The program is operationalized in three steps:
• First, one isolates monetary policy shocks in actual economies and characterizes the
nature of the corresponding monetary experiments.
• Second, one characterizes the actual economy's response to these monetary experi-
ments.
• Third, one performs the same experiments in the model economies to be evaluated
and compares the outcomes with actual economies' responses to the corresponding
experiments.
These steps are designed to assist in the selection of a model that convincingly
1 Other applications of the Lucas program include the work of Gall (1997) who studies the dynamic
effects of technology shocks, and Rotemberg and Woodford (1992) and Ramey and Shapiro (1998), who
study the dynamic effects of shocks to government purchases.

68 L.J. Christiano et al.
answers the question, "how does the economy respond to an exogenous monetary
policy shock?" Granted, the fact that a model passes this test is not sufficient to give
us complete confidence in its answers to the types of questions we are interested in.
However this test does help narrow our choices and gives guidance in the development
of existing theory.
A central feature of the program is the analysis of monetary policy shocks. Why
not simply focus on the actions of monetary policy makers? Because monetary policy
actions reflect, in part, policy makers' responses to nonmonetary developments in the
economy. A given policy action and the economic events that follow it reflect the effects
of all the shocks to the economy. Our application of the Lucas program focuses on the
effects of a monetary policy shock per se. An important practical reason for focusing
on this type of shock is that different models respond very differently to the experiment
of a monetary policy shock. In order to use this information we need to know what
happens in response to the analog experiment in the actual economy. There is no point
in comparing a model's response to one experiment with the outcome of a different
experiment in the actual economy. So, to proceed with our program, we must know
what happens in the actual economy after a shock to monetary policy.
The literature explores three general strategies for isolating monetary policy shocks.
The first is the primary focus of our analysis. It involves making enough identifying
assumptions to allow the analyst to estimate the parameters of the Federal Reserve's
feedback rule, i.e., the rule which relates policymakers' actions to the state of the
economy. The necessary identifying assumptions include functional form assumptions,
assumptions about which variables the Fed looks at when setting its operating
instrument and an assumption about what the operating instrument is. In addition,
assumptions must be made about the nature of the interaction of the policy shock with
the variables in the feedback rule. One assumption is that the policy shock is orthogonal
to these variables. Throughout, we refer to this as the recursiveness assumption. Along
with linearity of the Fed's feedback rule, this assumption justifies estimating policy
shocks by the fitted residuals in the ordinary least squares regression of the Fed's
policy instrument on the variables in the Fed's information set. The economic content
of the recursiveness assumption is that the time t variables in the Fed's information set
do not respond to time t realizations of the monetary policy shock. As an example,
Christiano et al. (1996a) assume that the Fed looks at current prices and output, among
other things, when setting the time t value of its policy instrument. In that application,
the recursiveness assumption implies that output and prices respond only with a lag
to a monetary policy shock.
While there are models that are consistent with the previous recursiveness
assumption, it is nevertheless controversial. 2 This is why authors like Bernanke (1986),
2 See Christiano, Eichenbaum and Evans (1997b) and Rotemberg and Woodford (1997) for models that
are consistent with the assumption that contemporaneous output and the price level do not respond to a
monetary policy shock.

Ch. 2: Monetary Policy Shocks: What Have we Learned and to What End? 69
Sims (1986), Sims and Zha (1998) and Leeper et al. (1996) adopt an alternative
approach. No doubt there are some advantages to abandoning the recursiveness
assumption. But there is also a substantial cost: a broader set of economic relations
must be identified. And the assumptions involved can also be controversial. For
example, Sims and Zha (1998) assume, among other things, that the Fed does not look
at the contemporaneous price level or output when setting its policy instrument and that
contemporaneous movements in the interest rate do not directly affect aggregate output.
Both assumptions are clearly debatable. Finally, it should be noted that abandoning
the recursiveness assumption doesn't require one to adopt an identification scheme in
which a policy shock has a contemporaneous impact on all nonpolicy variables. For
example, Leeper and Gordon (1992) and Leeper et al. (1996) assume that aggregate
real output and the price level are not affected in the impact period of a monetary
policy shock.
The second and third strategies for identifying monetary policy shocks do not
involve explicitly modelling the monetary authority's feedback rule. The second
strategy involves looking at data that purportedly signal exogenous monetary policy
actions. For example, Romer and Romer (1989) examine records of the Fed's policy
deliberations to identify times in which they claim there were exogenous monetary
policy shocks. Other authors like Rudebusch (1995) assume that, in certain sample
periods, exogenous changes in monetary policy are well measured by changes in the
federal funds rate. Finally, authors like Cooley and Hansen (1989, 1997), King (1991),
Christiano (1991) and Christiano and Eichenbaum (1995) assume that all movements
in money reflect exogenous movements in monetary policy.
The third strategy identifies monetary policy shocks by the assumption that they
do not affect economic activity in the long run. 3 We will not discuss this approach
in detail. We refer the reader to Faust and Leeper (1997) and Pagan and Robertson
(1995) for discussions and critiques of this literature.
The previous overview makes clear that the literature has not yet converged on
a particular set of assumptions for identifying the effects of an exogenous shock to
monetary policy. Nevertheless, as we show, there is considerable agreement about the
qualitative effects of a monetary policy shock in the sense that inference is robust
across a large subset of the identification schemes that have been considered in the
literature. The nature of this agreement is as follows: after a contractionary monetary
policy shock, short term interest rates rise, aggregate output, employment, profits and
various monetary aggregates fall, the aggregate price level responds very slowly, and
various measures of wages fall, albeit by very modest amounts. In addition, there is
agreement that monetary policy shocks account for only a very modest percentage
of the volatility of aggregate output; they account for even less of the movements in
3 For an early example of this approach see Gali (1992).

70 L.J. Christiano et al.
the aggregate price level.4 The literature has gone beyond this to provide a richer,
more detailed picture of the economy's response to a monetary policy shock (see
Section 4.6). But even this small list of findings has proven to be useful in evaluating
the empirical plausibility of alternative monetary business cycle models [see Christiano
et al. (1997a)]. In this sense the Lucas program, as applied to monetary policy shocks,
is already proving to be a fruitful one.
Identification schemes do exist which lead to different inferences about the effects
of a monetary policy shock than the consensus view just discussed. How should we
select between competing identifying assumptions? We suggest one selection scheme:
eliminate a policy shock measure if it implies a set of impulse response functions
that is inconsistent with every element in the set of monetary models that we wish to
discriminate between. This is equivalent to announcing that if none of the models that
we are interested in can account for the qualitative features of a set of impulse response
functions, we reject the corresponding identifying assumptions, not the entire set of
models. In practice, this amounts to a set of sign and shape restrictions on impulse
response functions [see Uhlig (1997) for a particular formalization of this argument].
Since we have been explicit about the restrictions we impose, readers can make their
own decisions about whether to reject the identifying assumptions in question.
In the end, the key contribution of the monetary policy shock literature may be
this: it has clarified the mapping from identification assumptions to inference about
the effects of monetary policy shocks. This substantially eases the task of readers and
model builders in evaluating potentially conflicting claims about what actually happens
after a monetary policy shock.
The remainder of this chapter is organized as follows:
Section 2: We discuss possible interpretations of monetary policy shocks.
Section 3: We discuss the main statistical tool used in the analysis, namely the Vector
Autoregression (VAR). In addition we present a reasonably self-contained discussion
of the identification issues involved in estimating the economic effects of a monetary
policy shock.
Section 4: We discuss inference about the effects of a monetary policy shock using
the recursiveness assumption. First, we discuss the link between the recursiveness
assumption and identified VAR's. Second, we display the dynamic response of various
economic aggregates to a monetary policy shock under three benchmark identification
schemes, each of which satisfies the recursiveness assumption. In addition, we discuss
related findings in the literature concerning other aggregates not explicitly analyzed
here. Third, we discuss the robustness of inference to various perturbations including:
alternative identification schemes which also impose the recursiveness assumption,
incorporating information from the federal funds futures market into the analysis and
varying the subsample over which the analysis is conducted. Fourth, we consider
4 These latter two findings say nothing about the impact of the systematic component of monetary
policy on aggregate output and the price level. The literature that we review is silent on this point.

Ch. 2: Monetary Policy Shocks: What Have we Learned and to What End? 71
some critiques of the benchmark identification schemes. Fifth, we consider the
implications of the benchmark identification schemes for the volatility of various
economic aggregates.
Section 5." We. consider other approaches which focus on the monetary authority's
feedback rule, but which do not impose the recursiveness assumption.
Section 6." We discuss the difficulty of directly interpreting estimated monetary policy
rules.
Section 7: We consider the narrative approach to assessing the effects of a monetary
policy shock.
Section 8: We conclude with a brief discussion of various approaches to implementing
the third step of the Lucas program as applied to monetary policy shocks. In particular
we review a particular approach to performing monetary experiments in model
economies, the outcomes of which can be compared to the estimated effects of a
policy shock in actual economies. In addition we provide some summary remarks.
2. Monetary policy shocks: some possible interpretations
Many economists think that a significant fraction of the variation in central bank
policy actions reflects policy makers' systematic responses to variations in the state
of the economy. As noted in the introduction, this systematic component is typically
formalized with the concept of a feedback rule, or reaction function. As a practical
matter, it is recognized that not all variations in central bank policy can be accounted
for as a reaction to the state of the economy. The unaccounted variation is formalized
with the notion of a monetary policy shock. Given the large role that the concepts of a
feedback rule and a policy shock play in the literature, we begin by discussing several
sources of exogenous variation in monetary policy.
Throughout this chapter we identify a monetary policy shock with the disturbance
term in an equation of the form
St =f(£2t) + ose~'. (2.1)
Here St is the instrument of the monetary authority, say the federal funds rate or some
monetary aggregate, and f is a linear fimction that relates St to the information set
£2t. The random variable, ase 7, is a monetary policy shock. Here, e7 is normalized to
have unit variance, and we refer to as as the standard deviation of the monetary policy
shock.
One interpretation off and f2t is that they represent the monetary authority's
feedback rule and information set, respectively. As we indicate in Section 6, there
are other ways to think about f and g2t which preserve the interpretation of e7 as a
shock to monetary policy.
What is the economic interpretation of these policy shocks? We offer three
interpretations. The first is that e reflects exogenous shocks to the preferences of

72 L.J. Christiano et al.
the monetary authority, perhaps due to stochastic shifts in the relative weight given
to unemployment and inflation. These shifts could reflect shocks to the preferences of
the members of the Federal Open Market Committee (FOMC), or to the weights by
which their views are aggregated. A change in weights may reflect shifts in the political
power of individual committee members or in the factions that they represent. A second
source of exogenous variation in policy can arise because of the strategic considerations
developed in Ball (1995) and Chari, Christiano and Eichenbaum (1998). These authors
argue that the Fed's desire to avoid the social costs of disappointing private agents'
expectations can give rise to an exogenous source of variation in policy like that
captured by e7 . Specifically, shocks to private agents' expectations about Fed policy can
be self-fulfilling and lead to exogenous variations in monetary policy. A third source of
exogenous variation in Fed policy could reflect various technical factors. For one set of
possibilities, see Hamilton (1997). Another set of possibilities, stressed by Bernanke
and Mihov (1995), focuses on the measurement error in the preliminary data available
to the FOMC at the time it makes its decision.
We find it useful to elaborate on Bernanke and Mihov's suggestion for three reasons.
First, their suggestion is of independent interest. Second, we use it in Section 6 to
illustrate some of the difficulties involved in trying to interpret the parameters of
f Third, we use a version of their argument to illustrate how the interpretation of
monetary policy shocks can interact with the plausibility of alternative assumptions
for identifying e~.
Suppose the monetary authority sets the policy variable, G, as an exact function
of current and lagged observations on a set of variables, xt. We denote the time t
observations on xt and xt-1 by xt(O) and xt_ffl), where
xt(O) =x~+vt, x~_l(1) =x~_l +u,_l. (2.2)
So, vt represents the contemporaneous measurement error in xt, while ut represents the
measurement error in xt from the standpoint of period t + 1. Ifxt is observed perfectly
with a one period delay, then ut = 0 for all t. Suppose that the policy maker sets St
as follows:
St = fioSt_l q- ~ixt(O) + ~2xt 1(1). (2.3)
Expressed in terms of correctly measured variables, this policy rule reduces to
Equation (2.1) with:
f ( f2t) = 3oSt-1 + 31xt + 32xt-1, Os6 t = 31Ut + ~2Ut-1 • (2.4)
This illustrates how noise in the data collection process can be a source of exogenous
variation in monetary policy actions.
This example can be used to illustrate how one's interpretation of the error term
can affect the plausibility of alternative assumptions used to identify eZ. Recall the

Ch. 2: Monetary Policy Shocks: What Have we Learned and to What End? 73
recursiveness assumption, according to which e 7 is orthogonal to the elements of g2t.
Under what circumstances would this assumption be correct under the measurement
error interpretation of eT?
To answer this, suppose that vt and ut are classical measurement errors, i.e. they
are uncorrelated with xt at all leads and lags. If fi0 = 0, then the recursiveness
assumption is satisfied. Now suppose that fi0 e 0. If ut -- 0, then this assumption
is still satisfied. However, in the more plausible case where fi2 ~ 0, ut ~ 0 and ut and
vt are correlated with each other, then the recursiveness condition fails. This last case
provides an important caveat to measurement error as an interpretation of the monetary
policy shocks estimated by analysts who make use of the recursiveness assumption.
We suspect that this may also be true for analysts who do not use the recursiveness
assumption (see Section 5 below), because in developing identifying restrictions, they
typically abstract from the possibility of measurement error.
3. Vector autoregressions and identification
A fundamental tool in the literature that we review is the vector autoregression (VAR).
A VAR is a convenient device for summarizing the first and second moment properties
of the data. We begin by defining more precisely what a VAR is. We then discuss
the identification problem involved in measuring the dynamic response of economic
aggregates to a fundamental economic shock. The basic problem is that a given
set of second moments is consistent with many such dynamic response functions.
Solving this problem amounts to making explicit assumptions that justify focusing
on a particular dynamic response function.
A VAR for a k-dimensional vector of variables, Zt, is given by
Zt = B1Zt_I + ... q- BqZt-q-k blt, Eutu~ = E (3.1)
Here, q is a nonnegative integer and ut is uncorrelated with all variables dated t- 1
and earlier. 5 Consistent estimates of the Bi's can be obtained by running ordinary least
squares equation by equation on Equation (3.1). One can then estimate V from the
fitted residuals.
Suppose that we knew the Bi's, the ut's and V. It still would not be possible
to compute the dynamic response function of Zt to the fundamental shocks in the
economy. The basic reason is that ut is the one step ahead forecast error in Zt. In
general, each element of ut reflects the effects of all the fundamental economic shocks.
There is no reason to presume that any element of ut corresponds to a particular
economic shock, say for example, a shock to monetary policy.
5 For a discussion of the class of processes that VAR's summarize, see Sargent (1987). The absence
of a constant term in Equation (3.1) is without loss of generality, since we are free to set one of the
elements of Zt to be identically equal to unity.

74 L.J. Christiano et aL
To proceed, we assume that the relationship between the VAR disturbances and the
fundamental economic shocks, et, is given by Aout = et. Here, A0 is an invertible,
square matrix and Eete = D, where D is a positive definite matrix. 6 Premultiplying
Equation (3.1) by A0, we obtain:
AoZt = AIZt 1 -t- .. • + AqZ t q + E t. (3.2)
Here Ai is a k × k matrix of constants, i = 0,..., q and
Bi AolAi, i=l,...,q, and V=AoID(Aol) ' (3.3)
The response of Zt+h to a unit shock in et, Yh, can be computed as follows. Let ~h
be the solution to the following difference equation:
~/h=Bl~h L+'"+Bq)hq, h=l,2 .... (3.4)
with initial conditions
~0
-- 1, ~1 -- ~2 --" ~q = 0. (3.5)
Then,
Yh = ~hAo 1, h = 0, 1 ..... (3.6)
Here, the (j, l) element of Yh represents the response of the jth component of Z~+h to
a unit shock in the/th component of et. The gh's characterize the "impulse response
function" of the elements of Zt to the elements of et.
Relation (3.6) implies we need to know A0 as well as the Bi's in order to compute the
impulse response function. While the Bi's can be estimated via ordinary least squares
regressions, getting A0 is not so easy. The only information in the data about A0 is that
it solves the equations in (3.3). Absent restrictions on A0 there are in general many
solutions to these equations. The traditional simultaneous equations literature places
no assumptions on D, so that the equations represented by V = AolD (Ao 1) ~ provide no
information about A0. Instead, that literature develops restrictions on Ai, i = O, ..., q
that guarantee a unique solution to AoBi = Ai, i = 1, ..., q.
In contrast, the literature we survey always imposes the restriction that the
fundamental economic shocks are uncorrelated (i.e., D is a diagonal matrix), and places
no restrictions on Ai, i = 1. .... q. 7 Absent additional restrictions on A0 we can set
D = I. (3.7)
Also note that without any restrictions on the Ai's, the equations represented by
AoBi = Ai, i = 1, ..., q provide no information about A0. All of the information about
6 This corresponds to the assumption that the economic shocks are recoverable from a finite list of
current and past Zt 's. For our analysis, we only require that a subset of the et 's be recoverable from
current and past Zt's.
7 See Leeper, Sims and Zha (1996) for a discussion of Equation (3.7).

Ch. 2: MonetaryP olicy Shocks: What Have we Learned and to WhatE nd? 75
this matrix is contained in the relationship V = Ao 1 (A01) ~. Define the set of solutions
to this equation by
In general, this set contains many elements. This is because A0 has k 2 parameters while
the symmetric matrix, V, has at most k(k + 1)/2 distinct numbers. So, Qv is the set
of solutions to k(k + 1)/2 equations in k 2 unknowns. As long as k > 1, there will
in general be many solutions to this set of equations, i.e., there is an identification
problem.
To solve this problem we must find and defend restrictions on A0 so that there is
only one element in Qv satisfying them. In practice, the literature works with two types
of restrictions: a set of linear restrictions on the elements of A0 and a requirement that
the diagonal elements of A0 be positive. Suppose that the analyst has in mind l linear
restrictions on A0. These can be represented as the requirement rvec(A0) = 0, where
T is a matrix of dimension 1 × k 2 and vec(A0) is the k 2 x 1 vector composed of the k
columns of A0. Each of the l rows of T represents a different restriction on the elements
of A0. We denote the set of A0 satisfying these restrictions by:
Q~ = {A0 : rvec(A0) = 0}. (3.9)
In the literature that we survey, the restrictions summarized by ~ are either zero
restrictions on the elements of A0 or restrictions across the elements of individual rows
of A0. Cross equation restrictions, i.e., restrictions across the elements of different rows
of A0, are not considered.
Next we motivate the sign restrictions that the diagonal elements of A0 must be
strictly positive. 8 If Q~ n Qv is nonempty, it can never be composed of just a single
matrix. This is because irA0 lies in QvN Q~, then A0 obtained from A0 by changing
the sign of all elements of an arbitrary subset of rows of A0 also lies in Q~ N Qv. To
see this, let W be a diagonal matrix with an arbitrary pattern of ones and minus ones
along the diagonal. It is obvious that WAo E Q~. Also, because W is orthonormal (i.e.,
W'W = I), WAo E Qv as well.
Suppose we impose the restriction that the diagonal elements of A0 be strictly
positive. This rules out matrices A0 that are obtained from an A0 E Q~ N Qv by
changing the signs of all the elements of A0. In what follows we only consider A0
matrices that obey the sign restrictions. That is, we insist that Ao E Qs, where
Qs = {A0 :A0 has strictly positive diagonal elements}. (3.10)
From Equation (3.2) we see that the ith diagonal of A0 being positive corresponds to
the normalization that a positive shock to the ith element of et represents a positive
shock to the ith element of Zt when the other elements of Zt are held fixed.
s The following discussion ignores the possibility that Q~ N Qv contains a mataix with one or more
diagonal elements that are exactly zero. A suitable modification of the argument below can accommodate
this possibility.

76 L.J Christiano et al.
When there is more than one element in the set Qv A Qr N Qs we say that the system
is "underidentified", or, "not identified". When Qv N Qr N Qs has one element, we
say it is "identified". So, in these terms, solving the identification problem requires
selecting a r which causes the system to be identified.
Note that Qv n Qr is the set of solutions to k(k + 1)/2 + l equations in the k 2
unknowns of A0. In practice, the literature seeks to achieve identification by selecting
a full row rank ~ satisfying the order condition, l >~ k(k - 1)/2. However, the order and
sign conditions are not sufficient for identification. For example, when l = k(k- 1)/2
underidentification could occur for two reasons. First, a neighborhood of a given
Ao E Qv n Qr N Qs could contain other matrices belonging to Qv N Qr n Qs. This
possibility can be ruled out by verifying a simple rank condition, namely that the
matrix derivative with respect to A0 of the equations defining (3.8) is of full rank. 9
In this case, we say we have established local identification. A second possibility is
that there may be other matrices belonging to Qv n Q~ n Qs but which are not in
a small neighborhood of A0. ~0 In general, no known simple conditions rule out this
possibility. If we do manage to rule it out, we say the system is globally identified. 11
In practice, we use the rank and order conditions to verify local identification. Global
identification must be established on a case by case basis. Sometimes, as in our
discussion of Bernanke and Mihov (1995), this can be done analytically. More typically,
one is limited to building confidence in global identification by conducting an ad hoc
numerical search through the parameter space to determine if there are other elements
in Qv n Qr n Qs.
The difficulty of establishing global identification in the literature we survey
stands in contrast to the situation in the traditional simultaneous equations context.
9 Here we define a particular rank condition and establish that the rank and order conditions are
sufficient for local identification. Let a be the k(k + 1)/2 dimensional column vector of parameters in
A0 that remain free after imposing condition (3.9), so that Ao(a) C Qr for all a. Letf(a) denote the
k(k + 1)/2 dimensional row vector composed of the upper triangular part of A0(a ) 1 iAo(a) its_ V. Let
F(a) denote the k(k + 1)/2 by k(k + 1)/2 derivative matrix off(a) with respect to a. Let a* satisfy
f(a*) - O. Consider the following rank condition: F(a) has full rank for all a E D(a*), where D(a ~) is
some neighborhood of a*. We assume thatf is continuous and that F is well defined. A straightforward
application of the mean value theorem (see Bartle (1976), p. 196) establishes that this rank condition
guarantees f(a) ~ 0 for all a C D(a*) and a ,~ a*. Let gL : [.eL,eLI Rk(k+l)/2 be defined by
--+
gL(e) = f(a* + re), where ~ is an arbitrary non-zero k(k + 1)/2 column vector, and _eL and 2t are the
smallest and largest values, respectively, of e such that (a* + be) E D(a*). Note that g~(e) - trF(a* + te)
and e L < 0 < et. By the mean value theorem, gL(e) = gL(0) + g~(y)e for some 7 between 0 and e. This
can be written gt(e) = t~F(a * + ~e)e. The rank condition implies that the expression to the right of the
equality is nonzero, as long as e ~ 0. Since the choice of t e 0 was arbitrary, the result is established.
10 A simple example is (x - a) (x - b) = 0, which is one equation with two isolated solutions, x = a and
x-b.
11 We can also differentiate other concepts of identification. For example, asymptotic and small sample
identification correspond to the cases where V is the population and finite sample value of the variance
covariance matrix of the VAR disturbances, respectively. Obviously, asymptotic identification could hold
while finite sample identification fails, as well as the converse.

Ch. 2: Monetary Policy Shocks." What Haue we Learned and to What End? 77
There, the identification problem only involves systems of linear equations. Under
these circumstances, local identification obtains if and only if global identification
obtains. The traditional simultaneous equations literature provides a simple set of
rank and order conditions that are necessary and sufficient for identification. These
conditions are only sufficient to characterize local identification for the systems
that we consider. 12 Moreover, they are neither necessary nor sufficient for global
identification.
We now describe two examples which illustrate the discussion above. In the first
case, the order and sign conditions are sufficient to guarantee global identification.
In the second, the order condition and sign conditions for identification hold, yet the
system is not identified.
In the first example, we select z- so that all the elements above (alternatively, below)
the diagonal of Ao are zero. If, in addition, we impose the sign restriction, then it is
well known that there is only one element in Qv A Qr A Qs, i.e., the system is globally
identified. This result is an implication of the uniqueness of the Cholesky factorization
of a positive definite symmetric matrix. This example plays a role in the section on
identification of monetary policy shocks with a recursiveness assumption.
For our second example, consider the case k = 3 with the following restricted Ao
matrix:
al, 0 a13
Ao = 0 a22 a23/ '
0 a32 a33 J
where aii > 0 for i = 1,2, 3. Since there are three zero restrictions, the order condition
is satisfied. Suppose that Ao c Qv, so that Ao E Qv c-I Q~ cl Qs. Let W be a block
diagonal matrix with unity in the (1, 1) element and an arbitrary 2 x 2 orthonormal
matrix in the second diagonal block. Let W also have the property that WAo has positive
elements on the diagonal. Then, g~ = I, and WAo E Qv N Qr N Qs. 13 In this case
we do not have identification, even though the order and sign conditions are satisfied.
The reason for the failure of local identification is that the rank condition does not
hold. If it did hold, then identification would have obtained. The failure of the rank
condition in this example reflects that the second and third equations in the system are
indistinguishable.
12 To show that the rank condition is not necessary for local identification, consider f(x) = (x a) 2 .
For this function there is a globally unique zero at x - a, yetf~(a) = 0.
13 To see that this example is non empty, consider the case all - 0.70, a13 = 0.40, a22 - 0.38, a23 -- 0.50,
a32 = 0.83, a33 - 0.71 and let the 2 x 2 lower block in W be
I
0.4941 0.8694 I '
0.8694 -0.4941
It is easy to verify that WAo satisfies the zero and sign restrictions on A0 .

78 L.J. Christiano et al.
It is easy to show that every element in Qv n Qr n Qs generates the same dynamic
response function to the first shock in the system. To see this, note from Equation (3.5)
that the first column of Ao 1 is what characterizes the response of all the variables to
the first shock. Similarly, the first column of (WAo) ~ controls the response of the
transformed system to the first shock. But, the result (WA0) -1 = Ao 1 W t, and our
definition of W imply that the first columns of (WA0)- 1 and ofAo 1 are the same. So, if
one is only interested in the dynamic response of the system to the first shock, then the
choice of the second diagonal block of W is irrelevant. An extended version of this
observation plays an important role in our discussion of nonrecursive identification
schemes below.
4. The effects of a monetary policy shock: a recursiveness assumption
In this section we discuss one widely used strategy for estimating the effects of
a monetary policy shock. The strategy is based on the recursiveness assumption,
according to which monetary policy shocks are orthogonal to the information set of the
monetary authority. Section 4.1 discusses the relationship between the recursiveness
assumption and VARs. Section 4.2 describes three benchmark identification schemes
which embody the recursiveness assumption. In addition, we display estimates of
the dynamic effects of a monetary policy shock on various economic aggregates,
obtained using the benchmark identification schemes. Section 4.3 reviews some
results in the literature regarding the dynamic effects of a monetary policy shock on
other economic aggregates, obtained using close variants of the benchmark schemes.
Section 4.4 considers robustness of the empirical results contained in Section 4.2.
Section 4.5 discusses various critiques of the benchmark identification schemes.
Finally, Section 4.6 investigates the implications of the benchmark schemes for the
volatility of various economic aggregates.
4.1. The recursiveness assumption and VARs
The recursiveness assumption justifies the following two-step procedure for estimating
the dynamic response of a variable to a monetary policy shock. First, estimate the
policy shocks by the fitted residuals in the ordinary least squares regression of St
on the elements of £2t. Second, estimate the dynamic response of a variable to a
monetary policy shock by regressing the variable on the current and lagged values
of the estimated policy shocks.
In our analysis we find it convenient to map the above two-step procedure into an
asymptotically equivalent VAR-based procedure. There are two reasons for this. First,
the two-step approach implies that we lose a number of initial data points equal to the
number of dynamic responses that we wish to estimate, plus the number of lags, q, in
g2t. With the VAR procedure we only lose the latter. Second, the VAR methodology
provides a complete description of the data generating process for the elements of g2t.

Ch. 2: Monetary Policy Shocks." What Have we Learned and to What End? 79
This allows us to use a straightforward bootstrap methodology for use in conducting
hypothesis tests.
We now indicate how the recursiveness assumption restricts A0 in Equation (3.2).
Partition Zt into three blocks: the kl variables, Xlz, whose contemporaneous values
appear in g2t, the k2 variables, X2t , which only appear with a lag in £2t, and St itself.
Then, k = kl + k2 + 1, where k is the dimension of Zt. That is:
z'=/%
We consider kl, k2 > 0. To make the analysis interesting we assume that if kl = 0,
so that Xlt is absent from the definition of Zt, then k2 > 1. Similarly, if k2 = 0, then
kl > 1. The recursiveness assumption places the following zero restrictions on Ao •
all 0 0
(kl xkl) (kl x 1) (k~ xk2)
a21 a22 0
Ao = (lxk~) (1×1) (lxk2) (4.1)
17/3l a32 a33
(k2 ×kl) (k2 × 1) (k2 × k2)
Here, expressions in parentheses indicate the dimension of the associated matrix and
a22 = 1/G, where G > 0.
The zero block in the middle row of this matrix reflect the assumption that the policy
maker does not see X2t when St is set. The two zero blocks in the first row of Ao reflect
our assumption that the monetary policy shock is orthogonal to the elements in Xlt.
These blocks correspond to the two distinct channels by which a monetary policy shock
could in principle affect the variables in Xlt. The first of these blocks corresponds to
the direct effect of St on Xw The second block corresponds to the indirect effect that
operates via the impact of a monetary policy shock on the variables in X2~.
We now show that the recursiveness assumption is not sufficient to identify all the
elements of Ao. This is not surprising, in light of the fact that the first kl equations are
indistinguishable from each other, as are the last k2 equations. Significantly, however,
the recursiveness assumption is sufficient to identify the object of interest: the dynamic
response of Zt to a monetary policy shock. Specifically, we establish three results. The
first two are as follows: (i) there is a nonempty family of Ao matrices, one of which
is lower triangular with positive terms on the diagonal, which are consistent with the
recursiveness assumption i.e., satisfy Equation (4.1) and satisfy Ao 1 (A01) ' = V; and
(ii) each member of this family generates precisely the same dynamic response function
of the elements of Zt to a monetary policy shock. Result (iii) is that if we adopt the
normalization of always selecting the lower triangular Ao matrix identified in (i), then
the dynamic response of the variables in Zt are invariant to the ordering of variables
in J(lt and X2t.

80 L.J. Christiano et al.
To prove (i)-(iii) it is useful to establish a preliminary result. We begin by defining
some notation. Let the ((kl + 1)k2 + kl) × k 2 matrix r summarize the zero restrictions
on A0 in Equation (4.1). So, Qr is the set of A0 matrices consistent with the
recursiveness assumption. Let Qv be the set of A0 matrices defined by the property
that Aol(Aol) / see Equation (3.8). In addition, let
W = 0 1 0 , (4.2)
0 0 W33
where W is partitioned confonrlably with Ao in Equation (4.1) and WH and W33 are
arbitrary orthonormal matrices. Define
Q~0 = {A0 : A0 = WA0, for some W satisfying (4.2)}.
Here A0 is a matrix conformable with W.
We now establish the following result:
Q~o = Qv n Q~, (4.3)
where ~0 is an arbitrary element of Qv n Qr. It is straightforward to establish that
A0 E Q~0 implies A0 E Qv n Qr. The result, A0 E Qv follows from orthonormality of
W and the fact, ~0 E Qv. The result, A0 C Qr, follows from the block diagonal
structure of W in Equation (4.2). Now consider an arbitrary A0 C Qv n Qr. To
show that A0 E Q~0, consider the candidate orthonormal matrix W = A0~o 1, where
invertibility of ~0 reflects A0 E Qv. Since W is the product of two block-lower
triangular matrices, it too is block-lower triangular. Also, it is easy to verify that
WW / = /. The orthonormality of W, together with block-lower triangularity imply
that W has the form (4.2). This establishes A0 E Q~0 and, hence, Equation (4.3).
We now prove result (i). The fact that Qv n Qr is not empty follows from the
fact that we can always set A0 equal to the inverse of the lower triangular Cholesky
factor of V. The existence and invertability of this matrix is discussed in Hamilton
(1994, p. 91). 14 To see that there is more than one element in Qv n Qr, use the
characterization result (4.3), with A0 equal to the inverse of the Cholesky factor of
V. Construct the orthonormal matrix W ~ I by interchanging two of either the first
kl rows or the last k2 rows of the k-dimensional identity matrix. 15 Then, W~0 ¢ ~0.
Result (i) is established because W~0 E Qv N Qr.
14 The Cholesky factor of a positive definite, symmetric matrix, V, is a lower triangular matrix, C, with
the properties (i) it has positive elements along the diagonal, and (ii) it satisfies the property, CCI = V.
15 Recall, orthonormality of a matrix means that the inner product between two different columns is
zero and the inner product of any column with itself is unity. This property is obviously satisfied by the
identity matrix. Rearranging the rows of the identity matrix just changes the order of the terms being
added in the inner products defining orthonorrnality, and so does not alter the value of column inner
products. Hence a matrix obtained from the identity matrix by arbitrarily rearranging the order of its
rows is orthonormal.

Ch. 2: Monetary Policy Shocks: What Have we Learned and to What End? 81
We now prove result (ii). Consider any two matrices, Ao, ~4o E Qv N Qr. By
Equation (4.3) there exists a W satisfying Equation (4.2), with the property -40 = WAo,
so that
z01 = Ao I W t.
In conjunction with Equation (4.2), this expression implies that the (kl + 1)th column
of ~o 1 and Ao I are identical. But, by Equation (3.6) the implied dynamic responses
of Zt+i, i = 0, 1. ... to a monetary policy shock are identical too. This establishes
result (ii).
We now prove (iii) using an argument essentially the same as the one used to prove
(ii). We accomplish the proof by starting with a representation of Zt in which A0
is lower triangular with positive diagonal elements. We then arbitrarily reorder the
first kl and the last k2 elements of Zt. The analog to A0 in the resulting system
need not be lower triangular with positive elements. We then apply a particular
orthonormal transformation which results in a lower triangular system with positive
diagonal elements. The response of the variables in Zt to a monetary policy shock is
the same in this system and in the original system.
Consider Zt = DZ, where D is the orthonormal matrix constructed by arbitrarily
reordering the columns within the first kl and the last k2 columns of the identity
matrix. 16 Then, Zt corresponds to Zt with the variables in Xlt and X2t reordered
arbitrarily. Let Bi, i = 1. .... q and V characterize the VAR of Zt and let A0 be
the unique lower triangular matrix with positive diagonal terms with the property
Ao 1 (Aol) ~ = V. Given the Bi's, Ao characterizes the impulse response function of
the Zt's to et see Equations (3.4)-(3.6). The VAR representation of Zt, obtained by
suitably reordering the equations in (3.1), is characterized by DBiD ~, i = 1. .... q, and
DVD'. Iv Also, it is easily verified that (AoD') -t (AoD')-l ' = DVD', and that given the
DBiD ~'s, AoD ~ characterizes the impulse response function of the Zt's to et. Moreover,
these responses coincide with the responses of the corresponding variables in Zt to et.
Note that AoD ~ is not in general lower triangular. Let -40 = AoDq
[
nil 0 0
f40= ~2l ~22 0 ,
a31 a32 a33
where aii is full rank, but not necessarily lower triangular, for i = 1, 3. Let the QR
decomposition of these matrices be ?tu = QiRi, where Qi is a square, orthonormal
16 The type of reasoning in the previous footnote indicates that permuting the columns of the identity
matrix does not alter orthonormality.
17 To see this, simply premultiply Equation (3.1) by D on both sides and note that BiZ t i = BiOtDZt-i,
because D~D = L

82 L.J Christiano et aL
matrix, and Ri is lower triangular with positive elements along the diagonal. This
decomposition exists as long as ~lii , i = 1, 3, is nonsingular, a property guaranteed
1 00
by the fact Ao E Qv N Qr see Strang (1976), p. 124. 18 Let
W = 10 .
0 Q'
3
Note that WW '= I, (W.40) -a (W~0)-~ '= DVD', and WA0 is lower triangular with
L ~
positive elements along the diagonal. Since (W.~0) -1 = Ao 1 W I, the (kl + 1)th columns
of~o 1 W / and .~o I coincide. We conclude that, under the normalization that A0 is lower
diagonal with positive diagonal terms, the response of the variables in Zt to a monetary
policy shock is invariant to the ordering of variables in Xlt and X2t. This establishes
(iii).
We now summarize these results in the form of a proposition.
Proposition 4.1. Consider the sets Qv and Qr.
(i) The set Qv N Qr is nonempty and contains more than one element.
(ii) The (kl + 1)th column of 7i, i = O, 1, ... in Equation (3.6) is invariant to the
choice of Ao E Qv n Qr.
(iii) Restricting Ao E Qv n Qr to be lower triangular with positive diagonal terms, the
(kl + 1)th column of 7i, i = O, 1, ... is invariant to the ordering of the elements
in Xlt and X2t.
We now provide a brief discussion of (i)-(iii). According to results (i) and (ii), under
the recursiveness assumption the data are consistent with an entire family, Qz n QT,
of A0 matrices. It follows that the recursiveness assumption is not sufficient to pin
down the dynamic response functions of the variables in Zt to every element of et.
But, each Ao E Qv n QT does generate the same response to one of the et's, namely
the one corresponding to the monetary policy shock. In this sense, the recursiveness
assumption identifies the dynamic response of Zt to a monetary shock, but not the
response to other shocks.
In practice, computational convenience dictates the choice of some Ao E Qv n Qr.
A standard normalization adopted in the literature is that the A0 matrix is lower
triangular with nonnegative diagonal terms. This still leaves open the question of how
to order the variables in Xlt and X2t. But, according to result (iii), the dynamic response
of the variables in Zt to a monetary policy shock is invariant to this ordering. At
is Actually, it is customary to state the QR decomposition of the (n × n) matrix A as A = QR, where R
is upper triangular. We get it into lower triangular form by constructing the orthonormal matrix E with
zeros everywhere and 1' s in the (n + 1 - i, i)th entries, i = 1,2 ..... n, and writing A = (QE) (E~R). The
orthonormal matrix to which we refer in the text is actually QE.

Ch. 2: MonetaryP olicy Shocks: WhatH ave we Learned and to What End? 83
the same time, the dynamic impact on Zt of the nonpolicy shocks is sensitive to the
ordering of the variables in Xlt and Xzt. The recursiveness assumption has nothing to
say about this ordering. Absent further identifying restrictions, the nonpolicy shocks
and the associated dynamic response functions simply reflect normalizations adopted
for computational convenience.
4.2. Three benchmark identification schemes
We organize our empirical discussion around three benchmark recursive identification
schemes. These correspond to different specifications of St and g2t. In our first
benchmark system, we measure the policy instrument, St, by the time t federal
funds rate. This choice is motivated by institutional arguments in McCallum (1983),
Bernanke and Blinder (1992) and Sims (1986, 1992). Let Yt, Pt, PCOMt, FFt, TRt,
NBRt, and Mt denote the time t values of the log of real GDP, the log of the implicit
GDP deflator, the smoothed change in an index of sensitive commodity prices (a
component in the Bureau of Economic Analysis' index of leading indicators), the
federal funds rate, the log of total reserves, the log of nonborrowed reserves plus
extended credit, and the log of either M1 or M2, respectively. Here all data are
quarterly. Our benchmark specification of g2t includes current and four lagged values
of Y, Pt, and PCOMt, as well as four lagged values ofFFt, NBRt, TRt and Mr. We
refer to the policy shock measure corresponding to this specification as an FF policy
shock.
In our second benchmark system we measure St by NBRt. This choice is motivated
by arguments in Eichenbaum (1992) and Christiano and Eiehenbaum (1992) that
innovations to nonborrowed reserves primarily reflect exogenous shocks to monetary
policy, while innovations to broader monetary aggregates primarily reflect shocks to
money demand. We assume that f2t includes current and four lagged values of Yt, Pt,
and PCOMt, as well as four lagged values of FFt, NBRt, TRt and Mr. We refer to the
policy shock measure corresponding to this specification as an NBR policy shock.
Note that in both benchmark specifications, the monetary authority is assumed to
see Yt, Pt and PCOMt, when choosing St. 19 This assumption is certainly arguable
because quarterly real GDP data and the GDP deflator are typically known only with
a delay. Still, the Fed does have at its disposal monthly data on aggregate employment,
industrial output and other indicators of aggregate real economic activity. It also
has substantial amounts of information regarding the price level. In our view the
assumption that the Fed sees Yt and Pt when they choose St seems at least as plausible
as assuming that they don't. 20 Below we document the effect of deviating from this
benchmark assumption.
19 Examples of analyses which make this type of information assumption include Christiano and
Eichenbaum (1992), Christiano et al. (1996a, 1997a), Eichenbaum and Evans (1995), Strongin (1995),
Bernanke and Blinder (1992), Bernanke and Mihov (1995), and Gertler and Gilchfist (1994).
2o See for example the specifications in Sims and Zha (1998) and Leeper et al. (1996).

84 L.J Christiano et al.
Notice that under our assumptions, Yt, Pt and PCOMt do not change in the impact
period of either an FF or an NBR policy shock. Christiano et al. (1997b) present a
dynamic stochastic general equilibrium model which is consistent with the notion that
prices and output do not move appreciably in the impact period of a monetary policy
shock. The assumption regarding PCOMt is more difficult to assess on theoretical
grounds absent an explicit monetary general equilibrium model that incorporates a
market for commodity prices. In any event, we show below that altering the benchmark
specification to exclude the contemporaneous value of PCOMt from g2t has virtually
no effect on our results. 21
In the following subsection we display the time series of the two benchmark policy
shock estimates. After that, we study the dynamic response of various economic time
series to these shocks. At this point, we also consider our third benchmark system,
a variant of the NBR policy shocks associated with Strongin (1995). Finally, we
consider the contribution of different policy shock measures to the volatility of various
economic aggregates.
4.2.1. The benchmark policy shocks" displayed
We begin by discussing some basic properties of the estimated time series of the FF
and NBR policy shocks. These are obtained using quarterly data over the sample period
1965:3-1995:2. Figure 1 contains two time series of shocks. The dotted line depicts
the quarterly FF policy shocks. The solid line depicts the contemporaneous changes
in the federal funds rate implied by contractionary NBR policy shocks. In both cases
the variable Mt was measured as Mlt.
Since the policy shock measures are by construction serially uncorrelated, they tend
to be noisy. For ease of interpretation we report the centered, three quarter moving
average of the shock, i.e., we report (eT+l + e7 + el_ 1)/3. Also, for convenience we include
shaded regions, which begin at a National Bureau of Economic Research (NBER)
business cycle peak, and end at a trough. The two shocks are positively correlated, with
a correlation coefficient of 0.5 I. The estimated standard deviation of the FF policy
shocks is 0.71, at an annual rate. The estimated standard deviation of the NBR is 1.53%
and the standard deviation of the implied federal funds rate shock is 0.39, at an annual
rate.
In describing our results, we find it useful to characterize monetary policy as "tight"
or "contractionary", when the smoothed policy shock is positive, and "loose" or
"expansionary" when it is negative. According to the FF policy shock measure, policy
was relatively tight before each recession, and became easier around the time of the
trough. 22 A similar pattern is observed for the movements in the federal funds rate
21 This does not mean that excluding lagged values from £2~ has no effect on our results.
22 In Figure 1, the beginning of the 1973~4 recession appears to be an exception to the general pattern.
To some extent this reflects the effects of averaging since there was a 210 basis point FF policy shock
in 1973Q3.

Ch. 2: Monetary Policy Shocks." What Have we Learned and to What End? 85
2.0
1.5
1.0
0.5
x ~ k I
"E
0.o3
0.0
n I I I II / ~ I\ /
i'V7
-0.5 I i I
!,
I
II i I
NBR model --
- 1.0
Fed Funds model ....
- 1.5 7 I I I I I
6 4 81
Three-month centered, equal-weighted moving average
Fig. 1. Contractionary benchmark policy shocks in units of federal funds rate. The dotted line depicts
the quarterly FF policy shocks. The solid line depicts the contemporaneous changes in the federal funds
rate implied by contxactionary NBR policy shocks. In both cases the variable Mt was measured as M1 t.
implied by the NBR shocks, except that in the 1981-1982 period, policy was loose at
the start, very tight in the middle, and loose at the end of the recession.
4.2.2. What happens after a benchmark policy shock?
4.2.2.1. Results for some major economic aggregates. Figure 2 displays the estimated
impulse response functions of contractionary benchmark FF and NBR policy shocks
on various economic aggregates included in g2t. These are depicted in columns 1
and 2, respectively. Column 3 reports the estimated impulse response functions from
a third policy shock measure which we refer to as an NBR/TR policy shock. This
shock measure was proposed by Strongin (1995) who argued that the demand for total
reserves is completely interest inelastic in the short run, so that a monetary policy
shock initially only rearranges the composition of total reserves between nonborrowed
and borrowed reserves. Strongin argues that, after controlling for movements in certain
variables that are in the Fed's information set, a policy shock should be measured as the

86 L.J Christiano et al.
Fed Funds Model with M1 NBR Model with M1 NBR/TR Model with M1
0~ MP Shock => Y MP Shock => Y MP Shock => Y
~ \ - _ _-
6
MP Shock => Price MP Shock => Price MP Shock => Price
. . . . . . . . "~2--
0
MP Shock => Pcom MP Shock => Pcom MP Shock => Pcorn
iiil
iiij >--- f - r
\ . f .
MP Shock => FF MP Shock -> FF MP Shock => FF
°o°~ ~ \
MP Shock => NBR MP Shock => NBR MP Shock => NBR
os0
so / / /
o"~ / ~ ~ ~ ~ ' -i t/
o 3 9 12 1~
MP Shock => TR MP Shock => TR MP Shock =>TR
;~l .- ......... ]
00 +"
1:: o --- -6._ .... ~--.o ,~s 'o r r; . . . . . . 0 12' '1' 5 IS
MP Shock => M1 MP Shock => M1 MP Shock => M1
iit j. ..........
Fed Funds Model with M2 NBR Model with M2 NBR/TR Model with M2
MP Shock => M2 MP Shock => M2 MP Shock => M2
Fig. 2. The estimated impulse response functions of contractionary benchmark FF and NBR policy
shocks on various economic aggregates included in f2t (columns 1 and 2). Column 3 reports the estimated
impulse response functions from a third policy shock measure which we refer to as an NBR/TR policy
shock. The solid lines in the figure report the point estimates of the different dynamic response functions.
Dashed lines denote a 95% confidence interval for the dynamic response functions.

Ch. 2: Monetary Policy Shocks: What Have we Learned and to What End? 87
innovation to the ratio of nonborrowed to total reserves. We capture this specification
by measuring St as NBR and assuming that g2t includes the current value of TR. With
this specification, a shock to e[ does not induce a contemporaneous change in TR.
All three identification schemes were implemented using M1 and M2 as our measure
of money. This choice turned out to have very little effect on the results. The results
displayed in Figure 2 are based on a system that included M1. The last row of Figure 2
depicts the impulse response function of M2 to the different policy shock measures,
obtained by replacing M 1 with M2 in our specification of £2t. The solid lines in the
figure report the point estimates of the different dynamic response functions. Dashed
lines denote a 95% confidence interval for the dynamic response functions. 23
The main consequences of a contractionary FF policy shock can be summarized
as follows. First, there is a persistent rise in the federal funds rate and a persistent
drop in nonborrowed reserves. This finding is consistent with the presence of a strong
liquidity effect. Second, the fall in total reserves is negligible initially. But eventually
total reserves fall by roughly 0.3 percent. So according to this policy shock measure,
the Fed insulates total reserves in the short run from the full impact of a contraction
in nonborrowed reserves by increasing borrowed reserves. 24 This is consistent with
the arguments in Strongin (1995). Third, the response of M1 is qualitatively similar
to the response of TR. In contrast, for the M2 system, the FF policy shock leads to
an immediate and persistent drop in M2. Fourth, after a delay of 2 quarters, there is
a sustained decline in real GDE Notice the 'hump shaped' response function with the
maximal decline occurring roughly a year to a year and a half after the policy shock.
Fifth, after an initial delay, the policy shock generates a persistent decline in the index
of commodity prices. The GDP deflator is flat for roughly a year and a half after which
it declines.
23 These were computed using a bootstrap Monte Carlo procedure. Specifically,w e constructed 500 time
r
series on the vector Z t as follows. Let { t}t=l denote the vector of residuals from the estimated VAR.
We constructed 500 sets of new time series of residuals, {~t(j)}r 1, j = 1. ... ,500. The tth element of
{~t(J)}T 1 was selected by drawing randomly, with replacement, from the set of fitted residual vectors,
{ *}r,= 1. For each {~t(j)}tr_l, we constructed a synthetic time series of Zt, denoted {Zt(.J)}Tl, using
the estimated VAR and the historical initial conditions on Zt. We then re-estimated the VAR using
{Zt(j)}tr_l and the historical initial conditions, and calculated the implied impulse response functions
forj = 1, ..., 500. For each fixed lag, we calculated the 12th lowest and 487th highest values of the
corresponding impulse response coefficients across all 500 synthetic impulse response functions. The
boundaries of the confidence intervals in the figures correspond to a graph of these coefficients. In many
cases the point estimates of the impulse response functions are quite similar to the mean value of the
simulated impulse response functions. But there is some evidence of bias, especially for Y, M2, NBR
and FE The location of the solid lines inside the confidencei ntervals indicates that the estimated impulse
response functions are biased towards zero in each of these cases. See Killian (1998) and Parekh (1997)
for different procedures for accommodating this bias.
24 A given percentage change in total reserves corresponds roughly to an equal dollar change in the
total and nonborrowed reserves. Historically, nonborrowed reserves are roughly 95% of total reserves.
Since 1986, that ratio has moved up, being above 98% most of the time.

88 L.J. Christiano et al.
Before going on, it is of interest to relate these statistics to the interest elasticity of
the demand for NBR and M1. Following Lucas (1988, 1994), suppose the demand for
either of these two assets has the following form:
Mt = fM(g2t) - q)FF, + el,
where e/denotes the money demand disturbance and M denotes the log of either M1
or NBR. Here, q~ is the short run, semi-log elasticity of money demand. A consistent
estimate of q~ is obtained by dividing the contemporaneous response of Mt to a unit
policy shock by the contemporaneous response of FFt to a unit policy shock. This ratio
is just the instrumental variables estimate of q~ using the monetary policy shock. The
consistency of this estimator relies on the assumed orthogonality of e~' with eta and the
elements of g2t. 2s Performing the necessary calculations using the results in the first
column of Figure 2, we find that the short run money demand elasticities for M1 and
NBR are roughly -0.1 and -1.0, respectively. The M1 demand elasticity is quite small,
and contrasts sharply with estimates of the long run money demand elasticity. For
example, the analogous number in Lucas (1988) is -8.0. Taken together, these results
are consistent with the widespread view that the short run money demand elasticity is
substantially smaller than the long run elasticity [see Goodfriend (1991)].
We next consider the effect of an NBR policy shock. As can be seen, with two
exceptions, inference is qualitatively robust. The exceptions have to do with the impact
effect of a policy shock on TR and M 1. According to the FF policy shock measure,
total reserves are insulated, roughly one to one, contemporaneously from a monetary
policy shock. According to the NBR policy shock measure, total reserves fall by
roughly one half of a percent. Consistent with these results, an NBR policy shock leads
to a substantially larger contemporaneous reduction in M1, compared to the reduction
induced by an FF policy shock. Interestingly, M2 responds in very similar ways to an
FF and an NBR policy shock.
25 To see this, note first the consistency of the instrumental variables estimator:
Cov(M. eD
-qJ Cov(FFt, eT)"
Note too that:
Cov(Mt, el) : cpMa~, Cov(FFt, e;) : q)Rae2 ,
where q~M and q~R denote the contemporaneous effects of a unit policy shock on Mt and FFt, respectively,
and o 2 denotes the variance of the monetary policy shock. The result, that the instrumental variable
estimator coincides with q~m/cpR, follows by taking the ratio of the above two covariances. These results
also hold if Mr, FFt, and g2t are nonstationary. In this case, we think of the analysis as being conditioned
on the initial observations.

Ch. 2." Monetary Policy Shocks: What Have we Learned and to What End? 89
From column 3 of Figure 2 we see that, aside from TR and M1, inference is also
qualitatively similar to an NBR/TR policy shock. By construction TR does not respond
in the impact period of a policy shock. While not constrained, M 1 also hardly responds
in the impact period of the shock but then falls. In this sense the NBR/TR shock has
effects that are more similar to an FF policy shock than an NBR policy shock.
A maintained assumption of the NBR, FF and NBR/TR policy shock measures is that
the aggregate price level and output are not affected in the impact period of a monetary
policy shock. On a priori grounds, this assumption seems more reasonable for monthly
rather than quarterly data. So it seems important to document the robustness of
inference to working with monthly data. Indeed this robustness has been documented
by various authors. 26 Figure 3 provides such evidence for the benchmark policy
shocks. It is the analog of Figure 2 except that it is generated using monthly rather
than quarterly data. In generating these results we replace aggregate output with
nonfarm payroll employment and the aggregate price level is measured by the implicit
deflator for personal consumption expenditures. Comparing Figures 2 and 3 we see
that qualitative inference is quite robust to working with the monthly data.
To summarize, all three policy shock measures imply that in response to a
contractionary policy shock, the federal funds rate rises, monetary aggregates decline
(although some with a delay), the aggregate price level initially responds very little,
aggregate output falls, displaying a hump shaped pattern, and commodity prices fall.
In the next subsection, we discuss other results regarding the effects of a monetary
policy shock.
We conclude this subsection by drawing attention to an interesting aspect of our
results that is worth emphasizing. The correlations between our three policy shock
measures are all less than one (see, for example, Figure 1). 27 Nevertheless, all three
lead to similar inference about qualitative effects of a disturbance to monetary policy.
One interpretation of these results is that all three policy shock measures are dominated
by a common monetary policy shock. Since the bivariate correlations among the three
are less than one, at least two must be confounded by nonpolicy shocks as well.
Evidently, the effects of these other shocks is not strong enough to alter the qualitative
characteristics of the impulse response functions. It is interesting to us just how low
the correlation between the shock measures can be without changing the basic features
of the impulse response functions.
A similar set of observations emerges if we consider small perturbations to the
auxiliary assumptions needed to implement a particular identification scheme. For
example, suppose we implement the benchmark FF model in two ways: measuring Mt
by the growth rate of M2 and by the tog of M1. The resulting policy shock measures
26 See for example Geweke and Runkle (1995), Bernanke and Mihov (1995) and Christiano et al.
(1996b).
27 Recall, the estimated correlation between an FF and NBR shock is 0.51. The analog correlation
between anNBR / TR shock and anFF shock is 0.65. Finally, the correlation between anNBR/TR shock
and an NBR shock is 0.82.

90 L.J. Christiano et al.
Monthly Fed Funds Modet with M1 Mpnthly NBR Model with M1 Monthly NBR/TR Model with M1
MP Shock => EM MP Shock => EM MP Shock => EM
:::;J ............
MP Shock => Price MP Shock -> Price MP Shock -> Price
iit J ..........
'
MP Shock => Pcom MP Shock => Pcom MP Shock => Pcom
~ t
i "J"- -" ..... I
i!ii7 '--'~'J
MP Shock => FF MP Shock => FF MP Shock => FF
o,
MP Shock => NBR MP Shock => NBR MP Shock => NBR
::.71, . . . . . . . . . .....
MP Shock => TR MP Shock => TR MP Shock => TR
::7_ i. f- ...... 1 !~! s- .......
ooo ~ i oo l" ~ /
MP Shock => M1 MP Shock => M1 MP Shock => M1
Monthly Fed Funds Model with M2 Monthly NBR Model with M2 Monthly NBR/TR Model with M2
MP Shock => M2 MP Shock -> M2 MP Shock => M2
Fig. 3. Evidence for benchmark policy shocks. Analog of Figure 2, but using monthly rather than
quarterly data.
have a correlation coefficient of only 0.85. This reflects in part that in several episodes
the two shock measures give substantially different impressions about the state of

Ch. 2: Monetary Policy Shocks: What Have we Learned and to What End? 91
monetary policy. For example in 1993Q4, the M1 based shock measure implies a
20 basis point contractionary shock. The M2 growth rate based shock measure implies
an 80 basis point contractionary shock. These types of disagreements notwithstanding,
both versions of the benchmark FF model give rise to essentially the same inference
about the effect of a given monetary policy shock.
We infer from these results that while inference about the qualitative effects of a
monetary policy shock appears to be reliable, inference about the state of monetary
policy at any particular date is not.
4.3. Results for other economic aggregates
In the previous section we discussed the effects of the benchmark policy shocks on
various economic aggregates. The literature has provided a richer, more detaited picture
of the way the economy responds to a monetary policy shock. In this section we discuss
some of the results that have been obtained using close variants of the benchmark
policy shocks. Rather than provide an exhaustive review, we highlight a sample of the
results and the associated set of issues that they have been used to address. The section
is divided into two parts. The first subsection considers the effects of a monetary policy
shock on domestic US economic aggregates. In the second subsection, we discuss
the effects of a monetary policy shock on exchange rates. The papers we review use
different sample periods as well as different identifying assumptions. Given space
constraints, we refer the reader to the papers for these details.
4.3.1. US domestic aggregates
The work in this area can be organized into two categories. The first category pertains
to the effects of a monetary policy shock on different measures of real economic
activity, as well as on wages and profits. The second category pertains to the effects
of a monetary policy shock on the borrowing and lending activities of different agents
in the economy.
4.3.1.1. Aggregate real variables, wages and profits. In Section 4.2.2 we showed that
aggregate output declines in response to contractionary benchmark FF and NBR policy
shocks. Christiano et al. (1996a) consider the effects of a contractionary monetary
policy shock on various other quarterly measures of economic activity. They find
that after a contractionary benchmark FF policy shock, unemployment rises after a
delay of about two quarters. 28 Other measures of economic activity respond more
quickly to the policy shock. Specifically, retail sales, corporate profits in retail trade
28 Working with monthly data Bernanke and Blinder (1992) also find that unemployment rises after a
contractionary monetary policy shock. The shock measure which they use is related to our benchmark
FF policy shock measure in the sense that both are based on innovations to the Federal Funds rate and
both impose a version of the recursiveness assumption.

92 L.J Christiano et al.
and nonfinancial corporate profits immediately fall while manufacturing inventories
immediately rise. 29
Fisher (1997) examines how different components of aggregate investment respond
to a monetary policy shock see also Bernanke and Gertler (1995). He does so using
shock measures that are closely related to the benchmark FF and NBR policy measures.
Fisher argues that all components of investment decline after a contractionary policy
shock. But he finds important differences in the timing and sensitivity of different types
of investment to a monetary policy shock. Specifically, residential investment exhibits
the largest decline, followed by equipment, durables, and structures. In addition he
finds a distinctive lead-lag pattern in the dynamic response functions: residential
investment declines the most rapidly, reaching its peak response several quarters before
the other variables do. Fisher uses these results to discuss the empirical plausibility of
competing theories of investment.
Gertler and Gilchrist (1994) emphasize a different aspect of the economy's
response to a monetary policy shock: large and small manufacturing firms' sales
and inventories. 3° According to Gertler and Gilchrist, small firms account for
a disproportionate share of the decline in manufacturing sales that follows a
contractionary monetary policy shock. In addition they argue that while small
firms' inventories fall immediately after a contractionary policy shock, large firms'
inventories initially rise before falling. They use these results, in conjunction with other
results in their paper regarding the borrowing activities of large and small firms, to
assess the plausibility of theories of the monetary transmission mechanism that stress
the importance of credit market imperfections.
Campbell (1997) studies a different aspect of how the manufacturing sector responds
to a monetary policy shock: the response of total employment, job destruction and job
creation. Using a variant of the benchmark FF policy shock measure, Campbell finds
that, after a contractionary monetary policy shock, manufacturing employment falls
immediately, with the maximal decline occurring roughly a year after the shock. The
decline in employment primarily reflects increases in job destruction as the policy
shock is associated with a sharp, persistent rise in job destruction but a smaller,
transitory fall in job creation. Campbell argues that these results are useful as a guide
in formulating models of cyclical industry dynamics.
We conclude this subsection by discussing the effects of a contractionary monetary
policy shock on real wages and profits. Christiano et al. (1997a) analyze various
measures of aggregate real wages, manufacturing real wages, and real wages for ten
2 digit SIC level industries. In all cases, real wages decline after a contractionary
benchmark FF policy shock, albeit by modest amounts. Manufacturing real wages
29 The qualitative results of Christiano et al. (1996a) are robust to whether they work with benchmark
NBR, FF policy shocks or with Romer and Romer (1989) shocks.
3o Gert|er and Gilchrist (1994) use various monetary policy shock measures, including one that is related
to the benchmark FF policy shock as well as the onset of Romer and Romer (1989) episodes.

Ch. 2: Monetary Policy Shocks: What Have we Learned and to What End? 93
fall more sharply than economy-wide measures. Within manufacturing, real wages
fall more sharply in durable goods industries than in nondurable good industries.
Christiano et al. (1997a) argue that these results cast doubt on models of the monetary
transmission mechanism which stress the effects of nominal wage stickiness per se.
This is because those types of models predict that real wages should rise, not fall, after
a contractionary monetary policy shock.
To study the response of real profits to a monetary policy shock, Christiano et al.
(1997a) consider various measures of aggregate profits as well as before tax profits
in five sectors of the economy: manufacturing, durables, nondurables, retail and
transportation and utilities. In all but two cases, they find that a contractionary FF
policy shock leads to a sharp persistent drop in profits. 31 Christiano et al. (1997a)
argue that these results cast doubt on models of the monetary transmission mechanism
which stress the effects of sticky prices per se but don't allow for labor market frictions
whose effect is to inhibit cyclical movements in marginal costs. This is because those
types of models predict that profits should rise, not fall, after a contractionary monetary
policy shock.
Finally, we note that other authors have obtained similar results to those cited above
using policy shock measures that are not based on the recursiveness assumption. For
example, policy shock measures based on the identifying assumptions in Sims and Zha
(1998) lead to a qualitatively similar impact on wages, profits and various measures of
aggregate output as the benchmark FF policy shock. Similarly, Leeper, Sims and Zha's
(1996) results regarding the response of investment are quite similar to Fisher's.
4.3.1.2. Borrowing and lending activities. Various authors have investigated how a
monetary policy shock affects borrowing and lending activities in different sectors
of the economy. In an early contribution, Bernanke and Blinder (1992) examined
the effects of a contractionary monetary policy shock on bank deposits, securities
and loans. Their results can be summarized as follows. A contractionary monetary
policy shock (measured using a variant of the benchmark FF policy shock) leads to
an immediate, persistent decline in the volume of bank deposits as well as a decline
in bank assets. The decline in assets initially reflects a fall in the amount of securities
held by banks. Loans are hardly affected. Shortly thereafter security holdings begin
climbing back to their preshock values while loans start to fall. Eventually, securities
return to their pre-shock values and the entire decline in deposits is reflected in loans.
Bernanke and Blinder (1992) argue that these results are consistent with theories of the
monetary transmission mechanism that stress the role of credit market imperfections.
Gertler and Gilchrist (t993, 1994) pursue this line of inquiry and argue that a mon-
etary policy shock has different effects on credit flows to small borrowers (consumers
and small firms) versus large borrowers. Using a variant of the benchmark FF policy
31 The two exceptions are nondarable goods and transportation and utilities. For these industries they
cannot reject the hypothesis that profits are unaffected by contractionary policy shock.

94 L.J Christiano et al.
shock, they find that consumer and real estate loans fall after a contractionary policy
shock but commercial and industrial loans do not Gertler and Gilchrist (1993). In
addition, loans to small manufacturing firms decline relative to large manufacturing
firms after a contractionary monetary policy shock. In their view, these results support
the view that credit market imperfections play an important role in the monetary
transmission mechanism.
Christiano et al. (1996a) examine how net borrowing by different sectors of the
economy responds to a monetary policy shock. Using variants of the FF and NBR
benchmark policy shocks, they find that after a contractionary shock to monetary
policy, net funds raised in financial markets by the business sector increases for
roughly a year. Thereafter, as the decline in output induced by the policy shock gains
momentum, net funds raised by the business sector begin to fall. Christiano et al.
(1996a) argue that this pattern is not captured by existing monetary business cycle
models. 32 Christiano et al. (1996a) also find that net funds raised by the household
sector remains unchanged for several quarters after a monetary policy shock. They
argue that this response pattern is consistent with limited participation models of the
type discussed in Christiano et al. (1997a,b). Finally, Christiano et al. (1996a) show that
the initial increase in net funds raised by firms after a contractionary benchmark FF
policy shock coincides with a temporary reduction in net funds raised (i.e., borrowing)
by the government. This reduction can be traced to a temporary increase in personal
tax receipts. After about a year, though, as output declines further and net funds raised
by the business and household sectors falls, net funds raised by the government sector
increases (i.e., the government budget deficit goes up).
Taken together, the above results indicate that a contractionary monetary policy
shock has differential effects on the borrowing and lending activities of different agents
in the economy. Consistent with the version of the Lucas program outlined in the
introduction to this survey, these findings have been used to help assess the empirical
plausibility of competing theories of the monetary transmission mechanism.
4.3.2. Exchange rates and monetary policy shocks
Various papers have examined the effects of a monetary policy shock on exchange
rates. Identifying exogenous monetary policy shocks in an open economy can lead to
substantial complications relative to the closed economy case. For example, in some
countries, monetary policy may not only respond to the state of the domestic economy
but also to the state of foreign economies, including foreign monetary policy actions.
At least for the USA, close variants of the benchmark policy shock measures continue
to give reasonable results. For example, Eichenbaum and Evans (1995) consider
variants of the benchmark FF and NBR/TR policy shock measures in which some
32 Christiano et al. (1996a) and Gertler and Gilchrist (1994) discuss possible ways to account for this
response pattern.

Ch. 2: Monetary Policy Shocks: What Have we Learned and to What End? 95
foreign variables appear in the Fed's reaction ftmction. A maintained assumption of
their analysis is that the Fed does not respond contemporaneously to movements in the
foreign interest rate or the exchange rate. Eichenbaum and Evans use their policy shock
measures to study the effects of a contractionary US monetary policy shock on real
and nominal exchange rates as well as domestic and foreign interest rates. 33 They find
that a contractionary shock to US monetary policy leads to (i) persistent, significant
appreciations in US nominal and real exchange rates and (ii) persistent decreases in the
spread between foreign and US interest rates, and (iii) significant, persistent deviations
from uncovered interest rate parity in favor of US investments. 34 Under uncovered
interest rate parity, the larger interest rate differential induced by a contractionary
US monetary policy shock should be offset by expected future depreciations in the
dollar. Eichenbaum and Evans' empirical results indicate that the opposite is true:
the larger return is actually magnified by expected future appreciations in the dollar.
Eichenbaum and Evans discuss the plausibility of alternative international business
cycle models in light of their results.
While variants of the benchmark FF identification scheme generate results that
are consistent with traditional monetary analyses when applied to the USA, this is
generally not the case when they are used to identify foreign monetary policy shocks.
For example, Grilli and Roubini (1995) consider policy shock measures for non-US
G7 countries that are closely related to Eichenbaum and Evans' measures. Using these
measures, they find that a contractionary shock to a foreign country's monetary policy
leads initially to a depreciation in the foreign country's currency. Grilli and Roubini
argue that this result reflects that the measured policy shocks are confounded by the
systematic reaction of foreign monetary policy to US monetary policy and expected
inflation. This motivates them to construct an alternative policy shock measure which
is based on the recursiveness assumption and a measure of St equal to the spread
between foreign short term and long term interest rates. With this measure, they find
that a contractionary shock to foreign monetary policy leads to a transitory appreciation
in the foreign exchange rate and a temporary fall in output.
In contrast to Grilli and Roubini, authors like Cushman and Zha (1997), Kim and
Roubini (1995), and Ctarida and Gertler (1997) adopt identification schemes that do
not employ the recursiveness assumption. In particular, they abandon the assumption
that the foreign monetary policy authority only looks at predetermined variables when
setting its policy instrument. Cushman and Zha (1997) assume that Bank of Canada
officials look at contemporaneous values of the Canadian money supply, the exchange
rate, the US foreign interest rate and an index of world commodity prices when setting
a short term Canadian interest rate. Kim and Roubini (1995) assume that the reaction
33 The foreign countries which they look at are Japan, Germany, Italy, France and Great Britain.
34 Sims (1992) and Grilli and Roubini (1995) also analyze the effect of a monetary policy shock
on US exchange rates using close variants of the FF benchmark policy shock. They too fred that a
contractionary policy shock leads to an appreciation of the US exchange rate.

96 L.J Christiano et al.
function of foreign central bankers includes contemporaneous values of the money
supply, the exchange rate and the world price of oil (but not the federal fund rate).
Clarida and Gertler (1997) assume that the Bundesbank's reaction function includes
current values of an index of world commodity prices, the exchange rate, as well as
the German money supply (but not the US federal funds rate). 35 In all three cases, it is
assumed that the money supply and the exchange rate are not predetermined relative to
the policy shock. As a consequence, monetary policy shocks cannot be recovered from
an ordinary least squares regression. Further identifying assumptions are necessary to
proceed.
The precise identifying assumptions which these authors make differ. But in all
cases, they assume the existence of a group of variables that are predetermined relative
to the policy shock. 36 These variables constitute valid instruments for estimating the
parameters in the foreign monetary policy maker's reaction function. We refer the
reader to the papers for details regarding the exact identifying assumptions. 37
With their preferred policy shocks measures, all three of the above papers find
that a contractionary foreign monetary policy shock causes foreign exchange rates
to appreciate and leads to a rise in the differential between the foreign and domestic
interest rate. 38 In this sense, their results are consistent with Eichenbaum and Evans'
evidence regarding the effects of a shock to monetary policy. In addition, all three
papers provide evidence that a contractionary foreign monetary policy shock drives
foreign monetary aggregates and output down, interest rates up and affects the foreign
price level only with a delay. In this sense, the evidence is consistent with the
evidence in Section 4.2.2 regarding the effect of a benchmark FF policy shock on
the US economy.
4.4. Robustness of the benchmark analysis
In this subsection we assess the robustness of our benchmark results to various
perturbations. First, we consider alternative identification schemes which also impose
the recursiveness assumption. Second, we consider the effects of incorporating
information from the federal funds futures market into the analysis. Finally, we analyze
the subsample stability of our results.
35 Clarida et al. (1998) provide a different characterization of the Bundesbank's reaction function as
well as the reaction functions of five other central banks.
36 For example in all these cases it is assumed that a measure of commodity prices, foreign industrial
production, the foreign price level and the federal funds rate are predetermined relative to the foreign
monetary policy shock.
37 Clarida and Gall (1994) use long run identifying restrictions to assess the effects of nominal shocks
on real exchange rates.
38 Consistent with the evidence in Eichenbaum and Evans (1995), Cushman and Zha (1997) find that a
contractionary foreign monetary policy shock induces a persistent, significant deviation from uncovered
interest parity in favor of foreign investments.

Ch. 2: Monetary Policy Shocks: What Have we Learned and to What End? 97
4.4.1. Excluding current output and prices from f2t
The estimated one-step-ahead forecast errors in Yt and FFt are positively correlated
(.38), while those in Yt and NBRt are negatively correlated (-.22). Any identification
scheme in which St is set equal to either the time t federal funds rate or nonborrowed
reserves must come to terms with the direction of causation underlying this correlation:
Does it reflect (a) the endogenous response of policy to real GDP via the Fed's
feedback rule, or (b) the response of real GDP to policy? Our benchmark policy
measures are based on the assumption that the answer to this question is (a). Under
this assumption we found that a contractionary monetary policy shock drives aggregate
out-put down. Figure 4 displays the results when the answer is assumed to be (b).
Specifically, columns 1 and 3 report the estimated impulse response functions of
various economic aggregates to policy shock measures that were computed under the
same identification assumptions as those underlying the FF and NBR policy shocks
except that Yt is excluded from f2t. The key result is that under these identifying
assumptions, a contractionary policy shock drives aggregate output up before driving
it down. In other respects, the results are unaffected.
It might be thought that the initial response pattern of output could be rationalized by
monetary models which stress the effects of an inflation tax on economic activity, as in
Cooley and Hansen (1989). It is true that in these models a serially correlated decrease
in the money supply leads to an increase in output. But, in these models this happens
via a reduction in anticipated inflation and in the interest rate. Although the candidate
policy shock is associated with a serially correlated decrease in the money supply, it is
also associated with a rise in the interest rate and virtually no movement in the price
level. This response pattern is clearly at variance with models in which the key effects
of monetary policy shocks are those associated with the inflation tax. We do not know
of other models which can rationalize a rise in output after a contractionary monetary
policy shock. Absent some coherent model that can account for the response functions
in columns 1 and 3 of Figure 4, we reject the underlying identifying assumptions as
being implausible. We suspect that the resulting shock measures confound policy and
nonpolicy disturbances.
Columns 2 and 4 of Figure 4 report the estimated impulse response functions to
policy shock measures computed under the same identification assumptions as those
underlying the FF and NBR policy shocks except that Pt is excluded from f2t. As can
be seen, the benchmark results are virtually unaffected by this perturbation.
4.4.2. Excluding commodity prices from g-2t: The price puzzle
On several occasions in the postwar era, a rise in inflation was preceded by a rise in
the federal funds rate and in commodity prices. An example is the oil price shock in
1974. Recursive identification schemes that set St equal to FFt and do not include the
commodity prices in f2t as leading indicators of inflation in the Fed's feedback rule
sometimes imply that contractionary monetary policy shocks lead to a sustained rise in

98 L.J. Christiano et al.
Fed Funds Model, Y after MP Fed Funds Model, P after MP NBR Model, Y after MP NBR Model, P after MP
MP Shock => Y MP Shock => Y o~ MP Shock =~ Y MP Shock =>Y
o1 \
2:
° , ° + ,~ ,,
MP Shock => Price MP Shock => Price MP Shock => Price MP Shock => Price
ii: :i
il +"F 2 ~-~===--: 1
iil. ....: > - A
.......... _
MP Shock => Pcom MP Shock => Pcom MP Shock => Pcom MP Shock => Pcom
r
'+--" .... iit '-"
o + , + +, ,,
MP Shock => FF MP Shock => FF MP Shock => FF MP Shock => FF
°+ /\ ',iw
o,+ /\
+,+ \ /
2:
::L_ _'_- - - ...... I Z .... "~2Y,ZT 7 7 +--~ . . . .
o , , + ,~ ,s
MP Shock => NBR MP Shock=> NBR
/ /
Z /
~i +j
0 3 ~ 9 12 I~ . . . . . . . + o , + + ,~ ,+
MP Shock => TR MP Shock => TR
Z / .....
°"I \ // +" \/ //
.-°. .... _ ....
MP Shock => M1 MP Shock => ml MP Shock => M1 MP Shock => ml
"® j // "~t //
i . . . . . 0~/ X/J
0 , + + ,= ,.
Fig. 4. Results when the answer is assumed to be the response of real GDP to policy. Columns 1
and 3 report the estimated impulse response functions of various economic aggregates to policy shock
measures that were computed under the same identification assumptions as those underlying the FF and
NBR policy shocks except that Yt is excluded from Qt. Columns 2 and 4 report the estimated impulse
response functions to policy shock measures computed under the same identification assumptions as
those underlying the FF and NBR policy shocks except that Pt is excluded from ~2t . As can be seen,
the benchmark results are virtually unaffected by this perturbation.

Ch. 2: Monetary Policy Shocks: What Have we Learned and to What End? 99
the price level. 39 Eichenbaum (1992) viewed this implication as sufficiently anomalous
relative to standard theory to justify referring to it as "the price puzzle". 4o Sims (1992)
conjectured that prices appeared to rise after certain measures of a contractionary
policy shock because those measures were based on specifications of g2t that did not
include information about future inflation that was available to the Fed. Put differently,
the conjecture is that policy shocks which are associated with substantial price puzzles
are actually confounded with nonpolicy disturbances that signal future increases in
prices. Christiano et al. (1996a) and Sims and Zha (1998) show that when one modifies
such shock measures by including current and lagged values of commodity prices in
Dr, the price puzzle often disappears. It has now become standard practice to work
with policy shock measures that do not generate a price puzzle.
To document both the nature of the puzzle and the resolution, Figure 5 displays
the impulse response of Pt to eight different contractionary monetary policy shock
measures. The top and bottom rows display the effects of shocks to systems in which St
is measured by FFt and NBRt, respectively. Columns 1-4 correspond to policy shock
measures in which (i) the current value of Pt, Yt and current and lagged values of
PCOMt are omitted from g2t, (ii) current and lagged values of PCOMt are omitted
from £2¢, (iii) the current value of PCOMt is omitted from £2t, and (iv) g2t is given by
our benchmark specification, respectively.
A number of interesting results emerge here. First, policy shock measures based
on specifications in which current and lagged values of PCOM are omitted from g2t
imply a rise in the price level that lasts several years after a contractionary policy shock.
Second, according to the point estimates, the price puzzle is particularly pronounced
for the specification in which the current values of Yt and Pt are also excluded from
g2t (column 1). Recall that deleting Pt from (2t had virtually no effect on our results.
These findings suggest that current Y and current and past PCOM play a similar role in
purging policy shock measures of nonpolicy disturbances. Third, the 95% confidence
intervals displayed in Figure 5 indicate that the price puzzle is statistically significant
for the Fed Funds based shock measures associated with columns 1 and 2 in Figure 5.41
39 The first paper that documents the "price puzzle" for the USA and several other countries appears
to be Sims (1992).
4o There do exist some models that predict a temporary rise in the price level after a contraction. These
models stress the role of self fulfilling shocks to expectations in the monetary transmission mechanism.
See for example Beaudry and Devereux (1995). Also there exist some limited participation models of
the monetary transmission mechanism in which the impact effect of contractionary monetary policy
shocks is so strong that prices rise in the impact period of the policy shock. See for example Fuerst
(1992) and Christiano et al. (1997a).
4~ We used the artificial data underlying the confidence intervals reported in Figure 5 to obtain a different
test of the price puzzle. In particular, we computed the number of times that the average price response
over the first 2, 4 and 6 quarters was positive. For the FF model underlying the results in column 1 the
results were 96.4%, 97.2%, and 98.0%, respectively. Thus, at each horizon, the price puzzle is significant
at the 5% significance level. For the FF model underlying the second column, the results are 95.6%,
94.6%, and 89.8%, so that there is a marginally significant price puzzle over the first year. Regardless

100 L.J. Christiano et al.
Fed Funds, MP first: No Pcom Fed Funds,: No Pcom Fed Funds: Pcom after MP Fed Funds with M1
MP Shock => P MP Shock -> P MP Shock => P MP Shock => P
0.70 0.70 I 0.70 [ 0.70
/
0.35
0.35 / 0,35 ' 0.35
oo0
0.00 , ~ - 0.00 ~ / ~
\x
\\ ~°°°l
-0.35 x 0.35 -0.35 \
-0.70 , -0.70 0.70 ~
4 7 10 13 1 4 7 10 13 1 4 7 10 13 1 4 7 10 13
quarters quarters quarters quarters
NBR. MP first: No Pcom NBR: NO Pcom NBR: Pcom after MP NBR with M1
MP Shock => P MP Shock => P MP Shock => P MP Shock => P
0.70 0.70 0.70 0.70
0.35 0.35 0.35
$ 0.00
0.35 -0.35 -0.35 \~\~\~
-0.70 -0,70 . . . . .4. i . . . . . . rv -0.70 , . . . . . . . . . . . . . .
1 4 7 10 13 1 4 7 10 13 1 7 10 13 1 4 7 10 13
quarters quarters quarters quarters
Fig. 5. The impulse response of Pt to eight different contractionary monetary policy shock measures.
The top and bottom rows display the effects of shocks to systems in which S t is measured by FF t and
NBRt, respectively. Columns 1-4 correspond to policy shock measures in which (i) the current value of
Pt, Yt and current and lagged values ofPCOM t are omitted from g2t, (ii) current and lagged values of
PCOM t are omitted from E2t, (iii) the current value of PCOM t is omitted from g2,, and (iv) ~2t is given
by our benchmark specification, respectively.
Fourth, consistent with results in Eichenbaum (1992), the price puzzle is less severe
for the NBR based policy shocks. Fifth, little evidence of a price puzzle exists for the
benchmark FF and NBR policy shocks.
We conclude this section by noting that, in results not reported here, we found that
the dynamic responses of nonprice variables to monetary policy shocks are robust to
deleting current and lagged values of PCOM from £2t.
4.4.3. Equating the policy instrument, St, with MO, M1 or M2
There is a long tradition of identifying monetary policy shocks with statistical
innovations to monetary aggregates like the base (M0), M 1 and M2. Indeed this was
of the horizon, the price puzzle was not significant at even the 10% significance level for the other
specifications in Figure 5.

Ch. 2: Monetary Policy Shocks: What Have we Learned and to What End? 101
the standard practice in the early literature on the output and interest rate effects of an
unanticipated shock to monetary policy. 42 This practice can be thought of as setting St
equal to a monetary aggregate like M0, M1 or M2 and using a particular specification
of Y2t. We refer the reader to Leeper, Sims and Zha (1996) and Cochrane (1994) for
critical reviews of this literature.
Here we discuss the plausibility of identification schemes underlying M based policy
shock measures by examining the implied response functions to various economic
aggregates. Figure 6 reports estimated response functions corresponding to six policy
measures. Columns 1 and 2 pertain to policy shock measures in which St is set equal
to M0t. Column 1 is generated assuming that g2t consists of 4 lagged values of Yt, Pt,
PCOMt, FFt, NBRt and M0t. For column 2, we add the current value of Yt, Pt, and
PCOMt to g2t. Columns 3 and 4 are the analogs of columns 1 and 2 except that M0t
is replaced by Mlt. Columns 5 and 6 are the analogs of columns 1 and 2 except that
MOt is replaced by M2.
We begin by discussing the dynamic response functions corresponding to the M0
based policy shock measures. Notice that the responses in column 1 are small and
estimated very imprecisely. Indeed, it would be difficult to reject the hypotheses
that Y, P, PCOM, and FF are all unaffected by the policy shock. Once we take
sampling uncertainty into account, it is hard to argue that these response functions
are inconsistent with the benchmark policy shock measure based response functions.
In this limited sense, inference is robust. Still, the point estimates of the response
functions are quite different from our benchmark results. In particular, they indicate
that a contractionary policy shock drives Pt and FFt down. The fall in Pt translates
into a modest decline in the rate of inflation. 43 After a delay of one or two periods,
Zt rises by a small amount. The delay aside, this response pattern is consistent with a
simple neoclassical monetary model of the sort in which there is an inflation tax effect
on aggregate output see for example Cooley and Hansen (1989).
The response functions in column 2 are quite similar to those in column 1. As
before, they are estimated with sufficient imprecision that they can be reconciled with
various models. The point estimates themselves are consistent with simple neoclassical
monetary models. Compared to column 1, the initial decline in Yt after a contractionary
policy shock is eliminated, so that the results are easier to reconcile with a simple
neoclassical monetary model.
The impulse response fimctions associated with the M1 based policy shocks in
columns 3 and 4 are similar to those reported in columns t and 2, especially when
sampling uncertainty is taken into account. The point estimates themselves seem harder
to reconcile with a simple monetary neoclassical model. For example, according to
42 See for example Barro (1977), Mishkin (1983), S. King (1983) and Reichenstein (1987). For more
recent work in this tradition see King (1991) and Cochrane (1994).
43 The fall in P~ translates into an initial .20 percent decline in the annual inflation rate. The maximal
decline in the inflation rate is about .25 percent which occurs after 3 periods. The inflation rate returns
to its preshock level after two years.

102 L.J. Christiano et al.
Money Model: MO first Money Model Money Model: M1 first
M0 Shock => Y MO Shock => Y M1 Shock => Y
/
/--' ./
o 3 e • ,2 ,~
MO Shock => Price M0 Shock => Price MI ShOCk => Price
]]
.--'" o,
I
/
f
1
MO Shock => PCOM M0 Shook => PCOM Mf ShOck => PCOM
kt i l ~
ijI -
M0 Shock => FF MO Shock => FF M1 Shock => FF
/
/
\ \\l'~. l " / ~ \ ~- I "~, / ~ I
o 3 e ~ I= ,5
M0 Shock => NBR M0 Shock => NBR M1 Shock => NBR
. ~ . . 1= ,i
M0 Shock => M0 MO Shock => M0 M1 Shock => M1
I
f
jl i i
i /
Fig. 6. Estimated response fimctions corresponding to six policy measures.

Ch. 2: Monetary Policy Shocks." What Have we Learned and to What End? 103
Money Model Money Model: M2 first Money Model
M1 Shock => Y M2 Shock => Y M2 Shock => Y
/,/ . //
M1 Shock => Price M2 Shock => Price M2 Shock => Price
/ f f
, 3 t , ,~ is 0 ~ e • 12 is
M1 Shock => PCOM M2 Shock => PCOM M2 Shock => PCOM
o° \, .I
0 ~ 4 t 12 IS o a i • I= ,s
M1 Shock => FF M2 Shock => FF M2 Shock => FF
"~,.~ t/, ~'~ ../ >.-~r?
° 3 g = I~ i~ .o. . . . .~ e = .1.2 . . ,s
M1 Shock => NBR M2 Shock => NBR M2 Shock => NBR
o® //
~"=t 1 ....
I~ 1 \ ~ - - ~
o ~ ~ 9 12 .
M1 Shock => M1 M2 Shock => M2 M2 Shock => M2
°I
\ ~ / j /
~=

104 L.J. Christiano et al.
column 3, output falls for over two quarters after a contractionary policy shock. The
fact that output eventually rises seems difficult to reconcile with limited participation
or sticky wage/price models. This is also true for the results displayed in column 4.
Moreover, the results in that column also appear to be difficult to reconcile with the
neoclassical monetary model. For example, initially inflation is hardly affected by a
monetary contraction, after which it actually rises. Sampling uncertainty aside, we
conclude that the MI based policy shock measures are difficult to reconcile with known
(at least to us) models of the monetary transmission mechanism.
Finally, consider the M2 based policy shock measures. Here a number of interesting
results emerge. First, the impulse response functions are estimated more precisely
than those associated with the M0 and M1 based policy shock measures. Second, the
impulse response functions share many of the qualitative properties of those associated
with the benchmark policy shocks measures. In particular, according to both columns 5
and 6, a contractionary monetary policy shock generates a prolonged decline in output
and a rise in FFt. Also the price level hardly changes for roughly 3 quarters. This is
true even for the policy shock measure underlying column 5 where the price level is
free to change in the impact period of the shock. There is one potentially important
anomaly associated with the M2 based policy shock measures: after a delay, NBR and
M2 move in opposite directions.
In sum, the M based policy shock measures provide mixed evidence on the
robustness of the findings associated with our benchmark policy shocks. The response
functions associated with the M0 and M1 policy shock measures are estimated
quite imprecisely. In this sense they do not provide evidence against robustness. The
point estimates of the response functions associated with the M1 based policy shock
measures are hard to reconcile with existing models of the monetary transmission
mechanism. But the point estimates associated with the M0 based policy shock
measures are consistent with simple neoclassical monetary models. If one wants
evidence that is not inconsistent with simple neoclassical monetary models, this is
where to look. Finally, apart from the anomalous response of NBR, qualitative inference
about the effects of a monetary policy shock are robust to whether we work with the
M2 based policy shock measure or the benchmark policy shock measures.
4.4.4. Using information from the federal funds futures market
An important concern regarding the benchmark policy shock measures is that they
may be based on a smaller information set than the one available to the monetary
authority or private agents. Rudebusch (1996) notes that one can construct a market-
based measure of the one-month ahead unanticipated component of the federal fimds
rate. He does so using data from the federal funds futures market, which has been active
since late 1988. 44 He recognizes that a component of the unanticipated move in the
44 See Brunner (1994), Carlson et al. (1995), and Krueger and Kuttner (1996) for further discussion
and analysis of the federal funds futures market.

Ch. 2: Monetary Policy Shocks: What Have we Learned and to What End? 105
federal funds rate reflects the Federal Reserve's endogenous response to the economy.
To deal with this problem, he measures the exogenous shock to monetary policy as the
part of the unanticipated component of the federal funds rate which is orthogonal to a
measure of news about employment. In Rudebusch's view, the correlation between the
resulting measure and our FF benchmark policy shock measure is sufficiently low to
cast doubt upon the latter. 45 But policy shock measures can display a low correlation,
while not changing inference about the economic effects of monetary policy shocks.
We now investigate whether and how inference is affected by incorporating federal
funds futures market data into the analysis.
To study this question, we repeated the benchmark FF analysis, replacing FFt with
FFt -FMt-1 in the underlying monthly VAR. 46 Here FMt_I denotes the time t- 1
futures rate for the average federal funds rate during time t. 47 We refer to the orthog-
onalized disturbance in the FFt - FM¢ I equation as the FM policy shock. In addition,
because of data limitations, we redid the analysis for what we refer to as the Rudebusch
sample period, 1989:04-1995:03. Because of the short sample period, we limit the
number of lags in the VAR to six. Before considering impulse response functions to the
policy shocks, we briefly discuss the shocks themselves. Panel A of Figure 7 displays
the FM policy shocks for the period 1989:10-1995:03. In addition, we display FF pol-
icy shocks for the same period. These were computed using our benchmark, monthly
VAR model, estimated over the whole sample period, using six lags in the VAR.
Panel B is the same as Panel A, except that the VAR underlying the benchmark FF
policy shocks is estimated using data only over the Rudebusch sample period.
A few features of Figure 7 are worth noting. First, the shock measures in Panel A
are of roughly similar magnitude, with a standard deviation of the benchmark and
FM policy shocks being 0.22 and 0.16, respectively. Consistent with the type of
findings reported by Rudebusch, the correlation between the two shock measures
is relatively low, 0.34. 48 Second, when we estimate the VARs underlying the
benchmark FF and FM policy shocks over the same sample period, the correlations
rise to approximately 0.45. Interestingly, the FF policy shocks now have a smaller
standard deviation than the FM policy shocks. 49
We now proceed to consider robustness of inference regarding the effects of
monetary policy shocks. The dynamic response functions to an FM policy shock,
together with 95% confidence intervals, are displayed in column 1 of Figure 8. There
45 See Sims (1996) for a critique of Rudebusch's analysis.
46 Evans and Kuttner (1998) find that small, statistically insignificant deviations from futures market
efficiency partially account for the low correlations between variants of the FF benchmark policy shocks
and FF~ - FMt 1.
47 These data were taken from Krueger and Kuttner (1996).
48 Rudebusch actually reports the R2 in the regression relation between the two shocks. This is the
square of the correlation between the two variables. So, our correlation translates into an R2 of 0.12.
49 Given the short sample, it is important to emphasize that the standard deviations have been adjusted
for degrees of freedom.

L.d Christiano et al.
106
1.00
CEE66 " / 66 startdate, 6 lags
0.75
RUDE EPS
0.50
0.25
0.00
-0.25
-0.50
-0.75
-1.00
90 92 94
, _
E89 -1 89 startdate, 6 lags
0.75 4~
/ FIUDE EPS .... ]
0.50 ~L__ -- _ _ _ _ J
0,25 ~ /~
-0.25 1 ~ : ~
-050 '" V
-0.75 J
I
-1.00 '
90 92 94
Fig. 7. Top: the FM policy shocks for the period 1989:10-1995:03. In addition, we display FF policy
shocks for the same period. These were computed using our benchmark, monthly VAR model, estimated
over the whole sample period, using six lags in the VAR. Bottom: the same as top, except that the VAR
underlying the benchmark FF policy shocks is estimated using data only over the Rudebusch sample
period.
are two obvious features to these results. First, the policy shock itself is very small (a
little over 10 basis points). Second, with the exception of FFL- FMt-1, the response
of the other variables is not significantly different from zero at all lags.
To compare these results with those based on the benchmark FF policy shocks, we
need to control for the difference in sample periods and lag lengths. To this end, we
report the impulse response functions and standard errors of the 6 lag benchmark FF
model estimated over the Rudebusch sample period. These are displayed in column 2
of Figure 8. We see that the same basic message emerges here as in column 1:
over the Rudebusch sample period, the shocks are small and the impulse response
functions are imprecisely estimated. We conclude that there is no evidence to support

Ch. 2: Monetary Policy Shocks." What Haue we Learned and to What End? 107
Short Sample Rudebusch FM Model Short FF Model, short sample confidence Short FF Mode~, fu~l sample confidence Short FF Model, bootsub3 confidence
MP Sh~k => EM MP Shock => EM MP Shock => EM MP Shock => EM
[ f
MP Shock => Price MP Shock => Price MP Shock => Pdce MP Shock => Price
°~7--
i: ........................................ I ::i .................................. I 1111.. ..........~ ,:,~,~,~ i
MP Shock => Pcom MP Shock => Pcom MP Shock ~ Pcom MP Shock => Poem
°'°I 1
=o.t.,
MP Shock => Rudebusch Shocks MP Shock => FF MP Shock => FF MP Shock => FF
t°
i
°~ X ~
MP Shock => NBR MP Shock => NBR MP Shock => NBR MP Shock => NBR
~ii I 1:2 ~ ............. ~':1
....................... .... ' iiil/~:,~,:r.~r:~,;,
M P Shock => TR MP Shock => TR MP Shock => TR MP Sh~k =>TR
o~ o~
J
~o.~, mo.~ . . . . ,., ~o,th,
MP Shock => MI MP Shock => M1 MP Shock => M1 MP Shock =, M1
i q ~ r !
2 tl ~ ~g 3~
monks
Fig. 8. The dynamic response functions to an FM policy shock, together with 95% confidence intervals,
are displayed in column 1. There are two obvious features to these results. First, the policy shock itself
is very small (a little over 10 basis points). Second, with the exception ofFF t -FM~ 4, the response of
the other variables is not significantly different from zero at all lags.

108 L.J. Christiano et al.
the notion that inference is sensitive to incorporating federal funds market data into the
analysis. This conclusion may very well reflect the limited data available for making
the comparison.
4.4.5. Sample period sensitioity
Comparing the results in Figure 8 with our full sample, benchmark FF results (see
column 1, Figure 2) reveals that the impulse response functions are much smaller in
the Rudebusch sample period. A similar phenomenon arises in connection with our
benchmark NBR model. Pagan and Robertson (1995) characterize this phenomenon
as the "vanishing liquidity effect". Wong (1996) also documents this phenomenon for
various schemes based on the recursiveness assumption. These findings help motivate
the need to study the robustness of inference to different sample periods.
We now proceed to investigate subsample stability. Our discussion is centered
around two general questions. First, what underlies the difference in impulse response
functions across subsamples? Here, we distinguish between two possibilities. One
possibility is that the difference reflects a change in the size of the typical monetary
policy shock. The other possibility is that it reflects a change in the dynamic
response to a shock of a given magnitude. We will argue that, consistent with
the findings in Christiano's (1995) discussion of the vanishing liquidity effect, the
evidence is consistent with the hypothesis that the first consideration dominates.
Second, we discuss robustness of qualitative inference. Not surprisingly in view
of our findings regarding the first question, we find that qualitative inference
about the effects of a monetary policy shock is robust across subsamples. This
last finding is consistent with results in Christiano et al. (1996b). In the analysis
that follows, we focus primarily on results for the benchmark FF policy shocks.
We then briefly show that our conclusions are robust to working with the NBR
policy shocks.
To begin our analysis of subsample stability, we test the null hypothesis that there
was no change at all in the data generating mechanism for the Rudebusch sample
period. To this end, we constructed confidence intervals for the impulse response
functions in column 2 of Figure 8 under the null hypothesis that the true model
is the one estimated using data over the full sample. 50 The resulting confidence
intervals are reported in column 3. In addition, that column reports for convenience
the estimated response functions from column 2. We see that the estimated impact
effect of a one standard deviation policy shock on the federal funds rate (see the
so These confidence intervals were computed using a variant of the standard bootstrap methodology
employed in this paper. In particular, we generated 500 artificial time series, each of length equal to
that of the full sample, using the six lag, benchmark full sample FF VAR and its fitted disturbances. In
each artificial time series we estimated a six lag, benchmark FF VAR model using artificial data over
the period corresponding to the Rudebusch sample period. The 95% confidence intervals are based on
the impulse response functions corresponding to the VARs estimated from the artificial data.

Ch. 2: Monetary Policy Shocks: What Have we Learned and to What End? 109
fourth row of column 3) lies well below the 95% confidence interval. So, we reject
the null hypothesis that there was no change at all in the data generating mechanism
in the Rudebusch sample. 51 Next, we modified the null hypothesis to accommodate
the notion that the only thing which changed in the Rudebusch sample was the nature
of the monetary policy shocks. In all other respects, the data generating mechanism
is assumed to remain unchanged. Under this null hypothesis, we generated 95%
confidence intervals for the estimated impulse response functions in column 2 of
Figure 8. s2 These confidence intervals are reported in column 4 of Figure 8, which
also repeats for convenience the point estimates from column 2. Notice that, with
one exception, all of the estimated impulse response functions lie within the plotted
confidence intervals. 53 The exception is that the impulse response function of PCOM
lies just outside the plotted confidence intervals for roughly the first six periods. Based
on these results, we conclude that there is little evidence against the joint hypothesis
that (i) the response of the aggregates to a given policy shock is the same in the
two sample periods and (ii) the size of the shocks was smaller in the post 1988:10
period. For any particular subsample, we refer to these two conditions as the modified
subsample stability hypothesis.
We now consider the stability of impulse response functions in other subsamples.
Figure 9 reports response functions to monthly benchmark FF policy shocks, estimated
over four subsamples: the benchmark sample, and the periods 1965:1-1979:9,
1979:10-1994:12, and 1984:2-1994:12. In each case, the method for computing
confidence intervals is analogous to the one underlying the results in column 4
of Figure 8. 54 From Figure 9 we see that the estimated response functions for
51 The procedure we have used to reject the null hypothesis of no change versus the alternative of a
change in 1989 implicitly assumes the choice of break date is exogenous with respect to the stochastic
properties of the data. There is a large literature (see Christiano (1992) and the other papers in that
Journal of Business and Economic Statistics volume) which discusses the pitfalls of inference about
break dates when the choice of date is endogenous. In this instance our choice was determined by the
opening of the Federal Funds Futures Market. Presumably,t his date can be viewed as exogenous for the
purpose of our test.
52 With one exception, these confidence intervals were computed using the procedure described in the
previous footnote. The exception has to do with the way the shocks were handled. In particular, the
artificial data were generated by randomly sampling from the orthogonalized shocks, rather than the
estimated VAR disturbances. Residuals other than the policy shocks were drawn, with replacement,
from the full sample period set of residuals. The policy shocks were drawn from two sets. Shocks for
periods prior to the analog of the Rudebusch sample period were drawn, with replacement, from the
pre-Rudebusch sample fitted policy shocks. Shocks for periods during the analog of the Rudebusch
sample period were drawn, with replacement, from the Rudebusch sample fitted policy shocks.
53 In this manuscript, we have adopted the extreme assumption that the stochastic properties of the
policy shock changed abruptly on particular dates. An alternative is that the changes occur smoothly
in the manner captured by an ARCH specification for the policy shocks. Parekh (1997) pursues this
interpretation. He modifies our bootstrap procedures to accommodate ARCH behavior in the shocks.
54 That is, they are computed under the assumption that the data generating mechanism is the six lag,
full sample estimated VAR with policy shocks drawn only from the relevant subsample. All other shocks
are drawn randomly from the full sample of fitted shocks.

110 L.J Christiano et al.
Fed Funds Model 65:01 to 94:12 Fed Funds Model 65:01 to 79:09 Fed Funds Model 79:10 to 94:12 Fed Funds Model 84:02 to 94:12
MP Shock => EM MP Shock => EM MP Shock => EM MP Shock => EM
ii ..............................J...
MP Shock => Price MP Shock => Price MP Shock => Price
MP Shock => Pcom MP Shock => Pcom MP Shock => Pcom MP Shock => Pcom
::2:t .....................
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
MP Shock => FF MP Shock => FF MP Shock => FF
e\ /\ ~\
=L," ........................................r.
MP Shock => NBR MP Shock => NBR MP Shock=> NBR MP Shock => NBR
¢
MP Shock => TR MP Shock => TR MP Shock => TR MP Shock => TR
iil
::J .......... 1
I g 17 25 . . . . . . . . 5 ~ ~1
MP Shock => M1 MP Shock => M1 MP Shock => M1 MP Shock => M1
2', " ~
.....: TT ?.:.::,:.:2L~
0, ..........................
Fig. 9. Response functions to monthly benchmark FF policy shocks, estimated over four subsamples:
the bencl~mark sample, and the periods 1965:1-1979:9, 1979:10-1994:12, and 1984:2-1994:12.

Ch. 2: Monetary Policy Shocks: What Have we Learned and to What End? 111
employment, P, PCOM, and M1 almost always lie within the confidence intervals. For
the third and fourth sample periods there is no evidence against the modified subsample
stability hypothesis. There is some marginal evidence against the hypothesis in the first
subsample. In particular, the PCOM and price level responses lie outside the plotted
confidence interval at some horizons. We find these results somewhat troubling, since
they may indicate that the benchmark FF policy shocks are contaminated by other
shocks to which the Fed responds. Despite this, the overall impression one gets from
these results is that the modified subsample stability hypothesis is not rejected for the
benchmark FF policy shocks.
At the same time, there is strong evidence that the variance of the policy shocks
changed over the sample. One interpretation is that the early 1980s were a period in
which policy shocks were very large, but that the shocks were of comparable magnitude
and substantially smaller size throughout the rest of the post-war period. One bit of
evidence in favor of this view is that the estimated policy shocks in the second and
fourth sample periods are reasonably similar in size, 20 basis points versus 12 basis
points, respectively.
We now briefly point out that qualitative inference is robust across subsamples.
For each subsample we find evidence consistent with a liquidity effect. Specifically, a
policy-induced rise in the federal funds rate is associated with a decline in nonborrowed
reserves, total reserves and M1. In addition, the contractionary policy shock is
associated with a delayed response of employment and a very small change in the
price level.
We now consider the results for the benchmark NBR policy shocks, reported in
Figure 10. The overall impression conveyed here is similar to what we saw in Figure 9.
There is relatively little evidence against the modified subsample sensitivity hypothesis.
For the most part, the point estimates all tie within the plotted confidence intervals.
Note that the impulse response functions are qualitatively robust across subsamples.
We now turn to a complementary way of assessing subsample stability, which
focuses on the magnitude of the liquidity effect. Panels A and B of Table 1 report
summary statistics on the initial liquidity effect associated with the benchmark FF and
NBR identification schemes, respectively. In that table, FF/NBR denotes the average
of the first three responses in the federal funds rate, divided by the average of the
first three responses in nonborrowed reserves. These responses are taken from the
appropriate entries in Figure 9. As a result, FF/NBR denotes the percentage point
change in the federal funds rate resulting from a policy-induced one percent change
in NBR. FF/M1 denotes the corresponding statistic with the policy-induced change
in M1 in the denominator. Because of the shape of the impulse response function in
M1, we chose to calculate this statistic by averaging the first six responses in FF and
M1. The statistics are reported for the four sample periods considered in Figure 9. In
addition, the 95% confidence intervals are computed using the appropriately modified
version of the bootstrap methodology used to compute confidence intervals in Figure 9.
Panel B is the exact analog of Panel A, except that the results are based on the NBR
policy shocks.

112 L.J. Christiano et al.
NBR Model 85:01 to 94:12 NBR Model 85:01 to 79:09 NBR Model 79:10 to 94:12 NBR Model 84:02 to 94:12
MP Shock => EM MP Shock => EM MP Shock => EM MP Shock => EM
ii!!
. . . . ~5 ~ 41
MP Shock => Price MP Shock -> Price MP Shock => Price
MP Shock => Pcom MP Shock >Pcom MP Shock -> Pcom MP Shock -> Poem
11,t1 ~__~ ~
~.~
MP Shock >FF MP Shock => FF MP Shock-> FF MP Shock => gg
MP Shock => NBR MP Shock -> NBR MP Shook => NBR MP Shock -> NBR
MP Shock => TR MP Shock => TR MP Shock => TR
2~ ............................................ ~ 23 ............................. i J
MP Shock => M1 MP Shock => M1 MP Shock => M1 MP Shock => M1
..... L ~ i
Fig. 10. Results for the benchmark NBR policy shocks.

Ch. 2: Monetary Policy Shocks: What Have we Learned and to What End? 113
Table 1
The liquidity effect, sample period sensitivity
Subsample FF/NBR FF/M 1
Panel A: FF Policy Shock
65:01~4:12 -0.94 -2.17
(-1.30, -0.73) (-3.61, -1.36)
65:01-79:09 -0.70 -1.88
( 2.64,-0.55) (-8.32,-0.72)
79:10-94:12 0.71 -1.13
(-1.95,-0.64) ( 4.48, 0.82)
84:02-94:12 -0.69 -0.97
(-5.52, 1.86) (-13.92, 13.39)
Panel B: NBR Policy Shocks
65:01-94:12 -0.23 -1.14
( 0.29, 0.17) ( 2.10,-0.59)
65:01-79:09 -0.07 -2.08
(-0.36, -0.11) (-4.86, -0.14)
79:1044:12 -0.27 -0.37
( 0.35, 0.13) (-3.56,-0.15)
84:02-94:12 -0.13 -0.47
(-0.45,-0.04) (-10.12, 5.35)
We begin our discussion by reviewing the results in panel A. The full sample results
indicate that a one percent policy-shock induced increase in nonborrowed reserves
results in roughly a one percentage point reduction in the federal funds rate. A one
percent policy-shock induced increase in M1 results in roughly a two percentage point
decline in the federal funds rate. The point estimates do vary across the subsamples.
However, the evidence suggests that the differences in estimated responses can be
accounted for by sampling uncertainty. In particular, there is little evidence against
the null hypothesis that the true responses are the same in the subsamples. This is
evident from the fact that the confidence intervals in the subsamples include the point
estimates for the full sample.
Turning to panel B, we see that, using the NBR identification scheme, we obtain point
estimates of the responses that are generally smaller. Again, there is little evidence
against subsample stability.
We now summarize our findings regarding subsample stability. We have two basic
findings. First, there is evidence that the variance of the policy shocks is larger in the
early 1980s than in the periods before or after. Second, we cannot reject the view that
the response of economic variables to a shock of given magnitude is stable over the
different subsamples considered.

114 L.J Christiano et al.
We conclude this section by noting that other papers have also examined the
subsample stability question. See, for example Balke and Emery (1994), Bernanke and
Mihov (1995) and Strongin (1995). These papers focus on a slightly different question
than we do. They investigate whether the Fed adopted different operating procedures
in different subperiods, and provide some evidence that different specifications of the
policy rule in Equation (2.1) better characterize different subsamples. At the same
time, Bernanke and Mihov (1995) and Strongin (1995) do not find that the dynamic
response functions to a monetary policy shock are qualitatively different over the
different subsample periods that they consider. In this sense, their results are consistent
with ours.
4.5. Discriminating between the benchmark identification schemes
In the introduction we sketched a strategy for assessing the plausibility of different
identification schemes. The basic idea is to study the dynamic response of a broad
range of variables to a monetary policy shock. We dismiss an identification scheme if
it implies a set of dynamic response functions that is inconsistent with every model
we are willing to consider.
The first subsection illustrates our approach by comparing the plausibility of two
interpretations of an orthogonalized shock to NBR. These amount to two alternative
identification schemes. The first corresponds to the benchmark NBR identification
scheme described in Section 4. Under this scheme, an orthogonalized contractionary
shock to NBR is interpreted as a negative money supply shock. The second scheme,
recently proposed by Coleman, Gilles and Labadie (1996), interprets the same shock
as either a positive shock to money demand, or as news about a future monetary
expansion. When we use our strategy to assess their identification scheme, we find
that we can dismiss it as implausible. 55
The second subsection contrasts our approach to discriminating among identification
schemes with one recently proposed in Bernanke and Mihov (1995). We review their
methodology and explain why we think our approach is more likely to be fruitful.
4.5.1. The Coleman, Gilles and Labadie identification scheme
According to Coleman, Gilles and Labadie (1996), understanding why an NBR policy
shock may not coincide with an exogenous contractionary shock to monetary policy
requires understanding the technical details about the way the Fed allocates the
different tasks of monetary policy between the discount window and the Federal Open
Market Committee. They argue, via two examples that a contractionary NBR shock
may correspond to other types of shocks.
55 The discussion presented here summarizes the analysis in Christiano (1996).

Ch. 2: Monetary Policy Shocks: What Have we Learned and to What End? 115
In their first example, they argue that a negative NBR shock may actually correspond
to a positive shock to the demand for money. The argument goes as follows. Suppose
that there was a shock to either the demand for TR, M1 or M2 that drove up the
interest rate. Absent a change in the discount rate, this would lead to an increase
in Borrowed Reserves via the discount window. Suppose in addition that the FOMC
believes that the managers of the discount window always over accommodate shocks
to the demand for money, and respond by pulling nonborrowed reserves out of the
system. An attractive feature of this story is that it can potentially account for the
fact that the federal funds rate is negatively correlated with nonborrowed reserves and
positively correlated with borrowed reserves see Christiano and Eichenbaum (1992).
Unfortunately, the story has an important problem: it is hard to see why a positive
shock to money demand would lead to a sustained decline in total reserves, M1 or
M2. But this is what happens after an NBR policy shock (see Figure 2). In light of
this fact, the notion that a negative NBR policy shock really corresponds to a positive
money demand shock seems unconvincing.
In their second example, Coleman, Gilles and Labadie argue that a negative NBR
shock may actually correspond to a positive fi~ture shock to the money supply. The
basic idea is that the Fed signals policy shifts in advance of actually implementing
them, and that a signal of an imminent increase in total reserves produces an immediate
rise in the interest rate. Such a rise would occur in standard neoclassical monetary
economies of the type considered by Cooley and Hansen (1989). Suppose that the rise
in the interest rate results in an increase in borrowed reserves. If the Fed does not wish
the rise in borrowed reserves to generate an immediate rise in total reserves, it would
respond by reducing nonborrowed reserves.
This interpretation of the rise in the interest rate after an NBR policy shock is
particularly interesting because it does not depend on the presence of a liquidity effect.
Indeed, this interpretation presumes that the interest rate rises in anticipation of a future
increase in the money supply. To the extent that the interpretation is valid, it would
constitute an important attack on a key part of the evidence cited by proponents of the
view that plausible models of the monetary transmission mechanism ought to embody
strong liquidity effects. Again there is an important problem with this interpretation
of the evidence: the anticipated rise in the future money supply that the contractionary
NBR policy shock is supposed to be proxying for never happens: TR, M1 and M2fall
for over two years after a contractionary NBR policy shock. In light of this, the notion
that a contractionary NBR policy shock is proxying for expansionary future money
supply shocks seems very unlikely.
4.5.2. The Bernanke-Mihov critique
The preceding subsection illustrates our methodology for assessing the plausibility of
different identification schemes. Bernanke and Mihov (BM) propose an alternative ap-
proach. Under the assumption that the policy function is of the form of Equation (2.1),
they develop a particular test of the null hypothesis that e7 is a monetary policy shock

116 L.J Christiano et al.
against the alternative that Ei~ ' is confounded by nonmonetary policy shocks to the
market for federal funds.
To implement their test, Bernanke and Mihov develop a model of the federal funds
market which is useful for interpreting our benchmark identification schemes. These
schemes are all exactly identified, so that each fits the data equally well. To develop
a statistical test for discriminating between these schemes, BM impose a particular
overidentifying restriction: the amount that banks borrow at the discount window is
not influenced by the total amount of reserves in the banking system. BM interpret a
rejection of a particular overidentified model as a rejection of the associated NBR, FF
or NBR/TR identification scheme. But a more plausible interpretation is that it reflects
the implausibility of their overidentifying restriction. This is because that restriction
is not credible in light of existing theory about the determinants of discount window
borrowing and the empirical evidence presented below.
4.5.2.1. A model of the federal funds market. BM assume that the demand for total
reserves is given by
rRt = fTR(Y2t) -- aFFt + OdEd , (4.4)
where fTR(g2t) is a linear function of the elements of £2,, a, oa > 0, and eta is a
unit variance shock to the demand for reserves which is orthogonal to Or. According
to Equation (4.4), the demand for total reserves depends on the elements of g2t and
responds negatively to the federal funds rate. The demand for borrowed reserves is:
BRt =fBR(Qt)+ 3FFt - yNBRt + Obebt , (4.5)
wherefBR(g2t) is a linear function of the elements of f2t and ob > 0. The unit variance
shock to borrowed reserves, Ebt , is assumed to be orthogonal to f2t. BM proceed
throughout under the assumption that y = 0. Below, we discuss in detail the rationale
for specification (4.5). 56 Finally, they specify the following Fed policy rule for setting
NBRt:
NBR~ = fxgR ( g2t ) + et, (4.6)
where
et = Oa ad( + Ob Obetb + ase7 (4.7)
Here, e 7 is the unit variance exogenous shock to monetary policy. By assumption,
etd , e), e 7 are mutually orthogonal, both contemporaneously and at all leads and lags.
56 We follow BM in not including the interest rate charged at the discount window (the discount rate)
as an argument in Equation (4.5). BM rationalize this decision on the grounds that the discount rate
does not change very often.

Ch. 2. Monetary Policy Shocks: What Have we Learned and to What End? 117
The parameters q~d and Cb control the extent to which Fed responds contemporaneously
to shocks in the demand for total reserves and borrowed reserves.
Using the fact that TR = NBR + BR, and solving Equations (4.4)-(4.7), we obtain
TRt
NBRt I = F(f2t) + ut, ut = Be~, (4.8)
FF, J
where
"fTR(~3
F(g2t) 0 1 0 fNBR(~2t) (4.9)
=
1 y 1 1
and
(Td~ CdaY+OJaflU~- -aO's~ -~a/3 --tZ~b~-l +O~Y-¢bfi+a
B = ~ra4)a G G~ z' (4.10)
~d~d7
~ a+l 7 1 ~ -1+¢b7-~ ~
~+a ~s ~ ~'b
e, = (4.11)
4/
4.5.2.2. Identifying the parameters of the model. We now turn to the problem of
identifying the parameters of the money market model. As in Section 3, we first
estimate ut using the fitted disturbances, ~tt, in a linear regression of the money market
variables on g2t, and then estimate et from ~, = B-lht using a sample estimate of B.
The latter can be obtained by solving
V = BB ~, (4.12)
where V is the Gaussian maximum likelihood estimate of Eutd t which respects the
restrictions, if any, implied by Equation (4.12) and the structure of B in Equation (4.10).
The estimate, V, is obtained by maximizing
T 1 T
2 {loglVl+tr(SV-')}, where S =~Zht~t;, (4.13)
t=l
subject to conditions (4.10)-(4.12). When the latter restrictions are not binding, the
solution to this maximization problem is V = S. s7
57 BM use a slightly different estimation strategy. See the appendix in BM.

118 L.J Christiano et al.
Denote the model's eight structural parameters by
~p = [ a, [3, 7, cpd , o b, ad2 , 0-2, 0-21. (4.14)
Let ~0r denote a value of ~0 which implies a B that satisfies condition (4.12). The
model is underidentified if there exist other values of ~ that have this property too.
The model is exactly identified if ~r is the only value of ~ with this property. Finally,
the model is overidentified if the number of structural parameters is less than six, the
number of independent elements in S.
Given the symmetry of V, condition (4.12) corresponds to six equations in eight
unknown parameters: a, fi, 7, q~d, q~b, 0-2, 0-I, 0-2. To satisfy the order condition
discussed in Section 3, at least two more restrictions must be imposed.
Recall that the FF, NBR and NBR/TR identification schemes analyzed in the previous
section correspond to a particular orthogonality condition on the monetary policy
shock. These conditions are satisfied in special cases of the federal funds market model
described above. Each special case corresponds to a different set of two restrictions on
the elements of ~p. In each case, the estimation procedure described above reduces to
first setting V = S and then solving the inverse mapping from V to the free elements
of ~p in condition (4.12). The uniqueness of this inverse mapping establishes global
identification.
When St = NBRt, relations (4.8)-(4.10) imply that the measured policy shock is
given by Equation (4.7). So, from the perspective of this framework, our NBR system
assumes:
q~d = q~b = O. (4.15)
The free parameters in ~p are uniquely recovered from V as follows:
V21 0 -2 = V22, (4.16)
a -- V32,
Vll+ uV31
fi - V31+ aV33' a~2 =(13+a)[V31+ aV33]' (4.17)
g 1 V21(~ + a) 2
= (/0-2 , O~i = V33(a+/3)2_O-c~_(1_ 7) 2 a s2 . (4.18)
where V O. refers to the (i,j) element of V.
When St = FFt then
~pd(y_l)+la+e; -l+q~b(g-1)~+e~, y-1
et - fi + a fi + a ~et.s (4.19)
From the perspective of this framework, the benchmark FF system assumes:
q~d _ 1 q~b = _q)d. (4.20)
1--(cid:127)'
The free parameters in ~p are recovered from V as follows:
_ ~/- 1 0-2 _ V322 V31 (4.21)
C /~ q- a' V33, Of = -- V3~,

Ch. 2: Monetary Policy Shocks: What Have we Learned and to What End? 119
1
-;= gll _ a2C2 0- s 2 ,
y = 1 -- V 21-k
acq,2J
'
(4.22)
V32
0-2 = (1- y)2 V22 0-2 0-2 /3 = (y 1) V7-7- ss - a . (4.23)
L (1 - 7) 2 " ' -
The NBR/TR system assumes:
a = q}b = O. (4.24)
Under these conditions, it is easy to verify that the error of the regression of NBRt on
g2t and TRt is e~. The free parameters of the money model are recovered from V as
follows:
0-; = gll, ~d _ V21 0"2 = V22-(0 d ) 20.2d , (4.25)
V~I'
V32 - Odv3~ v31
cl - 0.2 , c2- 02, fi= c2-0~cl -~ , (4.26)
d :/32 v33- c20-~2 - cZos2, y = /3C 1 + 1. (4.27)
Restrictions (4.15), (4.20), (4.24) guarantee that the benchmark NBR, FF and
NBR/TR policy shock measures are not polluted by nonmunetary policy shocks,
respectively.
4.5.2.3. The Bernanke-Mihov test. Recall that the basic purpose of the money market
model discussed above is to help assess whether different monetary policy shock
measures are polluted by nonpolicy shocks to the money market. In the case of the
NBR policy system this amounts to testing restriction (4.15). For the FF and NBR/TR
systems this corresponds to testing restrictions (4.20) and (4.24), respectively. The
problem is that, since each of these systems is exactly identified, the restrictions cannot
be tested using standard statistical procedures. From this perspective, the money market
model is not helpful. As the model stands, to assess the different identification schemes,
one must revert to the strategy laid out in the previous section. Namely, one must
examine the qualitative properties of the impulse response functions.
Instead BM impose an additional maintained assumption on the model. Specifically,
they assume y = 0, i.e., the demand for borrowed reserves does not depend on the level
of nonborrowed reserves. With this additional restriction, the NBR, FF and NBR/TR
models have only five structural parameters, so each is overidentified. Consequently,
each can be tested using standard likelihood ratio methods. An important limitation
of this approach is that we can always interpret a rejection as evidence against the
maintained hypothesis, y = 0, rather than as evidence against the NBR, FF or NBR/TR
identification schemes. A rejection would be strong evidence against one of these
identification schemes only to the extent that one had overwhelmingly sharp priors

120 L.J Christiano et al.
that y really is zero. In fact, there are no compelling reasons to believe that y is zero.
Just the opposite is true. Standard dynamic models of the market for reserves suggest
that y is not zero.
Consider for example Goodfriend's (1983) model of a bank's demand for borrowed
reserves. Goodfriend highlights two factors that affect a bank's decision to borrow
funds from the Federal Reserve's discount window. The first factor is the spread
between the federal funds rate and the Fed's discount rate (here assumed constant).
The higher this spread is, the lower is the cost of borrowing funds from the discount
window, relative to the cost of borrowing in the money market. The second factor is
the existence of nonprice costs of borrowing at the Federal Reserve discount window.
These costs rise for banks that borrow too much or too frequently, or who are perceived
to be borrowing simply to take advantage of the spread between the federal funds rate
and the discount rate.
Goodfriend writes down a bank objective function which captures both of the
aforementioned factors and then derives a policy rule for borrowed reserves that is
of the following form:
O<3
BRt = 21BRt 1 - 22hFFt - h Z )J2Et(FFt-I+i)' -1 < 21, 22 < O, h > O. (4.28)
i-2
Here Et denotes the conditional expectation based on information at time t. Reflecting
the presence of the first factor in banks' objective functions, the current federal funds
rate enters the decision rule for BR with a positive coefficient. The variable, BRt 1,
enters this expression with a negative coefficient because of the second factor. The
presence of the expected future federal funds rate in the policy rule reflects both factors.
For example, when EtFFt+I is high, banks want BRt to be low so that they can take
full advantage of the high expected funds rate in the next period without having to
suffer large nonprice penalties at the discount window.
The crucial thing to note from Equation (4.28) is that any variable which enters
Et (FFt-l+i) also enters the "demand for borrowed reserves" (4.5). So, if nonborrowed
reserves help forecast future values of the federal funds rate, y should not equal zero.
To assess the empirical importance of this argument we proceeded as follows. We
regressed FFt on 12 lagged values (starting with month t - 1) of data on employment,
P, PCOM, FF, NBR, and TR. The estimation period for the regression is the same
as for our monthly benchmark VAR's. We computed an F-statistic for testing the null
hypothesis that all the coefficients on NBR in this equation are equal to zero. The value
of this statistic is 3.48 which has a probability value of less than 0.001 percent using
conventional asymptotic theory.
Given our concerns about the applicability of conventional asymptotic theory in
this context we also computed the probability value of the F-statistic using an
appropriately modified version of the bootstrap methodology used throughout this
chapter. Specifically, we estimated a version of our benchmark monthly VAR in

Ch. 2: MonetaryP olicy Shocks: What Have we Learned and to What End? 121
which all values of NBR were excluded from the federal funds equation. 58 Using the
estimated version of this VAR, we generated 500 synthetic time series by drawing
randomly, with replacement, from the set of fitted residuals. On each synthetic data
set, we computed an F-statistic using the same procedure that was applied in the actual
data. Proceeding in this way, we generated a distribution for the F-statistic under the
null hypothesis that lagged values of NBR do not help forecast the federal funds rate.
We find that none of the simulated F-statistics exceed the empirical value of 3.48. This
is consistent with the results reported in the previous paragraph which were based on
conventional asymptotic distribution theory. Based on this evidence, we reject the null
hypothesis that lagged values of NBR are not useful for forecasting future values of
FF and the associated hypothesis that NBR is not an argument of the demand for BR.
The argument against the BM exclusion restriction (7 = 0), is a special case of the
general argument against exclusion restrictions presented in Sargent (1984) and Sims
(1980). In fact, this argument suggests that none of the parameters of BM's money
market model are identified since even exact identification relies on the exclusion of
NBR and BR from total reserves demand (4.4), and TR from the borrowed reserves
function (4.5).
There is another reason not to expect 7 = 0. The second factor discussed above
suggests that a bank which is not having reserve problems, but still borrows funds
at the discount window, may suffer a higher nonprice marginal cost of borrowing.
This would happen if the discount window officer suspected such a bank were simply
trying to profit from the spread between the federal funds rate and discount rate. 59
Presumably a bank that possesses a large amount of nonborrowed reserves could be
viewed as having an "ample supply of federal funds". The appropriate modification
to the analysis in Goodfriend (1983) which reflects these considerations leads to the
conclusion that NBRt should enter on the right hand side of Equation (4.28) with
a negative coefficient. We conclude that what we know about the operation of the
discount window and the dynamic decision problems of banks provides no support for
the BM maintained hypothesis that 7 is equal to zero.
4.5.2.4. Empirical results. To make concrete the importance of BM's maintained
assumption that g = 0, we estimated both the restricted and unrestricted NBR, FF and
NBR/TR models, as discussed above. The results are reported in Tables 2a and 2b. Each
table reports results based on two data sets, the BM monthly data and the quarterly
data used in the rest of this chapter. For the BM data, we used their estimated S matrix,
which they kindly provided to us. The column marked "restricted" reports results for
the model with 7 = 0. These correspond closely to those reported by BM. 6o The
5s Each equation in this VAR was estimated separately using OLS and 12 lags of the right hand side
variables.
59 Regulation A, the regulation which governs the operation of the discount window, specifically excludes
borrowing for this purpose.
6o The small differences between the two sets of results reflect different estimation methods.

L.J Christiano et aL
122
Table 2a
Estimation results for money market models
NBR model FF model
B-M Data, 1965:1-1994:12 1965:Q3- B-M Data, 1965:1-1994:12 1965:Q3-
restricted unrestricted 1995:Q2 restricted unrestricted 1995:Q2
unrestricted unrestricted
a 0.009 0.035 0.022 -0.003 -0.003 -0.001
(0.00763) (0.00763) (0.00550) (0.00099) (0.00070) (0.00104)
fi 0.03 (cid:127) 0.012 0.012 0.012 0.012 0.012
(0.00269) (0.00129) (0.00151) (0.00106) (0.00091) (0.00107)
y 0 0.481 0.279 0 -0.103 -0.073
(0.03229) (0.05599) (0.04849) (0.05864)
0 d 0 0 0 1 1 1
crd 0.011 0.020 0.022 0.009 0.009 0.013
(0.00065) (0.00333) (0.00387) (0.00033) (0.00023) (0.00058)
~s 0.013 0.013 0.018 0.004 0.004 0.008
(0.00048) (0.00048) (0.00114) (0.00070) (0.00047) (0.00107)
ob 0.013 0.007 0.009 0.009 0.010 0.011
(0.00100) (0.00033) (0.00070) (0.00035) (0.00053) (0.00077)
p-value 0.000 0.052
columns marked "unrestricted" report the analog results when the restriction, 7 = 0,
is not imposed. The bottom row of Tables 2a and 2b reports the p-values for testing
the monthly restricted versus unrestricted model. 61
Several results in these tables are worth noting. To begin with, according to column 1
of Table 2a, BM's restricted NBR model is strongly rejected. Recall, they interpret
this rejection as reflecting that 0~ and/or 0b are nonzero. As we have stressed, one
can just as well infer that 7 is not zero. In fact, from column 2 we see that the
estimated value of 7 is positive and highly statistically significant. Of course, this result
would not be particularly interesting if the estimated values of the other parameters
in the unrestricted model violated BM's sign restrictions. But, this is not the case. All
the parameter values satisfy BM's sign restrictions. This is the case whether we use
monthly or quarterly data. Taken together, our results indicate that BM's claim to have
rejected the benchmark NBR model is unwarranted.
61 We use a likelihood ratio statistic which, under the null hypothesis, has a chi-square distribution with
1 degree of freedom.

Ch. 2: Monetary Policy Shocks." What Have we Learned and to What End? 123
Table 2b
Estimation results, restricted and unrestricted models
NBR/TR model
B-M Data, 1965:1-1994:12 1965:Q3-1995:Q2
restricted unrestricted unrestricted
a o o o
/3 0.046 0.038 0.026
(0.00424) (0.00422) (0.00358)
7 0 0.200 -0.011
(0.07836) (0.10371)
0 a 0.802 0.802 0.886
(0.06350) (0.06350) (0.09664)
ad 0.009 0.009 0.013
(0.00033) (0.00033) (0.00082)
a~. 0.011 0.011 0.014
(0.00040) (0.00040) (0.00087)
crb 0.019 0.016 0.015
(0.00188) (0.0018 l) (0.00234)
p-value 0.032
Next, from column 4 of Table 2a, we see that, consistent with BM's results, the
FF model cannot be rejected on the basis of the likelihood ratio test. Notice, however,
that the estimated value of a is negative. Indeed, the null hypothesis, a ~> 0, is strongly
rejected. This calls into question the usefulness of their model for interpreting the
benchmark FF identification scheme for the sample period as a whole. 62 Finally, note
from Table 2b that the NBR/TR model is not strongly rejected by BM's likelihood ratio
test and the parameter values are consistent with all of BM's sign restrictions.
In sum, BM have proposed a particular way to test whether the policy shock
measures associated with different identification schemes are polluted by nonpolicy
shocks. The previous results cast doubt on the effectiveness of that approach.
4.6. Monetary policy shocks and volatility
Up to now we have focussed on answering the question, what are the dynamic
effects of a monetary policy shock? A related question is: How have monetary policy
62 BM actually argue that this model is most suitable for the pre-1979 period. Here too, their point
estimate of a is negative and significantly different from zero.

124 L.J Christiano et al.
shocks contributed to the volatility of various economic aggregates? The answer
to this question is of interest for two reasons. First, it sheds light on the issue of
whether policy shocks have been an important independent source of impulses to the
business cycle. Second, it sheds light on identification strategies which assume that
the bulk of variations in monetary aggregates reflect exogenous shocks to policy. For
example, this is a maintained assumption in much of the monetized real business cycle
literature. 63
Table 3 summarizes the percentage of the variance of the k step ahead forecast errors
in P, Y, PCOM, FF, NBR, TR and M 1 that are attributable to quarterly benchmark FF,
NBR and NBR/TR policy shocks. Analog results for policy shock measures based on
M0, M 1, and M2 are reported in Table 4.
We begin by discussing the results based on the benchmark policy measures.
First, according to the benchmark FF measure, monetary policy shocks have had
an important impact on the volatility of aggregate output, accounting for 21%, 44%
and 38% of the variance of the 4, 8 and 12 quarter ahead forecast error variance
in output, respectively. However, these effects are smaller when estimated using the
NBR/TR policy shock measures and smaller still for the benchmark NBR policy shocks.
Indeed, the latter account for only 7%, 10% and 8% of the 4, 8 and 12 quarter
ahead forecast error variance of output. Evidently, inference about the importance of
monetary policy shocks depends sensitively on which policy shock measure is used.
In addition, conditioning on the policy shock measure, there is substantial sampling
uncertainty regarding how important policy shocks are in accounting for the variance
of the k step forecast error.
Second, none of the policy shock measures account for much of the volatility of the
price level, even at the three year horizon. In addition, only the FF benchmark policy
shock measure accounts for a nontrivial portion of the variability of PCOM. Evidently,
monetary policy shocks are not an important source of variability in prices, at least at
horizons of time up to three years in length.
Third, regardless of whether we identify St with the federal funds rate or NBR,
policy shocks account for a large percent of the volatility of St at the two quarter
horizon. However, their influence declines substantially over longer horizons. Fourth,
according to the benchmark FF and NBR/TR measures, monetary policy shocks play
a very minor role in accounting for the variability in TR and M1. Policy shocks
play a more important role according to the benchrnark NBR measure. Even here,
most of the volatility in TR and M1 arises as a consequence of nonpolicy shocks.
Identification strategies which assume that monetary aggregates are dominated by
shocks to policy are inconsistent with these results. Finally, policy shocks are more
important in explaining the volatility in M2 than for TR or M1. This is true regardless
of which benchmark policy measure we consider. Still, the variation in M2 due to
policy shocks never exceeds 50%.
63 See Cooley and Hansen (1989), Chaff et al. (1996) and Christiano and Eichenbaum (1995).

Ch. 2." Monetary Policy Shocks: What Have we Learned and to What End? 125
¢~ ,~- ~- ~ ~ 0"5
o)
52
¢9
0
09 ,-2

L.J. Christiano et al.
126
Z t¢3
m ~ ~
v
s
cq
v
o
~Z
o TM
& ~Z t"-I
v
&
¢q

Ch. 2: Monetary Policy Shocks: What Have we Learned and to What End? 127
Next we consider the results obtained for policy shock measures based on M0,
M1, and M2. The VAR's underlying these results correspond to the ones underlying
the results reported in columns 2, 4 and 6 in Figure 6. In each case, St is equated
to either M0, MI or M2, and the information set, g2t, includes current and past
values of Yt, Pt, PCOMt as well as lagged values ofFFt, TRt and St. A number of
results are interesting to note here. First, the M0 and Ml-based policy shock measures
account for only a trivial fraction of the fluctuations in output. In contrast, at horizons
greater than a year, M2-based policy measures account for a noticeably larger fraction
of output variations. While they account for a smaller fraction of output volatility
than do the FF policy shocks, they are similar on this dimension to the NBR/TR
policy shock measures. Second, neither the M0 or Ml-based policy shock measures
account for more than a trivial part of the volatility of P and PCOM. Policy shock
measures based on M2 play a somewhat larger role at horizons of a year or longer.
However, there is considerable sampling uncertainty about these effects. Finally, at
horizons up to a year, M0, M1, and M2-based policy shocks account for sizeable
percentages of M0, M1, and M2, respectively. At longer horizons the percentages are
lower.
Viewed across both sets of identification strategies that we have discussed, there is a
great deal of uncertainty about the importance of monetary policy shocks in aggregate
fluctuations. The most important role for these shocks emerged with the FF-based
measure of policy shocks. The smallest role is associated with the M0 and Ml-based
policy shock measures.
We conclude this subsection by noting that even if monetary policy shocks have
played only a very small role in business fluctuations, it does not follow that the
systematic component, f in Equation (2.1), of monetary policy has played a small
role. The same point holds for prices. A robust feature of our results is that monetary
policy shocks account for a very small part of the variation in prices. This finding does
not deny the proposition that systematic changes in monetary policy, captured by f,
can play a fundamental role in the evolution of prices at all horizons of time.
5. The effects of monetary policy shocks: abandoning the recursiveness
approach
In this section we discuss an approach to identifying the effects of monetary policy
shocks that does not depend on the recursiveness assumption. Under the recursiveness
assumption, the disturbance term, e)~ , in the monetary anthority's reaction function
see Equation (2.1) is orthogonal to the elements of their information set g2t. As
discussed above see Equation (4.1) this assumption corresponds to the notion that
economic variables within the quarter are determined in a block recursive way: first,
the variables associated with goods markets (prices, employment, output, etc.) are
determined; second, the Fed sets its policy instrument (i.e., NBR in the case of the

128 L.J Christiano et al.
benchmark NBR system, and FF in the case of the benchmark FF system); and third,
the remaining variables in the money market are determined.
To help compare the recursiveness assumption with alternative identifying assump-
tions, it is convenient to decompose it into two parts. First, it posits the existence of
a set of variables that is predetermined relative to the policy shock. Second, it posits
that the Fed only looks at predetermined variables in setting its policy instrument.
Together, these assumptions imply that monetary policy shocks can be identified with
the residuals in the ordinary least squares regression of the policy instrument on the
predetermined variables.
The papers discussed in this section abandon different aspects of the recursiveness
assumption. All of them drop the assumption that the Fed only looks at variables that
are predetermined relative to the monetary policy shock. This implies that ordinary
least squares is not valid for isolating the monetary policy shocks. Consequently, all
these papers must make further identifying assumptions to proceed. The papers differ
in whether they assume the existence of variables which are predetermined relative to
the monetary policy shock. Sims and Zha (1998) assume there are no variables with
this property. In contrast, papers like Sims (1986), Gordon and Leeper (1994), and
Leeper, Sims and Zha (1996) assume that at least a subset of goods market variables are
predetermined. Under their assumptions, these variables constitute valid instruments
for estimating the parameters of the Fed's policy rule.
The section is organized as follows. First, we discuss the identifying assumptions in
the paper by Sims and Zha (1998). We then compare their results with those obtained
using the benchmark identification schemes. Finally, we briefly consider the analyses
in the second group of papers mentioned above.
5.1. A fully simultaneous system
This section is organized as follows. In the first subsection we discuss the specification
of the Sims and Zha (1998) (SZ) model and corresponding identification issues. In the
second subsection, we compare results obtained with a version of the SZ model to those
obtained using the benchmark policy shocks.
5.1.1. Sims-Zha: model specification and identification
We begin our discussion of the SZ model by describing their specification of the money
supply equation. It is analogous to our policy function (2.1), with St identified with a
short term interest rate, Rt. Sims and Zha (1998) assume that the only contemporaneous
variables which the Fed sees when setting St are a producer's price index for crude
materials (Pcm) and a monetary aggregate (M). In addition, the Fed is assumed to
see a list of lagged variables to be specified below. Note that unlike the benchmark
systems, £2t does not contain the contemporaneous values of the aggregate price level

Ch. 2: Monetary Policy Shocks: What Have we Learned and to What End? 129
and output. As Sims and Zha (1998) point out, this is at best only a reasonable working
hypothesis. 64 The reaction function in the SZ model can be summarized as follows:
Rt = const. + aiMt + a2Pcmt +.fs(Zt-1 .... , Zt-q) + a~~ , (5.1)
where fs(Z~-i .... , Zt_q) is a linear function of past values of all the variables in the
system, q > 0, a > 0, and Est is a serially uncorrelated monetary policy shock.
Sims and Zha (1998) assume that Pcm and M are immediately affected by a
monetary policy shock. As noted above, this rules out ordinary least squares as a
method to estimate Equation (5.1). Instrumental variables would be a possibility if
they made the identifying assumption that there exists a set of variables predetermined
relative to the monetary policy shock. However, they are unwilling to do so. They make
other identifying assumptions instead.
First, they postulate a money demand function of the form:
Mt - Pt - Yt : const. + blRf + fM(Zt 1, ..., Zt-q) + aMe M. (5.2)
Here, fM(Zt_l .... , Zt-q) is a linear function of past values of all the variables in the
system, aM > 0, and eM is a serially uncorrelated shock to money demand. Recall,
Yt and Pt denote aggregate output and the price level. Note that the coefficients on
Et and Pt are restricted to unity. Sims and Zha display a model which rationalizes a
money demand relationship like Equation (5.2). 65
Second, they assume that Pcmt responds contemporaneously to all shocks in the
system. They motivate this assumption from the observation that crude materials prices
are set in auction markets. Third, as noted above, they are not willing to impose the
assumption that goods market variables like P and Y are predetermined relative to the
monetary policy shock. Clearly, they cannot allow P and Y to respond to all shocks
in an unconstrained way, since the system would then not be identified. Instead, they
limit the channels by which monetary policy and other shocks have a contemporaneous
effect on P and Y. To see how they do this, it is convenient to define a vector of variables
denoted by Xt, which includes Pt and Yr. Sims and Zha impose the restriction that Xt
does not respond directly to Mt or Rt, but that it does respond to Pcmt. A monetary
64 This is because the Fed does have at its disposal various indicators of price and output during the
quarter. For example, the Fed has access to weekly reports on unemployment claims and retail sales.
Also, two weeks prior to each FOMC meeting, policymakers have access to the "Beige Book", which
is compiled from nationwide surveys of business people. In addition, FOMC members are in constant
contact with members of the business community. Moreover, the Fed receives, with a one month lag,
various monthly measures of output and prices (e.g. employment, wages and the consumer price level).
65 Their model rationalizes a relationship between the contemporaneous values of Mr , Pt, Yt and St. One
can rationalize the lagged terms in the money demand equation if there is a serially correlated shock
to the marginal product of money in their model economy. Ireland (1997) and Kim (1998) rationalize
similar relationships with Y replaced by consumption.

130 L.J Christiano et al.
policy shock has a contemporaneous impact on the variables in Xt via its impact on
Pcmt.
To see this, first let
Xt = Wt , Zt= R, "
Pimt
Lrbk' j x,
where Pim denotes the producer price index of intermediate materials, W denotes
average hourly earnings of nonagricultural workers, Tbk denotes the number of
personal and business bankruptcy filings. The assumptions stated up to now imply
the following restrictions on the matrix A0 in representation (3.2) of Zt:
-all a12 a13 a14 a15 al6 a17 a18
0 a22 a23-a22-a22 0 0 0
a31 a32 a33 0 0 0 0 0
A0 = a41 0 0 a44 a45 a46 a47 a48 (5.3)
asa 0 0 a54 a55 a56 a57 a58
a61 0 0 a64 a65 a66 a67 a68
aT1 0 0 a74 a75 a76 a77 a78
as1 0 0 a84 a85 a86 a87 a88
The first row of A0 corresponds to the Pcm equation. The second and third rows
correspond to the money demand equation (5.2), and to the monetary policy rule (5.1),
respectively. The next five rows correspond to Xt. The second and third elements of
et in Equation (3.2) correspond to ~ and e7 .
It is evident from Equation (5.3) that the impact of a monetary policy shock operates
on Xt via its influence on Peru. Specifically, this reflects the fact that the (4, 1) to
(8, 1) elements of A0 are potentially nonzero. If we impose that these elements are
zero, then, given the other zero restrictions in the second and third columns of A0, the
variables in Xt are predetermined relative to a monetary policy shock.
We now consider identification of the SZ model. Notice that the last five rows in
A0 have the same restrictions, suggesting that Equation (3.2) is not identified. To see
,o
that this is in fact the case, consider the following orthonormal matrix:
(3×3) (3;5)
m = 0 - ' (5.4)
(5×3) (5x5) J
where the dimensions are indicated in parentheses and ~" is an arbitrary orthonormal
matrix. Note that if A0 satisfies (i) the restrictions in Equation (5.3) and (ii) the relation

Ch. 2.. Monetary Policy Shocks: What Have we Learned and to What End? 131
Ao I (Aol) ' = V, then WAo does too. Here, V denotes the variance covariance matrix
of the fitted residuals in the VAR (3.1), for Zt. By the identification arguments in
Section 3, representation (3.2) with A0 and with WAo are equivalent from the standpoint
of the data. That is, there is a family of observationally equivalent representations (3.2),
for the data. Each corresponds to a different choice of A0.
We now discuss the implications of this observational equivalence result for
impulse response functions. Recall from Equation (3.6) that, conditional on the Bz's
characterizing the VAR of Zt, the dynamic response functions of Zt to et are determined
by Ao 1. Also, note that (WAo) -1 = Ao I W I. Two important conclusions follow from these
observations. First, the impulse response functions of Zt to the first three elements of
et are invariant to the choice of A0 belonging to the set of observational equivalent A0's
defined above, i.e., generated using W~s of the form given by Equation (5.4). Second,
the dynamic response functions to the last five elements of et are not. To the extent
that one is only interested in the response functions to the first three elements of et, the
precise choice of ff~ is irrelevant. Sims and Zha choose to work with the A0 satisfying
Equation (5.3) and the additional restriction that the square matrix formed from the
bottom right 5 × 5 matrix in A0 is upper triangular. 66 The corresponding dynamic
response functions of Zt to the last five shocks in et simply reflect this normalization.
We now make some summary remarks regarding identification of the SZ model. In
Section 3 we discussed an order condition which, in conjunction with a particular rank
condition, is sufficient for local identification. According to that order condition, we
need at least 28 restrictions on A0. The restrictions in Equation (5.3), along with the
normalization mentioned in the previous paragraph, represent 31 restrictions on A0.
So, we satisfy one of the sufficient conditions for identification. The rank condition
must be assessed at the estimated parameter values. Finally, to help guarantee global
identification, Sims and Zha impose the restriction that the diagonal element of A0 are
positive.
5.1.2. Empirical results
We organize our discussion of the empirical results around three major questions.
First, what are the effects of a contractionary monetary policy shock using the
SZ identification scheme? Second, how do these effects compare to those obtained
using the benchmark identification scheme? Third, what is the impact on Sims
and Zha's (1998) results of their assumption that the variables in Xt respond
contemporaneously to a monetary policy shock?
66 The A0 matrix is contained in the set of observationally equivalent A0 's as long as that set is non-empty.
To see this, suppose there is some A0 that satisfies (i) Equation (5.3) and (ii) the relation A~1 (Aol) I = V.
Let QR denote the QR decomposition of the lower right 5 × 5 part of this matrix ~. The 5 × 5 matrix
Q is orthonormal and R is upper triangular. Then, form the orthonormal matrix W as in Equation (5.4),
with W = Qt. The matrix WAo satisfies (i) and (ii) with the additional restriction on Equation (5.3) that
the lower fight 5 × 5 matrix in A0 W is upper triangular. This establishes the result sought.

132 L.J Christiano et al.
To answer these questions, we employ a version of the SZ model in which Mt
corresponds to M2 growth and Rt corresponds to the 3 month Treasury Bill Rate. 67
The four-lag VAR model was estimated using data over the period 1965Q3-1995Q2.68
Our results are presented in column 1 of Figure 11. The solid lines correspond to our
point estimates of the dynamic response of the variables in Zt to a contractionary
monetary policy shock. The dotted lines represent 95% confidence intervals about the
mean of the impulses. 69 The main consequences of a contractionary SZ policy shock
can be summarized as follows. First, there is a persistent decline in the growth rate
of M2 and a rise in the interest rate. Second, there is a persistent decline in the GDP
deflator and the prices of intermediate goods and crude materials. Third, after a delay,
the shock generates a persistent decline in real GDP. Finally, note that the real wage
is basically unaffected by the SZ policy shock. Comparing these results with those in
Figure 2, we see that the qualitative response of the system to an SZ policy shock
is quite similar to those in the benchmark FF and NBR systems. It is interesting to
note that the estimated SZ policy shocks are somewhat smaller than the estimated
benchmark FF policy shocks. For example, the impact effect of a benchmark FF policy
shock on the federal funds rate is about 70 basis points, while the impact of a SZ policy
shock on the three-month Treasury bill rate is about 40 basis points. At the same time,
the SZ policy shock measure is roughly of the same order of magnitude as an NBR
policy shock. In both cases a policy shock is associated with a forty basis point move
in the federal funds rate.
We now turn to the third question posed above. We show that Sims and Zha's
insistence that Xt is not predetermined relative to a monetary policy shock has
essentially no impact on their results. To do this, we simply shut down the coefficients
in A0 which allow a monetary policy shock to have a contemporaneous impact on
Xt and reestimate the system. Column 2 in Figure 11 reports the results. Comparing
columns 1 and 2, we see that inference is virtually unaffected.
It is interesting to compare the SZ model with the analysis in Leeper et al. (1996).
They work with a system that contains more variables. But, the fundamental difference
is that they impose the assumption that goods market variables are predetermined
67 The variable, Tbk, is not used in our analysis. Also, SZ measure M as the log level of M2. Comparing
the estimated dynamic response functions to a monetary shock in our version of SZ with those in SZ it
can be verified that these two perturbations make essentially no difference to the results.
68 The variable, Pcm, was measured as the log of the producer price index for crude materials, SA;
Pim is the logged producer price index for intermediate materials, SA; Y is logged GDP in fixed-weight
1987 dollars, SA; P is the logged GDP deflator derived from nominal GDP and GDP in fixed-weight
1987 dollars, SA; R is the three-month Treasury bill rate; and the change in the log of M2, SA. These
data series are taken from the Federal Reserve Board's macroeconomic database. Logged average hourly
earnings of private nonagricultural production workers are divided by the GDP deflator, SA, and are
derived from the Citibase data set.
69 These were computed using the procedure described in Sims and Zha (1995).

Ch. 2: Monetary Policy Shocks." What Have we Learned and to What End? 133
Sims_Zha, Quarterly ~Sim,s-Zh~a Mon thly
MP Shock => GDP MP Shock => GDP
0.40 I
o.oo| I ~ . ~ ~ ooo
-0.40 / -- -- ~ ~ R -ors
o 80 . o . . .3 . 6 9 -0,32 1 8 15 22 29
quarters months
MP Shock => GDP Price Deflator MP Shock => PCE Price Deflator
0.1B 0.18
-0.18
-0.36 ~ . . .
-0.54 o 3 quarters 6 9 1 8 month 1 s 5 22
MP Shock => FF MP Shock => FF
0.80
/\\
0.30
o.o0 ~.~ ~ . . . . . ~ 8. o.oo
-0.40 o 3 6 9 -0.3O ... 1 .. . 8 15 22 2g
quarters months
MP Shock => Growth in M2 MP Shock => Growth in M2
O,OB
&
/
-O.4 0 3 6 0 1 8 15 23 29
quarters months
MP Shock => Crude Materials Prices MP Shock => Crude Materials Prices
0.25 0.5 / ~ - - ~ - - ~
0.oo . . . . . . o.o --~-'
-o.2s /
-0.50 ~ ~ ~ ~ -- ~ ~ ~ -1 .o
-0.75 0 3 6 9 -1,5 1 8 15 22 29
quarters months
MP Shock=> Intermediate Materials Prices MP Shock => Intermediate Materials Prices
03
-0.30
-0.60
-t.6 -0.~
o 3 6 9 1 8 15 22 29
qua~ers months
MP Shock => Real Wages MP Shock => Real Wages
0.32
-0.12 ~ "~
-0.16 -0 04 '"
-0.32 O.36 ....................................
o 3 6 9 1 8 15 22 29
quaders months
Fig. 11.

134 L.J. Christiano et al.
relative to a monetary policy shock. 70 The response to a monetary policy shock of
the variables that these analyses have in common is very similar. This is consistent
with our finding that the absence of predeterminedness of good market variables in
the SZ model is not important.
A number of other studies also impose predeterminedness of at least some goods
market variables. These include Sims (1986), who assumes predeterminedness of
investment, and Gordon and Leeper (1994), who assume all goods market variables and
the 10 year Treasury rate are predetermined. Inference about the dynamic response of
economic aggregates is very similar across these papers, Sims and Zha (1998), Leeper
et al. (1996) and the benchmark systems.
6. Some pitfalls in interpreting estimated monetary policy rules
In Sections 4 and 5 we reviewed alternative approaches for identifying the effects of
a monetary policy shock. A common feature of these different approaches is that they
make enough identifying assumptions to enable the analyst to estimate the parameters
of the Federal Reserves's feedback rule. A natural question is: why did we not display
or interpret the parameter estimate? The answer is that these parameters are not easily
interpretable.
In this section we describe three examples which illustrate why the estimated policy
rules are difficult to interpret in terms of the behavior of the monetary authority. We
emphasize, however, that the considerations raised here need not necessarily pose a
problem for the econometrician attempting to isolate monetary policy shocks and their
consequences.
The central feature of our examples is that the policy maker reacts to data that
are different from the data used by the econometrician. In the first example, the
decision maker uses error-corrupted data, while the econometrician uses error-free
data. In the second and third examples the decision maker reacts to a variable that
is not in the econometrician's data set. The policy rule parameters estimated by the
econometrician are a convolution of the parameters of the rule implemented in real time
by the policy maker and the parameters of the projection of the missing data onto the
econometrician's data set. It is the convolution of these two types of parameters which
makes it difficult to assign behavioral interpretations to the econometrician's estimated
policy rule parameters.
Our first example builds on the measurement error example discussed in Section 2.
We assume there is measurement error in the data used by real time policy makers,
while the econometrician uses final revised data. We suppose xt + vt corresponds to the
70 In their description of the model, monetary policy shocks impact on the analog of X via a limited
set of variables. In practice, however, they set the coefficients on these variables equal to zero. So, all
their estimated systems have the property that the goods market variables are predetermined relative to
the monetary policy shock.

Ch. 2: Monetary Policy Shocks: What Have we Learned and to What End? 135
raw data received by the primary data collection agency and that o t reflects classical
reporting and transmission errors that are uncorrelated with the true variable, xt, at all
leads and lags. In addition, we suppose that the reporting errors are discovered in one
period, so that ut in Equation (2.2) is zero. We assume that the data collection agency
(or, the staff of the policy maker) reports its best guess, ~?t, of the true data, xt, using
its knowledge of the underlying data generating mechanism and the properties of the
measurement error process. 71 Finally, suppose that xt evolves according to
xt = plSt-1 + p2xt-1 + oat,
where rot is uncorrelated with all variables dated t- 1 and earlier. Suppose the data
collection authority computes ~?t as the linear projection ofxt on the data available to
it. Then,
fft = Pxt St 1, xt + ut, xt 1 = a0St-I + al (xt + ut) + a2x~l, (6.1)
where the ai's are functions of pl,/)2, and the variances of oat and or. Now, suppose
that the policy authority is only interested in responding to xt, and that it attempts to
do so by setting
St = a2ct (6.2)
in real time. Substituting Equation (6.1) into this expression, we see that Equation (6.2)
reduces to Equations (2.1) and (2.4) with
to = aao, 31 = aal, 32 = aa2. (6.3)
Notice how different the econometrician's estimated policy rule, (2.4) and (6.3), is from
the real time policy rule (6.2). The 3's in the estimated policy rule are a convolution
of the behavioral parameter, a, the measurement error variance, and the parameters
governing the data generating mechanism underlying the variables that interest the
policy maker. 72 Also notice that an econometrician who estimates the policy rule using
the recursiveness assumption will, in population, correctly identify the monetary policy
shock with aalvt.
This example shows how variables might enter f, perhaps even with long lags,
despite the fact that the policy maker does not care about them per se. In the example,
the variables St-l and xt-i enter only because they help solve a signal extraction
problem. Finally, the example illustrates some of the dangers involved in trying to give
71 For a discussion of the empirical plausibility of this model of the data collection agency, see Mankiw
et al. (1984), and Mankiw and Shapiro (1986).
72 See Sargent (1989), for a discussion of how to econometrically unscramble parameters like this in
the presence of measurement error.

136 L.J. Christiano et al.
a structural interpretation to the coefficients in f Suppose a0 and a are positive. An
analyst might be tempted to interpret the resulting positive value of/3o as reflecting
a desire to minimize instrument instability. In this example, such an interpretation
would be mistaken. Significantly, even though the estimated policy rule has no clear
behavioral interpretation, the econometrician in this example correctly identifies the
exogenous monetary policy shock.
For our second example, we assume that the policy maker responds only to the
current innovation in some variable, for example, output. In particular suppose that,
St = aet + cr~.Et,
where e~ is the innovation to which the policy maker responds, a is the policy
parameter, and E~ is the exogenous policy shock. Suppose that et is related to data
in the following way, et = ~i~-o/3ixt-i, so that in Equation (2.1),
O<75
f ( f2t ) : a Z 3ixt-i.
i=0
Suppose the econometrician makes the correct identification assumptions and recovers
f(U2t) exactly. An analyst with sharp priors about the number of lags in the policy
maker's decision rule, or about the pattern of coefficients in that rule, might be misled
into concluding that fundamental specification error is present. In fact, there is not.
The disturbance recovered by the econometrician, St -f(f2t), corresponds exactly to
the exogenous monetary policy shock.
Our final example is taken from Clarida and Gertler (1997) and Clarida et al. (1997,
1998). They consider the possibility that the rule implemented by the policy authority
has the form St = aEtxt+l + crseT. In this case, f(f2t) = aEtxt+i, and £2t contains all the
variables pertinent to the conditional expectation, Etxt+b Assuming there is substantial
persistence in xt, f will contain long lags and its coefficients will be hard to interpret
from the standpoint of the behavior of policy makers. 73
These examples suggest to us that direct interpretation of estimated policy rules is
fraught with pitfalls. This is why we did not discuss or report the estimated policy
rules. Instead, we focused on dynamic response functions of economic aggregates to
monetary policy shocks.
7. The effects of a monetary policy shock: the narrative approach
In the previous sections, we have discussed formal statistical approaches to identifying
exogenous monetary policy shocks and their effects on the economy. The central
73 Claridae t al. (1997, 1998) estimate the parameters of forward lookingp olicy rules, so that in principle
they can uncover interpretable parameters like a.

Ch. 2: Monetary Policy Shocks: What Have we Learned and to What End? 137
problem there lies with the identification of the exogenous monetary policy shock
itself. As we discussed above, there are many reasons why shocks measured in this way
may not be exogenous. These include all the reasons that policy rules, like (2.1), might
be misspecified. For example, there may be subsample instability in the monetary
policy rule, policymakers' information sets may be misspecified. In addition, the
various auxiliary assumptions that must be made in practice, e.g., the specification
of lag lengths, are always subject to question. Romer and Romer motivate what they
call the narrative approach as a way of identifying monetary policy shocks that avoids
these difficulties. 74
This section is organized as follows. First, we discuss the specific identifying
assumptions in Romer and Romer's analysis. Second, we contrast results obtained
under their assumptions with the benchmark results reported above. 75
Any approach that wishes to assess the effects of a monetary policy action on the
economy must grapple with the endogeneity problem. Romer and Romer (1989) do so
by identifying episodes (p. 134) "... when the Federal Reserve specifically intended
to use the tools it had available to attempt to create a recession to cure inflation."
They select such episodes based on records pertaining to policy meetings of the
Federal Reserve. They interpret the behavior of output in the wake of these episodes as
reflecting the effects of monetary policy actions and not some other factors. To justify
this interpretation, they make and attempt to defend two identifying assumptions.
First, in these episodes, inflation did not exert a direct effect on output via, say, the
anticipated inflation tax effects emphasized in Cooley and Hansen (1989). Second,
in these episodes inflation was not driven by shocks which directly affected output,
such as supply shocks. These two assumptions underlie their view that the behavior
of output in the aftermath of a Romer and Romer episode reflected the effects of the
Fed's actions.
The Romer and Romer (1989) episodes are: December 1968; April 1974; August
1978; October 1979. We follow Kashyap et al. (1993) by adding the 1966 credit crunch
(1966:2) to the index of monetary contractions. In addition, we add the August 1988
episode identified by Oliner and Rudebusch (1996) as the beginning of a monetary
contraction. 76 For ease of exposition, we refer to all of these episodes as Romer and
Romer episodes.
It is difficult to judge on a priori grounds whether the narrative approach or the
strategy discussed in the previous sections is better. The latter approach can lead to
misleading results if the wrong identifying assumptions are made in specifying the
Fed's policy rule. A seeming advantage of Romer and Romer's approach is that one
is not required formally to specify a Fed feedback rule. But there is no free lunch.
74 They attribute the narrative approach to Friedman and Schwartz (1963).
75 See Christiano et al. (1996b), Eichenbaum and Evans (1995) and Leeper (1997) for a similar
comparison.
76 In a later paper, Romer and Romer (1994) also add a date around this time.

138 L.J Christiano et al.
2.0 I
I
1.5
I
I
I
1.0
0.5
"E
.o
0.0
Q.
-0.5
NBR model - -
-1.0
Fed Funds model ....
-F
-1.5 , ,,, ~ -|, f , 1 t f -
67 74 81 88
Three-month centered, equal-weighted moving average
Fig. 12. Contractionary benchmark policy shocks in units of federal funds rate; three-month centered,
equal-weighted moving average, with Romer dates.
As we pointed out, they too must make identifying assumptions which are subject to
challenge. Shapiro (1994) for example challenges the usefulness of these dates on the
grounds that they do not reflect an exogenous component of monetary policy. In his
view, they reflect aspects of monetary policy that are largely forecastable using other
macro variables. An additional shortcoming of the Romer and Romer approach, at
least as applied to postwar monetary policy, is that it delivers only a few episodes of
policy actions, with no indications of their relative intensity. In contrast, the strategy
discussed in the previous section generates many "episodes", one for each date in the
sample period, and a quantitative measure of the intensity of the exogenous shock for
each date. So in principle, this approach can generate more precise estimates of the
effects of a monetary policy shock.
It is of interest to compare the Romer and Romer episodes with the benchmark FF
and NBR shocks. According to Figure 12, with one exception each Romer and
Romer episode is followed, within one or two quarters, by a contracfionary FF
and NBR policy contraction. The exception is October 1979, which is not followed

Ch. 2: Monetary Policy Shocks: What Have we Learned and to What End? 139
by a contractionary NBR policy shock. 77 At the same time, we identify several
contractionary policy shocks which are not associated with a Romer and Romer
episode.
We now turn to the issue of how qualitative inference is affected by use of the
Romer and Romer index. To determine the impact of a Romer and Romer episode
on the set of variables, Zt, we proceed as follows. First, we define the dummy
variable, dr, to be one during a Romer and Romer episode, and zero otherwise.
Second, we modify the benchmark VAR to include current and lagged values of
d,:
Zt = A(L)Zt 1 q-~(L)dt --ut. (7.1)
Here, fi(L) is a finite ordered vector polynomial in nonnegative powers of L. We
estimate Equation (7.1) using equation-by-equation least squares. For calculations
based on quarterly data, the highest power of L in A(L) and in /3(L) are 5 and
6, respectively. For calculations based on monthly data, the corresponding figures
are 11 and 12. The response of Z¢+/~ to a Romer and Romer episode is given by
the coefficient on L I~ in the expansion of I-A(L)L -I fi(L). To obtain confidence
intervals for the dynamic response function of Zt, we apply a version of the
bootstrap Monte Carlo procedure used above which accommodates the presence of
dt in Equation (7.1). In principle, the right way to proceed is to incorporate into
the bootstrap simulations a model of how the Fed and then Romer and Romer
process the data in order to assign values to dr. This task is clearly beyond the
scope of this analysis. In our calculations, we simply treat dt as fixed in repeated
samples.
We also report results obtained using the monetary policy index constructed by
Boschen and Mills (t991). Based on their reading of the FOMC minutes, Boschen
and Mills rate monetary policy on a discrete scale, {-2, -1,0, 1,2} where -2 denotes
very tight and +2 denotes very loose. To look at the effects of this policy measure, we
include it in our definition of Zt and calculate the dynamic response of the variables
in Zt to an innovation in the Boschen and Mills index.
Figure 13 reports the monthly data based estimates of the dynamic response of
various aggregates to a Romer and Romer shock and an innovation in the Boschen
and Mills index. To facilitate comparisons, column 1 reproduces the dynamic response
functions associated with our monthly benchmark FF policy shocks.
According to our point estimates, the qualitative responses to an FF policy shock
and a Romer and Romer episode shock are quite similar: the federal funds rate
rises, the price level is not much affected, at least initially, employment falls with
a delay, PCOM falls, and all the monetary aggregates (NBR, M1 and M2) fall. It
is interesting that the initial impacts of a Romer and Romer episode on employment
77 We cannot estimate benchmark shocks for 1966:2 because of data limitations.

140 L.J Christiano et al.
Monthly Fed Funds Model with M1 Monthly Romer Model with M1 Monthly Boschen & Mills Model with M1
MP Shock => EM MP Shock => EM MP Shock => EM
MP Shock => Price MP Policy Shock => Price MP Shock -> Price
:°dl- ~
~22
MP Shock => Pcom MP Policy Shock => Pcom MP Shock => Pcom
i!:!!i
MP Shock => FF MP Policy Shock => FP MP Shock => FF
~1 o,~
io !
MP Shock => NBR MP Policy Shock -> NBR MP Shock -> NBR
\rv~J
°° ~x / . . . . . ------ -
MP Shock => TFI MP Policy Shock -> TR MP Shock => TR
0~ °0~ ~ .....
.0~ 0,
MP Shock => M1 MP Pollcy Shock => M1 MP Shock > M1
0 i,
2° , - - ~ ....
~° a ~
:°°2
Monthly Fed Funds Model with M2 Monthly Romer Model with M2 MontNy Boschen & Mills Model with M2
o= MP Shock => M2 MP Policy Shock > M2 MP Shock -> M2
N\ -- --\ / j
0,
Not Applicable Not Applicable MP Shock=> Bo Mi Index
0~0
Fig. 13. The monthly data based estimates of the dynamic response of various aggregates to a Romer
and Romer shock and an innovation in the Boschen and Mills index. To facilitate comparisons, colunm 1
reproduces the dynamic response functions associated with our monthly benchmark FF policy shocks.

Ch. 2: Monetary Policy Shocks: What Have we Learned and to What End? 141
and the price level are quite small. Unlike the identification schemes underlying the
benchmark shock measures, this is not imposed by the Romer and Romer procedure.
There are some differences between the estimated effects of the two shock measures.
These pertain to the magnitude and timing of the responses. Romer and Romer
episodes coincide with periods in which there were large rises in the federal funds
rate. The maximal impact on the federal funds rate after a Romer and Romer episode
is roughly 100 basis points. In contrast, the maximal impact on the federal funds
rate induced by an FF policy shock is roughly 60 points. Consistent with this
difference, the maximal impact of a Romer and Romer shock on employment, PCOM,
NBR, TR, M1 and M2 is much larger than that of a FF policy shock. Finally,
note that the response functions to a Romer and Romer shock are estimated less
precisely than the response functions to an FF policy shock. Indeed, there is little
evidence against the hypothesis that output is unaffected by a Romer and Romer
shock. 78
While similar in some respects, the estimated response functions to an innovation
in the Boschen and Mills results do differ in some important ways from both the
FF and Romer and Romer shocks. First, the impact of a Boschen and Mills shock
is delayed compared to the impact of the alternative shock measures. For example
the maximal increase in the federal funds rate occurs 14 months after a Boschen and
Mills shock. In contrast, the maximal increase of the federal funds rate occurs 1 and
3 periods after an FF and Romer and Romer shock, respectively. Another anomaly
associated with the Boschen and Mills response functions is the presence of a price
puzzle: both PCOM and the price level rise for a substantial period of time after a
contraction.
Figure 14 reports the quarterly data based estimates of the dynamic response of
various aggregates to a Romer and Romer shock and an innovation in the Boschen
and Mills index. The key finding here is that the qualitative properties of the
estimated impulse response functions associated with the three policy shock measures
are quite similar. Unlike the monthly results where employment initially rises in
response to a Romer and Romer episode, there is no initial rise in aggregate output.
The only major difference is that, as with the monthly data, the maximal impact
of a Boschen and Mills shock measure on the federal funds rate is substantially
delayed relative to the other two shock measures. Integrating over the monthly
and quarterly results, we conclude that qualitative inference about the effects of a
monetary policy shock is quite robust to the different shock measures discussed in
this section.
7s Romer and Romer report statistically significant effects on output. This difference could arise for
two reasons. First, we include more variables in our analysis than do Romer and Romer. Second, we
compute standard errors using a different method than they do.

142 L.J Christiano et al.
Fed Funds Model with M1 Romer Model with M1 Boschen & Mills Model with M1
MP Shock => Y o~ MP Shock => Y MP Shock => Y
o-o! ~k% 'E~LF---- ---~ ~2-~ -
"1 xX./ . . - - _ -- I
MP Shock => Price MP Policy Shock => Price MP Shock => Price
,~1 ...................... ?-- °0N ~-.
MP Shock => Pcom MP Policy Shock => Pcom MP Shock => Pcom
J
MP Shock => FF MP Policy Shock => PP MP Shock => FF
MP Shock => NBR MP Policy Shock => NBR MP Shock => NBR
iil
........
:S 7 y o 2~_r ,,
MP Shock => TR MP Policy Shock => TR MP Shock => TR
MP Shock => M1 MP Policy Shock => M1 MP Shock => M1
Fed Funds Model with M2 Romer Model with M2 Boschen & Mills Model with M2
MP Shock => M2 MP Policy Shock => M2 MP Shock => M2
iji
iit W---- ........ '
.......
Not Applicable Not Applicable MP Shock => Bo Mi index
:::I
,"---- .......
iil Y"-
i
Fig. 14. The quarterly data based estimates of the dynamic response of various aggregates to a Romer
and Romer shock and an innovation in the Boschen and Mills index.

Ch. 2: Monetary Policy Shocks: What Have we Learned and to What End? 143
8. Conclusion
In this chapter we have reviewed the recent literature that grapples with the question:
What happens after a shock to monetary policy? This question is of interest because it
lies at the center of the particular approach to model evaluation that we discussed: the
Lucas program applied to monetary economics. The basic step in that program involves
subjecting monetary models to a particular experiment: a monetary policy shock.
Since alternative models react very differently to such a shock, this experiment can, in
principle, be the basis of a useful diagnostic test. But to be useful in practice, we need
to know how the actual economy responds to the analog experiment. Isolating these
data based experiments requires identifying assumptions. We argued that qualitative
inference about the effects of a monetary policy shock is robust across many, but not
all the sets of identifying assumptions that have been pursued in the literature.
A key question remains: How can the results of the literature we reviewed be
used to quantitatively assess the performance of a particular model? Much of the
empirical literature on monetary policy shocks proceeds under the assumption that
monetary policy is highly reactive to the state of the economy. In sharp contrast,
analyses of quantitative general equilibrium models often proceed under much simpler
assumptions about the nature of the monetary authority's reaction function. This leads
to an obvious problem: unless the monetary policy rule has been specified correctly,
the nature of the monetary experiment being conducted in the model is not the same
as the experiment in the data.
One way to deal with the problem is to solve theoretical models using estimated
reaction functions taken from the policy shock literature. There are two potential
problems associated with this approach. First, and most importantly, it is often the case
that models have multiple equilibria when policy is specified as a relationship between
endogenous variables. Second, the complexity of estimated reaction functions makes it
difficult (at least for us) to gain intuition for the way a monetary policy shock impacts
on a model economy.
Christiano et al. (1997b) suggest an alternative approach to ensuring the consistency
between model and data based experiments. The basic idea is to calculate the dynamic
effects of a policy shock in a model economy under the following representation of
monetary policy: the growth rate of money depends only on current and past shocks
to monetary policy. Formally such a specification represents the growth rate of money
as a univariate, exogenous stochastic process. However this representation cannot be
developed by examining the univariate time series properties of the growth rate of
money, say by regressing the growth rate of money on its own lagged values. Instead
the representation must be based on the estimated impulse response function of the
growth rate of money to a monetary policy shock.
The rationale underlying the proposal by Christiano et al. (1997b) is as follows. To
actually implement a particular monetary policy rule, the growth rate of money must
(if only implicitly) respond to current and past exogenous shocks in an appropriate
way. This is true even when the systematic component of policy is thought of as a

144 L.J. Christiano et al.
relationship between endogenous variables, like the interest rate, output and inflation.
The literature on monetary policy shocks provides an estimate of the way the growth
rate of money actually does respond to a particular shock - a monetary policy shock.
For concreteness we refer to the estimated impulse response function of the growth
rate of money to a policy shock as "the exogenous monetary policy rule". 79
Suppose that an analyst solves a monetary model under the assumption that policy
is given by the exogenous policy rule. In addition, suppose that the model has
been specified correctly. In this case, the dynamic responses of the model variables
to a policy shock should be the same as the dynamic response functions of the
corresponding variables to a policy shock in the VAR underlying the estimate of
exogenous policy rule [see Christiano et al. (1997b)]. This is true even if the monetary
policy shock was identified in the VAR assuming a policy rule that was highly reactive
to the state of the economy. So, the empirical plausibility of a model can be assessed
by comparing the results of an exogenous policy shock in the model to the results of
a policy shock in a VAR.
It is often the case that a model economy will have multiple equilibria when policy
is represented as a relationship between endogenous variables. Each may be supported
by a different rule for the way the growth rate of money responds to fundamental
economic shocks. Yet, for any given rule relating the growth rate of money to these
shocks, it is often (but not always) the case that there is a unique equilibrium [see
Christiano et al. (1997b) for examples]. Under these circumstances the proposal by
Christiano et al. (1997b) for evaluating models is particularly useful. The monetary
policy shock literature tells us which exogenous policy rule the Fed did adopt and
how the economy did respond to a policy shock. These responses can be compared to
the unique prediction of the model for what happens after a shock to monetary policy.
However, it is unclear how to proceed under a parameterization of monetary policy in
which there are multiple equilibria.
We conclude by noting that we have stressed one motivation for isolating the
effects of a monetary policy shock: the desire to isolate experiments in the data
whose outcomes can be compared with the results of analog experiments in models.
Authors like Sims and Zha (1998) and Bernanke et al. (1997) have pursued a different
motivation. These authors argue that if the analyst has made enough assumptions to
isolate another fundamental shock to the economy, then it is possible to understand
the consequences of a change in the systematic way that monetary policy responds
to that shock, even in the absence of a structural model. Their arguments depend in
a critical way on ignoring the Lucas critique. This may or may not be reasonable in
their particular applications. We are open minded but skeptical. For now we rest our
79 Christiano et al. (1997b) argue that a good representation for the exogenous monetary policy rule
relating the growth rate of M1 to current and past policy shocks is a low order MA process with a
particular feature: the contemporaneous effect of a monetary policy shock is small while the lagged
effects are much larger. In contrast, the dynamic response function of the growth rate of M2 to current
and past policy shocks is well approximated by an AR(1) process.

Ch. 2: Monetary Policy Shocks: What Have we Learned and to What End? 145
case for the usefulness of the monetary policy shock literature on the motivation we
have pursued: the desire to build structural economic models that can be used to think
about systematic changes in policy institutions and rules.