# State and Message Contract
## Supabase data model · the envelope you receive · the JSON you return · asynchronous play

> **GM-FACING FILE (file 05 of 05).** This file defines what is stored in Supabase, what the MCP server sends you (the **envelope**), and what you must return (the **response**). Behavior is governed by file 01, rules by file 02, tables by file 03, and the adventure by file 04 or the stored generated adventure. The shape of every JSON object comes from this file.
>
> All JSON examples use illustrative ids and values. Field names and value sets are the contract. `null` means "not set".

---

## 1. Principles

1. **Supabase is the single source of truth.** You are stateless. The envelope is a snapshot. Your `state_changes` are the only way state changes.
2. **Fixed content versus this run.** The adventure (file 04 or the stored generated adventure) is fixed content. State holds only what is specific to this run.
3. **Everything established is saved.** If a player has been told it, it exists in state (file 01 §10).
4. **Visibility.** Every record is `gm`, `all`, or limited to named players. Section 5 lists the GM-only fields. The server sends a player only their own `player_results` entry and the `shared_digest`.
5. **Ids.** Use short, stable, readable ids with a prefix: `p_` player, `c_` character, `npc_` NPC, `loc_` place, `wf_` world fact, `ev_` event, `d_` decision, `pl_` plan, `se_` scheduled event, `m_` message, `k_` knowledge item, `t_` thread, `so_` spend offer, `it_` inventory item. Never reuse an id. Create new ids for new records.
6. **Idempotency.** Resolving a tick twice must change nothing. The server marks a tick `resolving` before it calls you and `resolved` after it applies your response.
7. **Time.** In-game time is a day number and a Block (Morning, Afternoon, Evening, Night). Real time is ISO 8601 UTC.

---

## 2. Entities

The server may store each entity as a table row with a `data` JSONB column plus `id`, `game_id`, `created_at` and `updated_at`. The logical fields below are what matters.

### 2.1 `game` (one record per game)

```json
{
  "id": "g_001",
  "title": "The Breathing Hill",
  "phase": "active",
  "format": "solo",
  "party_size_at_start": 1,
  "host_player_id": "p_jorge",
  "language": "en",
  "adventure": { "source": "supplied", "ref": "AI_GM_04_Genius_Loci_Adventure.md" },
  "settings": {
    "tick_interval_hours": 24,
    "tick_span": "day",
    "early_close": true,
    "pace": "slow",
    "pvp": "soft",
    "tone_preset": "sordid_gritty",
    "modules": ["hazard_stages", "perception_drift", "belief_states", "blocks_clocks"],
    "setup_deadline": "2026-11-01T18:00:00Z",
    "crisis": { "active": false, "tick_span": "beat", "tick_interval_hours": 24 }
  },
  "clock": {
    "tick": 3,
    "day": 3,
    "block": "Morning",
    "deadline_tick": 5,
    "tick_opens": "2026-11-03T08:00:00Z",
    "tick_closes": "2026-11-04T08:00:00Z"
  },
  "gm_state": {
    "tension": 2,
    "heat": 1,
    "intensity": "mild",
    "clock_steps": 0,
    "clue_progress": { "C1": { "players": ["p_jorge"], "tick": 2, "route": "automatic" } },
    "flags": {}
  },
  "chronicle": "GM-only running summary, at most 400 words, rewritten every tick."
}
```

- `phase`: `setup`, `characters`, `active`, `epilogue`, `closed`.
- `format`: `solo` or `party`, from the number of players when `setup` ends.
- `adventure.source`: `supplied`, `generated_full` or `generated_emergent`. For generated adventures, the content is the `adventure` record (§2.2).
- `tick_span`: `day` (four Blocks), `block` (one Block), `beat` (crisis). `pvp`: `none`, `soft`, `full`.
- `clock.tick` is the currently open tick. `clock.day` and `clock.block` are the in-game time at its start.
- `gm_state` and `chronicle` are GM-only. `clue_progress` maps each clue-matrix conclusion to the players who have it.

### 2.2 `adventure` (only for generated adventures; GM-only)

```json
{
  "id": "adv_g_002",
  "game_id": "g_002",
  "kind": "generated_emergent",
  "version": 4,
  "content": {
    "truth": "The rational explanation, written plainly and first.",
    "hook": "Who writes, who is missing, what deadline.",
    "antagonist": { "name": "…", "motivation": "…", "method": "…", "weakness": "…" },
    "clock": { "deadline_tick": 6, "checkpoints": [1, 3, 5] },
    "hazard": null,
    "cast_seed": ["npc_antagonist", "npc_helper", "npc_witness", "npc_authority"],
    "clue_matrix": [
      { "id": "C1", "conclusion": "…", "routes": ["…", "…", "…"] }
    ],
    "finale": { "beats": ["…"], "warnings": ["…", "…", "…"], "ways_through": ["…"] },
    "endings": ["…"],
    "notes": "Anything else needed to stay consistent."
  }
}
```

Update it with `merge` as the emergent adventure grows. Bump `version` each time. A supplied adventure is not stored here. It is the file named in `game.adventure.ref`.

### 2.3 `player`

```json
{
  "id": "p_jorge",
  "game_id": "g_001",
  "display_name": "Jorge",
  "language": "en",
  "role": "host",
  "status": "active",
  "character_id": "c_eleanor",
  "joined_tick": 0,
  "missed_ticks": 0,
  "last_submitted_tick": 2,
  "safety": {
    "lines": [],
    "veils": ["graphic injury"],
    "fears": ["not being believed"],
    "pvp_optout": false,
    "stop_signal": "pause"
  },
  "standing_orders": {
    "hold": "Stay at the lodging, rest, write up notes.",
    "risk_tolerance": "low",
    "check_reality": { "mode": "auto", "anchor": "Larry's letter", "spend": null },
    "default_spends": [],
    "never_do": ["enter the hospital alone"],
    "reply_to_messages": true
  }
}
```

- `role`: `host` or `player`. `status`: `active`, `away`, `paused`, `dropped`.
- `check_reality.mode`: `auto` or `believe`. `default_spends`: a list like `{ "ability": "Sense Trouble", "points": 1 }`.

### 2.4 `character` (the full sheet and everything specific to this run)

```json
{
  "id": "c_eleanor",
  "game_id": "g_001",
  "player_id": "p_jorge",
  "name": "Eleanor Vance",
  "status": "active",
  "origin": "pregen",
  "validation": { "result": "pass", "tick": 0, "notes": [] },
  "concept": "Dutiful freelance journalist",
  "occupation": "Freelance correspondent for regional newspapers and literary magazines",
  "era_place": "Massachusetts, November 1925",
  "appearance": null,
  "risk_factor": { "drive": "Duty", "hard": "Abandoning Larry or vulnerable people in danger she knows about", "soft": "Not printing or exposing the story" },
  "personal_goal": "Bring Larry home safely and print the truth in a form no editor or lawyer can wave away.",
  "sheet": {
    "investigative": {
      "Research": { "max": 8, "cur": 8 },
      "Bullshit Detector": { "max": 5, "cur": 5 }
    },
    "general": {
      "Health": { "max": 8, "cur": 8 },
      "Stability": { "max": 12, "cur": 12 }
    },
    "hit_threshold": 3,
    "unrated_general": ["Filch", "Scuffling", "Shooting"]
  },
  "conditions": [],
  "sources_of_stability": [
    { "name": "Peg Doyle", "kind": "person", "unlocked": true, "last_used_day": null }
  ],
  "haven": { "last_used_day": null, "breached": false },
  "location": { "id": "loc_boston_lodgings", "zone": "clear" },
  "inventory": [
    { "id": "it_01", "item": "press card", "qty": 1, "state": "carried", "notes": "", "source": "kit" }
  ],
  "means": { "money": "modest freelance income", "transport": ["train", "hired car"], "contacts": ["Peg Doyle"] },
  "relationships": [
    { "with_type": "npc", "with_id": "npc_peg", "attitude": "ally", "trust": 2, "notes": "Wants documents before she will print.", "last_tick": 1 }
  ],
  "run_notes": {
    "known_gaps": ["Cop Talk", "Streetwise", "Law", "Science"],
    "promises": [],
    "debts": [],
    "scars": [],
    "unlocked_traits": [],
    "goals_progress": "",
    "other": {}
  },
  "gm_only": { "ep": 0, "drift": 0, "slips": [], "heat_marks": 0, "surface_tests": 0, "flags": {} }
}
```

- The `sheet` holds **every** ability with its **maximum** (`max`) and **current** (`cur`) values, for both Investigative and General abilities. Health and Stability are General abilities and may go below 0.
- `status`: `pregen` (unclaimed), `active`, `dead`, `gone`, `committed`, `npc_controlled`.
- `origin`: `generated`, `pregen`, `provided`, `converted`.
- `conditions`: items like `{ "name": "Hurt", "since_tick": 3, "effect": "No Investigative spends; Difficulties +1" }`.
- `inventory[].state`: `carried`, `stored`, `lent`, `lost`, `used_up`. Add `where` when stored or lent.
- `relationships`: `with_type` is `pc` or `npc`; `trust` runs from -3 to +3. Include relationships with other player characters.
- `run_notes` is player-visible and holds what is specific to this run: injuries, promises, debts, unlocked traits, personal facts.
- `gm_only` holds Exposure Points (`ep`), Drift (`drift`), the Slip record (`slips`: `{ "tick": 3, "text": "…", "tell": "…" }`), Heat contribution, Surface tests and any hidden flags. Never show these.

### 2.5 `npc`

```json
{
  "id": "npc_hallett",
  "game_id": "g_001",
  "name": "Nurse Hallett",
  "role": "Desk nurse",
  "trait": "Half of her left ear is missing, and she touches the scar.",
  "goal": "Keep order.",
  "secret": "She was the first to join the Hour of Telling.",
  "belief_state": "devout",
  "status": "active",
  "location": { "id": "loc_front_office", "zone": "fringe" },
  "stats": {
    "tier": "ordinary",
    "health": { "max": 4, "cur": 4 },
    "stability": null,
    "abilities": { "Athletics": 3, "Scuffling": 2 },
    "hit_threshold": 3,
    "weapon_mod": null
  },
  "inventory": [{ "item": "ring of keys", "qty": 1 }],
  "attitudes": [{ "toward_player": "p_jorge", "attitude": "polite, watchful", "trust": -1, "last_tick": 3 }],
  "knows": ["Eleanor Vance asked to see Larry Croswell on day 3."],
  "schedule": "Days at the front desk. Evenings in the staff room.",
  "origin": { "by": "adventure", "tick": 0 }
}
```

- Visible to players: `name`, `role`, `trait`, and only what an investigator has actually seen or learned. Everything else is GM-only.
- `status`: `active`, `missing`, `hurt`, `dead`, `gone`.
- `origin.by`: `adventure`, `oracle` or `play`. Every NPC created in play gets a full record, including `stats` (file 02 §9), `inventory`, `attitudes` and `knows`.
- Update `knows` with what each investigator tells the NPC or does in front of them.

### 2.6 `location`

```json
{
  "id": "loc_greenhouse",
  "game_id": "g_001",
  "name": "The greenhouse",
  "zone": "hot",
  "past_detail": "A trowel rusted into a wall.",
  "features": ["Compost beds along the north wall", "Grey dust on the sills"],
  "exits": ["loc_kitchen_garden", "loc_steam_tunnel"],
  "state": "",
  "origin": { "by": "adventure", "tick": 0 }
}
```

Create a record for every place you create or that matters. `zone` is GM-only. `features` the players have seen are player-visible.

### 2.7 `player_knowledge` (one record per player)

```json
{
  "game_id": "g_001",
  "player_id": "p_jorge",
  "facts": [
    { "id": "k_001", "text": "Larry's typed letter calls him Lawrence, and Larry never types.", "tick": 2, "source": "own observation", "confidence": "verified" }
  ],
  "clues": [
    { "id": "cl_001", "text": "The hospital's letter is not in Larry's voice.", "tick": 2 }
  ],
  "documents": [
    { "id": "h2", "title": "The hospital's letter", "summary": "Typed. Asks her not to come.", "tick": 2 }
  ],
  "threads": [
    { "id": "t_001", "type": "task", "text": "Ask Miss Wentworth about the 1922 minutes.", "status": "open", "proposed_tick": 2, "updated_tick": 2 }
  ],
  "spend_offers": [
    { "id": "so_1", "ability": "Research", "cost": 1, "teaser": "There is more in the 1922 minutes.", "expires_tick": 4 }
  ],
  "journal": "Player-safe notebook summary, at most 250 words.",
  "met": ["npc_hallett"]
}
```

- This is **what each player knows**, what is **pending** (`threads`: tasks, ideas, questions and leads, with `status`: `open`, `done`, `dropped`) and what is open to claim (`spend_offers`).
- `confidence`: `verified`, `hearsay` or `perceived`. Facts told by another investigator are `hearsay` with `source: "told by <name>"`. A Slip is stored only in the character's `gm_only.slips`, never here.
- Which clue-matrix conclusions a player has is recorded in `game.gm_state.clue_progress`, not here.

### 2.8 `world_fact`, `event_log` and `decision`

**`world_fact`**: a fact about this run that is not already in the adventure.

```json
{
  "id": "wf_014",
  "game_id": "g_001",
  "text": "The hall telephone at Mrs. Tolland's house is on the landing.",
  "visibility": "all",
  "tags": ["location"],
  "source": "play",
  "tick": 2,
  "supersedes": null
}
```

- `visibility`: `"gm"`, `"all"`, or a list of player ids.
- `source`: `adventure`, `oracle`, `play` or `player`. Tag the immutable rational truth of a generated adventure with `"truth"`.

**`event_log`** (append-only): what happened, by tick, for consistency and for the chronicle.

```json
{
  "id": "ev_0031",
  "game_id": "g_001",
  "tick": 3,
  "day": 3,
  "block": "Morning",
  "location": "loc_berger_office",
  "participants": ["p_jorge", "npc_berger"],
  "summary": "Eleanor interviewed Dr. Berger and asked to visit Larry.",
  "visibility": "gm",
  "tags": ["interview", "heat"]
}
```

**`decision`**: a decision a player took that has an impact on the unfolding of the adventure.

```json
{
  "id": "d_001",
  "game_id": "g_001",
  "player_id": "p_jorge",
  "tick": 3,
  "summary": "Told Dr. Berger she is a journalist.",
  "gm_impact": "Heat +1. Berger now has her watched.",
  "tags": ["heat", "trust"],
  "status": "active"
}
```

`summary` is player-visible. `gm_impact` is GM-only. Record a decision whenever a plan chooses something with lasting consequences: an alliance, a promise, a betrayal, a lie told, a risk taken, a thing destroyed, a person trusted.

### 2.9 `plan`

```json
{
  "id": "pl_0004",
  "game_id": "g_001",
  "player_id": "p_jorge",
  "tick": 3,
  "status": "queued",
  "submitted_at": "2026-11-03T09:12:00Z",
  "raw_text": "In the morning I'll interview Dr. Berger and ask to see Larry. In the afternoon I'll visit Larry if he allows it, otherwise the library.",
  "parsed": {
    "blocks": [
      {
        "block": "Morning",
        "intent": "Interview Dr. Berger and ask to visit Larry",
        "method": "Polite, press card, mention Peg",
        "abilities": ["Bureaucracy", "Flattery", "Bullshit Detector"],
        "spend": [{ "ability": "Flattery", "points": 1 }],
        "priority": "Get permission without raising suspicion",
        "if_fails": "Withdraw politely and go to the library",
        "abort_if": "Berger asks her to stay overnight"
      },
      { "block": "Afternoon", "intent": "Visit Larry if the permit allows it, otherwise research the 1922 minutes at the Peabody Institute Library", "abilities": ["Reassurance", "Research"], "spend": [] }
    ],
    "share": [],
    "messages": [{ "to": "npc_peg", "channel": "telephone", "text": "Tell Peg I have arrived and I am going in." }],
    "tasks": [],
    "ideas": [],
    "claim_spend_offers": [],
    "continue_until_told": [],
    "questions": []
  },
  "clarifications": []
}
```

- Free text is always accepted. You parse it into `parsed` and store both. A new plan for the same tick replaces the old one (`status: "superseded"`).
- `blocks` has at most as many entries as the tick span allows (four for `day`). Each costs a Block.
- `status`: `queued`, `resolved`, `superseded`.
- `share`: `{ "to": "<character or npc id>", "text": "…" }`. `messages`: `channel` is `in_person`, `telephone`, `telegram` or `letter`.

### 2.10 `scheduled_event` and `message`

```json
{
  "id": "se_03",
  "game_id": "g_001",
  "when": { "tick": 3, "day": 3, "block": "Night" },
  "condition": "MacBride can reach a telephone",
  "what": "MacBride calls the hall telephone at the lodging.",
  "targets": ["p_jorge"],
  "fallback": "Mrs. Tolland takes a message and gives it to Eleanor in the morning.",
  "status": "pending",
  "visibility": "gm"
}
```

`status`: `pending`, `fired`, `cancelled`. Create scheduled events from the adventure's timeline at the start, and add consequences you promise (an inspector's visit, a deadline, a delivery).

```json
{
  "id": "m_01",
  "game_id": "g_001",
  "from": "p_jorge",
  "to": "npc_peg",
  "channel": "telephone",
  "text": "Tell Peg I have arrived and I am going in.",
  "sent_tick": 3,
  "deliver_tick": 3,
  "status": "delivered",
  "visibility": ["p_jorge"]
}
```

Messages between player characters are stored the same way, with `to` set to the other player's id and a delivery tick that reflects the channel.

### 2.11 `tick` and `tick_results`

```json
{
  "game_id": "g_001",
  "n": 3,
  "status": "open",
  "span": "day",
  "day": 3,
  "block_start": "Morning",
  "opens_at": "2026-11-03T08:00:00Z",
  "closes_at": "2026-11-04T08:00:00Z",
  "resolved_at": null,
  "shared_digest": []
}
```

`status`: `open`, `resolving`, `resolved`. The server stores each player's result as `{ "game_id", "tick", "player_id", "result": <player_results entry>, "delivered": false }` so players can collect it whenever they connect. The server also keeps an append-only `dice_log` (`{ "game_id", "tick", "die", "value", "for" }`).

---

## 3. The envelope (what you receive)

### 3.1 Structure

```json
{
  "mode": "resolve_tick",
  "now": "2026-11-04T08:00:00Z",
  "game": { },
  "available_adventures": [
    { "ref": "AI_GM_04_Genius_Loci_Adventure.md", "title": "Genius Loci, Danvers, 1925", "format": "solo or party", "era": "1925" }
  ],
  "adventure": { "source": "supplied", "ref": "AI_GM_04_Genius_Loci_Adventure.md", "stored": null },
  "players": [ ],
  "characters": [ ],
  "npcs": [ ],
  "locations": [ ],
  "world_facts": [ ],
  "knowledge": [ ],
  "decisions": [ ],
  "plans": [ ],
  "scheduled_events": [ ],
  "recent_events": [ ],
  "messages": [ ],
  "tick": { },
  "dice": { "d6": [4, 2, 6], "d10": [7, 1], "d20": [13, 5] },
  "request": null
}
```

- `mode`: `intake` or `resolve_tick`.
- `adventure.stored` holds the `adventure` record for generated games. For a supplied game it is `null` and the adventure text is file 04.
- `game`, `players`, `characters`, `npcs`, `locations`, `world_facts`, `knowledge`, `decisions` and `scheduled_events` are the current records. The server prunes closed items: finished threads older than five ticks, resolved scheduled events, and details of dead or gone NPCs not mentioned recently.
- `recent_events` holds the last 30 events. Use the chronicle in `game` for older history.
- `plans` are the queued plans for the open tick (all players in `resolve_tick`; the requester's in `intake`).
- `request` is `null` in `resolve_tick`.

### 3.2 Dice

The server generates `dice.d6`, `dice.d10` and `dice.d20` with a cryptographic random source for every call. Each stream is long enough for the work (the server decides the size; a typical resolve call has at least 60 d6, 20 d10 and 20 d20).

- Use each stream **in order, from the first value**. Never skip, reorder or reuse a value.
- d10 values run from 1 to 10.
- Consume dice in the order you resolve the timeline.
- Record every die you use in `dice_log`. The server discards the dice you report as used.
- If a stream runs out, return `{ "status": "needs_dice", "mode": "...", "game_id": "...", "tick": N, "player_results": {}, "state_changes": [], "dice_log": [], "errors": ["d6 stream exhausted"] }` and nothing else. The server will call you again with a fresh stream.
- Intake mode uses no dice.

### 3.3 The `request` object (intake mode)

```json
{
  "player_id": "p_jorge",
  "kind": "plan",
  "text": "In the morning I'll interview Dr. Berger…",
  "payload": { }
}
```

`kind` values:

| kind | What it is | `payload` |
|---|---|---|
| `setup_answers` | Answers to setup prompts | `{ "answers": { "<prompt id>": "…" } }` |
| `character_submission` | A character route | `{ "route": "generate|pregen|provided", "pregen_id": "c_…", "sheet_text": "…", "sheet_json": { }, "changes": "…" }` |
| `character_confirm` | The player approves or rejects the summary | `{ "approved": true }` |
| `plan` | A plan for the open tick (free text accepted) | `{ }` |
| `standing_orders` | New or changed standing orders | `{ "standing_orders": { } }` |
| `thread_note` | A task, idea or question to remember | `{ "type": "idea", "text": "…" }` |
| `message` | A message to send in the fiction | `{ "to": "…", "channel": "…", "text": "…" }` |
| `free_query` | An out-of-character question | `{ }` |
| `pause` | The stop signal | `{ }` |
| `resume` | The player returns | `{ "choice": "continue|veil|skip|stop" }` |
| `join` | A player joins the game | `{ "display_name": "…", "language": "…" }` |

If the player's text does not fit any `kind`, treat it as a free query.

---

## 4. The response (what you return)

Return **one JSON object and nothing else** (no markdown fences, no commentary).

### 4.1 Structure

```json
{
  "status": "ok",
  "mode": "resolve_tick",
  "game_id": "g_001",
  "tick": 3,
  "player_results": {
    "p_jorge": {
      "language": "en",
      "facts": [
        { "block": "Morning", "kind": "scene", "text": "The front office smells of wet wool and floor polish. Nurse Hallett touches the scar where half her left ear should be and tells you the superintendent is expecting you." },
        { "block": "Morning", "kind": "dialogue", "text": "Dr. Berger smiles slowly and says, \"Miss Vance, you are very welcome here.\" He does not let go of the third button of his coat." },
        { "block": "Morning", "kind": "result", "text": "He signs a permit for a supervised visit to Larry this afternoon. An orderly, he adds, will stand in the room the whole time." }
      ],
      "roll_report": [
        { "block": "Morning", "ability": "Flattery", "type": "spend", "spend": 1, "note": "Investigative spend, no roll" }
      ],
      "notebook_entry": null,
      "status_line": "Health 8/8. Stability 12/12. A tight headache since the front office.",
      "spend_offers": [
        { "id": "so_2", "ability": "Bullshit Detector", "cost": 1, "teaser": "Something in how Berger answered about the visit does not sit right.", "expires_tick": 5 }
      ],
      "ally_advice": [
        { "from": "npc_peg", "text": "Get that permit in writing, and do not sign anything." }
      ],
      "prompts": [
        {
          "id": "q_next_3",
          "type": "next",
          "text": "The permit lets you see Larry this afternoon with an orderly in the room. You could take the visit as planned, ask the orderly to wait outside, or call Peg first. Or tell me your own plan.",
          "options": ["Take the visit as planned", "Ask the orderly to wait outside", "Call Peg first"]
        }
      ],
      "narration_hints": {
        "mood": "polite and wrong",
        "pace": "measured",
        "senses": ["smell", "touch"],
        "do_not": ["name the cause of the headaches", "add rooms or people that are not in the facts"]
      }
    }
  },
  "shared_digest": [],
  "state_changes": [
    { "op": "append", "entity": "event_log", "doc": { "tick": 3, "day": 3, "block": "Morning", "location": "loc_berger_office", "participants": ["p_jorge", "npc_berger"], "summary": "Eleanor interviewed Dr. Berger and got a supervised-visit permit for the afternoon.", "visibility": "gm", "tags": ["interview", "heat"] } },
    { "op": "adjust", "entity": "character", "id": "c_eleanor", "path": "sheet.investigative.Flattery.cur", "delta": -1 },
    { "op": "adjust", "entity": "game", "id": "g_001", "path": "gm_state.heat", "delta": 1 },
    { "op": "merge", "entity": "plan", "id": "pl_0004", "patch": { "status": "resolved" } }
  ],
  "dice_log": [],
  "gm_notes": "Heat 1 to 2. Berger noted her press card. Next: staff in street clothes on day 4 Morning.",
  "validation": null,
  "errors": []
}
```

(The example is truncated to what fits here. A real response ends the tick with the full set of `state_changes` in §4.3 below.)

### 4.2 Fields

**Top level**

| Field | Meaning |
|---|---|
| `status` | `ok`, `needs_dice` or `error`. |
| `mode` | Echo of the envelope's mode. |
| `game_id`, `tick` | Echo. |
| `player_results` | An object keyed by player id. In `resolve_tick`, one entry per active, away or paused player. In `intake`, only the requesting player. |
| `shared_digest` | Events every player's investigator could know (an alarm, a death at the hospital, a headline). Each: `{ "text": "…", "visible_to": "all" }`. May be empty. |
| `state_changes` | The operations in §4.3. |
| `dice_log` | One entry per die used: `{ "die": "d6", "value": 4, "for": "p_jorge Morning Infiltration" }`. |
| `gm_notes` | GM-only. The server stores it and may fold it into the chronicle. Never shown to players. |
| `validation` | The character-validation block (§4.4), or `null`. |
| `errors` | A list of strings. Empty when `status` is `ok`. |

**`player_results[<player_id>]`**

| Field | Meaning |
|---|---|
| `language` | The player's language. |
| `facts` | The perspective-bounded facts, in time order. Each: `{ "block": "Morning|Afternoon|Evening|Night|null", "kind": "…", "text": "…" }`. `kind` is one of `scene`, `observation`, `dialogue`, `result`, `document`, `sensation`, `cost`, `world`, `system`. Use `system` for intake acknowledgements and out-of-character answers. |
| `roll_report` | One entry per roll or spend: `{ "block": "…", "ability": "…", "type": "test|contest|check_reality|surface|priority|spend|auto-fail", "spend": 0, "die": "d6", "value": 4, "total": 5, "outcome": "success|narrow success|failure|narrow failure|auto-fail", "note": "short, no Difficulty" }`. Leave `die`, `value` and `total` out when nothing was rolled. |
| `notebook_entry` | A short plain entry of verifiable facts in the character's voice, or `null`. Never contains a Slip. |
| `status_line` | One short plain sentence on pools and conditions. Bodies in symptoms. Never EP or Drift numbers. |
| `spend_offers` | Extras the player may claim next tick: `{ "id", "ability", "cost", "teaser", "expires_tick" }`. |
| `ally_advice` | Advice from GM-run allies: `{ "from": "<npc id>", "text": "…" }`. |
| `prompts` | Questions and gates, each `{ "id", "type", "text", "options": [ ] }`. `type` is one of `setup`, `character`, `question`, `decision_gate`, `risk_factor`, `safety_checkin`, `spoiler_confirm`, `next`. Every result includes exactly one `next` prompt (file 01 §3). |
| `narration_hints` | `{ "mood", "pace", "senses": [ ], "do_not": [ ] }`, for the front-end narrator. |

### 4.3 State-change operations

`state_changes` is an ordered list. The server applies it in order, in one transaction. If one operation fails, none apply and the server reports an error.

| op | Fields | Effect |
|---|---|---|
| `upsert` | `entity`, `id`, `doc` | Creates the record, or replaces it entirely with `doc`. Use for new NPCs, places and other new records. |
| `merge` | `entity`, `id`, `patch` | Deep-merges `patch` into the record. Objects merge. **Arrays are replaced whole.** A `null` value deletes the key. |
| `adjust` | `entity`, `id`, `path`, `delta` | Adds a number to the value at `path` (dot notation). The server does the arithmetic and does not clamp. You keep results within the rules. Use this for every pool change. |
| `append` | `entity`, `id` (when the entity is one record, such as `player_knowledge`), `path` (the array inside it), `doc` | Adds an item to an array. For log entities (`event_log`, `world_fact`, `decision`, `message`, `scheduled_event`) leave out `id` and `path`; the server assigns the id if `doc` has none. |
| `remove` | `entity`, `id`, `path`, `item_id` | Removes the array item with that `id`. |

Allowed `entity` values: `game`, `adventure`, `player`, `character`, `npc`, `location`, `player_knowledge`, `world_fact`, `event_log`, `decision`, `plan`, `scheduled_event`, `message`, `tick`.

Guidelines:

- Use `adjust` for numbers, `append` and `remove` for list items, `merge` for scalar and object fields, and `upsert` for new records. To change one item of an array, `remove` it and `append` the new version.
- Always include, in a `resolve_tick` response: the event log entries; pool changes; inventory, relationship, location and condition changes; knowledge updates for each player; `gm_state` changes (Tension, Heat, intensity, Exposure Points, Drift); NPC and location changes; scheduled events fired or added; each processed plan set to `resolved`; the `clock` advanced to the next tick (you set `tick`, `day`, `block` and `deadline_tick`; the server sets `tick_opens` and `tick_closes` from the settings); the `tick` record set to `resolved` with its `shared_digest`; and the rewritten `chronicle`.
- Exposure Points and Drift are `adjust` or `merge` operations on `character.gm_only`.
- Write each player's `journal` and `spend_offers` into their `player_knowledge`.
- In `intake` mode, limit changes to what the request needs: store the plan, standing orders, thread notes, messages, the character record and its validation, setup answers on the game, and the `phase` change when a phase completes.

### 4.4 The `validation` block

```json
{
  "character_id": "c_new",
  "result": "pass_with_adjustments",
  "party_size_used": 2,
  "checks": [
    { "n": 2, "name": "General budget", "result": "pass", "note": "Total 60." },
    { "n": 3, "name": "Investigative budget", "result": "adjust", "note": "Total 24, budget for a party of 2 is 22." }
  ],
  "adjustments": [
    { "what": "Reduce Research from 8 to 6", "why": "Investigative budget", "needs_approval": true }
  ]
}
```

`result` is `pass`, `pass_with_adjustments` or `fail`. `checks[].n` is the row of the checklist in file 02 §2.1. Also give the player a short player-safe summary in their facts and a `character` prompt asking for confirmation.

---

## 5. Redaction (what players never see)

The server must send each client only that player's `player_results` entry and the `shared_digest`. It must also redact any direct read of state. These fields are **GM-only**:

- `game.gm_state`, `game.chronicle`, and the whole `adventure` record.
- Every `character.gm_only` field, and every other player's character `inventory` and `run_notes` unless that information is publicly visible in the fiction.
- `npc`: everything except `name`, `role`, `trait`, and what a given investigator has seen or learned. In particular `secret`, `stats`, `belief_state`, `attitudes`, `knows` and `schedule`.
- `location.zone`.
- `world_fact` and `event_log` records whose `visibility` does not include the player.
- `decision.gm_impact`.
- `scheduled_event` (whole record).
- Other players' plans, knowledge, messages and standing orders.
- `dice_log`, `gm_notes`, `validation` details beyond the player's own.

Files 03 and the GM-only parts of file 04 are never sent to a client.

---

## 6. Defaults

Apply when a player or the host does not answer, or at the setup deadline.

| Setting | Default |
|---|---|
| `tick_interval_hours` | 24 |
| `tick_span` | `day` (four Blocks) |
| `early_close` | `true` for solo, `false` for party |
| `pace` | `slow` |
| `pvp` | `soft` |
| `adventure.source` | the supplied adventure if one exists, otherwise `generated_emergent` |
| `standing_orders.hold` | Stay safe, rest, take no risks |
| `standing_orders.check_reality` | `{ "mode": "auto", "anchor": null, "spend": null }` |
| `language` | the language the player last wrote in |
| Source of Stability | the adventure's default, otherwise the player's first-named person |
| `safety.stop_signal` | `pause` |

---

## 7. The narration brief (the server sends this text to the front-end Claude with every result)

The server renders each `player_results` entry as a text block and prefixes it with this brief. It is player-facing. Keep it exactly as written.

```
You are the narrator for one player in an asynchronous horror game. The game master has resolved your player's character's actions. Below are the FACTS, the ROLLS and the PROMPTS for this tick.

1. Treat the facts as ground truth. Do not add events, people, objects, clues, places or outcomes that are not in the facts. You may add sensory texture that fits them.
2. Never reveal anything that is not in the facts. Never speculate about hidden causes. Never confirm a monster, curse or ghost. Do not label any perception a hallucination.
3. Write in the player's language, in the second person, in plain storyteller sentences. No em dashes. No bullet lists, headings or tables inside the narration. About 150 to 350 words per scene.
4. Keep ordinary details next to the strange ones. Keep any distortion exactly as written.
5. Never describe what the character thinks or decides beyond the facts. The player decides.
6. After the narration, show the rolls as one short plain line each (ability, spend, die, total, outcome). Do not show or guess a Difficulty.
7. Show the notebook entry exactly as written. Show spend offers, advice and prompts as plain options. End with the "next" prompt and remind the player they can send a plan for the next tick.
8. Follow the narration hints.
```

A suggested text rendering of one result:

```
=== TICK 3 · <character name> ===
[NARRATION BRIEF]
…
[FACTS]
Morning: …
Afternoon: …
[ROLLS]
Morning, Flattery, spend 1, no roll
[NOTEBOOK]
…
[STATUS]
…
[SPEND OFFERS]
so_2: Bullshit Detector, cost 1. …
[ADVICE]
Peg: …
[PROMPTS]
next: …
[HINTS]
mood: …; pace: …; senses: …; do not: …
```
