"""
repository/ingestion/settings.yaml — what the pipeline must remember between runs.

Two sections:

  files:            per-PDF entries, keyed by file name (with .pdf). Either extraction
                    settings that differ from DEFAULT, or `status: needs_attention` for a
                    file the tools cannot ingest (a scan, a failed page check), so the sweep
                    lists it without retrying it every run. Every entry carries a `reason`.
  topics_on_hold:   topic -> reason. The sweep reports these topics and never ingests them.

A re-run on the same PDF reproduces the same text because the settings live here, not in
anyone's memory.
"""

from pathlib import Path

import yaml

SETTINGS_FILE = Path(__file__).resolve().parent.parent / "settings.yaml"
DEFAULT = {"mode": "plumber", "x_tolerance": 1.5, "decode_shift": 0}
STATUSES = {"needs_attention"}
_FILE_KEYS = set(DEFAULT) | {"reason", "status"}


def load() -> dict:
    if not SETTINGS_FILE.exists():
        return {"files": {}, "topics_on_hold": {}}
    data = yaml.safe_load(SETTINGS_FILE.read_text(encoding="utf-8")) or {}
    unknown = set(data) - {"files", "topics_on_hold"}
    if unknown:
        raise ValueError(f"settings.yaml: unknown sections {sorted(unknown)}")
    files = data.get("files") or {}
    for name, entry in files.items():
        bad = set(entry) - _FILE_KEYS
        if bad:
            raise ValueError(f"settings.yaml, {name!r}: unknown keys {sorted(bad)}")
        if "reason" not in entry:
            raise ValueError(f"settings.yaml, {name!r}: every entry needs a 'reason'")
        if "status" in entry and entry["status"] not in STATUSES:
            raise ValueError(f"settings.yaml, {name!r}: status must be one of {sorted(STATUSES)}")
    return {"files": files, "topics_on_hold": data.get("topics_on_hold") or {}}


def settings_for(pdf_name: str) -> dict:
    """Extraction settings for one PDF file name (with the .pdf extension)."""
    entry = load()["files"].get(pdf_name, {})
    return {k: entry.get(k, v) for k, v in DEFAULT.items()}


def status_for(pdf_name: str) -> tuple[str, str] | None:
    """(status, reason) when the file is marked as not ingestible, else None."""
    entry = load()["files"].get(pdf_name, {})
    return (entry["status"], entry["reason"]) if "status" in entry else None


def topics_on_hold() -> dict:
    return load()["topics_on_hold"]
