"""Relatorio em PDF dos dois testes do Modelo Estrutural de 2026-10-30.

Pedido do usuario (coordenacao/C_modelo.md, "Decisoes", resultado dos testes): um
relatorio simples, com graficos, tabelas e boa explicacao, do teste da ancora e do
teste A do hiato, com as alternativas como proximos passos. Leitor: o usuario,
economista; sem jargao de codigo.

Segue o padrao do `FX Outlook` (analytics/brasil/exchange_rate/generate_fx_outlook_pdf.py):
toolkit copiado e nao importado, e nenhum numero digitado em prosa -- tudo sai das
funcoes dos dois experimentos, rodadas na geracao.

    uv run python analytics/brasil/structural_model/experimentos/relatorio_testes_2026-10-30/gerar_pdf.py
"""
from __future__ import annotations

import datetime as _dt
import math
import os
import sys
import tempfile
import warnings
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from matplotlib.ticker import FuncFormatter  # noqa: E402
from PIL import Image as PILImage  # noqa: E402
from reportlab.lib import colors  # noqa: E402
from reportlab.lib.pagesizes import A4  # noqa: E402
from reportlab.lib.styles import ParagraphStyle  # noqa: E402
from reportlab.lib.units import mm  # noqa: E402
from reportlab.pdfbase import pdfmetrics  # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont  # noqa: E402
from reportlab.platypus import (HRFlowable, Image as RLImage, KeepTogether,  # noqa: E402
                                Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle)

warnings.filterwarnings("ignore")
EXP = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(EXP / "ancora_2026-10-30"))
sys.path.insert(0, str(EXP / "hiato_2026-10-30"))
import ancora as A  # noqa: E402
import hiato_a as H  # noqa: E402

OUT_PATH = EXP / "Testes do Modelo Estrutural - ancora e hiato.pdf"

matplotlib.rcParams["mathtext.fontset"] = "dejavusans"
matplotlib.rcParams["text.parse_math"] = False
_ASSET_DIR = tempfile.mkdtemp(prefix="lis_testes_modelo_")

# ---------------------------------------------------------------------------
# Fontes, paleta e estilos -- os do FX Outlook
# ---------------------------------------------------------------------------
_MPL_TTF = os.path.join(matplotlib.get_data_path(), "fonts", "ttf")
for nome, arq in (("DejaVuSans", "DejaVuSans.ttf"), ("DejaVuSans-Bold", "DejaVuSans-Bold.ttf"),
                  ("DejaVuSans-Oblique", "DejaVuSans-Oblique.ttf"),
                  ("DejaVuSans-BoldOblique", "DejaVuSans-BoldOblique.ttf")):
    pdfmetrics.registerFont(TTFont(nome, os.path.join(_MPL_TTF, arq)))
pdfmetrics.registerFontFamily("DejaVuSans", normal="DejaVuSans", bold="DejaVuSans-Bold",
                              italic="DejaVuSans-Oblique", boldItalic="DejaVuSans-BoldOblique")

NAVY = colors.HexColor("#1F2853")
GOLD = colors.HexColor("#BB9B1D")
GREEN = colors.HexColor("#418791")
RED = colors.HexColor("#EA523A")
MUTED = colors.HexColor("#7A88A8")
LINE = colors.HexColor("#D8DCE6")
BG_EQ = colors.HexColor("#F4F5F7")
C_NAVY, C_GOLD, C_GREEN, C_RED = "#1F2853", "#BB9B1D", "#418791", "#EA523A"
C_MUTED, C_GRID = "#7A88A8", "#E4E7EF"
C_PURPLE, C_SAND = "#6B5B95", "#C8842B"

TITLE = ParagraphStyle("Title", fontName="DejaVuSans-Bold", fontSize=20, leading=24, textColor=NAVY, spaceAfter=4)
SUBTITLE = ParagraphStyle("Subtitle", fontName="DejaVuSans", fontSize=11, leading=14, textColor=MUTED, spaceAfter=2)
DATE_BADGE = ParagraphStyle("DateBadge", fontName="DejaVuSans", fontSize=9, leading=11, textColor=MUTED)
H1 = ParagraphStyle("H1", fontName="DejaVuSans-Bold", fontSize=15, leading=19, textColor=NAVY, spaceBefore=6, spaceAfter=2)
H1_TAG = ParagraphStyle("H1Tag", fontName="DejaVuSans", fontSize=9, leading=11, textColor=GOLD, spaceAfter=6)
H2 = ParagraphStyle("H2", fontName="DejaVuSans-Bold", fontSize=10.5, leading=13, textColor=NAVY, spaceBefore=10, spaceAfter=4)
BODY = ParagraphStyle("Body", fontName="DejaVuSans", fontSize=9.3, leading=13.2,
                      textColor=colors.HexColor("#1A1A1A"), spaceAfter=6, alignment=4)
LEAD = ParagraphStyle("Lead", parent=BODY, fontSize=10, leading=14.5, textColor=NAVY)
BULLET = ParagraphStyle("Bullet", parent=BODY, leftIndent=12, bulletIndent=0, spaceAfter=4)
FOOTNOTE = ParagraphStyle("Footnote", parent=BODY, fontSize=7.4, leading=9.7,
                          textColor=colors.HexColor("#6E7688"), spaceAfter=0)
CAP = ParagraphStyle("Cap", fontName="DejaVuSans", fontSize=7.6, leading=9.6, textColor=MUTED,
                     spaceBefore=2, spaceAfter=8, alignment=4)
FOOTER = ParagraphStyle("Footer", fontName="DejaVuSans", fontSize=7.6, leading=10, textColor=MUTED, alignment=1)
_asset_counter = [0]


def n(x, d=1, sign=False):
    if x is None or (isinstance(x, float) and math.isnan(x)):
        return "n/d"
    s = format(float(x), ("+,.%df" % d) if sign else (",.%df" % d))
    return s.replace(",", "@").replace(".", ",").replace("@", ".")


def pct(x, d=0, sign=True):
    return n(100 * x, d, sign) + "%"


def tri(p) -> str:
    """Period('2026Q3') -> '3T26'."""
    return "%dT%s" % (p.quarter, str(p.year)[2:])


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
    t.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 0.6, LINE), ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                           ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                           ("TOPPADDING", (0, 0), (-1, -1), 8), ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                           ("LEFTPADDING", (0, 0), (-1, -1), 8), ("RIGHTPADDING", (0, 0), (-1, -1), 8)]))
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
        data.append([Paragraph(c, bodyr if i >= align_right_from else body) for i, c in enumerate(r)])
    t = Table(data, colWidths=col_widths, repeatRows=1)
    style = [("BACKGROUND", (0, 0), (-1, 0), NAVY), ("GRID", (0, 0), (-1, -1), 0.5, LINE),
             ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
             ("TOPPADDING", (0, 0), (-1, -1), 3.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 3.5),
             ("LEFTPADDING", (0, 0), (-1, -1), 5), ("RIGHTPADDING", (0, 0), (-1, -1), 5)]
    for i in range(2, len(data), 2):
        style.append(("BACKGROUND", (0, i), (-1, i), BG_EQ))
    t.setStyle(TableStyle(style))
    return t


def nota(text, label="Ressalva"):
    return [HRFlowable(width=110, thickness=0.5, color=LINE, spaceBefore=5, spaceAfter=3, hAlign="LEFT"),
            Paragraph("<b>%s.</b> %s" % (label, text), FOOTNOTE), Spacer(1, 5)]


def section_header(number, title_text, subtitle_text):
    head = ("%s. %s" % (number, title_text)) if number else title_text
    return [Paragraph(head, H1), Paragraph(subtitle_text, H1_TAG), rule()]


def bullets(items):
    return [Paragraph("&bull;&nbsp; %s" % b, BULLET) for b in items]


def caption(text):
    return Paragraph(text, CAP)


def _fig(w=6.4, h=3.15):
    fig, ax = plt.subplots(figsize=(w, h), dpi=200)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#C9CEDC")
    ax.spines["bottom"].set_color("#C9CEDC")
    ax.tick_params(labelsize=8, colors="#55607A", length=3)
    ax.grid(axis="y", color=C_GRID, lw=0.6)
    ax.set_axisbelow(True)
    return fig, ax


def _title(ax, t, sub=None):
    ax.set_title(t, fontsize=10.5, color=C_NAVY, loc="left", fontweight="bold", pad=22 if sub else 7)
    if sub:
        ax.text(0, 1.012, sub, transform=ax.transAxes, fontsize=8, color=C_MUTED, va="bottom")


def _legend(ax, ncol=None):
    """Legenda fora do quadro, abaixo -- dentro ela cobre a serie (regra do FX Outlook)."""
    h, l = ax.get_legend_handles_labels()
    if h:
        ax.figure.legend(h, l, loc="upper center", bbox_to_anchor=(0.5, 0.0),
                         ncol=ncol or min(3, len(h)), frameon=False, fontsize=8,
                         handlelength=1.7, columnspacing=1.8, borderaxespad=0)


def _br_fmt(d=1):
    return FuncFormatter(lambda v, _: n(v, d))


def _tri_ticks(ax, periodos, cada=8):
    idx = list(range(0, len(periodos), cada))
    ax.set_xticks(idx)
    ax.set_xticklabels([str(periodos[i].year) for i in idx], fontsize=8)


# ---------------------------------------------------------------------------
# Dados: as funcoes dos dois experimentos, rodadas agora
# ---------------------------------------------------------------------------
def carregar() -> dict:
    D = {}
    # ancora
    df = A.painel()
    comum = A.amostra_comum(df)
    D["comum"] = comum
    est = {}
    for k, v in A.VARIANTES.items():
        d = A.matriz(df, v["k"]).loc[comum]
        cR, _, oR = A.est_R(d)
        cH, rH, oH = A.est_H(d, v["dev"])
        est[k] = {"cR": cR, "cH": cH, "tH": dict(zip(rH, oH.tvalues)),
                  "lp": cR["dI"] / (1 - cR["y1"] - cR["y2"])}
    D["est"] = est
    D["oos_cond"] = A.fora_da_amostra(df, comum)
    D["oos_sim"] = A.fora_da_amostra_segurado(df, comum)
    D["choque"] = {k: A.choque_ntnb(df, est[k]["cR"], est[k]["cH"], v["k"]) for k, v in A.VARIANTES.items()}
    fech = df[df["completo"].astype(bool)]
    D["anc_series"] = pd.DataFrame({
        "selic": fech["selic"],
        "cru": fech["rr_10a"] + fech["meta_12m"],
        "mm4": fech["rr_10a"].rolling(4).mean() + fech["meta_12m"],
        "mm8": fech["rr_10a"].rolling(8).mean() + fech["meta_12m"],
    }).loc[comum[0]:]
    D["bc_ic"] = A.taylor.BCB_IC

    # hiato
    V = H.vintages()
    M = H.mensais()
    nuci_sa = H._nivel_sa(M["nuci"])
    ult = V.columns.max()
    D["V"], D["ult"] = V, ult
    D["rev"] = H.revisao_por_idade(V)
    X = H.insumos(M, ult, nuci_sa)
    y = V[ult][V.index <= ult - H.N_PADRAO]
    D["X"], D["y_tr"] = X, y
    r1, am1 = H.ajustar(y, X[H.ESPECS["S1"]])
    r0, _ = H.ajustar(y, X[H.ESPECS["S0"]])
    rn, _ = H.ajustar(y, X[["nuci"]])
    D["r1"], D["am1"], D["r0"], D["rn"] = r1, am1, r0, rn
    sub = {}
    for nome, (a, b) in {"2004–2014": ("2004Q1", "2014Q4"), "2015–2023": ("2015Q1", "2023Q4")}.items():
        yy = y[(y.index >= pd.Period(a, "Q")) & (y.index <= pd.Period(b, "Q"))]
        sub[nome] = H.ajustar(yy, X[H.ESPECS["S1"]])
    D["sub"] = sub
    # regressao em todo o historico: S1 onde ha PIB, S0 no trimestre sem PIB
    linhas = {}
    for t in X.index:
        row = X.loc[[t]]
        if row[H.ESPECS["S1"]].notna().all(axis=1).iloc[0]:
            linhas[t] = float(H.prever(r1, row[H.ESPECS["S1"]]).iloc[0])
        elif row[H.ESPECS["S0"]].notna().all(axis=1).iloc[0]:
            linhas[t] = float(H.prever(r0, row[H.ESPECS["S0"]]).iloc[0])
    D["reg_hist"] = pd.Series(linhas).sort_index()
    D["so_nuci"] = H.prever(rn, X[["nuci"]].dropna())
    D["prt"] = {(alvo, N): H.pseudo_rt(V, M, nuci_sa, N, alvo)
                for alvo in (False, True) for N in (8, 12)}
    D["desoc_min"] = float(X.reindex(am1.index)["desoc"].min())
    D["desoc_hoje"] = float(X["desoc"].dropna().iloc[-1])
    D["desoc_hoje_tri"] = X["desoc"].dropna().index[-1]
    return D


def _rmse(s, sem_covid=False):
    return A._rmse(s, sem_covid)


def _rel(D, modo, var, eq, h):
    o = D[modo]
    return _rmse(o[var][(eq, h)]) / _rmse(o["0"][(eq, h)]) - 1


def _ganho(P, idades):
    t = P[P.idade.isin(idades)]
    return 1 - t.e_reg.abs().mean() / t.e_bc.abs().mean()


# ---------------------------------------------------------------------------
# Graficos -- um eixo por figura, legenda abaixo
# ---------------------------------------------------------------------------
def fig_ancoras(D):
    s = D["anc_series"]
    fig, ax = _fig()
    x = range(len(s))
    ax.plot(x, s["selic"], color=C_NAVY, lw=1.6, label="Selic (média do trimestre)")
    ax.plot(x, s["cru"], color=C_RED, lw=1.1, label="âncora de hoje: juro real de 10 anos + meta")
    ax.plot(x, s["mm4"], color=C_GOLD, lw=1.4, label="com média de 4 trimestres")
    ax.plot(x, s["mm8"], color=C_GREEN, lw=1.4, ls="--", label="com média de 8 trimestres")
    _tri_ticks(ax, list(s.index), 8)
    ax.yaxis.set_major_formatter(_br_fmt(0))
    ax.set_ylabel("% ao ano", fontsize=8.2, color="#55607A")
    _title(ax, "A Selic e as três âncoras testadas",
           "Trimestral, %s a %s · âncora = juro nominal de equilíbrio da regra e da IS"
           % (tri(s.index[0]), tri(s.index[-1])))
    _legend(ax, ncol=2)
    fig.tight_layout()
    return fig


def fig_oos(D):
    grupos = [("R", 1), ("R", 4), ("R", 8), ("H", 1), ("H", 4), ("H", 8)]
    rot = ["Selic\n1 tri", "Selic\n4 tri", "Selic\n8 tri", "hiato\n1 tri", "hiato\n4 tri", "hiato\n8 tri"]
    var = [("1", "média de 4 trimestres", C_GOLD), ("2", "média de 8 trimestres", C_GREEN),
           ("1b", "média de 4 + desvio na IS", C_SAND), ("2b", "média de 8 + desvio na IS", C_PURPLE)]
    fig, ax = _fig(6.4, 3.3)
    w = 0.2
    for j, (k, nome, cor) in enumerate(var):
        vals = [100 * _rel(D, "oos_sim", k, eq, h) for eq, h in grupos]
        ax.bar(np.arange(6) + (j - 1.5) * w, vals, w, color=cor, label=nome)
    ax.axhline(0, color="#55607A", lw=0.8)
    ax.axhline(5, color=C_RED, lw=0.9, ls=":", label="limite do critério: +5%")
    ax.set_xticks(range(6))
    ax.set_xticklabels(rot, fontsize=8)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: n(v, 0, True) + "%"))
    ax.set_ylabel("erro contra a âncora de hoje", fontsize=8.2, color="#55607A")
    _title(ax, "Erro de previsão de cada variante contra a âncora de hoje",
           "Fora da amostra, %d origens desde 1T16, como o simulador projeta (NTN-B, Focus e meta paradas)"
           % len(D["oos_sim"]["0"][("R", 1)]))
    _legend(ax, ncol=3)
    fig.tight_layout()
    return fig


def fig_choque(D):
    fig, ax = _fig(6.4, 3.0)
    for k, nome, cor, ls in (("0", "âncora de hoje", C_RED, "-"), ("1", "média de 4 trimestres", C_GOLD, "-"),
                             ("2", "média de 8 trimestres", C_GREEN, "--")):
        c = D["choque"][k]
        ax.plot([0] + list(c.index), [0] + list(c["selic"]), color=cor, lw=1.6, ls=ls, marker="o", ms=3,
                label=nome)
    ax.set_xticks(range(0, 13))
    ax.set_xlabel("trimestres depois do salto da NTN-B", fontsize=8.2, color="#55607A")
    ax.yaxis.set_major_formatter(_br_fmt(2))
    ax.set_ylabel("p.p. de Selic", fontsize=8.2, color="#55607A")
    _title(ax, "Quanto a Selic do modelo sobe com 1 p.p. a mais na NTN-B de 10 anos",
           "Diferença contra o cenário sem o salto · Focus e meta paradas · pesos estimados na amostra comum")
    _legend(ax)
    fig.tight_layout()
    return fig


def fig_revisao(D):
    R = D["rev"]
    g = R.groupby("idade")["rev"].apply(lambda s: s.abs().mean()).loc[0:16]
    g2 = R[R.pos2024].groupby("idade")["rev"].apply(lambda s: s.abs().mean()).loc[0:16]
    fig, ax = _fig(6.4, 3.0)
    ax.bar(g.index, g.values, color=C_NAVY, width=0.7, label="todas as edições desde 3T21")
    ax.plot(g2.index, g2.values, color=C_GOLD, lw=1.6, marker="o", ms=3,
            label="só edições desde 3T24 (metodologia atual)")
    ax.axvline(H.N_PADRAO - 0.5, color=C_RED, lw=0.9, ls=":")
    ax.text(H.N_PADRAO - 0.3, ax.get_ylim()[1] * 0.92, "3 anos", fontsize=8, color=C_RED)
    ax.set_xticks(range(0, 17))
    ax.set_xlabel("idade do trimestre na edição (trimestres)", fontsize=8.2, color="#55607A")
    ax.yaxis.set_major_formatter(_br_fmt(1))
    ax.set_ylabel("p.p. do PIB potencial", fontsize=8.2, color="#55607A")
    _title(ax, "Quanto o hiato do BC ainda muda depois de publicado",
           "Distância média entre o valor publicado e o da edição de %s, só trimestres já consolidados"
           % tri(D["ult"]))
    _legend(ax)
    fig.tight_layout()
    return fig


def fig_historico(D):
    V, ult = D["V"], D["ult"]
    bc = V[ult].dropna()
    reg = D["reg_hist"].reindex(bc.index)
    fig, ax = _fig(6.4, 3.3)
    x = np.arange(len(bc))
    corte = list(bc.index).index(ult - H.N_PADRAO)
    ax.axvspan(corte + 0.5, len(bc) - 1, color="#EEF1F7", zorder=0)
    ax.axhline(0, color="#55607A", lw=0.7)
    ax.plot(x, bc.values, color=C_NAVY, lw=1.6, label="hiato do BC, edição de %s" % tri(ult))
    ax.plot(x, reg.values, color=C_GOLD, lw=1.4, label="regressão em NUCI, desocupação, PIB e CAGED")
    sn = D["so_nuci"].reindex(bc.index)
    ax.plot(x[corte + 1:], sn.values[corte + 1:], color=C_GREEN, lw=1.2, ls="--",
            label="regressão só na NUCI (trecho recente)")
    ax.text(corte + 1.5, ax.get_ylim()[0] * 0.85, "fora do treino", fontsize=8, color=C_MUTED)
    _tri_ticks(ax, list(bc.index), 8)
    ax.yaxis.set_major_formatter(_br_fmt(0))
    ax.set_ylabel("% do PIB potencial", fontsize=8.2, color="#55607A")
    _title(ax, "O hiato do BC e o que a regressão diz",
           "Treino: %s a %s (idade de 12 trimestres ou mais) · área sombreada: trimestres que o BC ainda revisa"
           % (tri(D["am1"].index[0]), tri(D["am1"].index[-1])))
    _legend(ax, ncol=2)
    fig.tight_layout()
    return fig


def fig_episodio(D):
    P = D["prt"][(False, 12)]
    p = P[P.idade == 0].sort_values("tri")
    fig, ax = _fig(6.4, 3.0)
    x = np.arange(len(p))
    ax.axhline(0, color="#55607A", lw=0.7)
    ax.plot(x, p["bc"], color=C_RED, lw=1.6, marker="o", ms=3.5, label="primeira publicação do BC")
    ax.plot(x, p["reg"], color=C_GOLD, lw=1.6, marker="o", ms=3.5, label="regressão com o dado da época")
    ax.plot(x, p["final"], color=C_NAVY, lw=1.6, marker="o", ms=3.5, label="valor de hoje (consolidado)")
    ax.set_xticks(x)
    ax.set_xticklabels([tri(t) for t in p["tri"]], fontsize=8)
    ax.yaxis.set_major_formatter(_br_fmt(1))
    ax.set_ylabel("% do PIB potencial", fontsize=8.2, color="#55607A")
    _title(ax, "O hiato do trimestre corrente, na hora e hoje",
           "Cada ponto é o trimestre da própria edição do RPM, de %s a %s"
           % (tri(p["tri"].iloc[0]), tri(p["tri"].iloc[-1])))
    _legend(ax)
    fig.tight_layout()
    return fig


def fig_dispersao(D):
    am = D["am1"]
    X, ult = D["X"], D["ult"]
    fig, ax = _fig(6.4, 3.2)
    ax.scatter(am["desoc"], am["y"], s=12, color=C_NAVY, alpha=0.75, label="trimestres do treino (%s a %s)"
               % (tri(am.index[0]), tri(am.index[-1])))
    rec = [t for t in X.index if t > am.index[-1] and t in D["V"].index and not pd.isna(X.at[t, "desoc"])]
    ax.scatter(X.loc[rec, "desoc"], D["V"].loc[rec, ult], s=22, color=C_RED, marker="D",
               label="%s a %s, hiato publicado" % (tri(rec[0]), tri(rec[-1])))
    ax.axvline(D["desoc_min"], color=C_MUTED, lw=0.9, ls=":")
    ax.text(D["desoc_min"] + 0.1, ax.get_ylim()[0] + 0.3, "menor desocupação do treino: %s%%"
            % n(D["desoc_min"], 2), fontsize=7.6, color=C_MUTED)
    ax.xaxis.set_major_formatter(_br_fmt(0))
    ax.yaxis.set_major_formatter(_br_fmt(0))
    ax.set_xlabel("taxa de desocupação, % (dessazonalizada)", fontsize=8.2, color="#55607A")
    ax.set_ylabel("hiato, % do PIB potencial", fontsize=8.2, color="#55607A")
    _title(ax, "Hiato contra desocupação: hoje fora de qualquer trimestre do treino",
           "Hiato da edição de %s · desocupação retropolada pelo BC" % tri(ult))
    _legend(ax, ncol=2)
    fig.tight_layout()
    return fig


# ---------------------------------------------------------------------------
# Texto
# ---------------------------------------------------------------------------
def story(D):
    st = []
    est, ult = D["est"], D["ult"]
    ic = D["bc_ic"]
    rel = lambda var, eq, h, modo="oos_sim": _rel(D, modo, var, eq, h)  # noqa: E731
    r1 = D["r1"]
    P12 = D["prt"][(False, 12)]
    ganhos = [_ganho(P, [0, 1, 2]) for P in D["prt"].values()]
    caso = P12[(P12.tri >= pd.Period("2022Q4", "Q")) & (P12.tri <= pd.Period("2024Q1", "Q")) & (P12.idade <= 2)]
    acerto_bc = int((np.sign(caso.bc) == np.sign(caso.final)).sum())
    acerto_reg = [int(((np.sign(P[(P.tri >= pd.Period("2022Q4", "Q")) & (P.tri <= pd.Period("2024Q1", "Q"))
                                  & (P.idade <= 2)].reg)) ==
                       np.sign(P[(P.tri >= pd.Period("2022Q4", "Q")) & (P.tri <= pd.Period("2024Q1", "Q"))
                                 & (P.idade <= 2)].final)).sum()) for P in D["prt"].values()]
    hoje = [ult - i for i in range(3, -1, -1)]
    reg_hoje = D["reg_hist"].reindex(hoje)
    bc_hoje = D["V"][ult].reindex(hoje)
    n_oos = len(D["oos_sim"]["0"][("R", 1)])
    sub = D["sub"]

    # capa
    st.append(Paragraph("LIS CAPITAL", ParagraphStyle("brand", fontName="DejaVuSans-Bold", fontSize=10,
                                                      textColor=GOLD, spaceAfter=2)))
    st.append(Paragraph("Modelo Estrutural: dois testes", TITLE))
    st.append(Paragraph("A âncora do juro e o hiato do produto · o que os dados dizem e o que fica para decidir",
                        SUBTITLE))
    st.append(Paragraph("Documento interno &middot; %s &middot; dados até %s"
                        % (_dt.date.today().strftime("%d/%m/%Y"), tri(ult)), DATE_BADGE))
    st.append(rule(color=NAVY, thickness=2, space_before=8, space_after=10))

    # sumario
    st += section_header("", "Sumário", "O que os dois testes concluem")
    st.append(Paragraph(
        "Os dois testes nasceram da mesma queixa dos agentes no ciclo de outubro: o modelo não deixa "
        "o salto da NTN-B apertar a economia, e parte do hiato que ele usa como ponto de partida ainda "
        "vai ser revista pelo Banco Central. O primeiro teste mostra que suavizar a âncora melhora a "
        "Selic, mas não resolve a queixa. O segundo mostra que dá para estimar o hiato recente melhor "
        "que a primeira publicação, mas hoje a resposta depende de uma pergunta que a regressão não "
        "responde: onde está a taxa de desemprego que não acelera a inflação.", LEAD))
    st += bullets([
        "<b>Âncora com média de 4 trimestres:</b> erra a Selic %s menos um trimestre à frente e %s "
        "menos em um ano, e o hiato no máximo %s mais. Passa o critério do jeito que o simulador projeta."
        % (pct(-rel("1", "R", 1), 0, False), pct(-rel("1", "R", 4), 0, False),
           pct(max(rel("1", "H", h) for h in (1, 4, 8)), 1, False)),
        "<b>Nenhuma versão faz a NTN-B apertar o hiato.</b> Em todas, a Selic do modelo acompanha a "
        "âncora e a distância entre as duas, que é o aperto, não muda. A média móvel só atrasa a "
        "passagem: um quarto no trimestre, o resto em um ano.",
        "<b>O desvio da NTN-B contra a própria média, como custo de capital na IS, sai com o sinal "
        "trocado</b> (%s e %s, sem significância). Fica rejeitado nessa forma."
        % (n(est["1b"]["cH"]["dev_l"], 3, True), n(est["2b"]["cH"]["dev_l"], 3, True)),
        "<b>Hiato:</b> uma regressão em NUCI e desocupação explica %s%% do hiato consolidado, acertou "
        "o sinal do episódio 2022–23 que o BC errou (%d ou %d de 12 casos contra %d) e corta entre "
        "%s%% e %s%% do erro dos três trimestres mais recentes. Mas os pesos não são estáveis."
        % (n(100 * r1.rsquared, 0), min(acerto_reg), max(acerto_reg), acerto_bc,
           n(100 * min(ganhos), 0), n(100 * max(ganhos), 0)),
        "<b>Hoje ela dá hiato de %s em %s, contra %s publicado.</b> A diferença vem quase toda do "
        "desemprego de %s%%, abaixo de qualquer trimestre usado para estimar (mínimo de %s%%): é a "
        "pergunta da NAIRU, não um erro de medida."
        % (n(reg_hoje.iloc[-1], 1, True), tri(ult), n(bc_hoje.iloc[-1], 2, True),
           n(D["desoc_hoje"], 1), n(D["desoc_min"], 1)),
    ])

    # 1. ancora
    st += section_header("1", "A âncora da regra de juros e da curva IS",
                         "Juro real de 10 anos cru contra a média móvel")
    st.append(Paragraph("O que se testou", H2))
    st.append(Paragraph(
        "No modelo, a regra de juros persegue um juro nominal de equilíbrio igual ao juro real da "
        "NTN-B de 10 anos mais a meta de inflação, e a curva IS mede o aperto monetário como a "
        "distância entre a Selic e esse mesmo número. As duas equações dividem a âncora, então toda "
        "variante troca as duas juntas. A alternativa ao juro de 10 anos do trimestre é a média dos "
        "últimos 4 ou 8 trimestres, que olha só para trás. Como variante extra, a curva IS recebeu "
        "também o desvio do juro de 10 anos contra a própria média, a leitura possível de "
        "\"prêmio\" sem uma série de juro neutro. Esse termo aninha as duas outras formas: com "
        "peso igual a menos o do aperto, a IS volta a ler o juro cru; com peso zero, lê a média.", BODY))
    st.append(chart_box(fig_ancoras(D)))
    st.append(caption(
        "As três âncoras andam juntas no longo prazo; a média só tira o vaivém de trimestre a "
        "trimestre. Hoje a âncora é %s%% ao ano na forma atual, %s%% com a média de 4 trimestres e "
        "%s%% com a de 8."
        % (n(D["anc_series"]["cru"].iloc[-1], 2), n(D["anc_series"]["mm4"].iloc[-1], 2),
           n(D["anc_series"]["mm8"].iloc[-1], 2))))

    st.append(Paragraph("Os pesos estimados", H2))
    rot_var = {"0": "Juro de 10 anos cru (hoje)", "1": "Média de 4 trimestres", "2": "Média de 8 trimestres",
               "1b": "Média de 4 + desvio na IS", "2b": "Média de 8 + desvio na IS"}
    rows = [["Variante", "Inércia da Selic, 1 tri", "Inércia da Selic, 2 tri", "Inflação esperada, longo prazo",
             "Aperto sobre o hiato (t)", "Desvio sobre o hiato (t)"]]
    for k in A.VARIANTES:
        e = est[k]
        rows.append([rot_var[k], n(e["cR"]["y1"], 3), n(e["cR"]["y2"], 3), n(e["lp"], 2),
                     "%s (%s)" % (n(e["cH"]["ap_l"], 3), n(e["tH"]["ap_l"], 1)),
                     "%s (%s)" % (n(e["cH"]["dev_l"], 3, True), n(e["tH"]["dev_l"], 1)) if "dev_l" in e["cH"]
                     else "—"])
    rows.append(["Intervalo publicado pelo BC", "%s a %s" % (n(ic["t1"][0], 2), n(ic["t1"][1], 2)),
                 "%s a %s" % (n(ic["t2"][0], 2), n(ic["t2"][1], 2)),
                 "%s a %s" % (n(ic["t3"][0], 2), n(ic["t3"][1], 2)), "—", "—"])
    st.append(results_table(rows, [118, 62, 62, 72, 82, 85]))
    st.append(caption(
        "Mínimos quadrados, amostra comum de %s a %s (%d trimestres), erro-padrão robusto a "
        "autocorrelação. O efeito do aperto sobre o hiato é praticamente o mesmo em todas as formas. "
        "Com a média de 4 trimestres, a segunda defasagem da Selic fica levemente fora do intervalo "
        "do BC; o efeito de longo prazo fica dentro em todas."
        % (tri(D["comum"][0]), tri(D["comum"][-1]), len(D["comum"]))))

    st.append(Paragraph("Fora da amostra", H2))
    st.append(Paragraph(
        "O teste decisivo é a previsão. Estimei as duas equações só com o dado até cada trimestre "
        "desde 2016 (%d origens) e projetei Selic e hiato 1, 4 e 8 trimestres à frente. Há duas "
        "maneiras de fazer isso, e elas discordam. Na primeira, como o simulador roda, a NTN-B, a "
        "Focus e a meta ficam paradas no valor da origem, a Selic sai da regra e o hiato lê essa "
        "Selic. Na segunda, cada equação recebe o caminho que de fato aconteceu."
        % n_oos, BODY))
    st.append(chart_box(fig_oos(D)))
    rows = [["Variante", "Selic 1 tri", "Selic 4 tri", "Selic 8 tri", "Hiato 1 tri", "Hiato 4 tri",
             "Hiato 8 tri"]]
    for modo, rot_modo in (("oos_sim", "como o simulador"), ("oos_cond", "com a NTN-B realizada")):
        for k in ("1", "2"):
            rows.append(["%s, %s" % (rot_var[k], rot_modo)] +
                         [pct(rel(k, eq, h, modo), 1) for eq in ("R", "H") for h in (1, 4, 8)])
    st.append(results_table(rows, [150, 55, 55, 55, 55, 55, 55]))
    st.append(caption(
        "Variação do erro quadrático médio contra a âncora de hoje; negativo é melhor. O critério "
        "combinado: nenhuma das duas equações pior que +5%% e pelo menos uma melhor. A média de 4 "
        "trimestres passa na leitura do simulador e falha na outra; a de 8 falha por pouco nas duas."))
    st.append(Paragraph(
        "A vantagem do juro cru na segunda leitura existe só para quem conhece a NTN-B que de fato "
        "aconteceu, e o mercado forma essa taxa olhando a própria Selic: a correlação entre a âncora "
        "e o aperto é alta. Projetando, ninguém tem esse caminho. Por isso a leitura que vale para o "
        "uso do modelo é a primeira, e nela a média de 4 trimestres melhora a Selic em todos os "
        "horizontes sem piorar o hiato além do limite.", BODY))

    st.append(KeepTogether([Paragraph("O salto da NTN-B", H2), chart_box(fig_choque(D))]))
    c1b, c2b = D["choque"]["1b"], D["choque"]["2b"]
    st.append(Paragraph(
        "Este é o resultado que importa para a queixa dos agentes. Com 1 p.p. permanente a mais na "
        "NTN-B, a Selic do modelo sobe 1 p.p. no mesmo trimestre na âncora de hoje, e em um ou dois "
        "anos nas médias. <b>O hiato não se mexe em nenhuma das três</b>, porque a Selic e a âncora "
        "sobem juntas e o aperto, que é a distância entre elas, não muda. Com o desvio na IS o hiato "
        "chega a subir (%s p.p. em quatro trimestres com a média de 4, %s com a de 8): o sinal é o "
        "oposto do de custo de capital, e o coeficiente não é significativo."
        % (n(c1b.loc[4, "hiato"], 2, True), n(c2b.loc[4, "hiato"], 2, True)), BODY))
    st.append(Paragraph(
        "<b>Leitura do teste.</b> A média de 4 trimestres é uma melhora modesta e real: a NTN-B "
        "passa para a Selic aos poucos, o que tira do modelo a reação de um trimestre a um pregão. "
        "Ela não faz a NTN-B apertar a economia. Para isso a IS precisa de um juro neutro separado "
        "do prêmio, e essa série não existe no modelo hoje. É o primeiro próximo passo da seção 3.",
        BODY))

    # 2. hiato
    st += section_header("2", "O hiato do produto: teste A",
                         "Estimar hoje o hiato que o Banco Central vai publicar daqui a três anos")
    st.append(Paragraph("O problema", H2))
    st.append(Paragraph(
        "O hiato do BC é estimado, não medido, e cada Relatório de Política Monetária reescreve os "
        "trimestres recentes. O modelo parte do hiato da edição mais nova, que é justamente a parte "
        "menos firme. A ideia do teste é estimar o hiato nos trimestres antigos, em que o BC já quase "
        "não mexe, contra os mesmos indicadores que ele usa (PIB, CAGED, desocupação e NUCI), e "
        "aplicar a regressão aos trimestres recentes. Os indicadores entram de forma que só olha para "
        "trás, porque o filtro que o BC usa no PIB e no CAGED olha para os dois lados e tem o mesmo "
        "problema de fim de amostra que se quer evitar.", BODY))
    st.append(chart_box(fig_revisao(D)))
    g = D["rev"].groupby("idade")["rev"].apply(lambda s: s.abs().mean())
    st.append(caption(
        "Em média o trimestre corrente é revisto em %s p.p., e com 12 trimestres de idade ainda em "
        "%s. A barra inclui a troca de metodologia do BC em 2024, que reescreveu a série inteira; nas "
        "edições da metodologia atual, a revisão cai abaixo de 0,1 p.p. depois de uns dois anos. "
        "Os três anos de corte do treino são, portanto, conservadores."
        % (n(g.loc[0], 2), n(g.loc[12], 2))))

    st.append(Paragraph("O ajuste", H2))
    rows = [["Indicador", "Peso", "Estatística t", "2004–2014", "2015–2023"]]
    nomes = {"const": "Constante", "nuci": "NUCI (p.p.)", "desoc": "Desocupação (p.p.)",
             "pib": "Ciclo do PIB (%)", "caged": "Ciclo do CAGED (%)"}
    for c in r1.params.index:
        rows.append([nomes[c], n(r1.params[c], 3), n(r1.tvalues[c], 1),
                     n(sub["2004–2014"][0].params[c], 3), n(sub["2015–2023"][0].params[c], 3)])
    rows.append(["Ajuste (R²)", n(r1.rsquared, 3), "", n(sub["2004–2014"][0].rsquared, 3),
                 n(sub["2015–2023"][0].rsquared, 3)])
    st.append(results_table(rows, [150, 70, 70, 90, 90]))
    st.append(caption(
        "Hiato da edição de %s contra os quatro indicadores, de %s a %s. Ciclo do PIB e do CAGED pelo "
        "método de Hamilton (o erro de prever o nível com o de dois anos antes), que não usa dado futuro."
        % (tri(ult), tri(D["am1"].index[0]), tri(D["am1"].index[-1]))))
    st.append(Paragraph(
        "Quem explica o hiato são a NUCI e a desocupação. Dadas as duas, PIB e CAGED não acrescentam "
        "nada, e o do CAGED sai até com o sinal trocado. O ajuste é bom, mas os pesos não são estáveis: "
        "da primeira para a segunda metade da amostra, NUCI e desocupação passam a pesar a metade. O "
        "mesmo hiato hoje corresponde a mais ociosidade medida do que antes.", BODY))
    st.append(chart_box(fig_historico(D)))
    st.append(caption(
        "A regressão acompanha o BC no trecho de treino e até 2024. A partir de 2025 os dois se separam: "
        "o BC vê o hiato fechando, a regressão o vê aberto em torno de 1,5. Só com a NUCI, a regressão "
        "volta para perto do número do BC."))

    st.append(Paragraph("Contra a primeira publicação", H2))
    st.append(Paragraph(
        "Para saber se a regressão teria ajudado na época, refiz o exercício em cada edição desde o "
        "terceiro trimestre de 2021, só com o que aquela edição sabia: estimei a regressão nos "
        "trimestres velhos dela e estimei os recentes. As duas estimativas, a do BC e a da regressão, "
        "foram comparadas ao valor de hoje, só onde ele já está consolidado. Sobram nove edições e um "
        "episódio.", BODY))
    t = P12.groupby("idade").agg(nn=("e_bc", "size"), bc=("e_bc", lambda s: s.abs().mean()),
                                 reg=("e_reg", lambda s: s.abs().mean()))
    rows = [["Idade do trimestre", "Casos", "Erro do BC (p.p.)", "Erro da regressão (p.p.)", "Redução"]]
    for i in range(0, 8):
        rows.append([str(i), str(int(t.loc[i, "nn"])), n(t.loc[i, "bc"], 2), n(t.loc[i, "reg"], 2),
                     pct(1 - t.loc[i, "reg"] / t.loc[i, "bc"], 0)])
    st.append(results_table(rows, [100, 60, 100, 120, 80]))
    st.append(caption(
        "Distância média até o valor de hoje. Treino na própria edição, corte de três anos. Com corte "
        "de dois anos, ou com o treino na metodologia atual do BC, a redução média nos três trimestres "
        "mais recentes vai de %s%% a %s%%. Do sexto trimestre em diante a regressão erra mais que o BC."
        % (n(100 * min(ganhos), 0), n(100 * max(ganhos), 0))))
    st.append(chart_box(fig_episodio(D)))
    st.append(Paragraph(
        "O gráfico mostra o episódio inteiro. Do fim de 2022 ao terceiro trimestre de 2023, o último "
        "que já dá para dar como consolidado, o BC publicou hiato negativo trimestre após trimestre, e "
        "hoje todos esses trimestres são positivos. Com o dado da época, a regressão já dizia positivo "
        "na maior parte deles: nos quatro trimestres, lidos na edição em que saíram e nas duas "
        "seguintes, acertou o sinal em %d a %d de 12 casos, contra %d do BC. Em 2021, logo depois da "
        "pandemia, foi o contrário: a regressão errou mais que o BC. É o resultado mais forte do teste, "
        "e também a sua fraqueza: a avaliação inteira cabe em um episódio, em que o BC errou sempre "
        "para o mesmo lado."
        % (min(acerto_reg), max(acerto_reg), acerto_bc), BODY))

    st.append(Paragraph("O hiato de hoje", H2))
    rows = [["", *[tri(t) for t in hoje]],
            ["Publicado pelo BC (%s)" % tri(ult), *[n(v, 2, True) for v in bc_hoje]],
            ["Regressão com os quatro indicadores", *[n(v, 2, True) for v in reg_hoje]],
            ["Regressão só na NUCI", *[n(v, 2, True) for v in D["so_nuci"].reindex(hoje)]]]
    st.append(results_table(rows, [190, 70, 70, 70, 70]))
    st.append(chart_box(fig_dispersao(D)))
    st.append(Paragraph(
        "A regressão vê hoje uma economia bem mais aquecida que o BC, e a razão é uma só. A "
        "desocupação de %s%% em %s está abaixo de todos os trimestres usados para estimar; o menor foi "
        "%s%%. A regressão supõe que a relação entre desemprego e hiato de 2004 a 2023 vale hoje, ou "
        "seja, que a taxa de desemprego compatível com inflação estável não mudou. O BC, ao que tudo "
        "indica, supõe que ela caiu. A regressão não tem como arbitrar isso, e a diferença de cerca de "
        "1 p.p. entre os dois números é exatamente o tamanho dessa pergunta."
        % (n(D["desoc_hoje"], 1), tri(D["desoc_hoje_tri"]), n(D["desoc_min"], 2)), BODY))
    st.append(Paragraph(
        "<b>Leitura do teste.</b> Passou em dois dos três critérios combinados: acertou o episódio de "
        "2022–23 e reduziu o erro recente na fronteira dos 30%, mas os pesos não são estáveis. Como "
        "correção do hiato do BC nos últimos trimestres ela tem valor; como resposta para hoje, não, "
        "enquanto a pergunta do desemprego estiver aberta. Para o agente de mercado de trabalho isso "
        "muda o papel: a tese dele sobre essa taxa passa a ser o insumo que mais move o ponto de "
        "partida do hiato, se alguma versão deste teste entrar no modelo.", BODY))
    st += nota(
        "Não há vintages dos indicadores no banco: a NUCI, o PIB e o CAGED usados são os de hoje, só "
        "cortados na data de cada edição. As revisões do PIB, menores que as do hiato, ficam dentro "
        "do exercício. A NUCI vem da FGV via IPEADATA e ainda não tem tabela própria no banco.")

    # 3. proximos passos
    st += section_header("3", "Próximos passos", "As duas alternativas, nenhuma rodada ainda")
    st.append(Paragraph("Um juro neutro pela Focus, com o prêmio na curva IS", H2))
    st.append(Paragraph(
        "<b>O que testaria.</b> Se o salto da NTN-B aperta a economia quando o modelo separa o juro "
        "neutro do prêmio de prazo. O neutro viria do juro real que a Focus espera para daqui a quatro "
        "ou cinco anos (Selic esperada menos IPCA esperado no mesmo ano), série que existe desde antes "
        "de 2006. O prêmio seria a NTN-B de 10 anos menos esse neutro. A regra de juros e a IS passam a "
        "perseguir o neutro, e a IS recebe o prêmio como custo de capital. As leituras do QPC sobre o "
        "juro neutro, dez desde 2021, servem de conferência do nível.", BODY))
    st.append(Paragraph(
        "<b>Critério.</b> O mesmo deste documento, mais o que motivou o teste: o prêmio precisa "
        "entrar na IS com peso negativo e significativo, de modo que 1 p.p. a mais na NTN-B, "
        "mantido o neutro, abra o hiato para baixo. <b>Custo:</b> cerca de 250 mil tokens, com a série "
        "do neutro feita por um subagente e conferida contra o QPC.", BODY))
    st.append(Paragraph("A taxa de desemprego de equilíbrio que anda no tempo", H2))
    st.append(Paragraph(
        "<b>O que testaria.</b> Se a regressão do hiato continua acertando os trimestres recentes "
        "quando a desocupação entra como distância até uma tendência lenta, em vez do nível. Se a "
        "taxa de equilíbrio caiu, a regressão nova deve trazer o hiato de hoje para perto do número "
        "do BC; se não, mantém o hiato alto e reforça a leitura de economia aquecida. As três leituras "
        "de taxa de desemprego de equilíbrio do QPC, desde 2025, servem de conferência.", BODY))
    st.append(Paragraph(
        "<b>Critério.</b> Os três de antes, com o de estabilidade dos pesos como o que precisa "
        "melhorar. <b>Custo:</b> cerca de 100 mil tokens, feito por mim.", BODY))

    st.append(Paragraph("As três decisões em aberto", H2))
    st += bullets([
        "<b>A. A âncora.</b> Adotar a média de 4 trimestres na regra de juros e na IS, ou manter o juro "
        "de 10 anos do trimestre. A recomendação é adotar: melhora a Selic, não piora o hiato e tira do "
        "modelo a reação imediata a um pregão.",
        "<b>B. O hiato.</b> Refazer a regressão com a taxa de equilíbrio andando no tempo antes de "
        "decidir; usar a regressão só como cenário de hiato alto para os agentes; ou manter o hiato "
        "do BC. A recomendação é refazer.",
        "<b>C. O neutro.</b> Construir o neutro pela Focus agora, ou depois de A e B. A recomendação é "
        "depois, porque ele muda as duas equações de novo.",
    ])
    st.append(Spacer(1, 10))
    st.append(rule(color=LINE, thickness=0.8, space_before=2, space_after=6))
    st.append(Paragraph(
        "Fontes: Banco Central do Brasil (hiato do produto e suas edições no anexo do RPM, Selic, "
        "desocupação retropolada, estoque do CAGED, Focus), B3 (NTN-B de 10 anos), IBGE (PIB "
        "dessazonalizado) e FGV via IPEADATA (NUCI da indústria de transformação). Todos os números "
        "foram calculados no momento da geração.", FOOTER))
    return st


def _rodape(canvas, doc):
    canvas.saveState()
    canvas.setFont("DejaVuSans", 7.5)
    canvas.setFillColor(MUTED)
    canvas.drawString(20 * mm, 12 * mm, "LIS Capital — Modelo Estrutural")
    canvas.drawRightString(A4[0] - 20 * mm, 12 * mm, "Página %d" % doc.page)
    canvas.restoreState()


def run(out_path=OUT_PATH, D=None):
    D = D or carregar()
    doc = SimpleDocTemplate(str(out_path), pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm,
                            topMargin=16 * mm, bottomMargin=18 * mm,
                            title="Modelo Estrutural: dois testes — LIS Capital", author="LIS Capital")
    doc.build(story(D), onFirstPage=_rodape, onLaterPages=_rodape)
    print("Saved %s" % out_path)
    return out_path


if __name__ == "__main__":
    run()
