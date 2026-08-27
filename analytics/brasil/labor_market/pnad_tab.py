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

So visualizacao nesta rodada (a pedido explicito do usuario -- "For now, I
don't want to create metrics like Okun, just visualize the data"): Nivel e
Var. anual pre-computados em Python (analytics/brasil/labor_market/
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

--- Seletor de Frequencia (2026-08-27) -------------------------------------

Cada tabela tem DOIS seletores, Frequencia x Metrica, e a chave da variante e a
concatenacao dos dois ("mensal__yoy") -- ver transforms.py. Na visao Mensal so
aparecem as linhas de mt_pnad; na Trimestral aparecem todas, no eixo trimestral
(as de mt_pnad reamostradas por to_quarterly()). O filtro e por AUSENCIA de
dado, nao por marcacao na arvore: o JS esconde o no que nao tem serie na
frequencia corrente nem descendente que tenha. Assim uma linha nunca aparece
como fila de travessoes, que era a queixa que originou o seletor.

--- Unidades (2026-08-27) --------------------------------------------------

Cada folha carrega `unit` (unidade curta, mostrada ao lado do rotulo na tabela
so na visao Nivel) e `def` (a DEFINICAO curta, que vira o titulo do eixo Y do
grafico -- "desocupados / forca de trabalho, %" em vez de so "%"). A pedido do
usuario: "a taxa de desocupacao mede o que? o percentual de desempregados vis a
vis a forca de trabalho".

Os numeradores/denominadores nao foram copiados da documentacao do IBGE, foram
RECONSTRUIDOS dos niveis da propria mt_pnad e conferidos (2026-08-27): as 10
taxas fecham com MAE ~0,025 p.p., que e exatamente o arredondamento de 1 decimal
da fonte. Duas surpresas que a checagem pegou:
  - `taxa_subocupacao_horas` e subocupados / OCUPADOS (MAE 0,024), nao
    subocupados / forca de trabalho (0,604) nem / forca ampliada (0,949);
  - `nivel_ocupacao`/`nivel_desocupacao` tem denominador populacao 14+, nao
    forca de trabalho -- e por isso `nivel_desocupacao` != `taxa_desocupacao`.
`pct_desalentados` e desalentados / (forca de trabalho + desalentados), a
"forca de trabalho potencial" do denominador da publicacao.
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
    "priv_excl_domestico_com_carteira": "Privado, com carteira",
    "priv_excl_domestico_sem_carteira": "Privado, sem carteira",
    "domestico_com_carteira": "Doméstico, com carteira",
    "domestico_sem_carteira": "Doméstico, sem carteira",
    "pub_excl_militar_com_carteira": "Público, com carteira",
    "pub_excl_militar_sem_carteira": "Público, sem carteira",
    "pub_militar_estatutario": "Militar e estatutário",
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
    "inform_comun_financ_imob_prof_adm": "Informação, finanças e serv. profissionais",
    "admpub_educ_saude_segsoc": "Adm. pública, educação e saúde",
    "outros_servicos": "Outros serviços",
    "servicos_domesticos": "Serviços domésticos",
}

# --- Unidades ----------------------------------------------------------------
# (unidade curta para a tabela, definicao curta para o eixo Y do grafico).
# Denominadores reconstruidos e conferidos contra os niveis -- ver docstring.

_U_MILP = ("mil pessoas", "mil pessoas")
_U_REND = ("R$/mês", "rendimento médio mensal, R$ por pessoa")
_U_MASSA = ("R$ mi/mês", "massa de rendimento mensal, R$ milhões")

_UNITS = {
    "taxa_desocupacao":                 ("%", "desocupados / força de trabalho, %"),
    "taxa_participacao":                ("%", "força de trabalho / população 14+, %"),
    "taxa_informalidade":               ("%", "ocupados informais / total de ocupados, %"),
    "nivel_ocupacao":                   ("%", "ocupados / população 14+, %"),
    "nivel_desocupacao":                ("%", "desocupados / população 14+, %"),
    "taxa_subutil_combinada_horas":     ("%", "(desocupados + subocupados) / força de trabalho, %"),
    "taxa_subutil_combinada_potencial": ("%", "(desocupados + força potencial) / força ampliada, %"),
    "taxa_subutil_composta":            ("%", "(desocupados + subocupados + força potencial) / força ampliada, %"),
    "taxa_subocupacao_horas":           ("%", "subocupados por horas / total de ocupados, %"),
    "pct_desalentados":                 ("%", "desalentados / (força de trabalho + desalentados), %"),
    "pct_contribuintes_previdencia":    ("%", "contribuintes da previdência / ocupados, %"),
    "ocupado":                          _U_MILP,
    "desocupado":                       _U_MILP,
    "fora_da_forca_trabalho":           _U_MILP,
    "ocup_informal":                    _U_MILP,
    "subutil_subocupado_horas":         _U_MILP,
    "subutil_forca_potencial":          _U_MILP,
    "subutil_desalentado":              _U_MILP,
}


def _unit_of(series_key: str) -> tuple[str, str]:
    """Unidade de uma seriesKey. Exata para os indicadores de _UNITS; por
    prefixo para as familias grandes (ocup_/rend_/massa_) e para os cortes
    demograficos de mt_pnad_trimestral (`taxa_desocupacao_sexo_homens` herda a
    unidade de `taxa_desocupacao` -- e a mesma variavel do IBGE, so quebrada)."""
    if series_key in _UNITS:
        return _UNITS[series_key]
    for base, unit in _UNITS.items():
        if series_key.startswith(f"{base}_"):
            return unit
    if series_key.startswith("massa_"):
        return _U_MASSA
    if series_key.startswith("rend_"):
        return _U_REND
    if series_key.startswith("ocup_"):
        return _U_MILP
    return ("", "")


# --- Informacao por linha: nome oficial + explicacao -------------------------
# O rotulo da linha e curto (senao a coluna da tabela deforma); o nome completo
# da fonte e a definicao vivem aqui e aparecem num card ao passar o mouse / ao
# clicar no botao de informacao ao lado do rotulo -- pedido do usuario
# (2026-08-27): "algumas linhas poderiam ter um nome mais simples com um card
# descritivo quando passa o mouse por cima ... assim nao precisa escrever tudo
# na linha e deixar a tabela deformada".
#
# seriesKey -> (nome oficial na fonte, explicacao). Qualquer um dos dois pode
# ser "". Linha sem entrada aqui nao ganha botao -- o rotulo ja basta.
# Os nomes oficiais vieram dos metadados da API do IBGE (agregados 6379-6441,
# 8513, 3919, 6318, 6438, 6320/6323, 6389/6391, 6390/6392), nao de memoria.

_INFO = {
    "taxa_desocupacao": (
        "Taxa de desocupação, na semana de referência, das pessoas de 14 anos ou mais de idade",
        "Parcela da força de trabalho que procurou trabalho e estava disponível para trabalhar na "
        "semana de referência. Quem não procurou está fora da força de trabalho e não entra em "
        "nenhum dos dois lados da conta — é por isso que a taxa pode cair sem que ninguém tenha "
        "sido contratado.",
    ),
    "taxa_participacao": (
        "Taxa de participação na força de trabalho, na semana de referência, das pessoas de 14 anos ou mais de idade",
        "Quanto da população em idade de trabalhar está na força de trabalho, ocupada ou "
        "procurando. Sobe quando quem estava fora volta a procurar — o que costuma empurrar a "
        "taxa de desocupação para cima no curto prazo.",
    ),
    "taxa_informalidade": (
        "Taxa de informalidade das pessoas de 14 anos ou mais de idade ocupadas na semana de referência",
        "Empregados sem carteira, empregadores e conta própria sem CNPJ e trabalhadores "
        "familiares auxiliares, sobre o total de ocupados.",
    ),
    "nivel_ocupacao": (
        "Nível da ocupação, na semana de referência, das pessoas de 14 anos ou mais de idade",
        "Não confundir com a taxa de desocupação: aqui o denominador é a população de 14 anos ou "
        "mais, não a força de trabalho. Mede quanto da população adulta está de fato trabalhando.",
    ),
    "nivel_desocupacao": (
        "Nível da desocupação, na semana de referência, das pessoas de 14 anos ou mais de idade",
        "Desocupados sobre a população de 14 anos ou mais — denominador diferente do da taxa de "
        "desocupação (que usa a força de trabalho), por isso os dois números não coincidem.",
    ),
    "taxa_subutil_combinada_horas": (
        "Taxa combinada de desocupação e de subocupação por insuficiência de horas trabalhadas, "
        "na semana de referência, das pessoas de 14 anos ou mais de idade",
        "Soma desocupados e subocupados por insuficiência de horas, sobre a força de trabalho. "
        "É a taxa de desocupação ampliada para incluir quem trabalha menos do que gostaria.",
    ),
    "taxa_subutil_combinada_potencial": (
        "Taxa combinada de desocupação e força de trabalho potencial, na semana de referência, "
        "das pessoas de 14 anos ou mais de idade",
        "A força de trabalho potencial são pessoas fora da força que gostariam de trabalhar mas "
        "não procuraram, ou procuraram e não estavam disponíveis. O denominador é a força "
        "ampliada (força de trabalho + potencial).",
    ),
    "taxa_subutil_composta": (
        "Taxa composta de subutilização da força de trabalho, na semana de referência, das "
        "pessoas de 14 anos ou mais de idade",
        "A medida mais ampla de ociosidade: desocupados + subocupados por horas + força de "
        "trabalho potencial, sobre a força ampliada. Roda bem acima da taxa de desocupação.",
    ),
    "taxa_subocupacao_horas": (
        "Taxa de subocupação por insuficiência de horas trabalhadas, na semana de referência, "
        "das pessoas de 14 anos ou mais de idade",
        "Ocupados que trabalham menos de 40 horas semanais, gostariam de trabalhar mais e "
        "estavam disponíveis para isso. O denominador é o total de ocupados (conferido contra os "
        "níveis da própria PNAD — não é a força de trabalho).",
    ),
    "pct_desalentados": (
        "Percentual de pessoas desalentadas na população de 14 anos ou mais de idade na força de "
        "trabalho ou desalentada, na semana de referência",
        "Desalentados desistiram de procurar por não achar trabalho na região, não ter a "
        "qualificação exigida ou ser considerado jovem/idoso demais. Não são contados como "
        "desocupados justamente porque não procuraram.",
    ),
    "pct_contribuintes_previdencia": (
        "Percentual de pessoas contribuintes de instituto de previdência em qualquer trabalho na "
        "população de 14 anos ou mais de idade ocupada na semana de referência",
        "Leitura de formalidade complementar à taxa de informalidade: contribuir para a "
        "previdência em qualquer trabalho, mesmo sem carteira assinada, conta aqui.",
    ),
    "subutil_forca_potencial": (
        "Pessoas de 14 anos ou mais de idade na força de trabalho potencial",
        "Fora da força de trabalho, mas gostariam de trabalhar — não procuraram, ou procuraram e "
        "não estavam disponíveis. É a reserva que volta a pressionar a taxa de desocupação "
        "quando o mercado melhora.",
    ),
    "subutil_desalentado": (
        "Pessoas de 14 anos ou mais de idade desalentadas",
        "Subconjunto da força de trabalho potencial: desistiram de procurar por motivo ligado ao "
        "próprio mercado de trabalho.",
    ),
    "subutil_subocupado_horas": (
        "Pessoas de 14 anos ou mais de idade subocupadas por insuficiência de horas trabalhadas",
        "Ocupadas, mas trabalhando menos de 40 horas semanais e disponíveis para trabalhar mais.",
    ),
    "ocup_informal": (
        "Pessoas de 14 anos ou mais de idade ocupadas em situação de informalidade",
        "Mesmo conceito da taxa de informalidade, em nível: sem carteira, sem CNPJ ou trabalhador "
        "familiar auxiliar.",
    ),
    "fora_da_forca_trabalho": (
        "Pessoas de 14 anos ou mais de idade fora da força de trabalho",
        "Nem ocupadas nem procurando: estudantes, aposentados, quem cuida da casa, e a força de "
        "trabalho potencial. Não entra em nenhum lado da taxa de desocupação.",
    ),
    "ocup_priv_excl_domestico_com_carteira": (
        "Empregado no setor privado, exclusive trabalhador doméstico, com carteira de trabalho assinada", ""),
    "ocup_priv_excl_domestico_sem_carteira": (
        "Empregado no setor privado, exclusive trabalhador doméstico, sem carteira de trabalho assinada", ""),
    "ocup_domestico_com_carteira": ("Trabalhador doméstico com carteira de trabalho assinada", ""),
    "ocup_domestico_sem_carteira": ("Trabalhador doméstico sem carteira de trabalho assinada", ""),
    "ocup_pub_excl_militar_com_carteira": (
        "Empregado no setor público, exclusive militar e servidor estatutário, com carteira de trabalho assinada", ""),
    "ocup_pub_excl_militar_sem_carteira": (
        "Empregado no setor público, exclusive militar e servidor estatutário, sem carteira de trabalho assinada", ""),
    "ocup_pub_militar_estatutario": ("Militar e servidor estatutário", ""),
    "ocup_inform_comun_financ_imob_prof_adm": (
        "Informação, comunicação e atividades financeiras, imobiliárias, profissionais e administrativas", ""),
    "ocup_admpub_educ_saude_segsoc": (
        "Administração pública, defesa, seguridade social, educação, saúde humana e serviços sociais", ""),
    "rend_inform_comun_financ_imob_prof_adm": (
        "Informação, comunicação e atividades financeiras, imobiliárias, profissionais e administrativas", ""),
    "rend_admpub_educ_saude_segsoc": (
        "Administração pública, defesa, seguridade social, educação, saúde humana e serviços sociais", ""),
    "rend_priv_excl_domestico_com_carteira": (
        "Empregado no setor privado, exclusive trabalhador doméstico, com carteira de trabalho assinada", ""),
    "rend_priv_excl_domestico_sem_carteira": (
        "Empregado no setor privado, exclusive trabalhador doméstico, sem carteira de trabalho assinada", ""),
    "rend_pub_excl_militar_com_carteira": (
        "Empregado no setor público, exclusive militar e servidor estatutário, com carteira de trabalho assinada", ""),
    "rend_pub_excl_militar_sem_carteira": (
        "Empregado no setor público, exclusive militar e servidor estatutário, sem carteira de trabalho assinada", ""),
    "rend_pub_militar_estatutario": ("Militar e servidor estatutário", ""),
    "rend_domestico_com_carteira": ("Trabalhador doméstico com carteira de trabalho assinada", ""),
    "rend_domestico_sem_carteira": ("Trabalhador doméstico sem carteira de trabalho assinada", ""),
    "rend_habitual_real_todos_trabalhos": (
        "Rendimento médio mensal real habitualmente recebido em todos os trabalhos",
        "Habitual é o que a pessoa costuma receber; efetivo é o que recebeu naquele mês (afetado "
        "por férias, licenças, atrasos). Real é deflacionado a preços do último período.",
    ),
    "rend_efetivo_real_todos_trabalhos": (
        "Rendimento médio mensal real efetivamente recebido em todos os trabalhos",
        "Efetivo captura o que entrou no bolso no mês, inclusive quedas por afastamento — mais "
        "volátil que o habitual.",
    ),
    "massa_real_habitual": (
        "Massa de rendimento mensal real habitualmente recebida em todos os trabalhos",
        "Rendimento médio × número de ocupados com rendimento: é a massa que efetivamente vira "
        "consumo, e pode subir com o rendimento médio caindo, se a ocupação crescer mais.",
    ),
}


# --- Construtores de no ------------------------------------------------------

def _leaf(series_key: str, label: str, children: list | None = None, key: str | None = None) -> dict:
    """th.direct() + as duas unidades (curta para a tabela, definicao para o
    eixo) + o nome oficial/explicacao de _INFO, quando houver. Nos so-cabecalho
    (grupos de dimensao) nao passam por aqui."""
    node = th.direct(series_key, label, children, key)
    unit, defin = _unit_of(series_key)
    if unit:
        node["unit"] = unit
        node["def"] = defin
    nome, expl = _INFO.get(series_key, ("", ""))
    # So vira "full" o nome que ACRESCENTA algo ao rotulo curto ja exibido.
    if nome and nome != label:
        node["full"] = nome
    if expl:
        node["desc"] = expl
    return node


def _dim_group(var: str, suffix: str, dim_label: str, categorias: dict) -> dict:
    children = [
        _leaf(f"{var}_{suffix}_{slug}", label)
        for slug, label in categorias.items()
    ]
    # No de dimensao e so-cabecalho (sem serie propria) -- th.direct, nao _leaf.
    return th.direct(f"{var}__dim_{suffix}", dim_label, children)


def _indicador(var: str, label: str, dims: list | None = None) -> dict:
    """No de indicador com "Total" (mt_pnad, a propria seriesKey `var`) + um
    grupo filho por dimensao disponivel em mt_pnad_trimestral (`dims`, lista de
    (suffix, dim_label, categorias) -- None/[] para indicadores so-mensais."""
    children = [_dim_group(var, suffix, dim_label, cats) for suffix, dim_label, cats in (dims or [])]
    return _leaf(var, label, children or None)


def _flat(prefix: str, categorias: dict) -> list[dict]:
    """Lista de folhas de raiz (sem no-agrupador) -- usado quando o titulo do
    card da tabela ja diz o que agrupa (ex.: "Ocupação por Atividade"), entao a
    arvore em si nao precisa repetir esse rotulo num no-cabecalho proprio."""
    return [_leaf(f"{prefix}{slug}", label) for slug, label in categorias.items()]


# --- Controles ---------------------------------------------------------------
# Dois seletores por tabela, NA ORDEM: Frequencia x Metrica -- a chave da
# variante e a concatenacao ("mensal__yoy", ver transforms.py). O rotulo da
# metrica a/a muda com o tipo de serie da tabela, porque a unidade muda: em
# tabela de taxa e uma DIFERENCA em p.p., em tabela de nivel/R$ e uma variacao
# percentual, e em tabela mista e uma coisa em cada linha (dai `ymode: "diff"`,
# que faz o JS resolver por serie).

_CTRL_FREQ = {
    "key": "freq", "label": "Frequência",
    "options": [
        {"value": "mensal", "label": "Mensal (trimestre móvel)", "dateFmt": "mes"},
        {"value": "trimestral", "label": "Trimestral", "dateFmt": "trimestre"},
    ],
}


def _ctrl_metrica(label_level: str, label_yoy: str) -> dict:
    return {
        "key": "metric", "label": "Métrica",
        "options": [
            {"value": "level", "label": label_level, "fmt": "auto", "ymode": "unit"},
            {"value": "yoy", "label": label_yoy, "fmt": "auto", "ymode": "diff"},
        ],
    }


# Tabela 100% taxa chama a coluna de nivel de "Taxa" ("taxa de desocupacao:
# nivel deve ser taxa e diferenca Y/Y"); nas outras "Nivel" continua certo,
# porque ali o nivel e mil pessoas ou R$, nao uma razao.
_CTRLS_TAXA  = [_CTRL_FREQ, _ctrl_metrica("Taxa", "Diff Y/Y")]         # tabelas 100% taxa
_CTRLS_NIVEL = [_CTRL_FREQ, _ctrl_metrica("Nível", "Var. % Y/Y")]      # tabelas 100% nivel/R$
_CTRLS_MISTA = [_CTRL_FREQ, _ctrl_metrica("Nível", "Var. Y/Y")]        # taxa e nivel na mesma


# --- Tabelas por aba ---------------------------------------------------------
# Cada tabela: {key, label, tree, default_checked, controls}. `key` so precisa
# ser unico dentro da propria aba -- report.html prefixa com a chave da aba para
# montar ids de DOM (ex.: "taxas__desocupacao").

_TAB_TAXAS = [
    {
        "key": "desocupacao", "label": "Taxa de Desocupação",
        "tree": [_indicador("taxa_desocupacao", "Taxa de Desocupação", _DIMS_COMPLETAS)],
        "default_checked": ["taxa_desocupacao"],
        "controls": _CTRLS_TAXA,
        # Cabecalho dentro do card do grafico, para ele se explicar sozinho num
        # print (o h2 do card fica atras da barra de controles e da tabela).
        # 2026-08-27: so esta tabela tem, como amostra para o usuario aprovar.
        "chart_title": "Taxa de Desocupação — Brasil",
        "chart_source": "Fonte: IBGE, PNAD Contínua",
    },
    {
        "key": "participacao", "label": "Taxa de Participação na Força de Trabalho",
        "chart_title": "Taxa de Participação na Força de Trabalho — Brasil",
        "chart_source": "Fonte: IBGE, PNAD Contínua",
        "tree": [_indicador("taxa_participacao", "Taxa de Participação na Força de Trabalho", _DIMS_COMPLETAS)],
        "default_checked": ["taxa_participacao"],
        "controls": _CTRLS_TAXA,
    },
    {
        "key": "informalidade", "label": "Taxa de Informalidade",
        "chart_title": "Taxa de Informalidade — Brasil",
        "chart_source": "Fonte: IBGE, PNAD Contínua",
        "tree": [_indicador("taxa_informalidade", "Taxa de Informalidade", _DIMS_COMPLETAS)],
        "default_checked": ["taxa_informalidade"],
        "controls": _CTRLS_TAXA,
    },
    {
        "key": "subutilizacao", "label": "Subutilização da Força de Trabalho",
        "chart_title": "Subutilização da Força de Trabalho — Brasil",
        "chart_source": "Fonte: IBGE, PNAD Contínua",
        "tree": [
            _indicador("taxa_subutil_combinada_horas", "Taxa Combinada — Horas", _DIMS_SEXO_IDADE),
            _indicador("taxa_subutil_combinada_potencial", "Taxa Combinada — Força Potencial", _DIMS_SEXO_IDADE),
            _indicador("taxa_subutil_composta", "Taxa Composta de Subutilização", _DIMS_SEXO_IDADE),
            _indicador("taxa_subocupacao_horas", "Taxa de Subocupação por Horas"),
            _indicador("pct_desalentados", "Desalentados"),
            _leaf("subutil_subocupado_horas", "Subocupados por Horas"),
            _leaf("subutil_forca_potencial", "Força de Trabalho Potencial"),
            _leaf("subutil_desalentado", "Pessoas Desalentadas"),
        ],
        "default_checked": ["taxa_subutil_composta"],
        "controls": _CTRLS_MISTA,
    },
]

_TAB_OCUPACAO = [
    {
        "key": "niveis", "label": "Ocupação e Desocupação (Níveis)",
        "chart_title": "Ocupação e Desocupação — Brasil",
        "chart_source": "Fonte: IBGE, PNAD Contínua",
        "tree": [
            _indicador("nivel_ocupacao", "Nível da Ocupação", _DIMS_COMPLETAS),
            _indicador("nivel_desocupacao", "Nível da Desocupação", _DIMS_COMPLETAS),
            _leaf("ocupado", "Pessoas Ocupadas"),
            _leaf("desocupado", "Pessoas Desocupadas"),
            _leaf("fora_da_forca_trabalho", "Fora da Força de Trabalho"),
        ],
        "default_checked": ["ocupado", "desocupado"],
        "controls": _CTRLS_MISTA,
    },
    {
        "key": "posicao", "label": "Ocupação por Posição na Ocupação",
        "chart_title": "Ocupação por Posição na Ocupação — Brasil",
        "chart_source": "Fonte: IBGE, PNAD Contínua",
        "tree": _flat("ocup_", _POSICAO_LABELS),
        "default_checked": ["ocup_priv_excl_domestico_com_carteira"],
        "controls": _CTRLS_NIVEL,
    },
    {
        "key": "atividade", "label": "Ocupação por Atividade",
        "chart_title": "Ocupação por Atividade — Brasil",
        "chart_source": "Fonte: IBGE, PNAD Contínua",
        "tree": _flat("ocup_", _ATIVIDADE_LABELS),
        "default_checked": ["ocup_admpub_educ_saude_segsoc"],
        "controls": _CTRLS_NIVEL,
    },
    {
        "key": "informalidade_previdencia", "label": "Informalidade e Previdência",
        "chart_title": "Informalidade e Previdência — Brasil",
        "chart_source": "Fonte: IBGE, PNAD Contínua",
        "tree": [
            _leaf("ocup_informal", "Ocupados na Informalidade"),
            _leaf("pct_contribuintes_previdencia", "Contribuintes da Previdência"),
        ],
        "default_checked": ["ocup_informal", "pct_contribuintes_previdencia"],
        "controls": _CTRLS_MISTA,
    },
]

_TAB_RENDIMENTO = [
    {
        "key": "medio", "label": "Rendimento Médio",
        "chart_title": "Rendimento Médio do Trabalho — Brasil",
        "chart_source": "Fonte: IBGE, PNAD Contínua",
        "tree": [
            _leaf("rend_habitual_real_todos_trabalhos", "Habitual, real (todos os trabalhos)"),
            _leaf("rend_habitual_nominal_todos_trabalhos", "Habitual, nominal (todos os trabalhos)"),
            _leaf("rend_efetivo_real_todos_trabalhos", "Efetivo, real (todos os trabalhos)"),
            _leaf("rend_efetivo_nominal_todos_trabalhos", "Efetivo, nominal (todos os trabalhos)"),
            _leaf("rend_efetivo_real_trabalho_principal", "Efetivo, real (trabalho principal)"),
        ],
        "default_checked": ["rend_habitual_real_todos_trabalhos"],
        "controls": _CTRLS_NIVEL,
    },
    {
        "key": "posicao", "label": "Rendimento por Posição na Ocupação",
        "chart_title": "Rendimento por Posição na Ocupação — Brasil",
        "chart_source": "Fonte: IBGE, PNAD Contínua",
        "tree": _flat("rend_", {**_REND_POSICAO_LABELS, "media_nacional": "Rendimento médio nacional (todas as posições)"}),
        "default_checked": ["rend_media_nacional"],
        "controls": _CTRLS_NIVEL,
    },
    {
        "key": "atividade", "label": "Rendimento por Atividade",
        "chart_title": "Rendimento por Atividade — Brasil",
        "chart_source": "Fonte: IBGE, PNAD Contínua",
        "tree": _flat("rend_", _ATIVIDADE_LABELS),
        "default_checked": ["rend_admpub_educ_saude_segsoc"],
        "controls": _CTRLS_NIVEL,
    },
    {
        "key": "massa", "label": "Massa de Rendimento",
        "chart_title": "Massa de Rendimento do Trabalho — Brasil",
        "chart_source": "Fonte: IBGE, PNAD Contínua",
        "tree": [
            _leaf("massa_real_habitual", "Habitual, real"),
            _leaf("massa_nominal_habitual", "Habitual, nominal"),
            _leaf("massa_efetiva_real", "Efetivamente recebida, real"),
            _leaf("massa_efetiva_nominal", "Efetivamente recebida, nominal"),
        ],
        "default_checked": ["massa_real_habitual"],
        "controls": _CTRLS_NIVEL,
    },
]

TABS = [
    {"key": "taxas", "label": "Taxas", "tables": _TAB_TAXAS},
    {"key": "ocupacao", "label": "Ocupação", "tables": _TAB_OCUPACAO},
    {"key": "rendimento", "label": "Rendimento", "tables": _TAB_RENDIMENTO},
]

# Todo indicador que TEM corte comeca expandido, para que a visao Trimestral
# mostre de saida quais cortes existem em vez de exigir um clique para revelar
# que ha algo ali ("quando clico trimestral vejo todas as linhas disponiveis").
# Custa nada na visao Mensal, onde esses filhos nao existem e o no nem oferece o
# triangulo. Expande um nivel so -- abrir tambem os grupos de dimensao poria as
# 18 categorias da desocupacao na tela de uma vez.
for _tab in TABS:
    for _table in _tab["tables"]:
        _table.setdefault(
            "default_expanded",
            [n["key"] for n in _table["tree"] if n.get("children")],
        )

# --- Series "rate" (ja em %, variam em p.p.) -- mesmas chaves de mt_pnad.py's
# _SIMPLES. Tudo o mais (niveis em mil pessoas ou R$) varia em % ------------

_RATE_VARS = {
    "taxa_desocupacao", "taxa_participacao", "taxa_informalidade",
    "nivel_ocupacao", "nivel_desocupacao",
    "taxa_subutil_combinada_horas", "taxa_subutil_combinada_potencial", "taxa_subutil_composta",
    "taxa_subocupacao_horas", "pct_desalentados", "pct_contribuintes_previdencia",
}

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
        series[name] = tf.variants_pnad_mensal(s["dates"], s["values"], rate=name in _RATE_VARS)

    for name in DB_NAMES_TRIMESTRAL:
        s = trimestral.get(name)
        if s is None:
            continue
        series[name] = tf.variants_pnad_trimestral(s["dates"], s["values"], rate=True)

    ref_date = mensal["taxa_desocupacao"]["dates"][-1]
    rate_keys = [k for k in series if k in _RATE_VARS or any(k.startswith(f"{v}_") for v in _RATE_VARS)]
    return {"tabs": TABS, "series": series, "ref_date": ref_date, "rate_keys": rate_keys}
