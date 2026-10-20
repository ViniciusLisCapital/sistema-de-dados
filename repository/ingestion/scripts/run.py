"""
repository/ingestion/scripts/run.py — the ingestion pipeline's sweep and commit step.

Workflow (SISTEMA_AGENTES.md II.I.iv): a PDF is saved straight into
repository/<topic>/raw_pdf/ (top level). A PDF there with no raw_md/<name>.md is
pending; `/ingest [topic]` hands the pending ones to the ingestion agent, which picks
the extraction settings with qc.py, checks the candidate against the PDF pages, and
then runs this script to write the result:

  1. Extracts the PDF (extract.py, with the file's entry in settings.yaml or the default)
  2. Cleans the text (clean_code.py: deterministic regex, no AI)
  3. Writes  repository/<topic>/raw_md/<name>.md
             obsidian/<topic>/clean_md/<name>.md
  4. Appends one line to repository/ingestion/LOG.md
  5. Updates the literature tracker (tracker.py → repository/agent_mapping/data_tracker.xlsx)

The PDF never moves. Every character of raw_md and clean_md comes from the tools, so a
re-run on the same PDF with the same settings reproduces both files (qc.py check).

Only the top level of raw_pdf/ is swept: monetary_policy/raw_pdf/central_bank/ belongs
to the Copom ETL, and repository/mental_model/ (manager letters) has its own pipeline.

Guards — each one stops that file and says why, the rest continue:
  - the topic must be a folder of repository/, and not on hold (settings.yaml);
  - the file name must follow `description_in_snake_case (Author, Year).pdf`;
  - the same file name in another topic's raw_pdf/ is a duplicate;
  - a file marked `status: needs_attention` in settings.yaml is not retried;
  - blocking QC flags (no text layer, garbled, letter-spaced, run-together) stop the
    write unless --accept-flags;
  - an existing raw_md/clean_md is not replaced unless --overwrite.

Usage:
    uv run python repository/ingestion/scripts/run.py --list                     # what is pending, every topic
    uv run python repository/ingestion/scripts/run.py --list monetary_policy
    uv run python repository/ingestion/scripts/run.py monetary_policy "taylor_rule (Taylor, 1993).pdf"
    uv run python repository/ingestion/scripts/run.py monetary_policy "taylor_rule (Taylor, 1993).pdf" --overwrite
    uv run python repository/ingestion/scripts/run.py --reclean       # after a cleaner change
"""

import argparse
import datetime as dt
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from extract import pages_text  # noqa: E402
from qc import evaluate  # noqa: E402
from settings import DEFAULT, settings_for, status_for, topics_on_hold  # noqa: E402

SCRIPTS = Path(__file__).resolve().parent
INGESTION = SCRIPTS.parent
REPOSITORY = INGESTION.parent
ROOT = REPOSITORY.parent
OBSIDIAN = ROOT / "obsidian"
LOG = INGESTION / "LOG.md"

NAME_RE = re.compile(r"^[a-z0-9_]+ \([^()]+, \d{4}[a-z]?\)$")
BLOCKING = ("no_text_layer", "garbled", "letter_spaced", "run_together")
_NOT_TOPICS = {"ingestion", "agent_mapping", "mental_model"}


def topics() -> list[str]:
    return sorted(d.name for d in REPOSITORY.iterdir()
                  if d.is_dir() and not d.name.startswith((".", "_")) and d.name not in _NOT_TOPICS)


def paths(topic: str, name: str) -> dict[str, Path]:
    """name = file stem, without .pdf."""
    return {
        "pdf": REPOSITORY / topic / "raw_pdf" / f"{name}.pdf",
        "raw": REPOSITORY / topic / "raw_md" / f"{name}.md",
        "clean": OBSIDIAN / topic / "clean_md" / f"{name}.md",
    }


def scan(topic: str) -> list[dict]:
    """Every PDF at the top level of raw_pdf/, with its state:
    ingested · pending · needs_attention · on_hold."""
    hold = topics_on_hold().get(topic)
    out = []
    for pdf in sorted((REPOSITORY / topic / "raw_pdf").glob("*.pdf")):
        p = paths(topic, pdf.stem)
        st = status_for(pdf.name)
        if p["raw"].exists() and p["clean"].exists():
            state, note = "ingested", ""
        elif hold:
            state, note = "on_hold", hold
        elif st:
            state, note = st
        else:
            state, note = "pending", "" if NAME_RE.match(pdf.stem) else "name to fix"
        out.append({"topic": topic, "file": pdf.name, "name": pdf.stem, "state": state, "note": note})
    return out


def _log(row: list[str]) -> None:
    if not LOG.exists():
        LOG.write_text(
            "# Ingestion log\n\nOne line per file written by `run.py` (newest last). Settings "
            "\"default\" = plumber, x_tolerance 1.5.\n\n"
            "| date | topic | file | settings | pages | raw chars | removed | flags |\n"
            "|---|---|---|---|---|---|---|---|\n", encoding="utf-8")
    with LOG.open("a", encoding="utf-8") as f:
        f.write("| " + " | ".join(row) + " |\n")


def ingest_one(topic: str, file_name: str, overwrite: bool, accept_flags: bool) -> str:
    name = Path(file_name).stem
    p = paths(topic, name)
    if not p["pdf"].exists():
        return f"SKIP not found: {p['pdf'].relative_to(ROOT)}"
    if not NAME_RE.match(name):
        return "SKIP name does not follow 'description (Author, Year).pdf' — rename it in raw_pdf/ first"
    others = [t for t in topics() if t != topic and (REPOSITORY / t / "raw_pdf" / p["pdf"].name).exists()]
    if others:
        return f"SKIP duplicate: the same file is in {', '.join(others)}/raw_pdf/"
    st = status_for(p["pdf"].name)
    if st:
        return f"SKIP marked {st[0]} in settings.yaml: {st[1]}"
    if (p["raw"].exists() or p["clean"].exists()) and not overwrite:
        return "SKIP already ingested (use --overwrite to redo it)"

    s = settings_for(p["pdf"].name)
    res, raw, cleaned = evaluate(pages_text(p["pdf"], s["mode"], s["x_tolerance"], s["decode_shift"]))
    blocking = [f for f in res["flags"] if f.startswith(BLOCKING)]
    if blocking and not accept_flags:
        return "STOP blocking QC flags, nothing written: " + "; ".join(blocking)

    for d in (p["raw"].parent, p["clean"].parent):
        d.mkdir(parents=True, exist_ok=True)
    p["raw"].write_text(raw, encoding="utf-8")
    p["clean"].write_text(cleaned, encoding="utf-8")

    setting_txt = "default" if s == DEFAULT else ", ".join(f"{k} {v}" for k, v in s.items() if v != DEFAULT[k])
    _log([dt.date.today().isoformat(), topic, name, setting_txt, str(res["pages"]),
          f"{res['chars']:,}", f"{res['removed_pct']}%", "; ".join(res["flags"]) or "—"])
    return (f"OK   raw {res['chars']:,} chars, clean {res['clean_chars']:,} ({res['removed_pct']}% removed)"
            + (f"\n     flags: {'; '.join(res['flags'])}" if res["flags"] else ""))


def cmd_reclean(only: str | None) -> None:
    """Rewrite every ingested clean_md from its raw_md with the current cleaner. For a cleaner
    change: the raw_md (the audit trail) is not touched and no PDF is re-extracted."""
    from clean_code import clean
    for t in ([only] if only else topics()):
        changed = 0
        for r in scan(t):
            if r["state"] != "ingested":
                continue
            p = paths(t, r["name"])
            new = clean(p["raw"].read_text(encoding="utf-8"))
            if new != p["clean"].read_text(encoding="utf-8"):
                p["clean"].write_text(new, encoding="utf-8")
                changed += 1
                _log([dt.date.today().isoformat(), t, r["name"], "reclean (cleaner change)", "", "", "", "—"])
        print(f"{t}: {changed} clean_md rewritten")


def cmd_list(only: str | None) -> None:
    for t in ([only] if only else topics()):
        rows = scan(t)
        if not rows:
            continue
        count = {s: sum(1 for r in rows if r["state"] == s) for s in ("ingested", "pending", "needs_attention", "on_hold")}
        print(f"{t}: {len(rows)} PDFs · " + " · ".join(f"{k.replace('_', ' ')} {v}" for k, v in count.items() if v))
        if t in topics_on_hold():
            print(f"   on hold: {topics_on_hold()[t]}")
        for r in rows:
            if r["state"] not in ("ingested", "on_hold"):
                print(f"   {r['state']:16s} {r['file']}" + (f"  — {r['note']}" if r["note"] else ""))


def main() -> None:
    ap = argparse.ArgumentParser(description="Sweep repository/<topic>/raw_pdf/ for PDFs not yet ingested, and write them.")
    ap.add_argument("topic", nargs="?")
    ap.add_argument("names", nargs="*", help="PDF file names in repository/<topic>/raw_pdf/")
    ap.add_argument("--list", action="store_true", help="list the state of every PDF (all topics, or the one given)")
    ap.add_argument("--overwrite", action="store_true", help="redo a file that is already ingested")
    ap.add_argument("--accept-flags", action="store_true", help="write even with blocking QC flags (after checking the pages)")
    ap.add_argument("--reclean", action="store_true", help="after a cleaner change: rewrite every clean_md from its raw_md")
    a = ap.parse_args()

    if a.topic and a.topic not in topics():
        sys.exit(f"unknown topic {a.topic!r}; existing: {', '.join(topics())}")
    if a.list:
        cmd_list(a.topic)
        return
    if a.reclean:
        cmd_reclean(a.topic)
        return
    if not a.topic or not a.names:
        sys.exit("give a topic and the file names to write (or --list to see what is pending)")
    if a.topic in topics_on_hold():
        sys.exit(f"{a.topic} is on hold: {topics_on_hold()[a.topic]}")
    for i, n in enumerate(a.names, 1):
        print(f"[{i}/{len(a.names)}] {n}")
        try:
            print("     " + ingest_one(a.topic, n, a.overwrite, a.accept_flags))
        except Exception as e:  # noqa: BLE001 — one bad file must not stop the rest
            print(f"     ERROR {e!r}")
    try:
        from tracker import build
        print("tracker: " + build())
    except Exception as e:  # noqa: BLE001 — the tracker never costs an ingestion
        print(f"tracker NOT updated: {e!r}")


if __name__ == "__main__":
    main()
