# analytics/brasil/monetary_policy/ — Contexto para o Claude

Curva de Phillips estimada + material de referência. **Esta pasta não tem relatório HTML** — a
réplica do modelo pequeno do BCB foi removida em 2026-08.

## A réplica removida (2026-08)

Removida a pedido do usuário, junto com as duas tabelas que a alimentavam (`pm_hiato_seed`,
`pm_parametros`). Saíram `model.py` (motor de simulação das 5 equações), `generate_report.py`,
`report.html` e o output `reports/brasil/bcb_model.html`. Motivo: um modelo novo está sendo
construído sobre a extração automatizada do relatório do BCB (`connectors/bcb_rpm.py` +
`pm_hiato_produto`/`pm_hiato_produto_vintages`), e o hiato/parâmetros digitados à mão que a réplica
usava deixaram de fazer sentido como fonte.

**A lacuna que motivou a remoção, para não ser repetida no modelo novo:** a réplica aproximava a
trajetória futura esperada da Selic pela taxa corrente/simulada, sem curva forward, então não
descontava a antecipação de reversão de um choque. O IRF saía com sinal e timing certos, mas
magnitude ~4-5x maior que a publicada pelo BCB. `expc_focus_copom` é a curva forward que resolve
isso — o `MODEL_REPLICATION_PLAN.md` registra que `i^e_{t,t+4|t}` precisa da média ponderada
0,5/1/1/1/0,5 dos 4 trimestres à frente. Ver "Pendências" no [`CLAUDE.md` da
raiz](../../../CLAUDE.md).

Histórico completo da réplica (o que foi validado e o que não fechou) em
`referencia/MODEL_REPLICATION_PLAN.md` e no git log.

## O que ficou na pasta

- **`phillips_excel.py`** — estima a Curva de Phillips "flavored" (12m Y/Y, sem intercepto, pesos de
  inércia e expectativa somando 1 para garantir neutralidade de longo prazo) e gera
  `data/curva_phillips_auditoria.xlsx`, planilha auditável célula a célula com histórico e projeção
  na MESMA aba, para que as defasagens sejam simples referências de linha. Independente do motor
  removido — lê o MySQL direto (`inflc_agregados`, `expc_focus`, `cmb_ptax`, `inflc_meta`,
  `comm_icbr_usd`, `pm_hiato_produto`), nunca usou seed nem `pm_parametros`.

  ```powershell
  uv run python -c "from analytics.brasil.monetary_policy.phillips_excel import run; run()"
  ```

- **`referencia/`** — PDFs do modelo original do BCB (`atualizacao_modelos.pdf`,
  `modelo_agregado.pdf`, `modelo_desagregado.pdf`), o `MODEL_REPLICATION_PLAN.md`, e os CSVs das duas
  tabelas dropadas (`pm_parametros_RI_2021T4.csv` — as 22 modas a posteriori da Tabela 1 do boxe de
  dez/2021 —, `pm_hiato_seed_2026-04.csv`).
- **`models/curva_juros/`** — material legado de curva de juros (`yield_curve.py`,
  `yield_curve_model.py`, planilhas de DI/títulos/governo sob `guardar/dados/`), movido de
  `quarantine/` em 2026-08. Nunca integrado a nada, e o motor que seria o destino (`model.py`) foi
  removido — revisitar quando essa frente for retomada.
- **`copom_280_vs_279_comparison.md`/`.pdf`** — comparação de comunicados do Copom.
- **`data/`** — `curva_phillips_auditoria.xlsx`, saída do `phillips_excel.py`.

## Pending

- **Modelo novo sobre `pm_hiato_produto`/`_vintages`** — ainda não começado. Quando começar, usar
  `expc_focus_copom` como curva forward desde o início (ver a lacuna acima).
- **`models/curva_juros/`** — decidir entre integrar ou descartar.
