"""
The ingestion pipeline (repository/ingestion/scripts/), from the defects measured on the
46 monetary-policy PDFs on 2026-10-19:

  - the References cut ran to EOF when the next heading was not ALL CAPS, deleting the
    whole "Comments and Discussion" of Campbell et al. (2012);
  - x_tolerance=3 glued words together in ~20 files;
  - Clarida-Gali-Gertler 1999/2000 are Caesar-shifted by 3; Orphanides 2001 is letter-spaced.

Script with asserts, not pytest (the project has no pytest), like tests/test_sync_calendar.py:

    uv run python tests/test_ingestion.py
"""

import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "repository" / "ingestion" / "scripts"))

import clean_code  # noqa: E402
import extract  # noqa: E402
import qc  # noqa: E402
import run  # noqa: E402
import settings  # noqa: E402

PROSE = ("The central bank raises the policy rate when inflation is above the target, and the "
         "effect on output comes with a lag of several quarters.")
BLOCKING = ("no_text_layer", "garbled", "letter_spaced", "run_together")


def _pdf(name: str) -> Path | None:
    p = ROOT / "repository" / "monetary_policy" / "raw_pdf" / name
    return p if p.exists() else None


# ── References cut ───────────────────────────────────────────────────────────

def test_cut_stops_at_mixed_case_discussion():
    lines = [PROSE, "References", "Smith, J. 1990. A paper. Journal 1: 1-10.",
             "Comments and Discussion", "Comment By", PROSE]
    assert clean_code.block_cut_spans(lines) == [(1, 3, "Comments and Discussion")]
    out = clean_code.clean("\n".join(lines))
    assert "Comments and Discussion" in out and "Smith, J." not in out
    assert out.count(PROSE) == 2


def test_cut_stops_at_section_starters():
    for stop in ["Appendix A: Data", "Online Appendix", "APPENDIX", "Tables", "General Discussion"]:
        spans = clean_code.block_cut_spans(["References", "Doe, A. (2001), Title.", stop, PROSE])
        assert spans == [(0, 2, stop)], (stop, spans)


def test_cut_stops_at_content_after_references():
    # Each lost real content behind its reference list (2026-10-19).
    for stop in ["Endnotes", "Notes", "Data Sources", "Figure 1 - Exchange Rate and Market Interest Rate",
                 "Table 1. Interest Rate Pass-Through Regressions", "Coefficient"]:
        spans = clean_code.block_cut_spans(["References", "Doe, A. (2001), Title.", stop, PROSE])
        assert spans == [(0, 2, stop)], (stop, spans)
    # ...but a wrapped citation that starts with "Appendix," is not a heading.
    lines = ["References", "Rabanal, P., 2001, Brazil: Selected Issues and Statistical",
             'Appendix," IMF Country Report No. 01110.', "Roe, B. (2002), Other."]
    assert clean_code.block_cut_spans(lines) == [(0, 4, "EOF")]


def test_numbered_references_heading_starts_the_cut():
    # "8 - References" (Muinhos & Nakane 2006) and "6 References" were never cut.
    for head in ["8 - References", "6 References", "8. References", "References"]:
        spans = clean_code.block_cut_spans([PROSE, head, "Doe, A. (2001), Title.", "APPENDIX", PROSE])
        assert spans == [(1, 3, "APPENDIX")], (head, spans)


def test_running_head_does_not_end_the_cut():
    # Gali (2015) ch. 8: the all-caps running head ended the cut one page into the list.
    page = ["Doe, A. (2001), Title.", "POLICY IN THE OPEN ECONOMY", "257"]
    lines = [PROSE, "References"] + page * 3 + ["Roe, B. (2002).", "CHAPTER 8", "Poe, C. (2003).", "EXERCISES", PROSE]
    assert clean_code.block_cut_spans(lines) == [(1, len(lines) - 2, "EXERCISES")]
    spans = clean_code.block_cut_spans(["References", "Doe, A. (2001).", "Fig 1: Efficient Policy Frontier", PROSE])
    assert spans == [(0, 2, "Fig 1: Efficient Policy Frontier")]


def test_cleaner_keeps_body_lines_it_used_to_delete():
    # Each of these was deleted from a real paper (2026-10-19).
    body = [
        "(1995), Ireland (1996a), Carlstrom and Fuerst (1995), and Rotemberg and Woodford",  # year-initial
        "r = p + .5y + .5(p - 2) + 2 (1)",          # Taylor (1993), the rule itself
        "πt = κxt + υt",                             # an equation with short tokens
        "1 to t. In the equilibrium we",             # prose with short words (Gertler & Karadi 2011)
    ]
    out = clean_code.clean("\n".join([PROSE] + body + [PROSE]))
    for line in body:
        assert line in out, line
    assert "© 2006 International Monetary Fund" not in clean_code.clean(PROSE + "\n© 2006 International Monetary Fund\n" + PROSE)


def test_page_number_only_at_a_page_edge():
    # A bare number inside a page is a table cell (pymupdf prints one per line); at the edge
    # of a page (next to the blank line extract.py puts between pages) it is a page number.
    text = PROSE + "\n12\n\n" + PROSE + "\nYear\n1984\n0.496\n" + PROSE
    out = clean_code.clean(text).split("\n")
    assert "12" not in out and "1984" in out


def test_table_rows_are_not_a_running_header():
    rows = [f"FF{i} 17.930 [6.675 22.673] 0.496 [0.434 0.540]" for i in range(4)]
    out = clean_code.clean("\n".join([PROSE] + rows + [PROSE]))
    assert all(r in out for r in rows)
    note = "Note: Responses to a US contractionary monetary policy shock"
    out = clean_code.clean("\n".join([PROSE, PROSE, note, PROSE, note, PROSE, note, PROSE, PROSE]))
    assert out.count(note) == 3   # repeated inside a page: content (a row label, a note)
    page = "\n".join([PROSE, PROSE, "Running Head Of The Paper"])
    out = clean_code.clean("\n\n".join([page] * 4))
    assert out.count("Running Head Of The Paper") == 1   # at a page edge: a running head, first copy kept
    assert "Source: Authors' calculations." in clean_code.clean(PROSE + "\nSource: Authors' calculations.\n" + PROSE)
    spans = clean_code.block_cut_spans(["References", "Doe, A. (2001).", "A Credit and Banking Data – For Online Publication", PROSE])
    assert spans == [(0, 2, "A Credit and Banking Data – For Online Publication")]


def test_chart_block_keeps_its_caption():
    block = ["Figure 4: Responses of Expected Output Growth", "0.2", "0.3", "-0.5", "0.1", "1", "2"]
    out = clean_code.clean("\n".join([PROSE, ""] + block + ["", PROSE]))
    assert "Figure 4: Responses of Expected Output Growth" in out and "\n0.3\n" not in out


def test_ocr_references_heading():
    assert clean_code.block_cut_spans(["Refermces", "Doe, A. (2001).", "APPENDIX"]) == [(0, 2, "APPENDIX")]
    assert clean_code.block_cut_spans(["Preferences", "Households maximize utility."]) == []


def test_acronym_line_does_not_end_the_cut():
    lines = ["References", "Smith, J. (2010), Report,", "ECB", "Working Paper.", "EXERCISES", PROSE]
    assert clean_code.block_cut_spans(lines) == [(0, 4, "EXERCISES")]


def test_cut_to_eof_when_references_are_last():
    lines = [PROSE, "References", "Doe, A. (2001), Title.", "Roe, B. (2002), Other."]
    assert clean_code.block_cut_spans(lines) == [(1, 4, "EOF")]
    assert clean_code.clean("\n".join(lines)) == PROSE


def test_ordinary_citation_does_not_end_the_cut():
    lines = ["References", "Taylor, John B. 1993. Discretion versus Policy Rules in Practice.", PROSE]
    assert clean_code.block_cut_spans(lines) == [(0, 3, "EOF")]


def test_appendix_at_line_start_ends_the_cut():
    # Trade-off, asserted so that changing it is deliberate: a citation line that happens to
    # start with "Appendix" ends the cut early, which keeps text (safe) rather than losing it.
    lines = ["References", "Appendix to the Federal Reserve Bulletin was cited.", "Taylor, J. (1993)."]
    assert clean_code.block_cut_spans(lines)[0][2].startswith("Appendix")


# ── extraction, QC, settings, naming ─────────────────────────────────────────

def test_caesar_decode_page_by_page():
    plain = "The science of monetary policy is the study of rules."
    shifted = "".join(chr(ord(c) + 3) if c != " " else c for c in plain)  # how the PDF encodes it
    assert shifted.startswith("Wkh")
    assert extract._decode_page(shifted, 3) == plain
    assert extract._decode_page(PROSE, 3) == PROSE  # a readable page is left alone


def test_qc_flags():
    glued = "Anaturalinterpretationofthisevidenceisthattheannouncements " * 20 + PROSE
    assert any(f.startswith("run_together") for f in qc.flags([glued], glued, glued, []))
    spaced = " ".join("letterspacedtext") * 30
    assert any(f.startswith("letter_spaced") for f in qc.flags([spaced], spaced, spaced, []))
    assert qc.flags([PROSE * 3], PROSE * 3, PROSE * 3, []) == []
    assert any(f.startswith("no_text_layer") for f in qc.flags(["", "", PROSE * 3], PROSE * 3, PROSE * 3, []))


def _with_settings(text: str, fn):
    saved = settings.SETTINGS_FILE
    with tempfile.TemporaryDirectory() as d:
        settings.SETTINGS_FILE = Path(d) / "settings.yaml"
        settings.SETTINGS_FILE.write_text(text, encoding="utf-8")
        try:
            return fn()
        finally:
            settings.SETTINGS_FILE = saved


def _raises(fn, word):
    try:
        fn()
    except ValueError as e:
        assert word in str(e), e
        return
    raise AssertionError(f"expected a ValueError mentioning {word!r}")


def test_settings_require_a_reason():
    _with_settings('files:\n  "a (B, 2000).pdf": {mode: pymupdf}\n',
                   lambda: _raises(lambda: settings.settings_for("a (B, 2000).pdf"), "reason"))
    _with_settings('files:\n  "a (B, 2000).pdf": {status: broken, reason: x}\n',
                   lambda: _raises(lambda: settings.status_for("a (B, 2000).pdf"), "status"))
    _with_settings('inbox: {}\n', lambda: _raises(settings.load, "sections"))

    def ok():
        assert settings.settings_for("a (B, 2000).pdf") == {"mode": "pymupdf", "x_tolerance": 1.5, "decode_shift": 0}
        assert settings.settings_for("other (C, 2001).pdf") == settings.DEFAULT
        assert settings.status_for("scan (D, 1999).pdf") == ("needs_attention", "no text layer")
        assert settings.status_for("a (B, 2000).pdf") is None
        assert settings.topics_on_hold() == {"trader": "undecided"}
    _with_settings('files:\n  "a (B, 2000).pdf": {mode: pymupdf, reason: math}\n'
                   '  "scan (D, 1999).pdf": {status: needs_attention, reason: no text layer}\n'
                   'topics_on_hold:\n  trader: undecided\n', ok)


def test_settings_file_is_valid():
    s = settings.load()
    assert s["files"] and "trader" in s["topics_on_hold"], "repository/ingestion/settings.yaml should load"


def test_sweep_states():
    # The real folders: every state must be one of the four, and the known scan is not "pending".
    states = {r["file"]: r["state"] for t in run.topics() for r in run.scan(t)}
    assert set(states.values()) <= {"ingested", "pending", "needs_attention", "on_hold"}
    scan = "optimal_contracts_central_bankers (Walsh, 1995).pdf"
    if scan in states:
        assert states[scan] == "needs_attention"
    trader = [r for r in run.scan("trader")]
    assert all(r["state"] in ("on_hold", "ingested") for r in trader)


def test_tracker_matching():
    import tracker
    assert tracker._same_word("rate", "rates") and tracker._same_word("flow", "flows")
    assert not tracker._same_word("international", "intervention")
    rows = [  # (row, author tokens, year, title tokens) — the Krugman chapters that once tied
        (19, {"krugman", "obstfeld", "melitz"}, "2023", tracker._norm_tokens("International Economics, Ch. 18 - Fixed Exchange Rates and Foreign Exchange Intervention")),
        (23, {"krugman", "obstfeld", "melitz"}, "2023", tracker._norm_tokens("International Economics, Ch. 17 - Output and the Exchange Rate in the Short Run")),
        (5, {"rogoff"}, "1985", tracker._norm_tokens("The Optimal Degree of Commitment")),
    ]
    assert tracker._match(tracker._parse_stem("fixed_exchange_rate_intervention (Krugman, 2023)"), rows) == (19, None)
    assert tracker._match(tracker._parse_stem("output_exchange_rates_sr (Krugman, 2023)"), rows) == (23, None)
    assert tracker._match(tracker._parse_stem("x (Rogoff, 1986)"), rows) == (None, "")  # wrong year never matches
    tie = [(1, {"smith"}, "2000", ["alpha"]), (2, {"smith"}, "2000", ["alpha"])]
    r, why = tracker._match(tracker._parse_stem("alpha (Smith, 2000)"), tie)
    assert r is None and "several" in why


def test_name_convention():
    assert run.NAME_RE.match("taylor_rule (Taylor, 1993)")
    assert run.NAME_RE.match("credit_channel_transmission (Bernanke & Gertler, 1995)")
    assert not run.NAME_RE.match("The Optimal Degree of Commitment (Kenneth Rogoff, 1985)")


# ── the real PDFs (skipped where the file is not on this machine) ───────────

REAL = [
    ("forward_guidance_effects (Campbell et al., 2012).pdf", "discussion"),
    ("information_effect_hf_identification (Nakamura & Steinsson, 2018).pdf", "glued"),
    ("science_of_monetary_policy (Clarida, Gali & Gertler, 1999).pdf", "decoded"),
    ("policy_rules_real_time_data (Orphanides, 2001).pdf", "spacing"),
]


def test_real_pdfs():
    for name, check in REAL:
        pdf = _pdf(name)
        if pdf is None:
            print(f"   skip (not on this machine): {name}")
            continue
        s = settings.settings_for(name)
        res, raw, cleaned = qc.evaluate(extract.pages_text(pdf, s["mode"], s["x_tolerance"], s["decode_shift"]))
        blocking = [f for f in res["flags"] if f.startswith(BLOCKING)]
        assert blocking == [], (name, blocking)
        if check == "discussion":
            assert "Comments and Discussion" in cleaned, name
            assert res["removed_pct"] < 25, (name, res["removed_pct"])
        if check == "decoded":
            assert res["common_word_share"] > 0.2, (name, res["common_word_share"])
        if check == "spacing":
            assert res["one_letter_share"] < 0.15, (name, res["one_letter_share"])


def test_pymupdf_has_no_lone_carriage_return():
    # PyMuPDF emits "\r" for some math glyphs; on disk it read back as "\n" and the check
    # raw_reproduces_pdf failed on three Gali chapters (2026-10-19).
    name = "classical_monetary_model_ch2 (Gali, 2015).pdf"
    pdf = _pdf(name)
    if pdf is None:
        print(f"   skip (not on this machine): {name}")
        return
    assert not any("\r" in t for t in extract.pages_text(pdf, "pymupdf"))


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
