---
paths:
  - "domain/**/*.py"
---

# Padrão dos scripts de domínio

Cada script expõe apenas `run()` — sem execução ao importar.

```python
# Carga histórica (primeira vez)
atv_pim.run(periodos="all")
atv_ibcbr.run(start="all")

# Atualização rotineira (padrão)
atv_pim.run()             # últimos N anos (default do script)
inflc_agregados.run()     # últimos N meses

# Range específico
atv_pib.run(periodos=(2015, 2024))
mt_caged.run(start="01/01/2020", end="31/12/2024")
```

Scripts IBGE usam `periodos=` (formatos do connector IBGE).
Scripts BCB SGS usam `start=`/`end=` (formato `"DD/MM/YYYY"`) ou `start="all"`.
Os 3 scripts de Focus (`expc_focus`, `expc_focus_copom`, `expc_focus_periodo`) usam
`start=`/`end=` ISO (`"YYYY-MM-DD"`), `start="all"` para a carga histórica completa, ou `n_dias=`
para a janela retroativa do default (90 dias). A carga completa de `expc_focus_periodo` são 1,28 M
linhas / ~11 min (medido) — minutos, não segundos; as outras duas são ~88 mil cada, ~2-3 min.
