"""pm2: os cenários da etapa 1 (caminhos das exógenas) e os temperos (i) da etapa 2,
rodados no simulador do Modelo Estrutural do ciclo. Sem reestimar: os pesos são os do retrato.

Caminhos em nível, na unidade do cartão do simulador (modelo.listar). Um valor vale do
trimestre dado em diante, até o próximo.
"""
from analytics.agent_system import modelo

sim = modelo.carregar("2026-10-15")

TRIS = ["4T26", "1T27", "2T27", "3T27", "4T27", "1T28"]

# Base: os preços de 15/10 segurados. NTN-B 10a: média do 4T26 se ficar em 6,869 até 31/12 = 6,887
# (pm2_leituras); depois 6,87 (a curva real é plana entre 2 e 10 anos, 6,80 a 6,87).
# CDS: 112 (14/10). Fed Funds: 3,88 (meta de set/26) no 4T26; 4,13 a partir do 1T27 (o T-bill de
# 3 meses a 4,28 está 0,41 p.p. acima do ponto médio da meta). Dólar contra emergentes: 129,77 (09/10).
BASE = {
    "rr_10a": {"4T26": 6.89, "1T27": 6.87},
    "fiscal": {"4T26": 112},
    "ffr": {"4T26": 3.88, "1T27": 4.13},
    "dxy_em": {"4T26": 129.77},
}
# Worst: o salto de 05/10 se desfaz e o prêmio volta a subir; o Fed sobe mais.
WORST = {
    "rr_10a": {"4T26": 7.35, "1T27": 7.84, "2T27": 8.00},
    "fiscal": {"4T26": 131, "1T27": 150},
    "ffr": {"4T26": 3.88, "1T27": 4.38},
    "dxy_em": {"4T26": 131.0, "1T27": 133.7},
}
# Best: a compressão continua (o mercado precifica mais consolidação fiscal); Fed parado.
BEST = {
    "rr_10a": {"4T26": 6.75, "1T27": 6.40, "2T27": 6.20},
    "fiscal": {"4T26": 105, "1T27": 95},
    "ffr": {"4T26": 3.88},
    "dxy_em": {"4T26": 129.77},
}

VARS = ["selic_fim", "selic", "ipca_12m", "focus_12m", "hiato", "ptax"]


def linha(res, var):
    """Extrai a central por trimestre de um resultado (lê o dicionário do resultado)."""
    return res


def mostrar(nome, res):
    print(f"\n######## {nome}")
    print(modelo.texto(res))


rodadas = {
    "padrão do simulador (sem caminho)": modelo.rodar(sim, caminhos={}),
    "BASE": modelo.rodar(sim, caminhos=BASE),
    "WORST (modelo)": modelo.rodar(sim, caminhos=WORST),
    "BEST (modelo)": modelo.rodar(sim, caminhos=BEST),
    # temperos (i)
    "WORST + R.t3 x1,3 (reação ao desvio das expectativas mais forte)": modelo.rodar(sim, caminhos=WORST, mult={"R.t3": 1.3}),
    "BASE + R.t3 x1,3": modelo.rodar(sim, caminhos=BASE, mult={"R.t3": 1.3}),
    "BEST + H.h2 x1,5 (aperto pesa mais no hiato)": modelo.rodar(sim, caminhos=BEST, mult={"H.h2": 1.5}),
    "BASE + H.h2 x1,5": modelo.rodar(sim, caminhos=BASE, mult={"H.h2": 1.5}),
    "BEST + R.t1 x0,95 (menos inércia no hiato entre a Selic e a âncora)": modelo.rodar(sim, caminhos=BEST, mult={"R.t1": 0.95}),
    "BASE + R.t1 x1,05 (mais inércia)": modelo.rodar(sim, caminhos=BASE, mult={"R.t1": 1.05}),
    # sensibilidades de uma exógena por vez, a partir da base
    "SENS: base com rr_10a no padrão (7,84)": modelo.rodar(sim, caminhos={k: v for k, v in BASE.items() if k != "rr_10a"}),
    "SENS: base com Fed Funds 3,88 parado": modelo.rodar(sim, caminhos={**BASE, "ffr": {"4T26": 3.88}}),
    "SENS: base com CDS 131 (fechamento do 3T26)": modelo.rodar(sim, caminhos={**BASE, "fiscal": {"4T26": 131}}),
}
for nome, res in rodadas.items():
    mostrar(nome, res)

# posição dos multiplicadores no posterior
print("\n######## coeficientes usados nos temperos")
for c in modelo.coeficientes(sim):
    if c.get("chave") in ("R.t3", "H.h2", "R.t1", "R.t2") or c.get("key") in ("R.t3", "H.h2"):
        print(c)
