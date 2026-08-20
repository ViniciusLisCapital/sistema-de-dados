"""
Relative importance (pesos) do CPI dos EUA -- snapshot de dezembro, um por ano.

--------------------------------------------------------------------------------
POR QUE TABELA SEPARADA (e nao coluna em inflc_cpi, como no Brasil)
--------------------------------------------------------------------------------
No Brasil `inflc_decomposicao` traz var_mensal/pesos/contribuicao na mesma linha,
porque o IBGE publica peso mensal. O BLS nao: publica UM peso por item por ANO.
Escrever esse peso em cada linha mensal ou duplicaria 12x o mesmo numero, ou --
pior -- sugeriria um peso mensal que nunca foi publicado.

Com a tabela separada, a contribuicao (= variacao x peso) passa a ser uma decisao
de JOIN explicita e documentada em vez de ficar embutida no schema. A convencao:
carregar o snapshot de dezembro para frente pelo ano seguinte.

**Testado, e a escolha do snapshot importa.** Reconstruindo a variacao mensal do
headline a partir dos 3 nos de nivel 1 (Food, Energy, core) em 2020-2026 e
comparando com o headline publicado:
    um unico vetor (2025) para a amostra toda   erro medio absoluto 0,0186 p.p.
    o snapshot do proprio ano de cada mes       erro medio absoluto 0,0147 p.p.
Usar o peso do ano certo corta o erro 21%. Os pesos de nivel 1 andam o suficiente
para isso: Energy foi 6,155 -> 7,348 -> 6,383 nas planilhas de 2020, 2021 e 2025.

Os ~0,015 p.p. que sobram sao irredutiveis com dado publicado, e vale saber disso
antes de tratar qualquer decomposicao como identidade: a relative importance e um
snapshot de DEZEMBRO de uma grandeza que o BLS atualiza por preco continuamente,
entao nenhum vetor unico reproduz todo mes. NAO e artefato de ajuste sazonal --
repetindo o teste em NSA o erro fica um pouco PIOR (0,0191), o que descarta essa
explicacao.

--------------------------------------------------------------------------------
DUAS ARMADILHAS DO ARQUIVO
--------------------------------------------------------------------------------
1. **A Tabela 1 empilha DUAS arvores independentes**, separadas por linhas de
   nivel 0 sem peso. `Expenditure category` soma 100; `Special aggregate indexes`
   soma ~664, porque sao recortes que se sobrepoem (Energy, core, Commodities,
   Services, Durables...). Somar as duas juntas da 764 e nao significa nada -- por
   isso `secao` esta na chave e nunca deve ser agregada por cima.

2b. **5 itens tem rotulo diferente em cu.item** e por isso ficavam sem codigo --
   resolvidos com o `_ALIAS` de `inflc_cpi_dim`, importado daqui para as duas
   tabelas nao divergirem. Ver a docstring da dim para como cada par foi confirmado.

2. **O arquivo nao traz item_code**, so nome + nivel de indentacao -- por isso a
   chave e (reference_period, indice, secao, indent_level, item_name) e o
   `item_code` e uma coluna resolvida por nome contra `cu.item`, que pode ser NULL.
   Fica NULL nos residuos "Unsampled ..." que o BLS publica com peso mas sem serie.
   Eles sao mantidos de proposito: carregam peso e sao filhos de verdade na
   aritmetica da arvore (a soma dos filhos de `Owners' equivalent rent` so fecha
   com o "Unsampled owners' equivalent rent" dentro).

`weights_year` e o ano da CESTA de gasto, distinto do ano de `reference_period`: a
planilha de 2025 traz a cesta de 2024 precificada a dezembro de 2025. Fica **NULL em
2020 e 2021**, e isso vem da fonte: ali o BLS declara cesta BIENAL ("2017-2018
weights", "2019-2020 weights"), que nao cabe num ano so -- a atualizacao anual comecou
em 2023. A coluna nasceu NOT NULL e foi para NULL por causa disso (ALTER 2026-08); o
INSERT falhava com 1048 e a falha vinha impressa, nao levantada -- ver
domain/db/us/_gravar.py.

--------------------------------------------------------------------------------
COBERTURA: 1947 EM DIANTE, EM TRES FORMATOS
--------------------------------------------------------------------------------
`bls.list_relative_importance_years()` devolve 2020-2025, e so isso, porque le os
links `<ano>.xlsx` da pagina. Isso NAO e o fim da cobertura -- e o fim de um
formato. A pagina tambem linka arquivos de decada, verificados ao vivo (baixados,
magic bytes conferidos, lista de entradas lida):

  2020-2025  <ano>.xlsx                                     xlsx    <- carregado aqui
  2010-2019  ri-archive-2010-2019.zip   (35 entradas)       txt fixed-width
  2000-2009  ri-archive-2000-2009.zip   (24 entradas)       txt fixed-width
  1990-1999  ri-archive-1990-1999.zip   (10 arquivos)       txt fixed-width, COM item_code
  1987-1989  ri-archive-1987-1989.zip   (3 arquivos)        txt fixed-width, COM item_code
  1947-1986  historical-relative-importance-1947-1986.xlsx  xlsx, 13 abas por faixa

Ou seja o peso pode chegar a 1947 e nao a 2020; falta parser, nao dado. Os arquivos
dos anos 90 sao os MAIS faceis de casar -- trazem coluna de item code, que o formato
moderno perdeu. `run()` avisa quando o ano pedido cai fora do formato xlsx, em vez
de falhar em silencio.

Ha ainda um peso MENSAL, para as 37 linhas da Tabela 1 do news release, que nao esta
nesta tabela -- vem do HTML do release e nao da planilha. Ver
us_project/inflation_hierarchy.md, secao 2.

--------------------------------------------------------------------------------
DDL
--------------------------------------------------------------------------------
  CREATE TABLE macro_us.inflc_cpi_pesos (
      reference_period DATE         NOT NULL,
      indice           VARCHAR(10)  NOT NULL,
      secao            VARCHAR(32)  NOT NULL,
      indent_level     TINYINT      NOT NULL,
      item_name        VARCHAR(160) NOT NULL,
      item_code        VARCHAR(16),
      weight           DOUBLE,
      weights_year     SMALLINT     NULL,      -- NULL em 2020/2021: cesta bienal
      PRIMARY KEY (reference_period, indice, secao, indent_level, item_name),
      KEY idx_code (item_code, reference_period)
  );
  -- COMMENTs de tabela e de coluna aplicados no MySQL (ver domain/db/CLAUDE.md).

Banco: macro_us.inflc_cpi_pesos
       PRIMARY KEY (reference_period, indice, secao, indent_level, item_name)
"""

from __future__ import annotations

import pandas as pd

from connectors.bls import BLS
from domain.db.us.inflation.inflc_cpi_dim import _ALIAS
from domain.db.us._gravar import gravar

_DATABASE = "macro_us"
_TABLE = "inflc_cpi_pesos"

_SECAO = {
    "Expenditure category": "expenditure",
    "Special aggregate indexes": "special_aggregate",
}

# Primeiro ano publicado como <ano>.xlsx. Antes disso a pagina do BLS serve zips de
# decada em formato fixed-width -- ver "COBERTURA" na docstring.
_PRIMEIRO_XLSX = 2020


def run(years: int | list[int] | None = None, validar: bool = True) -> None:
    """Atualiza macro_us.inflc_cpi_pesos.

    Args:
        years:   ano, lista de anos, ou None (default) para todos os anos que o BLS
                 publica no formato xlsx. Anos anteriores a 2020 sao recusados com
                 aviso -- existem, mas em outro formato, ainda sem parser.
        validar: confere que a secao `expenditure` soma 100 em cada ano/populacao
                 (default True). E o teste que pega a planilha mudando de forma.
    """
    bls = BLS()
    disponiveis = bls.list_relative_importance_years()

    if years is None:
        alvo = disponiveis
    else:
        alvo = [years] if isinstance(years, int) else list(years)

    antigos = [y for y in alvo if y < _PRIMEIRO_XLSX]
    if antigos:
        print(f"aviso: {antigos} ficam de fora -- antes de {_PRIMEIRO_XLSX} o BLS publica")
        print("       zips de decada em fixed-width, sem parser ainda (ver docstring).")
        alvo = [y for y in alvo if y >= _PRIMEIRO_XLSX]

    faltando = [y for y in alvo if y not in disponiveis]
    if faltando:
        print(f"aviso: {faltando} nao aparecem na pagina do BLS ({disponiveis}) -- tentando ainda assim")

    partes = []
    for y in alvo:
        try:
            ri = bls.get_relative_importance(y)
        except Exception as e:
            print(f"  {y}: FALHOU -- {type(e).__name__}: {str(e)[:90]}")
            continue

        df = ri[ri["section"].isin(_SECAO)].copy()
        df["secao"] = df["section"].map(_SECAO)
        df = df.rename(columns={"population": "indice"})
        df["item_name"] = df["item_name"].astype(str).str.strip()
        df["indent_level"] = df["indent_level"].astype(int)

        dup = df.duplicated(subset=["reference_period", "indice", "secao", "indent_level", "item_name"])
        if dup.any():
            # Mesmo nome no mesmo nivel e secao: a chave nao distingue, e a ultima
            # linha ganharia em silencio no upsert. Preferir falhar alto.
            exemplos = df.loc[dup, "item_name"].unique()[:5].tolist()
            raise ValueError(
                f"{y}: {dup.sum()} linhas colidem na chave (nome+nivel+secao), ex {exemplos}. "
                "A planilha mudou de forma -- rever antes de gravar."
            )

        if validar:
            for indice, g in df[df["secao"] == "expenditure"].groupby("indice"):
                total = g[g["indent_level"] == 1]["weight"].sum()
                marca = "ok" if abs(total - 100) < 0.01 else "NAO FECHA"
                print(f"  {y} {indice:<6} expenditure nivel 1 soma {total:.3f}  [{marca}]")
                if marca == "NAO FECHA":
                    raise ValueError(
                        f"{y}/{indice}: a secao expenditure deveria somar 100 no nivel 1, "
                        f"deu {total:.3f}. Nao gravando."
                    )

        partes.append(df[["reference_period", "indice", "secao", "indent_level",
                          "item_name", "weight", "weights_year"]])

    if not partes:
        print("nada a gravar")
        return

    out = pd.concat(partes, ignore_index=True)

    # item_code resolvido por nome (a planilha nao traz codigo). NULL fica NULL.
    # _ALIAS vem da dim: 5 itens que a planilha e o cu.item rotulam diferente. Sem
    # isto o peso deles fica com item_code NULL, e o relatorio -- que junta peso e
    # indice POR CODIGO -- nao acha contribuicao para itens que a tem publicada.
    itens = bls.get_item_tree()
    code_by_name = {}
    for _, r in itens.iterrows():
        code_by_name.setdefault(str(r["item_name"]).strip(), str(r["item_code"]).strip())
    for planilha, em_cu_item in _ALIAS.items():
        if em_cu_item in code_by_name:
            code_by_name.setdefault(planilha, code_by_name[em_cu_item])
    out["item_code"] = out["item_name"].map(code_by_name)
    resolvidos = out["item_code"].notna().sum()
    print(f"item_code resolvido por nome: {resolvidos}/{len(out)} linhas "
          f"({100 * resolvidos / len(out):.1f}%) -- o resto sao residuos 'Unsampled', esperado")
    out["item_code"] = out["item_code"].where(out["item_code"].notna(), None)

    cols = ["reference_period", "indice", "secao", "indent_level", "item_name",
            "item_code", "weight", "weights_year"]
    gravar(_DATABASE, _TABLE, out[cols], sonda="reference_period")
    anos = sorted(out["reference_period"].dt.year.unique().tolist())
    print(f"  anos carregados: {anos}")


if __name__ == "__main__":
    run()
