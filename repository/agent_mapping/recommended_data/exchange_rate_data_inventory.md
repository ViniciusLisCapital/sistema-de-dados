# Exchange Rate Data Inventory

**Purpose:** inventory of the data categories relevant to exchange rate (BRL) analysis — what each category is *for* analytically, and what already exists in the database (`macro_brasil` / `macro_international` — see `domain/db/CLAUDE.md`; `macro_analytics` was discontinued in 2026-07) and to what's still missing. Meant to inform the exchange rate analysis agent (see `.claude/agents/cambio-analyst.md`) about which series are available to support each type of argument.

**Cross-linked to the literature in two places.** Each section below opens with a **Why it matters** line naming the argument the category serves; the reverse direction — which theory each of these categories is evidence *for* — lives inside `../conceptual_maps/exchange_rate_conceptual_map.md`, whose clusters each carry a *Data that backs this cluster* block citing the section numbers used here. The reading list itself is `../recommended_bibliography/exchange_rate_bibliography.md`. That join is at **cluster** level only: individual concepts are not linked to individual series.

**The Why-it-matters lines were merged in on 2026-09-10** from a second, presentation-layer copy of this inventory that lived in `team_materials/` (as `data_inventory.md`), when that folder was narrowed to presentation-only material. That copy carried the same 8 categories in the same order, minus the database/status columns — so only the analytical rationale was new, and the file was deleted rather than kept in parallel. Its category order is the one used here: the price itself, then the two fastest-moving determinants (carry, terms of trade), then balance-of-payments flow and stock measures, then market positioning.

Technical details on schema, SGS codes and observation counts live in `analytics/brasil/exchange_rate/CLAUDE.md` — this file organizes the same information by analytical category instead of by table.

---

## 1. Spot price — ✓ resolved (2026-07)

**Why it matters:** the dependent variable — every other category in this inventory exists to explain moves in this one series.

| What we have | Table | Series | Coverage |
|---|---|---|---|
| PTAX sell (spot) | `macro_brasil.cmb_ptax` | `ptax_venda` (SGS 1) | 1994-07-01 → today, daily (Real Plan implementation — pre-Real data in extinct currencies excluded) |
| Interbank FX volume, T+1/T+2 settlement | `macro_brasil.cmb_ptax` | `fx_interbank_vol_t1` (SGS 20359), `fx_interbank_vol_t2` (SGS 20205) | 1994-07-04 → today, daily |

Script: `domain/db/brasil/bcb/cmb_ptax.py`. Daily series — historical load chunks by year (BCB API rejects windows > 10 years for daily series, confirmed via 406 response).

**Remaining gap:** the analysis agent (`analytics/brasil/exchange_rate/agent_data.py`) hasn't been updated yet to pull `cmb_ptax` into its snapshot — the data exists but isn't wired into the agent's output.

---

## 2. Interest rate differential (carry)

**Why it matters:** Selic and Fed Funds are the domestic and foreign legs of every carry argument (Verde's §3.1/§3.2 mental models). The **real ex-post** differential is the UIP-relevant comparison — it strips the pure inflation-differential effect out of the real-rate signal — while the **ex-ante** version is what markets are actually pricing, which is the input UIP and the fair-value models in the bibliography's cluster 2 actually need. The **cupom cambial** is the BCB's own named gauge for the cost of onshore dollar liquidity, Brazil's local instance of the CIP-basis concept, and Verde's tracked carry instrument (§3.4); DOL/WDO futures give the market-implied forward points directly.

| What we have | Table | Series | Coverage |
|---|---|---|---|
| Selic (raw) | `macro_international.diferenciais_juros` | `selic` | 1999-03 → today (SGS 432 has no earlier data) |
| Fed Funds (raw) | `macro_international.diferenciais_juros` | `fed_funds` | 1995 → today |
| Nominal ex-post differential | `macro_international.diferenciais_juros` | `diferencial_nominal` | 1999-03 → today |
| Real ex-post differential (Selic − IPCA vs. Fed Funds − CPI) | `macro_international.diferenciais_juros` | `real_br_ex_post`, `real_us_ex_post`, `diferencial_real` | 1999-03 → today |

Script: `domain/db/international/fred/diferenciais_juros.py`. Full history load (2026-07): `selic` (SGS 432, daily) is chunked in 8-year windows to avoid the BCB API's 406 on windows > 10 years.

**Gaps:**
- **Ex-ante** differentials (based on expectations, not realized inflation) not implemented yet — see the pending item in `analytics/brasil/exchange_rate/CLAUDE.md`, uses `macro_brasil.expc_focus` (Focus) on the BR side and FRED (`FF{m}` futures/OIS, `MICH`/`T5YIE`) on the US side.
- Cupom cambial (DDI/FRC curve) and B3 futures (DOL/WDO) — deferred, requires Bloomberg access (`blpapi`/`xbbg`).

---

## 3. Terms of trade / commodity prices

**Why it matters:** the aggregate index is the signal behind every commodity-exporter currency argument (BEER's fundamental driver set, GSFEER's current-account channel). Individual commodity prices decompose *which* commodity is driving a move — needed to tell a structural, volume-driven surplus from a cyclical, price-driven one (Verde's §2.1/§2.2).

| What we have | Table | Series | Note |
|---|---|---|---|
| Terms of trade index (PX/PM, base 2018=100) | `macro_brasil.cmb_termos_troca` | `termos_de_troca_funcex` (IPEADATA `FUNCEX12_TTR12`) | 1978 → today, monthly |

Script: `domain/db/brasil/ipea/cmb_termos_troca.py`. Source: Funcex, via the IPEADATA OData API (`connectors/ipeadata.py`) — **not** BCB SGS.

**Correction (2026-07):** the previous entries here (`termos_de_troca_a`/`b`, BCB SGS 22099/22100) were confirmed to be **National Accounts (GDP) series, not terms of trade** — BCB SGS does not publish a terms-of-trade index at all. Those two series and their rows were removed from `cmb_termos_troca`.

**Gaps:**
- No individual commodity prices (iron ore, soybeans, oil) — only the aggregate Funcex index. If the agent needs to decompose terms of trade by commodity, there's no data for that today.

---

## 4. Balance of payments

**Why it matters:** the flow-side counterpart to the trade-balance/capital-account identity at the base of the whole determination cluster. The FDI-vs-portfolio split is not cosmetic: FDI is the safest instrument in the capital-inflow riskiness ranking (Ostry et al. 2010), portfolio flows the riskier and more reversible counterpart — and that split is what the capital-controls literature (bibliography cluster 7) is built around, so tracking them separately is what lets crisis vulnerability be read at all.

| What we have | Table | Series | Coverage |
|---|---|---|---|
| Current account, trade balance+services, goods exports | `macro_brasil.cmb_balanco_pagmt` | `conta_corrente`, `balanca_comercial_servicos`, `exportacao_bens` | 2001 → today |
| Financial account, FDI (net and inflows), outward FDI | `macro_brasil.cmb_balanco_pagmt` | `conta_financeira`, `investimento_direto_liquido`, `idp_ingressos`, `ide_saidas` | 2001 → today |
| Portfolio investment (total, equities, fixed income) | `macro_brasil.cmb_balanco_pagmt` | `investimento_carteira`, `carteira_acoes`, `carteira_renda_fixa` | 2001 → today |

Script: `domain/db/brasil/bcb/cmb_balanco_pagmt.py`. BPM6 methodology.

**Gaps:** none identified at this time — coverage considered complete for the current FX report's purposes.

---

## 5. FX flow (registered vs. contracted)

**Why it matters:** registered flow is the broadest registered-channel measure, the empirical counterpart to the flow-supply/demand channel in the current-account-adjustment framework; contracted FX is the transactional, settlement-level view of the same market.

Two distinct tables measuring different channels — **not substitutes for one another**:

### 5a. Registered FX flow (BCB Nota Cambial)

| What we have | Table | Series |
|---|---|---|
| Total balance/inflow/outflow | `macro_brasil.cmb_fluxo_cambial` | `total_saldo`, `total_entrada`, `total_saida` |
| Commercial sector (inflow/outflow) | `macro_brasil.cmb_fluxo_cambial` | `comercial_entrada`, `comercial_saida` |
| Financial sector (balance) | `macro_brasil.cmb_fluxo_cambial` | `financeiro_saldo` |

Script: `domain/db/brasil/bcb/cmb_fluxo_cambial.py`. Coverage: 2003 → today.

**Gaps:** CEP/CBE sub-items of the financial flow (finer granularity, published in the weekly Nota Cambial) — candidate SGS codes (24372–24376) unconfirmed. Commercial balance (24366) timed out during research — can be derived as `comercial_entrada − comercial_saida` if needed.

### 5b. Contracted FX (bank-client movement)

| What we have | Table | Series |
|---|---|---|
| Daily — total balance, exports (total/ACC/PA/other), imports, commercial balance, financial purchases/sales/balance | `macro_brasil.cmb_cambio_contratado` | `cc_saldo_total`, `cc_export_*`, `cc_import_total`, `cc_saldo_comercial`, `cc_fin_compras`, `cc_fin_vendas`, `cc_fin_saldo` | since Sep/2008 |
| Monthly — detailed financial breakdown (services, income, domestic/foreign capital) | `macro_brasil.cmb_cambio_contratado` | `cc_fin_saldo_det`, `cc_fin_servicos`, `cc_fin_rendas`, `cc_fin_cap_bras`, `cc_fin_cap_ext` | since 1982 (monthly) / 2011 (detailed) |

Script: `domain/db/brasil/bcb/cmb_cambio_contratado.py`. ~46k observations.

**Conceptual difference:** `cmb_cambio_contratado` measures bank-client settlements (BCB Tables 13/14); `cmb_fluxo_cambial` (24xxx codes) is a broader measure covering all registered channels — the two should not be summed or treated as equivalent.

---

## 6. International reserves and BCB intervention

**Why it matters:** the stock side is how much ammunition the BCB has, central to every fixed/managed-rate defense argument in the bibliography's cluster 3. Banks' net FX spot position is the banking-system mirror of the carry trade (`posicao_vendida_carry_incentive` in the conceptual map, sourced from the BCB's own technical note) — who is actually short or long FX onshore. The swap position is the off-balance-sheet instrument the BCB uses *instead of* spot intervention, and the repo-line stock is temporary liquidity, distinct from a permanent reserves change. The intervention series are the flow side: what the BCB is doing right now, as opposed to what it holds.

| What we have | Table | Series (main) | Frequency |
|---|---|---|---|
| Total reserves and by component (FX securities, deposits, IMF, SDR, gold, other assets) | `macro_brasil.cmb_reservas_bc` | `reserves_total_monthly`, `reserves_fx_*`, `reserves_imf_position`, `reserves_sdrs`, `reserves_gold_*`, `reserves_other_*` | monthly |
| Reserves — total and liquidity concept | `macro_brasil.cmb_reservas_bc` | `reserves_total_daily`, `reserves_liquidity_daily` | daily |
| Banks' net FX spot position | `macro_brasil.cmb_reservas_bc` | `bank_fx_spot_position` (SGS 21195) | monthly |
| BCB FX swap — net position | `macro_brasil.cmb_reservas_bc` | `bcb_swap_cambial_position` (SGS 29533) | monthly |
| Stock of repo lines/loans/repurchase agreements in FX | `macro_brasil.cmb_reservas_bc` | `bcb_fx_stock_repos_loans` (SGS 29534) | monthly |
| BCB interventions (spot, forwards, FX loans/repos, repo lines) — only days with actual intervention | `macro_brasil.cmb_reservas_bc` | `bcb_intervention_spot`, `bcb_intervention_forwards`, `bcb_intervention_fx_loans_repos`, `bcb_intervention_repo_lines` | daily (sparse) |

Script: `domain/db/brasil/bcb/cmb_reservas_bc.py`. ~19k observations total. Full detail in `analytics/brasil/exchange_rate/CLAUDE.md`.

**Coverage considered robust** — includes both the stock (reserves, bank position, swap) and the intervention flow (BCB's net buying/selling in spot and forwards), which lets the agent distinguish "how much the BCB has" from "what the BCB is doing right now."

**Gaps:** none identified — the historical "gross reserves" pending item (SGS 13127, timeout) has been superseded by using the liquidity concept plus detailed components.

---

## 7. Real effective exchange rate (REER)

**Why it matters:** the core equilibrium-valuation benchmark underlying BEER/GSDEER-style arguments. The peer set is what lets BRL's REER move be read relative to comparable currencies rather than in isolation — which matters more here than it would elsewhere, since the base's non-Brazil EM depth is otherwise thin (see bibliography cluster 3).

| What we have | Table | Coverage |
|---|---|---|
| Real (broad) and nominal (broad) REER — Brazil, Mexico, Chile, Colombia | `macro_international.cmb_reer` | 1994 → today (BIS, full history) |

Script: `domain/db/international/bis/cmb_reer.py`. Source: BIS Statistics API.

**Gaps:**
- Only 4 LatAm countries (BR/MX/CL/CO) — no coverage of other relevant EM peers for comparison (e.g., Turkey, South Africa, India) or developed-market peers.
- `real_narrow` was excluded from scope (broad basket only).

---

## 8. Speculative positioning (FX futures)

**Why it matters:** the standard futures-market positioning gauge, and the data behind Verde's §5.3 positioning-as-contrarian-signal mental model. Options-based positioning (skew, risk reversal) would be the volatility-market complement — it ties directly to the FX-options gap in bibliography cluster 1 (Garman-Kohlhagen and the options/risk-reversal primer), so the data gap and the literature gap here are the same gap seen from two sides.

| What we have | Table | Series | Coverage |
|---|---|---|---|
| Open interest, net/long/short positioning of "leveraged money" and non-reportables | `macro_international.cmb_cot_fx` | `open_interest`, `lev_long`, `lev_short`, `lev_net`, `nonrept_long`, `nonrept_short` | BRL and MXN, weekly (Tuesdays), 2010 → today |

Script: `domain/db/international/cftc/cmb_cot_fx.py`. Source: CFTC Traders in Financial Futures.

**Gaps:**
- CLP and COP have no CME futures — they don't appear in the TFF report, and there's no equivalent alternative data today.
- History not available before 2010 (CFTC returns 404 for 2006–2009).
- No options-based positioning data (skew, risk reversal) — see the corresponding gap in the bibliography (`exchange_rate_bibliography_gaps.md`, section 4, FX options and volatility).

---

## 9. Inflation differential and market expectations

**Why it matters:** IPCA and US CPI are the two legs needed to turn the nominal Selic–Fed Funds spread into a real one (§2). Focus is the forward-looking domestic input the ex-ante differential needs, and the raw material for any credibility/anchoring argument (Verde's §1.7).

| What we have | Table | Note |
|---|---|---|
| IPCA (28 series, incl. cores) | `macro_brasil.inflc_agregados` | 1980 → today |
| Focus expectations — IPCA 12m/24m, IGP-M, Selic | `macro_brasil.expc_focus` | 2001 → today |
| US CPI (via FRED, consumed inside the differentials calculation) | `macro_international.diferenciais_juros` (`cpi_12m_us`) | ~36m rolling |

Scripts: `domain/db/brasil/bcb/inflc_agregados.py`, `domain/db/brasil/bcb/expc_focus.py`.

**Use for FX analysis:** `expc_focus` is already ready to feed the pending ex-ante differentials (item 2 above) — Focus Selic EOP 12m and Focus IPCA 12m are already available; only the script combining them with the US side is missing.

---

## 10. Domestic activity backdrop (context, not FX-specific)

**Not an FX category, kept as context.** The presentation-layer copy merged in here dropped this section outright, on the grounds that it is general macro backdrop rather than FX-specific data — a fair call for a reading audience, but the series are worth keeping listed for the agent. General `macro_brasil` series that help contextualize the domestic cycle (relevant for carry/country risk, but not "FX data" per se): `atv_ibcbr` (monthly GDP proxy), `atv_pib`, `atv_pim` (industrial production), `atv_pmc`/`atv_pms` (retail/services), `mt_pnad` (labor market), `mt_caged`, `cred_credito_amplo`, `cred_credito_familias`. Full table in `CLAUDE.md`.

On the US side, activity/inflation data today only exists ad hoc inside `analytics/oraculo/us/term_us.py` (via FRED) — there's no persistent `macro_us` schema equivalent to `macro_brasil` (already logged as a pending item in `CLAUDE.md`, "Média prioridade — US expandir dados").

---

## Gap summary (suggested priority)

| Priority | Gap | Category |
|---|---|---|
| High | Ex-ante interest rate differentials (Focus × Fed Funds futures/OIS) | §2 |
| Medium | CEP/CBE granularity of the financial FX flow | §5a |
| Medium | Wire `cmb_ptax` into the analysis agent's snapshot (`agent_data.py`) | §1 |
| Low | Cupom cambial + B3 futures (requires Bloomberg access) | §2 |
| Low | REER/COT for EM peers beyond BR/MX/CL/CO | §7, §8 |
| Low | Options-based positioning data (skew, risk reversal) | §8 |
| Low | Persistent `macro_us` schema (today only ad hoc FRED in the oráculo) | §10 |

---

## How to update this inventory

When creating a new table in `macro_brasil`/`macro_international` that's relevant to FX analysis, add a row to the corresponding section (or create a new section, if it's an analytical category not yet covered) and remove/update the corresponding gap in the summary table above.
