"""Expectativas: lista exógenas e coeficientes do Modelo Estrutural e roda o cenário padrão."""
from analytics.agent_system import modelo

sim = modelo.carregar("2026-10-27")
print(modelo.listar(sim))
res = modelo.rodar(sim)
print(modelo.texto(res))
