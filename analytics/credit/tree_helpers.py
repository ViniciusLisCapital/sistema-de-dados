"""
Helpers minimos para montar as arvores hierarquicas (recurso -> segmento -> modalidade)
usadas pelas abas interativas de analytics/credit/ (Saldo, Concessao e futuras — ver
saldo_tab.py/concessao_tab.py para os usos concretos). Compartilhado para nao duplicar
a mesma estrutura de no em cada modulo de aba.
"""


def leaf(table: str, modalidade: str, label: str) -> dict:
    key = f"{table}__{modalidade}"
    return {"key": key, "label": label, "seriesKey": key}


def group(table: str, modalidade: str, label: str, children: list) -> dict:
    node = leaf(table, modalidade, label)
    node["children"] = children
    return node


def direct(series_key: str, label: str, children: list | None = None, key: str | None = None) -> dict:
    """Para nos cuja seriesKey ja e a chave final (ex: series de cred_credito_resumo,
    que nao precisam do prefixo `table__` usado por leaf()/group()). `key` (identidade
    da linha na arvore -- estado de expand/check) default para `series_key`, mas pode
    ser diferente quando o mesmo dado aparece em mais de uma posicao da arvore (ex:
    "Total Geral" e a raiz de "Por Tipo de Cliente" sao o mesmo saldo_total_total, mas
    precisam de linhas independentes na tabela)."""
    node = {"key": key or series_key, "label": label, "seriesKey": series_key}
    if children is not None:
        node["children"] = children
    return node
