"""
As tabelas do agente de atividade (SISTEMA_AGENTES.md V.IV) e o F de cada uma.

A lista (quais tabelas) é decidida com o usuário e vive no SISTEMA_AGENTES.md; o gerador
levanta se esta declaração divergir dela. O tratamento (quais séries, que leitura) é do
sistema (IV.iv) e se ajusta pela qualidade do report.

Três coisas que valem para o arquivo inteiro:

  - Tabela que câmbio ou política monetária já declaram sai da declaração DELES (`de` e
    `so`, do motor), trocando só séries e leitura: a consulta fica idêntica e o A do ciclo,
    que é compartilhado, serve aos três. É o caso de quase todas, inclusive as que passaram
    a ser endógenas daqui (o hiato do BC, as contas nacionais, o mercado de trabalho).
  - A Focus do PIB sai da declaração de expectativas (`de`): mesma consulta, mesmo arquivo de
    A, só o F próprio muda. A da desocupação, que expectativas não declara (V.VII não a
    lista), segue com `variante="atividade"`, em arquivo próprio de A, até o dono declarar.
  - Profundidade (PRINCIPIOS I.II.vii): só o grupo "Endógeno" ganha a leitura completa;
    os de consulta e o TWA, a enxuta. O motor decide pelo nome do grupo.

As duas leituras combinadas respondem o que nenhuma tabela sozinha dá: o trimestre em
curso pelos indicadores mensais (Q1 do mapa) e o potencial implícito no hiato do BC, que
é a peça mecânica da linha companheira da tese (PIB interanual = potencial + Δ4 do hiato).
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from analytics.agent_system.dados import cambio, expectativas
from analytics.agent_system.dados import especiais as esp
from analytics.agent_system.dados import politica_monetaria as pm
from analytics.agent_system.dados.motor import (Ctx, Serie, Tabela, de, em, fdata, fmt,
                                                md_tabela, pctl, so)

SECAO = ("## (V.IV) Agente de atividade", "## (V.V)")
PIB = None

_FOCUS = "tipo_calculo = 'geral' AND base_calculo = 0 AND detalhe = ''"
_FOCUS_PIB = ("PIB Total", "PIB Agropecuária", "PIB Indústria", "PIB Serviços",
              "PIB Despesa de consumo das famílias", "PIB Despesa de consumo da administração pública",
              "PIB Formação Bruta de Capital Fixo", "PIB Exportação de bens e serviços",
              "PIB Importação de bens e serviços")


def _s(chave, rotulo, unidade, leitura, **kw) -> Serie:
    return Serie(chave, rotulo, unidade, leitura, **kw)


def _tri(d) -> str:
    return esp._periodo(pd.Timestamp(d), "trimestre")


# ── F próprio das endógenas (leitura completa) ────────────────────────────────
_TAXAS = (("pib_pm", "PIB"), ("agropecuaria", "Agropecuária"), ("industria", "Indústria"),
          ("ind_transformacao", "  Transformação"), ("ind_extrativas", "  Extrativa"),
          ("construcao", "  Construção"), ("servicos", "Serviços"),
          ("consumo_familias", "Consumo das famílias"), ("consumo_adm_publica", "Consumo do governo"),
          ("fbcf", "FBCF"), ("exportacao", "Exportação"), ("importacao", "Importação"))


def pib_taxas(df: pd.DataFrame, ctx: Ctx) -> list[str]:
    """As taxas oficiais do IBGE nos últimos cinco trimestres: contra o trimestre anterior
    (dessazonalizada) e contra o mesmo trimestre do ano anterior, por componente."""
    w = df.pivot_table(index="date", columns=["name", "indicador"], values="value", aggfunc="last").sort_index()
    datas = list(w.index[-5:])
    out = []
    for ind, titulo in (("qoq", "Contra o trimestre anterior, dessazonalizada (%)"),
                        ("yoy", "Contra o mesmo trimestre do ano anterior (%)")):
        linhas = []
        for k, rot in _TAXAS:
            if (k, ind) not in w:
                continue
            row = {"Componente": rot}
            for d in datas:
                row[_tri(d)] = fmt(w[(k, ind)].get(d), 1)
            if ctx.completo:
                s = w[(k, ind)].dropna()
                row["Pctl hist. do último"] = fmt(pctl(s, s.iloc[-1]) if len(s) else None, 0)
            linhas.append(row)
        out += [f"**{titulo}**", ""] + md_tabela(linhas) + [""]
    a4 = w[("pib_pm", "acum_4t")].dropna() if ("pib_pm", "acum_4t") in w else pd.Series(dtype=float)
    if not a4.empty:
        out.append(f"PIB acumulado em quatro trimestres até {_tri(a4.index[-1])}: {fmt(a4.iloc[-1], 1)}%. "
                   "Taxas oficiais do IBGE (impostos sem taxa contra o trimestre anterior).")
    return out


def hiato_vintages(df: pd.DataFrame, ctx: Ctx) -> list[str]:
    """A revisão do hiato e o placar: a central de cada trimestre recente nas últimas
    edições, e na primeira edição depois do PIB do IBGE daquele trimestre, a do fechamento do
    trimestre seguinte (a do placar)."""
    c = df[df["variavel"] == "central"]
    w = c.pivot_table(index="date", columns="vintage", values="value", aggfunc="last").sort_index()
    if w.empty:
        return []
    eds = list(w.columns[-4:])
    linhas = []
    for d, x in w.tail(8).iloc[::-1].iterrows():
        row = {"Trimestre": _tri(d)}
        placar = pd.Timestamp(d) + pd.DateOffset(months=5)         # fechamento do trimestre seguinte
        row["Placar: 1º RPM após o PIB"] = (f"{fmt(x.get(placar))} ({placar:%Y-%m})"
                                            if placar in w.columns else "ainda não saiu")
        for v in eds:
            row[f"Edição {pd.Timestamp(v):%Y-%m}"] = fmt(x.get(v))
        if len(eds) > 1:
            a, b = x.get(eds[-1]), x.get(eds[-2])
            row["Revisão na última (p.p.)"] = fmt(None if pd.isna(a) or pd.isna(b) else a - b, 2, True)
        linhas.append(row)
    return [f"{w.shape[1]} edições, desde {pd.Timestamp(w.columns[0]):%Y-%m}. Central, % do potencial. "
            "O placar do hiato de um trimestre é a central do primeiro RPM depois do PIB do IBGE "
            "daquele trimestre (a edição do fechamento do trimestre seguinte); a quebra metodológica entre 2024-06 e 2024-09 deixa só a central comparável.",
            ""] + md_tabela(linhas)


# ── F próprio da consulta a expectativas (leitura enxuta) ─────────────────────
def _focus(df: pd.DataFrame, ctx: Ctx, indicadores, anos: int = 3) -> list[str]:
    """Mediana da Focus: a pesquisa mais recente contra 4 semanas antes, por trimestre e por
    ano de referência."""
    datas = sorted(pd.DatetimeIndex(df["date"].unique()))
    d0 = datas[-1]
    d4 = esp._pesquisa_em(datas, d0 - pd.Timedelta(days=28))
    out = [f"Pesquisa de {fdata(d0)}; 4 semanas antes: {fdata(d4)}. Mediana.", ""]

    def med(d, ind, per, ref):
        if d is None:
            return None
        r = df[(df["date"] == d) & (df["indicador"] == ind) & (df["periodicidade"] == per)
               & (df["data_referencia"].astype(str) == ref)]
        return None if r.empty else float(r["mediana"].iloc[0])

    tri = df[(df["date"] == d0) & (df["periodicidade"] == "trimestral")]
    for ind in [i for i in indicadores if i in set(tri["indicador"])]:
        refs = tri[tri["indicador"] == ind].sort_values("ref_date")
        linhas = []
        for r in refs.itertuples():
            v0, v4 = r.mediana, med(d4, ind, "trimestral", str(r.data_referencia))
            linhas.append({"Trimestre": _tri(r.ref_date), "Mediana": fmt(v0),
                           "4 sem. antes": fmt(v4),
                           "Δ 4 sem.": fmt(None if v4 is None else v0 - v4, 2, True),
                           "Respondentes": "—" if pd.isna(r.numero_respondentes) else int(r.numero_respondentes)})
        un = refs["unidade"].dropna().iloc[0] if refs["unidade"].notna().any() else "—"
        out += [f"**{ind}, trimestral** (unidade: {un})", ""] + md_tabela(linhas) + [""]

    an = df[(df["date"] == d0) & (df["periodicidade"] == "anual")]
    anos_ref = sorted({str(a) for a in an["data_referencia"].astype(str)})[:anos]
    linhas = []
    for ind in [i for i in indicadores if i in set(an["indicador"])]:
        row = {"Indicador": ind}
        for a in anos_ref:
            v0, v4 = med(d0, ind, "anual", a), med(d4, ind, "anual", a)
            row[a] = fmt(v0)
            row[f"Δ 4 sem. {a}"] = fmt(None if v0 is None or v4 is None else v0 - v4, 2, True)
        linhas.append(row)
    if linhas:
        out += ["**Anual** (variação no ano para o PIB e os componentes; taxa no fim do ano para a "
                "desocupação)", ""] + md_tabela(linhas)
    return out


def focus_pib(df: pd.DataFrame, ctx: Ctx) -> list[str]:
    return _focus(df, ctx, _FOCUS_PIB)


def focus_desocupacao(df: pd.DataFrame, ctx: Ctx) -> list[str]:
    return _focus(df, ctx, ("Taxa de desocupação",))


def qpc(df: pd.DataFrame, ctx: Ctx) -> list[str]:
    """O que o QPC diz da atividade: PIB trimestral e hiato do mercado, o balanço de riscos do
    PIB e as variáveis estruturais (potencial, NAIRU, neutro), cada uma na edição mais recente
    em que foi perguntada."""
    df = df.copy()
    for c in ("referencia", "categoria", "estatistica", "variavel", "bloco"):
        df[c] = pm._texto(df[c])
    n0 = df["nro_reuniao"].max()
    q0 = df[df["nro_reuniao"] == n0]
    out = [f"QPC da reunião {int(n0)} (publicado em {fdata(q0['date'].max())}).", ""]

    def val(q, bloco, var, ref, est="mediana"):
        r = q[(q["bloco"] == bloco) & (q["variavel"] == var) & (q["referencia"] == ref)
              & (q["estatistica"] == est) & (q["categoria"] == "")]
        return None if r.empty else float(r["valor"].iloc[0])

    def anterior(bloco, var, ref):
        r = df[(df["nro_reuniao"] < n0) & (df["bloco"] == bloco) & (df["variavel"] == var)
               & (df["referencia"] == ref) & (df["estatistica"] == "mediana") & (df["categoria"] == "")]
        if r.empty:
            return "—"
        x = r.sort_values("nro_reuniao").iloc[-1]
        return f"{fmt(x['valor'])} (R{int(x['nro_reuniao'])})"

    linhas = []
    for bloco, var, rot in (("hiato", "hiato", "Hiato do produto (% do potencial)"),
                            ("pib_trimestral", "qoq_sa", "PIB, contra o trimestre anterior, dessaz. (%)"),
                            ("pib_trimestral", "yoy", "PIB, contra o mesmo trimestre do ano anterior (%)")):
        for ref in sorted(q0.loc[(q0["bloco"] == bloco) & (q0["variavel"] == var), "referencia"].unique()):
            linhas.append({"Variável": rot, "Referência": ref, "Mediana": fmt(val(q0, bloco, var, ref)),
                           "p25 a p75": f"{fmt(val(q0, bloco, var, ref, 'p25'))} a "
                                        f"{fmt(val(q0, bloco, var, ref, 'p75'))}",
                           "Última vez perguntado": anterior(bloco, var, ref)})
    out += ["Medianas do mercado. \"Última vez perguntado\": o QPC anterior mais recente com a mesma "
            "pergunta e a mesma referência.", ""] + md_tabela(linhas) + [""]

    r = q0[(q0["bloco"] == "vies_pib") & (q0["estatistica"] == "fracao")]
    linhas = [{"Ano": ref, "Respostas": "; ".join(f"{c.replace('_', ' ')} {v:.0%}"
                                                  for c, v in zip(g["categoria"], g["valor"]))}
              for ref, g in r.groupby("referencia")]
    if linhas:
        out += ["Balanço de riscos do PIB, fatia das respostas:", ""] + md_tabela(linhas) + [""]

    linhas = []
    for var, rot in (("pib_potencial", "Crescimento do PIB potencial (%)"),
                     ("nairu", "Taxa de desemprego neutra, NAIRU (%)"),
                     ("juro_real_neutro", "Juro real neutro (% a.a.)")):
        rr = df[(df["variavel"] == var) & (df["estatistica"] == "mediana")]
        if rr.empty:
            continue
        nro = rr["nro_reuniao"].max()
        for x in rr[rr["nro_reuniao"] == nro].itertuples():
            ant = rr[(rr["nro_reuniao"] < nro) & (rr["referencia"] == x.referencia)].sort_values("nro_reuniao")
            linhas.append({"Variável estrutural": rot, "Horizonte": x.referencia.replace("_", " ") or "—",
                           "Mediana": fmt(x.valor), "QPC": f"R{int(nro)} ({fdata(x.date)})",
                           "Na pergunta anterior": "—" if ant.empty else
                           f"{fmt(ant['valor'].iloc[-1])} (R{int(ant['nro_reuniao'].iloc[-1])})"})
    if linhas:
        out += ["Perguntadas só em algumas reuniões; vale a mais recente:", ""] + md_tabela(linhas)
    return out


# ── a declaração ──────────────────────────────────────────────────────────────
TABELAS: list[Tabela] = [
    # ── i. Endógeno ──────────────────────────────────────────────────────────
    de(pm, "atv_pib"),
    de(pm, "atv_pib_taxas", especial=pib_taxas),
    de(pm, "atv_pib_valores_correntes"),
    de(pm, "atv_pib_mensal"),
    de(pm, "atv_ibcbr"),
    de(pm, "atv_pim", series=tuple(
        _s(f"{k}|Y", rot, "índice, dessaz.", "pct") for k, rot in (
            ("industria_geral", "Indústria geral"), ("ind_transformacao", "Transformação"),
            ("ind_extrativas", "Extrativa")))),
    de(pm, "atv_pim_uso"),
    de(pm, "atv_pmc"),
    de(pm, "atv_pms"),
    de(pm, "atv_renda_poupanca"),
    de(pm, "pm_hiato_produto"),
    de(pm, "pm_hiato_produto_vintages", especial=hiato_vintages),
    de(pm, "mt_pnad", series=(
        _s("taxa_desocupacao", "Taxa de desocupação", "%", "dif", casas=1),
        _s("taxa_participacao", "Taxa de participação", "%", "dif", casas=1),
        _s("nivel_ocupacao", "Nível de ocupação", "% da PIA", "dif", casas=1),
        _s("taxa_subutil_composta", "Subutilização composta", "%", "dif", casas=1),
        _s("taxa_informalidade", "Informalidade", "% dos ocupados", "dif", casas=1),
        _s("ocupado", "Ocupados", "mil pessoas", "pct", casas=0),
        _s("rend_habitual_real_todos_trabalhos", "Rendimento habitual real", "R$", "pct", casas=0),
        _s("massa_real_habitual", "Massa de rendimento habitual real", "R$ bi", "pct", escala=1000.0, casas=1),
    )),
    de(pm, "mt_desocupacao_retro"),
    de(pm, "mt_caged"),
    de(pm, "mt_caged_setor"),
    # ── ii. Endógeno de política monetária ───────────────────────────────────
    so(pm, "br_interest_rate", ("POLICY|1d", "NTNBJS|24M", "NTNBJS|120M")),
    de(cambio, "pm_copom_reuniao"),
    de(cambio, "inflc_meta"),
    # ── iii. Endógeno de câmbio ──────────────────────────────────────────────
    so(cambio, "cmb_ptax", ("ptax_venda",)),
    de(cambio, "cmb_termos_troca"),
    so(cambio, "cmb_comex_produto", ("mundo_export", "petroleo_export", "soja_export",
                                     "minerio_ferro_export", "carnes_export", "cafe_export")),
    so(cambio, "cmb_comex_pais", ("mundo_export", "mundo_import", "china_export", "eua_export",
                                  "argentina_export")),
    # ── iv. Endógeno de inflação ─────────────────────────────────────────────
    de(cambio, "inflc_agregados", series=tuple(
        _s(k, rot, "%", "var_mensal") for k, rot in (
            ("ipca", "IPCA"), ("ipca_livres", "Livres"), ("ipca_servicos", "Serviços"),
            ("ipca_alimentacao", "Alimentação"), ("ipca_administrado", "Administrados")))),
    de(pm, "comm_icbr"),
    # ── v. Endógeno de fiscal ────────────────────────────────────────────────
    de(pm, "fisc_efgg"),
    de(pm, "fisc_rtn"),
    so(cambio, "fisc_nfsp", ("resultado_primario_pct_pib_12m", "resultado_nominal_pct_pib_12m")),
    de(cambio, "cmb_risco_pais"),
    # ── vi. Endógeno de externo ──────────────────────────────────────────────
    de(cambio, "comm_icbr_usd"),
    # ── vii. Endógeno de expectativas ────────────────────────────────────────
    de(expectativas, "expc_focus_periodo", recorte="PIB", especial=focus_pib),
    Tabela("expc_focus_periodo", recorte="desocupação", variante="atividade", especial=focus_desocupacao,
           filtro=_FOCUS + " AND periodicidade IN ('anual', 'trimestral') "
                           "AND indicador = 'Taxa de desocupação'"),
    de(pm, "expc_qpc", especial=qpc),
    # ── viii. TWA — crédito ──────────────────────────────────────────────────
    de(pm, "cred_credito_resumo"),
    de(pm, "cred_fluxo_financeiro"),
    de(pm, "cred_ptc"),
    de(pm, "cred_credito_familias"),
    de(pm, "cred_credito_amplo"),
    de(pm, "cred_modalidade_livre_pf"),
    de(pm, "cred_modalidade_livre_pj"),
    de(pm, "cred_modalidade_direcionado_pj"),
]


# ── leituras combinadas ───────────────────────────────────────────────────────
_MENSAIS = (("atv_ibcbr", "ibcbr_sa", "IBC-Br"),
            ("atv_ibcbr", "ibcbr_ex_agropecuaria_sa", "IBC-Br ex-agropecuária"),
            ("atv_pim", "industria_geral|Y", "Indústria geral"),
            ("atv_pim_uso", "bens_capital|Y", "Bens de capital"),
            ("atv_pim_uso", "bens_consumo_duraveis|Y", "Bens de consumo duráveis"),
            ("atv_pmc", "comercio_restrito_total|Y", "Varejo restrito"),
            ("atv_pmc", "comercio_ampliado_total|Y", "Varejo ampliado"),
            ("atv_pms", "servicos_total|Y", "Serviços"))


def trimestre_em_curso(ctx: Ctx) -> list[str]:
    """O trimestre pelos indicadores mensais dessazonalizados: a média dos meses já
    publicados do trimestre da última leitura contra a média do trimestre anterior, o
    carrego (último mês contra a média do anterior) e o trimestre anterior fechado."""
    linhas = []
    for nome, chave, rot in _MENSAIS:
        s = ctx.serie(nome, chave)
        if s.empty:
            continue
        s = s.resample("MS").last().dropna()
        q = s.groupby(s.index.to_period("Q"))
        med, n = q.mean(), q.size()
        t0 = s.index[-1]
        p0 = t0.to_period("Q")
        if p0 - 1 not in med.index:
            continue
        ant, ant2 = med[p0 - 1], med.get(p0 - 2)
        fechado = n.get(p0, 0) == 3
        linhas.append({
            "Indicador": rot, "Último mês": f"{t0:%Y-%m}",
            "Trimestre": f"{_tri(t0)} ({n.get(p0, 0)} de 3 meses)",
            "Média do tri contra o anterior (%)": fmt((med[p0] / ant - 1) * 100, 1, True),
            "Carrego: último mês contra o tri anterior (%)": fmt((s.iloc[-1] / ant - 1) * 100, 1, True),
            f"{_tri((p0 - 1).start_time)} contra {_tri((p0 - 2).start_time)} (%)":
                fmt(None if ant2 is None else (ant / ant2 - 1) * 100, 1, True),
            "Situação": "fechado" if fechado else "parcial"})
    caged = ctx.serie("mt_caged", "caged_total")
    out = ["### O trimestre pelos indicadores mensais", "",
           "Índices dessazonalizados. \"Carrego\": quanto o trimestre cresce sobre o anterior se os "
           "meses que faltam repetirem o último. O trimestre de cada linha é o do último mês publicado "
           "daquele indicador, e eles não andam juntos.", ""] + md_tabela(linhas)
    if not caged.empty:
        c = caged.resample("MS").last().dropna()
        saldo = c.diff().dropna()
        out += ["", f"Emprego formal (CAGED, estoque sem ajuste sazonal), até {c.index[-1]:%Y-%m}: "
                    f"saldo de {fmt(saldo.iloc[-3:].sum() / 1000, 0)} mil em 3 meses e "
                    f"{fmt(saldo.iloc[-12:].sum() / 1000, 0)} mil em 12 meses."]
    return out


def hiato_e_potencial(ctx: Ctx) -> list[str]:
    """A peça mecânica da linha companheira da tese. Com o hiato h da edição corrente e o
    PIB interanual g oficial, o potencial implícito em cada trimestre é g − (h − h de quatro
    trimestres antes); a média dos últimos quatro é o potencial da tradução
    PIB interanual (q) = potencial + h(q) − h(q − 4), com h(q) do modelo."""
    tx = ctx.ler("atv_pib_taxas")
    g = (tx[(tx["name"] == "pib_pm") & (tx["indicador"] == "yoy")].set_index("date")["value"]
         .sort_index())
    hd = ctx.ler("pm_hiato_produto")
    h = (hd[hd["variavel"] == "central"].set_index("date")["value"].sort_index())
    g.index, h.index = g.index.to_period("Q"), h.index.to_period("Q")
    h = h.reindex(pd.period_range(h.index.min(), h.index.max(), freq="Q"))
    d4 = h - h.shift(4)
    pot = (g - d4).dropna()
    linhas = []
    for p in pot.index[-8:][::-1]:
        linhas.append({"Trimestre": _tri(p.start_time), "PIB interanual (%)": fmt(g[p], 1),
                       "Hiato (%)": fmt(h[p]), "Hiato 4 tri antes (%)": fmt(h.get(p - 4)),
                       "Potencial implícito (%)": fmt(pot[p], 2)})
    media = float(pot.iloc[-4:].mean()) if len(pot) >= 4 else None
    out = ["### O hiato do BC e o potencial implícito nele", "",
           f"Hiato da edição de {fdata(hd['vintage'].max())}; PIB interanual oficial do IBGE. "
           "Potencial implícito = PIB interanual − (hiato − hiato de 4 trimestres antes).", ""] + md_tabela(linhas)
    out += ["", f"**Potencial da linha companheira** (média dos últimos 4 trimestres): "
                f"{fmt(media, 2)}% ao ano. PIB interanual de um trimestre projetado = este potencial + "
                "hiato do modelo no trimestre − hiato quatro trimestres antes (observado ou do modelo). "
                "A conta é mecânica, não tempero."]
    if h.index.max() > (g.index.max() if len(g) else h.index.max()):
        p = h.index.max()
        out.append(f"O hiato já tem {_tri(p.start_time)} (nowcast do BC) e o PIB oficial ainda não: "
                   f"na tradução, {_tri(p.start_time)} dá {fmt(media + h[p] - h.get(p - 4) if media is not None and h.get(p - 4) is not None else None, 2)}% "
                   "de PIB interanual implícito no hiato do BC.")
    # a folga no mercado de trabalho contra a NAIRU do mercado
    u = ctx.serie("mt_desocupacao_retro", "value")
    q = ctx.ler("expc_qpc")
    nai = q[(q["variavel"].astype(str) == "nairu") & (q["estatistica"].astype(str) == "mediana")]
    if not u.empty and not nai.empty:
        nro = nai["nro_reuniao"].max()
        cp = nai[(nai["nro_reuniao"] == nro)]
        partes = "; ".join(f"{pm._texto(pd.Series([x.referencia])).iloc[0].replace('_', ' ')} "
                           f"{fmt(x.valor)}% (desocupação {fmt(u.iloc[-1] - x.valor, 2, True)} p.p. contra ela)"
                           for x in cp.itertuples())
        out += ["", f"Desocupação dessazonalizada do BC em {u.index[-1]:%Y-%m}: {fmt(u.iloc[-1], 2)}%. "
                    f"NAIRU do QPC da reunião {int(nro)}, mediana: {partes}. Abaixo da NAIRU = mercado "
                    "de trabalho apertado."]
    return out


COMBINADAS = [trimestre_em_curso, hiato_e_potencial]
