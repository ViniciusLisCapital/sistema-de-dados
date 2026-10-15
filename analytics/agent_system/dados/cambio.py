"""
As tabelas do agente de câmbio (SISTEMA_AGENTES.md V.I) e o F de cada uma.

A lista (quais tabelas) é decidida com o usuário e vive no SISTEMA_AGENTES.md; o gerador
levanta se esta declaração divergir dela. O tratamento (quais séries, que leitura) é do
sistema (IV.iv) e se ajusta pela qualidade do report.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from analytics.agent_system.dados import especiais as esp
from analytics.agent_system.dados.motor import Ctx, Serie, Tabela, antes, em, fdata, fmt, md_tabela, pctl

SECAO = ("## (V.I) Agente de câmbio", "## (V.II)")
PIB = ("atv_pib_usd", "pib_usd")

_BI = 1000.0  # US$ milhões -> US$ bilhões


def _s(chave, rotulo, unidade, leitura, **kw) -> Serie:
    return Serie(chave, rotulo, unidade, leitura, **kw)


def _bop(chave, rotulo, pib=False):
    return _s(chave, rotulo, "US$ bi", "fluxo", escala=_BI, pib=pib)


def _comex(chaves: dict[str, str]):
    out = []
    for k, rot in chaves.items():
        out += [_s(f"{k}_export", f"{rot}, exportação", "US$ bi", "fluxo", escala=1e9),
                _s(f"{k}_import", f"{rot}, importação", "US$ bi", "fluxo", escala=1e9)]
    return tuple(out)


TABELAS: list[Tabela] = [
    # ── i. Endógeno ──────────────────────────────────────────────────────────
    Tabela("cmb_ptax", series=(
        _s("ptax_venda", "PTAX venda", "R$/US$", "pct", casas=4),
        _s("fx_interbank_vol_t1", "Volume interbancário D+1", "US$ mi/dia", "media", escala=1e6, casas=0),
        _s("fx_interbank_vol_t2", "Volume interbancário D+2", "US$ mi/dia", "media", escala=1e6, casas=0),
    )),
    Tabela("cmb_cambio_contratado", dims=("name",), series=(
        _s("cc_saldo_total", "Saldo total (comercial + financeiro)", "US$ bi", "fluxo", escala=_BI),
        _s("cc_saldo_comercial", "Comercial, saldo", "US$ bi", "fluxo", escala=_BI),
        _s("cc_export_total", "Comercial, exportação", "US$ bi", "fluxo", escala=_BI),
        _s("cc_import_total", "Comercial, importação", "US$ bi", "fluxo", escala=_BI),
        _s("cc_fin_saldo", "Financeiro, saldo", "US$ bi", "fluxo", escala=_BI),
        _s("cc_fin_compras", "Financeiro, compras", "US$ bi", "fluxo", escala=_BI),
        _s("cc_fin_vendas", "Financeiro, vendas", "US$ bi", "fluxo", escala=_BI),
        _s("cc_fin_servicos", "Financeiro: serviços (mensal)", "US$ bi", "fluxo", escala=_BI),
        _s("cc_fin_rendas", "Financeiro: rendas (mensal)", "US$ bi", "fluxo", escala=_BI),
        _s("cc_fin_cap_bras", "Financeiro: capitais brasileiros (mensal)", "US$ bi", "fluxo", escala=_BI),
        _s("cc_fin_cap_ext", "Financeiro: capitais estrangeiros (mensal)", "US$ bi", "fluxo", escala=_BI),
    )),
    Tabela("cmb_balanco_pagmt", series=(
        _bop("conta_corrente", "Transações correntes", pib=True),
        _bop("exportacao_bens", "Exportação de bens"),
        _bop("importacao_bens", "Importação de bens"),
        _bop("servicos", "Serviços, saldo"),
        _bop("renda_primaria", "Renda primária, saldo"),
        _bop("conta_financeira", "Conta financeira (concessões − captações líquidas)"),
        _bop("investimento_direto_liquido", "Investimento direto no país (passivos)", pib=True),
        _bop("portfolio_passivos", "Carteira, passivos", pib=True),
        _bop("acoes_passivos", "Carteira: ações, passivos"),
        _bop("titulos_dom", "Carteira: títulos no mercado doméstico, passivos"),
        _bop("outros_inv_passivos", "Outros investimentos, passivos"),
        _bop("ativos_reserva", "Ativos de reserva"),
        _bop("erros_omissoes", "Erros e omissões"),
    )),
    Tabela("cmb_comex_fator_agregado", series=_comex({
        "basicos": "Básicos", "semimanufaturados": "Semimanufaturados",
        "manufaturados": "Manufaturados", "demais": "Demais"})),
    Tabela("cmb_comex_pais", series=_comex({
        "mundo": "Mundo", "china": "China", "eua": "EUA", "argentina": "Argentina",
        "alemanha": "Alemanha"})),
    Tabela("cmb_comex_produto", series=_comex({
        "mundo": "Mundo", "petroleo": "Petróleo", "soja": "Soja", "minerio_ferro": "Minério de ferro",
        "carnes": "Carnes", "cafe": "Café"})),
    Tabela("cmb_reservas_bc", series=(
        _s("reserves_total_daily", "Reservas internacionais", "US$ bi", "dif", escala=_BI, casas=1),
        _s("reserves_liquidity_daily", "Reservas, conceito liquidez", "US$ bi", "dif", escala=_BI, casas=1),
        _s("bcb_swap_cambial_position", "Swap cambial do BC, posição (− = vendido)", "US$ bi", "dif", escala=_BI, casas=1),
        _s("bank_fx_spot_position", "Posição à vista dos bancos", "US$ bi", "dif", escala=_BI, casas=1),
        _s("bcb_intervention_spot", "Intervenção à vista (+ compra, − venda)", "US$ bi", "fluxo", escala=_BI, eventos=True),
        _s("bcb_intervention_repo_lines", "Leilões de linha (+ compra, − venda)", "US$ bi", "fluxo", escala=_BI, eventos=True),
    )),
    Tabela("cmb_cot_fx", dims=("currency", "name"), series=tuple(
        _s(f"{m}|{k}", f"{m}: {rot}", "contratos", "dif", casas=0)
        for m in ("BRL", "MXN")
        for k, rot in (("lev_net", "fundos alavancados, líquido"), ("asset_mgr_net", "asset managers, líquido"),
                       ("dealer_net", "dealers, líquido"), ("other_net", "outros reportáveis, líquido"),
                       ("nonrept_net", "não reportáveis, líquido"), ("open_interest", "posições em aberto"))
    )),
    Tabela("cmb_reer", dims=("country_code", "reer_type"), series=tuple(
        _s(f"{p}|{t}", f"{p}, {'real' if t.startswith('real') else 'nominal'} efetivo", "índice 2020=100", "pct")
        for p in ("BR", "MX", "CL", "CO") for t in ("real_broad", "nominal_broad")
    )),
    Tabela("cmb_termos_troca", series=(
        _s("termos_de_troca_funcex", "Termos de troca (Funcex)", "índice", "pct"),)),
    Tabela("cmb_fx_latam", dims=("country_code",), series=tuple(
        _s(p, rot, f"{u}/US$", "pct", casas=4 if p in ("MX", "PE") else 2)
        for p, rot, u in (("MX", "Peso mexicano", "MXN"), ("CL", "Peso chileno", "CLP"),
                          ("CO", "Peso colombiano", "COP"), ("PE", "Sol peruano", "PEN"))
    )),
    Tabela("diferenciais_juros", series=(
        _s("selic", "Selic", "% a.a.", "dif"),
        _s("fed_funds", "Fed Funds", "% a.a.", "dif"),
        _s("diferencial_nominal", "Diferencial nominal (Selic − Fed Funds)", "p.p.", "dif"),
        _s("ipca_12m", "IPCA 12m", "%", "dif"),
        _s("cpi_12m_us", "CPI EUA 12m", "%", "dif"),
        _s("real_br_ex_post", "Juro real ex-post Brasil", "% a.a.", "dif"),
        _s("real_us_ex_post", "Juro real ex-post EUA", "% a.a.", "dif"),
        _s("diferencial_real", "Diferencial real ex-post", "p.p.", "dif"),
    )),
    # ── ii. Endógeno de política monetária ───────────────────────────────────
    Tabela("pm_copom_calendario", corte=None, especial=esp.copom_calendario),
    Tabela("pm_copom_reuniao", especial=esp.copom_reuniao),
    Tabela("pm_copom_projecoes", corte="vintage", especial=esp.copom_projecoes),
    Tabela("br_di_grade", especial=esp.di_grade),
    Tabela("inflc_meta", especial=esp.inflc_meta),
    # ── iii. TWA — expectativas ──────────────────────────────────────────────
    *[Tabela("expc_focus_periodo", recorte=rec, especial=esp.focus_anual,
             filtro="indicador = %(ind)s AND periodicidade = 'anual' AND tipo_calculo = 'geral' "
                    "AND base_calculo = 0 AND detalhe = ''",
             params={"ind": ind})
      for rec, ind in (("câmbio", "Câmbio"), ("Selic", "Selic"), ("IPCA", "IPCA"))],
    Tabela("expc_focus_copom", filtro="tipo_calculo = 'geral' AND base_calculo = 0",
           especial=esp.focus_copom),
    # ── iv. TWA — externo ────────────────────────────────────────────────────
    Tabela("cmb_dollar_index", series=(_s("dxy", "DXY", "índice", "pct"),)),
    Tabela("cmb_dollar_index_em", series=(_s("dxy_em", "Dólar contra emergentes (FRED)", "índice", "pct"),)),
    Tabela("cmb_equity_us", series=(_s("sp500", "S&P 500", "pontos", "pct", casas=0),)),
    Tabela("us_interest_rate", dims=("curve", "tenor"),
           filtro="curve = 'POLICY' OR (curve = 'US_TREASURY' AND tenor IN ('2Y', '10Y'))", series=(
        _s("POLICY|1d", "Fed Funds, meta (ponto médio)", "% a.a.", "dif"),
        _s("US_TREASURY|2Y", "Treasury 2 anos", "% a.a.", "dif"),
        _s("US_TREASURY|10Y", "Treasury 10 anos", "% a.a.", "dif"),
    )),
    Tabela("cmb_real_rates", dims=("country_code", "name"), series=tuple(
        _s(f"{p}|real_rate_ex_post", f"{p}, juro real ex-post", "% a.a.", "dif")
        for p in ("BR", "MX", "CL", "CO", "PE")
    )),
    Tabela("comm_brent", series=(_s("brent_usd", "Brent", "US$/barril", "pct"),)),
    Tabela("comm_icbr_usd", series=(
        _s("icbr_usd", "IC-Br em dólar", "índice", "pct"),
        _s("icbr_agropecuaria_usd", "IC-Br agropecuária", "índice", "pct"),
        _s("icbr_metal_usd", "IC-Br metal", "índice", "pct"),
        _s("icbr_energia_usd", "IC-Br energia", "índice", "pct"),
    )),
    # ── v. TWA — doméstico ───────────────────────────────────────────────────
    Tabela("inflc_agregados", series=tuple(
        _s(k, rot, "%", "var_mensal") for k, rot in (
            ("ipca", "IPCA"), ("ipca_livres", "Livres"), ("ipca_administrado", "Administrados"),
            ("ipca_comercializaveis", "Comercializáveis"), ("ipca_nao_comercializaveis", "Não comercializáveis"),
            ("ipca_servicos", "Serviços"), ("ipca_industriais", "Industriais"))
    )),
    Tabela("fisc_nfsp", series=(
        _s("resultado_primario_pct_pib_12m", "Resultado primário, 12m (+ = superávit)", "% do PIB", "dif"),
        _s("resultado_nominal_pct_pib_12m", "Resultado nominal, 12m", "% do PIB", "dif"),
        _s("juros_nominais_pct_pib_12m", "Juros nominais, 12m", "% do PIB", "dif"),
    )),
    Tabela("fisc_divida", series=(
        _s("dbgg_pct_pib", "Dívida bruta do governo geral", "% do PIB", "dif", casas=1),
        _s("dlsp_pct_pib", "Dívida líquida do setor público", "% do PIB", "dif", casas=1),
    )),
    Tabela("atv_pib_usd", series=(_s("pib_usd", "PIB mensal em dólar", "US$ bi", "fluxo", escala=_BI),)),
    # ── vi. Exógeno ──────────────────────────────────────────────────────────
    Tabela("cmb_risco_pais", series=(_s("cds_5y_usd", "CDS 5 anos Brasil", "p.b.", "dif", casas=0),)),
]


# ── leituras combinadas ───────────────────────────────────────────────────────
def _vol(s: pd.Series, n: int) -> pd.Series:
    """Volatilidade realizada de n pregões, anualizada, em %."""
    return np.log(s).diff().rolling(n).std() * np.sqrt(252) * 100


def brl_e_pares(ctx: Ctx) -> list[str]:
    """O real contra os pares: variação, volatilidade realizada e carry contra o Fed."""
    moedas = [("BRL", ctx.serie("cmb_ptax", "ptax_venda"))]
    moedas += [(m, ctx.serie("cmb_fx_latam", p)) for m, p in
               (("MXN", "MX"), ("CLP", "CL"), ("COP", "CO"), ("PEN", "PE"))]
    fed = ctx.serie("us_interest_rate", "POLICY|1d")
    selic, d_selic = esp._selic_vigente(ctx, ctx.corte + pd.Timedelta(days=1))
    linhas = []
    for m, s in moedas:
        if s.empty:
            continue
        t0, v = s.index[-1], float(s.iloc[-1])
        var = {lab: em(s, antes(t0, k)) for lab, k in (("1m", 1), ("3m", 3), ("12m", 12))}
        v63 = _vol(s, 63)
        vol = float(v63.iloc[-1])
        if m == "BRL":
            juro, dj = selic, d_selic
        else:
            j = ctx.serie("cmb_real_rates", f"{m[:2]}|policy_rate")
            juro, dj = (float(j.iloc[-1]), j.index[-1]) if not j.empty else (None, None)
        f = em(fed, dj) if dj is not None else None
        carry = None if juro is None or f is None else juro - f
        row = {"Moeda": m, "Data": fdata(t0)}
        for lab, ref in var.items():
            row[f"Δ% {lab}"] = fmt(None if ref is None else (v / ref - 1) * 100, 1, True)
        if ctx.anterior is not None:
            ref = em(s, ctx.anterior)
            row["Δ% desde o ciclo ant."] = fmt(None if ref is None else (v / ref - 1) * 100, 1, True)
        row |= {"Vol. 21d": fmt(float(_vol(s, 21).iloc[-1]), 1), "Vol. 63d": fmt(vol, 1),
                "Pctl vol. 63d 10a": fmt(pctl(v63.loc[antes(t0, 120):], vol), 0),
                "Juro de política": f"{fmt(juro)} ({fdata(dj)})",
                "Carry vs Fed (p.p.)": fmt(carry, 2),
                "Carry / vol. 63d": fmt(None if carry is None or not vol else carry / vol, 2)}
        linhas.append(row)
    return (["### O real e os pares", "",
             "Moeda local por dólar: Δ% positivo = a moeda se desvalorizou. Volatilidade realizada "
             "em % ao ano. Juro de política dos pares pelo BIS (mensal, com defasagem: data ao lado); "
             "o do Brasil é a Selic vigente. Carry = juro de política menos a meta do Fed na mesma data.",
             ""] + md_tabela(linhas))


COMBINADAS = [brl_e_pares]
