# analytics/inflation/ — Panorama de Inflação

IPCA/IPCA-15 decomposition report: self-contained HTML that reads MySQL (`macro_brasil`) plus one local CSV. Same `/*REPORT_DATA*/` template + `str.replace()` pattern as `analytics/exchange_rate/` and `analytics/monetary_policy/` — no Jinja2.

## Generate the report

```powershell
uv run python analytics/inflation/fetch_bcb.py               # refresh data/ipca_bcb_series.csv — NOT scheduled, run manually
uv run python -c "from analytics.inflation.generate_report import run; run()"
# Output: reports/inflation_latest.html (self-contained, ~14 MB — the ~57k
# decomposition records embedded as inline JSON are the bulk of it)
```

`inflc_decomposicao`/`inflc_dim` (MySQL) are already refreshed by `jobs/update_db.py` — only the BCB/SGS aggregates CSV needs the manual `fetch_bcb.py` step above.

## Architecture

`generate_report.py` reads two sources and substitutes `/*REPORT_DATA*/` in `report.html` with a plain `str.replace()` — no templating engine:

- `_load_decomposicao()`: pulls `inflc_decomposicao` (facts) and `inflc_dim` (dimension) via `MySQLDataRequester`, joins them in pandas (`merge` on `subitem`) — not in SQL.
- `_load_bcb()`: reads `data/ipca_bcb_series.csv`; returns `{}` if the file is missing rather than raising — the report just skips BCB-sourced charts.

## Report structure (`report.html`)

Three tabs, driven entirely by the JSON payload above (no server, no build step):

- **Decomposição** — drilldown by Grupo/Subgrupo/Item/Subitem, monthly contribution stacked bars (`barmode:'relative'`, not `'stack'`, so negative-contribution categories render below zero correctly).
- **Núcleos & Difusão** — núcleo glossary, a núcleo-picker dropdown (3M SAAR + 12M side by side), and difusão-by-category using the official `nucleo_*` flags (not an approximation from grupo/subgrupo). Hidden entirely for IPCA-15 (see Gotchas).
- **Mapa de Calor** — heatmap of 3M SAAR for Grupos + Núcleos, last 12 months. Each series is z-scored against its own 60-month rolling mean/std (not a shared threshold) — same method as the FRED Blog inflation heatmap, chosen because BCB has no published equivalent to replicate.

## Data map

| Source | Content | Script | Refresh |
|---|---|---|---|
| MySQL `inflc_decomposicao` | IPCA/IPCA-15 by subitem: var_mensal/pesos/contribuicao (IBGE agregados 7060/7062); subitem IDs resolved dynamically via `listar_classificacoes()`, not hardcoded | `domain/db/brasil/ibge/inflc_decomposicao.py` | `jobs/update_db.py` |
| MySQL `inflc_dim` | subitem → grupo/subgrupo/item/subjacente + 7 núcleo membership flags (dimension table, no time axis) | `domain/db/brasil/ibge/inflc_dim.py` | `jobs/update_db.py` (idempotent — reflects the xlsx files every run) |
| `data/ipca_bcb_series.csv` | BCB/SGS aggregates (headline, components, núcleos) + STL `_ma3_sa` variants | `fetch_bcb.py` | manual only |
| `data/tabela_dimensao_ipca.xlsx` (gitignored) | manually maintained grupo/subgrupo/item + "Alimentos Subjacente" | read by `inflc_dim.py` | edit xlsx, then `inflc_dim.run()` |
| `data/Vetores_NT_57.xlsx` (gitignored) | BCB's official aggregation vector (Nota Técnica nº 57) — source of núcleo flags + Serviços/Industriais Subjacente | read by `inflc_dim.py` | replace file if BCB republishes the NT |

`inflc_agregados` documents its own 33 SGS series natively — `SHOW CREATE TABLE inflc_agregados` (or the Workbench column editor) lists every series+code without needing to open any Python.

`referencia/` holds context PDFs nothing reads: `Nucleos_inflacao.pdf` (the NT-57 itself) and `inflacao_servico.pdf` (services-reweighting box, see Pending).

## Gotchas

- **IPCA and IPCA-15 use different IBGE variable IDs inside the same classification.** Aggregate 7060 (IPCA): var_mensal=63, pesos=66. Aggregate 7062 (IPCA-15): var_mensal=355, pesos=357. Requesting the wrong variable ID for the wrong aggregate does not 404 — IBGE returns HTTP 500 (their bug), which reads like an oversized-payload error rather than an invalid-ID one. Confirm via `ibge.metadados(agregado).variaveis` before touching this.

- **`inflc_dim` is two sources stitched together, and one wins on conflict.** grupo/subgrupo/item + "Alimentos Subjacente" come from the manual `tabela_dimensao_ipca.xlsx`. `subjacente` (Serviços/Bens Industriais) and all 7 `nucleo_*` flags come from `Vetores_NT_57.xlsx` (BCB official) and take precedence whenever the two disagree, per explicit user instruction ("follow the official dimension"). Editing Serviços/Industriais Subjacente in the xlsx has no effect — it is overwritten by `_apply_official_subjacente()`. "Alimentos Subjacente" has no official counterpart and stays xlsx-only.

- **BCB/SGS aggregates live in two places that are NOT kept in sync automatically.** `data/ipca_bcb_series.csv` (`fetch_bcb.py`, uppercase names like `IPCA_nucleo_P55`) duplicates most of `macro_brasil.inflc_agregados` (lowercase, `ipca_nucleo_p55`). `fetch_bcb.py` carries one series with no DB counterpart (`IPCA_12m`, SGS 13522, used for the "12 Meses" KPI cross-check below). No migration is scheduled — adding a series to one does not update the other.

- **`fetch_bcb.py` has no scheduled run** — it is not in `jobs/update_db.py`. It has gone silently stale for a full month before with no visible error.

- **Núcleos do not exist for IPCA-15.** BCB only publishes núcleo series (EX-0/EX-01/…/P55/MA/MS/DP) for the full IPCA; `inflc_agregados`/`fetch_bcb.py` only carry the IPCA-15 headline (SGS 7478). Do not wire new núcleo charts to IPCA-15 series that do not exist upstream.

- **"12 Meses" KPI uses a 3-tier fallback**, in `report.html` JS: official BCB series (`IPCA_12m`/SGS 13522, IPCA only) → chaining the official monthly series (`computeYoY`, covers IPCA-15 too) → reconstruction from subitem data (`computeIpca`, last resort only). "IPCA Acumulado" reuses the same value when the selected window is exactly the last 12 months, so the two KPIs never disagree on the same window.

- **No 12-month variation stored in `inflc_decomposicao`** — deliberate: compute YoY/accumulated from `var_mensal` at the consumption layer instead of keeping a second source of truth in the DB.

- **STL ordering is deliberate**: `_apply_stl_ma3()` (`fetch_bcb.py`) seasonally adjusts the raw monthly series first, then takes MA(3) — not the reverse — matching BLS/X-13 convention. STL (not X-13ARIMA-SEATS) is used on purpose: X-13 needs a separate Census Bureau binary per machine, which would break `uv sync` reproducibility.

- **`pesos`/`contribuicao` round looser than `var_mensal`** in `_to_records()` (8 decimals vs. 5) — rounding low-weight subitems (~3e-6, e.g. "Fisioterapeuta") to 5 decimals zeroes them out, and the front-end's weighted-average chart divides by that weight, so it renders empty for those subitems.

- **"Média 5 Núcleos (BCB)" is a specific subset, not all núcleos**: EX-0, EX-03, Médias Aparadas (smoothed), Dupla Ponderação and P55 only — deliberately excludes EX-01/EX-02/EX-FE, mirroring how BCB itself summarizes núcleos (Estudo Especial 102).

## Pending

### High priority

- Migrate `fetch_bcb.py` to read from `macro_brasil.inflc_agregados` instead of re-fetching BCB/SGS directly — would also fix the uppercase/lowercase naming mismatch.

- Add `fetch_bcb.py` to `jobs/update_db.py` (or equivalent) so the CSV cannot silently go stale again.

- Núcleos for IPCA-15: not published by BCB, would need to be computed in-house from `inflc_decomposicao`/`inflc_dim` via NT-57's exclusion methodology — feasible for EX-0/EX-01/EX-02/EX-03/EX-FE; MA/MS/DP/P55 would require replicating the full statistical methodology (trimming, double-weighting, percentile).

- Heat map by monthly variation (not 3M SAAR) with a selectable level (Grupo/Subgrupo/Item/Subitem) — today's "Mapa de Calor" tab only covers a fixed set of Grupo/núcleo rows.

- Extend `inflc_decomposicao`/`inflc_dim` before 2020 — `Vetores_NT_57.xlsx` has one sheet per IPCA structural vintage back to jan/1991, so the official classification already exists; only the IBGE fetch (`inflc_decomposicao.py`) is scoped to the structure in force since jan/2020.

- Subitem-level decomposition *within* a núcleo (not just within the full IPCA) — `nucleo_*` flags already give membership; needs weight renormalization + núcleo-specific contribution logic.

- Aggregates computed directly from the IBGE decomposition, not just BCB/SGS — would allow decomposing núcleos/aggregates that BCB itself does not publish a breakdown for.

### Medium priority

- Report is ~14 MB; consider paginating or compressing the inline JSON if email delivery becomes a problem.

- 12-month contribution view per subitem — deferred; if needed, compute by chaining `var_mensal` in `generate_report.py` rather than reintroducing a `var_12m` column in the DB.

- Services-inflation reweighting by production factor (`referencia/inflacao_servico.pdf`, BCB RI jun/2024 box) — not started; needs TRU/IBGE factor weights mapped to IPCA subitems.
