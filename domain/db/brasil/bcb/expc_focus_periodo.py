"""
Expectativas Focus — PERIODO DE REFERENCIA FIXO (BCB/Olinda).

E o Boletim Focus propriamente dito: endpoints `ExpectativaMercadoMensais`,
`ExpectativasMercadoTrimestrais` e `ExpectativasMercadoAnuais`, onde a pergunta nao e
"quanto nos proximos 12 meses" (isso e a `expc_focus`) mas "quanto EM 2027", "quanto
EM marco de 2027". Por isso a tabela tem DUAS datas independentes: `date` = quando foi
perguntado, `data_referencia` = sobre qual periodo. Um unico dia de pesquisa gera ~440
linhas — ~225 no mensal (9 indicadores x 25 meses a frente), ~72 no trimestral (9 x 8)
e ~140 no anual (26 indicadores x 5 anos, mais os detalhes da Balanca comercial).

As tres periodicidades ficam numa tabela so, e nao em tres, porque compartilham a chave
inteira — o que muda e apenas o formato de `data_referencia` ('03/2027', '1/2027',
'2027'), e `periodicidade` ja discrimina. Mesmo racional dos dois cortes de
`fisc_investimento` numa tabela unica.

O que esta tabela permite e a `expc_focus` nao permite: fixar `data_referencia` e varrer
`date` da a HISTORIA DA REVISAO — como o consenso sobre um periodo especifico se moveu.
O IPCA para o ano de 2026, por exemplo, tem 1.154 observacoes desde 2022-01-11, saindo
de 3,00% (ancorado ali por quatro anos) para 5,32% em 2026-07 e 5,02% em 2026-08-14. A
`expc_focus` guarda horizonte movel, que por construcao mistura periodos de referencia
a cada dia e nao permite fixar um.

  detalhe    So a Balanca comercial se subdivide (Exportacoes / Importacoes / Saldo);
             todos os outros indicadores vem com `IndicadorDetalhe` nulo, gravado aqui
             como string vazia porque coluna de PRIMARY KEY nao aceita NULL. Sem essa
             coluna as tres linhas de Balanca comercial colidiriam e duas se perderiam.
  ref_date   `data_referencia` normalizada para o primeiro dia do periodo, so para
             graficar/ordenar. Redundante de proposito: a coluna da chave preserva o
             formato publicado pelo BCB, esta e derivada.
  unidade    A API NAO expoe unidade nenhuma, e esta e a unica tabela do projeto onde
             quatro familias convivem (%, R$/US$, US$ bi, % do PIB) — sem esta coluna
             nenhum grafico consegue se formatar. Vem do mapa `_UNIDADES` abaixo, que
             levanta se aparecer indicador nao mapeado, em vez de gravar vazio.
             Atencao: '%' cobre tanto variacao (IPCA, PIB, IGP-M) quanto nivel (Selic
             % a.a., Taxa de desocupacao % da forca de trabalho) — quem grafica precisa
             saber qual e qual, a unidade sozinha nao diz.

`Câmbio` e **fim de periodo**, nao media do periodo. A API nao documenta isso e nao ha
`IndicadorDetalhe` para distinguir (existe um `Indicador = 'Câmbio'` so), entao foi
medido: comparando a ultima pesquisa de cada ano contra a PTAX de venda realizada
(`cmb_ptax`), a previsao fica mais perto do fechamento do ano em 9 dos 10 anos de
2016 a 2025 — 2020 e a excecao aparente e nao conta contra, porque naquele ano o
fechamento (5,1967) e a media (5,1578) praticamente coincidiram. Nao somar nem comparar
com media anual de PTAX sem converter.

`base_calculo`: so a base 0 (janela de 30 dias) e carregada aqui. Ao contrario da
`expc_focus` e da `expc_focus_copom`, onde as duas bases entram porque sao baratas e o
sinal "fresco vs. amplo" importa, nesta tabela dobrar 2,3 milhoes de linhas para uma
leitura secundaria nao se paga — o valor aqui esta no detalhe de periodo de referencia.
A coluna existe na chave, entao a base 1 e backfill de dados se um dia fizer falta.
`tipo_calculo` fica em 'geral' pelo mesmo motivo (Top5 ainda nao carregado).

Indicadores: so os que a pesquisa ainda publica. Duas reformulacoes cortaram series e
esta tabela deliberadamente ignora as mortas — a familia antiga de indices de precos
(IGP-DI, INPC, IPA-DI, IPA-M, IPC-Fipe, IPCA-15) encerrada em 2021-02-17, e "Producao
industrial" encerrada em 2021-09-13. Cuidado com uma assimetria real: PIB Agropecuaria/
Industria/Servicos sairam do endpoint TRIMESTRAL em 2021-09-13 mas seguem vivos no
ANUAL, por isso aparecem em `_ANUAIS` e nao em `_TRIMESTRAIS`.

Banco: macro_brasil.expc_focus_periodo
  PRIMARY KEY (date, periodicidade, indicador, detalhe, data_referencia,
               base_calculo, tipo_calculo)
"""

from __future__ import annotations

import logging

import pandas as pd

from domain.db.brasil.bcb import _focus_core as core

logger = logging.getLogger(__name__)

_TABLE = "expc_focus_periodo"

_COMPONENTES_IPCA = [
    "IPCA Livres",
    "IPCA Administrados",
    "IPCA Serviços",
    "IPCA Bens industrializados",
    "IPCA Alimentação no domicílio",
]

_MENSAIS = ["IPCA", "IGP-M", *_COMPONENTES_IPCA, "Câmbio", "Taxa de desocupação"]

_TRIMESTRAIS = ["IPCA", *_COMPONENTES_IPCA, "Câmbio", "PIB Total", "Taxa de desocupação"]

_ANUAIS = [
    "IPCA", "IGP-M", *_COMPONENTES_IPCA,
    "Câmbio", "Selic", "Taxa de desocupação",
    "PIB Total", "PIB Agropecuária", "PIB Indústria", "PIB Serviços",
    "PIB Despesa de consumo das famílias",
    "PIB Despesa de consumo da administração pública",
    "PIB Formação Bruta de Capital Fixo",
    "PIB Exportação de bens e serviços",
    "PIB Importação de bens e serviços",
    "Balança comercial", "Conta corrente", "Investimento direto no país",
    "Dívida bruta do governo geral", "Dívida líquida do setor público",
    "Resultado primário", "Resultado nominal",
]

# periodicidade -> (endpoint, indicadores vivos, primeira data do endpoint)
_FONTES = {
    "mensal":     ("ExpectativaMercadoMensais",      _MENSAIS,     "2000-01-01"),
    "trimestral": ("ExpectativasMercadoTrimestrais", _TRIMESTRAIS, "2001-11-01"),
    "anual":      ("ExpectativasMercadoAnuais",      _ANUAIS,      "1999-04-01"),
}

_START = min(inicio for _, _, inicio in _FONTES.values())

# A API nao devolve unidade — este mapa e a unica fonte dela.
_UNIDADES = {
    "R$/US$": ["Câmbio"],
    "US$ bi": ["Balança comercial", "Conta corrente", "Investimento direto no país"],
    "% do PIB": [
        "Dívida bruta do governo geral", "Dívida líquida do setor público",
        "Resultado primário", "Resultado nominal",
    ],
}
_UNIDADE_POR_INDICADOR = {
    ind: unidade for unidade, inds in _UNIDADES.items() for ind in inds
}

_COLUNAS = [
    "date", "periodicidade", "indicador", "detalhe", "data_referencia",
    "base_calculo", "tipo_calculo", "ref_date", "unidade",
    "media", "mediana", "desvio_padrao", "minimo", "maximo", "numero_respondentes",
]


def _unidade(indicador: str) -> str:
    """Unidade do indicador; '%' e o default (IPCA, IGP-M, PIB, Selic, desocupacao)."""
    return _UNIDADE_POR_INDICADOR.get(indicador, "%")


def _ref_date(periodicidade: str, ref: str) -> pd.Timestamp:
    """Normaliza `data_referencia` para o primeiro dia do periodo.

    'MM/YYYY' (mensal) -> YYYY-MM-01
    'Q/YYYY'  (trimestral) -> primeiro mes do trimestre
    'YYYY'    (anual) -> YYYY-01-01
    """
    if periodicidade == "anual":
        return pd.Timestamp(int(ref), 1, 1)
    esquerda, ano = ref.split("/")
    if periodicidade == "trimestral":
        return pd.Timestamp(int(ano), (int(esquerda) - 1) * 3 + 1, 1)
    return pd.Timestamp(int(ano), int(esquerda), 1)


def _transformar(periodicidade: str, vivos: list[str], vistos: set[str]):
    permitidos = set(vivos)

    def fn(raw: pd.DataFrame) -> pd.DataFrame:
        df = raw[raw["indicador"].isin(permitidos)].copy()
        if df.empty:
            return df
        vistos.update(df["indicador"].unique())

        df["periodicidade"] = periodicidade
        df["tipo_calculo"] = "geral"
        # `IndicadorDetalhe` nem existe como campo nos endpoints mensal/trimestral.
        df["detalhe"] = (
            df["indicador_detalhe"].fillna("") if "indicador_detalhe" in df.columns else ""
        )
        df["unidade"] = df["indicador"].map(_unidade)
        df["ref_date"] = [
            _ref_date(periodicidade, r) for r in df["data_referencia"]
        ]
        return df[_COLUNAS]

    return fn


def run(start: str | None = None, end: str | None = None, n_dias: int = 90) -> None:
    """Atualiza macro_brasil.expc_focus_periodo.

    A carga historica completa (start="all") sao **1,28 milhao de linhas** medidas
    (mensal 508.631 + anual 656.481 + trimestral 114.588) e ~950 requests: 11 minutos
    na primeira carga, 2026-08. Bem menos que a estimativa inicial de 2,3 M, porque os
    anos pre-2021 tem muito menos indicador vivo e horizonte de referencia mais curto
    (~12 meses a frente no mensal, contra 25 hoje) — nao extrapolar volume de um ano
    recente para o historico inteiro nesta fonte. A insercao e incremental por janela
    mensal, entao uma falha no meio preserva o que ja entrou e reexecutar retoma por
    upsert.

    Args:
        start:  data inicial ISO "YYYY-MM-DD". Default: ultimos `n_dias` dias.
                Use start="all" para a carga historica completa (desde 1999-04).
        end:    data final ISO. Default: hoje.
        n_dias: janela retroativa usada quando start=None (default 90).
    """
    hoje = pd.Timestamp.today().strftime("%Y-%m-%d")
    if start == "all":
        start, end = _START, end or hoje
    elif start is None:
        padrao_ini, padrao_fim = core.janela_default(n_dias)
        start, end = padrao_ini, end or padrao_fim
    else:
        end = end or hoje

    for periodicidade, (endpoint, vivos, inicio_fonte) in _FONTES.items():
        # Nao pedir janela anterior ao inicio do proprio endpoint: economiza dezenas
        # de requests garantidamente vazios na carga historica.
        ini = max(start, inicio_fonte)
        if ini > end:
            continue
        vistos: set[str] = set()
        n = core.carregar(
            endpoint, _TABLE, _transformar(periodicidade, vivos, vistos),
            start=ini, end=end, filtros_extras="baseCalculo eq 0",
        )
        logger.info("expc_focus_periodo %s: %d linhas, %d indicadores",
                    periodicidade, n, len(vistos))
        faltando = sorted(set(vivos) - vistos)
        if faltando:
            logger.warning("expc_focus_periodo %s: sem dados para %s",
                           periodicidade, faltando)
