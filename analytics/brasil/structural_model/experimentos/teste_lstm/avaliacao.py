"""Walk-forward compartilhado: e o mesmo protocolo para benchmark e LSTM.

O ponto desta pasta e comparar. Se o LSTM roda num split e o AR noutro, o numero
final nao significa nada - entao o loop de folds, o corte de treino/teste e a
tabela de RMSE por horizonte vivem AQUI, e cada modelo entra como uma funcao
`ajustar(painel_treino) -> prever(painel_teste) -> matriz (n, 12)`.

Tres coisas que o protocolo garante e que sao faceis de perder:

1. O HIATO E DE TEMPO REAL (`dados.hiato_ibcbr_realtime`): cada mes ve so o HP
   rodado com dado da epoca. O filtro e bilateral, entao rodar uma vez sobre a
   amostra inteira injeta futuro em todo ponto historico - e o vazamento nao
   deixa rastro, so melhora o RMSE.
2. A PADRONIZACAO e ajustada no treino de CADA fold, nunca na amostra toda.
3. AVALIAR EXIGE ALVO COMPLETO, entao todo horizonte e medido nos mesmos meses.

Para medir o tamanho do vazamento que (1) evita, rode com
`montar_painel(hiato_vazado=True)` e compare - e um numero que vale conhecer.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Protocol

import numpy as np
import pandas as pd

from .dados import ALVOS, FEATURES, HORIZONTE, carregar_bruto, montar_painel

# Inicio do periodo de teste e cadencia de reestimacao.
TESTE_INICIO = pd.Timestamp("2015-01-01")
REFIT_MESES = 12  # reestima uma vez por ano, como no paper do HNN


class Modelo(Protocol):
    """Interface minima de um competidor."""

    nome: str

    def ajustar(self, X: pd.DataFrame, Y: pd.DataFrame) -> None: ...

    def prever(
        self, X: pd.DataFrame, contexto: pd.DataFrame | None = None
    ) -> np.ndarray:
        """Retorna matriz (len(X), HORIZONTE).

        `contexto` e o quadro de features INTEIRO (treino + teste), para que um
        modelo de janela possa olhar os meses anteriores a cada linha de teste.
        Os modelos planos ignoram. Sem isso, o primeiro mes de cada fold de
        teste nao teria os 23 meses de historico que a janela do LSTM exige - e
        preencher com zero seria inventar dado, nao previsao.
        """
        ...


@dataclass
class Fold:
    refit: pd.Timestamp
    fim_treino: pd.Timestamp
    meses_teste: pd.DatetimeIndex
    n_treino: int


@dataclass
class Resultado:
    nome: str
    previsto: pd.DataFrame  # index = mes do conjunto de informacao, cols y_h1..12
    observado: pd.DataFrame
    folds: list[Fold] = field(default_factory=list)
    diag: dict = field(default_factory=dict)  # diagnostico do ultimo fold

    @property
    def erro(self) -> pd.DataFrame:
        return self.previsto - self.observado

    def rmse_por_horizonte(self) -> pd.Series:
        e = self.erro
        return pd.Series(
            {c: float(np.sqrt(np.nanmean(e[c] ** 2))) for c in e.columns},
            name=self.nome,
        )

    def rmse_medio(self) -> float:
        return float(np.sqrt(np.nanmean(self.erro.to_numpy() ** 2)))

    def rmse_acumulado(self) -> float:
        """RMSE da inflacao ACUMULADA em 12 meses (a leitura que o usuario le)."""
        acc_p = (self.previsto / 100 + 1).prod(axis=1) - 1
        acc_o = (self.observado / 100 + 1).prod(axis=1) - 1
        return float(np.sqrt(np.nanmean(((acc_p - acc_o) * 100) ** 2)))


def montar_folds(painel: pd.DataFrame) -> list[Fold]:
    """Janela expansiva, reestimando a cada REFIT_MESES.

    Avaliar exige alvo COMPLETO (os 12 meses realizados), nao so features. Sem
    isso cada horizonte seria medido numa amostra diferente e o `medio` da
    tabela misturaria periodos - os ultimos 11 meses tem y_h1 mas nao y_h12.
    """
    treinavel = painel.dropna(subset=FEATURES + ALVOS).index
    avaliavel = painel.dropna(subset=FEATURES + ALVOS).index
    avaliavel = avaliavel[avaliavel >= TESTE_INICIO]
    if len(avaliavel) == 0:
        raise ValueError("nenhum mes de teste: confira TESTE_INICIO e o painel")

    folds: list[Fold] = []
    refits = pd.date_range(avaliavel.min(), avaliavel.max(), freq=f"{REFIT_MESES}MS")
    for i, r in enumerate(refits):
        # Treino: tudo com alvo completo ANTES do refit. Como o alvo do mes m
        # depende do IPCA de m+11, isso exclui automaticamente o que ainda nao
        # tinha realizado - sem precisar de corte manual.
        fim = r - pd.DateOffset(months=1)
        tr = treinavel[treinavel <= fim]
        prox = refits[i + 1] if i + 1 < len(refits) else avaliavel.max() + pd.DateOffset(months=1)
        meses = avaliavel[(avaliavel >= r) & (avaliavel < prox)]
        if len(tr) < 60 or len(meses) == 0:
            continue
        folds.append(Fold(refit=r, fim_treino=tr.max(), meses_teste=meses, n_treino=len(tr)))
    return folds


def rodar(
    fabricas: dict[str, Callable[[], Modelo]],
    verbose: bool = True,
    hiato_vazado: bool = False,
) -> dict[str, Resultado]:
    """Roda todos os modelos no MESMO conjunto de folds.

    `fabricas` mapeia nome -> callable que devolve um modelo virgem (uma
    instancia nova por fold, para nao carregar estado entre reestimacoes).
    """
    bruto = carregar_bruto()
    painel = montar_painel(bruto=bruto, hiato_vazado=hiato_vazado)
    folds = montar_folds(painel)
    if hiato_vazado and verbose:
        print("AVISO: hiato BILATERAL (com vazamento). Numero nao reportavel.")

    if verbose:
        n_teste = sum(len(f.meses_teste) for f in folds)
        print(f"{len(folds)} folds, teste de {folds[0].meses_teste.min():%Y-%m} "
              f"a {folds[-1].meses_teste.max():%Y-%m} ({n_teste} meses)")

    prev = {n: [] for n in fabricas}
    diags: dict[str, dict] = {}
    obs = []

    for fd in folds:
        tr = painel.loc[painel.index <= fd.fim_treino].dropna(subset=FEATURES + ALVOS)
        te = painel.loc[fd.meses_teste].dropna(subset=FEATURES)
        if len(te) == 0:
            continue

        obs.append(te[ALVOS])
        for nome, fabrica in fabricas.items():
            m = fabrica()
            m.ajustar(tr[FEATURES], tr[ALVOS])
            yhat = np.asarray(m.prever(te[FEATURES], painel[FEATURES]), dtype=float)
            if yhat.shape != (len(te), HORIZONTE):
                raise ValueError(
                    f"{nome}: previsao {yhat.shape}, esperado {(len(te), HORIZONTE)}"
                )
            prev[nome].append(pd.DataFrame(yhat, index=te.index, columns=ALVOS))
            if getattr(m, "diag", None):
                diags[nome] = m.diag

        if verbose:
            print(f"  fold {fd.refit:%Y-%m}: treino n={len(tr)} (ate {fd.fim_treino:%Y-%m})"
                  f", teste n={len(te)}")

    observado = pd.concat(obs)
    return {
        n: Resultado(
            nome=n,
            previsto=pd.concat(p),
            observado=observado,
            folds=folds,
            diag=diags.get(n, {}),
        )
        for n, p in prev.items()
    }


def tabela(res: dict[str, Resultado]) -> pd.DataFrame:
    """RMSE por horizonte + medio + acumulado 12m, uma coluna por modelo."""
    t = pd.DataFrame({n: r.rmse_por_horizonte() for n, r in res.items()})
    t.loc["medio"] = {n: r.rmse_medio() for n, r in res.items()}
    t.loc["acum12m"] = {n: r.rmse_acumulado() for n, r in res.items()}
    return t
