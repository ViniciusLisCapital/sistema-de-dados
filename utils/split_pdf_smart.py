"""
Smart PDF chapter splitter.
Uses Claude to parse the TOC and verify chapter boundaries.

Usage:
    uv run python utils/split_pdf_smart.py <pdf_path> <output_dir>
"""

import sys
import json
import re
import fitz
import anthropic
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


def get_text_range(doc, start, end):
    parts = []
    for i in range(start, min(end + 1, doc.page_count)):
        parts.append(f"---PDF_PAGE_{i}---\n{doc[i].get_text()}")
    return "\n\n".join(parts)


def parse_toc(client, toc_text):
    """Ask Claude to extract top-level chapters from TOC text."""
    prompt = f"""This is the table of contents from a textbook PDF.
Extract only the actual content sections: chapters, learning modules, preface, introduction, appendices, references, and indexes.

EXCLUDE purely administrative front matter such as:
- "How to Use the CFA Program Curriculum" or similar usage guides
- "About the Authors", "About the Publisher"
- Copyright, errata, or feedback pages
- Any section whose page number is a Roman numeral (i, ii, iii, iv, v, vi...) — skip those entirely

Return a JSON array where each item has:
  "num":       chapter/module number as integer, or 0 for unnumbered content sections
  "title":     section title as a short string
  "book_page": the page number shown in the TOC as an Arabic integer (skip entries with Roman numeral page numbers)

TOC text:
{toc_text}

Return ONLY a valid JSON array, no explanation."""

    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}],
    )
    raw = response.content[0].text.strip()
    raw = re.sub(r"^```[a-z]*\n?", "", raw)
    raw = re.sub(r"\n?```$", "", raw)
    chapters = json.loads(raw)
    return sorted(chapters, key=lambda c: c["book_page"])


def find_offset(client, doc, first_chapter):
    """Find PDF-page offset by locating the first chapter in pages 5–40."""
    search_start = 5
    search_end = min(40, doc.page_count - 1)
    pages_text = get_text_range(doc, search_start, search_end)

    prompt = f"""I need to find where a section starts in a textbook PDF.
Section: "{first_chapter['title']}" (book page {first_chapter['book_page']})

Below are PDF pages {search_start}–{search_end} with their PDF page index markers.
Find which PDF page index is the actual START of this section.
The start page shows the section title and the beginning of the text, not a continuation.

{pages_text}

Return ONLY JSON: {{"pdf_page": <integer index>}}"""

    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=100,
        messages=[{"role": "user", "content": prompt}],
    )
    result = extract_json(response.content[0].text)
    pdf_page = result["pdf_page"]
    return pdf_page - first_chapter["book_page"]


def extract_json(text):
    """Extract the first JSON object from a model response."""
    text = re.sub(r"^```[a-z]*\n?", "", text.strip())
    text = re.sub(r"\n?```$", "", text)
    m = re.search(r"\{[^{}]+\}", text, re.DOTALL)
    if m:
        return json.loads(m.group())
    return json.loads(text)


def verify_chapter_start(client, doc, chapter, candidate_pdf_page):
    """Confirm the exact PDF page where a chapter starts (searches ±6 pages)."""
    start = max(0, candidate_pdf_page - 6)
    end = min(doc.page_count - 1, candidate_pdf_page + 6)
    pages_text = get_text_range(doc, start, end)

    num_label = f"Chapter {chapter['num']}" if chapter["num"] else f'"{chapter["title"]}"'
    prompt = f"""I'm looking for the start of {num_label}: "{chapter['title']}" in a textbook PDF.
The TOC says it starts at book page {chapter['book_page']}.
I've extracted PDF pages {start}-{end} below (PDF index, not book page numbers).

The section START page typically shows the section title and the beginning of its content.

{pages_text}

Return ONLY JSON: {{"pdf_page": <integer index>, "confidence": "high" | "medium" | "low"}}"""

    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=150,
        messages=[{"role": "user", "content": prompt}],
    )
    return extract_json(response.content[0].text)


def safe_name(chapter):
    title = re.sub(r'[\\/:*?"<>|]', "", chapter["title"])[:50].strip()
    if chapter["num"]:
        return f"ch{chapter['num']:02d}_{title}"
    return title


def split_pdf(doc, boundaries, output_dir):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    for i, (name, start, end) in enumerate(boundaries):
        out = fitz.open()
        out.insert_pdf(doc, from_page=start, to_page=end)
        filename = f"{i:02d}_{name}.pdf"
        out.save(str(output_dir / filename))
        out.close()
        print(f"  {filename}  ({end - start + 1} pages, PDF {start}–{end})")


def run(pdf_path, output_dir):
    client = anthropic.Anthropic()
    doc = fitz.open(pdf_path)
    print(f"Opened: {Path(pdf_path).name}  ({doc.page_count} pages)\n")

    # Step 1: Parse TOC
    print("Step 1: Reading table of contents...")
    toc_text = get_text_range(doc, 0, 15)
    chapters = parse_toc(client, toc_text)
    print(f"  {len(chapters)} sections found:")
    for c in chapters:
        print(f"    [{c['num']:>2}] p.{c['book_page']:<5}  {c['title']}")

    # Step 2: Find offset using the first numbered chapter (skip unnumbered front matter)
    print("\nStep 2: Finding PDF page offset...")
    anchor = next((c for c in chapters if c["num"] > 0), chapters[0])
    offset = find_offset(client, doc, anchor)
    print(f"  Offset = {offset}  (PDF page = book page + {offset})")

    # Step 3: Verify each chapter boundary
    print("\nStep 3: Verifying boundaries...")
    confirmed = []
    for ch in chapters:
        candidate = ch["book_page"] + offset
        result = verify_chapter_start(client, doc, ch, candidate)
        pdf_page = result["pdf_page"]
        conf = result.get("confidence", "?")
        marker = "  " if conf == "high" else "? "
        pdf_str = str(pdf_page) if pdf_page is not None else "???"
        print(f"  {marker}[{ch['num']:>2}] book p.{ch['book_page']:<5} -> PDF p.{pdf_str:<5} [{conf}]  {ch['title']}")
        confirmed.append((ch, pdf_page))

    # Sort by verified PDF page and drop any that are out of order
    confirmed.sort(key=lambda x: x[1])
    clean = [confirmed[0]]
    for item in confirmed[1:]:
        if item[1] > clean[-1][1]:
            clean.append(item)
        else:
            print(f"  ! Skipping out-of-order section: '{item[0]['title']}' (PDF p.{item[1]} <= p.{clean[-1][1]})")
    confirmed = clean

    # Step 4: Split
    print("\nStep 4: Splitting PDF...")
    boundaries = []
    for i, (ch, start) in enumerate(confirmed):
        end = confirmed[i + 1][1] - 1 if i + 1 < len(confirmed) else doc.page_count - 1
        boundaries.append((safe_name(ch), start, end))

    split_pdf(doc, boundaries, output_dir)
    doc.close()
    print(f"\nDone. {len(boundaries)} files saved to: {Path(output_dir).resolve()}")


# --- SET PATHS HERE ---
PDF_PATH = "C:\\Users\\LIS CAPITAL\\LIS Capital Dropbox\\LIS Capital\\Macro\\Sistema de dados\\L2V04 - Corporate Issuers (CFA, 2025) - R04.pdf"
OUTPUT_DIR = "C:\\Users\\LIS CAPITAL\\LIS Capital Dropbox\\LIS Capital\\Macro\\Sistema de dados\\chapters_cfa_corporate"
# ----------------------

if __name__ == "__main__":
    if PDF_PATH and OUTPUT_DIR:
        run(PDF_PATH, OUTPUT_DIR)
    elif len(sys.argv) == 3:
        run(sys.argv[1], sys.argv[2])
    else:
        run(
            input("PDF path: ").strip().strip('"'),
            input("Output folder: ").strip().strip('"'),
        )
