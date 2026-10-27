"""in_corte: a leitura do IPCA com a informação disponível no corte do ciclo (2026-10-02).

O IPCA de set/26 foi divulgado em 9/10, depois do corte, e o F o traz (o F corta pela data de
referência, não pela de divulgação). Esta G refaz as leituras com o que existia em 02/10:
o IPCA até ago/26 e o IPCA-15 de set/26 (divulgado antes do corte).

Imprime:
  1. IPCA de ago/26: grupos do BC, núcleos e difusão — mês, acumulado 3m e 12m;
  2. ago/26 contra o mesmo mês dos 10 anos anteriores;
  3. IPCA de ago/26: maiores contribuições por subitem;
  4. IPCA-15 de set/26: os quatro grupos do BC refeitos dos subitens, maiores contribuições,
     e a comparação com o IPCA-15 de setembro dos 10 anos anteriores;
  5. trimestre 3T26 parcial (jul-ago) e o 3T26 com o QPC para setembro;
  6. IPCA 12m de set/26 e dez/26 implícitos nas medianas do QPC (set 0,56; out 0,34; nov 0,32;
     dez 0,55), a partir do 12m de ago/26.
"""
from pathlib import Path
import numpy as np
import pandas as pd

A = Path(__file__).resolve().parents[1] / "A"
pd.set_option("display.width", 220)

ag = pd.read_csv(A / "inflc_agregados.csv.gz", parse_dates=["date"])
dec = pd.read_csv(A / "inflc_decomposicao.csv.gz", parse_dates=["date"])
dim = pd.read_csv(A / "inflc_dim.csv.gz", encoding="utf-8")
piv = ag.pivot_table(index="date", columns="name", values="value").loc[:"2026-08-01"]

def acc(s):
    return (np.prod(1 + s / 100) - 1) * 100

cols = ["ipca", "ipca_servicos", "ipca_alimentacao", "ipca_industriais", "ipca_administrado", "ipca_livres",
        "ipca_nucleo_ex0", "ipca_nucleo_ex03", "ipca_nucleo_ex03_servicos", "ipca_nucleo_ex03_industriais",
        "ipca_nucleo_exfe", "ipca_nucleo_medias_aparadas", "ipca_nucleo_medias_aparadas_sem_suavizacao",
        "ipca_nucleo_p55", "ipca_nucleo_dp"]
print("1. IPCA ago/26 (mês · 3m · 12m · 12m 3 meses antes):")
for c in cols:
    v = piv[c].dropna()
    print(f"  {c:45s} {v.iloc[-1]:6.2f} {acc(v.iloc[-3:]):6.2f} {acc(v.iloc[-12:]):6.2f} {acc(v.iloc[-15:-3]):6.2f}")
d = piv["ipca_indice_difusao"].dropna()
print("  difusão ago/26:", d.iloc[-1], "; jul:", d.iloc[-2], "; média 10a:", round(d.loc["2016-09-01":].mean(), 1),
      "; pctl 10a:", round((d.loc["2016-09-01":] < d.iloc[-1]).mean() * 100))
nuc5 = ["ipca_nucleo_ex0", "ipca_nucleo_ex03", "ipca_nucleo_medias_aparadas", "ipca_nucleo_p55", "ipca_nucleo_dp"]
print("  média de EX0, EX3, MS, P55, DP em ago/26:", round(piv[nuc5].iloc[-1].mean(), 3),
      "; 3m:", round(np.mean([acc(piv[c].iloc[-3:]) for c in nuc5]), 2))

print("\n2. ago contra o mesmo mês 2016-2025:")
for c in ["ipca", "ipca_servicos", "ipca_alimentacao", "ipca_industriais", "ipca_administrado",
          "ipca_nucleo_ex03", "ipca_nucleo_medias_aparadas"]:
    v = piv[c]
    hist = np.array([v.loc[f"{y}-08-01"] for y in range(2016, 2026)])
    cur = v.loc["2026-08-01"]
    print(f"  {c:32s} {cur:6.2f} média {hist.mean():5.2f} mín {hist.min():5.2f} máx {hist.max():5.2f} "
          f"abaixo {int((hist < cur).sum())} de 10")
    h3 = np.array([acc(v.loc[f"{y}-06-01":f"{y}-08-01"]) for y in range(2016, 2026)])
    c3 = acc(v.loc["2026-06-01":"2026-08-01"])
    print(f"  {'':32s} jun-ago {c3:6.2f} média {h3.mean():5.2f} abaixo {int((h3 < c3).sum())} de 10")

dim["g"] = np.where(dim["grupo"].str.startswith("Monit"), "Monitorados", dim["subgrupo"])
names = dim.set_index("subitem_codigo")["nome"]
def topo(ind, mes, n=6):
    x = dec[(dec["indice"] == ind) & (dec["date"] == mes)].copy()
    x["nome"] = x["subitem_codigo"].map(names)
    x = x.sort_values("contribuicao")
    return x
x = topo("IPCA", "2026-08-01")
print("\n3. IPCA ago/26, para baixo:")
print(x.head(6)[["nome", "var_mensal", "pesos", "contribuicao"]].round(3).to_string(index=False))
print("para cima:")
print(x.tail(6)[["nome", "var_mensal", "pesos", "contribuicao"]].round(3).to_string(index=False))

print("\n4. IPCA-15 set/26 por grupo do BC (refeito dos subitens):")
def grupos(ind, mes):
    y = dec[(dec["indice"] == ind) & (dec["date"] == mes)].merge(dim[["subitem_codigo", "g", "subjacente"]],
                                                                  on="subitem_codigo", how="left")
    out = {}
    for g, z in y.groupby("g"):
        out[g] = (round(z["contribuicao"].sum() / z["pesos"].sum(), 2), round(z["contribuicao"].sum(), 3),
                  round(z["pesos"].sum() * 100 / y["pesos"].sum(), 1))
    sub = y[(y["g"] == "Serviços") & (y["subjacente"].notna())]
    out["Serviços subjacentes (subjacente não nulo)"] = round(sub["contribuicao"].sum() / sub["pesos"].sum(), 2) if len(sub) else None
    out["total"] = round(y["contribuicao"].sum(), 3)
    return out
print("  (variação %, contribuição p.p., peso %)", grupos("IPCA15", "2026-09-01"))
print("  dim.subjacente valores:", dim["subjacente"].dropna().unique()[:5], "; item serviços:", dim[dim.g == "Serviços"]["item"].unique())
y15 = dec[(dec["indice"] == "IPCA15") & (dec["date"] == "2026-09-01")].merge(dim[["subitem_codigo", "g", "item"]], on="subitem_codigo")
ss = y15[y15["item"] == "Serviços Subjacente"]
print("  serviços subjacentes IPCA-15 set/26:", round(ss["contribuicao"].sum() / ss["pesos"].sum(), 2))
x = topo("IPCA15", "2026-09-01")
print("  IPCA-15 set/26, para cima:")
print(x.tail(7)[["nome", "var_mensal", "pesos", "contribuicao"]].round(3).to_string(index=False))
print("  para baixo:")
print(x.head(5)[["nome", "var_mensal", "pesos", "contribuicao"]].round(3).to_string(index=False))
i15 = ag[ag["name"] == "ipca15"].set_index("date")["value"]
h = np.array([i15.loc[f"{y}-09-01"] for y in range(2016, 2026)])
print(f"  IPCA-15 set: 0,70 contra média {h.mean():.2f}, mín {h.min():.2f}, máx {h.max():.2f}, abaixo {int((h < 0.70).sum())} de 10")
print("  IPCA-15 por grupo, ago/26:", grupos("IPCA15", "2026-08-01"))

ip = piv["ipca"]
print("\n5. jul+ago/26 composto:", round(acc(ip.loc["2026-07-01":"2026-08-01"]), 2),
      "; com set = 0,56 (QPC):", round(acc(np.array([0.07, -0.32, 0.56])), 2))
f = 1.0422 * 1.0056 / 1.0048
print("6. 12m set/26 implícito no QPC:", round((f - 1) * 100, 2))
for a, b_ in [(0.34, 0.09), (0.32, 0.18), (0.55, 0.33)]:
    f *= (1 + a / 100) / (1 + b_ / 100)
print("   12m dez/26 implícito no QPC:", round((f - 1) * 100, 2))

# 7. serviços subjacentes no IPCA de ago/26; combustíveis e energia no IPCA-15 de set/26;
#    tabaco; e o 12m de energia e combustíveis até ago/26
def sub_media(ind, mes, item):
    y = dec[(dec["indice"] == ind) & (dec["date"] == mes)].merge(dim[["subitem_codigo", "item"]], on="subitem_codigo")
    z = y[y["item"] == item]
    return round(z["contribuicao"].sum() / z["pesos"].sum(), 2)
print("\n7. serviços subjacentes IPCA ago/26:", sub_media("IPCA", "2026-08-01", "Serviços Subjacente"),
      "; jul/26:", sub_media("IPCA", "2026-07-01", "Serviços Subjacente"),
      "; IPCA-15 set/26:", sub_media("IPCA15", "2026-09-01", "Serviços Subjacente"))
ss = [sub_media("IPCA", f"2026-{m:02d}-01", "Serviços Subjacente") for m in (6, 7, 8)]
print("   serviços subjacentes jun-ago/26 composto:", round(acc(np.array(ss)), 2))
for cod, nm in [(5104001, "Gasolina"), (5104003, "Óleo diesel"), (2201004, "Gás de botijão"), (2202003, "Energia")]:
    for ind in ["IPCA", "IPCA15"]:
        s = dec[(dec["indice"] == ind) & (dec["subitem_codigo"] == cod)].set_index("date")["var_mensal"]
        fim = "2026-08-01" if ind == "IPCA" else "2026-09-01"
        s = s.loc[:fim]
        print(f"   {nm} {ind}: últimos 4 {s.iloc[-4:].round(2).tolist()}; 12m até {fim[:7]}: {acc(s.iloc[-12:]):.2f}")
cig = dim[dim["nome"].str.contains("Cigarro", na=False)][["subitem_codigo", "nome", "g"]]
print("   cigarro:", cig.to_dict("records"))
