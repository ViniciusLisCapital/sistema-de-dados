"""
Monta o dataset da aba "Impulso" do Panorama de Credito.

A aba tem DUAS metricas de impulso, de fontes e conceitos diferentes, e elas
convivem de proposito -- a segunda e a resposta do proprio BCB a critica que ele
faz a primeira. As 3 primeiras tabelas usam a de Biggs et al., documentada logo
abaixo; a 4a usa a do BCB e esta documentada na secao "Fluxo financeiro e impulso
de credito NO CONCEITO DO BCB", no fim deste arquivo.

Metrica: impulso de credito no conceito de Biggs, Mayer & Pick (2009), na forma
aplicada ao Brasil pela serie do Blog do IBRE/FGV (Borca Jr., Furtado &
Barbosa-Filho, 2021) — a variacao do fluxo de credito de 12 meses, normalizado pelo
PIB nominal acumulado em 12 meses, em pontos percentuais do PIB:

    I_t = (Saldo_t - Saldo_{t-12}) / PIB12m_t
        - (Saldo_{t-12} - Saldo_{t-24}) / PIB12m_{t-12}

Le-se como "o credito novo desse ano pesou X p.p. do PIB a mais (ou a menos) do que
o credito novo do ano anterior" — o sinal indica aceleracao/desaceleracao da oferta
de recursos, nao o nivel dela.

## Duas frequencias, uma unica conta

"Anual (dez)" NAO e um calculo diferente de "Mensal (12m)": e a mesma serie lida
apenas em dezembro. Em dezembro, Saldo_t - Saldo_{t-12} ja e exatamente a variacao
do ano civil e PIB12m ja e exatamente o PIB do ano — entao a formula acima colapsa,
sem nenhum ajuste, na versao anual publicada pelo IBRE. As duas visoes sao
garantidamente consistentes por construcao, e nao por reconciliacao.

## Aditividade

A metrica e LINEAR no saldo e todas as linhas dividem o mesmo denominador (PIB), o
que torna a decomposicao por segmento exata: a soma dos filhos reproduz o pai sem
residuo. Verificado ao vivo contra a base — somando as 4 celulas recurso x segmento
contra o Total Geral, a discrepancia maxima em toda a serie e da ordem de 1e-4 p.p.
(ruido de ponto flutuante, nao erro de modelo). E por isso que as 3 tabelas desta aba
podem ser lidas como decomposicoes de verdade, e nao como aproximacoes.

Os totais de "Por Porte" e "Por Atividade Economica" sao SOMAS dos filhos (o BCB nao
publica um codigo SGS de total para esses dois cortes) — valido porque somar NIVEL em
R$ antes de aplicar a formula e legitimo, ao contrario de somar as p.p. resultantes.
Mesma regra ja documentada em saldo_tab.py.

## O que essa metrica NAO faz

E a segunda diferenca do estoque: nao remove da variacao do saldo os efeitos que nao
vem de concessao/pagamento — juros acruados, variacao cambial de contratos indexados
e baixas para prejuizo continuam dentro do numero. Essa e exatamente a critica que o
BCB faz a metrica de Biggs et al. no Estudo Especial 110/2021 ("Fluxo financeiro e
impulso de credito"), onde constroi uma versao limpa a partir do SCR. Aquela versao
depende de dados de juros/cambio/baixas que o BCB nao publica, e foi deliberadamente
deixada fora deste relatorio (decisao explicita do usuario, 2026-08) — o que esta
aqui e a medida do IBRE, exata mas conceitualmente contaminada, e nao a do BCB.

Implicacao pratica de leitura: uma linha pode marcar impulso positivo so por
repricing (juros altos inflando o estoque) sem nenhum credito novo. Vale para o total
e vale dentro de cada celula.

## Validacao

A replicacao bate com os numeros publicados pelo IBRE: 2016 total -5,3 (aqui -5,30) e
publicos -4,1 p.p. (aqui -4,13); 2020 publicos +2,8 p.p. (aqui +2,78); e a versao
mensal cruza zero em nov/2021 (+0,08), o mes que o post cita como de neutralidade.
As diferencas residuais em 2020 (total +4,29 vs. +4,4 publicado) sao revisoes do BCB
no saldo e no PIB desde a publicacao do post, nao divergencia de metodo.
"""
from analytics.brasil.credit import transforms as tf
from analytics.report_structure import tree_helpers as th

_leaf, _group, _direct = th.leaf, th.group, th.direct

# Series de cred_credito_resumo usadas pela tabela (a). Todas comecam em 2007-03
# (saldo_total_total vai a 1988-06, mas os 6 cortes abaixo nao) -> primeiro impulso
# calculavel em 2009-03, ja que a formula precisa de 24 meses de historico.
_RESUMO_IMPULSO_KEYS = [
    "saldo_total_total",
    "saldo_livre_total", "saldo_livre_pj", "saldo_livre_pf",
    "saldo_direcionado_total", "saldo_direcionado_pj", "saldo_direcionado_pf",
]

# ── (a) Recurso (Livre/Direcionado) x primeira divisao (PJ/PF) ────────────────────
# Aninhado sob "Total Geral" de proposito (diferente da aba Saldo, onde Livre e
# Direcionado sao irmaos do total): aqui a hierarquia E a mensagem — Livre +
# Direcionado reproduzem o Total exatamente, e PJ + PF reproduzem cada recurso.
_RECURSO_TREE = [
    _direct("saldo_total_total", "Total Geral", [
        _direct("saldo_livre_total", "Livre", [
            _direct("saldo_livre_pj", "Pessoa Jurídica"),
            _direct("saldo_livre_pf", "Pessoa Física"),
        ]),
        _direct("saldo_direcionado_total", "Direcionado", [
            _direct("saldo_direcionado_pj", "Pessoa Jurídica"),
            _direct("saldo_direcionado_pf", "Pessoa Física"),
        ]),
    ]),
]

# ── (b) Porte de empresa (PJ) — cred_credito_porte, metrica='saldo' ──────────────
# Comeca em 2012-01 -> primeiro impulso em 2014-01.
_PORTE_TREE = [
    _group("porte", "total", "Total PJ (MPME + Grande)", [
        _leaf("porte", "mpme", "MPME"),
        _leaf("porte", "grande", "Grande"),
    ]),
]

# ── (c) Atividade economica (PJ) — cred_credito_atividade_economica ──────────────
# So os 4 ramos de topo, sem drill-down (pedido explicito do usuario, 2026-08).
# industria_total/servicos_total sao codigos SGS reais do BCB, nao somas.
# Comeca em 2012-01 -> primeiro impulso em 2014-01.
_ATIVIDADE_TREE = [
    _group("ativ", "total", "Total PJ (por Atividade)", [
        _leaf("ativ", "agropecuaria", "Agropecuária"),
        _leaf("ativ", "industria_total", "Indústria"),
        _leaf("ativ", "servicos_total", "Serviços"),
        _leaf("ativ", "outros", "Outros"),
    ]),
]

TREES = {
    "recurso":   _RECURSO_TREE,
    "porte":     _PORTE_TREE,
    "atividade": _ATIVIDADE_TREE,
}

# Serie de referencia de datas de cada tabela (a mais completa da respectiva arvore) —
# o cabecalho de colunas sai dela, para as linhas nao desalinharem entre si.
ANCHORS = {
    "recurso":   "saldo_total_total",
    "porte":     "porte__total",
    "atividade": "ativ__total",
}

PORTE_TABLE = ("porte", "cred_credito_porte")
ATIVIDADE_ECONOMICA_TABLE = ("ativ", "cred_credito_atividade_economica")
# Da tabela de atividade so essas 4 entram — as outras ~34 linhas sao o detalhe
# setorial fino, que a aba Saldo ja expoe e esta aba deliberadamente nao abre.
ATIVIDADE_KEYS = ["agropecuaria", "industria_total", "servicos_total", "outros"]


def resumo_impulso_keys() -> list:
    return list(_RESUMO_IMPULSO_KEYS)


def _shift_months(date_str: str, n: int) -> str:
    """'YYYY-MM-DD' deslocado n meses para tras. Lookup por data (e nao por posicao
    na lista) para a conta nao depender de a serie estar sem buracos no calendario."""
    year, month = int(date_str[:4]), int(date_str[5:7])
    total = year * 12 + (month - 1) - n
    return f"{total // 12:04d}-{total % 12 + 1:02d}-{date_str[8:]}"


def compute_impulse(dates: list[str], values: list, gdp_acum_12m: dict) -> list:
    """I_t em p.p. do PIB (ver formula na docstring do modulo). Retorna lista alinhada
    a `dates`, com None onde falta saldo em t/t-12/t-24 ou PIB em t/t-12 — os primeiros
    24 meses de qualquer serie sao sempre None por construcao."""
    vmap = dict(zip(dates, values))
    out = []
    for d in dates:
        d12, d24 = _shift_months(d, 12), _shift_months(d, 24)
        v0, v12, v24 = vmap.get(d), vmap.get(d12), vmap.get(d24)
        g0, g12 = gdp_acum_12m.get(d), gdp_acum_12m.get(d12)
        if None in (v0, v12, v24, g0, g12) or not g0 or not g12:
            out.append(None)
        else:
            out.append(((v0 - v12) / g0 - (v12 - v24) / g12) * 100)
    return out


def _variants(dates: list[str], values: list, gdp_acum_12m: dict) -> dict:
    """{"m12": {...}, "anual": {...}} — "anual" e a MESMA serie filtrada em dezembro
    (ver docstring do modulo), nunca um recalculo."""
    impulse = compute_impulse(dates, values, gdp_acum_12m)
    rounded = [None if v is None else round(v, 4) for v in impulse]
    dec = [i for i, d in enumerate(dates) if d[5:7] == "12"]
    return {
        "m12":   {"dates": list(dates), "values": rounded},
        "anual": {"dates": [dates[i] for i in dec], "values": [rounded[i] for i in dec]},
    }


# -- Ciclos de politica monetaria (faixas de fundo dos graficos) ------------------
# Usado pelas abas Saldo e Impulso (D.ciclos, montado em generate_report._load_ciclos).
# Mora aqui porque foi aqui que nasceu, e porque `_DECISAO_PARA_CICLO` e a unica
# traducao entre o vocabulario do BCB e o dos graficos.
# Fonte: pm_copom_reuniao -- 247 reunioes desde 1999-04, derivadas da SGS 432 (meta
# diaria) cruzada com o calendario de reunioes, nao do texto do comunicado (ver
# analytics/brasil/monetary_policy/). O regime vigente ENTRE duas reunioes e a decisao
# tomada na primeira delas, e decisoes iguais consecutivas se fundem numa faixa so.
#
# A regra e essa e nao tem parametro de suavizacao, o que foi uma escolha medida. A
# alternativa testada -- absorver um bloco de manutencoes no ciclo que o cerca quando os
# dois lados vao na mesma direcao -- da uma leitura mais "de mercado" (32 segmentos
# contra 50 em toda a serie) mas engole o plato de 14 meses da Selic em 6,50% entre
# mai/2018 e jul/2019, que sairia pintado de ciclo de QUEDA por estar entre dois cortes.
# Um plato de mais de um ano e exatamente o que a faixa cinza existe para mostrar, entao
# a suavizacao foi descartada. O preco tambem foi medido: 6 faixas de uma unica reuniao
# em toda a serie, todas anteriores a 2005 e portanto fora da janela do impulso, que so
# comeca em 2009-03.
#
# Leitura: a faixa e um estado pontual (a Selic naquele dia) e o impulso e uma janela de
# 24 meses (a formula usa t, t-12 e t-24), entao a faixa NAO explica a barra que esta em
# cima dela -- ela situa o ciclo em que aquele ponto foi observado. A nota da aba diz
# isso ao leitor.
_DECISAO_PARA_CICLO = {
    "elevacao":   "alta",
    "manutencao": "manutencao",
    "reducao":    "queda",
}


def build_ciclos(reunioes: list, inicio: str | None = None, fim: str | None = None) -> list:
    """[(data_iso, decisao)] em ordem cronologica -> [{"de", "ate", "tipo"}].

    `tipo` e "alta" | "manutencao" | "queda". `inicio`/`fim` recortam a lista a janela
    do proprio dado plotado -- as faixas sao `shapes` com `xref: 'x'`, que entram no
    autorange do Plotly, entao uma faixa de 1999 puxaria o eixo X do grafico para tras
    ate la mesmo sem nenhum dado plotado naquele trecho.
    """
    segs = []
    for data, decisao in reunioes:
        tipo = _DECISAO_PARA_CICLO.get(decisao)
        if tipo is None:
            continue
        if segs and segs[-1]["tipo"] == tipo:
            continue
        segs.append({"de": data, "ate": None, "tipo": tipo})
    for i in range(len(segs) - 1):
        segs[i]["ate"] = segs[i + 1]["de"]
    if segs:
        segs[-1]["ate"] = fim or segs[-1]["de"]

    out = []
    for seg in segs:
        de, ate = seg["de"], seg["ate"]
        if inicio and ate <= inicio:
            continue
        if fim and de >= fim:
            continue
        out.append({
            "de":   max(de, inicio) if inicio else de,
            "ate":  min(ate, fim) if fim else ate,
            "tipo": seg["tipo"],
        })
    return out


def build(raw: dict, pib_acum_12m: dict) -> dict:
    """`raw`: {seriesKey: {"dates", "values"}} com o SALDO NOMINAL bruto de toda chave
    usada nas 3 arvores, exceto os 2 totais sinteticos ("porte__total", "ativ__total"),
    somados aqui. `pib_acum_12m`: serie bruta do PIB nominal acumulado 12m
    (atv_pib_mensal.pib_acum_12m, BCB SGS 4382) — mesmo denominador que o BCB usa em
    cred_credito_resumo.pct_pib_*.
    """
    raw = dict(raw)
    raw["porte__total"] = tf.sum_series(raw["porte__mpme"], raw["porte__grande"])
    raw["ativ__total"] = tf.sum_series(
        raw["ativ__agropecuaria"], raw["ativ__industria_total"],
        raw["ativ__servicos_total"], raw["ativ__outros"],
    )

    gdp_map = tf.to_date_map(pib_acum_12m)
    series = {k: _variants(s["dates"], s["values"], gdp_map) for k, s in raw.items()}

    anchor = series.get(ANCHORS["recurso"], {}).get("m12", {"dates": []})
    ref_date = anchor["dates"][-1] if anchor["dates"] else None

    return {"trees": TREES, "anchors": ANCHORS, "series": series, "ref_date": ref_date}


# ══════════════════════════════════════════════════════════════════════════════════
# Fluxo financeiro e impulso de credito NO CONCEITO DO BCB (4a tabela da aba)
# ══════════════════════════════════════════════════════════════════════════════════
#
# Metrica DIFERENTE da das 3 tabelas acima, e a diferenca e exatamente a critica que o
# BCB faz a Biggs et al. no Estudo Especial 110/2021:
#
#   Biggs et al. (tabelas a/b/c)  parte da variacao do SALDO, entao juros acruados,
#                                 variacao cambial e baixas para prejuizo entram no
#                                 numero como se fossem credito novo.
#   BCB (esta tabela)             parte do FLUXO FINANCEIRO -- concessoes menos
#                                 pagamentos --, que so contem dinheiro que trocou
#                                 de mao.
#
# As duas convivem de proposito: a de cima e mensal, comeca em 2009 e decompoe em
# modalidade/porte/atividade; esta e mais limpa conceitualmente mas comeca em 2015 e so
# se abre em PJ/PF.
#
# Tres series e so tres, e o motivo nao e escassez de dado: e o conjunto que as DUAS
# fontes publicam. O grafico recorrente do RPM traz Total/PJ/PF em toda edicao, e o boxe
# de 2025-03 traz os mesmos tres desde 2015-01 (por isso ele entra, pelo trecho
# 2015-2017). O boxe tambem publica Livre/Direcionado dentro de PJ e PF, e essa quebra
# ficou FORA: com conjuntos de series diferentes, a edicao mais nova sobrepoe o pai e nao
# o filho, os dois caem em vintages distintos e a aditividade para de fechar -- medido em
# 0,095 p.p. em PJ e 0,196 em PF. Com as duas fontes publicando as mesmas tres, cada mes
# tem sempre as tres vindas da mesma edicao e o problema nao existe.
#
# Fluxo (o dado publicado, % do PIB acumulado em 12 meses):
#   negativo = o setor real paga ao SFN mais do que toma emprestado. E o normal.
# Impulso (derivado aqui, p.p. do PIB):
#   I_t = Fluxo_t - Fluxo_{t-12}. Positivo = sobrou mais recurso liquido para
#   familias e empresas do que doze meses antes.
#
# Nao ha PIB nesta conta: a fonte ja publica em % do PIB, com o denominador do
# proprio BCB. Passar por `compute_impulse()` (que divide saldo por PIB) seria
# dividir duas vezes.
#
# Fonte e armadilhas da emenda entre edicoes: domain/db/brasil/bcb/cred_fluxo_financeiro.py.

FLUXO_TABLE = "cred_fluxo_financeiro"

# Aninhada sob o Total pelo mesmo motivo da tabela (a): a hierarquia E a mensagem --
# PJ + PF reproduzem o Total exatamente (residuo 0,000000 na fonte, conferido na carga).
FLUXO_TREE = [
    _direct("fluxo_total", "Total", [
        _direct("fluxo_pj", "Pessoa Jurídica"),
        _direct("fluxo_pf", "Pessoa Física"),
    ]),
]

FLUXO_ANCHOR = "fluxo_total"

FLUXO_KEYS = ["fluxo_total", "fluxo_pj", "fluxo_pf"]


def fluxo_keys() -> list:
    return list(FLUXO_KEYS)


def compute_impulso_bcb(dates: list[str], values: list) -> list:
    """Fluxo_t - Fluxo_{t-12}, em p.p. do PIB. Lista alinhada a `dates`, com None onde
    falta o fluxo em t ou em t-12 -- o que sempre inclui os 12 primeiros meses.

    Lookup por DATA, nao por posicao: a serie e emendada de duas edicoes do RPM e nao
    ha garantia de que o calendario saia sem buraco (ver cred_fluxo_financeiro.py)."""
    vmap = dict(zip(dates, values))
    out = []
    for d in dates:
        v0, v12 = vmap.get(d), vmap.get(_shift_months(d, 12))
        out.append(None if None in (v0, v12) else v0 - v12)
    return out


def _fluxo_variants(dates: list[str], values: list) -> dict:
    """{"fluxo": {"m12", "anual"}, "impulso": {"m12", "anual"}}.

    "anual" e a MESMA serie lida em dezembro, nunca um recalculo -- em dezembro o fluxo
    acumulado em 12 meses ja E o do ano civil, e a diferenca contra dezembro anterior ja
    E o impulso do ano. Mesma logica das 3 tabelas de cima."""
    dec = [i for i, d in enumerate(dates) if d[5:7] == "12"]

    def par(vals):
        r = [None if v is None else round(v, 4) for v in vals]
        return {
            "m12":   {"dates": list(dates), "values": r},
            "anual": {"dates": [dates[i] for i in dec], "values": [r[i] for i in dec]},
        }

    return {"fluxo": par(values), "impulso": par(compute_impulso_bcb(dates, values))}


def build_fluxo(raw: dict) -> dict:
    """`raw`: {name: {"dates", "values"}} lido cru de `cred_fluxo_financeiro` (ja em %
    do PIB acumulado em 12 meses). Sem PIB e sem IPCA: a fonte publica na unidade
    final."""
    series = {k: _fluxo_variants(s["dates"], s["values"])
              for k, s in raw.items() if k in FLUXO_KEYS}

    anchor = series.get(FLUXO_ANCHOR, {}).get("fluxo", {}).get("m12", {"dates": []})
    ref_date = anchor["dates"][-1] if anchor["dates"] else None

    return {"tree": FLUXO_TREE, "anchor": FLUXO_ANCHOR,
            "series": series, "ref_date": ref_date}
