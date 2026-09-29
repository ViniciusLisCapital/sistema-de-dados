"""
Connector para os **resultados quantitativos agregados do Questionario Pre-Copom (QPC)**
do BCB -- a planilha xlsx que o Depec publica depois de cada reuniao.

O QPC e enviado as instituicoes do Focus antes de cada reuniao e as respostas sao
insumo do Copom. Desde a 238a reuniao (mai/2021) o BCB publica as estatisticas
agregadas das respostas NUMERICAS, no dia seguinte a ata. As respostas em texto
(questao 2, sobre a comunicacao do Copom; os "por que?"; a descricao dos riscos)
nao sao publicadas. Como no anexo do RPM, a unidade aqui e uma EDICAO, nao uma serie.

Fonte:
    https://www.bcb.gov.br/conteudo/relinvest/PrCopom/<AAAA>_<MM>_Copom<NNN>_QPC_SumarioQuantitativo.xlsx
O formulario em branco da mesma edicao fica ao lado, em `QPC<NNN>.pdf`.

## O mes do nome do arquivo nao e confiavel

`AAAA_MM` costuma ser o mes da ata, mas nem sempre: a 249a (decisao em set/2022)
saiu como `2022_06` e a 248a (ago/2022) como `2022_08`. Nao ha listagem de diretorio
e a pagina do QPC e SPA sem rota `api/servico/sitebcb` propria (testado em
2026-09-29: `qpc`, `questionarioprecopom`, `prcopom` respondem "Requisicao invalida").
Entao `localizar()` testa primeiro o mes da reuniao e o seguinte, e depois varre
os 36 meses do ano anterior ao seguinte. Custa 2 requisicoes no caso normal.

A existencia e testada com GET de 2 bytes (`Range: bytes=0-1`), a mesma escolha do
`connectors/bcb_rpm.py`: nem todo caminho do CDN do BCB responde a HEAD.

## Cobertura (medida em 2026-09-29)

43 edicoes, 238 a 281. A 239a (jun/2021) nao responde em nenhum mes de 2020-2022.

Exemplo:

    from connectors.bcb_qpc import QPC

    qpc = QPC()
    url = qpc.localizar(281, dt.date(2026, 9, 16))
    wb = qpc.abrir(url)                      # openpyxl, data_only
    qpc.publicado_em(wb)                     # date(2026, 9, 23)
"""

from __future__ import annotations

import datetime as dt
import io
import re
import time

import openpyxl
import requests

_BASE_URL = "https://www.bcb.gov.br/conteudo/relinvest/PrCopom"
_UA = "Mozilla/5.0 (LIS Capital sistema de dados)"
PRIMEIRA_EDICAO = 238

_MESES_PT = {
    "janeiro": 1, "fevereiro": 2, "marco": 3, "março": 3, "abril": 4, "maio": 5, "junho": 6,
    "julho": 7, "agosto": 8, "setembro": 9, "outubro": 10, "novembro": 11, "dezembro": 12,
}


def url_de(nro_reuniao: int, ano: int, mes: int) -> str:
    return f"{_BASE_URL}/{ano}_{mes:02d}_Copom{nro_reuniao}_QPC_SumarioQuantitativo.xlsx"


def _mes_mais(ano: int, mes: int, k: int) -> tuple[int, int]:
    i = ano * 12 + (mes - 1) + k
    return i // 12, i % 12 + 1


class QPC:
    def __init__(self, timeout: int = 30, tentativas: int = 3):
        self.timeout = timeout
        self.tentativas = tentativas
        self.sessao = requests.Session()
        self.sessao.headers["User-Agent"] = _UA

    def _existe(self, url: str) -> bool:
        for k in range(self.tentativas):
            try:
                r = self.sessao.get(url, headers={"Range": "bytes=0-1"}, timeout=self.timeout)
                return r.status_code in (200, 206)
            except requests.RequestException:
                if k == self.tentativas - 1:
                    raise
                time.sleep(2 * (k + 1))
        return False

    def localizar(self, nro_reuniao: int, data_reuniao: dt.date) -> str | None:
        """URL do resultado da edicao, ou None se nao houver arquivo publicado."""
        a, m = data_reuniao.year, data_reuniao.month
        provaveis = [(a, m), _mes_mais(a, m, 1)]
        resto = [(y, mm) for y in (a - 1, a, a + 1) for mm in range(1, 13)
                 if (y, mm) not in provaveis]
        for ano, mes in provaveis + resto:
            url = url_de(nro_reuniao, ano, mes)
            if self._existe(url):
                return url
        return None

    def baixar(self, url: str) -> bytes:
        erro: Exception | None = None
        for k in range(self.tentativas):
            try:
                r = self.sessao.get(url, timeout=self.timeout)
                r.raise_for_status()
                return r.content
            except requests.RequestException as e:
                erro = e
                time.sleep(2 * (k + 1))
        raise RuntimeError(f"falhou em {self.tentativas} tentativas: {url} ({erro})")

    def abrir(self, url: str) -> openpyxl.Workbook:
        # Sem read_only: as abas sao pequenas e o modo read-only do openpyxl devolve
        # dimensoes erradas em algumas delas.
        return openpyxl.load_workbook(io.BytesIO(self.baixar(url)), data_only=True)

    @staticmethod
    def publicado_em(wb: openpyxl.Workbook) -> dt.date:
        """A data da aba 'Capa' ("Publicado em 23 de setembro de 2026")."""
        for ws in wb.worksheets[:2]:
            for row in ws.iter_rows(values_only=True):
                for v in row:
                    m = re.search(r"Publicado em (\d{1,2}) de (\w+) de (\d{4})", str(v or ""))
                    if m:
                        return dt.date(int(m.group(3)), _MESES_PT[m.group(2).lower()],
                                       int(m.group(1)))
        raise ValueError("data de publicacao nao encontrada na capa")
