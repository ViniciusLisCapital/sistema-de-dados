import numpy as np
import pandas as pd
from statsmodels.tsa.seasonal import STL


# ── Helpers ───────────────────────────────────────────────────────────────────

def GetMeanList(InputList):
    return round(sum(InputList) / len(InputList), 2)


def GetStdvList(InputList):
    return round(np.std(InputList), 2)


def SameMonthComparison(Vt, Index):
    """
    Produces two series (mean, std) where each value is compared against the
    same calendar month across all prior years.

    Args:
        Vt (pd.Series): Values.
        Index: Date index aligned with Vt.

    Returns:
        tuple: (MeanList, StdvList) — cumulative month-specific statistics.
    """
    months = {m: [] for m in range(1, 13)}
    MeanList = []
    StdvList = []

    for i in range(len(Vt)):
        month = Index[i].month
        months[month].append(Vt.iloc[i])
        MeanList.append(GetMeanList(months[month]))
        StdvList.append(0 if len(months[month]) < 2 else GetStdvList(months[month]))

    return MeanList, StdvList


# ── Sigmoid ───────────────────────────────────────────────────────────────────

def sigmoid(alfa, x):
    """alfa: steepness; x: input value. Returns value in (0, 1)."""
    return 1 / (1 + np.exp(alfa * x))


# ── Scoring functions ─────────────────────────────────────────────────────────

def Score(Yt, alfa, OutName, MovingAverage=False, Inputs=1):
    """
    Scores a time series on a 1–10 scale by normalising against its cumulative
    mean and std, then passing through a sigmoid.

    Args:
        Yt (pd.Series): Input series.
        alfa (float): Sigmoid steepness.
        OutName (str): Output column name.
        MovingAverage (bool): Apply rolling mean before scoring.
        Inputs (int): Rolling window size.

    Returns:
        pd.DataFrame: Single-column DataFrame with scores.
    """
    Vt = round(Yt.rolling(window=Inputs, min_periods=1).mean(), 2) if MovingAverage else Yt

    df = pd.DataFrame()
    df['Mean'] = Vt.rolling(window=Vt.shape[0], min_periods=1).mean()
    df['Std']  = Vt.rolling(window=Vt.shape[0], min_periods=1).std()
    df['Ht']   = (Vt - df['Mean']) / df['Std']
    df[OutName] = 5 + (sigmoid(-alfa, df['Ht']) - 0.5) * 10

    return pd.DataFrame(df[OutName], index=df.index)


def Score_SMC(Yt, alfa, OutName):
    """
    Scores by comparing each observation against the same calendar month in
    all prior years.

    Args:
        Yt (pd.Series): Input series (date-indexed).
        alfa (float): Sigmoid steepness.
        OutName (str): Output column name.

    Returns:
        pd.DataFrame: Single-column DataFrame with scores.
    """
    df = pd.DataFrame(index=Yt.index)
    df['Mean'], df['Std'] = SameMonthComparison(Yt, Yt.index)
    df['Ht'] = (Yt - df['Mean']) / df['Std']
    df[OutName] = 5 + (sigmoid(-alfa, df['Ht']) - 0.5) * 10

    return pd.DataFrame(df[OutName], index=df.index)


def Score_Diff(Yt, diff, alfa, OutName, MovingAverage=False, Inputs=0):
    """
    Scores the lagged differences of a series.

    Args:
        Yt (pd.Series): Input series.
        diff (int): Lag for differencing.
        alfa (float): Sigmoid steepness.
        OutName (str): Output column name.
        MovingAverage (bool): Smooth the differences before scoring.
        Inputs (int): Rolling window size.

    Returns:
        pd.DataFrame: Single-column DataFrame with scores.
    """
    Vt = Yt - Yt.shift(diff)
    if MovingAverage:
        Vt = round(Vt.rolling(window=Inputs, min_periods=1).mean(), 2)

    df = pd.DataFrame()
    df['Mean'] = Vt.rolling(window=Vt.shape[0], min_periods=1).mean()
    df['Std']  = Vt.rolling(window=Vt.shape[0], min_periods=1).std()
    df['Ht']   = (Vt - df['Mean']) / df['Std']
    df[OutName] = 5 + (sigmoid(-alfa, df['Ht']) - 0.5) * 10

    return pd.DataFrame(df[OutName], index=df.index)


def Score_Var(Yt, Var, alfa, OutName, MovingAverage=False, Inputs=0):
    """
    Scores the percentage changes of a series.

    Args:
        Yt (pd.Series): Input series.
        Var (int): Lag for % change calculation (e.g. 12 = YoY).
        alfa (float): Sigmoid steepness.
        OutName (str): Output column name.
        MovingAverage (bool): Smooth % changes before scoring.
        Inputs (int): Rolling window size.

    Returns:
        pd.DataFrame: Single-column DataFrame with scores.
    """
    Vt = ((Yt / Yt.shift(Var)) - 1) * 100
    if MovingAverage:
        Vt = round(Vt.rolling(window=Inputs, min_periods=1).mean(), 2)

    df = pd.DataFrame()
    df['Mean'] = Vt.rolling(window=Yt.shape[0], min_periods=1).mean()
    df['Std']  = Vt.rolling(window=Yt.shape[0], min_periods=1).std()
    df['Ht']   = (Vt - df['Mean']) / df['Std']
    df[OutName] = 5 + (sigmoid(-alfa, df['Ht']) - 0.5) * 10

    return pd.DataFrame(df[OutName], index=df.index)


def Score_SA(Yt, alfa, OutName):
    """
    Scores a series after removing its seasonal component via STL decomposition.

    Args:
        Yt (pd.Series): Input series.
        alfa (float): Sigmoid steepness.
        OutName (str): Output column name.

    Returns:
        pd.DataFrame: Single-column DataFrame with scores.
    """
    model = STL(Yt, period=12).fit()
    Vt = model.trend + model.resid

    df = pd.DataFrame()
    df['Mean'] = Vt.rolling(window=Yt.shape[0], min_periods=1).mean()
    df['Std']  = Vt.rolling(window=Yt.shape[0], min_periods=1).std()
    df['Ht']   = (Vt - df['Mean']) / df['Std']
    df[OutName] = 5 + (sigmoid(-alfa, df['Ht']) - 0.5) * 10

    return pd.DataFrame(df[OutName], index=df.index)


# ── OOP interface ─────────────────────────────────────────────────────────────

class ScoringFunction:
    """Object-oriented wrapper for the scoring functions above."""

    def __init__(self, alfa, OutName, MovingAverage=False, Inputs=1):
        self.alfa = alfa
        self.OutName = OutName
        self.MovingAverage = MovingAverage
        self.Inputs = Inputs
        self.df = pd.DataFrame()

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-self.alfa * x))

    def calculate_score(self, Yt):
        Vt = (round(Yt.rolling(window=self.Inputs, min_periods=1).mean(), 2)
              if self.MovingAverage else Yt)

        self.df['Mean'] = Vt.rolling(window=Vt.shape[0], min_periods=1).mean()
        self.df['Std']  = Vt.rolling(window=Vt.shape[0], min_periods=1).std()
        self.df['Ht']   = (Vt - self.df['Mean']) / self.df['Std']
        self.df[self.OutName] = 5 + (self.sigmoid(self.df['Ht']) - 0.5) * 10
        self.OutFrame = pd.DataFrame(self.df[self.OutName], index=self.df.index)
        return self.OutFrame

    def get_statistics(self):
        return self.df[['Mean', 'Std']]

    def calculate_score_sa(self, Yt):
        model = STL(Yt).fit()
        Vt = model.trend + model.resid

        self.df['Mean'] = Vt.rolling(window=Yt.shape[0], min_periods=1).mean()
        self.df['Std']  = Vt.rolling(window=Yt.shape[0], min_periods=1).std()
        self.df['Ht']   = (Vt - self.df['Mean']) / self.df['Std']
        self.df[self.OutName] = 5 + (self.sigmoid(self.df['Ht']) - 0.5) * 10
        self.OutFrame = pd.DataFrame(self.df[self.OutName], index=self.df.index)

    def calculate_score_smc(self, Yt):
        df = pd.DataFrame(index=Yt.index)
        df['Mean'], df['Std'] = self._same_month_comparison(Yt, Yt.index)
        df['Ht'] = (Yt - df['Mean']) / df['Std']
        df[self.OutName] = 5 + (self.sigmoid(df['Ht']) - 0.5) * 10
        self.OutFrame = pd.DataFrame(df[self.OutName], index=df.index)

    def _same_month_comparison(self, Vt, Index):
        months_data = {m: [] for m in range(1, 13)}
        mean_list, stdv_list = [], []

        for date, val in zip(Index, Vt):
            bucket = months_data[date.month]
            bucket.append(val)
            mean_list.append(sum(bucket) / len(bucket))
            if len(bucket) < 2:
                stdv_list.append(0)
            else:
                mean = sum(bucket) / len(bucket)
                stdv_list.append((sum((x - mean) ** 2 for x in bucket) / len(bucket)) ** 0.5)

        return mean_list, stdv_list
