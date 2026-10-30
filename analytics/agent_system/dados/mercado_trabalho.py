"""
As tabelas do agente de mercado de trabalho (SISTEMA_AGENTES.md V.VIII) e o F de cada uma.

A lista (quais tabelas) é decidida com o usuário e vive no SISTEMA_AGENTES.md; o gerador
levanta se esta declaração divergir dela. O tratamento (quais séries, que leitura) é do
sistema (IV.iv) e se ajusta pela qualidade do report.

Três coisas que valem para o arquivo inteiro:

  - As sete `mt_*` do grupo "Endógeno" nascem de `politica_monetaria` (`de(pm, ...)`), que as
    declara hoje: a consulta é a mesma, o arquivo de A é o mesmo e só as séries mudam (mais
    séries, para a leitura que o mapa pede). Enquanto os outros agentes ainda as declaram, é
    isso que mantém `conferir_consultas` quieto; quando migrarem para `de(mercado_trabalho, ...)`,
    a declaração passa a ter dono. As três que a PM não declara (`mt_pnad_trimestral`,
    `mt_caged_uf`, `mt_caged_salario`) são declaradas aqui.
  - Tabela de outro agente sai da declaração do dono (`de` e `so`, do motor), trocando só as
    séries: a atividade para o que ela ajustou, `politica_monetaria` para as contas nacionais e
    o crédito, `fiscal` para a `fisc_rtn`, `inflacao` para os preços. O A do ciclo, que é
    compartilhado, serve a todos.
  - Profundidade (PRINCIPIOS I.II.vii): só o grupo "Endógeno" ganha a leitura completa. As duas
    `mt_caged_uf` e `mt_caged_salario` estão nele mas a lista as quer em leitura enxuta; o
    motor decide pelo nome do grupo, então elas levam um `especial` que a desliga.

Duas leituras combinadas respondem o que nenhuma tabela sozinha dá (mapa, "Where the agent reads
the data"): a variação da taxa de desocupação aberta em emprego e força de trabalho (2.2) e o
saldo do CAGED de 12 meses por setor contra os 12 meses anteriores (2.6). A desocupação
dessazonalizada dos meses recentes, a produtividade e o custo unitário do trabalho não estão
aqui: a primeira espera a decisão do método; as duas últimas são G.
"""

from __future__ import annotations

import dataclasses

import pandas as pd

from analytics.agent_system.dados import atividade, fiscal, inflacao
from analytics.agent_system.dados import politica_monetaria as pm
from analytics.agent_system.dados.motor import (Ctx, Serie, Tabela, antes, bloco_generico, de,
                                                fdata, fmt, md_tabela)

SECAO = ("## (V.VIII) Agente de mercado de trabalho", "## (V.IX)")
PIB = None

_BI = 1000.0  # mil, ou R$ milhões -> um nível acima


def _s(chave, rotulo, unidade, leitura, **kw) -> Serie:
    return Serie(chave, rotulo, unidade, leitura, **kw)


def _enxuta(nome: str):
    """F genérico, mas na leitura enxuta: a lista quer assim para duas tabelas do grupo
    "Endógeno", que o motor leria por inteiro."""
    def f(df: pd.DataFrame, ctx: Ctx) -> list[str]:
        t = next(t for t in ctx.tabelas if t.nome == nome)
        return bloco_generico(t, df, dataclasses.replace(ctx, completo=False))
    f.__name__ = f"enxuta_{nome}"
    return f


# ── as séries ─────────────────────────────────────────────────────────────────
_MIL = "mil pessoas"
_PNAD_EXTRA = (
    # folga: o que a taxa de desocupação não conta (2.1, 2.2)
    _s("desocupado", "Desocupados", _MIL, "pct", casas=0),
    _s("fora_da_forca_trabalho", "Fora da força de trabalho", _MIL, "pct", casas=0),
    _s("taxa_subocupacao_horas", "Subocupação por insuficiência de horas", "%", "dif", casas=1),
    _s("taxa_subutil_combinada_horas", "Desocupação + subocupação por horas", "%", "dif", casas=1),
    _s("taxa_subutil_combinada_potencial", "Desocupação + força de trabalho potencial", "%", "dif", casas=1),
    _s("subutil_forca_potencial", "Força de trabalho potencial", _MIL, "pct", casas=0),
    _s("subutil_desalentado", "Desalentados", _MIL, "pct", casas=0),
    _s("pct_desalentados", "Desalentados", "% da força ampliada", "dif", casas=1),
    # emprego e renda por posição (2.4, 2.5, 2.9)
    _s("ocup_priv_excl_domestico_com_carteira", "Setor privado, com carteira", _MIL, "pct", casas=0),
    _s("ocup_priv_excl_domestico_sem_carteira", "Setor privado, sem carteira", _MIL, "pct", casas=0),
    _s("ocup_domestico_com_carteira", "Doméstico, com carteira", _MIL, "pct", casas=0),
    _s("ocup_domestico_sem_carteira", "Doméstico, sem carteira", _MIL, "pct", casas=0),
    _s("ocup_conta_propria_cnpj", "Conta própria, com CNPJ", _MIL, "pct", casas=0),
    _s("ocup_conta_propria_sem_cnpj", "Conta própria, sem CNPJ", _MIL, "pct", casas=0),
    _s("ocup_pub_excl_militar_com_carteira", "Setor público (sem militar), com carteira", _MIL, "pct", casas=0),
    _s("ocup_pub_excl_militar_sem_carteira", "Setor público (sem militar), sem carteira", _MIL, "pct", casas=0),
    _s("rend_priv_excl_domestico_com_carteira", "Rendimento: setor privado, com carteira", "R$", "pct", casas=0),
    _s("rend_priv_excl_domestico_sem_carteira", "Rendimento: setor privado, sem carteira", "R$", "pct", casas=0),
    _s("rend_conta_propria_cnpj", "Rendimento: conta própria, com CNPJ", "R$", "pct", casas=0),
    _s("rend_conta_propria_sem_cnpj", "Rendimento: conta própria, sem CNPJ", "R$", "pct", casas=0),
    _s("rend_efetivo_real_todos_trabalhos", "Rendimento efetivo real", "R$", "pct", casas=0),
    _s("massa_efetiva_real", "Massa de rendimento efetivo real", "R$ bi", "pct", escala=_BI, casas=1),
    # ocupação por atividade (2.6): compara-se direção, não nível, com o CAGED
    _s("ocup_agropecuaria", "Ocupados: agropecuária", _MIL, "pct", casas=0),
    _s("ocup_industria_geral", "Ocupados: indústria", _MIL, "pct", casas=0),
    _s("ocup_construcao", "Ocupados: construção", _MIL, "pct", casas=0),
    _s("ocup_comercio_rep_veiculo", "Ocupados: comércio", _MIL, "pct", casas=0),
    _s("ocup_transporte_armazenagem_correio", "Ocupados: transporte e correio", _MIL, "pct", casas=0),
    _s("ocup_alojamento_alimentacao", "Ocupados: alojamento e alimentação", _MIL, "pct", casas=0),
    _s("ocup_inform_comun_financ_imob_prof_adm", "Ocupados: informação, finanças e serviços profissionais",
       _MIL, "pct", casas=0),
    _s("ocup_admpub_educ_saude_segsoc", "Ocupados: administração pública, educação e saúde",
       _MIL, "pct", casas=0),
    _s("ocup_outros_servicos", "Ocupados: outros serviços", _MIL, "pct", casas=0),
    _s("ocup_servicos_domesticos", "Ocupados: serviços domésticos", _MIL, "pct", casas=0),
)

_CAGED_ESTOQUE = (
    ("caged_agropecuaria", "Agropecuária"), ("caged_ind_extrativa", "Indústria extrativa"),
    ("caged_SIUP", "Eletricidade, gás e água"), ("caged_aloj_alimentacao", "Alojamento e alimentação"),
    ("caged_ativ_financeiras_seguros", "Atividades financeiras e seguros"),
    ("caged_informacao_comunicacao", "Informação e comunicação"),
    ("caged_transp_arm_correios", "Transporte, armazenagem e correio"),
)

# O setor do Novo CAGED, pela seção CNAE: o rótulo que se lê.
_SETOR = {
    "agropecuaria": "Agropecuária", "industria_extrativa": "Indústria extrativa",
    "industria_transformacao": "Indústria de transformação", "eletricidade_gas": "Eletricidade e gás",
    "agua_esgoto_residuos": "Água, esgoto e resíduos", "construcao": "Construção",
    "comercio": "Comércio", "transporte_armazenagem_correio": "Transporte, armazenagem e correio",
    "alojamento_alimentacao": "Alojamento e alimentação",
    "informacao_comunicacao": "Informação e comunicação",
    "atividades_financeiras_seguros": "Financeiras e seguros",
    "atividades_imobiliarias": "Imobiliárias",
    "atividades_profissionais_cientificas_tecnicas": "Profissionais, científicas e técnicas",
    "atividades_administrativas_servicos_complementares": "Administrativas e serviços complementares",
    "administracao_publica_defesa_seguridade_social": "Administração pública",
    "educacao": "Educação", "saude_servicos_sociais": "Saúde e serviços sociais",
    "artes_cultura_esporte_recreacao": "Artes, cultura, esporte e recreação",
    "outras_atividades_servicos": "Outras atividades de serviços",
    "servicos_domesticos": "Serviços domésticos", "organismos_internacionais": "Organismos internacionais",
}

_UFS = ("AC AL AM AP BA CE DF ES GO MA MG MS MT PA PB PE PI PR RJ RN RO RR RS SC SE SP TO").split()

_FAIXAS = (("ate_1sm", "Até 1 SM"), ("de_1_a_1_5sm", "De 1 a 1,5 SM"), ("de_1_5_a_2sm", "De 1,5 a 2 SM"),
           ("de_2_a_3sm", "De 2 a 3 SM"), ("de_3_a_5sm", "De 3 a 5 SM"), ("de_5_a_7sm", "De 5 a 7 SM"),
           ("de_7_a_10sm", "De 7 a 10 SM"), ("de_10_a_15sm", "De 10 a 15 SM"),
           ("de_15_a_20sm", "De 15 a 20 SM"), ("mais_de_20sm", "Mais de 20 SM"))

_PNAD_TRI = (
    # a desocupação dos jovens é o corte mais cíclico (2.2, 2.6)
    *[_s(f"taxa_desocupacao_idade_{k}", f"Desocupação, {rot}", "%", "dif", casas=1) for k, rot in (
        ("14_17", "14 a 17 anos"), ("18_24", "18 a 24 anos"), ("25_39", "25 a 39 anos"),
        ("40_59", "40 a 59 anos"), ("60_mais", "60 anos ou mais"))],
    *[_s(f"taxa_desocupacao_instrucao_{k}", f"Desocupação, {rot}", "%", "dif", casas=1) for k, rot in (
        ("fund_incompleto", "fundamental incompleto"), ("medio_completo", "médio completo"),
        ("superior_completo", "superior completo"))],
    _s("taxa_desocupacao_sexo_homens", "Desocupação, homens", "%", "dif", casas=1),
    _s("taxa_desocupacao_sexo_mulheres", "Desocupação, mulheres", "%", "dif", casas=1),
    _s("taxa_subutil_composta_idade_14_17", "Subutilização composta, 14 a 17 anos", "%", "dif", casas=1),
    _s("taxa_subutil_composta_idade_18_24", "Subutilização composta, 18 a 24 anos", "%", "dif", casas=1),
    # a única série de horas trabalhadas (T4, 2.7)
    *[_s(f"horas_habitual_trabalho_principal_posicao_{k}", f"Horas habituais, {rot}", "horas/semana", "dif",
         casas=1) for k, rot in (("empregado", "empregado"), ("conta_propria", "conta própria"),
                                 ("empregador", "empregador"))],
    *[_s(f"horas_efetivo_trabalho_principal_posicao_{k}", f"Horas efetivas, {rot}", "horas/semana", "dif",
         casas=1) for k, rot in (("empregado", "empregado"), ("conta_propria", "conta própria"))],
    # rendimento por grupo de ocupação
    *[_s(f"rend_habitual_trabalho_principal_ocupacao_{k}", f"Rendimento habitual: {rot}", "R$", "pct", casas=0)
      for k, rot in (("diretores_gerentes", "diretores e gerentes"),
                     ("profissionais_ciencias", "profissionais das ciências"),
                     ("servicos_vendedores", "serviços e vendedores"),
                     ("ocupacoes_elementares", "ocupações elementares"))],
)

_RTN = (("seguro_desemprego", "Seguro-desemprego"), ("abono", "Abono salarial"),
        ("obrigatorias_com_controle_de_fluxo_bolsa_familia", "Bolsa Família"),
        ("beneficios_de_prestacao_continuada_da_loas_rmv", "BPC (LOAS/RMV)"),
        ("pessoal_encargos_sociais", "Pessoal e encargos sociais"))

_PIB_SETOR = (
    ("pib_pm", "PIB"), ("valor_adicionado", "Valor adicionado"), ("agropecuaria", "Agropecuária"),
    ("industria", "Indústria"), ("ind_transformacao", "Indústria de transformação"),
    ("ind_extrativas", "Indústria extrativa"), ("eletricidade_gas_agua", "Eletricidade, gás e água"),
    ("construcao", "Construção"), ("servicos", "Serviços"), ("comercio", "Comércio"),
    ("transporte_correio", "Transporte e correio"), ("informacao_comunicacao", "Informação e comunicação"),
    ("financeiras_seguros", "Financeiras e seguros"), ("imobiliarias", "Imobiliárias"),
    ("adm_saude_educacao_pub", "Administração pública, saúde e educação"),
    ("outros_servicos", "Outros serviços"))


# ── leituras combinadas ───────────────────────────────────────────────────────
def desocupacao_decomposta(ctx: Ctx) -> list[str]:
    """A variação de 12 meses da taxa de desocupação, aberta no que veio do emprego e no que veio da
    força de trabalho (mapa, 2.2). u = 1 − O/L. Com o emprego novo e a força de trabalho de antes,
    o efeito do emprego é −ΔO/L₀; o que sobra do Δu é o da força de trabalho (e inclui o cruzamento
    dos dois). Contra o mesmo mês do ano anterior, porque a PNAD não é dessazonalizada."""
    o, d = ctx.serie("mt_pnad", "ocupado"), ctx.serie("mt_pnad", "desocupado")
    if o.empty or d.empty:
        return ["### Variação da desocupação: emprego e força de trabalho", "", "Sem dado no corte."]
    L = (o + d).dropna()
    linhas = []
    for t1 in L.index[-6:][::-1]:
        t0 = antes(t1, 12)
        if t0 not in L.index:
            continue
        u1, u0 = d[t1] / L[t1] * 100, d[t0] / L[t0] * 100
        emp = -(o[t1] - o[t0]) / L[t0] * 100
        linhas.append({"Trimestre móvel até": f"{t1:%Y-%m}", "Desocupação (%)": fmt(u1, 1),
                       "Δ 12m (p.p.)": fmt(u1 - u0, 2, True),
                       "Efeito do emprego (p.p.)": fmt(emp, 2, True),
                       "Efeito da força de trabalho (p.p.)": fmt(u1 - u0 - emp, 2, True),
                       "Δ% ocupados": fmt((o[t1] / o[t0] - 1) * 100, 1, True),
                       "Δ% força de trabalho": fmt((L[t1] / L[t0] - 1) * 100, 1, True)})
    return ["### Variação da desocupação: emprego e força de trabalho", "",
            "Variação de 12 meses da taxa (mesmo trimestre móvel do ano anterior), em p.p.; positivo "
            "= sobe a desocupação. **Efeito do emprego** = −Δocupados ÷ força de trabalho de um ano "
            "antes (mais ocupados, menos desocupação). **Efeito da força de trabalho** = o resto (mais "
            "gente na força de trabalho, mais desocupação, e o cruzamento dos dois). Uma taxa que cai "
            "porque a força de trabalho encolhe não é aperto.", ""] + md_tabela(linhas)


def saldo_setorial_12m(ctx: Ctx) -> list[str]:
    """O saldo do Novo CAGED dos últimos 12 meses por setor, contra os 12 meses anteriores, e o que o
    explica: admissões e desligamentos de cada janela (mapa, 2.6). Hiring antes de firing: queda de
    admissões com desligamentos estáveis é desaceleração cedo."""
    df = ctx.ler("mt_caged_setor")
    if df.empty:
        return ["### Saldo do CAGED por setor, 12 meses", "", "Sem dado no corte."]
    t1 = df["date"].max()
    j1 = (df["date"] > antes(t1, 12)) & (df["date"] <= t1)
    j0 = (df["date"] > antes(t1, 24)) & (df["date"] <= antes(t1, 12))
    if df.loc[j0, "date"].nunique() < 12:
        return ["### Saldo do CAGED por setor, 12 meses", "", "Menos de 24 meses de dado: sem comparação."]

    def soma(j, metrica):
        x = df[j & (df["metrica"] == metrica)]
        return x.groupby("categoria")["value"].sum() / _BI

    adm1, des1, sal1 = soma(j1, "admissoes"), soma(j1, "desligamentos"), soma(j1, "saldo")
    adm0, des0, sal0 = soma(j0, "admissoes"), soma(j0, "desligamentos"), soma(j0, "saldo")
    linhas = []
    for c in sal1.sort_values(ascending=False).index:
        if c in ("nao_identificado",):
            continue
        g = lambda s: float(s.get(c, float("nan")))
        linhas.append({"Setor": _SETOR.get(c, c), "Saldo 12m": fmt(g(sal1), 1),
                       "Saldo 12m anteriores": fmt(g(sal0), 1),
                       "Δ": fmt(g(sal1) - g(sal0), 1, True),
                       "Admissões 12m": fmt(g(adm1), 0), "Δ adm.": fmt(g(adm1) - g(adm0), 0, True),
                       "Desligamentos 12m": fmt(g(des1), 0), "Δ deslig.": fmt(g(des1) - g(des0), 0, True)})
    tot = {"Setor": "**Total**", "Saldo 12m": fmt(float(sal1.sum()), 1),
           "Saldo 12m anteriores": fmt(float(sal0.sum()), 1),
           "Δ": fmt(float(sal1.sum() - sal0.sum()), 1, True),
           "Admissões 12m": fmt(float(adm1.sum()), 0), "Δ adm.": fmt(float(adm1.sum() - adm0.sum()), 0, True),
           "Desligamentos 12m": fmt(float(des1.sum()), 0),
           "Δ deslig.": fmt(float(des1.sum() - des0.sum()), 0, True)}
    return [f"### Saldo do CAGED por setor, 12 meses até {fdata(t1)}", "",
            "Mil empregos, Novo CAGED por seção CNAE, ordenado pelo saldo dos últimos 12 meses. "
            "Colunas Δ: contra os 12 meses imediatamente anteriores. Setor com admissões caindo e "
            "desligamentos estáveis está desacelerando; desligamentos subindo é fase mais tardia.",
            ""] + md_tabela(linhas + [tot])


COMBINADAS = [desocupacao_decomposta, saldo_setorial_12m]


# ── a declaração ──────────────────────────────────────────────────────────────
TABELAS: list[Tabela] = [
    # ── i. Endógeno (leitura completa) ───────────────────────────────────────
    de(pm, "mt_pnad", series=de(pm, "mt_pnad").series + _PNAD_EXTRA),
    de(pm, "mt_desocupacao_retro"),
    de(pm, "mt_caged", series=(
        _s("caged_total", "Estoque de emprego formal", "mil empregos", "pct", escala=_BI, casas=0),
        *de(pm, "mt_caged").series[1:],
        *[_s(k, rot, "mil empregos", "pct", escala=_BI, casas=0) for k, rot in _CAGED_ESTOQUE])),
    de(pm, "mt_caged_setor", series=tuple(
        _s(f"{k}|saldo", f"Saldo: {rot}", "mil empregos", "fluxo", escala=_BI, casas=1)
        for k, rot in _SETOR.items() if k != "organismos_internacionais")),
    Tabela("mt_pnad_trimestral", filtro="region = 'Brasil'", series=_PNAD_TRI),
    Tabela("mt_caged_uf", dims=("categoria", "metrica"), especial=_enxuta("mt_caged_uf"), series=tuple(
        _s(f"{uf}|saldo", f"Saldo: {uf}", "mil empregos", "fluxo", escala=_BI, casas=1) for uf in _UFS)),
    Tabela("mt_caged_salario", dims=("categoria", "metrica"), especial=_enxuta("mt_caged_salario"),
           nota="As faixas são múltiplos do salário mínimo, reajustado todo janeiro: elas saltam nesse mês.",
           series=tuple(_s(f"{k}|saldo", f"Saldo: {rot}", "mil empregos", "fluxo", escala=_BI, casas=1)
                        for k, rot in _FAIXAS)),
    # ── ii. Endógeno de atividade ────────────────────────────────────────────
    de(pm, "pm_hiato_produto"),
    de(pm, "atv_pib", series=tuple(_s(f"{k}|Y", rot, "índice, dessaz.", "pct") for k, rot in _PIB_SETOR)),
    de(pm, "atv_pib_taxas"),
    de(atividade, "atv_ibcbr"),
    de(atividade, "atv_pim"),
    de(atividade, "atv_pmc"),
    de(atividade, "atv_pms"),
    # ── iii. Endógeno de inflação ────────────────────────────────────────────
    de(inflacao, "inflc_agregados", especial=None, series=(
        _s("ipca", "IPCA", "%", "var_mensal"), _s("ipca_servicos", "Serviços", "%", "var_mensal"),
        _s("ipca_nucleo_ex03_servicos", "Serviços subjacentes (núcleo EX3, serviços)", "%", "var_mensal"))),
    # ── iv. Endógeno de expectativas ─────────────────────────────────────────
    de(atividade, "expc_focus_periodo", recorte="desocupação"),
    de(atividade, "expc_qpc"),
    # ── v. Endógeno de fiscal ────────────────────────────────────────────────
    de(fiscal, "fisc_rtn", especial=None, series=tuple(
        _s(k, rot, "R$ bi", "fluxo", escala=_BI, casas=1) for k, rot in _RTN)),
    # ── vi. Endógeno de crédito ──────────────────────────────────────────────
    # Vem da política monetária até o agente de crédito existir; então passa a `de(credito, ...)`.
    # O rótulo é do PM, com a escala corrigida: a coluna vai de −2 a +2 (o COMMENT do banco), não −1 a 1.
    de(pm, "cred_ptc", series=tuple(
        _s(f"{seg}_{lado}_observada", f"{rot}: {lado}, observada", "índice, −2 a +2", "dif")
        for seg, rot in (("pfc", "PF consumo"), ("pfh", "PF habitação"), ("ge", "Grandes empresas"),
                         ("mpme", "Micro, pequenas e médias"))
        for lado in ("oferta", "demanda"))),
]
