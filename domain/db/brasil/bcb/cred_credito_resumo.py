"""
Credito do sistema financeiro - resumo por recurso x segmento (BCB/SGS)

Series SGS coletadas (84 series: 72 = 8 metricas x 3 recursos x 3 segmentos, mais 12 do
corte "credito nao rotativo" da Tabela 14 -- ver abaixo):
  Metricas : saldo (R$ milhoes), concessao (R$ milhoes), concessao_sa (concessoes
             dessazonalizadas, R$ milhoes), taxa_juros (% a.a.), spread (p.p.), icc
             (Indicador de Custo do Credito, % a.a.), inadimplencia (>90d, %),
             pct_pib (% do PIB)
  Recursos : total, livre, direcionado, nao_rotativo, livre_nao_rotativo (os 2 ultimos
             so tem taxa_juros/spread -- ver abaixo)
  Segmentos: pj, pf, total

  **Corte "credito nao rotativo" (Tabela 14, 12 series novas)**: a mesma publicacao tem
  uma tabela de taxas/spread com um recorte adicional por tipo de credito -- "credito
  nao rotativo" (exclui cheque especial/cartao rotativo etc.) -- cruzado com recurso
  (total ou so livre; direcionado nao tem esse recorte, "rotativo" nao e um conceito
  direcionado) x segmento (pj/pf/total). Tabela 14 tambem repete taxa_juros/spread para
  total/livre/direcionado (== os codigos SGS ja existentes acima, confirmado idênticos)
  e expunha uma "taxa de captacao" (custo de funding do banco) para todo recurso x
  segmento -- mas **nenhuma dessas colunas de taxa de captacao tem codigo SGS proprio**
  (celula "-" na planilha-fonte, confirmado ao vivo, nao e erro de extracao) -- por isso
  nao ha `taxa_captacao_*` aqui, so o que a Tabela 14 realmente adiciona de novo
  (nao_rotativo/livre_nao_rotativo x taxa_juros/spread).

  **Unidade: saldo/concessao/concessao_sa vem da API SGS em R$ milhoes, nao R$
  bilhoes** -- a planilha-fonte do BCB (ver abaixo) exibe esses valores divididos
  por 1000 no cabecalho ("R$ bilhoes"), mas o codigo SGS cru retorna em milhoes.
  Confirmado ao vivo: codigo 20539 (saldo_total_total) em mar-2011 retorna
  1.759.678 no banco vs. 1.759,7 exibido na planilha -- razao exata de 1000,
  mesma convencao ja usada em cred_credito_amplo (tambem R$ milhoes).

  Fonte: BCB, "Tabelas de Estatisticas Monetarias e de Credito", Tabelas 3
  (recurso=total), 4 (recurso=livre), 5 (recurso=direcionado) e 14 (recurso=
  nao_rotativo/livre_nao_rotativo) -- cada tabela publica o codigo SGS de cada
  coluna no proprio arquivo, o que permite buscar tudo direto via API em vez de
  depender do reparse mensal de um xlsx (mesmo raciocinio de
  cred_credito_amplo.py/cred_inadimplencia_pj.py).

  A Tabela 2 (recurso: livre/direcionado/total, sem quebra PJ/PF) foi checada e
  achada totalmente redundante com as Tabelas 3+4+5 -- toda combinacao
  (recurso, segmento) que a Tabela 2 expoe (livre-total, direcionado-total,
  total-total) ja aparece com o MESMO codigo SGS em uma das outras tres (ex:
  "Saldos - Livre" da Tabela 2 e o codigo 20542, igual a "Saldos - Total" da
  Tabela 4, que e "Recursos Livres"). Por isso a Tabela 2 nao tem series
  proprias aqui.

Banco: macro_brasil.cred_credito_resumo -- PRIMARY KEY (date, name)
  name = "{metrica}_{recurso}_{segmento}", ex: "saldo_livre_pj",
  "taxa_juros_direcionado_pf", "inadimplencia_total_total".
"""

from connectors.bcb import BCB
from connectors.mysql import insert_data_into_database

_DATABASE = "macro_brasil"
_TABLE    = "cred_credito_resumo"

# recurso -> segmento -> metrica -> codigo SGS
_CODES = {
    "total": {
        "pj":    {"saldo": 20540, "concessao": 20632, "concessao_sa": 24440, "taxa_juros": 20715, "spread": 20784, "icc": 25352, "inadimplencia": 21083, "pct_pib": 20623},
        "pf":    {"saldo": 20541, "concessao": 20633, "concessao_sa": 24441, "taxa_juros": 20716, "spread": 20785, "icc": 25353, "inadimplencia": 21084, "pct_pib": 20624},
        "total": {"saldo": 20539, "concessao": 20631, "concessao_sa": 24439, "taxa_juros": 20714, "spread": 20783, "icc": 25351, "inadimplencia": 21082, "pct_pib": 20622},
    },
    "livre": {
        "pj":    {"saldo": 20543, "concessao": 20635, "concessao_sa": 24443, "taxa_juros": 20718, "spread": 20787, "icc": 25355, "inadimplencia": 21086, "pct_pib": 20626},
        "pf":    {"saldo": 20570, "concessao": 20662, "concessao_sa": 24444, "taxa_juros": 20740, "spread": 20809, "icc": 25356, "inadimplencia": 21112, "pct_pib": 20627},
        "total": {"saldo": 20542, "concessao": 20634, "concessao_sa": 24442, "taxa_juros": 20717, "spread": 20786, "icc": 25354, "inadimplencia": 21085, "pct_pib": 20625},
    },
    "direcionado": {
        "pj":    {"saldo": 20594, "concessao": 20686, "concessao_sa": 24446, "taxa_juros": 20757, "spread": 20826, "icc": 25358, "inadimplencia": 21133, "pct_pib": 20629},
        "pf":    {"saldo": 20606, "concessao": 20698, "concessao_sa": 24447, "taxa_juros": 20768, "spread": 20837, "icc": 25359, "inadimplencia": 21145, "pct_pib": 20630},
        "total": {"saldo": 20593, "concessao": 20685, "concessao_sa": 24445, "taxa_juros": 20756, "spread": 20825, "icc": 25357, "inadimplencia": 21132, "pct_pib": 20628},
    },
    # Tabela 14 -- so taxa_juros/spread existem para este corte (nao ha saldo/concessao/
    # icc/inadimplencia/pct_pib "credito nao rotativo" em nenhuma tabela da publicacao).
    "nao_rotativo": {
        "pj":    {"taxa_juros": 27624, "spread": 27632},
        "pf":    {"taxa_juros": 27625, "spread": 27633},
        "total": {"taxa_juros": 27623, "spread": 27631},
    },
    "livre_nao_rotativo": {
        "pj":    {"taxa_juros": 27627, "spread": 27635},
        "pf":    {"taxa_juros": 27628, "spread": 27636},
        "total": {"taxa_juros": 27626, "spread": 27634},
    },
}

_SERIES = {
    f"{metrica}_{recurso}_{segmento}": codigo
    for recurso, segmentos in _CODES.items()
    for segmento, metricas in segmentos.items()
    for metrica, codigo in metricas.items()
}

_bcb = BCB()


def run(n_meses: int = 24, start: str | None = None, end: str | None = None) -> None:
    """Atualiza macro_brasil.cred_credito_resumo.

    Args:
        n_meses: ultimos N meses (default 24). Ignorado se start/end fornecidos.
        start:   data inicial no formato "DD/MM/YYYY", ou "all" para serie completa.
        end:     data final no formato "DD/MM/YYYY". Default: hoje.
    """
    if start:
        df = _bcb.get_sgs(_SERIES, start=start, end=end)
    else:
        df = _bcb.get_sgs_ultimos(_SERIES, n=n_meses)

    insert_data_into_database(_DATABASE, _TABLE, df)
