"""Atividade, Q1: o 3T26 pelo IBC-Br.
- meses do IBC-Br (dessaz.) de abr a ago/2026, cheio e ex-agro;
- variação trimestral do IBC-Br contra o PIB do IBGE (qoq e yoy), últimos 12 trimestres: quanto o IBC-Br erra o PIB;
- 3T26: interanual do IBC-Br nos dois meses publicados (sem ajuste), e a qoq do tri sob três hipóteses para setembro;
- hiato do 3T26 implícito pela identidade do F: hiato(3T26) = hiato(3T25) + PIB yoy(3T26) - potencial (2,50)."""
import pandas as pd
from pathlib import Path
A = Path(__file__).resolve().parents[1] / "A"
ib = pd.read_csv(A / "atv_ibcbr.csv.gz", parse_dates=["date"])
tx = pd.read_csv(A / "atv_pib_taxas.csv.gz", parse_dates=["date"])

def s(name):
    return ib[ib.name == name].set_index("date")["value"].sort_index()

sa, sa_ex, nsa, nsa_ex = s("ibcbr_sa"), s("ibcbr_ex_agropecuaria_sa"), s("ibcbr_nsa"), s("ibcbr_ex_agropecuaria_nsa")
print("Meses, dessaz.:")
print(pd.DataFrame({"ibcbr_sa": sa, "ex_agro_sa": sa_ex, "agro_sa": s("ibcbr_agropecuaria_sa"),
                    "ind_sa": s("ibcbr_industria_sa"), "serv_sa": s("ibcbr_servicos_sa")}).loc["2026-01":].round(2))

q_sa = sa.resample("QS").mean(); q_nsa = nsa.resample("QS").mean()
n = sa.resample("QS").count()
qoq_ib = (q_sa / q_sa.shift(1) - 1) * 100
yoy_ib = (q_nsa / q_nsa.shift(4) - 1) * 100
pib_qoq = tx[(tx.name == "pib_pm") & (tx.indicador == "qoq")].set_index("date")["value"]
pib_yoy = tx[(tx.name == "pib_pm") & (tx.indicador == "yoy")].set_index("date")["value"]
cmp_ = pd.DataFrame({"ib_qoq": qoq_ib, "pib_qoq": pib_qoq, "ib_yoy": yoy_ib, "pib_yoy": pib_yoy}).dropna()
cmp_ = cmp_.loc["2023-07":]
cmp_["erro_qoq"] = cmp_.pib_qoq - cmp_.ib_qoq
cmp_["erro_yoy"] = cmp_.pib_yoy - cmp_.ib_yoy
print("\nIBC-Br trimestral contra o PIB (12 tri até 2T26):")
print(cmp_.round(2))
print("erro qoq: media %.2f, dp %.2f, min %.2f, max %.2f" % (cmp_.erro_qoq.mean(), cmp_.erro_qoq.std(), cmp_.erro_qoq.min(), cmp_.erro_qoq.max()))
print("erro yoy: media %.2f, dp %.2f, min %.2f, max %.2f" % (cmp_.erro_yoy.mean(), cmp_.erro_yoy.std(), cmp_.erro_yoy.min(), cmp_.erro_yoy.max()))

# 3T26: dois meses
jul_ago = ["2026-07-01", "2026-08-01"]
jul_ago_ant = ["2025-07-01", "2025-08-01"]
yoy2 = (nsa.loc[jul_ago].mean() / nsa.loc[jul_ago_ant].mean() - 1) * 100
yoy2_ex = (nsa_ex.loc[jul_ago].mean() / nsa_ex.loc[jul_ago_ant].mean() - 1) * 100
print(f"\n3T26, jul-ago contra jul-ago/2025 (sem ajuste): IBC-Br {yoy2:.2f}%, ex-agro {yoy2_ex:.2f}%")
q2 = sa.loc["2026-04":"2026-06"].mean(); q2_ex = sa_ex.loc["2026-04":"2026-06"].mean()
ago = sa.loc["2026-08-01"]; ago_ex = sa_ex.loc["2026-08-01"]
for nome, setv in [("setembro = agosto", 0.0), ("setembro +0,5%", 0.5), ("setembro +1,0%", 1.0), ("setembro -0,5%", -0.5)]:
    m3 = sa.loc[["2026-07-01", "2026-08-01"]].tolist() + [ago * (1 + setv / 100)]
    m3x = sa_ex.loc[["2026-07-01", "2026-08-01"]].tolist() + [ago_ex * (1 + setv / 100)]
    print(f"  {nome}: 3T26 qoq IBC-Br {(sum(m3)/3/q2-1)*100:.2f}%, ex-agro {(sum(m3x)/3/q2_ex-1)*100:.2f}%")
need = (3 * q2 - sa.loc["2026-07-01"] - ago) / ago * 100 - 100
print(f"  setembro precisa crescer {need:.2f}% sobre agosto para o 3T26 empatar com o 2T26 (IBC-Br cheio)")

# hiato implícito no 3T26 pela identidade do F
hi = pd.read_csv(A / "pm_hiato_produto.csv.gz", parse_dates=["date"])
c = hi[hi.variavel == "central"].set_index("date")["value"]
h3t25 = c.loc["2025-07-01"]; pot = 2.50
erro_yoy_med = cmp_.erro_yoy.mean()
print(f"\nhiato 3T25 (edicao 2026-09) = {h3t25}; potencial do F = {pot}")
for nome, y in [("Focus 3T26 1,70", 1.70), ("QPC 3T26 1,82", 1.82),
                ("IBC-Br jul-ago cru", yoy2), ("IBC-Br jul-ago + erro medio yoy", yoy2 + erro_yoy_med)]:
    if y is None:
        continue
    print(f"  {nome}: PIB yoy {y:.2f} -> hiato 3T26 {h3t25 + y - pot:.2f} (contra 0,41 do BC: {h3t25 + y - pot - 0.41:+.2f})")
print("\n3T26 qoq do PIB pelo IBC-Br (setembro = agosto) mais e menos um dp do erro qoq: %.2f a %.2f" % (
    -0.55 - cmp_.erro_qoq.std(), -0.55 + cmp_.erro_qoq.std()))
