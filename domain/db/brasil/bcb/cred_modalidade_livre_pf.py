"""
Crédito do sistema financeiro — recursos livres, por modalidade, Pessoa Física (BCB/SGS)

Series SGS coletadas, por metrica x modalidade -- Tabelas 7, 11, 16, 20 da publicacao mensal
do BCB "Tabelas de Estatisticas Monetarias e de Credito" (ver
analytics/brasil/credit/fontes_dados.md para o mapeamento completo). A coluna "Total" de cada
tabela-fonte foi deliberadamente excluida daqui -- ja existe em macro_brasil.cred_credito_resumo
sob outro nome (ex: esta tabela nao repete o que cred_credito_resumo ja cobre).

Algumas celulas da planilha-fonte nao tem codigo SGS proprio (mostram "-" em vez de um
numero) -- confirmado ao vivo, nao e erro de extracao. Omitidas dos dicionarios abaixo,
nao inseridas com NULL.

Metricas coletadas:
  saldo -- Tabela 7 (21 modalidades)
  concessao -- Tabela 11 (21 modalidades)
  taxa_media -- Tabela 16 (17 modalidades)
  inadimplencia -- Tabela 20 (18 modalidades)

Banco: macro_brasil.cred_modalidade_livre_pf -- PRIMARY KEY (date, modalidade, metrica)
DDL:
  CREATE TABLE macro_brasil.cred_modalidade_livre_pf (
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
_TABLE    = "cred_modalidade_livre_pf"

_CODES_SALDO = {
    "aquisicao_de_outros_bens": 20582,
    "aquisicao_de_veiculos": 20581,
    "arrendamento_mercantil_outros_bens": 20585,
    "arrendamento_mercantil_veiculos": 20584,
    "cartao_de_credito_a_vista": 20589,
    "cartao_de_credito_parcelado": 20588,
    "cartao_de_credito_rotativo": 20587,
    "cartao_de_credito_total": 20590,
    "cheque_especial": 20573,
    "composicao_de_dividas": 20575,
    "credito_pessoal_consignado_beneficiarios_do_inss": 20578,
    "credito_pessoal_consignado_servidores_publicos": 20577,
    "credito_pessoal_consignado_total": 20579,
    "credito_pessoal_consignado_trabalhadores_setor_privado": 20576,
    "credito_pessoal_nao_consignado_com_garantias": 29964,
    "credito_pessoal_nao_consignado_sem_garantias": 29965,
    "credito_pessoal_nao_consignado_total": 20574,
    "desconto_de_cheques": 20591,
    "outros": 20592,
    "total_nao_rotativo": 20571,
    "total_rotativo": 20572,
}

_CODES_CONCESSAO = {
    "aquisicao_de_outros_bens": 20674,
    "aquisicao_de_veiculos": 20673,
    "arrendamento_mercantil_outros_bens": 20677,
    "arrendamento_mercantil_veiculos": 20676,
    "cartao_de_credito_a_vista": 20681,
    "cartao_de_credito_parcelado": 20680,
    "cartao_de_credito_rotativo": 20679,
    "cartao_de_credito_total": 20682,
    "cheque_especial": 20665,
    "composicao_de_dividas": 20667,
    "credito_pessoal_consignado_beneficiarios_do_inss": 20670,
    "credito_pessoal_consignado_servidores_publicos": 20669,
    "credito_pessoal_consignado_total": 20671,
    "credito_pessoal_consignado_trabalhadores_setor_privado": 20668,
    "credito_pessoal_nao_consignado_com_garantias": 29967,
    "credito_pessoal_nao_consignado_sem_garantias": 29968,
    "credito_pessoal_nao_consignado_total": 20666,
    "desconto_de_cheques": 20683,
    "outros": 20684,
    "total_nao_rotativo": 20663,
    "total_rotativo": 20664,
}

_CODES_TAXA_MEDIA = {
    "aquisicao_de_outros_bens": 20750,
    "aquisicao_de_veiculos": 20749,
    "arrendamento_mercantil_outros_bens": 20753,
    "arrendamento_mercantil_veiculos": 20752,
    "cartao_de_credito_parcelado": 22023,
    "cartao_de_credito_rotativo": 22022,
    "cartao_de_credito_total": 22024,
    "cheque_especial": 20741,
    "composicao_de_dividas": 20743,
    "credito_pessoal_consignado_beneficiarios_do_inss": 20746,
    "credito_pessoal_consignado_servidores_publicos": 20745,
    "credito_pessoal_consignado_total": 20747,
    "credito_pessoal_consignado_trabalhadores_setor_privado": 20744,
    "credito_pessoal_nao_consignado_com_garantias": 29973,
    "credito_pessoal_nao_consignado_sem_garantias": 29974,
    "credito_pessoal_nao_consignado_total": 20742,
    "desconto_de_cheques": 20755,
}

_CODES_INADIMPLENCIA = {
    "aquisicao_de_outros_bens": 21122,
    "aquisicao_de_veiculos": 21121,
    "arrendamento_mercantil_outros_bens": 21125,
    "arrendamento_mercantil_veiculos": 21124,
    "cartao_de_credito_parcelado": 21128,
    "cartao_de_credito_rotativo": 21127,
    "cartao_de_credito_total": 21129,
    "cheque_especial": 21113,
    "composicao_de_dividas": 21115,
    "credito_pessoal_consignado_beneficiarios_do_inss": 21118,
    "credito_pessoal_consignado_servidores_publicos": 21117,
    "credito_pessoal_consignado_total": 21119,
    "credito_pessoal_consignado_trabalhadores_setor_privado": 21116,
    "credito_pessoal_nao_consignado_com_garantias": 29991,
    "credito_pessoal_nao_consignado_sem_garantias": 29992,
    "credito_pessoal_nao_consignado_total": 21114,
    "desconto_de_cheques": 21130,
    "outros": 21131,
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
    """Atualiza macro_brasil.cred_modalidade_livre_pf.

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
