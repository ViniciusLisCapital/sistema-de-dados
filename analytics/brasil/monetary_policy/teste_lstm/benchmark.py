"""Benchmarks. O LSTM tem de bater ESTES, nao um numero absoluto.

Cinco competidores, do mais bobo ao mais serio:

- `media12`  : os 12 meses a frente = media dos 12 ultimos. Piso absoluto.
- `sazonal`  : media historica de CADA mes-calendario. Inflacao brasileira tem
               sazonalidade forte e previsivel (ensino em fevereiro), entao um
               modelo que perde disto esta perdendo de graca.
- `focus`    : a expectativa da Focus de 12 meses, convertida para taxa mensal.
               Gratuita, publicada toda semana - e o custo de oportunidade real.
- `focus_saz`: o NIVEL da Focus com a FORMA sazonal do historico. Costuma ser o
               mais difícil de bater, e e a combinacao honesta das duas ideias.
- `ridge`    : as 10 features, uma regressao por horizonte, alpha por CV
               temporal. E o teto do que se consegue sem nao-linearidade - se o
               LSTM nao bater este, a nao-linearidade nao esta pagando.

Todos sao "diretos": uma previsao por horizonte, nada iterado.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.linear_model import RidgeCV
from sklearn.preprocessing import StandardScaler

from .dados import HORIZONTE


def _meses_alvo(idx: pd.DatetimeIndex) -> np.ndarray:
    """Mes-calendario (1-12) do alvo, matriz (len(idx), HORIZONTE).

    O alvo `y_h` do mes de informacao `t` e o IPCA de `t + (h-1)`.
    """
    base = idx.month.to_numpy()[:, None] - 1
    return (base + np.arange(HORIZONTE)[None, :]) % 12 + 1


class Media12:
    nome = "media12"

    def ajustar(self, X: pd.DataFrame, Y: pd.DataFrame) -> None:
        pass

    def prever(self, X: pd.DataFrame, contexto: pd.DataFrame | None = None) -> np.ndarray:
        # ipca_12m e a acumulada em 12m; a mensal equivalente e a raiz 12a.
        m = ((X["ipca_12m"].to_numpy() / 100 + 1) ** (1 / 12) - 1) * 100
        return np.repeat(m[:, None], HORIZONTE, axis=1)


class Sazonal:
    """Media historica por mes-calendario, estimada so no treino."""

    nome = "sazonal"

    def __init__(self, anos: int = 10):
        self.anos = anos
        self.perfil: dict[int, float] = {}
        self.geral = 0.0

    def ajustar(self, X: pd.DataFrame, Y: pd.DataFrame) -> None:
        # Reconstroi a serie de IPCA por mes de referencia a partir de y_h1
        # (que e o IPCA do proprio mes da linha).
        s = Y["y_h1"].dropna()
        s = s[s.index >= s.index.max() - pd.DateOffset(years=self.anos)]
        self.geral = float(s.mean())
        self.perfil = s.groupby(s.index.month).mean().to_dict()

    def prever(self, X: pd.DataFrame, contexto: pd.DataFrame | None = None) -> np.ndarray:
        mm = _meses_alvo(X.index)
        return np.vectorize(lambda m: self.perfil.get(int(m), self.geral))(mm)


class Focus:
    """Expectativa Focus de 12m, achatada em taxa mensal constante."""

    nome = "focus"

    def ajustar(self, X: pd.DataFrame, Y: pd.DataFrame) -> None:
        pass

    def prever(self, X: pd.DataFrame, contexto: pd.DataFrame | None = None) -> np.ndarray:
        m = ((X["focus_12m"].to_numpy() / 100 + 1) ** (1 / 12) - 1) * 100
        return np.repeat(m[:, None], HORIZONTE, axis=1)


class FocusSazonal:
    """Nivel da Focus, forma sazonal do historico.

    A soma dos 12 meses previstos reproduz a acumulada da Focus - o perfil
    sazonal so redistribui, nunca muda o total. E o que separa esta do `sazonal`
    puro: a forma vem do historico, o nivel vem da pesquisa de hoje.
    """

    nome = "focus_saz"

    def __init__(self, anos: int = 10):
        self.saz = Sazonal(anos=anos)

    def ajustar(self, X: pd.DataFrame, Y: pd.DataFrame) -> None:
        self.saz.ajustar(X, Y)

    def prever(self, X: pd.DataFrame, contexto: pd.DataFrame | None = None) -> np.ndarray:
        forma = self.saz.prever(X)  # (n, 12) em % mensal
        # Desvio multiplicativo de cada mes contra a media do proprio perfil.
        media_perfil = forma.mean(axis=1, keepdims=True)
        nivel = ((X["focus_12m"].to_numpy() / 100 + 1) ** (1 / 12) - 1) * 100
        return forma - media_perfil + nivel[:, None]


class Ridge:
    """Uma RidgeCV por horizonte, com padronizacao ajustada no treino."""

    nome = "ridge"

    def __init__(self, alphas: tuple[float, ...] = (0.1, 1.0, 10.0, 100.0, 1000.0)):
        self.alphas = alphas
        self.scaler: StandardScaler | None = None
        self.modelos: list[RidgeCV] = []

    def ajustar(self, X: pd.DataFrame, Y: pd.DataFrame) -> None:
        self.scaler = StandardScaler().fit(X.to_numpy())
        Xs = self.scaler.transform(X.to_numpy())
        self.modelos = []
        for h in range(1, HORIZONTE + 1):
            y = Y[f"y_h{h}"].to_numpy()
            m = RidgeCV(alphas=self.alphas).fit(Xs, y)
            self.modelos.append(m)

    def prever(self, X: pd.DataFrame, contexto: pd.DataFrame | None = None) -> np.ndarray:
        assert self.scaler is not None, "chame ajustar() antes"
        Xs = self.scaler.transform(X.to_numpy())
        return np.column_stack([m.predict(Xs) for m in self.modelos])


FABRICAS = {
    "media12": Media12,
    "sazonal": Sazonal,
    "focus": Focus,
    "focus_saz": FocusSazonal,
    "ridge": Ridge,
}
