"""in_leituras: as contas da argumentação do report de inflação, ciclo 2026-10-02, rodada 1.

Lê só ../A/. Imprime:
  1. surpresa do IPCA de set/26 contra o QPC (mediana), e núcleos contra a média esperada;
  2. o 4T25 mês a mês (o trimestre que sai da janela de 12 meses no 4T26), por grupo, e os
     subitens de maior contribuição de out-dez/25;
  3. a trajetória do Brent (últimos 30 pregões e médias mensais desde jun/26);
  4. o padrão sazonal do 4º trimestre (out-dez) do IPCA e dos grupos, 10 anos;
  5. distribuição histórica da variação trimestral das médias do IC-Br agro e metal em US$;
  6. as médias trimestrais recentes do IC-Br agro e metal em US$ e do IC-Br energia;
  7. energia elétrica residencial e gasolina: últimos 15 meses;
  8. peso dos grupos do BC no mês e a variação de 12m implícita na contribuição do modelo.
"""
from pathlib import Path
import numpy as np
import pandas as pd

A = Path(__file__).resolve().parents[1] / "A"
pd.set_option("display.width", 200)

ag = pd.read_csv(A / "inflc_agregados.csv.gz", parse_dates=["date"])
dec = pd.read_csv(A / "inflc_decomposicao.csv.gz", parse_dates=["date"])
dim = pd.read_csv(A / "inflc_dim.csv.gz", encoding="latin-1")
usd = pd.read_csv(A / "comm_icbr_usd.csv.gz", parse_dates=["date"])
brl = pd.read_csv(A / "comm_icbr.csv.gz", parse_dates=["date"])
brent = pd.read_csv(A / "comm_brent.csv.gz", parse_dates=["date"])

print("nomes em inflc_agregados:", sorted(ag["name"].unique()))

# 1. surpresa
piv = ag.pivot_table(index="date", columns="name", values="value")
s = piv.loc["2026-09-01"]
print("\n1. IPCA set/26 =", s["ipca"], "; QPC mediana 0,56 -> surpresa", round(s["ipca"] - 0.56, 2))
nuc = [c for c in piv.columns if c.startswith("ipca_nucleo") or "nucleo" in c]
print("núcleos set/26:", s[nuc].round(2).to_dict())
print("média simples dos núcleos listados:", round(s[nuc].mean(), 3), "(QPC esperava 0,29 para a média dos núcleos)")
print("acima de 0,29:", int((s[nuc] > 0.29).sum()), "de", len(nuc))

# 2. 4T25
grupos = [c for c in piv.columns if c in ("ipca", "ipca_servicos", "ipca_alimentacao", "ipca_industriais",
                                          "ipca_monitorados", "ipca_bens_industriais", "ipca_alimentos")]
print("\n2. 4T25 e 4T24 mês a mês:")
print(piv.loc["2024-10-01":"2025-12-01", grupos])
d = dec[(dec["indice"] == "IPCA") & (dec["date"] >= "2025-10-01") & (dec["date"] <= "2025-12-01")]
d = d.merge(dim[["subitem_codigo", "nome", "subgrupo"]], on="subitem_codigo", how="left")
tot = d.groupby(["subitem_codigo", "nome"])["contribuicao"].sum().sort_values()
print("subitens out-dez/25, maiores contribuições para baixo (p.p., soma mensal):")
print(tot.head(6).round(3))
print("para cima:")
print(tot.tail(6).round(3))
for m in ["2025-10-01", "2025-11-01", "2025-12-01"]:
    x = d[d["date"] == m].sort_values("contribuicao")
    print(m, "pior:", x.iloc[0][["nome", "var_mensal", "contribuicao"]].to_dict())

# 3. Brent
b = brent.set_index("date")["value"]
print("\n3. Brent, últimos 30 pregões:")
print(b.iloc[-30:].round(2).to_string())
bm = b.resample("MS").mean()
print("médias mensais desde 2026-01:")
print(bm.loc["2026-01-01":].round(2))
print("máximo histórico diário:", round(b.max(), 2), b.idxmax().date())
print("pctl do último no histórico:", round((b < b.iloc[-1]).mean() * 100, 1))

# 4. sazonal 4T
print("\n4. out-dez composto, 2016-2025:")
for g in grupos:
    v = piv[g]
    rows = []
    for y in range(2016, 2026):
        q = v.loc[f"{y}-10-01":f"{y}-12-01"]
        rows.append((np.prod(1 + q / 100) - 1) * 100)
    rows = np.array(rows)
    print(f"  {g}: média {rows.mean():.2f}, mín {rows.min():.2f}, máx {rows.max():.2f}, mediana {np.median(rows):.2f}")
for g in grupos:
    v = piv[g]
    rows = []
    for y in range(2016, 2026):
        q = v.loc[f"{y}-01-01":f"{y}-03-01"]
        rows.append((np.prod(1 + q / 100) - 1) * 100)
    print(f"  1T {g}: média {np.mean(rows):.2f}")

# 5/6. IC-Br USD trimestral
u = usd.pivot_table(index="date", columns="name", values="value")
uq = u.resample("QS").mean()
print("\n6. médias trimestrais IC-Br US$ (últimos 8):")
print(uq.iloc[-8:].round(2))
for c in ["icbr_agropecuaria_usd", "icbr_metal_usd", "icbr_energia_usd"]:
    ch = (np.log(uq[c]).diff() * 100).dropna()
    ch2 = (np.log(uq[c]).diff(2) * 100).dropna()
    print(f"5. {c}: Δlog trimestral desde 1998, p10 {ch.quantile(.1):.1f}, p25 {ch.quantile(.25):.1f}, "
          f"p50 {ch.median():.1f}, p75 {ch.quantile(.75):.1f}, p90 {ch.quantile(.9):.1f}, dp {ch.std():.1f}; "
          f"2 trimestres p10 {ch2.quantile(.1):.1f} p90 {ch2.quantile(.9):.1f}")
print("set/26 vs média 3T26:", (u.iloc[-1] / uq.iloc[-1]).round(4).to_dict())
r = brl.pivot_table(index="date", columns="name", values="value")
print("IC-Br R$ últimos 6 meses:")
print(r.iloc[-6:])

# 7. energia e gasolina
names = dim.set_index("subitem_codigo")["nome"]
ipca = dec[dec["indice"] == "IPCA"].copy()
ipca["nome"] = ipca["subitem_codigo"].map(names)
for alvo in ["Energia el", "Gasolina", "Óleo diesel", "Gás de botijão", "Passagem aérea"]:
    x = ipca[ipca["nome"].fillna("").str.startswith(alvo.encode("latin-1").decode("latin-1"))]
    if x.empty:
        x = ipca[ipca["nome"].fillna("").str.contains(alvo[:5])]
    print(f"\n7. {alvo}:")
    print(x[x["date"] >= "2025-07-01"][["date", "nome", "var_mensal", "pesos", "contribuicao"]].to_string(index=False))

# 8. pesos dos grupos do BC no mês
last = ipca[ipca["date"] == "2026-09-01"].merge(dim[["subitem_codigo", "subgrupo", "grupo"]], on="subitem_codigo")
last["g"] = np.where(last["grupo"].str.startswith("Monit"), "Monitorados", last["subgrupo"])
w = last.groupby("g")["pesos"].sum() * 100 / last["pesos"].sum()
print("\n8. pesos (%):", w.round(2).to_dict())
