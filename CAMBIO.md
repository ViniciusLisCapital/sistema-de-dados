# Pipeline Cambial — Status e Pendências

Schemas MySQL: `macro_brasil` · `macro_international` · `macro_analytics` (servidor 192.168.15.200)  
Entry points: `jobs/update_db.py` · `jobs/update_international.py` · `jobs/update_analytics.py`  
Construído em: junho 2026 · Reestruturado: junho 2026

---

## O que foi feito

### Fase 1 — BCB + FRED (connectors existentes)

| Tabela | Schema | Fonte | Período | Script |
|---|---|---|---|---|
| `reservas` | `macro_brasil` | BCB SGS 3546 | 2004 → hoje | `domain/db/brasil/bcb/reservas.py` |
| `balanco_pagamentos` | `macro_brasil` | BCB SGS (10 séries) | 2001 → hoje | `domain/db/brasil/bcb/balanco_pagamentos.py` |
| `fluxo_cambial` | `macro_brasil` | BCB SGS (6 séries) | 2003 → hoje | `domain/db/brasil/bcb/fluxo_cambial.py` |
| `termos_de_troca` | `macro_brasil` | BCB SGS 22099/22100 | variado | `domain/db/brasil/bcb/termos_de_troca.py` |
| `diferenciais_juros` | `macro_analytics` | BCB SGS + FRED | janela 36m | `domain/db/analytics/fred/diferenciais_juros.py` |

**`reservas`** — séries armazenadas:
- `reservas_liquidez_usd` — conceito de liquidez (USD milhões)

**`balanco_pagamentos`** — séries armazenadas:
- `conta_corrente`, `balanca_comercial_servicos`, `exportacao_bens`
- `conta_financeira`, `investimento_direto_liquido`, `idp_ingressos`, `ide_saidas`
- `investimento_carteira`, `carteira_acoes`, `carteira_renda_fixa`

**`fluxo_cambial`** — séries armazenadas:
- Total: `total_saldo`, `total_entrada`, `total_saida`
- Comercial: `comercial_entrada`, `comercial_saida`
- Financeiro: `financeiro_saldo`

**`termos_de_troca`** — séries armazenadas:
- `termos_de_troca_a` (22099), `termos_de_troca_b` (22100) — descrições exatas pendentes de verificação

**`diferenciais_juros`** — séries armazenadas (frequência mensal, month-start):
- Brutas: `selic`, `fed_funds`, `ipca_12m`, `cpi_12m_us`
- Diferenciais ex-post: `diferencial_nominal`, `real_br_ex_post`, `real_us_ex_post`, `diferencial_real`

### Fase 2 — BIS + CFTC (novos connectors)

| Tabela | Schema | Fonte | Período | Script |
|---|---|---|---|---|
| `reer` | `macro_international` | BIS API (stats.bis.org) | 1994 → hoje | `domain/db/international/bis/reer.py` |
| `cot_fx` | `macro_international` | CFTC TFF ZIPs | 2010 → hoje | `domain/db/international/cftc/cot_fx.py` |

**`reer`** — países × tipos (388 obs cada, ~1994–hoje):
- Brasil (BR), México (MX), Chile (CL), Colômbia (CO)
- Tipos: `real_broad`, `nominal_broad`
- BIS API key order: `FREQ.EER_TYPE.EER_BASKET.REF_AREA` (ex: `M.R.B.BR`)
- `real_narrow` foi excluído do escopo

**`cot_fx`** — BRL e MXN; semanal (terças):
- `open_interest`, `lev_long`, `lev_short`, `lev_net`, `nonrept_long`, `nonrept_short`
- Fonte: CFTC Traders in Financial Futures (`fut_fin_txt_{YYYY}.zip`)
- CLP e COP **não têm** futuros CME no relatório TFF

### Connectors criados

| Arquivo | API | Auth |
|---|---|---|
| `connectors/bis.py` | BIS Statistics API v1 (`stats.bis.org/api/v1`) | Nenhuma |
| `connectors/cftc.py` | CFTC TFF ZIPs anuais | Nenhuma |

---

## Relatório HTML — analytics/cambio/

Construído em junho 2026. Arquivo único autocontido (`reports/cambio_latest.html`) gerado por `analytics/cambio/generate_report.py` a partir do template `analytics/cambio/report.html`.

### Como atualizar

```powershell
# Atualizar dados (opcional — só se quiser dados mais frescos)
uv run python jobs/update_db.py            # macro_brasil (inclui reservas, BOP, fluxo, termos)
uv run python jobs/update_international.py # macro_international (reer, cot_fx)
uv run python jobs/update_analytics.py    # macro_analytics (diferenciais_juros)

# Gerar relatório
uv run python -c "from analytics.cambio.generate_report import run; run()"
# Saída: reports/cambio_latest.html  (~50 KB, abre em qualquer browser)
```

### Mecanismo de injeção

O template contém o marcador `/*REPORT_DATA*/` num bloco `<script>`. `generate_report.py` lê tabelas de `macro_brasil`, `macro_international` e `macro_analytics`, serializa como JSON e substitui o marcador via `str.replace()`. Sem Jinja2.

### Charts ativos

| ID | Dados | Tipo |
|---|---|---|
| `chart-nominal-rates` | Selic + Fed Funds | linha |
| `chart-diferencial-nominal` | diferencial_nominal | linha + fill |
| `chart-taxas-reais` | real_br/us ex-post + diferencial | 3 linhas |
| `chart-reer` | BR/MX/CL/CO real_broad | 4 linhas + linha base 100 |
| `chart-cot-brl` | lev_net (barras) + open_interest | bar + linha eixo duplo |
| `chart-reservas` | reservas_liquidez_usd | linha + fill |
| `chart-termos` | termos_de_troca_a/b | 2 linhas |
| `chart-fluxo` | total/comercial/financeiro_saldo | 3 linhas |
| `chart-bop` | cc + IDP + conta_financeira + carteira | 4 linhas |

---

## Pendências

### Alta prioridade

#### 1. Reservas internacionais — série "brutas" em aberto

O código SGS 13127 (supostamente `reservas_brutas_usd`) retorna timeout consistente — pode ser código errado ou série descontinuada. O BCB publica vários conceitos de reservas (liquidez, caixa, brutas) com fontes e metodologias distintas.

**Próximos passos:**
- Acessar o buscador de séries do BCB SGS: https://www3.bcb.gov.br/sgspub/localizarseries/localizarSeries.do
- Buscar por "reservas internacionais" e mapear os códigos disponíveis
- Avaliar se o conceito "brutas" é necessário para o dashboard ou se "liquidez" (3546) já é suficiente
- Verificar também a posição de swaps cambiais do BCB (não disponível no SGS — necessita scraper da URL `https://www4.bcb.gov.br/pom/demab/cronogramacambiais/vencdata.asp`)

#### 2. Diferenciais de juros ex-ante (nominal e real)

A `diferenciais_juros` hoje contém apenas ex-post (inflação realizada). Os ex-ante usam expectativas de mercado:

**Diferencial nominal ex-ante:**
- Brasil: mediana Focus Selic EOP 12m à frente (já em `macro_brasil.expectativas`)
- EUA: taxa implícita nos Fed Funds futuros (FRED: `FF{mês}` futures ou OIS) — **pendente de implementação**

**Diferencial real ex-ante:**
- Brasil: Selic EOP Focus 12m − IPCA 12m Focus (ambos já em `expectativas`)
- EUA: taxa implícita − CPI 12m expectativa (FRED: Michigan Survey `MICH` ou 5yr breakeven `T5YIE`)

**Implementação sugerida:** criar novas séries em `diferenciais_juros` com sufixo `_ex_ante` sem alterar as séries ex-post já existentes.

### Média prioridade

#### 3. Fluxo cambial — granularidade adicional

A BCB publica sub-itens do fluxo financeiro (CEP/CBE) na Nota Cambial semanal que podem ter códigos SGS — ainda não confirmados. Séries candidatas (24372–24376) retornaram dados na pesquisa inicial mas com descrições não confirmadas. Ver Nota Cambial BCB para mapeamento.

#### 4. Termos de troca — verificar descrições

SGS 22099 e 22100 têm descrições distintas (possivelmente metodologias FOB vs. CIF ou cestas diferentes). Confirmar via metadados BCB SGS antes de usar nos dashboards.

#### 5. Cupom cambial + futuros B3 — Bloomberg (Fase 3)

Deferred: requer `blpapi`/`xbbg` na máquina de Bloomberg.
- `cupom_cambial`: curva DDI/FRC, schema `PRIMARY KEY (date, name, maturity)`
- `b3_fx_futures`: DOL/WDO preço, volume, OI

---

## Notas técnicas

### BIS API
- Base correta: `https://stats.bis.org/api/v1/` (não `data.bis.org`)
- Key structure WS_EER: `FREQ.EER_TYPE.EER_BASKET.REF_AREA`
- Colunas CSV retornadas: `FREQ, EER_TYPE, EER_BASKET, REF_AREA, TIME_PERIOD, OBS_VALUE, ...`

### CFTC TFF
- URL: `https://www.cftc.gov/files/dea/history/fut_fin_txt_{YYYY}.zip`
- ZIP contém: `FinFutYY.txt` (87 colunas)
- Coluna de data: `Report_Date_as_YYYY-MM-DD` (2013+) ou `Report_Date_as_MM_DD_YYYY` (2010–2012 — o nome é enganoso, os valores também são `YYYY-MM-DD`). O connector auto-detecta.
- Histórico disponível: 2010 → hoje (2006–2009 retornam 404 no CFTC).
- FX contracts no arquivo: BRL e MXN. CLP/COP não têm futuros CME no TFF.

### Selic + alinhamento de frequência
- BCB SGS 432 (Selic) usa datas de reunião do COPOM, não datas de calendário
- Em `diferenciais_juros.py`: `bcb_wide.resample("MS").last()` alinha para month-start antes de concatenar com dados FRED mensais

---

## Roadmap do Relatório

### Fase 1 — Qualidade e detalhe dos dados

**Objetivo:** o relatório deve mostrar o quadro cambial completo, sem lacunas de série nem dados truncados.

#### 1a. Histórico `diferenciais_juros` (pendente)

O relatório hoje exibe dados a partir de ~2023 mesmo com o seletor "10a" ativo. O script usa janela padrão de 36 meses. Expandir a carga histórica: Selic disponível desde 1996 no BCB SGS, Fed Funds desde 1954 no FRED. Script: `domain/db/analytics/fred/diferenciais_juros.py`. Atenção: BCB SGS 432 (Selic diária) retorna 406 para janelas > ~5 anos — investigar uso de série mensal alternativa ou chunking.

#### 1b. Diferenciais ex-ante

Criar séries `_ex_ante` em `diferenciais_juros` sem remover as ex-post existentes:

| Nome da série | Fonte | Observação |
|---|---|---|
| `selic_ex_ante` | Focus Selic EOP 12m (`macro_brasil.expectativas`) | JOIN por data |
| `ipca_ex_ante` | Focus IPCA 12m (`macro_brasil.expectativas`) | JOIN por data |
| `real_br_ex_ante` | `selic_ex_ante − ipca_ex_ante` | calculado no script |
| `ff_ex_ante` | FRED: `FF{M}` futures ou OIS 1y | novo fetch |
| `cpi_ex_ante` | FRED: `MICH` (Michigan Survey) ou `T5YIE` breakeven | novo fetch |
| `real_us_ex_ante` | `ff_ex_ante − cpi_ex_ante` | calculado no script |
| `diferencial_nominal_ex_ante` | `selic_ex_ante − ff_ex_ante` | calculado no script |
| `diferencial_real_ex_ante` | `real_br_ex_ante − real_us_ex_ante` | calculado no script |

Adicionar dois charts novos no relatório: "Diferencial Nominal ex-ante" e "Taxas Reais ex-ante".

#### 1c. CFTC histórico ✓ (feito)

`connectors/cftc.py` agora suporta 2010 → hoje (auto-detecção de coluna de data entre formatos pré/pós-2013). 2006–2009 retornam 404 no servidor do CFTC — não há histórico disponível antes de 2010.

#### 1d. Pendências menores de ETL

- Confirmar SGS 22099/22100 (termos de troca) — descrições exatas
- Mapear sub-itens CEP/CBE do fluxo financeiro (candidatos 24372–24376)
- Reservas brutas: investigar código SGS correto (13127 retorna timeout)

---

### Fase 2 — Histórico ampliado no relatório

**Objetivo:** todos os charts mostrem o máximo de história disponível na base.

- Garantir que todos os scripts de domínio foram rodados com `start="all"` ao menos uma vez
- Verificar cobertura real de cada tabela:

| Tabela | Schema | Cobertura esperada | Status |
|---|---|---|---|
| `diferenciais_juros` | `macro_analytics` | 1995 → hoje | pendente — janela 36m hoje |
| `reer` | `macro_international` | 1994 → hoje | ✓ BIS full history |
| `cot_fx` | `macro_international` | 2010 → hoje | ✓ (2006–2009 indisponíveis no CFTC) |
| `balanco_pagamentos` | `macro_brasil` | 2001 → hoje | ✓ |
| `fluxo_cambial` | `macro_brasil` | 2003 → hoje | ✓ |
| `reservas` | `macro_brasil` | 2004 → hoje | ✓ conceito liquidez |
| `termos_de_troca` | `macro_brasil` | variado | após confirmar descrições SGS 22099/22100 |

- Adicionar no `generate_report.py` um campo `data_range` no JSON por seção (para exibir no tooltip do chart header: "2006 – jun/2026")

---

### Fase 3 — Agente de análise

**Objetivo:** ao rodar o relatório, um agente lê os dados atuais + uma biblioteca de textos selecionados e gera uma narrativa analítica estruturada, incorporada ao HTML ou exportada como documento separado.

#### Arquitetura proposta

```
analytics/cambio/
  generate_report.py    — existente (dados → HTML)
  analyze.py            — novo: dados + bibliography → narrativa
  bibliography/         — novo: PDFs ou .txt de papers/relatórios de referência
    README.md           — lista dos textos e por que foram incluídos
```

#### `analyze.py` — fluxo

1. `_load_context()` — lê `bibliography/` (PDFs via pypdf ou txt direto), constrói string de contexto
2. `_load_snapshot()` — lê tabelas `macro_cambio` e formata como texto tabular (últimas N observações por série)
3. `_build_prompt(context, snapshot)` — monta prompt estruturado: contexto bibliográfico + dados atuais + instruções de análise
4. `_call_claude(prompt)` → `anthropic.Anthropic().messages.create(model="claude-opus-4-8", ...)` → texto de análise
5. `run(output_html, inject=True)` — chama `generate_report.run()` e injeta o texto no HTML como seção "Análise"

#### Dependências novas

```powershell
uv add anthropic          # API Claude
uv add pypdf              # leitura de PDFs da bibliography (opcional)
```

#### Estrutura da bibliografia

O diretório `analytics/cambio/bibliography/` deve conter textos relevantes para análise do BRL. Exemplos de conteúdo útil:
- Framework de análise cambial (determinantes do BRL: carry, risco, termos de troca, fluxo)
- Research sobre posicionamento especulativo e reversão de câmbio
- Estudos BCB/FMI sobre equilíbrio do câmbio real no Brasil
- Notas internas de análise macro da LIS Capital

Cada texto deve ter um cabeçalho indicando fonte, data e relevância. O agente usa esse contexto para calibrar a interpretação dos dados, não para reproduzir o texto.

#### Output esperado

Seção "Análise Macro — BRL" no relatório com:
- Diagnóstico atual (ex: "REER apreciado X% acima da média histórica")
- Fatores dominantes (carry vs. fundamentos vs. posicionamento)
- Riscos e pontos de atenção
- Referências explícitas às séries que embasam cada conclusão
