---
aliases: ["Calvo 1983 - Staggered Prices in a Utility-Maximizing Framework"]
---

# Staggered Prices in a Utility-Maximizing Framework — Guillermo A. Calvo 1983

**Type:** paper
**Tags:** #calvo-pricing #sticky-prices #staggered-prices #phillips-curve #indeterminacy #interest-rate-peg
**Source:** Journal of Monetary Economics 12 (1983) 383-398, North-Holland (printed "383 398" in the extraction)
**Language:** English
**Source file:** [[monetary_policy/clean_md/staggered_prices (Calvo, 1983)]]

---

## Context and motivation

Staggered-contract models (Phelps 1978; Taylor 1979, 1980) captured non-synchronous price revisions but were analytically cumbersome, and closed the demand side with aggregate demand as a function of real money balances, leaving out interest-rate effects. Calvo proposes "an analytically more tractable price-setting technology" and puts it inside a model where demand comes from utility maximization by Sidrauski-Brock infinitely-lived families, so that monetary and fiscal policy can be analyzed for welfare.

## Core argument / thesis

If each firm may change its price only when a random signal arrives, with the arrival independent of the time since the last change and independent across firms, then (with a continuum of firms) a constant fraction of firms reprices per unit of time, the surviving prices have a geometric age distribution, and the price level is a predetermined variable. This yields a simple aggregate inflation equation and a model whose equilibrium can be found "on the basis of essentially graphical techniques". The paper uses it to show that money is the welfare-superior stabilization tool, and that "despite the price level being a predetermined variable, a policy of pegging the nominal interest rate will lead to the existence of a continuum of equilibria". The device "does not really depend on the existence of nominal contracts": it fits firms hit by random shocks that prevent continuous revisions or the observation of changes in the state of nature.

## Key mechanisms / model

- **Price-change signal (section 2, eq. (1))**: the probability density of receiving the signal h periods from today is exponential with parameter δ > 0, independent of the last time the signal was received, so "the expected length of a price quotation" is 1/δ. The timing of price changes is exogenous (unlike the menu-cost literature of Barro 1972 and Sheshinski and Weiss 1977). Footnote 4: the exogeneity of δ is "a not very satisfactory feature", but all results hold for any constant δ > 0.
- **Pricing rule (2)**: a firm resetting at t sets its (log) price as a weighted average of the future price level and future excess demand, each future date weighted by the probability that the quotation is still in force then; perfect foresight lets actual future values stand for expectations.
- **Price level (3)–(4)**: the (log) price level is the average of outstanding quotations, each vintage weighted by the share of firms that set their price at s and have not yet received a new signal at t; by the law of large numbers, with a continuum of firms, a measure δ of firms reprices per unit of time. The appendix derives (5b) as the limit of a discrete-time version as the number of price setters grows and the period shrinks.
- **Inflation dynamics (5)–(8)**: differentiating (2) and (3), the *rate of change of inflation* — the "velocity" of inflation — is a decreasing function of excess demand, (7) with b > 0 in (8): "what might be called a 'higher-order' inverse Phillips Curve". In equilibrium inflation is nonetheless positively associated with excess demand, but that Phillips-type relation is "a function of policy and all the parameters of the system". Footnote 6 compares the Phelps-Taylor fixed-length contracts, which give a difference-differential system with leads and lags.
- **Supply**: firms produce up to a capacity ȳ at zero variable cost and output is demand-determined when demand is below capacity, "as in the standard Keynesian framework".
- **Demand (section 3)**: families maximize discounted utility of consumption and real money balances (9)–(11) with money the only asset (12). A costless "price-regulation mechanism" (PRM) of taxes and subsidies makes every consumer face the same price (the geometric mean of quotations) and makes pricing rule (2) compatible with profit maximization, abstracting from how customers are matched to firms. Optimal control gives the consumption Euler condition (15); with goods-market (16) and money-market (17) equilibrium, the system (20) in consumption, real balances and inflation has a unique steady state (21) and, with real balances the only predetermined variable, a unique convergent path (proof in appendix A.2: one negative root, two with positive real parts). Below full employment the real interest rate exceeds its steady-state level, as in IS-LM after a fall in real balances (27).

## Main results / findings

- **Monetary vs. fiscal policy (section 4)**: from an excess-supply position, a once-and-for-all unanticipated increase in the money supply moves the economy immediately to full employment, and announcing a money growth rate that sets the marginal utility of money to zero at the steady state (29) attains the first best — "the optimal quantity of money". Raising government expenditure to fill the full-employment gap (30) also works (inflation stays at its steady-state rate, (31)–(33)) but lowers steady-state consumption permanently, so utility is "permanently lower" than under the monetary policy: fiscal policy is "an effective but Pareto-inferior tool".
- **Interest-rate peg (section 4)**: Sargent and Wallace (1975) showed price-level indeterminacy under a pegged interest rate with flexible prices. Here the price level is predetermined, yet pegging the nominal rate produces "a higher-order indeterminacy": a continuum of equilibrium (consumption, inflation) pairs on the convergent curve of Fig. 2, since both are free to jump at t = 0 — so the problem "is not just a mere artifact of their perfect-price-flexibility assumption". Footnote 11 extends the author's earlier flexible-price result for a rule in which money growth rises with the gap between the actual and target interest rate: non-uniqueness or uniqueness depending on whether the feedback coefficient is above or below one.
- **Robustness**: "all of our qualitative results are independent of the actual average length of price quotations".

## Limitations and caveats

- **Equations are heavily damaged by OCR.** The bodies of (2) (the pricing rule), (5a,b), (9) (utility), (12) (budget constraint), (14a,b), (19a,b), (20a,b,c) and the money-growth announcement just before (29) are missing or reduced to fragments; (7)–(8) print as "fl,=~~=6[~-~J= --bE," and "b=6$9>0"; footnote 6's (F.1)–(F.3) are garbled. In the appendix, (A.1)–(A.2), (A.6) onward and the matrix (A.8) are unreadable. Symbols are corrupted throughout (δ prints as "S", "6" or "d"; Π as "n", "I7", "fl" or "ff"; the money growth and discount rates as "p", "ji" or "fi"). The note describes the model from the surrounding text and does not restore any equation.
- The expected quotation length prints as "(l/S)l.'" (1/δ with a footnote mark); footnote 11's uniqueness condition prints as "non-uniqueness prevails if u > 1; but if a c I uniqueness always holds" — read here only as a threshold of one on the feedback coefficient.
- Figures 1 and 2 (phase diagrams) survive only as captions and stray axis labels. Footnotes 1, 2 and 5 are partly lost ("s a viable assumption here because despite the uncertaintyt o which price-…").
- No reference list in the extraction.
- Author's own caveats: δ is exogenous; the PRM is an artificial device to obtain a uniform consumer price; perfect foresight; the analysis concentrates on the excess-supply region (the excess-demand region is handled only through "notional demand"); uniqueness and monotonic convergence are local (neighborhood of the steady state).

## Connections

- [[calvo_pricing]] — the origin of the device: a constant hazard of price change, exogenous timing, geometric survival of quotations, expected price duration 1/δ, and aggregation by the law of large numbers
- [[nk_phillips_curve]] — the continuous-time ancestor: pricing on expected future price level and excess demand gives an inflation equation in which the change of inflation falls with excess demand, while in equilibrium inflation and excess demand move together
- [[taylor_principle]] — the extreme case of a rule with no response at all: a pegged nominal rate leaves a continuum of equilibria even with a predetermined price level; footnote 11's feedback-coefficient threshold of one
- [[monetary_policy/synthesis/basic_nk_model_ch3 (Gali, 2015)]] — Galí's discrete-time version (reset probability 1−θ, mean duration of four quarters) is the pricing block of the basic NK model
- [[monetary_policy/synthesis/science_of_monetary_policy (Clarida, Gali & Gertler, 1999)]] — the baseline Phillips curve of that survey rests on "an assumption due to Guillermo Calvo (1983)"
