"""
Risco-pais (CDS Brasil 5 anos, USD) — export manual da Bloomberg.

Substitui, em 2026-09-08, o loader que lia os CSVs do investing.com
(`domain/db/brasil/investing/`, removido no mesmo dia). A troca nao foi
cosmetica: nos 4.850 dias em que as duas fontes se sobrepoem, SO 13 valores
coincidiam (0,3%), com diferenca mediana de 2,14 bps e maxima de 126,5. Nao
era arredondamento nem defasagem — a correlacao das variacoes diarias e maxima
em lag 0 (0,80) e cai para 0,25 em qualquer vizinho, ou seja as datas estavam
certas e os valores e' que divergiam. Tres defeitos concretos do investing.com,
todos ausentes aqui:

  * 21/04 a 24/09/2008 era UMA cotacao congelada (121,65 em 113 pregoes). A
    Bloomberg tem 110 valores distintos no mesmo trecho, de 85,2 a 248,1 — o
    mercado se movia enquanto a fonte repetia um numero. Erro medio 18,9 bps.
  * 02/12 a 31/12/2015 faltava inteiro (o pior mes possivel: rebaixamento pela
    S&P e pela Fitch). Aqui os 23 pregoes existem, de 445,5 a 507,2.
  * 33 dias uteis faltantes ao todo, e a serie ainda congelava no presente
    (2,1% de dias sem variacao de 2011 pra ca, contra 0,2% da Bloomberg).

Ganho de amostra: a serie comeca em 2001-10-12 em vez de 2007-12-19. Isso
importa porque `fiscal` (esta tabela) e' o canal que amarrava o inicio do
ajuste do modelo Ridge — ver o docstring de `_standardize_ext()` em
analytics/brasil/exchange_rate/models/ridge_deviation_model.py.

Fonte: tela `BRAZIL CDS USD SR 5Y D14`, security `CBRZ1U5 CBIN Curncy`, campo
`PX_LAST`, em bps. Como o investing.com antes dela, NAO ha conector de API — a
Bloomberg nao e' acessivel deste ambiente, entao run() le o xlsx ja presente em
raw/ em vez de buscar de uma fonte externa. Para atualizar, exportar um xlsx
novo com as duas abas (`CDS-BR-5Y` e `Metadados`) e coloca-lo em raw/.

**Um export por vez, e o mais recente vence.** Diferente do loader antigo, que
combinava todos os CSVs de raw/, aqui so o xlsx de nome mais recente e' lido, e
a tabela e' TRUNCADA antes da carga. Os dois andam juntos e o motivo e' o
achado acima: misturar exports de fontes que discordam em 99,7% dos dias
produz uma serie que nao e' nenhuma das duas, e o `drop_duplicates` que
resolveria o conflito o resolveria pela ordem alfabetica do nome do arquivo —
criterio que nao tem nada a ver com qualidade de dado. Uma fonte, um arquivo.

Cobertura conferida na carga: 100% dos dias uteis de 2004 em diante; 84% em
2001-2003, quando o mercado de CDS soberano brasileiro ainda era ralo. A grade
e' de dia util (zero linhas em fim de semana) e cotacao existe em feriado, entao
dia util ausente e' ausencia de fato, nao convencao de calendario.

Banco: macro_brasil.cmb_risco_pais — PRIMARY KEY (date, name)
"""

import logging
from pathlib import Path

import pandas as pd

from connectors.mysql import (
    backup_table_before_truncate,
    insert_data_into_database,
    truncate_table,
)

logger = logging.getLogger(__name__)

_DATABASE = "macro_brasil"
_TABLE    = "cmb_risco_pais"
_NOME     = "cds_5y_usd"
_RAW_DIR  = Path(__file__).resolve().parent / "raw"
_BACKUP   = Path(__file__).resolve().parent / "backup"

_ABA_DADOS = "CDS-BR-5Y"
_ABA_META  = "Metadados"

# A aba de metadados traz contagem/min/max/ultimo calculados pela propria
# extracao. Conferir contra o que lemos separa "o export veio truncado" de
# "a serie mudou" — sem isso um xlsx cortado pela metade carrega em silencio.
# Tolerancia em bps: a aba imprime 3 casas, entao 0.001 e' o piso do
# arredondamento e nao um numero escolhido.
_TOL_BPS = 0.001


def _ler_meta(xlsx: Path) -> dict:
    meta = pd.read_excel(xlsx, sheet_name=_ABA_META, header=None)
    return {str(k).strip(): v for k, v in meta.itertuples(index=False)}


def _validar(df: pd.DataFrame, meta: dict, xlsx: Path) -> None:
    """Levanta se o que lemos discorda do que a propria extracao declarou."""
    def _num(*chaves) -> float | None:
        for k, v in meta.items():
            # A aba vem com acentuacao inconsistente conforme o encoding do
            # export ("Numero"/"N. de observacoes"), entao casa por prefixo
            # ASCII em vez de por igualdade.
            alvo = "".join(c for c in k.lower() if c.isalnum())
            if any(alvo.startswith(c) for c in chaves):
                return float(v)
        return None

    esperado_n = _num("nde", "node", "nobserv", "numerode")
    if esperado_n is not None and len(df) != int(esperado_n):
        raise ValueError(
            f"{xlsx.name}: a aba {_ABA_META} declara {int(esperado_n)} observacoes, "
            f"mas a aba {_ABA_DADOS} tem {len(df)} — export truncado?"
        )

    for chaves, obtido, rotulo in (
        (("minimo",), df["value"].min(), "minimo"),
        (("maximo",), df["value"].max(), "maximo"),
        (("ultimo",), df["value"].iloc[-1], "ultimo"),
    ):
        esperado = _num(*chaves)
        if esperado is not None and abs(float(obtido) - esperado) > _TOL_BPS:
            raise ValueError(
                f"{xlsx.name}: {rotulo} declarado {esperado} != lido {obtido}"
            )

    if df["date"].duplicated().any():
        dups = df.loc[df["date"].duplicated(), "date"].dt.date.tolist()[:5]
        raise ValueError(f"{xlsx.name}: datas repetidas na aba de dados: {dups}")
    if (df["value"] <= 0).any():
        raise ValueError(f"{xlsx.name}: spread <= 0, que nao existe em CDS")
    if df["date"].dt.dayofweek.isin([5, 6]).any():
        n = int(df["date"].dt.dayofweek.isin([5, 6]).sum())
        raise ValueError(f"{xlsx.name}: {n} linhas em fim de semana — grade inesperada")


def _cobertura(df: pd.DataFrame) -> str:
    grade = pd.bdate_range(df["date"].min(), df["date"].max())
    faltam = len(grade) - len(df)
    return f"{len(df)} obs / {len(grade)} dias uteis ({100 * len(df) / len(grade):.1f}%), {faltam} ausentes"


def _mais_recente(raw_dir: Path) -> Path:
    xlsxs = sorted(p for p in raw_dir.glob("*.xlsx") if not p.name.startswith("~$"))
    if not xlsxs:
        raise FileNotFoundError(f"nenhum .xlsx em {raw_dir}")
    return xlsxs[-1]


def _load_raw(xlsx: Path) -> pd.DataFrame:
    bruto = pd.read_excel(xlsx, sheet_name=_ABA_DADOS)
    # As duas primeiras colunas sao Data e o nivel em bps; as outras duas sao
    # variacao (bps e %), derivadas e nao armazenadas — nenhuma tabela deste
    # projeto guarda variacao pre-calculada. Posicional em vez de por nome
    # porque o cabecalho vem com acentuacao dependente do encoding do export.
    df = bruto.iloc[:, :2]
    df.columns = ["date", "value"]
    df = df.dropna(subset=["date", "value"]).copy()
    df["date"] = pd.to_datetime(df["date"])
    df["value"] = df["value"].astype(float)
    df = df.sort_values("date").reset_index(drop=True)
    df["name"] = _NOME
    return df[["date", "name", "value"]]


def run(raw_dir: str | None = None) -> None:
    """Recarrega macro_brasil.cmb_risco_pais do xlsx mais recente em raw/.

    Truncate + carga completa, nao upsert: a fonte distribui o historico
    inteiro e substituiu a fonte anterior, entao uma linha da carga antiga que
    sobrevivesse sob a mesma chave seria um valor do investing.com se passando
    por Bloomberg. Backup em CSV antes de truncar (5 rodadas mantidas).

    Args:
        raw_dir: pasta com o xlsx exportado da Bloomberg. Default: raw/ ao
                 lado deste script.
    """
    xlsx = _mais_recente(Path(raw_dir) if raw_dir else _RAW_DIR)
    df = _load_raw(xlsx)
    _validar(df, _ler_meta(xlsx), xlsx)

    logger.info("cmb_risco_pais: %s", xlsx.name)
    logger.info("  %s -> %s | %s", df["date"].min().date(), df["date"].max().date(), _cobertura(df))

    caminho = backup_table_before_truncate(_DATABASE, _TABLE, str(_BACKUP), keep=5)
    if caminho:
        logger.info("  backup da carga anterior: %s", caminho)
    truncate_table(_DATABASE, _TABLE)
    insert_data_into_database(_DATABASE, _TABLE, df)
