"""
Balanca comercial (bens) por pais parceiro — Comex Stat (MDIC).

Metodologia de "comercio geral" (SISCOMEX), NAO BPM6 (ver docstring de
connectors/comexstat.py para a diferenca em relacao a
`cmb_balanco_pagmt.mercadorias_gerais` — por isso os totais desta tabela sao
um recorte proprio/consistente entre si, e nao devem ser somados/
reconciliados linha a linha com a BOP).

Objetivo: preencher a lacuna documentada em `cmb_balanco_pagmt.py` — o BCB
SGS nao tem quebra por pais/bloco parceiro dentro do detalhamento BPM6,
apenas Mercadorias em Geral / Ouro Nao Monetario / Merchanting (agregado).

Parceiros escolhidos (2026-07): os 4 maiores por comercio total (export +
import) em 2025 — China, Estados Unidos, Argentina, Alemanha (juntos ~70%
do comercio de bens do Brasil) — mais o total mundial, que permite calcular
"Demais Paises" como residual (mundo - soma dos 4) na camada de consumo
(analytics/brasil/exchange_rate/generate_report.py), sem precisar buscar todos os ~200
parceiros individualmente.

Series (export/import separados; saldo por parceiro calculado no relatorio):
  china_export / china_import
  eua_export / eua_import
  argentina_export / argentina_import
  alemanha_export / alemanha_import
  mundo_export / mundo_import   (total, sem filtro de pais — usado para o residual "Demais Paises")

Codigos de pais no Comex Stat (API e bulk usam o MESMO codigo, confirmado
contra balanca.mdic.gov.br/balanca/bd/tabelas/PAIS.csv):
  China = 160, Estados Unidos = 249, Argentina = 063, Alemanha = 023

Cobertura: 1997-01 -> hoje (limite da propria fonte). Valores em USD FOB,
NAO convertidos (conversao para USD Bi acontece em generate_report.py, como
as demais tabelas de cambio).

DUAS fontes, dois casos de uso (2026-07-14 — pedido do usuario apos a API ao
vivo travar num rate limit persistente durante o backfill historico):
  - `backfill()`: download em massa (connectors/comexstat_bulk.py, arquivos
    anuais estaticos de balanca.mdic.gov.br) — SEM rate limit. Uso:
    carga historica completa, uma vez (ou reprocessamento, ex: parceiro
    novo adicionado). Insere por (ano, flow) incrementalmente — uma falha
    no meio nao descarta o que ja foi buscado.
  - `run()`: update rotineiro, tambem pelo download em massa (ultimos 2 anos).
    A API ao vivo (connectors/comexstat.py) saiu da rotina em 2026-10-22: 429
    persistente mesmo com uma chamada por vez.

Banco: macro_brasil.cmb_comex_pais — PRIMARY KEY (date, name)
"""

import pandas as pd

from connectors import comexstat_bulk
from connectors.mysql import insert_data_into_database

_DATABASE = "macro_brasil"
_TABLE    = "cmb_comex_pais"

_PAISES = {
    "china":     "160",
    "eua":       "249",
    "argentina": "063",
    "alemanha":  "023",
}

def backfill(start_year: int = 1997, end_year: int | None = None) -> None:
    """Carga historica completa via download em massa (SEM rate limit).

    Uso recomendado: rodar uma vez (ou ao adicionar/trocar um parceiro).
    Para updates rotineiros, usar run() (ultimos 2 anos, tambem em massa).

    Args:
        start_year: ano inicial (default 1997, inicio da serie na fonte).
        end_year:   ano final (default: ano corrente).
    """
    if end_year is None:
        end_year = pd.Timestamp.today().year

    for year in range(start_year, end_year + 1):
        for flow in ["export", "import"]:
            print(f"  Comex Stat bulk: {flow} {year}...")
            agg = comexstat_bulk.get_year(flow, year)
            if agg.empty:
                print(f"    (sem dados para {flow} {year} — pulando)")
                continue

            mundo = agg.groupby("month", as_index=False)["value_usd"].sum()
            mundo["name"] = f"mundo_{flow}"

            frames = [mundo]
            for nome, codigo in _PAISES.items():
                sub = agg.loc[agg["co_pais"] == codigo, ["month", "value_usd"]].copy()
                sub["name"] = f"{nome}_{flow}"
                frames.append(sub)

            out = pd.concat(frames, ignore_index=True)
            out["date"] = pd.to_datetime(str(year) + "-" + out["month"] + "-01")
            out = out[["date", "name", "value_usd"]].rename(columns={"value_usd": "value"})

            insert_data_into_database(_DATABASE, _TABLE, out)


def run(start_year: int | None = None, end_year: int | None = None) -> None:
    """Atualiza macro_brasil.cmb_comex_pais (update rotineiro).

    Wrapper fino sobre backfill() — default: ultimos 2 anos civis (cobre
    revisoes do ano anterior + o ano corrente), pelos arquivos em massa, sem
    rate limit. Desde 2026-10-22 NAO usa a API ao vivo: ela devolvia 429 mesmo
    com uma chamada por vez, e o update fazia ~40 chamadas.
    """
    if start_year is None:
        start_year = pd.Timestamp.today().year - 1
    backfill(start_year=start_year, end_year=end_year)
