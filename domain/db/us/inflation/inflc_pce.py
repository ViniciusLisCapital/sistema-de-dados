"""
Niveis mensais do PCE dos EUA por linha da tabela 2.4.x U do BEA -- a tabela de fato
do PCE.

Duas MEDIDAS das mesmas 402 linhas, na mesma grade mensal:

  `indice`   indice de preco encadeado, 2017=100  (tabela 2.4.4U)
  `nominal`  despesa em US$ milhoes, SAAR         (tabela 2.4.5U)

`medida` esta na CHAVE, nao virou duas colunas, pelo mesmo motivo que `ajuste` esta
na chave de `inflc_cpi`: a cobertura e desigual. As duas linhas de "net" do BEA
(`Net expenditures abroad by U.S. residents`, `Net foreign travel`, marcadas
`ZZZZZZ`) tem nominal e **nao** tem indice de preco -- uma coluna `valor_indice`
ficaria NULL nelas e sugeriria que o par existe. E duas tabelas separadas seriam
duas tabelas com chave identica.

--------------------------------------------------------------------------------
A FONTE E A API (desde 2026-08-26)
--------------------------------------------------------------------------------
Este script carregava do xlsx de release. Passou para a **API** (dataset
`NIUnderlyingDetail`), que e o contrato melhor para VALOR por tres razoes medidas:

1. **Nao depende de camada de apresentacao.** O parser do xlsx exige `"Line"` na
   celula A8, 2 espacos por nivel na coluna B, `.....` para ausente e "coluna A nao e
   numero" para nota de rodape. Um reformat cosmetico do BEA quebra tudo isso. A API
   devolve numero tipado em campo nomeado.
2. **Pede so a janela que vai gravar.** O xlsx traz sempre os 810 meses (12 MB);
   `Year=2024,2025,2026` traz 3 anos (~3 MB). A carga de rotina ficou ~4x mais leve.
3. **Traz o codigo da serie no proprio registro**, entao `code` nao precisa de um
   segundo passe pela estrutura.

O que a troca NAO muda: a arvore (`inflc_pce_dim`) continua saindo do xlsx, porque a
API nao publica hierarquia nenhuma. Isso nao e preferencia -- o proprio servico
responde que existem so quatro metodos (GetDatasetList, GetParameterList,
GetParameterValues, GetData), e o registro de `GetData` tem 10 campos, nenhum de pai,
nivel ou indentacao, com `LineDescription` sem os espacos da coluna B. Ver
`connectors/bea.py`.

**Precisa de `BEA_API_KEY`** no `.env` (gratuita, https://apps.bea.gov/API/signup/).
`fonte="xlsx"` segue funcionando como saida de emergencia se a API cair -- os dois
caminhos foram conferidos valor a valor, 608.442 observacoes, zero diferentes.

--------------------------------------------------------------------------------
A CONFERENCIA OPORTUNISTA
--------------------------------------------------------------------------------
`conferir=True` (default) compara o que veio da API com o xlsx **quando o xlsx do dia
ja esta em disco** -- que e o caso normal em `jobs/update_us.py`, onde
`inflc_pce_dim` roda antes e baixa o arquivo. Nesse caso a conferencia e de graca e
vira garantia por carga, nao so no teste: duas leituras independentes da mesma fonte
tem de dar o mesmo numero, e divergir levanta antes de gravar. Se o arquivo nao
estiver em cache, a conferencia e PULADA em vez de baixar 12 MB so para conferir --
`tests/test_bea_api.py` e quem faz a versao completa dela.

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
Medido em 2026-08-26:

  rotina (3 anos, 2 medidas)   2 requisicoes,  ~6 MB,   ~5s
  completa (1959->hoje)        2 requisicoes, ~150 MB, ~40s

A carga completa pela API e mais PESADA que pelo xlsx (12 MB), porque o xlsx traz as
duas tabelas de uma vez num arquivo comprimido enquanto a API manda JSON. A rotina,
que e o que roda todo mes, e mais leve. Limites documentados da API: 100 req/min,
100 MB/min, 30 erros/min -- a carga completa passa perto do de MB/min e mediu-se que
nao foi estrangulada, mas nao ha margem para rodar `--full` duas vezes no mesmo
minuto.

**Uma passada da dim basta**, ao contrario do CPI, onde `jobs/update_us.py` roda
`inflc_cpi_dim` antes e depois de `inflc_cpi` porque as colunas de cobertura sao
medidas da tabela de series. Aqui a arvore e a cobertura saem do MESMO xlsx, entao
`inflc_pce_dim` mede `idx_begin`/`nom_end` direto da fonte e nao depende desta tabela
ja estar carregada.

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

from connectors.bea import (ABA_PARA_TABELA, ABA_PCE_INDICE, ABA_PCE_NOMINAL,
                            anos_param, caminho_cache_hoje, comparar_obs,
                            indexar_obs, ler_tabela, ler_tabela_api)
from domain.db.us._gravar import gravar

_DATABASE = "macro_us"
_TABLE = "inflc_pce"

# medida -> aba do xlsx da Secao 2. A tabela da API sai de ABA_PARA_TABELA.
_ABAS = {
    "indice": ABA_PCE_INDICE,
    "nominal": ABA_PCE_NOMINAL,
}

_MIN_ANO = 1959


def _conferir(medida: str, api: pd.DataFrame, aba: str, ini: int, fim: int) -> str:
    """Compara os valores da API com o xlsx do dia, se ele estiver em cache.

    Args:
        medida: nome da medida, so para a mensagem.
        api:    o que veio da API, colunas linha/date/value, ja recortado na janela.
        aba:    aba correspondente do xlsx.
        ini:    primeiro ano da janela.
        fim:    ultimo ano da janela.

    Returns:
        Uma frase para o log.

    Raises:
        RuntimeError: se qualquer valor divergir, ou se uma das portas trouxer
                      observacao que a outra nao tem.
    """
    caminho = caminho_cache_hoje()
    if caminho is None:
        return "conferencia pulada (xlsx do dia nao esta em cache)"

    # A comparacao em si vive no connector, para nao haver duas implementacoes dela
    # (a outra e `conferir_api_xlsx`, a versao completa que o teste roda).
    r = comparar_obs(indexar_obs(api, (ini, fim)),
                     indexar_obs(ler_tabela(aba, caminho=caminho).observacoes,
                                 (ini, fim)))
    if r["n_so_a"] or r["n_so_b"] or r["n_diferentes"]:
        raise RuntimeError(
            f"{medida}: API e xlsx discordam -- {r['n_so_a']} obs so na API, "
            f"{r['n_so_b']} so no xlsx, {r['n_diferentes']} com valor diferente, "
            f"diferenca maxima {r['dif_max']:.10g} em {r['onde_dif']}. "
            "As duas portas leem a MESMA publicacao: divergir significa que uma das "
            "duas leituras esta errada, ou que o xlsx em cache e de um vintage "
            "anterior ao que a API esta servindo (confira as datas de publicacao). "
            "Nao gravei nada."
        )
    return f"conferido contra o xlsx: {r['n_comum']:,} obs, todas iguais"


def run(start_year: int | str | None = None, end_year: int | None = None,
        medidas: tuple[str, ...] = ("indice", "nominal"),
        fonte: str = "api", conferir: bool = True) -> None:
    """Atualiza macro_us.inflc_pce.

    Args:
        start_year: ano inicial. Default: 3 anos atras (janela de rotina). `"all"`
                    para a serie completa desde 1959. Pela API isto recorta tambem o
                    que e BAIXADO, nao so o que vai para o banco -- diferente do
                    xlsx, que traz a historia toda de qualquer jeito.
        end_year:   ano final. Default: ano corrente.
        medidas:    quais medidas gravar. Default as duas; `nominal` e o que sustenta
                    peso e contribuicao, entao carregar so `indice` deixa a
                    contribuicao sem base.
        fonte:      `"api"` (default) ou `"xlsx"`. O xlsx e saida de emergencia: os
                    dois caminhos foram conferidos valor a valor e dao o mesmo
                    numero, mas so a API e barata numa janela curta.
        conferir:   com `fonte="api"`, compara com o xlsx quando ele ja esta em cache
                    (de graca na passada do `update_us.py`) e levanta se divergir.
                    Ignorado quando `fonte="xlsx"`.

    Raises:
        ValueError:   se `medidas` tiver um nome que nao existe, ou `fonte` invalida.
        RuntimeError: se a conferencia com o xlsx divergir (nada e gravado).
    """
    desconhecidas = set(medidas) - set(_ABAS)
    if desconhecidas:
        raise ValueError(f"medida(s) desconhecida(s): {sorted(desconhecidas)}. "
                         f"Validas: {sorted(_ABAS)}")
    if fonte not in ("api", "xlsx"):
        raise ValueError(f"fonte {fonte!r} invalida -- use 'api' ou 'xlsx'")

    hoje = _dt.date.today()
    ini = _MIN_ANO if start_year == "all" else (hoje.year - 3 if start_year is None
                                               else int(start_year))
    fim = int(end_year) if end_year else hoje.year

    partes = []
    for medida in medidas:
        aba = _ABAS[medida]
        if fonte == "api":
            # A janela vai no pedido: "X" para a serie inteira, senao a lista de anos.
            anos = anos_param(None if start_year == "all" else ini,
                              None if start_year == "all" else fim)
            t = ler_tabela_api(ABA_PARA_TABELA[aba], anos=anos,
                              freq=aba.rsplit("-", 1)[-1])
        else:
            t = ler_tabela(aba)

        df = t.observacoes.copy()
        df["date"] = pd.to_datetime(df["date"])
        antes = len(df)
        df = df[(df["date"].dt.year >= ini) & (df["date"].dt.year <= fim)]
        df["medida"] = medida
        # A API traz o SeriesCode em cada registro; o xlsx, so na estrutura.
        code_por_linha = dict(zip(t.estrutura["linha"], t.estrutura["code"]))
        df["code"] = df["linha"].map(code_por_linha)
        partes.append(df[["date", "linha", "medida", "value", "code"]])

        print(f"  {medida:>7}: {len(df):,} obs de {antes:,} baixadas, "
              f"{df['linha'].nunique()} linhas, "
              f"{df['date'].min():%Y-%m} -> {df['date'].max():%Y-%m}  "
              f"({t.aba}, fonte={t.fonte})")
        if fonte == "api" and conferir:
            print(f"           {_conferir(medida, df, aba, ini, fim)}")

    out = pd.concat(partes, ignore_index=True)
    gravar(_DATABASE, _TABLE, out, sonda="linha")


if __name__ == "__main__":
    run()
