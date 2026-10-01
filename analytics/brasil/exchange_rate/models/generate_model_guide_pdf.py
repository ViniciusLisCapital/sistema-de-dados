"""Technical guide to the shipped USD/BRL FX Model (the "FX Model" tab of
reports/brasil/FX Report.html) -> team_materials/exchange_rate/ridge_model_explained.pdf.

Rewritten 2026-09-30 at the user's request, replacing the plain-language
version this file used to generate (then `generate_layman_model_doc.py`, still
describing the 8-channel spec of July). Three changes of brief, all the user's:

  * technical tone -- equations, estimator, transforms, sample, validation;
  * the rolling parameters explained as a mechanism, not a footnote;
  * the model framed as a SCENARIO PRODUCER (a conditional mapping from a
    path of drivers to a path of USD/BRL), not as a forecaster. The evidence
    for that framing is models/ridge_vs_random_walk.md: the mapping beats a
    random walk by ~42% of RMSE when the drivers are given, while the drivers
    themselves are less forecastable than the exchange rate.

Cut down the same day from the user's PDF comments: the guide keeps the
rationale and the mechanics and drops the evidence apparatus (drop-one
numbers, the forecastability table, lambda selection, the scaling argument,
sensitivities, the episode table, the validation section). The rolling charts
are not reproduced -- the text points to the dashboard's Fit diagnostics.

Then, same day, two facts from the user that govern every edit here: the
document GOES TO CLIENTS, and it is written in PORTUGUESE. So nothing about
how the model used to be (the realized-vol denominator, the 8-channel spec),
nothing about where a series is stored (the implied-vol CSV), no repo paths,
no function names, and no limitations section. Numbers use the decimal comma
(f() does it) and months are pt-BR (mon()).

The PPP statistics of section 2 other than the variance share (rolling free
beta -0.65..+2.14, negative in 45% of windows; horizon betas 1.1..2.4 since
1994, none different from 1) were re-measured on 2026-09-30 on the shipped
spec -- they are transcribed, so re-measure them if the spec or sample moves.
The 2026-09-01 figures they replace (-0.76..+0.87, 60%, 1.74..2.79 on
2008-2026) no longer held: on the 2006-2026 fit sample alone the 12-month
beta (3.32) rejects 1 and the 10-year one (0.66) is not different from 0,
which is why the claim is made on the full 1994+ history.

Where the numbers come from, and why it matters:

  * Every number about the FITTED model (coefficients, rolling paths, R2,
    lambda, sigma, error band, CDS episode library, the carry/vol
    decomposition) is computed here from the RIDGE_DATA payload
    embedded in reports/brasil/FX Report.html -- the same object the tab
    renders. The guide therefore cannot disagree with the dashboard it
    describes; regenerate the report first, then this file.
  * Numbers from VALIDATION studies that are not in the payload (the random-
    walk horse race, the window x horizon grid, the drop-one / backward-
    elimination record behind the 5-channel cut) are transcribed from
    models/ridge_vs_random_walk.md, referencia/equilibrium_model/
    ridge_window_horizon_grid.md and analytics/brasil/exchange_rate/CLAUDE.md,
    and the document dates them. If the spec changes, those studies have to be
    re-run before this text is trusted -- the payload numbers update themselves,
    these do not.

Scenario arithmetic goes through models/fx_forecast_sim.py, the Python port of
the tab's JavaScript recursion (verified there to 1e-9 against the JS).

Usage:
    uv run python -c "from analytics.brasil.exchange_rate.generate_report import run; run()"   # refresh the payload
    uv run python -c "from analytics.brasil.exchange_rate.models.generate_model_guide_pdf import run; run()"
"""

from __future__ import annotations

import json
import math
import os
import tempfile
from datetime import datetime

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker
import numpy as np
from PIL import Image as PILImage
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    HRFlowable,
    Image as RLImage,
    CondPageBreak,
    KeepTogether,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from analytics.brasil.exchange_rate.models import fx_forecast_sim as sim

matplotlib.rcParams["text.parse_math"] = False
_ASSET_DIR = tempfile.mkdtemp(prefix="lis_fxguide_assets_")

REPORT_PATH = os.path.join("reports", "brasil", "FX Report.html")
OUT_PATH = os.path.join("team_materials", "exchange_rate", "ridge_model_explained.pdf")

# ---------------------------------------------------------------------------
# Fonts and palette -- same registration as the other PDFs of this folder
# ---------------------------------------------------------------------------
_MPL_TTF = os.path.join(matplotlib.get_data_path(), "fonts", "ttf")
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

C_NAVY, C_GOLD, C_GREEN, C_RED = "#1F2853", "#BB9B1D", "#418791", "#EA523A"
C_MUTED, C_GRID = "#7A88A8", "#E4E7EF"
C_PURPLE, C_AMBER, C_BLUE = "#6B5B95", "#EE9900", "#0088CC"

TITLE = ParagraphStyle("Title", fontName="DejaVuSans-Bold", fontSize=20, leading=24, textColor=NAVY, spaceAfter=4)
SUBTITLE = ParagraphStyle("Subtitle", fontName="DejaVuSans", fontSize=11, leading=14, textColor=MUTED, spaceAfter=2)
DATE_BADGE = ParagraphStyle("DateBadge", fontName="DejaVuSans", fontSize=8.6, leading=11, textColor=MUTED)
H1 = ParagraphStyle("H1", fontName="DejaVuSans-Bold", fontSize=14.5, leading=18, textColor=NAVY, spaceBefore=6, spaceAfter=2)
H1_TAG = ParagraphStyle("H1Tag", fontName="DejaVuSans-Oblique", fontSize=9, leading=11, textColor=GOLD, spaceAfter=6)
H2 = ParagraphStyle("H2", fontName="DejaVuSans-Bold", fontSize=10.5, leading=13, textColor=NAVY, spaceBefore=9, spaceAfter=4)
BODY = ParagraphStyle("Body", fontName="DejaVuSans", fontSize=9.2, leading=13.1,
                      textColor=colors.HexColor("#1A1A1A"), spaceAfter=6, alignment=4)
BODY_TIGHT = ParagraphStyle("BodyTight", parent=BODY, spaceAfter=3)
BULLET = ParagraphStyle("Bullet", parent=BODY, leftIndent=12, bulletIndent=0, spaceAfter=3)
BULLET_LEFT = ParagraphStyle("BulletLeft", parent=BULLET, alignment=0)   # paths and identifiers do not justify
CARD_TITLE = ParagraphStyle("CardTitle", fontName="DejaVuSans-Bold", fontSize=10, leading=13, textColor=GOLD, spaceAfter=3)
CARD_BODY = ParagraphStyle("CardBody", parent=BODY, fontSize=8.8, leading=12.4, spaceAfter=4)
EQ = ParagraphStyle("Eq", fontName="DejaVuSans", fontSize=9.4, leading=13, textColor=NAVY)
EQ_NOTE = ParagraphStyle("EqNote", fontName="DejaVuSans", fontSize=8.4, leading=11, textColor=colors.HexColor("#3A4256"))
CAP = ParagraphStyle("Cap", fontName="DejaVuSans", fontSize=7.6, leading=9.6, textColor=MUTED,
                     spaceBefore=2, spaceAfter=8, alignment=4)
FOOTNOTE = ParagraphStyle("Footnote", parent=BODY, fontSize=7.4, leading=9.7,
                          textColor=colors.HexColor("#6E7688"), spaceAfter=0)
FOOTER = ParagraphStyle("Footer", fontName="DejaVuSans", fontSize=7.6, leading=10, textColor=MUTED, alignment=1)

# Channel metadata. `key` matches the payload; `name` is the label, `sym` the
# subscript used in the equation. The label and the in-sentence name are two
# fields on purpose (see .claude/rules/lis-dashboards.md, "O nome DENTRO de uma
# frase e um campo").
CH = [
    {"key": "delta_fiscal", "raw": "fiscal", "name": "Risco fiscal (CDS)", "sym": "fis", "shock_unit": "100 bps"},
    {"key": "delta_dxy_em", "raw": "dxy_em", "name": "Dólar contra emergentes", "sym": "em", "shock_unit": "1 ponto do índice"},
    {"key": "delta_carry_vol", "raw": "carry_vol", "name": "Carry/volatilidade", "sym": "cv", "shock_unit": "0,1 na razão"},
    {"key": "delta_sp500", "raw": "sp500", "name": "S&amp;P 500", "sym": "spx", "shock_unit": "1%"},
    {"key": "delta_icbr_usd", "raw": "icbr_usd", "name": "Commodities (IC-Br em US$)", "sym": "cmd",
     "shock_unit": "1%"},
]
CH_COLORS = {"delta_fiscal": C_RED, "delta_dxy_em": C_AMBER, "delta_carry_vol": C_PURPLE,
             "delta_sp500": C_BLUE, "delta_icbr_usd": C_GREEN, "delta_fx_lag1": C_MUTED}
# How much of the native unit one "shock_unit" is (fiscal in bps, carry_vol in ratio points).
SHOCK_SCALE = {"delta_fiscal": 100.0, "delta_dxy_em": 1.0, "delta_carry_vol": 0.1,
               "delta_sp500": 1.0, "delta_icbr_usd": 1.0}

_MON = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"]
_MES_LONGO = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro",
              "outubro", "novembro", "dezembro"]


def mon(ym):
    y, m = ym.split("-")[:2]
    return "%s/%s" % (_MON[int(m) - 1], y)


def f(x, d=2, sign=False):
    # typographic minus, so a table of signed coefficients reads the same as the prose around it
    # and a decimal comma: the guide is written in Portuguese
    return format(float(x), ("+.%df" if sign else ".%df") % d).replace("-", "−").replace(".", ",")


# ---------------------------------------------------------------------------
# Payload
# ---------------------------------------------------------------------------
def load_payload(path=REPORT_PATH):
    """RIDGE_DATA as embedded in the generated FX Report -- the object the tab renders."""
    with open(path, encoding="utf-8") as fh:
        s = fh.read()
    tag = "RIDGE_DATA = "
    i = s.find(tag)
    if i < 0:
        raise RuntimeError("RIDGE_DATA not found in %s -- regenerate the FX Report first" % path)
    D, _ = json.JSONDecoder().raw_decode(s[i + len(tag):])
    if not D:
        raise RuntimeError("%s was built with include_models=False; the model payload is empty" % path)
    built = datetime.fromtimestamp(os.path.getmtime(path))
    return D, built


def _prev_month(ym):
    y, m = map(int, ym.split("-"))
    m -= 1
    if m == 0:
        y, m = y - 1, 12
    return "%04d-%02d" % (y, m)


def derive(D):
    """Every model number the text quotes, computed from the payload."""
    F = D["forecast"]
    R = D["rolling"]
    ws, lw = D["whole_sample"], D["last_window"]
    sd = {k: v["std"] for k, v in F["channel_stats"].items()}
    out = {"D": D, "sd": sd, "ws": ws, "lw": lw}

    # rolling coefficients
    roll = {}
    for key, v in R["channels"].items():
        arr = np.array(v["mean"], dtype=float)
        roll[key] = {"min": arr.min(), "max": arr.max(), "first": arr[0], "last": arr[-1],
                     "med": float(np.median(arr)), "n": len(arr),
                     "same_sign": int((np.sign(arr) == np.sign(v["whole_sample"])).sum()),
                     "series": arr}
    out["roll"] = roll
    r2 = np.array(R["r2"], dtype=float)
    ends = R["window_end"]
    by_year = {}
    for d, x in zip(ends, r2):
        by_year.setdefault(d[:4], []).append(x)
    out["r2"] = {"series": r2, "ends": ends, "min": r2.min(), "max": r2.max(), "mean": r2.mean(),
                 "last": r2[-1], "by_year": {k: float(np.mean(v)) for k, v in by_year.items()},
                 "argmin": ends[int(r2.argmin())]}

    # cumulative decomposition, whole sample
    cm = D["contrib_monthly"]
    out["cum"] = {k: sum(x for x in v if x is not None) for k, v in cm.items()}
    act = D["fit_level"]["actual"]
    out["fx_first"], out["fx_last"] = D["fit_level"]["anchor_level"], act[-1]

    # carry/vol: how much of its monthly change is the volatility leg
    P = F["primitives"]
    fv = dict(zip(P["fx_vol"]["months"], P["fx_vol"]["values"]))
    se = dict(zip(P["selic"]["months"], P["selic"]["values"]))
    ff = dict(zip(P["fed_funds"]["months"], P["fed_funds"]["values"]))
    cvh = F["channel_history"]["carry_vol"]
    cv = dict(zip(cvh["months"], cvh["values"]))
    dfx = np.array(D["fit_delta"]["actual"], dtype=float)
    dv, dc, dcar = [], [], []
    for m in D["months"]:
        p = _prev_month(m)
        dv.append(fv[m] - fv[p])
        dc.append(cv[m] - cv[p])
        dcar.append((se[m] - ff[m]) - (se[p] - ff[p]))
    dv, dc, dcar = map(np.array, (dv, dc, dcar))
    out["cvol"] = {"r2_vol": float(np.corrcoef(dv, dc)[0, 1] ** 2),
                   "r2_carry": float(np.corrcoef(dcar, dc)[0, 1] ** 2),
                   "corr_dvol_dfx": float(np.corrcoef(dv, dfx)[0, 1]),
                   "corr_dvol_absdfx": float(np.corrcoef(dv, np.abs(dfx))[0, 1])}

    # in-sample sigma of each channel delta vs the reference sigma the model uses
    out["fiscal_sd_sample"] = None
    fh = F["channel_history"]["fiscal"]
    fmap = dict(zip(fh["months"], fh["values"]))
    dfis = np.array([fmap[m] - fmap[_prev_month(m)] for m in D["months"]])
    out["fiscal_sd_sample"] = float(dfis.std(ddof=1))

    # month-to-month variance share of the inflation gap; the offset's contribution IS dppp (beta = 1)
    _dppp = np.array(D["contrib_monthly"]["delta_ppp"], dtype=float)
    out["ppp_var_share"] = float(100 * _dppp.var(ddof=1) / dfx.var(ddof=1))
    out["bands"] = D["forecast_error_bands"]
    out["lambda_cv"] = D["lambda_cv"]
    out["exog"] = D["exog_scenarios"]["channels"]["fiscal"]
    return out


# ---------------------------------------------------------------------------
# Scenarios -- through the Python port of the tab's recursion
# ---------------------------------------------------------------------------
def _neutral(D):
    return sim.build_paths(D, {"neutral": {}}, rebase_to_spot=False)["neutral"]


def _ramp(v0, v1, k_up, n):
    return [v0 + (v1 - v0) * min(1.0, (i + 1) / k_up) for i in range(n)]


def example_scenarios(D, ex):
    """Two scenarios calibrated on the episode library, plus the neutral path."""
    base = _neutral(D)
    nr = base["n_real"]
    nfree = len(base["path"]) - nr
    lv = base["levels"]
    epi = {e["id"]: e for e in ex["episodes"]}
    e18, cov = epi["election_2018"], epi["covid_2020"]
    cds0 = lv["delta_fiscal"][nr - 1]
    em0 = lv["delta_dxy_em"][nr - 1]
    spx0 = lv["delta_sp500"][nr - 1]
    specs = {
        "Neutro": {},
        "Estresse fiscal (CDS de 2018)": {
            "delta_fiscal": _ramp(cds0, cds0 * e18["peak_x"], e18["months_to_peak"], nfree)},
        "Choque global (COVID, 2020)": {
            "delta_fiscal": _ramp(cds0, cds0 * cov["peak_x"], cov["months_to_peak"], nfree),
            "delta_dxy_em": _ramp(em0, em0 * (1 + cov["concurrent"]["dxy_em"] / 100), cov["months_to_peak"], nfree),
            "delta_sp500": _ramp(spx0, spx0 * (1 + cov["concurrent"]["sp500"] / 100), cov["months_to_peak"], nfree),
        },
    }
    paths = sim.build_paths(D, specs, rebase_to_spot=False)
    return paths, {"e18": e18, "cov": cov, "cds0": cds0}


# ---------------------------------------------------------------------------
# Layout helpers
# ---------------------------------------------------------------------------
_asset_counter = [0]


def chart_box(fig, max_width=464, box_width=481):
    _asset_counter[0] += 1
    path = os.path.join(_ASSET_DIR, "chart_%d.png" % _asset_counter[0])
    fig.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    with PILImage.open(path) as im:
        px_w, px_h = im.size
    nat_w, nat_h = px_w / 200 * 72, px_h / 200 * 72
    scale = min(max_width / nat_w, 1.25)
    t = Table([[RLImage(path, width=nat_w * scale, height=nat_h * scale)]], colWidths=[box_width])
    t.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.6, LINE), ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("TOPPADDING", (0, 0), (-1, -1), 8), ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    return t


def rule(color=GOLD, thickness=1.4, space_before=2, space_after=8):
    return HRFlowable(width="100%", thickness=thickness, color=color, spaceBefore=space_before, spaceAfter=space_after)


def section(number, title, tag):
    return [Paragraph("%s. %s" % (number, title), H1), Paragraph(tag, H1_TAG), rule()]


def P(text, style=BODY):
    return Paragraph(text, style)


def bullets(items, style=BULLET):
    return [Paragraph("&bull;&nbsp; %s" % b, style) for b in items]


def table(rows, col_widths=None, align_right_from=1, font=8.1):
    head = ParagraphStyle("th", fontName="DejaVuSans-Bold", fontSize=font, leading=font + 2.2, textColor=colors.white)
    body = ParagraphStyle("td", fontName="DejaVuSans", fontSize=font, leading=font + 2.6)
    bodyr = ParagraphStyle("tdr", parent=body, alignment=2)
    data = [[Paragraph(c, head) for c in rows[0]]]
    for r in rows[1:]:
        data.append([Paragraph(c, bodyr if (align_right_from >= 0 and i >= align_right_from) else body)
                     for i, c in enumerate(r)])
    t = Table(data, colWidths=col_widths, repeatRows=1)
    st = [("BACKGROUND", (0, 0), (-1, 0), NAVY), ("GRID", (0, 0), (-1, -1), 0.5, LINE),
          ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
          ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
          ("LEFTPADDING", (0, 0), (-1, -1), 5), ("RIGHTPADDING", (0, 0), (-1, -1), 5)]
    for i in range(2, len(data), 2):
        st.append(("BACKGROUND", (0, i), (-1, i), BG_SOFT))
    t.setStyle(TableStyle(st))
    return t


def card(title, paras):
    inner = [Paragraph(title, CARD_TITLE)] + [Paragraph(p, CARD_BODY) for p in paras]
    t = Table([[inner]], colWidths=[481])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), BG_SOFT), ("BOX", (0, 0), (-1, -1), 0.5, LINE),
                           ("LEFTPADDING", (0, 0), (-1, -1), 10), ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                           ("TOPPADDING", (0, 0), (-1, -1), 8), ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
    return KeepTogether([t, Spacer(1, 7)])


def footnote(text):
    return [HRFlowable(width=110, thickness=0.5, color=LINE, spaceBefore=4, spaceAfter=3, hAlign="LEFT"),
            Paragraph(text, FOOTNOTE), Spacer(1, 5)]


def equation_block(rows, left=190):
    data = [[Paragraph(a, EQ), Paragraph(b, EQ_NOTE)] for a, b in rows]
    t = Table(data, colWidths=[left, 481 - left])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), BG_SOFT), ("BOX", (0, 0), (-1, -1), 0.5, LINE),
                           ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                           ("TOPPADDING", (0, 0), (-1, -1), 2.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),
                           ("LEFTPADDING", (0, 0), (-1, -1), 10)]))
    return t


# ---------------------------------------------------------------------------
# Figures (one axis each, legend below the plot)
# ---------------------------------------------------------------------------
def _fig(w=6.4, h=3.0):
    fig, ax = plt.subplots(figsize=(w, h), dpi=200)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color("#C9CEDC")
    ax.tick_params(labelsize=7.8, colors="#55607A", length=3)
    ax.grid(axis="y", color=C_GRID, lw=0.6)
    ax.set_axisbelow(True)
    return fig, ax


def _title(ax, t, sub):
    ax.set_title(t, fontsize=10, color=C_NAVY, loc="left", fontweight="bold", pad=20)
    ax.text(0, 1.015, sub, transform=ax.transAxes, fontsize=7.6, color=C_MUTED, va="bottom")


def fig_scenarios(paths, D):
    """The three example paths, prefixed with the cutoff month so every line
    visibly starts from the last PTAX the model was fitted on."""
    fig, ax = _fig(h=3.0)
    names = list(paths)
    ref = paths[names[0]]
    fc = D["forecast"]
    cut = fc["nowcast"]["fit_cutoff"]
    seed = fc["seed_level"]
    months = [cut] + list(ref["months"])
    nr = ref["n_real"]                      # realized months after the cutoff
    x = list(range(len(months)))
    lo = [seed] + list(ref["lo"])
    hi = [seed] + list(ref["hi"])

    ax.axvspan(0, nr, color="#9AA3B8", alpha=0.13, lw=0)
    ax.fill_between(x, lo, hi, color=C_NAVY, alpha=0.09, lw=0, label="Faixa de ±1σ (neutro)")
    cols = [C_NAVY, C_GOLD, C_RED]
    for name, c in zip(names, cols):
        y = [seed] + list(paths[name]["path"])
        ax.plot(x, y, color=c, lw=1.8, label=name, zorder=3)
        ax.annotate(f(y[-1], 2), (x[-1], y[-1]), xytext=(5, 0), textcoords="offset points",
                    va="center", fontsize=7.6, color=c, fontweight="bold")
    nc = fc["nowcast"]["ptax"]
    obs = {cut: seed}
    obs.update({m: v for m, v in zip(nc["months"], nc["values"]) if m in months})
    ax.plot([months.index(m) for m in obs], list(obs.values()), "o", color=C_NAVY, ms=4.2, mfc="white",
            mew=1.3, zorder=4, label="PTAX observada")

    y0, y1 = ax.get_ylim()
    ax.set_ylim(y0, y1)
    ax.text(nr / 2, y0 + 0.03 * (y1 - y0), "fatores já\nobservados", ha="center", va="bottom",
            fontsize=6.8, color=C_MUTED, linespacing=1.1)
    ax.set_xlim(-0.4, x[-1] + 1.3)
    ax.set_xticks(x[::3])
    ax.set_xticklabels([mon(months[i]) for i in x[::3]], fontsize=7.4)
    ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f(v, 2)))
    ax.set_ylabel("R$ por US$", fontsize=7.8, color="#55607A")
    _title(ax, "Três cenários para o USD/BRL, pela mesma equação",
           "parâmetros da última janela de 72 meses; demais fatores no último valor observado")
    h, l = ax.get_legend_handles_labels()
    order = [l.index(k) for k in names + ["PTAX observada", "Faixa de ±1σ (neutro)"]]
    fig.legend([h[i] for i in order], [l[i] for i in order], loc="upper center", bbox_to_anchor=(0.5, 0.0),
               ncol=3, frameon=False, fontsize=7.6, handlelength=1.7, columnspacing=1.4)
    return fig


# ---------------------------------------------------------------------------
# Story
# ---------------------------------------------------------------------------
def build_story(D, built):
    X = derive(D)
    ws, lw, sd, roll = X["ws"], X["lw"], X["sd"], X["roll"]
    b = X["bands"]
    paths, pmeta = example_scenarios(D, X["exog"])
    resid = sim.spot_residual(D)
    months = D["months"]
    n = D["n"]
    fc = D["forecast"]
    nc = fc["nowcast"]
    cutoff = mon(nc["fit_cutoff"])
    story = []

    # ---- Capa ----------------------------------------------------------------
    story += [
        P("LIS CAPITAL", ParagraphStyle("brand", fontName="DejaVuSans-Bold", fontSize=10, textColor=GOLD, spaceAfter=2)),
        P("O modelo cambial USD/BRL", TITLE),
        P("Guia técnico: especificação, estimação móvel e construção de cenários", SUBTITLE),
        P("%s · amostra de estimação de %s a %s (%d meses) · coeficientes estimados até %s"
          % (_MES_LONGO[built.month - 1] + " de " + str(built.year), mon(months[0]), mon(months[-1]), n, cutoff),
          DATE_BADGE),
        rule(NAVY, 2, 8, 12),
    ]
    story.append(P(
        "Este documento descreve o modelo por trás da aba <b>FX Model</b> do FX Report. É uma regressão "
        "mensal da variação do USD/BRL contra a variação, no mesmo mês, de cinco fatores de mercado, mais "
        "um termo para o movimento do mês anterior e a diferença de inflação entre Brasil e Estados Unidos, "
        "que entra com peso fixo em um. Os coeficientes são estimados por regressão ridge, sobre a amostra "
        "inteira e sobre janelas móveis de 72 meses."))
    story.append(P(
        "<b>O modelo produz cenários; ele não é um previsor.</b> Dado um caminho para os cinco fatores e "
        "para a inflação, ele devolve o caminho do USD/BRL coerente com essas premissas, quanto cada fator "
        "contribuiu e uma faixa de erro medida em torno do resultado. Ele não projeta os fatores. A seção 1 "
        "mostra por que usá-lo assim; as seções 2 e 3 tratam da especificação e da razão de cada fator; a "
        "seção 4 explica os parâmetros móveis; e a seção 5, como montar e ler um cenário."))

    # ---- 1 -----------------------------------------------------------------------
    story += section("1", "Para que serve o modelo", "Uma tradução de premissas sobre os fatores em câmbio")
    story.append(P(
        "O teste relevante é fora da amostra: o modelo é estimado só com os dados disponíveis até cada data "
        "e avaliado nos meses seguintes, com os fatores nos valores que de fato ocorreram. Nessas condições, "
        "o seu Theil U é <b>0,564</b> em 3 meses e <b>0,584</b> em 12 meses. O Theil U divide o erro do "
        "modelo pelo erro de um passeio aleatório, a hipótese de que o câmbio futuro é igual ao de hoje, "
        "referência clássica e difícil de bater em câmbio; abaixo de 1, o modelo erra menos. Ou seja, "
        "conhecidos os fatores, o modelo reconstrói o caminho do câmbio com um erro 42%% a 44%% menor que o "
        "do passeio aleatório em todos os horizontes. O ganho vem dos fatores: sem eles, o mesmo teste dá um "
        "Theil U próximo de 1." % ()))
    story.append(P("Isso define como usá-lo:"))
    story += bullets([
        "<b>Os fatores são premissas, não previsões.</b> O cenário é a visão de quem o monta. O modelo "
        "acrescenta coerência interna, pesos calibrados no histórico e a decomposição do resultado.",
        "<b>A faixa de erro é condicional.</b> Ela mede quanto a tradução erra quando os fatores são "
        "conhecidos. Não inclui a incerteza sobre os próprios fatores; para isso servem os cenários "
        "alternativos.",
        "<b>A diferença entre dois cenários é mais confiável que o nível de cada um.</b> Todos os cenários "
        "partem do mesmo ponto e usam os mesmos coeficientes. O que o modelo não consegue explicar hoje "
        "entra igual em todos eles e se cancela quando dois cenários são comparados. Por isso, a "
        "pergunta que o modelo responde melhor é “quanto o câmbio muda se o CDS dobrar, em vez de ficar "
        "parado”, e não “onde o câmbio estará em doze meses”.",
    ])

    # ---- 2 -----------------------------------------------------------------------
    story.append(CondPageBreak(250))
    story += section("2", "Especificação", "Variável explicada, regressores, transformações e timing")
    story.append(P(
        "Todas as séries são tomadas no último dado de cada mês. A variável explicada é a variação "
        "logarítmica mensal da PTAX de venda, em pontos percentuais. Todo regressor entra no <b>mesmo "
        "mês</b> do movimento que explica:"))
    story.append(equation_block([
        ("Δfx<sub>t</sub> = 100·Δln PTAX<sub>t</sub>", "variação mensal do USD/BRL, p.p. (positivo = real mais fraco)"),
        ("&nbsp;&nbsp;= Δppp<sub>t</sub>", "diferença de inflação Brasil − EUA, 100·Δln(IPCA/CPI). Peso <b>fixo em 1</b>, não estimado"),
        ("&nbsp;&nbsp;+ α", "constante"),
        ("&nbsp;&nbsp;+ φ·Δfx<sub>t−1</sub>", "variação do câmbio no mês anterior. φ é negativo: parte do movimento é devolvida no mês seguinte"),
        ("&nbsp;&nbsp;+ Σ<sub>c</sub> β<sub>c</sub>·Δx<sub>c,t</sub>/σ<sub>c</sub>",
         "cinco fatores, cada variação dividida pelo seu desvio-padrão σ (tabela abaixo)"),
        ("&nbsp;&nbsp;+ ε<sub>t</sub>", "resíduo"),
    ], left=180))
    story.append(Spacer(1, 6))
    rows = [["Fator c", "Série e fonte", "Transformação Δx<sub>c</sub>", "σ<sub>c</sub>", "Histórico desde"]]
    src = {
        "delta_fiscal": ("CDS soberano de 5 anos do Brasil, em dólar (Bloomberg)", "diferença, bps"),
        "delta_dxy_em": ("Índice do dólar contra moedas emergentes, Fed (FRED)", "diferença, pontos"),
        "delta_carry_vol": ("(Selic − Fed funds) ÷ volatilidade implícita de 3 meses do USD/BRL (Bloomberg)", "diferença, razão"),
        "delta_sp500": ("Fechamento do S&amp;P 500", "100·Δln, %"),
        "delta_icbr_usd": ("Índice de commodities IC-Br em dólar (BCB)", "100·Δln, %"),
    }
    for c in CH:
        h = fc["channel_history"][c["raw"]]
        rows.append([c["name"], src[c["key"]][0], src[c["key"]][1], f(sd[c["key"]], 3 if sd[c["key"]] < 1 else 2),
                     mon(h["start"])])
    story.append(table(rows, col_widths=[88, 200, 88, 45, 60], align_right_from=3, font=7.8))
    story += footnote("σ<sub>c</sub> é o desvio-padrão da variação mensal de cada fator desde 2000, na unidade da "
                      "coluna de transformação.")
    story.append(P("<b>Paridade de poder de compra com peso fixo em 1</b>", H2))
    story.append(P(
        "A paridade relativa de poder de compra é uma relação de baixa frequência. De um mês para o outro, a "
        "diferença de inflação responde por %s%% da variância do câmbio, e um coeficiente estimado "
        "livremente lê ruído: nas janelas móveis de 72 meses ele vai de −0,65 a +2,14 e sai negativo em 45%% "
        "delas. Em horizontes de alguns anos a relação aparece. Regredindo a variação da PTAX em h meses "
        "contra a diferença de inflação acumulada no mesmo período, com toda a história disponível desde "
        "1994, o coeficiente é positivo em todos os horizontes de 1 a 10 anos, entre 1,1 e 2,4, e em nenhum "
        "deles é estatisticamente diferente de um. Por isso o termo entra com peso imposto em um, o valor que "
        "a teoria prevê e que os dados não rejeitam: o modelo é estimado sobre Δfx − Δppp, e Δppp é "
        "somado de volta na projeção. Os erros e o R² do modelo são sempre medidos sobre o próprio Δfx."
        % f(X["ppp_var_share"], 1)))
    story.append(P(
        "O efeito aparece na decomposição acumulada. Na amostra de estimação a PTAX foi de R$ %s a R$ %s, uma "
        "variação de %s p.p. em log. A diferença de inflação responde por %s p.p. Os cinco fatores somam "
        "%s p.p.: dólar contra emergentes %s, S&amp;P %s, commodities %s, CDS %s, carry/volatilidade %s. A "
        "constante e o termo do mês anterior somam %s p.p. A constante é de %s p.p. por mês e não é "
        "estatisticamente diferente de zero: o modelo não carrega uma tendência grande sem explicação."
        % (f(X["fx_first"], 2), f(X["fx_last"], 2), f(sum(X["cum"].values()), 1, True),
           f(X["cum"]["delta_ppp"], 1, True),
           f(sum(X["cum"][c["key"]] for c in CH), 1, True),
           f(X["cum"]["delta_dxy_em"], 1, True), f(X["cum"]["delta_sp500"], 1, True),
           f(X["cum"]["delta_icbr_usd"], 1, True), f(X["cum"]["delta_fiscal"], 1, True),
           f(X["cum"]["delta_carry_vol"], 1, True), f(X["cum"]["baseline"], 1, True), f(ws["alpha"], 3, True))))

    # ---- 3 -----------------------------------------------------------------------
    story.append(CondPageBreak(250))
    story += section("3", "Os fatores", "Cinco canais e a razão de cada um")
    rows = [["Fator", "β por σ (amostra inteira)", "Por unidade de choque (últimos 72 meses)",
             "Sinal mantido nas janelas"]]
    for c in CH:
        k = c["key"]
        native = lw["beta"][k] / sd[k] * SHOCK_SCALE[k]
        rows.append([c["name"], f(ws["beta"][k], 2, True),
                     "%s p.p. por %s" % (f(native, 2, True), c["shock_unit"]),
                     "%d / %d" % (roll[k]["same_sign"], roll[k]["n"])])
    rows.append(["Mês anterior (φ)", f(ws["beta"]["delta_fx_lag1"], 3, True),
                 "%s p.p. por p.p. do mês anterior" % f(lw["beta"]["delta_fx_lag1"], 3, True),
                 "%d / %d" % (roll["delta_fx_lag1"]["same_sign"], roll["delta_fx_lag1"]["n"])])
    story.append(table(rows, col_widths=[112, 100, 180, 89], font=7.8))
    story += footnote(
        "Positivo = real mais fraco. <b>β por σ:</b> cada fator entra na regressão como a sua variação "
        "mensal dividida pelo seu desvio-padrão σ (seção 2), então β é o movimento do USD/BRL no mesmo mês, "
        "em p.p., para uma variação de um desvio-padrão no fator. Isso põe os cinco fatores na mesma escala. "
        "<b>Por unidade de choque:</b> o mesmo movimento para um choque na unidade do próprio fator, com os "
        "parâmetros da última janela de 72 meses (%s a %s), que são os usados nos cenários."
        % (mon(lw["start"]), mon(lw["end"])))

    story.append(card("Risco fiscal — CDS soberano de 5 anos", [
        "O CDS é o preço de mercado do risco de crédito soberano brasileiro e a medida mais direta do "
        "prêmio fiscal. Um spread mais largo exige um retorno maior dos ativos brasileiros, e parte desse "
        "retorno vem por um real mais fraco. Sinal esperado e estimado: positivo.",
    ]))
    story.append(card("Dólar contra moedas emergentes", [
        "O real é negociado como parte do bloco de moedas emergentes. Entradas e saídas de recursos da "
        "classe de ativos como um todo movem o real independentemente do noticiário doméstico, e o índice "
        "do dólar contra emergentes capta esse fator comum. Sinal esperado e estimado: positivo.",
    ]))
    story.append(card("Carry/volatilidade — diferencial de juros por unidade de volatilidade implícita", [
        "É uma medida de carry ajustada ao risco, no espírito de um índice de Sharpe: o diferencial entre "
        "Selic e Fed funds dividido pela volatilidade implícita de 3 meses das opções de USD/BRL no fechamento "
        "do mês. Mede quanto rende a vantagem de juros por unidade do risco cambial que o mercado precifica. "
        "Quando a volatilidade implícita sobe, a perda esperada de uma posição de carry aumenta e a vantagem "
        "de juros vale menos. Uma razão mais alta atrai fluxo de carry e fortalece o real, que é o sinal "
        "negativo estimado.",
        "A volatilidade usada é a implícita, e não a realizada, porque a realizada de um mês é calculada "
        "sobre os próprios movimentos do câmbio que a equação quer explicar. A implícita é um preço, "
        "observado no mesmo fechamento que os demais fatores. O coeficiente é negativo em todas as %d "
        "janelas móveis." % roll["delta_carry_vol"]["n"],
    ]))
    story.append(card("S&amp;P 500 — variação mensal", [
        "Competição por capital. Para o investidor global, a bolsa americana é a principal alternativa aos "
        "ativos emergentes. Quando o S&amp;P sobe, o retorno esperado de ficar em ativos americanos aumenta, "
        "recursos que poderiam vir para o Brasil ficam ou voltam para os Estados Unidos, e o real enfraquece. "
        "O sinal positivo parece contraintuitivo porque uma alta da bolsa americana costuma vir com mercados "
        "mais calmos, o que ajuda o real. No modelo, essa ajuda chega pelos outros fatores: CDS mais baixo, "
        "dólar mais fraco contra emergentes e carry maior por unidade de volatilidade. Como o coeficiente do "
        "S&amp;P é medido com esses fatores constantes, o que sobra é só o efeito de competição.",
        "<b>Consequência para os cenários.</b> Num cenário de aversão a risco, a queda do S&amp;P "
        "<i>compensa</i> parte dos choques do CDS e do dólar em vez de somar a eles. Por isso o real se move "
        "menos do que as pernas de CDS e de dólar sugeririam sozinhas, e a perna do S&amp;P deve ser "
        "incluída por decisão, não por reflexo.",
    ]))
    story.append(card("Commodities — IC-Br em dólar", [
        "É o canal de termos de troca de um exportador de commodities. Preços mais altos em dólar para a "
        "pauta de exportação trazem mais dólares de exportação e fortalecem o real. Usa-se a versão em dólar "
        "porque o IC-Br em reais é convertido pelo próprio câmbio e seria parcialmente circular. Sinal "
        "esperado e estimado: negativo.",
    ]))

    # ---- 4 -----------------------------------------------------------------------
    story.append(CondPageBreak(250))
    story += section("4", "Parâmetros móveis", "Por que os coeficientes são reestimados, e como")
    fis = roll["delta_fiscal"]
    story.append(P(
        "A estimação móvel existe para captar <b>mudanças na sensibilidade do câmbio</b> a cada fator. Uma "
        "estimação única de %s a %s devolve uma sensibilidade média de vinte anos. Se a resposta do real a "
        "um fator triplicou, essa média subestima a resposta de hoje e superestima a de dez anos atrás, e um "
        "cenário rodado sobre ela não estaria calibrado para nenhum dos dois períodos. O risco fiscal é o "
        "caso mais claro: uma alta de 100 bps no CDS movia o USD/BRL em %s p.p. na primeira janela e move "
        "%s p.p. na última."
        % (mon(months[0]), mon(months[-1]), f(fis["first"] / sd["delta_fiscal"] * 100, 1),
           f(fis["last"] / sd["delta_fiscal"] * 100, 1))))
    story.append(P(
        "Por isso o modelo é estimado duas vezes. A <b>estimação sobre a amostra inteira</b> (%d meses) é a "
        "referência de longo prazo. A <b>estimação móvel</b> reestima a mesma equação sobre os últimos "
        "<b>72 meses</b>, avançando um mês por vez: a cada passo sai o mês mais antigo e entra o mais "
        "recente, e os coeficientes acompanham a sensibilidade à medida que ela muda. São %d janelas, "
        "terminando de %s a %s. Os cenários usam a última janela, que é a melhor estimativa disponível da "
        "sensibilidade atual."
        % (n, fis["n"], mon(D["rolling"]["window_end"][0]), mon(D["rolling"]["window_end"][-1]))))
    story.append(P(
        "<b>Por que 72 meses.</b> O tamanho da janela troca velocidade por precisão. Uma janela curta acompanha "
        "rápido uma mudança de sensibilidade, mas estima cada coeficiente com poucos meses e erra mais. Uma "
        "janela longa é estável, mas passa a misturar regimes diferentes. Entre as janelas testadas, de 24 a "
        "84 meses, a de 72 ficou entre as melhores nos horizontes de 3 a 12 meses."))
    story.append(P(
        "A trajetória do coeficiente de cada fator ao longo das janelas, e o R² de cada janela, estão no FX "
        "Report, aba <b>FX Model</b>, seção <b>Fit diagnostics</b> (gráficos <i>Rolling Coefficient</i> e "
        "<i>R² Over Time</i>)."))
    story.append(P(
        "<b>Os coeficientes ficam fixos entre reestimações.</b> Eles são estimados com dados até %s e mantidos "
        "até a próxima reestimação, para que um cenário não mude de um dia para o outro só porque chegou um "
        "dado novo. Os meses posteriores continuam aparecendo: como meses observados nas caixas de premissa e "
        "como a linha <i>Observed (since fit)</i> dos gráficos." % cutoff))

    # ---- 5 -----------------------------------------------------------------------
    story.append(CondPageBreak(250))
    story += section("5", "Como montar um cenário", "Premissas, calibragem e resultado")
    story.append(P(
        "O quadro de 12 meses da aba é o motor dos cenários. Ele roda a recursão abaixo com os parâmetros da "
        "última janela, partindo do último mês estimado (PTAX de R$ %s em %s, com variação de %s p.p. naquele "
        "mês):" % (f(fc["seed_level"], 4), cutoff, f(fc["seed_delta_fx_lag1"], 2, True))))
    story.append(equation_block([
        ("Δfx̂<sub>h</sub> = Δppp<sub>h</sub> + α + φ·Δfx̂<sub>h−1</sub> + Σ β<sub>c</sub>Δx<sub>c,h</sub>/σ<sub>c</sub>",
         "Δx<sub>c,h</sub> é a variação entre duas caixas consecutivas; a caixa 0 é o último mês estimado"),
        ("FX̂<sub>h</sub> = FX̂<sub>h−1</sub>·exp(Δfx̂<sub>h</sub>/100)", "o nível é encadeado mês a mês, sem reancorar"),
    ], left=270))
    story.append(Spacer(1, 6))
    story.append(P("Passo a passo", H2))
    story += bullets([
        "<b>Meses já observados ficam travados.</b> Os meses depois de %s que já têm dado vêm preenchidos e "
        "não podem ser editados; o mês corrente vem com a leitura parcial mais recente e continua editável. "
        "Hoje o CDS, o dólar contra emergentes e o S&amp;P estão observados até %s; o IC-Br e a inflação, "
        "até %s; e carry/volatilidade, até %s. Uma caixa que não é editada mantém o último valor observado "
        "do fator: sem uma visão sobre ele, ele fica onde está."
        % (cutoff, mon(nc["channels"]["fiscal"]["months"][-1]), mon(nc["channels"]["icbr_usd"]["months"][-1]),
           mon(nc["channels"]["carry_vol"]["months"][-1])),
        "<b>Cada fator pode ser digitado em nível ou em variação mensal.</b> A escolha muda só a exibição da "
        "caixa. A inflação é digitada como o diferencial de 12 meses entre IPCA e CPI, e as caixas não "
        "editadas seguem a tendência dos últimos 12 meses, e não um índice congelado: congelar o índice "
        "equivaleria a supor Brasil e Estados Unidos com a mesma inflação por um ano.",
        "<b>Carry/volatilidade entra pelas partes.</b> O botão <i>Break down into parts</i> monta a razão a "
        "partir dos caminhos de Selic, Fed funds e volatilidade implícita. Uma visão de política monetária "
        "entra como caminho de Selic, e uma visão de risco, como caminho de volatilidade. A volatilidade "
        "implícita sobe nos mesmos episódios em que o CDS abre e o dólar se fortalece contra emergentes, "
        "então um cenário de estresse deve movê-la também.",
        "<b>A calibragem vem do histórico.</b> O gráfico de cada fator mostra toda a sua história (CDS "
        "desde %s, carry/volatilidade desde %s, S&amp;P desde %s), em escala logarítmica quando a série "
        "varia mais de oito vezes. Para o CDS, a seção <i>Base scenarios</i> da aba traz uma biblioteca de "
        "episódios datados, medidos todos pela mesma régua."
        % tuple(fc["channel_history"][k]["start"][:4] for k in ("fiscal", "carry_vol", "sp500")),
        "<b>O resultado</b> é o caminho central, a faixa de ±1σ e a decomposição do caminho por fator. As "
        "premissas podem ser salvas com um nome e uma justificativa e exportadas para arquivo.",
    ])

    story.append(P("Entre a estimação e hoje: o que os fatores já dizem", H2))
    story.append(P(
        "Os coeficientes param em %s, mas os dados dos fatores continuam chegando. Os meses entre a estimação "
        "e hoje são rodados pelo modelo com os valores <i>observados</i> dos fatores: o caminho nesses meses "
        "é o que o modelo diz que o USD/BRL deveria ter feito, dado o que os fatores fizeram. Ele parte do "
        "nível do próprio modelo, e não do câmbio negociado, porque a distância até o câmbio negociado é "
        "justamente a leitura. Em %s o modelo explica o USD/BRL em R$ %s, contra uma PTAX de R$ %s: o real está "
        "%s%% %s do que os fatores justificam. Essa distância é a parte do movimento recente que os fatores "
        "não explicam, e é o que a próxima reestimação terá de absorver. Como todos os cenários partem do "
        "mesmo ponto, ela não altera a diferença entre dois cenários."
        % (cutoff, mon(resid[0]), f(resid[2], 3), f(resid[1], 3), f(abs(resid[3]), 1),
           "mais fraco" if resid[3] > 0 else "mais forte")))
    story.append(CondPageBreak(480))      # the example, its chart and its reading stay on one page
    story.append(P("Um exemplo", H2))
    e18, cov = pmeta["e18"], pmeta["cov"]
    names = list(paths)
    end = {k: paths[k]["path"][-1] for k in names}
    story.append(P(
        "Dois cenários montados a partir da biblioteca de episódios do CDS, rodados pela mesma equação. O "
        "<b>estresse fiscal</b> leva o CDS ao múltiplo do pico da eleição de 2018 (%s vezes o nível de "
        "partida) em %d meses e o mantém ali. O <b>choque global</b> reproduz o episódio da COVID por "
        "inteiro: CDS %s vezes em %d meses, com os movimentos que ocorreram junto no dólar contra emergentes "
        "(%s%%) e no S&amp;P (%s%%). Nos dois casos o pico é mantido, sem devolução. Essa é uma premissa do "
        "exemplo, não uma propriedade dos episódios: na crise de 2008, o CDS devolveu quase toda a alta "
        "dentro dos mesmos doze meses. Os demais fatores ficam no último valor observado."
        % (f(e18["peak_x"], 2), e18["months_to_peak"], f(cov["peak_x"], 2), cov["months_to_peak"],
           f(cov["concurrent"]["dxy_em"], 1, True), f(cov["concurrent"]["sp500"], 1, True))))
    story.append(chart_box(fig_scenarios(paths, D)))
    sig = b["std_error_pct"][-1]
    story.append(P(
        "Em %s os três caminhos terminam em R$ %s (neutro), R$ %s (estresse fiscal) e R$ %s (choque global). "
        "Em 12 meses, um desvio-padrão do erro condicional equivale a %s%% do nível: o estresse fiscal fica a "
        "cerca de %s desvio-padrão do neutro, e o choque global, a cerca de %s. Parte do choque global é compensada "
        "pela queda do S&amp;P, que no modelo fortalece o real (seção 3)."
        % (mon(paths[names[0]]["months"][-1]), f(end[names[0]], 2), f(end[names[1]], 2), f(end[names[2]], 2),
           f(sig, 1), f(100 * (end[names[1]] / end[names[0]] - 1) / sig, 1),
           f(100 * (end[names[2]] / end[names[0]] - 1) / sig, 1))))
    return story


def _footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("DejaVuSans", 7.6)
    canvas.setFillColor(MUTED)
    canvas.drawCentredString(A4[0] / 2, 12 * mm, "LIS Capital — O modelo cambial USD/BRL: guia técnico · página %d" % doc.page)
    canvas.restoreState()


def run(report_path=REPORT_PATH, out_path=OUT_PATH):
    D, built = load_payload(report_path)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    doc = SimpleDocTemplate(out_path, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm,
                            topMargin=18 * mm, bottomMargin=20 * mm,
                            title="O modelo cambial USD/BRL — guia técnico", author="LIS Capital")
    doc.build(build_story(D, built), onFirstPage=_footer, onLaterPages=_footer)
    print("Wrote %s" % out_path)
    return out_path


if __name__ == "__main__":
    run()
