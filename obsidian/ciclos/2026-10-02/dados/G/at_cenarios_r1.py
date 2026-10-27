"""at_ · cenários da rodada 1 do agente de atividade: base (padrão do simulador), sensibilidade ao
caminho de rr_10a do fiscal (aguarda fiscal/PM), e os multiplicadores de (H) das caudas.
Imprime o hiato por cenário e a linha companheira (PIB interanual) pela conta mecânica."""
from analytics.agent_system import modelo
sim = modelo.carregar("2026-10-02")
TRI = ["4T26", "1T27", "2T27", "3T27", "4T27", "1T28"]
rr_fiscal = {"4T26": 7.55, "1T27": 7.60, "2T27": 7.55, "3T27": 7.50, "4T27": 7.45, "1T28": 7.40}
cen = {
    "base": dict(),
    "base_rr_fiscal": dict(caminhos={"rr_10a": rr_fiscal}),
    "up_h2x0.5": dict(mult={"H.h2": 0.5}),
    "up_h2x0.5_h1x0.95": dict(mult={"H.h2": 0.5, "H.h1": 0.95}),
    "dn_h2x1.5": dict(mult={"H.h2": 1.5}),
    "dn_h2x1.5_h1x1.05": dict(mult={"H.h2": 1.5, "H.h1": 1.05}),
}
# hiato observado (edição 2026-09) dos trimestres que servem de base de 4 trimestres antes
obs = {"4T25": 0.74, "1T26": 0.60, "2T26": 0.51, "3T26": 0.41}
POT = (2.66 + 2.60 + 2.53 + 2.19) / 4  # potencial implícito médio, F "O hiato do BC e o potencial implícito nele"
ant = {"4T26": "4T25", "1T27": "1T26", "2T27": "2T26", "3T27": "3T26", "4T27": "4T26", "1T28": "1T27"}
first = True
for nome, kw in cen.items():
    res = modelo.rodar(sim, **kw)
    if first or nome == "base_rr_fiscal":
        print(modelo.texto(res, TRI))
    first = False
    txt = modelo.texto(res, TRI)
    linha = [l for l in txt.splitlines() if l.startswith("| Hiato do produto")][0]
    sel = [l for l in txt.splitlines() if l.startswith("| Selic, média")][0]
    print(f"\n## {nome}\n{linha}\n{sel}")
    # central do hiato por trimestre
    vals = [c.strip().split(" ")[0].replace(",", ".") for c in linha.split("|")[2:-1]]
    h = dict(zip(["3T26"] + TRI, [float(x) for x in vals]))
    g = {**obs, **{t: h[t] for t in TRI}}
    pib = {t: POT + g[t] - g[ant[t]] for t in TRI}
    print("hiato:", {t: round(h[t], 2) for t in TRI})
    print("PIB yoy mecânico:", {t: round(v, 2) for t, v in pib.items()})
