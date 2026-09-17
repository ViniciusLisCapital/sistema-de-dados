"""Gera o relatório narrativo de câmbio em PDF (`reports/brasil/FX Outlook`).

O `FX Report.html` e um dashboard: mostra tudo e não conclui nada. Este e o
documento que fica ao lado dele -- le os mesmos dados, separa o que mudou na
margem do que é nível estrutural, e termina em três cenários com probabilidade.

Três regras que valem para o arquivo inteiro:

1. **Nenhum número em prosa e digitado.** Todo valor citado no texto vem por
   f-string das mesmas variaveis que alimentam o gráfico ao lado. Este repo ja
   registrou três incidentes de frase que sobreviveu a troca de fonte e passou
   a contradizer o número impresso ao lado dela.
2. **Os dados vem dos carregadores do dashboard** (`generate_report._load_*`),
   não de SQL próprio, para que o PDF não possa divergir do dashboard por
   construção -- inclusive na inversão de sinal do balanço de pagamentos, que
   é uma convenção de apresentação e não do banco.
3. **As ressalvas são impressas.** Comex não reconcilia com o BP; o modelo
   corta em jun/2026 e os dados vao até set/2026; a soma dos claims de
   atribuição e soma e não média; a reserva em ouro subiu por preço e por
   volume; e, no modelo, o S&P caindo deixa o real mais forte. São o que impede
   o leitor de somar o que não soma.

O toolkit de PDF (fontes, paleta, estilos, `chart_box`, `results_table`) segue
a convenção da casa estabelecida em `models/generate_fx_attribution_pdf.py`:
copiado, não importado -- cada script de PDF deste projeto e autocontido.

    uv run python -c "from analytics.brasil.exchange_rate.generate_fx_outlook_pdf import run; run()"
"""

import datetime as _dt
import math
import os
import tempfile

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
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
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

import analytics.brasil.exchange_rate.generate_report as gr
from analytics.brasil.exchange_rate.models import fx_attribution_model as fxa
from analytics.brasil.exchange_rate.models import fx_forecast_sim as sim
from analytics.brasil.exchange_rate.models import ridge_deviation_model as rdm

matplotlib.rcParams["mathtext.fontset"] = "dejavusans"
# Sem isto, o cifrao de "R$ por US$" abre modo matematico e o rotulo do
# eixo sai como "RporUS" -- sem erro nenhum, so com o texto comido.
matplotlib.rcParams["text.parse_math"] = False
_ASSET_DIR = tempfile.mkdtemp(prefix="lis_fxoutlook_assets_")

# ---------------------------------------------------------------------------
# Fontes e paleta -- mesma escolha e racional de generate_fx_attribution_pdf.py
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
BG_EQ = colors.HexColor("#F4F5F7")

C_NAVY, C_GOLD, C_GREEN, C_RED = "#1F2853", "#BB9B1D", "#418791", "#EA523A"
C_MUTED, C_GRID = "#7A88A8", "#E4E7EF"
C_PURPLE, C_TEAL, C_SAND = "#6B5B95", "#2E8B8B", "#C8842B"

OUT_PATH = os.path.join("reports", "brasil", "FX Outlook.pdf")

# O modelo de atribuicao publica os rotulos das nove categorias em ingles.
# Este documento e em portugues, entao eles sao traduzidos na apresentacao --
# a chave (o slug) continua sendo a do modelo.
CAT_PT = {
    "fiscal_br": "Fiscal (Brasil)",
    "monetary_br": "Juros e política monetária",
    "politics_br": "Política doméstica",
    "global_usd": "Dólar global",
    "commodities": "Commodities e contas externas",
    "risk_sentiment": "Apetite a risco global",
    "china_em": "China e emergentes",
    "trade_policy": "Política comercial e tarifas",
    "capital_flows": "Fluxo de capital e posicionamento",
}

# ---------------------------------------------------------------------------
# Estilos
# ---------------------------------------------------------------------------
TITLE = ParagraphStyle("Title", fontName="DejaVuSans-Bold", fontSize=20, leading=24, textColor=NAVY, spaceAfter=4)
SUBTITLE = ParagraphStyle("Subtitle", fontName="DejaVuSans", fontSize=11, leading=14, textColor=MUTED, spaceAfter=2)
DATE_BADGE = ParagraphStyle("DateBadge", fontName="DejaVuSans", fontSize=9, leading=11, textColor=MUTED)

H1 = ParagraphStyle("H1", fontName="DejaVuSans-Bold", fontSize=15, leading=19, textColor=NAVY, spaceBefore=6, spaceAfter=2)
H1_TAG = ParagraphStyle("H1Tag", fontName="DejaVuSans", fontSize=9, leading=11, textColor=GOLD, spaceAfter=6)
H2 = ParagraphStyle("H2", fontName="DejaVuSans-Bold", fontSize=10.5, leading=13, textColor=NAVY, spaceBefore=10, spaceAfter=4)

# alignment=4 = justificado. hifenizacao nao existe no reportlab, entao o
# corpo fica em 9,3/13,2 numa coluna larga -- a faixa em que o justificado nao
# abre rios (a regra de `.claude/rules/lis-dashboards.md` e sobre HTML, onde a
# largura do bloco e livre; aqui a coluna e fixa em A4 menos as margens).
BODY = ParagraphStyle("Body", fontName="DejaVuSans", fontSize=9.3, leading=13.2, textColor=colors.HexColor("#1A1A1A"), spaceAfter=6, alignment=4)
BODY_TIGHT = ParagraphStyle("BodyTight", parent=BODY, spaceAfter=3)
LEAD = ParagraphStyle("Lead", parent=BODY, fontSize=10, leading=14.5, textColor=NAVY)
BULLET = ParagraphStyle("Bullet", parent=BODY, leftIndent=12, bulletIndent=0, spaceAfter=4)

MARG_LABEL = ParagraphStyle("MargLabel", fontName="DejaVuSans-Bold", fontSize=8.6, leading=11, textColor=GREEN, spaceAfter=1)
NIVEL_LABEL = ParagraphStyle("NivelLabel", fontName="DejaVuSans-Bold", fontSize=8.6, leading=11, textColor=GOLD, spaceAfter=1)

CAUTION_LABEL = ParagraphStyle("CautionLabel", fontName="DejaVuSans-Bold", fontSize=8.8, leading=12, textColor=RED, spaceAfter=2)
CAUTION_BODY = ParagraphStyle("CautionBody", parent=BODY, fontSize=8.8, leading=12.5, textColor=colors.HexColor("#3A2020"))

# A ressalva e nota de rodape, nao caixa de alerta (2026-09-10, pedido do
# usuario). Sao cinco delas, todas em caixa vermelha do tamanho do corpo:
# juntas competiam com o texto que existem para qualificar.
FOOTNOTE = ParagraphStyle("Footnote", parent=BODY, fontSize=7.4, leading=9.7,
                          textColor=colors.HexColor("#6E7688"), spaceAfter=0)

CAP = ParagraphStyle("Cap", fontName="DejaVuSans", fontSize=7.6, leading=9.6, textColor=MUTED, spaceBefore=2, spaceAfter=8, alignment=4)
FOOTER = ParagraphStyle("Footer", fontName="DejaVuSans", fontSize=7.6, leading=10, textColor=MUTED, alignment=1)

_asset_counter = [0]


# ---------------------------------------------------------------------------
# Numeros em portugues -- virgula decimal, ponto de milhar
# ---------------------------------------------------------------------------
def n(x, d=1, sign=False):
    if x is None or (isinstance(x, float) and math.isnan(x)):
        return "n/d"
    spec = ("+,.%df" % d) if sign else (",.%df" % d)
    s = format(float(x), spec)          # 1,234,567.89 no padrao ingles
    return s.replace(",", "@").replace(".", ",").replace("@", ".")


_MESES = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"]


def mes(ym):
    """'2026-09' -> 'set/26'."""
    y, m = ym.split("-")[:2]
    return "%s/%s" % (_MESES[int(m) - 1], y[2:])


def mes_longo(ym):
    y, m = ym.split("-")[:2]
    nomes = ["janeiro", "fevereiro", "marco", "abril", "maio", "junho", "julho",
             "agosto", "setembro", "outubro", "novembro", "dezembro"]
    return "%s de %s" % (nomes[int(m) - 1], y)


def dmy(iso):
    p = str(iso)[:10].split("-")
    return "%s/%s/%s" % (p[2], p[1], p[0])


# ---------------------------------------------------------------------------
# Blocos de layout
# ---------------------------------------------------------------------------
def chart_box(fig, max_width=464, box_width=481):
    _asset_counter[0] += 1
    path = os.path.join(_ASSET_DIR, "chart_%d.png" % _asset_counter[0])
    fig.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    with PILImage.open(path) as im:
        px_w, px_h = im.size
    nat_w, nat_h = px_w / 200 * 72, px_h / 200 * 72
    # Sobe E desce. Antes so reduzia, entao uma figura desenhada com folga saia
    # impressa menor do que a coluna comporta -- e o grafico e o corpo da
    # evidencia deste documento. O teto de 1,25x mantem o raster acima de
    # 160 dpi efetivos.
    scale = min(max_width / nat_w, 1.25)
    img = RLImage(path, width=nat_w * scale, height=nat_h * scale)
    t = Table([[img]], colWidths=[box_width])
    t.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.6, LINE),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
    ]))
    return t


def rule(color=GOLD, thickness=1.4, space_before=2, space_after=8):
    return HRFlowable(width="100%", thickness=thickness, color=color,
                      spaceBefore=space_before, spaceAfter=space_after)


def results_table(rows, col_widths=None, align_right_from=1):
    head = ParagraphStyle("th", fontName="DejaVuSans-Bold", fontSize=8.2, leading=10.4, textColor=colors.white)
    body = ParagraphStyle("td", fontName="DejaVuSans", fontSize=8.2, leading=10.8)
    bodyr = ParagraphStyle("tdr", parent=body, alignment=2)
    data = [[Paragraph(c, head) for c in rows[0]]]
    for r in rows[1:]:
        data.append([Paragraph(c, bodyr if (i >= align_right_from and align_right_from >= 0) else body)
                     for i, c in enumerate(r)])
    t = Table(data, colWidths=col_widths, repeatRows=1)
    style = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("GRID", (0, 0), (-1, -1), 0.5, LINE),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 3.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3.5),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style.append(("BACKGROUND", (0, i), (-1, i), BG_EQ))
    t.setStyle(TableStyle(style))
    return t


def caution(text, label="Ressalva"):
    """Nota de rodape.

    A ressalva impede o leitor de somar o que nao soma; ela nao e a mensagem
    da pagina. Como caixa vermelha do tamanho do corpo, cinco delas disputavam
    atencao com o texto que qualificam. Regra fina, corpo menor, cor apagada --
    e o conteudo intacto.
    """
    return [HRFlowable(width=110, thickness=0.5, color=LINE, spaceBefore=5,
                       spaceAfter=3, hAlign="LEFT"),
            Paragraph("<b>%s.</b> %s" % (label, text), FOOTNOTE),
            Spacer(1, 5)]


def section_header(number, title_text, subtitle_text):
    head = ("%s. %s" % (number, title_text)) if number else title_text
    return [Paragraph(head, H1),
            Paragraph(subtitle_text, H1_TAG),
            rule()]


def margem(text):
    return [Paragraph("NA MARGEM", MARG_LABEL), Paragraph(text, BODY_TIGHT), Spacer(1, 4)]


def nivel(text):
    return [Paragraph("NO NÍVEL", NIVEL_LABEL), Paragraph(text, BODY_TIGHT), Spacer(1, 4)]


def bullets(items):
    return [Paragraph("&bull;&nbsp; %s" % b, BULLET) for b in items]


def caption(text):
    return Paragraph(text, CAP)


# ---------------------------------------------------------------------------
# Matplotlib -- estilo unico
# ---------------------------------------------------------------------------
def _fig(w=6.4, h=3.15):
    fig, ax = plt.subplots(figsize=(w, h), dpi=200)
    _style(ax)
    return fig, ax


def _style(ax):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#C9CEDC")
    ax.spines["bottom"].set_color("#C9CEDC")
    ax.tick_params(labelsize=8, colors="#55607A", length=3)
    ax.grid(axis="y", color=C_GRID, lw=0.6)
    ax.set_axisbelow(True)


def _title(ax, t, sub=None):
    ax.set_title(t, fontsize=10.5, color=C_NAVY, loc="left", fontweight="bold", pad=22 if sub else 7)
    if sub:
        ax.text(0, 1.012, sub, transform=ax.transAxes, fontsize=8, color=C_MUTED, va="bottom")


def _legend(ax, ncol=None, **kw):
    """Legenda FORA do quadro, centrada abaixo do grafico.

    Dentro do quadro ela cobre a serie, e o fundo branco translucido que ela
    tinha antes so trocava "legenda ilegivel" por "linha coberta" -- num
    documento em que o grafico e a evidencia, tapar o dado para caber a
    etiqueta e o pior dos dois. Ancorada em coordenadas de FIGURA em y=0, ela
    fica abaixo de tudo o que existe no eixo, inclusive rotulo rotacionado, e
    nao pode colidir com nada. `bbox_inches="tight"` no savefig estende o
    recorte para inclui-la, entao nada e cortado.
    """
    h, l = ax.get_legend_handles_labels()
    if not h:
        return
    for morto in ("loc", "frameon", "facecolor", "edgecolor", "framealpha"):
        kw.pop(morto, None)          # os call sites ainda pedem posicao
    if ncol is None:
        ncol = min(3, len(h))
    kw.setdefault("fontsize", 8)
    ax.figure.legend(h, l, loc="upper center", bbox_to_anchor=(0.5, 0.0), ncol=ncol,
                     frameon=False, handlelength=1.7, handletextpad=0.5,
                     columnspacing=1.8, borderaxespad=0, **kw)


def _br_fmt(d=1):
    return FuncFormatter(lambda v, _: n(v, d))


def _monthly_ticks(ax, months, every=12, rot=0):
    idx = list(range(0, len(months), every))
    ax.set_xticks(idx)
    ax.set_xticklabels([mes(months[i]) for i in idx], rotation=rot,
                       ha="right" if rot else "center", fontsize=8)


# ---------------------------------------------------------------------------
# Dados
# ---------------------------------------------------------------------------
def _last(seq):
    for v in reversed(seq):
        if v is not None and not (isinstance(v, float) and math.isnan(v)):
            return v
    return None


def _at_or_before(dates, values, target):
    """Último valor com data <= target."""
    best = None
    for d, v in zip(dates, values):
        if v is None or (isinstance(v, float) and math.isnan(v)):
            continue
        if str(d)[:10] <= target:
            best = v
    return best


def _roll_sum(values, k):
    """Soma móvel de k, com None onde a janela não fecha."""
    out, acc, buf = [], 0.0, []
    for v in values:
        x = 0.0 if v is None or (isinstance(v, float) and math.isnan(v)) else float(v)
        buf.append(x)
        acc += x
        if len(buf) > k:
            acc -= buf.pop(0)
        out.append(acc if len(buf) == k else None)
    return out


def _month_key(d):
    return str(d)[:7]


def load_all():
    """Reune tudo o que o documento cita. Nada aqui é digitado a mao."""
    D = {}

    # --- carregadores do dashboard -----------------------------------------
    for fn in ("_load_ptax", "_load_reer", "_load_termos", "_load_bop",
               "_load_cambio_contratado", "_load_bcb_positioning", "_load_cot_fx",
               "_load_comex_pais", "_load_comex_fator_agregado", "_load_comex_produto",
               "_load_diferenciais"):
        D[fn[len("_load_"):]] = getattr(gr, fn)()

    # --- PTAX ---------------------------------------------------------------
    px = D["ptax"]
    dts, vals = px["dates"], px["ptax_venda"]
    pairs = [(str(d)[:10], v) for d, v in zip(dts, vals) if v is not None]
    last_d, last_v = pairs[-1]
    ref = _dt.date.fromisoformat(last_d)
    def _back(days):
        t = (ref - _dt.timedelta(days=days)).isoformat()
        prev = [v for d, v in pairs if d <= t]
        return prev[-1] if prev else None
    y2026 = [v for d, v in pairs if d >= "2026-01-01"]
    y2025 = [v for d, v in pairs if "2025-01-01" <= d < "2026-01-01"]
    D["px"] = {
        "date": last_d, "last": last_v,
        "d1m": _back(30), "d3m": _back(90), "d6m": _back(180), "d12m": _back(365),
        "min26": min(y2026), "max26": max(y2026), "mean25": sum(y2025) / len(y2025),
        "pairs": pairs,
    }
    for k, days in (("p1m", 30), ("p3m", 90), ("p6m", 180), ("p12m", 365)):
        base = D["px"]["d%s" % k[1:]]
        D["px"][k] = 100.0 * (last_v / base - 1.0) if base else None

    # --- REER e termos de troca --------------------------------------------
    rr = D["reer"]
    rd = [str(x)[:10] for x in rr["dates"]]
    D["reer_last_month"] = _month_key(rd[-1])
    D["reer_now"] = {c: _last(rr[c]) for c in ("BR", "MX", "CL", "CO")}
    t12 = (_dt.date.fromisoformat(rd[-1]) - _dt.timedelta(days=360)).isoformat()
    D["reer_12m"] = {c: _at_or_before(rd, rr[c], t12) for c in ("BR", "MX", "CL", "CO")}
    D["reer_hist"] = {"dates": rd, **{c: rr[c] for c in ("BR", "MX", "CL", "CO")}}

    tt = D["termos"]
    td = [str(x)[:10] for x in tt["dates"]]
    tv = tt["termos_de_troca_funcex"]
    D["tot"] = {
        "month": _month_key(td[-1]), "last": _last(tv),
        "prev12": _at_or_before(td, tv, (_dt.date.fromisoformat(td[-1]) - _dt.timedelta(days=360)).isoformat()),
        "max": max(v for v in tv if v is not None),
        "max_month": _month_key(td[[i for i, v in enumerate(tv) if v == max(x for x in tv if x is not None)][0]]),
        "dates": td, "values": tv,
    }

    # --- Balanco de pagamentos ---------------------------------------------
    bp = D["bop"]
    bd = [str(x)[:10] for x in bp["dates"]]
    D["bop_month"] = _month_key(bd[-1])
    gdp12 = _roll_sum(bp["gdp_usd_bi"], 12)

    def r12(key):
        return _roll_sum(bp[key], 12)

    keys = ["conta_corrente", "mercadorias_gerais", "servicos", "renda_primaria",
            "renda_secundaria", "lucros_dividendos", "juros", "idp_ingressos",
            "portfolio_passivos", "titulos_dom", "acoes_passivos",
            "exportacao_bens", "importacao_bens"]
    R = {k: r12(k) for k in keys if k in bp}
    D["bop12"] = {}
    for k, s in R.items():
        D["bop12"][k] = {"now": s[-1], "y1": s[-13], "y2": s[-25]}
    D["bop12_series"] = R
    D["bop_dates"] = bd
    D["gdp12"] = gdp12[-1]
    D["gdp12_series"] = gdp12
    D["cc_pct"] = 100.0 * R["conta_corrente"][-1] / gdp12[-1]
    D["cc_pct_y1"] = 100.0 * R["conta_corrente"][-13] / gdp12[-13]
    D["cc_pct_y2"] = 100.0 * R["conta_corrente"][-25] / gdp12[-25]
    D["cobertura_idp"] = R["idp_ingressos"][-1] / abs(R["conta_corrente"][-1])

    # --- Comex --------------------------------------------------------------
    def comex12(block, name):
        s = _roll_sum(block[name], 12)
        return s[-1], s[-13]

    cp, cf, cpr = D["comex_pais"], D["comex_fator_agregado"], D["comex_produto"]
    D["comex_month"] = _month_key(str(cp["dates"][-1])[:10])
    D["comex"] = {}
    for label, block, name in (
        ("export_mundo", cp, "export_mundo"), ("import_mundo", cp, "import_mundo"),
        ("saldo_china", cp, "saldo_china"), ("export_china", cp, "export_china"),
        ("saldo_eua", cp, "saldo_eua"), ("export_eua", cp, "export_eua"),
        ("export_basicos", cf, "export_basicos"), ("export_manufaturados", cf, "export_manufaturados"),
        ("import_manufaturados", cf, "import_manufaturados"),
        ("export_petroleo", cpr, "export_petroleo"), ("export_soja", cpr, "export_soja"),
        ("export_carnes", cpr, "export_carnes"), ("export_minerio_ferro", cpr, "export_minerio_ferro"),
    ):
        if name in block:
            a, b = comex12(block, name)
            D["comex"][label] = {"now": a, "y1": b, "var": a - b}

    # --- Fluxo cambial contratado ------------------------------------------
    cc = D["cambio_contratado"]
    cd = [str(x)[:10] for x in cc["dates"]]
    D["fluxo_month"] = _month_key(cd[-1])
    D["fluxo"] = {}
    for k in ("cc_saldo_total", "cc_saldo_comercial", "cc_fin_saldo"):
        s = _roll_sum(cc[k], 12)
        D["fluxo"][k] = {"now": s[-1], "y1": s[-13], "mes": cc[k][-1]}
    D["fluxo_series"] = {k: _roll_sum(cc[k], 12) for k in ("cc_saldo_total", "cc_saldo_comercial", "cc_fin_saldo")}
    D["fluxo_dates"] = cd

    # --- Reservas, swap, intervencao ---------------------------------------
    bcb = D["bcb_positioning"]
    res = bcb["reserves"]           # total diario (serie de liquidez)
    arv = bcb["reservas_arvore"]    # decomposicao mensal
    rdt = [str(x)[:10] for x in res["dates"]]
    adt = [str(x)[:10] for x in arv["dates"]]

    def _pair(dates, values):
        t = (_dt.date.fromisoformat(dates[-1]) - _dt.timedelta(days=365)).isoformat()
        return {"now": _last(values), "y1": _at_or_before(dates, values, t)}

    D["res"] = {}
    for k in ("reserves_liquidity_daily", "reserves_total_monthly"):
        if k in res:
            D["res"][k] = _pair(rdt, res[k])
    for k in ("reserves_fx_total", "reserves_gold_usd", "reserves_sdrs",
              "reserves_imf_position", "reserves_other_total", "reserves_total_monthly"):
        if k in arv:
            D["res"][k] = _pair(adt, arv[k])

    # O volume de ouro nao esta em nenhum carregador: ele e o que separa
    # "o BCB comprou ouro" de "o ouro subiu de preco", e as duas causas tem
    # de ser ditas em separado.
    try:
        w = gr._pivot("macro_brasil", "cmb_reservas_bc")
        gv = w["reserves_gold_volume"].dropna()
        gd = [str(x)[:10] for x in gv.index]
        D["res"]["reserves_gold_volume"] = _pair(gd, list(gv.values))
        # A SERIE, e nao so os dois pontos: o volume e uma escada de compras
        # discretas, e e a escada que separa "comprou" de "remarcou".
        D["gold_vol"] = {"months": [_month_key(d) for d in gd],
                         "values": [float(x) for x in gv.values]}
    except Exception:
        D["res"]["reserves_gold_volume"] = {"now": None, "y1": None}
        D["gold_vol"] = None

    D["res_date"] = rdt[-1]
    D["res_month"] = _month_key(adt[-1])
    D["res_series"] = arv
    D["res_dates"] = adt
    D["res_daily"] = {"dates": rdt, "values": res.get("reserves_liquidity_daily")}

    sw = bcb["swap"]
    swd = [str(x)[:10] for x in sw["dates"]]
    D["swap"] = {}
    for k in ("bcb_swap_cambial_position", "bank_fx_spot_position"):
        if k in sw:
            t = (_dt.date.fromisoformat(swd[-1]) - _dt.timedelta(days=365)).isoformat()
            D["swap"][k] = {"now": _last(sw[k]), "y1": _at_or_before(swd, sw[k], t),
                            "date": _month_key([d for d, v in zip(swd, sw[k]) if v is not None][-1])}
    D["swap_series"] = sw
    D["swap_dates"] = swd

    iv = bcb["intervencoes"]
    ivd = [str(x)[:10] for x in iv["dates"]]
    D["interv"] = {}
    for k, col in iv.items():
        if k == "dates" or not isinstance(col, list):
            continue
        s12 = _roll_sum(col, 12)
        D["interv"][k] = {"a12m": s12[-1] if s12 else None,
                          "a12m_prev": s12[-13] if len(s12) > 13 else None,
                          "mes": col[-1]}
    D["interv_last_date"] = iv.get("ultimo_dia_diario") or ivd[-1]
    D["interv_month"] = _month_key(ivd[-1])

    # --- CFTC ---------------------------------------------------------------
    ct = D["cot_fx"]
    ctd = [str(x)[:10] for x in ct["dates"]]
    D["cot_date"] = ctd[-1]
    D["cot"] = {}
    for k in ("asset_mgr_net", "lev_net", "dealer_net", "other_net", "nonrept_net", "open_interest"):
        if k in ct:
            vals_k = ct[k]
            t3 = (_dt.date.fromisoformat(ctd[-1]) - _dt.timedelta(days=90)).isoformat()
            t12 = (_dt.date.fromisoformat(ctd[-1]) - _dt.timedelta(days=365)).isoformat()
            clean = [v for v in vals_k if v is not None]
            D["cot"][k] = {"now": _last(vals_k), "m3": _at_or_before(ctd, vals_k, t3),
                           "y1": _at_or_before(ctd, vals_k, t12),
                           "min": min(clean), "max": max(clean)}
    D["cot_series"] = ct
    D["cot_dates"] = ctd

    # --- Diferenciais de juros ---------------------------------------------
    df = D["diferenciais"]
    dfd = [str(x)[:10] for x in df["dates"]]
    D["dif"] = {k: {"now": _last(df[k]),
                    "month": _month_key([d for d, v in zip(dfd, df[k]) if v is not None][-1]),
                    "y1": _at_or_before(dfd, df[k], (_dt.date.fromisoformat(dfd[-1]) - _dt.timedelta(days=365)).isoformat())}
              for k in ("selic", "fed_funds", "diferencial_nominal", "diferencial_real",
                        "real_br_ex_post", "ipca_12m", "cpi_12m_us")}
    D["carry_breakeven"] = D["px"]["last"] * (1.0 + D["dif"]["diferencial_nominal"]["now"] / 100.0)

    # --- FX Attribution -----------------------------------------------------
    D["attr"] = {}
    cats = [c["slug"] for c in fxa.CATEGORIES]
    D["attr_cat_label"] = {c["slug"]: c["label"] for c in fxa.CATEGORIES}
    D["attr_cats"] = cats
    mix24, mix_prev = {c: 0.0 for c in cats}, {c: 0.0 for c in cats}
    tot_docs = tot_claims = 0
    for mgr in ("kinea", "verde_asset", "kapitalo"):
        p = fxa.build_manager_payload(mgr)
        D["attr"][mgr] = p
        tot_docs += p["totals"]["n_documents"]
        tot_claims += p["totals"]["n_claims"]
        # Janelas SIMETRICAS de 24 meses. Com janelas de tamanhos diferentes
        # por gestor (a Kinea tem serie mais curta), a comparacao de
        # participacao fica enviesada pelo gestor que tem mais historico.
        for c in cats:
            mix24[c] += sum(abs(v) for v in p["monthly"][c][-24:])
            mix_prev[c] += sum(abs(v) for v in p["monthly"][c][-48:-24])
    D["attr_totals"] = {"docs": tot_docs, "claims": tot_claims, "managers": 3}
    s24, sp = sum(mix24.values()), sum(mix_prev.values())
    D["attr_mix"] = {c: (100 * mix24[c] / s24, 100 * mix_prev[c] / sp if sp else 0.0) for c in cats}

    # meses sem claim da Kapitalo
    kp = D["attr"]["kapitalo"]
    last_claim_i = max((i for i, v in enumerate(kp["n_claims"]) if v > 0), default=None)
    D["kapitalo_silence"] = {
        "last_claim_month": kp["months"][last_claim_i] if last_claim_i is not None else None,
        "months_silent": len(kp["months"]) - 1 - last_claim_i if last_claim_i is not None else None,
        "last_month": kp["months"][-1],
        "docs_since": sum(kp["n_documents"][last_claim_i + 1:]) if last_claim_i is not None else 0,
    }

    # --- Modelo -------------------------------------------------------------
    P = rdm.build_dashboard_payload()
    D["ridge"] = P
    D["model_resid"] = sim.spot_residual(P)

    # --- de onde viemos: o movimento desde dez/2024 aberto por forca --------
    # `contrib_monthly` e a contribuicao NAO acumulada de cada balde, um numero
    # por mes, entao a soma sobre a janela e a contribuicao daquela janela --
    # exata, porque o balde "residual" fecha a identidade por construcao. Somar
    # a serie ACUMULADA no lugar arrastaria o acervo de 2006 para dentro da
    # conta de 2025.
    _cm, _mths = P["contrib_monthly"], P["months"]
    _base = "2024-12"
    _i0 = _mths.index("2025-01") if "2025-01" in _mths else 1
    _act = P["fit_level"]["actual"]
    _nc = P["forecast"]["nowcast"].get("ptax") or {"months": [], "values": []}
    D["hist_dec"] = {
        "base": _base,
        "fim_modelo": _mths[-1],
        "ptax0": _act[_i0 - 1],
        "ptax1": _act[-1],
        "parts": {k: float(sum(v[_i0:])) for k, v in _cm.items()},
        "meses": len(_mths) - _i0,
        # o trecho ja realizado depois do corte do ajuste, que o modelo nao
        # decompoe: dito em separado em vez de somado por fora
        "pos_corte_mes": _nc["months"][-1] if _nc["months"] else None,
        "pos_corte_ptax": _nc["values"][-1] if _nc["values"] else None,
    }

    fc = P["forecast"]
    D["betas"] = fc["beta"]
    D["stds"] = {k: v["std"] for k, v in fc["channel_stats"].items()}
    D["ch_now"] = {}
    for rk in ("fiscal", "dxy_em", "carry_vol", "sp500", "icbr_usd", "ppp"):
        nc = fc["nowcast"]["channels"].get(rk) or {"months": [], "values": []}
        hist = fc["channel_history"][rk]
        if nc["values"]:
            D["ch_now"][rk] = {"month": nc["months"][-1], "value": nc["values"][-1]}
        else:
            D["ch_now"][rk] = {"month": hist["months"][-1], "value": hist["values"][-1]}

    # sensibilidade de cada canal, em pp de log por choque unitario
    b, sd = D["betas"], D["stds"]
    D["sens"] = {
        "cds100": b["delta_fiscal"] * 100.0 / sd["delta_fiscal"],
        "dxy1pct": b["delta_dxy_em"] * (D["ch_now"]["dxy_em"]["value"] * 0.01) / sd["delta_dxy_em"],
        "sp10dn": b["delta_sp500"] * (100 * math.log(0.90)) / sd["delta_sp500"],
        "icbr10dn": b["delta_icbr_usd"] * (100 * math.log(0.90)) / sd["delta_icbr_usd"],
        "carry010": b["delta_carry_vol"] * (-0.10) / sd["delta_carry_vol"],
    }

    sr = P.get("sample_range") or ["2006-02", "2026-06"]
    D["sample_txt"] = "%s a %s, %d meses" % (mes(sr[0]), mes(sr[1]), P.get("n", 0))
    D["r2"] = P["whole_sample"].get("r2") if isinstance(P.get("whole_sample"), dict) else None
    D["r2_win"] = P["last_window"].get("r2") if isinstance(P.get("last_window"), dict) else None

    # --- Calibragem dos cenarios -------------------------------------------
    D["cal"] = _calibrate(P)
    D["scen"] = _scenarios(P, D)
    return D


# ---------------------------------------------------------------------------
# Calibragem: frequencias historicas do CDS e as seis eleicoes
# ---------------------------------------------------------------------------
BANDS = [(0.0, 0.89, "até 0,89x"), (0.89, 1.33, "0,89x a 1,33x"), (1.33, 99.0, "1,33x ou mais")]
ELEICOES = (2002, 2006, 2010, 2014, 2018, 2022)


def _calibrate(P):
    h = P["exog_scenarios"]["channels"]["fiscal"]["history"]
    M, V = h["months"], h["values"]
    mv = dict(zip(M, V))
    wins = [(V[i + 12] / V[i], V[i]) for i in range(len(V) - 12)]

    def freq(sample):
        out = []
        for lo, hi, lab in BANDS:
            k = sum(1 for m, _ in sample if lo <= m < hi)
            out.append((lab, k, 100.0 * k / len(sample)))
        return out

    bases = sorted(b for _, b in wins)
    q1 = bases[len(bases) // 4]
    low = [w for w in wins if w[1] <= q1]

    els = []
    for y in ELEICOES:
        a, b2 = mv.get("%d-09" % y), mv.get("%d-09" % (y + 1))
        if a and b2:
            els.append({"ano": y, "base": a, "fim": b2, "mult": b2 / a})

    # Spearman entre nivel de partida e multiplo subsequente
    rho = None
    if len(els) >= 3:
        nn = len(els)
        rb = {i: r + 1 for r, i in enumerate(sorted(range(nn), key=lambda i: els[i]["base"]))}
        rm = {i: r + 1 for r, i in enumerate(sorted(range(nn), key=lambda i: els[i]["mult"]))}
        dd = sum((rb[i] - rm[i]) ** 2 for i in range(nn))
        rho = 1 - 6.0 * dd / (nn * (nn * nn - 1))

    dist = P["exog_scenarios"]["channels"]["fiscal"]["distribution"]["12m"]
    return {
        "n_windows": len(wins), "freq_all": freq(wins),
        "q1": q1, "n_low": len(low), "freq_low": freq(low),
        "eleicoes": els, "rho": rho,
        "cds_now": V[-1], "cds_month": M[-1], "cds_floor": min(V),
        "p": {k: math.exp(dist[k] / 100.0) for k in ("p5", "p50", "p90", "p95", "p99")},
        "dist_n": dist["n"],
        "episodes": P["exog_scenarios"]["channels"]["fiscal"]["episodes"],
        "ep_mult": {e["id"]: e["peak"] / e["base"]
                    for e in P["exog_scenarios"]["channels"]["fiscal"]["episodes"]
                    if e.get("base")},
    }


# ---------------------------------------------------------------------------
# Os tres cenarios
# ---------------------------------------------------------------------------
N_FREE = 12  # out/26 .. set/27


def _ramp(a, b, k=N_FREE):
    return [a + (b - a) * (i + 1) / k for i in range(k)]


def _hump(a, peak, end, i_peak, k=N_FREE):
    out = []
    for i in range(k):
        if i <= i_peak:
            out.append(a + (peak - a) * (i + 1) / (i_peak + 1))
        else:
            out.append(peak + (end - peak) * (i - i_peak) / (k - 1 - i_peak))
    return out


def _scenarios(P, D):
    c = D["ch_now"]
    cds0, dxy0, sp0, cv0, ic0 = (c["fiscal"]["value"], c["dxy_em"]["value"],
                                 c["sp500"]["value"], c["carry_vol"]["value"], c["icbr_usd"]["value"])

    spec = {
        "otimista": dict(
            cds_pico=118.0, cds_fim=95.0, i_pico=1,
            dxy=-5.0, sp=+10.0, carry=1.0625, icbr=+6.0,
        ),
        "neutro": dict(
            cds_pico=125.0, cds_fim=118.0, i_pico=1,
            dxy=0.0, sp=+7.0, carry=0.925, icbr=0.0,
        ),
        "pessimista": dict(
            cds_pico=215.0, cds_fim=200.0, i_pico=5,
            dxy=+6.0, sp=-12.0, carry=0.656, icbr=-12.0,
        ),
    }

    paths = {}
    for k, s in spec.items():
        paths[k] = {
            "delta_fiscal": _hump(cds0, s["cds_pico"], s["cds_fim"], s["i_pico"]),
            "delta_dxy_em": _ramp(dxy0, dxy0 * (1 + s["dxy"] / 100.0)),
            "delta_sp500": _ramp(sp0, sp0 * (1 + s["sp"] / 100.0)),
            "delta_carry_vol": _ramp(cv0, s["carry"]),
            "delta_icbr_usd": _ramp(ic0, ic0 * (1 + s["icbr"] / 100.0)),
        }

    res = sim.build_paths(P, paths)
    obs = P["forecast"]["nowcast"]["ptax"]["values"][-1]
    for k, r in res.items():
        n0 = r["n_real"]
        acc = {}
        for cc in r["contrib"][n0:]:
            for kk, vv in cc.items():
                acc[kk] = acc.get(kk, 0.0) + vv
        r["acc"] = acc
        r["spec"] = spec[k]
        r["fim"] = r["path"][-1]
        r["var_pct"] = 100.0 * (r["path"][-1] / obs - 1.0)
        r["dez26"] = r["path"][n0 + 2]
        r["jun27"] = r["path"][n0 + 8]
        r["start"] = obs
        r["free"] = paths[k]
        r["cds0"], r["dxy0"], r["sp0"], r["cv0"], r["ic0"] = cds0, dxy0, sp0, cv0, ic0
    res["_probs"] = {"otimista": 20, "neutro": 35, "pessimista": 45}
    return res


# ===========================================================================
# Graficos
# ===========================================================================
def _year_ticks(ax, dates, every=1):
    """Marca o primeiro ponto de cada ano na série."""
    seen, idx, lab = set(), [], []
    for i, d in enumerate(dates):
        y = d[:4]
        if y not in seen:
            seen.add(y)
            if int(y) % every == 0:
                idx.append(i)
                lab.append(y)
    ax.set_xticks(idx)
    ax.set_xticklabels(lab, fontsize=8)


def fig_ptax(D):
    pairs = [(d, v) for d, v in D["px"]["pairs"] if d >= "2015-01-01"]
    dts = [d for d, _ in pairs]
    vals = [v for _, v in pairs]
    fig, ax = _fig()
    i26 = next(i for i, d in enumerate(dts) if d >= "2026-01-01")
    ax.axvspan(i26, len(dts) - 1, color="#EEF1F7", zorder=0)
    ax.plot(range(len(vals)), vals, color=C_NAVY, lw=1.4)
    ax.axhline(D["px"]["mean25"], color=C_GOLD, lw=1.2, ls="--",
               label="média de 2025: %s" % n(D["px"]["mean25"], 2))
    ax.scatter([len(vals) - 1], [D["px"]["last"]], s=26, color=C_RED, zorder=5)
    ax.annotate(n(D["px"]["last"], 2), (len(vals) - 1, D["px"]["last"]),
                textcoords="offset points", xytext=(-6, 9), fontsize=8.5,
                color=C_RED, fontweight="bold", ha="right")
    ax.text(i26 + 12, ax.get_ylim()[1], "2026", fontsize=8, color=C_MUTED, va="top")
    _year_ticks(ax, dts)
    ax.yaxis.set_major_formatter(_br_fmt(2))
    ax.set_ylabel("R$ por US$", fontsize=8.2, color="#55607A")
    _title(ax, "Dólar à vista (PTAX venda)",
           "Fonte: Banco Central (SGS 1), diário, de jan/15 a %s" % dmy(D["px"]["date"]))
    _legend(ax)
    fig.tight_layout()
    return fig


def fig_reer(D):
    rh = D["reer_hist"]
    dts = rh["dates"]
    i0 = next(i for i, d in enumerate(dts) if d >= "2010-01-01")
    fig, ax = _fig()
    cols = {"BR": C_NAVY, "MX": C_GOLD, "CL": C_GREEN, "CO": C_PURPLE}
    nomes = {"BR": "Brasil", "MX": "México", "CL": "Chile", "CO": "Colômbia"}
    for c in ("BR", "MX", "CL", "CO"):
        ax.plot(range(len(dts) - i0), rh[c][i0:], color=cols[c],
                lw=2.1 if c == "BR" else 1.1, label=nomes[c],
                alpha=1.0 if c == "BR" else 0.7)
    ax.axhline(100, color="#B8BEC9", lw=0.8)
    ax.annotate(n(D["reer_now"]["BR"], 1), (len(dts) - 1 - i0, D["reer_now"]["BR"]),
                textcoords="offset points", xytext=(-5, 9), fontsize=8.5,
                color=C_NAVY, fontweight="bold", ha="right")
    _year_ticks(ax, dts[i0:], every=2)
    ax.yaxis.set_major_formatter(_br_fmt(0))
    ax.set_ylabel("índice, 2020 = 100", fontsize=8.2, color="#55607A")
    _title(ax, "Câmbio real efetivo: o real contra os vizinhos",
           "BIS, mensal. Quanto mais alto, mais cara a moeda. Até %s" % mes(D["reer_last_month"]))
    _legend(ax, ncol=4)
    fig.tight_layout()
    return fig


def fig_tot(D):
    td, tv = D["tot"]["dates"], D["tot"]["values"]
    j0 = next(i for i, d in enumerate(td) if d >= "2010-01-01")
    fig, ax = _fig()
    ax.plot(range(len(td) - j0), tv[j0:], color=C_GREEN, lw=1.9, label="Termos de troca")
    mx = D["tot"]["max"]
    ax.axhline(mx, color=C_RED, lw=1.0, ls="--",
               label="recorde: %s, em %s" % (n(mx, 1), mes(D["tot"]["max_month"])))
    ax.annotate(n(D["tot"]["last"], 1), (len(td) - 1 - j0, D["tot"]["last"]),
                textcoords="offset points", xytext=(-5, 9), fontsize=8.5,
                color=C_GREEN, fontweight="bold", ha="right")
    _year_ticks(ax, td[j0:], every=2)
    ax.yaxis.set_major_formatter(_br_fmt(0))
    ax.set_ylabel("índice, 2018 = 100", fontsize=8.2, color="#55607A")
    _title(ax, "Termos de troca: preço do que o Brasil vende sobre o do que compra",
           "Funcex, mensal. Até %s" % mes(D["tot"]["month"]))
    _legend(ax)
    fig.tight_layout()
    return fig


def fig_cc(D):
    bd, R, g = D["bop_dates"], D["bop12_series"], D["gdp12_series"]
    i0 = next(i for i, d in enumerate(bd) if d >= "2010-01-01")
    x = list(range(len(bd) - i0))

    def pct(key):
        return [100.0 * R[key][i] / g[i] if R[key][i] is not None and g[i] else None
                for i in range(i0, len(bd))]

    fig, ax = _fig()
    comp = [("mercadorias_gerais", "Bens (exporta menos importa)", C_GREEN),
            ("servicos", "Serviços (viagem, frete, seguro)", C_GOLD),
            ("renda_primaria", "Renda (lucros e juros ao exterior)", C_RED),
            ("renda_secundaria", "Transferências", C_PURPLE)]
    pos = [0.0] * len(x)
    neg = [0.0] * len(x)
    for key, lab, col in comp:
        v = pct(key)
        bot = [pos[i] if (v[i] or 0) >= 0 else neg[i] for i in range(len(x))]
        ax.bar(x, [vv or 0 for vv in v], bottom=bot, color=col, width=1.0, label=lab, alpha=0.9)
        for i in range(len(x)):
            if (v[i] or 0) >= 0:
                pos[i] += v[i] or 0
            else:
                neg[i] += v[i] or 0
    ax.plot(x, pct("conta_corrente"), color=C_NAVY, lw=2.0, label="Conta corrente (total)")
    ax.axhline(0, color="#98A1B5", lw=0.8)
    _year_ticks(ax, bd[i0:], every=2)
    ax.yaxis.set_major_formatter(_br_fmt(0))
    ax.set_ylabel("% do PIB, acumulado em 12 meses", fontsize=8.2, color="#55607A")
    _title(ax, "Conta corrente e suas partes",
           "Banco Central (BPM6). Negativo = o país gasta com o exterior mais do que recebe. Até %s"
           % mes(D["bop_month"]))
    _legend(ax, ncol=3)
    fig.tight_layout()
    return fig


def fig_fin(D):
    bd, R = D["bop_dates"], D["bop12_series"]
    i0 = next(i for i, d in enumerate(bd) if d >= "2010-01-01")
    x = list(range(len(bd) - i0))
    fig, ax = _fig()
    ax.plot(x, R["idp_ingressos"][i0:], color=C_GREEN, lw=1.8,
            label="Investimento direto (fábrica, participação)")
    ax.plot(x, R["portfolio_passivos"][i0:], color=C_GOLD, lw=1.8,
            label="Investimento em carteira (ações e títulos)")
    ax.plot(x, [-v if v is not None else None for v in R["conta_corrente"][i0:]],
            color=C_NAVY, lw=1.6, ls="--", label="Necessidade de financiamento")
    ax.axhline(0, color="#98A1B5", lw=0.8)
    _year_ticks(ax, bd[i0:], every=2)
    ax.yaxis.set_major_formatter(_br_fmt(0))
    ax.set_ylabel("US$ bilhões em 12 meses", fontsize=8.2, color="#55607A")
    _title(ax, "Quem financia o déficit",
           "Banco Central (BPM6), ingressos brutos. Até %s" % mes(D["bop_month"]))
    _legend(ax)
    fig.tight_layout()
    return fig


def fig_comex_fator(D):
    """A pauta de exportacao, em nivel e ao longo do tempo.

    Antes eram tres barras com a VARIACAO de doze meses. Elas repetiam o numero
    que o texto ao lado ja diz e nao mostravam o que importa aqui: que a
    distancia entre as duas linhas vem crescendo ha uma decada. A serie responde
    margem e nivel de uma vez, que e a separacao que este documento faz.
    """
    cf = D["comex_fator_agregado"]
    dts = [str(x)[:10] for x in cf["dates"]]
    i0 = next(i for i, d in enumerate(dts) if d >= "2012-01-01")
    fig, ax = _fig()
    for k, lab, col in (("export_basicos", "Básicos (soja, minério, petróleo, carne)", C_GREEN),
                        ("export_manufaturados", "Manufaturados", C_NAVY)):
        s = _roll_sum(cf[k], 12)
        ax.plot(range(len(dts) - i0), s[i0:], color=col, lw=1.9, label=lab)
        ax.annotate(n(s[-1], 0), (len(dts) - 1 - i0, s[-1]), textcoords="offset points",
                    xytext=(-5, 9), fontsize=8.5, color=col, fontweight="bold", ha="right")
    _year_ticks(ax, dts[i0:], every=2)
    ax.yaxis.set_major_formatter(_br_fmt(0))
    ax.set_ylabel("US$ bilhões, acumulado em 12 meses", fontsize=8.2, color="#55607A")
    _title(ax, "A exportação que cresce é a de commodity",
           "Comex Stat / MDIC. Até %s" % mes(D["comex_month"]))
    _legend(ax)
    fig.tight_layout()
    return fig


def fig_comex_pais(D):
    cp = D["comex_pais"]
    dts = [str(x)[:10] for x in cp["dates"]]
    i0 = next(i for i, d in enumerate(dts) if d >= "2012-01-01")
    fig, ax = _fig()
    ex, im = _roll_sum(cp["export_mundo"], 12), _roll_sum(cp["import_mundo"], 12)
    tot = [(a - b) if (a is not None and b is not None) else None for a, b in zip(ex, im)]
    ax.plot(range(len(dts) - i0), tot[i0:], color=C_MUTED, lw=1.5, ls="--",
            label="Saldo com o mundo")
    for key, lab, col in (("saldo_china", "China", C_GOLD),
                          ("saldo_eua", "Estados Unidos", C_NAVY)):
        s = _roll_sum(cp[key], 12)
        ax.plot(range(len(dts) - i0), s[i0:], color=col, lw=1.9, label=lab)
        ax.annotate(n(s[-1], 0), (len(dts) - 1 - i0, s[-1]), textcoords="offset points",
                    xytext=(-5, 9), fontsize=8.5, color=col, fontweight="bold", ha="right")
    ax.axhline(0, color="#98A1B5", lw=0.9)
    _year_ticks(ax, dts[i0:], every=2)
    ax.yaxis.set_major_formatter(_br_fmt(0))
    ax.set_ylabel("US$ bilhões, acumulado em 12 meses", fontsize=8.2, color="#55607A")
    _title(ax, "O superávit comercial tem uma origem só",
           "Comex Stat / MDIC. Até %s" % mes(D["comex_month"]))
    _legend(ax)
    fig.tight_layout()
    return fig


def fig_fluxo(D):
    cd = D["fluxo_dates"]
    S = D["fluxo_series"]
    i0 = next(i for i, d in enumerate(cd) if d >= "2010-01-01")
    x = list(range(len(cd) - i0))
    fig, ax = _fig()
    # As duas parcelas somam ao saldo total, entao tem de EMPILHAR. Desenhadas
    # como duas chamadas de bar() sem base, elas se sobrepoem: nos anos em que
    # comercial e financeiro tem o mesmo sinal, a segunda cobre a primeira e o
    # grafico passa a contradizer a legenda ao lado dele.
    com = [v or 0 for v in S["cc_saldo_comercial"][i0:]]
    fin = [v or 0 for v in S["cc_fin_saldo"][i0:]]
    ax.bar(x, com, color=C_GREEN, width=1.0, label="Comercial (exportador e importador)")
    base = [c if (f >= 0) == (c >= 0) else 0.0 for c, f in zip(com, fin)]
    ax.bar(x, fin, bottom=base, color=C_GOLD, width=1.0,
           label="Financeiro (investidor, empresa, remessa)")
    ax.plot(x, S["cc_saldo_total"][i0:], color=C_NAVY, lw=2.0, label="Saldo total")
    ax.axhline(0, color="#98A1B5", lw=0.9)
    _year_ticks(ax, cd[i0:], every=2)
    ax.yaxis.set_major_formatter(_br_fmt(0))
    ax.set_ylabel("US$ bilhões, acumulado em 12 meses", fontsize=8.2, color="#55607A")
    _title(ax, "Dólares efetivamente contratados com os bancos",
           "Banco Central, Tabela 13. Positivo = entrou mais do que saiu. Até %s" % mes(D["fluxo_month"]))
    _legend(ax, ncol=3)
    fig.tight_layout()
    return fig


def fig_ouro(D):
    """O que mudou nas reservas foi a COMPOSICAO, nao o tamanho.

    A coluna empilhada que estava aqui nao dizia nada: a parcela em moeda
    estrangeira e ~90% do total e esmaga as outras tres, entao o grafico era
    uma barra azul com uma tira colorida em cima, plana por quinze anos.

    O achado esta na razao, e ele so aparece pondo as tres series em multiplo
    de uma mesma base: o total nao andou, o ouro em dolar multiplicou, e o
    VOLUME de ouro subiu junto, em degraus. O que a linha de volume sobe e
    compra; a distancia entre ela e a linha de valor e preco. Sao as duas
    causas que o texto separa, ditas pelo desenho.
    """
    base_m = "2021-01"
    arv, ad = D["res_series"], D["res_dates"]
    am = [_month_key(d) for d in ad]

    def _map(vals):
        return {m: v for m, v in zip(am, vals or []) if v is not None}

    tot = _map(arv.get("reserves_total_monthly"))
    if not tot:                       # sem o total publicado, some as parcelas
        partes = ["reserves_fx_total", "reserves_gold_usd", "reserves_sdrs",
                  "reserves_imf_position"]
        tot = {m: sum((arv[k][i] or 0) for k in partes if k in arv)
               for i, m in enumerate(am)}
    gld = _map(arv["reserves_gold_usd"])
    gv = D.get("gold_vol")
    vol = dict(zip(gv["months"], gv["values"])) if gv else {}

    meses = [m for m in am if m >= base_m and m in tot and m in gld and (not vol or m in vol)]
    b_tot, b_gld = tot[meses[0]], gld[meses[0]]
    x = list(range(len(meses)))
    fig, ax = _fig()
    series = [([tot[m] / b_tot for m in meses], "Reservas totais", C_NAVY, "-", 2.0),
              ([gld[m] / b_gld for m in meses], "Ouro — valor em dólar", C_GOLD, "-", 2.0)]
    if vol:
        b_vol = vol[meses[0]]
        series.append(([vol[m] / b_vol for m in meses], "Ouro — quantidade de onças",
                       C_GREEN, "--", 1.8))
    for ys, lab, col, ls, lw in series:
        ax.plot(x, ys, color=col, lw=lw, ls=ls, label=lab)
        ax.annotate("%sx" % n(ys[-1], 1), (x[-1], ys[-1]), textcoords="offset points",
                    xytext=(6, -3), fontsize=8.5, color=col, fontweight="bold", ha="left")
    ax.axhline(1.0, color="#B8BEC9", lw=0.8)
    ax.set_xlim(0, len(meses) - 1 + max(5.0, len(meses) * 0.09))
    _monthly_ticks(ax, meses, every=6, rot=45)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: n(v, 1) + "x"))
    ax.set_ylabel("múltiplo do valor de %s" % mes(base_m), fontsize=8.2, color="#55607A")
    _title(ax, "As reservas não cresceram; o ouro dentro delas, sim",
           "Banco Central, mensal. Cada linha é o múltiplo do próprio valor de %s. Até %s"
           % (mes(base_m), mes(D["res_month"])))
    _legend(ax)
    fig.tight_layout()
    return fig


def fig_swap(D):
    sw, sd = D["swap_series"], D["swap_dates"]
    j0 = next(i for i, d in enumerate(sd) if d >= "2010-01-01")
    fig, ax = _fig()
    ax.plot(range(len(sd) - j0), sw["bcb_swap_cambial_position"][j0:], color=C_RED, lw=1.9,
            label="Swap cambial do Banco Central")
    ax.plot(range(len(sd) - j0), sw["bank_fx_spot_position"][j0:], color=C_NAVY, lw=1.4,
            label="Posição dos bancos")
    ax.axhline(0, color="#98A1B5", lw=0.9)
    _year_ticks(ax, sd[j0:], every=2)
    ax.yaxis.set_major_formatter(_br_fmt(0))
    ax.set_ylabel("US$ bilhões", fontsize=8.2, color="#55607A")
    _title(ax, "Exposição vendida em dólar",
           "Banco Central. Negativo = vendido em dólar. Até %s"
           % mes(D["swap"]["bcb_swap_cambial_position"]["date"]))
    _legend(ax)
    fig.tight_layout()
    return fig


def fig_cot(D):
    ct, cd = D["cot_series"], D["cot_dates"]
    i0 = next(i for i, d in enumerate(cd) if d >= "2015-01-01")
    x = list(range(len(cd) - i0))
    fig, ax = _fig()
    for k, lab, col in (("asset_mgr_net", "Gestores de recursos", C_NAVY),
                        ("lev_net", "Fundos alavancados", C_GOLD),
                        ("dealer_net", "Bancos (contraparte)", C_MUTED)):
        ax.plot(x, [v / 1000.0 if v is not None else None for v in ct[k][i0:]],
                color=col, lw=1.9 if k != "dealer_net" else 1.1, label=lab,
                alpha=1.0 if k != "dealer_net" else 0.7)
    ax.axhline(0, color="#98A1B5", lw=0.9)
    _year_ticks(ax, cd[i0:], every=1)
    ax.yaxis.set_major_formatter(_br_fmt(0))
    ax.set_ylabel("mil contratos, posição líquida", fontsize=8.2, color="#55607A")
    _title(ax, "Aposta líquida no real no mercado futuro americano",
           "CFTC (CME), semanal. Positivo = apostando na valorização do real. Até %s" % dmy(D["cot_date"]))
    _legend(ax)
    fig.tight_layout()
    return fig


def fig_attr_mix(D):
    itens = sorted(D["attr_mix"].items(), key=lambda kv: -kv[1][0])[:6]
    labs = [CAT_PT.get(k, D["attr_cat_label"][k]) for k, _ in itens]
    a24 = [v[0] for _, v in itens]
    aprev = [v[1] for _, v in itens]
    y = list(range(len(itens)))
    fig, ax = _fig(6.4, 2.95)
    ax.barh([i + 0.20 for i in y], a24, height=0.38, color=C_NAVY, label="últimos 24 meses")
    ax.barh([i - 0.20 for i in y], aprev, height=0.38, color="#B9C0D2", label="24 meses anteriores")
    for i, (v, w) in enumerate(zip(a24, aprev)):
        ax.annotate("%s%%" % n(v, 1), (v, i + 0.20), textcoords="offset points",
                    xytext=(4, -3), fontsize=8, color=C_NAVY, fontweight="bold")
        ax.annotate("%s%%" % n(w, 1), (w, i - 0.20), textcoords="offset points",
                    xytext=(4, -3), fontsize=8, color="#7B839A")
    ax.set_yticks(y)
    ax.set_yticklabels(labs, fontsize=8.5)
    ax.invert_yaxis()
    ax.grid(axis="y", lw=0)
    ax.grid(axis="x", color=C_GRID, lw=0.6)
    ax.set_xlim(0, max(a24 + aprev) * 1.18)
    ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _: n(v, 0) + "%"))
    _title(ax, "O assunto mudou: peso de cada causa no que as gestoras dizem",
           "Participação no total do que foi afirmado sobre câmbio, três casas somadas")
    _legend(ax, ncol=2)
    fig.tight_layout()
    return fig


def fig_attr_div(D):
    k, v = D["attr"]["kinea"], D["attr"]["verde_asset"]
    ms = k["months"][-24:]
    kv = k["monthly"]["global_usd"][-24:]
    vv = [v["monthly"]["global_usd"][v["months"].index(m)] if m in v["months"] else 0.0 for m in ms]
    xx = list(range(len(ms)))
    fig, ax = _fig(6.4, 2.75)
    ax.bar([i - 0.21 for i in xx], kv, width=0.42, color=C_NAVY, label="Kinea")
    ax.bar([i + 0.21 for i in xx], vv, width=0.42, color=C_GOLD, label="Verde")
    ax.axhline(0, color="#98A1B5", lw=0.9)
    idx = list(range(0, len(ms), 3))
    ax.set_xticks(idx)
    ax.set_xticklabels([mes(ms[i]) for i in idx], fontsize=8, rotation=45, ha="right")
    ax.yaxis.set_major_formatter(_br_fmt(1))
    ax.set_ylabel("efeito atribuído ao real", fontsize=8.2, color="#55607A")
    ax.set_ylim(-1.15, 1.15)
    _title(ax, "Dólar global: a mesma causa, lida em direções opostas",
           "Positivo = argumento a favor do real. Zero = o canal não foi citado no mês")
    _legend(ax, ncol=2)
    fig.tight_layout()
    return fig


def fig_decomp(D):
    dec = D["ridge"]["decomposition"]
    ordem = [("delta_ppp", "Diferença\nde inflação", C_MUTED),
             ("delta_dxy_em", "Dólar global\n(emergentes)", C_NAVY),
             ("delta_sp500", "Bolsa\namericana", C_GOLD),
             ("delta_icbr_usd", "Commodities", C_GREEN),
             ("delta_fiscal", "Risco Brasil\n(CDS)", C_RED),
             ("delta_carry_vol", "Juro por\nvolatilidade", C_PURPLE),
             ("baseline", "Não\nexplicado", "#9AA3B8")]
    vals, labs, cols = [], [], []
    for k, lab, col in ordem:
        v = dec.get(k)
        if isinstance(v, dict):
            v = v.get("total", v.get("cumulative"))
        if isinstance(v, (list, tuple)):
            # a decomposicao vem como serie acumulada; o que interessa e o
            # total ao fim da amostra
            v = next((z for z in reversed(v) if z is not None), None)
        if v is None:
            continue
        vals.append(float(v))
        labs.append(lab)
        cols.append(col)
    fig, ax = _fig(6.4, 2.95)
    b = ax.bar(range(len(vals)), vals, color=cols, width=0.62)
    for r, v in zip(b, vals):
        ax.annotate(n(v, 1, sign=True), (r.get_x() + r.get_width() / 2, v),
                    textcoords="offset points", xytext=(0, 4 if v >= 0 else -13),
                    ha="center", fontsize=8.2, color=C_NAVY, fontweight="bold")
    ax.axhline(0, color="#98A1B5", lw=0.9)
    ax.set_xticks(range(len(labs)))
    ax.set_xticklabels(labs, fontsize=7.6)
    ax.set_ylim(min(0, min(vals)) * 1.48, max(vals) * 1.24)
    ax.yaxis.set_major_formatter(_br_fmt(0))
    ax.set_ylabel("contribuição acumulada, %", fontsize=8.2, color="#55607A")
    _title(ax, "O que moveu o dólar na amostra do modelo",
           "%s. Positivo = empurrou o dólar para cima (real mais fraco)" % D["sample_txt"])
    fig.tight_layout()
    return fig


def fig_hist_decomp(D):
    """O movimento desde dez/2024, aberto pelas forcas do modelo.

    Barras horizontais porque os rotulos sao frases, ordenadas da que mais
    valorizou o real para a que mais o enfraqueceu. A ultima barra e o total
    OBSERVADO, contornada em dourado -- sem ela o leitor teria de somar oito
    numeros de cabeca para saber se a conta fecha.
    """
    hd = D["hist_dec"]
    ordem = [("delta_dxy_em", "Dólar global contra emergentes", C_NAVY),
             ("delta_fiscal", "Risco Brasil (CDS)", C_RED),
             ("delta_icbr_usd", "Commodities", C_GREEN),
             ("delta_carry_vol", "Juro por unidade de volatilidade", C_PURPLE),
             ("delta_ppp", "Diferença de inflação", C_MUTED),
             ("delta_sp500", "Bolsa americana", C_GOLD),
             ("baseline", "Base do modelo (constante e inércia)", "#B9C0D2"),
             ("residual", "Não explicado pelas seis forças", "#8A93A8")]
    itens = [(lab, hd["parts"][k], col) for k, lab, col in ordem if k in hd["parts"]]
    itens.sort(key=lambda t: t[1])
    total = 100.0 * math.log(hd["ptax1"] / hd["ptax0"])
    itens.append(("TOTAL observado no período", total, "#2E3A63"))

    labs = [t[0] for t in itens]
    vals = [t[1] for t in itens]
    cols = [t[2] for t in itens]
    y = list(range(len(itens)))
    fig, ax = _fig(6.4, 3.35)
    ax.barh(y, vals, height=0.62, color=cols)
    # a barra do total ganha contorno: ela e de outra natureza que as demais
    ax.barh([y[-1]], [vals[-1]], height=0.62, color="none", edgecolor=C_GOLD, lw=1.6)
    for i, v in enumerate(vals):
        ax.annotate(n(v, 1, sign=True), (v, i), textcoords="offset points",
                    xytext=(5 if v >= 0 else -5, -3.5), ha="left" if v >= 0 else "right",
                    fontsize=8.4, color=C_NAVY, fontweight="bold")
    ax.set_yticks(y)
    ax.set_yticklabels(labs, fontsize=8.5)
    ax.invert_yaxis()
    ax.axvline(0, color="#98A1B5", lw=0.9)
    ax.grid(axis="y", lw=0)
    ax.grid(axis="x", color=C_GRID, lw=0.6)
    lo, hi = min(vals), max(vals)
    ax.set_xlim(lo - abs(lo) * 0.26, hi + abs(hi) * 0.60)
    ax.xaxis.set_major_formatter(_br_fmt(0))
    ax.set_xlabel("contribuição para a variação do dólar, %", fontsize=8.2, color="#55607A")
    _title(ax, "O que trouxe o dólar de R$ %s para R$ %s"
           % (n(hd["ptax0"], 2), n(hd["ptax1"], 2)),
           "Negativo = empurrou o dólar para baixo (real mais forte). De %s a %s"
           % (mes(hd["base"]), mes(hd["fim_modelo"])))
    fig.tight_layout()
    return fig


def fig_scen(D):
    fig, ax = _fig(6.4, 3.4)
    pairs = [(d, v) for d, v in D["px"]["pairs"] if d >= "2023-01-01"]
    hist = {}
    for d, v in pairs:
        hist.setdefault(d[:7], []).append(v)
    hm = sorted(hist)
    hv = [hist[m][-1] for m in hm]
    nh = len(hm)
    ax.plot(range(nh), hv, color="#4A5678", lw=1.6, label="observado")

    S = D["scen"]
    r0 = S["neutro"]
    n0 = r0["n_real"]
    fut_months = r0["months"][n0 - 1:]
    xf = list(range(nh - 1, nh - 1 + len(fut_months)))
    est = {"otimista": (C_GREEN, "Otimista"), "neutro": (C_NAVY, "Neutro"),
           "pessimista": (C_RED, "Pessimista")}
    rn = S["neutro"]
    ax.fill_between(xf, [rn["start"]] + list(rn["lo"][n0:]), [rn["start"]] + list(rn["hi"][n0:]),
                    color=C_NAVY, alpha=0.07, lw=0,
                    label="margem de erro do modelo (mais ou menos 1 desvio)")
    for k in ("otimista", "neutro", "pessimista"):
        col, lab = est[k]
        r = S[k]
        yv = [r["start"]] + list(r["path"][n0:])
        ax.plot(xf, yv, color=col, lw=2.0, ls="--",
                label="%s: %s (%s%%)" % (lab, n(r["fim"], 2), n(r["var_pct"], 1, sign=True)))
        ax.scatter([xf[-1]], [yv[-1]], s=24, color=col, zorder=5)
        ax.annotate(n(yv[-1], 2), (xf[-1], yv[-1]), textcoords="offset points",
                    xytext=(7, -3), fontsize=8.4, color=col, fontweight="bold", ha="left")
    ax.axvline(nh - 1, color="#B8BEC9", lw=0.9, ls=":")

    todos = hm + fut_months[1:]
    ax.set_xlim(0, len(todos) - 1 + 4)
    idx = list(range(0, len(todos), 4))
    ax.set_xticks(idx)
    ax.set_xticklabels([mes(todos[i]) for i in idx], fontsize=8, rotation=45, ha="right")
    ax.yaxis.set_major_formatter(_br_fmt(2))
    ax.set_ylabel("R$ por US$", fontsize=8.2, color="#55607A")
    _title(ax, "Três cenários para o dólar, até %s" % mes(fut_months[-1]),
           "Partem do fechamento de %s. A margem mostrada é a do cenário neutro"
           % mes(D["ch_now"]["fiscal"]["month"]))
    _legend(ax, ncol=2)
    fig.tight_layout()
    return fig


# ===========================================================================
# Projecoes publicadas por terceiros
# ---------------------------------------------------------------------------
# Estas nao sao derivadas do nosso banco: sao transcritas do levantamento de
# 2026-09-08 em `referencia/literature/fair_value_casas_de_gestao.md`, que
# cruzou as cartas do corpus com declaracoes na imprensa. Servem de
# triangulacao -- o texto diz explicitamente que sao de terceiros.
# ---------------------------------------------------------------------------
PROJECOES = [
    ("Verde Asset", "valor justo R$ 4,40", "jan/26", "modelo próprio: dólar contra cesta emergente, juro Selic menos Fed, commodities e risco Brasil"),
    ("Armor Capital", "piso de R$ 4,90", "abr/26", "petróleo alto e um dos maiores juros reais do mundo, mas não deve durar"),
    ("Goldman Sachs", "R$ 5,20 e R$ 5,10 (3 e 6 meses)", "ago/26", "revisão para cima: o mercado passou a dar mais peso à incerteza política"),
    ("Focus (Banco Central)", "R$ 5,20 no fim de 2026", "ago/26", "mediana de cerca de 140 instituições"),
    ("Itaú BBA", "R$ 5,30 no fim de 2026", "ago/26", "aperto adicional nos EUA e prêmios domésticos elevados"),
]


def _story_part1(D):
    st = []
    px, dif = D["px"], D["dif"]
    S, cal = D["scen"], D["cal"]
    probs = S["_probs"]
    ot, ne, pe = S["otimista"], S["neutro"], S["pessimista"]
    hoje = _dt.date.today().isoformat()

    # ------------------------------------------------------------------ capa
    st.append(Paragraph("LIS CAPITAL", ParagraphStyle(
        "brand", fontName="DejaVuSans-Bold", fontSize=10, textColor=GOLD, spaceAfter=2)))
    st.append(Paragraph("Panorama Cambial", TITLE))
    st.append(Paragraph(
        "Onde está o real, o que mudou na margem, e três cenários para os próximos doze meses", SUBTITLE))
    st.append(Paragraph("Documento interno &middot; %s &middot; dados até %s"
                        % (mes_longo(hoje[:7]), dmy(px["date"])), DATE_BADGE))
    st.append(rule(color=NAVY, thickness=2, space_before=8, space_after=10))

    # ------------------------------------------------------- sumario executivo
    st += section_header("", "Sumário executivo", "O que este documento conclui")
    st.append(Paragraph(
        "O real se valorizou ao longo do último ano e as contas externas do país melhoraram. As duas "
        "coisas são verdade e nenhuma das duas é o que parece: a melhora externa veio quase toda de "
        "preço de commodity é de dinheiro financeiro que parou de sair, não de uma correção do "
        "desequilíbrio de fundo. E o mercado já pagou por essa melhora.", LEAD))

    st += bullets([
        "<b>O dólar fechou em R$ %s em %s</b> &mdash; %s%% em doze meses, %s%% em seis, e praticamente "
        "parado no último mês. Em 2026 andou entre R$ %s e R$ %s, contra uma média de R$ %s em 2025."
        % (n(px["last"], 4), dmy(px["date"]), n(px["p12m"], 1, sign=True), n(px["p6m"], 1, sign=True),
           n(px["min26"], 2), n(px["max26"], 2), n(px["mean25"], 2)),

        "<b>O déficit externo diminuiu na margem e continua grande.</b> A conta corrente acumulada em "
        "doze meses saiu de %s%% para %s%% do PIB &mdash; mas dois anos atrás era %s%%. A melhora e "
        "recente; o buraco é estrutural."
        % (n(D["cc_pct_y1"], 2), n(D["cc_pct"], 2), n(D["cc_pct_y2"], 2)),

        "<b>E a melhora é de commodity, não de competitividade.</b> Dos US$ %s bilhões a mais que o "
        "país exportou em doze meses, US$ %s bilhões (%s%%) são produtos básicos. Manufaturados "
        "somaram US$ %s bilhões."
        % (n(D["comex"]["export_mundo"]["var"], 1), n(D["comex"]["export_basicos"]["var"], 1),
           n(100 * D["comex"]["export_basicos"]["var"] / D["comex"]["export_mundo"]["var"], 0),
           n(D["comex"]["export_manufaturados"]["var"], 1)),

        "<b>O fluxo de dólares virou, e virou pelo lado financeiro.</b> O saldo contratado com os "
        "bancos passou de US$ %s bilhões negativos para US$ %s bilhões em doze meses. O comercial "
        "melhorou US$ %s bilhões; o financeiro deixou de sangrar US$ %s bilhões."
        % (n(abs(D["fluxo"]["cc_saldo_total"]["y1"]), 1), n(D["fluxo"]["cc_saldo_total"]["now"], 1),
           n(D["fluxo"]["cc_saldo_comercial"]["now"] - D["fluxo"]["cc_saldo_comercial"]["y1"], 1),
           n(abs(D["fluxo"]["cc_fin_saldo"]["now"] - D["fluxo"]["cc_fin_saldo"]["y1"]), 1)),

        "<b>Quem estava apostando no real está saindo.</b> A posição comprada dos gestores no futuro "
        "americano caiu de %s mil para %s mil contratos em um ano &mdash; ou seja, a valorização "
        "recente não foi puxada por dinheiro especulativo novo entrando."
        % (n(D["cot"]["asset_mgr_net"]["y1"] / 1000.0, 1), n(D["cot"]["asset_mgr_net"]["now"] / 1000.0, 1)),

        "<b>O assunto mudou.</b> Entre os gestores que acompanhamos, o peso do risco fiscal brasileiro "
        "na explicação do câmbio caiu de %s%% para %s%% do que foi dito, enquanto o dólar global subiu "
        "de %s%% para %s%%. O real virou passageiro."
        % (n(D["attr_mix"]["fiscal_br"][1], 0), n(D["attr_mix"]["fiscal_br"][0], 0),
           n(D["attr_mix"]["global_usd"][1], 0), n(D["attr_mix"]["global_usd"][0], 0)),

        "<b>Os três cenários, a doze meses:</b> R$ %s no otimista (%s%%), R$ %s no neutro (%s%%) e "
        "R$ %s no pessimista (%s%%). As probabilidades são %d%%, %d%% e %d%%."
        % (n(ot["fim"], 2), n(ot["var_pct"], 1, sign=True), n(ne["fim"], 2), n(ne["var_pct"], 1, sign=True),
           n(pe["fim"], 2), n(pe["var_pct"], 1, sign=True),
           probs["otimista"], probs["neutro"], probs["pessimista"]),

        "<b>A assimetria está para cima</b>, e a razão é medida: o risco Brasil está em %s pontos, a "
        "menor base de partida de qualquer setembro de ano eleitoral desde que a série existe, e o "
        "piso histórico é %s. Sobra pouco espaço para melhorar e muito para piorar."
        % (n(cal["cds_now"], 0), n(cal["cds_floor"], 0)),
    ])
    st.append(Spacer(1, 4))
    st.append(Paragraph(
        "Uma advertência que vale para o documento inteiro, e que a própria literatura de câmbio "
        "impõe: nenhum modelo de taxa de câmbio bate um passeio aleatório em horizonte de até um ano. "
        "Isso foi estabelecido em 1983 e nunca foi revertido de forma robusta. Os cenários adiante não "
        "são previsão: são a resposta do nosso modelo a caminhos que <i>nós</i> escolhemos para as "
        "forças que o alimentam. O valor está na consistência entre premissa e conclusão, não no "
        "número final.", BODY))
    st.append(PageBreak())

    # ================================================================== 1
    st += section_header("1", "Onde está o real hoje", "Aba Valuation")
    st += margem(
        "O dólar fechou a %s em R$ %s. Não saiu do lugar no último mês (%s%%), caiu %s%% em três meses, "
        "%s%% em seis e <b>%s%% em doze</b>. A valorização do real é real e é grande, mas ela aconteceu "
        "sobretudo entre o fim de 2025 e o começo de 2026 &mdash; nos últimos meses o câmbio está de lado."
        % (dmy(px["date"]), n(px["last"], 4), n(px["p1m"], 1, sign=True), n(abs(px["p3m"]), 1),
           n(abs(px["p6m"]), 1), n(abs(px["p12m"]), 1)))
    st += nivel(
        "Em 2026 o dólar andou entre R$ %s e R$ %s, contra uma média de R$ %s em 2025. O real está perto "
        "do ponto mais forte do próprio ciclo recente &mdash; não numa ruptura, e sim no topo de uma "
        "faixa que ele mesmo desenhou. E útil lembrar a referência que a maioria esqueceu: a máxima "
        "histórica foi R$ 6,21, em janeiro de 2025."
        % (n(px["min26"], 2), n(px["max26"], 2), n(px["mean25"], 2)))
    st.append(Paragraph(
        "Há uma conta que ajuda a dimensionar quanto o câmbio pode andar sem que quem está comprado em "
        "real perca dinheiro. Com a Selic em %s%% ao ano (%s) contra %s%% do juro americano, a diferença "
        "de juros é de %s pontos percentuais. Aplicada ao câmbio de hoje, <b>o dólar precisaria passar de "
        "R$ %s em doze meses</b> para que a posição comprada em real deixasse de dar lucro. É uma folga "
        "de %s%%."
        % (n(dif["selic"]["now"], 2), mes(dif["selic"]["month"]), n(dif["fed_funds"]["now"], 2),
           n(dif["diferencial_nominal"]["now"], 2), n(D["carry_breakeven"], 2),
           n(dif["diferencial_nominal"]["now"], 1)), BODY))
    st.append(chart_box(fig_ptax(D)))
    st.append(caption(
        "A faixa cinza marca 2026. A linha tracejada é a média de 2025, para dar a escala do movimento."))

    # ================================================================== 2
    st += section_header("2", "Preço relativo: câmbio real e termos de troca", "Aba Valuation")
    r_now, r_12 = D["reer_now"], D["reer_12m"]
    st += margem(
        "O câmbio real efetivo &mdash; o câmbio corrigido pela inflação e ponderado pelos parceiros "
        "comerciais, que é a medida de quão cara ou barata a moeda está de fato &mdash; subiu de %s para "
        "<b>%s</b> em doze meses (%s%%), na base do BIS em que 2020 vale 100. E os termos de troca, a "
        "razão entre o preço do que o Brasil vende e o do que compra, foram de %s para <b>%s</b>, a "
        "apenas %s%% do recorde de %s registrado em %s."
        % (n(r_12["BR"], 1), n(r_now["BR"], 1), n(100 * (r_now["BR"] / r_12["BR"] - 1), 1, sign=True),
           n(D["tot"]["prev12"], 1), n(D["tot"]["last"], 1),
           n(100 * (1 - D["tot"]["last"] / D["tot"]["max"]), 1), n(D["tot"]["max"], 1),
           mes(D["tot"]["max_month"])))
    st += nivel(
        "Apesar da valorização, o real segue sendo a moeda barata da região: %s contra %s do México e %s "
        "da Colômbia. Este é o exemplo mais limpo do que este relatório tenta separar &mdash; melhorou na "
        "margem, continua fraco no nível."
        % (n(r_now["BR"], 1), n(r_now["MX"], 1), n(r_now["CO"], 1)))
    st.append(Paragraph(
        "Vale registrar por que damos peso a esses dois gráficos, e não o mesmo peso. A tendência de o "
        "câmbio real voltar ao próprio equilíbrio existe e é lentíssima: a literatura mede meia-vida de "
        "três a cinco anos para desvios de paridade de poder de compra. Como sinal de doze meses, isso "
        "não serve. Já o canal de commodities é o único com suporte empírico direto e robusto para o "
        "real especificamente &mdash; é por isso que termos de troca perto do recorde é uma informação "
        "de peso, e não apenas um número bonito.", BODY))
    st.append(chart_box(fig_reer(D)))
    st.append(caption(
        "Quanto mais alto, mais valorizada a moeda em termos reais. A linha do Brasil está destacada; "
        "as outras três são as moedas com que o real costuma ser comparado."))
    st.append(chart_box(fig_tot(D)))
    st.append(caption(
        "O preço médio do que o país exporta dividido pelo preço médio do que importa. É a medida de "
        "quanto o mundo está pagando pelo que o Brasil vende, e está a poucos por cento do recorde."))

    # ================================================================== 3
    st += section_header("3", "Contas externas: o buraco e quem o financia", "Aba Balanço de Pagamentos")
    b = D["bop12"]
    st += margem(
        "O déficit em conta corrente acumulado em doze meses até %s é de <b>US$ %s bilhões</b>, ou "
        "<b>%s%% do PIB</b>. Doze meses antes era %s%%. Melhorou pouco mais de um ponto percentual."
        % (mes(D["bop_month"]), n(abs(b["conta_corrente"]["now"]), 1), n(D["cc_pct"], 2), n(D["cc_pct_y1"], 2)))
    st += nivel(
        "Dois anos atrás era <b>%s%% do PIB</b>. Ou seja: o déficit encolheu em relação ao ano passado e "
        "ainda está bem maior do que estava antes disso. A frase honesta é que ele parou de piorar, não "
        "que se resolveu." % n(D["cc_pct_y2"], 2))
    st.append(Paragraph(
        "Abrindo as partes, a melhora tem uma origem só e uma piora escondida. A balança de bens passou "
        "de US$ %s para US$ %s bilhões, um ganho de US$ %s bilhões que responde por toda a melhora. Do "
        "outro lado, a conta de renda &mdash; lucros e juros que empresas e investidores estrangeiros "
        "mandam para fora &mdash; <b>piorou</b>, de US$ %s para US$ %s bilhões negativos. Só a conta de lucros e "
        "dividendos subiu de US$ %s para <b>US$ %s bilhões</b>. Serviços ficaram praticamente parados em US$ "
        "%s bilhões negativos."
        % (n(b["mercadorias_gerais"]["y1"], 1), n(b["mercadorias_gerais"]["now"], 1),
           n(b["mercadorias_gerais"]["now"] - b["mercadorias_gerais"]["y1"], 1),
           n(abs(b["renda_primaria"]["y1"]), 1), n(abs(b["renda_primaria"]["now"]), 1),
           n(abs(b["lucros_dividendos"]["y1"]), 1), n(abs(b["lucros_dividendos"]["now"]), 1),
           n(abs(b["servicos"]["now"]), 1)), BODY))
    st.append(chart_box(fig_cc(D)))
    st.append(Paragraph(
        "<b>Quem paga a conta.</b> O déficit está financiado com folga: o investimento direto &mdash; "
        "dinheiro que entra para comprar ou montar empresa, o tipo que não vai embora no dia seguinte "
        "&mdash; somou US$ %s bilhões, <b>%s vezes</b> o tamanho do déficit. Mas a composição ficou mais "
        "quente na margem: o investimento em carteira (ações e títulos, dinheiro que sai rápido) saltou "
        "de US$ %s para <b>US$ %s bilhões</b>, com títulos no mercado doméstico em US$ %s bilhões e a "
        "compra líquida de ações voltando ao positivo (US$ %s bilhões, contra US$ %s bilhões negativos "
        "um ano antes). E dinheiro que ajuda hoje e some rápido se o humor virar."
        % (n(b["idp_ingressos"]["now"], 1), n(D["cobertura_idp"], 2),
           n(b["portfolio_passivos"]["y1"], 1), n(b["portfolio_passivos"]["now"], 1),
           n(b["titulos_dom"]["now"], 1), n(b["acoes_passivos"]["now"], 1),
           n(abs(b["acoes_passivos"]["y1"]), 1)), BODY))
    st.append(chart_box(fig_fin(D)))
    st += caution(
        "<b>Sinal invertido em relação à fonte.</b> Neste relatório, como no dashboard, o lado de ativos "
        "do balanço de pagamentos aparece com o sinal trocado em relação à publicação do Banco Central, "
        "para que a leitura seja a mesma em toda parte: negativo sempre significa dólar saindo do país. "
        "O banco de dados guarda a convenção original.")
    st.append(Paragraph(
        "Uma nota sobre o que este bloco pode e não pode dizer. Déficit em conta corrente é, na teoria, "
        "um fator de moeda mais fraca no longo prazo. Na prática o momento em que isso vira preço é "
        "dominado pelo fluxo de capital, que pode andar na direção contrária por anos &mdash; o dólar "
        "americano subiu durante boa parte dos anos 1980 e do fim dos anos 1990 com o déficit se "
        "abrindo. Serve como pano de fundo, não como gatilho.", BODY))

    # ================================================================== 4
    st += section_header("4", "Comércio: com quem e com o quê", "Aba Balanço de Pagamentos / Comex Stat")
    cx = D["comex"]
    st += margem(
        "Nos doze meses até %s o país exportou US$ %s bilhões, US$ %s bilhões a mais que nos doze meses "
        "anteriores, e importou US$ %s bilhões. O saldo comercial foi de US$ %s bilhões."
        % (mes(D["comex_month"]), n(cx["export_mundo"]["now"], 1), n(cx["export_mundo"]["var"], 1),
           n(cx["import_mundo"]["now"], 1),
           n(cx["export_mundo"]["now"] - cx["import_mundo"]["now"], 1)))
    st += nivel(
        "Mas a composição é o ponto. Dos US$ %s bilhões de ganho, <b>US$ %s bilhões vieram de produtos "
        "básicos</b> &mdash; %s%% do total. Manufaturados contribuíram com US$ %s bilhões, enquanto a "
        "importação de manufaturados subiu US$ %s bilhões. O país não ficou mais competitivo; vendeu "
        "mais do que já vendia, a preços melhores."
        % (n(cx["export_mundo"]["var"], 1), n(cx["export_basicos"]["var"], 1),
           n(100 * cx["export_basicos"]["var"] / cx["export_mundo"]["var"], 0),
           n(cx["export_manufaturados"]["var"], 1), n(cx["import_manufaturados"]["var"], 1)))
    st.append(Paragraph(
        "Quatro produtos explicam quase todo o ganho dos básicos: petróleo (US$ %s bilhões a mais), soja "
        "(US$ %s bilhões), carnes (US$ %s bilhões) e minério de ferro (US$ %s bilhões). Somados, US$ %s "
        "bilhões dos US$ %s bilhões de aumento em básicos.<br/><br/>"
        "Por parceiro, a história se divide em duas. Com a <b>China</b>, a exportação subiu de US$ %s para "
        "US$ %s bilhões e o superávit foi a US$ %s bilhões. Com os <b>Estados Unidos</b>, a exportação "
        "<b>caiu</b> US$ %s bilhões e o saldo está negativo em US$ %s bilhões. A concentração em um "
        "comprador só &mdash; e em um punhado de produtos &mdash; é o que torna o real tão sensível a "
        "preço de commodity, e é por isso que a China aparece nos cenários do fim deste documento."
        % (n(cx["export_petroleo"]["var"], 1), n(cx["export_soja"]["var"], 1),
           n(cx["export_carnes"]["var"], 1), n(cx["export_minerio_ferro"]["var"], 1),
           n(cx["export_petroleo"]["var"] + cx["export_soja"]["var"] + cx["export_carnes"]["var"]
             + cx["export_minerio_ferro"]["var"], 1),
           n(cx["export_basicos"]["var"], 1),
           n(cx["export_china"]["now"] - cx["export_china"]["var"], 1), n(cx["export_china"]["now"], 1),
           n(cx["saldo_china"]["now"], 1), n(abs(cx["export_eua"]["var"]), 1),
           n(abs(cx["saldo_eua"]["now"]), 1)), BODY))
    st.append(chart_box(fig_comex_fator(D)))
    st.append(caption(
        "Exportação acumulada em doze meses, separada entre produtos básicos e manufaturados. A "
        "distância entre as duas linhas é a concentração da pauta, e ela vem crescendo há uma década."))
    st.append(chart_box(fig_comex_pais(D)))
    st.append(caption(
        "Saldo comercial acumulado em doze meses. A linha tracejada é o saldo com o mundo inteiro; as "
        "duas cheias mostram de onde ele vem e com quem ele é negativo."))
    st += caution(
        "<b>Estes números não somam com os do bloco anterior.</b> O Comex Stat mede o comércio pela "
        "passagem na alfândega; o balanço de pagamentos mede pela mudança de propriedade, e exclui "
        "coisas que a alfândega inclui. Os dois cortes se complementam &mdash; um diz com quem e com o "
        "que, o outro diz quanto entra na conta do país &mdash; mas não são a mesma conta aberta de "
        "jeitos diferentes, e somar os dois produz um número que não existe.")

    # ================================================================== 5
    st += section_header("5", "O dólar que entra e sai de fato", "Aba Fluxo Cambial")
    fl = D["fluxo"]
    st += margem(
        "Este é o dado que menos aparece e que mais mudou. O saldo de câmbio efetivamente contratado com "
        "os bancos &mdash; dólares que de fato trocaram de mãos, não o registro contábil &mdash; "
        "acumulou <b>US$ %s bilhões positivos</b> nos doze meses até %s, contra <b>US$ %s bilhões "
        "negativos</b> nos doze anteriores. Uma virada de US$ %s bilhões."
        % (n(fl["cc_saldo_total"]["now"], 1), mes(D["fluxo_month"]),
           n(abs(fl["cc_saldo_total"]["y1"]), 1),
           n(fl["cc_saldo_total"]["now"] - fl["cc_saldo_total"]["y1"], 1)))
    st += nivel(
        "E a virada não veio de onde se imagina. O lado comercial melhorou US$ %s bilhões (de US$ %s "
        "para US$ %s bilhões). O lado financeiro melhorou US$ %s bilhões &mdash; mas continua negativo "
        "em US$ %s bilhões. <b>O que mudou foi o financeiro parar de sangrar, não o comercial passar a "
        "entregar mais.</b> E o saldo total, mesmo depois da virada, é praticamente zero: o último mês "
        "fechado foi negativo em US$ %s bilhões."
        % (n(fl["cc_saldo_comercial"]["now"] - fl["cc_saldo_comercial"]["y1"], 1),
           n(fl["cc_saldo_comercial"]["y1"], 1), n(fl["cc_saldo_comercial"]["now"], 1),
           n(fl["cc_fin_saldo"]["now"] - fl["cc_fin_saldo"]["y1"], 1),
           n(abs(fl["cc_fin_saldo"]["now"]), 1), n(abs(fl["cc_saldo_total"]["mes"]), 1)))
    st.append(chart_box(fig_fluxo(D)))
    st.append(caption(
        "As barras somam ao saldo total (a linha). O dado é diário e agregado por mês; o mês em "
        "andamento fica de fora para não aparecer pela metade."))
    st.append(Paragraph(
        "Por que dar tanto peso a esta série: entre todas as abordagens de câmbio testadas na literatura, "
        "a que melhor explica o movimento de curto prazo não é nenhuma das teorias de fundamento &mdash; "
        "é o fluxo de ordens de compra e venda em si, que chega a explicar mais da metade da variação "
        "diária. Este é o dado brasileiro mais próximo disso.", BODY))

    # ================================================================== 6
    st += section_header("6", "O Banco Central: reservas e exposição", "Aba Posicionamento")
    rs, sw = D["res"], D["swap"]
    gvol_now = rs["reserves_gold_volume"]["now"] / 1000.0 if rs["reserves_gold_volume"]["now"] else None
    gvol_y1 = rs["reserves_gold_volume"]["y1"] / 1000.0 if rs["reserves_gold_volume"]["y1"] else None
    st += margem(
        "As reservas internacionais estão em <b>US$ %s bilhões</b> (%s), contra US$ %s bilhões doze "
        "meses antes. E o estoque de swap cambial &mdash; o instrumento com que o Banco Central assume "
        "posição vendida em dólar sem gastar reserva &mdash; encolheu de US$ %s para <b>US$ %s bilhões "
        "negativos</b>."
        % (n(rs["reserves_liquidity_daily"]["now"], 1), dmy(D["res_date"]),
           n(rs["reserves_liquidity_daily"]["y1"], 1),
           n(abs(sw["bcb_swap_cambial_position"]["y1"]), 1),
           n(abs(sw["bcb_swap_cambial_position"]["now"]), 1)))
    st.append(Paragraph(
        "<b>O ouro merece uma linha própria, porque a leitura fácil está errada.</b> A posição em ouro "
        "saltou de US$ %s para US$ %s bilhões, uma alta de %s%%. Mas o <i>volume</i> também subiu &mdash; "
        "de %s para %s milhões de onças, %s%%. Ou seja: <b>o Banco Central comprou ouro de verdade</b>, "
        "e não apenas viu o preço do que já tinha subir. Reportar só o valor em dólar misturaria as duas "
        "causas, e elas dizem coisas diferentes sobre a intenção da autoridade."
        % (n(rs["reserves_gold_usd"]["y1"], 1), n(rs["reserves_gold_usd"]["now"], 1),
           n(100 * (rs["reserves_gold_usd"]["now"] / rs["reserves_gold_usd"]["y1"] - 1), 1),
           n(gvol_y1, 3), n(gvol_now, 3), n(100 * (gvol_now / gvol_y1 - 1), 1, sign=True)), BODY))
    st += nivel(
        "O swap continua sendo a maior exposição vendida em dólar do balanço do Banco Central, e reduzi-la "
        "é o que uma autoridade faz quando julga que a pressão passou. Já a intervenção direta no mercado "
        "à vista praticamente desapareceu: nos últimos doze meses somou US$ %s bilhões, contra US$ %s "
        "bilhões nos doze anteriores. O Banco Central saiu de cena porque não precisou estar nela."
        % (n(abs(D["interv"]["bcb_intervention_spot"]["a12m"]), 1),
           n(abs(D["interv"]["bcb_intervention_spot"]["a12m_prev"]), 1)))
    st.append(chart_box(fig_ouro(D)))
    st.append(caption(
        "As três séries estão em múltiplo do próprio valor de janeiro de 2021, que é a única forma de "
        "pôr no mesmo eixo uma coisa que não andou e outra que multiplicou. O tamanho das reservas é "
        "praticamente o mesmo; o ouro dentro delas não. E a linha tracejada &mdash; a quantidade de "
        "onças, que sobe em degraus &mdash; é o que separa compra de remarcação de preço: o que ela "
        "sobe é decisão do Banco Central, e a distância dela para a linha cheia dourada é preço."))
    st.append(chart_box(fig_swap(D)))
    st.append(caption(
        "Valores negativos são posição vendida em dólar. O swap é o instrumento com que o Banco "
        "Central assume essa posição sem gastar reserva; a linha dos bancos é o outro lado do mercado."))
    st += caution(
        "<b>Dia sem registro de intervenção é dia sem intervenção.</b> O processo de carga descarta "
        "linhas com valor zero, então a ausência de um dia na série significa que o Banco Central não "
        "operou, e não que o dado está faltando. A janela de publicação vem da série de reservas "
        "diárias, não da própria série de intervenção.")

    # ================================================================== 7
    st += section_header("7", "Como o mercado está posicionado", "Aba Posicionamento / CFTC")
    ct = D["cot"]
    st += margem(
        "Os gestores de recursos estão comprados em real em <b>%s mil contratos</b> no mercado futuro "
        "americano (dado de %s), contra %s mil três meses antes e %s mil um ano atrás. <b>A aposta "
        "comprada está sendo desmontada enquanto o real se valoriza</b> &mdash; o que diz que o movimento "
        "recente não foi puxado por dinheiro novo apostando na moeda."
        % (n(ct["asset_mgr_net"]["now"] / 1000.0, 1), dmy(D["cot_date"]),
           n(ct["asset_mgr_net"]["m3"] / 1000.0, 1), n(ct["asset_mgr_net"]["y1"] / 1000.0, 1)))
    st += nivel(
        "%s mil contratos ainda é uma posição grande: a série já foi de %s mil negativos a %s mil "
        "positivos. E os fundos alavancados foram no sentido oposto &mdash; de %s mil contratos vendidos "
        "um ano atrás para %s mil comprados hoje. Os dois grupos discordam."
        % (n(ct["asset_mgr_net"]["now"] / 1000.0, 1), n(abs(ct["asset_mgr_net"]["min"]) / 1000.0, 1),
           n(ct["asset_mgr_net"]["max"] / 1000.0, 1), n(abs(ct["lev_net"]["y1"]) / 1000.0, 1),
           n(ct["lev_net"]["now"] / 1000.0, 1)))
    st.append(chart_box(fig_cot(D)))
    st.append(Paragraph(
        "Como ler isso. Posicionamento extremo funciona como sinal contrário: quando todo mundo está do "
        "mesmo lado, falta quem compre para o preço continuar andando, e qualquer notícia na direção "
        "oposta produz um movimento desproporcional ao fundamento. É uma leitura que as casas que "
        "acompanhamos usam explicitamente. A diferença em relação aos casos que elas costumam citar é "
        "que naqueles o mercado estava <b>vendido</b> em real, e o sinal contrário era altista para a "
        "moeda. Hoje é o inverso: o mercado está comprado, e o sinal contrário aponta para o outro lado. "
        "Some-se a isso que a estratégia de ganhar com juro alto em moeda emergente tem retorno positivo "
        "na média mas perde muito e de uma vez quando vira &mdash; a distribuição é torta &mdash; e o "
        "quadro de posicionamento passa a ser um fator de risco, não de suporte.", BODY))
    st += caution(
        "<b>As cinco posições líquidas somam exatamente zero por construção.</b> Para cada comprado há um "
        "vendido, então os grupos não são cinco apostas independentes: são as duas pontas do mesmo "
        "conjunto de contratos, repartidas por tipo de participante.")

    return st


def _story_part2(D):
    st = []
    S, cal = D["scen"], D["cal"]
    probs = S["_probs"]
    ot, ne, pe = S["otimista"], S["neutro"], S["pessimista"]
    sens = D["sens"]
    mres, obs_res, mod_res, res_pct = D["model_resid"]

    # ================================================================== 8
    st += section_header("8", "O que os gestores estão dizendo &mdash; e o que mudou",
                         "Aba FX Attribution")
    at = D["attr_totals"]
    st.append(Paragraph(
        "Este bloco não usa preço. Ele lê as cartas mensais de três gestoras &mdash; Kinea, Verde Asset e "
        "Kapitalo &mdash;, identifica toda vez que uma delas afirma uma causa para o movimento do real, e "
        "pontua cada afirmação de %s1 (motivo forte para o real cair) a %s1 (motivo forte para subir), "
        "dentro de nove categorias fixas. São <b>%d documentos e %d afirmações</b> ao todo. O objetivo "
        "não é saber quem acerta: é ver qual explicação domina o debate em cada momento, e quando ela muda."
        % ("&minus;", "+", at["docs"], at["claims"]), BODY))
    mix = D["attr_mix"]
    st += margem(
        "<b>A explicação dominante trocou de lugar.</b> Comparando os últimos vinte e quatro meses com os "
        "vinte e quatro anteriores, o peso do <b>dólar global</b> no total do que foi dito subiu de %s%% "
        "para <b>%s%%</b>, enquanto o <b>risco fiscal brasileiro</b> caiu de %s%% para <b>%s%%</b>. "
        "Commodities também recuaram, de %s%% para %s%%, e fluxo de capital subiu de %s%% para %s%%."
        % (n(mix["global_usd"][1], 1), n(mix["global_usd"][0], 1),
           n(mix["fiscal_br"][1], 1), n(mix["fiscal_br"][0], 1),
           n(mix["commodities"][1], 1), n(mix["commodities"][0], 1),
           n(mix["capital_flows"][1], 1), n(mix["capital_flows"][0], 1)))

    k, v = D["attr"]["kinea"], D["attr"]["verde_asset"]
    ik_jul, ik_ago = k["months"].index("2026-07"), k["months"].index("2026-08")
    iv_jul, iv_ago = v["months"].index("2026-07"), v["months"].index("2026-08")
    kj, ka = k["monthly"]["global_usd"][ik_jul], k["monthly"]["global_usd"][ik_ago]
    vj, va = v["monthly"]["global_usd"][iv_jul], v["monthly"]["global_usd"][iv_ago]
    st += nivel(
        "E dentro dessa categoria, a mudança marginal mais nítida está no último mês disponível. Em %s "
        "Verde e Kinea marcaram <b>as duas o mesmo sinal</b> (%s e %s) sobre o dólar global. Em %s elas "
        "<b>divergiram</b>: Verde em <b>%s</b> &mdash; o dólar enfraquecendo com a atuação do Tesouro "
        "americano na parte longa da curva, beneficiando outras moedas &mdash; e Kinea em <b>%s</b>, "
        "mantendo viés comprado em dólar diante de um Federal Reserve mais duro. Mesmo mês, mesmo canal, "
        "sinal oposto, e as duas citando a moeda diretamente."
        % (mes("2026-07"), n(vj, 1, sign=True), n(kj, 1, sign=True), mes("2026-08"),
           n(va, 1, sign=True), n(ka, 1, sign=True)))
    st.append(chart_box(fig_attr_mix(D)))
    st.append(caption(
        "Participação de cada causa no total do que foi dito sobre câmbio pelas três gestoras, "
        "comparando os últimos 24 meses com os 24 anteriores. A leitura é de composição, não de "
        "intensidade: o que o gráfico mostra é sobre o que se fala, não quanto se fala."))
    st.append(chart_box(fig_attr_div(D)))
    st.append(caption(
        "Pontuação mensal atribuída ao canal dólar global por cada casa. Positivo é argumento a favor "
        "do real; zero significa que o canal não foi citado naquele mês, e não que ele foi citado como "
        "neutro. Os últimos meses são o ponto: a mesma causa, com sinais opostos."))

    v4 = [(m, v["monthly"]["global_usd"][v["months"].index(m)])
          for m in ("2026-05", "2026-06", "2026-07", "2026-08")]
    ks = D["kapitalo_silence"]
    st.append(Paragraph(
        "Dois detalhes que só aparecem olhando gestor a gestor. <b>A Verde concentrou-se por completo:</b> "
        "as últimas quatro afirmações dela sobre câmbio são todas sobre dólar global (%s), sem uma única "
        "menção a fiscal, política ou commodity. <b>E a Kapitalo está em silêncio:</b> a última afirmação "
        "cambial dela é de %s &mdash; são %d meses e %d cartas sem que a casa ligue nenhuma causa ao "
        "câmbio. Isso é informação, não lacuna de dado: uma gestora macro que escreve todo mês e não fala "
        "da moeda está dizendo que, para ela, a moeda não é onde a decisão está."
        % (", ".join("%s %s" % (mes(m), n(x, 1, sign=True)) for m, x in v4),
           mes(ks["last_claim_month"]), ks["months_silent"], ks["docs_since"]), BODY))
    st.append(Paragraph(
        "<b>Como interpretar a troca de assunto &mdash; e por que ela não prova mudança de regime.</b> A "
        "tentação é concluir que o fiscal deixou de importar. A literatura de câmbio tem uma explicação "
        "alternativa, e ela é mais econômica: quando o câmbio se move de um jeito que o motivo habitual "
        "não explica, o mercado passa a atribuir a explicação a qualquer fundamento que tenha tido um "
        "movimento grande naquele momento &mdash; sem que a relação verdadeira entre fundamentos e preço "
        "tenha mudado. A própria Verde descreve o mesmo fenômeno com outras palavras quando diz que o "
        "mercado brasileiro fica <i>passageiro</i> do exterior: fundamento doméstico define o valor de "
        "médio prazo, condição global define o desvio de curto. A leitura prática, então, é que o fiscal "
        "saiu do noticiário, não da conta &mdash; e isso é exatamente o que torna o cenário pessimista "
        "da seção 10 mais provável do que parece.", BODY))
    st += caution(
        "<b>Zero pode ser silêncio.</b> A pontuação mensal é a <i>soma</i> das afirmações do mês, não a "
        "média. Um mês sem afirmação aparece como zero, igual a um mês em que duas afirmações opostas se "
        "cancelaram. Por isso a contagem de afirmações anda junto do número, e a leitura de variação "
        "mês a mês é feita sobre a série crua, não sobre a média móvel de três meses que o dashboard "
        "mostra.")

    # ================================================================== 9
    st += section_header("9", "O modelo: o que explica o câmbio", "Aba FX Model")
    st.append(Paragraph(
        "O modelo da casa explica a variação mensal do dólar a partir de seis forças. Foi estimado em "
        "%s e explica <b>%s%%</b> do movimento mensal no período inteiro (%s%% na janela mais recente de "
        "seis anos). Ele não é uma previsão: dado um caminho que <i>você</i> fornece para as seis forças, "
        "ele diz que câmbio isso implica. Quem projeta as forças é o analista."
        % (D["sample_txt"], n(100 * D["r2"], 1), n(100 * D["r2_win"], 1)), BODY))

    rows = [["Força", "O que é", "Onde está hoje", "Efeito no dólar"]]
    ch = D["ch_now"]
    rows.append(["Risco Brasil", "Custo de proteger contra calote do país (CDS de 5 anos)",
                 "%s pontos (%s)" % (n(ch["fiscal"]["value"], 0), mes(ch["fiscal"]["month"])),
                 "+100 pontos &rarr; dólar <b>%s%%</b>" % n(sens["cds100"], 1, sign=True)])
    rows.append(["Dólar global", "Força do dólar contra uma cesta de moedas emergentes",
                 "%s (%s)" % (n(ch["dxy_em"]["value"], 1), mes(ch["dxy_em"]["month"])),
                 "+1%% no índice &rarr; dólar <b>%s%%</b>" % n(sens["dxy1pct"], 1, sign=True)])
    rows.append(["Commodities", "Índice de preços de commodities em dólar (IC-Br)",
                 "%s (%s)" % (n(ch["icbr_usd"]["value"], 1), mes(ch["icbr_usd"]["month"])),
                 "&minus;10%% &rarr; dólar <b>%s%%</b>" % n(sens["icbr10dn"], 1, sign=True)])
    rows.append(["Juro por unidade de risco", "Selic menos juro americano, dividido pela volatilidade do câmbio",
                 "%s (%s)" % (n(ch["carry_vol"]["value"], 3), mes(ch["carry_vol"]["month"])),
                 "&minus;0,10 &rarr; dólar <b>%s%%</b>" % n(sens["carry010"], 1, sign=True)])
    rows.append(["Bolsa americana", "S&amp;P 500",
                 "%s (%s)" % (n(ch["sp500"]["value"], 0), mes(ch["sp500"]["month"])),
                 "&minus;10%% &rarr; dólar <b>%s%%</b>" % n(sens["sp10dn"], 1, sign=True)])
    rows.append(["Diferença de inflação", "Inflação brasileira menos americana, acumulada",
                 "%s%% ao ano (Brasil %s%%, EUA %s%%)"
                 % (n(D["dif"]["ipca_12m"]["now"] - D["dif"]["cpi_12m_us"]["now"], 2),
                    n(D["dif"]["ipca_12m"]["now"], 2), n(D["dif"]["cpi_12m_us"]["now"], 2)),
                 "entra com peso fixo de 1"])
    st.append(results_table(rows, col_widths=[85, 150, 105, 130], align_right_from=-1))
    st.append(Spacer(1, 8))

    st.append(Paragraph(
        "<b>Um sinal é ao contrário do que o instinto diz, e ele muda o desenho dos cenários.</b> No "
        "modelo, a bolsa americana caindo 10%% deixa o real <b>%s%% mais forte</b>, não mais fraco. A "
        "leitura por trás disso é de competição por capital: quando o ativo americano fica menos "
        "atraente, parte do dinheiro procura retorno em outro lugar, e mercado emergente com juro alto é "
        "um desses lugares. A consequência prática é direta: <b>um cenário de aversão a risco global não "
        "soma com um cenário de piora do Brasil &mdash; ele compensa parte dele.</b> Quantificamos isso "
        "na seção 10." % n(abs(sens["sp10dn"]), 1), BODY))

    st.append(chart_box(fig_decomp(D)))
    st.append(caption(
        "Contribuição acumulada de cada força para o movimento do dólar ao longo da amostra do modelo. "
        "A diferença de inflação entre Brasil e Estados Unidos é, sozinha, a maior explicação de longo "
        "prazo &mdash; e a parte 'não explicada' é o que sobra depois de todas as seis."))

    se = D["ridge"]["forecast_error_bands"]["std_error_pct"]
    st.append(Paragraph(
        "<b>Três limites que o próprio modelo mede, e que precisam estar na mesa antes dos cenários.</b>",
        BODY))
    st += bullets([
        "<b>A margem de erro é grande e cresce.</b> Medida fora da amostra, é de %s%% em um mês e chega a "
        "<b>%s%% em doze</b>. Aplicada ao câmbio de hoje, doze meses a frente isso é uma faixa de "
        "aproximadamente R$ %s a R$ %s <i>sem nenhum cenário</i>."
        % (n(se[0], 1), n(se[-1], 1), n(D["px"]["last"] * (1 - se[-1] / 100), 2),
           n(D["px"]["last"] * (1 + se[-1] / 100), 2)),

        "<b>As forças se sobrepõem.</b> Cerca de %s%% do poder explicativo é compartilhado entre elas. Só "
        "o risco Brasil e o dólar global têm contribuição própria estatisticamente separável; os demais "
        "coeficientes devem ser lidos em conjunto, não um a um." % n(71, 0),

        "<b>O modelo está hoje pedindo um câmbio mais forte do que o observado.</b> Alimentado com os "
        "valores já realizados das seis forças, ele explica %s como R$ %s, contra os R$ %s de fato "
        "negociados &mdash; um resíduo de <b>%s%%</b>. Está dentro da margem de erro e não é significativo, "
        "mas a direção importa: há um pedaço de prêmio de risco no preço que as seis forças não capturam."
        % (mes(mres), n(mod_res, 2), n(obs_res, 2), n(res_pct, 2, sign=True)),
    ])
    st += caution(
        "<b>Duas datas diferentes.</b> O modelo foi estimado com dados até %s e esse corte está congelado "
        "de propósito, para que a leitura não mude a cada regeração. Os dados dos blocos 1 a 7 vão até "
        "%s. Os três primeiros meses da projeção já aconteceram e entram com os valores realizados; a "
        "projeção propriamente dita começa em %s."
        % (mes(D["ridge"]["months"][-1]), dmy(D["px"]["date"]), mes("2026-10")))
    st.append(PageBreak())

    # ================================================================== 10
    st += section_header("10", "Três cenários a doze meses", "FX Model, com as forças estressadas")

    # --- de onde viemos ----------------------------------------------------
    hd = D["hist_dec"]
    hp = hd["parts"]
    tot_log = 100.0 * math.log(hd["ptax1"] / hd["ptax0"])
    tot_pct = 100.0 * (hd["ptax1"] / hd["ptax0"] - 1.0)
    n_meses = hd["meses"]
    duas = abs(hp["delta_dxy_em"] + hp["delta_fiscal"])
    share_duas = 100.0 * duas / abs(tot_log)
    share_resid = 100.0 * abs(hp["residual"]) / abs(tot_log)

    def _dmeses(a, b):
        return (int(b[:4]) - int(a[:4])) * 12 + (int(b[5:7]) - int(a[5:7]))

    # A janela do MODELO termina no corte do ajuste; a do movimento vai ate o
    # ultimo dado. Sao duas contagens diferentes e o texto usa as duas.
    n_total = _dmeses(hd["base"], hd["pos_corte_mes"] or hd["fim_modelo"])

    st.append(Paragraph("De onde viemos: o movimento desde dezembro de 2024", H2))
    st.append(Paragraph(
        "Projetar sem olhar o caminho já andado é o erro mais comum em cenário de câmbio. O mesmo modelo "
        "que produz as projeções explica o passado, e o que ele diz sobre os últimos %d meses é o que dá "
        "sentido às premissas adiante." % n_total, LEAD))
    st.append(Paragraph(
        "No fim de dezembro de 2024 o dólar fechou em <b>R$ %s</b>. Em %s, último mês do ajuste do "
        "modelo, estava em <b>R$ %s</b> &mdash; uma queda de <b>%s%%</b>. Somando os três meses já "
        "realizados desde então, o dólar de hoje está %s%% abaixo do de dezembro de 2024. Não foi um "
        "evento: foram %d meses de valorização quase contínua. O que a decomposição abaixo abre são os "
        "%d meses que o modelo alcança, de dezembro de 2024 a %s."
        % (n(hd["ptax0"], 2), mes(hd["fim_modelo"]), n(hd["ptax1"], 2), n(abs(tot_pct), 1),
           n(abs(100.0 * ((hd["pos_corte_ptax"] or hd["ptax1"]) / hd["ptax0"] - 1.0)), 1), n_total,
           n_meses, mes(hd["fim_modelo"])), BODY))
    st.append(Paragraph(
        "<b>Duas forças fazem quase todo o trabalho, e são exatamente as duas que os cenários "
        "estressam.</b> O dólar global contra emergentes tirou <b>%s pontos percentuais</b> do preço e o "
        "risco Brasil outros <b>%s</b> &mdash; juntas, %s pontos, ou %s%% do movimento observado. "
        "Commodities e o juro por unidade de volatilidade tiraram %s e %s. Do outro lado, duas forças "
        "empurraram na direção contrária e perderam: a diferença de inflação entre Brasil e Estados "
        "Unidos somou %s pontos e a alta da bolsa americana, %s. O que se vê no preço é a diferença "
        "entre as duas pontas, e é por isso que as parcelas do gráfico abaixo somam mais, em módulo, do "
        "que o total."
        % (n(abs(hp["delta_dxy_em"]), 1), n(abs(hp["delta_fiscal"]), 1), n(duas, 1), n(share_duas, 0),
           n(abs(hp["delta_icbr_usd"]), 1), n(abs(hp["delta_carry_vol"]), 1),
           n(hp["delta_ppp"], 1), n(hp["delta_sp500"], 1)), BODY))
    st.append(Paragraph(
        "<b>E sobram %s pontos que as seis forças não explicam</b> &mdash; o equivalente a %s%% do "
        "movimento observado. Este é o número mais importante desta página: ele diz que o real ficou "
        "mais forte do que os canais "
        "justificam. Não é ruído de medição: é prêmio que apareceu sem uma causa mensurável atrás. "
        "Enquanto dura, um movimento assim se parece com fundamento; a literatura de câmbio é bem clara "
        "sobre o que costuma acontecer com ele depois, e o próprio dado desta página já sugere a "
        "resposta &mdash; foi construído com o mercado comprado em real, e essa posição está sendo "
        "desmontada." % (n(abs(hp["residual"]), 1), n(share_resid, 0)), BODY))
    st.append(chart_box(fig_hist_decomp(D)))
    st.append(caption(
        "Cada barra é quanto aquela força contribuiu para a variação do dólar entre dezembro de 2024 e "
        "%s. Barras à esquerda do zero empurraram o dólar para baixo (real mais forte). A barra "
        "contornada em dourado é o total efetivamente observado, e as oito acima dela somam exatamente "
        "a ele &mdash; é isso que torna a leitura uma decomposição e não uma lista de fatores."
        % mes(hd["fim_modelo"])))

    # --- e para onde vamos -------------------------------------------------
    st.append(Paragraph("Para frente: o que pode mover as mesmas forças", H2))
    st.append(Paragraph(
        "O evento que domina a janela é a <b>eleição de outubro de 2026</b>. Os três cenários se separam "
        "principalmente pelo que acontece com o risco Brasil, e a calibragem de quanto é muito não foi "
        "escolhida: saiu da própria história da série.", BODY))

    st.append(Paragraph("Quanto o risco Brasil costuma andar em doze meses", H2))
    st.append(Paragraph(
        "Em %d janelas de doze meses desde 2001, o multiplicador do CDS ficou abaixo de %sx na metade das "
        "vezes; %sx é o percentil 90 e %sx o percentil 95. Aplicados aos %s pontos de hoje, isso dá %s, "
        "%s e %s pontos. Do outro lado, o piso histórico da série é %s pontos &mdash; ou seja, mesmo o "
        "melhor caso concebível corta pouco mais de um terço do nível atual."
        % (cal["dist_n"], n(cal["p"]["p50"], 2), n(cal["p"]["p90"], 2), n(cal["p"]["p95"], 2),
           n(cal["cds_now"], 0), n(cal["cds_now"] * cal["p"]["p50"], 0),
           n(cal["cds_now"] * cal["p"]["p90"], 0), n(cal["cds_now"] * cal["p"]["p95"], 0),
           n(cal["cds_floor"], 0)), BODY))

    el = cal["eleicoes"]
    er = [["Eleição", "CDS em set do ano eleitoral", "CDS um ano depois", "Multiplicador"]]
    for e in sorted(el, key=lambda z: z["ano"]):
        er.append([str(e["ano"]), n(e["base"], 0), n(e["fim"], 0), n(e["mult"], 2) + "x"])
    er.append(["<b>2026</b>", "<b>%s</b>" % n(cal["cds_now"], 0), "<i>este documento</i>", "&mdash;"])
    st.append(results_table(er, col_widths=[84, 155, 132, 110]))
    st.append(Spacer(1, 6))
    subiu = sum(1 for e in el if e["mult"] > 1)
    st.append(Paragraph(
        "<b>E aqui está o achado que organiza as probabilidades.</b> Em %d das %d eleições anteriores o "
        "risco Brasil <b>caiu</b> nos doze meses seguintes a setembro do ano eleitoral. Mas as duas em "
        "que ele <b>subiu</b> &mdash; %s &mdash; são exatamente as duas que partiram dos níveis mais "
        "baixos. A correlação de ordem entre o nível de partida e o multiplicador seguinte é de "
        "<b>%s</b>: quanto mais baixo o ponto de partida, maior a alta subsequente. Com seis observações "
        "isso não é prova estatística, mas é a única evidência direta disponível &mdash; e <b>os %s "
        "pontos de hoje são a menor base de partida de toda a série</b>, abaixo dos %s de %d."
        % (len(el) - subiu, len(el),
           " e ".join(str(e["ano"]) for e in el if e["mult"] > 1),
           n(cal["rho"], 2), n(cal["cds_now"], 0),
           n(min(e["base"] for e in el), 0),
           [e["ano"] for e in el if e["base"] == min(z["base"] for z in el)][0]), BODY))

    st.append(Paragraph("As premissas de cada cenário", H2))
    hdr = [["", "Otimista", "Neutro", "Pessimista"]]
    def _row(lab, f):
        return [lab, f(ot), f(ne), f(pe)]
    tr = hdr + [
        _row("Risco Brasil (CDS)", lambda r: "%s &rarr; %s pts (%sx)"
             % (n(r["cds0"], 0), n(r["free"]["delta_fiscal"][-1], 0),
                n(r["free"]["delta_fiscal"][-1] / r["cds0"], 2))),
        _row("Dólar global", lambda r: "%s%%" % n(100 * (r["free"]["delta_dxy_em"][-1] / r["dxy0"] - 1), 1, sign=True)),
        _row("Commodities", lambda r: "%s%%" % n(100 * (r["free"]["delta_icbr_usd"][-1] / r["ic0"] - 1), 1, sign=True)),
        _row("Bolsa americana", lambda r: "%s%%" % n(100 * (r["free"]["delta_sp500"][-1] / r["sp0"] - 1), 1, sign=True)),
        _row("Juro por unidade de risco", lambda r: "%s &rarr; %s" % (n(r["cv0"], 2), n(r["free"]["delta_carry_vol"][-1], 2))),
        _row("<b>Dólar em %s</b>" % mes(ne["months"][-1]), lambda r: "<b>R$ %s</b> (%s%%)" % (n(r["fim"], 2), n(r["var_pct"], 1, sign=True))),
        _row("Faixa de erro do modelo", lambda r: "%s a %s" % (n(r["lo"][-1], 2), n(r["hi"][-1], 2))),
        _row("<b>Probabilidade</b>", lambda r: "<b>%d%%</b>" % probs[[k for k, vv in S.items() if vv is r][0]]),
    ]
    st.append(results_table(tr, col_widths=[124, 119, 119, 119]))
    st.append(Spacer(1, 8))
    st.append(chart_box(fig_scen(D)))
    st.append(caption(
        "A linha cheia é o observado. As três tracejadas partem do fechamento de "
        "setembro de 2026 e vão até setembro de 2027. A faixa cinza é a margem de erro do "
        "modelo em torno do cenário neutro &mdash; ela cresce com o horizonte e, no décimo "
        "segundo mês, cobre praticamente a distância entre o cenário otimista e o pessimista. "
        "É a forma honesta de dizer que a separação entre os três cenários está dentro do "
        "erro do próprio modelo: o que distingue um do outro é a premissa, não a precisão."))
    st.append(Spacer(1, 4))

    # --- os tres argumentos ------------------------------------------------
    st.append(Paragraph("Cenário otimista &mdash; R$ %s (%d%%)" % (n(ot["fim"], 2), probs["otimista"]), H2))
    st.append(Paragraph(
        "<b>Premissas.</b> A eleição se resolve sem ruptura e com sinalização de disciplina fiscal; o "
        "risco Brasil sobe pouco no período eleitoral e cai a %s pontos (%sx), acima do piso histórico "
        "mas abaixo de hoje. O Federal Reserve corta juros e o dólar global cede %s%% contra emergentes. "
        "Commodities sustentam o nível atual, subindo %s%%. A Selic cai, mas a volatilidade do câmbio cai "
        "junto, então o retorno por unidade de risco sobe de %s para %s.<br/><br/>"
        "<b>Conclusão.</b> O dólar vai a <b>R$ %s</b> em %s, %s%%. A maior contribuição individual vem do "
        "dólar global (%s pontos percentuais), não do Brasil: o risco país contribui com apenas %s "
        "pontos. Ou seja, <b>mesmo no cenário bom, a valorização do real é principalmente um evento "
        "externo</b> &mdash; e a alta da bolsa americana trabalha contra, tirando %s pontos."
        % (n(ot["free"]["delta_fiscal"][-1], 0), n(ot["free"]["delta_fiscal"][-1] / ot["cds0"], 2),
           n(abs(100 * (ot["free"]["delta_dxy_em"][-1] / ot["dxy0"] - 1)), 1),
           n(100 * (ot["free"]["delta_icbr_usd"][-1] / ot["ic0"] - 1), 1),
           n(ot["cv0"], 3), n(ot["free"]["delta_carry_vol"][-1], 3),
           n(ot["fim"], 2), mes(ot["months"][-1]), n(ot["var_pct"], 1, sign=True),
           n(ot["acc"]["delta_dxy_em"], 1), n(ot["acc"]["delta_fiscal"], 1),
           n(ot["acc"]["delta_sp500"], 1, sign=True)), BODY))

    st.append(Paragraph("Cenário neutro &mdash; R$ %s (%d%%)" % (n(ne["fim"], 2), probs["neutro"]), H2))
    st.append(Paragraph(
        "<b>Premissas.</b> A eleição passa sem surpresa e sem mudança de rumo: o risco Brasil oscila no "
        "período eleitoral e termina em %s pontos, praticamente onde está (%sx). O dólar global fica "
        "parado, commodities ficam paradas, a bolsa americana sobe %s%% (tendência de longo prazo) e a "
        "Selic cai o suficiente para reduzir o retorno por unidade de risco de %s para %s.<br/><br/>"
        "<b>Conclusão.</b> O dólar vai a <b>R$ %s</b>, %s%%. Praticamente todo esse movimento é mecânico: "
        "%s pontos vem da diferença de inflação entre Brasil e Estados Unidos, que corroe a moeda todo "
        "ano, e %s pontos da compressão do juro. <b>Num mundo em que nada acontece, o dólar sobe pouco "
        "mais de %s%% ao ano só pela inflação.</b> Este cenário é o mais próximo do consenso de mercado."
        % (n(ne["free"]["delta_fiscal"][-1], 0), n(ne["free"]["delta_fiscal"][-1] / ne["cds0"], 2),
           n(100 * (ne["free"]["delta_sp500"][-1] / ne["sp0"] - 1), 1),
           n(ne["cv0"], 3), n(ne["free"]["delta_carry_vol"][-1], 3),
           n(ne["fim"], 2), n(ne["var_pct"], 1, sign=True),
           n(ne["acc"]["delta_ppp"], 1), n(ne["acc"]["delta_carry_vol"], 1),
           n(ne["acc"]["delta_ppp"], 0)), BODY))

    st.append(Paragraph("Cenário pessimista &mdash; R$ %s (%d%%)" % (n(pe["fim"], 2), probs["pessimista"]), H2))
    st.append(Paragraph(
        "<b>Premissas.</b> O ruído eleitoral vira reprecificação fiscal: o risco Brasil sobe a um pico de "
        "%s pontos e termina em %s (%sx), o que corresponde ao percentil 90 da própria história da série "
        "&mdash; um evento de um em dez, e ainda assim <b>bem abaixo</b> dos %sx de 2015-16 e dos %sx da "
        "crise de 2008. O dólar global sobe %s%%, commodities caem %s%%, a bolsa americana cai %s%% e a "
        "volatilidade do câmbio dispara, derrubando o retorno por unidade de risco de %s para %s.<br/><br/>"
        "<b>Conclusão.</b> O dólar vai a <b>R$ %s</b>, %s%%. O risco país sozinho contribui com %s pontos "
        "percentuais e o dólar global com %s. <b>E aqui aparece a compensação que a seção 9 anunciou:</b> "
        "a queda da bolsa americana <b>subtrai %s pontos</b> do total. Sem esse efeito o cenário "
        "terminaria perto de R$ %s. Quem monta um cenário de aversão a risco somando tudo na mesma "
        "direção superestima o resultado em cerca de %s%%."
        % (n(max(pe["free"]["delta_fiscal"]), 0), n(pe["free"]["delta_fiscal"][-1], 0),
           n(pe["free"]["delta_fiscal"][-1] / pe["cds0"], 2),
           n(cal["ep_mult"].get("fiscal_2015", 0), 2), n(cal["ep_mult"].get("gfc_2008", 0), 2),
           n(100 * (pe["free"]["delta_dxy_em"][-1] / pe["dxy0"] - 1), 1),
           n(abs(100 * (pe["free"]["delta_icbr_usd"][-1] / pe["ic0"] - 1)), 1),
           n(abs(100 * (pe["free"]["delta_sp500"][-1] / pe["sp0"] - 1)), 1),
           n(pe["cv0"], 3), n(pe["free"]["delta_carry_vol"][-1], 3),
           n(pe["fim"], 2), n(pe["var_pct"], 1, sign=True),
           n(pe["acc"]["delta_fiscal"], 1), n(pe["acc"]["delta_dxy_em"], 1),
           n(abs(pe["acc"]["delta_sp500"]), 1),
           n(pe["fim"] * math.exp(abs(pe["acc"]["delta_sp500"]) / 100.0), 2),
           n(abs(pe["acc"]["delta_sp500"]), 1)), BODY))

    # --- probabilidades ----------------------------------------------------
    st.append(Paragraph("De onde vem cada probabilidade", H2))
    fa, fl = cal["freq_all"], cal["freq_low"]
    pr = [["Faixa do risco Brasil em 12 meses", "Todas as janelas (n=%d)" % cal["n_windows"],
           "Janelas que partiram de nível baixo (n=%d)" % cal["n_low"], "Adotado"]]
    adot = [probs["otimista"], probs["neutro"], probs["pessimista"]]
    nomes = ["Otimista", "Neutro", "Pessimista"]
    for i in range(3):
        pr.append(["%s &mdash; %s" % (nomes[i], fa[i][0]), "%s%%" % n(fa[i][2], 1),
                   "%s%%" % n(fl[i][2], 1), "<b>%d%%</b>" % adot[i]])
    st.append(results_table(pr, col_widths=[150, 110, 130, 78]))
    st.append(Spacer(1, 6))
    st.append(Paragraph(
        "A coluna do meio é a que vale, e a diferença entre as duas primeiras é o argumento inteiro. "
        "Olhando <i>todas</i> as janelas de doze meses, o risco Brasil sobe mais de %sx em %s%% das "
        "vezes. Mas olhando apenas as janelas que <b>partiram de um nível baixo</b> &mdash; o quartil "
        "mais baixo da série, abaixo de %s pontos, faixa em que os %s pontos de hoje se encaixam &mdash; "
        "essa frequência sobe para <b>%s%%</b>. Nível baixo não é conforto: é falta de espaço para "
        "melhorar.<br/><br/>"
        "<b>O ajuste que fizemos, e por que.</b> Tiramos %d pontos percentuais do cenário pessimista e "
        "distribuímos entre os outros dois. Duas razões. Primeira, as janelas da coluna do meio se "
        "sobrepõem &mdash; %d janelas mensais de doze meses contêm muito menos informação independente "
        "do que o número sugere, e elas se concentram em poucos episódios. Segunda, a posição externa "
        "hoje é materialmente mais sólida do que naqueles episódios: reservas em US$ %s bilhões, déficit "
        "coberto %s vezes por investimento direto e termos de troca a %s%% do recorde. Nada disso impede "
        "um choque, mas muda o ponto de partida."
        % (n(1.33, 2), n(fa[2][2], 0), n(cal["q1"], 0), n(cal["cds_now"], 0), n(fl[2][2], 0),
           int(round(fl[2][2] - probs["pessimista"])), cal["n_low"],
           n(D["res"]["reserves_liquidity_daily"]["now"], 0), n(D["cobertura_idp"], 2),
           n(100 * (1 - D["tot"]["last"] / D["tot"]["max"]), 1)), BODY))

    # --- triangulacao ------------------------------------------------------
    st.append(Paragraph("Como isso se compara com o que o mercado publica", H2))
    tri = [["Casa", "Número publicado", "Data", "Racional"]]
    for casa, num, data, rac in PROJECOES:
        tri.append([casa, num, data, rac])
    st.append(results_table(tri, col_widths=[80, 105, 45, 232], align_right_from=-1))
    st.append(Spacer(1, 6))
    st.append(Paragraph(
        "Duas coincidências que valem registrar. <b>O nosso cenário neutro põe o dólar em R$ %s em "
        "dezembro de 2026</b>, contra a mediana de R$ 5,20 do Focus &mdash; uma diferença de %s%%, "
        "praticamente o mesmo número, obtido por caminhos completamente diferentes. E o valor justo de "
        "R$ 4,40 da Verde fica <b>fora</b> até do nosso cenário otimista, cuja faixa de erro começa em "
        "R$ %s: para chegar lá seria preciso um cenário melhor do que o melhor que desenhamos. Vale "
        "lembrar que a própria Verde zerou a posição em real em maio de 2026 &mdash; valor justo e "
        "posição são coisas diferentes."
        % (n(ne["dez26"], 2), n(abs(100 * (ne["dez26"] / 5.20 - 1)), 1), n(ot["lo"][-1], 2)), BODY))
    st += caution(
        "<b>Os números da tabela acima não são nossos e não foram derivados aqui.</b> São transcritos de "
        "um levantamento interno de setembro de 2026 que cruzou as cartas das gestoras com declarações "
        "na imprensa. Nenhuma dessas casas foi lida em fonte primária para as declarações de imprensa.")

    # ================================================================== 11
    st += section_header("11", "Conclusão", "")
    st.append(Paragraph(
        "<b>O que os dados dizem.</b> O Brasil passou por doze meses bons no câmbio e as contas externas "
        "acompanharam, mas as duas coisas têm a mesma origem estreita. O déficit em conta corrente "
        "encolheu de %s%% para %s%% do PIB porque a balança de bens melhorou US$ %s bilhões, e essa "
        "melhora é %s%% commodity vendida para a China. Ao mesmo tempo, a conta de lucros e dividendos ao exterior "
        "subiu para US$ %s bilhões, e o fluxo de dólares contratados, "
        "mesmo depois de uma virada de US$ %s bilhões, mal chega a zero. O que melhorou foi preço de "
        "commodity e dinheiro financeiro que parou de sair &mdash; não a capacidade estrutural do país "
        "de gerar dólares."
        % (n(D["cc_pct_y1"], 2), n(D["cc_pct"], 2),
           n(D["bop12"]["mercadorias_gerais"]["now"] - D["bop12"]["mercadorias_gerais"]["y1"], 1),
           n(100 * D["comex"]["export_basicos"]["var"] / D["comex"]["export_mundo"]["var"], 0),
           n(abs(D["bop12"]["lucros_dividendos"]["now"]), 1),
           n(D["fluxo"]["cc_saldo_total"]["now"] - D["fluxo"]["cc_saldo_total"]["y1"], 1)), BODY))
    st.append(Paragraph(
        "<b>O que o modelo acrescenta.</b> Duas coisas que os dados sozinhos não mostram. A primeira é "
        "que, alimentado com o que de fato aconteceu, o modelo pede um câmbio %s%% mais forte do que o "
        "observado &mdash; há prêmio de risco no preço que as seis forças não explicam, e ele não "
        "desapareceu com a valorização. A segunda é que, num cenário em que absolutamente nada muda, o "
        "dólar ainda sobe cerca de %s%% ao ano só pela diferença de inflação. <b>Estabilidade cambial "
        "não é câmbio parado.</b>"
        % (n(abs(res_pct), 2), n(ne["acc"]["delta_ppp"], 0)), BODY))
    st.append(Paragraph(
        "<b>E de que lado está a assimetria.</b> Do lado da depreciação, e a razão é de nível, não de "
        "diagnóstico. O risco Brasil está em %s pontos, a menor base de partida de qualquer setembro de "
        "ano eleitoral desde que a série existe; o piso histórico é %s. Mesmo o melhor caso concebível "
        "corta pouco mais de um terço. Do outro lado não há teto. Somem-se a isso os dois sinais de "
        "posicionamento &mdash; a aposta comprada em real sendo desmontada (%s mil contratos, contra %s "
        "mil um ano atrás) e o debate migrando do fiscal doméstico para o dólar global, que é "
        "exatamente o padrão que precede uma volta de atenção ao que ficou sem ser resolvido. E some-se "
        "o que a decomposição da seção 10 mostrou: <b>%s%% da valorização desde dezembro de 2024 não tem "
        "causa mensurável atrás dela</b>, e é justamente a parte de um movimento que menos razões tem "
        "para se sustentar. A distribuição fica torta para cima. Daí a probabilidade de %d%% no cenário "
        "pessimista contra %d%% no otimista."
        % (n(cal["cds_now"], 0), n(cal["cds_floor"], 0),
           n(D["cot"]["asset_mgr_net"]["now"] / 1000.0, 1), n(D["cot"]["asset_mgr_net"]["y1"] / 1000.0, 1),
           n(100.0 * abs(D["hist_dec"]["parts"]["residual"])
             / abs(100.0 * math.log(D["hist_dec"]["ptax1"] / D["hist_dec"]["ptax0"])), 0),
           probs["pessimista"], probs["otimista"]), BODY))
    st.append(Paragraph(
        "<b>O que observar para saber que cenário está valendo.</b> Três marcadores, em ordem de "
        "utilidade: o risco Brasil rompendo %s pontos para cima (ponto em que o cenário neutro deixa de "
        "descrever o que está acontecendo) ou %s para baixo; o saldo mensal de câmbio contratado voltando "
        "a ser negativo por três meses seguidos; e a posição comprada dos gestores cruzando zero &mdash; "
        "o momento em que quem sustentava a moeda deixa de sustentar."
        % (n(ne["free"]["delta_fiscal"][-1] * 1.15, 0), n(ot["free"]["delta_fiscal"][-1], 0)), BODY))

    st.append(Spacer(1, 10))
    st.append(rule(color=LINE, thickness=0.8, space_before=2, space_after=6))
    st.append(Paragraph(
        "Fontes: Banco Central do Brasil (balanço de pagamentos, PTAX, câmbio contratado, reservas, "
        "swap e intervenção), Comex Stat/MDIC, BIS (câmbio real efetivo), Funcex via IPEADATA (termos de "
        "troca), CFTC/CME (posicionamento), FRED (dólar contra emergentes e inflação americana), Yahoo "
        "Finance (S&amp;P 500) e Bloomberg (risco Brasil). O bloco 8 usa as cartas mensais de Kinea, "
        "Verde Asset e Kapitalo. Todos os números deste documento foram calculados no momento da geração, "
        "a partir das mesmas funções que alimentam o painel interativo <i>FX Report</i> &mdash; a única "
        "exceção são as projeções de terceiros da seção 10, que são transcritas e estão marcadas como "
        "tais. O dashboard interativo acompanha este documento.", FOOTER))
    return st


def build_story(D):
    return _story_part1(D) + _story_part2(D)


def _footer_canvas(canvas, doc):
    canvas.saveState()
    canvas.setFont("DejaVuSans", 7.5)
    canvas.setFillColor(MUTED)
    canvas.drawString(20 * mm, 12 * mm, "LIS Capital — Panorama Cambial")
    canvas.drawRightString(A4[0] - 20 * mm, 12 * mm, "Página %d" % doc.page)
    canvas.restoreState()


def run(out_path=OUT_PATH, D=None):
    D = D or load_all()
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    doc = SimpleDocTemplate(
        out_path, pagesize=A4,
        leftMargin=20 * mm, rightMargin=20 * mm, topMargin=16 * mm, bottomMargin=18 * mm,
        title="Panorama Cambial — LIS Capital",
        author="LIS Capital",
    )
    doc.build(build_story(D), onFirstPage=_footer_canvas, onLaterPages=_footer_canvas)
    print("Saved %s" % out_path)
    return out_path


if __name__ == "__main__":
    run()
