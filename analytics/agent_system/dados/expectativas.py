"""
As tabelas do agente de expectativas (SISTEMA_AGENTES.md V.VII) e o F de cada uma.

A lista (quais tabelas) é decidida com o usuário e vive no SISTEMA_AGENTES.md; o gerador
levanta se esta declaração divergir dela. O tratamento (quais séries, que leitura) é do
sistema (IV.iv) e se ajusta pela qualidade do report.

Três coisas que valem para o arquivo inteiro:

  - As quatro tabelas `expc_*` são deste agente (III.III.vii, 2026-10-22). As da Focus por
    período fixo entram em quatro recortes: dois novos (inflação, PIB), com a consulta deste
    agente, e dois herdados do câmbio (Selic, câmbio), com a consulta dele. Tabela que câmbio
    ou PM já declaram sai da declaração deles (`de`/`so`): a consulta fica idêntica e o A do
    ciclo serve a todos. Nenhuma tabela aqui é de um agente novo que ainda não tem módulo.
  - A variável da tese é a Focus IPCA 12 meses suavizada, base de 30 dias, como MÉDIA DO
    TRIMESTRE (a `pi_e` do Modelo Estrutural; `modelo_painel.focus_ipca_12m` + `para_q`). O F
    imprime essa média por trimestre, que é o que o placar compara.
  - Desancoragem é distância da meta do MESMO horizonte: a 12 meses, a meta do ano e a do
    seguinte pesadas pelos meses da janela (como `panel.META_W_Q` do modelo); por ano-calendário,
    a meta daquele ano. Depois do último ano publicado, a última meta. A posição no histórico
    (Q1 do mapa) sai daqui, não da memória do agente.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from analytics.agent_system.dados import cambio, politica_monetaria
from analytics.agent_system.dados import especiais as esp
from analytics.agent_system.dados.motor import (Ctx, Tabela, antes, de, em, fdata, fmt, md_tabela,
                                                pctl, so)

SECAO = ("## (V.VII) Agente de expectativas", "*Fim das listas por agente.*")
PIB = None

# O IPCA e os cinco componentes, com o nome que a pesquisa usa.
_IPCA = ("IPCA", "IPCA Livres", "IPCA Administrados", "IPCA Serviços", "IPCA Bens industrializados",
         "IPCA Alimentação no domicílio")
_PIB = ("PIB Total", "PIB Agropecuária", "PIB Indústria", "PIB Serviços",
        "PIB Despesa de consumo das famílias", "PIB Despesa de consumo da administração pública",
        "PIB Formação Bruta de Capital Fixo", "PIB Exportação de bens e serviços",
        "PIB Importação de bens e serviços")
_CURTO = {"IPCA": "IPCA", "IPCA Livres": "Livres", "IPCA Administrados": "Administrados",
          "IPCA Serviços": "Serviços", "IPCA Bens industrializados": "Bens industrializados",
          "IPCA Alimentação no domicílio": "Alimentação no domicílio",
          "PIB Total": "PIB", "PIB Agropecuária": "Agropecuária", "PIB Indústria": "Indústria",
          "PIB Serviços": "Serviços", "PIB Despesa de consumo das famílias": "Consumo das famílias",
          "PIB Despesa de consumo da administração pública": "Consumo do governo",
          "PIB Formação Bruta de Capital Fixo": "Investimento (FBCF)",
          "PIB Exportação de bens e serviços": "Exportação",
          "PIB Importação de bens e serviços": "Importação"}


def _lista_sql(nomes) -> str:
    return ", ".join("'" + n.replace("'", "''") + "'" for n in nomes)


# ── auxiliares ────────────────────────────────────────────────────────────────
def _datas(df: pd.DataFrame) -> list[pd.Timestamp]:
    return sorted(pd.DatetimeIndex(df["date"].unique()))


def _refs(ctx: Ctx, d0, datas) -> dict[str, pd.Timestamp | None]:
    """As datas de pesquisa de comparação: 4 e 13 semanas antes e a do ciclo anterior."""
    out = {"4 sem.": esp._pesquisa_em(datas, d0 - pd.Timedelta(days=28)),
           "13 sem.": esp._pesquisa_em(datas, d0 - pd.Timedelta(days=91))}
    if ctx.anterior is not None:
        out["ciclo ant."] = esp._pesquisa_em(datas, ctx.anterior)
    return out


def _metas(ctx: Ctx) -> dict[int, float]:
    m = ctx.ler("inflc_meta").sort_values("date")
    return {int(d.year): float(v) for d, v in zip(m["date"], m["value"])}


def _meta_ano(metas: dict[int, float], ano: int) -> float | None:
    if not metas:
        return None
    if ano in metas:
        return metas[ano]
    if ano > max(metas):
        return metas[max(metas)]          # depois do último ano publicado, a última meta
    return None


def _meta_12m(metas: dict[int, float], d: pd.Timestamp) -> float | None:
    """Meta dos 12 meses à frente da data d: os meses que caem neste ano e no seguinte."""
    a, b = _meta_ano(metas, d.year), _meta_ano(metas, d.year + 1)
    if a is None or b is None:
        return None
    return ((12 - d.month) * a + d.month * b) / 12.0


def _movel(ctx: Ctx, indicador="IPCA", horizonte="12m", suav="S", base=0, col="mediana") -> pd.Series:
    df = ctx.ler("expc_focus", "inflação")
    r = df[(df["indicador"] == indicador) & (df["horizonte"] == horizonte) & (df["suavizada"] == suav)
           & (df["base_calculo"] == base)].sort_values("date")
    return r.set_index("date")[col].astype(float)


def _anual_k(ctx: Ctx, recorte: str, indicador: str, col: str = "mediana") -> pd.DataFrame:
    """Ano-calendário por distância: coluna k = ano de referência − ano da pesquisa."""
    df = ctx.ler("expc_focus_periodo", recorte)
    r = df[(df["indicador"] == indicador) & (df["periodicidade"] == "anual")].copy()
    r["ano"] = pd.to_numeric(r["data_referencia"].astype(str).str[:4], errors="coerce")
    r["k"] = r["ano"] - r["date"].dt.year
    return r.pivot_table(index="date", columns="k", values=col, aggfunc="last").sort_index()


def _fmt_pctl(hist: pd.Series, v) -> str:
    return fmt(pctl(hist, v), 0)


# ── F próprio das endógenas (leitura completa) ────────────────────────────────
def focus_movel(df: pd.DataFrame, ctx: Ctx) -> list[str]:
    """Horizonte móvel: a variável da tese por trimestre, o IPCA e os componentes a 12 e 24 meses,
    a dispersão e as respostas frescas (base de 4 dias úteis) contra a de 30 dias."""
    out = []
    # 1. A variável da tese: média do trimestre.
    s = _movel(ctx)
    if not s.empty:
        g = s.groupby(pd.PeriodIndex(s.index, freq="Q"))
        med, n = g.mean(), g.size()
        lim = 0.5 * float(n.iloc[:-1].median()) if len(n) > 1 else 0
        linhas = []
        for per in med.index[-7:][::-1]:
            completo = per != med.index[-1] or ctx.corte >= per.end_time.normalize()
            linhas.append({"Trimestre": f"{per.quarter}T{str(per.year)[2:]}",
                           "Média do trimestre (% a.a.)": fmt(med[per]),
                           "Pesquisas": int(n[per]),
                           "": "" if completo else ("em curso, parcial" if n[per] >= lim
                                                    else "em curso, menos da metade das pesquisas")})
        out += ["**A variável da tese**: Focus IPCA 12 meses à frente, suavizada, base de 30 dias, "
                "mediana, **média das pesquisas do trimestre** (a `pi_e` do Modelo Estrutural). "
                "É o que o placar compara.", ""] + md_tabela(linhas) + [""]

    # 2. Horizonte móvel, por indicador.
    datas = _datas(df)
    d0 = datas[-1]
    refs = _refs(ctx, d0, datas)
    linhas = []
    for ind in _IPCA:
        for hor in ("12m", "24m"):
            se = _movel(ctx, ind, hor)
            if se.empty:
                continue
            v = float(se.iloc[-1])
            row = {"Indicador": _CURTO[ind], "Horizonte": hor, f"Mediana ({fdata(se.index[-1])})": fmt(v)}
            for lab, d in refs.items():
                ref = em(se, d) if d is not None else None
                row[f"Δ {lab}"] = fmt(None if ref is None else v - ref, 2, True)
            dp = _movel(ctx, ind, hor, col="desvio_padrao")
            row["Desvio-padrão"] = fmt(dp.iloc[-1] if not dp.empty else None)
            row["Pctl hist."] = _fmt_pctl(se, v)
            row["Desde"] = fdata(se.index[0])
            linhas.append(row)
    out += [f"IPCA e componentes, mediana da pesquisa suavizada, base de 30 dias, % nos próximos 12 "
            f"ou 24 meses. Pesquisa mais recente: {fdata(d0)}. Comparações: "
            + ", ".join(f"{lab} = {fdata(d)}" for lab, d in refs.items()) + ". O histórico dos "
            "componentes é curto (a pesquisa os acrescentou depois): o percentil vale para a "
            "janela da coluna Desde.", ""] + md_tabela(linhas) + [""]

    # 3. Dispersão e respostas frescas do IPCA.
    linhas = []
    for hor in ("12m", "24m"):
        b0, b1 = _movel(ctx, "IPCA", hor), _movel(ctx, "IPCA", hor, base=1)
        dp = _movel(ctx, "IPCA", hor, col="desvio_padrao")
        mi, ma = _movel(ctx, "IPCA", hor, col="minimo"), _movel(ctx, "IPCA", hor, col="maximo")
        media = _movel(ctx, "IPCA", hor, col="media")
        n0 = _movel(ctx, "IPCA", hor, col="numero_respondentes")
        n1 = _movel(ctx, "IPCA", hor, base=1, col="numero_respondentes")
        if b0.empty:
            continue
        gap = (b1 - b0).dropna()
        linhas.append({
            "Horizonte": hor, "Mediana, 30 dias": fmt(b0.iloc[-1]),
            "Mediana, 4 dias úteis": fmt(b1.iloc[-1] if not b1.empty else None),
            "4 dias − 30 dias (p.p.)": fmt(gap.iloc[-1] if not gap.empty else None, 2, True),
            "Média − mediana": fmt(media.iloc[-1] - b0.iloc[-1] if not media.empty else None, 2, True),
            "Desvio-padrão": fmt(dp.iloc[-1] if not dp.empty else None),
            "Pctl desvio hist.": _fmt_pctl(dp, dp.iloc[-1] if not dp.empty else None),
            "Mín–máx": f"{fmt(mi.iloc[-1] if not mi.empty else None)} a {fmt(ma.iloc[-1] if not ma.empty else None)}",
            "Respondentes (30 d / 4 d)": f"{int(n0.iloc[-1]) if not n0.empty else '—'} / "
                                         f"{int(n1.iloc[-1]) if not n1.empty else '—'}"})
    out += ["IPCA, dispersão e respostas frescas. A base de 4 dias úteis só conta quem respondeu "
            "nos últimos dias: quando ela se afasta da de 30 dias, há revisão em curso que a mediana "
            "ainda não mostra. Média acima da mediana = cauda de respondentes acima.", ""]
    return out + md_tabela(linhas)


def focus_periodo_inflacao(df: pd.DataFrame, ctx: Ctx) -> list[str]:
    """Por período fixo: o IPCA e os componentes por ano, os próximos trimestres e meses."""
    datas = _datas(df)
    d0 = datas[-1]
    d4 = esp._pesquisa_em(datas, d0 - pd.Timedelta(days=28))
    dant = esp._pesquisa_em(datas, ctx.anterior) if ctx.anterior is not None else None
    hoje = df[df["date"] == d0]
    metas = _metas(ctx)

    def med(d, ind, per, ref):
        if d is None:
            return None
        r = df[(df["date"] == d) & (df["indicador"] == ind) & (df["periodicidade"] == per)
               & (df["data_referencia"].astype(str) == str(ref))]
        return None if r.empty else float(r["mediana"].iloc[0])

    out = []
    an = hoje[hoje["periodicidade"] == "anual"]
    anos = sorted({int(str(a)[:4]) for a in an["data_referencia"].astype(str)})
    linhas = []
    for ind in _IPCA:
        row = {"Indicador": _CURTO[ind]}
        for a in anos:
            v, v4 = med(d0, ind, "anual", a), med(d4, ind, "anual", a)
            row[str(a)] = ("—" if v is None else
                           f"{fmt(v)} ({fmt(None if v4 is None else v - v4, 2, True)})")
        linhas.append(row)
    linhas.append({"Indicador": "Meta do CMN", **{str(a): fmt(_meta_ano(metas, a)) for a in anos}})
    out += [f"**Por ano-calendário**, mediana de {fdata(d0)} e, entre parênteses, a variação em 4 "
            f"semanas (desde {fdata(d4)}), em p.p. A meta de anos ainda não fixados é a última "
            "publicada.", ""] + md_tabela(linhas) + [""]

    # Dispersão do IPCA por ano.
    linhas = []
    for a in anos:
        r = an[(an["indicador"] == "IPCA") & (an["data_referencia"].astype(str) == str(a))]
        if r.empty:
            continue
        r = r.iloc[0]
        row = {"Ano": a, "Mediana": fmt(r["mediana"]), "Média": fmt(r["media"]),
               "Desvio-padrão": fmt(r["desvio_padrao"]),
               "Mín–máx": f"{fmt(r['minimo'])} a {fmt(r['maximo'])}",
               "Respondentes": int(r["numero_respondentes"])}
        if dant is not None:
            row[f"Ciclo ant. ({fdata(dant)})"] = fmt(med(dant, "IPCA", "anual", a))
        linhas.append(row)
    out += ["IPCA por ano: dispersão das respostas.", ""] + md_tabela(linhas) + [""]

    # Próximos trimestres e meses do IPCA.
    for per, n, rot in (("trimestral", 6, "trimestre"), ("mensal", 6, "mês")):
        h = hoje[(hoje["periodicidade"] == per) & (hoje["indicador"] == "IPCA")].sort_values("ref_date").head(n)
        linhas = []
        for r in h.itertuples():
            v4 = med(d4, "IPCA", per, r.data_referencia)
            linhas.append({"Referência": r.data_referencia, "Mediana (%)": fmt(r.mediana),
                           "Δ 4 sem.": fmt(None if v4 is None else r.mediana - v4, 2, True),
                           "Desvio-padrão": fmt(r.desvio_padrao)})
        out += [f"IPCA nos próximos {n} períodos, por {rot} (variação no período, %).", ""] + md_tabela(linhas) + [""]
    return out


def focus_pib(df: pd.DataFrame, ctx: Ctx) -> list[str]:
    """A abertura da atividade esperada: PIB total, setores e componentes da demanda."""
    datas = _datas(df)
    d0 = datas[-1]
    d4 = esp._pesquisa_em(datas, d0 - pd.Timedelta(days=28))
    d13 = esp._pesquisa_em(datas, d0 - pd.Timedelta(days=91))
    hoje = df[df["date"] == d0]

    def med(d, ind, per, ref):
        if d is None:
            return None
        r = df[(df["date"] == d) & (df["indicador"] == ind) & (df["periodicidade"] == per)
               & (df["data_referencia"].astype(str) == str(ref))]
        return None if r.empty else float(r["mediana"].iloc[0])

    an = hoje[hoje["periodicidade"] == "anual"]
    anos = sorted({int(str(a)[:4]) for a in an["data_referencia"].astype(str)})[:3]
    linhas = []
    for ind in _PIB:
        row = {"Componente": _CURTO[ind]}
        for a in anos:
            v, v4, v13 = med(d0, ind, "anual", a), med(d4, ind, "anual", a), med(d13, ind, "anual", a)
            row[str(a)] = "—" if v is None else fmt(v)
            row[f"Δ 4 sem. {a}"] = fmt(None if v is None or v4 is None else v - v4, 2, True)
            row[f"Δ 13 sem. {a}"] = fmt(None if v is None or v13 is None else v - v13, 2, True)
        linhas.append(row)
    out = [f"Crescimento real esperado no ano, %, mediana de {fdata(d0)}; variações em p.p. contra "
           f"{fdata(d4)} (4 sem.) e {fdata(d13)} (13 sem.). Setores e componentes da demanda "
           "entraram na pesquisa em set/2021.", ""] + md_tabela(linhas) + [""]
    tri = hoje[(hoje["periodicidade"] == "trimestral") & (hoje["indicador"] == "PIB Total")].sort_values("ref_date")
    linhas = [{"Trimestre": r.data_referencia, "Mediana (%)": fmt(r.mediana),
               "Δ 4 sem.": fmt(None if (v4 := med(d4, "PIB Total", "trimestral", r.data_referencia)) is None
                               else r.mediana - v4, 2, True)} for r in tri.head(6).itertuples()]
    unid = tri["unidade"].dropna().iloc[0] if not tri.empty and tri["unidade"].notna().any() else "—"
    return out + [f"PIB por trimestre (unidade da pesquisa: {unid}).", ""] + md_tabela(linhas)


def focus_selic(df: pd.DataFrame, ctx: Ctx) -> list[str]:
    """A Selic de fim de ano, com a dispersão das respostas."""
    out = esp.focus_anual(df, ctx)
    d0 = df["date"].max()
    h = df[df["date"] == d0].sort_values("data_referencia")
    linhas = [{"Ano": r.data_referencia, "Desvio-padrão": fmt(r.desvio_padrao),
               "Mín–máx": f"{fmt(r.minimo)} a {fmt(r.maximo)}"} for r in h.head(4).itertuples()]
    return out + ["", "Dispersão das respostas, mesma pesquisa:", ""] + md_tabela(linhas)


def inflacao_implicita(df: pd.DataFrame, ctx: Ctx) -> list[str]:
    """A inflação implícita na curva: (1 + DI × pré)/(1 + NTN-B) − 1 no mesmo vértice."""
    w = df.assign(_k=df["curve"].astype(str) + "|" + df["tenor"].astype(str)).pivot_table(
        index="date", columns="_k", values="value", aggfunc="last").sort_index()
    metas = _metas(ctx)
    meta_lp = _meta_ano(metas, ctx.corte.year + 2)
    linhas = []
    for ten, rot in (("12M", "1 ano"), ("24M", "2 anos"), ("60M", "5 anos"), ("120M", "10 anos")):
        n, r = w.get(f"DIPRE|{ten}"), w.get(f"NTNBJS|{ten}")
        if n is None or r is None:
            continue
        imp = (((1 + n / 100) / (1 + r / 100) - 1) * 100).dropna()
        if imp.empty:
            continue
        t0, v = imp.index[-1], float(imp.iloc[-1])
        row = {"Vértice": rot, "Data": fdata(t0), "DI × pré (%)": fmt(float(n.dropna().iloc[-1])),
               "NTN-B (%)": fmt(float(r.dropna().iloc[-1])), "Implícita (%)": fmt(v),
               "Implícita − meta (p.p.)": fmt(None if meta_lp is None else v - meta_lp, 2, True)}
        for lab, m in (("1m", 1), ("3m", 3), ("12m", 12)):
            ref = em(imp, antes(t0, m))
            row[f"Δ {lab}"] = fmt(None if ref is None else v - ref, 2, True)
        if ctx.anterior is not None:
            ref = em(imp, ctx.anterior)
            row["Δ desde o ciclo ant."] = fmt(None if ref is None else v - ref, 2, True)
        row["Pctl hist."] = _fmt_pctl(imp, v)
        row["Pctl 10a"] = _fmt_pctl(imp.loc[antes(t0, 120):], v)
        linhas.append(row)
    return ([f"Inflação implícita = (1 + DI × pré)/(1 + NTN-B) − 1, no mesmo vértice (razão, não "
             f"diferença). É preço: carrega prêmio de risco de inflação e efeitos de liquidez. Meta de "
             f"referência: {fmt(meta_lp)}% (a do ano {ctx.corte.year + 2} ou a última publicada). "
             "Histórico desde 2006. Δ em p.p.", ""] + md_tabela(linhas))


# ── declaração ────────────────────────────────────────────────────────────────
TABELAS: list[Tabela] = [
    # ── i. Endógeno ──────────────────────────────────────────────────────────
    Tabela("expc_focus", recorte="inflação",
           filtro=f"indicador IN ({_lista_sql(_IPCA)}) AND tipo_calculo = 'geral'",
           especial=focus_movel),
    Tabela("expc_focus_periodo", recorte="inflação",
           filtro=f"indicador IN ({_lista_sql(_IPCA)}) AND tipo_calculo = 'geral' "
                  "AND base_calculo = 0 AND detalhe = ''",
           especial=focus_periodo_inflacao),
    Tabela("expc_focus_periodo", recorte="PIB",
           filtro=f"indicador IN ({_lista_sql(_PIB)}) AND periodicidade IN ('anual', 'trimestral') "
                  "AND tipo_calculo = 'geral' AND base_calculo = 0 AND detalhe = ''",
           especial=focus_pib),
    de(cambio, "expc_focus_periodo", recorte="Selic", especial=focus_selic),
    de(cambio, "expc_focus_periodo", recorte="câmbio"),
    de(cambio, "expc_focus_copom"),
    de(politica_monetaria, "expc_qpc"),
    # ── ii. Endógeno de política monetária ──────────────────────────────────
    de(cambio, "inflc_meta"),
    de(politica_monetaria, "pm_copom_projecoes"),
    de(politica_monetaria, "pm_copom_reuniao"),
    de(cambio, "pm_copom_calendario"),
    de(politica_monetaria, "br_interest_rate", especial=inflacao_implicita),
    # ── iii. Endógeno de inflação ────────────────────────────────────────────
    de(politica_monetaria, "inflc_agregados"),
    # ── iv. Endógeno de câmbio ───────────────────────────────────────────────
    so(cambio, "cmb_ptax", ("ptax_venda",)),
    # ── v. Endógeno de fiscal ────────────────────────────────────────────────
    de(cambio, "cmb_risco_pais"),
]


# ── leituras combinadas ───────────────────────────────────────────────────────
def desancoragem(ctx: Ctx) -> list[str]:
    """A distância da meta por horizonte, e a posição dela no histórico (Q1 do mapa)."""
    metas = _metas(ctx)
    series: list[tuple[str, pd.Series]] = []
    s12 = _movel(ctx)
    if not s12.empty:
        m12 = pd.Series([_meta_12m(metas, d) for d in s12.index], index=s12.index, dtype=float)
        series.append(("12 meses à frente (a variável da tese)", (s12 - m12).dropna()))
    k = _anual_k(ctx, "inflação", "IPCA")
    for dist, rot in ((0, "ano corrente"), (1, "ano seguinte (t+1)"), (2, "t+2"), (3, "t+3")):
        if dist not in k:
            continue
        x = k[dist].dropna()
        mt = pd.Series([_meta_ano(metas, d.year + dist) for d in x.index], index=x.index, dtype=float)
        series.append((rot, (x - mt).dropna()))
    linhas = []
    for rot, g in series:
        if g.empty:
            continue
        t0, v = g.index[-1], float(g.iloc[-1])
        dez = g.loc[antes(t0, 120):]
        i_max = g.idxmax()
        row = {"Horizonte": rot, "Data": fdata(t0), "Expectativa − meta (p.p.)": fmt(v, 2, True)}
        for lab, m in (("3m", 3), ("12m", 12)):
            ref = em(g, antes(t0, m))
            row[f"Δ {lab}"] = fmt(None if ref is None else v - ref, 2, True)
        if ctx.anterior is not None:
            ref = em(g, ctx.anterior)
            row["Δ desde o ciclo ant."] = fmt(None if ref is None else v - ref, 2, True)
        row |= {"Pctl hist.": _fmt_pctl(g, v), "Pctl 10a": _fmt_pctl(dez, v),
                "Maior da série": f"{fmt(float(g.max()), 2, True)} ({fdata(i_max)})",
                "Desde": fdata(g.index[0])}
        linhas.append(row)
    return (["### Desancoragem: distância da meta por horizonte, e onde ela está no histórico", "",
             "Mediana da Focus menos a meta do mesmo horizonte, em p.p. A 12 meses, a meta do ano e a "
             "do seguinte pesadas pelos meses da janela; por ano-calendário, a meta daquele ano (a "
             "última publicada para anos ainda não fixados). Ano corrente e t+1 carregam choques já "
             "visíveis; a ancoragem se julga em t+2 e t+3. Pctl = posição da distância de hoje entre "
             "todas as pesquisas da série (hist.) e dos últimos 10 anos. Ano-calendário desde 2000; "
             "12 meses desde 2001.", ""] + md_tabela(linhas))


def juro_real_esperado(ctx: Ctx) -> list[str]:
    """A coerência da pesquisa: Selic esperada contra IPCA esperado, ano a ano, e o neutro do QPC."""
    sel = ctx.ler("expc_focus_periodo", "Selic")
    ipc = ctx.ler("expc_focus_periodo", "inflação")
    d0 = min(sel["date"].max(), ipc["date"].max())
    s = sel[sel["date"] == d0]
    i = ipc[(ipc["date"] == d0) & (ipc["indicador"] == "IPCA") & (ipc["periodicidade"] == "anual")]
    metas = _metas(ctx)
    linhas = []
    for r in s.sort_values("data_referencia").itertuples():
        a = str(r.data_referencia)
        x = i[i["data_referencia"].astype(str) == a]
        if x.empty:
            continue
        pi = float(x["mediana"].iloc[0])
        real = ((1 + r.mediana / 100) / (1 + pi / 100) - 1) * 100
        linhas.append({"Ano": a, "Selic no fim do ano (%)": fmt(r.mediana), "IPCA do ano (%)": fmt(pi),
                       "Meta (%)": fmt(_meta_ano(metas, int(a[:4]))),
                       "IPCA − meta (p.p.)": fmt(None if (mt := _meta_ano(metas, int(a[:4]))) is None
                                                 else pi - mt, 2, True),
                       "Juro real implícito na pesquisa (%)": fmt(real)})
    out = ["### A pesquisa contra ela mesma: Selic e IPCA esperados", "",
           f"Focus de {fdata(d0)}, medianas por ano. Juro real = (1 + Selic do fim do ano)/(1 + IPCA "
           "do ano) − 1: uma aproximação do juro real que a pesquisa espera, não uma taxa ex-ante de "
           "mercado. Se a pesquisa espera inflação acima da meta e, ao mesmo tempo, juro real caindo, "
           "é sinal de dúvida sobre a reação do Copom (mapa 2.8).", ""] + md_tabela(linhas)
    q = ctx.ler("expc_qpc")
    n = q[(q["variavel"] == "juro_real_neutro") & (q["estatistica"] == "mediana")]
    if not n.empty:
        nro = n["nro_reuniao"].max()
        x = n[n["nro_reuniao"] == nro]
        out += ["", f"Juro real neutro no QPC da reunião {int(nro)}, mediana: "
                + "; ".join(f"{str(r.referencia).replace('_', ' ')} {fmt(r.valor)}%" for r in x.itertuples()) + "."]
    return out


def focus_contra_copom(ctx: Ctx) -> list[str]:
    """A Focus, o QPC e o Copom no horizonte relevante (Q3)."""
    p = ctx.ler("pm_copom_projecoes")
    p = p[(p["indice"] == "ipca") & (p["cenario"] == "juros_esperado") & (p["horizonte_relevante"] == 1)]
    if p.empty:
        return []
    nro = p["nro_reuniao"].max()
    sub = p[p["nro_reuniao"] == nro]
    doc = "relatorio" if (sub["documento"] == "relatorio").any() else "comunicado"
    r = sub[sub["documento"] == doc].iloc[0]
    hr = esp._periodo(r["date"], r["periodo_tipo"])
    linhas = [{"Fonte": f"Copom, reunião {int(nro)} ({'RPM' if doc == 'relatorio' else 'comunicado'}, "
                        f"{fdata(r['vintage'])})", "IPCA 4 trimestres no horizonte relevante (%)": fmt(r["value"], 1)}]
    q = ctx.ler("expc_qpc")
    x = q[(q["bloco"] == "ipca_horizonte_relevante") & (q["variavel"] == "ipca_4t") & (q["estatistica"] == "mediana")]
    if not x.empty:
        nq = x["nro_reuniao"].max()
        y = x[x["nro_reuniao"] == nq].iloc[0]
        linhas.append({"Fonte": f"QPC da reunião {int(nq)}, mediana (referência {y['referencia']})",
                       "IPCA 4 trimestres no horizonte relevante (%)": fmt(y["valor"], 2)})
    s12 = _movel(ctx)
    if not s12.empty:
        linhas.append({"Fonte": f"Focus, 12 meses à frente ({fdata(s12.index[-1])})",
                       "IPCA 4 trimestres no horizonte relevante (%)": f"{fmt(float(s12.iloc[-1]))} "
                       "(outro horizonte: os próximos 12 meses)"})
    return (["### O Copom, o QPC e a Focus no horizonte relevante", "",
             f"Horizonte relevante do Copom: {hr}. A projeção do Copom é condicional aos caminhos que ele "
             "usa (Selic da Focus, câmbio, petróleo): não é a previsão dele.", ""] + md_tabela(linhas))


COMBINADAS = [desancoragem, juro_real_esperado, focus_contra_copom]
