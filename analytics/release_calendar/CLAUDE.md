# analytics/release_calendar/ — Calendário de Divulgações

Self-contained HTML report showing when Brazilian macro data is expected to be released for the rest
of 2026 — a forward-looking calendar, not a historical-values report like its `analytics/` siblings.
Same `/*REPORT_DATA*/` marker-substitution pattern (`analytics.report_structure.builder.render_report()`),
but the data source is a local YAML file, not MySQL — see
[`domain/release_calendar/CLAUDE.md`](../../domain/release_calendar/CLAUDE.md) for the schema and how
it was researched.

## Generate

```powershell
uv run python -c "from analytics.release_calendar.generate_report import run; run()"
# Output: reports/release_calendar.html
```

No DB connection needed — `generate_report.py` only reads `domain/release_calendar/calendar_2026.yaml`.
Re-run whenever that file is updated (new dates confirmed, next year's calendar added).

**Year rollover:** two things here are hardcoded to 2026 and will silently show the wrong year —
`_YAML_PATH` ([generate_report.py:24](generate_report.py#L24)) and the literal period label `Ago–Dez 2026`
([report.html:116](report.html#L116), plus the research-date note at line 171). Both are listed as steps in
[`domain/release_calendar/ROLLOVER.md`](../../domain/release_calendar/ROLLOVER.md) — read that before the
turn of the year; the recommended path (extend the window on the existing YAML rather than creating
`calendar_2027.yaml`) avoids needing to touch `_YAML_PATH` at all.

The BCB dates in that YAML are refreshed from BCB's own ICS feeds by
[`domain/release_calendar/update_calendar.py`](../../domain/release_calendar/CLAUDE.md#update_calendarpy).
Usual sequence — nothing chains them automatically:

```powershell
uv run python -m domain.release_calendar.update_calendar          # ve o drift
uv run python -m domain.release_calendar.update_calendar --write  # aplica no YAML
uv run python -c "from analytics.release_calendar.generate_report import run; run()"
```

## Update button + `serve.py` (2026-08-17)

Each release row has an **Atualizar** column that runs that release's ETL. A self-contained HTML file
can't execute Python, so one button covers two modes:

```powershell
uv run python analytics/release_calendar/serve.py          # modo servido: o botão roda o ETL
uv run python analytics/release_calendar/serve.py --port 9000 --no-browser
```

Or double-click [`jobs/abrir_calendario.bat`](../../jobs/abrir_calendario.bat) — same thing
without the terminal, added because "do I have to type this every time?" is the obvious first
reaction. **The served page must be reached at `127.0.0.1:8765`**; double-clicking
`reports/release_calendar.html` yields file mode even while the server runs, since a `file://` page
can't call a localhost origin. That confusion has already happened once — the report's own mode badge
("modo arquivo" / "servido") exists so the answer is visible on the page instead of needing to be
explained.

- **Servido** — `serve.py` (stdlib `http.server`, no new dependency) serves the report from
  `http://127.0.0.1:8765` and exposes `GET /api/ping`, `GET /api/status`, `POST /api/run`. Clicking
  posts a group slug, the ETL runs, and the table re-renders from a fresh `/api/status` so **every row
  of that group** updates, not just the one clicked.
- **Arquivo** — opened as `file://` or emailed, the ping fails and the same button copies
  `uv run python jobs/update_db.py --group <slug>` to the clipboard. A shared report has no dead
  controls and no way to run anything on the recipient's machine. (Clipboard API needs a secure
  context, which `file://` isn't — hence the `execCommand` fallback, and a last resort that just
  displays the command to copy by hand.)

**Dois `serve.py` na mesma porta, e o VELHO é quem responde (2026-09-23).** No Windows o
`allow_reuse_address` do `HTTPServer` vem ligado, então um segundo processo dá bind na 8765 **sem
erro nenhum** — em Linux falharia. Medido: um servidor das 13:13 e outro das 15:41 escutando
juntos, e a aba mostrando `desatualizado` onde a linha de comando dizia `não dá para conferir`,
porque o processo antigo tinha a versão antiga do `status.py` em memória. **Parece defeito do
relatório e é um processo esquecido** — e o caminho que produz isso é o mais natural de todos: um
duplo clique a mais no `abrir_calendario.bat` com o servidor já no ar.

`ja_servindo(port)` agora é consultado antes do bind: se algo responde, o script **não sobe um
segundo**, abre o browser no que já existe e avisa que aquele processo pode estar com código
antigo (a saída é fechar a janela dele e rodar de novo). Coberto por `tests/test_serve_calendar.py`.
Se a aba e o `status.py` discordarem, esta é a primeira coisa a checar:
`netstat -ano | findstr :8765` — tem de haver **uma** linha `LISTENING`.

Four row states, from the release date plus `sync.py`'s verdict for the group:

| State | Shown | When |
|---|---|---|
| future | dimmed `—` | release date (or `date_end`) hasn't passed |
| late | **orange button** | released, and some table is behind → the only attention-grabbing state |
| ok | `✓ em dia` | released, data present |
| unknown | neutral button | released, but no verdict possible (file mode, DB down, or a group with no datable period like Copom/FOMC) |
| — | `sem tabela` | group feeds no table (`bcb_copom_ata`) — never offers a button |

**Security, and why each piece:** binds `127.0.0.1` only; the POST takes a **group slug and resolves
scripts through the YAML** — it never accepts a module name, path, or command from the page, and an
unknown slug is a 400; there is no shell anywhere in the path; and the `Host` header is checked, without
which any website open in the same browser could point a domain at `127.0.0.1` and fire POSTs (DNS
rebinding). All five are covered by `tests/test_serve_calendar.py`.

The slug→script resolution is [`domain/db/registry.py`](../../domain/db/CLAUDE.md) via
`jobs/update_db.py --group`; nothing about which script writes which table lives in this folder.

## Architecture

- `generate_report.py` — `_load_groups()` parses the YAML; `_flatten_entries()` denormalizes each
  group's `entries` into one flat list with institution/name/tables copied onto every row (what
  `report.html`'s table and stat cards consume directly, no lookup back into `groups` needed);
  `_recurring_groups()` pulls out groups with no dated `entries`. **Since 2026-08-17 that returns an
  empty list**: `bcb_focus` was the only member and now carries 19 itemized dates (BCB's own ICS feed
  shifts three of them off Monday for holidays, which a bare "every Monday" rule got wrong). The
  recurring strip auto-hides when empty (`report.html` checks `REPORT_DATA.recurring.length`), so no
  code change was needed — but the code path is now dormant rather than dead, and would light up again
  if a future group is added as a cadence rule without dates.
- `report.html` — uma barra de recorte com quatro `<select>` (País, Fonte, Divulgação, Mês) **dentro do
  card da lista, encostada na tabela**, e a tabela agrupada por semana ou por mês conforme o recorte.
  Todas as opções são computadas do que existe no YAML, nunca hardcoded, então o YAML de um ano futuro
  funciona sem mudança. **Sem gráfico** — a "Linha do Tempo" em Plotly saiu em 2026-08 a pedido do
  usuário, e o Plotly não é mais carregado. **Sem stat cards** — os três saíram em 2026-09-22 (ver a
  seção abaixo); o que sobrou deles é a linha de contagem ao lado do título.

## Data map

| Element | Source |
|---|---|
| Table, stat cards | `domain/release_calendar/calendar_2026.yaml`'s `groups[].entries[]`, flattened |
| Recurring-releases strip | `groups[]` with no `entries` list — **empty since 2026-08-17**, strip hidden |

No MySQL table is read by this report — see the parent `domain/release_calendar/` folder for why the
underlying data lives in a YAML file instead of the database (release dates are provenance/timing
metadata, not a time series with a natural DB row per observation, and change only a few times a year).

## Gotchas

- **Institution color mapping is hardcoded in `report.html`** (`INSTITUTION_COLORS`) — used for the
  table's institution badge only now (was also used by the removed timeline). If a 6th institution is
  ever added to the YAML, add its color there too or it falls back to `--muted` gray.
- **`date`/`date_end` window entries** (used for `confirmed: false` estimates) only render in the table
  now, as `"DD/MM – DD/MM"` in the date column — there's no separate window visualization since the
  timeline was removed.
- **No browser has visually confirmed this report** — same caveat as every other report in this
  project (no browser available in this sandbox). Open `reports/release_calendar.html` before trusting
  the filter/table interaction feel.

## No longer purely forward-looking (2026-08-17)

The YAML was backfilled with the 10 BCB groups' **past** releases (May–Aug 2026), because
[`domain/release_calendar/sync.py`](../../domain/release_calendar/CLAUDE.md#syncpy--freshness-do-banco-contra-o-calendário)'s
freshness check reads the most recent release that already happened and was inert without
them. Entry count went 127 → 165. Nothing here needed changing — the month pills and
institution filters are computed from whatever is present — but the table now shows past
months, and the "próxima divulgação" stat card is still correct only because it's computed
against `reference_date`, not against the first row. The 15 non-BCB groups are still
future-only, so the past coverage is BCB-only and uneven by design, not by accident.

## Tab "Status dashboard" (2026-08-26)

The report gained a tab bar; the release table is now the first of two tabs. The second answers the
other half of the update question: the calendar button updates the **database**, and nothing was
regenerating the **reports** that read it — a release could land, the button go green, and every HTML
in `reports/` stay a week behind with no visible sign.

One card per dashboard, from
[`domain/dashboards/manifest.yaml`](../../domain/dashboards/CLAUDE.md): what it consumes, which table
each item lives in (or that it's **outside MySQL** — CSV, model artifact, YAML or live source), the
role it plays, and the last data available at the source. Verdict pill per dashboard: `em dia` /
`dado novo na fonte` / **`não dá para conferir`** / `nunca gerado`. The last two carry a one-line
reason *inside the `<summary>`* (`VERDICT_PORQUE`), readable with the card closed — a grey pill with
no reason reads as a defect in the page. The label used to be `sem stamp`, which is the builder's
word, not the reader's — the user read that pill and answered *"eu não sei o que é stamp"*; see
"O rótulo do estado não pode ser a palavra de quem construiu" in
[`.claude/rules/lis-dashboards.md`](../../.claude/rules/lis-dashboards.md). The internal verdict key
is still `sem stamp`; only what the page prints changed.

The guard is on the **rendered tab, stripped of tags**, not on the label dictionary: zero occurrences
of "stamp" in the text a reader sees (`class="stamped"` is markup, and asserting on the raw HTML
fails on it). Verified against 4 mutants — the old label back, the reason removed, the reason moved
out of the `<summary>` (it would vanish with the card closed), and the reason keeping the problem but
losing the way out. Confirmed in Chrome headless against the delivered file: 13 cards, 5 `em dia`,
7 `não dá para conferir` each with its reason inside the summary, 1 `dado novo na fonte`, zero
exceptions, no horizontal overflow.

Both modes work off the same renderer, because `REPORT_DATA.dashboards` (embedded at generation) and
`GET /api/dashboards` (recomputed now) carry the same shape:

- **Servido** — live state, ~2s. `?live=1` also probes the external sources (FRED), one network call
  per series, which is why it's off by default.
- **Arquivo** — the snapshot from when the HTML was generated, and the hint says so. Without this the
  emailed report would show the dependency tree with an empty "último dado" column.

`_garantir_html()` generates through `status.gerar()` rather than `run()`. That used to be the only
way the calendar stamped itself; **since 2026-09-23 `run()` stamps too** (`render_report()` does it),
so the call is now about the *recalculation* half of `gerar()`, not the stamp.

**One wrinkle inherent to this report, in file mode only:** its own card reports the state of the
*previous* generation. The dashboards payload is computed before the file is written and stamped, so
what it embeds is "file N−1 against stamp N−1" — which normally reads `em dia`, and is why this went
unnoticed for so long. It only looks wrong right after a generation that did **not** stamp: measured
2026-09-23, the first run after the fix embedded `não dá para conferir` for itself, because the run
before it (pre-fix) had left no record; the next run embedded `em dia`. Served mode always recomputes
and shows the truth. Not worth a special case — a report's own row is the one place the snapshot
cannot be about the file that carries it.

**Each card has its own Regerar button** (`POST /api/gerar`, same key-allowlist shape as
`/api/run`'s slug allowlist — the page never sends a module path). The POST returns the regenerated
dashboard's new state row only, so the card flips to "em dia" without re-querying the other eleven.
In file mode the same button copies `uv run python -m domain.dashboards.status --gerar <key>`.
Alongside it, since 2026-09-03, a **batch control per tab** — see "Atualizar/Regerar pendentes"
below; the per-row and per-card buttons did not go anywhere.

So the two tabs split the work the way the update actually happens: **tab 1 updates the data
that was released, tab 2 regenerates whichever dashboards you care about right now.**

**Regerar also RECALCULATES (2026-08-31).** Direct user request, after the three-button version
of this — a per-procedure "Rodar" button — was judged confusing: *"Eu quero apenas dois botoes:
(i) Atualizar os dados na base de dados (ii) regenerar o dashboard (trazendo os dados novos,
recalculando as metricas, tudo que houver para atualizar e recalcular)."* So `status.gerar()`
now runs, before generating, whatever `procedures:` the manifest declares as **behind** — a model
estimation, a backtest — and `POST /api/gerar` returns in `procedimentos` what it ran, which the
card prints ("refez X (50.5s) e regerou em 15.8s"). The block inside the card is read-only:
it says what will be redone and how long that costs, so the button's time is announced before the
click (`~Xs para regerar (Ys de geração + Zs de recálculo)`).

What keeps this from becoming "run everything, always" is the `granularidade` of each step (see
[`domain/dashboards/CLAUDE.md`](../../domain/dashboards/CLAUDE.md)): the quarterly panel only falls
behind when a new quarter opens, so a typical click on Monetary Policy is ~55s of recalculation,
and once a quarter it is ~6 min. A step that fails does not block generation — the report comes
out with the old artifact and the card says so, in red.

### The card's prose is product text, not our conversation (2026-09-01)

Direct user correction, from a screenshot of the Monetary Policy card: *"você está transferindo
nossa conversa daqui para o dash, e eu não quero isso. Lá deve ser a explicação do que está
acontecendo ali, para alguém que nunca viu o dashboard."* And, on the procedures block's own
heading: *"'O Regerar refaz antes de gerar · nada atrasado' isso não significa nada."*

They were right, and the defect was systematic rather than one bad sentence: the notes and labels
had been written **in the same session that built the mechanism**, so they inherited its
vocabulary — `generate_report`, `procedures`, `granularidade`, "Desde 2026-08-31", "Segundos não
medidos". Every one of those is true and none answers the question the reader has.

Rewritten: the manifest's 10 `note:` fields, the procedures block heading and note, each step's
metadata line, all three `procVeredito()` verdicts, the tab's mode hint, and the freshness strip in
the monetary policy report. The four substitutions that cover almost every edit are written up in
[`.claude/rules/lis-dashboards.md`](../../.claude/rules/lis-dashboards.md) and were promoted into
the `lis-dashboard` skill; the two worth remembering here:

- **A mechanism's name is not an explanation of it.** `cada trimestre` was the *unit of comparison*
  between the step's cut and the source. It now reads "fica velho quando abre um trimestre novo",
  which is the same fact in the form that is useful. The word `granularidade` no longer appears on
  the page, and an assertion enforces that.
- **The block's heading names what the block contains** — "O que este dashboard calcula por conta
  própria" — and its note explains the *problem* (a number computed from older data than the
  database already has stays old inside a brand-new file) instead of the procedure.

The guard is what prevents relapse, and it is cheap: prose was the only content of the card that no
assertion looked at. `tests/test_release_calendar_js.js` pulls the `.dash-note`/`.proc-note`/
`.proc-hint` blocks out of the rendered HTML and rejects a term list. It runs **only in MODE=file**,
where the cards come from the real embedded payload — so it covers what is written in
`manifest.yaml`, not just what the template assembles — and it was verified against a mutant that
re-injects the old sentence.

### E esta aba também perdeu os 3 stat cards (2026-09-23)

Mesmo pedido que a aba de Divulgações tinha recebido no dia anterior, sobre um print dos cards:
*"pode retirar esses cards, por favor"*. Saíram `Dashboards Mapeados`, `Com Dado Novo na Fonte` e
`Dependências Fora do MySQL`; a página encolheu ~130 px e não sobrou stat card nenhum em lugar
nenhum (há um assert para isso).

O que sobreviveu, e o que não:

- **A contagem virou uma linha ao lado do `<h2>`** (`#dash-resumo`), no mesmo padrão da outra aba:
  `12 dashboards · 5 em dia · 1 com dado novo · 6 sem como conferir`. Conta o **recorte de área**,
  como o lote ao lado — um número que os cards logo abaixo contradizem é pior do que nenhum. Só o
  número que pede ação sai colorido, na cor do selo do card.
- **Os nomes dos dashboards com dado novo não voltaram.** O card do meio listava `Crédito ·
  Expectativas · Política Monetária`, e isso já estava na tela duas vezes: o botão **Regerar
  pendentes (N)** carrega a mesma contagem, e os cards laranja carregam os nomes.
- **A explicação de "fora do MySQL" foi para o `title` da pill que filtra por isso.** Era o
  subtítulo do terceiro card; sem ela a pill vira jargão. Mesmo destino para "com dado novo".

Verificado contra 5 mutantes (cards de volta, resumo contando a lista inteira, resumo sumindo,
o número de ação sem destaque, e o resumo depois do botão de lote em vez de antes) e conferido em
Chrome headless contra o arquivo entregue.

### "Atualizar pendentes" / "Regerar pendentes" — one click for the whole backlog (2026-09-03)

Direct user request, one button per tab: *"colocar um botao, 'Regenerar pendentes' que regenerar
todos os dash pendentes; coloque esse botão tambem no calendar 'Atualiza pendentes'"*. This
**reverses the 2026-08-26 decision** that there would be no batch control anywhere on the page (the
old reasoning: after updating the IPCA you pick which of the six dashboards that read it you want
now). The per-row and per-card buttons are untouched — the batch is an addition, not a replacement,
and it exists for the other case: the answer is "everything that fell behind".

Both live in the card header, right of the `<h2>`, and both carry a count so the click is never a
surprise: `Atualizar pendentes (3)` · `Regerar pendentes (2) · ~153s no total`.

**There is no batch endpoint, and that is the design.** Each button loops over the *existing*
single-item POST, one at a time. Four things follow, all of them wanted:

- the server keeps receiving one slug (or one key) per request, validated against the YAML or the
  manifest — the security story of the two POSTs is unchanged, and no new route exists to audit;
- each row/card updates on screen as its own request returns, instead of the page freezing for
  minutes with no signal;
- two ETL scripts (or two generators) never fight over the same database;
- **the announced time is the sum of the per-item announcements**, which for dashboards means
  generation *plus* whatever each one will recalculate first — the same arithmetic the card button
  already did, added up.

Three rules that are easy to get wrong and produce no error when you do:

- **The queue is snapshotted before the first request.** Recomputing it between items looks
  equivalent and isn't: an item that is *still* pending after running — a group with no script, a
  dashboard whose recalculation step failed — goes back into the queue and is retried forever. The
  mutant that does this doesn't fail the harness, it hangs it.
- **A failure does not abort the queue.** It lands in that item's own card/row and in the closing
  summary (`1 de 2 regerado(s) · falhou: Inflação (BR)`), and the rest still runs. Same instinct as
  `recalcular_atrasados()`: one broken step is not a reason to skip everything after it.
- **"Pending" is narrower than "not green".** For dashboards the queue is `dado novo na fonte` plus
  *a step behind the data*, and deliberately **not** `nunca gerado` (building a report for the first
  time is a decision, not a consequence of data moving — the same rule `regerar_afetados()` applies
  on the CLI) nor `sem stamp` (not lateness: the absence of the snapshot that would let us claim it
  matches). Missing an automatic entry point is out too, by the same criterion as the card button.

**The two tabs differ on one point, and it is the interesting one: the releases tab has a third
state.** Its verdict comes from `/api/status`, so with no server — or with the database down —
there is no freshness verdict at all and therefore no list of pending releases. It says that,
rather than a button or a reassuring "nothing pending", which would be asserting a verdict nobody
has. The dashboards tab has no such gap: its embedded snapshot carries verdicts, so in file mode the
batch is real and degrades to copying **one `--gerar <key>` line per pending dashboard**. Not
`--gerar todos` — that one generates all twelve *without* recalculating, which is not what the
button does.

Covered by four new scenarios in `tests/test_release_calendar_js.js` (batch happy path, batch with a
failure mid-queue, the releases batch, and the two no-verdict cases), verified against 14 mutants —
including parallel-instead-of-serial, each excluded verdict individually let back in, queue
recomputed mid-flight, and the file-mode copy collapsing to `--gerar todos`. The old assertion that
*forbade* a batch control was removed; it had gone stale in place, and would have passed anyway,
since it only looked inside `#dash-cards`.

Two harness bugs surfaced while writing those, both worth remembering: the `/api/dashboards` stub
was handing out `DASHBOARDS_STUB` **by reference**, and `aplicarLinha()` writes into `DASH.rows` — so
the first Regerar of an earlier scenario stamped "em dia" into the shared fixture and the batch
scenario, running later, legitimately saw zero pending. And a capture of "what got copied" that only
stubs `navigator.clipboard` misses the `execCommand` path, which `copiarTexto()` takes whenever the
context isn't secure — the stub returns `true`, so the copy "succeeds" with nothing captured and the
failure reads as a bug in the page.

### A second dashboard got its own recalculation step (2026-09-01)

User asked to extend the `procedures:` pilot to the other dashboards, "like the monetary policy one".
The survey is the result worth recording: of the 12 dashboards, **two** have a step to declare —
monetary policy's three (panels, estimation, forecast) and **inflation's one**, which is a *fetch*
rather than a calculation. `data/ipca_bcb_series.csv` is the only input that report reads from outside
MySQL, so **neither button reached it**: Atualizar writes to the database, and the generator only
reads. It was a month behind when measured (file through 2026-07, `inflc_decomposicao` already at
2026-08), invisible on every screen. Regerar now re-fetches it in ~18s when it is behind.

The other ten legitimately have nothing: they read the database and compute in-process, so the honest
card is the one they already show, with no block. Câmbio is the interesting near-miss — its two Ridge
caches are now **declared as dependencies** (they never were), but deliberately not as steps; the
reasons, including a `min`-vs-`max` trap that would have made a step recalculate forever, are in
[`analytics/brasil/exchange_rate/CLAUDE.md`](../brasil/exchange_rate/CLAUDE.md).

### The console encoding could fail a Regerar, and did (2026-09-01)

Found while wiring that step. `serve.py` inherits the console's encoding, and the Windows console
`abrir_calendario.bat` opens is **cp1252** — so a progress `print` carrying a character it cannot
encode raises `UnicodeEncodeError` *inside* the generator. The inflation report's own summary prints
an arrow (U+2192), which means clicking Regerar on that card returned an error and did not rebuild
the file, **for a reason with nothing to do with the data**.

Measured both ways: `status.gerar('brasil_inflation')` in a cp1252 shell dies on `'\u2192'`; with
`PYTHONIOENCODING=utf-8` it finishes in 19.9s. Fixed at the layer that owns the process's streams —
`utils/console.stdout_utf8()`, called first in `main()`, reconfigures stdout/stderr to UTF-8 with
`errors="replace"`, because a character the terminal cannot draw must never cost the operation.
Verified through the real server: `POST /api/gerar` for `brasil_inflation` returned ok in 17.8s with
zero tracebacks.

**Three entry points needed it, not one**, and the other two were already broken before this round:
`jobs/update_db.py` regenerates the dashboards it affects (since 2026-08-28), so
`--group ibge_ipca` finished the ETL and then died in the regeneration; `status.py --gerar` the same.
A test asserts all three call it, since the failure only shows up in a real cp1252 console.

## A aba Divulgações abre no MÊS, em blocos de semana (2026-09-22)

Pedido do usuário, em quatro partes: abrir sempre no mês corrente com um clique-expande para
escolher outro; pôr Fonte e Mês em clique-expande também (a Divulgação já era um `<select>`);
separar o mês em blocos por semana, com o que já saiu em cinza e a semana corrente aberta; e
marcar cada linha com o país — `(BR)`, `(US)`, `(INT)`.

A barra de filtros virou **quatro `<select>`** — País · Fonte · Divulgação · Mês de divulgação —
mais um **Limpar** que volta ao padrão (`Todos`/`Todas`/`Todas`/mês corrente). As pill rows
saíram; `buildPills()` foi substituída por `buildSelect()`.

Quatro decisões que valem além desta página:

- **O padrão estreito tem de dizer que é estreito.** Um seletor fora do "todos" fica marcado
  (`.ctrl-select.narrow`, dourado). Sem isso "o mês está vazio" e "o recorte esconde o resto"
  ficam indistinguíveis — e o recorte agora é o padrão, não uma escolha.
- **E não pode APAGAR o que ficou de fora.** O lote continua agindo só sobre o que está listado
  (regra de 2026-09-03, intacta), mas a barra passou a contar os grupos atrasados **fora** do
  recorte: `+1 pendente(s) fora do recorte: BCB — IC-Br — troque o mês para alcançá-las`. Sem
  essa linha, abrir no mês corrente esconderia um atraso de dois meses atrás sem nada na tela.
- **A "próxima divulgação" ignora o mês de propósito.** Os outros três recortes valem; o mês
  não, senão no dia 30 o card diria "—" existindo uma divulgação na semana seguinte. Quando a
  próxima cai fora do mês escolhido, o card diz isso.
- **A cascata precisa de fallback explícito.** Cada seletor lista só o que existe sob os
  anteriores, e um valor que deixou de existir (`US` + `IBGE`) **cai de volta** para "todas" em
  `normalizarRecorte()`. Sem isso o estado fica válido no objeto e inválido na tela, e a tabela
  sai vazia sem dizer por quê.

### O bloco de semana é uma LINHA de cabeçalho, não um `<details>`

`<details>` dentro de `<tbody>` quebra a tabela, e uma tabela por semana perderia o alinhamento
das colunas entre os blocos — que é metade do valor de ler o mês. Então o clique-expande é um
`<tr class="week-header">` com caret `+`/`−` e a chave da semana num `data-week` da célula; o
listener da tabela passou a procurar dois seletores (`button.upd-btn` e `[data-week]`).

- **Semana de segunda a domingo, contas em UTC.** `new Date('2026-09-01')` é lido como UTC e
  `new Date('2026-09-01T00:00:00')` como hora local: misturar os dois desloca o bloco inteiro
  pelo fuso da máquina, e o sintoma é uma linha de segunda aparecendo na semana anterior — sem
  erro nenhum. O teste afirma `segundaDa()` em domingo, segunda e sábado.
- **Abre a semana corrente; num mês futuro, a primeira; num mês vencido, a última.** Um mês
  inteiro fechado é uma tela sem nada, pior do que abrir a semana errada.
- **O que o usuário abriu sobrevive ao re-render.** O default só é aplicado quando *nenhuma*
  semana daquele mês foi tocada — sem essa distinção, fechar a semana corrente a reabriria no
  clique seguinte (mesmo modo de falha do `DASH.abertos` dos cards).
- **Cinza é para o que já saiu, menos o que está atrasado.** A linha laranja é a única da página
  que pede ação; apagá-la por "já ter saído" apagaria exatamente essa. Os dois lados são
  afirmados — só o primeiro passaria num mutante que apaga as duas.

### O selo de país é DERIVADO do schema, não escrito à mão

`_paises_dos_grupos()` em [`generate_report.py`](generate_report.py) resolve as tabelas de cada
grupo pelo `domain/db/registry.py` e lê a área do módulo: `brasil/` → BR, `us/` → US,
`international/` → INT. É a mesma divisão dos três jobs (`update_db`, `update_us`,
`update_international`), então ela não tem como divergir do banco sem o registry mudar junto. Um
grupo que espalhe tabelas por duas áreas, ou uma instituição desconhecida sem tabela nenhuma,
**levanta** em vez de virar badge em branco.

Consequência que vale saber antes de estranhar: **FOMC e COT saem como INT, não como US.** As
tabelas que eles escrevem — `diferenciais_juros` e `cmb_cot_fx` — são séries entre países e vivem
no schema international. Quem publica é americano; o dado não é de um país só. Se algum dia a
leitura desejada for a do publicador, a troca é usar `_INSTITUICAO_PAIS` como fonte primária em
vez de fallback. Hoje: BR 23 grupos · US 5 · INT 2.

O mesmo selo entrou no card da aba **Status dashboard** (`AREA_PAIS`, com `raiz` → INT: o que
monitora o sistema inteiro não é de um país).

### E a janela do cabeçalho passou a ser derivada

`Período: Ago–Dez 2026` estava fixo no HTML desde a primeira versão, e o YAML já carregava o ano
inteiro — uma linha que o payload ao lado contradizia e que ninguém levantaria na virada do ano.
Agora sai do `min`/`max` das próprias divulgações. Um dos dois itens de rollover desta pasta
deixou de existir; o outro (`_YAML_PATH`) continua.

### E a barra desceu para dentro do card, sem os stat cards (mesmo dia)

Segundo pedido, sobre um print da barra: *"Coloque o seletor logo acima da tabela, e melhor, pode
retirar esses cards"*. A barra era um cartão próprio no topo da aba, com os 3 stat cards entre ela e
a tabela — então o controle da tabela ficava a ~250 px do que ele controla.

- **A barra virou um strip DENTRO do `.table-card`**, sem fundo nem borda própria (cartão dentro de
  cartão lê como dois blocos), separada da tabela por uma linha e a 2 px dela. Um guarda estático em
  `tests/test_release_calendar_js.js` afirma a ordem no markup entregue — "está acima da tabela" é
  propriedade do HTML, não do render, então o harness de DOM-string não alcança.
- **O cap de largura do `<select>` é o que a mantém em uma linha.** Dentro do card sobram ~1.330 px,
  não os 1.440 da página, e com o `max-width: 360px` do seletor de Divulgação os quatro controles
  quebravam para uma segunda linha: medido em browser, **82 px de altura contra 45** com o cap de
  250 px. O nome comprido continua inteiro na lista aberta; só a caixa fechada trunca.
- **Os 3 stat cards saíram e as contagens ficaram**, numa linha de metadado ao lado do título:
  `34 divulgações · 21 já saíram · 1 com data estimada`. Ela conta o **recorte**, não o calendário —
  um número que a tabela ao lado contradiz é pior do que nenhum. A "próxima divulgação" não voltou em
  texto: com a lista abrindo na semana corrente, ela é a primeira linha não-cinza da tela.

**Confirmado em browser real** (Chrome headless via CDP, contra `reports/release_calendar.html`):
zero exceções, 4 seletores, 5 blocos de semana com só a corrente aberta, 5 linhas com selo,
2 em cinza, clique num cabeçalho fechado abre (5 → 12 linhas), `País=US` deixa 3 linhas todas US
e estreita a lista de fontes para BEA/BLS, o Limpar volta ao padrão, a barra fica em uma linha
(45 px) dentro do card e a aba inteira cabe sem rolagem. Coberto por 38 asserções novas em
`tests/test_release_calendar_js.js`, verificadas contra **18 mutantes** (ano inteiro por padrão,
todas as semanas abertas, nenhuma aberta, primeira em vez da corrente, selo removido, cinza na
atrasada, cinza em ninguém, pendente fora do recorte sumindo, cascata removida, fallback removido,
`segundaDa` com getters locais, clique que não redesenha, cada um dos dois filtros não filtrando,
barra de volta para fora do card, resumo contando o calendário inteiro, resumo contando só as
linhas visíveis, e resumo sumindo).

## Pending

- Add the remaining gaps listed in `domain/release_calendar/CLAUDE.md`'s "Known gaps" (international
  BIS/NOAA series, `atv_pib_usd`, `cmb_risco_pais`, `fisc_investimento`) once that research is done —
  this report picks them up automatically on the next regeneration, no code change needed here.
  `cred_ptc` is no longer pending: it's confirmed and charted as `bcb_ptc`.
- Not wired into `jobs/update_db.py` or any other routine job — this is a one-off/on-demand report, run
  manually when the calendar YAML changes.
- **Confirmed in a real browser (2026-08-26)** — cards, dependency table and the Regerar button in
  served mode. What that round also caught: the button's label was following `DASH.ao_vivo` (did the
  state load?) instead of `LIVE.on` (is there a server?). The two only diverge when `/api/dashboards`
  fails on a served page — the button fell back to "Copiar cmd" and the hint said "modo arquivo",
  both wrong, while `/api/gerar` was up the whole time. Fixed, and the mode hint now has three
  states instead of two. Regression covered by the "SERVIDO SEM ESTADO" section of
  `tests/test_release_calendar_js.js`. Still unconfirmed visually: the two filter pill rows and the
  file-mode clipboard fallback.
- **Chaining the two tabs was considered and rejected** (2026-08-26, still true): one click that
  updates a group *and* regenerates everything it feeds. The calendar button stays data-only. Note
  that the 2026-09-03 batch buttons are *not* this — each one stays inside its own tab, so updating
  data and rebuilding reports remain two deliberate actions. Don't collapse them.
- The update button's **served mode has not been confirmed in a real browser** — the interaction is
  covered by [`tests/test_release_calendar_js.js`](../../tests/test_release_calendar_js.js) (real
  script, stubbed DOM/fetch, click dispatched) and the endpoints by
  [`tests/test_serve_calendar.py`](../../tests/test_serve_calendar.py), but nobody has watched a
  button actually turn green in a browser window. Same standing caveat as every other report here.
- **A slow group blocks its own button with no progress feedback.** `POST /api/run` is synchronous, so
  `mte_caged_novo` (~50MB from the FTP, minutes) leaves the button on "rodando..." with nothing to
  watch. `ThreadingHTTPServer` means it doesn't block *other* requests, and closing the tab doesn't
  abort the run. If that becomes annoying, the fix is a job id + polling, not a timeout.
- Open in a real browser to confirm the three filters (institution/month/divulgação) compose correctly
  and the stat cards agree with the filtered table. Not yet done for the 2026-08-17 regeneration, whose
  entry count grew from ~108 to 127 and which hides the recurring strip for the first time.
