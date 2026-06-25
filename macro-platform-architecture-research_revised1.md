# Macro Research Platform — Architecture Decision Research
### Internal Working Document · Asset Management

---

## How to Read This Document

For each option in every building block, we assess four things:

- **Complexity** — rated 1 to 5, combining implementation difficulty and ongoing maintenance burden. Both matter: a tool that is easy to build but hard to keep running is not actually low-complexity.
- **Financial cost** — initial capital expenditure (capex) and estimated annual operating cost (opex). Ranges are indicative, not quotes.
- **Pros and cons** — grounded in the specific context of an asset manager running quantitative macro research.
- **Interactions** — how the choice amplifies or constrains what is possible in the other two building blocks.

The three building blocks — Raw Materials, Process, Deliverables — are deliberately sequential. The decisions made in Raw Materials constrain what is technically feasible in Process. The decisions made in Process constrain what quality of Deliverables is achievable. This means the most important decisions are made first.

---

## Building Block 1: Raw Materials

Raw materials are the inputs to the entire system. There are three categories: **Text** (qualitative and research content), **Quantitative Data** (structured time series and market data), and **News & Web** (real-time and near-real-time intelligence).

*User: The key difference between Text and News would be that News is more lean to real time info, and the Text try to construct foundational base knowlegde. In this sense, the foundation knowlegde is the lens to interpret the New*
---

### 1.1 Text Sources

Text is the primary carrier of macro analysis, research, policy communication, and institutional knowledge. How text enters the system determines whether the platform can synthesize existing knowledge or only retrieve keywords.

#### Option A — PDF Only
**Complexity: 2/5 · Capex: ~$0 · Opex: <$500/yr**

PDF is the dominant format for institutional research: academic papers, central bank communications, broker reports, IMF/World Bank publications, internal memos. PyMuPDF and pdfplumber can extract clean text from most PDFs in seconds; scanned or image-based PDFs require OCR (Tesseract for free, AWS Textract at ~$1.50/1,000 pages for better accuracy). *User: Does the cost come onlyn from having to extract the scanned pdf?*

**Pros**
- Covers the large majority of relevant institutional and academic content
- No licensing or API costs — files are collected directly
- Straightforward ingestion into any LLM pipeline (LangChain and LlamaIndex both handle PDF natively) *User: Will you explain these tools?*
- Familiar to any analyst: the same PDFs they already read

**Cons**
- Tables and charts within PDFs are poorly extracted and often garbled; data within PDFs should not be trusted as structured data *it would work to get mental models only*
- Scanned documents (common for older ANBIMA reports, for example) require OCR, which introduces errors and latency
- Ingestion is manual unless combined with automated download pipelines *I believe some ingestions could be automated.*
- The format contains no real-time content by definition *User: Only fundational knowlegde*

**Key interactions with other blocks**
- This is the natural and best-suited input for any RAG-based knowledge base. Vector DBs *User: What's vector DB?* and PDF text are designed for each other.
- Choosing PDF-only does not block any downstream options, but it does mean your knowledge base reflects historical research, not live intelligence. *User: The News raw material will do that, Text serves as the foundational base.*
- Combining PDF-only with manual data uploads creates a fully offline, zero-automation pipeline — viable for a proof of concept, not for operational use. 

---

#### Option B — Multi-Format Text (PDF + DOCX + Markdown + HTML + TXT)
**Complexity: 3/5 · Capex: ~$500 · Opex: <$1,000/yr**

Expands the ingestion pipeline to cover all common document types. DOCX covers internal research and client communications; Markdown is the output format of many modern research tools and AI systems; HTML enables direct ingestion of web content; TXT covers raw transcripts, data exports, and legacy documents.

**Pros**
- Maximum coverage across all research formats the team actually produces and consumes
- Markdown and plain HTML parse very cleanly with near-zero noise *User: Is markedown the most robust?* 
- Opens the door to ingesting structured output from other AI systems directly
- Materially better automation potential than PDF-only

**Cons**
- Requires separate parsing logic for each format (typically a different library for each); the failure modes differ
- DOCX and HTML often carry significant layout noise (tables used as formatting, repeated headers, navigation menus)
- Higher pipeline complexity to maintain as formats and libraries evolve
- Quality of extraction varies; a rigorous cleaning step is necessary

**Key interactions with other blocks**
- Multi-format text works much better with a managed vector DB than with keyword search; the heterogeneity of sources requires semantic retrieval to be useful.
- If you intend to build a knowledge graph, multi-format text is required — you need varied content from which to extract entities and relationships.
- Pairs well with an orchestrator (Prefect or Dagster) *User: Explain better that tool* to automate conversion and ingestion across formats on a schedule.

---

### 1.2 Quantitative Data
*User: Here I think there is no much question, we have a database in MySQL and a bloomberg license and a structure to several Free API. The data would be organize there and retrieve to feed the analyses and models*

This is the numerical backbone of the platform: the time series, model inputs, dashboard feeds, and alert triggers. The choice here has the largest impact on the overall architecture because it determines the velocity, freshness, and completeness of every downstream output.

#### Option A — Manual Uploads (CSV / Excel)
**Complexity: 1/5 · Capex: ~$0 · Opex: <$200/yr**

Analysts export data from their existing tools (Bloomberg, Reuters, internal systems) and upload flat files manually or via a shared folder. The system reads from a designated ingestion directory.

**Pros**
- Requires no infrastructure; can be operational in hours
- Full analyst control over what data enters the system
- No API rate limits, no licensing complications, no new vendor contracts
- Easy to audit — every dataset has a clear human owner

**Cons**
- Human bottleneck: the system is only as current as the last upload
- Structurally incompatible with real-time dashboards, automated alerts, or any scheduled pipeline
- Does not scale; becomes unmanageable as data coverage expands
- Analysts spending time on data logistics is an opportunity cost

**Key interactions with other blocks**
- Rules out: live dashboards, alert engines, any automated scheduled report that requires fresh data.
- Compatible with: simple RAG knowledge base, basic static reports, a chat interface over historical documents (though the chat will not have access to current market data).
- If chosen in Phase 1, plan the migration to automated APIs as a hard Phase 2 commitment — not a "nice to have."

---

#### Option B — Free Public APIs
**Complexity: 2/5 · Capex: ~$0 · Opex: <$1,000/yr (infrastructure only)**

The macro research community is unusually well-served by free, high-quality public APIs. The key sources for a Brazil-focused fund are:

- **BCB (Banco Central do Brasil) — SGS and Open Data portal**: SELIC, IPCA, exchange rates (PTAX), credit aggregates, external sector data. The `python-bcb` and `DadosAbertosBrasil` libraries provide clean pandas-native access. As of March 2025, the BCB imposed pagination limits on daily series via JSON/CSV, so large historical pulls require batching.
- **IBGE — SIDRA API**: GDP components, PNAD labor data, industrial production (PIM), retail sales (PMC), services (PMS), and CPI detail (IPCA components). The `sidrapy` library is well-maintained.
- **FRED (St. Louis Fed)**: US macro data (Fed Funds, CPI, PCE, payrolls, ISM), international series, and exchange rates. The `fredapi` Python library is the standard wrapper. Excellent historical depth.
- **World Bank Open Data**: Cross-country macro data (GDP, trade, debt, demographics). Good for structural analysis but published with long lags.
- **IPEA Data**: Brazilian fiscal and social data, including primary surplus, public debt, and social indicators. Available via the `ipeadatapy` library.

**Pros**
- Covers approximately 80% of macro time series needed for a Brazil-focused fund at zero licensing cost
- Well-documented, stable, and actively maintained endpoints with good historical depth
- Python libraries handle authentication, pagination, and data normalization
- Enables fully automated, scheduled pipelines without any procurement process
- SELIC, IPCA, USDBRL, fiscal data, and GDP components are all available here at no cost

**Cons**
- Data is published with standard institutional delays: BCB daily series (T+1), IPCA (monthly), GDP (quarterly)
- No market pricing data: equity prices, credit spreads, CDS, or futures are not available here
- Limited equity fundamentals coverage for the fund's stock-specific macro exposure
- Some series require combining multiple sources, which adds data normalization work

**Key interactions with other blocks**
- Enables: automated reports (daily/weekly macro digests), alert engines on macro thresholds (SELIC surprises, IPCA prints), internal dashboards with near-real-time macro data.
- Excellent starting point for Phase 1; a hybrid stack (free APIs + selective premium) is a natural Phase 2 evolution.
- Works well with any orchestration option (Cron is fine for scheduled pulls; Prefect adds monitoring and retry logic).

---

#### Option C — Premium Market Data (Bloomberg / Refinitiv / FactSet)
**Complexity: 3/5 · Capex: $10k–$30k · Opex: $15k–$80k+/yr**

Institutional data terminals and APIs providing real-time or near-real-time market pricing, fundamentals, consensus estimates, and corporate actions. Bloomberg is the dominant platform in Brazilian buy-side; Refinitiv (now LSEG) is a common alternative.

- **Bloomberg Terminal + Bloomberg API (BLPAPI)**: ~$25k/seat/year. The API requires a running terminal for authentication. The Python `blpapi` library is the standard. Comprehensive real-time and historical data for all Brazilian and global asset classes.
- **Refinitiv Eikon / LSEG Data**: Typically ~$15k–$20k/year. `refinitiv.data` Python library. Strong on fixed income and FX analytics.
- **FactSet**: Common for equity research workflows; pricing varies by coverage.

**Pros**
- Comprehensive, institutional-grade data for all asset classes: equities, FX, rates, commodities, CDS
- Built-in data cleaning, corporate actions adjustments, and point-in-time history
- Enables real-time dashboards, live alert engines, and quantitative model inputs at full fidelity
- Consensus estimates and economic surprise data (vs. Bloomberg Survey) are high-value macro signals

**Cons**
- Bloomberg Terminal is one of the highest-cost line items any firm can add; procurement and legal review takes months
- The API requires a live terminal session for authentication — running it on a server requires a server license (additional cost)
- Most macro time series you need are available for free via BCB/FRED/IBGE — paying Bloomberg for SELIC is redundant
- Creates significant vendor lock-in and data format dependency

**Key interactions with other blocks**
- Unlocks: real-time dashboards with live pricing, sophisticated quantitative models using market data, high-quality automated alerts on market events.
- Best used in combination with free APIs (Option B), not as a replacement.
- The cost-benefit is strongest for market pricing and equity fundamentals; weak for pure macro time series.

---

#### Option D — Hybrid Data Stack (Recommended)
**Complexity: 3/5 · Capex: $2k–$10k · Opex: $5k–$30k/yr depending on premium coverage**

The pragmatic configuration for most asset managers: use free public APIs as the primary source for macro time series, and add selective premium coverage for market pricing and equity fundamentals where free alternatives do not exist.

A typical hybrid stack for a Brazil-focused equity/macro fund:
- BCB + IBGE + FRED + IPEA → macro time series (free)
- B3 market data API or Economatica → Brazilian equity data (low-to-medium cost)
- Bloomberg or Refinitiv for FX real-time, credit spreads, and consensus data → targeted premium spend

**Pros**
- Best coverage-to-cost ratio across all options
- Avoids over-reliance on a single vendor
- Free macro coverage is genuinely excellent and should not be paid for
- Premium spending can be targeted at the specific gaps rather than the full terminal

**Cons**
- Multiple connectors, authentication methods, and data schemas to normalize
- Data lineage tracking becomes critical — you need to know which source produced which number
- Some premium vendors have terms that restrict mixing their data with free sources in automated systems (review carefully)
- More complex ETL pipeline to build and maintain

**Key interactions with other blocks**
- This is the data foundation that enables the full range of deliverables (reports, dashboards, alerts, agent analysis).
- Pairs well with Prefect or Dagster orchestration to manage the different update schedules across sources.
- Works with any knowledge base option; data is stored in a structured database (Postgres/TimescaleDB) separate from the document vector store.

---

### 1.3 News & Web Intelligence

News covers the real-time and near-real-time qualitative signal that drives macro markets: policy communications, economic releases, geopolitical events, and market commentary.

#### Option A — Web Search APIs
**Complexity: 1/5 · Capex: ~$0 · Opex: $60–$600/yr**

APIs like Tavily, Brave Search, and Serper provide on-demand web search results in structured format, purpose-built for LLM agent use. A single function call retrieves the top N results for any query with full page content.

**Pros**
- Trivial to implement: one API key, one function call
- Very broad coverage — anything indexed by a search engine is accessible
- Ideal for agent-driven, on-demand research tasks ("what did the Fed say yesterday?")
- Pricing is very low even at high usage volumes

**Cons**
- Not specialized for financial or macro news — general search engines prioritize popular content, not analytical quality
- High noise-to-signal ratio for specific macro questions
- No guaranteed freshness, sourcing, or consistency
- Not appropriate as the sole news source for systematic pipelines — too variable

**Key interactions with other blocks**
- Best used as a tool available to LLM agents for ad-hoc research, not as a primary feed for automated ingestion.
- Incompatible with systematic alert generation — results are too inconsistent for threshold-based triggers.
- Works naturally with any agent framework (LangChain, CrewAI, LlamaIndex all support web search as a native tool).

---

#### Option B — News APIs
**Complexity: 2/5 · Capex: ~$0 · Opex: $600–$6k/yr**

Structured news aggregation services with filtering by source, topic, date, country, and language. Key options:

- **NewsAPI**: Broad coverage, filterable. Free tier limited to headlines only; Developer plan (~$450/yr) provides full article text from 150k+ sources.
- **GDELT Project**: Free global event and news database updated every 15 minutes. Extremely noisy but comprehensive. Good for thematic filters.
- **TheNewsAPI, Marketaux**: Financial news focused. Marketaux specifically targets financial news with ticker tagging.

**Pros**
- Automatable: scheduled pulls on a cron or pipeline cadence fit a standard pipeline model
- Can build persistent thematic filters for macro topics (SELIC, fiscal, inflation, exchange rate)
- GDELT is free with very broad coverage for emerging markets research
- Financial-focused APIs (Marketaux) provide entity tagging that reduces downstream filtering work

**Cons**
- Most valuable sources are behind paywalls — APIs often return only headlines for premium publishers
- Not real-time: typical delay is 5 minutes to 1 hour from publication
- GDELT is heavily noisy and requires significant filtering infrastructure to be useful
- Coverage of Brazilian Portuguese content varies significantly across providers

**Key interactions with other blocks**
- Can feed the knowledge base via scheduled ingestion (news summaries become searchable documents)
- Supports automated report generation (weekly news digest)
- Insufficient alone for real-time alert generation, but supports lagged macro commentary alerts

---

#### Option C — Premium Financial News Feeds
**Complexity: 3/5 · Capex: $5k–$20k · Opex: $20k–$100k+/yr**

Institutional news distribution services designed for programmatic consumption by trading and research systems.

- **Dow Jones DNA (Dow Jones News Archive API)**: Structured delivery of WSJ, Barron's, Dow Jones Newswires
- **Bloomberg News Feed**: Part of Bloomberg terminal agreement; requires separate data licensing for streaming
- **Reuters News Feed**: Available via LSEG/Refinitiv licensing

**Pros**
- Highest quality financial news coverage globally
- Structured metadata: tickers, sectors, countries, event types
- True real-time delivery via streaming APIs
- Full article text with rights to store and process internally (within license terms)

**Cons**
- Enterprise pricing — typically requires annual minimum commitments of $20k+
- Legal complexity around internal redistribution, storage duration, and automated summarization (AI usage rights are not universal in these contracts)
- Almost certainly overkill for an internal research platform in its first iteration
- Often bundled with broader data licensing agreements rather than available standalone

**Key interactions with other blocks**
- Enables real-time alert generation based on news events
- Premium feeds + live dashboard = the full "institutional command center" vision
- Introduces significant legal review requirements before AI processing of news content

---

#### Option D — RSS + Custom Web Scraping
**Complexity: 4/5 · Capex: $1k–$5k (dev time) · Opex: $1k–$4k/yr**

Building a curated list of high-priority sources and ingesting them directly via their RSS feeds or targeted scrapers. Priority targets for a Brazil macro fund:

- **BCB communications**: Copom minutes, Focus Report, IEF, press releases (official RSS feed available)
- **Tesouro Nacional**: Primary balance, debt management reports
- **IBGE**: Press releases for IPCA, GDP, labor market releases
- **Federal Reserve, ECB, BIS**: Policy statements, speeches, working papers
- **Valor Econômico, Folha de S.Paulo, Estadão** (Brazilian business press, scrapers only)
- **FT, Bloomberg Opinion** (partial access via RSS)

**Pros**
- Fully customizable — precisely the sources that matter for the fund's investment thesis
- No per-article cost at operating scale
- Direct access to central bank communications without an intermediary
- Building a proprietary source list creates a genuine competitive advantage

**Cons**
- High maintenance burden: websites change HTML structure frequently; scrapers break silently
- Commercial web scraping of Brazilian news portals operates in a legal grey area (robots.txt compliance, ToS)
- Requires robust orchestration with retry, monitoring, and alerting — cron is not sufficient
- Quality and availability varies; some sources block aggressive scraping

**Key interactions with other blocks**
- Structurally requires an orchestration framework (Option B or C under Orchestration) — this is a hard dependency
- Works well as a feed into the knowledge base: scraped articles are chunked and embedded alongside research PDFs
- Central bank RSS feeds are reliable and low-maintenance; news portal scraping is the high-maintenance portion *User: Could I use a agent to search infos? or that wouldn't be so real time?*

---

## Building Block 2: Process

Process is the engineering layer: how raw materials are cleaned, structured, stored, and made available to AI reasoning. It divides into three decisions: how the knowledge base is architected, how LLMs and agents are used, and how pipelines are orchestrated.

---

### 2.1 Knowledge Base Architecture

The knowledge base is the long-term memory of the system. It determines what the AI can know and retrieve when answering questions, generating reports, or building analysis. This is the most consequential architectural decision because it is the hardest to change after initial deployment. *User: Why?*

#### Option A — File System + Keyword Search *User: Here we have no meaning, just word. It do not understandin synonomus*
**Complexity: 1/5 · Capex: ~$0 · Opex: <$300/yr**

Documents stored in a structured directory or simple database with full-text search (BM25 or SQLite FTS) *User: Explain this tools*. Retrieval uses keyword matching. *User: Is it basically a RAG, right?*

**Pros**
- No new infrastructure; operational in hours
- Completely transparent — you always know exactly what is in the system
- Zero vendor dependency
- Appropriate for a proof-of-concept or pilot with a small, very well-curated document set 

**Cons**
- No semantic search — searching for "monetary policy tightening" will not find a document about "Copom raising the SELIC rate"
- Does not scale beyond a few hundred documents before retrieval quality collapses *User: Important point*
- Cannot support any LLM-powered retrieval pattern (RAG, agents) *User: What's the difference between this and RAG system?*
- Incapable of synthesizing across documents — only retrieves them

**Key interactions with other blocks**
- Rules out: research chat interface, autonomous analyst agent, and any multi-step AI reasoning
- Compatible with: simple manual reports, a basic keyword-searchable document library
- This is a legitimate starting point for document organization, not for AI-powered analysis

---

#### Option B — Vector Database + RAG (Self-Hosted)
**Complexity: 3/5 · Capex: $500–$2k · Opex: $500–$2k/yr** *User: From where come the cost? - this must be indicate for all*

Documents are split into chunks, converted into numerical embeddings (via OpenAI or an open-source model), and stored in a vector database hosted on your own infrastructure. Retrieval finds the most semantically relevant chunks for a given query. This retrieved context is then passed to an LLM for synthesis. *User: That sou

**Primary self-hosting options:**
- **pgvector**: A PostgreSQL extension that adds vector search to an existing database. If you already run Postgres, this is the lowest-overhead path. Supports hybrid search (vector + keyword). Scales well up to ~1–2M vectors before needing specialized tuning.
- **ChromaDB**: Purpose-built vector database, extremely easy to set up (pip install, one line to start). Best for up to ~100M vectors. No external cloud dependency. Actively developed; the Cloud offering reached GA in 2025.
- **Qdrant**: High-performance, supports sophisticated metadata filtering. Well-suited for production workloads with complex retrieval requirements. Can be self-hosted on a single server effectively.

**Pros**
- Complete data sovereignty: documents never leave your infrastructure — important for proprietary research
- No per-query cost beyond fixed compute
- pgvector reuses existing Postgres infrastructure if you already run it
- Right choice if regulatory or compliance requirements mandate on-premise data storage

**Cons**
- DevOps capacity required to manage, monitor, back up, and scale *User: maintanence burden*
- No managed SLAs — infrastructure failures are your problem and your on-call burden *user: SLAs is basically a support, right?*
- Choosing the right chunking strategy, embedding model, and retrieval configuration requires expertise; mistakes significantly degrade quality *User: That an important point. The vectorization must be well done.*
- Performance at very large scale (>10M vectors) requires careful tuning

**Key interactions with other blocks**
- Enables: research chat interface, multi-agent reasoning, report generation with source citation
- Pairs naturally with self-hosted OSS LLM *user: what's this?* (maximum data sovereignty)
- Works with any orchestration option; Prefect/Dagster add reliable monitoring of ingestion pipelines

---

#### Option C — Vector Database + RAG (Managed) - *User: That could be colapse into the former option with the additional changes that come from the managed RAG. I think the final material should contain more profund explation of what's the Vector Database - how that vectorization work in simples terms, and the same for the RAG.*
**Complexity: 2/5 · Capex: ~$0 (free tiers) · Opex: $500–$5k/yr**

Same vector search and RAG architecture as Option B, but hosted by a specialized cloud provider. The provider handles infrastructure, scaling, backups, and SLAs.

**Primary managed options in 2026:**
- **Pinecone**: The most mature managed vector DB. Serverless pricing: $0.33/GB storage, $8.25 per 1M read units, $2.00 per 1M write units. Free tier available. Sub-33ms p99 latency at production scale. No self-hosted option.
- **Weaviate Cloud**: Managed offering with a free Sandbox tier. Native hybrid search (BM25 + vectors) with no extra storage cost for keyword indexes. Agent-native features added in 2025–2026.
- **Qdrant Cloud**: More cost-effective than Pinecone at scale ($500–$800/month at 100M vectors vs. $5,000+). Excellent for complex metadata filtering. Self-hosted option also available.

**Pros**
- No infrastructure to manage; scales automatically with your document volume
- Free tiers enable getting started without commitment
- Native LangChain and LlamaIndex integration: weeks not months to a working prototype
- Managed backups, uptime SLAs, and monitoring are included

**Cons**
- Documents and their embeddings are stored on third-party infrastructure — compliance review required
- Cost scales with volume and query load; high-throughput production use can become expensive (Pinecone especially)
- Vendor lock-in: migrating 100M+ vectors to a different provider incurs significant egress costs and re-embedding work *User: Import point*
- Data sovereignty concerns for a regulated asset manager

**Key interactions with other blocks**
- The fastest path to a working research chat interface or agent prototype
- Best combined with a multi-agent framework (LlamaIndex specifically was designed for this pattern)
- Complement with cold storage (S3 or Postgres) of raw embeddings to protect against vendor lock-in

---

#### Option D — Knowledge Graph *User: In think this option seems more like a wiki from obsidian. Am I right?*
**Complexity: 5/5 · Capex: $5k–$20k · Opex: $3k–$12k/yr**

A graph database that explicitly models entities (countries, companies, indicators, central banks, policies) and the relationships between them ("BCB raises SELIC" → affects → "USDBRL exchange rate" → affects → "IBOV equity index"). Built on Neo4j or Memgraph. *User: Explain this tools*

**Pros**
- Unique capability: multi-hop reasoning across explicitly modeled macro relationships *User: what "mult-hop" is?*
- Enables questions like: "Which sectors have the highest historical sensitivity to a BRL depreciation of more than 10%?"
- Auditable and explainable: every inference path through the graph can be traced *User: that's good*
- Can formally encode decades of macro institutional knowledge into a queryable structure 
- Highly differentiated — no off-the-shelf solution does this for Brazilian macro

**Cons**
- Requires significant domain expertise to design the ontology correctly: what are the entities, what are the relationship types, what are the properties? *User: Could a agent do this?*
- Maintenance intensive as the macro regime evolves (new relationships, deprecated relationships, updated weights)
- Requires Cypher query language expertise in addition to Python *User: What's is this*
- Building the initial graph from scratch requires either manual expert input or LLM-assisted extraction (itself a significant engineering project)

**Key interactions with other blocks**
- This option and multi-agent frameworks (LLM & Agents Option B) are strongly synergistic — agents can traverse the graph to find non-obvious connections
- Often implemented as a complement to vector RAG, not a replacement (GraphRAG pattern) *user: That's specially important. How would that work?* 
- Incompatible with cron-based orchestration *User: What's that?*; graph updates require transactional pipeline management

---

#### Option E — Hybrid RAG + Knowledge Graph (GraphRAG) 
**Complexity: 5/5 · Capex: $10k–$30k · Opex: $8k–$25k/yr**

The combination of a vector database for document retrieval and a knowledge graph for structured relationship reasoning. The LLM agent can draw on both: retrieve relevant research documents semantically, AND traverse the macro relationship graph to understand structural connections. This is the architecture behind Microsoft's GraphRAG research and several production financial research platforms.

**Pros**
- Maximum analytical depth: semantic context from documents + structural reasoning from the graph
- The platform that most closely realizes the "PhD analyst" vision — synthesizes research literature AND structured macro knowledge
- GraphRAG has been shown to produce materially higher quality answers on complex multi-document questions

**Cons**
- The most complex option in the entire architecture map — requires expertise in four distinct systems (vector DB, graph DB, LLM orchestration, data pipelines) *User: Let's go deeper on this topics.*
- Very high risk of over-engineering in early phases; most of the value can be captured with RAG alone initially
- Build time is 6–12 months minimum for a production-quality implementation *User: That's important*
- Strong recommendation: build RAG first, add the knowledge graph as Phase 3

**Key interactions with other blocks**
- Requires multi-agent framework and premium data to fully justify its complexity
- The long-term target architecture if the fund commits to AI-driven macro research as a sustained capability

---

### 2.2 LLM & Agent Layer

This is the AI reasoning core: the system that reads the retrieved context, interprets the data, writes analysis, and executes multi-step research tasks.

#### Option A — Single LLM API
**Complexity: 2/5 · Capex: ~$0 · Opex: $1k–$10k/yr** *User: This is important only If I need to Q&A the agent, right? Because if use the Claude code to organize and maintain the repository, it's not necessary API (I'm asking)*

A direct API call to a frontier language model. The leading options for a macro research context:

- **Claude (Anthropic)**: Claude Opus 4 / Sonnet 4 series. Strong on long-context analysis, instruction-following, and structured output. Extended thinking mode (Opus 4) enables genuine multi-step reasoning. Good for complex document synthesis.
- **GPT-4o (OpenAI)**: Broad capability, best Python ecosystem support via the official SDK, strong structured output.
- Pricing (approximate, 2026): Claude Sonnet ~$3/MTok input, $15/MTok output; GPT-4o similar range.

**Pros**
- Operational in minutes: API key, pip install, write a prompt
- State-of-the-art reasoning quality — these models genuinely perform at graduate-level macro analysis
- No infrastructure to manage
- Easy to swap models as the field improves

**Cons**
- All data sent to external servers — regulatory and compliance review required for proprietary research content
- Cost scales linearly with token volume; heavy use can accumulate significant monthly spend
- Cannot be fine-tuned on your specific investment process or research style
- Single point of failure: API outages affect the entire platform

**Key interactions with other blocks**
- Compatible with any knowledge base option
- Sufficient for: research chat interface, automated report generation, simple data interpretation
- Not sufficient for: autonomous multi-step research, complex tool use, parallel task execution — those require Option B

---

#### Option B — Multi-Agent Framework
**Complexity: 4/5 · Capex: $2k–$8k (dev time) · Opex: $3k–$15k/yr**

Frameworks that enable LLMs to use tools, maintain memory, plan multi-step tasks, and collaborate as specialized sub-agents. The landscape in 2026:

- **LangChain / LangGraph**: The broadest ecosystem, 97k+ GitHub stars. LangGraph (the stateful agent layer) went GA in October 2025 and supports explicit control over branching, retries, and human-in-the-loop steps. Best for complex, stateful workflows. Large hiring pool.
- **LlamaIndex**: RAG-first framework with strong native support for financial document workflows. Best choice when the primary use case is retrieval-augmented analysis (querying a research knowledge base with complex questions).
- **CrewAI**: Role-based multi-agent coordination. Define an Analyst, a Data Researcher, and an Editor; they collaborate on a research memo. Fast to prototype (working multi-agent crew in <50 lines of code). Less control than LangGraph for complex workflows.
- **Anthropic Claude SDK (Agent SDK)**: Anthropic's official agentic framework, the same architecture that powers Claude Code. Gained significant production adoption in 2025–2026. Best for Anthropic-native deployments.

**Pros**
- Enables genuinely autonomous research tasks: "research the impact of fiscal deterioration on USDBRL in the past 10 years and write a memo"
- Agents can use external tools: web search, data APIs, Python code execution, database queries
- Parallel sub-agents can divide research tasks (one agent fetches data, another synthesizes literature, another writes)
- This is the architecture that enables the "PhD analyst" vision

**Cons**
- Debugging multi-step agent failures is significantly harder than debugging a single LLM call *User: We could create a protocol of reasoning steps debug*
- Framework APIs changed rapidly in 2024–2025 (LangChain had breaking changes multiple times); stability has improved but the risk remains
- Hallucination compounds across reasoning steps — without strong validation and human oversight, errors can propagate into decisions
- Testing and evaluation frameworks for agents are still immature; knowing whether your agent is "good enough" is genuinely hard

**Key interactions with other blocks**
- Requires vector RAG knowledge base (Options B, C, or E) — agents need semantic retrieval to function well
- Incompatible with cron orchestration — agent workflows are dynamic and stateful, not schedulable in a static DAG
- Powers: autonomous analyst agent, complex research chat, structured report generation with deep analysis

---

#### Option C — Self-Hosted Open-Source LLM
**Complexity: 5/5 · Capex: $8k–$30k (GPU hardware) · Opex: $8k–$40k/yr**

Running open-source language models (Llama 3, Mistral, Qwen, DeepSeek) on your own GPU infrastructure. A capable research assistant requires at minimum a 70B parameter model, which needs a multi-GPU server (2–4 A100s or H100s) or a capable cloud GPU instance.

**Pros**
- Complete data sovereignty: all data, all inference stays on your hardware
- No per-token cost at high volume — fixed compute cost regardless of usage
- Can be fine-tuned on proprietary research to match your specific investment process and style
- Immune to API provider pricing changes, outages, or policy changes

**Cons**
- Significant and persistent performance gap vs. frontier APIs (Claude Opus, GPT-4o) on complex analytical tasks — the gap narrowed in 2025 but remains material for multi-step reasoning
- Requires ML engineering expertise to serve, scale, monitor, and tune models
- GPU infrastructure is capital-intensive and has ongoing operational overhead
- Not cost-effective at low-to-medium usage volumes (the fixed GPU cost exceeds API costs unless usage is very high)

**Key interactions with other blocks**
- Natural complement to self-hosted vector DB — fully on-premise stack
- The current performance gap makes this a poor choice for the autonomous analyst agent unless you fine-tune specifically for macro reasoning
- Viable for lower-stakes tasks (document classification, entity extraction, summarization) at high volume

---

### 2.3 Orchestration

Orchestration is what runs the pipelines on schedule, handles failures gracefully, monitors data freshness, and coordinates the dependencies between ingestion, processing, and delivery. It is unglamorous and often underweighted in architecture discussions — until something breaks silently in production.

#### Option A — Python Scripts + Cron
**Complexity: 1/5 · Capex: ~$0 · Opex: <$500/yr**

Scheduled shell scripts calling Python ETL scripts. The oldest and simplest approach to pipeline scheduling.

**Pros**
- Every developer can read, understand, and modify it immediately
- No tools to learn, no new infrastructure to run
- Zero licensing cost
- Appropriate for simple, single-step, low-frequency jobs with no dependencies

**Cons**
- No retry logic: if a script fails, it fails silently. You discover this when a dashboard is stale.
- No monitoring or alerting: there is no native mechanism to know a job failed
- Cannot express dependencies between tasks: task A must finish before task B cannot be enforced
- Not suitable for anything stateful, parallel, or multi-step

**Key interactions with other blocks**
- Compatible with: simple periodic data pulls from free APIs, scheduled PDF downloads, basic report generation
- Incompatible with: web scraping pipelines, multi-agent workflows, any pattern requiring retry logic or dependency management
- If chosen in Phase 1, plan migration to Prefect in Phase 2 as a non-negotiable engineering investment

---

#### Option B — Workflow Orchestrator (Prefect / Dagster / Airflow)
**Complexity: 4/5 · Capex: $2k–$6k (setup and dev time) · Opex: $1k–$4k/yr**

Production-grade pipeline management with scheduling, retry logic, dependency graphs, monitoring, alerting, and run history.

**The 2026 consensus on each:**

- **Prefect**: The easiest transition from Python scripts. Any Python function decorated with `@task` and `@flow` becomes an orchestrated, monitored, retriable pipeline. Strong managed cloud option. Best choice for teams whose background is analytics rather than engineering. Prefect Cloud starts at ~$100/month for a small team; self-hosted is free.
- **Dagster**: Asset-centric model — you define *what data you produce* rather than *tasks to run*. Excellent for teams that care about data lineage and quality. Strong dbt integration. Dagster+ pricing: $100/month (Starter) + pay-per-execution. The asset model fits a macro data platform well because each macro series is a first-class asset.
- **Apache Airflow**: The industry standard with the largest ecosystem and hiring pool. More complex to configure than Prefect or Dagster; DAG-based model is task-centric not asset-centric. Best choice if you already run it or plan to hire standard data engineers. Managed by Astronomer if self-hosting is not desired.

**Recommended for this context: Prefect or Dagster.** Airflow's operational complexity is harder to justify for a small in-house team building from scratch.

**Pros**
- Retry logic, monitoring, alerting, and run history are built-in
- Dependency management: ensures data is fresh before a report is generated
- Dashboard for operational visibility into all pipeline runs
- Enables reliable scraping pipelines, multi-source data integration, and scheduled AI analysis

**Cons**
- Learning curve: Prefect and Dagster require understanding their execution model (tasks, flows, assets, schedules)
- Another system to operate and monitor; adds to total infrastructure complexity
- Overkill for very simple, single-step, low-failure-risk pipelines
- Managed cloud costs scale with team size and job frequency

**Key interactions with other blocks**
- Required for: web scraping pipelines, multi-source hybrid data stacks, any pipeline where a failure has downstream consequences
- Pairs naturally with the hybrid data stack, news API ingestion, and multi-agent agent orchestration (note: Prefect/Dagster schedule when to run; agent frameworks determine what to reason about — these are complementary, not competing)

---

#### Option C — Cloud-Native Pipelines
**Complexity: 3/5 · Capex: $1k–$4k · Opex: $500–$3k/yr**

Serverless orchestration using cloud provider-native tools: AWS Step Functions, GCP Workflows, or Azure Logic Apps.

**Pros**
- Fully managed: no orchestration infrastructure to run or maintain
- Native integration with the same cloud's storage and database services
- Pay-per-execution pricing — cost is proportional to actual usage
- Native monitoring and run history in the cloud console

**Cons**
- Significant vendor lock-in to the chosen cloud provider
- Limited Python support compared to Prefect/Airflow for complex data transformation logic
- Step Functions JSON-based state machine definitions are verbose for complex logic
- Requires cloud IAM, VPC, and networking expertise; adds operational complexity of a different kind

**Key interactions with other blocks**
- Works well if the entire stack (vector DB, LLM inference, storage) is already on the same cloud provider
- Incompatible with self-hosted LLM and self-hosted vector DB — creates a hybrid that is architecturally awkward

---

## Building Block 3: Deliverables

Deliverables are what the investment team actually sees and uses. They must be trustworthy, readable, and integrated into the daily workflow. Building beautiful deliverables on top of an unreliable process layer creates a dangerous illusion of rigor.

---

### 3.1 Automated Reporting

#### Option A — Scheduled Reports & Digests
**Complexity: 2/5 · Capex: ~$500 · Opex: <$500/yr**

LLM-generated macro summaries, data commentary, and research digests delivered on a fixed schedule. Outputs can be formatted as PDF, Markdown, or HTML and distributed via email or Slack.

**Typical formats:**
- **Daily macro brief** (Monday–Friday): SELIC expectations, FX, equity performance, key macro releases, overnight news summary
- **Weekly macro digest**: Synthesis of the week's data releases, central bank communications, and notable research
- **Event-driven memos**: Auto-generated within minutes of a Copom decision, GDP release, or IPCA print

**Pros**
- Immediately useful and tangible — easy to demonstrate project value to the board
- Relatively simple to implement once data and LLM API are connected
- Distributable via email or Slack without any additional interface
- Builds analyst trust in the system incrementally

**Cons**
- Static: no drill-down, no ability to ask follow-up questions, no interactivity
- Quality is entirely dependent on the reliability and freshness of the data feeding it
- LLM-generated text requires a review process before distribution to prevent errors in client-facing or investment-decision contexts
- Does not help analysts navigate to the underlying data or reasoning

**Key interactions with other blocks**
- Works with any data option from Option B (free APIs) upward
- A single LLM API is sufficient for this deliverable — no agent framework needed
- Can be built with cron orchestration; Prefect adds monitoring to ensure reports are actually sent

---

#### Option B — Alert & Signal Engine
**Complexity: 3/5 · Capex: $1k–$3k · Opex: $500–$2k/yr**

Automated push notifications when macro variables cross defined thresholds or when significant events are detected. Delivered via Slack, email, or WhatsApp (common in Brazilian buy-side).

**Examples of alerts this could generate:**
- SELIC futures repricing by more than 25bps in a single session
- IPCA monthly print deviates from Focus Survey consensus by more than 0.2 p.p.
- BCB intervenes in the FX market (detected via PTAX volume spike + news classifier)
- Brazilian CDS spread crosses a defined historical percentile

**Pros**
- Proactive: the system notifies the team rather than waiting for them to check a dashboard
- High perceived value relative to its implementation cost
- Can be rules-based (simple threshold crossing) or AI-enhanced (LLM classifies whether news is materially relevant)
- Integrates into existing communication workflows

**Cons**
- Alert fatigue is a real risk if thresholds are too sensitive
- Requires reliable, timely data feeds; alerts on stale data are actively harmful to the investment process
- Threshold rules require ongoing calibration as market regimes change
- AI-enhanced alerts need a systematic human validation process before being trusted for decisions

**Key interactions with other blocks**
- Requires automated data feeds (Option B or C under Data, or D — not compatible with manual uploads)
- Works independently of the knowledge base and LLM layer for simple rules-based alerts
- AI-enhanced alerts require the LLM API layer

---

### 3.2 Dashboards

#### Option A — Internal Dashboard (Streamlit / Dash)
**Complexity: 2/5 · Capex: $1k–$3k · Opex: $500–$2k/yr**

Python-based interactive web applications that any Python developer can build and maintain.

- **Streamlit** (acquired by Snowflake in 2022, remains actively developed): Any Python script with `st.` calls becomes a web app. Approximately half the code of an equivalent Dash app. The dominant choice for internal analytics tools in 2025–2026. Deploys on Streamlit Community Cloud (free), any cloud VM, or Docker. Not multi-process by default; horizontal scaling requires a load balancer.
- **Dash** (Plotly): Built on Flask + React.js + Plotly.js. More control over layout, callback logic, and component behavior. Steeper learning curve. Dash 3 (released 2025) added significant improvements. Better for production applications that need fine-grained control over interactivity.

**Recommended for internal macro dashboards: Streamlit.** Its development speed advantage (half the code, faster iteration) is decisive for a small team. For customer-facing or board-presentation dashboards, Dash or a custom React app is more appropriate.

**Content for a macro dashboard:**
- Macro thermometer: visual summary of key macro variables vs. historical distributions (SELIC, IPCA, USDBRL, IBOV, primary balance)
- Economic surprise index: recent prints vs. consensus across all major releases
- Central bank communication tracker: sentiment and key phrase frequency across BCB/Fed/ECB communications
- Model outputs: GDP nowcast, inflation forecast, FX fair value estimate

**Pros**
- Fast to build: a working Streamlit macro dashboard can be built in days
- Full Python data stack: pandas, plotly, statsmodels, scipy all work natively
- Easily iterable: adding a new panel or data source does not require redesign
- Inexpensive to host

**Cons**
- Not board-presentation quality without significant additional work on design
- Streamlit's full-script rerun model creates performance issues with complex or large data
- Limited enterprise auth and access control without additional configuration
- Not suitable for real-time streaming data without explicit workarounds

**Key interactions with other blocks**
- Works with free APIs and hybrid data stack; not suitable with manual upload-only data
- A single LLM API can power LLM-driven panels within the dashboard (e.g., a natural language summary of what the data says)

---

#### Option B — Live Production Dashboard (React / Tableau / Power BI)
**Complexity: 4/5 · Capex: $5k–$20k · Opex: $3k–$15k/yr**

Enterprise-grade, production-quality dashboards suitable for board presentations, client reporting, and real-time monitoring.

- **Custom React + Recharts/D3**: Maximum control, highest quality output, but requires a dedicated frontend developer. Build time 3–6 months for a comprehensive macro dashboard.
- **Tableau**: Drag-and-drop dashboard builder. $15–35/user/month. Large library of financial chart templates. Does not natively support Python models; data must be pre-processed externally.
- **Power BI**: Microsoft ecosystem; $10–20/user/month. Better Excel/Office integration than Tableau. SQL and Python integration for data prep.
- **Apache Superset**: Open-source BI tool. Free to self-host. Less polished than Tableau/Power BI; requires more configuration.

**Pros**
- Board-presentation quality: professional design, smooth interactivity, full branding control
- Enterprise auth (SSO, LDAP), user permissioning, and audit logging are standard
- Tableau and Power BI can connect directly to databases without manual data preparation
- Real-time data streaming support (WebSocket-capable in custom React builds)

**Cons**
- Significantly more expensive and longer to build than Streamlit
- Tableau and Power BI require separate data preparation pipelines; they are visualization tools, not analysis environments
- Custom React requires frontend engineering skills that may not exist in a quant/data team
- Often over-engineered for purely internal analytical use — Streamlit can serve most internal needs at a fraction of the cost

**Key interactions with other blocks**
- Premium or hybrid data stack is required to justify the real-time dashboard capability
- An orchestration framework (Prefect/Dagster) should be feeding a data warehouse or time-series DB that the dashboard reads from
- This is the right target for client-facing or board deliverables; Streamlit is the right tool for internal iteration

---

### 3.3 AI Interface

#### Option A — Research Chat Interface (RAG Q&A)
**Complexity: 3/5 · Capex: $2k–$6k · Opex: $2k–$8k/yr**

A conversational interface where analysts ask questions in natural language and receive cited answers drawn from the knowledge base. Deployable as a Slack bot, internal web app, or standalone chat interface.

**Example queries this enables:**
- "What does the historical analysis say about the relationship between SELIC cuts and USDBRL appreciation?"
- "Summarize the last three Copom meeting minutes and identify any shift in language about the neutral rate"
- "What does [author name]'s research on the fiscal multiplier in Brazil conclude?"

**Pros**
- Very high user satisfaction — analysts perceive this as a genuine research capability upgrade
- Democratizes access to the full document library; a junior analyst can query the same knowledge base as a senior PM
- Answers are cited to specific source documents, enabling verification
- Deployable as a Slack bot — zero friction to adopt within existing workflows

**Cons**
- Quality is entirely determined by the completeness and quality of the knowledge base; gaps in coverage mean gaps in answers
- Hallucination risk is real when the knowledge base does not contain a directly relevant document — the model may confabulate
- Users require calibration time to understand what the system knows and does not know
- Cannot take actions; retrieval and synthesis only

**Key interactions with other blocks**
- Requires vector RAG knowledge base (managed or self-hosted) — incompatible with keyword-only search
- Works with a single LLM API; does not require an agent framework
- Feeds directly into the knowledge base decisions — the richer the document collection, the better the chat

---

#### Option B — Autonomous Analyst Agent
**Complexity: 5/5 · Capex: $10k–$40k · Opex: $8k–$30k/yr**

A multi-step AI agent that executes research tasks autonomously: fetching live data, querying the knowledge base, running statistical analysis via Python code execution, synthesizing findings, and producing structured deliverables.

**Example tasks this enables:**
- "Analyze the 5-year relationship between Brazilian primary balance deterioration and USDBRL. Fit a regression, identify outliers, and write a one-page memo with implications for the next 6 months."
- "Review the last 12 months of BCB communications and identify any semantic shift in forward guidance language. Compare with what consensus expects."
- "Build a scenario analysis for the portfolio assuming SELIC stays flat, cuts 150bps, or raises 100bps. Estimate the P&L impact on each equity sector."

**Pros**
- The closest realization of the "PhD macro analyst" vision that motivates the entire project
- Combines retrieval, data analysis, code execution, and synthesis in a single workflow
- Dramatically multiplies analyst capacity for data-intensive research tasks
- Creates genuine competitive advantage if implemented well

**Cons**
- Extremely complex to build, test, and trust in a production investment context
- Requires robust human-in-the-loop oversight — autonomous agents can produce confidently wrong analysis
- LLM API costs for long reasoning runs are significant; extended tasks can cost $5–20 per run
- Evaluation is genuinely hard: how do you know if the agent's analysis is correct? This requires systematic back-testing and validation processes
- Build time is 6–12 months to production-ready quality

**Key interactions with other blocks**
- Requires: multi-agent framework, vector RAG knowledge base, reliable data APIs, and an orchestration framework
- Premium market data dramatically improves the quality of agent analysis by providing institutional-grade inputs
- This is a Phase 3 deliverable; attempting to build it in Phase 1 is the most common mistake in projects like this

---

## Cross-Cutting Interaction Rules

The most important design constraints arise from the interactions between building block choices. These are the rules that determine whether your selections are coherent as a system.

**Rule 1 — Data is the hardest constraint**
The data choice limits everything downstream. Manual uploads block live dashboards and alerts permanently. Free public APIs support most Phase 1 deliverables but cap your market data quality. No amount of sophisticated AI can compensate for stale or incomplete data inputs.

**Rule 2 — The knowledge base choice is the hardest to reverse**
Once documents are chunked and embedded in a vector DB, migration to a different system requires re-processing everything. The choice between self-hosted and managed is particularly sticky. Make this decision with multi-year scalability in mind, not just current convenience.

**Rule 3 — Cron and agents cannot coexist**
Cron job scheduling and multi-agent workflows are architecturally incompatible. Agent workflows are dynamic, stateful, and failure-prone in unpredictable ways. If you plan to use agents, you need Prefect, Dagster, or Airflow from the start. Retrofitting orchestration onto a cron-based system is painful and disruptive.

**Rule 4 — The autonomous agent is a Phase 3 deliverable**
Building toward the autonomous analyst agent requires: working vector RAG + working data pipelines + working orchestration + working LLM integration. None of these can be skipped. Teams that try to build the agent before the foundation is solid consistently fail. The chat interface (Option A under AI Interface) is the right Phase 2 target — it is structurally similar to the agent but significantly simpler to validate and trust.

**Rule 5 — Cost compounds across the stack**
Premium data + managed vector DB + frontier LLM API + live dashboard platform can add up to $150k+/year if all premium options are chosen simultaneously. The free and low-cost options are genuinely good; use them in Phase 1 and add premium spend only where the specific gap justifies it.

**Rule 6 — Web scraping requires a production orchestrator**
RSS feeds and custom scrapers will fail silently if run via cron. Sites change structure, rate limits are hit, and servers go down. If web scraping is part of your news strategy, Prefect or Dagster is a hard requirement — budget for the operational overhead accordingly.

---

## Complexity and Cost Summary

| Option | Category | Complexity | Annual Opex |
|---|---|---|---|
| PDF Only | Text | 2/5 | <$500 |
| Multi-format Text | Text | 3/5 | <$1k |
| Manual Data Uploads | Data | 1/5 | <$200 |
| Free Public APIs | Data | 2/5 | <$1k |
| Premium Data (Bloomberg) | Data | 3/5 | $15k–$80k+ |
| Hybrid Data Stack | Data | 3/5 | $5k–$30k |
| Web Search APIs | News | 1/5 | <$600 |
| News APIs | News | 2/5 | $600–$6k |
| Premium News Feeds | News | 3/5 | $20k–$100k+ |
| RSS + Scraping | News | 4/5 | $1k–$4k |
| File System + Keyword | Knowledge Base | 1/5 | <$300 |
| Vector RAG (Self-hosted) | Knowledge Base | 3/5 | $500–$2k |
| Vector RAG (Managed) | Knowledge Base | 2/5 | $500–$5k |
| Knowledge Graph | Knowledge Base | 5/5 | $3k–$12k |
| Hybrid RAG + Graph | Knowledge Base | 5/5 | $8k–$25k |
| Single LLM API | LLM & Agents | 2/5 | $1k–$10k |
| Multi-Agent Framework | LLM & Agents | 4/5 | $3k–$15k |
| Self-Hosted OSS LLM | LLM & Agents | 5/5 | $8k–$40k |
| Cron Scripts | Orchestration | 1/5 | <$500 |
| Workflow Orchestrator | Orchestration | 4/5 | $1k–$4k |
| Cloud-Native Pipelines | Orchestration | 3/5 | $500–$3k |
| Automated Reports | Deliverables | 2/5 | <$500 |
| Alert Engine | Deliverables | 3/5 | $500–$2k |
| Internal Dashboard (Streamlit) | Deliverables | 2/5 | $500–$2k |
| Live Dashboard (React/Tableau) | Deliverables | 4/5 | $3k–$15k |
| Research Chat Interface | Deliverables | 3/5 | $2k–$8k |
| Autonomous Analyst Agent | Deliverables | 5/5 | $8k–$30k |

---

## Proposed Phased Approach (For Discussion)

### Phase 1 — Prove the Concept (0–4 months, ~$5k–$15k/year total)
**Goal:** A working system the team uses daily, that demonstrably improves research quality.

- Text: PDF + Markdown ingestion
- Data: Free public APIs (BCB, IBGE, FRED, IPEA)
- News: Web search APIs + BCB RSS
- Knowledge Base: Managed vector DB (Weaviate Cloud or Qdrant free tier)
- LLM: Single LLM API (Claude Sonnet 4)
- Orchestration: Prefect (open source, self-hosted)
- Deliverables: Weekly automated macro digest + Internal Streamlit dashboard + Research chat interface via Slack

This stack can be built by 1–2 engineers in 8–12 weeks and gives the team three real deliverables to evaluate.

### Phase 2 — Automate and Expand (4–12 months, ~$15k–$40k/year total)
**Goal:** Operational reliability, live data, and alert capability.

- Data: Migrate to Hybrid Stack (free APIs + selective premium for FX and equity data)
- News: Add News APIs + BCB/central bank scraping with Prefect monitoring
- Knowledge Base: Expand document collection; evaluate self-hosted vector DB for data sovereignty
- LLM: Evaluate multi-agent framework for report automation
- Deliverables: Add alert engine + Upgrade dashboard toward Dash or semi-custom React

### Phase 3 — The PhD Analyst (12–24 months, ~$40k–$100k/year total)
**Goal:** Autonomous research capability that redefines the team's analytical capacity.

- Knowledge Base: Evaluate knowledge graph layer for macro relationship modeling
- LLM: Deploy multi-agent framework with code execution and data analysis tools
- Deliverables: Autonomous analyst agent for on-demand quantitative research tasks + Live production dashboard for fund monitoring

---

*Document prepared for internal discussion. All cost estimates are indicative based on publicly available pricing as of mid-2026. Actual costs depend on usage volume, contract terms, and infrastructure choices.*
