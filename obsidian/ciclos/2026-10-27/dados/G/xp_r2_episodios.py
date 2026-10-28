"""Expectativas, rodada 2: como os anos-calendário da Focus reagiram a choques parecidos com o de 26/10.

Lê só A/ (expc_focus_periodo__inflacao, expc_focus__inflacao, cmb_ptax, br_interest_rate).
 (a) Depois de uma depreciação da PTAX de 5% ou mais em 21 dias úteis (episódios separados por
     pelo menos 63 dias úteis; a mesma definição do G xp_historico (d) da rodada 1), quanto a
     mediana da Focus para o IPCA de t+1 e de t+2 (anos fixados na data do episódio) andou em
     30 e em 45 dias úteis. 30 dias úteis depois de 26/10 é a véspera da reunião de 09/12.
     Conta também em quantos episódios t+1 subiu 0,26 p.p. ou mais e t+2 0,25 p.p. ou mais
     (os sinalizadores do agente de política monetária: 2027 acima de 4,6 e 2028 acima de 4,0).
 (b) Depois de uma alta da inflação implícita de 24 meses de 0,60 p.p. ou mais em 5 dias úteis
     (episódios separados por 63 dias úteis, desde 2006), quanto andaram a Focus 12m, t+1 e t+2
     em 30 e 45 dias úteis, e quanto da alta da implícita restava 45 dias úteis depois
     (fração: (implícita 45 du depois − implícita 5 du antes do episódio) / alta em 5 du).
"""
from pathlib import Path
import numpy as np
import pandas as pd

A = Path(__file__).resolve().parent.parent / "A"
p = pd.read_csv(A / "expc_focus_periodo__inflacao.csv.gz")
p = p[(p.indicador == "IPCA") & (p.periodicidade == "anual") & (p.base_calculo == 0)
      & (p.tipo_calculo == "geral")].copy()
p["date"] = pd.to_datetime(p.date)
p["ref"] = p.data_referencia.astype(int)
anual = p.pivot_table(index="date", columns="ref", values="mediana").sort_index()

f = pd.read_csv(A / "expc_focus__inflacao.csv.gz")
f12 = f[(f.indicador == "IPCA") & (f.horizonte == "12m") & (f.suavizada == "S") & (f.base_calculo == 0)
        & (f.tipo_calculo == "geral")].set_index("date").mediana.sort_index()
f12.index = pd.to_datetime(f12.index)

def passo(serie, d0, n):
    """valor antes de d0 (último <= d0) e n observações depois."""
    s = serie.dropna()
    a = s[:d0]
    b = s[d0:]
    if len(a) == 0 or len(b) <= n:
        return None
    return a.iloc[-1], b.iloc[n] - a.iloc[-1]

def episodios(sinal, limiar, sep=63):
    eps, last = [], None
    for dte, v in sinal.items():
        if v >= limiar and (last is None or (sinal.index.get_loc(dte) - sinal.index.get_loc(last)) >= sep):
            eps.append(dte); last = dte
    return eps

# (a)
pt = pd.read_csv(A / "cmb_ptax.csv.gz")
pt = pt[pt.name == "ptax_venda"].copy(); pt["date"] = pd.to_datetime(pt.date)
pt = pt.set_index("date").value.sort_index()
pt = pt[pt.index >= "2001-12-01"]
ch = (pt / pt.shift(21) - 1).dropna()
rows = []
for e in episodios(ch, 0.05):
    ano = e.year
    lin = {"data": e.date(), "ptax_21d_%": round(ch[e] * 100, 1)}
    ok = True
    for k in (1, 2):
        if ano + k not in anual.columns:
            ok = False; break
        for n in (30, 45):
            r = passo(anual[ano + k], e, n)
            if r is None:
                ok = False; break
            lin[f"t+{k} antes"] = round(r[0], 2)
            lin[f"Δt+{k} {n}du"] = round(r[1], 2)
    if ok:
        rows.append(lin)
df = pd.DataFrame(rows)
print("(a) episódios de depreciação ≥5% em 21 du, desde 2001-12\n", df.to_string(index=False))
for c in ["Δt+1 30du", "Δt+1 45du", "Δt+2 30du", "Δt+2 45du"]:
    x = df[c]
    print(f"   {c}: n={len(x)} mediana {x.median():+.2f} p25 {x.quantile(.25):+.2f} p75 {x.quantile(.75):+.2f} "
          f"p90 {x.quantile(.9):+.2f} máx {x.max():+.2f} · subiu em {100*(x>0).mean():.0f}% · parado (|Δ|<0,05) em {100*(x.abs()<0.05).mean():.0f}%")
for c, lim in [("Δt+1 30du", 0.26), ("Δt+1 45du", 0.26), ("Δt+2 30du", 0.25), ("Δt+2 45du", 0.25)]:
    print(f"   {c} ≥ {lim}: {int((df[c] >= lim).sum())} de {len(df)} ({100*(df[c] >= lim).mean():.0f}%)")
g = df[df["ptax_21d_%"] >= 8]
print(f"   só os episódios ≥8% (n={len(g)}): Δt+1 30du mediana {g['Δt+1 30du'].median():+.2f}, "
      f"Δt+2 30du mediana {g['Δt+2 30du'].median():+.2f}, Δt+1 45du mediana {g['Δt+1 45du'].median():+.2f}, "
      f"Δt+2 45du mediana {g['Δt+2 45du'].median():+.2f}")
d10 = df[pd.to_datetime(df.data) >= "2010-01-01"]
print(f"   desde 2010 (n={len(d10)}): Δt+2 45du mediana {d10['Δt+2 45du'].median():+.2f}, "
      f"p75 {d10['Δt+2 45du'].quantile(.75):+.2f}; Δt+1 45du mediana {d10['Δt+1 45du'].median():+.2f}, p75 {d10['Δt+1 45du'].quantile(.75):+.2f}")

# (b)
r = pd.read_csv(A / "br_interest_rate.csv.gz")
r["date"] = pd.to_datetime(r.date)
def impl(ten):
    di = r[(r.curve == "DIPRE") & (r.tenor == ten)].set_index("date").value
    nb = r[(r.curve == "NTNBJS") & (r.tenor == ten)].set_index("date").value
    return (((1 + di / 100) / (1 + nb / 100) - 1) * 100).dropna().sort_index()
i24 = impl("24M")
d5 = (i24 - i24.shift(5)).dropna()
rows = []
for e in episodios(d5, 0.60):
    ano = e.year
    lin = {"data": e.date(), "Δimpl24 5du": round(d5[e], 2)}
    pos = i24.index.get_loc(e)
    if pos + 45 >= len(i24):
        lin["resta da alta em 45du"] = None
    else:
        lin["resta da alta em 45du"] = round((i24.iloc[pos + 45] - i24.iloc[pos - 5]) / d5[e], 2)
    for nome, s in [("f12", f12), ("t+1", anual.get(ano + 1)), ("t+2", anual.get(ano + 2))]:
        for n in (30, 45):
            rr = None if s is None else passo(s, e, n)
            lin[f"Δ{nome} {n}du"] = None if rr is None else round(rr[1], 2)
    rows.append(lin)
db = pd.DataFrame(rows)
print("\n(b) altas da implícita de 24 meses ≥0,60 p.p. em 5 du, desde 2006\n", db.to_string(index=False))
ok = db.dropna()
for c, lim in [("Δt+1 30du", 0.26), ("Δt+1 45du", 0.26), ("Δt+2 30du", 0.25), ("Δt+2 45du", 0.25), ("Δf12 45du", 0.0)]:
    print(f"   {c} ≥ {lim}: {int((ok[c] >= lim).sum())} de {len(ok)}" if lim else f"   {c} > 0: {int((ok[c] > 0).sum())} de {len(ok)}")
print(f"   Δt+1 30du mediana {ok['Δt+1 30du'].median():+.2f} · Δt+2 30du mediana {ok['Δt+2 30du'].median():+.2f}")
print(f"   com 45 du depois (n={len(ok)}): Δf12 mediana {ok['Δf12 45du'].median():+.2f}, Δt+1 mediana {ok['Δt+1 45du'].median():+.2f}, "
      f"Δt+2 mediana {ok['Δt+2 45du'].median():+.2f}; fração da alta que restava: mediana {ok['resta da alta em 45du'].median():.2f}")

# (c) Para o agente de câmbio: nos mesmos episódios de (a), quanto da depreciação a Focus do câmbio
#     de fim do ano corrente incorporou em 5 e em 30 dias úteis: Δ% da mediana / Δ% da PTAX em 21 du.
#     Episódios depois de setembro usam o ano seguinte (o ano corrente já está quase realizado).
c = pd.read_csv(A / "expc_focus_periodo__cambio.csv.gz")
c = c[(c.base_calculo == 0) & (c.tipo_calculo == "geral")].copy()
c["date"] = pd.to_datetime(c.date); c["ref"] = c.data_referencia.astype(int)
cam = c.pivot_table(index="date", columns="ref", values="mediana").sort_index()
rows = []
for e in episodios(ch, 0.05):
    ano = e.year + (1 if e.month >= 10 else 0)
    if ano not in cam.columns:
        continue
    lin = {"data": e.date(), "ptax_21d_%": round(ch[e] * 100, 1), "ref": ano}
    ok = True
    for n in (5, 30):
        rr = passo(cam[ano], e, n)
        if rr is None:
            ok = False; break
        lin[f"fração {n}du"] = round((rr[1] / rr[0]) / ch[e], 2)
    if ok:
        rows.append(lin)
dc = pd.DataFrame(rows)
print("\n(c) Focus do câmbio de fim de ano: fração da depreciação incorporada\n", dc.to_string(index=False))
for k in ("fração 5du", "fração 30du"):
    print(f"   {k}: n={len(dc)} mediana {dc[k].median():.2f} p25 {dc[k].quantile(.25):.2f} p75 {dc[k].quantile(.75):.2f}")

# (d) a semana de 26/10 contra todas as janelas de 5 dias úteis desde 2006, e as contagens de (b)
ant = d5[d5.index < "2026-10-26"]
print(f"\n(d) implícita 24m, maior alta em 5 du antes de 2026-10-26: {ant.max():+.2f} em {ant.idxmax().date()}; "
      f"em 2026-10-26: {d5.loc['2026-10-26']:+.2f}")
okb = db.dropna()
for c in ["Δf12 45du", "Δt+1 45du", "Δt+2 45du"]:
    print(f"   (b) {c} > 0 em {int((okb[c] > 0).sum())} de {len(okb)}")
