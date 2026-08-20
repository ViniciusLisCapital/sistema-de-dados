# Handover — 2026-08-13

Scope: full conversation. Task (Novo CAGED/MTE-PDET FTP connector, from the previous
session's HANDOVER.md) is **complete and validated**. This note exists mainly so a
future session knows the state and doesn't re-derive or re-run anything.

## Goal

Build a primary-source (not distributor) pipeline for Brazil's Novo CAGED labor-market
microdata — saldo/admissões/desligamentos by setor, UF, and salary band — sourced
directly from the MTE/PDET FTP, minimizing bandwidth via a shared downloader, then
backfill full history (2020-01→2026-06) into `macro_brasil`.

## Instructions and constraints given (explicit, this session)

- Do NOT save the FTP investigation facts to memory ("Não salvar").
- Include faixa salarial in scope from the start, alongside setor and UF.
- Use **independent cuts** (3 separate national series), NOT a crossed
  setor×UF×faixa grid.
- User wanted the network/disk cost explained precisely before approving — asked for
  it twice, once quantitatively ("Brasil-only, sem UF, como fica a conta?"), once as a
  plain-English/"10yo kid" framing of the *ongoing* monthly update cost, not just the
  one-time backfill. Approved after that: "Sim, construir o orquestrador e fazer o
  backfill de 4GB."
- User asked me to research whether an easier extraction method exists before
  building the FTP approach — researched (legacy CAGED gated, BCB/IPEA distributor
  gaps, Base dos Dados as an imperfect alternative) and confirmed FTP+manual
  MOV/FOR/EXC combination is genuinely how this is done; no shortcut exists.

## Conventions and decisions established

- Shared orchestrator (`mt_caged_novo.py`) downloads each FTP release exactly once,
  feeding all 3 cut tables in one pass — cut backfill cost from ~12GB to ~4GB.
- `_caged_core.py`'s `processar()` is a two-phase generator (read all FOR/EXC
  corrections first, then MOV release-by-release, yielding one competência at a time)
  so partial progress is never lost and re-runs are idempotent
  (`ON DUPLICATE KEY UPDATE`).
- PK convention for the 3 new tables: `PRIMARY KEY (date, categoria, metrica)`,
  `date` = competência de MOVIMENTAÇÃO (not declaração/release).
- Validated formula: `saldo(X) = MOV(X) + FOR(X) - EXC(X)`, EXC keeps original sign.

## Work completed

- `connectors/pdet_ftp.py` — FTP client (`ftplib.FTP(..., encoding="latin-1")`),
  listing + `.7z` download + extraction helpers.
- `domain/db/brasil/mte/_caged_core.py` — combination/aggregation logic, decimal
  normalizer (`_normalizar_salario`, handles 2023-08/09's dot-decimal quirk), the
  two-phase generator `processar()`.
- `domain/db/brasil/mte/mt_caged_setor.py`, `mt_caged_uf.py`, `mt_caged_salario.py` —
  one `categoria(df)` function + `run()` each.
- `domain/db/brasil/mte/mt_caged_novo.py` — orchestrator, single shared download.
- `domain/db/brasil/mte/__init__.py`.
- 3 MySQL tables created in `macro_brasil`: `mt_caged_setor` (VARCHAR(60) categoria,
  widened after a real overflow), `mt_caged_uf` (VARCHAR(5)), `mt_caged_salario`
  (VARCHAR(20)). All TRUNCATEd once mid-session to clear this session's own test
  debris right before the real backfill's write phase.
- `pyproject.toml` — `py7zr` added via `uv add`.
- `jobs/update_db.py` — `mt_caged_novo` wired in, placed last (slower than the rest).
- Docs updated: `connectors/CLAUDE.md` (new `pdet_ftp.py` section, all 3 source
  quirks), `domain/db/CLAUDE.md` (3 new active tables + PK pattern note), root
  `CLAUDE.md` (tree entries + new "Mercado de trabalho — pendências pós-Novo CAGED"
  item), `analytics/brasil/labor_market/fontes_dados.md` (coverage table flipped to ✅,
  new "Novo CAGED" explainer section).
- **Backfill run and validated**: `mt_caged_novo.run(start="all")` completed exit 0.

## Current state

- All 3 tables: 78/78 months, 2020-01→2026-06, no gaps.
- Row counts: `mt_caged_setor`=5103, `mt_caged_uf`=6552, `mt_caged_salario`=2574.
- Cross-check query (sum of `saldo` per month across the 3 independent cuts) returned
  **0 divergent months** — strongest available correctness signal.
- June/2026 saldo reproduced exactly (145,161) against an independently-known figure.
- Result already reported to the user in chat; no open questions from them.

## Open items / next steps

None requested by the user. Documented-but-not-requested future work (do NOT start
without explicit ask, per root `CLAUDE.md`'s "Mercado de trabalho — pendências
pós-Novo CAGED"):
- `domain/db/brasil/bcb/mt_caged.py` still mislabels estoque as "saldo".
- Unmapped cuts available in the same microdado but not modeled: município, ocupação
  (CBO), sexo/idade/instrução/raça.
- `mt_pnad_trimestral` UF/N3 level still out of scope (pre-existing, unrelated).
- No report/dashboard consumes the 3 new tables yet — no `analytics/brasil/labor_market/`
  report project exists, just the `fontes_dados.md` inventory.

## Files to read first

- `domain/db/brasil/mte/_caged_core.py` — the core logic, has a long docstring
  explaining the MOV/FOR/EXC formula and the two-phase generator design.
- `domain/db/brasil/mte/mt_caged_novo.py` — orchestrator entry point.
- `analytics/brasil/labor_market/fontes_dados.md` — coverage table + "Novo CAGED" explainer.
- `connectors/pdet_ftp.py` — FTP client, if touching the download layer.

## Gotchas

- `urllib.request` fails on accented FTP filenames (decodes percent-escapes as UTF-8,
  corrupting Latin-1 bytes) — must use `ftplib.FTP(..., encoding="latin-1")` directly.
- `py7zr` 1.1.3 has no in-memory read API — must `.extract()` to a temp dir.
- Not every release has all 3 file types: 2020-01 has MOV only, 2020-02/03 have
  MOV+FOR only (no EXC) — `listar_arquivos()` checks presence before downloading.
- Decimal separator in `salário` is inconsistent: comma normally, but dot in the
  2023-08 and 2023-09 releases specifically — `_normalizar_salario()` handles both.
- Windows path gotcha: git-bash POSIX paths (`/c/Users/...`) don't work with native
  Windows Python invoked via `uv run python` from the Bash tool — use
  `C:\Users\...`-style paths.
- Terminal codepage garbles accented characters in tool output (cosmetic only,
  underlying strings are correct) — don't build grep/Monitor patterns that rely on
  matching accented substrings; use ASCII-only patterns instead.

## Not yet saved to durable memory (flag for user sign-off)

Per this session's explicit instruction, none of the FTP/CAGED investigation facts
were saved to auto-memory — they're fully captured in the docstrings and CLAUDE.md
files listed above instead. Nothing else from this session looks like it needs a
memory save beyond what's already there.
