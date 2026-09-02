"""
Monta o dataset da aba "Emprego Formal" do Panorama de Mercado de Trabalho --
CAGED/MTE, 5 tabelas: Nacional, Por Setor, Por UF, Por Faixa Salarial e Estoque.

Por que aba separada, e nao dentro de Taxas/Ocupacao/Rendimento (avaliacao de
2026-08): CAGED e PNAD medem universos diferentes e nao sao comparaveis no mesmo
grafico. PNAD e pesquisa domiciliar (~103M ocupados, inclui informal, resultado
em taxa/nivel); CAGED e registro administrativo do emprego formal celetista
(~48M de estoque) e o que ele publica e FLUXO -- admissoes, desligamentos e o
saldo entre os dois, em pessoas/mes. As tabelas hierarquicas deste relatorio
plotam todas as linhas marcadas num eixo so, entao misturar `ocupado` (mil
pessoas, PNAD) com `saldo` (pessoas/mes, CAGED) produziria leitura errada por
construcao. Somam-se a isso a janela (2020-01 vs. 2012-03 da PNAD) e a revisao
retroativa, que so o CAGED tem.

## Controles: por que NAO ha variacao percentual aqui

As abas de PNAD usam Frequencia x Nivel/Diff Y-Y. Para fluxo de CAGED isso
nao serve: saldo e liquido e cruza zero -- confirmado ao vivo (2026-08), as 22
secoes CNAE cruzam, e a variacao anual em % do saldo nacional chega a 696%.
Percentual sobre serie que troca de sinal e ruido numerico, nao leitura ruim.
As tabelas de fluxo usam entao Mensal / Acum. 12m / Acum. no ano -- que e como o
proprio MTE publica, e continua sendo so visualizacao (nenhuma metrica derivada,
mesma restricao de escopo da v1, ver CLAUDE.md).

A tabela de Estoque tem seletor proprio (Nivel / Var. Mensal / Diff Y-Y):
estoque nunca cruza zero, entao a variacao percentual e valida la -- e a Var.
Mensal em pessoas e justamente a leitura de saldo dessa serie.

## Dois cortes setoriais que NAO se conversam

`mt_caged_setor` (microdado) traz as 22 secoes CNAE 2.0. `mt_caged` (BCB) traz
uma taxonomia propria de 3 niveis com agregados intermediarios (SIUP, Servicos)
que nao mapeia 1:1 nas secoes. Ficam em tabelas separadas de proposito -- ver o
Apendice do relatorio.
"""
from analytics.report_structure import tree_helpers as th
from analytics.brasil.labor_market import transforms as tf

# --- Cortes ------------------------------------------------------------------
# Slugs identicos aos que domain/db/brasil/mte/mt_caged_*.py gravam em
# `categoria` -- ver _SECAO/_UF/_BANDAS la.

_SETOR_LABELS = {
    "agropecuaria": "Agropecuária",
    "industria_extrativa": "Indústria extrativa",
    "industria_transformacao": "Indústria de transformação",
    "eletricidade_gas": "Eletricidade e gás",
    "agua_esgoto_residuos": "Água, esgoto e resíduos",
    "construcao": "Construção",
    "comercio": "Comércio",
    "transporte_armazenagem_correio": "Transporte, armazenagem e correio",
    "alojamento_alimentacao": "Alojamento e alimentação",
    "informacao_comunicacao": "Informação e comunicação",
    "atividades_financeiras_seguros": "Atividades financeiras e seguros",
    "atividades_imobiliarias": "Atividades imobiliárias",
    "atividades_profissionais_cientificas_tecnicas": "Ativ. profissionais e científicas",
    "atividades_administrativas_servicos_complementares": "Ativ. administrativas",
    "administracao_publica_defesa_seguridade_social": "Adm. pública e defesa",
    "educacao": "Educação",
    "saude_servicos_sociais": "Saúde e serviços sociais",
    "artes_cultura_esporte_recreacao": "Artes, cultura, esporte e recreação",
    "outras_atividades_servicos": "Outros serviços",
    "servicos_domesticos": "Serviços domésticos",
    "organismos_internacionais": "Organismos internacionais",
    "nao_identificado": "Não identificado",
}

# Regioes IBGE. `NI` (nao identificado) fica como folha solta fora das regioes --
# nao pertence a nenhuma, e enfia-lo numa distorceria o total regional.
_REGIOES = [
    ("norte", "Norte", ["RO", "AC", "AM", "RR", "PA", "AP", "TO"]),
    ("nordeste", "Nordeste", ["MA", "PI", "CE", "RN", "PB", "PE", "AL", "SE", "BA"]),
    ("sudeste", "Sudeste", ["MG", "ES", "RJ", "SP"]),
    ("sul", "Sul", ["PR", "SC", "RS"]),
    ("centro_oeste", "Centro-Oeste", ["MS", "MT", "GO", "DF"]),
]
_UF_LABELS = {
    "RO": "Rondônia", "AC": "Acre", "AM": "Amazonas", "RR": "Roraima", "PA": "Pará",
    "AP": "Amapá", "TO": "Tocantins", "MA": "Maranhão", "PI": "Piauí", "CE": "Ceará",
    "RN": "Rio Grande do Norte", "PB": "Paraíba", "PE": "Pernambuco", "AL": "Alagoas",
    "SE": "Sergipe", "BA": "Bahia", "MG": "Minas Gerais", "ES": "Espírito Santo",
    "RJ": "Rio de Janeiro", "SP": "São Paulo", "PR": "Paraná", "SC": "Santa Catarina",
    "RS": "Rio Grande do Sul", "MS": "Mato Grosso do Sul", "MT": "Mato Grosso",
    "GO": "Goiás", "DF": "Distrito Federal", "NI": "Não identificado",
}

_SALARIO_LABELS = {
    "ate_1sm": "Até 1 salário mínimo",
    "de_1_a_1_5sm": "De 1 a 1,5 SM",
    "de_1_5_a_2sm": "De 1,5 a 2 SM",
    "de_2_a_3sm": "De 2 a 3 SM",
    "de_3_a_5sm": "De 3 a 5 SM",
    "de_5_a_7sm": "De 5 a 7 SM",
    "de_7_a_10sm": "De 7 a 10 SM",
    "de_10_a_15sm": "De 10 a 15 SM",
    "de_15_a_20sm": "De 15 a 20 SM",
    "mais_de_20sm": "Mais de 20 SM",
    "nao_identificado": "Não identificado",
}

_METRICAS = ["saldo", "admissoes", "desligamentos"]

# --- Informacao por linha: nome oficial + explicacao -------------------------
# O rotulo da linha e curto; o nome completo da fonte e a definicao aparecem num
# card ao passar o mouse / clicar no botao de informacao -- mesmo mecanismo de
# pnad_tab.py, ver o comentario de _INFO la. seriesKey -> (nome oficial na
# fonte, explicacao); qualquer um dos dois pode ser "".

_INFO = {
    "nac__saldo": (
        "Saldo de movimentações: admissões menos desligamentos",
        "É um fluxo LÍQUIDO: cruza zero, e por isso a tabela oferece acumulados em vez de "
        "variação percentual. Não é o estoque de empregos — é quanto ele mudou no período.",
    ),
    "nac__admissoes": ("Admissões declaradas na competência", ""),
    "nac__desligamentos": (
        "Desligamentos declarados na competência",
        "Inclui todos os motivos: demissão sem justa causa, pedido de demissão, fim de contrato "
        "por prazo determinado, aposentadoria e falecimento.",
    ),
    "setor__agua_esgoto_residuos": (
        "Água, esgoto, atividades de gestão de resíduos e descontaminação", ""),
    "setor__atividades_profissionais_cientificas_tecnicas": (
        "Atividades profissionais, científicas e técnicas", ""),
    "setor__atividades_administrativas_servicos_complementares": (
        "Atividades administrativas e serviços complementares",
        "Inclui a terceirização de mão de obra (agências de emprego temporário, limpeza, "
        "segurança) — costuma se mover antes dos setores que contratam esses serviços.",
    ),
    "setor__administracao_publica_defesa_seguridade_social": (
        "Administração pública, defesa e seguridade social",
        "Só o vínculo celetista: estatutários e militares não entram no CAGED, então este setor "
        "é uma fração pequena do emprego público real.",
    ),
    "setor__outras_atividades_servicos": ("Outras atividades de serviços", ""),
    "setor__nao_identificado": (
        "Seção CNAE não identificada",
        "Vínculos cujo CNAE não foi informado ou não pôde ser classificado — não é um setor, é "
        "ausência de informação.",
    ),
    "uf__NI": (
        "Unidade da federação não identificada",
        "Vínculos sem UF declarada. Fica fora das cinco regiões de propósito: colocá-lo em uma "
        "delas distorceria o subtotal regional.",
    ),
    "salario__nao_identificado": (
        "Faixa salarial não identificada",
        "Vínculos sem remuneração declarada — não significa salário baixo.",
    ),
    "salario__ate_1sm": (
        "Até 1 salário mínimo",
        "As faixas são múltiplos do salário mínimo VIGENTE NA COMPETÊNCIA, não valores nominais "
        "fixos em R$ — é a convenção das publicações oficiais do CAGED, porque bandas em R$ "
        "nominal perdem sentido conforme a inflação salarial desloca a distribuição inteira.",
    ),
    "caged_total": (
        "Estoque de empregos formais celetistas (BCB/SGS 28763)",
        "ESTOQUE, não saldo: é quantos vínculos existem, não quantos foram criados. A variação "
        "mensal desta série é que reproduz o saldo do microdado — em 2026-06 as duas fontes dão "
        "exatamente 145.161. É essa igualdade que permite o tampão: quando o BCB está um release "
        "atrás do Novo CAGED, o mês que falta entra somando o saldo do microdado ao último nível "
        "publicado, e a linha de fonte do gráfico diz qual mês é provisório.",
    ),
    "caged_SIUP": (
        "Serviços industriais de utilidade pública",
        "Agregado do BCB: eletricidade e gás mais água, esgoto e gestão de resíduos. Fecha exato "
        "com a soma dos dois filhos — em todos os 235 meses em que os dois existem. O agregado vai "
        "a 1992; os dois filhos, só a jan/2007.",
    ),
    "caged_servicos": (
        "Serviços (taxonomia do BCB)",
        "Vários subsetores de serviços não têm código SGS próprio, então o BCB publica só quatro "
        "filhos. O que falta entra aqui como “Demais serviços”, calculado por diferença — sem ele "
        "os filhos somariam um terço do pai e uma decomposição empilhada mentiria.",
    ),
    "caged_servicos_outros": (
        "Demais serviços (resíduo, calculado por diferença)",
        "NÃO é uma série do BCB: é Serviços menos os quatro subsetores que têm código SGS próprio. "
        "São os serviços que o SGS não abre — imobiliárias, profissionais e científicas, "
        "administrativas, administração pública, educação, saúde, e os demais. Hoje respondem por "
        "cerca de dois terços do estoque de Serviços, e existem para que a árvore feche: sem esta "
        "linha, a soma dos filhos não dá o pai.",
    ),
}


def _leaf(series_key: str, label: str, children: list | None = None, key: str | None = None) -> dict:
    """_leaf() + o nome oficial/explicacao de _INFO, quando houver."""
    node = th.direct(series_key, label, children, key)
    nome, expl = _INFO.get(series_key, ("", ""))
    if nome and nome != label:
        node["full"] = nome
    if expl:
        node["desc"] = expl
    return node


# --- Estoque (mt_caged, BCB) -- arvore de 3 niveis, validada ao vivo somando as
# partes (ver docstring de domain/db/brasil/bcb/mt_caged.py) -----------------

_ESTOQUE_TREE = [
    _leaf("caged_total", "Total Brasil", [
        _leaf("caged_agropecuaria", "Agropecuária"),
        _leaf("caged_ind_extrativa", "Indústria extrativa"),
        _leaf("caged_ind_transformacao", "Indústria de transformação"),
        _leaf("caged_SIUP", "SIUP", [
            _leaf("caged_eletricidade_gas", "Eletricidade e gás"),
            _leaf("caged_gestao_residuos", "Água, esgoto e gestão de resíduos"),
        ]),
        _leaf("caged_construcao", "Construção"),
        _leaf("caged_comercio", "Comércio"),
        _leaf("caged_servicos", "Serviços", [
            _leaf("caged_transp_arm_correios", "Transporte, armazenagem e correios"),
            _leaf("caged_aloj_alimentacao", "Alojamento e alimentação"),
            _leaf("caged_informacao_comunicacao", "Informação e comunicação"),
            _leaf("caged_ativ_financeiras_seguros", "Atividades financeiras e seguros"),
            _leaf("caged_servicos_outros", "Demais serviços"),
        ]),
    ]),
]
DB_NAMES_ESTOQUE = [
    "caged_total", "caged_agropecuaria", "caged_ind_extrativa", "caged_ind_transformacao",
    "caged_SIUP", "caged_eletricidade_gas", "caged_gestao_residuos", "caged_construcao",
    "caged_comercio", "caged_servicos", "caged_transp_arm_correios", "caged_aloj_alimentacao",
    "caged_informacao_comunicacao", "caged_ativ_financeiras_seguros",
]
# Filhos publicados de Servicos -- o resto vira "caged_servicos_outros" por
# diferenca, em build().
_SERVICOS_FILHOS = [
    "caged_transp_arm_correios", "caged_aloj_alimentacao",
    "caged_informacao_comunicacao", "caged_ativ_financeiras_seguros",
]
# Os 7 setores de 1o nivel, que somam o total.
_ESTOQUE_TOPO = [
    "caged_agropecuaria", "caged_ind_extrativa", "caged_ind_transformacao", "caged_SIUP",
    "caged_construcao", "caged_comercio", "caged_servicos",
]

# --- Controles ----------------------------------------------------------------
# Cada opcao pode carregar `fmt` (como formatar o valor na tabela) e `ypart` (um
# TRECHO do rotulo do eixo Y). Quando ha 2 controles, a chave da variante e a
# concatenacao dos dois valores com "__"; o `fmt` do ultimo controle que define
# um vence, e os `ypart` de todos eles sao concatenados na ordem -- entao o eixo
# diz o que esta medindo E em que janela ("admissões — pessoas, acum. 12 meses"),
# em vez de so a janela. Ver makeSimpleHierTab() em report.html.
#
# As abas de PNAD nao usam `ypart`: la a unidade varia por LINHA (uma tabela
# mistura taxa em % com nivel em mil pessoas), entao a opcao carrega `ymode` e o
# JS resolve o rotulo a partir das series marcadas -- ver pnad_tab.py.

_CTRL_METRICA = {
    "key": "metrica", "label": "Métrica",
    "options": [
        {"value": "saldo", "label": "Saldo", "ypart": "saldo (admissões − desligamentos)"},
        {"value": "admissoes", "label": "Admissões", "ypart": "admissões"},
        {"value": "desligamentos", "label": "Desligamentos", "ypart": "desligamentos"},
    ],
}
_CTRL_PERIODO = {
    "key": "periodo", "label": "Período",
    "options": [
        {"value": "mensal", "label": "Mensal", "fmt": "pessoas", "ypart": "pessoas no mês"},
        {"value": "acum12m", "label": "Acum. 12m", "fmt": "pessoas", "ypart": "pessoas, acum. 12 meses"},
        {"value": "acum_ano", "label": "Acum. no ano", "fmt": "pessoas", "ypart": "pessoas, acum. no ano"},
    ],
}
# Terceiro eixo dos cortes: nao escolhe uma serie, TRANSFORMA a que os dois
# primeiros escolheram -- daí `derived: True`, que tira este controle da chave
# da variante no JS. `lag` e a defasagem em meses da diferenca.
#
# So Y/Y por enquanto (pedido do usuario, 2026-08-28). O M/M sobre o saldo cru
# ficou de fora de proposito: o saldo mensal e fortemente sazonal (dezembro e
# negativo todo ano), entao a contribuicao contra o mes anterior responde quase
# sempre a mesma coisa. O Y/Y neutraliza a sazonalidade por construcao.
_CTRL_VISAO = {
    "key": "visao", "label": "Visão", "derived": True,
    "options": [
        {"value": "nivel", "label": "Nível"},
        {
            "value": "contrib_yy", "label": "Contribuição Y/Y", "lag": 12,
            "ypart": "contribuição para a variação contra o mesmo mês do ano anterior, pessoas",
            "ypartDrops": ["periodo"],
        },
    ],
}
_CTRL_ESTOQUE = {
    "key": "metric", "label": "Métrica",
    "options": [
        {"value": "level", "label": "Nível", "fmt": "pessoas", "ypart": "vínculos formais celetistas, pessoas"},
        {"value": "mom_diff", "label": "Var. Mensal (pessoas)", "fmt": "pessoas", "ypart": "variação do estoque no mês, pessoas"},
        {"value": "yoy", "label": "Diff Y/Y (%)", "fmt": "pct", "ypart": "variação do estoque em 12 meses, %"},
        {
            "value": "contrib_yy", "label": "Contribuição Y/Y (p.p.)", "fmt": "pp", "contrib": True,
            "ypart": "contribuição para a variação do estoque em 12 meses, p.p.",
        },
    ],
}


def _cut_tree(prefix: str, labels: dict, total_label: str) -> list:
    """Arvore de um corte plano: raiz "Total Brasil" (soma real, ver build()) com
    uma folha por categoria."""
    children = [_leaf(f"{prefix}__{slug}", label) for slug, label in labels.items()]
    return [_leaf(f"{prefix}__total", total_label, children)]


def _uf_tree() -> list:
    regioes = [
        _leaf(
            f"uf__reg_{slug}", label,
            [_leaf(f"uf__{sigla}", _UF_LABELS[sigla]) for sigla in siglas],
        )
        for slug, label, siglas in _REGIOES
    ]
    return [_leaf("uf__total", "Total Brasil", regioes + [_leaf("uf__NI", _UF_LABELS["NI"])])]


TABLES = [
    {
        "key": "nacional", "label": "Nacional — Saldo, Admissões e Desligamentos",
        "chart_title": "Emprego Formal Celetista — Brasil",
        "chart_source": "Fonte: MTE/PDET, Novo CAGED (microdado)",
        "controls": [_CTRL_PERIODO],
        "tree": [
            _leaf("nac__saldo", "Saldo (admissões − desligamentos)"),
            _leaf("nac__admissoes", "Admissões"),
            _leaf("nac__desligamentos", "Desligamentos"),
        ],
        "default_checked": ["nac__saldo"],
    },
    {
        "key": "setor", "label": "Por Setor de Atividade (CNAE 2.0, seção)",
        "chart_title": "Emprego Formal por Setor de Atividade — Brasil",
        "chart_source": "Fonte: MTE/PDET, Novo CAGED (microdado)",
        "controls": [_CTRL_METRICA, _CTRL_PERIODO, _CTRL_VISAO],
        "tree": _cut_tree("setor", _SETOR_LABELS, "Total Brasil"),
        "default_checked": ["setor__total"],
        "default_expanded": ["setor__total"],
    },
    {
        "key": "uf", "label": "Por Unidade da Federação",
        "chart_title": "Emprego Formal por Unidade da Federação",
        "chart_source": "Fonte: MTE/PDET, Novo CAGED (microdado)",
        "controls": [_CTRL_METRICA, _CTRL_PERIODO, _CTRL_VISAO],
        "tree": _uf_tree(),
        "default_checked": [f"uf__reg_{slug}" for slug, _l, _s in _REGIOES],
        "default_expanded": ["uf__total"],
    },
    {
        "key": "salario", "label": "Por Faixa de Salário de Contratação (múltiplos do SM vigente)",
        "chart_title": "Emprego Formal por Faixa de Salário de Contratação — Brasil",
        "chart_source": "Fonte: MTE/PDET, Novo CAGED (microdado)",
        "controls": [_CTRL_METRICA, _CTRL_PERIODO, _CTRL_VISAO],
        "tree": _cut_tree("salario", _SALARIO_LABELS, "Total Brasil"),
        "default_checked": ["salario__total"],
        "default_expanded": ["salario__total"],
    },
    {
        "key": "estoque", "label": "Estoque de Empregos Formais (BCB/SGS, desde 1992)",
        "chart_title": "Estoque de Empregos Formais — Brasil",
        "chart_source": "Fonte: BCB/SGS, séries 28763-28776",
        "controls": [_CTRL_ESTOQUE],
        "tree": _ESTOQUE_TREE,
        "default_checked": ["caged_total"],
        "default_expanded": ["caged_total"],
    },
]


_MESES_PT = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"]


def _mes_ano(iso: str) -> str:
    return f"{_MESES_PT[int(iso[5:7]) - 1]}/{iso[:4]}"


def _tables_com_provisorio(estoque: dict) -> list[dict]:
    """Anota na linha de fonte do grafico de estoque os meses que vieram do
    tampao (`fonte='mte'` em mt_caged): o BCB ainda nao publicou e o nivel foi
    reconstruido somando o saldo do microdado. Sem isso o cabecalho diria
    "Fonte: BCB/SGS" sobre um ponto que o BCB nao imprimiu -- e o cabecalho e
    justamente a parte que viaja junto num print do grafico.

    Some sozinha quando o BCB publica: a coluna volta a 'bcb' e nao ha mais
    nada a anotar. Devolve TABLES intacto nesse caso."""
    serie = estoque.get("caged_total", {})
    prov = [d for d, f in zip(serie.get("dates", []), serie.get("fonte", [])) if f != "bcb"]
    if not prov:
        return TABLES

    rotulo = _mes_ano(prov[0]) if len(prov) == 1 else f"{_mes_ano(prov[0])} a {_mes_ano(prov[-1])}"
    saida = []
    for tabela in TABLES:
        if tabela["key"] == "estoque":
            tabela = dict(tabela)
            tabela["chart_source"] += (
                f" · {rotulo} provisório: o BCB ainda não publicou, nível reconstruído "
                "somando o saldo do Novo CAGED"
            )
        saida.append(tabela)
    return saida


def _com_demais_servicos(estoque: dict) -> dict:
    """Acrescenta `caged_servicos_outros` = Serviços − os 4 filhos publicados.

    Sem ele a árvore do estoque não fecha em Serviços: os 4 subsetores com
    código SGS somam cerca de um terço do pai (7,6 de 23,5 milhões em jul/2026),
    e uma barra empilhada dessa decomposição mostraria um terço do que existe
    sem indicar que falta algo. É aritmética exata sobre séries publicadas, não
    uma estimativa -- mas é uma série DERIVADA, e o cartão de definição da linha
    diz isso."""
    pai = estoque.get("caged_servicos")
    filhos = [estoque.get(k) for k in _SERVICOS_FILHOS]
    if pai is None or any(f is None for f in filhos):
        return estoque
    # Casa por DATA: os 4 filhos comecam em 2007-01 e o pai em 1992-01.
    mapas = [dict(zip(f["dates"], f["values"])) for f in filhos]
    datas, valores = [], []
    for d, v in zip(pai["dates"], pai["values"]):
        partes = [m.get(d) for m in mapas]
        if v is None or any(p is None for p in partes):
            continue
        datas.append(d)
        valores.append(round(float(v) - sum(float(p) for p in partes), 4))
    saida = dict(estoque)
    saida["caged_servicos_outros"] = {"dates": datas, "values": valores}
    return saida


# Tolerância do teste de aditividade, em vínculos, sobre um estoque de ~48
# milhões. Medido: de 2007-12 em diante o resíduo máximo é 93 vínculos (Total
# menos os 7 setores) e 0 (SIUP menos os 2 filhos, e Serviços menos os 5 depois
# de _com_demais_servicos); nos anos 1990 o primeiro chega a 57.655. É a
# separação entre arredondamento e discrepância de verdade.
_TOL_ADITIVIDADE = 1000


def _primeiro_aditivo(estoque: dict) -> str | None:
    """Primeira data (ISO) a partir da qual a árvore do estoque fecha e continua
    fechando até o fim; None se nunca fecha.

    Duas coisas a impedem, e as duas importam: **as 6 sub-séries do BCB só
    começam em 2007-01** (o agregado vai a 1992-01, então antes disso não há o
    que decompor), e nos anos 1990 o total excede a soma dos 7 setores em até
    57.655 vínculos. A contribuição só sai daí em diante — janela em que a conta
    não fecha mostra nada, em vez de mostrar uma pilha cuja altura não é o
    total."""
    total = estoque["caged_total"]
    mapa = {k: dict(zip(v["dates"], v["values"])) for k, v in estoque.items()}
    grupos = [("caged_total", _ESTOQUE_TOPO),
              ("caged_SIUP", ["caged_eletricidade_gas", "caged_gestao_residuos"]),
              ("caged_servicos", _SERVICOS_FILHOS + ["caged_servicos_outros"])]
    ultima_ruim_idx = -1
    for i, d in enumerate(total["dates"]):
        for pai, filhos in grupos:
            v = mapa[pai].get(d)
            partes = [mapa[k].get(d) for k in filhos]
            if v is None or any(p is None for p in partes):
                ultima_ruim_idx = i
                break
            if abs(float(v) - sum(float(p) for p in partes)) > _TOL_ADITIVIDADE:
                ultima_ruim_idx = i
                break
    j = ultima_ruim_idx + 1
    return total["dates"][j] if j < len(total["dates"]) else None


def _sum_metricas(cortes: list[dict]) -> dict:
    """Soma elemento a elemento varios {metrica: [valores]} ja alinhados no mesmo
    eixo de datas. Somar contagens de movimentacao por categoria e valido (sao
    particoes do mesmo universo) -- ao contrario de somar taxas, que este
    relatorio nunca faz."""
    if not cortes:
        return {}
    n = len(next(iter(cortes[0].values())))
    return {
        metrica: [sum(c[metrica][i] for c in cortes) for i in range(n)]
        for metrica in _METRICAS
    }


def _build_cut(series: dict, prefix: str, dados: dict, dates: list[str], slugs: list[str]) -> dict:
    """Grava as variantes de cada categoria do corte em `series` e devolve o
    {metrica: [valores]} de cada uma, para os totais/subtotais serem somados."""
    por_slug = {}
    for slug in slugs:
        por_metrica = {m: dados.get(slug, {}).get(m, [0.0] * len(dates)) for m in _METRICAS}
        por_slug[slug] = por_metrica
        series[f"{prefix}__{slug}"] = tf.variants_caged_fluxo(dates, por_metrica)
    return por_slug


def build(setor: dict, uf: dict, salario: dict, estoque: dict) -> dict:
    """`setor`/`uf`/`salario`: {categoria: {"dates": [...], metrica: [valores]}}
    ja reindexados num eixo mensal comum (ver generate_report.py's
    _load_caged_cut()). `estoque`: {name: {dates, values}} de mt_caged.

    Retorna {tables, series, ref_date} -- mesmo contrato de pnad_tab.build(),
    exceto que `tables` e uma lista plana (a aba e uma so) e nao ha `rate_keys`
    (o formato vem do controle, nao da serie -- ver _CTRL_* acima)."""
    series = {}
    dates = setor["_dates"]

    por_setor = _build_cut(series, "setor", setor, dates, list(_SETOR_LABELS))
    por_uf = _build_cut(series, "uf", uf, dates, list(_UF_LABELS))
    por_salario = _build_cut(series, "salario", salario, dates, list(_SALARIO_LABELS))

    # Total de cada corte somado do PROPRIO corte (nao emprestado de outro): os
    # tres tem que fechar no mesmo total nacional por construcao, entao calcular
    # separado transforma a igualdade num cross-check em vez de numa suposicao.
    totais = {
        "setor": _sum_metricas(list(por_setor.values())),
        "uf": _sum_metricas(list(por_uf.values())),
        "salario": _sum_metricas(list(por_salario.values())),
    }
    for prefix, total in totais.items():
        series[f"{prefix}__total"] = tf.variants_caged_fluxo(dates, total)

    divergencias = [
        (prefix, metrica, i)
        for prefix, total in totais.items() if prefix != "setor"
        for metrica in _METRICAS
        for i in range(len(dates))
        if abs(total[metrica][i] - totais["setor"][metrica][i]) > 0.5
    ]
    if divergencias:
        raise ValueError(
            f"Cortes do CAGED nao fecham no mesmo total nacional em {len(divergencias)} "
            f"celula(s) -- ex.: {divergencias[:3]}. Os tres cortes sao particoes do mesmo "
            "universo de movimentacoes; divergencia indica carga parcial de alguma tabela."
        )

    # UF: subtotal por regiao (soma real, plotavel -- nao linha so-cabecalho).
    for slug, _label, siglas in _REGIOES:
        series[f"uf__reg_{slug}"] = tf.variants_caged_fluxo(
            dates, _sum_metricas([por_uf[s] for s in siglas])
        )

    # Tabela Nacional: uma linha por metrica, so o seletor de periodo.
    for metrica in _METRICAS:
        series[f"nac__{metrica}"] = tf.variants_caged_periodo(dates, totais["setor"][metrica])

    estoque = _com_demais_servicos(estoque)
    total = estoque.get("caged_total")
    desde = _primeiro_aditivo(estoque) if total else None
    total_por_data = dict(zip(total["dates"], total["values"])) if total else None
    for name in DB_NAMES_ESTOQUE + ["caged_servicos_outros"]:
        s = estoque.get(name)
        if s is None:
            continue
        series[name] = tf.variants_caged_estoque(
            s["dates"], s["values"], total=total_por_data, desde=desde,
        )

    return {
        "tables": _tables_com_provisorio(estoque),
        "series": series,
        "ref_date": dates[-1],
        "ref_date_estoque": estoque["caged_total"]["dates"][-1] if "caged_total" in estoque else None,
    }
