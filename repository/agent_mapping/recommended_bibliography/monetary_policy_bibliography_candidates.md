# Monetary Policy — Bibliography Candidates (acquisition tracker)

**Purpose:** what is still to be sourced for the monetary-policy agent's technical literature, with
priority, suggested filename and where to get it — plus the extraction quirks of the PDFs already
in hand, which have to be handled before ingestion. Built following `BIBLIOGRAPHY_METHODOLOGY.md`.

**Since 2026-10-07 this file holds only what is pending.** The full list — every source, acquired or
not, with what it contributes to the agent and whether it reached the vault — is
[`monetary_policy_bibliography.md`](monetary_policy_bibliography.md). Same split as exchange rate
(`exchange_rate_bibliography.md` is the list, `_gaps.md` the tracker). The cluster numbers are kept
because other bibliographies cite them (the fiscal file's boundary note on cluster 7, for one);
a cluster with nothing pending says so.

**Acquired PDFs** live in `repository/monetary_policy/raw_pdf/theorical_literature/` (46 files on
2026-10-07). Naming convention: `topic_description (Author, Year).pdf`, with the year of the
canonical published version even when the file is a working-paper copy. Ingestion into the vault is
a separate step: `repository/ingestion/scripts/run.py`, one PDF at a time.

**Priority:** high = answers one of the agent's standing questions directly (the table at the top of
the bibliography file); medium = thickens a cluster the agent uses; low = reference depth.

---

## Pending, by cluster

### 1. `#policy_rules_and_credibility` — nothing pending

### 2. `#new_keynesian_transmission` — nothing pending

### 3. `#inflation_targeting_regimes`

| Source | Priority | Suggested filename | Where |
|---|---|---|---|
| Svensson, L. (2010), "Inflation Targeting," *Handbook of Monetary Economics* vol. 3B | low | `inflation_targeting_handbook (Svensson, 2010).pdf` | NBER WP 16654 |

### 4. `#transmission_channels_financial_frictions`

| Source | Priority | Suggested filename | Where |
|---|---|---|---|
| Havranek, T. & Rusnak, M. (2013), "Transmission Lags of Monetary Policy: A Meta-Analysis," *IJCB* | medium | `transmission_lags_meta_analysis (Havranek & Rusnak, 2013).pdf` | Czech National Bank working-paper version; *IJCB* is open access (ijcb.org) |

### 5. `#unconventional_policy_zlb` — nothing pending

### 6. `#global_spillovers_em_autonomy`

| Source | Priority | Suggested filename | Where |
|---|---|---|---|
| Kalemli-Özcan, Ş. (2019), "U.S. Monetary Policy and International Risk Spillovers," Jackson Hole | medium | `us_policy_international_risk_spillovers (Kalemli-Ozcan, 2019).pdf` | NBER WP 26297 / Kansas City Fed symposium page |
| Ostry, J., Ghosh, A. & Chamon, M. (2012), "Two Targets, Two Instruments," IMF SDN 12/01 | medium | `two_targets_two_instruments (Ostry, Ghosh & Chamon, 2012).pdf` | imf.org — manual download (see the IMF note below) |

### 7. `#brazil_monetary_policy`

| Source | Priority | Suggested filename | Where |
|---|---|---|---|
| Arida, P., Bacha, E. & Lara-Resende, A. (2005), "Credit, Interest, and Jurisdictional Uncertainty," in Giavazzi, Goldfajn & Herrera (eds.), MIT Press | medium | `credit_interest_jurisdictional_uncertainty (Arida, Bacha & Lara-Resende, 2005).pdf` | Book chapter; look for the IEPE/Casa das Garças working-paper version |
| de Castro, M. et al. (2011), "SAMBA," BCB WP 239 + updated version, BCB WP 578 | medium | `samba_dsge_brazil (de Castro et al., 2011).pdf` and `samba_dsge_brazil_update (BCB WP 578).pdf` (confirm authors/year of 578 on acquisition) | bcb.gov.br/pec/wps/ingl/wps239.pdf, wps578.pdf |
| Bonomo, M. & Martins, B. (2016), "The Impact of Government-Driven Loans in the Monetary Transmission Mechanism," BCB WP 419 | medium | `directed_credit_monetary_transmission (Bonomo & Martins, 2016).pdf` | bcb.gov.br/pec/wps/ingl/wps419.pdf |

**The 2006 cutoff is partly closed.** The open gap this cluster carried — nothing after 2006 — is
now covered on transmission (Minella & Souza-Sobrinho 2013, Bonomo & Martins 2016), the FX reaction
(Kohlscheen 2014) and the BCB's model (SAMBA). Still uncovered by technical literature: the 2015-16
recession and the 2021-23 cycle. For those, the Copom's own documents (§8) and the technical boxes
of the RPM — which come with the full RPM history, `SISTEMA_AGENTES.md` II.III.iv — are the primary
source, not a paper still to be found.

### 9. `#reaction_function_and_gradualism`

| Source | Priority | Suggested filename | Where |
|---|---|---|---|
| Brainard, W. (1967), "Uncertainty and the Effectiveness of Policy," *AER P&P* | medium | `uncertainty_policy_effectiveness (Brainard, 1967).pdf` | JSTOR (paywalled); no free copy checked yet |
| Woodford, M. (2003), "Optimal Interest-Rate Smoothing," *REStud* | medium | `optimal_interest_rate_smoothing (Woodford, 2003).pdf` | Woodford's Columbia page; the precursor is NBER WP 7884 ("Optimal Monetary Policy Inertia") |

### 10. `#policy_surprises_and_information_effect`

| Source | Priority | Suggested filename | Where |
|---|---|---|---|
| Gürkaynak, R., Sack, B. & Swanson, E. (2005), "Do Actions Speak Louder Than Words?," *IJCB* | medium | `policy_actions_vs_words (Gurkaynak, Sack & Swanson, 2005).pdf` | *IJCB* is open access; also Fed FEDS 2004-66 |
| Christiano, L., Eichenbaum, M. & Evans, C. (1999), "Monetary Policy Shocks: What Have We Learned and to What End?," *Handbook of Macroeconomics* 1A | low | `monetary_policy_shocks_survey (Christiano, Eichenbaum & Evans, 1999).pdf` | NBER WP 6400 |
| Romer, C. & Romer, D. (2004), "A New Measure of Monetary Shocks: Derivation and Implications," *AER* | low | `new_measure_monetary_shocks (Romer & Romer, 2004).pdf` | NBER WP 9866 / the authors' Berkeley pages |

### 11. `#communication_and_forward_guidance` — nothing pending

### 12. `#neutral_rate`

| Source | Priority | Suggested filename | Where |
|---|---|---|---|
| Segura-Ubiergo, A. (2012), "The Puzzle of Brazil's High Interest Rates," IMF WP 12/62 | **high** | `high_interest_rates_puzzle_brazil (Segura-Ubiergo, 2012).pdf` | imf.org/external/pubs/ft/wp/2012/wp1262.pdf — **manual download** |
| Perrelli, R. & Roache, S. (2014), "Time-Varying Neutral Interest Rate — The Case of Brazil," IMF WP 14/84 | **high** | `neutral_rate_time_varying_brazil (Perrelli & Roache, 2014).pdf` | imf.org/external/pubs/ft/wp/2014/wp1484.pdf — **manual download** |

### 13. `#term_structure_and_market_pricing`

| Source | Priority | Suggested filename | Where |
|---|---|---|---|
| Adrian, T., Crump, R. & Moench, E. (2013), "Pricing the Term Structure with Linear Regressions," *JFE* | medium | `term_structure_linear_regressions (Adrian, Crump & Moench, 2013).pdf` | NY Fed Staff Report 340 |

### Primary legal sources

| Source | Priority | Suggested filename | Where |
|---|---|---|---|
| Decreto nº 3.088/1999 | medium | `decreto_3088_1999_metas_inflacao.pdf` | planalto.gov.br |
| Lei Complementar nº 179/2021 | medium | `lc_179_2021_autonomia_bcb.pdf` | planalto.gov.br |
| Decreto nº 12.079/2024 | medium | `decreto_12079_2024_meta_continua.pdf` | planalto.gov.br |

**The IMF blocks automated download.** imf.org returns 403 to scripted requests (Akamai), for both
the `/external/pubs/ft/wp/` and the `/-/media/` paths, from curl and from PowerShell alike (tested
2026-10-07). The papers themselves are free — open the link in a browser and save the PDF into
`raw_pdf/theorical_literature/` with the suggested filename. Third-party mirrors were not used.

---

## Dropped (2026-10-07)

| Source | Why dropped |
|---|---|
| Woodford, M. (2003), *Interest and Prices* — book | Covered for this agent by Galí (2015) ch. 3-5 and Clarida-Galí-Gertler (1999) |
| Cukierman, A. (1992), *Central Bank Strategy, Credibility, and Independence* — book | Theory covered by Rogoff, Walsh and Barro-Gordon; the CBI index matters only for cross-country work |
| Bernanke, B., Laubach, T., Mishkin, F. & Posen, A. (1999), *Inflation Targeting* — book | Covered by Svensson (1997), Mishkin (2000) and the Brazil IT papers |

---

## Extraction quirks of PDFs already in hand — handle before ingestion

| File | Problem | What to do |
|---|---|---|
| `science_of_monetary_policy (Clarida, Gali & Gertler, 1999).pdf` | Text layer is Caesar-shifted (font-encoding artifact); extraction reads as garbage | Either decode (every character's code minus 3 — verified on the 2000 paper, same encoding) or replace with NBER WP 7147 |
| `monetary_policy_rules_stability (Clarida, Gali & Gertler, 2000).pdf` | Same Caesar shift (UPF Economics WP 350 copy, May 1999). The NBER WP 6442 copy is scanned, no text layer at all, which is why this copy was kept | Decode by subtracting 3 from each character code; tested on the title page, reads correctly |
| `financial_accelerator (Bernanke, Gertler & Gilchrist, 1999).pdf` | Scanned, no text layer | Replace with NBER WP 6455 |
| `optimal_contracts_central_bankers (Walsh, 1995).pdf` | Scanned, no text layer | Low priority; OCR or a vision read if ever needed |
| `policy_rules_real_time_data (Orphanides, 2001).pdf` | Fed FEDS 1998-03; pdfplumber separates every letter with a space, pymupdf only some ("con tribute") | Try a larger `x_tolerance` in `extract.py`; the only free copy found |
| Galí (2015) chapters, Kydland & Prescott (1977), Bernanke & Gertler (1995) | Words run together ("Thepresentchapter") | The opposite tolerance problem; tune `extract.py` per file |

---

## 8. `#brazil_policy_communication` — Copom primary sources

A recurring institutional feed, not settled literature; no foundational score. **The two decisions
this section used to defer are taken:** retention is the full history for comunicados (234) and atas
(261), and the RPM for the last three years in full (12, Dec/2023 on); ingestion is the Copom ETL
(`pm_copom_projecoes.run()`, code in `domain/db/brasil/bcb/_copom_texto.py` and
`_rpm_projecoes.py`), writing straight into `obsidian/monetary_policy/clean_md/central_bank/`. Still
pending: the full RPM history (`SISTEMA_AGENTES.md` II.III.iv).

| Document | Portuguese name | Cadence |
|---|---|---|
| Statement | Comunicado | Same day as each meeting (~8/year) |
| Minutes | Ata do Copom | ~6 business days after the meeting |
| Quarterly Report | Relatório de Política Monetária (RPM; *Relatório de Inflação* before 2023) | Mar/Jun/Sep/Dec |

---

## History

- **2026-07-06 → 2026-07-13** — first pass: 31 candidates in 7 clusters plus the §8 Copom track; 26
  acquired from free copies, each checked against its own title page.
- **Later in 2026-07/08** — Rogoff (1985), Galí (2015) ch. 2-8, Tambakis & Tarashev (2012) and BIS
  (2026) added; 36 PDFs.
- **2026-10-07** — review against the agent's standing questions. Five clusters added (9-13), the
  three books dropped, the acquired rows moved to `monetary_policy_bibliography.md`. Ten of the
  twelve high-priority sources acquired the same day, each checked against its title page:
  Clarida-Galí-Gertler (2000), Orphanides (2001), Nakamura & Steinsson (2018), Jarociński & Karadi
  (2020), Kohlscheen (2014), Minella & Souza-Sobrinho (2013), Laubach & Williams (2003), Holston,
  Laubach & Williams (2017), Blinder et al. (2008), Campbell et al. (2012). The two IMF papers need a
  browser.
</content>
