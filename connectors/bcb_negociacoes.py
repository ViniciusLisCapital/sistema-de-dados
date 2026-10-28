"""
Negociacao de titulos federais no mercado secundario (BCB/Demab, Selic).

## A fonte

    https://www4.bcb.gov.br/pom/demab/negociacoes/download/Neg{N}{AAAAMM}.ZIP

Um zip por mes com um CSV dentro, sem autenticacao, de 2003-01 ao mes
corrente (atualizado ate D-1). `N` e o universo: **T** = todas as operacoes,
**E** = so as extragrupo (entre conglomerados diferentes -- tira a operacao
entre empresas do mesmo grupo, que move titulo sem formar preco). Dicionario
oficial no portal de dados abertos do BCB, conjunto "Negociacao de Titulos
Federais no Mercado Secundario".

So operacoes DEFINITIVAS -- compromissada nao entra. Uma linha por dia e
titulo (ISIN), com numero de operacoes, quantidade, PU minimo/medio/maximo,
PU de lastro e valor par. Tres coisas do dicionario que mudam a leitura:

- **Taxa so existe para LTN e LFT** (e a extinta LFT-B). NTN-B e NTN-F vem com
  PU e sem taxa.
- **Desde 2006-10-02 os PUs nao incluem operacoes com broker** -- o numero de
  operacoes e a quantidade continuam incluindo.
- **VALOR NEGOCIADO foi descontinuado** e vem vazio; o volume financeiro e
  quantidade x PU medio.

As colunas de corretagem (NUM OPER / QUANT NEG COM CORRETAGEM) aparecem so nos
arquivos mais recentes; os antigos tem 17 colunas, os novos 19. A leitura e por
NOME de coluna, nunca por posicao.

Mes sem arquivo devolve 404 (antes de 2003, ou o mes corrente antes do 1o
pregao) e `get_mes` devolve None -- distinto de falha de rede, que levanta.
"""

from __future__ import annotations

import io
import logging
import time
import zipfile

import pandas as pd
import requests

logger = logging.getLogger(__name__)

URL = "https://www4.bcb.gov.br/pom/demab/negociacoes/download/Neg{universo}{ano_mes}.ZIP"
PRIMEIRO_MES = "2003-01"
UNIVERSOS = {"T": "todas", "E": "extragrupo"}

_COLUNAS = {
    "DATA MOV": "date",
    "SIGLA": "sigla",
    "CODIGO": "codigo",
    "CODIGO ISIN": "isin",
    "EMISSAO": "emissao",
    "VENCIMENTO": "vencimento",
    "NUM DE OPER": "num_operacoes",
    "QUANT NEGOCIADA": "quantidade",
    "VALOR NEGOCIADO": "valor_negociado",
    "PU MIN": "pu_min",
    "PU MED": "pu_med",
    "PU MAX": "pu_max",
    "PU LASTRO": "pu_lastro",
    "VALOR PAR": "valor_par",
    "TAXA MIN": "taxa_min",
    "TAXA MED": "taxa_med",
    "TAXA MAX": "taxa_max",
    "NUM OPER COM CORRETAGEM": "num_operacoes_corretagem",
    "QUANT NEG COM CORRETAGEM": "quantidade_corretagem",
}
_OBRIGATORIAS = list(_COLUNAS)[:17]


def _baixar(universo: str, ano_mes: str, tentativas: int = 4) -> bytes | None:
    url = URL.format(universo=universo, ano_mes=ano_mes)
    ultimo = None
    for i in range(tentativas):
        try:
            r = requests.get(url, timeout=90)
            if r.status_code == 404:
                return None
            if r.status_code == 200 and r.content[:2] == b"PK":
                return r.content
            ultimo = f"HTTP {r.status_code}, {len(r.content)} bytes"
        except requests.RequestException as exc:
            ultimo = repr(exc)
        time.sleep(1.5 * (i + 1))
    raise RuntimeError(f"bcb_negociacoes Neg{universo}{ano_mes}: {ultimo}")


def get_mes(ano_mes, universo: str = "T") -> pd.DataFrame | None:
    """Um mes de negociacoes. `ano_mes` em qualquer forma que o pandas leia
    como data ('2026-09', Timestamp...). None se o BCB nao tem o arquivo."""
    if universo not in UNIVERSOS:
        raise ValueError(f"universo {universo!r}: use {list(UNIVERSOS)}")
    am = pd.Timestamp(ano_mes).strftime("%Y%m")
    conteudo = _baixar(universo, am)
    if conteudo is None:
        return None
    z = zipfile.ZipFile(io.BytesIO(conteudo))
    texto = z.read(z.namelist()[0]).decode("latin-1")
    df = pd.read_csv(io.StringIO(texto), sep=";", decimal=",", dtype=str)
    df.columns = [c.strip() for c in df.columns]
    faltam = [c for c in _OBRIGATORIAS if c not in df.columns]
    if faltam:
        raise ValueError(f"Neg{universo}{am}: colunas ausentes {faltam}")
    df = df[[c for c in _COLUNAS if c in df.columns]].rename(columns=_COLUNAS)
    for c in _COLUNAS.values():
        if c not in df.columns:
            df[c] = None

    for c in ("date", "emissao", "vencimento"):
        df[c] = pd.to_datetime(df[c], format="%d/%m/%Y", errors="coerce")
    for c in ("num_operacoes", "quantidade", "valor_negociado", "pu_min", "pu_med",
              "pu_max", "pu_lastro", "valor_par", "taxa_min", "taxa_med", "taxa_max",
              "num_operacoes_corretagem", "quantidade_corretagem"):
        df[c] = pd.to_numeric(df[c].astype(str).str.replace(",", ".", regex=False)
                              .replace({"": None, "nan": None, "None": None}),
                              errors="coerce")
    for c in ("sigla", "codigo", "isin"):
        df[c] = df[c].astype(str).str.strip()
    df.insert(1, "universo", UNIVERSOS[universo])
    return df[df["date"].notna()].reset_index(drop=True)
