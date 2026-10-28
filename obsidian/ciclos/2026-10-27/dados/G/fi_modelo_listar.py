"""fi: lista as exógenas e os coeficientes do Modelo Estrutural do ciclo (chaves, convenção, último valor)."""
from analytics.agent_system import modelo
sim = modelo.carregar("2026-10-27")
print(modelo.listar(sim))
