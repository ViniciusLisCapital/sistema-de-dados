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
- Chart.js 4.4.1 via CDN
- chartjs-plugin-datalabels 2.2.0 via CDN
- CSS inline com variáveis do design system
- Dados embarcados como array JS (não fetch externo)

## Regras obrigatórias

### Layout
- **Página**: `padding: 24px 32px`, sem `max-width` (full-width)
- **Header**: logo "LIS CAPITAL", título central, badge + data à direita
- **Stats cards**: grid de 3 colunas acima do gráfico (último valor + data, máxima + data, mínima + data)
- **Chart container**: card branco com título, subtítulo, e botão "Dados no gráfico"
- **Footer**: linha centralizada com contexto

### Gráficos — Chart.js
- **Tipo padrão**: `line` com `fill:true`, `tension:0.25`, `borderWidth:2`
- **Cor da linha**: `#1F2853` (navy)
- **Fill**: `rgba(31,40,83,0.06)`
- **Pontos coloridos por variação**: verde `rgba(65,135,145,0.7)` se subiu, vermelho `rgba(234,82,58,0.7)` se caiu
- **Point radius**: 3 normal, 4 para poucos pontos, hover sempre 6-7
- **Options obrigatórias**: `responsive:true`, `maintainAspectRatio:false`
- **Chart wrap**: `position:relative; height:480px;`
- **Registrar plugin**: `Chart.register(ChartDataLabels)` no início do script

### Botão "Dados no gráfico"
OBRIGATÓRIO em todo dashboard. Comportamento:
- Começa **desligado** (labels ocultos)
- Ao clicar, mostra valores sobre cada ponto do gráfico
- Ao clicar de novo, oculta
- Classe `.dl-toggle` / `.dl-toggle.on`

### Formatação de labels (datalabels)
- **Truncar, não arredondar**: usar `Math.floor(v*10)/10` antes de `.toFixed(1)`
- **Separador decimal**: vírgula (formato BR) → `.replace('.',',')`
- **Sufixo**: `%` para percentuais, `R$` prefix para preços
- **Exemplo**: 16.951 → "16,9%" (não "17,0%")
- **Step para muitos pontos**: >60 pontos → mostrar a cada 5; >30 → a cada 3; ≤30 → todos
- **Estilo do label**: `backgroundColor:'rgba(255,255,255,0.85)'`, `borderRadius:3`, font JetBrains Mono 9px

### Tooltips
- Background: `#1F2853`
- Font título: JetBrains Mono 11px
- Font body: Barlow 12px
- Padding: 12, cornerRadius: 8
- Mostrar todas as métricas disponíveis (% NAV, preço, quantidade, etc.)

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
- Grid X: `rgba(31,40,83,0.04)`, ticks JetBrains Mono 9-10px, `maxTicksLimit:20`
- Grid Y: `rgba(31,40,83,0.06)`, ticks JetBrains Mono 10px
- Ticks Y com sufixo adequado (`%`, `R$`, `k`)

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
