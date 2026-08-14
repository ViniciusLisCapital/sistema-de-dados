"""
Cliente FTP do PDET/MTE -- microdados não-identificados do Novo CAGED.

ftp://ftp.mtps.gov.br/pdet/microdados/NOVO CAGED/<AAAA>/<AAAAMM>/CAGED{MOV,FOR,EXC}<AAAAMM>.7z

Login anônimo, sem TLS ("Microsoft FTP Service"/IIS). Cada competência de
publicação tem 3 arquivos .7z:
  CAGEDMOV<AAAAMM> -- movimentações declaradas no prazo, competência de
                      movimentação == AAAAMM sempre (arquivo fixo, nunca
                      revisado depois de publicado -- confirmado ao vivo).
  CAGEDFOR<AAAAMM> -- declarações fora do prazo, competência de movimentação
                      pode ser qualquer mês ANTERIOR a AAAAMM (correções
                      retroativas chegando via um release mais novo).
  CAGEDEXC<AAAAMM> -- exclusões de registros já declarados antes (idem, mês
                      de movimentação anterior a AAAAMM).
Ver domain/db/brasil/mte/_caged_core.py para a lógica de combinação
MOV+FOR-EXC por competência de movimentação (não a competência do arquivo).

Detalhe técnico: nomes de pasta/arquivo acentuados no FTP são Latin-1/cp1252,
não UTF-8 -- `ftplib.FTP(..., encoding="latin-1")` resolve isso de forma
transparente (a string Python com acento é codificada em Latin-1 na hora de
montar o comando FTP), sem precisar de percent-encoding manual. Confirmado
ao vivo: `urllib.request.urlopen("ftp://...%E3...")` NÃO funciona (a rotina
default do urllib decodifica o percent-encoding como UTF-8 antes de repassar
pro ftplib, corrompendo o byte Latin-1) -- usar sempre este módulo, não
urlopen, para qualquer caminho com acento.
"""

import io
from ftplib import FTP

import py7zr

_HOST = "ftp.mtps.gov.br"
_ROOT = "pdet/microdados/NOVO CAGED"


def _connect() -> FTP:
    ftp = FTP(_HOST, encoding="latin-1", timeout=60)
    ftp.login()
    return ftp


def listar_competencias(ano: int) -> list[str]:
    """Lista as competências (AAAAMM) publicadas para um ano."""
    ftp = _connect()
    try:
        ftp.cwd(f"{_ROOT}/{ano}")
        return sorted(ftp.nlst())
    finally:
        ftp.quit()


def listar_anos() -> list[str]:
    """Lista os anos (pastas) disponíveis na raiz do Novo CAGED."""
    ftp = _connect()
    try:
        ftp.cwd(_ROOT)
        return sorted(n for n in ftp.nlst() if n.isdigit())
    finally:
        ftp.quit()


def listar_arquivos(competencia: str) -> list[str]:
    """Lista os .7z presentes numa competência de release.

    Nem toda competência tem os 3 tipos: 2020-01 (primeiro release do Novo
    CAGED) só tem MOV -- não havia competência anterior para corrigir --, e
    2020-02/03 têm MOV+FOR mas nenhum EXC. Confirmado ao vivo.
    """
    ano = competencia[:4]
    ftp = _connect()
    try:
        ftp.cwd(f"{_ROOT}/{ano}/{competencia}")
        return sorted(ftp.nlst())
    finally:
        ftp.quit()


def baixar_7z(competencia: str, tipo: str) -> bytes:
    """Baixa o .7z de uma competência de publicação.

    Args:
        competencia: "AAAAMM" (ex: "202401") -- a competência do RELEASE,
                      não necessariamente a competência de movimentação
                      dos registros dentro do arquivo (ver docstring do módulo).
        tipo: "MOV" | "FOR" | "EXC".

    Returns:
        Conteúdo binário do .7z.
    """
    ano = competencia[:4]
    nome = f"CAGED{tipo}{competencia}.7z"
    ftp = _connect()
    buf = bytearray()
    try:
        ftp.cwd(f"{_ROOT}/{ano}/{competencia}")
        ftp.retrbinary(f"RETR {nome}", buf.extend)
    finally:
        ftp.quit()
    return bytes(buf)


def baixar_layout() -> bytes:
    """Baixa o layout_novo_caged.xlsx (dicionário de variáveis + tabelas de domínio)."""
    ftp = _connect()
    buf = bytearray()
    try:
        ftp.cwd(_ROOT)
        ftp.retrbinary(
            "RETR Layout Não-identificado Novo Caged Movimentação.xlsx", buf.extend
        )
    finally:
        ftp.quit()
    return bytes(buf)


def extrair_csv(conteudo_7z: bytes, nome_interno: str, dest_dir: str) -> str:
    """Extrai um único arquivo de dentro do .7z para `dest_dir`.

    py7zr (1.1.3) não expõe leitura pura em memória (sem tocar disco) -- só
    `extract()`/`extractall()`, que escrevem no filesystem. Chamador é
    responsável por apagar `dest_dir` depois de ler o CSV (padrão
    "agregar-e-descartar" do projeto -- nunca persistir o microdado bruto).

    Args:
        conteudo_7z: bytes do .7z (retorno de `baixar_7z`).
        nome_interno: nome do arquivo dentro do .7z (ex: "CAGEDMOV202401.txt").
        dest_dir: diretório onde extrair (deve existir).

    Returns:
        Caminho completo do CSV extraído.
    """
    with py7zr.SevenZipFile(io.BytesIO(conteudo_7z), mode="r") as z:
        z.extract(path=dest_dir, targets=[nome_interno])
    return f"{dest_dir}/{nome_interno}"
