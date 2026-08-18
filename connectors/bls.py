"""
Connector para o BLS (Bureau of Labor Statistics) — API publica v2 mais os
arquivos brutos de `download.bls.gov` e as tabelas de importancia relativa do CPI.

Tres caminhos de acesso, com papeis diferentes:

1. **API** (`get_series`) — series por id, JSON. Serve TODAS as pesquisas do BLS
   com a mesma chamada (CPI, PPI, CES, CPS, JOLTS, precos de importacao/
   exportacao) — testado ao vivo. E o caminho para atualizacao incremental.
2. **Arquivos brutos** (`read_flat_table`, `get_data_file`) — o dump completo de
   cada pesquisa em TSV, sem chave e sem limite de requisicao. E o caminho para
   backfill de historico e para as tabelas de dimensao (arvore de itens,
   catalogo de series com begin/end).
3. **Importancia relativa do CPI** (`get_relative_importance`) — xlsx anual com
   o peso de cada item no indice. NAO existe na API nem nos arquivos brutos, e e
   o que viabiliza decomposicao/contribuicao no estilo de `inflc_decomposicao` +
   `inflc_dim` do lado Brasil.

## Chave de API: opcional, mas muda os limites

`BLS_API_KEY` no `.env` (registro gratuito e imediato em
https://data.bls.gov/registrationEngine/). Sem chave a v2 responde normalmente,
mas com os limites da v1 — e a degradacao e SILENCIOSA (`REQUEST_SUCCEEDED` com
um aviso em `message[]`, nunca um erro HTTP):

| Limite                | Sem chave | Com chave |
|-----------------------|-----------|-----------|
| Series por requisicao | 25        | 50        |
| Anos por requisicao   | 10        | 20        |
| Requisicoes por dia   | 25        | 500       |
| `catalog=True`        | ignorado  | funciona  |
| `calculations=True`   | ignorado  | funciona  |

Os limites por requisicao das DUAS colunas foram medidos ao vivo (2026-08-18); a cota diaria e a
unica linha ainda documentada-e-nao-medida, porque o BLS nao expoe contador de uso.

O truncamento de janela e ancorado no `startyear` e avanca para frente: pedir
1990-2026 sem chave devolve **1990-1999** com status de sucesso. Este connector
fatia series e anos ANTES de chamar, e trata qualquer aviso de truncamento como
erro (`BLSTruncationError`) — se o limite real diferir da tabela acima, ele
estoura em vez de devolver a janela errada em silencio.

Exemplo de uso:

    from connectors.bls import BLS

    bls = BLS()

    # --- API: series por id (fatiamento de series/anos e automatico) ---
    df = bls.get_series(["CUSR0000SA0", "CUSR0000SA0L1E"], 1947, 2026)
    # colunas: date (Timestamp, dia 1), series_id, value (float), period

    # --- Arquivos brutos: dimensoes do CPI ---
    itens = bls.get_item_tree("cu")           # item_code / item_name / display_level (0-8)
    catalogo = bls.get_series_catalog("cu")   # 8.104 series com begin_year/end_year

    # --- Arquivos brutos: backfill de historico sem gastar requisicao de API ---
    hist = bls.get_data_file("cu", "cu.data.1.AllItems")

    # --- Importancia relativa (pesos) ---
    pesos = bls.get_relative_importance(2025)  # indent_level / item_name / cpi_u / cpi_w
"""

from __future__ import annotations

import io
import json
import os
import re
import time
import warnings

import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()

_API = "https://api.bls.gov/publicAPI/v2/timeseries/data/"
_FLAT = "https://download.bls.gov/pub/time.series/{survey}/{name}"
_FLAT_DIR = "https://download.bls.gov/pub/time.series/{survey}/"
_RI_XLSX = "https://www.bls.gov/cpi/tables/relative-importance/{year}.xlsx"
_RI_HOME = "https://www.bls.gov/cpi/tables/relative-importance/home.htm"

# Limites por requisicao. AMBAS as linhas medidas ao vivo em 2026-08-18 (com e
# sem chave): 51 series -> aviso "limit of 50 series", 21 anos -> aviso "limit of
# 20 years". _check_messages continua tratando truncamento como erro, para o caso
# de o BLS mudar os limites sem aviso.
_LIMITS = {
    False: {"series": 25, "years": 10},
    True: {"series": 50, "years": 20},
}

# Cota diaria de requisicoes (documentada pelo BLS). Usada so para avisar antes
# de uma chamada cara -- o BLS nao expondo contador, nao ha como consultar o uso.
_DAILY_QUOTA = {False: 25, True: 500}

# download.bls.gov recusa o User-Agent default do requests. O BLS pede um UA
# identificavel com contato.
_UA = "LIS Capital macro research (fabian@liscapital.com.br)"

# Medias que o BLS intercala no meio da propria serie: M13/S03 = media anual,
# A01 = anual. Somar ou plotar junto com M01-M12 e o erro classico -- filtradas
# por default (include_aggregates=True mantem).
#
# S01/S02 (1o/2o semestre) NAO entram aqui: sao a frequencia REAL de series que o
# BLS so publica semestralmente (em cu.data.1.AllItems, 100 das 201 series sao
# semestrais e 101 mensais -- nenhuma tem as duas, conferido ao vivo). Filtra-las
# apagaria dado legitimo. Use a coluna `period` para separar frequencias.
_AGGREGATE_PERIODS = {"M13", "S03", "A01"}

# Primeiro ano com dado em qualquer pesquisa do BLS (CPI-U NSA comeca em 1913).
_MIN_YEAR = 1913

# "... U.S. city average, December 2025" -> mes de referencia dos pesos.
_MONTH_YEAR = re.compile(
    r"\b(January|February|March|April|May|June|July|August|September|October"
    r"|November|December)\s+(\d{4})\b",
    re.I,
)


class BLSError(RuntimeError):
    """Falha reportada pela API do BLS (status != REQUEST_SUCCEEDED)."""


class BLSTruncationError(BLSError):
    """A API truncou a lista de series ou a janela de anos.

    Nunca deve acontecer: o connector fatia antes de chamar. Se acontecer, os
    limites reais diferem de `_LIMITS` e o resultado seria uma janela errada
    devolvida com status de sucesso.
    """


class BLS:
    """Cliente para a API e os arquivos publicos do BLS."""

    def __init__(
        self,
        api_key: str | None = None,
        *,
        timeout: float = 90.0,
        retries: int = 3,
        backoff: float = 2.0,
        sleep_between: float = 0.2,
        user_agent: str = _UA,
    ):
        self.api_key = api_key if api_key is not None else os.environ.get("BLS_API_KEY", "")
        self.timeout = timeout
        self.retries = retries
        self.backoff = backoff
        self.sleep_between = sleep_between
        self._session = requests.Session()
        self._session.headers.update({"User-Agent": user_agent})

    @property
    def registered(self) -> bool:
        """True se ha chave de API configurada (limites maiores, catalog/calculations)."""
        return bool(self.api_key)

    @property
    def limits(self) -> dict[str, int]:
        """Limites por requisicao vigentes para esta instancia."""
        return dict(_LIMITS[self.registered])

    # ------------------------------------------------------------------ API

    def get_series(
        self,
        series_ids: str | list[str],
        start_year: int | None = None,
        end_year: int | None = None,
        *,
        include_aggregates: bool = False,
        annual_average: bool = False,
        calculations: bool = False,
        catalog: bool = False,
        keep_footnotes: bool = False,
        strict: bool = True,
    ) -> pd.DataFrame:
        """Baixa series por id e devolve formato long (date, series_id, value, period).

        Fatia automaticamente por numero de series e por janela de anos conforme
        `self.limits`, e concatena. Uma requisicao por (bloco de series x bloco
        de anos) — atencao a cota diaria de 25 requisicoes sem chave.

        Args:
            series_ids: id unico ou lista de ids do BLS (ex: "CUSR0000SA0").
            start_year: primeiro ano. Default: 1913 (inicio do CPI mais longo).
            end_year: ultimo ano. Default: ano corrente.
            include_aggregates: manter as linhas de MEDIA do periodo (M13/S03/A01)
                que o BLS intercala na serie. Default False. Nao afeta S01/S02,
                que sao a frequencia real de series semestrais.
            annual_average: pedir a media anual ao BLS (`annualaverage=True`).
                So faz sentido junto com include_aggregates=True.
            calculations: pedir as variacoes calculadas pelo BLS. Exige chave.
            catalog: pedir a metadata do catalogo. Exige chave.
            keep_footnotes: manter a coluna de footnotes (ex: "R" = revisado).
            strict: levantar BLSError se algum id for invalido. Com False, apenas
                emite warning e devolve o resto.

        Returns:
            DataFrame com date (Timestamp, dia 1 do periodo), series_id,
            value (float), period (codigo bruto: M01..M13, S01..S03).
            Ordenado por series_id, date.
        """
        ids = [series_ids] if isinstance(series_ids, str) else list(dict.fromkeys(series_ids))
        empty_cols = ["date", "series_id", "value", "period"] + (["footnotes"] if keep_footnotes else [])
        if not ids:
            return pd.DataFrame(columns=empty_cols)

        end_year = end_year or pd.Timestamp.today().year
        start_year = start_year or _MIN_YEAR
        if start_year > end_year:
            raise ValueError(f"start_year ({start_year}) > end_year ({end_year})")

        if (catalog or calculations) and not self.registered:
            warnings.warn(
                "catalog/calculations exigem BLS_API_KEY; o BLS vai ignorar os flags. "
                "Registre em https://data.bls.gov/registrationEngine/",
                stacklevel=2,
            )

        lim = self.limits
        id_blocks = _chunks(ids, lim["series"])
        windows = _year_windows(start_year, end_year, lim["years"])
        n_requests = len(id_blocks) * len(windows)
        if n_requests > _DAILY_QUOTA[self.registered]:
            warnings.warn(
                f"esta chamada gasta {n_requests} requisicoes e a cota diaria "
                f"{'com' if self.registered else 'sem'} chave e "
                f"{_DAILY_QUOTA[self.registered]}. Para historico longo prefira "
                f"get_data_file() (arquivo bruto, sem cota) e deixe a API para a "
                f"janela recente.",
                stacklevel=2,
            )

        frames: list[pd.DataFrame] = []
        invalid: set[str] = set()

        for id_block in id_blocks:
            for y0, y1 in windows:
                payload: dict = {
                    "seriesid": id_block,
                    "startyear": str(y0),
                    "endyear": str(y1),
                }
                if self.registered:
                    payload["registrationKey"] = self.api_key
                if annual_average:
                    payload["annualaverage"] = True
                if calculations:
                    payload["calculations"] = True
                if catalog:
                    payload["catalog"] = True

                data = self._post(payload)
                invalid |= _invalid_series(data.get("message", []))
                frames.append(
                    _parse_series(
                        data.get("Results", {}).get("series", []),
                        keep_footnotes=keep_footnotes,
                    )
                )
                time.sleep(self.sleep_between)

        if invalid:
            msg = f"ids invalidos para o BLS: {sorted(invalid)}"
            if strict:
                raise BLSError(msg)
            warnings.warn(msg, stacklevel=2)

        df = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame(columns=empty_cols)
        if df.empty:
            return pd.DataFrame(columns=empty_cols)

        if not include_aggregates:
            df = df[~df["period"].isin(_AGGREGATE_PERIODS)]

        df = df.drop_duplicates(subset=["series_id", "date", "period"])
        return df.sort_values(["series_id", "date"]).reset_index(drop=True)

    def _post(self, payload: dict) -> dict:
        """POST na API com retry em falha transitoria, e checagem das mensagens."""
        last_exc: Exception | None = None
        for attempt in range(self.retries):
            try:
                r = self._session.post(
                    _API,
                    data=json.dumps(payload),
                    headers={"Content-type": "application/json"},
                    timeout=self.timeout,
                )
                if r.status_code in (429, 500, 502, 503, 504):
                    raise requests.HTTPError(f"HTTP {r.status_code}")
                r.raise_for_status()
                data = r.json()
            except (requests.RequestException, ValueError) as exc:
                last_exc = exc
                if attempt < self.retries - 1:
                    time.sleep(self.backoff * (attempt + 1))
                    continue
                raise BLSError(
                    f"falha na API do BLS depois de {self.retries} tentativas: {exc}"
                ) from exc

            status = data.get("status")
            if status != "REQUEST_SUCCEEDED":
                detail = "; ".join(data.get("message", [])) or str(status)
                # Chave invalida e cota diaria estourada nao sao transitorias.
                raise BLSError(f"BLS respondeu {status}: {detail}")

            _check_messages(data.get("message", []))
            return data

        raise BLSError(f"falha na API do BLS: {last_exc}")

    # --------------------------------------------------- arquivos brutos

    def get_flat_file(self, survey: str, name: str) -> bytes:
        """Baixa um arquivo bruto de download.bls.gov/pub/time.series/<survey>/.

        Sem chave e sem limite de requisicao. `survey` e o codigo de duas letras
        (cu = CPI-U, cw = CPI-W, su = C-CPI-U, wp = PPI commodity, pc = PPI
        industry, ce = CES, ln = CPS, jt = JOLTS, ei = precos de imp/exp).
        """
        url = _FLAT.format(survey=survey, name=name)
        r = self._session.get(url, timeout=self.timeout)
        r.raise_for_status()
        # O BLS serve pagina de erro com HTTP 200 em path errado -- checar corpo.
        head = r.content[:200].lstrip().lower()
        if head.startswith((b"<!doctype", b"<html")):
            raise BLSError(f"{url} devolveu HTML (path invalido?), nao o arquivo")
        if not r.content:
            raise BLSError(f"{url} devolveu corpo vazio")
        return r.content

    def read_flat_table(self, survey: str, name: str) -> pd.DataFrame:
        """Le um arquivo bruto TSV do BLS num DataFrame, com colunas/valores strip()ados.

        Os arquivos do BLS tem padding de espacos em quase toda coluna de texto
        (`'CUSR0000SA0      '`), inclusive nos nomes de coluna.
        """
        raw = self.get_flat_file(survey, name)
        df = pd.read_csv(io.BytesIO(raw), sep="\t", dtype=str, encoding="latin1")
        df.columns = [c.strip() for c in df.columns]
        for col in df.columns:
            if df[col].dtype == object:
                df[col] = df[col].str.strip()
        return df

    def list_flat_files(self, survey: str) -> list[str]:
        """Lista os arquivos disponiveis no diretorio de uma pesquisa."""
        r = self._session.get(_FLAT_DIR.format(survey=survey), timeout=self.timeout)
        r.raise_for_status()
        pat = rf"/pub/time\.series/{re.escape(survey)}/([A-Za-z0-9._\-]+)"
        return sorted(set(re.findall(pat, r.text)))

    def get_item_tree(self, survey: str = "cu") -> pd.DataFrame:
        """Arvore de itens de uma pesquisa (`<survey>.item`).

        Para o CPI: 400 itens com `display_level` 0-8 — o equivalente direto de
        `inflc_dim` do lado Brasil. `display_level` e a profundidade na hierarquia
        de despesa; NAO ha coluna de pai, o pai e inferido pelo item anterior de
        nivel menor na ordem de `sort_sequence`.
        """
        df = self.read_flat_table(survey, f"{survey}.item")
        for col in ("display_level", "sort_sequence"):
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")
        return df

    def get_series_catalog(self, survey: str = "cu") -> pd.DataFrame:
        """Catalogo completo de series de uma pesquisa (`<survey>.series`).

        Traz series_id, os codigos de dimensao (area/item/seasonal/periodicity),
        o titulo e — o que a API nao da sem chave — `begin_year`/`begin_period` e
        `end_year`/`end_period` de cada serie. E como descobrir o que existe sem
        gastar requisicao de API.
        """
        df = self.read_flat_table(survey, f"{survey}.series")
        for col in ("begin_year", "end_year"):
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")
        return df

    def get_data_file(
        self,
        survey: str,
        name: str,
        *,
        include_aggregates: bool = False,
    ) -> pd.DataFrame:
        """Le um arquivo de dados bruto (`<survey>.data.*`) em formato long.

        Caminho de BACKFILL: devolve o historico completo de todas as series do
        arquivo numa requisicao, sem chave e sem gastar cota. Escolha o arquivo
        por grupo de itens (`list_flat_files`) — `cu.data.0.Current` tem 49 MB.

        Returns:
            DataFrame com date, series_id, value, period (+ footnotes).
        """
        df = self.read_flat_table(survey, name)
        df = df.rename(columns={"footnote_codes": "footnotes"})
        df["value"] = pd.to_numeric(df["value"], errors="coerce")
        df["date"] = [_to_date(y, p) for y, p in zip(df["year"], df["period"])]
        if not include_aggregates:
            df = df[~df["period"].isin(_AGGREGATE_PERIODS)]
        df = df.dropna(subset=["date"])
        cols = [c for c in ("date", "series_id", "value", "period", "footnotes") if c in df.columns]
        return df[cols].sort_values(["series_id", "date"]).reset_index(drop=True)

    # ------------------------------------- importancia relativa do CPI

    def list_relative_importance_years(self) -> list[int]:
        """Anos com xlsx de importancia relativa publicado (varre a pagina do BLS)."""
        r = self._session.get(_RI_HOME, timeout=self.timeout)
        r.raise_for_status()
        years = re.findall(r"relative-importance/(\d{4})\.xlsx", r.text)
        return sorted({int(y) for y in years})

    def relative_importance_tables(self, year: int) -> dict[str, str]:
        """Mapeia aba -> titulo do xlsx de importancia relativa de um ano."""
        xl = pd.ExcelFile(io.BytesIO(self._ri_bytes(year)))
        out = {}
        for sheet in xl.sheet_names:
            head = xl.parse(sheet, header=None, nrows=3)
            title = ""
            for val in head.to_numpy().ravel():
                if isinstance(val, str) and val.strip().lower().startswith("table"):
                    title = val.strip()
                    break
            out[sheet] = title
        return out

    def get_relative_importance(self, year: int, sheet: str = "Table 1") -> pd.DataFrame:
        """Importancia relativa (peso, % do indice) de cada item do CPI num ano.

        Esta e a peca que NAO existe na API nem nos arquivos brutos, e sem a qual
        nao ha contribuicao/decomposicao — o equivalente de `inflc_dim.peso`.

        Quatro coisas que o formato do BLS impoe, todas verificadas ao vivo:

        1. **O ano do arquivo nao e o ano dos pesos.** `2025.xlsx` diz "Table 1
           (2024 Weights) ... December 2025": cesta de despesa de 2024, atualizada
           a preco de dezembro de 2025. `weights_year` e `reference_period` leem
           os dois rotulos do proprio arquivo em vez de assumir. O rotulo de peso
           so existe de 2022 em diante (quando o BLS passou a peso anual); em
           2020/2021 `weights_year` volta None e a cesta e bienal.
        2. **Cada tabela empilha varias arvores independentes.** A Table 1 tem
           "Expenditure category" (a arvore de despesa, que soma 100 no nivel 1) e
           "Special aggregate indexes" (cortes alternativos e sobrepostos — "All
           items less food and energy", "Services less energy services" — que
           somam 664). Sao separadas pela coluna `section`; somar sem filtrar da
           764 em vez de 100.
        3. **A chave e o NOME do item + o nivel de indentacao, nao `item_code`.**
           Juntar com `get_item_tree()`/`get_series_catalog()` exige casamento por
           nome (ver connectors/CLAUDE.md).
        4. **As tabelas 2-6 sao grades de area x populacao** com 2-3 linhas de
           header e celulas mescladas. Por isso o retorno e sempre long: uma linha
           por (item, area, populacao).

        Args:
            year: ano do arquivo publicado (ver list_relative_importance_years()).
            sheet: aba. "Table 1" = US city average (o caso de uso normal),
                "Table 2"/"Table 3" = areas metropolitanas, "Table 4" = regioes,
                "Table 5" = classes de tamanho de populacao, "Table 6" = cruzamento
                regiao x tamanho, "Table 7" = peso de cada area (nesta, `item_name`
                carrega nomes de area, nao de item).

        Returns:
            DataFrame long com year, weights_year, reference_period (Timestamp),
            sheet, section, indent_level (int), item_name, area, population
            ("CPI-U"/"CPI-W"), weight (float, % do indice).
        """
        raw = pd.ExcelFile(io.BytesIO(self._ri_bytes(year))).parse(sheet, header=None)

        weights_year, reference_period = None, None
        for val in raw.head(4).to_numpy().ravel():
            if not isinstance(val, str):
                continue
            if weights_year is None:
                m = re.search(r"\((\d{4})\s+Weights?\)", val, re.I)
                if m:
                    weights_year = int(m.group(1))
            if reference_period is None:
                # O mes de referencia vem no fim do titulo, mas nem sempre no fim
                # da string: a Table 2 termina com "(Cities normally priced...)".
                m = re.search(_MONTH_YEAR, val)
                if m:
                    try:
                        reference_period = pd.Timestamp(f"{m.group(1)} 1, {m.group(2)}")
                    except ValueError:
                        pass

        # A linha de header e a que traz "Indent Level" na primeira coluna.
        hdr = None
        for i in range(min(15, len(raw))):
            if str(raw.iat[i, 0]).strip().lower() == "indent level":
                hdr = i
                break
        if hdr is None:
            raise BLSError(f"nao achei a linha 'Indent Level' na aba {sheet!r} de {year}")

        # Primeira linha de dado = primeira cujo "Indent Level" e numerico. O que
        # esta entre o header e ela sao linhas de sub-header (1 a 3, dependendo da
        # tabela: area / classe de tamanho / CPI-U vs CPI-W).
        first_data = None
        for i in range(hdr + 1, len(raw)):
            if pd.notna(pd.to_numeric(raw.iat[i, 0], errors="coerce")):
                first_data = i
                break
        if first_data is None:
            raise BLSError(f"aba {sheet!r} de {year} nao tem linha de dado")

        col_area, col_pop = _ri_column_labels(raw, hdr, first_data)

        body = raw.iloc[first_data:].copy()
        body[0] = pd.to_numeric(body[0], errors="coerce")
        body = body.dropna(subset=[0])
        body = body[body[1].notna()]
        if body.empty:
            raise BLSError(f"aba {sheet!r} de {year} nao tem linhas de item")

        weight_cols = sorted(col_pop)
        # Linhas de secao: nivel 0 sem nenhum peso. Marcam a arvore a que
        # pertencem as linhas seguintes.
        is_header = body[weight_cols].apply(
            lambda r: pd.to_numeric(r, errors="coerce").isna().all(), axis=1
        ) & (body[0] == 0)
        section = body[1].where(is_header).ffill()

        rows = []
        for idx in body.index[~is_header]:
            for col in weight_cols:
                weight = pd.to_numeric(body.at[idx, col], errors="coerce")
                if pd.isna(weight):
                    continue
                rows.append(
                    {
                        "year": year,
                        "weights_year": weights_year,
                        "reference_period": reference_period,
                        "sheet": sheet,
                        "section": section.get(idx),
                        "indent_level": int(body.at[idx, 0]),
                        "item_name": str(body.at[idx, 1]).strip(),
                        "area": col_area.get(col),
                        "population": col_pop.get(col),
                        "weight": float(weight),
                    }
                )
        return pd.DataFrame(rows)

    def _ri_bytes(self, year: int) -> bytes:
        r = self._session.get(_RI_XLSX.format(year=year), timeout=self.timeout)
        if r.status_code == 404 or r.content[:2] != b"PK":
            raise BLSError(
                f"importancia relativa de {year} nao disponivel (HTTP {r.status_code}). "
                "Ver list_relative_importance_years() para os anos publicados -- hoje 2020-2025. "
                "Antes disso so existe historical-relative-importance-1947-1986.xlsx (formato "
                "diferente) e um zip de 1987-1989; 1990-2019 nao tem arquivo nessa pagina."
            )
        r.raise_for_status()
        return r.content


# ------------------------------------------------------------- helpers


def _chunks(seq: list, size: int) -> list[list]:
    return [seq[i : i + size] for i in range(0, len(seq), size)]


def _year_windows(start: int, end: int, span: int) -> list[tuple[int, int]]:
    """Janelas de no maximo `span` anos cobrindo [start, end]."""
    out = []
    y = start
    while y <= end:
        out.append((y, min(y + span - 1, end)))
        y += span
    return out


def _ri_column_labels(
    raw: pd.DataFrame, hdr: int, first_data: int
) -> tuple[dict[int, str | None], dict[int, str]]:
    """Resolve os rotulos de cada coluna de peso das tabelas de importancia relativa.

    O header ocupa de 1 a 3 linhas com celulas mescladas: area (Table 2-4),
    classe de tamanho (Table 5-6) e populacao (CPI-U vs CPI-W) podem estar em
    linhas diferentes. Cada linha de header e forward-filled entre colunas para
    desfazer o merge; o token CPI-U/CPI-W vira `population` e o resto, `area`.

    Returns:
        (col_area, col_pop) indexados pelo numero da coluna do DataFrame bruto.
        Colunas sem nenhum rotulo ficam fora de col_pop e sao ignoradas.
    """
    n_cols = raw.shape[1]
    layers: list[dict[int, str]] = []
    for i in range(hdr, first_data):
        row = raw.iloc[i, 2:n_cols].copy()
        row = row.map(lambda v: re.sub(r"\s+", " ", str(v)).strip() if pd.notna(v) else None)
        filled = row.ffill()
        layers.append({j: v for j, v in filled.items() if v})

    col_area: dict[int, str | None] = {}
    col_pop: dict[int, str] = {}
    for j in range(2, n_cols):
        labels = [layer[j] for layer in layers if j in layer]
        pops = [x for x in labels if x.upper() in ("CPI-U", "CPI-W")]
        rest = [x for x in labels if x.upper() not in ("CPI-U", "CPI-W")]
        if not pops and not rest:
            continue
        col_pop[j] = pops[-1].upper() if pops else "CPI-U"
        col_area[j] = " | ".join(dict.fromkeys(rest)) or None
    return col_area, col_pop


def _check_messages(messages: list[str]) -> None:
    """Estoura se o BLS avisou que truncou series ou janela de anos."""
    for m in messages:
        if "reduced to the system-allowed limit" in m.lower():
            raise BLSTruncationError(
                f"BLS truncou a requisicao ({m!r}). Os limites reais diferem de "
                "connectors.bls._LIMITS -- corrigir a tabela antes de confiar no resultado."
            )


def _invalid_series(messages: list[str]) -> set[str]:
    """Extrai ids invalidos das mensagens ('Invalid Series for Series XYZ')."""
    out = set()
    for m in messages:
        found = re.search(r"invalid series\s+for\s+series\s+(\S+)", m, re.I)
        if found:
            out.add(found.group(1))
    return out


def _to_date(year, period) -> pd.Timestamp | None:
    """Converte (year, period) do BLS num Timestamp no primeiro dia do periodo.

    M01-M12 -> mes. M13/S03/A01 (media anual) -> 1 de janeiro. S01/S02
    (semestres) -> 1 de janeiro / 1 de julho. Q01-Q04 -> inicio do trimestre.
    Qualquer outro codigo -> None.

    O connector antigo (`not_in_production/bls.py`) fazia `int(period[1:])` como
    mes, o que estoura em M13 e devolve data errada em S01/S02.
    """
    try:
        y = int(year)
    except (TypeError, ValueError):
        return None
    p = str(period).strip().upper()
    if len(p) < 2:
        return None
    kind, num = p[0], p[1:]
    try:
        n = int(num)
    except ValueError:
        return None

    if kind == "M":
        if 1 <= n <= 12:
            return pd.Timestamp(year=y, month=n, day=1)
        if n == 13:
            return pd.Timestamp(year=y, month=1, day=1)
        return None
    if kind == "S":
        return {
            1: pd.Timestamp(year=y, month=1, day=1),
            2: pd.Timestamp(year=y, month=7, day=1),
            3: pd.Timestamp(year=y, month=1, day=1),
        }.get(n)
    if kind == "Q" and 1 <= n <= 4:
        return pd.Timestamp(year=y, month=(n - 1) * 3 + 1, day=1)
    if kind == "A":
        return pd.Timestamp(year=y, month=1, day=1)
    return None


def _parse_series(series: list[dict], *, keep_footnotes: bool) -> pd.DataFrame:
    """Achata a resposta JSON da API em (date, series_id, value, period)."""
    rows = []
    for s in series:
        sid = s.get("seriesID")
        for obs in s.get("data", []) or []:
            date = _to_date(obs.get("year"), obs.get("period"))
            if date is None:
                continue
            row = {
                "date": date,
                "series_id": sid,
                "value": pd.to_numeric(obs.get("value"), errors="coerce"),
                "period": str(obs.get("period", "")).strip(),
            }
            if keep_footnotes:
                notes = obs.get("footnotes") or []
                row["footnotes"] = ",".join(
                    n.get("code", "") for n in notes if isinstance(n, dict) and n.get("code")
                )
            rows.append(row)
    cols = ["date", "series_id", "value", "period"] + (["footnotes"] if keep_footnotes else [])
    return pd.DataFrame(rows, columns=cols)
