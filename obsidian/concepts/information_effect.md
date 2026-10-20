# Information Effect

**Type:** Transmission channel / central bank signaling
**Tags:** #information-effect #delphic #fomc #policy-surprises #expectations #natural-rate

---

## Definition

The effect of a central bank announcement on private-sector beliefs about **non-monetary** economic fundamentals, as distinct from its effect on beliefs about the future path of policy. Nakamura & Steinsson (2018), following Romer and Romer (2000), call it the "Fed information effect": when an FOMC announcement signals higher rates than markets expected, participants may infer that the Fed is more optimistic about the economy than they are, and revise their own outlook up. Campbell et al. (2012) describe the same content as the **Delphic** component of policy communication — a forecast based on the central bank's possibly superior information.

## Mechanism

- **Signature in the data**: a surprise tightening should lower expected output and raise expected unemployment under the conventional reading. Instead, Blue Chip expected output growth rises after a tightening (Nakamura & Steinsson), and expected unemployment falls (Campbell et al.) — the "wrong sign".
- **Modeling it (Nakamura & Steinsson)**: a fraction ψ of the policy shock is read as news about the path of the natural rate of interest, and the rest as a tightening relative to it. What moves the output gap and inflation is the real interest rate gap (real rate minus believed natural rate), so a large information share means a given rise in real rates is less contractionary than it looks. Estimated share: roughly 2/3 of the real-rate response is the natural rate, 1/3 a tightening relative to it.
- **Why the central bank can have this effect**: the FOMC has essentially the same data as the private sector, but a staff that processes it; information "can flow both ways". Nakamura & Steinsson find policy news shocks tend to be positive when the Greenbook growth forecast is above Blue Chip's, and the gap narrows afterwards.

## When it applies / when it fails

- It belongs to **surprises**, not to systematic policy: a rate move that follows from the reaction function to public information carries no information effect, by definition. Shock-based estimates therefore have an external validity problem when used to infer the effect of rule-based policy (Nakamura & Steinsson, Figure 9: rule-based increases reduce output substantially).
- Its size depends on what the market thinks the surprise reveals; the Volcker tightening, read as a different loss function rather than optimism, is cited as a case with a small information effect.
- Separating it from a pure policy shock is hard. Campbell et al.'s Odyssean component is measured as a residual; Nakamura & Steinsson's ψ is one fraction for all episodes, and their causal decomposition rests on an assumed counterfactual for when the news would otherwise have arrived.
- Policy consequence: a central bank surprising markets can be "fighting against itself"; a surprise easing may spread pessimism. Withholding bad news may be optimal only when the bank cannot track the natural rate, e.g. at the zero lower bound (Nakamura & Steinsson).

## How it appears across sources

| Source | Role |
|---|---|
| [[monetary_policy/synthesis/forward_guidance_effects (Campbell et al., 2012)]] | Wrong-sign responses of Blue Chip unemployment and inflation forecasts to FOMC surprises, read as Delphic content |
| [[monetary_policy/synthesis/information_effect_hf_identification (Nakamura & Steinsson, 2018)]] | Names and estimates the Fed information effect: expected output growth rises after a tightening; a NK model where ψ of the shock moves beliefs about the natural rate, estimated at about 2/3 |

## BRL / application to the current analysis

The sources linked here say nothing about Brazil yet.

## Connections

- [[forward_guidance]] — the Delphic/Odyssean split is the communication-side version of the same distinction; high-frequency shocks built from futures capture guidance and information together
- [[natural_rate_of_interest]] — Nakamura & Steinsson model the information as news about the natural rate's path
- [[nk_phillips_curve]] — ignoring the information effect biases the estimated slope down (more rigidity)
- [[monetary_policy/synthesis/forward_guidance_effects (Campbell et al., 2012)]] — Delphic content in FOMC statement surprises
- [[monetary_policy/synthesis/information_effect_hf_identification (Nakamura & Steinsson, 2018)]] — the defining paper for the term and its structural estimate
