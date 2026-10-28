---
id: guide_generate_adventure
title: Generate a new adventure
---
# Generate a new adventure

Use this when the player wants a new adventure from an idea, or wants to convert an adventure document they have into the engine's format.

## Before you call

1. Make sure you have the player's `player_key`.
2. Call `list_adventures` to see the available rulesets (`ruleset_id`) and what already exists. Do not write a duplicate of an existing adventure if the player would be happy with that one.
3. Decide with the player (one batch of questions, offer defaults):
   - **Seed:** premise, theme, era, place, tone. A short paragraph is enough.
   - **Document:** if the player pastes an existing adventure, you will convert it without changing its facts.
   - **Generation mode:** `emergent` (default: a short secret seed, the rest is created in play, ideal for replay and surprise) or `full` (a complete secret plan, ideal for a fixed module).
   - **Ruleset:** one of the ids from `list_adventures`.
   - **Language** of the adventure.

## The call

`generate_adventure(player_key, ruleset_id, seed_text, document_text, generation, language)`. Give `seed_text` or `document_text`, not both.

It returns a **work package**. Its `instructions` (from the server) are the authoritative step-by-step procedure: read the ruleset and oracles, build the truth first with the server's dice stream, then the hook, antagonist, NPCs, locations and clock, then self-check. Follow them.

## Secrets

The player who generates an adventure will know its secrets, but the rest of the group must not. Do not quote the secret parts (the truth, Part B, Part C) in the chat. Show the player only the title, the premise and hook, the era, the player count and the recommended settings.

## Checklist before you submit

- Every essential conclusion has at least three routes tied to abilities that typical characters have, plus a simple search route.
- The finale has at least three fair warnings and a discoverable way through.
- The clock is stated in ticks.
- The player-safe part (Part A) reveals no secret.
- NPC and location ids are stable and unique (`npc_...`, `loc_...`).
- You used the server's dice stream in order and report `dice_used`.
- The package has the exact shape in `submission.schema`.

## After

`submit_package(player_key, task_id, package)`. If rejected, fix the listed problems and submit again. When accepted you get an `adventure_id`. Tell the player, and offer to start a game from it (`get_guide("create-game")`).
