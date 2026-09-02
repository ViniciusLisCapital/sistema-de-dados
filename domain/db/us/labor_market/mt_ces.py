"""
CES (Current Employment Statistics) -- o "payroll" do Employment Situation do BLS.

    from domain.db.us.labor_market import mt_ces
    mt_ces.run()                # ultimos 4 anos (rotina)
    mt_ces.run(anos="all")      # historico completo, 1939-> (carga inicial)

Escreve `macro_us.mt_ces` e, antes, `macro_us.mt_ces_dim` (a arvore de industrias --
ver o docstring dela, que e onde vive a parte dificil deste ramo).

--------------------------------------------------------------------------------
DE ONDE VEM: 30 ARQUIVOS, NAO A API
--------------------------------------------------------------------------------
A CES nao tem um `AllItems` como o JOLTS. Os arquivos sao particionados por
supersetor x familia de medida:

    ce.data.<SS>a.<Nome>.Employment                    18 arquivos, 78 MB
    ce.data.<SS>b.<Nome>.AllEmployeeHoursAndEarnings   12 arquivos
    (as familias `c` -- producao/nao-supervisorios -- e `ce.data.02b/03c`
     ficam de fora nesta rodada, por decisao de escopo do usuario)

Sao ~22 mil series no catalogo; pela API, com o teto de 50 series por requisicao e
20 anos por janela, isso seriam centenas de requisicoes contra a cota diaria. Os
arquivos trazem o historico inteiro sem cota. Mesma decisao do JOLTS, e pelo mesmo
motivo medido. A API entra como CONFERENCIA de vintage (`_conferir_api`).

--------------------------------------------------------------------------------
O series_id DA CES: 13 CARACTERES, E O AJUSTE ESTA NO PREFIXO
--------------------------------------------------------------------------------
    CES  0500000003   ->  CE + S/U + industry_code(8) + data_type(2)
    ^^^^ ^^^^^^^^ ^^
    |    |        \\-- datatype: 01 emprego, 03 ganho/hora, ...
    |    \\----------- industry_code, o mesmo de ce.industry
    \\---------------- CES = dessazonalizado, CEU = bruto

Nao ha campo separado de ajuste: **o terceiro caractere E o ajuste** (`S`/`U`), como
em `CUSR`/`CUUR` do CPI e `JTS`/`JTU` do JOLTS. Confirmado contra `ce.series`: as
22.049 series tem 13 caracteres e os tres campos batem em todas.

--------------------------------------------------------------------------------
A BORDA DIREITA E IRREGULAR, E ISSO NAO E ATRASO -- E O CALENDARIO DA CES
--------------------------------------------------------------------------------
A primeira divulgacao de um mes traz os niveis agregados; o detalhe fino vem com a
divulgacao do mes seguinte. Medido no catalogo (emprego, SA, ago/2026):

    niveis 0-4    todas as 119 series terminam em 2026-M07
    nivel 5       54 em M07, 187 em M06
    niveis 6-7    todas as 482 em M06

Ou seja **nao existe um "ultimo mes" da CES**: existe um por profundidade. Um
`_grade()` como o do JOLTS -- que levanta se os cortes nao compartilham a janela --
reprovaria um passe correto. O relatorio precisa conviver com o degrau, e a
consequencia pratica e que o total nonfarm tem um mes que a maior parte do detalhe
ainda nao tem.

--------------------------------------------------------------------------------
AS 13 MEDIDAS, E QUAL DELAS SOMA ENTRE INDUSTRIAS
--------------------------------------------------------------------------------
Escopo desta rodada (decisao do usuario): emprego, horas e ganhos de **todos os
empregados**, os ganhos reais que o BLS ja publica deflacionados, e os agregados de
horas e folha. Fora: producao/nao-supervisorios, mulheres e os indices de difusao.

A coluna `aditivo` e a que o relatorio usa, e ela nao e cosmetica:

    aditivo = 1   emprego, horas agregadas, folha agregada, overtime agregado
    aditivo = 0   toda MEDIA por trabalhador (horas/semana, ganho/hora, ganho/semana)
                  e todo INDICE (2007=100)

Somar ganho medio por hora de duas industrias nao produz ganho medio de nada -- e uma
media ponderada pelo emprego, e o peso nao esta na serie. Empilhar dois indices de
base 2007=100 tampouco. **Nenhuma medida da CES acumula em 12 meses**: emprego e
estoque, e todo o resto e taxa semanal ou indice; a folha agregada, por exemplo, e
"a folha de UMA semana", entao somar doze meses dela nao da a folha do ano.

--------------------------------------------------------------------------------
DDL
--------------------------------------------------------------------------------
    CREATE TABLE mt_ces (
        date        DATE         NOT NULL COMMENT 'primeiro dia do mes de referencia',
        categoria   VARCHAR(8)   NOT NULL COMMENT 'industry_code; junta com mt_ces_dim.categoria',
        medida      VARCHAR(20)  NOT NULL COMMENT 'emprego, horas_semana, ganho_hora, ... (ver _MEDIDAS)',
        ajuste      VARCHAR(3)   NOT NULL COMMENT 'sa = dessazonalizado, nsa = bruto',
        valor       DECIMAL(14,3) NULL    COMMENT 'na unidade da medida (ver mt_ces_medidas no docstring)',
        natureza    VARCHAR(10)  NOT NULL COMMENT 'estoque | media | indice | agregado',
        aditivo     TINYINT      NOT NULL COMMENT '1 se a medida soma entre industrias',
        preliminar  TINYINT      NOT NULL COMMENT '1 se o BLS marcou o mes como preliminar',
        series_id   VARCHAR(13)  NOT NULL COMMENT 'series_id do BLS, para rastrear a origem',
        PRIMARY KEY (date, categoria, medida, ajuste)
    ) COMMENT 'CES/BLS: emprego, horas e ganhos por industria. Borda direita irregular
               por profundidade da arvore -- ver o docstring do modulo.'
"""

from __future__ import annotations

import pandas as pd

from connectors.bls import BLS
from domain.db.us._gravar import gravar
from domain.db.us.labor_market import mt_ces_dim

_DATABASE = "macro_us"
_TABLE = "mt_ces"

# datatype -> (medida, natureza, aditivo, unidade legivel)
_MEDIDAS = {
    "01": ("emprego", "estoque", 1, "thousands of employees"),
    "02": ("horas_semana", "media", 0, "average weekly hours"),
    "03": ("ganho_hora", "media", 0, "average hourly earnings, US$"),
    "04": ("overtime_semana", "media", 0, "average weekly overtime hours"),
    "11": ("ganho_semana", "media", 0, "average weekly earnings, US$"),
    "12": ("ganho_semana_real", "media", 0, "average weekly earnings, 1982-84 US$"),
    "13": ("ganho_hora_real", "media", 0, "average hourly earnings, 1982-84 US$"),
    "15": ("ganho_hora_ex_ot", "media", 0, "average hourly earnings excl. overtime, US$"),
    "16": ("idx_horas", "indice", 0, "index of aggregate weekly hours, 2007=100"),
    "17": ("idx_folha", "indice", 0, "index of aggregate weekly payrolls, 2007=100"),
    "56": ("horas_agreg", "agregado", 1, "aggregate weekly hours, thousands"),
    "57": ("folha_agreg", "agregado", 1, "aggregate weekly payrolls, thousands of US$"),
    "58": ("overtime_agreg", "agregado", 1, "aggregate weekly overtime hours, thousands"),
}
_FAMILIAS = (".Employment", ".AllEmployeeHoursAndEarnings")

# Conferencia contra a API: as series de manchete do release, mais uma de cada
# familia de medida. Se o arquivo e a API discordarem, a carga levanta.
_CONFERENCIA = [
    "CES0000000001",   # total nonfarm, emprego, SA
    "CES0500000001",   # total private, emprego, SA
    "CES9000000001",   # government, emprego, SA
    "CES0500000002",   # total private, horas semanais
    "CES0500000003",   # total private, ganho medio/hora
    "CES0500000011",   # total private, ganho medio/semana
    "CES0500000013",   # total private, ganho/hora em US$ de 1982-84
    "CES0500000016",   # total private, indice de horas agregadas
    "CES0500000017",   # total private, indice de folha agregada
    "CEU0000000001",   # total nonfarm, emprego, NSA
]
_ANOS_PADRAO = 4


def _ler_arquivos(bls: BLS, desde: int | None) -> pd.DataFrame:
    """As 13 medidas dos 30 arquivos, ja em formato longo."""
    arqs = [a for a in bls.list_flat_files("ce") if a.endswith(_FAMILIAS)]
    if len(arqs) < 25:
        raise RuntimeError(
            f"so {len(arqs)} arquivos de dados da CES foram listados (esperado ~30). "
            "O layout do diretorio mudou -- confira em "
            "https://download.bls.gov/pub/time.series/ce/ antes de gravar parcial."
        )
    partes = []
    for nome in arqs:
        df = bls.read_flat_table("ce", nome)
        df.columns = [c.strip() for c in df.columns]
        df["series_id"] = df["series_id"].astype(str).str.strip()
        df["dt"] = df["series_id"].str[11:13]
        df = df[df["dt"].isin(_MEDIDAS)]
        df["period"] = df["period"].astype(str).str.strip()
        df = df[df["period"].str.match(r"^M(0[1-9]|1[0-2])$")]   # M13 = media anual
        df["year"] = df["year"].astype(int)
        if desde is not None:
            df = df[df["year"] >= desde]
        if not df.empty:
            partes.append(df[["series_id", "year", "period", "value",
                              "footnote_codes", "dt"]])
        print(f"    {nome[8:]:56s} {len(df):8,}")
    if not partes:
        raise RuntimeError("nenhuma linha da CES sobreviveu ao filtro -- nada a gravar")
    return pd.concat(partes, ignore_index=True)


def _longo(bruto: pd.DataFrame, categorias: set[str]) -> pd.DataFrame:
    d = pd.DataFrame({
        "date": pd.to_datetime(bruto["year"].astype(str) + "-"
                               + bruto["period"].str[1:] + "-01"),
        "categoria": bruto["series_id"].str[3:11],
        "series_id": bruto["series_id"],
        "ajuste": bruto["series_id"].str[2].map({"S": "sa", "U": "nsa"}),
        "valor": pd.to_numeric(bruto["value"], errors="coerce"),
        "preliminar": bruto["footnote_codes"].astype(str).str.contains("P").astype(int),
    })
    med = bruto["dt"].map(lambda k: _MEDIDAS[k])
    d["medida"] = [m[0] for m in med]
    d["natureza"] = [m[1] for m in med]
    d["aditivo"] = [m[2] for m in med]

    if d["ajuste"].isna().any():
        ruins = bruto.loc[d["ajuste"].isna(), "series_id"].unique()[:5]
        raise RuntimeError(
            f"series_id da CES com terceiro caractere fora de S/U: {list(ruins)}. "
            "O prefixo CES/CEU e o unico lugar em que o ajuste sazonal aparece."
        )

    fora = set(d["categoria"]) - categorias
    if fora:
        raise RuntimeError(
            f"{len(fora)} industrias nos dados que nao estao em ce.industry: "
            f"{sorted(fora)[:8]}. A dimensao e os dados sairiam de sincronia."
        )
    d = d.dropna(subset=["valor"])
    dup = d.duplicated(subset=["date", "categoria", "medida", "ajuste"]).sum()
    if dup:
        raise RuntimeError(f"{dup} linhas duplicadas na chave (date, categoria, medida, ajuste)")
    return d


def _conferir_api(bls: BLS, dados: pd.DataFrame) -> None:
    """O arquivo bate com a API nas series de manchete?"""
    ult = dados["date"].max()
    ano = int(ult.year)
    api = bls.get_series(_CONFERENCIA, start_year=ano - 1, end_year=ano)
    if api.empty:
        print("  aviso: a API nao devolveu nada -- conferencia de vintage nao feita")
        return
    api = api.rename(columns={"value": "api"})[["series_id", "date", "api"]]
    api["date"] = pd.to_datetime(api["date"])
    arq = dados[dados["series_id"].isin(_CONFERENCIA)][["series_id", "date", "valor"]]
    j = api.merge(arq, on=["series_id", "date"], how="inner")
    if j.empty:
        raise RuntimeError(
            "nenhum mes em comum entre o arquivo e a API nas series de conferencia -- "
            "o arquivo pode estar de uma safra antiga."
        )
    dif = (j["api"] - j["valor"]).abs()
    if (dif > 0.051).any():
        pior = j.loc[dif.idxmax()]
        raise RuntimeError(
            f"arquivo e API discordam em {int((dif > 0.051).sum())} de {len(j)} "
            f"celulas conferidas; pior caso {pior.series_id} em "
            f"{pior['date'].date()}: arquivo {pior.valor} x API {pior.api}."
        )
    # A API nao pode estar A FRENTE do arquivo: seria arquivo velho.
    fim_api = api.groupby("series_id")["date"].max()
    fim_arq = arq.groupby("series_id")["date"].max()
    atras = [s for s in fim_api.index if s in fim_arq and fim_arq[s] < fim_api[s]]
    if atras:
        raise RuntimeError(
            f"o arquivo esta atras da API em {len(atras)} series (ex.: {atras[0]}, "
            f"arquivo {fim_arq[atras[0]].date()} x API {fim_api[atras[0]].date()}). "
            "Rode de novo mais tarde -- os arquivos do FTP saem depois da API."
        )
    print(f"  conferencia: {len(j)} celulas batem com a API "
          f"({j['series_id'].nunique()} series, dif max {dif.max():.3f})")


def run(anos: int | str | None = None) -> pd.DataFrame:
    """Carrega a CES.

    Args:
        anos: `None` (default) traz os ultimos 4 anos -- o suficiente para cobrir a
              revisao anual do benchmark, que reescreve os 5 anos mais recentes.
              `"all"` traz o historico inteiro (1939->, ~3,4 M linhas, dezenas de
              minutos). Um inteiro traz os ultimos N anos.

    Returns:
        As linhas gravadas.
    """
    bls = BLS()
    print(f"{_TABLE}: montando a arvore antes dos dados")
    dim = mt_ces_dim.run()

    if anos == "all":
        desde = None
    else:
        n = _ANOS_PADRAO if anos is None else int(anos)
        desde = pd.Timestamp.today().year - n + 1
    print(f"  lendo os arquivos da CES ({'historico completo' if desde is None else f'de {desde}'})")
    bruto = _ler_arquivos(bls, desde)
    dados = _longo(bruto, set(dim["categoria"]))
    print(f"  {len(dados):,} linhas, {dados['series_id'].nunique():,} series, "
          f"{dados['date'].min().date()} -> {dados['date'].max().date()}")
    for med, n in dados.groupby("medida").size().sort_values(ascending=False).items():
        print(f"    {med:20s} {n:9,}")
    _conferir_api(bls, dados)

    cols = ["date", "categoria", "medida", "ajuste", "valor", "natureza",
            "aditivo", "preliminar", "series_id"]
    saida = dados[cols].sort_values(["date", "categoria", "medida", "ajuste"])
    gravar(_DATABASE, _TABLE, saida, sonda="categoria")
    return saida


if __name__ == "__main__":
    run()
