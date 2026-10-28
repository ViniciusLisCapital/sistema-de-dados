"""Testes da carga do mercado de titulos publicos (2026-10-27).

Tres pecas, cada uma com o defeito que a motivou:

  - `fisc_leiloes.transformar`: a planilha do Tesouro publica taxa em DECIMAL e 0
    quando nada foi aceito, e na LFT 0 e valor real. Errar a conversao da 1358%
    ou 0,1358% em vez de 13,58%, e tratar 0 por igual apaga 348 leiloes de LFT
    vendidos ao par.
  - `bcb_negociacoes.get_mes`: o arquivo antigo tem 17 colunas e o novo 19, e o
    ISIN vem `000000000000` no dia da 1a emissao -- foi isso que derrubou a
    primeira carga com chave duplicada.
  - `b3_curvas.parse`: o regex antigo exigia espaco depois do nome da curva, e o
    cupom limpo ("DIxXDOL Cupom l", 15 caracteres cheios) sumia sem erro.

Offline: nada aqui toca a rede nem o banco.

    uv run --with pytest pytest tests/test_mercado_titulos.py -v
"""

import io
import zipfile

import pandas as pd
import pytest

from connectors import b3_curvas, bcb_negociacoes
from domain.db.brasil.tesouro import fisc_leiloes


# ---------------------------------------------------------------------------
# fisc_leiloes
# ---------------------------------------------------------------------------

def _bruto(**kw):
    base = dict(data=pd.Timestamp("2026-10-27"), titulo="NTN-B", tipo="Extra Compra",
                volta="1.ª volta", liquidacao=pd.Timestamp("2026-10-28"),
                vencimento=pd.Timestamp("2035-05-15"), oferta=1000000,
                taxa_media=0.0765, taxa_corte=0.0765, aceita=895750,
                financeiro=3976932592.81, aceita_bacen=0, financeiro_bacen=0.0)
    base.update(kw)
    return base


def test_taxa_vira_percentual_sem_ruido_de_ponto_flutuante():
    out = fisc_leiloes.transformar(pd.DataFrame([_bruto()]))
    assert out.loc[0, "taxa_media"] == 7.65          # e nao 7.6499999999999995
    assert out.loc[0, "tipo"] == "extra_compra"
    assert out.loc[0, "volta"] == 1


def test_lft_com_taxa_zero_e_valor_real_e_fica():
    out = fisc_leiloes.transformar(pd.DataFrame([_bruto(titulo="LFT", taxa_media=0.0,
                                                        taxa_corte=0.0, tipo="Venda")]))
    assert out.loc[0, "taxa_media"] == 0.0


def test_taxa_zero_fora_da_lft_vira_nulo():
    out = fisc_leiloes.transformar(pd.DataFrame([_bruto(titulo="LTN", taxa_media=0.0,
                                                        taxa_corte=0.0, tipo="Venda")]))
    assert pd.isna(out.loc[0, "taxa_media"]) and pd.isna(out.loc[0, "taxa_corte"])


def test_segunda_volta_sem_venda_mantem_a_taxa_da_primeira():
    """E o que a fonte publica: a 2a volta e a preco da 1a, mesmo sem nada aceito."""
    out = fisc_leiloes.transformar(pd.DataFrame([_bruto(volta="2.ª volta", aceita=0,
                                                        tipo="Venda")]))
    assert out.loc[0, "volta"] == 2 and out.loc[0, "taxa_media"] == 7.65


def test_linha_repetida_na_fonte_e_descartada():
    df = pd.DataFrame([_bruto(), _bruto(financeiro=3976932592.67)])
    assert len(fisc_leiloes.transformar(df)) == 1


def test_tipo_novo_na_fonte_levanta():
    with pytest.raises(ValueError, match="tipo de leilao novo"):
        fisc_leiloes.transformar(pd.DataFrame([_bruto(tipo="Leilao Especial")]))


def test_taxa_em_unidade_errada_levanta():
    """0,0765 lido como 7,65 e multiplicado de novo daria 765% -- o guarda pega."""
    with pytest.raises(ValueError, match="fora de"):
        fisc_leiloes.transformar(pd.DataFrame([_bruto(taxa_media=7.65, taxa_corte=7.65)]))


# ---------------------------------------------------------------------------
# bcb_negociacoes
# ---------------------------------------------------------------------------

_CAB_17 = ("DATA MOV;SIGLA;CODIGO;CODIGO ISIN;EMISSAO;VENCIMENTO;NUM DE OPER;QUANT NEGOCIADA;"
           "VALOR NEGOCIADO;PU MIN;PU MED;PU MAX;PU LASTRO;VALOR PAR;TAXA MIN;TAXA MED;TAXA MAX")
_CAB_19 = _CAB_17 + ";NUM OPER COM CORRETAGEM;QUANT NEG COM CORRETAGEM"


def _zip(texto: str) -> bytes:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        z.writestr("NegT200001.CSV", texto.encode("latin-1"))
    return buf.getvalue()


def test_arquivo_antigo_de_17_colunas_le_e_completa_as_de_corretagem(monkeypatch):
    linha = ("02/01/2003;LFT;210100;BRSTNCLF17J5;15/08/2002;22/01/2003;35;4657;7024648,13;"
             "1508,37837100;1508,40633597;1508,53324600;1508,34219260;1508,39245643;-0,17;-0,02;0,02")
    monkeypatch.setattr(bcb_negociacoes, "_baixar", lambda u, am: _zip(_CAB_17 + "\n" + linha))
    df = bcb_negociacoes.get_mes("2003-01", "T")
    assert len(df) == 1 and df.loc[0, "universo"] == "todas"
    assert df.loc[0, "pu_med"] == pytest.approx(1508.40633597)
    assert df.loc[0, "taxa_med"] == pytest.approx(-0.02)
    assert pd.isna(df.loc[0, "num_operacoes_corretagem"])


def test_arquivo_novo_de_19_colunas_e_isin_zerado_preservado_no_connector(monkeypatch):
    """O connector devolve o ISIN como veio; quem o anula e o script de dominio."""
    linha = ("26/10/2026;NTN-F;950199;000000000000;09/01/2026;01/01/2037;218;1358285;;"
             "747,43107800;874,91390800;884,39597400;852,77096702;1000,00000000;;;;0;0")
    monkeypatch.setattr(bcb_negociacoes, "_baixar", lambda u, am: _zip(_CAB_19 + "\n" + linha))
    df = bcb_negociacoes.get_mes("2026-10", "E")
    assert df.loc[0, "universo"] == "extragrupo"
    assert df.loc[0, "isin"] == "000000000000"
    assert pd.isna(df.loc[0, "taxa_med"]) and pd.isna(df.loc[0, "valor_negociado"])
    assert df.loc[0, "quantidade_corretagem"] == 0


def test_mes_sem_arquivo_devolve_none(monkeypatch):
    monkeypatch.setattr(bcb_negociacoes, "_baixar", lambda u, am: None)
    assert bcb_negociacoes.get_mes("2002-12", "T") is None


def test_coluna_obrigatoria_ausente_levanta(monkeypatch):
    cab = _CAB_17.replace(";PU MED", "")
    monkeypatch.setattr(bcb_negociacoes, "_baixar", lambda u, am: _zip(cab + "\n"))
    with pytest.raises(ValueError, match="PU MED"):
        bcb_negociacoes.get_mes("2026-10", "T")


# ---------------------------------------------------------------------------
# b3_curvas.parse -- largura fixa
# ---------------------------------------------------------------------------

# Linhas reais do TaxaSwap de 2026-10-26. A do cupom limpo tem o nome com 15
# caracteres cheios, colado no prazo -- a que o regex antigo perdia.
_TAXASWAP = "\n".join([
    "0001000010120261026T1PRE  DIxPRE         0003000021+00000136170000M00030",
    "0001010010120261026T1DOC  DIxXDOL Cupom l0036000247+00000060400000M00360",
    "0001020010120261026T1DOL  DIxDOL         0036000247-00000013800000M00360",
    "0001030010120261026T1010  LTN            0007000046+00000136275000M00070",
])


def test_parse_le_o_nome_de_15_caracteres_cheios():
    D = b3_curvas.parse(_TAXASWAP)
    assert set(D.cod) == {"PRE", "DOC", "DOL", "010"}
    doc = D[D.cod == "DOC"].iloc[0]
    assert (doc.dc, doc.du, doc.taxa) == (360, 247, pytest.approx(6.04))
    assert D[D.cod == "DOL"].iloc[0].taxa == pytest.approx(-1.38)   # o sinal vem da fonte


def test_todo_codigo_carregado_tem_curva_e_vertices():
    assert set(b3_curvas.CODIGOS.values()) == set(b3_curvas.VERTICES)
