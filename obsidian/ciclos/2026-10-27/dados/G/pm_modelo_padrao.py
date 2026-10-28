"""Roda o Modelo Estrutural no cenário padrão (nenhum caminho dado) para ver a partida (ciclo 2026-10-27)."""
from analytics.agent_system import modelo

sim = modelo.carregar("2026-10-27")
res = modelo.rodar(sim)
print(modelo.texto(res))
