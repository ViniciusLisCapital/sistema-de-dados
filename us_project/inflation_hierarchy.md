# US inflation — data hierarchy

Built live on 2026-08-18 from the primary sources through [`connectors/bls.py`](../connectors/bls.py),
not from documentation. Companion to [`inflation_fontes_dados.md`](inflation_fontes_dados.md), which
maps *what exists*; this file maps *how it nests*, which is what the table design depends on.

Machine-readable output, two files:

| File | Rows | What it is |
|---|---|---|
| [`cpi_item_hierarchy.tsv`](cpi_item_hierarchy.tsv) | 294 | The **expenditure tree** — the full statistical structure of the CPI, 9 levels deep |
| [`cpi_headline_hierarchy.tsv`](cpi_headline_hierarchy.tsv) | 21 | The **news-release tree** — food / energy / core goods / core services, how the CPI is actually read |

Both carry level, parent, both weights (CPI-U and CPI-W), the SA and NSA series ids and each one's
coverage window. Everything below is derived from them and reproduces by re-running the connector.

**Two structural facts worth having up front.** First, **the CPI has two different trees, not one**,
and neither is a subset of the other's presentation — section 1 is the statistical hierarchy, section
2 is the analytical one the market and the Fed read, and they draw on different parts of the source.
Second, **only the CPI has a real hierarchy at all**: every other US price measure in this branch is
flat (a handful of headline series) or nests on a completely different principle (NAICS industry
codes, commodity groups). There is no single tree that holds "US inflation" the way `inflc_dim` holds
the IPCA.

---

## 1. CPI expenditure tree — the full statistical structure

**9 levels, 294 items, additive.** Level 0 is "All items"; level 1 is the eight major groups; the
tree runs to level 8 (e.g. `All items > Food and beverages > Food > Food at home > Meats, poultry,
fish and eggs > Meats, poultry, and fish > Meats > Pork > Ham`).

| Level | Items | Σ weight (CPI-U) | With a published series |
|---|---|---|---|
| 0 | 1 | 100.000 | 1 |
| 1 | 8 | 100.000 | 8 |
| 2 | 25 | 99.998 | 25 |
| 3 | 76 | 99.055 | 68 |
| 4 | 105 | 81.406 | 88 |
| 5 | 24 | 13.592 | 24 |
| 6 | 32 | 7.437 | 32 |
| 7 | 15 | 2.869 | 15 |
| 8 | 8 | 0.979 | 8 |

Levels 0-2 in full, with the 2024 weights priced to December 2025 (CPI-U), the item code, the
seasonally adjusted series id, and the first year of the NSA series:

```
All items                                    100.000  SA0     CUSR0000SA0      1913
  Food and beverages                          14.539  SAF     CUSR0000SAF      1967
    Food                                      13.698  SAF1    CUSR0000SAF1     1913
    Alcoholic beverages                        0.840  SAF116  CUSR0000SAF116   1952
  Housing                                     44.469  SAH     CUSR0000SAH      1967
    Shelter                                   35.625  SAH1    CUSR0000SAH1     1952
    Fuels and utilities                        4.546  SAH2    CUSR0000SAH2     1952
    Household furnishings and operations       4.298  SAH3    CUSR0000SAH3     1967
  Apparel                                      2.368  SAA     CUSR0000SAA      1913
    Men's and boys' apparel                    0.588  SAA1    CUSR0000SAA1     1935
    Women's and girls' apparel                 0.928  SAA2    CUSR0000SAA2     1935
    Footwear                                   0.585  SEAE    CUSR0000SEAE     1935
    Infants' and toddlers' apparel             0.103  SEAF    CUSR0000SEAF     1947
    Jewelry and watches                        0.163  SEAG    CUSR0000SEAG     1986
  Transportation                              16.316  SAT     CUSR0000SAT      1935
    Private transportation                    14.832  SAT1    CUSR0000SAT1     1935
    Public transportation                      1.485  SETG    CUSR0000SETG     1935
  Medical care                                 8.423  SAM     CUSR0000SAM      1935
    Medical care commodities                   1.489  SAM1    CUSR0000SAM1     1935
    Medical care services                      6.935  SAM2    CUSR0000SAM2     1935
  Recreation                                   5.137  SAR     CUSR0000SAR      1993
    Video and audio                            1.053  SERA    CUSR0000SERA     1993
    Pets, pet products and services            1.158  SERB    CUSR0000SERB     1997
    Sporting goods                             0.526  SERC    CUSR0000SERC     1977
    Photography                                0.064  SERD    CUSR0000SERD     1997
    Other recreational goods                   0.380  SERE    CUSR0000SERE     1997
    Other recreation services                  1.841  SERF    CUSR0000SERF     1997
    Recreational reading materials             0.114  SERG    CUSR0000SERG     1977
  Education and communication                  5.846  SAE     CUSR0000SAE      1993
    Education                                  2.602  SAE1    CUSR0000SAE1     1993
    Communication                              3.244  SAE2    CUSR0000SAE2     1993
  Other goods and services                     2.902  SAG     CUSR0000SAG      1967
    Tobacco and smoking products               0.445  SEGA    CUSR0000SEGA     1935
    Personal care                              2.456  SAG1    CUSR0000SAG1     1935
```

Note how uneven the tree is: **Housing is 44.5% of the index and Shelter alone is 35.6%**, while
Apparel is 2.4% across five children. A decomposition chart that gives each major group equal visual
weight will misrepresent the index.

### The hierarchy has to be assembled — no source publishes it

Three primary-source pieces, none of which contains the tree on its own:

| Piece | Source | Gives | Missing |
|---|---|---|---|
| Item catalogue | `cu.item` flat file | 400 item codes, names, `display_level`, sort order | no parent column; no weights; and its own levels have defects (below) |
| Series catalogue | `cu.series` flat file | which items have an SA and/or NSA series, and each one's begin/end | no hierarchy, no weights |
| Relative importance | `relative-importance/<year>.xlsx` | the weight of every item, CPI-U and CPI-W, and an `indent_level` | keyed by **item name**, not item code |

The parent of a node is inferred from the indentation: walking the rows in published order, a node's
parent is the nearest preceding node one level shallower. Both the flat file and the weights table
support that walk, and neither has an illegal level jump.

### Validated, not assumed

- **Additivity: 90 of 90 parents, maximum deviation 0.001** — every parent's weight equals the sum of
  its children's, to published rounding. This is the property a decomposition depends on, and it is
  the test that proves the inferred tree is the real one.
- **Name → code join: 269 of 294 (91.5%), zero ambiguity.** The weights table is keyed by name and
  everything else by code, so this join is unavoidable. All 25 misses are structural, not sloppy
  matching: 21 are BLS's `Unsampled …` residual categories, the rest are priced items with no
  national index of their own (`Housing at school, excluding board`, `Care of invalids and elderly at
  home`, `Technical and business school tuition and fees`). **Unmatched weight mass is 2.35% of the
  index and 0.00% at level 1.**
- **Series coverage: 269 items have a published national series** — 230 with both SA and NSA, 39 NSA
  only. NSA history reaches 1913 for the headline. The **179 leaves that have a series carry 97.65% of
  the index**, which is the practical ceiling for a bottom-up decomposition.

### Two published nodes are misindented — the weights prove it

Taking the published indentation literally breaks additivity in exactly four places, which resolve
into two offsetting pairs. In both cases the arithmetic settles the correct parent, so this is a fix,
not a judgement call:

- **`Alcoholic beverages` (SAF116)** is published as a sibling of `Food at home`, i.e. a child of
  `Food`. But `Food and beverages` (14.539) = `Food` (13.698) + `Alcoholic beverages` (0.840). It is a
  child of **Food and beverages**. Note `cu.item` makes the same error independently — it puts SAF116
  at the same `display_level` as SAF11.
- **`Information technology, hardware and services` (SEEE)** is published as a sibling of
  `Information and information processing`. But `Information and information processing` (3.181) =
  `Telephone services` (1.466) + `Information technology, hardware and services` (1.714), and
  `Communication` (3.244) = `Postage and delivery services` (0.064) + `Information and information
  processing` (3.181). It is a **child of Information and information processing**. Left uncorrected
  it double-counts 1.7pp of the index.

Both corrections are applied in `cpi_item_hierarchy.tsv` and are the only two hard-coded overrides.

### Also worth knowing before building on this

- **`cu.item.display_level` is not the same depth as the weights table's `indent_level`.** The offset
  is exactly +1 for 266 of 269 matched items, because the flat file treats the eight major groups as
  level-0 roots — **`SA0` "All items" is a *sibling* of the major groups there, not their parent**, so
  the flat file is a forest and the tree root has to be synthesised. The three exceptions are `SA0`
  itself and `Poultry`/`Chicken`, where the flat file puts them one level deeper than their own
  siblings. Where the two sources disagree, **the weights table wins** — it is the one that has to
  add up, and it does.
- **The weight vector is annual, not monthly.** Each xlsx is a December snapshot (`2025.xlsx` = 2024
  expenditure basket priced to December 2025) and the basket is only labelled from 2022 on; 2020-2021
  are biennial and carry no label. Weights are published for **2020-2025** only, so a
  weight-dependent decomposition currently cannot reach before 2020 without the separate 1947-1986
  historical file. This is the sharpest contrast with Brazil, where SIDRA publishes a weight per
  subitem per month.
- **Weights move enough to matter**: Housing went 42.385 → 44.469 and Food and beverages 15.157 →
  14.539 between the 2020 and 2025 files. Using one year's weights across the whole sample is a
  visible error, not a rounding one.
- **The tree covers CPI-U and CPI-W in the same file** (the `population` column). CPI-W is the
  indexation index for Social Security; CPI-U is the headline.

---

## 2. CPI news-release tree — how the US actually reads its CPI

Different tree, same 400-item universe. This is the structure of the CPI news release: **food,
energy, and core, then core split into goods and services**. It is what the Fed talks about, what
moves markets on release day, and what "core services ex-shelter" is carved out of. Four levels, 21
nodes — in [`cpi_headline_hierarchy.tsv`](cpi_headline_hierarchy.tsv):

```
All items                                       100.000  SA0      CUSR0000SA0      1913
  Food                                           13.698  SAF1     CUSR0000SAF1     1913
    Food at home                                  8.325  SAF11    CUSR0000SAF11    1947
    Food away from home                           5.373  SEFV     CUSR0000SEFV     1953
  Energy                                          6.383  SA0E     CUSR0000SA0E     1957
    Energy commodities                            3.120  SACE     CUSR0000SACE     1957
      Gasoline (all types)                        2.895  SETB01   CUSR0000SETB01   1935
      Fuel oil                                    0.083  SEHE01   CUSR0000SEHE01   1935
    Energy services                               3.262  SEHF     CUSR0000SEHF     1935
      Electricity                                 2.489  SEHF01   CUSR0000SEHF01   1913
      Utility (piped) gas service                 0.773  SEHF02   CUSR0000SEHF02   1935
  All items less food and energy                 79.919  SA0L1E   CUSR0000SA0L1E   1957
    Commodities less food and energy commodities 19.176  SACL1E   CUSR0000SACL1E   1957
      New vehicles                                3.838  SETA01   CUSR0000SETA01   1935
      Used cars and trucks                        2.759  SETA02   CUSR0000SETA02   1952
      Apparel                                     2.368  SAA      CUSR0000SAA      1913
      Medical care commodities                    1.489  SAM1     CUSR0000SAM1     1935
    Services less energy services                60.744  SASLE    CUSR0000SASLE    1957
      Shelter                                    35.625  SAH1     CUSR0000SAH1     1952
      Transportation services                     6.315  SAS4     CUSR0000SAS4     1935
      Medical care services                       6.935  SAM2     CUSR0000SAM2     1935
```

All 21 nodes resolve to an item code, and **all 21 have both an SA and an NSA series** — no gaps,
unlike the expenditure tree. History reaches 1957 for the core aggregates (`SA0L1E`, `SACL1E`,
`SASLE`, `SA0E` all start there) and 1913 for All items, Food and Electricity.

### This tree is declared, not inferred — and here is why that is the honest way to build it

The expenditure tree could be walked out of the published indentation because it adds up. This one
cannot: **the published indentation of the weights file's "Special aggregate indexes" section is
presentational and semantically wrong.** It nests `Energy commodities` *inside* `Commodities less food
and energy commodities` — a category that by definition excludes energy commodities. Inferring
parents from that indentation would produce a tree that is arithmetically impossible.

So the 21-node structure is stated explicitly and then **validated against the weight identities**,
which is the test that actually proves it. All of them close:

| Identity | Computed | Expected |
|---|---|---|
| Food + Energy + core = All items | 100.000 | 100.000 |
| Food at home + Food away from home = Food | 13.698 | 13.698 |
| Energy commodities + Energy services = Energy | 6.382 | 6.383 |
| Electricity + Utility gas = Energy services | 3.262 | 3.262 |
| Core goods + core services = core | 79.920 | 79.919 |

### The one trap: this tree is not exhaustive at its bottom level

Three parents show only their largest children, by design of the release. The missing mass is large:

| Parent | Own weight | Children shown | Residual |
|---|---|---|---|
| Energy commodities | 3.120 | 2.978 | 0.142 |
| Commodities less food and energy commodities | 19.176 | 10.454 | **8.722** |
| Services less energy services | 60.744 | 48.875 | **11.869** |

**A decomposition built only on this tree's leaves accounts for 79.3 of 100 points of the index.** The
residual has to be shown as an explicit "other" bar, not dropped — otherwise the chart silently loses
21% of the index, most of it in core services, which is exactly the part under discussion in 2026. The
expenditure tree in section 1 is what fills those gaps when the detail matters (its 179
leaves-with-series cover 97.65%).

The release table continues past the rows above with a few more aggregates (education and
communication services, other personal services, and cuts like "All items less shelter"); they build
the same way — declare the parent, pull the weight by name, check the identity.

---

## 3. Everything else in the branch is flat, or nests differently

| Measure | Source | Hierarchy | Depth |
|---|---|---|---|
| **CPI-W** | `cw` flat files | Same 400-item structure as `cu` | 9 levels, identical shape |
| **C-CPI-U** (chained) | `su` flat files | `su.item` has **29 items only** — headline, major groups, a few aggregates | 1999→, effectively 2 levels |
| **PPI commodity** | `wp` flat files | **`wp.group` (55 groups) × `wp.item` (4,013 items)** — two levels, no `display_level` at all. 5,311 series (4,013 NSA + 1,298 SA) | 2 levels |
| **PPI industry** | `pc` flat files | **998 NAICS industries × products**, and the hierarchy is encoded in the *code length*, not a column: `1133--` → `11331-` → `113310` are the 4/5/6-digit levels | 3 levels, implicit |
| **Import/export prices** | `ei` flat files | `ei.index`, not an item tree (no `ei.item` — that path 404s) | flat |
| **PCE price index** | BEA | NIPA table structure; component detail needs the **BEA key** we don't have. FRED carries only headline and core | not mapped |
| **Cores** (median, trimmed-mean, sticky) | Cleveland / Dallas / Atlanta Feds | Single series each, no components published | flat |
| **Expectations** (breakevens, Michigan, NY Fed SCE, Cleveland model) | Treasury / UMich / NY Fed / Cleveland | Single series per horizon | flat |

Two consequences for the report design. First, **PPI cannot reuse the CPI tab's machinery** — 4,013
items in a two-level grouping is a different navigation problem from 294 items in nine levels, and the
industry-vs-commodity split means two incompatible trees for the same survey. Second, the
much-discussed CPI-vs-PCE comparison is **headline-only** until the BEA key exists; there is no
component-level bridge between the two without it.

---

## 4. Proposed `macro_us` tables

Mirrors the Brazil pair (`inflc_decomposicao` + `inflc_dim`) with the naming convention already in
use, but splits the weights out because the US publishes them on a different frequency than the
indices.

| Table | Primary key | Holds |
|---|---|---|
| `inflc_cpi_dim` | `(arvore, item_code)` | The trees: `item_name`, `level`, `parent_item_code`, `path`, `series_sa`, `series_nsa`, coverage window, `is_leaf`. `arvore` = `despesa` / `divulgacao` — both trees live here, keyed apart, since the same item code sits at a different level and under a different parent in each (`Apparel` is a level-1 major group in one and a level-3 core-goods component in the other). These are the two TSVs |
| `inflc_cpi` | `(date, indice, item_code, ajuste)` | The index levels and monthly variation. `indice` = `CPI-U`/`CPI-W`/`C-CPI-U`, `ajuste` = `SA`/`NSA` — the SA/NSA distinction has to be in the key, not folded away, since only 230 of 269 items have both |
| `inflc_cpi_pesos` | `(reference_period, indice, item_code)` | The weight vector, one row per December snapshot per population |

**Why weights get their own table rather than a column on the monthly rows, as in Brazil:** the BLS
publishes one weight per item per year, so writing it onto every month would either duplicate it
twelvefold or imply a monthly weight that was never published. Contribution (= variation × weight)
then becomes an explicit, documented join choice — carry December's weight forward through the next
year, which is what the BLS's own construction implies — instead of a silent one baked into the
schema. `contribuicao` should be computed at read time in the report, not stored, until that
convention is settled.

**Tested, and the per-year weights are worth the extra table.** Rebuilding the headline monthly
variation from the three level-1 nodes (Food, Energy, core) over 2020-2026 and comparing with the
published headline:

| Weight basis | Mean abs. gap | Max |
|---|---|---|
| One snapshot (2025) for the whole sample | 0.0186pp | 0.1368pp |
| Each year's own snapshot | **0.0147pp** | 0.1074pp |

Joining each month to its own year's weights **cuts the reconciliation error by 21%**. The level-1
weights move enough to matter: Energy ran 6.155 → 7.348 → 6.383 across the 2020, 2021 and 2025 files.

The remaining ~0.015pp is irreducible from published data and worth knowing before anyone treats a
decomposition as an identity: the relative importance is a *December snapshot* of a quantity the BLS
price-updates continuously, so no single vector reproduces every month exactly. It is **not** a
seasonal-adjustment artefact — repeating the test on NSA series gives a slightly *worse* gap (0.0191pp),
which rules that explanation out.

Two further design points that follow from the findings above: the `ajuste` dimension belongs in the
key because SA coverage is incomplete, and any decomposition tab should be built on the **179
leaves-with-series** (97.65% of the index) with the residual shown explicitly rather than hidden.

---

## Open items

- ~~Register a free `BLS_API_KEY`~~ — **done 2026-08-18**, in `.env`. Verified live: the caps really
  are 50 series / 20 years (measured, not just documented), and `catalog`/`calculations` now work —
  `calculations=True` returns BLS's own 1/3/6/12-month percent changes per observation.
- **Extend the news-release tree** past the 21 nodes above with the remaining release-table
  aggregates (education and communication services, other personal services, "All items less
  shelter"), and decide whether "core services ex-shelter" — the current policy focus, and *not* a
  published series — gets built from `Services less energy services` minus `Shelter` using these
  weights.
- **Weights before 2020** — `historical-relative-importance-1947-1986.xlsx` exists (13 sheets by year
  range, different format, not yet parsed) and a 1987-1989 zip; **1990-2019 has no file on the BLS
  page**. Until that gap is filled, a weighted decomposition starts in 2020 while the index series
  themselves reach 1913.
- **Decide the weight-carry convention** (December snapshot forward through the following year) and
  whether `contribuicao` is stored or computed.
- **Get the BEA key** for PCE component detail — without it the CPI/PCE comparison stays headline-only.
- **Not mapped this round**: regional and metro CPI cuts (`cu.area` has the area codes and Tables 2-6
  of the weights file have the matching weights), the PPI item tree in detail, `ei.index`, and the
  R-CPI-E (elderly) variant, which has its own weights files (`r-cpi-e-<year>.xlsx`).
