# Base incremental Bloomberg — CDS soberanos, curva de DI e cupom cambial (FRA), com atualização semanal

**Escopo revisado** (2026-08-04) a partir da proposta original: CDS mantido integralmente; DI reduzido a curva (vértices) + contratos vivos, sem genéricos; cupom cambial reduzido a **apenas FRA** (`GD`, DDI/`EV` fora de escopo), limitado a um horizonte de **~12 meses à frente** — tanto nos contratos vivos quanto nos genéricos. Motivo do corte: o uso inicial é acompanhar a "suavidade"/funcionamento do mercado de câmbio via a ponta curta da curva de cupom cambial, não reconstruir uma série longuíssima. Isso reduz o universo de ~298 séries (proposta original) para **~95-100 séries**, e deve eliminar a necessidade de backfill faseado em vários dias (a confirmar com medição real no Terminal — ver seção de volume abaixo).

Adicionado nesta revisão: **curva de volatilidade implícita USDBRL** (Grupo 6) — insumo para o métrico carry/vol (o mesmo tipo de uso que `cmb_fx_latam`/yfinance já alimenta hoje em `analytics/exchange_rate/models/ppp_equilibrium.py`, mas com vol *implícita* de opções em vez de vol *realizada* de spot). Mesma lógica do corte acima: curva pronta (como os vértices de DI), sem contratos/genéricos por trás, sem necessidade de reconstrução histórica via instrumentos expirados.

## Context

O repo `Automacao-DadosBBG` já tem o acesso genérico à Bloomberg pronto ([bloomberg.py](bloomberg.py): `reference_data`, `historical_data`, `open_session`) e um consumidor de exemplo ([cdi_historico.py](cdi_historico.py)), mas nenhuma base persistente: cada execução refaz o pull inteiro e sobrescreve o CSV. As pastas [cambio/](cambio/) e [fiscal/](fiscal/) estão vazias — a organização por domínio foi planejada e nunca implementada.

Objetivo: montar a **base histórica em CSV organizada por pasta**, com extração **sempre incremental**, atualizada **automaticamente toda segunda às 18:00**. A restrição dominante do desenho continua sendo **não estourar a cota da API da Bloomberg**, mas com o escopo abaixo o risco cai bastante em relação à proposta original — a maior parte do volume da proposta original (genéricos `OD`/`EV`/`GD` completos, 1..45) sai de escopo.

### Volume de dados — o que já foi medido vs. o que falta medir

Ponto de dado = ticker × data × campo. As linhas de CDS e vértices vêm da medição original no Terminal (inalteradas). As linhas de DI contratos vivos e cupom cambial FRA (ambas com escopo novo/reduzido) **ainda precisam ser medidas no Terminal** pela equipe que tem acesso — os números abaixo marcados "estimativa" são extrapolação grosseira a partir de amostras da proposta original, não uma medição, e não devem ser tratados como cota real.

| Grupo | Séries | Campos | Pontos no backfill |
|---|---:|---:|---:|
| CDS soberanos 5Y | 4 | 1 | **21.145** (medido) |
| Vértices `BCSF*` (curva DI, prazo constante) | 25 | 1 | **136.507** (medido) |
| DI contratos vivos (`OD`, cadeia completa) | 45 | 3 | a medir — fazia parte dos 309.543 originais (`OD`+`EV`+`GD` juntos, não discriminado por raiz) |
| Cupom cambial FRA — contratos vivos, **só ~12 meses à frente** | ~11-12 (janela móvel, ver abaixo) | 3 | a medir — universo bem menor que os 44 vivos originais do `GD` |
| Cupom cambial FRA — genéricos, **apenas `GD1`..`GD12`** | 12 | 3 | a medir — amostra da proposta original: `GD1`=4.913 · `GD10`=3.998 pontos, sugerindo algo na casa de **50-60 mil** para os 12 juntos, mas é extrapolação, não medição |
| Curva de vol. implícita USDBRL (ATM, até ~1a) | ~7 (estimativa, ver Grupo 6) | 1 | a medir — nunca verificado no Terminal, nem os mnemonics |

Fora de escopo nesta versão: `EV`/DDI (grupo inteiro), genéricos `OD` (`OD1`..`OD45`), genéricos `GD` além de `GD12`, e qualquer contrato `GD` vencendo depois de ~12 meses.

Duas coisas que já dá para afirmar mesmo sem a medição fina:
1. O corte elimina o maior item de custo da proposta original (genéricos completos, 1,3M de pontos, 74% do backfill). O volume total esperado aqui deve ficar uma ordem de grandeza abaixo do 1,76M original.
2. É plausível que o backfill inteiro caiba num teto único (`--limite-pontos 250000` default) — a confirmar assim que a medição de DI-contratos e GD-bounded estiver feita.

### A janela de "~12 meses à frente" no cupom cambial é móvel, não uma lista fixa

Ao contrário do CDS/vértices/DI-contratos (que são universos estáveis, redescobertos só ocasionalmente), o filtro de 12 meses do cupom cambial **depende da data de execução**: a cada rodada, a lista de contratos `GD` "vivos e dentro de ~12 meses" muda (um vence, sai da janela; o próximo mês entra). Isso é lógica nova, não coberta pelo motor original (que só distinguia vivo/expirado, não "vivo e dentro de um horizonte X"). Ver `series_catalog.py` abaixo.

`GD` nunca tem vencimento em julho (achado da proposta original, confirmado como válido em qualquer ano) — então uma janela de 12 meses corridos normalmente captura **11** contratos `GD`, não 12. Recomendação: usar uma janela de 13 meses (`hoje + ~395 dias`) para garantir cobertura de 12 vencimentos reais, em vez de contar meses corridos.

---

## Especificação das séries

Tudo abaixo (exceto onde indicado) foi **verificado no Terminal** na proposta original (mnemonics resolvidos, campos testados, datas de início lidas de `HISTORY_START_DT` / `FUT_FIRST_TRADE_DT`). Periodicidade **DAILY**, `periodicityAdjustment=ACTUAL`, sem preenchimento de dia não-útil.

### Campos: significado e unidade

| Campo Bloomberg | Coluna no CSV | Significado | Unidade | Aplica-se a |
|---|---|---|---|---|
| `PX_LAST` | `PX_LAST` | Último valor do dia. **Em DI e no FRA de cupom cambial é taxa, não preço** | CDS: bps · DI: % a.a. base 252 · FRA cupom cambial: % a.a. base 360 | todos |
| `PX_VOLUME` | `PX_VOLUME` | Volume negociado no dia | nº de contratos | só futuros/FRA |
| `OPEN_INT` | `OPEN_INT` | Posições em aberto no fim do dia | nº de contratos | só futuros/FRA |

`PX_VOLUME`/`OPEN_INT` **não existem** para CDS nem para os vértices `BCSF*` (retornam `fieldException`) — campos declarados **por grupo**, nunca globalmente.

### Grupo 1 — CDS soberanos 5Y · `data/cds/` · campos: `PX_LAST` · **fase 1**

| Mnemonic Bloomberg | Emissor | Arquivo | Início do histórico | Pontos |
|---|---|---|---|---:|
| `US CDS USD SR 5Y D14 Corp` | United States of America | `US_CDS_USD_SR_5Y_D14.csv` | 2018-08-30 | 1.977 |
| `BRAZIL CDS USD SR 5Y D14 Corp` | Federative Republic of Brazil | `BRAZIL_CDS_USD_SR_5Y_D14.csv` | 2001-10-12 | 6.363 |
| `MEX CDS USD SR 5Y D14 Corp` | United Mexican States | `MEX_CDS_USD_SR_5Y_D14.csv` | 2001-10-12 | 6.370 |
| `COLOM CDS USD SR 5Y D14 Corp` | Republic of Colombia | `COLOM_CDS_USD_SR_5Y_D14.csv` | 2003-01-24 | 6.100 |

Convenção do mnemonic: `<obligor> CDS <moeda> <senioridade> <prazo> <doc clause>`. `SR` = senior unsecured, `D14` = ISDA 2014 Definitions. Yellow key **`Corp`**. Padronizado em **USD** (inclui `US CDS USD`, série mais curta — desde 2018 — mas comparável).

### Grupo 2 — DI vértices de prazo constante (a curva) · `data/di/vertices/` · campos: `PX_LAST` · **fase 1**

Curva DI interpolada em prazo fixo em **dias úteis (DY)**, sem roll nem vencimento — é a série contínua que já representa a curva pronta, sem interpolação por nossa conta. Nome Bloomberg: `BRL SW BMF DI FUT <n>DY`. Yellow key **`Curncy`**. **A letra não é sequencial: não existe `BCSFO`, e há um salto de 294DY (`N`) para 504DY (`P`)**.

| Mnemonic | Prazo | Início | | Mnemonic | Prazo | Início |
|---|---:|---|---|---|---:|---|
| `BCSFAPDV Curncy` | 21 DY | 2000-08-30 | | `BCSFNPDV Curncy` | 294 DY | 2000-09-04 |
| `BCSFBPDV Curncy` | 42 DY | 2000-08-28 | | `BCSFPPDV Curncy` | 504 DY | 2002-06-05 |
| `BCSFCPDV Curncy` | 63 DY | 2000-08-30 | | `BCSFQPDV Curncy` | 756 DY | 2002-06-05 |
| `BCSFDPDV Curncy` | 84 DY | 2000-09-04 | | `BCSFRPDV Curncy` | 1008 DY | 2014-02-13 |
| `BCSFEPDV Curncy` | 105 DY | 2000-08-28 | | `BCSFSPDV Curncy` | 1260 DY | 2014-02-13 |
| `BCSFFPDV Curncy` | 126 DY | 2000-08-29 | | `BCSFTPDV Curncy` | 1512 DY | 2014-02-13 |
| `BCSFGPDV Curncy` | 147 DY | 2000-08-29 | | `BCSFUPDV Curncy` | 1764 DY | 2014-02-12 |
| `BCSFHPDV Curncy` | 168 DY | 2000-08-28 | | `BCSFVPDV Curncy` | 2016 DY | 2014-02-13 |
| `BCSFIPDV Curncy` | 189 DY | 2000-10-02 | | `BCSFWPDV Curncy` | 2268 DY | 2014-02-12 |
| `BCSFJPDV Curncy` | 210 DY | 2000-09-04 | | `BCSFXPDV Curncy` | 2520 DY | 2014-02-12 |
| `BCSFKPDV Curncy` | 231 DY | 2000-08-28 | | `BCSFYPDV Curncy` | 2772 DY | 2014-02-12 |
| `BCSFLPDV Curncy` | 252 DY | 2000-10-03 | | `BCSFZPDV Curncy` | 3024 DY | 2014-02-12 |
| `BCSFMPDV Curncy` | 273 DY | 2000-09-11 | | | | |

Arquivo = mnemonic sem yellow key (`BCSFLPDV.csv`). 25 séries, 136.507 pontos. Sem alteração de escopo — é a curva completa até ~12 anos (3024 DY), não só até 12 meses (o corte de horizonte pedido é específico do cupom cambial, ver Contexto acima).

### Grupo 3 — DI contratos por vencimento (cadeia viva) · `data/di/contratos/` · campos: `PX_LAST`, `PX_VOLUME`, `OPEN_INT` · **fase 2**

Descoberto por `FUT_CHAIN` no contrato ativo `ODA Comdty`. **Só vivos** — expirados fora de escopo. Sem alteração de escopo em relação à proposta original: cadeia completa, sem limite de horizonte (a limitação de ~12 meses é só para o cupom cambial).

| Raiz | Yellow key | Contrato ativo | Instrumento | Vivos | Faixa de vencimento | 1º trade mais antigo |
|---|---|---|---|---:|---|---|
| `OD` | `Comdty` | `ODA Comdty` | DI de 1 dia (B3) — taxa pré | 45 | 2026-08-31 → 2040-12-28 | 2014-06-03 |

Mnemonic = `<raiz><mês><ano>` com o código de mês da Bloomberg — `F`jan `G`fev `H`mar `J`abr `K`mai `M`jun `N`jul `Q`ago `U`set `V`out `X`nov `Z`dez. Exemplo: `ODF27 Comdty` (DI jan/27). Arquivo = `ODF27.csv`.

**`OD` não entra com genéricos nesta versão** — a curva já vem pronta pelos vértices (Grupo 2); os contratos vivos aqui servem para acompanhar liquidez (`PX_VOLUME`/`OPEN_INT`) por vencimento, não para reconstruir a curva.

### Grupo 4 — Cupom cambial FRA · contratos vivos, **janela ~12 meses** · `data/cupom_cambial/fra_contratos/` · campos: `PX_LAST`, `PX_VOLUME`, `OPEN_INT` · **fase 3**

Root `GD` (FRA de cupom cambial), yellow key `Curncy`. Descoberto por `FUT_CHAIN` em `GDA Curncy` (44 vivos na proposta original, 2026-08-27 → 2040-11-28), **filtrado** a `LAST_TRADEABLE_DT <= hoje + ~395 dias`. `GD` não tem vencimento em julho — a janela normalmente resulta em ~11 contratos, não 12.

Mnemonic = `<raiz><mês><ano>`, mesmo código de mês do Grupo 3. Exemplo: `GDZ26 Curncy` (FRA dez/26). Arquivo = `GDZ26.csv`.

**Por que FRA e não DDI**: decisão do usuário — cupom cambial nesta base vem só do FRA (`GD`), não do DDI (`EV`). O FRA expressa taxas forward-forward (ex.: taxa implícita entre o mês 3 e o mês 6), diferente do DDI, que é a taxa acumulada spot-a-vencimento. Isso significa que a "curva" aqui é uma sequência de taxas a termo encadeadas, não uma curva spot ponto-a-ponto como a de DI — vale ter isso em mente na hora de interpretar/plotar.

### Grupo 5 — Cupom cambial FRA · genéricos `GD1`..`GD12` · `data/cupom_cambial/fra_genericos/` · campos: `PX_LAST`, `PX_VOLUME`, `OPEN_INT` · **fase 3**

`GD1` = 1º vencimento em aberto, `GD2` = 2º, ..., até `GD12`. Ao contrário da proposta original (que ia até `GD45`), esta versão **para em `GD12`** — o suficiente para cobrir a janela de ~12 meses à frente com folga, já que `GD` pula julho.

Start no catálogo = `20030101` (a Bloomberg trunca no 1º ponto real: `GD1` começa em 2003-10-29 na proposta original — usar `FUT_FIRST_TRADE_DT` aqui devolveria a data do contrato subjacente atual, não o início da série, mesma armadilha documentada no grupo de genéricos original).

⚠️ Mesmo dentro de `GD1`..`GD12` (universo mais líquido, ponta curta da curva), aplicar a mesma trava de série vazia (`sem_dados`) usada na proposta original para `GD45` — não custa nada verificar, e a ponta curta costuma ser a mais líquida mas não é garantia absoluta.

### Grupo 6 — Curva de volatilidade implícita USDBRL (ATM) · `data/cambio/vol/` · campos: `PX_LAST` · **fase 1**

⚠️ **Diferente de todos os grupos acima, isto NÃO foi verificado no Terminal ainda** — mnemonics, campos e datas de início abaixo são a convenção-padrão da Bloomberg para curvas de vol implícita de câmbio, não uma medição. Confirmar tudo isto no Terminal antes de codificar, do mesmo jeito que os outros grupos foram confirmados na proposta original.

Convenção usual da Bloomberg para vol ATM (at-the-money) de um par de câmbio: `<par>V<tenor> Curncy`, yellow key `Curncy`, campo `PX_LAST` (nível de vol implícita, em % a.a.). Para USDBRL, o padrão esperado é `USDBRLV<tenor> Curncy`.

| Mnemonic esperado | Tenor | Uso no carry/vol |
|---|---|---|
| `USDBRLV1W Curncy` | 1 semana | |
| `USDBRLV1M Curncy` | 1 mês | ponta curta, mais reativa a eventos |
| `USDBRLV2M Curncy` | 2 meses | |
| `USDBRLV3M Curncy` | 3 meses | tenor mais comum como referência de "vol de curto prazo" |
| `USDBRLV6M Curncy` | 6 meses | |
| `USDBRLV9M Curncy` | 9 meses | |
| `USDBRLV1Y Curncy` | 12 meses | teto do horizonte desta base, mesmo critério de ~12m usado no cupom cambial |

Arquivo = mnemonic sem yellow key (`USDBRLV3M.csv`). **Só ATM nesta versão** — sem risk reversal nem butterfly (skew), que ficam de fora salvo pedido explícito; se quiser adicionar depois, são mnemonics irmãos (`USDBRL25R1M Curncy`, `USDBRL25B1M Curncy` etc., convenção a confirmar também).

Sem contratos/genéricos por trás — é uma curva cotada diretamente pelo mercado de opções (como os vértices de DI), então não há `PX_VOLUME`/`OPEN_INT` nem cadeia viva a descobrir via `FUT_CHAIN`. Início do histórico: **não medido** — verificar `HISTORY_START_DT` de cada tenor no Terminal antes do backfill.

**Uso pretendido**: insumo de vol *implícita* (forward-looking, precificada pelo mercado de opções) para o métrico carry/vol, complementar à vol *realizada* que `cmb_fx_latam` (yfinance, spot histórico) já alimenta em `analytics/exchange_rate/models/ppp_equilibrium.py`. A integração desse dado ao modelo é um passo separado, fora do escopo deste plano (que cobre só a extração do lado Bloomberg).

### Resumo do backfill por fase

| Fase | Grupos | Séries | Pontos |
|---:|---|---:|---:|
| 1 | CDS + vértices DI + vol. implícita USDBRL | ~36 | 157.652 (CDS+vértices, medido) + vol. a medir |
| 2 | DI contratos vivos (`OD`) | 45 | a medir |
| 3 | Cupom cambial FRA (contratos ~12m + genéricos `GD1`-`GD12`) | ~23-24 | a medir (estimativa grosseira: 50-90 mil) |
| | **Total** | **~104-105** | **provavelmente < 500 mil — a confirmar** |

Com os tetos default (250 mil/rodada, 500 mil/dia), é plausível que o backfill inteiro caiba em **1-2 rodadas**, não os ~4 dias da proposta original. Confirmar assim que a fase 2 e 3 forem medidas no Terminal (mesma metodologia da proposta original: `HISTORY_START_DT`/`FUT_FIRST_TRADE_DT` por série, ou `--dry-run` do motor já implementado, ver Verificação item 2).

### Armadilhas descobertas na proposta original que continuam valendo

- `MEX/BRAZIL/COLOM CDS EUR ...` **não existem**; `BRAZIL CDS EUR SR 5Y D14 Curncy` resolve por fuzzy match para um ETF de equity. O catálogo precisa **validar `NAME`/`SECURITY_TYP`**, não confiar em "não deu erro".
- `FUT_CHAIN` retorna os vencimentos vivos — escopo desta entrega. Caminho para expirados (`INCLUDE_EXPIRED_CONTRACTS=Y`) permanece **fora de escopo**, não implementado nesta versão (na proposta original estava implementado e desligado; como o motor muda um pouco de qualquer forma nesta versão, decidir depois se vale portar esse caminho).
- Tickers antigos têm espaço interno (`ODU4 94 Comdty`) → saneamento do nome de arquivo entra desde já.
- `PX_VOLUME`/`OPEN_INT` **não se aplicam** aos vértices `BCSF*` → campos por classe, não globais.
- **Segunda 18:00 é durante/logo após o fechamento da B3**: `PX_VOLUME`/`OPEN_INT` do próprio dia saem incompletos e são revisados depois. Lookback de **10 dias corridos** (não 7) garante que a rodada seguinte recaptura e corrige.

---

## Arquitetura

Código plano na raiz (segue o estilo atual do repo); dados isolados em `data/`.

```
Automacao-DadosBBG/
├── PLANO.md                este plano, versionado no repo
├── bloomberg.py            (existente — reutilizar, NÃO modificar)
├── config.py               (existente — usar bloomberg_endpoint())
├── bbg_series.py           NOVO — motor incremental + ledger de consumo
├── series_catalog.py       NOVO — catálogo, descoberta, janela móvel e validação
├── update_series.py        NOVO — CLI
├── atualizar.bat           NOVO — wrapper do Task Scheduler
├── agendar_semanal.ps1     NOVO — registra a tarefa semanal (rodar 1x)
└── data/
    ├── _registry.csv                      metadados dos tickers descobertos
    ├── _usage.csv                         ledger de consumo da API
    ├── _logs/2026-08-04_1800.log          log por rodada
    ├── cds/BRAZIL_CDS_USD_SR_5Y_D14.csv   ...
    ├── di/{contratos,vertices}/ODF27.csv, BCSFLPDV.csv
    ├── cupom_cambial/{fra_contratos,fra_genericos}/GDZ26.csv, GD1.csv
    └── cambio/vol/USDBRLV3M.csv, USDBRLV1Y.csv, ...
```

**Formato do CSV** (igual ao de `cdi_historico.to_csv`): delimitador `;`, encoding `utf-8-sig`, data ISO `YYYY-MM-DD`, decimal `.`, ordenado por data crescente.

```
data;PX_LAST;PX_VOLUME;OPEN_INT
2026-07-31;13.798;51893;6800482
```

---

## Implementação

### 1. `bbg_series.py` — motor incremental + controle de cota

Núcleo reutilizável para qualquer série futura (câmbio, fiscal, etc.). Sem mudanças de desenho em relação à proposta original — a redução de escopo não muda o motor, só o que é passado a ele.

**Persistência**
- `SeriesSpec` (dataclass): `ticker`, `path`, `fields`, `start`, `fase` (prioridade no backfill).
- `read_watermark(path) -> date | None` — última data gravada lendo **só a cauda** do arquivo (`seek` do fim). `None` se não existe.
- `upsert(path, fields, new_rows) -> (n_novas, n_revisadas)` — merge por data, **linha nova vence a antiga**, grava ordenado. Resolve a revisão de `OPEN_INT`/`PX_VOLUME` sem duplicar datas.

**Decisão incremental** — `plan_fetch(spec, lookback_days, full)`:
- arquivo ausente ou `full=True` → `spec.start` (carga completa daquela série)
- senão → `watermark - lookback_days` (default **10 dias corridos**)
- `None` (nada a fazer) se `watermark >= último dia útil`

**Controle de cota**:
- `estimate_points(specs, start, end)` — dias úteis na janela × nº de campos × nº de securities, **antes** de enviar a request.
- `Ledger` sobre `data/_usage.csv` (`timestamp;modo;grupo;securities;campos;pontos_estimados;pontos_reais`): `spent_today()`, `spent_this_month()`, `record(...)` com os pontos **reais** (`len(series) × n_fields`) após a resposta.
- Portão em duas camadas, checado **antes de cada lote**: `--limite-pontos` (teto da rodada) e `--limite-diario` (teto acumulado no dia, somando o ledger). Ao bater o teto, a rodada **para de enfileirar e sai com aviso "retome com --backfill"**.
- Defaults conservadores (`250_000` por rodada, `500_000` por dia) — com o escopo reduzido, é plausível que a fase 2+3 combinadas caibam num teto só; a confirmar com a medição real.
- A rodada **semanal** (bem menor que os ~5 mil da proposta original, já que o universo caiu de 298 para ~98 séries) nunca encosta em teto nenhum.

**Execução** — `run(specs, *, session, lookback_days=10, full=False, dry_run=False, chunk=25, limite_pontos, limite_diario)`:
- agrupa specs por `(tuple(fields), start_efetivo)` e fatia em lotes de **25 securities** → uma `historical_data` por lote, na **mesma sessão** (`open_session()`) durante toda a rodada
- descarta specs sem trabalho *antes* de montar o lote
- por ticker: erro de security → registra e continua; série vazia → "sem dados novos"
- retorna resumo por spec: `(ticker, n_novas, n_revisadas, pontos, erro)`

### 2. `series_catalog.py` — catálogo, descoberta, janela móvel e validação

Constantes declarativas no topo:

- `CDS` — os 4 mnemonics do Grupo 1, `["PX_LAST"]`, `data/cds`, start `19980101`, fase 1.
- `VERTICES` — os 25 do Grupo 2, `["PX_LAST"]`, `data/di/vertices`, start `20000101`, fase 1.
- `DI_CONTRATOS` — raiz `OD`, `["PX_LAST","PX_VOLUME","OPEN_INT"]`, `data/di/contratos`, start `19940101`, fase 2, **sem genéricos**.
- `FRA_CONTRATOS` — raiz `GD`, mesmos campos, `data/cupom_cambial/fra_contratos`, fase 3, **com filtro de janela** (ver abaixo).
- `FRA_GENERICOS` — `GD1`..`GD12` (fixo, sem sondagem), mesmos campos, `data/cupom_cambial/fra_genericos`, start `20030101`, fase 3.
- `FX_VOL` — os 7 mnemonics do Grupo 6 (`USDBRLV1W`..`USDBRLV1Y Curncy`, a confirmar no Terminal), `["PX_LAST"]`, `data/cambio/vol`, start a definir após medição, fase 1. Sem cadeia viva nem genéricos — lista fixa, sem `discover()` além da validação de `NAME`/`CRNCY`.

- `discover(session, horizonte_meses=None)`:
  - `reference_data([ODA, GDA], ["FUT_CHAIN"])` → vencimentos vivos.
  - Para `GD` (e só para `GD`, dado o parâmetro `horizonte_meses`): filtra o resultado do `FUT_CHAIN` a `LAST_TRADEABLE_DT <= run_date + horizonte_meses*30 + margem`. **Isso é lógica nova** — a proposta original só tinha "vivo/expirado", nunca "vivo dentro de um horizonte X". Recalculado a cada rodada (não é uma lista fixa gravada uma vez).
  - `OD` não é filtrado por horizonte — cadeia completa, como no Grupo 3.
  - genéricos `GD1`..`GD12` são fixos por constante, **sem sondagem** (a proposta original sondava até 45 com `reference_data(..., ["NAME"])`; aqui não precisa, já que o número é fixo e pequeno — mas ainda vale rodar a mesma sondagem por `NAME` começando com `"Generic"` como guarda de sanidade, é barato).
  - **marca `sem_dados=1`** no registry para qualquer série que resolva mas retorne 0 pontos, e exclui das rodadas seguintes (mesma trava da proposta original, agora aplicada a um universo menor).
  - busca `NAME`, `LAST_TRADEABLE_DT`, `HISTORY_START_DT` e `FUT_FIRST_TRADE_DT`, grava `data/_registry.csv`. Descoberta é **barata e cacheada**: só roda com `--descobrir`, exceto o filtro de janela do `GD`, que precisa ser **reavaliado a cada rodada semanal** mesmo sem `--descobrir` (um contrato pode sair da janela de 12 meses entre uma segunda e outra sem que a cadeia em si tenha mudado).
- `ticker_to_filename(ticker)` — remove yellow key, troca espaço e `/` por `_`.
- `validate(snapshot)` — guard contra fuzzy match: exige `SECURITY_TYP == "CREDIT DEFAULT SWAP"` para CDS e `NAME` começando pelo mnemonic pedido; para futuros/FRA, `CRNCY` esperada (`BRL` em `OD`, `USD` em `GD`). Divergência → aborta com mensagem clara.
- **Regra de expiração**: pula o contrato se `LAST_TRADEABLE_DT` já passou **e** o watermark do CSV `>= LAST_TRADEABLE_DT`. Aplica-se a `OD` (sempre) e a `GD` (adicionalmente ao filtro de janela — um `GD` pode sair de escopo tanto por expirar quanto por sair da janela de 12 meses).
- **Fases** — `--fase N` (cumulativo) filtra as specs conforme a tabela *Resumo do backfill por fase*.

### 3. `update_series.py` — CLI

```
python update_series.py                        # rodada incremental (tudo o que já existe)
python update_series.py --grupo cds
python update_series.py --grupo di
python update_series.py --grupo cupom_cambial
python update_series.py --grupo cambio          # curva de vol. implícita USDBRL
python update_series.py --descobrir             # redescobre cadeia/genéricos, reescreve o registry
python update_series.py --backfill --fase 1     # carga inicial faseada, respeita os tetos
python update_series.py --backfill              # continua de onde parou (fases 1-3)
python update_series.py --horizonte-meses 12    # tamanho da janela do cupom cambial FRA (default 12)
python update_series.py --limite-pontos 500000 --limite-diario 1000000
python update_series.py --lookback 30
python update_series.py --full                  # ignora watermark, refaz do zero (usar com cuidado)
python update_series.py --dry-run               # só estima o consumo, não escreve nada
python update_series.py --agendado               # modo Task Scheduler (ver abaixo)
```

Resumo final por grupo: séries processadas, linhas novas, linhas revisadas, séries puladas (expiradas / fora da janela / já atualizadas), **pontos consumidos na rodada e no dia**, erros.

**Exit codes**: `0` sucesso · `1` erro de security em alguma série · `2` teto de cota atingido (backfill incompleto, retomável) · `3` Bloomberg indisponível → dispara a retentativa.

`--agendado` faz, nesta ordem: (1) *health check* — abre sessão e faz um `reference_data` de 1 ticker; se falhar, loga e sai com **`3`** sem consumir cota; (2) reavalia a janela móvel do `GD` (mesmo sem `--descobrir`); (3) rodada incremental normal; (4) grava `data/_logs/<data>_<hora>.log`.

### 4. `atualizar.bat` + `agendar_semanal.ps1` — agendamento semanal

Sem mudanças em relação à proposta original.

`atualizar.bat` — chama `python update_series.py --agendado` a partir da raiz do repo e **propaga o exit code** (`exit /b %ERRORLEVEL%`).

`agendar_semanal.ps1` — registra a tarefa uma única vez via `Register-ScheduledTask`:
- `New-ScheduledTaskTrigger -Weekly -DaysOfWeek Monday -At 18:00`
- `New-ScheduledTaskSettingsSet -RestartInterval (New-TimeSpan -Hours 2) -RestartCount 3`
- `-StartWhenAvailable`
- `-MultipleInstances IgnoreNew`
- `-LogonType Interactive` (sessão do usuário, **não SYSTEM**) — obrigatório para alcançar o Terminal em `localhost:8194`
- `-AllowStartIfOnBatteries -DontStopIfGoingOnBatteries`

Registrar a tarefa **altera o agendador do Windows** — confirmar antes de executar; o script imprime o comando de remoção (`Unregister-ScheduledTask`).

### Ordem de execução

0. **Salvar este plano como `PLANO.md` na raiz do repo**.
1. `bbg_series.py` (motor, upsert, ledger) — testável sem Bloomberg, com CSV sintético. Sem mudanças em relação à proposta original.
2. `series_catalog.py` (catálogo, descoberta, **filtro de janela do `GD`**, validação) — a única peça com lógica genuinamente nova.
3. `update_series.py` (CLI, com o novo `--horizonte-meses`).
4. **Medir no Terminal** os pontos reais de `DI_CONTRATOS` (`OD`, 45 séries) e `FRA_CONTRATOS`+`FRA_GENERICOS` (universo bounded) antes de rodar o backfill de verdade — os números desta versão do plano são estimativa, ao contrário do Grupo 1/2.
5. `--descobrir`, depois `--backfill --fase 1` (157.652, medido), `--fase 2` (`OD`, a medir) e `--fase 3` (cupom cambial FRA bounded, a medir) — provavelmente 1-2 rodadas no total, a confirmar.
6. `atualizar.bat` + `agendar_semanal.ps1`, com a tarefa registrada só depois de uma rodada manual bem-sucedida.

---

## Verificação

1. **Motor isolado, sem Bloomberg** — CSV temporário; `upsert` com linhas sobrepostas e novas: data repetida é **substituída** (não duplicada), ordem por data mantida, `read_watermark` devolve a última data.
2. **Estimativa antes de gastar** — `--dry-run --backfill` imprime os pontos estimados por fase e **não cria nenhum arquivo** em `data/`. A fase 1 deve reproduzir 157.652; fases 2/3 dão a medição real que falta nesta versão do plano.
3. **CDS ponta a ponta** — `--grupo cds`: 4 CSVs em `data/cds/`, 1ª data batendo com a tabela (Brasil 2001-10-12, US 2018-08-30).
4. **Idempotência — o requisito central** — rodar `--grupo cds` de novo imediatamente: **0 linhas novas**.
5. **Revisão** — apagar à mão as 3 últimas linhas de um CSV de contrato DI e rodar de novo: as 3 voltam, sem duplicar data.
6. **Teto de cota** — rodar `--backfill --limite-pontos 5000`: precisa parar cedo, sair com **exit code 2**, registrar o consumido em `data/_usage.csv`, e a rodada seguinte deve **continuar de onde parou**.
7. **Série vazia** — qualquer série de `GD1`..`GD12` ou dos contratos `GD` bounded que retorne 0 pontos deve ser marcada `sem_dados=1` na 1ª rodada e **não ser consultada** na 2ª.
8. **Janela móvel do `GD` — teste específico desta versão** — rodar `--descobrir` com `--horizonte-meses 12` e conferir que a lista de `FRA_CONTRATOS` tem só vencimentos dentro da janela (nenhum além de ~13 meses à frente); simular avanço de um mês (ou usar uma data futura sintética) e conferir que o contrato mais próximo do vencimento **sai** da lista sem erro.
9. **Custo real da rodada semanal** — depois do backfill, uma rodada incremental precisa reportar um número pequeno de pontos (ordem de grandeza a definir após medição, mas deve ser << o volume do backfill). Se vier muito maior, o watermark não está sendo respeitado.
10. **Expiração** — conferir no log que a cadeia `OD`/`GD` descoberta traz só vencimentos vivos e, no `GD`, só dentro da janela.
11. **Guard do fuzzy match** — `validate` contra `BRAZIL CDS EUR SR 5Y D14 Curncy` precisa **falhar**, não gravar.
12. **Health check e retentativa** — rodar `--agendado` e conferir exit `0` com o Terminal aberto. Para o caminho de falha: apontar `BLOOMBERG_PORT` para uma porta morta no `.env` e confirmar exit **`3`** sem consumo de cota. Depois, `Start-ScheduledTask` para validar a tarefa registrada de ponta a ponta.
13. **Conferência no Terminal** — comparar 2–3 pontos de `data/di/contratos/ODF27.csv` com `ODF27 Comdty GP <GO>`, e de um `GDxx Curncy` dentro da janela com o Terminal.
14. **Mnemonics da vol. USDBRL — verificação obrigatória antes de codificar** — confirmar no Terminal que `USDBRLV1M Curncy` (e os demais tenores do Grupo 6) resolvem para o instrumento certo (`NAME`/`CRNCY` batendo, mesmo guard de fuzzy match do item 11) e que retornam `PX_LAST` de fato — ao contrário dos outros grupos, estes mnemonics nunca foram testados no Terminal, só assumidos pela convenção padrão da Bloomberg.

## Observações

- **`.gitignore` ignora `*.csv`** — nada de `data/` seria versionado. Decidir depois se `data/` entra no versionamento ou fica só em disco/backup.
- **Como esses CSVs chegam ao `Sistema de dados`**: este plano cobre só o lado do `Automacao-DadosBBG` (máquina com acesso Bloomberg). Ainda não há um mecanismo definido para os CSVs atravessarem para este repo/banco (`macro_brasil`/`macro_international`) — vale decidir isso como próximo passo, seguindo o padrão de `connectors/`/`domain/db/` já usado aqui.
- **Inconsistência pré-existente:** [cdi_historico.py](cdi_historico.py) grava com `;` e o `cdi_full.csv` da raiz está com `,`. A base nova padroniza `;`. Migrar `cdi_full.csv` está **fora deste escopo**.
- `BMFXSPFT Index` (casado dólar spot/futuro, desde 2016) apareceu na busca original e é vizinho natural do cupom cambial, mas **não foi pedido** — fica de fora.
- **DDI (`EV`) fica fora desta versão por decisão explícita** — se no futuro fizer sentido ter também a taxa spot de cupom cambial (não só as forward-forward do FRA) como âncora da ponta curta, `EV` é candidato natural a reentrar no catálogo; o motor já suporta adicionar uma raiz nova sem mudança estrutural.
- **Genéricos `OD` (DI) ficam fora** — a curva de DI já vem pronta pelos vértices; se um dia for preciso comparar a curva "oficial" da Bloomberg (vértices) com uma reconstrução própria a partir dos contratos, os genéricos `OD` voltariam a fazer sentido.
- Os tetos default (250 mil/rodada, 500 mil/dia) continuam conservadores; ajustar depois que `data/_usage.csv` tiver 2-3 rodadas de dado real.
- **Contratos expirados** seguem fora de escopo em ambas as versões do plano.
- **Vol. implícita USDBRL (Grupo 6) é o único grupo não verificado no Terminal** nesta versão do plano — todo o resto herda a medição/verificação já feita na proposta original. Tratar os mnemonics `USDBRLV*` como hipótese a confirmar, não como fato, até a checagem do item 14 da Verificação.
- **Risk reversal / butterfly (skew) do USDBRL** ficaram de fora por ora — só a vol ATM entrou. Se o carry/vol precisar de assimetria da distribuição (não só o nível de vol), esses mnemonics entram depois, mesma lógica de "candidato natural a reentrar" usada para `EV`/DDI e genéricos `OD` acima.
