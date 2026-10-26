"""MCP tools. Players use these. resolve_tick is NOT a player tool: see app.py (/internal/resolve_tick)."""
import functools

from .engine import Engine, EngineError
from .db import Conflict


def _safe(fn):
    @functools.wraps(fn)
    def wrapper(*a, **kw):
        try:
            return fn(*a, **kw)
        except EngineError as e:
            return {"error": str(e)}
        except Conflict:
            return {"error": "The game changed while your request was processed. Please try again."}
    return wrapper


def register(mcp, engine: Engine):
    @mcp.tool()
    @_safe
    def list_adventures(player_id: str) -> dict:
        """List the adventures and rulesets available. Adventures can be supplied files or ones you generated."""
        return engine.list_adventures(player_id)

    @mcp.tool()
    @_safe
    def generate_adventure(player_id: str, ruleset_id: str, seed_text: str = "", document_text: str = "",
                           generation: str = "emergent", language: str = "en") -> dict:
        """Generate a new adventure from a short seed (premise, theme, era, place) or from a document with notes or a full adventure.
        generation is 'emergent' (a secret seed, the rest is created in play) or 'full' (a complete secret plan)."""
        return engine.generate_adventure(player_id, ruleset_id, seed_text, document_text, generation, language)

    @mcp.tool()
    @_safe
    def create_game(player_id: str, adventure_id: str, title: str = "", language: str = "", display_name: str = "",
                    lethality: str = "", tick_interval_hours: int = 0, tick_span: str = "", pvp: str = "") -> dict:
        """Create a new game run from an adventure and become its host. Optional settings: lethality (low, moderate, high),
        tick_interval_hours, tick_span (day, block), pvp (none, soft, full). Returns the setup questions."""
        s = {k: v for k, v in {"lethality": lethality, "tick_interval_hours": tick_interval_hours or None,
                               "tick_span": tick_span, "pvp": pvp}.items() if v}
        return engine.create_game(player_id, adventure_id, title or None, language or None, s, display_name or None)

    @mcp.tool()
    @_safe
    def join_game(player_id: str, game_id: str, display_name: str = "", language: str = "") -> dict:
        """Join an existing game by its id."""
        return engine.join_game(player_id, game_id, display_name or None, language or None)

    @mcp.tool()
    @_safe
    def generate_character(player_id: str, game_id: str, route: str = "generate", concept: str = "", pregen_id: str = "",
                           sheet_text: str = "", sheet_json: dict | None = None, npc_id: str = "",
                           replaces_character_id: str = "", changes: str = "") -> dict:
        """Create a character for a game. route: 'generate' (built with the Master from a concept), 'pregen' (pick a pregenerated
        one), 'provided' (a sheet you paste, cross-checked against the rules) or 'from_npc' (replacement only, from an available NPC).
        After a character dies, pass replaces_character_id to continue in the same game."""
        return engine.generate_character(player_id, game_id, route, concept, pregen_id or None, sheet_text, sheet_json,
                                         npc_id or None, replaces_character_id or None, changes)

    @mcp.tool()
    @_safe
    def submit_action(player_id: str, game_id: str, kind: str, text: str = "", character_id: str = "",
                      payload: dict | None = None) -> dict:
        """Send anything the character does or the player decides. kind is one of: action (what the character wants to do, free text),
        say (speak to a character in the same place; payload {to, whisper}), setup_answers (payload {answers}),
        character_submission, character_confirm (payload {approved}), standing_orders (payload {standing_orders, safety}),
        thread_note (payload {type, text}), message (payload {to, channel, text}), decision (payload {prompt_id, choice}),
        free_query, pause, resume (payload {choice}). Minor actions that affect only your character are resolved at once;
        the rest wait for the tick. Returns the results now available to you."""
        return engine.submit_action(player_id, game_id, kind, text, character_id or None, payload)

    @mcp.tool()
    @_safe
    def get_results(player_id: str, game_id: str = "") -> dict:
        """Collect results you have not received yet: tick results, what other characters did in front of yours, messages and speech.
        Call it at the start of every session and whenever the player asks what happened."""
        return engine.get_results(player_id, game_id or None)

    @mcp.tool()
    @_safe
    def get_character(player_id: str, game_id: str, character_id: str = "") -> dict:
        """Fetch the character's current state, knowledge, settings and saved story summary from the server (the truth)."""
        return engine.get_character(player_id, game_id, character_id or None)

    @mcp.tool()
    @_safe
    def get_rules(ruleset_id: str) -> dict:
        """Read the text of a ruleset."""
        return engine.get_rules(ruleset_id)

    @mcp.tool()
    @_safe
    def save_story_summary(player_id: str, game_id: str, character_id: str, text: str, tick: int = -1) -> dict:
        """Store the story summary you keep for the character, so it survives if the chat is compacted."""
        return engine.save_story_summary(player_id, game_id, character_id, text, None if tick < 0 else tick)
