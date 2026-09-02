"""
As tres arvores do JOLTS: industria, tamanho de estabelecimento e regiao.

--------------------------------------------------------------------------------
POR QUE TRES CORTES E NAO UM
--------------------------------------------------------------------------------
O JOLTS nao publica um cubo. Cada eixo existe SO no total do outro, e o release diz
isso em nota de pe de tabela ("Establishment size class data are produced for the
total private sector only"). Conferido no proprio catalogo de series (`jt.series`,
2.060 series):

    industria   28 industrias  x  estado 00  x  tamanho 00
    tamanho      6 classes     x  estado 00  x  industria 100000  <- Total PRIVATE
    regiao       4 regioes     x  tamanho 00 x  industria 000000  <- Total nonfarm

**A raiz do corte de tamanho e Total private, nao Total nonfarm.** A diferenca nao e
cosmetica: em jul/2026 sao 6.461 mil vagas contra 7.271 mil, 810 mil de governo que
o corte de tamanho simplesmente nao cobre. Uma arvore que pendurasse as 6 classes em
Total nonfarm nao fecharia por exatamente esse tanto -- e "nao fecha por 11%" e o
tipo de erro que passa por plausivel num grafico. Por isso `industry_code`,
`state_code` e `sizeclass_code` sao COLUNAS desta tabela: cada linha carrega os tres
componentes com que o `series_id` dela e montado, o que torna a afirmacao acima
verificavel em vez de documentada.

Os ESTADOS ficaram fora de proposito: existem 51 no catalogo, mas todos terminam em
**2025-M12** -- o BLS parou de publicar a serie estadual. Entrariam como historico
morto num relatorio de dado corrente. `jt.state` continua listando os 51, entao a
ausencia aqui e decisao, nao lacuna: ver `_CORTES`.

--------------------------------------------------------------------------------
COMO O PAI E DERIVADO (o BLS nao publica parentesco)
--------------------------------------------------------------------------------
`jt.industry` traz `display_level` (0-3) e `sort_sequence`, e nenhuma coluna de pai --
mesma situacao do `cu.item` do CPI. O pai e o registro anterior, na ordem de
`sort_sequence`, com `display_level` um a menos. A regra so e valida se a ordem
publicada for uma travessia em profundidade da arvore, e e ela que a validacao abaixo
confere -- indiretamente, mas de forma que uma re-indentacao nao sobrevive.

--------------------------------------------------------------------------------
O QUE A VALIDACAO CONFERE (e se recusa a gravar)
--------------------------------------------------------------------------------
Aditividade dos NIVEIS, nos tres cortes, nas 6 medidas, nos 2 ajustes, em toda a
historia (2000-12 -> hoje). Medido: 33.264 checagens na arvore de industria mais
3.696 nos outros dois cortes, residuo maximo **3 mil vagas** num total de 7,3
milhoes.

A tolerancia nao e um epsilon a dedo: o BLS publica cada nivel arredondado ao milhar,
entao a soma de k filhos contra um pai arredondado pode diferir de ate
`0,5 * (k + 1)` so por arredondamento. Um pai de 10 filhos admite 5,5; o pior caso
medido usa 3 desses 5,5. Trocar uma industria de pai move centenas de milhares e nao
passa.

**As TAXAS nao entram na validacao, e nao e omissao.** Elas sao razoes contra o
emprego da propria industria (vagas / (emprego + vagas); as outras cinco /
emprego), e razoes de bases diferentes nao somam. O relatorio precisa saber disso
-- e por isso a coluna `agregavel` existe: ela responde "esta linha pode ser somada
com as irmas?" para quem le a tabela, em vez de deixar a resposta implicita no tipo
de medida.

--------------------------------------------------------------------------------
DDL
--------------------------------------------------------------------------------
  CREATE TABLE macro_us.mt_jolts_dim (
      corte           VARCHAR(10)  NOT NULL,   -- industria | tamanho | regiao
      categoria       VARCHAR(8)   NOT NULL,   -- codigo dentro do corte
      nome            VARCHAR(90)  NOT NULL,   -- rotulo oficial do BLS
      nome_curto      VARCHAR(40)  NOT NULL,   -- rotulo de linha/legenda
      nivel           TINYINT      NOT NULL,   -- profundidade (0 = raiz do corte)
      pai             VARCHAR(8),
      n_filhos        SMALLINT     NOT NULL,
      is_leaf         TINYINT      NOT NULL,
      agregavel       TINYINT      NOT NULL,   -- filhos somam o pai (niveis)?
      ordem           SMALLINT     NOT NULL,
      caminho         VARCHAR(400) NOT NULL,
      industry_code   VARCHAR(6)   NOT NULL,   -- os 3 componentes do series_id
      state_code      VARCHAR(2)   NOT NULL,
      sizeclass_code  VARCHAR(2)   NOT NULL,
      inicio          VARCHAR(7),              -- medido do dado, YYYY-MM
      fim             VARCHAR(7),
      PRIMARY KEY (corte, categoria),
      KEY idx_pai (corte, pai)
  );

Banco: macro_us.mt_jolts_dim -- PRIMARY KEY (corte, categoria)
"""

from __future__ import annotations

import pandas as pd

from connectors.bls import BLS
from domain.db.us._gravar import gravar

_DATABASE = "macro_us"
_TABLE = "mt_jolts_dim"

_SURVEY = "jt"
_ARQUIVO_DADOS = "jt.data.1.AllItems"

# As 6 medidas de fluxo/estoque do release. UO (vagas por desempregado) e R1/R2
# (taxas de resposta da pesquisa) ficam de fora daqui de proposito: UO e uma razao
# entre duas pesquisas e nao pertence a nenhuma arvore aditiva; R1/R2 sao metrica de
# qualidade da coleta, nao dado economico.
MEDIDAS = ("JO", "HI", "TS", "QU", "LD", "OS")

# Definicao de cada corte. `industry`/`state`/`size` sao os componentes FIXOS do
# series_id; o componente que varia e o que da a `categoria` de cada linha.
#
# Estados nao estao aqui: as 51 series terminam em 2025-M12 (BLS descontinuou).
_CORTES = {
    "industria": {"varia": "industry", "state": "00", "size": "00"},
    "tamanho": {"varia": "size", "industry": "100000", "state": "00"},
    "regiao": {"varia": "state", "industry": "000000", "size": "00"},
}

# Rotulo curto por codigo de industria. Existe porque o nome oficial do BLS estoura
# qualquer celula de tabela e qualquer legenda de grafico ("State and local
# government, excluding education" tem 47 caracteres). O nome oficial vive na coluna
# `nome` e o relatorio o mostra no cartao de definicao -- so quando difere deste.
_CURTO_INDUSTRIA = {
    "000000": "Total nonfarm",
    "100000": "Total private",
    "110099": "Mining & logging",
    "230000": "Construction",
    "300000": "Manufacturing",
    "320000": "Durable goods",
    "340000": "Nondurable goods",
    "400000": "Trade, transp. & utilities",
    "420000": "Wholesale trade",
    "440000": "Retail trade",
    "480099": "Transp., warehousing & util.",
    "510000": "Information",
    "510099": "Financial activities",
    "520000": "Finance & insurance",
    "530000": "Real estate & leasing",
    "540099": "Prof. & business services",
    "600000": "Private educ. & health",
    "610000": "Private educational svcs",
    "620000": "Health care & social asst.",
    "700000": "Leisure & hospitality",
    "710000": "Arts, entert. & recreation",
    "720000": "Accommodation & food svcs",
    "810000": "Other services",
    "900000": "Government",
    "910000": "Federal",
    "920000": "State & local",
    "923000": "State & local education",
    "929000": "State & local, ex-education",
}

# A raiz do corte de tamanho. O BLS chama o codigo '00' de "All size classes", que
# omite o fato que muda o numero: o corte cobre SO o setor privado.
_RAIZ_TAMANHO = ("Total private, all size classes", "Total private")

_CURTO_REGIAO = {
    "00": "Total US",
    "NE": "Northeast",
    "SO": "South",
    "MW": "Midwest",
    "WE": "West",
}

_ORDEM_REGIAO = ["00", "NE", "SO", "MW", "WE"]


def series_id(
    industry: str,
    state: str,
    size: str,
    medida: str,
    ratelevel: str,
    ajuste: str,
) -> str:
    """Monta um series_id do JOLTS.

    O layout tem largura fixa e nenhum separador, e errar a contagem de zeros
    devolve `None` em vez de erro -- foi o que aconteceu na primeira tentativa de
    conferir a Tabela A (168 celulas "divergentes", todas por um id de 19 caracteres
    onde o BLS usa 21):

        JT | S/U | industria(6) | estado(2) | area(5) | tamanho(2) | medida(2) | L/R

    Args:
        industry:  codigo de 6 digitos de `jt.industry`.
        state:     '00' (nacional), 'NE'/'SO'/'MW'/'WE' (regiao) ou FIPS de estado.
        size:      '00' (todas) ou '01'-'06'.
        medida:    JO | HI | TS | QU | LD | OS | UO.
        ratelevel: 'L' (nivel, em milhares) ou 'R' (taxa, em %).
        ajuste:    'sa' ou 'nsa'.

    Returns:
        O id de 21 caracteres.
    """
    seas = "S" if ajuste.lower() == "sa" else "U"
    sid = f"JT{seas}{industry}{state}00000{size}{medida}{ratelevel}"
    if len(sid) != 21:
        raise ValueError(f"series_id com {len(sid)} caracteres, esperado 21: {sid!r}")
    return sid


def _arvore_industria(bls: BLS) -> pd.DataFrame:
    """A arvore de industrias, com o pai derivado de display_level + sort_sequence."""
    ind = bls.read_flat_table(_SURVEY, f"{_SURVEY}.industry")
    ind["display_level"] = ind["display_level"].astype(int)
    ind["sort_sequence"] = ind["sort_sequence"].astype(int)
    ind = ind.sort_values("sort_sequence").reset_index(drop=True)

    faltando = sorted(set(ind["industry_code"]) - set(_CURTO_INDUSTRIA))
    if faltando:
        raise RuntimeError(
            f"jt.industry trouxe {len(faltando)} codigos sem rotulo curto em "
            f"_CURTO_INDUSTRIA: {faltando}. O BLS mudou a lista de industrias -- "
            "acrescente o rotulo em vez de deixar a tabela cair no nome oficial, "
            "que estoura a celula."
        )

    pais, ultimo_por_nivel = [], {}
    for _, r in ind.iterrows():
        nivel = r["display_level"]
        pais.append(ultimo_por_nivel.get(nivel - 1))
        ultimo_por_nivel[nivel] = r["industry_code"]

    return pd.DataFrame({
        "corte": "industria",
        "categoria": ind["industry_code"],
        "nome": ind["industry_text"],
        "nome_curto": [_CURTO_INDUSTRIA[c] for c in ind["industry_code"]],
        "nivel": ind["display_level"],
        "pai": pais,
        "ordem": ind["sort_sequence"],
        "industry_code": ind["industry_code"],
        "state_code": "00",
        "sizeclass_code": "00",
    })


def _arvore_tamanho(bls: BLS) -> pd.DataFrame:
    """As 6 classes de tamanho, penduradas em Total private."""
    sz = bls.read_flat_table(_SURVEY, f"{_SURVEY}.sizeclass")
    sz["display_level"] = sz["display_level"].astype(int)
    sz["sort_sequence"] = sz["sort_sequence"].astype(int)
    sz = sz.sort_values("sort_sequence").reset_index(drop=True)

    nomes, curtos = [], []
    for code, texto in zip(sz["sizeclass_code"], sz["sizeclass_text"]):
        if code == "00":
            nomes.append(_RAIZ_TAMANHO[0])
            curtos.append(_RAIZ_TAMANHO[1])
        else:
            nomes.append(texto)
            curtos.append(texto.replace(" employees", ""))

    return pd.DataFrame({
        "corte": "tamanho",
        "categoria": sz["sizeclass_code"],
        "nome": nomes,
        "nome_curto": curtos,
        "nivel": sz["display_level"],
        "pai": [None if c == "00" else "00" for c in sz["sizeclass_code"]],
        "ordem": sz["sort_sequence"],
        "industry_code": "100000",
        "state_code": "00",
        "sizeclass_code": sz["sizeclass_code"],
    })


def _arvore_regiao(bls: BLS) -> pd.DataFrame:
    """As 4 regioes, penduradas em Total US. Os 51 estados ficam fora (ver docstring)."""
    st = bls.read_flat_table(_SURVEY, f"{_SURVEY}.state")
    st = st.set_index("state_code")

    nomes = []
    for code in _ORDEM_REGIAO:
        if code not in st.index:
            raise RuntimeError(
                f"jt.state nao traz mais o codigo {code!r} -- o BLS mudou a lista de "
                "regioes."
            )
        nomes.append("Total US" if code == "00" else st.loc[code, "state_text"])

    return pd.DataFrame({
        "corte": "regiao",
        "categoria": _ORDEM_REGIAO,
        "nome": nomes,
        "nome_curto": [_CURTO_REGIAO[c] for c in _ORDEM_REGIAO],
        "nivel": [0] + [1] * 4,
        "pai": [None] + ["00"] * 4,
        "ordem": range(1, len(_ORDEM_REGIAO) + 1),
        "industry_code": "000000",
        "state_code": _ORDEM_REGIAO,
        "sizeclass_code": "00",
    })


def _caminho(df: pd.DataFrame) -> list[str]:
    """Caminho ' > ' da raiz do corte ate cada linha."""
    por_chave = {(r["corte"], r["categoria"]): r for _, r in df.iterrows()}
    saida = []
    for _, r in df.iterrows():
        partes, atual = [], r
        visto = set()
        while atual is not None:
            chave = (atual["corte"], atual["categoria"])
            if chave in visto:
                raise RuntimeError(f"ciclo na arvore em {chave}")
            visto.add(chave)
            partes.append(atual["nome_curto"])
            pai = atual["pai"]
            atual = por_chave.get((r["corte"], pai)) if pai else None
        saida.append(" > ".join(reversed(partes)))
    return saida


def _validar_aditividade(dim: pd.DataFrame, dados: pd.DataFrame) -> dict:
    """Confere que os filhos somam o pai, em NIVEL, em toda a historia.

    Levanta se qualquer pai estourar `0,5 * (n_filhos + 1)` -- o limite que o
    arredondamento ao milhar do BLS admite, e nada alem dele.

    Returns:
        Resumo com numero de checagens e o pior residuo (para o log).
    """
    # Uma matriz data x series_id. O pivot e feito UMA vez: fatiar `dados` por
    # series_id dentro do laco custaria uma varredura de 600 mil linhas por serie.
    largo = dados.pivot_table(index="date", columns="series_id", values="value")
    total_checagens, pior, pior_ctx = 0, 0.0, None

    for corte, sub in dim.groupby("corte", sort=False):
        por_cat = sub.set_index("categoria")
        for ajuste in ("sa", "nsa"):
            for medida in MEDIDAS:
                col = {}
                for cat, r in por_cat.iterrows():
                    sid = series_id(
                        r["industry_code"], r["state_code"], r["sizeclass_code"],
                        medida, "L", ajuste,
                    )
                    if sid in largo.columns:
                        col[cat] = largo[sid]
                if not col:
                    continue
                painel = pd.DataFrame(col)

                for cat, r in por_cat.iterrows():
                    filhos = [c for c in por_cat.index[por_cat["pai"] == cat]
                              if c in painel.columns]
                    if not filhos or cat not in painel.columns:
                        continue
                    soma = painel[filhos].sum(axis=1, min_count=len(filhos))
                    resid = (soma - painel[cat]).abs().dropna()
                    if resid.empty:
                        continue
                    limite = 0.5 * (len(filhos) + 1)
                    total_checagens += len(resid)
                    if resid.max() > limite:
                        raise RuntimeError(
                            f"aditividade quebrada em {corte}/{cat} ({medida}, {ajuste}): "
                            f"residuo maximo {resid.max():.3f} mil contra limite de "
                            f"arredondamento {limite:.1f}. Isto nao e arredondamento -- "
                            "e o BLS tendo mudado o parentesco publicado, ou a derivacao "
                            "de pai por display_level + sort_sequence ter deixado de valer."
                        )
                    if resid.max() > pior:
                        pior, pior_ctx = resid.max(), f"{corte}/{cat} {medida} {ajuste}"

    return {"checagens": total_checagens, "pior": pior, "contexto": pior_ctx}


def _cobertura(dim: pd.DataFrame, dados: pd.DataFrame) -> pd.DataFrame:
    """Preenche inicio/fim (YYYY-MM) medidos do dado, por linha da dim."""
    obs = dados.dropna(subset=["value"]).copy()
    obs["ym"] = obs["date"].dt.strftime("%Y-%m")
    por_serie = obs.groupby("series_id")["ym"].agg(["min", "max"])

    inicios, fins = [], []
    for _, r in dim.iterrows():
        janelas = []
        for ajuste in ("sa", "nsa"):
            for medida in MEDIDAS:
                for rl in ("L", "R"):
                    sid = series_id(
                        r["industry_code"], r["state_code"], r["sizeclass_code"],
                        medida, rl, ajuste,
                    )
                    if sid in por_serie.index:
                        janelas.append((por_serie.loc[sid, "min"], por_serie.loc[sid, "max"]))
        inicios.append(min(j[0] for j in janelas) if janelas else None)
        fins.append(max(j[1] for j in janelas) if janelas else None)

    dim = dim.copy()
    dim["inicio"], dim["fim"] = inicios, fins
    return dim


def montar(bls: BLS | None = None, dados: pd.DataFrame | None = None) -> pd.DataFrame:
    """Monta e valida as tres arvores, sem gravar.

    Args:
        bls:   connector (criado se ausente).
        dados: `jt.data.1.AllItems` ja lido, para a validacao de aditividade e a
               cobertura. Se ausente, e baixado -- 34 MB, uma requisicao, sem cota.

    Returns:
        A dim completa, pronta para gravar.
    """
    bls = bls or BLS()
    partes = [_arvore_industria(bls), _arvore_tamanho(bls), _arvore_regiao(bls)]
    dim = pd.concat(partes, ignore_index=True)

    n_filhos, is_leaf = [], []
    for _, r in dim.iterrows():
        n = int(((dim["corte"] == r["corte"]) & (dim["pai"] == r["categoria"])).sum())
        n_filhos.append(n)
        is_leaf.append(1 if n == 0 else 0)
    dim["n_filhos"], dim["is_leaf"] = n_filhos, is_leaf
    dim["agregavel"] = 1                     # niveis somam; taxas nao (ver docstring)
    dim["caminho"] = _caminho(dim)

    if dados is None:
        print("  baixando jt.data.1.AllItems para validar a arvore (34 MB, 1 requisicao)")
        dados = bls.get_data_file(_SURVEY, _ARQUIVO_DADOS)

    resumo = _validar_aditividade(dim, dados)
    print(f"  aditividade: {resumo['checagens']:,} checagens, residuo maximo "
          f"{resumo['pior']:.3f} mil ({resumo['contexto']})")

    dim = _cobertura(dim, dados)
    ordem_corte = {"industria": 0, "tamanho": 1, "regiao": 2}
    dim = dim.sort_values(
        ["corte", "ordem"], key=lambda s: s.map(ordem_corte) if s.name == "corte" else s
    ).reset_index(drop=True)

    cols = ["corte", "categoria", "nome", "nome_curto", "nivel", "pai", "n_filhos",
            "is_leaf", "agregavel", "ordem", "caminho", "industry_code", "state_code",
            "sizeclass_code", "inicio", "fim"]
    return dim[cols]


def run(dados: pd.DataFrame | None = None) -> pd.DataFrame:
    """Atualiza macro_us.mt_jolts_dim.

    Args:
        dados: `jt.data.1.AllItems` ja lido (evita baixar duas vezes quando
               `mt_jolts.run()` chama este passo).

    Returns:
        A dim gravada -- `mt_jolts.run()` a reaproveita para saber quais series
        buscar, em vez de reconstruir a lista.
    """
    print(f"{_TABLE}: montando as 3 arvores do JOLTS")
    dim = montar(dados=dados)
    for corte, sub in dim.groupby("corte", sort=False):
        print(f"  {corte}: {len(sub)} linhas, niveis {sub['nivel'].min()}-"
              f"{sub['nivel'].max()}, {sub['inicio'].min()} -> {sub['fim'].max()}")
    gravar(_DATABASE, _TABLE, dim, sonda="categoria")
    return dim


if __name__ == "__main__":
    run()
