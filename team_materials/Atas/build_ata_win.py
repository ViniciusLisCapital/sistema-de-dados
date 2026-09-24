# -*- coding: utf-8 -*-
"""Roda o build_ata.py da skill registrando as fontes do Windows.

O _register_fonts() original procura apenas em /usr/share/fonts (Linux); no
Windows ele cai para Times/Courier, que sao Latin-1 e nao tem ŷ, Δ nem ✓ —
os glifos saem como caixa preta. Aqui registramos Georgia/Consolas antes.
"""
import sys, json, os, importlib.util
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

SKILL = (r"C:\Users\LIS CAPITAL\.claude\skills\synced"
         r"\9f9fc76c-a2e1-4c66-a04b-42620d6b1e79_8a728709-fb55-462b-af5d-6e380261b7c0"
         r"\lis-ata-reuniao\scripts\build_ata.py")

spec_mod = importlib.util.spec_from_file_location("build_ata", SKILL)
mod = importlib.util.module_from_spec(spec_mod)
spec_mod.loader.exec_module(mod)

FONTS = os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts")


def _win_fonts():
    def reg(name, *files):
        for f in files:
            p = os.path.join(FONTS, f)
            if os.path.exists(p):
                try:
                    pdfmetrics.registerFont(TTFont(name, p))
                    return name
                except Exception:
                    pass
        return None
    serif = reg("Serif", "georgia.ttf", "times.ttf")
    serifb = reg("SerifB", "georgiab.ttf", "timesbd.ttf")
    mono = reg("Mono", "consola.ttf", "cour.ttf")
    return (serif or "Times-Roman", serifb or "Times-Bold", mono or "Courier")


mod._register_fonts = _win_fonts


def _patch_symbols():
    """Georgia tem ŷ e Δ, mas nao tem ✓ nem →. Os marcadores sao desenhados
    com a fonte serifada, entao envolvemos cada simbolo num <font name="Sym">
    (Segoe UI Symbol), que tem os dois."""
    p = os.path.join(FONTS, "seguisym.ttf")
    if not os.path.exists(p):
        return
    try:
        pdfmetrics.registerFont(TTFont("Sym", p))
    except Exception:
        return
    mod.SYMBOLS = {k: ('<font name="Sym">%s</font>' % s, c)
                   for k, (s, c) in mod.SYMBOLS.items()}


def _patch_sans():
    """O corpo dos paragrafos, cards e tabelas usa Helvetica, que e base-14 e
    so cobre Latin-1 — ŷ e Δ saem como caixa preta. Troca por Arial (TTF, mesmo
    desenho), com a familia registrada para o <b> continuar funcionando."""
    faces = {"Sans": "arial.ttf", "SansB": "arialbd.ttf",
             "SansI": "ariali.ttf", "SansBI": "arialbi.ttf"}
    for name, fn in faces.items():
        p = os.path.join(FONTS, fn)
        if not os.path.exists(p):
            return
        try:
            pdfmetrics.registerFont(TTFont(name, p))
        except Exception:
            return
    pdfmetrics.registerFontFamily("Sans", normal="Sans", bold="SansB",
                                  italic="SansI", boldItalic="SansBI")
    troca = {"Helvetica": "Sans", "Helvetica-Bold": "SansB"}
    base = mod.ParagraphStyle

    class _PS(base):
        def __init__(self, name, parent=None, **kw):
            if "fontName" in kw:
                kw["fontName"] = troca.get(kw["fontName"], kw["fontName"])
            base.__init__(self, name, parent, **kw)

    mod.ParagraphStyle = _PS


def _patch_repeat_header():
    """Uma tabela que quebra de pagina perde o cabecalho navy, e as colunas
    deixam de ser legiveis na continuacao. Repete a primeira linha — so nas
    tabelas de conteudo, identificadas pelo fundo navy no cabecalho; cards e
    marcadores tambem sao Table e nao podem repetir nada."""
    base = mod.Table

    class _T(base):
        def setStyle(self, style):
            try:
                for cmd in style.getCommands():
                    if (cmd[0] == "BACKGROUND" and tuple(cmd[1]) == (0, 0)
                            and tuple(cmd[2]) == (-1, 0) and cmd[3] == mod.NAVY):
                        self.repeatRows = 1
                        break
            except Exception:
                pass
            return base.setStyle(self, style)

    mod.Table = _T


if __name__ == "__main__":
    _patch_symbols()
    _patch_sans()
    _patch_repeat_header()
    with open(sys.argv[1], encoding="utf-8") as f:
        conteudo = json.load(f)
    mod.build(conteudo, sys.argv[2])
    print("gerado:", sys.argv[2])
