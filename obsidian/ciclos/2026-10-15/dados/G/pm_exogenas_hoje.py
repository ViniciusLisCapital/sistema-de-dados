"""G pm: nível de hoje, média do 3T26, média do 4T26 até o corte e média do 4T26 se o último valor
se mantiver até 31/12, para as exógenas do Modelo Estrutural que a política monetária usa.
Lê só A/. Ciclo 2026-10-15."""
from pathlib import Path
import pandas as pd

A = Path(__file__).resolve().parent.parent / "A"
CORTE = pd.Timestamp("2026-10-15")
T3 = (pd.Timestamp("2026-07-01"), pd.Timestamp("2026-09-30"))
T4 = (pd.Timestamp("2026-10-01"), pd.Timestamp("2026-12-31"))


def serie(arq, **filtro):
    d = pd.read_csv(A / arq, parse_dates=["date"])
    for k, v in filtro.items():
        d = d[d[k] == v]
    return d.set_index("date")["value"].sort_index()


def resumo(nome, s):
    s = s[s.index <= CORTE]
    t3 = s[(s.index >= T3[0]) & (s.index <= T3[1])].mean()
    q = s[(s.index >= T4[0])]
    ult_d, ult = s.index[-1], s.iloc[-1]
    # dias úteis restantes do 4T26 depois do último dado, com o último valor repetido
    resto = pd.bdate_range(ult_d + pd.Timedelta(days=1), T4[1])
    n_obs = len(q)
    t4_mantido = (q.sum() + ult * len(resto)) / (n_obs + len(resto)) if n_obs else float("nan")
    print(f"{nome}: último {ult:.3f} ({ult_d.date()}) · média 3T26 {t3:.3f} · média 4T26 até o corte "
          f"{q.mean():.3f} ({n_obs} obs.) · 4T26 se o último se mantiver {t4_mantido:.3f}")


resumo("NTN-B 10 anos (juro real, % a.a.)", serie("br_interest_rate.csv.gz", curve="NTNBJS", tenor="120M"))
resumo("Selic meta (% a.a.)", serie("br_interest_rate.csv.gz", curve="POLICY", tenor="1d"))
resumo("CDS 5 anos (p.b.)", serie("cmb_risco_pais.csv.gz", name="cds_5y_usd"))
resumo("Fed funds, meta ponto médio (% a.a.)", serie("us_interest_rate__curva.csv.gz", curve="POLICY", tenor="1d"))
resumo("Dólar contra emergentes (índice)", serie("cmb_dollar_index_em.csv.gz", name="dxy_em"))
resumo("Brent (US$/barril)", serie("comm_brent.csv.gz", name="brent_usd"))
for n in ["icbr_usd", "icbr_agropecuaria_usd", "icbr_metal_usd", "icbr_energia_usd"]:
    s = serie("comm_icbr_usd.csv.gz", name=n)
    print(f"{n}: " + " · ".join(f"{d:%Y-%m} {v:.2f}" for d, v in s.iloc[-4:].items())
          + f" · média 3T26 {s['2026-07-01':'2026-09-01'].mean():.2f}")

# trajetória recente da NTN-B 10a e do DI 10a: onde aconteceu o movimento de outubro
ntnb = serie("br_interest_rate.csv.gz", curve="NTNBJS", tenor="120M")
di10 = serie("br_interest_rate.csv.gz", curve="DIPRE", tenor="120M")
ust10 = serie("us_interest_rate__curva.csv.gz", curve="US_TREASURY", tenor="10Y")
j = pd.concat({"ntnb10": ntnb, "di10": di10, "ust10": ust10}, axis=1)["2026-09-10":"2026-10-15"].dropna(how="all")
print(j.round(2).to_string())

# Convenção do simulador (fechamento ou média do trimestre): o valor no último dia útil de 2T26 e 3T26
for nome, s in [("CDS", serie("cmb_risco_pais.csv.gz", name="cds_5y_usd")),
                ("dxy_em", serie("cmb_dollar_index_em.csv.gz", name="dxy_em")),
                ("Fed funds meta", serie("us_interest_rate__curva.csv.gz", curve="POLICY", tenor="1d")),
                ("NTN-B 10a", ntnb)]:
    for fim in ["2026-06-30", "2026-09-30"]:
        v = s[:fim]
        print(f"{nome} no fechamento de {fim}: {v.iloc[-1]:.3f} ({v.index[-1].date()})")
