# Macro Research Platform — Project Context

## What we are building
An in-house AI-driven macro research platform for an equity asset manager with growing macro exposure. The goal is a "PhD analyst" system that synthesizes research literature, monitors data, and produces analysis on demand.

## Framework: three building blocks
**Raw Materials → Process → Deliverables**

Evaluated across four criteria: implementation/maintenance complexity (1–5), financial cost (capex + opex), pros/cons, and cross-block interactions.

**Key distinction:** Text (PDFs, research) is foundational knowledge — the lens. News is the real-time signal interpreted through that lens. These serve different roles in the architecture.

## Existing team setup (already decided)
- **Quantitative data:** MySQL + Bloomberg + free APIs (BCB, IBGE, FRED, IPEA). No change needed in Phase 1.
- **Development environment:** Claude Code for curation and build work. API for the deployed, autonomous system.

## Architecture under evaluation: Obsidian vault + specialist agents
The team developed an alternative to managed vector RAG:

**Vault structure:**
```
obsidian/<domain>/synthesis/   ← one .md per source (Claude Code generates these)
obsidian/<domain>/concepts/    ← one .md per concept, with [[wiki-links]]
```

**Agent layer:** Domain-specialist agents (monetary policy, fiscal policy, FX) with file-system tools (`read_file`, `follow_wikilink`, `search_vault`). An orchestrator above them detects cross-domain signals via structured output fields and delegates accordingly.

**Navigation:** Primary = wiki-link traversal. Fallback = BM25 full-text search (rank_bm25 library, ~30 lines of Python, index rebuilt when vault changes).

**Key insight:** Agents are not just prompts — they require callable tool functions to navigate the vault. The Obsidian vault is just a folder of markdown files; no Obsidian application dependency.

**Vs. managed vector DB:** Obsidian gives higher knowledge quality (expert-curated links) at near-zero infrastructure cost, bounded to the curated vault. Vector RAG scales to any volume but retrieval quality is variable. Not mutually exclusive.

## Phased approach
- **Phase 1 (0–4 mo, ~$5–15k/yr):** PDF + Markdown ingestion · Managed vector DB (Weaviate/Qdrant free tier) OR Obsidian vault · Claude Sonnet API · Prefect · Streamlit dashboard · Research chat (Slack) · Weekly automated digest
- **Phase 2 (4–12 mo, ~$15–40k/yr):** News APIs + BCB/CB scraping · Alert engine · Agent framework evaluation · Dashboard upgrade
- **Phase 3 (12–24 mo, ~$40–100k/yr):** Multi-agent framework · Knowledge graph (optional) · Autonomous analyst agent · Live production dashboard

## Open decision (needed week 1)
**Knowledge base architecture:** managed vector DB (faster to build, third-party infra) vs. Obsidian curated vault (lower cost, higher quality for scoped domain, requires curation discipline).

## Artifacts produced
- `macro-platform-architecture-research-v2.md` — full research document with all options, costs, pros/cons, interactions, glossary, and Obsidian architecture discussion
- `macro-board-presentation.pptx` — 21-slide board deck (11 main + 9 appendix) with hyperlinks between main slides and appendix detail slides
