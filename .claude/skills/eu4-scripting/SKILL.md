---
name: eu4-scripting
description: EU4 Clausewitz scripting for ABA (Ante Bellum: Actum, merged ABF + TLW submod of Ante Bellum) — events, missions, decisions, modifiers, scripted effects/triggers, government reforms, on_actions, custom GUI. Use whenever writing, editing, debugging or reviewing any .txt game script in this repo, or checking compatibility with base Ante Bellum.
---

# EU4 scripting for ABA

Code style reference = **suoncha's TLW code** (`TLW_*` files). Match it in new code and in code you edit. Don't mass-restyle existing ABF code unless asked.

## Before writing

1. Find precedent with `aba-lookup` (`find.py` / `outline.py`): a similar TLW construct first, then AB's.
2. Verify every tag, culture, religion, modifier, scripted effect/trigger and event id you reference exists (`find.py KEY`). Never invent keys.
3. Same path + filename as an AB file = full override. Prefer new prefixed files; if overriding, say so.

## Code style (from TLW)

**Naming**
- Files: `TLW_<Topic>.txt` / `ABF_<Topic>.txt` by workstream.
- Event namespace lowercase `tlw_<topic>` (ABF: `abf_<topic>_event`), ids from `.0`. When extending an AB chain, keep AB's namespace (`ab_punic`, `ab_byzantium`).
- Scripted effects `TLW_<snake_name>_effect`; triggers `<snake_name>_trigger` (or `tlw_..._trigger`).
- Flags/variables snake_case with topic prefix (`pun_...`, `rom_...`, `TLW_NCI_preview` for system flags).
- Mission groups `tlw_<theme>_<n>`; missions `<tag>_<snake_name>`.

**Structure**
- `on_actions`: thin hooks that only call a scripted effect, e.g. `on_monthly_pulse = { TLW_on_monthly_pulse = yes }`. Logic lives in `common/scripted_effects/TLW_on_actions.txt`. This keeps ABA patchable and merge-friendly.
- Reusable logic → scripted effects/triggers, not copy-paste across missions/events.
- Triggers shown to players are wrapped: `custom_trigger_tooltip = { tooltip = KEY ... }`.
- Rewards: visible `custom_tooltip = KEY` + real code in `hidden_effect = { }`; `custom_tooltip = AB_EMPTY` as spacer between reward blocks.
- Branching: `if = { limit = { } }` / `else_if` / `else` chains, not separate mutually-exclusive ifs.
- Cross-country references via saved event targets (`save_global_event_target_as`, `event_target:name = { }`) and variables (`set_variable`/`change_variable`/`export_to_variable` with `which`/`value`).
- Prefer AB helper effects when they exist: `add_mercantilism_or_monarch_power = { amount = N }`, `add_army_tradition_or_mil_power = { amount = N }`, etc. (look them up).
- `hidden = yes` for technical events; `ai_chance = { factor = N }` on options when choices aren't equal.

**Formatting**
- Tabs. One statement per line. Single condition may be inline: `NOT = { has_country_flag = x }`; multiple conditions → multi-line block.
- Mission key order: `icon`, `required_missions = { a b }` (always present, `{ }` if empty, inline), `position`, `provinces_to_highlight`, `trigger`, `effect`.
- Event header order: `id`, `title`, `desc`, `picture`, blank line, `hidden`/`is_triggered_only`, then `trigger`, `immediate`, options.
- `# Comment` above every event/major block naming it; `### Section` comments inside long effects.

Illustrative shape (real examples: `events/TLW_Rome.txt`, `missions/TLW_Punic_CTG.txt`, `common/on_actions/TLW_on_actions.txt`):

```
# Restoration of Rome
country_event = {
	id = tlw_rome.1
	title = tlw_rome.1.t
	desc = tlw_rome.1.d
	picture = CULTURE_eventPicture

	is_triggered_only = yes

	option = {
		name = tlw_rome.1.a
		ai_chance = { factor = 100 }
		custom_tooltip = TLW_ROME_RESTORATION_TT
		hidden_effect = {
			TLW_switch_to_hellenic_empire_effect = yes
		}
	}
}
```

## Correctness checklist

- Scopes: province effects in province scope, country in country scope; `ROOT`/`FROM`/`PREV`/`THIS` resolve as intended inside nested scopes and event targets.
- Missions: `provinces_to_highlight` mirrors `trigger`; `required_missions` exist; no slot/position collisions; `potential` cheap.
- Events: `is_triggered_only = yes` unless MTTH is truly needed.
- Every modifier name used is defined in `common/event_modifiers/` (ABA or AB); every loc key exists (`check_mod.py --stub` prints missing ones).
- Tooltips state the real effect after any reward change.

## Performance

- No `every_province`/`any_province` with heavy limits on pulses; narrow to region/area/owned scopes.
- Cheapest, most-likely-false condition first.
- Prefer on_action/mission-triggered events over MTTH and pulses; cache results in flags/variables.

## Validate (once, at the end)

```
python -I .claude/skills/eu4-scripting/scripts/check_mod.py --paths <changed files...>
```

Brace balance, loc BOM/header, missing event/mission loc keys (searches ABA + AB via `AB_PATH`). `--stub` prints missing keys as ready-to-paste lines. Remind the user to check `error.log` in game.
