"""G do câmbio, ciclo 2026-10-02: lista as exógenas e os coeficientes do Modelo Estrutural e
roda o cenário padrão (nenhum caminho, nenhum multiplicador)."""
from analytics.agent_system import modelo

sim = modelo.carregar("2026-10-02")
print(modelo.listar(sim))
res = modelo.rodar(sim)
print(modelo.texto(res))
