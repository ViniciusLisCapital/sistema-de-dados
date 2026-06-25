"""
PDF text extractor — converts PDF files to .md (raw text, no AI).

Usage:
    # Single file
    uv run python utils/extract_pdf.py path/to/file.pdf

    # Entire folder (recursive)
    uv run python utils/extract_pdf.py path/to/folder/

    # Folder with custom output directory
    uv run python utils/extract_pdf.py path/to/folder/ --output path/to/output/

    # Overwrite already converted files
    uv run python utils/extract_pdf.py path/to/folder/ --overwrite

As a function:
    from utils.extract_pdf import process
    process("agent_bibliography/general/gestores", output_dir="agent_bibliography/raw/verde")
"""

import argparse
from pathlib import Path

import pdfplumber


def extract(pdf_path: Path, output_path: Path) -> int:
    """Extract text from a single PDF. Returns number of pages with content."""
    pages = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text and text.strip():
                pages.append(text.strip())

    output_path.write_text("\n\n".join(pages), encoding="utf-8")
    return len(pages)


def process(
    source: str | Path,
    output_dir: str | Path | None = None,
    overwrite: bool = False,
    recursive: bool = True,
) -> None:
    """
    Convert one PDF or all PDFs in a folder to .md files.

    Args:
        source:     Path to a PDF file or a folder.
        output_dir: Where to write .md files. Defaults to same folder as each PDF.
        overwrite:  If False, skip files that already have a .md counterpart.
        recursive:  If True, search subfolders as well (only applies when source is a folder).
    """
    source = Path(source)
    output_dir = Path(output_dir) if output_dir else None

    if source.is_file():
        if source.suffix.lower() != ".pdf":
            raise ValueError(f"Not a PDF file: {source}")
        pdfs = [source]
    elif source.is_dir():
        pattern = "**/*.pdf" if recursive else "*.pdf"
        pdfs = sorted(source.glob(pattern))
        if not pdfs:
            print(f"No PDF files found in: {source}")
            return
    else:
        raise FileNotFoundError(f"Path not found: {source}")

    total = len(pdfs)
    for i, pdf_path in enumerate(pdfs, 1):
        dest_dir = output_dir if output_dir else pdf_path.parent
        out = dest_dir / pdf_path.with_suffix(".md").name

        prefix = f"[{i}/{total}]"

        if out.exists() and not overwrite:
            print(f"{prefix}  skip     {pdf_path.name}")
            continue

        dest_dir.mkdir(parents=True, exist_ok=True)

        try:
            pages = extract(pdf_path, out)
            print(f"{prefix}  ok       {pdf_path.name}  ({pages}p) → {out.name}")
        except Exception as e:
            print(f"{prefix}  ERROR    {pdf_path.name}: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert PDF files to .md (raw text extraction, no AI)."
    )
    parser.add_argument("source", help="PDF file or folder path")
    parser.add_argument(
        "--output", "-o",
        default=None,
        help="Output directory (default: same folder as each PDF)",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing .md files (default: skip)",
    )
    parser.add_argument(
        "--no-recursive",
        action="store_true",
        help="Do not search subfolders (default: recursive)",
    )
    args = parser.parse_args()

    process(
        source=args.source,
        output_dir=args.output,
        overwrite=args.overwrite,
        recursive=not args.no_recursive,
    )
