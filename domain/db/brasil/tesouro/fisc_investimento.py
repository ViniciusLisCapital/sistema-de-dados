"""
Investimento do Governo Federal, mensal, R$ milhoes correntes.

78 series do Tema 13 ("Investimento do Governo Federal") da API de Series
Temporais do Tesouro Nacional -- ver connectors/tesouro_series_temporais.py.
Dois subtemas, que sao DOIS CORTES INDEPENDENTES do mesmo agregado:

    13.1 -> corte "funcao"    (60 series) -- GND x funcao orcamentaria
    13.2 -> corte "natureza"  (18 series) -- GND x natureza da despesa

## GND: o que a tabela cobre e o que deliberadamente nao cobre

GND = Grupo de Natureza da Despesa, a classificacao orcamentaria brasileira que
agrupa a despesa pelo efeito economico. Sao 6 grupos; este tema so tem os dois
de capital, que e o que "investimento" significa aqui:

    GND 4 -- Investimentos: cria ativo novo (obras e instalacoes, equipamentos e
             material permanente), mais as transferencias de capital a
             estados/DF/municipios.
    GND 5 -- Inversoes Financeiras: so troca a titularidade de um ativo que ja
             existe (participacao da Uniao no capital, integralizacao de cotas em
             fundos garantidores/organismos internacionais).

Os outros 4 (1 Pessoal, 2 Juros da Divida, 3 Outras Despesas Correntes,
6 Amortizacao) nao estao neste tema. Para despesa corrente por rubrica use
`fisc_rtn` (Governo Central, Tema 10); por natureza economica GFSM use
`fisc_efgg`.

A distincao GND 4 vs. GND 5 e a mesma que faz o canal parafiscal de credito a
instituicoes financeiras oficiais nao aparecer no resultado primario -- ver o
"Impulso via Credito a Inst. Financ. Oficiais" em analytics/brasil/fiscal_policy/ e
`fisc_dlsp_fatores`.

## Estrutura de cada corte

Os dois cortes compartilham os 4 nos de cima (`total`, `gnd4`, `gnd5`,
`ajuste_ordem_bancaria`) e divergem so abaixo disso:

    total                          INVESTIMENTO TOTAL
      gnd4                         Investimentos (GND 4)
        [corte=funcao]             28 funcoes orcamentarias
        [corte=natureza]           aplicacoes diretas (+4 filhos), transf. a
                                   estados/DF, transf. a municipios, outras
      gnd5                         Inversoes Financeiras (GND 5)
        [corte=funcao]             as mesmas 28 funcoes
        [corte=natureza]           participacao no capital, integralizacao de
                                   cotas (+3 filhos), demais
      ajuste_ordem_bancaria        Ajuste de Ordem Bancaria

Os nos intermediarios sao series proprias da API, com valor proprio -- nao
rotulos. Somar pai e filhos junto double-conta.

## Identidades (todas verificadas ao vivo, 2026-08, desvio exato 0.0)

    total  == gnd4 + gnd5 + ajuste_ordem_bancaria         (nos dois cortes)
    gnd4   == soma dos seus filhos de nivel 1             (28 no corte funcao,
    gnd5   == soma dos seus filhos de nivel 1              4/3 no corte natureza)
    gnd4__aplicacoes_diretas   == soma dos seus 4 filhos
    gnd5__integralizacao_cotas == soma dos seus 3 filhos
    funcao[k] == natureza[k]  para os 4 nos compartilhados

`_validate()` levanta se qualquer uma delas romper acima de R$ 0,01 mi. Nao ha
janela de excecao tolerada aqui (diferente de `fisc_dlsp_fatores`, que tolera a
quebra de revisao historica do BCB em 2003-2004).

## SERIE COMECA EM 2008-01, NAO EM 1997-01 -- a metadata da API mente

`dataInicialSerie` da API diz 1997-01 para todas as 78 series, mas os 132 meses
de 1997-01 a 2006-12 vem com valor 0.0 em TODAS elas -- zero como "sem dado",
nao como "investimento igual a zero", que e implausivel para 11 anos seguidos de
investimento federal. 2007 e um caso hibrido: os 59 componentes do corte funcao e
as 18 series do corte natureza (INCLUSIVE o total, id 8720) sao zero nos 12 meses,
mas a serie de total do corte funcao (id 8420) carrega R$ 21,9 bi no ano. Ou seja,
para 2007 as duas series de total do mesmo tema se contradizem, e nenhuma
decomposicao existe.

`_START` corta em 2008-01 por isso: e o primeiro mes em que as duas series de
total concordam e a decomposicao existe, e e o que faz as identidades acima
fecharem em TODA linha gravada -- que e o que permite a guarda de `_validate()`
ser incondicional. O total de 2007 do corte funcao fica de fora deliberadamente:
gravar um total sem decomposicao, presente num corte e ausente no outro, seria
uma linha que nenhuma consulta pode usar sem uma excecao propria.

## Banco

macro_brasil.fisc_investimento -- PRIMARY KEY (date, corte, item).
78 series x 222 meses (2008-01 -> 2026-06) ~= 17,3 mil linhas.

Zeros DEPOIS de 2008-01 sao gravados como zero, nao omitidos: sao zeros de
verdade (muitas funcoes orcamentarias simplesmente nao recebem inversao
financeira num mes dado, e `ajuste_ordem_bancaria` e zero na maior parte da
serie recente). Mesma decisao de `fisc_dlsp_fatores` -- guardar o zero explicito
evita a convencao implicita "linha ausente = 0".

`run()` faz upsert, NAO truncate. A tabela e alimentada so por este script, mas
`_verify_contract()` confere a arvore inteira dos dois subtemas contra `_ITEMS`
antes de baixar qualquer dado -- se o Tesouro inserir, remover ou renumerar um
no, levanta antes de gravar, entao nao ha risco de linha orfa que justificaria
truncar. Revisao de valor em data ja existente entra pelo ON DUPLICATE KEY UPDATE.
Isso e uma guarda mais forte que a de `fisc_rtn.py`, que mapeia so id -> nome sem
reconferir a arvore: um id reatribuido a outra serie passaria silenciosamente lah.
"""

from __future__ import annotations

import pandas as pd

from connectors.mysql import insert_data_into_database
from connectors.tesouro_series_temporais import SeriesTemporais

_DATABASE = "macro_brasil"
_TABLE = "fisc_investimento"

# Primeiro mes com dado de verdade -- ver "SERIE COMECA EM 2008-01" na docstring.
_START = "2008-01-01"

# corte -> id interno do subtema na API (nao o codigo externo "1"/"2").
_SUBTEMAS = {"funcao": 270, "natureza": 370}

# corte -> {slug do item: (id da serie, planoContas)}. Contrato explicito,
# reconferido a cada execucao por _verify_contract(). planoContas e a chave
# estrutural (posicao na arvore do Tesouro); o id e o que a API usa no download.
_ITEMS: dict[str, dict[str, tuple[int, str]]] = {
    "funcao": {
        "total":                             (8420, "13.1.1"),        # INVESTIMENTO TOTAL
        "gnd4":                              (8421, "13.1.1.1"),      # Investimentos (GND 4)
        "gnd4__funcao_legislativa":          (8422, "13.1.1.1.01"),   # Funcao Legislativa
        "gnd4__funcao_judiciaria":           (8423, "13.1.1.1.02"),   # Funcao Judiciaria
        "gnd4__funcao_essencial_justica":    (8424, "13.1.1.1.03"),   # Funcao Essencial a Justica
        "gnd4__funcao_administracao":        (8425, "13.1.1.1.04"),   # Funcao Administracao
        "gnd4__funcao_defesa_nacional":      (8426, "13.1.1.1.05"),   # Funcao Defesa Nacional
        "gnd4__funcao_seguranca_publica":    (8427, "13.1.1.1.06"),   # Funcao Seguranca Publica
        "gnd4__funcao_relacoes_exteriores":  (8428, "13.1.1.1.07"),   # Funcao Relacoes Exteriores
        "gnd4__funcao_assistencia_social":   (8429, "13.1.1.1.08"),   # Funcao Assistencia Social
        "gnd4__funcao_previdencia_social":   (8430, "13.1.1.1.09"),   # Funcao Previdencia Social
        "gnd4__funcao_saude":                (8431, "13.1.1.1.10"),   # Funcao Saude
        "gnd4__funcao_trabalho":             (8432, "13.1.1.1.11"),   # Funcao Trabalho
        "gnd4__funcao_educacao":             (8433, "13.1.1.1.12"),   # Funcao Educacao
        "gnd4__funcao_cultura":              (8434, "13.1.1.1.13"),   # Funcao Cultura
        "gnd4__funcao_direitos_cidadania":   (8435, "13.1.1.1.14"),   # Funcao Direitos da Cidadania
        "gnd4__funcao_urbanismo":            (8436, "13.1.1.1.15"),   # Funcao Urbanismo
        "gnd4__funcao_habitacao":            (8437, "13.1.1.1.16"),   # Funcao Habitacao
        "gnd4__funcao_saneamento":           (8438, "13.1.1.1.17"),   # Funcao Saneamento
        "gnd4__funcao_gestao_ambiental":     (8439, "13.1.1.1.18"),   # Funcao Gestao Ambiental
        "gnd4__funcao_ciencia_tecnologia":   (8440, "13.1.1.1.19"),   # Funcao Ciencia e Tecnologia
        "gnd4__funcao_agricultura":          (8441, "13.1.1.1.20"),   # Funcao Agricultura
        "gnd4__funcao_organizacao_agraria":  (8442, "13.1.1.1.21"),   # Funcao Organizacao Agraria
        "gnd4__funcao_industria":            (8443, "13.1.1.1.22"),   # Funcao Industria
        "gnd4__funcao_comercio_servicos":    (8444, "13.1.1.1.23"),   # Funcao Comercio e Servicos
        "gnd4__funcao_comunicacoes":         (8445, "13.1.1.1.24"),   # Funcao Comunicacoes
        "gnd4__funcao_energia":              (8446, "13.1.1.1.25"),   # Funcao Energia
        "gnd4__funcao_transporte":           (8447, "13.1.1.1.26"),   # Funcao Transporte
        "gnd4__funcao_desporto_lazer":       (8448, "13.1.1.1.27"),   # Funcao Desporto e Lazer
        "gnd4__funcao_encargos_especiais":   (8449, "13.1.1.1.28"),   # Funcao Encargos Especiais
        "gnd5":                              (8458, "13.1.1.2"),      # Inversoes Financeiras (GND 5)
        "gnd5__funcao_legislativa":          (8459, "13.1.1.2.01"),   # Funcao Legislativa
        "gnd5__funcao_judiciaria":           (8460, "13.1.1.2.02"),   # Funcao Judiciaria
        "gnd5__funcao_essencial_justica":    (8461, "13.1.1.2.03"),   # Funcao Essencial a Justica
        "gnd5__funcao_administracao":        (8462, "13.1.1.2.04"),   # Funcao Administracao
        "gnd5__funcao_defesa_nacional":      (8463, "13.1.1.2.05"),   # Funcao Defesa Nacional
        "gnd5__funcao_seguranca_publica":    (8464, "13.1.1.2.06"),   # Funcao Seguranca Publica
        "gnd5__funcao_relacoes_exteriores":  (8465, "13.1.1.2.07"),   # Funcao Relacoes Exteriores
        "gnd5__funcao_assistencia_social":   (8466, "13.1.1.2.08"),   # Funcao Assistencia Social
        "gnd5__funcao_previdencia_social":   (8467, "13.1.1.2.09"),   # Funcao Previdencia Social
        "gnd5__funcao_saude":                (8468, "13.1.1.2.10"),   # Funcao Saude
        "gnd5__funcao_trabalho":             (8700, "13.1.1.2.11"),   # Funcao Trabalho
        "gnd5__funcao_educacao":             (8701, "13.1.1.2.12"),   # Funcao Educacao
        "gnd5__funcao_cultura":              (8704, "13.1.1.2.13"),   # Funcao Cultura
        "gnd5__funcao_direitos_cidadania":   (8705, "13.1.1.2.14"),   # Funcao Direitos da Cidadania
        "gnd5__funcao_urbanismo":            (8706, "13.1.1.2.15"),   # Funcao Urbanismo
        "gnd5__funcao_habitacao":            (8707, "13.1.1.2.16"),   # Funcao Habitacao
        "gnd5__funcao_saneamento":           (8708, "13.1.1.2.17"),   # Funcao Saneamento
        "gnd5__funcao_gestao_ambiental":     (8710, "13.1.1.2.18"),   # Funcao Gestao Ambiental
        "gnd5__funcao_ciencia_tecnologia":   (8709, "13.1.1.2.19"),   # Funcao Ciencia e Tecnologia
        "gnd5__funcao_agricultura":          (8711, "13.1.1.2.20"),   # Funcao Agricultura
        "gnd5__funcao_organizacao_agraria":  (8712, "13.1.1.2.21"),   # Funcao Organizacao Agraria
        "gnd5__funcao_industria":            (8713, "13.1.1.2.22"),   # Funcao Industria
        "gnd5__funcao_comercio_servicos":    (8981, "13.1.1.2.23"),   # Funcao Comercio e Servicos
        "gnd5__funcao_comunicacoes":         (8714, "13.1.1.2.24"),   # Funcao Comunicacoes
        "gnd5__funcao_energia":              (8715, "13.1.1.2.25"),   # Funcao Energia
        "gnd5__funcao_transporte":           (8716, "13.1.1.2.26"),   # Funcao Transporte
        "gnd5__funcao_desporto_lazer":       (8717, "13.1.1.2.27"),   # Funcao Desporto e Lazer
        "gnd5__funcao_encargos_especiais":   (8718, "13.1.1.2.28"),   # Funcao Encargos Especiais
        "ajuste_ordem_bancaria":             (8719, "13.1.1.3"),      # Ajuste de Ordem Bancaria
    },
    "natureza": {
        "total":                                                       (8720, "13.2.1"),        # Investimento Total
        "gnd4":                                                        (8721, "13.2.1.1"),      # Investimentos (GND 4)
        "gnd4__aplicacoes_diretas":                                    (8722, "13.2.1.1.1"),    # Aplicacoes Diretas da Uniao
        "gnd4__aplicacoes_diretas__obras_instalacoes":                 (8723, "13.2.1.1.1.1"),  # Aplicacoes Diretas - Obras e instalacoes
        "gnd4__aplicacoes_diretas__equipamentos_material_permanente":  (8724, "13.2.1.1.1.2"),  # Aplicacoes Diretas - Equipamentos e material permanente
        "gnd4__aplicacoes_diretas__servicos":                          (8726, "13.2.1.1.1.3"),  # Aplicacoes Diretas - Servicos
        "gnd4__aplicacoes_diretas__demais":                            (8727, "13.2.1.1.1.4"),  # Aplicacoes Diretas - Demais aplicacoes diretas da Uniao
        "gnd4__transf_estados_df":                                     (8728, "13.2.1.1.2"),    # Transferencias a Estados/DF
        "gnd4__transf_municipios":                                     (8729, "13.2.1.1.3"),    # Transferencias a Municipios
        "gnd4__outras_transferencias":                                 (8730, "13.2.1.1.4"),    # Outras Transferencias
        "gnd5":                                                        (8731, "13.2.1.2"),      # Inversoes Financeiras (GND 5)
        "gnd5__participacao_uniao_capital":                            (8732, "13.2.1.2.1"),    # Participacao da Uniao no Capital
        "gnd5__integralizacao_cotas":                                  (8752, "13.2.1.2.2"),    # Integralizacao de Cotas
        "gnd5__integralizacao_cotas__fundos_garantidores":             (8753, "13.2.1.2.2.1"),  # Fundos garantidores
        "gnd5__integralizacao_cotas__organismos_internacionais":       (8754, "13.2.1.2.2.2"),  # Organismos internacionais
        "gnd5__integralizacao_cotas__outras":                          (8755, "13.2.1.2.2.3"),  # Integralizacao de Cotas - Outras
        "gnd5__demais":                                                (8756, "13.2.1.2.3"),    # Inversoes Financeiras - Demais
        "ajuste_ordem_bancaria":                                       (8757, "13.2.1.3"),      # Ajuste de Ordem Bancaria
    },
}

# Pai -> filhos, por corte. Usado por _validate() para as identidades de soma.
# So os pais que TEM filhos aparecem aqui.
_TREE: dict[str, dict[str, list[str]]] = {
    corte: {
        parent: sorted(
            item for item in items
            if item.startswith(parent + "__") and item.count("__") == parent.count("__") + 1
        )
        for parent in items
        if any(i.startswith(parent + "__") for i in items)
    }
    for corte, items in _ITEMS.items()
}

# Nos presentes nos dois cortes -- tem que ser identicos entre eles.
_SHARED = ("total", "gnd4", "gnd5", "ajuste_ordem_bancaria")

_TOL = 0.01  # R$ mi

_st = SeriesTemporais()


def _verify_contract() -> None:
    """Confere a arvore viva dos dois subtemas contra `_ITEMS`.

    Levanta se um no foi inserido, removido ou renumerado no Tesouro -- antes de
    baixar qualquer dado, para nao gravar meia carga. Confere planoContas <-> id
    nos dois sentidos: um planoContas que trocou de id (serie reconstruida) e um
    id reatribuido a outra posicao da arvore quebram os dois igualmente, e o
    segundo caso e o que passaria silenciosamente num contrato so de id -> nome.
    """
    for corte, subtema_id in _SUBTEMAS.items():
        live = {
            n["planoContas"]: n["id"]
            for n in _st.flatten_arvore(_st.get_arvore(subtema_id))
        }
        expected = {pc: sid for sid, pc in _ITEMS[corte].values()}
        if live != expected:
            faltando = sorted(set(expected) - set(live))
            novos = sorted(set(live) - set(expected))
            trocados = sorted(
                f"{pc}: contrato={expected[pc]} vivo={live[pc]}"
                for pc in set(expected) & set(live)
                if expected[pc] != live[pc]
            )
            raise ValueError(
                f"Arvore do subtema {corte} (id {subtema_id}) divergiu de _ITEMS. "
                f"Sumiram: {faltando}. Novos: {novos}. Id trocado: {trocados}. "
                f"Atualize _ITEMS em {__name__} antes de recarregar."
            )


def _validate(df: pd.DataFrame) -> None:
    """Confere as identidades de soma e a grade de datas. Levanta em qualquer desvio.

    Ver "Identidades" na docstring do modulo. Sem janela de excecao: as 6 familias
    de identidade fecham com desvio exato 0.0 no historico de 2008-01 em diante
    (confirmado ao vivo, 2026-08), entao qualquer desvio acima de R$ 0,01 mi e
    sinal de contrato rompido, nao de revisao da fonte.
    """
    wide = {
        corte: df[df["corte"] == corte].pivot(index="date", columns="item", values="value")
        for corte in _ITEMS
    }

    for corte, w in wide.items():
        faltando = set(_ITEMS[corte]) - set(w.columns)
        if faltando:
            raise ValueError(f"corte={corte}: series ausentes na carga: {sorted(faltando)}")

        idx = pd.DatetimeIndex(w.index)
        esperado = pd.date_range(idx.min(), idx.max(), freq="MS")
        if not idx.equals(esperado):
            raise ValueError(
                f"corte={corte}: grade de datas nao e mensal contigua "
                f"({len(idx)} meses observados vs. {len(esperado)} esperados entre "
                f"{idx.min().date()} e {idx.max().date()})"
            )

        resid = (w["total"] - w[["gnd4", "gnd5", "ajuste_ordem_bancaria"]].sum(axis=1)).abs()
        if resid.max() > _TOL:
            pior = resid.idxmax()
            raise ValueError(
                f"corte={corte}: total != gnd4+gnd5+ajuste_ordem_bancaria. "
                f"Pior mes {pior.date()}: desvio {resid.max():.4f} R$ mi"
            )

        for parent, kids in _TREE[corte].items():
            resid = (w[parent] - w[kids].sum(axis=1)).abs()
            if resid.max() > _TOL:
                pior = resid.idxmax()
                raise ValueError(
                    f"corte={corte}: {parent} != soma dos {len(kids)} filhos. "
                    f"Pior mes {pior.date()}: desvio {resid.max():.4f} R$ mi"
                )

    for item in _SHARED:
        resid = (wide["funcao"][item] - wide["natureza"][item]).abs()
        if resid.max() > _TOL:
            pior = resid.idxmax()
            raise ValueError(
                f"no compartilhado '{item}' divergiu entre os cortes. "
                f"Pior mes {pior.date()}: desvio {resid.max():.4f} R$ mi"
            )


def run(start: str | None = None) -> None:
    """Atualiza macro_brasil.fisc_investimento.

    Confere o contrato da arvore, baixa as 78 series, corta o periodo sem dado
    (ver `_START`), valida as identidades e faz upsert. Levanta antes de gravar
    qualquer linha se o contrato ou uma identidade romper.

    Args:
        start: primeiro mes a gravar, ISO ("2008-01-01"). Default `_START`.
               Nao economiza download -- a API de Series Temporais so distribui
               cada serie como historico completo, sem parametro de range; o
               corte e aplicado depois, na memoria. Passar um `start` anterior a
               `_START` faz `_validate()` levantar (a decomposicao nao existe
               antes disso), o que e deliberado.
    """
    _verify_contract()

    frames = []
    for corte, items in _ITEMS.items():
        df = _st.get_series_bulk({slug: sid for slug, (sid, _) in items.items()})
        df = df.rename(columns={"name": "item"})
        df["corte"] = corte
        frames.append(df)

    df = pd.concat(frames, ignore_index=True)
    df = df[df["date"] >= pd.Timestamp(start or _START)].reset_index(drop=True)

    _validate(df)

    insert_data_into_database(_DATABASE, _TABLE, df[["date", "corte", "item", "value"]])
