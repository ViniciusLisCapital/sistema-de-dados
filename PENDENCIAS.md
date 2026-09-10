# Pendências transversais

O que **não tem dono numa pasta só**. Toda pendência de um relatório específico vive no `CLAUDE.md`
da pasta dele, na seção "Pending", e é lá que ela é atualizada:

| área | onde |
|---|---|
| Câmbio | [`analytics/brasil/exchange_rate/CLAUDE.md`](analytics/brasil/exchange_rate/CLAUDE.md) |
| Inflação (BR) | [`analytics/brasil/inflation/CLAUDE.md`](analytics/brasil/inflation/CLAUDE.md) |
| Atividade | [`analytics/brasil/economic_activity/CLAUDE.md`](analytics/brasil/economic_activity/CLAUDE.md) |
| Fiscal | [`analytics/brasil/fiscal_policy/CLAUDE.md`](analytics/brasil/fiscal_policy/CLAUDE.md) — inclui o double-count de transferências no Governo Geral, a re-estimação dos multiplicadores do IEG e o bloqueio do MEFA |
| Crédito | [`analytics/brasil/credit/CLAUDE.md`](analytics/brasil/credit/CLAUDE.md) |
| Mercado de trabalho (BR) | [`analytics/brasil/labor_market/CLAUDE.md`](analytics/brasil/labor_market/CLAUDE.md) |
| Política monetária | [`analytics/brasil/monetary_policy/CLAUDE.md`](analytics/brasil/monetary_policy/CLAUDE.md) — inclui o bloco de preços administrados, a eq. (5) dentro do filtro, e **a taxa neutra**, que é a premissa que domina os cenários (r\* em ~7,9% contra ~4,8% do BC) |
| Expectativas | [`analytics/brasil/expectations/CLAUDE.md`](analytics/brasil/expectations/CLAUDE.md) |
| Inflação (US) | [`analytics/us/inflation/CLAUDE.md`](analytics/us/inflation/CLAUDE.md) |
| Mercado de trabalho (US) | [`analytics/us/labor_market/CLAUDE.md`](analytics/us/labor_market/CLAUDE.md) |
| Curadoria / bibliografia | [`repository/CLAUDE.md`](repository/CLAUDE.md) |
| Calendário e status | [`domain/release_calendar/CLAUDE.md`](domain/release_calendar/CLAUDE.md) · [`domain/dashboards/CLAUDE.md`](domain/dashboards/CLAUDE.md) |

Várias delas são a mesma coisa: **confirmação visual num browser real**, que o ambiente de
desenvolvimento não tem.

---

## Cobertura de dados

- **Expectativas Focus — consumo nos relatórios**: **o relatório dedicado existe desde 2026-08-24**
  (`analytics/brasil/expectations/` → `reports/brasil/Expectations.html`, 8 abas sobre as 3 tabelas e
  nada mais — inclusive o gráfico de convergência, que só a `expc_focus_periodo.data_referencia`
  permite). O que segue pendente é o consumo **dentro das outras áreas**, onde a expectativa entra
  cruzada com meta/realizado/modelo — coisa que o relatório de escopo "só Focus" deliberadamente não
  faz. Por ordem de retorno: (a) `expc_focus_copom` no modelo de política monetária — é a curva
  forward cuja ausência produziu o IRF 4-5x maior que o do BCB na réplica removida (o motor
  aproximava a Selic futura pela taxa corrente); o `MODEL_REPLICATION_PLAN.md` registra que
  `i^e_{t,t+4|t}` precisa da média ponderada 0,5/1/1/1/0,5 dos 4 trimestres à frente; (b) aba de
  expectativas em `analytics/brasil/inflation/` — o que o Panorama de Expectativas não pode mostrar:
  as medianas anuais **contra `inflc_meta`**; (c) diferenciais ex-ante em
  `analytics/brasil/exchange_rate/`, pendência já aberta em 3 `CLAUDE.md`; (d) consenso vs. realizado
  em `economic_activity/`, `fiscal_policy/` e `labor_market/`.
- **Focus Top5 não carregado**: os 6 endpoints Top5 têm a mesma forma de chave das 3 tabelas mais a
  dimensão `tipo_calculo`, que já existe na chave com valor `'geral'` — então é backfill de dados,
  não migração. Só vale se a leitura "consenso vs. Top5" interessar. `base_calculo=1` na
  `expc_focus_periodo` está na mesma situação.
- **Mercado de trabalho — pendências pós-Novo CAGED** (o conector do FTP e as 3 tabelas de corte
  ficaram prontos em 2026-08, ver `domain/db/brasil/mte/` e `analytics/brasil/labor_market/fontes_dados.md`;
  a rotulagem estoque-vs-saldo de `mt_caged.py` e a integração das 3 tabelas ao relatório foram
  resolvidas em 2026-08, ver a aba "Emprego Formal"):
  (a) cortes do microdado ainda não modelados: município, ocupação (CBO), sexo/idade/instrução/raça
  — todos disponíveis no mesmo microdado já baixado, adicionar é só uma tabela irmã nova com o
  mesmo padrão (`categoria`/`metrica`), sem migração;
  (b) `mt_pnad_trimestral`: nível UF/N3 deixado de fora deliberadamente, sem previsão.
- **US — expandir dados**: o mapeamento das 8 áreas macro está em [`us_project/`](us_project/)
  (levantado ao vivo contra as APIs, 377 séries FRED conferidas uma a uma). Inflação e mercado de
  trabalho já foram construídos — ver os dois `CLAUDE.md` da tabela acima.
  **Falta**: as outras 6 áreas macro (só `bls.py` e `bea.py` existem como connectors), o resto do
  mercado de trabalho (**claims semanais e ECI** — CPS, CES e produtividade entraram; claims seria
  a primeira grade *semanal* do schema), os
  pesos pré-2020 do CPI (existem
  desde 1947 no site do BLS, em 2 formatos antigos sem parser — é lacuna de parser, não de dado),
  CPI-W/C-CPI-U (schema e loader suportam, não carregados) e, do lado do PCE, as tabelas **reais** nas
  mesmas 402 linhas (2.4.3U índices de quantidade e 2.4.6U dólares encadeados — seriam um `medida` novo
  na mesma árvore, mas são atividade, não inflação: pelo critério de prefixo temático virariam `atv_`).
- **Jobs de rotina incompletos** (a checagem de freshness em `domain/release_calendar/sync.py` confirmou
  em 2026-08-17 que isto causa atraso real, não só teórico: `comm_icbr`/`comm_icbr_usd` estavam um mês
  atrás e avançaram ao rodar o script à mão). O `--continuous` do `update_db.py` (2026-08) fechou
  metade do buraco: `cmb_ptax`, `cmb_dollar_index`, `cmb_dollar_index_em`, `cmb_fx_latam`,
  `cmb_equity_us` e `comm_brent` já rodam por ele (via `registry.py`, mesmo as 6
  de `macro_international`), e **o agendamento existe desde 2026-09-03** — a tarefa
  `Macro - series diarias` roda `--continuous` de 30 em 30 min das 09:30 às 12:00, cobrindo
  as 11 tabelas contínuas (ver [`jobs/CLAUDE.md`](jobs/CLAUDE.md)). O que segue
  **sem nenhum job**, só à mão ou via `--tables`: `comm_icbr`/`comm_icbr_usd`/`inflc_meta` e
  `inflc_decomposicao_item` (este alimenta os núcleos MA/MS/DP do IPCA-15) em
  `domain/db/brasil/`, `clima_oni`/`cmb_real_rates` em `domain/db/international/`, e
  `cmb_risco_pais` (que por natureza não automatiza — planilha exportada à mão da Bloomberg).
  `update_international.py` continua com 3 scripts só.
- **Órfãos de verdade são só duas tabelas** — `comm_brent` e `clima_oni`, ambas insumo da réplica do
  modelo do BCB removida em 2026-08: decidir se voltam a alimentar o modelo novo ou se são dropadas.
  A lista antiga de "órfãos" desta seção estava errada, conferida script a script em 2026-08-19:
  `comm_icbr` (ppp_equilibrium + ridge_deviation_model + phillips_excel), `comm_icbr_usd` e
  `inflc_meta` (ppp_equilibrium + phillips_excel), `atv_pib_usd` (generate_report do câmbio +
  ppp_equilibrium), `cmb_dollar_index`/`cmb_dollar_index_em`/`cmb_equity_us`
  (ppp_equilibrium) e `cmb_real_rates` (real_rates_comparison.py) todas têm consumidor vivo — o que
  a remoção da réplica quebrou foi menos do que se registrou na época.
- **`team_materials/agent_materials/exchange_rate/` — notas desatualizadas**: `data_inventory.md` ainda diz que o `conceptual_map.md` "não foi construído" (já foi); `introduction_pt.md` não lista o `conceptual_map.md` entre os documentos da pasta.
- **Kinea PDF órfão**: `team_materials/agent_materials/exchange_rate/kinea_fx_mental_models.pdf` existe mas não há `.md` de origem em lugar nenhum, e `bibliography.md` ainda marca Kinea como "pendente" — investigar se é um artefato de teste esquecido ou uma síntese real nunca finalizada (fonte bruta: `repository/mental_model/kinea_insights/`).
