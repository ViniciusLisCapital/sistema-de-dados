"""
Parsing compartilhado do grafico de hiato do produto do anexo estatistico do
RI/RPM -- usado por `pm_hiato_produto.py` (edicao corrente) e
`pm_hiato_produto_vintages.py` (o painel de todas as edicoes).

Existe separado porque os dois scripts leem a MESMA aba com as MESMAS
armadilhas; duplicar o parser garantiria que as duas tabelas divergissem na
primeira vez que o BCB mudasse alguma coisa. Mesmo motivo do
`domain/db/brasil/mte/_caged_core.py`.

## As cinco armadilhas desta aba (todas confirmadas ao vivo, 2026-08)

1. **O numero do grafico anda.** Ja foi `Graf 2.2.3` (2021-09/12), `2.2.4`
   (2022-03 a 2024-03), `2.2.6` (2024-06) e `2.2.8` (2024-09 em diante).
   Localizamos por titulo via `AnexoRPM.localizar_aba()`, nunca por nome de aba.

2. **O titulo tambem muda**: "Estimativa do hiato do produto" ate 2024-06,
   "Hiato do produto: estimativas e dispersao" depois. `_PADRAO_ABA` casa a
   parte estavel ("grafico 2.2.<n>" + "hiato do produto").

3. **Duas metodologias de apresentacao.** Ate 2024-06 a aba traz um modelo com
   banda de +-2 desvios-padrao; de 2024-09 em diante traz a DISPERSAO de uma
   suite de modelos (minimo/P25/P75/maximo) mais o "Cenario de referencia".
   A serie comparavel entre todas as edicoes e a central: `Hiato` no regime
   antigo e `Cenario de referencia` no novo, ambos gravados como `central`.

4. **Rotulo de trimestre em tres formatos**: data de verdade na maioria das
   edicoes, `"IV\\n2003"` em 2021-09 e `"2003 IV"` em 2021-12.

5. **A convencao de data muda no meio da serie** -- a mais perigosa das cinco,
   porque nao quebra nada, so desalinha. Ate a edicao 2022-03 o trimestre e
   carimbado no seu PRIMEIRO mes (2003-10-01 = 2003T4); de 2022-06 em diante,
   no ULTIMO (2003-12-01 = 2003T4). Sem normalizar, as edicoes antigas entram
   defasadas em um trimestre contra as novas e a matriz de revisao fica errada
   com numeros que parecem plausiveis. Tudo e normalizado para o PRIMEIRO mes
   do trimestre, que e a convencao do resto do banco (`atv_pib`, `atv_pib_taxas`,
   `cred_ptc` -- todas com meses 1/4/7/10).

Rotulos de coluna tambem variam dentro do mesmo regime: as edicoes 2022-12,
2023-03 e 2023-06 chamam a banda SUPERIOR de "Hiato +- 2 desvios-padrao".
`_CANON` mapeia todas as grafias ja vistas; qualquer rotulo novo levanta em vez
de ser ignorado em silencio -- uma coluna nova do BCB tem que virar decisao
explicita, nao sumir.
"""

from __future__ import annotations

import datetime as dt
import re

import pandas as pd

from connectors.bcb_rpm import AnexoRPM, normalizar

# Casa "Grafico 2.2.3/2.2.4/2.2.6/2.2.8 - ... hiato do produto ..." em qualquer
# edicao. O texto ja chega normalizado (minusculo, sem acento).
_PADRAO_ABA = r"^grafico 2\.2\.\d+ .*hiato do produto"

# Rotulo publicado (normalizado) -> nome canonico no banco.
_CANON = {
    # regime "banda" (ate 2024-06): um modelo + banda de +-2 desvios-padrao
    "hiato": "central",
    "hiato + 2 desvios-padrao": "banda_sup",
    "hiato +2 desvios-padrao": "banda_sup",
    "hiato +2 d.p.": "banda_sup",
    "hiato +- 2 desvios-padrao": "banda_sup",
    "hiato - 2 desvios-padrao": "banda_inf",
    "hiato -2 desvios-padrao": "banda_inf",
    "hiato -2 d.p.": "banda_inf",
    "hiato -2 desvio-padrao": "banda_inf",
    # regime "suite" (de 2024-09): dispersao entre modelos + cenario de referencia
    "cenario de referencia": "central",
    "minimo": "minimo",
    "percentil 25": "p25",
    "percentil 75": "p75",
    "maximo": "maximo",
}

VARIAVEIS = sorted(set(_CANON.values()))

# Rotulos aceitos na celula que abre a coluna de datas.
_ROTULOS_EIXO_X = ("trimestre", "data", "periodo")

_ROMANO_INICIO_TRI = {"I": 1, "II": 4, "III": 7, "IV": 10}
_RE_ROMANO_ANO = re.compile(r"^(I{1,3}|IV) (\d{4})$")
_RE_ANO_ROMANO = re.compile(r"^(\d{4}) ?T?(I{1,3}|IV)$")
_RE_WS = re.compile(r"\s+")


def _inicio_do_trimestre(ano: int, mes: int) -> dt.date:
    """Snap para o PRIMEIRO mes do trimestre (ver armadilha 5 na docstring)."""
    return dt.date(ano, ((mes - 1) // 3) * 3 + 1, 1)


def _para_data(valor: object) -> dt.date | None:
    """Rotulo de trimestre -> primeiro mes do trimestre, ou None se nao for um."""
    if isinstance(valor, (dt.datetime, dt.date)):
        return _inicio_do_trimestre(valor.year, valor.month)
    texto = _RE_WS.sub(" ", str(valor).strip())
    m = _RE_ROMANO_ANO.match(texto)
    if m:
        return dt.date(int(m.group(2)), _ROMANO_INICIO_TRI[m.group(1)], 1)
    m = _RE_ANO_ROMANO.match(texto)
    if m:
        return dt.date(int(m.group(1)), _ROMANO_INICIO_TRI[m.group(2)], 1)
    return None


def _linha_do_cabecalho(grade: pd.DataFrame) -> int:
    for i, rotulo in grade[0].items():
        if rotulo is not None and normalizar(rotulo) in _ROTULOS_EIXO_X:
            return i
    raise RuntimeError(
        f"aba do hiato sem linha de cabecalho reconhecivel (procurados "
        f"{_ROTULOS_EIXO_X} na coluna A)."
    )


def _mapear_colunas(grade: pd.DataFrame, linha: int, vintage: dt.date) -> dict[int, str]:
    colunas: dict[int, str] = {}
    desconhecidas: list[str] = []
    for j in range(1, grade.shape[1]):
        rotulo = grade.iat[linha, j]
        if rotulo is None or not str(rotulo).strip():
            continue
        chave = normalizar(rotulo)
        if chave in _CANON:
            colunas[j] = _CANON[chave]
        else:
            desconhecidas.append(str(rotulo).strip())
    if desconhecidas:
        raise RuntimeError(
            f"edicao {vintage:%Y-%m}: coluna(s) nao mapeada(s) na aba do hiato: "
            f"{desconhecidas}. O BCB mudou a apresentacao -- decidir o nome "
            f"canonico e adicionar em _CANON (domain/db/brasil/bcb/_rpm_hiato.py) "
            f"antes de gravar."
        )
    if "central" not in colunas.values():
        raise RuntimeError(
            f"edicao {vintage:%Y-%m}: aba do hiato sem coluna central "
            f"('Hiato' ou 'Cenario de referencia'). Colunas lidas: {sorted(set(colunas.values()))}."
        )
    return colunas


def parse(anexo: AnexoRPM, vintage: dt.date) -> tuple[pd.DataFrame, str]:
    """Le o hiato do produto de uma edicao.

    Args:
        anexo: cliente `AnexoRPM` (reaproveita o cache de download entre edicoes).
        vintage: primeiro dia do mes de publicacao (ex: date(2026, 6, 1)).

    Returns:
        (DataFrame com colunas date/variavel/value ordenado, nome da aba lida).
    """
    wb = anexo.abrir(vintage)
    ws, _titulo = anexo.localizar_aba(wb, _PADRAO_ABA)
    aba = ws.title
    grade = anexo.grade(ws)

    linha = _linha_do_cabecalho(grade)
    colunas = _mapear_colunas(grade, linha, vintage)

    registros = []
    for i in range(linha + 1, len(grade)):
        data = _para_data(grade.iat[i, 0]) if grade.iat[i, 0] is not None else None
        if data is None:
            continue
        for j, variavel in colunas.items():
            valor = grade.iat[i, j]
            if isinstance(valor, (int, float)) and not isinstance(valor, bool):
                registros.append({"date": data, "variavel": variavel,
                                  "value": round(float(valor), 4)})

    df = pd.DataFrame(registros)
    if df.empty:
        raise RuntimeError(f"edicao {vintage:%Y-%m}: aba '{aba}' do hiato sem dados apos o parsing.")

    duplicadas = df.duplicated(subset=["date", "variavel"]).sum()
    if duplicadas:
        raise RuntimeError(
            f"edicao {vintage:%Y-%m}: {duplicadas} par(es) (date, variavel) duplicado(s) -- "
            f"a normalizacao de trimestre colapsou linhas distintas."
        )

    return df.sort_values(["date", "variavel"]).reset_index(drop=True), aba
