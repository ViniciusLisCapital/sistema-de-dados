"""
As tabelas do agente externo (SISTEMA_AGENTES.md V.VI) e o F de cada uma.

A lista (quais tabelas) é decidida com o usuário e vive no SISTEMA_AGENTES.md; o gerador
levanta se esta declaração divergir dela. O tratamento (quais séries, que leitura) é do
sistema (IV.iv) e se ajusta pela qualidade do report.

O agente escreve a tese sobre exógenas do Modelo Estrutural (as que a aba "Exógenas" lhe dá;
a proposta é `ffr`, `infl_us`, `dxy_em`, `sp500`, `icbr_usd`, `icbr_agr_usd`, `icbr_met_usd`),
cada uma na convenção de `modelo.CONVENCAO`. Por isso a leitura combinada principal é essa:
o valor de cada uma, trimestre a trimestre, na MESMA convenção em que o simulador a lê — a
linha "hoje" de onde o caminho parte, e o placar dos trimestres que fecharam.

Tabelas declaradas por câmbio ou PM vêm por `motor.de`/`motor.so` (mesma consulta, mesmo
arquivo de A). Nenhuma tabela daqui é de outro agente novo: o CDS e o QPC já são declarados
por câmbio e PM.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from analytics.agent_system.dados import cambio, politica_monetaria
from analytics.agent_system.dados.motor import (Ctx, Serie, Tabela, antes, de, em, fdata, fmt,
                                                md_tabela, so)

SECAO = ("## (V.VI) Agente externo", "## (V.VII)")

_TENORES = ("1M", "3M", "6M", "1Y", "2Y", "3Y", "5Y", "7Y", "10Y", "20Y", "30Y")
_ROT_TENOR = {"1M": "1 mês", "3M": "3 meses", "6M": "6 meses", "1Y": "1 ano", "2Y": "2 anos",
              "3Y": "3 anos", "5Y": "5 anos", "7Y": "7 anos", "10Y": "10 anos", "20Y": "20 anos",
              "30Y": "30 anos"}
_CPI = (("SA0", "CPI cheio"), ("SA0L1E", "Núcleo (sem alimentos e energia)"),
        ("SACL1E", "Bens sem alimentos e energia"), ("SASLE", "Serviços sem energia"),
        ("SAH1", "Habitação (shelter)"), ("SAF1", "Alimentos"), ("SA0E", "Energia"))
_PCE_CHEIO, _PCE_NUCLEO = 1, 374          # linhas da tabela 2.4.4U do BEA
_PARES = (("MX", "México"), ("CL", "Chile"), ("CO", "Colômbia"), ("PE", "Peru"))
_DIA_SEGUINTE = ("CL", "CO")              # taxa oficial de t formada em t−1 (ver risco_e_dolar)


def _s(chave, rotulo, unidade, leitura, **kw) -> Serie:
    return Serie(chave, rotulo, unidade, leitura, **kw)


TABELAS: list[Tabela] = [
    # ── i. Endógeno ──────────────────────────────────────────────────────────
    de(cambio, "us_interest_rate", variante="curva completa",
       filtro="curve IN ('POLICY', 'US_TREASURY')",
       series=(_s("POLICY|1d", "Fed Funds, meta (ponto médio)", "% a.a.", "dif"),
               *[_s(f"US_TREASURY|{t}", f"Treasury {_ROT_TENOR[t]}", "% a.a.", "dif")
                 for t in _TENORES])),
    Tabela("diferenciais_juros", recorte="EUA",
           filtro="name IN ('fed_funds', 'cpi_12m_us', 'real_us_ex_post')", series=(
        _s("fed_funds", "Fed Funds efetivo, média do mês (o `ffr` do modelo)", "% a.a.", "dif"),
        _s("cpi_12m_us", "CPI EUA 12 meses", "%", "dif"),
        _s("real_us_ex_post", "Juro real ex-post EUA (Fed Funds − CPI 12m)", "% a.a.", "dif"),
    )),
    Tabela("inflc_cpi", dims=("item_code",),
           filtro="indice = 'CPI-U' AND ajuste = 'SA' AND item_code IN "
                  "('SA0', 'SA0L1E', 'SACL1E', 'SASLE', 'SAH1', 'SAF1', 'SA0E')",
           series=tuple(_s(k, rot, "índice, com ajuste sazonal", "pct", casas=3) for k, rot in _CPI),
           nota="Outubro de 2025 não existe (o BLS não coletou durante a paralisação do governo "
                "americano); a variação de um mês que atravesse ele é calculada por G."),
    Tabela("inflc_pce", dims=("linha",),
           filtro=f"medida = 'indice' AND linha IN ({_PCE_CHEIO}, {_PCE_NUCLEO})", series=(
        _s(str(_PCE_CHEIO), "PCE cheio", "índice 2017=100", "pct", casas=3),
        _s(str(_PCE_NUCLEO), "PCE núcleo (sem alimentos e energia)", "índice 2017=100", "pct", casas=3),
    )),
    Tabela("expc_inflacao", dims=("tenor",), series=tuple(
        _s(t, f"Inflação esperada, {r}", "% a.a.", "dif")
        for t, r in (("1Y", "1 ano"), ("2Y", "2 anos"), ("5Y", "5 anos"), ("10Y", "10 anos"),
                     ("30Y", "30 anos")))),
    Tabela("mt_ces", dims=("categoria", "medida"), valor="valor",
           filtro="ajuste = 'sa' AND ((categoria = '00000000' AND medida = 'emprego') OR "
                  "(categoria = '05000000' AND medida IN ('emprego', 'ganho_hora')))", series=(
        _s("0|emprego", "Payroll, emprego total (Δ 1m = criação de vagas no mês)", "mil", "dif", casas=0),
        _s("5000000|emprego", "Payroll, emprego privado", "mil", "dif", casas=0),
        _s("5000000|ganho_hora", "Salário médio por hora, privado", "US$", "pct"),
    ), nota="O mês mais recente é preliminar e o BLS o revisa nos dois meses seguintes."),
    Tabela("mt_cps", dims=("categoria",), valor="valor",
           filtro="ajuste = 'sa' AND categoria IN "
                  "('taxa_desemprego', 'u6', 'participacao', 'razao_emprego_pop')", series=(
        _s("taxa_desemprego", "Taxa de desemprego (U-3)", "%", "dif"),
        _s("u6", "Desemprego amplo (U-6)", "%", "dif"),
        _s("participacao", "Taxa de participação", "%", "dif"),
        _s("razao_emprego_pop", "Emprego / população", "%", "dif"),
    )),
    Tabela("mt_jolts", dims=("medida", "tipo"), valor="valor",
           filtro="corte = 'industria' AND categoria = '000000' AND ajuste = 'sa' AND "
                  "((tipo = 'taxa' AND medida IN ('JO', 'HI', 'QU', 'LD')) OR medida = 'UO')",
           series=(
        _s("JO|taxa", "Vagas em aberto, taxa", "% do emprego + vagas", "dif"),
        _s("HI|taxa", "Contratações, taxa", "% do emprego", "dif"),
        _s("QU|taxa", "Pedidos de demissão, taxa", "% do emprego", "dif"),
        _s("LD|taxa", "Demissões, taxa", "% do emprego", "dif"),
        _s("UO|razao", "Desempregados por vaga", "razão", "dif"),
    )),
    de(cambio, "cmb_dollar_index"),
    de(cambio, "cmb_dollar_index_em"),
    de(cambio, "cmb_equity_us"),
    de(cambio, "comm_icbr_usd"),
    de(cambio, "comm_brent"),
    de(politica_monetaria, "inter_interest_rate"),
    de(cambio, "cmb_real_rates", series=tuple(
        _s(f"{p}|{n}", f"{p}, {rot}", u, "dif")
        for p in ("BR", "MX", "CL", "CO", "PE")
        for n, rot, u in (("policy_rate", "juro de política", "% a.a."),
                          ("cpi_yoy", "inflação 12m", "%"),
                          ("real_rate_ex_post", "juro real ex-post", "% a.a.")))),
    # ── ii. Endógeno de câmbio (consulta) ────────────────────────────────────
    de(cambio, "cmb_fx_latam"),
    so(cambio, "cmb_cot_fx", ("BRL|lev_net", "BRL|asset_mgr_net", "BRL|open_interest",
                              "MXN|lev_net", "MXN|asset_mgr_net", "MXN|open_interest")),
    de(cambio, "cmb_termos_troca"),
    so(cambio, "cmb_comex_pais", ("mundo_export", "china_export", "eua_export")),
    # ── iii. Endógeno de fiscal (consulta) ───────────────────────────────────
    de(cambio, "cmb_risco_pais"),
    # ── iv. Endógeno de expectativas (consulta) — `especial` abaixo ──────────
]


# ── o QPC: só o bloco do ambiente externo ─────────────────────────────────────
def qpc_externo(df: pd.DataFrame, ctx: Ctx) -> list[str]:
    """A avaliação do ambiente externo nos dois QPCs mais recentes, fração das respostas."""
    d = df.copy()
    for c in ("referencia", "categoria", "estatistica", "bloco"):
        d[c] = politica_monetaria._texto(d[c])
    d = d[(d["bloco"] == "ambiente_externo") & (d["estatistica"] == "fracao")]
    if d.empty:
        return ["O QPC não traz o bloco de ambiente externo no corte."]
    nros = sorted(d["nro_reuniao"].unique())[-2:]
    linhas = []
    for (ref, cat), g in d[d["nro_reuniao"].isin(nros)].groupby(["referencia", "categoria"], sort=False):
        row = {"Pergunta": ("ambiente externo " + ref).strip().replace("_", " "),
               "Resposta": cat.replace("_", " ")}
        for n in nros:
            r = g[g["nro_reuniao"] == n]
            row[f"R{int(n)} ({fdata(d.loc[d['nro_reuniao'] == n, 'date'].max())})"] = (
                "—" if r.empty else f"{float(r['valor'].iloc[0]):.0%}")
        linhas.append(row)
    return ["Fração das respostas do Questionário Pré-Copom sobre o ambiente externo; as outras "
            "perguntas do QPC são do agente de expectativas.", ""] + md_tabela(linhas)


TABELAS.append(de(politica_monetaria, "expc_qpc", especial=qpc_externo))


# ── as exógenas na convenção do modelo ────────────────────────────────────────
def _tri(d: pd.Timestamp) -> str:
    return f"{(d.month - 1) // 3 + 1}T{d.year % 100:02d}"


def _fim_tri(p: pd.Period) -> pd.Timestamp:
    return p.end_time.normalize()


def exogenas_na_convencao(ctx: Ctx) -> list[str]:
    """As sete exógenas, trimestre a trimestre, na convenção de `modelo.CONVENCAO`."""
    ffr = ctx.serie("diferenciais_juros", "fed_funds", "EUA")
    cpi = ctx.serie("inflc_cpi", "SA0")
    dem = ctx.serie("cmb_dollar_index_em", "dxy_em")
    spx = ctx.serie("cmb_equity_us", "sp500")
    ic = {k: ctx.serie("comm_icbr_usd", k) for k in
          ("icbr_usd", "icbr_agropecuaria_usd", "icbr_metal_usd")}
    atual = pd.Period(ctx.corte, freq="Q")
    linhas = []
    for k in range(6, -1, -1):
        p = atual - k
        ini, fim = p.start_time.normalize(), _fim_tri(p)
        meses = pd.date_range(ini, periods=3, freq="MS")
        ult_mes, mes_ant = meses[-1], meses[0] - pd.DateOffset(months=1)
        parcial = k == 0

        def mensal_em(s, m):
            return float(s.loc[m]) if m in s.index else None

        def fech(s):
            s2 = s.loc[ini:min(fim, ctx.corte)]
            if s2.empty:
                return "—"
            v = fmt(float(s2.iloc[-1]), 2)
            return f"{v} (até {s2.index[-1]:%d/%m})" if parcial else v

        def media3(s):
            vals = [s.loc[m] for m in meses if m in s.index]
            if not vals:
                return "—"
            v = fmt(float(np.mean(vals)), 2)
            return f"{v} ({len(vals)} de 3 meses)" if len(vals) < 3 else v

        f = mensal_em(ffr, ult_mes)
        c1, c0 = mensal_em(cpi, ult_mes), mensal_em(cpi, mes_ant)
        icu = mensal_em(ic["icbr_usd"], ult_mes)
        linhas.append({
            "Trimestre": _tri(ini) + (" (em curso)" if parcial else ""),
            "ffr": fmt(f) if f is not None else "—",
            "infl_us": fmt(100 * np.log(c1 / c0)) if c1 and c0 else "—",
            "dxy_em": fech(dem),
            "sp500": fech(spx),
            "icbr_usd": fmt(icu) if icu is not None else "—",
            "icbr_agr_usd": media3(ic["icbr_agropecuaria_usd"]),
            "icbr_met_usd": media3(ic["icbr_metal_usd"]),
        })
    return ["### As sete exógenas na convenção do modelo", "",
            "O valor de cada trimestre como o Modelo Estrutural o lê (`modelo.CONVENCAO`): é nesta "
            "convenção que o caminho é escrito e que o placar é medido. `ffr` = Fed Funds efetivo, "
            "média do último mês do trimestre; `infl_us` = 100·Δlog do CPI cheio (SA) do último mês "
            "do trimestre anterior ao último deste, em % no trimestre (sem anualizar); `dxy_em` e "
            "`sp500` = fechamento; `icbr_usd` = o índice do último mês; `icbr_agr_usd` e "
            "`icbr_met_usd` = média dos três meses. O trimestre em curso sai parcial, marcado.", ""
            ] + md_tabela(linhas)


# ── política dos EUA: a curva contra a meta, a inflação recente anualizada ────
def _anual(s: pd.Series, meses: int) -> float | None:
    """Variação dos últimos `meses` meses, anualizada, em %."""
    if s.empty:
        return None
    t0 = s.index[-1]
    ref = em(s, antes(t0, meses))
    return None if not ref else ((float(s.iloc[-1]) / ref) ** (12 / meses) - 1) * 100


def politica_eua(ctx: Ctx) -> list[str]:
    """A curva americana contra a meta do Fed, e a inflação recente anualizada."""
    meta = ctx.serie("us_interest_rate", "POLICY|1d")
    t = {k: ctx.serie("us_interest_rate", f"US_TREASURY|{k}") for k in _TENORES}
    efe = ctx.serie("diferenciais_juros", "fed_funds", "EUA")
    ex10 = ctx.serie("expc_inflacao", "10Y")
    out = ["### Política dos EUA: a curva contra a meta", ""]
    if not meta.empty and not t["2Y"].empty:
        d0 = t["2Y"].index[-1]
        m0 = em(meta, d0)
        linhas = []
        for k in ("1M", "3M", "6M", "1Y", "2Y"):
            v = em(t[k], d0)
            linhas.append({"Vértice": f"Treasury {_ROT_TENOR[k]}", "Taxa": fmt(v),
                           "Menos a meta (p.p.)": fmt(None if v is None or m0 is None else v - m0, 2, True)})
        out += [f"Em {fdata(d0)}, meta do Fed (ponto médio) {fmt(m0)}% e Fed Funds efetivo de "
                f"{fmt(float(efe.iloc[-1]) if not efe.empty else None)}% ({efe.index[-1]:%m/%Y}, média "
                "do mês). Um vértice curto abaixo da meta é corte precificado no prazo dele, "
                "somado a um prêmio; não há futuros de Fed Funds no banco.", ""] + md_tabela(linhas) + [""]
        incl = []
        for a, b in (("3M", "10Y"), ("2Y", "10Y"), ("10Y", "30Y")):
            va, vb = em(t[a], d0), em(t[b], d0)
            ha, hb = em(t[a], antes(d0, 3)), em(t[b], antes(d0, 3))
            sp = None if va is None or vb is None else vb - va
            sp3 = None if ha is None or hb is None else hb - ha
            incl.append({"Inclinação": f"{_ROT_TENOR[b]} − {_ROT_TENOR[a]}", "Hoje (p.p.)": fmt(sp, 2, True),
                         "3 meses antes (p.p.)": fmt(sp3, 2, True)})
        out += md_tabela(incl) + [""]
        v10, e10 = em(t["10Y"], d0), (float(ex10.iloc[-1]) if not ex10.empty else None)
        if v10 is not None and e10 is not None:
            out += [f"Juro real ex-ante de 10 anos aproximado: Treasury 10 anos {fmt(v10)}% menos a "
                    f"inflação esperada de 10 anos do Cleveland Fed {fmt(e10)}% ({ex10.index[-1]:%m/%Y}) "
                    f"= {fmt(v10 - e10)}%.", ""]
    infl = []
    for tab, chave, rot in (("inflc_cpi", "SA0", "CPI cheio"), ("inflc_cpi", "SA0L1E", "CPI núcleo"),
                            ("inflc_cpi", "SASLE", "CPI serviços sem energia"),
                            ("inflc_pce", str(_PCE_CHEIO), "PCE cheio"),
                            ("inflc_pce", str(_PCE_NUCLEO), "PCE núcleo")):
        s = ctx.serie(tab, chave)
        if s.empty:
            continue
        infl.append({"Medida": rot, "Mês": f"{s.index[-1]:%Y-%m}",
                     "3m anualizado": fmt(_anual(s, 3), 2), "6m anualizado": fmt(_anual(s, 6), 2),
                     "12m": fmt(_anual(s, 12), 2)})
    out += ["Inflação americana recente, % ao ano (o CPI não tem outubro de 2025; uma janela que o "
            "atravessa compara com o mês disponível anterior):", ""] + md_tabela(infl)
    return out


# ── risco e dólar: andam juntos agora? ────────────────────────────────────────
def risco_e_dolar(ctx: Ctx) -> list[str]:
    """Correlação dos retornos diários do dólar EM com o S&P e com os pares, 3 e 12 meses."""
    dem = ctx.serie("cmb_dollar_index_em", "dxy_em")
    ret = {"S&P 500": ctx.serie("cmb_equity_us", "sp500"), "DXY": ctx.serie("cmb_dollar_index", "dxy")}
    for p, rot in _PARES:
        s = ctx.serie("cmb_fx_latam", p)
        # A taxa oficial do Chile e a da Colômbia datadas em t são formadas nos negócios do dia
        # útil anterior: no mesmo dia elas não correlacionam com nada. Alinhadas um dia antes.
        ret[rot] = s.shift(-1).dropna() if p in _DIA_SEGUINTE else s
    if dem.empty:
        return []
    r0 = np.log(dem).diff()
    t0 = dem.index[-1]
    linhas = []
    for rot, s in ret.items():
        if s.empty:
            continue
        j = pd.concat([r0, np.log(s).diff()], axis=1, join="inner").dropna()
        row = {"Contra o dólar EM": rot}
        for lab, m in (("3m", 3), ("12m", 12)):
            x = j.loc[antes(t0, m):]
            row[f"Correlação {lab}"] = fmt(float(x.iloc[:, 0].corr(x.iloc[:, 1])) if len(x) > 20 else None, 2, True)
        x = j.loc[antes(t0, 120):]
        row["Correlação 10a"] = fmt(float(x.iloc[:, 0].corr(x.iloc[:, 1])) if len(x) > 20 else None, 2, True)
        linhas.append(row)
    return ["### Risco e dólar: o que anda junto agora", "",
            f"Correlação dos retornos diários (log) com o dólar contra emergentes, até {fdata(t0)}. "
            "Moedas latinas em moeda local por dólar: correlação positiva = a moeda se desvaloriza "
            "quando o dólar EM sobe. Chile e Colômbia entram com a taxa oficial do dia útil seguinte, que é a "
            "formada no dia do retorno do dólar EM. Na (F) o S&P e o dólar EM entram juntos (mapa, 2.5).", ""
            ] + md_tabela(linhas)


# ── commodities: os sub-índices mês a mês ─────────────────────────────────────
def commodities(ctx: Ctx) -> list[str]:
    """IC-Br em dólar por grupo e Brent, nos últimos seis meses publicados."""
    ic = {rot: ctx.serie("comm_icbr_usd", k) for k, rot in
          (("icbr_usd", "IC-Br"), ("icbr_agropecuaria_usd", "Agro"), ("icbr_metal_usd", "Metal"),
           ("icbr_energia_usd", "Energia"))}
    brent = ctx.serie("comm_brent", "brent_usd").resample("MS").mean()
    if ic["IC-Br"].empty:
        return []
    meses = ic["IC-Br"].index[-6:]
    linhas = []
    for m in meses:
        row = {"Mês": f"{m:%Y-%m}"}
        for rot, s in ic.items():
            v, a = em(s, m), em(s, antes(m, 1))
            row[rot] = f"{fmt(v, 1)} ({fmt(None if not a else (v / a - 1) * 100, 1, True)}%)"
        row["Brent, média do mês"] = fmt(em(brent, m), 1)
        linhas.append(row)
    b = ctx.serie("comm_brent", "brent_usd")
    return ["### Commodities: os grupos mês a mês", "",
            "IC-Br em dólar (média do mês, publicado pelo BC com cerca de um mês de defasagem) e a "
            "variação contra o mês anterior. O Brent diário vai até "
            f"{fdata(b.index[-1]) if not b.empty else '—'}, além do último IC-Br: é ele que mostra o "
            "mês ainda não publicado na energia.", ""] + md_tabela(linhas)


COMBINADAS = [exogenas_na_convencao, politica_eua, risco_e_dolar, commodities]
