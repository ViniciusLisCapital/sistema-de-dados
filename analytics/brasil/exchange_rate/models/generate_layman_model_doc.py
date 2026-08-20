"""Generates a plain-language internal PDF explaining the shipped Ridge
USD/BRL model (ridge_deviation_model.py) -- what it predicts, why each of
its 8 ingredients is in it, how it re-learns over time, how good it has
been, and how the dashboard's forecast tool works. Written for a
non-technical reader: no jargon left unexplained, no equations, no
rejected-channel history (shipped 8-channel spec only, per direct user
request -- contrast with generate_model_spec_pdf.py, which is the
technical, per-tab companion document for the same dashboard and does
carry that history).

Same reportlab/Platypus approach and LIS brand colors/fonts as
generate_model_spec_pdf.py (font registration and palette copied from
there), but no matplotlib/mathtext machinery -- this document's whole
point is avoiding notation.

Static content, not live-computed: every number here is hand-transcribed
from ridge_deviation_model.py's own docstrings, analytics/brasil/exchange_rate/
CLAUDE.md, and referencia/equilibrium_model/ridge_window_horizon_grid.md as of 2026-07-31.
If the model is refit/reespecified, update this file's numbers by hand in
the same session (same convention generate_model_spec_pdf.py documents).

Usage:
    uv run python -c "from analytics.brasil.exchange_rate.models.generate_layman_model_doc import run; run()"
"""

import os

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    HRFlowable,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

import matplotlib

_MPL_TTF = os.path.join(matplotlib.get_data_path(), "fonts", "ttf")
# Same DejaVu Sans registration as generate_model_spec_pdf.py -- full Greek/
# accented-character Unicode coverage the base-14 PDF fonts don't have, and
# reused rather than re-registered differently so both PDFs render identically.
pdfmetrics.registerFont(TTFont("DejaVuSans", os.path.join(_MPL_TTF, "DejaVuSans.ttf")))
pdfmetrics.registerFont(TTFont("DejaVuSans-Bold", os.path.join(_MPL_TTF, "DejaVuSans-Bold.ttf")))
pdfmetrics.registerFont(TTFont("DejaVuSans-Oblique", os.path.join(_MPL_TTF, "DejaVuSans-Oblique.ttf")))
pdfmetrics.registerFont(TTFont("DejaVuSans-BoldOblique", os.path.join(_MPL_TTF, "DejaVuSans-BoldOblique.ttf")))
pdfmetrics.registerFontFamily(
    "DejaVuSans", normal="DejaVuSans", bold="DejaVuSans-Bold",
    italic="DejaVuSans-Oblique", boldItalic="DejaVuSans-BoldOblique",
)

NAVY = colors.HexColor("#1F2853")
GOLD = colors.HexColor("#BB9B1D")
GREEN = colors.HexColor("#418791")
RED = colors.HexColor("#EA523A")
MUTED = colors.HexColor("#7A88A8")
LINE = colors.HexColor("#D8DCE6")
BG_SOFT = colors.HexColor("#F4F5F7")

OUT_PATH = os.path.join("reports", "brasil", "ridge_model_explained.pdf")

# ---------------------------------------------------------------------------
# Paragraph styles -- larger body text, more whitespace, simpler than the
# technical companion PDF, matching the "explain it simply" brief.
# ---------------------------------------------------------------------------
TITLE = ParagraphStyle("Title", fontName="DejaVuSans-Bold", fontSize=22, leading=27, textColor=NAVY, spaceAfter=4)
SUBTITLE = ParagraphStyle("Subtitle", fontName="DejaVuSans", fontSize=12, leading=16, textColor=MUTED, spaceAfter=2)
DATE_BADGE = ParagraphStyle("DateBadge", fontName="DejaVuSans", fontSize=9, leading=11, textColor=MUTED)

H1 = ParagraphStyle("H1", fontName="DejaVuSans-Bold", fontSize=16, leading=20, textColor=NAVY, spaceBefore=6, spaceAfter=2)
H1_TAG = ParagraphStyle("H1Tag", fontName="DejaVuSans-Oblique", fontSize=10, leading=13, textColor=GOLD, spaceAfter=8)
H2 = ParagraphStyle("H2", fontName="DejaVuSans-Bold", fontSize=11.5, leading=14, textColor=NAVY, spaceBefore=10, spaceAfter=4)

BODY = ParagraphStyle("Body", fontName="DejaVuSans", fontSize=10.6, leading=15.5, textColor=colors.HexColor("#1A1A1A"), spaceAfter=8, alignment=4)
BODY_TIGHT = ParagraphStyle("BodyTight", parent=BODY, spaceAfter=4)
BULLET = ParagraphStyle("Bullet", parent=BODY, leftIndent=14, bulletIndent=0, spaceAfter=5)

CAUTION_LABEL = ParagraphStyle("CautionLabel", fontName="DejaVuSans-Bold", fontSize=9.6, leading=13, textColor=RED, spaceAfter=2)
CAUTION_BODY = ParagraphStyle("CautionBody", parent=BODY, fontSize=9.8, leading=14, textColor=colors.HexColor("#3A2020"), spaceAfter=0)

FOOTER = ParagraphStyle("Footer", fontName="DejaVuSans", fontSize=7.8, leading=10, textColor=MUTED, alignment=1)


def rule(color=GOLD, thickness=1.4, space_before=2, space_after=10):
    return HRFlowable(width="100%", thickness=thickness, color=color, spaceBefore=space_before, spaceAfter=space_after)


def section_header(number, title_text, subtitle_text):
    return [
        Paragraph(f"{number}. {title_text}", H1),
        Paragraph(subtitle_text, H1_TAG),
        rule(),
    ]


def ingredient_card(name, plain_name, definition, thesis, direction_note=None):
    """One shaded box per ingredient -- name the everyday way, one-sentence
    definition avoiding jargon, then the plain-English thesis for why it's
    believed to move the exchange rate. direction_note, when given, is an
    extra callout for a counter-intuitive sign (only real_yield_diff needs
    this among the 8 shipped channels)."""
    rows = [
        [Paragraph(f'<font color="#BB9B1D"><b>{name}</b></font> <font color="#7A88A8">— {plain_name}</font>', ParagraphStyle("ing_h", fontName="DejaVuSans-Bold", fontSize=11.2, leading=14))],
        [Paragraph(f"<b>What it is:</b> {definition}", BODY_TIGHT)],
        [Paragraph(f"<b>Why we think it matters:</b> {thesis}", BODY_TIGHT)],
    ]
    if direction_note:
        rows.append([Paragraph(f"<b>Worth noting:</b> {direction_note}", ParagraphStyle("note", parent=BODY_TIGHT, textColor=colors.HexColor("#7A4A00")))])
    t = Table(rows, colWidths=[440])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), BG_SOFT),
        ("BOX", (0, 0), (-1, -1), 0.7, LINE),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    return t


def results_table(rows, col_widths=None):
    data = [[Paragraph(c, ParagraphStyle("th", fontName="DejaVuSans-Bold", fontSize=9.2, leading=11.5, textColor=colors.white)) for c in rows[0]]]
    body_style = ParagraphStyle("td", fontName="DejaVuSans", fontSize=9.2, leading=12)
    for r in rows[1:]:
        data.append([Paragraph(c, body_style) for c in r])
    t = Table(data, colWidths=col_widths, repeatRows=1)
    style = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("GRID", (0, 0), (-1, -1), 0.5, LINE),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style.append(("BACKGROUND", (0, i), (-1, i), BG_SOFT))
    t.setStyle(TableStyle(style))
    return t


def caution(text, label="Honest caveat"):
    return [
        Paragraph(label, CAUTION_LABEL),
        Paragraph(text, CAUTION_BODY),
        Spacer(1, 6),
    ]


def _footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("DejaVuSans", 7.8)
    canvas.setFillColor(MUTED)
    canvas.drawCentredString(A4[0] / 2, 12 * mm, f"LIS Capital — How the Exchange Rate Model Works · page {doc.page}")
    canvas.restoreState()


# ---------------------------------------------------------------------------
# Document body
# ---------------------------------------------------------------------------

def build_story():
    story = []

    # --- Cover / intro -------------------------------------------------
    story.append(Paragraph("LIS CAPITAL", ParagraphStyle("brand", fontName="DejaVuSans-Bold", fontSize=10, textColor=GOLD, spaceAfter=2)))
    story.append(Paragraph("How the Exchange Rate Model Works", TITLE))
    story.append(Paragraph("A plain-language guide to the USD/BRL forecasting model", SUBTITLE))
    story.append(Paragraph("Internal document · July 2026", DATE_BADGE))
    story.append(rule(color=NAVY, thickness=2, space_before=8, space_after=12))

    story.append(Paragraph(
        "This model tries to guess how much the Brazilian Real will move against the US Dollar each month, "
        "using 8 pieces of real-world information. This document explains, in plain language, what those 8 "
        "pieces are, why we picked each one, how the model keeps itself up to date, how good its guesses have "
        "actually been, and how you can use the dashboard's new tool to test your own \"what if\" scenarios for "
        "the next 12 months.",
        BODY,
    ))
    story.append(Paragraph(
        "No formulas, no statistics jargon — just the ideas.",
        BODY,
    ))
    story.append(Spacer(1, 6))

    # ========================================================================
    # 1. The big idea
    # ========================================================================
    story += section_header("1", "The Big Idea", "How the model turns information into a guess")

    story.append(Paragraph(
        "Think of the model as a recipe. Every month, it looks at how much 8 different real-world things "
        "changed — for example, how much riskier Brazil looked to investors, or how strong the US dollar was "
        "against currencies worldwide. Over about 18 years of history, the model has learned roughly how much "
        "each of those changes tends to push the Real up or down against the Dollar.",
        BODY,
    ))
    story.append(Paragraph(
        "Each month, it adds up all 8 \"pushes,\" plus one more ingredient — the exchange rate's own momentum "
        "from the month before — to produce its best single guess for how much the Real will move this month.",
        BODY,
    ))
    story.append(Paragraph(
        "It's a bit like a recipe where every ingredient has a learned \"how much it matters\" weight. A pinch "
        "of salt changes a dish less than a cup of sugar — the model has learned similar weights for its 8 "
        "ingredients, based on what has actually moved the exchange rate in the past.",
        BODY,
    ))
    story.append(Paragraph(
        "One important detail: those weights aren't fixed forever. Section 4 explains why, and how the model "
        "keeps re-measuring them.",
        BODY,
    ))
    story.append(PageBreak())

    # ========================================================================
    # 2. The 8 ingredients
    # ========================================================================
    story += section_header("2", "The 8 Ingredients", "What the model watches, and why each one is believed to matter")

    story.append(Paragraph(
        "These are the 8 pieces of information the model uses every month. Each one was chosen because, when "
        "tested against nearly two decades of real history, it reliably helped explain the Real's actual moves — "
        "not because it sounded reasonable in theory.",
        BODY,
    ))
    story.append(Spacer(1, 4))

    story.append(ingredient_card(
        "Fiscal Risk", "how worried investors are about Brazil's government finances",
        "The price of a kind of insurance investors buy to protect against Brazil failing to pay its debts "
        "(in the market, this is called a \"credit default swap,\" or CDS). When that insurance gets more "
        "expensive, it means investors are getting more nervous about Brazil's fiscal health.",
        "When investors get more worried about Brazil's government finances, they tend to demand a weaker Real "
        "as compensation for the extra risk. This has been one of the single strongest ingredients in the "
        "whole model.",
    ))
    story.append(Spacer(1, 8))

    story.append(ingredient_card(
        "Interest-Rate Advantage per Unit of Risk", "how attractive Brazil's interest rates are, adjusted for how bumpy the ride is",
        "Brazil usually pays a higher interest rate than the US. Investors can borrow cheaply in dollars and "
        "invest in Brazilian assets to pocket that difference (a strategy known as the \"carry trade\") — but "
        "only if the Real isn't swinging around too wildly, since a bumpy currency can wipe out the extra "
        "interest earned. This ingredient divides Brazil's rate advantage by how bumpy the Real has recently "
        "been.",
        "When Brazil's rate advantage is large and the currency is calm, that combination tends to attract more "
        "money into Brazil, which should support (not weaken) the Real. When the ride gets bumpy, that same "
        "rate advantage becomes less attractive, and money can flow back out.",
    ))
    story.append(Spacer(1, 8))

    story.append(ingredient_card(
        "Global Dollar Strength", "whether the US Dollar is broadly strong or weak against major world currencies",
        "A widely used index (the \"Dollar Index,\" or DXY) that tracks the Dollar against a basket of major "
        "currencies like the Euro, Yen, and British Pound — mostly other large, developed economies.",
        "When the Dollar strengthens broadly against the whole world, it usually strengthens against the Real "
        "too, for reasons that have little to do with Brazil specifically — it's simply a stronger Dollar "
        "everywhere.",
    ))
    story.append(Spacer(1, 8))

    story.append(ingredient_card(
        "Emerging-Market Dollar Strength", "whether the US Dollar is strong specifically against other emerging-market currencies",
        "A separate index (built by the US Federal Reserve) that tracks the Dollar against a basket of about 19 "
        "emerging-market currencies — Brazil, China, Mexico, South Korea, and others — rather than against "
        "major developed-market currencies.",
        "The Real doesn't just move with the Dollar in general — it often moves together with the whole group "
        "of emerging-market currencies specifically, as global investors shift money in or out of \"emerging "
        "markets\" as a category. This ingredient captures that group movement separately from the broader "
        "Dollar-strength ingredient above.",
    ))
    story.append(Spacer(1, 8))
    story.append(PageBreak())

    story.append(ingredient_card(
        "Inflation-Protected Bond Curve Steepening", "how much more Brazil pays to borrow for 10 years versus 2 years, after stripping out inflation",
        "The extra interest rate Brazil pays on 10-year government bonds compared to 2-year bonds, using bonds "
        "that are protected against inflation. When this gap widens (\"steepens\"), it means long-term lending "
        "to Brazil has become relatively more expensive than short-term lending.",
        "This is another way of reading fiscal risk — but focused purely on the real (inflation-adjusted) cost "
        "of long-term borrowing, separate from the CDS-based fiscal-risk ingredient above. Brazil holds large "
        "dollar reserves, which makes an outright default on foreign debt unlikely even when domestic finances "
        "look shakier — so this ingredient can pick up worries that the CDS insurance price doesn't fully "
        "capture.",
    ))
    story.append(Spacer(1, 8))

    story.append(ingredient_card(
        "The US Stock Market", "how the S&amp;P 500 (a broad US stock index) has been performing",
        "The monthly change in the S&amp;P 500, one of the most widely followed measures of the US stock "
        "market.",
        "When US stocks are doing well, global investors have an attractive, safe place to put their money "
        "without leaving the US at all — money that might otherwise have gone to emerging markets like Brazil "
        "stays home instead. Think of it as US stocks \"competing\" with Brazil for the same pool of investor "
        "money. What matters here is specifically how the stock market's price is moving, not a general \"fear "
        "gauge\" of investor nervousness — a separate fear-based measure was tested and did not add anything "
        "once this one was already included.",
    ))
    story.append(Spacer(1, 8))

    story.append(ingredient_card(
        "Brazil-US Real Interest Rate Gap", "a second, independent read on how much risk investors see in Brazil",
        "The gap between Brazil's 10-year inflation-protected government bond rate and the equivalent US "
        "10-year inflation-protected rate.",
        "This ingredient is not another version of the carry-trade ingredient above — it's a <b>risk-premium "
        "gauge</b>, like fiscal risk and curve steepening, just measured through interest rates instead of an "
        "insurance price or a borrowing-cost gap. The idea: when investors demand an unusually high real "
        "interest rate to hold Brazilian government debt, that's usually them pricing in extra risk, not "
        "just offering a reward for patient investors.",
        direction_note=(
            "Because this ingredient measures risk rather than reward, it moves the exchange rate the "
            "<b>opposite</b> way from a typical carry-trade ingredient. A bigger gap has actually gone together "
            "with a <b>weaker</b> Real, not a stronger one — consistent with reading it as a warning sign about "
            "risk, the same underlying story as the fiscal-risk and curve-steepening ingredients, not a "
            "coincidence or a data quirk."
        ),
    ))
    story.append(Spacer(1, 8))
    story.append(PageBreak())

    story.append(ingredient_card(
        "Commodity Prices (in Dollars)", "the dollar price of the basket of raw materials Brazil exports",
        "A broad index of commodity prices — things like iron ore, soybeans, and oil — priced in US Dollars, "
        "tracking what Brazil earns from its major exports.",
        "Brazil is a major commodity exporter. When commodity prices rise in dollar terms, more dollars flow "
        "into the country from exports, which tends to strengthen the Real. This turned out to be one of the "
        "single most powerful ingredients added to the model — its effect has been reliably in this direction "
        "across almost the entire history tested.",
    ))
    story.append(Spacer(1, 8))

    story.append(Paragraph(
        "Plus one more ingredient that isn't really \"news\" about the world: the exchange rate's own momentum "
        "from last month. Currencies, like many things in economics, tend to keep moving a little in the same "
        "direction they were already moving — this ingredient lets the model account for that momentum "
        "directly, on top of the 8 news-driven ingredients above.",
        BODY,
    ))
    story.append(PageBreak())

    # ========================================================================
    # 3. How the model re-learns over time
    # ========================================================================
    story += section_header("3", "How the Model Keeps Itself Up to Date", "Why the recipe's weights are re-measured, not fixed forever")

    story.append(Paragraph(
        "The relationship between these 8 ingredients and the exchange rate doesn't stay exactly the same "
        "forever. What mattered most in, say, 2015 might matter a bit differently today — the Brazilian and "
        "global economy keep changing, and a model that assumed one fixed relationship across 18 years would "
        "be describing an average of very different periods, calm and turbulent alike.",
        BODY,
    ))
    story.append(Paragraph(
        "So instead of measuring the weights once and freezing them, the model re-measures them regularly: "
        "every month, it looks back over the most recent 6 years of data, re-learns how much each of the 8 "
        "ingredients currently matters, and drops the oldest month from that 6-year window. It's a rolling "
        "6-year memory, not a fixed, forever answer.",
        BODY,
    ))
    story.append(Paragraph(
        "This means the \"recipe\" you'd see today is not identical to the one the model would have shown five "
        "years ago — both are legitimate readings, just taken from different windows of experience.",
        BODY,
    ))
    story += caution(
        "The model is also careful not to overreact to any single ingredient's month-to-month noise. Behind "
        "the scenes, it applies a mild \"be careful not to overfit\" brake (called Ridge regularization) that "
        "keeps its weights sensible even when a few of the 8 ingredients happen to move in similar ways at the "
        "same time. You don't need to know how this works — only that it's a deliberate safeguard, not an "
        "afterthought.",
        label="A technical safeguard, in one sentence",
    )
    story.append(PageBreak())

    # ========================================================================
    # 4. How good has it been?
    # ========================================================================
    story += section_header("4", "How Good Has It Been?", "Judging the model honestly, in plain numbers")

    story.append(Paragraph(
        "Two different questions matter here, and they have two different answers: (1) how well does the model "
        "explain the moves that already happened, and (2) how well can it actually forecast moves it hasn't "
        "seen yet? The second question is the harder, more honest test.",
        BODY,
    ))

    story.append(Paragraph("Explaining the past", H2))
    story.append(Paragraph(
        "Looking back across its full ~18-year history, the model's 8 ingredients together explain roughly "
        "61% of the actual month-to-month moves in the exchange rate (using its most recent 6-year "
        "\"memory window\" — the same window described in Section 3). The remaining share is noise, surprises, "
        "and short-term moves the 8 ingredients simply don't capture — no model of a currency this actively "
        "traded should be expected to explain everything.",
        BODY,
    ))

    story.append(Paragraph("Genuinely forecasting the future", H2))
    story.append(Paragraph(
        "A more demanding test asks: if you only gave the model information up to some point in the past, how "
        "close would its guess have come to what actually happened over the following months? This was tested "
        "directly, many times, across the whole history. The clear pattern: the further out you ask the model "
        "to guess, the less precise that guess becomes — a 3-month-ahead guess is meaningfully more reliable "
        "than a 12-month-ahead one.",
        BODY,
    ))
    story.append(results_table(
        [
            ["Looking ahead", "How well it explains the outcome", "Typical size of the miss*"],
            ["3 months", "About 65 out of 100", "Smallest"],
            ["6 months", "About 67 out of 100", "Small"],
            ["9 months", "About 65 out of 100", "Medium"],
            ["12 months", "About 61 out of 100", "Largest"],
        ],
        col_widths=[110, 190, 150],
    ))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "*\"Typical size of the miss\" is a plain-language stand-in for the actual measured forecast error at "
        "each horizon — the exact numbers behind this table live in the technical companion document. The "
        "\"how well it explains\" column uses a 0–100 scale where 100 would mean a perfect guess every time and "
        "0 would mean no better than always guessing \"no change.\"",
        ParagraphStyle("fn", fontName="DejaVuSans-Oblique", fontSize=8.4, textColor=MUTED, spaceAfter=8),
    ))
    story.append(Paragraph(
        "This table uses the model's current setting of a 6-year \"memory window\" (see Section 3), which "
        "testing found to be the most reliable single choice across every time horizon from 3 to 12 months — "
        "not the largest possible window, and not the smallest, but the one that held up best overall.",
        BODY,
    ))

    story += caution(
        "The model's ability to explain what's happening has been gradually getting harder in the last few "
        "years compared to earlier in its history. This doesn't mean the model is \"broken\" — currency markets "
        "go through periods that are simply harder to explain with any fixed set of ingredients — but it's an "
        "honest signal to hold the more recent forecasts a bit more loosely than the historical average would "
        "suggest, and to keep watching whether this trend continues.",
    )
    story.append(PageBreak())

    # ========================================================================
    # 5. The forecast tool
    # ========================================================================
    story += section_header("5", "The Forecast Tool on the Dashboard", "How to test your own \"what if\" scenario for the next 12 months")

    story.append(Paragraph(
        "The dashboard includes a hands-on tool that lets you type in your own expectations for each of the 8 "
        "ingredients over the next 12 months, and see what the model would guess for the exchange rate under "
        "that scenario — without needing to touch any code or run anything yourself.",
        BODY,
    ))

    story.append(Paragraph("Entering your own numbers", H2))
    story.append(Paragraph(
        "For each of the 8 ingredients, you get 12 boxes — one per month ahead. You can fill each box in "
        "whichever way is easier for you to think in: the actual expected level of that ingredient (for "
        "example, \"the fiscal-risk insurance price will be around 250\"), or the expected percentage change "
        "from the month before (for example, \"up 3% from last month\"). A toggle button switches the boxes "
        "between these two ways of entering the same information — the model translates either one into "
        "exactly what it needs behind the scenes.",
        BODY,
    ))

    story.append(Paragraph("Checking your guess against history", H2))
    story.append(Paragraph(
        "Next to each ingredient, a \"Show regressor chart\" button reveals a chart with that ingredient's "
        "entire history, plus the path you just typed in continuing forward as a dashed line. This is a "
        "sanity check — it lets you see at a glance whether the numbers you entered are realistic compared to "
        "how that ingredient has actually behaved in the past, or whether you've accidentally typed in "
        "something far outside anything ever observed. The same chart also has a toggle to show the numbers as "
        "\"how unusual is this level compared to its own history,\" which can make an extreme scenario even "
        "easier to spot.",
        BODY,
    ))

    story.append(Paragraph("Reading the uncertainty band", H2))
    story.append(Paragraph(
        "Any 12-month-ahead guess comes with real uncertainty, and it grows the further out you look — exactly "
        "the pattern shown in Section 4's table. The forecast chart shows this directly as a widening band "
        "around the central guess: narrower for month 1, wider for month 12. That band wasn't guessed at — it "
        "was measured by testing the model, over and over, on 6 years of real past data, checking each time "
        "how far off its guess tended to be at 1 month ahead, 2 months ahead, and so on up to 12, and using "
        "that history of misses to size the band at every step.",
        BODY,
    ))
    story += caution(
        "This tool tells you what the model would guess <b>given your own assumptions</b> about the 8 "
        "ingredients — it does not forecast those 8 ingredients themselves. If your assumptions turn out to be "
        "wrong, the resulting exchange-rate guess will be wrong in the same way, no matter how carefully the "
        "underlying model was built. Use the regressor charts described above to keep your own assumptions "
        "grounded in what has actually happened before.",
        label="What this tool can and can't do",
    )

    return story


def run():
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    doc = SimpleDocTemplate(
        OUT_PATH, pagesize=A4,
        topMargin=20 * mm, bottomMargin=18 * mm, leftMargin=22 * mm, rightMargin=22 * mm,
        title="How the Exchange Rate Model Works",
    )
    doc.build(build_story(), onFirstPage=_footer, onLaterPages=_footer)
    print(f"Wrote {OUT_PATH}")


if __name__ == "__main__":
    run()
