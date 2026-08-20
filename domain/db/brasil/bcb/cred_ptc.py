"""
PTC (Pesquisa Trimestral de Condicoes de Credito) -- pesquisa do BCB junto a
bancos comerciais sobre as condicoes de oferta e demanda de credito que eles
proprios percebem, equivalente brasileiro ao Senior Loan Officer Opinion
Survey do Fed / Bank Lending Survey do BCE. Trimestral, 4 segmentos (grandes
empresas, MPME, pessoa fisica consumo, pessoa fisica habitacional) x 2
direcoes (oferta/demanda) x 2 horizontes (observada = ultimos 3 meses,
esperada = proximos 3 meses) = 16 series.

Valor: cada respondente escolhe um de CINCO niveis, convertidos para inteiros de
-2 a +2, e o publicado e a MEDIA ARITMETICA SIMPLES (nao ponderada) das respostas
do segmento -- I = (1/N) * SOMA respostas, N = respondentes daquela questao naquele
trimestre. Escala: -2 consideravelmente mais restritivo / demanda consideravelmente
mais fraca; -1 moderadamente; 0 basicamente inalterado; +1 moderadamente mais
flexivel / mais forte; +2 consideravelmente. Positivo em oferta = aprovacao mais
frouxa; positivo em demanda = demanda maior. Nao e taxa de inadimplencia nem
probabilidade de default.

CORRECAO 2026-08: esta docstring dizia "indice de difusao (saldo liquido de
respostas, -1 a +1)" -- errado nas duas metades. Nao e saldo liquido (% que apertou
menos % que afrouxou, como o SLOOS do Fed), e media de niveis com peso 1 e 2; e o
intervalo e -2 a +2, nao -1 a +1 -- 19 dos 960 pontos da base passam de 1 em modulo,
extremos -1,21 (mpme_oferta_esperada, 2016-T1) e +1,57 (pfh_demanda_observada,
2020-T4). Fonte: BCB Trabalhos para Discussao 245, Annibal & Koyama (2011),
"Pesquisa Trimestral de Condicoes de Credito no Brasil"
(https://www.bcb.gov.br/pec/wps/port/TD245.pdf), secoes 2.3/2.6, mais a
"Introducao" de qualquer relatorio trimestral da PTC ("as avaliacoes sao convertidas
em valores entre -2 e 2 e sao apresentadas as medias nao ponderadas das respostas").
Cuidado: a nota de rodape desses relatorios cita "TD 254" -- erro de digitacao do
proprio BCB, o TD 254 e um paper de regulacao macroprudencial de outros autores.

O COMMENT da tabela no MySQL repetia o mesmo "-1 a +1" e foi corrigido em 2026-08
(ALTER TABLE): a tabela agora descreve chave/segmentos/horizontes e cita o TD 245, e a
escala -2..+2 com a definicao de media nao ponderada ficou no COMMENT da coluna `value`.

Painel pequeno: sendo media simples de N respostas, o indice so anda em multiplos
de 1/N. Participantes na rodada de junho/2024 (e N modal recuperado da propria
serie): grandes empresas 22, MPME 28, PF consumo 17, PF habitacional 7 (8 em 2011).
Logo o degrau minimo em PF Habitacional e ~0,14 -- uma variacao desse tamanho ali e
UM banco mudando de opiniao, nao mudanca de regime.

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
analytics/brasil/painel_setores/painel_setores.py (todos os 4 segmentos), estao
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
analytics/brasil/credit/fontes_dados.md para o detalhe completo.

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
