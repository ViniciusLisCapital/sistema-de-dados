"""G do externo, ciclo 2026-10-02: o caminho do Fed que os T-bills precificam em 02/10.

Bill − efetivo pós-17/09 − prêmio histórico (ex_relacoes.py, item 1, desde 2010) = alta média
precificada no prazo. Com um caminho linear a partir de hoje, a alta no FIM do prazo é o dobro
da média. Em número de altas de 25 p.b. Lê só ../A/.
"""
from pathlib import Path
import pandas as pd

A = Path(__file__).resolve().parent.parent / "A"
c = pd.read_csv(A / "us_interest_rate__curva_completa.csv.gz")
c = c[(c.curve == "US_TREASURY") & (c.date == "2026-10-02")].set_index("tenor")["value"]
EFETIVO = 3.89          # ex_relacoes.py, item 2: ponto médio 3,875 + desvio de 2026 (3,885 a 3,907)
PREMIO = {"1M": 0.01, "3M": 0.02, "6M": 0.04, "1Y": -0.13}   # ex_relacoes.py, item 1, desde 2010
PRAZO = {"1M": "início de nov", "3M": "início de jan/27", "6M": "início de abr/27", "1Y": "início de out/27"}
for t in ["1M", "3M", "6M", "1Y"]:
    media = c[t] - EFETIVO - PREMIO[t]
    fim = 2 * media
    print(f"{t}: bill {c[t]:.2f} · média precificada {media:+.2f} p.p. · no fim do prazo ({PRAZO[t]}) "
          f"{fim:+.2f} p.p. ≈ {fim/0.25:.1f} altas de 25 p.b. · sem o prêmio: {2*(c[t]-EFETIVO):+.2f}")
