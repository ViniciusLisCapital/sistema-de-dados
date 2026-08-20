"""
Monta o dataset da aba "Divida Liquida (DLSP)" do Panorama Fiscal: os fatores
condicionantes da DLSP (macro_brasil.fisc_dlsp_fatores, da planilha Facdetp.xlsx do
BCB -- ver domain/db/brasil/bcb/fisc_dlsp_fatores.py) em NOVE tabelas separadas, uma
por fator, espelhando as 9 abas da planilha original (2026-08, a pedido do usuario:
"Separate the tables like in the excel: Estoque, Primario and so on").

As 9 tabelas compartilham a MESMA arvore de 95 itens e a MESMA grade de datas -- e
assim que a planilha e construida (confirmado ao vivo: zero divergencia de rotulo
entre as 9 abas). Por isso o payload guarda `dates` e `tree` UMA vez na raiz e cada
serie vira so um par de arrays nus (ver `build()`), em vez do formato
{"dates", "values"} repetido por serie que gfsm_tab.py/rtn_tab.py usam: sao 95 itens
x 9 fatores x 2 metricas = 1.710 series, e repetir as 295 datas em cada uma
multiplicaria o tamanho do HTML por ~3 sem acrescentar informacao.

## Duas metricas apenas: Nivel e % do PIB

Escopo explicito desta rodada ("For now, the only metric should be Level and % GDP")
-- sem Nominal/Real, sem Y/Y, sem Marginal, sem toggle de frequencia:

  - **Nivel**: o valor exatamente como a planilha publica -- saldo de fim de mes
    (fator `estoque`) ou fluxo do proprio mes (os 8 fatores de fluxo), R$ milhoes
    correntes. E deliberadamente o dado cru: o fluxo mensal de um fator e ruidoso
    (um pagamento pontual move um mes inteiro em dezenas de bilhoes), e a leitura
    suavizada e justamente o "% do PIB" abaixo.
  - **% do PIB**: sempre sobre o PIB acumulado em 12 meses
    (`atv_pib_mensal.pib_acum_12m`, SGS 4382), mas com o numerador diferente por
    natureza do fator:
      * `estoque` -> saldo de fim de mes / PIB 12m. E exatamente a razao que o BCB
        publica: confirmado ao vivo que reproduz `fisc_divida.dlsp_pct_pib` (SGS) a
        +/-0,005pp em todos os 295 meses, e por devedor tambem.
      * fluxos -> acumulado movel de 12 meses do fluxo / PIB 12m. Nao e o fluxo do
        mes dividido pelo PIB do mes: um fluxo mensal solto sobre o PIB mensal seria
        ruidoso e nao comparavel a nenhuma divulgacao. O acumulado em 12m e a
        convencao padrao para fator condicionante em %PIB e a mesma ja usada por
        `fisc_nfsp`'s colunas `*_pct_pib_12m` neste projeto.

    Essa escolha preserva a identidade contabil em termos de %PIB: a soma dos 8
    fluxos acumulados em 12m, dividida pelo PIB 12m, e a variacao do estoque em 12
    meses como % do PIB -- que e a apresentacao classica de "o que explica a
    variacao da divida no ano". Se os fluxos usassem o PIB do proprio mes, essa
    leitura se perderia.

    Atencao ao misturar tabelas: um valor de `estoque` em %PIB e um SALDO (~65% do
    PIB), um valor de fluxo em %PIB e um FLUXO ANUAL (~1-8% do PIB). Estao na mesma
    unidade mas nao na mesma escala -- ver a legenda da aba em report.html.

## Sinal

Mantido como o BCB publica (`fisc_dlsp_fatores` nao inverte -- ver a docstring do
script de ETL): fluxo positivo AUMENTA a divida liquida, logo `primario` positivo e
DEFICIT primario. Isso e o INVERSO da convencao de `fisc_nfsp` usada na aba Impulso
Fiscal deste mesmo relatorio. Inverter aqui quebraria a identidade
estoque = soma dos fluxos, que e a razao de existir da tabela -- entao a aba avisa
disso no texto em vez de "corrigir" o sinal.
"""
from __future__ import annotations

from domain.db.brasil.bcb.fisc_dlsp_fatores import FATORES, ITEM_TREE

# Rotulo de exibicao de cada fator (a chave e o slug gravado em
# fisc_dlsp_fatores.fator; a ordem aqui e a ordem das secoes na aba, que e a mesma
# ordem das abas da planilha do BCB).
FATOR_LABELS = [
    ("estoque",                  "Estoques"),
    ("primario",                 "Primário"),
    ("juros",                    "Juros Nominais"),
    ("ajuste_met_interno",       "Ajuste Metodológico Interno"),
    ("ajuste_met_externo",       "Ajuste Metodológico Externo"),
    ("ajuste_paridade",          "Ajuste de Paridade"),
    ("ajuste_caixa_competencia", "Ajuste Caixa-Competência"),
    ("reconhecimento_dividas",   "Reconhecimento de Dívidas"),
    ("privatizacoes",            "Privatizações"),
]

# Uma frase por fator, exibida sob o titulo da secao -- o que o fator mede, em
# linguagem de leitor de relatorio, nao de contador. Fonte: Manual de Estatisticas
# Fiscais do BCB (maio/2019) + as notas da propria planilha.
FATOR_NOTES = {
    "estoque": (
        "Saldo da dívida líquida no fim de cada mês — o estoque que os oito fatores "
        "seguintes explicam. É a única tabela desta aba que é um saldo, não um fluxo."
    ),
    "primario": (
        "Resultado primário (receitas menos despesas, exceto juros). "
        "<strong>Positivo aumenta a dívida</strong> — ou seja, positivo aqui é déficit primário, "
        "o inverso da convenção usada na aba Impulso Fiscal."
    ),
    "juros": (
        "Juros nominais apropriados por competência sobre o estoque da dívida — "
        "tipicamente o maior fator de crescimento da DLSP."
    ),
    "ajuste_met_interno": (
        "Reavaliação da dívida interna indexada ao câmbio: variação do valor em reais de "
        "dívidas e créditos internos atrelados a moeda estrangeira, sem que tenha havido "
        "qualquer pagamento ou emissão."
    ),
    "ajuste_met_externo": (
        "O mesmo efeito para a dívida externa: variação cambial sobre o estoque denominado "
        "em moeda estrangeira, convertido a reais."
    ),
    "ajuste_paridade": (
        "Efeito da variação das paridades entre as moedas que compõem a dívida externa "
        "(euro, iene, cesta do BID/Bird etc.) contra o dólar — separado do ajuste externo, "
        "que capta só a variação do real contra o dólar."
    ),
    "ajuste_caixa_competencia": (
        "Diferença entre o momento em que uma despesa/receita é reconhecida (competência) e "
        "aquele em que efetivamente afeta o caixa — reconcilia as duas óticas."
    ),
    "reconhecimento_dividas": (
        "Incorporação ao estoque de dívidas passadas até então não registradas (os "
        "\"esqueletos\"), e o efeito de renegociações. Não é gasto novo do período: é "
        "reconhecimento de obrigação anterior."
    ),
    "privatizacoes": (
        "Receita de alienação de ativos aplicada ao abatimento da dívida — reduz o estoque "
        "(valores negativos) sem ser resultado primário."
    ),
}

# Ancora das colunas de data da tabela (a serie mais completa da arvore -- existe em
# todos os fatores e em todas as datas). Ver makeDlspHierTab() em report.html.
ANCHOR_ITEM = "total"

# ---------------------------------------------------------------------------
# Balanco por entidade (2026-08, a pedido do usuario)
# ---------------------------------------------------------------------------
# Reorganiza os MESMOS itens numa arvore Entidade > Passivos | Ativos (> Caixa |
# Titulos e creditos), em vez do corte interna/externa das 9 secoes acima. A
# pergunta do usuario era se dava para separar por Passivos/Ativos/Caixa, e depois
# se dava para separar por entidade -- por entidade e a versao que funciona, por
# duas razoes confirmadas ao vivo:
#
#   1. **Reconciliacao exata e completa**: `interna__X + externa__X == total__X`
#      para cada uma das 5 entidades, e a soma das 5 == `total`, com desvio
#      0,000000 em todos os 295 meses. Entao o balanco de cada entidade e montavel
#      a partir das folhas das duas arvores, sem residuo.
#   2. **Os offsets intra-governo deixam de ser double-count**. Dois pares de itens
#      aparecem duas vezes com sinal oposto e se cancelam exatamente:
#      Uniao<->BCB (Conta Unica, +/-R$2,06tri; divida mobiliaria na carteira do
#      Bacen, +/-R$2,97tri) e Uniao<->estados/municipios (Lei 9.496/MP 2.185 --
#      soma dos dois lados = 0 em TODOS os 295 meses; Lei 8.727; dividas
#      reestruturadas). Somar o BRUTO das 5 entidades da R$18,4tri de passivos,
#      numero nao consolidado; mas os LIQUIDOS somam a DLSP publicada
#      automaticamente, porque os pares se cancelam no liquido. Ou seja: o balanco
#      por entidade e real e o total continua certo, desde que nunca se some a
#      coluna de bruto entre entidades. Os itens de offset levam "(<->)" no rotulo
#      exatamente para isso ficar visivel na tabela.
#
# E por isso tambem que "Caixa" so faz sentido por entidade: a Conta Unica e um
# ativo real da Uniao (R$2,06tri, 15,6% do PIB -- o colchao de caixa do Tesouro),
# que desaparece no consolidado porque e um deposito no proprio BCB. No consolidado
# sobram so ~R$54bi de depositos a vista em bancos comerciais (0,4% do PIB).
#
# **A classificacao afeta interpretacao, nao aritmetica**: os buckets sao uma
# PARTICAO das mesmas folhas, entao Passivos + Ativos == Liquido por construcao,
# qualquer que seja a classificacao de cada item.
#
# Quatro itens trocam de sinal ao longo da historia (Previdencia social,
# Equalizacao Cambial nos dois lados, Demais contas do Bacen) -- classificados pela
# NATUREZA do item, nao pelo sinal observado, entao num mes de sinal contrario o
# item aparece com valor negativo dentro do seu proprio bucket (um "passivo
# negativo"). Preferivel a uma linha que pula de bucket ao longo do tempo.

_PASSIVO, _CAIXA, _CREDITO = "passivo", "caixa", "credito"

# {item: bucket} ou {item: (bucket, rotulo_alternativo)}. Cobre TODAS as folhas de
# interna__X/externa__X das 5 entidades -- `build_entity_tree()` levanta se alguma
# folha ficar de fora, para uma linha nova do BCB nao sumir silenciosamente do
# balanco.
_CLASSE: dict[str, object] = {
    # ── Governo Federal ────────────────────────────────────────────────────────
    "interna__gov_federal__mobiliaria_mercado__mobiliaria_tesouro": (_PASSIVO, "Dívida mobiliária do Tesouro (em mercado)"),
    "interna__gov_federal__mobiliaria_mercado__titulos_custodia_fge": _CREDITO,
    "interna__gov_federal__securitizadas_tda": _PASSIVO,
    "interna__gov_federal__bancaria": _PASSIVO,
    "interna__gov_federal__arrec_recolher": _CREDITO,
    "interna__gov_federal__dep_vista": _CAIXA,
    "interna__gov_federal__fat": _CREDITO,
    "interna__gov_federal__previdencia": _CREDITO,
    "interna__gov_federal__reneg_9496_2185": (_CREDITO, "Renegociação Lei 9.496/MP 2.185 (⇄ estados/municípios)"),
    "interna__gov_federal__reneg_8727": (_CREDITO, "Renegociação Lei 8.727 (⇄ subnacionais/estatais)"),
    "interna__gov_federal__reestruturadas": _CREDITO,
    "interna__gov_federal__creditos_inst_fin_oficiais__instrumentos_hibridos": _CREDITO,
    "interna__gov_federal__creditos_inst_fin_oficiais__creditos_bndes": _CREDITO,
    "interna__gov_federal__aplic_fundos_programas": _CREDITO,
    "interna__gov_federal__outros_creditos": _CREDITO,
    "interna__gov_federal__relac_bacen__conta_unica": (_CAIXA, "Conta Única no Bacen (⇄ BCB)"),
    "interna__gov_federal__relac_bacen__mobiliaria_carteira_bacen": (_PASSIVO, "Dívida mobiliária na carteira do Bacen (⇄ BCB)"),
    "interna__gov_federal__relac_bacen__equaliz_cambial": (_PASSIVO, "Equalização cambial (⇄ BCB)"),
    "externa__gov_federal__titulos_mercado_domestico": (_PASSIVO, "Externa: títulos no mercado doméstico"),
    "externa__gov_federal__demais": (_PASSIVO, "Externa: demais"),
    # ── Banco Central ─────────────────────────────────────────────────────────
    "interna__bacen__base_monetaria": _PASSIVO,
    "interna__bacen__mobiliaria_bacen": _PASSIVO,
    "interna__bacen__compromissadas": _PASSIVO,
    "interna__bacen__dep_bacen__dep_voluntarios": _PASSIVO,
    "interna__bacen__dep_bacen__demais_depositos": (_PASSIVO, "Demais depósitos (recolhimentos compulsórios)"),
    "interna__bacen__creditos_inst_fin": _CREDITO,
    "interna__bacen__demais_contas": _CREDITO,
    "interna__bacen__relac_gov_federal__conta_unica": (_PASSIVO, "Conta Única do Tesouro (⇄ União)"),
    "interna__bacen__relac_gov_federal__mobiliaria_carteira_bacen": (_CREDITO, "Títulos públicos em carteira (⇄ União)"),
    "interna__bacen__relac_gov_federal__equaliz_cambial": (_CREDITO, "Equalização cambial (⇄ União)"),
    # Nota 15/ da planilha: esta linha "inclui as reservas internacionais" -- e a
    # posicao externa LIQUIDA do BC (reservas menos divida externa do proprio BC),
    # nao as reservas brutas. Para reservas brutas em linha propria seria preciso
    # cruzar com macro_brasil.cmb_reservas_bc, que esta fora do escopo desta aba.
    "externa__bacen": (_CAIXA, "Reservas internacionais (líq. da dívida externa do BC)"),
    # ── Governos estaduais ────────────────────────────────────────────────────
    "interna__gov_est__mobiliaria_liquida": _PASSIVO,
    "interna__gov_est__reneg_9496": (_PASSIVO, "Renegociação Lei 9.496 (⇄ União)"),
    "interna__gov_est__reneg_8727": (_PASSIVO, "Renegociação Lei 8.727 (⇄ União)"),
    "interna__gov_est__reestruturadas": _PASSIVO,
    "interna__gov_est__bancaria": _PASSIVO,
    "interna__gov_est__outros_debitos": _PASSIVO,
    "interna__gov_est__arrec_recolher": _CREDITO,
    "interna__gov_est__dep_vista": _CAIXA,
    "interna__gov_est__outros_creditos": _CREDITO,
    "externa__gov_est": (_PASSIVO, "Dívida externa"),
    # ── Governos municipais ───────────────────────────────────────────────────
    "interna__gov_mun__mobiliaria_liquida": _PASSIVO,
    "interna__gov_mun__reneg_2185": (_PASSIVO, "Renegociação MP 2.185 (⇄ União)"),
    "interna__gov_mun__reneg_8727": (_PASSIVO, "Renegociação Lei 8.727 (⇄ União)"),
    "interna__gov_mun__reestruturadas": _PASSIVO,
    "interna__gov_mun__bancaria": _PASSIVO,
    "interna__gov_mun__arrec_recolher": _CREDITO,
    "interna__gov_mun__dep_vista_aplic": _CAIXA,
    "externa__gov_mun": (_PASSIVO, "Dívida externa"),
    # ── Empresas estatais (rotulo prefixado pela sub-esfera, ver _ENTIDADES) ───
    "interna__estatais__federais__reestruturadas": _PASSIVO,
    "interna__estatais__federais__bancaria": _PASSIVO,
    "interna__estatais__federais__outros_debitos": _PASSIVO,
    "interna__estatais__federais__reneg_8727": _CREDITO,
    "interna__estatais__federais__carteira_titulos_publicos": _CREDITO,
    "interna__estatais__federais__dep_vista": _CAIXA,
    "interna__estatais__federais__outros_creditos": _CREDITO,
    "interna__estatais__estaduais__reestruturadas": _PASSIVO,
    "interna__estatais__estaduais__bancaria": _PASSIVO,
    "interna__estatais__estaduais__debentures": _PASSIVO,
    "interna__estatais__estaduais__reneg_8727": _PASSIVO,
    "interna__estatais__estaduais__carteira_titulos_publicos": _CREDITO,
    "interna__estatais__estaduais__dep_vista_aplic": _CAIXA,
    "interna__estatais__municipais__reestruturadas": _PASSIVO,
    "interna__estatais__municipais__bancaria": _PASSIVO,
    "interna__estatais__municipais__reneg_8727": _PASSIVO,
    "interna__estatais__municipais__dep_vista": _CAIXA,
    "externa__estatais__federais": (_PASSIVO, "Dívida externa"),
    "externa__estatais__estaduais": (_PASSIVO, "Dívida externa"),
    "externa__estatais__municipais": (_PASSIVO, "Dívida externa"),
}

# Entidades do balanco: (slug, rotulo, chave da serie liquida ja existente).
# `total__X` ja e publicado pelo BCB, entao o no "Líquido" nao e sintetico -- serve
# de conferencia visual contra Passivos + Ativos.
_ENTIDADES = [
    ("gov_federal", "Governo Federal", "total__gov_federal"),
    ("bacen", "Banco Central", "total__bacen"),
    ("gov_est", "Governos estaduais", "total__gov_est"),
    ("gov_mun", "Governos municipais", "total__gov_mun"),
    ("estatais", "Empresas estatais", "total__estatais"),
]

# Sub-esfera das estatais -> prefixo de rotulo. Evita 3 linhas "Dívida bancária"
# indistinguiveis dentro do mesmo bucket, sem precisar de um nivel extra de arvore.
_SUB_ESFERA_PREFIX = {"federais": "Federais", "estaduais": "Estaduais", "municipais": "Municipais"}

_BUCKETS = [
    (_PASSIVO, "Passivos"),
    (_CAIXA, "Caixa e equivalentes"),
    (_CREDITO, "Títulos e créditos"),
]

# Janela de 12 meses usada tanto para acumular o fluxo quanto no PIB do denominador
# (atv_pib_mensal.pib_acum_12m ja vem acumulado da fonte).
_TTM_WINDOW = 12


def build_tree() -> list:
    """Converte o ITEM_TREE plano do script de ETL na arvore aninhada que o lado JS
    consome ({key, label, seriesKey, children}), preservando a ordem original das
    linhas da planilha (ITEM_TREE e um dict construido na ordem de `_ITEMS`).

    Sao TRES raizes independentes -- `total`, `interna`, `externa` -- nao uma so:
    `total` e a abertura da divida liquida por devedor, `interna`/`externa` sao a
    mesma divida aberta por item de balanco. `total` = `interna` + `externa` em todo
    mes, entao marcar as tres raizes no grafico plota o mesmo agregado duas vezes
    (uma inteira, duas metades) -- e uma escolha do leitor, nao um erro a bloquear.
    """
    nodes = {
        slug: {"key": slug, "label": meta["label"], "seriesKey": slug}
        for slug, meta in ITEM_TREE.items()
    }
    roots = []
    for slug, meta in ITEM_TREE.items():
        parent = meta["parent"]
        if parent is None:
            roots.append(nodes[slug])
        else:
            nodes[parent].setdefault("children", []).append(nodes[slug])
    return roots


def _leaves_of(root: str) -> list[str]:
    """Folhas (itens sem filhos) sob `root`, na ordem original das linhas da planilha."""
    kids: dict[str, list[str]] = {}
    for slug, meta in ITEM_TREE.items():
        kids.setdefault(meta["parent"], []).append(slug)
    out: list[str] = []

    def walk(slug):
        if slug in kids:
            for child in kids[slug]:
                walk(child)
        else:
            out.append(slug)

    walk(root)
    return out


def _entity_leaves(ent: str) -> list[str]:
    """Folhas das DUAS arvores para uma entidade -- `interna__X` + `externa__X`.

    Juntas elas somam exatamente `total__X` (confirmado ao vivo, desvio 0,000000 em
    todos os 295 meses), que e o que torna o balanco por entidade completo e sem
    residuo.
    """
    return [
        item
        for root in (f"interna__{ent}", f"externa__{ent}")
        if root in ITEM_TREE
        for item in _leaves_of(root)
    ]


def _classify(item: str, ent: str) -> tuple[str, str]:
    """(bucket, rotulo) de uma folha. Levanta se o item nao estiver em `_CLASSE` --
    uma linha nova na planilha do BCB tem de aparecer como erro aqui, nao sumir do
    balanco em silencio (o parser de fisc_dlsp_fatores.py ja levanta antes, mas esta
    classificacao e uma segunda lista que tambem precisa ser mantida a mao)."""
    spec = _CLASSE.get(item)
    if spec is None:
        raise RuntimeError(
            f"item '{item}' (entidade '{ent}') nao esta em _CLASSE -- classificar como "
            f"passivo/caixa/credito antes de gerar o relatorio."
        )
    bucket, label = (spec, ITEM_TREE[item]["label"]) if isinstance(spec, str) else spec
    if ent == "estatais":
        parts = item.split("__")
        prefix = _SUB_ESFERA_PREFIX.get(parts[2] if len(parts) > 2 else "")
        if prefix:
            label = f"{prefix} — {label}"
    return bucket, label


def build_entity_tree() -> tuple[list, dict]:
    """Arvore do balanco: Entidade > (Líquido | Passivos | Caixa e equivalentes |
    Títulos e créditos) > item.

    Returns:
        (tree, synthetic) onde `synthetic` mapeia cada chave sintetica de agregado
        (`bal__{ent}`, `bal__{ent}__{bucket}`) para a lista de itens que ela soma --
        `build()` usa isso para pre-computar as series desses nos, que nao existem em
        fisc_dlsp_fatores (o BCB nao publica "total de passivos do Banco Central").
        O no "Líquido" NAO e sintetico: usa `total__{ent}`, ja publicado.
    """
    tree, synthetic = [], {}
    for ent, label, total_key in _ENTIDADES:
        leaves = _entity_leaves(ent)
        by_bucket: dict[str, list[str]] = {}
        for item in leaves:
            bucket, item_label = _classify(item, ent)
            by_bucket.setdefault(bucket, []).append((item, item_label))

        children = [{"key": f"bal__{ent}__liquido", "label": "Líquido (contribuição à DLSP)", "seriesKey": total_key}]
        for bucket, bucket_label in _BUCKETS:
            entries = by_bucket.get(bucket, [])
            if not entries:
                continue
            agg = f"bal__{ent}__{bucket}"
            synthetic[agg] = [item for item, _ in entries]
            children.append({
                "key": agg, "label": bucket_label, "seriesKey": agg,
                "children": [
                    {"key": f"bal__{ent}__{item}", "label": item_label, "seriesKey": item}
                    for item, item_label in entries
                ],
            })

        tree.append({"key": f"bal__{ent}", "label": label, "seriesKey": total_key, "children": children})
    return tree, synthetic


def _rolling_sum(values: list, window: int) -> list:
    """Soma movel das ultimas `window` observacoes. None enquanto a janela nao
    estiver cheia ou qualquer ponto dela for None. Local (nao reusa
    transforms.rolling_sum) so para nao carregar pandas por causa de uma soma sobre
    855 series curtas -- mesmo resultado."""
    out, acc, missing = [], 0.0, 0
    for i, v in enumerate(values):
        if v is None:
            missing += 1
        else:
            acc += v
        if i >= window:
            old = values[i - window]
            if old is None:
                missing -= 1
            else:
                acc -= old
        out.append(None if (i + 1 < window or missing) else acc)
    return out


def _sum_arrays(entries: list, metric: str, n: int) -> list:
    """Soma termo a termo as series de `entries` (cada uma o dict {level, pctpib} de
    um item, ou o escalar 0 das series identicamente nulas, ou None se ausente).

    Uma data e None so se TODOS os componentes forem None ali -- as folhas do balanco
    compartilham a mesma grade e a mesma janela de 12 meses, entao os None de `pctpib`
    coincidem nos 11 primeiros meses; tratar "algum None" como None inteiro apagaria
    o agregado sem motivo.
    """
    out = []
    for i in range(n):
        acc, seen = 0.0, False
        for e in entries:
            if e is None:
                continue
            if e == 0:
                seen = True
                continue
            v = e[metric][i]
            if v is not None:
                acc += v
                seen = True
        out.append(_compact(acc, 1 if metric == "level" else 4) if seen else None)
    return out


def _compact(value, digits: int):
    """Arredonda e devolve `int` quando o resultado e inteiro -- `26845` ocupa 5 bytes
    no JSON contra 7 de `26845.0`. Com 1.710 series x 295 pontos, essa diferenca
    sozinha vale centenas de KB no HTML final."""
    if value is None:
        return None
    r = round(value, digits)
    return int(r) if r == int(r) else r


def build(raw: dict, dates: list[str], gdp_ttm: dict) -> dict:
    """`raw`: {fator: {item: [valores alinhados a `dates`]}} -- ja na grade unica da
    planilha (ver generate_report.py's _load_dlsp_tab_data()). `dates`: a grade
    mensal compartilhada pelas 9 abas. `gdp_ttm`: {date: PIB acumulado em 12 meses}
    (atv_pib_mensal.pib_acum_12m).

    Retorna {fatores, notes, tree, dates, series, anchor}, com
    `series[fator][item] = {"level": [...], "pctpib": [...]}` -- arrays nus alinhados
    a `dates` (ver docstring do modulo para por que nao {dates, values} por serie).
    `pctpib` usa o saldo do proprio mes para `estoque` e o acumulado em 12 meses para
    os 8 fatores de fluxo; o denominador e o mesmo PIB 12m nos dois casos.

    **Series identicamente nulas viram o escalar `0`**, nao um array de 295 zeros:
    quatro dos oito fatores de fluxo (ajustes metodologicos, paridade, caixa-
    competencia) so tocam ~25 dos 95 itens e ficam exatamente zero no resto -- 364 das
    855 series. O lado JS (makeDlspHierTab() em report.html) expande o escalar de
    volta para zeros. Efeito colateral aceito e deliberado: num item identicamente
    zero, o "% do PIB" dos 11 primeiros meses da amostra mostra 0,00% em vez de "—"
    (a janela movel de 12 meses ainda nao esta cheia ali, mas a soma movel de zeros e
    zero de qualquer forma -- nao ha ambiguidade a esconder).
    """
    gdp = [gdp_ttm.get(d) for d in dates]

    series = {}
    for fator in FATORES:
        by_item = raw.get(fator, {})
        out_fator = {}
        for item in ITEM_TREE:
            values = by_item.get(item)
            if values is None:
                continue
            if all(v is None or v == 0 for v in values):
                out_fator[item] = 0
                continue
            numerator = values if fator == "estoque" else _rolling_sum(values, _TTM_WINDOW)
            out_fator[item] = {
                "level": [_compact(v, 1) for v in values],
                "pctpib": [
                    None if (n is None or g is None or g == 0) else _compact(n / g * 100, 4)
                    for n, g in zip(numerator, gdp)
                ],
            }
        series[fator] = out_fator

    # Agregados sinteticos do balanco por entidade (Passivos/Caixa/Títulos e
    # créditos). Somar as duas metricas termo a termo e valido: `level` e uma soma
    # direta, e `pctpib` tem o MESMO denominador para todos os itens (PIB 12m), entao
    # soma de razoes com denominador comum = razao da soma. Nao vale para nenhuma
    # outra metrica -- se um dia entrar Y/Y ou Real aqui, este atalho quebra.
    bal_tree, bal_synthetic = build_entity_tree()
    for fator in FATORES:
        by_item = series[fator]
        for agg, items in bal_synthetic.items():
            by_item[agg] = {
                metric: _sum_arrays([by_item.get(i) for i in items], metric, len(dates))
                for metric in ("level", "pctpib")
            }

    return {
        "fatores": [{"key": k, "label": label} for k, label in FATOR_LABELS],
        "notes": FATOR_NOTES,
        "tree": build_tree(),
        "balanco_tree": bal_tree,
        "dates": dates,
        "series": series,
        "anchor": ANCHOR_ITEM,
    }
