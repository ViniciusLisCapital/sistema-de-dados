"""
Impulso fiscal via resultado primario ACIMA DA LINHA (RTN, Governo Central) -- 4a secao
da aba Impulso Fiscal, adicionada em 2026-08-28 a pedido do usuario ("o impulso do
resultado primario poderia ser feito com os dados do RTN, ao inves de usar os dados que
o BCB divulga, pois os dados do tesouro parecem que saem primeiro").

SOMA, nao substitui, a secao "Impulso via Resultado Primario por Esfera"
(_load_fiscal_impulse_nfsp(), fisc_nfsp) -- decisao explicita do usuario na mesma rodada.
O que cada uma entrega, e por que as duas ficam:

  fisc_nfsp (abaixo da linha)   setor publico CONSOLIDADO, com quebra por esfera
                                (Gov. Federal, BC, Estados, Municipios, Estatais).
                                Escopo que o RTN nao cobre.
  fisc_rtn  (acima da linha)    so Governo Central, mas decomposto em RECEITA x DESPESA
                                e, dentro de cada uma, por rubrica orcamentaria.
                                Leitura que o abaixo da linha nao pode dar.

O ganho de PRAZO que motivou o pedido existe mas e pequeno, e foi medido (2026-08-28,
contra as duas agendas de domain/release_calendar/calendar_2026.yaml): o RTN sai 1 a 3
dias antes da Nota para a Imprensa do BCB (media 1,8 dia -- 28/08 vs 31/08 para julho,
29/09 vs 30/09 para agosto, 29/10 vs 30/10, 27/11 vs 30/11, 29/12 vs 30/12). Nesses 1-3
dias o RTN esta um mes de referencia a frente, que e a janela em que o usuario reparou.
E trocar de fonte nao traria dado novo: `fisc_rtn.resultado_primario_abaixo_linha` e
IDENTICA ao fisc_nfsp (Gov. Federal + Banco Central) em 330 meses, diferenca maxima 0,00
-- o Tesouro republica o numero do BCB dentro do proprio RTN, um mes atras. O que
justifica esta secao e a decomposicao, nao o calendario.

Convencao de sinal (a mesma das outras tres metricas da aba): POSITIVO = EXPANSIONISTA.

    impulso = -Delta12( resultado_primario / PIB ) ,  resultado = receita_liq - despesa

Derivando os dois ramos dessa identidade:

    d impulso / d receita_liquida  =  -Delta12(.)     receita caindo = expansionista
    d impulso / d despesa_total    =  +Delta12(.)     despesa subindo = expansionista

Por isso cada no carrega um `sign`, e nao ha um sinal unico para a arvore inteira. O caso
que nao se adivinha e `transferencias_reparticao_receita`: ela esta DENTRO de Receita
Liquida mas entra SUBTRAINDO (receita_liquida = receita_total - transferencias, conferido
ao vivo em 355 meses, |max| 0,00), entao o sinal dela inverte de novo e volta a +1.

Aditividade, medida em 2026-08-28 contra o banco (a mesma disciplina do resto do
relatorio -- o que fecha e o que nao fecha, com numero):

  - NIVEL 1 fecha SEMPRE e EXATO: receita_liquida - despesa_total -
    resultado_primario_governo_central = 0,00 em todos os 355 meses. Entao as duas barras
    de topo somam a linha do total em qualquer ponto da amostra.
  - Niveis mais fundos fecham EXATO a partir de 2016-01. Antes disso o proprio RTN nao
    publica a decomposicao completa: `receita_administrada_rfb` so fecha nos 9 tributos a
    partir de 2016-01, `despesas_executivo_prog_financeira` a partir de 2008-01 e
    `beneficios_previdenciarios` a partir de 2001-01. Nao e defeito nosso nem do parser --
    e a cobertura da fonte, e por isso a secao imprime a janela em que a decomposicao
    fecha em vez de fingir que fecha desde 1997.

Como a transformacao inteira (soma movel 12m -> razao com o PIB -> diferenca de 12 meses
-> multiplicacao por sign) e LINEAR, a nao-aditividade em nivel se propaga sem amplificar:
onde os niveis somam o pai em R$, as contribuicoes somam a contribuicao do pai em p.p.
"""
from analytics.brasil.fiscal_policy.rtn_tab import RTN_TREE

# Contribuicao ao impulso = sign * Delta12(serie / PIB12). Ver o docstring acima para a
# derivacao; `_SIGN_RAIZ` e o unico lugar em que o sinal e escolhido, os filhos herdam.
_SIGN_RAIZ = {"receita_liquida": -1, "despesa_total": +1}

# Excecao unica: dentro de Receita Liquida, transferencias entra subtraindo (receita_liquida
# = receita_total - transferencias), entao o sinal herdado inverte.
_SIGN_EXCECOES = {"transferencias_reparticao_receita": +1}

# O no que vira a LINHA de total do grafico, nao uma barra -- sai da arvore de barras.
TOTAL_CODE = "resultado_primario_governo_central"

# Primeiro mes em que TODOS os pais da arvore fecham nos filhos (medido, ver docstring).
ADITIVIDADE_DESDE = "2016-01-01"


def _com_sinal(nodes: list, sign: int) -> list:
    """Copia a arvore do RTN anexando `sign` a cada no, respeitando as excecoes."""
    out = []
    for n in nodes:
        s = _SIGN_EXCECOES.get(n["seriesKey"], sign)
        novo = {"key": n["key"], "label": n["label"], "seriesKey": n["seriesKey"], "sign": s}
        if n.get("children"):
            novo["children"] = _com_sinal(n["children"], s)
        out.append(novo)
    return out


def tree() -> list:
    """Arvore de contribuicoes: os 2 ramos do RTN com sinal, sem o no de resultado
    primario (que e a linha de total, nao uma barra)."""
    return [_com_sinal([n], _SIGN_RAIZ[n["seriesKey"]])[0]
            for n in RTN_TREE if n["seriesKey"] in _SIGN_RAIZ]


def codes() -> list[str]:
    """Todos os codigos de fisc_rtn que esta secao le, incluindo o do total."""
    vistos: list[str] = []

    def walk(nodes):
        for n in nodes:
            if n["seriesKey"] not in vistos:
                vistos.append(n["seriesKey"])
            if n.get("children"):
                walk(n["children"])

    walk(tree())
    vistos.append(TOTAL_CODE)
    return vistos


def flat_nodes() -> list[dict]:
    """A arvore achatada, para quem precisa iterar no (key, seriesKey, sign)."""
    out: list[dict] = []

    def walk(nodes):
        for n in nodes:
            out.append(n)
            if n.get("children"):
                walk(n["children"])

    walk(tree())
    return out
