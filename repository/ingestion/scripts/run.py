"""
repository/ingestion/scripts/run.py — the ingestion pipeline, one command.

Workflow: drop a PDF into repository/ingestion/land_space/<topic>/, where
<topic> is one of repository/'s own topic names (exchange_rate,
monetary_policy, fiscal_policy, inflation, ...). Running this script for that
topic:

  1. Extracts the PDF (extract.py: pdfplumber, no AI, no rewriting risk)
  2. Cleans the extracted text (clean_code.py: deterministic regex, no AI —
     no paraphrasing risk, no truncation risk, since no LLM call or token
     budget is involved)
  3. Writes the raw text to   repository/<topic>/raw_md/<name>.md
     Writes the clean text to repository/<topic>/clean_md/<name>.md
     Moves the PDF itself to  repository/<topic>/raw_pdf/<name>.pdf

The drop-zone folder (repository/ingestion/land_space/<topic>/) ends up empty
once its PDFs are ingested — everything ends up organized under
repository/<topic>/.

If repository/<topic>/raw_md/<name>.md already exists, it's preserved (moved
to repository/<topic>/raw_md/_legacy_ai_rewrite/<name>.md) rather than
overwritten — same safety behavior established during the 2026-08 audit that
found an earlier AI-based cleaner had silently corrupted several files.

Usage:
    uv run python repository/ingestion/scripts/run.py                 # every topic folder with PDFs waiting
    uv run python repository/ingestion/scripts/run.py exchange_rate   # just one topic
    uv run python repository/ingestion/scripts/run.py --overwrite     # reprocess even if clean_md already exists
                                                                        # (raw_md/raw_pdf are always legacy-preserved / never silently clobbered)
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from clean_code import clean
from extract import extract as extract_pdf

SCRIPTS = Path(__file__).resolve().parent   # repository/ingestion/scripts/
INGESTION = SCRIPTS.parent                  # repository/ingestion/
REPOSITORY = INGESTION.parent                # repository/
ROOT = REPOSITORY.parent                     # project root
LAND_SPACE = INGESTION / "land_space"        # repository/ingestion/land_space/


def _topic_dirs(only: str | None = None) -> list[Path]:
    if only:
        d = LAND_SPACE / only
        return [d] if d.is_dir() else []
    if not LAND_SPACE.is_dir():
        return []
    return sorted(
        d for d in LAND_SPACE.iterdir()
        if d.is_dir() and not d.name.startswith((".", "_"))
    )


def ingest_one(pdf_path: Path, topic: str, overwrite: bool = False) -> None:
    name = pdf_path.stem

    raw_dir = REPOSITORY / topic / "raw_md"
    clean_dir = REPOSITORY / topic / "clean_md"
    pdf_dir = REPOSITORY / topic / "raw_pdf"
    for d in (raw_dir, clean_dir, pdf_dir):
        d.mkdir(parents=True, exist_ok=True)

    raw_dest = raw_dir / f"{name}.md"
    clean_dest = clean_dir / f"{name}.md"
    pdf_dest = pdf_dir / pdf_path.name

    # Never silently overwrite an existing raw_md — move it to a clearly
    # labeled legacy holding spot first, exactly once.
    if raw_dest.exists():
        legacy_dir = raw_dir / "_legacy_ai_rewrite"
        legacy_dir.mkdir(parents=True, exist_ok=True)
        legacy_dest = legacy_dir / f"{name}.md"
        if not legacy_dest.exists():
            raw_dest.replace(legacy_dest)
            print(f"        legacy    existing raw_md moved -> {legacy_dest.relative_to(ROOT)}")

    print(f"        extracting ...")
    chars = extract_pdf(pdf_path, raw_dest)
    print(f"        raw_md    {chars:,} chars -> {raw_dest.relative_to(ROOT)}")

    if clean_dest.exists() and not overwrite:
        print(f"        skip      clean_md exists (use --overwrite to replace)")
    else:
        raw_text = raw_dest.read_text(encoding="utf-8")
        cleaned = clean(raw_text)
        clean_dest.write_text(cleaned, encoding="utf-8")
        reduction = 100 * (1 - len(cleaned) / len(raw_text)) if raw_text else 0
        print(f"        clean_md  {len(raw_text):,} -> {len(cleaned):,} chars  ({reduction:.0f}% removed) -> {clean_dest.relative_to(ROOT)}")

    if pdf_dest.exists() and pdf_dest != pdf_path:
        print(f"        raw_pdf   already exists at destination, leaving source PDF in the drop zone: {pdf_dest.relative_to(ROOT)}")
    else:
        pdf_path.replace(pdf_dest)
        print(f"        raw_pdf   -> {pdf_dest.relative_to(ROOT)}")


def run(only: str | None = None, overwrite: bool = False) -> None:
    topic_dirs = _topic_dirs(only)
    if not topic_dirs:
        print(f"No topic folder found" + (f" named '{only}'" if only else " in repository/ingestion/land_space/"))
        return

    pdfs = [(p, d.name) for d in topic_dirs for p in sorted(d.glob("*.pdf"))]
    if not pdfs:
        where = only if only else "any repository/ingestion/land_space/<topic>/ folder"
        print(f"No PDFs waiting in {where}.")
        return

    total = len(pdfs)
    for i, (pdf_path, topic) in enumerate(pdfs, 1):
        print(f"\n[{i}/{total}] {topic}/{pdf_path.name}")
        try:
            ingest_one(pdf_path, topic, overwrite=overwrite)
        except Exception as e:
            print(f"        ERROR: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingest PDFs sitting in repository/ingestion/land_space/<topic>/ into repository/<topic>/{raw_pdf,raw_md,clean_md}/.")
    parser.add_argument("topic", nargs="?", default=None, help="Process only this topic folder (default: every topic folder with PDFs waiting)")
    parser.add_argument("--overwrite", action="store_true", help="Reprocess clean_md even if it already exists (raw_md/raw_pdf are always legacy-preserved, never silently overwritten)")
    args = parser.parse_args()

    run(only=args.topic, overwrite=args.overwrite)
