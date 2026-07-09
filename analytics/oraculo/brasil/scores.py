"""
Oraculo Brasil — Calculo de notas macro para o termometro.

Banco de dados: macro_brasil
"""

from pathlib import Path

import pandas as pd

from connectors.mysql import MySQLDataRequester
from utils.thermometer import Score, Score_SMC, Score_SA
from utils.transforms import (pivot_table_to_long as unpivot,
                               expand_to_monthly as Expandir_Frequencia,
                               marginal_to_interanual_change, marginal_to_index)

_N = 11000  # janela maxima de observacoes na saida

# --- Dados carregados por _load_data() ----------------------------------------
_data_inflacao           = None   # wide: IPCA, IPCA_Nucleo_MediasAparadasSuavizadas, Indice_Difusao, ...
_data_expectativas       = None   # wide: coluna 'mediana' (IPCA 12m, resample MS)
_data_caged              = None   # wide: caged_total, ...
_data_forca_trabalho     = None   # wide: ocupado, desocupado (region='Brasil')
_data_credito            = None   # wide: emp_* + total_credito_ampliado_empresas
_data_condicoes_familias = None   # wide: endividamento_renda, comp_renda_juros, comp_renda_servico_total
_data_gdp                = None   # wide: 'Agropecuária - total', 'Indústria - total', 'Serviços - total'
_data_pms                = None   # wide: 'Total' (servicos_total SA)
_data_pim                = None   # wide: industria_geral (SA)
_data_ibc_br             = None   # wide: ibcbr_sa


def _load_data() -> None:
    """Carrega todos os DataFrames de macro_brasil para as variaveis globais."""
    global _data_inflacao, _data_expectativas, _data_caged, _data_forca_trabalho, \
           _data_credito, _data_condicoes_familias, _data_gdp, _data_pms, \
           _data_pim, _data_ibc_br

    # -- Inflacao --
    req = MySQLDataRequester('macro_brasil', 'inflc_agregados')
    req.connect()
    _data_inflacao = req.long_to_wide(req.request_data()).astype(float).rename(columns={
        'ipca_nucleo_medias_aparadas': 'IPCA_Nucleo_MediasAparadasSuavizadas',
        'ipca_indice_difusao':         'Indice_Difusao',
        'ipca':                        'IPCA',
    })

    # -- Expectativas Focus --
    req = MySQLDataRequester('macro_brasil', 'expc_focus')
    req.connect()
    df = req.request_data()
    mask = (df['indicador'] == 'IPCA') & (df['horizonte'] == '12m')
    df_exp = df[mask][['date', 'mediana']].copy()
    df_exp['date'] = pd.to_datetime(df_exp['date'])
    _data_expectativas = (df_exp.sort_values('date')
                                .set_index('date')[['mediana']]
                                .resample('MS').last()
                                .astype(float))

    # -- CAGED --
    req = MySQLDataRequester('macro_brasil', 'mt_caged')
    req.connect()
    _data_caged = req.long_to_wide(req.request_data()).astype(float)

    # -- PNAD: forca de trabalho --
    # region='Brasil' obrigatorio — pnad tem chave (date, name, region) e multiplas regioes
    req = MySQLDataRequester('macro_brasil', 'mt_pnad')
    req.connect()
    df = req.request_data()
    mask = df['name'].isin(['ocupado', 'desocupado']) & (df['region'] == 'Brasil')
    _data_forca_trabalho = MySQLDataRequester.long_to_wide(df[mask].copy()).astype(float)

    # -- Credito --
    req = MySQLDataRequester('macro_brasil', 'cred_credito_amplo')
    req.connect()
    _data_credito = req.long_to_wide(req.request_data()).astype(float)
    emp_cols = [c for c in _data_credito.columns if c.startswith('emp_')]
    _data_credito['total_credito_ampliado_empresas'] = _data_credito[emp_cols].sum(axis=1)

    # -- Condicoes financeiras familias --
    req = MySQLDataRequester('macro_brasil', 'cred_credito_familias')
    req.connect()
    _data_condicoes_familias = req.long_to_wide(req.request_data()).astype(float)

    # -- GDP --
    req = MySQLDataRequester('macro_brasil', 'atv_pib')
    req.connect()
    df = req.request_data()
    _data_gdp = (req.long_to_wide(df[df['seasonal_adjs'] == 'Y'].copy())
                    [['agropecuaria', 'industria', 'servicos']]
                    .astype(float)
                    .rename(columns={
                        'agropecuaria': 'Agropecuária - total',
                        'industria':    'Indústria - total',
                        'servicos':     'Serviços - total',
                    }))

    # -- PMS --
    req = MySQLDataRequester('macro_brasil', 'atv_pms')
    req.connect()
    df = req.request_data()
    _data_pms = (req.long_to_wide(df[df['seasonal_adjs'] == 'Y'].copy())
                    [['servicos_total']]
                    .astype(float)
                    .rename(columns={'servicos_total': 'Total'}))

    # -- PIM --
    req = MySQLDataRequester('macro_brasil', 'atv_pim')
    req.connect()
    df = req.request_data()
    _data_pim = (req.long_to_wide(df[df['seasonal_adjs'] == 'Y'].copy())
                    [['industria_geral']]
                    .astype(float))

    # -- IBC-BR --
    req = MySQLDataRequester('macro_brasil', 'atv_ibcbr')
    req.connect()
    df = req.request_data()
    _data_ibc_br = req.long_to_wide(df[df['name'] == 'ibcbr_sa'].copy()).astype(float)


# --- Helper: finaliza frames de scoring ---------------------------------------

def _finalize(*frames) -> pd.DataFrame:
    """Aplica tail, unpivot e concat em todos os frames de scoring."""
    return pd.concat([unpivot(f.tail(_N)) for f in frames]).dropna()


# --- Calculo de notas: INFLACAO -----------------------------------------------

def ipca():
    df = _data_inflacao[['IPCA']].copy()
    df['yoy'] = list(marginal_to_interanual_change(df['IPCA']))
    df = df.dropna()
    return _finalize(
        Score(df['yoy'],  -1, 'IPCA - [Var(Yt, 12)]',        False),
        Score(df['IPCA'], -1, 'IPCA - [Var(Yt, 1)]',          False),
        Score_SMC(df['IPCA'], -1, 'IPCA - [SMC(Var(Yt, 1))]'),
    )


def nucleo_ipca():
    col = 'IPCA_Nucleo_MediasAparadasSuavizadas'
    df = _data_inflacao[[col]].copy().dropna()
    df['yoy'] = list(marginal_to_interanual_change(df[col]))
    df = df.dropna()
    return _finalize(
        Score(df['yoy'], -1, 'Núcleo IPCA - [Var(Yt, 12)]'),
        Score(df[col],   -1, 'Núcleo IPCA - [Var(Yt, 1)]'),
        Score_SMC(df[col], -1, 'Núcleo IPCA - [SMC(Var(Yt, 1))]'),
    )


def indice_difusao():
    df = _data_inflacao[['Indice_Difusao']].copy()
    df['diff_1m'] = df['Indice_Difusao'] - df['Indice_Difusao'].shift(1)
    df = df.dropna()
    return _finalize(
        Score(df['Indice_Difusao'], -1, 'Indice de difusão - [MA (Yt, 12)]', True, 12),
        Score(df['diff_1m'],        -1, 'Indice de difusão - [diff(Yt, 1)]'),
        Score_SA(df['Indice_Difusao'], -1, 'Indice de difusão - [SA(Yt)]'),
    )


def expectativas():
    df = _data_expectativas.copy()
    df['diff_1m'] = df['mediana'] - df['mediana'].shift(1)
    return _finalize(
        Score(df['diff_1m'], -1, '12m_Expect Inflação - [Diff(Yt, 1)]', False),
    )


# --- Calculo de notas: MERCADO DE TRABALHO ------------------------------------

def caged():
    df = _data_caged[['caged_total']].copy()
    df['diff_1m'] = df['caged_total'] - df['caged_total'].shift(1)
    df = df.dropna()
    return _finalize(
        Score(df['diff_1m'], 1, 'CAGED - [MA(diff(Yt, 1), 12)]', True, 12),
        Score(df['diff_1m'], 1, 'CAGED - [diff(Yt, 1)]'),
        Score_SMC(df['diff_1m'], 1, 'CAGED - [SMC(diff(Yt, 1))]'),
    )


def tx_desemprego():
    df = pd.DataFrame(index=_data_forca_trabalho.index)
    df['taxa'] = (
        _data_forca_trabalho['desocupado']
        / (_data_forca_trabalho['desocupado'] + _data_forca_trabalho['ocupado'])
    ) * 100
    df['diff_1m'] = df['taxa'] - df['taxa'].shift(1)
    df = df.dropna()
    return _finalize(
        Score(df['diff_1m'], -1, 'Taxa de desemprego - [MA(diff(Yt, 1), 12)]', True, 12),
        Score(df['diff_1m'], -1, 'Taxa de desemprego - [diff(Yt, 1)]'),
        Score_SA(df['taxa'], -1, 'Taxa de desemprego - [SA(Yt)]'),
    )


# --- Calculo de notas: CONDICOES FINANCEIRAS ----------------------------------

def saldo_credito_empresas():
    deflator = marginal_to_index(_data_inflacao['IPCA'], '2013/01/01', '2013/01/01') / 100
    deflator = deflator.reindex(_data_credito.index)
    df = pd.DataFrame(index=_data_credito.index)
    df['credito_real'] = _data_credito['total_credito_ampliado_empresas'] / deflator
    df['diff_1m'] = df['credito_real'] - df['credito_real'].shift(1)
    df = df.dropna()
    return _finalize(
        Score(df['diff_1m'], 1, 'Saldo de Credito (Empresas) - [MA(diff(Yt, 1), 12)]', True, 12),
        Score(df['diff_1m'], 1, 'Saldo de Credito (Empresas) - [diff(Yt, 1)]'),
        Score_SMC(df['diff_1m'], 1, 'Saldo de Credito (Empresas) - [SMC(diff(Yt, 1))]'),
    )


def divida_renda():
    df = _data_condicoes_familias[['endividamento_renda']].copy()
    df['diff_1m'] = df['endividamento_renda'] - df['endividamento_renda'].shift(1)
    df = df.dropna()
    return _finalize(
        Score(df['endividamento_renda'], -1, 'Dívida/Renda (Famílias) - [Yt]'),
        Score(df['diff_1m'],             -1, 'Dívida/Renda (Famílias) - [diff(Yt, 1)]'),
        Score(df['diff_1m'],             -1, 'Dívida/Renda (Famílias) - [MA(diff(Yt, 1), 12)]', True, 12),
    )


def serv_divida_renda():
    df = _data_condicoes_familias[['comp_renda_servico_total']].copy()
    df.columns = ['total_servico']
    df['diff_1m'] = df['total_servico'] - df['total_servico'].shift(1)
    df = df.dropna()
    return _finalize(
        Score(df['total_servico'], -1, 'Serviço da dívida/Renda (Famílias) - [Yt]'),
        Score(df['diff_1m'],       -1, 'Serviço da dívida/Renda (Famílias) - [diff(Yt, 1)]'),
        Score(df['diff_1m'],       -1, 'Serviço da dívida/Renda (Famílias) - [MA(diff(Yt, 1), 12)]', True, 12),
    )


# --- Calculo de notas: GDP ----------------------------------------------------

def _gdp_sector_score(col: str, label: str) -> pd.DataFrame:
    df = _data_gdp[[col]].copy()
    df['yoy']       = df[col] / df[col].shift(4) - 1
    df['acum4']     = df[col].rolling(window=4, min_periods=4).sum()
    df['var_acum4'] = df['acum4'] / df['acum4'].shift(4) - 1
    df['mom']       = df[col] / df[col].shift(1) - 1
    df = df.dropna()
    return _finalize(
        Expandir_Frequencia(Score(df['yoy'],       1, f'{label} - [Var(Yt, 4)]',   False), 'date', f'{label} - [Var(Yt, 4)]'),
        Expandir_Frequencia(Score(df['var_acum4'], 1, f'{label} - [Var(Acum(4))]', False), 'date', f'{label} - [Var(Acum(4))]'),
        Expandir_Frequencia(Score(df['mom'],       1, f'{label} - [Var(Yt, 1)]',   False), 'date', f'{label} - [Var(Yt, 1)]'),
    )


def gdp_indice_sa_agro():
    return _gdp_sector_score('Agropecuária - total', 'PIB AGRO')


def gdp_indice_sa_industria():
    return _gdp_sector_score('Indústria - total', 'PIB Industrial')


def gdp_indice_sa_servicos():
    return _gdp_sector_score('Serviços - total', 'PIB de Serviços')


# --- Calculo de notas: PESQUISAS MENSAIS --------------------------------------

def _pesquisa_score(data: pd.DataFrame, col: str, label: str) -> pd.DataFrame:
    df = data[[col]].copy()
    df['yoy']        = (df[col] / df[col].shift(12) - 1) * 100
    df['acum12']     = df[col].rolling(window=12, min_periods=12).sum()
    df['var_acum12'] = (df['acum12'] / df['acum12'].shift(12) - 1) * 100
    df['mom']        = (df[col] / df[col].shift(1) - 1) * 100
    df = df.dropna()
    return _finalize(
        Score(df['yoy'],        1, f'{label} - [Var(Yt, 12)]',   False),
        Score(df['var_acum12'], 1, f'{label} - [Var(Acum(12))]', False),
        Score(df['mom'],        1, f'{label} - [Var(Yt, 1)]',    False),
    )


def pms():
    return _pesquisa_score(_data_pms, 'Total', 'PMS')


def pim():
    return _pesquisa_score(_data_pim, 'industria_geral', 'PM_I')


def ibc_br():
    df = _data_ibc_br[['ibcbr_sa']].copy()
    df['yoy'] = (df['ibcbr_sa'] / df['ibcbr_sa'].shift(12) - 1) * 100
    df['mom'] = (df['ibcbr_sa'] / df['ibcbr_sa'].shift(1)  - 1) * 100
    df = df.dropna()
    return _finalize(
        Score(df['yoy'], 1, 'IBC_BR - [Var(Yt, 12)]',     False),
        Score(df['yoy'], 1, 'IBC_BR - [MA(Var(Yt, 12))]', True, 12),
        Score(df['mom'], 1, 'IBC_BR - [Var(Yt, 1)]',      False),
    )


# --- Entry point --------------------------------------------------------------

def run() -> pd.DataFrame:
    """Atualiza Brasil_base.csv com todas as notas macro do oraculo Brasil."""
    _load_data()

    frames = [
        ipca(),
        nucleo_ipca(),
        indice_difusao(),
        expectativas(),
        tx_desemprego(),
        caged(),
        serv_divida_renda(),
        divida_renda(),
        saldo_credito_empresas(),
        gdp_indice_sa_agro(),
        gdp_indice_sa_industria(),
        gdp_indice_sa_servicos(),
        pms(),
        pim(),
        ibc_br(),
    ]

    df = pd.concat(frames, ignore_index=True)
    path = Path(__file__).resolve().parent / 'base' / 'brasil_base.csv'
    df.to_csv(path, index=False)
    print("Calculo de notas BRL: Executado com sucesso!")
    return df
