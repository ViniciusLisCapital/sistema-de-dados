"""
Gerador do Panorama Fiscal em HTML.

Impulso Fiscal (IEG) + Apendice sao as unicas abas depois da limpeza de 2026-08 --
usuario pediu para apagar Visao Geral/Divida Publica/Resultado Fiscal/Receita e
Despesa e reconstruir o dashboard aba por aba, mesmo padrao ja usado em
analytics/credit/ (ver "Report structure" em analytics/fiscal_policy/CLAUDE.md).
fisc_divida/fisc_nfsp/fisc_rtn continuam alimentadas normalmente por
jobs/update_db.py -- so pararam de ser lidas por ESTE relatorio ate as abas
correspondentes serem reconstruidas (se/quando forem).

Le fisc_efgg (IEG) + atv_pib_valores_correntes (denominador do IEG) +
atv_pib_taxas (comparacao com o PIB oficial) de macro_brasil, e injeta no
template report.html, gerando um arquivo HTML autocontido. Mesmo padrao
/*REPORT_DATA*/ de analytics/economic_activity/ e analytics/inflation/ -- sem
Jinja2, via analytics.report_structure.builder.render_report().

Uso:
    uv run python analytics/fiscal_policy/generate_report.py
    uv run python -c "from analytics.fiscal_policy.generate_report import run; run()"
"""

from datetime import datetime
from pathlib import Path

import pandas as pd

from analytics.fiscal_policy import gfsm_tab
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
    analytics/fiscal_policy/transforms.py's compute_pct_pib_ttm()). Recalculado aqui
    em vez de reusar o pib_4t interno de _load_ieg() para nao acoplar as duas
    funcoes -- o calculo (rolling(4).sum() sobre ~65 trimestres) e trivial.
    """
    pib = _load_table("atv_pib_valores_correntes")
    pib_pm = pib[pib["name"] == "pib_pm"].set_index("date")["value"].sort_index()
    pib_4t = pib_pm.rolling(4).sum()
    return {d.strftime("%Y-%m-%d"): (None if pd.isna(v) else float(v)) for d, v in pib_4t.items()}


def _load_gfsm_tab_data() -> dict:
    """Aba Receitas e Despesas (GFSM) -- ver analytics/fiscal_policy/gfsm_tab.py."""
    efgg = _load_flat("fisc_efgg")
    raw = {k: efgg[k] for k in gfsm_tab.DB_NAMES}
    ipca = _load_flat("inflc_agregados")["ipca"]
    gdp_ttm = _load_pib_4t()
    return gfsm_tab.build(raw, ipca, gdp_ttm)


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
    """PIB (total) + os 5 componentes da otica da demanda, variacao interanual (Y/Y, sem ajuste
    sazonal), taxa OFICIAL do IBGE -- atv_pib_taxas, indicador='yoy' (mesma tabela/indicador que
    analytics/economic_activity usa para o mesmo fim, ver Data map desse relatorio). Usado para
    comparar contra o IEG na aba Impulso Fiscal -- nao entra no calculo do IEG em si.
    """
    req = MySQLDataRequester(_DATABASE, "atv_pib_taxas")
    req.connect()
    df = req.request_data()
    req.close_connection()
    df["date"] = pd.to_datetime(df["date"])
    df["value"] = pd.to_numeric(df["value"])
    df = df[(df["indicador"] == "yoy") & (df["name"].isin(_PIB_DEMANDA_NAMES))]

    result = {}
    for name, grp in df.groupby("name"):
        grp = grp.sort_values("date")
        result[name] = {
            "dates":  grp["date"].dt.strftime("%Y-%m-%d").tolist(),
            "values": [None if pd.isna(v) else round(float(v), 4) for v in grp["value"]],
        }
    return result


def _ieg_contrib_for_esfera(wide: pd.DataFrame, prefix: str, pib_4t: pd.Series, idx: pd.DatetimeIndex) -> dict:
    """Replica o calculo do IEG (ver docstring de _load_ieg) para uma unica esfera de governo
    (prefix = 'geral_'/'central_'/'estados_'/'municipios_'), sempre dividindo pelo PIB total
    (pib_4t) -- nao um PIB por esfera, mesma convencao das Tabelas 8-12 do paper (Resende & Pires),
    que usam o PIB nacional como denominador tanto para a Uniao quanto para Estados/Municipios.
    Retorna {categoria: Serie de contribuicao ponderada, indexada por idx}.
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
    pct_pib = {k: (v.reindex(idx) / pib_4t.reindex(idx) * 100) for k, v in componentes_ttm.items()}
    return {k: pct_pib[k].diff(4) * mult for k, mult in _IEG_MULTIPLICADORES.items()}


def _load_ieg() -> dict:
    """IEG (Impulso Estrutural do Gasto) -- Resende & Pires, Textos para Discussao no.16
    (FGV/Tesouro, 2024). Usa os multiplicadores FIXOS publicados no paper (ainda nao
    re-estimados neste projeto -- ver analytics/fiscal_policy/reference/rtn_vs_efgg.md):
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
    ver analytics/fiscal_policy/reference/rtn_vs_efgg.md para a diferenciacao completa.

    Decomposicao por ente ("esfera"): fisc_efgg ja guarda os mesmos 16 codigos GFSM sob 4
    namespaces -- central_/estados_/municipios_/geral_ (geral = soma dos 3, ver
    domain/db/brasil/tesouro/fisc_efgg.py). Rodar _ieg_contrib_for_esfera() para cada uma das 3
    esferas, sempre dividindo pelo MESMO PIB total (pib_4t, nao um PIB por esfera -- mesma
    convencao das Tabelas 8-12 do paper), reconcilia exatamente com o IEG geral: como
    geral_x = central_x + estados_x + municipios_x para cada categoria x, e diff()/soma por
    multiplicador sao operacoes lineares, contrib_geral = contrib_central + contrib_estados +
    contrib_municipios em toda data -- nao e uma aproximacao.
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
    contrib_full = _ieg_contrib_for_esfera(wide, "geral_", pib_4t, idx_full)
    ieg_full = sum(contrib_full.values())
    valid = ieg_full.dropna()
    idx = idx_full[(idx_full >= valid.index.min()) & (idx_full <= valid.index.max())] if len(valid) else idx_full

    contrib = {k: v.reindex(idx) for k, v in contrib_full.items()}
    ieg = ieg_full.reindex(idx)

    # pct_pib (nivel, nao contribuicao) e usado so pelo grafico de decomposicao por categoria --
    # precisa ser recalculado aqui (nao vem de _ieg_contrib_for_esfera, que so retorna as
    # contribuicoes ja multiplicadas).
    def col_geral(name):
        key = f"geral_{name}"
        return wide[key] if key in wide.columns else pd.Series(index=wide.index, dtype=float)

    componentes_geral = {
        "folha": col_geral("salarios_vencimentos"),
        "transferencias": col_geral("beneficios_previdenciarios_assistenciais"),
        "investimentos": col_geral("aquisicao_ativos_nao_financeiros"),
    }
    despesa_ajustada = col_geral("gasto") - col_geral("consumo_capital_fixo") - col_geral("juros") - col_geral("transferencias_doacoes")
    componentes_geral["outras"] = despesa_ajustada - componentes_geral["folha"] - componentes_geral["transferencias"] - componentes_geral["investimentos"]
    pct_pib = {k: (v.rolling(4).sum().reindex(idx) / pib_4t.reindex(idx) * 100) for k, v in componentes_geral.items()}

    # central_* comeca em 2006 no fisc_efgg (antes de estados_/municipios_/geral_ existirem, que so
    # tem dados a partir de 2010-I -- ver domain/db/brasil/tesouro/fisc_efgg.py) -- sem essa
    # mascara, a Uniao apareceria com contribuicao real anos antes de a linha do IEG (geral)
    # comecar a existir, quebrando a garantia de que as 3 esferas somam exatamente o IEG total.
    #
    # Importante: calcula sobre idx_full (nao o idx ja recortado acima), so reindexando para
    # idx no final -- _ieg_contrib_for_esfera() reindexa pct_pib para o idx recebido ANTES de
    # aplicar .diff(4), que e um diff posicional (linha i menos linha i-4 DENTRO da serie
    # recebida). Passar o idx ja recortado faz as primeiras 4 linhas perderem o "olhar pra
    # tras" de que precisam, gerando None nos primeiros 4 trimestres do grafico por ente --
    # exatamente o mesmo tipo de "range vazio" que a mascara abaixo existe pra evitar, so que
    # introduzido por este calculo em vez de pela janela de fisc_efgg.
    esferas = {}
    for esfera, prefix in [("central", "central_"), ("estados", "estados_"), ("municipios", "municipios_")]:
        esfera_contrib = _ieg_contrib_for_esfera(wide, prefix, pib_4t, idx_full)
        esferas[esfera] = sum(esfera_contrib.values()).reindex(idx).where(ieg.notna())

    def to_list(s):
        return [None if pd.isna(v) else round(float(v), 4) for v in s.reindex(idx)]

    return {
        "dates": idx.strftime("%Y-%m-%d").tolist(),
        "ieg": to_list(ieg),
        "contrib": {k: to_list(v) for k, v in contrib.items()},
        "pct_pib": {k: to_list(v) for k, v in pct_pib.items()},
        "esfera": {k: to_list(v) for k, v in esferas.items()},
    }


def run(output: str = "reports/fiscal_policy_latest.html") -> None:
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
        ieg = _load_ieg()
        data["ieg"] = ieg
        print(f"  ieg (fisc_efgg + atv_pib_valores_correntes): {len(ieg['dates'])} trimestres")
    except Exception as exc:
        print(f"  ieg: FALHOU -- {exc}")
        data["ieg"] = {}

    try:
        pib_yoy = _load_pib_yoy()
        data["pib_yoy"] = pib_yoy
        n_obs = sum(len(v["dates"]) for v in pib_yoy.values())
        print(f"  pib_yoy (atv_pib_taxas): {len(pib_yoy)} series, {n_obs} obs")
    except Exception as exc:
        print(f"  pib_yoy: FALHOU -- {exc}")
        data["pib_yoy"] = {}

    out = render_report(_TEMPLATE, data, output)
    print(f"Relatorio salvo: {out}")


if __name__ == "__main__":
    run()
