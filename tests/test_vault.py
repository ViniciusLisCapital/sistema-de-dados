"""
The vault agent's helper (repository/ingestion/scripts/vault.py), built 2026-10-19 with the
agent. What it must keep true:

  - a synthesis note has the clean_md's name, so --list and the tracker match exactly;
  - every number of the note is in the clean_md (the 2026-10-19 run over the 19 older notes
    found journal volumes, page ranges and coefficients that the clean_md does not contain);
  - a synthesis note and its clean_md share a name, so a bare [[name]] is ambiguous and links
    to either carry the path from the vault root;
  - one concepts folder, obsidian/concepts/, and every concept a note links links back.

Script with asserts, not pytest (the project has no pytest), like tests/test_ingestion.py:

    uv run python tests/test_vault.py
"""

import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "repository" / "ingestion" / "scripts"))

import tracker  # noqa: E402
import vault  # noqa: E402

NAME = "taylor_rule (Taylor, 1993)"
CLEAN = """Discretion versus policy rules in practice
The rule sets the federal funds rate at 2 percent plus inflation, with a weight of 0.5 on
the output gap and 0.5 on inflation above 2 percent. The sample runs from 1987 to 1992.
Table 1 reports a correlation of .73 and a fit of 1,000 basis points over the period.
"""
NOTE = f"""---
aliases: ["Taylor 1993 - Discretion versus Policy Rules"]
---

# Discretion versus Policy Rules in Practice — Taylor 1993

**Type:** paper
**Tags:** #taylor-rule
**Source:** Carnegie-Rochester Conference Series
**Language:** English
**Source file:** [[mp/clean_md/{NAME}]]

---

## Context and motivation

Written in 1993 about the 1987–92 period.

## Core argument / thesis

A weight of 0.50 on the gap and 0.5 on inflation (Table 1: correlation 0.73, fit 1000).

## Key mechanisms / model

1. The rate is 2 percent plus inflation.

## Main results / findings

See Verde sections 1.1–1.11.

## Limitations and caveats

None in the text.

## Connections

- [[taylor_rule]] — the rule itself
- [[taylor_principle]] (proposed) — stability condition
"""
CONCEPT = f"""# Taylor rule

## How it appears across sources

| Source | Role |
|---|---|
| [[mp/synthesis/{NAME}\\|Taylor 1993]] | the origin |
"""


class TempVault:
    """A vault in a temp folder, with vault.OBSIDIAN and vault.CONCEPTS pointed at it."""

    def __init__(self, note=NOTE, concept=CONCEPT, clean=CLEAN):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        for d in ("mp/clean_md/central_bank", "mp/synthesis", "concepts"):
            (self.root / d).mkdir(parents=True)
        (self.root / "mp/clean_md" / f"{NAME}.md").write_text(clean, encoding="utf-8")
        (self.root / "mp/clean_md/other_paper (Doe, 2000).md").write_text("x", encoding="utf-8")
        (self.root / "mp/clean_md/central_bank/ata_250.md").write_text("x", encoding="utf-8")
        if note is not None:
            (self.root / "mp/synthesis" / f"{NAME}.md").write_text(note, encoding="utf-8")
        if concept is not None:
            (self.root / "concepts/taylor_rule.md").write_text(concept, encoding="utf-8")

    def __enter__(self):
        self.saved = vault.OBSIDIAN, vault.CONCEPTS
        vault.OBSIDIAN, vault.CONCEPTS = self.root, self.root / "concepts"
        return self

    def __exit__(self, *exc):
        vault.OBSIDIAN, vault.CONCEPTS = self.saved
        self.tmp.cleanup()

    def check(self, meta=None):
        return vault.check("mp", NAME, meta=meta or {})     # {}: never the real workbook


# ── numbers ──────────────────────────────────────────────────────────────────

def test_number_forms():
    have = vault.source_numbers("1,000 and 0,5 and .73 and 0.70 and 1.234,5 and 12.500")
    for tok in ("1000", "1,000", "0.5", "0,5", "0.73", ".73", "0.7", "1234.5", "12500"):
        assert vault._forms(tok) & have, tok
    assert not (vault._forms("0.732") & vault.source_numbers("0.73")), "no rounding"
    assert not (vault._forms("7.3") & vault.source_numbers("0.732")), "no unit conversion"


def test_numbers_that_are_not_compared():
    toks = {t for _, t, _ in vault._numbers(NOTE, NAME)}
    assert "1993" not in toks                 # the source's own year (title, aliases, prose)
    assert "92" not in toks                   # 1987–92
    assert "1.11" not in toks and "1.1" not in toks   # a mental model's section numbers
    assert not vault._numbers("1. The rate\n## 2. Section", NAME)    # list and heading numbering
    assert {"0.50", "0.5", "0.73", "1000", "2", "1987"} <= toks
    linked = "- [[fp/synthesis/fiscal_dominance (itau, 2025)]] — Itaú restates it for 2025, at 0.31"
    assert {t for _, t, _ in vault._numbers(linked, NAME)} == {"0.31"}   # the linked source's year only
    line = "Written in 1999, vol. 84."
    assert {"1999", "84"} <= {t for _, t, _ in vault._numbers(line, NAME)}


# ── links ────────────────────────────────────────────────────────────────────

def test_link_parsing():
    text = "a [[uip]] b [[x/y/z (A, 2000)#Sec|alias]] c | [[p/q\\|alias]] |\n- [[new_one]] (proposed) — x"
    got = [(t, pr) for _, t, pr in vault.links(text)]
    assert got == [("uip", False), ("x/y/z (A, 2000)", False), ("p/q", False), ("new_one", True)], got


def test_same_name_is_ambiguous_and_the_path_resolves():
    with TempVault() as v:
        idx = vault.index()
        assert vault.resolve(NAME, idx)[0] == "ambiguous"
        assert vault.resolve(f"mp/clean_md/{NAME}", idx)[0] == "ok"
        assert vault.resolve("Taylor_Rule", idx)[0] == "ok"      # Obsidian matches names without case
        assert vault.resolve("nothing_here", idx)[0] == "missing"


# ── check ────────────────────────────────────────────────────────────────────

def test_check_passes_a_good_note():
    with TempVault() as v:
        r = v.check()
        assert r["ok"], r["problems"]
        assert r["proposed"] == ["taylor_principle"] and r["concepts"] == ["taylor_rule"]


def test_check_failures():
    cases = [
        (NOTE.replace("0.73", "0.732"), "number not in the clean_md"),
        (NOTE.replace("Carnegie-Rochester Conference Series", "vol. 39, pp. 195-214"), "number not in the clean_md"),
        (NOTE.replace("## Limitations and caveats", "## Caveats"), "section missing: ## Limitations"),
        (NOTE.replace("**Language:** English\n", ""), "field missing: **Language:**"),
        (NOTE.replace(f"[[mp/clean_md/{NAME}]]", f"[[{NAME}]]"), "Source file must be"),
        (NOTE.replace(f"[[mp/clean_md/{NAME}]]", "[[mp/clean_md/other_paper (Doe, 2000)]]"), "Source file must be"),
        (NOTE.replace(" (proposed)", ""), "[[taylor_principle]] resolves to no file"),
        (NOTE.replace("[[taylor_principle]]", "[[Taylor Principle]]"), "not a snake_case slug"),
        (NOTE + f"- [[{NAME}]] — itself\n", "matches several files"),
    ]
    for note, expect in cases:
        with TempVault(note=note) as v:
            r = v.check()
            assert not r["ok"] and any(expect in p for p in r["problems"]), (expect, r["problems"])
    with TempVault(concept="# Taylor rule\n\nNo link back.\n") as v:
        r = v.check()
        assert any("does not link back" in p for p in r["problems"]), r["problems"]
    with TempVault(note=None) as v:
        assert not v.check()["ok"]


def test_source_line_may_take_the_tracker_biblio():
    """A book chapter's clean_md has no title page: the Source line may cite the tracker row
    (2nd ed., 2015), and only the Source line."""
    src = NOTE.replace("Carnegie-Rochester Conference Series", "Monetary Policy (2nd ed.), 2015")
    meta = {"Name": "Monetary Policy (2nd ed.)", "Date": "2015"}
    with TempVault(note=src) as v:
        assert not v.check()["ok"]                          # 2015 is not in the clean_md
        assert v.check(meta)["ok"], v.check(meta)["problems"]
    body = NOTE.replace("Written in 1993", "Written in 2015")
    with TempVault(note=body) as v:
        assert not v.check(meta)["ok"], "the biblio only counts on the Source line"


def test_concept_numbers():
    """A linked line is checked against the clean_md of the notes it links; an unlinked line
    against every source of the page; a mental model stands for its own section numbers."""
    page = f"""# Taylor rule

## Definition

A weight of 0.5 on the gap, 2 percent target. Taylor (1993) and Doe (2000).

| [[mp/synthesis/{NAME}\\|Taylor 1993]] | correlation .73 |
| [[mp/synthesis/other_paper (Doe, 2000)]] | coefficient 0.42 |

- [[verde_mp_mental_models]] — 3.2–3.4: carry as support
"""
    with TempVault(concept=page) as v:
        (v.root / "mp/synthesis/other_paper (Doe, 2000).md").write_text("x", encoding="utf-8")
        (v.root / "mp/clean_md/other_paper (Doe, 2000).md").write_text("a coefficient of 0.42", encoding="utf-8")
        (v.root / "mp/mental_models").mkdir()
        (v.root / "mp/mental_models/verde_mp_mental_models.md").write_text("### 3.2\n### 3.4", encoding="utf-8")
        assert vault.check_concept("taylor_rule")["ok"], vault.check_concept("taylor_rule")["problems"]
        for old, new in ((".73", "0.74"), ("0.42", "0.5"), ("0.5 on", "0.6 on"), ("3.4", "3.5")):
            (v.root / "concepts/taylor_rule.md").write_text(page.replace(old, new, 1), encoding="utf-8")
            assert not vault.check_concept("taylor_rule")["ok"], (old, new)
        # 0.5 is in Taylor's clean_md, not in Doe's: a line linking only Doe fails on it
        (v.root / "concepts/taylor_rule.md").write_text(page.replace("coefficient 0.42", "coefficient 0.5"), encoding="utf-8")
        assert not vault.check_concept("taylor_rule")["ok"]
        # the note's own check sees the patch it added (the row linking it), not the rest
        (v.root / "concepts/taylor_rule.md").write_text(page.replace("correlation .73", "correlation 0.74"), encoding="utf-8")
        assert any("number in concepts/taylor_rule.md" in p for p in v.check()["problems"])
        (v.root / "concepts/taylor_rule.md").write_text(page.replace("coefficient 0.42", "coefficient 0.99"), encoding="utf-8")
        assert v.check()["ok"], v.check()["problems"]


def test_list_states():
    with TempVault() as v:
        rows = {r["name"]: r["state"] for r in vault.scan("mp")}
        assert rows == {NAME: "done", "other_paper (Doe, 2000)": "pending"}, rows   # central_bank/ skipped
        assert "mp" in vault.topics() and "concepts" not in vault.topics()
        (v.root / "mp/synthesis/Taylor 1993 - Old Name.md").write_text("x", encoding="utf-8")
        assert vault.orphans("mp") == ["Taylor 1993 - Old Name"]


def test_tracker_match_is_exact():
    with TempVault() as v:
        saved = tracker.OBSIDIAN
        tracker.OBSIDIAN = v.root
        try:
            files = [{"name": NAME}, {"name": "other_paper (Doe, 2000)"}, {"name": "taylor_rule_ii (Taylor, 1993)"}]
            assert tracker._with_synthesis("mp", files) == {NAME}
        finally:
            tracker.OBSIDIAN = saved


# ── the real vault ───────────────────────────────────────────────────────────

def test_real_vault_layout():
    obs = ROOT / "obsidian"
    assert (obs / "concepts").is_dir()
    assert not list(obs.glob("*/concepts")), "one concepts folder: obsidian/concepts/"
    for t in vault.topics():
        for r in vault.scan(t):
            if r["state"] != "done":
                continue
            probs = vault.check(t, r["name"])["problems"]
            bad = [p for p in probs if p.startswith("Source file") or "matches several files" in p]
            assert not bad, (r["name"], bad)


if __name__ == "__main__":
    tests = [(k, v) for k, v in dict(globals()).items() if k.startswith("test_") and callable(v)]
    falhas = 0
    for nome, fn in tests:
        try:
            fn()
            print(f"ok    {nome}")
        except AssertionError as e:
            falhas += 1
            print(f"FALHA {nome}: {e}")
    print(f"\n{len(tests) - falhas}/{len(tests)} ok")
    sys.exit(1 if falhas else 0)
