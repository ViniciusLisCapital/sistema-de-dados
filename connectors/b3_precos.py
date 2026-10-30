"""
Boletim de precos da B3 (BVBG.086, "PriceReport"), do arquivo de pregao: por
contrato, negocios, contratos negociados, volume em R$ e US$, posicao em aberto,
precos do dia e o ajuste.

## A fonte

    https://www.b3.com.br/pesquisapregao/download?filelist=PR{AAMMDD}.zip

Mesmo endpoint do TaxaSwap (`b3_curvas.py`) e do premio das opcoes
(`b3_premio.py`). Livre, sem autenticacao, um por pregao, **de jan/2018 em
diante** (2017 inteiro volta vazio; conferido em 2017-07/09/10/11/12 e
2018-01-02). Zip com um zip dentro, e dentro dele **3 ou 4 XMLs**: a B3
republica o boletim inteiro na mesma noite (18:43, 19:14, 19:25, 20:38 em
27/10/2026), cada versao com o dia todo -- so a ultima vale. Hoje sao ~127 MB de
XML e ~54 mil instrumentos por versao; aqui so os de `PRODUTOS` interessam.

## A pegadinha: a posicao em aberto e a do INICIO do pregao

`OpnIntrst` no arquivo do dia D e a posicao no fechamento de D-1. Conferido em
seis contratos contra o Boletim Diario da B3 de 27/10/2026, que traz a posicao
do fim do dia e a variacao: DOLX26 1.050.672 no arquivo = 1.060.086 - 9.414;
DI1F27 9.374.538 = 9.194.163 + 180.375; idem DDIF27, WDOX26, DAPK27, WINZ26.
Este conector devolve o campo como ele e (`oi_abertura`); quem grava a posicao
do fechamento e `domain/db/brasil/b3/_contratos_b3.py`, lendo o arquivo do
pregao seguinte.

## Ausencia

Mesmas regras de `b3_curvas`/`b3_premio`: resposta nao-zip e falha (nao
cacheia); zip valido e vazio e pregao sem arquivo (feriado); para o dia corrente
nao se cacheia ausencia, porque o arquivo sai depois do fechamento.
"""

from __future__ import annotations

import io
import logging
import os
import re
import time
import zipfile
from concurrent.futures import ThreadPoolExecutor

import pandas as pd
import requests

logger = logging.getLogger(__name__)

URL = "https://www.b3.com.br/pesquisapregao/download?filelist=PR{}.zip"
_HEADERS = {"User-Agent": "Mozilla/5.0"}
INICIO = "2018-01-02"

# Mercadorias guardadas. O resto do boletim (acoes, opcoes de indice, agro...)
# fica no arquivo e nao entra no cache.
PRODUTOS = ("DOL", "WDO", "DDI", "FRC", "DR1", "FRP", "DI1", "DAP", "IND", "WIN")

CACHE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "domain", "db", "brasil", "b3", "cache_precos",
)
# As opcoes de Copom (CPM) num cache PROPRIO, e nao em PRODUTOS: os ~2.300 pregoes ja no
# cache acima foram gravados sem elas, e um dia sem CPM ali diria "nao houve negocio" quando
# a verdade e "nao foi lido". Aqui, arquivo ausente = nao lido. Todo download do boletim
# enche os dois (2026-10-30), entao o passe diario de qualquer tabela de contratos traz o CPM
# de graca; a historia anterior so com um passe proprio (ver precos_cpm()).
CACHE_CPM = CACHE + "_cpm"

# campo do cache -> tag do XML. `FinInstrmQty`, `NtlFinVol` e `IntlFinVol` sao os
# totais do dia (pregao regular + fora dele: o dolar tem negocio "nao regular").
_CAMPOS = {
    "negocios": "TradQty",
    "contratos": "FinInstrmQty",
    "vol_brl": "NtlFinVol",
    "vol_usd": "IntlFinVol",
    "oi_abertura": "OpnIntrst",
    "abertura": "FrstPric",
    "minimo": "MinPric",
    "maximo": "MaxPric",
    "medio": "TradAvrgPric",
    "ultimo": "LastPric",
    "ajuste": "AdjstdQt",
    "taxa_ajuste": "AdjstdQtTax",
}
COLUNAS = ["ticker"] + list(_CAMPOS)
# `<Tag>` ou `<Tag Ccy="BRL">` -- e nunca `<AdjstdQtTax>` quando se pede AdjstdQt.
_RE = {c: re.compile(r"<%s(?: [^>]*)?>([^<]+)</%s>" % (t, t)) for c, t in _CAMPOS.items()}

_MESES = dict(zip("FGHJKMNQUVXZ", range(1, 13)))
_RE_FUT = re.compile(r"^([A-Z0-9]{3})([FGHJKMNQUVXZ])(\d\d)$")
_RE_OPC = re.compile(r"^(DOL|WDO)([FGHJKMNQUVXZ])(\d\d)([CP])(\d{6})$")
_RE_ROL = re.compile(r"^(DR1)([FGHJKMNQUVXZ])(\d\d)[FGHJKMNQUVXZ]\d\d$")
_RE_FRP = re.compile(r"^FRP\d$")


def _mes(letra: str, aa: str) -> pd.Timestamp:
    return pd.Timestamp(2000 + int(aa), _MESES[letra], 1)


def classificar(ticker: str) -> dict | None:
    """O que e o instrumento, pelo codigo de negociacao. None = codigo que nao
    segue nenhum dos padroes, e fica fora em vez de virar um vencimento
    inventado. Dois casos conhecidos:

    - contratos especiais que nao sao vencimento mensal (DOLB11, DOLA11T,
      DOLL39, INDE11);
    - a serie de opcao com sufixo E (DOLM21C005000E) que aparece no dia do
      vencimento: e o EXERCICIO, nao negocio -- `contratos` e a quantidade
      exercida (igual a posicao da serie sem o E) e o "preco" e o strike.
      Medido em 2021-06-01: 29 series, 32.606 contratos. Contada como negocio,
      inflaria o volume de opcoes do dia de vencimento.

    `vencimento` e o MES de vencimento (dia 1): o dia exato depende da regra de
    cada contrato (1o dia util para dolar, DI e cupom; dia 15 para o DAP; a
    quarta mais proxima do dia 15 para o Ibovespa).
    """
    m = _RE_OPC.match(ticker)
    if m:
        return {"ativo": m[1], "tipo": "opcao", "vencimento": _mes(m[2], m[3]),
                "opcao": m[4], "strike": float(int(m[5]))}
    m = _RE_FUT.match(ticker)
    if m and m[1] in PRODUTOS:
        return {"ativo": m[1], "tipo": "futuro", "vencimento": _mes(m[2], m[3])}
    m = _RE_ROL.match(ticker)
    if m:
        # rolagem: a perna curta da o vencimento; o codigo guarda as duas
        return {"ativo": "DR1", "tipo": "rolagem", "vencimento": _mes(m[2], m[3])}
    if _RE_FRP.match(ticker):
        return {"ativo": "FRP", "tipo": "estruturada", "vencimento": None}
    return None


def parse_xml(xml: str, produtos: tuple = PRODUTOS) -> pd.DataFrame:
    """Os instrumentos de `produtos` (default PRODUTOS) de UMA versao do boletim, campos crus."""
    linhas = []
    for bloco in xml.split("</PricRpt>"):
        i = bloco.find("<TckrSymb>")
        if i < 0:
            continue
        ticker = bloco[i + 10:bloco.find("<", i + 10)]
        if ticker[:3] not in produtos:
            continue
        linha = [ticker]
        for c, rx in _RE.items():
            m = rx.search(bloco)
            linha.append(float(m.group(1)) if m else None)
        linhas.append(linha)
    D = pd.DataFrame(linhas, columns=COLUNAS)
    # instrumento listado sem o campo de posicao tem posicao zero
    D["oi_abertura"] = D["oi_abertura"].fillna(0)
    return D.drop_duplicates("ticker", keep="last").reset_index(drop=True)


def _ultima_versao(conteudo: bytes) -> tuple[str | None, int]:
    """(XML da ultima versao do dia, quantos XMLs o zip trazia). Desce em zips
    aninhados. A versao e ordenada pelo nome, que carrega o identificador da
    mensagem, crescente no tempo."""
    xmls = {}

    def _abrir(b: bytes) -> None:
        z = zipfile.ZipFile(io.BytesIO(b))
        for nome in z.namelist():
            dado = z.read(nome)
            if dado[:2] == b"PK":
                _abrir(dado)
            elif nome.lower().endswith(".xml"):
                xmls[nome] = dado

    _abrir(conteudo)
    if not xmls:
        return None, 0
    return xmls[max(xmls)].decode("utf-8"), len(xmls)


def _baixar_com_retry(yymmdd: str, tentativas: int = 4) -> tuple[str | None, bool]:
    """(XML da ultima versao, sem_sessao). Mesma semantica de b3_curvas."""
    vazio = 0
    for i in range(tentativas):
        try:
            r = requests.get(URL.format(yymmdd), headers=_HEADERS, timeout=180, verify=False)
            if r.content[:2] == b"PK":
                xml, n = _ultima_versao(r.content)
                if xml is None:
                    vazio += 1
                else:
                    return xml, False
        except Exception as exc:                                   # noqa: BLE001
            logger.debug("b3_precos %s tentativa %d: %s", yymmdd, i + 1, exc)
        time.sleep(0.6 * (i + 1))
    return None, vazio >= 2


def caminho_cache(data) -> str:
    return os.path.join(CACHE, pd.Timestamp(data).strftime("%y%m%d") + ".csv.gz")


def precos(data, usar_cache: bool = True) -> pd.DataFrame | None:
    """Instrumentos de PRODUTOS naquele pregao, do cache ou da fonte. None = sem
    arquivo (ou falha de rede, que nao vai para o cache)."""
    os.makedirs(CACHE, exist_ok=True)
    caminho = caminho_cache(data)
    if usar_cache and os.path.exists(caminho):
        D = pd.read_csv(caminho)
        return D if len(D) else None
    return _baixar_e_gravar(data)[0]


def _baixar_e_gravar(data) -> tuple[pd.DataFrame | None, pd.DataFrame | None]:
    """Baixa o boletim do pregao e grava os DOIS caches (PRODUTOS e CPM). Devolve
    (PRODUTOS, CPM). Ausencia so e gravada quando a B3 diz que nao houve sessao, e nunca
    para o dia corrente -- as regras do modulo, iguais para os dois."""
    os.makedirs(CACHE, exist_ok=True)
    os.makedirs(CACHE_CPM, exist_ok=True)
    xml, sem_sessao = _baixar_com_retry(pd.Timestamp(data).strftime("%y%m%d"))
    D = C = None
    if xml:
        dt = re.search(r"<TradDt>\s*<Dt>([^<]+)</Dt>", xml)
        if dt and pd.Timestamp(dt.group(1)) != pd.Timestamp(data).normalize():
            raise ValueError(f"b3_precos: arquivo de {data:%Y-%m-%d} traz o pregao {dt.group(1)}")
        D = parse_xml(xml)
        D = D if len(D) else None
        C = parse_xml(xml, ("CPM",))
        C = C if len(C) else None
    if not xml and not sem_sessao:
        return None, None
    if not xml and pd.Timestamp(data).normalize() >= pd.Timestamp.today().normalize():
        return None, None
    (D if D is not None else pd.DataFrame(columns=COLUNAS)).to_csv(caminho_cache(data), index=False)
    (C if C is not None else pd.DataFrame(columns=COLUNAS)).to_csv(caminho_cache_cpm(data), index=False)
    return D, C


def caminho_cache_cpm(data) -> str:
    return os.path.join(CACHE_CPM, pd.Timestamp(data).strftime("%y%m%d") + ".csv.gz")


def precos_cpm(data, usar_cache: bool = True) -> pd.DataFrame | None:
    """As opcoes de Copom (CPM) naquele pregao, do cache proprio ou da fonte. None = sem
    arquivo, ou pregao sem CPM listado.

    Codigo `CPM` + letra do MES do vencimento + ano + `C` + strike em seis digitos com tres
    decimais: CPMX26C099750 e a call de novembro/2026 no strike 99,750 (corte de 25 p.b.).
    Contratos em pontos de R$ 1 (volume = contratos x preco medio, conferido em 29/10/2026).
    Um pregao fora do cache CPM baixa o boletim inteiro (~11 MB, ~130 MB de XML)."""
    caminho = caminho_cache_cpm(data)
    if usar_cache and os.path.exists(caminho):
        C = pd.read_csv(caminho)
        return C if len(C) else None
    return _baixar_e_gravar(data)[1]


def baixar_muitos(datas, workers: int = 2, cpm: bool = False) -> None:
    """Preenche o cache (o do CPM com `cpm=True`). 2 workers pelo mesmo motivo de
    b3_curvas: com mais, a B3 throttla."""
    caminho, fn = (caminho_cache_cpm, precos_cpm) if cpm else (caminho_cache, precos)
    faltando = [d for d in datas if not os.path.exists(caminho(d))]
    if not faltando:
        return
    logger.info("b3_precos: baixando %d pregoes%s", len(faltando), " (CPM)" if cpm else "")
    with ThreadPoolExecutor(workers) as ex:
        list(ex.map(fn, faltando))
