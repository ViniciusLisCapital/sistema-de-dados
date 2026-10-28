"""Atividade, etapa 1 e 3.3: cenários do Modelo Estrutural para o hiato, e o que cada tempero faz.

- NTN-B 10 anos (br_interest_rate, NTNBJS 120M): último, médias de 3T26, set e out/2026;
- base: o padrão do simulador (rodada 1: rr_10a e meta_12m ainda sem o caminho do principal);
- sensibilidades: rr_10a no nível de 26/10 (8,05) e CDS em 137 (o dado de 26/10), H.h2 x0,5 e x1,5, H.h1 x1,05;
- aperto da (H) por trimestre no base: Selic média - rr_10a - meta;
- temperos (ii) sobre o modelo, por trimestre:
    partida: o hiato do 3T26 abaixo do nowcast do BC por d, propagado pela inércia h1 (d * h1^k);
    resíduo: um choque positivo de e por trimestre na (H), acumulado pela inércia (o viés recente).
"""
import pandas as pd
from pathlib import Path
from analytics.agent_system import modelo

A = Path(__file__).resolve().parents[1] / "A"
br = pd.read_csv(A / "br_interest_rate.csv.gz", parse_dates=["date"])
nb = br[(br.curve == "NTNBJS") & (br.tenor == "120M")].set_index("date")["value"].sort_index()
print("NTN-B 10a: ultimo %.2f (%s); 23/10 %.2f; media 3T26 %.2f; set %.2f; out ate o corte %.2f" % (
    nb.iloc[-1], nb.index[-1].date(), nb.loc["2026-10-23"], nb.loc["2026-07":"2026-09"].mean(),
    nb.loc["2026-09"].mean(), nb.loc["2026-10"].mean()))

sim = modelo.carregar("2026-10-27")
Q = ["4T26", "1T27", "2T27", "3T27", "4T27", "1T28"]
cen = {
    "base": dict(),
    "rr_10a 8,05": dict(caminhos={"rr_10a": {"4T26": 8.05}}),
    "rr_10a 8,05 + CDS 137": dict(caminhos={"rr_10a": {"4T26": 8.05}, "fiscal": {"4T26": 137}}),
    "h2 x0,5": dict(mult={"H.h2": 0.5}),
    "h2 x1,5": dict(mult={"H.h2": 1.5}),
    "h1 x1,05": dict(mult={"H.h1": 1.05}),
    "upside: h2 x0,5 + rr_10a 8,05": dict(caminhos={"rr_10a": {"4T26": 8.05}}, mult={"H.h2": 0.5}),
    "downside: h2 x1,5": dict(mult={"H.h2": 1.5}),
}
R = {n: modelo.rodar(sim, **kw) for n, kw in cen.items()}


def linha(nome, var, casas=2, faixa=False):
    e = R[nome]["endogenas"][var]
    tr = R[nome]["trimestres"]
    vals = [e["central"][tr.index(q)] for q in Q]
    s = " | ".join(f"{v:.{casas}f}" for v in vals)
    if faixa:
        s += "   faixa90: " + " | ".join(f"[{e['lo'][tr.index(q)]:.2f};{e['hi'][tr.index(q)]:.2f}]" for q in Q)
    return f"{nome:34s} {var:9s} {s}"


print("\n" + " " * 44 + " | ".join(Q))
for n in R:
    print(linha(n, "hiato", faixa=(n == "base")))
for n in ["base", "rr_10a 8,05", "rr_10a 8,05 + CDS 137", "h2 x0,5", "h2 x1,5"]:
    print(linha(n, "selic"))
for n in ["base", "rr_10a 8,05 + CDS 137", "h2 x0,5", "h2 x1,5"]:
    print(linha(n, "ipca_12m"))
    print(linha(n, "ptax", casas=3))

# aperto da (H) no base: selic media - rr_10a - meta (rr_10a e meta no padrao: 7,84 e 3,00)
b = R["base"]
ent = b["entradas"]
print("\nentradas do base (rr_10a, meta_12m):", {k: ent[k] for k in ("rr_10a", "meta_12m")} if isinstance(ent.get("rr_10a"), (int, float)) else "")
sel = b["endogenas"]["selic"]["central"]; tr = b["trimestres"]
print("aperto no 3T26 (observado): %.2f" % (b["partida"]["selic"] - 7.84 - 3.00))
print("aperto no base:", " | ".join(f"{q} {sel[tr.index(q)] - 7.84 - 3.00:.2f}" for q in Q))

# temperos (ii) sobre o modelo
h1 = 0.874689157807679
base = [b["endogenas"]["hiato"]["central"][tr.index(q)] for q in Q]
print("\nTempero partida (hiato do 3T26 abaixo do nowcast de 0,41), efeito por trimestre:")
for d in (-0.15, -0.30, -0.45, -0.80):
    ef = [d * h1 ** (k + 1) for k in range(6)]
    print(f"  d={d:+.2f}: efeito " + " | ".join(f"{x:+.2f}" for x in ef) + "   hiato: " + " | ".join(f"{bb + x:.2f}" for bb, x in zip(base, ef)))
print("Tempero residuo (choque e por trimestre na H, desde o 4T26, acumulado pela inercia):")
for e in (0.10, 0.15, 0.25):
    acc = 0.0; ef = []
    for k in range(6):
        acc = h1 * acc + e
        ef.append(acc)
    print(f"  e={e:+.2f}: efeito " + " | ".join(f"{x:+.2f}" for x in ef) + "   hiato: " + " | ".join(f"{bb + x:.2f}" for bb, x in zip(base, ef)))

# contas citadas no report
s_b = R["base"]["endogenas"]["selic"]["central"]; s_r = R["rr_10a 8,05"]["endogenas"]["selic"]["central"]
print("\nSelic media 4T26: base %.2f, rr_10a 8,05 %.2f, diferenca %.2f" % (s_b[0], s_r[0], s_r[0] - s_b[0]))
print("meio ponto de aperto na (H): 0,5 x h2 = %.4f p.p. de hiato por trimestre" % (0.5 * -0.07091757284446645))
acc = 0.0; ccd = []
for k in range(6):
    acc = h1 * acc - 0.035; ccd.append(acc)
print("condicoes financeiras -0,035/tri acumulado:", " | ".join(f"{x:+.3f}" for x in ccd))
