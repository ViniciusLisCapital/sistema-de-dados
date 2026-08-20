"""
Estresse de credito PJ (pessoa juridica) + Selic — insumos para testar a tese
"juros altos levam empresas a quebrar". Nao existe uma serie publica direta de
falencia/recuperacao judicial no BCB/IBGE (ver analytics/credit_stress/CLAUDE.md
para as fontes que teriam esse dado, nenhuma via API aberta) — estas sao as
proxies de estresse de credito corporativo mais proximas disponiveis via SGS.

Series SGS coletadas (5 series):
  selic                 4189  — Selic acumulada no mes, anualizada base 252 (% a.a.), mensal,
                                desde 1986-08
  inadimplencia_pj      21083 — Inadimplencia da carteira de credito PJ (%), mensal, desde 2011-03
  atraso_pj             21004 — % carteira em atraso 15-90 dias, PJ, mensal, desde 2011-03
  taxa_juros_pj         20715 — Taxa media de juros das operacoes de credito, PJ (% a.a.), mensal,
                                desde 2011-03
  concessao_credito_pj  20632 — Concessoes de credito, PJ (R$ milhoes), mensal, desde 2011-03

**PTCC removida desta tabela (2026-08)**: ptcc_grandes/ptcc_mpme (codigos 21397/21399)
viviam aqui, mas os codigos estavam ERRADOS — nao descontinuados como a documentacao
anterior concluiu, so obsoletos: o BCB continuou publicando a Pesquisa Trimestral de
Condicoes de Credito sob outros codigos SGS (confirmado ao vivo contra a planilha oficial
https://www.bcb.gov.br/content/publicacoes/ptc/xls/Series_PTC.xlsx), e 21397/21399
simplesmente pararam de ser atualizados em 2022-10 enquanto a serie real seguia. Toda a
pesquisa (16 series — 4 segmentos x oferta/demanda x observada/esperada, nao so
"Aprovacao Observada" de 2 segmentos) foi migrada para uma tabela propria,
macro_brasil.cred_ptc (domain/db/brasil/bcb/cred_ptc.py) — ver esse arquivo para o
detalhe completo da correcao. As linhas antigas de ptcc_grandes/ptcc_mpme foram
apagadas desta tabela.

**Codigo da Selic corrigido de 4390 para 4189 (2026-08, achado antes de publicar)**: 4390
("Taxa de juros - Selic acumulada no mes") NAO e anualizada — retorna a taxa mensal (ex.:
1.22% em jul/2026), nao os ~14% a.a. que a Selic meta (codigo 432) tinha no mesmo periodo.
4189 e a variante "anualizada base 252" da mesma serie, e bate com a meta (432) dentro do
espalhamento efetiva-vs-meta esperado. Confirmado por chamada direta as 3 series (4390,
432, 4189) antes de gravar qualquer dado.

Codigos confirmados via chamada direta a api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo}
em 2026-08 (nao apenas por memoria/copia de analytics/brasil/painel_setores/painel_setores.py,
que ja usava os codigos de inadimplencia/atraso/taxa/concessao) — mesma pratica adotada
apos o bug de codigo SGS em cmb_balanco_pagmt.

Banco: macro_brasil.cred_inadimplencia_pj — PRIMARY KEY (date, name)
"""

from connectors.bcb import BCB
from connectors.mysql import insert_data_into_database

_DATABASE = "macro_brasil"
_TABLE    = "cred_inadimplencia_pj"

_SERIES = {
    "selic":                4189,
    "inadimplencia_pj":     21083,
    "atraso_pj":            21004,
    "taxa_juros_pj":        20715,
    "concessao_credito_pj": 20632,
}

_bcb = BCB()


def run(n_meses: int = 36, start: str | None = None, end: str | None = None) -> None:
    """Atualiza macro_brasil.cred_inadimplencia_pj.

    Args:
        n_meses: ultimos N meses (default 36). Ignorado se start/end fornecidos.
        start:   data inicial "DD/MM/YYYY", ou "all" para serie completa.
        end:     data final "DD/MM/YYYY". Default: hoje.
    """
    if start:
        df = _bcb.get_sgs(_SERIES, start=start, end=end)
    else:
        df = _bcb.get_sgs_ultimos(_SERIES, n=n_meses)

    insert_data_into_database(_DATABASE, _TABLE, df)
