"""
Cotacao diaria das moedas latino-americanas pares (MX/CL/CO/PE) contra o USD --
BIS, dataset WS_XRU (taxas bilaterais contra o dolar, FREQ=D). Nao alimenta
nenhum relatorio diretamente; e o insumo de volatilidade cambial para o metrico
carry/vol em analytics/brasil/exchange_rate/models/ppp_equilibrium.py
(relative_carry_vol), o mesmo papel que cmb_ptax ja cumpre para o lado
brasileiro.

Moeda local por USD -- mesma convencao de cotacao do PTAX (maior = moeda local
mais fraca). O BIS republica a taxa oficial de cada banco central (o FIX do
Banxico, o dolar observado do BCCh, a TRM do BanRep, a interbancaria do BCRP),
entao a cotacao e uma por dia e de fonte oficial, nao o ultimo preco de um
provedor de mercado.

Nao inclui AR -- mesma exclusao ja aplicada em cmb_real_rates.py (regime
idiossincratico, BIS parou de atualizar a taxa de politica monetaria em
2025-07; nao ha razao para tratar o cambio de forma diferente aqui).

## Por que o BIS e nao o Yahoo (trocado em 2026-10-07)

Ate 2026-10-07 a tabela vinha do Yahoo Finance (MXN=X, CLP=X, COP=X, PEN=X), e
tres das quatro series tinham defeito de fonte. O PEN alternava entre duas
cotacoes em dias seguidos (~3,33 e ~3,40) no historico inteiro, o que levava a
volatilidade realizada de 63 dias do sol a 28% a.a.; e havia ticks errados
isolados (CLP 5,00 em 2016-12-22, COP 33,4 em 2016-02-18, PEN 3,70 em
2018-06-20). Medido de 2004 em diante, dias com movimento acima de 1,5% que
desfaz no dia seguinte ("vai e volta"):

    moeda   Yahoo   BIS
    MXN       40     44   (os do BIS sao eventos reais: 05/08/2024, 06/11/2024)
    CLP      221     10
    COP      234     10
    PEN      618      0

Nos dias comuns, a diferenca mediana entre as duas fontes e 0,3-0,4% -- o
horario da cotacao (fixing do meio-dia contra fechamento), nao nivel diferente.
Os bancos centrais foram considerados um a um e descartados pelo custo, nao
pela qualidade: Banxico e BCCh exigem credencial, e seriam quatro connectors
para o que o BIS entrega numa chamada so, pelo connector que ja existia.

## O custo: o BIS republica em lote

O ultimo ponto fica ~1 a 2 semanas atras de hoje (medido em 2026-10-07: MX e CL
em 29/09, PE em 25/09, CO em 23/09) -- o mesmo atraso da curva POLICY de
`inter_interest_rate`, que vem do mesmo BIS. O consumidor e mensal (vol de 6
meses no fechamento do mes), entao o atraso so pesa no mes corrente. Ver
`max_age_days` em domain/release_calendar/calendar_2026.yaml.

## So dias de semana

A TRM colombiana e publicada para todo dia corrido, inclusive sabado e domingo
(vigora no fim de semana). Gravada assim, a serie teria ~365 pontos por ano com
dois retornos zero por semana, e a volatilidade anualizada por sqrt(252) sairia
subestimada. O run() descarta sabados e domingos das quatro moedas; os feriados
locais em dia de semana ficam (a TRM repete o valor anterior, retorno zero).

Banco: macro_international.cmb_fx_latam
Schema: PRIMARY KEY (date, country_code)
"""

from connectors.bis import BIS
from connectors.mysql import insert_data_into_database

_DATABASE = "macro_international"
_TABLE = "cmb_fx_latam"

_MOEDAS = {"MX": "MXN", "CL": "CLP", "CO": "COP", "PE": "PEN"}


def run(start: str = "2000-01-01") -> None:
    """Atualiza macro_international.cmb_fx_latam.

    Args:
        start: data inicial ISO "YYYY-MM-DD". Rebusca a serie inteira a cada
               passe (o upsert nao duplica), o que cura qualquer buraco historico
               e absorve revisao do BIS. As quatro series do BIS comecam antes
               de 2000 (MX 1954, CO 1967, CL 1982, PE 1990); o corte e a
               amostra que o modelo usa, nao a disponibilidade.
    """
    df = BIS().get_fx_usd(_MOEDAS, start=start)
    df = df[df["date"].dt.dayofweek < 5]          # TRM de fim de semana, ver docstring
    insert_data_into_database(_DATABASE, _TABLE, df[["date", "country_code", "value"]])
