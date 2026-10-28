"""Expectativas: padrões históricos usados no report (cada um com a janela dita).

Lê só A/. Imprime:
 (a) com que frequência a média das 46 pesquisas seguintes da Focus 12m (suavizada, base 0,
     mediana) ficou 0,48 p.p. ou mais ABAIXO do valor do dia — o que o 4T26 do modelo exige;
 (b) a distância implícita (DIPRE/NTNBJS) − Focus no mesmo prazo, 12 e 24 meses: hoje
     (implícita de 2026-10-26 contra a Focus de 2026-10-23, e as duas em 2026-10-23) e o
     percentil na história comum das duas séries;
 (c) média − mediana da Focus por ano-calendário em t+3 (ano corrente + 3), percentil;
 (d) depois de uma depreciação da PTAX de 5% ou mais em 21 dias úteis (episódios separados por
     pelo menos 63 dias úteis), quanto a Focus 12m andou nos 45 dias úteis seguintes.
"""
from pathlib import Path
import numpy as np
import pandas as pd

A = Path(__file__).resolve().parent.parent / "A"
f = pd.read_csv(A / "expc_focus__inflacao.csv.gz")
def foc(h):
    s = f[(f.indicador == "IPCA") & (f.horizonte == h) & (f.suavizada == "S") & (f.base_calculo == 0)
          & (f.tipo_calculo == "geral")].set_index("date").mediana.sort_index()
    s.index = pd.to_datetime(s.index)
    return s
f12, f24 = foc("12m"), foc("24m")

# (a)
fut = f12[::-1].rolling(46).mean()[::-1].shift(-1)
dif = (fut - f12).dropna()
for ini in ["2001-01-01", "2016-10-01"]:
    x = dif[dif.index >= ini]
    print(f"(a) desde {ini[:4]}: n={len(x)}, queda ≥0,48 em {100*(x <= -0.48).mean():.1f}% dos dias; "
          f"pctl 5 = {x.quantile(.05):+.2f}, pctl 1 = {x.quantile(.01):+.2f}")
    # condicionado a PTAX: nada; e condicionado a Focus acima de 4,3
# (b)
r = pd.read_csv(A / "br_interest_rate.csv.gz")
r["date"] = pd.to_datetime(r.date)
def impl(ten):
    di = r[(r.curve == "DIPRE") & (r.tenor == ten)].set_index("date").value
    nb = r[(r.curve == "NTNBJS") & (r.tenor == ten)].set_index("date").value
    return (((1 + di / 100) / (1 + nb / 100) - 1) * 100).dropna().sort_index()
for ten, fs in [("12M", f12), ("24M", f24)]:
    im = impl(ten)
    j = pd.concat([im.rename("imp"), fs.rename("foc")], axis=1).dropna()
    gap = j.imp - j.foc
    hoje_pre = gap.loc["2026-10-23"]
    hoje = im.loc["2026-10-26"] - fs.loc["2026-10-23"]
    print(f"(b) {ten}: desde {j.index[0].date()} n={len(gap)} · gap em 2026-10-23 = {hoje_pre:+.2f} "
          f"(pctl {100*(gap < hoje_pre).mean():.0f}) · implícita 26/10 − Focus 23/10 = {hoje:+.2f} "
          f"(pctl {100*(gap < hoje).mean():.0f}) · mediana hist {gap.median():+.2f}, máx {gap.max():+.2f} em {gap.idxmax().date()}")
    g10 = gap[gap.index >= "2016-10-01"]
    print(f"     últimos 10 anos: pctl de {hoje:+.2f} = {100*(g10 < hoje).mean():.0f}, mediana {g10.median():+.2f}")
# (c)
p = pd.read_csv(A / "expc_focus_periodo__inflacao.csv.gz")
p = p[(p.indicador == "IPCA") & (p.periodicidade == "anual") & (p.base_calculo == 0) & (p.tipo_calculo == "geral")].copy()
p["ano"] = pd.to_datetime(p.date).dt.year
p["ref"] = p.data_referencia.astype(int)
for k in (2, 3):
    x = p[p.ref == p.ano + k].set_index("date")
    mm = (x.media - x.mediana).dropna()
    hoje = mm.iloc[-1]
    print(f"(c) t+{k}: média − mediana em {mm.index[-1]} = {hoje:+.3f}; pctl hist {100*(mm < hoje).mean():.0f} "
          f"(n={len(mm)} desde {mm.index[0]}); últimos 10a pctl {100*(mm[mm.index>='2016-10-01'] < hoje).mean():.0f}")
# (d)
pt = pd.read_csv(A / "cmb_ptax.csv.gz")
pt = pt[pt.name == "ptax_venda"].copy(); pt["date"] = pd.to_datetime(pt.date)
pt = pt.set_index("date").value.sort_index()
pt = pt[pt.index >= "2001-12-01"]
ch = pt / pt.shift(21) - 1
eps, last = [], None
for dte, v in ch.items():
    if v >= 0.05 and (last is None or (pt.index.get_loc(dte) - pt.index.get_loc(last)) >= 63):
        eps.append(dte); last = dte
rows = []
for e in eps:
    a = f12[:e]
    b = f12[e:]
    if len(a) == 0 or len(b) < 46:
        continue
    rows.append((e.date(), round(ch[e] * 100, 1), round(a.iloc[-1], 2), round(b.iloc[45] - a.iloc[-1], 2)))
df = pd.DataFrame(rows, columns=["data", "ptax_21d_%", "focus12_antes", "Δ focus12 em 45 du"])
print("(d)\n", df.to_string(index=False))
print(f"   n={len(df)}, mediana Δ {df.iloc[:,3].median():+.2f}, pctl25 {df.iloc[:,3].quantile(.25):+.2f}, "
      f"pctl75 {df.iloc[:,3].quantile(.75):+.2f}, subiu em {100*(df.iloc[:,3]>0).mean():.0f}%")
d16 = df[pd.to_datetime(df.data) >= "2010-01-01"]
print(f"   desde 2010: n={len(d16)}, mediana {d16.iloc[:,3].median():+.2f}, pctl75 {d16.iloc[:,3].quantile(.75):+.2f}, subiu em {100*(d16.iloc[:,3]>0).mean():.0f}%")

# (e) o tamanho do pregão de 2026-10-26 na história: PTAX (variação % em um dia, desde 1999-02)
#     e inflação implícita de 24 e 60 meses (variação em p.p. em um dia, desde 2006)
pt2 = pd.read_csv(A / "cmb_ptax.csv.gz")
pt2 = pt2[pt2.name == "ptax_venda"].copy(); pt2["date"] = pd.to_datetime(pt2.date)
pt2 = pt2.set_index("date").value.sort_index()
pt2 = pt2[pt2.index >= "1999-02-01"]
d1 = (pt2 / pt2.shift(1) - 1).dropna() * 100
v = d1.loc["2026-10-26"]
maiores = d1.sort_values(ascending=False).head(6)
print(f"(e) PTAX em 2026-10-26: {v:+.2f}% no dia; maiores altas diárias desde 1999-02:")
print(maiores.round(2).to_string())
for ten in ["24M", "60M"]:
    im = impl(ten)
    dd = im.diff().dropna()
    v = dd.loc["2026-10-26"]
    print(f"    implícita {ten} em 2026-10-26: {v:+.2f} p.p. no dia; pctl {100*(dd < v).mean():.2f}; "
          f"maiores: {dd.sort_values(ascending=False).head(4).round(2).to_dict()}")
