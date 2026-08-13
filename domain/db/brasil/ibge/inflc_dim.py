"""
Dimensao do IPCA/IPCA-15 por subitem: Grupo/Subgrupo/Item (classificacao
BCB), marcacao de nucleo "Subjacente" (Servicos/Bens Industriais Subjacente),
classificacao Comercializavel/Nao Comercializavel, e flags de pertencimento
aos nucleos por exclusao oficiais do BC (EX-0/EX-01/EX-02/EX-03/EX-FE + os
dois subcomponentes do EX-03).

Schema macro_brasil.inflc_dim:
  PRIMARY KEY (subitem_codigo)
  Colunas: subitem_codigo VARCHAR(10) | nome VARCHAR(120) | grupo VARCHAR(60) |
           subgrupo VARCHAR(80) | item VARCHAR(150) | subjacente VARCHAR(60) |
           comercializavel VARCHAR(30) |
           nucleo_ex0 TINYINT(1) | nucleo_ex01 TINYINT(1) |
           nucleo_ex02 TINYINT(1) | nucleo_ex03 TINYINT(1) |
           nucleo_ex03_servicos TINYINT(1) | nucleo_ex03_industriais TINYINT(1) |
           nucleo_exfe TINYINT(1)

DDL:
  DROP TABLE IF EXISTS macro_brasil.inflc_dim;
  CREATE TABLE macro_brasil.inflc_dim (
      subitem_codigo           VARCHAR(10)   NOT NULL,
      nome                     VARCHAR(120)  NOT NULL,
      grupo                    VARCHAR(60),
      subgrupo                 VARCHAR(80),
      item                     VARCHAR(150),
      subjacente               VARCHAR(60),
      comercializavel          VARCHAR(30),
      nucleo_ex0               TINYINT(1),
      nucleo_ex01              TINYINT(1),
      nucleo_ex02              TINYINT(1),
      nucleo_ex03              TINYINT(1),
      nucleo_ex03_servicos     TINYINT(1),
      nucleo_ex03_industriais  TINYINT(1),
      nucleo_exfe              TINYINT(1),
      PRIMARY KEY (subitem_codigo)
  );

  -- Adicionada 2026-08 a uma tabela ja existente:
  ALTER TABLE macro_brasil.inflc_dim
      ADD COLUMN comercializavel VARCHAR(30) AFTER subjacente;

Fonte unica para Grupo/Subgrupo/Item/nucleos: analytics/inflation/data/
Vetores_NT_57.xlsx, arquivo de apoio da Nota Tecnica do Banco Central do
Brasil no 57, com uma aba por vigencia de classificacao oficial (ago99-dez05,
jan06-jun06, jul06-dez11, jan12-dez19, jan20-presente — jan91-jul99 fora de
escopo). Essas vigencias de CLASSIFICACAO sao um eixo independente das
vigencias de FETCH de dados em inflc_decomposicao.py (ex.: jan06-jun06 e uma
aba propria por refletir uma reclassificacao pontual do BC — troca de etanol
por medicamentos no grupo Monitorados, ver
analytics/inflation/referencia/RI2005-12_boxe_Alteracao_composicao_administrados_monitorados_jan2006.pdf
— nao uma atualizacao de POF) — as duas so se encontram no join por
subitem_codigo em generate_report.py.

Cada aba tem as MESMAS colunas de flag 0/1 por componente do IPCA (indice
geral/grupo/subgrupo/item/subitem), com a inclusao marcada apenas no nivel
hierarquico mais alto possivel (NT-57 Subsecao 2.1.2) — _rollup() propaga
cada flag do ancestral mais alto marcado até os subitens descendentes,
mesmo algoritmo usado desde sempre para os nucleos, agora generalizado para
Grupo/Subgrupo/Item tambem:
  - Administrados/Livres -> Grupo (rotulo final "Monitorados"/"Livres" —
    dimensao_bcb historica usava "Monitorados", NT-57 usa "Administrados"
    para o mesmo conceito; seguimos o rotulo BCB por ser o que o relatorio
    ja exibia).
  - Alimentacao no domicilio/Servicos/Bens industriais -> Subgrupo.
  - Bens nao duraveis/semiduraveis/duraveis -> Item, quando Subgrupo=Bens
    Industriais.
  - EX3 Servicos -> Item ("Servicos Subjacente"/"Servicos Ex Subjacentes"),
    quando Subgrupo=Servicos.
  - Comercializaveis/Nao comercializaveis -> `comercializavel` (rotulo
    "Comercializavel"/"Nao Comercializavel"), eixo independente de
    Grupo/Subgrupo/Item — presente e uniforme nas 5 abas 1999-hoje, ao
    contrario de "Alimentos Subjacente" (ver REGRESSAO CONHECIDA abaixo).
  - Nucleo EX-FE/EX0/EX1/EX2/EX3 + EX3 Servicos/Industriais -> flags de
    nucleo (inalterado).
Verificado por conferencia cruzada com a extinta tabela_dimensao_ipca.xlsx
(dimensao_bcb_2020, recuperada da lixeira do Windows so para validacao):
0 divergencias em Grupo (377/377, a menos do rotulo Administrados/
Monitorados), Subgrupo (340/377 — o resto e Grupo=Monitorados, sem Subgrupo
proprio), Item por durabilidade (113/113) e Item Servicos Subjacente/Ex-
Subjacente (68/68).

Item quando Subgrupo=Alimentos (estagio de processamento: in natura/semi-
elaborado/industrializado) NAO esta em Vetores_NT_57.xlsx — vem de
analytics/inflation/referencia/EE069_Atualizacoes_estrutura_ponderacao_IPCA_2020.pdf,
Tabela 5, que define essa classificacao por NOME DE ITEM (4 digitos), nao
por subitem (_ALIMENTOS_PROCESSAMENTO abaixo), com uma unica excecao
conhecida a nivel de subitem (_ALIMENTOS_EXCECAO_SUBITEM). Verificado
estavel: (a) a Tabela 4 do mesmo EE069 — lista exaustiva de mudancas de
classificacao entre as estruturas 2012-2019 e 2020 — nao tem nenhuma entrada
de processamento de alimentos; (b) os nomes de item de 4 digitos da faixa
1101-1116 sao identicos nos agregados 655/2938/1419/7060 (ago/1999-hoje,
conferido via API). Por isso o mapa e aplicado a QUALQUER vigencia, nao so
2020+.

Grupo=Monitorados nao tem Subgrupo/Item proprios em nenhuma fonte — regra
explicita (Subgrupo=Item="Monitorados").

REGRESSAO CONHECIDA: "Alimentos Subjacente" (um dos tres rotulos possiveis
de `subjacente`, ao lado de Servicos/Bens Industriais Subjacente, que TEM
fonte oficial via EX3 Servicos/EX3 Industriais) nao tem equivalente na NT-57
nem em nenhuma outra fonte encontrada — antes vinha so de ~34 subitens
escolhidos a mao na planilha manual tabela_dimensao_ipca.xlsx, hoje
descontinuada. Esse rotulo fica indisponivel — sem fallback.

TRADE-OFF CONHECIDO: como esta tabela nao tem eixo de tempo e cada subitem
recebe a classificacao da vigencia mais recente em que aparece (concat
cronologico + drop_duplicates(keep="last")), um subitem reclassificado ao
longo do tempo (ex.: a troca de etanol/medicamentos em jan/2006 citada
acima) recebe seu rotulo ATUAL para TODO o seu historico, inclusive meses em
que, na epoca, era classificado diferente. Consequencia inerente da decisao
de chave (subitem_codigo sem eixo de tempo), nao um bug.

`nome` (nome de exibicao canonico) vem de uma consulta ao vivo às arvores de
classificacao do IBGE (nao de nenhum xlsx) — ver _nomes_por_vigencia().
Percorre VIGENCIAS["IPCA"] (so IPCA — IPCA-15 e subconjunto por codigo E
nome, verificado, entao nunca introduz um codigo/nome que IPCA nao tenha) da
vigencia mais nova para a mais antiga, primeiro match vence — um subitem
descontinuado antes de 2020 ainda resolve para a grafia mais recente
disponivel.

Uso:
    uv run python -c "from domain.db.brasil.ibge.inflc_dim import run; run()"
"""

from pathlib import Path

import pandas as pd

from connectors.mysql import insert_data_into_database
from domain.db.brasil.ibge.inflc_decomposicao import VIGENCIAS, _extract_code, _ibge

_DATABASE = "macro_brasil"
_TABLE = "inflc_dim"
_DATA_DIR = Path(__file__).resolve().parents[4] / "analytics" / "inflation" / "data"
_VETORES_XLSX = _DATA_DIR / "Vetores_NT_57.xlsx"

# Ordem cronologica; jan91-jul99 fora de escopo (ver docstring do modulo).
_VETOR_SHEETS = ["ago99-dez05", "jan06-jun06", "jul06-dez11", "jan12-dez19", "jan20-presente"]

_COLS_GRUPO = ["Administrados", "Livres"]
_COLS_SUBGRUPO = ["Alimentação no domicílio", "Serviços", "Bens industriais"]
_COLS_ITEM_DURAB = ["Bens não duráveis", "Bens semiduráveis", "Bens duráveis"]
_COLS_COMERCIALIZAVEL = ["Comercializáveis", "Não comercializáveis"]
_COLS_NUCLEO = {
    "Núcleo EX-FE": "nucleo_exfe",
    "Núcleo EX0": "nucleo_ex0",
    "Núcleo EX1": "nucleo_ex01",
    "Núcleo EX2": "nucleo_ex02",
    "Núcleo EX3": "nucleo_ex03",
    "EX3 Serviços": "nucleo_ex03_servicos",
    "EX3 Industriais": "nucleo_ex03_industriais",
}
_ALL_VETOR_COLS = _COLS_GRUPO + _COLS_SUBGRUPO + _COLS_ITEM_DURAB + _COLS_COMERCIALIZAVEL + list(_COLS_NUCLEO)

# EE069 (2020), Tabela 5 — nomes de Item de 4 digitos, estaveis ago/1999-hoje
# (verificado via API contra os agregados 655/2938/1419/7060). Chave e o
# nome de ITEM real da arvore de classificacao do IBGE (confirmado via
# listar_classificacoes(7060), nivel de 4 digitos) -- "Leites e derivados"
# no plural, nao "Leite e derivados" como o texto corrido do EE069 as vezes
# escreve (mesmo padrao de grafia inconsistente do BC visto em Administrados/
# Monitorados). O item 1110 "Aves e ovos" NAO tem regra de item aqui de
# proposito -- o EE069 so nomeia 3 dos seus subitens individualmente (ver
# _ALIMENTOS_EXCECAO_SUBITEM), sem dar uma regra geral para o item; alguns
# subitens de corte de frango descontinuados antes de 2020 (peito/coxa/asa)
# ficam sem classificacao de processamento por falta de fonte -- nao e bug,
# e ausencia de dados no proprio EE069.
_ALIMENTOS_PROCESSAMENTO = {
    "Tubérculos, raízes e legumes": "Alimentos in natura",
    "Hortaliças e verduras": "Alimentos in natura",
    "Frutas": "Alimentos in natura",
    "Cereais, leguminosas e oleaginosas": "Alimentos semi-elaborados",
    "Carnes": "Alimentos semi-elaborados",
    "Pescados": "Alimentos semi-elaborados",
    "Farinhas, féculas e massas": "Alimentos industrializados",
    "Açúcares e derivados": "Alimentos industrializados",
    "Carnes e peixes industrializados": "Alimentos industrializados",
    "Leites e derivados": "Alimentos industrializados",
    "Panificados": "Alimentos industrializados",
    "Óleos e gorduras": "Alimentos industrializados",
    "Bebidas e infusões": "Alimentos industrializados",
    "Enlatados e conservas": "Alimentos industrializados",
    "Sal e condimentos": "Alimentos industrializados",
}
# Excecoes a nivel de subitem, citadas nominalmente no EE069 (nao cobertas
# pela regra de item acima, seja porque o item pai nao tem regra propria
# -- Aves e ovos -- ou porque o subitem e uma excecao dentro de um item que
# tem regra -- Leite longa vida dentro de Leites e derivados).
_ALIMENTOS_EXCECAO_SUBITEM = {
    "1111004": "Alimentos semi-elaborados",  # Leite longa vida
    "1110009": "Alimentos semi-elaborados",  # Frango inteiro
    "1110010": "Alimentos semi-elaborados",  # Frango em pedaços
    "1110044": "Alimentos in natura",         # Ovo de galinha
}


def _item_name_4digit(code: str, by_code: pd.DataFrame, name_col: str) -> str | None:
    item_code = code[:4]
    if item_code not in by_code.index:
        return None
    raw = str(by_code.loc[item_code, name_col])
    return raw.split(".", 1)[1].strip() if "." in raw else raw


def _rollup(sheet: str) -> pd.DataFrame:
    """Le uma aba do Vetores_NT_57.xlsx: propaga cada flag 0/1 de
    _ALL_VETOR_COLS do nivel mais alto em que estiver marcada até os
    subitens (7 digitos) descendentes, e resolve o nome de Item de 4
    digitos (usado so para a faceta Alimentos)."""
    vet = pd.read_excel(_VETORES_XLSX, sheet_name=sheet)
    name_col = vet.columns[0]
    vet["code"] = vet[name_col].astype(str).str.extract(r"^(\d+)\.")
    by_code = vet.set_index("code")

    def ancestors(code: str) -> list[str]:
        return [lv for lv in ("0", code[:1], code[:2], code[:4]) if lv in by_code.index]

    subitens = vet[vet["code"].str.len() == 7].copy()
    for col in _ALL_VETOR_COLS:
        subitens[col] = subitens["code"].apply(
            lambda code, c=col: int(
                any(by_code.loc[a, c] == 1 for a in ancestors(code)) or by_code.loc[code, c] == 1
            )
        )
    subitens["item_4digit_nome"] = subitens["code"].apply(
        lambda code: _item_name_4digit(code, by_code, name_col)
    )
    return subitens[["code", "item_4digit_nome"] + _ALL_VETOR_COLS]


def _derive_classificacao(rolled: pd.DataFrame) -> pd.DataFrame:
    dim = pd.DataFrame({"subitem_codigo": rolled["code"]})

    dim["grupo"] = None
    dim.loc[rolled["Administrados"] == 1, "grupo"] = "Monitorados"
    dim.loc[rolled["Livres"] == 1, "grupo"] = "Livres"

    dim["subgrupo"] = None
    dim.loc[rolled["Alimentação no domicílio"] == 1, "subgrupo"] = "Alimentos"
    dim.loc[rolled["Serviços"] == 1, "subgrupo"] = "Serviços"
    dim.loc[rolled["Bens industriais"] == 1, "subgrupo"] = "Bens Industriais"
    dim.loc[dim["grupo"] == "Monitorados", "subgrupo"] = "Monitorados"

    dim["item"] = None

    is_bens_ind = dim["subgrupo"] == "Bens Industriais"
    dim.loc[is_bens_ind & (rolled["Bens duráveis"] == 1), "item"] = "Duráveis"
    dim.loc[is_bens_ind & (rolled["Bens semiduráveis"] == 1), "item"] = "Semi-duráveis"
    dim.loc[is_bens_ind & (rolled["Bens não duráveis"] == 1), "item"] = "Não Duráveis"

    is_servicos = dim["subgrupo"] == "Serviços"
    dim.loc[is_servicos & (rolled["EX3 Serviços"] == 1), "item"] = "Serviços Subjacente"
    dim.loc[is_servicos & (rolled["EX3 Serviços"] == 0), "item"] = "Serviços Ex Subjacentes"

    is_alimentos = dim["subgrupo"] == "Alimentos"
    alimentos_item = rolled["item_4digit_nome"].map(_ALIMENTOS_PROCESSAMENTO)
    dim.loc[is_alimentos, "item"] = alimentos_item[is_alimentos]
    for code, label in _ALIMENTOS_EXCECAO_SUBITEM.items():
        dim.loc[dim["subitem_codigo"] == code, "item"] = label

    dim.loc[dim["grupo"] == "Monitorados", "item"] = "Monitorados"

    dim["subjacente"] = None
    dim.loc[rolled["EX3 Serviços"] == 1, "subjacente"] = "Serviços Subjacente"
    dim.loc[rolled["EX3 Industriais"] == 1, "subjacente"] = "Bens Industriais Subjacente"
    # "Alimentos Subjacente" sem fonte — ver REGRESSAO CONHECIDA na docstring do modulo.

    dim["comercializavel"] = None
    dim.loc[rolled["Comercializáveis"] == 1, "comercializavel"] = "Comercializável"
    dim.loc[rolled["Não comercializáveis"] == 1, "comercializavel"] = "Não Comercializável"

    for src, dst in _COLS_NUCLEO.items():
        dim[dst] = rolled[src]

    return dim


def _nomes_por_vigencia() -> pd.DataFrame:
    """Nome de exibicao canonico por subitem_codigo: vigencia mais nova
    para a mais antiga (VIGENCIAS["IPCA"] — IPCA-15 e subconjunto, nunca
    introduz codigo/nome que IPCA nao tenha), primeiro match vence."""
    nomes: dict[str, str] = {}
    for vig in reversed(VIGENCIAS["IPCA"]):
        for agregado in vig.agregados:
            cls = _ibge.listar_classificacoes(agregado)
            cls = cls[cls["classificacao_id"] == 315]
            for nome_raw in cls["categoria_nome"]:
                code = _extract_code(nome_raw)
                if code and len(code) == 7 and code not in nomes:
                    nomes[code] = str(nome_raw).split(".", 1)[1].strip()
    return pd.DataFrame(nomes.items(), columns=["subitem_codigo", "nome"])


def run() -> None:
    """Sincroniza macro_brasil.inflc_dim a partir de Vetores_NT_57.xlsx
    (classificacao) + IBGE ao vivo (nome canonico). Rebuild completo em toda
    chamada — barato, sem chamadas de API alem da resolucao de nome (8
    agregados no maximo, so metadados de classificacao)."""
    rolled_por_vigencia = [_rollup(sheet) for sheet in _VETOR_SHEETS]
    rolled = pd.concat(rolled_por_vigencia, ignore_index=True).drop_duplicates("code", keep="last")

    dim = _derive_classificacao(rolled)

    nomes = _nomes_por_vigencia()
    dim = dim.merge(nomes, on="subitem_codigo", how="left")

    dim = dim.astype(object).where(pd.notna(dim), None)
    insert_data_into_database(_DATABASE, _TABLE, dim)


if __name__ == "__main__":
    run()
