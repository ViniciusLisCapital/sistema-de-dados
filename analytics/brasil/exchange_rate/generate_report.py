"""
Gerador do relatório HTML de fundamentos cambiais.

Lê tabelas de macro_brasil e macro_international, injeta os dados no template
report.html e salva um único arquivo HTML autocontido em "reports/brasil/FX Report.html".

Desde 2026-08 este é o ÚNICO entry point do relatório cambial: as três abas de
modelo que antes viviam num dashboard separado (reports/ppp_dashboard.html, via
models/ppp_dashboard_template.html) foram fundidas no mesmo report.html, então
run() monta quatro payloads — os dados brutos (/*REPORT_DATA*/) mais PPP,
FX Attribution e Ridge. Os três de modelo são opcionais (include_models=False,
ou qualquer falha na construção): cada aba já tem seu próprio estado "sem dados
embutidos", então o relatório de dados continua saindo inteiro.

Uso:
    uv run python -c "from analytics.brasil.exchange_rate.generate_report import run; run()"
    # sem as abas de modelo (mais rápido — não busca FRED nem roda os fits):
    uv run python -c "from analytics.brasil.exchange_rate.generate_report import run; run(include_models=False)"
"""

from datetime import datetime
from pathlib import Path

import pandas as pd

from analytics.report_structure.builder import render_report
from connectors.mysql import MySQLDataRequester

_TEMPLATE = Path(__file__).parent / "report.html"


# ── Helpers ───────────────────────────────────────────────────────────────────

def _dates(index: pd.DatetimeIndex) -> list:
    return [d.strftime("%Y-%m-%d") for d in index]


def _to_list(s: pd.Series) -> list:
    return [None if pd.isna(v) else float(v) for v in s]


def _col(wide: pd.DataFrame, name: str):
    if name not in wide.columns:
        return None
    return _to_list(wide[name])


def _fetch(database: str, table: str) -> pd.DataFrame | None:
    req = MySQLDataRequester(database, table)
    req.connect()
    if req.connection is None:
        print(f"  Aviso: sem conexão para {database}.{table}")
        return None
    df = req.request_data()
    req.close_connection()
    if df is None or df.empty:
        print(f"  Aviso: {database}.{table} vazia ou sem dados")
        return None
    df["date"] = pd.to_datetime(df["date"])
    return df


def _pivot(database: str, table: str) -> pd.DataFrame | None:
    """Lê tabela com schema (date, name, value) e pivota para wide."""
    df = _fetch(database, table)
    if df is None:
        return None
    df["value"] = df["value"].astype(float)
    return df.pivot(index="date", columns="name", values="value").sort_index()


# ── Data loaders ──────────────────────────────────────────────────────────────

def _load_diferenciais() -> dict:
    try:
        wide = _pivot("macro_international", "diferenciais_juros")
        if wide is None:
            return {}
        return {
            "dates":               _dates(wide.index),
            "selic":               _col(wide, "selic"),
            "fed_funds":           _col(wide, "fed_funds"),
            "ipca_12m":            _col(wide, "ipca_12m"),
            "cpi_12m_us":          _col(wide, "cpi_12m_us"),
            "diferencial_nominal": _col(wide, "diferencial_nominal"),
            "real_br_ex_post":     _col(wide, "real_br_ex_post"),
            "real_us_ex_post":     _col(wide, "real_us_ex_post"),
            "diferencial_real":    _col(wide, "diferencial_real"),
        }
    except Exception as exc:
        print(f"  Aviso: erro em diferenciais_juros — {exc}")
        return {}


def _load_reer() -> dict:
    try:
        df = _fetch("macro_international", "cmb_reer")
        if df is None:
            return {}
        df["value"] = df["value"].astype(float)
        rb = df[df["reer_type"] == "real_broad"].copy()
        wide = rb.pivot(index="date", columns="country_code", values="value").sort_index()
        return {
            "dates": _dates(wide.index),
            "BR":    _col(wide, "BR"),
            "MX":    _col(wide, "MX"),
            "CL":    _col(wide, "CL"),
            "CO":    _col(wide, "CO"),
        }
    except Exception as exc:
        print(f"  Aviso: erro em cmb_reer — {exc}")
        return {}


# As cinco categorias de participante do TFF, na ordem em que o proprio relatorio
# da CFTC as lista. Carregadas desde 2026-09-01 (antes so `lev` e `nonrept`, e o
# relatorio so desenhava `lev_net`) -- a pergunta "alem dos alavancados, quem mais
# esta no mercado" nao tinha resposta no dado.
_COT_PARTIES = ["dealer", "asset_mgr", "lev", "other", "nonrept"]


def _load_cot_fx() -> dict:
    """Posicionamento COT do futuro de BRL na CME (CFTC TFF), semanal.

    Serializa o open interest e, por categoria, a posicao liquida mais as pernas
    bruta comprada e vendida. Duas identidades fecham EXATAMENTE nas 748 semanas
    (conferido contra o banco, residuo 0): a soma dos cinco liquidos e zero, e a
    soma de (comprado + spread) de todos e o open interest -- as mesmas dos dois
    lados. Sao elas que autorizam a pilha do grafico.

    A serie e semanal com data de TERCA (740 das 748; as 8 restantes caem na
    segunda, semana de feriado) e tem buracos: 16 intervalos maiores que 8 dias
    ate 2015, um deles de 196 dias entre out/2011 e abr/2012. O relatorio nao
    reindexa para uma grade semanal densa -- a media movel la aplica um guarda de
    span justamente para nao chamar de "12 semanas" uma janela de 12 OBSERVACOES
    que cobre oito meses.
    """
    try:
        df = _fetch("macro_international", "cmb_cot_fx")
        if df is None:
            return {}
        df["value"] = df["value"].astype(float)
        brl = df[df["currency"] == "BRL"].copy()
        wide = brl.pivot(index="date", columns="name", values="value").sort_index()
        out = {"dates": _dates(wide.index), "open_interest": _col(wide, "open_interest")}
        for p in _COT_PARTIES:
            # `spread` entra apesar de nenhum grafico o desenhar: sem ele a
            # identidade bruta (comprado + spread, somado nas 5 categorias = open
            # interest) nao fecha no arquivo entregue, e a participacao de cada
            # grupo no mercado -- que as notas e os cartoes AFIRMAM em numero --
            # deixa de ser reproduzivel por quem le. `nonrept` nao tem spread na
            # fonte, entao a coluna sai ausente e `_col` devolve nulos.
            for suf in ("net", "long", "short", "spread"):
                if p == "nonrept" and suf == "spread":
                    continue
                out[f"{p}_{suf}"] = _col(wide, f"{p}_{suf}")
        return out
    except Exception as exc:
        print(f"  Aviso: erro em cmb_cot_fx — {exc}")
        return {}


def _load_bcb_positioning() -> dict:
    """Reservas internacionais, posicao de cambio (BCB/bancos) e intervencoes.

    Alimenta a aba "Posicionamento do BCB". `cmb_reservas_bc` mistura frequencias
    (mensal para reservas/swap, diaria para reservas_liquidity/intervencoes)
    numa unica tabela -- pivotar tudo junto criaria um indice de datas comum
    onde a maioria das linhas mensais ficaria cercada de nulls (a serie
    "quebraria" visualmente com connectgaps=false). Em vez disso, cada
    subgrupo abaixo pivota so suas proprias series e carrega seu proprio
    eixo "dates".

    Todas as series usadas aqui (reservas, ouro, swap, intervencoes) estao em
    USD MM na fonte -- convertidas para USD Bi (/1000) para exibicao no
    relatorio. `reserves_gold_volume` (troy oz) nao e usada nesta funcao.

    Dois subgrupos alimentam tabelas hierarquicas (2026-08-27):

    `reservas_arvore` -- o template de reservas do FMI que o BCB publica em SGS
    3546-3556/7323, e cuja aditividade fecha na fonte (medido: residuo medio
    0,0005 USD Bi, maximo 0,010 em 307 meses):
        total = moeda estrangeira + ouro + DES + posicao no FMI + outros
        moeda estrangeira = titulos + moeda e depositos
        outros = compromissadas reversas + emprestimos + derivativos
    E ESTOQUE, nao fluxo: o relatorio agrega por FIM DE PERIODO, nunca somando.

    `intervencoes` -- as 4 series de intervencao liquida liquidada, somadas em
    meses. A tabela **descarta os zeros** por decisao do ETL (ver
    `_drop_zero_interventions` em domain/db/brasil/bcb/cmb_reservas_bc.py), entao
    dia ausente dentro da janela de publicacao e intervencao zero, e nao dado
    faltante -- e isso que justifica somar sobre um calendario completo em vez de
    propagar null. A janela de publicacao NAO pode sair do max() das proprias
    series (o BCB passa meses sem intervir -- 2023 nao tem nenhum registro de
    spot, e cortar ali esconderia meses de zeros legitimos): vem de
    `reserves_total_daily`, que e diaria na mesma tabela e nao sofre a remocao de
    zeros. O ultimo mes so entra se essa serie alcancou o ultimo dia util dele,
    mesma regra de _load_cambio_contratado().
    """
    try:
        df = _fetch("macro_brasil", "cmb_reservas_bc")
        if df is None:
            return {}
        df["value"] = df["value"].astype(float) / 1000.0

        def _subgroup(names: list) -> dict:
            sub = df[df["name"].isin(names)]
            if sub.empty:
                return {}
            wide = sub.pivot(index="date", columns="name", values="value").sort_index()
            return {"dates": _dates(wide.index), **{n: _col(wide, n) for n in names}}

        # PIB mensal em USD, reindexado para a grade de cada subgrupo. Nas reservas
        # o denominador e a soma movel de 12 meses (estoque / PIB anual, a leitura
        # usual de adequacao de reservas); nas intervencoes e a soma na MESMA janela
        # do bucket, como no resto do relatorio.
        gdp_wide = _pivot("macro_brasil", "atv_pib_usd")
        gdp_m = ((gdp_wide["pib_usd"] / 1000.0)
                 if gdp_wide is not None and "pib_usd" in gdp_wide.columns else None)

        # -- arvore de reservas (mensal, template do FMI) ----------------------
        _ARV = ["reserves_total_monthly", "reserves_fx_total", "reserves_fx_securities",
                "reserves_fx_currency_deposits", "reserves_gold_usd", "reserves_sdrs",
                "reserves_imf_position", "reserves_other_total", "reserves_other_reverse_repo",
                "reserves_other_loans", "reserves_other_derivatives"]
        sub = df[df["name"].isin(_ARV)]
        arvore = {}
        if not sub.empty:
            w = sub.pivot(index="date", columns="name", values="value").sort_index()
            # Corte em 2001-01, onde a decomposicao comeca. O total sozinho vai a
            # 1971, mas mante-lo aqui abriria a arvore com 30 anos em que so a raiz
            # tem valor -- o grafico de manchete da secao acima e quem mostra essa
            # historia longa, e ele nao e arvore.
            w = w[w.index >= pd.Timestamp("2001-01-01")]
            w = w.reindex(pd.date_range(w.index.min(), w.index.max(), freq="MS"))
            arvore = {"dates": _dates(w.index), **{n: _col(w, n) for n in _ARV}}
            if gdp_m is not None:
                arvore["gdp_usd_bi"] = _to_list(gdp_m.reindex(w.index))

        # -- intervencoes (diarias, somadas em meses) --------------------------
        _INT = ["bcb_intervention_spot", "bcb_intervention_forwards",
                "bcb_intervention_fx_loans_repos", "bcb_intervention_repo_lines"]
        sub = df[df["name"].isin(_INT)]
        interv = {}
        if not sub.empty:
            w = sub.pivot(index="date", columns="name", values="value").sort_index()
            diario = df[df["name"] == "reserves_total_daily"]["date"]
            alcance = diario.max() if not diario.empty else w.index.max()
            w = w.reindex(pd.date_range(w.index.min(), alcance, freq="D")).fillna(0.0)
            mensal = w.resample("MS").sum(min_count=0)
            if alcance < (alcance + pd.offsets.BMonthEnd(0)):
                mensal = mensal.iloc[:-1]
            for c in _INT:
                if c not in mensal.columns:
                    mensal[c] = 0.0
            mensal["bcb_intervention_total"] = mensal[_INT].sum(axis=1)
            interv = {"dates": _dates(mensal.index),
                      **{c: _to_list(mensal[c]) for c in _INT + ["bcb_intervention_total"]}}
            if gdp_m is not None:
                interv["gdp_usd_bi"] = _to_list(gdp_m.reindex(mensal.index))
            interv["ultimo_dia_diario"] = alcance.strftime("%Y-%m-%d")

        # A secao de posicao cambial ganhou tabela em 2026-08-27: precisa do mesmo
        # denominador de 12 meses da arvore de reservas, porque tambem e posicao em
        # aberto e nao fluxo.
        swap = _subgroup(["bcb_swap_cambial_position", "bcb_fx_stock_repos_loans",
                          "bcb_fx_other_assets_liabilities", "bank_fx_spot_position"])
        if swap and gdp_m is not None:
            swap["gdp_usd_bi"] = _to_list(gdp_m.reindex(pd.to_datetime(swap["dates"])))

        return {
            "reserves": _subgroup(["reserves_liquidity_daily", "reserves_total_monthly"]),
            # As tres linhas do BCB sao a exposicao cambial dele FORA das reservas;
            # a dos bancos e de outra entidade e entra so como contraparte. Nao vira
            # arvore: a fonte nao publica total das tres, e somar por conta propria
            # seria inventar um agregado.
            "swap":     swap,
            "reservas_arvore": arvore,
            "intervencoes":    interv,
        }
    except Exception as exc:
        print(f"  Aviso: erro em cmb_reservas_bc -- {exc}")
        return {}


def _load_cambio_contratado() -> dict:
    """Câmbio contratado entre bancos e clientes — a fonte de fluxo cambial do relatório.

    Tabelas 13 (diária, desde set/2008) e 14 (mensal, desde 2011) dos Indicadores
    Econômicos Selecionados do BCB — ver o docstring de
    domain/db/brasil/bcb/cmb_cambio_contratado.py para o mapa código→série.

    Substituiu `cmb_fluxo_cambial` nesta aba em 2026-08-27, porque aquela tabela
    **não contém fluxo cambial**: o `total_saldo` dela vai de 81,0 a 82,9 ao longo
    de 307 meses e NUNCA troca de sinal, enquanto um saldo de fluxo cambial oscila
    em torno de zero (o dado real troca de sinal em 107 dos 216 meses em comum).
    A correlação entre os dois é 0,05 e as magnitudes diferem ~60x. Os códigos SGS
    24352/24363/24364/24369/24370/24371 que aquele script usa não são o que o
    docstring dele afirma — e ele próprio já registrava a dúvida ("confirmar
    unidade na BCB SGS"). Ver analytics/brasil/exchange_rate/CLAUDE.md.

    Aqui as identidades fecham EXATAMENTE (resíduo 0,000 em 4.501 dias):
        saldo_total     = saldo_comercial + saldo_financeiro
        saldo_comercial = exportação − importação
        exportação      = ACC + PA + demais
        saldo_financeiro = compras − vendas
        saldo_fin_det   = serviços + rendas + capitais BR + capitais estrangeiros

    As séries diárias são somadas em meses; o mês em curso é DESCARTADO em vez de
    somado pela metade (regra de período incompleto, ver analytics/metric_layers.md).
    """
    try:
        wide = _pivot("macro_brasil", "cmb_cambio_contratado")
        if wide is None:
            return {}

        diarias = ["cc_saldo_total", "cc_saldo_comercial", "cc_export_total", "cc_export_acc",
                   "cc_export_pa", "cc_export_outros", "cc_import_total",
                   "cc_fin_saldo", "cc_fin_compras", "cc_fin_vendas"]
        diarias = [c for c in diarias if c in wide.columns]
        mensais = ["cc_fin_saldo_det", "cc_fin_servicos", "cc_fin_rendas",
                   "cc_fin_cap_bras", "cc_fin_cap_ext"]
        mensais = [c for c in mensais if c in wide.columns]

        mensal = wide[diarias].resample("MS").sum(min_count=1)

        # O mês em curso só entra se a série alcançou o último DIA ÚTIL dele. Sem
        # isto, agosto com 15 pregões apareceria somado ao lado de meses de 22 —
        # o mesmo defeito de período incompleto corrigido em aggregateSum().
        # Feriado no último dia útil faz descartar um mês que estava completo:
        # erra para menos, que é o lado seguro.
        ultimo = wide[diarias].dropna(how="all").index.max()
        if ultimo is not None and ultimo < (ultimo + pd.offsets.BMonthEnd(0)):
            mensal = mensal.iloc[:-1]

        mensal = mensal / 1000.0  # USD MM -> USD Bi
        det = (wide[mensais] / 1000.0).reindex(mensal.index) if mensais else None

        out = {"dates": _dates(mensal.index)}
        for c in diarias:
            out[c] = _to_list(mensal[c])
        if det is not None:
            for c in mensais:
                out[c] = _to_list(det[c])
        out["ultimo_dia_diario"] = ultimo.strftime("%Y-%m-%d") if ultimo is not None else None
        return out
    except Exception as exc:
        print(f"  Aviso: erro em cmb_cambio_contratado — {exc}")
        return {}


def _load_interbancario() -> dict:
    """Volume interbancário de câmbio (T+1/T+2), diário em `cmb_ptax`, somado em meses.

    Mesma regra de mês incompleto de _load_cambio_contratado().
    """
    try:
        wide = _pivot("macro_brasil", "cmb_ptax")
        if wide is None or "fx_interbank_vol_t1" not in wide.columns:
            return {}
        cols = ["fx_interbank_vol_t1", "fx_interbank_vol_t2"]
        mensal = wide[cols].resample("MS").sum(min_count=1)
        ultimo = wide[cols].dropna(how="all").index.max()
        if ultimo is not None and ultimo < (ultimo + pd.offsets.BMonthEnd(0)):
            mensal = mensal.iloc[:-1]
        mensal = mensal / 1e9  # USD -> USD Bi (esta série vem em USD, não USD MM)
        return {
            "dates":     _dates(mensal.index),
            "vol_t1":    _to_list(mensal["fx_interbank_vol_t1"]),
            "vol_t2":    _to_list(mensal["fx_interbank_vol_t2"]),
            "vol_total": _to_list(mensal["fx_interbank_vol_t1"] + mensal["fx_interbank_vol_t2"]),
        }
    except Exception as exc:
        print(f"  Aviso: erro em cmb_ptax (volume interbancário) — {exc}")
        return {}


def _load_fluxo() -> dict:
    """ATENÇÃO — esta tabela NÃO contém fluxo cambial; ver _load_cambio_contratado().

    Mantida porque `agent_data.get_fx_snapshot()` ainda a consome, e retirá-la de lá
    é decisão de quem cuida do agente `cambio-analyst`. O relatório parou de usá-la
    em 2026-08-27. A tabela e o script `domain/db/brasil/bcb/cmb_fluxo_cambial.py`
    precisam de uma decisão: corrigir os códigos SGS ou dropar.
    """
    try:
        wide = _pivot("macro_brasil", "cmb_fluxo_cambial")
        if wide is None:
            return {}
        wide = wide / 1000.0  # USD MM -> USD Bi
        if "comercial_entrada" in wide.columns and "comercial_saida" in wide.columns:
            wide["comercial_saldo"] = wide["comercial_entrada"] - wide["comercial_saida"]
        return {
            "dates":             _dates(wide.index),
            "total_saldo":       _col(wide, "total_saldo"),
            "total_entrada":     _col(wide, "total_entrada"),
            "total_saida":       _col(wide, "total_saida"),
            "comercial_saldo":   _col(wide, "comercial_saldo"),
            "comercial_entrada": _col(wide, "comercial_entrada"),
            "comercial_saida":   _col(wide, "comercial_saida"),
            "financeiro_saldo":  _col(wide, "financeiro_saldo"),
        }
    except Exception as exc:
        print(f"  Aviso: erro em cmb_fluxo_cambial — {exc}")
        return {}


def _load_bop() -> dict:
    """Balanço de Pagamentos — séries brutas (SGS) + agregados derivados.

    Os agregados abaixo foram cross-checados contra o quadro condensado
    oficial do BCB ("Financiamento Externo") em 5 meses (Jan-Mai/2026) —
    ver docstring de domain/db/brasil/bcb/cmb_balanco_pagmt.py para as
    fórmulas e a validação.

    Todas as séries de `cmb_balanco_pagmt` estão em USD MM na fonte —
    convertidas para USD Bi (/1000) para exibição no relatório.
    """
    try:
        wide = _pivot("macro_brasil", "cmb_balanco_pagmt")
        if wide is None:
            return {}
        wide = wide / 1000.0  # USD MM -> USD Bi

        # `lucros_reinvestidos` (SGS 22815) não tem dado publicado pelo BCB
        # entre 1999-01 e 2009-12 (confirmado direto na API: 404 "Value(s)
        # not found" para essa janela — lacuna real da fonte, não do
        # pipeline). Sem o fillna, a soma abaixo propagaria NaN pela década
        # inteira e "Lucros e Dividendos" desapareceria do gráfico de
        # composição nesse período mesmo com remetidos/carteira presentes.
        wide["lucros_reinvestidos"] = wide["lucros_reinvestidos"].fillna(0)

        # Convenção de sinal do lado Ativos/Derivativos/Reserva invertida
        # (2026-07, pedido do usuário) — para ler a Conta Financeira como
        # "contraparte" da Conta Corrente com a MESMA regra em toda parte:
        # negativo = SAÍDA de USD do país, positivo = ENTRADA de USD (igual
        # à leitura natural de Conta Corrente: déficit/negativo = saída).
        #
        # No BPM6 publicado pelo BCB, positivo em Ativos = aumento de ativo
        # no exterior = SAÍDA de USD (o oposto do que queremos aqui) — negado.
        # Passivos JÁ segue a regra desejada sem alteração: positivo em
        # Passivos = aumento de passivo externo = ENTRADA de USD (ex: IDE
        # ingressando) — por isso Passivos NÃO é invertido (ao contrário de
        # uma tentativa anterior nesta sessão, desfeita: inverter Passivos
        # estava errado, o lado que precisava de ajuste era Ativos).
        # Derivativos segue a mesma convenção de Ativos (negativo hoje =
        # entrada, por instrução do usuário) — negado. Ativos de Reserva:
        # quando o BC aumenta reservas (positivo hoje), esse USD é absorvido
        # pelo BC em vez de ficar disponível/circulando — ou seja, um
        # aumento de reservas "remove" parte do que entrou, mesma direção de
        # Ativos — negado.
        #
        # `conta_financeira` (total oficial) também é invertido para
        # continuar batendo com a soma dos 4 componentes já ajustados
        # (identidade original: conta_financeira = ativos_ativos - passivos +
        # derivativos + reserva; invertendo ativos/derivativos/reserva e
        # deixando passivos como está, a identidade só fecha se
        # conta_financeira também for invertido — confirmado numericamente
        # contra a API para Jan-Mai/2026).
        #
        # Como as fórmulas abaixo são combinações lineares, invertê-las aqui
        # já propaga corretamente para investimentos_ativos sem reescrever
        # nenhuma fórmula. Só a tabela `wide` (usada apenas neste relatório)
        # é afetada — `macro_brasil.cmb_balanco_pagmt` continua com os
        # valores exatamente como o BCB publica.
        _INVERTED_COLS = ["idp_exterior", "portfolio_ativos", "outros_inv_ativos",
                           "acoes_ativos", "fundos_ativos", "titulos_ativos_cp", "titulos_ativos_lp",
                           "derivativos", "ativos_reserva", "conta_financeira"]
        for col in _INVERTED_COLS:
            wide[col] = -wide[col]

        # PIB mensal em USD (BCB SGS 4385, `atv_pib_usd` — tabela separada de
        # `cmb_balanco_pagmt`) — usado pelo botão "% PIB" da aba no relatório
        # para normalizar as séries acima. Reindexado ao índice de datas do
        # BOP (mesma granularidade mensal) para alinhar 1:1 nos dois lados.
        gdp_wide = _pivot("macro_brasil", "atv_pib_usd")
        gdp_usd_bi = None
        if gdp_wide is not None and "pib_usd" in gdp_wide.columns:
            gdp_usd_bi = (gdp_wide["pib_usd"] / 1000.0).reindex(wide.index)

        out = {"dates": _dates(wide.index)}
        out["gdp_usd_bi"] = _to_list(gdp_usd_bi) if gdp_usd_bi is not None else None
        for name in [
            "conta_corrente", "balanca_comercial_servicos", "exportacao_bens", "importacao_bens",
            "mercadorias_gerais", "mercadorias_gerais_export", "mercadorias_gerais_import",
            "merchanting", "ouro_nao_monetario", "ouro_nao_monetario_export", "ouro_nao_monetario_import",
            "servicos", "viagens", "transportes", "aluguel_equipamentos",
            "renda_primaria", "remuneracao_empregados", "renda_secundaria", "conta_capital",
            "conta_financeira", "idp_exterior", "ide_saidas", "investimento_direto_liquido", "idp_ingressos",
            "portfolio_ativos", "outros_inv_ativos", "portfolio_passivos", "acoes_passivos", "fundos_passivos",
            "acoes_ativos", "fundos_ativos", "titulos_ativos_cp", "titulos_ativos_lp",
            "titulos_dom", "titulos_externo_cp", "titulos_externo_lp",
            "outros_inv_passivos", "emprestimos_cp_passivos", "emprestimos_lp_passivos",
            "derivativos", "ativos_reserva", "erros_omissoes",
        ]:
            out[name] = _col(wide, name)

        # Agregados validados contra o quadro oficial "Financiamento Externo"
        out["demais_servicos"] = _to_list(
            wide["servicos"] - wide["viagens"] - wide["transportes"] - wide["aluguel_equipamentos"]
        )
        out["juros"] = _to_list(
            wide["juros_intercompanhia"] + wide["juros_carteira_externo"]
            + wide["juros_carteira_domestico"] + wide["juros_outros_investimentos"] + wide["renda_reservas"]
        )
        out["lucros_dividendos"] = _to_list(
            wide["lucros_remetidos"] + wide["lucros_reinvestidos"] + wide["lucros_dividendos_carteira"]
        )
        out["investimentos_ativos"] = _to_list(
            wide["idp_exterior"] + wide["portfolio_ativos"] + wide["outros_inv_ativos"]
        )
        out["investimentos_passivos"] = _to_list(
            wide["investimento_direto_liquido"] + wide["portfolio_passivos"] + wide["outros_inv_passivos"]
        )
        out["acoes_totais"] = _to_list(wide["acoes_passivos"] + wide["fundos_passivos"])
        out["acoes_fundos_ativos"] = _to_list(wide["acoes_ativos"] + wide["fundos_ativos"])
        out["emprestimos_titulos_lp_externo"] = _to_list(
            wide["titulos_externo_lp"] + wide["emprestimos_lp_passivos"]
        )
        out["emprestimos_titulos_cp_externo"] = _to_list(
            wide["titulos_externo_cp"] + wide["emprestimos_cp_passivos"]
        )
        # Residual de "Outros Investimentos — Passivos" além dos dois empréstimos
        # publicados (moeda e depósitos, créditos comerciais, outros passivos):
        # os dois empréstimos NÃO fecham a conta (resíduo médio de 1,4 e máximo de
        # 16,7 USD Bi), então o ramo precisa da linha de resto para somar ao pai —
        # mesma construção de `demais_servicos`.
        out["demais_outros_passivos"] = _to_list(
            wide["outros_inv_passivos"] - wide["emprestimos_cp_passivos"] - wide["emprestimos_lp_passivos"]
        )
        out["demais_passivos"] = _to_list(
            wide["portfolio_passivos"] + wide["outros_inv_passivos"]
            - wide["acoes_passivos"] - wide["fundos_passivos"] - wide["titulos_dom"]
            - wide["titulos_externo_lp"] - wide["emprestimos_lp_passivos"]
            - wide["titulos_externo_cp"] - wide["emprestimos_cp_passivos"]
        )
        return out
    except Exception as exc:
        print(f"  Aviso: erro em cmb_balanco_pagmt — {exc}")
        return {}


_COMEX_PAISES = ["china", "eua", "argentina", "alemanha"]


def _load_comex_pais() -> dict:
    """Balança de Bens por país/bloco parceiro — Comex Stat (MDIC), NÃO BPM6.

    Metodologia de comércio geral (SISCOMEX) — ver docstring de
    connectors/comexstat.py e domain/db/brasil/mdic/cmb_comex_pais.py para a
    diferença estrutural em relação a `cmb_balanco_pagmt.mercadorias_gerais`.
    `saldo_mundo` (total Comex Stat) é o total desta MESMA fonte, não o total
    da BOP — os dois não fecham exatamente um com o outro, de propósito.

    A fonte já vem em USD (não USD MM, diferente de cmb_balanco_pagmt) —
    convertida para USD Bi (/1e9) para exibição.
    """
    try:
        wide = _pivot("macro_brasil", "cmb_comex_pais")
        if wide is None:
            return {}
        wide = wide / 1e9  # USD -> USD Bi

        # Além do saldo, a fonte publica exportação e importação SEPARADAS por
        # parceiro — detalhe que a Balança de Bens do BPM6 não abre. A árvore
        # da aba usa os três níveis (total -> parceiro -> exportação/importação),
        # por isso os dois lados brutos vão no payload, não só a diferença.
        out = {"dates": _dates(wide.index)}
        saldo_paises = export_paises = import_paises = None
        for pais in _COMEX_PAISES:
            export, import_ = wide[f"{pais}_export"], wide[f"{pais}_import"]
            saldo = export - import_
            out[f"saldo_{pais}"] = _to_list(saldo)
            out[f"export_{pais}"] = _to_list(export)
            out[f"import_{pais}"] = _to_list(import_)
            saldo_paises = saldo if saldo_paises is None else saldo_paises + saldo
            export_paises = export if export_paises is None else export_paises + export
            import_paises = import_ if import_paises is None else import_paises + import_

        export_mundo, import_mundo = wide["mundo_export"], wide["mundo_import"]
        out["saldo_demais"] = _to_list(export_mundo - import_mundo - saldo_paises)
        out["export_demais"] = _to_list(export_mundo - export_paises)
        out["import_demais"] = _to_list(import_mundo - import_paises)
        out["saldo_mundo"] = _to_list(export_mundo - import_mundo)
        out["export_mundo"] = _to_list(export_mundo)
        out["import_mundo"] = _to_list(import_mundo)
        return out
    except Exception as exc:
        print(f"  Aviso: erro em cmb_comex_pais — {exc}")
        return {}


_COMEX_FATOR_AGREGADO_CATEGORIAS = ["basicos", "semimanufaturados", "manufaturados", "demais"]


def _load_comex_fator_agregado() -> dict:
    """Balança de Bens por Fator Agregado — Comex Stat (MDIC), NÃO BPM6.

    Diferente de _load_comex_pais(), as 4 categorias aqui JÁ cobrem 100% do
    total (toda transação cai em exatamente 1 dos 6 códigos oficiais de
    Fator Agregado, agrupados em basicos/semimanufaturados/manufaturados/
    demais — ver docstring de cmb_comex_fator_agregado.py) — não precisa de
    uma série "mundo" + residual separada, o total é a soma direta das 4.

    A fonte já vem em USD (não USD MM) — convertida para USD Bi (/1e9).
    """
    try:
        wide = _pivot("macro_brasil", "cmb_comex_fator_agregado")
        if wide is None:
            return {}
        wide = wide / 1e9  # USD -> USD Bi

        # "demais" (transações especiais/consumo de bordo/reexportação/não
        # classificado) tem meses SEM nenhuma transação — sobretudo do lado
        # import (só 51 dos 354 meses têm alguma linha) — ausência = zero
        # real, não dado faltante. Sem o fillna, NaN propagaria pela
        # subtração export−import e pela soma do total aditivo, criando
        # buracos onde as outras 3 categorias têm dado completo.
        wide = wide.fillna(0)

        # Mesma abertura exportação/importação de _load_comex_pais() — aqui o
        # total é a soma direta das 4 categorias (partição exata), então não há
        # "mundo" separado nem residual.
        out = {"dates": _dates(wide.index)}
        saldo_total = export_total = import_total = None
        for cat in _COMEX_FATOR_AGREGADO_CATEGORIAS:
            export, import_ = wide[f"{cat}_export"], wide[f"{cat}_import"]
            saldo = export - import_
            out[f"saldo_{cat}"] = _to_list(saldo)
            out[f"export_{cat}"] = _to_list(export)
            out[f"import_{cat}"] = _to_list(import_)
            saldo_total = saldo if saldo_total is None else saldo_total + saldo
            export_total = export if export_total is None else export_total + export
            import_total = import_ if import_total is None else import_total + import_

        out["saldo_total"] = _to_list(saldo_total)
        out["export_total"] = _to_list(export_total)
        out["import_total"] = _to_list(import_total)
        return out
    except Exception as exc:
        print(f"  Aviso: erro em cmb_comex_fator_agregado — {exc}")
        return {}


_COMEX_PRODUTOS = ["soja", "petroleo", "minerio_ferro", "carnes", "cafe"]


def _load_comex_produto() -> dict:
    """Balança de Bens por produto específico — Comex Stat (MDIC), NÃO BPM6.

    Mesmo padrão de _load_comex_pais(): as 5 séries de produto NÃO cobrem
    100% do total (são recortes SH específicos, não uma partição) — precisa
    de `mundo_export`/`mundo_import` (total geral) para calcular
    `saldo_demais` como residual.

    A fonte já vem em USD (não USD MM) — convertida para USD Bi (/1e9).
    """
    try:
        wide = _pivot("macro_brasil", "cmb_comex_produto")
        if wide is None:
            return {}
        wide = wide / 1e9  # USD -> USD Bi

        # Import de commodities que o Brasil majoritariamente EXPORTA tem
        # meses sem nenhuma transação (ex: minerio_ferro_import só em 283
        # dos 354 meses, petroleo_export em 321) — ausência = zero real, não
        # dado faltante (mesmo caso de "demais" em
        # _load_comex_fator_agregado()). mundo_export/import são sempre
        # completos (354/354), então o fillna só afeta as séries esparsas.
        wide = wide.fillna(0)

        # Mesma abertura exportação/importação de _load_comex_pais().
        out = {"dates": _dates(wide.index)}
        saldo_produtos = export_produtos = import_produtos = None
        for prod in _COMEX_PRODUTOS:
            export, import_ = wide[f"{prod}_export"], wide[f"{prod}_import"]
            saldo = export - import_
            out[f"saldo_{prod}"] = _to_list(saldo)
            out[f"export_{prod}"] = _to_list(export)
            out[f"import_{prod}"] = _to_list(import_)
            saldo_produtos = saldo if saldo_produtos is None else saldo_produtos + saldo
            export_produtos = export if export_produtos is None else export_produtos + export
            import_produtos = import_ if import_produtos is None else import_produtos + import_

        export_mundo, import_mundo = wide["mundo_export"], wide["mundo_import"]
        out["saldo_demais"] = _to_list(export_mundo - import_mundo - saldo_produtos)
        out["export_demais"] = _to_list(export_mundo - export_produtos)
        out["import_demais"] = _to_list(import_mundo - import_produtos)
        out["saldo_mundo"] = _to_list(export_mundo - import_mundo)
        out["export_mundo"] = _to_list(export_mundo)
        out["import_mundo"] = _to_list(import_mundo)
        return out
    except Exception as exc:
        print(f"  Aviso: erro em cmb_comex_produto — {exc}")
        return {}


def _load_ptax() -> dict:
    try:
        wide = _pivot("macro_brasil", "cmb_ptax")
        if wide is None:
            return {}
        vol_total = None
        if "fx_interbank_vol_t1" in wide.columns and "fx_interbank_vol_t2" in wide.columns:
            vol_total = wide["fx_interbank_vol_t1"].fillna(0) + wide["fx_interbank_vol_t2"].fillna(0)
        return {
            "dates":       _dates(wide.index),
            "ptax_venda":  _col(wide, "ptax_venda"),
            "vol_t1":      _col(wide, "fx_interbank_vol_t1"),
            "vol_t2":      _col(wide, "fx_interbank_vol_t2"),
            "vol_total":   _to_list(vol_total) if vol_total is not None else None,
        }
    except Exception as exc:
        print(f"  Aviso: erro em cmb_ptax — {exc}")
        return {}


def _load_termos() -> dict:
    try:
        wide = _pivot("macro_brasil", "cmb_termos_troca")
        if wide is None:
            return {}
        return {
            "dates":                  _dates(wide.index),
            "termos_de_troca_funcex": _col(wide, "termos_de_troca_funcex"),
        }
    except Exception as exc:
        print(f"  Aviso: erro em cmb_termos_troca — {exc}")
        return {}


# ── Abas de modelo ────────────────────────────────────────────────────────────

def _empty_models() -> dict[str, dict | None]:
    """Os três marcadores de modelo, todos vazios. Sempre passados ao
    render_report() — mesmo com include_models=False — porque o template
    declara `const PPP_DATA = /*PPP_DATA*/;`: marcador não substituído é erro
    de sintaxe, não aba vazia."""
    return {"PPP_DATA": None, "FXATTR_DATA": None, "RIDGE_DATA": None}


def _load_models() -> dict:
    """Payloads das três abas de modelo (Equilíbrio PPP / FX Attribution /
    Ridge), fundidas neste relatório em 2026-08.

    Bem mais caro que os `_load_*()` acima: busca o CPI americano no FRED ao
    vivo, roda a validação cruzada walk-forward do Ridge e reestima a janela
    móvel. Mesmo padrão de degradação do resto do arquivo — cada payload é
    try/exceptado por conta própria e volta como None, o que o template
    renderiza como a mensagem "sem dados embutidos" daquela aba.
    """
    from analytics.brasil.exchange_rate.models import (
        fx_attribution_model,
        ppp_equilibrium,
        ridge_deviation_model,
    )

    payloads = _empty_models()

    try:
        print("Carregando o núcleo PPP (MySQL + FRED)...")
        df = ppp_equilibrium.load_data()
        payloads["PPP_DATA"] = ppp_equilibrium.build_payload(df)
    except Exception as exc:
        print(f"  Aviso: aba Equilíbrio PPP sem dados — {exc}")

    try:
        payloads["FXATTR_DATA"] = fx_attribution_model.build_dashboard_payload()
    except Exception as exc:
        print(f"  Aviso: aba FX Attribution sem dados — {exc}")

    try:
        print("Estimando o modelo Ridge (walk-forward + janela móvel)...")
        payloads["RIDGE_DATA"] = ridge_deviation_model.build_dashboard_payload()
    except Exception as exc:
        print(f"  Aviso: aba Ridge sem dados — {exc}")

    return payloads


# ── Entry point ───────────────────────────────────────────────────────────────

def run(output: str = "reports/brasil/FX Report.html", include_models: bool = True) -> None:
    """Gera o relatório HTML de fundamentos cambiais.

    Lê tabelas de macro_brasil e macro_international, injeta os dados no
    template report.html e salva um único arquivo HTML autocontido.

    Args:
        output: caminho de saída. Default "reports/brasil/FX Report.html".
        include_models: se False, pula as três abas de modelo (nada de FRED
            nem de fits) e elas saem com a mensagem "sem dados embutidos".
    """
    print("Carregando dados de macro_brasil / macro_international...")
    report_data = {
        "generated_at": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "ptax":            _load_ptax(),
        # `diferenciais` saiu do payload em 2026-09-01, com a secao Diferenciais de
        # Juros (pedido do usuario) -- eram 39 KB para tres graficos que nao existem
        # mais. `_load_diferenciais()` FICA: agent_data.py o importa para montar o
        # snapshot do subagente cambio-analyst, que nao passa por este payload.
        "reer":            _load_reer(),
        "cot_fx":          _load_cot_fx(),
        "bcb_positioning": _load_bcb_positioning(),
        # `fluxo` (cmb_fluxo_cambial) saiu do payload em 2026-08-27 — não é fluxo
        # cambial, ver o docstring de _load_fluxo(). A aba passou a ler
        # cmb_cambio_contratado, que é a fonte que o BCB publica para isso.
        "cambio_contratado": _load_cambio_contratado(),
        "interbancario":     _load_interbancario(),
        "bop":             _load_bop(),
        "comex_pais":      _load_comex_pais(),
        "comex_fator_agregado": _load_comex_fator_agregado(),
        "comex_produto":   _load_comex_produto(),
        "termos":          _load_termos(),
    }

    models = _load_models() if include_models else _empty_models()
    out = render_report(_TEMPLATE, report_data, output, extra_markers=models)
    print(f"Relatório salvo: {out}")
