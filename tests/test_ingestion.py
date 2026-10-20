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
    for stop in ["Appendix A: Data", "Online Appendix", "APPENDIX", "Tables", "General Discussion",
                 "Comment"]:   # the bare heading, discussant on the next line (Krugman 2000)
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


def test_cleaner_does_not_judge_a_line_by_its_shape():
    # Since 2026-10-20 only References blocks, the disclosure tail and known boilerplate text
    # go. Each line below was deleted by a shape rule, and each was content somewhere.
    kept = [
        "http://www.bmf.com.br/). Therefore, the domestic interest rate is computed through the",  # Garcia & Valpassos 1998
        "Public Sector Net Debt (1+2+3) 28.5 29.9 34.4 34.5",       # a totals row read as a phone number
        "Source: International Monetary Fund, COFER, at http://www.imf.org/external/",  # Krugman 2023
        "in particular in lower-income countries, with food accounting for 28% of the CPI marialudovica.ambrosino@gs.com",
        "I 23% 42 -15 6 10 57", "FF 65 30 19 17 19",
        "12",                                                       # a page number: noise, not loss
    ]
    out = clean_code.clean("\n".join(sum(([PROSE, k] for k in kept), []) + [PROSE]))
    for k in kept:
        assert k in out.split("\n"), k
    # A table printed one cell per line (pymupdf): the short cells were dropped as axis ticks
    # and the long ones kept, so the survivors sat under the wrong row (Minella & Souza-Sobrinho
    # 2013, Table 2). Every cell stays, in order.
    table = ["Net Exports/GDP", "1.07", "0.87", "1.02", "0.87", "0.79", "0.55", "-0.24", "0.26",
             "Inflation Rate", "1.07", "0.94", "1.02", "0.94", "0.36", "0.48", "0.12", "0.40"]
    assert clean_code.clean("\n".join([PROSE, ""] + table + ["", PROSE])).split("\n")[2:-2] == table
    # A running head repeated on every page stays on every page.
    page = "\n".join([PROSE, PROSE, "Running Head Of The Paper"])
    assert clean_code.clean("\n\n".join([page] * 4)).count("Running Head Of The Paper") == 4
    spans = clean_code.block_cut_spans(["References", "Doe, A. (2001).", "A Credit and Banking Data – For Online Publication", PROSE])
    assert spans == [(0, 2, "A Credit and Banking Data – For Online Publication")]


def test_known_boilerplate_is_removed():
    for junk in ["For the exclusive use of PEDRO.LINZMEYER@LISCAPITAL.COM.BR",
                 "This content downloaded from 143.107.252.97 on Mon, 19 Oct 2026 12:00:00 UTC",
                 "All use subject to https://about.jstor.org/terms",
                 "M14_KRUG9719_12_GE_C14.indd 381 16/11/2021 16:16",
                 "3 November 2025 2",
                 "Investors should consider this report as only a single factor in making their investment decision."]:
        assert clean_code.clean("\n".join([PROSE, junk, PROSE])) == "\n".join([PROSE, PROSE]), junk
    # ...but a body line that merely mentions a date and a number is not a footer.
    assert "3 November 2025 the Copom kept" in clean_code.clean(PROSE + "\n3 November 2025 the Copom kept\n" + PROSE)
    text = "\n".join([PROSE, "Disclosure Appendix", "Reg AC text.", "More legal text."])
    assert clean_code.clean(text) == PROSE


def test_footnote_inside_references_survives_the_cut():
    refs = ["References", "Doe, A. (2001): “A paper”, Journal of Things, vol 1.",
            "Roe, B. (2002): “Another paper”, Journal of Stuff, vol 2."]
    fn = ["9Other economists have advanced arguments in favor of balkanization of multiregional",
          "countries (see for example, A. D. Scott [10]); and the argument adds to the list."]
    out = clean_code.clean("\n".join([PROSE] + refs + fn + ["Scott, A.D., “A Note”, Economica (1950)."]))
    assert all(f in out for f in fn) and "Doe, A." not in out and "Scott, A.D." not in out   # the cut resumes
    out = clean_code.clean("\n".join([PROSE] + refs + ["", "10", "The online appendix shows that this result also "
                                                       "extends to the unwinding of short positions in forwards."]))
    assert "The online appendix shows" in out and "Roe, B." not in out
    title = "3 On the Existence of a Consistent Course of Action when Tastes are Changing"
    assert title not in clean_code.clean("\n".join([PROSE] + refs + [title]))   # a cited title, not a footnote


def test_layout_stamps_go_and_table_rows_stay():
    stamps = [f"{PROSE}\n{PROSE}\nM14_KRUG9719_12_GE_C14.indd {n} 16/11/2021 16:16" for n in (381, 382, 383, 384)]
    assert ".indd" not in clean_code.clean("\n\n".join(stamps))
    rows = [f"{PROSE}\n{PROSE}\nAdj. R-Squared 0.{n}2 0.01 0.06" for n in range(4)]
    assert clean_code.clean("\n\n".join(rows)).count("Adj. R-Squared") == 4


def test_ocr_references_heading():
    assert clean_code.block_cut_spans(["Refermces", "Doe, A. (2001).", "APPENDIX"]) == [(0, 2, "APPENDIX")]
    assert clean_code.block_cut_spans(["Preferences", "Households maximize utility."]) == []


def test_citation_tail_does_not_end_the_cut():
    lines = ["References", "Orphanides, A., 2001, \"Monetary Policy Rules Based on Real-Time Data,\"",
             "FEDS 2001-53.", "Woodford, M., 2003, Interest and Prices.", "APPENDIX TABLES"]
    assert [(a, b) for a, b, _ in clean_code.block_cut_spans(lines)] == [(0, 4)]


def test_acronym_line_does_not_end_the_cut():
    lines = ["References", "Smith, J. (2010), Report,", "ECB", "Working Paper.", "EXERCISES", PROSE]
    assert clean_code.block_cut_spans(lines) == [(0, 4, "EXERCISES")]


def test_roman_numbered_and_literature_cited_headings():
    # "XI. References" ... "X. Appendix" (Goldfajn 2000); "LITERATURE CITED" (Krugman 1979)
    lines = ["XI. References", "Doe, A. (2001), Title.", "X. Appendix", PROSE]
    assert clean_code.block_cut_spans(lines) == [(0, 2, "X. Appendix")]
    lines = [PROSE, "LITERATURE CITED", "1. Brock, William A. \"A Simple Model.\""]
    assert clean_code.block_cut_spans(lines) == [(1, 3, "EOF")]
    assert clean_code.block_cut_spans(["XIV", PROSE]) == []    # a bare numeral is no heading


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


def test_reversed_text_flag():
    # A rotated table read backwards: "Table", "inflation", "rate" reversed on one page.
    body = [PROSE + " Table 1 shows the inflation rate and the exchange rate."] * 4
    rotated = "1 elbaT noitalfni etar egnahcxe 0.5 0.7"
    flags = qc.flags(body + [rotated], PROSE, PROSE, [])
    assert any(f.startswith("reversed_text (p.5: 4 words") for f in flags), flags
    assert qc.reversed_pages(body) == []
    # two stray reversals on a page are noise, not a rotated block
    assert qc.reversed_pages(body + ["elbaT etar"]) == []


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
    assert s["files"] and isinstance(s["topics_on_hold"], dict), "repository/ingestion/settings.yaml should load"


def test_sweep_states():
    # The real folders: every state must be one of the four, and a file marked needs_attention
    # in settings.yaml is never swept as "pending" (it would be retried every run).
    states = {r["file"]: r["state"] for t in run.topics() for r in run.scan(t)}
    assert set(states.values()) <= {"ingested", "pending", "needs_attention", "on_hold"}
    for name, entry in settings.load()["files"].items():
        if entry.get("status") and name in states:
            assert states[name] != "pending", name
    for topic in settings.load()["topics_on_hold"]:   # a held topic is never swept as pending
        assert all(r["state"] in ("on_hold", "ingested") for r in run.scan(topic)), topic


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
    # one row per book chapter: "Ch. 3" in the title is the "ch3" of the file name (Gali 2015 ch. 3 and 4 share words)
    book = "Monetary Policy, Inflation, and the Business Cycle (2nd ed.), Ch. "
    gali = [(12, {"gali"}, "2015", tracker._norm_tokens(book + "3 - The Basic New Keynesian Model")),
            (13, {"gali"}, "2015", tracker._norm_tokens(book + "4 - Monetary Policy Design in the Basic New Keynesian Model"))]
    assert tracker._match(tracker._parse_stem("basic_nk_model_ch3 (Gali, 2015)"), gali) == (12, None)
    assert tracker._match(tracker._parse_stem("monetary_policy_design_nk_ch4 (Gali, 2015)"), gali) == (13, None)
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


def test_ocr_tidy():
    # blank lines go (the cleaner would read each as a page edge and drop a table's numbers);
    # a dash glued to a number is a minus, a dash between two numbers is not
    raw = "Table 1\n\nAustralia 0.005 —0.67*** 0.01\n\n2.58\n\nbetween —0.5 and –3.2, in 1990—2000"
    assert extract._ocr_tidy(raw) == "Table 1\nAustralia 0.005 -0.67*** 0.01\n2.58\nbetween -0.5 and -3.2, in 1990—2000"


def test_ocr_reads_what_the_font_lost():
    # Tambakis & Tarashev (2012) p.36: the text layer prints 0.005 as "0005" in every mode
    name = "systematic_monetary_policy_forward_premium_puzzle (Tambakis & Tarashev, 2012).pdf"
    pdf = _pdf(name)
    try:
        extract.tesseract()
    except RuntimeError:
        pdf = None
    if pdf is None:
        print(f"   skip (no PDF or no Tesseract on this machine): {name}")
        return
    import fitz
    import tempfile
    with fitz.open(pdf) as doc, tempfile.TemporaryDirectory() as d:
        text, conf = extract._ocr_image(extract.tesseract(), doc[35], 0, Path(d))
    assert "0.005" in text and conf > extract.OCR_CONF_MIN, (conf, text[:200])


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
