"""
Gerador do Panorama Fiscal em HTML.

Cinco abas, reconstruidas uma a uma depois da limpeza de 2026-08 (o usuario pediu
para apagar Visao Geral/Divida Publica/Resultado Fiscal/Receita e Despesa e refazer
o dashboard aba por aba, mesmo padrao ja usado em analytics/brasil/credit/ -- ver
analytics/brasil/fiscal_policy/CLAUDE.md): Receitas e Despesas (GFSM + RTN), Divida Liquida
(DLSP, fatores condicionantes), Investimento (GND x funcao / GND x natureza, 2026-08),
Impulso Fiscal (IEG + resultado primario) e Apendice. Visao Geral e Resultado Fiscal
seguem apagadas; `fisc_divida` continua alimentada por jobs/update_db.py sem ser lida
aqui (ver Pending no CLAUDE.md desta pasta).

Le de macro_brasil: fisc_efgg (GFSM + IEG), fisc_rtn (RTN), fisc_dlsp_fatores (DLSP),
fisc_investimento (Investimento), fisc_nfsp (impulso via resultado primario),
atv_pib_valores_correntes/atv_pib_mensal (denominadores de %PIB), inflc_agregados
(deflator IPCA) e atv_pib_taxas (comparacao com o PIB oficial) -- e injeta no template
report.html, gerando um arquivo HTML autocontido. Mesmo padrao /*REPORT_DATA*/ de
analytics/brasil/economic_activity/ e analytics/brasil/inflation/ -- sem Jinja2, via
analytics.report_structure.builder.render_report().

Uso:
    uv run python analytics/brasil/fiscal_policy/generate_report.py
    uv run python -c "from analytics.brasil.fiscal_policy.generate_report import run; run()"
"""

from datetime import datetime
from pathlib import Path

import pandas as pd

from analytics.brasil.fiscal_policy import dlsp_tab, gfsm_tab, investimento_tab, rtn_tab
from analytics.brasil.fiscal_policy import transforms as tf
from analytics.report_structure.builder import render_report
from connectors.mysql import MySQLDataRequester

_HERE = Path(__file__).parent
_TEMPLATE = _HERE / "report.html"

_DATABASE = "macro_brasil"


def _load_table(table: str) -> pd.DataFrame:
    req = MySQLDataRequester(_DATABASE, table)
    req.connect()
    df = req.request_data()
    req.close_connection()
    df["date"] = pd.to_datetime(df["date"])
    df["value"] = pd.to_numeric(df["value"])
    return df


def _load_flat(table: str) -> dict:
    df = _load_table(table)
    result = {}
    for name, grp in df.groupby("name"):
        grp = grp.sort_values("date")
        result[name] = {
            "dates":  grp["date"].dt.strftime("%Y-%m-%d").tolist(),
            "values": [None if pd.isna(v) else round(float(v), 4) for v in grp["value"]],
        }
    return result


def _load_pib_4t() -> dict:
    """PIB nominal acumulado em 4 trimestres (TTM), mesmo denominador usado por
    fisc_nfsp/IEG neste relatorio (ver _load_ieg()'s pib_4t e
    analytics/brasil/fiscal_policy/transforms.py's compute_pct_pib_ttm()). Recalculado aqui
    em vez de reusar o pib_4t interno de _load_ieg() para nao acoplar as duas
    funcoes -- o calculo (rolling(4).sum() sobre ~65 trimestres) e trivial. Denominador
    do %PIB no nivel Acumulado da GFSM -- ver _load_pib_pm_raw() para o nivel
    Trimestral (mesmo periodo, sem acumular).
    """
    pib = _load_table("atv_pib_valores_correntes")
    pib_pm = pib[pib["name"] == "pib_pm"].set_index("date")["value"].sort_index()
    pib_4t = pib_pm.rolling(4).sum()
    return {d.strftime("%Y-%m-%d"): (None if pd.isna(v) else float(v)) for d, v in pib_4t.items()}


def _load_pib_pm_raw() -> dict:
    """PIB nominal trimestral SEM acumular (valor do proprio trimestre) -- mesma serie
    que _load_pib_4t() rola em 4 trimestres, aqui bruta. Denominador do %PIB "mesmo
    periodo" no nivel Trimestral da GFSM (2026-08, adicionado na reorganizacao dos 3
    eixos de metrica -- ver analytics/brasil/fiscal_policy/transforms.py's docstring).
    """
    pib = _load_table("atv_pib_valores_correntes")
    pib_pm = pib[pib["name"] == "pib_pm"].set_index("date")["value"].sort_index()
    return {d.strftime("%Y-%m-%d"): (None if pd.isna(v) else float(v)) for d, v in pib_pm.items()}


def _load_gfsm_tab_data() -> dict:
    """Aba Receitas e Despesas (GFSM) -- ver analytics/brasil/fiscal_policy/gfsm_tab.py."""
    efgg = _load_flat("fisc_efgg")
    raw = {k: efgg[k] for k in gfsm_tab.DB_NAMES}
    ipca = _load_flat("inflc_agregados")["ipca"]
    gdp_ttm = _load_pib_4t()
    gdp_same_period = _load_pib_pm_raw()
    return gfsm_tab.build(raw, ipca, gdp_ttm, gdp_same_period)


def _load_rtn_tab_data() -> dict:
    """2a tabela+grafico da aba Receitas e Despesas -- metodologia RTN (Governo
    Central, caixa, rubrica orcamentaria), ao lado da GFSM acima -- ver
    analytics/brasil/fiscal_policy/rtn_tab.py e reference/rtn_vs_efgg.md."""
    rtn = _load_flat("fisc_rtn")
    raw = {k: rtn[k] for k in rtn_tab.CODES}
    ipca = _load_flat("inflc_agregados")["ipca"]
    pib_mensal_all = _load_flat("atv_pib_mensal")
    pib_acum_12m = pib_mensal_all["pib_acum_12m"]
    pib_mensal = pib_mensal_all["pib_mensal"]
    return rtn_tab.build(raw, ipca, pib_acum_12m, pib_mensal)


def _load_investimento_tab_data() -> dict:
    """Aba Investimento -- investimento do Governo Federal por GND, nos dois cortes de
    fisc_investimento (funcao e natureza), ver analytics/brasil/fiscal_policy/investimento_tab.py.

    `fisc_investimento` tem PK (date, corte, item), nao (date, name) como as demais
    tabelas fiscais, entao _load_flat() (que agrupa por `name`) nao serve -- agrupa
    aqui pelas duas colunas de dimensao, como _load_dlsp_tab_data() faz para
    (fator, item).
    """
    df = _load_table("fisc_investimento")
    raw: dict = {}
    for (corte, item), grp in df.groupby(["corte", "item"]):
        grp = grp.sort_values("date")
        raw.setdefault(corte, {})[item] = {
            "dates":  grp["date"].dt.strftime("%Y-%m-%d").tolist(),
            "values": [None if pd.isna(v) else round(float(v), 4) for v in grp["value"]],
        }
    ipca = _load_flat("inflc_agregados")["ipca"]
    pib_mensal_all = _load_flat("atv_pib_mensal")
    return investimento_tab.build(
        raw, ipca, pib_mensal_all["pib_mensal"], pib_mensal_all["pib_acum_12m"])


def _load_dlsp_tab_data() -> dict:
    """Aba Divida Liquida (DLSP) -- 9 tabelas, uma por fator condicionante, ver
    analytics/brasil/fiscal_policy/dlsp_tab.py.

    Le fisc_dlsp_fatores num unico SELECT e pivota para {fator: {item: [valores]}} na
    grade de datas compartilhada pelas 9 abas da planilha do BCB (uma grade so --
    validado na ingestao, ver domain/db/brasil/bcb/fisc_dlsp_fatores.py). Denominador
    do %PIB: atv_pib_mensal.pib_acum_12m (SGS 4382), o mesmo que reproduz
    fisc_divida.dlsp_pct_pib a +/-0,005pp.
    """
    df = _load_table("fisc_dlsp_fatores")
    dates = sorted(df["date"].unique())
    date_strs = [pd.Timestamp(d).strftime("%Y-%m-%d") for d in dates]

    wide = df.pivot_table(index="date", columns=["fator", "item"], values="value", aggfunc="first").reindex(dates)
    raw: dict = {}
    for fator, item in wide.columns:
        raw.setdefault(fator, {})[item] = [None if pd.isna(v) else float(v) for v in wide[(fator, item)]]

    pib_acum_12m = _load_flat("atv_pib_mensal")["pib_acum_12m"]
    gdp_ttm = dict(zip(pib_acum_12m["dates"], pib_acum_12m["values"]))

    return dlsp_tab.build(raw, date_strs, gdp_ttm)


# Impulso via credito a instituicoes financeiras oficiais (2026-08, a pedido do
# usuario). Item de fisc_dlsp_fatores + os 2 subcomponentes que o BCB publica --
# confirmado ao vivo que o pai e a soma exata dos dois filhos, em `estoque` e em
# `primario` (desvio 0,0).
_CREDITO_OFICIAL_PAI = "interna__gov_federal__creditos_inst_fin_oficiais"
_CREDITO_OFICIAL_TREE = [
    (_CREDITO_OFICIAL_PAI, "Créditos concedidos a Inst. Financ. Oficiais", [
        (f"{_CREDITO_OFICIAL_PAI}__creditos_bndes", "Créditos junto ao BNDES"),
        (f"{_CREDITO_OFICIAL_PAI}__instrumentos_hibridos", "Instrumentos híbridos de capital e dívida"),
    ]),
]


def _load_impulso_credito_oficial() -> dict:
    """Impulso fiscal via credito a instituicoes financeiras oficiais -- metrica nova
    (2026-08, a pedido explicito do usuario), complementar ao IEG e ao impulso via
    resultado primario, NAO integrada a nenhum dos dois.

    O que mede: o canal PARAFISCAL. Quando o Tesouro empresta a uma instituicao
    financeira oficial (historicamente o BNDES, em volume), isso e uma operacao
    financeira -- aumenta um ativo do Governo Federal e nao aparece como despesa no
    resultado primario "acima da linha". Mas e expansionista: coloca funding
    subsidiado na economia. O fator `primario` desse item em fisc_dlsp_fatores isola
    exatamente esse fluxo.

    Construcao (escopo definido pelo usuario -- "summing up the 12m the Primario
    factor only, in level and % GDP"):
      1. fator `primario` do item e dos 2 subcomponentes (SOMENTE `primario`; o item
         tambem tem fluxo de `juros` e de `ajuste_met_interno`, deliberadamente fora);
      2. soma movel de 12 meses;
      3. **sinal invertido** -- na convencao da planilha, emprestar torna o item mais
         negativo (o ativo cresce), e o usuario explicitou que emprestar e impulso e
         portanto deve aparecer POSITIVO. Isso alinha esta metrica a convencao
         "positivo = expansionista" que o IEG e o impulso via resultado primario ja
         usam nesta aba;
      4. "% do PIB" divide pelo PIB acumulado em 12 meses (atv_pib_mensal.pib_acum_12m),
         mesmo denominador e mesma convencao TTM/TTM do resto do relatorio.

    Sanidade confirmada ao vivo contra a historia conhecida do canal BNDES: pico de
    +4,65% do PIB em 2010-05 (capitalizacao pos-crise), reversao a -2,65% em 2018-08
    (pre-pagamentos do BNDES ao Tesouro), +0,67% em 2026-06.
    """
    df = _load_table("fisc_dlsp_fatores")
    itens = [_CREDITO_OFICIAL_PAI] + [k for _p, _l, kids in _CREDITO_OFICIAL_TREE for k, _kl in kids]
    prim = (
        df[(df["fator"] == "primario") & (df["item"].isin(itens))]
        .pivot(index="date", columns="item", values="value")
        .sort_index()
    )

    pib_acum_12m = _load_flat("atv_pib_mensal")["pib_acum_12m"]
    gdp = dict(zip(pib_acum_12m["dates"], pib_acum_12m["values"]))

    dates = [d.strftime("%Y-%m-%d") for d in prim.index]
    series = {}
    for item in itens:
        # -1 x soma movel de 12m: positivo = emprestando = impulso (ver docstring).
        acum = (-prim[item].rolling(12).sum())
        level = [None if pd.isna(v) else round(float(v), 1) for v in acum]
        series[item] = {
            "level": level,
            "pctpib": [
                None if (v is None or gdp.get(d) in (None, 0)) else round(v / gdp[d] * 100, 4)
                for d, v in zip(dates, level)
            ],
        }

    tree = [
        {"key": pai, "label": label, "seriesKey": pai,
         "children": [{"key": k, "label": kl, "seriesKey": k} for k, kl in kids]}
        for pai, label, kids in _CREDITO_OFICIAL_TREE
    ]
    return {"dates": dates, "series": series, "tree": tree, "anchor": _CREDITO_OFICIAL_PAI}


_IMPULSO_NFSP_ESFERAS = {
    "governo_federal": "resultado_primario_governo_federal_pct_pib_12m",
    "banco_central": "resultado_primario_banco_central_pct_pib_12m",
    "estados": "resultado_primario_estados_pct_pib_12m",
    "municipios": "resultado_primario_municipios_pct_pib_12m",
    "empresas_estatais": "resultado_primario_empresas_estatais_pct_pib_12m",
}

# Ordem/rotulo de exibicao das 5 esferas na tabela hierarquica (2026-08 -- ver
# makeImpulsoHierTab() em report.html). Lista plana, sem segundo nivel: a decomposicao
# aqui e SO por esfera ("The same for 'Impulso via Resultado Primario por Esfera', but only
# with the spheres"), ao contrario do IEG (Esfera > Categoria de despesa).
_IMPULSO_NFSP_TREE_LABELS = [
    ("governo_federal", "Governo Federal (sem BC)"),
    ("estados", "Estados"),
    ("municipios", "Municípios"),
    ("empresas_estatais", "Empresas Estatais"),
    ("banco_central", "Banco Central"),
]

# Contraparte NAO acumulada (fluxo mensal bruto, R$ mi) de cada serie acima -- ver
# docstring de domain/db/brasil/bcb/fisc_nfsp.py. "total" nao tem entrada em
# _IMPULSO_NFSP_ESFERAS (nao e uma esfera) por isso fica de fora deste dict e e
# tratado a parte em _load_fiscal_impulse_nfsp().
_IMPULSO_NFSP_FLUXO_TOTAL = "resultado_primario_fluxo_mensal"
_IMPULSO_NFSP_FLUXO_ESFERAS = {
    "governo_federal": "resultado_primario_governo_federal_fluxo_mensal",
    "banco_central": "resultado_primario_banco_central_fluxo_mensal",
    "estados": "resultado_primario_estados_fluxo_mensal",
    "municipios": "resultado_primario_municipios_fluxo_mensal",
    "empresas_estatais": "resultado_primario_empresas_estatais_fluxo_mensal",
}


def _impulso_quarter_via_stl(flow: dict, gdp_by_date: dict, target_dates: list[str]) -> list:
    """Leitura T/T geniunamente dessazonalizada (STL) do impulso via resultado
    primario (2026-08, substitui o atalho anterior -- pp_diff(3) sobre o proprio
    acumulado em 12m, sem rodar STL -- a pedido explicito do usuario: "We have the
    monthly primary result data from BCB... why not make the seasonal
    adjustments?").

    `flow` = {dates, values}, fluxo mensal bruto (R$ mi, NAO acumulado, ja com o
    sinal invertido na ingestao -- ver fisc_nfsp.py) de resultado_primario_fluxo_mensal
    ou uma de suas 5 contrapartes por esfera. Passos:
      (1) soma movel de 3 meses do fluxo bruto E do PIB mensal (gdp_by_date,
          atv_pib_mensal.pib_mensal), ambos via rolling_sum(window=3) -- o fluxo
          mensal bruto e extremamente ruidoso mes a mes (pagamentos pontuais de
          precatorios, calendario de arrecadacao etc. concentram valores enormes
          num unico mes -- testado ao vivo: sem essa suavizacao, o resultado final
          oscilava +-7pp de um mes para o outro, uma ordem de grandeza maior que o
          acum12m, claramente nao comparavel); a janela de 3 meses (nao 12, que
          voltaria a ser o proprio acumulado que este calculo tenta evitar) da a
          mesma suavizacao de "um trimestre" que a serie trimestral nativa do IEG
          ja tem por construcao.
      (2) razao das duas somas moveis x100 = % do PIB "trimestral" (rolante, um
          ponto por mes, ao contrario do trimestre calendario nao sobreposto de
          compute_variants_quarterly_step());
      (3) STL (period=12 -- a serie ainda tem cadencia MENSAL, so trimestral no
          sentido de somar 3 meses moveis) sobre essa serie -- dessazonaliza de
          verdade (ao contrario do acumulado em 12m, que so cancela sazonalidade
          por ja somar um ciclo anual inteiro, sem isolar o componente sazonal em
          si; um rolante de so 3 meses NAO cancela sazonalidade por construcao,
          por isso o STL aqui e necessario, ao contrario do acum12m acima);
      (4) pp_diff(3) sobre a serie dessazonalizada = variacao trimestral genuina
          (trimestre terminado em t contra o trimestre terminado 3 meses antes);
      (5) sinal invertido (como `impulso` acima) para bater com a convencao
          "positivo = expansionista".

    Resultado alinhado (por data, nao por posicao) a `target_dates` -- o grid de
    resultado_primario_pct_pib_12m, para o campo "quarter" conviver no mesmo array
    `dates` que "acum12m" no payload final (mesma tecnica ja usada para realinhar as
    5 series de esfera acumuladas, ver loop abaixo).
    """
    dates, values = flow["dates"], flow["values"]
    flow_3m = tf.rolling_sum(values, window=3)
    gdp_3m = tf.rolling_sum([gdp_by_date.get(d) for d in dates], window=3)
    pctgdp = [None if (f is None or g is None) else f / g * 100 for f, g in zip(flow_3m, gdp_3m)]
    # STL so sobre a janela densa (mesma regra de _stl_on_valid_window() no lado do IEG --
    # ver Gotchas em analytics/brasil/fiscal_policy/CLAUDE.md): pctgdp comeca com 2 meses None
    # (janela movel de 3 ainda incompleta), e stl_seasonal_adjust() faz
    # interpolate(limit_direction="both") antes do fit -- alimentar esses None de volta
    # backfillaria um valor artificial no inicio da amostra.
    sa_dense = _stl_on_valid_window(
        pd.Series(pctgdp, index=pd.to_datetime(dates)), period=12,
    )
    sa_by_date = {d.strftime("%Y-%m-%d"): v for d, v in sa_dense.items()}
    sa = [sa_by_date.get(d) for d in dates]
    delta = tf.pp_diff(sa, 3)
    quarter_by_date = dict(zip(dates, (None if v is None else -v for v in delta)))
    return [quarter_by_date.get(d) for d in target_dates]


def _load_fiscal_impulse_nfsp() -> dict:
    """Tabela nova na aba Impulso Fiscal (2026-08, a pedido explicito do usuario --
    "adicione tambem a medida de impulso fiscal (delta resultado primario)... coloque
    uma tabela nova, pois depois vamos consolidar"), complementar ao IEG acima, NAO
    integrada a ele ainda -- fonte, escopo e convencao de sinal diferentes:

    - Fonte: fisc_nfsp (BCB SGS, "abaixo da linha"), nao fisc_efgg/fisc_rtn -- resultado
      primario do SETOR PUBLICO CONSOLIDADO (Governo Central + Estados/Municipios +
      Empresas Estatais + Banco Central), ja em % do PIB acumulado em 12 meses (mesma
      convencao TTM/TTM do resto deste relatorio, sem precisar recalcular). Escopo mais
      proximo do Governo Geral do IEG (mais amplo que o Governo Central da aba RTN) --
      ver domain/db/brasil/bcb/fisc_nfsp.py para a inversao de sinal ja aplicada na
      ingestao (positivo = superavit, convencao "resultado", nao "necessidade").
    - "acum12m" = variacao interanual (12 meses, p.p., NAO pct_change -- ver
      transforms.pp_diff()) do resultado primario acumulado (% do PIB) -- diferenca
      simples de pontos percentuais, mesma unidade que o IEG, sinal invertido
      (`impulso = -delta`) para bater com a convencao do IEG (positivo =
      expansionista): uma PIORA do resultado primario (superavit caindo/deficit
      subindo) e fiscalmente expansionista, entao vira impulso POSITIVO.
    - "quarter" (2026-08, reescrito -- ver _impulso_quarter_via_stl()): antes um
      atalho pp_diff(3) sobre o proprio acumulado em 12m (sem rodar STL); agora um
      STL genuino (period=12) sobre o fluxo MENSAL bruto (fisc_nfsp's 6 series
      *_fluxo_mensal, novas nesta rodada -- ver docstring de
      domain/db/brasil/bcb/fisc_nfsp.py), dividido pelo PIB do mesmo mes
      (atv_pib_mensal.pib_mensal). Motivado por feedback direto do usuario apos ver
      o "Visao Combinada" da rodada anterior: "the metrics [aren't] talking to each
      other" -- o atalho T/T-sobre-acumulado nao e uma variacao trimestral genuina
      (e uma medida de aceleracao/desaceleracao do proprio acumulado movel),
      inconsistente com a leitura T/T do IEG (tambem reescrita nesta rodada, ver
      _ieg_contrib_for_esfera()) e do PIB (indicador 'qoq' do IBGE, ja
      dessazonalizado). Verificado ao vivo (2026-08) que o fluxo mensal, acumulado
      em 12m e dividido pelo PIB acumulado, reconcilia com resultado_primario_pct_pib_12m
      a menos de 0,01pp -- mesma serie, so ainda nao acumulada.

    Deliberadamente uma tabela/secao a parte, nao mesclada ao IEG (fonte e escopo
    diferentes, sinal so comparavel apos a inversao acima) -- consolidacao entre os
    dois fica para uma proxima rodada, ver Pending em analytics/brasil/fiscal_policy/CLAUDE.md.

    Decomposicao por esfera (2026-08, a pedido explicito do usuario -- "quero
    decompor [o impulso] por esfera: Governo Central, Estados e Municipios - nao
    Banco Central"): fisc_nfsp ja tem, para o mesmo mes, 5 series que desagregam o
    resultado primario consolidado por esfera -- Governo Federal (SEM Banco
    Central), Banco Central (sozinho), Estados, Municipios, Empresas Estatais (ver
    _IMPULSO_NFSP_ESFERAS/_IMPULSO_NFSP_FLUXO_ESFERAS e o docstring de
    domain/db/brasil/bcb/fisc_nfsp.py). "acum12m" aplica o MESMO calculo (pp_diff de
    12 meses, sinal invertido) a cada uma -- como pp_diff() e uma operacao linear
    (diferenca), e as 5 series somam o total a cada mes (confirmado ao vivo, ver
    fisc_nfsp.py), a soma dos 5 "acum12m por esfera" reproduz o "acum12m" total a
    cada mes, a menos do mesmo arredondamento de +/-0,01pp por serie do SGS --
    garantia EXATA, nao aproximada.

    "quarter" por esfera roda o MESMO STL da funcao acima, um fit independente por
    esfera (fluxo mensal daquela esfera / PIB do mesmo mes). Como STL (com
    robust=True) nao e uma operacao linear, a soma das 5 esferas "quarter" NAO
    reconcilia mais exatamente com o "quarter" total (ao contrario de "acum12m",
    acima) -- um residuo pequeno e esperado (ver Apendice/CLAUDE.md), o preco de
    trocar o atalho linear por uma dessazonalizacao de verdade em cada corte.
    """
    nfsp = _load_flat("fisc_nfsp")
    pib_mensal = _load_flat("atv_pib_mensal")["pib_mensal"]
    gdp_by_date = dict(zip(pib_mensal["dates"], pib_mensal["values"]))

    s = nfsp["resultado_primario_pct_pib_12m"]
    delta_yoy = tf.pp_diff(s["values"], 12)
    impulso = [None if v is None else -v for v in delta_yoy]
    impulso_quarter = _impulso_quarter_via_stl(nfsp[_IMPULSO_NFSP_FLUXO_TOTAL], gdp_by_date, s["dates"])

    # As series de esfera comecam antes de resultado_primario_pct_pib_12m (1998/1999
    # vs. 2002-11 -- ver domain/db/brasil/bcb/fisc_nfsp.py) -- pp_diff() e posicional
    # (pandas .diff(periods=12) sobre o array recebido), entao cada serie precisa ser
    # realinhada ao MESMO grid de datas de `s` (por data, nao por posicao bruta)
    # antes do diff, ou o lag de 12 meses ficaria deslocado.
    esfera = {}
    for key, col in _IMPULSO_NFSP_ESFERAS.items():
        es = nfsp.get(col, {"dates": [], "values": []})
        by_date = dict(zip(es["dates"], es["values"]))
        aligned = [by_date.get(d) for d in s["dates"]]
        es_delta_12m = tf.pp_diff(aligned, 12)
        acum12m = [None if v is None else -v for v in es_delta_12m]

        flow = nfsp[_IMPULSO_NFSP_FLUXO_ESFERAS[key]]
        quarter = _impulso_quarter_via_stl(flow, gdp_by_date, s["dates"])

        esfera[key] = {"acum12m": acum12m, "quarter": quarter}

    return {
        "dates": s["dates"],
        "impulso": impulso,
        "impulso_quarter": impulso_quarter,
        "esfera": esfera,
        "tree": [{"key": k, "label": label, "seriesKey": k} for k, label in _IMPULSO_NFSP_TREE_LABELS],
    }


_IEG_MULTIPLICADORES = {
    "folha": 1.32,
    "transferencias": 1.46,
    "investimentos": 1.66,
    "outras": 0.64,
}

_PIB_DEMANDA_NAMES = [
    "pib_pm", "consumo_familias", "consumo_adm_publica", "fbcf", "exportacao", "importacao",
]


def _load_pib_yoy() -> dict:
    """PIB (total) + os 5 componentes da otica da demanda, taxas OFICIAIS do IBGE --
    atv_pib_taxas (mesma tabela que analytics/brasil/economic_activity usa para o mesmo fim, ver Data
    map desse relatorio). Usado para comparar contra o IEG/impulso via resultado primario na aba
    Impulso Fiscal -- nao entra no calculo de nenhum dos dois.

    Tres taxas por componente -- todas ja sao taxas REAIS (o IBGE publica sobre o indice de
    VOLUME, nao sobre valores correntes), o que atende o pedido do usuario de o PIB entrar no
    grafico combinado pela taxa real:
      - acum_4t: acumulado nos ultimos 4 trimestres contra os 4 anteriores (indicador 6563).
        Par do "4T/12m Acumulado" no grafico combinado (2026-08, substituiu 'yoy' nesse papel a
        pedido do usuario) -- e a unica das tres com a MESMA forma que as outras duas metricas
        do grafico (o IEG compara TTM contra TTM 4 trimestres antes; o impulso PB compara o
        acumulado em 12m contra o de 12 meses antes), enquanto 'yoy' e uma comparacao ponto a
        ponto de um unico trimestre.
      - yoy: variacao interanual (indicador 6561), sem ajuste sazonal por construcao. Nao e mais
        usada pelo grafico combinado; mantida no payload por ser a leitura mais citada do PIB.
      - qoq: variacao T/T imediatamente anterior (indicador 6564), JA dessazonalizada pelo IBGE
        (ver docstring de domain/db/brasil/ibge/atv_pib_taxas.py) -- usada como par da modelagem
        "Trimestre" do grafico combinado.
    """
    req = MySQLDataRequester(_DATABASE, "atv_pib_taxas")
    req.connect()
    df = req.request_data()
    req.close_connection()
    df["date"] = pd.to_datetime(df["date"])
    df["value"] = pd.to_numeric(df["value"])
    df = df[(df["indicador"].isin(["yoy", "qoq", "acum_4t"])) & (df["name"].isin(_PIB_DEMANDA_NAMES))]

    result = {}
    for (name, indicador), grp in df.groupby(["name", "indicador"]):
        grp = grp.sort_values("date")
        result.setdefault(name, {})[indicador] = {
            "dates":  grp["date"].dt.strftime("%Y-%m-%d").tolist(),
            "values": [None if pd.isna(v) else round(float(v), 4) for v in grp["value"]],
        }
    return result


def _ieg_contrib_for_esfera(
    wide: pd.DataFrame, prefix: str, pib_4t: pd.Series, pib_pm: pd.Series, idx: pd.DatetimeIndex,
) -> dict:
    """Replica o calculo do IEG (ver docstring de _load_ieg) para uma unica esfera de governo
    (prefix = 'geral_'/'central_'/'estados_'/'municipios_'), sempre dividindo pelo PIB total
    (pib_4t/pib_pm) -- nao um PIB por esfera, mesma convencao das Tabelas 8-12 do paper (Resende &
    Pires), que usam o PIB nacional como denominador tanto para a Uniao quanto para Estados/
    Municipios.

    Retorna {categoria: {"acum4t": Serie, "quarter": Serie}}, indexadas por idx:
      - "acum4t" (D4, o IEG original do paper): variacao do acumulado em 4 trimestres (TTM,
        `pib_4t` como denominador) contra o TTM de 4 trimestres antes -- .diff(4) sobre o TTM, ver
        docstring de _load_ieg(). Inalterado nesta rodada.
      - "quarter" (2026-08, reescrito -- STL genuino, a pedido explicito do usuario apos ver o
        "Visao Combinada" da rodada anterior: "we have quarterly data, why not make the seasonal
        adjustment to work with the data properly?"): STL (period=4, ver
        transforms.stl_seasonal_adjust()) sobre a serie TRIMESTRAL bruta (SEM acumular -- `pib_pm`
        como denominador, NAO `pib_4t`) de cada categoria como %PIB do MESMO trimestre, seguido de
        .diff(1) sobre a serie ja dessazonalizada. Antes (rodada anterior) era um atalho --
        .diff(1) sobre o acumulado em 4T (TTM), sem rodar STL, escolhido por reusar dado ja
        coletado -- descartado porque nao e uma variacao trimestral genuina (e uma medida de
        aceleracao/desaceleracao do proprio acumulado movel) e deixava o IEG inconsistente com o
        PIB (indicador 'qoq' do IBGE, ja dessazonalizado de verdade) no grafico combinado. Mais
        proximo do metodo do proprio paper (secao 4.1, X-13 por categoria) do que o atalho
        anterior. Cada categoria roda seu proprio fit STL de forma independente -- a soma das 4
        categorias ainda reproduz o total EXATAMENTE (o total e definido em _load_ieg() como a
        soma das 4 "quarter" desta funcao, nao recalculado a parte), mas a soma de
        central+estados+municipios NAO reconcilia mais exatamente com geral (STL nao e linear,
        ao contrario de acum4t) -- ver Apendice/CLAUDE.md.

        **Cuidado com reindex antes do STL (bug encontrado e corrigido ao vivo, 2026-08)**:
        `central_` tem dado real desde 2006, 4 anos antes de `geral_`/`estados_`/`municipios_`
        existirem (2010-I, ver domain/db/brasil/tesouro/fisc_efgg.py). Reindexar cada componente
        para `idx` (janela cheia, 2006+) ANTES do STL fazia as 3 series mais curtas ganharem ~16
        trimestres de NaN no inicio, que `stl_seasonal_adjust()`'s `interpolate(limit_direction=
        "both")` preenche (backfill) com o primeiro valor real de 2010 -- um plato artificial que
        muda o fit do STL (media/tendencia sobre TODA a amostra) mesmo nos trimestres reais mais
        recentes, muito alem da borda. Confirmado ao vivo: central+estados+municipios chegava a
        ficar ~4-5x diferente de geral num mesmo trimestre (ex.: 2025-07, soma das 3 esferas =
        0,40 contra geral = 1,85) -- nao o residuo pequeno esperado de STL nao-linear (paragrafo
        acima), um bug real. Corrigido rodando o STL so sobre a janela onde CADA serie de
        categoria realmente tem dado (`_stl_on_valid_window()`, dropna() antes do fit, sem
        reindex previo para uma janela maior), remapeando o resultado de volta para `idx` so no
        final (None fora da janela real daquela esfera/categoria).
    """
    def col(name):
        key = f"{prefix}{name}"
        return wide[key] if key in wide.columns else pd.Series(index=wide.index, dtype=float)

    folha = col("salarios_vencimentos")
    transferencias = col("beneficios_previdenciarios_assistenciais")
    investimentos = col("aquisicao_ativos_nao_financeiros")
    despesa_ajustada = col("gasto") - col("consumo_capital_fixo") - col("juros") - col("transferencias_doacoes")
    outras = despesa_ajustada - folha - transferencias - investimentos

    componentes = {"folha": folha, "transferencias": transferencias, "investimentos": investimentos, "outras": outras}
    componentes_ttm = {k: v.rolling(4).sum() for k, v in componentes.items()}
    pct_pib_ttm = {k: (v.reindex(idx) / pib_4t.reindex(idx) * 100) for k, v in componentes_ttm.items()}
    # SEM reindex(idx) aqui -- fica no indice natural de cada componente (mais curto que idx para
    # central_/estados_/municipios_ nos casos em que a esfera comeca depois), pra
    # _stl_on_valid_window() rodar o fit so sobre a janela onde a serie realmente existe.
    pct_pib_raw = {k: (v / pib_pm.reindex(v.index) * 100) for k, v in componentes.items()}

    out = {}
    for k, mult in _IEG_MULTIPLICADORES.items():
        sa = _stl_on_valid_window(pct_pib_raw[k], period=4).reindex(idx)
        quarter = sa.diff(1) * mult
        out[k] = {"acum4t": pct_pib_ttm[k].diff(4) * mult, "quarter": quarter}
    return out


def _stl_on_valid_window(series: pd.Series, period: int) -> pd.Series:
    """Roda tf.stl_seasonal_adjust() so sobre o trecho DENSO (sem NaN) de `series`, nunca sobre
    uma janela reindexada/padded com NaN de fora -- ver docstring de _ieg_contrib_for_esfera() para
    o bug real que isso corrige (STL fitado sobre um plato artificial de backfill muda o resultado
    mesmo longe da borda). Retorna uma Serie indexada so pelas datas validas -- quem chama faz o
    proprio .reindex(idx) para voltar a grade completa (None fora da janela real)."""
    valid = series.dropna()
    if valid.empty:
        return pd.Series(dtype=float)
    dates_str = valid.index.strftime("%Y-%m-%d").tolist()
    sa = tf.stl_seasonal_adjust(dates_str, valid.tolist(), period=period)
    return pd.Series(sa, index=valid.index)


def _load_ieg() -> dict:
    """IEG (Impulso Estrutural do Gasto) -- Resende & Pires, Textos para Discussao no.16
    (FGV/Tesouro, 2024). Usa os multiplicadores FIXOS publicados no paper (ainda nao
    re-estimados neste projeto -- ver analytics/brasil/fiscal_policy/reference/rtn_vs_efgg.md):
        Folha          x1,32  <- fisc_efgg geral_salarios_vencimentos       (GFSM 211)
        Transferencias x1,46  <- fisc_efgg geral_beneficios_previdenciarios_assistenciais (27)
        Investimentos  x1,66  <- fisc_efgg geral_aquisicao_ativos_nao_financeiros (31.1)
        Outras         x0,64  <- residuo = despesa_ajustada - (Folha+Transf.+Invest.), onde
                                  despesa_ajustada = gasto (2) - consumo_capital_fixo (23)
                                  - juros (24) - transferencias_doacoes (26)

    IEG(t) = soma_i multiplicador_i x D4(pct_PIB_i(t)), D4 = variacao interanual (4 trimestres) do
    acumulado em 4 trimestres (ver abaixo).

    O paper (secao 4.1) deflaciona, LOGARITIMIZA e DESSAZONALIZA (X-13) PIB e despesa antes de
    calcular qualquer variacao, e seus resultados (Tabela 6/8-12) sao variacoes ANUAIS (ano t vs.
    ano t-1 -- ver Tabela 6). A primeira versao desta funcao pulou os dois passos -- tomava
    diff() trimestral (Q vs. Q-1) direto sobre a serie NSA -- o que reintroduz exatamente a
    sazonalidade que o paper remove: gasto publico tem um calendario de execucao
    orcamentaria/pagamento fortemente sazonal dentro do ano (ex.: 13o salario, concentracao de
    investimento no fim do ano), entao um diff() trimestral bruto oscila Q1-negativo/Q2-positivo
    todo ano, sem relacao com o "impulso" que o indicador pretende medir.

    Correcao: em vez de rodar X-13 por categoria (exigiria amostra mais longa por serie para
    convergir bem), usa-se o acumulado em 4 trimestres (TTM) tanto no numerador (cada categoria
    de despesa) quanto no denominador (PIB) -- mesma convencao ja usada no projeto para series
    fiscais (fisc_nfsp's colunas *_pct_pib_12m) -- e a variacao e tomada com .diff(4), nao
    .diff(1): TTM(t) - TTM(t-4) de uma serie X equivale a [X(t)+...+X(t-3)] -
    [X(t-4)+...+X(t-7)], ou seja, compara o ano-movel terminado em t contra o ano-movel terminado
    um ano antes -- uma versao "rolante" (recalculada a cada trimestre) da mesma comparacao
    ano-contra-ano-anterior do paper, sem precisar de X-13. Validado diretamente contra a Tabela 6
    do paper: o valor do 4o trimestre de cada ano (onde o TTM = soma do ano civil) fica muito
    proximo do impulso anual publicado (ex.: 2020 6,87% nos dois; 2018 -0,24% nos dois; 2012 0,71%
    nos dois) -- pequenas diferencas residuais vem da definicao de escopo/periodo e do paper usar
    X-13 de fato em vez do atalho TTM usado aqui.

    Escopo Governo Geral (Central+Estados+Municipios), NAO Governo Central sozinho (RTN) --
    ver analytics/brasil/fiscal_policy/reference/rtn_vs_efgg.md para a diferenciacao completa.

    Decomposicao por ente ("esfera") x categoria (2026-08, reestruturado a pedido do usuario --
    "IEG: decomposition bar-graph (Quarter and 4Q accum) by spheres and categories. Put a table
    like the one in Receitas e Despesas"): fisc_efgg ja guarda os mesmos 16 codigos GFSM sob 4
    namespaces -- central_/estados_/municipios_/geral_ (geral = soma dos 3, ver
    domain/db/brasil/tesouro/fisc_efgg.py). Roda _ieg_contrib_for_esfera() para cada uma das 4
    esferas (geral incluida), sempre dividindo pelo MESMO PIB total (pib_4t, nao um PIB por
    esfera -- mesma convencao das Tabelas 8-12 do paper), o que reconcilia exatamente: como
    geral_x = central_x + estados_x + municipios_x para cada categoria x, e diff()/soma por
    multiplicador sao operacoes lineares, contrib_geral = contrib_central + contrib_estados +
    contrib_municipios em toda data e em AMBAS as variantes (acum4t/quarter) -- nao e uma
    aproximacao. Retorna uma arvore/serie no mesmo formato {tree, series} usado por
    gfsm_tab.py/rtn_tab.py (ver makeImpulsoHierTab() em report.html), so que SEM os eixos
    Nominal/Real/%PIB da GFSM/RTN -- a contribuicao do IEG ja e uma variacao ponderada em p.p.,
    nao um nivel monetario a ser deflacionado ou dividido pelo PIB de novo. Desde 2026-08 a
    Esfera deixou de ser um dropdown e virou o PRIMEIRO NIVEL da propria arvore (Esfera >
    Categoria, ver a construcao de `tree` abaixo), sobrando um unico eixo de controle: a
    modelagem Trimestre/Acum. 4T ("Nivel"). A esfera "banco_central" do impulso via resultado
    primario (fisc_nfsp, abaixo) NAO existe aqui -- fisc_efgg/EFGG so cobre Governo
    Geral/Central/Estados/Municipios, sem um corte de Banco Central proprio.
    """
    efgg = _load_table("fisc_efgg")
    wide = efgg.pivot(index="date", columns="name", values="value")

    pib = _load_table("atv_pib_valores_correntes")
    pib_pm = pib[pib["name"] == "pib_pm"].set_index("date")["value"].sort_index()
    pib_4t = pib_pm.rolling(4).sum()

    # wide.index e a UNIAO das datas de TODAS as colunas/esferas em fisc_efgg -- inclui
    # central_* isolado, que comeca em 2006, bem antes de geral_/estados_/municipios_
    # existirem (2010-I). Sem recortar para a janela onde o IEG (geral) de fato tem valor,
    # cada serie enviada ao relatorio carregaria anos de datas com y=None na ponta esquerda
    # -- o Plotly ainda reserva espaco de eixo X pra esse trecho vazio (sobretudo no botao
    # "Tudo"), deixando uma faixa em branco no grafico sem nenhuma barra/ponto. Calcula o
    # IEG geral numa janela "cheia" primeiro, so pra descobrir onde ele de fato comeca/termina
    # a ter valor, e recorta idx pra essa janela antes de montar o resto do payload.
    idx_full = wide.index.intersection(pib_4t.dropna().index).sort_values()
    contrib_full = _ieg_contrib_for_esfera(wide, "geral_", pib_4t, pib_pm, idx_full)
    ieg_full_acum4t = sum(v["acum4t"] for v in contrib_full.values())
    ieg_full_quarter = sum(v["quarter"] for v in contrib_full.values())
    valid = ieg_full_acum4t.dropna()
    idx = idx_full[(idx_full >= valid.index.min()) & (idx_full <= valid.index.max())] if len(valid) else idx_full

    ieg_acum4t = ieg_full_acum4t.reindex(idx)
    ieg_quarter = ieg_full_quarter.reindex(idx)

    def to_list(s):
        return [None if pd.isna(v) else round(float(v), 4) for v in s.reindex(idx)]

    def variant_pair(acum4t_series, quarter_series):
        return {
            "acum4t":  {"dates": idx.strftime("%Y-%m-%d").tolist(), "values": to_list(acum4t_series)},
            "quarter": {"dates": idx.strftime("%Y-%m-%d").tolist(), "values": to_list(quarter_series)},
        }

    # central_* comeca em 2006 no fisc_efgg (antes de estados_/municipios_/geral_ existirem, que so
    # tem dados a partir de 2010-I -- ver domain/db/brasil/tesouro/fisc_efgg.py) -- sem essa
    # mascara, a Uniao apareceria com contribuicao real anos antes de a linha do IEG (geral)
    # comecar a existir, quebrando a garantia de que as 4 esferas somam exatamente o IEG total.
    #
    # Importante: calcula sobre idx_full (nao o idx ja recortado acima), so reindexando para
    # idx no final -- _ieg_contrib_for_esfera() reindexa pct_pib para o idx recebido ANTES de
    # aplicar .diff(4)/.diff(1), que sao diffs posicionais (linha i menos linha i-N DENTRO da
    # serie recebida). Passar o idx ja recortado faz as primeiras linhas perderem o "olhar pra
    # tras" de que precisam, gerando None nos primeiros trimestres do grafico por ente --
    # exatamente o mesmo tipo de "range vazio" que a mascara abaixo existe pra evitar, so que
    # introduzido por este calculo em vez de pela janela de fisc_efgg.
    ESFERAS = [
        ("geral", "geral_", "Geral (Governo Geral)"),
        ("central", "central_", "União"),
        ("estados", "estados_", "Estados"),
        ("municipios", "municipios_", "Municípios"),
    ]
    CATEGORIAS = [
        ("folha", "Folha (×1,32)"),
        ("transferencias", "Transferências (×1,46)"),
        ("investimentos", "Investimentos (×1,66)"),
        ("outras", "Outras (×0,64)"),
    ]

    series = {}
    mask = ieg_acum4t.notna()
    for esfera, prefix, _ in ESFERAS:
        esfera_contrib = contrib_full if esfera == "geral" else _ieg_contrib_for_esfera(wide, prefix, pib_4t, pib_pm, idx_full)
        acum4t_total = sum(v["acum4t"] for v in esfera_contrib.values()).reindex(idx).where(mask)
        quarter_total = sum(v["quarter"] for v in esfera_contrib.values()).reindex(idx).where(mask)
        # O total da esfera e uma chave IRMA das categorias dentro do mesmo `series`
        # (chave = so o nome da esfera, sem "__categoria") -- e o no PAI na arvore abaixo,
        # entao precisa ser plotavel/checavel exatamente como qualquer outra linha.
        series[esfera] = variant_pair(acum4t_total, quarter_total)
        for categoria, _label in CATEGORIAS:
            acum4t_cat = esfera_contrib[categoria]["acum4t"].reindex(idx).where(mask)
            quarter_cat = esfera_contrib[categoria]["quarter"].reindex(idx).where(mask)
            series[f"{esfera}__{categoria}"] = variant_pair(acum4t_cat, quarter_cat)

    # Arvore Esfera > Categoria de despesa (2026-08, a pedido explicito do usuario --
    # "The hierarque should be: Sphere > Expenditure catergories. Then I can click on the
    # series I want to see. Mantain just the 'Nivel' click-dropdown"). Substitui o par
    # anterior (dropdown de Esfera + lista plana das 4 categorias): as 4 esferas agora
    # convivem na MESMA tabela, cada uma expansivel nas suas 4 categorias, e o seletor de
    # Esfera deixou de existir.
    tree = [
        {
            "key": esfera, "label": label, "seriesKey": esfera,
            "children": [
                {"key": f"{esfera}__{cat}", "label": cat_label, "seriesKey": f"{esfera}__{cat}"}
                for cat, cat_label in CATEGORIAS
            ],
        }
        for esfera, _prefix, label in ESFERAS
    ]

    return {
        "dates": idx.strftime("%Y-%m-%d").tolist(),
        "ieg": to_list(ieg_acum4t),
        "ieg_quarter": to_list(ieg_quarter),
        "tree": tree,
        "series": series,
    }


def run(output: str = "reports/brasil/Fiscal Policy.html") -> None:
    print("Carregando dados...")
    data = {"generated_at": datetime.now().strftime("%d/%m/%Y %H:%M")}

    try:
        gfsm = _load_gfsm_tab_data()
        data["gfsm"] = gfsm
        print(f"  gfsm (arvore Receita/Despesa GFSM): {len(gfsm['series'])} series")
    except Exception as exc:
        print(f"  gfsm: FALHOU -- {exc}")
        data["gfsm"] = {"tree": [], "series": {}, "ref_date": None}

    try:
        rtn = _load_rtn_tab_data()
        data["rtn"] = rtn
        print(f"  rtn (arvore Receita/Despesa RTN, Governo Central): {len(rtn['series'])} series")
    except Exception as exc:
        print(f"  rtn: FALHOU -- {exc}")
        data["rtn"] = {"tree": [], "series": {}, "ref_date": None}

    try:
        dlsp = _load_dlsp_tab_data()
        data["dlsp"] = dlsp
        n_series = sum(len(v) for v in dlsp["series"].values())
        print(f"  dlsp (fisc_dlsp_fatores): {len(dlsp['fatores'])} fatores, {n_series} series, {len(dlsp['dates'])} meses")
    except Exception as exc:
        print(f"  dlsp: FALHOU -- {exc}")
        data["dlsp"] = {"fatores": [], "notes": {}, "tree": [], "dates": [], "series": {}, "anchor": None}

    try:
        investimento = _load_investimento_tab_data()
        data["investimento"] = investimento
        n_series = sum(len(c["series"]) for c in investimento["cortes"].values())
        print(f"  investimento (fisc_investimento): {len(investimento['cortes'])} cortes, {n_series} series")
    except Exception as exc:
        print(f"  investimento: FALHOU -- {exc}")
        data["investimento"] = {"cortes": {}, "ref_date": None}

    try:
        ieg = _load_ieg()
        data["ieg"] = ieg
        print(f"  ieg (fisc_efgg + atv_pib_valores_correntes): {len(ieg['dates'])} trimestres")
    except Exception as exc:
        print(f"  ieg: FALHOU -- {exc}")
        data["ieg"] = {}

    try:
        pib_yoy = _load_pib_yoy()
        data["pib_yoy"] = pib_yoy
        n_obs = sum(len(m["dates"]) for v in pib_yoy.values() for m in v.values())
        print(f"  pib_yoy (atv_pib_taxas): {len(pib_yoy)} series, {n_obs} obs")
    except Exception as exc:
        print(f"  pib_yoy: FALHOU -- {exc}")
        data["pib_yoy"] = {}

    try:
        credito_oficial = _load_impulso_credito_oficial()
        data["credito_oficial"] = credito_oficial
        print(f"  credito_oficial (fisc_dlsp_fatores, fator primario): {len(credito_oficial['dates'])} meses")
    except Exception as exc:
        print(f"  credito_oficial: FALHOU -- {exc}")
        data["credito_oficial"] = {"dates": [], "series": {}, "tree": [], "anchor": None}

    try:
        fiscal_impulse_nfsp = _load_fiscal_impulse_nfsp()
        data["fiscal_impulse_nfsp"] = fiscal_impulse_nfsp
        print(f"  fiscal_impulse_nfsp (fisc_nfsp): {len(fiscal_impulse_nfsp['dates'])} meses")
    except Exception as exc:
        print(f"  fiscal_impulse_nfsp: FALHOU -- {exc}")
        data["fiscal_impulse_nfsp"] = {}

    out = render_report(_TEMPLATE, data, output)
    print(f"Relatorio salvo: {out}")


if __name__ == "__main__":
    run()
