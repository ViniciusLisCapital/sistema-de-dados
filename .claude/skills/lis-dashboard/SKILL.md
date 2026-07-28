---
name: lis-dashboard
description: >
  Cria dashboards HTML interativos para visualização de dados financeiros da Lis Capital.
  Use sempre que o usuário pedir gráficos, charts, dashboards ou visualizações de dados
  de ativos, posições, NAV, preço, quantidade, P&L, hedge, ou qualquer série temporal
  financeira. Também deve ser usado quando o usuário enviar arquivos CSV/XLSX com dados
  de ativos — mesmo que não peça gráficos explicitamente. Aplica-se a qualquer ativo
  (ações, opções, fundos, índices) e qualquer métrica (% NAV, preço, quantidade, retorno,
  volatilidade). O padrão visual é o da Lis Capital: fundo cinza claro, cards brancos,
  tipografia Barlow/JetBrains Mono, paleta navy/gold/green/red.
---

# Lis Capital — Dashboard Skill

Skill para gerar dashboards HTML interativos no padrão visual da Lis Capital.

## Quando usar

- Usuário envia CSV/XLSX com dados de ativos (mesmo sem pedir gráfico explicitamente)
- Pedidos de gráficos de % NAV, preço, quantidade, P&L, retorno, etc.
- Qualquer série temporal financeira que precise de visualização
- Pedidos de "montar gráfico", "dashboard", "visualização" de dados de mercado

## Fluxo obrigatório (SEMPRE seguir nesta ordem)

### Passo 1 — Ler e entender os dados
Usar Python (openpyxl/pandas/csv) para:
1. Listar headers/colunas do arquivo
2. Mostrar primeiras linhas como amostra
3. Identificar: coluna de data, métricas numéricas, ativo(s), período coberto
4. Apresentar ao usuário um resumo estruturado dos dados encontrados

### Passo 2 — Perguntar ao usuário
ANTES de montar qualquer gráfico, perguntar ao usuário:
- Quais gráficos ou visualizações ele quer
- Qual métrica principal (% NAV, preço, quantidade, etc.)
- Se quer filtros por período, toggle de séries, etc.
- Qualquer preferência específica

**Não assumir os gráficos por conta própria.** O usuário decide o que quer ver.

### Passo 3 — Ler a referência de design
`view` o arquivo `references/design-system.md` nesta skill para CSS base, componentes e padrões JS.

### Passo 4 — Montar os dashboards
Seguir as regras de design abaixo. Confirmar o NAV do fundo se necessário para cálculos de % — o usuário pode ter informado nas memórias.

## Estrutura do output

O output é um **artifact HTML direto no chat** (não salvar em pasta específica). O HTML inclui:
- Google Fonts (Barlow, Barlow Condensed, JetBrains Mono)
- Plotly 2.35.2 via CDN (charting padrão do projeto desde 2026-07-28 — ver `references/design-system.md#zoom-pan`; substituiu Chart.js, que esta skill usava antes)
- CSS inline com variáveis do design system
- Dados embarcados como array JS (não fetch externo)

## Regras obrigatórias

### Layout
- **Página**: `padding: 24px 32px`, sem `max-width` (full-width)
- **Header**: logo "LIS CAPITAL", título central, badge + data à direita
- **Stats cards**: grid de 3 colunas acima do gráfico (último valor + data, máxima + data, mínima + data)
- **Chart container**: card branco com título, subtítulo, e botão "Dados no gráfico"
- **Footer**: linha centralizada com contexto

### Gráficos — Plotly
- **Tipo padrão**: `type:'scatter'`, `mode:'lines+markers'`, `line:{shape:'spline', smoothing:0.25}`, `fill:'tozeroy'`
- **Cor da linha**: `#1F2853` (navy)
- **Fill**: `rgba(31,40,83,0.06)`
- **Marcadores coloridos por variação**: verde `rgba(65,135,145,0.7)` se subiu, vermelho `rgba(234,82,58,0.7)` se caiu — array em `marker.color`
- **Marker size**: 3 normal, 4 para poucos pontos
- **Cada gráfico é um `<div id="...">` vazio** (nunca `<canvas>`) — `Plotly.newPlot(divId, traces, layout, config)`
- **Chart wrap**: `position:relative; height:480px;` (o `layout.height` do Plotly deve ficar próximo desse valor)
- **Zoom/pan interativo (obrigatório)**: arrastar move os dois eixos (pan), scroll/pinch dá zoom nos dois eixos, double-click reseta, sem gesto de box-zoom, mais botões de range rápido (1a/3a/5a/10a/Tudo) — via `dragmode:'pan'` + `scrollZoom:true` (nativo do Plotly) + `rangeselector`, e `_bindYAutofit(divId)` chamado logo após cada `Plotly.newPlot`/`react` (cobre o caso em que um clique no rangeselector move X sem mover Y). Ver `references/design-system.md#zoom-pan` para o bloco de código completo (`mkLayout()`, `PLOTLY_CONFIG`, `_bindYAutofit`) e a explicação — mesmo padrão já usado em `analytics/exchange_rate/report.html`/`analytics/inflation/report.html`/`analytics/monetary_policy/report.html`.

### Botão "Dados no gráfico"
OBRIGATÓRIO em todo dashboard. Comportamento:
- Começa **desligado** (labels ocultos)
- Ao clicar, mostra valores sobre cada ponto do gráfico
- Ao clicar de novo, oculta
- Classe `.dl-toggle` / `.dl-toggle.on`

### Formatação de labels (texto sobre o gráfico via `text`/`textposition`)
- **Truncar, não arredondar**: usar `Math.floor(v*10)/10` antes de `.toFixed(1)`
- **Separador decimal**: vírgula (formato BR) → `.replace('.',',')`
- **Sufixo**: `%` para percentuais, `R$` prefix para preços
- **Exemplo**: 16.951 → "16,9%" (não "17,0%")
- **Step para muitos pontos**: >60 pontos → mostrar a cada 5; >30 → a cada 3; ≤30 → todos
- **Estilo do label**: `textfont: {family:'JetBrains Mono', size:9, color: <cor da série>}` — Plotly não tem um "chip" com fundo/borderRadius por label como o chartjs-plugin-datalabels tinha; texto simples sobre o gráfico é o padrão aqui, não tente forçar um background por annotation (custo/complexidade não valem a pena para esse efeito)

### Tooltips (`hoverlabel` + `hovertemplate`)
- Background: `#1F2853` (`hoverlabel.bgcolor`)
- Font: Barlow 12px (`hoverlabel.font`) — Plotly usa uma única fonte para título+corpo do hover, não título/corpo separados como o Chart.js
- `hovermode: 'x unified'` no layout
- Valores formatados em BR entram via `customdata` (não dá pra formatar direto no `%{y}` do `hovertemplate` com vírgula decimal)
- Mostrar todas as métricas disponíveis (% NAV, preço, quantidade, etc.) — várias linhas no mesmo `hovertemplate`, `<br>` entre elas

### Filtros de período (quando aplicável)
- Botões tipo pill com classe `.month-btn`
- Primeiro botão = período completo (ex: "2026"), depois meses individuais
- Ao trocar filtro, atualizar gráfico E stats cards

### Toggle de séries (quando multi-variável)
- Botões coloridos por série com `.toggle-btn`
- Cada série tem cor fixa: navy (primária), `#02739B` (secundária), `#BB9B1D` (terciária)
- Séries secundárias começam desligadas
- Eixos independentes: primária à esquerda, secundárias à direita

### Escalas
- Grid X: `showgrid:false` (linha de base só, `showline:true` + `linecolor:'rgba(31,40,83,0.1)'`), ticks JetBrains Mono 9-10px — Plotly gerencia a densidade de ticks automaticamente (sem um `maxTicksLimit` explícito; use `xaxis.nticks` só se precisar forçar)
- Grid Y: `gridcolor:'rgba(31,40,83,0.06)'`, ticks JetBrains Mono 10px
- Ticks Y com sufixo simples via `ticksuffix`/`tickprefix` (`%`, `R$`, `k`) quando o formato é direto — para vírgula decimal BR completa, use `customdata`/`hovertemplate` no tooltip em vez de tentar formatar o tick do eixo (ver nota em "Formatação BR" na referência)

### Stats cards
- Exatamente 3 cards em grid `repeat(3, 1fr)`
- Card 1: último valor + data
- Card 2: máxima + data (classe `.up` no valor)
- Card 3: mínima + data (classe `.dn` no valor)
- Os cards devem ser dinâmicos (atualizar com filtros se houver)

## Paleta de cores (referência rápida)

| Token    | Valor         | Uso                        |
|----------|---------------|----------------------------|
| --bg     | #F4F5F7       | Fundo da página            |
| --bg2    | #FFFFFF       | Cards e containers         |
| --navy   | #1F2853       | Texto principal, linhas    |
| --ice2   | #3A4F72       | Texto secundário           |
| --gold   | #BB9B1D       | Destaques, filtro ativo    |
| --muted  | #7A88A8       | Labels, subtítulos         |
| --green  | #418791       | Positivo (subiu)           |
| --red    | #EA523A       | Negativo (caiu)            |
| --purple | #02739B       | Ações, toggles, badges     |
| --line   | rgba(31,40,83,0.1) | Bordas                |

## Tipografia

| Variável | Família                        | Uso                          |
|----------|--------------------------------|------------------------------|
| --sans   | Barlow                         | Texto geral                  |
| --cond   | Barlow Condensed               | Títulos, stat values         |
| --mono   | JetBrains Mono                 | Labels, datas, dados, badges |

## Leitura de dados

### XLSX (openpyxl)
```python
import openpyxl
wb = openpyxl.load_workbook('arquivo.xlsx', data_only=True)
ws = wb[wb.sheetnames[0]]
for row in ws.iter_rows(min_row=2, values_only=True):
    # extrair colunas relevantes
```

### CSV (direto)
```python
import csv
with open('arquivo.csv') as f:
    reader = csv.DictReader(f)
    for row in reader:
        # usar row['coluna']
```

Sempre imprimir os headers e primeiras linhas para identificar a estrutura antes de montar o dashboard.

## Referência completa

Para o CSS base completo, componentes HTML, e exemplos de código, consulte:
→ `references/design-system.md`
