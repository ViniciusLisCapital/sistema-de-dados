"""Entry point do experimento.

    # so os benchmarks (nao precisa de torch)
    uv run python -m analytics.brasil.monetary_policy.teste_lstm.run --sem-lstm

    # completo
    uv run --with torch --with-editable . python -m analytics.brasil.monetary_policy.teste_lstm.run

Grava em `data/`: a tabela de RMSE, as previsoes de cada modelo e um JSON de
diagnostico. O veredito nao e o RMSE do LSTM - e a diferenca dele contra o
melhor benchmark.
"""

from __future__ import annotations

import argparse
import json
import warnings
from pathlib import Path

import pandas as pd

from . import avaliacao, benchmark
from .dados import DATA

warnings.filterwarnings("ignore")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sem-lstm", action="store_true", help="so os benchmarks")
    ap.add_argument(
        "--hiato-vazado",
        action="store_true",
        help="HP bilateral: mede quanto o vazamento embelezaria (nao reportar)",
    )
    args = ap.parse_args()

    fabricas = dict(benchmark.FABRICAS)
    if not args.sem_lstm:
        from .modelo import FABRICAS as LSTM_FABRICAS

        fabricas.update(LSTM_FABRICAS)

    res = avaliacao.rodar(fabricas, hiato_vazado=args.hiato_vazado)
    tab = avaliacao.tabela(res)

    DATA.mkdir(parents=True, exist_ok=True)
    sufixo = "_vazado" if args.hiato_vazado else ""
    tab.to_csv(DATA / f"rmse{sufixo}.csv", float_format="%.4f")
    for nome, r in res.items():
        r.previsto.to_csv(DATA / f"prev_{nome}{sufixo}.csv", float_format="%.4f")
    next(iter(res.values())).observado.to_csv(
        DATA / f"observado{sufixo}.csv", float_format="%.4f"
    )

    print()
    print(tab.round(3).to_string())

    # --- veredito ----------------------------------------------------------- #
    medios = tab.loc["medio"].sort_values()
    print()
    print("ordem por RMSE medio:")
    for nome, v in medios.items():
        print(f"  {nome:10s} {v:.4f}")

    if "lstm" in medios.index:
        bench = medios.drop("lstm")
        melhor_b, v_b = bench.index[0], float(bench.iloc[0])
        v_l = float(medios["lstm"])
        delta = (v_l / v_b - 1) * 100
        print()
        print(f"LSTM {v_l:.4f} contra {melhor_b} {v_b:.4f}: {delta:+.1f}%")
        print(
            "  VEREDITO: o LSTM bate o melhor benchmark."
            if delta < 0
            else "  VEREDITO: o LSTM NAO bate o melhor benchmark."
        )
        diag = res["lstm"].diag
        json.dump(
            {
                "rmse_medio": {k: float(v) for k, v in medios.items()},
                "melhor_benchmark": melhor_b,
                "delta_pct_lstm_vs_benchmark": delta,
                "diag_lstm": diag,
            },
            open(DATA / f"veredito{sufixo}.json", "w", encoding="utf-8"),
            indent=2,
            ensure_ascii=False,
        )

    print()
    print(f"artefatos em {DATA}")


if __name__ == "__main__":
    main()
