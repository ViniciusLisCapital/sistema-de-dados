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
- **Chart container**: card branco com cabeçalho de 3 linhas (título fixo, subtítulo derivado, fonte + período), o gráfico, as pills de range **abaixo** dele, e o botão "Dados no gráfico"
- **Footer**: linha centralizada com contexto

### Gráficos — Plotly
- **Tipo padrão**: `type:'scatter'`, `mode:'lines+markers'`, `line:{shape:'spline', smoothing:0.25}`, `fill:'tozeroy'`
- **Cor da linha**: `#1F2853` (navy)
- **Fill**: `rgba(31,40,83,0.06)`
- **Marcadores coloridos por variação**: verde `rgba(65,135,145,0.7)` se subiu, vermelho `rgba(234,82,58,0.7)` se caiu — array em `marker.color`
- **Marker size**: 3 normal, 4 para poucos pontos
- **Cada gráfico é um `<div id="...">` vazio** (nunca `<canvas>`) — `Plotly.newPlot(divId, traces, layout, config)`
- **Chart wrap**: `position:relative; height:480px;` (o `layout.height` do Plotly deve ficar próximo desse valor)
- **Zoom/pan interativo (obrigatório)**: arrastar move os dois eixos (pan), scroll/pinch dá zoom nos dois eixos, double-click reseta, sem gesto de box-zoom, mais botões de range rápido (1a/3a/5a/10a/Tudo) — via `dragmode:'pan'` + `scrollZoom:true` (nativo do Plotly) + `_bindYAutofit(divId)` chamado logo após cada `Plotly.newPlot`/`react`. **Os botões de range rápido são HTML normais + `Plotly.relayout()` direto, NÃO `xaxis.rangeselector` nativo do Plotly** — esse componente nativo quebrou em produção duas vezes (não suporta range exato por botão, e ainda ancora no range atual do eixo, que pode estar com padding automático) — ver `references/design-system.md#zoom-pan` para o porquê completo e o código (`mkLayout()`, `PLOTLY_CONFIG`, `quickRangeOptions()`/`renderQuickRangeButtons()`, `_bindYAutofit`) — mesmo padrão já usado em `analytics/brasil/economic_activity/report.html` (origem da correção) e nos demais relatórios analíticos.

### Cabeçalho descritivo (obrigatório em todo gráfico)
- Três linhas no topo do card, **acima** do gráfico: título, subtítulo e `Fonte: ... · <período>`
- **Só o título e a fonte são texto fixo.** O subtítulo e o período são preenchidos por JS **a cada render** — um subtítulo escrito no HTML passa a mentir assim que o usuário mexe num seletor, e é o print tirado depois desse clique que vai circular
- O subtítulo diz, nesta ordem: séries plotadas (quando acrescentam algo ao título) · estado dos **seletores** · unidade (a mesma string do título do eixo Y)
- Não repetir: pedaço que o título do eixo já contenha sai fora, e o nome da série some quando é o próprio título do gráfico
- O período vem da extensão **real** das séries plotadas, não de uma constante — numa visão de variação anual o gráfico começa um ano depois, e tem que dizer isso
- Código e o porquê: `references/design-system.md#cabecalho` (`describeChart()`, `dataExtent()`)

### Texto explicativo: justificado e na largura do bloco
- **Todo texto explicativo e de apêndice sai `text-align: justify`** — legenda de gráfico, corpo de apêndice, nota de metodologia, lead de seção
- **`hyphens: auto` junto, sempre**, e o `<html lang="pt-BR">` (ou `en`) é o que faz a hifenização existir: sem o `lang` o browser não hifeniza e o justificado abre rios de espaço branco
- **Sem `max-width` em `ch` na prosa.** Ela ocupa a largura do bloco — o que cobre o vazio à direita e, ocupando mais linha, deixa o bloco mais baixo
- **Não justifique** célula de tabela, popover de definição (`.info-pop`), linha de metadado em mono nem legenda centralizada: container estreito é onde os rios aparecem
- Código, medições e a tabela do que fica de fora: `references/design-system.md#prosa`

### E escrito para quem nunca viu o dashboard
- **A prosa do dashboard não é a nossa conversa sobre ele.** Cada bloco responde "o que é isto que estou vendo, e o que isso muda para mim?" — no vocabulário do domínio (dado, cálculo, relatório, banco), não no do repositório
- **Fora:** nome de função/arquivo do repositório, nome de tabela, comando de terminal, data de decisão nossa ("desde 2026-…"), pendência nossa ("segundos não medidos")
- **Nome de mecanismo → consequência**: não "granularidade trimestral", e sim "fica velho quando abre um trimestre novo". **Identificador → nome que se lê**: não `expc_focus_periodo`, e sim "a pesquisa Focus" — guarde o nome legível ao lado do técnico na estrutura de dados, para não divergirem
- **Ordem interna de funções não é explicação.** Diga o que pode dar errado e como se corrige
- O que é decisão, medição e "por que" continua sendo escrito — no `CLAUDE.md` da pasta e nos comentários, não na página
- Vale um teste: extraia os blocos de prosa do HTML renderizado e proíba a lista de termos, rodando contra o payload real. Ver `references/design-system.md#audiencia`

### Rótulos longos: nome curto + botão de definição
- Rótulo que não cabe (linha de tabela, toggle de série, label de stat card) vira **nome curto** + um botão `i` de 14px; o nome oficial da fonte e a explicação abrem num card no hover, e o clique fixa
- **Só ganha botão quem precisa** — a informação vive num mapa `chave → {full, desc, unit}`, e o ícone nasce da presença da entrada. Ícone em tudo não significa nada
- **Um único `.info-pop` no `<body>`**, reposicionado a cada abertura — nunca um popover por item
- `full` só entra no card quando difere do rótulo já visível; a última linha reaproveita a mesma string de unidade do título do eixo Y
- Código e o porquê: `references/design-system.md#info-card` (`attachInfo()`, `showInfo()`)

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

### Cores de séries: duas linhas do mesmo gráfico nunca podem ser confundidas
- **ΔE2000 ≥ 20 entre quaisquer duas séries que possam aparecer no mesmo gráfico.** Limiar calibrado contra as paletas publicadas de referência (Okabe-Ito fecha em 21,7; Tol bright em 20,5) — não é um número escolhido a esmo
- Use a `PALETTE` de 14 cores de `references/design-system.md#cores-series` (mínimo interno 20,8). `PALETTE[0]`, o navy da marca, é **reservado para a linha de total/agregado**
- **A cor sai da POSIÇÃO da série**, via `assignSeriesColors(cats, defaults)`, com as marcadas por padrão na frente da fila — nunca um literal `color:` por categoria. Foi exatamente isso que produziu, num relatório real, três pares de séries com a **mesma** cor na vista padrão: duas listas coloridas em momentos diferentes não sabem uma da outra
- **Acima de 13 séries, troque de canal**: a cor volta ao início da paleta e o `line.dash` muda. 13 matizes separáveis é o teto prático; não empilhe mais matizes
- **Verifique com o `deltaE()` do design-system no harness de teste**, por gráfico — e marque tudo de propósito para exercitar o tracejado, que nenhuma vista padrão alcança
- Cores da paleta antiga que **não** passam e saíram: `#02739B` (13,0 de `#418791`), `#FBC852` (13,9 de `#BB9B1D`), `#BFBFBF` (9,3 de `#9E9E9E`)

### Toggle de séries (quando multi-variável)
- Botões coloridos por série com `.toggle-btn`
- Cores vêm da `PALETTE` pela ordem (ver acima), não escolhidas à mão
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
