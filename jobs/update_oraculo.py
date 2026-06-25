"""
Atualiza o Oraculo (termometro macro Brasil e US).

Uso:
    .venv\\Scripts\\python jobs\\update_oraculo.py
"""

from pathlib import Path

import pandas as pd

from analytics.oraculo.brasil.scores import run as run_brasil
#from analytics.oraculo.us.term_us import run as run_us

_ROOT    = Path(__file__).resolve().parents[1]
_ORACULO = _ROOT / "analytics" / "oraculo"
path_out = _ORACULO / "base" / "Central_base.csv"

db_brl = run_brasil()
#db_us  = run_us()

#central = pd.concat([db_brl, db_us])
db_brl.to_csv(path_out, index=False)

print("Oraculo atualizado com sucesso!")
