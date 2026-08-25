# analytics/brasil/expectations/ — Panorama de Expectativas (Focus)

Relatório HTML autocontido sobre o **Sistema de Expectativas de Mercado do BCB**, e só ele. Lê as
três tabelas `expc_focus`, `expc_focus_copom` e `expc_focus_periodo` de `macro_brasil` — sem meta de
inflação, sem série realizada, sem projeção do Copom. Escopo "só Focus" é decisão explícita do
usuário (2026-08-24); comparação contra meta/realizado vive nos relatórios de Inflação e Política
Monetária, cada um com a sua fonte declarada.

```powershell
uv run python analytics/brasil/expectations/generate_report.py   # -> reports/brasil/Expectations.html
node tests/test_expectations_js.js                               # framework + renderizadores
uv run python tests/test_expectations_data.py                    # payload vs. MySQL, valor a valor
```

Mesmo padrão dos demais: `generate_report.py` + `report.html` com `/*REPORT_DATA*/`,
`/*THEME_CSS*/` e `/*Y_AUTOFIT_JS*/` via `analytics.report_structure.builder.render_report()`.
Editar `report.html`, nunca o gerado.

## Abas

| Aba | Tabela | O que responde |
|---|---|---|
| Boletim | `expc_focus_periodo` (anual) | mediana de hoje × 1/4/12/52 semanas, por indicador e ano de referência, + barra de maiores revisões |
| Revisão | `expc_focus_periodo` (3 periodicidades) | fixa o período previsto e varre as datas de pesquisa. Eixo X alternável: data da pesquisa ou **meses até o período** (sobrepõe anos diferentes na mesma escala) |
| Curva do Copom | `expc_focus_copom` | curva por reunião em várias datas, Selic esperada por horizonte ao longo do tempo, e mapa de calor horizonte × semana |
| Horizonte Móvel | `expc_focus` | IPCA/IGP-M e componentes a 12m/24m, toggles suavizada e base, + inclinação 24m−12m |
| Trajetória | `expc_focus_periodo` | a curva à frente inteira numa semana (X = período previsto), com fotografias antigas sobrepostas + deslocamento |
| Dispersão | as três | desvio-padrão, coef. de variação, amplitude (só onde há min/max), tamanho do painel |
| Bases | `expc_focus` + `expc_focus_copom` | base 0 (30 dias) × base 1 (4 dias úteis) e o gap entre elas |
| Apêndice | cobertura medida no banco | as 4 reformulações, definição das bases, grade semanal, o que ficou de fora |

## Grade semanal e compressão do payload

Tudo que é série temporal é reduzido a **uma observação por semana ISO** e as três tabelas
compartilham **uma grade global** (`meta.grade`, 1.425 semanas de 1999-04 a hoje). Cada série é
gravada como `{i0, m[], s[], n[]}` — bloco contíguo a partir do índice `i0` da grade, `null` nas
semanas sem pesquisa. Sem isso o arquivo não fecha: 1,28 M de linhas na `expc_focus_periodo` sozinha.
Com isso o payload fica em **5,6 MB** (268 mil pontos semanais em ~2.260 séries).

Duas regras de redução **diferentes de propósito**, e a diferença importa se alguém for mexer:

- **`expc_focus_periodo`** reduz por JOIN com o `MAX(date)` da semana **na própria tabela**, então
  todo indicador de uma mesma semana vem da **mesma data de pesquisa** — é o que torna a tabela do
  Boletim uma leitura transversal honesta. Custo: uma série que não reportou naquela data específica
  perde a semana em vez de herdar o ponto anterior da semana.
- **`expc_focus` e `expc_focus_copom`** reduzem por `(série, semana)` em pandas — último ponto que
  *aquela série* tem na semana. As tabelas são pequenas e a leitura é série a série.

`minimo`/`maximo` só entram nos stores de `expc_focus` e `expc_focus_copom`. Para o `periodo` vão só
mediana, desvio-padrão e respondentes: as cinco estatísticas em 268 mil linhas dobrariam o arquivo
por uma leitura secundária. É por isso que a métrica "Amplitude" da aba Dispersão fica indisponível
nas três periodicidades.

**"Há 4 semanas" anda por data, não por posição na grade**: `gidxBackWeeks()` procura o ponto mais
recente ≤ hoje − 28 dias. Contar 4 posições daria 35 dias numa semana de feriado. A coluna
equivalente do Boletim publicado pelo BCB usa a data exata, então pode haver diferença de dias.

## Gotchas da fonte (o resumo; o completo está no Apêndice do próprio relatório)

- **Quatro reformulações** cortaram séries: 2018-07-05, **2021-02-17** (família antiga de índices de
  preços), **2021-09-13/14** (sai Produção industrial e o PIB setorial *trimestral*, entram os 5
  componentes do IPCA, desocupação e os componentes de demanda) e 2026-01-29. Quase todo componente
  começa em set/2021 por causa disso — não é falha de carga.
- **A base 1 não cobre o histórico todo**: começa em 2014-01 nos endpoints de inflação e 2021-03 no
  de Selic. `expc_focus_periodo` só tem base 0 (decisão de escopo — dobraria 1,28 M de linhas).
- **A ordem das reuniões do Copom não é alfabética** e não é derivável da data da pesquisa. O
  `_parseReuniao()` do template extrai `(ano, número)` de `"R<n>/<ano>"`; não há calendário do Copom
  no payload, e o eixo X da curva é a sequência de reuniões, não o calendário.
- **Eixo de categoria com mais de uma curva precisa de `categoryarray` explícito.** O Plotly ordena
  categoria por **ordem de aparição** entre os traces. Uma curva de 12 semanas atrás cota reuniões
  que já passaram (R4/26, R5/26): como são categorias novas para o eixo, iam parar depois de R5/28,
  no canto direito. `_copCategorias()` monta a união ordenada por `ord` e o layout passa
  `categoryorder: 'array'`. Foi bug visual real (2026-08-24) — qualquer gráfico de categoria novo
  aqui tem de fazer o mesmo.
- **"Período vigente" se mede pelo FIM, não pelo começo.** Filtrar `ref_date >= hoje` tira o ano
  corrente do seletor a partir de fevereiro — em agosto de 2026 a aba Revisão abria em 2027.
  `vigenteOuFuturo()` compara o fim do período (+12/+3/+1 mês conforme a periodicidade).
- **Δ de horizonte tem de comparar a mesma reunião.** No KPI do Copom, "a 1ª reunião à frente de 4
  semanas atrás" pode ser outra reunião (houve Copom no meio); a comparação é por `reuniao`, não por
  posição na fila.
- **Câmbio é fim de período**, não média (medido contra a PTAX realizada, 9 de 10 anos).
- **A unidade `%` cobre variação e nível** — IPCA e Selic na mesma coluna. Quem separa é a família.
- Indicador novo na fonte cai em `"Outros"` no mapa `_FAMILIAS` do gerador; o teste JS falha se isso
  acontecer, que é o sinal de que a pesquisa mudou.

## Pending

- **Confirmação visual num browser real** — o ambiente não tem browser, e a primeira rodada de
  revisão no browser (2026-08-24) já pagou: o eixo desordenado da curva do Copom só aparece com duas
  curvas na tela. Falta olhar: (a) o mapa de calor da aba Copom, único gráfico não-linha do
  relatório; (b) a tabela do Boletim com scroll horizontal e cabeçalho fixo; (c) o eixo invertido
  ("meses até o período") da aba Revisão.
- **Top5 não carregado** — os 6 endpoints Top5 têm a mesma forma de chave mais `tipo_calculo`, que já
  existe na PK com valor `'geral'`. É backfill de dados, não migração: uma vez carregados, "consenso
  vs. Top5" entra como pill em todas as abas sem mudança de estrutura. Ver
  [`domain/db/brasil/bcb/focus_inventario.md`](../../../domain/db/brasil/bcb/focus_inventario.md).
- **Ancoragem como leitura derivada** — a série "expectativa para t+1 ano, rolando" (para cada data
  de pesquisa, o ano seguinte) é montável no cliente a partir do store anual e não existe como aba.
  É a leitura padrão de desancoragem em research; entra barato se fizer falta.
- **Sem `data/` nem `referencia/`** — tudo vem do MySQL, nada local.
