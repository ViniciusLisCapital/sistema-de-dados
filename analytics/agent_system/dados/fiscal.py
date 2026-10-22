"""
As tabelas do agente fiscal (SISTEMA_AGENTES.md V.V) e o F de cada uma.

A lista (quais tabelas) é decidida com o usuário e vive no SISTEMA_AGENTES.md; o gerador
levanta se esta declaração divergir dela. O tratamento (quais séries, que leitura) é do
sistema (IV.iv) e se ajusta pela qualidade do report.

O que vale para o arquivo inteiro:

  - A prioridade do agente é a discussão (ii) do mapa: o efeito da política fiscal sobre a
    atividade e a inflação (postura, crescimento real das despesas, impulso, demanda do
    governo no PIB). Por isso as leituras próprias são a despesa em termos reais, por grupo,
    e o impulso em quatro medidas lado a lado; a discussão (i), as contas, fica com a
    leitura padrão.
  - Tabela que câmbio ou PM já declaram sai da declaração deles (`de`/`so` do motor), trocando
    só séries ou leitura: a consulta fica idêntica e o A do ciclo, que é compartilhado, serve
    aos dois.
  - Tabela de outro agente NOVO que câmbio e PM não declaram (o recorte fiscal da Focus) leva
    `variante="fiscal"`, para não depender de um módulo que ainda está sendo escrito. Será
    unificada depois.
  - Profundidade (PRINCIPIOS I.II.vii): só o grupo "Endógeno" ganha a leitura completa.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from analytics.agent_system.dados import cambio, politica_monetaria as pm
from analytics.agent_system.dados import especiais as esp
from analytics.agent_system.dados.motor import (Ctx, Serie, Tabela, antes, bloco_generico, de, em,
                                                fdata, fmt, md_tabela, so)

SECAO = ("## (V.V) Agente fiscal", "## (V.VI)")
PIB = None

_BI = 1000.0  # R$ milhões -> R$ bilhões


def _s(chave, rotulo, unidade, leitura, **kw) -> Serie:
    return Serie(chave, rotulo, unidade, leitura, **kw)


# ── auxiliares ────────────────────────────────────────────────────────────────
def _indice_ipca(ctx: Ctx) -> pd.Series:
    """Número-índice do IPCA (mês a mês), da variação mensal em `inflc_agregados`."""
    v = ctx.serie("inflc_agregados", "ipca")
    return (1 + v / 100).cumprod() if not v.empty else v


def _pib12(ctx: Ctx) -> pd.Series:
    return ctx.serie("atv_pib_mensal", "pib_acum_12m")


def _real_12m(flow: pd.Series, p: pd.Series) -> tuple[float | None, float | None, float | None]:
    """(soma 12m nominal, soma 12m um ano antes, crescimento real 12m contra 12m em %)."""
    f = flow.dropna()
    if len(f) < 24:
        return None, None, None
    f = f.iloc[-24:]
    pr = p.reindex(f.index)
    s0, s1 = f.iloc[-12:].sum(), f.iloc[:12].sum()
    if pr.isna().any():
        return s0, s1, None
    r = f / pr
    return s0, s1, (r.iloc[-12:].sum() / r.iloc[:12].sum() - 1) * 100


# ── F próprio das endógenas ───────────────────────────────────────────────────
_RTN_GRUPOS = (
    ("receita_liquida", "Receita líquida"),
    ("despesa_total", "Despesa total"),
    ("beneficios_previdenciarios", "Benefícios previdenciários"),
    ("pessoal_encargos_sociais", "Pessoal e encargos"),
    ("beneficios_de_prestacao_continuada_da_loas_rmv", "BPC/LOAS"),
    ("abono_e_seguro_desemprego", "Abono e seguro-desemprego"),
    ("obrigatorias_com_controle_de_fluxo", "Obrigatórias com controle de fluxo (inclui Bolsa Família)"),
    ("obrigatorias_com_controle_de_fluxo_bolsa_familia", "  dessas, Bolsa Família"),
    ("subsidios_subvencoes_e_proagro", "Subsídios, subvenções e Proagro"),
    ("sentencas_judiciais_e_precatorios_custeio_e_capital", "Sentenças judiciais e precatórios"),
    ("despesas_discricionarias_do_poder_executivo", "Discricionárias do Executivo"),
    ("resultado_primario_governo_central", "Resultado primário do governo central (+ = superávit)"),
)


def rtn(df: pd.DataFrame, ctx: Ctx) -> list[str]:
    """O governo central em 12 meses: nível, % do PIB e crescimento real, por grupo."""
    w = df.pivot_table(index="date", columns="name", values="value", aggfunc="last").sort_index()
    t0 = w.index[-1]
    p = _indice_ipca(ctx)
    pib = em(_pib12(ctx), t0)
    linhas = []
    for k, rot in _RTN_GRUPOS:
        if k not in w:
            continue
        s0, s1, real = _real_12m(w[k], p)
        if s0 is None:
            continue
        if k.startswith("resultado_"):
            real = None                     # crescimento de um saldo que troca de sinal não diz nada
        linhas.append({"Grupo": rot, "12m (R$ bi)": fmt(s0 / _BI, 1),
                       "12m % do PIB": fmt(s0 / pib * 100 if pib else None, 2),
                       "12m um ano antes (R$ bi)": fmt(s1 / _BI, 1),
                       "Cresc. real 12m (%)": fmt(real, 1, True)})
    ult_ipca = p.index[-1] if not p.empty else None
    out = [f"Governo central, acima da linha, R$ correntes, 12 meses até {t0:%Y-%m}. Crescimento "
           "real: soma dos 12 meses deflacionada mês a mês pelo IPCA contra a dos 12 meses "
           f"anteriores (IPCA até {fdata(ult_ipca)}; mês sem IPCA deixa a célula em branco). "
           "% do PIB sobre o PIB nominal de 12 meses. Precatórios e créditos extraordinários "
           "movem os totais sem mudar a postura: leia os grupos.", ""] + md_tabela(linhas)
    # O trimestre: o último trimestre fechado contra o mesmo do ano anterior, em termos reais.
    q = w.index[w.index.month % 3 == 0]
    if len(q):
        qf = q[-1]
        meses = pd.date_range(qf - pd.DateOffset(months=2), qf, freq="MS")
        ant = meses - pd.DateOffset(years=1)
        tri = []
        for k, rot in _RTN_GRUPOS[:3] + (_RTN_GRUPOS[-2],):
            if k not in w:
                continue
            a, b = w[k].reindex(meses), w[k].reindex(ant)
            pa, pb = p.reindex(meses), p.reindex(ant)
            ok = not (a.isna().any() or b.isna().any() or pa.isna().any() or pb.isna().any())
            tri.append({"Grupo": rot, f"{esp._periodo(qf, 'trimestre')} (R$ bi)": fmt(a.sum() / _BI, 1),
                        "Mesmo trimestre do ano anterior (R$ bi)": fmt(b.sum() / _BI, 1),
                        "Cresc. real (%)": fmt(((a / pa).sum() / (b / pb).sum() - 1) * 100 if ok else None, 1, True)})
        out += ["", "Último trimestre fechado contra o mesmo trimestre do ano anterior:", ""] + md_tabela(tri)
    return out


_EFGG = (
    ("geral_despesa_total", "Despesa total"),
    ("geral_juros", "Juros"),
    ("geral_beneficios_previdenciarios_assistenciais", "Benefícios previdenciários e assistenciais"),
    ("geral_remuneracao_empregados", "Remuneração de empregados"),
    ("geral_uso_bens_servicos", "Uso de bens e serviços"),
    ("geral_subsidios", "Subsídios"),
    ("geral_investimento_liquido", "Investimento líquido"),
    ("geral_receita_total", "Receita total"),
)


def _soma4(w: pd.DataFrame, k: str) -> pd.Series:
    return w[k].rolling(4).sum() if k in w else pd.Series(dtype=float)


def efgg(df: pd.DataFrame, ctx: Ctx) -> list[str]:
    """O governo geral por natureza, em 4 trimestres: % do PIB, Δ em um ano e crescimento real."""
    w = df.pivot_table(index="date", columns="name", values="value", aggfunc="last").sort_index()
    if "geral_despesa_total" in w and "geral_juros" in w:
        w["_primaria"] = w["geral_despesa_total"] - w["geral_juros"]
    pibq = ctx.ler("atv_pib_valores_correntes")
    pibq = pibq[pibq["name"] == "pib_pm"].set_index("date")["value"].sort_index().rolling(4).sum()
    p = _indice_ipca(ctx)
    pq = p.resample("QS").mean() if not p.empty else p
    t0 = w.index[-1]
    t1 = antes(t0, 12)
    linhas = []
    for k, rot in (("_primaria", "Despesa exceto juros"),) + _EFGG:
        s = _soma4(w, k)
        if s.empty or pd.isna(em(s, t0)):
            continue
        v0, v1 = em(s, t0), em(s, t1)
        p0, p1 = em(pibq, t0), em(pibq, t1)
        g0 = v0 / p0 * 100 if p0 else None
        g1 = v1 / p1 * 100 if p1 and v1 is not None else None
        r = w[k].iloc[-8:] / pq.reindex(w.index[-8:]).values if len(w) >= 8 else None
        real = ((r.iloc[-4:].sum() / r.iloc[:4].sum() - 1) * 100
                if r is not None and not r.isna().any() else None)
        linhas.append({"Conta": rot, f"% do PIB, 4 tri até {esp._periodo(t0, 'trimestre')}": fmt(g0, 1),
                       "Um ano antes": fmt(g1, 1),
                       "Δ (p.p. do PIB)": fmt(None if g0 is None or g1 is None else g0 - g1, 1, True),
                       "Cresc. real 4 tri (%)": fmt(real, 1, True)})
    return ["Governo geral (GFSM) = SOMA de União, estados e municípios, sem consolidar as "
            "transferências entre esferas: o nível fica acima do governo geral consolidado; leia a "
            "variação. Soma de 4 trimestres sobre o PIB nominal dos mesmos 4; real = deflacionado "
            "pela média trimestral do IPCA. A Δ da despesa exceto juros em % do PIB é a medida de "
            "impulso pela despesa (+ = expansionista).", ""] + md_tabela(linhas)


def investimento(df: pd.DataFrame, ctx: Ctx) -> list[str]:
    """O investimento federal (GND 4) e as inversões (GND 5) em 12 meses, em termos reais."""
    d = df[df["corte"] == "natureza"]
    w = d.pivot_table(index="date", columns="item", values="value", aggfunc="last").sort_index()
    p = _indice_ipca(ctx)
    t0 = w.index[-1]
    pib = em(_pib12(ctx), t0)
    linhas = []
    for k, rot in (("total", "Total (GND 4 + 5)"), ("gnd4", "GND 4, investimentos"),
                   ("gnd4__aplicacoes_diretas__obras_instalacoes", "  obras e instalações"),
                   ("gnd4__aplicacoes_diretas__equipamentos_material_permanente", "  equipamentos"),
                   ("gnd4__transf_estados_df", "  transferências a estados"),
                   ("gnd4__transf_municipios", "  transferências a municípios"),
                   ("gnd5", "GND 5, inversões financeiras")):
        if k not in w:
            continue
        s0, s1, real = _real_12m(w[k], p)
        if s0 is None:
            continue
        linhas.append({"Item": rot, "12m (R$ bi)": fmt(s0 / _BI, 1),
                       "12m % do PIB": fmt(s0 / pib * 100 if pib else None, 2),
                       "12m um ano antes (R$ bi)": fmt(s1 / _BI, 1),
                       "Cresc. real 12m (%)": fmt(real, 1, True)})
    return [f"Governo federal, pago, 12 meses até {t0:%Y-%m}. GND 4 cria ativo novo (é demanda); "
            "GND 5 só troca a titularidade de um ativo (não é demanda).", ""] + md_tabela(linhas)


def dlsp_fatores(df: pd.DataFrame, ctx: Ctx) -> list[str]:
    """Os fatores da dívida líquida (a leitura da PM) e o crédito às instituições oficiais."""
    out = pm.dlsp_fatores(df, ctx)
    it = "interna__gov_federal__creditos_inst_fin_oficiais"
    e = df[(df["item"] == it) & (df["fator"] == "estoque")].set_index("date")["value"].sort_index()
    if e.empty:
        return out
    t0 = e.index[-1]
    pib = _pib12(ctx)
    p0, p1 = em(pib, t0), em(pib, antes(t0, 12))
    v0, v1 = float(e.iloc[-1]), em(e, antes(t0, 12))
    linhas = [{"": "Créditos do Tesouro a instituições financeiras oficiais (estoque)",
               "Último (R$ bi)": fmt(v0 / _BI, 1), "Um ano antes (R$ bi)": fmt(None if v1 is None else v1 / _BI, 1),
               "Δ 12m (R$ bi)": fmt(None if v1 is None else (v0 - v1) / _BI, 1, True),
               "% do PIB": fmt(v0 / p0 * 100 if p0 else None, 2),
               "% do PIB, um ano antes": fmt(v1 / p1 * 100 if p1 and v1 is not None else None, 2)}]
    return out + ["", f"O canal parafiscal, até {t0:%Y-%m}. No estoque da dívida líquida um crédito do "
                      "governo é ATIVO e aparece negativo: mais negativo = mais crédito concedido.",
                  ""] + md_tabela(linhas)


def cds(df: pd.DataFrame, ctx: Ctx) -> list[str]:
    """A leitura padrão do CDS e os fechamentos de trimestre, que é a convenção do modelo."""
    out = bloco_generico(_CDS, df, ctx)
    s = df[df["name"] == "cds_5y_usd"].set_index("date")["value"].sort_index().dropna()
    q = s.groupby(s.index.to_period("Q")).last().iloc[-9:]
    d = s.groupby(s.index.to_period("Q")).apply(lambda x: x.index[-1]).iloc[-9:]
    linhas = [{"Trimestre": f"{per.quarter}T{per.year % 100:02d}", "Último pregão": fdata(d[per]),
               "CDS (p.b.)": fmt(q[per], 0)} for per in q.index]
    return out + ["", "Fechamento de cada trimestre (último pregão), a convenção da exógena `fiscal` "
                      "do Modelo Estrutural; o trimestre em curso aparece com o último dado.", ""] + md_tabela(linhas)


# ── F próprio das consultas ───────────────────────────────────────────────────
_FOCUS_FISCAL = ("Resultado primário", "Resultado nominal", "Dívida líquida do setor público",
                 "Dívida bruta do governo geral", "PIB Despesa de consumo da administração pública")


def focus_fiscal(df: pd.DataFrame, ctx: Ctx) -> list[str]:
    out = ["Focus, mediana por ano de referência, para cada indicador fiscal.", ""]
    for ind in _FOCUS_FISCAL:
        sub = df[df["indicador"] == ind]
        if sub.empty:
            continue
        out += [f"**{ind}**", ""] + esp.focus_anual(sub, ctx) + [""]
    return out


def focus_ipca_longo(df: pd.DataFrame, ctx: Ctx) -> list[str]:
    """A Focus do IPCA em todos os anos publicados, inclusive os distantes."""
    d0 = df["date"].max()
    datas = sorted(pd.DatetimeIndex(df["date"].unique()))
    d13 = esp._pesquisa_em(datas, d0 - pd.Timedelta(days=91))
    linhas = []
    for a in sorted(int(x) for x in df.loc[df["date"] == d0, "data_referencia"].astype(str).unique()):
        def med(d):
            r = df[(df["date"] == d) & (df["data_referencia"].astype(str) == str(a))]
            return None if d is None or r.empty else float(r["mediana"].iloc[0])
        v0, v13 = med(d0), med(d13)
        linhas.append({"Ano": a, f"Mediana ({fdata(d0)})": fmt(v0), f"13 sem. antes ({fdata(d13)})": fmt(v13),
                       "Δ 13 sem.": fmt(None if v0 is None or v13 is None else v0 - v13, 2, True)})
    return ["IPCA, % no ano. Os anos distantes são a expectativa longa: subir com notícia fiscal é "
            "sinal de dominância (mapa 2.12).", ""] + md_tabela(linhas)


def qpc_fiscal(df: pd.DataFrame, ctx: Ctx) -> list[str]:
    """A percepção da situação fiscal no Questionário Pré-Copom, nas últimas edições."""
    s = df[df["bloco"] == "situacao_fiscal"]
    if s.empty:
        return ["Sem o bloco de situação fiscal."]
    linhas = []
    for nro, g in sorted(s.groupby("nro_reuniao"), key=lambda x: x[0])[-6:][::-1]:
        f = g[g["estatistica"] == "fracao"].set_index("categoria")["valor"]
        n = g[g["estatistica"] == "n_respostas"]["valor"]
        linhas.append({"Reunião": int(nro), "Publicação": fdata(g["date"].max()),
                       "Piorou (%)": fmt(f.get("piorou", np.nan) * 100, 0),
                       "Sem mudança (%)": fmt(f.get("sem_mudancas_relevantes", np.nan) * 100, 0),
                       "Melhorou (%)": fmt(f.get("melhorou", np.nan) * 100, 0),
                       "Respostas": "—" if n.empty else int(n.iloc[0])})
    return ["Fração das respostas sobre a situação fiscal DESDE O COPOM ANTERIOR (difusão, não nível).",
            ""] + md_tabela(linhas)


_CDS = de(cambio, "cmb_risco_pais")

# ── a declaração ──────────────────────────────────────────────────────────────
TABELAS: list[Tabela] = [
    # ── i. Endógeno ──────────────────────────────────────────────────────────
    de(pm, "fisc_rtn", especial=rtn),
    de(pm, "fisc_efgg", especial=efgg),
    Tabela("fisc_investimento", dims=("corte", "item"), especial=investimento),
    de(cambio, "fisc_nfsp", series=(
        _s("resultado_primario_pct_pib_12m", "Primário, setor público consolidado, 12m (+ = superávit)", "% do PIB", "dif"),
        _s("resultado_primario_governo_federal_bc_pct_pib_12m", "Primário, governo federal e BC, 12m", "% do PIB", "dif"),
        _s("resultado_primario_estados_municipios_pct_pib_12m", "Primário, estados e municípios, 12m", "% do PIB", "dif"),
        _s("resultado_primario_empresas_estatais_pct_pib_12m", "Primário, estatais, 12m", "% do PIB", "dif"),
        _s("juros_nominais_pct_pib_12m", "Juros nominais, 12m", "% do PIB", "dif"),
        _s("resultado_nominal_pct_pib_12m", "Resultado nominal, 12m", "% do PIB", "dif"),
    )),
    de(pm, "fisc_dlsp_fatores", especial=dlsp_fatores),
    de(cambio, "fisc_divida", series=(
        _s("dbgg_pct_pib", "Dívida bruta do governo geral", "% do PIB", "dif", casas=1),
        _s("dlsp_pct_pib", "Dívida líquida do setor público", "% do PIB", "dif", casas=1),
        _s("dlsp_governo_federal_pct_pib", "DLSP, governo federal", "% do PIB", "dif", casas=1),
        _s("dlsp_banco_central_pct_pib", "DLSP, Banco Central", "% do PIB", "dif", casas=1),
        _s("dlsp_estados_municipios_pct_pib", "DLSP, estados e municípios", "% do PIB", "dif", casas=1),
        _s("dlsp_empresas_estatais_pct_pib", "DLSP, estatais", "% do PIB", "dif", casas=1),
    )),
    de(cambio, "cmb_risco_pais", especial=cds,
       nota="carga manual (export da Bloomberg), com um trecho provisório de outra fonte; "
            "confira a data do último dado no cabeçalho antes de usar."),
    # ── ii. Endógeno de atividade ────────────────────────────────────────────
    de(pm, "pm_hiato_produto"),
    so(pm, "atv_pib", ("pib_pm|Y", "consumo_adm_publica|Y", "fbcf|Y", "consumo_familias|Y")),
    de(pm, "atv_pib_taxas", series=(
        _s("pib_pm|qoq", "PIB, contra o trimestre anterior (dessaz.)", "%", "dif", casas=1),
        _s("pib_pm|yoy", "PIB, contra o mesmo trimestre do ano anterior", "%", "dif", casas=1),
        _s("pib_pm|acum_4t", "PIB, acumulado em 4 trimestres", "%", "dif", casas=1),
        _s("consumo_adm_publica|qoq", "Consumo do governo, contra o trimestre anterior", "%", "dif", casas=1),
        _s("consumo_adm_publica|yoy", "Consumo do governo, contra o mesmo trimestre", "%", "dif", casas=1),
        _s("consumo_adm_publica|acum_4t", "Consumo do governo, acumulado em 4 trimestres", "%", "dif", casas=1),
        _s("fbcf|yoy", "FBCF, contra o mesmo trimestre", "%", "dif", casas=1),
    )),
    de(pm, "atv_pib_valores_correntes"),
    de(pm, "atv_pib_mensal"),
    # ── iii. Endógeno de inflação ────────────────────────────────────────────
    de(cambio, "inflc_agregados", series=(
        _s("ipca", "IPCA", "%", "var_mensal"),
        _s("ipca_administrado", "Administrados", "%", "var_mensal"),
        _s("ipca_livres", "Livres", "%", "var_mensal"),
    )),
    # ── iv. Endógeno de política monetária ───────────────────────────────────
    de(pm, "pm_copom_reuniao"),
    so(pm, "br_interest_rate", ("POLICY|1d", "DIPRE|12M", "DIPRE|60M", "DIPRE|120M",
                                "NTNBJS|24M", "NTNBJS|60M", "NTNBJS|120M")),
    # ── v. Endógeno de câmbio ────────────────────────────────────────────────
    so(cambio, "cmb_ptax", ("ptax_venda",)),
    so(cambio, "cmb_reservas_bc", ("reserves_total_daily", "bcb_swap_cambial_position")),
    de(cambio, "cmb_fx_latam"),
    # ── vi. Endógeno de expectativas ─────────────────────────────────────────
    Tabela("expc_focus_periodo", recorte="fiscal", variante="fiscal", especial=focus_fiscal,
           filtro="indicador IN (" + ", ".join(f"%(i{k})s" for k in range(len(_FOCUS_FISCAL)))
                  + ") AND periodicidade = 'anual' AND tipo_calculo = 'geral' "
                    "AND base_calculo = 0 AND detalhe = ''",
           params={f"i{k}": ind for k, ind in enumerate(_FOCUS_FISCAL)}),
    de(cambio, "expc_focus_periodo", recorte="IPCA", especial=focus_ipca_longo),
    de(pm, "expc_qpc", especial=qpc_fiscal),
    # ── vii. Endógeno de externo ─────────────────────────────────────────────
    de(cambio, "us_interest_rate"),
    de(cambio, "cmb_equity_us"),
    de(cambio, "cmb_dollar_index_em"),
    de(cambio, "comm_brent"),
    # ── viii. TWA — crédito ──────────────────────────────────────────────────
    de(pm, "cred_credito_controle_capital"),
    de(pm, "cred_modalidade_direcionado_pj"),
    de(pm, "cred_modalidade_direcionado_pf"),
    de(pm, "cred_credito_resumo", series=(
        _s("saldo_total_total", "Saldo total", "R$ bi", "pct", escala=_BI, casas=0),
        _s("saldo_direcionado_total", "Saldo direcionado", "R$ bi", "pct", escala=_BI, casas=0),
        _s("pct_pib_direcionado_total", "Saldo direcionado", "% do PIB", "dif", casas=1),
        _s("concessao_direcionado_total", "Concessões direcionadas", "R$ bi", "fluxo", escala=_BI, casas=1),
        _s("taxa_juros_direcionado_total", "Taxa de juros, direcionado", "% a.a.", "dif"),
        _s("taxa_juros_livre_pj", "Taxa de juros, livre PJ", "% a.a.", "dif"),
    )),
]


# ── leituras combinadas ───────────────────────────────────────────────────────
def impulso(ctx: Ctx) -> list[str]:
    """O impulso fiscal em quatro medidas, lado a lado, em p.p. do PIB (+ = expansionista)."""
    linhas = []
    nfsp = ctx.serie("fisc_nfsp", "resultado_primario_pct_pib_12m")
    if not nfsp.empty:
        t0 = nfsp.index[-1]
        for lab, m in (("3 meses", 3), ("12 meses", 12)):
            ref = em(nfsp, antes(t0, m))
            linhas.append({"Medida": f"Setor público consolidado, primário 12m (NFSP), variação em {lab}",
                           "Até": f"{t0:%Y-%m}", "Último (% do PIB)": fmt(nfsp.iloc[-1]),
                           "Antes": fmt(ref),
                           "Impulso (p.p.)": fmt(None if ref is None else -(nfsp.iloc[-1] - ref), 2, True)})
    rtn = ctx.ler("fisc_rtn")
    s = rtn[rtn["name"] == "resultado_primario_governo_central"].set_index("date")["value"].sort_index()
    pib = _pib12(ctx)
    if len(s) >= 24 and not pib.empty:
        g = (s.rolling(12).sum() / pib.reindex(s.index) * 100).dropna()
        if not g.empty:
            t0 = g.index[-1]
            for lab, m in (("3 meses", 3), ("12 meses", 12)):
                ref = em(g, antes(t0, m))
                linhas.append({"Medida": f"Governo central, primário 12m (RTN), variação em {lab}",
                               "Até": f"{t0:%Y-%m}", "Último (% do PIB)": fmt(g.iloc[-1]), "Antes": fmt(ref),
                               "Impulso (p.p.)": fmt(None if ref is None else -(g.iloc[-1] - ref), 2, True)})
    ef = ctx.ler("fisc_efgg")
    w = ef.pivot_table(index="date", columns="name", values="value", aggfunc="last").sort_index()
    if {"geral_despesa_total", "geral_juros"} <= set(w.columns):
        pq = ctx.ler("atv_pib_valores_correntes")
        pq = pq[pq["name"] == "pib_pm"].set_index("date")["value"].sort_index().rolling(4).sum()
        d = ((w["geral_despesa_total"] - w["geral_juros"]).rolling(4).sum() / pq.reindex(w.index) * 100).dropna()
        if not d.empty:
            t0 = d.index[-1]
            ref = em(d, antes(t0, 12))
            linhas.append({"Medida": "Governo geral (EFGG), despesa exceto juros 4 tri, variação em 1 ano",
                           "Até": esp._periodo(t0, "trimestre"), "Último (% do PIB)": fmt(d.iloc[-1]),
                           "Antes": fmt(ref),
                           "Impulso (p.p.)": fmt(None if ref is None else d.iloc[-1] - ref, 2, True)})
    dl = ctx.ler("fisc_dlsp_fatores")
    e = dl[(dl["item"] == "interna__gov_federal__creditos_inst_fin_oficiais")
           & (dl["fator"] == "estoque")].set_index("date")["value"].sort_index()
    if not e.empty and not pib.empty:
        g = (-e / pib.reindex(e.index) * 100).dropna()
        if not g.empty:
            t0 = g.index[-1]
            ref = em(g, antes(t0, 12))
            linhas.append({"Medida": "Parafiscal: créditos do Tesouro a inst. financeiras oficiais (estoque), variação em 1 ano",
                           "Até": f"{t0:%Y-%m}", "Último (% do PIB)": fmt(g.iloc[-1]), "Antes": fmt(ref),
                           "Impulso (p.p.)": fmt(None if ref is None else g.iloc[-1] - ref, 2, True)})
    hi = ctx.ler("pm_hiato_produto")
    hi = hi[(hi["variavel"] == "central") & (hi["vintage"] == hi["vintage"].max())].sort_values("date")
    rodape = ("" if hi.empty else
              f" Hiato do BC (edição de {fdata(hi['vintage'].max())}): {fmt(hi['value'].iloc[-1])}% em "
              f"{esp._periodo(hi['date'].iloc[-1], 'trimestre')}, para ler o impulso contra o ciclo.")
    return (["### O impulso fiscal em quatro medidas", "",
             "Em p.p. do PIB, + = expansionista. Primário: impulso = −(variação do primário em % do PIB), "
             "sem correção pelo ciclo nem por receitas e despesas extraordinárias. EFGG: variação da despesa "
             "exceto juros em % do PIB (soma não consolidada das três esferas). Parafiscal: variação do "
             "crédito do Tesouro às instituições oficiais em % do PIB (sinal trocado: + = mais crédito)."
             + rodape, ""] + md_tabela(linhas))


def premio(ctx: Ctx) -> list[str]:
    """O preço do risco na convenção do modelo: o CDS no fechamento e a NTN-B de 10 anos na média
    do trimestre (a `rr_10a`), com a inflação implícita de 10 anos."""
    cds_ = ctx.serie("cmb_risco_pais", "cds_5y_usd")
    rr = ctx.serie("br_interest_rate", "NTNBJS|120M")
    di = ctx.serie("br_interest_rate", "DIPRE|120M")
    if rr.empty:
        return []
    per = rr.index.to_period("Q")
    rq = rr.groupby(per).mean().iloc[-7:]
    linhas = []
    for p_ in rq.index:
        c = cds_[cds_.index.to_period("Q") == p_]
        d_ = di[di.index.to_period("Q") == p_].mean() if not di.empty else None
        r_ = rq[p_]
        impl = None if d_ is None or pd.isna(d_) else ((1 + d_ / 100) / (1 + r_ / 100) - 1) * 100
        linhas.append({"Trimestre": f"{p_.quarter}T{p_.year % 100:02d}",
                       "NTN-B 10a, média (`rr_10a`, %)": fmt(r_),
                       "DI 10a, média (%)": fmt(d_),
                       "Inflação implícita 10a, média (%)": fmt(impl),
                       "CDS 5a, fechamento (p.b.)": fmt(None if c.empty else c.iloc[-1], 0),
                       "Pregões": int((per == p_).sum())})
    return (["### O preço do risco na convenção do modelo", "",
             "NTN-B de 10 anos na média dos pregões do trimestre (é a `rr_10a` do Modelo Estrutural) e "
             "CDS no último pregão do trimestre (a `fiscal`); o trimestre em curso vai até o último dado. "
             "Inflação implícita = (1 + DI)/(1 + NTN-B) − 1, com prêmio de risco de inflação dentro.",
             ""] + md_tabela(linhas))


COMBINADAS = [impulso, premio]
