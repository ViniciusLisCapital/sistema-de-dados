"""Uma página A4 paisagem com o levantamento de valor justo do USDBRL.

Data | Fonte | Valor justo | Lógica — uma linha por declaração pública ou por
carta de gestão, em ordem cronológica. É a versão imprimível da nota em
`referencia/literature/fair_value_casas_de_gestao.md`; o texto é
hand-transcribed dali (mesma convenção de `models/generate_fx_attribution_pdf.py`),
nada é lido de CSV ou do MySQL, então roda offline.

    uv run python analytics/brasil/exchange_rate/generate_fair_value_pdf.py

Restrição de projeto: **cabe em uma página, e isso é verificado** — `run()`
levanta se o PDF sair com mais de uma. Ao acrescentar linha, encurte a coluna
Lógica: a 7,0pt em 167 mm cabem ~118 caracteres por linha, e o layout foi
dimensionado para no máximo duas linhas por célula.

Cores e fontes seguem os outros PDFs da pasta (paleta LIS, DejaVu Sans pela
cobertura Unicode). A cor do nome da fonte codifica o tipo: dourado = gestora
brasileira, verde = banco/sell side, navy = as demais.
"""
import os

import matplotlib
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    HRFlowable,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

_MPL_TTF = os.path.join(matplotlib.get_data_path(), "fonts", "ttf")
pdfmetrics.registerFont(TTFont("DejaVuSans", os.path.join(_MPL_TTF, "DejaVuSans.ttf")))
pdfmetrics.registerFont(TTFont("DejaVuSans-Bold", os.path.join(_MPL_TTF, "DejaVuSans-Bold.ttf")))
pdfmetrics.registerFont(TTFont("DejaVuSans-Oblique", os.path.join(_MPL_TTF, "DejaVuSans-Oblique.ttf")))
pdfmetrics.registerFontFamily(
    "DejaVuSans", normal="DejaVuSans", bold="DejaVuSans-Bold", italic="DejaVuSans-Oblique",
)

NAVY = colors.HexColor("#1F2853")
GOLD = colors.HexColor("#BB9B1D")
GREEN = colors.HexColor("#418791")
INK = colors.HexColor("#1A1F33")
MUTED = colors.HexColor("#7A88A8")
LINE = colors.HexColor("#D8DCE6")
BAND = colors.HexColor("#F4F5F8")

OUT_PATH = os.path.join("reports", "brasil", "fair_value_usdbrl.pdf")

# gestora brasileira | banco/sell side | demais
KIND_COLOR = {"g": GOLD, "s": GREEN, "o": NAVY}

# (data, fonte, kind, valor justo, tem número?, lógica)
ROWS = [
    ("28/06/2021", "IIF — Robin Brooks", "o", "R$ 4,50", True,
     "Boom de exportação de commodities e conta corrente projetada perto de +2% do PIB, a maior em 16 anos. Spot 4,90."),
    ("dez/2025", "Kapitalo — K10", "g", "real caro", False,
     "Prêmios de risco (câmbio, implícita, crédito, ERP) “muito baixos e subestimam sobremaneira” o risco de continuidade da política."),
    ("27/01/2026", "Verde — Stuhlberger, LAIC/UBS", "g", "R$ 4,40", True,
     "Modelo próprio de quatro canais: dólar contra cesta EM + DXY, Selic−Fed Funds, índice de commodities e CDS do Brasil. Gap atribuído ao fiscal. Spot 5,2392."),
    ("26/02/2026", "Legacy — Pedro Jobim", "g", "abaixo de R$ 5,00", True,
     "Avalia o dólar, não o real: caro numa janela de 50 anos, o que faz do real destino natural de fluxo, com carry a favor. Spot 5,1382."),
    ("16/04/2026", "Armor — Alfredo Menezes", "g", "R$ 4,90 (piso)", True,
     "Dois pilares temporários: petróleo perto de US$ 90 (≈US$ 20 bi de superávit extra) e juro real alto. A eleição devolve o foco ao fiscal. Spot 5,0007."),
    ("28/04/2026", "Goldman Sachs", "s", "4,90 · 5,00 · 5,00", True,
     "Projeções de 3, 6 e 12 meses, cortadas de 5,20/5,30/5,30 no meio do rali, com o real como a melhor moeda do ano. Spot 4,9878."),
    ("18/05/2026", "Morgan Stanley", "s", "“justo”; 4,50 com ajuste", True,
     "Prêmio de risco fiscal excedente perto de zero, país negociando em linha com o rating. Os 4,50 valem só no cenário de consolidação. Spot 5,0093."),
    ("1S/2026", "BTG · XP · BofA · BNP", "s", "4,90 · 5,00 · 4,95 · 4,90", True,
     "Todas revisadas para baixo durante o rali do real. Fonte mais fraca desta tabela: resumo de busca, não artigo lido na íntegra."),
    ("05/08/2026", "Focus — BCB", "o", "5,20 (fim de 2026)", True,
     "Mediana de mercado."),
    ("18/08/2026", "Goldman Sachs", "s", "5,20 · 5,10", True,
     "Revisão de volta em quatro meses, para 3 e 6 meses: “o mercado passou a atribuir maior peso à incerteza política”. Spot 5,2043."),
    ("18/08/2026", "Itaú BBA", "s", "5,30 (fim de 2026)", True,
     "Aperto monetário adicional nos Estados Unidos somado à manutenção de prêmios de risco domésticos elevados."),
    ("18/08/2026", "Citi", "s", "sai do real", False,
     "Encerra a posição comprada em real e a substitui pelo rand sul-africano. Risco eleitoral, não valuation."),
    ("ago/2026", "Kinea — carta", "g", "neutra", False,
     "Eleição sem favorito claro e estrangeiro reduzindo exposição “para voltar mais adiante”; exposição neutra ao país até outubro."),
]

TITLE = ParagraphStyle("t", fontName="DejaVuSans-Bold", fontSize=15, leading=18, textColor=NAVY)
SUB = ParagraphStyle("s", fontName="DejaVuSans", fontSize=8.4, leading=11, textColor=MUTED)
BRAND = ParagraphStyle("b", fontName="DejaVuSans-Bold", fontSize=7.6, leading=9,
                       textColor=GOLD, alignment=2)
STAMP = ParagraphStyle("d", fontName="DejaVuSans", fontSize=7.6, leading=9,
                       textColor=MUTED, alignment=2)
TH = ParagraphStyle("th", fontName="DejaVuSans-Bold", fontSize=8.4, leading=10.5,
                    textColor=colors.white)
TD = ParagraphStyle("td", fontName="DejaVuSans", fontSize=8.4, leading=10.5, textColor=INK)
TD_DATE = ParagraphStyle("tdd", fontName="DejaVuSans", fontSize=8.4, leading=10.5, textColor=MUTED)
NOTE = ParagraphStyle("n", fontName="DejaVuSans", fontSize=8.0, leading=10.6,
                      textColor=MUTED, alignment=4)


def _src(name, kind):
    return ParagraphStyle("src_" + kind, parent=TD, fontName="DejaVuSans-Bold",
                          textColor=KIND_COLOR[kind]), name


def build_story(width):
    story = []

    head = Table(
        [[Paragraph("Nível justo do USDBRL", TITLE),
          Paragraph("LIS CAPITAL", BRAND)],
         [Paragraph("O que cada casa nomeou como nível, e com que raciocínio. "
                    "PTAX de venda como referência de spot.", SUB),
          Paragraph("Levantamento de 8 de setembro de 2026", STAMP)]],
        colWidths=[width * 0.66, width * 0.34],
    )
    head.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "BOTTOM"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 3),
        ("BOTTOMPADDING", (0, 1), (-1, 1), 0),
    ]))
    story.append(head)
    story.append(Spacer(1, 4))
    story.append(HRFlowable(width="100%", thickness=1.1, color=NAVY, spaceAfter=6))

    data = [[Paragraph(h, TH) for h in ("Data", "Fonte", "Valor justo", "Lógica")]]
    for date, src, kind, value, has_number, logic in ROWS:
        style, name = _src(src, kind)
        val_style = ParagraphStyle(
            "val_" + kind, parent=TD,
            fontName="DejaVuSans-Bold" if has_number else "DejaVuSans-Oblique",
            textColor=INK if has_number else MUTED,
        )
        data.append([Paragraph(date, TD_DATE), Paragraph(name, style),
                     Paragraph(value, val_style), Paragraph(logic, TD)])

    tbl = Table(data, colWidths=[22 * mm, 42 * mm, 38 * mm, width - 102 * mm], repeatRows=1)
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 3.0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3.0),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("LINEBELOW", (0, 1), (-1, -2), 0.4, LINE),
        ("LINEBELOW", (0, -1), (-1, -1), 0.8, NAVY),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, BAND]),
    ]))
    story.append(tbl)
    story.append(Spacer(1, 6))

    story.append(Paragraph(
        '<b>Como ler.</b> A cor do nome identifica o tipo: '
        '<font color="#BB9B1D"><b>gestora brasileira</b></font>, '
        '<font color="#418791"><b>banco / sell side</b></font>, '
        '<font color="#1F2853"><b>demais</b></font>. Valor em negrito é nível nomeado; em itálico, '
        'postura sem nível — e a distinção é o achado principal: das gestoras brasileiras, só a '
        'Verde publica um número. Os níveis nomeados vão de 4,40 a 5,30, e a distância diz menos '
        'sobre discordância a respeito do Brasil do que sobre o que cada conta responde: valor '
        'justo de conta corrente e prêmio de risco puxa para baixo, projeção de fim de ano com '
        'risco eleitoral puxa para cima.', NOTE))
    story.append(Spacer(1, 3))
    story.append(Paragraph(
        '<b>Procedência.</b> As linhas de Kinea e Kapitalo vêm das cartas das próprias casas '
        '(corpus interno). Todas as demais vêm de reportagem, não de material primário — Brazil '
        'Journal, CNN Brasil e Forbes (27/01); Seu Dinheiro (26/02, 16/04); InfoMoney '
        '(28/04, 18/05, 18/08); Bora Investir/B3 (05/08); Mais Retorno (28/06/2021). '
        'PTAX de venda: <font name="DejaVuSans-Oblique">macro_brasil.cmb_ptax</font>, série do Banco Central, '
        'último dado em 04/09/2026. Detalhe e ressalvas em '
        '<font name="DejaVuSans-Oblique">analytics/brasil/exchange_rate/referencia/literature/fair_value_casas_de_gestao.md</font>.',
        NOTE))
    return story


def run(out_path=OUT_PATH):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    page = landscape(A4)
    doc = SimpleDocTemplate(
        out_path, pagesize=page,
        leftMargin=12 * mm, rightMargin=12 * mm, topMargin=11 * mm, bottomMargin=10 * mm,
        title="Nível justo do USDBRL", author="LIS Capital",
    )
    doc.build(build_story(doc.width))

    import fitz  # a restrição de uma página é o ponto do documento, então é verificada
    with fitz.open(out_path) as pdf:
        n = pdf.page_count
    if n != 1:
        raise SystemExit(
            f"{out_path} saiu com {n} páginas. Encurte a coluna Lógica das linhas mais longas "
            "(~118 caracteres por linha, máximo de duas linhas por célula)."
        )
    print(f"OK, 1 página: {out_path}")
    return out_path


if __name__ == "__main__":
    run()
