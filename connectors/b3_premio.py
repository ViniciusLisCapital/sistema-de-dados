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

## Opcoes de Copom (`CPM`, 2026-10-29)

O mesmo arquivo traz as opcoes digitais de Copom: uma call por vencimento (o dia
util seguinte a reuniao) e por strike, que paga 100 pontos se a variacao da meta
Selic decidida for a do strike. **O strike e 100 + variacao em p.p.**: 99,75 e o
corte de 25 p.b., 100,00 a manutencao. Conferido contra duas decisoes: na vespera
da 281a (corte de 25) a 99,75 valia 96,00 e a 100,00, 3,50; na da 280a, 95,50 e
3,25. So calls -- nao ha put no arquivo.

**O layout de verdade e strike [37:52] com 2 decimais e premio [52:67]** -- com 3
decimais de 2020-08-07 a 2023-09-08, que `parse_copom()` corrige. O
[37:50]/[50:67] do dolar so funciona porque strike de dolar nunca tem centavos e
as duas casas que ele joga no premio sao `00`; no `CPM` elas sao `75`, `50`,
`25`, e lidas daquele jeito o premio sai na casa dos 10^16. `parse_copom()` usa o
layout certo; `parse()` fica como esta para nao tocar no que ja roda.

O cache guarda as duas mercadorias de cada download (`cache_premio/` e
`cache_premio_cpm/`), para o passe da vol do dolar nao baixar o arquivo outra vez
para o Copom no mesmo dia.
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
# mercadoria -> pasta do cache. A do dolar fica onde sempre esteve.
_CACHES = {"DOL": CACHE, "CPM": CACHE + "_cpm"}


def caminho_cache(data, mercadoria: str = MERCADORIA) -> str:
    return os.path.join(_CACHES[mercadoria], pd.Timestamp(data).strftime("%y%m%d") + ".csv.gz")


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


def parse_copom(txt: str) -> pd.DataFrame | None:
    """Opcoes de Copom: (tipo, vencimento, strike, premio), strike em 100 + variacao
    da meta em p.p. Layout com o strike de 15 posicoes -- ver o docstring do modulo."""
    linhas = []
    for linha in txt.split("\n"):
        linha = linha.rstrip("\r")
        if len(linha) < 68 or linha[19:22] != "CPM":
            continue
        strike = int(linha[37:52]) / 100
        # De 2020-08-07 a 2023-09-08 a B3 grava o strike com TRES decimais (100,500 vira
        # 1005,00 lido com duas): medido no cache inteiro, todo strike dessa janela fica entre
        # 985 e 1040 e nenhum de fora passa de 103. Nenhum strike real passa de 200.
        if strike > 200:
            strike /= 10
        linhas.append((linha[27], linha[29:37], round(strike, 3),
                       int(linha[52:67]) / 10 ** int(linha[67])))
    if not linhas:
        return None
    D = pd.DataFrame(linhas, columns=_COLUNAS)
    D["vencimento"] = pd.to_datetime(D["vencimento"], format="%Y%m%d")
    return D.drop_duplicates(["tipo", "vencimento", "strike"]).sort_values(
        ["vencimento", "tipo", "strike"]).reset_index(drop=True)


_PARSERS = {"DOL": parse, "CPM": parse_copom}


def premios(data, usar_cache: bool = True, mercadoria: str = MERCADORIA) -> pd.DataFrame | None:
    """Opcoes de `mercadoria` (DOL ou CPM) daquele pregao, do cache ou da fonte. None =
    sem arquivo, sem a mercadoria no arquivo, ou falha de rede (que nao vai para o
    cache). Um download grava o cache das duas mercadorias."""
    caminho = caminho_cache(data, mercadoria)
    if usar_cache and os.path.exists(caminho):
        D = pd.read_csv(caminho, parse_dates=["vencimento"])
        return D if len(D) else None
    txt, sem_sessao = _baixar_com_retry(pd.Timestamp(data).strftime("%y%m%d"))
    if txt is None:
        if not sem_sessao or pd.Timestamp(data).normalize() >= pd.Timestamp.today().normalize():
            return None
    out = None
    for merc, fn in _PARSERS.items():
        D = fn(txt) if txt else None
        os.makedirs(_CACHES[merc], exist_ok=True)
        (D if D is not None else pd.DataFrame(columns=_COLUNAS)).to_csv(
            caminho_cache(data, merc), index=False)
        if merc == mercadoria:
            out = D
    return out


def baixar_muitos(datas, workers: int = 2, mercadoria: str = MERCADORIA) -> None:
    """Preenche o cache. 2 workers pelo mesmo motivo de b3_curvas: com mais, a
    B3 throttla."""
    faltando = [d for d in datas if not os.path.exists(caminho_cache(d, mercadoria))]
    if not faltando:
        return
    logger.info("b3_premio: baixando %d pregoes (%s)", len(faltando), mercadoria)
    with ThreadPoolExecutor(workers) as ex:
        list(ex.map(lambda d: premios(d, mercadoria=mercadoria), faltando))
