"""
F próprio das tabelas que não são uma série no tempo: curvas, pesquisas por período de
referência, calendário e decisões do Copom. Cada função recebe o A da tabela e o contexto e
devolve linhas de markdown. Compartilhadas entre agentes: o de política monetária vai usar as
mesmas.
"""

from __future__ import annotations

import re

import numpy as np
import pandas as pd

from analytics.agent_system.dados.motor import Ctx, antes, fdata, fmt, md_tabela

_ROTULO_REUNIAO = re.compile(r"R(\d+)/(\d{4})$")


def _pesquisa_em(datas: list, ref) -> pd.Timestamp | None:
    ds = [d for d in datas if d <= ref]
    return ds[-1] if ds else None


# ── Focus ─────────────────────────────────────────────────────────────────────
def focus_anual(df: pd.DataFrame, ctx: Ctx) -> list[str]:
    """Mediana da Focus por ano de referência: a pesquisa mais recente contra 4 e 13 semanas antes."""
    datas = sorted(pd.DatetimeIndex(df["date"].unique()))
    d0 = datas[-1]
    d4, d13 = _pesquisa_em(datas, d0 - pd.Timedelta(days=28)), _pesquisa_em(datas, d0 - pd.Timedelta(days=91))
    dant = _pesquisa_em(datas, ctx.anterior) if ctx.anterior is not None else None
    anos = sorted(int(a) for a in df.loc[df["date"] == d0, "data_referencia"].astype(str).unique())[:4]

    def med(d, ano):
        if d is None:
            return None
        r = df[(df["date"] == d) & (df["data_referencia"].astype(str) == str(ano))]
        return None if r.empty else float(r["mediana"].iloc[0])

    linhas = []
    for a in anos:
        v0, v4 = med(d0, a), med(d4, a)
        r = {"Ano": a, f"Mediana ({fdata(d0)})": fmt(v0), f"4 sem. antes ({fdata(d4)})": fmt(v4),
             f"13 sem. antes ({fdata(d13)})": fmt(med(d13, a)),
             "Δ 4 sem.": fmt(None if v0 is None or v4 is None else v0 - v4, 2, True)}
        if dant is not None:
            r[f"Ciclo ant. ({fdata(dant)})"] = fmt(med(dant, a))
        n = df[(df["date"] == d0) & (df["data_referencia"].astype(str) == str(a))]["numero_respondentes"]
        r["Respondentes"] = "—" if n.empty or pd.isna(n.iloc[0]) else int(n.iloc[0])
        linhas.append(r)
    un = df["unidade"].dropna().iloc[-1] if df["unidade"].notna().any() else "—"
    return [f"Unidade: {un}. Mediana da pesquisa (janela de 30 dias).", ""] + md_tabela(linhas)


def _datas_reunioes(ctx: Ctx) -> dict[tuple[int, int], pd.Timestamp]:
    """(posição no ano, ano) -> data da decisão, do calendário oficial em A."""
    cal = ctx.ler("pm_copom_calendario")
    out = {}
    for ano, g in cal.groupby(cal["date"].dt.year):
        for k, d in enumerate(sorted(g["date"]), start=1):
            out[(k, int(ano))] = d
    return out


def _selic_vigente(ctx: Ctx, d) -> tuple[float | None, pd.Timestamp | None]:
    r = ctx.ler("pm_copom_reuniao")
    r = r[r["date"] < d].sort_values("date")
    return (None, None) if r.empty else (float(r["selic_decidida"].iloc[-1]), r["date"].iloc[-1])


def focus_copom(df: pd.DataFrame, ctx: Ctx) -> list[str]:
    """Selic mediana da Focus em cada uma das próximas reuniões, contra 4 semanas antes."""
    datas = sorted(pd.DatetimeIndex(df["date"].unique()))
    d0 = datas[-1]
    d4 = _pesquisa_em(datas, d0 - pd.Timedelta(days=28))
    dant = _pesquisa_em(datas, ctx.anterior) if ctx.anterior is not None else None
    cal = _datas_reunioes(ctx)

    def chave(rot):
        m = _ROTULO_REUNIAO.match(str(rot))
        return (int(m.group(2)), int(m.group(1))) if m else (9999, 0)

    hoje = df[df["date"] == d0].copy()
    hoje["k"] = hoje["reuniao"].map(chave)
    hoje = hoje.sort_values("k").head(8)

    def med(d, rot):
        if d is None:
            return None
        r = df[(df["date"] == d) & (df["reuniao"] == rot)]
        return None if r.empty else float(r["mediana"].iloc[0])

    linhas = []
    for r in hoje.itertuples():
        ano, k = r.k
        v4 = med(d4, r.reuniao)
        row = {"Reunião": r.reuniao, "Data": fdata(cal.get((k, ano))),
               f"Mediana ({fdata(d0)})": fmt(r.mediana), f"4 sem. antes ({fdata(d4)})": fmt(v4),
               "Δ 4 sem. (p.p.)": fmt(None if v4 is None else r.mediana - v4, 2, True),
               "Mín–máx": f"{fmt(r.minimo)} a {fmt(r.maximo)}"}
        if dant is not None:
            row[f"Ciclo ant. ({fdata(dant)})"] = fmt(med(dant, r.reuniao))
        linhas.append(row)
    vig, dv = _selic_vigente(ctx, d0 + pd.Timedelta(days=1))
    return [f"Selic vigente na data da pesquisa: {fmt(vig)}% (decidida em {fdata(dv)}). "
            "Mediana da pesquisa (janela de 30 dias), % a.a.", ""] + md_tabela(linhas)


# ── Copom ─────────────────────────────────────────────────────────────────────
def copom_calendario(df: pd.DataFrame, ctx: Ctx) -> list[str]:
    datas = sorted(df["date"])
    passadas = [d for d in datas if d < ctx.corte]
    futuras = [d for d in datas if d >= ctx.corte][:4]
    linhas = [{"Reunião": "última" if i == 0 else f"próxima {i}", "Decisão": fdata(d),
               "Dias a partir do corte": (d - ctx.corte).days}
              for i, d in enumerate(passadas[-1:] + futuras)]
    return [f"O calendário oficial vai até {fdata(datas[-1])}.", ""] + md_tabela(linhas)


def copom_reuniao(df: pd.DataFrame, ctx: Ctx) -> list[str]:
    ult = df.sort_values("date").tail(6).iloc[::-1]
    linhas = [{"Reunião": int(r.nro_reuniao), "Decisão": fdata(r.date),
               "Selic decidida (% a.a.)": fmt(r.selic_decidida),
               "Passo (p.b.)": f"{int(r.variacao_bps):+d}"} for r in ult.itertuples()]
    return md_tabela(linhas)


def _periodo(d: pd.Timestamp, tipo: str) -> str:
    return str(d.year) if tipo == "ano" else f"{(d.month - 1) // 3 + 1}T{d:%y}"


def copom_projecoes(df: pd.DataFrame, ctx: Ctx) -> list[str]:
    """O caminho de IPCA projetado na reunião mais recente, cenário com os juros da Focus."""
    df = df[(df["indice"] == "ipca") & (df["cenario"] == "juros_esperado")]
    if df.empty:
        return ["Sem projeção no cenário com juros esperados."]

    def da_reuniao(nro):
        sub = df[df["nro_reuniao"] == nro]
        doc = "relatorio" if (sub["documento"] == "relatorio").any() else "comunicado"
        return sub[sub["documento"] == doc].sort_values("date"), doc

    nros = sorted(df["nro_reuniao"].unique())
    sub, doc = da_reuniao(nros[-1])
    linhas = [{"Período": _periodo(r.date, r.periodo_tipo), "IPCA 4 trimestres (%)": fmt(r.value, 1),
               "": "horizonte relevante" if r.horizonte_relevante == 1 else ""}
              for r in sub.itertuples()]
    out = [f"Reunião {nros[-1]} (de {fdata(sub['vintage'].iloc[0])}), "
           f"{'Relatório de Política Monetária' if doc == 'relatorio' else 'comunicado'}. "
           "Valor = IPCA acumulado em quatro trimestres.", ""] + md_tabela(linhas)
    if len(nros) > 1:
        ant, doc_a = da_reuniao(nros[-2])
        hr = ant[ant["horizonte_relevante"] == 1]
        if not hr.empty:
            r = hr.iloc[0]
            out += ["", f"Na reunião anterior ({nros[-2]}), o horizonte relevante "
                        f"({_periodo(r['date'], r['periodo_tipo'])}) estava em {fmt(r['value'], 1)}%."]
    return out


def inflc_meta(df: pd.DataFrame, ctx: Ctx) -> list[str]:
    ult = df.sort_values("date").tail(3)
    return md_tabela([{"Ano": r.date.year, "Meta (%)": fmt(r.value, 2)} for r in ult.itertuples()])


# ── curva DI ──────────────────────────────────────────────────────────────────
_PRAZOS = (("1 mês", 21), ("3 meses", 63), ("6 meses", 126), ("1 ano", 252), ("2 anos", 504),
           ("3 anos", 756), ("5 anos", 1260), ("10 anos", 2520))


def _taxa(du: np.ndarray, tx: np.ndarray, alvo: int) -> float | None:
    """Taxa no prazo `alvo` (dias úteis), flat-forward entre vértices, como a B3 monta a curva."""
    if len(du) == 0 or alvo > du.max():
        return None
    xs = np.concatenate([[0.0], du])
    lnf = np.concatenate([[0.0], du / 252.0 * np.log1p(tx / 100.0)])
    return float(np.expm1(np.interp(alvo, xs, lnf) * 252.0 / alvo) * 100)


def di_grade(df: pd.DataFrame, ctx: Ctx) -> list[str]:
    from analytics.brasil.monetary_policy.expectativas_juros import caminho_di

    pregoes = sorted(pd.DatetimeIndex(df["date"].unique()))
    p0 = pregoes[-1]

    def curva(p):
        g = df[df["date"] == p].sort_values("du")
        return g["du"].to_numpy(float), g["value"].to_numpy(float)

    refs = {lab: _pesquisa_em(pregoes, antes(p0, m)) for lab, m in (("1m", 1), ("3m", 3), ("12m", 12))}
    if ctx.anterior is not None:
        refs["ciclo ant."] = _pesquisa_em(pregoes, ctx.anterior)
    curvas = {p: curva(p) for p in {p0, *[r for r in refs.values() if r is not None]}}
    linhas = []
    for nome, alvo in _PRAZOS:
        v = _taxa(*curvas[p0], alvo)
        row = {"Prazo": nome, "Taxa (% a.a.)": fmt(v, 2)}
        for lab, p in refs.items():
            ref = None if p is None else _taxa(*curvas[p], alvo)
            row[f"Δ {lab} (p.b.)"] = fmt(None if v is None or ref is None else (v - ref) * 100, 0, True)
        linhas.append(row)
    out = [f"Pregão de {fdata(p0)}. DI × pré, base 252, nos prazos redondos.", ""] + md_tabela(linhas)

    # A Selic que a curva precifica em cada reunião (preço, com prêmio de prazo; não previsão).
    cal = sorted(ctx.ler("pm_copom_calendario")["date"])
    futuras = [d for d in cal if d >= p0]
    if not futuras:
        return out

    def caminho(p):
        reun = [d for d in cal if d >= p]
        cdi0, cam = caminho_di(p.date(), *curvas.setdefault(p, curva(p)), [d.date() for d in reun])
        vig, _ = _selic_vigente(ctx, p + pd.Timedelta(days=1))
        if vig is None:
            return {}
        return {d: v + (vig - cdi0) for d, v in zip(reun, cam)}

    c0 = caminho(p0)
    p1 = refs.get("1m")
    c1 = caminho(p1) if p1 is not None else {}
    vig0, _ = _selic_vigente(ctx, p0 + pd.Timedelta(days=1))
    linhas, prev = [], vig0
    for d in futuras:
        if d not in c0:
            break
        v, v1 = c0[d], c1.get(d)
        linhas.append({"Reunião": fdata(d), "Selic na curva (% a.a.)": fmt(v, 2),
                       "Passo implícito (p.b.)": fmt(None if prev is None else (v - prev) * 100, 0, True),
                       f"1 mês antes ({fdata(p1)})": fmt(v1, 2),
                       "Δ 1 mês (p.b.)": fmt(None if v1 is None else (v - v1) * 100, 0, True)})
        prev = v
    out += ["", f"Selic precificada na curva em cada reunião (meta vigente {fmt(vig0)}%). "
                "É preço, com prêmio de prazo, não previsão. Reuniões só até onde vai o calendário "
                f"oficial ({fdata(cal[-1])}).", ""] + md_tabela(linhas)
    return out
