import asyncio
import json

from server.app import build_mcp, client_instructions

EXPECTED = {"register_player", "get_setup_guide", "list_games", "list_adventures", "generate_adventure", "create_game", "join_game", "generate_character", "submit_action",
            "get_results", "get_character", "get_rules", "save_story_summary", "submit_package", "list_images", "get_image", "set_game_options"}


class Dummy:
    def __init__(self):
        self.calls = []

    def authenticate(self, key):
        return "p_" + key

    def __getattr__(self, name):
        def f(*a, **k):
            self.calls.append((name, a, k))
            return {"ok": name}
        return f


def test_tools_exposed_and_resolve_tick_is_not_a_player_tool():
    mcp = build_mcp(Dummy())
    tools = asyncio.run(mcp.list_tools())
    names = {t.name for t in tools}
    assert names == EXPECTED
    assert "resolve_tick" not in names
    sa = next(t for t in tools if t.name == "submit_action")
    assert {"player_key", "game_id", "kind"} <= set(sa.inputSchema["required"])
    assert "player_id" not in sa.inputSchema["properties"]
    # nothing in the player tools can administer the server
    assert not [n for n in names if "delete" in n or "admin" in n or "reset" in n]
    assert "payload" in sa.inputSchema["properties"]


def test_tool_call_reaches_engine():
    d = Dummy()
    mcp = build_mcp(d)
    out = asyncio.run(mcp.call_tool("submit_action", {"player_key": "p", "game_id": "g", "kind": "action", "text": "x"}))
    assert d.calls[0][0] == "submit_action"
    assert d.calls[0][1][:3] == ("p_p", "g", "action")


def test_client_instructions_mention_artifacts():
    t = client_instructions()
    assert "Character state" in t and "Knowledge and plans" in t and "The story so far" in t
    assert "server data is the truth" in t.lower()


def test_new_player_tools_need_no_key_only_where_intended():
    mcp = build_mcp(Dummy())
    tools = {t.name: t for t in asyncio.run(mcp.list_tools())}
    assert "player_key" not in tools["get_setup_guide"].inputSchema.get("required", [])
    assert "player_key" not in tools["register_player"].inputSchema.get("required", [])
    for n in ("list_games", "join_game", "create_game", "submit_action", "get_results"):
        assert "player_key" in tools[n].inputSchema["required"], n
