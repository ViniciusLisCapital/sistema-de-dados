"""Expectativas, ciclo 2026-10-02: exógenas, coeficientes e chaves do Modelo Estrutural."""
from analytics.agent_system import modelo

sim = modelo.carregar("2026-10-02")
print(modelo.listar(sim))
