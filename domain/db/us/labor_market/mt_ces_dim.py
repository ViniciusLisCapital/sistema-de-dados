"""
A arvore de industrias da CES (Current Employment Statistics -- o "payroll").

    from domain.db.us.labor_market import mt_ces_dim
    mt_ces_dim.run()

--------------------------------------------------------------------------------
POR QUE O PARENTESCO NAO PODE SER DERIVADO COMO NO JOLTS
--------------------------------------------------------------------------------
`ce.industry` traz `display_level` (0-7) e `sort_sequence` e nenhuma coluna de pai --
mesma situacao do `jt.industry` e do `cu.item`. La a regra "o pai e o registro
anterior com display_level um a menos" bastou. Aqui ela produz uma arvore ERRADA, e
nao de leve:

**Os 4 nos de display_level 1 sao agregados que se SOBREPOEM.** Total private,
Goods-producing, Service-providing e Private service-providing somados dao **257% do
total nonfarm** (medido, jul/2026). Nenhum deles particiona nada em relacao aos
outros: Total private = Goods-producing + Private service-providing, e
Service-providing = Private service-providing + Government. Alem disso, a regra
ingenua faria 'Mining and logging' (nivel 2) herdar 'Private service-providing' --
o nivel-1 imediatamente anterior no sort --, o que poe mineracao dentro de servicos.

Por isso o topo e DECLARADO (`_TOPO`) e ha uma tabela pequena de correcoes
(`_CORRECOES`), **cada uma conferida numericamente pelo proprio loader**: a declaracao
diz o que se afirma, e `_validar_correcoes()` refaz a conta e levanta se a identidade
deixar de valer. Uma re-indentacao do BLS nao sobrevive em silencio.

    Total nonfarm
    |- Total private
    |  |- Goods-producing            (todo privado)
    |  |  |- Mining and logging / Construction / Manufacturing
    |  \- Private service-providing
    |     \- os 7 supersetores de servico privado
    \- Government

'Service-providing' fica FORA da arvore (`alternativo = 1`): ele atravessa a fronteira
de Total private, exatamente o mesmo defeito que a linha "Empr./Tit. LP Externo" tinha
na arvore do balanco de pagamentos do relatorio cambial. Continua carregado em
`mt_ces` -- o que sai e a posicao na hierarquia, nao o dado.

--------------------------------------------------------------------------------
O SEGUNDO EIXO: RESIDENCIAL x NAO-RESIDENCIAL NA CONSTRUCAO
--------------------------------------------------------------------------------
A CES publica os contratantes de servicos especializados (NAICS 238) por subsetor
NAICS **e**, em paralelo, divididos em residencial e nao-residencial. Os dois cortes
fecham no mesmo pai (238 = 2381+2382+2383+2389 e 238 = Residencial + Nao-residencial,
este exato em 307 meses), o que faz deles dois EIXOS e nao dois niveis. Misturar os
dois numa arvore so seria dupla contagem -- as barras empilhadas somariam 163% do pai.
Os 10 nos `part 238*` ficam `alternativo = 1`.

--------------------------------------------------------------------------------
AS 4 CORRECOES QUE A INDENTACAO DO BLS NAO DA
--------------------------------------------------------------------------------
1. **'Health care' (621,2,3)** aparece como IRMAO de Ambulatory (621), Hospitals (622)
   e Nursing (623), quando e a soma dos tres -- exata, 439 meses, diferenca 0,00. Vira
   pai deles, o que transforma 177% de sobreposicao em dois niveis que fecham.
2. **'Motor vehicles and parts' (3361,2,3)** idem, sobre 3361/3362/3363 (438 meses,
   diferenca maxima 5,4 mil num agregado de ~1 milhao -- arredondamento do detalhe a
   uma decimal, ver a tolerancia abaixo).
3. **'Other Federal government'** esta indentado sob 'U.S. Postal Service', e nao e
   dele: USPS = 603 mil e 'Other Federal' = 1.256 mil, o filho seria o dobro do pai.
   Ele pertence a 'Federal, except U.S. Postal Service', onde a identidade fecha
   (hospitais + DoD + outros = 2.083,0 contra 2.082,9 publicados).
4. **'Investment banking and securities intermediation' (52315)** e impresso com
   display_level 6 ANTES do seu pai de nivel 5 ('Securities and commodity contracts
   brokerage', 5231,2) -- a unica inversao de ordem da arvore. Pela indentacao ele
   sobe um nivel e produz 139% de sobreposicao; pelo NAICS (52315 e prefixado por
   5231) o lugar e claro.

--------------------------------------------------------------------------------
A ARVORE E VALIDADA NO DADO **SEM AJUSTE SAZONAL**, E ISSO NAO E DETALHE
--------------------------------------------------------------------------------
O BLS dessazonaliza cada serie de forma INDEPENDENTE, e o proprio release avisa
("Detail ... will not necessarily add to totals because of the independent seasonal
adjustment of the various series"). Medido nos 284 pais desta arvore:

    sem ajuste (NSA)   pior excesso dos filhos sobre o pai:  +0,068%   (1 pai > 0,05%)
    com ajuste (SA)    pior excesso:                        +15,475%   (222 pais > 0,05%)

Ou seja: **a aditividade e uma garantia de construcao apenas no dado bruto.** Validar
a arvore no SA reprovaria uma arvore correta -- foi o que aconteceu na primeira
execucao, com 12 pais "sobrepostos" em 100,3%-101,7% que nao tinham nada de errado.

No SA a aditividade e *imposta* pelo BLS no topo (niveis 0-2 fecham exatos) e fica
livre no detalhe. Por isso a validacao roda no NSA e o desvio do SA e **medido e
gravado** (`desvio_sa`), para o relatorio poder dizer o tamanho do erro em vez de
sugerir que a pilha soma exatamente.

--------------------------------------------------------------------------------
O QUE A VALIDACAO CONFERE (e se recusa a gravar)
--------------------------------------------------------------------------------
- **Nenhum pai pode ter filhos que somem MAIS que ele no NSA** (alem da tolerancia).
  E o guarda que pega um eixo alternativo novo: sobreposicao no bruto e sempre erro
  de arvore.
- Cada uma das 3 identidades que autorizam as correcoes, refeita nos dados.
- Uma raiz so, e nenhum ciclo no caminho.
- A tolerancia tem duas metades: o BLS publica os agregados em milhar inteiro e o
  detalhe com uma decimal, entao k filhos contra um pai arredondado admitem
  `0,5 x (k+1)` (mesma conta do JOLTS); e um piso relativo de 0,1% cobre as revisoes
  historicas de series longas, onde o absoluto sozinho e apertado demais.

**Cobertura incompleta NAO e erro** e por isso e uma COLUNA, nao uma excecao. Medido:
260 dos 284 pais fecham em todos os meses, e os 24 que nao fecham estao todos nos
niveis 4-6 -- detalhe que a CES publica so em parte. Num mes COMPLETO as 555 folhas
somam **97,8% do total nonfarm** (jun/2026, tanto NSA quanto SA). `agregavel` diz se
os filhos fecham sempre, `cobertura` guarda a fracao do ultimo mes e `desvio_sa` o
pior desvio relativo no dado dessazonalizado -- para o relatorio dizer o numero em vez
de sugerir uma particao que nao existe.

O "mes completo" da frase acima e o que a borda irregular (ver `mt_ces.py`) obriga a
distinguir: no mes mais recente **so 27 das 555 folhas tem dado**, e a soma delas da
16% do total. Nao e cobertura ruim, e detalhe que ainda nao saiu.

--------------------------------------------------------------------------------
DDL
--------------------------------------------------------------------------------
    CREATE TABLE mt_ces_dim (
        categoria      VARCHAR(8)   NOT NULL COMMENT 'industry_code da CES (8 digitos)',
        nome           VARCHAR(255) NOT NULL COMMENT 'industry_name publicado pelo BLS',
        nome_curto     VARCHAR(80)  NOT NULL COMMENT 'rotulo curto para tabela e legenda',
        naics          VARCHAR(20)  NULL     COMMENT 'naics_code do BLS; "-" nos agregados sem NAICS',
        nivel          TINYINT      NOT NULL COMMENT 'display_level do BLS (0=Total nonfarm)',
        pai            VARCHAR(8)   NULL     COMMENT 'categoria do pai; NULL na raiz',
        n_filhos       SMALLINT     NOT NULL COMMENT 'filhos diretos na arvore',
        is_leaf        TINYINT      NOT NULL COMMENT '1 se nao tem filho',
        agregavel      TINYINT      NOT NULL COMMENT '1 se os filhos somam o pai em TODOS os meses',
        cobertura      DECIMAL(8,4) NULL     COMMENT '% do pai que os filhos cobrem no ultimo mes (NSA)',
        desvio_sa      DECIMAL(8,4) NULL     COMMENT 'pior |filhos-pai|/pai no dado SA, em %',
        alternativo    TINYINT      NOT NULL COMMENT '1 = agregacao alternativa, fora da arvore',
        tem_horas      TINYINT      NOT NULL COMMENT '1 se a industria tem serie de horas/ganhos',
        ordem          SMALLINT     NOT NULL COMMENT 'sort_sequence do BLS',
        caminho        VARCHAR(255) NOT NULL COMMENT 'categorias da raiz ate aqui, separadas por >',
        inicio         DATE         NULL     COMMENT 'primeiro mes com emprego publicado',
        fim            DATE         NULL     COMMENT 'ultimo mes com emprego publicado',
        PRIMARY KEY (categoria)
    ) COMMENT 'Arvore de industrias da CES/BLS (payroll). Topo declarado: os 4 nos de
               display_level 1 se sobrepoem (257% do total). Ver o docstring do modulo.'
"""

from __future__ import annotations

import pandas as pd

from connectors.bls import BLS
from domain.db.us._gravar import gravar

_DATABASE = "macro_us"
_TABLE = "mt_ces_dim"

# ── o topo, declarado ────────────────────────────────────────────────────────
# Os 4 nos de display_level 1 nao particionam nada entre si (257% do total nonfarm).
_TOPO = {
    "00000000": None,          # Total nonfarm
    "05000000": "00000000",    # Total private
    "06000000": "05000000",    # Goods-producing -- todo privado
    "08000000": "05000000",    # Private service-providing
    "90000000": "00000000",    # Government
}
_BENS = {"10000000", "20000000", "30000000"}
_SERV_PRIV = {"40000000", "50000000", "55000000", "60000000",
              "65000000", "70000000", "80000000"}

# ── agregacoes alternativas: ficam fora da arvore ────────────────────────────
# 07: Service-providing = Private service-providing + Government, atravessa Total private.
# 202380xx: o corte residencial/nao-residencial de NAICS 238, um segundo EIXO.
_ALTERNATIVOS = {"07000000"} | {
    "20238001", "20238002", "20238101", "20238102", "20238201",
    "20238202", "20238301", "20238302", "20238901", "20238902",
}

# ── correcoes ao parentesco derivado, cada uma com a identidade que a prova ──
# `filho -> pai`. `_validar_correcoes()` refaz a conta e levanta se parar de valer.
_CORRECOES = {
    # 'Health care' (621,2,3) e a soma de 621+622+623, nao irma deles.
    "65621000": "65620001",
    "65622000": "65620001",
    "65623000": "65620001",
    # 'Motor vehicles and parts' (3361,2,3) idem sobre 3361/3362/3363.
    "31336100": "31336001",
    "31336200": "31336001",
    "31336300": "31336001",
    # 'Other Federal government' esta indentado sob USPS e e de 'Federal, except USPS'.
    "90919999": "90911000",
    # 'Investment banking' (52315) e impresso ANTES do seu pai de nivel 5 (5231,2).
    "55523150": "55523200",
}
# As identidades que autorizam as correcoes: pai -> filhos que devem soma-lo.
_IDENTIDADES = {
    "65620001": ["65621000", "65622000", "65623000"],
    "31336001": ["31336100", "31336200", "31336300"],
    "90911000": ["90916220", "90919110", "90919999"],
}
# A tolerancia tem duas metades. A absoluta e o arredondamento da fonte:
# `0,5 x (k+1)` para k filhos contra um pai arredondado ao milhar. A relativa cobre as
# revisoes historicas de series de 80 anos, onde a absoluta e apertada demais -- 'Motor
# vehicles and parts' fecha com 5,4 mil de folga em algum mes de um agregado de ~1
# milhao, e a afirmacao que interessa e "a identidade e estrutural", nao "fecha ao
# milhar em 1990".
_TOL_RELATIVA = 0.001


def _limite(pai: pd.Series, k: int) -> pd.Series:
    """Tolerancia por mes: o maior entre o piso de arredondamento e 0,1% do pai."""
    return (pai.abs() * _TOL_RELATIVA).clip(lower=0.5 * (k + 1))

# ── rotulos curtos ──────────────────────────────────────────────────────────
# Os nomes do BLS chegam a 130 caracteres ("Cutlery, handtool, ball and roller
# bearing, ..."), o que deforma tabela e legenda. O nome oficial inteiro vai para o
# cartao de definicao do relatorio; aqui fica o rotulo. Regras, em ordem:
_CURTO_EXATO = {
    "00000000": "Total nonfarm",
    "05000000": "Total private",
    "06000000": "Goods-producing",
    "07000000": "Service-providing",
    "08000000": "Private services",
    "10000000": "Mining and logging",
    "20000000": "Construction",
    "30000000": "Manufacturing",
    "31000000": "Durable goods",
    "32000000": "Nondurable goods",
    "40000000": "Trade, transport, utilities",
    "41000000": "Wholesale trade",
    "42000000": "Retail trade",
    "43000000": "Transport and warehousing",
    "44000000": "Utilities",
    "50000000": "Information",
    "55000000": "Financial activities",
    "60000000": "Professional, business svcs",
    "65000000": "Education and health",
    "70000000": "Leisure and hospitality",
    "80000000": "Other services",
    "90000000": "Government",
    "90910000": "Federal",
    "90920000": "State government",
    "90930000": "Local government",
    "65620000": "Health care, social asst.",
    "65620001": "Health care",
    "31336001": "Motor vehicles and parts",
}
# Sufixos que so repetem o ramo em que a linha ja esta.
_PODAS = (
    " manufacturing", " construction", " merchant wholesalers", " stores",
    " services", " and related activities", " establishments",
)


def _curto(codigo: str, nome: str, limite: int = 42) -> str:
    """Rotulo curto: excecao declarada, senao poda de sufixo, senao truncamento."""
    if codigo in _CURTO_EXATO:
        return _CURTO_EXATO[codigo]
    s = nome.strip()
    if len(s) <= limite:
        return s
    for suf in _PODAS:
        if s.lower().endswith(suf) and len(s) - len(suf) >= 12:
            s = s[: -len(suf)].rstrip(" ,")
            break
    if len(s) <= limite:
        return s
    # corta no separador mais tardio que cabe, para nao terminar no meio de uma palavra
    corte = s[:limite]
    for sep in (";", ",", " and ", " "):
        i = corte.rfind(sep)
        if i >= limite // 2:
            return corte[:i].rstrip(" ,;") + "..."
    return corte.rstrip() + "..."


# ── derivacao ───────────────────────────────────────────────────────────────
def _catalogo(bls: BLS) -> pd.DataFrame:
    ind = bls.read_flat_table("ce", "ce.industry")
    ind.columns = [c.strip() for c in ind.columns]
    for c in ind.columns:
        if ind[c].dtype == object:
            ind[c] = ind[c].astype(str).str.strip()
    ind["display_level"] = ind["display_level"].astype(int)
    ind["sort_sequence"] = ind["sort_sequence"].astype(int)
    return ind.sort_values("sort_sequence").reset_index(drop=True)


def _pais(ind: pd.DataFrame) -> dict[str, str | None]:
    """Parentesco: topo declarado, nivel 2 mapeado, resto por display_level."""
    pais: dict[str, str | None] = {}
    pilha: list[tuple[int, str]] = []
    for _, r in ind.iterrows():
        cod, niv = r.industry_code, r.display_level
        if cod in _ALTERNATIVOS:
            # Nao entra na arvore E nao entra na pilha: os 10 nos residencial/
            # nao-residencial ficam intercalados com os subsetores NAICS de 238, e
            # deixa-los na pilha faria 2382 herdar o no residencial de 2381.
            pais[cod] = None
            continue
        if cod in _TOPO:
            pais[cod] = _TOPO[cod]
            # A pilha TEM de ser reiniciada aqui. Sem isso 'Government' (que esta no
            # topo com display_level 2) nao a reinicia, e 'Federal' (nivel 3) herda o
            # ultimo nivel-2 anterior no sort -- 'Other services'. A cobertura daquele
            # pai vai a 485% e a do Federal a 39%, sem erro nenhum.
            pilha = [(niv, cod)]
            continue
        if niv == 2:
            pais[cod] = "06000000" if cod in _BENS else "08000000" if cod in _SERV_PRIV else None
            if pais[cod] is None:
                raise RuntimeError(
                    f"supersetor de display_level 2 sem pai declarado: {cod} "
                    f"({r.industry_name}). A CES ganhou um supersetor novo -- decida "
                    f"se ele e bens (_BENS) ou servico privado (_SERV_PRIV) antes de "
                    f"gravar, porque o default seria pendurar servico em bens."
                )
            pilha = [(2, cod)]
            continue
        while pilha and pilha[-1][0] >= niv:
            pilha.pop()
        if not pilha:
            raise RuntimeError(f"{cod} ({r.industry_name}, nivel {niv}) sem ancestral no sort")
        pais[cod] = pilha[-1][1]
        pilha.append((niv, cod))

    for filho, pai in _CORRECOES.items():
        if filho not in pais:
            raise RuntimeError(f"correcao para {filho}, que nao esta no catalogo da CES")
        pais[filho] = pai
    return pais


def _emprego(bls: BLS) -> pd.DataFrame:
    """Emprego (datatype 01) dos 18 arquivos, em (date x industry) para o SA."""
    partes = []
    for nome in [a for a in bls.list_flat_files("ce") if a.endswith(".Employment")]:
        df = bls.read_flat_table("ce", nome)
        df.columns = [c.strip() for c in df.columns]
        df["series_id"] = df["series_id"].astype(str).str.strip()
        df = df[df["series_id"].str[11:13] == "01"]
        partes.append(df[["series_id", "year", "period", "value"]])
    d = pd.concat(partes, ignore_index=True)
    d["period"] = d["period"].astype(str).str.strip()
    d = d[d["period"] != "M13"]            # M13 e a media anual, nao um mes
    d["ind"] = d["series_id"].str[3:11]
    d["seas"] = d["series_id"].str[2]
    d["date"] = d["year"].astype(str) + "-" + d["period"].str[1:] + "-01"
    d["value"] = pd.to_numeric(d["value"], errors="coerce")
    return d


def _validar_correcoes(piv: pd.DataFrame) -> None:
    """Refaz cada identidade que autoriza uma correcao. Levanta se parar de valer."""
    for pai, filhos in _IDENTIDADES.items():
        faltam = [f for f in [pai] + filhos if f not in piv.columns]
        if faltam:
            raise RuntimeError(f"identidade de {pai}: series ausentes {faltam}")
        j = pd.concat([piv[pai].rename("pai"),
                       piv[filhos].sum(axis=1, min_count=len(filhos)).rename("soma")],
                      axis=1).dropna()
        if j.empty:
            raise RuntimeError(f"identidade de {pai}: nenhum mes em comum")
        erro = (j["soma"] - j["pai"]).abs()
        limite = _limite(j["pai"], len(filhos))
        pior = (erro / limite).idxmax()
        if (erro > limite).any():
            raise RuntimeError(
                f"a identidade que autoriza a correcao de {pai} deixou de valer: em "
                f"{pior} os filhos {filhos} somam {j.loc[pior, 'soma']:,.1f} contra "
                f"{j.loc[pior, 'pai']:,.1f} publicados (limite {limite[pior]:,.2f}). "
                f"Sem ela o no e uma agregacao alternativa e a arvore conta duas vezes."
            )
        print(f"  ok  {pai} = soma de {len(filhos)} filhos em {len(j)} meses "
              f"(erro max {erro.max():,.2f})")


def _juntar(piv: pd.DataFrame, pai: str, filhos: list[str]) -> pd.DataFrame | None:
    """(pai, soma dos filhos) mes a mes, so onde os dois existem."""
    pres = [f for f in filhos if f in piv.columns]
    if pai not in piv.columns or not pres:
        return None
    j = pd.concat([piv[pai].rename("pai"),
                   piv[pres].sum(axis=1, min_count=len(pres)).rename("soma")],
                  axis=1).dropna()
    if j.empty:
        return None
    j.attrs["k"] = len(pres)
    return j


def _cobertura(ind: pd.DataFrame, nsa: pd.DataFrame, sa: pd.DataFrame) -> pd.DataFrame:
    """Por pai: fecha sempre no NSA? que fracao cobre? e quanto o SA desvia?

    O veredito sai do NSA porque a aditividade so e garantia de construcao no dado
    bruto -- o BLS dessazonaliza cada serie independentemente. Ver o docstring.
    """
    filhos = ind.dropna(subset=["pai"]).groupby("pai")["categoria"].apply(list).to_dict()
    linhas, sobrepostos = [], []
    for pai, fs in filhos.items():
        j = _juntar(nsa, pai, fs)
        if j is None:
            continue
        k = j.attrs["k"]
        lim = _limite(j["pai"], k)
        excesso = j["soma"] - j["pai"] - lim
        if (excesso > 0).any():
            i = excesso.idxmax()
            sobrepostos.append(
                f"{pai}: filhos somam {j.loc[i, 'soma']:,.1f} contra {j.loc[i, 'pai']:,.1f} "
                f"em {i} ({100 * j.loc[i, 'soma'] / j.loc[i, 'pai']:.2f}%)")
        ult = j.iloc[-1]
        js = _juntar(sa, pai, fs)
        desvio = None
        if js is not None:
            rel = ((js["soma"] - js["pai"]).abs() / js["pai"].abs().replace(0, pd.NA)).dropna()
            if not rel.empty:
                desvio = round(100 * float(rel.max()), 4)
        linhas.append({
            "pai": pai,
            "agregavel": int(((j["soma"] - j["pai"]).abs() <= lim).all()),
            "cobertura": round(100 * ult["soma"] / ult["pai"], 4) if ult["pai"] else None,
            "desvio_sa": desvio,
        })
    if sobrepostos:
        raise RuntimeError(
            "ha pai cujos filhos somam MAIS que ele NO DADO BRUTO -- isto e sempre erro "
            "de arvore (no SA seria esperado, porque o BLS dessazonaliza cada serie "
            "independentemente). O candidato mais provavel e uma agregacao alternativa "
            "nova: um no que e a soma dos proprios irmaos. Declare-o em _ALTERNATIVOS "
            "(se for um segundo eixo) ou em _CORRECOES + _IDENTIDADES (se for um nivel "
            "que faltava):\n  " + "\n  ".join(sobrepostos[:12])
        )
    return pd.DataFrame(linhas)


def montar(bls: BLS | None = None) -> pd.DataFrame:
    bls = bls or BLS()
    ind = _catalogo(bls)
    pais = _pais(ind)

    dados = _emprego(bls)
    nsa = (dados[dados["seas"] == "U"]
           .pivot_table(index="date", columns="ind", values="value").sort_index())
    sa = (dados[dados["seas"] == "S"]
          .pivot_table(index="date", columns="ind", values="value").sort_index())
    _validar_correcoes(nsa)

    horas = set()
    ser = bls.read_flat_table("ce", "ce.series")
    ser.columns = [c.strip() for c in ser.columns]
    for c in ("industry_code", "data_type_code"):
        ser[c] = ser[c].astype(str).str.strip()
    horas = set(ser.loc[ser["data_type_code"].isin(
        {"02", "03", "04", "11", "12", "13", "15", "16", "17", "56", "57", "58"}),
        "industry_code"])

    janela = (dados.dropna(subset=["value"]).groupby("ind")["date"].agg(["min", "max"]))

    dim = pd.DataFrame({
        "categoria": ind["industry_code"],
        "nome": ind["industry_name"],
        "naics": ind["naics_code"],
        "nivel": ind["display_level"],
        "ordem": ind["sort_sequence"],
    })
    dim["nome_curto"] = [_curto(c, n) for c, n in zip(dim["categoria"], dim["nome"])]
    dim["alternativo"] = dim["categoria"].isin(_ALTERNATIVOS).astype(int)
    dim["pai"] = dim["categoria"].map(pais)
    # Um no alternativo nao entra na arvore: nem como filho, nem como pai de ninguem.
    dim.loc[dim["alternativo"] == 1, "pai"] = None
    dim["tem_horas"] = dim["categoria"].isin(horas).astype(int)
    dim["inicio"] = dim["categoria"].map(janela["min"])
    dim["fim"] = dim["categoria"].map(janela["max"])

    arvore = dim[dim["alternativo"] == 0]
    n_filhos = arvore.dropna(subset=["pai"]).groupby("pai").size()
    dim["n_filhos"] = dim["categoria"].map(n_filhos).fillna(0).astype(int)
    dim["is_leaf"] = (dim["n_filhos"] == 0).astype(int)

    cob = _cobertura(arvore, nsa, sa)
    dim = dim.merge(cob, left_on="categoria", right_on="pai", how="left",
                    suffixes=("", "_cob")).drop(columns=["pai_cob"])
    # Folha nao tem cobertura a declarar; pai sem serie de filho tampouco.
    dim["agregavel"] = dim["agregavel"].fillna(0).astype(int)

    pai_de = dict(zip(dim["categoria"], dim["pai"]))
    def caminho(cod: str) -> str:
        cadeia, visto = [cod], {cod}
        while pai_de.get(cadeia[-1]) is not None:
            p = pai_de[cadeia[-1]]
            if p in visto:
                raise RuntimeError(f"ciclo no caminho de {cod}: {cadeia} -> {p}")
            visto.add(p)
            cadeia.append(p)
        return " > ".join(reversed(cadeia))
    dim["caminho"] = [caminho(c) for c in dim["categoria"]]

    raizes = dim[(dim["alternativo"] == 0) & dim["pai"].isna()]
    if list(raizes["categoria"]) != ["00000000"]:
        raise RuntimeError(f"a arvore tem {len(raizes)} raizes: {list(raizes['categoria'])}")

    cols = ["categoria", "nome", "nome_curto", "naics", "nivel", "pai", "n_filhos",
            "is_leaf", "agregavel", "cobertura", "desvio_sa", "alternativo", "tem_horas",
            "ordem", "caminho", "inicio", "fim"]
    return dim[cols].sort_values("ordem").reset_index(drop=True)


def run() -> pd.DataFrame:
    print(f"{_TABLE}: montando a arvore de industrias da CES")
    dim = montar()
    arv = dim[dim["alternativo"] == 0]
    print(f"  {len(dim)} industrias no catalogo, {len(arv)} na arvore, "
          f"{int(dim['alternativo'].sum())} alternativas")
    print(f"  niveis {arv['nivel'].min()}-{arv['nivel'].max()}, "
          f"{int(arv['is_leaf'].sum())} folhas, "
          f"{int(arv['tem_horas'].sum())} com horas/ganhos")
    pais = arv[arv["is_leaf"] == 0]
    print(f"  {len(pais)} pais: {int(pais['agregavel'].sum())} fecham sempre, "
          f"{len(pais) - int(pais['agregavel'].sum())} tem cobertura parcial")
    gravar(_DATABASE, _TABLE, dim, sonda="categoria")
    return dim


if __name__ == "__main__":
    run()
