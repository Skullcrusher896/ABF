---
name: aba-lookup
description: Fast, token-cheap navigation of the ABA repo and base Ante Bellum — find where a mission, event, effect, trigger, modifier, reform, decision or loc key is defined and used, and outline large script files before reading them. Use before opening any large .txt/.yml file, whenever you need to check if something exists in ABA or AB, or to see how AB implements something.
---

# ABA lookup

Big files (TLW_Punic.txt is 13k lines) burn context. Locate first, then read only the range you need.

Scripts live in `.claude/skills/aba-lookup/scripts/`. Base AB is found via `AB_PATH` (see CLAUDE.md). Run with `python -I`.

## Find a definition (ABA and AB side by side)

```
python -I .claude/skills/aba-lookup/scripts/find.py KEY [KEY ...] [--in aba|ab|both] [--usages] [--max-lines N]
```

- Matches `KEY = {` blocks, events by `id = KEY`, and loc `KEY: "..."`; prints the block with `file:start-end`, tagged `[ABA]` or `[AB]`.
- An `[ABA]` and `[AB]` hit at the same path = ABA overrides AB.
- `--usages` lists where the key is referenced (capped at 30).
- Several keys per call is cheaper than several calls.
- Blocks over `--max-lines` (default 80) are cut, with the offset to Read for the rest.

## Outline a file

```
python -I .claude/skills/aba-lookup/scripts/outline.py FILE [--depth 2] [--grep TEXT]
```

Top-level blocks with line ranges, the `#` comment above each, event ids, mission slot/position. `--depth 2` lists missions inside groups and options inside events. `--grep` filters.

## Looking at AB for reference

To copy AB's approach (design, wording, reward size), find a comparable AB mission/event with `find.py --in ab`, or Grep `$AB_PATH/missions` / `$AB_PATH/localisation` with `head_limit`. Don't read whole AB files.

## When not to use

A single known key in a small file → Grep or Read directly.
