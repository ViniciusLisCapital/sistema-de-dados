"""
Cliente para a API publica do Comex Stat (MDIC) — comercio exterior brasileiro.

https://api-comexstat.mdic.gov.br — sem autenticacao, mas com rate limit
agressivo (HTTP 429 apos poucas chamadas rapidas em sequencia, confirmado
empiricamente) — por isso todo metodo usa retry com backoff exponencial.

Cobertura: 1997-01 -> presente (mensal), atualizado ~3 dias apos o
fechamento do mes (mais rapido que o Balanco de Pagamentos do BCB). Valores
em USD FOB.

IMPORTANTE — nao e' BPM6: Comex Stat/SECEX usa metodologia de "comercio
geral" (registro aduaneiro, SISCOMEX). O BCB aplica ajustes documentados
(bens para transformacao que cruzam fronteira sem mudanca de propriedade,
bens que mudam de propriedade sem cruzar fronteira, etc) para chegar da
base Comex Stat/SECEX ate a serie `mercadorias_gerais` de
`macro_brasil.cmb_balanco_pagmt`. Os totais desta fonte NAO devem ser
somados/comparados linha a linha com os da BOP como se fossem identicos —
sao um recorte complementar (quebra por pais/bloco), nao uma reconciliacao.

A API tambem tem uma quebra por categoria de produto (NCM/SH/CUCI/ISIC/CGCE),
mas a classica "Fator Agregado" (Basicos/Semimanufaturados/Manufaturados) so
existe no arquivo de correlacao NCM.csv do download em massa
(balanca.economia.gov.br) — nao esta disponivel como filtro/detail da API.

Exemplo de uso:

    from connectors.comexstat import ComexStat

    cs = ComexStat()
    df = cs.get_trade("export", "1997-01", "2026-06", country_code="160")  # China
    df_total = cs.get_trade("export", "1997-01", "2026-06")  # mundo (sem filtro)
"""

from __future__ import annotations

import time

import pandas as pd
import requests

_BASE = "https://api-comexstat.mdic.gov.br"


class ComexStat:
    """Cliente minimo para o endpoint POST /general do Comex Stat.

    Rate limit confirmado empiricamente: ~5 chamadas rapidas em sequencia
    bastam para levar um 429 ("tente novamente em 10 segundos"). Por isso
    todo request espera `_min_interval` desde o request anterior (throttle
    proativo) ALEM do backoff reativo em cima de 429 — sem isso, um backfill
    de varios anos/paises (get_trade faz 1 chamada por ano internamente)
    fica preso em ciclos de retry.
    """

    def __init__(self, *, timeout: float = 30.0, min_interval: float = 2.0):
        self.timeout = timeout
        self._min_interval = min_interval
        self._last_request_at = 0.0
        self._session = requests.Session()

    def _post(self, path: str, payload: dict, max_retries: int = 10) -> dict:
        url = f"{_BASE}{path}"
        backoff = 11.0  # a API sugere "tente novamente em 10 segundos" — 11s de margem
        for _ in range(max_retries):
            elapsed = time.monotonic() - self._last_request_at
            if elapsed < self._min_interval:
                time.sleep(self._min_interval - elapsed)
            resp = self._session.post(url, json=payload, timeout=self.timeout)
            self._last_request_at = time.monotonic()
            if resp.status_code == 429:
                time.sleep(backoff)
                backoff = min(backoff * 1.5, 60.0)
                continue
            resp.raise_for_status()
            return resp.json()
        raise RuntimeError(f"Comex Stat: rate limited apos {max_retries} tentativas ({url})")

    def get_trade(
        self,
        flow: str,
        start: str,
        end: str,
        country_code: str | None = None,
    ) -> pd.DataFrame:
        """Serie mensal de valor FOB (USD) por fluxo, com filtro opcional de pais.

        Args:
            flow: "export" ou "import".
            start, end: "YYYY-MM".
            country_code: codigo Comex Stat do pais (ex: "160" China,
                          "249" Estados Unidos, "063" Argentina,
                          "023" Alemanha — ver /tables/countries para outros).
                          None retorna o total mundial (sem filtro/agrupamento).

        Returns:
            DataFrame tidy com colunas date (Timestamp), value (float, USD FOB).

        Gotcha confirmado empiricamente (2026-07): quando `start`/`end` cobrem
        mais de um ano, a API NAO trata `period.from`/`period.to` como uma
        janela continua — ela aplica o INTERVALO DE MESES (from ate to) em
        TODO ANO entre os dois anos. Ex: from="1997-01" to="2026-06" nao
        retorna 1997-01 -> 2026-06 continuo; retorna jan-jun de CADA ano
        entre 1997 e 2026 (confirmado: 180 linhas = 30 anos x 6 meses, nao os
        ~354 meses esperados). Um range que cruza anos com mes(from) >
        mes(to) (ex: 1997-07 -> 1998-02) retorna lista vazia, sem erro —
        silenciosamente incorreto, nao um 4xx. Por isso este metodo faz UMA
        chamada POR ANO internamente (from/to sempre dentro do mesmo ano
        civil) e concatena — a unica forma confirmada de obter historico
        continuo correto.
        """
        start_year, start_month = int(start[:4]), start[5:7]
        end_year, end_month = int(end[:4]), end[5:7]

        frames = []
        for year in range(start_year, end_year + 1):
            year_from = f"{year}-{start_month}" if year == start_year else f"{year}-01"
            year_to   = f"{year}-{end_month}"   if year == end_year   else f"{year}-12"
            payload = {
                "flow": flow,
                "monthDetail": True,
                "period": {"from": year_from, "to": year_to},
                "filters": [{"filter": "country", "values": [country_code]}] if country_code else [],
                "details": [],
                "metrics": ["metricFOB"],
            }
            data = self._post("/general", payload)
            rows = data["data"]["list"]
            if rows:
                frames.append(pd.DataFrame(rows))

        if not frames:
            return pd.DataFrame(columns=["date", "value"])
        df = pd.concat(frames, ignore_index=True)
        df["date"] = pd.to_datetime(df["year"] + "-" + df["monthNumber"] + "-01")
        df["value"] = df["metricFOB"].astype(float)
        return df[["date", "value"]].sort_values("date").reset_index(drop=True)
