"""in_leituras: as contas do report de inflação do ciclo 2026-10-27 (rodada 1).

Lê só ../A/. Imprime:
 1. IPCA mensal de out-dez/2025 (sai da janela de 12m no 4T26) e de 2026.
 2. Padrão sazonal por trimestre (2016-2025), por grupo do BC: média, mín, máx.
 3. 4T26 implícito: pela Focus 2026 (mediana 23/10) e pela QPC (medianas de out-dez); o IPCA 12m
    de dez/26 que cada uma implica; idem com o IPCA-15 de outubro no lugar de outubro.
 4. IPCA-15 de outubro por grupo do BC e maiores contribuições por subitem.
 5. Alimentação por classe (in natura, semi-elaborados, industrializados): set/26, 3m e 12m.
 6. Energia elétrica residencial e gasolina, mês a mês, últimos 12 meses.
 7. PTAX: média de 3T26, média de outubro até 26/10, fechamento 30/09, e a variação.
 8. Brent: média de 3T26 e de outubro; IC-Br agro e metal em US$, média de 3T26 e do 3T25.
 9. Difusão de setembro contra setembro dos dez anos anteriores.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.stdout.reconfigure(encoding="utf-8")
A = Path(__file__).resolve().parent.parent / "A"


def rd(n):
    return pd.read_csv(A / f"{n}.csv.gz")


def comp(xs):
    return (np.prod([1 + x / 100 for x in xs]) - 1) * 100


# 1 ---------------------------------------------------------------------------------------------
ig = rd("inflc_indice_geral")
ig["date"] = pd.to_datetime(ig["date"])
ipca = ig[ig.indice == "IPCA"].set_index("date")["var_mensal"]
ip15 = ig[ig.indice == "IPCA15"].set_index("date")["var_mensal"] if "IPCA15" in set(ig.indice) else None
print("1. IPCA mensal")
for d in pd.date_range("2025-07-01", "2026-09-01", freq="MS"):
    print(f"   {d:%Y-%m}: {ipca.get(d)}")
saem = [ipca[pd.Timestamp(f"2025-{m:02d}-01")] for m in (10, 11, 12)]
print(f"   out-dez/2025 composto: {comp(saem):.2f}")

# 2 ---------------------------------------------------------------------------------------------
ag = rd("inflc_agregados")
ag["date"] = pd.to_datetime(ag["date"])
piv = ag.pivot_table(index="date", columns="name", values="value")
grp = {"IPCA": "ipca", "Serviços": "ipca_servicos", "Alimentação": "ipca_alimentacao",
       "Industriais": "ipca_industriais", "Monitorados": "ipca_administrado",
       "Serv. subj. (EX3 serv.)": "ipca_nucleo_ex03_servicos"}
print("\n2. Trimestre composto, 2016-2025 (média, mín, máx) e 2025, 2026")
for q in (1, 2, 3, 4):
    print(f"   {q}T")
    for lab, col in grp.items():
        vals = {}
        for y in range(2016, 2027):
            ms = [pd.Timestamp(f"{y}-{3*(q-1)+k:02d}-01") for k in (1, 2, 3)]
            s = piv[col].reindex(ms)
            if s.notna().all():
                vals[y] = comp(s.tolist())
        h = [vals[y] for y in range(2016, 2026) if y in vals]
        print(f"     {lab:24s} média {np.mean(h):5.2f} mín {min(h):5.2f} máx {max(h):5.2f}"
              f" | 2025 {vals.get(2025, float('nan')):5.2f} | 2026 {vals.get(2026, float('nan')):5.2f}")

# 3 ---------------------------------------------------------------------------------------------
fp = rd("expc_focus_periodo__ipca")
f26 = fp[(fp.data_referencia == 2026) & (fp.date == fp.date.max())]["mediana"].iloc[0]
ytd = comp([ipca[pd.Timestamp(f"2026-{m:02d}-01")] for m in range(1, 10)])
q4_focus = ((1 + f26 / 100) / (1 + ytd / 100) - 1) * 100
m12_set = comp([ipca[pd.Timestamp(d)] for d in pd.date_range("2025-10-01", "2026-09-01", freq="MS")])
print(f"\n3. Focus 2026 (mediana {fp.date.max()}): {f26:.2f}; jan-set/26 composto {ytd:.2f};"
      f" 4T26 implícito {q4_focus:.2f}; 12m set/26 recomposto {m12_set:.2f}")
qpc = [0.34, 0.32, 0.55]
q4_qpc = comp(qpc)
dez_qpc = ((1 + m12_set / 100) * (1 + q4_qpc / 100) / (1 + comp(saem) / 100) - 1) * 100
print(f"   QPC out-dez (0,34; 0,32; 0,55): 4T26 {q4_qpc:.2f}; 12m dez/26 {dez_qpc:.2f}")
print(f"   12m dez/26 implícito pela Focus 2026 = a própria Focus 2026: {f26:.2f}")
if ip15 is not None:
    o15 = ip15.get(pd.Timestamp("2026-10-01"))
    q4_15 = comp([o15, 0.32, 0.55])
    dez_15 = ((1 + m12_set / 100) * (1 + q4_15 / 100) / (1 + comp(saem) / 100) - 1) * 100
    print(f"   Com o IPCA-15 de out ({o15}) no lugar de out e QPC nov-dez: 4T26 {q4_15:.2f}; 12m dez/26 {dez_15:.2f}")
# o que o modelo põe no 4T26 (1,27) em 12m: conferência
dez_mod = ((1 + m12_set / 100) * (1 + 1.27 / 100) / (1 + comp(saem) / 100) - 1) * 100
print(f"   conferência: 4T26 de 1,27 dá 12m dez/26 {dez_mod:.2f}")
# Quanto o 4T26 precisa ser para o 12m ficar em 5,00 / 4,80 / 5,50
for alvo in (4.6, 4.8, 5.0, 5.5, 5.6):
    q = ((1 + alvo / 100) * (1 + comp(saem) / 100) / (1 + m12_set / 100) - 1) * 100
    print(f"   12m dez/26 = {alvo:.2f} exige 4T26 = {q:.2f}")

# 4 ---------------------------------------------------------------------------------------------
dc = rd("inflc_decomposicao")
dc["date"] = pd.to_datetime(dc["date"])
dim = rd("inflc_dim")
dim["subitem_codigo"] = dim["subitem_codigo"].astype(str)
dc["subitem_codigo"] = dc["subitem_codigo"].astype(str)
dc = dc.merge(dim[["subitem_codigo", "nome", "grupo", "subgrupo", "item", "subjacente"]],
              on="subitem_codigo", how="left")


def bc_grupo(r):
    if r.grupo == "Monitorados":
        return "Monitorados"
    return {"Alimentos": "Alimentação", "Bens Industriais": "Industriais",
            "Serviços": "Serviços"}.get(r.subgrupo, "?")


dc["bc"] = dc.apply(bc_grupo, axis=1)


def por_grupo(ind, d, chave="bc"):
    x = dc[(dc.indice == ind) & (dc.date == d)]
    g = x.groupby(chave).apply(lambda t: pd.Series({
        "var": (t.var_mensal * t.pesos).sum() / t.pesos.sum(),
        "peso": t.pesos.sum() * 100 / x.pesos.sum() * 100 / 100,
        "contrib": (t.var_mensal * t.pesos).sum() / x.pesos.sum()}))
    return g


print("\n4. IPCA-15 out/26 por grupo do BC (var. no mês, peso %, contribuição p.p.)")
print(por_grupo("IPCA15", pd.Timestamp("2026-10-01")).round(3).to_string())
x = dc[(dc.indice == "IPCA15") & (dc.date == pd.Timestamp("2026-10-01"))].copy()
x["c"] = x.var_mensal * x.pesos / x.pesos.sum()
print("   maiores para cima:")
print(x.nlargest(6, "c")[["nome", "bc", "var_mensal", "c"]].round(3).to_string(index=False))
print("   maiores para baixo:")
print(x.nsmallest(6, "c")[["nome", "bc", "var_mensal", "c"]].round(3).to_string(index=False))
print("   IPCA-15 set/26 por grupo (para comparar):")
print(por_grupo("IPCA15", pd.Timestamp("2026-09-01")).round(3).to_string())
# serviços subjacentes no IPCA-15
for d in ("2026-09-01", "2026-10-01"):
    t = x if d == "2026-10-01" else dc[(dc.indice == "IPCA15") & (dc.date == pd.Timestamp(d))]
    s = t[(t.bc == "Serviços") & (t.subjacente.notna()) & (t.subjacente.astype(str) != "")]
    print(f"   IPCA-15 {d[:7]} serviços com marca subjacente: {(s.var_mensal*s.pesos).sum()/s.pesos.sum():.2f}"
          f" ({len(s)} subitens)")

# 5 ---------------------------------------------------------------------------------------------
print("\n5. Alimentação por classe do BC (IPCA): set/26, acum. 3m, acum. 12m")
ali = dc[(dc.indice == "IPCA") & (dc.bc == "Alimentação")]
for cl in ("Alimentos in natura", "Alimentos semi-elaborados", "Alimentos industrializados"):
    t = ali[ali.item == cl]
    m = t.groupby("date").apply(lambda u: (u.var_mensal * u.pesos).sum() / u.pesos.sum())
    m = m.sort_index()
    print(f"   {cl:28s} set {m.iloc[-1]:6.2f} | 3m {comp(m.iloc[-3:].tolist()):6.2f}"
          f" | 12m {comp(m.iloc[-12:].tolist()):6.2f} | último {m.index[-1]:%Y-%m}")
    print("      mês a mês desde jan/26: " + "; ".join(f"{v:.2f}" for v in m.loc['2026-01-01':].tolist()))

# 6 ---------------------------------------------------------------------------------------------
di = rd("inflc_decomposicao_item")
di["date"] = pd.to_datetime(di["date"])
print("\n6. Mês a mês (IPCA), subitem")
for nome in ("Energia elétrica residencial", "Gasolina", "Óleo diesel", "Gás de botijão"):
    cod = dim[dim.nome == nome]["subitem_codigo"].tolist()
    t = dc[(dc.indice == "IPCA") & (dc.subitem_codigo.isin(cod))].groupby("date")["var_mensal"].mean()
    t = t.loc["2025-09-01":]
    print(f"   {nome}: " + "; ".join(f"{d:%y-%m} {v:.2f}" for d, v in t.items()))
    t15 = dc[(dc.indice == "IPCA15") & (dc.subitem_codigo.isin(cod))].groupby("date")["var_mensal"].mean()
    print(f"     IPCA-15 out/26: {t15.get(pd.Timestamp('2026-10-01'))}")

# 7 ---------------------------------------------------------------------------------------------
px = rd("cmb_ptax")
px["date"] = pd.to_datetime(px["date"])
pt = px[px.name == "ptax_venda"].set_index("date")["value"]
m3 = pt.loc["2026-07-01":"2026-09-30"].mean()
mo = pt.loc["2026-10-01":].mean()
m2 = pt.loc["2026-04-01":"2026-06-30"].mean()
print(f"\n7. PTAX média 2T26 {m2:.4f}; 3T26 {m3:.4f}; out/26 até {pt.index[-1]:%d/%m} {mo:.4f}"
      f" ({(mo/m3-1)*100:+.1f}% contra 3T26; 3T26 contra 2T26 {(m3/m2-1)*100:+.1f}%)")
print(f"   fechamento 30/09: {pt.loc[:'2026-09-30'].iloc[-1]:.4f}; último {pt.iloc[-1]:.4f}"
      f" ({(pt.iloc[-1]/pt.loc[:'2026-09-30'].iloc[-1]-1)*100:+.1f}%)")
print(f"   se a PTAX ficar em {pt.iloc[-1]:.4f} até 31/12, média 4T26 = "
      f"{(pt.loc['2026-10-01':].sum() + pt.iloc[-1]*(64 - len(pt.loc['2026-10-01':])))/64:.4f} (64 dias úteis aprox.)")

# 8 ---------------------------------------------------------------------------------------------
br = rd("comm_brent")
br["date"] = pd.to_datetime(br["date"])
b = br[br.name == "brent_usd"].set_index("date")["value"]
print(f"\n8. Brent média 2T26 {b.loc['2026-04':'2026-06'].mean():.1f}; 3T26 {b.loc['2026-07':'2026-09'].mean():.1f};"
      f" out/26 {b.loc['2026-10'].mean():.1f}; 3T25 {b.loc['2025-07':'2025-09'].mean():.1f}; máx 2026 {b.loc['2026'].max():.1f} em {b.loc['2026'].idxmax():%d/%m}")
cu = rd("comm_icbr_usd")
cu["date"] = pd.to_datetime(cu["date"])
cp = cu.pivot_table(index="date", columns="name", values="value")
for c in ("icbr_agropecuaria_usd", "icbr_metal_usd"):
    s = cp[c]
    print(f"   {c}: média 3T26 {s.loc['2026-07':'2026-09'].mean():.2f}; 2T26 {s.loc['2026-04':'2026-06'].mean():.2f};"
          f" 3T25 {s.loc['2025-07':'2025-09'].mean():.2f}; meses 2026: "
          + "; ".join(f"{v:.1f}" for v in s.loc['2026'].tolist()))
cr = rd("comm_icbr")
cr["date"] = pd.to_datetime(cr["date"])
crp = cr.pivot_table(index="date", columns="name", values="value")
s = crp["icbr_agropecuaria"]
print(f"   IC-Br agro em R$: média 3T26 {s.loc['2026-07':'2026-09'].mean():.2f}; 2T26 {s.loc['2026-04':'2026-06'].mean():.2f}"
      f" ({(s.loc['2026-07':'2026-09'].mean()/s.loc['2026-04':'2026-06'].mean()-1)*100:+.1f}%)")

# 9 ---------------------------------------------------------------------------------------------
dif = piv["ipca_indice_difusao"]
sets = [dif.get(pd.Timestamp(f"{y}-09-01")) for y in range(2016, 2026)]
print(f"\n9. Difusão set/26 {dif.get(pd.Timestamp('2026-09-01'))}; setembros 2016-2025 média {np.mean(sets):.1f},"
      f" mín {min(sets):.1f}, máx {max(sets):.1f}; abaixo do atual: {sum(v < dif.get(pd.Timestamp('2026-09-01')) for v in sets)} de 10")
