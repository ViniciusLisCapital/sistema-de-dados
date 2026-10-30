# Labour Market — Conceptual Map

**Status:** Parts 1–4 approved by the user on 2026-10-30 (`coordenacao/B_novos_agentes.md`,
Decisões): boundaries, the five central questions, the agent's own unemployment path, the skeleton
without a separate rates-and-credit channel, the outputs and inputs, and the data list. The thesis
variable stays **provisional, decided with the model** (`SISTEMA_AGENTES.md` III.III.ix). Part 5
belongs to chat D.

**What this file is.** This is the labour-market agent's (`mercado_trabalho`, code **MT**) contract
with the rest of the system. It says what every report must answer (Part 1, central questions), what
moves the Brazilian labour market and how it reaches activity and prices (Part 2), what this agent
tells the others matters TO IT (Part 3, outputs), and what the others told this agent matters TO THEM
(Part 4, inputs). Part 5, the concept index and the layer 1, comes from chat D before cycle 2; the
agent reads that layer through its knowledge snapshot, like the others. The map still carries the
reasoning on its own — the mechanism, its premises, when it holds and when it fails — and no
estimate from any paper enters as a current value (`PRINCIPIOS_AGENTES.md` I.I.vii).

**The agent's role** (decided by the user, 2026-10-30): **to be an input of the activity agent and
of the output gap.** Its main product is what it tells activity — the labour slack, its two projected
paths (unemployment and the CAGED) and employment by sector (ME-AT1, ME-AT2) —, ahead of what it
tells inflation and monetary policy.

**Where this agent comes from.** Until 2026-10-30 the activity agent held the labour market
provisionally (`SISTEMA_AGENTES.md` III.III.vii). The boundaries now (III.III.ix):

- this agent owns the Brazilian labour tables (`mt_pnad`, `mt_desocupacao_retro`, `mt_caged`,
  `mt_caged_setor`, and the other `mt_*` of Brazil, see the data list);
- **the output gap stays with the activity agent.** Labour slack — unemployment against the NAIRU,
  wages against productivity — is this agent's **output** to activity, inflation and monetary policy;
- the US labour market (`mt_jolts`, `mt_ces`, `mt_cps`) stays with the external agent;
- credit (`cred_*`) belongs to the credit agent (CR), still to be built: this agent consults it.

**How the parts connect to the rest of the vault.** `[[concept]]` links go to `concepts/`; a name in
`code` font is either a MySQL table of this agent's list or a concept with no page yet (to be listed
in Part 5). "Data" names tables of this agent's list (`SISTEMA_AGENTES.md` V, to be written when this
map is approved). No mental model of an asset manager exists for this area yet.

**Outputs and inputs.** An output of agent A to agent B is what A tells B is important for A, coming
from B. An input of A from B is what B told A is important for B, coming from A
(`SISTEMA_AGENTES.md` I.III.vii). This agent's outputs carry the prefix **MT** plus the other agent's
code — CB (câmbio), PM (política monetária), IN (inflação), AT (atividade), EX (externo), EP
(expectativas), FS (fiscal), CR (crédito) — so `MT-AT1` is the first thing this agent needs from
activity. Its inputs carry **ME** with the same codes (no other map uses ME). A row is a request; the
content flows the other way. It gives emphasis and tells the other agent what to flag; it never limits
the analysis.

**Two layers.** What is written here is the **fixed** layer: what matters every cycle. Each cycle
adds a **dynamic** layer in the reports, set by that cycle's theses.

**Data rule** (`SISTEMA_AGENTES.md` I.III.ix–x). *Endogenous*: the PNAD Contínua (monthly and
quarterly), the BCB's seasonally adjusted unemployment and the CAGED (stock, and the Novo CAGED by
sector, state and wage band). *Endogenous of another agent*, read for consultation, never concluded
on: the gap, GDP and the monthly activity indicators (atividade), the IPCA and services (inflação),
transfers and payroll (fiscal), the Focus and the QPC (expectativas), and credit supply to small firms
(crédito)
— each owner's position arrives through Part 3. No TWA and no exogenous table. Every number is
traceable to table and date; every pattern stated as historical — "construction turns first", "the
informal absorbs the downturn" — comes out of a G over the cycle's A, with the window said, or does
not enter (`PRINCIPIOS_AGENTES.md` I.II.ix). The patterns in Part 2 are written as hypotheses for that
G, not as findings.

---

## Part 1 — Central questions: what every report answers

**Decided by the user, 2026-10-30.** The questions are the floor, not the ceiling. They are kept in
Portuguese, the language of the report.

The agent does not describe the PNAD: it says how much slack the labour market has and how sure
anyone can be of it, what is moving jobs and income, where in the cycle the sectors say we are, and
whether wages are running ahead of productivity — and turns that into the thesis and into what it
tells activity first (for the gap and the nowcast), then inflation and monetary policy.

| # | Question | What the answer covers | Where to look |
|---|---|---|---|
| T1 | Quanta folga há no mercado de trabalho? | Unemployment (seasonally adjusted) against the NAIRU — the market's (QPC) and any the agent estimates with a G, with the uncertainty around it; the other measures of slack: underutilization, time-related underemployment, the potential labour force and discouraged workers, participation; whether they agree; the reading told to activity, inflation and PM as **labour slack** | 2.1, 2.2, 2.3 |
| T2 | O que move o emprego e a renda agora? | Employment (PNAD and CAGED) against output; formal against informal, employees against own-account; real earnings, habitual and effective, and the real wage bill; what is cyclical and what is composition, policy or one-off | 2.3, 2.4, 2.5, 2.9 |
| T3 | Que setores lideram e quais viram primeiro? | The dynamics of the sectors most sensitive to the cycle (CAGED and PNAD by sector): who hires and who stops, admissions against separations, employment against each sector's output; what the composition says about the phase of the cycle; the formal × informal, age and regional cuts when they say something about the cycle | 2.6, 2.4 |
| T4 | Os salários crescem acima da produtividade, e o que isso pede da inflação de serviços? | Real wage growth against labour productivity (per worker and per hour), unit labour costs, indexation and the minimum wage; the part of wage pressure the output gap does not already carry; what that asks of services inflation — told to inflation, which concludes on prices | 2.7, 2.8, 2.9 |
| T5 | Qual o cenário para os seis trimestres? | The thesis below: the path of the thesis variable by quarter, central, base band and tails, with what leads to each tail; the labour slack and the wage reading over the horizon, for the agents that use them | the horizon; 2.1–2.9 |

### The horizon and the thesis — provisional, decided with the model

The system's theses are per quarter of the Structural Model, six quarters from the current one, with
the variable measured at the close of the quarter (`SISTEMA_AGENTES.md` III.III.i; in a cycle dated
2026-10-30, 4T26 to 1T28). Today **no labour variable enters the model**. The model team's test of an
estimated gap (2026-10-30, `coordenacao/C_modelo.md`, test A) found that unemployment is what moves
an estimated gap most — 0.8 of the 1.0 p.p. difference against the BCB's gap at the time, with the
CAGED and GDP weighing little — and the user postponed the model decisions to before cycle 2. So the
thesis is **provisória, decide com o modelo**, with two alternatives written down. **It has two
variables** (decided by the user, 2026-10-30): the unemployment rate (below) and the **CAGED — the
Novo CAGED's net balance of formal jobs over the twelve months ending at the close of each quarter**,
in thousand jobs (equal to the change of the formal-employment stock over a year; twelve months and
not the quarter's own balance because the monthly balance is strongly seasonal, and it is what
activity compares with GDP growth). Both are the agent's own projections, with central, base band
and tails; the CAGED is scored at the first publication of the quarter's last month. The two paths
must tell one story (formal jobs growing while unemployment rises needs a stated reason).

1. **(a) If unemployment enters the model:** the thesis is the **seasonally adjusted unemployment
   rate at the close of each quarter**, % of the labour force. The PNAD's rolling quarter ending in
   the last month of a calendar quarter *is* that quarter, so "close" and "quarter" coincide. The
   central follows the model's design: if unemployment is an exogenous path of the model (an input to
   the gap's starting point), this agent writes it, the central is the agent's base path and the rule
   of the fiscal and external agents applies (tutela in the "Exógenas" tab of
   `repository/agent_mapping/data_tracker.xlsx`); if the model gets an equation for it, the central
   is the model's, without adjustment, like every endogenous thesis. Series: `mt_desocupacao_retro`
   (the BCB's own seasonally adjusted series, the one its aggregate model uses) — but it moves only
   with each RPM, so for the most recent quarters the F has to carry a seasonal adjustment of
   `mt_pnad` by a fixed method, set by the system, not by the agent (IV.iv). **Pending: which series
   and method, decided with the model.** Scoreboard: the BCB's series in the first RPM edition that
   contains the quarter, as the activity agent scores the gap.
2. **(b) Otherwise:** the fiscal and external rule — the thesis is the base path of the model's
   exogenous variables this agent tutors, and the distribution around it. **Today there are none.**
   For that case (decided by the user, 2026-10-30): the agent writes the same seasonally adjusted
   unemployment path, and the CAGED path, as its own centrals, outside the model and outside P, with base band and tails,
   scored the same way, so the report keeps a falsifiable number and the scoreboard can test it.
3. **Upside and downside**, for both alternatives: position only, as for every thesis
   (`SISTEMA_AGENTES.md` III.III.i). For unemployment, upside is the rate above the base band — more
   slack —, downside below it — a tighter market; for the CAGED, upside is more formal jobs than the
   base band. The report says in words what each tail of each variable means for Brazil; for
   unemployment, the upside tail is the bad one for employment and income and the disinflationary one for services; the downside tail is
   the one that carries wage and services pressure, the risk the inflation and PM agents watch.
4. **The NAIRU question is this agent's whether or not anything enters the model.** T1 reads
   unemployment against the NAIRU in every report. The database has no NAIRU (gap in the tracker);
   the market's comes from the QPC, and an estimate of the agent's own is a G, logged, candidate to
   the F. The model team's test also showed why it matters now: a regression of the gap on
   unemployment breaks when the rate leaves the range of its training sample, and whether the NAIRU
   has moved with it is the question that decides the reading.
5. **Registered for later:** the activity agent's idea of decomposing the gap into components
   (output, unemployment and others) would make part of the gap this agent's (activity map, Part 1,
   horizon item 7).

---

## Part 2 — Causal skeleton

**Where the labour market enters the Structural Model** (`analytics/agent_system/modelo.py`,
`listar`). Nowhere, today. The model has no unemployment, employment or wage variable: labour reaches
it only through the BCB's output gap, which the IS curve (H) produces and the Phillips curves (I) read
— services strongly, industrial goods less, food not at all. So this agent's readings reach the
system as **tempero of type (ii) on another agent's variable**, and only for the part the gap does not
already carry: the activity agent decides it on the gap, the inflation agent on services. This agent
never sets the gap or the IPCA. If test A goes forward, unemployment becomes an input of the gap's
starting point and this changes (Part 1, the horizon).

### Block A — slack (T1)

#### 2.1 Unemployment against the NAIRU

- **Mechanism.** Below the rate of unemployment that does not accelerate wages, firms compete for
  workers, wages rise faster than expected inflation plus productivity and costs feed prices; above
  it, wage growth slows. The NAIRU is not observed and it moves: institutions (labour law, minimum
  wage, unemployment insurance), the composition of the labour force (age, education), the share of
  informal and own-account work, and the time it takes to match workers to jobs all shift it. After a
  long slump part of the unemployment can become structural (hysteresis), and a reform can lower it.
  So the distance to the NAIRU is a judgement with a band, not a number.
- **Read:** [[natural_rate_of_unemployment]], [[phillips_curve]], [[sticky_wages]]; `hysteresis`,
  `wage_phillips_curve`.
- **Data:** `mt_desocupacao_retro` (the BCB's seasonally adjusted rate, since 2004), `mt_pnad`
  (`taxa_desocupacao`, not seasonally adjusted); consultation of `expc_qpc` (the market's NAIRU and
  gap) and `expc_focus_periodo` (the consensus for unemployment).
- **Model:** outside the model; the slack reading is told to atividade (ME-AT1), inflação (ME-IN1)
  and PM (ME-PM1).
- **Trap.** The PNAD is not seasonally adjusted: compare a month with the same month a year earlier,
  or use the BCB's series, never two consecutive months. The rolling quarter overlaps two thirds of
  the previous reading. The NAIRU is not in the database: never write one from memory — use the QPC's
  or a logged G, and say which, with its uncertainty. A rate below every rate in an estimation sample
  is exactly where a fixed NAIRU stops being trustworthy.

#### 2.2 The other measures of slack: hours, participation, discouragement

- **Mechanism.** Unemployment counts only those without work who searched. Slack also hides in
  people working fewer hours than they want (time-related underemployment), in those who would work
  but did not search (the potential labour force, discouraged workers) and in participation. In a
  downturn people leave the labour force, so unemployment rises less than job losses (discouraged
  workers); a second household member may enter when the first loses a job (added worker).
  Transfers raise the reservation wage and can lower participation without changing labour demand.
  Ageing lowers participation trend-wise. When unemployment falls because participation falls, slack
  did not close.
- **Read:** [[natural_rate_of_unemployment]]; `labour_force_participation`, `discouraged_workers`.
- **Data:** `mt_pnad` (`taxa_participacao`, `nivel_ocupacao`, `taxa_subutil_composta`,
  `taxa_subocupacao_horas`, `subutil_forca_potencial`, `subutil_desalentado`, `pct_desalentados`,
  `fora_da_forca_trabalho`); `mt_pnad_trimestral` (rates by age and education); consultation of
  `fisc_rtn` (Bolsa Família and BPC).
- **Model:** outside the model; part of the slack reading (T1).
- **Trap.** A falling unemployment rate with falling participation is not a tightening: decompose
  the change of the rate into employment and labour force with a G before reading it. Demographic
  trend and cycle are hard to separate in a short sample (the PNAD starts in 2012).

### Block B — employment and income now (T2)

#### 2.3 Employment against output: Okun and the lag

- **Mechanism.** Employment follows output with a lag and less than one for one: firms keep
  workers through a slowdown they think is temporary (labour hoarding) because hiring and firing
  cost, and hire only when they believe the recovery. So unemployment keeps falling for a while after
  activity slows, and keeps rising after it recovers; the relation between the change of unemployment
  and growth above potential (Okun) is a rule of thumb whose coefficient differs by country and
  period. Productivity is the mirror: it falls when output slows and employment holds, and rises when
  output recovers first. **This is also the way interest rates and credit reach jobs** (decided by the
  user, 2026-10-30): they affect unemployment, but through growth first — a tighter policy rate or
  scarcer credit slows demand and output, and employment follows output. So the map has no separate
  rates-and-credit channel to employment; the growth path that carries them is activity's (MT-AT1),
  and the one firm-level exception is a note in 2.6.
- **Read:** [[output_gap]], [[monetary_transmission_lags]]; `okun_law`, `labour_hoarding`.
- **Data:** `mt_pnad` (`ocupado`), `mt_caged` (formal stock, monthly); consultation of
  `pm_hiato_produto` (the BCB's gap), `atv_pib`, `atv_pib_taxas` (GDP, value added),
  `atv_ibcbr` (the monthly cycle).
- **Model:** outside the model; the answer to activity's slack cross-check (ME-AT1), and the reason a
  tight labour market and a slowing economy can coexist.
- **Trap.** The gap is activity's (MT-AT1): read it, never conclude on it. "Employment lags output
  by N months" is a pattern: measure it with a G over the cycle's A, with the window, or do not say it.
  Monthly GDP does not exist: the quarter's productivity uses quarterly GDP and the PNAD's quarter.

#### 2.4 Formal and informal, employees and own-account

- **Mechanism.** The two surveys measure different universes: the PNAD counts everyone working,
  formal or not; the CAGED counts formal employees (CLT) from the employers' records, monthly and
  faster. Informal and own-account work act as a buffer — they can absorb people who lose formal jobs
  in a downturn and grow first in a recovery — and their incomes are more flexible. A recovery led by
  informal jobs adds less income stability, less payroll-deducted credit and less tax revenue than one
  led by formal jobs. Self-employment with a CNPJ (MEI) blurs the line.
- **Read:** [[sticky_wages]]; `informality`.
- **Data:** `mt_pnad` (`ocup_priv_excl_domestico_com_carteira` / `_sem_carteira`,
  `ocup_conta_propria_cnpj` / `_sem_cnpj`, `ocup_informal`, `taxa_informalidade`,
  `pct_contribuintes_previdencia`, and the earnings of each position), `mt_caged`, `mt_caged_setor`.
- **Model:** outside the model; T2 and T3.
- **Trap.** The CAGED and the PNAD can diverge for months without either being wrong. The CAGED
  stock is re-anchored by the BCB backwards, and its last month may be provisional (column `fonte`,
  `mte`): check before reading the year-on-year. The Novo CAGED (sector, state, wage band) starts in
  2020 with a new source of records: do not splice it with the older stock without saying so. The
  CAGED's monthly balance is strongly seasonal (December is negative): compare with the same month,
  or use twelve-month sums.

#### 2.5 Real earnings and the wage bill

- **Mechanism.** Household income from work is employment times the real wage — the wage bill — and
  is the main driver of household consumption, the largest component of demand. Real earnings rise
  with a tight market, with productivity and with the minimum wage, and are eroded by inflation; past
  inflation feeds wage claims with a lag (indexation). The average wage moves also by **composition**:
  when low-wage workers lose their jobs first, the average rises without anyone earning more.
- **Read:** [[sticky_wages]], [[inflation_persistence]]; `composition_effect`, `wage_indexation`.
- **Data:** `mt_pnad` (`rend_habitual_real_todos_trabalhos`, `rend_efetivo_real_todos_trabalhos`,
  `massa_real_habitual`, `massa_efetiva_real`, and earnings by position and by sector),
  `mt_pnad_trimestral` (earnings by occupation and activity); consultation of `inflc_agregados` (the
  deflator).
- **Model:** outside the model; the income reading told to activity (ME-AT1), which concludes on
  consumption.
- **Trap.** Habitual and effective earnings differ: effective includes bonuses and the thirteenth
  salary, so it is seasonal; read the habitual for the trend. The real series come deflated by the
  IBGE; a G deflating by the IPCA must say so, and will not match. Read the wage bill before the
  average wage: it does not suffer the composition effect.

### Block C — the sectors and the phase of the cycle (T3)

#### 2.6 Which sectors lead, which turn first

- **Mechanism.** Sectors differ in how much and how early they respond to the cycle. Those whose
  demand depends on credit and on the policy rate — construction, durable-goods manufacturing,
  vehicle and appliance retail — and those firms use to adjust quickly — temporary staffing and
  administrative services — are expected to turn first; agriculture moves with harvests and weather;
  public administration, health and education move with budgets and demography, not with the cycle.
  Within a sector, hiring usually moves before firing: a fall in admissions with stable separations
  is an early slowdown, rising separations a later stage. So the composition of net hiring — cyclical
  against acyclical sectors, admissions against separations, formal against informal, young against
  prime-age (youth unemployment moves most), state by state — is a reading of the **phase** of the
  cycle, earlier than the aggregate. Comparing each sector's employment with its own output shows
  where firms hoard labour (output falls, jobs hold) or where hiring runs ahead.
  **A note on credit to small firms.** Credit reaches aggregate employment through growth (2.3), but
  at the firm level there is a composition effect worth watching: small firms that depend on one bank
  for working capital, when that bank cuts credit, fire more than similar firms whose bank does not —
  the reasoning of firm-level studies of the 2008–09 credit crunch in the US. It does not add a
  channel: it says where the job losses land when credit to small firms locks, so the agent looks at
  small-firm-heavy sectors (commerce, services) first in that case.
- **Read:** [[monetary_transmission_lags]], [[credit_channel]], [[output_gap]];
  `sectoral_cyclicality`.
- **Data:** `mt_caged_setor` (admissions, separations and balance by CNAE section), `mt_caged` (stock
  by sector, since 1992), `mt_pnad` (occupation by activity), `mt_pnad_trimestral` (unemployment by
  age), `mt_caged_uf` (balance by state), `mt_caged_salario` (hiring by wage band); consultation of
  `atv_pib` (value added by sector), `atv_pim`, `atv_pmc`, `atv_pms`, `atv_ibcbr`; endogenous of credit
  (consultation) `cred_ptc` (banks' reading of credit supply, small and medium firms among the
  segments), for the note above.
- **Model:** outside the model; the phase reading is told to activity (ME-AT2) and PM (ME-PM1).
- **Trap.** **Which sectors lead in Brazil is a claim to measure, not to remember**: before stating
  it, a G over the stock series since 1992 (and the PNAD since 2012) says which sector's employment
  turned before the aggregate, in which episodes, with the window. One sector moving is not a phase;
  the phase is a pattern across several. The PNAD's sector cut is not the CAGED's (household survey
  against CNAE register): compare directions, not levels. The wage bands of `mt_caged_salario` are
  multiples of the minimum wage, which is readjusted every January: the bands jump then.

### Block D — wages, productivity and prices (T4)

#### 2.7 Wages against productivity: unit labour costs

- **Mechanism.** A firm's labour cost per unit of output is the wage divided by productivity. Real
  wages growing in line with productivity leave unit labour costs and margins unchanged; growing
  above it, they raise costs, which are passed to prices where demand allows or compress margins.
  Productivity is measured as output per worker or per hour; in the short run it is mostly cyclical
  (2.3), so a fall in productivity in a slowdown raises unit labour costs without any wage pressure.
  A wage Phillips curve links wage growth to the unemployment gap and to expected or past inflation;
  the minimum wage sets a floor for a large share of formal wages and indexes benefits.
- **Read:** [[sticky_wages]], [[phillips_curve]], [[nk_phillips_curve]]; `unit_labour_costs`,
  `wage_phillips_curve`, `minimum_wage`.
- **Data:** `mt_pnad` (earnings and employment), `mt_pnad_trimestral` (hours worked by position,
  quarterly — the only hours series); consultation of `atv_pib` (value added, total and by sector,
  quarterly), `inflc_agregados` (the deflator).
- **Model:** outside the model; T4 is told to inflation (ME-IN1) and PM (ME-PM1).
- **Trap.** **The database has no unit labour cost, no productivity series, no minimum-wage series
  and no INPC** (gaps in the tracker): productivity and unit labour costs are a G (output from
  `atv_pib`, employment or hours from the PNAD), logged, and the minimum wage comes from fiscal
  (MT-FS1) or is declared as a gap. Per-worker and per-hour productivity can diverge when hours move.
  Output by sector against employment by sector compares two different classifications.

#### 2.8 From wages to services inflation

- **Mechanism.** Services are labour-intensive and not traded: their prices follow local demand and
  unit labour costs, so wage pressure shows first in services. Wage income also sustains the demand
  for services. But wages and the output gap move together, and services already respond to the gap
  in the model: only the part of wage pressure the gap does not carry is new information — a minimum
  wage above the market, indexation of past inflation, a labour-supply shock that tightens the market
  without more demand.
- **Read:** [[nk_phillips_curve]], [[divine_coincidence]], [[inflation_persistence]];
  `unit_labour_costs`.
- **Data:** consultation of `inflc_agregados` (services, underlying services), `pm_hiato_produto`.
- **Model:** the gap enters the services equation of (I), the inflation agent's: this agent says how
  much wage pressure lies beyond the gap, and the inflation agent decides the tempero on services
  (ME-IN1). This agent never sets the IPCA.
- **Trap.** Adding wages and the gap for the same quarters is double counting. Wages rising after an
  inflation burst are partly propagation of past inflation, not new demand. Say which part each
  argument is about.

### Block E — policy and institutions

#### 2.9 Labour policy and institutions

- **Mechanism.** The minimum-wage rule, transfers (Bolsa Família, BPC, unemployment insurance, the
  abono), payroll taxes and exemptions, public hiring and civil-service pay, and labour law change
  wages, participation and the NAIRU without passing through demand. A minimum wage rising faster
  than productivity compresses the bottom of the wage distribution and raises indexed benefits;
  more generous transfers can lower participation and raise the reservation wage; a labour reform
  that cuts hiring costs or changes the form of contracts can lower the NAIRU and shift jobs between
  formal and informal.
- **Read:** [[fiscal_impulse]], [[natural_rate_of_unemployment]]; `minimum_wage`,
  `reservation_wage`.
- **Data:** consultation of `fisc_rtn` (`seguro_desemprego`, `abono`,
  `obrigatorias_com_controle_de_fluxo_bolsa_familia`, `beneficios_de_prestacao_continuada_da_loas_rmv`,
  `pessoal_encargos_sociais`); `mt_pnad` (public-sector employment and earnings).
- **Model:** outside the model; T1, T2 and T4. The decisions and their dates come from fiscal
  (MT-FS1, MT-FS2).
- **Trap.** The minimum-wage rule and the labour law are not in the database: never write the rule
  or next year's value from memory; ask fiscal and declare the gap. A transfer's effect on
  participation is a hypothesis to check with the data, not a given.

### Where the agent reads the data

The agent reads every table of its list through `obsidian/ciclos/<date>/dados/F_mercado_trabalho.md`,
fixed for the cycle (module `analytics/agent_system/dados/mercado_trabalho.py`, to be built in chat
B's B2). Besides each table's reading, the F is meant to carry what no single table gives: the
seasonally adjusted unemployment for the recent months (method set by the system, Part 1 item 1), the
change of the unemployment rate split into employment and labour force (2.2), and the twelve-month
CAGED balance by sector against the previous twelve months (2.6). Productivity and unit labour costs
stay a G until promoted.

---

## Part 3 — Outputs: what this agent tells the others matters to it

Each row is what this agent needs from that agent, every cycle; it becomes an input row in that
agent's map (window B3). The FX and external agents get no fixed row: the exchange rate and the
global cycle reach jobs through activity and the tradable sectors' output (MT-AT2); a cycle that
needs them asks in the report. For the same reason this agent asks monetary policy nothing about the
Selic path and asks credit only about small firms: rates and credit reach jobs through growth (2.3),
which comes from activity (MT-AT1).

### 3.1 To atividade

| # | What this agent needs | Why it matters to this agent | Flag when | Used in |
|---|---|---|---|---|
| MT-AT1 | **The output-gap path and GDP growth by quarter** (the thesis and its companion row), with the BCB's latest revision | The gap and unemployment are two readings of the same slack: when they disagree, one of them is off (T1); GDP growth is what the two projected paths (unemployment and the CAGED) are built from, through Okun and the employment elasticity (2.3); GDP is the numerator of productivity (T4) | The gap changes sign, is revised materially, or moves against the unemployment reading | 2.1, 2.3, 2.7 |
| MT-AT2 | **Output by sector**: value added by sector and the monthly indicators (industry, retail, services, agriculture, construction), with what is cyclical and what is one-off | T3 compares each sector's employment with its own output: where firms hoard labour, where hiring runs ahead, which sectors lead; and productivity by sector (T4) | A sector's output turns while its employment does not, or a one-off (harvest, extraction) moves a sector | 2.6, 2.7 |

### 3.2 To política monetária

| # | What this agent needs | Why it matters to this agent | Flag when | Used in |
|---|---|---|---|---|
| MT-PM1 | **How the Copom read the labour market at the last meeting**: tight or loosening, wages against productivity, the RPM's labour analyses and its seasonally adjusted unemployment | T1 and T4 confront the Copom's reading; the BCB's seasonally adjusted series moves only with the RPM | The Copom changes its labour language, or an RPM revises its unemployment series | 2.1, 2.7 |

### 3.3 To inflação

| # | What this agent needs | Why it matters to this agent | Flag when | Used in |
|---|---|---|---|---|
| MT-IN1 | **The IPCA path** (quarter and 12 months) | It deflates earnings and the wage bill (T2); past inflation is what wage claims and the minimum-wage rule index to (T4) | The path moves enough to change real wage growth | 2.5, 2.7 |
| MT-IN2 | **Is wage pressure showing in services?** Underlying services against what the gap explains | It is the price-side check of T4: services above the gap's path with a tight labour market supports the wage reading; services in line with the gap says wages are not adding anything | Services diverge from the gap's path for more than one quarter | 2.8 |

### 3.4 To fiscal

| # | What this agent needs | Why it matters to this agent | Flag when | Used in |
|---|---|---|---|---|
| MT-FS1 | **The minimum-wage rule and next year's value, and the transfers to households** (Bolsa Família, BPC, unemployment insurance, abono), with dates | The minimum wage is a floor for a large share of formal wages and is not in the database; transfers change income, participation and the reservation wage outside the labour market | The value is decided, the rule changes, or a transfer programme starts, ends or changes | 2.2, 2.5, 2.9 |
| MT-FS2 | **Public hiring and civil-service pay decisions** | Public employment and earnings are part of the PNAD's totals and move with budgets, not with the cycle | A hiring programme or a pay adjustment is decided | 2.6, 2.9 |

### 3.5 To expectativas

| # | What this agent needs | Why it matters to this agent | Flag when | Used in |
|---|---|---|---|---|
| MT-EP1 | **The consensus for the labour market**: the Focus for unemployment (annual and quarterly) and its revisions; the QPC's NAIRU and gap | Separates surprise from convergence (T5); the market's NAIRU is the benchmark of T1 | The consensus revises unemployment, or a QPC edition moves the NAIRU | 2.1, Part 1 |

### 3.6 To crédito (pending: the credit map does not exist yet)

| # | What this agent needs | Why it matters to this agent | Flag when | Used in |
|---|---|---|---|---|
| MT-CR1 | **Credit supply to small and medium firms**: the banks' reading of supply for that segment and working capital | The firm-level composition note of 2.6: when credit to small firms locks, the job losses land first in small-firm-heavy sectors | Supply to small firms tightens, or working-capital rates jump | 2.6 |

**What this agent tells the others (their side, to be confirmed in their maps in B3).** The labour
slack — unemployment against the NAIRU and the other measures — to activity, inflation and PM; the
wage bill and real income to activity; the phase of the cycle by sector to activity and PM; wages
against productivity and the part of wage pressure beyond the gap to inflation and PM; formal
employment and income, the drivers of household default, to credit; the consensus check on
unemployment, as a reading, to expectations.

---

## Part 4 — Inputs: what the others told this agent matters to them

The mirror of what the other maps ask of the labour market today, written from this side. Until now
they asked it of the activity agent, which held the labour market provisionally; the source row
carries the label in that map, and the window B3 moves the labour part of those rows here. Where a
map reads the labour tables in a channel but has no row yet, the input is **proposed** and marked so;
it becomes a row in that map in B3. FX, external and expectations ask nothing of the labour market
today (the expectations map says it reaches it through the gap, its XS9).

| # | Source row | What the other agent needs | Why it matters to it | How this agent answers |
|---|---|---|---|---|
| ME-PM1 | PM S10 (asked of activity; its labour part moves here) | **The labour market: unemployment against the NAIRU and wages against productivity**, and where the cycle is by sector | The Copom watches wages growing above productivity and a tight labour market; slack decides how much of the gap reaches inflation | T1 (channels 2.1–2.2) and T4 (2.7–2.8), with T3 (2.6) for the phase of the cycle; flag it when the slack reading changes sign against the NAIRU, or real wage growth moves away from productivity |
| ME-IN1 | Inflation 2.4 and the "wages beyond the gap" tempero (reads `mt_pnad` today; its IN-S5 asks income of activity); **proposed** | **Wages against productivity, unit labour costs, and the part of wage pressure the gap does not carry** | Services follow unit labour costs; wages are not in the model, so wage pressure is a tempero (ii) on services only beyond the gap, or it is double counted | T4, channels 2.7 and 2.8: real wage growth, productivity and unit labour costs (G), indexation and the minimum wage, and which part is beyond the gap; flag it when unit labour costs accelerate, or a minimum-wage or indexation decision changes the path |
| ME-AT1 | Activity Q3 and channels 2.4, 2.8 (the labour cross-check of slack and the income driver of consumption; no row yet); **proposed** | **The labour slack and the real wage bill**: unemployment against the NAIRU, the other slack measures, real earnings and the wage bill | Labour slack is the observed cross-check of the gap (Q3); the wage bill is the main driver of household consumption (2.4). **This agent's main product** (user, 2026-10-30): it exists to be an input of activity and of the gap | T1 (2.1–2.2) and T2 (2.3, 2.5), and the thesis by quarter — the unemployment and CAGED paths —, with where its unemployment reading puts the gap against the BCB's; flag it when slack and the gap disagree in direction, or the real wage bill turns |
| ME-AT2 | Activity Q1 (formal employment among the monthly indicators of the nowcast; no row yet); **proposed** | **Employment in the quarter in course and where it is moving by sector** | Formal employment is a monthly signal of the quarter, faster than GDP; the sectors that hire or fire say where the cycle is | T2 and T3, channels 2.3, 2.4 and 2.6: the CAGED and the PNAD of the quarter against the previous one, by sector; flag it when the cyclical sectors turn, or the CAGED and the PNAD diverge |
| ME-CR1 | Credit map (pending) | **Formal employment, unemployment and real income**, the drivers of household default and of the capacity to borrow | Credit concludes on household debt and default (its C5); payroll-deducted credit depends on formal jobs | T1, T2 and the thesis; flag it when formal jobs fall or real income turns |

---

## Part 5 — Concept index

Belongs to chat D (`coordenacao/D_conhecimento.md`): the concept index and the layer 1 of this
agent's literature come after Parts 1–4 are approved.
