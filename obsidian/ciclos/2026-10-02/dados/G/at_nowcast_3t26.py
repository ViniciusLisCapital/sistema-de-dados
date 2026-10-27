"""at_ · nowcast do 3T26 pelo IBC-Br e a tradução em hiato pela identidade da linha companheira.
Lê só A/. Q1 do report de atividade, rodada 1."""
import pandas as pd
A = "../A/"
d = pd.read_csv(A + "atv_ibcbr.csv.gz", parse_dates=["date"])
w = d.pivot_table(index="date", columns="name", values="value")
def q(s):
    return s.resample("QS").mean()
out = {}
for nome in ["ibcbr", "ibcbr_ex_agropecuaria"]:
    sa = w[nome + "_sa"].dropna(); nsa = w[nome + "_nsa"].dropna()
    # q/q dessaz.: (a) média dos 2 meses; (b) setembro = agosto
    q2 = sa["2026-04-01":"2026-06-01"].mean(); q1 = sa["2026-01-01":"2026-03-01"].mean()
    jul, ago = sa["2026-07-01"], sa["2026-08-01"]
    out[nome] = {
        "2T26 qoq": 100 * (q2 / q1 - 1),
        "3T26 qoq, media jul-ago": 100 * ((jul + ago) / 2 / q2 - 1),
        "3T26 qoq, set=ago": 100 * ((jul + 2 * ago) / 3 / q2 - 1),
        "3T26 qoq, set = ago +0,5%": 100 * ((jul + ago + ago * 1.005) / 3 / q2 - 1),
        # yoy sem ajuste: jul-ago/26 contra jul-ago/25, e 2T26 contra 2T25
        "jul-ago yoy (nsa)": 100 * (nsa["2026-07-01":"2026-08-01"].mean() / nsa["2025-07-01":"2025-08-01"].mean() - 1),
        "2T26 yoy (nsa)": 100 * (nsa["2026-04-01":"2026-06-01"].mean() / nsa["2025-04-01":"2025-06-01"].mean() - 1),
        "1T26 yoy (nsa)": 100 * (nsa["2026-01-01":"2026-03-01"].mean() / nsa["2025-01-01":"2025-03-01"].mean() - 1),
        "3T25 yoy (nsa)": 100 * (nsa["2025-07-01":"2025-09-01"].mean() / nsa["2024-07-01":"2024-09-01"].mean() - 1),
    }
for k, v in out.items():
    print(k); [print(f"  {a}: {b:.2f}") for a, b in v.items()]
# PIB yoy oficial, para calibrar IBC-Br contra PIB
t = pd.read_csv(A + "atv_pib_taxas.csv.gz", parse_dates=["date"])
pib = t[(t.name == "pib_pm") & (t.indicador == "yoy")].set_index("date")["value"]
print("PIB yoy oficial:", pib["2025-07-01":].to_dict())
# identidade: hiato_3T26 = hiato_3T25 + yoy_3T26 - potencial (2,495; média dos 4 potenciais implícitos do F)
pot = (2.66 + 2.60 + 2.53 + 2.19) / 4
h3t25 = 0.95
print(f"potencial medio = {pot:.3f}")
for yoy in [1.0, 1.2, 1.5, 1.82, 1.96, 2.0]:
    print(f"  yoy 3T26 = {yoy:.2f} -> hiato 3T26 implícito = {h3t25 + yoy - pot:.2f}")
# q/q: hiato_3T = hiato_2T + (g_qq - pot_qq)
potq = 100 * ((1 + pot / 100) ** 0.25 - 1)
print(f"potencial trimestral = {potq:.2f}")
for g in [-0.5, -0.3, 0.0, 0.2, 0.5]:
    print(f"  qoq 3T26 = {g:+.1f} -> hiato 3T26 = {0.51 + g - potq:.2f}")
# calibração: PIB yoy oficial menos IBC-Br yoy (nsa, média do trimestre), 2T24 a 2T26
nsa = w["ibcbr_nsa"].dropna()
iq = nsa.resample("QS").mean()
iy = 100 * (iq / iq.shift(4) - 1)
cal = pd.DataFrame({"pib": pib, "ibc": iy}).dropna()["2024-04-01":"2026-04-01"]
cal["dif"] = cal.pib - cal.ibc
print(cal.round(2).to_string())
print(f"dif média 2T24-2T26 = {cal.dif.mean():.2f}; mín {cal.dif.min():.2f}; máx {cal.dif.max():.2f}")
ibc_ja = out["ibcbr"]["jul-ago yoy (nsa)"]
for k in [cal.dif.min(), cal.dif.mean(), cal.dif.max()]:
    y = ibc_ja + k
    print(f"  PIB yoy 3T26 = {y:.2f} -> hiato 3T26 = {h3t25 + y - pot:.2f}")
