"""G do fiscal, ciclo 2026-10-02: lista as exógenas e os coeficientes do Modelo Estrutural e roda
o cenário padrão do simulador (nenhum caminho, nenhum multiplicador)."""
from analytics.agent_system import modelo

sim = modelo.carregar("2026-10-02")
print(modelo.listar(sim))
print(modelo.texto(modelo.rodar(sim)))
