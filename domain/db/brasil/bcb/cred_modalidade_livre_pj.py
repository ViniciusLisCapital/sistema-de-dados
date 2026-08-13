"""
Crédito do sistema financeiro — recursos livres, por modalidade, Pessoa Jurídica (BCB/SGS)

Series SGS coletadas, por metrica x modalidade -- Tabelas 6, 10, 15, 19 da publicacao mensal
do BCB "Tabelas de Estatisticas Monetarias e de Credito" (ver
analytics/credit/fontes_dados.md para o mapeamento completo). A coluna "Total" de cada
tabela-fonte foi deliberadamente excluida daqui -- ja existe em macro_brasil.cred_credito_resumo
sob outro nome (ex: esta tabela nao repete o que cred_credito_resumo ja cobre).

Algumas celulas da planilha-fonte nao tem codigo SGS proprio (mostram "-" em vez de um
numero) -- confirmado ao vivo, nao e erro de extracao. Omitidas dos dicionarios abaixo,
nao inseridas com NULL.

Metricas coletadas:
  saldo -- Tabela 6 (24 modalidades)
  concessao -- Tabela 10 (22 modalidades)
  taxa_media -- Tabela 15 (22 modalidades)
  inadimplencia -- Tabela 19 (21 modalidades)

Banco: macro_brasil.cred_modalidade_livre_pj -- PRIMARY KEY (date, modalidade, metrica)
DDL:
  CREATE TABLE macro_brasil.cred_modalidade_livre_pj (
      date       DATE          NOT NULL,
      modalidade VARCHAR(100)  NOT NULL,
      metrica    VARCHAR(30)   NOT NULL,
      value      DECIMAL(15,5),
      PRIMARY KEY (date, modalidade, metrica)
  ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
"""

import pandas as pd

from connectors.bcb import BCB
from connectors.mysql import insert_data_into_database

_DATABASE = "macro_brasil"
_TABLE    = "cred_modalidade_livre_pj"

_CODES_SALDO = {
    "acc": 20565,
    "antecipacao_de_faturas_de_cartao": 20546,
    "aquisicao_de_outros_bens": 20554,
    "aquisicao_de_veiculos": 20553,
    "arrendamento_mercantil_outros_bens": 20557,
    "arrendamento_mercantil_veiculos": 20556,
    "capital_de_giro_prazo_maior_365_dias": 20548,
    "capital_de_giro_prazo_menor_365_dias": 20547,
    "capital_de_giro_teto_rotativo": 20549,
    "capital_de_giro_total": 20550,
    "cartao_de_credito_a_vista": 20563,
    "cartao_de_credito_parcelado": 20562,
    "cartao_de_credito_rotativo": 20561,
    "cartao_de_credito_total": 20564,
    "cheque_especial": 20552,
    "compror": 20560,
    "conta_garantida": 20551,
    "desconto_de_cheques": 20545,
    "desconto_de_duplicatas_e_recebiveis": 20544,
    "financiamento_exportacoes": 20567,
    "financiamento_importacoes": 20566,
    "outros": 20569,
    "repasse_externo": 20568,
    "vendor": 20559,
}

_CODES_CONCESSAO = {
    "acc": 20657,
    "antecipacao_de_faturas_de_cartao": 20638,
    "aquisicao_de_outros_bens": 20646,
    "aquisicao_de_veiculos": 20645,
    "arrendamento_mercantil_outros_bens": 20649,
    "arrendamento_mercantil_veiculos": 20648,
    "capital_de_giro_prazo_maior_365_dias": 20640,
    "capital_de_giro_prazo_menor_365_dias": 20639,
    "capital_de_giro_teto_rotativo": 20641,
    "capital_de_giro_total": 20642,
    "cartao_de_credito_a_vista": 20655,
    "cartao_de_credito_total": 20656,
    "cheque_especial": 20644,
    "compror": 20652,
    "conta_garantida": 20643,
    "desconto_de_cheques": 20637,
    "desconto_de_duplicatas_e_recebiveis": 20636,
    "financiamento_exportacoes": 20659,
    "financiamento_importacoes": 20658,
    "outros": 20661,
    "repasse_externo": 20660,
    "vendor": 20651,
}

_CODES_TAXA_MEDIA = {
    "acc": 20736,
    "antecipacao_de_faturas_de_cartao": 20721,
    "aquisicao_de_outros_bens": 20729,
    "aquisicao_de_veiculos": 20728,
    "arrendamento_mercantil_outros_bens": 20732,
    "arrendamento_mercantil_veiculos": 20731,
    "capital_de_giro_prazo_maior_365_dias": 20723,
    "capital_de_giro_prazo_menor_365_dias": 20722,
    "capital_de_giro_teto_rotativo": 20724,
    "capital_de_giro_total": 20725,
    "cartao_de_credito_parcelado": 22020,
    "cartao_de_credito_rotativo": 22019,
    "cartao_de_credito_total": 22021,
    "cheque_especial": 20727,
    "compror": 20735,
    "conta_garantida": 20726,
    "desconto_de_cheques": 20720,
    "desconto_de_duplicatas_e_recebiveis": 20719,
    "financiamento_exportacoes": 20738,
    "financiamento_importacoes": 20737,
    "repasse_externo": 20739,
    "vendor": 20734,
}

_CODES_INADIMPLENCIA = {
    "acc": 21107,
    "antecipacao_de_faturas_de_cartao": 21089,
    "aquisicao_de_outros_bens": 21097,
    "aquisicao_de_veiculos": 21096,
    "arrendamento_mercantil_outros_bens": 21100,
    "arrendamento_mercantil_veiculos": 21099,
    "capital_de_giro_prazo_maior_365_dias": 21091,
    "capital_de_giro_prazo_menor_365_dias": 21090,
    "capital_de_giro_teto_rotativo": 21092,
    "capital_de_giro_total": 21093,
    "cartao_de_credito": 21106,
    "cheque_especial": 21095,
    "compror": 21103,
    "conta_garantida": 21094,
    "desconto_de_cheques": 21088,
    "desconto_de_duplicatas_e_recebiveis": 21087,
    "financiamento_exportacoes": 21109,
    "financiamento_importacoes": 21108,
    "outros": 21111,
    "repasse_externo": 21110,
    "vendor": 21102,
}

_bcb = BCB()


def _fetch_metrica(metrica: str, codes: dict, start: str | None, end: str | None, n_meses: int) -> pd.DataFrame:
    if start:
        df = _bcb.get_sgs(codes, start=start, end=end)
    else:
        df = _bcb.get_sgs_ultimos(codes, n=n_meses)
    df = df.rename(columns={"name": "modalidade"})
    df["metrica"] = metrica
    return df[["date", "modalidade", "metrica", "value"]]


def run(n_meses: int = 24, start: str | None = None, end: str | None = None) -> None:
    """Atualiza macro_brasil.cred_modalidade_livre_pj.

    Args:
        n_meses: ultimos N meses (default 24). Ignorado se start/end fornecidos.
        start:   data inicial no formato "DD/MM/YYYY", ou "all" para serie completa.
        end:     data final no formato "DD/MM/YYYY". Default: hoje.
    """
    frames = [
        _fetch_metrica("saldo", _CODES_SALDO, start, end, n_meses),
        _fetch_metrica("concessao", _CODES_CONCESSAO, start, end, n_meses),
        _fetch_metrica("taxa_media", _CODES_TAXA_MEDIA, start, end, n_meses),
        _fetch_metrica("inadimplencia", _CODES_INADIMPLENCIA, start, end, n_meses),
    ]
    df = pd.concat(frames, ignore_index=True)
    insert_data_into_database(_DATABASE, _TABLE, df)
