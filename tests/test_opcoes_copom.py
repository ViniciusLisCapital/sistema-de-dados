"""Testes das opcoes digitais de Copom da B3, do arquivo RE ao payload da aba.

Nenhum com rede nem banco. Tres coisas, cada uma um erro que sairia numero plausivel:

  - o layout (`b3_premio.parse_copom`): o strike do CPM ocupa 15 posicoes com 2 decimais.
    Lido com o layout do dolar ([37:50] e [50:67]), as duas casas do strike (75, 50, 25)
    entram no premio e o strike perde a fracao -- 99,75 vira 9,9 e o corte de 25 colapsa
    com a manutencao. As linhas aqui sao COPIADAS do arquivo da B3 de 15/09/2026, vespera
    da 281a (corte de 25);
  - a carga (`pm_copom_opcoes.linhas_do_pregao`): variacao em p.b. e o vencimento do dia
    fica fora (no dia do vencimento a opcao ja e exercicio, nao preco);
  - o payload (`expectativas_juros.opcoes`): probabilidade = premio / soma da reuniao, e a
    Selic esperada soma o passo esperado de CADA reuniao ate a escolhida, so quando todas
    tem opcao naquele pregao.

    uv run --with pytest pytest tests/test_opcoes_copom.py -v
"""

import datetime as dt

import pandas as pd
import pytest

from connectors import b3_premio
from domain.db.brasil.b3 import pm_copom_opcoes as m

# Do RE de 15/09/2026, como a B3 publica.
_RAW = """0022230010120260915CPM3UV80CE202609170000000000099000000000000000002
0022240010120260915CPM3UV81CE202609170000000000099250000000000000002
0022250010120260915CPM3UV82CE202609170000000000099500000000000001002
0022260010120260915CPM3UV83CE202609170000000000099750000000000096002
0022270010120260915CPM3UV84CE202609170000000000100000000000000003502
0022280010120260915CPM3UV85CE202609170000000000100250000000000000002
0022440010120260915CPM3XV84CE202611050000000000100000000000000035002
0022430010120260915CPM3XV83CE202611050000000000099750000000000057002
0022420010120260915CPM3XV82CE202611050000000000099500000000000006002
0022450010120260915CPM3XV85CE202611050000000000100250000000000000032"""


def test_parse_copom_le_o_strike_de_15_posicoes():
    P = b3_premio.parse_copom(_RAW)
    assert len(P) == 10
    u = P[P.vencimento == pd.Timestamp("2026-09-17")].set_index("strike").premio
    assert u[99.75] == pytest.approx(96.0)       # o corte de 25 decidido no dia seguinte
    assert u[100.0] == pytest.approx(3.5)
    assert u[99.5] == pytest.approx(1.0)
    assert u.sum() == pytest.approx(100.5)       # ~100 x fator de desconto de 2 dias
    assert set(P.tipo) == {"C"}


def test_o_layout_do_dolar_estragaria_o_copom():
    """A razao de parse_copom existir: o parse do dolar le o mesmo texto e erra."""
    D = b3_premio.parse(_RAW, mercadoria="CPM")
    assert D.premio.max() > 1e10                  # as casas do strike entraram no premio
    assert len(D) < 10                            # e strikes vizinhos colapsaram


def test_parse_copom_ignora_o_dolar_e_devolve_none_sem_cpm():
    linha_dol = "0" * 11 + "20261023" + "DOLX26  CE20261201" + f"{54000:013d}" + f"{1234567:017d}" + "3"
    assert b3_premio.parse_copom(linha_dol) is None
    assert len(b3_premio.parse_copom(_RAW + "\n" + linha_dol)) == 10


def test_linhas_do_pregao_em_pb_e_sem_o_vencimento_do_dia():
    P = b3_premio.parse_copom(_RAW)
    L = m.linhas_do_pregao(P, "2026-09-15")
    assert sorted(L.variacao_bps.unique()) == [-100, -75, -50, -25, 0, 25]
    assert L.loc[(L.vencimento == dt.date(2026, 9, 17)) & (L.variacao_bps == -25), "premio"].item() == 96.0
    # No dia do vencimento o premio ja nao e preco.
    L17 = m.linhas_do_pregao(P, "2026-09-17")
    assert dt.date(2026, 9, 17) not in set(L17.vencimento)


# ── payload ──────────────────────────────────────────────────────────────────
def _payload(monkeypatch, linhas):
    from analytics.brasil.monetary_policy import expectativas_juros as ej
    df = pd.DataFrame(linhas, columns=["date", "vencimento", "variacao_bps", "premio"])
    monkeypatch.setattr(ej, "q", lambda db, sql: df.copy())
    reun = [{"date": dt.date(2026, 8, 5), "selic": 14.0},
            {"date": dt.date(2026, 9, 16), "selic": None},
            {"date": dt.date(2026, 11, 4), "selic": None},
            {"date": dt.date(2026, 12, 9), "selic": None}]
    return ej.opcoes(reun)


def test_payload_normaliza_pela_soma_e_soma_os_passos(monkeypatch):
    d = "2026-09-01"
    O = _payload(monkeypatch, [
        # 281a: 80% de corte de 25 sobre uma soma de 99 (desconto).
        (d, "2026-09-17", -25, 79.2), (d, "2026-09-17", 0, 19.8),
        # 282a: metade corte de 25, metade manutencao, soma 98.
        (d, "2026-11-05", -25, 49.0), (d, "2026-11-05", 0, 49.0),
    ])
    assert O["datas"] == [d] and O["vig"] == [14.0] and O["j0"] == [1]
    b1, b2 = O["por_reuniao"]["1"], O["por_reuniao"]["2"]
    assert b1["p"]["-25"] == [80.0] and b1["p"]["0"] == [20.0]
    assert b1["d"] == [-20.0] and b1["soma"] == [99.0]
    assert b1["v"] == [pytest.approx(13.80)]
    # A da 282a soma o passo esperado das DUAS: 14 - 0,20 - 0,125.
    assert b2["v"] == [pytest.approx(13.675)]


def test_sem_opcao_numa_reuniao_do_meio_nao_ha_selic_esperada(monkeypatch):
    d = "2026-09-01"
    O = _payload(monkeypatch, [
        (d, "2026-09-17", 0, 99.0),
        (d, "2026-12-10", -25, 97.0),             # a 283a, sem a 282a no meio
    ])
    assert O["por_reuniao"]["1"]["v"] == [14.0]
    assert O["por_reuniao"]["3"]["v"] == [None]
    assert O["por_reuniao"]["3"]["d"] == [-25.0]  # a variacao esperada dela existe


def test_vencimento_casa_com_a_reuniao_da_vespera(monkeypatch):
    O = _payload(monkeypatch, [("2026-09-16", "2026-09-17", -25, 99.0),
                               ("2026-09-17", "2026-11-05", 0, 99.0)])
    assert set(O["por_reuniao"]) == {"1", "2"}
    # O pregao do dia da decisao ainda cota a reuniao; o vencimento casa com ela, e nao com
    # a seguinte.
    assert O["por_reuniao"]["1"]["i0"] == 0
