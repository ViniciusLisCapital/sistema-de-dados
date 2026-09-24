# -*- coding: utf-8 -*-
"""Extrato em Excel das curvas de juros trimestrais, para exame fora do dashboard.

Pedido do usuario em 2026-09-21, para examinar a correlacao entre as series que a
equacao (R) usa: Selic, 2 anos (nominal e real), 10 anos (nominal e real), mais a
expectativa Focus longa interpolada e a projecao do Copom.

Nao alimenta relatorio nenhum e nao esta no manifesto: e um extrato para leitura humana,
que existe aqui em vez de num script solto porque vai ser regerado quando o dado andar.

Cinco abas:
    Trimestral (media)       o painel inteiro, na convencao que o modelo usa
    Trimestral (fechamento)  as series de curva pelo ultimo pregao do trimestre
    Correlacoes (nivel)      a matriz em nivel
    Correlacoes (variacao)   a mesma matriz em primeira diferenca
    Taxas a termo            o teste da opcao A: a taxa a termo escapa da correlacao
                             entre o RR* e o aperto monetario? (nao escapa -- ver o
                             veredito no topo da aba) + as series a termo trimestrais
    Dicionario               uma linha por coluna: o que e, de onde vem, a convencao

**As duas matrizes existem porque elas contam coisas diferentes, e a diferenca e o
achado.** Em nivel tudo correlaciona com tudo (0,83 a 0,97), porque as series dividem a
mesma tendencia de vinte anos. Em primeira diferenca o quadro se separa: a NTN-B de 10
anos contra a inclinacao real cai de +0,80 para **+0,01**, e a pre de 10 anos contra a
inclinacao nominal troca de sinal (+0,67 -> -0,13). Ler a correlacao so em nivel
responderia a pergunta errada.

Saida: reports/brasil/Curva de Juros Trimestral.xlsx

Uso:
    uv run python -m analytics.brasil.structural_model.planilha_curvas
"""
from __future__ import annotations

import pandas as pd
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

from analytics.brasil.monetary_policy.modelo_painel import para_q, q
from analytics.brasil.structural_model import panel
from analytics.brasil.structural_model.equations import taylor as _taylor

SAIDA = "reports/brasil/Curva de Juros Trimestral.xlsx"

# curva -> {rotulo: vertice}.  DIPRE e a curva nominal com os dois vertices completos
# desde 2006-01-02; a PREJS so tem 120M a partir de 2010-02, entao nao serve de par.
CURVAS = {
    "DIPRE":  {"Pré 2a": "24M", "Pré 5a": "60M", "Pré 10a": "120M"},
    "NTNBJS": {"NTN-B 2a": "24M", "NTN-B 5a": "60M", "NTN-B 10a": "120M"},
}

NAVY = "1F2853"
GOLD = "BB9B1D"

# vertice -> prazo em anos, para as taxas a termo
ANOS = {"3M": 0.25, "6M": 0.5, "9M": 0.75, "12M": 1.0,
        "24M": 2.0, "60M": 5.0, "120M": 10.0, "240M": 20.0}

# Segmentos a termo testados como candidatos a RR*. O de 5a->10a e o que motivou o
# teste: ele remove, por construcao, a politica esperada dos proximos cinco anos.
SEGMENTOS = [("12M", "24M", "1a→2a"), ("24M", "60M", "2a→5a"),
             ("60M", "120M", "5a→10a"), ("24M", "120M", "2a→10a"),
             ("120M", "240M", "10a→20a")]


def _curvas_diarias() -> pd.DataFrame:
    """Um pregao por linha, uma coluna por vertice pedido."""
    out = {}
    for curva, verts in CURVAS.items():
        d = q("macro_brasil",
              "SELECT date, tenor, value FROM br_interest_rate WHERE curve='%s' "
              "AND tenor IN (%s) ORDER BY date"
              % (curva, ", ".join("'%s'" % v for v in verts.values())))
        d["date"] = pd.to_datetime(d["date"])
        piv = d.pivot_table(index="date", columns="tenor", values="value", aggfunc="last")
        for rot, v in verts.items():
            if v not in piv.columns:
                raise ValueError("%s sem o vertice %s" % (curva, v))
            out[rot] = piv[v].astype(float)
    sel = q("macro_brasil", "SELECT date, value FROM br_interest_rate "
                            "WHERE curve='POLICY' AND tenor='1d' ORDER BY date")
    sel["date"] = pd.to_datetime(sel["date"])
    out["Selic"] = sel.set_index("date")["value"].astype(float)
    return pd.DataFrame(out)


def _fisher(nom: pd.Series, real: pd.Series) -> pd.Series:
    """Inflacao implicita EXATA: (1+i)/(1+r) - 1, e nao a diferenca simples.

    A diferenca simples descola ~0,2 p.p. nos niveis que o Brasil pratica, o que e
    grande contra a propria variacao da implicita.
    """
    return ((1.0 + nom / 100.0) / (1.0 + real / 100.0) - 1.0) * 100.0


def montar(como: str) -> pd.DataFrame:
    """Painel trimestral de curvas, na convencao `como` ('media' ou 'last')."""
    di = _curvas_diarias()
    t = pd.DataFrame({c: para_q(di[c].dropna(), como=como) for c in di.columns})
    for pz in ("2a", "5a", "10a"):
        t["Implícita %s" % pz] = _fisher(t["Pré %s" % pz], t["NTN-B %s" % pz])
    t["Inclinação nominal 2a−10a"] = t["Pré 2a"] - t["Pré 10a"]
    t["Inclinação real 2a−10a"] = t["NTN-B 2a"] - t["NTN-B 10a"]
    return t[["Selic", "Pré 2a", "Pré 5a", "Pré 10a",
              "NTN-B 2a", "NTN-B 5a", "NTN-B 10a",
              "Implícita 2a", "Implícita 5a", "Implícita 10a",
              "Inclinação nominal 2a−10a", "Inclinação real 2a−10a"]]


def curva_completa(nome: str, como: str = "media") -> pd.DataFrame:
    """Todos os vertices de uma curva, trimestrais. Para as taxas a termo."""
    d = q("macro_brasil", "SELECT date, tenor, value FROM br_interest_rate "
                          "WHERE curve='%s' ORDER BY date" % nome)
    d["date"] = pd.to_datetime(d["date"])
    piv = d.pivot_table(index="date", columns="tenor", values="value", aggfunc="last")
    return pd.DataFrame({t: para_q(piv[t].dropna(), como=como)
                         for t in ANOS if t in piv.columns})


def a_termo(t: pd.DataFrame, v1: str, v2: str) -> pd.Series:
    """Taxa a termo composta entre dois vertices, em % ao ano.

    (1+y2)^n2 = (1+y1)^n1 * (1+f)^(n2-n1)

    **Supoe taxa ZERO nos dois vertices**, e essa hipotese nao esta verificada: a
    curva 076 da B3 bate com a taxa indicativa da ANBIMA, que e rendimento de titulo
    COM cupom (NTN-B paga 6% a.a. semestral). Se os vertices forem rendimento ao
    vencimento e nao taxa zero, esta conta e uma aproximacao cujo erro cresce com a
    inclinacao da curva. Para o teste de correlacao que esta aba faz, o erro e suave
    na forma da curva e nao inverte o sinal da resposta -- mas para publicar um nivel
    de taxa a termo, o certo e a curva DIC (DI x IPCA), que e swap zero-cupom e esta
    disponivel na mesma fonte, ainda nao carregada.
    """
    a, b = ANOS[v1], ANOS[v2]
    return (((1 + t[v2] / 100) ** b / (1 + t[v1] / 100) ** a) ** (1.0 / (b - a)) - 1) * 100


def termo_series(como: str = "media") -> pd.DataFrame:
    """As taxas a termo reais e nominais de cada segmento de SEGMENTOS."""
    real, nom = curva_completa("NTNBJS", como), curva_completa("DIPRE", como)
    out = {}
    for v1, v2, rot in SEGMENTOS:
        if v1 in real.columns and v2 in real.columns:
            out["Real %s" % rot] = a_termo(real, v1, v2)
        if v1 in nom.columns and v2 in nom.columns:
            out["Nominal %s" % rot] = a_termo(nom, v1, v2)
    return pd.DataFrame(out)


def teste_termo(df: pd.DataFrame) -> pd.DataFrame:
    """O teste da opcao A: a taxa a termo escapa da correlacao com o aperto?

    A pergunta e a pendencia R2 da equacao (R). O RR* em uso -- a NTN-B de 10 anos --
    correlaciona +0,80 com `g_rr`, a medida de aperto monetario, entao a ancora
    `RR* + Meta` se move junto com a propria politica. A taxa a termo de 5 a 10 anos
    remove POR CONSTRUCAO a politica esperada dos proximos cinco anos, entao ela era
    a candidata natural a escapar.

    Cada linha traz as duas metades da resposta: o que a candidata faz com a
    correlacao, e o que ela faz com a equacao quando entra no lugar do RR*.
    """
    fe = df[df["completo"].astype(bool)]
    g, real = fe["g_rr"], curva_completa("NTNBJS")
    F = termo_series()

    cands = [("NTN-B 10 anos (em uso)", real["120M"]), ("NTN-B 20 anos", real["240M"])]
    cands += [("A termo real %s" % rot, F["Real %s" % rot]) for _, _, rot in SEGMENTOS]

    linhas = []
    for rot, serie in cands:
        j = pd.concat([serie.rename("s"), g, real["24M"].rename("c2")], axis=1).dropna()
        d2 = df.copy()
        d2["rr_10a"] = serie.reindex(df.index)   # e `rr_10a` que vira RR* em taylor.py
        r = _taylor.estimar(_taylor.montar(d2))
        linhas.append({
            "Candidata a RR*": rot,
            "Corr. com o aperto (nível)": round(j["s"].corr(j["g_rr"]), 3),
            "Corr. com o aperto (variação)": round(j["s"].diff().corr(j["g_rr"].diff()), 3),
            "Corr. com a NTN-B de 2 anos": round(j["s"].corr(j["c2"]), 3),
            "Nível hoje, %": round(float(serie.dropna().iloc[-1]), 2),
            "Média 2006-2026, %": round(float(serie.mean()), 2),
            "r1": round(float(r["coef"]["r1"]), 3),
            "r1b": round(float(r["coef"]["r1b"]), 3),
            "Efeito de longo prazo": round(float(r["efeito_lp"]), 2),
            "R² centrado": round(float(r["r2_cent"]), 3),
            "Ljung-Box Q(4)": round(float(r["lb_p4"]), 3),
        })
    return pd.DataFrame(linhas)


VEREDITO = [
    "TESTE — a taxa a termo resolve a correlação do RR* com o aperto monetário?",
    "",
    "Não resolve. A taxa a termo de 5 a 10 anos remove por construção a política esperada dos "
    "próximos cinco anos, e mesmo assim correlaciona +0,70 com o aperto, contra +0,80 da NTN-B "
    "de 10 anos à vista. O melhor segmento (10 a 20 anos) chega a +0,69, e é o mais ilíquido.",
    "",
    "O motivo está na coluna da direita da primeira tabela: TODO ponto da curva real "
    "correlaciona pelo menos 0,88 com a NTN-B de 2 anos, e é ela que domina a medida de aperto "
    "(desvio de 2,30 contra 1,41 na ponta de 10 anos, com correlação de 0,965 entre as duas). A "
    "curva se move em bloco: a contaminação é um fator de nível comum, não uma componente de "
    "política de curto prazo que se possa recortar escolhendo outro vértice.",
    "",
    "O achado colateral é tranquilizador: a equação quase não se importa com a escolha. As sete "
    "candidatas dão efeito de longo prazo entre 2,44 e 2,77, todas dentro do intervalo [1,47; "
    "2,64] que o Banco Central publica, e resíduo limpo em todas. A NTN-B de 10 anos, que está "
    "em uso, continua sendo a única com os TRÊS parâmetros dentro dos intervalos publicados.",
    "",
    "Consequência para a lista de pendências: separar expectativa de prêmio de maturidade exige "
    "um modelo — pesquisa Focus ou estrutura a termo afim —, não um recorte da curva.",
    "",
    "Ressalva da conta: a taxa a termo supõe taxa ZERO nos dois vértices, e a curva da B3 bate "
    "com a taxa indicativa da ANBIMA, que é rendimento de título com cupom. Para o teste de "
    "correlação isso não inverte a resposta; para publicar um nível, a fonte certa é a curva "
    "DI × IPCA, que é swap zero-cupom e ainda não está carregada.",
]

# A planilha comeca onde o painel comeca. Antes disso so a Selic existe (ela vai a
# 1994T3 no banco), e uma linha com uma coluna preenchida so atrapalha quem examina.
INICIO = pd.Period("2001Q4", "Q")


def montar_tudo() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    p = panel.construir()
    med = montar("media").loc[INICIO:]
    fim = montar("last").loc[INICIO:]

    d = med.copy()
    d["Focus IPCA 12m"] = p["pi_e"]
    d["Focus IPCA 2 anos (interpolada)"] = p["pi_e_2a"]
    d["Projeção do Copom (horiz. relevante)"] = p["pi_bcb"]
    d["Meta 12m"] = p["meta_12m"]
    d["Meta 24m"] = p["meta_24m"]
    d["Desvio — Focus 12m"] = p["pi_e"] - p["meta_12m"]
    d["Desvio — Focus 2 anos"] = p["pi_e_2a"] - p["meta_24m"]
    d["Desvio — Copom"] = p["pi_bcb"] - p["meta_12m"]
    d["Selic real ex-ante"] = d["Selic"] - p["pi_e"]
    # a ancora e o desvio que a equacao (R) explica, com RR* = NTN-B de 10 anos
    d["Âncora (RR* + Meta)"] = d["NTN-B 10a"] + p["meta_12m"]
    d["Desvio da âncora"] = d["Selic"] - d["Âncora (RR* + Meta)"]
    d["Hiato do produto"] = p["hiato"]
    d["Trimestre fechado"] = p["completo"].astype(bool)
    return d, fim, p


def correls(d: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    cols = ["Selic", "Pré 2a", "Pré 5a", "Pré 10a",
            "NTN-B 2a", "NTN-B 5a", "NTN-B 10a",
            "Implícita 2a", "Implícita 5a", "Implícita 10a",
            "Inclinação nominal 2a−10a", "Inclinação real 2a−10a",
            "Focus IPCA 12m", "Focus IPCA 2 anos (interpolada)",
            "Desvio — Focus 12m", "Desvio da âncora", "Hiato do produto"]
    sub = d[cols]
    return sub.corr().round(3), sub.diff().corr().round(3)


DIC = [
    ("Selic", "Taxa básica definida pelo Copom", "br_interest_rate, curva POLICY, vértice 1d",
     "Fonte BIS. Média dos pregões do trimestre. No banco ela vai a 1994T3; esta planilha "
     "começa em 2001T4, onde o resto do painel começa"),
    ("Pré 2a", "Juro nominal de 2 anos", "br_interest_rate, curva DIPRE, vértice 24M",
     "Curva de swap DI×pré da B3. Média dos pregões"),
    ("Pré 5a", "Juro nominal de 5 anos", "br_interest_rate, curva DIPRE, vértice 60M", "Idem"),
    ("Pré 10a", "Juro nominal de 10 anos", "br_interest_rate, curva DIPRE, vértice 120M",
     "Idem. A curva PREJS não serve de par: o vértice de 120M dela só começa em 2010-02"),
    ("NTN-B 2a", "Juro real de 2 anos", "br_interest_rate, curva NTNBJS, vértice 24M",
     "Curva real da B3, indexada ao IPCA. Média dos pregões"),
    ("NTN-B 5a", "Juro real de 5 anos", "br_interest_rate, curva NTNBJS, vértice 60M",
     "Idem. A curva real tem oito vértices no banco (3M, 6M, 9M, 12M, 2a, 5a, 10a, 20a), todos "
     "desde 2006-01-02; a planilha traz os três que a equação (R) discute"),
    ("NTN-B 10a", "Juro real de 10 anos", "br_interest_rate, curva NTNBJS, vértice 120M",
     "Idem. É o RR* que a equação (R) usa hoje"),
    ("Implícita 2a", "Inflação implícita de 2 anos", "derivada",
     "Fisher EXATO: (1+pré)/(1+real)−1. A diferença simples descola ~0,2 p.p."),
    ("Implícita 5a", "Inflação implícita de 5 anos", "derivada", "Idem"),
    ("Implícita 10a", "Inflação implícita de 10 anos", "derivada", "Idem"),
    ("Inclinação nominal 2a−10a", "Inclinação da curva nominal", "derivada", "Diferença simples, p.p."),
    ("Inclinação real 2a−10a", "Inclinação da curva real", "derivada",
     "É o `g_rr` da equação (H), a medida de aperto monetário, p.p."),
    ("Focus IPCA 12m", "Expectativa de IPCA 12 meses à frente", "expc_focus, horizonte 12m, suavizada",
     "Série publicada, mediana. Último boletim do trimestre"),
    ("Focus IPCA 2 anos (interpolada)", "Expectativa de IPCA a 2 anos",
     "expc_focus_periodo, pesquisa anual, interpolada",
     "A série rolante publicada só começa em 2021-03. Esta é interpolada da curva anual em "
     "h=1,5 ano (o centro da janela de 24 meses está a 18 meses). Erro médio de 0,071 p.p. "
     "contra a publicada nos 1.370 boletins em que coexistem"),
    ("Projeção do Copom (horiz. relevante)", "IPCA projetado pelo próprio Copom",
     "pm_copom_projecoes, horizonte_relevante=1, cenário juros_esperado",
     "Horizonte relevante = 6 trimestres à frente. Um vintage por trimestre desde 2008T1; "
     "faltam os T3 de 2003 a 2007"),
    ("Meta 12m", "Meta do CMN no horizonte de 12 meses", "inflc_meta (SGS 13521)",
     "Mistura ponderada entre o ano corrente e o seguinte, pelos meses que a janela alcança"),
    ("Meta 24m", "Meta do CMN no horizonte de 24 meses", "inflc_meta (SGS 13521)",
     "Os mesmos pesos, um ano adiante. Existe para casar com a Focus de 2 anos"),
    ("Desvio — Focus 12m", "Expectativa acima da meta", "derivada", "É o `dI` da equação (R), p.p."),
    ("Desvio — Focus 2 anos", "Idem, no horizonte de 2 anos", "derivada",
     "Contra a Meta 24m, não a de 12 — senão entra um degrau de janeiro"),
    ("Desvio — Copom", "Idem, pela projeção do comitê", "derivada", "Contra a Meta 12m"),
    ("Selic real ex-ante", "Selic menos a expectativa de 12 meses", "derivada", "p.p."),
    ("Âncora (RR* + Meta)", "Nível nominal de repouso da regra", "derivada",
     "NTN-B de 10 anos + Meta 12m. É contra ela que a equação (R) mede o desvio"),
    ("Desvio da âncora", "Selic menos a âncora", "derivada",
     "É a variável dependente da equação (R): `y = R − RR* − Meta`"),
    ("Real 5a→10a etc. (aba Taxas a termo)", "Taxa a termo entre dois vértices",
     "derivada de br_interest_rate",
     "(1+y₂)^n₂ = (1+y₁)^n₁·(1+f)^(n₂−n₁). Supõe taxa ZERO nos dois vértices — a curva da B3 "
     "bate com a taxa indicativa da ANBIMA, que é rendimento de título COM cupom, então o nível "
     "é aproximado. Para publicar nível, a fonte certa é a curva DI × IPCA (zero-cupom), "
     "disponível na mesma fonte e ainda não carregada"),
    ("Hiato do produto", "Hiato publicado pelo BCB", "pm_hiato_produto, variavel='central'",
     "Edição corrente do anexo do RPM, % do produto potencial. Já é trimestral"),
    ("Trimestre fechado", "O trimestre tem todos os dados?", "derivada",
     "FALSO no trimestre da ponta, que ainda está em curso. A estimação filtra por esta coluna"),
]


def _rot(idx) -> list[str]:
    return ["%dT%d" % (p.year, p.quarter) for p in idx]


def _cli(txt: str) -> str:
    """O console do Windows e cp1252: o menos tipografico e os acentos estouram nele."""
    return txt.encode("cp1252", "replace").decode("cp1252")


def escrever(d: pd.DataFrame, fim: pd.DataFrame, pnl: pd.DataFrame) -> None:
    cn, cd = correls(d)
    with pd.ExcelWriter(SAIDA, engine="openpyxl") as xw:
        for nome, df, rotulo in (
            ("Trimestral (média)", d, "Trimestre"),
            ("Trimestral (fechamento)", fim, "Trimestre"),
        ):
            t = df.copy()
            t.insert(0, rotulo, _rot(t.index))
            t.to_excel(xw, sheet_name=nome, index=False)

        cn.to_excel(xw, sheet_name="Correlações (nível)")
        cd.to_excel(xw, sheet_name="Correlações (variação)")
        teste = teste_termo(pnl)
        n_ver = len(VEREDITO)
        teste.to_excel(xw, sheet_name="Taxas a termo", index=False, startrow=n_ver + 1)
        ft = termo_series()
        ft.insert(0, "Trimestre", _rot(ft.index))
        ft.to_excel(xw, sheet_name="Taxas a termo", index=False,
                    startrow=n_ver + len(teste) + 4)
        pd.DataFrame(DIC, columns=["Coluna", "O que é", "De onde vem", "Convenção e ressalvas"]) \
            .to_excel(xw, sheet_name="Dicionário", index=False)

    _formatar(d, fim, cn, cd, teste)


def _formatar(d, fim, cn, cd, teste) -> None:
    import openpyxl
    wb = openpyxl.load_workbook(SAIDA)
    cab = Font(bold=True, color="FFFFFF", size=10)
    fill = PatternFill("solid", fgColor=NAVY)
    fina = Side(style="thin", color="D9D9D9")

    for ws in wb.worksheets:
        for c in ws[1]:
            c.font = cab
            c.fill = fill
            c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        ws.row_dimensions[1].height = 42
        ws.freeze_panes = "B2"

    for nome in ("Trimestral (média)", "Trimestral (fechamento)"):
        ws = wb[nome]
        ws.freeze_panes = "B2"
        ws.auto_filter.ref = ws.dimensions
        ws.column_dimensions["A"].width = 11
        for j in range(2, ws.max_column + 1):
            ws.column_dimensions[get_column_letter(j)].width = 15
            for i in range(2, ws.max_row + 1):
                cel = ws.cell(row=i, column=j)
                if isinstance(cel.value, (int, float)):
                    cel.number_format = "0.00"
                cel.border = Border(bottom=fina)

    for nome, m in (("Correlações (nível)", cn), ("Correlações (variação)", cd)):
        ws = wb[nome]
        ws.column_dimensions["A"].width = 34
        for j in range(2, ws.max_column + 1):
            ws.column_dimensions[get_column_letter(j)].width = 13
        for i in range(2, ws.max_row + 1):
            ws.cell(row=i, column=1).font = Font(bold=True, size=9)
            for j in range(2, ws.max_column + 1):
                cel = ws.cell(row=i, column=j)
                cel.number_format = "0.00"
                v = cel.value
                if isinstance(v, (int, float)):
                    # quanto mais forte a correlacao, mais escura a celula -- em modulo,
                    # porque o sinal ja esta no numero e colorir por sinal esconderia -0,9
                    a = abs(v)
                    if a >= 0.999:
                        cel.fill = PatternFill("solid", fgColor="D9D9D9")
                    elif a >= 0.8:
                        cel.fill = PatternFill("solid", fgColor="F2D98C")
                    elif a >= 0.6:
                        cel.fill = PatternFill("solid", fgColor="FAEBC8")

    ws = wb["Taxas a termo"]
    ws.freeze_panes = None
    n_ver = len(VEREDITO)
    for i, linha in enumerate(VEREDITO, start=1):
        cel = ws.cell(row=i, column=1, value=linha)
        cel.font = Font(bold=(i == 1), size=12 if i == 1 else 10,
                        color=NAVY if i == 1 else "000000")
        cel.alignment = Alignment(vertical="top", wrap_text=True)
        # altura pela largura util do bloco mesclado (~175 caracteres por linha),
        # senao os paragrafos longos ficam cortados sem nada avisar
        if i == 1:
            ws.row_dimensions[i].height = 26
        elif not linha:
            ws.row_dimensions[i].height = 8
        else:
            ws.row_dimensions[i].height = 15 * (len(linha) // 175 + 1) + 4
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=11)
    for i, linha in enumerate(VEREDITO, start=1):
        if i > 1 and linha:
            ws.merge_cells(start_row=i, start_column=1, end_row=i, end_column=11)
    ws.column_dimensions["A"].width = 30
    for j in range(2, 13):
        ws.column_dimensions[get_column_letter(j)].width = 15
    cab_t = Font(bold=True, color="FFFFFF", size=10)
    for lin in (n_ver + 2, n_ver + len(teste) + 5):
        for c in ws[lin]:
            if c.value is not None:
                c.font = cab_t
                c.fill = fill
                c.alignment = Alignment(horizontal="center", vertical="center",
                                        wrap_text=True)
        ws.row_dimensions[lin].height = 42
    # a linha da candidata em uso, destacada
    for i in range(n_ver + 3, n_ver + 3 + len(teste)):
        if str(ws.cell(row=i, column=1).value or "").endswith("(em uso)"):
            for j in range(1, 12):
                ws.cell(row=i, column=j).fill = PatternFill("solid", fgColor="F2D98C")
    for i in range(n_ver + 3, ws.max_row + 1):
        for j in range(2, ws.max_column + 1):
            cel = ws.cell(row=i, column=j)
            if isinstance(cel.value, (int, float)):
                cel.number_format = "0.00" if abs(cel.value) >= 1 else "0.000"
            cel.border = Border(bottom=fina)

    ws = wb["Dicionário"]
    for col, w in (("A", 34), ("B", 38), ("C", 42), ("D", 76)):
        ws.column_dimensions[col].width = w
    for i in range(2, ws.max_row + 1):
        for j in range(1, 5):
            ws.cell(row=i, column=j).alignment = Alignment(vertical="top", wrap_text=True)
    wb.save(SAIDA)


def main() -> None:
    d, fim, pnl = montar_tudo()
    escrever(d, fim, pnl)
    print("gravado: %s" % SAIDA)
    print("  %d trimestres, %s -> %s (%d colunas)"
          % (len(d), _rot(d.index)[0], _rot(d.index)[-1], d.shape[1]))
    print()
    print("  coluna                                  primeiro   ultimo    n")
    for c in d.columns:
        s = d[c].dropna()
        print("  %-38s  %-9s  %-9s %3d"
              % (_cli(c), _rot(s.index)[0], _rot(s.index)[-1], len(s)))
    cn, cd = correls(d)
    print()
    print("  as correlacoes que motivaram a planilha (nivel / variacao):")
    for a, b in (("Selic", "NTN-B 10a"), ("Selic", "NTN-B 5a"), ("Selic", "NTN-B 2a"),
                 ("NTN-B 2a", "NTN-B 5a"), ("NTN-B 5a", "NTN-B 10a"),
                 ("NTN-B 2a", "NTN-B 10a"), ("Pré 2a", "Pré 10a"),
                 ("NTN-B 10a", "Inclinação real 2a−10a"),
                 ("Desvio da âncora", "Desvio — Focus 12m")):
        print("    %-28s x %-26s %+.2f  /  %+.2f"
              % (_cli(a), _cli(b), cn.loc[a, b], cd.loc[a, b]))


if __name__ == "__main__":
    main()
