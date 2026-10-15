"""
IPCA e IPCA-15, indice geral: numero-indice e as variacoes que o IBGE publica.

Agregados: 1737 (IPCA, dez/1979 em diante) e 3065 (IPCA-15, mai/2000 em diante)
Variaveis:
  IPCA   : 2266 numero-indice (dez/1993 = 100), 63 mensal, 69 no ano, 2265 em 12 meses
  IPCA-15: 1117 numero-indice (dez/1993 = 100), 355 mensal, 356 no ano, 1120 em 12 meses

Schema macro_brasil.inflc_indice_geral:
  PRIMARY KEY (date, indice)

DDL:
  CREATE TABLE macro_brasil.inflc_indice_geral (
      date           DATE         NOT NULL,
      indice         VARCHAR(10)  NOT NULL COMMENT 'IPCA | IPCA15',
      numero_indice  DOUBLE       COMMENT 'Numero-indice, dez/1993 = 100',
      var_mensal     DOUBLE       COMMENT 'Variacao mensal, % (como publicada)',
      var_ano        DOUBLE       COMMENT 'Variacao acumulada no ano, %',
      var_12m        DOUBLE       COMMENT 'Variacao acumulada em 12 meses, %',
      PRIMARY KEY (date, indice)
  ) COMMENT='IBGE/SIDRA 1737 e 3065: indice geral do IPCA e do IPCA-15';

Por que existe, se inflc_agregados ja tem o headline (SGS 433/7478/13522):
  1. O SGS espelha a divulgacao do IBGE com ate um dia de atraso. No dia do IPCA
     o relatorio de inflacao tinha a decomposicao do mes novo e nenhum numero
     oficial do headline -- o 12 meses saia da reconstrucao por subitem, 0,02 p.p.
     abaixo do publicado (4,56 contra 4,58 em set/2026).
  2. So o numero-indice da o acumulado EXATO de uma janela qualquer
     (I_fim / I_inicio-1 - 1). Encadear a variacao mensal de 2 casas, ou somar as
     contribuicoes por subitem, carrega o arredondamento de cada mes. Medido contra
     o publicado desde 1995: a razao de indices bate a variacao em 12 meses em
     368 de 369 meses (IPCA) e 304 de 305 (IPCA-15) -- as duas excecoes sao a
     troca de estrutura de 2012 -- e a do ano em 368 de 369 / 309 de 309.

Uso:
    uv run python -c "from domain.db.brasil.ibge.inflc_indice_geral import run; run()"
    uv run python -c "from domain.db.brasil.ibge.inflc_indice_geral import run; run(periodos='all')"
"""

import pandas as pd

from connectors.ibge import IBGE
from connectors.mysql import insert_data_into_database

_DATABASE = "macro_brasil"
_TABLE    = "inflc_indice_geral"

# indice -> (agregado, {variavel_id: coluna})
_FONTES = {
    "IPCA":   (1737, {2266: "numero_indice", 63: "var_mensal", 69: "var_ano", 2265: "var_12m"}),
    "IPCA15": (3065, {1117: "numero_indice", 355: "var_mensal", 356: "var_ano", 1120: "var_12m"}),
}

_COLUNAS = ["date", "indice", "numero_indice", "var_mensal", "var_ano", "var_12m"]

_ibge = IBGE()


def run(periodos: str = "last:36") -> None:
    """Atualiza macro_brasil.inflc_indice_geral (IPCA e IPCA-15).

    Args:
        periodos: qualquer formato aceito pelo connector IBGE; "all" para a serie inteira.
    """
    frames = []
    for indice, (agregado, variaveis) in _FONTES.items():
        raw = _ibge.get(
            agregado=agregado,
            variaveis=list(variaveis),
            localidades={"N1": "all"},
            periodos=periodos,
        )
        if raw.empty:
            continue
        wide = (raw.assign(coluna=raw["variavel_id"].astype(int).map(variaveis))
                   .pivot_table(index="date", columns="coluna", values="value")
                   .reset_index())
        wide["indice"] = indice
        frames.append(wide.reindex(columns=_COLUNAS))

    if not frames:
        return
    insert_data_into_database(_DATABASE, _TABLE, pd.concat(frames, ignore_index=True))
