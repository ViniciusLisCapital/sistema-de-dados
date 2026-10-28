"""G cambio (rodada 2): (1) a volatilidade realizada da PTAX que a janela de 63 dias terá em 31/12/2026 se os
pregões restantes forem calmos, e a implícita que a relação histórica (a mesma de cambio_vol.py) daria com ela;
(2) o modelo com o base do P1 e três variações: vol do 4T26 em 18,5; F.b_sp500 x 0,55 no base e no downside."""
import json
import numpy as np
import pandas as pd
from pathlib import Path
from analytics.agent_system import modelo

A = Path(__file__).resolve().parent.parent / "A"
d = json.load(open(A / "modelo_estrutural.json", encoding="utf-8"))
p = d["p"]; iv = pd.Series(p["var"]["vol"]["obs"], index=p["rot"], dtype="float")
pt = pd.read_csv(A / "cmb_ptax.csv.gz", parse_dates=["date"])
pt = pt[pt.name == "ptax_venda"].set_index("date").value.sort_index()
r = np.log(pt).diff().dropna()
rv21 = r.rolling(21).std() * np.sqrt(252) * 100
rv63 = r.rolling(63).std() * np.sqrt(252) * 100
def fim(k):
    a, q = int(k[:4]), int(k[-1]); return pd.Timestamp(a, 3 * q, 1) + pd.offsets.MonthEnd(0)
rows = []
for k in p["rot"]:
    t = fim(k); a = rv21[rv21.index <= t]; b = rv63[rv63.index <= t]
    rows.append((iv[k], a.iloc[-1] if len(a) else np.nan, b.iloc[-1] if len(b) else np.nan))
ok = pd.DataFrame(rows, columns=["iv", "r21", "r63"]).dropna()
X = np.column_stack([np.ones(len(ok)), ok.r21, ok.r63]); c, *_ = np.linalg.lstsq(X, ok.iv, rcond=None)
print(f"implícita = {c[0]:.2f} + {c[1]:.3f}*real21 + {c[2]:.3f}*real63 (N={len(ok)})")

feriados = pd.to_datetime(["2026-11-02", "2026-11-20", "2026-12-25"])
resto = [x for x in pd.bdate_range("2026-10-27", "2026-12-31") if x not in feriados]
print("pregões restantes no 4T26 (aprox.):", len(resto))
for calma in (8.0, 10.0, 13.0):
    s = calma / 100 / np.sqrt(252)
    hist = r.values
    sim = np.concatenate([hist, np.full(len(resto), s)])   # retorno constante em módulo: só a variância importa
    # desvio-padrão com sinais alternados para média ~0
    sim[-len(resto):] = s * np.where(np.arange(len(resto)) % 2 == 0, 1, -1)
    w63 = sim[-63:]; w21 = sim[-21:]
    v63 = w63.std(ddof=1) * np.sqrt(252) * 100; v21 = w21.std(ddof=1) * np.sqrt(252) * 100
    print(f"  restante a {calma:.0f}% a.a.: real21 {v21:.1f}  real63 {v63:.1f}  -> implícita ajustada {c[0] + c[1]*v21 + c[2]*v63:.1f}")

P = json.load(open(Path(__file__).resolve().parent.parent.parent / "P1.json", encoding="utf-8"))
base = {k: dict(v) for k, v in P["caminhos_usados"].items()}
T = ["4T26", "1T27", "2T27", "3T27", "4T27", "1T28"]
def com(**mud):
    cc = {k: dict(v) for k, v in base.items()}
    for k, v in mud.items(): cc[k] = dict(zip(T, v))
    return cc
VOL_DN = [13.0, 12.5, 12.0, 12.0, 12.0, 12.0]
CDS_DN = [115, 110, 108, 106, 105, 105]
RR_DN = [7.35, 6.90, 6.80, 6.75, 6.70, 6.70]
sim_ = modelo.carregar("2026-10-27")
for nome, cam, m in [
    ("base_vol_4T26_18.5", com(vol=[18.5, 15.5, 14.5, 14.0, 13.5, 13.5]), {}),
    ("base_sp_x0.55", base, {"F.b_sp500": 0.55}),
    ("downside_sp_x0.55", com(vol=VOL_DN, fiscal=CDS_DN, rr_10a=RR_DN), {"F.b_sp500": 0.55}),
]:
    res = modelo.rodar(sim_, caminhos=cam, mult=m)
    linhas = [l for l in modelo.texto(res, trimestres=T).splitlines() if l.startswith("| PTAX") or l.startswith("| Selic, fech")]
    print(f"\n## {nome}"); print("\n".join(linhas))
