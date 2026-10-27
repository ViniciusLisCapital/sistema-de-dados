"""pm, rodada 1: o Modelo Estrutural nos três cenários do report de política monetária.

Base: meta_12m 3,00 (tutela pm, nível 1) e rr_10a 7,51 segurado (o último pregão, 02/10, NTN-B 10a
em br_interest_rate; tutela pm nível 2, fiscal nível 1). As outras exógenas no padrão do simulador
(aguardam fiscal, externo e câmbio).
Upside (Selic acima): o choque do petróleo persiste e a percepção de risco piora; rr_10a volta a 8,05
(o nível de 30/06), CDS a 180 e dólar contra emergentes +4% (caminhos ilustrativos, fora da tutela
de pm: não vão para o JSON). Com tempero (i): R.t3 x 1,35 (dentro do intervalo de 90%).
Downside (Selic abaixo): o petróleo devolve, o ciclo global desacelera; rr_10a 7,20 (o mínimo de
2025-26 é 7,16), CDS 115, IC-Br agro e metal −8%. Tempero (i): R.t3 x 0,75 (dentro do intervalo).
Também roda a sensibilidade: base com rr_10a no padrão (7,84) para isolar o efeito da âncora.
"""
from analytics.agent_system import modelo

sim = modelo.carregar("2026-10-02")
ult = {e["chave"]: e["ultimo"] for e in modelo.exogenas(sim)}
print("últimos:", {k: ult[k] for k in ["rr_10a", "fiscal", "dxy_em", "icbr_agr_usd", "icbr_met_usd"]})
pct = lambda k, x: round(float(ult[k]["valor"] if isinstance(ult[k], dict) else ult[k]) * (1 + x / 100), 2)
Q = ["4T26", "1T27", "2T27", "3T27", "4T27", "1T28"]
flat = lambda v: {q: v for q in Q}

base_c = {"meta_12m": flat(3.00), "rr_10a": flat(7.51)}

up_c = {"meta_12m": flat(3.00),
        "rr_10a": {"4T26": 7.80, "1T27": 8.05},
        "fiscal": {"4T26": 160, "1T27": 180},
        "dxy_em": {"4T26": pct("dxy_em", 2), "1T27": pct("dxy_em", 4)}}

dn_c = {"meta_12m": flat(3.00),
        "rr_10a": {"4T26": 7.35, "1T27": 7.20},
        "fiscal": {"4T26": 120, "1T27": 115},
        "icbr_agr_usd": {"4T26": pct("icbr_agr_usd", -4), "1T27": pct("icbr_agr_usd", -8)},
        "icbr_met_usd": {"4T26": pct("icbr_met_usd", -4), "1T27": pct("icbr_met_usd", -8)}}
print("caminhos up:", up_c); print("caminhos down:", dn_c)

runs = {
    "padrao (rr_10a 7,84)": modelo.rodar(sim, caminhos={"meta_12m": flat(3.00)}),
    "BASE": modelo.rodar(sim, caminhos=base_c),
    "UPSIDE modelo": modelo.rodar(sim, caminhos=up_c),
    "UPSIDE tempero R.t3x1,35": modelo.rodar(sim, caminhos=up_c, mult={"R.t3": 1.35}),
    "DOWNSIDE modelo": modelo.rodar(sim, caminhos=dn_c),
    "DOWNSIDE tempero R.t3x0,75": modelo.rodar(sim, caminhos=dn_c, mult={"R.t3": 0.75}),
    "BASE com R.t3x1,35": modelo.rodar(sim, caminhos=base_c, mult={"R.t3": 1.35}),
}
for k, r in runs.items():
    print("\n########", k)
    print(modelo.texto(r, trimestres=Q))

print("\n\n######## RESUMO (central [faixa 90% do posterior]) ########")
for k, r in runs.items():
    print("\n--", k)
    ix = [r["trimestres"].index(q) for q in Q]
    for v in ["selic_fim", "selic", "ipca_12m", "focus_12m", "hiato", "ptax"]:
        e = r["endogenas"][v]
        cel = []
        for i in ix:
            c, lo, hi = e["central"][i], e["lo"][i], e["hi"][i]
            cel.append("—" if c is None else f"{c:.2f} [{lo:.2f};{hi:.2f}]")
        print(f"{v:10s}", " | ".join(cel))

print("\n######## posição dos multiplicadores no posterior ########")
for k in ["UPSIDE tempero R.t3x1,35", "DOWNSIDE tempero R.t3x0,75"]:
    print(k, runs[k]["mult"])
print("\n######## entradas usadas na base (4T26..1T28) ########")
b = runs["BASE"]; ix = [b["trimestres"].index(q) for q in Q]
for kx, e in b["entradas"].items():
    print(kx, [round(e["caminho"][i], 2) for i in ix], e["fonte"] if isinstance(e["fonte"], str) else "")

print("\n######## 3.3: modelo -> com tempero (Selic de fechamento) ########")
OLEO_UP = {"4T26": 0.25, "1T27": 0.50, "2T27": 0.50, "3T27": 0.50, "4T27": 0.50, "1T28": 0.25}  # tempero (ii)
for nome, mod, tmp, extra in [("upside", "UPSIDE modelo", "UPSIDE tempero R.t3x1,35", OLEO_UP),
                              ("downside", "DOWNSIDE modelo", "DOWNSIDE tempero R.t3x0,75", {})]:
    a, t = runs[mod], runs[tmp]
    for q in Q:
        i = a["trimestres"].index(q)
        m0 = a["endogenas"]["selic_fim"]["central"][i]
        m1 = t["endogenas"]["selic_fim"]["central"][i] + extra.get(q, 0)
        print(nome, q, f"modelo {m0:.2f} -> com tempero {m1:.2f}")
