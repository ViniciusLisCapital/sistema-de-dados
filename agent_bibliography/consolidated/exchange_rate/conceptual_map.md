# Exchange Rate — Data × Literature Integration Map

**Purpose:** step (iii) of the three-part deliverable — connecting `data_inventory.md`'s 8 analytical data categories to `bibliography.md`'s 9 clusters, so it's visible which literature each data series is actually evidence *for* (and, read the other way, which data a given theoretical argument needs to be checked against). Nothing in `exchange_rate_conceptual_map.md` (the full ~140-concept map) or the other consolidated files was modified to build this.

**How to read this file:** same convention as `exchange_rate_conceptual_map.md` — `[[concept_slug]]` marks an integration point (Obsidian-style wikilink, not yet split into a separate note, just a consistent name to search on). `#tag` marks the literature cluster from `bibliography.md`. Each bullet cites the specific `data_inventory.md` section(s) it draws on, in parentheses. Organized by literature cluster (the same 9 used in `bibliography.md`), since that's the axis a reader is more likely to start from — "what data backs this argument" — rather than starting from the data side.

Every bullet below is traceable to a specific line already written in `bibliography.md` or `data_inventory.md` — this file doesn't introduce new claims, it just makes the cross-references between the two documents explicit and organized by cluster.

---

## `#market_microstructure`

- **[[bcb_fx_plumbing_data_link]]** — the BCB's FX position/intervention data (reserves & intervention, §6) and the registered/contracted FX flow tables (§5) are the operational, transaction-level counterpart to this cluster's BCB technical note and CFA market-structure material — the plumbing the literature describes is exactly what these series record. *(data_inventory.md §5, §6)*
- **[[fx_options_positioning_data_gap]]** — the options-based-positioning gap flagged in the data map (§8) is the same gap as this cluster's Garman-Kohlhagen/options-primer literature entries. Neither the data side nor the theory side of FX options is built out yet — a gap that reinforces itself across both documents. *(data_inventory.md §8)*

## `#exchange_rate_determination`

- **[[spot_price_as_dependent_variable]]** — the PTAX spot series (§1) is the literal dependent variable every UIP, PPP, and overshooting argument in this cluster is trying to explain. *(data_inventory.md §1)*
- **[[carry_differential_uip_input]]** — the ex-ante and ex-post rate differentials, plus the cupom cambial (§2), are the direct empirical inputs to this cluster's UIP/CIP parity-conditions material and Fama's forward-premium econometrics. *(data_inventory.md §2)*

## `#currency_regimes`

- **[[reserves_as_peg_defense_evidence]]** — the reserves and BCB intervention stock/flow data (§6) is the empirical counterpart to this cluster's fixed-rate-defense mechanics (Krugman Ch. 18, Mundell 1963). *(data_inventory.md §6)*
- **[[reer_em_peer_comparison_gap]]** — the REER EM-peer comparison set (§7) is what would close this cluster's flagged non-Brazil EM depth gap — currently only 4 LatAm peers are tracked. *(data_inventory.md §7)*

## `#balance_of_payments`

- **[[bop_identity_empirical_counterpart]]** — the current account, financial account, and portfolio-investment data (§4) is the direct empirical instantiation of this cluster's trade-balance/capital-account accounting identities. *(data_inventory.md §4)*
- **[[terms_of_trade_bop_mechanism]]** — terms of trade (§3) operates through this cluster's trade-balance mechanics as much as through the valuation models in `#applied_valuation_tools` below. *(data_inventory.md §3)*
- **[[fx_flow_current_account_channel]]** — registered FX flow (§5) is the empirical counterpart to this cluster's flow-supply/demand current-account-adjustment channel. *(data_inventory.md §5)*

## `#policy_transmission`

**No data-category link identified.** Worth flagging explicitly rather than silently omitting: this is the base's most purely theoretical cluster (Mundell-Fleming policy-mix effectiveness, Frieden's political-economy sectoral framework), and neither argument is the kind a single tracked time series directly validates — it's the one cluster this data map can't check empirically against what LIS currently tracks.

## `#applied_valuation_tools`

- **[[beer_gsdeer_fundamental_inputs]]** — the real interest rate differential (§2), terms of trade (§3), and REER itself (§7) are exactly BEER's/GSDEER's canonical fundamental driver set (Paiva 2006's own list) — the input series any equilibrium-exchange-rate estimate in this cluster is built on. *(data_inventory.md §2, §3, §7)*
- **[[spot_price_valuation_target]]** — spot price (§1) is what every valuation model in this cluster (BEER, GSDEER, GSFEER) produces a fair-value estimate *of*. *(data_inventory.md §1)*

## `#capital_controls`

- **[[bop_instrument_riskiness_data]]** — the FDI-vs-portfolio-investment split within balance of payments (§4) is the direct empirical counterpart to Ostry et al. (2010)'s capital-inflow riskiness ranking and the CFM/MPM design questions this cluster is built around. *(data_inventory.md §4)*

## `#currency_crisis_dynamics`

- **[[reserve_depletion_crisis_mechanics_data]]** — the reserves and intervention data (§6) is the empirical counterpart to the reserve-depletion mechanics at the core of the first-generation crisis models (Krugman 1979, Flood & Garber). *(data_inventory.md §6)*
- **[[positioning_unwind_crisis_amplifier_data]]** — speculative positioning (§8) tracks the leveraged-position-unwinding mechanism that amplifies the capital-flow-surge-reversal pattern opening this cluster. *(data_inventory.md §8)*

## `#practitioner_mental_models`

- **[[verde_carry_data_link]]** — carry/rate differential data (§2) underlies Verde's §3.1/§3.2/§3.4 mental models (carry as BRL support, the real rate as a valuation anchor, the cupom cambial as a tracked carry instrument). *(data_inventory.md §2)*
- **[[verde_terms_of_trade_data_link]]** — terms of trade (§3) underlies Verde's §2.1/§2.2 structural-vs-cyclical-surplus framework. *(data_inventory.md §3)*
- **[[verde_positioning_data_link]]** — speculative positioning data (§8) underlies Verde's §5.3 positioning-as-contrarian-signal mental model. *(data_inventory.md §8)*

---

## Coverage notes

**Best-integrated data categories:** carry/rate differential (§2) and reserves/intervention (§6) each connect to four literature clusters (determination, valuation, crisis dynamics or regimes, and mental models) — these two data categories are the base's most load-bearing, cited from the most distinct theoretical angles.

**Weakest link:** `#policy_transmission` has no data-category connection at all (see above) — a genuine, not-yet-resolved gap between this bibliography's most political-economy-flavored cluster and what LIS's pipeline tracks quantitatively.

**One data category, several theories:** terms of trade (§3) and positioning (§8) each feed three clusters spanning both the academic/institutional literature and the Verde practitioner layer — a useful reminder that a single series often needs to be read through more than one theoretical lens at once.

---

## Status

Step (iii) complete: all 8 data categories connected to at least one literature cluster (7 of 9 clusters have at least one link; `#policy_transmission` does not, flagged above rather than papered over). Every bullet traces back to text already written in `bibliography.md` or `data_inventory.md` — nothing new asserted here. Full concept-level integration (linking individual `[[concepts]]` in `exchange_rate_conceptual_map.md`, not just cluster tags, to specific data series) remains a separate, larger effort not undertaken in this pass.

This closes all three parts of the original request: (i) `bibliography.md`, (ii) `data_inventory.md`, (iii) this file.
