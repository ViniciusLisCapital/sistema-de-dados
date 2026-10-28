"""in_cenario_base: o cenário base do Modelo Estrutural, com todas as exógenas no padrão do
simulador (rodada 1: nenhum principal publicou caminho ainda)."""
import sys
from analytics.agent_system import modelo

sys.stdout.reconfigure(encoding="utf-8")
sim = modelo.carregar("2026-10-27")
res = modelo.rodar(sim, caminhos={})
print(modelo.texto(res))
