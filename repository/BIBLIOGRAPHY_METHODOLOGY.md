# Bibliography Methodology

**Purpose:** reusable guidelines for building topic-specific literature inventories and conceptual maps for LIS Capital's analysis agents — exchange rate, monetary policy, fiscal policy, and any future area. Established 2026-07 while starting the monetary policy bibliography, generalizing the process already used for `exchange_rate_policy/`.

**Folder layout:** the repository keeps the raw material and the acquisition planning; the vault keeps everything an agent reads.

```
repository/
  BIBLIOGRAPHY_METHODOLOGY.md          — this file (process doc, not a topic output)
  <topic>/raw_pdf/, raw_md/            — acquired PDFs and their untouched extraction
  agent_mapping/
    data_tracker.xlsx                  — the single home of every list (since 2026-10-19, when the
                                         .md lists were folded into it): one "Qual - <Area>" tab per
                                         topic (the literature: candidates, acquired, dropped, gaps),
                                         one "Quant - <Area>" tab (the data inventory), and a "Notes"
                                         tab with the reasoning per cluster and per data section
obsidian/<topic>/
  clean_md/                            — full cleaned text, written by repository/ingestion/
  synthesis/, concepts/, mental_models/
  <topic>_conceptual_map.md            — one per topic: causal skeleton, outputs to / inputs from other areas, concept index
```

The map keeps the topic prefix in the filename because Obsidian resolves `[[wikilinks]]` by name across the whole vault: six files called `conceptual_map.md` would be ambiguous.

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

1. **Candidate list** — rows in the topic's "Qual - <Area>" tab of `agent_mapping/data_tracker.xlsx`: Name, Autor/Company, Date, Importance (the 1-5 foundational score of §c), "Do we have it?" = No, Type (paper/book+chapter), Cluster (`#tag`), Why (what it gives the agent). Acquisition details go in Comments: priority (high = answers one of the agent's standing questions directly; medium = thickens a cluster the agent uses; low = reference depth), the suggested file name, where to get it. The reasoning per cluster — scope boundaries with other topics, open gaps with no source identified yet, acquisition order — goes in the Notes tab. This is the *pre-acquisition* deliverable.
2. **Acquisition** — save PDFs into `repository/<topic>/raw_pdf/` and run `/ingest <topic>` (the ingestion agent, `repository/ingestion/INGESTION.md`), using the naming convention `topic_description (Author, Year).pdf`, with the year of the canonical published version even when the file is a working-paper copy. Every ingestion updates the tab's system columns (J-P) and "Do we have it?".
3. **Processing** — read each source and fold it into `obsidian/<topic>/<topic>_conceptual_map.md`: concept bullets filed under the relevant `#cluster` tag in Part 4 (and, if it changes what moves the variable or what another area needs, into Parts 1–3), cross-links (`[[concept]]`) to existing concepts where a genuine connection exists. Process **one source at a time**, not in parallel — the user's preferred cadence, because it lets each new source be weighed against what's already in the map before moving on.
4. **Gaps** — a candidate not yet acquired is a row with "Do we have it?" = No; a source dropped from the list stays as a row with "Dropped" and the reason in Comments, so the decision is visible; a gap with no source identified yet is a note on its cluster in the Notes tab.
5. **The vault is the only layer agents read.** The conceptual map, `clean_md/`, syntheses, concepts and mental models all live in `obsidian/<topic>/`; `repository/` holds the raw PDFs/extractions and the tracker, which no agent consumes.
6. **Data inventory** — separately, the topic's "Quant - <Area>" tab: one row per series or gap (Name, Source = table · series, Date = coverage, Importance = gap priority, "Do we have it?", Category = the analytical category, Comments), and the "why it matters" of each category in the Notes tab (Kind = Data). Independent of the literature pipeline above, though doing literature first helps clarify which data categories actually matter.

**Type labels:** "Paper" covers journal articles and working papers; "Textbook chapter" and "CFA curriculum reading" are pedagogical syntheses rather than original contributions (scored accordingly — useful, current, rarely a 5); "Practitioner research note" covers bank/asset-manager research; "Central bank technical note" and "Official institutional doctrine" cover primary policy-institution sources; "Primary legal source" covers laws and decrees, which define the framework and carry no foundational score.
