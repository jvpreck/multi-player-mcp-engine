"""MCP tools. Players use these, identified by their secret player key (see register_player).
There are no administrator tools here: resolve_tick and the host commands live behind /internal/* (see app.py and admin.py)."""
import functools

from .engine import Engine, EngineError
from .db import Conflict
from .files import AdventureSourceError


def _safe(fn):
    @functools.wraps(fn)
    def wrapper(*a, **kw):
        try:
            return fn(*a, **kw)
        except EngineError as e:
            return {"error": str(e)}
        except AdventureSourceError as e:
            return {"error": f"The supplied adventures cannot be read right now ({e}). Try again later."}
        except Conflict:
            return {"error": "The game changed while your request was processed. Please try again."}
    return wrapper


def register(mcp, engine: Engine):
    @mcp.tool()
    @_safe
    def register_player(display_name: str = "", language: str = "en") -> dict:
        """First step for a new player. Creates the player and returns their secret player_key, shown only once. Keep it (in this chat or
        project) and pass it as player_key on every other call. Never show it to anyone else, and never print it in shared places."""
        return engine.register_player(display_name, language)

    @mcp.tool()
    @_safe
    def get_setup_guide(topic: str = "") -> dict:
        """The guide for a new player. Needs no key. topic is empty for the whole guide, or one of: start, choose, character, commands,
        ticks, autonomous, death, mechanics. Relay it in the player's language and show only what was asked."""
        return engine.setup_guide(topic)

    @mcp.tool()
    @_safe
    def list_games(player_key: str) -> dict:
        """The player's games, and the open games that have free seats and can be joined with join_game."""
        return engine.list_games(engine.authenticate(player_key))

    @mcp.tool()
    @_safe
    def list_adventures(player_key: str) -> dict:
        """List the adventures and rulesets available. Adventures can be supplied files or ones you generated."""
        return engine.list_adventures(engine.authenticate(player_key))

    @mcp.tool()
    @_safe
    def generate_adventure(player_key: str, ruleset_id: str, seed_text: str = "", document_text: str = "",
                           generation: str = "emergent", language: str = "en") -> dict:
        """Start generating a new adventure from a short seed (premise, theme, era, place) or from a document. Returns a work package:
        follow its instructions step by step in the chat, then send the result with submit_package.
        generation is 'emergent' (a secret seed, the rest is created in play) or 'full' (a complete secret plan)."""
        return engine.generate_adventure(engine.authenticate(player_key), ruleset_id, seed_text, document_text, generation, language)

    @mcp.tool()
    @_safe
    def create_game(player_key: str, adventure_id: str, title: str = "", language: str = "", display_name: str = "",
                    lethality: str = "", tick_interval_hours: int = 0, tick_span: str = "", pvp: str = "", visibility: str = "") -> dict:
        """Start a new game run from an adventure. Returns a work package that collects the settings (lethality low, moderate or high,
        tick interval, pvp, pace, language, visibility private or open) with the player; then send the result with submit_package. Optional arguments prefill defaults."""
        s = {k: v for k, v in {"lethality": lethality, "tick_interval_hours": tick_interval_hours or None,
                               "tick_span": tick_span, "pvp": pvp, "visibility": visibility}.items() if v}
        return engine.create_game(engine.authenticate(player_key), adventure_id, title or None, language or None, s, display_name or None)

    @mcp.tool()
    @_safe
    def join_game(player_key: str, game_id: str, display_name: str = "", language: str = "") -> dict:
        """Join an existing game by its id."""
        return engine.join_game(engine.authenticate(player_key), game_id, display_name or None, language or None)

    @mcp.tool()
    @_safe
    def generate_character(player_key: str, game_id: str, route: str = "generate", concept: str = "", pregen_id: str = "",
                           sheet_text: str = "", sheet_json: dict | None = None, npc_id: str = "",
                           replaces_character_id: str = "", changes: str = "") -> dict:
        """Create a character for a game. route 'generate' (build a new one) and 'provided' (convert and check a sheet the player pastes)
        return a work package to follow in the chat, then send the result with submit_package. route 'pregen' (pick a pregenerated one)
        and 'from_npc' (replacement only, from an available NPC) act at once. After a character dies, pass replaces_character_id
        to continue in the same game."""
        return engine.generate_character(engine.authenticate(player_key), game_id, route, concept, pregen_id or None, sheet_text, sheet_json,
                                         npc_id or None, replaces_character_id or None, changes)

    @mcp.tool()
    @_safe
    def submit_package(player_key: str, task_id: str, package: dict) -> dict:
        """Send back the finished work package for generate_adventure, create_game or generate_character. If accepted is false, fix the
        listed problems and submit again with the same task_id."""
        return engine.submit_package(engine.authenticate(player_key), task_id, package)

    @mcp.tool()
    @_safe
    def submit_action(player_key: str, game_id: str, kind: str, text: str = "", character_id: str = "",
                      payload: dict | None = None) -> dict:
        """Send anything the character does or the player decides. kind is one of: action (what the character wants to do, free text),
        say (speak to a character in the same place; payload {to, whisper}), setup_answers (payload {answers}),
        character_submission, character_confirm (payload {approved}), standing_orders (payload {standing_orders, safety}),
        thread_note (payload {type, text}), message (payload {to, channel, text}), decision (payload {prompt_id, choice}),
        free_query, pause, resume (payload {choice}). Minor actions that affect only your character are resolved at once;
        the rest wait for the tick. Returns the results now available to you."""
        return engine.submit_action(engine.authenticate(player_key), game_id, kind, text, character_id or None, payload)

    @mcp.tool()
    @_safe
    def get_results(player_key: str, game_id: str = "") -> dict:
        """Collect results you have not received yet: tick results, what other characters did in front of yours, messages and speech.
        Call it at the start of every session and whenever the player asks what happened."""
        return engine.get_results(engine.authenticate(player_key), game_id or None)

    @mcp.tool()
    @_safe
    def get_character(player_key: str, game_id: str, character_id: str = "") -> dict:
        """Fetch the character's current state, knowledge, settings and saved story summary from the server (the truth)."""
        return engine.get_character(engine.authenticate(player_key), game_id, character_id or None)

    @mcp.tool()
    @_safe
    def get_rules(ruleset_id: str) -> dict:
        """Read the text of a ruleset."""
        return engine.get_rules(ruleset_id)

    @mcp.tool()
    @_safe
    def save_story_summary(player_key: str, game_id: str, character_id: str, text: str, tick: int = -1) -> dict:
        """Store the story summary you keep for the character, so it survives if the chat is compacted."""
        return engine.save_story_summary(engine.authenticate(player_key), game_id, character_id, text, None if tick < 0 else tick)
