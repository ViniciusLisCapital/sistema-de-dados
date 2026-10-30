"""
The knowledge to-do: repository/agent_mapping/data_tracker.xlsx, one "Qual - <Area>" tab per
agent area (the curated literature lists), plus the managers' letters and the Copom documents,
kept in step with what is on disk.

Called by run.py after every write (letters included), by `mental.py done`, by the Copom ETL
(domain/db/brasil/bcb/_copom_texto.py), and runnable on its own:

    uv run python repository/ingestion/scripts/tracker.py
    uv run python repository/ingestion/scripts/tracker.py --file <copy.xlsx>   # a copy, not the real one

What it writes, and only this:
  - columns M-S of every "Qual - <Area>" tab (File, Ingestion, Ingested on, Extraction,
    QC flags, Synthesis, Ingestion note), cleared and rewritten on each run, with a navy
    header so they read as the system's columns next to the user's teal ones;
  - the headers of the layer columns right after I (LAYER_HEADERS: "Dono", "Camada",
    "Fila" in J-L): the agent that owns each source, its layer in the owner's library and its
    place in the promotion queue (SISTEMA_AGENTES I.III.xvii, PLANO_AGENTES.md I). The
    values are the user's, as A-I are. A tab in any other layout — the one before 2026-10-21,
    with the system's columns in J-P, or one with other layer columns — is migrated on the
    first run (_migrate): the layer values move by header name, the system's columns are
    cleared (they are rewritten anyway) and nothing in A-I moves;
  - "Do we have it?" = Yes on a row whose PDF is in repository/<topic>/raw_pdf/ (a row
    with no PDF keeps whatever the user wrote);
  - one row at the bottom of the tab for each PDF the curated list does not have, marked in
    Comments as added by ingestion (rebuilt on each run, so they never pile up; the user
    keeps one by filling A-I and deleting the mark). A Camada/Fila typed on such a row is
    carried over to its rebuilt row, by file name;
  - a "Literature summary" tab with the counts, as formulas;
  - a "Mental Models" tab, rebuilt from the folders: one line per document (area x manager:
    window, letters in it, letters read per ledger/, pending, last run), then one line per
    letter in the window. Camada and Fila of each document are the user's, kept by document
    name across rebuilds;
  - a "Copom" tab, rebuilt from obsidian/monetary_policy/clean_md/central_bank/: one line per
    kind (statement, minutes, RPM), then one per document, with its layer (copom_layer(), the
    same function the cycle's knowledge snapshot uses): layer 1 = everything published since the
    current governor's term began and before the cycle date.
Every other cell — the curated columns A-L, the Notes tab, the Quant tabs — is the user's.
The workbook is the single home of the literature and data lists (since 2026-10-19; the
.md lists were folded into it). The formatting follows its own: Calibri 11, top-aligned and
wrapped, thin grey borders, Yes/No fills.

A PDF is matched to a row by year plus author surnames, with the words of the file's
description against the row's title as the tie-break. A file that matches two rows equally
is appended with a note naming them, rather than guessed.

Facts come from the folders (raw_pdf/, raw_md/, clean_md/, synthesis/), settings.yaml and
LOG.md, never from memory. The .xlsx is in git (the one *.xlsx exception in .gitignore).
"""

import argparse
import datetime as dt
import math
import os
import re
import sys
import unicodedata
from pathlib import Path

import openpyxl
from openpyxl.comments import Comment
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

sys.path.insert(0, str(Path(__file__).resolve().parent))
from run import LOG, NAME_RE, OBSIDIAN, REPOSITORY, scan, topics  # noqa: E402

TRACKER = REPOSITORY / "agent_mapping" / "data_tracker.xlsx"
MM_DIR = REPOSITORY / "mental_model"
SUMMARY = "Literature summary"
TAB = {
    "exchange_rate": "Qual - Exchange Rate", "monetary_policy": "Qual - Monetary Policy",
    "economic_activity": "Qual - Economic Activity", "fiscal_policy": "Qual - Fiscal Policy",
    "inflation": "Qual - Inflation", "labor_market": "Qual - Labor Market", "trader": "Qual - Trader",
}
BASE_HEADERS = ["Name", "Autor/Company", "Date", "Importance (1-5)", "Do we have it?", "Type", "Cluster", "Why", "Comments"]
BASE_WIDTHS = [42, 28, 12, 10, 14, 20, 28, 55, 30]
LAYER_HEADERS = ["Dono", "Camada", "Fila"]  # the user's, like A-I (SISTEMA_AGENTES I.III.xvii)
LAYER_WIDTHS = [18, 10, 8]
# The agents a source can belong to, including those that do not exist yet, and the topic folder of
# each (None: no folder yet). The tracker never writes Dono; it only warns about a value outside this
# list (a typo would drop the source from every snapshot without a word) and about a source sitting
# in another agent's folder (owner.py moves it). analytics/agent_system/conhecimento.py's AREA is the
# same map (tests/test_conhecimento.py holds them equal).
OWNERS = {"cambio": "exchange_rate", "politica_monetaria": "monetary_policy", "inflacao": "inflation",
          "fiscal": "fiscal_policy", "externo": "external", "expectativas": "expectations",
          "atividade": "economic_activity", "credito": None, "mercado_trabalho": "labor_market",
          "trader": "trader"}
# The layout of the layer columns is this list; _migrate() moves the user's values by header name
# whenever it changes.
FIRST_LAYER = len(BASE_HEADERS) + 1        # column J
LAYER_COLS = range(FIRST_LAYER, FIRST_LAYER + len(LAYER_HEADERS))
CAMADA, FILA = (FIRST_LAYER + LAYER_HEADERS.index(h) for h in ("Camada", "Fila"))
NEW_HEADERS = ["File", "Ingestion", "Ingested on", "Extraction", "QC flags", "Synthesis", "Ingestion note"]
NEW_WIDTHS = [44, 16, 15, 22, 36, 11, 40]
FIRST_NEW = LAYER_COLS.stop                # column M
OLD_FIRST_NEW = FIRST_LAYER                # before 2026-10-21 the system's columns started at J
ADDED_MARK = "Added by ingestion"
LAYER_NOTE = ("Dono: the agent whose library the source belongs to, by the question it answers "
              f"({', '.join(OWNERS)}; one that does not exist yet is fine). Camada, in the owner's library: "
              "1 = the core the agent reads, 2 = depth and alternatives, 3 = the rest. Other agents reach a "
              "layer-1 source through the concept pages (SISTEMA_AGENTES I.III.xvii, PLANO_AGENTES I). "
              "Fila: the order in which layers 2 and 3 are promoted, 1 first. All three are yours; "
              "tracker.py never writes them.")
MM_LAYER_NOTE = ("Camada and Fila of the document in the library of its area's agent (the owner is the "
                 "document's area). Yours; tracker.py never writes them.")
MM_TAB, COPOM_TAB = "Mental Models", "Copom"
LABEL = {"ingested": "Ingested", "pending": "Pending", "needs_attention": "Needs attention", "on_hold": "On hold"}
_RANK = ["needs_attention", "pending", "on_hold", "ingested"]   # the worst state of a row's files wins
_STOP = {"and", "the", "of", "in", "a", "an", "for", "on", "to", "et", "al", "l1", "l2", "l3", "vs"}

# The workbook's own conventions (measured on the hand-kept tabs).
FONT = Font(name="Calibri", size=11)
HEADER_FONT = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
TEAL = PatternFill("solid", fgColor="418791")     # the user's header colour
NAVY = PatternFill("solid", fgColor="1F2853")     # the system's columns
EDGE = Side(style="thin", color="D7DAE2")
BORDER = Border(left=EDGE, right=EDGE, top=EDGE, bottom=EDGE)
TOP = Alignment(vertical="top", wrap_text=True)
TOP_CENTER = Alignment(horizontal="center", vertical="top", wrap_text=True)
HEAD = Alignment(horizontal="center", vertical="center", wrap_text=True)
YES_FILL, NO_FILL = "DCEEE8", "FBEAE6"
STATE_FILL = {"Ingested": "DCEEE8", "Pending": "FFF1CC", "Needs attention": "F8DAD5", "On hold": "E6E8EE"}
CENTERED = {3, 4, 5, *LAYER_COLS, FIRST_NEW + 1, FIRST_NEW + 2, FIRST_NEW + 5}   # Date, Importance, Do we have it, the layer columns, Ingestion, Ingested on, Synthesis
LINE_PT = 15.0


# ── matching ─────────────────────────────────────────────────────────────────

def _norm_tokens(s: str) -> list[str]:
    s = unicodedata.normalize("NFKD", str(s or "")).encode("ascii", "ignore").decode().lower()
    # "Ch. 3" in a row's title is the "ch3" of the file name: one row per book chapter, and the
    # chapter number is what separates Gali (2015) ch. 3 from ch. 4, whose titles share words.
    s = re.sub(r"\bch(?:apter)?\.?\s*(\d+)\b", r"ch\1", s)
    return [t for t in re.split(r"[^a-z0-9]+", s) if len(t) > 1 and t not in _STOP]


# Institutions abbreviated in file names but spelled out in the lists.
_ALIASES = {"bcb": "brasil", "imf": "monetary", "bis": "settlements", "fed": "reserve"}


def _parse_stem(stem: str) -> tuple[list[str], list[str], str] | None:
    m = re.match(r"^(.*) \((.+), (\d{4})[a-z]?\)$", stem)
    if not m:
        return None
    desc, authors, year = m.groups()
    a = _norm_tokens(authors)
    return _norm_tokens(desc.replace("_", " ")), a + [_ALIASES[t] for t in a if t in _ALIASES], year


def _same_word(a: str, b: str) -> bool:
    # "rate"/"rates", "flow"/"flows" match; "international"/"intervention" do not.
    k = min(6, len(a), len(b))
    return k >= 4 and a[:k] == b[:k] or a == b


def _overlap(desc: list[str], words: list[str]) -> int:
    """How many distinct words of the title are covered by the file's description
    (counted on the title's side, so "rate" and "rates" in one description count once)."""
    return sum(1 for w in set(words) if any(_same_word(t, w) for t in desc))


def _match(file_info, rows):
    """rows: list of (row id, author tokens, year, title tokens). Returns (row, None) or (None, why)."""
    desc, authors, year = file_info
    scored = []
    for r, a_tok, r_year, n_tok in rows:
        if r_year != year:
            continue
        a = sum(1 for t in authors if t in a_tok)
        if a:
            scored.append(((a, _overlap(desc, n_tok)), r))
    if not scored:
        # No author in common ("IMF" on the file, the staff names on the row): the same year and
        # at least two title words, from one row only.
        by_title = sorted(((_overlap(desc, n_tok), r) for r, _, r_year, n_tok in rows if r_year == year), reverse=True)
        if by_title and by_title[0][0] >= 2 and (len(by_title) == 1 or by_title[0][0] > by_title[1][0]):
            return by_title[0][1], None
        return None, ""
    scored.sort(key=lambda x: x[0], reverse=True)
    if len(scored) > 1 and scored[0][0] == scored[1][0]:
        return None, "matches several rows equally: " + ", ".join(str(r) for _, r in scored[:3])
    return scored[0][1], None


def _with_synthesis(topic: str, files: list[dict]) -> set[str]:
    """File names that have a synthesis note. The vault agent names each note after its file
    (synthesis/<name>.md, since 2026-10-19; the older notes were renamed the same day), so the
    match is exact. A note named freely ("Fleming 1962 - Domestic Financial Policies…") goes to
    the one file with its year and first author whose description it shares most words with;
    a tie goes to nobody."""
    d = OBSIDIAN / topic / "synthesis"
    if not d.is_dir():
        return set()
    names = {f["name"] for f in files}
    out = {n.stem for n in d.glob("*.md") if n.stem in names}
    parsed = [(f["name"], _parse_stem(f["name"])) for f in files]
    for note in d.glob("*.md"):
        if note.stem in names or NAME_RE.match(note.stem):
            continue                     # exact, or named after a file that has no PDF here
        words = _norm_tokens(note.stem)
        scored = sorted(((_overlap(info[0], words), name) for name, info in parsed
                         if info and info[1] and info[2] in words and info[1][0] in words), reverse=True)
        if scored and scored[0][0] >= 1 and (len(scored) == 1 or scored[0][0] > scored[1][0]):
            out.add(scored[0][1])
    return out


def _log_rows() -> dict[tuple[str, str], list[str]]:
    out = {}
    if LOG.exists():
        for line in LOG.read_text(encoding="utf-8").splitlines():
            if re.match(r"^\| \d{4}-\d{2}-\d{2} \|", line):
                cells = [c.strip() for c in line.strip("|").split("|")]
                out[(cells[1], cells[2])] = cells          # last line per file wins
    return out


# ── formatting ───────────────────────────────────────────────────────────────

def _header(ws, col: int, text: str, fill: PatternFill, width: float) -> None:
    c = ws.cell(1, col, text)
    c.font, c.fill, c.alignment, c.border = HEADER_FONT, fill, HEAD, BORDER
    ws.column_dimensions[get_column_letter(col)].width = width


def _body(cell) -> None:
    cell.font = FONT
    cell.border = BORDER
    cell.alignment = TOP_CENTER if cell.column in CENTERED else TOP


def _lines(value, width: float) -> int:
    if value in (None, ""):
        return 1
    per_line = max(int(width * 1.15), 1)     # Calibri 11 fits ~1.15 characters per width unit
    return sum(max(math.ceil(len(part) / per_line), 1) for part in str(value).split("\n"))


def _fit_height(ws, r: int, cols: range, keep_existing: bool) -> None:
    need = max(_lines(ws.cell(r, c).value, ws.column_dimensions[get_column_letter(c)].width or 10) for c in cols)
    h = need * LINE_PT + 4
    cur = ws.row_dimensions[r].height
    ws.row_dimensions[r].height = max(h, cur) if keep_existing and cur else h


def _ensure_tab(wb, title: str):
    if title in wb.sheetnames:
        return wb[title]
    ws = wb.create_sheet(title)
    for i, (h, w) in enumerate(zip(BASE_HEADERS, BASE_WIDTHS), 1):
        _header(ws, i, h, TEAL, w)
    ws.row_dimensions[1].height = 27.6
    ws.freeze_panes = "A2"
    ws.sheet_view.showGridLines = False
    ws.sheet_view.zoomScale = 70
    return ws


# ── one tab ──────────────────────────────────────────────────────────────────

def _migrate(ws) -> bool:
    """Puts the tab in the current layout — A-I, then LAYER_HEADERS, then the system's columns —
    whatever layout it had: the one before 2026-10-21 (system in J-P, no layer columns) or one
    with other layer columns. The user's layer values are read by HEADER NAME and written back
    under the same name, so adding, dropping or reordering a layer column moves no value to the
    wrong place (a column no longer in LAYER_HEADERS is dropped, and said so). The system's
    columns are rewritten on every run, so clearing them loses nothing; A-I are not touched."""
    head = {str(ws.cell(1, c).value or ""): c for c in range(OLD_FIRST_NEW, ws.max_column + 1)}
    want = LAYER_HEADERS + NEW_HEADERS
    if [ws.cell(1, OLD_FIRST_NEW + i).value for i in range(len(want))] == want:
        return False
    sys_col = head.get(NEW_HEADERS[0], ws.max_column + 1)
    layer = {h: c for h, c in head.items() if h and c < sys_col}
    dropped = [h for h in layer if h not in LAYER_HEADERS]
    if dropped and any(ws.cell(r, layer[h]).value not in (None, "") for h in dropped for r in range(2, ws.max_row + 1)):
        print(f"  {ws.title}: layer column(s) {', '.join(dropped)} no longer in the layout — their values are dropped")
    kept = {h: [ws.cell(r, c).value for r in range(2, ws.max_row + 1)] for h, c in layer.items() if h in LAYER_HEADERS}
    for r in range(1, ws.max_row + 1):
        for c in range(OLD_FIRST_NEW, ws.max_column + 1):
            cell = ws.cell(r, c)
            cell.value, cell.fill, cell.comment = None, PatternFill(), None
    for h, values in kept.items():
        c = OLD_FIRST_NEW + LAYER_HEADERS.index(h)
        for r, v in enumerate(values, 2):
            ws.cell(r, c).value = v
    return True


def _fill_tab(ws, topic: str, log: dict) -> dict:
    last_new = FIRST_NEW + len(NEW_HEADERS) - 1
    _migrate(ws)
    # 1. remove the rows this script appended last time (keeping a Camada/Fila typed on them, by
    #    file name); clear its columns on the others
    carried = {}
    for r in range(ws.max_row, 1, -1):
        if str(ws.cell(r, 9).value or "").startswith(ADDED_MARK):
            layer = tuple(ws.cell(r, c).value for c in LAYER_COLS)
            if any(v not in (None, "") for v in layer):
                carried[str(ws.cell(r, FIRST_NEW).value or "")] = layer
            ws.delete_rows(r)
            ws.row_dimensions[r].height = None
    for r in range(2, ws.max_row + 1):
        for c in range(FIRST_NEW, last_new + 1):
            cell = ws.cell(r, c)
            cell.value, cell.fill = None, PatternFill()
    for i, (h, w) in enumerate(zip(LAYER_HEADERS, LAYER_WIDTHS)):
        _header(ws, FIRST_LAYER + i, h, TEAL, w)
    ws.cell(1, FIRST_LAYER).comment = Comment(LAYER_NOTE, "tracker")
    for i, (h, w) in enumerate(zip(NEW_HEADERS, NEW_WIDTHS)):
        _header(ws, FIRST_NEW + i, h, NAVY, w)
    ws.cell(1, FIRST_NEW).comment = Comment(
        f"The navy columns ({get_column_letter(FIRST_NEW)}-{get_column_letter(last_new)}) are written by "
        "repository/ingestion/scripts/tracker.py after every ingestion; edits in them are overwritten. "
        f"The teal columns (A-{get_column_letter(FIRST_NEW - 1)}) are yours.", "ingestion")

    # 2. match each PDF on disk to a row
    rows = [(r, set(_norm_tokens(ws.cell(r, 2).value)), str(ws.cell(r, 3).value or "")[:4], _norm_tokens(ws.cell(r, 1).value))
            for r in range(2, ws.max_row + 1) if ws.cell(r, 1).value]
    curated_rows = {r for r, *_ in rows}
    per_row: dict[int, list[dict]] = {}
    unmatched = []
    files = scan(topic)
    with_syn = _with_synthesis(topic, files)
    for f in files:
        info = _parse_stem(f["name"])
        r, why = _match(info, rows) if info else (None, "")
        if r:
            per_row.setdefault(r, []).append(f)
        else:
            unmatched.append((f, info, why))

    # 3. append a row per PDF the curated list lacks; the user moves it into the list by filling A-I
    for f, info, why in unmatched:
        r = ws.max_row + 1
        author = re.search(r"\((.+), \d{4}", f["name"])
        title = f["name"].split(" (")[0].replace("_", " ")
        values = [title[:1].upper() + title[1:], author.group(1) if author else "", int(info[2]) if info else None,
                  None, "Yes", None, None, None,
                  f"{ADDED_MARK}: not in the curated list" + (f" ({why})" if why else "")
                  + ". Fill in columns A-I and delete this sentence to keep the row."]
        values += list(carried.get(f["name"], (None,) * len(LAYER_COLS)))
        for c, v in enumerate(values, 1):
            _body(ws.cell(r, c, v))
        per_row[r] = [f]

    # 4. the status columns
    for r, group in per_row.items():
        state = min((f["state"] for f in group), key=_RANK.index)
        label = LABEL[state]
        logs = [log.get((topic, f["name"])) for f in group]
        dates = sorted({lg[0] for lg in logs if lg})
        extraction = sorted({lg[3] for lg in logs if lg})
        flags = sorted({lg[7] for lg in logs if lg and lg[7] != "—"})
        if any(f["state"] == "ingested" for f in group) and not all(logs):
            dates.append("before 2026-10-19")
            extraction.append("old pipeline (x_tolerance 3)")
        n_syn = sum(1 for f in group if f["name"] in with_syn)
        has_syn = "Yes" if n_syn == len(group) else (f"{n_syn} of {len(group)}" if n_syn else "")
        notes = sorted({f["note"] for f in group if f["note"]})
        values = ["\n".join(f["name"] for f in group), label, ", ".join(dates), ", ".join(extraction),
                  "; ".join(flags), has_syn, "; ".join(notes)]
        for i, v in enumerate(values):
            _body(ws.cell(r, FIRST_NEW + i, v or None))
        ws.cell(r, FIRST_NEW + 1).fill = PatternFill("solid", fgColor=STATE_FILL[label])
        e = ws.cell(r, 5)
        e.value = "Yes"
        if e.fill.fill_type is None or (e.fill.fgColor.rgb or "").endswith(NO_FILL):
            e.fill = PatternFill("solid", fgColor=YES_FILL)    # a user's own highlight (e.g. yellow) stays
        for c in LAYER_COLS:
            _body(ws.cell(r, c))
        _fit_height(ws, r, range(1, last_new + 1), keep_existing=r in curated_rows)

    # 5. curated rows without a PDF still get the grid in the new columns
    for r in curated_rows - set(per_row):
        for c in range(FIRST_LAYER, last_new + 1):
            _body(ws.cell(r, c))

    # 6. an owner outside the list drops the source from every snapshot without a word: say so
    dono = FIRST_LAYER + LAYER_HEADERS.index("Dono")
    odd = sorted({str(ws.cell(r, dono).value) for r in range(2, ws.max_row + 1)
                  if ws.cell(r, dono).value not in (None, "") and str(ws.cell(r, dono).value).strip() not in OWNERS})
    if odd:
        print(f"  {ws.title}: Dono not in {', '.join(OWNERS)}: {', '.join(odd)}")
    # 7. a source in another owner's folder is read from there by the snapshot all the same, but the
    #    folders stop telling whose library it is: say so, and owner.py --move puts it back
    away = sorted(str(ws.cell(r, FIRST_NEW).value).splitlines()[0] for r in range(2, ws.max_row + 1)
                  if ws.cell(r, FIRST_NEW).value
                  and OWNERS.get(str(ws.cell(r, dono).value or "").strip()) not in (None, topic))
    if away:
        print(f"  {ws.title}: {len(away)} source(s) outside their owner's folder "
              f"(owner.py --move): {'; '.join(away)}")

    ws.auto_filter.ref = f"A1:{get_column_letter(last_new)}{ws.max_row}"
    ws.sheet_view.showGridLines = False
    return {"files": sum(len(v) for v in per_row.values()), "appended": len(unmatched), "odd_owners": odd,
            "away": away}


def _summary(wb, tabs: list[tuple[str, str]]) -> None:
    """One line per area, read left to right as the work goes: the list, the PDFs, the text,
    the synthesis. Every count is of rows of the area tab, one row per source file (a book
    has a row per chapter). Dropped rows are out of the list. The two shares divide by
    Sources, so they read as how far each area is from done."""
    if SUMMARY in wb.sheetnames:
        del wb[SUMMARY]
    ws = wb.create_sheet(SUMMARY, 0)
    groups = [("", 1, 1), ("The list", 2, 3), ("Ingestion (text into the vault)", 4, 6), ("Synthesis", 7, 8)]
    heads = ["Area", "Sources", "Acquired",
             "Ingested", "% of sources", "Needs attention",
             "Synthesized", "% of sources"]
    pct_cols = {5, 8}
    # teal = the user's columns (the list), navy = the system's (ingestion, synthesis)
    fill = lambda c: TEAL if c <= 3 else NAVY  # noqa: E731
    for i, h in enumerate(heads, 1):
        for row, text in ((1, None), (2, h)):
            cell = ws.cell(row, i, text)
            cell.font, cell.alignment, cell.border, cell.fill = HEADER_FONT, HEAD, BORDER, fill(i)
        ws.column_dimensions[get_column_letter(i)].width = 24 if i == 1 else 13
    for title, a, b in groups:
        ws.cell(1, a).value = title or None
        if b > a:
            ws.merge_cells(start_row=1, start_column=a, end_row=1, end_column=b)
    ws.row_dimensions[1].height = 22
    ws.row_dimensions[2].height = 30
    first = 3
    ing, syn = get_column_letter(FIRST_NEW + 1), get_column_letter(FIRST_NEW + 5)
    for r, (_, tab) in enumerate(tabs, first):
        q = f"'{tab}'!"
        share = lambda col: f'=IF(B{r}=0,"",{col}{r}/B{r})'  # noqa: E731
        values = [tab.replace("Qual - ", ""),
                  f'=COUNTA({q}A:A)-1-COUNTIF({q}E:E,"Dropped")', f'=COUNTIF({q}E:E,"Yes")',
                  f'=COUNTIF({q}{ing}:{ing},"Ingested")', share("D"), f'=COUNTIF({q}{ing}:{ing},"Needs attention")',
                  f'=COUNTIF({q}{syn}:{syn},"Yes")', share("G")]
        for c, v in enumerate(values, 1):
            cell = ws.cell(r, c, v)
            cell.font, cell.border = FONT, BORDER
            cell.alignment = Alignment(vertical="center", horizontal="left" if c == 1 else "center")
            if c in pct_cols:
                cell.number_format = "0%"
        ws.row_dimensions[r].height = 20
    t = first + len(tabs)
    ws.cell(t, 1, "Total")
    for c in range(2, len(heads) + 1):
        col = get_column_letter(c)
        if c in pct_cols:           # the total's share, not a sum of shares
            num = get_column_letter(c - 1)
            ws.cell(t, c, f'=IF(B{t}=0,"",{num}{t}/B{t})').number_format = "0%"
        else:
            ws.cell(t, c, f"=SUM({col}{first}:{col}{t - 1})")
    for c in range(1, len(heads) + 1):
        cell = ws.cell(t, c)
        cell.font, cell.border = Font(name="Calibri", size=11, bold=True), BORDER
        cell.alignment = Alignment(vertical="center", horizontal="left" if c == 1 else "center")
        cell.fill = PatternFill("solid", fgColor="EEF0F5")
    ws.row_dimensions[t].height = 20
    notes = [
        "Sources: rows of the area tab, one per file (a book has a row per chapter), dropped rows excluded. "
        "Acquired: the PDF is in the folder. Ingested: its text is in the vault. Needs attention: ingestion was tried "
        "and the tools could not read it (a scan, a broken font — the reason is in the area tab). Synthesized: the "
        "ingested file has a synthesis note. Both % columns divide by Sources.",
        "Acquired but neither Ingested nor Needs attention: not run yet (/ingest), or the area is on hold in "
        "settings.yaml (Trader). Recurring BCB documents (Copom statement, minutes, RPM) reach the vault through "
        "the Copom ETL and are listed in the Copom tab; the managers' letters, in the Mental Models tab.",
        "The reasoning behind each area's list — scope, cluster notes, open gaps, acquisition order — is in the Notes tab.",
        "Written by repository/ingestion/scripts/tracker.py on every ingestion, mental-model run and Copom load. "
        "In the area tabs, teal columns are yours (Dono, Camada and Fila included), navy ones the system's.",
    ]
    for i, n in enumerate(notes, t + 2):
        ws.cell(i, 1, n).font = Font(name="Calibri", size=10, italic=True, color="5B6377")
    ws.freeze_panes = "B3"
    ws.sheet_view.showGridLines = False
    ws.sheet_view.zoomScale = 100


# ── the tabs rebuilt from the folders: Mental Models, Copom ──────────────────

def _rebuild(wb, title: str):
    """Drop and recreate a tab in the same place (at the end the first time)."""
    pos = wb.sheetnames.index(title) if title in wb.sheetnames else len(wb.sheetnames)
    if title in wb.sheetnames:
        del wb[title]
    ws = wb.create_sheet(title, pos)
    ws.sheet_view.showGridLines = False
    ws.sheet_view.zoomScale = 85
    return ws


def _table(ws, top: int, heads: list[tuple[str, float, PatternFill]], rows: list[list], centered: set[int]) -> int:
    """Header row at `top` and the rows under it. Returns the last row written."""
    for c, (h, w, fill) in enumerate(heads, 1):
        cell = ws.cell(top, c, h)
        cell.font, cell.fill, cell.alignment, cell.border = HEADER_FONT, fill, HEAD, BORDER
        dim = ws.column_dimensions[get_column_letter(c)]
        dim.width = max(w, dim.width if top != 1 and dim.width else 0)
    ws.row_dimensions[top].height = 30
    for r, values in enumerate(rows, top + 1):
        for c, v in enumerate(values, 1):
            cell = ws.cell(r, c, v)
            cell.font, cell.border = FONT, BORDER
            cell.alignment = TOP_CENTER if c in centered else TOP
    return top + len(rows)


def _kept(wb, title: str, key: str, cols: tuple[str, ...]) -> dict[str, tuple]:
    """The user's values in `cols` of the first table of a tab about to be rebuilt, by `key`."""
    if title not in wb.sheetnames:
        return {}
    ws = wb[title]
    head = {ws.cell(1, c).value: c for c in range(1, ws.max_column + 1)}
    if key not in head or not all(c in head for c in cols):
        return {}
    out = {}
    for r in range(2, ws.max_row + 1):
        k = ws.cell(r, head[key]).value
        if not k:
            break                                  # the blank row before the second table
        vals = tuple(ws.cell(r, head[c]).value for c in cols)
        if any(v not in (None, "") for v in vals):
            out[str(k)] = vals
    return out


def _mental_models(wb) -> dict:
    import mental
    cfg = mental.config()
    kept = _kept(wb, MM_TAB, "Document", ("Camada", "Fila"))
    configured = set(cfg.get("documents") or {})
    docs = sorted({(m, a) for m in cfg["managers"] for a in cfg["areas"]
                   if mental.doc_path(cfg, m, a).exists() or mental.ledger_path(mental.doc_name(cfg, m, a)).exists()
                   or mental.doc_name(cfg, m, a) in configured}, key=lambda x: (x[1], x[0]))
    awaiting = {}           # the PDFs /ingest has not turned into clean_md yet (not scan(): it reads settings.yaml per file)
    for m, mc in cfg["managers"].items():
        folders = {c["path"].split("/")[0] for c in mc["corpora"]}
        awaiting[m] = sum(1 for fo in folders for pdf in (MM_DIR / fo / "raw_pdf").glob("*.pdf")
                          if not (MM_DIR / fo / "clean_md" / f"{pdf.stem}.md").exists())
    summary, letters_rows, counts = [], [], {}
    for m, a in docs:
        s = mental.state(cfg, m, a)
        read_on = mental.ledger(s["name"])
        window = (f"{s['start']:%Y-%m}" if s["start"] else "start") + " → " + (f"{s['end']:%Y-%m}" if s["end"] else "open")
        in_window = sorted(s["done"] + s["pending"], key=lambda x: (x["date"], x["name"]))
        runs = sorted(v for v in read_on.values() if v != "seeded")
        last = runs[-1] if runs else ("seeded (before the ledger)" if read_on else "—")
        camada, fila = kept.get(s["name"], (None, None))
        summary.append([s["name"], a, cfg["managers"][m]["name"], window, len(s["done"]) + len(s["pending"]),
                        len(s["done"]), len(s["pending"]), last, awaiting[m], camada, fila])
        counts[s["name"]] = {"read": len(s["done"]), "pending": len(s["pending"])}
        for x in in_window:
            letters_rows.append([s["name"], x["name"], x["date"].isoformat(), str(x["path"].parent.relative_to(MM_DIR)),
                                 "Read" if x["name"] in read_on else "Pending", read_on.get(x["name"])])
    ws = _rebuild(wb, MM_TAB)
    heads = [("Document", 34, NAVY), ("Area", 24, NAVY), ("Manager", 14, NAVY), ("Window", 22, NAVY),
             ("Letters in window", 12, NAVY), ("Read", 12, NAVY), ("Pending", 9, NAVY), ("Last run", 15, NAVY),
             ("Awaiting /ingest", 11, NAVY), ("Camada", 10, TEAL), ("Fila", 8, TEAL)]
    end = _table(ws, 1, heads, summary, centered=set(range(5, 12)))
    ws.cell(1, 1).comment = Comment(
        "Rebuilt from the folders by repository/ingestion/scripts/tracker.py (run.py, mental.py done). Read = letters in "
        "ledger/<document>.tsv; Pending = letters in the window not read yet; Awaiting /ingest = the manager's PDFs "
        "without clean_md. Camada and Fila (teal) are yours and survive the rebuild.", "tracker")
    ws.cell(1, 10).comment = Comment(MM_LAYER_NOTE, "tracker")
    for r in range(2, end + 1):
        if ws.cell(r, 7).value:
            ws.cell(r, 7).fill = PatternFill("solid", fgColor=STATE_FILL["Pending"])
    top = end + 2
    lheads = [("Document", 34, NAVY), ("Letter", 24, NAVY), ("Date", 14, NAVY), ("Corpus", 22, NAVY),
              ("Status", 12, NAVY), ("Read on", 12, NAVY)]
    last = _table(ws, top, lheads, letters_rows, centered={3, 5, 6})
    for r in range(top + 1, last + 1):
        ws.cell(r, 5).fill = PatternFill("solid", fgColor=STATE_FILL["Ingested" if ws.cell(r, 5).value == "Read" else "Pending"])
    ws.freeze_panes = "B2"
    return counts


COPOM = OBSIDIAN / "monetary_policy" / "clean_md" / "central_bank"
COPOM_KINDS = (("Statement", "comunicados"), ("Minutes", "atas"), ("RPM", "rpm"))
# Layer 1 of the Copom documents = every statement, minutes and RPM PUBLISHED since this date and
# before the cycle: the start of the term of the current BCB governor (Galípolo, 2025-01-01).
# Changes when the governor changes. Decided by the user 2026-10-21.
MANDATO_INICIO = dt.date(2025, 1, 1)
COPOM_LAYER1 = 1       # a cycle dated before MANDATO_INICIO (a backtest) gets this many latest of each kind
_ISO = r"(\d{4}-\d{2}-\d{2})"


def copom_docs() -> list[dict]:
    """Every Copom document in the vault: {kind, folder, name, path, meeting, date, published}.
    date = the meeting (statement, minutes) or the issue (RPM); published = when the text came out,
    from the file's own header: the minutes come ~6 days after the meeting, the statement the same
    day. This is what the recency rule compares with the cycle date."""
    out = []
    for kind, folder in COPOM_KINDS:
        for p in sorted((COPOM / folder).glob("*.md")):
            with p.open(encoding="utf-8") as fh:
                head = fh.read(1500)
            g = lambda rx: (re.search(rx, head, re.M) or [None, None])[1]  # noqa: E731
            ref = g(rf"^Data de refer[êe]ncia:\s*{_ISO}") or (re.findall(_ISO, p.stem) or [None])[-1]
            pub = g(rf"^Data de publica[çc][ãa]o:\s*{_ISO}") or g(rf"^Publicado em:\s*{_ISO}") or ref
            meeting = g(r"^Reuni[ãa]o:\s*(\d+)")
            out.append({"kind": kind, "folder": folder, "name": p.stem, "path": p,
                        "meeting": int(meeting) if meeting else None,
                        "date": dt.date.fromisoformat(ref) if ref else None,
                        "published": dt.date.fromisoformat(pub) if pub else None})
    return out


def copom_layer(docs: list[dict], before: dt.date, n: int = COPOM_LAYER1,
                mandato: dt.date = MANDATO_INICIO) -> dict[str, int | None]:
    """The layer of each Copom document for a cycle on `before`, by document name. Only what was
    published strictly before `before` counts (the minutes by their publication, ~6 days after the
    meeting); one published on or after it is None — it did not exist yet for that cycle.
    Layer 1 = every statement, minutes and RPM published since `mandato` (the current governor's
    term); the rest is layer 3 (history). A cycle dated before `mandato` (a backtest) falls back
    to the `n` latest of each kind, so it is never left without a document."""
    out = {}
    for kind, _ in COPOM_KINDS:
        known = sorted((d for d in docs if d["kind"] == kind and d["published"] and d["published"] < before),
                       key=lambda d: (d["published"], d["meeting"] or 0, d["name"]), reverse=True)
        in_term = before > mandato
        for i, d in enumerate(known):
            out[d["name"]] = 1 if (d["published"] >= mandato if in_term else i < n) else 3
    for d in docs:
        out.setdefault(d["name"], None)
    return out


def _copom(wb) -> dict:
    docs = copom_docs()
    tomorrow = dt.date.today() + dt.timedelta(days=1)
    layer = copom_layer(docs, tomorrow)
    summary, rows, counts = [], [], {}
    for kind, folder in COPOM_KINDS:
        ds = [d for d in docs if d["kind"] == kind]
        pubs = sorted(d["published"] for d in ds if d["published"])
        l1 = sorted((d for d in ds if layer[d["name"]] == 1), key=lambda d: (d["published"], d["name"]))
        latest = (l1[0]["name"] if len(l1) == 1 else f"{len(l1)}: {l1[0]['name']} … {l1[-1]['name']}") if l1 else None
        summary.append([kind, f"central_bank/{folder}", len(ds), pubs[0].isoformat() if pubs else None,
                        pubs[-1].isoformat() if pubs else None, latest or None])
        counts[folder] = len(ds)
        for d in sorted(ds, key=lambda d: (d["published"] or dt.date.min, d["name"]), reverse=True):
            rows.append([kind, d["meeting"], d["name"], d["date"].isoformat() if d["date"] else None,
                         d["published"].isoformat() if d["published"] else None, layer[d["name"]]])
    ws = _rebuild(wb, COPOM_TAB)
    heads = [("Kind", 12, NAVY), ("Folder", 14, NAVY), ("Documents", 28, NAVY), ("First published", 13, NAVY),
             ("Last published", 12, NAVY), ("Layer 1 today", 36, NAVY)]
    end = _table(ws, 1, heads, summary, centered={3, 4, 5})
    ws.cell(1, 1).comment = Comment(
        "Rebuilt by repository/ingestion/scripts/tracker.py from obsidian/monetary_policy/clean_md/central_bank/ "
        "(the Copom ETL calls it after each load). First table: per kind, the count and the first and last "
        "publication. Layer, for a cycle on a date: every statement, minutes and RPM published since the current "
        f"BCB governor's term began ({MANDATO_INICIO:%Y-%m-%d}) and before the date is layer 1; the rest is layer 3 "
        "(history). The minutes count by their publication date. Here the cycle date is tomorrow; the cycle's knowledge snapshot "
        "applies the same rule (copom_layer) to its own date.", "tracker")
    top = end + 2
    dheads = [("Kind", 12, NAVY), ("Meeting", 14, NAVY), ("Document", 28, NAVY), ("Meeting date", 13, NAVY),
              ("Published", 12, NAVY), ("Layer", 36, NAVY)]
    last = _table(ws, top, dheads, rows, centered={2, 4, 5, 6})
    for r in range(top + 1, last + 1):
        if ws.cell(r, 6).value == 1:
            ws.cell(r, 6).fill = PatternFill("solid", fgColor=YES_FILL)
    ws.freeze_panes = "A2"
    return counts


def build(path: Path = TRACKER) -> str:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(path)
    wb = openpyxl.load_workbook(path)
    log = _log_rows()
    done = []
    for topic in topics():
        has_pdfs = any((REPOSITORY / topic / "raw_pdf").glob("*.pdf"))
        if TAB.get(topic) not in wb.sheetnames and not has_pdfs:
            continue
        ws = _ensure_tab(wb, TAB.get(topic, f"Qual - {topic.replace('_', ' ').title()}"))
        _fill_tab(ws, topic, log)
        done.append((topic, ws.title))
    _summary(wb, done)
    mm = _mental_models(wb)
    cp = _copom(wb)
    wb.active = 0
    wb.calculation.fullCalcOnLoad = True
    tmp = path.with_name(path.stem + ".tmp.xlsx")
    wb.save(tmp)
    try:
        os.replace(tmp, path)
    except PermissionError:
        tmp.unlink(missing_ok=True)
        raise PermissionError(f"{path.name} is open in Excel — close it and run tracker.py again")
    try:
        shown = path.relative_to(REPOSITORY.parent)
    except ValueError:
        shown = path
    return (f"{shown} updated ({len(done)} areas, {len(mm)} mental-model documents, "
            f"Copom {cp.get('comunicados', 0)}/{cp.get('atas', 0)}/{cp.get('rpm', 0)})")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description="Rewrite the system's columns and tabs of the knowledge tracker.")
    ap.add_argument("--file", type=Path, default=TRACKER, help="another copy of the workbook (default: the real one)")
    print(build(ap.parse_args().file))
