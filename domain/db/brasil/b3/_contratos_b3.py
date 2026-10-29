"""
Nucleo compartilhado das quatro tabelas que saem do boletim de precos da B3
(`connectors/b3_precos.py`): cmb_contratos_b3, cmb_opcoes_dolar,
br_juros_contratos e bolsa_ibov_futuro. Nao e tabela (sem `_TABLE`): o registry
nao o enxerga.

O arquivo e baixado uma vez por pregao e cacheado so com os instrumentos de
`b3_precos.PRODUTOS`; cada tabela le o cache e fica com as mercadorias dela.

## A posicao em aberto e gravada no FECHAMENTO do dia

O boletim do pregao D traz a posicao do inicio de D (= fechamento de D-1; ver o
docstring do conector). Aqui `posicao_aberto` de (D, contrato) e a posicao de
ABERTURA do pregao seguinte, que e o numero que o Boletim Diario e a imprensa
chamam de posicao do dia. Tres casos:

- o pregao seguinte tem o contrato: a posicao dele;
- o pregao seguinte existe e o contrato sumiu: zero (venceu ou foi deslistado);
- o pregao seguinte ainda nao saiu, ou o download dele falhou: NULL -- e o
  proximo passe de rotina preenche, porque a janela volta 10 dias.

Zero que volta: um contrato com posicao em D, zero no arquivo seguinte e posicao
de novo no outro fica NULL em D. Sao arquivos com a abertura zerada pela fonte --
o de 10/05/2018 em 354 codigos, o de 11/09/2025 em 29 (DI1F27, DDIF26, DAP...) --,
e uma varredura das 2.301 sessoes acha so esses dois mais tres codigos isolados
de pouca liquidez, em que um dia nulo nao custa nada.

Feriado (arquivo vazio, cacheado) e pulado; falha de rede (nada no cache) NAO e
pulada, para nao atribuir a D a posicao de dois pregoes depois.

FRA de cupom (FRC), rolagem (DR1) e casado (FRP) nao carregam posicao propria --
a do FRA cai no cupom (DDI), a da rolagem e do casado no dolar --, e ficam com
`posicao_aberto` NULL, nao zero.
"""

from __future__ import annotations

import logging
import os

import numpy as np
import pandas as pd

from connectors import b3_precos

logger = logging.getLogger(__name__)

_SEM_POSICAO = ("FRC", "DR1", "FRP")

# Colunas comuns as tabelas de contrato (as de opcao trocam o ajuste por tipo e strike)
COLUNAS_CONTRATO = ["date", "ticker", "ativo", "tipo", "vencimento", "negocios", "contratos",
                    "vol_brl", "vol_usd", "posicao_aberto", "abertura", "minimo", "maximo",
                    "medio", "ultimo", "ajuste", "taxa_ajuste"]
COLUNAS_OPCAO = ["date", "ticker", "ativo", "vencimento", "opcao", "strike", "negocios",
                 "contratos", "vol_brl", "vol_usd", "posicao_aberto", "abertura", "minimo",
                 "maximo", "medio", "ultimo"]


def datas(full: bool, dias: int) -> list[pd.Timestamp]:
    fim = pd.Timestamp.today().normalize()
    return list(pd.bdate_range(b3_precos.INICIO, fim) if full
                else pd.bdate_range(end=fim, periods=dias))


def painel(datas_, ativos) -> pd.DataFrame:
    """Um registro por (pregao, instrumento) das mercadorias pedidas, com a
    posicao do fechamento e a classificacao do codigo."""
    b3_precos.baixar_muitos(datas_)
    # (data, DataFrame | None, status): ok | feriado | falha
    dias = []
    for d in datas_:
        D = b3_precos.precos(d)
        if D is not None:
            dias.append((d, D, "ok"))
        else:
            dias.append((d, None, "feriado" if os.path.exists(b3_precos.caminho_cache(d)) else "falha"))

    falhas = [d.date() for d, _, s in dias if s == "falha"]
    if falhas:
        logger.warning("b3_precos: %d pregoes sem download (%s%s)", len(falhas), falhas[:5],
                       " ..." if len(falhas) > 5 else "")

    blocos, fora = [], {}
    for k, (d, D, st) in enumerate(dias):
        if st != "ok":
            continue
        # posicao de abertura dos dois pregoes seguintes (o segundo so serve de prova)
        prox = prox2 = None
        seguintes = [(s2, D2) for _, D2, s2 in dias[k + 1:] if s2 != "feriado"][:2]
        if seguintes and seguintes[0][0] == "ok":
            prox = seguintes[0][1].set_index("ticker")["oi_abertura"]
            if len(seguintes) == 2 and seguintes[1][0] == "ok":
                prox2 = seguintes[1][1].set_index("ticker")["oi_abertura"]
        D = D.copy()
        cls = D["ticker"].map(b3_precos.classificar)
        for t in D.loc[cls.isna(), "ticker"]:
            fora[t] = fora.get(t, 0) + 1
        D, cls = D[cls.notna()], cls[cls.notna()]
        meta = pd.DataFrame(list(cls), index=D.index)
        D = D.join(meta)
        D = D[D["ativo"].isin(ativos)]
        if D.empty:
            continue
        D["date"] = d.date()
        D["posicao_aberto"] = (D["ticker"].map(prox).fillna(0) if prox is not None else np.nan)
        if prox2 is not None:
            # com posicao hoje, zero amanha e posicao de novo depois de amanha: o zero e
            # defeito do arquivo, nao fechamento (ver o docstring) -- vira NULL
            volta = D["ticker"].map(prox2).fillna(0) > 0
            D.loc[(D["oi_abertura"] > 0) & (D["posicao_aberto"] == 0) & volta, "posicao_aberto"] = np.nan
        D.loc[D["ativo"].isin(_SEM_POSICAO), "posicao_aberto"] = np.nan
        ativo = ((D["contratos"].fillna(0) > 0) | (D["oi_abertura"] > 0)
                 | (D["posicao_aberto"].fillna(0) > 0))
        blocos.append(D[ativo])

    if fora:
        logger.info("b3_precos: codigos fora do padrao ignorados: %s",
                    sorted(fora, key=fora.get, reverse=True)[:10])
    if not blocos:
        return pd.DataFrame()
    P = pd.concat(blocos, ignore_index=True)
    P["vencimento"] = pd.to_datetime(P["vencimento"]).dt.date
    neg = P[(P[["contratos", "vol_brl", "vol_usd", "posicao_aberto"]] < 0).any(axis=1)]
    if len(neg):
        raise ValueError(f"b3_precos: quantidade negativa em {len(neg)} linhas:\n{neg.head()}")
    return P
