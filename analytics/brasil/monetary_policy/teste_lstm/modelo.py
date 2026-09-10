"""LSTM de previsao direta: janela de L meses -> 12 saidas.

Nao importa `torch` no topo de proposito. O resto da pasta (painel, benchmarks,
avaliacao) roda no venv do projeto sem dependencia de deep learning; so este
modulo precisa dela, e ela e efemera enquanto o experimento nao provar nada:

    uv run --with torch --with-editable . python -m analytics.brasil.monetary_policy.teste_lstm.run

ESCALA DO PROBLEMA, medida e nao estimada: ~180 janelas de treino no primeiro
fold contra ~6.000 parametros. E o mesmo regime do paper do HNN (257 obs, 2M
parametros), e o que segura o overfit sao as mesmas quatro amarras dele:
arquitetura pequena, early stopping em hold-out, dropout e ensemble de seeds.

TRES ARMADILHAS ESPECIFICAS DE JANELA DESLIZANTE, todas silenciosas:

1. JANELAS VIZINHAS COMPARTILHAM L-1 MESES. Entao um hold-out cortado no meio
   das janelas tem quase os mesmos dados que o treino, e o early stopping para
   tarde. Aqui o corte e temporal E purgado: joga fora as janelas que cruzam a
   fronteira (`_purga = L + HORIZONTE`).
2. O ALVO TAMBEM VAZA PELA FRONTEIRA. A janela que termina em `m` preve ate
   `m+11`, entao ela ja "sabe" o que o hold-out mede. A purga cobre os dois.
3. A PADRONIZACAO DE Y muda o peso relativo dos horizontes na perda. Um unico
   par (media, desvio) para os 12 - nao um por horizonte - senao o modelo passa
   a minimizar erro relativo e o RMSE reportado deixa de ser o comparavel.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from .dados import HORIZONTE

JANELA = 24  # meses de historico por amostra
SEEDS = (0, 1, 2, 3, 4)  # ensemble: integra o ruido de inicializacao


def _janelas(
    feats: pd.DataFrame,
    fins: pd.DatetimeIndex,
    L: int,
) -> tuple[np.ndarray, list[pd.Timestamp]]:
    """Empilha (n, L, n_feat) para cada mes em `fins` que tenha L meses cheios.

    `feats` e o quadro INTEIRO (treino + teste): e o que permite o primeiro mes
    de um fold de teste ter os 23 meses anteriores. Uma janela com qualquer NaN
    e descartada - preencher com zero seria inventar dado.
    """
    arr = feats.to_numpy(dtype=float)
    pos = {d: i for i, d in enumerate(feats.index)}
    saida, datas = [], []
    for d in fins:
        i = pos.get(d)
        if i is None or i + 1 < L:
            continue
        w = arr[i + 1 - L : i + 1]
        if np.isnan(w).any():
            continue
        saida.append(w)
        datas.append(d)
    if not saida:
        return np.empty((0, L, arr.shape[1])), []
    return np.stack(saida), datas


class LSTM:
    """Uma LSTM por fold, com ensemble de seeds e early stopping purgado."""

    nome = "lstm"

    def __init__(
        self,
        janela: int = JANELA,
        oculto: int = 32,
        camadas: int = 1,
        dropout: float = 0.2,
        lr: float = 1e-3,
        epocas: int = 400,
        paciencia: int = 40,
        val_frac: float = 0.2,
        seeds: tuple[int, ...] = SEEDS,
    ):
        self.janela = janela
        self.oculto = oculto
        self.camadas = camadas
        self.dropout = dropout
        self.lr = lr
        self.epocas = epocas
        self.paciencia = paciencia
        self.val_frac = val_frac
        self.seeds = seeds
        self._purga = janela + HORIZONTE
        self.redes: list = []
        self.mu_x = self.sd_x = self.mu_y = self.sd_y = None
        self.treino_feats: pd.DataFrame | None = None
        self.diag: dict = {}

    # -- construcao da rede ------------------------------------------------- #
    def _rede(self, n_feat: int, seed: int):
        import torch
        from torch import nn

        torch.manual_seed(seed)

        class Rede(nn.Module):
            def __init__(s, n_feat, oculto, camadas, dropout):
                super().__init__()
                s.lstm = nn.LSTM(
                    input_size=n_feat,
                    hidden_size=oculto,
                    num_layers=camadas,
                    batch_first=True,
                    dropout=dropout if camadas > 1 else 0.0,
                )
                s.drop = nn.Dropout(dropout)
                s.head = nn.Linear(oculto, HORIZONTE)

            def forward(s, x):
                out, _ = s.lstm(x)
                return s.head(s.drop(out[:, -1, :]))  # so o ultimo passo

        return Rede(n_feat, self.oculto, self.camadas, self.dropout)

    # -- interface do protocolo --------------------------------------------- #
    def ajustar(self, X: pd.DataFrame, Y: pd.DataFrame) -> None:
        import torch

        self.treino_feats = X
        W, datas = _janelas(X, X.index, self.janela)
        if len(W) < 40:
            raise ValueError(f"janelas insuficientes para treinar: {len(W)}")
        Yv = Y.loc[datas].to_numpy(dtype=float)

        # Corte temporal purgado. `_purga` cobre as duas vias de vazamento:
        # sobreposicao de janela (L) e sobreposicao de alvo (HORIZONTE).
        n = len(W)
        n_val = max(12, int(round(n * self.val_frac)))
        fim_tr = n - n_val - self._purga
        if fim_tr < 30:  # amostra curta: abre mao da validacao, epocas fixas
            idx_tr, idx_val = np.arange(n), np.empty(0, dtype=int)
        else:
            idx_tr = np.arange(fim_tr)
            idx_val = np.arange(n - n_val, n)

        # Padronizacao: media/desvio SO do treino do fold.
        self.mu_x = W[idx_tr].reshape(-1, W.shape[2]).mean(axis=0)
        self.sd_x = W[idx_tr].reshape(-1, W.shape[2]).std(axis=0) + 1e-8
        self.mu_y = float(Yv[idx_tr].mean())  # um par para os 12 horizontes
        self.sd_y = float(Yv[idx_tr].std()) + 1e-8

        Wt = torch.tensor((W - self.mu_x) / self.sd_x, dtype=torch.float32)
        Yt = torch.tensor((Yv - self.mu_y) / self.sd_y, dtype=torch.float32)

        self.redes = []
        epocas_usadas = []
        for seed in self.seeds:
            rede = self._rede(W.shape[2], seed)
            opt = torch.optim.Adam(rede.parameters(), lr=self.lr)
            perda = torch.nn.MSELoss()
            melhor, melhor_ep, espera = np.inf, 0, 0
            melhor_estado = {k: v.clone() for k, v in rede.state_dict().items()}

            for ep in range(1, self.epocas + 1):
                rede.train()
                opt.zero_grad()
                perda(rede(Wt[idx_tr]), Yt[idx_tr]).backward()
                opt.step()

                if len(idx_val) == 0:
                    continue
                rede.eval()
                with torch.no_grad():
                    v = float(perda(rede(Wt[idx_val]), Yt[idx_val]))
                if v < melhor - 1e-6:
                    melhor, melhor_ep, espera = v, ep, 0
                    melhor_estado = {k: t.clone() for k, t in rede.state_dict().items()}
                else:
                    espera += 1
                    if espera >= self.paciencia:
                        break

            if len(idx_val):
                rede.load_state_dict(melhor_estado)
                epocas_usadas.append(melhor_ep)
            rede.eval()
            self.redes.append(rede)

        n_par = sum(p.numel() for p in self.redes[0].parameters())
        self.diag = {
            "janelas": n,
            "n_treino": len(idx_tr),
            "n_val": len(idx_val),
            "purga": self._purga,
            "parametros": n_par,
            "par_por_janela": round(n_par / max(len(idx_tr), 1), 1),
            "epoca_media": round(float(np.mean(epocas_usadas)), 1) if epocas_usadas else None,
        }

    def prever(
        self, X: pd.DataFrame, contexto: pd.DataFrame | None = None
    ) -> np.ndarray:
        import torch

        if contexto is None:
            raise ValueError("LSTM exige `contexto` para montar a janela")
        W, datas = _janelas(contexto, X.index, self.janela)
        out = np.full((len(X), HORIZONTE), np.nan)
        if len(W) == 0:
            return out

        Wt = torch.tensor((W - self.mu_x) / self.sd_x, dtype=torch.float32)
        with torch.no_grad():
            preds = np.mean([r(Wt).numpy() for r in self.redes], axis=0)
        preds = preds * self.sd_y + self.mu_y

        pos = {d: i for i, d in enumerate(X.index)}
        for k, d in enumerate(datas):
            out[pos[d]] = preds[k]
        # Mes sem janela cheia cai para a ultima leitura de 12m disponivel, em
        # vez de virar NaN e desaparecer do RMSE - desaparecer premiaria o
        # modelo justo onde ele nao tem o que dizer.
        falta = np.isnan(out[:, 0])
        if falta.any():
            fb = ((X["ipca_12m"].to_numpy() / 100 + 1) ** (1 / 12) - 1) * 100
            out[falta] = np.repeat(fb[falta][:, None], HORIZONTE, axis=1)
        return out


FABRICAS = {"lstm": LSTM}
