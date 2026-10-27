"""in_modelo_listar: as exógenas e os coeficientes do Modelo Estrutural no ciclo 2026-10-02,
e o cenário padrão do simulador (sem caminho nenhum), para ver o ponto de partida."""
from analytics.agent_system import modelo

sim = modelo.carregar("2026-10-02")
print(modelo.listar(sim))
print("\n===== cenário padrão (sem caminhos) =====")
print(modelo.texto(modelo.rodar(sim)))
