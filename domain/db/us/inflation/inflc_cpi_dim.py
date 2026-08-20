"""
Dimensao de itens do CPI dos EUA -- as DUAS arvores que o BLS publica, na mesma
tabela, separadas pela coluna `arvore`:

  arvore='despesa'     355 itens x 10 niveis. A estrutura estatistica completa do
                       CPI. E a arvore que responde "de que e feito o indice".
  arvore='divulgacao'   37 linhas x 5 niveis. A Tabela 1 do news release:
                       food / energy / core, e core dividido em bens e servicos.
                       E a arvore que o Fed e o mercado leem no dia da divulgacao.

O MESMO item_code aparece nas duas com nivel e pai diferentes -- `Apparel` (SAA) e
um grupo de nivel 1 na arvore de despesa e um componente de core goods no nivel 3 da
de divulgacao. Por isso a chave e (arvore, item_code) e nao item_code.

Detalhe completo, com a validacao de cada arvore: us_project/inflation_hierarchy.md

--------------------------------------------------------------------------------
COMO CADA ARVORE E CONSTRUIDA (as duas de fonte primaria, ao vivo)
--------------------------------------------------------------------------------

**despesa** -- nenhuma fonte do BLS publica esta arvore como pares pai/filho; ela e
montada. Duas fontes:
  1. `cu.item` (flat file) da os 400 item_code/item_name + `display_level`.
  2. A planilha anual de relative importance (Tabela 1, secao "Expenditure category")
     da os 294 itens que formam a arvore de despesa, na ordem publicada, com o nivel
     de indentacao e o peso.
O pai de cada linha e a ultima linha anterior com indentacao um nivel acima
(stack-walk na ordem do arquivo). `cu.item` NAO serve para isso direto: ali "All
items" (SA0) e IRMAO dos 8 grupos principais, nao pai deles -- sao 12 raizes de
nivel 0, uma floresta, nao uma arvore. A raiz e sintetizada a partir da planilha,
onde All items realmente esta um nivel acima.

O item_code vem de casar o NOME contra `cu.item`: a planilha de pesos nao traz
codigo, so nome + nivel de indentacao. Os que nao casam sao os 22 residuos
"Unsampled ..." que o BLS publica com peso mas sem serie (por isso has_series=0) --
mais 5 itens que as duas fontes rotulam DIFERENTE, resolvidos em `_ALIAS`. Sem os
aliases esses 5 caiam fora da dim tendo peso E serie publicados (0,861 ponto do
indice invisivel no relatorio). Cada par foi confirmado por POSICAO, nao por
semelhanca de nome: cada linha da planilha sem codigo tem exatamente um candidato de
`cu.item` entre os codigos dos seus vizinhos publicados, e em 2 dos 5 o
`series_title` da API traz o nome da PLANILHA, nao o de `cu.item` (a planilha diz
"swimwear, and accessories", cu.item diz "swimwear and accessories").

**A PLANILHA NAO E O NIVEL MAIS FUNDO** (`_enxertar` abaixo). Ela para em 294 linhas;
`cu.item` vai mais fundo, e esses itens tem serie publicada: Gasoline (all types) tem
os 3 tipos (unleaded regular/midgrade/premium), Coffee tem roasted e instant, New
vehicles tem cars e trucks, e ha Smartphones, College textbooks, Inpatient/Outpatient
hospital services. Sao 83 itens, todos com serie NSA (60 tambem com SA), que a arvore
ignorava por completo antes de 2026-08.

O enxerto usa a MESMA regra de pai, aplicada a ordem de `sort_sequence` de `cu.item`:
o pai e a ultima linha anterior com `display_level` um acima que JA esteja na arvore.
A regra foi validada contra a planilha antes de ser usada -- nos 266 itens que a
planilha ja posicionava, ela reproduz o pai publicado em 254, e as 12 divergencias
sao todas de itens cujo pai verdadeiro e um agregado SA (os 8 grupos de nivel 1, cujo
pai e a raiz sintetizada, mais 4 casos onde `cu.item` omite o nivel SA intermediario).
Nenhuma esta no nivel que o enxerto toca. Por isso o enxerto SO acrescenta folhas
(`tem_peso=0`) e nunca reposiciona um item que a planilha ja tenha colocado -- a
planilha continua sendo a autoridade da estrutura, e a validacao de aditividade dos
pesos roda so nela, intocada.

`tem_peso` separa as duas origens: 1 = a planilha publica peso para o item (272 itens,
mais as 37 linhas do release), 0 = veio do enxerto e NAO ha peso publicado.
Contribuicao existe so para tem_peso=1 -- os filhos enxertados de um pai nao somam o
pai em peso porque nao ha peso para somar.

Tres itens de `cu.item` ficam DE FORA do enxerto de proposito -- `Information
technology commodities` (SEEEC), `Video and audio products` (SERAC) e `Video and
audio services` (SERAS). Vem com `display_level=1`, o que os poria como filhos da
raiz, e nao estao em NENHUMA das duas secoes da planilha (nem expenditure nem special
aggregate): sao cortes transversais sem lugar nesta arvore. O `run()` lista quem ficou
fora, entao um item novo do BLS aparece no log em vez de desaparecer em silencio.

**DOIS NOS SAO RE-PARENTEADOS** (`_REPARENT` abaixo). A indentacao publicada coloca
`Alcoholic beverages` e `Information technology, hardware and services` num nivel
que nao fecha na aritmetica de pesos. A prova e o proprio peso:
    Food and beverages 14,539 = Food 13,698 + Alcoholic beverages 0,840
    Information and information processing 3,181 = 1,466 + IT hardware 1,714
    (e Communication 3,244 = 0,064 + 3,181)
Com esses dois corrigidos, TODOS os 90 pais fecham (soma dos filhos = pai, erro
maximo 0,001 -- ver `run(validar=True)`, que refaz o teste na carga).

O teste roda na arvore COMPLETA, antes de descartar os itens sem codigo. Os residuos
"Unsampled ..." carregam peso e sao filhos de verdade: testando so nos itens com
codigo, 22 dos 90 pais parecem nao fechar quando na verdade fecham.

**divulgacao** -- esta NAO precisa ser inferida: o BLS declara a hierarquia na
propria marcacao HTML da Tabela 1 do release. Cada rotulo vem em
`<p class="subN">`, onde N e a profundidade, e cada linha tem um id hierarquico
(`cpipress1.r.1`, `cpipress1.r.1.1`, ...) cujo pai e o proprio id menos o ultimo
segmento. Entao profundidade e parentesco sao LIDOS da fonte.

Isso importa porque inferir esta arvore da planilha de pesos daria errado: na secao
"Special aggregate indexes" a indentacao publicada aninha `Energy commodities`
DENTRO de `Commodities less food and energy commodities` -- uma categoria que por
definicao exclui energy commodities. A marcacao do release nao tem esse problema.

Seis nos desta arvore nao existem na de despesa (`is_special_aggregate=1`): SA0E
(Energy), SACE (Energy commodities), SA0L1E (core), SACL1E (core goods), SASLE
(core services), SAS4 (Transportation services).

`decomposicao` responde "posso somar os filhos desta linha?" -- e a coluna que
impede o erro mais facil de cometer com esta arvore:
  complete  os filhos exibidos somam o pai (niveis 0/1/2: cada um particiona o
            indice inteiro, somando 100,000)
  partial   o release mostra so os maiores filhos; falta massa (em
            `peso_nao_exibido`). 7 dos 13 pais, 25,583 pontos do indice sem linha
  leaf      sem filhos
Grafico/waterfall em nivel >= 3 precisa de barra de residuo explicita.

--------------------------------------------------------------------------------
COBERTURA (sa_begin / nsa_begin / nsa_end)
--------------------------------------------------------------------------------
MEDIDA, nao lida de metadata: e o MIN/MAX real das observacoes ja carregadas em
`macro_us.inflc_cpi`. Numa base vazia essas 3 colunas ficam NULL e o proprio
`run()` avisa. Ordem numa carga fria:

    inflc_cpi_dim.run()   # estrutura; cobertura NULL, com aviso
    inflc_cpi.run(...)    # os niveis, que leem os item_code daqui
    inflc_cpi_dim.run()   # agora preenche a cobertura

Depois disso a ordem deixa de importar -- todo run() reescreve a cobertura a partir
do que estiver no banco (upsert, idempotente).

--------------------------------------------------------------------------------
DDL
--------------------------------------------------------------------------------
  CREATE DATABASE IF NOT EXISTS macro_us
      CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;

  CREATE TABLE macro_us.inflc_cpi_dim (
      arvore               VARCHAR(12)   NOT NULL,
      item_code            VARCHAR(16)   NOT NULL,
      item_name            VARCHAR(160)  NOT NULL,
      nivel                TINYINT       NOT NULL,
      parent_item_code     VARCHAR(16),
      parent_item_name     VARCHAR(160),
      caminho              VARCHAR(1024),
      series_sa            VARCHAR(24),
      series_nsa           VARCHAR(24),
      sa_begin             SMALLINT,
      nsa_begin            SMALLINT,
      nsa_end              VARCHAR(7),
      n_filhos             SMALLINT      NOT NULL DEFAULT 0,
      is_leaf              TINYINT(1)    NOT NULL,
      has_series           TINYINT(1)    NOT NULL,
      is_special_aggregate TINYINT(1)    NOT NULL DEFAULT 0,
      tem_peso             TINYINT(1)    NOT NULL DEFAULT 1,
      decomposicao         VARCHAR(10),
      peso_nao_exibido     DOUBLE,
      sort_order           SMALLINT      NOT NULL,
      PRIMARY KEY (arvore, item_code),
      KEY idx_parent (arvore, parent_item_code)
  );
  -- COMMENTs de tabela e de coluna aplicados no MySQL (ver domain/db/CLAUDE.md).

Banco: macro_us.inflc_cpi_dim -- PRIMARY KEY (arvore, item_code)
"""

from __future__ import annotations

import re

import pandas as pd

from connectors.bls import BLS
from connectors.mysql import MySQLDataRequester
from domain.db.us._gravar import gravar

_DATABASE = "macro_us"
_TABLE = "inflc_cpi_dim"

_RELEASE_T01 = "https://www.bls.gov/news.release/cpi.t01.htm"

# Ver "DOIS NOS SAO RE-PARENTEADOS" na docstring: sem isto 4 dos 90 pais nao fecham.
_REPARENT = {
    "Alcoholic beverages": "Food and beverages",
    "Information technology, hardware and services": "Information and information processing",
}

# A planilha de pesos e o cu.item rotulam 5 itens de forma diferente. Ver
# "O item_code vem de casar o NOME" na docstring: cada par foi confirmado por posicao
# na ordem de publicacao, nao por semelhanca de nome.
#   nome na planilha de pesos  ->  nome em cu.item
_ALIAS = {
    "Housing at school, excluding board": "Lodging while at school",            # SEHB01
    "Men's underwear, nightwear, swimwear, and accessories":
        "Men's underwear, nightwear, swimwear and accessories",                  # SEAA02
    "Women's underwear, nightwear, swimwear, and accessories":
        "Women's underwear, nightwear, swimwear and accessories",                # SEAC04
    "Care of invalids and elderly at home": "Home health care",                  # SEMD03
    "Technical and business school tuition and fees":
        "Technical and vocational school tuition and fixed fees",                # SEEB04
}

# Os 6 agregados especiais da arvore de divulgacao: existem em cu.item mas nao na
# secao "Expenditure category" da planilha de pesos, logo nao na arvore de despesa.
_SPECIAL = {
    "Energy": "SA0E",
    "Energy commodities": "SACE",
    "All items less food and energy": "SA0L1E",
    "Commodities less food and energy commodities": "SACL1E",
    "Services less energy services": "SASLE",
    "Transportation services": "SAS4",
}

_SUB_ROW = re.compile(r'<th[^>]*id="([^"]+)"[^>]*>\s*<p class="sub(\d+)">(.*?)</p>', re.S)
_TR = re.compile(r"<tr[^>]*>(.*?)</tr>", re.S)
_FOOTNOTE = re.compile(r"(\(\d\))+$")


def _text(html: str) -> str:
    s = re.sub(r"<[^>]+>", "", html)
    s = s.replace("&nbsp;", " ").replace("&amp;", "&").replace("&#39;", "'")
    return re.sub(r"\s+", " ", s).strip()


def _sid(item_code: str, ajuste: str) -> str:
    return f"CU{'S' if ajuste == 'SA' else 'U'}R0000{item_code}"


# ---------------------------------------------------------------------------
# arvore = despesa
# ---------------------------------------------------------------------------
def _build_despesa(bls: BLS, weights_year: int) -> pd.DataFrame:
    itens = bls.get_item_tree()
    code_by_name = {}
    for _, r in itens.iterrows():
        code_by_name.setdefault(r["item_name"].strip(), r["item_code"].strip())
    seq_by_code = {r["item_code"].strip(): int(r["sort_sequence"]) for _, r in itens.iterrows()}

    for planilha, em_cu_item in _ALIAS.items():
        if em_cu_item not in code_by_name:
            raise ValueError(
                f"_ALIAS: {em_cu_item!r} nao existe mais em cu.item (era o item que a "
                f"planilha de pesos chama de {planilha!r}). O BLS renomeou de novo. "
                "Confirmar o novo nome por posicao antes de gravar -- sem o alias este "
                "item sai da dim tendo peso e serie publicados."
            )
        code_by_name.setdefault(planilha, code_by_name[em_cu_item])

    ri = bls.get_relative_importance(weights_year)
    exp = ri[(ri["population"] == "CPI-U") & (ri["section"] == "Expenditure category")].copy()
    exp = exp.reset_index(drop=True)

    # stack-walk: o pai e a ultima linha anterior com indent_level - 1
    rows, stack = [], {}
    for i, r in exp.iterrows():
        lvl = int(r["indent_level"])
        name = str(r["item_name"]).strip()
        stack[lvl] = name
        for deeper in [k for k in stack if k > lvl]:
            del stack[deeper]
        parent = _REPARENT.get(name, stack.get(lvl - 1))
        rows.append({
            "item_name": name,
            "nivel": lvl,
            "parent_item_name": parent,
            "weight": r["weight"],
            "sort_order": i,
        })

    df = pd.DataFrame(rows)
    df["item_code"] = df["item_name"].map(code_by_name)
    df["parent_item_code"] = df["parent_item_name"].map(code_by_name)
    df["arvore"] = "despesa"
    df["is_special_aggregate"] = 0
    df["decomposicao"] = None
    df["peso_nao_exibido"] = None
    # Itens sem codigo sao os residuos "Unsampled ..." -- ficam fora da tabela (a
    # chave exige item_code); o peso deles vive em inflc_cpi_pesos, que os preserva.
    #
    # Devolve as DUAS versoes de proposito. A aditividade tem de ser testada na
    # completa: os residuos "Unsampled ..." carregam peso e sao filhos de verdade,
    # entao testar so nos itens com codigo faz 22 dos 90 pais "nao fecharem" quando
    # na verdade fecham -- o que falta e exatamente o filho sem codigo (o caso mais
    # visivel e Owners' equivalent rent, 26,204 vs 25,230, os 0,974 que faltam sendo
    # "Unsampled owners' equivalent rent").
    codificados = df[df["item_code"].notna()].copy()
    codificados["sort_order"] = (
        codificados["item_code"].map(seq_by_code).fillna(codificados["sort_order"]).astype(int)
    )
    codificados["tem_peso"] = 1
    return df, _enxertar(itens, codificados)


def _enxertar(itens: pd.DataFrame, despesa: pd.DataFrame) -> pd.DataFrame:
    """Acrescenta os itens de cu.item que a planilha de pesos nao lista.

    So acrescenta folhas, nunca reposiciona quem a planilha ja colocou. A regra de
    pai e a validacao dela estao em "A PLANILHA NAO E O NIVEL MAIS FUNDO", na
    docstring do modulo.
    """
    itens = itens.copy()
    itens["display_level"] = itens["display_level"].astype(int)
    itens["sort_sequence"] = itens["sort_sequence"].astype(int)
    itens = itens.sort_values("sort_sequence")

    nivel_de = dict(zip(despesa["item_code"], despesa["nivel"]))
    nome_de = dict(zip(despesa["item_code"], despesa["item_name"]))
    pilha: dict[int, tuple[str, int]] = {}   # display_level de cu.item -> (code, nivel nosso)
    novos, fora = [], []

    for r in itens.itertuples():
        code, nome, dl = r.item_code.strip(), r.item_name.strip(), int(r.display_level)
        for mais_fundo in [k for k in pilha if k > dl]:
            del pilha[mais_fundo]

        if code in nivel_de:            # a planilha ja posicionou: serve de ancora
            pilha[dl] = (code, int(nivel_de[code]))
            continue
        # display_level < 2 em cu.item = corte transversal (SEEEC/SERAC/SERAS) ou
        # agregado SA; nenhum dos dois tem lugar na arvore de despesa.
        if code.startswith(("SA", "AA")) or dl < 2 or (dl - 1) not in pilha:
            fora.append((code, nome, dl))
            continue

        pai_code, pai_nivel = pilha[dl - 1]
        novos.append({
            "item_name": nome,
            "nivel": pai_nivel + 1,
            "parent_item_name": nome_de.get(pai_code),
            "parent_item_code": pai_code,
            "weight": float("nan"),
            "sort_order": int(r.sort_sequence),
            "item_code": code,
            "arvore": "despesa",
            "is_special_aggregate": 0,
            "decomposicao": None,
            "peso_nao_exibido": None,
            "tem_peso": 0,
        })
        nome_de[code] = nome
        pilha[dl] = (code, pai_nivel + 1)

    print(f"  enxerto de cu.item: +{len(novos)} itens sem peso publicado "
          "(o nivel mais fundo, que a planilha nao lista)")
    transversais = [f"{n} [{c}]" for c, n, dl in fora if not c.startswith(("SA", "AA"))]
    if transversais:
        print(f"    fora do enxerto: {', '.join(transversais)} -- sem lugar nesta "
              "arvore, ver a docstring")
    return pd.concat([despesa, pd.DataFrame(novos)], ignore_index=True) if novos else despesa


# ---------------------------------------------------------------------------
# arvore = divulgacao
# ---------------------------------------------------------------------------
def _build_divulgacao(bls: BLS, despesa: pd.DataFrame) -> pd.DataFrame:
    html = bls.get_release_table(_RELEASE_T01)
    body = html[html.find("<tbody"):]
    code_by_name = dict(zip(despesa["item_name"], despesa["item_code"]))
    code_by_name.update(_SPECIAL)

    rows = []
    for i, tr in enumerate(_TR.findall(body)):
        m = _SUB_ROW.search(tr)
        if not m:
            continue
        rid, lvl, label = m.group(1), int(m.group(2)), _text(m.group(3))
        name = _FOOTNOTE.sub("", label).strip()
        ri_txt = [_text(v) for v in re.findall(r"<td[^>]*>(.*?)</td>", tr, re.S)]
        rows.append({
            "row_id": rid,
            "nivel": lvl,
            "item_name": name,
            "item_code": code_by_name.get(name),
            "ri": float(ri_txt[0]) if ri_txt and ri_txt[0] else None,
            "sort_order": i,
        })

    df = pd.DataFrame(rows)
    if df["item_code"].isna().any():
        raise ValueError(
            "linhas da Tabela 1 sem item_code: "
            f"{df.loc[df['item_code'].isna(), 'item_name'].tolist()} -- "
            "o BLS mudou um rotulo, ou um agregado novo entrou no release. "
            "Conferir _SPECIAL e o nome em cu.item antes de seguir."
        )

    # pai = o id menos o ultimo segmento (cpipress1.r.1.1 -> cpipress1.r.1)
    by_id = dict(zip(df["row_id"], df["item_name"]))
    parent_name, parent_code = [], []
    for rid in df["row_id"]:
        pid = rid.rsplit(".", 1)[0] if rid.count(".") > 2 else None
        pn = by_id.get(pid) if pid else None
        parent_name.append(pn)
        parent_code.append(code_by_name.get(pn) if pn else None)
    df["parent_item_name"] = parent_name
    df["parent_item_code"] = parent_code

    soma = df.groupby("parent_item_name")["ri"].sum()
    n_kids = df.groupby("parent_item_name")["ri"].size()
    df["_kids"] = df["item_name"].map(n_kids).fillna(0).astype(int)
    df["_soma"] = df["item_name"].map(soma)
    df["peso_nao_exibido"] = (df["ri"] - df["_soma"]).round(3)
    df["decomposicao"] = [
        "leaf" if k == 0 else ("complete" if abs(d) < 0.002 else "partial")
        for k, d in zip(df["_kids"], df["peso_nao_exibido"].fillna(0))
    ]
    df.loc[df["decomposicao"] != "partial", "peso_nao_exibido"] = None
    df["arvore"] = "divulgacao"
    df["is_special_aggregate"] = df["item_name"].isin(_SPECIAL).astype(int)
    df["tem_peso"] = 1      # o proprio release publica a RI das 37 linhas
    return df.drop(columns=["row_id", "_kids", "_soma", "ri"])


# ---------------------------------------------------------------------------
def _finalize(df: pd.DataFrame) -> pd.DataFrame:
    """Colunas derivadas comuns as duas arvores: caminho, n_filhos, is_leaf, series."""
    out = []
    for arvore, g in df.groupby("arvore", sort=False):
        g = g.copy()
        name_by_code = dict(zip(g["item_code"], g["item_name"]))
        parent_by_code = dict(zip(g["item_code"], g["parent_item_code"]))

        def caminho(code):
            # pd.isna() e nao `if code`: o pai da raiz vem como NaN do merge, e NaN
            # e truthy -- um `while code` puro poe o NaN dentro do caminho e o join
            # estoura com "expected str instance, float found".
            partes, seen = [], set()
            while isinstance(code, str) and code and code not in seen:
                seen.add(code)
                partes.append(name_by_code.get(code, code))
                code = parent_by_code.get(code)
            return " > ".join(reversed(partes))[:1024]

        g["caminho"] = g["item_code"].map(caminho)
        kids = g["parent_item_code"].value_counts()
        g["n_filhos"] = g["item_code"].map(kids).fillna(0).astype(int)
        g["is_leaf"] = (g["n_filhos"] == 0).astype(int)
        out.append(g)

    df = pd.concat(out, ignore_index=True)
    df["series_sa"] = df["item_code"].map(lambda c: _sid(c, "SA"))
    df["series_nsa"] = df["item_code"].map(lambda c: _sid(c, "NSA"))
    df["has_series"] = 1
    return df


def _coverage() -> pd.DataFrame | None:
    """MIN/MAX real por item_code x ajuste, do que ja esta em macro_us.inflc_cpi."""
    req = MySQLDataRequester(_DATABASE, _TABLE)
    req.connect()
    if req.connection is None:
        return None
    try:
        cov = pd.read_sql(
            "SELECT item_code, ajuste, MIN(date) AS ini, MAX(date) AS fim, COUNT(*) AS n "
            "FROM inflc_cpi WHERE value IS NOT NULL GROUP BY item_code, ajuste",
            req.connection,
        )
    finally:
        req.connection.close()
    if not len(cov):
        return None
    # pd.read_sql sobre conexao DBAPI crua devolve DATE como object (datetime.date),
    # nao datetime64 -- sem este to_datetime o .dt logo abaixo levanta
    # "Can only use .dt accessor with datetimelike values".
    cov["ini"] = pd.to_datetime(cov["ini"])
    cov["fim"] = pd.to_datetime(cov["fim"])
    return cov


def _aplicar_cobertura(df: pd.DataFrame) -> pd.DataFrame:
    cov = _coverage()
    df["sa_begin"] = pd.NA
    df["nsa_begin"] = pd.NA
    df["nsa_end"] = pd.NA
    if cov is None:
        print("  aviso: macro_us.inflc_cpi esta vazia -- sa_begin/nsa_begin/nsa_end")
        print("         ficam NULL. Rode inflc_cpi.run() e depois este script de novo.")
        return df

    sa = cov[cov["ajuste"] == "SA"].set_index("item_code")
    nsa = cov[cov["ajuste"] == "NSA"].set_index("item_code")
    df["sa_begin"] = df["item_code"].map(sa["ini"].dt.year if len(sa) else {})
    df["nsa_begin"] = df["item_code"].map(nsa["ini"].dt.year if len(nsa) else {})
    df["nsa_end"] = df["item_code"].map(
        nsa["fim"].dt.strftime("%Y-%m") if len(nsa) else {}
    )
    # has_series=0 quando nem SA nem NSA tem observacao no banco.
    df["has_series"] = (df["sa_begin"].notna() | df["nsa_begin"].notna()).astype(int)
    df.loc[df["sa_begin"].isna(), "series_sa"] = None
    df.loc[df["nsa_begin"].isna(), "series_nsa"] = None
    return df


def _validar_despesa(despesa_raw: pd.DataFrame) -> None:
    """Refaz o teste de aditividade dos pesos: soma dos filhos == pai, 90/90."""
    w = dict(zip(despesa_raw["item_name"], despesa_raw["weight"]))
    soma = despesa_raw.groupby("parent_item_name")["weight"].sum()
    piores, n = [], 0
    for pai, s in soma.items():
        if pai is None or pai not in w or pd.isna(w[pai]):
            continue
        n += 1
        piores.append((abs(w[pai] - s), pai, w[pai], s))
    piores.sort(reverse=True)
    ruins = [p for p in piores if p[0] > 0.002]
    print(f"  aditividade dos pesos: {n - len(ruins)}/{n} pais fecham "
          f"(erro maximo {piores[0][0]:.3f})")
    for d, pai, pv, s in ruins[:5]:
        print(f"    NAO FECHA  {pai}: pai {pv:.3f} vs soma dos filhos {s:.3f} (diff {d:.3f})")
    if ruins:
        raise ValueError(
            f"{len(ruins)} pais nao fecham na aritmetica de pesos. Provavelmente o BLS "
            "mudou a indentacao publicada -- reveja _REPARENT antes de gravar."
        )


def run(weights_year: int = 2025, validar: bool = True) -> None:
    """Reconstroi macro_us.inflc_cpi_dim a partir das fontes primarias.

    Args:
        weights_year: ano da planilha de relative importance que define a arvore de
                      despesa (quais itens, em que nivel). Default 2025, a mais
                      recente. So a ESTRUTURA vem daqui -- os pesos de todos os anos
                      vivem em inflc_cpi_pesos.
        validar:      refaz o teste de aditividade dos pesos e levanta se algum pai
                      nao fechar (default True; e o que detecta o BLS mudando a
                      indentacao publicada).
    """
    bls = BLS()

    print(f"despesa: cu.item + relative importance {weights_year}...")
    completa, despesa = _build_despesa(bls, weights_year)
    com_peso = int((despesa["tem_peso"] == 1).sum())
    print(f"  planilha: {len(completa)} linhas, {com_peso} com codigo "
          f"({len(completa) - com_peso} sem -- residuos 'Unsampled', esperado)")
    print(f"  arvore de despesa: {len(despesa)} itens, {len(despesa) - com_peso} deles "
          "sem peso publicado (enxerto)")
    if validar:
        _validar_despesa(completa)

    print("divulgacao: Tabela 1 do news release...")
    divulgacao = _build_divulgacao(bls, despesa)
    conta = divulgacao["decomposicao"].value_counts().to_dict()
    print(f"  {len(divulgacao)} linhas, niveis {divulgacao['nivel'].min()}-{divulgacao['nivel'].max()}, "
          f"decomposicao {conta}")
    naoexib = divulgacao["peso_nao_exibido"].sum()
    print(f"  massa sem linha filha nos pais 'partial': {naoexib:.3f} pontos do indice")

    base_cols = ["arvore", "item_code", "item_name", "nivel", "parent_item_code",
                 "parent_item_name", "is_special_aggregate", "tem_peso", "decomposicao",
                 "peso_nao_exibido", "sort_order"]
    df = _finalize(pd.concat(
        [despesa.reindex(columns=base_cols), divulgacao.reindex(columns=base_cols)],
        ignore_index=True,
    ))
    df = _aplicar_cobertura(df)

    for c in ("parent_item_code", "parent_item_name", "decomposicao"):
        df[c] = df[c].where(df[c].notna(), None)

    cols = ["arvore", "item_code", "item_name", "nivel", "parent_item_code",
            "parent_item_name", "caminho", "series_sa", "series_nsa", "sa_begin",
            "nsa_begin", "nsa_end", "n_filhos", "is_leaf", "has_series",
            "is_special_aggregate", "tem_peso", "decomposicao", "peso_nao_exibido",
            "sort_order"]
    gravar(_DATABASE, _TABLE, df[cols], sonda="arvore")
    print(f"  {(df.arvore == 'despesa').sum()} despesa + "
          f"{(df.arvore == 'divulgacao').sum()} divulgacao")


if __name__ == "__main__":
    run()
