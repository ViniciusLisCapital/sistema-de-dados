# connectors/ — Contexto para o Claude

Clientes de APIs externas usados pelos scripts de domínio (`domain/db/`). Cada connector é paramétrico — não tem lógica de negócio, só chamada de API + parsing.

### `connectors/ibge.py` — API de Agregados IBGE v3

Cliente paramétrico baseado em `view=flat`. Substituiu o antigo `ibge_get(url, start, end, freq)`.

```python
from connectors.ibge import IBGE

ibge = IBGE()
df = ibge.get(
    agregado=8888,
    variaveis=12606,
    classificacoes={544: "all"},
    localidades={"N1": "all"},
    periodos="last:24",    # ou "202401-202412", "all", (2024, 2024)
)
# date: Timestamp, value: float64, sentinels -> NaN
```

**Detalhes técnicos da API IBGE v3:**
- `periodos`: aceita `YYYYMM-YYYYMM`, `last:N`, `-N`, `all`. A tupla `(ano_ini, ano_fim)` usa metadados para inferir o sufixo correto.
- `view=flat`: primeiro item do array é sempre o cabeçalho — `_parse_flat` pula automaticamente.
- Frequência inferida do cabeçalho `D2N` (`"Mês"`, `"Trimestre"`, `"Trimestre Móvel"`, `"Semestre"`, `"Ano"`).
- `"trimestral móvel"` (PNAD) é mapeado para formato `YYYYMM` igual ao mensal.
- Retry: 6 tentativas, backoff 1s, respeita `Retry-After`.

### `connectors/bcb.py` — APIs SGS e Focus do BCB

```python
from connectors.bcb import BCB

bcb = BCB()

# SGS: últimos N meses
df = bcb.get_sgs_ultimos({"ibcbr_nsa": 24363, "ibcbr_sa": 24364}, n=36)

# SGS: por período ou histórico completo
df = bcb.get_sgs(series, start="01/01/2020")
df = bcb.get_sgs(series, start="all")   # série histórica completa desde o início

# Focus/Olinda
df = bcb.get_focus(
    endpoint="ExpectativasMercadoInflacao12Meses",
    indicador="IPCA",
    campos=["Data", "Media", "Mediana", "DesvioPadrao"],
    start="2020-01-01",
    filtros_extras="Suavizada eq 'S' and baseCalculo eq 0",
)
# colunas em snake_case, date como Timestamp
```

**Detalhes técnicos:**
- SGS: `/ultimos/{n}` tem limite ~24 — `get_sgs_ultimos` usa `/dados?dataInicial=...` calculando a data.
- SGS `start="all"` mapeia para `"01/01/1970"` internamente; a API retorna desde o início real da série.
- Focus: URL deve ter `$` literal — `requests(params={})` percent-encoda para `%24` e a API rejeita. URL é construída manualmente.
- `$count` não suportado pelo endpoint Focus do BCB — paginação por `$skip` até `len(page) < page_size`.
- `ExpectativasMercadoSelic` não tem campo `Suavizada` — filtro diferente de inflação.
- Paralelismo: `ThreadPoolExecutor` para múltiplas séries SGS simultâneas.

### `connectors/fred.py` — API FRED (Federal Reserve)

```python
from connectors.fred import FredUniFrame, FredMultFrame

# Série única
df = FredUniFrame("PCE", "PCEPI", "2010-01-01", "2024-12-31")
# colunas: Date, <NameSerie>

# Múltiplas séries (wide ou unpivoted)
df = FredMultFrame({"PCE": "PCEPI", "CPI": "CPIAUCSL"}, "2010-01-01", "2024-12-31")
df_long = FredMultFrame({...}, start, end, Pivot=True)
```

**Detalhes:**
- API key via `FRED_API_KEY` no `.env` — nunca hardcoded.
- `US_IndexNormalize`: expande dados trimestrais para mensais via merge com CPI e `ffill(limit=2)`.

### `connectors/bis.py` — BIS Statistics API v1

Sem autenticação. Três datasets SDMX-CSV expostos:

```python
from connectors.bis import BIS

bis = BIS()

# WS_EER — Effective Exchange Rates (REER/NEER)
df = bis.get_eer(countries=["BR", "MX", "CL", "CO"], types=[("R", "B"), ("N", "B")])
# colunas: date (month-start), country_code, reer_type (real_broad | nominal_broad | ...), value

# WS_CBPOL — Central Bank Policy Rates
df = bis.get_policy_rates(countries=["BR", "MX", "CL", "CO", "PE", "AR"], freq="D")
# colunas: date, country_code, value (% a.a.)

# WS_LONG_CPI — Consumer Prices (série longa)
df = bis.get_cpi(countries=["BR", "MX", "CL", "CO", "PE"], unit="yoy")
# colunas: date (month-start), country_code, value (% a.a., YoY)
```

**Detalhes técnicos:**
- Key SDMX difere por dataset: `WS_EER` é `FREQ.ADJUSTMENT.REF_AREA.BASKET` (4 dimensões); `WS_CBPOL` é
  `FREQ.REF_AREA` (2 dimensões); `WS_LONG_CPI` é `FREQ.REF_AREA.UNIT_MEASURE` (3 dimensões, `UNIT_MEASURE`
  `771`=YoY % ou `628`=índice 2010=100 — `get_cpi(unit=...)` aceita `"yoy"`/`"index"` ou o código direto).
- `WS_CBPOL` também expõe frequência mensal, mas é só o fechamento de mês da série diária — por isso a
  maioria dos scripts de domínio usa `freq="D"`; `cmb_real_rates.py` é a exceção, usa `freq="M"` para
  alinhar com o CPI (também mensal).
- Cuidado com o range de valores: Brasil na hiperinflação (1989-1994) chega a ~790.799% a.a. — coluna
  `value` no banco precisa de `decimal(12,4)`, não `decimal(8,4)`, em qualquer tabela que use `WS_CBPOL`
  sem truncar esse período.
- Argentina (`AR`) parou de ser atualizada pelo BIS em 2025-07 — gap esperado no fim da série, não é
  falha do connector/script. `WS_LONG_CPI` não cobre AR nos países acompanhados aqui (não testado).
- `WS_LONG_CPI` é live/atualizado mensalmente (cobre até o mês corrente, checado em 2026-08) — ao
  contrário do CPI de MX/CL/CO exposto no FRED (fonte OECD, descontinuado lá em 2023-2024) e de PE
  (sem série mensal alguma no FRED). Preferir `WS_LONG_CPI` a FRED para CPI desses 4 países.
- Retry: 4 tentativas, backoff 1s, respeita `Retry-After` (429/5xx).

### `connectors/yfinance.py` — Yahoo Finance (via pacote `yfinance`)

```python
from connectors.yfinance import get_history

df = get_history("DX-Y.NYB", start="1971-01-01")
# colunas: date, value (value = Close)
```

**Detalhes:**
- Usado por `domain/db/international/yfinance/cmb_dollar_index.py` (DXY) — historico desde 1971,
  bem mais longo que o equivalente FRED (`DTWEXBGS`, so cobre a partir de 2006).
- `end=None` (default) baixa ate a data atual.
- `yf.download` retorna colunas em MultiIndex (`Price`, `Ticker`) — `get_history` ja acha e renomeia.

### `connectors/mysql.py` — Insert/Update no banco

```python
from connectors.mysql import insert_data_into_database

insert_data_into_database("macro_brasil", "atv_pim", df)
```

Faz `SHOW COLUMNS FROM table`, reordena o df, e executa `INSERT ... ON DUPLICATE KEY UPDATE` em batches de 1000 linhas.

**Bug corrigido:** `.where(pd.notna(df), None)` não convertia NaN em float64 para None — `executemany` enviava `float('nan')` como string `'nan'` ao MySQL. Fix: `df.astype(object).where(...)`.
