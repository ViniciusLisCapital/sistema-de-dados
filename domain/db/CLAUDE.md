# domain/db/ — Context for Claude

ETL scripts that populate `macro_brasil` (`brasil/`) and `macro_international` (`international/`) on the MySQL server at `192.168.15.200` (credentials in `.env`, never hardcoded). See [`.claude/rules/domain-scripts.md`](../../.claude/rules/domain-scripts.md) for the shared `run()`-only script pattern.

## Schema criterion: domain/geography, not raw-vs-computed

A table's schema depends only on which countries' data it needs — never on whether it's raw or derived.

```
macro_brasil        — anything Brazil-specific (BCB, IBGE), raw or computed
macro_international — anything needing data from 2+ countries to exist or make sense
macro_us             — future: US-only data that isn't just an input to an international series
```

E.g. `inflc_decomposicao.contribuicao` (= `var_mensal × pesos`, computed) stays in `macro_brasil` because both inputs are Brazilian. `diferenciais_juros` stores raw `selic`/`fed_funds` alongside the computed differentials in `macro_international`, because it needs both countries to exist at all.

Signal raw vs. computed at the table/column level instead, via MySQL's native `COMMENT` (see `inflc_agregados`, `SHOW CREATE TABLE`) and/or a "Raw series" / "Derived series" docstring section (see `international/fred/diferenciais_juros.py`, `brasil/ibge/inflc_decomposicao.py`).

**A `macro_analytics`-style schema-per-computation-stage was tried and discontinued in 2026-07** — it never grew past one table (`diferenciais_juros`), which already qualified for `macro_international` under the rule above. Only reconsider a dedicated cross-domain schema if 2-3+ tables genuinely belong to no single domain (e.g. if `oraculo`'s CSV-based scores, which already mix BR+US in one file, ever migrate to MySQL) — don't recreate one preemptively for a single table.

## Naming convention: theme prefix, not schema/stage

Table names are prefixed by macro theme, independent of schema or computation stage — the prefix classifies what the data *is*.

`macro_brasil`:
```
atv_    — real activity (GDP, industrial production, retail, services, IBC-Br)
mt_     — labor market (PNAD, CAGED) — kept its unabbreviated prefix
cred_   — credit and household/corporate financial conditions
cmb_    — FX and its determinants (reserves, BOP, flow, terms of trade, contracted FX)
inflc_  — IPCA/IPCA-15 (aggregates, subitem decomposition, dimension table)
expc_   — market expectations (Focus)
```

`macro_international`:
```
cmb_    — FX: cmb_reer, cmb_cot_fx
(none)  — diferenciais_juros: the one table in this schema with no prefix,
           by explicit user instruction — not "cmb_diferenciais_juros"
```

`diferenciais_juros` is deliberately unprefixed despite being FX/rate-themed — don't add `cmb_` to it in a future cleanup without reconfirming. A table only gets a prefix if the theme helps group it visually among others in the same schema.

Renaming a table never touches its columns/data — only `RENAME TABLE` plus updating the script/file name and every consumer to match.

## Active tables (`macro_brasil`)

| Table | Source | Available range | Script |
|---|---|---|---|
| `atv_pim` | IBGE 8888 | 2002 → today | `brasil/ibge/atv_pim.py` |
| `atv_pib` | IBGE 1620/1621 | 2016 → today | `brasil/ibge/atv_pib.py` |
| `atv_pmc` | IBGE 8880/8881/8883 | 2023 → today | `brasil/ibge/atv_pmc.py` |
| `atv_pms` | IBGE 8688 | 2023 → today | `brasil/ibge/atv_pms.py` |
| `atv_ibcbr` | BCB SGS (12 series) | 2003 → today | `brasil/bcb/atv_ibcbr.py` |
| `mt_pnad` | IBGE 6318/6320/6323/6387/6388/6389/6391/6392 | 2024 → today | `brasil/ibge/mt_pnad.py` |
| `mt_caged` | BCB SGS (14 series) | 1992 → today | `brasil/bcb/mt_caged.py` |
| `cred_credito_amplo` | BCB SGS (17 series) | 2013 → today | `brasil/bcb/cred_credito_amplo.py` |
| `cred_credito_familias` | BCB SGS (3 series — household debt/income) | 2005 → today | `brasil/bcb/cred_credito_familias.py` |
| `inflc_agregados` | BCB SGS (33 series — IPCA/IPCA-15 + cores) | 1980 → today | `brasil/bcb/inflc_agregados.py` |
| `inflc_decomposicao` | IBGE 7060/7062 (subitem: monthly var/weights/contribution) | 2020 → today | `brasil/ibge/inflc_decomposicao.py` |
| `inflc_dim` | Subitem → Group/Subgroup/Item (manual) + core-inflation flag (hybrid, see `analytics/inflation/CLAUDE.md`) | — (no date) | `brasil/ibge/inflc_dim.py` |
| `expc_focus` | BCB Focus (IPCA 12m/24m, IGP-M, Selic) | 2001 → today | `brasil/bcb/expc_focus.py` |
| `atv_pib_usd` | BCB SGS 4385 (monthly GDP in USD) | — → today | `brasil/bcb/atv_pib_usd.py` |
| `comm_icbr` | BCB SGS 27574-27577 (IC-Br + 3 sub-indices) | 1998-02 → today | `brasil/bcb/comm_icbr.py` |
| `inflc_meta` | BCB SGS 13521 (CMN inflation target) | 1999 → today | `brasil/bcb/inflc_meta.py` |
| `cmb_risco_pais` | investing.com (manual CSV export, Brazil 5Y CDS USD) | 2007-12 → today (gap: 2015-12-02→2015-12-31, real gap in source exports) | `brasil/investing/cmb_risco_pais.py` |

`cmb_*` FX tables in `macro_brasil` (reserves, BOP, flow, terms of trade, contracted FX, Comex breakdowns) plus `macro_international`'s `cmb_reer`/`cmb_cot_fx`/`diferenciais_juros` are documented in [`analytics/exchange_rate/CLAUDE.md`](../../analytics/exchange_rate/CLAUDE.md) instead, since that's where they're actually consumed.

`inflc_agregados` has native MySQL documentation: `COMMENT` on the table and on the `name` column (lists every series with its SGS code) — see `SHOW CREATE TABLE inflc_agregados` or the Workbench table editor.

## Primary key patterns

All tables use a natural composite key (no synthetic `id`):

```sql
-- Seasonally adjusted series
PRIMARY KEY (date, name, seasonal_adjs)   -- atv_pim, atv_pib, atv_pmc, atv_pms

-- Not seasonally adjusted
PRIMARY KEY (date, name)                  -- inflc_agregados, mt_caged, cred_credito_amplo, atv_ibcbr, cred_credito_familias
PRIMARY KEY (date, name, region)          -- mt_pnad

-- Focus expectations
PRIMARY KEY (date, indicador, horizonte)  -- expc_focus

-- IPCA by subitem
PRIMARY KEY (date, indice, subitem)       -- inflc_decomposicao (indice = IPCA | IPCA15)
PRIMARY KEY (subitem)                     -- inflc_dim (dimension table, no date)
```

`ON DUPLICATE KEY UPDATE` on insert makes it an idempotent upsert.
