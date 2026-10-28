"""Testes da vol implicita do dolar recuperada do premio de referencia da B3.

Tres coisas, nenhuma com rede nem banco:

  - o layout de largura fixa do Premio.txt (`b3_premio.parse`): strike x 10 e
    numero de casas decimais na ULTIMA coluna -- ler o premio sem ela erra por
    potencia de dez e a vol continua saindo um numero;
  - a conta (`cmb_vol_implicita`): numa superficie sintetica de Black com F, D e
    vol conhecidos, a paridade tem de devolver F e D e a inversao a vol;
  - a regra de prazo fixo: interpola variancia total e NAO extrapola. Um prazo
    alem do ultimo vencimento some, em vez de virar a vol do ultimo.

    uv run --with pytest pytest tests/test_vol_implicita.py -v
"""

import numpy as np
import pandas as pd
import pytest

from connectors import b3_premio
from domain.db.brasil.b3 import cmb_vol_implicita as m

DATA = pd.Timestamp("2026-10-23")


def _linha(tipo, venc, strike, premio_int, casas, merc="DOL"):
    linha = ("0" * 11 + "20261023" + f"{merc}X26  " + tipo + "E" + venc
             + f"{int(round(strike * 10)):013d}" + f"{premio_int:017d}" + str(casas))
    assert len(linha) == 68
    return linha


def test_parse_le_strike_x10_e_as_casas_da_ultima_coluna():
    txt = "\r\n".join([
        _linha("C", "20261201", 5400.0, 1234567, 3),
        _linha("V", "20261201", 5400.0, 98765, 2),
        _linha("C", "20261201", 5400.0, 1, 0, merc="IND"),      # outra mercadoria
        "cabecalho curto",
    ])
    P = b3_premio.parse(txt)
    assert len(P) == 2
    c = P[P.tipo == "C"].iloc[0]
    assert c.strike == 5400.0 and c.premio == pytest.approx(1234.567)
    assert P[P.tipo == "V"].iloc[0].premio == pytest.approx(987.65)
    assert c.vencimento == pd.Timestamp("2026-12-01")


def test_arquivo_sem_dolar_devolve_none():
    assert b3_premio.parse(_linha("C", "20261201", 5400.0, 1, 0, merc="IND")) is None


def _superficie(vols, F=5400.0, r=0.14, passo=50.0, n=12):
    """Calls e puts de Black, europeias sobre o futuro, para cada vencimento."""
    linhas = []
    for venc, s in vols.items():
        T = (pd.Timestamp(venc) - DATA).days / 365
        D = np.exp(-r * T)
        for k in F + passo * np.arange(-n, n + 1):
            for tipo, call in (("C", True), ("V", False)):
                linhas.append((tipo, pd.Timestamp(venc), k, m._black(F, k, T, D, s, call)))
    return pd.DataFrame(linhas, columns=["tipo", "vencimento", "strike", "premio"])


def test_paridade_e_inversao_devolvem_a_superficie_que_a_gerou():
    vols = {"2026-12-01": 0.20, "2027-01-04": 0.18, "2027-02-01": 0.16}
    V = m.vol_por_vencimento(_superficie(vols), DATA)
    assert len(V) == 3
    for _, v in V.iterrows():
        T = v.dias / 365
        assert v.F == pytest.approx(5400.0, rel=1e-6)
        assert v.D == pytest.approx(np.exp(-0.14 * T), rel=1e-6)
        assert v.vol == pytest.approx(vols[v.vencimento.strftime("%Y-%m-%d")], abs=1e-6)


def test_prazo_fixo_interpola_variancia_e_nao_extrapola():
    # vencimentos a 39, 73 e 101 dias: so o 1M (30d) cai antes do primeiro e o
    # 6M em diante depois do ultimo -- nenhum dos dois pode sair.
    vols = {"2026-12-01": 0.20, "2027-01-04": 0.18, "2027-02-01": 0.16}
    res = m.nos_prazos(m.vol_por_vencimento(_superficie(vols), DATA))
    assert set(res) == {"2M", "3M"}, res
    # 3M = 91 dias, entre 73 e 101: variancia total linear em dias
    w = (91 - 73) / (101 - 73)
    var = (1 - w) * 0.18 ** 2 * 73 + w * 0.16 ** 2 * 101
    assert res["3M"] == pytest.approx(100 * np.sqrt(var / 91), abs=1e-4)


def test_vol_plana_sai_plana_em_todo_prazo_coberto():
    vencs = ["2026-11-03", "2027-01-04", "2027-04-01", "2027-07-01", "2027-11-01"]
    res = m.nos_prazos(m.vol_por_vencimento(_superficie({v: 0.15 for v in vencs}), DATA))
    assert set(res) == {"1M", "2M", "3M", "6M", "9M", "1Y"}, res
    assert all(v == pytest.approx(15.0, abs=1e-4) for v in res.values()), res


def test_forward_fora_dos_strikes_nao_da_vol():
    """Sem strike dos dois lados de F a vol seria extrapolada no strike."""
    P = _superficie({"2026-12-01": 0.20}, F=5400.0, passo=50.0, n=12)
    P = P[P.strike <= 5300]
    assert m.vol_por_vencimento(P, DATA).empty
