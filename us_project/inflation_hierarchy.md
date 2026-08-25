# US inflation — data hierarchy

Built live on 2026-08-18 from the primary sources through [`connectors/bls.py`](../connectors/bls.py),
not from documentation. Companion to [`inflation_fontes_dados.md`](inflation_fontes_dados.md), which
maps *what exists*; this file maps *how it nests*, which is what the table design depends on.

Machine-readable output, two files:

| File | Rows | What it is |
|---|---|---|
| [`cpi_item_hierarchy.tsv`](cpi_item_hierarchy.tsv) | 294 | The **expenditure tree** as the relative-importance spreadsheet publishes it, 9 levels deep. **Not the deepest layer** — see §1b; the loaded version in `macro_us.inflc_cpi_dim` is 355 items over 10 levels |
| [`cpi_newsrelease_table1.tsv`](cpi_newsrelease_table1.tsv) | 37 | The **news-release tree** — food / energy / core goods / core services, how the CPI is actually read. Extracted from Table 1 of the release, where BLS declares the hierarchy in its own markup |

Both carry level, parent, weights, the SA and NSA series ids and each one's measured coverage window.
The news-release file adds the release's published values (monthly relative importance, the three
unadjusted indexes, y/y and m/m, three months of seasonally adjusted m/m) and a `decomposition` column
flagging whether a parent's shown children add up to it. Everything below is derived from these two
files and reproduces by re-running the connector.

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

### 1b. The spreadsheet is not the bottom of the tree

Found 2026-08 while checking the report against the release: `cu.item` carries **400** item codes, and
the expenditure tree above uses 267 of them. Of the 133 left over, 40 are special aggregates (a
different tree — §3) and 2 are old-base series, but **83 are genuine deeper items with published index
series** that the relative-importance spreadsheet simply does not list:

| Parent in the spreadsheet | What sits below it, unlisted |
|---|---|
| Gasoline (all types) | unleaded regular, unleaded midgrade, unleaded premium |
| Coffee | roasted coffee, instant coffee |
| New vehicles | new cars, new trucks (and, discontinued, new cars and trucks / new motorcycles) |
| Milk | fresh whole milk, fresh milk other than whole |
| Bread | white bread, bread other than white |
| Hospital services | inpatient hospital services, outpatient hospital services |
| Telephone hardware / education | smartphones, college textbooks |

All 83 have an NSA series; 60 also have SA. Median start 1997, earliest 1935. Seventeen are
discontinued (last observations from 1998 to 2026), which is a fact about the series, not a load gap.

They have **no published weight** at all — the spreadsheet is where weights come from, and it stops
above them. So they support Index / Y-Y / M-M / 3M and cannot support contribution, and they cannot be
part of any additivity check. That is why the loaded table carries a `tem_peso` flag rather than
pretending the two layers are the same thing.

Parentage comes from the same rule used for the rest, applied to `cu.item`'s own publication order: the
last preceding line one `display_level` up. **Validated before use** — on the 266 items the spreadsheet
already positions, the rule reproduces the published parent in 254, and all 12 disagreements are items
whose true parent is a special aggregate (the 8 level-1 groups under the synthesised root, plus 4 where
`cu.item` omits the intermediate SA level). None sits at the depth the graft touches, so the graft only
adds leaves and never moves a spreadsheet-placed item.

Three `cu.item` entries stay out on purpose: `Information technology commodities` (SEEEC), `Video and
audio products` (SERAC) and `Video and audio services` (SERAS). They arrive at `display_level` 1, which
would make them children of *All items*, and they are in neither section of the spreadsheet —
cross-cutting aggregates with nowhere to go in this tree.

### 1b-bis. The monthly relative importance does not need to be scraped

The relative-importance workbook is annual (December), but Table 1 of every monthly release prints a
relative importance dated one month behind its reference month, and the two differ materially — Energy was
6.383 in the December 2025 workbook against 7.432 in the July 2026 release. That looked like a loading gap
until it turned out to be an arithmetic one: the monthly figure is the December weight updated by the
item's own NSA index ratio since that December, divided by the All-items ratio over the same span. Checked
against the July 2026 release, all **37** printed figures come back within **0.0008**, and the eight
level-1 groups still sum to 100.000 after being updated one at a time. So the release's weight column is
reproducible from what is already loaded, for any item that has a December weight — 265 of the 355
expenditure items.

### 1c. Five items were lost to a label mismatch

Also found 2026-08. The spreadsheet and `cu.item` disagree on five labels, and a name join drops the
item silently:

| In the spreadsheet | In `cu.item` | Code | Weight |
|---|---|---|---|
| Housing at school, excluding board | Lodging while at school | SEHB01 | 0.221 |
| Men's underwear, nightwear, swimwear**,** and accessories | …swimwear and accessories | SEAA02 | 0.130 |
| Women's underwear, nightwear, swimwear**,** and accessories | …swimwear and accessories | SEAC04 | 0.234 |
| Care of invalids and elderly at home | Home health care | SEMD03 | 0.230 |
| Technical and business school tuition and fees | Technical and vocational school tuition and fixed fees | SEEB04 | 0.046 |

0.861 index points, each with both a weight and a series published, invisible until the mismatch was
resolved. Each pair was confirmed **by position**, not by resemblance: every unmatched spreadsheet line
has exactly one `cu.item` candidate sitting between its coded neighbours in publication order, and for
the two underwear rows the API's own `series_title` carries the *spreadsheet's* spelling, which settles
which label is stale. The weight-additivity proof passed before and after (90/90), because it runs on
names and always counted these rows.

---

## 2. CPI news-release tree — how the US actually reads its CPI

Different tree, same 400-item universe. This is the structure of **Table 1 of the CPI news release**
([`cpi.t01.htm`](https://www.bls.gov/news.release/cpi.t01.htm)): food, energy, and core, then core
split into goods and services. It is what the Fed talks about, what moves markets on release day, and
what "core services ex-shelter" is carved out of. **37 rows, 5 levels (0-4)**, in
[`cpi_newsrelease_table1.tsv`](cpi_newsrelease_table1.tsv).

### This tree is declared by BLS, not inferred by us

The expenditure tree in section 1 had to be assembled and then proved by arithmetic. This one does not:
**BLS ships the hierarchy inside the release page's own markup.** Each row label is wrapped in
`<p class="subN">`, where `N` is the depth, and each row carries a hierarchical id
(`cpipress1.r.1`, `cpipress1.r.1.1`, ...) whose parent is its own id minus the last segment. So depth
and parentage are both read off the source, not guessed from visual indentation.

That matters because inferring this tree from the *weights file* would fail. There, the
"Special aggregate indexes" section nests `Energy commodities` inside `Commodities less food and energy
commodities` — a category that by definition excludes energy commodities. The release page's markup has
none of that problem: it is the publisher's own parent-child statement.

The extraction was then checked against the API, which is the test that matters: **111 of 111 published
index values (Jul-2025, Jun-2026 and Jul-2026 for all 37 rows) match the series pulled by item code to
the third decimal, with zero mismatches.** Every row resolves to an item code and **every one of the 37
has both an SA and an NSA series** — no gaps, unlike the expenditure tree. Six of them are special
aggregates that do not exist in the expenditure tree at all (`SA0E`, `SACE`, `SA0L1E`, `SACL1E`,
`SASLE`, `SAS4`). History reaches 1913 for All items, Food and Electricity; 1957 for the core
aggregates.

### The structure, with July 2026 numbers

```
                                                code      RI Jun26   y/y%  sa m/m%   decomposition
All items                                       SA0        100.000    3.4      0.1   complete
  Food                                          SAF1        13.522    3.0      0.1   complete
    Food at home                                SAF11        8.231    2.7     -0.1   complete
      Cereals and bakery products               SAF111       1.023    2.7      0.2
      Meats, poultry, fish, and eggs            SAF112       1.959    1.9     -0.7
      Dairy and related products                SEFJ         0.743   -0.5     -0.1
      Fruits and vegetables                     SAF113       1.283    5.1     -0.1
      Nonalcoholic beverages                    SAF114       0.981    4.1      0.9
      Other food at home                        SAF115       2.242    2.5      0.0
    Food away from home                         SEFV         5.290    3.4      0.3
  Energy                                        SA0E         7.432   14.7     -1.5   complete
    Energy commodities                          SACE         4.132   24.7     -2.9   partial (0.055 unshown)
      Fuel oil                                  SEHE01       0.106   39.1     -1.7
      Motor fuel                                SETB         3.971   24.8     -3.0   partial (0.119 unshown)
        Gasoline (all types)                    SETB01       3.852   24.6     -2.9
    Energy services                             SEHF         3.300    4.3      0.3   complete
      Electricity                               SEHF01       2.552    4.2      0.1
      Utility (piped) gas service               SEHF02       0.748    4.3      0.7
  All items less food and energy                SA0L1E      79.047    2.5      0.2   complete
    Commodities less food and energy commod.    SACL1E      18.829    0.8      0.2   partial (7.282 unshown)
      Apparel                                   SAA          2.437    3.9      0.1
      New vehicles                              SETA01       3.751    0.5      0.1
      Used cars and trucks                      SETA02       2.679   -1.9      0.4
      Medical care commodities                  SAM1         1.412   -2.7     -0.6
      Alcoholic beverages                       SAF116       0.823    2.1      0.2
      Tobacco and smoking products              SEGA         0.445    6.7      0.5
    Services less energy services               SASLE       60.217    3.0      0.2   partial (11.721 unshown)
      Shelter                                   SAH1        35.304    3.2      0.1   partial (1.739 unshown)
        Rent of primary residence               SEHA         7.716    2.9      0.3
        Owners equivalent rent of residences    SEHC        25.849    3.2      0.3
      Medical care services                     SAM2         6.840    2.7      0.6   partial (3.024 unshown)
        Physicians services                     SEMC01       1.660    2.4      0.2
        Hospital services                       SEMD01       2.156    5.2      0.5
      Transportation services                   SAS4         6.352    2.9      0.3   partial (1.643 unshown)
        Motor vehicle maintenance and repair    SETD         1.048    6.6      0.6
        Motor vehicle insurance                 SETE         2.570   -4.5     -0.3
        Airline fares                           SETG01       1.091   25.5      2.2
```

(Labels above are the release's own, minus its footnote markers; the TSV keeps the exact strings.)

### Levels 0-2 are an exact partition; the detail rows are selective

This is the single most important structural fact for building a decomposition on this tree:

| Level | Nodes | Weights sum to |
|---|---|---|
| 0 (All items) | 1 | 100.000 |
| 1 (food / energy / core) | 3 | 100.001 |
| 2 (the six components) | 6 | 99.999 |
| 3 | 19 | 75.651 |
| 4 | 8 | 45.942 |

So **the top three levels each re-partition the whole index exactly** — a waterfall or contribution
chart built on any of them is complete and needs no residual. Below that it stops being a partition:
7 of the 13 parents show only their largest children, leaving **25.583 points of the index unshown**,
concentrated in exactly the places under discussion in 2026 — 11.721 inside core services and 7.282
inside core goods. The 24 leaf rows together account for only 74.4 of 100 points.

Consequence for the report: **charts at level <= 2 are exact; anything deeper needs an explicit "other"
bar**, computed as parent minus the sum of shown children, never dropped. The section-1 expenditure
tree is what fills those gaps when the detail matters (its 179 leaves-with-series cover 97.65%).

### The release publishes a *monthly* weight — and it is not the December one

The weight column in Table 1 is headed "Relative importance **Jun. 2026**", one month behind the
reference month. That is a different vector from the December snapshot in the annual xlsx, and the gap
is not noise:

| Node | Dec-2025 xlsx | Jun-2026 release | Diff |
|---|---|---|---|
| Food | 13.698 | 13.522 | -0.176 |
| **Energy** | 6.383 | **7.432** | **+1.049** |
| All items less food and energy | 79.919 | 79.047 | -0.872 |
| Energy commodities | 3.120 | 4.132 | +1.012 |
| Services less energy services | 60.744 | 60.217 | -0.527 |

Energy's weight rose 16% in relative terms over seven months, because relative importance is
price-updated continuously and energy prices ran +24.7% y/y. Using the December vector for a July
calculation therefore understates energy's weight by about a sixth. This is the same effect measured
in section 4's reconciliation test, seen directly.

**Monthly weight history is recoverable**, which was not previously established: the archived releases
carry the same table with their own RI column (`archives/cpi_01132026.htm` -> "Nov. 2025",
`archives/cpi_08122026.htm` -> "Jun. 2026"). The archive is keyed by exact release date
(`cpi_MMDDYYYY.htm`), so harvesting it needs the release-date calendar — a wrong date is a plain 404.
Left as an open item; the December xlsx remains the only weight source covering all 294 expenditure
items.

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
- **Extend the news-release tree** past Table 1's 37 rows using the release's later tables
  (Table 2 carries the further aggregates — education and communication services, other personal
  services, cuts like "All items less shelter"). They extract the same way: same `subN`/row-id markup.
  Still to decide: whether "core services ex-shelter" — the current policy focus, and *not* a
  published series — gets built as `Services less energy services` minus `Shelter`.
- **Weights before 2020 — the gap is a parsing job, not a data gap** (corrected 2026-08-18; an
  earlier round of this file wrongly said "1990-2019 has no file on the BLS page", having probed the
  `<year>.xlsx` pattern, which only exists from 2020). Reading the RI page's own link list instead of
  guessing URLs turns up continuous annual coverage back to 1947:

  | Period | File | Contents | Format |
  |---|---|---|---|
  | 2020-2025 | `<year>.xlsx` | 1 file/year, 7 tables | xlsx, **parsed** (`get_relative_importance`) |
  | 2010-2019 | `ri-archive-2010-2019.zip` | 35 entries, `<year>.txt` + `.pdf` | fixed-width, dot leaders, indentation = depth, **no item code** |
  | 2000-2009 | `ri-archive-2000-2009.zip` | 24 entries, same shape | same as 2010s |
  | 1990-1999 | `ri-archive-1990-1999.zip` | 10 `<year>.txt` | fixed-width **with an `Item code` column** — easier than the modern files, no name-matching needed |
  | 1987-1989 | `ri-archive-1987-1989.zip` | 3 `<year>.txt` | as 1990s |
  | 1947-1986 | `historical-relative-importance-1947-1986.xlsx` | 13 sheets by year range | xlsx, not yet parsed |

  All six were downloaded and opened live (magic bytes checked, entry lists read, two year-files
  parsed as samples). So a weighted decomposition can reach 1947 rather than 2020 — it costs two more
  parsers (the 1987-2019 fixed-width form and the 1947-1986 workbook), not new data access.
  `https://www.bls.gov/web/cpi/cpi-relative-importance.xlsx` is a "latest year" alias of the same
  annual file, not a separate monthly source.
- **Monthly weights** exist only for the news-release rows, recoverable from archived releases — see
  section 2's last subsection. `list_relative_importance_years()` reports 2020-2025 only, because it
  reads the `<year>.xlsx` links; it does not know about the decade archives.
- **Decide the weight-carry convention** (December snapshot forward through the following year) and
  whether `contribuicao` is stored or computed.
- **Get the BEA key** for PCE component detail — without it the CPI/PCE comparison stays headline-only.
- **Not mapped this round**: regional and metro CPI cuts (`cu.area` has the area codes and Tables 2-6
  of the weights file have the matching weights), the PPI item tree in detail, `ei.index`, and the
  R-CPI-E (elderly) variant, which has its own weights files (`r-cpi-e-<year>.xlsx`).
