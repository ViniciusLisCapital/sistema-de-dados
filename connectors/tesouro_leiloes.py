"""
Resultado dos leiloes de titulos da DPMFi, publicado pelo Tesouro Nacional.

## A fonte

    https://sisweb.tesouro.gov.br/apex/cosis/rleiloes/arquivos/unico/desc/historico-leiloes-{ano}.xlsx

Um xlsx por ano, 2000 em diante, sem autenticacao. E o que o dataset `ds013`
do CKAN da Tesouro Transparente aponta -- o CKAN so lista ate 2023, mas a
mesma URL serve todo ano, inclusive o corrente, que e atualizado no proprio
dia do leilao (conferido em 2026-10-27: a planilha ja trazia o leilao daquela
manha). Ha tambem um `historico-leiloes-todos.xls`, com uma aba por ano, que
nao e usado: e .xls e pediria `xlrd`, uma dependencia a mais para o mesmo dado.

A API de leiloes (`apiapexprd.tesouro.gov.br/aria/v1/api-leiloes-pub`) devolvia
404 "Azure Container App - Unavailable" no mesmo dia -- nao usada.

## O que ha e o que nao ha

Por linha: data do leilao, titulo, tipo (Venda, Compra, Troca, Extra Compra,
Extra Venda), volta (1a ou 2a), liquidacao, vencimento, quantidade OFERTADA,
taxa media e de corte, quantidade ACEITA, financeiro, e a parte vendida ao
BCB. **Nao ha a quantidade demandada** (propostas recebidas): a demanda so se
le indiretamente, pela fracao aceita da oferta e pela distancia entre corte e
media.

Duas armadilhas da planilha, as duas tratadas no script de dominio e nao aqui:
taxa vem em DECIMAL (0,1358 = 13,58% a.a.; na LFT e o agio/desagio sobre a
Selic) e vale 0 quando nada foi aceito; e 2009-05-12 tem seis linhas de NTN-B
listadas duas vezes, iguais ate a quantidade e diferentes em centavos no
financeiro.
"""

from __future__ import annotations

import io
import logging
import time

import pandas as pd
import requests

logger = logging.getLogger(__name__)

URL = ("https://sisweb.tesouro.gov.br/apex/cosis/rleiloes/arquivos/unico/desc/"
       "historico-leiloes-{ano}.xlsx")
PRIMEIRO_ANO = 2000
_HEADERS = {"User-Agent": "Mozilla/5.0"}

# Cabecalho em portugues (linha 6 da planilha, colunas B a N) -> nome curto.
# Conferido igual em todos os anos de 2000 a 2026. Se a planilha mudar, o
# casamento falha e a leitura levanta em vez de ler coluna trocada.
_COLUNAS = {
    "data do leilao": "data",
    "titulo": "titulo",
    "tipo de leilao": "tipo",
    "volta": "volta",
    "data de liquidacao": "liquidacao",
    "data de vencimento": "vencimento",
    "oferta": "oferta",
    "taxa media": "taxa_media",
    "taxa de corte": "taxa_corte",
    "venda": "aceita",
    "financeiro (r$)": "financeiro",
    "venda para bacen": "aceita_bacen",
    "financeiro para bacen (r$)": "financeiro_bacen",
}


def _normalizar(s: str) -> str:
    import unicodedata
    s = unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode()
    return " ".join(s.lower().split())


def _baixar(ano: int, tentativas: int = 3) -> bytes:
    ultimo = None
    for i in range(tentativas):
        try:
            r = requests.get(URL.format(ano=ano), headers=_HEADERS, timeout=90)
            if r.status_code == 200 and r.content[:2] == b"PK":
                return r.content
            ultimo = f"HTTP {r.status_code}, {len(r.content)} bytes"
        except requests.RequestException as exc:
            ultimo = repr(exc)
        time.sleep(2 * (i + 1))
    raise RuntimeError(f"tesouro_leiloes {ano}: {ultimo}")


def get_ano(ano: int) -> pd.DataFrame:
    """Leiloes de um ano, uma linha por (leilao, titulo, vencimento, volta).

    Colunas: as de `_COLUNAS`, cruas -- datas como Timestamp, numeros como na
    planilha (taxa em decimal, 0 quando nada foi aceito).
    """
    bruto = pd.read_excel(io.BytesIO(_baixar(ano)), header=None)
    cab = [_normalizar(v) for v in bruto.iloc[5].tolist()]
    mapa = {i: _COLUNAS[c] for i, c in enumerate(cab) if c in _COLUNAS}
    if sorted(mapa.values()) != sorted(_COLUNAS.values()):
        faltam = set(_COLUNAS.values()) - set(mapa.values())
        raise ValueError(f"tesouro_leiloes {ano}: cabecalho mudou, faltam {faltam}: {cab}")

    df = bruto.iloc[6:, list(mapa)].copy()
    df.columns = list(mapa.values())
    df["data"] = pd.to_datetime(df["data"], errors="coerce")
    df = df[df["data"].notna()].copy()     # a linha do cabecalho em ingles cai aqui
    for c in ("liquidacao", "vencimento"):
        df[c] = pd.to_datetime(df[c], errors="coerce")
    for c in ("oferta", "taxa_media", "taxa_corte", "aceita", "financeiro",
              "aceita_bacen", "financeiro_bacen"):
        df[c] = pd.to_numeric(df[c], errors="coerce")
    return df.reset_index(drop=True)


def get_anos(anos) -> pd.DataFrame:
    partes = []
    for ano in anos:
        partes.append(get_ano(ano))
        time.sleep(0.5)
    return pd.concat(partes, ignore_index=True)
