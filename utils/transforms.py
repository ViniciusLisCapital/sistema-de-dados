import pandas as pd
import numpy as np
from datetime import datetime, timedelta


# ── Wide → Long ──────────────────────────────────────────────────────────────

def pivot_table_to_long(frame):
    """
    Converts a pivot table (wide format) into a long format DataFrame.

    Args:
        frame (pd.DataFrame): Input pivot table.

    Returns:
        pd.DataFrame: Long format with columns "Values", "Name", "Date".
    """
    Rows, Cols = frame.shape
    data = {
        "Values": frame.to_numpy().ravel("F"),
        "Name":   np.asanyarray(frame.columns).repeat(Rows),
        "Date":   np.tile(np.asanyarray(frame.index), Cols),
    }
    return pd.DataFrame(data)

PivotTable = pivot_table_to_long  # backward compat


# ── Index & variation calculations ───────────────────────────────────────────

def marginal_change_to_index(time_series):
    """Converts a series of monthly % changes into a cumulative index starting at 100."""
    index = []
    cumulative_index = 100
    for change in time_series:
        cumulative_index *= (1 + change / 100)
        index.append(cumulative_index)
    return index


def marginal_to_interanual_change(variacoes_mensais):
    """Converts monthly % changes into year-over-year % changes."""
    indices_precos = [100]
    for variacao in variacoes_mensais:
        indices_precos.append(indices_precos[-1] * (1 + variacao / 100))
    series_indices = pd.Series(indices_precos)
    return (series_indices.pct_change(12) * 100).iloc[1:]


def marginal_to_index(serie, data_inicio_acumulo, data_base_100):
    """
    Builds a cumulative index from monthly % changes, rebased so that
    data_base_100 = 100.

    Args:
        serie (pd.Series): Monthly % changes indexed by date.
        data_inicio_acumulo: Start date for accumulation.
        data_base_100: Date that will equal 100 in the output index.

    Returns:
        pd.Series: Cumulative index.
    """
    serie = serie.sort_index()
    serie.index = pd.to_datetime(serie.index)
    serie = serie.loc[data_inicio_acumulo:]
    indice = (1 + serie / 100).cumprod()
    return (indice / indice.loc[data_base_100]) * 100


def GetIndexFromAFrame(FrameBase, ColumnsToGetIndex, KeepIndex=True):
    """
    Converts multiple DataFrame columns of % changes into cumulative index vectors.

    Args:
        FrameBase (pd.DataFrame): Input DataFrame.
        ColumnsToGetIndex (list): Column names to process.
        KeepIndex (bool): Whether to preserve the original DataFrame index.

    Returns:
        pd.DataFrame: Cumulative index for each requested column.
    """
    result = {}
    for col in ColumnsToGetIndex:
        result[col] = np.cumprod((1 + FrameBase[col] / 100).to_numpy(dtype=float))

    if KeepIndex:
        return pd.DataFrame(result, index=FrameBase.index)
    return pd.DataFrame(result)


def GetIndexOrVar(DataFrame, ColumnToGetIndex, OutName, Index=True, Var=0):
    """
    Takes a column of monthly % changes and either returns the cumulative index
    or a period-over-period variation of that index.

    Args:
        DataFrame (pd.DataFrame): Input frame (modified in place).
        ColumnToGetIndex (str): Column with monthly % changes (MoM).
        OutName (str): Output column name.
        Index (bool): If True, return the index; if False, return the variation.
        Var (int): Number of periods for the variation (e.g. 12 = YoY).

    Returns:
        pd.DataFrame: Modified input DataFrame.
    """
    DataFrame['ColunaAjuste'] = (1 + DataFrame[ColumnToGetIndex] / 100)
    DataFrame['Index'] = DataFrame['ColunaAjuste'].cumprod(axis='index')

    if Index:
        DataFrame.drop(columns=['ColunaAjuste', ColumnToGetIndex], inplace=True)
    else:
        DataFrame[OutName] = ((DataFrame['Index'] / DataFrame['Index'].shift(Var)) - 1) * 100
        DataFrame.drop(columns=['Index', 'ColunaAjuste'], inplace=True)

    return DataFrame


# ── Frequency & date helpers ──────────────────────────────────────────────────

def expand_to_monthly(df, date_col, value_col):
    """
    Expands quarterly data to monthly frequency by forward-filling values.

    Args:
        df (pd.DataFrame): Input frame with quarterly data.
        date_col (str): Name of the date column (format '%Y/%m/%d').
        value_col (str): Name of the value column.

    Returns:
        pd.DataFrame: Monthly-frequency frame indexed by date_col.
    """
    df_q = df.copy()
    df_q.reset_index(inplace=True)
    df_q[date_col] = pd.to_datetime(df_q[date_col], format='%Y/%m/%d')

    date_range = pd.date_range(
        start=df_q[date_col].min(),
        end=df_q[date_col].max() + pd.DateOffset(months=2),
        freq='MS',
    )
    df_monthly = pd.DataFrame({date_col: date_range})
    df_final = pd.merge_asof(df_monthly, df_q, on=date_col, direction='backward')
    df_final[value_col] = df_final[value_col].ffill()
    df_final[date_col] = df_final[date_col].dt.strftime('%d/%m/%Y')
    df_final.set_index(date_col, inplace=True)
    return df_final

Expandir_Frequencia = expand_to_monthly  # backward compat


def get_date_range(offset, freq, just_year=False):
    """
    Returns a (start_date, end_date) tuple for API requests, going `offset`
    periods back from today.

    Args:
        offset (int): Number of periods to go back.
        freq (str): 'M' for monthly (30-day steps) or 'T' for quarterly (90-day steps).
        just_year (bool): If True, return integer years instead of formatted strings.

    Returns:
        tuple: (start, end) as '%d/%m/%Y' strings, or as ints if just_year=True.
    """
    data_final = datetime.now()
    days = offset * (30 if freq == 'M' else 90)
    data_inicial = data_final - timedelta(days=days)

    data_final_str = data_final.strftime('%d/%m/%Y')
    data_inicial_str = data_inicial.strftime('%d/%m/%Y')

    if just_year:
        return (datetime.strptime(data_inicial_str, '%d/%m/%Y').year,
                datetime.strptime(data_final_str, '%d/%m/%Y').year)

    return data_inicial_str, data_final_str

get_relative_date = get_date_range  # backward compat


# ── Deflation ─────────────────────────────────────────────────────────────────

def deflate_series(deflator_df, series_to_deflate):
    """
    Deflates a nominal time series to real values.

    Args:
        deflator_df (pd.DataFrame): Deflation rates (%) indexed by date, single column.
        series_to_deflate (pd.DataFrame): Nominal series indexed by date.

    Returns:
        pd.DataFrame: Deflated series with column name suffixed by '_ia'
                      (inflation adjusted).
    """
    merged = series_to_deflate.merge(deflator_df, how='inner',
                                     left_index=True, right_index=True)
    merged.dropna(axis=0, how='any', inplace=True)

    deflation_index = np.cumprod(1 + np.array(merged[deflator_df.columns] / 100))
    deflated = np.array(merged[series_to_deflate.columns]) / deflation_index

    col_name = series_to_deflate.columns[0] + '_ia'
    return pd.DataFrame({col_name: deflated[0]}, index=merged.index)


def nominal_to_real(df_nominal_vars, inflacao_mom):
    """
    Converts a wide-format DataFrame of nominal variables to real values,
    handling different start dates per variable.

    Args:
        df_nominal_vars (pd.DataFrame): Nominal data (wide format, date index).
        inflacao_mom (pd.Series): Monthly inflation rates in decimal (e.g. 0.03 = 3%).

    Returns:
        pd.DataFrame: Real values with the same shape as the input.
    """
    df_real = pd.DataFrame(index=df_nominal_vars.index,
                           columns=df_nominal_vars.columns)

    for col in df_nominal_vars.columns:
        data_inicial = df_nominal_vars[col].dropna().index[0]
        data_inicial = datetime.strftime(data_inicial, '%Y-%m-%d')
        deflator = (marginal_to_index(inflacao_mom, data_inicial, data_inicial) / 100).squeeze()
        df_real[col] = df_nominal_vars[[col]].squeeze() / deflator

    return df_real
