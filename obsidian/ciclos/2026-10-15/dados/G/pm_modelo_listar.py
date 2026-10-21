"""G pm: lista entradas, coeficientes e padrão do simulador do Modelo Estrutural, e roda o padrão (ciclo 2026-10-15)."""
from analytics.agent_system import modelo

sim = modelo.carregar("2026-10-15")
print(modelo.listar(sim))
res = modelo.rodar(sim)
print(modelo.texto(res))
