"""G · câmbio · ciclo 2026-10-15: lista as exógenas e os coeficientes do Modelo Estrutural
e roda o cenário padrão do simulador (todas as exógenas no último valor observado)."""
import sys

from analytics.agent_system import modelo

sys.stdout.reconfigure(encoding="utf-8")
TRI = ["4T26", "1T27", "2T27", "3T27", "4T27", "1T28"]

sim = modelo.carregar("2026-10-15")
print(modelo.listar(sim))
print()
for e in modelo.exogenas(sim):
    print(e["chave"], "|", e["nome"], "|", e["unidade"], "|", e["regiao"], "|", e["como_digitar"])
print()
print(modelo.texto(modelo.rodar(sim), TRI))
