---
aliases: ["Gali 2015 - Unemployment in the New Keynesian Model"]
---

# Unemployment in the New Keynesian Model (Chapter 7) — Jordi Galí 2015

**Type:** book chapter
**Tags:** #new-keynesian #unemployment #wage-phillips-curve #natural-rate-of-unemployment #sticky-wages #wage-markup #taylor-rule
**Source:** Chapter 7 of *Monetary Policy, Inflation, and the Business Cycle* (2nd ed.) (title from the tracker; the clean_md prints only "Chapter 7 / Unemployment in the New Keynesian Model")
**Language:** English
**Source file:** [[monetary_policy/clean_md/unemployment_nk_model_ch7 (Gali, 2015)]]

---

## Context and motivation

The New Keynesian model with staggered price and wage setting of chapter 6 is "a framework of reference", and medium-scale versions are used by many central banks for forecasting and policy simulation. One of its most cited weaknesses is "the lack of any reference to unemployment", which could even suggest central banks need not monitor or respond to it. Most of the literature fixes this by embedding search and matching frictions (Mortensen and Pissarides 1994). This chapter, drawing on Galí (2011a, 2011b), takes a different route: it reinterprets the labor market of the chapter 6 model rather than extending it, keeping the representative household and making the unemployment rate an equilibrium object conditional on the policy rule.

## Core argument / thesis

With indivisible labor, unemployment is the gap between the labor force — everyone whose real wage exceeds their disutility of work — and employment, which is demand-determined. Market power in wage setting (a positive desired wage markup) explains why there is unemployment even with flexible wages; nominal wage rigidity, by making the average wage markup move, explains why unemployment fluctuates. The wage markup is proportional to the unemployment rate, so the wage inflation equation of chapter 6 becomes a forward-looking "New Keynesian Wage Phillips Curve" in the unemployment gap. Under a conventional Taylor rule unemployment is too volatile relative to the optimal policy, suggesting "likely welfare gains from stabilizing the unemployment rate beyond what is implied by the Taylor rule"; a simple rule that responds to unemployment tracks the optimal policy much better. The framework abstracts from frictional unemployment from costly reallocation, but the text notes that the labor-frictions literature finds such frictions alone insufficient to generate realistic unemployment fluctuations, "pointing to the need for some kind of wage rigidity".

## Key mechanisms / model

- **Households and wage setting (7.1.1)**: each household has members indexed by labor type j and by s, which sets the disutility of work χs^ϕ if employed; full risk sharing within the household gives all members the same consumption (the text calls this "not an innocuous assumption, especially from a welfare viewpoint"). Unions reset wages with Calvo probability 1 − θw, giving wage inflation (4), negatively related to the deviation of the average wage markup from its desired value.
- **Labor force and unemployment (7.1.2)**: an individual participates if and only if the real wage in his trade exceeds his disutility of work in consumption units; the marginal participant defines the labor force, and aggregating gives a participation (labor supply) equation (6). The unemployment rate is the log difference between labor force and employment (7), close to the conventional 1 − N/L for low rates. Combined with the definition of the average wage markup this gives `µw t = ϕut` (8): the wage markup is the vertical gap between wage and labor supply, unemployment the horizontal gap between labor supply and demand (Figure 7.1), with ratio ϕ.
- **Natural rate of unemployment (10)**: defined as "the unemployment rate that would prevail in the absence of nominal wage rigidities"; with a constant desired wage markup it is constant and equal to the desired markup divided by ϕ. Market power accounts for positive unemployment without rigidities; unemployment *fluctuations* need nominal wage rigidity. If the desired markup varies, the natural rate fluctuates too, and actual unemployment has a natural-rate component and a rigidity component.
- **Wage Phillips curve (11)**: `πw t = βEt{πw t+1} −λwϕ(ut −un)`. Galí (2011a) "refers to the previous equation as the New Keynesian Wage Phillips Curve" and reports supporting evidence from postwar US data. Unlike Phillips (1958) it is forward-looking and derived from first principles with structural coefficients.
- **Equilibrium (7.2)**: the dynamic IS equation (12), price inflation (13), the wage Phillips curve in the unemployment gap (14), the real wage gap identity (15), plus an equation linking the unemployment gap to the output and real wage gaps (16). Combining (14) and (16) gives back chapter 6's wage inflation equation, so the extension adds one variable and one equation; the optimal-policy conditions (18)–(21) are those of chapter 6, since the welfare approximation and constraints are unchanged.
- **Calibration discipline (7.3)**: the gross wage markup equals exp{ϕun}; with ϕ = 5 and un = 0.05 (an average unemployment rate of 5 percent), ϵw = 4.5, "associated with an average wage markup of 28 percent". The rest of the calibration is chapter 6's.

## Main results / findings

- **Monetary policy shock (Figure 7.2)**, under the Taylor rule `it = 0.01 + 1.5π p t + 0.125 yt + vt` (17), ρv = 0.5, an initial impulse of 0.25 (100 basis points annualized): unemployment "rises substantially, and persistently", mostly because employment falls and only marginally because the labor force rises (a negative wealth effect with a nearly unchanged real wage); the real wage falls slightly. Footnote 10: the small countercyclical labor force response "appears to be at odds" with the evidence in Christiano, Trabandt, and Walentin (2010); Galí, Smets, and Wouters (2012) fix it with Jaimovich–Rebelo preferences.
- **Wage rigidity and unemployment fluctuations (Table 7.1)**, monetary shocks with σv = 0.25 percent (1 percent annualized), θw ∈ {0.1, 0.5, 0.75}, ρv ∈ {0.0, 0.5, 0.9}: volatility (standard deviation of unemployment) rises with θw for every ρv — for ρv = 0.9 from 0.31 to 1.24 to 2.47. Persistence (first-order autocorrelation) also rises with θw and with ρv: 0.48 under the baseline (θw = 0.75, ρv = 0.5), 0.87 with ρv = 0.9, versus 0.90 in the United States and 0.92 in the euro area (HP-detrended, footnote 13); with ρv = 0.0 it is negative (−0.14, −0.02, −0.01). Cyclicality (correlation with output) is strongly negative everywhere, from −0.77 to −0.99. Conclusion: with realistic wage rigidity and shock persistence the model "can potentially generate unemployment fluctuations with properties comparable to those observed in actual economies."
- **Optimal policy vs. Taylor rule, technology shock (Figure 7.3)**, one percent: the optimal policy is more accommodative — output rises more, employment stays largely unchanged instead of falling, close to the efficient response (zero employment and participation response, output one-for-one with technology given σ = 1). Unemployment "declines somewhat under the optimal policy, which contrasts with the strong rise observed under the Taylor rule". The real wage rises less than its natural counterpart but more than under the Taylor rule.
- **Demand shock (Figure 7.4)**, one percent in zt: the optimal policy fully insulates output, inflation and all labor market variables, moving only the nominal and real rates one-for-one with the natural rate; under the Taylor rule output and employment rise, unemployment falls and inflation is positive — "the Taylor rule is not sufficiently stabilizing in the face of demand shocks."
- **A rule with unemployment (Figures 7.5, 7.6)**: `it = 0.01 + 1.5π p t −0.5 ut` (22), which Galí (2011b) argues fits the Fed's decisions from 1987 to 2008 better than the standard Taylor rule, after technology shocks gives responses that "approximate pretty well the responses under the optimal policy", tracking it "much better than the Taylor rule" for every variable shown, and similarly after demand shocks.
- **Literature (7.4)**: Galí, Smets, and Wouters (2012) use the same approach in a medium-scale model and show that unemployment data separately identify wage markup and labor supply shocks, answering the Chari, Kehoe, and McGrattan (2009) critique (exercise 7.2 develops this).

## Limitations and caveats

- **Equations are damaged in places**: hats are lost, so in rules (17) and (22) the output and unemployment terms print without the marker of a gap or deviation ("0.125 yt", "−0.5 ut"), and the gap variables in (12)–(16) print like levels; the Δ in (15) is lost. The household utility integral, (6)'s approximations and (16) read as fragments. Described in words here, not restored.
- **Figures 7.1–7.6** survive only as captions, panel labels and a few axis ticks; the impulse-response findings above are the text's descriptions.
- **Table 7.1** is extracted one value per line; the values quoted follow the extraction's order (three θw columns within each of the three panels, per ρv row), which matches the text's statements.
- The text says the optimality conditions (18)–(21) "are identical to those derived in chapter 3", while it introduces them as "derived in chapter 6", and they match the chapter 6 conditions. Flagged as written.
- Model limits stated by the text: no frictional unemployment from costly reallocation; full consumption insurance within the household; none of the "bells and whistles" of medium-scale DSGE models (habits, capital, indexation); a constant desired wage markup, so the natural rate of unemployment is constant. Optimal policy is under commitment only. Exercises 7.1–7.3 are posed but not solved.

## Connections

- [[natural_rate_of_unemployment]] — defined as unemployment without nominal wage rigidities, equal to the desired wage markup over ϕ (10); constant here, time-varying if desired markups move
- [[sticky_wages]] — nominal wage rigidity is "a necessary ingredient" for unemployment fluctuations; Table 7.1 shows volatility and persistence rising with θw
- [[nk_phillips_curve]] — the New Keynesian Wage Phillips Curve (11): wage inflation driven by expected wage inflation and the unemployment gap, contrasted with Phillips (1958)
- [[taylor_rule]] — the standard rule (17) leaves unemployment too volatile against the optimal policy; an unemployment-augmented rule (22) fits the Fed 1987–2008 and approximates the optimum
- [[monetary_policy/synthesis/sticky_wages_prices_ch6 (Gali, 2015)]] — the model this chapter reinterprets: same equilibrium conditions and optimal-policy conditions, plus the unemployment equation (16)
