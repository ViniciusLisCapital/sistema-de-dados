"""Gera o PDF de propósito, metodologia e achados do modelo de atribuição de
causas cambiais (FX Attribution).

Documento complementar à aba "FX Attribution (Manager Letters)" de
`reports/FX Report.html` e a `fx_attribution_model.py`/`.md` (mesma
pasta de modelos) — não lê `claims.csv`/`documents.csv` diretamente para todo
o texto (a maior parte é hand-transcribed, mesma convenção de
`generate_model_spec_pdf.py`), mas as tabelas de contagem por categoria e o
gráfico da Seção 6 SÃO computados ao vivo a partir dos CSVs reais via
`fx_attribution_model`, já que essa fonte está disponível localmente (sem
dependência de MySQL, diferente dos modelos de PPP).

Revisado 2026-07-30 a partir de comentários de revisão (destaques em PDF)
feitos diretamente sobre a primeira versão deste documento — ver o histórico
da conversa para a lista completa. Mudanças principais dessa rodada:
- Seção 2: removida a menção a candidatos futuros (Kapitalo/SPX) — irrelevante
  para o propósito do documento, já coberta de forma mais natural no roadmap.
- Seção 3: adicionada uma nota sobre possível fusão futura de categorias.
- Seção 4: removida uma frase de meta-comentário desnecessária; adicionada
  uma tabela de exemplos reais de reivindicações (positiva, negativa, zero);
  corrigido o uso de "restatar"/"restatement" (anglicismo).
- Seção 5: corrigido "promediadas" (palavra estranha) para uma forma mais
  clara.
- Seção 6 (Kinea): removida uma inferência que ia além do que a taxonomia
  captura (o modelo não infere causas domésticas ocultas) e substituída por
  um gráfico real da série rolante de global_usd, computado ao vivo.
- Seção 7 (Verde Asset): adicionada uma tabela de contagem por categoria no
  mesmo formato da Seção 6 (pedido direto de revisão); achados reescritos
  para focar em qual regime domina em cada período, não em quando uma
  categoria "aparece pela primeira vez".
- Seções 8+9 fundidas em uma única seção curta, com o ponto sobre comparar
  narrativa vs. modelos quantitativos elevado a uso central (não mais uma
  entre seis notas de limitação/roadmap), e a linguagem de "estilo de
  escrita" substituída por "modelo mental do gestor" (correção direta de
  revisão: a diferença entre gestores é uma propriedade de como cada casa
  concebe a causalidade, não um artefato de redação).
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

from analytics.brasil.exchange_rate.models import fx_attribution_model as fx

matplotlib.rcParams["mathtext.fontset"] = "dejavusans"
_ASSET_DIR = tempfile.mkdtemp(prefix="lis_fxattr_assets_")

# ---------------------------------------------------------------------------
# Fonts — DejaVu Sans (bundled with matplotlib) for full Unicode coverage,
# same choice/rationale as generate_model_spec_pdf.py.
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

OUT_PATH = os.path.join("reports", "fx_attribution_methodology.pdf")

# ---------------------------------------------------------------------------
# Paragraph styles (same as generate_model_spec_pdf.py, duplicated here since
# each report script in this project is self-contained by convention)
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


_asset_counter = [0]


def _render_equation_png(mathtext_lines, fontsize=14, color="#1F2853"):
    text = "\n".join(f"${line}$" for line in mathtext_lines)
    _asset_counter[0] += 1
    path = os.path.join(_ASSET_DIR, f"eq_{_asset_counter[0]}.png")
    fig = plt.figure(figsize=(0.1, 0.1))
    fig.text(0, 0, text, fontsize=fontsize, color=color, linespacing=2.0)
    fig.savefig(path, dpi=300, transparent=True, bbox_inches="tight", pad_inches=0.09)
    plt.close(fig)
    return path


def equation_box(mathtext_lines, fontsize=14, max_width=420, box_width=440):
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


def chart_box(fig, max_width=460, box_width=470):
    """Embeds a matplotlib figure (already fully styled/labeled by the
    caller) as a bordered image block, same visual treatment as
    equation_box() but without the shaded background (a chart already has
    its own white plot area)."""
    _asset_counter[0] += 1
    path = os.path.join(_ASSET_DIR, f"chart_{_asset_counter[0]}.png")
    fig.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    with PILImage.open(path) as im:
        px_w, px_h = im.size
    dpi = 200
    nat_w, nat_h = px_w / dpi * 72, px_h / dpi * 72
    scale = min(1.0, max_width / nat_w)
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


def caution(text, label="Ressalva"):
    return [
        Paragraph(label, CAUTION_LABEL),
        Paragraph(text, CAUTION_BODY),
        Spacer(1, 4),
    ]


def reference(text):
    return Paragraph(f'<font name="DejaVuSans-Bold" color="#BB9B1D">Referência —</font> <i>{text}</i>', REF_BODY)


def section_header(number, title_text, subtitle_text):
    return [
        Paragraph(f"{number}. {title_text}", H1),
        Paragraph(subtitle_text, H1_TAG),
        rule(),
    ]


def bullets(items):
    return [Paragraph(f"•  {b}", BULLET) for b in items]


# ---------------------------------------------------------------------------
# Live data — category counts and the Kinea global_usd rolling chart are
# computed directly from the real claims.csv/documents.csv (not hand-
# transcribed), since this data lives locally and needs no MySQL connection.
# ---------------------------------------------------------------------------

def category_totals(manager):
    """Returns (n_claims, [(slug, count, pct), ...]) sorted by count desc."""
    claims = fx.load_claims(manager)
    totals = {s: 0 for s in fx.CATEGORY_SLUGS}
    for c in claims:
        totals[c["category"]] += 1
    n = len(claims)
    slugs_sorted = sorted(fx.CATEGORY_SLUGS, key=lambda s: -totals[s])
    return n, [(s, totals[s], 100 * totals[s] / n) for s in slugs_sorted]


def category_table(manager):
    n, rows = category_totals(manager)
    table_rows = [["Categoria", "Claims", "% do total"]]
    for slug, count, pct in rows:
        table_rows.append([slug, str(count), f"{pct:.1f}%".replace(".", ",")])
    return results_table(table_rows, col_widths=[150, 90, 220])


def kinea_globalusd_chart():
    claims = fx.load_claims("kinea")
    docs = fx.load_documents("kinea")
    monthly = fx.aggregate_monthly(claims, docs)
    months = [m["month"] for m in monthly]
    signed = [m["global_usd"] for m in monthly]
    rolling_signed = fx.rolling_mean(signed)
    rolling_abs = fx.rolling_mean([abs(v) for v in signed])

    x = list(range(len(months)))
    fig, ax = plt.subplots(figsize=(6.3, 2.5), dpi=200)
    ax.axhline(0, color="#B8BEC9", linewidth=0.8, zorder=1)
    ax.plot(x, rolling_signed, color="#1F2853", linewidth=1.6, label="Relevância direcional (com sinal)")
    ax.plot(x, rolling_abs, color="#BB9B1D", linewidth=1.4, linestyle="--", label="Grau de relevância (|score|)")
    tick_idx = list(range(0, len(months), 6))
    ax.set_xticks(tick_idx)
    ax.set_xticklabels([months[i] for i in tick_idx], rotation=45, ha="right", fontsize=7)
    ax.set_ylabel("Score rolante (3 meses)", fontsize=8)
    ax.tick_params(axis="y", labelsize=7)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.legend(fontsize=7, loc="upper left", frameon=False)
    ax.set_title(
        "Kinea — relevância de global_usd ao longo do tempo (média móvel de 3 meses)",
        fontsize=8.7, color="#1F2853", loc="left",
    )
    fig.tight_layout()
    return fig, months, rolling_signed, rolling_abs


# ---------------------------------------------------------------------------
# Document body
# ---------------------------------------------------------------------------

def build_story():
    story = []

    # --- Cover / intro -----------------------------------------------------
    story.append(Paragraph("LIS CAPITAL", ParagraphStyle("brand", fontName="DejaVuSans-Bold", fontSize=10, textColor=GOLD, spaceAfter=2)))
    story.append(Paragraph("Modelo de Atribuição de Causas Cambiais (FX Attribution)", TITLE))
    story.append(Paragraph("Propósito, metodologia e achados — leitura sistemática de cartas de gestores como sinal complementar aos modelos de preço", SUBTITLE))
    story.append(Paragraph("Documento interno · Julho de 2026", DATE_BADGE))
    story.append(rule(color=NAVY, thickness=2, space_before=8, space_after=10))

    story.append(Paragraph(
        "Este documento descreve o modelo de atribuição de causas cambiais (FX Attribution): uma leitura "
        "sistemática e taxonômica de cartas mensais de gestores de fundos, transformando comentário qualitativo "
        "sobre o câmbio USD/BRL em uma série numérica mensal. Ao contrário dos demais modelos documentados em "
        "<i>ppp_model_specs.pdf</i> — que regridem o desvio observado da PPP contra séries de preço (carry, DXY, "
        "CDS, termos de troca) —, este modelo captura o que os próprios gestores <b>dizem</b> estar movendo o "
        "Real, funcionando como um sinal independente de checagem cruzada contra os modelos estatísticos, não "
        "como um substituto para eles.",
        BODY,
    ))
    story.append(Paragraph(
        "As Seções 1–5 descrevem o propósito, o corpus, a taxonomia e a metodologia (fixos, independentes de "
        "qual gestor está sendo lido); as Seções 6–7 resumem os achados de cada um dos dois gestores hoje "
        "cobertos; a Seção 8 fecha com o uso pretendido deste framework e o que ainda falta construir.",
        BODY,
    ))
    story.append(Spacer(1, 6))

    # ========================================================================
    # SEÇÃO 1 — Propósito e Motivação
    # ========================================================================
    story += section_header("1", "Propósito e Motivação", "Por que um modelo baseado em narrativa, ao lado de modelos baseados em preço")

    story.append(Paragraph(
        "Todo modelo em <i>analytics/brasil/exchange_rate/models/</i> — UIP, carry, o modelo de desvio bayesiano, o "
        "filtro de Kalman, o BEER, o Ridge — é <b>baseado em preço</b>: regride o USD/BRL (ou seu desvio em "
        "relação a um equilíbrio de PPP) contra séries mensuráveis (diferencial de juros, CDS, DXY, termos de "
        "troca). Nenhum deles pergunta o que os agentes de mercado dizem estar acontecendo — apenas o que os "
        "dados estatisticamente sustentam.",
        BODY,
    ))
    story.append(Paragraph(
        "O modelo de atribuição de causas cambiais preenche essa lacuna deliberadamente: em vez de testar uma "
        "teoria contra os dados, ele lê a própria explicação do gestor para cada movimento do Real, mês a mês, e "
        "converte essa explicação em um placar numérico por regime causal (fiscal, monetário/carry, política, "
        "dólar global, commodities, sentimento de risco, China/EM, política comercial, fluxos de capital).",
        BODY,
    ))
    story.append(Paragraph("Usos concretos pretendidos", H2))
    story += bullets([
        "Identificar quando o consenso narrativo (ex.: \"é tudo dólar global\") diverge do que os modelos "
        "estatísticos de fato encontram como canal explicativo do desvio observado (ver Seção 8).",
        "Acompanhar como os regimes atribuídos mudam ao longo do tempo e entre gestores — um mesmo evento "
        "(ex.: tarifas de Trump) pode ser enquadrado por um gestor como <i>global_usd</i> e por outro como "
        "<i>trade_policy</i>, revelando diferenças no modelo mental de cada casa sobre a cadeia causal do câmbio.",
        "Servir de base metodológica reutilizável para outras tarefas de pontuação de texto no futuro (ex.: "
        "hawkish/dovish nas atas do Copom) — mesma ideia de esquema de extração fixo, taxonomia diferente.",
    ])
    story.append(PageBreak())

    # ========================================================================
    # SEÇÃO 2 — Corpus e Gestores Cobertos
    # ========================================================================
    story += section_header("2", "Corpus e Gestores Cobertos", "Fonte dos dados: cartas mensais de gestores de fundos")

    story.append(Paragraph(
        "Cada gestor recebe sua própria subpasta em <i>fx_attribution_data/&lt;gestor&gt;/</i>, com "
        "<i>documents.csv</i> (registro de todos os documentos-fonte, independentemente de terem gerado alguma "
        "reivindicação) e <i>claims.csv</i> (as reivindicações extraídas manualmente, fonte da verdade). O "
        "framework é agnóstico ao gestor por construção — a taxonomia, as regras de extração e a lógica de "
        "agregação não mudam; apenas o corpus-fonte difere.",
        BODY,
    ))
    story.append(results_table(
        [
            ["Gestor", "Documentos", "Claims", "Período", "Estrutura da publicação"],
            ["Kinea", "124", "101", "2021-05 a 2026-06", "Duas séries paralelas: carta principal (\"Carta do Gestor\") + \"Kinea Insights\" (aprofundamento temático)"],
            ["Verde Asset", "197", "172", "2010-01 a 2026-05", "Série única mensal (\"Relatório de Gestão\"); arquivo bruto vai até 1999, mas só 2010+ foi extraído até agora"],
        ],
        col_widths=[70, 65, 55, 90, 180],
    ))
    story.append(Spacer(1, 4))
    story += caution(
        "A cobertura de Kinea começa no meio de 2021 porque não há arquivo mais antigo disponível — não é um "
        "recorte deliberado. A de Verde Asset é um recorte deliberado (2010+ de um arquivo que vai até 1999), "
        "por ora não estendido."
    )
    story.append(reference("fx_attribution_model.md, seções \"Corpus\" e \"Verde Asset — second manager\"."))
    story.append(PageBreak())

    # ========================================================================
    # SEÇÃO 3 — Taxonomia
    # ========================================================================
    story += section_header("3", "Taxonomia (Nove Categorias Fixas)", "Definida antes da extração — não muda por gestor, nem é revisada durante a leitura de um corpus")

    story.append(Paragraph(
        "A taxonomia é definida <b>a priori</b> e compartilhada por todos os gestores. Isso é o que torna o "
        "modelo comparável entre gestores: a mesma categoria significa a mesma coisa, não importa qual carta "
        "está sendo lida.",
        BODY,
    ))
    story.append(results_table(
        [
            ["Categoria", "Definição", "Fronteira"],
            ["fiscal_br", "Trajetória de déficit/dívida do Brasil, medidas de gasto/receita, regra fiscal", "Numérico/legislativo, não popularidade"],
            ["monetary_br", "Nível/trajetória da Selic, guidance do BCB, diferencial de juro real BR-EUA", "Especificamente o canal de carry"],
            ["politics_br", "Eleições, Congresso, decisões judiciais, popularidade, imprevisibilidade de política", "Risco político não-numérico"],
            ["global_usd", "Força/fraqueza ampla do dólar do lado dos EUA — Fed, fiscal americano, política/instituições americanas, \"excepcionalismo\", de-dolarização", "Absorve o <i>porquê</i> o dólar se moveu; o efeito sobre o BRL é o que é pontuado"],
            ["commodities", "Minério, soja, petróleo, agro, energia; dinâmica de conta corrente/contas externas (balança comercial, entrada de USD via termos de troca)", "Renomeada de \"commodities\" para incluir contas externas — mesmo mecanismo causal em termos de balanço de pagamentos"],
            ["risk_sentiment", "VIX, fluxos para porto-seguro, apetite a risco em EM de forma ampla, não ligado a commodities ou ao dólar", "—"],
            ["china_em", "Estímulo/mercado imobiliário/crescimento chinês como motor de demanda por commodities e sentimento EM", "—"],
            ["trade_policy", "Ações tarifárias diretas (sobre o Brasil ou globais)", "Distinto do canal de dólar/sentimento de risco que ela pode disparar"],
            ["capital_flows", "Reivindicações explícitas de fluxo/posicionamento, não de fundamentos", "Raramente populada em corpus de estilo mais narrativo"],
        ],
        col_widths=[75, 240, 145],
    ))
    story.append(Spacer(1, 4))
    story += caution(
        "Único caso de fronteira resolvido até agora: uma reivindicação de março de 2024 (Kinea) citava carry "
        "elevado <b>e</b> melhora estrutural da conta corrente como motores conjuntos. Decisão do usuário: não "
        "criar uma décima categoria — dividir a reivindicação em duas linhas, mantendo a parte de carry em "
        "<i>monetary_br</i> e movendo a parte de conta corrente para <i>commodities</i> (renomeada para incluir "
        "\"termos de troca / contas externas\")."
    )
    story.append(Paragraph(
        "É possível que, à medida que mais gestores forem adicionados, outras destas nove categorias se revelem "
        "redundantes entre si e sejam fundidas — como já ocorreu uma vez (caso acima). Por ora, a granularidade "
        "é mantida deliberadamente alta: o objetivo desta fase é observar quais fronteiras emergem organicamente "
        "da leitura das cartas, não impor um agrupamento a priori.",
        BODY,
    ))
    story.append(reference("fx_attribution_model.md, tabela \"Taxonomy\" e nota de resolução de 2026-07-29."))
    story.append(PageBreak())

    # ========================================================================
    # SEÇÃO 4 — Convenção de Sinal e Regras de Extração
    # ========================================================================
    story += section_header("4", "Convenção de Sinal e Regras de Extração", "Como uma frase de uma carta vira um número")

    story.append(Paragraph("Convenção de sinal", H2))
    story.append(Paragraph(
        "A direção pontua o efeito implícito da reivindicação <b>sobre o BRL</b>, nunca sobre o sujeito da "
        "própria reivindicação. +1 = fortemente favorável à apreciação do BRL; −1 = fortemente indutor de "
        "depreciação. Uma reivindicação do tipo \"o dólar está se fortalecendo globalmente\" é pontuada "
        "<b>negativa</b> (ruim para o BRL), não positiva.",
        BODY,
    ))
    story.append(Paragraph("Exemplos reais (cartas Kinea)", H2))
    story.append(results_table(
        [
            ["Trecho da carta", "Categoria", "Direção", "Por que essa pontuação"],
            ["\"...manter uma posição comprada no dólar norte-americano...\"", "global_usd", "−0,5", "Aposta na força do dólar por força econômica americana → efeito negativo sobre o BRL, mesmo sendo formalmente uma posição em dólar, não em real"],
            ["\"...o real foi a pior moeda do mundo no ano...\"", "fiscal_br", "−1,0", "Crise de credibilidade fiscal citada explicitamente como motor do pior desempenho global do BRL"],
            ["\"...permanecemos comprados no Real em virtude do elevado diferencial de juros...\"", "monetary_br", "+1,0", "Diferencial de juros citado explicitamente como razão da posição favorável ao BRL"],
            ["\"...a tendência da moeda foi contrária à esperada vis-à-vis o início do ciclo de cortes do BACEN...\"", "monetary_br", "0,0", "O canal de carry é nomeado explicitamente, mas o texto relata que ele falhou em explicar o movimento do ano — zero deliberado (regra 6), não silêncio"],
        ],
        col_widths=[195, 65, 55, 145],
    ))
    story.append(Spacer(1, 6))
    story.append(Paragraph("Regras de extração", H2))
    story += bullets([
        "<b>O câmbio precisa ser o efeito, não uma causa citada de outra coisa.</b> Quando uma carta cita um "
        "movimento passado do BRL como causa de um resultado político (não o contrário), a reivindicação é "
        "excluída — é o inverso do que este modelo mede.",
        "<b>O texto precisa conectar explicitamente a causa a um efeito cambial</b> (câmbio, real, dólar, "
        "moeda) — não basta discutir um tema (fiscal, tarifas, China) que <i>provavelmente</i> afetaria o "
        "câmbio pela lógica econômica. Exigir que as próprias palavras do gestor tracem o vínculo, em vez de "
        "aplicar prioris econômicos próprios, é o que faz deste um modelo do que os gestores atribuem, não do "
        "que a teoria implicaria.",
        "<b>Uma reivindicação por (categoria, direção/horizonte) por documento</b>, não por frase — uma mesma "
        "carta costuma repetir o mesmo argumento causal duas ou três vezes com palavras diferentes; contar cada "
        "repetição infla a soma pela verbosidade, não por sinal genuíno. Argumentos genuinamente opostos na "
        "mesma carta permanecem como reivindicações separadas.",
        "<b>Um movimento cambial regional/bilateral não é \"Global USD\"</b> a menos que o texto enquadre a "
        "força/fraqueza do dólar como ampla/global.",
        "<b>Posicionamento próprio não é, por si só, uma reivindicação de atribuição.</b> \"Estamos vendidos em "
        "real, como hedge\" descreve uma posição, não uma causa — só conta quando o texto dá uma razão explícita.",
        "<b>Uma reivindicação pode pontuar 0 deliberadamente</b> — ex.: \"o BRL flutuou sem tendência clara "
        "apesar da aversão a risco\" é uma afirmação real e explícita de que um canal <i>não</i> moveu a moeda "
        "dessa vez, o que é substancialmente diferente daquele canal simplesmente não ter sido discutido (que "
        "não aparece de forma alguma em <i>claims.csv</i>, não contribuindo para a soma por omissão).",
    ])
    story += caution(
        "A regra 6 (zero deliberado) é responsável por alguns dos achados mais reveladores do corpus: um ensaio "
        "fiscal inteiro (\"Frankenstein\", Kinea, ago/2024) ou um ensaio sobre a balança comercial de petróleo "
        "(\"O petróleo é nosso!\", Kinea, out/2023) pode discutir o tema exaustivamente e ainda pontuar zero, "
        "porque a implicação cambial nunca é explicitada — a relevância temática não é critério de extração, "
        "um vínculo explícito a um efeito cambial é."
    )
    story.append(reference("fx_attribution_model.md, seções \"Sign convention\" e \"Extraction rules\"; exemplos extraídos de fx_attribution_data/kinea/claims.csv."))
    story.append(PageBreak())

    # ========================================================================
    # SEÇÃO 5 — Agregação, Suavização e Saídas
    # ========================================================================
    story += section_header("5", "Agregação, Suavização e Saídas", "Como as reivindicações mensais viram uma série de tempo")

    story.append(Paragraph("Agregação: soma mensal, não média", H2))
    story.append(equation_box([
        r"\mathrm{score}_c(m)=\sum_{i\,\in\,\mathrm{claims}(c,\,m)}\mathrm{direction}_i",
    ]))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "Por categoria <i>c</i> e mês <i>m</i>, as reivindicações daquele mês são <b>somadas</b> — nunca é "
        "calculada uma média simples. É a mesma convenção de \"hawkish menos dovish\" líquido usada na pontuação "
        "de textos de bancos centrais. Isso tem uma propriedade útil: um mês sem reivindicações em uma categoria "
        "soma 0, que é matematicamente o valor correto de \"sem sinal líquido\" — não precisa de tratamento "
        "especial contra uma reivindicação \"neutra\", porque não existe uma.",
        BODY,
    ))
    story.append(Paragraph(
        "O que a soma sozinha não distingue: 0 por <b>silêncio</b> (nenhuma reivindicação naquele mês) vs. 0 por "
        "<b>reivindicações genuínas que se cancelaram</b>. Por isso <i>n_documents</i> e <i>n_claims</i> "
        "acompanham cada linha mensal, tanto no CSV quanto no Excel — para que essa distinção nunca se perca ao "
        "olhar só a soma.",
        BODY,
    ))
    story.append(Paragraph("Suavização: média móvel de 3 meses, em duas leituras", H2))
    story.append(Paragraph(
        "Duas visões, não uma só: <b>relevância direcional</b> (média móvel de 3 meses da soma <i>com sinal</i> "
        "— para qual lado o regime está apontando) e <b>grau de relevância</b> (média móvel de 3 meses de "
        "|score| — o quanto o regime importou, independentemente da direção, para que um mês com "
        "reivindicações opostas ainda apareça em vez de anular para perto de zero).",
        BODY,
    ))
    story.append(Paragraph("Saídas", H2))
    story += bullets([
        "<i>documents.csv</i> / <i>claims.csv</i> — as duas fontes da verdade, por gestor.",
        "<i>monthly.csv</i> — derivado, uma linha por mês (regenerado a cada execução).",
        "<i>fx_attribution.xlsx</i> — três abas (Claims, Monthly, Trends), com os dois gráficos de linha da "
        "aba Trends, também regenerados a cada execução.",
        "Aba \"FX Attribution (Manager Letters)\" em <i>FX Report.html</i> — "
        "seletor de gestor, gráficos das duas visões de suavização, gráfico de barras de documentos/claims por "
        "mês, e uma tabela de reivindicações filtrável por categoria.",
    ])
    story.append(reference("fx_attribution_model.md, seções \"Aggregation\" e \"Files\"; fx_attribution_model.py."))
    story.append(PageBreak())

    # ========================================================================
    # SEÇÃO 6 — Achados: Kinea
    # ========================================================================
    story += section_header("6", "Achados — Kinea", "124 documentos, 101 claims, 2021-05 a 2026-06 — piloto original, arquivo integral disponível")

    story.append(category_table("kinea"))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "<b>global_usd</b> concentra quase 40% das reivindicações de Kinea — bem à frente de qualquer outra "
        "categoria. O gráfico abaixo mostra a relevância rolante (3 meses) desse regime ao longo de todo o "
        "arquivo, nas duas leituras (direcional e magnitude), para que os períodos em que ele pesou mais fiquem "
        "visíveis diretamente nos dados, em vez de em uma afirmação solta: a relevância direcional atinge seu "
        "ponto mais negativo em 2025-01 (−0,9) e seu ponto mais positivo em 2026-01 (+0,6). O modelo não infere "
        "nada além disso — não afirma, por exemplo, que uma causa \"na verdade\" doméstica esteja sendo "
        "atribuída ao dólar global; ele só registra o que a própria carta declara.",
        BODY,
    ))
    fig, _, _, _ = kinea_globalusd_chart()
    story.append(chart_box(fig))
    story.append(Spacer(1, 6))
    story += bullets([
        "<b>trade_policy nunca dispara uma única vez em mais de cinco anos</b>, apesar das tarifas de Trump "
        "(vintages de 2018-19 e 2025-26), da guerra de chips EUA-China e do reshoring dominarem várias cartas "
        "por volume de texto — a Kinea canaliza quase todo efeito cambial de tarifas via enquadramento de "
        "<i>global_usd</i>, não como um vínculo direto.",
        "<i>Kinea Insights</i> (o aprofundamento temático) carrega apenas 10% do total de reivindicações apesar "
        "de ser pouco mais da metade de todos os documentos (64 de 124) — a carta principal (\"Carta do "
        "Gestor\") carrega quase todo o sinal, todo ano.",
        "Um ensaio fiscal inteiro pode pontuar zero: o texto de agosto/2024 (\"Frankenstein: o monstro fiscal "
        "brasileiro\") é inteiramente sobre a estrutura fiscal do Brasil, mas não contribui nada a "
        "<i>fiscal_br</i>, porque nunca declara a implicação cambial explicitamente.",
        "Dezembro é consistentemente um dos meses mais acentuados em vários anos — 2024 é o caso extremo "
        "(<i>fiscal_br</i> −1,7, <i>global_usd</i> −1,2, dois documentos com reivindicações retrospectivas/de "
        "perspectiva de alta confiança no mesmo mês).",
    ])
    story.append(reference("fx_attribution_model.md, seção \"Findings from the full-history run\"; tabela e gráfico computados ao vivo a partir de fx_attribution_data/kinea/."))
    story.append(PageBreak())

    # ========================================================================
    # SEÇÃO 7 — Achados: Verde Asset
    # ========================================================================
    story += section_header("7", "Achados — Verde Asset", "197 documentos, 172 claims, 2010-01 a 2026-05 — estendido para trás em seis rodadas")

    story.append(category_table("verde_asset"))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "Em números de corpus inteiro, <b>global_usd também é a categoria mais frequente para Verde</b> "
        "(25,6%) — mas a distribuição é bem mais equilibrada do que a de Kinea: o topo de Verde concentra "
        "pouco mais de um quarto das reivindicações, contra quase 40% de Kinea no seu próprio topo. Isso já é, "
        "em si, uma diferença de modelo mental entre as duas casas: Kinea lê o câmbio predominantemente por uma "
        "lente global-macro; Verde distribui a atribuição de forma mais equilibrada entre fiscal, fluxos, "
        "carry e commodities.",
        BODY,
    ))
    story.append(Paragraph(
        "A pergunta mais relevante para Verde não é quando uma categoria \"aparece pela primeira vez\", e sim "
        "qual regime domina em cada período — a tabela abaixo, construída a partir das seis rodadas de extração "
        "que compuseram este corpus, mostra exatamente isso:",
        BODY_TIGHT,
    ))
    story.append(results_table(
        [
            ["Janela", "Docs", "Claims", "Categoria dominante no período"],
            ["2010-2013", "48", "37", "commodities e monetary_br co-dominam (10 e 9 de 37) — auge do superciclo de commodities e do carry; global_usd distante terceiro (5)"],
            ["2014-2017", "48", "53", "global_usd (14 de 53) — sequência de choques globais (desvalorização do RMB, Brexit, eleição de Trump)"],
            ["2018-2019", "24", "15", "monetary_br (5 de 15) — narrativa de erosão de carry"],
            ["2020-2022", "36", "24", "fiscal_br (9 de 24) — desmonte do Teto de Gastos"],
            ["2023-2024", "24", "20", "fiscal_br permanece relevante (6 dos 20 meses) — mesmo regime da janela anterior, não uma categoria nova"],
            ["2025-2026", "17", "23", "capital_flows (5 de 23) — narrativas de fluxo estrangeiro explicitamente quantificadas"],
        ],
        col_widths=[75, 45, 55, 285],
    ))
    story.append(Spacer(1, 6))
    story += bullets([
        "<b>O regime dominante muda de forma real e sistemática por época</b> — do binômio "
        "commodities/carry do superciclo (2010-2013), para o dólar global dos choques de 2014-2017, para o "
        "carry doméstico de 2018-2019, para o fiscal dominante de 2020-2024, para os fluxos quantificados de "
        "2025-2026. Cada janela reflete o regime macro genuinamente vivido naquele período, não um artefato da "
        "ordem de extração.",
        "<b>trade_policy dispara em Verde (2 de 172 claims, jul/2025 e uma ocorrência anterior) mas nunca em "
        "Kinea</b> — a mesma tarifa de 50% de Trump sobre o Brasil é lida por Verde como um vínculo direto "
        "(trade_policy) e por Kinea, historicamente, sempre através do enquadramento de dólar global — um "
        "contraste real de modelo mental entre gestores diante do mesmo tipo de evento.",
        "<b>capital_flows é proporcionalmente muito mais ativa em Verde (14,0%) do que em Kinea (5,0%)</b> — "
        "reflexo de um modelo mental que se apoia mais em narrativas de fluxo explícitas e frequentemente "
        "quantificadas (entradas/saídas de renda variável estrangeira, timing de repatriação de dividendos) do "
        "que o de Kinea, mais concentrado no eixo global-macro.",
    ])
    story.append(reference("fx_attribution_model.md, seção \"Verde Asset — second manager\"; tabela de categorias computada ao vivo a partir de fx_attribution_data/verde_asset/."))
    story.append(PageBreak())

    # ========================================================================
    # SEÇÃO 8 — Da Narrativa ao Quantitativo (uso pretendido + limitações)
    # ========================================================================
    story += section_header(
        "8", "Da Narrativa ao Quantitativo",
        "O uso central deste framework — e o que ainda falta construir para chegar lá",
    )

    story.append(Paragraph(
        "O uso mais importante deste framework — ainda não realizado, apenas habilitado por este documento — é "
        "comparar a atribuição narrativa (o que os gestores dizem estar movendo o BRL) com os canais que os "
        "modelos baseados em preço deste mesmo projeto (Bayesiano, Ridge, espaço de estados, BEER — ver "
        "<i>ppp_model_specs.pdf</i>) de fato encontram como explicativos do desvio observado. Um mês em que os "
        "gestores atribuem o movimento a <i>global_usd</i>, mas em que o modelo de Ridge não atribui peso "
        "relevante a DXY naquele mesmo período, é tão informativo quanto um mês em que narrativa e modelo "
        "concordam — em ambos os casos, a divergência (ou a concordância) é o dado, não um problema a ser "
        "resolvido antes de reportar.",
        BODY,
    ))
    story.append(Paragraph(
        "Qual regime domina em cada época — e o quanto uma categoria como <i>trade_policy</i> ou "
        "<i>capital_flows</i> aparece ou não — é uma propriedade do <b>modelo mental de cada gestor</b>: como "
        "aquela casa genuinamente concebe a cadeia causal por trás do câmbio, não um artefato de como o texto "
        "foi redigido. É exatamente por isso que comparar dois gestores entre si, e cada um deles contra os "
        "modelos quantitativos, tem valor real: cada comparação testa um modelo mental diferente contra os "
        "mesmos dados de preço.",
        BODY,
    ))
    story.append(Paragraph(
        "A peça que ainda falta construir para viabilizar essa comparação: hoje, a matriz mensal de cada "
        "gestor é independente — não há um cruzamento sistemático entre gestores, nem entre narrativa e modelo "
        "quantitativo. Esse cruzamento é o próximo passo natural deste framework, não uma extensão hipotética.",
        BODY,
    ))
    story.append(Spacer(1, 10))
    story.append(rule(color=LINE, thickness=0.8, space_before=2, space_after=6))
    story.append(Paragraph(
        "Fonte: metodologia e achados documentados em <i>fx_attribution_model.md</i> e "
        "<i>analytics/brasil/exchange_rate/CLAUDE.md</i>; código em <i>fx_attribution_model.py</i> (pasta "
        "<i>analytics/brasil/exchange_rate/models/</i>). As tabelas de categoria e o gráfico da Seção 6 foram "
        "computados diretamente a partir de <i>fx_attribution_data/&lt;gestor&gt;/claims.csv</i> e "
        "<i>documents.csv</i> ao gerar este PDF, não hand-transcribed. Os dados brutos por gestor e o dashboard "
        "interativo (aba \"FX Attribution\" de <i>FX Report.html</i>) acompanham este documento.",
        FOOTER,
    ))

    return story


def _footer_canvas(canvas, doc):
    canvas.saveState()
    canvas.setFont("DejaVuSans", 7.5)
    canvas.setFillColor(MUTED)
    canvas.drawString(20 * mm, 12 * mm, "LIS Capital — Modelo de Atribuição de Causas Cambiais")
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
        title="Modelo de Atribuição de Causas Cambiais — LIS Capital",
    )
    story = build_story()
    doc.build(story, onFirstPage=_footer_canvas, onLaterPages=_footer_canvas)
    print(f"Saved {out_path}")


if __name__ == "__main__":
    run()
