"""
Gerador do relatório HTML de fundamentos cambiais.

Lê tabelas de macro_brasil e macro_international, injeta os dados no template
report.html e salva um único arquivo HTML autocontido em reports/fx_report.html.

Uso:
    uv run python -c "from analytics.exchange_rate.generate_report import run; run()"
"""

import json
from datetime import datetime
from pathlib import Path

import pandas as pd

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


def _load_cot_fx() -> dict:
    try:
        df = _fetch("macro_international", "cmb_cot_fx")
        if df is None:
            return {}
        df["value"] = df["value"].astype(float)
        brl = df[df["currency"] == "BRL"].copy()
        wide = brl.pivot(index="date", columns="name", values="value").sort_index()
        return {
            "dates":         _dates(wide.index),
            "lev_net":       _col(wide, "lev_net"),
            "lev_long":      _col(wide, "lev_long"),
            "lev_short":     _col(wide, "lev_short"),
            "open_interest": _col(wide, "open_interest"),
        }
    except Exception as exc:
        print(f"  Aviso: erro em cmb_cot_fx — {exc}")
        return {}


def _load_bcb_positioning() -> dict:
    """Reservas internacionais, posição de câmbio (BCB/bancos) e intervenções.

    Alimenta a aba "BCB Positioning". `cmb_reservas_bc` mistura frequências
    (mensal para reservas/swap, diária para reservas_liquidity/intervenções)
    numa única tabela — pivotar tudo junto criaria um índice de datas comum
    onde a maioria das linhas mensais ficaria cercada de nulls (a série
    "quebraria" visualmente com connectgaps=false). Em vez disso, cada
    subgrupo abaixo pivota só suas próprias séries e carrega seu próprio
    eixo "dates".

    Todas as séries usadas aqui (reservas, ouro, swap, intervenções) estão em
    USD MM na fonte — convertidas para USD Bi (/1000) para exibição no
    relatório. `reserves_gold_volume` (troy oz) não é usada nesta função.
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

        return {
            "reserves": _subgroup(["reserves_liquidity_daily", "reserves_total_monthly"]),
            "gold":     _subgroup(["reserves_gold_usd"]),
            "swap":     _subgroup(["bcb_swap_cambial_position", "bank_fx_spot_position"]),
            "interventions": _subgroup([
                "bcb_intervention_spot",
                "bcb_intervention_forwards",
                "bcb_intervention_fx_loans_repos",
                "bcb_intervention_repo_lines",
            ]),
        }
    except Exception as exc:
        print(f"  Aviso: erro em cmb_reservas_bc — {exc}")
        return {}


def _load_fluxo() -> dict:
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

        out = {"dates": _dates(wide.index)}
        saldo_paises = None
        for pais in _COMEX_PAISES:
            saldo = wide[f"{pais}_export"] - wide[f"{pais}_import"]
            out[f"saldo_{pais}"] = _to_list(saldo)
            saldo_paises = saldo if saldo_paises is None else saldo_paises + saldo

        saldo_mundo = wide["mundo_export"] - wide["mundo_import"]
        out["saldo_demais"] = _to_list(saldo_mundo - saldo_paises)
        out["saldo_mundo"] = _to_list(saldo_mundo)
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

        out = {"dates": _dates(wide.index)}
        saldo_total = None
        for cat in _COMEX_FATOR_AGREGADO_CATEGORIAS:
            saldo = wide[f"{cat}_export"] - wide[f"{cat}_import"]
            out[f"saldo_{cat}"] = _to_list(saldo)
            saldo_total = saldo if saldo_total is None else saldo_total + saldo

        out["saldo_total"] = _to_list(saldo_total)
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

        out = {"dates": _dates(wide.index)}
        saldo_produtos = None
        for prod in _COMEX_PRODUTOS:
            saldo = wide[f"{prod}_export"] - wide[f"{prod}_import"]
            out[f"saldo_{prod}"] = _to_list(saldo)
            saldo_produtos = saldo if saldo_produtos is None else saldo_produtos + saldo

        saldo_mundo = wide["mundo_export"] - wide["mundo_import"]
        out["saldo_demais"] = _to_list(saldo_mundo - saldo_produtos)
        out["saldo_mundo"] = _to_list(saldo_mundo)
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


# ── Entry point ───────────────────────────────────────────────────────────────

def run(output: str = "reports/fx_report.html") -> None:
    """Gera o relatório HTML de fundamentos cambiais.

    Lê tabelas de macro_brasil e macro_international, injeta os dados no
    template report.html e salva um único arquivo HTML autocontido.

    Args:
        output: caminho de saída. Default "reports/fx_report.html".
    """
    print("Carregando dados de macro_brasil / macro_international...")
    report_data = {
        "generated_at": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "ptax":            _load_ptax(),
        "diferenciais":    _load_diferenciais(),
        "reer":            _load_reer(),
        "cot_fx":          _load_cot_fx(),
        "bcb_positioning": _load_bcb_positioning(),
        "fluxo":           _load_fluxo(),
        "bop":             _load_bop(),
        "comex_pais":      _load_comex_pais(),
        "comex_fator_agregado": _load_comex_fator_agregado(),
        "comex_produto":   _load_comex_produto(),
        "termos":          _load_termos(),
    }

    template = _TEMPLATE.read_text(encoding="utf-8")
    payload = json.dumps(report_data, ensure_ascii=False, default=str)
    html = template.replace("/*REPORT_DATA*/", f"const REPORT_DATA = {payload};")

    out = Path(output)
    out.parent.mkdir(exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print(f"Relatório salvo: {out.resolve()}")
