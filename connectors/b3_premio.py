"""
Premio de referencia das opcoes de dolar, do arquivo de pregao da B3 (Premio.txt).

## A fonte

    https://www.b3.com.br/pesquisapregao/download?filelist=RE{AAMMDD}.ex_

Mesmo endpoint e mesmo empacotamento do TaxaSwap (`connectors/b3_curvas.py`):
zip com um auto-extraivel dentro, que contem `Premio.txt`, largura fixa, 68
caracteres. Livre, sem autenticacao, um por pregao, 2006 em diante (conferido
em 2006-03-31). Traz o premio TEORICO de toda opcao autorizada a negociar; aqui
so interessam as de dolar comercial (`DOL`), ~2.100 linhas por pregao hoje.

A B3 nao publica a volatilidade implicita num arquivo aberto -- a superficie
que ela usa para as flexiveis ("SupVol") esta descrita na pagina de arquivos e
nao esta na lista de download. Mas o premio de referencia SAI dessa superficie:
invertendo Black (opcao europeia sobre o futuro), call e put do mesmo strike
devolvem a mesma vol ate a 4a casa. E isso que `domain/db/brasil/b3/
cmb_vol_implicita.py` faz.

Layout (posicoes 0-based), inferido do arquivo e conferido contra a paridade:

    [11:19]  data do pregao        [19:22]  mercadoria (DOL)
    [19:27]  codigo da serie       [27]     C = call, V = put
    [28]     E = europeia          [29:37]  vencimento AAAAMMDD
    [37:50]  strike x 10 (R$ por US$ 1.000)
    [50:67]  premio, com [67] casas decimais

Mesmas duas regras de ausencia do TaxaSwap, pelo mesmo motivo: resposta nao-zip
e falha (nao cacheia), zip valido e vazio e pregao sem arquivo -- e para o dia
corrente nao se cacheia ausencia, porque o arquivo sai depois do fechamento. Ha
dias uteis sem arquivo (2026-07-30 voltou vazio em seis tentativas).
"""

from __future__ import annotations

import io
import logging
import os
import time
import zipfile
from concurrent.futures import ThreadPoolExecutor

import pandas as pd
import requests

logger = logging.getLogger(__name__)

URL = "https://www.b3.com.br/pesquisapregao/download?filelist=RE{}.ex_"
_HEADERS = {"User-Agent": "Mozilla/5.0"}
MERCADORIA = "DOL"

CACHE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "domain", "db", "brasil", "b3", "cache_premio",
)
_COLUNAS = ["tipo", "vencimento", "strike", "premio"]


def caminho_cache(data) -> str:
    return os.path.join(CACHE, pd.Timestamp(data).strftime("%y%m%d") + ".csv.gz")


def _baixar_com_retry(yymmdd: str, tentativas: int = 4) -> tuple[str | None, bool]:
    """(texto do Premio.txt, sem_sessao). Mesma semantica de b3_curvas."""
    vazio = 0
    for i in range(tentativas):
        try:
            r = requests.get(URL.format(yymmdd), headers=_HEADERS, timeout=90, verify=False)
            if r.content[:2] == b"PK":
                z = zipfile.ZipFile(io.BytesIO(r.content))
                nomes = z.namelist()
                if not nomes:
                    vazio += 1
                else:
                    z2 = zipfile.ZipFile(io.BytesIO(z.read(nomes[0])))
                    return z2.read(z2.namelist()[0]).decode("latin-1"), False
        except Exception as exc:                                   # noqa: BLE001
            logger.debug("b3_premio %s tentativa %d: %s", yymmdd, i + 1, exc)
        time.sleep(0.6 * (i + 1))
    return None, vazio >= 2


def parse(txt: str, mercadoria: str = MERCADORIA) -> pd.DataFrame | None:
    linhas = []
    for linha in txt.split("\n"):
        linha = linha.rstrip("\r")
        if len(linha) < 68 or linha[19:22] != mercadoria:
            continue
        linhas.append((linha[27], linha[29:37], int(linha[37:50]) / 10,
                       int(linha[50:67]) / 10 ** int(linha[67])))
    if not linhas:
        return None
    D = pd.DataFrame(linhas, columns=_COLUNAS)
    D["vencimento"] = pd.to_datetime(D["vencimento"], format="%Y%m%d")
    return D.drop_duplicates(["tipo", "vencimento", "strike"]).sort_values(
        ["vencimento", "tipo", "strike"]).reset_index(drop=True)


def premios(data, usar_cache: bool = True) -> pd.DataFrame | None:
    """Opcoes de dolar daquele pregao, do cache ou da fonte. None = sem arquivo
    (ou falha de rede, que nao vai para o cache)."""
    os.makedirs(CACHE, exist_ok=True)
    caminho = caminho_cache(data)
    if usar_cache and os.path.exists(caminho):
        D = pd.read_csv(caminho, parse_dates=["vencimento"])
        return D if len(D) else None
    txt, sem_sessao = _baixar_com_retry(pd.Timestamp(data).strftime("%y%m%d"))
    D = parse(txt) if txt else None
    if D is None and not sem_sessao:
        return None
    if D is None and pd.Timestamp(data).normalize() >= pd.Timestamp.today().normalize():
        return None
    (D if D is not None else pd.DataFrame(columns=_COLUNAS)).to_csv(caminho, index=False)
    return D


def baixar_muitos(datas, workers: int = 2) -> None:
    """Preenche o cache. 2 workers pelo mesmo motivo de b3_curvas: com mais, a
    B3 throttla."""
    faltando = [d for d in datas if not os.path.exists(caminho_cache(d))]
    if not faltando:
        return
    logger.info("b3_premio: baixando %d pregoes", len(faltando))
    with ThreadPoolExecutor(workers) as ex:
        list(ex.map(premios, faltando))
