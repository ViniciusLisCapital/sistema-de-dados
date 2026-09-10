"""
ETL de juros de economias sem schema proprio -> macro_international.inter_interest_rate.

A tabela foi criada VAZIA em 2026-09-03 (a `base_mercado.interest_rates` de onde
as outras duas foram migradas so tinha BR e US). Este script lhe da o primeiro
conteudo, e por enquanto **uma curva so**:

    POLICY   a taxa de politica monetaria, no vertice de 1 dia util,
             para MX / CL / CO / PE / AR

Existe por decisao explicita do usuario (2026-09-03): *"na tabela de interest
rate coloque tambem a policy_rate descrita como tal. Assim centralizamos os
dados de juros na mesma tabela, independente se ele e o dado da curva, ou dado
definido pelo BC"*. As tres tabelas irmas (`br_interest_rate`,
`us_interest_rate`, esta) passam a ter a mesma curva `POLICY` com a mesma
semantica, e e isso que permite ler juro de politica de qualquer economia por
uma consulta so.

## Este script E a ingestao do BIS (mudou em 2026-09-03, 2a rodada)

Na primeira versao ele **lia** `macro_international.cmb_policy_rates`, que era
o ETL do BIS. As duas tabelas passaram a guardar o mesmo numero: medido, as
53.663 linhas de `cmb_policy_rates` eram reproduzidas **exatamente** (dif
maxima 0,0, zero linhas orfas dos dois lados) por esta tabela mais a curva
POLICY de `macro_brasil.br_interest_rate`. O usuario pediu para eliminar a
duplicacao, entao `cmb_policy_rates` foi removida e o fetch do BIS veio para
ca -- e para `br_interest_rate.py`, que faz o mesmo com BR.

**Isso e uma peca de codigo compartilhada, nao um dado duplicado**: os dois
scripts chamam `connectors.bis.BIS.get_policy_rates()` com listas de paises
**disjuntas** (BR aqui nao entra, ver abaixo), entao nenhum numero e gravado
duas vezes. O que era duplicacao era a tabela, nao a chamada.

**Estrutura a termo desses paises segue sem fonte.** A tabela aceita `curve`
por pais e o dia em que houver curva soberana ou de swap de MX/CL/etc., ela
entra aqui com outro valor de `curve`; o que existe hoje e so o ponto curto.
Nao confundir "a tabela tem dado" com "a tabela tem curva".

## Por que BR e US ficam de FORA

Nao e arbitrario, e o que o COMMENT da coluna `country_code` declara: os dois
tem schema proprio (`macro_brasil.br_interest_rate` e
`macro_us.us_interest_rate`), e duplicar o Brasil aqui daria duas linhas para o
mesmo fato com chaves diferentes. AR **entra**, com a ressalva de que o BIS
parou de atualizar a serie dela em meados de 2025 -- gap no fim e esperado.

O US tambem nao vem do BIS: a POLICY dele e a **meta anunciada pelo Fed**
(`DFEDTAR` e o ponto medio de `DFEDTARL`/`DFEDTARU`, via FRED), que e outra
serie e outra escolha -- ver `domain/db/us/rates/us_interest_rate.py`.

Banco: macro_international.inter_interest_rate
       PRIMARY KEY (date, country_code, curve, tenor)
"""

from __future__ import annotations

import logging

import pandas as pd

from connectors.bis import BIS
from connectors.mysql import insert_data_into_database

logger = logging.getLogger(__name__)

_DATABASE = "macro_international"
_TABLE = "inter_interest_rate"

# BR e US saem por regra de schema (ver docstring), nao por falta de dado.
_PAISES = ["MX", "CL", "CO", "PE", "AR"]

_TENOR = "1d"
# 1 dia util em anos. Zero seria errado: `tenor_years` existe para interpolar e
# ordenar, e um vertice em zero quebra qualquer interpolacao ancorada no curto.
_TENOR_YEARS = round(1 / 252, 6)

# Faixa de sanidade generosa de proposito: a Argentina chegou a **557,04% a.a.**
# em 1993 (medido na serie) e o Peru a 0,25%, entao um teto "razoavel" para uma
# economia reprovaria dado correto de outra. O piso e 0 -- nenhuma das cinco
# teve meta negativa.
_PISO, _TETO = 0.0, 1000.0

# Dias corridos para tras no passe de rotina. Generoso de proposito: o BIS
# republica em lote, com lag medido de 8 dias e ate 12 no pior caso (e o maior
# de todas as fontes do `--continuous`), entao uma janela curta perderia
# revisao. Como a insercao e upsert, reescrever 30 dias nao custa nada.
_DIAS_ROTINA = 30

_bis = BIS()


def coletar(full: bool = False, dias: int = _DIAS_ROTINA) -> pd.DataFrame:
    """Busca no BIS e monta o DataFrame pronto para a tabela.

    Args:
        full: True busca a historia inteira (~42 mil linhas nos 5 paises,
              a mais antiga sendo AR em 1993-04).
        dias: janela retroativa do passe de rotina, em dias corridos.
    """
    start = None
    if not full:
        corte = pd.Timestamp.today().normalize() - pd.Timedelta(days=max(dias, 1))
        start = corte.strftime("%Y-%m-%d")

    pr = _bis.get_policy_rates(countries=_PAISES, freq="D", start=start)

    # O BIS ignora paises que nao tem dado na janela em vez de levantar, entao
    # um erro de codigo de pais sairia como serie faltando em silencio.
    inesperados = set(pr["country_code"].unique()) - set(_PAISES)
    if inesperados:
        raise ValueError(f"BIS devolveu pais fora da lista: {sorted(inesperados)}")

    pr = pr.copy()
    pr["date"] = pd.to_datetime(pr["date"])
    pr["value"] = pr["value"].astype(float)
    pr = pr.dropna(subset=["value"]).sort_values(["country_code", "date"])

    fora = pr[(pr.value < _PISO) | (pr.value > _TETO)]
    if len(fora):
        raise ValueError(f"{len(fora)} valores fora de [{_PISO}, {_TETO}]:\n"
                         f"{fora.head().to_string()}")

    df = pd.DataFrame({
        "date": pr["date"].dt.date,
        "country_code": pr["country_code"],
        "curve": "POLICY",
        "tenor": _TENOR,
        "tenor_years": _TENOR_YEARS,
        "value": pr["value"].round(8),
    })
    if df.duplicated(["date", "country_code", "curve", "tenor"]).any():
        raise ValueError("chave duplicada na coleta")
    return df


def run(full: bool = False, dias: int = _DIAS_ROTINA) -> None:
    """Atualiza macro_international.inter_interest_rate.

    Args:
        full: True recarrega o historico inteiro do BIS (~42 mil linhas).
        dias: janela retroativa do passe de rotina, em dias corridos.
    """
    df = coletar(full=full, dias=dias)
    if df.empty:
        logger.warning("inter_interest_rate: nada a inserir")
        return
    logger.info("inter_interest_rate: %d linhas, %s -> %s",
                len(df), df["date"].min(), df["date"].max())
    for pais, g in df.groupby("country_code"):
        logger.info("  %s POLICY %6d linhas, %s -> %s",
                    pais, len(g), g["date"].min(), g["date"].max())
    insert_data_into_database(_DATABASE, _TABLE, df)
