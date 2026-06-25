"""
Step 2 — AI cleaning agent (2-pass pipeline, no intermediate files).

Pass 1 — Structure: reformats raw extracted text into clean markdown in memory,
          fixes PDF encoding artifacts, marks obvious boilerplate with
          > [BOILERPLATE] blockquotes.
Pass 2 — Clean: identifies and removes all boilerplate. Writes the final file.

Output:
  <name>.md  — final cleaned document (written to output_dir)

Usage (CLI):
    uv run python ingestion/clean.py ingestion/sample/raw/teste.md
    uv run python ingestion/clean.py ingestion/sample/raw/ --output ingestion/sample/clean/

As a function:
    from ingestion.clean import clean_file
    clean_path = clean_file("ingestion/sample/raw/teste.md", output_dir="ingestion/sample/clean")
"""

import argparse
import os
from pathlib import Path

import anthropic
from dotenv import load_dotenv

load_dotenv()

INGEST_MODEL = "claude-haiku-4-5-20251001"
MAX_CHARS = 180_000  # ~45k tokens — truncates only extremely long docs

_STRUCTURE_PROMPT = """\
You are a document structuring assistant. The text below was extracted raw from a PDF and may contain:
- Garbled, reversed, or corrupted text (PDF encoding artifacts)
- Missing paragraph breaks or run-on sentences from page joins
- Page number artifacts and repeated headers mixed into the content
- Inconsistent spacing and formatting

Your task: reformat the text into clean, readable markdown. Rules:
1. Add proper headers (## for main sections, ### for subsections) inferred from the document's structure.
2. Fix obvious encoding artifacts — e.g., reversed text, broken Unicode sequences, obfuscated strings.
3. Separate paragraphs with blank lines. Merge broken lines that belong to the same sentence.
4. Mark boilerplate by wrapping it in a blockquote prefixed with [BOILERPLATE]:
   > [BOILERPLATE] <original text of the section>
   Boilerplate includes: disclaimers, legal notices, copyright, regulatory disclosures,
   contact details (phone numbers, email addresses), analyst certification statements,
   "about the author/company" sections, table of contents, blank filler pages.
5. Do NOT remove any content — only restructure and mark.
6. Return only the structured markdown. No commentary, no preamble.

Document:
---
{text}
---"""

_CLEAN_PROMPT = """\
You are a document cleaning assistant. The structured text below was extracted from a PDF.
Sections marked with > [BOILERPLATE] are candidates for removal.

Your task: remove all boilerplate and return ONLY the cleaned document.

Boilerplate to remove:
- Any section marked with > [BOILERPLATE]
- Table of contents / index
- Disclaimers and legal notices
- Repeated page headers/footers (page numbers, document title artifacts)
- Copyright / publisher information
- Contact details: phone numbers, email addresses, analyst names with contact info
- "About the author" or "About the company" sections
- References / bibliography that is just a citation list (no annotation)
- Regulatory certifications and compliance statements

Return ONLY the cleaned document. No commentary, no preamble.
Keep all substantive content intact and in order. Preserve the markdown structure (headers, paragraphs).

Document:
---
{text}
---"""


def _call(client: anthropic.Anthropic, model: str, prompt: str, max_tokens: int = 8096) -> str:
    msg = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        messages=[{"role": "user", "content": prompt}],
    )
    return msg.content[0].text.strip()


def clean_file(
    source: str | Path,
    output_dir: str | Path | None = None,
    model: str = INGEST_MODEL,
) -> Path:
    """
    Run the 2-pass pipeline on a single raw .md file.
    Structure pass runs in memory; only the final clean file is written.

    Returns clean_path.
    """
    source = Path(source)
    if not source.exists():
        raise FileNotFoundError(source)

    text = source.read_text(encoding="utf-8")
    if len(text) > MAX_CHARS:
        print(f"  [warn] document truncated to {MAX_CHARS:,} chars for analysis")
        text = text[:MAX_CHARS]

    dest_dir = Path(output_dir) if output_dir else source.parent
    dest_dir.mkdir(parents=True, exist_ok=True)

    stem = source.stem
    base = stem[:-4] if stem.endswith("_raw") else stem  # strip _raw suffix for output names
    clean_path = dest_dir / f"{base}.md"

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise EnvironmentError("ANTHROPIC_API_KEY not set in environment / .env")

    client = anthropic.Anthropic(api_key=api_key)

    # Pass 1: structure (in memory)
    structured = _call(client, model, _STRUCTURE_PROMPT.replace("{text}", text))
    print(f"        structured: {len(structured):,} chars (in memory)")

    # Pass 2: clean (identify + remove boilerplate, write final file)
    cleaned = _call(client, model, _CLEAN_PROMPT.replace("{text}", structured))
    clean_path.write_text(cleaned, encoding="utf-8")
    print(f"        cleaned:    {len(cleaned):,} chars -> {clean_path.name}")

    return clean_path


def process(
    source: str | Path,
    output_dir: str | Path | None = None,
    overwrite: bool = False,
    model: str = INGEST_MODEL,
) -> None:
    """Clean one .md file or all .md files in a folder."""
    source = Path(source)

    if source.is_file():
        files = [source]
    elif source.is_dir():
        files = sorted(f for f in source.glob("*.md") if not f.stem.endswith("_structured"))
        if not files:
            print(f"No .md files found in: {source}")
            return
    else:
        raise FileNotFoundError(f"Path not found: {source}")

    total = len(files)
    for i, f in enumerate(files, 1):
        print(f"\n[{i}/{total}] {f.name}")
        dest = Path(output_dir) if output_dir else f.parent
        base = f.stem[:-4] if f.stem.endswith("_raw") else f.stem
        clean_path = dest / f"{base}.md"
        if clean_path.exists() and not overwrite:
            print(f"  skip (use --overwrite to replace)")
            continue
        print(f"  structuring + cleaning ...")
        try:
            clean_file(f, output_dir=dest, model=model)
        except Exception as e:
            print(f"  ERROR: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AI cleaning agent for raw .md files.")
    parser.add_argument("source", help=".md file or folder of .md files")
    parser.add_argument("--output", "-o", default=None, help="Output directory")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing cleaned files")
    parser.add_argument("--model", default=INGEST_MODEL, help=f"Claude model for cleaning (default: {INGEST_MODEL})")
    args = parser.parse_args()

    process(source=args.source, output_dir=args.output, overwrite=args.overwrite, model=args.model)
