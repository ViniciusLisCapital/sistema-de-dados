"""
Curate Kapitalo K10 letters: raw_md/*.md (permanent, unedited) -> clean_md/*.md
(curated per CURATION_SCOPE.md).

Applies uniformly across both format eras (see CURATION_SCOPE.md):
- Era 1 "Carta K10" (Jul/2019-Aug/2023): VaR chart bar values and the
  Atribuicao de Performance table are INTERLEAVED line-by-line in the raw
  pdfplumber extraction (two page columns merged). A strategy-label row can
  even have stray VaR numbers prefixed on the same line before the label
  (e.g. "0,17% 0,49% Performance do Fundo 2,68% ..."). This script finds the
  label anywhere in the line and keeps only the label onward.
- Era 2 "CARTA DO GESTOR" (Sep/2023-present, already hand-corrected in
  raw_md/): VaR chart is its own clean "Label: max/med/min" section (all
  dropped, no percent-bearing label row can survive there because Section
  scoping never applies label-search to it -- see below) and the Atribuicao
  table is a clean header + one-row-per-line block.

Core rule enforced: within the Alocacao/Atribuicao zone, a candidate line is
only kept as a real data row if the label match is followed by an actual
percent value on the same line -- a bare axis-label line like "Commodities
Moedas Bolsa Renda Fixa Total" (era 1's chart x-axis, no percent signs)
would otherwise collide with the "Commodities" strategy-row label. The
"Estrategias"/"ESTRATEGIAS" header line is special-cased (kept whenever
found, since it never carries a percent sign itself).

Cross-validation safety gate: Performance do Fundo's first (monthly) column
must equal CDI + sum(Juros, Moedas, Bolsa, Commodities, Caixa e Custos) for
that same column, within a small rounding tolerance. A file that fails this
gets its clean_md written with a visible warning instead of being silently
trusted -- never guess a value that doesn't reconcile.
"""
import re
import sys
import unicodedata
from pathlib import Path

CORPUS_DIR = Path(__file__).parent
RAW_MD_DIR = CORPUS_DIR / "raw_md"
CLEAN_MD_DIR = CORPUS_DIR / "clean_md"

ALOCACAO_MARKERS = ["alocação por fator de risco"]
# Mar/2025-onward template splits "ALOCAÇÃO" / "POR FATOR DE RISCO" across two
# lines (sometimes with a stray VaR number glued onto either line), so the
# literal-phrase markers above never match from that point on. This regex
# tolerates arbitrary whitespace/newlines/digits between the two words.
ALOCACAO_MARKER_RE = re.compile(r"aloca[cç][aã]o\s*[\d.,%\s]*\s*por\s+fator\s+de\s+risco", re.I)
ATRIBUICAO_HEADER_MARKERS = ["atribuição de performance"]
# Same split-header issue for "ATRIBUIÇÃO" / "DE PERFORMANCE" in that same
# template -- used only for era-2 standalone-header detection (see below).
ATRIBUICAO_HEADER_RE = re.compile(r"atribui[cç][aã]o\s*[\d.,%\s]*\s*de\s+performance", re.I)
ESTRATEGIAS_MARKERS = ["estratégias", "estrategias"]
FOOTNOTE_MARKER = "mínimo, médio e máximo"

DISCLAIMER_ANCHORS = [
    "este conteúdo foi preparado",
    "este conteúdo foi elaborado",
    "esse documento foi elaborado",
    "a kapitalo ciclo não comercializa",
]

# Order matters: check longer/more specific labels before short ones that
# could match as a substring of them. "% CDI" uses a negative lookbehind so
# it never accidentally matches a stray, unrelated VaR-chart percent value
# that happens to sit right before a genuine plain "CDI" row on the same
# interleaved era-1 line (e.g. "0,21% CDI 0,57% ..." is the CDI row, NOT a
# "% CDI" row, even though a naive substring search for "% CDI" would have
# matched it -- confirmed as a real bug against kapitalo_k10_072019.md
# before this lookbehind was added).
ROW_LABEL_PATTERNS = [
    ("Performance do Fundo", re.compile(r"performance\s+do\s+fundo", re.I)),
    ("Caixa e Custos", re.compile(r"caixa\s+e\s+custos", re.I)),
    ("% CDI", re.compile(r"(?<![\d,])%\s*cdi\b", re.I)),
    ("Juros", re.compile(r"\bjuros\b", re.I)),
    ("Moedas", re.compile(r"\bmoedas\b", re.I)),
    ("Bolsa", re.compile(r"\bbolsa\b", re.I)),
    ("Commodities", re.compile(r"\bcommodities\b", re.I)),
    ("CDI", re.compile(r"\bcdi\b", re.I)),
]

PCT_RE = re.compile(r"-?\d+[.,]\d+%")


def strip_accents_lower(s):
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return s.lower()


def find_ci(text, needle, start=0):
    """Case-insensitive find on the ORIGINAL text (plain .lower(), not the
    accent-stripping helper above): .lower() never changes string length for
    this alphabet, so positions found this way stay valid for slicing `text`
    itself. NFKD accent-stripping DOES change length (decomposes then drops
    combining marks), which silently misaligned every index computed through
    it against the original string -- a real bug caught when a table-zone
    boundary computed from a stripped-text offset was used to slice the
    original text and landed hundreds of characters into the wrong place.
    Safe here because these marker phrases (Alocação, Atribuição, Mínimo...,
    the disclaimer openers) always appear correctly accented in this corpus."""
    return text.lower().find(needle.lower(), start)


def first_pct(rest_of_line):
    m = PCT_RE.search(rest_of_line)
    return m.group(0) if m else None


def to_float(pct):
    return float(pct.replace("%", "").replace(",", "."))


def merge_wrapped_performance_label(zone_lines):
    """Mar/2025-onward template wraps "Performance do Fundo"'s row across two
    lines -- a lone "Performance" line, then "do Fundo -0,05% ...% ..." on the
    next -- since the table cell itself got narrower in that template. Every
    ROW_LABEL_PATTERNS regex is deliberately single-line-only (avoids cross-
    line false matches in the noisy chart region above the table), so this
    row would otherwise never match. Join the two lines back into one
    wherever this exact wrap shape occurs; every other line is untouched."""
    merged = []
    skip_next = False
    for i, line in enumerate(zone_lines):
        if skip_next:
            skip_next = False
            continue
        if line.strip() == "Performance" and i + 1 < len(zone_lines) and zone_lines[i + 1].strip().lower().startswith("do fundo"):
            merged.append(line.strip() + " " + zone_lines[i + 1].strip())
            skip_next = True
        else:
            merged.append(line)
    return merged


def extract_zone_rows(zone_lines):
    """Return (header_line_or_None, rows) where rows is a list of
    (matched_label, full_row_text) in the order encountered. Only lines
    whose matched-label remainder actually contains a percent sign are
    kept as data rows (excludes bare chart-axis label lines like
    "Commodities Moedas Bolsa Renda Fixa Total")."""
    header_line = None
    rows = []
    for line in merge_wrapped_performance_label(zone_lines):
        line_noaccent_lower = strip_accents_lower(line)
        is_header = any(m in line_noaccent_lower for m in ESTRATEGIAS_MARKERS)
        if is_header and header_line is None:
            header_line = line.strip()
            continue
        matched = None
        for label, pattern in ROW_LABEL_PATTERNS:
            m = pattern.search(line)
            if m:
                candidate = line[m.start():].strip()
                if "%" in candidate:
                    matched = (label, candidate)
                    break
        if matched:
            rows.append(matched)
    return header_line, rows


def cross_validate(rows, tolerance=0.06):
    """Compare Performance do Fundo's first column against CDI + sum of the
    five strategy rows' first column. Returns (ok, detail_message)."""
    firsts = {}
    for label, text in rows:
        key = strip_accents_lower(label).strip()
        if key in firsts:
            continue  # keep first occurrence only (monthly column's own row)
        pct = first_pct(text)
        if pct:
            firsts[key] = to_float(pct)

    required = ["juros", "moedas", "bolsa", "commodities", "caixa e custos", "cdi", "performance do fundo"]
    if not all(k in firsts for k in required):
        return False, "missing one or more required rows for cross-validation"

    strategy_sum = (
        firsts["juros"] + firsts["moedas"] + firsts["bolsa"]
        + firsts["commodities"] + firsts["caixa e custos"] + firsts["cdi"]
    )
    perf = firsts["performance do fundo"]
    diff = abs(strategy_sum - perf)
    ok = diff <= tolerance
    detail = (
        f"CDI+estrategias={strategy_sum:.2f} vs Performance do Fundo={perf:.2f} "
        f"(diff={diff:.2f}, tolerance={tolerance})"
    )
    return ok, detail


def process_file(raw_path: Path):
    text = raw_path.read_text(encoding="utf-8")
    lines = text.splitlines()

    aloc_idx = None
    for m in ALOCACAO_MARKERS:
        i = find_ci(text,m)
        if i != -1:
            aloc_idx = i
            break
    if aloc_idx is None:
        m = ALOCACAO_MARKER_RE.search(text)
        if m:
            aloc_idx = m.start()
    if aloc_idx is None:
        return {"file": raw_path.name, "error": "ALOCACAO marker not found"}

    disc_idx = None
    for m in DISCLAIMER_ANCHORS:
        i = find_ci(text,m, start=aloc_idx)
        if i != -1 and (disc_idx is None or i < disc_idx):
            disc_idx = i
    if disc_idx is None:
        return {"file": raw_path.name, "error": "disclaimer anchor not found"}

    body_text = text[:aloc_idx].rstrip()

    # Two distinct shapes for what sits between the Alocação marker and the
    # disclaimer:
    # - Era 2 (already hand-corrected raw_md/): a standalone "Atribuição de
    #   Performance" header exists; the table zone is that header up to the
    #   disclaimer, with nothing else in between.
    # - Era 1: the VaR chart and the table are one interleaved block with NO
    #   separate header, always closed by a "*Mínimo, Médio e Máximo..."
    #   footnote line. Some early letters (e.g. Jul/2019, the fund's first)
    #   have a long standalone essay AFTER that footnote and BEFORE the
    #   disclaimer -- bounding the table zone at the footnote (not at the
    #   disclaimer) keeps that essay out of the label-scan, where it would
    #   otherwise false-match ordinary prose ("...taxa de juros..." followed
    #   coincidentally by an unrelated "1.25%" later in the same sentence)
    #   as if it were a real performance row. Confirmed as a real bug
    #   against kapitalo_k10_072019.md before this bounding was added.
    # Era 1's own combined title is literally "Alocação por Fator de Risco*
    # Atribuição de Performance" -- BOTH markers on the SAME line. A naive
    # search for "atribuição de performance" starting at aloc_idx matches
    # that combined title immediately and wrongly looks like era 2's
    # standalone header, extending the table zone all the way to the
    # disclaimer and swallowing any essay in between (the real bug this
    # module's docstring already describes -- caught by inspecting
    # kapitalo_k10_072019.md's actual output, not just reasoning about it).
    # Require the match to be on a DIFFERENT line from the Alocação marker
    # to count as era 2's real standalone header.
    # Mar/2025-onward template: the "*Mínimo, Médio e Máximo..." footnote sits
    # right after the ALOCAÇÃO/POR FATOR DE RISCO title, BEFORE the chart bars
    # even start, not right before the table like every older era-1 letter.
    # Bounding the zone at that footnote (the era-1 fallback below) would cut
    # off the chart+table that follows it entirely. This template instead has
    # its own real standalone "ATRIBUIÇÃO / DE PERFORMANCE" header (split
    # across two lines, same reason ALOCACAO_MARKER_RE exists) sitting right
    # after the chart's own axis-label line -- closer to era 2's clean shape
    # than era 1's interleaved one. Try the regex form first; it also matches
    # era 1's literal single-line phrase, so it doesn't need a separate path.
    atrib_idx = None
    for m in ATRIBUICAO_HEADER_MARKERS:
        i = find_ci(text,m, start=aloc_idx)
        if i != -1 and i < disc_idx and "\n" in text[aloc_idx:i]:
            atrib_idx = i
            break
    if atrib_idx is None:
        m = ATRIBUICAO_HEADER_RE.search(text, aloc_idx)
        if m and m.start() < disc_idx and "\n" in text[aloc_idx:m.start()]:
            atrib_idx = m.start()

    essay_text = None
    if atrib_idx is not None:
        table_zone_start, table_zone_end = atrib_idx, disc_idx
    else:
        foot_idx = find_ci(text,FOOTNOTE_MARKER, start=aloc_idx)
        if foot_idx != -1 and foot_idx < disc_idx:
            line_end = text.find("\n", foot_idx)
            table_zone_end = line_end if line_end != -1 else disc_idx
            tail = text[table_zone_end:disc_idx].strip()
            essay_text = tail if tail else None
        else:
            table_zone_end = disc_idx
        table_zone_start = aloc_idx

    zone_text = text[table_zone_start:table_zone_end]
    header_line, rows = extract_zone_rows(zone_text.splitlines())
    ok, detail = (False, "no rows extracted") if not rows else cross_validate(rows)

    title = lines[0].strip() if lines else raw_path.stem

    out = [body_text, "", "[Alocação por Fator de Risco — gráfico de VaR omitido: sem rótulo por barra confiável na extração, ver raw_md para o texto bruto.]", ""]
    out.append("ATRIBUIÇÃO DE PERFORMANCE")
    if header_line:
        out.append(header_line)
    for label, row_text in rows:
        out.append(row_text)
    if not ok:
        out.append("")
        out.append(f"> [Aviso: verificação cruzada da tabela de atribuição falhou ({detail}). Confira contra `raw_md/{raw_path.name}` antes de usar estes números.]")
    if essay_text:
        out.append("")
        out.append(essay_text)
    out.append("")
    out.append(f"**Fonte:** curadoria automática (`curate.py`) de `raw_md/{raw_path.name}` (extração bruta, auditoria) do PDF original em `raw_pdf/{raw_path.stem}.pdf`. Seção de disclaimer legal e (quando presente) características do fundo/histórico de retornos mensais omitidas por serem boilerplate administrativo/legal.")

    clean_text = "\n".join(out) + "\n"
    return {"file": raw_path.name, "title": title, "rows": len(rows), "validated": ok, "detail": detail, "text": clean_text}


def run(filenames):
    CLEAN_MD_DIR.mkdir(exist_ok=True)
    reports = []
    for name in filenames:
        raw_path = RAW_MD_DIR / name
        if not raw_path.exists():
            reports.append({"file": name, "error": "raw_md file not found"})
            continue
        result = process_file(raw_path)
        if "error" in result:
            reports.append(result)
            continue
        clean_path = CLEAN_MD_DIR / name
        clean_path.write_text(result["text"], encoding="utf-8")
        reports.append({k: v for k, v in result.items() if k != "text"})
    return reports


if __name__ == "__main__":
    names = sys.argv[1:]
    for r in run(names):
        print(r)
