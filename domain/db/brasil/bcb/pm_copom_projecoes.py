"""
Projecoes de inflacao do proprio Copom, extraidas dos comunicados de decisao.

NAO e a pesquisa Focus. `expc_focus*` guarda o que o MERCADO espera; esta tabela guarda o que o
BANCO CENTRAL projeta no seu cenario de referencia -- a variavel que o Copom diz estar perseguindo
quando decide a Selic, e a unica forma de medir o gap entre a projecao oficial e a meta.

Fonte: API de comunicados do BCB (`connectors/bcb_copom.py`). O texto de cada reuniao e gravado em
`repository/monetary_policy/raw_md/central_bank_comunication/` antes do parsing, e o parsing le de la
-- a carga e reproduzivel offline e o `.md` fica como trilha de auditoria do que o BCB publicou.

Parsing e levantamento dos regimes de comunicacao: `_copom_texto.py` nesta pasta.
Panorama da fonte (o que existe por era, o que nao existe): `copom_comunicados.md`.

## Series brutas

Nada e calculado aqui. Cada linha e um numero publicado no comunicado; `date`, `periodo_tipo`,
`horizonte_relevante`, `trimestres_a_frente` e `regime` sao normalizacoes do rotulo publicado, nao
transformacoes do valor.

## Escala

Variacao do IPCA acumulada em QUATRO TRIMESTRES, em %. Nao anualizar, nao acumular. Pode ser
negativa (administrados projetados em -3,9% para 2022).

## Banco

macro_brasil.pm_copom_projecoes -- PRIMARY KEY (nro_reuniao, indice, cenario, date).
Upsert: reprocessar o mesmo comunicado corrige a linha em vez de duplicar.
396 linhas de 75 reunioes (206a, 2017-04-12, a 280a, 2026-08-05).

A leitura principal e uma linha por reuniao -- a projecao do horizonte que o Copom diz estar
perseguindo, no cenario de Selic da Focus:

    SELECT vintage, nro_reuniao, date, value
    FROM pm_copom_projecoes
    WHERE horizonte_relevante = 1 AND cenario = 'juros_focus'
      AND indice = 'ipca' AND regime = 'hr_6_trimestres'
    ORDER BY vintage;

`cenario` classifica pelo CONDICIONAMENTO (juros_focus | juros_constante), nao pelo rotulo
publicado -- o nome "cenario de referencia" significava o OPOSTO em 2016-2017. O rotulo original
fica em `cenario_publicado`. Tirar o filtro de `regime` mistura tres conceitos de horizonte
diferentes; ver o COMMENT da coluna.

## Cobertura

As reunioes 48-205 (2000-06 a 2017-02) estao baixadas em `raw_md/` mas NAO entram na tabela:
ate 2009 os comunicados nao publicavam projecao alguma, e em 2016-2017 duas projecoes de cenarios
diferentes dividem a mesma frase ("nos cenarios de referencia e mercado, ... 4,4% e 4,7%,
respectivamente") com o rotulo no sentido invertido. Sao ~10 pontos; `_copom_texto.PRIMEIRA_REUNIAO_CARGA`
e onde esse piso vive.
"""

from __future__ import annotations

import datetime as dt

import pandas as pd

from connectors.mysql import insert_data_into_database
from domain.db.brasil.bcb import _copom_texto as ct

_DATABASE = "macro_brasil"
_TABLE = "pm_copom_projecoes"

# tabela ganha da prosa quando as duas dizem a mesma celula
_PRECEDENCIA_FONTE = {"tabela": 0, "prosa": 1}


def _primeiro_mes_do_trimestre(p: ct.Periodo) -> dt.date:
    return dt.date(p.ano, 3 * ((p.trimestre or 4) - 1) + 1, 1)


def montar(comunicados: list[ct.Comunicado]) -> pd.DataFrame:
    """Comunicados parseados -> DataFrame no shape da tabela, sem duplicata de chave."""
    por_chave: dict[tuple, dict] = {}

    for c in comunicados:
        hr_norms = c.horizonte_relevante_norms()
        for proj in c.projecoes:
            chave = (c.nro_reuniao, proj.indice, proj.cenario, _primeiro_mes_do_trimestre(proj.periodo))
            linha = {
                "nro_reuniao": c.nro_reuniao,
                "date": chave[3],
                "indice": proj.indice,
                "cenario": proj.cenario,
                "cenario_publicado": proj.cenario_publicado,
                "value": proj.valor,
                "vintage": dt.date.fromisoformat(c.data_reuniao),
                "periodo_tipo": proj.periodo.tipo,
                "horizonte_relevante": int(proj.periodo.norm in hr_norms),
                "trimestres_a_frente": c.trimestres_a_frente(proj.periodo),
                "fonte": proj.fonte,
                "regime": c.regime,
            }
            anterior = por_chave.get(chave)
            if anterior is None or (
                _PRECEDENCIA_FONTE[proj.fonte] < _PRECEDENCIA_FONTE[anterior["fonte"]]
            ):
                por_chave[chave] = linha

    df = pd.DataFrame(list(por_chave.values()))
    if df.empty:
        return df
    return df.sort_values(["nro_reuniao", "cenario", "indice", "date"]).reset_index(drop=True)


def run(sincronizar: bool = True, inicio: int | None = None, fim: int | None = None) -> None:
    """Atualiza macro_brasil.pm_copom_projecoes.

    Args:
        sincronizar: baixa os comunicados novos antes de parsear (default). `False` usa so o que ja
                     esta em `repository/monetary_policy/raw_md/central_bank_comunication/`, sem rede.
        inicio/fim:  recorte de reunioes, para reprocessar uma faixa. None = tudo o que ha em disco
                     (e, com `sincronizar=True`, tudo o que a API tem: da 48a a mais recente).
    """
    if sincronizar:
        r = ct.sincronizar(
            inicio=inicio if inicio is not None else ct.bcb_copom.PRIMEIRA_REUNIAO,
            fim=fim,
            verbose=False,
        )
        print(
            f"{_TABLE}: {len(r['novos'])} comunicados baixados, "
            f"{len(r['existentes'])} ja em disco, {len(r['erros'])} erros."
        )
        if r["erros"]:
            print(f"  erros: {r['erros']}")

    piso = inicio if inicio is not None else ct.PRIMEIRA_REUNIAO_CARGA
    comunicados = []
    for caminho in ct.arquivos():
        nro = int(caminho.name.split("_")[1])
        if nro < piso or (fim is not None and nro > fim):
            continue
        comunicados.append(ct.parse(caminho.read_text(encoding="utf-8"), caminho.name))

    problemas = {c.nro_reuniao: v for c in comunicados if (v := ct.validar(c))}
    if problemas:
        print(f"{_TABLE}: ATENCAO, conferencia prosa x tabela apontou {len(problemas)} reuniao(oes):")
        for nro, v in problemas.items():
            print(f"  reuniao {nro}: {'; '.join(v)}")

    df = montar(comunicados)
    if df.empty:
        print(f"{_TABLE}: nada a inserir.")
        return

    com_proj = df["nro_reuniao"].nunique()
    hr = df[(df.horizonte_relevante == 1) & (df.cenario == "juros_focus") & (df.indice == "ipca")]
    print(
        f"{_TABLE}: {len(df)} linhas de {com_proj} reunioes "
        f"({len(comunicados)} comunicados lidos, {len(comunicados) - com_proj} sem projecao "
        f"numerica no texto), periodos {df['date'].min()} -> {df['date'].max()}, "
        f"{len(hr)} pontos de horizonte relevante."
    )

    insert_data_into_database(_DATABASE, _TABLE, df)
