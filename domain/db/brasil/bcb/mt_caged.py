"""
Novo CAGED - Cadastro Geral de Empregados e Desempregados (via BCB SGS)

Series SGS coletadas (14 series): **ESTOQUE de empregos formais celetistas**
(nivel, em pessoas), total e por setor de atividade economica -- NAO o saldo
(admissoes menos desligamentos), apesar do que a docstring deste modulo dizia
ate 2026-08. Confirmado ao vivo contra a API do SGS: a serie 28763
(`caged_total`) marca 48.032.308 em 2026-06, ordem de grandeza de um estoque
nacional de vinculos, nao de um fluxo mensal (que roda na casa das centenas de
milhares -- o saldo real de 2026-06 foi 145.161, ver `domain/db/brasil/mte/`).

O saldo/admissoes/desligamentos vem do microdado do FTP do PDET/MTE, em
`mt_caged_setor`/`mt_caged_uf`/`mt_caged_salario` -- e a DIFERENCA MENSAL desta
serie de estoque reproduz aproximadamente aquele saldo (e o que
`analytics/oraculo/brasil/scores.py` ja faz, corretamente, com `diff_1m`).

Taxonomia setorial propria do BCB, que NAO e a das 22 secoes CNAE 2.0 do
microdado -- e uma arvore de 3 niveis com agregados intermediarios, validada ao
vivo (2026-08) somando as partes:
  Total = Agropecuaria + Ind. extrativa + Ind. transformacao + SIUP
          + Construcao + Comercio + Servicos          (fecha em ~4 vinculos)
  SIUP  = Eletricidade e gas + Agua/esgoto/residuos    (fecha exato)
  Servicos > Transporte/Alojamento/Informacao/Financeiras (subconjunto
          publicado, NAO soma o total de Servicos -- ha subsetores sem codigo
          SGS proprio)

Cobertura 1992-01 -> hoje: e a unica serie longa de emprego formal do projeto
(o microdado do Novo CAGED so comeca em 2020-01).

Banco: macro_brasil.mt_caged
Consumidores: analytics/oraculo/brasil/scores.py, analytics/brasil/labor_market/
"""

from connectors.bcb import BCB
from connectors.mysql import insert_data_into_database

_DATABASE = "macro_brasil"
_TABLE    = "mt_caged"

_SERIES = {
    "caged_total":                       28763,
    "caged_agropecuaria":                28764,
    "caged_ind_extrativa":               28765,
    "caged_ind_transformacao":           28766,
    "caged_SIUP":                        28767,
    "caged_eletricidade_gas":            28768,
    "caged_gestao_residuos":             28769,
    "caged_construcao":                  28770,
    "caged_comercio":                    28771,
    "caged_servicos":                    28772,
    "caged_transp_arm_correios":         28773,
    "caged_aloj_alimentacao":            28774,
    "caged_informacao_comunicacao":      28775,
    "caged_ativ_financeiras_seguros":    28776,
}

_bcb = BCB()


def run(n_meses: int = 24, start: str | None = None, end: str | None = None) -> None:
    """Atualiza macro_brasil.mt_caged.

    Args:
        n_meses: ultimos N meses (default 24). Ignorado se start/end fornecidos.
        start:   data inicial no formato "DD/MM/YYYY", ou "all" para serie completa.
        end:     data final no formato "DD/MM/YYYY". Default: hoje.
    """
    if start:
        df = _bcb.get_sgs(_SERIES, start=start, end=end)
    else:
        df = _bcb.get_sgs_ultimos(_SERIES, n=n_meses)

    insert_data_into_database(_DATABASE, _TABLE, df)
