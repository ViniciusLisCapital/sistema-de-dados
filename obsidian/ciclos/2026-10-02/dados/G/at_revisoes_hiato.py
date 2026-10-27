"""at_ · revisões da central do hiato do BC entre edições do RPM (pm_hiato_produto_vintages).
Nowcast = edição do fechamento do próprio trimestre; placar = edição do trimestre seguinte (1º RPM
depois do PIB); última = edição de 2026-09. Só a central (quebra metodológica 2024-06/2024-09)."""
import pandas as pd
v = pd.read_csv("../A/pm_hiato_produto_vintages.csv.gz", parse_dates=["vintage", "date"])
v = v[v.variavel == "central"].pivot_table(index="date", columns="vintage", values="value")
ed = sorted(v.columns)
rows = []
for q in v.index:
    # edição do fechamento do trimestre q: vintage no mesmo trimestre
    now = [e for e in ed if e.to_period("Q") == q.to_period("Q")]
    pla = [e for e in ed if e.to_period("Q") == (q.to_period("Q") + 1)]
    if not now:
        continue
    r = {"tri": q.to_period("Q"), "nowcast": v.loc[q, now[0]],
         "placar": v.loc[q, pla[0]] if pla else None, "ultima": v.loc[q, ed[-1]]}
    rows.append(r)
r = pd.DataFrame(rows).set_index("tri")
r["now→placar"] = r.placar - r.nowcast
r["placar→ultima"] = r.ultima - r.placar
print(r.round(2).to_string())
ok = r.dropna(subset=["placar"])
print(f"\nnowcast→placar: n={len(ok)}, média {ok['now→placar'].mean():+.2f}, mediana {ok['now→placar'].median():+.2f}, "
      f"mín {ok['now→placar'].min():+.2f}, máx {ok['now→placar'].max():+.2f}, positivas {int((ok['now→placar']>0).sum())}")
pos = ok[ok.index >= pd.Period('2024Q3')]
print(f"desde a quebra (3T24+): n={len(pos)}, média {pos['now→placar'].mean():+.2f}, positivas {int((pos['now→placar']>0).sum())}")
# variação da central de um trimestre fixo entre edições consecutivas, últimas 4 edições
for a, b in zip(ed[-5:-1], ed[-4:]):
    comum = v[[a, b]].dropna()
    comum = comum[comum.index >= "2024-01-01"]
    print(f"{a.date()}→{b.date()}: revisão média dos trimestres desde 1T24 {(comum[b]-comum[a]).mean():+.2f}")
# a revisão nowcast→placar contra o PIB do trimestre (qoq dessaz. e yoy oficiais, atv_pib_taxas)
t = pd.read_csv("../A/atv_pib_taxas.csv.gz", parse_dates=["date"])
t = t[t.name == "pib_pm"].pivot_table(index="date", columns="indicador", values="value")
t.index = t.index.to_period("Q")
j = ok.join(t[["qoq", "yoy"]], how="inner")
print(j[["now→placar", "qoq", "yoy"]].round(2).to_string())
print(f"corr(revisão, qoq) = {j['now→placar'].corr(j.qoq):.2f}; corr(revisão, yoy) = {j['now→placar'].corr(j.yoy):.2f}")
import numpy as np
b = np.polyfit(j.qoq, j["now→placar"], 1)
print(f"revisão = {b[1]:+.2f} {b[0]:+.2f} × qoq ; com qoq 3T26 = -0,3 -> {b[1]+b[0]*-0.3:+.2f}; qoq 0,2 -> {b[1]+b[0]*0.2:+.2f}")
lo = j[j.qoq <= 0.3]
print(f"trimestres com qoq ≤ 0,3: n={len(lo)}, revisão média {lo['now→placar'].mean():+.2f}, {lo.index.tolist()}")
