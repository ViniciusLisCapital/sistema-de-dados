"""
Connector para o BEA (Bureau of Economic Analysis) — tabelas NIPA da Secao 2
(Personal Income and Outlays), no formato de "underlying detail".

--------------------------------------------------------------------------------
NAO PRECISA DE CHAVE
--------------------------------------------------------------------------------
O `us_project/inflation_fontes_dados.md` registrava "Get the BEA key" como
pendencia para chegar ao PCE com granularidade de tabela NIPA. Nao precisa: o BEA
publica as tabelas inteiras como xlsx aberto no site de release, e o arquivo da
Secao 2 traz as tabelas de underlying detail MENSAIS, que sao justamente as de
maior granularidade. A API, com chave, serviria para vintages e para outras
secoes — nao para isto.

    https://apps.bea.gov/national/Release/XLS/Underlying/Section2All_xls.xlsx

12 MB, 22 abas, sem autenticacao e sem cota. Medido ao vivo em 2026-08.

--------------------------------------------------------------------------------
AS ABAS QUE INTERESSAM
--------------------------------------------------------------------------------
O nome da aba e o numero da tabela sem pontos, mais o sufixo de frequencia:

As 7 tabelas do arquivo, todas SA, com o numero de linhas e de meses medidos:

  aba         tabela   conteudo                                linhas   meses
  U20404-M    2.4.4U   indice de preco, 2017=100                  402     810
  U20405-M    2.4.5U   despesa nominal, US$ mi SAAR               402     810
  U20403-M    2.4.3U   PCE real, indices de quantidade            402     810
  U20406-M    2.4.6U   PCE real, dolares encadeados               402     234
  U20304-M    2.3.4U   indice de preco, corte grosso               46     810
  U20305-M    2.3.5U   despesa nominal, corte grosso               46     810
  U20306-M    2.3.6U   PCE real encadeado, corte grosso            46     234

`-A` e `-Q` sao as mesmas tabelas em anual e trimestral.

Duas coisas para nao confundir:

- **As 2.3.xU nao sao "o corte por funcao"** — sao "by Major Type of Product **and**
  by Major Function", 46 linhas: uma tabela grossa que mistura os dois criterios, nao
  um espelho de 402 linhas por funcao. A arvore detalhada por funcao e a **2.5.x**, e
  ela NAO esta neste arquivo (a nota de rodape da 2.4.4U referencia as linhas da 2.5.4
  justamente porque e outra tabela).
- **As 4 tabelas 2.4.xU compartilham as MESMAS 402 linhas**, entao a arvore montada
  aqui serve para todas. As de dolares encadeados (`.6U`) comecam bem depois (234
  meses, ~2007) — encadeado nao e publicado ate 1959 nesse detalhe.

**As duas abas que este projeto usa casam linha a linha**: 2.4.4U e 2.4.5U tem as
mesmas 402 linhas de dado, na mesma ordem, com o mesmo rotulo e a mesma
indentacao — conferido linha a linha em `inflc_pce_dim`. Ou seja indice de preco e
valor nominal se juntam pelo NUMERO DA LINHA, sem casar nome, que foi a fonte de
todo o trabalho sujo do lado do CPI (ver `inflc_cpi_dim`: cinco itens perdidos por
uma virgula de diferenca no rotulo).

--------------------------------------------------------------------------------
FORMA DO ARQUIVO
--------------------------------------------------------------------------------
    linha 1   titulo da tabela
    linha 2   unidade  ("[Index numbers, 2017=100; ... seasonally adjusted]")
    linha 3   periodo coberto ("Monthly data from 1959M01 to 2026M06")
    linha 5   data de publicacao
    linha 8   cabecalho: col A = "Line", col D em diante = "1959M01", "1959M02", ...
    linha 9+  dados: col A = numero da linha, col B = rotulo INDENTADO,
              col C = codigo da serie BEA, col D+ = valores

Convencoes do arquivo, todas exercitadas pelo parser:

- **Indentacao = hierarquia**, 2 espacos por nivel, na coluna B. E a unica fonte
  de parentesco no arquivo (nao ha coluna de pai).
- **A linha 1 e a excecao**: `Personal consumption expenditures` vem indentada com
  6 espacos, enquanto `Goods` e `Services` vem com 0. E cosmetico do stub head do
  BEA. `indentacao` sai crua daqui; quem monta a arvore trata a raiz (ver
  `inflc_pce_dim`).
- **`.....`** = nao disponivel. Vira ausencia de linha em `observacoes`.
- **`ZZZZZZ`** na coluna C = o BEA nao publica serie para aquela linha (sao os dois
  "nets": Net expenditures abroad, Net foreign travel). O nominal existe, o indice
  de preco nao.
- **Codigos repetem**: 13 codigos aparecem em duas linhas cada (a mesma serie entra
  duas vezes na arvore — `Health care` sob Household consumption e sob
  Market-based PCE, por exemplo). Conferido: os valores sao identicos nas duas
  posicoes. Por isso a chave e a LINHA, nao o codigo.
- **Rodape**: as ultimas linhas tem texto de nota na coluna A. Sao descartadas
  porque o filtro de linha de dado exige que a coluna A seja um numero.

--------------------------------------------------------------------------------
SO EXISTE SA
--------------------------------------------------------------------------------
O mensal do BEA e dessazonalizado; nao ha contrapartida NSA destas tabelas. Nao e
lacuna de carga, e da fonte — e coerente com o uso (o PCE e lido dessazonalizado).
"""

from __future__ import annotations

import datetime as _dt
import pathlib
import re
import tempfile
import urllib.request
from dataclasses import dataclass

import openpyxl
import pandas as pd

_URL_SECAO2_UNDERLYING = (
    "https://apps.bea.gov/national/Release/XLS/Underlying/Section2All_xls.xlsx"
)

# Onde o xlsx baixado fica. Reaproveitado no mesmo dia: `update_us.py` roda o script
# da dim e o das series na mesma passada, e sem isto baixaria 12 MB duas vezes. O
# cache em memoria (`_wb_cache`) ja resolve isso dentro de um processo; o cache em
# disco existe para uma segunda execucao no mesmo dia nao rebaixar.
#
# No temp do sistema, nao no repositorio: nenhum connector deste projeto grava dado
# baixado dentro da arvore de codigo (`pdet_ftp.py` devolve bytes e deixa o destino
# para quem chama), e um caminho relativo como "data/bea" seria resolvido a partir do
# CWD -- ou seja, escreveria em lugares diferentes dependendo de onde o script roda.
_CACHE_DIR = pathlib.Path(tempfile.gettempdir()) / "lis_bea"

# Marcadores de nota de rodape do BEA, e referencias cruzadas para a linha
# correspondente da tabela 2.5.4 (declaradas na nota do proprio arquivo). Nada disso
# e nome de item; sai do rotulo e o original fica em `rotulo_bruto`.
_NOTA = re.compile(r"\\\d+\\")
_XREF = re.compile(
    r"\s*\((?:parts? of\s+)?\d+(?:[,\s]+(?:and\s+)?(?:parts? of\s+)?\d+)*\)\s*$"
)

_USER_AGENT = "Mozilla/5.0 (LIS Capital macro data pipeline)"

_wb_cache: dict[pathlib.Path, object] = {}


@dataclass
class TabelaNipa:
    """Uma aba mensal de tabela NIPA, ja separada em estrutura e observacoes.

    Attributes:
        aba:          nome da aba ("U20404-M").
        titulo:       titulo publicado ("Table 2.4.4U. Price Indexes for ...").
        unidade:      linha de unidade, entre colchetes, como o BEA escreve.
        periodo:      "Monthly data from 1959M01 to 2026M06".
        publicado_em: "Data published July 30, 2026".
        periodos:     rotulos de periodo na ordem das colunas ("1959M01", ...).
        estrutura:    uma linha por linha da tabela — linha, code, rotulo,
                      rotulo_bruto, indentacao.
        observacoes:  formato longo — linha, date (1o dia do mes), value. Linhas sem
                      valor publicado simplesmente nao aparecem.
    """

    aba: str
    titulo: str
    unidade: str
    periodo: str
    publicado_em: str
    periodos: list[str]
    estrutura: pd.DataFrame
    observacoes: pd.DataFrame

    @property
    def sazonalidade(self) -> str:
        return "SA" if "seasonally adjusted" in self.unidade.lower() else "NSA"


def baixar_secao2_underlying(force: bool = False) -> pathlib.Path:
    """Baixa (ou reaproveita) o xlsx da Secao 2, underlying detail.

    Args:
        force: baixa de novo mesmo que o arquivo de hoje ja exista.

    Returns:
        Caminho do xlsx local.

    Raises:
        RuntimeError: se a resposta for pequena demais para ser o arquivo (tipico de
                      pagina de erro devolvida com status 200).
    """
    _CACHE_DIR.mkdir(parents=True, exist_ok=True)
    dest = _CACHE_DIR / f"Section2All_Underlying_{_dt.date.today():%Y%m%d}.xlsx"
    if dest.exists() and not force:
        return dest

    req = urllib.request.Request(_URL_SECAO2_UNDERLYING, headers={"User-Agent": _USER_AGENT})
    with urllib.request.urlopen(req, timeout=300) as r:
        conteudo = r.read()
    if len(conteudo) < 1_000_000:
        raise RuntimeError(
            f"o xlsx da Secao 2 veio com {len(conteudo):,} bytes, muito menor que os "
            f"~12 MB esperados -- provavelmente uma pagina de erro. "
            f"URL: {_URL_SECAO2_UNDERLYING}"
        )
    dest.write_bytes(conteudo)
    return dest


def _workbook(caminho: pathlib.Path):
    if caminho not in _wb_cache:
        _wb_cache[caminho] = openpyxl.load_workbook(caminho, read_only=True, data_only=True)
    return _wb_cache[caminho]


def _limpar_rotulo(bruto: str) -> str:
    return _XREF.sub("", _NOTA.sub("", bruto).rstrip()).strip()


def _mes(periodo: str) -> _dt.date:
    """'1959M01' -> date(1959, 1, 1)."""
    ano, mes = periodo.split("M")
    return _dt.date(int(ano), int(mes), 1)


def ler_tabela(aba: str, caminho: pathlib.Path | None = None) -> TabelaNipa:
    """Le uma aba mensal do xlsx da Secao 2.

    Args:
        aba:     nome da aba, ex. "U20404-M" (2.4.4U mensal).
        caminho: xlsx local. Default: baixa/reaproveita o do dia.

    Returns:
        TabelaNipa com `estrutura` e `observacoes` separadas.

    Raises:
        KeyError:     se a aba nao existir no arquivo.
        RuntimeError: se o cabecalho nao estiver na forma esperada.
    """
    caminho = caminho or baixar_secao2_underlying()
    wb = _workbook(caminho)
    if aba not in wb.sheetnames:
        raise KeyError(f"aba {aba!r} nao existe em {caminho.name}. Abas: {wb.sheetnames}")

    linhas = list(wb[aba].iter_rows(values_only=True))
    if len(linhas) < 10:
        raise RuntimeError(f"aba {aba!r} tem so {len(linhas)} linhas -- formato inesperado")

    cab = linhas[7]
    if str(cab[0]).strip() != "Line":
        raise RuntimeError(
            f"aba {aba!r}: esperava 'Line' na coluna A da linha 8, achei {cab[0]!r}. "
            "O BEA mudou o layout do arquivo."
        )
    periodos = [str(c) for c in cab[3:] if c]
    fora = [p for p in periodos if not re.fullmatch(r"\d{4}M\d{2}", p)]
    if fora:
        raise RuntimeError(f"aba {aba!r}: periodos fora do formato YYYYMnn: {fora[:5]}")

    datas = [_mes(p) for p in periodos]
    estrutura: list[dict] = []
    obs_linha: list[int] = []
    obs_data: list[_dt.date] = []
    obs_valor: list[float] = []
    for r in linhas[8:]:
        if r[0] is None or not str(r[0]).strip().isdigit():
            continue  # rodape: nota de texto na coluna A
        n = int(str(r[0]).strip())
        bruto = r[1] or ""
        estrutura.append({
            "linha": n,
            "code": (str(r[2]).strip() if r[2] else None),
            "rotulo": _limpar_rotulo(bruto),
            "rotulo_bruto": bruto.strip(),
            "indentacao": len(bruto) - len(bruto.lstrip(" ")),
        })
        for d, v in zip(datas, r[3:3 + len(periodos)]):
            if isinstance(v, (int, float)):
                obs_linha.append(n)
                obs_data.append(d)
                obs_valor.append(float(v))

    return TabelaNipa(
        aba=aba,
        titulo=str(linhas[0][0] or "").strip(),
        unidade=str(linhas[1][0] or "").strip(),
        periodo=str(linhas[2][0] or "").strip(),
        publicado_em=str(linhas[4][0] or "").strip(),
        periodos=periodos,
        estrutura=pd.DataFrame(estrutura),
        observacoes=pd.DataFrame({"linha": obs_linha, "date": obs_data, "value": obs_valor}),
    )


# Abas usadas pelo ramo de PCE deste projeto.
ABA_PCE_INDICE = "U20404-M"
ABA_PCE_NOMINAL = "U20405-M"
