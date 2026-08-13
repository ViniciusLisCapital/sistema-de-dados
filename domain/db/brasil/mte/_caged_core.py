"""
Lógica compartilhada de download+combinação+agregação do Novo CAGED (FTP do
PDET/MTE) -- usada por mt_caged_setor.py / mt_caged_uf.py / mt_caged_salario.py.
Não é um script de domínio próprio (sem `run()`), só o núcleo comum.

Fonte: ftp://ftp.mtps.gov.br/pdet/microdados/NOVO CAGED/<AAAA>/<AAAAMM>/
Ver connectors/pdet_ftp.py para o cliente FTP (encoding Latin-1) e a
docstring de cada arquivo MOV/FOR/EXC.

## Fórmula de saldo por competência de MOVIMENTAÇÃO (validada ao vivo, 2026-08)

    saldo(X)         = MOV(X) + FOR(X) - EXC(X)
    admissões(X)      = Σ valores positivos de MOV+FOR  -  Σ valores positivos de EXC
    desligamentos(X)  = Σ |valores negativos| de MOV+FOR -  Σ |valores negativos| de EXC

`saldomovimentação` é sempre ±1 por linha (admissão=+1, desligamento=-1).
Confirmado inspecionando linhas reais de CAGEDEXC202401.txt: uma exclusão de
desligamento (tipomovimentação=40, "Desligamento a pedido") aparece com
saldomovimentação=-1 -- ou seja, EXC guarda o SINAL ORIGINAL do registro que
está sendo cancelado, não pré-invertido. Por isso a fórmula SUBTRAI o EXC em
vez de somar.

## Por que "competência do arquivo" != "competência de movimentação"

Cada arquivo pertence a uma competência de RELEASE (ex: o release de
2024-01 publica CAGEDMOV202401.7z + CAGEDFOR202401.7z + CAGEDEXC202401.7z).
Confirmado ao vivo:
  - CAGEDMOV<AAAAMM>: TODA linha tem competênciamov==AAAAMM -- é um arquivo
    fixo, nunca revisado depois de publicado. Só precisa ser baixado UMA VEZ,
    na sua própria competência de release.
  - CAGEDFOR<AAAAMM>/CAGEDEXC<AAAAMM>: contêm linhas com competênciamov de
    QUALQUER mês anterior a AAAAMM (ex: o FOR de 2024-01 corrigiu
    competências de movimentação espalhadas por 2023 inteiro). Ou seja, o
    saldo "final" de uma competência passada só fica completo depois que
    TODOS os releases seguintes já publicaram seus FOR/EXC -- a mesma
    "reescrita histórica silenciosa" confirmada no HANDOVER.md.

Consequência prática: uma reconstrução histórica completa (`start="all"`)
precisa varrer o MOV+FOR+EXC de TODOS os releases desde 2020-01, agregando
por competência de movimentação (não pela competência do arquivo) --
implementado em `carregar_releases`/`agregar_por_corte` abaixo. Uma
atualização de rotina (`n_meses` recente) só reprocessa os releases mais
recentes -- suficiente para capturar a maioria das correções (fora-do-prazo
é aceito por até 12 meses, ver Leia-me do FTP), mas não reabre uma exclusão
rara referente a uma competência muito antiga fora dessa janela.
"""

import shutil
import tempfile

import pandas as pd

from connectors.pdet_ftp import baixar_7z, extrair_csv, listar_anos, listar_competencias

_COLS = ["competênciamov", "saldomovimentação", "seção", "uf", "salário"]


def competencias_disponiveis() -> list[str]:
    """Lista todas as competências de release publicadas no FTP, em ordem."""
    comps = []
    for ano in listar_anos():
        comps.extend(listar_competencias(int(ano)))
    return sorted(comps)


def resolver_releases(n_meses: int, start: str | None, end: str | None) -> list[str]:
    """Resolve a lista de competências de RELEASE a processar.

    Args:
        n_meses: últimos N releases publicados (ignorado se start for dado).
        start:   "AAAAMM" inicial, ou "all" para a série completa desde 2020-01.
        end:     "AAAAMM" final (default: o último release disponível).
    """
    disponiveis = competencias_disponiveis()
    if start == "all":
        return disponiveis
    if start:
        fim = end or disponiveis[-1]
        return [c for c in disponiveis if start <= c <= fim]
    return disponiveis[-n_meses:]


def _ler_arquivo(competencia: str, tipo: str) -> pd.DataFrame:
    nome_interno = f"CAGED{tipo}{competencia}.txt"
    conteudo = baixar_7z(competencia, tipo)
    tmp = tempfile.mkdtemp(prefix="caged_")
    try:
        path = extrair_csv(conteudo, nome_interno, tmp)
        df = pd.read_csv(path, sep=";", decimal=",", encoding="utf-8", usecols=_COLS)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    df["_sinal"] = 1 if tipo in ("MOV", "FOR") else -1
    return df


def carregar_releases(releases: list[str]) -> pd.DataFrame:
    """Baixa e empilha MOV+FOR+EXC de cada competência de release em `releases`.

    Nunca persiste o microdado bruto em disco alem da extracao temporaria
    (apagada logo apos a leitura) -- padrao "agregar-e-descartar" do projeto.

    Returns:
        DataFrame com _COLS + `_sinal` (+1 MOV/FOR, -1 EXC), todas as linhas
        de todos os releases empilhadas.
    """
    frames = []
    for comp in releases:
        for tipo in ("MOV", "FOR", "EXC"):
            frames.append(_ler_arquivo(comp, tipo))
    return pd.concat(frames, ignore_index=True)


def agregar_por_corte(df: pd.DataFrame, corte_col: str) -> pd.DataFrame:
    """Agrega saldo/admissões/desligamentos por (competência de movimentação, corte).

    Args:
        df: retorno de `carregar_releases`, com uma coluna de corte adicional
            já pronta (`seção`, `uf`, ou uma coluna `categoria` derivada de
            `salário`, ver mt_caged_salario.py).
        corte_col: nome da coluna de corte em `df`.

    Returns:
        DataFrame tidy: date, categoria, metrica (saldo|admissoes|desligamentos), value.
    """
    valor_assinado = df["saldomovimentação"] * df["_sinal"]
    admissoes = valor_assinado.where(df["saldomovimentação"] > 0, 0.0)
    desligamentos = (-valor_assinado).where(df["saldomovimentação"] < 0, 0.0)

    chave = [df["competênciamov"], df[corte_col]]
    partes = {
        "saldo": valor_assinado.groupby(chave).sum(),
        "admissoes": admissoes.groupby(chave).sum(),
        "desligamentos": desligamentos.groupby(chave).sum(),
    }

    out = []
    for metrica, serie in partes.items():
        s = serie.reset_index()
        s.columns = ["competencia", "categoria", "value"]
        s["metrica"] = metrica
        out.append(s)

    resultado = pd.concat(out, ignore_index=True)
    resultado["date"] = pd.to_datetime(resultado["competencia"].astype(str), format="%Y%m")
    return resultado[["date", "categoria", "metrica", "value"]]
