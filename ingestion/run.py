"""
Full ingestion pipeline: inbox PDF -> work (raw + structured) -> agent_bibliography (clean)
                         -> quality report (compare structured vs clean).

Flow:
  ingestion/inbox/<topic>/paper.pdf
    -> ingestion/work/<topic>/paper_raw.md        (raw extraction)
    -> ingestion/work/<topic>/paper_structured.md (formatted intermediate)
    -> agent_bibliography/<topic>/paper.md        (final clean output)
    -> ingestion/compare_report.md                (quality check, newly processed files only)

Skips any PDF whose clean output already exists in agent_bibliography/.
Use --overwrite to force reprocessing.

Models:
  --ingest-model   Claude model for extraction/cleaning (default: claude-haiku-4-5-20251001)
  --verify-model   Claude model for quality verification (default: claude-haiku-4-5-20251001)
  --no-verify      Skip the quality report step

Usage:
    # Process all PDFs in inbox/
    uv run python ingestion/run.py

    # Process a single PDF
    uv run python ingestion/run.py ingestion/inbox/general/paper.pdf

    # Force reprocess everything
    uv run python ingestion/run.py --overwrite

    # Use a different model for verification
    uv run python ingestion/run.py --verify-model claude-sonnet-4-6
"""

import argparse
from pathlib import Path

from ingestion.clean import INGEST_MODEL, clean_file
from ingestion.compare import VERIFY_MODEL, generate_report
from ingestion.extract import extract

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


def process_one(
    pdf: Path,
    topic: str,
    overwrite: bool = False,
    ingest_model: str = INGEST_MODEL,
) -> tuple[Path, Path] | None:
    """
    Run the full pipeline for a single PDF.

    Returns (structured_path, clean_path) if processed, None if skipped.
    Raises on error.
    """
    stem = pdf.stem

    work_dir = WORK / topic if topic else WORK
    bib_dir = BIBLIOGRAPHY / topic if topic else BIBLIOGRAPHY

    clean_out = bib_dir / f"{stem}.md"
    if clean_out.exists() and not overwrite:
        print(f"  skip  (clean output exists — use --overwrite to reprocess)")
        return None

    work_dir.mkdir(parents=True, exist_ok=True)
    bib_dir.mkdir(parents=True, exist_ok=True)

    # Step 1: extract PDF -> raw .md in work/
    raw_out = work_dir / f"{stem}_raw.md"
    print(f"  [1/2] extracting ...")
    chars = extract(pdf, raw_out)
    print(f"        -> {raw_out.name}  ({chars:,} chars)")

    # Step 2: structure + clean (in memory) -> write final to work/, then move to bib/
    print(f"  [2/2] structuring + cleaning ...")
    work_clean = clean_file(raw_out, output_dir=work_dir, model=ingest_model)

    # Move clean output from work/ to agent_bibliography/
    work_clean.rename(clean_out)
    print(f"  done  -> {clean_out.relative_to(ROOT)}")

    return raw_out, clean_out


def run(
    source: Path = INBOX,
    overwrite: bool = False,
    ingest_model: str = INGEST_MODEL,
    verify_model: str = VERIFY_MODEL,
    no_verify: bool = False,
) -> None:
    pdfs = _find_pdfs(source)
    if not pdfs:
        print(f"No PDF files found in: {source}")
        return

    total = len(pdfs)
    processed = skipped = errors = 0
    new_pairs: list[tuple[Path, Path]] = []

    for i, (pdf, topic) in enumerate(pdfs, 1):
        label = f"{topic}/{pdf.name}" if topic else pdf.name
        print(f"\n[{i}/{total}] {label}")
        try:
            result = process_one(pdf, topic, overwrite=overwrite, ingest_model=ingest_model)
            if result is not None:
                processed += 1
                new_pairs.append(result)
            else:
                skipped += 1
        except Exception as e:
            print(f"  ERROR: {e}")
            errors += 1

    print(f"\n{'='*50}")
    print(f"  processed: {processed}  |  skipped: {skipped}  |  errors: {errors}")

    if new_pairs and not no_verify:
        print(f"\n  running quality check on {len(new_pairs)} new file(s) ...")
        report_path = ROOT / "ingestion" / "compare_report.md"
        generate_report(new_pairs, model=verify_model, out_path=report_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingest PDFs: inbox -> work -> agent_bibliography")
    parser.add_argument(
        "source",
        nargs="?",
        default=str(INBOX),
        help="PDF file or folder to process (default: ingestion/inbox/)",
    )
    parser.add_argument("--overwrite", action="store_true", help="Reprocess even if clean output exists")
    parser.add_argument(
        "--ingest-model",
        default=INGEST_MODEL,
        dest="ingest_model",
        help=f"Claude model for extraction/cleaning (default: {INGEST_MODEL})",
    )
    parser.add_argument(
        "--verify-model",
        default=VERIFY_MODEL,
        dest="verify_model",
        help=f"Claude model for quality verification (default: {VERIFY_MODEL})",
    )
    parser.add_argument("--no-verify", action="store_true", dest="no_verify", help="Skip quality report")
    args = parser.parse_args()

    run(
        source=Path(args.source),
        overwrite=args.overwrite,
        ingest_model=args.ingest_model,
        verify_model=args.verify_model,
        no_verify=args.no_verify,
    )
