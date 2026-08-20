"""
Monta o dataset das abas "Taxas"/"Ocupação"/"Rendimento" do Panorama de Mercado
de Trabalho: 3 tabs, 4 tabelas hierarquicas cada (12 no total), cada uma com sua
propria tabela+grafico -- versao "quebrada" da v1 original (que tinha uma unica
tabela monolitica na aba "Indicadores"), a pedido explicito do usuario. Mescla as
series nacionais de mt_pnad (mensal/trimestre movel, sem quebra) com os cortes
demograficos/ocupacionais de mt_pnad_trimestral (trimestral "cheia") sob o MESMO
indicador, quando os dois existem -- mesmo padrao "tabela hierarquica + grafico"
ja usado por analytics/brasil/fiscal_policy/gfsm_tab.py (makeHierTab() no lado JS, aqui
uma variante mais simples, instanciada uma vez por tabela -- ver report.html).

So visualizacao nesta rodada (v1, a pedido explicito do usuario -- "For now, I
don't want to create metrics like Okun, just visualize the data"): Nivel/Var.
curto prazo/Var. anual pre-computados em Python (analytics/brasil/labor_market/
transforms.py), sem STL, deflacao ou %PIB.

Mescla mensal x trimestral -- por que e segura: mt_pnad_trimestral.py define os
nomes de variavel dos grupos "condicao/taxas" (agr 4093/4094/4095/6402) e
"subutilizacao" (agr 6396/6397) como STRINGS LITERALMENTE IGUAIS as chaves de
mt_pnad.py's _SIMPLES (`taxa_desocupacao`, `taxa_participacao`,
`taxa_informalidade`, `nivel_ocupacao`, `nivel_desocupacao`,
`taxa_subutil_combinada_horas`, `taxa_subutil_combinada_potencial`,
`taxa_subutil_composta` -- confirmado lendo os dois scripts, nao inferido) --
entao "Total" (mt_pnad) e "Sexo/Idade/Instrucao/Raca" (mt_pnad_trimestral)
citam exatamente o mesmo agregado/variavel do IBGE, so com/sem quebra
demografica, sem risco de parear indicadores semanticamente diferentes. Os
outros indicadores de mt_pnad (ocupacao/rendimento por posicao/atividade,
massa, niveis brutos da forca de trabalho) NAO tem contrapartida em
mt_pnad_trimestral nesta rodada e ficam como tabelas so-mensais.

Escopo do corte trimestral (2026-08, resposta a "curado vs completo" -- usuario
escolheu curado): so os 8 indicadores acima, por Sexo/Idade/Instrucao/Raca (os
5 de "condicao/taxas") ou so Sexo/Idade (os 3 de "subutilizacao", unicas
dimensoes que esse agregado publica) -- ~111 series. Rendimento/massa/
populacao/horas por posicao/atividade/ocupacao (mais ~230 series) ficam para
uma v2 -- ver Pending em analytics/brasil/labor_market/CLAUDE.md.
"""
from analytics.report_structure import tree_helpers as th
from analytics.brasil.labor_market import transforms as tf

# --- Dimensoes (slug -> rotulo), mesmos slugs que domain/db/brasil/ibge/
# mt_pnad_trimestral.py grava em `name` (_DIM_SEXO/_DIM_IDADE/_DIM_INSTRUCAO/
# _DIM_RACA la, so que aqui chaveado pelo slug, nao pelo id IBGE) ------------

_DIM_SEXO = {"homens": "Homens", "mulheres": "Mulheres"}
_DIM_IDADE = {
    "14_17": "14 a 17 anos", "18_24": "18 a 24 anos", "25_39": "25 a 39 anos",
    "40_59": "40 a 59 anos", "60_mais": "60 anos ou mais",
}
_DIM_INSTRUCAO = {
    "sem_instrucao": "Sem instrução", "fund_incompleto": "Fundamental incompleto",
    "fund_completo": "Fundamental completo", "medio_incompleto": "Médio incompleto",
    "medio_completo": "Médio completo", "superior_incompleto": "Superior incompleto",
    "superior_completo": "Superior completo", "nao_determinado": "Não determinado",
}
_DIM_RACA = {"branca": "Branca", "preta": "Preta", "parda": "Parda"}

_DIMS_COMPLETAS = [
    ("sexo", "Sexo", _DIM_SEXO),
    ("idade", "Idade", _DIM_IDADE),
    ("instrucao", "Instrução", _DIM_INSTRUCAO),
    ("raca", "Cor ou Raça", _DIM_RACA),
]
_DIMS_SEXO_IDADE = [
    ("sexo", "Sexo", _DIM_SEXO),
    ("idade", "Idade", _DIM_IDADE),
]

# --- Posicao na ocupacao / atividade (mesmos slugs que mt_pnad.py's
# _POSICAO_BASE/_ATIVIDADE_BASE) -- so-mensal, sem corte trimestral -----------

_POSICAO_LABELS = {
    "priv_excl_domestico_com_carteira": "Setor privado (exceto doméstico), com carteira",
    "priv_excl_domestico_sem_carteira": "Setor privado (exceto doméstico), sem carteira",
    "domestico_com_carteira": "Trabalhador doméstico, com carteira",
    "domestico_sem_carteira": "Trabalhador doméstico, sem carteira",
    "pub_excl_militar_com_carteira": "Setor público (exceto militar), com carteira",
    "pub_excl_militar_sem_carteira": "Setor público (exceto militar), sem carteira",
    "pub_militar_estatutario": "Militar e servidor estatutário",
    "empregador_cnpj": "Empregador, com CNPJ",
    "empregador_sem_cnpj": "Empregador, sem CNPJ",
    "conta_propria_cnpj": "Conta própria, com CNPJ",
    "conta_propria_sem_cnpj": "Conta própria, sem CNPJ",
    "familiar_auxiliar": "Trabalhador familiar auxiliar",
}
# Rendimento nao tem "familiar_auxiliar" (sem remuneracao por definicao) mas
# tem "rend_media_nacional", exclusivo dessa serie -- ver mt_pnad.py's
# _REND_POSICAO.
_REND_POSICAO_LABELS = {k: v for k, v in _POSICAO_LABELS.items() if k != "familiar_auxiliar"}

_ATIVIDADE_LABELS = {
    "agropecuaria": "Agropecuária",
    "industria_geral": "Indústria geral",
    "construcao": "Construção",
    "comercio_rep_veiculo": "Comércio e reparação de veículos",
    "transporte_armazenagem_correio": "Transporte, armazenagem e correio",
    "alojamento_alimentacao": "Alojamento e alimentação",
    "inform_comun_financ_imob_prof_adm": "Informação, comunicação, financeiro, imobiliário, profissional e administrativo",
    "admpub_educ_saude_segsoc": "Administração pública, educação, saúde e serviços sociais",
    "outros_servicos": "Outros serviços",
    "servicos_domesticos": "Serviços domésticos",
}

# --- Series "rate" (ja em %, variam em p.p.) -- mesmas chaves de mt_pnad.py's
# _SIMPLES. Tudo o mais (niveis em mil pessoas ou R$) varia em % ------------

_RATE_VARS = {
    "taxa_desocupacao", "taxa_participacao", "taxa_informalidade",
    "nivel_ocupacao", "nivel_desocupacao",
    "taxa_subutil_combinada_horas", "taxa_subutil_combinada_potencial", "taxa_subutil_composta",
    "taxa_subocupacao_horas", "pct_desalentados", "pct_contribuintes_previdencia",
}


def _dim_group(var: str, suffix: str, dim_label: str, categorias: dict) -> dict:
    children = [
        th.direct(f"{var}_{suffix}_{slug}", label)
        for slug, label in categorias.items()
    ]
    return th.direct(f"{var}__dim_{suffix}", dim_label, children)


def _indicador(var: str, label: str, dims: list | None = None) -> dict:
    """No de indicador com "Total" (mt_pnad, a propria seriesKey `var`) + um
    grupo filho por dimensao disponivel em mt_pnad_trimestral (`dims`, lista de
    (suffix, dim_label, categorias) -- None/[] para indicadores so-mensais."""
    children = [_dim_group(var, suffix, dim_label, cats) for suffix, dim_label, cats in (dims or [])]
    return th.direct(var, label, children or None)


def _flat(prefix: str, categorias: dict) -> list[dict]:
    """Lista de folhas de raiz (sem no-agrupador) -- usado quando o titulo do
    card da tabela ja diz o que agrupa (ex.: "Ocupação por Atividade"), entao a
    arvore em si nao precisa repetir esse rotulo num no-cabecalho proprio."""
    return [th.direct(f"{prefix}{slug}", label) for slug, label in categorias.items()]


# --- Tabelas por aba ---------------------------------------------------------
# Cada tabela: {key, label, tree, default_checked}. `key` so precisa ser unico
# dentro da propria aba -- report.html prefixa com a chave da aba para montar
# ids de DOM (ex.: "taxas__desocupacao").

_TAB_TAXAS = [
    {
        "key": "desocupacao", "label": "Taxa de Desocupação",
        "tree": [_indicador("taxa_desocupacao", "Taxa de Desocupação", _DIMS_COMPLETAS)],
        "default_checked": ["taxa_desocupacao"],
    },
    {
        "key": "participacao", "label": "Taxa de Participação na Força de Trabalho",
        "tree": [_indicador("taxa_participacao", "Taxa de Participação na Força de Trabalho", _DIMS_COMPLETAS)],
        "default_checked": ["taxa_participacao"],
    },
    {
        "key": "informalidade", "label": "Taxa de Informalidade",
        "tree": [_indicador("taxa_informalidade", "Taxa de Informalidade", _DIMS_COMPLETAS)],
        "default_checked": ["taxa_informalidade"],
    },
    {
        "key": "subutilizacao", "label": "Subutilização da Força de Trabalho",
        "tree": [
            _indicador("taxa_subutil_combinada_horas", "Taxa Combinada (Desocupação + Subocupação por Insuficiência de Horas)", _DIMS_SEXO_IDADE),
            _indicador("taxa_subutil_combinada_potencial", "Taxa Combinada (Desocupação + Força de Trabalho Potencial)", _DIMS_SEXO_IDADE),
            _indicador("taxa_subutil_composta", "Taxa Composta de Subutilização", _DIMS_SEXO_IDADE),
            _indicador("taxa_subocupacao_horas", "Taxa de Subocupação por Insuficiência de Horas"),
            _indicador("pct_desalentados", "Desalentados (% da força de trabalho potencial)"),
            th.direct("subutil_subocupado_horas", "Subocupados por Insuficiência de Horas (nível, mil pessoas)"),
            th.direct("subutil_forca_potencial", "Força de Trabalho Potencial (nível, mil pessoas)"),
            th.direct("subutil_desalentado", "Desalentados (nível, mil pessoas)"),
        ],
        "default_checked": ["taxa_subutil_composta"],
    },
]

_TAB_OCUPACAO = [
    {
        "key": "niveis", "label": "Ocupação e Desocupação (Níveis)",
        "tree": [
            _indicador("nivel_ocupacao", "Nível da Ocupação", _DIMS_COMPLETAS),
            _indicador("nivel_desocupacao", "Nível da Desocupação", _DIMS_COMPLETAS),
            th.direct("ocupado", "Pessoas Ocupadas (mil pessoas)"),
            th.direct("desocupado", "Pessoas Desocupadas (mil pessoas)"),
            th.direct("fora_da_forca_trabalho", "Fora da Força de Trabalho (mil pessoas)"),
        ],
        "default_checked": ["ocupado", "desocupado"],
    },
    {
        "key": "posicao", "label": "Ocupação por Posição na Ocupação",
        "tree": _flat("ocup_", _POSICAO_LABELS),
        "default_checked": ["ocup_priv_excl_domestico_com_carteira"],
    },
    {
        "key": "atividade", "label": "Ocupação por Atividade",
        "tree": _flat("ocup_", _ATIVIDADE_LABELS),
        "default_checked": ["ocup_admpub_educ_saude_segsoc"],
    },
    {
        "key": "informalidade_previdencia", "label": "Informalidade e Previdência",
        "tree": [
            th.direct("ocup_informal", "Pessoas Ocupadas em Situação de Informalidade (nível, mil pessoas)"),
            th.direct("pct_contribuintes_previdencia", "Contribuintes da Previdência Social (%)"),
        ],
        "default_checked": ["ocup_informal", "pct_contribuintes_previdencia"],
    },
]

_TAB_RENDIMENTO = [
    {
        "key": "medio", "label": "Rendimento Médio",
        "tree": [
            th.direct("rend_habitual_real_todos_trabalhos", "Habitual, real (todos os trabalhos)"),
            th.direct("rend_habitual_nominal_todos_trabalhos", "Habitual, nominal (todos os trabalhos)"),
            th.direct("rend_efetivo_real_todos_trabalhos", "Efetivo, real (todos os trabalhos)"),
            th.direct("rend_efetivo_nominal_todos_trabalhos", "Efetivo, nominal (todos os trabalhos)"),
            th.direct("rend_efetivo_real_trabalho_principal", "Efetivo, real (trabalho principal)"),
        ],
        "default_checked": ["rend_habitual_real_todos_trabalhos"],
    },
    {
        "key": "posicao", "label": "Rendimento por Posição na Ocupação",
        "tree": _flat("rend_", {**_REND_POSICAO_LABELS, "media_nacional": "Rendimento médio nacional (todas as posições)"}),
        "default_checked": ["rend_media_nacional"],
    },
    {
        "key": "atividade", "label": "Rendimento por Atividade",
        "tree": _flat("rend_", _ATIVIDADE_LABELS),
        "default_checked": ["rend_admpub_educ_saude_segsoc"],
    },
    {
        "key": "massa", "label": "Massa de Rendimento",
        "tree": [
            th.direct("massa_real_habitual", "Habitual, real"),
            th.direct("massa_nominal_habitual", "Habitual, nominal"),
            th.direct("massa_efetiva_real", "Efetivamente recebida, real"),
            th.direct("massa_efetiva_nominal", "Efetivamente recebida, nominal"),
        ],
        "default_checked": ["massa_real_habitual"],
    },
]

TABS = [
    {"key": "taxas", "label": "Taxas", "tables": _TAB_TAXAS},
    {"key": "ocupacao", "label": "Ocupação", "tables": _TAB_OCUPACAO},
    {"key": "rendimento", "label": "Rendimento", "tables": _TAB_RENDIMENTO},
]

# Controle unico das 12 tabelas de PNAD. `fmt: "auto"` = decide por serie via
# rate_keys (uma mesma tabela mistura taxas em % e niveis em mil pessoas, ex.:
# Subutilizacao) -- ao contrario da aba CAGED, onde o formato vem do controle.
# Anexado aqui, num laco so, em vez de repetido nos 12 dicts acima.
_CONTROLS = [{
    "key": "metric", "label": "Nível",
    "options": [
        {"value": "level", "label": "Nível", "fmt": "auto", "ytitle": "% ou nível (ver Apêndice)"},
        {"value": "curto", "label": "Var. Curto Prazo", "fmt": "auto", "ytitle": "p.p. ou % (ver Apêndice)"},
        {"value": "yoy", "label": "Var. Anual", "fmt": "auto", "ytitle": "p.p. ou % (ver Apêndice)"},
    ],
}]
for _tab in TABS:
    for _table in _tab["tables"]:
        _table.setdefault("controls", _CONTROLS)

# Todas as chaves de mt_pnad usadas nas tabelas acima (as 71 series da tabela,
# nenhuma orfa fora de alguma tabela) -- generate_report.py usa isto pra montar
# `series`. Mantido como lista explicita (nao derivada das TABS) porque foi
# live-verificada contra a base -- ver Gotchas em CLAUDE.md.
DB_NAMES_MENSAL = (
    ["taxa_desocupacao", "taxa_participacao", "taxa_informalidade",
     "taxa_subutil_combinada_horas", "taxa_subutil_combinada_potencial", "taxa_subutil_composta",
     "taxa_subocupacao_horas", "pct_desalentados",
     "nivel_ocupacao", "nivel_desocupacao",
     "subutil_subocupado_horas", "subutil_forca_potencial", "subutil_desalentado",
     "ocupado", "desocupado", "fora_da_forca_trabalho",
     "ocup_informal", "pct_contribuintes_previdencia",
     "rend_habitual_real_todos_trabalhos", "rend_habitual_nominal_todos_trabalhos",
     "rend_efetivo_real_todos_trabalhos", "rend_efetivo_nominal_todos_trabalhos",
     "rend_efetivo_real_trabalho_principal",
     "massa_real_habitual", "massa_nominal_habitual", "massa_efetiva_real", "massa_efetiva_nominal"]
    + [f"ocup_{slug}" for slug in _POSICAO_LABELS]
    + [f"ocup_{slug}" for slug in _ATIVIDADE_LABELS]
    + [f"rend_{slug}" for slug in _REND_POSICAO_LABELS]
    + ["rend_media_nacional"]
    + [f"rend_{slug}" for slug in _ATIVIDADE_LABELS]
)

# Chaves de mt_pnad_trimestral usadas (as ~111 series do corte curado).
_TRIMESTRAL_INDICADORES = [
    ("taxa_desocupacao", _DIMS_COMPLETAS), ("taxa_participacao", _DIMS_COMPLETAS),
    ("taxa_informalidade", _DIMS_COMPLETAS), ("nivel_ocupacao", _DIMS_COMPLETAS),
    ("nivel_desocupacao", _DIMS_COMPLETAS),
    ("taxa_subutil_combinada_horas", _DIMS_SEXO_IDADE),
    ("taxa_subutil_combinada_potencial", _DIMS_SEXO_IDADE),
    ("taxa_subutil_composta", _DIMS_SEXO_IDADE),
]
DB_NAMES_TRIMESTRAL = [
    f"{var}_{suffix}_{slug}"
    for var, dims in _TRIMESTRAL_INDICADORES
    for suffix, _label, categorias in dims
    for slug in categorias
]


def build(mensal: dict, trimestral: dict) -> dict:
    """`mensal`/`trimestral`: {name: {dates, values}} de mt_pnad/mt_pnad_trimestral
    (ver generate_report.py's _load_flat()). Retorna {tabs, series, ref_date,
    rate_keys} -- `tabs` e a lista de 3 abas x 4 tabelas (ver TABS acima), cada
    tabela com sua propria `tree`; `series` e um unico dict achatado com todas as
    182 series, compartilhado por todas as tabelas (o lado JS resolve cada
    seriesKey contra esse dict, independente de qual tabela/aba a linha esta)."""
    series = {}
    for name in DB_NAMES_MENSAL:
        s = mensal.get(name)
        if s is None:
            continue
        series[name] = tf.variants_mensal(s["dates"], s["values"], rate=name in _RATE_VARS)

    for name in DB_NAMES_TRIMESTRAL:
        s = trimestral.get(name)
        if s is None:
            continue
        series[name] = tf.variants_trimestral(s["dates"], s["values"], rate=True)

    ref_date = mensal["taxa_desocupacao"]["dates"][-1]
    rate_keys = [k for k in series if k in _RATE_VARS or any(k.startswith(f"{v}_") for v in _RATE_VARS)]
    return {"tabs": TABS, "series": series, "ref_date": ref_date, "rate_keys": rate_keys}
