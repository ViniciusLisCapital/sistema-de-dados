"""
Connector para a EFGG (Estatisticas Fiscais do Governo Geral), Secretaria do
Tesouro Nacional -- classificacao economica GFSM 2014 do FMI (Remuneracao de
empregados, Transferencias, Investimento liquido em ativos nao financeiros
etc.), publicada separadamente por esfera de governo (Governo Central,
Estados, Municipios).

Publicacao trimestral, HTML puro (Plone -- nao e SPA, confirmado ao vivo com
requests simples, sem headless browser). A pagina e um link fixo cujo
conteudo e sobrescrito a cada trimestre (mesmo padrao das "tabelas especiais"
do BCB) -- ver analytics/brasil/fiscal_policy/reference/rtn_vs_efgg.md para o achado
completo, incluindo a validacao de que Central+Estados+Municipios somam
exatamente ao arquivo consolidado de Governo Geral.

Os 4 anexos xlsx tem id numerico (`thot-arquivos.tesouro.gov.br/publicacao-
anexo/{id}`) que muda a cada publicacao -- por isso resolvido a cada chamada
via parse do HTML, nunca hardcoded. Sem autenticacao.

Exemplo de uso:

    from connectors.tesouro_efgg import EFGG

    efgg = EFGG()
    urls = efgg.get_current_urls()
    raw = efgg.download_table(urls["estados"], sheet_name="1.3")
"""

from __future__ import annotations

import io

import pandas as pd
import requests
from bs4 import BeautifulSoup

_PAGE_URL = "https://www.tesourotransparente.gov.br/publicacoes/estatisticas-fiscais-do-governo-geral/2021/22"

_ANNEX_FILENAMES = {
    "central": "demonstrativos_governo_central_orcamentario.xlsx",
    "estados": "demonstrativos_governos_estaduais.xlsx",
    "municipios": "demonstrativos_governos_municipais.xlsx",
    "investimento_geral": "demonstrativos_investimento_governo_geral.xlsx",
}


class EFGG:
    """Connector para os anexos xlsx da publicacao trimestral EFGG."""

    def __init__(self, *, timeout: float = 60.0):
        self.timeout = timeout
        self._session = requests.Session()
        self._session.headers.update({"User-Agent": "Mozilla/5.0"})

    def get_current_urls(self) -> dict[str, str]:
        """Resolve as URLs de download vigentes dos 4 anexos xlsx.

        Le a pagina fixa (`_PAGE_URL`), que a Tesouro Transparente sobrescreve
        a cada nova publicacao trimestral -- o `id` numerico de cada anexo
        muda a cada vez, entao precisa ser lido de novo em toda chamada.
        """
        resp = self._session.get(_PAGE_URL, timeout=self.timeout)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        urls = {}
        for key, filename in _ANNEX_FILENAMES.items():
            link = soup.find("a", title=filename)
            if link is None or not link.get("href"):
                raise RuntimeError(
                    f"Anexo '{filename}' nao encontrado na pagina da EFGG "
                    f"({_PAGE_URL}) -- layout pode ter mudado."
                )
            urls[key] = link["href"]
        return urls

    def download_table(self, url: str, sheet_name: str) -> pd.DataFrame:
        """Baixa um anexo e retorna uma aba crua (sem header), pronta para parsing por codigo.

        Args:
            url: uma das URLs retornadas por get_current_urls().
            sheet_name: nome da aba, ex: "1.3" (Despesa Trimestral em
                Estados/Municipios) ou "2.3" (Despesa Trimestral no Governo
                Central -- numeracao de aba difere por esfera, ver
                domain/db/brasil/tesouro/fisc_efgg.py).

        Returns:
            DataFrame com header=None (colunas 0, 1, 2, ... na ordem crua do
            Excel) -- quem chama e responsavel por localizar a linha de
            cabecalho e as linhas de codigo, igual ao padrao ja usado em
            connectors/tesouro.py.
        """
        resp = self._session.get(url, timeout=self.timeout)
        resp.raise_for_status()
        return pd.read_excel(io.BytesIO(resp.content), sheet_name=sheet_name, header=None)
