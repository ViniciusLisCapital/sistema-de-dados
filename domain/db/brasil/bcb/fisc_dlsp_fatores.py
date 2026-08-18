"""
Fatores condicionantes da DLSP (Divida Liquida do Setor Publico) -- detalhamento
por item, mensal, R$ milhoes correntes.

Fonte: planilha `Facdetp.xlsx` das "Tabelas especiais" de estatisticas fiscais do
BCB (ver connectors/bcb_tabelas_especiais.py). NAO existe no SGS -- o SGS publica
os agregados de divida (`fisc_divida`: DBGG/DLSP em %PIB) e de resultado
(`fisc_nfsp`: primario/nominal/juros em %PIB), mas nao a DECOMPOSICAO da variacao
do estoque nos fatores que a condicionam, nem por item de balanco.

## O que a tabela responde

`fisc_divida` diz que a DLSP subiu X pontos de PIB. Esta tabela diz POR QUE:
quanto veio do resultado primario, quanto de juros nominais, quanto de ajustes
metodologicos (reavaliacao cambial da divida interna/externa), quanto de paridade
de moedas, quanto de reconhecimento de "esqueletos", quanto de privatizacoes.
E a identidade contabil que fecha exatamente (ver "Identidade" abaixo).

## Estrutura da planilha

9 abas, TODAS com layout identico -- mesma taxonomia de 95 linhas e mesma grade
de datas (confirmado ao vivo, 2026-08: zero divergencia de rotulo entre abas):
    Estoques   -> fator "estoque"                   (SALDO em fim de mes)
    Primario   -> fator "primario"                  (FLUXO do mes)
    Juros      -> fator "juros"                     (FLUXO do mes)
    Met Int    -> fator "ajuste_met_interno"        (FLUXO do mes)
    Met Ext    -> fator "ajuste_met_externo"        (FLUXO do mes)
    Paridade   -> fator "ajuste_paridade"           (FLUXO do mes)
    Cx Comp    -> fator "ajuste_caixa_competencia"  (FLUXO do mes)
    Rec Div    -> fator "reconhecimento_dividas"    (FLUXO do mes)
    Privat     -> fator "privatizacoes"             (FLUXO do mes)

Layout de cada aba: linha 5 (1-based) = ano, esparso (so na coluna de Janeiro e,
no comeco da serie, tambem de Julho); linha 7 = nome do mes em portugues; linhas
10-114 = itens, hierarquia dada pelo numero de espacos a esquerda do rotulo;
colunas 3+ = um mes cada, de 2001-12 em diante.

As 95 linhas formam TRES arvores independentes, nao uma so (ver `_ITEMS`):
    total    -- "Divida liquida total", aberta por devedor (Gov. Federal, Bacen,
                estados, municipios, estatais)
    interna  -- "Divida interna liquida", aberta por devedor E por item de
                balanco dentro de cada devedor (divida mobiliaria, conta unica,
                compromissadas, FAT, base monetaria, renegociacoes etc.)
    externa  -- "Divida externa liquida", aberta por devedor
`total` = `interna` + `externa` em todo mes (confirmado ao vivo, desvio maximo
1,9e-09). `total` tambem = soma dos 5 devedores, exato em todas as 9 abas.

## SINAL: convencao "necessidade de financiamento", OPOSTA a de fisc_nfsp

**Fluxo positivo = AUMENTA a divida liquida.** Logo `primario` positivo aqui e
DEFICIT primario, nao superavit -- exatamente o inverso do que
`macro_brasil.fisc_nfsp` armazena (aquele script inverte o sinal na gravacao,
ver `_FLIP_SIGN` em fisc_nfsp.py, para guardar a convencao de mercado
"positivo = superavit").

Este script **NAO inverte o sinal**, deliberadamente: inverter quebraria a
identidade aditiva com `estoque`, que e a razao de existir desta tabela. Quem
cruzar `fisc_dlsp_fatores.primario` com `fisc_nfsp.resultado_primario_*` tem que
esperar sinais opostos -- confirmado ao vivo, sao negativos exatos um do outro
(ver "Validacao" abaixo). Ver o gotcha equivalente em analytics/fiscal_policy/
CLAUDE.md antes de charetar qualquer coisa desta tabela junto de fisc_nfsp.

## Identidade

Para todo item e todo mes t:

    estoque[t] - estoque[t-1] == primario[t] + juros[t] + ajuste_met_interno[t]
                                + ajuste_met_externo[t] + ajuste_paridade[t]
                                + ajuste_caixa_competencia[t]
                                + reconhecimento_dividas[t] + privatizacoes[t]

Verificada ao vivo em todas as 27.930 celulas (95 itens x 294 transicoes
mensais): fecha em 27.904 delas com desvio < R$ 0,01 mi. As 26 excecoes estao
TODAS em 2003-10/11 e 2004-02/03, em pares que se cancelam entre meses
consecutivos (ex: "Recursos do FAT" erra +622,77 em 2003-10 e -622,77 em
2003-11) -- e uma quebra da revisao historica do proprio BCB, nao de parsing.
`_validate()` tolera essa janela e levanta em qualquer desvio fora dela: um erro
de parsing de verdade (coluna deslocada, linha trocada) produziria desvio grande
e generalizado, nao 26 celulas pareadas em 4 meses de 2003-2004.

## Banco

macro_brasil.fisc_dlsp_fatores -- PRIMARY KEY (date, fator, item).
95 itens x 9 fatores x ~295 meses ~= 252 mil linhas.

Zeros sao gravados como zero, nao omitidos: 4 dos 8 fatores de fluxo (met
interno/externo, paridade, caixa-competencia) so tocam ~25 dos 95 itens e ficam
exatamente 0 no resto. Guardar o zero explicito evita a convencao implicita
"linha ausente = 0", que e o tipo de premissa que quebra silenciosamente numa
consulta futura.

`run()` faz upsert, NAO truncate -- diferente de fisc_rtn.py/fisc_efgg.py, que
truncam porque nao validam a taxonomia da fonte. Aqui `_ITEMS` e um contrato
explicito conferido rotulo por rotulo a cada execucao: se o BCB inserir, remover
ou renomear uma linha, `_parse_sheet()` levanta antes de gravar qualquer coisa,
entao nao ha o risco de linha orfa que justifica o truncate lah. Revisao de valor
em data ja existente entra normalmente pelo ON DUPLICATE KEY UPDATE.
"""

from __future__ import annotations

import re
import unicodedata

import pandas as pd

from connectors.bcb_tabelas_especiais import TabelasEspeciais
from connectors.mysql import insert_data_into_database

_DATABASE = "macro_brasil"
_TABLE = "fisc_dlsp_fatores"
_FILENAME = "Facdetp.xlsx"

# Aba da planilha -> slug do fator. A ordem importa: "estoque" e o saldo, os 8
# seguintes sao os fluxos que somam a variacao dele (ver docstring, "Identidade").
_FATORES = {
    "Estoques": "estoque",
    "Primário": "primario",
    "Juros": "juros",
    "Met Int": "ajuste_met_interno",
    "Met Ext": "ajuste_met_externo",
    "Paridade": "ajuste_paridade",
    "Cx Comp": "ajuste_caixa_competencia",
    "Rec Div": "reconhecimento_dividas",
    "Privat": "privatizacoes",
}
_ESTOQUE = "estoque"
_FLUXOS = [f for f in _FATORES.values() if f != _ESTOQUE]

# Linhas (1-based, como no Excel) do cabecalho de datas.
_ROW_YEAR = 5
_ROW_MONTH = 7

_MESES = {
    "janeiro": 1, "fevereiro": 2, "marco": 3, "abril": 4, "maio": 5, "junho": 6,
    "julho": 7, "agosto": 8, "setembro": 9, "outubro": 10, "novembro": 11, "dezembro": 12,
}

# Janela em que a propria revisao historica do BCB nao fecha a identidade
# (ver docstring, "Identidade") -- desvios aqui sao tolerados, fora dela nao.
_IDENTITY_EXCEPTION_MONTHS = {"2003-10", "2003-11", "2004-02", "2004-03"}
_IDENTITY_TOL = 0.01          # R$ mil (0,01 milhao) -- ruido de float
_IDENTITY_TOL_EXCEPTION = 700.0

# Taxonomia dos 95 itens: (linha_excel, nivel, slug, slug_do_pai, rotulo_do_bcb).
# Contrato explicito conferido a cada execucao (ver `_parse_sheet`) -- nao e
# inferido do arquivo em runtime, justamente para que uma mudanca de layout do
# BCB levante em vez de gravar dado remapeado errado em silencio.
_ITEMS = [
    ( 10, 0, 'total', None, 'Dívida líquida total'),
    ( 12, 1, 'total__gov_federal', 'total', 'Governo Federal'),
    ( 13, 1, 'total__bacen', 'total', 'Banco Central do Brasil'),
    ( 14, 1, 'total__gov_est', 'total', 'Governos estaduais'),
    ( 15, 1, 'total__gov_mun', 'total', 'Governos municipais'),
    ( 16, 1, 'total__estatais', 'total', 'Empresas estatais'),
    ( 17, 2, 'total__estatais__federais', 'total__estatais', 'Federais'),
    ( 18, 2, 'total__estatais__estaduais', 'total__estatais', 'Estaduais'),
    ( 19, 2, 'total__estatais__municipais', 'total__estatais', 'Municipais'),
    ( 21, 0, 'interna', None, 'Dívida interna líquida'),
    ( 23, 1, 'interna__gov_federal', 'interna', 'Governo federal'),
    ( 24, 2, 'interna__gov_federal__mobiliaria_mercado', 'interna__gov_federal', 'Dívida mobiliária em mercado'),
    ( 25, 3, 'interna__gov_federal__mobiliaria_mercado__mobiliaria_tesouro', 'interna__gov_federal__mobiliaria_mercado', 'Dívida mobiliária do Tesouro Nacional'),
    ( 26, 3, 'interna__gov_federal__mobiliaria_mercado__titulos_custodia_fge', 'interna__gov_federal__mobiliaria_mercado', 'Títulos sob custódia do FGE'),
    ( 27, 2, 'interna__gov_federal__securitizadas_tda', 'interna__gov_federal', 'Dívidas securitizadas e TDA'),
    ( 28, 2, 'interna__gov_federal__bancaria', 'interna__gov_federal', 'Dívida bancária federal'),
    ( 29, 2, 'interna__gov_federal__arrec_recolher', 'interna__gov_federal', 'Arrecadação a recolher'),
    ( 30, 2, 'interna__gov_federal__dep_vista', 'interna__gov_federal', 'Depósitos a vista'),
    ( 31, 2, 'interna__gov_federal__fat', 'interna__gov_federal', 'Recursos do FAT'),
    ( 32, 2, 'interna__gov_federal__previdencia', 'interna__gov_federal', 'Previdência social'),
    ( 33, 2, 'interna__gov_federal__reneg_9496_2185', 'interna__gov_federal', 'Renegociação (Lei nº 9.496 e MP nº 2.185)'),
    ( 34, 2, 'interna__gov_federal__reneg_8727', 'interna__gov_federal', 'Renegociação (Lei nº 8.727)'),
    ( 35, 2, 'interna__gov_federal__reestruturadas', 'interna__gov_federal', 'Dívidas reestruturadas'),
    ( 36, 2, 'interna__gov_federal__creditos_inst_fin_oficiais', 'interna__gov_federal', 'Créditos concedidos a Inst. Financ. Oficiais'),
    ( 37, 3, 'interna__gov_federal__creditos_inst_fin_oficiais__instrumentos_hibridos', 'interna__gov_federal__creditos_inst_fin_oficiais', 'Instrumentos híbridos de capital e dívida'),
    ( 38, 3, 'interna__gov_federal__creditos_inst_fin_oficiais__creditos_bndes', 'interna__gov_federal__creditos_inst_fin_oficiais', 'Créditos junto ao BNDES'),
    ( 39, 2, 'interna__gov_federal__aplic_fundos_programas', 'interna__gov_federal', 'Aplicações em fundos e programas'),
    ( 40, 2, 'interna__gov_federal__outros_creditos', 'interna__gov_federal', 'Outros créditos do Governo Federal'),
    ( 41, 2, 'interna__gov_federal__relac_bacen', 'interna__gov_federal', 'Relacionamento com Banco Central'),
    ( 42, 3, 'interna__gov_federal__relac_bacen__conta_unica', 'interna__gov_federal__relac_bacen', 'Conta única'),
    ( 43, 3, 'interna__gov_federal__relac_bacen__mobiliaria_carteira_bacen', 'interna__gov_federal__relac_bacen', 'Dívida Mobiliária na carteira do Bacen'),
    ( 44, 3, 'interna__gov_federal__relac_bacen__equaliz_cambial', 'interna__gov_federal__relac_bacen', 'Equalização Cambial'),
    ( 46, 1, 'interna__bacen', 'interna', 'Banco Central do Brasil'),
    ( 47, 2, 'interna__bacen__base_monetaria', 'interna__bacen', 'Base monetária'),
    ( 48, 2, 'interna__bacen__mobiliaria_bacen', 'interna__bacen', 'Dívida mobiliária do Bacen'),
    ( 49, 2, 'interna__bacen__compromissadas', 'interna__bacen', 'Operações compromissadas'),
    ( 50, 2, 'interna__bacen__dep_bacen', 'interna__bacen', 'Depósitos no Bacen'),
    ( 51, 3, 'interna__bacen__dep_bacen__dep_voluntarios', 'interna__bacen__dep_bacen', 'Depósitos voluntários remunerados'),
    ( 52, 3, 'interna__bacen__dep_bacen__demais_depositos', 'interna__bacen__dep_bacen', 'Demais depósitos'),
    ( 53, 2, 'interna__bacen__creditos_inst_fin', 'interna__bacen', 'Créditos do Bacen às inst. financeiras'),
    ( 54, 2, 'interna__bacen__demais_contas', 'interna__bacen', 'Demais contas do Bacen'),
    ( 55, 2, 'interna__bacen__relac_gov_federal', 'interna__bacen', 'Relacionamento com Governo Federal'),
    ( 56, 3, 'interna__bacen__relac_gov_federal__conta_unica', 'interna__bacen__relac_gov_federal', 'Conta única'),
    ( 57, 3, 'interna__bacen__relac_gov_federal__mobiliaria_carteira_bacen', 'interna__bacen__relac_gov_federal', 'Dívida Mobiliária na carteira do Bacen'),
    ( 58, 3, 'interna__bacen__relac_gov_federal__equaliz_cambial', 'interna__bacen__relac_gov_federal', 'Equalização Cambial'),
    ( 60, 1, 'interna__gov_est', 'interna', 'Governos estaduais'),
    ( 61, 2, 'interna__gov_est__mobiliaria_liquida', 'interna__gov_est', 'Dívida mobiliária líquida'),
    ( 62, 2, 'interna__gov_est__reneg_9496', 'interna__gov_est', 'Renegociação (Lei nº 9.496)'),
    ( 63, 2, 'interna__gov_est__reneg_8727', 'interna__gov_est', 'Renegociação (Lei nº 8.727)'),
    ( 64, 2, 'interna__gov_est__reestruturadas', 'interna__gov_est', 'Dívidas reestruturadas'),
    ( 65, 2, 'interna__gov_est__bancaria', 'interna__gov_est', 'Dívida bancária estadual'),
    ( 66, 2, 'interna__gov_est__outros_debitos', 'interna__gov_est', 'Outros débitos'),
    ( 67, 2, 'interna__gov_est__arrec_recolher', 'interna__gov_est', 'Arrecadação a recolher'),
    ( 68, 2, 'interna__gov_est__dep_vista', 'interna__gov_est', 'Depósitos à vista'),
    ( 69, 2, 'interna__gov_est__outros_creditos', 'interna__gov_est', 'Outros créditos'),
    ( 71, 1, 'interna__gov_mun', 'interna', 'Governos municipais'),
    ( 72, 2, 'interna__gov_mun__mobiliaria_liquida', 'interna__gov_mun', 'Dívida mobiliária líquida'),
    ( 73, 2, 'interna__gov_mun__reneg_2185', 'interna__gov_mun', 'Renegociação (MP nº 2.185)'),
    ( 74, 2, 'interna__gov_mun__reneg_8727', 'interna__gov_mun', 'Renegociação (Lei nº 8.727)'),
    ( 75, 2, 'interna__gov_mun__reestruturadas', 'interna__gov_mun', 'Dívidas reestruturadas'),
    ( 76, 2, 'interna__gov_mun__bancaria', 'interna__gov_mun', 'Dívida bancária municipal'),
    ( 77, 2, 'interna__gov_mun__arrec_recolher', 'interna__gov_mun', 'Arrecadação a recolher'),
    ( 78, 2, 'interna__gov_mun__dep_vista_aplic', 'interna__gov_mun', 'Depósitos à vista e aplicações'),
    ( 80, 1, 'interna__estatais', 'interna', 'Empresas estatais'),
    ( 81, 2, 'interna__estatais__federais', 'interna__estatais', 'Federais'),
    ( 82, 3, 'interna__estatais__federais__reestruturadas', 'interna__estatais__federais', 'Dívidas reestruturadas'),
    ( 83, 3, 'interna__estatais__federais__bancaria', 'interna__estatais__federais', 'Dívida bancária'),
    ( 84, 3, 'interna__estatais__federais__outros_debitos', 'interna__estatais__federais', 'Outros débitos'),
    ( 85, 3, 'interna__estatais__federais__reneg_8727', 'interna__estatais__federais', 'Renegociação (Lei nº 8.727)'),
    ( 86, 3, 'interna__estatais__federais__carteira_titulos_publicos', 'interna__estatais__federais', 'Carteira de tít.  púb.  das  emp.  estatais'),
    ( 87, 3, 'interna__estatais__federais__dep_vista', 'interna__estatais__federais', 'Depósitos à vista'),
    ( 88, 3, 'interna__estatais__federais__outros_creditos', 'interna__estatais__federais', 'Outros créditos'),
    ( 90, 2, 'interna__estatais__estaduais', 'interna__estatais', 'Estaduais'),
    ( 91, 3, 'interna__estatais__estaduais__reestruturadas', 'interna__estatais__estaduais', 'Dívidas reestruturadas'),
    ( 92, 3, 'interna__estatais__estaduais__bancaria', 'interna__estatais__estaduais', 'Dívida bancária'),
    ( 93, 3, 'interna__estatais__estaduais__debentures', 'interna__estatais__estaduais', 'Debêntures'),
    ( 94, 3, 'interna__estatais__estaduais__reneg_8727', 'interna__estatais__estaduais', 'Renegociação (Lei nº 8.727)'),
    ( 95, 3, 'interna__estatais__estaduais__carteira_titulos_publicos', 'interna__estatais__estaduais', 'Carteira de tít.  púb.  das  emp.  estatais'),
    ( 96, 3, 'interna__estatais__estaduais__dep_vista_aplic', 'interna__estatais__estaduais', 'Depósitos à vista e aplicações'),
    ( 98, 2, 'interna__estatais__municipais', 'interna__estatais', 'Municipais'),
    ( 99, 3, 'interna__estatais__municipais__reestruturadas', 'interna__estatais__municipais', 'Dívidas reestruturadas'),
    (100, 3, 'interna__estatais__municipais__bancaria', 'interna__estatais__municipais', 'Dívida bancária'),
    (101, 3, 'interna__estatais__municipais__reneg_8727', 'interna__estatais__municipais', 'Renegociação (Lei nº 8.727)'),
    (102, 3, 'interna__estatais__municipais__dep_vista', 'interna__estatais__municipais', 'Depósitos à vista'),
    (104, 0, 'externa', None, 'Dívida externa líquida'),
    (105, 1, 'externa__gov_federal', 'externa', 'Governo Federal'),
    (106, 2, 'externa__gov_federal__titulos_mercado_domestico', 'externa__gov_federal', 'Títulos de dív. negociados no mercado doméstico'),
    (107, 2, 'externa__gov_federal__demais', 'externa__gov_federal', 'Demais'),
    (108, 1, 'externa__bacen', 'externa', 'Banco Central do Brasil'),
    (109, 1, 'externa__gov_est', 'externa', 'Governos estaduais'),
    (110, 1, 'externa__gov_mun', 'externa', 'Governos municipais'),
    (111, 1, 'externa__estatais', 'externa', 'Empresas estatais'),
    (112, 2, 'externa__estatais__federais', 'externa__estatais', 'Federais'),
    (113, 2, 'externa__estatais__estaduais', 'externa__estatais', 'Estaduais'),
    (114, 2, 'externa__estatais__municipais', 'externa__estatais', 'Municipais'),
]

# Arvore publica, para analytics/ montar tabela hierarquica sem reparsear o Excel:
# {slug: {"nivel": int, "parent": str | None, "label": str, "arvore": str}}.
ITEM_TREE = {
    slug: {"nivel": nivel, "parent": parent, "label": label, "arvore": slug.split("__")[0]}
    for _row, nivel, slug, parent, label in _ITEMS
}

FATORES = list(_FATORES.values())


def _norm(s) -> str:
    """Normaliza um rotulo para comparacao: sem acento, sem marcador de nota de
    rodape ("3/"), espacos colapsados, minusculo.

    A planilha usa espacos duplos dentro de alguns rotulos ("Carteira de tit.
    pub.  das  emp.  estatais") e marcadores de nota de rodape que o BCB
    renumera de tempo em tempo -- comparar cru quebraria por motivo cosmetico.
    """
    if s is None:
        return ""
    s = re.sub(r"\d+/\s*$", "", str(s).strip())
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return re.sub(r"\s+", " ", s).strip().lower()


def _parse_dates(raw: pd.DataFrame) -> pd.Series:
    """Monta a grade de datas a partir das linhas de ano (5) e mes (7).

    O ano so aparece na coluna de Janeiro (e tambem de Julho no comeco da
    serie), entao e propagado para a frente. Valida que a sequencia resultante
    e mensal, estritamente crescente e sem buraco -- um deslocamento de coluna
    apareceria aqui, antes de qualquer valor ser lido.

    Returns:
        Series indexada pela posicao da coluna no DataFrame cru -> Timestamp.
    """
    years = raw.iloc[_ROW_YEAR - 1]
    months = raw.iloc[_ROW_MONTH - 1]

    dates = {}
    current_year = None
    for col in raw.columns:
        y = years.get(col)
        if isinstance(y, (int, float)) and not pd.isna(y) and 1900 < int(y) < 2200:
            current_year = int(y)
        month = _MESES.get(_norm(months.get(col)))
        if month is None or current_year is None:
            continue
        dates[col] = pd.Timestamp(current_year, month, 1)

    out = pd.Series(dates).sort_index()
    if out.empty:
        raise RuntimeError(f"{_FILENAME}: nenhuma coluna de data reconhecida (linhas {_ROW_YEAR}/{_ROW_MONTH}).")

    expected = pd.date_range(out.iloc[0], periods=len(out), freq="MS")
    if not (out.values == expected.values).all():
        first_bad = int((out.values != expected.values).argmax())
        raise RuntimeError(
            f"{_FILENAME}: grade de datas nao e mensal contigua -- coluna {out.index[first_bad]} "
            f"lida como {out.iloc[first_bad].date()}, esperado {expected[first_bad].date()}."
        )
    return out


def _parse_sheet(raw: pd.DataFrame, fator: str, dates: pd.Series) -> pd.DataFrame:
    """Converte uma aba crua em formato longo (date, fator, item, value).

    Confere rotulo por rotulo contra `_ITEMS` antes de ler valor nenhum: se o
    BCB inserir/remover/renomear uma linha, levanta aqui em vez de gravar a
    serie errada sob o slug antigo.
    """
    for excel_row, _nivel, slug, _parent, label in _ITEMS:
        got = raw.iat[excel_row - 1, 0]
        if _norm(got) != _norm(label):
            raise RuntimeError(
                f"{_FILENAME}, aba do fator '{fator}': linha {excel_row} deveria ser "
                f"'{label}' (item '{slug}'), veio '{got}'. O layout da planilha mudou -- "
                f"conferir _ITEMS antes de rodar de novo."
            )

    rows = [r - 1 for r, _n, _s, _p, _l in _ITEMS]
    slugs = [s for _r, _n, s, _p, _l in _ITEMS]

    block = raw.iloc[rows][list(dates.index)].apply(pd.to_numeric, errors="coerce")
    block.index = slugs
    block.columns = dates.values

    long_df = (
        block.stack(future_stack=True)
        .rename("value")
        .reset_index()
        .rename(columns={"level_0": "item", "level_1": "date"})
        .dropna(subset=["value"])
    )
    long_df["fator"] = fator
    return long_df[["date", "fator", "item", "value"]]


def _validate(df: pd.DataFrame) -> None:
    """Confere a identidade estoque/fluxos (ver docstring do modulo).

    Levanta se algum desvio aparecer fora da janela conhecida de revisao
    historica do BCB (2003-10/11, 2004-02/03).
    """
    wide = df.pivot_table(index=["item", "date"], columns="fator", values="value", aggfunc="first")
    faltando = [f for f in _FATORES.values() if f not in wide.columns]
    if faltando:
        raise RuntimeError(f"{_FILENAME}: fatores ausentes apos o parsing: {faltando}.")

    delta = wide[_ESTOQUE].groupby(level="item").diff()
    soma = wide[_FLUXOS].sum(axis=1)
    dev = (delta - soma).abs().dropna()

    mes = dev.index.get_level_values("date").strftime("%Y-%m")
    excecao = pd.Series(mes.isin(_IDENTITY_EXCEPTION_MONTHS), index=dev.index)
    limite = excecao.map({True: _IDENTITY_TOL_EXCEPTION, False: _IDENTITY_TOL})

    ruim = dev[dev > limite]
    if not ruim.empty:
        pior = ruim.sort_values(ascending=False).head(5)
        raise RuntimeError(
            f"{_FILENAME}: identidade estoque/fluxos violada em {len(ruim)} celula(s) fora da "
            f"janela de revisao conhecida. Piores desvios (R$ mi):\n{pior.to_string()}"
        )

    n_toleradas = int((dev[excecao] > _IDENTITY_TOL).sum())
    print(
        f"Identidade estoque = soma dos 8 fatores conferida em {len(dev)} celulas "
        f"({n_toleradas} desvio(s) tolerado(s) na janela 2003-2004 do BCB)."
    )


def run(start: str | None = None) -> None:
    """Atualiza macro_brasil.fisc_dlsp_fatores.

    A planilha do BCB so existe como historico completo (nao ha parametro
    incremental na fonte), entao o download e sempre inteiro (~2MB) e a
    validacao da identidade roda sempre sobre a serie toda. `start` filtra
    apenas o que vai para o banco.

    Args:
        start: data inicial ISO ("YYYY-MM-DD" ou "YYYY-MM") para limitar as
               linhas gravadas. None (default) grava o historico completo --
               e o recomendado: o BCB revisa historico, e um upsert so da
               janela recente deixaria a revisao antiga desatualizada no banco.
    """
    te = TabelasEspeciais()
    sheets = te.read_sheets(_FILENAME, list(_FATORES))

    dates = _parse_dates(sheets["Estoques"])

    frames = [_parse_sheet(sheets[aba], fator, dates) for aba, fator in _FATORES.items()]
    df = pd.concat(frames, ignore_index=True)

    _validate(df)

    if start:
        df = df[df["date"] >= pd.Timestamp(start)]

    print(
        f"{_TABLE}: {len(df)} linhas ({df['item'].nunique()} itens x {df['fator'].nunique()} fatores, "
        f"{df['date'].min().date()} -> {df['date'].max().date()})."
    )
    insert_data_into_database(_DATABASE, _TABLE, df)
