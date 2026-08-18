"""
Variantes de exibicao (Nivel/Var. curto prazo/Var. anual) para as series de
mt_pnad (mensal/trimestre movel) e mt_pnad_trimestral (trimestral) -- v1 do
Panorama de Mercado de Trabalho, so visualizacao (sem STL/dessazonalizacao,
deflacao ou %PIB -- ao contrario de analytics/fiscal_policy/transforms.py, que
resolve um problema mais amplo). Reusa pct_change()/pp_diff() de la em vez de
duplicar.

Duas familias de serie, unidades diferentes:
  - "rate" (True): series ja em % (taxa_desocupacao, taxa_participacao,
    taxa_informalidade, taxa_subutil_*, nivel_ocupacao/desocupacao,
    pct_desalentados, pct_contribuintes_previdencia) -- variacao em PONTOS
    PERCENTUAIS (pp_diff), nao em variacao percentual da taxa (pct_change
    daria "taxa caiu 6,7%" quando na verdade caiu de 7,5% para 7,0%, ou seja
    -0,5 p.p. -- unidade errada para uma serie que ja e uma razao).
  - "rate=False": niveis em milhares de pessoas (ocup_*, forca_*,
    subutil_subocupado_horas/forca_potencial/desalentado) ou R$
    (rend_*, massa_*) -- variacao percentual normal (pct_change).

mt_pnad (mensal/trimestre movel): curto prazo = m/m (lag 1), longo = a/a
(lag 12). mt_pnad_trimestral (trimestral "cheia", ver docstring do script de
ingestao): curto prazo = t/t (lag 1), longo = a/a (lag 4).

Terceira familia, adicionada em 2026-08 com a aba "Emprego Formal" (CAGED):
  - FLUXO (mt_caged_setor/_uf/_salario -- saldo/admissoes/desligamentos):
    Mensal / Acum. 12m / Acum. no ano. Deliberadamente SEM variacao percentual
    -- saldo e fluxo liquido e cruza zero (as 22 secoes CNAE cruzam, e o a/a %
    do saldo nacional chega a 696%), entao pct_change ali nao e uma leitura
    ruim, e ruido numerico. Acumular e como o proprio MTE publica.
  - ESTOQUE (mt_caged, BCB): Nivel / Var. Mensal (diferenca em pessoas, que e
    justamente o saldo) / Var. Anual (%). Estoque e sempre positivo, entao a
    variacao percentual e valida aqui.
"""
from analytics.fiscal_policy.transforms import pct_change, pp_diff


def _diff_fn(rate: bool):
    return pp_diff if rate else pct_change


def variants_mensal(dates: list[str], values: list, rate: bool) -> dict:
    diff = _diff_fn(rate)
    return {
        "level": {"dates": dates, "values": values},
        "mom": {"dates": dates, "values": diff(values, 1)},
        "yoy": {"dates": dates, "values": diff(values, 12)},
    }


def variants_trimestral(dates: list[str], values: list, rate: bool) -> dict:
    diff = _diff_fn(rate)
    return {
        "level": {"dates": dates, "values": values},
        "qoq": {"dates": dates, "values": diff(values, 1)},
        "yoy": {"dates": dates, "values": diff(values, 4)},
    }


# --- CAGED --------------------------------------------------------------------

def rolling_sum(values: list, window: int = 12) -> list:
    """Soma movel de `window` periodos. None ate a janela encher (nao soma
    parcial -- um "acumulado 12m" com 7 meses dentro nao e comparavel com um
    cheio, e plotar os dois na mesma linha esconderia isso)."""
    out, acc, buf = [], 0.0, []
    for v in values:
        x = 0.0 if v is None else float(v)
        buf.append(x)
        acc += x
        if len(buf) > window:
            acc -= buf.pop(0)
        out.append(round(acc) if len(buf) == window else None)
    return out


def ytd_sum(dates: list[str], values: list) -> list:
    """Acumulado no ano corrente, zerando em cada janeiro. Assume `dates`
    ordenado (o `_load_*` do generate_report.py ja ordena)."""
    out, acc, ano = [], 0.0, None
    for d, v in zip(dates, values):
        if d[:4] != ano:
            ano, acc = d[:4], 0.0
        acc += 0.0 if v is None else float(v)
        out.append(round(acc))
    return out


def variants_caged_fluxo(dates: list[str], por_metrica: dict) -> dict:
    """`por_metrica`: {"saldo": [...], "admissoes": [...], "desligamentos": [...]}.
    Devolve 9 variantes com chave "{metrica}__{periodo}" -- o lado JS monta essa
    chave concatenando os dois seletores da tabela (Metrica x Periodo)."""
    out = {}
    for metrica, values in por_metrica.items():
        out[f"{metrica}__mensal"] = {"dates": dates, "values": values}
        out[f"{metrica}__acum12m"] = {"dates": dates, "values": rolling_sum(values, 12)}
        out[f"{metrica}__acum_ano"] = {"dates": dates, "values": ytd_sum(dates, values)}
    return out


def variants_caged_periodo(dates: list[str], values: list) -> dict:
    """Variantes de uma serie de fluxo que NAO tem seletor de metrica (a tabela
    Nacional, onde saldo/admissoes/desligamentos sao linhas, nao opcoes) --
    mesmas 3 janelas, chaveadas so pelo periodo."""
    return {
        "mensal": {"dates": dates, "values": values},
        "acum12m": {"dates": dates, "values": rolling_sum(values, 12)},
        "acum_ano": {"dates": dates, "values": ytd_sum(dates, values)},
    }


def variants_caged_estoque(dates: list[str], values: list) -> dict:
    """Estoque de vinculos formais (mt_caged, BCB). `mom_diff` (diferenca em
    pessoas) e a leitura de fluxo desta serie -- e o que aproxima o saldo do
    microdado. `yoy` em % e valido porque estoque nunca cruza zero."""
    diffs = [None] * len(values)
    for i in range(1, len(values)):
        a, b = values[i - 1], values[i]
        if a is not None and b is not None:
            diffs[i] = round(float(b) - float(a))
    return {
        "level": {"dates": dates, "values": values},
        "mom_diff": {"dates": dates, "values": diffs},
        "yoy": {"dates": dates, "values": pct_change(values, 12)},
    }
