"""
Download em massa do Comex Stat (MDIC) — dados historicos por NCM.

Fonte: balanca.economia.gov.br — arquivos anuais estaticos, SEM rate limit
(diferente de connectors/comexstat.py, que usa a API ao vivo e tem throttle
agressivo — confirmado empiricamente que um backfill de ~300 chamadas
esgota uma cota que leva minutos para se recuperar). Recomendado pela
propria documentacao da API para consultas grandes/historicas. Uso deste
connector: SOMENTE o backfill historico completo (uma vez); updates
rotineiros/marginais devem usar connectors/comexstat.py (API ao vivo, janela
curta — poucas dezenas de chamadas, nao centenas).

Arquivos anuais NCM-level (`;` separado, aspas duplas em campos texto):
  https://balanca.economia.gov.br/balanca/bd/comexstat-bd/ncm/EXP_{ano}.csv
  https://balanca.economia.gov.br/balanca/bd/comexstat-bd/ncm/IMP_{ano}.csv

Colunas export: CO_ANO;CO_MES;CO_NCM;CO_UNID;CO_PAIS;SG_UF_NCM;CO_VIA;CO_URF;QT_ESTAT;KG_LIQUIDO;VL_FOB
Colunas import: idem + VL_FRETE;VL_SEGURO

Codigos de CO_PAIS confirmados IDENTICOS aos usados pela API ao vivo
(connectors/comexstat.py) — China=160, Estados Unidos=249, Argentina=063,
Alemanha=023 — conferido diretamente contra
balanca.economia.gov.br/balanca/bd/tabelas/PAIS.csv.

Quebra por "Fator Agregado" (Basicos/Semimanufaturados/Manufaturados) — a
classica classificacao brasileira de comercio exterior, NAO disponivel na
API ao vivo (confirmado checando /general/filters) — so existe via join
contra a tabela de correlacao NCM.csv (coluna CO_FAT_AGREG), que mapeia cada
codigo NCM de 8 digitos a 1 dos 6 codigos de
balanca.economia.gov.br/balanca/bd/tabelas/NCM_FAT_AGREG.csv:
  01 Produtos Basicos, 02 Semimanufaturados, 03 Manufaturados,
  04 Transacoes Especiais, 05 Consumo de Bordo, 06 Reexportacao.
Os 3 ultimos + os poucos NCM sem correspondencia na tabela (residual
pequeno, <0.05% do total em 2025) sao agrupados como "demais" pelo caller —
ver domain/db/brasil/mdic/cmb_comex_fator_agregado.py.

Nota tecnica — encoding: NCM.csv tem caracteres acentuados (nomes de
produtos em NO_NCM_POR/ESP/ING) e precisa de `encoding="latin1"` — mesmo
padrao de PAIS.csv. As colunas usadas aqui (CO_NCM, CO_FAT_AGREG) sao
puramente numericas, mas o parser C do pandas decodifica a linha inteira
antes de aplicar `usecols`, entao o encoding errado (utf-8 default) ainda
quebra com UnicodeDecodeError mesmo sem ler as colunas de texto.

Quebra por produto especifico (soja, petroleo, minerio de ferro, cafe) —
usa o codigo SH6 (Sistema Harmonizado, 6 digitos, coluna CO_SH6 de NCM.csv)
truncado no nivel de precisao que melhor identifica cada produto: SH4 (4
digitos, "posicao") para produtos onde 1 posicao domina o capitulo
(soja=1201 ~=97% do capitulo 12; minerio de ferro=2601 ~=83% do capitulo 26,
que tambem inclui minerio de cobre etc; cafe=0901 ~=95% do capitulo 09;
petroleo bruto=2709, distinto de combustiveis refinados=2710); SH2 (2
digitos, "capitulo") para "carnes" (capitulo 02), que genuinamente abrange
varios tipos de carne (bovina, suina, de aves) sem uma posicao dominante —
ver domain/db/brasil/mdic/cmb_comex_produto.py para os codigos exatos e a
validacao numerica.

Nota tecnica — downloads interrompidos: arquivos anuais tem ~50-100MB, e
`ChunkedEncodingError`/`IncompleteRead` (conexao cai no meio da transferencia
do corpo, depois dos headers ja terem sido recebidos com 200 OK) acontecem
ocasionalmente e NAO sao cobertos pelo `Retry` do urllib3 montado no
adapter — esse retry cobre falhas de conexao/status HTTP, nao uma leitura de
corpo que comeca e e' interrompida no meio. `_get_csv_bytes()` adiciona um
retry manual em cima disso (3 tentativas, backoff simples).

Nota tecnica — TLS: o servidor balanca.economia.gov.br envia apenas o
certificado folha, sem a cadeia intermediaria (confirmado via
`openssl s_client -showcerts`: 1 certificado, contra 3 em
api-comexstat.mdic.gov.br) — `requests`/certifi rejeita com
CERTIFICATE_VERIFY_FAILED ("unable to get local issuer certificate") porque
nao faz AIA fetching. `curl`/Windows Schannel completam a cadeia
automaticamente via AIA, por isso funcionavam nos testes manuais. Corrigido
usando `truststore` (verificacao nativa do SO, mesmo comportamento do
Schannel) em vez do bundle padrao do certifi.
"""

from __future__ import annotations

import io
import ssl
import time

import pandas as pd
import requests
import truststore
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

_BASE = "https://balanca.economia.gov.br/balanca/bd/comexstat-bd/ncm"
_TABELAS_BASE = "https://balanca.economia.gov.br/balanca/bd/tabelas"

_FAT_AGREG_LABELS = {
    "01": "basicos",
    "02": "semimanufaturados",
    "03": "manufaturados",
    "04": "transacoes_especiais",
    "05": "consumo_bordo",
    "06": "reexportacao",
}


class _TruststoreAdapter(HTTPAdapter):
    """HTTPAdapter que verifica certificados via o SO (truststore) em vez do certifi."""

    def init_poolmanager(self, *args, **kwargs):
        kwargs["ssl_context"] = truststore.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        return super().init_poolmanager(*args, **kwargs)


def _build_session() -> requests.Session:
    s = requests.Session()
    s.headers["User-Agent"] = "lis-capital-comexstat-bulk-connector/1.0"
    retry = Retry(
        total=4,
        backoff_factor=2.0,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=frozenset(["GET"]),
    )
    s.mount("https://", _TruststoreAdapter(max_retries=retry))
    return s


_session = _build_session()


def _get_csv_bytes(url: str, timeout: float, max_retries: int = 3) -> bytes:
    """GET com retry manual para downloads interrompidos no meio do corpo
    (ChunkedEncodingError/IncompleteRead — ver nota tecnica no docstring do
    modulo). O `Retry` do urllib3 no adapter nao cobre esse caso.
    """
    last_exc: Exception | None = None
    for attempt in range(max_retries):
        try:
            resp = _session.get(url, timeout=timeout)
            resp.raise_for_status()
            return resp.content
        except (requests.exceptions.ChunkedEncodingError, requests.exceptions.ConnectionError) as exc:
            last_exc = exc
            time.sleep(3.0 * (attempt + 1))
    raise RuntimeError(f"Download falhou apos {max_retries} tentativas: {url}") from last_exc


def get_year(flow: str, year: int) -> pd.DataFrame:
    """Baixa o CSV anual (bulk) e agrega VL_FOB por (mes, pais).

    Args:
        flow: "export" ou "import".
        year: ano civil.

    Returns:
        DataFrame com colunas: month ("01".."12", str), co_pais (str,
        codigo Comex Stat), value_usd (float, VL_FOB somado). Uma linha por
        (mes, pais) presente no ano — inclui TODOS os paises; o caller
        filtra/agrupa para "mundo" (soma de tudo) e para parceiros
        especificos.
    """
    prefix = "EXP" if flow == "export" else "IMP"
    url = f"{_BASE}/{prefix}_{year}.csv"
    content = _get_csv_bytes(url, timeout=180.0)

    df = pd.read_csv(
        io.BytesIO(content),
        sep=";",
        usecols=["CO_MES", "CO_PAIS", "VL_FOB"],
        dtype={"CO_MES": str, "CO_PAIS": str},
    )
    agg = df.groupby(["CO_MES", "CO_PAIS"], as_index=False)["VL_FOB"].sum()
    return agg.rename(columns={"CO_MES": "month", "CO_PAIS": "co_pais", "VL_FOB": "value_usd"})


_ncm_fat_agreg_cache: pd.DataFrame | None = None


def get_ncm_fator_agregado() -> pd.DataFrame:
    """Tabela de correlacao NCM (8 digitos) -> codigo de Fator Agregado.

    Cacheada em memoria apos o primeiro fetch (arquivo de referencia,
    nao muda dentro de uma execucao/processo).

    Returns:
        DataFrame com colunas: co_ncm (str), co_fat_agreg (str, "01".."06").
    """
    global _ncm_fat_agreg_cache
    if _ncm_fat_agreg_cache is None:
        url = f"{_TABELAS_BASE}/NCM.csv"
        content = _get_csv_bytes(url, timeout=120.0)
        df = pd.read_csv(
            io.BytesIO(content),
            sep=";",
            usecols=["CO_NCM", "CO_FAT_AGREG"],
            dtype={"CO_NCM": str, "CO_FAT_AGREG": str},
            encoding="latin1",
        )
        _ncm_fat_agreg_cache = df.rename(columns={"CO_NCM": "co_ncm", "CO_FAT_AGREG": "co_fat_agreg"})
    return _ncm_fat_agreg_cache


def get_year_by_fator_agregado(flow: str, year: int) -> pd.DataFrame:
    """Baixa o CSV anual (bulk), junta contra NCM.csv e agrega VL_FOB por
    (mes, categoria de Fator Agregado).

    Args:
        flow: "export" ou "import".
        year: ano civil.

    Returns:
        DataFrame com colunas: month ("01".."12", str), categoria (str —
        "basicos"/"semimanufaturados"/"manufaturados"/"transacoes_especiais"/
        "consumo_bordo"/"reexportacao"/"nao_classificado"), value_usd
        (float, VL_FOB somado). "nao_classificado" cobre NCMs sem
        correspondencia em NCM.csv (residual pequeno, <0.05% do total em
        2025) — o caller tipicamente soma isso junto com as 3 categorias de
        "operacoes especiais" num bucket "demais".
    """
    prefix = "EXP" if flow == "export" else "IMP"
    url = f"{_BASE}/{prefix}_{year}.csv"
    content = _get_csv_bytes(url, timeout=180.0)

    df = pd.read_csv(
        io.BytesIO(content),
        sep=";",
        usecols=["CO_MES", "CO_NCM", "VL_FOB"],
        dtype={"CO_MES": str, "CO_NCM": str},
    )
    ncm_map = get_ncm_fator_agregado()
    df = df.merge(ncm_map, left_on="CO_NCM", right_on="co_ncm", how="left")
    df["categoria"] = df["co_fat_agreg"].map(_FAT_AGREG_LABELS).fillna("nao_classificado")

    agg = df.groupby(["CO_MES", "categoria"], as_index=False)["VL_FOB"].sum()
    return agg.rename(columns={"CO_MES": "month", "VL_FOB": "value_usd"})


_ncm_sh6_cache: pd.DataFrame | None = None


def get_ncm_sh6() -> pd.DataFrame:
    """Tabela de correlacao NCM (8 digitos) -> SH6 (Sistema Harmonizado, 6 digitos).

    Cacheada em memoria apos o primeiro fetch. SH4 (posicao) e SH2
    (capitulo) sao derivados truncando SH6 (`co_sh6.str[:4]`/`str[:2]`).

    Returns:
        DataFrame com colunas: co_ncm (str), co_sh6 (str, 6 digitos).
    """
    global _ncm_sh6_cache
    if _ncm_sh6_cache is None:
        url = f"{_TABELAS_BASE}/NCM.csv"
        content = _get_csv_bytes(url, timeout=120.0)
        df = pd.read_csv(
            io.BytesIO(content),
            sep=";",
            usecols=["CO_NCM", "CO_SH6"],
            dtype={"CO_NCM": str, "CO_SH6": str},
            encoding="latin1",
        )
        _ncm_sh6_cache = df.rename(columns={"CO_NCM": "co_ncm", "CO_SH6": "co_sh6"})
    return _ncm_sh6_cache


def get_year_by_produto(flow: str, year: int, produtos: dict[str, str]) -> pd.DataFrame:
    """Baixa o CSV anual (bulk), junta contra NCM.csv (SH6) e agrega VL_FOB
    por (mes, produto), casando por prefixo de codigo SH (2 ou 4 digitos).

    Args:
        flow: "export" ou "import".
        year: ano civil.
        produtos: dict {nome: prefixo_sh} (ex: {"soja": "1201", "carnes": "02"}
                   — prefixo casado contra os primeiros N digitos de CO_SH6).

    Returns:
        DataFrame com colunas: month, produto (str — uma chave de `produtos`,
        ou "mundo" para o total geral, sem filtro), value_usd. "mundo"
        permite ao caller calcular "Demais Produtos" como residual, igual ao
        padrao de cmb_comex_pais.py.
    """
    prefix = "EXP" if flow == "export" else "IMP"
    url = f"{_BASE}/{prefix}_{year}.csv"
    content = _get_csv_bytes(url, timeout=180.0)

    df = pd.read_csv(
        io.BytesIO(content),
        sep=";",
        usecols=["CO_MES", "CO_NCM", "VL_FOB"],
        dtype={"CO_MES": str, "CO_NCM": str},
    )
    sh_map = get_ncm_sh6()
    df = df.merge(sh_map, left_on="CO_NCM", right_on="co_ncm", how="left")
    df["co_sh6"] = df["co_sh6"].fillna("")

    frames = []
    mundo = df.groupby("CO_MES", as_index=False)["VL_FOB"].sum()
    mundo["produto"] = "mundo"
    frames.append(mundo.rename(columns={"VL_FOB": "value_usd"})[["CO_MES", "produto", "value_usd"]])

    for nome, prefixo in produtos.items():
        sub = df[df["co_sh6"].str.startswith(prefixo)]
        agg = sub.groupby("CO_MES", as_index=False)["VL_FOB"].sum()
        agg["produto"] = nome
        frames.append(agg.rename(columns={"VL_FOB": "value_usd"})[["CO_MES", "produto", "value_usd"]])

    out = pd.concat(frames, ignore_index=True)
    return out.rename(columns={"CO_MES": "month"})
