"""Painel mensal para o teste de LSTM na previsao do IPCA 12 meses a frente.

CONVENCAO DE INDEXACAO (leia antes de mexer)
--------------------------------------------
A linha `t` do painel contem SO o que estava publicado no fim do mes `t`, e o
alvo sao os 12 proximos IPCA que ainda nao sairam: meses `t`, `t+1`, ..., `t+11`.

O IPCA do mes `t` entra no ALVO e nao nas features, porque ele so e divulgado em
`t+1` (o de julho/2026 saiu em ~13/08). Indexar pelo mes de referencia e ler
`date <= t` daria o IPCA de `t` como conhecido, sem lancar excecao nenhuma. E a
mesma regra de corte que `condicoes_copom.py` documenta.

As defasagens de publicacao estao declaradas em LAGS_PUBLICACAO, em meses, uma
por serie. Sao conservadoras de proposito: quando a fonte publica no meio do mes
seguinte, arredonda-se para cima. Trocar um numero ali muda o conjunto de
informacao do modelo inteiro, entao mexa com o motivo escrito no commit.
"""

from __future__ import annotations

import os
from pathlib import Path

import mysql.connector
import numpy as np
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

DATA = Path(__file__).parent / "data"
PAINEL_CSV = DATA / "painel_mensal.csv"

HORIZONTE = 12  # meses previstos por amostra

# Defasagem de PUBLICACAO, em meses. Ver docstring.
LAGS_PUBLICACAO = {
    "ipca": 1,        # mes M sai em ~M+1 dia 10
    "focus_12m": 0,   # pesquisa semanal, praticamente tempo real
    "icbr_usd": 1,    # indice mensal do BCB
    "ptax": 0,        # diario
    "ibcbr": 2,       # mes M sai ~45 dias depois
    "hiato_bc": 4,    # trimestral, anexo do RPM: ~1 trimestre de atraso
    "selic": 0,       # o comunicado sai as ~18:30 do dia 2 da reuniao
}


def _conn(schema: str = "macro_brasil"):
    return mysql.connector.connect(
        host=os.environ["MYSQL_HOST"],
        user=os.environ["MYSQL_USER"],
        password=os.environ["MYSQL_PASSWORD"],
        database=schema,
    )


def _mensal(s: pd.Series) -> pd.Series:
    """Reindexa para inicio de mes, sem preencher buraco."""
    s = s.sort_index()
    s.index = pd.to_datetime(s.index).to_period("M").to_timestamp()
    return s[~s.index.duplicated(keep="last")]


# --------------------------------------------------------------------------- #
# Series brutas
# --------------------------------------------------------------------------- #
def carregar_bruto() -> dict[str, pd.Series]:
    """As series na frequencia nativa, sem defasagem nem transformacao."""
    cn = _conn()
    try:
        # IPCA: variacao % MENSAL (a tabela ja guarda a taxa, nao o indice)
        ipca = pd.read_sql(
            "SELECT date, value FROM inflc_agregados "
            "WHERE name = 'ipca' ORDER BY date",
            cn,
        ).set_index("date")["value"].astype(float)

        # Focus: expectativa suavizada de IPCA para 12 meses a frente.
        # base_calculo = 0 e a amostra cheia (1 restringe aos ultimos 30 dias).
        focus = pd.read_sql(
            "SELECT date, mediana FROM expc_focus "
            "WHERE indicador = 'IPCA' AND horizonte = '12m' "
            "AND suavizada = 'S' AND base_calculo = 0 AND tipo_calculo = 'geral' "
            "ORDER BY date",
            cn,
        ).set_index("date")["mediana"].astype(float)

        # Commodities em USD (indice de commodities Brasil, dolarizado)
        icbr = pd.read_sql(
            "SELECT date, value FROM comm_icbr_usd "
            "WHERE name = 'icbr_usd' ORDER BY date",
            cn,
        ).set_index("date")["value"].astype(float)

        # Cambio: PTAX venda, diario
        ptax = pd.read_sql(
            "SELECT date, value FROM cmb_ptax "
            "WHERE name = 'ptax_venda' ORDER BY date",
            cn,
        ).set_index("date")["value"].astype(float)

        # IBC-Br dessazonalizado: base do hiato mensal
        ibcbr = pd.read_sql(
            "SELECT date, value FROM atv_ibcbr "
            "WHERE name = 'ibcbr_sa' ORDER BY date",
            cn,
        ).set_index("date")["value"].astype(float)

        # Selic decidida por reuniao do Copom. Nao vem de texto: `pm_copom_reuniao`
        # deriva da SGS 432 cruzada com o calendario de reunioes.
        copom = pd.read_sql(
            "SELECT date, selic_decidida FROM pm_copom_reuniao ORDER BY date",
            cn,
        ).set_index("date")["selic_decidida"].astype(float)

        # Selic esperada da Focus, por ANO de referencia (fim de periodo).
        # Duas linhas por data (ano corrente e seguintes) - a interpolacao para
        # 12 meses a frente e feita em `selic_esperada_12m`.
        selic_exp = pd.read_sql(
            "SELECT date, data_referencia, mediana FROM expc_focus_periodo "
            "WHERE indicador = 'Selic' AND periodicidade = 'anual' "
            "AND base_calculo = 0 AND tipo_calculo = 'geral' "
            "ORDER BY date, data_referencia",
            cn,
        )

        # Hiato do BC (trimestral) - usado como VALIDACAO do hiato mensal
        hiato_bc = pd.read_sql(
            "SELECT date, value FROM pm_hiato_produto "
            "WHERE variavel = 'central' ORDER BY date",
            cn,
        ).set_index("date")["value"].astype(float)
    finally:
        cn.close()

    ptax.index = pd.to_datetime(ptax.index)

    # Selic em vigor no fim de cada mes: passo por reuniao, propagado para
    # frente. A taxa nova vale do dia util seguinte a decisao, entao a reuniao
    # do dia 5 ja governa o fim daquele mes. Os 8 movimentos por vies fora de
    # reuniao (coluna `alterada_fora_da_reuniao`) nao sao tratados a parte:
    # numa serie mensal eles caem no mesmo mes da reuniao seguinte.
    copom.index = pd.to_datetime(copom.index)
    selic_m = copom.resample("MS").last()
    selic_m = selic_m.reindex(
        pd.date_range(selic_m.index.min(), ptax.index.max(), freq="MS")
    ).ffill()

    return {
        "ipca": _mensal(ipca),
        "focus_12m": _mensal(focus),  # ultima pesquisa do mes
        "icbr_usd": _mensal(icbr),
        "ptax_media": _mensal(ptax.resample("MS").mean()),
        "ptax_fim": _mensal(ptax.resample("MS").last()),
        "ibcbr": _mensal(ibcbr),
        "hiato_bc": _mensal(hiato_bc),
        "selic": _mensal(selic_m),
        "selic_exp_anual": selic_exp,
    }


# --------------------------------------------------------------------------- #
# Hiato mensal
# --------------------------------------------------------------------------- #
HP_LAMB = 14400  # convencao mensal
HP_MIN_OBS = 60  # 5 anos antes de confiar numa tendencia HP


def hiato_ibcbr_bilateral(ibcbr: pd.Series, lamb: float = HP_LAMB) -> pd.Series:
    """Hiato HP sobre a amostra INTEIRA. NAO use para treinar.

    O filtro e bilateral: o valor de 2010 muda quando chega dado de 2026. Fica
    aqui so para medir o quanto o vazamento embelezaria o resultado.
    """
    from statsmodels.tsa.filters.hp_filter import hpfilter

    s = ibcbr.dropna()
    if len(s) < HP_MIN_OBS:
        return pd.Series(dtype=float, name="hiato_bilateral")
    ciclo, _tend = hpfilter(np.log(s), lamb=lamb)
    return (ciclo * 100).rename("hiato_bilateral")


def hiato_ibcbr_realtime(ibcbr: pd.Series, lamb: float = HP_LAMB) -> pd.Series:
    """Hiato em TEMPO REAL: para cada mes m, roda o HP so com dado ate m e
    guarda a ULTIMA observacao do ciclo.

    E o que separa esta funcao de `hiato_ibcbr_bilateral`, e a diferenca nao e
    cosmetica. O HP e bilateral, entao filtrar a amostra toda e depois cortar o
    teste injeta futuro em cada ponto historico - o vazamento nao lanca excecao,
    so melhora o RMSE. Aqui cada ponto ve exatamente o que existia na epoca.

    O vies de ponta entra de proposito: e ele que o previsor de verdade enfrenta.
    Fica ~280 execucoes do filtro, poucos segundos.
    """
    from statsmodels.tsa.filters.hp_filter import hpfilter

    s = ibcbr.dropna()
    if len(s) < HP_MIN_OBS:
        return pd.Series(dtype=float, name="hiato")

    log_s = np.log(s)
    vals: dict[pd.Timestamp, float] = {}
    for i in range(HP_MIN_OBS, len(log_s) + 1):
        janela = log_s.iloc[:i]
        ciclo, _tend = hpfilter(janela, lamb=lamb)
        vals[janela.index[-1]] = float(ciclo.iloc[-1]) * 100
    return pd.Series(vals, name="hiato").sort_index()


# --------------------------------------------------------------------------- #
# Selic esperada a 12 meses
# --------------------------------------------------------------------------- #
def selic_esperada_12m(selic_exp_anual: pd.DataFrame) -> pd.Series:
    """i^e: a Selic esperada NO PONTO 12 meses a frente, nao a media do caminho.

    A distincao e do proprio BC e esta medida em
    `analytics/brasil/monetary_policy/CLAUDE.md`: contra a Tabela 1 do boxe da
    neutra, o ponto erra +0,14 e a media do caminho +0,82.

    A Focus anual publica a Selic de FIM DE ANO. Doze meses a frente do mes `m`
    do ano `Y` e o mes `m` do ano `Y+1`, que fica a fracao `m/12` do caminho
    entre o fim de `Y` e o fim de `Y+1` - dai a interpolacao linear entre as
    duas referencias anuais. Nos extremos ela degenera no lugar certo: em
    dezembro devolve exatamente a expectativa de fim do ano seguinte.
    """
    df = selic_exp_anual.copy()
    df["date"] = pd.to_datetime(df["date"])
    df["ano"] = df["data_referencia"].astype(str).str.slice(0, 4).astype(int)
    piv = df.pivot_table(index="date", columns="ano", values="mediana", aggfunc="last")

    vals: dict[pd.Timestamp, float] = {}
    for d, linha in piv.iterrows():
        y, m = d.year, d.month
        a, b = linha.get(y), linha.get(y + 1)
        if pd.isna(a) or pd.isna(b):
            continue
        w = m / 12.0
        vals[d] = float(a) * (1 - w) + float(b) * w
    s = pd.Series(vals, name="selic_e12").sort_index()
    return _mensal(s)  # ultima pesquisa de cada mes


# --------------------------------------------------------------------------- #
# Painel
# --------------------------------------------------------------------------- #
# As 3 defasagens extras de IPCA existem para os modelos PLANOS (AR/Ridge), que
# veem uma linha por vez e nao teriam historico sem elas. O LSTM recebe a janela
# inteira e as veria de qualquer jeito - ficam no conjunto comum porque o
# protocolo de comparacao exige que todo mundo enxergue as mesmas features.
# A de 12 meses e a sazonal: fevereiro do ano passado informa fevereiro deste.
FEATURES_ECON = [
    "ipca_m",
    "ipca_m_l2",
    "ipca_m_l3",
    "ipca_m_l12",
    "ipca_12m",
    "focus_12m",
    "focus_d",
    "hiato",
    "icbr_dlog",
    "ptax_dlog",
    # --- politica monetaria (2026-09-02) - VER "CAUSALIDADE REVERSA" abaixo -- #
    "selic",
    "selic_d12",
    "juro_real_e",
]

# CAUSALIDADE REVERSA: o que estas tres features NAO significam
# -------------------------------------------------------------
# A Selic sobe QUANDO a inflacao esperada sobe - e por isso que o Copom existe.
# Entao um modelo de previsao vai muito provavelmente aprender uma relacao
# POSITIVA entre Selic e inflacao futura, e ela nao e o efeito da politica: e o
# Copom reagindo a informacao que o modelo tambem esta lendo.
#
# Para PREVER isso e legitimo e util - a Selic e um sinal de que o BC viu
# pressao. O que e ilegitimo e ler o coeficiente como multiplicador de politica
# ou usar este modelo para responder "e se a Selic fosse a 12%". Aquela pergunta
# pertence ao modelo estrutural desta pasta (`modelo_agregado.py`), onde a
# resposta vem de restricao imposta e nao de correlacao estimada.
#
# As tres medem coisas diferentes de proposito:
#   selic       nivel, % a.a. - a POSTURA. E a mais suspeita das tres: em
#               2008-2014 (primeiro fold de treino) ela varia entre ~7 e 14%, e
#               os 2% de 2020 caem FORA desse suporte. ReLU extrapola linearmente
#               fora do intervalo visto, o que e exatamente o modo de falha que
#               a regra de estacionariedade no topo deste arquivo existe para
#               evitar. Se algo parecer estranho em 2020-2021, suspeite dela.
#   selic_d12   variacao em 12 meses, p.p. - a ACAO. Estacionaria por construcao.
#   juro_real_e i^e - pi^e, diferenca simples, como na eq. (2.1) do boxe do BC
#               (Fisher exato descola ~0,2 p.p. e a convencao da casa e a
#               simples). E o objeto teoricamente certo para postura, e o unico
#               que nao confunde "juro alto" com "juro alto porque a inflacao
#               esta alta".

# Dummies de mes-calendario (2026-09-02, a pedido do usuario). Uma coluna por
# mes, ligada quando a linha e daquele mes.
#
# TRES DECISOES, cada uma com uma alternativa que parece equivalente e nao e:
#
# 1. UMA POR MES, nao seno/cosseno do angulo do mes. O par sin/cos custaria 2
#    features em vez de 12, mas IMPOE SUAVIDADE ao longo do ano - e a
#    sazonalidade do IPCA nao e suave: fevereiro e um degrau (reajuste de
#    ensino), nao um ponto de uma onda. Codificacao ciclica brigaria com o dado
#    exatamente no mes que mais importa.
# 2. AS 12, nao 11. Com vies nas camadas, 12 dummies sao colineares com ele -
#    o que num OLS seria matriz singular e aqui e so capacidade redundante. As
#    12 mantem a simetria (nenhum mes vira categoria de referencia implicita) e
#    custam 128 parametros a mais, o que e barato contra o risco de ler
#    coeficiente de mes como desvio contra dezembro sem perceber.
# 3. SEM DEFASAGEM DE PUBLICACAO. O calendario nao e divulgado por ninguem:
#    saber que a linha e de marco nao usa informacao que nao existia. Elas
#    entram em `shifts` com 0 de proposito, e nao por omissao.
#
# A dummy vale em TODO passo da janela, nao so no ultimo: numa janela de 24
# meses cada mes aparece exatamente 2 vezes, entao a rede pode alinhar o
# `ipca_m` de cada passo com o mes dele em vez de so saber onde ela esta hoje.
MESES_ABREV = [
    "jan", "fev", "mar", "abr", "mai", "jun",
    "jul", "ago", "set", "out", "nov", "dez",
]
FEATURES_CAL = [f"mes_{m}" for m in MESES_ABREV]

FEATURES = FEATURES_ECON + FEATURES_CAL
ALVOS = [f"y_h{h}" for h in range(1, HORIZONTE + 1)]


def montar_painel(
    bruto: dict[str, pd.Series] | None = None,
    hiato_vazado: bool = False,
) -> pd.DataFrame:
    """Painel mensal com as features defasadas pela data de publicacao.

    O hiato e de TEMPO REAL por construcao (ver `hiato_ibcbr_realtime`), entao
    o painel e o mesmo em todos os folds - nao ha o que recalcular por refit.

    `hiato_vazado=True` troca pelo HP bilateral e serve para UMA coisa: medir
    quanto o vazamento embelezaria o resultado. Nunca para reportar numero.

    `bruto` permite reaproveitar uma leitura do banco.
    """
    b = bruto if bruto is not None else carregar_bruto()
    hiato = (
        hiato_ibcbr_bilateral(b["ibcbr"]).rename("hiato")
        if hiato_vazado
        else hiato_ibcbr_realtime(b["ibcbr"])
    )

    cru = pd.DataFrame(
        {
            "ipca": b["ipca"],
            "focus_12m": b["focus_12m"],
            "icbr_usd": b["icbr_usd"],
            "ptax": b["ptax_media"],
            "hiato_ibcbr": hiato,
            "selic": b["selic"],
            "selic_e12": selic_esperada_12m(b["selic_exp_anual"]),
            "hiato_bc": b["hiato_bc"],  # trimestral, so para confronto
        }
    )
    grade = pd.date_range(cru.index.min(), cru.index.max(), freq="MS")
    cru = cru.reindex(grade)

    # --- transformacoes (ver CLAUDE.md da pasta) ---------------------------- #
    f = pd.DataFrame(index=grade)
    f["ipca_m"] = cru["ipca"]  # ja e taxa %
    f["ipca_m_l2"] = cru["ipca"].shift(1)
    f["ipca_m_l3"] = cru["ipca"].shift(2)
    f["ipca_m_l12"] = cru["ipca"].shift(11)
    f["ipca_12m"] = (
        cru["ipca"].div(100).add(1).rolling(12).apply(np.prod, raw=True).sub(1).mul(100)
    )
    f["focus_12m"] = cru["focus_12m"]  # nivel %
    f["focus_d"] = cru["focus_12m"].diff()  # revisao
    f["hiato"] = cru["hiato_ibcbr"]  # nivel (desvio %)
    f["icbr_dlog"] = np.log(cru["icbr_usd"]).diff().mul(100)
    f["ptax_dlog"] = np.log(cru["ptax"]).diff().mul(100)
    f["selic"] = cru["selic"]                       # nivel, % a.a.
    f["selic_d12"] = cru["selic"].diff(12)          # acao de politica, p.p.
    f["juro_real_e"] = cru["selic_e12"] - cru["focus_12m"]  # i^e - pi^e
    for i, nome in enumerate(FEATURES_CAL, start=1):
        f[nome] = (grade.month == i).astype(float)

    # --- defasagem de PUBLICACAO ------------------------------------------- #
    # Os nomes ja descrevem a defasagem FINAL: `ipca_m_l12` = shift(11) interno
    # + 1 de publicacao = IPCA de t-12, a mesma referencia sazonal do alvo.
    shifts = {
        "ipca_m": LAGS_PUBLICACAO["ipca"],
        "ipca_m_l2": LAGS_PUBLICACAO["ipca"],
        "ipca_m_l3": LAGS_PUBLICACAO["ipca"],
        "ipca_m_l12": LAGS_PUBLICACAO["ipca"],
        "ipca_12m": LAGS_PUBLICACAO["ipca"],
        "focus_12m": LAGS_PUBLICACAO["focus_12m"],
        "focus_d": LAGS_PUBLICACAO["focus_12m"],
        "hiato": LAGS_PUBLICACAO["ibcbr"],
        "icbr_dlog": LAGS_PUBLICACAO["icbr_usd"],
        "ptax_dlog": LAGS_PUBLICACAO["ptax"],
        "selic": LAGS_PUBLICACAO["selic"],
        "selic_d12": LAGS_PUBLICACAO["selic"],
        "juro_real_e": LAGS_PUBLICACAO["selic"],
        # O calendario nao tem data de divulgacao - ver a nota em FEATURES_CAL.
        **{c: 0 for c in FEATURES_CAL},
    }
    X = pd.DataFrame({c: f[c].shift(shifts[c]) for c in FEATURES}, index=grade)

    # --- alvo: os 12 IPCA que ainda nao sairam em `t` ----------------------- #
    # y_h1 = IPCA do proprio mes t (sai em t+1), ..., y_h12 = IPCA de t+11.
    alvo = pd.DataFrame(
        {f"y_h{h}": cru["ipca"].shift(-(h - 1)) for h in range(1, HORIZONTE + 1)},
        index=grade,
    )

    painel = pd.concat([X, alvo, cru[["hiato_bc"]]], axis=1)
    painel.index.name = "date"
    return painel


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    p = montar_painel()
    p.to_csv(PAINEL_CSV, float_format="%.6f")

    completo = p.dropna(subset=FEATURES)
    treinavel = p.dropna(subset=FEATURES + ALVOS)
    print(f"painel gravado em {PAINEL_CSV}")
    print(
        f"  grade             : {p.index.min():%Y-%m} a {p.index.max():%Y-%m}"
        f"  ({len(p)} meses)"
    )
    print(
        f"  features completas: {completo.index.min():%Y-%m} a"
        f" {completo.index.max():%Y-%m}  ({len(completo)})"
    )
    print(
        f"  com alvo completo : {treinavel.index.min():%Y-%m} a"
        f" {treinavel.index.max():%Y-%m}  ({len(treinavel)})"
    )
    print()
    print("cobertura por coluna (primeiro/ultimo nao-nulo):")
    for c in FEATURES_ECON:
        s = p[c].dropna()
        print(f"  {c:12s} {s.index.min():%Y-%m} .. {s.index.max():%Y-%m}   n={len(s):4d}")

    # Confronto hiato mensal x hiato do BC, nos trimestres em que os dois existem
    j = p[["hiato", "hiato_bc"]].dropna()
    if len(j) > 8:
        print()
        print(
            f"hiato IBC-Br x hiato BC: corr={j['hiato'].corr(j['hiato_bc']):+.3f}"
            f"  em {len(j)} trimestres"
        )


if __name__ == "__main__":
    main()
