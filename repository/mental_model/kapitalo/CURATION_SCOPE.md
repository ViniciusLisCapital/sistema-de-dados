# Curation scope — Kapitalo K10 monthly letters

## Purpose

Feeds the same macro/FX mental-model synthesis use case as the Verde Asset corpus
(`repository/mental_model/verde_asset/`): we want the manager's own reasoning, stated
market view, and positioning, not fund administrivia. The performance/attribution
table is kept as supporting structured data (it's what the commentary is explaining),
not as the primary content.

## Always keep

- The scenario/market-view commentary ("Cenário" in the older template, an untitled
  or ad-hoc-titled section right after the letter header in the newer template) —
  this is the manager's actual reasoning.
- The "Posições" section (position summary by asset class: Moedas, Commodities,
  Bolsa, Juros) — what they actually did as a result of that reasoning.
- Any standalone thematic/deep-dive section when present (e.g. the "Colômbia" section
  in the Maio 2026 letter) — same status as the scenario commentary, just longer-form.
- The "Atribuição de Performance" / "ATRIBUIÇÃO DE PERFORMANCE" table (monthly, YTD,
  12M, 24M, 60M, since-inception return by strategy: Juros, Moedas, Bolsa,
  Commodities, Caixa e Custos, CDI, Performance do Fundo, %CDI). This table extracts
  cleanly as one row per line in both format eras — no reconstruction needed, just
  reflow into a markdown table.

## Always drop

- "Alocação por Fator de Risco" / "ALOCAÇÃO POR FATOR DE RISCO" — a VaR bar chart
  (Mín/Médio/Máx per risk factor). The extracted text is a flat list of percentages
  with no reliable per-bar label attached (chart noise, not structured data) — never
  attempt to reconstruct which number belongs to which factor.
- The legal/regulatory disclaimer block (always the paragraph starting near
  "Este conteúdo foi preparado pela..." / "Este conteúdo foi elaborado por...").
- The "Material Informativo" fund-characteristics section: Objetivo do Fundo,
  Política de Investimentos, the full historical monthly-returns grid ("Retornos
  Líquidos..."), the return-distribution statistics block, the return charts, and the
  fund's administrative info (CNPJ, minimums, redemption terms, addresses, SAC/
  Ouvidoria phone numbers). None of this is manager reasoning; it repeats verbatim
  (aside from the returns grid extending by one row) every month.
- The "PERFORMANCE DESDE O INÍCIO" cumulative-return line chart (newer template only)
  — same chart-noise reasoning as the VaR bar chart; the since-inception column of
  the Atribuição table already carries this number.

## Known PDF format eras

- **Era 1 — "Carta K10" (Jul/2019–Aug/2023, ~52 letters).** Single-column body text.
  `utils/extract_pdf.py` (pdfplumber, no layout awareness) extracts this cleanly —
  reading order is correct, the Atribuição table is one row per line, boilerplate
  starts predictably after the table.
- **Era 2 — "CARTA DO GESTOR" (Sep/2023–present, 33 letters as of 2026-07-30:
  Sep–Dec 2023, all of 2024, all of 2025, Jan–May 2026).** Two-column layout for the
  scenario commentary and "Posições" sections specifically. Plain pdfplumber
  extraction interleaves the two columns line-by-line into nonsense (confirmed
  empirically, not just suspected — see `repository/CLAUDE.md`'s pending caveat and
  this corpus's `raw_md/` for the pre-fix files). The structured tables (Atribuição de
  Performance, and the VaR chart's flat number list) are NOT affected — they render as
  full-width single blocks in the source PDF and extract in correct order even under
  plain pdfplumber. Only the narrative sections needed column-aware re-extraction
  (direct PDF read preserving left-column-then-right-column order), not the whole
  file.

## Known format eras (continued)

- **A third legal-disclaimer wording variant exists**: "Esse documento foi
  elaborado pelo grupo Kapitalo (Kapitalo Investimentos e Kapitalo Ciclo)..."
  — used around the Kapitalo Investimentos/Kapitalo Ciclo rebranding period
  (first confirmed in Abr/2022). `curate.py`'s `DISCLAIMER_ANCHORS` now
  includes this alongside "este conteúdo foi preparado" / "este conteúdo foi
  elaborado" / "a kapitalo ciclo não comercializa". If a future file errors
  with "disclaimer anchor not found", check its actual wording before adding
  yet another variant — don't assume it's the same fix.
- **Era 3 — a further PDF layout tweak starting Mar/2025** (still "CARTA DO
  GESTOR", not a new named template, but a real structural change, not
  garbling). Three things changed simultaneously, all confirmed from
  Mar/2025 through Dez/2025:
  1. Both section titles that `curate.py` searches for as literal one-line
     phrases now render split across two lines by pdfplumber: "ALOCAÇÃO" /
     "POR FATOR DE RISCO" (sometimes with a stray VaR percent glued onto
     either line) and "ATRIBUIÇÃO" / "DE PERFORMANCE". Handled via
     `ALOCACAO_MARKER_RE` / `ATRIBUICAO_HEADER_RE`, tried as a fallback only
     when the plain literal-phrase search fails (so era 1/2 files are
     untouched).
  2. The "*Mínimo, Médio e Máximo..." footnote — which era 1 always places
     right before the Atribuição table, and which `curate.py` uses to bound
     era 1's table zone — now sits right after the ALOCAÇÃO title, BEFORE
     the chart bars even start. Bounding the zone at the footnote (era 1's
     path) would cut off the entire chart+table that follows. Fixed by
     preferring the (now regex-detected) standalone "ATRIBUIÇÃO DE
     PERFORMANCE" header to start the table zone whenever it's found,
     closer to era 2's clean-header shape than era 1's footnote-bounded one
     — the footnote path is now purely a fallback for files where no
     standalone header exists at all.
  3. The "Performance do Fundo" row's label wraps across two lines too — a
     lone "Performance" line, then "do Fundo -0,05% ..." on the next — since
     every `ROW_LABEL_PATTERNS` regex is deliberately single-line-only.
     Fixed with `merge_wrapped_performance_label()`, which rejoins that
     specific two-line shape before per-line label matching runs; every
     other line is passed through untouched.
  
  All three fixes are additive fallbacks gated behind "if the literal/era-1
  path already worked, don't touch it" — re-running the full 2019–2024
  batch was not needed to confirm this, since those years all already
  validated via the original literal-string paths before this change.

## Known unresolved limitations

- **Embedded chart-axis noise inside thematic annexes/essays — a recurring
  pattern, not a one-off.** Several era-1 letters have a long standalone
  deep-dive (e.g. Jul/2019's "Estudo de Caso" on NOK, Abr/2020's "Anexo I —
  O Ouro Como Alternativa de Investimento") with many embedded charts. The
  essay prose itself is genuinely valuable and is kept in full (per the
  "always keep" thematic/deep-dive rule) — `curate.py` only bounds and
  extracts the VaR/Atribuição table zone, it doesn't touch essay text at all.
  But these essays carry pre-existing chart-extraction noise from the
  ORIGINAL raw_md (bare axis-tick numbers, and in Abr/2020's case entire
  axis date labels extracted character-reversed, e.g. "78\n-naj" = "jan-87"
  read backwards). Left as-is rather than mechanically stripped: distinguishing
  real chart noise from legitimate short prose lines reliably, across
  whatever essay a given month happens to have, would need the same
  chart-by-chart manual judgment used for the PDF re-extraction work, not a
  generic rule safe to automate. Expect this in other months with a
  standalone annex/estudo de caso section — readable but noisier than the
  rest of the corpus in those specific stretches.
- Minor cosmetic-only quirk, not content loss: some era-1 multi-page letters
  (e.g. Dec/2019) repeat the running page header ("Carta K10 – <Mês> <Ano>")
  mid-paragraph in `clean_md`, carried through unchanged from `raw_md`.
  `curate.py` doesn't strip these.

## Progress (updated as years are processed)

- 2019 (Jul–Dec, 6 letters) — done, all cross-validated. `curate.py` written
  and debugged against this batch (fixed: an accent-stripping index-alignment
  bug, an era-1/era-2 misdetection bug where the combined "Alocação por Fator
  de Risco* Atribuição de Performance" title line falsely looked like era 2's
  standalone header, and a "% CDI" vs "CDI" label collision).
- 2020 (12 letters) — done, all cross-validated, no new script bugs found.
- 2021 (12 letters) — done, all cross-validated, no new script bugs found.
- 2022 (12 letters) — done, all cross-validated. Abr/2022's raw_md was
  missing the ATRIBUIÇÃO DE PERFORMANCE table and the legal disclaimer
  entirely (a genuine original-extraction gap, not garbling) — re-read
  directly from `raw_pdf/kapitalo_k10_042022.pdf` and patched into raw_md,
  cross-validated before trusting. Also surfaced the third disclaimer
  wording variant noted above.
- 2023 (12 letters) — done, all cross-validated, no new script bugs found.
  Includes the Set/2023 era transition (last era-1 letter Ago/2023, first
  era-2 "CARTA DO GESTOR" letter Set/2023) — both eras' shapes handled
  correctly with no code changes needed.
- 2024 (12 letters) — done, all cross-validated, no new script bugs found.
  All era-2 "CARTA DO GESTOR" shape.
- 2025 (12 letters) — done, all cross-validated. Jan/Fev 2025 matched the
  existing era-2 shape with no changes. Mar/2025 onward (10 letters)
  introduced the "era 3" layout tweak documented above (split section
  titles, relocated footnote, wrapped Performance-row label) — `curate.py`
  updated with additive regex fallbacks to handle it, all 10 re-validated
  successfully after the fix.
- 2026 (Jan–May, 5 letters) — done, all cross-validated, no new script bugs
  found (era 3 shape throughout). Maio/2026 includes the standalone
  "Colômbia" thematic section (kept in full per the always-keep rule).

**All 83 letters (Jul/2019–Mai/2026) now have both raw_md and clean_md,
cross-validated.** Corpus curation complete as of 2026-07-31.
