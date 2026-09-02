"""
Novo CAGED - Cadastro Geral de Empregados e Desempregados (via BCB SGS)

Series SGS coletadas (14 series): **ESTOQUE de empregos formais celetistas**
(nivel, em pessoas), total e por setor de atividade economica -- NAO o saldo
(admissoes menos desligamentos), apesar do que a docstring deste modulo dizia
ate 2026-08. Confirmado ao vivo contra a API do SGS: a serie 28763
(`caged_total`) marca 48.032.308 em 2026-06, ordem de grandeza de um estoque
nacional de vinculos, nao de um fluxo mensal (que roda na casa das centenas de
milhares -- o saldo real de 2026-06 foi 145.161, ver `domain/db/brasil/mte/`).

O saldo/admissoes/desligamentos vem do microdado do FTP do PDET/MTE, em
`mt_caged_setor`/`mt_caged_uf`/`mt_caged_salario` -- e a DIFERENCA MENSAL desta
serie de estoque reproduz aquele saldo (e o que
`analytics/oraculo/brasil/scores.py` ja faz, corretamente, com `diff_1m`).

## O tampao (coluna `fonte`, 2026-08-28)

O BCB publica o estoque com um release de atraso em relacao ao microdado: em
2026-08-28 o SGS parava em 2026-06 e o Novo CAGED ja tinha 2026-07. Como a
diferenca mensal do estoque E o saldo do microdado (medido: mediana do erro
zero em 78 meses, corr 0,9996), o mes que falta e reconstruivel sem estimar
nada:

    estoque(t) = estoque(t-1)  +  saldo do microdado em t

`run()` grava esses meses com `fonte='mte'`; o que veio do SGS fica
`fonte='bcb'`. E auto-corrigivel por construcao: quando o BCB publicar, o
INSERT do SGS sobrescreve valor E fonte pela chave (date, name), e o passo de
tampao seguinte nao acha mais lacuna. Consumidor que quiser distinguir le a
coluna; quem so quer o nivel ignora.

Composicao BCB -> secoes CNAE 2.0 do microdado, toda verificada ao vivo contra
o SGS (entre parenteses, a mediana do erro em 75 meses):

    caged_total     = as 22 secoes, inclusive Z                          (0)
    caged_servicos  = H a U, SEM o Z (com Z a mediana vai a 13 -- o BCB
                      poe o nao identificado no total, nao em servicos)  (0)
    caged_SIUP      = D + E                                              (0)
    os outros 11    = uma secao cada                                     (0)

## Taxonomia setorial

Propria do BCB, que NAO e a das 22 secoes CNAE 2.0 do microdado -- e uma arvore
de 3 niveis com agregados intermediarios, validada ao vivo (2026-08) somando as
partes:
  Total = Agropecuaria + Ind. extrativa + Ind. transformacao + SIUP
          + Construcao + Comercio + Servicos
  SIUP  = Eletricidade e gas + Agua/esgoto/residuos
  Servicos > Transporte/Alojamento/Informacao/Financeiras (subconjunto
          publicado, NAO soma o total de Servicos: os 4 dao ~1/3 do pai --
          7,6 de 23,5 milhoes em 2026-07 --, ha subsetores sem codigo SGS
          proprio. Quem decompoe precisa do residuo por diferenca; e o que
          analytics/brasil/labor_market/caged_tab.py chama de "Demais servicos")

Aditividade, medida com alinhamento por DATA (2026-08-28):

  SIUP = os 2 filhos           EXATO, 0 em todos os 235 meses em que existem
  Total = os 7 setores         -57.655 em 1992, encolhendo monotonicamente
                               (-3.832 em 2006) ate -64 a partir de 2008 e
                               -7 hoje. E o "nao identificado", que era 0,25%
                               do estoque nos anos 1990 e virou arredondamento.

Cobertura: **so 8 das 14 series comecam em 1992-01**. As 6 sub-series
(eletricidade_gas, gestao_residuos e os 4 filhos de Servicos) comecam em
**2007-01**, entao antes disso o agregado existe e a decomposicao nao -- e
casar as series por POSICAO em vez de por data desloca 15 anos sem lancar
excecao nenhuma. Ainda assim e a unica serie longa de emprego formal do
projeto (o microdado do Novo CAGED so comeca em 2020-01).

## Cuidado: o BCB reancora o NIVEL retroativamente

Em algum ponto apos 2024-06 o BCB reancorou toda a serie para baixo, revisando
de 1992-01 a 2024-05 de uma vez. E reancoragem de NIVEL, nao revisao de fluxo:
o deslocamento e praticamente constante em cada serie e a diferenca mes a mes
mudou no maximo 77 vinculos (contra 1,36 milhao de nivel). Medido em 2026-08-28,
comparando a tabela com a API do SGS serie a serie:

    caged_total          -1.357.851      caged_servicos       -893.094
    caged_comercio         -352.974      caged_ind_transf.     -84.564
    caged_agropecuaria      -27.412      caged_construcao       +7.466 (sobe)

Como `run()` so reescreve os ultimos `n_meses`, a revisao nao chegou ao trecho
antigo e a tabela ficou com 389 dos 414 meses no vintage velho. O sintoma nao e
o nivel, que ninguem olha em serie de 34 anos -- e o **y/y**, que ficou
deprimido durante exatamente 12 meses (2024-06 a 2025-05: 380 mil no lugar de
1,74 milhao) e voltou sozinho depois, desenhando um buraco no meio do grafico
que parece evento economico e nao existe na fonte. **Uma revisao de nivel do BCB
exige recarga completa; `n_meses` nao a captura.**

Duas licoes de processo, das duas vezes que isto passou:

  1. O buraco foi achado por um PRINT do relatorio, nao pelo ETL -- nada aqui
     lanca excecao quando dois vintages se encostam. A checagem que vale e
     comparar a tabela inteira contra a API, serie a serie, e exigir zero
     diferencas: e o que `tests/test_sgs_vintage.py` faz, para as 26 tabelas
     que carregam por janela. A varredura que nasceu deste bug achou o mesmo
     defeito, menor, em outras 7.
  2. Esta secao ja afirmava "Corrigido em 2026-08-28 com run(start='all')"
     ANTES de a recarga ter sido executada de fato. Docstring nao e evidencia:
     so escreva que foi corrigido depois de medir de novo.

Banco: macro_brasil.mt_caged
Consumidores: analytics/oraculo/brasil/scores.py, analytics/brasil/labor_market/
"""

import pandas as pd

from connectors.bcb import BCB
from connectors.mysql import MySQLDataRequester, insert_data_into_database

_DATABASE = "macro_brasil"
_TABLE    = "mt_caged"
_SETOR    = "mt_caged_setor"

_SERIES = {
    "caged_total":                       28763,
    "caged_agropecuaria":                28764,
    "caged_ind_extrativa":               28765,
    "caged_ind_transformacao":           28766,
    "caged_SIUP":                        28767,
    "caged_eletricidade_gas":            28768,
    "caged_gestao_residuos":             28769,
    "caged_construcao":                  28770,
    "caged_comercio":                    28771,
    "caged_servicos":                    28772,
    "caged_transp_arm_correios":         28773,
    "caged_aloj_alimentacao":            28774,
    "caged_informacao_comunicacao":      28775,
    "caged_ativ_financeiras_seguros":    28776,
}

# Secoes CNAE 2.0 na ordem A..U, mais o Z (nao identificado). Slugs identicos aos
# que domain/db/brasil/mte/mt_caged_setor.py grava na coluna `categoria`.
_SECOES = [
    "agropecuaria",                                       # A
    "industria_extrativa",                                # B
    "industria_transformacao",                            # C
    "eletricidade_gas",                                   # D
    "agua_esgoto_residuos",                               # E
    "construcao",                                         # F
    "comercio",                                           # G
    "transporte_armazenagem_correio",                     # H
    "alojamento_alimentacao",                             # I
    "informacao_comunicacao",                             # J
    "atividades_financeiras_seguros",                     # K
    "atividades_imobiliarias",                            # L
    "atividades_profissionais_cientificas_tecnicas",      # M
    "atividades_administrativas_servicos_complementares", # N
    "administracao_publica_defesa_seguridade_social",     # O
    "educacao",                                           # P
    "saude_servicos_sociais",                             # Q
    "artes_cultura_esporte_recreacao",                    # R
    "outras_atividades_servicos",                         # S
    "servicos_domesticos",                                # T
    "organismos_internacionais",                          # U
    "nao_identificado",                                   # Z
]

# Serie do BCB -> secoes cujo saldo a alimenta. Ver a docstring do modulo para o
# erro medido de cada linha.
_COMPOSICAO = {
    "caged_total":                    _SECOES,
    "caged_agropecuaria":             ["agropecuaria"],
    "caged_ind_extrativa":            ["industria_extrativa"],
    "caged_ind_transformacao":        ["industria_transformacao"],
    "caged_SIUP":                     ["eletricidade_gas", "agua_esgoto_residuos"],
    "caged_eletricidade_gas":         ["eletricidade_gas"],
    "caged_gestao_residuos":          ["agua_esgoto_residuos"],
    "caged_construcao":               ["construcao"],
    "caged_comercio":                 ["comercio"],
    "caged_servicos":                 _SECOES[7:21],   # H a U, sem o Z
    "caged_transp_arm_correios":      ["transporte_armazenagem_correio"],
    "caged_aloj_alimentacao":         ["alojamento_alimentacao"],
    "caged_informacao_comunicacao":   ["informacao_comunicacao"],
    "caged_ativ_financeiras_seguros": ["atividades_financeiras_seguros"],
}

_bcb = BCB()


def _ler(tabela: str) -> pd.DataFrame | None:
    req = MySQLDataRequester(_DATABASE, tabela)
    req.connect()
    df = req.request_data()
    req.close_connection()
    return df


def tampao() -> pd.DataFrame:
    """Reconstroi os meses que o microdado ja tem e o SGS ainda nao.

    Devolve o DataFrame gravado (vazio quando nao ha lacuna), com fonte='mte'.
    Idempotente: recalcula do zero a cada chamada, a partir do ultimo nivel com
    fonte='bcb' -- entao uma revisao do nivel pelo BCB, ou do saldo pelo MTE, se
    propaga sozinha na proxima execucao.
    """
    est = _ler(_TABLE)
    sal = _ler(_SETOR)
    if est is None or sal is None or est.empty or sal.empty:
        return pd.DataFrame()

    est["date"] = pd.to_datetime(est["date"])
    est["value"] = pd.to_numeric(est["value"])
    sal = sal[sal["metrica"] == "saldo"].copy()
    sal["date"] = pd.to_datetime(sal["date"])
    sal["value"] = pd.to_numeric(sal["value"])
    saldo = sal.pivot_table(index="date", columns="categoria", values="value",
                            aggfunc="sum").fillna(0.0).sort_index()

    # Uma secao nova no microdado sairia do total sem lancar excecao nenhuma --
    # o tampao continuaria somando as 22 conhecidas e o nivel ficaria baixo por
    # um numero pequeno. Mesma logica do registry.py: valida em vez de envelhecer
    # em silencio.
    novas = [c for c in saldo.columns if c not in _SECOES]
    if novas:
        raise ValueError(
            f"mt_caged_setor tem secao(oes) que _SECOES nao conhece: {novas}. "
            "Inclua em _SECOES e no ramo certo de _COMPOSICAO antes de tampar -- "
            "senao o total do tampao fica abaixo do que o BCB vai publicar."
        )

    linhas = []
    for name, secoes in _COMPOSICAO.items():
        base = est[(est["name"] == name) & (est["fonte"] == "bcb")]
        if base.empty:
            continue
        ancora = base["date"].max()
        nivel = float(base.loc[base["date"] == ancora, "value"].iloc[0])

        # So a cauda CONTIGUA: um buraco no microdado interromperia a soma
        # acumulada e produziria um nivel errado sem lancar excecao nenhuma.
        esperado = ancora + pd.DateOffset(months=1)
        for d in saldo.index[saldo.index > ancora]:
            if d != esperado or any(s not in saldo.columns for s in secoes):
                break
            nivel += float(saldo.loc[d, secoes].sum())
            linhas.append({"date": d.date(), "name": name,
                           "value": round(nivel, 5), "fonte": "mte"})
            esperado = d + pd.DateOffset(months=1)

    df = pd.DataFrame(linhas)
    if df.empty:
        print("Tampao: nada a preencher (o SGS esta em dia com o microdado).")
        return df

    meses = sorted({str(d) for d in df["date"]})
    print(f"Tampao: {len(df)} linhas em {len(meses)} mes(es) ({', '.join(meses)}) "
          f"reconstruidas do saldo do microdado -- fonte='mte', provisorio.")
    insert_data_into_database(_DATABASE, _TABLE, df)
    return df


def run(n_meses: int = 24, start: str | None = None, end: str | None = None,
        com_tampao: bool = True) -> None:
    """Atualiza macro_brasil.mt_caged.

    Args:
        n_meses: ultimos N meses (default 24). Ignorado se start/end fornecidos.
                 NAO captura reancoragem de nivel do BCB -- ver a docstring do
                 modulo; para isso, start="all".
        start:   data inicial no formato "DD/MM/YYYY", ou "all" para serie completa.
        end:     data final no formato "DD/MM/YYYY". Default: hoje.
        com_tampao: preenche com o saldo do microdado os meses que o SGS ainda
                 nao publicou (fonte='mte'). Ver `tampao()`.
    """
    if start:
        df = _bcb.get_sgs(_SERIES, start=start, end=end)
    else:
        df = _bcb.get_sgs_ultimos(_SERIES, n=n_meses)

    df = df.copy()
    df["fonte"] = "bcb"
    insert_data_into_database(_DATABASE, _TABLE, df)

    if com_tampao:
        tampao()
