# gm/ : the AI Master's files

These files are adventure- and ruleset-independent. The server builds the AI Master's system prompt from them plus one ruleset and one adventure.

| File | For | Purpose |
|---|---|---|
| `protocol.md` | AI Master | How to behave: secrecy, voice, lifecycle, interaction classes (client, query, say, autonomous, queued, message), tick resolution, arbitration, lethality and replacement, persistence, adventure generation |
| `oracles.md` | AI Master | Random tables and generators |
| `state_and_messages.md` | AI Master and server | The Supabase data model, the envelope, the JSON response |
| `player_client_brief.md` | Player's Claude | How to narrate, the three artifacts, which tools to call |

Prompt assembly order: protocol, oracles, state contract, the ruleset (`../rulesets/`), then the adventure (`../adventures/`). The client brief is not sent to Gemini. The server gives it to the player's Claude as MCP `instructions`.

Rulesets and adventures have YAML front matter (`id`, `title`, and so on) so the server can list them. See `../README.md`.
