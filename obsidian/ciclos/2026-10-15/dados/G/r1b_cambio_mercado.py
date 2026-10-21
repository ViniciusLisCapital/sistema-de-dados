"""G r1b: condições de mercado: datas das intervenções do BC (set-out), fluxo contratado diário de outubro,
COT do BRL (12 semanas), swap e posição dos bancos (6 meses), data da alta do Fed, diferencial ex-ante
(DI 2 anos − Treasury 2 anos), e a PTAX média dos 5 dias úteis até a sexta antes do Copom de 16/09."""
from pathlib import Path
import numpy as np
import pandas as pd

A = Path(__file__).resolve().parents[1] / "A"
rd = lambda t: pd.read_csv(A / f"{t}.csv.gz", parse_dates=["date"])
pd.set_option("display.width", 250)

r = rd("cmb_reservas_bc")
for n in ["bcb_intervention_spot", "bcb_intervention_repo_lines", "bcb_intervention_forwards", "bcb_intervention_fx_loans_repos"]:
    x = r[(r.name == n) & (r.date >= "2026-06-01")][["date", "value"]]
    print(n, x.to_string(index=False) if len(x) else "sem registro desde jun")
for n in ["bcb_swap_cambial_position", "bank_fx_spot_position", "reserves_total_monthly"]:
    x = r[r.name == n].tail(7)[["date", "value"]]
    print(n); print(x.to_string(index=False))

c = rd("cmb_cambio_contratado")
x = c[(c.date >= "2026-09-01") & c.name.isin(["cc_saldo_total", "cc_saldo_comercial", "cc_fin_saldo"])]
x = x.pivot_table(index="date", columns="name", values="value")
print("fluxo diário (US$ mi)"); print(x.round(0).to_string())
print("soma set (US$ mi)", x.loc["2026-09"].sum().round(0).to_dict())
print("soma 01-09/out (US$ mi)", x.loc["2026-10"].sum().round(0).to_dict())
print("soma 01-02/out", x.loc["2026-10-01":"2026-10-02"].sum().round(0).to_dict(), "· 05-09/out", x.loc["2026-10-05":"2026-10-09"].sum().round(0).to_dict())

t = rd("cmb_cot_fx")
t = t[(t.currency == "BRL") & t.name.isin(["lev_net", "asset_mgr_net", "dealer_net", "open_interest", "lev_long", "lev_short"])]
print(t.pivot_table(index="date", columns="name", values="value").tail(14).to_string())

u = rd("us_interest_rate")
pol = u[u.curve == "POLICY"].set_index("date")["value"]
ch = pol[pol.diff() != 0].tail(4)
print("Fed: mudanças da meta", ch.to_string())
ust2 = u[(u.curve == "US_TREASURY") & (u.tenor == "2Y")].set_index("date")["value"]

di = rd("br_di_grade")
di = di[di.date >= "2026-09-01"]
di2 = pd.Series({d: np.interp(504, g.sort_values("du").du, g.sort_values("du").value) for d, g in di.groupby("date")})
for d in ["2026-09-14", "2026-09-30", "2026-10-13"]:
    dd = pd.Timestamp(d)
    a = di2[:dd].iloc[-1]; b = ust2[:dd].iloc[-1]
    print(f"{d}: DI 2a {a:.2f} − UST 2a {b:.2f} = {a-b:.2f} p.p.")

p = rd("cmb_ptax"); p = p[p.name == "ptax_venda"].set_index("date")["value"]
ref = p[:"2026-09-11"].tail(5)
print("PTAX 5 dias úteis até 11/09:", ref.round(4).to_dict(), "média", round(ref.mean(), 4), "· 14/10 contra ela:", f"{100*(p.iloc[-1]/ref.mean()-1):+.2f}%")
