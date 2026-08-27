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

macro_brasil.pm_copom_projecoes -- PRIMARY KEY (nro_reuniao, documento, indice, cenario, date).
`documento` distingue este script (sempre 'comunicado') das linhas de 'relatorio', que vem do
RPM/RI e projetam os mesmos periodos com numeros proprios.
Upsert: reprocessar o mesmo comunicado corrige a linha em vez de duplicar.
396 linhas de 75 reunioes (206a, 2017-04-12, a 280a, 2026-08-05).

A leitura principal e uma linha por reuniao -- a projecao do horizonte que o Copom diz estar
perseguindo, no cenario de Selic da Focus:

    SELECT vintage, nro_reuniao, date, value
    FROM pm_copom_projecoes
    WHERE horizonte_relevante = 1 AND cenario = 'juros_esperado'
      AND indice = 'ipca' AND regime = 'hr_6_trimestres' AND documento = 'comunicado'
    ORDER BY vintage;

`cenario` classifica pelo CONDICIONAMENTO (juros_esperado | juros_constante), nao pelo rotulo
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
from domain.db.brasil.bcb import _rpm_projecoes as rp

_DATABASE = "macro_brasil"
_TABLE = "pm_copom_projecoes"

# tabela ganha da prosa quando as duas dizem a mesma celula
_PRECEDENCIA_FONTE = {"tabela": 0, "prosa": 1}


def _primeiro_mes_do_trimestre(p: ct.Periodo) -> dt.date:
    return dt.date(p.ano, 3 * ((p.trimestre or 4) - 1) + 1, 1)


def _input_juros(proj: ct.Projecao) -> str:
    """O que entrou como trajetoria de juros, independente do rotulo publicado."""
    if proj.cenario == "juros_constante":
        return "constante"
    # nos comunicados carregados (206+) a trajetoria esperada e sempre a mediana da Focus; o
    # "cenario de mercado" de 2016-2017, que vinha de futuros e swaps de DI, esta fora da carga
    return "focus"


def montar(comunicados: list[ct.Comunicado]) -> pd.DataFrame:
    """Comunicados parseados -> DataFrame no shape da tabela, sem duplicata de chave."""
    por_chave: dict[tuple, dict] = {}

    for c in comunicados:
        hr_norms = c.horizonte_relevante_norms()
        for proj in c.projecoes:
            chave = (c.nro_reuniao, proj.indice, proj.cenario, _primeiro_mes_do_trimestre(proj.periodo))
            linha = {
                "nro_reuniao": c.nro_reuniao,
                "documento": "comunicado",
                "date": chave[3],
                "indice": proj.indice,
                "cenario": proj.cenario,
                "cenario_publicado": proj.cenario_publicado,
                "input_juros": _input_juros(proj),
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


def montar_relatorios(edicoes: list[rp.EdicaoParseada]) -> pd.DataFrame:
    """Edicoes do RPM/RI parseadas -> DataFrame no shape da tabela.

    Uma edicao por reuniao: o relatorio sai depois da reuniao daquele mes (mar/jun/set/dez) e o
    Copom se reune 8 vezes por ano, entao nunca ha duas edicoes para a mesma reuniao -- a assercao
    abaixo garante, porque se houvesse a PK colapsaria as duas silenciosamente.
    """
    linhas = []
    vistas: dict[int, str] = {}
    for ed in edicoes:
        if ed.nro_reuniao is None or not ed.projecoes:
            continue
        anterior = vistas.get(ed.nro_reuniao)
        assert anterior is None, (
            f"edicoes {anterior} e {ed.ano_mes} casaram na mesma reuniao {ed.nro_reuniao}"
        )
        vistas[ed.nro_reuniao] = ed.ano_mes

        hr = rp.horizonte_relevante(ed.data_reuniao)
        d = dt.date.fromisoformat(ed.data_reuniao)
        tri_reuniao = d.year * 4 + (d.month - 1) // 3 + 1
        regime = (
            "hr_6_trimestres"
            if ed.nro_reuniao >= rp.PRIMEIRA_REUNIAO_HR_OFICIAL
            else "hr_aproximado"
        )
        for proj in ed.projecoes:
            qa = proj.periodo.indice - tri_reuniao
            # A tabela matriz das edicoes 2024-09+ traz tambem trimestres JA FECHADOS -- a nota diz
            # "valores em fundo branco sao efetivos e os hachurados sao projecoes", e o sombreado nao
            # existe no texto extraido. Sao 4 colunas de IPCA realizado por edicao; gravar seria
            # passar realizado por projecao. O corte e o trimestre da propria reuniao (qa=0), que
            # ainda esta aberto e portanto e projecao. O formato leque nunca comeca antes de qa=0.
            if qa < 0:
                continue
            linhas.append({
                "nro_reuniao": ed.nro_reuniao,
                "documento": "relatorio",
                "date": proj.periodo.primeiro_mes,
                "indice": proj.indice,
                "cenario": proj.cenario,
                "cenario_publicado": proj.cenario_publicado,
                "input_juros": proj.input_juros,
                "value": proj.valor,
                "vintage": ed.vintage,
                "periodo_tipo": "trimestre",
                "horizonte_relevante": int(proj.periodo.norm == hr.norm),
                "trimestres_a_frente": qa,
                "fonte": proj.fonte,
                "regime": regime,
            })
    df = pd.DataFrame(linhas)
    if df.empty:
        return df
    return df.sort_values(["nro_reuniao", "cenario", "indice", "date"]).reset_index(drop=True)


def run(sincronizar: bool = True, inicio: int | None = None, fim: int | None = None,
        relatorios: bool = True) -> None:
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
    hr = df[(df.horizonte_relevante == 1) & (df.cenario == "juros_esperado") & (df.indice == "ipca")]
    print(
        f"{_TABLE}: {len(df)} linhas de {com_proj} reunioes "
        f"({len(comunicados)} comunicados lidos, {len(comunicados) - com_proj} sem projecao "
        f"numerica no texto), periodos {df['date'].min()} -> {df['date'].max()}, "
        f"{len(hr)} pontos de horizonte relevante."
    )

    insert_data_into_database(_DATABASE, _TABLE, df)

    if not relatorios:
        return

    if sincronizar:
        r = rp.sincronizar(verbose=False)
        print(f"{_TABLE}: relatorios -- {len(r['baixados'])} PDFs baixados, "
              f"{len(r['extraidos'])} extraidos, {len(r['existentes'])} ja em disco, "
              f"{len(r['erros'])} erros.")
        if r["erros"]:
            print(f"  erros: {r['erros']}")

    edicoes = rp.carregar()
    dfr = montar_relatorios(edicoes)
    if dfr.empty:
        print(f"{_TABLE}: nenhum relatorio a inserir.")
        return
    sem_cenario = sum(1 for e in edicoes for a in e.avisos if "sem cenario" in a)
    por_ordem = sum(1 for e in edicoes for a in e.avisos if "por ORDEM" in a)
    hr = dfr[(dfr.horizonte_relevante == 1) & (dfr.cenario == "juros_esperado")
             & (dfr.indice == "ipca")]
    print(
        f"{_TABLE}: relatorios -- {len(dfr)} linhas de {dfr['nro_reuniao'].nunique()} edicoes "
        f"({len(edicoes)} lidas, {len(edicoes) - dfr['nro_reuniao'].nunique()} sem projecao), "
        f"periodos {dfr['date'].min()} -> {dfr['date'].max()}, {len(hr)} pontos de HR. "
        f"Tabelas sem cenario identificado: {sem_cenario}; classificadas por ordem: {por_ordem}."
    )
    insert_data_into_database(_DATABASE, _TABLE, dfr)
