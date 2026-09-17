# utils/ — funções auxiliares compartilhadas

Biblioteca, não lugar de análise nem de script que roda sozinho. Cada módulo existe porque algo
era copiado entre pastas.

| módulo | o que faz |
|---|---|
| `explore.py` | Leitura rápida do MySQL + gráfico descartável, para construir modelo. Ver abaixo |
| `analise_template.py` | Template de análise `#%%` — **para copiar**, não para rodar daqui |
| `console.py` | `stdout_utf8()`: o console do Windows abre em cp1252 e um `print` com seta (U+2192) levantava `UnicodeEncodeError` dentro do gerador |
| `transforms.py` | Conversões wide ↔ long e transformações de série |
| `extract_pdf.py` | Extração de texto via `pdfplumber` (PDFs born-digital, coluna única) |
| `split_pdf_smart.py` | Quebra de PDF grande em pedaços |
| `thermometer.py` | Auxiliares do termômetro macro (`analytics/oraculo/`) |

---

## `explore.py` — visualização durante a construção de um modelo

O caminho curto entre uma tabela do banco e um gráfico numa célula `#%%` do VS Code. **Não gera
relatório**: isso é trabalho do `generate_report.py` de cada área, sobre `analytics/report_structure/`.
O corte entre os dois é deliberado — no dia em que `plot()` receber argumento de cor, título de eixo
e fonte, o trabalho virou relatório e muda de pasta.

```python
from utils import explore as ex

ex.tables()                          # schemas
ex.tables("macro_brasil")            # tabelas + nº aproximado de linhas
ex.columns("macro_brasil", "atv_pib")

df = ex.load("macro_brasil", "atv_pib", wide=True, seasonal_adjs="Y")
ex.peek(df)                          # por série: início, fim, n, último valor
ex.plot(df, ["industria", "servicos"])

ex.q("SELECT ... JOIN ...", schema="macro_brasil", params={...})
```

**Três coisas que a `load()` resolve**, e é por elas que ela existe em vez de um
`MySQLDataRequester` direto:

- O MySQL devolve `value` como `Decimal` e `date` como `datetime.date`, ambos em coluna `object`.
  `numpy` e `statsmodels` quebram nisso — e o sintoma aparece longe da leitura, não no `SELECT`.
- A maioria das tabelas vem em formato longo (`date`/`name`/`value`) e modelo se escreve sobre o largo.
- Tabela com dimensão extra (ajuste sazonal, índice, item) traz a mesma série mais de uma vez: o
  pivot cru levanta `duplicate entries`, ou — pior — passa calado com a série errada. O rótulo da
  coluna só cresce enquanto a dimensão acrescentada **separa mais séries**, então a dimensão fixada
  por um filtro não vira sufixo e a redundante (`series_id` depois de `item_code`) também não.

`q()` existe porque o `MySQLDataRequester` só sabe `SELECT * FROM tabela` — join, filtro e agregação
passam por aqui.

### O que a `plot()` não faz

Zoom de scroll não é default do Plotly e não há config global: para ele, `ex.plot(df).show(config=ex.CONFIG)`.
Arrastar já dá pan e duplo clique reseta, que é o modelo de interação do resto do repositório
(`.claude/rules/lis-dashboards.md`).

---

## O ambiente que isso exige

`ipykernel` e `plotly` vivem no grupo `dev` do `pyproject.toml`, em **`[dependency-groups]`** — que
o `uv sync` sem flag nenhuma já instala. Enquanto o grupo morava em `[project.optional-dependencies]`
(até 2026-09-16), o `uv sync` que o `AMBIENTE.md` documenta **desinstalava** os dois em silêncio e as
células `#%%` paravam de rodar sem erro nenhum.
