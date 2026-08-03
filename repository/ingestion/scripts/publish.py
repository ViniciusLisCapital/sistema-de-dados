"""
repository/ingestion/scripts/publish.py — Publish an existing *_raw.md (raw
extraction, not yet a PDF) into repository/<topic>/raw_md/ and clean_md/,
without re-extracting.

Lower-level tool for a *_raw.md file that already exists by some other means
(e.g. hand-run extract.py output, or a one-off recovered extraction). For
ingesting a brand-new PDF, use run.py in this same folder instead — drop the
PDF in repository/ingestion/land_space/<topic>/ and run it; that does
extraction + cleaning + this publish step in one pass. There is no default
input folder — pass a *_raw.md file or a folder to scan recursively.

  1. Writes the raw text, _raw suffix stripped, to
     repository/<topic>/raw_md/<name>.md — if a file already exists at that
     path, it is moved (never overwritten in place) to
     repository/<topic>/raw_md/_legacy_ai_rewrite/<name>.md first, so nothing
     already there is silently lost.
  2. Runs the deterministic, non-AI cleaner (clean_code.py) over the raw text
     and writes the result to repository/<topic>/clean_md/<name>.md. This is a
     pure regex pass — no paraphrasing, no truncation risk, since no LLM call
     or token budget is involved.

Usage:
    uv run python repository/ingestion/scripts/publish.py <folder>               # publish every *_raw.md found recursively
    uv run python repository/ingestion/scripts/publish.py <topic>/some_raw.md    # publish a single file
    uv run python repository/ingestion/scripts/publish.py <folder> --overwrite   # re-publish even if clean_md already exists
                                                                                  # (raw_md is always legacy-preserved, never silently overwritten)
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from clean_code import clean

SCRIPTS = Path(__file__).resolve().parent   # repository/ingestion/scripts/
INGESTION = SCRIPTS.parent                  # repository/ingestion/
REPOSITORY = INGESTION.parent                # repository/
ROOT = REPOSITORY.parent                     # project root


def _base_name(raw_path: Path) -> str:
    """_raw suffix stripped, plus trailing comma/whitespace normalized (a
    known artifact from one source PDF's filename, e.g. 'Paiva, 2006), ')."""
    stem = raw_path.stem
    if stem.endswith("_raw"):
        stem = stem[:-4]
    return stem.rstrip(" ,")


def publish_one(raw_path: Path, topic: str, overwrite: bool = False) -> tuple[Path, Path]:
    """
    Publish a single ingestion/work/<topic>/<name>_raw.md into
    repository/<topic>/raw_md/ and repository/<topic>/clean_md/.

    Returns (raw_dest, clean_dest).
    """
    name = _base_name(raw_path)
    raw_dir = REPOSITORY / topic / "raw_md"
    clean_dir = REPOSITORY / topic / "clean_md"
    raw_dir.mkdir(parents=True, exist_ok=True)
    clean_dir.mkdir(parents=True, exist_ok=True)

    raw_dest = raw_dir / f"{name}.md"
    clean_dest = clean_dir / f"{name}.md"

    raw_text = raw_path.read_text(encoding="utf-8")

    # Never silently overwrite an existing raw_md — move it to a clearly
    # labeled legacy holding spot first, exactly once.
    if raw_dest.exists():
        legacy_dir = raw_dir / "_legacy_ai_rewrite"
        legacy_dir.mkdir(parents=True, exist_ok=True)
        legacy_dest = legacy_dir / f"{name}.md"
        if not legacy_dest.exists():
            raw_dest.replace(legacy_dest)
            print(f"        legacy   existing raw_md moved -> {legacy_dest.relative_to(ROOT)}")

    raw_dest.write_text(raw_text, encoding="utf-8")

    if clean_dest.exists() and not overwrite:
        print(f"        skip     clean_md exists (use --overwrite to replace)")
    else:
        cleaned = clean(raw_text)
        clean_dest.write_text(cleaned, encoding="utf-8")
        reduction = 100 * (1 - len(cleaned) / len(raw_text)) if raw_text else 0
        print(f"        clean_md {len(raw_text):,} -> {len(cleaned):,} chars  ({reduction:.0f}% removed)")

    return raw_dest, clean_dest


def run(source: Path, overwrite: bool = False) -> None:
    if source.is_file():
        raw_files = [source]
    else:
        raw_files = sorted(source.rglob("*_raw.md"))

    if not raw_files:
        print(f"No *_raw.md files found in: {source}")
        return

    total = len(raw_files)
    for i, raw_path in enumerate(raw_files, 1):
        if source.is_file():
            # No folder to infer a topic from — the file's own immediate
            # parent folder name is the topic (e.g. .../exchange_rate/some_raw.md).
            topic = raw_path.parent.name
        else:
            try:
                rel = raw_path.relative_to(source)
                topic = rel.parts[0] if len(rel.parts) > 1 else ""
            except ValueError:
                topic = ""

        if not topic:
            print(f"\n[{i}/{total}] {raw_path.name}  SKIPPED (no topic subfolder found — place under <source>/<topic>/)")
            continue

        label = f"{topic}/{raw_path.name}"
        print(f"\n[{i}/{total}] {label}")
        raw_dest, clean_dest = publish_one(raw_path, topic, overwrite=overwrite)
        print(f"        -> {raw_dest.relative_to(ROOT)}")
        print(f"        -> {clean_dest.relative_to(ROOT)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Publish an existing *_raw.md extraction into repository/<topic>/raw_md/ and clean_md/.")
    parser.add_argument("source", help="A single *_raw.md file (topic = its parent folder name), or a folder of <topic>/*_raw.md to scan recursively")
    parser.add_argument("--overwrite", action="store_true", help="Re-publish clean_md even if it already exists (raw_md is always legacy-preserved, never overwritten)")
    args = parser.parse_args()

    run(source=Path(args.source), overwrite=args.overwrite)
