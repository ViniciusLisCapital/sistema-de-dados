"""in_contas_texto: as somas e diferenças que o texto do report cita, a partir das saídas do
modelo (in_cenarios_r1.py) e das leituras do QPC (in_corte.py). Nada novo: só a aritmética."""
from analytics.agent_system import modelo

sim = modelo.carregar("2026-10-02")
T = ["4T26", "1T27", "2T27", "3T27", "4T27", "1T28"]
base = {"icbr_agr_usd": {t: 200.53 for t in T}, "icbr_met_usd": {t: 330.14 for t in T}}
up = {"icbr_agr_usd": {"4T26": 217.23, "1T27": 226.32}, "icbr_met_usd": {"4T26": 373.35, "1T27": 408.51}}
rb = modelo.rodar(sim, caminhos=base)
ru = modelo.rodar(sim, caminhos=up, mult={"I.IA.ia2": 1.4}, faixa=False)
tri = rb["trimestres"]
def v(res, k, t, campo="central"):
    return res["endogenas"][k][campo][tri.index(t)]
print("alim+monit 4T26:", round(v(rb, "ipca_12m_alimentacao", "4T26") + v(rb, "ipca_12m_monitorados", "4T26"), 2))
print("alim+monit 1T28:", round(v(rb, "ipca_12m_alimentacao", "1T28") + v(rb, "ipca_12m_monitorados", "1T28"), 2))
print("serviços 4T26 − 1T28:", round(v(rb, "ipca_12m_servicos", "4T26") - v(rb, "ipca_12m_servicos", "1T28"), 2))
print("Selic fim upside − base 1T28:", round(v(ru, "selic_fim", "1T28") - v(rb, "selic_fim", "1T28"), 2))
print("QPC dez/26 − set/26 implícitos: 4,94 − 4,30 =", round(4.94 - 4.30, 2))
for t in ["4T26", "1T28"]:
    lo, hi, c = v(rb, "ipca_12m", t, "lo"), v(rb, "ipca_12m", t, "hi"), v(rb, "ipca_12m", t)
    print(f"faixa do posterior {t}: {lo:.2f} a {hi:.2f}, meia-largura {(hi - lo) / 2:.2f}, central {c:.2f}")
