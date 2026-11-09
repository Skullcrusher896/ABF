# ABA — Ante Bellum: Actum

EU4 1.37 submod of **Ante Bellum (AB)**. Merges two AB submods: **ABF** (Ante Bellum Flavor, `ABF_*` files) and **TLW** (The Lost World, `TLW_*` files). The repo, README and `descriptor.mod` still say ABF — that's legacy naming, not a separate project. `AB_*` files here override/extend base AB files of the same path.

## Team & workstreams

- **TLW** (`TLW_*`): suoncha (HOANGVU) — lead coder; their code is the style reference.
- **ABF** (`ABF_*`): teammate.
- Keep new files in the owner's prefix. Touching the other workstream's files is fine, but say so.

## Base AB location (per user)

Scripts and lookups need the base AB folder. Each person sets it in their own **`.claude/settings.local.json`** (gitignored):

```json
{ "env": { "AB_PATH": "D:/path/to/ab" } }
```

Fallback: a sibling `../ab` folder. In shell commands use `$AB_PATH`. Never hard-code a personal path in committed files.

## Style sources — two different references

- **Code** (structure, naming, formatting) → match suoncha's TLW code. See the `eu4-scripting` skill.
- **Content design, lore, writing** → match **base AB**, for consistency with the parent mod. See `aba-content-design`, `ab-lore-research`, `aba-writing`.

## Skills

| Skill | Use for |
|---|---|
| `aba-lookup` | Find definitions/usages in ABA + AB, outline big files. **Use before reading any large file.** |
| `eu4-scripting` | Writing/reviewing any game script; `check_mod.py` validator |
| `eu4-localisation` | Any `.yml` text |
| `ab-lore-research` | Lore briefs before new content |
| `aba-content-design` | Mission trees, events, mechanics, reward balance |
| `aba-writing` | Player-facing prose, changelogs |

## Working rules (speed & tokens, without cutting quality)

- **Answer first.** Lead with the answer or the change; no preamble, no restating the question, no closing recap of what the diff already shows.
- **Don't read whole files.** Many are 3k–13k lines. Use `outline.py` / `find.py` (aba-lookup) or Grep, then Read only the line range you need.
- **Look up, don't guess.** Verify tags, cultures, modifiers, effects and loc keys exist (ABA or AB) with `find.py` instead of reasoning from memory.
- **Edit, don't rewrite.** Use targeted Edits; never reformat or restyle code you weren't asked to touch.
- **Batch independent tool calls** in one message. Use subagents only for broad multi-area research.
- **Validate once at the end** with `check_mod.py --paths <changed files>` — not after every edit.
- Ask a question only when the answer changes what you'd build; otherwise pick the AB-consistent default and state it in one line.
- Known pre-existing brace errors (don't attribute to new edits): `common/scripted_effects/wallachian_terror_scripted_effects.txt`, `events/wallachia/AB_wallachia_events.txt`, `missions/ABMP_WAL.txt`.

## README.md = Steam Workshop description

`README.md` is published as the mod's workshop page (Steam BBCode). Player-facing only: ABA presented as one mod with one unified feature list. No dev setup, commands, style rules or team info there — that belongs in this file.

## Files & encoding

- Helper scripts need Python 3 (`python -I <script>`).

- Script `.txt`: tabs, UTF-8 (BOM tolerated). Localisation `.yml`: **UTF-8 with BOM**, `l_english:` header, space-indented keys.
- In-game test: `Documents/Paradox Interactive/Europa Universalis IV/logs/error.log`.
- A Chinese translation mod is a dependency; list new English loc keys in your reply so translators can follow.
