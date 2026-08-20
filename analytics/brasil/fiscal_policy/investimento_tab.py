"""
Monta o dataset da aba "Investimento": investimento do Governo Federal por GND,
`macro_brasil.fisc_investimento` (Tema 13 da API de Series Temporais do Tesouro --
ver domain/db/brasil/tesouro/fisc_investimento.py). Mensal, R$ milhoes correntes,
2008-01 em diante.

## GND: o que a aba mostra

GND = Grupo de Natureza da Despesa. Esta aba cobre so os dois grupos de capital, que
e o que "investimento" significa na estatistica do Tesouro:
  GND 4 -- Investimentos: cria ativo novo (obras, equipamentos) + transferencias de
           capital a estados/DF/municipios.
  GND 5 -- Inversoes Financeiras: so troca a titularidade de um ativo existente
           (participacao no capital, integralizacao de cotas).
Somar os dois numa linha so esconde exatamente a distincao que o corte por GND existe
para mostrar -- o pico de 1,38% do PIB em 2020 e quase todo GND 5 (0,83pp), operacao
financeira, nao investimento que cria ativo. Por isso as duas tabelas trazem GND 4 e
GND 5 marcados por default, separados, e nao o `total`.

## DUAS TABELAS, nao um seletor de corte

`fisc_investimento` tem dois cortes independentes do mesmo agregado (`funcao` e
`natureza`), que compartilham os 4 nos de cima e divergem abaixo. Isso vira DUAS
tabelas+graficos na mesma aba -- mesmo padrao GFSM/RTN da aba "Receitas e Despesas" --
e NAO um seletor de Corte no estilo do `esferaSelectId` da GFSM. O motivo e estrutural:
o seletor de Esfera da GFSM troca o NAMESPACE de uma taxonomia identica entre esferas
(`geral_x` -> `central_x`, mesma arvore), enquanto aqui as duas arvores sao DIFERENTES
abaixo do GND -- trocar o corte teria que trocar a arvore junto, e o estado de
marcado/expandido do usuario apontaria para chaves que nao existem no outro corte
(`gnd4__funcao_saude` nao tem contraparte em `natureza`). Duas tabelas evitam isso sem
generalizar o tratamento de arvore de makeHierTab().

## Quatro modelagens de Nivel, um denominador de %PIB

Cada serie carrega as 4 janelas lado a lado (ver analytics/brasil/fiscal_policy/transforms.py):

    mensal      valor do proprio mes          Y/Y, M/M(STL), T/T(STL)  %PIB / PIB 12m
    trimestral  soma do trimestre calendario  Y/Y, T/T(STL period=4)   %PIB / PIB 12m
    acum12m     soma movel de 12 meses        Y/Y, M/M, T/T            %PIB / PIB 12m
    acum_ano    soma no ano civil (reseta)    Y/Y                      %PIB / PIB 12m

**%PIB usa a convencao B de analytics/metric_layers.md** (escolha explicita do usuario,
2026-08, resolvendo a "Open convention 1" daquele arquivo): o NUMERADOR acompanha a
janela do Nivel, o DENOMINADOR e sempre o PIB acumulado em 12 meses
(`atv_pib_mensal.pib_acum_12m`, SGS 4382). Le-se como "share anualizado do produto", e a
consequencia que interessa e que os quatro Niveis ficam na MESMA escala -- um %PIB lido
no Mensal e comparavel com um lido no Acum. 12m, o que a convencao A (os dois lados na
mesma janela, usada por GFSM/RTN nesta mesma pasta) nao permite. O custo e que o numero
mensal fica pequeno (~1/12 do anual) e precisa da legenda, que esta no caption e no
Apendice.

Isso DIVERGE de GFSM/RTN (convencao A) de proposito -- o usuario escolheu B so para esta
aba; retrofitar as outras duas foi oferecido e nao escolhido. Mesma convencao que
analytics/brasil/credit/ e a aba DLSP ja usam.

**Divergencia deliberada em relacao a RTN: M/M e T/T ficam DISPONIVEIS no Nivel
Acum. 12m aqui.** A RTN desabilita "Marginal" nesse nivel de proposito (ver
analytics/brasil/fiscal_policy/CLAUDE.md), porque a variacao de um acumulado mede a
aceleracao da propria janela, nao mes-contra-mes. Aqui as duas ficam habilitadas por
pedido explicito do usuario ("Y/Y, M/M and Q/Q growth ... for each acumulation"), com
a leitura de aceleracao dita no caption e no Apendice. Nao "corrigir" uma das duas
abas para casar com a outra sem reconfirmar. As unicas exclusoes sao as degeneradas:
M/M no Nivel Trimestral (constante dentro do degrau) e M/M e T/T no Acum. no ano
(atravessariam o reset de janeiro).
"""
from analytics.report_structure import tree_helpers as th

_direct = th.direct

# As 28 funcoes orcamentarias, na ordem do plano de contas do Tesouro (13.1.1.x.NN).
# Identicas nos dois GNDs -- por isso a lista e montada uma vez e reusada com prefixo.
_FUNCOES = [
    ("legislativa", "Legislativa"),
    ("judiciaria", "Judiciária"),
    ("essencial_justica", "Essencial à Justiça"),
    ("administracao", "Administração"),
    ("defesa_nacional", "Defesa Nacional"),
    ("seguranca_publica", "Segurança Pública"),
    ("relacoes_exteriores", "Relações Exteriores"),
    ("assistencia_social", "Assistência Social"),
    ("previdencia_social", "Previdência Social"),
    ("saude", "Saúde"),
    ("trabalho", "Trabalho"),
    ("educacao", "Educação"),
    ("cultura", "Cultura"),
    ("direitos_cidadania", "Direitos da Cidadania"),
    ("urbanismo", "Urbanismo"),
    ("habitacao", "Habitação"),
    ("saneamento", "Saneamento"),
    ("gestao_ambiental", "Gestão Ambiental"),
    ("ciencia_tecnologia", "Ciência e Tecnologia"),
    ("agricultura", "Agricultura"),
    ("organizacao_agraria", "Organização Agrária"),
    ("industria", "Indústria"),
    ("comercio_servicos", "Comércio e Serviços"),
    ("comunicacoes", "Comunicações"),
    ("energia", "Energia"),
    ("transporte", "Transporte"),
    ("desporto_lazer", "Desporto e Lazer"),
    ("encargos_especiais", "Encargos Especiais"),
]


def _funcoes_de(gnd: str) -> list:
    return [_direct(f"{gnd}__funcao_{slug}", label) for slug, label in _FUNCOES]


_GND4_LABEL = "Investimentos (GND 4)"
_GND5_LABEL = "Inversões Financeiras (GND 5)"
_AJUSTE_LABEL = "Ajuste de Ordem Bancária"

# Arvore do corte por funcao orcamentaria (subtema 13.1 -- 60 series).
TREE_FUNCAO = [
    _direct("total", "Investimento Total", [
        _direct("gnd4", _GND4_LABEL, _funcoes_de("gnd4")),
        _direct("gnd5", _GND5_LABEL, _funcoes_de("gnd5")),
        _direct("ajuste_ordem_bancaria", _AJUSTE_LABEL),
    ]),
]

# Arvore do corte por natureza da despesa (subtema 13.2 -- 18 series).
TREE_NATUREZA = [
    _direct("total", "Investimento Total", [
        _direct("gnd4", _GND4_LABEL, [
            _direct("gnd4__aplicacoes_diretas", "Aplicações Diretas da União", [
                _direct("gnd4__aplicacoes_diretas__obras_instalacoes", "Obras e Instalações"),
                _direct("gnd4__aplicacoes_diretas__equipamentos_material_permanente", "Equipamentos e Material Permanente"),
                _direct("gnd4__aplicacoes_diretas__servicos", "Serviços"),
                _direct("gnd4__aplicacoes_diretas__demais", "Demais Aplicações Diretas"),
            ]),
            _direct("gnd4__transf_estados_df", "Transferências a Estados/DF"),
            _direct("gnd4__transf_municipios", "Transferências a Municípios"),
            _direct("gnd4__outras_transferencias", "Outras Transferências"),
        ]),
        _direct("gnd5", _GND5_LABEL, [
            _direct("gnd5__participacao_uniao_capital", "Participação da União no Capital"),
            _direct("gnd5__integralizacao_cotas", "Integralização de Cotas", [
                _direct("gnd5__integralizacao_cotas__fundos_garantidores", "Fundos Garantidores"),
                _direct("gnd5__integralizacao_cotas__organismos_internacionais", "Organismos Internacionais"),
                _direct("gnd5__integralizacao_cotas__outras", "Outras"),
            ]),
            _direct("gnd5__demais", "Demais Inversões Financeiras"),
        ]),
        _direct("ajuste_ordem_bancaria", _AJUSTE_LABEL),
    ]),
]

# corte -> (arvore, itens que existem naquele corte). A lista de itens e derivada da
# propria arvore em _items_da_arvore() -- nao ha segunda lista para desincronizar.
CORTES = {"funcao": TREE_FUNCAO, "natureza": TREE_NATUREZA}

# Marcados por default: GND 4 e GND 5 separados, NAO o total (ver docstring do modulo).
DEFAULT_CHECKED = ["gnd4", "gnd5"]


def _items_da_arvore(tree: list) -> list[str]:
    out = []

    def _walk(nodes):
        for n in nodes:
            out.append(n["seriesKey"])
            if n.get("children"):
                _walk(n["children"])

    _walk(tree)
    return out


def _compact(variantes: dict) -> dict:
    """{basis: {metrica: {"dates", "values"}}} -> {basis: {metrica: [valores]}}.

    Descarta o array de datas de cada variante (todas as 78 series compartilham a mesma
    grade mensal, guardada UMA vez na raiz do payload -- ver a docstring de build()) e
    arredonda: `level` de nominal/real e R$ milhoes, 1 casa (a propria fonte publica 1);
    todo o resto e percentual (Y/Y, M/M, T/T e o `level` do pctpib), 3 casas.

    Uma variante identicamente vazia vira o escalar `null` e uma identicamente zero vira
    o escalar `0`, expandidos de volta no JS por `invArr()` -- mesma compressao dos zeros
    escalares de dlsp_tab.py, e aqui ela pega bastante: a maioria das 28 funcoes
    orcamentarias nunca recebe inversao financeira (GND 5), entao essas series sao zero
    nos 222 meses inteiros.
    """
    out: dict = {}
    for basis, por_metrica in variantes.items():
        out[basis] = {}
        for metrica, v in por_metrica.items():
            casas = 1 if (metrica == "level" and basis != "pctpib") else 3
            vals = [None if x is None else round(float(x), casas) for x in v["values"]]
            if all(x is None for x in vals):
                out[basis][metrica] = None
            elif all(x == 0 for x in vals):
                out[basis][metrica] = 0
            else:
                out[basis][metrica] = vals
    return out


def build(raw: dict, ipca_pct: dict, pib_mensal: dict, pib_acum_12m: dict) -> dict:
    """`raw`: {corte: {item: {"dates", "values"}}} -- exatamente o que
    generate_report.py's _load_investimento_tab_data() monta a partir de
    fisc_investimento. `ipca_pct`: IPCA mensal bruto (inflc_agregados.ipca), para a
    base Real. `pib_mensal`/`pib_acum_12m`: atv_pib_mensal (SGS 4380/4382).

    Retorna:

        {"dates": [...],                      # UMA grade, compartilhada por tudo
         "cortes": {corte: {"tree", "series", "default_checked"}},
         "ref_date": ...}

    onde `series[item][nivel][basis][metrica]` e um array de valores NU (sem datas) --
    ou o escalar `0`/`null` quando a serie inteira e zero/vazia. Essa e a forma compacta
    de dlsp_tab.py, deliberadamente NAO a forma `{dates, values}` por variante que
    makeHierTab() usa para gfsm/rtn: com 78 series x 4 niveis x ate 9 variantes, repetir
    a grade de 222 datas em cada uma custava **15,3 MB** medidos (mais que o relatorio
    inteiro antes desta aba) contra ~1 MB assim. E o mesmo problema que o Pending do
    CLAUDE.md desta pasta registra para `rtn`/`gfsm`; esta aba nasce ja sem ele. O lado
    JS recebe `sharedDates`/`root` em opts para ler esse formato (ver report.html).

    Um bloco por tabela do lado JS, cada um com sua propria arvore e seu proprio dict de
    series (chaveado pelo item nu, sem prefixo de corte, ja que cada tabela resolve
    contra o seu). Levanta se um item da arvore nao existir em `raw`, ou se as series nao
    compartilharem a mesma grade de datas -- um typo de slug silenciosamente viraria uma
    linha vazia na tabela (o bug que analytics/brasil/labor_market/CLAUDE.md documenta ter
    acontecido de verdade), e uma grade divergente desalinharia silenciosamente os
    valores das datas depois de descartar o array por variante.
    """
    from analytics.brasil.credit import transforms as credit_tf
    from analytics.brasil.fiscal_policy import transforms as fiscal_tf

    price_index = fiscal_tf.build_price_index(ipca_pct["dates"], ipca_pct["values"])
    ref_date = ipca_pct["dates"][-1]

    # Convencao B: um unico denominador (PIB 12m) para as 4 janelas -- ver a docstring do
    # modulo. `pib_mensal` continua sendo lido porque e a fonte de onde o proprio
    # pib_acum_12m vem no payload de generate_report.py, mas nao entra em nenhum %PIB.
    gdp_ttm_map = credit_tf.to_date_map(pib_acum_12m)

    grade: list[str] | None = None
    cortes = {}
    for corte, tree in CORTES.items():
        items = _items_da_arvore(tree)
        faltando = [i for i in items if i not in raw.get(corte, {})]
        if faltando:
            raise ValueError(
                f"corte={corte}: itens da arvore ausentes em fisc_investimento: {faltando}"
            )

        series = {}
        for item in items:
            s = raw[corte][item]
            dates, values = s["dates"], s["values"]
            if grade is None:
                grade = dates
            elif dates != grade:
                raise ValueError(
                    f"corte={corte}, item={item}: grade de datas diverge da dos demais "
                    f"({len(dates)} datas, {dates[0]}..{dates[-1]} vs. {len(grade)}, "
                    f"{grade[0]}..{grade[-1]}) -- o payload compacto exige uma grade unica"
                )

            # Os 4 %PIB dividem pelo MESMO denominador (PIB 12m, convencao B); o que muda
            # entre eles e so o numerador, que acompanha a janela do Nivel. Por isso os
            # tres primeiros passam por credit_tf.compute_pct_pib() com o numerador ja
            # agregado, e o acum12m usa o gdp_ttm= do proprio compute_variants_monthly_ttm
            # (que rola o numerador em 12m internamente -- mesmo resultado).
            mensal = credit_tf.compute_variants(dates, values, price_index, ref_date)
            mensal["pctpib"] = {"level": {
                "dates": dates,
                "values": credit_tf.compute_pct_pib(dates, values, gdp_ttm_map),
            }}

            trimestral = fiscal_tf.compute_variants_quarterly_step(
                dates, values, price_index, ref_date, seasonal=True)
            trimestral["pctpib"] = {"level": {
                "dates": dates,
                "values": credit_tf.compute_pct_pib(
                    dates, fiscal_tf.quarterly_step_level(dates, values), gdp_ttm_map),
            }}

            acum12m = fiscal_tf.compute_variants_monthly_ttm(
                dates, values, price_index, ref_date, gdp_ttm=gdp_ttm_map)

            acum_ano = fiscal_tf.compute_variants_ytd(dates, values, price_index, ref_date)
            acum_ano["pctpib"] = {"level": {
                "dates": dates,
                "values": credit_tf.compute_pct_pib(
                    dates, fiscal_tf.ytd_sum(dates, values), gdp_ttm_map),
            }}

            series[item] = {
                "mensal":     _compact(mensal),
                "trimestral": _compact(trimestral),
                "acum12m":    _compact(acum12m),
                "acum_ano":   _compact(acum_ano),
            }

        # ref_date repetido em cada bloco (e nao so na raiz) porque o lado JS le
        # `opts.root().ref_date` para montar o titulo do eixo Y da base Real.
        cortes[corte] = {
            "tree": tree, "series": series,
            "default_checked": DEFAULT_CHECKED, "ref_date": ref_date,
        }

    return {"dates": grade or [], "cortes": cortes, "ref_date": ref_date}
