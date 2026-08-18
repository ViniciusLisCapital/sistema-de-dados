"""
Connector para as "Tabelas especiais" de estatisticas fiscais do BCB -- planilhas
xlsx publicadas fora do SGS, com detalhamento que as series do SGS nao expoem.

Diferente de connectors/bcb.py (SGS/Focus, APIs JSON): aqui a fonte e um arquivo
Excel numa pasta de conteudo estatico do site do BCB. O nome do arquivo e FIXO --
o BCB sobrescreve o mesmo arquivo a cada divulgacao mensal (mesmo padrao da pagina
fixa da EFGG em connectors/tesouro_efgg.py, mas sem `id` variavel para resolver,
entao nao precisa parse de HTML: a URL e montada direto do nome do arquivo).

Sem autenticacao. Confirmado ao vivo (2026-08) que a pasta responde 200 para
nome valido e 404 para nome inexistente -- nao ha listagem de diretorio, entao
um nome novo precisa ser descoberto por tentativa direta (a pagina de
Estatisticas Fiscais e SPA Angular: `requests`/WebFetch trazem so o shell, sem
os links).

**Inventario dos arquivos desta pasta** -- conteudo, abas e quais nomes retornam
404 -- vive em `analytics/fiscal_policy/fontes_dados.md` (secao das Tabelas
Especiais do BCB), nao duplicado aqui: e um mapa de fontes fiscais, mantido do
lado de quem escolhe o que ingerir.

Exemplo de uso:

    from connectors.bcb_tabelas_especiais import TabelasEspeciais

    te = TabelasEspeciais()
    sheets = te.read_sheets("Facdetp.xlsx")           # todas as abas, header=None
    sheets = te.read_sheets("Facdetp.xlsx", ["Juros"])  # so uma aba
"""

from __future__ import annotations

import io

import pandas as pd
import requests

_BASE_URL = "https://www.bcb.gov.br/content/estatisticas/Documents/Tabelas_especiais"

# So o que este projeto ja consome, para servir de referencia de nome exato na
# mensagem de erro do 404. O inventario completo da pasta esta em
# analytics/fiscal_policy/fontes_dados.md (ver docstring do modulo).
KNOWN_FILES = {
    "Facdetp.xlsx": (
        "Fatores condicionantes da divida liquida do setor publico (DLSP) -- "
        "detalhamento por item, mensal, R$ milhoes. 9 abas: Estoques + 8 fatores "
        "de fluxo. Ver domain/db/brasil/bcb/fisc_dlsp_fatores.py."
    ),
}


class TabelasEspeciais:
    """Cliente para as planilhas de tabelas especiais de estatisticas fiscais do BCB."""

    def __init__(self, *, timeout: float = 120.0):
        self.timeout = timeout
        self._session = requests.Session()
        self._session.headers.update({"User-Agent": "Mozilla/5.0"})

    def url_for(self, filename: str) -> str:
        return f"{_BASE_URL}/{filename}"

    def download(self, filename: str) -> bytes:
        """Baixa o arquivo cru. Levanta se o nome nao existir (404) na pasta."""
        url = self.url_for(filename)
        resp = self._session.get(url, timeout=self.timeout)
        if resp.status_code == 404:
            raise RuntimeError(
                f"'{filename}' nao encontrado em {_BASE_URL} (404) -- o BCB pode ter "
                f"renomeado ou movido o arquivo. Nomes ja confirmados: {sorted(KNOWN_FILES)}."
            )
        resp.raise_for_status()
        return resp.content

    def read_sheets(
        self, filename: str, sheet_names: list[str] | None = None
    ) -> dict[str, pd.DataFrame]:
        """Baixa e le abas como DataFrames crus (header=None).

        Args:
            filename: nome exato do arquivo, ex: "Facdetp.xlsx".
            sheet_names: abas a ler; None le todas.

        Returns:
            {nome_da_aba: DataFrame}, todos com header=None (colunas 0, 1, 2, ...
            na ordem crua do Excel) -- o parsing de cabecalho/hierarquia fica no
            script de dominio, mesmo padrao de connectors/tesouro_efgg.py.
        """
        content = self.download(filename)
        sheet = sheet_names if sheet_names is not None else None
        raw = pd.read_excel(io.BytesIO(content), sheet_name=sheet, header=None)
        return raw if isinstance(raw, dict) else {sheet_names[0]: raw}
