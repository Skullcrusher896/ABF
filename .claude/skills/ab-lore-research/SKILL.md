---
name: ab-lore-research
description: Lore and history research for ABA content, anchored to base Ante Bellum canon — separating AB canon, real history and ABA invention before writing missions, events, cultures or names. Use when designing content for a nation/culture/region, naming provinces, cultures, rulers or reforms, or when asked "what would X be like in Ante Bellum".
---

# Lore research for ABA

**Base AB is canon.** ABA content must fit AB's world and contradict nothing in it.

AB's premise (from its bookmark text): after the Hussites' defeat, the Holy Roman Empire — under the **Carolingian** dynasty — lost the Iberian Crusade to the Andalusians at Valencia; the Frankish Emperor and his son died, and the aged Lothair took the throne without an heir. Other bookmarks (e.g. *Right of Conquest*, the Nizzarid sultanate) set up further divergences. Read `$AB_PATH/localisation/AB_bookmark_l_english.yml` for the full set.

## Three layers — always label the source of a claim

1. **AB canon** — base AB files: `history/countries`, `history/provinces`, `common/cultures`, `common/religions`, AB mission/event text, bookmarks, loading tips (`localisation/replace/AB_loadingtips_replace_l_english.yml`).
2. **ABA canon** — existing ABF/TLW content (e.g. Perkunas-worshipping Livonia, Polans/Lendia split, Tocharia's three paths, TLW Rome's cultural spheres, the Punic League). Extend, don't retcon, unless asked.
3. **Real history** — the analogue AB's version grew from. Used for texture: titles, institutions, endonyms, economy, period detail.

New invention must sit on top of 1 and 2 and rhyme with 3.

## Process (cheap → expensive)

1. `find.py <TAG> <culture> <religion> --in ab` and Grep AB loc for the names — AB's own mission/event text is lore.
2. Read the tag's `history/countries` file and capital `history/provinces` file (AB, then ABA override): start state, rulers, neighbours.
3. Check existing ABA content for the tag (`find.py`, `outline.py`).
4. Only then research the real analogue (web search if available; cite sources).
5. Deliver the brief below before content is written.

## Lore brief template

```
## <Nation/Culture> — lore brief
Starting situation (AB canon, with file refs): ...
Existing ABA content: ...
Real-world analogue(s): ... (sources)
Divergence in AB: what differs and why
Themes: 3–5
Names & terms: titles, institutions, places, endonyms (origin)
Possible arcs: 2–4
Open questions / contradictions: ...
```

## Rules

- Never present invention as AB canon; when unsure, check the files.
- Keys implied by prose (cultures, tags, religions) must exist in the game files.
- Use the spellings AB uses for in-game names, even where history differs.
