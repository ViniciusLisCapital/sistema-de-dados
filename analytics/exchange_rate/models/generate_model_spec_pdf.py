"""Gera o PDF de especificação/metodologia/resultados dos modelos de PPP USD/BRL.

Documento complementar ao `ppp_dashboard.html` (mesma pasta de modelos) — não lê
dados do MySQL nem reajusta nenhum modelo; apenas escreve, em texto fixo, o que
já está fixado (e verificado) em `analytics/exchange_rate/CLAUDE.md`. Se algum
modelo for refeito/reespecificado, atualizar este arquivo manualmente junto do
CLAUDE.md, na mesma sessão.
"""

import os
import tempfile

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
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
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

# Equations render through matplotlib's mathtext (proper fractions, subscripts,
# Greek letters) rather than monospace text — a flat "β_carry·z(...)" line
# reads like source code, not a typeset equation. "dejavusans" keeps the
# equation glyphs visually consistent with the rest of the document's font.
matplotlib.rcParams["mathtext.fontset"] = "dejavusans"
_EQ_DIR = tempfile.mkdtemp(prefix="lis_ppp_eq_")

# ---------------------------------------------------------------------------
# Fonts — DejaVu Sans (bundled with matplotlib, already a project dependency)
# is used instead of the base-14 PDF fonts because it has full Unicode
# coverage (Greek letters, arrows, superscripts) that Helvetica/Courier lack.
# ---------------------------------------------------------------------------
_MPL_TTF = os.path.join(matplotlib.get_data_path(), "fonts", "ttf")
pdfmetrics.registerFont(TTFont("DejaVuSans", os.path.join(_MPL_TTF, "DejaVuSans.ttf")))
pdfmetrics.registerFont(TTFont("DejaVuSans-Bold", os.path.join(_MPL_TTF, "DejaVuSans-Bold.ttf")))
pdfmetrics.registerFont(TTFont("DejaVuSans-Oblique", os.path.join(_MPL_TTF, "DejaVuSans-Oblique.ttf")))
pdfmetrics.registerFont(TTFont("DejaVuSans-BoldOblique", os.path.join(_MPL_TTF, "DejaVuSans-BoldOblique.ttf")))
# Without this, inline <b>/<i> markup inside Paragraph text silently fails to
# switch to the bold/oblique TTFs (confirmed via pdfplumber char-level color/
# font inspection: the color changed but the font stayed regular-weight).
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

OUT_PATH = os.path.join("reports", "ppp_model_specs.pdf")

# ---------------------------------------------------------------------------
# Paragraph styles
# ---------------------------------------------------------------------------
TITLE = ParagraphStyle("Title", fontName="DejaVuSans-Bold", fontSize=20, leading=24, textColor=NAVY, spaceAfter=4)
SUBTITLE = ParagraphStyle("Subtitle", fontName="DejaVuSans", fontSize=11, leading=14, textColor=MUTED, spaceAfter=2)
DATE_BADGE = ParagraphStyle("DateBadge", fontName="DejaVuSans", fontSize=9, leading=11, textColor=MUTED)

H1 = ParagraphStyle("H1", fontName="DejaVuSans-Bold", fontSize=15, leading=19, textColor=NAVY, spaceBefore=6, spaceAfter=2)
H1_TAG = ParagraphStyle("H1Tag", fontName="DejaVuSans", fontSize=9, leading=11, textColor=GOLD, spaceAfter=6)
H2 = ParagraphStyle("H2", fontName="DejaVuSans-Bold", fontSize=10.5, leading=13, textColor=NAVY, spaceBefore=10, spaceAfter=4)

BODY = ParagraphStyle("Body", fontName="DejaVuSans", fontSize=9.3, leading=13.2, textColor=colors.HexColor("#1A1A1A"), spaceAfter=6, alignment=4)
BODY_TIGHT = ParagraphStyle("BodyTight", parent=BODY, spaceAfter=3)
BULLET = ParagraphStyle("Bullet", parent=BODY, leftIndent=12, bulletIndent=0, spaceAfter=3)

CAUTION_LABEL = ParagraphStyle("CautionLabel", fontName="DejaVuSans-Bold", fontSize=8.8, leading=12, textColor=RED, spaceAfter=2)
CAUTION_BODY = ParagraphStyle("CautionBody", parent=BODY, fontSize=8.8, leading=12.5, textColor=colors.HexColor("#3A2020"))

REF_LABEL = ParagraphStyle("RefLabel", fontName="DejaVuSans-Bold", fontSize=8.6, leading=11, textColor=GOLD)
REF_BODY = ParagraphStyle("RefBody", fontName="DejaVuSans-Oblique", fontSize=8.6, leading=11.5, textColor=MUTED)

FOOTER = ParagraphStyle("Footer", fontName="DejaVuSans", fontSize=7.6, leading=10, textColor=MUTED, alignment=1)


_eq_counter = [0]


def _render_equation_png(mathtext_lines, fontsize=14, color="#1F2853"):
    """Rasterize one or more mathtext lines (each WITHOUT the $ delimiters —
    added here) to a transparent PNG via matplotlib, so equations get real
    typeset fractions/subscripts/Greek letters instead of a monospace
    "β_carry·z(...)" line that reads like source code, not mathematics."""
    text = "\n".join(f"${line}$" for line in mathtext_lines)
    _eq_counter[0] += 1
    path = os.path.join(_EQ_DIR, f"eq_{_eq_counter[0]}.png")
    fig = plt.figure(figsize=(0.1, 0.1))
    fig.text(0, 0, text, fontsize=fontsize, color=color, linespacing=2.0)
    fig.savefig(path, dpi=300, transparent=True, bbox_inches="tight", pad_inches=0.09)
    plt.close(fig)
    return path


def equation_box(mathtext_lines, fontsize=14, max_width=420, box_width=440):
    """A padded, shaded, bordered block holding a typeset equation image —
    built as a single-cell Table (not a bordered Paragraph style), since
    ReportLab's Paragraph border/background support under-reports its own
    height for wrapped multi-line content and visibly overlaps the flowable
    drawn just before it."""
    path = _render_equation_png(mathtext_lines, fontsize=fontsize, color="#1F2853")
    with PILImage.open(path) as im:
        px_w, px_h = im.size
    dpi = 300
    nat_w, nat_h = px_w / dpi * 72, px_h / dpi * 72
    scale = min(1.0, max_width / nat_w)
    img = RLImage(path, width=nat_w * scale, height=nat_h * scale)
    t = Table([[img]], colWidths=[box_width])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), BG_EQ),
        ("BOX", (0, 0), (-1, -1), 0.6, LINE),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 12),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
    ]))
    return t


def rule(color=GOLD, thickness=1.4, space_before=2, space_after=8):
    return HRFlowable(width="100%", thickness=thickness, color=color, spaceBefore=space_before, spaceAfter=space_after)


def results_table(rows, col_widths=None):
    """rows[0] is the header. Cell strings may contain simple <b>/<i> markup."""
    data = [[Paragraph(c, ParagraphStyle("th", fontName="DejaVuSans-Bold", fontSize=8.4, leading=10.5, textColor=colors.white)) for c in rows[0]]]
    body_style = ParagraphStyle("td", fontName="DejaVuSans", fontSize=8.4, leading=11)
    for r in rows[1:]:
        data.append([Paragraph(c, body_style) for c in r])
    t = Table(data, colWidths=col_widths, repeatRows=1)
    style = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("GRID", (0, 0), (-1, -1), 0.5, LINE),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style.append(("BACKGROUND", (0, i), (-1, i), BG_EQ))
    t.setStyle(TableStyle(style))
    return t


def caution(text):
    return [
        Paragraph("Ressalva", CAUTION_LABEL),
        Paragraph(text, CAUTION_BODY),
        Spacer(1, 4),
    ]


def reference(text):
    return Paragraph(f'<font name="DejaVuSans-Bold" color="#BB9B1D">Referência no dashboard —</font> <i>{text}</i>', REF_BODY)


def section_header(number, title_text, subtitle_text):
    return [
        Paragraph(f"{number}. {title_text}", H1),
        Paragraph(subtitle_text, H1_TAG),
        rule(),
    ]


# ---------------------------------------------------------------------------
# Document body
# ---------------------------------------------------------------------------

def build_story():
    story = []

    # --- Cover / intro -----------------------------------------------------
    story.append(Paragraph("LIS CAPITAL", ParagraphStyle("brand", fontName="DejaVuSans-Bold", fontSize=10, textColor=GOLD, spaceAfter=2)))
    story.append(Paragraph("Modelos de Equilíbrio Cambial USD/BRL", TITLE))
    story.append(Paragraph("Especificação, metodologia e resultados — companion do dashboard <i>ppp_dashboard.html</i>", SUBTITLE))
    story.append(Paragraph("Documento interno · Julho de 2026", DATE_BADGE))
    story.append(rule(color=NAVY, thickness=2, space_before=8, space_after=10))

    story.append(Paragraph(
        "Este documento descreve os seis modelos/construções que compõem o dashboard de paridade do poder de "
        "compra (PPP) USD/BRL: a construção do equilíbrio e dos canais candidatos (Seção 1), quatro especificações "
        "estatísticas que testam esses canais contra o desvio observado em relação à PPP (Seções 2–5), e um teste "
        "de estabilidade temporal dos parâmetros (Seção 6). Cada seção documenta a equação estimada, a metodologia "
        "de ajuste, a amostra utilizada, os resultados numéricos (médias posteriores e intervalos de credibilidade "
        "de 94%, salvo indicação contrária) e uma leitura honesta — incluindo sinais inesperados, sinais fracos e "
        "limitações conhecidas, sem suavizar achados desconfortáveis. Uma síntese comparativa entre os seis modelos "
        "encerra o documento.",
        BODY,
    ))
    story.append(Paragraph(
        "Convenção de sinal usada em todos os modelos: <i>deviation(t) = 100 · ln(PTAX(t) / equilíbrio(t))</i> — "
        "um desvio positivo significa que o Real está mais depreciado do que o nível implícito pela PPP; um "
        "coeficiente positivo em qualquer canal, portanto, significa \"esse canal empurra o desvio para cima "
        "(BRL mais fraco)\".",
        BODY,
    ))
    story.append(Spacer(1, 6))

    # ========================================================================
    # SEÇÃO 1 — Equilíbrio & Dados
    # ========================================================================
    story += section_header("1", "Equilíbrio de PPP e Canais Candidatos", "Aba do dashboard: “Equilibrium &amp; Data” — base de dados, não é um modelo de regressão")

    story.append(Paragraph("Especificação", H2))
    story.append(Paragraph(
        "O equilíbrio é a PPP <b>relativa</b> (não absoluta): a razão entre o índice de preços cheio do Brasil "
        "(IPCA) e o índice de preços cheio dos EUA (CPI), ancorada à PTAX efetivamente observada em um mês-base "
        "selecionável no próprio dashboard.",
        BODY,
    ))
    story.append(equation_box([
        r"\mathrm{equilíbrio}(t)=PTAX(t_0)\cdot\dfrac{IPCA_{BR}(t)/IPCA_{BR}(t_0)}{CPI_{US}(t)/CPI_{US}(t_0)}",
        r"\mathrm{deviation}(t)=100\cdot\ln\!\left(\dfrac{PTAX(t)}{\mathrm{equilíbrio}(t)}\right)",
    ]))
    story.append(Spacer(1, 8))
    story.append(Paragraph("<i>t₀</i> = mês-base, selecionável no próprio dashboard.", BODY_TIGHT))
    story.append(Paragraph("Metodologia", H2))
    story.append(Paragraph(
        "Não é uma regressão — é a construção de dados que alimenta as cinco seções seguintes. A dependência do "
        "mês-base é real (PPP relativa não é invariante à escolha do mês-base) e é exposta diretamente no "
        "dashboard via o seletor de mês-base, não escondida atrás de um valor fixo.",
        BODY,
    ))
    story.append(Paragraph("Amostra", H2))
    story.append(Paragraph(
        "1994-07 até o mês mais recente — a janela onde PTAX, IPCA (Brasil) e CPI (EUA) coexistem.",
        BODY,
    ))
    story.append(Paragraph("Canais candidatos", H2))
    story.append(Paragraph(
        "Oito séries candidatas a explicar o desvio, cada uma com sua própria janela de cobertura (sem "
        "preenchimento retroativo antes do início real de cada uma):",
        BODY,
    ))
    story.append(results_table(
        [
            ["Canal", "Definição", "Início", "Fonte"],
            ["carry", "Selic − Fed Funds (diferencial de juros nominal)", "1999-03", "diferenciais_juros"],
            ["tot", "Termos de troca (Funcex PX/PM)", "1994-07*", "cmb_termos_troca (IPEADATA)"],
            ["breakeven", "Inflação implícita de 10 anos (PREJS − NTNBJS @120M)", "2006-01", "base_mercado.interest_rates"],
            ["breakeven_gap", "breakeven − meta de inflação (CMN)", "2006-01", "inflc_meta (SGS 13521)"],
            ["fiscal", "CDS Brasil 5Y USD", "2007-12", "cmb_risco_pais (investing.com)"],
            ["dxy", "ICE US Dollar Index (DXY)", "1971*", "cmb_dollar_index (Yahoo Finance)"],
            ["trade_pct_gdp", "Saldo comercial, m. móvel 12m / PIB USD m. móvel 12m", "—", "cmb_balanco_pagmt + atv_pib_usd"],
            ["ca_pct_gdp", "Conta corrente, m. móvel 12m / PIB USD m. móvel 12m", "—", "cmb_balanco_pagmt + atv_pib_usd"],
        ],
        col_widths=[62, 188, 55, 137],
    ))
    story.append(Spacer(1, 3))
    story.append(Paragraph("* histórico mais longo, recortado para o início da amostra (1994-07).", ParagraphStyle("fn", fontName="DejaVuSans-Oblique", fontSize=7.6, textColor=MUTED, spaceAfter=6)))
    story.append(reference("aba “Equilibrium &amp; Data” — gráfico principal (PTAX vs. equilíbrio) e o seletor com as 8 séries de canais brutos."))
    story.append(PageBreak())

    # ========================================================================
    # SEÇÃO 2 — Modelo Bayesiano (contemporâneo)
    # ========================================================================
    story += section_header("2", "Modelo Bayesiano — Especificação Contemporânea", "Aba do dashboard: “Bayesian Model” · especificação “primary_contemp”")

    story.append(Paragraph("Especificação", H2))
    story.append(equation_box([
        r"\Delta\,\mathrm{dev}(t)=\alpha+\beta_{\mathrm{carry}}\,z(\Delta\mathrm{carry}_t)+\beta_{\mathrm{fiscal}}\,z(\Delta\mathrm{fiscal}_t)",
        r"{}+\beta_{\mathrm{gap}}\,z(\Delta\mathrm{gap}_t)+\beta_{\mathrm{dxy}}\,z(\Delta\mathrm{dxy}_t)+\varepsilon_t",
    ]))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "Todas as variáveis explicativas entram em primeira diferença, contemporânea (sem defasagem adicional), "
        "padronizadas (z-score).",
        BODY_TIGHT,
    ))
    story.append(Paragraph("Metodologia", H2))
    story.append(Paragraph(
        "Regressão bayesiana via PyMC/NUTS, 4 cadeias. Erro Normal (testado contra Student-t em versões anteriores "
        "da especificação; Normal favorecida — sem evidência de caudas pesadas neste tamanho de amostra). "
        "Convergência limpa: r-hat = 1,00 em todos os parâmetros, ~28s de tempo de ajuste.",
        BODY,
    ))
    story.append(Paragraph("Amostra: n = 221, 2008-01 a 2026-06.", BODY_TIGHT))
    story.append(Paragraph("Resultados", H2))
    story.append(results_table([
        ["Parâmetro", "Média posterior", "IC 94%", "Leitura"],
        ["α", "0,227", "—", "drift residual do desvio"],
        ["β_carry", "−0,464", "[−0,847, −0,074]", "confiavelmente negativo — sinal “errado” vs. UIP"],
        ["β_fiscal", "+2,651", "[2,165, 3,111]", "fortemente positivo, sinal esperado"],
        ["β_breakeven_gap", "+0,133", "cruza zero", "sem sinal detectável"],
        ["β_dxy", "+1,030", "[0,594, 1,449]", "positivo, sinal esperado"],
    ], col_widths=[80, 80, 100, 182]))
    story.append(Spacer(1, 3))
    story.append(Paragraph(
        "Fiscal e DXY são os canais mais robustos desta especificação. Carry aparece com sinal consistentemente "
        "negativo — quanto maior o diferencial de juros a favor do Brasil, maior (não menor) o desvio — a mesma "
        "direção “errada” em relação à paridade descoberta de juros (UIP) já encontrada, de forma independente, em "
        "<i>uip_model.py</i> e <i>carry_model.py</i>.",
        BODY,
    ))
    story += caution(
        "O intercepto (α) absorve a maior parte do drift de longo prazo do desvio — um teste à parte (não "
        "incorporado ao dashboard) mostrou que forçar α=0 não elimina esse drift, apenas o realoca para o resíduo; "
        "um segundo teste com correção de erro (deviation_lag1) sugere reversão à média fraca (P≈89%, abaixo do "
        "critério de 94% deste documento), com meia-vida mediana de ~44 meses — compatível com a literatura "
        "clássica do “PPP puzzle” (Rogoff), mas não incorporada como especificação própria no dashboard."
    )
    story.append(reference(
        "aba “Bayesian Model” — tabela de diagnóstico, gráfico de ajuste histórico (Δdeviation observado vs. "
        "ajustado, banda de credibilidade 94%), decomposição cumulativa (log/%) e ponte em R$/US$ nominal."
    ))
    story.append(PageBreak())

    # ========================================================================
    # SEÇÃO 3 — Espaço de Estados, Tentativa Dois (η=0)
    # ========================================================================
    story += section_header("3", "Espaço de Estados — Tentativa Dois (η fixado em zero)", "Aba do dashboard: “State-Space (Attempt Two)”")

    story.append(Paragraph("Especificação", H2))
    story.append(equation_box([
        r"\mathrm{dev}(t)=\alpha+\varphi\,\mathrm{dev}(t{-}1)+\beta_{\mathrm{carry}}z(\Delta\mathrm{carry}_t)+\beta_{\mathrm{tot}}z(\Delta\mathrm{tot}_t)",
        r"{}+\beta_{\mathrm{be}}z(\Delta\mathrm{be}_t)+\beta_{\mathrm{fiscal}}z(\Delta\mathrm{fiscal}_t)+\beta_{\mathrm{dxy}}z(\Delta\mathrm{dxy}_t)+\varepsilon_t",
    ]))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "φ restrito a (0,1) via prior Uniforme (impõe estacionariedade a priori); dev(t−1) mantido em "
        "unidades nativas (não padronizado). equilíbrio(t) é tomado como exatamente igual ao PPP determinístico "
        "da Seção 1 — η (ruído do próprio equilíbrio) fixado em zero nesta versão. <i>be</i> abrevia breakeven.",
        BODY_TIGHT,
    ))
    story.append(Paragraph("Metodologia", H2))
    story.append(Paragraph(
        "PyMC/NUTS, mesma ferramenta da Seção 2. Convergência limpa: r-hat = 1,00, sem divergências, ~41s de "
        "tempo de ajuste. Nesta forma (η=0), o modelo ainda <b>não</b> é um verdadeiro filtro de Kalman de dois "
        "estados — nada aqui é de fato não observado; equilíbrio e desvio são ambos diretamente calculáveis a "
        "partir da Seção 1. A versão com η livre está na Seção 4.",
        BODY,
    ))
    story.append(Paragraph("Amostra: n = 219, 2008-01 a 2026-04.", BODY_TIGHT))
    story.append(Paragraph("Resultados", H2))
    story.append(results_table([
        ["Parâmetro", "Valor", "IC 94% / P(sinal)", "Leitura"],
        ["φ", "0,993", "[≈0,982, 1,000]", "quase-raiz-unitária; meia-vida mediana 111m, IC [38, 1669]m — não confiável"],
        ["α", "≈0,331", "cruza zero", "sem drift claramente não-nulo"],
        ["β_carry", "—", "[−0,868, −0,048]", "confiavelmente negativo, sinal “errado” vs. UIP"],
        ["β_tot", "—", "P(β&lt;0)=0,511", "cara-ou-coroa — sem sinal (tentativa 1 achava este o canal mais forte)"],
        ["β_breakeven", "—", "P=0,811", "direção esperada, mas abaixo do critério de 94%"],
        ["β_fiscal", "3,086→2,635*", "P=1,000", "extremamente forte e certo"],
        ["β_dxy", "+1,031", "[0,601, 1,469], P=1,000", "positivo, sinal esperado"],
    ], col_widths=[75, 65, 115, 187]))
    story.append(Spacer(1, 3))
    story.append(Paragraph("* valor recalculado após a inclusão do canal dxy no reajuste; os demais canais não se alteraram de forma material com essa inclusão.", ParagraphStyle("fn", fontName="DejaVuSans-Oblique", fontSize=7.6, textColor=MUTED, spaceAfter=4)))
    story += caution(
        "A troca de defasagem para contemporâneo (vs. a especificação original em diferença defasada, não mais "
        "exibida no dashboard) reordenou substancialmente quais canais carregam sinal — carry passa a ter sinal "
        "confiável (na direção “errada”), terms-of-trade perde todo o sinal que tinha. Isso indica que o "
        "ranking de canais de uma especificação isolada não deve ser lido como fato assentado."
    )
    story.append(reference(
        "aba “State-Space (Attempt Two)” — ajuste histórico (Δdeviation), ajuste em nível nominal PTAX, "
        "decomposição e ponte."
    ))
    story.append(PageBreak())

    # ========================================================================
    # SEÇÃO 4 — Filtro de Kalman (η livre)
    # ========================================================================
    story += section_header("4", "Filtro de Kalman — η Livre", "Aba do dashboard: “Kalman Filter (η free)” · o único modelo de dois estados de fato")

    story.append(Paragraph("Especificação", H2))
    story.append(equation_box([
        r"eq(t)=eq(t{-}1)+\pi_{\mathrm{diff}}(t)+\eta(t),\quad\eta\sim\mathcal{N}(0,\sigma_\eta^2)",
        r"dev(t)=\alpha+\varphi\,dev(t{-}1)+\beta_{\mathrm{carry}}z(\Delta\mathrm{carry}_t)+\beta_{\mathrm{tot}}z(\Delta\mathrm{tot}_t)",
        r"{}+\beta_{\mathrm{be}}z(\Delta\mathrm{be}_t)+\beta_{\mathrm{fiscal}}z(\Delta\mathrm{fiscal}_t)+\varepsilon_t",
        r"y(t)=eq(t)+dev(t),\quad R=0",
    ]))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "Medição exata (R=0) — identificação vem da dinâmica distinta dos dois estados (eq é passeio aleatório "
        "puro, impulsionado pelo diferencial real de inflação BR−US em log; dev é AR(1) com regressores, <i>be</i> "
        "abreviando breakeven). Canais: apenas os 4 originais (carry, tot, breakeven, fiscal) — dxy não está "
        "incluído aqui (conjunto de canais desta aba congelado antes da adição do dxy na Seção 3).",
        BODY_TIGHT,
    ))
    story.append(Paragraph("Metodologia", H2))
    story.append(Paragraph(
        "Implementado manualmente via <i>pytensor.scan</i> — nenhum pacote pronto de espaço de estados se encaixa "
        "neste formato específico. Validado contra a versão η=0 (Seção 3) antes de ser usado: σ_η→0 reproduz o "
        "equilíbrio/desvio determinísticos da Seção 1 a ~1e-9. PyMC/NUTS, r-hat = 1,00, 0 divergências, ~39 "
        "minutos de tempo de ajuste (bem mais lento que os demais modelos — gradiente via <i>scan</i>).",
        BODY,
    ))
    story.append(Paragraph("Resultados", H2))
    story.append(results_table([
        ["Parâmetro", "Valor", "IC 94% / nota"],
        ["σ_η", "média 2,49", "[0,76, 3,49], P(σ_η&lt;0,1)=0,007 — não colapsou a zero"],
        ["φ", "0,970", "caiu de 0,992 (versão η=0)"],
        ["σ (ruído de dev)", "≈1,55", "caiu pela metade (era 3,15) — equilíbrio agora absorve parte do ruído"],
        ["meia-vida implícita", "≈27 meses", "caiu de mediana 94m (η=0) — mais próxima da faixa clássica de Rogoff (3–5 anos)"],
        ["β_carry", "—", "enfraquece, IC passa a tocar zero (antes confiavelmente negativo)"],
        ["β_tot", "—", "segue sem sinal"],
        ["β_breakeven, β_fiscal", "—", "essencialmente inalterados vs. Seção 3"],
    ], col_widths=[95, 75, 292]))
    story.append(Spacer(1, 3))
    story.append(Paragraph(
        "Como a medição é exata, eq_filtrado(t) + dev_filtrado(t) soma exatamente à taxa observada em cada "
        "rascunho posterior (~1e-14) — um gráfico “ajustado vs. observado” seria tautológico; a aba compara, em "
        "vez disso, a <b>partição</b> equilíbrio/desvio do filtro contra a partição rígida da Seção 3 (η=0).",
        BODY,
    ))
    story.append(Paragraph(
        "Achado substantivo: no mês mais recente da amostra, o equilíbrio filtrado está em R$ 5,18 vs. a "
        "estimativa PPP determinística de R$ 3,48 (PTAX real: R$ 4,99) — o modelo reatribui boa parte do que "
        "parecia “desvio do BRL em relação à PPP” para “o próprio equilíbrio de PPP se deslocou”, em média "
        "~R$ 0,70 acima do caminho determinístico ao longo de toda a amostra.",
        BODY,
    ))
    story += caution(
        "A decomposição desta aba inclui um bloco de “atualização do filtro” (informação nova que a taxa "
        "observada revelou além da previsão determinística) que não é atribuível a nenhum canal — é calculada "
        "por rascunho posterior e depois com a média, já que a recursão de Kalman é não-linear nos parâmetros "
        "(φ, σ_η, σ_ε), ao contrário das Seções 2, 3 e 5."
    )
    story.append(reference(
        "aba “Kalman Filter (η free)” — comparação da partição equilíbrio/desvio (filtro vs. determinístico η=0) "
        "e decomposição com o bloco de atualização do filtro."
    ))
    story.append(PageBreak())

    # ========================================================================
    # SEÇÃO 5 — BEER (Níveis)
    # ========================================================================
    story += section_header("5", "Modelo BEER — Níveis", "Aba do dashboard: “BEER Model (Levels)” · especificação com 7 canais")

    story.append(Paragraph("Especificação", H2))
    story.append(equation_box([
        r"dev(t)=\alpha+\sum_{c}\beta_c\,z\left(\mathrm{canal}_c(t)\right)+\varepsilon_t",
    ]))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "Canais entram em NÍVEL contemporâneo (não em diferença), padronizados; SEM termo autorregressivo "
        "(sem φ, sem dev(t−1)) — regressão estática multivariada, no estilo clássico BEER/“pull factors”. "
        "α foi incluído por escolha deliberada além da equação literal fornecida (que não tem constante).",
        BODY_TIGHT,
    ))
    story.append(Paragraph(
        "Sete canais: carry, tot, breakeven, fiscal, dxy, trade_pct_gdp, ca_pct_gdp — os dois últimos exclusivos "
        "desta seção (saldo comercial e conta corrente, ambos % do PIB, janela móvel de 12 meses).",
        BODY,
    ))
    story.append(Paragraph("Metodologia", H2))
    story.append(Paragraph(
        "PyMC/NUTS, r-hat = 1,00, ~42s de tempo de ajuste. Amostra: n = 220, 2007-12 a 2026-04.",
        BODY,
    ))
    story.append(Paragraph("Resultados", H2))
    story.append(results_table([
        ["Parâmetro", "Valor", "IC 94%", "Leitura"],
        ["α", "14,5", "[13,1, 15,9]", "—"],
        ["β_carry", "−8,35", "[−10,16, −6,48]", "decisivamente negativo — sinal “errado” vs. UIP, agora inequívoco"],
        ["β_tot", "+1,41", "cruza zero", "sem sinal"],
        ["β_breakeven", "+1,90", "[0,22, 3,67]", "sinal esperado"],
        ["β_fiscal", "+6,61", "[4,86, 8,48]", "sinal esperado, forte"],
        ["β_dxy", "+13,88", "[11,83, 15,72]", "sinal esperado — o mais forte dos sete"],
        ["β_trade_pct_gdp", "+7,55", "[5,16, 10,16]", "significativo, mas sinal CONTRÁRIO ao esperado ingenuamente"],
        ["β_ca_pct_gdp", "−2,88", "[−5,11, −0,93]", "significativo, sinal esperado"],
    ], col_widths=[85, 55, 100, 222]))
    story += caution(
        "Regressão em níveis, sem termo AR e sem tendência explícita — não distingue uma relação causal genuína "
        "de duas séries persistentes que apenas caminharam juntas na mesma janela de ~18 anos. Risco de "
        "regressão espúria maior que nas especificações em diferença (Seções 2–4). trade_pct_gdp e ca_pct_gdp "
        "são altamente correlacionados entre si (comércio é grande componente da conta corrente) — mesmo com "
        "ambos individualmente significativos, isso deve ser lido como “o modelo não separa plenamente os dois”, "
        "não como dois efeitos independentes. De fato, testes de remoção de canais mostraram que o sinal "
        "“correto” de β_ca_pct_gdp isolado (removendo tot e trade_pct_gdp) se inverte para +1,60 — artefato da "
        "colinearidade, não um achado robusto. β_trade_pct_gdp, ao contrário, permanece positivo e significativo "
        "com ou sem ca_pct_gdp presente — mais robusto, ainda que na direção “errada”. Removendo também "
        "trade_pct_gdp, chega-se ao subconjunto “core 4” (carry, breakeven, fiscal, dxy) usado na Seção 6."
    )
    story.append(reference(
        "aba “BEER Model (Levels)” — tabela de diagnóstico, decomposição e ponte nominal (sem gráfico de ajuste "
        "histórico, já que não há termo autorregressivo — a decomposição já é o ajuste)."
    ))
    story.append(PageBreak())

    # ========================================================================
    # SEÇÃO 6 — Janela Móvel (Core 4)
    # ========================================================================
    story += section_header("6", "Janela Móvel — “Core 4”", "Aba do dashboard: “Rolling Window (Core 4)” · estabilidade temporal dos parâmetros")

    story.append(Paragraph("Especificação", H2))
    story.append(equation_box([
        r"dev(t)=\alpha+\beta_{\mathrm{carry}}z(\mathrm{carry}_t)+\beta_{\mathrm{be}}z(\mathrm{be}_t)+\beta_{\mathrm{fiscal}}z(\mathrm{fiscal}_t)+\beta_{\mathrm{dxy}}z(\mathrm{dxy}_t)+\varepsilon_t",
    ]))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "Mesma equação estática da Seção 5, restrita ao subconjunto “core 4” (<i>be</i> abrevia breakeven). "
        "Canais padronizados UMA VEZ sobre a média/desvio-padrão da amostra completa (não por janela) — assim, "
        "qualquer deriva aparente de um β reflete mudança real na relação, não mudança na média/desvio-padrão da "
        "própria janela.",
        BODY_TIGHT,
    ))
    story.append(Paragraph("Metodologia", H2))
    story.append(Paragraph(
        "OLS com erros-padrão HAC (Newey-West, maxlags=3), ajustado em janelas móveis de 60 meses (5 anos), "
        "passo mensal — 163 janelas, 2012-11 a 2026-06. Escolha deliberada em vez de reajustar o modelo "
        "bayesiano completo por janela (levaria bem mais de uma hora de processamento para a mesma resposta "
        "substantiva).",
        BODY,
    ))
    story.append(Paragraph("Referência de amostra completa (mesmo “core 4”, ajustado uma única vez)", H2))
    story.append(Paragraph("n = 222, 2007-12 a 2026-06 — todos os quatro canais significativos:", BODY_TIGHT))
    story.append(results_table([
        ["Parâmetro", "Valor", "IC 94%"],
        ["α", "14,71", "—"],
        ["β_carry", "−8,90", "[−10,67, −6,99]"],
        ["β_breakeven", "+2,31", "[0,47, 4,18]"],
        ["β_fiscal", "+4,27", "[2,61, 5,87]"],
        ["β_dxy", "+17,87", "[16,20, 19,55]"],
    ], col_widths=[100, 90, 272]))
    story.append(Paragraph("Resultados da janela móvel", H2))
    story.append(Paragraph(
        "Instabilidade real e substantiva dos parâmetros ao longo do tempo — não ruído estatístico:",
        BODY_TIGHT,
    ))
    for b in [
        "R² varia de 0,96 (janelas de 2013–2018) a 0,24 (janela de 2022), voltando a ~0,45 hoje.",
        "DXY — o canal mais forte na amostra completa — varia de ~+16 (2016–2018) para ~−10 (2022) e volta a "
        "perto de zero hoje; sua significância na amostra completa é, essencialmente, uma média entre períodos "
        "em que a relação funcionou fortemente e períodos em que não funcionou ou funcionou ao contrário.",
        "Carry e breakeven também trocam de sinal em alguns pontos da amostra.",
        "Fiscal é o canal mais estável na maior parte da amostra, mas perde significância na janela mais recente.",
    ]:
        story.append(Paragraph(f"•  {b}", BULLET))
    story.append(Spacer(1, 4))
    story += caution(
        "Os coeficientes de amostra completa descrevem uma relação MÉDIA entre 2008 e 2026, não uma relação "
        "estrutural estável. Para qualquer leitura prospectiva, os últimos 3–5 anos de janela móvel são mais "
        "informativos do que a média de amostra completa reportada em qualquer uma das Seções 2–5."
    )
    story.append(reference(
        "aba “Rolling Window (Core 4)” — gráfico de coeficiente móvel (seletor α/carry/breakeven/fiscal/dxy, "
        "banda de IC 95%, linha de referência de amostra completa), gráfico de R² móvel, e ponte nominal com "
        "seletor de mês inicial."
    ))
    story.append(PageBreak())

    # ========================================================================
    # SÍNTESE
    # ========================================================================
    story += section_header("7", "Síntese Comparativa", "Leitura conjunta das seis seções — o que se sustenta entre especificações")

    for label, txt in [
        ("Fiscal (CDS 5Y) e DXY", "os canais mais consistentemente significativos e com sinal esperado em praticamente todas as especificações que os incluem (Seções 2–6)."),
        ("Carry", "aparece com sinal “errado” em relação à UIP em toda especificação contemporânea/em nível (Seções 2, 3, 5, 6) — consistente com <i>uip_model.py</i> e <i>carry_model.py</i>, que já haviam encontrado o mesmo padrão de forma independente, fora deste dashboard."),
        ("Terms-of-trade (tot)", "foi o canal mais confiável na especificação original em diferença defasada do modelo bayesiano (não mais exibida no dashboard), mas perde todo o sinal assim que a especificação passa a ser contemporânea (Seções 3 e 4) — um lembrete de que o ranking de canais de uma especificação isolada é, em parte, artefato da própria especificação, não um fato assentado."),
        ("Breakeven / gap de desancoragem", "sinal fraco e inconsistente ao longo dos modelos — nunca atinge o critério de 94% de forma robusta, exceto de forma marginal no espaço de estados/Kalman (~81%) e no BEER em níveis."),
        ("Instabilidade temporal", "a Seção 6 mostra que mesmo os canais “core 4” (robustos em amostra completa) têm relações que mudam de magnitude e até de sinal ao longo do tempo — qualquer leitura pontual de um β deve vir acompanhada dessa ressalva."),
        ("Alerta metodológico transversal", "φ próximo de 1 (quase-raiz-unitária) nas Seções 3 e 4 torna a meia-vida implícita numericamente frágil; a especificação em níveis sem termo AR da Seção 5 tem risco de regressão espúria mais alto que as demais."),
    ]:
        story.append(Paragraph(f'<b><font color="#1F2853">{label}</font></b> — {txt}', BODY))

    story.append(Spacer(1, 10))
    story.append(rule(color=LINE, thickness=0.8, space_before=2, space_after=6))
    story.append(Paragraph(
        "Fonte: código e resultados documentados em <i>analytics/exchange_rate/CLAUDE.md</i> e nos módulos "
        "<i>ppp_equilibrium.py</i>, <i>bayesian_deviation_model.py</i>, <i>state_space_model.py</i> e "
        "<i>beer_model.py</i> (pasta <i>analytics/exchange_rate/models/</i>). Todas as séries brutas e o "
        "dashboard interativo (<i>ppp_dashboard.html</i>) acompanham este documento.",
        FOOTER,
    ))

    return story


def _footer_canvas(canvas, doc):
    canvas.saveState()
    canvas.setFont("DejaVuSans", 7.5)
    canvas.setFillColor(MUTED)
    canvas.drawString(20 * mm, 12 * mm, "LIS Capital — Modelos de Equilíbrio Cambial USD/BRL")
    canvas.drawRightString(A4[0] - 20 * mm, 12 * mm, f"Página {doc.page}")
    canvas.restoreState()


def run(out_path=OUT_PATH):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    doc = SimpleDocTemplate(
        out_path,
        pagesize=A4,
        leftMargin=20 * mm,
        rightMargin=20 * mm,
        topMargin=16 * mm,
        bottomMargin=18 * mm,
        title="Modelos de Equilíbrio Cambial USD/BRL — LIS Capital",
    )
    story = build_story()
    doc.build(story, onFirstPage=_footer_canvas, onLaterPages=_footer_canvas)
    print(f"Saved {out_path}")


if __name__ == "__main__":
    run()
