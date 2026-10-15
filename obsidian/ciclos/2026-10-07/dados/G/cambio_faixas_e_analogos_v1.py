"""G · câmbio · ciclo 2026-10-07 · calibração das faixas e análogos eleitorais.

Lê só ../A/. Três contas:
1. Distribuição histórica da variação log da PTAX em 39, 142 e 268 dias úteis (horizontes de
   fim de nov/2026, fim de abr/2027 e fim de out/2027 a partir de 06/10/2026), em 10 anos e
   desde 2003, e o desvio-padrão implícito pela vol realizada de 63 dias de hoje.
2. Análogos: PTAX no último dia útil antes do 1º turno presidencial, no primeiro depois, e no fim
   do mês seguinte (nov), em abr e em out do ano seguinte. Datas do 1º turno (fato do calendário
   eleitoral, não do F): 2002-10-06, 2006-10-01, 2010-10-03, 2014-10-05, 2018-10-07, 2022-10-02.
   DXY nas mesmas janelas, para separar o dólar global.
3. Fluxo cambial financeiro contratado em nov, dez e jan, média 2016-2025 (sazonalidade).
"""
from pathlib import Path

import numpy as np
import pandas as pd

A = Path(__file__).resolve().parent.parent / "A"


def rd(nome):
    return pd.read_csv(A / f"{nome}.csv.gz", parse_dates=["date"])


p = rd("cmb_ptax")
p = p[p.name == "ptax_venda"].set_index("date")["value"].sort_index()
lp = np.log(p)
r = lp.diff().dropna()

hoje = p.index[-1]
print("Último PTAX:", hoje.date(), p.iloc[-1])
for nome, alvo in [("fim nov/26", "2026-11-30"), ("fim abr/27", "2027-04-30"), ("fim out/27", "2027-10-29")]:
    du = len(pd.bdate_range(hoje + pd.Timedelta(days=1), alvo))
    vol63 = r.iloc[-63:].std() * np.sqrt(252)
    vol252 = r.iloc[-252:].std() * np.sqrt(252)
    print(f"\n== {nome}: {du} dias úteis (calendário seg-sex, sem feriados)")
    print(f"vol 63d anual {vol63*100:.1f}% · vol 252d anual {vol252*100:.1f}% · sigma no horizonte (vol 252d) {vol252*np.sqrt(du/252)*100:.1f}%")
    for ini in ["2016-10-01", "2003-06-01"]:
        x = lp[lp.index >= ini]
        ch = (x.shift(-du) - x).dropna()
        q = np.exp(ch.quantile([0.05, 0.10, 0.25, 0.50, 0.75, 0.90, 0.95])) - 1
        print(f"  desde {ini}: n={len(ch)} " + " ".join(f"q{int(k*100)}={v*100:+.1f}%" for k, v in q.items()))
        s0 = p.iloc[-1]
        print("    em R$/US$ a partir de 4,9698: " + " ".join(f"q{int(k*100)}={s0*(1+v):.2f}" for k, v in q.items()))

dxy = rd("cmb_dollar_index").set_index("date")["value"].sort_index()


def em(s, d, antes=False):
    d = pd.Timestamp(d)
    return (s[s.index < d].iloc[-1], s[s.index < d].index[-1]) if antes else (s[s.index >= d].iloc[0], s[s.index >= d].index[0])


def fim_mes(s, ano, mes):
    x = s[(s.index.year == ano) & (s.index.month == mes)]
    return x.iloc[-1] if len(x) else np.nan


print("\n== Análogos eleitorais (PTAX; entre parênteses, DXY na mesma janela)")
for d in ["2002-10-06", "2006-10-01", "2010-10-03", "2014-10-05", "2018-10-07", "2022-10-02"]:
    y = int(d[:4])
    a, da = em(p, d, antes=True)
    b, db = em(p, d)
    xa, _ = em(dxy, d, antes=True)
    xb, _ = em(dxy, d)
    nov, abr, out = fim_mes(p, y, 11), fim_mes(p, y + 1, 4), fim_mes(p, y + 1, 10)
    dnov, dabr, dout = fim_mes(dxy, y, 11), fim_mes(dxy, y + 1, 4), fim_mes(dxy, y + 1, 10)
    f = lambda u, v: (v / u - 1) * 100
    print(f"{d}: antes {a:.4f} ({da.date()}) -> depois {b:.4f} ({db.date()}) {f(a,b):+.1f}% (DXY {f(xa,xb):+.1f}%) | "
          f"desde o dia seguinte: fim nov {f(b,nov):+.1f}% (DXY {f(xb,dnov):+.1f}%), fim abr {f(b,abr):+.1f}% (DXY {f(xb,dabr):+.1f}%), "
          f"fim out+1 {f(b,out):+.1f}% (DXY {f(xb,dout):+.1f}%)")

cc = rd("cmb_cambio_contratado")
cc = cc[cc.name == "cc_fin_saldo"].set_index("date")["value"].sort_index()
m = cc.resample("MS").sum() / 1000
m = m[(m.index >= "2016-01-01") & (m.index < "2026-01-01")]
print("\n== Fluxo financeiro contratado, média mensal 2016-2025 (US$ bi)")
print(m.groupby(m.index.month).mean().round(2).to_string())
