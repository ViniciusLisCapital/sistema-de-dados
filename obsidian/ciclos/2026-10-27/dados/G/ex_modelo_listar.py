"""G externo: lista exógenas, convenção, último valor e coeficientes do Modelo Estrutural do ciclo."""
from analytics.agent_system import modelo
sim = modelo.carregar("2026-10-27")
print(modelo.listar(sim))
res = modelo.rodar(sim)
print(modelo.texto(res))
