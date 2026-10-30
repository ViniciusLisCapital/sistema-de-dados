# analytics/brasil/structural_model/experimentos/ — Contexto para o Claude

Estimações e testes que **nenhum dashboard usa**. Moraram em `analytics/brasil/monetary_policy/`
até 2026-09-24, quando aquela pasta passou a guardar só o relatório. Cada um é independente dos
outros e do Modelo Estrutural.

- **`phillips_excel.py`** — Curva de Phillips "flavored" (12m Y/Y, sem intercepto, pesos de inércia
  e expectativa somando 1) → `data/curva_phillips_auditoria.xlsx`, auditável célula a célula.
  Independente do modelo agregado. **Rodar recria a planilha e destrói abas adicionadas à mão.**

      uv run python -c "from analytics.brasil.structural_model.experimentos.phillips_excel import run; run()"

- **`teste_lstm/`** — um LSTM prevendo o IPCA 12 meses à frente contra benchmarks. Experimento, não
  produção; o [`CLAUDE.md`](teste_lstm/CLAUDE.md) de lá diz como rodar e quando apagar.
- **`tvp_2026-08-21/`** — teste de parâmetro variante no tempo para a transmissão do juro real
  (movido da raiz do projeto em 2026-08-25). **O script que o produziu não existe**; ver o README.
- **`curva_juros/`** — material legado, nunca integrado; os imports apontam para um layout de
  pacote que não existe mais.
- **`ancora_2026-10-30/`** e **`hiato_2026-10-30/`** — os dois testes da frente C do Plano 2 sobre o
  Modelo Estrutural:
    - `ancora_2026-10-30/` testa a âncora da (R) e da (H) com o juro de 10 anos em média móvel;
    - `hiato_2026-10-30/` regride o hiato consolidado do BC contra NUCI, desocupação, PIB e CAGED.
  Os resultados estão no `RESULTADOS.md` de cada pasta, e a decisão em `coordenacao/C_modelo.md`.
  Rodar pelo caminho do arquivo (o hífen impede importar como módulo):

      uv run python analytics/brasil/structural_model/experimentos/hiato_2026-10-30/hiato_a.py

## Pending

- **`tvp_2026-08-21/`** — decidir se o teste de TVP vira script versionado (hoje só o
  resultado sobreviveu) ou se é descartado. O veredito depende de qual neutra se assume e não
  sobrevive fora da amostra, então a barra para reescrevê-lo é alta.
- **`curva_juros/`** — decidir entre integrar ou descartar.
