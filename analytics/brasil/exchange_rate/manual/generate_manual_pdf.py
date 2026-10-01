"""Guia de leitura do FX Report para envio a cliente -> reports/brasil/cliente/FX Report - Guia de leitura.pdf

Pedido do usuário (2026-09-30): um manual de todas as abas do FX Report, para um cliente
específico, num PDF só. As seis abas de dados e de modelo descritivo são escritas aqui; a aba
FX Model entra como segunda parte, com o guia técnico de `models/generate_model_guide_pdf.py`
(o mesmo conteúdo de `team_materials/exchange_rate/ridge_model_explained.pdf`).

Três decisões que valem para o arquivo inteiro:

1. **As figuras são capturas do arquivo que o cliente recebe** (`reports/brasil/cliente/FX
   Report.html`), tiradas por um Chrome de verdade em `capture_screens.js`. O guia mostra
   exatamente o que o leitor vai ver, inclusive a ausência do bloco em construção, que a versão
   de envio não tem.
2. **A segunda parte é composta, não colada.** `build_story()` do guia técnico entra no mesmo
   documento, com a mesma paginação e o mesmo rodapé. Colar o PDF pronto deixaria duas numerações
   de página dentro do mesmo arquivo. Para não virar outra coisa em silêncio, `run()` confere que
   o texto da segunda parte é o texto do PDF de `team_materials/` página a página, e avisa se
   não for, que é o sinal de que um dos dois precisa ser regerado.
3. **A prosa não afirma número de dado.** Um guia de leitura descreve o que cada controle faz e
   como ler o sinal; o número do mês está na tela, e uma frase que o repetisse envelheceria a cada
   divulgação. A única data impressa é a da versão do relatório, lida do próprio arquivo.

    uv run python -c "from analytics.brasil.exchange_rate.generate_report import run; run(client=True, recipient='<nome>')"
    uv run python -c "from analytics.brasil.exchange_rate.manual.generate_manual_pdf import run; run('<nome>')"
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import tempfile

from PIL import Image as PILImage, ImageDraw, ImageFont
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import (
    BaseDocTemplate,
    CondPageBreak,
    Flowable,
    Frame,
    Image as RLImage,
    KeepTogether,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

from analytics.brasil.exchange_rate.generate_report import client_notice
from analytics.brasil.exchange_rate.models import generate_model_guide_pdf as guide
from analytics.brasil.exchange_rate.models.generate_model_guide_pdf import (
    BG_SOFT, BODY, BULLET, CAP, DATE_BADGE, FOOTER, H2, LINE, MUTED, NAVY, SUBTITLE, TITLE,
    ParagraphStyle, bullets, card, P, rule, section, table,
)

HERE = os.path.dirname(os.path.abspath(__file__))
CLIENT_REPORT = os.path.join("reports", "brasil", "cliente", "FX Report.html")
INTERNAL_REPORT = os.path.join("reports", "brasil", "FX Report.html")  # carries the model payload the guide reads
MODEL_GUIDE_PDF = os.path.join("team_materials", "exchange_rate", "ridge_model_explained.pdf")
OUT_PATH = os.path.join("reports", "brasil", "cliente", "FX Report - Guia de leitura.pdf")

COL_W = 481
_MES = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro",
        "outubro", "novembro", "dezembro"]


# ---------------------------------------------------------------------------
# Screenshots
# ---------------------------------------------------------------------------
def capture(report_path, shots_dir):
    """Runs capture_screens.js against the client report. Needs Chrome and network."""
    os.makedirs(shots_dir, exist_ok=True)
    r = subprocess.run(["node", os.path.join(HERE, "capture_screens.js"), report_path, shots_dir],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        raise RuntimeError("capture_screens.js failed:\n" + r.stdout + r.stderr)
    return shots_dir


def _font(size):
    for name in ("DejaVuSans-Bold.ttf", "arialbd.ttf"):
        try:
            import matplotlib
            p = os.path.join(matplotlib.get_data_path(), "fonts", "ttf", name)
            return ImageFont.truetype(p if os.path.exists(p) else name, size)
        except OSError:
            continue
    return ImageFont.load_default()


def annotate_anatomy(shots_dir):
    """Numbers the controls of the BOP section, from the boxes capture_screens.js measured."""
    with open(os.path.join(shots_dir, "anatomy.json"), encoding="utf-8") as fh:
        A = json.load(fh)
    im = PILImage.open(os.path.join(shots_dir, "anatomy.png")).convert("RGB")
    d = ImageDraw.Draw(im)
    gold, navy = (187, 155, 29), (31, 40, 83)
    ctrl_right = A["expand"]["x"] + A["expand"]["w"] * 2.25  # both buttons, not the empty rest of the bar
    marks = [
        (1, (A["ctrl"]["x"] + 2, A["ctrl"]["y"] - 2, ctrl_right, A["ctrl"]["y"] + A["ctrl"]["h"] + 2)),
        (2, (A["checkbox"]["x"] - 4, A["checkbox"]["y"] - 4, A["checkbox"]["x"] + A["checkbox"]["w"] + 4,
             A["checkbox"]["y"] + A["checkbox"]["h"] + 4)),
        (3, (A["caret"]["x"] - 3, A["caret"]["y"] - 2, A["caret"]["x"] + A["caret"]["w"] + 3,
             A["caret"]["y"] + A["caret"]["h"] + 2)),
        (4, (A["info"]["x"] - 4, A["info"]["y"] - 4, A["info"]["x"] + A["info"]["w"] + 4,
             A["info"]["y"] + A["info"]["h"] + 4)),
        (5, (A["head"]["x"], A["head"]["y"], A["head"]["x"] + A["head"]["w"] * 0.55, A["head"]["y"] + A["head"]["h"])),
        (6, (A["range"]["x"] + 4, A["range"]["y"] - 3, A["range"]["x"] + 330, A["range"]["y"] + A["range"]["h"] + 3)),
    ]
    f = _font(22)
    r = 17
    gutter = 2 * r + 20          # badges 2 and 3 sit in a margin left of the table, not over the labels
    for n, (x0, y0, x1, y1) in marks:
        d.rounded_rectangle((x0, y0, x1, y1), radius=6, outline=gold, width=4)
    badges = []
    for n, (x0, y0, x1, y1) in marks:
        cy = y0 + (y1 - y0) / 2
        if n in (2, 3):
            badges.append((n, -gutter / 2 - 2, cy, x0))  # x in gutter coordinates, leader line to x0
        else:
            badges.append((n, x1 + r + (10 if n == 5 else 6), cy, None))

    # Crop: controls + table + chart header, then the range ruler strip, so the picture can be
    # printed at full column width instead of being shrunk to fit the empty plot area.
    top_end = int(A["head"]["y"] + A["head"]["h"] + 24)
    strip0, strip1 = int(A["range"]["y"] - 14), int(A["range"]["y"] + A["range"]["h"] + 14)
    gap = 26
    W = im.width + gutter
    out_im = PILImage.new("RGB", (W, top_end + gap + (strip1 - strip0)), (255, 255, 255))
    out_im.paste(im.crop((0, 0, im.width, top_end)), (gutter, 0))
    out_im.paste(im.crop((0, strip0, im.width, strip1)), (gutter, top_end + gap))
    d2 = ImageDraw.Draw(out_im)
    yc = top_end + gap / 2
    for k in range(gutter + 20, W - 20, 28):  # dashed cut line: the plot in between is left out
        d2.line((k, yc, k + 14, yc), fill=(170, 176, 190), width=2)
    for n, cx, cy, lead_to in badges:
        cx += gutter
        if n == 6:
            cy = cy - strip0 + top_end + gap
        if lead_to is not None:
            d2.line((cx + r, cy, lead_to + gutter - 5, cy), fill=gold, width=3)
        d2.ellipse((cx - r, cy - r, cx + r, cy + r), fill=navy, outline=(255, 255, 255), width=3)
        d2.text((cx, cy), str(n), fill=(255, 255, 255), font=f, anchor="mm")
    out = os.path.join(shots_dir, "anatomy_annotated.png")
    out_im.save(out)
    return out


def shot(shots_dir, name, caption, max_h=330):
    """One screenshot at column width, framed, with its caption. JPEG to keep the file small."""
    src = name if os.path.isabs(name) else os.path.join(shots_dir, name + ".png")
    im = PILImage.open(src).convert("RGB")
    jpg = os.path.splitext(src)[0] + ".jpg"
    im.save(jpg, quality=86, optimize=True)
    w, h = im.size
    width = COL_W - 2
    height = width * h / w
    if height > max_h:
        width, height = width * max_h / height, max_h
    t = Table([[RLImage(jpg, width=width, height=height)]], colWidths=[COL_W])
    t.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 0.6, LINE), ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                           ("TOPPADDING", (0, 0), (-1, -1), 0), ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
                           ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0)]))
    return KeepTogether([t, Paragraph(caption, CAP)])


# ---------------------------------------------------------------------------
# Small layout helpers
# ---------------------------------------------------------------------------
H3 = ParagraphStyle("H3", parent=H2, fontSize=9.6, leading=12, spaceBefore=6, spaceAfter=3)
NUM = ParagraphStyle("Num", parent=BODY, leftIndent=18, firstLineIndent=-18, spaceAfter=3)


def numbered(items):
    return [Paragraph('<font color="#1F2853"><b>%d</b></font>&nbsp;&nbsp;&nbsp;%s' % (i + 1, t), NUM)
            for i, t in enumerate(items)]


def how_to_read(lines):
    return card("Como ler", lines)


class _Part(Flowable):
    """Zero-size marker: from the page it lands on, the footer names the second part."""

    def __init__(self, label):
        super().__init__()
        self.label = label

    def wrap(self, *a):
        return 0, 0

    def draw(self):
        self.canv._lis_part = self.label


_NOTICE = [None]  # the confidentiality line, set by run(); printed on every page


def _footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("DejaVuSans", 7.6)
    canvas.setFillColor(MUTED)
    part = getattr(canvas, "_lis_part", None)
    label = "LIS Capital — FX Report: guia de leitura" + (" · " + part if part else "")
    canvas.drawCentredString(A4[0] / 2, 12 * mm, "%s · página %d" % (label, doc.page))
    if _NOTICE[0]:
        canvas.setFont("DejaVuSans", 6.8)
        canvas.drawCentredString(A4[0] / 2, 8.5 * mm, _NOTICE[0])
    canvas.restoreState()


def _generated_at(report_path):
    with open(report_path, encoding="utf-8") as fh:
        s = fh.read()
    m = re.search(r'"generated_at":\s*"([^"]+)"', s)
    return m.group(1) if m else None


# ---------------------------------------------------------------------------
# Content
# ---------------------------------------------------------------------------
NOTICE_BOX = ParagraphStyle("Notice", parent=BODY, fontSize=8.6, leading=12, alignment=1,
                            textColor=colors.HexColor("#5A4A0C"))


def notice_box(text):
    t = Table([[Paragraph(text, NOTICE_BOX)]], colWidths=[COL_W])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F4F1E4")),
                           ("BOX", (0, 0), (-1, -1), 0.6, colors.HexColor("#E2D7A8")),
                           ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
    return t


def story_part1(S, generated_at, with_model, notice=None):
    st = []
    dia, mes, ano = generated_at.split(" ")[0].split("/")
    st += [
        Paragraph('<font color="#BB9B1D"><b>LIS CAPITAL</b></font>', ParagraphStyle("k", parent=SUBTITLE, fontSize=9)),
        Paragraph("FX Report — guia de leitura", TITLE),
        Paragraph("Como ler e usar cada aba do Panorama Cambial", SUBTITLE),
        Paragraph("%s de %s · referente à versão do relatório gerada em %s" % (_MES[int(mes) - 1], ano, generated_at),
                  DATE_BADGE),
        rule(color=NAVY, thickness=1.2, space_before=6, space_after=10),
    ]
    if notice:
        st += [notice_box(notice), Spacer(1, 10)]
    st += [
        P("O FX Report reúne num arquivo só os dados que explicam o real: quanto dólar entra e sai do país "
          "e por qual canal, quem está posicionado em câmbio e em que direção, se a moeda está cara ou barata, "
          "e a que fatores os gestores de recursos atribuem os seus movimentos. Este guia percorre as abas "
          "na ordem em que aparecem e, para cada uma, diz que pergunta ela responde, como ler o gráfico e o que "
          "cada controle faz."),
        P("O relatório é um único arquivo HTML: abre em qualquer navegador, sem instalação e sem acesso a "
          "sistema nenhum. A biblioteca que desenha os gráficos e as fontes tipográficas são carregadas da "
          "internet, então é preciso estar conectado para vê-lo. Os dados são os da data de geração; o arquivo "
          "não se atualiza sozinho."),
        P("A seção 1 trata do que vale para o relatório inteiro: a anatomia de uma seção, a convenção de sinal, "
          "a agregação e o “% do PIB”. As seções 2 a 7 tratam de uma aba cada. "
          + ("A aba FX Model, que é um modelo estimado e não uma leitura de dados, tem um guia técnico próprio, "
             "reproduzido na segunda parte deste documento com numeração de seções própria."
             if with_model else
             "A aba FX Model, que é um modelo estimado e não uma leitura de dados, tem um guia técnico próprio.")),
        Spacer(1, 4),
        table([
            ["Aba", "Pergunta que responde", "Frequência"],
            ["Balanço de Pagamentos", "Como o país fecha as contas com o exterior: comércio, renda e capital", "mensal"],
            ["Fluxo Cambial", "Quanto dólar de fato entrou e saiu pelo mercado de câmbio, e por qual canal",
             "diária, somada em meses"],
            ["Posicionamento: BCB e mercado", "Quem está exposto a câmbio e em que direção: o Banco Central e os "
             "participantes do futuro de real em Chicago", "mensal e semanal"],
            ["Valuation", "Se o real está caro ou barato: o preço, o câmbio real contra parceiros e os termos de troca",
             "diária e mensal"],
            ["Equilíbrio PPP", "Onde estaria o câmbio se tivesse acompanhado só a diferença de inflação entre "
             "Brasil e EUA", "mensal"],
            ["FX Attribution", "A que fatores gestores de recursos atribuem, mês a mês, os movimentos do real", "mensal"],
            ["FX Model", "Que caminho do câmbio é coerente com um caminho para os seus fatores" +
             (" (segunda parte)" if with_model else ""), "mensal"],
        ], col_widths=[118, 283, 80], align_right_from=-1),
        Spacer(1, 6),
        P("As três abas de modelo — Equilíbrio PPP, FX Attribution e FX Model — estão em inglês, e as abas de "
          "dados em português. O guia usa os rótulos exatamente como aparecem na tela.",
          ParagraphStyle("n", parent=BODY, textColor=MUTED, fontSize=8.6, leading=12)),
    ]

    # ---- 1. Common conventions --------------------------------------------------------
    st += [CondPageBreak(300)] + section(1, "Como o relatório funciona", "O que vale para todas as abas")
    st += [
        P("As quatro abas de dados seguem o mesmo desenho: cada seção tem uma nota curta sobre a fonte, uma "
          "tabela com os valores mais recentes e, logo abaixo, o gráfico da série inteira. A tabela e o gráfico "
          "estão ligados — o que se marca na tabela é o que se vê no gráfico."),
        shot(S, annotate_anatomy(S),
             "Figura 1 — A primeira seção da aba Balanço de Pagamentos, com o cartão de definição da Conta "
             "Corrente aberto. O gráfico foi cortado na linha tracejada, para mostrar a régua de período que fica "
             "abaixo dele. Os números indicam os controles descritos a seguir.", max_h=620),
    ]
    st += numbered([
        "<b>Controles do gráfico.</b> <i>Agregação</i> escolhe a janela de cada ponto (mês, trimestre, ano ou "
        "12 meses acumulados); <i>Unidade</i> alterna entre dólares e % do PIB, onde faz sentido; <i>Gráfico</i> "
        "alterna entre barras empilhadas e linhas. <i>Expandir Tudo</i> e <i>Recolher Tudo</i> abrem e fecham a "
        "árvore inteira. Os controles valem só para a seção em que estão.",
        "<b>Caixa de marcação.</b> Cada linha marcada vira uma série no gráfico. A cor ao lado do nome é a cor "
        "da série na legenda.",
        "<b>Seta.</b> Abre os componentes da linha. A tabela é uma árvore: cada linha é a soma das que estão "
        "recuadas abaixo dela.",
        "<b>Botão i.</b> Abre um cartão com o nome oficial da série na fonte, o que ela mede e em que unidade "
        "está. Passar o mouse abre; clicar fixa o cartão para leitura; Esc ou um clique fora fecham.",
        "<b>Cabeçalho do gráfico.</b> Três linhas: o título; o que está plotado, em que frequência, unidade e "
        "tipo de gráfico; e a fonte com o período coberto. Ele é refeito a cada mudança de controle, então uma "
        "captura de tela do gráfico se explica sozinha, longe do relatório.",
        "<b>Régua de período.</b> 1a, 3a, 5a, 10a e Tudo ajustam a janela visível do gráfico. A escala vertical "
        "se reajusta ao que ficou na tela.",
    ])
    st += [
        P("A tabela mostra os doze períodos mais recentes da agregação escolhida — doze meses, doze trimestres ou "
          "doze anos —, e o gráfico mostra a série inteira. Para ver um valor antigo com precisão, passe o mouse "
          "sobre o gráfico."),
        Paragraph("Navegar nos gráficos", H3),
    ]
    st += bullets([
        "<b>Rolar</b> a roda do mouse (ou pinçar no trackpad) dá zoom nos dois eixos, centrado no cursor.",
        "<b>Arrastar</b> move o gráfico, nos dois eixos.",
        "<b>Duplo clique</b> volta à série inteira.",
        "<b>Clicar num item da legenda</b> esconde ou mostra aquela série; duplo clique no item isola a série.",
        "<b>Passar o mouse</b> mostra o valor de cada série naquela data.",
    ])
    st += [Paragraph("Convenção de sinal", H3),
           P("No Balanço de Pagamentos e no Fluxo Cambial vale uma regra só: <b>positivo é entrada de dólar no país, "
             "negativo é saída</b>. Para isso, alguns itens aparecem com o sinal trocado em relação à publicação "
             "do Banco Central: do lado dos ativos da Conta Financeira, um brasileiro investindo lá fora ou o "
             "Banco Central acumulando reservas aparecem como negativo, porque são dólares que saem do mercado "
             "doméstico. Importações e vendas aparecem já negativas, marcadas “(saída)”, para somarem ao saldo "
             "da linha de cima. Onde a grandeza não é um fluxo, o sinal tem leitura própria:"),
           table([
               ["Onde", "Positivo significa"],
               ["Balanço de Pagamentos, Fluxo Cambial", "entrada de dólares no país"],
               ["Intervenções cambiais", "o Banco Central comprou dólares (retirou do mercado)"],
               ["Swap cambial do BCB", "negativo: o Banco Central está vendido em dólar via swap"],
               ["Futuro de real na CME (CFTC)", "comprado em real, isto é, aposta em apreciação"],
               ["Desvio do equilíbrio PPP", "real mais fraco do que a paridade de inflação indica"],
               ["FX Attribution", "a narrativa do gestor é favorável ao real"],
           ], col_widths=[170, 311], align_right_from=-1),
           Spacer(1, 6),
           Paragraph("Barras empilhadas e linhas", H3),
           P("Em <i>Barras empilhadas</i>, uma linha marcada que tenha algum componente também marcado é desenhada "
             "como <b>linha</b>, por cima da pilha — ela é o total daquilo que está empilhado, e desenhá-la como "
             "barra contaria o mesmo valor duas vezes. Marcar a Conta Corrente e os seus três componentes, como na "
             "figura 1, dá a leitura “componentes em barra, total em linha”. Em <i>Linhas</i>, toda série vira "
             "linha. Onde as partes não somam um total, a seção não oferece barras empilhadas."),
           Paragraph("Agregação, fluxo e estoque", H3),
           P("Um <b>fluxo</b> — exportações, câmbio contratado, intervenções — é somado dentro da janela: o valor "
             "trimestral é a soma dos três meses, e <i>12m Acumulado</i> é a soma dos doze meses até cada data, "
             "que é a janela usual para comparar com o ano anterior sem sazonalidade. Um <b>estoque</b> — reservas, "
             "posição em swap — não se soma: ali a agregação se chama <i>Fim do mês</i>, <i>Fim do trimestre</i> "
             "e <i>Fim do ano</i>, e o valor é o saldo no fim da janela."),
           P("<b>Período incompleto sai em branco.</b> Um trimestre com dois meses ou um ano com sete não é "
             "mostrado: a soma parcial se leria como queda. Pela mesma razão, nas séries diárias somadas em meses "
             "o mês corrente só aparece quando fecha."),
           Paragraph("% do PIB", H3),
           P("Para um fluxo, o valor da janela é dividido pelo PIB em dólares somado <b>na mesma janela</b>: em "
             "<i>12m Acumulado</i>, a Conta Corrente em % do PIB é a medida usual de déficit externo. Para um "
             "estoque, a divisão é sempre pelo PIB dos <b>doze meses</b> encerrados naquele mês, que é a forma "
             "usual de medir adequação de reservas; por isso ali o número não muda de escala quando se troca a "
             "agregação."),
           ]

    # ---- 2. BOP -----------------------------------------------------------------------
    st += [PageBreak()] + section(2, "Balanço de Pagamentos", "As contas do país com o exterior, e o comércio de bens aberto por país, categoria e produto")
    st += [
        Paragraph("Balanço de Pagamentos — Árvore Completa", H3),
        P("A árvore segue o manual do FMI (BPM6), na ordem em que ele apresenta as contas. No topo estão "
          "quatro linhas:"),
    ]
    st += bullets([
        "<b>Conta Corrente</b> — tudo o que o país transaciona com o exterior sem criar nem quitar dívida: "
        "<i>Bens e Serviços</i> (a balança de bens, com mercadorias, ouro não monetário e <i>merchanting</i>, e a de "
        "serviços, com viagens, transportes, aluguel de equipamentos e demais), <i>Renda Primária</i> (juros, "
        "lucros e dividendos e remuneração de empregados) e <i>Renda Secundária</i> (transferências).",
        "<b>Conta Capital</b> — transferências de capital; é pequena.",
        "<b>Conta Financeira</b> — como o resultado corrente é financiado. Os dois lados, <i>Ativos</i> (o que "
        "residentes aplicam lá fora) e <i>Passivos</i> (o que não residentes aplicam aqui), abrem nas mesmas três "
        "categorias — investimento direto, investimento em carteira e outros investimentos —, para que um lado "
        "possa ser lido contra o outro no mesmo nível. O detalhe por prazo e por mercado (títulos no mercado "
        "doméstico e no externo, empréstimos de curto e longo prazo) fica um nível abaixo. Derivativos e Ativos "
        "de Reserva completam a conta.",
        "<b>Erros e Omissões</b> — não é conta: é o item que fecha a identidade.",
    ])
    st += [
        P("Com a convenção de sinal do relatório, <b>as quatro linhas de topo somam zero em todo mês</b>. É a "
          "identidade do balanço de pagamentos, e a tabela permite conferi-la coluna a coluna. Um déficit em Conta "
          "Corrente (negativo) aparece, portanto, como um valor positivo de mesma ordem na Conta Financeira."),
        shot(S, "bop_tree", "Figura 2 — Conta Corrente aberta nos três componentes, em barras empilhadas, com o "
             "total em linha."),
        how_to_read([
            "Para o câmbio, o saldo corrente importa menos que a qualidade do seu financiamento. Abra a Conta "
            "Financeira em Passivos e compare <i>Investimento Direto no País</i>, que é estável e de longo prazo, "
            "com <i>Investimento em Carteira</i>, que entra e sai com o humor do mercado.",
            "Use <i>12m Acumulado</i> e <i>% do PIB</i> juntos para comparar anos diferentes: tira a sazonalidade "
            "e o efeito do tamanho da economia.",
            "<i>Lucros e Dividendos</i> inclui lucros reinvestidos, série que o Banco Central não publica para "
            "1999–2009; nesses anos o agregado pode estar levemente subestimado.",
        ]),
        Paragraph("Comex Stat — três recortes da balança de bens", H3),
        P("As três seções seguintes vêm de outra fonte, o Comex Stat do Ministério do Desenvolvimento, que usa o "
          "registro aduaneiro (“comércio geral”) e não a metodologia do balanço de pagamentos. Por isso o total "
          "delas <b>não fecha exatamente</b> com o ramo Balança de Bens da árvore acima: são recortes "
          "complementares, não uma decomposição dela. O que elas acrescentam é abrir exportação e importação "
          "separadas — expanda qualquer item para ver os dois lados. Estão sempre em dólares, sem % do PIB."),
    ]
    st += bullets([
        "<b>Por país parceiro</b> — os quatro maiores parceiros por comércio total em 2025 e “Demais Países”, "
        "que é o resíduo (mundo menos os quatro).",
        "<b>Por fator agregado</b> — Básicos (commodities como soja, minério e petróleo), Semimanufaturados, "
        "Manufaturados e Demais. Aqui as quatro categorias somam exatamente o total.",
        "<b>Por produto</b> — os cinco maiores produtos de exportação em 2025 e “Demais Produtos”, o resíduo.",
    ])
    st += [shot(S, "comex_fator", "Figura 3 — Balança de bens por fator agregado: o saldo positivo de básicos contra o "
                "negativo de manufaturados.")]

    # ---- 3. Flow ----------------------------------------------------------------------
    st += [PageBreak()] + section(3, "Fluxo Cambial", "O dólar que de fato passa pelo mercado de câmbio")
    st += [
        P("O balanço de pagamentos registra transações; o fluxo cambial registra câmbio: a troca de reais por "
          "dólares contratada entre bancos e clientes. As duas medidas diferem no tempo e na cobertura — um "
          "exportador que embarca e mantém a receita lá fora aparece no balanço e não no fluxo, e um adiantamento "
          "de exportação aparece no fluxo antes de o bem ser embarcado. Para a pressão sobre a moeda no "
          "curto prazo, o fluxo é a medida mais direta."),
        Paragraph("Câmbio Contratado — Fluxo entre Bancos e Clientes", H3),
        P("A árvore tem quatro níveis e fecha exatamente na fonte:"),
    ]
    st += bullets([
        "<b>Saldo Total</b> = Saldo Comercial + Saldo Financeiro.",
        "<b>Saldo Comercial</b> = Exportação de Bens − Importação de Bens. A exportação abre em <i>ACC</i> "
        "(adiantamento de contrato de câmbio: o exportador contrata o câmbio antes de embarcar), <i>PA</i> "
        "(pagamento antecipado pelo importador estrangeiro) e demais.",
        "<b>Saldo Financeiro</b> = Compras − Vendas de moeda por motivo financeiro: investimentos, remessas de "
        "lucro, pagamentos de dívida, serviços e rendas.",
    ])
    st += [
        P("A fonte é diária desde setembro de 2008 e é somada em meses; o mês em curso não aparece até fechar."),
        shot(S, "flow_contratado", "Figura 4 — Câmbio contratado: saldo comercial e financeiro em barras, saldo "
             "total em linha."),
        Paragraph("Câmbio Contratado — Financeiro Detalhado", H3),
        P("Abre o saldo financeiro por natureza da operação: Serviços, Rendas Primária e Secundária, Capitais "
          "Brasileiros e Capitais Estrangeiros. Vem de outra tabela do Banco Central, mensal na fonte: o saldo "
          "agregado tem histórico desde 1982, e as quatro linhas de detalhe só desde 2011, por isso as colunas "
          "anteriores ficam em branco. O saldo desta seção e o da seção anterior medem a mesma coisa em tabelas "
          "diferentes e podem divergir por arredondamento e revisão."),
        Paragraph("Volume Interbancário de Câmbio", H3),
        P("Volume negociado entre bancos, por prazo de liquidação (T+1 e T+2). Mede <b>atividade e liquidez</b>, "
          "não direção: todo negócio tem um comprador e um vendedor, então este número nunca diz se entrou ou saiu "
          "dólar. Volume alto com o câmbio andando indica convicção; volume baixo, um mercado mais fácil de "
          "deslocar."),
        how_to_read([
            "O saldo financeiro costuma ser negativo em dezembro, quando empresas remetem lucros e dividendos: "
            "compare o mesmo mês de anos diferentes antes de ler um mês ruim como fuga.",
            "Para tendência, use <i>12m Acumulado</i>; o mensal é ruidoso.",
        ]),
    ]

    # ---- 4. Positioning ---------------------------------------------------------------
    st += [PageBreak()] + section(4, "Posicionamento: BCB e mercado",
                                  "Quem está exposto a câmbio: o Banco Central de um lado, o mercado futuro do outro")
    st += [
        P("As três primeiras seções mostram a exposição do Banco Central — o que ele tem em reservas, o que ele "
          "ofereceu de proteção cambial por swaps e quanto ele comprou ou vendeu à vista. A última mostra a "
          "exposição dos participantes do mercado futuro de real em Chicago."),
        Paragraph("Composição das Reservas", H3),
        P("As reservas internacionais abertas no formato do FMI: <i>Moeda Estrangeira</i> (títulos, e moeda e "
          "depósitos), <i>Ouro</i>, <i>DES</i> (Direitos Especiais de Saque, a moeda-cesta do FMI), <i>Posição de "
          "Reservas no FMI</i> e <i>Outros Ativos de Reserva</i> (compromissadas reversas, empréstimos a não "
          "residentes e derivativos, que podem ficar negativos por serem posição líquida). A decomposição começa "
          "em janeiro de 2001; a linha do total vai até 1971."),
        P("É estoque: a agregação é o saldo no fim do período, e o % do PIB é contra o PIB de doze meses. Uma "
          "variação do ouro em dólares é, na maior parte, preço do metal, e não compra ou venda."),
        shot(S, "bcb_reserves", "Figura 5 — Composição das reservas internacionais, fim de mês."),
        Paragraph("Posição Cambial — BCB e Bancos", H3),
        P("A exposição do Banco Central fora das reservas e a dos bancos:"),
    ]
    st += bullets([
        "<b>Swap Cambial do BCB</b> — negativo quando o Banco Central está vendido em dólar via swap. É uma "
        "intervenção sintética: oferece proteção contra alta do dólar, liquidada em reais, sem gastar reserva.",
        "<b>Linhas e Empréstimos em ME</b> — o estoque de linhas de recompra e empréstimos em moeda estrangeira.",
        "<b>Demais Ativos e Passivos em ME</b> — o restante da exposição em moeda estrangeira do balanço do BCB.",
        "<b>Posição de Câmbio dos Bancos</b> — a posição à vista dos bancos, que é a contraparte do mercado.",
    ])
    st += [
        P("A tabela é plana e o gráfico só tem linhas: a fonte não publica um total dessas quatro exposições, e "
          "empilhá-las inventaria um agregado que não existe. As três linhas do BCB começam em 2008; a dos bancos, "
          "em 1994."),
        Paragraph("Intervenções Cambiais", H3),
        P("Intervenções líquidas liquidadas, por instrumento — mercado à vista, contratos a termo, empréstimos e "
          "recompras em moeda estrangeira, linhas de recompra. <b>Positivo é o Banco Central comprando dólar</b>, "
          "negativo, vendendo. A fonte registra só os dias com intervenção, então um mês vazio é intervenção "
          "zero, e não dado faltante. Entre 2013 e 2018 o mercado à vista aparece zerado porque o Banco Central "
          "atuou por swap, que está na seção anterior."),
        Paragraph("Posicionamento no Futuro de Real — CFTC (CME)", H3),
        P("A CFTC, reguladora americana de derivativos, publica toda semana a posição de cada grupo de "
          "participantes no contrato futuro de real da bolsa de Chicago, em cinco grupos: <i>Dealer / "
          "Intermediário</i>, <i>Asset Manager / Institucional</i>, <i>Fundos Alavancados</i>, <i>Outros "
          "Reportáveis</i> e <i>Não-Reportáveis</i>. O contrato é cotado em dólares por real, então <b>positivo é "
          "comprado em real</b>."),
        shot(S, "bcb_cot", "Figura 6 — Posição líquida dos cinco grupos, em contratos."),
        how_to_read([
            "<b>As cinco posições líquidas somam zero</b>, porque todo contrato futuro tem um comprado e um vendido. "
            "A pilha mostra, portanto, quem está do outro lado de quem: quando os fundos alavancados compram real, "
            "algum outro grupo vende.",
            "O “posicionamento especulativo” de que se costuma falar são só os Fundos Alavancados, e eles não são "
            "o maior grupo do contrato. Leia os cinco antes de concluir sobre o mercado.",
            "O <i>Open Interest</i> é o tamanho do mercado, não a soma das posições. Ele fica numa pilha própria, "
            "ao lado, e diz se um movimento veio de dinheiro novo entrando no contrato ou de uma troca de mãos "
            "com o mercado do mesmo tamanho.",
            "<i>Média móvel</i> de 12 ou 24 semanas suaviza o ruído semanal. Onde falhas antigas da série "
            "esticariam a janela, a média sai em branco em vez de fingir que cobre o período — isso só acontece "
            "antes de 2016.",
            "Os dados têm data de terça-feira e são publicados na sexta seguinte. Cobrem só o real negociado em "
            "Chicago, e não o dólar futuro da B3, que é o mercado maior.",
        ]),
    ]

    # ---- 5. Valuation -----------------------------------------------------------------
    st += [PageBreak()] + section(5, "Valuation", "O preço e as duas réguas contra as quais ele é lido")
    st += [
        Paragraph("PTAX — Câmbio à Vista", H3),
        P("A taxa de referência do Banco Central para o dólar, na ponta de venda: a média das cotações do "
          "mercado interbancário em quatro janelas do dia, usada em contratos e balanços. Está em reais por dólar, "
          "então <b>subir é o real enfraquecer</b>. É o nível contra o qual as outras duas seções são lidas."),
        Paragraph("Taxa de Câmbio Efetiva Real — BIS", H3),
        P("O câmbio contra uma cesta ampla de parceiros comerciais, ponderada pelo comércio e ajustada pela "
          "inflação de cada parceiro, calculado pelo Banco de Compensações Internacionais. Índice com 2020 = 100: "
          "<b>acima de 100, a moeda está mais apreciada</b> em termos reais do que em 2020. O Brasil aparece ao "
          "lado de México, Chile e Colômbia."),
        shot(S, "val_reer", "Figura 7 — Câmbio efetivo real do Brasil e de três pares latino-americanos."),
        how_to_read([
            "Cada índice é relativo ao seu próprio 2020, então o gráfico compara <b>trajetórias</b>, não níveis: "
            "ele diz se o real se apreciou mais ou menos que o peso mexicano desde 2020, e não qual das duas moedas "
            "está mais cara.",
            "Um movimento comum aos quatro países é regional ou global; um movimento só do Brasil é doméstico.",
        ]),
        Paragraph("Termos de Troca", H3),
        P("O preço médio do que o Brasil exporta dividido pelo preço médio do que importa, calculado pela Funcex, "
          "índice com média de 2018 = 100. Uma alta significa que a mesma quantidade exportada paga mais "
          "importações; tende a melhorar a balança comercial e a se associar a câmbio real mais apreciado."),
    ]

    # ---- 6. PPP -----------------------------------------------------------------------
    st += [PageBreak()] + section(6, "Equilíbrio PPP", "Onde estaria o câmbio se tivesse acompanhado só a inflação")
    st += [
        P("A paridade de poder de compra relativa diz que, no longo prazo, o câmbio acompanha a diferença de "
          "inflação entre os dois países: se o Brasil inflaciona 3 pontos a mais que os EUA num ano, o dólar "
          "deveria valer cerca de 3% mais reais no fim dele. A aba desenha esse caminho e mede a distância do "
          "câmbio observado até ele."),
        guide.equation_block([
            ("equilíbrio(t) = PTAX(b) × [IPCA(t)/IPCA(b)] ÷ [CPI(t)/CPI(b)]",
             "parte da PTAX de um mês-base b e a corrige pela inflação acumulada de cada país desde então"),
            ("desvio(t) = 100 × ln(PTAX(t) / equilíbrio(t))",
             "em %: positivo é o real mais fraco do que a paridade indica"),
        ], left=250),
        Spacer(1, 8),
        P("O IPCA e o CPI são os índices cheios de cada país. A PTAX é a do fim de cada mês."),
        Paragraph("Controles", H3),
    ]
    st += bullets([
        "<b>Base month</b> escolhe o mês-base b, em que o equilíbrio é forçado a coincidir com o câmbio "
        "observado. <b>Reset to Jul/1994</b> volta ao início do Plano Real, que é o padrão.",
        "Os três cartões mostram o desvio mais recente, o maior e o menor da série, com as datas, para a base "
        "escolhida.",
        "<b>Dados no gráfico</b>, no canto de cada gráfico, escreve os valores sobre a linha.",
    ])
    st += [
        shot(S, "ppp_controls", "Figura 8 — Seletor do mês-base e os três cartões de desvio.", max_h=150),
        shot(S, "ppp_dev", "Figura 9 — Desvio do câmbio observado em relação ao equilíbrio de PPP."),
        how_to_read([
            "<b>O nível do desvio depende da base.</b> No mês-base o desvio é zero por construção, então trocar a "
            "base desloca a curva inteira para cima ou para baixo. O que não depende da base é a forma: quando o "
            "real se afastou do equilíbrio, quanto e por quanto tempo. Escolha como base um mês em que você "
            "considere o câmbio perto do equilíbrio, e compare hoje com o histórico sempre na mesma base.",
            "Desvios da paridade duram anos. Esta é uma âncora de longo prazo, não um sinal para o mês seguinte. "
            "O modelo da aba FX Model usa a mesma diferença de inflação como tendência, e é lá que ela é combinada "
            "com os fatores de curto prazo.",
        ]),
    ]

    # ---- 7. FX Attribution ------------------------------------------------------------
    st += [PageBreak()] + section(7, "FX Attribution", "O que os gestores de recursos dizem que move o real")
    st += [
        P("A aba transforma o comentário sobre câmbio das cartas mensais de gestores de recursos em números. Cada "
          "vez que uma carta liga explicitamente uma causa a um movimento do real, essa afirmação é classificada "
          "numa de nove categorias fixas e recebe uma nota de −1 a +1 pelo efeito que o gestor atribui <b>sobre o "
          "real</b>: +1 é fortemente favorável à apreciação, −1 fortemente a favor da depreciação. Uma frase como "
          "“o dólar se fortalece globalmente” recebe nota negativa, porque é ruim para o real. As notas são então "
          "somadas por categoria e por mês."),
        table([
            ["Categoria", "O que entra"],
            ["Fiscal (Brasil)", "trajetória de dívida e déficit, medidas de gasto e receita, regra fiscal"],
            ["Monetary policy / rate differential", "Selic, comunicação do Banco Central, diferencial de juros"],
            ["Politics / idiosyncratic (Brasil)", "eleições, Congresso, decisões judiciais, imprevisibilidade política"],
            ["Global USD / DXY", "força ou fraqueza do dólar vinda do lado americano: Fed, fiscal e política dos EUA"],
            ["Commodities / terms of trade / external accounts",
             "preços de minério, soja, petróleo e energia, e as contas externas que eles movem"],
            ["Global risk sentiment", "apetite a risco global, fuga para ativos seguros"],
            ["China / EM growth", "crescimento e estímulo na China como demanda por commodities e humor emergente"],
            ["Trade policy / tariffs", "tarifas e ações comerciais diretas"],
            ["Capital flows / positioning", "afirmações sobre fluxo e posicionamento, e não sobre fundamentos"],
        ], col_widths=[176, 305], align_right_from=-1),
        Spacer(1, 6),
        Paragraph("O que conta como afirmação", H3),
    ]
    st += bullets([
        "O próprio gestor tem de ligar a causa ao câmbio. Discutir um tema que, pela teoria, afetaria o real não "
        "basta: a aba mede o que os gestores atribuem, e não o que a teoria diria.",
        "O câmbio tem de ser o efeito. Uma carta que cita a alta do dólar como causa de outra coisa, como a "
        "inflação, não conta.",
        "Uma posição sem motivo declarado não é atribuição: “estamos comprados em real” só conta se vier com o "
        "porquê.",
        "Cada argumento conta uma vez por carta, mesmo que seja repetido. Argumentos opostos na mesma carta — o "
        "dólar caiu este mês, mas deve subir à frente — contam separados.",
        "A nota pode ser zero de propósito, quando o gestor diz que um fator <i>não</i> moveu a moeda.",
    ])
    st += [
        Paragraph("Controles e gráficos", H3),
    ]
    st += bullets([
        "<b>Seletor de gestor</b> (Kapitalo, Kinea, Verde Asset). Cada gestor tem a sua própria extração, com "
        "cobertura e densidade diferentes; os cartões mostram quantos meses, quantas cartas e quantas afirmações "
        "por carta. Um número menor de afirmações reflete o estilo de escrita da casa, e não que ela se preocupe "
        "menos com câmbio.",
        "<b>Quarterly</b> troca a média móvel de três meses pela soma do trimestre, nos dois gráficos.",
        "<b>Directional Relevance</b> — a nota com sinal, média de três meses, empilhada por categoria, com o total "
        "em linha tracejada. Acima de zero, a narrativa do período é favorável ao real.",
        "<b>Grau de relevância</b> — a participação de cada categoria no total das notas em valor absoluto, em "
        "100%. Mostra quais temas dominam o comentário, independentemente da direção.",
        "<b>Tabela de afirmações</b> — cada afirmação extraída, da mais recente para a mais antiga, com o mês que "
        "a carta cobre, a data de publicação, a categoria, a nota e o trecho original da carta. O filtro de "
        "categoria restringe a tabela.",
    ])
    st += [
        shot(S, "fxattr_dir", "Figura 10 — Directional Relevance de um gestor: notas com sinal por categoria e o "
             "total."),
        shot(S, "fxattr_claims", "Figura 11 — A tabela de afirmações, com o trecho de cada carta.", max_h=260),
        how_to_read([
            "<b>Zero pode ser silêncio ou empate.</b> Um mês sem nenhuma afirmação e um mês com duas afirmações "
            "opostas dão o mesmo zero no gráfico; a tabela de afirmações distingue os dois.",
            "É soma, não média: um mês com mais afirmações na mesma direção pesa mais.",
            "As cartas saem depois do fim do mês que cobrem, então o mês mais recente pode ainda não ter a carta de "
            "todos os gestores.",
            "A aba mede a narrativa, não o câmbio. Ela é mais útil para ver quando os gestores mudam de assunto — "
            "de fiscal para dólar global, por exemplo — do que para prever a direção da moeda.",
        ]),
    ]

    # ---- Sources ------------------------------------------------------------------------
    st += [KeepTogether([Paragraph("Fontes dos dados", H2), table([
        ["Fonte", "Onde aparece"],
        ["Banco Central do Brasil", "balanço de pagamentos, câmbio contratado, volume interbancário, reservas, swaps, "
         "intervenções, PTAX, PIB em dólares"],
        ["Ministério do Desenvolvimento (Comex Stat)", "balança de bens por país, fator agregado e produto"],
        ["CFTC — Traders in Financial Futures", "posicionamento no futuro de real da CME"],
        ["Banco de Compensações Internacionais (BIS)", "câmbio efetivo real"],
        ["Funcex, via IPEADATA", "termos de troca"],
        ["IBGE (IPCA) e BLS (CPI, via FRED)", "equilíbrio de PPP"],
        ["Cartas mensais públicas de Kapitalo, Kinea e Verde Asset", "FX Attribution; a classificação é da LIS Capital"],
        ["Bloomberg, Federal Reserve (FRED) e as fontes acima", "FX Model; o detalhe por fator está na segunda parte"],
    ], col_widths=[190, 291], align_right_from=-1)])]
    return st


def story_part2(internal_report):
    D, built = guide.load_payload(internal_report)
    return [PageBreak(), _Part("FX Model")] + guide.build_story(D, built)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
def _check_part2(out_path, n_part1_pages, model_pdf):
    """The second part must read like the approved team_materials PDF, page by page (footers aside)."""
    import fitz

    def body(page):
        lines = page.get_text().splitlines()
        return [l for l in lines if "página" not in l and not l.startswith("Apresentação exclusiva")]

    ours, theirs = fitz.open(out_path), fitz.open(model_pdf)
    got = [body(ours[i]) for i in range(n_part1_pages, ours.page_count)]
    want = [body(theirs[i]) for i in range(theirs.page_count)]
    if got != want:
        return "a segunda parte difere de %s (%d contra %d páginas) — regere o guia técnico ou este" % (
            model_pdf, len(got), len(want))
    return None


def run(recipient, notice_date=None, client_report=CLIENT_REPORT, out_path=OUT_PATH, with_model=True,
        internal_report=INTERNAL_REPORT, shots_dir=None, recapture=True):
    """`recipient` goes in the confidentiality notice, on the cover and on every page's footer --
    the same text generate_report.run(client=True, recipient=...) puts in the dashboard."""
    notice = client_notice(recipient, notice_date)
    _NOTICE[0] = notice
    generated_at = _generated_at(client_report)
    if not generated_at:
        raise RuntimeError("%s has no generated_at -- regenerate with run(client=True)" % client_report)
    S = shots_dir or tempfile.mkdtemp(prefix="lis_fxmanual_")
    if recapture or not os.path.exists(os.path.join(S, "anatomy.json")):
        capture(client_report, S)

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    doc = BaseDocTemplate(out_path, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm,
                          topMargin=18 * mm, bottomMargin=20 * mm,
                          title="FX Report — guia de leitura", author="LIS Capital")
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="f")
    doc.addPageTemplates([PageTemplate(id="p", frames=[frame], onPageEnd=_footer)])

    part1 = story_part1(S, generated_at, with_model, notice)
    # Build part 1 alone once to know where part 2 starts, for the comparison below.
    probe = BaseDocTemplate(os.path.join(S, "_part1.pdf"), pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm,
                            topMargin=18 * mm, bottomMargin=20 * mm)
    probe.addPageTemplates([PageTemplate(id="p", frames=[Frame(probe.leftMargin, probe.bottomMargin, probe.width,
                                                               probe.height)], onPageEnd=_footer)])
    probe.build(story_part1(S, generated_at, with_model, notice))
    n1 = probe.page

    story = part1 + (story_part2(internal_report) if with_model else [])
    doc.build(story)
    print("Wrote %s (%d pages; part 1: %d)" % (out_path, doc.page, n1))
    if with_model and os.path.exists(MODEL_GUIDE_PDF):
        warn = _check_part2(out_path, n1, MODEL_GUIDE_PDF)
        print("ATENÇÃO: " + warn if warn else "Parte 2 idêntica a %s" % MODEL_GUIDE_PDF)
    return out_path


if __name__ == "__main__":
    import sys
    run(sys.argv[1])
