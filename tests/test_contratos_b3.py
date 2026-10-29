"""Testes das quatro tabelas do boletim de precos da B3 (`connectors/b3_precos.py`
+ `domain/db/brasil/b3/_contratos_b3.py`).

Duas partes:

  - sem rede nem banco: a leitura dos codigos (futuro, opcao, rolagem, casado,
    e o que fica fora -- contratos especiais e a serie de EXERCICIO com sufixo
    E, que inflaria o volume do dia de vencimento), o parse do XML (AdjstdQt nao
    pode ler AdjstdQtTax) e a regra da posicao em aberto: o boletim de D traz a
    posicao do INICIO de D, entao a do fechamento vem do pregao seguinte; feriado
    e pulado, falha de download nao.
  - contra o cache local (pula se nao houver): os precos que repetem o que outras
    tabelas ja tem TEM de bater -- a taxa de ajuste do DI1 com a grade PRE (a de
    br_di_grade), a do cupom cambial com a grade DOL do TaxaSwap, e o ajuste do
    dolar futuro com a conta de cmb_dol_futuro. Medido em 7 pregoes de 2018 a
    2026: DI e cupom exatos, dolar a R$ 0,0005 por US$ 1.000. O contrato no dia
    do proprio vencimento fica fora (taxa zero, ajuste = PTAX do dia).

    uv run --with pytest pytest tests/test_contratos_b3.py -v
"""

import os

import numpy as np
import pandas as pd
import pytest

from connectors import b3_precos
from domain.db.brasil.b3 import _contratos_b3 as nucleo


# ---------------------------------------------------------------------------
# Codigos
# ---------------------------------------------------------------------------

def test_futuro_da_o_mes_de_vencimento():
    c = b3_precos.classificar("DOLX26")
    assert c == {"ativo": "DOL", "tipo": "futuro", "vencimento": pd.Timestamp("2026-11-01")}
    assert b3_precos.classificar("DI1F27")["vencimento"] == pd.Timestamp("2027-01-01")


def test_opcao_le_tipo_e_strike_em_reais_por_mil_dolares():
    c = b3_precos.classificar("DOLZ26C005700")
    assert (c["ativo"], c["tipo"], c["opcao"], c["strike"]) == ("DOL", "opcao", "C", 5700.0)
    assert b3_precos.classificar("WDOZ26P005150")["opcao"] == "P"


def test_rolagem_e_casado():
    assert b3_precos.classificar("DR1X26F27") == {
        "ativo": "DR1", "tipo": "rolagem", "vencimento": pd.Timestamp("2026-11-01")}
    assert b3_precos.classificar("FRP0")["tipo"] == "estruturada"


@pytest.mark.parametrize("ticker", ["DOLB11", "DOLA11T", "DOLL39", "INDE11",
                                    "DOLM21C005000E", "PETR4", "ABCX26"])
def test_codigo_fora_do_padrao_e_exercicio_ficam_fora(ticker):
    assert b3_precos.classificar(ticker) is None


# ---------------------------------------------------------------------------
# XML
# ---------------------------------------------------------------------------

def _bloco(ticker, campos):
    moeda = ' Ccy="BRL"'
    corpo = "".join(f"<{k}{moeda if 'Pric' in k or 'Vol' in k else ''}>{v}</{k}>"
                    for k, v in campos.items())
    return (f"<PricRpt><TradDt><Dt>2026-10-27</Dt></TradDt><SctyId><TckrSymb>{ticker}"
            f"</TckrSymb></SctyId><FinInstrmAttrbts>{corpo}</FinInstrmAttrbts></PricRpt>")


def test_parse_separa_ajuste_de_taxa_e_zera_posicao_ausente():
    xml = (_bloco("DI1F27", {"AdjstdQtTax": "13.659", "AdjstdQtStin": "F",
                             "AdjstdQt": "97739.64", "OpnIntrst": "9374538",
                             "FinInstrmQty": "1403966"})
           + _bloco("DOLZ26C005700", {"FinInstrmQty": "240", "LastPric": "35.5"})
           + _bloco("PETR4", {"FinInstrmQty": "1"}))
    D = b3_precos.parse_xml(xml).set_index("ticker")
    assert list(D.index) == ["DI1F27", "DOLZ26C005700"]          # PETR4 nao e produto
    assert D.loc["DI1F27", "ajuste"] == 97739.64
    assert D.loc["DI1F27", "taxa_ajuste"] == 13.659
    assert D.loc["DOLZ26C005700", "oi_abertura"] == 0             # listado sem posicao
    assert pd.isna(D.loc["DOLZ26C005700", "ajuste"])


# ---------------------------------------------------------------------------
# Posicao em aberto: do pregao seguinte
# ---------------------------------------------------------------------------

def _dia(linhas):
    return pd.DataFrame([{**{c: np.nan for c in b3_precos.COLUNAS}, **l} for l in linhas])


@pytest.fixture
def boletins(monkeypatch, tmp_path):
    """Quatro dias: 26/10 e 27/10 normais, 28/10 feriado (cacheado vazio),
    29/10 normal, 30/10 sem download."""
    dias = {
        "2026-10-26": _dia([{"ticker": "DOLX26", "oi_abertura": 100, "contratos": 5},
                            {"ticker": "DOLV26", "oi_abertura": 50, "contratos": 0},
                            {"ticker": "FRCF27", "oi_abertura": 0, "contratos": 9}]),
        "2026-10-27": _dia([{"ticker": "DOLX26", "oi_abertura": 110, "contratos": 7},
                            {"ticker": "FRCF27", "oi_abertura": 0, "contratos": 3}]),
        "2026-10-29": _dia([{"ticker": "DOLX26", "oi_abertura": 130, "contratos": 1}]),
    }
    cache = {"2026-10-26", "2026-10-27", "2026-10-28", "2026-10-29"}
    monkeypatch.setattr(b3_precos, "baixar_muitos", lambda ds: None)
    monkeypatch.setattr(b3_precos, "precos",
                        lambda d: dias.get(pd.Timestamp(d).strftime("%Y-%m-%d")))
    monkeypatch.setattr(b3_precos, "caminho_cache",
                        lambda d: str(tmp_path / pd.Timestamp(d).strftime("%Y-%m-%d")))
    for c in cache:
        (tmp_path / c).write_text("")
    return nucleo.painel(list(pd.bdate_range("2026-10-26", "2026-10-30")), ("DOL", "FRC"))


def _pos(P, data, ticker):
    r = P[(P.date == pd.Timestamp(data).date()) & (P.ticker == ticker)]
    return r.posicao_aberto.iloc[0] if len(r) else "ausente"


def test_posicao_do_fechamento_e_a_abertura_do_pregao_seguinte(boletins):
    assert _pos(boletins, "2026-10-26", "DOLX26") == 110


def test_feriado_e_pulado(boletins):
    # 28/10 nao teve pregao: o fechamento de 27/10 e a abertura de 29/10
    assert _pos(boletins, "2026-10-27", "DOLX26") == 130


def test_contrato_que_sumiu_no_dia_seguinte_fecha_em_zero(boletins):
    assert _pos(boletins, "2026-10-26", "DOLV26") == 0


def test_sem_o_pregao_seguinte_a_posicao_fica_nula_e_nao_zero(boletins):
    # 30/10 sem download: nao se sabe o fechamento de 29/10
    assert pd.isna(_pos(boletins, "2026-10-29", "DOLX26"))


def test_fra_nao_carrega_posicao_propria(boletins):
    assert pd.isna(_pos(boletins, "2026-10-26", "FRCF27"))


def test_zero_que_volta_no_pregao_seguinte_vira_nulo(monkeypatch, tmp_path):
    # os casos de 10/05/2018 e 11/09/2025: o arquivo seguinte traz a abertura zerada
    # e o outro a traz de volta -- o fechamento da vespera fica desconhecido, nao zero
    dias = {
        "2026-10-26": _dia([{"ticker": "DOLX26", "oi_abertura": 100, "contratos": 1},
                            {"ticker": "DOLZ26", "oi_abertura": 80, "contratos": 1},
                            {"ticker": "DOLF27", "oi_abertura": 60, "contratos": 1}]),
        "2026-10-27": _dia([{"ticker": "DOLX26", "oi_abertura": 0, "contratos": 1},
                            {"ticker": "DOLZ26", "oi_abertura": 85, "contratos": 1},
                            {"ticker": "DOLF27", "oi_abertura": 0, "contratos": 1}]),
        "2026-10-28": _dia([{"ticker": "DOLX26", "oi_abertura": 105, "contratos": 1},
                            {"ticker": "DOLZ26", "oi_abertura": 90, "contratos": 1},
                            {"ticker": "DOLF27", "oi_abertura": 0, "contratos": 1}]),
    }
    monkeypatch.setattr(b3_precos, "baixar_muitos", lambda ds: None)
    monkeypatch.setattr(b3_precos, "precos",
                        lambda d: dias.get(pd.Timestamp(d).strftime("%Y-%m-%d")))
    monkeypatch.setattr(b3_precos, "caminho_cache",
                        lambda d: str(tmp_path / pd.Timestamp(d).strftime("%Y-%m-%d")))
    P = nucleo.painel(list(pd.bdate_range("2026-10-26", "2026-10-28")), ("DOL",))
    assert pd.isna(_pos(P, "2026-10-26", "DOLX26"))      # zerou e voltou
    assert _pos(P, "2026-10-26", "DOLZ26") == 85          # normal
    assert _pos(P, "2026-10-26", "DOLF27") == 0           # zerou e ficou: fechou de verdade
    assert _pos(P, "2026-10-27", "DOLX26") == 105         # o dia zerado le o seguinte, normal


# ---------------------------------------------------------------------------
# Contra o cache: o que repete outra tabela tem de bater
# ---------------------------------------------------------------------------

_DATAS = ["2018-01-02", "2021-06-01", "2026-10-21", "2026-10-22", "2026-10-23", "2026-10-26"]


def _disponivel():
    from connectors import b3_curvas
    return [pd.Timestamp(d) for d in _DATAS
            if os.path.exists(b3_precos.caminho_cache(d)) and os.path.exists(b3_curvas.caminho_cache(d))]


def _casar(P, grade, dias_ok):
    """(taxa do contrato, taxa do vertice da grade que vence no mesmo mes)."""
    out = []
    for _, r in P.iterrows():
        v = pd.Timestamp(r.vencimento)
        venc = [(dc, t) for dc, t in zip(grade.dc, grade.taxa)
                if (r.date + pd.Timedelta(days=int(dc))).year == v.year
                and (r.date + pd.Timedelta(days=int(dc))).month == v.month
                and (r.date + pd.Timedelta(days=int(dc))).day in dias_ok]
        if len(venc) == 1 and pd.notna(r.taxa_ajuste):
            out.append((r.taxa_ajuste, venc[0][1]))
    return out


@pytest.mark.parametrize("ativo,cod", [("DI1", "PRE"), ("DDI", "DOL")])
def test_taxa_de_ajuste_e_a_curva_que_ja_temos(ativo, cod):
    from connectors import b3_curvas
    datas = _disponivel()
    if not datas:
        pytest.skip("sem cache do boletim e do TaxaSwap")
    pares = []
    for d in datas:
        P = nucleo.painel([d], (ativo,))
        P = P[(P.tipo == "futuro") & (pd.to_datetime(P.vencimento) > d)]
        P["date"] = d
        G = b3_curvas.grades(d)
        pares += _casar(P, G[G.cod == cod], range(1, 8))
    assert len(pares) > 50
    assert max(abs(a - b) for a, b in pares) < 1e-9


def test_ajuste_do_dolar_futuro_e_a_conta_de_cmb_dol_futuro():
    from connectors import b3_curvas
    datas = _disponivel()
    if not datas:
        pytest.skip("sem cache do boletim e do TaxaSwap")
    try:
        from dotenv import load_dotenv
        load_dotenv(".env")
        from domain.db.brasil.b3.cmb_dol_futuro import _ptax
        ptax = _ptax()
    except Exception as exc:                                       # noqa: BLE001
        pytest.skip(f"MySQL indisponivel: {exc}")
    difs = []
    for d in datas:
        G = b3_curvas.grades(d)
        pre, dol = G[G.cod == "PRE"].sort_values("dc"), G[G.cod == "DOL"].sort_values("dc")
        p1 = ptax[ptax.index < d].iloc[-1]
        P = nucleo.painel([d], ("DOL",))
        P = P[(P.tipo == "futuro") & (pd.to_datetime(P.vencimento) > d)]
        for _, r in P.iterrows():
            v = pd.Timestamp(r.vencimento)
            c = dol[[(d + pd.Timedelta(days=int(x))).month == v.month
                     and (d + pd.Timedelta(days=int(x))).year == v.year
                     and (d + pd.Timedelta(days=int(x))).day <= 7 for x in dol.dc]]
            if len(c) != 1 or pd.isna(r.ajuste):
                continue
            dc, du, cs = c.dc.iloc[0], c.du.iloc[0], c.taxa.iloc[0] / 100
            di = np.interp(dc, pre.dc, pre.taxa) / 100
            difs.append(r.ajuste - 1000 * p1 * (1 + di) ** (du / 252) / (1 + cs * dc / 360))
    assert len(difs) > 20
    assert max(abs(x) for x in difs) < 0.01        # R$ por US$ 1.000; medido 0,0005
