import asyncio
import json

from server.app import build_mcp, client_instructions

EXPECTED = {"list_adventures", "generate_adventure", "create_game", "join_game", "generate_character", "submit_action",
            "get_results", "get_character", "get_rules", "save_story_summary"}


class Dummy:
    def __init__(self):
        self.calls = []

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
    assert {"player_id", "game_id", "kind"} <= set(sa.inputSchema["required"])
    assert "payload" in sa.inputSchema["properties"]


def test_tool_call_reaches_engine():
    d = Dummy()
    mcp = build_mcp(d)
    out = asyncio.run(mcp.call_tool("submit_action", {"player_id": "p", "game_id": "g", "kind": "action", "text": "x"}))
    assert d.calls[0][0] == "submit_action"
    assert d.calls[0][1][:3] == ("p", "g", "action")


def test_client_instructions_mention_artifacts():
    t = client_instructions()
    assert "Character state" in t and "Knowledge and plans" in t and "The story so far" in t
    assert "server data is the truth" in t.lower()
