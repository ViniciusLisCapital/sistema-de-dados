"""Atividade, Q3: revisões do hiato do BC entre edições do RPM (pm_hiato_produto_vintages, central).
Para cada trimestre q: nowcast = central na edição do próprio trimestre (a 1a vez que q aparece);
placar = central na edição seguinte (a 1a depois do PIB de q); última = edição 2026-09.
Mede placar - nowcast e última - placar, e a revisão média por edição dos últimos 8 trimestres."""
import pandas as pd
from pathlib import Path
A = Path(__file__).resolve().parents[1] / "A"
v = pd.read_csv(A / "pm_hiato_produto_vintages.csv.gz", parse_dates=["vintage", "date"])
c = v[v.variavel == "central"].pivot_table(index="date", columns="vintage", values="value")
eds = sorted(c.columns)
print("edicoes:", [e.strftime("%Y-%m") for e in eds])
rows = []
for q in c.index:
    s = c.loc[q].dropna()
    ed_q = [e for e in eds if e.to_period("Q") == q.to_period("Q")]
    if not ed_q or ed_q[0] not in s.index:
        continue
    first_ed = ed_q[0]
    later = [e for e in eds if e > first_ed]
    plac = s.get(later[0]) if later else None
    rows.append(dict(tri=f"{q.quarter}T{str(q.year)[2:]}", edicao_nowcast=first_ed.strftime("%Y-%m"),
                     nowcast=s[first_ed], placar=plac, ultima=s.get(eds[-1])))
r = pd.DataFrame(rows)
r["placar_menos_nowcast"] = r.placar - r.nowcast
r["ultima_menos_placar"] = r.ultima - r.placar
print(r.round(2).to_string())
ok = r.dropna(subset=["placar"])
print("\nplacar - nowcast: n=%d media %.2f dp %.2f min %.2f max %.2f; positivas %d" % (
    len(ok), ok.placar_menos_nowcast.mean(), ok.placar_menos_nowcast.std(),
    ok.placar_menos_nowcast.min(), ok.placar_menos_nowcast.max(), (ok.placar_menos_nowcast > 0).sum()))
pos = ok[ok.edicao_nowcast >= "2024-09"]
print("so desde a quebra (nowcast em 2024-09 ou depois): n=%d media %.2f min %.2f max %.2f" % (
    len(pos), pos.placar_menos_nowcast.mean(), pos.placar_menos_nowcast.min(), pos.placar_menos_nowcast.max()))
ok2 = r.dropna(subset=["ultima_menos_placar"])
ok2 = ok2[ok2.edicao_nowcast < eds[-2].strftime("%Y-%m")]
print("ultima - placar: n=%d media %.2f min %.2f max %.2f" % (len(ok2), ok2.ultima_menos_placar.mean(), ok2.ultima_menos_placar.min(), ok2.ultima_menos_placar.max()))
# revisao da ultima edicao contra a anterior, por trimestre, ao longo das edicoes recentes
print("\nRevisao media da edicao contra a anterior (trimestres comuns dos ultimos 2 anos):")
for a, b in zip(eds[:-1], eds[1:]):
    comum = c[[a, b]].dropna()
    comum = comum[comum.index >= a - pd.DateOffset(years=2)]
    print(f"  {b.strftime('%Y-%m')} vs {a.strftime('%Y-%m')}: {(comum[b]-comum[a]).mean():+.2f} (n={len(comum)})")

# a revisao placar - nowcast anda com o PIB do trimestre? (qoq dessaz. do IBGE, taxa do trimestre q)
tx = pd.read_csv(A / "atv_pib_taxas.csv.gz", parse_dates=["date"])
qoq = tx[(tx.name == "pib_pm") & (tx.indicador == "qoq")].set_index("date")["value"]
r["q"] = [pd.Timestamp(f"20{t[2:]}-{(int(t[0])-1)*3+1:02d}-01") for t in r.tri]
r["pib_qoq"] = r.q.map(qoq)
ok = r.dropna(subset=["placar", "pib_qoq"])
print("\ncorrelacao (placar - nowcast) x PIB qoq do trimestre: %.2f (n=%d)" % (ok.placar_menos_nowcast.corr(ok.pib_qoq), len(ok)))
import numpy as np
b = np.polyfit(ok.pib_qoq, ok.placar_menos_nowcast, 1)
print("reta: revisao = %.2f + %.2f * PIB qoq" % (b[1], b[0]))
print(ok[["tri", "pib_qoq", "placar_menos_nowcast"]].round(2).to_string())
