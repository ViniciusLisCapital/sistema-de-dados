"""in_temperos: contas auxiliares do report de inflação, ciclo 2026-10-27, rodada 1.

 1. Soma das cinco maiores contribuições do IPCA de set/26 e a fatia do mês que elas explicam.
 2. PTAX: variação de 23/10 para 26/10; Brent: média de out/26 contra a média do 3T26.
 3. Pesos dos quatro grupos do BC no IPCA de set/26 (de inflc_dim + inflc_decomposicao).
 4. Focus por componente 2027 (mediana 23/10) × peso do grupo: a contribuição que a Focus
    implica, para comparar com a do modelo no 4T27 (0,63 alim., 1,76 serv., 0,82 ind., 1,01 mon.).
 5. Tamanho dos temperos (ii): peso × variação suposta.
 6. Diferença entre o caminho do modelo e a projeção do Copom (pm_copom_projecoes, reunião 281).
"""
import sys
from pathlib import Path

import pandas as pd

sys.stdout.reconfigure(encoding="utf-8")
A = Path(__file__).resolve().parent.parent / "A"
rd = lambda n: pd.read_csv(A / f"{n}.csv.gz")

# 1
top = [0.318, 0.083, 0.069, 0.062, 0.044]   # F, inflc_decomposicao, set/26
print(f"1. cinco maiores contribuições: {sum(top):.3f} p.p. de 0,82 = {sum(top)/0.82*100:.0f}%;"
      f" energia sozinha {0.318/0.82*100:.0f}%; IPCA sem as cinco ~ {0.82-sum(top):.2f}")

# 2
px = rd("cmb_ptax")
pt = px[px.name == "ptax_venda"].set_index("date")["value"]
print(f"2. PTAX 23/10 {pt['2026-10-23']} → 26/10 {pt['2026-10-26']}: {(pt['2026-10-26']/pt['2026-10-23']-1)*100:+.1f}%")
br = rd("comm_brent"); br["date"] = pd.to_datetime(br["date"])
b = br[br.name == "brent_usd"].set_index("date")["value"]
m3, mo = b.loc["2026-07":"2026-09"].mean(), b.loc["2026-10"].mean()
print(f"   Brent média out/26 {mo:.1f} contra 3T26 {m3:.1f}: {(mo/m3-1)*100:+.0f}%;"
      f" 20/10 {b.iloc[-1]} contra 02/10 {b['2026-10-02']}: {(b.iloc[-1]/b['2026-10-02']-1)*100:+.0f}%")

# 3
dc = rd("inflc_decomposicao"); dim = rd("inflc_dim")
dc = dc[(dc.indice == "IPCA") & (dc.date == "2026-09-01")].merge(
    dim[["subitem_codigo", "grupo", "subgrupo", "item"]], on="subitem_codigo", how="left")
dc["bc"] = dc.apply(lambda r: "Monitorados" if r.grupo == "Monitorados" else
                    {"Alimentos": "Alimentação", "Bens Industriais": "Industriais",
                     "Serviços": "Serviços"}.get(r.subgrupo, "?"), axis=1)
w = dc.groupby("bc")["pesos"].sum() / dc.pesos.sum() * 100
print("3. pesos set/26 (%):", w.round(1).to_dict())
wn = dc[dc.item == "Alimentos in natura"].pesos.sum() / dc.pesos.sum() * 100
print(f"   in natura {wn:.2f}%")

# 4
fp = rd("expc_focus_periodo__componentes__inflacao")
last = fp.date.max()
f = fp[(fp.date == last) & (fp.data_referencia == 2027)][["indicador", "detalhe", "mediana"]]
print(f"4. Focus 2027 por componente ({last}):")
print(f.to_string(index=False))
mapa = {"Alimentação": 6.77, "Serviços": 5.16, "Industriais": 2.71, "Monitorados": 3.99}
mapa["Alimentação"] = 5.76
mod = {"Alimentação": 0.63, "Serviços": 1.76, "Industriais": 0.82, "Monitorados": 1.01}
for g, v in mapa.items():
    print(f"   {g}: Focus 2027 {v:.2f}% × peso {w[g]:.1f}% = {v*w[g]/100:.2f} p.p.; modelo 4T27 {mod[g]:.2f};"
          f" diferença {v*w[g]/100-mod[g]:+.2f}")
print(f"   soma Focus implícita {sum(mapa[g]*w[g]/100 for g in mapa):.2f} (Focus IPCA 2027 4,34); modelo 4T27 4,23")

# 5
comb = 6.05   # item Combustíveis (veículos), peso set/26 (inflc_decomposicao_item)
ener = 3.98
print("5. temperos (ii):")
for v in (5, 3, -3):
    print(f"   combustíveis {v:+d}% × {comb}% = {comb*v/100:+.2f} p.p.")
for v in (5, -5):
    print(f"   energia elétrica {v:+d}% × {ener}% = {ener*v/100:+.2f} p.p.")
for v in (10, -10):
    print(f"   in natura {v:+d}% × {wn:.2f}% = {wn*v/100:+.2f} p.p.")

# 6
cop = {"4T26": 5.2, "1T27": 4.9, "2T27": 4.5, "3T27": 4.5, "4T27": 3.9, "1T28": 3.2}
mdl = {"4T26": 5.28, "1T27": 4.85, "2T27": 4.33, "3T27": 4.34, "4T27": 4.23, "1T28": 4.08}
print("6. modelo − Copom (p.p.):", {k: round(mdl[k]-cop[k], 2) for k in cop})
# livres e monitorados do modelo, em contribuição, no 1T28 e 4T27
print(f"   1T28 modelo: livres (serv+alim+ind) 1,69+0,61+0,81 = {1.69+0.61+0.81:.2f} p.p. em {100-w['Monitorados']:.1f}% de peso"
      f" ≈ {(1.69+0.61+0.81)/(100-w['Monitorados'])*100:.1f}%; monitorados 0,97 p.p. ≈ {0.97/w['Monitorados']*100:.1f}%")
print(f"   1T28 modelo: serviços 1,69 p.p. ≈ {1.69/w['Serviços']*100:.1f}%")

# 7. conferências do texto
ag = rd("inflc_agregados"); ag["date"] = pd.to_datetime(ag["date"])
ip = ag[ag.name == "ipca"].set_index("date")["value"]
q4 = {}
for y in range(2016, 2026):
    v = 1.0
    for m in (10, 11, 12):
        v *= 1 + ip[pd.Timestamp(f"{y}-{m:02d}-01")] / 100
    q4[y] = round((v - 1) * 100, 2)
print("7. IPCA no 4T, 2016-2025:", q4, "| abaixo de 0,60:", [y for y, v in q4.items() if v < 0.60])
print(f"   in natura jul+ago/26 composto: {((1-0.0598)*(1-0.0438)-1)*100:.1f}%")
print(f"   alimentação no 12m que a contribuição do modelo no 4T27 implica: 0,63/{w['Alimentação']:.1f}% ≈ {0.63/w['Alimentação']*100:.1f}%")
