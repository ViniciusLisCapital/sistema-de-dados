NBER WORKING PAPER SERIES
OPTIMAL MONETARY POLICY INERTIA
Michael Woodford
Working Paper 7261
http://www.nber.org/papers/w7261
NATIONAL BUREAU OF ECONOMIC RESEARCH
1050 Massachusetts Avenue
Cambridge, MA 02138
July 1999
I would like to thank Alan Blinder, Gregory Chow, Ray Fair, Mark Gertler, Marvin Goodfriend, Bob Hall, Pat
Kehoe, Nobuhiro Kiyotaki, Phillipe Moutot, Athanasios Orphanides, Tom Sargent, Lars Svensson, John
Vickers, Carl Walsh, Julian Wright, and especially Julio Rotemberg, for helpful discussions, and Marc
Giannoni for excellent research assistance. I also thank the National Science Foundation, the John Simon
Guggenheim Foundation, and the Center for Economic Policy Studies, Princeton University for research
support.  The views expressed herein are those of the authors and not necessarily those of the National
Bureau of Economic Research.
© 1999 by Michael Woodford.  All rights reserved.  Short sections of text, not to exceed two paragraphs, may

be quoted without explicit permission provided that full credit, including © notice, is given to the source.
Optimal Monetary Policy Inertia
Michael Woodford
NBER Working Paper No. 7261
July 1999
JEL No.  E52
ABSTRACT
This paper considers the desirability of the observed tendency of central banks to adjust
interest rates only gradually in response to changes in economic conditions.  It shows, in the
context of a simple model of optimizing private-sector behavior, that such inertial policy can
be optimal.  The reason is that small but persistent changes in short-term interest rates in
response to shocks allow a larger effect of monetary policy on long rates and hence upon
aggregate demand, for a given degree of overall interest-rate variability.
The paper also considers two ways of achieving the desirable degree of inertia in the
equilibrium responses to shocks.  One is by assignment of a loss function that penalizes
squared interest-rate changes (despite the fact that interest-rate changes do not affect the true
social objective) to a central bank that is then expected to use discretion in the pursuit of the
goal.  The second is through commitment to an explicit instrument rule, a generalization of the
“Taylor rule” in which the funds rate is an increasing function of the lagged funds rate, as in
estimated Fed reaction functions.
Michael Woodford
Department of Economics
Princeton University
Princeton, NJ 08544
and NBER
woodford@princeton.edu

1
Central Bank Inertia and Optimal Policy
Many students of central bank behavior have commented on the fact that the level of nominal
interest rates in the recent past appears to be an important determinant of where the central
bank will set its interest-rate instrument in the present. Changes in observed conditions, such
as in the rate of inﬂation or in the level of economic activity, result in changes in the level of
the central bank’s operating target for the short-term interest rate that it controls, but these
changes typically occur through a series of small adjustments in the same direction, drawn
out over a period of months, rather than through an immediate once-and-for-all response
to the new development. This type of behavior is especially noticeable in the case of the
Federal Reserve in the U.S., but characterizes many other central banks to at least some
extent as well.
One way that this inertial character of central bank behavior shows up is in estimated
central-bank reaction functions.
Many studies model the Fed’s behavior in terms of an
implicit “target” level for the federal funds rate that depends upon the current rate of
inﬂation and a measure of real activity.1 A typical speciﬁcation is of the form
¯rt = r∗+ φπ(πt −π∗) + φy(yt −y∗
t ),
(1.1)
where ¯rt is the funds rate target, πt is a measure of inﬂation, π∗is the Fed’s (implicit) target
rate of inﬂation, yt is a measure of output, y∗
t a measure of trend or potential output, and
r∗, φπ, and φy are a set of constant coeﬃcients. Estimated reaction functions of this form,
however, always incorporate some form of partial adjustment of the actual funds rate toward
this target, for example by specifying that the actual funds rate2 rt follows a law of motion
of the form
rt = θrt−1 + (1 −θ)¯rt
(1.2)
1Such speciﬁcations have been used in macroeconometric models since at least the work of Fair (1978,
1979). Interest in such speciﬁcations has recently been revived by the inﬂuential discussion by Taylor (1993).
2Actually, in this equation rt refers to the Fed’s operating target for the funds rate, which it seeks to
achieve through its daily interventions. The actual (spot) funds rate may vary considerably from this level
during the day, though such deviations from the Fed’s operating target are largely eliminated by the next
day. See Rudebusch (1995).
2

where the coeﬃcient θ measures the degree of inertia in the central bank’s response. Sack
(1998b) estimates a reaction function of the form given by (1.1) – (1.2), using quarterly
data for the U.S. during the Greenspan chairmanship of the Fed. His estimated value for
θ is .63, with a standard error of .08.3 The estimated degree of inertia is thus large and
highly signiﬁcant. Other estimates for the U.S. yield similar magnitudes,4 and Clarida et al.
(1998b) report similar values of θ in estimated reaction functions for several other central
banks.
Another sort of evidence, not dependent upon an assumed speciﬁcation of the variables
to which the Fed reacts, is provided by Rudebusch (1995), who analyzes the statistical
properties of changes in the Fed’s operating target for the funds rate over the periods 1974-
1979 and 1984-1992.5 Rudebusch shows the Fed’s discrete target changes are much more
likely to be followed by another change of the same sign than by a change of the opposite sign,
though the hazard rate for another change of the same sign falls as the length of time since
the last target change increases, so that after an interval of ﬁve weeks with no change, the
next change is about equally likely to have either sign.6 Goodhart (1996) supplies further
evidence in the same vein, and shows that several other central banks appear to behave
similarly, though the tendency for target changes to be followed by further changes in the
same direction is strongest for the Fed. These statistics are consistent with a discretized
version of a partial-adjustment model like (1.2), in which a movement of the underlying
target rate ¯rt away from the current funds rate level results in a series of changes in the
operating target rt, each in the direction that reduces the discrepancy between rt and ¯rt.
What should one make of this feature of central bank behavior?
A common view is
that it shows that central banks are too slow to respond to new information that indicates
3This is his OLS estimate. An instrumental variables estimate is also reported, of .65 with a standard
error of .06.
4See, e.g., , Clarida et al. (1998a) and Orphanides (1997). Fair (1978, 1979) ﬁnds an even higher degree
of inertia using data from an earlier period.
5These periods are studied as they are ones in which it is reasonably clear that Fed policy was conducted
in terms of an operating target for the funds rate. The target rate series is obtained from internal documents
of the Federal Reserve Bank of New York Trading Desk. This series refers to the variable denoted rt in (1.2),
not to the unobserved variable ¯rt.
6Sack (1998a) shows that similar conclusions hold for a sample that is extended through 1997.
3

the inappropriateness of current policy.
The fact that further interest rate changes are
somewhat forecastable is taken to indicate that the central bank delays taking actions the
need for which could already be seen weeks or months earlier.
7 This is often supposed to
be due to an unwillingness of central banks to act before the situation becomes dire enough
for public opinion and political leaders to agree upon the need for action, or perhaps to a
simple unwillingness of central bankers to suggest that previous policy choices can ever have
been mistaken. In either case, the inertial character of policy is regarded as something that
makes monetary policy less eﬀective, especially in the stabilization of short-run ﬂuctuations
in inﬂation or other target variables.
It is sometimes said that central banks seek to “smooth” interest rates, in the sense
that they seek to minimize the variability of interest-rate changes, in addition to their other
objectives such as inﬂation stabilization. But models of optimizing central bank behavior
that incorporate such an objective seem to be motivated mainly by a desire to rationalize the
observed inertial character of interest rates, rather than by any plausible account of why such
an objective is actually appropriate.8 There are a number of reasons why policymakers should
prefer policies that do not require the level of short-term interest rates to be too variable. On
the one hand, the zero nominal interest-rate ﬂoor (resulting from the availability of cash as
a riskless, perfectly liquid zero-return asset) means that rates cannot be pushed below zero.
This means that a policy consistent with a low average rate of inﬂation, which implies a low
average level of nominal interest rates, cannot involve interest-rate reductions in response
to deﬂationary shocks that are ever too large. And at the same time, high nominal interest
7An explicit argument to this eﬀect is oﬀered by Goodhart (1998). If one supposes – as do many discussions
of “inﬂation targeting”, especially as currently practiced in the U.K. – that the interest-rate instrument should
respond solely to deviations of the central bank’s forecast of inﬂation some years in the future from a target
rate, then in the absence of changes in the inﬂation target, changes in short-term interest rates should reﬂect
changes in the inﬂation forecast, which should themselves be unforecastable. This view of what “inﬂation
targeting” should entail is, however, subjected to important qualiﬁcations in Svensson (1999). The view that
the desired level of interest rates at any point in time follows a random walk is also explicit, for example, in
Guthrie and Wright (1998).
8We do provide a possible rationalization for a central bank “smoothing objective” below, in section 4,
in terms of an optimal delegation problem. What we mean to argue here is that such a goal has no place
in a true social objective function, so that a reason for the central bank to care about it must be sought
elsewhere.
4

rates always imply distortions, as resources are wasted on unnecessary eﬀorts to economize
on cash balances. Friedman (1969) stresses that this is a reason to prefer a regime with low
average inﬂation, or even moderate deﬂation; but it is actually the level of nominal interest
rates that directly determines the size of the distortion, and the argument applies as much
to short-run variation in nominal interest rates as to their average level.9 Thus it is also
desirable on this ground for policy not to raise nominal interests too much in response to
inﬂationary shocks. In fact, if one supposes (by analogy with the standard argument for
distorting taxes) that the distortions associated with positive nominal interest rates are a
convex function of the interest rate, then, for any contemplated average level of interest
rates, a lower variance of interest rates will reduce’ the average size of these distortions.10
But while it makes a great deal of sense for a central bank to seek to achieve its other aims
in a way consistent with as low as possible a variance of the level of short-run nominal rates,
this in no way implies a direct concern with the variability of interest-rate changes.
If we discount any rational “smoothing” objective, it is often supposed that an optimizing
central bank should condition its actions only upon state variables that aﬀect either the
current or future determination of its goal variables (such as inﬂation). Thus past interest
rates as such should be of no signiﬁcance in determining the optimal current level of interest
rates, and neither should past perceptions of the direction in which interest rates needed (at
that time) to be adjusted. Nor should the past behavior of goal variables (such as inﬂation)
matter for current policy, except insofar as they may enter into central bank estimates
of relevant current states or forecasts of relevant future states. Thus it is supposed that
optimal policy would involve no true element of inertia at all; any persistence in interest rate
ﬂuctuations that would be observed under an optimal regime would have to be attributable
9See Woodford (1990) for discussion both of the generality of the argument that a positive nominal interest
rate implies a distortion of private incentives, and of its implications for the desirability of low interest-rate
variability.
10This is the basis for Mankiw’s (1987) argument for the desirability of interest-rate “smoothing,” in
the sense of eliminating predictable interest-rate variation. But “smoothing” in Mankiw’s sense would be
something very diﬀerent from the sort of inertial behavior discussed here, which implies predictable interest-
rate changes. In particular, Mankiw’s argument provides no reason why past interest rates, or other past
states, should matter for the determination of the optimal current level of interest rates.
5

to serial correlation in the underlying disturbances to which the central bank responds, and
not to any inertia in the central bank’s own response to those disturbances.11
But this conclusion, I believe, depends upon a misunderstanding of the kind of optimal
control problem that a central bank faces. In particular, it fails to take proper account of the
forward-looking character of private sector behavior. In the case of a standard (engineering)
optimal control problem, in which the system to be controlled evolves as a mechanical func-
tion of its current state (including possible exogenous random disturbances) and the current
setting of the control variable, then it is indeed true that the controller’s optimal action
(from the point of view of minimization of a loss function that depends in a time-separable
way upon the system state) at any point in time depends only upon the system’s state at
that time. Here the concept of the “state” of the system includes all information available
at a given time that can help to forecast its future evolution (conditional upon any assumed
path for the control variable), but does not include any details of past actions or states
that do not continue to exert a causal inﬂuence upon the determination of goal variables
at current or future dates. This is an important principle, and is at the heart of “dynamic
programming” approaches to optimal control. It is also an idea that continues to pervade
discussions of optimal monetary policy, which often assume a control problem of this kind,
owing to the absence of forward-looking elements in many of the econometric models used
for policy evaluation exercises, despite the warning of Lucas (1976) about the errors to which
this can lead.
A central bank that recognizes that private sector behavior is forward-looking (as this is
an inevitable result of private sector optimization) should instead realize that the evolution
of its goal variables depends not only upon its current actions, but also upon how the
11Of course, it would possible for an estimated central bank reaction function to include lagged interest-
rate terms even in the absence of true inertia, due to serial correlation in shocks, as in the results of Aoki
(1998). It is also possible that inertia might exist, consistent with the conventional (“dynamic programming”)
reasoning described here, simply because lagged interest rates aﬀect the determination of current and future
output and inﬂation, as in the results of Fair and Howrey (1996). In the model used here, such eﬀects of
lagged interest rates are excluded, to make clear that the explanation of inertia oﬀered here is of a diﬀerent
kind. Note that delayed eﬀects of monetary policy disturbances can be explained without relying upon any
such eﬀects (Rotemberg and Woodford, 1997).
6

private sector expects monetary policy to be conducted in the future. It follows from this
that a more desirable outcome may be achieved if it can be arranged for private sector
expectations of future policy actions to adjust in an appropriate way in response to shocks.
But it does not make sense for the bank to suppose that it can manipulate expectations
through announcements of intentions that bear no relation to what it actually later does.
Instead, making use of this dimension upon which the economy’s responses to shocks may
be improved depends upon the credibility of the central bank’s commitments to behave in
a certain way in the future as a result of the shocks that have occurred earlier. But this
credibility, which ultimately frees the central bank to act more eﬀectively, can be maintained
only if in the short run the bank regards itself as constrained to fulﬁll previous (explicit or
implicit) commitments. And the need to fulﬁll such commitments means that central bank
behavior should not depend solely upon current conditions and the bank’s current forecast
of future conditions – it should depend upon past conditions as well, and speciﬁcally those
past actions by the central bank itself which (under an optimal regime) have given rise to
private sector expectations of a particular kind of monetary policy now.
One reason that this critique of the traditional conception of the central bank’s problem
has not been more widely absorbed may have been the emphasis, in many early expositions,
upon simple policy rules (such as a constant-growth-rate rule for a monetary aggregate) as
the alternative to old-fashioned optimal control. Insofar as central banks have not been
persuaded that judicious responses to economic developments cannot improve economic per-
formance, their research staﬀs have been reluctant to abandon the study of desirable feedback
rules. But, while simple rules have certain practical advantages owing to their transparency,
it is not generally true that the optimal form of central bank commitment, taking into ac-
count the forward-looking character of private-sector behavior, is a rule that involves no
adjustment of the central bank’s instrument in response to current observations. Nor need
the optimal commitment involve any reference to monetary targets; it may quite naturally
be formulated as a feedback rule for a nominal interest-rate operating target, as the analysis
below illustrates.
7

Another reason that the failure of the dynamic-programming principle in the case of the
optimal control of forward-looking systems is not more widely appreciated is probably the
popularity of analyses of optimizing central bank behavior that assume discretionary central
bank behavior, i.e., an inability of the central bank to commit itself to any future actions other
than those that should appear optimal at that time. Under this assumption,12 even when
forward-looking elements are present in one’s model, the central bank chooses its action at
any given date under the assumption that it cannot aﬀect private sector expectations about
its behavior at later dates, owing to its inability to commit itself. Hence its optimization
problem at each date can be cast in a dynamic-programming form, and the resulting solution
makes its action a function only of the economy’s current state.
But even if this model of central bank behavior involves optimization, it does not repre-
sent optimal policy. That is to say, it does not achieve the best possible outcome, in terms
of the central bank’s objective function, among those that could be achieved by an appro-
priate rule for central bank behavior. The celebrated analysis by Barro and Gordon (1983)
of the undesirably high average rate of inﬂation that results under discretion illustrates the
suboptimal nature, in general, of what is eﬀectively a noncooperative equilibrium of a game
played by a succession of policymakers. But while the Barro-Gordon point is widely appre-
ciated, many discussions seem to presume that the problem with discretionary policymaking
is solved once one substitutes an alternative target for the average rate of inﬂation (a central
banker that desires lower inﬂation than is truly optimal) or for the average output gap (a
central banker that does not seek to keep output above the natural rate, even though the nat-
ural rate is ineﬃciently low), or perhaps an alternative weighting of the bank’s stabilization
objectives (a central banker that cares more about inﬂation stabilization than does society).
Instead, there is typically a similar problem with discretionary policymaking in regard to
the optimal response of policy to random shocks, even if one has adjusted the central bank’s
objective so as to make discretion compatible with an optimal steady state in the absence
12Here I have in mind the common practice of considering only the Markov-perfect solution of such a
model. See further discussion in sections 3.2 and 4.1 below.
8

of shocks. Here, too, an optimal commitment on the part of the central bank can often lead
to a better outcome than is attained through optimization under discretion.13
The essential insight into why a commitment to inertial behavior may be optimal for
a central bank is provided by a suggestion of Goodfriend (1991) regarding the reason for
apparent interest-rate “smoothing” by banks like the Fed.14 Goodfriend argues that output
and prices do not respond to daily ﬂuctuations in the (overnight) federal funds rate, but only
variations in longer-term interest rates. The Fed can thus achieve its stabilization goals only
insofar as its actions aﬀect these longer-term rates. But long rates should be determined
by market expectations of future short rates. Hence an eﬀective response by the Fed to
inﬂationary pressures, say, requires it to communicate a credible commitment to a changed
future path of short rates. One straightforward way to do this is to establish a reputation for
maintaining interest rates at a higher level for a period of time once they are raised – or even
for following initial small interest-rate changes by further changes in the same direction,
in the absence of a change in conditions that makes this unnecessary.
Such a policy, if
understood by the private sector, oﬀers the prospect of signiﬁcant eﬀects of central bank
policy upon aggregate demand, without requiring excessively volatile short-term interest
rates, which would be undesirable for the reasons summarized earlier.
There is a certain amount of evidence suggesting that in the U.S. at least, the inertial
character of Fed policy has this beneﬁcial eﬀect. Cook and Hahn (1989), Rudebusch (1995),
and Goodhart (1996) all present evidence showing that changes in Fed operating targets for
the federal funds rate do aﬀect longer-term interest rates, especially at the time of changes
in the direction of movement of the target. Furthermore, Watson (1999) argues that the
increased volatility of long rates since the mid-1980s (relative to an earlier 1960-75 sample
period) can be explained by a greater degree of persistence of funds rate movements in the
later period – a period that has been characterized by greater success at inﬂation stabi-
lization, and, many would argue, an increase in the credibility of the Fed’s commitment to
13Clarida et al. (1999) also discuss this point in the context of a similar model.
14This explanation is also endorsed by Rudebusch (1995).
9

a consistent anti-inﬂationary policy. Indeed, some commentators have proposed that U.S.
monetary policy has been so successful at inﬂation stabilization in the 1990s, despite rel-
atively little change in the funds rate for years at a time, because “the bond market does
the Fed’s work for it,” responding to disturbances in the way needed to keep inﬂation stable
without the need for large policy adjustments by the Fed. This is exactly what a good policy
regime should look like, according to the analysis that I shall oﬀer here – not because the
bond market has any reason to react, of course, if short rates will never be adjusted at all,
but because a credible commitment to an optimal (highly inertial) feedback rule on the part
of the Fed should not require large movements of short-term interest rates in equilibrium,
highly persistent low-amplitude variations being suﬃcient to achieve a desirable degree of
inﬂation stabilization.
This interpretation of the nature of monetary policy inertia has the advantage of resolving
the mystery of why central banks that exhibit a great deal of inertia in their behavior (such as
the Fed) nonetheless have quite good records with respect to inﬂation control – an observation
that is mostly puzzling under the view that inertia is an obstacle to eﬀective central bank
action. Whether one should suppose that these banks have been best able to control inﬂation
because of their better understanding of the advantages of inertial behavior, or whether it is
rather that the advantages of inertial behavior only become important in the case of central
banks that have ﬁrst established a certain degree of credibility as a result of the consistency
of their policy, I shall not here seek to judge. But it makes a great deal of sense that those
central banks that have most clearly learned the beneﬁts of commitment with regard to the
average rate of inﬂation should also be the ones that are also most able to beneﬁt from
a perceived commitment to predictable responses to shocks as well – a commitment that
should manifest itself in inertial behavior. 15
15An alternative explanation, that would also make gradual policy changes optimal, without requiring a
rejection of the dynamic-programming principle, attributes policy inertia to gradual central bank learning
about the eﬀects of its actions (Caplin and Leahy, 1996; Sack, 1998a, 1998b). The reason oﬀered here for
optimal policy to be inertial is quite diﬀerent. In particular, I shall assume a linear-quadratic approximation
to the central bank’s optimization problem, under which optimal policy is certainty-equivalent. This means
that a predictable increase over time in the precision of the central bank’s estimate of the current state
should not be a reason for forecastable changes in its desired instrument setting.
10

The analysis below oﬀers a formal analysis of the beneﬁts of inertial behavior in the
context of a simple, and now rather standard, forward-looking macro model, with clear
foundations in optimizing private sector behavior. The model is too simple to provide the
basis for a realistic quantitative policy analysis; a companion paper (Rotemberg and Wood-
ford, 1998) that addresses this issue in the context of a small econometric model ﬁt to U.S.
time series is perhaps more interesting in that regard. But numerical results in the context
of a speciﬁc quantitative model, of the sort oﬀered in the other paper, inevitably raise many
questions about how sensitive the conclusions may be to a long list of arguable assumptions
that are made along the way. The analytical treatment here of a simpliﬁed version of that
model is intended to help clarify the source of some of those numerical results, and thus to
suggest lessons that may be of more general validity.
The paper is organized as follows. Section 2 presents the model of the economy and
poses the problem of optimal monetary policy.
Section 3 characterizes the responses of
endogenous variables, including nominal interest rates, to shocks under an optimal regime,
and highlights the advantages of commitment, by contrasting the optimal responses with
those that would result from optimization under discretion. It is shown that the optimal
responses involve intrinsic inertia in interest-rate responses, in addition to the persistence
resulting from persistence of the exogenous real disturbances themselves. Section 4 then
considers the optimal assignment of an objective to a central bank with instrument (but
not goal) independence, that is expected to pursue its assigned goal under discretion. It
is shown that in this case, it is desirable for the central bank’s loss function to include
an “interest-rate smoothing” objective, even though the true social loss function does not.
Finally, section 5 considers the form of interest-rate feedback rule that can achieve the desired
dynamic responses to shocks, if the central bank’s commitment to such a rule is credible to
the private sector.
It is shown that such a rule must involve dependence of the current
operating target upon the level of interest rates in the recent past, as is characteristic of
estimated central bank reaction functions.
11

2
The Problem of Optimal Monetary Policy
In order to illustrate more concretely the themes of the preceding discussion, it is useful to
introduce a simple optimizing model of inﬂation and output determination under alterna-
tive monetary policies, where monetary policy is speciﬁed in terms of a feedback rule for
a short-term nominal interest rate instrument. The model is similar, if not identical, to
the small forward-looking models used in a number of recent analyses of monetary policy
rules, including Kerr and King (1996), Woodford (1996), Bernanke and Woodford (1997),
McCallum and Nelson (1997, 1998), Kiley (1998), and Clarida et al. (1999). As is explained
in Woodford (1996), the model’s equations can be derived as log-linear approximations to
the equilibrium conditions of a simple intertemporal general equilibrium model with sticky
prices. While the model is quite simple, it incorporates forward-looking private sector be-
havior in three respects, each of which is surely of considerable importance in reality, and
would therefore also be present in some roughly similar form in any realistic model. It also
shares many features with the econometric model of Rotemberg and Woodford (1997, 1998),
and so analysis of this model can provide insight into the source of some of the numerical
results obtained there.
The model’s two key equations are an intertemporal IS equation of the form
yt −gt = Et[yt+1 −gt+1] −σ−1[rt −Etπt+1],
(2.1)
and an aggregate supply equation of the form
πt = κ[yt −yn
t ] + βEtπt+1,
(2.2)
where yt is the deviation of the log of real output from its trend path, πt is the rate of
inﬂation (ﬁrst diﬀerence of the log of the price level), and rt is the deviation of the short-
term nominal interest rate (the central bank’s policy instrument) from its steady-state value
in the case of zero inﬂation and steady output growth.16
These two equations, together
16Thus all three variables denote percentage deviations from the values of the variables in a steady state
with zero inﬂation and output growth at the constant trend rate.
12

with an interest-rate rule such as (1.1) – (1.2) representing monetary policy, determine the
equilibrium evolution of the three endogenous variables πt, yt, and rt. The two exogenous
disturbances to these structural equations are the processes gt, representing autonomous
variation in spending not motivated by intertemporal substitution in response to real interest-
rate changes, and yn
t , representing time variation in the “natural rate” of output, which
would be the equilibrium level of output under perfectly ﬂexible prices (and is independent
of monetary policy). Finally, on theoretical grounds the structural parameters σ and κ are
both positive.
The system of equations (2.1) – (2.2) implies that no lagged values of any endogenous
variables play any role in the determination of the equilibrium values of inﬂation, output,
or interest rates at a given point in time, unless such dependence is introduced by the
monetary policy rule. On the other hand, they do involve important dynamic linkages from
expectations of the future to the present, as both Etπt+1 and Etyt+1 enter the equations
that determine equilibrium at date t.
The complete exclusion of inertial terms in these
structural equations means that if the “dynamic programming principle” referred to above
were valid, the only source of inertia in the endogenous variables under an optimal policy
would be persistence in the exogenous disturbances (gt and yn
t ). Analysis of such a system
thus makes it especially clear how the presence of forward-looking elements in the structural
equations renders that principle invalid. The model is obviously an extremely simple one,
and in particular, the complete absence of inertial terms in the structural equations is not
entirely realistic. But what is more important for present purposes is the justiﬁcation of the
forward-looking elements, that are critical for the results obtained below.
There is in fact considerable support, both theoretical and empirical, for each of the cru-
cial forward-looking elements in this system. First of all, aggregate demand (intertemporal
substitution) depends upon real as opposed to nominal interest rates, as a result of which
inﬂation expectations enter the IS equation. Second, current aggregate demand depends
not simply upon current expected short-term real rates of return, but also upon expected
future aggregate demand, since (2.1) indicates the incentives for intertemporal substitution
13

of demand created by real interest rate expectations (Kerr and King, 1994). Alternatively,
(2.1) can be integrated forward to yield
yt = gt −σ−1
∞
X
j=0
Et[rt+j −πt+j+1].
(2.3)
Under this way of writing the equation, it states that aggregate demand depends not upon
current short rates alone, but rather upon expected long-term real rates, which in turn
depend upon expected future short rates, as speciﬁed for example by Fuhrer and Moore
(1995). This aspect of the assumed eﬀects of monetary policy upon aggregate demand is
a critical element in the argument of Goodfriend (1991), which we seek to formalize. Here
it might be objected that the expectations theory of the term structure of interest rates
has been subject to considerable empirical criticism. But these criticisms relate mainly to
the hypothesis that long rates are moved only by changes in rational expectations of future
short rates; they do not show that forecastable movements in future short rates do not aﬀect
long rates as the theory would predict. The inclusion of a time-varying “term premium” is
not a problem for the justiﬁcation of an IS relation of the form (2.3), as long as the term
premium is exogenous. For then variations in the term premium are simply another source
of variations in the disturbance term gt.
Finally, because prices are not expected to be continuously changed, they are set on the
basis of expectations of future cost and demand conditions, and not just on the basis of cur-
rent conditions. This results in the expected inﬂation term in (2.2). If one adopts the device
introduced by Calvo (1983) of exogenous stochastic intervals between price changes, together
with monopolistic competition among price-setting suppliers, a log-linear approximation to
the ﬁrst-order condition for optimal price-setting implies that average prices should adjust
at a rate πt that satisﬁes
πt = ωct + βEtπt+1,
(2.4)
where ct represents (percentage deviations in) the average level of real marginal cost of supply,
the coeﬃcient 0 < β < 1 represents the factor with which suppliers discount future real
income17, and the coeﬃcient ω > 0 depends upon the average frequency of price changes and
14

the elasticity of demand faced by suppliers of individual goods. Prices are more nearly ﬂexible
the higher is ω, as a high ω indicates a low tolerance for discrepancies between one’s current
price (or more precisely, marginal revenue, which is proportional to one’s price) and one’s
current nominal marginal cost. If one writes (2.4) as an equation to determine the current
average price level as a weighted average of the past average price level, current average
marginal cost, and the expected future average price level, then as ω is made unboundedly
large, the weights on both past and future prices go to zero. If one adjoins to this a simple
theory of cyclical variation in real marginal cost of the form
ct = η[yt −yn
t ],
(2.5)
then one obtains an aggregate supply relation of the form (2.2). Here the exogenous distur-
bance term yn
t represents the level of output consistent with ct = 0 at each point in time,
and hence the equilibrium level of output in the limiting case of perfect price ﬂexibility.
Empirical support for this sort of forward-looking model of pricing behavior is found,
for example, in Roberts (1995), Sbordone (1998), and Gal´i and Gertler (1998). Sbordone
tests the implications of (2.4) using average unit labor costs as a proxy for the average level
of nominal marginal cost, and shows that the path of inﬂation implied by the evolution
of unit labor costs given (2.4), and using a VAR model to forecast future growth in unit
labor costs, is quite similar to the actual path of U.S. inﬂation. Furthermore, she shows
not only that pricing equation (2.4) ﬁts the data much better than would the hypothesis
of ﬂexible prices, but that the presence of the forward-looking term considerably improves
the ﬁt of the model. Speciﬁcally, nonlinear least-squares estimation of the parameters ω
and β implies that β is signiﬁcantly greater than zero,18 and in fact quite close to one,
in addition to implying a signiﬁcantly positive value for 1/ω. Gal´i and Gertler similarly
estimate the pricing equation (2.4), using a slightly diﬀerent measure of marginal cost and
an instrumental-variables technique, and reach similar conclusions. When they generalize
17This corresponds to the discount factor of the representative household, in a general-equilibrium version
of the model, as in Woodford (1996).
18The case of β = 0, but ω ﬁnite, would correspond to a model in which prices are set proportional to a
weighted average of current and past unit labor costs, with no forward-looking terms.
15

the model to allow for a mixture of forward-looking and backward-looking price-setters, they
estimate a larger fraction of the population to obey the forward-looking pricing equation,
and ﬁnd that the presence of the backward-looking price-setters accounts for relatively little
of aggregate inﬂation dynamics.
Roberts (1995) instead directly estimates the “new-Keynesian Phillips curve” (2.2), using
a variety of proxies for inﬂation expectations and for variations in the natural rate of output.
Most of his results similarly support the existence of a signiﬁcantly positive coeﬃcient on
Etπt+1, and the poorer ﬁt obtained in this case may relate more to the simplicity of the
model of marginal cost (2.5), or to failure to adequately control for variation in yn
t , than to
any problem with the theory of pricing. Roberts (1998) suggests instead that the aggregate
supply relation ﬁts better if the assumption of rational expectations is replaced by a partially
backward-looking model of expected inﬂation. But even here, his preferred speciﬁcations
(partial adjustment of expectations toward the rational forecast) imply important forward-
looking elements in the AS relation of the kind speciﬁed in (2.2).
It is convenient to rewrite the model’s structural equations in terms of the output gap
xt ≡yt −yn
t . Equation (2.2) may then be simply written
πt = κxt + βEtπt+1.
(2.6)
Since we shall assume that we are interested in the output gap rather than detrended output
anyway, in evaluating the success of stabilization policy, it is useful to rewrite the equation
in this way, that eliminates the disturbance term. Equation (2.1) correspondingly becomes
xt = Etxt+1 −σ−1[(rt −rn
t ) −Etπt+1]
(2.7)
where
rn
t ≡σEt[(yn
t+1 −yn
t ) −(gt+1 −gt)].
The exogenous disturbance rn
t corresponds to Wicksell’s “natural rate of interest”, the
interest rate (determined by purely real factors) that would represent the equilibrium real rate
of return under ﬂexible prices, and that corresponds to the nominal interest rate consistent
16

with an equilibrium with constant prices.19 In our simple model, disturbances to the natural
rate represent a useful summary statistic for all non-monetary disturbances that matter for
the determination of inﬂation and the output gap, for no other disturbance term enters either
equation (2.6) or (2.7). Hence if, as we shall suppose, the goals of stabilization policy can be
described in terms of the paths of the inﬂation rate, the output gap, and interest rates alone,
then the problem of optimal monetary policy may be formulated as a problem of the optimal
response to disturbances to the natural rate of interest. It may furthermore be observed that
neither the interest rate controlled by the central bank nor the natural rate enters either of
the structural equations, except through the “interest-rate gap” rt −rn
t . Thus non-monetary
disturbances matter only insofar as the interest rate controlled by the central bank fails to
track the resulting ﬂuctuations in the natural rate; and whether the interest rate set by the
central bank at any point in time should be considered high or low, in the sense that is
relevant for inﬂation determination, depends purely upon where it is relative to the current
natural rate.
I shall assume that the objective of monetary policy is to minimize the expected value of
a loss criterion of the form
W = E0
( ∞
X
t=0
βtLt
)
,
(2.8)
where 0 < β < 1 is a discount factor, and the loss each period is given by
Lt = π2
t + λx(xt −x∗)2 + λr(rt −r∗)2,
(2.9)
for some optimal levels x∗≥0 and r∗of the output gap and the nominal interest rate, and
some weights λx, λr > 0. The assumed form of (2.9) is relatively conventional, except that
an interest-rate variability term is included, for either or both of the reasons discussed in
the introduction. (Note that an interest-rate “smoothing” objective is not assumed!) The
sign of r∗depends upon whether it is desirable to stabilize nominal interest rates around
a value greater or less than the level associated with a steady-state equilibrium with zero
19See Blinder (1998, chap. 2) for a recent discussion of the usefulness of this concept in the theory of
central banking.
17

inﬂation. Insofar as the interest-rate term represents the distortions emphasized by Friedman
(1969), one would expect r∗to be a small negative quantity (since a zero nominal interest rate
corresponds to r∗= log β < 0 in our notation). But insofar as it represents an approximation
to the constraint imposed by the zero bound on nominal interest rates, it may be appropriate
to set r∗> 0, as a higher average value of interest rates reduces the extent to which interest-
rate variability is constrained by the zero ﬂoor.20
The allowance for x∗> 0 reﬂects the fact that the natural rate of output may well be
ineﬃciently low. The explicit general equilibrium model underlying the structural equations
presented here (as presented, for example, in Woodford, 1996) implies that this should be so,
as a result of the small amount of market power that the producers of diﬀerentiated goods are
assumed to have (in order to allow them the power to set prices), if one does not assume an
oﬀsetting output subsidy.21 Finally, I assume that the distortions associated with inﬂation
are minimized in the case of zero inﬂation. Some might prefer to instead see a term of the form
(πt −π∗)2 in (2.9), where π∗is not necessarily zero. This would in fact make little diﬀerence
for our conclusions below.22 But there would seem to be good theoretical grounds to argue
that the distortions associated with price-level instability are minimized when prices never
change (rather than by some other steady inﬂation rate). And some commonly discussed
reasons to prefer a non-zero average inﬂation rate are appropriately modeled by a non-zero
value for r∗, rather than a non-zero π∗; these include both Friedman’s (1969) argument for
mild deﬂation and Summers’ (1991) argument for mild inﬂation, since both arguments really
are about the desirable average level of nominal interest rates.
20The derivation of the interest-rate variation term in the loss function from either of these two concerns
is taken up in Woodford (1999b, sec. 4), which also explains the theoretical values of both λr and r∗.
21The welfare calculations in Rotemberg and Woodford (1997, 1998) are carried out under the assumption
that x∗= 0, in order to focus on the welfare losses associated with price stickiness and imperfect stabilization
of the eﬀects of shocks, in abstraction from other distortions that it is not properly the job of monetary policy
to address. However, whether this is assumed or not has little eﬀect upon our conclusions about the nature of
optimal responses to shocks, as will be seen. It matters much more for the analysis of discretionary monetary
policy, as shown in the next section.
22It would aﬀect the conclusion reached about the steady-state rate of inﬂation that should be implicit
in the optimal policy rule, for obvious reasons, but it would have no eﬀect upon our conclusions about the
desirable responses to shocks, or the desirable type of feedback from endogenous variables to interest rates.
18

Finally, it should be noted that the presence of an (xt −x∗)2 term in (2.9) assumes that
the random ﬂuctuations in the natural rate of output (shifts in the aggregate supply curve)
are all variations in the eﬃcient level of output as well, even if the eﬃcient level of output
may at all times be a certain number of percentage points above the natural rate. This
makes sense if the distortions resulting from delays in price adjustment, on the one hand,
and from a constant level of market power, on the other, are the only reasons why equilibrium
output ever diﬀers from the eﬃcient level. In this case, disturbances to the natural rate of
output due to variations in government purchases, exogenous changes in household tastes,
or random variation in the rate of technical progress, will indeed shift the natural rate and
the eﬃcient level of output in the same proportion (in our log-linear approximation to the
rational expectations equilibrium). But other sorts of distortions might, in principle, result
in time variation of diﬀerent sorts in the two series.23 Such complications would require an
additional term in (2.9).
An important justiﬁcation for the speciﬁc form of objective assumed here is that it
represents a second-order Taylor series approximation to the theoretically correct welfare
measure, the expected utility level of the representative household, in the same optimizing
model as is used to derive the structural equations (2.1) – (2.2).24 Let us suppose that the
ﬂuctuations in the natural rate of interest rn
t around its average value satisfy a uniform bound
that is linear in a parameter ||ξ||, and let us suppose that the coeﬃcients x∗and r∗of the loss
function (2.9), that measure the degree of ineﬃciency of the zero-inﬂation steady state, also
satisfy bounds that are linear in ||ξ||. Then our log-linear approximate structural equations
(2.6) – (2.7) are accurate approximations to the exact, nonlinear equilibrium conditions
implied by the optimizing model in the case that ||ξ|| is made small enough; strictly speaking,
we can show that the distance between the paths of the endogenous variables in the solution
to these approximate structural equations and in the exact equilibrium is of order O(||ξ||2)
23This is the point, for example, of the assumption by Clarida et al. (1999) of a “cost-push” disturbance
term in (2.2) that is not netted out in their deﬁnition of the “output gap” that policymakers are assumed
to wish to stabilize.
24See Woodford (1999b) for details of the derivation.
19

or smaller.25 The welfare measure (2.8) with period loss function
˜Lt = π2
t + λx(xt −x∗)2
(2.10)
represents a quadratic approximation to the exact theoretical welfare measure (expected
utility) in the same sense; the diﬀerence between W and the exact level of expected utility26
is of order O(||ξ||3).
Such a quadratic approximation is appropriate, not only to facilitate comparison between
our results and those elsewhere in the literature, but because this is in any event the highest-
order approximation to utility that can be computed using only our log-linear approximate
characterization of the equilibrium resulting from a given policy rule.27
Furthermore, a
quadratic approximation to the theoretically correct objective suﬃces to allow us to obtain
a log-linear approximation to the optimal responses to shocks, by ﬁnding the policy that
minimizes our approximate loss criterion subject to the log-linear constraints imposed by
our approximate structural equations.28 Since studies that characterize optimal policy on
the basis of the exact utility functions and ﬁrst-order conditions (such as King and Wol-
man, 1998) frequently use log-linear approximations to characterize the optimal responses
to shocks in any event, this order of accuracy is as much as we really need.
The ﬁnal term in (2.9) can be justiﬁed either as representing further distortions associated
with high nominal interest rates (for example, ineﬃcient substitution between “cash” and
“credit” goods, as in Yun, 1996), or as a quadratic approximation to the penalty on interest-
25This result assumes the existence of a determinate equilibrium associated with the policy rule under
consideration, in the sense discussed in section 4.1 below, and that that unique bounded solution is the one
under discussion.
26Here we have omitted from W constant terms that are independent of the evolution of the endogenous
variables, and have chosen units for the measurement of W in which the period loss associated with steady
inﬂation of one percent per year is equal to a ﬂow loss of one per time period.
27Even a second-order approximation to utility can be computed only because of our assumption that
the parameters x∗and r∗are of order O(||ξ||). This means that only contributions of order O(||ξ||) to the
average levels of the endogenous variables matter for the terms of second order or larger in W. Otherwise,
second-order contributions to the average level of variables such as xt would matter, and these could not be
computed without a higher-order approximation to our model structural equations.
28The ﬁrst-order conditions obtained in section 3.1 below diﬀer from the exact ones by terms that are
only of order O(||ξ||2). This depends upon the fact that the steady-state values of the Lagrange multipliers
associated with the constraints imposed by the structural equations are only of order O(||ξ||).
20

rate variability implied by the zero bound on nominal rates. We shall emphasize the latter
interpretation here.
Rotemberg and Woodford (1997, 1998) propose to approximate the
eﬀects of the zero bound by imposing instead a requirement that the mean federal funds
rate be at least k = 2.26 standard deviations above zero.29
The alternative constraint,
while inexact, has the advantage that checking it requires only computation of ﬁrst and
second moments under alternative policy regimes; and, given linear structural equations and
a quadratic loss function, the optimal policy is linear. But a constraint of this form can
equivalently be expressed as a requirement that the average value of r2
t be not more than
K ≡1+k−2 = 1.44 times the square of the average value of rt. If we use discounted averages,
for conformity with the other terms in our welfare measure, we obtain a constraint of the
form
E0
"
(1 −β)
∞
X
t=0
βtr2
t
#
≤KE0
"
(1 −β)
∞
X
t=0
βtrt
#2
.
(2.11)
And using the usual Kuhn-Tucker arguments, the policy that minimizes the expected dis-
counted value of (2.10) subject to (2.11) can be shown to also minimize an (unconstrained)
loss criterion of the form
E0
"
(1 −β)
∞
X
t=0
βt ˜Lt
#
−µ1E0
"
(1 −β)
∞
X
t=0
βtr2
t
#
+ µ2E0
"
(1 −β)
∞
X
t=0
βtrt
#
,
where µ1 and µ2 are appropriately chosen Lagrange multipliers. Finally, the terms in this
expression can be rearranged to yield a discounted loss criterion of the form (2.8) – (2.9),
where λr ≡µ1 and r∗≡µ2/2µ1.30 When constraint (2.11) binds, the Lagrange multipli-
ers have values µ1, µ2 > 0, so that λr, r∗> 0. We adopt this interpretation below, when
“calibrating” the parameters of the loss function.
An advantage of deriving the loss function from welfare-economic foundations in this way
is that it not only provides justiﬁcation for the general form of our welfare criterion, but for
a speciﬁc quantitative speciﬁcation. The theoretical derivation implies, for example, that
29This numerical value is the one satisﬁed by the stationary distribution for the federal funds rate implied
by their estimated VAR using U.S. data.
30There is also a constant term involved in completing the square, that has no eﬀect upon our ranking of
alternative policies.
21

the discount factor in (2.8) should be the same as the coeﬃcient on expected inﬂation in
the structural equation (2.2), as both are equal to the discount factor of the representative
household in the underlying optimizing model. It similarly implies that π∗should equal
zero in (2.9), as I have assumed in writing the equation, and implies theoretical values
for coeﬃcients such as λx and x∗in the terms of the same underlying model parameters
(mainly preference parameters of the representative household) as determine the values of
the coeﬃcients σ and κ of the structural equations. These theoretical relations are used in the
illustrative numerical calculations reported below. However, the algebraic characterizations
of optimal policy apply for arbitrary values of the parameters of the period loss function
(2.9), so our qualitative conclusions do not depend upon this particular view of the proper
objectives of monetary policy, but only upon a loss function of the (rather conventional)
general form (2.8) – (2.9).
3
Optimal Responses to Fluctuations in the Natural
Rate of Interest
I turn now to the characterization of optimal monetary policy in the context of the model just
set out. In the present section, I shall be concerned solely with the question of what pattern
of ﬂuctuations in the endogenous variables, inﬂation, output and interest rates, would be
associated with the optimal equilibrium, by which I mean the equilibrium that achieves the
lowest possible value of the loss measure (2.8). I shall set aside until the next section the
question of what kind of policy rule should bring about such an equilibrium, were it to be
properly understood by the private sector. Since the only random disturbances that matter
for this optimization problem are the variations in the natural rate of interest rn
t , the problem
of this section can be alternatively posed as the question of how it is optimal for inﬂation, the
output gap, and nominal interest rates to respond to exogenous ﬂuctuations in the natural
rate.
Formally, our problem is to choose stochastic processes πt, xt, and rt — specifying each
of these variables as a function of a random state It that includes not only the complete
22

history of the exogenous disturbances (rn
t , rn
t−1, . . . , rn
0), but also all public information at
date t about the future evolution of the natural rate31— in order to minimize the criterion
deﬁned by (2.8) and (2.9), subject to the constraint that the processes satisfy equilibrium
conditions (2.6) and (2.7) at all dates t ≥0. We imagine that a policymaker can choose the
entire future (state-contingent) evolutions of these variables, once and for all, at date zero.
Thus we wish to consider optimal policy under commitment on the part of the policymaker
– even though we have not yet speciﬁed the type of explicit commitment, as to the way
in which policy will be conducted, that is involved. Note that the assumed possibility of
commitment matters, in the case of an optimization problem of this kind. For, because of
the forward-looking terms in our structural equations (2.6) and (2.7), the value of the period
loss Lt that can be achieved at a given time depends upon what the private sector expects
about the subsequent evolution of the endogenous variables. Commitments about how policy
will be used to aﬀect those variables at later dates, that need not coincide with what would
optimally be chosen at the later dates in the absence of an advance commitment, will thus
be a typical feature of an optimal plan.
3.1
First-Order Conditions for the Optimal Plan
This sort of linear-quadratic optimization problem can be treated using methods that are
by now familiar.32 It is useful to write a Lagrangian of the form33
E0
( ∞
X
t=0
βt{Lt + 2φ1t[xt −xt+1 + σ−1(rt −rn
t −πt+1)] + 2φ2t[πt −κxt −βπt+1]}
)
.
(3.1)
31We may at this point also allow It to include other information, including irrelevant “sunspot” variables,
but we shall ﬁnd that it is not optimal for the endogenous variables to respond to any such additional
information.
32See, e.g., Backus and Driﬃll (1986) for treatment of a general linear-quadratic problem. Early applica-
tions of the Lagrangean method used here include Kydland and Prescott (1980), Hansen, Epple and Roberds
(1985), and Sargent (1987, chap. XV). Methods of this kind are applied extensively to problems of optimal
monetary policy by Currie and Levine (1993).
33Here the Lagrange multipliers are multiplied by two to eliminate a recurrent factor of two from the
resulting ﬁrst-order conditions; the same result is often instead achieved by deﬁning the loss function Lt
to equal one-half of (2.9). Note also that conditional expectations are dropped from the way in which the
constraints are written inside the square brackets, because the expectation E0 at the front of the entire
expression makes them redundant.
23

An optimal plan then must satisfy the ﬁrst-order conditions
πt −(βσ)−1φ1t−1 + φ2t −φ2t−1 = 0,
(3.2)
λx(xt −x∗) + φ1t −β−1φ1t−1 −κφ2t = 0,
(3.3)
λr(rt −r∗) + σ−1φ1t = 0,
(3.4)
obtained by diﬀerentiating the Lagrangian with respect to πt, xt, and rt respectively. Each
of conditions (3.2) – (3.4) must hold at each date t ≥1, and the same conditions also must
hold at date t = 0, where however one adds the stipulation that
φ1−1 = φ2−1 = 0.
(3.5)
We may omit consideration of the transversality conditions, as we shall consider only bounded
solutions to these equations, which necessarily satisfy the transversality conditions.34
A
(bounded) optimal plan is then a set of bounded processes {πt, xt, rt, φ1t, φ2t} for dates t ≥0,
that satisfy (2.6), (2.7), and (3.2) – (3.4) at all of these dates, consistent with the initial
conditions (3.5).
It is obvious that such an optimal plan will, in general, not be time consistent, in the sense
discussed by Kydland and Prescott (1977). For a policymaker that solves a corresponding
problem at some date T > 0 will choose processes for dates t ≥T that satisfy the stochastic
diﬀerence equations just listed, and initial conditions
φ1T−1 = φ2T−1 = 0
corresponding to (3.5). But these last conditions will, in general, not be satisﬁed by the
optimal plan (with commitment) chosen at date zero. This can be shown as follows. The
optimal plan is time consistent only if φit = 0 for i = 1, 2 and for all t ≥0. Substituting these
values into (3.2) – (3.4), we see that this requires that the optimal plan involve πt = 0, xt =
34Here it is important to recall that we are not solving an exact linear-quadratic problem, which might have
an unbounded solution. Our Taylor series methods imply that the solution to the linear-quadratic problem
taken up here should approximate the solution to the exact nonlinear welfare maximization problem only in
the case that solution involves ﬂuctuations in the state variables that are uniformly small.
24

x∗, rt = r∗at all times. But substitution of these values into (2.6) and (2.7) shows that this
cannot represent an equilibrium, unless x∗= 0, and rn
t = r∗at all times. Thus the optimal
plan is time consistent only if the problem satisﬁes both of those properties. The failure of
time consistency in the case that x∗̸= 0 (i.e., the natural rate of output is ineﬃcient, and so
not the level that a benevolent policymaker would prefer to achieve) occurs essentially for
the same reason as in the celebrated analysis of Barro and Gordon (1983). However, even
if we assume that x∗= 0,35 the optimal plan is still generally not time consistent, for time
consistency would also require that there be no variation in the natural rate of interest.36
Even in the absence of any desire to make the level of output higher than the natural rate
on average, and hence of a systematic inﬂation bias, a more desirable pattern of responses to
shocks is available under commitment. This is why credibility is valuable to a central bank,
and the commitment to a policy rule desirable, even in the absence of such bias.
3.2
Comparison with the Result of Optimization without Com-
mitment
It may be useful to compare the optimal (commitment) plan to the time-consistent plan
that results from optimization under discretion, i.e., optimization by a central bank that
expects itself to re-optimize at each successive date, and is unable to commit itself to do
anything at future dates other than choose a policy that is expected to minimize (2.8) given
the expected behavior of its successors. By this latter plan I shall mean the Markov-perfect
equilibrium of the game played by the succession of central bankers, or what is sometimes
called the “non-reputational” solution to the central bank’s problem (e.g., Currie and Levine,
1993). Under the time-consistent plan, πt, xt and rt are chosen at any given date t, subject
35This might be either because the discretionary policymaker seeks to minimize a version of (2.9) in which
x∗= 0 despite the ineﬃciency of the natural rate (as assumed in Clarida et al., 1999), or because the natural
rate is actually assumed to be eﬃcient (as in the welfare calculations of Rotemberg and Woodford, 1998).
36Actually, this condition is required only because we have assumed that λr > 0. If x∗= 0 and λr = 0,
then the optimal plan is time-consistent, and is given by πt = 0, xt = 0, rt = rn
t at all times. Thus our
arguments for the desirability of low interest-rate volatility are crucial to the argument given here for the
desirability of an inertial, non-time-consistent policy. But similar conclusions could be reached even when
λr = 0, if we assume some other reason for the ﬁrst-best level of welfare not to be attainable, such as the
“cost-push shocks” assumed in Clarida et al. (1999).
25

to the constraints (2.6) and (2.7), so as to minimize Lt, given the exogenous state rn
t , and
taking as given the way that the endogenous variables will be chosen (as a function of the
economy’s exogenous state IT) at all dates T > t. The evolution of the endogenous variables
at later dates is not assumed to depend upon the choices at date t, because the equilibrium
conditions (2.6) and (2.7), that will constrain the later choices, do not involve any lagged
endogenous variables, and neither does the period objective function (2.9). The ﬁrst-order
conditions for this optimization problem at each date are given by
πt + φ2t = 0,
(3.6)
λx(xt −x∗) + φ1t −κφ2t = 0,
(3.7)
λr(rt −r∗) + σ−1φ1t = 0,
(3.8)
instead of (3.2) – (3.4). A Markov-perfect solution is a set of processes {πt, xt, rt, φ1t, φ2t}
that satisfy (2.6), (2.7), and (3.6) – (3.8) at all dates, with the property that each of the
endogenous variables just listed depends at date t only upon the part of It that is relevant
for forecasting current and future values of the exogenous disturbance rn
t+j. Note that the
absence of the lagged Lagrange multiplier terms from these conditions in every period, and
not just at date zero, means that there is no problem of time consistency in this case.
The steady-state values of the various variables under the time-consistent plan – i.e., the
values they would take in the case that one expected rn
t = 0 forever – may be obtained by
substituting constant values for each variable into the equilibrium conditions and solving.
The steady-state values of the endogenous variables are given by
rtc = πtc =
λxx∗−σλrr∗
κ + λx(1 −β)κ−1 −λrσ,
xtc =
λxx∗−σλrr∗
λx + (1 −β)−1κ[κ −λrσ].
(3.9)
As is discussed further in the next subsection, these values typically imply a steady-state
inﬂation rate higher than the one that would minimize the steady-state value of the period
loss L.
In determining the equilibrium responses to shocks, it is convenient to work in terms of
deviations from steady-state values. Thus we deﬁne ˆπt ≡πt −πtc, and so on. The hatted
26

variables satisfy the same set of diﬀerence equations as before, except that we may now
drop the constant terms from equations (3.7) – (3.8). If we substitute out the Lagrange
multipliers, equations (3.6) – (3.8) imply an equilibrium relation of the form
ˆrt =
κ
λrσ ˆπt + λx
λrσ ˆxt
(3.10)
among the endogenous variables. Using this to substitute out rt in (2.7), we are left with
two stochastic diﬀerence equations in the endogenous variables zt ≡[ˆπt ˆxt]′. These may be
written in the matrix form
Etzt+1 = Azt + arn
t ,
(3.11)
where A is a 2 × 2 matrix of coeﬃcients, and a ≡[0 −σ−1]′.
Now let the relevant information at date t about the future evolution of the natural rate
be summarized by an exogenous state vector st, with law of motion
st+1 = Tst + ϵt+1,
(3.12)
where ϵt+1 is a vector of exogenous disturbances unforecastable at t, and where the natural
rate itself is given by some linear function of these states,
rn
t = k′st.
(3.13)
Then we seek a solution to (3.11) of the form zt = Fst. It follows from (3.11) and (3.12) that
the matrix F must satisfy
FT −AF = ak′.
(3.14)
This is a set of 2n linear equations (where n is the number of elements in st) to determine
the 2n coeﬃcients F, and so except in singular cases, a solution exists and is unique.
An instructive simple case is that in which the natural rate follows a ﬁrst-order autore-
gressive process,
rn
t+1 = ρrn
t + ϵt+1,
(3.15)
27

in which case the state vector st consists simply of rn
t itself.
(We shall throughout the
following discussion always assume that 0 ≤ρ < 1.) In this case, there exists a time-
consistent plan as long as ρ is not an eigenvalue of the matrix A, and it is given by
F = −[A −ρI]−1a.
In this solution, the endogenous variables are functions simply of the current value of the
natural rate of interest,
ˆπt = fπrn
t ,
ˆxt = fxrn
t ,
ˆrt = frrn
t .
(3.16)
In the case that
ρ
(1 −ρ)(1 −βρ) < σ
κ,
i.e., as long as the ﬂuctuations in the natural rate are not too persistent, one can show that
these coeﬃcients furthermore satisfy
fπ, fx > 0,
0 < fr < 1,
regardless of the size of λx and λr.
This means that interest rates adjust in the direction of the disturbance to the natural
rate, but by less than the full amount of the change in the natural rate, owing to the desire to
reduce interest-rate variability. (In the limiting case with λr = 0, one ﬁnds that fr = 1, and
fπ = fx = 0.) As a result of the incomplete adjustment of nominal interest rates, an increase
in the natural rate stimulates aggregate demand, with the result that both inﬂation and the
output gap increase. Note that in this solution, the only source of persistence in interest-
rate ﬂuctuations is the persistence (if any) of the exogenous ﬂuctuations in the natural rate.
(Nominal interest rates would be observed to follow a ﬁrst-order autoregressive process,
with autocorrelation coeﬃcient ρ.) Thus if central bank policy is optimizing in this time-
consistent sense, the conventional view described in the introduction is correct – optimizing
policy does not involve any inertia in nominal interest rates other than what results from
the persistence of the underlying economic conditions in response to which interest rates are
properly adjusted.
28

If one assumes a non-Markovian natural rate process, so that there are additional states
in the vector st besides the current natural rate itself, that are relevant for forecasting the
future level of the natural rate, then in general the time-consistent solution for rt will also
depend upon these states. For example, in the case that the matrix A has both eigenvalues
outside the unit circle, the unique bounded solution to (3.11) is obtained by “solving forward”
to yield
zt = −
∞
X
j=0
A−(j+1)aEtrn
t+j.
(3.17)
(Such a solution necessarily exists, and is bounded, as long as the natural rate process itself
is bounded.) This expression oﬀers an alternative representation of the time-consistent plan
(3.14). Substitution of (3.17) into (3.10) then allows a similar expression
ˆrt = −q′
∞
X
j=0
A−(j+1)aEtrn
t+j,
(3.18)
where q′ is the row vector of coeﬃcients in (3.10), to be derived for the evolution of the
nominal interest rate under the time-consistent plan. Expressions (3.17) and (3.18) show
clearly that such policy should in general be “forward-looking”, and not simply a function
of current conditions alone.37 At the same time, there is no reason for the central bank’s
setting of the nominal interest rate to depend either upon past levels of the natural rate
(except insofar as these may be variables that help to forecast future levels of the natural
rate) or upon past levels of the nominal interest rate itself.
But while this equilibrium could be explained as the result of optimization (by a central
bank that is unable to commit itself), it does not represent optimal policy – for it does not
achieve the lowest expected value of the central bank objective function (2.8) consistent with
37Note, however, that even this representation of optimizing policy gives one no reason to suppose that
policy needs to be based upon forecasts of goal variables, such as inﬂation forecasts, as opposed to forecasts
of future exogenous disturbances. Note also that the mere fact that one wanted the endogenous variables
to respond to information about the future level of the natural rate in the way indicated by (3.17) would
not necessarily require explicit response to forecasts by the central bank; it could be achieved as a rational
expectations equilibrium response, owing to forward-looking behavior on the part of the private sector, even
if the central bank’s policy rule responds only to current endogenous variables. See the discussion in the
next section.
29

the constraints imposed by the requirements for a rational expectations equilibrium. That
optimal plan is instead described by the ﬁrst-order conditions (3.2) – (3.4) derived earlier.
3.3
Comparison with the Optimal Non-Inertial Plan
The optimal plan (which requires commitment) is almost invariably diﬀerent from the time-
consistent optimizing plan just characterized, and as we shall see, one respect in which it is
diﬀerent is that it generally involves persistence in the responses of the endogenous variables
to shocks that are not due to the persistence of the ﬂuctuations in the natural rate of interest.
However, one might ask to what extent the optimal policy is better because it allows for a
commitment to inertial behavior, as opposed to being better simply because it allows for
commitment. For even among the category of plans under which the endogenous variables
are functions only of the state vector st (in accordance with the dynamic programming
principle), commitment generally makes possible a better outcome than that obtained under
discretion, as discussed by Clarida et al. (1999). Hence it may be worth brief consideration
of the optimal non-inertial plan.38
We shall proceed directly to the case in which the natural rate evolves according to
(3.15). In this case, non-inertial plans are those in which each endogenous variable yt is a
time-invariant linear function of the current natural rate of interest,
yt = ys + fyrn
t ,
(3.19)
where ys is the steady-state value of the variable under the optimal “simple” rule, and fy
indicates its response to ﬂuctuations in the natural rate, as in (3.16).
Substituting the
representation (3.19) for each of the variables y = π, x, r into (2.6) – (2.7), we ﬁnd that
feasible non-inertial plans correspond to coeﬃcients ys, fy that satisfy
(1 −β)πs = κxs,
(3.20)
38This is closely related to the question of the optimal “simple” policy rule, considered by Levine (1991).
However, there the nature of optimal feedback to the instrument from endogenous variables is considered,
whereas we defer this question to section 4.2 below. Furthermore, there the choice of the optimal “simple”
rule is allowed to depend upon the state of the economy in the initial period.
30

rs = πs,
(3.21)
(1 −βρ)fπ = κfx,
(3.22)
(1 −ρ)fx = −σ−1(fr −1 −ρfπ).
(3.23)
Among these plans, we seek the one that minimizes E[W], the unconditional expectation
of (2.8), taking the unconditional expectation over the stationary distribution of possible
initial exogenous states rn
0. We take this unconditional expectation so that our choice of the
optimal plan does not depend upon the state that the economy happens to be in at the time
that the commitment is made.39
Given our restriction to non-inertial plans, minimization of E[W] is equivalent to min-
imization of E[L], the unconditional expectation of the period loss (2.9). Thus we seek to
minimize
E[L] = [πs2 + λx(xs −x∗)2 + λr(rs −r∗)2] + [f 2
π + λxf 2
x + λrf 2
r ]var(rn),
(3.24)
subject to the linear constraints (3.20) – (3.23). Note that the ﬁrst term in square brackets
in (3.24) involves only the steady-state values ys, while the second term involves only the
response coeﬃcients fy; similarly, constraints (3.20) – (3.21) involve only the former coef-
ﬁcients, while constraints (3.22) – (3.23) involve only the latter. Thus separate problems
deﬁne the optimal values of each of the two sets of coeﬃcients.
The optimal non-inertial plan is easily seen to involve a steady state in which
rs = πs = (1 −β)κ−1λxx∗+ λrr∗
1 + [(1 −β)κ−1]2λx + λr
,
39If instead we were to minimize W, conditioning upon the state of the economy at the time of choice as
in Levine (1991), the exact non-inertial plan that would be chosen would in general depend upon that state.
This is because the choice of how the variables should depend upon rn would be distorted by the desire to
obtain an initial (unexpected) inﬂation, without creating expectations of a similar rate of inﬂation on average
in the future; this could be done by exploiting the fact that rn
0 is known to have a value diﬀerent from its
expected value in the future (which is near zero eventually). By instead deﬁning the optimal non-inertial
policy as we do, we obtain a unique policy of this kind, and associated unique values for statistics such as
the variability of inﬂation under this policy. Also, under our deﬁnition, unlike Levine’s, the optimal “simple”
plan is certainty-equivalent, just like the fully optimal plan and the time-consistent optimizing plan. That
is, the optimal steady-state values ys are the same as for a certainty problem, while the optimal response
coeﬃcients fy are independent of the variance of the disturbance process.
31

with xs then given by (3.20). We observe that in the case that λr and/or r∗are small enough,
the steady-state inﬂation rate satisﬁes
0 < πs < πtc.
It is slightly positive, as in the calculation of King and Wolman (1996), because (2.6) implies
a slightly upward-sloping long-run Phillips curve;40 but it is smaller than in the discretion
equilibrium, because (given β near one) the long-run Phillips curve is much steeper than the
short-run trade-oﬀ. This indicates that discretionary optimization gives rise to an “inﬂation
bias”, as in the analysis of Barro and Gordon (1983).41
Turning to the optimal non-inertial responses to disturbance, the ﬁrst-order conditions
for optimal choice of the fy imply that
fr =
κ(1 −βρ)−1fπ + λxfx
[(1 −ρ)σ −ρκ(1 −βρ)−1]λr
.
(3.25)
This condition along with (3.22) – (3.23) determines the optimal response coeﬃcients. Note
that (3.25) reduces to (3.10) in the case that ρ = 0, so that the optimal non-inertial policy
coincides with the time-consistent policy in this case. However, in general the two solutions
do not coincide, and for large ρ they can be quite diﬀerent (for example, response coeﬃcients
may have opposite signs in the two cases).
40This is described by (3.20). The eﬀect is quite small, not only because β is plausibly near one, making
the long-run Phillips curve steep, but because λx is small in a plausible utility-based welfare criterion. The
Calvo (1983) model of price-setting is criticized on this ground by McCallum and Nelson (1998), who feel
that a plausible model ought to satisfy Friedman’s (1968) “natural rate hypothesis”.
The natural rate
property is restored in Yun’s (1996) version of the model, that assumes that prices increase at a constant
rate between the occasions upon which they are re-calculated, where the constant rate corresponds to the
economy’s long-run average rate of inﬂation. It is interesting to note, however, that even if one feels that
the violation of the natural rate hypothesis is reasonable, this provides no ground for preferring a positive
average rate of inﬂation. For, as is shown in the next section, the fully optimal policy implies a steady-state
inﬂation rate that is independent of x∗.
41Note that in the present model, a mere demonstration that πtc > 0 does not necessarily imply an
inﬂation bias in this sense, both because positive steady-state inﬂation raises the steady-state output gap in
this model, unlike that of Barro and Gordon, and because we allow for the possibility that r∗> 0, which
also implies advantages to a positive average inﬂation rate.
32

3.4
Interest-Rate Inertia under the Optimal Plan
The optimal plan corresponds to a bounded solution of the system of diﬀerence equations
(2.6), (2.7), and (3.2) – (3.4), consistent with the initial conditions (3.5). We begin, as
above, by computing the steady-state values of the endogenous variables implied by these
equations, by which we mean the constant values that would satisfy the diﬀerence equations
in all periods (setting aside for the moment the issue of the initial conditions). These steady-
state values are given by
ropt = πopt =
λr
λr + β r∗,
xopt = 1 −β
κ
λr
λr + βr∗,
(3.26)
and the associated steady-state Lagrange multipliers by42
φopt
1
= βσλr
λr + β r∗,
φopt
2
= 1 −β
κ
 λx
κ −σ
!
λr
λr + β r∗−λx
κ x∗.
Note that the optimal steady-state inﬂation rate is independent of x∗; this means that as
long as r∗= 0, i.e., the optimal nominal interest rate is the one consistent with zero steady-
state inﬂation, the optimal steady-state inﬂation rate is zero, even when the associated
steady-state output level (the natural rate of output) is ineﬃcient. This is true even though
a policymaker optimizing in the absence of commitment would wish to choose a positive
level of inﬂation (assuming x∗> 0 and λr not too large) in order to increase output to a
more nearly eﬃcient level; and it is true even though, in the present model (unlike that of
Barro and Gordon, 1983), there is a long-run Phillips curve trade-oﬀ. We obtain the same
conclusion if λr = 0, and in this case our results agree with those of King and Wolman (1998)
for a closely related model with overlapping two-period price commitments. If λr > 0 and
r∗̸= 0, then πopt ̸= 0 as well; but this is because of the desirability of a non-zero inﬂation
42Note that these values are linear in x∗and r∗. Thus, as asserted in the previous section, if the values
x∗and r∗that measure the ineﬃciency of the zero-inﬂation steady state are only of order O(||ξ||), then the
steady-state values of the Lagrange multipliers are only of order O(||ξ||) as well. It then follows that in a
Taylor series expansion of the exact ﬁrst-order conditions to characterize the optimal plan, terms of order
O(||ξ||2) in the structural equations of the model, which contribute terms of order O(||ξ||) to the partial
derivatives of the constraints with respect to the endogenous variables, contribute terms that are only of
order O(||ξ||2) to the ﬁrst-order conditions. Hence equations (3.2) – (3.4) represent a ﬁrst-order Taylor series
approximation to the exact conditions, and their solution represents a similar log-linear approximation to
the exact optimal plan.
33

rate in order to allow the nominal interest rate to be nearer its optimal level (say, to reduce
the transactions costs associated with economizing on money holdings), and not because of
any optimal exploitation of the long-run Phillips curve tradeoﬀ. The contrast between this
result and (3.9) indicates the desirability of a central bank’s being able to commit itself to
a policy that maintains zero average inﬂation (or at any rate, an average inﬂation rate that
diﬀers from zero only because r∗̸= 0), rather than simply acting in the public interest on a
period-by-period basis.
One may wonder, of course, about the signiﬁcance of this “steady-state” solution, given
that the equations describing the optimal plan do not generally admit a solution that is
constant over time, even when rn
t is expected to equal zero at all dates. (This is because the
steady-state values of the multipliers are generally inconsistent with the initial conditions
(3.5). Only if both x∗= 0 and r∗= 0 do we obtain φopt
i
= 0 for both i = 1, 2.) However,
in the case of interest to us here – the case in which a bounded optimal plan exists – the
optimal plan involves values of the endogenous variables that converge asymptotically to
the steady-state values, as discussed below. Hence commitment to an optimal plan, in the
case that r∗= 0, means commitment to a rate of inﬂation that will eventually be zero on
average.43 A central bank that wished to behave as if it had committed itself to an optimal
plan at a date far in the past (as a way of forswearing the temptation to exploit the gains
from an unanticipated change in policy) therefore chooses a policy that resulted in zero
average inﬂation, as well.
We turn now to the question of the optimal response to shocks. It will again simplify our
equations if we rewrite them in terms of deviations from the steady-state values, deﬁning
ˆπt ≡πt −πopt, and so on. The same system of ﬁve equations then applies to the hatted
variables, except that all constant terms are eliminated from the equations. Using (3.4) to
eliminate ˆrt from (2.7), we are ﬁnally left with a system of four stochastic diﬀerence equations
in the four endogenous variables ˆπt, ˆxt, ˆφ1t, and ˆφ2t. The system can be written in vector
43In the case that λr = 0, the optimal inﬂation rate is eventually zero in all states, as is argued by King
and Wolman (1998). But that is not true here, if we allow a concern for reduction of the variability of
interest rates.
34

form as
"
Etzt+1
φt
#
=
"
A
B
C
D
# "
zt
φt−1
#
+
"
a
0
#
rn
t ,
(3.27)
where φt ≡[ˆφ1t ˆφ2t]′ is the vector of deviations of the values of the Lagrange multipliers, A
and a are the same matrix and column vector as in (3.11) above, and B, C, and D are other
2×2 matrices of coeﬃcients. Here the bottom two equations are equations (3.3) and (3.2), in
that order, expressed as laws of motion for the Lagrange multipliers. The top two equations
are again (2.6) and (2.7), in that order, expressed as expectational diﬀerence equations for
inﬂation and the output gap. The ﬁrst equation is substituted into the second to eliminate
Etˆπt+1, and the third equation is similarly substituted into it to eliminate ˆφ1t. The non-zero
elements of B (which occur only in the second row) result from this last substitution.
Given a bounded stochastic process for the exogenous disturbance rn
t , one can show using
the methods of Blanchard and Kahn (1980) that the system (3.27) has a unique bounded
solution if and only if the matrix
M ≡
"
A
B
C
D
#
has exactly two eigenvalues outside the unit circle, and two that are inside.44 (This is because
the state vector contains exactly two predetermined variables, the two elements of φt−1.) One
can show that the matrix M necessarily has two eigenvalues with modulus greater than β−1/2
and two with modulus smaller than this. This means that there are necessarily at least two
eigenvalues outside the unit circle, and so there is at most a single bounded solution. (This
is as we should expect, since any bounded solution would have to correspond to an optimal
plan.) The conditions required for there to be only two eigenvalues outside the unit circle,
so that a bounded solution does exist, seem likely to be satisﬁed for reasonable parameter
values,45 and since our Taylor series approximation methods can only validly be employed
in this case, we assume that they are satisﬁed.
44Here we neglect to discuss certain non-generic cases that can occur only for special parameter values.
45For example, they are satisﬁed by the “calibrated” parameter values used for the numerical computations
below.
35

In this case, the unique bounded solution can be written in the form
zt = Gφt−1 −
∞
X
j=0
˜A−(j+1)aEtrn
t+j,
(3.28)
where G and ˜A are 2 ×2 matrices. Furthermore, the eigenvalues of the matrix ˜A are exactly
the two eigenvalues of M that lie outside the unit circle, so that the inﬁnite sum converges
in the case of any bounded process for the natural rate. Substituting this solution for zt into
the last two equations of (3.27), we obtain a law of motion for the Lagrange multipliers of
the form
φt = Nφt−1 −C
∞
X
j=0
˜A−(j+1)aEtrn
t+j,
(3.29)
where N ≡CG+D is a 2×2 matrix the eigenvalues of which are exactly the two eigenvalues
of M that lie inside the unit circle. This last property of the matrix N implies that (3.29)
deﬁnes a bounded stochastic process for the multipliers φt, given any bounded process for the
natural rate. Then (3.29) describes the evolution of the multipliers, given the initial condition
(3.5) and an exogenous process for the natural rate, while (3.28) describes the evolution of
the endogenous variables zt, given the evolution of the multipliers and an exogenous process
for the natural rate. Given this evolution of the variables zt and φt, the implied evolution of
the central bank’s instrument rt is easily derived, and can also be written in the form
ˆrt = p′φt−1 −q′
∞
X
j=0
˜A−(j+1)aEtrn
t+j.
(3.30)
where q′ is the same vector of coeﬃcients as in (3.18), and p′ is another vector of two
coeﬃcients.46
Note that the second term on the right-hand side of (3.28) is of a similar form as (3.17),
and likewise for the second term on the right-hand side of (3.30) and (3.18). (The only
diﬀerence in these terms is the replacement of the matrix A by ˜A.) The crucial qualitative
diﬀerence is the presence of the φt−1 terms as well in the case of the optimal plan. These terms
imply that the endogenous variables at date t – and in particular, the central bank’s setting
46It is easily seen from (3.4) that p′ must equal −(λrσ)−1 times the ﬁrst row of the matrix N. In fact, q′
is the same multiple of the ﬁrst row of C.
36

of the interest rate at that date – should not depend solely upon current and forecasted future
values of the natural rate of interest. They should also depend upon the predetermined state
variables φt−1, which represent an additional source of inertia in optimal monetary policy,
independent of any inertia that may be present in the exogenous disturbance process rn
t .
The additional terms represent the way in which policy should deviate from what would be
judged optimal simply taking into account the current outlook for the economy, in order
to follow through upon commitments made at an earlier date. It is the desirability of the
central bank’s being able to credibly commit itself in this way that makes it desirable for
monetary policy to be somewhat inertial.
The extent to which these equations imply inertial behavior of the nominal interest rate
can be clariﬁed by writing a law of motion for the interest rate that makes no reference to
the Lagrange multipliers. Let us assume again a state-space representation (3.12) – (3.13)
for the evolution of the natural rate. Equation (3.29) then takes the form
φt = Nφt−1 + nst,
(3.31)
where the matrix of coeﬃcients n is given by
n ≡−C
∞
X
j=0
˜A−(j+1) ak′ T j.
The endogenous variable φ2t may be eliminated from the system of equations (3.31), yielding
an equation with instead two lags of φ1t. We may write this last equation as
det[I −NL]φ1t = n′
1st + (N12n′
2 −N22n′
1)st−1,
where L is the lag operator, and n′
i is the ith row of the matrix n. Then using (3.4) to
substitute out φ1t, we obtain the law of motion
Q(L)ˆrt = R(L)st
(3.32)
for the nominal interest rate, where
Q(L) ≡det[I −NL],
R(L) ≡−(λrσ)−1[n′
1 + (N12n′
2 −N22n′
1)L].
(3.33)
37

This should be compared with the simple result (3.13) in the case of the time-consistent
plan.
Equation (3.32) implies that under the optimal plan, there are intrinsic dynamics to the
evolution of the nominal interest rate, unrelated to any persistence in the ﬂuctuations in the
exogenous states st. For example, in the case that rn
t is an exogenous white-noise process
(unforecastable at any prior date), (3.32) implies that rt should instead follow a second-order
autoregressive process. The degree of persistence of these intrinsic dynamics is determined
by the roots µi of the characteristic equation
Q(µ) = 0
associated with the autoregressive polynomial in (3.32). These roots are just the eigenvalues
of the matrix N, or the two eigenvalues of M that have a modulus less than one. The
implied degree of monetary policy inertia is greater the larger are these roots. These roots
are determined by factors independent of the dynamics of the exogenous disturbances. Thus
it may be optimal for nominal interest rates to exhibit a great deal of persistence, regardless
of the degree of persistence of the ﬂuctuations in the natural rate.
3.5
A Simple Limiting Case
The extent to which the equations just derived imply behavior that might appear to involve
interest-rate “smoothing” can be clariﬁed by considering a limiting case, in which a simple
closed-form solution may be obtained. This is the limiting case in which the value of the
parameter κ (the slope of the “short-run Phillips curve”) approaches zero. In this limit,
variations in output relative to potential cause no change in the level of real marginal cost,
and ﬁrms accordingly have no reason to change their prices at any time. Hence πt = 0 at all
times, regardless of monetary policy. We shall assume that the values of all other parameters
are unchanged.47
47This does not necessarily make sense, if the coeﬃcients in the loss function (2.9) are intended to represent
an approximation to true social welfare, as suggested above, since in that case there is a theoretical relation
between λx and the various preference and technology parameters that also determine κ. But even in that
38

In this limiting case, the κφ2t term in (3.3) can be neglected, so that it becomes possible
to solve for the variables xt, rt, and φ1t using only equations (2.7), (3.3), and (3.4).48 This
system of equations can again be written in the form (3.27), but now zt is simply the scalar
variable ˆxt and φt is simply the scalar variable ˆφ1t. As a consequence, A, B, C, D, and a are
all now scalars, given by
A
=
1 + λx(λrσ2)−1,
B
=
−(βλrσ2)−1,
C
=
−λx,
D
=
β−1,
a
=
−σ−1.
The characteristic equation for M is then simply
µ2 −[1 + β−1 + λx(λrσ2)−1]µ + β−1 = 0.
(3.34)
One observes that it necessarily has two real roots, satisfying
0 < µ1 < 1 < β−1 < µ2,
and that µ2 = (βµ1)−1. Because exactly one root is inside the unit circle, the system of
equations (3.27) has a unique bounded solution. The solution is given by equations (3.28)
and (3.29), where now G, N, and ˜A are scalars
G
=
(β−1 −µ1)λ−1
x
> 0,
N
=
µ1 > 0,
˜A
=
µ2 > 1.
case, we may view the present calculation as solving a mathematical problem that is closely similar in form,
even if not identical, to one that arises in an optimal monetary policy problem.
48The intuition for this reduction in the order of the system of equations is simple. We no longer need to
solve for πt, as we set this variable equal to zero. We no longer obtain a ﬁrst-order condition corresponding
to (3.2) by diﬀerentiating the Lagrangian with respect to πt, because it is not possible to vary inﬂation.
Likewise, we no longer obtain a Lagrange multiplier φ2t corresponding to constraint (2.6), as this constraint
is already guaranteed to be satisﬁed once we have set πt equal to zero at all times.
39

Since equation (3.29) now involves only ˆφ1t, it is possible to use (3.4) to substitute ˆrt for ˆφ1t,
and thus directly obtain an equation for the optimal interest-rate dynamics,
ˆrt = µ1ˆrt−1 + λx(λrσ2)−1
∞
X
j=0
µ−(j+1)
2
Etrn
t+j.
(3.35)
This gives us a law of motion of the form (3.32), but in this limiting case, a representation
is possible in which Q(L) is only of ﬁrst order, and R(L) is a constant (there are no lags at
all). In fact, one can easily show that (3.35) is a partial-adjustment equation of the form
(1.2), where the inertia coeﬃcient θ = µ1, and the time-varying interest-rate “target” is
given by49
¯rt = ropt + (1 −µ−1
2 )
∞
X
j=0
µ−j
2 Etrn
t+j.
(3.36)
Thus the optimal interest-rate dynamics are described by partial adjustment toward a moving
average of current and expected future natural rates of interest.
In the case that the natural-rate dynamics are of the simple form (3.15), the target rate
is just a function of the current natural rate of interest, although (because of expected mean-
reversion of the natural rate in the future) it varies less than does the natural rate itself.
Speciﬁcally, we have
¯rt = ropt + krn
t ,
(3.37)
where k ≡(µ2 −1)/(µ2 −ρ), so that 0 < k < 1. If the ﬂuctuations in the natural rate
are largely transitory, the elasticity k may be quite small, though it is any event necessarily
greater than 1 −β. If the ﬂuctuations in the natural rate are nearly a random walk (ρ is
near one), the elasticity k instead approaches one. In this case, interest rates eventually
change by nearly as much as the (nearly permanent) change that has occurred in the natural
rate; but even in this case, the change in the level of nominal interest rates is delayed. As
a result, an innovation in the natural rate is followed by a series of interest rate changes in
the same direction, as in the characterizations of actual central-bank behavior by Rudebusch
and Goodhart.
49This representation is possible because (3.34) implies that λx(λrσ2)−1 is equal to (1 −µ1)(µ2 −1).
40

While this partial-adjustment representation is only exactly correct in an unrealistic
limiting case, it provides considerable insight into the optimal interest-rate responses in
more realistic cases. This can be shown through numerical analysis of a case with κ > 0.
3.6
A Numerical Example
To consider what degree of interest-rate inertia might be optimal in practice, it is useful
to consider a numerical example, “calibrated” to match certain quantitative features of the
Rotemberg and Woodford (1997, 1998) analysis of optimal monetary policy for the U.S.
economy. The numerical values that we shall use are given in Table 1. The value of β must
be only slightly less than one, given observation of only a small positive average real rate of
return. The values for σ and κ represent the estimates of Rotemberg and Woodford, who ﬁnd
that these values result in the best ﬁt between the estimated impulse responses of inﬂation
and output to a monetary policy (identiﬁed using structural VAR methodology) and those
predicted by their model (which, insofar as the role of these two parameters is concerned, is
essentially the same as that considered here).
The assumed standard deviation of ﬂuctuations in the natural rate follows from the
Rotemberg-Woodford estimates of the statistical properties of the residuals of their structural
equations.50 The value of this parameter has in any event no eﬀect upon our conclusions
about the relative variability of diﬀerent variables under alternative policies, since there is
only one kind of stochastic disturbance.51
More important are our assumptions about the serial correlation properties of the shocks.
We shall assume an AR(1) process as in (3.15), as a result of which we need only calibrate
50Speciﬁcally, this number represents their estimate of the standard deviation of Et−2rn
t , where rn
t is
deﬁned as in (3.13). This is because their structural equations coincide with those of the simpler model used
here only when conditioned upon information available two quarters earlier. Because of the two-period lag
assumed in the eﬀects of monetary policy upon output and inﬂation in their variant model, Et−2rn
t is the
exogenous disturbance process in their model that plays the role most analogous to that of the “natural rate
of interest” in the present model.
51However, our assumption about the variability of the natural rate plays an important role in justifying
our assumed value for λr. The value assumed here implies that the standard deviation of the natural rate
is roughly the same size as its mean.
Hence it is frequently negative, meaning that in a zero-inﬂation
environment the zero bound on nominal interest rates would prevent short rates from perfectly tracking the
natural rate of interest.
41

a single parameter ρ. The value of most interest here is unclear, since in reality there are
probably diﬀerent types of disturbances, with diﬀering degrees of persistence.52 We shall
accordingly compare our results under diﬀerent assumed values for ρ. Our baseline value
of ρ = .35, however, is chosen so as to imply, in the simpler model used here, a degree
of concern for reduction of interest-rate variability similar to that obtained by Rotemberg
and Woodford in their estimated model. We have sought a value for ρ such that optimal
monetary policy (i) involves a similar degree of interest-rate variability as in their numerical
results, and (ii) implies a similar shadow value of relaxation of the interest-rate variability
constraint (2.11). The value ρ = .35 is reasonably satisfactory on both grounds.53 Below,
however, we also report numerical results for the values ρ = 0 and ρ = .9. These values are
chosen to illustrate how our conclusions depend upon the assumed degree of serial correlation
of the shocks.
The coeﬃcient λx is the theoretical relative weight on output gap variability obtained
by Taylor series expansion of the expected utility of the representative household, evaluated
using the structural parameters of their model; it corresponds to a coeﬃcient from a similar
Taylor series expansion reported in the Rotemberg-Woodford welfare analysis. And ﬁnally,
λr is the Lagrange multiplier associated with interest-rate variability, if we seek to minimize
the expected discounted sum of welfare losses (2.10) subject to the constraint (2.11), as
discussed in section 2.54
We impose this constraint assuming the value of K = 1.44 as
discussed above, and assuming the values given in Table 1 for the other parameters. Hence,
in our baseline case (ρ = .35), the policy that minimizes our welfare criterion E[W] also
52The shock process estimated by Rotemberg and Woodford has two innovations per period and compli-
cated dynamics. See Appendix 2 of their NBER working paper.
53As shown in Table 2, this value implies that under the optimal policy, V [r] = 1.921, whereas Rotemberg
and Woodford obtain var(r) = 1.928 for their optimal policy. (The measure of interest-rate variability V [r]
used in this paper is deﬁned below in (3.38).) A slightly higher value of ρ, but in any event well below .4,
would match this precisely. At the same time, this value implies a shadow value (in terms of increasing
E[ ˜W]) of increased interest-rate variability V [r] equal to .236, as reported in Table 1. This compares with
the value .224 reported by Rotemberg and Woodford. A slightly lower value of ρ, but in any event well above
.3, would match this precisely.
54To be precise, this measures the marginal increase in E[˜L] that is possible per unit marginal increase
in V [r], the variability measure deﬁned below in (3.38). The unconditional expectation that is taken of the
loss measure is the same as that discussed below for the statistic E[W] reported in Table 2.
42

minimizes the expected discounted sum of (2.10), our quadratic approximation to the utility
of the representative household, subject to the constraint implied by the zero bound on
nominal interest rates. We could similarly calibrate the parameters x∗and r∗, but as these
do not matter for the optimal responses to shocks, we omit discussion of them.
For the parameter values in Table 1, the matrix N is given by
N =
"
.4611
.0007
−.7743
.6538
#
,
and its eigenvalues are found to be approximately .65 and .46. Both of these are substantial
positive quantities, suggesting that once interest rates are perturbed in response to some
shock, it should take several quarters for them to be restored to nearly their normal level,
even if the shock is completely transitory.
Figure 1 illustrates this by showing the optimal response of the short-term nominal
interest rate to a purely transitory increase in the natural rate of interest. This might be
due either to a temporary increase in the autonomous component of spending, ˆGt, or to a
temporary decrease in the natural rate of output due to an adverse “supply shock”. Either
type of shock would imply a temporary increase in the equilibrium real rate of interest in a
ﬂexible-price model, and, in our model with sticky prices, will increase both the output gap
and inﬂation,55 in the absence of an oﬀsetting adjustment of monetary policy.
To be precise, the Figure displays the impulse response of ˆrt+j, for j = 0 through 10,
to a unit positive innovation in ϵt, where the law of motion for the natural rate is given by
(3.15) with autocorrelation coeﬃcient ρ = 0. The shock in question unexpectedly raises the
natural rate rn
t by one percentage point, but the natural rate is expected to return to its
normal level by the next quarter, as shown by the dashed impulse response. The disturbance
to the nominal interest rate is equally transitory under the optimal non-inertial plan, also
shown in the ﬁgure by a dash-dotted line, though the amplitude of the nominal interest rate
increase would be smaller than the increase in the natural rate, in order to reduce interest-
rate variability at the price of some increase in inﬂation and output gap variability. The
55Note that an adverse supply shock lowers output, but increases the output gap, as sticky prices prevent
output from falling as much as it would in the case of fully ﬂexible prices.
43

impulse response under an optimal policy is instead given by the solid line. Nominal interest
rates rise immediately, but by only a fraction of the increase in the natural rate (about 24
basis points). However, the optimal path of nominal interest rates involves a more persistent
increase than in the case of the natural rate. While the natural rate is perturbed only in
the quarter of the shock, the central bank keeps nominal interest rates 11 basis points above
their normal level in the following quarter, and still 5 basis points above normal even two
quarters later.
The associated eﬀects of the shock upon inﬂation and the output gap are shown by the
solid impulse responses in Figure 2, which also reproduces the impulse response of the nom-
inal interest rate in the third panel.56 In the quarter of the shock, the failure of interest
rates to rise as much as the increase in the natural rate results in a temporarily negative
“interest-rate gap”, but by the next quarter the interest-rate gap has become positive (inter-
est rates higher than the natural rate), owing to the inertia in central bank policy. The fact
that a negative interest-rate gap is allowed to develop in the quarter of the shock results in a
temporary positive output gap; but in the next quarter and after, the positive (current and
expected future) interest-rate gaps result in negative output gaps. The resulting response of
inﬂation involves only a very small increase in the quarter of the shock, and then a sharper
decrease in the inﬂation rate after the positive interest-rate gap develops. In the quarter of
the shock, the inﬂationary eﬀect of the positive output gap is oﬀset by the disinﬂationary
eﬀect of the anticipation of negative output gaps in the later quarters. It is this eﬀect of the
private sector’s anticipation of inertial monetary policy that accounts for the desirability of
such inertia – for it allows the central bank to oﬀset the inﬂationary impact of the shock
without having to raise nominal interest rates by nearly as much as the increase in the nat-
ural rate, as it would have to in order to prevent increased inﬂation in the quarter of the
shock through an interest-rate increase that is expected to be no more persistent than the
shock.
56Here the inﬂation rate and nominal interest rate are reported as annualized percentage rates; thus the
responses plotted are actually for 4ˆπt and 4ˆrt.
44

To further clarify the advantages of interest-rate inertia, Figure 2 also plots the impulse
responses associated with the optimal non-inertial policy, assuming the same parameter
values. (These impulse responses are plotted as dash-dotted lines in each panel.) Note that
the responses of all variables to the shock are purely transitory under the non-inertial plan,
as they would be under the time-consistent plan. (Note that the optimal non-inertial plan
coincides with the time-consistent plan, in the case that ρ = 0.) The shock would result in a
much larger increase in inﬂation in the quarter of the shock than occurs under the optimal
policy, even though the central bank also raises nominal interest rates more sharply under
this plan. This shows the cost to the central bank of not being able to commit itself to an
inertial policy. The initial positive output gap is larger under the non-inertial plan as well.
Of course, the non-inertial plan has the advantage that the disturbances to inﬂation, the
output gap, and the nominal interest rate are purely transitory. Still, the overall variability
of inﬂation is lower under the optimal plan than under the non-inertial one; for even though
inﬂation falls below its normal level in the quarter following the shock, under the optimal
plan, the decline in this quarter under the optimal plan is not as large as the increase in
inﬂation during the quarter of the shock under the time-consistent plan.
Statistics regarding the variability of the various series under the two plans are reported
in the ﬁrst panel of Table 2. Here independent drawings from the same distribution of shocks
ϵt are assumed to occur each period,57 and inﬁnite-horizon stochastic equilibria are computed
under each policy. The measure of variability reported for each variable zt is
V [z] ≡E[E0{(1 −β)
∞
X
t=0
βtˆz2
t }],
(3.38)
where the outer (unconditional) expectation is over possible initial states of the economy rn
0
at the time that policy is chosen, computed using the stationary distribution associated with
the exogenous process (3.15) for the natural rate. The unconditional expectation allows us a
measure that is independent of the economy’s initial state. Except for the discounting, E[z]
57The assumed variance of the shocks ϵt is chosen so as to imply a standard deviation for the natural
rate of interest of the size indicated in Table 1. This is irrelevant, of course, for the comparisons of relative
variances between the two regimes, or comparison of the relative size of expected losses E[W].
45

corresponds to the unconditional variance of zt, and in the case of non-inertial plans, it is
equal to the unconditional variance even though β < 1. In the case of the optimal plan, the
discounted measure is of greater interest, because our loss measure E[W] is in that case just
a weighted sum of the previous three columns.
Here E[W] is again the unconditional expectation of (2.8), integrating over the stationary
distribution for the initial state rn
0. Since the optimal plan minimizes W regardless of the
initial state rn
0, it minimizes E[W] among all possible plans consistent with the structural
equations. The optimal non-inertial plan also minimizes E[W] among all non-inertial plans;
thus there is a necessary ranking of this loss measure, among the three plans for which
statistics are reported for each value of ρ. The values reported in Table 2 are computed for
the case in which x∗= r∗= 0, so that the steady-state values of the variables are the same
under all three plans. Thus the reported statistic E[W] refers only to losses associated with
the economy’s response to transitory shocks under each of the three policies. Alternatively,
the ﬁnal column reports the amount by which E[W] exceeds the steady-state value (the
value of W achieved if rn
t = 0 with certainty forever). This is the statistic of interest if
one wants to compare fully optimal policy under commitment to a regime of discretionary
optimization (for example) in which the values of x∗and r∗have been adjusted to make the
steady state under discretion coincide with the optimal steady state. (Were we not to make
this assumption, the welfare losses associated with time-consistent and optimal non-inertial
policies would exceed those associated with the optimal policy by an extent even larger than
is indicated in Table 2, owing to the distortions of the steady state discussed above.)
One observes that the variability of inﬂation is nearly 75 percent larger under the time-
consistent policy, or the optimal non-inertial policy, than under the optimal policy, while
the variance of the nominal interest rate is more than twice as large. (The variance of the
output gap is more than a third larger as well, although, since the variability of this variable
has only a small weight in our assumed loss function, the optimal policy is not primarily
chosen with a view to stabilization of the output gap.) Hence the loss measure E[W] is 60
percent higher under the time-consistent or non-inertial policy.
46

Figures 3 and 4 present the corresponding impulse response functions in the case of a
natural rate process that exhibits positive serial correlation, speciﬁcally, our baseline case
described by (3.15) with an autoregressive parameter ρ = .35. In this case the advantages of
optimal policy over the time-consistent plan are more pronounced, though commitment to an
optimal non-inertial policy can also do somewhat better in this case than the discretionary
outcome. Again one observes that under an optimal policy regime, the nominal interest rate
does not at ﬁrst rise as much as the increase in the natural rate; then, as the natural rate
declines back toward its normal level, the central bank continues to keep nominal interest
rates high for a time, so that they return to normal more slowly than does the natural rate.
Thus optimal policy results in a negative interest-rate gap at ﬁrst, followed by a positive
interest-rate gap later. Again, this is associated with an initial positive output gap, followed
by a smaller negative output gap a few quarters later, and a very small initial increase in
inﬂation, followed by a subsequent decrease in inﬂation to a level lower than its steady-state
level.
And once again, this pattern results in lower overall variability of inﬂation, the output
gap, and of the nominal interest rate, than one would obtain under the time-consistent
optimizing policy. In fact, the relative advantage of the optimal policy is even greater in this
case: the variance of inﬂation is nearly four times as large under the time-consistent plan,
and the variances of both the output gap and the nominal interest rate are more than twice
as large. The result is that the central bank’s loss function is two-and-a-third times as large
under the time-consistent policy.
The picture is somewhat diﬀerent if the central bank commits itself to an optimal non-
inertial policy. In this case, it should commit itself to raise interest rates more in response
to an increase in the natural rate than occurs under the time-consistent plan; the result
is that the responses of the interest-rate gap, inﬂation, and the output gap are all smaller
in amplitude by a factor of about two-thirds. The result is substantially less variability of
inﬂation and the output gap, but even more variability of interest rates, achieving a small,
but rather modest, reduction in E[W]. The optimal plan is still signiﬁcantly better in terms
47

of both inﬂation variability and interest-rate variability (though output gap variability, which
matters relatively little for welfare under our parameter values, is slightly higher), and the
overall loss measure E[W] is still more than twice as large under the non-inertial policy. These
comparisons clearly show the advantages, from the point of view of improved stabilization,
not only of the central bank’s being able to commit itself, but of its committing itself to an
inertial policy.
Finally, Figures 5 and 6 present the corresponding impulse response functions in the case
of an even more persistent natural rate process, with ρ = .9. In the case of these very per-
sistent ﬂuctuations in the natural rate of interest, time-consistent optimizing behavior does
extremely poorly at stabilizing the central bank’s goal variables. The variance of inﬂation is
a thousand times as large as under the optimal plan, and the variance of the interest rate is
over 60 times as large; as a result, the expected value of the loss criterion is more than 230
times as large.58
The dramatic failure of discretionary optimization in this case occurs because, for these
parameter values, the time-consistent optimizing response actually involves an interest-rate
increase that is larger than the increase in the natural rate, despite the positive weight λr in
the central bank’s loss function. This occurs because of a “discretion trap” similar to the one
analyzed by Barro and Gordon (1983), despite the fact that it involves no incorrect target
level of output or bias in the average rate of inﬂation. When an inﬂationary real disturbance
occurs, the expectation that the central bank will allow high inﬂation in subsequent quarters
(while the natural rate of interest continues to be high) creates a situation in which the
central bank feels compelled to choose high inﬂation in the present; given the inﬂationary
expectations, the only policy that could achieve lower inﬂation would involve an unacceptably
large increase in interest rates. But the expectation that the central bank will behave this
way results in an equilibrium in which the central bank must accept very high (nominal)
58Given the highly volatile behavior of the endogenous variables under this solution, one may doubt the
accuracy of our linear-quadratic approximations. Still, the qualitative conclusion is surely correct; for if
there were a solution with low inﬂation and interest-rate volatility, then our approximate methods would
accurately describe it.
48

interest rates, as a result of the persistent high inﬂation.
Interestingly, in the case of a shock as persistent as this, the optimal plan does not involve
nominal interest rates that ever rise to the same degree as does the natural rate. However,
the optimal response does again involve deﬂation after the initial quarter, brought about by
a negative output gap that is expected to be maintained from late in the ﬁrst year onward.
This low level of output is achieved because short-term real interest rates are high (rising by
70 basis points during the ﬁrst year after the shock). Real interest rates are high, of course,
because expected inﬂation is low, rather than because nominal interest rates are high (by
comparison with what happens under the time-consistent plan). This illustrates that it is
not simply the path of nominal interest rates alone that distinguishes optimal policy, a topic
to which we return in the next section.
The instability here of the time-consistent plan is mainly an indication that discretionary
optimization is severely suboptimal, rather than an indication that a non-inertial plan must
be extremely unstable. Indeed, the optimal non-inertial plan is not too much worse than the
fully optimal plan, and is worse only insofar as it involves higher interest-rate volatility. As
Figure 6 shows, the optimal non-inertial plan involves a commitment to lower inﬂation and
a negative output gap when the natural rate is above average, results that are achieved by
raising real interest rates by even more than the increase in the natural rate. Such a response,
however, cannot be achieved endogenously by a non-inertial “Taylor rule” that raises nominal
interest rates only insofar as either inﬂation or the output gap increase. The “Taylor rule”
would have to be augmented by a term that is increasing in the current natural rate of
interest, with a coeﬃcient greater than one. Hence achievement of these stabilization gains
through commitment to a non-inertial policy rule would depend critically upon accurate
observation of the current exogenous shock. But as we show below, the optimal plan can be
implemented by an inertial feedback rule that requires no feedback at all from the exogenous
shock, and this may be another important advantage of inertial policy.
Visual inspection of the optimal impulse responses in Figures 1, 3 and 5 suggests that
“partial adjustment” of the nominal adjustment toward a level determined by the current
49

natural rate of interest, just as in the limiting case analyzed above, gives a reasonable
approximate account of optimal interest-rate dynamics. The reason for this is not hard to
see from our previous analysis. Note that the element N12 of the matrix N is quite small; it
is three orders of magnitude smaller than the other elements of the matrix. Hence one would
not obtain too poor an approximation to the optimal interest-rate dynamics by setting N12
equal to zero in expression (3.32). But in that case, Q(L) and R(L) reduce to
Q(L) = (1 −N11L)(1 −N22L),
R(L) = −(λrσ)−1n′
1(1 −N22L),
as a result of which (3.32) is equivalent to
ˆrt = N11ˆrt−1 −(λrσ)−1n′
1st.
(3.39)
This implies partial adjustment of the interest rate, as in equation (1.2), toward a time-
varying “target” interest rate equal to
¯rt = ropt −[(1 −N11)λrσ]−1n′
1st,
(3.40)
with an inertia coeﬃcient of θ = N11. In the case that the natural rate evolves according
to (3.15), this time-varying target rate is again described by an equation of the form (3.37).
In our numerical example, in the case that ρ = 0, the target rate (neglecting the constant
term) is given by ¯rt = .44rn
t , while in the case that ρ = .35, the elasticity is instead k = .52,
and when ρ = .9, k = .75. In each case, the inertia coeﬃcient is equal to θ = .46, indicating
that interest rates should be adjusted only about half of the way toward the current target
level (implied by the natural rate) within the quarter.
4
Advantages of a Central Bank Preference for Smooth-
ing
We turn now to the question of how the optimal responses to shocks, derived in the previous
section, are to be brought about in practice. There are various ways in which this question
50

of implementation might be approached. Perhaps the most straightforward is the design of a
policy rule to which the central bank may commit itself; this approach is treated in the next
section. But another approach is to conceive the choice of monetary policy as a delegation
problem. That is, one asks what sort of central banker (or monetary policy committee)
should be appointed, taking it as given that the central banker will seek to maximize the
good as he or she personally conceives it; or one asks what goal the central bank should be
charged with, understanding that the details of the pursuit of the goal on a day-to-day basis
should then be left to the bank. This sort of question is of considerable practical relevance,
especially since the central banks that are currently most explicit about their commitment
to systematic monetary policy (such as the “inﬂation targeting” central banks (Svensson
(1999)), generally make commitments about goals rather than the details of their operating
procedures.
The optimal delegation question becomes non-trivial if one assumes, as is common in
this literature, that the central bank will pursue its goal in a discretionary fashion, rather
than committing itself to an optimal plan, so that the outcome for the economy will be
the time-consistent plan associated with that goal.59 In this case, the optimal goal with
which to charge the central bank need not correspond to the true social welfare function;
ineﬃcient (discretionary) pursuit of a distorted objective may produce a better outcome,
from the standpoint of the true social objective, than ineﬃcient pursuit of the true objective
itself.60 For example, Rogoﬀ(1985) famously argues that appointment of a central banker
who assigns a greater relative weight to inﬂation stabilization than does the true social
welfare function may actually better serve social welfare, as an appropriate degree of bias
can help to oﬀset the inﬂationary bias due to discretion.61 Svensson (1996) similarly argues
59It is, however, sometimes disputed whether actual central bankers are as little capable of choosing to
commit themselves as such models assume; see, e.g., McCallum (1999, sec. 2).
60This somewhat paradoxical conclusion is familiar in the theory of delegation more generally. See, e.g.,
Persson and Tabellini (1994).
61Walsh’s (1995) contracting solution to the problem of inﬂation bias under discretion also amounts to
arranging for the central banker to pursue an objective other than social welfare. In that formulation, the
state-contingent payments to the central banker serve to modify the bank’s objective function in the desired
direction. Here we shall speak of choosing the central bank’s objective, without specifying how this is to
be done. It might be through a contract, through screening of the personalities of central bankers before
51

that a central bank with a price level target, rather than an inﬂation target, may better
serve to stabilize inﬂation in response to shocks, owing to the bias resulting from discretion
in the central bank’s response to shocks.62
We have shown above that in the case of the policy problem considered here, discre-
tionary pursuit of the true social objective (2.8) similarly results in a sub-optimal response
to ﬂuctuations in the natural rate of interest. In particular, we have shown that it results
in interest-rate responses that are insuﬃciently inertial. This raises the question whether it
would not be better for a central bank that is expected to act under discretion to pursue
an alternative objective, one that includes an interest-rate smoothing objective in the sense
discussed in the introduction. Note that actual central banks are often described as pursuing
interest-rate smoothing as one goal among several, though we argued above that such a goal
had no place in the true social welfare function described by (2.8) – (2.9). In fact, such an
attitude on the part of central bankers may not be something one should try to correct, if
one expects them to pursue their goals in a discretionary fashion.
4.1
Time-Consistent Equilibrium with a Smoothing Objective
We now consider the consequences of delegating the conduct of monetary policy to a central
banker that is expected to seek to minimize the expected value of a criterion of the form
(2.8), where however (2.9) is replaced by a function of the form
Lcb
t = π2
t + ˆλx(xt −ˆx∗)2 + ˆλr(rt −ˆr∗)2 + λ∆(rt −rt−1)2.
(4.1)
Here we allow the weights ˆλx, ˆλr to diﬀer from the weights λx, λr associated with the true
social loss function, and similarly allow the targets ˆx∗, ˆr∗to diﬀer from x∗and r∗. We also
allow for the existence of a term that penalizes interest-rate changes, not present in the true
social loss function (2.9).
The time-consistent optimizing plan associated with such a loss function can be derived
appointment, or by teaching central bankers that the pursuit of certain objectives rather than others is in
the general good.
62Kiley (1998) addresses the same issue in the context of a model closely related to the one used here.
52

using familiar methods, expounded for example in Soderlind (1998). The problem is more
complicated than the one considered earlier, because the presence of a term involving the
lagged interest rate in the period loss function (4.1) means that even in a Markovian equi-
librium, outcomes will depend upon the lagged interest rate. This in turn means that the
central bank’s expectations at date t about equilibrium in periods t + 1 and later are not
independent of its choice of rt. However, in such an equilibrium, the central bank’s value
function in period t is given by a function V (rt−1; rn
t ), which function is time-invariant.
(Here we simplify by assuming that the natural rate of interest is itself a Markovian process,
with law of motion (3.15), though we could easily generalize our results to allow for more
complicated linear state-space models.)
Standard dynamic programming reasoning implies that the value function must satisfy
the Bellman equation63
V (rt−1; rn
t )
=
min
(rt,πt,xt) Et
1
2[π2
t + ˆλx(xt −ˆx∗)2 + ˆλr(rt −ˆr∗)2 + λ∆(rt −rt−1)2]
+βV (rt; rn
t+1)
o
,
(4.2)
where the minimization is subject to the constraints
πt
=
κxt + βEt[π(rt; rn
t+1)],
xt
=
Et[x(rt; rn
t+1) −σ−1(rt −rn
t −π(rt; rn
t+1))].
Here the functions π(rt; rn
t+1), x(rt; rn
t+1) describe the equilibrium that the central bank ex-
pects to result in period t+1, conditional upon the exogenous state rn
t+1. This represents the
consequence of discretionary action at that date and later, that the current central banker re-
gards him or herself as unable to change. Similarly, V (rt; rn
t+1) represents the value expected
for the central bank’s objective as of date t + 1, in the discretionary equilibrium described
by those functions.
Discretionary optimization by the central bank at date t is then deﬁned by the minimiza-
tion problem on the right-hand side of (4.2). The solution to this problem, for any given
63Multiplication of the central bank’s loss function by a factor 1/2 here eliminates a factor of 2 from
subsequent expressions such as (4.6), and is purely a normalization of the value function.
53

current state (rt−1; rn
t ), deﬁnes a set of functions r(rt−1; rn
t ), π(rt−1; rn
t ), x(rt−1; rn
t ), indicating
the optimal values of rt, πt, and xt, and a function V (rt−1; rn
t ) indicating the minimized value
of the right-hand side of the equation. Consistency of the central bank’s expectations then
requires that the functions V , π, x used to deﬁne this minimization problem are identical to
the functions obtained as its solution.
We shall furthermore restrict attention to solutions of the Bellman equation in which the
value function is a quadratic function of its arguments, and the solution functions for r, π,
and x are each linear functions of their arguments. The solution functions can accordingly
be written
r(rt−1; rn
t ) = r0 + rrrt−1 + rnrn
t ,
(4.3)
π(rt−1; rn
t ) = π0 + πrrt−1 + πnrn
t ,
(4.4)
x(rt−1; rn
t ) = x0 + xrrt−1 + xnrn
t ,
(4.5)
where r0, rr, rn, and so on are constant coeﬃcients to be determined by solving a ﬁxed-point
problem. The ﬁrst-order conditions for the optimization problem in (4.2) involve the partial
derivative of the value function with respect to the lagged interest rate. This too must be a
linear function of its arguments. In fact, diﬀerentiation of (4.2) using the envelope theorem
implies that when the value function is deﬁned, the partial derivative with respect to its ﬁrst
argument must satisfy
V1(rt−1; rn
t ) = λ∆[rt−1 −r(rt−1; rn
t )].
(4.6)
Thus linearity of the solution function r guarantees the linearity of this function as well.
We turn now to the ﬁxed-point problem for the constant coeﬃcients in the solution
functions. First of all, substitution of the assumed linear solution functions into the two
constraints following (4.2), and using
Etrn
t+1 = ρrn
t ,
(4.7)
allows us to solve for xt and πt as linear functions of rt and rn
t . (Let the coeﬃcients on
rt in the solutions for xt and πt be denoted Xr and Πr respectively. These coeﬃcients are
54

themselves linear combinations of the coeﬃcients xr and Πr introduced in (4.4) – (4.5).)
Requiring the solution functions deﬁned in (4.3) – (4.5) to satisfy these linear restrictions
yields a set of six nonlinear restrictions upon the coeﬃcients x0, xr, xn and so on.64
Substituting these solutions for xt and πt into the right-hand side of (4.2), the expression
inside the minimization operator can be written as a function of rt and rn
t . This expression
is quadratic in rt, and so it achieves a minimum if and only if it is convex, in which case
the optimum is characterized by the ﬁrst-order condition obtained from diﬀerentiation with
respect to rt. Because the function is quadratic, it is globally convex if and only if the second-
order condition is satisﬁed; thus a solution satisfying the ﬁrst- and second-order conditions
is both necessary and suﬃcient for optimality.
Substituting (4.6) for the derivative of the value function, the ﬁrst-order condition may
be written as
Πrπt + ˆλxXr(xt −ˆx∗) + ˆλr(rt −ˆr∗) + λ∆(rt −rt−1) + βλ∆(rt −Etrt+1) = 0.
(4.8)
Substituting into this the above solutions for πt and xt as functions of rt and rn
t , and the
assumed solution (4.3) for rt+1 as a function of rt and rn
t , we see that the second-order
condition may be written as
Ω≡Π2
r + ˆλxX2
r + ˆλr + λ∆+ βλ∆(1 −rr) ≥0.
(4.9)
Now requiring that the solutions deﬁned in (4.3) – (4.5) always satisfy the linear equation
(4.8) gives us another set of three nonlinear restrictions on the constant coeﬃcients of the
solution functions. We thus have a set of nine nonlinear equations to solve for the nine
coeﬃcients of equations (4.3) – (4.5). A set of coeﬃcients satisfying these equations, and
also satisfying the inequality (4.9), represent a linear Markov equilibrium for the central
bank objective (4.1).
We shall as usual be interested solely in the case of a stationary equilibrium, so that
ﬂuctuations in rt, πt and xt are bounded if the ﬂuctuations in rn
t are bounded. (As before, this
64The restrictions are nonlinear because the coeﬃcients Xr and so on are themselves functions of the
coeﬃcients xr and so on.
55

is the case in which our linear-quadratic approximations are justiﬁable in terms of a Taylor
series approximation to the exact conditions associated with private-sector optimization, in
the case of small enough exogenous disturbances.) Given (4.3) – (4.5) and the assumption
of stationary ﬂuctuations in rn
t , it is clear that πt and xt will be stationary processes as long
as rt is. It is also obvious that rt will be stationary (bounded) if and only if
|rr| < 1.
(4.10)
Thus we are interested in solutions to the nine nonlinear equations that satisfy both inequal-
ities (4.9) and (4.10).
In the case that ˆλx, ˆλr, λ∆≥0, it will be observed that (4.10) implies condition (4.9),
so that we need not concern ourselves with the convexity issue in that case. However, non-
negativity of these weights in the central-bank objective is not necessary for convexity of the
central bank’s optimization problem, and it is of some interest to consider delegation to a
central banker with a negative weight on some term. In particular, we shall see that there are
advantages to delegation to a central banker with ˆλr < 0, while λ∆> 0: the central banker
dislikes large interest-rate changes of either sign, but actually prefers for interest rates to
deviate farther from their “target” level ˆr∗(which in such a case is hardly a target!). Such
preferences need not result in a violation of convexity, though the negative ˆλr term itself
makes it harder for (4.9) to be satisﬁed. As long as positive weights are placed on inﬂation
and output variability in the central bank loss function, the eﬀects of current interest-rate
decisions on current inﬂation and output tend to make the central bank’s criterion function
convex in rt. If in addition λ∆> 0, convexity is increased, both because of the direct eﬀect
of the current interest-rate level upon the current interest-rate change, and because of the
eﬀect of the current interest-rate decision upon expected future inﬂation and output. In this
case, four out of ﬁve terms on the left-hand side of (4.9) are necessarily positive, and the
condition will be satisﬁed as long as these terms together outweigh the negative ˆλr term.65
65Note that the conditions required for convexity of the bank’s objective at date t, when it takes as given
equilibrium outcomes from date t + 1 onward, are much weaker than the conditions that would be required
for convexity of its objective if it viewed itself as being able to commit itself at date t to any state-contingent
plan from that date onward that was consistent with the structural equations (2.6) – (2.7).
56

We turn now to the question of what loss function the central bank should be assigned to
minimize, if it is assumed that a time-consistent plan of this sort will be pursued. As above,
we begin by considering the steady state associated with such an equilibrium. It is no longer
possible, as above, to give a closed-form solution for the steady-state inﬂation rate without
solving for the equilibrium responses to shocks. Nonetheless, it is clear that the parameters
ˆx∗, ˆr∗aﬀect only the steady state, and not the character of the deviations from the steady
state resulting from ﬂuctuations in the natural rate. Furthermore, these two parameters of
central bank preferences give us more than enough degrees of freedom to bring about the
desired steady state, whatever values we may choose for ˆλx, ˆλr, and λ∆. For there is only a
one-parameter family of possible steady-state values of π, x, r consistent with the structural
equations (2.6) – (2.7), regardless of monetary policy. We thus only need to vary one policy
parameter in order to make the equilibrium steady state coincide with the optimal one. For
example, we may stipulate that ˆr∗= r∗, the target value in the true social welfare function,
and simply adjust ˆx∗to eliminate any bias in the steady-state inﬂation rate resulting from
discretion.66
Accordingly, we may determine the desired values of the weights ˆλx, ˆλr, and λ∆simply
with regard to achieving desirable equilibrium responses to shocks, taking it as given that
the steady state is the optimal one described in (3.26).
Then, whatever our choices for
the weights, we can choose target values ˆx∗, ˆr∗that make the time-consistent steady state
coincide with the optimal one.
As a simple example, suppose that x∗> 0, while r∗= 0. Then as shown earlier, the
optimal steady state involves πopt = xopt = ropt = 0. But this is the steady state consistent
with equilibrium conditions (2.6), (2.7) and (4.8) as long as
ˆλxXrˆx∗+ ˆλrˆr∗= 0.
A suﬃcient condition for this (though not necessary) would be to choose ˆx∗= ˆr∗= 0. Thus,
as in the proposal of Blinder (1998, chap. 2), the average inﬂation bias is eliminated by
66Because the present speciﬁcation already has more degrees of freedom than are needed, we have not
bothered to consider a target inﬂation rate diﬀerent from zero in (4.1).
57

choosing a central banker whose goal is to stabilize output around the natural rate (i.e., for
whom ˆx∗= 0), even though the true social welfare function is one with x∗> 0.67
We turn now to the consequences of the weights in the central-bank loss function (4.1)
for the equilibrium responses to shocks. As conjectured above, we ﬁnd that setting λ∆> 0
results in inertial interest-rate responses to ﬂuctuations in the natural rate.
If we take
the partial derivative of the left-hand side of (4.8) with respect to rt−1, using the solution
functions to express all terms as functions of rt−1 and rn
t , we obtain a coeﬃcient equal to
Ωrr −λ∆, where Ωis deﬁned in (4.9). The ﬁrst-order condition (4.8) thus implies that
Ωrr = λ∆
in any solution. Then if λ∆> 0, both Ωand rr must be non-zero, and of the same sign. The
second-order condition (4.9) then implies that in any equilibrium, both quantities must be
positive. Combining this result with (4.10), we conclude that in any stationary equilibrium,
0 < rr < 1.
(4.11)
Given this, the law of motion (4.3) for the nominal interest rate implies partial adjustment
toward a time-varying target that is a linear function of the current natural rate of interest.
Since this is at least a rough characterization of a way in which the optimal responses to
shocks diﬀer from the time-consistent responses when the central bank seeks to minimize true
social losses, it is plausible that delegating monetary policy to a central banker who believes
it is better to reduce the variability of interest-rate changes can improve social welfare.
One may wonder whether it is possible to choose the weights in the central bank’s loss
function so as to completely eliminate the distortions associated with discretion, and achieve
the same responses as under an optimal commitment. It should be immediately apparent
that it is not in general possible to achieve this outcome exactly. For we have shown above
67Of course, as in Rogoﬀ(1985), one might alternatively keep ˆx∗equal to the target value x∗in the true
social welfare function, and instead seek to mitigate the inﬂation bias by adjusting the value of ˆλx. The
inﬂation bias could be completely eliminated by setting ˆλx = 0. However, the value of ˆλx also aﬀects the
equilibrium responses to shocks, and such distortion of the weight put on output gap stabilization may have
undesirable consequences for that reason. Indeed, Rogoﬀargues that it is not desirable to adjust ˆλx to the
point that the inﬂation bias is fully eliminated, exactly because of this tension.
58

that the optimal interest-rate dynamics have a representation of the form (3.32), where Q(L)
is of second order and R(L) is of ﬁrst order; thus they generally do not take a form as simple
as (4.3). Nonetheless, we can show that exact implementation of the optimal plan is possible
at least in a limiting case. And we can also show that it is possible to achieve a pattern of
responses nearly as good as the optimal plan, in the “calibrated” numerical example taken
up earlier. These points are taken up in succession in the next two subsections.
4.2
Optimal Delegation in a Limiting Case
Here we consider again the limiting case with κ = 0 taken up in section 3.5. We have shown
there that in this special case, the optimal interest-rate and output dynamics do take the
form given by (4.3) and (4.5), where the coeﬃcients (neglecting the constant term) are given
by
rr = µ1,
rn
=
(1 −µ1)
 µ2 −1
µ2 −ρ
!
,
(4.12)
xr = −(β−1 −µ1)σ λr
λx
,
xn
=
1
σ(µ2 −ρ).
(4.13)
Here µ1, µ2 refer to the two roots of (3.34) discussed earlier. The question that we wish
to ask, then, is whether it is possible to choose the weights in (4.1) so that the optimal
values (4.12) – (4.13) solve the equilibrium conditions just derived. Since the optimal values
necessarily satisfy the conditions required for consistency with the structural equation (2.7),
it suﬃces that they also be consistent with conditions (4.8) and (4.9) for time-consistent
optimizing behavior on the part of the central bank.
In this limiting case, the conditions required for consistency of (4.3) and (4.5) with (4.8)
simplify to
(xr −σ−1)ˆλxxr + ˆλrrr + (1 −βrr)λ∆(rr −1) = 0,
(xr −σ−1)ˆλxxn + ˆλrrn + (1 + β(1 −rr −ρ))λ∆rn = 0.
These two equations depend only upon the ratios of the weights in the policy objective, ˆλr/ˆλx
and λ∆/ˆλx, rather than upon the absolute size of the three weights. (This is because inﬂation
59

variations are negligible under any policy regime, so the relative weight on inﬂation variability
no longer matters.) Hence we may, without loss of generality, suppose that ˆλx = λx, the
weight in the true social objective function. Using this simpliﬁcation, and substituting the
optimal values (4.12)–(4.13), the above two linear equations can be solved for the unique
values of ˆλr and λ∆consistent with the optimal equilibrium responses. These are given by
λ∆= λr
λrσ2(β−1 −µ1) + λx
(1 −βρµ1)βλx
> 0,
(4.14)
ˆλr = −(1 −βρ)(1 −βµ1)λ∆< 0.
(4.15)
While one ﬁnds that the kind of partial-adjustment interest-rate dynamics associated
with the optimal plan do require λ∆> 0, as conjectured, one ﬁnds that they cannot be
exactly matched through delegation to a central banker with discretion unless in addition
ˆλr < 0. This is another diﬀerence between the best objective for the central banker and the
true social objective function, since in the latter, λr > 0. As noted earlier, a negative value
for ˆλr does not necessarily imply violation of the convexity condition (4.9) needed for central-
bank optimization. In fact, we have shown above that the convexity condition holds in the
case of any solution to the ﬁrst-order condition with λ∆> 0 and rr > 0. As (4.12) implies
that rr > 0, and (4.14) implies that λ∆> 0, the above assumed central-bank objective does
result in a convex optimization problem for the central bank. Thus the optimal pattern of
responses to shocks can in this case be supported as an equilibrium outcome under discretion,
as long as the central bank is charged with pursuit of an objective that involves interest-rate
smoothing.
4.3
A Numerical Example
When κ > 0, no such simple analytical result is available. It might in this more general case
still be possible to support the optimal plan as an equilibrium outcome under discretion, if
a central-bank objective more complex than (4.1) were considered. We do not pursue this
here, but instead note that even with an objective in the simpler class (4.1), it is possible
to achieve quite a good approximation to the optimal pattern of responses to shocks, in the
60

case of plausible parameter values. We demonstrate this through numerical analysis of the
model, assuming the same “calibrated” parameter values as earlier.
Speciﬁcally, we assume that the parameters of the structural equations and the shock
process are as speciﬁed in Table 1. But we now assume a central-bank loss function of the
form (4.1), and consider how the time-consistent optimizing plan varies with the assumed
weights in that loss function. To begin, we shall assume that ˆλx = λx = .048 (the value in
Table 1), and consider only the consequences of variation in ˆλr and λ∆.
We ﬁrst note that the nonlinear equations referred to above do not always have a unique
solution for the coeﬃcients rr, rn, and so on. It can be shown that given a value for rr
consistent with these equations, a unique solution can be obtained, generically, for the other
coeﬃcients. However, rr solves a quintic equation, which equation may have as many as
ﬁve real roots. For example, Figure 7 plots the solutions to this equation, as a function
of ˆλr, in the case that λ∆= 0. One observes that there is a unique real root, rr = 0, in
the case of any ˆλr > 0.68 However, for ˆλr < 0, there are multiple solutions, and given the
results of the previous sub-section, we are interested in considering loss functions of this kind.
In the ﬁgure, solutions that also satisfy conditions (4.9) and (4.10), and so correspond to
stationary equilibria, are indicated by solid lines, while additional branches of solutions that
do not correspond to stationary equilibria are indicated by dashed lines.69 We observe that
while there exist multiple solutions to the nonlinear equations for all ˆλr < 0, there is still
a unique stationary equilibrium involving optimization under discretion for all ˆλr > −1.70
68The time-consistent solution characterized in section 3.2 refers to a case of this sort. In such a case,
the unique solution involves rr = πr = xr = 0, so that lagged interest rates have no eﬀect. This solution
obviously satisﬁes (4.9) and (4.10) as well, and so represents the unique stationary Markov equilibrium.
69Technically, because here λ∆= 0, the second-order condition is (weakly) satisﬁed even by solutions in
which rr < 0. But our real interest is not in the case λ∆= 0, but rather in the set of solutions that exist
for small positive values of λ∆. The solutions shown in Figure 7 with rr < 0 also correspond to solutions
with rr < 0 in the case of small positive λ∆, and under that perturbation these solutions cease to satisfy the
second-order condition. Hence we show these branches of solutions with dashed lines in Figure 7. The correct
statement would be that for any small enough value λ∆> 0, there exists a unique stationary equilibrium for
all ˆλr > −1. This identiﬁes the boundary of the white region in Figures 8-10, near the horizontal axis.
70It is interesting to note that for values of ˆλr below a critical value, approximately -0.02, the unique
stationary equilibrium no longer corresponds to the “minimum state variable solution”, i.e., the solution in
which lagged interest rates are irrelevant.
61

Only for even larger negative values do we actually have multiple time-consistent equilibria.
The same turns out to be true for λ∆> 0 as well, at least in the case of the moderate
values of λ∆that we shall consider here. (For very high values of λ∆> 0, not shown in the
ﬁgures below, there exist multiple equilibria even for higher values of ˆλr.) Note that our
time-consistent outcome is essentially a Nash equilibrium in a game played by successive
central bankers, rather than the solution to an optimization problem. Thus there is nothing
paradoxical about the possible existence of multiple solutions.
We turn now to a consideration of how the properties of the stationary time-consistent
equilibrium vary with the parameters ˆλr and λ∆. In each of Figures 8-10, the white region
indicates the set of loss function weights for which there is a unique stationary equilibrium
of the linear form characterized above. In this region, the contour lines plot properties of
this equilibrium. The grey region indicates weights for which there are multiple stationary
equilibria. Here we plot the values associated with the best of these equilibria, the one with
the lowest value of E[W]. As it turns out, the best equilibrium that is attainable corresponds
to weights in the white region, so that we do not have to face the question of whether one
should choose weights that are consistent with one good equilibrium but also with other bad
ones.
Figure 8 shows how the inertia coeﬃcient rr in representation (4.3) of the equilibrium
interest-rate dynamics varies with the loss function weights.
As one might expect, the
equilibrium inertia coeﬃcient increases as λ∆is increased, for any given value of ˆλr. At
the same time, for any given value of λ∆> 0, the inertia coeﬃcient also increases if ˆλr is
reduced. This continues to be true as ˆλr is made negative. Figure 9 shows the corresponding
equilibrium values of the coeﬃcient rn, describing the immediate interest-rate response to
an increase in the natural rate of interest. Increasing either ˆλr or λ∆lowers this response
coeﬃcient, at least in the region where both are positive, though the response is positive.
Figure 10 presents the corresponding contour plot for the true social loss measure E[W].
Four sets of policy weights are marked on this ﬁgure (as on the others). The X indicates the
weights in the true social loss function; but charging a discretionary central bank to minimize
62

this objective does not lead to the best equilibrium, even under this criterion. (These weights,
and properties of the resulting time-consistent equilibrium, are described in the ﬁrst line of
Table 3.) The large black dot instead indicates the weights that lead to the best outcome,
when one still restricts attention to central bank loss functions with no smoothing objective
(λ∆= 0).
This corresponds to a weight ˆλr that makes the time-consistent equilibrium
implement the optimal non-inertial plan, characterized earlier. (Compare the second line
of Table 3 with the ﬁfth line of Table 2.)
It involves a value ˆλr < λr, so that interest
rates respond more vigorously to variations in the natural rate of interest than occurs under
discretion when the central bank seeks to minimize the true social loss function.
The circled star (or wheel) instead indicates the minimum achievable value of E[W],
among time-consistent equilibria of this kind. These weights therefore solve the optimal
delegation problem, if we restrict ourselves to central-bank objectives of the form (4.1). As
in the limiting case solved explicitly above, the optimal weights involve λ∆> 0, ˆλr < 0.
(The optimal weights and the properties of the resulting equilibrium are described on the
fourth line of Table 3.) Finally, the star without a circle indicates the optimal equilibrium
that can be achieved subject to the constraint that ˆλr ≥0. (One might restrict attention
to these cases, if one does not think it would be easy to explain to a central bank that
it will be rewarded for creating interest-rate variability, while being punished for failing to
smooth interest-rate changes.) This point corresponds to a point of tangency between an
isoquant of E[W] and the vertical axis at ˆλr = 0 (though neither curve is drawn in the
ﬁgure). In this case, it is still desirable to direct the central bank to penalize large interest-
rate changes, though the optimal λ∆is smaller than if it were possible to choose ˆλr < 0.
(These constrained-optimal weights are shown on the third line of Table 3.)
In this exercise, we have assumed that the relative weight on output gap variability, ˆλx,
equals the weight in the true social loss function, λx, given in Table 1. In fact, consideration
of values ˆλx ̸= λx allows us to do no better, either in the case of loss functions with no
smoothing objective, or in the case of the fully unconstrained family. For the policy on the
second line of Table 3 already implements the optimal non-inertial plan, and the policy on the
63

fourth line already implements the optimal plan of the form given by equations (4.3) – (4.5).
This is not because ˆλx = λx is a uniquely optimal value in either case, but rather because
we can ﬁnd weights that support the optimal plan for an arbitrary value of ˆλx, so that the
constraint that ˆλx = λx has no cost. The structural equations (2.6) and (2.7) place four
restrictions upon the coeﬃcients (rr, rn, πr, πn, xr, xn), so that there is only a two-parameter
family of possible responses to shocks that are consistent with the structural equations. To
pick out the optimal member of this family, it suﬃces that one be able to freely vary two
parameters of the central bank loss function, such as ˆλr and λ∆. For example, it would also
be possible to impose the constraint that ˆλx = 0, so that there is no output-gap term in the
central bank loss function at all. The optimal weights in this case are given on the ﬁfth line
of Table 3. Note that again ˆλr < 0, λ∆> 0.
The only case in which it is of some beneﬁt to relax the requirement that the relative
weight on the inﬂation and output-gap terms in (4.1) are the same as in the true social loss
function is when we impose the constraint that all weights be non-negative. As noted above,
in this case the constraint that ˆλr ≥0 binds. But if we must set ˆλr = 0, the additional
degree of freedom allowed by varying ˆλx as well as λ∆does allow some improvement of the
time-consistent equilibrium, in general. In fact, for the numerical parameter values used
above, the optimal ˆλx is inﬁnite; that is, the relative weight on the inﬂation term is best
set to zero. To analyze this case, it is thus convenient to instead write the central bank loss
function as
Lcb
t = (xt −ˆx∗)2 + ˜λππ2
t + ˜λr(rt −ˆr∗)2 + ˜λ∆(rt −rt−1)2.
(4.16)
In terms of this alternative notation, the loss function described on the fourth line of Table
3 can instead be described as on the sixth line of the Table. We now consider the optimal
central bank of objective of the form (4.16), when we impose the constraint that ˜λr ≥0.
Figure 11 plots the value of E[W] in the time-consistent equilibrium, as a function of the
policy weights ˜λπ and ˜λ∆, in the case that ˜λr = 0. As in the earlier ﬁgures, the X marks the
weights in the true social loss function (corresponding to the ﬁrst line in Table 3). The star
without a circle again indicates the best attainable policy in this plane, under the constraint
64

that ˜λπ = 1/λx, the weight in the true social loss function. The star is at a point of tangency
between an E[W] isoquant and a vertical line at ˜λπ = 1/λx, and corresponds to the policy
described on the third line of Table 3. However, we observe that it is possible to reduce
E[W] by lowering ˜λπ, and the minimum value consistent with non-negative policy weights
(indicated by the wheel in the ﬁgure, and described on the seventh line of Table 3) involves
˜λπ = 0, so that a positive weight is assigned to output-gap stabilization, and none to inﬂation
stabilization.71 Note that this constrained-optimal central bank loss function again involves
˜λ∆> 0, so that it is desirable for the central bank to seek to smooth interest-rate changes.
How good an equilibrium can be achieved through optimal delegation of this kind? One
will recall from Table 2 that for these parameter values (the case ρ = .35 in that table), the
optimal policy achieves an expected loss of E[W] = 1.097, while the expected loss is more
than twice as large (E[W] = 2.547) under the time-consistent optimizing plan (assuming a
central bank that seeks to minimize the true social loss measure). However, the minimum
value of E[W] shown in Figure 10 is also equal to 1.097, to three signiﬁcant digits. Thus
more than 99.9 percent of the reduction in expected loss that is possible in principle, through
an optimal commitment, can be achieved through an appropriate choice of objective for a
discretionary central bank.72 The exact optimal pattern of responses could presumably be
supported as a time-consistent equilbrium if we were to consider more complex central bank
loss functions.
5
Optimal Interest-Rate Feedback Rules
We turn now to an alternative approach to implementation of the optimal pattern of re-
sponses to shocks. Here we ask what kind of policy rule would achieve that end, assuming
71Further insight into why it is optimal to set ˜λπ = 0 in this case may be provided by Figure 12, which
plots E[W] as a function of ˜λr and ˜λπ, ﬁxing ˜λ∆at the value shown on the sixth line of Table 3, i.e.,
the unconstrained optimal weight. The wheel again indicates the unconstrained optimal central bank loss
function. Under the constraint that ˜λr ≥0, however, the best attainable point in this plane is at the star,
corresponding to ˜λπ = ˜λr = 0.
72The equilibrium achieved in this way is also very similar in other respects, such as the other statistics
for the optimal plan reported in Table 2.
65

that the central bank commits itself to systematically conduct policy in this particular way,
and that the commitment is understood by and credible to the private sector. We shall
assume that the kind of characterization of optimal policy that is sought is a feedback rule
expressing the short-run nominal interest rate (the central bank’s instrument) as a func-
tion of current and lagged values of various variables that may be observed by the central
bank, and lagged values of the interest rate itself, as in the econometric studies mentioned
in the introduction. The question in which we are especially interested is the nature of the
dependence upon lagged interest rates in an optimal rule.
It is important to recognize that the question of optimal interest-rate inertia in this sense
is a distinct one from the question of the optimal response of interest rates to shocks taken
up in section 3. This is because a mere description of how one would like for the interest rate
to vary as a function of the history of shocks does not in itself uniquely identify a feedback
rule for the central bank that achieves this outcome.
We have obtained one description
of interest-rate dynamics under an optimal plan, given by equation (3.32). But this need
not be the central bank’s policy rule, since many other relations between interest rates and
other state variables are equally correct descriptions of a relation that should hold under
the optimal plan. If the variables in question are all part of the central bank’s information
set, then there is no reason not to suppose that another of these relations might equally well
represent an appropriate policy rule.
One might think that the relation (3.32) is a uniquely appropriate way of representing
optimal policy, since it is the unique relation that holds in equilibrium that involves only
the interest rate itself and exogenous states. However, there are two important reasons why
other relations satisﬁed by the nominal interest rate under the optimal plan may be of greater
usefulness as proposed policy rules. One is that other rules that are equally consistent with
the optimal equilibrium may require less information for implementation by the central bank.
Relation (3.32), if proposed as a policy rule, would require the central bank to determine at
each point in time the current value of the natural rate of interest. But as we shall see, it is
possible for the central bank to adopt a feedback rule that involves no explicit dependence
66

upon the natural rate, and so does not even require the central bank to know the value
of that variable, and yet results in the desired rational expectations equilibrium variation
of inﬂation and interest rates with disturbances to the natural rate. Under such a regime,
the central bank relies upon the private sector’s awareness of the current underlying state
variables to bring about the desired responses of endogenous variables to these states.
The second reason is that rules that are equally consistent with the optimal equilibrium
may not serve equally to uniquely determine the optimal plan as the equilibrium outcome.
This is because rational expectations equilibrium may be indeterminate under some interest-
rate feedback rules that include the optimal plan as one of the many possible equilibria. In
fact, the relation (3.32), if adopted as a rule for ﬁxing the central bank’s interest-rate target
each period, would have this unfortunate feature. But as we shall see, other relatively simple
feedback rules exist which result in a determinate equilibrium (in the sense that there is at
any rate a unique stationary equilibrium) which achieves the optimal plan. Such rules are
accordingly of greater interest as candidate monetary policy rules.
5.1
The Problem of Determinacy of Equilibrium
A fundamental issue in the evaluation of alternative policy rules in a rational expectations
equilibrium framework, when one’s structural model possesses forward-looking elements, is
the question of whether a proposed policy rule is associated with a determinate equilibrium
or not. Policy rules may easily be associated with very large sets of rational expectations
equilibria, and this problem of indeterminacy is an important reason for excluding certain
categories of rules from consideration.73 Sargent and Wallace (1975) famously argued for
money-supply rules as opposed to interest-rate rules for monetary policy on the ground
that interest-rate rules resulted in price-level indeterminacy. In fact, as McCallum (1981)
showed, this is not a problem of interest-rate rules as such, even in the context of the
particular rational expectations IS-LM model used by Sargent and Wallace. Rather, their
73See, e.g., Bernanke and Woodford (1997), Rotemberg and Woodford (1998), Clarida et al. (1998a),
Schmitt-Groh´e and Uribe (1999), Christiano and Gust (1999), and Woodford (1999a) for recent examples of
analyses of monetary policy rules that emphasize this issue.
67

result applies only to interest-rate rules that specify each period’s nominal interest rate as a
function solely of exogenous states. However, this particular result applies to our structural
model as well, and it explains why the law of motion (3.32) for the nominal interest rate is
not a suitable interest-rate rule through which to implement optimal policy.
Consider any policy rule in which the central bank’s instrument rt evolves exogenously.
We can represent such such a rule by an equation of the form
ˆrt = ξ′st,
(5.1)
where st is the vector of exogenous states that evolves according to (3.12), and ξ is a vector
of coeﬃcients. (Here we suppose that the vector st may be extended to include states that
are not needed to forecast the evolution of the natural rate of interest, but that matter for
the central bank’s setting of its instrument. In particular, we may now allow the vector st
to include lagged values of the interest rate itself, so that rules of the form (3.32) may be
given a representation of the form (5.1).) Then using (5.1) to substitute for rt in (2.7), our
structural equations take the form
Etzt+1 = ˆAzt + ˆast,
(5.2)
where
ˆA ≡
"
β−1
−β−1κ
−β−1σ−1
1 + κβ−1σ−1
#
,
ˆa ≡
"
0
σ−1(ξ′ −k′)
#
.
Given the signs assumed for β, σ, and κ, it is apparent that the matrix ˆA has two real
eigenvalues, satisfying
0 < λ1 < 1 < λ2.
The fact that one eigenvalue has modulus less than one, even though neither element of zt
is a predetermined variable, implies that rational expectations equilibrium is indeterminate
in this case. Speciﬁcally, for {zt} any bounded stochastic process satisfying (5.2), another
bounded solution is given by
z′
t = zt + vψt,
68

where v is the right eigenvector of ˆA associated with the eigenvalue λ1, and the stochastic
process ψt evolves according to
ψt+1 = λ1ψt + νt+1,
where νt+1 is any bounded random variable with mean zero that is unforecastable at date t,
and the initial condition ψ0 may be chosen arbitrarily. Note that the disturbances νt may be
of any amplitude,74 and may have any correlation with the “fundamental” disturbances ϵt.
Thus the system (5.2) admits a large multiplicity of bounded (or stationary) solutions, in-
cluding both solutions implying diﬀerent equilibrium responses to shocks to “fundamentals”
and solutions involving responses to “sunspot” states as well. Furthermore, these solutions
include equilibria involving arbitrarily large ﬂuctuations in the endogenous variables πt and
xt. Hence even if the rule is chosen (as in the case of (3.32)) to be consistent with the optimal
equilibrium, the set of rational expectations equilibria consistent with such a rule includes
equilibria that are very bad, from the point of view of the welfare criterion (2.8) – (2.9).
Thus such a rule does not represent a desirable way of implementing optimal policy.
5.2
An Optimal Simple Rule
The problem of indeterminacy of rational expectations equilibrium can be resolved through
suﬃciently strong feedback from endogenous variables, such as the inﬂation rate, the output
gap, or both.75
(Note that while McCallum (1981) stresses the role of feedback from a
“nominal anchor” in the resolution of the problem of price-level indeterminacy, no feedback
from any nominal variable is actually necessary, given the link between real and nominal
variables implied by our aggregate supply relation.) However, once we consider the possibility
of feedback from additional variables, there ceases to be a unique set of coeﬃcients for the
policy rule that is consistent with the optimal equilibrium. Even when we add the additional
74This is subject, of course, to the caveat that our log-linear approximation to the structural equations
may break down in the case of ﬂuctuations that are too large.
75Because our system of structural equations (2.6) – (2.7) involves only these two endogenous variables,
in addition to the interest rate itself, we consider only rules involving feedback from these variables here.
Consideration of the eﬀects of feedback from other variables would require that we adjoin to our model
additional equations for determination of those variables.
69

requirement that the policy rule support the optimal plan as the unique bounded rational
expectations equilibrium, the set of policies that satisfy this requirement will be large, since
the additional requirement of determinacy adds only a set of inequality constraints that the
coeﬃcients must satisfy.
This allows us to consider additional desiderata in choosing a policy rule. An additional
criterion of considerable practical interest is minimization of the information required in
order for the central bank to implement the rule in question. From this point of view, a
rule that involves feedback only from the inﬂation rate (i.e., involving no dependence upon
either exogenous states or the output gap) is especially desirable, since it can be implemented
without the central bank having to possess good estimates of the current values of either
the natural rate of interest or the natural rate of output. The uniquely minimal information
requirements of such a rule favor both accuracy of implementation and transparency, so that
the chances are greatest that the private sector will be able to correctly anticipate future
monetary policy. A rule that is purely backward-looking, responding only to inﬂation that
has already occurred rather than to forecasts of future inﬂation (whether those of the central
bank itself or of outside parties) is also advantageous on these same grounds.
As an illustration of these principles, let us consider policy rules within the simple family
ˆrt = θˆrt−1 + φπˆπt + φxˆxt + φnrn
t .
(5.3)
Note that this family includes the sort of generalized “Taylor rule” with partial-adjustment
dynamics described by equations (1.1)–(1.2), though we shall not necessarily assume that
θ < 1, as would be required by the partial-adjustment interpretation. We also allow for the
possibility of direct feedback from an observation of the current natural rate of interest, if
available. For simplicity, we also again assume a ﬁrst-order autoregressive process (3.15) for
the natural rate of interest. Our complete set of structural equations then consists of (2.6)
– (2.7), (3.15), and (5.3).
This system (setting aside the equation for the exogenous dynamics of the natural rate)
70

can be written in matrix form as
"
Etzt+1
ˆrt
#
=
" ˆA
−θa
φ′
θ
# "
zt
ˆrt−1
#
+
"
ˆa
φn
#
rn
t ,
(5.4)
where φ′ ≡[φπφx] is the row vector of coeﬃcients indicating the policy feedback from the
endogenous variables zt, ˆA is a 2×2 matrix the elements of which depend upon the coeﬃcients
φ,76 a is the vector that also appears in (3.11), and ˆa ≡(1 −φn)a. Because there is one
predetermined endogenous variable (ˆrt−1), the system (5.4) has a unique bounded solution
if and only if exactly two eigenvalues of the 3 × 3 matrix lie outside the unit circle. The
conditions for this to obtain imply a set of inequalities that the coeﬃcients φπ, φx and θ
must satisfy (that also involve the structural parameter β, σ, and κ.
We shall not here
develop these conditions, but we note that for any value |θ| < 1, the required conditions are
violated for all φ in a neighborhood of zero, as we should expect from our above analysis of
an exogenous interest-rate target.77 We also note that a suﬃcient condition for determinacy
is that φπ, φx, θ ≥0, and that
φπ + θ > 1.
(5.5)
This last condition expresses the “Taylor principle” that if inﬂation persists at a level above
its long-run target level for a suﬃcient period of time, the interest rate is eventually raised
by more than the amount by which inﬂation exceeds its target level.
In the case that equilibrium is determinate, we shall again be able to solve for the
non-predetermined endogenous variables zt as a linear function of the predetermined and
exogenous state variables rt−1 and rn
t . (Here we use the assumption that rn
t is Markovian, so
that the only relevant exogenous state is rn
t .) It then follows from (5.3) that ˆrt will also be
a linear function of the same two variables. Thus the equilibrium dynamics are necessarily
of the form (4.3) – (4.5). It follows that at best, a rule within the family (5.3) may be
76Note that this matrix reduces to the matrix ˆA in (5.2) in the case that the coeﬃcients of the policy rule
are φ = 0, and to the matrix A in (3.11) in the case that the coeﬃcients φ are those of (3.10).
77Note that when φ = 0, the eigenvalues of the matrix in (5.4) reduce to the two eigenvalues of ˆA,
characterized in section 5.1, and θ.
As one eigenvalue of ˆA satisﬁes 0 < λ1 < 1, there are too many
eigenvalues inside the unit circle for determinacy. By continuity, the same is true for all coeﬃcients φ in a
neighborhood of zero.
71

chosen so as to achieve the optimal pattern of responses to shocks among those that can be
described by partial-adjustment dynamics of this form. But we have seen earlier, in sections
3.5 and 3.6, that partial-adjustment dynamics of this kind can be found that approximate
the optimal impulse responses reasonably well, as long as κ is small.
Furthermore, we
have already identiﬁed the optimal responses from among this family, as they are the ones
associated with the time-consistent equilibrium when the policy weights in the central bank
loss function (4.1) are chosen optimally (that is, the responses in the equilibria described in
lines 4 – 6 of Table 3). Thus we turn to the question of whether a feedback rule of the form
(5.3) can be found that achieves this near-optimal pattern of responses as a determinate
equilibrium.
The near-optimal pattern of responses described by the coeﬃcients (rr, rn, πr, πn, xr, xn)
is consistent with the policy rule (5.3) if and only if the coeﬃcients of the rule satisfy two
linear restrictions:
rr = θ + φππr + φxxr,
(5.6)
rn = φππn + φxxn + φn.
(5.7)
Thus there will be a two-parameter family of such rules, each of which is equally consistent
with the desired equilibrium.
We could, of course, obtain a unique selection from this two-parameter family by stipulat-
ing that φπ = φx, so that there is no feedback from endogenous variables. But in this case, we
have seen that the conditions for determinacy of equilibrium will not be met. On the other
hand, imposing the requirement of determinacy does not in itself result in a unique selection,
because this only imposes additional inequality constraints. Thus there remain, in general,
a set of equally satisfactory rules corresponding to an open subset of the two-dimensional
linear space of coeﬃcients that satisfy (5.6)–(5.7).
A further possible criterion for a desirable policy rule, as mentioned above, is that it
require less information for the central bank to implement it. In the case of the family of
rules (5.3), the central bank can implement the rule without having to observe the current
exogenous disturbances rn
t and yn
t if and only if φx = φn = 0. (We assume here that the
72

bank can observe inﬂation and output, but that it cannot observe the current value of the
output gap without also being able to observe the current natural rate of output.) This
criterion thus provides two more linear restrictions upon the coeﬃcients of the policy rule,
suﬃcient to identify a unique rule that is both consistent with the desired equilibrium and
implementable without any need to observe the exogenous shocks directly. The unique rule
of this kind is a rule of the form
ˆrt = θˆrt−1 + φπˆπt,
(5.8)
with coeﬃcients
θ = rr −rn
πr
πn
,
φπ = rn
πn
.
(5.9)
In the case of parameter values like those investigated in section 3.5, the optimal impulse
responses to ﬂuctuations in the natural rate of interest are well approximated by partial-
adjustment dynamics with coeﬃcients
0 < rn < 1,
0 < rr < 1,
πn > 0,
πr < 0.
This is because the nominal interest rate adjusts gradually toward a moving target that is an
increasing function of (but moves less than proportionally with) the natural rate of interest;
while the inﬂation rate increases at the time of a positive innovation in the natural rate, but
subsequently undershoots its long-run level. In such a case, the coeﬃcients (5.9) satisfy
φπ > 0,
θ > rr.
Such a rule results in a determinate rational expectations equilibrium, involving the desired
near-optimal pattern of responses to shocks, if the coeﬃcients φπ and θ are not just positive,
but large enough to satisfy (5.5). In fact, for empirically realistic parameter values, each
coeﬃcient is likely to be greater than one on its own, so that the determinacy condition is
easily satisﬁed.
Thus we again conclude that intrinsic inertia in interest rates is justiﬁed, here measured
by the positive coeﬃcient θ in the feedback rule (5.8). In fact, we ﬁnd not only that a
73

positive θ is called for, but one greater than rr. Thus the degree of intrinsic inertia that
should be incorporated into a feedback rule of this kind is even greater than the degree of
inertia previously determined to be optimal in the dynamic response of the interest rate to
exogenous disturbances. The reason is that under a policy of the kind described by (5.8),
the central bank does not respond directly to exogenous disturbances, but instead reacts
to them only indirectly, as a result of their eﬀects upon inﬂation. In this case, there is an
additional reason for the interest rate at any time to be an increasing function of the previous
period’s interest rate, apart from the desire for inertia in the response to variations in the
natural rate. This is that the disturbance to the natural rate of interest that can be inferred
from any given level of inﬂation is higher if nominal interest rates have been higher in the
recent past. This is because, in equilibrium, higher nominal interest rates are followed by
lower inﬂation; so the degree of exogenous inﬂationary pressure that can be inferred from
any given level of current inﬂation is higher in the case that interest rates have recently been
high.78
Note that the same would be true of the output gap, if it were observed by the central bank
and used as an indicator of inﬂationary pressures. In the optimal equilibrium, the output
gap ﬁrst increases in response to an increase in the natural rate (the direct eﬀect xn > 0),
but subsequently undershoots its long-run value as a result of the tightening of monetary
policy (xr < 0). This would imply that if we seek to achieve the optimal equilibrium through
any feedback rule with φn = 0, and with φπ and φx of the same sign, we would need to use
a rule with φπ, φx > 0 (as proposed by Taylor), and with θ > rr. (The conclusion that
φπ, φx must both be positive if they have the same sign follows directly from (5.7), if the
desired equilibrium involves πn, xn > 0. The conclusion that θ > rr then follows from (5.6),
78Note that this argument has nothing to do with the idea that the disturbances to the natural rate are
themselves serially correlated, so that evidence of a high natural rate in the recent past leads one to infer a
higher current natural rate. For even in the case that ρ = 0, we have seen that the optimal impulse responses
involve an initial increase in inﬂation followed by subsequent undershooting, so that also in this case the
optimal coeﬃcients satisfy θ > rr > 0. In the present case, the current value of the natural rate can be
perfectly inferred from observations of inﬂation, so there is no need to use estimates of the natural rate in
the past to infer the current value. In the more realistic case, in which observations of current conditions do
not suﬃce to fully reveal the state of the economy, the argument suggested above can be a further reason
for an optimal interest-rate feedback rule to be inertial, as shown by Aoki (1998).
74

given that the desired equilibrium involves πr, xr < 0.) Thus the conclusion that a desirable
feedback rule involves θ > rr does not depend upon the exclusive use of inﬂation itself as an
indicator of underlying inﬂationary pressures.
In fact, the degree of inertia indicated by estimated central bank reaction functions
is typically greater than the optimal degree of intrinsic inertia in the response to shocks
computed above (an inertia coeﬃcient rr of less than .5, at the quarterly frequency, for our
calibrated parameter values). But given that such reaction functions respond to endogenous
indicators of inﬂationary pressure, such as inﬂation and output, rather than to exogenous
disturbances directly, it is in fact optimal for them to involve inertia coeﬃcients greater than
the value of rr.
Indeed, if anything, the degree of inertia implied by estimated reaction functions is less
than would be indicated as optimal on the grounds considered here. This can be illustrated
in an especially dramatic way by considering the properties of the equilibria associated with
rules of the form (5.8), for alternative values of φπ and θ. Figures 13-16 describe the numerical
solution for the stationary rational expectations equilibrium associated with such a feedback
rule, in the case of the parameter values given in Table 1, including the speciﬁcation ρ = .35.
In each of these ﬁgures, the set of coeﬃcients for which rational expectations equilibrium is
indeterminate is indicated by the grey region. Note that in the non-negative orthant (the
region of these ﬁgures of primary interest to us), the condition for determinacy is given by
(5.5), as noted above.79
In the zone of determinacy, the ﬁgures display contour plots for the statistics V [π], V [x],
V [r], and E[W]. One observes that from the point of view of stabilization of inﬂation and
of the output gap alone, there is no advantage to rules with θ ̸= 0; the greatest degree of
stabilization occurs if φπ is made as large as possible, but in the case of a suﬃciently large
value of φπ, the variability of both target variables is minimized by choosing θ = 0. However,
a rule with θ > 0 results in less volatile short-term interest rates in equilibrium; in fact, for
79The same condition applies in the more complicated model of Rotemberg and Woodford (1998). See the
corresponding ﬁgures in that paper.
75

given φπ > 0, the variability of the nominal interest rate is minimized by choosing θ as large
as possible. Minimization of our overall loss criterion E[W] involves a compromise between
these two objectives; it is optimal to choose large positive (but ﬁnite) values for both φπ
and θ. For the parameter values used here, the loss-minimizing policy rule coeﬃcients are
φπ = 46.1 and θ = 13.0.
This value of θ implies a great deal of inertia indeed in the rule used by the central bank
to set interest rates. The optimal value turns out to be decreasing in the assumed coeﬃcient
of autocorrelation of the natural rate of process. But for any value of ρ, the optimal rule
within the family (5.8) is a “super-inertial” one with θ > 1.80
5.3
A Feedback Rule that Implements the Optimal Plan
We now turn brieﬂy to the question of designing an interest-rate feedback rule that can im-
plement exactly the optimal pattern of responses to shocks described in section 3. As above,
there will be many feedback rules that equally share the property of having a determinate
rational expectations equilibrium that corresponds to the optimal plan. Rather than trying
to characterize all such rules, we shall we restrict our attention here to rules that involve
feedback only from the inﬂation rate, and from past values of the interest rate itself, i.e.,
rules of the form
A(L)ˆrt = B(L)ˆπt,
(5.10)
where A(L) and B(L) are two ﬁnite-order polynomials in the lag operator.
The degree
to which such a rule involves intrinsic interest-rate inertia of the kind discussed in the in-
troduction is indicated by the lag polynomial A(L), and in particular by the roots of the
characteristic polynomial
A(µ−1) = 0.
(5.11)
As in the simpler case just considered, there is no simple relation between the form of the
lag polynomial A(L) in the feedback rule (5.10 and that of the lag polynomial Q(L) in
80See Giannoni (1999) for further discussion of how the optimal simple rule depends upon model parame-
ters, and for an analysis of “robust” optimal policy taking account of parameter uncertainty. Giannoni ﬁnds
that in the case of parameter uncertainty the robust-optimal simple rule involves an even larger value of θ.
76

(3.32) describing how interest rates evolve in response to shocks, in the stationary rational
expectations equilibrium associated with such a policy rule. In particular, a “super-inertial”
policy, in which A(µ−1) has a root larger than one, may nonetheless be consistent with a
stationary rational expectations equilibrium, even though stationarity implies that all roots
of Q(µ−1) must lie within the unit circle.
We again restrict attention to the case of a natural rate process described by (3.15). In
this case, the vector of endogenous variables qt ≡[ˆrt ˆπt]′ that enter the monetary policy rule
(5.10) evolve according to a law of motion of the form
qt = Hφt−1 + hrn
t
(5.12)
under the optimal plan, while the Lagrange multipliers evolve according to
φt = Nφt−1 + nrn
t .
(5.13)
Here N is the same matrix as in (3.29) and (3.31), while n is the column vector deﬁned by
n ≡−C
∞
X
j=0
ρj ˜A−(j+1)a.
The ﬁrst row of H is given by the row vector p′ from (3.30), and the second row is given by
the ﬁrst row of the matrix G in (3.28). Finally, the column vector h is deﬁned by
h ≡−
"
q′
e′
1
#
∞
X
j=0
ρj ˜A−(j+1)a,
where q′ is the row vector in (3.30), and we use ei to denote the ith unit vector (i.e., the
vector whose ith element is one, and all other elements zero).
A ﬁrst question is then whether there exists a relation of the form (5.10) such that this
relation holds at all times if the vector qt evolves according to (5.12) – (5.13). It can be shown
that the answer is yes, and that the lowest-order polynomials81 for which this is possible are
a second-order polynomial A(L) and a ﬁrst-order polynomial B(L). It is furthermore shown
81Obviously, for any polynomials A(L) and B(L) with this property, the polynomials ˜A(L) ≡C(L)A(L)
and ˜B(L) ≡C(L)B(L) will also have the property, where C(L) is any lag polynomial whatsoever. But the
latter, higher-order polynomials represent simply a more complex description of an equivalent policy rule.
77

that there is a unique such relation with polynomials of this order; speciﬁcally, it is the
unique such relation in which neither A(L) nor B(L) is of order greater than two. This
relation can be written in the form
2
X
j=0
v′
jqt−j = 0,
(5.14)
where the three vectors of coeﬃcients v′
j are given by
v′
0
=
e′
1R−1,
v′
1
=
−e′
1R−1HPQ−1,
v′
2
=
e′
1R−1H[PQ−1 −NH−1]HNH−1,
and
P ≡[n
Nn −N2H−1h],
Q ≡[h
Hn −HNH−1h],
R ≡[e1
h].
As one can show furthermore that this deﬁnition implies that v′
2e2 = 0, the polynomials
A(L) and B(L) implied by (5.14) are indeed of the asserted order.
There is thus a relation of the desired form that is consistent with the optimal pattern of
responses of inﬂation and interest rates to disturbances to the natural rate. It remains for
us to determine whether imposition of (5.14) as a policy rule would result in a determinate
equilibrium. The algebraic conditions that determine this are rather complex, but numerical
investigation indicates that, at least in the case of parameters in the area of those listed
in Table 1, the conditions for determinacy are satisﬁed by this rule. Thus we have found
a policy rule that is not only consistent with the optimal equilibrium responses to shocks,
but also satisﬁes both of our additional desiderata: its implementation does not require the
central bank to observe the current values of the natural rates of interest and output, and it
results in a determinate equilibrium.
What does the form of this optimal interest-rate feedback rule indicate about the desir-
ability of interest-rate inertia of the kind indicated by the empirical studies summarized in
the introduction? Our characterization here of the optimal form of the lag polynomial A(L)
in (5.10) is arguably more relevant for that question than our previous characterization of
78

the optimal form of the lag polynomial Q(L) in (3.32), since a number of the studies referred
to seek to estimate an explicit interest-rate feedback rule intended to represent systematic
Fed policy. It is thus of particular interest to note that (5.14) implies that the coeﬃcients
on the lags in A(L) should again be substantial in magnitude.
Indeed, for plausible parameter values, these coeﬃcients imply an even greater degree of
interest-rate inertia than was suggested by the coeﬃcients on the lags in Q(L). Again, it is
useful to consider the roots of the characteristic polynomial (5.11). For example, in the case
of the parameter values given in Table 1, and our baseline natural-rate process with ρ = .35,
the optimal rule (5.8) takes the form
A(L) = 1−12.9L+8.3L2 = (1−12.2L)(1−.68L),
B(L) = 42.6−27.8L = 42.6(1−.65L).
The roots of (5.11) are thus 12.2 and .68; the larger of these is very large indeed.
Furthermore, it is clearly the larger root, in this case, that mainly determines the degree
of interest-rate inertia implied by the speciﬁcation (5.10). For one observes that A(L) and
B(L) are close to having a common factor (1 −.65L); thus, for these parameter values,
(5.10) can be approximated by a rule of the simpler form (5.8), with coeﬃcients φπ = 42.6,
θ = 12.2. (Note that these coeﬃcients are close to the ones found above to be optimal among
rules of that class.) Thus, as concluded earlier, a simple rule of that form provides a good
approximation to an optimal policy.
5.4
Discussion
This same conclusion – that the optimal policy rule involves an autoregressive polynomial
with a largest root that is even greater than one – also obtains in the more complex model
studied by Rotemberg and Woodford (1998). In that model, there are two independent
types of innovations each period to the state vector st that describes current information
about the future evolution of the IS and AS disturbances. (The two orthogonal shocks are
identiﬁed in the U.S. data with two diﬀerent orthogonal innovations from a tri-variate VAR.)
An optimal plan involves interest-rate responses to each of these kinds of news, and as a
79

result feedback from the current inﬂation rate alone, along with lagged variables, does not
allow a suﬃciently ﬂexible class of responses to include one that achieves the exact optimal
plan. However, it is still possible to ﬁnd a policy rule that supports the optimal plan, and
that does not require the central bank to observe the current values of any of the exogenous
shocks for its implementation. This rule is of the form
A(L)ˆrt = B(L)ˆπt + C(L)ˆyt,
where ˆyt represents the log of detrended real output, rather than the output gap. Rotemberg
and Woodford ﬁnd that for the parameter values associated with their estimated model, the
characteristic equation (5.11) has a largest root µ = 1.33; this is less explosive than the
optimal lag polynomial in the calculations just reported, but it is explosive nonetheless.
The presence of an autoregressive root greater than one means that in the case of arbitrary
bounded ﬂuctuations in inﬂation, interest-rate determination according to (5.10) would in
general imply explosive ﬂuctuations in the interest rate, that would not remain forever within
any ﬁnite bounds. However, this does not mean that in the rational expectations equilibrium
associated with such a rule, interest rates will be highly volatile. Instead, the stationary
equilibrium associated with this rule involves a lower variance of the stationary distribution
of nominal interest rates than is associated, for example, with the time-consistent optimizing
policy, or with the optimal non-inertial policy, as shown in Table 2. This is because, in
equilibrium, the anticipation that interest rates will be set according to (5.10) results in
inﬂation ﬂuctuations that keep nominal interest rates from exploding, or even from deviating
very far from their steady-state level.
An unexpected inﬂationary shock (an unexpected increase in the natural rate of interest)
requires some initial increase in the level of nominal interest rates. But it does not imply
further explosive growth of interest rates in subsequent quarters, because inﬂation falls, and
indeed undershoots its long-run level, after its initial small increase. Given this undershoot-
ing, the policy rule (5.10) allows the nominal interest rate to converge back to its normal
level after a few quarters. The inﬂation reduction occurs, in equilibrium, because if demand
80

did not decline enough, and price increases were not moderated enough, to achieve this, the
private sector would have to expect steep interest-rate increases a few quarters in the future,
and that expectation would justify sharper reductions of demand and of price increases. The
fact that the rule requires this to occur in equilibrium, of course, is exactly what makes it
an optimal policy, since as we saw in section 3, an optimal plan would arrange for that to
occur, in order to reconcile low inﬂation variability with low interest-rate variability.
Conﬁdence that the private sector will in fact adopt spending and pricing behavior that
keeps the economy on a non-explosive path, as in the stationary rational expectations equi-
librium, depends, of course, upon the credibility of the central bank’s commitment to the
inertial rule. A consideration of what kind of rule would be optimal in the case that the rule
is not expected to be perfectly credible, or if the private sector is expected to learn about
the new regime only over time, is beyond the scope of the present study. However, it is
worth noting that “super-inertial” rules need not produce such dramatically bad outcomes,
even if the behavioral assumptions of our forward-looking model are incorrect, as is sug-
gested by exercises like that of Rudebusch and Svensson (1998). These authors substitute
a super-inertial interest-rate feedback rule, found to have desirable properties in the model
of Rotemberg and Woodford (1998) for reasons essentially the same as those analyzed here,
into a backward-looking structural model (not derived from optimizing behavior), and ﬁnd
that it results in inﬁnite variances, and hence a worse outcome than would be associated
with other, less inertial rules.
This might make it seem that a concern for “robustness” should make one avoid super-
inertial rules, simply because they lead to extremely bad outcomes under some possible
assumptions (Taylor, 1998). However, it is important to note that the inﬁnite variances
result only if the rule is taken to apply, with constant coeﬃcients, no matter how extreme
the levels of inﬂation and interest rates may have become. The desirable properties of the
rule in the model considered here, by contrast, depend only upon a commitment to apply the
rule in the case of ﬂuctuations in inﬂation and interest rates over bounded intervals, the range
over which these variables ﬂuctuate in the stationary rational expectations equilibrium. One
81

could modify the rule outside these intervals (for example, specifying that interest rates will
never fall below a certain ﬂoor, or rise above a certain ceiling, no matter what the history
of inﬂation and interest rates may be), and still obtain the same prediction of a determinate
rational expectations equilibrium with the desirable properties analyzed above. Thus, while
the question of the robustness of our results to model uncertainty is certainly an important
one,82 it seems premature to judge that super-inertial rules as such can be excluded from
consideration.
It is clear that the particular numerical coeﬃcients derived above for an optimal feedback
rule do not deserve much emphasis, even if the model were viewed as a reasonable approx-
imation of the U.S. economy. For these coeﬃcients – for example, the optimal (φπ, θ) in a
rule of the form (5.8) – are quite sensitive to relatively small changes in the speciﬁcation of
the model. This is shown by a comparison of our results here with those of Rotemberg and
Woodford (1998) for the same class of policy rules, despite the fact that we have “calibrated”
the simpler model used here to resemble theirs to the extent possible. One can also show
that even within the context of the model as speciﬁed here, the optimal values of φπ and θ
are quite sensitive to variation in the assumed values of structural parameters such as κ and
σ.
The reason for this fragility is not too hard to see. In section 5.2 above, we have shown
how a rule of the form (5.8) may be consistent with equilibrium interest-rate responses of the
desired sort, which involve partial adjustment of the short nominal rate toward an increasing
function of the current natural rate.
But this depends, essentially, upon responding to
current inﬂation and past interest rates in a way that responds appropriately to the level
of the current natural rate of interest that can be inferred from those endogenous variables.
The problem with such a strategy for monetary policy is that, in a near-optimal equilibrium,
inﬂation does not respond much to an innovation in the natural rate (Figure 4), and so it is a
poor indicator of the underlying pressures that monetary policy should respond to.83 Because
82See Hansen and Sargent (1999) for an analysis of this question in the case of one particular description
of the possible speciﬁcation error.
83The problem is related to the problem discussed in Bernanke and Woodford (1997), that arises when
82

inﬂation increases by only a small amount in response to such a shock, the optimal feedback
rule must respond to observed inﬂation variations with an extremely large coeﬃcient. And,
because it is necessary to correct for the amount that one would have expected inﬂation to
decline in the absence of such a shock, which is an increasing function of the lagged interest
rate, the lagged interest rate must receive an extremely large coeﬃcient as well.
This is nonetheless a desirable feedback rule, under the assumption that the signal con-
tained in variations in current inﬂation, while weak, is perfectly observed, so that one need
only amplify the signal by responding very strongly to it. Indeed, in the absence of other
indicators of changes in the natural rate of interest, it is the best that one can do. But it is
clearly unrealistic, in practice, to assume that the relevant inﬂation variable is observed with
complete precision, especially in real time.84 At the same time, other relevant information is
available, including estimates of the current output gap (the other relevant variable in our
simple model), that, while possibly subject to greater uncertainty than estimates of current
inﬂation, surely contain additional information. We do not here take up the question of
how the optimal feedback rule is aﬀected by taking account of such noise in the information
available to the central bank.85 But it seems likely that under a more realistic speciﬁcation
of available information, less weight would be put on the recent rate of inﬂation, and more
on other indicators that, like the output gap in our simulations above, respond more to in-
novations in the natural rate in a desirable equilibrium. This is likely to considerably reduce
the desired size of the inertia coeﬃcient θ.
Nonetheless, our basic argument for a value of θ in excess of rr would seem likely to
extend to the more general setting. For this depends solely upon the fact that the endogenous
variable that is used as an indicator of exogenous inﬂationary pressures will tend to ﬁrst rise
in response to such pressures, but later fall as a result of the tightening of monetary policy
that occurs in a desirable equilibrium. Thus the degree of policy inertia implied by estimated
an inﬂation forecast is used as an indicator of the real disturbances, despite the fact that successful policy
should large stabilize forecastable inﬂation.
84Orphanides (1997) documents the degree of error contained in real-time estimates of the current rate of
inﬂation available to the Federal Open Market Committee in its deliberations.
85See Aoki (1998) for a treatment of related issues in a forward-looking model similar to that used here.
83

Fed reaction functions like that of Sack (1998b) seems unlikely to be greater than can be
justiﬁed as part of an optimal policy commitment. Indeed, it is possible that a more detailed
analysis would still conclude, like the simple treatment above, that current U.S. policy is
not even inertial enough. Our ﬁnding that even a “super-inertial” autoregressive polynomial
may be optimal shows how wrong it is to assume that evidence of inertial behavior provides
prima facie evidence of incompetence.
84

References
Aoki, Kosuke, “On the Optimal Monetary Policy Response to Noisy Indicators,” unpub-
lished, Princeton University, November 1998.
Backus, David, and John Driﬃll, “The Consistency of Optimal Policy in Stochastic
Rational Expectations Models,” CEPR discussion paper no. 124, August 1986.
Barro, Robert J., and David B. Gordon, “A Positive Theory of Monetary Policy in a
Natural Rate Model,” Journal of Political Economy 91: 589-610 (1983).
Bernanke, Ben S., and Michael Woodford, “Inﬂation Forecasts and Monetary Policy,”
Journal of Money, Credit, and Banking, 24: 653-84 (1997).
Blanchard, Olivier J., and Charles Kahn, “The Solution of Linear Diﬀerence Equations
under Rational Expectations,” Econometrica 48: 1305-1311 (1980).
Blinder, Alan S., Central Banking in Theory and Practice, Cambridge: M.I.T. Press,
1998.
Calvo, Guillermo, “Staggered Prices in a Utility-Maximizing Framework,” Journal of
Monetary Economics, 12: 383-98 (1983).
Caplin, Andrew, and John Leahy, “Monetary Policy as a Process of Search,” American
Economic Review 86: 689-702 (1996).
Christiano, Lawrence J., and Christopher J. Gust, “Taylor Rules in a Limited Participa-
tion Model,” NBER working paper no. 7017, March 1999.
Clarida, Richard, Jordi Gal´i and Mark Gertler,“Monetary Policy Rules and Macroeco-
nomic Stability: Evidence and Some Theory,” NBER working paper no. 6442,
March 1998a.
—- —-, —- —- and —- —-, “Monetary Policy Rules in Practice: Some International
Evidence,”European Economic Review 42:1033-1068 (1998b).
—- —-, —- —- and —- —-, “The Science of Monetary Policy,” Journal of Economic
Literature, forthcoming 1999.
Cook, Timothy, and Thomas Hahn, “The Eﬀect of Changes in the Federal Funds Rate
Target on Market Interest Rates in the 1970s,” Journal of Monetary Economics 24:
331-352 (1989).
85

Currie, David, and Paul Levine, Rules, Reputation and Macroeconomic Policy Coordi-
nation, Cambridge: Cambridge University Press, 1993.
Fair, Ray C., “The Sensitivity of Fiscal Policy Eﬀects to Assumptions about the Behavior
of the Federal Reserve,” Econometrica 46: 1165-1179 (1978).
—- —-, “An Analysis of a Macro-Econometric Model with Rational Expectations in the
Bond and Stock Markets,” American Economic Review 69: 539-552 (1979).
—- —-, and E. Philip Howrey, “Evaluating Alternative Monetary Policy Rules,” Journal
of Monetary Economics 38: 173-193 (1996).
Friedman, Milton,“The Role of Monetary Policy,” American Economic Review 58: 1-17
(1968).
—- —-, “The Optimum Quantity of Money,” in The Optimum Quantity of Money and
Other Essays, Chicago: Aldine, 1969.
Fuhrer, Jeﬀrey C. and Geoﬀrey Moore, “Monetary Policy Trade-oﬀs and the Correlation
between Nominal Interest Rates and Real Output,” American Economic Review
85: 219-239 (1995).
Gali, Jordi, and Mark Gertler, “Inﬂation Dynamics: A Structural Econometric Analysis,”
unpublished, New York University, August 1998.
Giannoni, Marc, “Does Model Uncertainty Justify Caution? Robust Optimal Monetary
Policy in a Forward-Looking Model,” unpublished, Princeton University, June 1999.
Goodfriend, Marvin, “Interest Rate Smoothing in the Conduct of Monetary Policy,”
Carnegie-Rochester Conference Series on Public Policy, Spring 1991, 7-30.
Goodhart, Charles A. E., “Why Do the Monetary Authorities Smooth Interest Rates?”
Special Paper no. 81, LSE Financial Markets Group, February 1996.
—- —-, “Central Bankers and Uncertainty,” Keynes Lecture, British Academy, October
29, 1998.
Guthrie, Graeme, and Julian Wright, “The Optimal Form of Interest-Rate Targeting,”
unpublished, University of Auckland, December 1998.
Hansen, Lars P., Dennis Epple, and William Roberds, “Linear-Quadratic Duopoly Mod-
els of Resource Depletion,” in T.J. Sargent, ed., Energy, Foresight and Strat-
egy,Washington: Resources for the Future, 1985.
86

Hansen, Lars P., and Thomas J. Sargent, “Robustness and Commitment: A Monetary
Policy Example,” unpublished, Stanford University, March 1999.
Kerr, William, and Robert G. King, “Limits on Interest Rate Rules in the IS Model,”
Economic Quarterly, Federal Reserve Bank of Richmond, Spring 1996, pp. 47-76.
King, Robert G., and Alexander L. Wolman, “Inﬂation Targeting in a St. Louis Model of
the 21st Century,” Federal Reserve Bank of St. Louis Review 78(3): 83-107 (1996).
—- —- and —- —-, “What Should the Monetary Authority do When Prices are Sticky?”
unpublished, University of Virginia, April 1998.
Kiley, Michael T., “Monetary Policy under Neoclassical and New-Keynesian Phillips
Curves, with an Application to Price Level and Inﬂation Targeting,” FEDS discus-
sion paper no. 1998-27, May 1998.
Kydland, Finn E., and Edward C. Prescott, “Rules Rather than Discretion: The Incon-
sistency of Optimal Plans,” Journal of Political Economy 85: 473-491 (1977).
—- —- and —- —-, “Dynamic Optimal Taxation, Rational Expectations and Optimal
Control,” Journal of Economic Dynamics and Control 2: 79-91 (1980).
Levin, Andrew, Volker Wieland, and John C. Williams, “Robustness of Simple Monetary
Policy Rules under Model Uncertainty,” NBER working paper no. 6570, May 1998.
Levine, Paul, “Should Rules be Simple?” CEPR discussion paper no. 515, March 1991.
[Reprinted as chapter 6 of Currie and Levine (1993).]
Lucas, Robert E., Jr., “Econometric Policy Evaluation: A Critique,” Carnegie-Rochester
Conference Series on Public Policy,1, 1976, 19-46.
Mankiw, N. Gregory, “The Optimal Collection of Seignorage: Theory and Evidence,”
Journal of Monetary Economics 20: 327-341 (1987).
McCallum, Bennett T., “Price Level Determinacy with an Interest Rate Policy Rule and
Rational Expectations,” Journal of Monetary Economics 8: 319-329 (1981).
—- —-, “Issues in the Design of Monetary Policy Rules,” in J.B. Taylor and M. Wood-
ford, eds., Handbook of Macroeconomics, Amsterdam: North-Holland, forthcoming
1999.
—- —-, and Edward Nelson, “An Optimizing IS-LM Speciﬁcation for Monetary Policy
and Business Cycle Analysis,” unpublished, Carnegie-Mellon University, October
1997.
87

—- —- and —- —-, “Performance of Operational Policy Rules in an Estimated Semi-
Classical Structural Model,” NBER working paper no. 6599, June 1998.
Orphanides, Athanasios, “Monetary Policy Rules Based on Real-Time Data,” FEDS
discussion paper no. 1998-3, Federal Reserve Board, December 1997.
Persson, Torsten, and Guido Tabellini, “Introduction,” in Monetary and Fiscal Policy,
Volume 1: Credibility, Cambridge: M.I.T. Press, 1994.
Roberts, John M., “New Keynesian Economics and the Phillips Curve,” Journal of
Money, Credit and Banking 27: 975-984 (1995).
—- —-, “Inﬂation Expectations and the Transmission of Monetary Policy,” FEDS dis-
cussion paper no. 1998-43, Federal Reserve Board, October 1998.
Rogoﬀ, Kenneth, “The Optimal Degree of Commitment to an Intermediate Monetary
Target,” Quarterly Journal of Economics 100: 1169-1190 (19985).
Rotemberg, Julio J., and Michael Woodford, “ An Optimization-Based Econometric
Framework for the Evaluation of Monetary Policy,” NBER Macroeconomics An-
nual 1997, 297-346.
[Expanded version circulated as NBER Technical Working
Paper no. 233, May 1998.]
—- —-, and —- —-, “Interest-Rate Rules in an Estimated Sticky-Price Model,” NBER
working paper no. 6618, June 1998.
Rudebusch, Glenn D., “Federal Reserve Interest Rate Targeting, Rational Expectations
and the Term structure”, Journal of Monetary Economics, 35, 1995, 245-74.
—- —-, and Lars E.O. Svensson, “Policy Rules for Inﬂation Targeting,” in John B. Taylor,
ed., Monetary Policy Rules, Chicago: University of Chicago Press, forthcoming.
Sack, Brian, “Does the Fed Act Gradually? A VAR analysis”, FEDS discussion paper
no. 1998-17, Federal Reserve Board, March 1998a.
—- —-, “Uncertainty, Learning, and Gradual Monetary Policy,” FEDS discussion paper
no. 1998-34, Federal Reserve Board, July 1998b.
Sargent, Thomas J., Macroeconomic Theory, 2d ed., New York: Academic Press, 1987.
—- —-, and Neil Wallace, “Rational Expectations, the Optimal Monetary Instrument,
and the Optimal Money Supply Rule,” Journal of Political Economy 83: 241-254
(1975).
88

Sbordone, Argia M., “Prices and Unit Labor Costs: A New Test of Sticky Prices,”
Seminar Paper no. 653, Institute for International Economic Studies, Stockholm,
October 1998.
Schmitt-Groh´e, Stephanie, and Martin Uribe, “Price Level Determinacy and Monetary
Policy under a Balanced-Budget Requirement,” Journal of Monetary Economics,
forthcoming 1999.
Soderlind, Paul, “Solution and Estimation of RE Macromodels with Optimal Policy,”
unpublished, Stockholm School of Economics, December 1998.
Summers, Lawrence, “How Should Long Term Monetary Policy Be Determined?” Journal
of Money, Credit and Banking, 23, August 1991, 625-31.
Svensson, Lars E.O., “Price Level Targeting versus Inﬂation Targeting: A Free Lunch?”
NBER working paper no. 5719, August 1996.
—- —-, “Inﬂation Targeting as a Monetary Policy Rule,” Journal of Monetary Economics,
forthcoming 1999.
Taylor, John B., “Discretion Versus Policy Rules in Practice,” Carnegie-Rochester Con-
ference Series on Public Policy 39: 195-214 (1993).
—- —-, “The Robustness and Eﬃciency of Monetary Policy Rules as Guidelines for
Interest Rate Setting by the European Central Bank,” IIES seminar paper no.
649, August 1998.
Walsh, Carl, “Optimal Contracts for Central Bankers,” American Economic Review 85:
150-167 (1995).
Watson, Mark W., “Explaining the Increased Variability in Long Term Interest Rates,”
unpublished, Princeton University, May 1999.
Woodford, Michael, “The Optimum Quantity of Money,” in B.M. Friedman and F.H.
Hahn, eds. Handbook of Monetary Economics, vol. II, Amsterdam: North-Holland,
1990.
—- —-, “Control of the Public Debt: A Requirement for Price Stability?” NBER working
paper no. 5684, July 1996.
—- —-, “Price-Level Determination under Interest-Rate Rules,” unpublished, Princeton
University, April 1999a.
—- —-, “Inﬂation Stabilization and Welfare,” unpublished, Princeton University, June
89

1999b.
Yun, Tack, “Nominal Price Rigidity, Money Supply Endogeneity, and Business Cycles,”
Journal of Monetary Economics 37: 345-370 (1996).
90

Table 1: “Calibrated” parameter values.
Structural parameters
β
.99
σ
.157
κ
.024
Shock process
ρ
.35
sd(rn)
3.72
Loss function
λx
.048
λr
.236
Table 2: Statistics for alternative policies.
Case: ρ = 0.
Policy
V[π]
V[x]
V[r]
E[W]
Time Consist.
.122
13.43
2.004
1.244
Non-Inertial
.122
13.43
2.004
1.244
Optimal
.070
9.76
.983
.774
Case: ρ = .35.
Policy
V[π]
V[x]
V[r]
E[W]
Time Consist.
.487
22.95
4.023
2.547
Non-Inertial
.211
9.92
6.720
2.279
Optimal
.130
10.60
1.921
1.097
Case: ρ = .9.
Policy
V[π]
V[x]
V[r]
E[W]
Time Consist.
402.9
528.2
413.7
526.3
Non-Inertial
.353
.463
10.41
2.836
Optimal
.400
4.74
6.77
2.228
91

Table 3: Time-Consistent Equilibria with Alternative Policy Weights.
Policy Weights
Equilibrium Statistics
ˆλπ
ˆλx
ˆλr
λ∆
V[π]
V[x]
V[r]
E[W]
1
.048
.236
0
.487
22.95
4.023
2.547
1
.048
.120
0
.211
9.92
6.720
2.279
1
.048
0
.282
.082
11.73
2.907
1.337
1
.048
-.439
.807
.135
10.50
1.922
1.097
1
0
-.232
.204
.135
10.50
1.922
1.097
20.7
1
-9.09
16.7
.135
10.50
1.922
1.097
0
1
0
5.51
.077
11.95
2.649
1.281
92

0
1
2
3
4
5
6
7
8
9
10
−0.1
0
0.1
0.2
0.3
0.4
0.5
0.6
0.7
0.8
0.9
Natural, Optimal, and Optimal Non−inertial Interest Rate [ρ = 0]
Figure 1
rn(t)
r(t) 
rs(t)

0
1
2
3
4
5
6
7
8
9
10
−0.1
−0.05
0
0.05
0.1
Inflation: Optimal (−) and Optimal Non−inertial (−.) [ρ = 0]
0
1
2
3
4
5
6
7
8
9
10
−0.5
0
0.5
1
Output Gap: Optimal (−) and Optimal Non−inertial (−.) [ρ = 0]
0
1
2
3
4
5
6
7
8
9
10
0
0.2
0.4
0.6
0.8
1
Interest Rate: Optimal (−) and Optimal Non−inertial (−.) [ρ = 0]
Figure 2

0
1
2
3
4
5
6
7
8
9
10
−0.1
0
0.1
0.2
0.3
0.4
0.5
0.6
0.7
0.8
0.9
Natural, Optimal, and Optimal Non−inertial Interest Rate [ρ = 0.35]
Figure 3
rn(t)
r(t) 
rs(t)

0
1
2
3
4
5
6
7
8
9
10
−0.1
−0.05
0
0.05
0.1
0.15
Inflation: Optimal (−) and Optimal Non−inertial (−.) [ρ = 0.35]
0
1
2
3
4
5
6
7
8
9
10
−0.5
0
0.5
1
Output Gap: Optimal (−) and Optimal Non−inertial (−.) [ρ = 0.35]
0
1
2
3
4
5
6
7
8
9
10
0
0.2
0.4
0.6
0.8
1
Interest Rate: Optimal (−) and Optimal Non−inertial (−.) [ρ = 0.35]
Figure 4

0
5
10
15
20
25
30
35
40
−0.1
0
0.1
0.2
0.3
0.4
0.5
0.6
0.7
0.8
0.9
Natural, Optimal, and Optimal Non−inertial Interest Rate [ρ = 0.9]
Figure 5
rn(t)
r(t) 
rs(t)

0
5
10
15
20
25
30
35
40
−0.2
−0.15
−0.1
−0.05
0
0.05
Inflation: Optimal (−) and Optimal Non−inertial (−.) [ρ = 0.9]
0
5
10
15
20
25
30
35
40
−0.5
0
0.5
1
1.5
Output Gap: Optimal (−) and Optimal Non−inertial (−.) [ρ = 0.9]
0
5
10
15
20
25
30
35
40
0
0.2
0.4
0.6
0.8
1
Interest Rate: Optimal (−) and Optimal Non−inertial (−.) [ρ = 0.9]
Figure 6

−10
−8
−6
−4
−2
0
2
4
6
8
10
−3
−2
−1
0
1
2
3
λr
^
rr
Figure 7

−2
−1.5
−1
−0.5
0
0.5
1
1.5
2
0
0.2
0.4
0.6
0.8
1
1.2
1.4
1.6
1.8
2
Mult. sol.
0.5
0.45
0.4
0.3
0.2
0.1
0.05
X
rr
λr
^
λ∆
Figure 8

−2
−1.5
−1
−0.5
0
0.5
1
1.5
2
0
0.2
0.4
0.6
0.8
1
1.2
1.4
1.6
1.8
2
Mult. sol.
1
0.5
0.35
0.25
0.2
0.15
0.1
X
rn
λr
^
λ∆
Figure 9

−2
−1.5
−1
−0.5
0
0.5
1
1.5
2
0
0.2
0.4
0.6
0.8
1
1.2
1.4
1.6
1.8
2
Mult. sol.
1.12
1.2
1.5
2
3
5
10
5
3
2
1.5
X
E[W]
λr
^
λ∆
Figure 10

0
5
10
15
20
25
0
1
2
3
4
5
6
7
8
9
10
1.29
1.3
1.32
1.34
1.35
1.5
2
3.2
1.35
X
E[W]
λπ
~
λ∆
~
Figure 11

−25
−20
−15
−10
−5
0
5
10
15
20
25
0
5
10
15
20
25
30
35
40
45
50
4
3
2
1.5
1.25
1.1
1.25
1.5
2
3
4
X
Mult. sol.
E[W]
λr
~
λπ
~
Figure 12

0
10
20
30
40
50
60
−2
0
2
4
6
8
10
12
14
16
0.5
0.3
0.2
0.1
0.05
0.025
0.01
0.005
θ
Indet.
Instab.
Figure 13
φπ
V[π]

0
10
20
30
40
50
60
−2
0
2
4
6
8
10
12
14
16
50
25
20
15
10
7
4
1
2
0.5
θ
Indet.
Instab.
Figure 14
φπ
V[x]

0
10
20
30
40
50
60
−2
0
2
4
6
8
10
12
14
16
0.01
0.01
0.1
0.5
1
2.5
5
10
50
25
θ
Indet.
Instab.
Figure 15
φπ
V[r]

0
10
20
30
40
50
60
−2
0
2
4
6
8
10
12
14
16
2
1.5
1.3
1.2
1.15
1.1
1.097
1.15
1.2
1.3
1.5
2
5
10
Instab.
Instab.
θ
Indet.
Instab.
Indet.
Figure 16
φπ
E[W]