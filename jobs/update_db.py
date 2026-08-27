"""
Atualiza o banco de dados brasil com os dados mais recentes de todas as fontes.

Uso:
    uv run python jobs/update_db.py                      # passe completo (51 scripts)
    uv run python jobs/update_db.py --continuous         # so as series continuas (diarias)
    uv run python jobs/update_db.py --group ibge_ipca    # so uma divulgacao do calendario
    uv run python jobs/update_db.py --tables atv_pim,atv_pmc
    uv run python jobs/update_db.py --list               # o que existe para selecionar

Cada script e independente: se um falhar, os demais continuam.
Exit code 1 se houver qualquer falha.

Tres formas de recortar, todas resolvidas por `domain/db/registry.py` (tabela ->
script, descoberto por convencao) em vez de uma segunda lista mantida a mao:

  --continuous  as series de mercado que nao tem data de divulgacao (PTAX, DXY, Brent,
                policy rates...). Sao as que fazem sentido rodar todo dia: a lista vem
                de `no_release.continuous` no calendar YAML, nao daqui.
  --group       as tabelas de um grupo do calendario de divulgacoes. E o que o botao
                "Atualizar" do relatorio de calendario chama (via analytics/
                release_calendar/serve.py) quando uma divulgacao ja saiu.
  --tables      escape hatch para uma tabela especifica.

O passe completo (sem argumento) segue existindo e inalterado — e a rede de seguranca
que pega revisao de historico fora de qualquer evento de divulgacao.
"""

import argparse
import logging
import sys
from datetime import datetime
from types import ModuleType

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("update_db")

# IBGE
from domain.db.brasil.ibge import (
    atv_pib, atv_pib_valores_correntes, atv_pib_taxas, atv_renda_poupanca, atv_pim, atv_pim_uso,
    atv_pmc, atv_pms, mt_pnad, mt_pnad_trimestral, inflc_decomposicao, inflc_dim,
)

# BCB
from domain.db.brasil.bcb import (
    atv_ibcbr, atv_pib_usd, atv_pib_mensal, mt_caged, cred_credito_amplo, cred_credito_familias,
    cred_credito_resumo, cred_inadimplencia_pj, cred_modalidade_livre_pj,
    cred_modalidade_livre_pf, cred_modalidade_direcionado_pj, cred_modalidade_direcionado_pf,
    cred_credito_porte, cred_credito_atividade_economica, cred_credito_tipo_cliente,
    cred_credito_controle_capital, cred_ptc, inflc_agregados,
    expc_focus, expc_focus_copom, expc_focus_periodo,
    cmb_cambio_contratado, cmb_reservas_bc, cmb_balanco_pagmt, cmb_fluxo_cambial, cmb_ptax,
    fisc_divida, fisc_nfsp, fisc_dlsp_fatores,
    pm_hiato_produto, pm_hiato_produto_vintages, pm_copom_reuniao,
)

# IPEA
from domain.db.brasil.ipea import cmb_termos_troca

# MDIC
from domain.db.brasil.mdic import cmb_comex_fator_agregado, cmb_comex_pais, cmb_comex_produto

# MTE/PDET (Novo CAGED, microdado do FTP)
from domain.db.brasil.mte import mt_caged_novo

# Tesouro Nacional
from domain.db.brasil.tesouro import fisc_rtn, fisc_efgg, fisc_investimento

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
    ("IBGE · GDP / Renda e Poupanca",   atv_renda_poupanca,    {}),
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
    ("BCB  · Focus / Caminho do Copom", expc_focus_copom,      {}),
    # ~440 linhas por dia de pesquisa (contra ~50 das duas acima), entao a janela de
    # 90 dias do default ja sao ~28 mil linhas -- segundos, nao minutos, mas o mais
    # pesado dos tres. Carga historica completa (1,28 M linhas, ~11 min) e
    # run(start="all") -- rodar a mao, nao pelo passe diario.
    ("BCB  · Focus / Periodo de Ref.",  expc_focus_periodo,    {}),
    ("BCB  · Reservas Internacionais", cmb_reservas_bc,       {}),
    ("BCB  · Balanco de Pagamentos",   cmb_balanco_pagmt,     {}),
    ("BCB  · Fluxo Cambial",           cmb_fluxo_cambial,     {}),
    ("BCB  · Cambio Contratado",       cmb_cambio_contratado, {}),
    ("BCB  · PTAX + Volume Interbanc.", cmb_ptax,              {}),
    ("BCB  · Divida Publica",           fisc_divida,           {}),
    ("BCB  · NFSP",                     fisc_nfsp,             {}),
    # Tabela especial Facdetp.xlsx (fora do SGS): baixa ~2MB e regrava o historico
    # completo (~252 mil linhas) a cada execucao, porque o BCB revisa historico e a
    # planilha so existe inteira. Mais lento que os scripts de SGS acima (dezenas de
    # segundos, nao segundos) -- ver domain/db/brasil/bcb/fisc_dlsp_fatores.py.
    ("BCB  · DLSP Fatores Condicionantes", fisc_dlsp_fatores,   {}),
    # Anexo estatistico do RPM (xlsx trimestral, fora do SGS). O de vintages so
    # baixa edicao que ainda nao esta no banco -- entao custa ~20 requests de 2
    # bytes nos trimestres em que nao ha edicao nova, e ~1MB quando ha. O da serie
    # corrente baixa 1 arquivo sempre. Ver domain/db/brasil/bcb/_rpm_hiato.py.
    ("BCB  · Hiato do Produto (RPM)",   pm_hiato_produto,      {}),
    ("BCB  · Hiato do Produto / vintages", pm_hiato_produto_vintages, {}),
    # Decisao de Selic por reuniao do Copom: SGS 432 (4 requests) + a listagem de atas,
    # segundos. Entra aqui e a irma `pm_copom_projecoes` nao porque esta le so API, enquanto
    # aquela sincroniza 109 PDFs do RPM e 233 comunicados e segue sendo rodada a mao.
    ("BCB  · Copom / decisao de Selic", pm_copom_reuniao,      {}),
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
    # 78 series, uma chamada HTTP por serie (a API nao tem download em lote) mais 2
    # de verificacao da arvore -- ~80 requests, dezenas de segundos. Regrava o
    # historico completo a cada execucao, pelo mesmo motivo do RTN acima: a API so
    # distribui cada serie inteira, sem parametro de range.
    ("Tesouro · Investimento Federal",  fisc_investimento,     {}),
]


# ---------------------------------------------------------------------------
# Execucao
# ---------------------------------------------------------------------------


def _executar(plano: list[tuple[str, ModuleType, dict]]) -> list[dict]:
    """Roda um plano de (label, modulo, kwargs). Um erro nao interrompe os demais."""
    resultados: list[dict] = []
    for label, mod, kwargs in plano:
        try:
            logger.info("%-40s ...", label)
            mod.run(**kwargs)
            logger.info("%-40s OK", label)
            resultados.append({"label": label, "modulo": mod.__name__, "ok": True,
                               "erro": None})
        except Exception as exc:
            logger.error("%-40s FALHOU: %s", label, exc)
            resultados.append({"label": label, "modulo": mod.__name__, "ok": False,
                               "erro": f"{type(exc).__name__}: {exc}"})
    return resultados


def executar_tabelas(tabelas) -> dict:
    """Roda o menor conjunto de scripts que cobre `tabelas`.

    Usado pelo `--group`/`--tables` e por analytics/release_calendar/serve.py (o botao
    do relatorio). Devolve resumo estruturado — quem chama de HTTP precisa serializar,
    nao ler log. `sem_script` sai explicito: tabela que nenhum script sabe alimentar
    nao pode virar sucesso silencioso.
    """
    from domain.db.registry import carregar, scripts_para_tabelas

    plano_reg, sem_script = scripts_para_tabelas(tabelas)
    plano = []
    for dotted, tbs in plano_reg:
        mod = carregar(dotted)
        plano.append((f"{dotted.rsplit('.', 1)[-1]} ({', '.join(tbs)})", mod, {}))

    resultados = _executar(plano)
    return {
        "resultados": resultados,
        "sem_script": sem_script,
        "n_ok": sum(1 for r in resultados if r["ok"]),
        "n_erro": sum(1 for r in resultados if not r["ok"]),
    }


def executar_grupo(slug: str) -> dict:
    """Roda os scripts que alimentam as tabelas de um grupo do calendario."""
    from domain.release_calendar.sync import carregar as carregar_yaml
    from domain.release_calendar.sync import tabelas_por_grupo

    grupos = tabelas_por_grupo(carregar_yaml())
    if slug not in grupos:
        raise KeyError(f"grupo desconhecido: {slug!r}")
    tabelas = grupos[slug]
    if not tabelas:
        return {"resultados": [], "sem_script": [], "n_ok": 0, "n_erro": 0,
                "tabelas": []}
    out = executar_tabelas(tabelas)
    out["tabelas"] = tabelas
    return out


def executar_continuas() -> dict:
    """Roda as series continuas (`no_release.continuous` do calendario)."""
    from domain.release_calendar.sync import carregar as carregar_yaml
    from domain.release_calendar.sync import continuas

    return executar_tabelas(continuas(carregar_yaml()))


def _listar() -> None:
    from domain.release_calendar.sync import carregar as carregar_yaml
    from domain.release_calendar.sync import continuas, tabelas_por_grupo

    doc = carregar_yaml()
    print("--continuous roda estas tabelas:")
    for t in continuas(doc):
        print(f"    {t}")
    print("\n--group aceita:")
    for slug, tabelas in sorted(tabelas_por_grupo(doc).items()):
        print(f"    {slug:28s} {', '.join(tabelas) or '(sem tabelas)'}")


def main(argv: list[str] | None = None) -> None:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    p.add_argument("--group", action="append", metavar="SLUG",
                   help="grupo do calendario de divulgacoes (pode repetir)")
    p.add_argument("--tables", metavar="t1,t2",
                   help="tabelas especificas, separadas por virgula")
    p.add_argument("--continuous", action="store_true",
                   help="so as series continuas/diarias (sem data de divulgacao)")
    p.add_argument("--list", action="store_true", dest="listar",
                   help="lista os grupos e as tabelas continuas, e sai")
    args = p.parse_args(argv)

    if args.listar:
        _listar()
        return

    inicio = datetime.now()

    if args.continuous or args.group or args.tables:
        alvos: list[str] = []
        if args.continuous:
            from domain.release_calendar.sync import carregar as carregar_yaml
            from domain.release_calendar.sync import continuas
            alvos += continuas(carregar_yaml())
        if args.tables:
            alvos += [t.strip() for t in args.tables.split(",") if t.strip()]
        if args.group:
            from domain.release_calendar.sync import carregar as carregar_yaml
            from domain.release_calendar.sync import tabelas_por_grupo
            grupos = tabelas_por_grupo(carregar_yaml())
            for slug in args.group:
                if slug not in grupos:
                    p.error(f"grupo desconhecido: {slug!r} (use --list)")
                alvos += grupos[slug]

        alvos = sorted(set(alvos))
        logger.info("Atualizacao seletiva — %d tabela(s) alvo", len(alvos))
        out = executar_tabelas(alvos)
        resultados, sem_script = out["resultados"], out["sem_script"]
    else:
        logger.info("Iniciando atualizacao — %d scripts", len(_SCRIPTS))
        resultados = _executar(_SCRIPTS)
        sem_script = []

    erros = [(r["label"], r["erro"]) for r in resultados if not r["ok"]]
    elapsed = (datetime.now() - inicio).seconds
    n_ok = len(resultados) - len(erros)
    logger.info("Concluido em %ds — %d/%d OK", elapsed, n_ok, len(resultados))

    if sem_script:
        logger.error("%d tabela(s) sem script conhecido: %s",
                     len(sem_script), ", ".join(sem_script))

    if erros:
        logger.error("%d script(s) falharam:", len(erros))
        for label, err in erros:
            logger.error("  - %s: %s", label, err)

    if erros or sem_script:
        sys.exit(1)


if __name__ == "__main__":
    main()
