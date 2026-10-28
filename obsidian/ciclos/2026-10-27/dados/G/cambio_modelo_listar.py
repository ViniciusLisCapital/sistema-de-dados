"""G cambio: lista exógenas e coeficientes do Modelo Estrutural do ciclo, e a rodada padrão."""
from analytics.agent_system import modelo

sim = modelo.carregar("2026-10-27")
print(modelo.listar(sim))
res = modelo.rodar(sim)
print(modelo.texto(res))
