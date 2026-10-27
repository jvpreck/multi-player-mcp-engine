# gm/ : the AI Master's files

These files are adventure- and ruleset-independent. The server builds the AI Master's system prompt from them plus one ruleset and one adventure.

| File | For | Purpose |
|---|---|---|
| `protocol.md` | AI Master | How to behave: secrecy, voice, lifecycle, interaction classes (client, query, say, autonomous, queued, message), tick resolution, arbitration, lethality and replacement, persistence, adventure generation |
| `oracles.md` | AI Master | Random tables and generators |
| `state_and_messages.md` | AI Master and server | The Supabase data model, the envelope, the JSON response |
| `player_client_brief.md` | Player's Claude | How to narrate, the three artifacts, which tools to call |
| `setup_guide.md` | CLIENT-FACING. The guide for a new player (how to start, choose a game, make a character, the commands, ticks and collaboration, autonomous actions, death, other mechanics). Returned by `get_setup_guide`. |
| `client_tasks.md` | Player's Claude | Step-by-step work packages: generate a character, generate an adventure, create a game. The server serves them to the client, which does the work locally and sends the result back with `submit_package` |

Prompt assembly order: protocol, oracles, state contract, the ruleset (`../rulesets/`), then the adventure (read from the private repository `jvpreck/rpg_adventures`, never from this one). The client brief and the client tasks are not sent to Gemini. The server gives the brief to the player's Claude as MCP `instructions`, and the tasks as work packages.

Rulesets and adventures have YAML front matter (`id`, `title`, and so on) so the server can list them. See `../README.md`.
