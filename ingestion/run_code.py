"""
Code-only ingestion test runner.

Reads all *_raw.md files already in ingestion/work/ and applies the
deterministic code-only cleaner (no AI calls). Outputs to ingestion/test/
preserving topic subfolder structure, for comparison with the AI pipeline.

Usage:
    uv run python ingestion/run_code.py
    uv run python ingestion/run_code.py --overwrite
"""

import argparse
from pathlib import Path

from ingestion.clean_code import clean_file

ROOT = Path(__file__).parent.parent
WORK = ROOT / "ingestion" / "work"
TEST = ROOT / "ingestion" / "test"


def run(overwrite: bool = False) -> None:
    raw_files = sorted(WORK.rglob("*_raw.md"))
    if not raw_files:
        print(f"No *_raw.md files found in: {WORK}")
        return

    processed = skipped = errors = 0

    for raw in raw_files:
        # Infer topic from immediate subfolder under work/
        try:
            rel = raw.relative_to(WORK)
            topic = rel.parts[0] if len(rel.parts) > 1 else ""
        except ValueError:
            topic = ""

        out_dir = TEST / topic if topic else TEST
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
            print(f"  ok    {original:,} -> {cleaned:,} chars  ({reduction:.0f}% removed)  -> {result.relative_to(ROOT)}")
            processed += 1
        except Exception as e:
            print(f"  ERROR: {e}")
            errors += 1

    print(f"\n{'='*50}")
    print(f"  processed: {processed}  |  skipped: {skipped}  |  errors: {errors}")
    print(f"  output: {TEST.relative_to(ROOT)}/")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Code-only cleaner: work/_raw.md -> test/")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing outputs")
    args = parser.parse_args()
    run(overwrite=args.overwrite)
