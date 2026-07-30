# Verde Asset — how to download the monthly letters (`raw_pdf/`)

Process for pulling Verde Asset Management's monthly "Relatório de Gestão" PDFs
(the flagship multimercado fund, VERDE FIF CIC MULTIMERCADO RL) straight from
their website into `repository/mental_model/verde_asset/raw_pdf/`. Read this
before running another year — it saves re-discovering the URL pattern from
scratch each session.

## The URL pattern

```
https://www.verdeasset.com.br/public/files/rel_gestao/158094/Verde-REL-{YYYY}_{MM}.pdf
```

- `158094` is the **fund's permanent site ID**, not a per-file ID — it never
  changes across years/months. Only `{YYYY}_{MM}` varies (`{MM}` zero-padded,
  `01`-`12`).
- Filename prefix is always `Verde-REL-` for this fund. (Other Verde funds use
  different prefixes under their own ID — e.g. `Acoes-REL-`, `Icatu-Prev-REL-`
  — see "Other Verde funds" below if that's ever needed.)

## The authoritative list of what actually exists

Don't just guess 01–12 and treat 404s as "missing" — the site publishes its
own index, which is the real source of truth (and is what caught the genuine
historical gaps below):

```
https://www.verdeasset.com.br/public/fundos/data/relatorios/158094.json
```

Returns every published month as `{"ano": YYYY, "mes": M, "url": "/public/files/..."}`.
Fetch it once per session and grep it instead of re-deriving anything:

```bash
curl -s "https://www.verdeasset.com.br/public/fundos/data/relatorios/158094.json" -o /tmp/relatorios_158094.json
grep -B2 -A2 '"ano": 2019' /tmp/relatorios_158094.json     # months for one year
grep -o '"ano": [0-9]*' /tmp/relatorios_158094.json | sort -u   # full year range
```

As of 2026-07, the index covers **1998 through the current month**. 1998 has
not been downloaded yet (only 1999 onward has been pulled so far).

**Known real gaps** (months genuinely never published, confirmed via this
index — not download failures):
- 1999: missing 04, 10, 11
- 2000: missing 02, 04, 11
- 2001: missing 05
- 2003: missing 04

Every year 2004–2026 has the full 12 months.

## How this endpoint was found (in case a similar site needs the same trick)

The site (`verdeasset.com.br`) is a single-page app on the "Infront" CMS —
static HTML shell, content loaded by JS. Standard scraping of the rendered
HTML finds nothing. The path that worked:

1. Fetch site root → find it loads `js/core.js`, `js/router.js`, `js/site.js`.
2. `core.js` shows the general data-loading convention: `base_uri + '/public/data/' + jsonFile + '.json'`.
3. `router.js` maps page routes (e.g. `/performance`) to template files under `tpl/`.
4. Fetch `tpl/performance.html` (the funds/performance page) → it references
   `/public/fundos/data/lista_preview.json` (list of all funds, each with a
   numeric `id`) and `/public/fundos/data/relatorios/{id}.json` (full report
   archive for that fund).
5. Confirmed `id: 158094` in `lista_preview.json` is `"nome": "VERDE FIF CIC
   MULTIMERCADO RL"` — the fund these letters are for.

If Verde changes their CMS, or another manager's site needs the same
treatment, repeat this: look for a `public/data/*.json`-style API before
falling back to HTML scraping.

## Download procedure

One year at a time (a 5-year loop of `curl` calls has hit the Bash tool's
2-minute timeout partway through — keep batches to 1–3 years per call):

```bash
mkdir -p "repository/mental_model/verde_asset/raw_pdf"
for m in 01 02 03 04 05 06 07 08 09 10 11 12; do
  url="https://www.verdeasset.com.br/public/files/rel_gestao/158094/Verde-REL-${YEAR}_${m}.pdf"
  out="repository/mental_model/verde_asset/raw_pdf/Verde-REL-${YEAR}_${m}.pdf"
  code=$(curl -s -o "$out" -w "%{http_code}" --max-time 30 "$url")
  size=$(wc -c < "$out" 2>/dev/null)
  echo "${YEAR}_${m}: HTTP $code, size $size bytes"
done
```

Skip months the JSON index says don't exist for that year.

### Gotcha: transient failures, not real 404s

A meaningful fraction of calls fail with `No such file or directory` on the
`-o` path or `HTTP 000` — this is **not** a filesystem/permissions problem
and not a real 404. `curl -v` traces show the actual cause is a transient DNS
resolution failure (`Could not resolve host: www.verdeasset.com.br`),
presumably rate-limiting or flakiness on the CDN/DNS side. It clears up on
retry essentially every time.

**Always check the HTTP code, never assume a failed curl call means the file
is missing.** After each batch, retry every non-200 result (up to ~3
attempts each) before concluding a month is genuinely absent — cross-check
against the JSON index either way.

## After download: text extraction

This doc only covers acquiring `raw_pdf/`. Turning them into `raw_md/` follows
the general PDF routing rule in the root `CLAUDE.md` ("Extração de PDFs para
bibliography"): these are born-digital, single-column PDFs, so use
`utils/extract_pdf.py` (pdfplumber) — zero token cost — the same way the
2020+ letters already in `raw_md/` were produced. `clean_md/` (currently only
`Verde-REL-2026_05.md`) is a further hand/agent-cleaned step on top of that,
not something to reproduce automatically for every month.

## Other Verde funds (not yet pulled)

`lista_preview.json` (`https://www.verdeasset.com.br/public/fundos/data/lista_preview.json`)
lists every Verde fund with its own `id` and current `report_mes` path — the
same `{id}.json` / `relatorios/{id}.json` pattern applies to any of them if
their letters are ever needed (e.g. `118` = Ações, `162853` = Icatu Prev,
`350132`/`350136` = Mundi Ações Globais). Not in scope for this folder so far
— only the flagship multimercado fund (`158094`) has been collected.
