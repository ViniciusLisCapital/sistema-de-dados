# Bibliography Methodology

**Purpose:** reusable guidelines for building topic-specific literature inventories and conceptual maps for LIS Capital's analysis agents — exchange rate, monetary policy, fiscal policy, and any future area. Established 2026-07 while starting the monetary policy bibliography, generalizing the process already used for `exchange_rate_policy/`.

**Folder layout (established 2026-07):** all per-topic mapping outputs live under `agent_bibliography/agent_mapping/`, split by output type rather than by topic:

```
agent_bibliography/
  BIBLIOGRAPHY_METHODOLOGY.md          — this file (process doc, not a topic output)
  <topic>_policy/                      — raw acquired PDFs for a topic (e.g. exchange_rate_policy/), unaffected by this layout
  agent_mapping/
    conceptual_maps/                   — <topic>_conceptual_map.md, one per topic, built after acquisition
    recommended_bibliography/          — <topic>_bibliography_candidates.md (pre-acquisition) and <topic>_bibliography_gaps.md (post-map gaps) for every topic
    recommended_data/                  — <topic>_data_inventory.md, one per topic
```

Raw PDF vaults (per point b) and this methodology doc stay at the `agent_bibliography/` root — `agent_mapping/` holds only the *analysis and planning* documents built on top of those sources, not the sources themselves.

**This is a set of defaults, not a rigid template.** Each topic gets to apply these points with discretion — e.g. a topic that is inherently global (say, commodity cycles) may weight international sources much more heavily than Brazil-specific ones; a topic that is inherently domestic (say, a specific BCB facility) may skip the international side almost entirely. Deviate when the topic calls for it, and note the deviation in that topic's own files rather than treating it as a violation of the rule.

---

## a) Mix international and Brazil-specific material

Cover the general/international theory of the topic *and* how it plays out in Brazil specifically. The two halves inform each other: international theory gives the framework, Brazil-specific sources (BCB working papers, Brazilian case studies, local applications) show how the framework fits — or breaks — in the actual market LIS trades.

**Discretion:** the right mix depends on the topic. Exchange rate policy and monetary policy both have a substantial Brazil-specific literature (BCB regime documents, COPOM history, local case studies) — expect something like a third to half of sources to be Brazil-focused. A more universal topic may have very little Brazil-specific literature to draw on, and that's fine; don't force it.

## b) Papers and textbooks — extract only the relevant chapter(s) from books

Include both journal articles/working papers and textbooks. For a textbook, don't plan to process the whole book — identify the specific chapter(s) that cover the concept(s) this topic actually needs, and note that at candidate stage (before acquisition) so the eventual extraction step is targeted, not exploratory.

**Discretion:** a short, focused textbook (e.g. a CFA curriculum reading) may be processed in full; a dense 500-page reference (e.g. a graduate macro textbook) should almost always be reduced to 1-3 chapters.

## c) Score the age-vs-foundational tension explicitly

Old and foundational is not the same as old and outdated — a source can be decades old and still be *the* reference (Taylor 1993 on policy rules, Kydland & Prescott 1977 on time inconsistency), while another source from the same era may be superseded and only useful for tracing intellectual history. Score every candidate on a **1-5 foundational scale**, shown next to its publication year, so the two dimensions (canonicity, recency) stay visually distinct instead of collapsing into a single "old = low priority" heuristic:

| Score | Meaning |
|---|---|
| 5 | Still the field's primary reference on its specific question; heavily cited/taught today regardless of age |
| 4 | Highly influential, frequently cited, but later work has refined or partially superseded it |
| 3 | Solid, well-regarded contribution; a useful complement, not essential on its own |
| 2 | Historically important stepping stone; largely superseded by later, better-known work |
| 1 | Only historical/genealogical interest; include only if the topic specifically wants to trace the intellectual history of an idea |

**Discretion:** the score is a prioritization aid for acquisition order, not a strict gate — a 3 that closes an otherwise-empty thematic block still gets acquired before a 5 that only adds a fourth source to an already-strong block.

## d) Organize by thematic/concept blocks

Group candidate sources (and, later, processed concepts) into named clusters — the same pattern used in `exchange_rate_conceptual_map.md`'s `#tag` clusters (`#market_microstructure`, `#currency_regimes`, etc.). Propose the cluster taxonomy up front, before deep acquisition, so sourcing effort spreads across the topic's actual sub-structure instead of clumping around whatever is easiest to find.

**Discretion:** clusters typically number 5-9 per topic and usually include at least one pure-theory cluster, one policy-regime/mechanism cluster, and one Brazil-specific cluster (per point a) — but the exact taxonomy is topic-specific and should be sanity-checked with the user before the acquisition phase starts.

---

## Standard workflow per topic

1. **Candidate list** — draft `agent_mapping/recommended_bibliography/<topic>_bibliography_candidates.md`: sources organized by cluster, each with type (paper/book+chapter), foundational score + year, target cluster tag, and suggested filename. This is the *pre-acquisition* deliverable — nothing has been bought/downloaded yet.
2. **Acquisition** — source PDFs one at a time into `agent_bibliography/<topic>/`, using the naming convention `topic_description (Author, Year).pdf`.
3. **Processing** — read each PDF (or the identified chapter) and fold it into `agent_mapping/conceptual_maps/<topic>_conceptual_map.md`: a row in a Sources table, concept bullets filed under the relevant `#cluster` tag, cross-links (`[[concept]]`) to existing concepts where a genuine connection exists. Process **one source at a time**, not in parallel — this has been the user's preferred cadence (see `agent_mapping/conceptual_maps/exchange_rate_conceptual_map.md`'s processing history) because it lets each new source be weighed against what's already in the map before moving on.
4. **Gaps tracking** — once the map exists, maintain `agent_mapping/recommended_bibliography/<topic>_bibliography_gaps.md` for candidates not yet acquired/processed, following the same format established in `agent_mapping/recommended_bibliography/exchange_rate_bibliography_gaps.md`.
5. **No automatic reconciliation** with any pre-existing topic vault elsewhere (e.g. an Obsidian vault of concept pages) unless the user explicitly asks for it — these are deliberately parallel systems, per the precedent set for `exchange_rate_policy/` vs. `obsidian/exchange_rate/`.
6. **Data inventory** — separately (see e.g. `agent_mapping/recommended_data/exchange_rate_data_inventory.md`), build a `agent_mapping/recommended_data/<topic>_data_inventory.md` mapping the topic's analytical categories to what already exists in the LIS database vs. what's missing. This is independent of the literature pipeline above and does not need to wait for it to finish, though doing literature first (as agreed for monetary policy) helps clarify which data categories actually matter.
