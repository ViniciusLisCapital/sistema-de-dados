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
`expc_focus.run()` usa `start=` ISO (`"YYYY-MM-DD"`) ou `n_dias=` para janela retroativa.
