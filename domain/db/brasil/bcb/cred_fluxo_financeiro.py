"""
Fluxo financeiro do credito bancario (concessoes - pagamentos), em % do PIB
acumulado em 12 meses -- a serie a partir da qual o BCB define o IMPULSO DE
CREDITO no conceito dele.

Fonte: anexo estatistico do RI/RPM (ver connectors/bcb_rpm.py), grafico "Fluxo
financeiro acumulado em 12 meses" do capitulo de conjuntura. NAO existe no SGS, e
nao da para reconstruir de fora: a perna de PAGAMENTOS e uma proxy que o BCB
deriva da decomposicao do saldo usando juros acruados, variacao cambial e baixas
para prejuizo, nenhum dos tres publicado. Concessoes estao no SGS; pagamentos,
nao.

## Escopo: TRES series, Total/PJ/PF, e nada abaixo disso

O grafico recorrente publica exatamente essas tres, e o boxe de 2025-03 ("Fluxo
financeiro e impulso de credito em 2024", RPM) publica as mesmas tres desde
2015-01 -- mais uma quebra Livre/Direcionado que **fica de fora**. Entao o boxe
entra so pelo trecho 2015-01..2017-12, que estende o historico, e nao pelo nivel
extra, que nao se repete.

A distincao e o que faz a emenda funcionar, e ela custou uma rodada para ficar
clara. Carregando as 7 series do boxe, os 4 filhos ficavam num vintage e os pais
noutro assim que a edicao corrente sobrepunha o trecho comum, e a **aditividade
parava de fechar** (residuo de 0,095 p.p. em PJ e 0,196 em PF -- o tamanho da
revisao entre edicoes). Com as duas fontes publicando o MESMO conjunto de 3
series, o problema desaparece por construcao: cada edicao escreve as 3 de todos
os meses dela de uma vez, entao um mes qualquer tem sempre as 3 vindas da mesma
edicao, e preferir a mais nova na sobreposicao e seguro.

O **impulso** tambem nao entra como dado: o BCB nao o publica como serie -- ele
saiu em boxe duas vezes em 20 edicoes com anexo (RI de set/2021 e RPM de
mar/2025), e a nota 1 do primeiro diz *"nao ha intencao de calcular essas series
de forma recorrente ou sistematica"*. O que e recorrente e o fluxo; o impulso e
derivado dele no relatorio.

## As duas fontes encadeiam, e isso foi medido

Mesma definicao e mesma unidade, com 85 meses de sobreposicao (2018-01..2025-01)
entre o boxe e o grafico recorrente da edicao 2026-03. A diferenca ali e revisao
de vintage, nao quebra: **PJ 0,038 p.p. em media e 0,095 no maximo; PF 0,059 e
0,196; Total 0,090 e 0,241**. Nenhuma correcao de nivel e aplicada -- deslocar o
trecho antigo para casar com o novo inventaria dado que ninguem publicou.

Na pratica a emenda nao se ve: como a edicao corrente vence na sobreposicao, o
boxe sobra so ate onde a janela dela comeca (2018-03, com a edicao 2026-06), e o
degrau ali e de **0,343 p.p. no total** -- 79o percentil dos passos mensais da
propria serie, com o trecho subindo monotonicamente de -5,92 a -4,60 em volta. A
emenda ANDA um trimestre a cada edicao nova; quando ela passar de 2025-01 o boxe
deixa de aparecer inteiro, e so o trecho 2015-2017 sobra dele.

Onde a emenda importa e no IMPULSO, nao no nivel: os 12 pontos cuja janela de 12
meses a cruza misturam duas edicoes e carregam ate 0,24 p.p. de revisao alheia ao
movimento do fluxo.

## Por que so a leitura em % do PIB

O mesmo grafico sai em duas unidades conforme a era: **R$ bilhoes deflacionados**
ate a edicao 2025-12, e **% do PIB acumulado em 12 meses** de 2026-03 em diante.
So a segunda encadeia entre edicoes -- a versao em R$ vem "em reais do mes da
edicao", ou seja com base de deflator que muda a cada trimestre, e rebasear nao
fecha (medido entre as edicoes 2021-09 e 2025-03: fator implicito 1,2655, R2
0,996, contra 1,2208 de IPCA no periodo). Por isso `_PADRAO_RECORRENTE` exige o
"acumulado em 12 meses" do titulo, que so aparece na forma nova: apontar o script
para uma edicao anterior a 2026-03 levanta, em vez de gravar R$ como se fosse %.

## Sinal

Fluxo = concessoes - pagamentos. **Negativo = o setor real (familias e empresas)
paga ao SFN mais do que toma emprestado**, que e o normal (a remuneracao dos
servicos financeiros). O boxe de 2025-03 le -0,9% de dez/2024 como "o sistema
financeiro recebeu 0,9% do PIB em recursos liquidos do setor nao financeiro".

O IMPULSO e a variacao em 12 meses deste fluxo, e NAO esta gravado aqui -- e
derivado em analytics/brasil/credit/impulso_tab.py, mesma escolha que ja vale
para o impulso de Biggs et al. (a tabela guarda o dado publicado, o relatorio
calcula a metrica). Confere com o numero que o proprio BCB imprime: pelo dado
desta tabela o fluxo vai de -1,9% (dez/2023) a -0,7% (dez/2024), impulso +1,2
p.p., contra o "+1,1% do PIB" escrito no boxe de mar/2025 -- a diferenca e
revisao de vintage, nao de metodo.

## Janela movel, e a tabela ACUMULA

Cada edicao publica uma janela movel de 97 meses (8 anos) que rola um trimestre
por vez. A carga e upsert, nao truncate: a edicao nova reescreve os meses que ela
cobre e os anteriores, que ela ja nao publica, ficam. Entao o historico da tabela
cresce a cada edicao em vez de deslizar junto com a fonte, e `vintage` registra de
que edicao veio cada mes.

Ordem de escrita em `run()`: boxe primeiro, edicao corrente depois -- o
`ON DUPLICATE KEY UPDATE` faz a ultima vencer, entao a sobreposicao fica com a
edicao mais recente. Para estender ainda mais o historico do lado do grafico
recorrente, rode `run(vintage="AAAA-MM")` numa edicao mais antiga ANTES da
corrente; hoje isso vale so para 2026-03 (+3 meses), porque as anteriores publicam
em R$.

## Variaveis

    fluxo_total   Total (PJ + PF)
    fluxo_pj      Pessoas juridicas
    fluxo_pf      Pessoas fisicas

## Historico

2015-01 -> mes de referencia da edicao corrente. O comeco e o do boxe; sem ele a
serie comecaria em 2018-01, primeira edicao a publicar o grafico recorrente em %
do PIB.

## Aditividade

Exata na fonte, conferida a cada carga: PJ + PF = Total, residuo maximo 0,000000.
`run()` levanta em vez de gravar se isso deixar de valer -- e o que faz a arvore
do relatorio ser decomposicao de verdade.

## Banco

macro_brasil.cred_fluxo_financeiro -- PRIMARY KEY (date, name).

DDL:
  CREATE TABLE macro_brasil.cred_fluxo_financeiro (
      date     DATE          NOT NULL,
      name     VARCHAR(40)   NOT NULL,
      value    DECIMAL(12,6),
      vintage  DATE          NOT NULL,
      PRIMARY KEY (date, name)
  );
"""

from __future__ import annotations

import datetime as dt
import re

import pandas as pd

from connectors.bcb_rpm import AnexoRPM, normalizar
from connectors.mysql import insert_data_into_database

_DATABASE = "macro_brasil"
_TABLE = "cred_fluxo_financeiro"

# Titulo do grafico. Casa contra o bloco de cabecalho da coluna A, nunca contra o nome da
# aba -- o numero do grafico anda a cada edicao (1.2.28 na 2026-03, 1.2.30 na 2026-06).
# O "acumulado em 12 meses" e load-bearing duas vezes: separa esta era da anterior, em R$
# (ver docstring), e o grafico irmao de debentures quebra a sequencia contigua
# ("...fluxo financeiro DE DEBENTURES acumulado em 12 meses"), entao nao casa.
_PADRAO_RECORRENTE = r"fluxo financeiro acumulado em 12 meses"

# Rotulo publicado na linha de cabecalho -> sufixo do nome da serie.
_COLUNAS = {"pessoas juridicas": "pj", "pessoas fisicas": "pf", "total": "total"}

# --- Boxe "Fluxo financeiro e impulso de credito em 2024" (RPM 2025-03) --------------
# Entra SO pelo trecho 2015-01..2017-12, que o grafico recorrente nao alcanca em % do
# PIB. Dele saem as MESMAS 3 series -- a quebra Livre/Direcionado que o boxe tambem
# publica fica de fora de proposito (ver "Escopo" na docstring: duas fontes com conjuntos
# de series diferentes e o que quebrava a aditividade).
_VINTAGE_BOXE = dt.date(2025, 3, 1)

# Total: Grafico 2, que traz o fluxo em duas unidades lado a lado (R$ bilhoes acumulados
# no trimestre e % do PIB em 12 meses). So a segunda serve aqui.
_PADRAO_BOXE_TOTAL = r"grafico 2 . fluxo financeiro$"
_COLUNA_BOXE_TOTAL = "% pib"

# PJ e PF: dois graficos com titulo IDENTICO, distinguidos pelo subtitulo da linha
# seguinte. Ancorado no fim ($) para nao pegar o Grafico 10 do mesmo boxe, "Decomposicao
# do fluxo financeiro de Debentures" -- mercado de capitais, nao credito bancario.
_PADRAO_BOXE_SEG = r"decomposicao do fluxo financeiro$"
_SUBTITULOS = {"pessoas juridicas": "pj", "pessoas fisicas": "pf"}
_COLUNA_BOXE_SEG = "total"

_MIN_LINHAS = 60  # abaixo disso a aba nao e a que se procura, ou o layout mudou


def _bloco(ws) -> tuple[list[str], pd.DataFrame]:
    """(rotulos das colunas, DataFrame indexado por data) de uma aba do anexo.

    A linha de cabecalho e a que comeca com 'Data' ou 'Mes' na coluna A -- procurada,
    nao fixada por indice, porque o bloco de dados comeca na linha 9 em umas abas e na
    10 em outras dentro do MESMO arquivo.
    """
    grade = pd.DataFrame([list(r) for r in ws.iter_rows(values_only=True)])

    cabecalho = None
    for i in range(min(15, len(grade))):
        if normalizar(grade.iat[i, 0]) in ("data", "mes", "ano"):
            cabecalho = i
            break
    if cabecalho is None:
        raise RuntimeError(
            f"aba '{ws.title}': nenhuma linha de cabecalho ('Data'/'Mes') nas 15 "
            f"primeiras linhas -- o layout do anexo mudou."
        )

    rotulos = [normalizar(v) for v in grade.iloc[cabecalho].tolist()]
    corpo = grade.iloc[cabecalho + 1:]
    datas = pd.to_datetime(corpo.iloc[:, 0], errors="coerce")
    corpo = corpo[datas.notna()]
    datas = datas[datas.notna()]

    if len(corpo) < _MIN_LINHAS:
        raise RuntimeError(
            f"aba '{ws.title}': so {len(corpo)} linhas de data -- esperado >= "
            f"{_MIN_LINHAS}. Conferir se o BCB trocou o formato da coluna de data."
        )

    out = pd.DataFrame(
        {j: pd.to_numeric(corpo.iloc[:, j], errors="coerce") for j in range(1, grade.shape[1])}
    )
    out.index = [d.date().replace(day=1) for d in datas]
    return rotulos, out.sort_index()


def _abas_com(wb, padrao: str) -> list:
    """Todas as abas cujo bloco de cabecalho casa `padrao` (regex ja normalizado)."""
    rx = re.compile(padrao)
    return [ws for ws in wb.worksheets
            if any(rx.search(normalizar(l)) for l in AnexoRPM.cabecalho(ws))]


def _long(series: dict, vintage: dt.date) -> pd.DataFrame:
    linhas = []
    for name, s in series.items():
        for data, valor in s.items():
            if pd.isna(valor):
                continue
            linhas.append({"date": data, "name": name,
                           "value": round(float(valor), 6), "vintage": vintage})
    return pd.DataFrame(linhas)


def parse(anexo: AnexoRPM, vintage: dt.date) -> dict:
    """{'fluxo_pj'|'fluxo_pf'|'fluxo_total': Series} do grafico recorrente da edicao."""
    wb = anexo.abrir(vintage)
    abas = _abas_com(wb, _PADRAO_RECORRENTE)
    if not abas:
        raise RuntimeError(
            f"edicao {vintage:%Y-%m}: nenhuma aba com titulo casando "
            f"/{_PADRAO_RECORRENTE}/. Esse grafico so sai em % do PIB desde a edicao "
            f"2026-03 (antes era em R$ deflacionados, que nao encadeia) -- se a edicao "
            f"e posterior a essa, o BCB renomeou o grafico e o padrao precisa mudar."
        )
    rotulos, dados = _bloco(abas[0])

    out = {}
    for j, rotulo in enumerate(rotulos):
        sufixo = _COLUNAS.get(rotulo)
        if sufixo and j in dados:
            out[f"fluxo_{sufixo}"] = dados[j].dropna()
    faltando = set(_COLUNAS.values()) - {k.removeprefix("fluxo_") for k in out}
    if faltando:
        raise RuntimeError(
            f"edicao {vintage:%Y-%m}, aba '{abas[0].title}': colunas ausentes {faltando}. "
            f"Rotulos encontrados: {rotulos}."
        )
    return out


def parse_boxe(anexo: AnexoRPM, vintage: dt.date = _VINTAGE_BOXE) -> dict:
    """As MESMAS 3 series, do boxe de 2025-03 -- Grafico 2 (total, coluna % PIB) e
    Graficos 3 e 4 (PJ e PF, coluna Total). A quebra Livre/Direcionado dos dois ultimos
    e deliberadamente ignorada; ver "Escopo" na docstring do modulo."""
    wb = anexo.abrir(vintage)

    totais = _abas_com(wb, _PADRAO_BOXE_TOTAL)
    if len(totais) != 1:
        raise RuntimeError(
            f"edicao {vintage:%Y-%m}: esperada 1 aba casando /{_PADRAO_BOXE_TOTAL}/ "
            f"(o total do boxe), achadas {len(totais)}."
        )
    rotulos, dados = _bloco(totais[0])
    if _COLUNA_BOXE_TOTAL not in rotulos:
        raise RuntimeError(
            f"aba '{totais[0].title}': coluna '{_COLUNA_BOXE_TOTAL}' ausente "
            f"(rotulos={rotulos}). Sem ela o total sairia em R$, que nao encadeia."
        )
    out = {"fluxo_total": dados[rotulos.index(_COLUNA_BOXE_TOTAL)].dropna()}

    segmentos = _abas_com(wb, _PADRAO_BOXE_SEG)
    if len(segmentos) != 2:
        raise RuntimeError(
            f"edicao {vintage:%Y-%m}: esperadas 2 abas casando /{_PADRAO_BOXE_SEG}/ "
            f"(PJ e PF), achadas {len(segmentos)}."
        )
    for ws in segmentos:
        linhas = [normalizar(l) for l in AnexoRPM.cabecalho(ws)]
        seg = next((v for l in linhas for k, v in _SUBTITULOS.items() if k in l), None)
        if seg is None:
            raise RuntimeError(
                f"aba '{ws.title}': subtitulo nao identifica PJ nem PF (linhas={linhas})."
            )
        rotulos, dados = _bloco(ws)
        if _COLUNA_BOXE_SEG not in rotulos:
            raise RuntimeError(
                f"aba '{ws.title}': coluna '{_COLUNA_BOXE_SEG}' ausente (rotulos={rotulos})."
            )
        out[f"fluxo_{seg}"] = dados[rotulos.index(_COLUNA_BOXE_SEG)].dropna()

    return out


def _checar_aditividade(series: dict, rotulo: str, tol: float = 1e-6) -> None:
    """PJ + PF = Total. A propriedade que faz a arvore do relatorio ser decomposicao e
    nao aproximacao -- se um dia parar de valer, e porque o BCB mudou a definicao, e a
    carga tem que parar em vez de gravar em silencio uma hierarquia que nao fecha."""
    if not {"fluxo_total", "fluxo_pj", "fluxo_pf"} <= set(series):
        return
    soma = series["fluxo_pj"] + series["fluxo_pf"]
    comum = series["fluxo_total"].index.intersection(soma.index)
    if not len(comum):
        return
    erro = float((series["fluxo_total"].loc[comum] - soma.loc[comum]).abs().max())
    print(f"    {rotulo}: |fluxo_pj + fluxo_pf - fluxo_total| max = {erro:.6f}")
    if erro > tol:
        raise RuntimeError(
            f"{rotulo}: fluxo_total nao fecha com fluxo_pj + fluxo_pf (residuo maximo "
            f"{erro:.6f} > {tol}). A hierarquia deixou de ser aditiva -- conferir o "
            f"anexo antes de gravar."
        )


def run(vintage: str | dt.date | None = None, *, com_boxe: bool = True) -> None:
    """Atualiza macro_brasil.cred_fluxo_financeiro com o grafico de fluxo financeiro da
    edicao do RPM.

    Args:
        vintage: edicao a ler, "AAAA-MM" ou date. None (default) descobre a mais
                 recente publicada -- o comportamento de rotina. Passar uma edicao
                 antiga faz BACKFILL: a carga e upsert, entao rodar a antiga antes da
                 corrente estende o historico para tras sem sobrescrever a ponta (ver
                 "Janela movel" na docstring). So funciona de 2026-03 em diante; antes
                 disso o grafico sai em R$ e o parse levanta.
        com_boxe: tambem carrega o trecho 2015-01..2017-12 do boxe de 2025-03, que o
                  grafico recorrente nao alcanca em % do PIB. Deixar True: e uma edicao
                  a mais para baixar, uma vez por passe, e garante que a tabela seja
                  reconstituivel do zero por um comando.
    """
    anexo = AnexoRPM()

    if vintage is None:
        alvo = anexo.vintage_mais_recente()
        if alvo is None:
            raise RuntimeError(
                "nenhuma edicao do anexo estatistico do RPM respondeu -- "
                "conferir connectors/bcb_rpm.py (o BCB pode ter mudado a URL)."
            )
    else:
        alvo = vintage if isinstance(vintage, dt.date) else pd.Timestamp(vintage).date().replace(day=1)

    quadros = []

    # Boxe primeiro: onde as duas fontes cobrem o mesmo mes, a edicao corrente vence
    # (o insert faz a ultima escrita ganhar). Seguro porque as duas publicam o MESMO
    # conjunto de 3 series -- ver "Escopo" na docstring.
    if com_boxe:
        boxe = parse_boxe(anexo)
        _checar_aditividade(boxe, f"boxe {_VINTAGE_BOXE:%Y-%m}")
        df_boxe = _long(boxe, _VINTAGE_BOXE)
        print(f"{_TABLE}: boxe {_VINTAGE_BOXE:%Y-%m}, {len(df_boxe)} linhas, "
              f"{df_boxe['date'].min()} -> {df_boxe['date'].max()}, series={sorted(boxe)}.")
        quadros.append(df_boxe)

    series = parse(anexo, alvo)
    _checar_aditividade(series, f"edicao {alvo:%Y-%m}")
    df = _long(series, alvo)
    print(f"{_TABLE}: edicao {alvo:%Y-%m}, {len(df)} linhas, "
          f"{df['date'].min()} -> {df['date'].max()}, series={sorted(series)}.")
    quadros.append(df)

    for quadro in quadros:
        insert_data_into_database(_DATABASE, _TABLE, quadro)


if __name__ == "__main__":
    run()
