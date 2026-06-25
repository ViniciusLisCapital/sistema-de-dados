# -*- coding: utf-8 -*-
"""
Demonstracao do connector ibge2.

Roda com:
    .venv\Scripts\python tests\test_ibge2.py
"""

import pandas as pd
from connectors.ibge import IBGE

ibge = IBGE()

pd.set_option("display.width", 120)
pd.set_option("display.max_columns", 12)

# ---------------------------------------------------------------------------
# 1. Producao industrial (PIM) -- mensal
# ---------------------------------------------------------------------------

print("\n--- 1. Producao Industrial (ultimos 6 meses) ---")

df_pim = ibge.get(
    agregado=8888,
    variaveis=12606,                               # indice sem ajuste sazonal
    classificacoes={544: [129314, 129315, 129316]}, # geral, extrativa, transformacao
    periodos="last:6",
)



# print(df_pim[["date", "class_1_nome", "value"]])



m = ibge.metadados(1620)

print(f"  Pesquisa  : {m.pesquisa} \n")
print(f"  Frequencia: {m.frequencia} \n")
print(f"  Disponivel: {m.inicio} ate {m.fim} \n")
print(f"  Niveis    : {m.niveis_territoriais} \n")
print(f"  variaveis    : {m.variaveis} \n")
print(f"  classificacoes    : {m.classificacoes}")









# # ---------------------------------------------------------------------------
# # 2. PIB trimestral
# # ---------------------------------------------------------------------------

# print("\n--- 2. PIB (ultimos 4 trimestres) ---")

# df_pib = ibge.get(
#     agregado=1620,
#     variaveis=583,
#     classificacoes={11255: [90707, 90687, 90691]},  # PIB pm, Agropecuaria, Industria
#     periodos="last:4",
# )

# print(df_pib[["date", "class_1_nome", "value"]])

# # ---------------------------------------------------------------------------
# # 3. Varejo (PMC) -- dois indices ao mesmo tempo
# # ---------------------------------------------------------------------------

# print("\n--- 3. Varejo - Comercio Restrito (SA e NSA, ultimos 6 meses) ---")

# df_pmc = ibge.get(
#     agregado=8880,
#     variaveis=[7169, 7170],              # NSA e SA
#     classificacoes={11046: [56734]},     # total comercio restrito
#     periodos="last:6",
# )

# print(df_pmc[["date", "variavel_nome", "value"]])

# # ---------------------------------------------------------------------------
# # 4. Que variaveis existem num agregado? (descoberta)
# # ---------------------------------------------------------------------------

# print("\n--- 4. Variaveis disponiveis no agregado de servicos (8688) ---")

# print(ibge.listar_variaveis(8688)[["id", "nome"]])

# # ---------------------------------------------------------------------------
# # 5. Que categorias existem numa classificacao? (descoberta)
# # ---------------------------------------------------------------------------

# print("\n--- 5. Primeiras 10 categorias da classificacao 544 (PIM) ---")

# print(ibge.listar_classificacoes(8888)[["categoria_id", "categoria_nome"]].head(10))

# # ---------------------------------------------------------------------------
# # 6. Quando estao disponiveis os dados? (range da serie)
# # ---------------------------------------------------------------------------

# print("\n--- 6. Metadados do PIM ---")

# m = ibge.metadados(8888)
# print(f"  Pesquisa  : {m.pesquisa}")
# print(f"  Frequencia: {m.frequencia}")
# print(f"  Disponivel: {m.inicio} ate {m.fim}")
# print(f"  Niveis    : {m.niveis_territoriais}")
