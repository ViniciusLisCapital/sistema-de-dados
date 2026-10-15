"""
O retrato de dados de um ciclo: A → F(A) (SISTEMA_AGENTES.md IV.iv).

    A     as tabelas da lista do agente (SISTEMA_AGENTES.md, seção V), lidas do banco UMA vez,
          no início do ciclo: obsidian/ciclos/<data>/dados/A/<tabela>.csv.gz
    F     as transformações fixas de cada tabela (último valor, variações, posição no histórico)
    F(A)  obsidian/ciclos/<data>/dados/F_<agente>.md, o que o agente lê
    G     conta que o F não faz: o agente escreve em dados/G/ e lê os arquivos de A

Uso:
    uv run python -m analytics.agent_system.dados cambio [--ciclo AAAA-MM-DD] [--refazer]
"""
