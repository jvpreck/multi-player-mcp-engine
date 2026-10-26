# GM files: the AI Master's instructions

These files are the instructions, rules, tables, adventure and data contract for the AI Master (the Gemini model behind the MCP server). Files `AI_GM_01` to `AI_GM_05` are passed to the AI Master on every request. **This README is not** part of the prompt. Do not load it.

| File | Role | Secret from players? |
|---|---|---|
| `AI_GM_01_Agent_Protocol.md` | How the AI Master behaves: tick loop, secrecy, arbitration, solo and party play, adventure generation | Yes (GM-facing) |
| `AI_GM_02_Fear_Itself_Rules.md` | Rules (Fear Itself / GUMSHOE) with asynchronous house rules, character validation, conflict arbitration | No (player-safe) |
| `AI_GM_03_Oracles.md` | Random tables and the emergent adventure kit | Yes |
| `AI_GM_04_*.md` | A supplied adventure. Part A is player-safe, Part B is GM-only | Part B: yes |
| `AI_GM_05_State_and_Messages.md` | Supabase data model, the envelope the server sends, the JSON the AI Master returns, redaction, the narration brief | Yes |

To add another supplied adventure, add a file named `AI_GM_04_<name>.md` that follows the module contract in file 01 §16.1. The server offers every `AI_GM_04_*.md` file as an available adventure.

## What the server needs to do

1. **Build the system prompt** by concatenating files 01, 02, 03, 05 and the chosen adventure file, in that order, with a clear separator and file name before each. Use context caching: the files change rarely.
2. **Build the envelope** (file 05 §3) from Supabase for each call, in `intake` mode (one player's submission, immediate) or `resolve_tick` mode (when a tick closes).
3. **Generate the dice** (file 05 §3.2) with a cryptographic random source, fresh for every call. The AI Master does not generate random numbers.
4. **Apply the response** (file 05 §4) in one transaction: `state_changes` in order, `dice_log`, the per-player results, the shared digest, then mark the tick `resolved`. Mark the tick `resolving` first so it cannot run twice.
5. **Close ticks** on a schedule (for example Vercel Cron), when `tick_closes` passes or, with `early_close`, when every active player has submitted.
6. **Redact** (file 05 §5): return to a client only that player's result and the shared digest. Never return GM-only fields.
7. **Prefix each result** sent to a player's Claude with the narration brief (file 05 §7).

Suggested MCP tools: `join_game`, `submit_action` (intake: plan, setup answers, character, free query), `get_results` (collect stored tick results), plus an internal `resolve_tick` that is called by the scheduler and is not exposed to players.

## Vercel note

The files live in `gm/`, outside `api/`. If the deployed function cannot find them at runtime, add `"includeFiles": "gm/**"` to the `api/index.py` entry under `functions` in `vercel.json`.
