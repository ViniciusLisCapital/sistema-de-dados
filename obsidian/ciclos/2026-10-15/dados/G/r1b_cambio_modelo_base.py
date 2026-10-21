"""G r1b: cenário base do Modelo Estrutural — exógenas no último dado do corte, seguradas até 1T28."""
from analytics.agent_system import modelo

TRI = ["4T26", "1T27", "2T27", "3T27", "4T27", "1T28"]
plano = lambda v: {t: v for t in TRI}
BASE = {
    "fiscal": plano(112.19),    # cmb_risco_pais · 14/10
    "vol": plano(12.19),        # sem dado no F; padrão do simulador (2T26)
    "dxy_em": plano(129.7715),  # cmb_dollar_index_em · 09/10
    "sp500": plano(7720.99),    # cmb_equity_us · 15/10
    "icbr_usd": plano(205.70),  # comm_icbr_usd · set
    "ffr": plano(3.875),        # us_interest_rate, meta (ponto médio) · 15/10
    "infl_us": plano(0.91),     # padrão: média dos 4 últimos trimestres
}
if __name__ == "__main__":
    sim = modelo.carregar("2026-10-15")
    print(modelo.texto(modelo.rodar(sim, caminhos=BASE, mult={})))
