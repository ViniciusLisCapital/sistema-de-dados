"""
ingestion/compare.py — Semantic quality check for the ingestion pipeline.

Uses Claude to verify that a structured/cleaned .md preserves all substantive
content from the raw .md. Boilerplate removal is expected and correct.

── Hardcoded pairs (edit FILES below, then run with no arguments) ────────────
    uv run python ingestion/compare.py

── CLI (ad-hoc comparison) ──────────────────────────────────────────────────
    uv run python ingestion/compare.py <file_a> <file_b>

Options:
    --model   Claude model to use (default: claude-haiku-4-5-20251001)
    --output  Output .md path (default: ingestion/compare_report.md)

Requires ANTHROPIC_API_KEY in .env
"""

# ── Hardcoded pairs ───────────────────────────────────────────────────────────
# Paths are relative to the project root (or absolute).
FILES: list[tuple[str, str]] = [
    (
        "ingestion\work\\fiscal_policy\\fiscal_dominance (itau, 2025)_structured.md",
        "agent_bibliography\\fiscal_policy\\fiscal_dominance (itau, 2025).md"
        ,
    ),
    # (
    #     "ingestion/work/exchange_rate_policy/primer_gsdeer_gsfeer (Goldman, 2025)_raw.md",
    #     "ingestion/work/exchange_rate_policy/primer_gsdeer_gsfeer (Goldman, 2025)_structured.md",
    # ),
]

import argparse
import datetime
import json
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

DEFAULT_MODEL = "claude-haiku-4-5-20251001"

_PROMPT = """\
You are a quality-control reviewer for a document ingestion pipeline.

FILE A is the raw extraction of a PDF (may contain boilerplate, chart noise, \
page numbers, disclaimers).
FILE B is the structured/cleaned version produced by an AI agent.

Your job: verify that FILE B preserves ALL substantive content from FILE A.
Boilerplate removal is expected and correct. Flag only genuine content loss.

Respond with a JSON object (no markdown fences) with exactly these fields:
{{
  "verdict": "ok" | "warning" | "loss",
  "preserved_pct": <integer 0-100, your estimate of substantive content preserved>,
  "lost": [<short description of each substantive idea/section dropped>],
  "added": [<anything meaningful added that was not in File A>],
  "notes": "<one or two sentences of overall assessment>"
}}

Verdict guide:
  ok      — all substantive content preserved; only boilerplate removed
  warning — minor content missing or ambiguous; worth a human glance
  loss    — clear substantive content was dropped

FILE A:
{file_a}

FILE B:
{file_b}
"""

_VERDICT_EMOJI = {"ok": "✅", "warning": "⚠️", "loss": "❌"}


def _check(a_path: Path, b_path: Path, model: str) -> str:
    """Run semantic check for one pair. Returns a Markdown section string."""
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


def _resolve(p: str, root: Path) -> Path:
    path = Path(p)
    if not path.exists():
        path = root / p
    return path


def main() -> None:
    parser = argparse.ArgumentParser(description="Semantic quality check for ingestion pipeline.")
    parser.add_argument("file_a", nargs="?", help="Raw file (omit to use FILES list)")
    parser.add_argument("file_b", nargs="?", help="Structured file (omit to use FILES list)")
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"Claude model (default: {DEFAULT_MODEL})",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Output .md path (default: ingestion/compare_report.md)",
    )
    args = parser.parse_args()
    root = Path(__file__).parent.parent
    out_path = Path(args.output) if args.output else root / "ingestion" / "compare_report.md"

    pairs = [(args.file_a, args.file_b)] if (args.file_a and args.file_b) else list(FILES)

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    parts = [
        "# Ingestion Quality Report\n",
        f"Generated: {timestamp}  |  Model: `{args.model}`\n",
        "---\n",
    ]

    for i, (fa, fb) in enumerate(pairs, 1):
        a_path = _resolve(fa, root)
        b_path = _resolve(fb, root)
        parts.append(f"# Pair {i}: {a_path.name} → {b_path.name}\n")
        parts.append(f"| | Path |")
        parts.append(f"|---|---|")
        parts.append(f"| **File A** | `{a_path}` |")
        parts.append(f"| **File B** | `{b_path}` |")
        parts.append("")
        parts.append(_check(a_path, b_path, model=args.model))
        parts.append("---\n")

    out_path.write_text("\n".join(parts), encoding="utf-8")
    print(f"Report written to: {out_path.relative_to(root)}")


if __name__ == "__main__":
    main()
