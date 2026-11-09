---
name: aba-content-design
description: Gameplay/content design for ABA, calibrated to base Ante Bellum — mission trees, event chains, decisions, government mechanics, reforms, estate privileges, spawnable cultures, great projects, reward balance and AI behaviour. Use when planning new content, reworking or balancing a mission tree, or choosing rewards and mechanics, before code is written.
---

# Content design for ABA

Design consistency target = **base AB**. A player moving between AB and ABA content shouldn't feel a change in scale, pacing or style. When unsure, find the closest comparable AB tree (`find.py --in ab`, Grep `$AB_PATH/missions`) and match it.

## Workflow

1. Lore brief (`ab-lore-research`).
2. Design doc (template below) → user sign-off.
3. Implement (`eu4-scripting`, `eu4-localisation`), write text (`aba-writing`).

## Mission trees (AB shape)

- 5 slots, used about evenly in AB. Each column a theme; cross-column requirements tell the story.
- Early rows doable in the first decades; capstones are the nation's climax.
- Triggers readable from the card: provinces/areas, development, reforms, buildings, diplomacy. Avoid RNG/hidden requirements.
- Provide alternatives where a requirement can become impossible (tag formed, province lost, building upgraded).
- AB patterns worth reusing: timed missions that are removed on failure (`ab_cornwall`), branching paths with a switch (TLW mission switch), preview events for tree choice.

## Reward calibration (measured across AB's missions)

| Reward | AB norm |
|---|---|
| Modifier duration | permanent (`-1`) most common; else 7300 (20y), 9125 (25y), 5475 (15y); 3650 (10y) rare |
| Monarch power | 100 typical; 50 small; 150–200 big |
| `add_years_of_income` | 0.5 / 1 / 1.5; 3 for major |
| Other common rewards | permanent claims (by far the most common), province modifiers, base tax/production/manpower, CoT levels, power projection, army/navy tradition, professionalism, trade modifiers, ruler modifiers |

- Claims on the next mission's targets are the default "connective" reward, as in AB.
- Flavourful mechanic unlocks (reforms, estates, cultures, mechanics, great projects) for mid/late missions.
- Check modifier magnitudes against a comparable AB modifier (`find.py <ab_modifier> --in ab`) rather than guessing.
- Every reward gets an accurate tooltip. Consider what the AI does with it.

## Event chains

- Real trade-offs, not good/bad. 2–4 options. AB often frames choices around identity (e.g. "Dream of Albion" / "Goidelic Union" / "British Empire").
- Fire from missions, decisions, on_actions; avoid random pulses.
- Explain system consequences plainly in the description when needed (AB's timed-mission events do this).

## Design doc template

```
# <Feature> design
Fantasy: one sentence
Who/access: tags, cultures, religions; potential/allow
Lore: link to brief
AB comparison: which AB tree/feature this is calibrated against
Structure: slot × row table, or event flow
Rewards: per mission/option
New assets: modifiers, flags, cultures, reforms, GFX, loc
Compatibility: AB files touched/overridden; interaction with ABF/TLW content
Balance / AI notes
```

Reviewing: flag unreachable missions, missing alternatives, inaccurate tooltips, rewards off AB norms, and style drift from AB.
