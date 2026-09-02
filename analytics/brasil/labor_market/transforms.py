"""
Variantes de exibicao das series do Panorama de Mercado de Trabalho -- so
visualizacao (sem STL/dessazonalizacao, deflacao ou %PIB, ao contrario de
analytics/brasil/fiscal_policy/transforms.py, que resolve um problema mais
amplo). Reusa pct_change()/pp_diff() de la em vez de duplicar.

Duas familias de unidade nas series de PNAD:
  - "rate" (True): series ja em % (taxa_desocupacao, taxa_participacao,
    taxa_informalidade, taxa_subutil_*, nivel_ocupacao/desocupacao,
    pct_desalentados, pct_contribuintes_previdencia) -- variacao em PONTOS
    PERCENTUAIS (pp_diff), nao em variacao percentual da taxa (pct_change
    daria "taxa caiu 6,7%" quando na verdade caiu de 7,5% para 7,0%, ou seja
    -0,5 p.p. -- unidade errada para uma serie que ja e uma razao).
  - "rate=False": niveis em mil pessoas (ocup_*, ocupado/desocupado/
    fora_da_forca_trabalho, subutil_*), R$/mes (rend_*) ou R$ milhoes/mes
    (massa_*) -- variacao percentual normal (pct_change).

FREQUENCIA (2026-08-27, a pedido do usuario -- "como temos dados mensais e
trimestrais, separe a visualizacao"): cada serie de PNAD ganha as variantes nas
DUAS frequencias, chaveadas "{freq}__{metrica}" (o lado JS monta essa chave
concatenando os seletores da tabela). mt_pnad e mensal (trimestre movel) e
existe nas duas; mt_pnad_trimestral e trimestral e existe so em `trimestral__*`
-- e e isso que permite ao JS esconder a linha em vez de imprimir uma fila de
travessoes na visao mensal.

O alinhamento entre as duas nao e suposto, foi MEDIDO (2026-08-27): a data de
mt_pnad_trimestral e o PRIMEIRO mes do trimestre (2026-04 = 2o tri) e a de
mt_pnad e o ULTIMO mes do trimestre movel, entao o trimestre fechado Abr-Jun
esta em mt_pnad sob 2026-06. Reconstruindo o total nacional da taxa de
desocupacao a partir dos cortes por sexo de mt_pnad_trimestral (ponderando
populacao x taxa de participacao) e comparando com mt_pnad: MAE 0,038 p.p. em
57 trimestres (max 0,097) contra o ultimo mes, e 0,499 p.p. (max 1,426) contra
o primeiro -- ou seja, o casamento pelo ultimo mes e exato a menos do
arredondamento de 1 decimal da fonte, e o pelo primeiro esta 13x pior. Por isso
to_quarterly() colhe os meses 3/6/9/12 e REDATA para o 1o mes do trimestre.

Var. curto prazo (m/m e t/t) foi REMOVIDA em 2026-08-27, a pedido explicito do
usuario ("pode retirar a metrica de curto prazo de todos os graficos").

Terceira familia, da aba "Emprego Formal" (CAGED):
  - FLUXO (mt_caged_setor/_uf/_salario -- saldo/admissoes/desligamentos):
    Mensal / Acum. 12m / Acum. no ano. Deliberadamente SEM variacao percentual
    -- saldo e fluxo liquido e cruza zero (as 22 secoes CNAE cruzam, e o a/a %
    do saldo nacional chega a 696%), entao pct_change ali nao e uma leitura
    ruim, e ruido numerico. Acumular e como o proprio MTE publica.
  - ESTOQUE (mt_caged, BCB): Nivel / Var. Mensal (diferenca em pessoas, que e
    justamente o saldo) / Var. Anual (%). Estoque e sempre positivo, entao a
    variacao percentual e valida aqui.
"""
from analytics.brasil.fiscal_policy.transforms import pct_change, pp_diff

# Mes que fecha o trimestre -> mes que ABRE o mesmo trimestre (a convencao de
# data de mt_pnad_trimestral). Ver a medicao na docstring do modulo.
_FECHA_PARA_ABRE = {3: "01", 6: "04", 9: "07", 12: "10"}


def _diff_fn(rate: bool):
    return pp_diff if rate else pct_change


def to_quarterly(dates: list[str], values: list) -> tuple[list[str], list]:
    """Serie mensal de mt_pnad -> serie trimestral na convencao de data de
    mt_pnad_trimestral (1o mes do trimestre). Colhe so os meses que FECHAM um
    trimestre (3/6/9/12), porque a observacao de mt_pnad e um trimestre movel
    rotulado pelo seu ultimo mes -- ver a medicao na docstring do modulo."""
    out_d, out_v = [], []
    for d, v in zip(dates, values):
        abre = _FECHA_PARA_ABRE.get(int(d[5:7]))
        if abre is None:
            continue
        out_d.append(f"{d[:4]}-{abre}-01")
        out_v.append(v)
    return out_d, out_v


def variants_pnad_mensal(dates: list[str], values: list, rate: bool) -> dict:
    """mt_pnad: existe nas duas frequencias. Lag 12 no mensal, lag 4 no
    trimestral -- os dois sao "mesmo periodo um ano antes"."""
    diff = _diff_fn(rate)
    qd, qv = to_quarterly(dates, values)
    return {
        "mensal__level":     {"dates": dates, "values": values},
        "mensal__yoy":       {"dates": dates, "values": diff(values, 12)},
        "trimestral__level": {"dates": qd, "values": qv},
        "trimestral__yoy":   {"dates": qd, "values": diff(qv, 4)},
    }


def variants_pnad_trimestral(dates: list[str], values: list, rate: bool) -> dict:
    """mt_pnad_trimestral: so trimestral. A AUSENCIA das chaves `mensal__*` e o
    que faz o JS esconder a linha na visao mensal (em vez de imprimir "--")."""
    diff = _diff_fn(rate)
    return {
        "trimestral__level": {"dates": dates, "values": values},
        "trimestral__yoy":   {"dates": dates, "values": diff(values, 4)},
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


def variants_caged_estoque(dates: list[str], values: list,
                           total: dict | None = None,
                           desde: str | None = None) -> dict:
    """Estoque de vinculos formais (mt_caged, BCB). `mom_diff` (diferenca em
    pessoas) e a leitura de fluxo desta serie -- e o que aproxima o saldo do
    microdado. `yoy` em % e valido porque estoque nunca cruza zero.

    `contrib_yy` e a decomposicao da variacao anual, em pontos percentuais:

        contrib_i(t) = [ S_i(t) - S_i(t-12) ] / S_total(t-12) * 100

    O denominador e o estoque TOTAL de 12 meses atras, o mesmo dos irmaos --
    e por isso que as contribuicoes somam o `yoy` do total, e por isso que
    esta variante precisa de `total` de fora (as outras tres so olham a
    propria serie). Na linha do total, `contrib_yy` == `yoy` por construcao.

    `total` e um dict {data: nivel}, NAO uma lista: as 6 sub-series do estoque
    comecam em 2007-01 e as 8 restantes em 1992-01, entao casar por posicao
    pegaria o denominador de outro mes -- sem lancar excecao nenhuma.

    `desde` e a primeira data (ISO) em que a arvore fecha; antes dela as partes
    nao somam o pai e uma barra empilhada mentiria (ver
    caged_tab._primeiro_aditivo)."""
    diffs = [None] * len(values)
    for i in range(1, len(values)):
        a, b = values[i - 1], values[i]
        if a is not None and b is not None:
            diffs[i] = round(float(b) - float(a))

    contrib = [None] * len(values)
    if total is not None:
        for i in range(12, len(values)):
            d, d12 = dates[i], dates[i - 12]
            if desde is not None and d12 < desde:
                continue
            a, b, den = values[i - 12], values[i], total.get(d12)
            if a is None or b is None or den in (None, 0):
                continue
            contrib[i] = round(100.0 * (float(b) - float(a)) / float(den), 4)

    return {
        "level": {"dates": dates, "values": values},
        "mom_diff": {"dates": dates, "values": diffs},
        "yoy": {"dates": dates, "values": pct_change(values, 12)},
        "contrib_yy": {"dates": dates, "values": contrib},
    }
