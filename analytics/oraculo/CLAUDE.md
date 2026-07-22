# analytics/oraculo/ — Contexto para o Claude

Termômetro Macro: calcula "notas" (scores 1–10) para variáveis macroeconômicas de Brasil e EUA, alimentando dashboards Power BI.

### Componentes

| Módulo | Função | Output |
|---|---|---|
| `brasil/scores.py` | Notas macro Brasil (inflação, trabalho, crédito, atividade) | `brasil/base/Brasil_base.csv` |
| `us/term_us.py` | Notas macro EUA (labor, inflation, activity, financial, housing) | `us/base/US_BASE.csv` |
| `brasil/thermometer.py` | Múltiplos financeiros BRL (P/E, P/B, EV/EBITDA) | `brasil/base/Brasil_notas_preco.csv` |
| `us/thermometer.py` | Múltiplos financeiros US | `us/base/` |
| `jobs/update_oraculo.py` | Entry point: importa os módulos acima e combina em Central_base.csv | `base/Central_base.csv` |

### Fluxo de execução

```
jobs/update_oraculo.py
  scores.run()   → _load_data() lê macro_brasil → grava Brasil_base.csv → retorna DataFrame
  term_us.run()  → lê FRED/BCB → grava US_BASE.csv → retorna DataFrame
  pd.concat([db_brl, db_us]) → base/Central_base.csv
```

A lógica de scoring está em `utils/thermometer.py` (`Score`, `Score_SMC`, `Score_SA`, `Score_Diff`) e usa sigmóide normalizada para transformar qualquer série em nota 1–10.

### Padrão de `scores.py` (Brasil)

`_load_data()` centraliza todos os reads do banco e popula variáveis de módulo `_data_*`. `run()` chama `_load_data()` uma vez e concatena os frames de scoring. Colunas são renomeadas em `_load_data()` para manter os corpos das funções de scoring inalterados. Todas as séries consumidas por `_load_data()` vêm de `macro_brasil` via `MySQLDataRequester` — sem dependência direta de connectors externos (BCB, FRED etc.).

Funções de scoring em snake_case (ex: `inflacao`, `ibc_br`) — nomes de função, não as tabelas (que levam o prefixo de tema, ver `CLAUDE.md` raiz). `_finalize(*frames)` elimina boilerplate: `pd.concat([unpivot(f.tail(_N)) for f in frames]).dropna()`.

**Pendências:**
- `us/term_us.py` — revisão de qualidade: snake_case, `_load_data()` centralizado, bugs de robustez. Se os scores migrarem para MySQL no futuro, ver `domain/db/CLAUDE.md` — cenário citado lá como justificativa legítima para um schema de analytics dedicado.
- `brasil/thermometer.py` lê de `MySQLDataRequester('br_finance', 'brazil_real_yield_curve')` — verificar se schema ainda existe.
