"""
As tabelas do agente de inflação (SISTEMA_AGENTES.md V.III) e o F de cada uma.

A lista (quais tabelas) é decidida com o usuário e vive no SISTEMA_AGENTES.md; o gerador
levanta se esta declaração divergir dela. O tratamento (quais séries, que leitura) é do
sistema (IV.iv) e se ajusta pela qualidade do report.

Três coisas que valem para o arquivo inteiro:

  - Tabela que o câmbio ou a PM já declaram sai da declaração DELES (`de`/`so`, do motor),
    trocando só séries ou o F próprio: a consulta fica idêntica e o A do ciclo, que é
    compartilhado, serve a todos. O `expc_focus_periodo (componentes)` é a única consulta nova
    de uma tabela de outro agente novo (expectativas); leva `variante="inflacao"` até a
    declaração ser unificada com a dele.
  - Profundidade (PRINCIPIOS I.II.vii): só o grupo "Endógeno" ganha a leitura completa. As
    posições no histórico das séries de inflação partem de 2000 (regime de metas): a série do
    SGS vai a 1980, e um percentil contra a hiperinflação não diz nada.
  - As leituras combinadas são o que as perguntas do mapa pedem e nenhuma tabela dá sozinha:
    o IPCA e os quatro grupos por trimestre (a unidade do Modelo Estrutural, e o placar), o
    último mês contra o mesmo mês dos dez anos anteriores (a sazonalidade, medida, não
    lembrada) e os administrados item a item.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from analytics.agent_system.dados import cambio, politica_monetaria
from analytics.agent_system.dados import especiais as esp
from analytics.agent_system.dados.motor import (Ctx, Serie, Tabela, _nivel, _var_mensal, de, fdata,
                                                fmt, md_tabela, pctl, so)

SECAO = ("## (V.III) Agente de inflação", "## (V.IV)")
PIB = None

_INICIO_HIST = pd.Timestamp("2000-01-01")   # percentis no regime de metas, não desde 1980


def _s(chave, rotulo, unidade, leitura, **kw) -> Serie:
    return Serie(chave, rotulo, unidade, leitura, **kw)


# Os quatro grupos do BC, que são os quatro do Modelo Estrutural (SGS; os mesmos recortes de
# subitem que `inflc_dim` dá).
_GRUPOS = (("ipca", "IPCA"), ("ipca_servicos", "Serviços"), ("ipca_alimentacao", "Alimentação"),
           ("ipca_industriais", "Bens industriais"), ("ipca_administrado", "Monitorados"))

_AGREGADOS = (
    *[_s(k, rot, "%", "var_mensal") for k, rot in (
        ("ipca", "IPCA"), ("ipca15", "IPCA-15"),
        ("ipca_servicos", "Serviços"), ("ipca_alimentacao", "Alimentação"),
        ("ipca_industriais", "Bens industriais"), ("ipca_administrado", "Monitorados"),
        ("ipca_livres", "Livres"), ("ipca_comercializaveis", "Comercializáveis"),
        ("ipca_nao_comercializaveis", "Não comercializáveis"),
        ("ipca_nucleo_ex0", "Núcleo EX0"), ("ipca_nucleo_ex03", "Núcleo EX3"),
        ("ipca_nucleo_ex03_servicos", "Núcleo EX3, serviços"),
        ("ipca_nucleo_ex03_industriais", "Núcleo EX3, industriais"),
        ("ipca_nucleo_exfe", "Núcleo EXFE"),
        ("ipca_nucleo_medias_aparadas", "Núcleo médias aparadas com suavização"),
        ("ipca_nucleo_medias_aparadas_sem_suavizacao", "Núcleo médias aparadas sem suavização"),
        ("ipca_nucleo_p55", "Núcleo P55"), ("ipca_nucleo_dp", "Núcleo dupla ponderação"))],
    _s("ipca_indice_difusao", "Índice de difusão", "% dos subitens com alta", "dif", casas=1),
    _s("ipca_12m", "IPCA acumulado em 12 meses (publicado)", "%", "dif"),
)


# ── F próprio das endógenas (leitura completa) ────────────────────────────────
def _largo_agregados(df: pd.DataFrame) -> pd.DataFrame:
    return df.pivot_table(index="date", columns="name", values="value", aggfunc="last").sort_index()


def agregados(df: pd.DataFrame, ctx: Ctx) -> list[str]:
    """As séries do SGS: variação do mês e acumulados, com a posição no histórico desde 2000."""
    w = _largo_agregados(df)
    var, niv, faltam = [], [], []
    for se in _AGREGADOS:
        s = w[se.chave].dropna() if se.chave in w else pd.Series(dtype=float)
        s = s.loc[_INICIO_HIST:]
        if s.empty:
            faltam.append(se.chave)
            continue
        if se.leitura == "var_mensal":
            var.append(_var_mensal(se, s, ctx))
        else:
            niv.append(_nivel(se, s, ctx, False))
    out = ["Variação mensal (%), sem ajuste sazonal. Acumulados compostos. Posição no histórico "
           "desde 2000. Grupos e núcleos na classificação do BC.", ""] + md_tabela(var)
    out += [""] + md_tabela(niv)
    if faltam:
        out += ["", f"Sem dado no corte: {', '.join(faltam)}."]
    return out


def indice_geral(df: pd.DataFrame, ctx: Ctx) -> list[str]:
    """O índice como o IBGE publica: os últimos seis meses e o 12 meses nos fechamentos de
    trimestre, que é o número do placar."""
    out = []
    for ind, rot in (("IPCA", "IPCA"), ("IPCA15", "IPCA-15")):
        d = df[df["indice"] == ind].sort_values("date")
        if d.empty:
            continue
        linhas = [{"Mês": f"{r.date:%Y-%m}", "Número-índice": fmt(r.numero_indice, 2),
                   "No mês (%)": fmt(r.var_mensal), "No ano (%)": fmt(r.var_ano),
                   "12 meses (%)": fmt(r.var_12m)} for r in d.tail(6).iloc[::-1].itertuples()]
        out += [f"{rot}, últimos seis meses (IBGE/SIDRA):", ""] + md_tabela(linhas) + [""]
    d = df[(df["indice"] == "IPCA") & (df["date"].dt.month.isin([3, 6, 9, 12]))].sort_values("date")
    linhas = [{"Trimestre": esp._periodo(r.date, "trimestre"), "Mês de fechamento": f"{r.date:%Y-%m}",
               "IPCA 12 meses (%)": fmt(r.var_12m)} for r in d.tail(8).iloc[::-1].itertuples()]
    out += ["IPCA acumulado em 12 meses no fechamento dos últimos oito trimestres (a variável da "
            "tese e do placar):", ""] + md_tabela(linhas)
    return out


# ── F próprio das consultas (leitura enxuta) ──────────────────────────────────
def copom_projecoes(df: pd.DataFrame, ctx: Ctx) -> list[str]:
    """O caminho projetado na reunião mais recente (IPCA, livres, administrados) e o horizonte
    relevante nas últimas quatro reuniões."""
    ref = df[df["cenario"] == "juros_esperado"]
    if ref.empty:
        return ["Sem projeção no cenário com juros esperados."]

    def da_reuniao(nro):
        sub = ref[ref["nro_reuniao"] == nro]
        doc = "relatorio" if (sub["documento"] == "relatorio").any() else "comunicado"
        return sub[sub["documento"] == doc], doc

    nros = sorted(ref["nro_reuniao"].unique())
    sub, doc = da_reuniao(nros[-1])
    larga = sub.pivot_table(index="date", columns="indice", values="value", aggfunc="last")
    hr = set(sub.loc[sub["horizonte_relevante"] == 1, "date"])
    tipo = sub.groupby("date")["periodo_tipo"].first()
    linhas = []
    for d in larga.index:
        row = {"Período": esp._periodo(d, tipo[d])}
        for k, rot in (("ipca", "IPCA"), ("ipca_livres", "Livres"), ("ipca_administrados", "Administrados")):
            row[f"{rot} (%)"] = fmt(larga[k].get(d) if k in larga else None, 1)
        row[""] = "horizonte relevante" if d in hr else ""
        linhas.append(row)
    out = [f"Reunião {nros[-1]} (de {fdata(sub['vintage'].iloc[0])}), "
           f"{'Relatório de Política Monetária' if doc == 'relatorio' else 'comunicado'}, cenário "
           "de referência (juros da Focus). Valor = acumulado em quatro trimestres. Os condicionantes "
           "(petróleo, bandeira, câmbio) estão no texto do Copom e chegam pela IN-S4.", ""] + md_tabela(linhas)
    hist = []
    for nro in nros[-4:][::-1]:
        s, dc = da_reuniao(nro)
        h = s[(s["horizonte_relevante"] == 1) & (s["indice"] == "ipca")]
        if h.empty:
            continue
        x = h.iloc[0]
        hist.append({"Reunião": int(nro), "Documento": dc, "Data": fdata(x["vintage"]),
                     "Horizonte relevante": esp._periodo(x["date"], x["periodo_tipo"]),
                     "IPCA projetado (%)": fmt(x["value"], 1)})
    return out + ["", "O horizonte relevante nas últimas reuniões:", ""] + md_tabela(hist)


def focus_por_indicador(df: pd.DataFrame, ctx: Ctx) -> list[str]:
    """A Focus anual de cada componente, um bloco por indicador."""
    out = []
    for ind in sorted(df["indicador"].unique()):
        out += [f"**{ind}**", ""] + esp.focus_anual(df[df["indicador"] == ind], ctx) + [""]
    return out


def qpc_inflacao(df: pd.DataFrame, ctx: Ctx) -> list[str]:
    """O Questionário Pré-Copom mais recente, só o que é inflação: o curto prazo, o horizonte
    relevante com a probabilidade de desvio e o balanço de riscos."""
    df = df.copy()
    for c in ("referencia", "categoria", "estatistica", "variavel", "bloco"):
        df[c] = politica_monetaria._texto(df[c])
    nros = sorted(df["nro_reuniao"].unique())
    n0 = nros[-1]
    q0 = df[df["nro_reuniao"] == n0]

    def val(q, bloco, var, ref, est, cat=""):
        r = q[(q["bloco"] == bloco) & (q["variavel"] == var) & (q["referencia"] == ref)
              & (q["estatistica"] == est) & (q["categoria"] == cat)]
        return None if r.empty else float(r["valor"].iloc[0])

    linhas = []
    for bloco, var, rot in (("ipca_curto_prazo", "ipca", "IPCA no mês (%)"),
                            ("ipca_curto_prazo", "media_nucleos", "Média dos núcleos no mês (%)"),
                            ("ipca_curto_prazo", "servicos_subjacentes", "Serviços subjacentes no mês (%)"),
                            ("ipca_horizonte_relevante", "ipca_4t", "IPCA no horizonte relevante, 4 trimestres (%)")):
        for ref in sorted(q0.loc[(q0["bloco"] == bloco) & (q0["variavel"] == var), "referencia"].unique()):
            ant = df[(df["nro_reuniao"] < n0) & (df["bloco"] == bloco) & (df["variavel"] == var)
                     & (df["referencia"] == ref) & (df["estatistica"] == "mediana") & (df["categoria"] == "")]
            ant = ant.sort_values("nro_reuniao")
            linhas.append({"Variável": rot, "Referência": ref, "Mediana": fmt(val(q0, bloco, var, ref, "mediana")),
                           "p25 a p75": f"{fmt(val(q0, bloco, var, ref, 'p25'))} a "
                                        f"{fmt(val(q0, bloco, var, ref, 'p75'))}",
                           "Última vez perguntado": "—" if ant.empty else
                           f"{fmt(ant['valor'].iloc[-1])} (R{int(ant['nro_reuniao'].iloc[-1])})"})
    out = [f"QPC da reunião {n0} (publicado em {fdata(q0['date'].max())}). Medianas.", ""] + md_tabela(linhas)
    pd_ = q0[(q0["bloco"] == "ipca_horizonte_relevante") & (q0["variavel"] == "prob_desvio")
             & (q0["estatistica"] == "mediana")]
    if not pd_.empty:
        out += ["", "Probabilidade de o IPCA no horizonte relevante desviar da meta, mediana das "
                    "respostas: " + "; ".join(f"{c.replace('_', ' ').replace('0 5pp', '0,5 p.p.')} "
                                             f"{v:.0%}" for c, v in zip(pd_["categoria"], pd_["valor"])) + "."]
    vies = q0[(q0["bloco"] == "vies_ipca") & (q0["estatistica"] == "fracao")]
    if not vies.empty:
        out += ["", "Balanço de riscos do IPCA, fatia das respostas: "
                + " · ".join(f"{ref}: " + ", ".join(f"{c.replace('_', ' ')} {v:.0%}"
                                                   for c, v in zip(g["categoria"], g["valor"]))
                             for ref, g in vies.groupby("referencia")) + "."]
    return out


# ── a declaração ──────────────────────────────────────────────────────────────
TABELAS: list[Tabela] = [
    # ── i. Endógeno ──────────────────────────────────────────────────────────
    de(cambio, "inflc_agregados", series=_AGREGADOS, especial=agregados),
    Tabela("inflc_indice_geral", dims=("indice",), valor="numero_indice", especial=indice_geral),
    de(politica_monetaria, "inflc_decomposicao"),
    de(politica_monetaria, "inflc_decomposicao_item"),
    de(politica_monetaria, "inflc_dim"),
    de(politica_monetaria, "comm_icbr"),
    # ── ii. Endógeno de câmbio ───────────────────────────────────────────────
    so(cambio, "cmb_ptax", ("ptax_venda",)),
    # ── iii. Endógeno de política monetária ──────────────────────────────────
    de(cambio, "inflc_meta"),
    de(cambio, "pm_copom_projecoes", especial=copom_projecoes),
    # ── iv. Endógeno de atividade ────────────────────────────────────────────
    de(politica_monetaria, "pm_hiato_produto"),
    de(politica_monetaria, "atv_pms"),
    so(politica_monetaria, "mt_pnad", ("taxa_desocupacao", "rend_habitual_real_todos_trabalhos",
                                       "massa_real_habitual", "ocupado", "taxa_informalidade")),
    de(politica_monetaria, "mt_desocupacao_retro"),
    so(politica_monetaria, "mt_caged", ("caged_total", "caged_servicos")),
    # ── v. Endógeno de expectativas ──────────────────────────────────────────
    de(politica_monetaria, "expc_focus", series=(
        _s("IPCA|12m|S", "IPCA 12 meses à frente (suavizada)", "%", "dif"),
        _s("IPCA|24m|N", "IPCA 24 meses à frente", "%", "dif"),
        *[_s(f"IPCA {c}|12m|S", f"IPCA {c.lower()} 12 meses à frente (suavizada)", "%", "dif")
          for c in ("Livres", "Administrados", "Serviços", "Bens industrializados",
                    "Alimentação no domicílio")],
        _s("IGP-M|12m|S", "IGP-M 12 meses à frente (suavizada)", "%", "dif"),
    )),
    de(cambio, "expc_focus_periodo", recorte="IPCA"),
    Tabela("expc_focus_periodo", recorte="componentes", variante="inflacao",
           especial=focus_por_indicador,
           filtro="indicador IN ('IPCA Livres', 'IPCA Administrados', 'IPCA Serviços', "
                  "'IPCA Bens industrializados', 'IPCA Alimentação no domicílio', 'IGP-M') "
                  "AND periodicidade = 'anual' AND tipo_calculo = 'geral' AND base_calculo = 0 "
                  "AND detalhe = ''"),
    de(politica_monetaria, "expc_qpc", especial=qpc_inflacao),
    # ── vi. Endógeno de externo ──────────────────────────────────────────────
    de(cambio, "comm_icbr_usd"),
    de(cambio, "comm_brent"),
]


# ── leituras combinadas ───────────────────────────────────────────────────────
def _comp(x) -> float | None:
    x = pd.Series(x).dropna()
    return None if x.empty else float((np.prod(1 + x / 100) - 1) * 100)


def ipca_trimestral(ctx: Ctx) -> list[str]:
    """O IPCA e os quatro grupos por trimestre: a inflação do trimestre (a unidade da curva de
    Phillips do modelo) e o acumulado em 12 meses no fechamento (a variável da tese)."""
    w = _largo_agregados(ctx.ler("inflc_agregados"))
    cols = [k for k, _ in _GRUPOS if k in w]
    m = w[cols].loc[_INICIO_HIST:]
    ult = m["ipca"].dropna().index[-1]
    tri, doze = [], []
    for k in range(8, -1, -1):
        fim = (ult.to_period("Q") - k).end_time.normalize().replace(day=1)
        ini = fim - pd.DateOffset(months=2)
        bloco = m.loc[ini:fim]
        completo = len(bloco["ipca"].dropna()) == 3
        rot = esp._periodo(fim, "trimestre") + ("" if completo else f" (até {bloco['ipca'].dropna().index[-1]:%m/%Y})")
        rt, rd = {"Trimestre": rot}, {"Trimestre": rot}
        for c, nome in _GRUPOS:
            if c not in m:
                continue
            rt[nome] = fmt(_comp(bloco[c]))
            rd[nome] = fmt(_comp(m[c].loc[fim - pd.DateOffset(months=11):fim])) if completo else "—"
        tri.append(rt)
        doze.append(rd)
    return (["### O IPCA e os quatro grupos por trimestre", "",
             "Variação composta dos meses do trimestre (%, sem ajuste sazonal), como a curva de "
             "Phillips do Modelo Estrutural a lê. Os quatro grupos são os do modelo (classificação "
             "do BC). O trimestre em curso aparece com os meses que já saíram.", ""]
            + md_tabela(tri)
            + ["", "Acumulado em 12 meses no fechamento de cada trimestre (%), a variável da tese:", ""]
            + md_tabela(doze))


def sazonalidade(ctx: Ctx) -> list[str]:
    """O último mês e o último trimestre contra o mesmo período dos dez anos anteriores: o padrão
    sazonal medido, para separar sazonalidade de pressão."""
    w = _largo_agregados(ctx.ler("inflc_agregados"))
    series = list(_GRUPOS) + [("ipca_nucleo_ex03", "Núcleo EX3"), ("ipca_nucleo_medias_aparadas",
                                                                     "Núcleo médias aparadas")]
    linhas_m, linhas_t = [], []
    for c, nome in series:
        if c not in w:
            continue
        s = w[c].dropna()
        t0 = s.index[-1]
        anteriores = [t0 - pd.DateOffset(years=k) for k in range(1, 11)]
        ref = pd.Series([s.get(d) for d in anteriores], dtype=float).dropna()
        v = float(s.iloc[-1])
        linhas_m.append({"Série": nome, "Mês": f"{t0:%Y-%m}", "Último (%)": fmt(v),
                         "Mesmo mês, média 10a": fmt(ref.mean() if len(ref) else None),
                         "Mín–máx 10a": f"{fmt(ref.min())} a {fmt(ref.max())}" if len(ref) else "—",
                         "Anos abaixo do atual": f"{int((ref < v).sum())} de {len(ref)}",
                         "Último − média": fmt(v - ref.mean() if len(ref) else None, 2, True)})
        a3 = s.rolling(3).apply(lambda x: (np.prod(1 + x / 100) - 1) * 100, raw=True)
        v3 = float(a3.iloc[-1])
        ref3 = pd.Series([a3.get(d) for d in anteriores], dtype=float).dropna()
        linhas_t.append({"Série": nome, "3 meses até": f"{t0:%Y-%m}", "Acum. 3m (%)": fmt(v3),
                         "Mesma janela, média 10a": fmt(ref3.mean() if len(ref3) else None),
                         "Mín–máx 10a": f"{fmt(ref3.min())} a {fmt(ref3.max())}" if len(ref3) else "—",
                         "Anos abaixo do atual": f"{int((ref3 < v3).sum())} de {len(ref3)}"})
    return (["### O último mês contra o mesmo mês dos dez anos anteriores", "",
             "Sem ajuste sazonal: a comparação com o mesmo mês é o padrão sazonal medido. "
             "\"Anos abaixo do atual\" conta em quantos dos dez anos anteriores aquele mês foi menor.",
             ""] + md_tabela(linhas_m)
            + ["", "A mesma comparação para os três meses até o último:", ""] + md_tabela(linhas_t))


def monitorados_itens(ctx: Ctx) -> list[str]:
    """Os preços monitorados item a item (item do IBGE, 4 dígitos), do maior peso ao menor."""
    dec = ctx.ler("inflc_decomposicao")
    dec = dec[dec["indice"] == "IPCA"].assign(sub=lambda x: x["subitem_codigo"].astype(str))
    dim = ctx.ler("inflc_dim").assign(sub=lambda x: x["subitem_codigo"].astype(str))
    mon = dim[dim["subgrupo"] == "Monitorados"][["sub", "ibge_item"]]
    d = dec.merge(mon, on="sub", how="inner")
    d = d.assign(pv=d["pesos"] * d["var_mensal"])
    g = d.groupby(["ibge_item", "date"])[["pv", "pesos", "contribuicao"]].sum().reset_index()
    g["var"] = g["pv"] / g["pesos"]
    t0 = g["date"].max()
    linhas = []
    for item, x in g.groupby("ibge_item"):
        x = x.set_index("date").sort_index()
        if t0 not in x.index:
            continue
        v = x["var"]
        linhas.append({"Item": item, "Peso (%)": x.loc[t0, "pesos"] * 100,
                       "No mês (%)": fmt(v.loc[t0]), "Acum. 3m (%)": fmt(_comp(v.loc[:t0].iloc[-3:])),
                       "Acum. 12m (%)": fmt(_comp(v.loc[:t0].iloc[-12:])),
                       "Contribuição no mês (p.p.)": fmt(x.loc[t0, "contribuicao"], 3),
                       "Soma das contribuições 12m (p.p.)": fmt(x["contribuicao"].loc[:t0].iloc[-12:].sum(), 2)})
    linhas.sort(key=lambda r: -r["Peso (%)"])
    peso = sum(r["Peso (%)"] for r in linhas)
    for r in linhas:
        r["Peso (%)"] = fmt(r["Peso (%)"], 2)
    return (["### Os preços monitorados, item a item", "",
             f"IPCA de {t0:%Y-%m}. Subitens monitorados pela classificação do BC, somados no item do "
             f"IBGE; variação ponderada pelos pesos de cada mês. Peso dos monitorados no mês: "
             f"{fmt(peso, 1)}%. Nenhum destes canais está no Modelo Estrutural, salvo pela inércia e "
             "pela indexação ao IPCA (mapa, 2.7).", ""] + md_tabela(linhas))


COMBINADAS = [ipca_trimestral, sazonalidade, monitorados_itens]
