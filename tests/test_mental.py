"""
repository/ingestion/scripts/mental.py — the parts added on 2026-10-30 (the "pente fino"):

  - evidence on every new claim, checked only for runs whose run file says "evidence_required";
  - the review base, written by `done` whenever the review matches the document;
  - `packet --delta`: only the blocks changed since the last review, only the letters they cite;
  - `done` carrying the earlier verdict of unchanged blocks, and a failing one still blocking;
  - `findings`: every blocking item in full.

Everything lives in tmp_path: the module's path constants are patched, the vault index is stubbed
and the tracker is stubbed, so the real ledger, documents and workbook are never touched.

    uv run pytest tests/test_mental.py
"""

import json
import sys
import types
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "repository" / "ingestion" / "scripts"))
import mental  # noqa: E402

CFG = {"managers": {"mgr": {"corpora": [{"path": "mgr/clean_md", "date": r"L-(?P<y>\d{4})_(?P<m>\d{2})"}]}},
       "areas": {"inflation": "inflation"}, "documents": {}}
NAME = "mgr_inflation_mental_models"

LETTER_1 = ("The manager wrote that the exchange rate feeds into prices slowly and that the pass-through "
            "to services is weaker than to goods in this episode.\n")
LETTER_2 = ("The manager wrote that food prices push the approval of the government down and that the "
            "market had not priced this in yet.\n")
EV_1 = "the exchange rate feeds into prices slowly"
EV_2 = "food prices push the approval of the government down"

OLD_DOC = """# Inflation Mental Models - Mgr

## About this document

Covers the letters of the manager.

## 1. Pass-through

Intro of the cluster.

## 1.1 Exchange rate pass-through

**What it is:** Prices respond to the exchange rate with a lag, through imports.

**Key variables:**
- exchange rate

**How Mgr applied it:**
- **Jan/2024:** The manager saw the lag as short.

## 1.2 Food and politics

**What it is:** Food inflation weighs on how the government is seen.

**Key variables:**
- food prices

**How Mgr applied it:**
- **Jan/2024:** The manager linked food to approval.

## Connections

- none
"""

NEW_11 = "- **Feb/2025:** The exchange rate feeds into prices slowly, and the pass-through to services is weaker.\n"
NEW_12 = "- **Feb/2025:** Food prices push the approval of the government down.\n"


def doc_text(n11=NEW_11, n12=NEW_12):
    d = OLD_DOC.replace("The manager saw the lag as short.\n", "The manager saw the lag as short.\n" + n11, 1)
    return d.replace("The manager linked food to approval.\n", "The manager linked food to approval.\n" + n12, 1)


def claims(evidence=True):
    def n(letter, text, ev):
        c = {"claim": text, "letter": letter}
        if evidence:
            c["evidence"] = ev
        return c
    return {"1.1": {"old": {"C1": "Prices respond to the exchange rate with a lag."},
                    "new": {"N1": n("L-2025_01", "The pass-through to services is weaker.", EV_1)}},
            "1.2": {"old": {"C1": "Food inflation weighs on how the government is seen."},
                    "new": {"N1": n("L-2025_02", "Food pushes the approval down.", EV_2)}}}


class Env:
    def __init__(self, root: Path):
        self.root = root
        self.doc = root / "obsidian" / "inflation" / "mental_models" / f"{NAME}.md"
        self.ledger = root / "repository" / "mental_model" / "ledger"

    def side(self, kind):
        return self.ledger / f".{NAME}.{kind}.json"

    def write_claims(self, cl):
        self.side("claims").write_text(json.dumps(cl), encoding="utf-8")

    def write_doc(self, text):
        self.doc.write_text(text, encoding="utf-8")

    def review(self, doc, entries):
        self.side("review").write_text(json.dumps({"document_sha": mental.doc_sha(doc), "entries": entries}),
                                       encoding="utf-8")

    def ok(self, k, where, ev):
        return {"old": {"C1": {"verdict": "kept", "where": where}},
                "new": {"N1": {"verdict": "supported", "evidence": ev}}, "uncovered_old": [], "extra": []}

    def bad(self, k, where, note="x " * 100):
        e = self.ok(k, where, "")
        e["new"]["N1"] = {"verdict": "unsupported", "note": note}
        return e


@pytest.fixture
def env(tmp_path, monkeypatch):
    e = Env(tmp_path)
    clean = tmp_path / "repository" / "mental_model" / "mgr" / "clean_md"
    clean.mkdir(parents=True)
    (clean / "L-2025_01.md").write_text(LETTER_1, encoding="utf-8")
    (clean / "L-2025_02.md").write_text(LETTER_2, encoding="utf-8")
    e.doc.parent.mkdir(parents=True)
    e.ledger.mkdir()
    e.write_doc(OLD_DOC)
    monkeypatch.setattr(mental, "OBSIDIAN", tmp_path / "obsidian")
    monkeypatch.setattr(mental, "MM", tmp_path / "repository" / "mental_model")
    monkeypatch.setattr(mental, "LEDGER", e.ledger)
    monkeypatch.setattr(mental, "index", lambda: {})
    monkeypatch.setitem(sys.modules, "tracker", types.SimpleNamespace(build=lambda: "stub"))
    mental.cmd_begin(CFG, "mgr", "inflation", None, [])
    return e


def run_check():
    return mental.check(CFG, "mgr", "inflation")


def done(*accept):
    mental.cmd_done(CFG, "mgr", "inflation", list(accept))


W11, W12 = "Prices respond to the exchange rate with a lag", "Food inflation weighs on how the government is seen"


def blocked_first_run(env):
    """A complete first pass: both blocks repacked, review of the current document, 1.1.N1 unsupported."""
    env.write_doc(doc_text())
    env.write_claims(claims())
    env.review(doc_text(), {"1.1": env.bad("1.1", W11, "the letter does not say it " * 10),
                            "1.2": env.ok("1.2", W12, EV_2)})
    with pytest.raises(SystemExit) as e:
        done()
    return str(e.value)


# ── evidence ─────────────────────────────────────────────────────────────────

def test_begin_marks_the_run_as_requiring_evidence(env):
    assert json.loads(mental.run_path(NAME).read_text(encoding="utf-8"))["evidence_required"] is True


def test_evidence_is_required_and_checked_when_the_run_says_so(env):
    env.write_doc(doc_text())
    env.write_claims(claims(evidence=False))
    res = run_check()
    assert not res["ok"] and any("evidence" in p and "1.1.N1" in p for p in res["problems"])
    cl = claims()
    cl["1.1"]["new"]["N1"]["evidence"] = "a sentence that is nowhere in the letters"
    env.write_claims(cl)
    assert any("1.1.N1" in p and "evidence" in p for p in run_check()["problems"])
    env.write_claims(claims())
    assert run_check()["ok"], run_check()["problems"]


def test_evidence_is_not_required_for_runs_begun_before(env):
    run = json.loads(mental.run_path(NAME).read_text(encoding="utf-8"))
    del run["evidence_required"]
    mental.run_path(NAME).write_text(json.dumps(run), encoding="utf-8")
    env.write_doc(doc_text())
    env.write_claims(claims(evidence=False))
    assert run_check()["ok"], run_check()["problems"]


# ── review base ──────────────────────────────────────────────────────────────

def test_done_writes_the_review_base_even_when_blocked(env):
    msg = blocked_first_run(env)
    assert "1.1.N1 UNSUPPORTED" in msg
    base = json.loads(env.side("review_base").read_text(encoding="utf-8"))
    assert set(base["blocks"]) == {"1.1", "1.2"}
    nb = mental.blocks(doc_text())
    assert base["blocks"]["1.1"]["hash"] == mental.block_hash(nb["1.1"]["text"])
    assert base["blocks"]["1.2"]["entry"]["new"]["N1"]["verdict"] == "supported"
    assert base["blocks"]["1.1"]["entry"]["new"]["N1"]["verdict"] == "unsupported"


def test_no_review_base_when_the_review_is_of_another_version(env):
    env.write_doc(doc_text())
    env.write_claims(claims())
    env.review(doc_text("- **Feb/2025:** Something else, the exchange rate feeds into prices slowly.\n"),
               {"1.1": env.ok("1.1", W11, EV_1), "1.2": env.ok("1.2", W12, EV_2)})
    with pytest.raises(SystemExit) as e:
        done()
    assert "another version" in str(e.value)
    assert not env.side("review_base").exists()


# ── packet --delta ───────────────────────────────────────────────────────────

def test_delta_needs_a_base(env, capsys):
    env.write_doc(doc_text())
    env.write_claims(claims())
    with pytest.raises(SystemExit) as e:
        mental.cmd_packet(CFG, "mgr", "inflation", delta=True)
    assert "no review base" in str(e.value)


def test_delta_packet_prints_only_the_changed_block_and_its_letters(env, capsys):
    blocked_first_run(env)
    capsys.readouterr()
    fixed = doc_text(n11="- **Feb/2025:** The exchange rate feeds into prices slowly.\n")
    env.write_doc(fixed)
    mental.cmd_packet(CFG, "mgr", "inflation", delta=True)
    out = capsys.readouterr().out
    assert "BLOCK 1.1" in out and "BLOCK 1.2" not in out
    assert "L-2025_01.md" in out and "L-2025_02.md" not in out
    assert "1 of 2 blocks changed" in out
    # the full packet still lists everything
    mental.cmd_packet(CFG, "mgr", "inflation")
    full = capsys.readouterr().out
    assert "BLOCK 1.1" in full and "BLOCK 1.2" in full and "L-2025_02.md" in full


def test_delta_packet_with_nothing_changed(env, capsys):
    blocked_first_run(env)
    capsys.readouterr()
    mental.cmd_packet(CFG, "mgr", "inflation", delta=True)
    out = capsys.readouterr().out
    assert "0 of 2 blocks changed" in out and "BLOCK" not in out.replace("blocks changed", "")


def test_a_claims_only_change_makes_the_block_stale(env, capsys):
    blocked_first_run(env)
    capsys.readouterr()
    cl = claims()
    cl["1.2"]["new"]["N1"]["claim"] = "Food pushes the approval down, said otherwise."
    env.write_claims(cl)
    mental.cmd_packet(CFG, "mgr", "inflation", delta=True)
    assert "BLOCK 1.2" in capsys.readouterr().out


# ── done merging ─────────────────────────────────────────────────────────────

FIXED_11 = "- **Feb/2025:** The exchange rate feeds into prices slowly.\n"


def test_done_merges_base_verdicts_for_unchanged_blocks(env):
    blocked_first_run(env)
    fixed = doc_text(n11=FIXED_11)
    env.write_doc(fixed)
    cl = claims()
    cl["1.1"]["new"]["N1"]["claim"] = "The exchange rate feeds into prices slowly."
    env.write_claims(cl)
    env.review(fixed, {"1.1": env.ok("1.1", W11, EV_1)})          # a delta review: only the changed block
    done()
    assert not mental.run_path(NAME).exists() and not env.side("review_base").exists()
    assert mental.ledger(NAME).keys() == {"L-2025_01", "L-2025_02"}
    log = (env.ledger / f"{NAME}.log.md").read_text(encoding="utf-8")
    assert "| 1.2 | N1 |" in log and "| 1.1 | N1 |" in log and "supported" in log


def test_done_uses_the_new_verdict_for_a_changed_block(env):
    blocked_first_run(env)
    fixed = doc_text(n11=FIXED_11)
    env.write_doc(fixed)
    cl = claims()
    cl["1.1"]["new"]["N1"]["claim"] = "The exchange rate feeds into prices slowly."
    env.write_claims(cl)
    env.review(fixed, {"1.1": env.bad("1.1", W11, "still not in the letter"),
                       "1.2": env.ok("1.2", W12, EV_2)})
    with pytest.raises(SystemExit) as e:
        done()
    assert "1.1.N1 UNSUPPORTED" in str(e.value) and "still not in the letter" in str(e.value)
    assert "1.2" not in str(e.value)


def test_a_failing_verdict_of_an_unchanged_block_still_blocks(env):
    blocked_first_run(env)
    fixed = doc_text(n12="- **Feb/2025:** Food prices push the approval of the government down, says the letter.\n")
    env.write_doc(fixed)
    env.review(fixed, {"1.2": env.ok("1.2", W12, EV_2)})           # 1.1 (failing) is not re-listed
    with pytest.raises(SystemExit) as e:
        done()
    assert "1.1.N1 UNSUPPORTED" in str(e.value)
    assert mental.run_path(NAME).exists()


def test_a_changed_block_missing_from_the_delta_review_is_not_reviewed(env):
    blocked_first_run(env)
    fixed = doc_text(n11=FIXED_11)
    env.write_doc(fixed)
    env.review(fixed, {})
    with pytest.raises(SystemExit) as e:
        done()
    assert "block 1.1 was not reviewed" in str(e.value)


# ── findings ─────────────────────────────────────────────────────────────────

def test_findings_prints_the_full_notes_and_texts(env, capsys):
    blocked_first_run(env)
    capsys.readouterr()
    mental.cmd_findings(CFG, "mgr", "inflation")
    out = capsys.readouterr().out
    note = ("the letter does not say it " * 10).strip()
    assert note in out                                            # nothing cut at 120 characters
    assert "BLOCK 1.1 · N1 · unsupported" in out
    assert "The pass-through to services is weaker." in out
    assert "letter the claim cites: L-2025_01" in out
    assert "CURRENT TEXT OF BLOCK 1.1" in out and "CURRENT TEXT OF BLOCK 1.2" not in out
    assert "L-2025_01.md" in out and "L-2025_02.md" not in out


def test_findings_with_a_clean_review(env, capsys):
    env.write_doc(doc_text())
    env.write_claims(claims())
    env.review(doc_text(), {"1.1": env.ok("1.1", W11, EV_1), "1.2": env.ok("1.2", W12, EV_2)})
    mental.cmd_findings(CFG, "mgr", "inflation")
    assert "no blocking item" in capsys.readouterr().out
