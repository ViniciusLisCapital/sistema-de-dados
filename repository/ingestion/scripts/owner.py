"""
Puts every source in its owner's folder (SISTEMA_AGENTES I.III.xvii): the owner is the Dono of the
source's row in the tracker; the folder is the topic of the "Qual" tab the row sits in.

    uv run python repository/ingestion/scripts/owner.py            # what is out of place
    uv run python repository/ingestion/scripts/owner.py --move     # move it

The owner always came from the tracker, never from the folder, so a source can sit in another
agent's folder for a while (the knowledge snapshot reads it from there all the same). tracker.py
says when one does. Moving it, for each file of such a row:
  - repository/<from>/raw_pdf/<name>.pdf and raw_md/<name>.md  -> repository/<to>/
  - obsidian/<from>/clean_md/<name>.md and synthesis/<name>.md -> obsidian/<to>/
  - every "<from>/clean_md/<name>" and "<from>/synthesis/<name>" in obsidian/ (the vault's links
    carry the folder) becomes "<to>/..." — except in obsidian/ciclos/, whose snapshots are frozen
    with the paths they were made with;
  - the topic of the file's lines in repository/ingestion/LOG.md (the tracker reads the log by
    topic and file);
  - the row (the user's columns A-L, values and formatting) leaves the "Qual" tab of <from> for the
    bottom of <to>'s, and tracker.py rebuilds the system's columns of both. When <to>'s list
    already has the source (one row the tracker would match to the file), that row stays as it is
    and only takes the moved row's Dono, Camada and Fila where it has none.
Nothing is moved when anything would be overwritten, or when the workbook cannot be written (open in
Excel): the workbook is saved to a temporary copy first, and the copy replaces it only after every
file has moved. A row whose owner has no folder yet (credito) stays where it is.
Run vault.py check afterwards: a link the rewrite missed resolves to no file and fails there.
"""

import argparse
import os
import re
import shutil
import sys
from pathlib import Path

import openpyxl
from openpyxl.comments import Comment

sys.path.insert(0, str(Path(__file__).resolve().parent))
import tracker  # noqa: E402
from run import LOG, OBSIDIAN, REPOSITORY  # noqa: E402

FROZEN = {"ciclos"}            # obsidian/ folders whose links are never rewritten


def _topic_of(title: str) -> str:
    rev = {t: k for k, t in tracker.TAB.items()}
    return rev.get(title, title.removeprefix("Qual - ").lower().replace(" ", "_"))


def _tab_of(topic: str) -> str:
    return tracker.TAB.get(topic, f"Qual - {topic.replace('_', ' ').title()}")


def plan(wb) -> tuple[list[dict], list[str]]:
    """Every row whose Dono's folder is not its tab's: {tab, row, src, dst, names}. Also the rows
    left alone, with why."""
    out, skipped = [], []
    dono_col = tracker.FIRST_LAYER + tracker.LAYER_HEADERS.index("Dono")
    for title in wb.sheetnames:
        if not title.startswith("Qual - "):
            continue
        ws, src = wb[title], _topic_of(title)
        for r in range(2, ws.max_row + 1):
            dono = str(ws.cell(r, dono_col).value or "").strip()
            names = [n.strip() for n in str(ws.cell(r, tracker.FIRST_NEW).value or "").splitlines() if n.strip()]
            if not dono or not names or dono not in tracker.OWNERS:
                continue
            dst = tracker.OWNERS[dono]
            if dst == src:
                continue
            if dst is None:
                skipped.append(f"{title} row {r} ({'; '.join(names)}): {dono} has no folder yet")
                continue
            out.append({"tab": title, "row": r, "src": src, "dst": dst, "dono": dono, "names": names})
    return out, skipped


def _files(src: str, dst: str, name: str) -> list[tuple[Path, Path]]:
    pairs = [(REPOSITORY / src / "raw_pdf" / f"{name}.pdf", REPOSITORY / dst / "raw_pdf" / f"{name}.pdf"),
             (REPOSITORY / src / "raw_md" / f"{name}.md", REPOSITORY / dst / "raw_md" / f"{name}.md"),
             (OBSIDIAN / src / "clean_md" / f"{name}.md", OBSIDIAN / dst / "clean_md" / f"{name}.md"),
             (OBSIDIAN / src / "synthesis" / f"{name}.md", OBSIDIAN / dst / "synthesis" / f"{name}.md")]
    return [(a, b) for a, b in pairs if a.exists()]


def _copy_row(ws_from, r_from: int, ws_to, r_to: int) -> None:
    for c in range(1, tracker.FIRST_NEW):
        a, b = ws_from.cell(r_from, c), ws_to.cell(r_to, c)
        b.value = a.value
        if a.has_style:
            b._style = a._style
        if a.comment:
            b.comment = Comment(a.comment.text, a.comment.author)
        if a.hyperlink:
            b.hyperlink = a.hyperlink.target
    h = ws_from.row_dimensions[r_from].height
    if h:
        ws_to.row_dimensions[r_to].height = h


def _same_source(ws, names: list[str]) -> int | None:
    """The curated row of the owner's tab that tracker.py would match to these files, when there is
    exactly one: the owner's list often already had the source (Goldfajn & Werlang 2000 was in both
    the FX and the inflation lists). Appending the moved row next to it would make the file match two
    rows, and the tracker would set it aside as unmatched."""
    rows = [(r, set(tracker._norm_tokens(ws.cell(r, 2).value)), str(ws.cell(r, 3).value or "")[:4],
             tracker._norm_tokens(ws.cell(r, 1).value))
            for r in range(2, ws.max_row + 1)
            if ws.cell(r, 1).value and not str(ws.cell(r, 9).value or "").startswith(tracker.ADDED_MARK)]
    hits = set()
    for name in names:
        info = tracker._parse_stem(name)
        hits.add(tracker._match(info, rows)[0] if info else None)
    return hits.pop() if len(hits) == 1 and None not in hits else None


def _merge_layer(ws_from, r_from: int, ws_to, r_to: int) -> None:
    """Dono, Camada and Fila of the moved row, where the owner's row has none."""
    for c in tracker.LAYER_COLS:
        if ws_to.cell(r_to, c).value in (None, "") and ws_from.cell(r_from, c).value not in (None, ""):
            ws_to.cell(r_to, c).value = ws_from.cell(r_from, c).value


def _rewrite_links(renames: dict[str, str]) -> dict[Path, int]:
    """'<from>/<kind>/<name>' -> '<to>/<kind>/<name>' in every .md of obsidian/ outside FROZEN and
    the dot folders. Returns the files changed, with the count."""
    if not renames:
        return {}
    rx = re.compile("|".join(re.escape(k) for k in sorted(renames, key=len, reverse=True)))
    changed = {}
    for p in OBSIDIAN.rglob("*.md"):
        rel = p.relative_to(OBSIDIAN).parts
        if rel[0] in FROZEN or any(part.startswith(".") for part in rel):
            continue
        with open(p, encoding="utf-8", newline="") as f:     # keep each file's line endings
            text = f.read()
        new, n = rx.subn(lambda m: renames[m.group(0)], text)
        if n:
            with open(p, "w", encoding="utf-8", newline="") as f:
                f.write(new)
            changed[p] = n
    return changed


def _rewrite_log(moves: dict[str, tuple[str, str]]) -> int:
    """The topic cell of each moved file's lines in LOG.md. moves: name -> (from, to)."""
    if not LOG.exists():
        return 0
    with open(LOG, encoding="utf-8", newline="") as f:
        lines, n = f.read().split("\n"), 0
    for i, line in enumerate(lines):
        if re.match(r"^\| \d{4}-\d{2}-\d{2} \|", line):
            cells = line.split("|")
            name = cells[3].strip()
            if name in moves and cells[2].strip() == moves[name][0]:
                cells[2] = f" {moves[name][1]} "
                lines[i] = "|".join(cells)
                n += 1
    with open(LOG, "w", encoding="utf-8", newline="") as f:
        f.write("\n".join(lines))
    return n


def move(path: Path = tracker.TRACKER) -> list[str]:
    tracker.build(path)                    # the File column, from the folders as they are now
    wb = openpyxl.load_workbook(path)
    rows, skipped = plan(wb)
    report = [f"left alone: {s}" for s in skipped]
    if not rows:
        return report + ["nothing out of place"]

    # 1. everything that would move, and nothing in the way
    pairs, clash = [], []
    for row in rows:
        for name in row["names"]:
            for a, b in _files(row["src"], row["dst"], name):
                (clash.append(str(b.relative_to(REPOSITORY.parent))) if b.exists() else pairs.append((a, b)))
    if clash:
        raise FileExistsError("already in the owner's folder, nothing moved: " + "; ".join(clash))

    # 2. the rows, saved to a copy first (an open workbook fails here, before any file moves)
    by_tab: dict[str, list[int]] = {}
    for row in rows:
        ws_to = tracker._ensure_tab(wb, _tab_of(row["dst"]))
        same = _same_source(ws_to, row["names"])
        if same:
            _merge_layer(wb[row["tab"]], row["row"], ws_to, same)
            report.append(f"merged into {ws_to.title} row {same}, which already listed "
                          f"{'; '.join(row['names'])} (its A-I kept)")
        else:
            _copy_row(wb[row["tab"]], row["row"], ws_to, ws_to.max_row + 1)
        by_tab.setdefault(row["tab"], []).append(row["row"])
    for title, rs in by_tab.items():
        for r in sorted(rs, reverse=True):
            wb[title].delete_rows(r)
    tmp = path.with_name(path.stem + ".tmp.xlsx")
    wb.save(tmp)

    # 3. the files, the links, the log
    for a, b in pairs:
        b.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(a), str(b))
    renames, moves = {}, {}
    for row in rows:
        for name in row["names"]:
            moves[name] = (row["src"], row["dst"])
            for kind in ("synthesis", "clean_md"):
                renames[f"{row['src']}/{kind}/{name}"] = f"{row['dst']}/{kind}/{name}"
    links = _rewrite_links(renames)
    n_log = _rewrite_log(moves)
    os.replace(tmp, path)
    print(tracker.build(path))

    for row in rows:
        report.append(f"{row['src']} -> {row['dst']} ({row['dono']}): {'; '.join(row['names'])}")
    report.append(f"{len(pairs)} files moved, {sum(links.values())} links rewritten in {len(links)} notes, "
                  f"{n_log} log lines")
    return report


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description="Put every source in its owner's folder.")
    ap.add_argument("--move", action="store_true", help="move them (default: only list)")
    ap.add_argument("--file", type=Path, default=tracker.TRACKER, help="another copy of the workbook")
    a = ap.parse_args()
    if a.move:
        print("\n".join(move(a.file)))
    else:
        rows, skipped = plan(openpyxl.load_workbook(a.file, read_only=False))
        for row in rows:
            print(f"{row['src']} -> {row['dst']} ({row['dono']}): {'; '.join(row['names'])}")
        for s in skipped:
            print(f"left alone: {s}")
        print(f"{len(rows)} row(s) out of place" + (" — run with --move" if rows else ""))
