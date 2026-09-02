# -*- coding: utf-8 -*-
"""
Confere as 26 tabelas carregadas do SGS contra a API do BCB, serie a serie.

Roda com:
    uv run python tests/test_sgs_vintage.py            # relatorio completo
    uv run python tests/test_sgs_vintage.py --tabelas mt_caged,fisc_divida
    uv run pytest tests/test_sgs_vintage.py   # se o pytest estiver instalado

Precisa de rede e do MySQL (`.env`). ~3 min para as 26 tabelas / ~630 series.

--------------------------------------------------------------------------------
POR QUE ESTE TESTE EXISTE
--------------------------------------------------------------------------------
Quase todo script de `domain/db/brasil/bcb/` atualiza por JANELA
(`get_sgs_ultimos`, `n_meses=24` ou 36). Quando o BCB **revisa o historico**, a
janela reescreve so a ponta e a tabela fica com dois vintages encostados. Nada
lanca excecao: as chaves sao as mesmas, o insert e upsert, o range nao muda.

Em 2026-08-28 isso apareceu num print do relatorio de mercado de trabalho como um
buraco de 12 meses no y/y do estoque de emprego formal. O BCB tinha reancorado
`mt_caged` para baixo em 1.357.851 vinculos revisando de 1992-01 a 2024-05 de uma
vez; a nossa tabela tinha 389 dos 414 meses no vintage velho. O **nivel** ninguem
confere numa serie de 34 anos -- mas um degrau permanente de nivel vira um vale
de exatamente 12 meses na variacao anual, que tem a forma de um evento economico.

A varredura que se seguiu achou o mesmo defeito, menor, em outras 7 tabelas
(`atv_ibcbr`, `atv_pib_mensal`, `atv_pib_usd`, `cmb_fluxo_cambial`,
`cred_credito_amplo`, `cred_credito_resumo`, `fisc_divida`) -- ali sao as revisoes
de rotina, sobretudo das series **dessazonalizadas**, que o BCB reestima sobre o
historico inteiro a cada divulgacao. Todas recarregadas com `run(start="all")`.

--------------------------------------------------------------------------------
COMO ELE CASA SERIE GRAVADA COM SERIE OFICIAL
--------------------------------------------------------------------------------
NAO pelo mapeamento nome->codigo de cada script. Se lesse o mapeamento, um script
que aponta para o codigo errado passaria no teste (e ha um caso vivo disso:
`cmb_fluxo_cambial` guarda IBC-Br com nomes de fluxo cambial). Em vez disso, casa
pelos **valores**: dos ultimos 6 meses COMUNS as duas series, que estao dentro da
janela de qualquer `n_meses` e portanto sao necessariamente iguais quando a serie
e a mesma. So depois compara o historico inteiro.

Quatro detalhes que o metodo exigiu, cada um vindo de um falso resultado:

  - **6 meses COMUNS, nao os 6 ultimos gravados.** A cauda de `mt_caged` e tampao
    (`fonte='mte'`, mes que o SGS ainda nao publicou); exigir que os 6 existam na
    fonte fazia a tabela inteira sair como "nao conferida" -- um atestado de saude
    que nao mediu nada.
  - **O casamento tem de ser UNICO.** Duas series oficiais podem coincidir nos
    ultimos 6 meses (as de intervencao cambial sao zero em quase todo mes), e ai o
    "par" seria sorteio. Sem essa regra, `cmb_reservas_bc` reportou uma divergencia
    de 21.480 que era so identificacao errada.
  - **Tambem com o sinal trocado.** `fisc_nfsp` inverte 5 series na carga (o SGS
    publica "necessidade de financiamento", positivo = deficit), entao comparar so
    o valor cru deixava 15 series sem par.
  - **Serie DIARIA recusa (406) janela de 1970 ate hoje.** Repesca em 10 anos, que
    basta para casar e comparar.

--------------------------------------------------------------------------------
O QUE ELE NAO COBRE
--------------------------------------------------------------------------------
Das ~630 series, 3 a 8 saem como "nao conferidas" a cada execucao, e isso e do
metodo, nao defeito da tabela. Tres sao fixas, em `cmb_reservas_bc`:
`reserves_other_loans` e `bcb_fx_stock_repos_loans` tem seis candidatos igualmente
validos (varios componentes de reservas sao zero ou constantes nos ultimos meses),
e `bcb_intervention_forwards` nao acha par porque o proprio ETL **descarta os
zeros** dessa serie de proposito. As demais variam de rodada para rodada: sao as
DIARIAS de `cmb_cambio_contratado`, cuja repesca de 10 anos as vezes tambem cai no
406. Uma serie sem par nao e aprovacao -- e ausencia de veredito, e por isso a
coluna existe separada de "ok".
"""

import argparse
import importlib
import sys

import pandas as pd

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from connectors.bcb import BCB
from connectors.mysql import MySQLDataRequester

TABELAS = """atv_ibcbr atv_pib_mensal atv_pib_usd cmb_balanco_pagmt cmb_cambio_contratado
cmb_fluxo_cambial cmb_reservas_bc comm_icbr comm_icbr_usd cred_credito_amplo
cred_credito_atividade_economica cred_credito_controle_capital cred_credito_familias
cred_credito_porte cred_credito_resumo cred_credito_tipo_cliente cred_inadimplencia_pj
cred_modalidade_direcionado_pf cred_modalidade_direcionado_pj cred_modalidade_livre_pf
cred_modalidade_livre_pj cred_ptc fisc_divida fisc_nfsp inflc_agregados mt_caged""".split()

# Diferenca absoluta e relativa que ainda e arredondamento da fonte, nao vintage.
_TOL_ABS = 1e-4
_TOL_REL = 1e-6
_N_CASAMENTO = 6

_bcb = BCB()


def codigos_do_modulo(nome: str) -> list[int]:
    """Codigos SGS declarados no script, lidos dos dicts do MODULO importado.

    Nao por regex sobre o texto: ali `n_meses=24`, ano e numero de tabela do BCB
    entram como se fossem codigo e o teste passa a buscar series que nao existem.
    """
    mod = importlib.import_module(f"domain.db.brasil.bcb.{nome}")
    achados: set[int] = set()

    def anda(v, prof=0):
        if prof > 4 or isinstance(v, bool):
            return
        if isinstance(v, int) and 1 <= v <= 30000:
            achados.add(v)
        elif isinstance(v, dict):
            for x in v.values():
                anda(x, prof + 1)
        elif isinstance(v, (list, tuple, set)):
            for x in v:
                anda(x, prof + 1)

    for k, v in vars(mod).items():
        if not k.startswith("__") and not callable(v):
            anda(v)
    return sorted(achados)


def _oficiais(cods: list[int]) -> dict[str, pd.Series]:
    of = _bcb.get_sgs({str(c): c for c in cods}, start="01/01/1970")
    of["date"] = pd.to_datetime(of["date"])
    out = {k: g.set_index("date")["value"].astype(float).sort_index()
           for k, g in of.groupby("name")}

    faltando = [c for c in cods if str(c) not in out]
    if faltando:                       # serie diaria: 406 na janela longa
        de = (pd.Timestamp.today() - pd.DateOffset(years=10)).strftime("%d/%m/%Y")
        of2 = _bcb.get_sgs({str(c): c for c in faltando}, start=de)
        if of2 is not None and not of2.empty:
            of2["date"] = pd.to_datetime(of2["date"])
            for k, g in of2.groupby("name"):
                out[k] = g.set_index("date")["value"].astype(float).sort_index()
    return out


def _casar(s: pd.Series, oficiais: dict[str, pd.Series]):
    """A serie oficial que reproduz `s` nos ultimos meses comuns, ou None."""
    cands = []
    for k, o0 in oficiais.items():
        comuns = s.index.intersection(o0.index).sort_values()
        if len(comuns) < _N_CASAMENTO:
            continue
        janela = comuns[-_N_CASAMENTO:]
        recente = s.reindex(janela)
        for sinal in (1, -1):
            o = o0 * sinal
            if (o.reindex(janela) - recente).abs().max() < max(
                    _TOL_ABS, recente.abs().max() * 1e-9):
                cands.append((k if sinal == 1 else f"-{k}", o))
                break
    return cands[0] if len(cands) == 1 else None


def auditar(tabela: str) -> dict:
    """{ok, divergentes, nao_conferidas, detalhe} para uma tabela."""
    cods = codigos_do_modulo(tabela)
    req = MySQLDataRequester("macro_brasil", tabela)
    req.connect()
    df = req.request_data()
    req.close_connection()
    if df is None or df.empty or not cods:
        return {"ok": 0, "divergentes": [], "nao_conferidas": [], "vazia": True}

    df["date"] = pd.to_datetime(df["date"])
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    chaves = [c for c in df.columns if c not in ("date", "value", "fonte", "vintage")]
    oficiais = _oficiais(cods)

    n_ok, divergentes, nao_conferidas = 0, [], []
    for chave, g in df.groupby(chaves):
        s = g.set_index("date")["value"].sort_index().dropna()
        if s.empty:
            continue
        par = _casar(s, oficiais)
        if par is None:
            nao_conferidas.append(str(chave))
            continue
        cod, o = par
        j = pd.DataFrame({"db": s, "sgs": o}).dropna()
        d = (j["db"] - j["sgs"]).abs()
        ruim = d[(d > _TOL_ABS) & (d / j["sgs"].abs().clip(lower=1e-9) > _TOL_REL)]
        if ruim.empty:
            n_ok += 1
        else:
            escala = j["sgs"].abs().median() or float("nan")
            divergentes.append({
                "serie": str(chave), "sgs": cod, "meses": len(ruim),
                "de": str(ruim.index.min().date()), "ate": str(ruim.index.max().date()),
                # O degrau na EMENDA e o que vira evento falso na variacao; o
                # tamanho da revisao, espalhado pelo historico, nao vira.
                "degrau": float(d.loc[ruim.index.max()]),
                "pct": float(ruim.max() / escala * 100),
            })
    return {"ok": n_ok, "divergentes": divergentes,
            "nao_conferidas": nao_conferidas, "vazia": False}


def relatorio(tabelas: list[str]) -> int:
    print(f"{'tabela':<34}{'ok':>5}{'DIVERGE':>9}{'nao conf.':>11}")
    print("-" * 59)
    problemas = []
    for t in tabelas:
        r = auditar(t)
        print(f"{t:<34}{r['ok']:>5}{len(r['divergentes']):>9}"
              f"{len(r['nao_conferidas']):>11}")
        sys.stdout.flush()
        if r["divergentes"]:
            problemas.append((t, r["divergentes"]))

    print("\n" + "=" * 72)
    if not problemas:
        print("Nenhuma divergencia: tudo que esta gravado bate com o SGS de hoje.")
        return 0
    for t, ds in problemas:
        print(f"\n### {t}  ({len(ds)} series)")
        for d in sorted(ds, key=lambda x: -x["pct"])[:12]:
            print(f"  {d['serie']:<42} sgs {d['sgs']:<7}{d['meses']:>4}m  "
                  f"{d['de']} -> {d['ate']}  degrau {d['degrau']:>12,.4f}  "
                  f"({d['pct']:.3f}% da serie)")
    print("\nRecarregue com run(start='all') -- janela nao captura revisao de historico.")
    return 1


def test_sem_vintage_misto():
    """Nenhuma serie gravada pode divergir do que o SGS publica hoje."""
    achados = {}
    for t in TABELAS:
        d = auditar(t)["divergentes"]
        if d:
            achados[t] = [x["serie"] for x in d]
    assert not achados, f"vintage misto (rode run(start='all')): {achados}"


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--tabelas", help="lista separada por virgula (default: todas)")
    a = p.parse_args()
    alvos = a.tabelas.split(",") if a.tabelas else TABELAS
    sys.exit(relatorio(alvos))
