"""
Code-only ingestion test runner.

Reads *_raw.md files from a given source folder and applies the
deterministic code-only cleaner (clean_code.py, no AI calls), preserving
topic subfolder structure in the output — a staging area for inspecting
clean_code.py's output before it's actually published into
repository/<topic>/clean_md/ via publish.py or run.py.

This is a lower-level inspection tool, not part of the normal one-command
flow — for ingesting a brand-new PDF, use run.py instead.

Usage:
    uv run python repository/ingestion/scripts/run_code.py <source_folder> <output_folder>
    uv run python repository/ingestion/scripts/run_code.py <source_folder> <output_folder> --overwrite
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from clean_code import clean_file

SCRIPTS = Path(__file__).resolve().parent   # repository/ingestion/scripts/
INGESTION = SCRIPTS.parent                  # repository/ingestion/
REPOSITORY = INGESTION.parent                # repository/
ROOT = REPOSITORY.parent                     # project root


def run(source: Path, output: Path, overwrite: bool = False) -> None:
    raw_files = sorted(source.rglob("*_raw.md"))
    if not raw_files:
        print(f"No *_raw.md files found in: {source}")
        return

    processed = skipped = errors = 0

    for raw in raw_files:
        # Infer topic from immediate subfolder under source
        try:
            rel = raw.relative_to(source)
            topic = rel.parts[0] if len(rel.parts) > 1 else ""
        except ValueError:
            topic = ""

        out_dir = output / topic if topic else output
        stem = raw.stem[:-4] if raw.stem.endswith("_raw") else raw.stem
        out_path = out_dir / f"{stem}.md"

        label = f"{topic}/{raw.name}" if topic else raw.name
        print(f"\n{label}")

        if out_path.exists() and not overwrite:
            print(f"  skip  (exists — use --overwrite to replace)")
            skipped += 1
            continue

        try:
            result = clean_file(raw, output_dir=out_dir)
            original = len(raw.read_text(encoding="utf-8"))
            cleaned = len(result.read_text(encoding="utf-8"))
            reduction = 100 * (1 - cleaned / original) if original else 0
            print(f"  ok    {original:,} -> {cleaned:,} chars  ({reduction:.0f}% removed)  -> {result}")
            processed += 1
        except Exception as e:
            print(f"  ERROR: {e}")
            errors += 1

    print(f"\n{'='*50}")
    print(f"  processed: {processed}  |  skipped: {skipped}  |  errors: {errors}")
    print(f"  output: {output}/")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Code-only cleaner: <source>/*_raw.md -> <output>/")
    parser.add_argument("source", help="Folder to scan recursively for *_raw.md files")
    parser.add_argument("output", help="Folder to write cleaned output to (topic subfolder structure preserved)")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing outputs")
    args = parser.parse_args()
    run(source=Path(args.source), output=Path(args.output), overwrite=args.overwrite)
