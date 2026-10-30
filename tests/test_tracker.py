"""
The knowledge tracker (repository/ingestion/scripts/tracker.py), for the five things that fail
without raising anything:

  1. the migration to Camada/Fila (2026-10-21) moves or blanks a cell of the user's columns A-I,
     or leaves an old system value (a file name) sitting in the new Camada/Fila columns;
  2. a Camada/Fila typed by the user is lost when the tracker rebuilds its rows and tabs;
  3. the Copom recency rule hands a cycle a document published on or after the cycle date (the
     minutes come ~6 days after the meeting: dating them by the meeting would leak them);
  4. the Copom ETL's call to the tracker raises when the workbook cannot be written (open in
     Excel), which would cost the load;
  5. owner.py, moving a source to its owner's folder, rewrites a frozen cycle snapshot, misses a
     link, or appends a second row next to the one the owner's list already had (the file would
     then match two rows and drop out of the list).

Script with asserts, not pytest (the project has no pytest), like tests/test_ingestion.py:

    uv run python tests/test_tracker.py

Never writes the real data_tracker.xlsx: every write goes to a copy in a temporary folder.
"""

import datetime as dt
import shutil
import sys
import tempfile
from pathlib import Path

import openpyxl

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "repository" / "ingestion" / "scripts"))

import tracker  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")
OLD_SYSTEM = ["File", "Ingestion", "Ingested on", "Extraction", "QC flags", "Synthesis", "Ingestion note"]


def _old_tab():
    """A Qual tab as it was before 2026-10-21: the user's A-I, the system's J-P."""
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Qual - Test"
    for c, h in enumerate(tracker.BASE_HEADERS + OLD_SYSTEM, 1):
        ws.cell(1, c, h)
    for r in range(2, 6):
        for c in range(1, 10):
            ws.cell(r, c, f"user {r},{c}")
        for c in range(10, 17):
            ws.cell(r, c, f"system {r},{c}")
    return wb, ws


def test_migration_keeps_a_to_i_and_clears_the_old_system_columns():
    wb, ws = _old_tab()
    before = [[ws.cell(r, c).value for c in range(1, 10)] for r in range(1, 6)]
    assert tracker._migrate(ws)
    assert [[ws.cell(r, c).value for c in range(1, 10)] for r in range(1, 6)] == before
    assert all(ws.cell(r, c).value is None for r in range(1, 6) for c in range(10, 17))
    # once the headers are in the current layout (_fill_tab writes them), _migrate is a no-op
    for c, h in enumerate(tracker.LAYER_HEADERS + OLD_SYSTEM, 10):
        ws.cell(1, c, h)
    ws.cell(2, 10, 1)
    assert not tracker._migrate(ws) and ws.cell(2, 10).value == 1


def test_migration_moves_layer_values_by_header_name():
    """A tab with other layer columns (here Camada, Fila, before Dono came in front): each value
    moves with its header, never by position."""
    wb, ws = _old_tab()
    tracker._migrate(ws)
    for c, h in enumerate(["Camada", "Fila"] + OLD_SYSTEM, 10):
        ws.cell(1, c, h)
    ws.cell(2, 10, 1), ws.cell(2, 11, 5), ws.cell(3, 10, 2)
    ws.cell(2, 12, "system file")
    assert tracker.LAYER_HEADERS == ["Dono", "Camada", "Fila"]
    assert tracker._migrate(ws)
    assert [ws.cell(2, c).value for c in (10, 11, 12)] == [None, 1, 5]
    assert [ws.cell(3, c).value for c in (10, 11, 12)] == [None, 2, None]
    assert ws.cell(2, 13).value is None                        # the old system column is cleared
    assert [ws.cell(2, c).value for c in range(1, 10)] == [f"user 2,{c}" for c in range(1, 10)]


def test_layout():
    assert tracker.LAYER_HEADERS == ["Dono", "Camada", "Fila"]
    assert (tracker.FIRST_LAYER, tracker.CAMADA, tracker.FILA, tracker.FIRST_NEW) == (10, 11, 12, 13)  # J, K, L, M
    assert tracker.NEW_HEADERS == OLD_SYSTEM


def test_unknown_owner_is_reported():
    wb, ws = _old_tab()
    ws.title = "Qual - Exchange Rate"
    tracker._migrate(ws)
    for c, h in enumerate(tracker.LAYER_HEADERS + OLD_SYSTEM, 10):
        ws.cell(1, c, h)
    ws.cell(2, tracker.FIRST_LAYER, "cambio"), ws.cell(3, tracker.FIRST_LAYER, "câmbio")
    out = tracker._fill_tab(ws, "exchange_rate", {})
    assert out["odd_owners"] == ["câmbio"], out


def test_kept_reads_the_first_table_only():
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = tracker.MM_TAB
    for c, h in enumerate(["Document", "x", "Camada", "Fila"], 1):
        ws.cell(1, c, h)
    ws.cell(2, 1, "doc_a"), ws.cell(2, 3, 1)
    ws.cell(3, 1, "doc_b")                                     # nothing typed: not kept
    ws.cell(5, 1, "Document"), ws.cell(6, 1, "doc_a"), ws.cell(6, 3, 9)   # second table, after the blank row
    assert tracker._kept(wb, tracker.MM_TAB, "Document", ("Camada", "Fila")) == {"doc_a": (1, None)}


def _doc(kind, name, published, meeting=None):
    return {"kind": kind, "name": name, "published": published, "meeting": meeting}


def test_copom_layer_uses_publication_date_strictly_before_the_cycle():
    d = dt.date
    docs = [_doc("Statement", "c267", d(2024, 12, 11), 267), _doc("Statement", "c268", d(2025, 1, 29), 268),
            _doc("Statement", "c280", d(2026, 8, 5), 280), _doc("Statement", "c281", d(2026, 9, 16), 281),
            _doc("Minutes", "a267", d(2024, 12, 17), 267), _doc("Minutes", "a268", d(2025, 2, 4), 268),
            _doc("Minutes", "a280", d(2026, 8, 12), 280), _doc("Minutes", "a281", d(2026, 9, 22), 281),
            _doc("RPM", "r12", d(2024, 12, 19)), _doc("RPM", "r06", d(2026, 6, 25)), _doc("RPM", "r09", d(2026, 9, 24))]
    # a cycle on 2026-09-18: everything published in the current term (since 2025-01-01) is layer 1,
    # what came before is history; the 281st minutes are not out yet (meeting 16/09, published 22/09)
    lay = tracker.copom_layer(docs, d(2026, 9, 18))
    assert lay == {"c267": 3, "c268": 1, "c280": 1, "c281": 1,
                   "a267": 3, "a268": 1, "a280": 1, "a281": None,
                   "r12": 3, "r06": 1, "r09": None}, lay
    # on the publication day itself the document does not count yet (strictly before)
    assert tracker.copom_layer(docs, d(2026, 9, 22))["a281"] is None
    assert tracker.copom_layer(docs, d(2026, 9, 23))["a281"] == 1
    # a cycle before the term (a backtest) still gets the latest of each kind
    early = tracker.copom_layer(docs, d(2025, 1, 1))
    assert (early["c267"], early["a267"], early["r12"]) == (1, 1, 1), early
    assert tracker.MANDATO_INICIO == d(2025, 1, 1)


def test_copom_layer_today_matches_the_decision():
    """2026-10-21: statements and minutes of meetings 268-281 (14 each), RPMs 202503-202609 (7)."""
    docs = tracker.copom_docs()
    lay = tracker.copom_layer(docs, dt.date(2026, 10, 22))
    l1 = {k: sorted(x["meeting"] or 0 for x in docs if x["kind"] == k and lay[x["name"]] == 1)
          for k, _ in tracker.COPOM_KINDS}
    assert l1["Statement"] == list(range(268, 282)), l1["Statement"]
    assert l1["Minutes"] == list(range(268, 282)), l1["Minutes"]
    rpm = sorted(x["name"][:10] for x in docs if x["kind"] == "RPM" and lay[x["name"]] == 1)
    assert rpm == [f"rpm_{m}" for m in ("202503", "202506", "202509", "202512", "202603", "202606", "202609")], rpm


def test_copom_docs_match_the_folders():
    docs = tracker.copom_docs()
    for kind, folder in tracker.COPOM_KINDS:
        on_disk = len(list((tracker.COPOM / folder).glob("*.md")))
        mine = [x for x in docs if x["kind"] == kind]
        assert len(mine) == on_disk, (kind, len(mine), on_disk)
        assert all(x["published"] for x in mine), [x["name"] for x in mine if not x["published"]][:3]
    atas = [x for x in docs if x["kind"] == "Minutes"]
    # the minutes are dated by publication, never by the meeting
    assert atas and all(x["published"] > x["date"] for x in atas), [x["name"] for x in atas if x["published"] <= x["date"]][:3]


def test_build_on_a_copy_keeps_the_users_layer_values():
    if not tracker.TRACKER.exists():
        print("  (skipped: no data_tracker.xlsx)")
        return
    with tempfile.TemporaryDirectory() as tmp:
        copy = Path(tmp) / "data_tracker.xlsx"
        shutil.copy(tracker.TRACKER, copy)
        tracker.build(copy)
        wb = openpyxl.load_workbook(copy)
        tab = next(t for t in wb.sheetnames if t.startswith("Qual"))
        wb[tab].cell(2, tracker.FIRST_LAYER, "cambio")
        wb[tab].cell(2, tracker.CAMADA, 1)
        wb[tab].cell(2, tracker.FILA, 3)
        mm = wb[tracker.MM_TAB]
        mm.cell(2, 10, 2)
        doc = mm.cell(2, 1).value
        wb.save(copy)
        tracker.build(copy)
        wb = openpyxl.load_workbook(copy)
        assert [wb[tab].cell(2, c).value for c in tracker.LAYER_COLS] == ["cambio", 1, 3]
        mm = wb[tracker.MM_TAB]
        assert mm.cell(2, 1).value == doc and mm.cell(2, 10).value == 2
        assert [wb[tab].cell(1, c).value for c in range(10, 20)] == tracker.LAYER_HEADERS + OLD_SYSTEM


def test_copom_etl_hook_never_raises():
    from domain.db.brasil.bcb import _copom_texto as ct
    with tempfile.TemporaryDirectory() as tmp:
        assert ct.atualizar_tracker(Path(tmp) / "missing.xlsx") is None      # warns, does not raise
        if tracker.TRACKER.exists():
            copy = Path(tmp) / "data_tracker.xlsx"
            shutil.copy(tracker.TRACKER, copy)
            assert "Copom" in (ct.atualizar_tracker(copy) or "")
            assert tracker.COPOM_TAB in openpyxl.load_workbook(copy).sheetnames


# ── owner.py: a source in another owner's folder ─────────────────────────────

import owner  # noqa: E402


def _current_tab(wb, title, rows):
    """A Qual tab in the current layout; rows: (Name, Autor, Date, Dono, File)."""
    ws = wb.create_sheet(title)
    for c, h in enumerate(tracker.BASE_HEADERS + tracker.LAYER_HEADERS + tracker.NEW_HEADERS, 1):
        ws.cell(1, c, h)
    for r, (name, autor, date, dono, file) in enumerate(rows, 2):
        ws.cell(r, 1, name), ws.cell(r, 2, autor), ws.cell(r, 3, date)
        ws.cell(r, tracker.FIRST_LAYER, dono), ws.cell(r, tracker.FIRST_NEW, file)
    return ws


def test_owner_plan_moves_only_rows_whose_owner_has_another_folder():
    wb = openpyxl.Workbook()
    _current_tab(wb, "Qual - Exchange Rate", [
        ("Pass-through", "Goldfajn", "2000", "inflacao", "depreciation_pass_through (Goldfajn, 2000)"),
        ("Overshooting", "Dornbusch", "1976", "cambio", "overshooting (Dornbusch, 1976)"),
        ("Credit", "Someone", "2010", "credito", "credit_thing (Someone, 2010)"),
        ("Not here yet", "Nobody", "2020", "externo", None)])
    rows, skipped = owner.plan(wb)
    assert [(r["src"], r["dst"], r["names"]) for r in rows] == [
        ("exchange_rate", "inflation", ["depreciation_pass_through (Goldfajn, 2000)"])], rows
    assert len(skipped) == 1 and "credito has no folder" in skipped[0], skipped


def test_owner_merges_into_the_owners_row_when_its_list_already_has_the_source():
    wb = openpyxl.Workbook()
    src = _current_tab(wb, "Qual - Exchange Rate", [
        ("Pass-through", "Goldfajn, I. & Werlang, S.", "2000", "inflacao", "depreciation_pass_through (Goldfajn, 2000)")])
    src.cell(2, tracker.CAMADA, 2)
    dst = _current_tab(wb, "Qual - Inflation", [
        ("Other", "Calvo", "1983", None, None),
        ("The Pass-Through from Depreciation to Inflation", "Goldfajn, I. & Werlang, S.", "2000", None, None)])
    dst.cell(3, tracker.FILA, 4)
    assert owner._same_source(dst, ["depreciation_pass_through (Goldfajn, 2000)"]) == 3
    assert owner._same_source(dst, ["something_else (Belaisch, 2003)"]) is None
    owner._merge_layer(src, 2, dst, 3)
    assert [dst.cell(3, c).value for c in tracker.LAYER_COLS] == ["inflacao", 2, 4]   # the owner's Fila stays


def test_owner_rewrites_links_but_not_the_frozen_cycles():
    with tempfile.TemporaryDirectory() as tmp:
        root, old = Path(tmp), owner.OBSIDIAN
        link = "[[exchange_rate/synthesis/x (A, 2000)\\|x]] and [[exchange_rate/clean_md/x (A, 2000)]]"
        for rel in ("concepts/c.md", "ciclos/2026-10-27/conhecimento/cambio/c.md", ".obsidian/w.md"):
            (root / rel).parent.mkdir(parents=True)
            (root / rel).write_bytes(f"line\r\n{link}\r\n".encode())
        owner.OBSIDIAN = root
        try:
            changed = owner._rewrite_links({"exchange_rate/synthesis/x (A, 2000)": "inflation/synthesis/x (A, 2000)",
                                            "exchange_rate/clean_md/x (A, 2000)": "inflation/clean_md/x (A, 2000)"})
        finally:
            owner.OBSIDIAN = old
        assert list(changed.values()) == [2], changed
        assert (root / "concepts/c.md").read_bytes() == (
            b"line\r\n[[inflation/synthesis/x (A, 2000)\\|x]] and [[inflation/clean_md/x (A, 2000)]]\r\n")
        for rel in ("ciclos/2026-10-27/conhecimento/cambio/c.md", ".obsidian/w.md"):
            assert b"exchange_rate/synthesis" in (root / rel).read_bytes(), rel


def test_owner_rewrites_the_log_topic_of_moved_files_only():
    with tempfile.TemporaryDirectory() as tmp:
        log, old = Path(tmp) / "LOG.md", owner.LOG
        log.write_bytes(b"| date | topic | file |\r\n"
                        b"| 2026-10-19 | exchange_rate | x (A, 2000) | default |\r\n"
                        b"| 2026-10-19 | exchange_rate | y (B, 2001) | default |\r\n")
        owner.LOG = log
        try:
            assert owner._rewrite_log({"x (A, 2000)": ("exchange_rate", "inflation")}) == 1
        finally:
            owner.LOG = old
        assert log.read_bytes() == (b"| date | topic | file |\r\n"
                                    b"| 2026-10-19 | inflation | x (A, 2000) | default |\r\n"
                                    b"| 2026-10-19 | exchange_rate | y (B, 2001) | default |\r\n")


if __name__ == "__main__":
    fails = 0
    for name, fn in list(globals().items()):
        if name.startswith("test_") and callable(fn):
            try:
                fn()
                print(f"ok    {name}")
            except AssertionError as e:
                fails += 1
                print(f"FAIL  {name}: {e}")
    print(f"\n{'all passed' if not fails else f'{fails} failed'}")
    sys.exit(1 if fails else 0)
