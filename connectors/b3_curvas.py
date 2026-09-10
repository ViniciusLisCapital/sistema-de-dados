"""
Curvas de juros do arquivo de pregao da B3 (TaxaSwap.txt).

Substitui, desde 2026-09-03, a construcao de curva que vinha do Tesouro Direto
pelo projeto CentralManagement. O defeito daquela fonte era estrutural, nao um
bug: ela interpolava sobre os titulos **ofertados no Tesouro Direto** (um
subconjunto do que circula) com `scipy.interp1d(fill_value="extrapolate")`, e
sem limite de extrapolacao um vertice sem titulo que o sustente vira reta
esticada. Dois casos medidos: a NTN-B curta colapsou em 17/08/2026 quando a
2026-08-15 venceu (o pool passou a comecar em 1.448 dias corridos, e 1M-24M
viraram extrapolacao para tras, todos saindo com o mesmo 8,200), e o pre de
10a/20a foi a -30% a.a. em 14 pregoes de 2010 por uma cotacao placeholder da
fonte (Taxa Compra = 0,00) no vertice mais longo.

## A fonte

    https://www.b3.com.br/pesquisapregao/download?filelist=TS{AAMMDD}.ex_

Livre, sem autenticacao, um arquivo por pregao, funciona desde 2004. O que vem
e um zip contendo um auto-extraivel (PKSFX) que por sua vez contem o
TaxaSwap.txt, largura fixa. Por isso o zipfile e aplicado duas vezes.

A curva 076 **e** a taxa indicativa da ANBIMA (confere na 4a decimal em toda
maturidade compartilhada), o que resolve de graca o historico que a ANBIMA so
vende. Codigos usados aqui:

    PRE  -> DIPRE   DI x pre (swap DI contra prefixado; o mais liquido)
    095  -> PREJS   NTN-F / Tesouro Prefixado com Juros Semestrais
    076  -> NTNBJS  NTN-B / Tesouro IPCA+ com Juros Semestrais
    DIC  -> (nao carregado) DI x IPCA, disponivel se o breakeven precisar de
            fonte homogenea em vez de PRE contra 076

Achado que vale para qualquer conector desta fonte: **resposta nao-zip NAO e
prova de "pregao inexistente" -- e o que uma resposta throttled parece.**
Cachear isso como vazio envenenou 438 datas numa rodada de 2026-09-02 e
produziu 91,5% de cobertura falsa, com a primeira retentativa recuperando zero
porque o veneno ja estava gravado. So um zip **valido e vazio** pode contar
como ausencia -- e o que _baixar_com_retry devolve em sem_sessao.

## Ausencias legitimas

Dos 5.159 dias uteis de 2006-01-02 a 2026-09-02, 43 nao tem arquivo: sao
feriado estadual de SP (20/11, 25/01, 09/07, 24 e 31/12) -- B3 fechada,
Tesouro Direto publicando. Mais 2020-05-07, em que a B3 publicou as curvas de
DI (PRE, DIC) mas nenhuma curva de titulo (010, 076, 095).
"""

from __future__ import annotations

import io
import logging
import os
import re
import time
import zipfile
from concurrent.futures import ThreadPoolExecutor

import numpy as np
import pandas as pd
import requests

logger = logging.getLogger(__name__)

URL = "https://www.b3.com.br/pesquisapregao/download?filelist=TS{}.ex_"
_HEADERS = {"User-Agent": "Mozilla/5.0"}

# Layout do TaxaSwap.txt: 6 digitos + 5 digitos, data (8), "T1", codigo da curva
# (2-3 chars), nome, dias corridos (5), dias uteis (5), sinal, taxa (14 digitos
# com 7 decimais implicitos -- por isso a divisao por 1e7).
_LINHA = re.compile(
    r"^\d{6}\d{5}(\d{8})T1(\S{2,3})\s+(.{1,15}?)\s+(\d{5})(\d{5})([+-])(\d{14})"
)

# Codigo no TaxaSwap -> nome da curva no nosso schema.
CODIGOS = {"PRE": "DIPRE", "095": "PREJS", "076": "NTNBJS"}

# Dias corridos por mes -- 365,25/12, a mesma convencao do conector antigo,
# mantida de proposito para a serie nova ser comparavel vertice a vertice.
DIAS_POR_MES = 30.44

# Vertices por curva. O corte de cada uma foi decidido com o usuario e nao e
# arbitrario -- e onde a grade da B3 sustenta o vertice na maior parte da
# amostra. DIPRE vai a 240M porque o DI e o mais longo; PREJS para em 120M
# porque nao ha NTN-F de 20 anos; NTNBJS comeca em 3M porque a NTN-B mais curta
# raramente esta a menos de 90 dias do vencimento.
VERTICES = {
    "DIPRE": [1, 3, 6, 9, 12, 24, 60, 120, 240],
    "PREJS": [6, 9, 12, 24, 60, 120],
    "NTNBJS": [3, 6, 9, 12, 24, 60, 120, 240],
}

# Cache local do parse, um CSV por pregao. Fica fora do git (ver .gitignore):
# sao ~5.100 arquivos e o conteudo e reproduzivel a partir da fonte.
CACHE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "domain", "db", "brasil", "b3", "cache",
)


# ---------------------------------------------------------------------------
# Download e parse
# ---------------------------------------------------------------------------

def _baixar_com_retry(yymmdd: str, tentativas: int = 4) -> tuple[str | None, bool]:
    """Devolve (texto do TaxaSwap.txt, sem_sessao).

    sem_sessao=True so quando a B3 respondeu um zip VALIDO e VAZIO em pelo
    menos duas tentativas -- ai e pregao que nao existe. Qualquer outra falha
    (resposta nao-zip, timeout, excecao) devolve (None, False), que o chamador
    trata como "nao sei" e NAO cacheia. Distinguir os dois e o que impede o
    cache de envenenar; ver o docstring do modulo.
    """
    vazio_confirmado = 0
    for i in range(tentativas):
        try:
            r = requests.get(URL.format(yymmdd), headers=_HEADERS,
                             timeout=90, verify=False)
            if r.content[:2] == b"PK":
                z = zipfile.ZipFile(io.BytesIO(r.content))
                nomes = z.namelist()
                if not nomes:
                    vazio_confirmado += 1
                else:
                    z2 = zipfile.ZipFile(io.BytesIO(z.read(nomes[0])))
                    return z2.read("TaxaSwap.txt").decode("latin-1"), False
        except Exception as exc:                                   # noqa: BLE001
            logger.debug("b3_curvas %s tentativa %d: %s", yymmdd, i + 1, exc)
        time.sleep(0.6 * (i + 1))
    return None, vazio_confirmado >= 2


def parse(txt: str, codigos=tuple(CODIGOS)) -> pd.DataFrame | None:
    """Vertices das curvas pedidas: (cod, dias corridos, dias uteis, taxa)."""
    linhas = []
    for linha in txt.split("\n"):
        m = _LINHA.match(linha.rstrip("\r"))
        if m and m.group(2) in codigos:
            linhas.append((m.group(2), int(m.group(4)), int(m.group(5)),
                           (1 if m.group(6) == "+" else -1) * int(m.group(7)) / 1e7))
    if not linhas:
        return None
    return (pd.DataFrame(linhas, columns=["cod", "dc", "du", "taxa"])
              .drop_duplicates(["cod", "dc"]).sort_values(["cod", "dc"]))


def grades(data, usar_cache: bool = True) -> pd.DataFrame | None:
    """Grade crua de todas as curvas naquele pregao, do cache ou da fonte.

    Devolve None quando o pregao nao existe na B3 (feriado estadual de SP) ou
    quando o download falhou -- os dois casos se distinguem pelo cache: o
    primeiro fica gravado como CSV vazio, o segundo nao fica gravado.
    """
    yymmdd = pd.Timestamp(data).strftime("%y%m%d")
    os.makedirs(CACHE, exist_ok=True)
    caminho = os.path.join(CACHE, yymmdd + ".csv")
    if usar_cache and os.path.exists(caminho):
        D = pd.read_csv(caminho)
        return D if len(D) else None
    txt, sem_sessao = _baixar_com_retry(yymmdd)
    D = parse(txt) if txt else None
    if D is None and not sem_sessao:
        return None                       # falha de rede: nao cacheia
    (D if D is not None else pd.DataFrame(columns=["cod", "dc", "du", "taxa"])
     ).to_csv(caminho, index=False)
    return D


def baixar_muitos(datas, workers: int = 2) -> None:
    """Preenche o cache. 2 workers de proposito -- com 6 a B3 throttla, e foi
    isso que envenenou 438 datas antes do guarda de sem_sessao existir."""
    faltando = [
        d for d in datas
        if not os.path.exists(os.path.join(
            CACHE, pd.Timestamp(d).strftime("%y%m%d") + ".csv"))
    ]
    if not faltando:
        return
    logger.info("b3_curvas: baixando %d pregoes", len(faltando))
    with ThreadPoolExecutor(workers) as ex:
        list(ex.map(grades, faltando))


# ---------------------------------------------------------------------------
# Interpolacao nos vertices
# ---------------------------------------------------------------------------

def nos_vertices(D, data) -> list[tuple]:
    """Linhas (date, curve, tenor, tenor_years, value) de um pregao.

    A regra unica de qualidade: o alvo em dias corridos tem de cair DENTRO da
    grade publicada pela B3 naquele pregao. Fora dela nao sai linha -- nunca
    extrapolamos, que e exatamente o defeito que motivou a troca de fonte.
    Por isso a cobertura nao e uniforme (DIPRE@240M so desde 2014-08).
    """
    if D is None:
        return []
    out = []
    for cod, curva in CODIGOS.items():
        sub = D[D.cod == cod].sort_values("dc")
        if len(sub) < 2:
            continue
        lo, hi = sub.dc.min(), sub.dc.max()
        for meses in VERTICES[curva]:
            alvo = meses * DIAS_POR_MES
            if alvo < lo or alvo > hi:
                continue
            out.append((pd.Timestamp(data).date(), curva, str(meses) + "M",
                        round(meses / 12, 6),
                        round(float(np.interp(alvo, sub.dc, sub.taxa)), 8)))
    return out
