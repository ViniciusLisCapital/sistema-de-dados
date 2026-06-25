"""
Full ingestion pipeline: inbox PDF -> work (raw + structured + report) -> agent_bibliography (clean).

Flow:
  ingestion/inbox/<topic>/paper.pdf
    -> ingestion/work/<topic>/paper_raw.md        (raw extraction)
    -> ingestion/work/<topic>/paper_structured.md (formatted intermediate)
    -> ingestion/work/<topic>/paper_report.json   (boilerplate report)
    -> agent_bibliography/<topic>/paper.md        (final output)

Skips any PDF whose clean output already exists in agent_bibliography/.
Use --overwrite to force reprocessing.

Usage:
    # Process all PDFs in inbox/
    uv run python ingestion/run.py

    # Process a single PDF
    uv run python ingestion/run.py ingestion/inbox/general/paper.pdf

    # Force reprocess everything
    uv run python ingestion/run.py --overwrite
"""

import argparse
from pathlib import Path

from ingestion.extract import extract
from ingestion.clean import clean_file

ROOT = Path(__file__).parent.parent
INBOX = ROOT / "ingestion" / "inbox"
WORK = ROOT / "ingestion" / "work"
BIBLIOGRAPHY = ROOT / "agent_bibliography"


def _find_pdfs(source: Path) -> list[tuple[Path, str]]:
    """
    Return list of (pdf_path, topic) tuples.
    Topic is the immediate subfolder name under inbox/, or '' if at inbox root.
    """
    if source.is_file():
        topic = source.parent.name if source.parent != INBOX else ""
        return [(source, topic)]

    pdfs = sorted(source.rglob("*.pdf"))
    result = []
    for pdf in pdfs:
        rel = pdf.relative_to(source)
        topic = rel.parts[0] if len(rel.parts) > 1 else ""
        result.append((pdf, topic))
    return result


def process_one(pdf: Path, topic: str, overwrite: bool = False) -> bool:
    """
    Run the full pipeline for a single PDF.
    Returns True if processed, False if skipped.
    """
    stem = pdf.stem

    # Resolve output dirs
    work_dir = WORK / topic if topic else WORK
    bib_dir = BIBLIOGRAPHY / topic if topic else BIBLIOGRAPHY

    clean_out = bib_dir / f"{stem}.md"
    if clean_out.exists() and not overwrite:
        print(f"  skip  (clean output exists — use --overwrite to reprocess)")
        return False

    work_dir.mkdir(parents=True, exist_ok=True)
    bib_dir.mkdir(parents=True, exist_ok=True)

    # Step 1: extract PDF -> raw .md in work/
    raw_out = work_dir / f"{stem}_raw.md"
    print(f"  [1/3] extracting ...")
    chars = extract(pdf, raw_out)
    print(f"        -> {raw_out.name}  ({chars:,} chars)")

    # Steps 2-4: structure + identify + clean -> work/ and bibliography/
    # structured and report go to work/, clean goes to bib/
    print(f"  [2/3] structuring ...")
    print(f"  [3/3] identifying + cleaning ...")
    clean_file(raw_out, output_dir=work_dir)

    # Move clean output from work/ to agent_bibliography/
    work_clean = work_dir / f"{stem}.md"
    work_clean.rename(clean_out)
    print(f"  done  -> {clean_out.relative_to(ROOT)}")
    return True


def run(source: Path = INBOX, overwrite: bool = False) -> None:
    pdfs = _find_pdfs(source)
    if not pdfs:
        print(f"No PDF files found in: {source}")
        return

    total = len(pdfs)
    processed = skipped = errors = 0

    for i, (pdf, topic) in enumerate(pdfs, 1):
        label = f"{topic}/{pdf.name}" if topic else pdf.name
        print(f"\n[{i}/{total}] {label}")
        try:
            ok = process_one(pdf, topic, overwrite=overwrite)
            if ok:
                processed += 1
            else:
                skipped += 1
        except Exception as e:
            print(f"  ERROR: {e}")
            errors += 1

    print(f"\n{'='*50}")
    print(f"  processed: {processed}  |  skipped: {skipped}  |  errors: {errors}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingest PDFs: inbox -> work -> agent_bibliography")
    parser.add_argument(
        "source",
        nargs="?",
        default=str(INBOX),
        help="PDF file or folder to process (default: ingestion/inbox/)",
    )
    parser.add_argument("--overwrite", action="store_true", help="Reprocess even if clean output exists")
    args = parser.parse_args()

    run(source=Path(args.source), overwrite=args.overwrite)
