"""
ingestion/compare.py — Semantic quality check for the ingestion pipeline.

Uses a configurable Claude model to verify that a cleaned .md preserves all
substantive content from its raw source. Boilerplate removal and formatting
cleanup are both expected and correct.

── Programmatic use (called by run.py after ingestion) ──────────────────────
    from ingestion.compare import generate_report
    generate_report(pairs, model=VERIFY_MODEL, out_path=Path("ingestion/compare_report.md"))
    # pairs: list of (raw_path, clean_path)

── Standalone (ad-hoc comparison) ──────────────────────────────────────────
    uv run python ingestion/compare.py <raw.md> <clean.md>
    uv run python ingestion/compare.py  # uses hardcoded FILES list below

Options:
    --model   Claude model for verification (default: claude-haiku-4-5-20251001)
    --output  Output .md path (default: ingestion/compare_report.md)

Requires ANTHROPIC_API_KEY in .env
"""

# ── Hardcoded pairs for standalone use ───────────────────────────────────────
# Each tuple: (raw_path, clean_path). Paths relative to project root or absolute.
FILES: list[tuple[str, str]] = [
    (
        r"ingestion\work\general\depreciation_pass_through (Goldfajn, 2000)_raw.md",
        r"repository\general\depreciation_pass_through (Goldfajn, 2000).md",
    ),
]

import argparse
import datetime
import json
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

VERIFY_MODEL = "claude-haiku-4-5-20251001"

_PROMPT = """\
You are a quality-control reviewer for a document ingestion pipeline.

FILE A is the raw text extracted directly from a PDF — it may contain boilerplate,
encoding artifacts, page numbers, disclaimers, and other noise.
FILE B is the final cleaned version produced by an AI agent: restructured into
clean markdown and stripped of all boilerplate.

Your job: verify that FILE B preserves ALL substantive content from FILE A.
Boilerplate removal and formatting cleanup are both expected and correct.
Flag only genuine content loss — substantive ideas, data, or arguments that
were dropped rather than cleaned.

Respond with a JSON object (no markdown fences) with exactly these fields:
{{
  "verdict": "ok" | "warning" | "loss",
  "preserved_pct": <integer 0-100, your estimate of substantive content preserved>,
  "lost": [<short description of each substantive idea/section dropped>],
  "added": [<anything meaningful added that was not in File A>],
  "notes": "<one or two sentences of overall assessment>"
}}

Verdict guide:
  ok      — all substantive content preserved; only boilerplate/noise removed
  warning — minor content missing or ambiguous; worth a human glance
  loss    — clear substantive content was dropped

FILE A (raw):
{file_a}

FILE B (clean):
{file_b}
"""

_VERDICT_EMOJI = {"ok": "✅", "warning": "⚠️", "loss": "❌"}


def check_pair(a_path: Path, b_path: Path, model: str) -> str:
    """Run semantic check for one (raw, clean) pair. Returns a Markdown section string."""
    if not a_path.exists():
        return f"> **ERROR:** file not found: `{a_path}`\n"
    if not b_path.exists():
        return f"> **ERROR:** file not found: `{b_path}`\n"

    try:
        import anthropic
    except ImportError:
        return "> `anthropic` package not installed. Run `uv add anthropic`.\n"

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        return "> `ANTHROPIC_API_KEY` not found in environment / .env.\n"

    a_text = a_path.read_text(encoding="utf-8")
    b_text = b_path.read_text(encoding="utf-8")
    prompt = _PROMPT.format(file_a=a_text, file_b=b_text)

    client = anthropic.Anthropic(api_key=api_key)
    try:
        message = client.messages.create(
            model=model,
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}],
        )
        raw = message.content[0].text.strip()
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
            raw = raw.strip()
        result = json.loads(raw)
    except json.JSONDecodeError:
        return f"> Model returned unparseable JSON:\n\n```\n{raw}\n```\n"
    except Exception as e:
        return f"> API error: {e}\n"

    verdict = result.get("verdict", "unknown")
    emoji = _VERDICT_EMOJI.get(verdict, "❓")
    pct = result.get("preserved_pct", "?")
    lost = result.get("lost", [])
    added = result.get("added", [])
    notes = result.get("notes", "")

    lines = [
        f"| Field | Value |",
        f"|-------|-------|",
        f"| Model | `{model}` |",
        f"| Verdict | {emoji} **{verdict.upper()}** |",
        f"| Content preserved | {pct}% |",
        "",
        f"> {notes}",
        "",
    ]

    if lost:
        lines.append("**Content lost:**\n")
        for item in lost:
            lines.append(f"- {item}")
        lines.append("")

    if added:
        lines.append("**Content added (not in File A):**\n")
        for item in added:
            lines.append(f"- {item}")
        lines.append("")

    return "\n".join(lines)


def generate_report(
    pairs: list[tuple[Path, Path]],
    model: str = VERIFY_MODEL,
    out_path: Path | None = None,
) -> Path:
    """
    Run semantic quality checks for a list of (raw_path, clean_path) pairs
    and write a Markdown report.

    Returns the path of the written report.
    """
    root = Path(__file__).parent.parent
    if out_path is None:
        out_path = root / "ingestion" / "compare_report.md"

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    parts = [
        "# Ingestion Quality Report\n",
        f"Generated: {timestamp}  |  Verify model: `{model}`\n",
        "---\n",
    ]

    for i, (a_path, b_path) in enumerate(pairs, 1):
        parts.append(f"## [{i}] {b_path.stem}\n")
        parts.append(f"| | Path |")
        parts.append(f"|---|---|")
        parts.append(f"| **Raw** | `{a_path}` |")
        parts.append(f"| **Clean** | `{b_path}` |")
        parts.append("")
        parts.append(check_pair(a_path, b_path, model=model))
        parts.append("---\n")

    out_path.write_text("\n".join(parts), encoding="utf-8")
    print(f"  quality report -> {out_path.relative_to(root)}")
    return out_path


def _resolve(p: str, root: Path) -> Path:
    path = Path(p)
    if not path.exists():
        path = root / p
    return path


def main() -> None:
    parser = argparse.ArgumentParser(description="Semantic quality check for ingestion pipeline.")
    parser.add_argument("file_a", nargs="?", help="Raw .md (omit to use FILES list)")
    parser.add_argument("file_b", nargs="?", help="Clean .md (omit to use FILES list)")
    parser.add_argument(
        "--model",
        default=VERIFY_MODEL,
        help=f"Claude model for verification (default: {VERIFY_MODEL})",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Output .md path (default: ingestion/compare_report.md)",
    )
    args = parser.parse_args()
    root = Path(__file__).parent.parent
    out_path = Path(args.output) if args.output else root / "ingestion" / "compare_report.md"

    if args.file_a and args.file_b:
        pairs = [(_resolve(args.file_a, root), _resolve(args.file_b, root))]
    else:
        pairs = [(_resolve(fa, root), _resolve(fb, root)) for fa, fb in FILES]

    generate_report(pairs, model=args.model, out_path=out_path)


if __name__ == "__main__":
    main()
