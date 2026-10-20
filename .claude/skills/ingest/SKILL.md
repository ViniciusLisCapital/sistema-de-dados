---
name: ingest
description: Ingest the PDFs saved in repository/<topic>/raw_pdf/ that have not been extracted yet (sweep, extract, check against the pages, write raw_md and the vault's clean_md, update the literature tracker). Run as /ingest [topic] [file ...] [--overwrite].
argument-hint: "[topic] [file name ...] [--overwrite]"
context: fork
agent: ingestion
disable-model-invocation: true
---

Ingest into the knowledge base. Arguments: $ARGUMENTS

Follow your instructions (`.claude/agents/ingestion.md`) step by step: sweep with
`run.py --list`, then one pending file at a time, and end with the report table they specify.
No topic means every topic.
