"""
Helpers minimos para montar as arvores hierarquicas ({key, label, seriesKey, children})
consumidas pelas tabelas interativas dos relatorios — makeHierTab()/makeSimpleHierTab()/
makeImpulseTab() no lado JS.

Vive em analytics/report_structure/ desde 2026-08 (rename pais > area): antes estava em
analytics/credit/, mas analytics/fiscal_policy/ e analytics/labor_market/ ja importavam de
la, e um relatorio sob analytics/us/ nao pode depender de uma pasta de analytics/brasil/.
Nada aqui e especifico de pais ou de area — sao construtores de no puros. As transformacoes
(deflacao/STL/crescimento) NAO vieram junto: analytics/brasil/credit/transforms.py encadeia
IPCA e divide por um denominador de PIB do BCB, entao e especifico do Brasil.

Consumidores atuais: analytics/brasil/credit/{saldo,concessao,amplo,taxa,inadimplencia,
impulso,ptc}_tab.py, analytics/brasil/fiscal_policy/{gfsm,rtn,investimento}_tab.py,
analytics/brasil/labor_market/{pnad,caged}_tab.py.
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
