"""
PTC (Pesquisa Trimestral de Condicoes de Credito) -- pesquisa do BCB junto a
bancos comerciais sobre as condicoes de oferta e demanda de credito que eles
proprios percebem, equivalente brasileiro ao Senior Loan Officer Opinion
Survey do Fed / Bank Lending Survey do BCE. Trimestral, 4 segmentos (grandes
empresas, MPME, pessoa fisica consumo, pessoa fisica habitacional) x 2
direcoes (oferta/demanda) x 2 horizontes (observada = ultimos 3 meses,
esperada = proximos 3 meses) = 16 series. Valor e um indice de difusao
(saldo liquido de respostas, -1 a +1): positivo em oferta = aprovacao mais
frouxa; positivo em demanda = demanda maior. Nao e taxa de inadimplencia
nem probabilidade de default.

Series SGS coletadas (16 series), confirmadas via a planilha oficial do BCB
(https://www.bcb.gov.br/content/publicacoes/ptc/xls/Series_PTC.xlsx, aba
"Dicionario", coluna "Presente.no.SGS") e por chamada direta a api.bcb.gov.br
em 2026-08:
  ge_oferta_observada    21389 -- Grandes Empresas, oferta, ultimos 3 meses
  ge_oferta_esperada     21388 -- Grandes Empresas, oferta, proximos 3 meses
  ge_demanda_observada   21381 -- Grandes Empresas, demanda, ultimos 3 meses
  ge_demanda_esperada    21380 -- Grandes Empresas, demanda, proximos 3 meses
  mpme_oferta_observada  21391 -- MPME, oferta, ultimos 3 meses
  mpme_oferta_esperada   21390 -- MPME, oferta, proximos 3 meses
  mpme_demanda_observada 21383 -- MPME, demanda, ultimos 3 meses
  mpme_demanda_esperada  21382 -- MPME, demanda, proximos 3 meses
  pfc_oferta_observada   21393 -- PF Consumo, oferta, ultimos 3 meses
  pfc_oferta_esperada    21392 -- PF Consumo, oferta, proximos 3 meses
  pfc_demanda_observada  21385 -- PF Consumo, demanda, ultimos 3 meses
  pfc_demanda_esperada   21384 -- PF Consumo, demanda, proximos 3 meses
  pfh_oferta_observada   21395 -- PF Habitacional, oferta, ultimos 3 meses
  pfh_oferta_esperada    21394 -- PF Habitacional, oferta, proximos 3 meses
  pfh_demanda_observada  21387 -- PF Habitacional, demanda, ultimos 3 meses
  pfh_demanda_esperada   21386 -- PF Habitacional, demanda, proximos 3 meses

Todas desde 2011-04 (trimestral), atualizadas ao vivo -- confirmado com dado
mais recente em 2026-01 (planilha PTC datada de marco/2026, atualizada em
21/05/2026).

**Achado corrigindo um bug de dados existente (2026-08)**: os codigos 21397/
21399/21401/21403 ("PTCC - <segmento> - Aprov. Observadas"), usados antes em
cred_inadimplencia_pj.py (ptcc_grandes/ptcc_mpme) e em
analytics/painel_setores/painel_setores.py (todos os 4 segmentos), estao
CONGELADOS desde 2022-10 -- o BCB continuou publicando a pesquisa, só sob
outros codigos SGS (os 16 acima), nao descontinuou a serie como a
documentacao anterior concluiu. Confirmado ao vivo: 21397/21399/21401/21403
retornam 47 obs (ate 2022-10), os codigos corretos (21389/21391/21393/21395,
mesmo conceito -- oferta observada) retornam 60 obs (ate 2026-01), com a
mesma origem (2011-04) e valores plausiveis mas distintos ponto a ponto do
codigo antigo a partir de onde a serie antiga parou de ser atualizada mas
continuaria variando. ptcc_grandes/ptcc_mpme foram removidos de
cred_inadimplencia_pj.py (dados obsoletos apagados da tabela) e
painel_setores.py foi corrigido para os codigos certos -- ver
analytics/credit/fontes_dados.md para o detalhe completo.

Banco: macro_brasil.cred_ptc -- PRIMARY KEY (date, name)
"""

from connectors.bcb import BCB
from connectors.mysql import insert_data_into_database

_DATABASE = "macro_brasil"
_TABLE    = "cred_ptc"

_SERIES = {
    "ge_oferta_observada":    21389,
    "ge_oferta_esperada":     21388,
    "ge_demanda_observada":   21381,
    "ge_demanda_esperada":    21380,
    "mpme_oferta_observada":  21391,
    "mpme_oferta_esperada":   21390,
    "mpme_demanda_observada": 21383,
    "mpme_demanda_esperada":  21382,
    "pfc_oferta_observada":   21393,
    "pfc_oferta_esperada":    21392,
    "pfc_demanda_observada":  21385,
    "pfc_demanda_esperada":   21384,
    "pfh_oferta_observada":   21395,
    "pfh_oferta_esperada":    21394,
    "pfh_demanda_observada":  21387,
    "pfh_demanda_esperada":   21386,
}

_bcb = BCB()


def run(n_meses: int = 36, start: str | None = None, end: str | None = None) -> None:
    """Atualiza macro_brasil.cred_ptc.

    Args:
        n_meses: ultimos N meses (default 36). Ignorado se start/end fornecidos.
                 Serie trimestral -- ok pegar so 1-2 pontos novos em janela curta.
        start:   data inicial "DD/MM/YYYY", ou "all" para serie completa.
        end:     data final "DD/MM/YYYY". Default: hoje.
    """
    if start:
        df = _bcb.get_sgs(_SERIES, start=start, end=end)
    else:
        df = _bcb.get_sgs_ultimos(_SERIES, n=n_meses)

    insert_data_into_database(_DATABASE, _TABLE, df)
