---
name: vault
description: Synthesize the clean_md files of the vault that have no synthesis note yet (sweep, read each in full, write obsidian/<topic>/synthesis/<name>.md, patch or create the concept pages in obsidian/concepts/, check with vault.py, update the tracker). Run as /vault [topic] [file ...].
argument-hint: "[topic] [file name ...]"
context: fork
agent: vault
disable-model-invocation: true
---

Synthesize into the vault. Arguments: $ARGUMENTS

Follow your instructions (`.claude/agents/vault.md`) step by step: sweep with
`vault.py --list`, then one pending file at a time (at most 5), and end with the report table
and the proposed map additions they specify. No topic means every topic.
