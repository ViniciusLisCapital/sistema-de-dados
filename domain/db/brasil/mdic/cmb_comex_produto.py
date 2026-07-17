"""
Balanca comercial (bens) por produto especifico — Comex Stat (MDIC).

Metodologia de "comercio geral" (SISCOMEX), NAO BPM6 (mesma ressalva de
cmb_comex_pais.py / cmb_comex_fator_agregado.py — nao reconciliar linha a
linha com `cmb_balanco_pagmt.mercadorias_gerais`).

Objetivo: usuario pediu quebra por produto especifico (soja, petroleo) apos
ja ter a quebra por Fator Agregado (categorias amplas — Basicos/Semi/
Manufaturados, cmb_comex_fator_agregado.py) — essa nao respondia "quais
produtos", so "que tipo de produto" em sentido amplo.

Produtos escolhidos (2026-07, via pergunta ao usuario — top 5 commodities
classicas do Brasil por valor de exportacao em 2025): Petroleo, Soja,
Minerio de Ferro, Carnes, Cafe. Codigos SH (Sistema Harmonizado) — nivel de
precisao escolhido por produto (ver connectors/comexstat_bulk.py):
  soja           = SH4 1201 (Soja — ~97% do capitulo 12 "sementes
                   oleaginosas" em 2025; capitulo inteiro incluiria outras
                   sementes que nao soja)
  petroleo       = SH4 2709 (Petroleo bruto — distinto de 2710,
                   combustiveis/derivados refinados)
  minerio_ferro  = SH4 2601 (Minerios de ferro — ~83% do capitulo 26
                   "minerios, escorias e cinzas"; o capitulo tambem inclui
                   minerio de cobre etc)
  carnes         = SH2 02  (capitulo inteiro — ao contrario dos acima, carnes
                   brasileiras se dividem genuinamente entre bovina/suina/
                   aves, sem uma posicao dominante isolada)
  cafe           = SH4 0901 (Cafe — ~95% do capitulo 09 "cafe, cha, mate e
                   especiarias")

Series (export/import separados; saldo por produto calculado no relatorio):
  soja_export / soja_import
  petroleo_export / petroleo_import
  minerio_ferro_export / minerio_ferro_import
  carnes_export / carnes_import
  cafe_export / cafe_import
  mundo_export / mundo_import   (total, sem filtro de produto — usado para o
                                  residual "Demais Produtos")

SO existe fonte bulk para esta quebra (a mesma logica de
cmb_comex_fator_agregado.py: sem endpoint de produto/SH na API ao vivo do
Comex Stat) — `run()` e' um wrapper fino sobre `backfill()` com janela curta
(ultimos 2 anos, sem risco de rate limit — e' so um download de arquivo
estatico por ano).

Cobertura: 1997-01 -> hoje (limite da propria fonte). Valores em USD FOB,
NAO convertidos (conversao para USD Bi acontece em generate_report.py).

Banco: macro_brasil.cmb_comex_produto — PRIMARY KEY (date, name)
"""

import pandas as pd

from connectors import comexstat_bulk
from connectors.mysql import insert_data_into_database

_DATABASE = "macro_brasil"
_TABLE    = "cmb_comex_produto"

_PRODUTOS = {
    "soja":          "1201",
    "petroleo":      "2709",
    "minerio_ferro": "2601",
    "carnes":        "02",
    "cafe":          "0901",
}


def backfill(start_year: int = 1997, end_year: int | None = None) -> None:
    """Atualiza macro_brasil.cmb_comex_produto via download em massa.

    Sem rate limit (arquivo estatico) — usar tanto para a carga historica
    completa quanto para updates rotineiros. Insere incrementalmente por
    (ano, flow) — uma falha no meio nao descarta o que ja foi buscado.

    Args:
        start_year: ano inicial (default 1997, inicio da serie na fonte).
        end_year:   ano final (default: ano corrente).
    """
    if end_year is None:
        end_year = pd.Timestamp.today().year

    for year in range(start_year, end_year + 1):
        for flow in ["export", "import"]:
            print(f"  Comex Stat (Produto) bulk: {flow} {year}...")
            agg = comexstat_bulk.get_year_by_produto(flow, year, _PRODUTOS)
            if agg.empty:
                print(f"    (sem dados para {flow} {year} — pulando)")
                continue

            agg["name"] = agg["produto"] + f"_{flow}"
            out = agg[["month", "name", "value_usd"]].copy()
            out["date"] = pd.to_datetime(str(year) + "-" + out["month"] + "-01")
            out = out[["date", "name", "value_usd"]].rename(columns={"value_usd": "value"})

            insert_data_into_database(_DATABASE, _TABLE, out)


def run(start_year: int | None = None, end_year: int | None = None) -> None:
    """Atualiza macro_brasil.cmb_comex_produto (update rotineiro).

    Wrapper fino sobre backfill() — default: ultimos 2 anos civis (cobre
    revisoes do ano anterior + o ano corrente). Para a carga historica
    completa, usar backfill(start_year=1997) diretamente.
    """
    if start_year is None:
        start_year = pd.Timestamp.today().year - 1
    backfill(start_year=start_year, end_year=end_year)
