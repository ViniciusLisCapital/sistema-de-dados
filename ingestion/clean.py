"""
Step 2 — AI cleaning agent (3-pass pipeline).

Pass 1 — Structure: reformats raw extracted text into clean markdown,
          fixes PDF encoding artifacts, marks obvious boilerplate with
          > [BOILERPLATE] blockquotes.
Pass 2 — Identify: analyzes the structured text and returns a JSON report
          of boilerplate sections with type and reason.
Pass 3 — Clean: rewrites the structured text with boilerplate removed.

Outputs (all in output_dir):
  <name>_structured.md   — formatted intermediate (auditable)
  <name>_report.json     — list of what was identified and why
  <name>_clean.md        — final cleaned document

Usage (CLI):
    uv run python ingestion/clean.py ingestion/sample/raw/teste.md
    uv run python ingestion/clean.py ingestion/sample/raw/ --output ingestion/sample/clean/

As a function:
    from ingestion.clean import clean_file
    report, clean_path = clean_file("ingestion/sample/raw/teste.md", output_dir="ingestion/sample/clean")
"""

import argparse
import json
import os
import re
from pathlib import Path

import anthropic
from dotenv import load_dotenv

load_dotenv()

MODEL = "claude-haiku-4-5-20251001"
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

_IDENTIFY_PROMPT = """\
You are a document cleaning assistant. The structured text below was extracted from a PDF
and has already been pre-formatted. Sections marked with > [BOILERPLATE] are candidates for removal.

Your task: identify all boilerplate sections that should be removed to leave only substantive content.
Include the pre-marked [BOILERPLATE] sections and any others you find.

Boilerplate includes:
- Table of contents / index
- Disclaimers and legal notices
- Repeated page headers/footers (page numbers, document title artifacts)
- Copyright / publisher information
- Contact details: phone numbers, email addresses, analyst names with contact info
- "About the author" or "About the company" sections
- References / bibliography that is just a citation list (no annotation)
- Regulatory certifications and compliance statements

Return a JSON object — no markdown fences, just raw JSON — in this exact shape:
{
  "boilerplate": [
    {
      "type": "toc|disclaimer|header_footer|copyright|contact|references|about|regulatory|other",
      "excerpt": "<first 120 characters of the section>",
      "reason": "<one sentence explaining why this is boilerplate>"
    }
  ],
  "content_summary": "<1-2 sentences: what is the substantive content about>"
}

If no boilerplate is found, return {"boilerplate": [], "content_summary": "..."}.

Document:
---
{text}
---"""

_CLEAN_PROMPT = """\
You are a document cleaning assistant.

Below is a structured document and a JSON list of boilerplate sections to remove.
Return ONLY the cleaned document — no commentary, no JSON, no preamble.
Remove all boilerplate sections completely. Remove any remaining > [BOILERPLATE] markers even if not in the list.
Keep all substantive content intact and in order. Preserve the markdown structure (headers, paragraphs).

Boilerplate to remove:
{boilerplate_json}

Document:
---
{text}
---"""


def _call(client: anthropic.Anthropic, prompt: str, max_tokens: int = 8096) -> str:
    msg = client.messages.create(
        model=MODEL,
        max_tokens=max_tokens,
        messages=[{"role": "user", "content": prompt}],
    )
    return msg.content[0].text.strip()


def _parse_report(raw: str) -> dict:
    raw = re.sub(r"^```(?:json)?\s*", "", raw.strip(), flags=re.IGNORECASE)
    raw = re.sub(r"\s*```$", "", raw.strip())
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        m = re.search(r"\{[\s\S]*\}", raw)
        if m:
            try:
                return json.loads(m.group())
            except json.JSONDecodeError:
                pass
        raise ValueError(f"Could not parse JSON from model response:\n{raw[:600]}")


def clean_file(
    source: str | Path,
    output_dir: str | Path | None = None,
) -> tuple[dict, Path]:
    """
    Run the 3-pass pipeline on a single raw .md file.

    Returns (report_dict, clean_path).
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
    structured_path = dest_dir / f"{base}_structured.md"
    report_path = dest_dir / f"{base}_report.json"
    clean_path = dest_dir / f"{base}.md"

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise EnvironmentError("ANTHROPIC_API_KEY not set in environment / .env")

    client = anthropic.Anthropic(api_key=api_key)

    # Pass 1: structure
    structured = _call(client, _STRUCTURE_PROMPT.replace("{text}", text), max_tokens=8096)
    structured_path.write_text(structured, encoding="utf-8")
    print(f"        structured: {len(structured):,} chars -> {structured_path.name}")

    # Pass 2: identify boilerplate (on structured text)
    raw_report = _call(client, _IDENTIFY_PROMPT.replace("{text}", structured))
    report = _parse_report(raw_report)
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    n_items = len(report.get("boilerplate", []))
    print(f"        identified: {n_items} boilerplate section(s) -> {report_path.name}")

    # Pass 3: apply cleaning (on structured text)
    boilerplate_json = json.dumps(report.get("boilerplate", []), ensure_ascii=False, indent=2)
    prompt3 = _CLEAN_PROMPT.replace("{boilerplate_json}", boilerplate_json).replace("{text}", structured)
    cleaned = _call(client, prompt3, max_tokens=8096)
    clean_path.write_text(cleaned, encoding="utf-8")
    print(f"        -> {clean_path.name}  ({len(cleaned):,} chars)")

    return report, clean_path


def process(
    source: str | Path,
    output_dir: str | Path | None = None,
    overwrite: bool = False,
) -> None:
    """Clean one .md file or all .md files in a folder."""
    source = Path(source)

    if source.is_file():
        files = [source]
    elif source.is_dir():
        files = sorted(f for f in source.glob("*.md") if not f.stem.endswith(("_structured", "_clean")))
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
        print(f"  structuring / identifying / cleaning ...")
        try:
            clean_file(f, output_dir=dest)
        except Exception as e:
            print(f"  ERROR: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AI cleaning agent for raw .md files.")
    parser.add_argument("source", help=".md file or folder of .md files")
    parser.add_argument("--output", "-o", default=None, help="Output directory")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing cleaned files")
    args = parser.parse_args()

    process(source=args.source, output_dir=args.output, overwrite=args.overwrite)
