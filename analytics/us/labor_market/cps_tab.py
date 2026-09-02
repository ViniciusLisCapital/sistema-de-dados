"""
Conteudo de dominio da aba da CPS -- a pesquisa domiciliar.

Nao e hierarquia, e ganha tabela do mesmo jeito: quase tudo que a fabrica de tabela
entrega (celula mes a mes, caixa que plota, cor casando tabela e legenda, cartao de
definicao, cabecalho, regua) nao depende de parentesco -- so o recuo, a seta e a regra
barra/linha dependem. Regra escrita em `.claude/rules/lis-dashboards.md`
("It isn't a hierarchy is not a reason to skip the table").

--------------------------------------------------------------------------------
QUATRO BLOCOS, E POR QUE NAO UM SO
--------------------------------------------------------------------------------
1. **Situacao na forca de trabalho** -- e o unico bloco que E aditivo, e por isso o
   unico com arvore de verdade:

       Populacao civil (nao ajustada por sazonalidade, e o BLS diz isso na tabela)
       |- Forca de trabalho
       |  |- Ocupados
       |  \\- Desocupados
       \\- Fora da forca de trabalho
          \\- Quer trabalhar
             \\- Marginalmente ligados
                \\- Desalentados

2. **Taxas por grupo** -- 12 taxas de desemprego (sexo/idade, raca, etnia,
   escolaridade). Nao somam nada: cada uma tem a sua propria forca de trabalho no
   denominador. Tabela plana, sem barras empilhadas, sem "% do total".
3. **Composicao do desemprego** -- motivo (4 linhas) e duracao (4 linhas) sao **dois
   eixos sobre o mesmo total**, cada um somando os desocupados. Nunca podem ser
   irmaos: viram dois blocos com um pill de eixo, exatamente como o corte
   residencial/nao-residencial da construcao na CES fica fora da arvore.
4. **Subutilizacao (U-1 a U-6)** -- seis taxas encaixadas por definicao (cada uma
   contem a anterior), mas com **denominadores diferentes**: U-4 divide pela forca de
   trabalho mais desalentados, U-5 e U-6 pela forca mais todos os marginalmente
   ligados. Encaixe conceitual nao e aditividade, entao tabela plana tambem.

--------------------------------------------------------------------------------
DOIS AVISOS QUE A PAGINA TEM DE DAR
--------------------------------------------------------------------------------
- **A populacao nao e dessazonalizada** e a propria Summary table A marca a linha com
  nota. Ela entra so em `nsa`, e a pill de ajuste fica desligada nessa linha.
- **Outubro de 2025 nao existe na CPS.** A paralisacao do governo cancelou a coleta;
  o JOLTS e a CES continuaram. Isso apaga *duas* variacoes mensais (a de outubro e a
  de novembro), o que e diferente de "um mes sem dado".
"""

from __future__ import annotations

import pandas as pd

# ── os quatro blocos ─────────────────────────────────────────────────────────
# (chave do bloco, rotulo, aditivo?)
BLOCOS = [
    ("status", "Labor force status", 1),
    ("taxa_grupo", "Unemployment rates by group", 0),
    ("composicao", "Composition of unemployment", 0),
    ("alternativa", "Alternative measures of underutilization", 0),
]

# rotulo curto + arvore do bloco aditivo. `pai` None = raiz do bloco.
LINHAS: dict[str, dict] = {
    # ── status (arvore) ────────────────────────────────────────────────────
    "populacao": {"label": "Civilian population", "pai": None, "bloco": "status",
                  "so_nsa": True},
    "forca_trabalho": {"label": "Labor force", "pai": "populacao", "bloco": "status"},
    "ocupados": {"label": "Employed", "pai": "forca_trabalho", "bloco": "status"},
    "desocupados": {"label": "Unemployed", "pai": "forca_trabalho", "bloco": "status"},
    "fora_forca": {"label": "Not in labor force", "pai": "populacao", "bloco": "status"},
    "quer_trabalhar": {"label": "Want a job", "pai": "fora_forca", "bloco": "status"},
    "marginalmente_ligados": {"label": "Marginally attached", "pai": "quer_trabalhar",
                              "bloco": "status"},
    "desalentados": {"label": "Discouraged", "pai": "marginalmente_ligados",
                     "bloco": "status"},
    # as tres taxas de manchete acompanham o bloco, como razoes (nao somam)
    "participacao": {"label": "Participation rate", "pai": None, "bloco": "status",
                     "razao": True},
    "razao_emprego_pop": {"label": "Employment-population ratio", "pai": None,
                          "bloco": "status", "razao": True},
    "taxa_desemprego": {"label": "Unemployment rate", "pai": None, "bloco": "status",
                        "razao": True},
    # ── taxas por grupo ───────────────────────────────────────────────────
    "taxa_25_mais": {"label": "25 years and over", "bloco": "taxa_grupo"},
    "taxa_homens_20": {"label": "Men, 20 and over", "bloco": "taxa_grupo"},
    "taxa_mulheres_20": {"label": "Women, 20 and over", "bloco": "taxa_grupo"},
    "taxa_16_19": {"label": "Teenagers, 16-19", "bloco": "taxa_grupo"},
    "taxa_brancos": {"label": "White", "bloco": "taxa_grupo"},
    "taxa_negros": {"label": "Black or African American", "bloco": "taxa_grupo"},
    "taxa_asiaticos": {"label": "Asian", "bloco": "taxa_grupo"},
    "taxa_hispanicos": {"label": "Hispanic or Latino", "bloco": "taxa_grupo"},
    "taxa_sem_medio": {"label": "Less than high school", "bloco": "taxa_grupo"},
    "taxa_medio": {"label": "High school, no college", "bloco": "taxa_grupo"},
    "taxa_superior_incompleto": {"label": "Some college", "bloco": "taxa_grupo"},
    "taxa_superior": {"label": "Bachelor's or higher", "bloco": "taxa_grupo"},
    # ── composicao: dois eixos ────────────────────────────────────────────
    "perderam_emprego": {"label": "Job losers", "bloco": "composicao", "eixo": "motivo"},
    "pediram_demissao": {"label": "Job leavers", "bloco": "composicao", "eixo": "motivo"},
    "reentrantes": {"label": "Reentrants", "bloco": "composicao", "eixo": "motivo"},
    "novos_entrantes": {"label": "New entrants", "bloco": "composicao", "eixo": "motivo"},
    "dur_ate_5s": {"label": "Less than 5 weeks", "bloco": "composicao", "eixo": "duracao"},
    "dur_5_14s": {"label": "5 to 14 weeks", "bloco": "composicao", "eixo": "duracao"},
    "dur_15_26s": {"label": "15 to 26 weeks", "bloco": "composicao", "eixo": "duracao"},
    "dur_27s_mais": {"label": "27 weeks and over", "bloco": "composicao", "eixo": "duracao"},
    "dur_media": {"label": "Average duration", "bloco": "composicao", "eixo": "duracao",
                  "razao": True},
    "dur_mediana": {"label": "Median duration", "bloco": "composicao", "eixo": "duracao",
                    "razao": True},
    "parcial_economico": {"label": "Part time for economic reasons",
                          "bloco": "composicao", "eixo": "parcial"},
    "parcial_falta_trabalho": {"label": "— slack work or business conditions",
                               "bloco": "composicao", "eixo": "parcial"},
    "parcial_so_achou_pt": {"label": "— could only find part-time work",
                            "bloco": "composicao", "eixo": "parcial"},
    "parcial_nao_economico": {"label": "Part time for noneconomic reasons",
                              "bloco": "composicao", "eixo": "parcial"},
    # ── U-1 a U-6 ─────────────────────────────────────────────────────────
    "u1": {"label": "U-1", "bloco": "alternativa"},
    "u2": {"label": "U-2", "bloco": "alternativa"},
    "u3": {"label": "U-3 (headline)", "bloco": "alternativa"},
    "u4": {"label": "U-4", "bloco": "alternativa"},
    "u5": {"label": "U-5", "bloco": "alternativa"},
    "u6": {"label": "U-6", "bloco": "alternativa"},
}

EIXOS_COMPOSICAO = [
    ("motivo", "By reason"),
    ("duracao", "By duration"),
    ("parcial", "Part-time status"),
]

# ── cartoes ──────────────────────────────────────────────────────────────────
INFO: dict[str, dict] = {
    "cps:populacao": {
        "full": "Civilian noninstitutional population",
        "desc": "Everyone 16 and over who is not in the armed forces and not in an "
                "institution. It is the denominator of the participation rate, and the "
                "only line in the release that is never seasonally adjusted — the BLS "
                "footnotes it on the summary table.",
    },
    "cps:forca_trabalho": {
        "full": "Civilian labor force",
        "desc": "Employed plus unemployed. Someone who wants a job but has not looked "
                "for one in the last four weeks is not in it, which is why the labor "
                "force can shrink while the population grows.",
    },
    "cps:ocupados": {
        "full": "Employment level",
        "desc": "People who did any paid work in the reference week, plus those absent "
                "from a job they hold. Counts PEOPLE, so a second job does not add a "
                "second count — the opposite of the payroll survey, and the main reason "
                "the two employment levels differ by millions.",
    },
    "cps:desocupados": {
        "full": "Unemployment level",
        "desc": "People without a job who looked for work in the last four weeks and "
                "were available to take one, plus those on temporary layoff. Wanting a "
                "job is not enough — the search is what puts someone here rather than "
                "outside the labor force.",
    },
    "cps:fora_forca": {
        "desc": "Everyone in the population who is neither employed nor unemployed. "
                "Includes retirees, students and carers, so its level says little on "
                "its own; the sublines below are the part that reads as slack.",
    },
    "cps:quer_trabalhar": {
        "full": "Not in labor force — want a job now",
        "desc": "People outside the labor force who say they want a job. Not counted as "
                "unemployed because they did not search recently or were unavailable.",
    },
    "cps:marginalmente_ligados": {
        "full": "Marginally attached to the labor force",
        "desc": "Want a job, were available, and searched sometime in the previous 12 "
                "months — but not in the last four weeks. They are the group U-5 and "
                "U-6 add to the unemployed.",
    },
    "cps:desalentados": {
        "full": "Discouraged workers",
        "desc": "The subset of the marginally attached who gave a job-market reason for "
                "not searching — they believe no job is available for them. The group "
                "U-4 adds to the unemployed.",
    },
    "cps:participacao": {
        "full": "Labor force participation rate",
        "desc": "Labor force as a share of the civilian population. It falls both when "
                "people give up looking and when the population ages, and the two are "
                "not distinguishable in this series.",
    },
    "cps:razao_emprego_pop": {
        "desc": "Employment as a share of the population. Unlike the unemployment rate, "
                "it does not depend on whether the jobless are searching, so it does not "
                "improve when people leave the labor force.",
    },
    "cps:taxa_desemprego": {
        "full": "Unemployment rate (U-3)",
        "desc": "Unemployed as a share of the labor force. The headline measure, and the "
                "U-3 of the six alternatives.",
    },
    "cps:taxa_16_19": {
        "desc": "The most volatile of the group rates by a wide margin — a small "
                "population and a large share of it entering and leaving the labor "
                "force each month. A one-month move here is rarely a signal."
    },
    "cps:taxa_superior": {
        "full": "Unemployment rate — bachelor's degree and higher, 25 years and over",
        "desc": "Restricted to 25 and over, unlike the headline rate, because most "
                "people under 25 with a degree have only just entered the labor force.",
    },
    "cps:perderam_emprego": {
        "full": "Job losers and persons who completed temporary jobs",
        "desc": "The cyclical part of unemployment: people who did not choose to leave. "
                "It leads the other three reasons at a turning point.",
    },
    "cps:pediram_demissao": {
        "desc": "People who quit and are looking. Rises when workers are confident, so "
                "it moves the opposite way from job losers over the cycle.",
    },
    "cps:reentrantes": {
        "full": "Reentrants to the labor force",
        "desc": "People returning to search after a spell outside the labor force.",
    },
    "cps:novos_entrantes": {
        "desc": "People searching for a first job — mostly recent graduates.",
    },
    "cps:dur_27s_mais": {
        "full": "Number unemployed for 27 weeks and over",
        "desc": "Long-term unemployment. It peaks well after the unemployment rate does, "
                "because a spell has to last half a year to enter this line.",
    },
    "cps:dur_media": {
        "full": "Average weeks unemployed",
        "desc": "Mean length of ongoing spells. It is pulled up by the long tail, so it "
                "sits far above the median — the gap between the two is itself the read "
                "on how concentrated long-term unemployment is.",
    },
    "cps:dur_mediana": {"full": "Median weeks unemployed"},
    "cps:parcial_economico": {
        "full": "Employed part time for economic reasons, all industries",
        "desc": "People working 1-34 hours who wanted full-time work but had their hours "
                "cut or could not find a full-time job. The group U-6 adds to the "
                "unemployed and the marginally attached.",
    },
    "cps:parcial_nao_economico": {
        "full": "At work 1-34 hours, usually work part time for noneconomic reasons",
        "desc": "People working part time by choice — school, childcare, retirement. Not "
                "slack, and included here because the release's summary table carries it "
                "next to the economic-reasons line.",
    },
    "cps:u1": {
        "full": "U-1: persons unemployed 15 weeks or longer, as a percent of the labor force",
        "desc": "The narrowest measure. Excludes short spells entirely, so it is the "
                "slowest to rise and the slowest to fall.",
    },
    "cps:u2": {
        "full": "U-2: job losers and persons who completed temporary jobs, as a percent "
                "of the labor force",
        "desc": "The involuntary part of the headline rate.",
    },
    "cps:u3": {
        "full": "U-3: total unemployed, as a percent of the civilian labor force",
        "desc": "The official unemployment rate. The same series as the headline line in "
                "the block above.",
    },
    "cps:u4": {
        "full": "U-4: total unemployed plus discouraged workers, as a percent of the "
                "labor force plus discouraged workers",
        "desc": "Adds discouraged workers to both numerator and denominator — which is "
                "why it is not simply U-3 plus a number.",
    },
    "cps:u5": {
        "full": "U-5: total unemployed, plus discouraged workers, plus all other "
                "marginally attached, as a percent of the labor force plus all "
                "marginally attached",
    },
    "cps:u6": {
        "full": "U-6: total unemployed, plus all marginally attached, plus total "
                "employed part time for economic reasons, as a percent of the labor "
                "force plus all marginally attached",
        "desc": "The broadest published measure. Roughly twice U-3, and the gap between "
                "them widens in a downturn because involuntary part-time work rises "
                "before layoffs do.",
    },
}

UNIDADES = {
    "mil": "thousands of people",
    "pct": "% of the relevant base",
    "semanas": "weeks",
}


def linhas_do_bloco(bloco: str, presentes: set[str]) -> list[dict]:
    """As linhas declaradas do bloco que existem no banco, na ordem de LINHAS."""
    out = []
    for slug, cfg in LINHAS.items():
        if cfg["bloco"] != bloco or slug not in presentes:
            continue
        out.append({
            "key": slug,
            "label": cfg["label"],
            "pai": cfg.get("pai"),
            "eixo": cfg.get("eixo"),
            "razao": int(bool(cfg.get("razao"))),
            "soNsa": int(bool(cfg.get("so_nsa"))),
        })
    return out


def orfaos(presentes: set[str]) -> list[str]:
    """Slugs declarados em LINHAS que nao existem em mt_cps, e vice-versa."""
    decl = set(LINHAS)
    return sorted((decl - presentes) | (presentes - decl))


def info_orfaos() -> list[str]:
    """Chaves do INFO que nao resolvem contra LINHAS."""
    return sorted(k for k in INFO if k.split(":", 1)[1] not in LINHAS)


def full_redundante() -> list[str]:
    """Entradas cujo `full` repete o rotulo curto -- proibido pela regra do projeto."""
    return sorted(k for k, e in INFO.items()
                  if e.get("full")
                  and e["full"].strip() == LINHAS.get(k.split(":", 1)[1], {}).get("label", "").strip())


def unidade_por_linha(dados: pd.DataFrame) -> dict[str, str]:
    """slug -> unidade, lida do banco (nao declarada aqui, para nao divergir)."""
    return dict(dados.groupby("categoria")["unidade"].first())
