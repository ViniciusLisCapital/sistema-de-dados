"""G r1b: lista as entradas, coeficientes e o padrão do simulador do Modelo Estrutural (ciclo 2026-10-15)."""
from analytics.agent_system import modelo

sim = modelo.carregar("2026-10-15")
print(modelo.listar(sim))
