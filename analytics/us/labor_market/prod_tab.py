"""
Conteudo de dominio da aba Productivity: setores, medidas, duracoes e cartoes.

E a unica aba TRIMESTRAL da pagina -- JOLTS, CES e CPS sao mensais --, e a unica em que
a "transformacao" nao e calculada: o BLS publica as tres leituras (indice, variacao
trimestral anualizada, variacao sobre o mesmo trimestre do ano anterior) como series
distintas, e a pill escolhe qual serie ler.

A razao NAO e que a reconta erre -- o arquivo traz o indice com tres decimais e a
reconta concorda com a taxa publicada em 0,0500 p.p. no maximo, que e o arredondamento
da propria taxa. A razao e que a taxa publicada e o numero citavel (quem compara com a
manchete quer 1,4) e que assim a leitura anual da pagina e a do BLS. Ver o docstring de
`domain/db/us/labor_market/mt_produtividade.py`, que mede as duas coisas.

--------------------------------------------------------------------------------
NADA AQUI E ADITIVO, E ISSO DESLIGA TRES CONTROLES
--------------------------------------------------------------------------------
Os seis setores se CONTEM em vez de particionar (Business ⊃ Nonfarm business ⊃
Manufacturing e Nonfinancial corporations), e o unico par que particiona de verdade --
Durable + Nondurable = Manufacturing -- tampouco soma, porque o que se publica e
indice: dois indices de base 100 somados dao ~200.

Entao `aditivo` e 0 nas 19 medidas, o que desliga barras empilhadas, "% do total" e a
regra "pai marcado com filho marcado vira linha". A hierarquia visual de Manufacturing
existe para dizer CONTENCAO, nao soma -- e a nota da aba diz isso.

--------------------------------------------------------------------------------
A GRADE SETOR x MEDIDA E ESBURACADA, E O BURACO CARREGA O AVISO DA FONTE
--------------------------------------------------------------------------------
Quatro medidas (lucros, lucro unitario, custo unitario nao-trabalho e custo unitario
combinado) existem SO para as corporacoes nao financeiras -- e a Tabela 6 do release.
Elas ficam na tela desabilitadas com o motivo, no padrao desta pagina.

E o buraco mais importante nao aparece na lista de medidas: `produto_real` significa
**valor adicionado** nos tres primeiros setores e **produto setorial** nos tres de
transformacao. Sao conceitos diferentes, com fonte e metodo diferentes, e o release
avisa em prosa que nao sao comparaveis. Aqui o aviso e derivado do dado
(`conceito_produto`) e entra na linha de unidade quando os dois conceitos estao
plotados juntos, em vez de virar nota de rodape que ninguem le.
"""

from __future__ import annotations

# ── setores ─────────────────────────────────────────────────────────────────
# A arvore tem TRES raizes soltas mais uma com filhos, o que e legitimo aqui: nao ha
# total, porque os setores se contem. `contem` alimenta o cartao de definicao.
SETORES: list[dict] = [
    {"key": "nonfarm_business", "label": "Nonfarm business"},
    {"key": "business", "label": "Business"},
    {"key": "nonfinancial_corp", "label": "Nonfinancial corporations"},
    {"key": "manufacturing", "label": "Manufacturing", "children": [
        {"key": "manufacturing_durable", "label": "Durable manufacturing"},
        {"key": "manufacturing_nondurable", "label": "Nondurable manufacturing"},
    ]},
]

DEFAULT_SETORES = ["nonfarm_business", "manufacturing"]

# ── as 19 medidas ───────────────────────────────────────────────────────────
# `so_nfc` marca as quatro que existem apenas nas corporacoes nao financeiras.
# `y_indice` / `y_variacao` sao os dois titulos de eixo, porque a mesma medida muda de
# unidade com a duracao -- indice de base 2017 numa, por cento na outra.
MEDIDAS: dict[str, dict] = {
    "produtividade": {
        "label": "Labor productivity", "short": "Productivity",
        "y_indice": "real output per hour worked, index 2017=100",
        "y_variacao": "real output per hour worked, % change",
    },
    "produto_real": {
        "label": "Output", "short": "Output",
        "y_indice": "real output, index 2017=100",
        "y_variacao": "real output, % change",
    },
    "horas_trabalhadas": {
        "label": "Hours worked", "short": "Hours",
        "y_indice": "hours worked by all persons, index 2017=100",
        "y_variacao": "hours worked by all persons, % change",
    },
    "remuneracao_hora": {
        "label": "Hourly compensation", "short": "Comp/hour",
        "y_indice": "labor compensation per hour worked, index 2017=100",
        "y_variacao": "labor compensation per hour worked, % change",
    },
    "remuneracao_hora_real": {
        "label": "Real hourly compensation", "short": "Real comp/hour",
        "y_indice": "hourly compensation deflated by the CPI, index 2017=100",
        "y_variacao": "hourly compensation deflated by the CPI, % change",
    },
    "custo_unitario_trabalho": {
        "label": "Unit labor costs", "short": "ULC",
        "y_indice": "labor cost per unit of real output, index 2017=100",
        "y_variacao": "labor cost per unit of real output, % change",
    },
    "parcela_trabalho": {
        "label": "Labor share", "short": "Labor share",
        "y_indice": "compensation as a share of output, index 2017=100",
        "y_variacao": "compensation as a share of output, % change",
    },
    "pagamento_unitario_nao_trabalho": {
        "label": "Unit nonlabor payments", "short": "Unit nonlabor",
        "y_indice": "nonlabor payments per unit of real output, index 2017=100",
        "y_variacao": "nonlabor payments per unit of real output, % change",
    },
    "deflator_produto": {
        "label": "Output price deflator", "short": "Deflator",
        "y_indice": "price of a unit of output, index 2017=100",
        "y_variacao": "price of a unit of output, % change",
    },
    "emprego": {
        "label": "Employment", "short": "Employment",
        "y_indice": "persons employed in the sector, index 2017=100",
        "y_variacao": "persons employed in the sector, % change",
    },
    "horas_semana": {
        "label": "Average weekly hours", "short": "Weekly hours",
        "y_indice": "average hours worked per week, index 2017=100",
        "y_variacao": "average hours worked per week, % change",
    },
    "produto_por_trabalhador": {
        "label": "Output per worker", "short": "Output/worker",
        "y_indice": "real output per person employed, index 2017=100",
        "y_variacao": "real output per person employed, % change",
    },
    "produto_nominal": {
        "label": "Nominal output", "short": "Nominal output",
        "y_indice": "output in current dollars, index 2017=100",
        "y_variacao": "output in current dollars, % change",
    },
    "remuneracao_total": {
        "label": "Labor compensation", "short": "Compensation",
        "y_indice": "total labor compensation, index 2017=100",
        "y_variacao": "total labor compensation, % change",
    },
    "pagamentos_nao_trabalho": {
        "label": "Nonlabor payments", "short": "Nonlabor payments",
        "y_indice": "total nonlabor payments, index 2017=100",
        "y_variacao": "total nonlabor payments, % change",
    },
    "lucro_unitario": {
        "label": "Unit profits", "short": "Unit profits", "so_nfc": 1,
        "y_indice": "pre-tax profits per unit of real output, index 2017=100",
        "y_variacao": "pre-tax profits per unit of real output, % change",
    },
    "lucros": {
        "label": "Profits", "short": "Profits", "so_nfc": 1,
        "y_indice": "pre-tax corporate profits, index 2017=100",
        "y_variacao": "pre-tax corporate profits, % change",
    },
    "custo_unitario_nao_trabalho": {
        "label": "Unit nonlabor costs", "short": "Unit nonlabor costs", "so_nfc": 1,
        "y_indice": "nonlabor costs per unit of real output, index 2017=100",
        "y_variacao": "nonlabor costs per unit of real output, % change",
    },
    "custo_unitario_combinado": {
        "label": "Unit combined input costs", "short": "Unit total costs", "so_nfc": 1,
        "y_indice": "labor plus nonlabor cost per unit of output, index 2017=100",
        "y_variacao": "labor plus nonlabor cost per unit of output, % change",
    },
}

ORDEM_MEDIDAS = list(MEDIDAS)

# ── duracoes: a pill escolhe QUAL SERIE ler, nao uma transformacao ──────────
DURACOES: list[dict] = [
    {"key": "tri_anual", "label": "Q/Q annualized",
     "desc": "change from the previous quarter, compounded to an annual rate"},
    {"key": "ano_a_ano", "label": "Y/Y",
     "desc": "change from the same quarter a year earlier"},
    {"key": "indice", "label": "Index 2017=100",
     "desc": "the index the two growth rates are computed from"},
]

# ── janelas de ciclo economico (graficos 3 e 4 do release) ──────────────────
# O release compara o ciclo corrente com o anterior e com o longo prazo, sempre como
# taxa anualizada entre as PONTAS -- nao a media das taxas trimestrais. As duas datas
# de pico sao as do NBER que o proprio BLS usa.
#
# `inicio_longo` e por setor porque a serie de transformacao comeca em 1987 e a de
# business/nonfarm em 1947, e o release cita o longo prazo de cada uma a partir do
# proprio inicio.
CICLOS: list[dict] = [
    {"key": "atual", "label": "Current cycle", "de": "2019Q4", "ate": None},
    {"key": "anterior", "label": "Previous cycle", "de": "2007Q4", "ate": "2019Q4"},
    {"key": "longo", "label": "Long term", "de": None, "ate": None},
]

CICLO_MEDIDAS = ["produtividade", "produto_real", "horas_trabalhadas"]

# Valores que o release de 2026-09-03 imprime para as janelas acima, usados como
# gabarito no teste. Nao entram no payload: a pagina calcula do indice.
CICLO_PUBLICADO: dict[str, dict[str, float]] = {
    "nonfarm_business": {"atual:produtividade": 2.1, "atual:produto_real": 2.5,
                         "atual:horas_trabalhadas": 0.4,
                         "anterior:produtividade": 1.5, "longo:produtividade": 2.1},
    "manufacturing": {"atual:produtividade": 0.5, "atual:produto_real": 0.2,
                      "atual:horas_trabalhadas": -0.3,
                      "anterior:produtividade": 0.1, "longo:produtividade": 2.1},
}

# ── cartoes de definicao ────────────────────────────────────────────────────
# Namespace `setor:` e `medida_prod:` -- a pagina hospeda tres pesquisas e as chaves
# colidiriam (`emprego` existe na CES e aqui, medindo coisas diferentes).
INFO: dict[str, dict] = {
    "setor:nonfarm_business": {
        "full": "Nonfarm business sector",
        "desc": "GDP minus general government, nonprofits, households (including "
                "owner-occupied housing) and farms, with the matching hours removed. "
                "About 76% of nominal GDP in 2025, and the sector the headline "
                "productivity number refers to.",
    },
    "setor:business": {
        "full": "Business sector",
        "desc": "The same exclusions as nonfarm business except that farming stays in. "
                "About 77% of nominal GDP in 2025. It CONTAINS nonfarm business, so "
                "the two never add to anything.",
    },
    "setor:nonfinancial_corp": {
        "full": "Nonfinancial corporate sector",
        "desc": "Corporations outside finance and insurance, also excluding "
                "unincorporated business and holding-company offices. About 51% of "
                "nominal GDP in 2025. It is the only sector with a profits breakdown, "
                "and the only one measured for employees alone — by construction it "
                "has no self-employed.",
    },
    "setor:manufacturing": {
        "full": "Manufacturing sector",
        "desc": "A cut from inside nonfarm business, so it does not add to it. Its "
                "output is built from Census value-of-production data deflated by BLS "
                "price indexes, with intrasectoral transactions removed — a different "
                "concept from the value-added output of the sectors above.",
    },
    "setor:manufacturing_durable": {
        "full": "Durable goods manufacturing",
        "desc": "Together with nondurable it partitions manufacturing in levels. The "
                "two still do not add on this page, because what is published is an "
                "index: two indexes based at 100 add to about 200.",
    },
    "setor:manufacturing_nondurable": {
        "full": "Nondurable goods manufacturing",
        "desc": "The other half of the manufacturing partition. Same caveat as durable: "
                "the levels partition, the indexes do not add.",
    },
    "medida_prod:produtividade": {
        "full": "Labor productivity (output per hour)",
        "desc": "Real output divided by hours worked by ALL persons — employees, the "
                "self-employed and unpaid family workers. It is not a measure of the "
                "workers' own effort: it moves with technology, capital, capacity "
                "utilisation and the composition of output as well.",
    },
    "medida_prod:produto_real": {
        "full": "Real output",
        "desc": "Value-added output for business, nonfarm business and nonfinancial "
                "corporations; sectoral output for the three manufacturing sectors. "
                "The two are built from different sources by different methods and the "
                "BLS states they are not directly comparable.",
    },
    "medida_prod:horas_trabalhadas": {
        "desc": "Hours actually worked, not hours paid: paid time off is removed using "
                "the National Compensation Survey and off-the-clock hours are added "
                "using the household survey. Someone with two jobs is counted at each.",
    },
    "medida_prod:remuneracao_hora": {
        "desc": "Wages and salaries plus employer contributions to social insurance and "
                "benefit plans, per hour worked. Outside nonfinancial corporations it "
                "also imputes compensation for the self-employed, at the same hourly "
                "rate as employees in the same sector.",
    },
    "medida_prod:remuneracao_hora_real": {
        "desc": "Hourly compensation deflated by the CPI-U for recent quarters and by "
                "the CPI-U-RS for the 1978-2025 trend. Because the deflator is a "
                "consumer price index, this is purchasing power, not a real cost to "
                "the employer.",
    },
    "medida_prod:custo_unitario_trabalho": {
        "desc": "Hourly compensation divided by productivity — the labor cost of "
                "producing one unit of output, and the series most often read as an "
                "indicator of cost-push pressure. Rising compensation pushes it up; "
                "rising productivity pulls it down.",
    },
    "medida_prod:parcela_trabalho": {
        "desc": "The share of output that accrues to workers as compensation, "
                "published as an index rather than as a percentage. The release quotes "
                "a level (52.8% for nonfarm business in 2026 Q2, a series low) that "
                "the published series does not carry — only the index does.",
    },
    "medida_prod:pagamento_unitario_nao_trabalho": {
        "desc": "Everything per unit of output that is not labor: profits, "
                "depreciation, production taxes net of subsidies, net interest, "
                "transfers, rental income and the surplus of government enterprises. "
                "With unit labor costs it accounts for the output price deflator.",
    },
    "medida_prod:deflator_produto": {
        "desc": "Current-dollar output divided by the output index — the price of a "
                "unit of what the sector produces. It is a producer-side price, not a "
                "consumer price index.",
    },
    "medida_prod:emprego": {
        "full": "Employment (all persons)",
        "desc": "Persons working in the sector, on the productivity program's own "
                "concept: it includes the self-employed and unpaid family workers, so "
                "it is not the payroll count from the establishment survey.",
    },
    "medida_prod:horas_semana": {
        "desc": "Hours worked divided by employment, per week. Hours worked and "
                "employment are both on the all-persons concept, so this is not the "
                "payroll survey's weekly-hours series either.",
    },
    "medida_prod:produto_por_trabalhador": {
        "desc": "Real output per person employed rather than per hour. It moves with "
                "hours per worker as well as with productivity, which is why the "
                "headline measure is the per-hour one.",
    },
    "medida_prod:produto_nominal": {
        "full": "Current-dollar output",
        "desc": "Output before deflating. Together with the real series it defines the "
                "output price deflator.",
    },
    "medida_prod:remuneracao_total": {
        "desc": "The sector's whole compensation bill, not per hour. Sourced mainly "
                "from the national accounts, with general government, nonprofits and "
                "households subtracted out.",
    },
    "medida_prod:pagamentos_nao_trabalho": {
        "desc": "The whole nonlabor bill, not per unit of output.",
    },
    "medida_prod:lucro_unitario": {
        "desc": "Pre-tax corporate profits with the inventory-valuation and "
                "capital-consumption adjustments, per unit of real output. Published "
                "only for nonfinancial corporations, and much more volatile than any "
                "other series here: it rose at a 43% annual rate in 2026 Q2.",
    },
    "medida_prod:lucros": {
        "full": "Corporate profits",
        "desc": "The same profits concept, before dividing by output. Published only "
                "for nonfinancial corporations.",
    },
    "medida_prod:custo_unitario_nao_trabalho": {
        "desc": "Nonlabor payments EXCLUDING profits — depreciation, production taxes "
                "net of subsidies, net interest and business transfers, per unit of "
                "output. Published only for nonfinancial corporations.",
    },
    "medida_prod:custo_unitario_combinado": {
        "desc": "Unit labor costs plus unit nonlabor costs. Published only for "
                "nonfinancial corporations.",
    },
}


def orfaos(chaves_setor: set[str], chaves_medida: set[str]) -> list[str]:
    """Chaves do INFO que nao resolvem contra os setores/medidas reais.

    Uma chave errada nao levanta: ela produz um botao `i` que nunca nasce, sem lacuna
    visivel na pagina. Este guarda e o unico jeito de perceber.
    """
    validas = ({f"setor:{k}" for k in chaves_setor}
               | {f"medida_prod:{k}" for k in chaves_medida})
    return sorted(set(INFO) - validas)


def full_redundante(rotulos: dict[str, str]) -> list[str]:
    """Entradas cujo `full` repete o rotulo que a linha ja mostra."""
    maus = []
    for chave, item in INFO.items():
        full = (item.get("full") or "").strip()
        curto = (rotulos.get(chave) or "").strip()
        if full and curto and full.lower() == curto.lower():
            maus.append(chave)
    return sorted(maus)


def sem_cartao(chaves_setor: set[str], chaves_medida: set[str]) -> list[str]:
    """Setores/medidas sem entrada no INFO — o inverso de `orfaos`.

    Aqui isso e erro e nao escolha: sao 6 setores e 19 medidas, todos com nome curto
    que precisa de definicao.
    """
    faltam = [f"setor:{k}" for k in sorted(chaves_setor) if f"setor:{k}" not in INFO]
    faltam += [f"medida_prod:{k}" for k in sorted(chaves_medida)
               if f"medida_prod:{k}" not in INFO]
    return faltam
