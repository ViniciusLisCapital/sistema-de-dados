"""fi: o preço do risco no histórico — distribuição das variações do CDS (fechamento do trimestre) e da
rr_10a (média do trimestre) em 1 a 6 trimestres (janela de 10 anos); percentil da NTN-B 10a hoje;
o que aconteceu depois de saltos diários grandes do CDS e da NTN-B 10a; inflação implícita 10a diária;
e a média de 4T26 da rr_10a sob níveis constantes para os pregões que faltam."""
from pathlib import Path
import numpy as np
import pandas as pd
A = Path(__file__).resolve().parent.parent / "A"
r = lambda f: pd.read_csv(A / f"{f}.csv.gz", parse_dates=["date"])
br = r("br_interest_rate")
nb = br[(br.curve == "NTNBJS") & (br.tenor == "120M")].set_index("date").value.sort_index()
di = br[(br.curve == "DIPRE") & (br.tenor == "120M")].set_index("date").value.sort_index()
c = r("cmb_risco_pais"); cds = c[c.name == "cds_5y_usd"].set_index("date").value.sort_index()
print("CDS desde", cds.index.min().date(), "· NTN-B 10a desde", nb.index.min().date())

cq = cds.resample("QE").last()
rq = nb.resample("QE").mean()
cq, rq = cq[cq.index <= "2026-09-30"], rq[rq.index <= "2026-09-30"]
def dist(s, win_start, nome, unidade):
    s = s[s.index >= win_start]
    print(f"\n{nome}: variação em h trimestres, janela desde {win_start} ({unidade}); percentis 5/10/25/50/75/90/95")
    for h in range(1, 7):
        d = (s - s.shift(h)).dropna()
        print(f"  h={h}: n={len(d)}", np.round(np.percentile(d, [5, 10, 25, 50, 75, 90, 95]), 2))
dist(cq, "2016-09-30", "CDS 5a, fechamento", "p.b.")
dist(rq, "2016-09-30", "NTN-B 10a, média do trimestre", "p.p.")
print("\nCDS fechamento trimestral desde 2023:", cq[cq.index >= "2023-01-01"].round(0).to_dict())
print("rr_10a média trimestral desde 2023:", rq[rq.index >= "2023-01-01"].round(2).to_dict())

# percentis da NTN-B 10a de 26/10
last = nb.iloc[-1]
for w, st in [("10a", "2016-10-26"), ("hist", "2000-01-01")]:
    x = nb[nb.index >= st]
    print(f"NTN-B 10a {nb.index[-1].date()} = {last:.2f}: percentil {w} = {100*(x < last).mean():.0f} (n={len(x)}, mín {x.min():.2f}, máx {x.max():.2f})")
print("Máximos da NTN-B 10a desde 2016 por ano:", nb[nb.index >= "2016-01-01"].groupby(nb[nb.index >= "2016-01-01"].index.year).max().round(2).to_dict())

# depois de saltos diários grandes (dia útil contra o anterior)
for nome, s, lim, un in [("CDS", cds, 15, "p.b."), ("NTN-B 10a", nb * 100, 40, "p.b.")]:
    d = s.diff()
    ev = d[d >= lim]
    ev = ev[ev.index < "2026-10-01"]
    # um evento por mês, para não contar o mesmo episódio várias vezes
    ev = ev.groupby(ev.index.to_period("M")).head(1)
    rows = []
    for t, v in ev.items():
        i = s.index.get_loc(t)
        def ahead(k):
            return s.iloc[i + k] - s.iloc[i] if i + k < len(s) else np.nan
        rows.append((t.date(), round(v, 1), round(s.iloc[i], 1), round(ahead(21), 1), round(ahead(63), 1), round(ahead(126), 1)))
    df = pd.DataFrame(rows, columns=["dia", "salto", "nível", "+21 pregões", "+63", "+126"])
    print(f"\nSaltos diários de {nome} ≥ {lim} {un} (um por mês), e a variação ADICIONAL depois (desde 2006):")
    df = df[pd.to_datetime(df.dia) >= "2006-01-01"]
    print(df.to_string(index=False))
    for k in ["+21 pregões", "+63", "+126"]:
        x = df[k].dropna()
        print(f"  {k}: n={len(x)}, mediana {x.median():.1f}, fração que reverteu (Δ<0) {100*(x<0).mean():.0f}%, fração que reverteu mais da metade do salto {100*((-x) > df.loc[x.index,'salto']/2).mean():.0f}%")

# inflação implícita 10a diária, set-out/2026
ii = (100 * ((1 + di / 100) / (1 + nb / 100) - 1)).dropna()
print("\nInflação implícita 10a (DI 10a vs NTN-B 10a), %:", ii[ii.index >= "2026-09-25"].round(2).to_dict())

# 4T26: média da rr_10a com os pregões que faltam a nível constante
q4 = nb[(nb.index >= "2026-10-01")]
dias = pd.bdate_range("2026-10-27", "2026-12-31")
fer = pd.to_datetime(["2026-11-02", "2026-11-20", "2026-12-24", "2026-12-25", "2026-12-31"])
dias = dias[~dias.isin(fer)]
print(f"\n4T26: {len(q4)} pregões observados, média {q4.mean():.3f}; faltam ~{len(dias)} pregões (dias úteis menos feriados presumidos)")
for L in [7.0, 7.5, 7.8, 8.05, 8.3, 8.6, 9.0]:
    print(f"  resto a {L:.2f}: média 4T26 = {(q4.sum() + L*len(dias))/(len(q4)+len(dias)):.2f}")
