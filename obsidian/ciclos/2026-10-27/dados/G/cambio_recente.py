"""G cambio: trajetória diária recente do real, dos pares, do CDS, dos índices de dólar e da curva DI,
e variações nas janelas usadas no report (fim do 3T26 = 30/09; ciclo anterior = 22/10; corte)."""
import pandas as pd
from pathlib import Path

A = Path(__file__).resolve().parent.parent / "A"
pd.set_option("display.width", 250); pd.set_option("display.max_rows", 500)

def ler(t):
    return pd.read_csv(A / f"{t}.csv.gz", parse_dates=["date"])

ptax = ler("cmb_ptax"); ptax = ptax[ptax.name == "ptax_venda"].set_index("date").value.rename("BRL")
lat = ler("cmb_fx_latam").pivot(index="date", columns="country_code", values="value")
# CL e CO: taxa do dia útil seguinte é a formada no dia (Atenção do F): desloca um pregão para trás
for c in ("CL", "CO"):
    s = lat[c].dropna(); lat[c] = pd.Series(s.values[1:], index=s.index[:-1]).reindex(lat.index)
cds = ler("cmb_risco_pais"); cds = cds[cds.name == "cds_5y_usd"].set_index("date").value.rename("CDS")
em = ler("cmb_dollar_index_em").set_index("date").value.rename("DXY_EM")
dxy = ler("cmb_dollar_index").set_index("date").value.rename("DXY")
sp = ler("cmb_equity_us").set_index("date").value.rename("SP500")
brent = ler("comm_brent").set_index("date").value.rename("Brent")
di = ler("br_di_grade")
def di_prazo(dc):
    d = di[(di.dc >= dc - 20) & (di.dc <= dc + 20)].copy()
    d["dist"] = (d.dc - dc).abs()
    return d.sort_values("dist").groupby("date").first().value.rename(f"DI{dc}")
di1 = di_prazo(365); di2 = di_prazo(730); di5 = di_prazo(1826)

df = pd.concat([ptax, lat, cds, em, dxy, sp, brent, di1, di2, di5], axis=1)
df = df[df.index >= "2026-08-25"]
print(df.round(4).to_string())

def em_data(s, d):
    s = s.dropna(); s = s[s.index <= d]; return s.iloc[-1], s.index[-1].date()

print("\nVariações (% para preços, p.b./pontos para CDS e DI):")
janelas = [("2026-09-30", "2026-10-22"), ("2026-10-22", "2026-10-27"), ("2026-09-30", "2026-10-27"),
           ("2026-09-25", "2026-10-27"), ("2026-07-31", "2026-10-27")]
for col in df.columns:
    s = pd.concat([ptax, lat, cds, em, dxy, sp, brent, di1, di2, di5], axis=1)[col]
    linhas = []
    for a, b in janelas:
        va, da = em_data(s, a); vb, db = em_data(s, b)
        if col in ("CDS",) or col.startswith("DI"):
            linhas.append(f"{a}->{b}: {va:.2f}({da})->{vb:.2f}({db}) Δ={vb-va:+.2f}")
        else:
            linhas.append(f"{a}->{b}: {va:.4f}({da})->{vb:.4f}({db}) {100*(vb/va-1):+.2f}%")
    print(col, " | ".join(linhas))
