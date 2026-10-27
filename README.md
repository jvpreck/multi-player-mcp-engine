# multi-player-mcp-engine

An asynchronous, multi-player (or solo) tabletop RPG run by an AI Master.

- Each player uses their own free Claude account with an MCP connector, on Claude desktop, web or Android, as the front end.
- Game, character and world state live in Supabase.
- The MCP server runs on Vercel (Python, FastMCP).
- The AI Master is Google Gemini (`gemini-3.5-flash-lite` by default, thinking level `medium`, both configurable by environment variable).

## How a request flows

1. **Claude to Vercel** (HTTP POST, optionally SSE): a standard MCP JSON-RPC 2.0 call to `/mcp`.
2. **Vercel to Supabase**: the server reads the records it needs (Supabase Python client, REST).
3. **Vercel to Gemini**: the server sends one JSON "envelope" (a state snapshot, server-generated dice, the request) with the AI Master's instructions as the system prompt: protocol, oracles, state contract, the game's ruleset, and the game's adventure.
4. **Gemini to Vercel**: one JSON response: per-character result facts, state changes, events, decisions, messages. The AI Master is stateless and never writes narration.
5. **Vercel to Supabase**: the server validates the response in memory, then saves it. Events and decisions are duplicated into the game record and into each concerned character record. Witnesses of an event get their own result item.
6. **Vercel to Claude**: the server returns only the results for the calling player's characters, plus a `sync` block (player-safe current state) so the client can keep its artifacts.
7. **Claude**: narrates from the facts and keeps three artifacts (character state, knowledge and plans, story so far). The server data is always the truth.

## Play model

- **Player and character.** A player is a human (id, name, language). A character belongs to one game and holds everything about itself in one record: sheet (maximum and current), inventory, relationships, knowledge, plans, standing orders, safety settings, decisions, events and inbox. A player can have several characters in different games.
- **Adventure and game.** An adventure is fixed content (a markdown file in `adventures/`, or a generated or imported one in the database). A game is one run of it and holds everything that changes: clock, world facts, events, decisions, scheduled events, messages and ticks.
- **NPCs and locations** are a fixed definition (in the adventure, or a database record scoped to a game) plus a per-game state record.
- **Ticks.** Every tick (default 24 hours) the AI Master resolves all queued actions, arbitrates conflicts and returns each player their own results. Solo games can close the tick as soon as the player has acted (`early_close`).
- **Playing without waiting.** The client answers narration, rules and stat questions locally. Minor actions that affect only one character are resolved at once (they use up that character's Blocks of the tick). Characters in the same place can talk instantly (`say`, handled by the server without calling the AI). Others in the scene see what a character does.
- **Lethality** (`low`, `moderate`, `high`) is set per game. When a character dies the player is offered a new character, a pregenerated one, or an available NPC, and carries on in the same game.

## Repository layout

| Path | Contents |
|---|---|
| `gm/` | AI Master files, independent of any ruleset or adventure: `protocol.md`, `oracles.md`, `state_and_messages.md`; `client_tasks.md` (step-by-step instructions for the work packages, sent to the player's Claude); and `player_client_brief.md` for the player's Claude (served as MCP instructions) |
| `rulesets/` | One markdown file per ruleset, with YAML front matter (`id`, `title`, ...). Currently `fear_itself.md` |
| `adventures/` | One markdown file per adventure, with front matter (`id`, `ruleset`, `players`, `recommended`, ...). Currently `genius_loci_danvers_1925.md` |
| `server/` | The Python server: `app.py` (gateway and MCP), `tools.py`, `engine.py`, `apply.py`, `db.py`, `prompt.py`, `gm.py`, `redact.py`, `dice.py`, `files.py`, `config.py` |
| `api/index.py` | Vercel entry point |
| `supabase/schema.sql` | Tables (`gm_*`) to create in Supabase |
| `tests/` | Unit tests with an in-memory database and a scripted AI Master |

To add a ruleset or an adventure, drop a markdown file with front matter into `rulesets/` or `adventures/`. An adventure names its ruleset in `ruleset:`.

## MCP tools (for players)

| Tool | Purpose |
|---|---|
| `list_adventures` | Adventures (files and the player's generated ones) and rulesets |
| `generate_adventure` | Returns a **work package** to write a new adventure locally (from a seed or a document) |
| `create_game` | Returns a work package to choose the game settings (lethality, tick, party size) locally |
| `join_game` | Join a game by id |
| `generate_character` | `generate` and `provided` return a work package to build or check the sheet locally; `pregen` and `from_npc` are handled on the server |
| `submit_package` | Sends back the finished package (`task_id` and the result). The server validates and stores it, or returns the problems to fix |
| `submit_action` | Actions, speech, setup answers, character confirmation, standing orders, decisions, messages, free queries, pause |
| `get_results` | Collect results not yet delivered |
| `get_character`, `get_rules`, `save_story_summary` | Resync, read the ruleset, store the client's story summary |

**Work packages.** For creative work, the server sends the client a structured package: step-by-step instructions, the ruleset and context needed, the exact schema of the result, and the instruction to return it with `submit_package`. The client does the work locally. The server checks structure and limits, stores the result and, for characters, has the AI Master cross-check the sheet against the rules. A package expires after 48 hours and allows 5 attempts. A client-written adventure is stored as data and fenced in the AI Master's prompt, so it cannot change the protocol. Only join games from hosts you trust.

`resolve_tick` is **not** a player tool. It is an HTTP endpoint for the server side: `GET|POST /internal/resolve_tick` (optional `?game_id=`), protected by `Authorization: Bearer $CRON_SECRET`. Without `game_id` it resolves every game whose tick is due. Call it from a scheduler (Vercel Cron, a GitHub Action, or any cron).

## Setup

1. Run `supabase/schema.sql` in the Supabase SQL editor.
2. Environment variables on Vercel:
   - `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY`
   - `GEMINI_API_KEY`; optional `GEMINI_MODEL` (default `gemini-3.5-flash-lite`) and `GEMINI_THINKING_LEVEL` (default `medium`)
   - `MCP_API_KEY`: the shared key for players (`Authorization: Bearer`, `x-api-key`, or `?key=` in the connector URL)
   - `CRON_SECRET`: for `/internal/resolve_tick`
3. Players add `https://<your-app>.vercel.app/mcp?key=<MCP_API_KEY>` as a custom connector.
4. Schedule `/internal/resolve_tick`. Vercel Hobby cron runs at most once a day, so use an external scheduler for hourly checks.

## Tests

```
pip install -r requirements.txt pytest
pytest tests
```

## Known limits

- **Authentication is one shared key.** A player is identified by the `player_id` they send, so a player with the key could impersonate another. Per-player keys or OAuth would fix this.
- **Cross-record writes are not one database transaction.** The server validates everything in memory and saves with optimistic version checks, so a rejected AI response changes nothing, but a crash in the middle of saving could leave records out of step.
- **Vercel limits.** `maxDuration` is 60 seconds. A tick with many characters and a large thinking budget may need more (Pro plan).
- **The AI Master is an LLM.** The server enforces structure, ownership of fields, dice, and the lethality guard, but the AI's judgement on secrecy and fairness is not machine-checked. A lite model on a long, rule-dense JSON task is unbenchmarked here, so `GEMINI_MODEL` can be changed without code changes.
