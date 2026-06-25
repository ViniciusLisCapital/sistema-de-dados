# Macro Research Platform — Architecture Decision Research
### Internal Working Document · Asset Management · Version 2.0

---

## How to Read This Document

For each option in every building block, we assess four things:

- **Complexity** — rated 1 to 5, combining implementation difficulty and ongoing maintenance burden. Both matter: a tool that is easy to build but hard to keep running is not actually low-complexity.
- **Financial cost** — initial capital expenditure (capex) and estimated annual operating cost (opex). Ranges are indicative, not quotes.
- **Pros and cons** — grounded in the specific context of an asset manager running quantitative macro research.
- **Interactions** — how the choice amplifies or constrains what is possible in the other two building blocks.

The three building blocks — Raw Materials, Process, Deliverables — are deliberately sequential. The decisions made in Raw Materials constrain what is technically feasible in Process. The decisions made in Process constrain what quality of Deliverables is achievable. This means the most important decisions are made first.

**A design principle that shapes the whole architecture:** Text and News are not simply two types of inputs — they serve fundamentally different cognitive roles in the system. Text sources build the foundational knowledge base: the conceptual frameworks, historical analysis, and institutional understanding that form the analytical lens. News is the real-time signal that gets interpreted through that lens. A Copom decision is a data point; what it means for inflation expectations, the exchange rate, or the equity market is a judgment that depends on the conceptual framework established by the foundational knowledge. The architecture should reflect this: Text feeds the long-term knowledge base, News feeds the real-time intelligence layer, and the agent applies the former to interpret the latter.

---

## Glossary of Technical Terms

This glossary defines technical terms used throughout the document. Readers familiar with these concepts can skip ahead.

**Agent / AI agent** — A language model equipped with tools it can call autonomously to complete a task. Instead of answering a question directly, an agent can search the web, read files, query a database, or run Python code as part of its reasoning process. The key distinction from a simple chatbot is that an agent takes actions, not just generates text.

**Agent framework** — A software library that makes it easier to build agents. It provides pre-built patterns for tool use, memory, multi-step reasoning, and agent-to-agent coordination. Examples: LangChain, LlamaIndex, CrewAI.

**BM25** — A text ranking algorithm used for search. Given a query, BM25 scores all documents by how well they match the query terms, accounting for how often terms appear and how long the document is. It is more sophisticated than simple keyword matching but less semantically aware than vector search. A BM25 search for "monetary tightening" will not find a document about "raising the policy rate" unless those exact words appear.

**Cron / Cron job** — A Unix scheduling system. You write a time expression (e.g., "every weekday at 8am") and it fires a command on that schedule. It has no awareness of whether the command succeeded, cannot retry on failure, cannot alert you if something goes wrong, and cannot coordinate dependencies between tasks. It is the simplest possible scheduler.

**Cypher** — The query language for Neo4j and Memgraph graph databases, equivalent to SQL for relational databases. Example: `MATCH (country:Brazil)-[:CONTROLS]->(rate:SELIC)-[:AFFECTS]->(fx:USDBRL) RETURN rate, fx` retrieves all paths where Brazil's SELIC rate affects the USDBRL exchange rate.

**Embedding** — A numerical representation of a piece of text that captures its meaning. A sentence like "the central bank raised interest rates" is converted into a list of hundreds of numbers (a vector) in such a way that sentences with similar meanings produce similar vectors. This is what allows semantic search: you search by meaning, not by keywords.

**GraphRAG** — A retrieval pattern that combines a vector database (for semantic document search) and a knowledge graph (for structured relationship reasoning) as context sources for an LLM. The LLM receives both: text evidence from documents and structural relationships from the graph.

**Knowledge graph** — A database that stores information as nodes (entities: countries, indicators, policies, institutions) and edges (relationships: "SELIC affects USDBRL", "fiscal deterioration causes BRL depreciation"). Unlike a relational database that stores rows and columns, a knowledge graph stores explicitly typed relationships. Queried programmatically by an agent.

**LangChain / LangGraph** — LangChain is a software framework for building LLM applications: it provides pre-built patterns for chaining prompts, connecting to data sources, and using tools. LangGraph is LangChain's layer specifically for stateful, multi-step agent workflows where the agent's progress and decisions need to be tracked and controlled explicitly.

**LlamaIndex** — A software framework focused specifically on connecting LLMs to data: documents, databases, APIs. Where LangChain covers broad LLM application patterns, LlamaIndex specializes in the retrieval side — ingesting documents, building vector indexes, and querying them efficiently. Particularly strong for document-heavy workflows like a research knowledge base.

**Multi-hop reasoning** — The ability to follow a chain of connections across multiple steps to answer a question. Example: to answer "how does fiscal deterioration affect inflation?", a system might traverse: fiscal deterioration → debt sustainability risk → BRL depreciation pressure → imported inflation → IPCA impact. Each step is one "hop." A keyword search can only find documents that explicitly mention all these terms together; a knowledge graph traverses the chain through explicitly stored relationships.

**Neo4j / Memgraph** — Graph database systems. Neo4j is the most mature and widely used; Memgraph is a newer, faster alternative optimized for real-time queries. Both store data as nodes and relationships and are queried via the Cypher language.

**Ontology** — In the knowledge graph context, the schema that defines what kinds of entities exist (Country, Indicator, Policy, Institution) and what kinds of relationships are valid between them (CONTROLS, AFFECTS, RESPONDS_TO). Designing an ontology requires deep domain expertise — it is the intellectual framework that determines what the graph can and cannot express.

**Orchestrator agent** — In a multi-agent system, the top-level agent responsible for receiving a task, breaking it into sub-tasks, delegating them to specialist agents, and consolidating their outputs into a final result.

**Prefect / Dagster / Airflow** — Workflow orchestration tools. Think of them as a major upgrade from cron: instead of a timer that fires a script and forgets, these tools know whether a pipeline run succeeded, retry it automatically on failure, alert the team if something goes wrong, enforce dependencies between tasks (task B only runs after task A succeeds), and provide a dashboard showing the full run history of all pipelines. The difference between cron and Prefect is roughly the difference between a physical alarm clock and a modern calendar application with reminders, snooze, and notifications.

**RAG (Retrieval-Augmented Generation)** — A pattern where an LLM's response is grounded in documents retrieved from a knowledge base. Instead of answering from memory alone, the LLM first searches the knowledge base for relevant content, then uses that content as context when generating its response. This dramatically reduces hallucination and enables the model to answer questions about specific documents or datasets.

**Vector database** — A database that stores documents as embeddings (numerical vectors) and retrieves them by semantic similarity rather than keyword matching. When you search, the database finds documents whose meaning is closest to your query, even if they use different words. This is what makes questions like "what does the literature say about monetary dominance?" work even when no document uses that exact phrase.

**Wiki-link** — In Obsidian and other markdown-based tools, a `[[link]]` syntax that creates a navigable connection between two notes. Wiki-links are the foundation of the explicit relationship graph in an Obsidian vault.

---

## Building Block 1: Raw Materials

Raw materials are the inputs to the entire system. There are three categories: **Text** (foundational knowledge content), **Quantitative Data** (structured time series and market data), and **News & Web** (real-time and near-real-time intelligence signals).

The distinction between Text and News is more than a format difference — it reflects two different roles in the analytical process. Text builds the lens: the conceptual frameworks, empirical research, and historical understanding that an analyst uses to interpret events. News provides what is being interpreted: policy decisions, data releases, market developments. A sophisticated AI research system mirrors this structure, using Text to build a deep knowledge base and News as the real-time input stream that gets analyzed through that base.

---

### 1.1 Text Sources

Text is the primary carrier of macro analysis, research, policy communication, and institutional knowledge. How text enters the system determines whether the platform can synthesize existing knowledge or only retrieve keywords.

#### Option A — PDF Only
**Complexity: 2/5 · Capex: ~$0 · Opex: <$500/yr**

PDF is the dominant format for institutional research: academic papers, central bank communications, broker reports, IMF/World Bank publications, internal memos.

**On cost:** The <$500/yr covers server infrastructure only. PDF processing itself is free for standard digital PDFs — PyMuPDF and pdfplumber are open-source Python libraries that extract text in seconds at no cost. The only additional cost arises specifically with scanned or image-based PDFs, which require Optical Character Recognition (OCR). Tesseract (free, open-source) handles this locally; AWS Textract (~$1.50/1,000 pages) provides better accuracy for complex layouts but adds cost. If your document set is predominantly digital PDFs from publishers and central banks, the OCR cost is near zero.

**On automation:** Many high-value sources can be automated. BCB publishes Copom minutes, the IEF, and Focus Reports on a regular, predictable schedule. The IMF, BIS, and Federal Reserve all publish research with consistent URL patterns. A simple download script run on a schedule (via Prefect) can pull new documents automatically without manual intervention. True manual effort is mainly required for curating documents from sources without predictable publication patterns — broker reports, academic papers, internal research.

**On LangChain and LlamaIndex:** These are software frameworks that simplify the process of connecting language models to documents. LangChain provides general-purpose patterns for building LLM applications; it has a pre-built PDF loader that handles all the parsing and chunking automatically. LlamaIndex focuses specifically on the retrieval side — ingesting documents into a searchable index and querying them efficiently. In practice, you use these libraries so you do not have to write the document parsing, chunking, and retrieval logic from scratch. See the Glossary for fuller definitions.

**Pros**
- Covers the large majority of relevant institutional and academic content
- No licensing or API costs — files are collected directly
- Straightforward ingestion via LangChain or LlamaIndex — the parsing is handled by the library
- Familiar to any analyst: the same PDFs they already read
- Many key sources (BCB, IMF, Fed) can be downloaded automatically on a schedule

**Cons**
- Tables and charts within PDFs are extracted as garbled text, not structured data. This is acceptable for conceptual and qualitative content — PDFs work well as a source of mental models, frameworks, and analytical reasoning — but numerical data within PDFs should always come from the dedicated quantitative data sources instead
- Scanned documents (older ANBIMA reports, archived research) require OCR, which introduces errors
- Ingestion of non-scheduled sources requires manual curation decisions — which documents belong in the knowledge base
- The format contains no real-time content by definition; this is by design, as Text is the foundational knowledge base, not the real-time signal layer (which is News)

**Key interactions with other blocks**
- The natural and best-suited input for any vector-based knowledge base. Semantic retrieval and PDF text are purpose-built for each other — this combination is the industry standard for AI research assistants
- Choosing PDF-only does not block downstream options; it simply means your knowledge base reflects deep historical and analytical content. The real-time layer is handled by the News building block
- Combining PDF-only with manual data uploads creates a fully offline pipeline — viable for a proof of concept, but plan automated data feeds as a Phase 2 requirement

---

#### Option B — Multi-Format Text (PDF + DOCX + Markdown + HTML + TXT)
**Complexity: 3/5 · Capex: ~$500 · Opex: <$1,000/yr**

Expands the ingestion pipeline to cover all common document types. DOCX covers internal research and client communications; Markdown is the output format of many modern research tools and AI systems; HTML enables direct ingestion of web content; TXT covers raw transcripts, data exports, and legacy documents.

**On Markdown robustness:** Yes — Markdown is the most robust text format for this use case. It is pure text with minimal, explicit formatting syntax. There is no binary encoding, no embedded metadata, no layout engine, no rendering dependencies. A Markdown file parses with 100% fidelity on any system using any library. It converts cleanly to HTML, PDF, or plain text without information loss. This is why modern research tools, AI systems, and the Obsidian-based architecture discussed later all output Markdown: it is the format least likely to introduce noise during processing.

**Pros**
- Maximum coverage across all research formats the team produces and consumes
- Markdown and plain HTML parse cleanly with near-zero noise
- Opens the door to ingesting structured output from other AI systems (Claude Code synthesis outputs, for example)
- Better automation potential — internal documents and external web content can be ingested alongside PDFs

**Cons**
- Requires separate parsing logic for each format; the failure modes of a DOCX parser differ from those of an HTML parser
- DOCX and HTML often carry significant layout noise — navigation menus, repeated headers, formatting tables — that requires a cleaning step
- Higher pipeline complexity to maintain as formats and libraries evolve
- Quality of extraction varies; rigorous cleaning is necessary for heterogeneous sources

**Key interactions with other blocks**
- Works much better with a vector database than with keyword search; heterogeneous sources demand semantic retrieval to be useful
- If a knowledge graph is on the long-term roadmap, multi-format text is a better foundation — varied content produces richer entity and relationship extraction
- Pairs naturally with a workflow orchestrator (Prefect or Dagster — see Glossary) to automate format conversion and ingestion across different source types on a defined schedule

---

### 1.2 Quantitative Data

**Note on the team's existing setup:** Based on the discussion, the quantitative data layer is largely settled: a MySQL database stores structured time series, Bloomberg provides market pricing and consensus data, and free public APIs (BCB, IBGE, FRED, IPEA) cover macro series. This corresponds to Option D (Hybrid Data Stack) in the framework below. The sections below are kept for completeness and to document the rationale behind that choice, but the selection decision has effectively been made. The relevant remaining questions are about how this existing data infrastructure connects to the process and deliverables layers.

This is the numerical backbone of the platform: the time series, model inputs, dashboard feeds, and alert triggers. The choice here has the largest impact on the overall architecture because it determines the velocity, freshness, and completeness of every downstream output.

#### Option A — Manual Uploads (CSV / Excel)
**Complexity: 1/5 · Capex: ~$0 · Opex: <$200/yr**

Analysts export data from their existing tools and upload flat files manually or via a shared folder.

**Pros**
- Requires no infrastructure; operational in hours
- Full analyst control over what data enters the system
- No API rate limits or licensing complications

**Cons**
- Human bottleneck: the system is only as current as the last upload
- Structurally incompatible with real-time dashboards, automated alerts, or any scheduled pipeline
- Does not scale; becomes unmanageable as data coverage expands

**Key interactions with other blocks**
- Rules out: live dashboards, alert engines, any automated report requiring fresh data
- If chosen in Phase 1, plan migration to automated APIs as a hard Phase 2 commitment

---

#### Option B — Free Public APIs
**Complexity: 2/5 · Capex: ~$0 · Opex: <$1,000/yr (infrastructure only)**

The macro research community is unusually well-served by free, high-quality public APIs. The key sources for a Brazil-focused fund:

- **BCB (Banco Central do Brasil) — SGS and Open Data portal**: SELIC, IPCA, PTAX exchange rates, credit aggregates, external sector data. The `python-bcb` and `DadosAbertosBrasil` libraries provide clean pandas-native access. As of March 2025, the BCB imposed pagination limits on daily series, so large historical pulls require batching.
- **IBGE — SIDRA API**: GDP components, PNAD labor data, industrial production (PIM), retail sales (PMC), services (PMS), IPCA components. The `sidrapy` library is well-maintained.
- **FRED (St. Louis Fed)**: US macro data (Fed Funds, CPI, PCE, payrolls, ISM), international series, exchange rates. The `fredapi` Python library is the standard wrapper.
- **World Bank Open Data**: Cross-country macro data (GDP, trade, debt, demographics). Good for structural analysis but published with long lags.
- **IPEA Data**: Brazilian fiscal and social data — primary surplus, public debt, social indicators. Available via `ipeadatapy`.

**Pros**
- Covers approximately 80% of macro time series needed at zero licensing cost
- SELIC, IPCA, USDBRL, fiscal data, and GDP components all available here
- Enables fully automated, scheduled pipelines without any procurement process

**Cons**
- Standard institutional publication delays: BCB daily series (T+1), IPCA (monthly), GDP (quarterly)
- No market pricing data: equity prices, credit spreads, CDS, or futures not available here
- Limited equity fundamentals coverage

**Key interactions with other blocks**
- Enables: automated macro digests, threshold alerts, internal dashboards with near-real-time macro data
- The natural complement to Bloomberg for a hybrid stack

---

#### Option C — Premium Market Data (Bloomberg / Refinitiv / FactSet)
**Complexity: 3/5 · Capex: $10k–$30k · Opex: $15k–$80k+/yr**

Institutional terminals and APIs providing real-time pricing, fundamentals, consensus estimates, and corporate actions. Bloomberg Terminal (~$25k/seat/year) is the standard in Brazilian buy-side; Refinitiv (~$15k–$20k/year) is a common alternative.

**Pros**
- Comprehensive, institutional-grade data for all asset classes
- Consensus estimates and economic surprise data are high-value macro signals
- Enables real-time dashboards and sophisticated quantitative model inputs

**Cons**
- Bloomberg Terminal: one of the highest-cost line items a firm can add; months for procurement and legal review
- API requires a live terminal session for authentication (server license costs extra)
- Most pure macro time series are available free via BCB/FRED/IBGE — paying Bloomberg for SELIC is redundant

**Key interactions with other blocks**
- Unlocks: real-time dashboards, live alert engines, quantitative models at full fidelity
- Best used in combination with free APIs, not as a replacement

---

#### Option D — Hybrid Data Stack (Current team configuration — Recommended)
**Complexity: 3/5 · Capex: $2k–$10k · Opex: $5k–$30k/yr depending on premium coverage**

The pragmatic configuration: free public APIs as the primary source for macro time series, premium coverage for market pricing and equity fundamentals. The team's current setup (MySQL + Bloomberg + free APIs) implements this pattern.

**On MySQL as the storage layer:** MySQL is a general-purpose relational database, not a time series database. For this use case, that distinction matters less than it might appear. The volumes involved — thousands of daily and monthly macro series — are modest by database standards. Standard SQL handles date-range queries, joins between series, and basic rolling calculations adequately. The main ergonomic limitation is that time series operations (rolling averages, resampling, gap-filling, lead/lag) are more expressive in PostgreSQL (richer window functions) or TimescaleDB (purpose-built for time series). However, since most quantitative analysis happens in Python with pandas anyway — pulling data out of the database and computing in memory — the SQL ergonomics matter less than they would in a pure SQL workflow. MySQL is adequate for this use case; PostgreSQL would be a low-friction upgrade that opens TimescaleDB as a future path.

**Pros**
- Best coverage-to-cost ratio across all options
- Free macro coverage is genuinely excellent — BCB, IBGE, and FRED together cover the core
- Premium spending targeted at specific gaps (real-time pricing, equity fundamentals, consensus)
- Not locked into a single vendor

**Cons**
- Multiple connectors, authentication methods, and data schemas to normalize
- Data lineage tracking is critical — you need to know which source produced which number
- Some premium vendors restrict mixing their data with free sources in automated systems (review contracts carefully)

**Key interactions with other blocks**
- This data foundation enables the full range of deliverables (reports, dashboards, alerts, agent analysis)
- Pairs naturally with Prefect or Dagster to manage different update schedules across sources
- The MySQL database is a separate layer from the document vector store — they serve different purposes and are queried differently


---

### 1.3 News & Web Intelligence

News covers the real-time and near-real-time qualitative signal that drives macro markets: policy communications, economic data releases, geopolitical events, and market commentary. Within the architecture described in this document, News plays a distinct role from Text: it is not foundational knowledge but rather the live stream of events that the foundational knowledge is used to interpret. A well-designed system uses the Text knowledge base as the analytical framework and routes incoming News through that framework to produce timely, grounded assessments.

#### Option A — Web Search APIs
**Complexity: 1/5 · Capex: ~$0 · Opex: $60–$600/yr**

APIs like Tavily, Brave Search, and Serper provide on-demand web search in structured format, purpose-built for LLM agent use.

**Pros**
- Trivial to implement: one API key, one function call
- Broad coverage — anything indexed by a search engine is accessible
- Ideal for agent-driven, on-demand research tasks ("what did the Fed say yesterday?")
- Low cost even at moderate usage volumes

**Cons**
- Not specialized for financial or macro news — general search engines prioritize popular content, not analytical quality
- High noise-to-signal ratio for specific macro questions
- No guaranteed freshness, sourcing, or consistency
- Not appropriate as the sole news source for systematic pipelines

**Key interactions with other blocks**
- Best used as a tool available to LLM agents for ad-hoc research, not as a primary ingestion feed
- Incompatible with systematic alert generation — results are too inconsistent
- Works naturally with any agent framework (LangChain, CrewAI, LlamaIndex all support web search as a native tool)

---

#### Option B — News APIs
**Complexity: 2/5 · Capex: ~$0 · Opex: $600–$6k/yr**

Structured news aggregation with filtering by source, topic, date, country, and language. Key options: NewsAPI (broad coverage, ~$450/yr for full article text), GDELT Project (free, global, very noisy), Marketaux (financial news with ticker tagging).

**Pros**
- Automatable: scheduled pulls fit a standard pipeline cadence
- Can build persistent thematic filters for macro topics (SELIC, fiscal, inflation, exchange rate)
- GDELT is free with broad emerging market coverage

**Cons**
- Most valuable sources are behind paywalls — APIs often return only headlines
- Real-time delay of 5 minutes to 1 hour
- Brazilian Portuguese content coverage varies significantly across providers

**Key interactions with other blocks**
- Can feed the knowledge base via scheduled ingestion (news summaries become searchable documents)
- Supports automated macro digest generation and lagged commentary alerts

---

#### Option C — Premium Financial News Feeds
**Complexity: 3/5 · Capex: $5k–$20k · Opex: $20k–$100k+/yr**

Institutional distribution services: Dow Jones DNA, Bloomberg News Feed, Reuters via LSEG. Real-time streaming, structured metadata, full article text with AI processing rights (review contract terms carefully — not universal).

**Pros**
- Highest quality and most complete financial news coverage globally
- Structured metadata: tickers, sectors, countries, event types
- True real-time streaming delivery

**Cons**
- Enterprise pricing — annual minimum commitments of $20k+
- Legal complexity around internal redistribution and AI-based summarization
- Almost certainly overkill for an internal research platform in its first iteration

**Key interactions with other blocks**
- Enables real-time alert generation based on news events
- Premium news + live dashboard = the full "institutional command center" configuration

---

#### Option D — RSS + Custom Web Scraping
**Complexity: 4/5 · Capex: $1k–$5k (dev time) · Opex: $1k–$4k/yr**

A curated list of high-priority sources ingested directly via RSS feeds or targeted scrapers. Priority targets for a Brazil macro fund: BCB Copom communications and IEF (official RSS available), Tesouro Nacional, IBGE press releases, Federal Reserve/ECB/BIS policy communications, Valor Econômico, FT.

**Pros**
- Fully customizable — precisely the sources that matter for the fund's investment thesis
- No per-article cost at operating scale
- Direct access to central bank communications without an intermediary
- Proprietary source selection creates a competitive advantage

**Cons**
- High maintenance burden: sites change HTML structure frequently; scrapers break silently
- Commercial scraping operates in a legal grey area (robots.txt, Terms of Service)
- Requires robust orchestration with retry and monitoring — cron is structurally insufficient for this

**Key interactions with other blocks**
- Hard dependency on a workflow orchestrator (Prefect or Dagster) — this is not optional
- Works well as a feed into the knowledge base: scraped articles are chunked and embedded alongside research PDFs
- Central bank RSS feeds are reliable and low-maintenance; news portal scraping is the high-maintenance portion

---

## Building Block 2: Process

Process is the engineering layer: how raw materials are cleaned, structured, stored, and made available to AI reasoning. It divides into three decisions: how the knowledge base is architected, how LLMs and agents are configured, and how pipelines are orchestrated.

---

### 2.1 Knowledge Base Architecture

The knowledge base is the long-term memory of the system. It determines what the AI can know and retrieve when answering questions, generating reports, or building analysis. This is the most consequential architectural decision because it is the hardest to change after initial deployment.

#### Option A — File System + Keyword Search
**Complexity: 1/5 · Capex: ~$0 · Opex: <$300/yr**

Documents stored in a structured directory with full-text search using keyword matching (BM25 or SQLite FTS). Retrieval finds documents containing the query words.

**Pros**
- No new infrastructure; operational immediately
- Completely transparent and auditable
- Zero vendor dependency

**Cons**
- No semantic search — searching for "monetary tightening" will not find a document about "raising the SELIC rate" unless those exact words appear together
- Does not scale beyond a few hundred documents before retrieval quality collapses
- Cannot support any LLM-powered retrieval pattern (RAG)
- Incapable of knowledge synthesis across documents

**Key interactions with other blocks**
- Rules out: research chat interface, autonomous analyst agent, any multi-step AI reasoning
- Compatible with: simple keyword-searchable document library
- This is a legitimate starting point for document organization, not for AI-powered analysis

---

#### Option B — Vector Database + RAG (Self-Hosted)
**Complexity: 3/5 · Capex: $500–$2k · Opex: $500–$2k/yr**

Documents are split into chunks, converted into embeddings (see Glossary), and stored in a vector database hosted on your own infrastructure. Retrieval finds the most semantically relevant chunks for a given query, which are then passed to an LLM as context for synthesis.

**Self-hosting options:**
- **pgvector**: A PostgreSQL extension that adds vector search to an existing database. If you already run Postgres, this is the lowest-overhead path. Supports hybrid search (vector + keyword). Scales well to ~1–2M vectors.
- **ChromaDB**: Purpose-built vector database, trivial to set up. Good for up to ~100M vectors. No external cloud dependency.
- **Qdrant**: High-performance with sophisticated metadata filtering. Well-suited for production workloads with complex retrieval requirements.

**Pros**
- Complete data sovereignty: documents never leave your infrastructure
- No per-query cost beyond fixed compute
- pgvector reuses existing PostgreSQL infrastructure if you already run it
- Right choice for compliance-sensitive environments

**Cons**
- DevOps capacity required to manage, monitor, back up, and scale
- No managed SLAs — outages are your problem
- Chunking strategy and embedding model choices require expertise; poor choices significantly degrade quality
- Performance at very large scale (>10M vectors) requires careful tuning

**Key interactions with other blocks**
- Enables: research chat interface, multi-agent reasoning, report generation with source citation
- Pairs naturally with self-hosted OSS LLM for a fully on-premise stack
- Works with any orchestration option

---

#### Option C — Vector Database + RAG (Managed)
**Complexity: 2/5 · Capex: ~$0 (free tiers) · Opex: $500–$5k/yr**

Same vector search and RAG architecture as Option B, but hosted by a specialized cloud provider who handles infrastructure, scaling, backups, and SLAs.

**Managed options:**
- **Pinecone**: The most mature. Serverless pricing: $0.33/GB storage, $8.25 per 1M read units, $2.00 per 1M write units. Sub-33ms p99 latency in production. No self-hosted option.
- **Weaviate Cloud**: Native hybrid search (BM25 + vectors) at no extra storage cost. Free Sandbox tier. Strong agent-native features added in 2025–2026.
- **Qdrant Cloud**: More cost-effective than Pinecone at scale ($500–$800/month at 100M vectors vs. $5,000+). Excellent metadata filtering. Self-hosted option available for migration.

**On vendor lock-in — an important risk:** Once 100M+ vectors are indexed in Pinecone, migrating to another provider requires re-exporting everything and paying significant egress fees. The mitigation is straightforward and should be implemented from day one: always store the raw source embeddings in cold storage (an S3 bucket or a Postgres table) before indexing them in the managed vector DB. This means you can re-index into any other provider without paying egress or re-calling the embedding API. This one practice eliminates most of the vendor lock-in risk.

**Pros**
- No infrastructure to manage; scales automatically
- Free tiers available for getting started (Pinecone, Weaviate)
- Native LangChain and LlamaIndex integration — weeks to a working prototype
- Managed backups, uptime SLAs, and monitoring included

**Cons**
- Documents and their embeddings stored on third-party infrastructure — compliance review required
- Cost scales with vector count and query volume
- Egress costs make migration expensive without proactive cold storage strategy
- Data sovereignty concerns for a regulated asset manager

**Key interactions with other blocks**
- The fastest path to a working research chat interface or agent prototype
- Best combined with LlamaIndex (designed specifically for this pattern)
- Complement with cold storage of raw embeddings from day one

---

#### Option D — Knowledge Graph
**Complexity: 5/5 · Capex: $5k–$20k · Opex: $3k–$12k/yr**

A database that explicitly models entities (countries, institutions, indicators, policies) and the typed relationships between them. Built on Neo4j or Memgraph (see Glossary).

**On the comparison to Obsidian:** Yes — there is a meaningful conceptual similarity. Both Obsidian (with wiki-links) and a knowledge graph represent entities as nodes and relationships as connections between them. The difference is operational: Obsidian is a human navigation tool — you browse through it, click links, read notes. A knowledge graph is a programmatically queryable database — an agent can traverse it in milliseconds, follow chains of inference, return structured results, and execute queries like "find all macro indicators that historically precede BRL depreciation of more than 10%." Your Obsidian vault, if well-constructed, is a very good manually curated approximation of what a knowledge graph does formally. It is lower cost, lower complexity, and more accessible — with the tradeoff that it requires a programmatic interface layer to be queryable by an agent.

**On building the ontology with an agent:** Partially yes, but with an important limitation. An LLM agent can do significant work in knowledge graph construction: given a Copom minute, it can extract entities mentioned (BCB, SELIC rate, inflation, output gap) and label the relationships between them ("BCB raises SELIC in response to inflation above target"). This is called automated knowledge extraction and is a legitimate use of LLMs. What an agent cannot reliably do is design the ontology — the schema that determines what kinds of entities matter, what relationship types are valid, and how relationships should be weighted or qualified. That requires macro domain expertise: deciding that "monetary transmission channel" should be a first-class entity type, or that the relationship between fiscal dominance and SELIC should behave differently in high-debt-to-GDP regimes, are judgments that require domain understanding. The practical path: domain experts design the ontology; agents populate it from documents.

**On Cypher:** Cypher is the query language for Neo4j and Memgraph, equivalent to SQL for relational databases. A simple example: `MATCH (p:Policy {name: "SELIC"})-[:AFFECTS]->(r:Indicator {name: "USDBRL"}) RETURN p, r` retrieves all stored relationships between the SELIC rate and the USDBRL exchange rate. More complex queries can traverse multiple hops: find all macro indicators that, through a chain of relationships, eventually affect Brazilian equity sector performance.

**On multi-hop reasoning:** "Multi-hop" means following a chain of relationships across multiple steps. Example for "how does fiscal deterioration affect inflation?": the graph traverses — fiscal deterioration → debt sustainability risk → sovereign risk premium rise → BRL depreciation → imported inflation component rises → headline IPCA impact. Each arrow is one hop. Keyword search can only find this chain if a single document explicitly states all five connections together. A knowledge graph traverses the path through explicitly stored relationships, even across documents that were never in the same collection.

**On GraphRAG (how vector DB + knowledge graph work together):** When a question arrives, the system simultaneously executes two searches: (1) a semantic vector search for document chunks that are conceptually close to the query, and (2) a graph traversal for entities and relationships structurally connected to the query topic. Both results are assembled into the LLM's context window before generating the answer. The LLM receives both text evidence ("here is what three research papers say about fiscal dominance and exchange rate dynamics") and structural evidence ("here is the mapped relationship chain showing how fiscal deterioration connects to BRL depreciation in the knowledge graph"). The combination produces materially higher quality answers on complex multi-hop questions than either source alone.

**Pros**
- Unique capability: multi-hop reasoning across explicitly modeled macro relationships
- Enables structural queries: "which sectors have the highest historical sensitivity to BRL depreciation above 10%?"
- Auditable and explainable: every inference path through the graph can be traced — critical for investment decisions
- Can formally encode decades of macro institutional knowledge into a queryable structure
- Highly differentiated: no off-the-shelf solution does this for Brazilian macro

**Cons**
- Requires significant domain expertise to design the ontology correctly
- Maintenance intensive as macro relationships and regimes evolve (new relationships must be added, obsolete ones deprecated)
- Requires Cypher query language expertise in addition to Python
- Building the initial graph requires either extensive manual expert input or LLM-assisted extraction — itself a significant engineering project
- Incompatible with cron-based orchestration (see Glossary for cron): graph updates require transactional pipeline management that only a proper orchestration framework can provide

**Key interactions with other blocks**
- Strongly synergistic with multi-agent frameworks — agents can traverse the graph to find non-obvious connections across domains
- Most powerful when implemented as a complement to vector RAG, not a replacement (GraphRAG pattern described above)
- Requires a workflow orchestrator for reliable updates

---

#### Option E — Hybrid RAG + Knowledge Graph (GraphRAG)
**Complexity: 5/5 · Capex: $10k–$30k · Opex: $8k–$25k/yr**

The combination of a vector database for semantic document retrieval and a knowledge graph for structured relationship reasoning. The LLM agent draws on both simultaneously, as described above under Option D.

**On the four systems involved — and why this is genuinely complex:** This architecture requires coordinating four distinct systems, each with its own tooling, failure modes, and maintenance burden:

1. **Vector database** (stores document embeddings and handles semantic search): requires decisions on embedding model, chunking strategy, index configuration, and re-indexing schedule as new documents are added.
2. **Graph database** (stores macro entity relationships and handles graph traversal): requires ontology design, relationship extraction pipelines, version management as the graph evolves, and Cypher query expertise.
3. **LLM orchestration layer** (the agent that decides when to query the vector DB vs. the graph, how to combine results, and how to synthesize a final answer): requires prompt engineering, tool definitions, reasoning chain design, and evaluation of output quality.
4. **Data ingestion pipeline** (processes new documents through both systems simultaneously — chunking and embedding for the vector DB, entity extraction and relationship updating for the graph): requires Prefect or Dagster, two separate processing pipelines, and coordination logic to keep both systems consistent.

The difficulty is not any one of these systems in isolation. It is coordinating all four into a maintainable, observable whole where a failure in any layer produces a clear error signal rather than a silent degradation in answer quality. This is why the build time estimate is 6–12 months minimum for a production-quality implementation, and why the strong recommendation is to build vector RAG alone in Phase 1, validate it, and add the knowledge graph in Phase 3 only if the analytical requirements justify the complexity.

**Pros**
- Maximum analytical depth: semantic evidence from documents + structural reasoning from the graph
- GraphRAG produces materially higher quality answers on complex multi-document, multi-hop questions
- The platform that most closely realizes the "PhD analyst" vision

**Cons**
- Highest implementation and maintenance complexity of any option in this document
- Very high risk of over-engineering in early phases
- 6–12 months minimum to production-quality implementation
- Strong recommendation: build vector RAG first, add the knowledge graph as Phase 3

**Key interactions with other blocks**
- Requires multi-agent framework and reliable data infrastructure to fully justify the complexity
- The long-term target architecture if the fund commits to AI-driven macro research as a sustained capability

---

### 2.2 LLM & Agent Layer

This is the AI reasoning core: the system that reads retrieved context, interprets data, writes analysis, and executes multi-step research tasks.

#### Option A — Single LLM API
**Complexity: 2/5 · Capex: ~$0 · Opex: $1k–$10k/yr**

**On whether the LLM API is only needed for Q&A, and whether Claude Code requires it:** This is an important distinction. Claude Code is a development environment — it uses Claude's capabilities interactively while you are working, and this cost is covered by your Claude subscription, not by a separate API. When you use Claude Code to read PDFs, synthesize content, and create Obsidian markdown files, no programmatic API integration is required — you are working with Claude directly.

The LLM API is needed when you want processes other than a human developer to call the model: a scheduled pipeline that automatically summarizes new BCB documents overnight, an alert system that classifies news relevance in real time, a chat interface that analysts query from Slack, or an agent that runs autonomously in response to a trigger. The API is the bridge between the deployed, running system and the model. So: Claude Code covers the curation and build work; the API covers the deployed, autonomous system that runs without a human operator present.

Pricing (approximate, 2026): Claude Sonnet 4 ~$3/MTok input, $15/MTok output. Claude Opus 4 higher; GPT-4o in a similar range.

**Pros**
- Operational in minutes: API key, pip install, write a prompt
- State-of-the-art reasoning — these models perform at graduate-level macro analysis
- No infrastructure to manage
- Easy to upgrade as frontier model capabilities improve

**Cons**
- All data sent to external servers — compliance review required for proprietary research content
- Cost scales linearly with token volume
- Cannot be fine-tuned on your specific investment process or research style
- Single vendor dependency and point of failure

**Key interactions with other blocks**
- Compatible with any knowledge base option
- Sufficient for: research chat interface, automated report generation, simple data interpretation
- Not sufficient for: autonomous multi-step research, complex tool use, parallel task execution — those require Option B

---

#### Option B — Multi-Agent Framework
**Complexity: 4/5 · Capex: $2k–$8k (dev time) · Opex: $3k–$15k/yr**

Frameworks that enable LLMs to use tools, maintain memory, plan multi-step tasks, and collaborate as specialized sub-agents.

**The landscape in 2026:**
- **LangChain / LangGraph**: Broadest ecosystem (97k+ GitHub stars). LangGraph went GA October 2025 — supports explicit control over branching, retries, and human-in-the-loop steps. Best for complex, stateful workflows.
- **LlamaIndex**: RAG-first framework, strongest for document-heavy workflows. Best choice when the primary use case is retrieval-augmented analysis over a research knowledge base.
- **CrewAI**: Role-based multi-agent coordination. Define specialized agents (Analyst, Data Researcher, Editor) that collaborate on a research task. Fast to prototype. Less control than LangGraph for complex workflows.
- **Anthropic Claude Agent SDK**: Anthropic's official agentic framework — the same architecture that powers Claude Code. Gained significant production adoption in 2025–2026. Best for Anthropic-native deployments and consistent with using Claude Code for development.

**On debugging and agent reasoning traces:** The instinct to create a structured debugging protocol is correct and important. This is called an agent trace or execution log, and it is a standard component of any production agent system. At each step, the agent should record: what input it received, what tools it called and with what parameters, what those tools returned, what reasoning decision it made based on those results, and what output it produced. This trace is what allows you to understand why an agent produced a wrong answer — not just that it did. LangSmith (the observability layer for LangChain) generates these traces automatically. For a custom implementation, each agent step should write a structured log entry in JSON format covering all the above fields. The trace also serves as the basis for systematic evaluation: you can replay traces on new model versions to detect regressions.

**Pros**
- Enables genuinely autonomous research tasks: "research the impact of fiscal deterioration on USDBRL in the past 10 years and write a memo"
- Agents use tools: web search, data APIs, Python code execution, database queries
- Parallel sub-agents can divide research tasks
- This is the architecture that enables the "PhD analyst" vision

**Cons**
- Debugging multi-step agent failures is significantly harder than debugging a single LLM call — a structured reasoning trace (see above) is essential from day one
- Framework APIs changed rapidly in 2024–2025; stability has improved but breaking changes remain a risk
- Hallucination compounds across reasoning steps — robust human validation is required before trusting agent outputs for investment decisions
- Testing and evaluation frameworks for agents are still immature

**Key interactions with other blocks**
- Requires vector RAG knowledge base — agents need semantic retrieval to function well
- Incompatible with cron orchestration — agent workflows are dynamic and stateful
- Powers: autonomous analyst agent, complex research chat, structured report generation with deep analysis

---

#### Option C — Self-Hosted Open-Source LLM
**Complexity: 5/5 · Capex: $8k–$30k (GPU hardware) · Opex: $8k–$40k/yr**

Running open-source language models (Llama 3, Mistral, Qwen, DeepSeek) on your own GPU infrastructure. A capable research assistant requires a minimum 70B parameter model, needing a multi-GPU server (2–4 A100s or H100s) or a cloud GPU instance.

**Pros**
- Complete data sovereignty: all data, all inference stays on your hardware
- No per-token cost at high volume — fixed compute cost regardless of usage
- Can be fine-tuned on proprietary research to match your investment process
- Immune to API provider pricing changes

**Cons**
- Significant and persistent performance gap vs. frontier APIs on complex analytical tasks — gap narrowed in 2025 but remains material for multi-step reasoning
- Requires ML engineering expertise to serve, scale, monitor, and tune
- GPU infrastructure is capital-intensive
- Not cost-effective at low-to-medium usage volumes

**Key interactions with other blocks**
- Natural complement to self-hosted vector DB — fully on-premise stack
- The performance gap makes this a poor choice for the autonomous analyst agent at current capability levels
- Viable for lower-stakes tasks (document classification, entity extraction) at high volume

---

### 2.3 Orchestration

Orchestration is what runs the pipelines on schedule, handles failures gracefully, monitors data freshness, and coordinates dependencies between ingestion, processing, and delivery. It is unglamorous and often underweighted in architecture discussions — until something breaks silently in production and no one knows.

**On cron (expanded):** A cron job is a scheduled command that fires at a defined time and runs. That is all it does. It has no awareness of whether the command succeeded, cannot retry automatically if it failed, has no built-in mechanism to alert the team when something goes wrong, and cannot express that task B should only run after task A completes successfully. For a simple, single-step, low-frequency job with a low cost of failure, cron is adequate. For anything where reliability matters — data freshness for a dashboard, news ingestion for an alert engine, document processing for a knowledge base — cron's silence on failure is a serious production risk.

#### Option A — Python Scripts + Cron
**Complexity: 1/5 · Capex: ~$0 · Opex: <$500/yr**

**Pros**
- Every developer can read, understand, and modify it immediately
- No tools to learn, no new infrastructure
- Zero licensing cost
- Appropriate for simple, single-step, low-frequency jobs with no downstream dependencies

**Cons**
- No retry logic: failures are silent
- No monitoring or alerting
- Cannot coordinate task dependencies
- Not suitable for stateful, parallel, or multi-step workflows

**Key interactions with other blocks**
- Compatible with: simple periodic free API pulls, basic report generation
- Incompatible with: web scraping, multi-agent workflows, any pattern where a failure has downstream consequences

---

#### Option B — Workflow Orchestrator (Prefect / Dagster / Airflow)
**Complexity: 4/5 · Capex: $2k–$6k (setup and dev time) · Opex: $1k–$4k/yr**

Production-grade pipeline management. Think of Prefect or Dagster as the upgrade from cron that a team inevitably needs: instead of a timer that fires a script and forgets, these tools know whether a pipeline run succeeded, retry it automatically on failure, notify the team if something goes wrong, enforce dependencies between tasks, and provide a dashboard showing the full history of all pipeline runs.

**The 2026 consensus:**
- **Prefect**: The easiest transition from Python scripts. Any Python function decorated with `@task` and `@flow` becomes an orchestrated, monitored, retriable pipeline. Best for teams whose background is analytics rather than engineering. Prefect Cloud starts at ~$100/month; self-hosted is free.
- **Dagster**: Asset-centric model — you define what data assets you produce rather than what tasks to run. The asset model fits a macro data platform well: each macro series (SELIC, IPCA, USDBRL) is a first-class data asset that Dagster tracks. Dagster+ pricing: $100/month (Starter) + pay-per-execution.
- **Apache Airflow**: The industry standard with the largest ecosystem and hiring pool. More complex to configure. Best choice if you already run it or plan to hire standard data engineers.

**Recommended for this context: Prefect or Dagster.** Airflow's operational complexity is harder to justify for a small team building from scratch.

**Pros**
- Retry logic, monitoring, alerting, and run history are built-in
- Dependency management: ensures data is fresh before a report runs
- Operational visibility dashboard across all pipeline runs
- Enables reliable scraping pipelines, multi-source data integration, scheduled AI analysis

**Cons**
- Learning curve: requires understanding their execution models (tasks, flows, assets, schedules)
- Another system to operate and monitor
- Overkill for very simple, single-step, low-failure-risk pipelines
- Managed cloud costs scale with team size and job frequency

**Key interactions with other blocks**
- Required for: web scraping pipelines, hybrid data stacks, any pipeline where failure has downstream consequences
- Note: Prefect/Dagster schedule *when* to run; agent frameworks determine *what* to reason about — these are complementary, not competing

---

#### Option C — Cloud-Native Pipelines
**Complexity: 3/5 · Capex: $1k–$4k · Opex: $500–$3k/yr**

Serverless orchestration using cloud provider-native tools: AWS Step Functions, GCP Workflows, Azure Logic Apps.

**Pros**
- Fully managed: no orchestration infrastructure to run
- Native integration with the same cloud's storage and database services
- Pay-per-execution pricing

**Cons**
- Significant vendor lock-in to the chosen cloud provider
- Limited Python support for complex data transformation
- Requires cloud IAM, VPC, and networking expertise

**Key interactions with other blocks**
- Works well if the entire stack is already on the same cloud provider
- Incompatible with self-hosted LLM and self-hosted vector DB


---

## Building Block 3: Deliverables

Deliverables are what the investment team actually sees and uses. They must be trustworthy, readable, and integrated into the daily workflow. Building sophisticated deliverables on top of an unreliable process layer creates a dangerous illusion of rigor.

---

### 3.1 Automated Reporting

#### Option A — Scheduled Reports & Digests
**Complexity: 2/5 · Capex: ~$500 · Opex: <$500/yr**

LLM-generated macro summaries, data commentary, and research digests delivered on a fixed schedule via email or Slack.

**Typical formats:**
- **Daily macro brief** (Monday–Friday): SELIC expectations, FX, equity performance, key macro releases, overnight news summary
- **Weekly macro digest**: Synthesis of the week's data releases, central bank communications, and notable research
- **Event-driven memos**: Auto-generated within minutes of a Copom decision, GDP release, or IPCA print

**Pros**
- Immediately useful and tangible — easy to demonstrate project value early
- Relatively simple to implement once data and LLM API are connected
- Distributable via email or Slack without any additional interface
- Builds analyst trust in the system incrementally

**Cons**
- Static: no drill-down, no interactivity
- LLM-generated text requires a review process before distribution — especially for anything investment-decision-relevant
- Does not help analysts navigate to the underlying data or reasoning

**Key interactions with other blocks**
- Works with any data option from free APIs upward
- A single LLM API is sufficient — no agent framework needed
- Can be built with cron; Prefect adds monitoring to ensure reports are actually sent

---

#### Option B — Alert & Signal Engine
**Complexity: 3/5 · Capex: $1k–$3k · Opex: $500–$2k/yr**

Automated push notifications when macro variables cross defined thresholds or significant events are detected. Delivered via Slack, email, or WhatsApp (common in Brazilian buy-side).

**Examples of alerts this could generate:**
- SELIC futures repricing by more than 25bps in a single session
- IPCA monthly print deviates from Focus Survey consensus by more than 0.2 p.p.
- BCB intervenes in the FX market (detected via PTAX volume spike + news classifier)
- Brazilian CDS spread crosses a defined historical percentile

**Pros**
- Proactive: the system notifies the team rather than waiting for them to check a dashboard
- High perceived value relative to implementation cost
- Can be rules-based (simple threshold crossing) or AI-enhanced (LLM classifies whether news is materially relevant)
- Integrates into existing communication workflows

**Cons**
- Alert fatigue is a real risk if thresholds are too sensitive
- Requires reliable, timely data feeds — alerts on stale data are actively harmful
- Threshold rules require ongoing calibration as market regimes change
- AI-enhanced alerts need a systematic human validation process

**Key interactions with other blocks**
- Requires automated data feeds — incompatible with manual uploads
- Works independently of the knowledge base for simple rules-based alerts
- AI-enhanced alerts require the LLM API layer

---

### 3.2 Dashboards

#### Option A — Internal Dashboard (Streamlit / Dash)
**Complexity: 2/5 · Capex: $1k–$3k · Opex: $500–$2k/yr**

Python-based interactive web applications that any Python developer can build and maintain.

- **Streamlit**: Any Python script with `st.` calls becomes a web app. Approximately half the code of an equivalent Dash app. The dominant choice for internal analytics tools in 2025–2026. Not multi-process by default; horizontal scaling requires a load balancer.
- **Dash** (Plotly): Built on Flask + React.js + Plotly.js. More control over layout and callback logic. Steeper learning curve. Better for production applications needing fine-grained interactivity.

**Recommended for internal macro dashboards: Streamlit.** Its development speed advantage is decisive for a small team. For board-presentation or client-facing dashboards, Dash or a custom React app is more appropriate.

**Content for a macro dashboard:**
- Macro thermometer: visual summary of key variables vs. historical distributions (SELIC, IPCA, USDBRL, IBOV, primary balance)
- Economic surprise index: recent prints vs. Focus Survey consensus
- Central bank communication tracker: sentiment and key phrase frequency across BCB/Fed/ECB
- Model outputs: GDP nowcast, inflation forecast, FX fair value estimate

**Pros**
- Fast to build: a working Streamlit macro dashboard can be done in days
- Full Python data stack: pandas, plotly, statsmodels all work natively
- Easily iterable — adding a new panel does not require a redesign
- Inexpensive to host

**Cons**
- Not board-presentation quality without significant additional design work
- Performance issues with complex or large data (full-script rerun model)
- Limited enterprise auth and access control without additional configuration

**Key interactions with other blocks**
- Works with free APIs and hybrid data stack; not suitable with manual-upload-only data
- A single LLM API can power natural language summary panels within the dashboard

---

#### Option B — Live Production Dashboard (React / Tableau / Power BI)
**Complexity: 4/5 · Capex: $5k–$20k · Opex: $3k–$15k/yr**

Enterprise-grade dashboards suitable for board presentations, client reporting, and real-time monitoring.

- **Custom React + Recharts/D3**: Maximum control, highest quality output, but requires a dedicated frontend developer. Build time 3–6 months.
- **Tableau**: Drag-and-drop dashboard builder. $15–35/user/month. Does not natively support Python models; data must be pre-processed externally.
- **Power BI**: Microsoft ecosystem. $10–20/user/month. Better Excel/Office integration.
- **Apache Superset**: Open-source BI tool. Free to self-host. Less polished than Tableau/Power BI.

**Pros**
- Board-presentation quality: professional design, smooth interactivity, full branding control
- Enterprise auth (SSO, LDAP), user permissioning, and audit logging standard
- Real-time data streaming support

**Cons**
- Significantly more expensive and longer to build than Streamlit
- Custom React requires frontend engineering skills that may not exist in a quant/data team
- Often over-engineered for purely internal analytical use

**Key interactions with other blocks**
- Premium or hybrid data stack required to justify real-time capability
- Prefect/Dagster should feed a data warehouse that the dashboard reads from
- Right target for client-facing or board deliverables; Streamlit for internal iteration

---

### 3.3 AI Interface

#### Option A — Research Chat Interface (RAG Q&A)
**Complexity: 3/5 · Capex: $2k–$6k · Opex: $2k–$8k/yr**

A conversational interface where analysts ask questions in natural language and receive cited answers drawn from the knowledge base.

**Example queries:**
- "What does the historical analysis say about the relationship between SELIC cuts and USDBRL appreciation?"
- "Summarize the last three Copom meeting minutes and identify any shift in language about the neutral rate"
- "What does [author]'s research on the fiscal multiplier in Brazil conclude?"

**Pros**
- High user satisfaction — analysts perceive this as a genuine research upgrade
- Democratizes access to the full document library across the team
- Answers cited to specific source documents, enabling verification
- Deployable as a Slack bot — zero friction to adopt

**Cons**
- Quality entirely determined by knowledge base completeness
- Hallucination risk when the knowledge base lacks a relevant document
- Users require calibration time to understand the system's coverage boundaries
- Retrieval and synthesis only — cannot take actions

**Key interactions with other blocks**
- Requires vector RAG knowledge base — incompatible with keyword-only search
- Works with a single LLM API; does not require an agent framework
- The richer the document collection, the better the chat quality

---

#### Option B — Autonomous Analyst Agent
**Complexity: 5/5 · Capex: $10k–$40k · Opex: $8k–$30k/yr**

A multi-step AI agent that executes research tasks autonomously: fetching live data, querying the knowledge base, running statistical analysis via Python code execution, synthesizing findings, and producing structured deliverables.

**Example tasks:**
- "Analyze the 5-year relationship between Brazilian primary balance deterioration and USDBRL. Fit a regression, identify outliers, and write a one-page memo with implications for the next 6 months."
- "Review the last 12 months of BCB communications and identify any semantic shift in forward guidance language. Compare with what consensus expects."
- "Build a scenario analysis assuming SELIC stays flat, cuts 150bps, or raises 100bps. Estimate the P&L impact on each equity sector."

**Pros**
- The closest realization of the "PhD analyst" vision
- Combines retrieval + data + code execution + synthesis in a single workflow
- Dramatically multiplies analyst capacity for data-intensive research tasks
- Creates genuine competitive advantage if implemented well

**Cons**
- Extremely complex to build, test, and trust in a production investment context
- Requires robust human-in-the-loop oversight — autonomous agents can produce confidently wrong analysis
- LLM API costs for long reasoning runs are significant ($5–20 per extended run)
- Evaluation is genuinely hard: systematic back-testing and validation processes are required
- Build time: 6–12 months to production-ready quality

**Key interactions with other blocks**
- Requires: multi-agent framework, vector RAG knowledge base, reliable data APIs, orchestration framework
- Premium market data dramatically improves agent analysis quality
- This is a Phase 3 deliverable — attempting it in Phase 1 is the most common failure mode in projects like this

---

## Cross-Cutting Interaction Rules

**Rule 1 — Data is the hardest constraint**
The data choice limits everything downstream. Manual uploads block live dashboards and alerts permanently. Free public APIs support most Phase 1 deliverables. No amount of AI sophistication compensates for stale or incomplete data.

**Rule 2 — The knowledge base choice is the hardest to reverse**
Once documents are chunked and embedded in a vector DB, migration requires re-processing everything. Make this decision with multi-year scalability in mind. Mitigate vendor lock-in by storing raw embeddings in cold storage from day one.

**Rule 3 — Cron and agents cannot coexist**
Agent workflows are dynamic, stateful, and failure-prone in unpredictable ways. If agents are in the roadmap, a proper orchestrator (Prefect, Dagster) is required from the start. Retrofitting orchestration onto a cron-based system is painful.

**Rule 4 — The autonomous agent is a Phase 3 deliverable**
It requires working vector RAG + working data pipelines + working orchestration + working LLM integration. None can be skipped. The research chat interface is the right Phase 2 target — structurally similar to the agent, significantly simpler to validate and trust.

**Rule 5 — Cost compounds across the stack**
Premium data + managed vector DB + frontier LLM API + live dashboard can reach $150k+/year if all premium options are chosen simultaneously. The free and low-cost options are genuinely good — use them in Phase 1 and add premium spend only where a specific gap justifies it.

**Rule 6 — Web scraping requires a production orchestrator**
RSS feeds and custom scrapers fail silently if run via cron. If web scraping is part of the news strategy, Prefect or Dagster is a hard requirement.

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

## Proposed Phased Approach

### Phase 1 — Prove the Concept (0–4 months, ~$5k–$15k/year total)
**Goal:** A working system the team uses daily, demonstrably improving research quality.

- Text: PDF + Markdown ingestion (automated for scheduled sources; manual curation for others)
- Data: Existing hybrid stack (MySQL + Bloomberg + free APIs) — no change required
- News: Web search APIs + BCB/central bank RSS feeds
- Knowledge Base: Managed vector DB (Weaviate Cloud or Qdrant free tier)
- LLM: Single LLM API (Claude Sonnet 4) — Claude Code for development and curation
- Orchestration: Prefect (open source, self-hosted)
- Deliverables: Weekly automated macro digest + Internal Streamlit dashboard + Research chat interface via Slack

This stack can be built by 1–2 engineers in 8–12 weeks and delivers three real deliverables the team can evaluate immediately.

### Phase 2 — Automate and Expand (4–12 months, ~$15k–$40k/year total)
**Goal:** Operational reliability, expanded news coverage, and alert capability.

- News: Add News APIs + BCB/central bank scraping pipeline with Prefect monitoring
- Knowledge Base: Expand document collection; evaluate self-hosted vector DB for data sovereignty; add BM25 search layer as fallback to semantic retrieval
- LLM: Begin evaluating multi-agent framework (LlamaIndex or Claude Agent SDK) for report automation
- Deliverables: Add alert engine on macro thresholds + Upgrade dashboard toward Dash or semi-custom React for board-facing views

### Phase 3 — The PhD Analyst (12–24 months, ~$40k–$100k/year total)
**Goal:** Autonomous research capability that redefines the team's analytical capacity.

- Knowledge Base: Evaluate knowledge graph layer for macro relationship modeling — domain experts design the ontology, agents assist with population
- LLM: Deploy multi-agent framework with code execution, data analysis tools, and structured reasoning traces
- Deliverables: Autonomous analyst agent for on-demand quantitative research tasks + Live production dashboard for fund monitoring

---

## Design Discussion: Obsidian-Based Knowledge Architecture with Specialist Agents

*This section documents an alternative architecture discussed with the team. It emerged from a key observation: for a scoped, expert-curated knowledge base in a specialized domain, human-curated conceptual relationships may be more reliable than machine-extracted vector similarity.*

---

### The Core Design

The proposed architecture has three layers:

**Layer 1 — Knowledge Curation (Obsidian Vault)**

The vault is organized by domain, with a two-tier structure within each:

```
obsidian/
├── monetary_policy/
│   ├── synthesis/          ← one .md file per source document
│   │   ├── bernanke_2015_monetary_transmission.md
│   │   ├── copom_minutes_march_2026.md
│   │   └── ...
│   └── concepts/           ← one .md file per analytical concept
│       ├── inflation_targeting.md
│       ├── monetary_transmission_channels.md
│       ├── fiscal_dominance.md
│       └── ...
├── fiscal_policy/
│   ├── synthesis/
│   └── concepts/
└── exchange_rate/
    ├── synthesis/
    └── concepts/
```

The synthesis files capture the main argument, key evidence, and analytical contribution of each source. The concept files define what each concept means, how it relates to other concepts (via wiki-links), and what the literature says about it. The wiki-link graph between concept files is a manually curated knowledge graph built in markdown — lower complexity than Neo4j, higher reliability than machine extraction.

This structure is built and maintained using Claude Code: the analyst uploads source PDFs, Claude Code extracts the main topics and content, synthesizes each into a structured markdown file, and creates or updates the relevant concept files. This work happens interactively, not via an API pipeline.

**Layer 2 — Agent Layer (Domain Specialists + Orchestrator)**

Each domain has a specialist agent defined by:
- A system prompt encoding the analytical framework for that domain (e.g., the monetary policy agent is instructed to reason in terms of monetary transmission channels, inflation expectations, and central bank credibility)
- A set of file-system tools it can call: `read_file(path)`, `list_files(directory)`, `follow_wikilink(file, link_text)`, `search_vault(query, folder=None)`
- A defined home directory in the Obsidian vault (the monetary policy agent reads from `obsidian/monetary_policy/`)

An orchestrator agent sits above the domain specialists. Its role is to receive an analytical question, determine which domain specialists are relevant, delegate sub-tasks to them, interpret their outputs, decide whether cross-domain consultation is needed, and consolidate the final response.

**Layer 3 — Navigation (Link Traversal + BM25 Search)**

The agent navigates the knowledge base through two mechanisms:

*Primary: wiki-link traversal.* The agent follows `[[concept_name]]` references as explicit relationships. When reading the `fiscal_dominance.md` concept file, it finds links to `[[debt_monetization]]`, `[[inflation_expectations]]`, and `[[monetary_policy_constraints]]` — and can follow each to deepen its understanding.

*Secondary: BM25 full-text search.* When the agent wants to check whether relevant content exists beyond what the explicit links surface — or when no clear link path connects the query to a concept — it calls `search_vault(query, folder)` to find files containing relevant terminology. This closes the gap where curated links are not exhaustive.

---

### An Example Interaction: Fiscal Dominance and Monetary Policy

*Query to the orchestrator:* "How should we interpret last week's Copom decision in the context of fiscal dominance concerns?"

**Step 1 — Orchestrator delegates to monetary policy agent**
The monetary policy agent reads `copom_minutes_march_2026.md` (synthesis file) and follows wiki-links to `fiscal_dominance.md` in the concepts folder. It reads the concept definition and finds a wiki-link flagged as an external domain reference: `[[fiscal_policy/concepts/debt_sustainability_trajectory]]`.

**Step 2 — Monetary policy agent returns structured output**
The agent returns its analysis plus a structured field: `cross_domain_references: ["fiscal_policy/concepts/debt_sustainability_trajectory", "fiscal_policy/concepts/primary_balance_dynamics"]`. This is an explicit signal, not an implicit one — the agent is designed to surface these references in a structured output field.

**Step 3 — Orchestrator detects cross-domain signal and delegates**
The orchestrator reads the structured output, identifies the fiscal policy references, and delegates a sub-task to the fiscal policy agent: "provide analysis of current debt sustainability trajectory and primary balance dynamics as context for the Copom decision interpretation."

**Step 4 — Fiscal policy agent responds**
The fiscal policy agent reads the referenced concept files, follows relevant links within its domain (connecting to `nominal_deficit_trajectory.md`, `bcb_debt_holdings.md`), and returns a structured fiscal assessment.

**Step 5 — Orchestrator consolidates**
The orchestrator receives both analyses and synthesizes a final response: the monetary policy read of the Copom decision, informed by the fiscal policy context, with explicit citations to the specific synthesis and concept files that grounded each claim.

---

### How This Compares to Vector RAG

| Dimension | Obsidian + Specialist Agents | Vector RAG (Managed) |
|---|---|---|
| Knowledge structure | Human-curated, explicit relationships | Machine-indexed, implicit similarity |
| Retrieval mechanism | Link traversal + BM25 fallback | Embedding similarity search |
| Coverage | Bounded to curated vault | Scales to any document volume |
| Relationship quality | High (expert-validated) | Variable (depends on embedding quality) |
| Maintenance burden | Curation discipline as vault grows | Re-indexing as documents are added |
| Setup complexity | Low (file system + tools) | Medium (vector DB, embedding pipeline) |
| Annual cost | Near-zero (only LLM API calls) | $500–$5k (managed vector DB) |
| Semantic fallback | BM25 (keyword-based) | Embedding similarity (semantic) |
| Best suited for | Scoped, expert-curated, specialist domain | Large, growing, heterogeneous document sets |

The key trade-off: vector RAG finds conceptually similar content even without explicit connections, and scales to any document volume. The Obsidian architecture finds only what the curated links connect — but the connections are validated, the concept structure is explicit, and the cost is dramatically lower. For a knowledge base that is intentionally scoped (the macro domains relevant to the fund) and carefully maintained, the Obsidian architecture likely produces higher-quality reasoning at lower cost and complexity. For a knowledge base that needs to grow autonomously by ingesting new documents without human review, vector RAG scales better.

These approaches are also not mutually exclusive. The Obsidian vault can serve as the primary reasoning layer (deep, curated, expert-validated), with a vector DB as a supplementary wide-net retrieval layer for less-curated sources. The orchestrator could route queries to the appropriate layer based on whether the question requires deep conceptual reasoning (Obsidian agents) or broad document discovery (vector RAG).

---

### Technical Implementation Notes

**The agents are more than just prompts.** An agent in this architecture requires three components: (1) a system prompt defining the analytical role and framework, (2) callable tool functions the LLM can invoke during its reasoning, and (3) a defined context boundary (the home folder). Without the tool functions — particularly `read_file()`, `follow_wikilink()`, and `search_vault()` — the agent cannot navigate the vault. It can only reason about what you put directly in the prompt. The traversal pattern only works because the agent can call these functions during its reasoning process.

**The Obsidian vault is just a folder of markdown files.** The agents never interact with the Obsidian application. The vault is accessed via standard file system operations. Wiki-links (`[[concept_name]]`) are resolved by a simple string parsing function that maps the link text to a file path. This means there is no Obsidian API dependency, no external application requirement, and no platform risk.

**The BM25 search layer** requires approximately 30 lines of Python using the `rank_bm25` library. At startup, an index is built over all markdown files in the vault. At query time, the agent passes a query string and receives ranked file paths. The index should be rebuilt whenever new files are added to the vault (this can be triggered automatically by a Prefect job that monitors for file system changes). At the scale of hundreds to a few thousand documents, BM25 performs in milliseconds.

**The orchestrator's cross-domain detection should be explicit.** Domain agents should be designed to return a structured output that includes a `cross_domain_references` field — a list of vault paths that fall outside their home domain but that they encountered during traversal. This is more reliable than having the orchestrator infer cross-domain needs from the content of the agent's natural language response. The orchestrator reads the structured field and routes accordingly, rather than relying on its own LLM judgment about whether to consult another domain.

**Recommended concept index:** A JSON file at the vault root mapping key concepts to their domain and primary file path. Example:

```json
{
  "fiscal_dominance": {
    "domain": "monetary_policy",
    "primary_file": "monetary_policy/concepts/fiscal_dominance.md",
    "related_domains": ["fiscal_policy"]
  },
  "debt_sustainability": {
    "domain": "fiscal_policy",
    "primary_file": "fiscal_policy/concepts/debt_sustainability.md",
    "related_domains": ["monetary_policy", "exchange_rate"]
  }
}
```

This index gives the orchestrator a fast lookup before delegating, rather than relying entirely on agent traversal to surface cross-domain connections. It also serves as a living map of the vault's conceptual structure — useful for onboarding new team members and for identifying coverage gaps.

---

### Strengths of This Architecture

- **Low cost and low infrastructure complexity.** The vault is a folder, the agents are Python functions, the search layer is one library. There is no vector database to manage, no embedding pipeline to maintain, no managed cloud service to depend on.
- **High knowledge quality.** Human-curated links and concept definitions are more reliable than machine-extracted relationships for a specialized domain. The analyst's judgment about what connects to what is encoded directly in the structure.
- **Interpretable reasoning.** Every agent action — which file it read, which link it followed, what search it ran — can be logged in a structured trace. This makes debugging and validation tractable.
- **Natural workflow integration.** Analysts already work with research documents. The curation workflow (Claude Code reads a paper, writes a synthesis and updates concept files) is a modest extension of existing research practice, not a new parallel system.
- **The wiki-link graph is a knowledge graph lite.** For the purposes of this project — reasoning about macro concepts and their relationships — a well-maintained Obsidian vault with disciplined linking captures most of what a formal knowledge graph provides at a fraction of the cost and complexity.

---

### Risks and Mitigations

**Risk 1 — Coverage dependency on curation quality.** The system finds only what the links connect. A concept that exists in the vault but has no link path from the query entry point will not be found by traversal. *Mitigation:* the BM25 search layer closes most of this gap; a regular vault audit process (checking for orphaned notes — files with no incoming or outgoing links) catches gaps systematically.

**Risk 2 — Curation discipline as the vault grows.** At 20 source files and 40 concept files, curation is manageable. At 200+ sources, maintaining linking discipline becomes the primary operational burden. *Mitigation:* Claude Code can assist with the curation process, flagging potential missing links and suggesting concept file updates when new sources are ingested. The two-tier structure (synthesis separate from concepts) also limits the maintenance surface — concept files need updating less frequently than synthesis files.

**Risk 3 — Scale ceiling.** At very high document volumes, link traversal alone cannot guarantee comprehensive coverage. *Mitigation:* at the scale where this becomes a problem (likely 300+ sources), a hybrid approach makes sense — the Obsidian vault handles the curated expert knowledge layer, and a vector DB handles the broader, less-curated document discovery layer. These layers are not competing: they answer different types of questions.

**Risk 4 — Orchestrator routing logic.** The orchestrator needs to know when to consult additional domains. If this logic is implicit (the orchestrator judges from content alone), it is less reliable. *Mitigation:* explicit structured output from domain agents (the `cross_domain_references` field), a concept index for fast pre-delegation lookup, and clear escalation logic in the orchestrator's system prompt.

---

*Document prepared for internal discussion. All cost estimates are indicative based on publicly available pricing as of mid-2026. Actual costs depend on usage volume, contract terms, and infrastructure choices.*
