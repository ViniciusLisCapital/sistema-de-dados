"""G r1b: referência para as probabilidades da tese. Distribuição lognormal com mediana na base do modelo
com o tempero (i) (CDS x1,5) e desvio = vol. realizada 63d do BRL (12,2% a.a., "O real e os pares", 14/10)
x raiz do tempo até o fim de cada trimestre (dias úteis/252, a partir de 14/10). Devolve P(abaixo, dentro,
acima) da faixa base escolhida. É referência; as probabilidades finais levam os ajustes da seção 3.2."""
import numpy as np
import pandas as pd
from math import erf, log, sqrt

VOL = 0.122
HOJE = pd.Timestamp("2026-10-14")
FIM = {"4T26": "2026-12-31", "1T27": "2027-03-31", "2T27": "2027-06-30", "3T27": "2027-09-30", "4T27": "2027-12-31", "1T28": "2028-03-31"}
CENTRAL = {"4T26": 5.156, "1T27": 5.194, "2T27": 5.197, "3T27": 5.183, "4T27": 5.199, "1T28": 5.223}
MEDIANA = {"4T26": 5.115, "1T27": 5.153, "2T27": 5.156, "3T27": 5.142, "4T27": 5.158, "1T28": 5.182}
FAIXA = {"4T26": (5.00, 5.30), "1T27": (4.95, 5.40), "2T27": (4.90, 5.45), "3T27": (4.90, 5.50), "4T27": (4.90, 5.55), "1T28": (4.90, 5.60)}
N = lambda z: 0.5 * (1 + erf(z / sqrt(2)))
for q, fim in FIM.items():
    t = np.busday_count(HOJE.date(), pd.Timestamp(fim).date()) / 252
    s = VOL * sqrt(t)
    lo, hi = FAIXA[q]; m = MEDIANA[q]
    pb, pw = N(log(lo / m) / s), 1 - N(log(hi / m) / s)
    print(f"{q}: t={t:.2f} a · desvio {100*s:.1f}% · faixa {lo:.2f}-{hi:.2f} ({100*(lo/CENTRAL[q]-1):+.1f}% / {100*(hi/CENTRAL[q]-1):+.1f}% da central)"
          f" · P best {100*pb:.0f}% · base {100*(1-pb-pw):.0f}% · worst {100*pw:.0f}%")
