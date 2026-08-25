"""
Niveis mensais do PCE dos EUA por linha da tabela 2.4.x U do BEA -- a tabela de fato
do PCE.

Duas MEDIDAS das mesmas 402 linhas, na mesma grade mensal, do mesmo arquivo:

  `indice`   indice de preco encadeado, 2017=100  (tabela 2.4.4U)
  `nominal`  despesa em US$ milhoes, SAAR         (tabela 2.4.5U)

`medida` esta na CHAVE, nao virou duas colunas, pelo mesmo motivo que `ajuste` esta
na chave de `inflc_cpi`: a cobertura e desigual. As duas linhas de "net" do BEA
(`Net expenditures abroad by U.S. residents`, `Net foreign travel`, marcadas
`ZZZZZZ`) tem nominal e **nao** tem indice de preco -- uma coluna `valor_indice`
ficaria NULL nelas e sugeriria que o par existe. E duas tabelas separadas seriam
duas tabelas com chave identica.

--------------------------------------------------------------------------------
POR QUE O NOMINAL ENTRA AQUI, E NAO NUMA TABELA DE PESOS
--------------------------------------------------------------------------------
Do lado do CPI, o peso e uma tabela propria (`inflc_cpi_pesos`) porque o BLS publica
um peso por item por ANO -- escrever isso em cada mes duplicaria doze vezes ou
sugeriria um peso mensal que nunca foi publicado.

Aqui e o contrario: o BEA publica a despesa nominal de cada linha em **todo mes**,
na mesma grade do indice. O peso do mes t e `nominal[linha, t] / nominal[1, t]`, e
guardar isso como coluna derivada seria guardar o que ja e derivavel do que esta na
tabela. Entao o peso nao e gravado -- a razao e calculada na leitura, em
`analytics/us/inflation/`, exatamente como as variacoes.

Consequencia pratica boa: a contribuicao do PCE nao carrega a aproximacao de
"snapshot de dezembro carregado para o ano seguinte" que a do CPI carrega. Medido
contra este banco, a contribuicao mensal reconstroi a variacao do headline com erro
medio de **0,0009 p.p.** no nivel 1 (contra 0,0124 p.p. do CPI).

--------------------------------------------------------------------------------
SO EXISTE SA
--------------------------------------------------------------------------------
O mensal do BEA e dessazonalizado e nao ha contrapartida NSA destas tabelas -- por
isso nao ha coluna `ajuste` aqui. Nao e lacuna de carga, e da fonte.

--------------------------------------------------------------------------------
NIVEL, NAO VARIACAO
--------------------------------------------------------------------------------
Mesma regra de `inflc_cpi`: so o nivel e gravado. Y/Y, M/M, 3 meses anualizados e
contribuicao saem dele sem perda e sao calculados na leitura -- gravar as duas
coisas abre espaco para elas discordarem.

**Nunca comparar niveis de indice entre linhas.** Todas as 2.4.4U estao em 2017=100,
o que e mais amigavel que o CPI (cuja base varia por item), mas 2017=100 nao
significa "mesmo preco": duas linhas no mesmo nivel so dizem que ambas andaram o
mesmo tanto desde 2017.

--------------------------------------------------------------------------------
CUSTO
--------------------------------------------------------------------------------
Uma requisicao HTTP de 12 MB, sem chave e sem cota (ver `connectors/bea.py`), e o
arquivo e reaproveitado no mesmo dia -- entao rodar isto depois de
`inflc_pce_dim.py` na mesma passada nao baixa de novo. A carga fria inteira
(1959-01 em diante, as duas medidas) sao 607.644 linhas.

**Uma passada da dim basta**, ao contrario do CPI, onde `jobs/update_us.py` roda
`inflc_cpi_dim` antes e depois de `inflc_cpi` porque as colunas de cobertura sao
medidas da tabela de series. Aqui a arvore e as series saem do MESMO arquivo, entao
`inflc_pce_dim` mede `idx_begin`/`nom_end` direto da fonte e nao depende desta
tabela ja estar carregada.

--------------------------------------------------------------------------------
DDL
--------------------------------------------------------------------------------
  CREATE TABLE macro_us.inflc_pce (
      date    DATE        NOT NULL,
      linha   SMALLINT    NOT NULL,
      medida  VARCHAR(8)  NOT NULL,
      value   DOUBLE,
      code    VARCHAR(10),
      PRIMARY KEY (date, linha, medida),
      KEY idx_linha (linha, medida, date)
  );
  -- COMMENTs de tabela e de coluna aplicados no MySQL (ver domain/db/CLAUDE.md).

Banco: macro_us.inflc_pce -- PRIMARY KEY (date, linha, medida)
"""

from __future__ import annotations

import datetime as _dt

import pandas as pd

from connectors.bea import ABA_PCE_INDICE, ABA_PCE_NOMINAL, ler_tabela
from domain.db.us._gravar import gravar

_DATABASE = "macro_us"
_TABLE = "inflc_pce"

# medida -> aba do xlsx da Secao 2.
_ABAS = {
    "indice": ABA_PCE_INDICE,
    "nominal": ABA_PCE_NOMINAL,
}

_MIN_ANO = 1959


def run(start_year: int | str | None = None, end_year: int | None = None,
        medidas: tuple[str, ...] = ("indice", "nominal")) -> None:
    """Atualiza macro_us.inflc_pce.

    Args:
        start_year: ano inicial. Default: 3 anos atras (janela de rotina). `"all"`
                    para a serie completa desde 1959. O arquivo baixado tem a
                    historia toda de qualquer jeito -- isto recorta o que vai para o
                    banco, nao o que e baixado.
        end_year:   ano final. Default: ano corrente.
        medidas:    quais medidas gravar. Default as duas; `nominal` e o que
                    sustenta peso e contribuicao, entao carregar so `indice` deixa a
                    contribuicao sem base.

    Raises:
        ValueError: se `medidas` tiver um nome que nao existe.
    """
    desconhecidas = set(medidas) - set(_ABAS)
    if desconhecidas:
        raise ValueError(f"medida(s) desconhecida(s): {sorted(desconhecidas)}. "
                         f"Validas: {sorted(_ABAS)}")

    hoje = _dt.date.today()
    ini = _MIN_ANO if start_year == "all" else (hoje.year - 3 if start_year is None
                                               else int(start_year))
    fim = int(end_year) if end_year else hoje.year

    partes = []
    for medida in medidas:
        t = ler_tabela(_ABAS[medida])
        code_por_linha = dict(zip(t.estrutura["linha"], t.estrutura["code"]))
        df = t.observacoes.copy()
        df["date"] = pd.to_datetime(df["date"])
        antes = len(df)
        df = df[(df["date"].dt.year >= ini) & (df["date"].dt.year <= fim)]
        df["medida"] = medida
        df["code"] = df["linha"].map(code_por_linha)
        partes.append(df[["date", "linha", "medida", "value", "code"]])
        print(f"  {medida:>7}: {len(df):,} obs de {antes:,} no arquivo, "
              f"{df['linha'].nunique()} linhas, "
              f"{df['date'].min():%Y-%m} -> {df['date'].max():%Y-%m}  ({t.aba})")

    out = pd.concat(partes, ignore_index=True)
    gravar(_DATABASE, _TABLE, out, sonda="linha")


if __name__ == "__main__":
    run()
