"""
Atualiza o banco de dados brasil com os dados mais recentes de todas as fontes.

Uso:
    .venv\\Scripts\\python jobs\\update_db.py

Cada script e independente: se um falhar, os demais continuam.
Exit code 1 se houver qualquer falha.
"""

import logging
import sys
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("update_db")

# IBGE
from domain.db.brasil.ibge import (
    atv_pib, atv_pib_valores_correntes, atv_pib_taxas, atv_pim, atv_pim_uso, atv_pmc, atv_pms,
    mt_pnad, mt_pnad_trimestral, inflc_decomposicao, inflc_dim,
)

# BCB
from domain.db.brasil.bcb import (
    atv_ibcbr, atv_pib_usd, atv_pib_mensal, mt_caged, cred_credito_amplo, cred_credito_familias,
    cred_credito_resumo, cred_inadimplencia_pj, cred_modalidade_livre_pj,
    cred_modalidade_livre_pf, cred_modalidade_direcionado_pj, cred_modalidade_direcionado_pf,
    cred_credito_porte, cred_credito_atividade_economica, cred_credito_tipo_cliente,
    cred_credito_controle_capital, cred_ptc, expc_focus, inflc_agregados,
    cmb_cambio_contratado, cmb_reservas_bc, cmb_balanco_pagmt, cmb_fluxo_cambial, cmb_ptax,
    fisc_divida, fisc_nfsp,
)

# IPEA
from domain.db.brasil.ipea import cmb_termos_troca

# MDIC
from domain.db.brasil.mdic import cmb_comex_fator_agregado, cmb_comex_pais, cmb_comex_produto

# MTE/PDET (Novo CAGED, microdado do FTP)
from domain.db.brasil.mte import mt_caged_novo

# Tesouro Nacional
from domain.db.brasil.tesouro import fisc_rtn, fisc_efgg

# ---------------------------------------------------------------------------
# Scripts e parametros de atualizacao rotineira
# ---------------------------------------------------------------------------
# Cada entrada: (label, modulo, kwargs)
# Os defaults de cada run() ja cobrem as janelas adequadas para updates diarios:
#   SGS  → ultimos N meses  (range revisao tipica de cada serie)
#   IBGE → ultimos N anos   (idem)
#   Focus → ultimos 90 dias

_SCRIPTS = [
    # IBGE
    ("IBGE · GDP / Contas Nacionais",  atv_pib,               {}),
    ("IBGE · GDP / Valores Correntes",  atv_pib_valores_correntes, {}),
    ("IBGE · GDP / Taxas Oficiais",     atv_pib_taxas,         {}),
    ("IBGE · PIM / Prod. Industrial",  atv_pim,               {}),
    ("IBGE · PIM / Categorias de Uso", atv_pim_uso,           {}),
    ("IBGE · PMC / Varejo",            atv_pmc,               {}),
    ("IBGE · PMS / Servicos",          atv_pms,               {}),
    ("IBGE · PNAD / Emprego",          mt_pnad,               {}),
    ("IBGE · PNAD Trimestral",         mt_pnad_trimestral,    {}),
    ("IBGE · IPCA Decomposicao",       inflc_decomposicao,    {}),
    ("IBGE · IPCA Dimensao",           inflc_dim,             {}),
    # BCB
    ("BCB  · IBC-Br",                  atv_ibcbr,             {}),
    ("BCB  · PIB Mensal (USD)",        atv_pib_usd,           {}),
    ("BCB  · PIB Mensal (R$)",         atv_pib_mensal,        {}),
    ("BCB  · IPCA Agregados",          inflc_agregados,       {}),
    ("BCB  · CAGED",                   mt_caged,              {}),
    ("BCB  · Credito",                 cred_credito_amplo,    {}),
    ("BCB  · Credito Resumo",           cred_credito_resumo,  {}),
    ("BCB  · Indicadores Familias",    cred_credito_familias, {}),
    ("BCB  · Inadimplencia PJ",         cred_inadimplencia_pj, {}),
    ("BCB  · Credito Modalidade Livre PJ",        cred_modalidade_livre_pj,        {}),
    ("BCB  · Credito Modalidade Livre PF",        cred_modalidade_livre_pf,        {}),
    ("BCB  · Credito Modalidade Direcionado PJ",  cred_modalidade_direcionado_pj,  {}),
    ("BCB  · Credito Modalidade Direcionado PF",  cred_modalidade_direcionado_pf,  {}),
    ("BCB  · Credito por Porte de Empresa",       cred_credito_porte,              {}),
    ("BCB  · Credito por Atividade Economica",    cred_credito_atividade_economica, {}),
    ("BCB  · Credito por Tipo de Cliente",        cred_credito_tipo_cliente,       {}),
    ("BCB  · Credito por Controle de Capital",    cred_credito_controle_capital,   {}),
    ("BCB  · Pesquisa Trimestral Condicoes Credito", cred_ptc,                     {}),
    ("BCB  · Expectativas Focus",      expc_focus,            {}),
    ("BCB  · Reservas Internacionais", cmb_reservas_bc,       {}),
    ("BCB  · Balanco de Pagamentos",   cmb_balanco_pagmt,     {}),
    ("BCB  · Fluxo Cambial",           cmb_fluxo_cambial,     {}),
    ("BCB  · Cambio Contratado",       cmb_cambio_contratado, {}),
    ("BCB  · PTAX + Volume Interbanc.", cmb_ptax,              {}),
    ("BCB  · Divida Publica",           fisc_divida,           {}),
    ("BCB  · NFSP",                     fisc_nfsp,             {}),
    ("IPEA · Termos de Troca (Funcex)", cmb_termos_troca,      {}),
    ("MDIC · Comex Stat (por pais)",    cmb_comex_pais,        {}),
    ("MDIC · Comex Stat (fator agreg.)", cmb_comex_fator_agregado, {}),
    ("MDIC · Comex Stat (produto)",     cmb_comex_produto,     {}),
    # Novo CAGED: baixa ~50MB/mes do FTP do PDET (release novo ~4 semanas apos o
    # fim do mes). Alimenta as 3 tabelas de corte num unico passe -- ver
    # domain/db/brasil/mte/mt_caged_novo.py. Bem mais lento que os scripts de API
    # acima (minutos, nao segundos), por isso fica no fim da lista.
    ("MTE  · Novo CAGED (setor/UF/salario)", mt_caged_novo,    {}),
    ("Tesouro · RTN",                   fisc_rtn,              {}),
    ("Tesouro · EFGG",                   fisc_efgg,             {}),
]


def main() -> None:
    inicio = datetime.now()
    erros: list[tuple[str, str]] = []

    logger.info("Iniciando atualizacao — %d scripts", len(_SCRIPTS))

    for label, mod, kwargs in _SCRIPTS:
        try:
            logger.info("%-40s ...", label)
            mod.run(**kwargs)
            logger.info("%-40s OK", label)
        except Exception as exc:
            logger.error("%-40s FALHOU: %s", label, exc)
            erros.append((label, str(exc)))

    elapsed = (datetime.now() - inicio).seconds
    n_ok = len(_SCRIPTS) - len(erros)
    logger.info("Concluido em %ds — %d/%d OK", elapsed, n_ok, len(_SCRIPTS))

    if erros:
        logger.error("%d script(s) falharam:", len(erros))
        for label, err in erros:
            logger.error("  - %s: %s", label, err)
        sys.exit(1)


if __name__ == "__main__":
    main()
