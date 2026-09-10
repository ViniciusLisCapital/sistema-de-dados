"""
Productivity and Costs (`prod2`) -- produtividade do trabalho, remuneracao e custo
unitario do trabalho por setor maior, do programa MSPC do BLS.

    from domain.db.us.labor_market import mt_produtividade
    mt_produtividade.run()               # 1947 -> hoje, as 282 series inteiras

E a terceira pesquisa do ramo de mercado de trabalho dos EUA a entrar, e a UNICA
trimestral -- JOLTS, CES e CPS sao mensais. Sai duas vezes por trimestre (preliminar
e revisada), as 08:30 ET, ~40 dias depois do fim do trimestre.

--------------------------------------------------------------------------------
O CATALOGO E PEQUENO E FECHADO: 282 SERIES, E ELAS SAO UM PRODUTO CARTESIANO
--------------------------------------------------------------------------------
    PRS 8500 6 09 2      PR + S/U + setor(4) + classe(1) + medida(2) + duracao(1)
    ^^^ ^^^^ ^ ^^ ^
    |   |    | |  \\-- 1 = %chg 4 trimestres, 2 = %chg tri anualizado, 3 = indice
    |   |    | \\----- a medida (22 codigos)
    |   |    \\------- 6 = todos os trabalhadores, 3 = empregados
    |   \\------------ o setor (6 codigos)
    \\---------------- PRS = dessazonalizado (nao existe serie U nesta pesquisa)

O id tem **11 caracteres**, nao 13 como a CES nem 20 como o JOLTS. Todos os 282 ids
derivados batem com `pr.series` (conferido na carga), e nao ha serie no dado que falte
no catalogo nem vice-versa.

A `classe` NAO e uma dimensao independente: e funcao do setor -- 6 (todos os
trabalhadores) nos cinco primeiros e 3 (empregados) nas corporacoes nao financeiras,
que por definicao nao tem conta propria. Por isso ela e coluna e nao entra na chave.

--------------------------------------------------------------------------------
(1) A `duracao` E O ACHADO QUE MUDA O DESENHO: A FONTE PUBLICA AS TRES LEITURAS
--------------------------------------------------------------------------------
Cada quantidade vem em tres series distintas -- o indice (2017=100), a variacao sobre
o trimestre anterior anualizada e a variacao sobre o mesmo trimestre do ano anterior.
Sao os tres paineis de cada tabela do release, e sao **dado publicado**, nao
transformacao nossa.

Duas precisoes diferentes, e o arquivo e mais generoso que o release: **o indice vem
com tres decimais e as duas variacoes com uma**. E exatamente a precisao que a nota (5)
das tabelas diz que o BLS usa para calcular ("percent changes are calculated using index
numbers to three decimal places"), e o release imprime o indice a uma decimal so "for
convenience".

Consequencia medida (317 observacoes do nonfarm, 157 do durable, mais o custo unitario):
recomputar a variacao a partir do indice **do arquivo** concorda com a publicada em
**0,025 p.p. em media e 0,0500 p.p. no maximo, nunca acima** -- ou seja, o residuo e
inteiramente o arredondamento da TAXA publicada a uma decimal, e a reconta e, se algo,
mais fina. Recomputar a partir do indice **do release** e que erra: 0,27 p.p. em media e
**1,35 p.p.** no maximo.

Entao a razao para carregar as tres duracoes nao e que a reconta erre. E que a taxa
publicada e o numero citavel -- quem compara com a manchete quer 1,4, nao 1,3999 -- e
que assim a leitura anual da pagina e a do BLS e nao a nossa. O aviso reutilizavel e
sobre o PDF: nao reconstrua serie a partir de numero impresso em tabela de divulgacao.

Corolario para o Q05 (media anual): as duracoes 1 e 2 tem o **mesmo** valor ali, porque
"trimestre anterior" e "mesmo trimestre do ano anterior" colapsam os dois no ano
anterior. Conferido em todas as medidas e todos os anos na carga.

--------------------------------------------------------------------------------
(2) NADA NESTA PESQUISA E ADITIVO, E POR DUAS RAZOES INDEPENDENTES
--------------------------------------------------------------------------------
Os seis setores **se contem** em vez de particionar: Business ⊃ Nonfarm business, e
Manufacturing e Nonfinancial corporations sao recortes de dentro do nonfarm. So
Durable + Nondurable = Manufacturing e uma particao de verdade -- e mesmo essa nao
soma, porque o que se publica e **indice**: (durable + nondurable) / manufacturing da
~2,0 (medido: media 2,021 na produtividade), que e o que dois indices de base 100
sempre dao.

Logo: nenhuma barra empilhada, nenhum "% do total", nenhuma regra de pai-vira-linha.
O relatorio desliga os tres controles e diz por que. E a versao mais limpa da regra de
`.claude/rules/lis-dashboards.md`: a validade do controle e propriedade do dado.

--------------------------------------------------------------------------------
(3) "PRODUTIVIDADE = PRODUTO - HORAS" ERRA ATE 15,9 P.P., E O PROPRIO RELEASE
    ESCREVE A IDENTIDADE ASSIM
--------------------------------------------------------------------------------
O texto do release diz "productivity increased 1.4 percent as output increased 1.7
percent and hours worked increased 0.3 percent" -- e 1,7 - 0,3 = 1,4, exato. A subtracao
funciona em taxas pequenas e **quebra em taxas grandes**, porque a relacao verdadeira e
multiplicativa: (1+p) = (1+o)/(1+h).

Medido nas 317 observacoes do nonfarm business e nas 157 do durable:

    | forma          | erro medio | erro maximo |
    |----------------|------------|-------------|
    | subtracao      | 0,14 p.p.  | **15,9 p.p.** |
    | multiplicativa | 0,04 p.p.  | 0,18 p.p.   |

O pior caso e 2020T3 no durable: produto +91,3%, horas +37,1%. A subtracao diz
produtividade +54,2%; o publicado e **+39,5%**. Os 0,04 p.p. que sobram na forma certa
sao o arredondamento acumulado de tres series de uma decimal, e nao caem mais.

A mesma coisa vale para custo unitario = remuneracao/hora ÷ produtividade. As duas
identidades sao verificadas na carga, na forma multiplicativa **e** no indice (onde
fecham em 0,002).

--------------------------------------------------------------------------------
(4) DOIS CONCEITOS DE PRODUTO NUMA COLUNA SO -- E ISSO ESTA NO PROPRIO CATALOGO
--------------------------------------------------------------------------------
O release avisa em prosa que "os conceitos, fontes e metodos do produto da industria de
transformacao diferem dos do business/nonfarm business; estas medidas nao sao
diretamente comparaveis". Nao e preciso confiar na nota: a incomparabilidade E o
catalogo. As medidas 04/05/14 (valor adicionado) existem **so** para business, nonfarm
e nao financeiras; as 21/22/23 (setorial) existem **so** para as tres de transformacao.
Nenhum setor tem as duas.

Esta tabela funde os pares num slug so (`produto_real`, `produto_nominal`,
`deflator_produto`) e carrega `conceito_produto` em toda linha, que e o que o release
faz na Tabela A1 -- uma coluna "Output" cobrindo os cinco setores, com a nota. A
alternativa (slugs separados) deixaria a grade esburacada e faria uma consulta por
"produto real" devolver tres setores em vez de seis, sem avisar. A carga garante que
cada setor tem **um** conceito.

--------------------------------------------------------------------------------
(5) A MEDIA ANUAL E UM PERIODO Q05, E O CONNECTOR NAO A CONHECIA
--------------------------------------------------------------------------------
`pr` publica Q01-Q04 mais **Q05 = media anual**, e so para anos completos (1947-2025;
2026 nao tem). Antes de 2026-09-03 o `_to_date` do connector nao conhecia o codigo e a
linha era descartada por `dropna`, nao pelo filtro de agregados -- mesmo resultado por
acidente, e sem jeito de pedir a media anual. Corrigido no connector; aqui as duas
grades entram separadas por `periodicidade`, o que impede a colisao (Q05 e Q01 de um
mesmo ano cairiam os dois em 1 de janeiro).

`MAX(date)` da tabela e o ultimo TRIMESTRE, porque a media anual do ano corrente nunca
existe -- e o que faz a checagem de frescor do calendario funcionar sem clausula extra.

--------------------------------------------------------------------------------
ARQUIVO E NAO API (como CES e JOLTS, ao contrario da CPS)
--------------------------------------------------------------------------------
`pr.data.1.AllData` tem 3,2 MB e traz as 282 series x 80 anos numa requisicao sem
chave. Pela API seriam 6 requisicoes por janela de 20 anos, 24 no historico inteiro. A
API entra como **conferencia independente** de vintage a cada carga (uma requisicao,
uma amostra de series na janela recente), no mesmo papel que tem no `mt_ces`.

--------------------------------------------------------------------------------
DDL
--------------------------------------------------------------------------------
    CREATE TABLE mt_produtividade (
        date             DATE          NOT NULL COMMENT 'primeiro dia do trimestre; 1 de janeiro quando periodicidade = anual',
        setor            VARCHAR(26)   NOT NULL COMMENT 'slug do setor maior (ver _SETORES)',
        medida           VARCHAR(34)   NOT NULL COMMENT 'slug da medida (ver _MEDIDAS)',
        duracao          VARCHAR(10)   NOT NULL COMMENT 'indice = 2017=100; tri_anual = %chg sobre o tri anterior anualizado; ano_a_ano = %chg sobre o mesmo tri do ano anterior',
        periodicidade    VARCHAR(10)   NOT NULL COMMENT 'trimestral (Q01-Q04) ou anual (Q05, media do ano; so anos completos)',
        valor            DECIMAL(12,3)     NULL COMMENT 'indice quando duracao = indice, por cento nas outras duas',
        classe           VARCHAR(12)   NOT NULL COMMENT 'todos = todos os trabalhadores; empregados = so empregados (nas corporacoes nao financeiras). E funcao do setor, nao dimensao',
        conceito_produto VARCHAR(16)   NOT NULL COMMENT 'valor_adicionado (business, nonfarm, nao financeiras) ou setorial (transformacao). Os dois NAO sao comparaveis -- ver (4) no docstring',
        revisado         TINYINT(1)    NOT NULL COMMENT '1 quando o BLS marca a celula com r=revised nesta divulgacao',
        series_id        VARCHAR(20)   NOT NULL COMMENT 'series_id do BLS (11 caracteres)',
        PRIMARY KEY (date, setor, medida, duracao, periodicidade)
    ) COMMENT 'BLS/MSPC (release prod2): produtividade do trabalho, remuneracao e custo
               unitario por setor maior. NADA aqui e aditivo (setores se contem e o que
               se publica e indice). Ver domain/db/us/labor_market/mt_produtividade.py'
"""

from __future__ import annotations

import pandas as pd

from connectors.bls import BLS
from domain.db.us._gravar import gravar

_DATABASE = "macro_us"
_TABLE = "mt_produtividade"

_SURVEY = "pr"
_ARQUIVO = "pr.data.1.AllData"
_ANO_INICIAL = 1947

# codigo -> (slug, rotulo, classe, conceito de produto)
_SETORES: dict[str, tuple[str, str, str, str]] = {
    "8500": ("nonfarm_business", "Nonfarm business", "todos", "valor_adicionado"),
    "8400": ("business", "Business", "todos", "valor_adicionado"),
    "8800": ("nonfinancial_corp", "Nonfinancial corporations", "empregados", "valor_adicionado"),
    "3000": ("manufacturing", "Manufacturing", "todos", "setorial"),
    "3100": ("manufacturing_durable", "Durable manufacturing", "todos", "setorial"),
    "3200": ("manufacturing_nondurable", "Nondurable manufacturing", "todos", "setorial"),
}

# codigo -> slug. Os tres pares valor-adicionado/setorial caem no MESMO slug de
# proposito (ver (4) no docstring): nenhum setor tem os dois lados do par.
_MEDIDAS: dict[str, str] = {
    "01": "emprego",
    "02": "horas_semana",
    "03": "horas_trabalhadas",
    "04": "produto_real",                       # valor adicionado
    "21": "produto_real",                       # setorial
    "05": "produto_nominal",                    # valor adicionado
    "23": "produto_nominal",                    # setorial
    "14": "deflator_produto",                   # valor adicionado
    "22": "deflator_produto",                   # setorial
    "06": "remuneracao_total",
    "08": "pagamentos_nao_trabalho",
    "09": "produtividade",
    "10": "remuneracao_hora",
    "11": "custo_unitario_trabalho",
    "12": "custo_unitario_nao_trabalho",
    "13": "pagamento_unitario_nao_trabalho",
    "15": "remuneracao_hora_real",
    "16": "produto_por_trabalhador",
    "17": "parcela_trabalho",
    "18": "lucros",
    "19": "lucro_unitario",
    "20": "custo_unitario_combinado",
}

_DURACOES: dict[str, str] = {
    "1": "ano_a_ano",
    "2": "tri_anual",
    "3": "indice",
}

# Series da amostra usada na conferencia contra a API: as manchetes dos seis setores
# nas tres duracoes. 54 series numa requisicao.
_AMOSTRA_MEDIDAS = ("09", "11", "10")

# Tolerancias, cada uma com origem declarada.
#
# _TOL_INDICE: as identidades no indice envolvem tres series arredondadas a uma
# decimal, entao o residuo maximo admissivel e ~0,05/100 propagado -- medido em 0,002.
_TOL_INDICE = 0.005
# _TOL_VARIACAO: idem na forma multiplicativa das taxas -- medido em 0,18 p.p. no
# durable, que e o setor de maior amplitude.
_TOL_VARIACAO = 0.30
# _TOL_API: o arquivo e a API sao o mesmo vintage; a diferenca esperada e zero.
_TOL_API = 0.0005


def _catalogo(bls: BLS) -> pd.DataFrame:
    """`pr.series` com o id derivado conferido contra o publicado."""
    cat = bls.get_series_catalog(_SURVEY)
    faltam = {"series_id", "sector_code", "class_code", "measure_code",
              "duration_code", "seasonal"} - set(cat.columns)
    if faltam:
        raise RuntimeError(f"pr.series sem as colunas {sorted(faltam)} — layout mudou")

    derivado = ("PR" + cat["seasonal"] + cat["sector_code"] + cat["class_code"]
                + cat["measure_code"] + cat["duration_code"])
    ruins = cat.loc[derivado != cat["series_id"], "series_id"].tolist()
    if ruins:
        raise RuntimeError(
            f"{len(ruins)} ids nao se derivam de (setor, classe, medida, duracao): "
            f"{ruins[:5]}. A composicao do series_id da pesquisa `pr` mudou."
        )

    desconhecidos = set(cat["sector_code"]) - set(_SETORES)
    if desconhecidos:
        raise RuntimeError(
            f"setores novos em pr.sector: {sorted(desconhecidos)}. Cada setor precisa "
            "de conceito de produto declarado — ver (4) no docstring."
        )
    desconhecidos = set(cat["measure_code"]) - set(_MEDIDAS)
    if desconhecidos:
        raise RuntimeError(f"medidas novas em pr.measure: {sorted(desconhecidos)}")

    # A classe e funcao do setor: se deixar de ser, ela precisa entrar na chave.
    por_setor = cat.groupby("sector_code")["class_code"].nunique()
    if (por_setor > 1).any():
        maus = por_setor[por_setor > 1].index.tolist()
        raise RuntimeError(
            f"os setores {maus} passaram a ter mais de uma classe de trabalhador. "
            "A chave primaria de mt_produtividade assume uma classe por setor."
        )
    for cod, (_, _, classe, _) in _SETORES.items():
        esperado = {"todos": "6", "empregados": "3"}[classe]
        real = set(cat.loc[cat["sector_code"] == cod, "class_code"])
        if real and real != {esperado}:
            raise RuntimeError(
                f"setor {cod}: classe declarada {classe} ({esperado}), catalogo diz {real}"
            )
    return cat


def _ler_arquivo(bls: BLS) -> pd.DataFrame:
    """`pr.data.1.AllData` em long, com Q01-Q05 e a marca de revisao."""
    bruto = bls.read_flat_table(_SURVEY, _ARQUIVO)
    bruto["valor"] = pd.to_numeric(bruto["value"], errors="coerce")
    bruto["periodicidade"] = bruto["period"].map(
        lambda p: "anual" if p == "Q05" else ("trimestral" if p in
                                             {"Q01", "Q02", "Q03", "Q04"} else None))
    fora = sorted(set(bruto.loc[bruto["periodicidade"].isna(), "period"]))
    if fora:
        raise RuntimeError(
            f"periodos desconhecidos em {_ARQUIVO}: {fora}. `pr` publica Q01-Q05."
        )
    ano = bruto["year"].astype(int)
    mes = bruto["period"].map({"Q01": 1, "Q02": 4, "Q03": 7, "Q04": 10, "Q05": 1})
    bruto["date"] = pd.to_datetime(dict(year=ano, month=mes, day=1))
    bruto["revisado"] = (bruto["footnote_codes"].fillna("").str.upper()
                         .str.contains("R").astype(int))
    return bruto.dropna(subset=["valor"])


def _montar(dados: pd.DataFrame, cat: pd.DataFrame) -> pd.DataFrame:
    dim = cat[["series_id", "sector_code", "class_code", "measure_code", "duration_code"]]
    out = dados.merge(dim, on="series_id", how="left")
    orfas = sorted(set(out.loc[out["sector_code"].isna(), "series_id"]))
    if orfas:
        raise RuntimeError(f"{len(orfas)} series no dado sem entrada em pr.series: {orfas[:5]}")

    sem_dado = set(cat["series_id"]) - set(dados["series_id"])
    if sem_dado:
        raise RuntimeError(
            f"{len(sem_dado)} series do catalogo sem uma linha de dado: "
            f"{sorted(sem_dado)[:5]}. O arquivo veio incompleto."
        )

    out["setor"] = out["sector_code"].map(lambda c: _SETORES[c][0])
    out["classe"] = out["sector_code"].map(lambda c: _SETORES[c][2])
    out["conceito_produto"] = out["sector_code"].map(lambda c: _SETORES[c][3])
    out["medida"] = out["measure_code"].map(_MEDIDAS)
    out["duracao"] = out["duration_code"].map(_DURACOES)

    # A fusao dos pares de produto so e legitima porque nenhum setor tem os dois lados.
    dupe = out.duplicated(subset=["date", "setor", "medida", "duracao", "periodicidade"])
    if dupe.any():
        exemplo = out.loc[dupe, ["date", "setor", "medida", "duracao"]].head(3)
        raise RuntimeError(
            "dois series_id caindo na mesma chave — um setor passou a publicar produto "
            f"por valor adicionado E setorial:\n{exemplo.to_string(index=False)}"
        )

    cols = ["date", "setor", "medida", "duracao", "periodicidade", "valor",
            "classe", "conceito_produto", "revisado", "series_id"]
    return out[cols].sort_values(["date", "setor", "medida", "duracao", "periodicidade"])


def _tabela(df: pd.DataFrame, periodicidade: str = "trimestral") -> pd.DataFrame:
    """(date x setor x medida) -> valor, para uma duracao e periodicidade."""
    return df[df["periodicidade"] == periodicidade]


def _validar_identidades(df: pd.DataFrame) -> dict[str, float]:
    """Produtividade = produto/horas e custo unitario = remuneracao/produtividade.

    No indice as duas sao razoes exatas; nas duas duracoes de variacao a forma certa e
    multiplicativa, NAO a subtracao que o texto do release usa (ver (3)).
    """
    piv = (_tabela(df).pivot_table(index=["date", "setor", "duracao"],
                                   columns="medida", values="valor", aggfunc="first"))
    necessarias = {"produtividade", "produto_real", "horas_trabalhadas",
                   "custo_unitario_trabalho", "remuneracao_hora"}
    faltam = necessarias - set(piv.columns)
    if faltam:
        raise RuntimeError(f"medidas ausentes para as identidades: {sorted(faltam)}")

    piores: dict[str, float] = {}
    for duracao in ("indice", "tri_anual", "ano_a_ano"):
        p = piv.xs(duracao, level="duracao")
        if duracao == "indice":
            e1 = (p["produtividade"] - p["produto_real"] / p["horas_trabalhadas"] * 100).abs()
            e2 = (p["custo_unitario_trabalho"]
                  - p["remuneracao_hora"] / p["produtividade"] * 100).abs()
            tol = _TOL_INDICE
        else:
            def cresc(a, b):
                return ((1 + a / 100) / (1 + b / 100) - 1) * 100
            e1 = (p["produtividade"] - cresc(p["produto_real"], p["horas_trabalhadas"])).abs()
            e2 = (p["custo_unitario_trabalho"]
                  - cresc(p["remuneracao_hora"], p["produtividade"])).abs()
            tol = _TOL_VARIACAO
        for nome, err in (("prod=produto/horas", e1), ("cut=remun/prod", e2)):
            err = err.dropna()
            if err.empty:
                raise RuntimeError(f"{duracao}/{nome}: nenhuma observacao para conferir")
            pior = float(err.max())
            piores[f"{duracao}:{nome}"] = pior
            if pior > tol:
                onde = err.idxmax()
                raise RuntimeError(
                    f"identidade {nome} nao fecha em {duracao}: erro maximo {pior:.3f} "
                    f"(> {tol}) em {onde}. As series nao sao as que os slugs dizem."
                )
    return piores


def _validar_anual(df: pd.DataFrame) -> int:
    """No Q05 as duas duracoes de variacao tem o mesmo valor (ver (1))."""
    a = _tabela(df, "anual")
    piv = a.pivot_table(index=["date", "setor", "medida"], columns="duracao",
                        values="valor", aggfunc="first")
    if "tri_anual" not in piv.columns or "ano_a_ano" not in piv.columns:
        raise RuntimeError("media anual sem as duas duracoes de variacao")
    par = piv[["tri_anual", "ano_a_ano"]].dropna()
    dif = (par["tri_anual"] - par["ano_a_ano"]).abs()
    if float(dif.max()) > 1e-9:
        onde = dif.idxmax()
        raise RuntimeError(
            f"na media anual as duracoes 1 e 2 deveriam coincidir; diferem "
            f"{float(dif.max()):.3f} em {onde}"
        )
    return len(par)


def _validar_horizonte(df: pd.DataFrame) -> None:
    """A media anual existe so para anos completos, e o ultimo trimestre manda."""
    tri, ano = _tabela(df), _tabela(df, "anual")
    ultimo_tri, ultimo_ano = tri["date"].max(), ano["date"].max()
    if ultimo_ano.year >= ultimo_tri.year and ultimo_tri.month > 1:
        raise RuntimeError(
            f"media anual de {ultimo_ano.year} publicada com o ano incompleto "
            f"(ultimo trimestre {ultimo_tri.date()}). MAX(date) deixaria de ser o "
            "ultimo trimestre e a checagem de frescor do calendario passaria a mentir."
        )
    if df["date"].max() != ultimo_tri:
        raise RuntimeError(
            f"MAX(date) da tabela ({df['date'].max().date()}) nao e o ultimo trimestre "
            f"({ultimo_tri.date()})"
        )


def _conferir_api(bls: BLS, df: pd.DataFrame) -> tuple[int, float]:
    """Confere uma amostra do arquivo contra a API — vintages independentes."""
    ids = sorted({
        f"PRS{cod}{'6' if classe == 'todos' else '3'}{med}{dur}"
        for cod, (_, _, classe, _) in _SETORES.items()
        for med in _AMOSTRA_MEDIDAS
        for dur in ("1", "2", "3")
    })
    fim = int(df["date"].max().year)
    api = bls.get_series(ids, start_year=fim - 2, end_year=fim, strict=False)
    if api.empty:
        raise RuntimeError("a API do BLS nao devolveu nenhuma serie de `pr`")
    api = api[api["period"].isin({"Q01", "Q02", "Q03", "Q04"})]
    api["date"] = pd.to_datetime(api["date"])

    arq = _tabela(df)[["date", "series_id", "valor"]]
    j = api.merge(arq, on=["date", "series_id"], how="inner")
    if j.empty:
        raise RuntimeError(
            "nenhuma celula em comum entre a API e o arquivo — a conferencia de "
            "vintage nao rodou, o que a torna inutil em vez de aprovada"
        )
    dif = (j["value"] - j["valor"]).abs()
    pior = float(dif.max())
    if pior > _TOL_API:
        onde = j.loc[dif.idxmax()]
        raise RuntimeError(
            f"arquivo e API discordam em {pior:.4f} ({onde['series_id']} em "
            f"{onde['date'].date()}: {onde['valor']} vs {onde['value']}). Um dos dois "
            "e de outro vintage."
        )
    return len(j), pior


def run(desde: int | None = None) -> pd.DataFrame:
    """Carrega produtividade e custos por setor maior.

    Args:
        desde: primeiro ano. Default 1947, o inicio da serie. O arquivo vem inteiro
               numa requisicao, entao janela curta nao economiza download -- ela existe
               so para recarga parcial.

    Returns:
        As linhas gravadas.
    """
    bls = BLS()
    print(f"{_TABLE}: BLS/MSPC (release prod2), {len(_SETORES)} setores x "
          f"{len(set(_MEDIDAS.values()))} medidas x {len(_DURACOES)} duracoes")

    cat = _catalogo(bls)
    print(f"  catalogo: {len(cat)} series, ids conferidos contra pr.series")

    bruto = _ler_arquivo(bls)
    df = _montar(bruto, cat)
    if desde is not None:
        df = df[df["date"].dt.year >= int(desde)]
    if df.empty:
        raise RuntimeError("nenhuma linha para gravar")

    piores = _validar_identidades(df)
    n_anual = _validar_anual(df)
    _validar_horizonte(df)
    print("  identidades fecham — pior residuo por duracao: "
          + " · ".join(f"{k.split(':')[0]} {v:.3f}"
                       for k, v in piores.items() if k.endswith("prod=produto/horas")))
    print(f"  media anual: {n_anual} celulas com as duas duracoes coincidindo")

    n_api, pior_api = _conferir_api(bls, df)
    print(f"  API confere o arquivo em {n_api} celulas (dif. maxima {pior_api:.4f})")

    tri = _tabela(df)
    print(f"  {len(df):,} linhas ({len(tri):,} trimestrais, {len(df) - len(tri):,} anuais), "
          f"{df['series_id'].nunique()} series, {tri['date'].min().date()} -> "
          f"{tri['date'].max().date()}")
    print(f"  {int(df['revisado'].sum())} celulas marcadas r=revised nesta divulgacao")
    gravar(_DATABASE, _TABLE, df, sonda="setor")
    return df


if __name__ == "__main__":
    run()
