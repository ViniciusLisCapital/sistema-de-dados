"""
Balanca comercial (bens) por categoria de Fator Agregado — Comex Stat (MDIC).

Metodologia de "comercio geral" (SISCOMEX), NAO BPM6 (mesma ressalva de
cmb_comex_pais.py / connectors/comexstat.py — nao reconciliar linha a linha
com `cmb_balanco_pagmt.mercadorias_gerais`).

Objetivo: quebra classica brasileira de comercio exterior por "Fator
Agregado" (Basicos/Semimanufaturados/Manufaturados) — pedido do usuario
apos a quebra por pais parceiro (cmb_comex_pais.py). Confirmado que essa
classificacao NAO esta disponivel na API ao vivo do Comex Stat, apenas via
join local contra a tabela de correlacao NCM.csv do download em massa — ver
connectors/comexstat_bulk.py.

Categorias (6 codigos oficiais, ver NCM_FAT_AGREG.csv, agrupados em 4 series
para manter o chart legivel — "demais" e' residual, nao aproximacao):
  basicos_export / basicos_import
  semimanufaturados_export / semimanufaturados_import
  manufaturados_export / manufaturados_import
  demais_export / demais_import   (= transacoes_especiais + consumo_bordo +
                                     reexportacao + NCMs sem correspondencia
                                     na tabela de correlacao — residual
                                     pequeno, <0.05% do total em 2025)

Diferente de cmb_comex_pais (que precisa de "mundo" + parceiros porque so 4
paises sao rastreados, nao os ~200), aqui as 4 series JA cobrem 100% do
total — toda transacao cai em exatamente 1 das 6 categorias oficiais, entao
basicos + semimanufaturados + manufaturados + demais = total mundial, sem
precisar de uma serie "mundo" separada.

SO existe fonte bulk para esta quebra (a API ao vivo nao expoe Fator
Agregado) — diferente de cmb_comex_pais.py, nao ha uma versao "via API" de
run(). `run()` (chamada por jobs/update_db.py) e' so um wrapper fino sobre
`backfill()` com uma janela curta (ultimos 2 anos, default) — sem rate
limit (e' so um download de arquivo estatico por ano), entao nao ha razao
para uma janela de update tao curta quanto a de cmb_comex_pais.run() (que
precisa ser curta por causa do rate limit da API). `backfill(start_year=1997)`
e' para a carga historica completa (uso manual, uma vez).

Cobertura: 1997-01 -> hoje (limite da propria fonte). Valores em USD FOB,
NAO convertidos (conversao para USD Bi acontece em generate_report.py).

Banco: macro_brasil.cmb_comex_fator_agregado — PRIMARY KEY (date, name)
"""

import pandas as pd

from connectors import comexstat_bulk
from connectors.mysql import insert_data_into_database

_DATABASE = "macro_brasil"
_TABLE    = "cmb_comex_fator_agregado"

# Agrupamento dos 6 codigos oficiais em 4 series de consumo.
_CATEGORIA_PARA_SERIE = {
    "basicos":              "basicos",
    "semimanufaturados":    "semimanufaturados",
    "manufaturados":        "manufaturados",
    "transacoes_especiais": "demais",
    "consumo_bordo":        "demais",
    "reexportacao":         "demais",
    "nao_classificado":     "demais",
}


def backfill(start_year: int = 1997, end_year: int | None = None) -> None:
    """Atualiza macro_brasil.cmb_comex_fator_agregado via download em massa.

    Sem rate limit (arquivo estatico) — usar tanto para a carga historica
    completa quanto para updates rotineiros (ex: `backfill(start_year=2025)`
    para so re-processar os ultimos ~2 anos). Insere incrementalmente por
    (ano, flow) — uma falha no meio nao descarta o que ja foi buscado.

    Args:
        start_year: ano inicial (default 1997, inicio da serie na fonte).
        end_year:   ano final (default: ano corrente).
    """
    if end_year is None:
        end_year = pd.Timestamp.today().year

    for year in range(start_year, end_year + 1):
        for flow in ["export", "import"]:
            print(f"  Comex Stat (Fator Agregado) bulk: {flow} {year}...")
            agg = comexstat_bulk.get_year_by_fator_agregado(flow, year)
            if agg.empty:
                print(f"    (sem dados para {flow} {year} — pulando)")
                continue

            agg["name"] = agg["categoria"].map(_CATEGORIA_PARA_SERIE) + f"_{flow}"
            out = agg.groupby(["month", "name"], as_index=False)["value_usd"].sum()
            out["date"] = pd.to_datetime(str(year) + "-" + out["month"] + "-01")
            out = out[["date", "name", "value_usd"]].rename(columns={"value_usd": "value"})

            insert_data_into_database(_DATABASE, _TABLE, out)


def run(start_year: int | None = None, end_year: int | None = None) -> None:
    """Atualiza macro_brasil.cmb_comex_fator_agregado (update rotineiro).

    Wrapper fino sobre backfill() — sem rate limit (fonte e' sempre bulk),
    entao o unico motivo para nao usar start_year=1997 sempre e' evitar
    trabalho desnecessario (60 downloads a cada execucao de
    jobs/update_db.py). Default: ultimos 2 anos civis (cobre revisoes do
    ano anterior + o ano corrente).

    Args:
        start_year: default ano_corrente - 1.
        end_year:   default ano corrente.
    """
    if start_year is None:
        start_year = pd.Timestamp.today().year - 1
    backfill(start_year=start_year, end_year=end_year)
