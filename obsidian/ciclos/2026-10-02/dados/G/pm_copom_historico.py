"""pm: regularidades das decisões do Copom (pm_copom_reuniao, desde 1999), lidas como dado.

1. Distribuição dos passos por janela.
2. Ciclos de corte (sequência de reuniões com passo < 0, interrompida por um passo >= 0):
   início, fim, número de cortes, total, passos usados, e o que veio nas duas reuniões seguintes.
3. Quantas vezes um ciclo de corte parou depois de um corte de 25 p.b. (passo seguinte = 0) e
   quantas vezes foi revertido em alta em até 3 reuniões.
4. Passos de alta desde 2005: tamanhos.
"""
from pathlib import Path

import pandas as pd

A = Path(__file__).resolve().parent.parent / "A"
d = pd.read_csv(A / "pm_copom_reuniao.csv.gz", parse_dates=["date"]).sort_values("date")
d = d[d.alterada_fora_da_reuniao == 0].reset_index(drop=True)
s = d.variacao_bps

print("== 1. passos ==")
for ini in ["1999-01-01", "2005-01-01", "2016-01-01"]:
    x = d[d.date >= ini].variacao_bps
    print(ini, "n=", len(x)); print(x.value_counts().sort_index().to_string())

print("\n== 2. ciclos de corte ==")
ciclos, cur = [], None
for i, r in d.iterrows():
    if r.variacao_bps < 0:
        if cur is None:
            cur = {"i0": i, "passos": []}
        cur["passos"].append(int(r.variacao_bps)); cur["i1"] = i
    else:
        if cur is not None:
            ciclos.append(cur); cur = None
if cur is not None:
    ciclos.append(cur)
for c in ciclos:
    i0, i1 = c["i0"], c["i1"]
    dep = d.variacao_bps.iloc[i1 + 1:i1 + 4].tolist()
    print(d.date[i0].date(), "->", d.date[i1].date(), "| n", len(c["passos"]), "| total", sum(c["passos"]),
          "| Selic", d.selic_anterior[i0], "->", d.selic_decidida[i1], "| passos", c["passos"],
          "| 3 seguintes", dep)

print("\n== 3. paradas e reversões (desde 2005) ==")
c05 = [c for c in ciclos if d.date[c["i0"]] >= pd.Timestamp("2005-01-01") and c["i1"] + 1 < len(d)]
ult25 = [c for c in c05 if c["passos"][-1] == -25]
print("ciclos de corte encerrados desde 2005:", len(c05), "; terminados num corte de 25:", len(ult25))
rev = [c for c in c05 if any(v > 0 for v in d.variacao_bps.iloc[c["i1"] + 1:c["i1"] + 4])]
print("revertidos em alta nas 3 reuniões seguintes:", [(d.date[c["i0"]].date(), d.date[c["i1"]].date()) for c in rev])
# dentro de um ciclo: uma pausa (0) entre cortes
pausas = []
for i in range(1, len(d) - 1):
    if d.variacao_bps[i] == 0 and d.variacao_bps[i - 1] < 0 and d.variacao_bps[i + 1] < 0:
        pausas.append(d.date[i].date())
print("pausa de uma reunião entre dois cortes:", pausas)
# mudanças de ritmo dentro de ciclos de corte desde 2005
mud = []
for c in c05:
    p = c["passos"]
    for k in range(1, len(p)):
        if p[k] != p[k - 1]:
            mud.append((d.date[c["i0"] + k].date(), p[k - 1], p[k]))
print("mudanças de ritmo dentro de ciclos de corte desde 2005:", mud)

print("\n== 4. altas desde 2005 ==")
x = d[(d.date >= "2005-01-01") & (d.variacao_bps > 0)]
print(x.variacao_bps.value_counts().sort_index().to_string())
print("ciclo em curso:", d.tail(8)[["nro_reuniao", "date", "selic_decidida", "variacao_bps"]].to_string(index=False))
