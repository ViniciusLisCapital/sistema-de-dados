"""
Lógica compartilhada de download+combinação+agregação do Novo CAGED (FTP do
PDET/MTE) -- usada por mt_caged.py (o orquestrador, que alimenta as 3 tabelas
de corte num único passe de download).

Fonte: ftp://ftp.mtps.gov.br/pdet/microdados/NOVO CAGED/<AAAA>/<AAAAMM>/
Ver connectors/pdet_ftp.py para o cliente FTP (encoding Latin-1).

## Fórmula de saldo por competência de MOVIMENTAÇÃO (validada ao vivo, 2026-08)

    saldo(X)         = MOV(X) + FOR(X) - EXC(X)
    admissões(X)      = Σ (+1) de MOV+FOR  -  Σ (+1) de EXC
    desligamentos(X)  = Σ (-1) de MOV+FOR  -  Σ (-1) de EXC   [em valor absoluto]

`saldomovimentação` é sempre ±1 por linha (admissão=+1, desligamento=-1).
Confirmado inspecionando linhas reais de CAGEDEXC202401.txt: uma exclusão de
desligamento (tipomovimentação=40) aparece com saldomovimentação=-1 -- ou seja,
EXC guarda o SINAL ORIGINAL do registro sendo cancelado, não pré-invertido.
Por isso a fórmula SUBTRAI o EXC em vez de somar.

Validação ao vivo (2026-08): competência 2026-06 fechou em saldo=145.161,
admissões=2.220.131, desligamentos=2.074.970 -- o saldo bate exatamente com o
número apurado independentemente na investigação anterior (ver HANDOVER.md).

## Por que "competência do arquivo" != "competência de movimentação"

Cada arquivo pertence a uma competência de RELEASE. Confirmado ao vivo:
  - CAGEDMOV<AAAAMM>: TODA linha tem competênciamov==AAAAMM -- arquivo fixo,
    nunca revisado depois de publicado. Baixado UMA vez, no seu próprio release.
  - CAGEDFOR/CAGEDEXC<AAAAMM>: contêm linhas com competênciamov de QUALQUER mês
    anterior (o FOR de 2024-01 corrigiu competências espalhadas por 2023 inteiro).

Ou seja, o saldo de uma competência X só fica completo depois que todos os
releases seguintes publicaram seus FOR/EXC -- a "reescrita histórica
silenciosa" do HANDOVER.md. Declaração fora do prazo é aceita por até ~12
meses, então uma competência estabiliza ~1 ano depois de publicada.

## Consequência para atualização incremental (importante para corretude)

Como as contribuições a uma competência X estão espalhadas por vários releases,
somar apenas os releases de uma janela recente daria um valor PARCIAL de X --
que, gravado com `ON DUPLICATE KEY UPDATE`, sobrescreveria o valor completo já
no banco. Para evitar isso, `processar` só devolve as competências X cujo
CAGEDMOV está DENTRO da janela processada: para essas, a janela contém o MOV(X)
original e todos os FOR/EXC publicados desde então, ou seja o valor completo
disponível hoje. Competências anteriores à janela recebem correções apenas na
próxima reconstrução completa (`start="all"`). Isso mantém a operação idempotente
-- rodar duas vezes dá o mesmo resultado, nunca duplica.
"""

import shutil
import tempfile

import pandas as pd

from connectors.pdet_ftp import (
    baixar_7z,
    extrair_csv,
    listar_anos,
    listar_arquivos,
    listar_competencias,
)

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


def _normalizar_salario(serie: pd.Series) -> pd.Series:
    """Converte a coluna `salário` para float aceitando as duas convenções da fonte.

    O separador decimal NÃO é consistente entre releases: a maioria usa vírgula
    ("4800,00"), mas os arquivos de 2023-08 e 2023-09 usam ponto ("2333.8").
    Confirmado ao vivo inspecionando o texto cru dos dois formatos. Por isso a
    coluna é lida como texto e normalizada aqui, em vez de confiar num
    `decimal=` fixo no `read_csv` (que deixava a coluna como object no formato
    inesperado e estourava TypeError na primeira divisão).

    Regra: se há vírgula, ela é o decimal e o ponto é separador de milhar;
    se não há, o ponto é o decimal.
    """
    texto = serie.astype("string").str.strip()
    com_virgula = texto.str.contains(",", na=False)
    texto = texto.mask(
        com_virgula,
        texto.str.replace(".", "", regex=False).str.replace(",", ".", regex=False),
    )
    return pd.to_numeric(texto, errors="coerce")


def _ler_arquivo(competencia: str, tipo: str) -> pd.DataFrame:
    nome_interno = f"CAGED{tipo}{competencia}.txt"
    conteudo = baixar_7z(competencia, tipo)
    tmp = tempfile.mkdtemp(prefix="caged_")
    try:
        path = extrair_csv(conteudo, nome_interno, tmp)
        df = pd.read_csv(
            path, sep=";", encoding="utf-8", usecols=_COLS, dtype={"salário": "string"}
        )
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    df["salário"] = _normalizar_salario(df["salário"])
    df["_sinal"] = 1 if tipo in ("MOV", "FOR") else -1
    return df


def _agregar(df: pd.DataFrame, corte_col: str) -> pd.DataFrame:
    """Agrega saldo/admissões/desligamentos por (competência de movimentação, corte)."""
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
    return pd.concat(out, ignore_index=True)


def _agregar_cortes(df: pd.DataFrame, cortes: dict) -> dict:
    out = {}
    for nome, fn in cortes.items():
        df["_categoria"] = fn(df)
        out[nome] = _agregar(df, "_categoria")
    return out


def processar(releases: list[str], cortes: dict):
    """Gera o resultado de cada competência, uma por vez, num único download.

    Duas fases, para gravar progresso de forma incremental sem sacrificar
    corretude:
      1. Lê os FOR/EXC de TODOS os releases da janela (arquivos pequenos,
         ~0,6MB cada) e acumula as correções agregadas por competência de
         movimentação.
      2. Lê o CAGEDMOV de cada release (o arquivo grande, ~50MB) um a um.
         Como MOV<X> contém exclusivamente a competência X, somar as correções
         já coletadas na fase 1 fecha o valor completo de X naquele momento --
         então cada competência pode ser gravada assim que processada, em vez
         de esperar o fim da varredura inteira.

    Descarta o microdado bruto antes do próximo release (padrão
    "agregar-e-descartar") -- nunca persiste o bruto, nunca carrega mais de uma
    competência na memória de uma vez.

    Args:
        releases: competências de release a processar (de `resolver_releases`).
        cortes:   {nome_do_corte: função(df) -> pd.Series de categorias}.

    Yields:
        (competencia, {nome_do_corte: DataFrame tidy (date, categoria, metrica, value)})
        para cada competência da janela, na ordem.
    """
    correcoes = {nome: [] for nome in cortes}
    for comp in releases:
        presentes = listar_arquivos(comp)
        for tipo in ("FOR", "EXC"):
            if f"CAGED{tipo}{comp}.7z" not in presentes:
                continue
            df = _ler_arquivo(comp, tipo)
            for nome, agregado in _agregar_cortes(df, cortes).items():
                correcoes[nome].append(agregado)
            del df
    print(f"  correções (FOR/EXC) de {len(releases)} release(s) lidas")

    correcoes = {
        nome: (
            pd.concat(frames, ignore_index=True)
            if frames
            else pd.DataFrame(columns=["competencia", "categoria", "value", "metrica"])
        )
        for nome, frames in correcoes.items()
    }

    for comp in releases:
        mov = _ler_arquivo(comp, "MOV")
        agregados = _agregar_cortes(mov, cortes)
        del mov

        resultado = {}
        for nome, base in agregados.items():
            corr = correcoes[nome]
            corr = corr[corr["competencia"] == int(comp)]
            df = pd.concat([base, corr], ignore_index=True)
            df = df.groupby(["competencia", "categoria", "metrica"], as_index=False)["value"].sum()
            df["date"] = pd.to_datetime(df["competencia"].astype(str), format="%Y%m")
            resultado[nome] = df[["date", "categoria", "metrica", "value"]]

        print(f"  competência {comp} processada")
        yield comp, resultado
