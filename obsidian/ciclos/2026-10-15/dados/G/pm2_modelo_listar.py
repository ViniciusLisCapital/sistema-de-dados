"""pm2: lista exógenas e coeficientes do simulador do ciclo, e roda o cenário padrão."""
from analytics.agent_system import modelo

sim = modelo.carregar("2026-10-15")
print(modelo.listar(sim))
res = modelo.rodar(sim, caminhos={}, mult={})
print(modelo.texto(res))
