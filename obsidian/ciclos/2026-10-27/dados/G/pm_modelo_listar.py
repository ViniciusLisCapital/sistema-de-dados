"""Lista as exógenas, a convenção e os coeficientes do simulador do Modelo Estrutural (ciclo 2026-10-27)."""
from analytics.agent_system import modelo

sim = modelo.carregar("2026-10-27")
print(modelo.listar(sim))
