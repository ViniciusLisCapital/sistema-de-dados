"""Expectativas, ciclo 2026-10-02: as leituras da Focus com o que estava DIVULGADO em 02/10.

A Focus é divulgada na segunda com as respostas coletadas até a sexta anterior: em 02/10 a última
divulgada era a de 28/09, com coleta até 25/09. Este G refaz, na data 2026-09-25, as leituras do F
que dependem da Focus (12m, 24m, componentes, anos-calendário, distância à meta e o percentil dela,
média do 3T26 sem as pesquisas de 28-30/09), e confere a mesma conta em 2026-10-02 contra o F.
Lê só ../A/."""
import pandas as pd
from pathlib import Path

A = Path(__file__).resolve().parent.parent / "A"
fo = pd.read_csv(A / "expc_focus__inflacao.csv.gz", parse_dates=["date"])
pe = pd.read_csv(A / "expc_focus_periodo__inflacao.csv.gz", parse_dates=["date"])
se = pd.read_csv(A / "expc_focus_periodo__selic.csv.gz", parse_dates=["date"])
cp = pd.read_csv(A / "expc_focus_copom.csv.gz", parse_dates=["date"])
meta = pd.read_csv(A / "inflc_meta.csv.gz", parse_dates=["date"])
meta = {d.year: v for d, v in zip(meta["date"], meta["value"])}
ult_meta = max(meta)
def m(ano): return meta.get(ano, meta[ult_meta])

D1, D0 = pd.Timestamp("2026-09-25"), pd.Timestamp("2026-10-02")

def nome(s): return s.encode("latin1", "ignore").decode("latin1")
fo["ind"] = fo["indicador"].map(nome)

# 1) Focus 12m e 24m, suavizada, por indicador, base 0 e base 1
print("== Focus por horizonte móvel, suavizada")
for d in (D1, D0):
    x = fo[(fo.date == d) & (fo.suavizada == "S")]
    for _, r in x.sort_values(["ind", "horizonte", "base_calculo"]).iterrows():
        print(d.date(), r["ind"][:28].ljust(28), r.horizonte, "base", r.base_calculo,
              "med", r.mediana, "media", r.media, "dp", r.desvio_padrao, "n", r.numero_respondentes)

# 2) média do trimestre (a variável da tese) no 3T26: com e sem as pesquisas de 28-30/09
v = fo[(fo.ind == "IPCA") & (fo.horizonte == "12m") & (fo.suavizada == "S") & (fo.base_calculo == 0)]
v = v.set_index("date")["mediana"].sort_index()
q3 = v["2026-07-01":"2026-09-30"]
print("\n== 3T26 média: todas", round(q3.mean(), 4), len(q3), "| até 25/09", round(q3[:D1].mean(), 4), len(q3[:D1]))
print("4T26 até 02/10:", v["2026-10-01":].round(4).to_dict())
print("12m mediana em 2026-09-04, 07-03, 06-26, 09-25:", v.get(pd.Timestamp("2026-09-04")), v.get(pd.Timestamp("2026-07-03")), v.get(pd.Timestamp("2026-06-26")), v.get(D1))
# trajetória semanal recente
print("12m, sextas recentes:", v["2026-06-01":][v["2026-06-01":].index.dayofweek == 4].round(2).to_dict())

# 3) anos-calendário IPCA e componentes
an = pe[(pe.periodicidade == "anual") & (pe.base_calculo == 0)].copy()
an["ind"] = an["indicador"].map(nome)
an["ano"] = an["data_referencia"].astype(str).str[:4].astype(int)
print("\n== Anos-calendário, mediana (média, dp, n)")
for d in (D1, pd.Timestamp("2026-09-04"), D0):
    x = an[an.date == d]
    for ind, g in x.groupby("ind"):
        g = g[(g.ano >= 2026) & (g.ano <= 2030)].sort_values("ano")
        print(d.date(), ind[:28].ljust(28), [(a, md, round(me, 2), round(dp, 2)) for a, md, me, dp in zip(g.ano, g.mediana, g.media, g.desvio_padrao)])

# 4) distância à meta por ano-calendário (t, t+1, t+2, t+3) e percentil histórico, como o F
ip = an[an.ind == "IPCA"][["date", "ano", "mediana"]]
ip = ip.assign(k=ip.ano - ip.date.dt.year)
ip = ip[ip.k.between(0, 3)]
ip["dist"] = ip.mediana - ip.ano.map(m)
print("\n== Distância à meta por horizonte, e percentil (todas as pesquisas até a data; últimos 10 anos)")
for d in (D1, D0):
    for k in range(4):
        h = ip[(ip.k == k) & (ip.date <= d)].sort_values("date")
        hoje = h[h.date == d]["dist"].iloc[0]
        p_all = (h.dist < hoje).mean() * 100 + (h.dist == hoje).mean() * 50
        h10 = h[h.date > d - pd.DateOffset(years=10)]
        p10 = (h10.dist < hoje).mean() * 100 + (h10.dist == hoje).mean() * 50
        # quando foi a última vez que a distância esteve igual ou acima de hoje
        acima = h[(h.dist >= hoje) & (h.date < d - pd.Timedelta(days=60))]
        ult = acima.date.max().date() if len(acima) else None
        print(d.date(), f"t+{k}", "dist", round(hoje, 2), "pctl hist", round(p_all), "pctl 10a", round(p10),
              "última vez >= (antes de 60d atrás):", ult)

# 4b) 12m: distância à meta (meta pesada pelos meses da janela) e percentil, até 25/09
def meta12(d):
    ms = 12 - d.month  # meses restantes no ano (aprox. do F: o ano e o seguinte pesados pelos meses)
    return (ms * m(d.year) + (12 - ms) * m(d.year + 1)) / 12
w = v.to_frame("med")
w["dist"] = [md - meta12(d) for d, md in zip(w.index, w.med)]
for d in (D1, D0):
    h = w[:d]
    hoje = h.dist.iloc[-1]
    print(d.date(), "12m dist", round(hoje, 2), "pctl hist", round((h.dist < hoje).mean() * 100 + (h.dist == hoje).mean() * 50),
          "pctl 10a", round(((h[h.index > d - pd.DateOffset(years=10)].dist < hoje).mean()) * 100))

# 5) Selic por ano e por reunião, em 25/09
print("\n== Selic anual, mediana")
for d in (D1, D0):
    x = se[(se.date == d) & (se.base_calculo == 0) & (se.data_referencia.between(2026, 2030))]
    print(d.date(), dict(zip(x.data_referencia, x.mediana)))
print("== Selic por reunião, mediana")
for d in (D1, D0):
    x = cp[(cp.date == d) & (cp.base_calculo == 0)]
    print(d.date(), dict(zip(x.reuniao, x.mediana)))

# 6) mensal e trimestral IPCA, em 25/09
mm = pe[(pe.periodicidade == "mensal") & (pe.base_calculo == 0) & (pe.indicador == "IPCA")]
for d in (D1, D0):
    x = mm[(mm.date == d) & (mm.ref_date >= "2026-09-01") & (mm.ref_date <= "2027-02-01")]
    print(d.date(), "IPCA mensal", dict(zip(x.data_referencia, x.mediana)))
