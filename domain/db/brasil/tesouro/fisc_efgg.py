"""
EFGG - Estatisticas Fiscais do Governo Geral (classificacao economica GFSM
2014 do FMI), Secretaria do Tesouro Nacional.

Despesa: 16 codigos por natureza economica (nao por rubrica orcamentaria/
funcao, como a RTN -- ver analytics/fiscal_policy/reference/rtn_vs_efgg.md
para a diferenciacao completa). Receita: 11 codigos por natureza economica
(adicionados 2026-08, ver "Impulso de receitas" em analytics/fiscal_policy/
CLAUDE.md -- mesmo connector/planilhas da despesa, so abas diferentes: Central
usa "2.2", Estados/Municipios usam "1.2", mesmo layout de cabecalho/linha
inicial que suas respectivas abas de despesa). Ambos trimestrais, por esfera
de governo (Governo Central, Estados, Municipios) mais o agregado "geral"
(soma das tres esferas, so nas datas em que as tres tem dado -- ver
`_build_geral()`). R$ milhoes, valores correntes.

Fonte primaria e diretamente a que o paper que originou o IEG (Impulso
Estrutural do Gasto, Resende & Pires, Textos para Discussao no.16, FGV/
Tesouro 2024, ver analytics/fiscal_policy/reference/impulso_estrutural_IEG.pdf)
usa: "Resultado de Estatisticas Fiscais do Governo Geral, disponibilizadas
pelo Tesouro Nacional". Essa tabela nao calcula o IEG em si (isso e um
indicador derivado -- multiplicadores fixos x variacao trimestral em % do
PIB -- que pertence a analytics/fiscal_policy/, nao a este script de ETL);
so guarda a serie bruta que o alimenta.

Mapeamento dos 4 grupos de despesa do paper -> codigo GFSM armazenado aqui:
    Folha          (multiplicador 1,32) -> salarios_vencimentos       (211)
    Transferencias (multiplicador 1,46) -> beneficios_previdenciarios_assistenciais (27)
    Investimentos  (multiplicador 1,66) -> aquisicao_ativos_nao_financeiros (31.1)
    Outras         (multiplicador 0,64) -> residuo = despesa_ajustada - (Folha+Transf.+Invest.),
                                            onde despesa_ajustada exclui consumo_capital_fixo (23),
                                            juros (24) e transferencias_doacoes (26)

Receita nao tem multiplicador equivalente usado nesta base ainda -- IEG
deliberadamente exclui receita (endogeneidade dos multiplicadores, ver
"Impulso de receitas" no CLAUDE.md citado acima); as 11 series de receita sao
guardadas cruas, prontas para quando essa decisao de metodologia for tomada.
Slugs de receita levam o prefixo "receita_" para nao colidir com nomes de
despesa que descrevem conceitos parecidos mas diferentes (ex: codigo de
despesa 212 "contribuicoes_sociais" vs. codigo de receita 12
"receita_contribuicoes_sociais" -- sao a despesa com contribuicoes sociais
dos empregadores e a arrecadacao de contribuicoes sociais, nao a mesma coisa).

Banco: macro_brasil.fisc_efgg -- PRIMARY KEY (date, name). name = "{esfera}_{slug}",
esfera em {central, estados, municipios, geral}.
"""

from __future__ import annotations

import os

import pandas as pd

from connectors.mysql import backup_table_before_truncate, insert_data_into_database, truncate_table
from connectors.tesouro_efgg import EFGG

_DATABASE = "macro_brasil"
_TABLE = "fisc_efgg"
_BACKUP_DIR = os.path.join(os.path.dirname(__file__), "_backups")

# Aba de despesa trimestral difere por esfera: Governo Central tem aba mensal
# ("1.3") alem da trimestral ("2.3"); Estados/Municipios so tem trimestral,
# na aba "1.3". Usar sempre a versao trimestral para as tres esferas serem
# comparaveis e somaveis.
_SHEETS = {
    "central": "2.3",
    "estados": "1.3",
    "municipios": "1.3",
}

# Aba de receita trimestral -- mesmo padrao de numeracao da despesa (Central
# tem "2.2", Estados/Municipios tem "1.2"), mesmo layout de cabecalho/linha
# inicial (confirmado ao vivo, 2026-08).
_SHEETS_RECEITA = {
    "central": "2.2",
    "estados": "1.2",
    "municipios": "1.2",
}

# Codigos de nivel superior da classificacao economica GFSM 2014 -- deixa de
# fora os subcodigos mais granulares (ex: 211.1/211.2, 271.1/271.2) porque o
# IEG so precisa do nivel superior e o resto normalmente esta vazio ("n.d.")
# para Estados/Municipios de qualquer forma.
_CODES = {
    "2M": "despesa_total",
    "2": "gasto",
    "21": "remuneracao_empregados",
    "211": "salarios_vencimentos",
    "212": "contribuicoes_sociais",
    "22": "uso_bens_servicos",
    "23": "consumo_capital_fixo",
    "24": "juros",
    "25": "subsidios",
    "26": "transferencias_doacoes",
    "27": "beneficios_previdenciarios_assistenciais",
    "28": "outros_gastos",
    "31": "investimento_liquido",
    "31.1": "aquisicao_ativos_nao_financeiros",
    "31.2": "venda_ativos_nao_financeiros",
    "31.3": "investimento_consumo_capital_fixo",
}

# Codigos de nivel superior da classificacao economica GFSM 2014 do lado da
# receita -- mesmo criterio de corte que _CODES (so nivel superior; 111-116
# e o unico segundo nivel mantido, para permitir o corte direto/indireto
# dentro de Impostos caso um dia seja necessario -- ver docstring do modulo).
_CODES_RECEITA = {
    "1": "receita_total",
    "11": "receita_impostos",
    "111": "receita_impostos_renda",
    "112": "receita_impostos_folha",
    "113": "receita_impostos_propriedade",
    "114": "receita_impostos_bens_servicos",
    "115": "receita_impostos_comercio_internacional",
    "116": "receita_outros_impostos",
    "12": "receita_contribuicoes_sociais",
    "13": "receita_transferencias_doacoes",
    "14": "receita_outras_receitas",
}

_QUARTER_MONTH = {"I": 1, "II": 4, "III": 7, "IV": 10}


def _parse_quarter_label(label) -> pd.Timestamp | None:
    if not isinstance(label, str) or "-" not in label:
        return None
    year, roman = label.split("-")
    month = _QUARTER_MONTH.get(roman)
    if month is None:
        return None
    return pd.Timestamp(int(year), month, 1)


def _parse_esfera_sheet(raw: pd.DataFrame, codes_map: dict[str, str]) -> pd.DataFrame:
    """raw: DataFrame cru (header=None) de uma aba de despesa OU receita trimestral.

    Linha 3 (indice 3) = cabecalho de periodo: col 0/1 vazias, colunas 2+ tem
    rotulos "YYYY-I".."YYYY-IV". Linhas 4+ = codigo (col 0), rotulo (col 1),
    valores (col 2+). Valores "n.d." (nao disponivel, comum em Estados/
    Municipios para subcodigos) viram NaN e sao descartados.

    codes_map: _CODES (despesa) ou _CODES_RECEITA (receita) -- os dois
    conjuntos de codigos nao se sobrepoem (despesa comeca em "2"/"3", receita
    em "1"), entao aplicar o mapa errado a uma aba so resultaria em zero
    linhas casadas, nao em dado errado.
    """
    header_row = raw.iloc[3]
    dates = header_row.iloc[2:].map(_parse_quarter_label)

    codes = raw.iloc[4:, 0].astype(str).str.strip()
    mask = codes.isin(codes_map)
    body = raw.iloc[4:][mask]
    names = codes[mask].map(codes_map)

    chunks = []
    for col in dates.index:
        date = dates[col]
        if date is None:
            continue
        values = pd.to_numeric(body[col], errors="coerce")
        chunks.append(pd.DataFrame({"date": date, "name": names.values, "value": values.values}))

    return pd.concat(chunks, ignore_index=True).dropna(subset=["value"])


def _build_geral(per_esfera: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Agrega Governo Geral = Central + Estados + Municipios, celula a celula.

    So soma nas datas em que as TRES esferas tem dado -- Municipios atrasa
    ~1 trimestre em relacao a Central/Estados (ver reference doc), e um
    "geral" calculado so com 2 das 3 esferas ficaria artificialmente baixo,
    exatamente o tipo de numero silenciosamente errado que este projeto evita
    (ver domain/db/CLAUDE.md e o precedente do truncate_table em fisc_rtn.py).
    """
    wide = {esfera: df.pivot(index="date", columns="name", values="value") for esfera, df in per_esfera.items()}

    common_dates = wide["central"].index
    for w in wide.values():
        common_dates = common_dates.intersection(w.index)

    geral = wide["central"].loc[common_dates]
    for esfera in ("estados", "municipios"):
        geral = geral.add(wide[esfera].loc[common_dates], fill_value=0)

    long_df = geral.reset_index().melt(id_vars="date", var_name="name", value_name="value").dropna(subset=["value"])
    long_df["name"] = "geral_" + long_df["name"]
    return long_df[["date", "name", "value"]]


def run(start: str | None = None) -> None:
    """Atualiza macro_brasil.fisc_efgg.

    Trunca a tabela antes de recarregar -- mesmo motivo/precedente de
    fisc_rtn.py: a fonte so distribui historico completo por chamada (sem
    parametro incremental), entao um upsert por chave deixaria sobreviver
    silenciosamente qualquer linha antiga cujo periodo a nova carga nao
    cubra mais sob a mesma chave.

    Antes de truncar, salva um snapshot CSV da tabela atual em `_BACKUP_DIR`
    (ultimos 5 mantidos, ver backup_table_before_truncate() em
    connectors/mysql.py) -- permite comparar com a rodada anterior se algum
    valor mudar de forma abrupta numa carga futura.

    Args:
        start: nao utilizado -- a EFGG so distribui cada anexo como historico
               completo. Mantido por consistencia de assinatura com os
               demais scripts run().
    """
    efgg = EFGG()
    urls = efgg.get_current_urls()

    per_esfera = {}
    for esfera in _SHEETS:
        raw_despesa = efgg.download_table(urls[esfera], sheet_name=_SHEETS[esfera])
        raw_receita = efgg.download_table(urls[esfera], sheet_name=_SHEETS_RECEITA[esfera])
        despesa = _parse_esfera_sheet(raw_despesa, _CODES)
        receita = _parse_esfera_sheet(raw_receita, _CODES_RECEITA)
        per_esfera[esfera] = pd.concat([despesa, receita], ignore_index=True)

    tagged = []
    for esfera, df in per_esfera.items():
        d = df.copy()
        d["name"] = f"{esfera}_" + d["name"]
        tagged.append(d)

    geral = _build_geral(per_esfera)

    df = pd.concat(tagged + [geral], ignore_index=True)
    backup_table_before_truncate(_DATABASE, _TABLE, _BACKUP_DIR)
    truncate_table(_DATABASE, _TABLE)
    insert_data_into_database(_DATABASE, _TABLE, df)
