"""Expectativas, ciclo 2026-10-02, rodada 1: o Modelo Estrutural no cenário base (padrão do simulador:
nenhuma exógena tem caminho deste agente) e os temperos (i) na (E), e duas condições de cauda em
exógenas fora da tutela (só para medir; não vão ao JSON)."""
from analytics.agent_system import modelo

sim = modelo.carregar("2026-10-02")
T = ["4T26", "1T27", "2T27", "3T27", "4T27", "1T28"]
cen = {
    "base": dict(),
    "e1x1.15_e2x1.30 (âncora mais fraca)": dict(mult={"E.e1": 1.15, "E.e2": 1.30}),
    "e2x1.30": dict(mult={"E.e2": 1.30}),
    "e1x1.15": dict(mult={"E.e1": 1.15}),
    "e1x0.85_e2x0.75 (âncora mais forte)": dict(mult={"E.e1": 0.85, "E.e2": 0.75}),
    "agro +15% (condição, fora da tutela)": dict(caminhos={"icbr_agr_usd": {"4T26": 230.6}}),
    "CDS 200 (condição, fora da tutela)": dict(caminhos={"fiscal": {"4T26": 200}}),
    "agro +15% e e1x1.15_e2x1.30": dict(caminhos={"icbr_agr_usd": {"4T26": 230.6}}, mult={"E.e1": 1.15, "E.e2": 1.30}),
    "agro -10% e e1x0.85_e2x0.75": dict(caminhos={"icbr_agr_usd": {"4T26": 180.5}}, mult={"E.e1": 0.85, "E.e2": 0.75}),
}
for nome, kw in cen.items():
    res = modelo.rodar(sim, **kw)
    print("=" * 20, nome)
    if nome == "base":
        print(modelo.texto(res, T))
    e = res["endogenas"]
    for k in ("focus_12m", "ipca_12m", "selic", "ptax", "hiato"):
        lo, hi = e[k].get("lo"), e[k].get("hi")
        print(k.ljust(10), [round(v, 2) if v is not None else None for v in e[k]["central"][:6]],
              "| 90% pesos:", [f"{a:.2f}-{b:.2f}" for a, b in zip(lo[:6], hi[:6])] if lo else "")
    print("mult:", res["mult"])
    print("partida:", {k: res["partida"].get(k) for k in ("focus_12m", "ipca_12m", "selic", "ptax", "hiato")})
