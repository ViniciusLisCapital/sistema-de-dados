"""
JOLTS (Job Openings and Labor Turnover Survey, BLS) — vagas, contratacoes e
separacoes, nos 3 cortes que o release publica.

Uma linha por (data, corte, categoria, medida, tipo, ajuste). 295.988 linhas sobre
913 series do BLS, 2000-12 -> hoje.

--------------------------------------------------------------------------------
O ARQUIVO BRUTO E O CAMINHO DE ROTINA, NAO SO DE BACKFILL
--------------------------------------------------------------------------------
Ao contrario do `inflc_cpi`, aqui o dump vence a API nas DUAS pontas. As 913 series
uteis (das 2.060 do catalogo) sao 19 requisicoes de API por janela de 20 anos,
contra **uma** requisicao de 34 MB que
traz a historia inteira em 1,6s e nao gasta cota nenhuma. Nao ha janela de rotina a
escolher: o arquivo ja e a coisa toda.

A API entra como CONFERENCIA independente, o mesmo arranjo de `inflc_pce_dim` com o
xlsx do BEA invertido: uma requisicao com as series de manchete valida o que o
arquivo trouxe. Se o arquivo estiver velho (o BLS republica os dois no mesmo
momento, mas nada garante isso na sua ponta), a conferencia levanta em vez de gravar
um mes atrasado em silencio.

--------------------------------------------------------------------------------
UMA MEDIDA E ESTOQUE, CINCO SAO FLUXO — E A TABELA GUARDA ISSO
--------------------------------------------------------------------------------
A nota de pe do release e explicita, e e a coisa mais facil de errar num grafico:

    "The job openings level is the number of job openings on the last business day
     of the month. The levels for hires, total separations, quits, layoffs and
     discharges, and other separations are the number of each DURING THE ENTIRE
     MONTH."

Vagas sao ESTOQUE (posicao no ultimo dia util). As outras cinco sao FLUXO (tudo que
passou pela folha no mes). Consequencia direta: somar tres meses de vagas para
formar um trimestre da ~3x o numero certo e continua parecendo um grafico de vagas
-- exatamente o modo de falha que `.claude/rules/lis-dashboards.md` registra para a
arvore de reservas do relatorio cambial. A coluna `natureza` existe para que quem
agrega nao precise saber isso de cor: `estoque` ou `fluxo`, por linha.

As TAXAS nao sao nem uma coisa nem outra e nao somam de jeito nenhum: sao razoes
contra o emprego da propria categoria. O denominador tambem difere entre medidas --
a taxa de vagas divide por `emprego + vagas` (todas as posicoes, preenchidas e
abertas), as outras cinco por `emprego`. Duas taxas do mesmo mes nao estao na mesma
base, e por isso "taxa de vagas menos taxa de contratacao" nao e uma quantidade.

--------------------------------------------------------------------------------
O QUE FICA FORA, E POR QUE
--------------------------------------------------------------------------------
`UO` (vagas por desempregado) **entra**, com `tipo='razao'`: e serie publicada pelo
BLS, nao calculo nosso. Duas coisas a saber sobre ela:

  - o denominador vem da CPS, nao do JOLTS, entao ela **tem um buraco de um mes**:
    **2025-10**, valor `-` com nota de pe 9, "Data unavailable due to the 2025 lapse
    in appropriations". E o mesmo mes que falta na `inflc_cpi` (613 das 634 series
    em branco) -- um evento, dois ramos do `macro_us`. Medido: os 54 registros nao
    numericos do arquivo inteiro sao 52 de UO, todos em 2025-10 (nacional + os 51
    estados), mais 2 de taxa de resposta em outros meses. **As series do proprio
    JOLTS nao tem buraco nenhum** -- vagas, contratacoes e separacoes seguem
    completas em 2025-10, porque a coleta do JOLTS nao parou; so a CPS parou;
  - a unidade e **pessoas por vaga**, nao porcento, mesmo o BLS codificando-a com
    `ratelevel='R'`. Plotar junto de uma taxa em % e erro de eixo.

`R1`/`R2` (taxas de resposta de 1o e 2o fechamento) ficam fora: e metrica de
qualidade de coleta, nao dado economico.

Os **51 estados** ficam fora porque terminaram em 2025-M12 -- ver
`mt_jolts_dim`.

--------------------------------------------------------------------------------
REVISAO: 5 ANOS, TODO JANEIRO
--------------------------------------------------------------------------------
"Five years of data are subject to revision" (Nota Tecnica). Com a divulgacao de
janeiro entram novo benchmark de emprego do CES, novos fatores sazonais e ajustes
especiais; e todo mes os dois ultimos meses se movem com os questionarios que
chegaram depois. Em jul/2026 o proprio release anuncia junho revisado em -177 mil
vagas.

Por isso o insert e upsert sobre a historia inteira e nao ha "janela de rotina":
gravar so os ultimos meses deixaria vintages misturados na tabela, que e o defeito
que `mt_caged` do lado Brasil documenta (buraco de 12 meses no y/y, invisivel no
nivel). Custa 296 mil linhas por passe, ~40s.

--------------------------------------------------------------------------------
DDL
--------------------------------------------------------------------------------
  CREATE TABLE macro_us.mt_jolts (
      date        DATE        NOT NULL,
      corte       VARCHAR(10) NOT NULL,   -- industria | tamanho | regiao
      categoria   VARCHAR(8)  NOT NULL,   -- FK -> mt_jolts_dim
      medida      VARCHAR(2)  NOT NULL,   -- JO HI TS QU LD OS UO
      tipo        VARCHAR(6)  NOT NULL,   -- nivel | taxa | razao
      ajuste      VARCHAR(3)  NOT NULL,   -- sa | nsa
      valor       DOUBLE,
      natureza    VARCHAR(8)  NOT NULL,   -- estoque | fluxo | razao
      preliminar  TINYINT     NOT NULL DEFAULT 0,
      series_id   VARCHAR(21) NOT NULL,
      PRIMARY KEY (date, corte, categoria, medida, tipo, ajuste),
      KEY idx_serie (series_id),
      KEY idx_corte (corte, medida, tipo, ajuste)
  );

Banco: macro_us.mt_jolts -- PRIMARY KEY (date, corte, categoria, medida, tipo, ajuste)
"""

from __future__ import annotations

import pandas as pd

from connectors.bls import BLS
from domain.db.us._gravar import gravar
from domain.db.us.labor_market import mt_jolts_dim
from domain.db.us.labor_market.mt_jolts_dim import MEDIDAS, series_id

_DATABASE = "macro_us"
_TABLE = "mt_jolts"

_SURVEY = "jt"
_ARQUIVO_DADOS = "jt.data.1.AllItems"

# Vagas sao posicao no ultimo dia util do mes; o resto e tudo que passou pela folha
# durante o mes. Ver docstring -- e o que decide se agregar por soma ou por ultimo.
_NATUREZA = {
    "JO": "estoque",
    "HI": "fluxo",
    "TS": "fluxo",
    "QU": "fluxo",
    "LD": "fluxo",
    "OS": "fluxo",
    "UO": "razao",
}

MEDIDA_NOME = {
    "JO": "Job openings",
    "HI": "Hires",
    "TS": "Total separations",
    "QU": "Quits",
    "LD": "Layoffs and discharges",
    "OS": "Other separations",
    "UO": "Unemployed persons per job opening",
}

# Series de manchete usadas para conferir o arquivo contra a API. Nacional, total
# nonfarm, as 5 medidas que o texto do release cita, nivel e taxa, SA -- 10 series,
# uma requisicao.
_CONFERENCIA = [
    series_id("000000", "00", "00", medida, rl, "sa")
    for medida in ("JO", "HI", "TS", "QU", "LD")
    for rl in ("L", "R")
]


def _long(dados: pd.DataFrame, dim: pd.DataFrame) -> pd.DataFrame:
    """Vira o arquivo bruto no formato da tabela, cortando as series que nao usamos.

    O arquivo traz 2.060 series; ficam 913, que viram 961 linhas de destino -- 48
    delas sao as duas raizes compartilhadas, contadas duas vezes de propriedade (ver
    abaixo). O corte e por LOOKUP no series_id, nao
    por regex no id: um id malformado desaparece em vez de virar uma linha errada, e
    a contagem no fim e que denuncia.

    **Um series_id pode ir para MAIS DE UMA linha da tabela, e isso e da fonte.** As
    tres arvores compartilham o apice: `JTS000000000000000JOL` (Total nonfarm, vagas,
    nivel, SA) e a raiz do corte de industria E a raiz do corte de regiao, e
    `JTS100000000000000JOL` (Total private) e um no do corte de industria E a raiz do
    corte de tamanho. Sao o mesmo numero aparecendo em duas hierarquias -- a mesma
    situacao dos 13 codigos do BEA que ocupam duas linhas em `inflc_pce_dim`.

    A primeira versao usava `dict[series_id] -> destino`, e o resultado foi silencioso
    e errado: `tamanho` e `regiao` sobrescreveram as entradas de `industria`, que
    perdeu **Total private inteiro** (7.392 linhas) e ficou com um Total nonfarm de
    308 linhas -- so a serie de UO, a unica que nenhum outro corte reivindica. Nada
    levantou; o corte simplesmente veio sem raiz. Por isso o mapa e
    `series_id -> [destinos]`, e por isso `run()` confere no fim que toda categoria
    da dim tem linha no dado -- a asercao que pega este defeito de frente.
    """
    esperadas: dict[str, list[tuple]] = {}
    for _, r in dim.iterrows():
        medidas = list(MEDIDAS)
        # UO existe so no total nonfarm nacional (nao tem quebra por industria,
        # tamanho nem regiao no que o BLS publica).
        if r["corte"] == "industria" and r["categoria"] == "000000":
            medidas = medidas + ["UO"]
        for medida in medidas:
            for rl, tipo in (("L", "nivel"), ("R", "taxa")):
                ajustes = ("sa", "nsa")
                if medida == "UO":
                    if rl == "L":
                        continue           # UO so existe como razao
                    tipo = "razao"
                    # UO e publicada SO dessazonalizada (52 series no catalogo,
                    # todas com seasonal='S'): o denominador e a taxa de desemprego
                    # SA da CPS, e o BLS nao publica a contrapartida bruta.
                    ajustes = ("sa",)
                for ajuste in ajustes:
                    sid = series_id(
                        r["industry_code"], r["state_code"], r["sizeclass_code"],
                        medida, rl, ajuste,
                    )
                    esperadas.setdefault(sid, []).append(
                        (r["corte"], r["categoria"], medida, tipo, ajuste)
                    )

    presentes = dados[dados["series_id"].isin(esperadas)].copy()
    achadas = set(presentes["series_id"].unique())
    ausentes = sorted(set(esperadas) - achadas)

    presentes["preliminar"] = (
        presentes.get("footnotes", pd.Series("", index=presentes.index))
        .fillna("").str.contains("P").astype(int)
    )
    presentes = presentes.rename(columns={"value": "valor"})

    # Uma copia do bloco de observacoes por destino. Nenhum id vai para mais de 2
    # destinos hoje (as duas raizes compartilhadas), entao a duplicacao e de ~7.700
    # linhas em 281 mil.
    blocos = []
    for sid, destinos in esperadas.items():
        if sid not in achadas:
            continue
        base = presentes[presentes["series_id"] == sid]
        for corte, categoria, medida, tipo, ajuste in destinos:
            bloco = base.copy()
            bloco["corte"] = corte
            bloco["categoria"] = categoria
            bloco["medida"] = medida
            bloco["tipo"] = tipo
            bloco["ajuste"] = ajuste
            bloco["natureza"] = _NATUREZA[medida]
            blocos.append(bloco)

    cols = ["date", "corte", "categoria", "medida", "tipo", "ajuste", "valor",
            "natureza", "preliminar", "series_id"]
    saida = (pd.concat(blocos, ignore_index=True)[cols]
             .sort_values(["corte", "categoria", "medida", "tipo", "ajuste", "date"])
             .reset_index(drop=True))
    return saida, ausentes


def _conferir_api(bls: BLS, dados: pd.DataFrame) -> None:
    """Confere o arquivo bruto contra a API, valor a valor, nos ultimos 2 anos.

    Uma requisicao (10 series, 2 anos). Levanta em qualquer divergencia -- as duas
    rotas do BLS saem do mesmo processamento, entao uma diferenca significa que uma
    das duas esta velha, e nao ha "tolerancia" razoavel para isso.
    """
    hoje = pd.Timestamp.today()
    api = bls.get_series(_CONFERENCIA, start_year=hoje.year - 2, end_year=hoje.year)
    if api.empty:
        raise RuntimeError(
            "a API do BLS nao devolveu nenhuma das series de conferencia -- "
            f"{len(_CONFERENCIA)} ids pedidos. Sem isso nao ha como afirmar que o "
            "arquivo bruto esta na mesma vintage."
        )

    arq = dados[dados["series_id"].isin(_CONFERENCIA)][["date", "series_id", "value"]]
    junto = api.merge(arq, on=["date", "series_id"], suffixes=("_api", "_arq"))
    if junto.empty:
        raise RuntimeError("nenhuma observacao em comum entre API e arquivo bruto")

    dif = junto[(junto["value_api"] - junto["value_arq"]).abs() > 1e-9]
    if not dif.empty:
        pior = dif.iloc[0]
        raise RuntimeError(
            f"arquivo bruto e API discordam em {len(dif)} de {len(junto)} observacoes "
            f"(ex.: {pior['series_id']} em {pior['date'].date()}, API "
            f"{pior['value_api']} x arquivo {pior['value_arq']}). Uma das duas rotas "
            "esta numa vintage anterior."
        )

    fim_api = api["date"].max()
    fim_arq = arq.dropna(subset=["value"])["date"].max()
    if fim_arq < fim_api:
        raise RuntimeError(
            f"o arquivo bruto termina em {fim_arq.date()} e a API ja tem "
            f"{fim_api.date()} -- o dump de download.bls.gov esta atrasado."
        )
    print(f"  conferencia API: {len(junto):,} observacoes, zero divergentes, "
          f"ambas terminam em {fim_api.date()}")


def run(conferir: bool = True, gravar_dim: bool = True) -> None:
    """Atualiza macro_us.mt_jolts (e, por default, mt_jolts_dim no mesmo passe).

    Nao ha janela de rotina: o BLS revisa 5 anos e reancora tudo em janeiro, e o
    arquivo bruto traz a historia inteira numa requisicao. Ver docstring.

    Args:
        conferir:   validar o arquivo bruto contra a API (1 requisicao, ~2s).
        gravar_dim: rodar `mt_jolts_dim` no mesmo passe, reaproveitando o arquivo
                    ja baixado. `False` le a dim que ja esta no banco.
    """
    bls = BLS()
    print(f"{_TABLE}: baixando {_ARQUIVO_DADOS} (34 MB, 1 requisicao, sem cota)")
    dados = bls.get_data_file(_SURVEY, _ARQUIVO_DADOS)
    print(f"  {len(dados):,} observacoes, {dados['series_id'].nunique():,} series, "
          f"{dados['date'].min().date()} -> {dados['date'].max().date()}")

    if conferir:
        _conferir_api(bls, dados)

    if gravar_dim:
        dim = mt_jolts_dim.run(dados=dados)
    else:
        from domain.db.us._gravar import ler
        dim = ler(_DATABASE, f"SELECT * FROM {mt_jolts_dim._TABLE}")
        if dim.empty:
            raise RuntimeError(
                f"{mt_jolts_dim._TABLE} esta vazia -- rode com gravar_dim=True."
            )

    df, ausentes = _long(dados, dim)
    if ausentes:
        raise RuntimeError(
            f"{len(ausentes)} series esperadas nao estao no arquivo bruto "
            f"(ex.: {ausentes[:5]}). O BLS descontinuou uma combinacao de "
            "corte x medida x ajuste, ou o layout do series_id mudou."
        )

    # Toda categoria da dim tem de aparecer no dado. E o guarda direto do modo de
    # falha que a docstring de `_long` descreve: um corte pode perder a raiz (ou
    # qualquer no) sem que nada levante, porque o series_id continua existindo --
    # ele so foi para outro corte.
    for corte, sub_dim in dim.groupby("corte", sort=False):
        tem = set(df.loc[df["corte"] == corte, "categoria"])
        falta = sorted(set(sub_dim["categoria"]) - tem)
        if falta:
            raise RuntimeError(
                f"corte {corte!r}: {len(falta)} categorias da dim sem nenhuma linha "
                f"no dado ({falta}). Uma categoria cujo series_id e compartilhado com "
                "outro corte pode ter sido sobrescrita no mapa de destinos."
            )

    for corte, sub in df.groupby("corte", sort=False):
        print(f"  {corte}: {len(sub):,} linhas, {sub['categoria'].nunique()} categorias, "
              f"{sub['date'].min().date()} -> {sub['date'].max().date()}")
    vazios = int(df["valor"].isna().sum())
    if vazios:
        buraco = df[df["valor"].isna()].groupby(["medida"])["date"].agg(["min", "max", "size"])
        print(f"  {vazios} observacoes sem valor (esperado: so UO em 2025-10):")
        print(buraco.to_string().replace("\n", "\n    "))

    gravar(_DATABASE, _TABLE, df, sonda="categoria")


if __name__ == "__main__":
    run()
