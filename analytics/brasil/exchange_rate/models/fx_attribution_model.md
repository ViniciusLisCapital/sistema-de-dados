# FX Cause-Attribution Model — pilot

Turns qualitative FX commentary into a numeric time series: for each month,
how much of the narrative attributes BRL/USD moves to each of a fixed set of
causal regimes. Goal (stated 2026-07-29): classify exchange-rate "regimes"
(fiscal, monetary, global USD, ...) numerically from text, in a way that
generalizes to other text-scoring tasks later (e.g. Copom minutes
hawkish/dovish) — same extraction-schema idea, different taxonomy/target.

**Status: manual-extraction pilot, one corpus, full available history.**
`claims.csv` was hand-extracted by Claude reading each source document
directly in-session — there is no automated text-to-claim function yet.
`fx_attribution_model.py` only covers claims -> monthly matrix -> Excel
export.

## Corpus

Kinea Investimentos, **the entire archive available in
`repository/mental_model/`** as of 2026-07-29 — both of their monthly
publications: `repository/mental_model/kinea/` (the "Carta do Gestor" main
letter, ~monthly, end of month) and `repository/mental_model/kinea_insights/`
(a separate single-topic deep-dive piece, ~monthly, mid-month). **128 documents
total (62 `kinea` + 66 `kinea_insights`)**, listed in
`fx_attribution_data/kinea/documents.csv`, spanning **2021-05 through 2026-08
(64 calendar months)**. Coverage is uniform from 2022 on; the irregularity is
confined to the archive's opening year:

**All of the per-year counts below are on the reference month** (the month a
letter covers), which is what `month` holds since 2026-09-08. They read very
differently from the publication-month counts this section used to carry —
see the correction note after the list.

- 2021: the archive starts mid-year — first `kinea` letter is 2021-05-16,
  first `kinea_insights` is 2021-05-18. May 2021 genuinely has two main
  letters ("A primavera da esperança," May 16, and "Da primavera ao verão
  econômico," May 17 — seventeen days apart, the one real double in the
  archive). `kinea` then has a true **Jun-Aug gap** and covers Sep-Dec (the
  December letter is the one published 2022-01-03); 6 letters over 5 distinct
  months. `kinea_insights` covers May-Dec (9 issues, May doubled).
- 2022: `kinea` has **12 main letters in 12 distinct months** — no collision,
  no gap. `kinea_insights` has all 12 months.
- 2023: `kinea` has **12 main letters in 12 distinct months**.
  `kinea_insights` has all 12 months.
- 2024: **12 main letters in 12 distinct months.** This year used to read as
  "April missing, November doubled" — both documents are real, but "O
  Alquimista" (published Nov 1) is the **October** letter, and moving it
  closes the April-to-November run at the same time. `kinea_insights` covers
  all 12 months.
- 2025: complete — 12 main letters in 12 months, plus two `kinea_insights`
  issues in December (2025-12-15 and 2025-12-19, the latter in English, see
  below).
- 2026: the archive runs through August 2026 (see the 2026H2 refresh section
  below). **Exactly one issue of each series per month, Jan through Ago** —
  "Dr. Strangelove" (published 01/08) is the Jul/2026 letter and "A hora do
  pesadelo" (31/08) is the Ago/2026 one. Before the 2026-09-08 month
  migration these two stacked into Ago/2026 and left Jul/2026 empty, which is
  what made the defect visible.

**The "double-letter-in-one-month pattern" was an artifact, and this paragraph
used to assert the opposite.** It read: *recurs often enough across years that
it reads as a genuine, if irregular, Kinea publishing habit rather than a
one-off.* Wrong. Those months (2022 Jan/Oct, 2023 Jan/Apr/Aug, 2024 Nov, 2026
Apr/Ago) were the old publication-month convention filing a letter one month
late, on top of the next one. Keyed on the covered month, **2022 through 2026
are uniform — 12 main letters in 12 distinct months every full year, zero
collisions and zero gaps** (2026 is 8 in 8 through August); corpus-wide the
count goes from 10 collision months and 12 empty months to **1 and 3**. Kinea's
real habit is one main letter per closed month, published in that month's last
days or the next month's first few. The only genuine double is **May 2021**,
the archive's opening, and the only genuine gap is **Jun-Aug 2021**, before the
series settled.

The reusable half: **a corpus statistic can manufacture a finding about the
source when the indexing convention is wrong**, and the more consistently the
convention is applied, the more solid the false finding looks — here it
survived long enough to be written up twice as a property of how Kinea
publishes. The check that catches it is structural, not textual: count
documents per bucket, and distrust any source that publishes N per period yet
produces buckets of 2 and 0. Verde and Kapitalo were audited the same way on
2026-09-08 and are clean (see below).

**Verde and Kapitalo were checked against an independent source, not just
re-read.** Both encode the reference month in the source filename
(`Verde-REL-YYYY_MM.md`, `kapitalo_k10_MMYYYY.md`), so the filename validates
the `month` column without coming from the same place: **0 mismatches in 200
and 85 documents**, no month with two documents, no empty month in either span.
Their publication lag is the tell that the two columns are genuinely different
things and both are right — Verde publishes one month after the covered month
in 199 of 200 cases (the exception is Jul/2011, published 2011-09-26, which
matches that PDF's own `/CreationDate` exactly, so it is a genuinely late
letter and not an error), while Kapitalo has a lag of exactly zero by
construction, since its `date` is a placeholder (the covered month's last day)
rather than a recovered publication date — its PDFs carry no `/CreationDate`.
`claims.csv` agrees with `documents.csv` on `(source_file, month, date)` for
every claim in all three managers, with no orphan claims.

**Language shift, late 2025.** `kinea_insights_19122025.md` ("The Hidden Side
of Artificial Intelligence") is the first document in the corpus written in
English rather than Portuguese — a real change in Kinea's own publishing
practice at that point, not a data artifact. Per the project's language rule,
its source text stayed in English and wasn't translated; all extraction
notes in `claims.csv` are already written in English regardless of source
language, so nothing about the pipeline itself needed to change.

**Writing-style shift, 2026.** The 2026 `kinea` main letters are noticeably
more FX-explicit than any prior year — they now routinely name "a moeda" or
"o BRL" directly with a stated mechanism (carry differential, capital flows,
terms-of-trade windfall, risk sentiment), often as its own subsection, rather
than leaving the currency implication to be inferred from a broader macro
discussion the way 2021-2024 letters mostly did. This shows up directly in
the claim count. Measured per main letter, after the 2026-09-08
re-extraction and month migration: 2021 1.3 · 2022 1.1 · 2023 1.1 · 2024 1.8 ·
2025 1.5 · **2026 2.5** (8 letters, 20 claims). The gap is real but smaller
than this note first claimed — it read "nearly a claim per category per
letter," which 2.8 claims across a 9-category taxonomy never supported. Whether this reflects a genuine change
in how Kinea writes, or just a coincidence of an eventful first half of 2026
(an Iran/Strait-of-Hormuz oil shock, a hawkish Fed transition under Kevin
Warsh, a tense Brazilian election year), isn't something a single
half-year of data can settle — worth revisiting once more 2026 issues exist.

## Taxonomy (fixed, defined upfront)

| Category | Definition | Boundary |
|---|---|---|
| `fiscal_br` | BR deficit/debt trajectory, spending/revenue measures, fiscal rule | numeric/legislative, not popularity |
| `monetary_br` | Selic level/path, BCB guidance, BR-US real rate differential | the carry channel specifically |
| `politics_br` | Elections, Congress, judicial rulings, popularity, policy unpredictability | non-numeric political risk |
| `global_usd` | Broad dollar strength/weakness from the US side — Fed, US fiscal, US politics/institutions, "exceptionalism," de-dollarization | absorbs *why* the dollar moved; BRL-effect is what's scored, not the dollar's own direction |
| `commodities` | Iron ore, soy, oil, agri, energy prices; current-account/external-accounts dynamics (trade balance, terms-of-trade-driven USD inflow) | same causal mechanism expressed in balance-of-payments terms rather than price terms -- see resolution note below |
| `risk_sentiment` | VIX, safe-haven flows, EM-wide risk appetite not tied to commodities or USD mechanics | |
| `china_em` | Chinese stimulus/property/growth as commodity-demand and EM-sentiment driver | |
| `trade_policy` | Direct tariff actions (on Brazil or globally) | distinct from the USD/risk-sentiment channel it triggers |
| `capital_flows` | Explicit flow/positioning claims, not fundamentals | rarely populated in this narrative-style corpus |

**Resolved 2026-07-29 — the flagged possible tenth category.** March 2024 had
a long BRL claim citing "carrego elevado e melhora estrutural na conta
corrente" (elevated carry **and** structural current-account improvement) as
joint drivers, originally filed entirely under `monetary_br` with a note
flagging the current-account half as taxonomy-orphaned. Resolution (user
call): don't add a tenth category — fold it into `commodities`, renamed
`commodities` → **"Commodities / terms of trade / external accounts."**
Rationale: higher commodity prices and higher export volumes both mean more
USD flowing into Brazil, which shows up in the current account — it's the
same underlying cause (export-driven USD inflow), just expressed in
balance-of-payments terms in one telling and price/volume terms in another,
not a genuinely distinct regime. The March 2024 claim was split into two rows
in `claims.csv` accordingly: the carry/activity half stays `monetary_br`
(0.7), the current-account half is now `commodities` (0.7).

**Sign convention:** direction scores the claim's implied effect **on BRL**,
never on the claim's own subject. +1 = strongly BRL-appreciation-supportive,
-1 = strongly BRL-depreciation-driving. A claim that "the dollar is
strengthening globally" is scored **negative** (bad for BRL), not positive —
got this backwards once during calibration; worth restating because it's an
easy sign error to reintroduce later.

## Extraction rules

1. **FX must be the effect, not a cited cause of something else.** Kinea
   sometimes cites a past BRL move as the cause of a political outcome (e.g.
   "Lula's popularity fell because of BRL's depreciation and the Pix crisis")
   — that's reverse of what this model measures and is excluded.
2. **The text must explicitly connect the cause to a currency/FX effect**
   (câmbio, real, dólar, moeda) — not merely discuss a topic (fiscal,
   tariffs, China) that would *plausibly* affect FX by economic logic.
   Requiring the manager's own words to draw the link, rather than applying
   our own economic priors, is what makes this a measure of what managers
   attribute, not what theory would imply.
3. **One claim per (category, direction/timeframe) per document, not per
   sentence.** A single letter often restates the same causal argument two
   or three times in different words — counting each restatement inflates
   the sum through verbosity rather than genuine signal. Same-direction
   elaborations within a document merge into one claim; genuinely opposing
   claims in the same letter (e.g. "USD weakened this month" *and* "USD
   should strengthen going forward") stay separate, since they're different
   arguments, not restatements.
4. **A regional/bilateral FX move is not "Global USD"** unless the text
   frames dollar weakness/strength as broad/global. A passage about European
   currencies specifically strengthening vs. USD on German fiscal news, with
   no broader dollar narrative, was excluded on this basis.
5. **Own positioning is not itself an attribution claim.** "We are short
   real, as a hedge" states a trade, not a cause. It only counts once the
   text gives an explicit reason ("... em virtude do elevado diferencial de
   juros") — the reason is the claim, not the position.
6. **A claim can score 0 deliberately** — e.g. "BRL floated without a clear
   trend despite risk-off" is a real, explicit statement that a channel did
   *not* move the currency this time, which is meaningfully different from
   that channel never being discussed at all (which is simply absent from
   `claims.csv`, contributing nothing to the sum by omission).

## Aggregation: monthly sum, not mean

Per category per calendar month, claims are **summed**, not averaged — the
same net hawkish-minus-dovish convention used in central-bank text scoring.
This has a useful property: a month with zero claims in a category sums to
0, which is mathematically the *correct* "no net signal" value — it doesn't
need special-casing against a "neutral" claim, because there isn't one.

The one thing sum-by-itself can't tell you: 0 from **silence** vs. 0 from
**genuine claims that canceled out**. April 2025's `global_usd` = 0.0 is two
real, opposing claims in the same letter (USD weakening now / USD should
strengthen ahead), not nothing being said. `monthly.csv` and the Excel
export both carry `n_documents` and `n_claims` alongside every month's
scores specifically so this distinction is never lost by looking at the sum
alone. Planned fix once this becomes a chart: a stacked bar per category
(not a single blended line) so which categories are actually contributing
each month is visible directly, rather than inferred from a footnote column.

## Findings from the full-history run (101 claims, 124 documents, 2021-05 to 2026-06)

> **Snapshot, not current state.** These counts and percentages are the
> 2026-07-29 full-history run and are kept as written. The corpus is now
> 128 documents / 104 claims through Ago/2026, and every `month` here is a
> publication month — the reference-month migration of 2026-09-08 (see
> Corpus above) moved 18 documents and 27 claims. The findings below hold
> in substance (category shares, `trade_policy` never firing, the rule-6
> zeros); the arithmetic is of that run.

- **`trade_policy` is the only category that has never fired once, across
  five-plus years** — despite Trump tariffs (both the 2018-19 and 2025-26
  vintages), the US-China chip war, and reshoring dominating several letters
  by word count. Kinea channels tariff/trade-war FX effects almost entirely
  through `global_usd` narrative framing rather than stating a direct link
  (e.g. "Trump tariffs -> dollar strengthens/weakens" gets scored under
  `global_usd`, not `trade_policy`). Not proposing to drop the category — a
  more flow-/trade-oriented publication might use it directly — but across
  the full archive of this one manager's writing, it's simply never how they
  frame the causal chain.
- **`global_usd` dominates overwhelmingly**: 40 of 101 claims (40%), still
  comfortably the largest category even as the archive roughly doubled in
  size this session. `monetary_br` (24) and `fiscal_br` (14) are the two
  next-largest; `commodities` (7, all tied to the renamed "external
  accounts" boundary — see resolution note above), `risk_sentiment` (6),
  `capital_flows` (5), `politics_br` (4), and `china_em` (1) are minor to
  rare. This is a real property of Kinea's own writing style, not
  necessarily representative of how other managers would frame the same
  events — the letters are written from a global-macro vantage point (US
  Fed cycle, US exceptionalism, global risk regime) with Brazil analyzed as
  one input to that global picture, which structurally routes most
  BRL-relevant reasoning through the `global_usd` lens even when the
  underlying driver (e.g. a BR rate cut, a fiscal package) is domestic.
- **A whole dedicated fiscal essay can still score zero.** The Aug 2024
  `kinea_insights` piece ("Frankenstein: o monstro fiscal brasileiro") is
  entirely about Brazil's fiscal structure — yet contributes nothing to
  `fiscal_br`, because it never once states the FX implication explicitly
  (no "isso deprecia o real" sentence anywhere in it). The Oct 2023
  `kinea_insights` piece on Brazil's oil trade balance ("O petróleo é
  nosso!") is the same story for `commodities`/external accounts, and the
  May 2026 piece on the Brazilian consumer ("Parasita") makes the identical
  move with terms-of-trade language instead of oil specifically: pages of
  current-account/terms-of-trade analysis, zero claims each time, because
  the câmbio implication is never spelled out. This is the strictest
  possible illustration of extraction rule #2: topical relevance isn't
  extraction criteria, an explicit stated link to a currency effect is.
- **December is consistently one of the sharpest months** across multiple
  years — 2024 is the extreme case (`fiscal_br` -1.7, `global_usd` -1.2, two
  documents making high-confidence retrospective/outlook claims in the same
  month), but 2023's December year-in-review letter also produced a distinct
  finding: an explicit admission that the BR rate-cut cycle *should* have
  depreciated BRL per the usual carry mechanism, but BRL appreciated instead
  ("teimosamente," stubbornly) — scored 0 under extraction rule #6, since the
  letter names the expected channel and reports it failed to predict
  direction that year, rather than offering a fresh causal story for the
  actual move. 2024's own admitted trading error — "stayed long BRL all
  year, underestimated fiscal deterioration" — remains the single most
  negative `fiscal_br` claim in the entire dataset (-1.0, a manager grading
  their own mistake, not just describing the market).
- `kinea_insights` (the thematic deep-dive) carries only a small fraction of
  the total signal: 10 of 101 claims (10%) despite being just over half of
  all documents (64 of 124) — confirmed consistently across every year in
  the archive, 2021 and 2026 included, not just 2024 as first observed. The
  main "Carta do Gestor" letter carries almost the entire signal every year.
  A second, earlier instance of extraction rule #6 (a channel explicitly
  *failing* to explain the currency, scored 0 rather than omitted) turned up
  in a `kinea_insights` piece from June 2021 on Brazil's agricultural export
  boom — the letter itself flags, as an open puzzle, that BRL "não
  respondia" to a transformational current-account improvement the way
  theory would suggest, predating the analogous December 2023 finding by
  over two years. Worth knowing before deciding whether a future scale-up
  should prioritize reading the main letters over the insights pieces for
  cost/effort reasons.
- **2022's global-macro shock year reads exactly as expected**: nearly every
  `global_usd` claim in 2022 (Jan-Aug, one per month with a claim) is a
  variant of "long USD vs. a basket, defensive, amid Fed tightening /
  recession risk" — the most one-note stretch of the whole dataset,
  consistent with 2022 being the year of the most synchronized, most
  aggressive global tightening cycle in decades. The one real break in that
  pattern is March 2022 (the Russia-Ucrânia-invasion letter), which produced
  a three-way joint-driver split (commodity-exporter position, BR
  hiking-cycle advancement, Brazil's relative insulation from the
  war-driven risk-off) that mirrors the already-documented March 2024 case
  almost exactly, down to the two-year gap between them.
- **2021, the first partial year, already contains the corpus's founding
  thesis.** The December 2021 `kinea_insights` piece "Davi e Golias" ("David
  and Goliath") — cited by name in the October 2022 main letter as the
  origin of Kinea's "small Brazil surprising the global Goliath" framing —
  is itself in this dataset, with an explicit `global_usd` claim (US
  exceptionalism vs. China/Europe softness) and a `monetary_br` claim (BRL's
  vol-adjusted carry becoming one of the largest among EM peers). Having the
  actual source document in `claims.csv`, rather than only its
  later citations, is a small but genuine gain in traceability from filling
  in 2021.
- **2026 (through June) already outweighs entire prior years in claim
  density** — see the "Writing-style shift, 2026" note in the Corpus section
  above. Concretely, `commodities`/external-accounts and `capital_flows`
  each picked up more claims from 6 months of 2026 letters than from any
  single full prior year, driven almost entirely by explicit,
  repeated statements that Brazil's net-oil-exporter position was benefiting
  BRL through the Iran/Strait-of-Hormuz shock, and that surging foreign
  equity inflows (R$63bn through April 2026, more than double all of 2025)
  were explicitly reinforcing the currency.

## Framework: one taxonomy, many managers

**Refactored 2026-07-29** to be manager-agnostic, per direct user request
("create that framework to be applied to the same type of material, with
the same categories, just another manager"). `fx_attribution_model.py`
keeps `CATEGORIES`/`CATEGORY_SLUGS` (the fixed 9-category taxonomy above) and
all the aggregation/rolling-mean/Excel-export logic shared across every
manager — only the source corpus differs. Each manager gets its own
subfolder under `fx_attribution_data/`:

```
fx_attribution_data/
  kinea/
    documents.csv         -- date, month, source, source_file
    claims.csv            -- date, month, source, source_file, category, direction, quote, note
    monthly.csv           -- derived, regenerated each run
    fx_attribution.xlsx   -- derived, regenerated each run
  <new_manager>/
    documents.csv
    claims.csv
    (monthly.csv / fx_attribution.xlsx appear after the first run)
```

### Adding a new manager

1. Create `fx_attribution_data/<manager>/` with `documents.csv` and
   `claims.csv`, same two schemas as Kinea's, hand-extracted following the
   Corpus/Taxonomy/Extraction-rules sections above — the categories, sign
   convention, and six extraction rules all carry over unchanged; only the
   source documents differ.
2. Run:
   ```powershell
   uv run python -c "from analytics.brasil.exchange_rate.models.fx_attribution_model import run; run(manager='<manager>')"
   ```
   This writes `monthly.csv` and `fx_attribution.xlsx` inside that manager's
   own subfolder. No code changes are needed — `manager_dir()` resolves the
   path and raises a clear error (listing the managers that do exist) if the
   folder is missing.
3. `run()` with no argument still defaults to `manager="kinea"`, so every
   command used earlier in this doc keeps working unchanged.

Cross-manager comparison/merging isn't built — each manager's monthly matrix
is independent. Combining two managers' claims into one shared monthly
series, if ever wanted, would be a deliberate next step (e.g. summing two
managers' claims into a single "consensus" monthly view, or keeping them
side by side as separate columns) rather than something this refactor
assumes.

## Verde Asset — second manager, 2010-01 to 2026-05 (2026-07-29, extended 2026-07-30)

**Scope, extended six times across two days.** Initially bounded to 2025-01
through 2026-05 per direct user request ("apply the framework on Verde
Asset Management from 2025 on"); extended backward to 2023-01 ("run for
2023-2024"); extended backward again to 2020-01 ("run from 2020-2022");
extended backward a third time to 2018-01 ("run for 2018-2019"); extended
backward a fourth time to 2014-01 ("run for 2014-2017") — all four same-day
extensions, 2026-07-29. Extended a fifth and sixth time (still same
underlying pattern, new day) to 2010-01, in one round covering both 2010-2011
and 2012-2013 in parallel ("run the fx contributor for the year of
2010-2013," 2026-07-30) — **200 months total, 2010-01 through 2026-08, a
single continuous run** (197 at the time of that round; the 2026H2 refresh
of 2026-09-08 added Jun/Jul/Ago 2026). Still not the full archive:
`repository/mental_model/verde_asset/raw_pdf/` goes back to 1999, but only
2010+ is extracted so far. A further backward extension (to 1999, 11 more
years) would be a distinct next step, not an assumed follow-on.

**Corpus and structure, different from Kinea in one real way:** Verde
publishes a single monthly series ("Relatório de Gestão"), not two parallel
publications the way Kinea has `kinea`/`kinea_insights` — so `documents.csv`
has exactly one row per covered month, 197 rows total, no double-counting
risk to watch for. `clean_md/` (pre-extracted by an earlier curation pass,
not built fresh for this task) already covered the needed window ready to
read directly. **`date` uses each PDF's `/CreationDate` metadata, not an
inferred value** — Verde's letters don't encode a publication day in their
filename or body text the way Kinea's do (`Verde-REL-2025_01.md` only names
the covered month), so the actual PDF creation timestamp (confirmed via
`pypdf`) was used as the real-world publication date — **with one
exception: `Verde-REL-2010_06.pdf` has no `/CreationDate` at all** (empty
field, confirmed by inspecting its full metadata dict, not just the one
field), the only gap found across 197 documents so far; its `date`
(2010-07-09) is inferred from the consistent early-to-mid-following-month
pattern of its immediate neighbors (2010-05 published 2010-06-10, 2010-07
published 2010-08-09), flagged here rather than silently treated as real
metadata. Consistent pattern otherwise across all 197: published
early-to-mid the *following* calendar month (e.g. the January letter
carries a 2025-02-10 creation date) — `month` in both CSVs is the letter's
own covered month (from its title, "Janeiro de 2025"), `date` is that later
publication date, mirroring Kinea's own date-vs-month split exactly. One
more publishing-cadence anomaly, distinct from the inferred-date gap above:
**the July and August 2011 letters share the identical creation date**
(2011-09-26), meaning Verde issued two months' letters together after an
roughly 2.5-month gap rather than one-per-month as usual — a real
publishing irregularity confirmed from the PDF metadata itself, not a data
error. The 2017-01 letter is a 20th-anniversary retrospective quoting
dozens of the fund's own past letters verbatim (1997-2016) — none of those
quoted passages were re-extracted as fresh 2017-01 claims, since they
describe other months' already-past (or, for 1997-2013, out-of-scope)
events, not anything new about January 2017 itself; the letter produced
zero fresh claims of its own for this reason.

**172 claims across 197 documents** (vs. Kinea's ~101 across 124) — a
claims-per-document rate of ~0.87 overall. The per-window rate is
definitively **not monotonic**, now confirmed a third time by this round:
2010-2013 (37 claims/48 documents ≈ 0.77) slots in between the existing
extremes rather than extending either the climb or the dip. The full
six-window sequence, oldest to newest, is **0.77 → 1.10 → 0.63 → 0.67 →
0.83 → 1.35** (2010-2013 → 2014-2017 → 2018-2019 → 2020-2022 → 2023-2024 →
2025-2026) — a real up-down-up-down-up zigzag, not a trend, and not even a
single clean "dip in the middle" shape once a sixth point is added. The
honest read, restated once more: Verde's claim density tracks how
FX-explicit a given stretch of letters happens to be written, not how far
back in time it sits — treat any claim about this corpus's density trend as
provisional by default, exactly as flagged after the previous two rounds.

**Findings:**
- **`fiscal_br` never fires once in this window** — despite Verde
  discussing Brazilian fiscal fragility repeatedly and explicitly (IOF
  hike/reversal, income-tax-exemption expansion, "acelerador fiscal com
  freio monetário," populist spending ahead of the 2026 election), not one
  passage explicitly states a resulting câmbio/Real effect the way
  extraction rule 2 requires — every one of those passages ties the fiscal
  discussion to equities/risk-premium language instead. Structurally the
  same pattern the Kinea corpus already showed with its Aug-2024 Frankenstein
  essay (a whole piece can be *about* fiscal risk and still score zero) —
  now confirmed as a repeating pattern within a single short window, not a
  one-off.
- **`trade_policy` fires for the first time across the whole framework.**
  Kinea's full 5+-year archive never produced a single `trade_policy`
  claim (Trump tariffs always got channeled through `global_usd` framing
  instead) — Verde's July 2025 letter breaks that pattern directly, tying
  Trump's 50% tariff announcement *on Brazil specifically* to explicit BRL
  weakening ("vimos... enfraquecimento do Real"), filed alongside a
  separate `politics_br` claim the same month for the concurrent Magnitsky-
  Act sanctions on STF Justice Alexandre de Moraes (a joint-driver split,
  same pattern as Kinea's March 2022/March 2024 precedents).
  Cross-manager read: this isn't evidence Kinea's manager-agnostic taxonomy
  was wrong, just that *which* channel absorbs a tariff shock's FX
  narrative is manager-specific writing style, not a taxonomy gap.
- **January 2026 is a clean three-way joint-driver month** — BRL's
  +4.25% rally explicitly attributed to `global_usd` (dollar flight),
  `commodities` (gold/silver/Brent surge on Iran risk), and `capital_flows`
  (a concretely quantified one-month equity inflow "similar a todo o fluxo
  do ano de 2025") all at once, split into three rows per the same
  joint-driver convention Kinea's March 2022/2024 months established.
- **April 2026 is a genuine extraction-rule-6 case**: the letter explicitly
  flags early signs of capital *outflow* and reduced relative attractiveness
  for Brazil, yet BRL still appreciated +4.3% that month — scored 0 for
  `capital_flows`, a channel explicitly failing to explain the move that
  month, not silence.
- **`capital_flows` is Verde's most active category in this window** (5 of
  23 claims) — a sharp contrast with Kinea, where it's rare (5 of 101 across
  5+ years). Verde's letters lean much more heavily on explicit,
  often-quantified flow narratives (foreign equity inflows/outflows,
  dividend-repatriation timing) than Kinea's more macro-narrative style —
  a real difference in house writing style worth keeping in mind before
  any cross-manager comparison is attempted.
**2023-2024 extension findings (20 new claims across 24 documents):**
- **`fiscal_br` fires for the first time once the window is widened** —
  zero times in 2025-2026, but 6 separate months across 2023-2024 (Mar/Apr
  2023 positive; Apr/May/Jun/Nov/Dec 2024 negative), directly contradicting
  the "never fires" read the 2025-2026-only window suggested above. That
  finding was an artifact of the narrower sample, not a real property of
  Verde's writing — a concrete illustration of why partial-window
  extractions need labeling as such rather than treated as settled.
- **June 2024 is the sharpest single-month BRL move in the whole Verde
  dataset so far** (-6.6%, explicitly named), a joint `fiscal_br`
  (-0.7)/`politics_br` (-0.6) driver — concrete fiscal-slippage numbers
  (spending +12.9% real vs. a 2.5% real rule; a R$295bn deficit vs. a
  R$28.8bn target) compounding with the president's own inflammatory public
  remarks, mirroring the joint-driver pattern seen elsewhere in both Verde
  and Kinea's corpora.
- **`china_em` fires for the only time in the whole Verde corpus in
  September 2024** — China's late-month stimulus package (equity-support
  facility, rate cuts, property easing) explicitly credited with an
  accompanying `commodities` claim as jointly lifting BRL, tempered by the
  letter's own caveat that the benefit is likely marginal against Brazil's
  idiosyncratic fiscal problems.
- **`monetary_br` only fires twice, both from an explicit BCB-credibility
  narrative, not a plain carry-differential one**: April 2024 (BCB
  abandoning forward guidance, credibility loss, -0.6, joint with
  `fiscal_br`) and July 2024 (BCB adopting a tougher, credibility-focused
  tone, +0.4). Both center the *signal* of BCB credibility rather than the
  *level* of the rate differential — a subtly different reading of
  "monetary policy" than the more carry-mechanical claims seen in the
  2025-2026 window (e.g. 2025-06, 2025-09).
- **December 2024 replays December 2023's own dynamic almost exactly**:
  a large-scale BCB FX intervention explicitly credited with cushioning
  (not fully offsetting) seasonal December outflows compounded by fiscal-
  credibility damage — split into a `fiscal_br` claim (the populist
  November package) and a separate, deliberately moderate `capital_flows`
  claim (-0.4, not more extreme, precisely because the intervention is
  explicitly said to have dampened the impact).
- **`risk_sentiment` and `trade_policy` never fire once across the full
  2023-2026 window** — `risk_sentiment` fired only once in the whole
  corpus (2025-03), and `trade_policy` only in 2025-07 (see above); neither
  shows up at all in 2023-2024, consistent with those being genuinely
  situational (a specific tariff shock, a specific March-2025 risk-off
  episode) rather than recurring channels in Verde's own writing.

**2020-2022 extension findings (24 new claims across 36 documents):** this
window covers the COVID shock, the "Teto de Gastos" (spending-cap) unwind,
and the Russia-Ukraine invasion — three of the sharpest macro episodes in
the whole corpus, and it shows in the claim intensity despite the lowest
per-document rate of any window (many months, especially March-August 2020,
are pure risk-asset/positioning commentary or a COVID-medicine deep-dive
with zero FX-explicit content at all).
- **`fiscal_br` is the dominant category by far in this window** (9 of 24
  claims, all but one negative) — the "Teto de Gastos" unwind is Verde's
  single most recurring FX narrative across 2020-2022, echoed in three
  separate essay-length treatments: a September 2020 fiscal deep-dive
  explicitly naming câmbio as one of the prices that react to any sign of
  abandoning the cap; an October 2021 essay (co-authored by founder Luis
  Stuhlberger, also published externally in Brazil Journal) quantifying
  BRL's -38% move since Jan-2020 against a -5.7% MXN/ZAR/INR peer average
  over the same window, explicitly ruling out a common-EM-shock story; and
  a January 2022 essay on a proposed fuel-tax cut.
- **A rare, explicit, quantified counterfactual — November 2022**: "caso o
  governo eleito exibisse um mínimo de disciplina fiscal, provavelmente
  estaríamos vendo taxa de câmbio na casa de R$4,90" — the letter names a
  specific BRL level it believes would prevail absent the transition
  government's fiscal indiscipline (the "PEC da Gastança"), stated
  alongside two genuinely favorable tailwinds that same month (a -5.0% DXY
  move, iron ore +30%) that the fiscal slippage was explicitly said to be
  offsetting. The clearest "fiscal cost, precisely priced" claim in the
  whole Verde corpus so far.
- **Two more extraction-rule-6 cases, both explicit "channel underperformed"
  admissions**: January 2022 ("O termômetro quebrou" — BRL actually
  appreciated despite a dedicated fiscal-populism essay that month, cushioned
  by returning carry and foreign equity flows, both filed as their own
  positive joint-driver claims) and December 2021 (BRL's 2021 depreciation
  explicitly called "tímida" relative to the size of that year's
  fiscal-driven risk-premium surge). Distinct from a true rule-6 zero (a
  channel with literally no net move) — both still score negative/zero
  rather than a strong negative, reflecting the letter's own "less than the
  shock implied" framing.
- **`politics_br` clusters entirely in the COVID-vaccine-rollout period**
  (2020-04 through 2021-08, 5 of 6 total `politics_br` claims in the whole
  corpus) — every instance ties political/institutional failure (vaccine
  procurement delay, institutional-crisis rhetoric) to BRL weakness during
  Brazil's specific COVID second-wave mismanagement; none of it recurs once
  vaccination completes in late 2021, a clean example of a channel that is
  genuinely episodic rather than a standing feature of Verde's writing.
- **`commodities` fires exactly twice, both tied to the same
  Russia-Ukraine shock** (March 2022, direct; November 2022, alongside the
  DXY/fiscal counterfactual) — a real, if narrow, cross-manager echo of
  Kinea's own March 2022 finding for the identical global event (see the
  Kinea section of this document).
- **`monetary_br`/`capital_flows` both fire for the first time in this
  window, in the SAME January 2022 month**, as the two positive channels
  explicitly offsetting that month's fiscal-populism risk (see the rule-6
  case above) — carry (returning post-hike Selic advantage) and foreign
  equity flows, filed as separate joint-driver claims per the same
  convention used for the multi-channel months elsewhere in this document.
- **March-August 2020 (6 consecutive months) is the single longest
  zero-claim stretch in the whole Verde corpus** — not for lack of dramatic
  content (this is the depth of the COVID crash and the fastest-ever
  market recovery) but because the letters' FX-relevant passages during
  this stretch either fail extraction rule 2 (general "ativos brasileiros"
  language, no câmbio singled out) or are entirely pandemic-response essays
  with no FX content at all (March 2020's letter is almost pure COVID
  epidemiology/vaccine-pipeline analysis). A genuine illustration that
  claim density tracks a manager's own writing habits in a given stretch,
  not the objective magnitude of the underlying market move.

**2018-2019 extension findings (15 new claims across 24 documents):** this
window opens the corpus with a dedicated "Nossa visão atual sobre os
mercados brasileiros" section (January 2018) that starts every year's
outlook with câmbio specifically — a structural habit of Verde's letters
this early on that the later years drop.
- **`fiscal_br`'s "never fires in 2025-2026" read turned out to be an
  artifact of window size, confirmed a second time.** The first backward
  extension (2020-2022) already overturned an earlier "fiscal_br never
  fires" claim from the 2025-2026-only window; this round's `fiscal_br`
  claims (November 2019's disappointing "cessão onerosa" auction) extend
  the category's presence back to the very start of the corpus. Combined
  with the claim-density reversal noted above, this window is a second,
  independent confirmation that conclusions from any single extraction
  round here should be held loosely until the window stops growing.
- **`monetary_br` is this window's dominant category** (5 of 15 claims,
  all but one negative) — a real contrast with 2020-2022 (where
  `monetary_br` never fired at all) and 2023-2024 (2 of 20). The clearest
  case: April 2018's carry-erosion essay, which precisely quantifies BRL's
  move from 3.25 to 3.55 in one month and attributes it explicitly to the
  BCB cutting rates by more than expected plus surprise dovish forward
  guidance — "o grão de areia que desestabilizou o castelo." May 2018
  continues the same story into the truckers'-strike crisis, explicitly
  invoking the Argentina/Turkey devaluation-spiral mechanism (carry
  collapse → forced hikes) while the same letter distinguishes Brazil's
  current-account position from those two peers (filed as a separate,
  mitigating `commodities` claim).
- **A uniquely rich, mostly-rule-6 month — November 2019.** The letter
  opens by naming "o valor da moeda" as that month's central theme, lists
  three explicit fear-drivers behind a real BRL selloff (a disappointing
  state oil-rights auction, deteriorating trade-balance/current-account
  data, and Chile/Colombia social-unrest contagion), then **retracts two of
  the three within the same document**: the trade data turned out to be
  erroneous and the current-account revision merely an accounting
  artifact with no real flow impact (scored 0 for `commodities`), and the
  regional-contagion read is explicitly judged unlikely to extend to
  Brazil (scored 0 for `risk_sentiment`) — only the auction result is kept
  as a real, if anticipated, `fiscal_br` negative. The single cleanest,
  most self-aware illustration of extraction rule 6 in the whole corpus:
  a manager naming a real price move, offering multiple candidate causes,
  then explicitly falsifying most of its own list in the same breath.
- **August 2018 and August 2019 are a genuine cross-year echo**: both are
  EM-contagion months triggered by a *different* country's crisis (Turkey
  in 2018, the Argentine primary-election shock in 2019) compounding with
  domestic noise (Bolsonaro-era election jitters in 2018; presidential
  environmental-policy remarks in 2019) — the same "regional crisis plus
  local noise" shape recurring a year apart, though scored under different
  categories each time (`risk_sentiment` in 2018 vs. a `politics_br`/
  `monetary_br`/`global_usd` joint-driver split in 2019) since the
  specific named mechanism differed.
- **October 2018 (Bolsonaro's election) is the cleanest, highest-confidence
  `politics_br` claim in the whole Verde corpus**: "A bolsa subiu, os
  juros caíram e o câmbio se valorizou" — all three asset classes named
  explicitly in one sentence, directly following the election result, with
  no hedging language at all.
- **February 2019's Fed-framework essay is a rare explicit sign-uncertainty
  admission**: the letter argues a structurally lower US real rate (from
  an anticipated Average Inflation Targeting shift) should weaken the
  Dollar and benefit EM assets like Brazil, but immediately qualifies "a
  pergunta crucial seja 'desvalorizar contra quem?'" — an unusually
  self-aware flag that the *which-currencies-benefit* question is genuinely
  open, scored at a moderate +0.4 rather than the stronger score a less
  hedged claim would get.

**2014-2017 extension findings (53 new claims across 48 documents):** this
window opens the corpus with the tail of the first Dilma-reelection cycle,
covers the 2015-2016 "Big Short"-era collapse (fiscal capitulation, the
impeachment cycle, Joaquim Levy's appointment and exit), and closes with
Temer's reform agenda stalling out through the Joesley Day shock and the
2018-election run-up — the single densest and most dramatic stretch of
Brazilian macro history in the whole Verde corpus so far, and it shows:
this is now the highest-density extraction window (see above).
- **`global_usd` is this window's dominant category by a wide margin** (14
  of 53 claims) — reflecting a run of genuinely global shocks landing on
  BRL in short order: the 2014 "dollar bull market" (accumulating US
  strength plus anticipated Fed liftoff), the 2015 China RMB devaluation
  shock, the 2016 Brexit-driven dollar reversal and subsequent Trump-election
  re-strengthening, and Trump's 2016 border-adjustment-tax proposal (the
  corpus's second `trade_policy` claim ever, after 2025-07's tariff
  finding — both scored, six years apart, from the same manager).
  December 2016 is a particularly rich month: broad dollar strength from
  the Fed's second hike is named explicitly *alongside* Brazil's own
  "curious" decoupling from that same trend (BRL hitting a multi-year
  overvaluation extreme instead, credited to strong capital inflows) —
  two deliberately separate `global_usd` claims in one document, the
  general fact and Brazil's specific exception to it, mirroring Kinea's
  own April-2025 "opposing claims stay separate" precedent.
- **`fiscal_br` is dense and almost entirely negative in 2014-2016**
  (10 of 22 non-zero `fiscal_br` months in the whole corpus fall in this
  four-year window alone), anchored by a long, explicit February-2014
  essay ("Razões para acreditarmos na depreciação do Real") building the
  entire Real-depreciation thesis directly on twin-deficit/fiscal-trajectory
  analysis — the single clearest "fiscal essay explicitly tied to câmbio"
  case in the whole corpus, a sharp contrast with Kinea's own Aug-2024
  Frankenstein essay (fiscal essay, zero câmbio claims) and even with
  several of Verde's own later, more equity/growth-framed fiscal passages.
  November 2015's "Câmbio a 3,70... os ativos com preços mais errados,
  dado o quadro fiscal" is the closest analogue in this window to the
  2020-2022 window's "R$4,90 counterfactual" finding — an explicit
  fiscal-driven mispricing claim, though without a similarly precise
  counterfactual level named.
- **A genuine two-driver joint-driver month, April 2015**, four-way rather
  than the more typical two- or three-way split seen elsewhere in the
  corpus: foreign capital inflows, an oil/iron-ore price recovery, a
  forming China equity bubble, and dovish-Fed hopes from weak US data are
  all named in one paragraph explaining the same month's surprising BRL
  appreciation — the richest single joint-driver month in the whole
  2014-2026 corpus by count of distinct categories (four), edging out
  January 2026's three-way split.
- **`monetary_br`'s carry-currently-supports-the-Real reading recurs
  explicitly twice, eleven months apart** (January 2015, July 2015) — both
  times the letter's own valuation framework states that Brazil's real
  carry, not fundamentals, is what's currently keeping the exchange rate
  from reflecting the manager's bearish thesis; July 2015 pairs this with
  an explicit, unusually blunt criticism of BCB's own swap-buyback
  intervention as counterproductive ("apagar fogo com gasolina" — like
  putting out fire with gasoline), reducing dollar supply and raising
  corporate hedging demand exactly when the opposite was intended.
- **Five separate rule-6 admissions in this window alone** — more than any
  other single extraction round — spanning both directions: January 2016
  and February 2017 both have the manager's own dollar-bullish thesis
  explicitly failing to show up in that year's prices; October 2016 and
  November 2017 both have capital/repatriation flows explicitly described
  as balanced or FX-irrelevant despite raising real money; and October
  2014's twin-deficit deterioration (restated in November 2014's own
  document) is explicitly said not to have "shocked" the currency at all,
  contrary to what the underlying fundamentals would imply. Read together
  with the 2018-2019 window's November-2019 case, rule 6 fires
  disproportionately often for this one manager compared to Kinea's
  archive — a real difference in how explicitly Verde's letters flag their
  own predictive misses, not an artifact of extraction inconsistency.
- **Politically-driven claims cluster around two distinct episodes**:
  2014's binary Dilma-vs-Aécio/Marina election (April 2014's falling-
  approval-ratings-read-as-pro-market finding) and 2016's impeachment
  acceleration (March 2016's improbable-to-viable-in-two-weeks finding,
  which explicitly names câmbio among what fiscal/political failure would
  otherwise "contaminate") — no `politics_br` claims fire at all in the
  quieter 2017 stretch between Temer's confirmation and the Joesley Day
  shock, despite 2017 containing plenty of political content overall; the
  category tracks acute political *inflection points*, not political
  content generally, consistent with how it behaves in every other window
  of this corpus.
- **May 2017's Joesley Day shock ("o cisne negro de 17 de maio") produced
  zero claims**, despite being one of the sharpest single-day BRL moves in
  Brazil's modern history (an ~8% intraday move) and despite the letter
  itself calling political-risk consequences for Brazilian asset prices
  "bastante claras" — the surrounding text names "ações brasileiras" and
  "juro real" as directly affected, and "preços de ativos brasileiros"
  generically, but never spells out an explicit câmbio/real/dólar
  connection for this specific shock, so it was excluded under extraction
  rule 2 exactly as the Frankenstein and Parasita essays were in the
  Kinea corpus — arguably the single strictest-reading exclusion made in
  this whole extraction effort, given how clearly FX-relevant the actual
  event was.

**2010-2013 extension findings (37 new claims across 48 documents,
extracted via two parallel subagents — 2010-2011 and 2012-2013 — the first
round of this pipeline to delegate the read-and-extract step rather than
have Claude read every letter directly in-session):** this window opens the
corpus at the tail of the 2008-09 crisis recovery, covers the peak of the
commodity supercycle, the original "currency war" episode, and closes with
the May-2013 taper-tantrum shock that hands off directly into 2014's fiscal
narrative.
- **`commodities` and `monetary_br` co-dominate this window (10 and 9 of 37
  claims respectively), with `global_usd` a distant third (5)** — a real
  reversal of the pattern seen in every other window of this corpus, where
  `global_usd` is consistently the largest or near-largest category. Reads
  as a genuine property of the period rather than an extraction artifact:
  2010-2013 was the peak of Brazil's commodity-supercycle/high-carry era,
  before the May-2013 taper tantrum flipped the dominant narrative to a
  global-dollar one that then carries through the whole 2014-2017 window.
- **The corpus captures the actual coining of "currency war."** September
  and October 2010's letters both invoke "Guerra Cambial"/"Global Currency
  War" by name, explicitly framing G7 quantitative easing as forcing EM
  (including BRL) appreciation at the cost of Brazilian industrial
  competitiveness — a real historical anchor, since Brazilian finance
  minister Guido Mantega coined the term in almost exactly this same
  window (Sept 2010).
- **`fiscal_br` is pushed back a full year earlier than any previous
  round found**, firing for the first time in this window's own February
  2013 letter (fixed-income investors' confidence in strong debt/GDP and
  primary-surplus metrics credited with an "esdruxulamente apreciado"
  Real) — a full year before the previously-earliest fiscal claim in the
  whole corpus (February 2014's dedicated depreciation essay). A fourth
  consecutive round in which a "this category starts here" read from a
  partial window gets pushed back further by the next extension.
- **A genuinely two-sided joint-driver month, April 2010**: the letter
  states an explicit five-part bear case for the Real (European-crisis
  risk aversion, stagnant commodity prices, a widening current-account
  deficit, eroding industrial competitiveness, a monetary-policy paradigm
  shift aimed at capping appreciation) and, in the same document, an
  explicit bull case (safe-haven flows into BRL/gold away from the
  traditional reserve currencies, plus resilient iron-ore-driven terms of
  trade) — four distinct categories touched, two of them (`risk_sentiment`,
  `commodities`) appearing twice each in *opposite* directions within one
  letter, the most internally two-sided single month in the corpus so far.
- **`politics_br` appears only twice, both in 2012, both about
  interventionist economic policy rather than elections or scandal** (April
  and June 2012's "Bull Market in Politics" thesis — deliberate government
  moves to cut rates, weaken the currency, and steer industrial policy) — a
  distinct flavor of `politics_br` claim from the election/impeachment/
  judicial-shock claims that dominate the category in every later window.
- **`capital_flows` fires four times, every instance explicit BCB
  intervention (swap-buyback or dollar-selling programs), never foreign
  portfolio positioning** — a different flavor from the 2025-2026 window's
  quantified foreign-equity-inflow claims, another instance of the same
  category meaning different things in different eras of Verde's own
  writing.
- **`trade_policy` and `china_em` stay almost entirely dark in this
  window**: zero `trade_policy` claims (consistent with every window before
  2016's border-adjustment-tax claim), and exactly one `china_em` claim
  (October 2010, Chinese growth credited with continuously improving
  Brazil's terms of trade) — the earliest instance yet of a category that
  otherwise fires only once more in the whole corpus (September 2024).
- **A clean rule-6 case, July 2011**: amid the US sovereign-downgrade/
  European-crisis risk-off shock that hit Brazilian equities hard, the
  letter explicitly notes câmbio, long-end rates, and CDS all held up
  "incrivelmente bem" — a deliberate near-zero, channel-didn't-move-as-
  theory-would-predict claim, the same pattern established in earlier
  rounds' rule-6 admissions.

Rerun via:
```powershell
uv run python -c "from analytics.brasil.exchange_rate.models.fx_attribution_model import run; run(manager='verde_asset')"
```

## Kapitalo K10 — third manager, year-by-year (2026-07-31, started)

**Scope, explicit user choice**: process year-by-year, stopping between each year for a go-ahead — the same pacing convention used for that corpus's `clean_md` curation (see `repository/mental_model/kapitalo/CURATION_SCOPE.md`). Source: `repository/mental_model/kapitalo/clean_md/`, one letter/month (like Verde, not two parallel series like Kinea) — `documents.csv` has exactly one row per covered month.

**No `/CreationDate` metadata in Kapitalo's PDFs** (confirmed via `pypdf`, unlike Verde's, where that field was the actual publication date) — there is no way to recover each letter's real-world publication date. Per direct user choice: `date` = the covered month's own last calendar day (e.g. `2019-07-31` for the July 2019 letter), a neutral placeholder distinct from `month` only by day precision, not a real publication date. Flagged here so this isn't later mistaken for a recovered date the way Verde's genuinely is.

**2019 (Jul–Dec, 6 letters) — done, ZERO claims.** A real, notable finding, not an extraction gap: these first six letters (the fund's inaugural stretch) are almost entirely global-macro scene-setting and asset-class position lists (Posições: Moedas/Commodities/Bolsa/Juros), with real-BRL mentions appearing only as bare positioning statements ("zeramos... a posição comprada de real contra dólar") or as a premise inside an unrelated argument ("apesar da desvalorização do real, o processo inflacionário continua benigno" — used to argue about BCB's reaction function, not to explain what caused the depreciation) — neither satisfies extraction rule 2 (an explicit stated cause-to-câmbio link, not just a mention). Jul/2019's own long NOK "Estudo de Caso" is a rich, explicit FX-causal essay, but about NOK/EUR, not BRL/USD, so it's out of scope for this corpus's BRL-only taxonomy regardless of how well-argued it is. Worth watching whether this changes in later years, the same way Kinea's writing became sharply more FX-explicit in 2026 (see the "Writing-style shift, 2026" note above) — Kapitalo's later letters (already read during `clean_md` curation) appeared noticeably more FX-explicit by 2022+, so a real shift is plausible here too, not yet confirmed by this extraction.

**2020 (12 letters) — done, exactly ONE claim for the whole year** (a joint-driver split): Maio/2020's "O mês de maio foi marcado pela melhora dos mercados globais e pela forte recuperação de preços das commodities. Os ativos brasileiros também tiveram bom desempenho, tendo o real apreciado de forma relevante contra o dólar" explicitly ties that month's BRL appreciation to both the global risk-on rally (`risk_sentiment`, +0.6) and the commodity price recovery (`commodities`, +0.5) in the same sentence sequence — filed as two separate rows per the established joint-driver convention. Every other 2020 month, including the COVID crash itself (Mar/2020) and Abr/2020's full gold/EM-currency-vulnerability essay, failed extraction rule 2: the crash coverage stays in pure epidemiology/market-mechanics terms with no explicit câmbio/real link, and Abr/2020's "moedas de países emergentes...serão mais vulneráveis" names EM currencies generically, never BRL specifically, so it was excluded on the same generic-not-BRL-specific basis Verde's own corpus has already established (see the "regional/bilateral FX move" boundary in extraction rule 4, applied here by analogy to "generic EM" vs. "BRL specifically"). This mirrors the 2020-2022 finding already documented in Verde's own corpus above ("March-August 2020...single longest zero-claim stretch") — a second manager's writing shows the same pattern for the same real-world stretch, reinforcing that this is a property of how COVID-era letters get written industry-wide, not an extraction artifact specific to one manager.

**2021 (12 letters) — done, exactly ONE claim for the whole year**: Ago/2021's explicit contrast — "Esta conjuntura de baixo juros internacionais e elevados preços de commodities é bastante favorável às economias emergentes. Contudo, não estamos otimistas com os ativos brasileiros, pois os desafios internos – deterioração fiscal e governança – não estão sendo endereçados," directly followed in the same letter by "[o]s livros de câmbio e commodities tiveram resultado negativo no mês" — filed as `fiscal_br` (−0.6), since domestic fiscal deterioration and governance failure is the letter's own explicit reason Brazil is the exception to an otherwise EM-favorable global backdrop, immediately preceding that month's stated negative câmbio result. Every other 2021 month (including Out/2021's and Nov/2021's own câmbio-book P&L mentions) only reports the outcome ("os livros de câmbio tiveram resultado positivo/negativo") without ever stating *why* câmbio moved that month — fails extraction rule 2 the same way Verde's and Kinea's own corpora have repeatedly shown a topic can be discussed at length (or a result merely reported) without ever crossing into an explicit causal claim. Consistent with the "sparse/positioning-heavy, narrative-light" character already seen in 2019-2020 — Kapitalo's letters through 2021 stay far more report-style than Kinea's or Verde's own writing in the same window.

**2022 (12 letters) — done, ZERO claims for BRL specifically**, despite two real, explicit FX-causal claims found this year — both excluded on the same generic-not-BRL-specific boundary already established by the Abr/2020 exclusion: Maio/2022's "A moeda parou de depreciar contra a cesta" is an explicit, well-argued CNY claim (tied to China reopening/new stimulus), not BRL — out of scope for this taxonomy regardless of quality. Nov/2022's "As bolsas da China, as commodities metálicas e as moedas de países emergentes foram os maiores beneficiários deste movimento" names "moedas de países emergentes" generically, never BRL specifically, and that same month's own book result (Moedas −1.19%) doesn't obviously support reading it as a BRL-specific claim either way. Dez/2022's "risco de termos uma crise de confiança com piora aguda dos ativos locais" is both generic ("ativos locais," not câmbio) and explicitly conditional/hypothetical ("se formos nessa direção"), not a stated realized cause — excluded on both grounds. 2022 also covers the full Rússia-Ucrânia invasion (Fev-Mar/2022) with no explicit BRL-causal claim anywhere in that stretch, a contrast worth noting against both Kinea's and Verde's own corpora, where that same event produced a clean joint-driver BRL claim (see the "2022's global-macro shock year" and "commodities fires exactly twice" findings in each manager's section above) — Kapitalo's own letters discuss the war's global/commodity implications extensively but never cross into an explicit câmbio-effect statement for it.

**2023 (12 letters) — done, SIX claims across four months**, a real step up from 2019-2022's combined total of 2 — the first year with genuinely rich, explicit BRL narrative, concentrated in the back half:
- **Maio/2023, a clean three-way joint-driver month**: "a aprovação do arcabouço fiscal" (`fiscal_br`, +0.6), "a derrubada de trechos do decreto do saneamento, mensagens moderadoras vindas do Congresso" (`politics_br`, +0.4), and "a inflexão no cenário prospectivo de inflação" plus the anticipated start of a BCB cutting cycle (`monetary_br`, +0.5) are all named together as the explicit triggers for a new long-BRL trade ("compramos o real contra o dólar"). Jun/2023's letter restates the identical thesis as a semester retrospective — treated as corroboration of the same claim, not filed as a second independent one, to avoid double-counting a single restated narrative across two consecutive letters (per extraction rule 3's spirit, applied here across adjacent months rather than within one document).
- **Out/2023**: BCB's "comunicação mais cautelosa" explicitly credited for "ganhos no sentido de ancoragem das expectativas e do câmbio" — filed as `monetary_br` (+0.5), a credibility/signal-based claim rather than a plain carry-differential one, the same "signal not level" distinction Verde's own corpus draws for its April/July 2024 BCB-credibility findings (see the Verde section above).
- **Nov/2023**: a record-high 2023 trade balance ("próxima a USD 90 bilhões... o maior valor da série histórica") and rising grain/oil export volumes explicitly credited with "ajudando a ancorar o câmbio" — filed as `commodities` (+0.6, external-accounts framing, matching this taxonomy's established category boundary).
- **Dez/2023**: Brazil's improving external accounts, named specifically alongside Mexico's (not generic EM, clearing the specificity bar the Abr/2020 and Nov/2022 exclusions failed), explicitly credited as driving expected good returns for "essas moedas cíclicas e de países emergentes" — filed as `commodities` (+0.5).

Notably, this richer narrative arrives right at the Set/2023 era-2 "CARTA DO GESTOR" template transition — consistent with the corpus's own `CURATION_SCOPE.md` note that the newer template's letters read as more analytically dense, though the causal mechanism (template change vs. genuine 2023 macro narrative shift, i.e. arcabouço fiscal approval + BCB's first cutting cycle) can't be disentangled from four data points alone.

**2024 (12 letters) — done, FIVE claims across three months**, continuing 2023's sharper trend, with the year's two richest months lining up closely with findings already documented in Verde's own corpus for the same real-world events:
- **Junho/2024, a three-way joint-driver month, mirroring Verde's own "sharpest single-month BRL move" finding for the same month**: a dedicated "BRASIL: AFROUXAMENTO DAS ÂNCORAS E CRISE DE CONFIANÇA" section explicitly names three drivers behind that month's risk-premium spike on Brazilian assets — fiscal-framework credibility deterioration (`fiscal_br`, −0.7, the primary-deficit target change and weak execution), perceived future BCB leniency under an incoming board (`monetary_br`, −0.6, a credibility/signal-based claim, same pattern as Out/2023's positive BCB-communication claim below), and worsening external accounts from import growth outpacing exports (`commodities`, −0.4, external-accounts framing).
- **Novembro/2024, the cleanest single claim in the whole corpus to date**: "Na falta de um âncora fiscal, o real vem depreciando bem mais do que os pares" — directly names the absence of a credible fiscal anchor (the disappointing spending-cut package) as the reason BRL is depreciating more than its peers. Filed as `fiscal_br` (−0.8).
- **Dezembro/2024, mirroring Verde's own December-2024 finding**: "houve uma saída recorde de recursos do país em dezembro, levando o Banco Central a vender USD 21,7 bilhões de reservas cambiais" — a record capital outflow requiring large-scale BCB FX reserve sales, filed as `capital_flows` (−0.5).

No claims in Jan-May, Jul-Oct/2024 — all either pure global-macro commentary or câmbio book-P&L-outcome-only, consistent with the corpus-wide pattern. Fev/2024 had an explicit currency-devaluation claim, but for EUR/GBP/SEK against USD (growth-divergence framing), not BRL — excluded on the same generic-not-BRL-specific boundary as prior exclusions.

**2025 (12 letters) — done, ONE claim**, a step back down from 2023-2024's density: Fevereiro/2025's "os ativos norte-americanos sofreram: as taxas de juros cederam de forma relevante, o dólar enfraqueceu e as bolsas caíram," explicitly tying broad US-dollar weakness to that month's rising uncertainty/falling US-growth confidence — filed as `global_usd` (+0.4, sign flipped per this taxonomy's convention that dollar weakness is BRL-supportive). Two real, explicit currency-effect claims were found and excluded on careful re-reading: Dezembro/2025's "desinflação importante, impulsionada pela forte valorização do real" states câmbio as the CAUSE of disinflation, the reverse of what this model measures (extraction rule 1 explicitly excludes FX-as-cause-of-something-else) — and no cause is stated for the real's own appreciation, so nothing survives from that sentence. Dezembro/2025 also has a forward-looking câmbio-risk-premium repricing discussion tied to the 2026 election, excluded as conditional/hypothetical rather than a stated realized cause, the same standard applied to Dez/2022's and Dez/2025's own political-risk exclusions elsewhere in this corpus. The year is otherwise dominated by non-BRL deep-dives (Colômbia in June, Argentina in August/September/October) and US-macro/tariff commentary with no explicit câmbio-BRL link.

**2026 (Jan-May, 5 letters) — done, ZERO claims.** Jan/2026 has a real, explicit claim about a "reacendimento do ímpeto por diversificação dos portfólios globais" (US geopolitics/tariffs/populist-midterm agenda driving diversification away from US assets) explicitly benefiting EM assets — but it names "ativos de países emergentes, principalmente as bolsas" (EM assets, MAINLY equities), generic and equity-focused rather than BRL/câmbio-specific — excluded on the same generic-EM boundary used throughout this corpus. Maio/2026 has a real, explicit dollar-strength claim (US growth differential + hawkish Fed) but explicitly scopes it to "principamente contra as moedas dos países desenvolvidos" (mainly against DEVELOPED-market currencies) — the opposite scope from what would support a BRL claim, so excluded rather than force-fit. Feb-Apr/2026 is dominated by the Iran/Strait-of-Hormuz war and its oil-market consequences, with no explicit câmbio-BRL link anywhere in that stretch. Maio/2026's Colômbia deep-dive (a direct continuation of the June-2025 thesis) draws an explicit historical analogy to Brazil's 2016 post-impeachment shift, but as illustrative comparison, not a BRL-causal claim about the current period.

## Corpus-wide summary — Kapitalo K10, full archive (2026-08-01)

**83 letters, Jul/2019 through Mai/2026, 15 claims total.** Category breakdown: `commodities` (4), `fiscal_br` (4), `monetary_br` (3), `risk_sentiment` (1), `politics_br` (1), `capital_flows` (1), `global_usd` (1) — `china_em` and `trade_policy` never fire once across the whole archive, despite extensive China/tariff commentary throughout (the same "channel absorbs the narrative differently per manager" pattern already documented for Kinea's own zero `trade_policy` finding).

**Claim density is sharply non-monotonic by year, not a trend**: 2019 (0), 2020 (1), 2021 (1), 2022 (0), 2023 (6), 2024 (5), 2025 (1), 2026 partial (0) — a clear hump centered on 2023-2024 (11 of 15 claims, 73% of the whole archive, from just 24 of 83 letters). This is the single most FX-explicit stretch in Kapitalo's writing found anywhere in the corpus, coinciding with Brazil's arcabouço fiscal approval, the BCB's 2023 cutting cycle, and 2024's fiscal-credibility deterioration — but as with every other density observation in this file (Kinea's 2026 writing-style shift, Verde's six-round zigzag), this reads as a property of what was actually happening in Brazil during those two years and how Kapitalo chose to write about it, not a stable per-manager rate to extrapolate forward.

**Structurally, Kapitalo differs from both Kinea and Verde in one clear way**: it is overwhelmingly a global-macro/commodities letter with Brazil as one regional input among many (Argentina, Colômbia, China, and country-specific commodity deep-dives routinely outweigh Brazil-specific content by letter count) — consistent with `capital_flows` and `politics_br` firing only once each in 83 letters, far more sparsely than either Kinea's or Verde's own corpora, and with several genuine EM-currency or non-BRL-specific claims (Abr/2020 gold essay, Maio/2022 CNY, Nov/2022 generic EM, Jan/2026 generic EM) excluded on the same specificity bar throughout. Three real cross-manager echoes were found despite this: Junho/2024's joint fiscal/monetary-credibility BRL story matches Verde's own "sharpest single-month BRL move" finding for the identical month, and Dezembro/2024's BCB FX-intervention/capital-outflow claim matches Verde's own December-2024 finding almost exactly — independent confirmation from two managers of the same real-world events, despite very different house writing styles.

Rerun via:
```powershell
uv run python -c "from analytics.brasil.exchange_rate.models.fx_attribution_model import run; run(manager='kapitalo')"
```

## 2026H2 refresh — all three managers brought current (2026-09-08)

First incremental round after the initial full-history builds, and it took
**two passes**: the first appended 18 claims, the user challenged both the
extraction and the Kinea dates, and the re-extraction that followed cut those
18 to **6**. Both halves of that correction are recorded here, because the
failure modes are the reusable part.

Net: **+9 documents, +6 claims**, taking the corpus to Verde 200/175, Kinea
128/104, Kapitalo 85/15 (documents/claims). Coverage runs to **Ago/2026** for
Verde and Kinea and **Jul/2026** for Kapitalo — Kapitalo's August letter was
not yet published when this ran. New material: Verde 2026_06/07/08, Kapitalo
062026/072026, Kinea's "Dr. Strangelove" (published 01/08, the **July** letter)
and "A hora do pesadelo" (31/08, the August letter), plus the two Insights of
the period (both AI/tech deep-dives, zero FX claims — normal for that series).

### The first pass ignored extraction rule 2, and it cost 12 of 18 claims

The extraction was done having read this file's Corpus, Taxonomy and tail, but
**not** the "Extraction rules" section above — so claims were included on
topical relevance and our own economic priors instead of on the manager's own
stated FX link. Audited mechanically (does the quote itself contain câmbio /
cambial / dólar / real / moeda / BRL?), the first pass scored **6 of 18**.

Removed, all for the same reason — the quote names a topic that would
plausibly move the currency and never says it did:

| gestora | documento | categoria | por que saiu |
|---|---|---|---|
| Verde | 2026_06 | `capital_flows`, `politics_br`, `fiscal_br` | saída de fluxos, ciclo eleitoral e o acelerador parafiscal, nenhum ligado ao câmbio |
| Verde | 2026_07 | `politics_br` | volatilidade eleitoral prospectiva, sem link com moeda |
| Verde | 2026_08 | `politics_br` | pontuado sobre o mercado **acionário**, que é onde a carta observa a reprecificação |
| Verde | 2026_08 | `global_usd` +0.3 | também **regra 3**: segunda claim de mesma direção no mesmo documento |
| Kapitalo | 062026 | `risk_sentiment` | cesta genérica de moedas emergentes — a mesma barra de especificidade que excluiu Abr/2020, Maio/2022, Nov/2022 e Jan/2026 |
| Kapitalo | 072026 | `monetary_br` | comentário puro de juros; o parágrafo de Brasil da carta não menciona moeda nenhuma |
| Kinea | 01082026 | `fiscal_br` | "pautas-bomba", "pé no acelerador" — fiscal, nunca câmbio |
| Kinea | 31082026 | `capital_flows`, `politics_br`, `monetary_br`, `fiscal_br` | quatro claims temáticas, nenhuma citação com palavra de moeda |

Two rows were **changed rather than deleted**, and both are worth reading:

- **Kinea 01082026 `commodities` went from −0.2 to 0.0** — extraction rule 6.
  The letter's only direct BRL observation is that the real was well-behaved
  *despite* the energy shock, i.e. it names the channel and reports it did
  **not** move the currency. Scoring that negative read our own prior into an
  explicit non-move. Same pattern as Dec/2023's "teimosamente" and the Jun/2021
  export-boom puzzle.
- **Kinea 31082026 gained a `global_usd` −0.3** the first pass had missed:
  "Mantemos viés comprado em dólar. Além do avanço *hawk* do Fed…" — a
  positioning statement with an explicit stated reason, so it clears rule 5.
  Scored moderate because the framing is mixed under rule 4 (the Fed leg is
  broad, the elaboration is about Europe). **Leaving a valid claim out is the
  mirror of the error being fixed**, so the re-extraction looked in both
  directions, not only for rows to delete.

The six survivors pass the rule-2 audit 6 of 6, violate rule 3 nowhere, and
every quote segment was re-checked verbatim against `clean_md/`.

**What this costs the earlier writeup:** the "clearest cross-manager
disagreement in the corpus" claimed for Ago/2026 — Verde +0.4 vs. Kinea −0.4 on
`politics_br`, plus both reporting foreign outflows — **does not survive**. All
four of those rows failed rule 2. Both managers do write those things; neither
ties them to the currency, so the model correctly has nothing to say about it.
Same for the `monetary_br` disagreement between Kapitalo and Kinea. That is
rule 2 stated as a result: **a real disagreement between two houses is not an
FX attribution unless they frame it as one.**

**One cross-manager disagreement does survive, and it is a better example than
the one it replaces**, because both sides state it in currency terms. Verde and
Kinea agree on `global_usd` in Jul/2026 (+0.3 each, both reading the July FOMC
as removing the dollar premium) and split in **Ago/2026**: Verde +0.5, on
Bessent's long-end intervention "enfraquecendo o Dólar e beneficiando outras
moedas"; Kinea −0.3, on "Mantemos viés comprado em dólar. Além do avanço *hawk*
do Fed…". Same month, same channel, opposite sign, and each quote names the
currency itself — which is exactly the difference between this and the
`politics_br` pair that had to be withdrawn.

### The Kinea `month` was the publication month, and that is now fixed

The user reported the Kinea dates looked wrong. They followed the convention
already in the data — `documents.csv` had always keyed `month` on the
**publication** date — but the convention itself was the defect, and it was
Kinea-only: **Verde and Kapitalo already key `month` on the reference month**
(Verde by the `Verde-REL-YYYY_MM` filename, Kapitalo by the covered month's last
day), so Kinea was the odd one out rather than the standard.

Kinea publishes the "Carta do Gestor" for a closed month either in its last
days or in the first days of the next one. Under publication-month bucketing
that puts two letters in one month and none in its neighbour. Measured across
the 62 main letters:

| | meses com 2 cartas | meses vazios no span |
|---|---|---|
| `month` = publicação (antes) | **10** | **12** |
| `month` = referência (agora) | **1** | **3** |

2026 is where it became visible, because Kinea's timing turned irregular —
"Apollo 13" on 30/06, "Dr. Strangelove" on 01/08, "A hora do pesadelo" on 31/08
— stacking two letters into Ago/2026 and leaving Jul/2026 empty, which is the
screenshot that prompted the question. In 2024 the same convention shifted
**every** letter one month late without ever colliding, so the defect produced
no visible symptom for two years. Confirmed from content, not inferred:
`kinea_01082026.md` says "durante o mês de julho" and `kinea_01082024.md` says
"No mês de julho" three times.

**The migration:** for `source == 'kinea'` (the main letter only), a
publication date on day ≤ 5 moves `month` back one; `date` is untouched and is
still the real publication date. **`kinea_insights` is deliberately not
migrated** — those are thematic deep-dives, not monthly letters covering a
prior period, so their publication month *is* their reference month. 18 rows in
`documents.csv` and 27 in `claims.csv` moved; Kinea 2026 now reads one main
letter plus one Insights piece per month, Jan through Ago, with no empty month.
`repository/mental_model/kinea/fetch_kinea.py`'s docstring asserted the old
convention and was corrected with it.

**The reusable half:** a date convention that is *consistently applied* can
still be *wrong*, and consistency is what hides it. The test that exposed it is
structural, not textual — count documents per bucket and look for a source that
publishes N per period producing buckets of 2 and 0.

### And two acquisition notes still worth carrying

- **The publication date is in the PDF, not in a guess.** Verde's
  `documents.csv` dates match each PDF's own `creationDate` exactly on all four
  2026 rows checked. The gap between reference month and publication is not
  constant (3 to 11 days here), so deriving one from the other is wrong.
- **Quotes must be verified against the right reading text, and it is not
  always the raw dump.** Kapitalo's letters are two-column and the pdfplumber
  extraction interleaves them line by line, so *nothing longer than a line* is
  contiguous in `raw_md/` — a quote check against it fails on correct quotes.
  Rebuild column-aware (crop each page at mid-width) for verification. Verde
  fails for a different reason: the legal disclaimer is re-extracted at every
  page break, splitting sentences that span one, so verify against `clean_md/`.

## Files

- `fx_attribution_data/<manager>/documents.csv` — registry of that manager's
  source documents (date, month, source, filename) — the authoritative list
  for `n_documents`, independent of whether a document yielded any claims.
  Kinea's currently has 128 rows (Verde 200, Kapitalo 85). For Kinea the
  `month` of a main letter is the month it COVERS, not the one it is
  published in (migrated 2026-09-08, see the refresh section above);
  `kinea_insights` rows are keyed on publication, which for those is the
  same thing.
- `fx_attribution_data/<manager>/claims.csv` — that manager's hand-extracted
  claims (source of truth): date, month, source, source_file, category,
  direction, quote, note. Kinea's currently has 104 rows (Verde 175,
  Kapitalo 15).
- `fx_attribution_data/<manager>/monthly.csv` — derived: one row per month,
  regenerated by `aggregate_monthly()` from the two CSVs above.
- `fx_attribution_data/<manager>/fx_attribution.xlsx` — same data, three
  sheets: "Claims", "Monthly", and "Trends" (regenerated fresh every run —
  replaces an earlier hand-built "User tab" the user added directly in
  Excel, which had to be manually rebuilt after each re-extraction; this
  sheet doesn't). "Trends" holds two tables + two line charts side by side:
  **Relevância direcional** (3-month rolling average of the signed
  per-category sum — which way each regime is pointing) and **Grau de
  relevância** (3-month rolling average of `|score|` per category — how much
  each regime has mattered regardless of direction, so a month with
  offsetting claims still registers instead of netting toward an
  artificially low value).
- `fx_attribution_model.py` — `manager_dir()` / `load_claims()` /
  `load_documents()` / `aggregate_monthly()` / `rolling_mean()` /
  `export_excel()` / `run(manager="kinea")`.

Rerun (Kinea) via:
```powershell
uv run python -c "from analytics.brasil.exchange_rate.models.fx_attribution_model import run; run()"
```

## Pending

- **No automated (code-based) extraction yet, but subagent-delegated
  hand-extraction was tried for the first time and worked, 2026-07-30.**
  The 2010-2013 Verde round (see below) was the first to delegate the
  read-and-extract step to subagents (two, run in parallel, one per
  two-year block) rather than have Claude read every letter directly in
  the main session — a deliberate test of the exact question this bullet
  used to only flag hypothetically. Result: no schema drift observed (both
  agents returned the same JSON shape, same category vocabulary, quotes in
  source-language Portuguese, notes in English); one genuine judgment call
  surfaced and was handled transparently rather than silently — the
  2010-01 letter's relative-valuation/mean-reversion argument didn't
  cleanly fit any of the 9 categories, and the agent folded it into
  `capital_flows` with an explicit note flagging the boundary call rather
  than inventing a 10th category or silently mis-filing it. Worth reusing
  this pattern for Kapitalo/SPX, but still only one data point — not yet
  "proven safe" for a much larger fan-out (e.g. all of Kapitalo's 83
  letters at once).
- **Verde Asset done, partially — 2010-01 through 2026-05 only** (see the
  "Verde Asset" section above). The full 1999-2026 `raw_pdf/` archive is
  not extracted, just the 2010+ window extracted so far across six
  rounds; extending further backward to 1999-2009 would be a distinct next
  step, not an automatic follow-on. Kapitalo (83 PDFs) and SPX Capital (7
  PDFs) are still untouched candidate corpora — same folder convention +
  `run(manager=...)` applies.
- **No dashboard yet, by design.** Per direct user instruction (2026-07-29),
  this stays numbers-only (CSV/Excel) for now; the eventual visualization is
  a new tab in the FX report (then `reports/ppp_dashboard.html`, fused into
  `reports/brasil/FX Report.html` in 2026-08 — stacked bar per category,
  `n_documents`/`n_claims` visible alongside), not a standalone page.
- **Reusability for other text-scoring tasks** (e.g. Copom hawkish/dovish)
  is an explicit design goal but hasn't been attempted — nothing here is
  factored out into a generic module yet, since a single application isn't
  enough evidence for what the generic interface should look like.
