"""at_ · lista as exógenas e os coeficientes do Modelo Estrutural do ciclo, e roda o cenário padrão."""
from analytics.agent_system import modelo
sim = modelo.carregar("2026-10-02")
print(modelo.listar(sim))
res = modelo.rodar(sim)
print(modelo.texto(res))
