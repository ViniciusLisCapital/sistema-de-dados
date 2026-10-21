"""G r1b: roda o simulador com todas as exógenas no padrão (referência para o cenário base)."""
from analytics.agent_system import modelo

sim = modelo.carregar("2026-10-15")
res = modelo.rodar(sim, caminhos={}, mult={})
print(modelo.texto(res))
