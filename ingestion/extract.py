"""
Step 1 — Extract text from PDF (and plain text) files into raw .md.

Wraps pdfplumber for PDFs and passes .txt/.md files through unchanged.
Output files land in a `raw/` sub-directory relative to the source,
or in the explicit output_dir you pass.

Usage (CLI):
    uv run python ingestion/extract.py ingestion/sample/teste.pdf
    uv run python ingestion/extract.py ingestion/sample/ --output ingestion/sample/raw/

As a function:
    from ingestion.extract import process
    raw_path = process("ingestion/sample/teste.pdf", output_dir="ingestion/sample/raw")
"""

import argparse
from pathlib import Path

import pdfplumber


SUPPORTED = {".pdf", ".txt", ".md"}


def _extract_pdf(path: Path) -> str:
    pages = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text and text.strip():
                pages.append(text.strip())
    return "\n\n".join(pages)


def _extract_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def extract(source: Path, dest: Path) -> int:
    """
    Convert a single file to .md. Returns character count of extracted text.
    dest should already have the .md extension.
    """
    suffix = source.suffix.lower()
    if suffix == ".pdf":
        text = _extract_pdf(source)
    elif suffix in {".txt", ".md"}:
        text = _extract_text(source)
    else:
        raise ValueError(f"Unsupported file type: {suffix}")

    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(text, encoding="utf-8")
    return len(text)


def process(
    source: str | Path,
    output_dir: str | Path | None = None,
    overwrite: bool = False,
    recursive: bool = True,
) -> Path | None:
    """
    Extract one file or all supported files in a folder to raw .md.

    Returns the output path for a single-file call, None for folder calls.
    """
    source = Path(source)

    if source.is_file():
        pdfs = [source]
    elif source.is_dir():
        pattern = "**/*" if recursive else "*"
        pdfs = sorted(p for p in source.glob(pattern) if p.suffix.lower() in SUPPORTED and p.is_file())
        if not pdfs:
            print(f"No supported files found in: {source}")
            return None
    else:
        raise FileNotFoundError(f"Path not found: {source}")

    result = None
    total = len(pdfs)

    for i, src in enumerate(pdfs, 1):
        if output_dir:
            dest_dir = Path(output_dir)
        else:
            dest_dir = src.parent / "raw"

        out = dest_dir / src.with_suffix(".md").name
        prefix = f"[{i}/{total}]"

        if out.exists() and not overwrite:
            print(f"{prefix}  skip     {src.name}  (use --overwrite to replace)")
            result = out
            continue

        try:
            chars = extract(src, out)
            print(f"{prefix}  ok       {src.name}  ({chars:,} chars) -> {out}")
            result = out
        except Exception as e:
            print(f"{prefix}  ERROR    {src.name}: {e}")

    return result if total == 1 else None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract text from PDF/text files to raw .md.")
    parser.add_argument("source", help="File or folder path")
    parser.add_argument("--output", "-o", default=None, help="Output directory")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing .md files")
    parser.add_argument("--no-recursive", action="store_true", help="Do not recurse into subfolders")
    args = parser.parse_args()

    process(
        source=args.source,
        output_dir=args.output,
        overwrite=args.overwrite,
        recursive=not args.no_recursive,
    )
