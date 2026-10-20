# Conservative Central Banker

**Type:** Institutional remedy / delegation scheme
**Tags:** #conservative-central-banker #time-inconsistency #inflation-bias #central-bank-independence #delegation

---

## Definition

Delegating monetary policy to an agent who places a larger weight on inflation stabilization, relative to employment stabilization, than society's own loss function does. Rogoff (1985): "Society can sometimes make itself better off by appointing a central banker who does not share the social objective function, but instead places 'too large' a weight on inflation-rate stabilization relative to employment stabilization."

## Mechanism

- **Why it helps**: under discretion, a labor-market distortion that keeps market employment below the social optimum creates an inflation bias — wage setters set wage inflation high enough that the central bank's marginal gain from raising employment is offset by the marginal cost of more inflation. A banker who cares more about inflation is less tempted, so the time-consistent inflation rate falls (Rogoff).
- **Why it costs**: the same weight distorts responses to supply shocks, letting more of them pass through to employment; demand shocks are still fully offset, since offsetting them stabilizes both inflation and employment (Rogoff).
- **Why the weight is finite**: at society's own weight the bank stabilizes optimally, so a slightly higher weight gives a first-order inflation gain at a second-order stabilization cost; with an infinite weight inflation reaches the social optimum but supply shocks pass "entirely through to employment", so lowering the weight gives "a first-order stabilization gain at a second-order inflation cost" (envelope theorem; Rogoff's Theorem: the optimal extra weight is strictly positive and finite when there is a distortion, zero when there is none).
- **Same logic for intermediate targets**: rewards and penalties that put direct weight on an inflation, nominal GNP or money-supply target reduce time-consistent inflation in the same way; the conservative banker is formally inflation-rate targeting (Rogoff, Section V).

## When it applies / when it fails

- Needed only when there is an incentive to inflate systematically; with no labor-market distortion the best agent shares society's loss (Rogoff).
- It is a "third-best" solution: removing the distortion (first best) or a constitutional state-contingent money rule (second best) would do better if feasible (Rogoff).
- Rogoff assumes the appointee's preferences are known with certainty and a one-period game without reputation; reputation can ameliorate the credibility problem but, except in special cases, not eliminate it.

## How it appears across sources

| Source | Role |
|---|---|
| [[monetary_policy/synthesis/optimal_commitment_intermediate_target (Rogoff, 1985)]] | Origin: the Theorem that the optimal extra weight on inflation is positive and finite; extension to inflation, nominal GNP, money and interest-rate targets; explanation of independent central banks and conservative governors |
| [[monetary_policy/synthesis/optimal_contracts_central_bankers (Walsh, 1995)]] | Shows that the bias-vs-stabilization trade-off of the conservative banker comes from restricting the contract to a heavier quadratic weight on inflation; a linear inflation contract removes the bias without distorting stabilization |
| [[monetary_policy/synthesis/optimal_monetary_policy_inertia (Woodford, 1999)]] | Optimal delegation applied to the response to shocks: a discretionary bank should be given a positive weight on squared rate changes and a negative weight on the rate level (4.14)–(4.15), recovering more than 99.9 percent of the gain from commitment (Table 3) |

## BRL / application to the current analysis

The linked sources say nothing about Brazil.

## Connections

- [[time_inconsistency]] — the inflation bias of discretion that the conservative banker reduces
- [[inflation_targeting]] — Rogoff reads the conservative-banker analysis as inflation-rate targeting
- [[monetary_targeting]] — money-supply targeting as another intermediate target with an optimal finite weight
- [[monetary_policy/synthesis/optimal_commitment_intermediate_target (Rogoff, 1985)]] — the paper that introduced it
- [[monetary_policy/synthesis/optimal_contracts_central_bankers (Walsh, 1995)]] — the optimal contract that dominates the conservative central banker
- [[monetary_policy/synthesis/optimal_monetary_policy_inertia (Woodford, 1999)]] — delegating a distorted objective, here an interest-rate smoothing goal, to fix discretion's poor response to shocks
