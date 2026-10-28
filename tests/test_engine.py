import json
import re
from datetime import datetime, timezone, timedelta

import pytest

from server import files, prompt, config
from server.db import MemoryStore
from server.engine import Engine, EngineError

ADV = "test_adventure"


CHECK = {"fail_next": 0, "payloads": []}


class ScriptedGM:
    """Plays the AI Master by returning prepared JSON. `rules` is a function(envelope) -> dict."""
    def __init__(self, rule):
        self.rule = rule
        self.calls = []
        self.tiers = []

    def call(self, system, user, tier="light"):
        env = json.loads(user)
        self.calls.append((system, env))
        self.tiers.append(tier)
        return json.dumps(self.rule(env, len(self.calls)))


def item(text, kind="own", **kw):
    return {"kind": kind, "language": "en", "facts": [{"block": None, "kind": "scene", "text": text}],
            "prompts": [{"id": "q", "type": "next", "text": "What now?", "options": []}],
            "narration_hints": {"mood": "", "pace": "", "senses": [], "do_not": []}, **kw}


def base():
    return {"status": "ok", "results": {}, "state_changes": [], "events": [], "decisions": [], "messages": [],
            "shared_digest": [], "dice_log": [], "errors": []}


def standard_gm(env, n):
    r = base()
    req = env.get("request") or {}
    mode = env["mode"]
    g = env["game"]
    if mode == "resolve_tick":
        t = g["clock"]["tick"]
        for c in env["characters"]:
            r["results"][c["id"]] = [item(f"Tick {t} resolved for {c['name']}")]
        r["state_changes"].append({"op": "merge", "entity": "game", "id": g["id"], "patch": {"clock": {"tick": t + 1, "day": t + 1, "block": "Morning"}}})
        return r
    kind = req.get("kind")
    pid = req.get("player_id")
    cid = req.get("character_id")
    if kind in ("game_created", "join"):
        r["results"][pid] = [item("Setup questions", kind="system")]
    elif kind == "character_submission":
        me = next(c for c in env["characters"] if c["id"] == cid)
        patch = {"status": "validated", "location": {"id": "loc_tolland_house", "detail": ""}}
        if not me.get("name"):
            patch["name"] = "Eleanor Vance" if len(env["characters"]) == 1 else "Marcus Hale"
            patch["sheet"] = {"groups": {"general": {"Health": {"max": 8, "cur": 8}}}, "derived": {}, "unrated": []}
        if CHECK["fail_next"] > 0:
            CHECK["fail_next"] -= 1
            patch["status"] = "draft"
            r["validation"] = {"character_id": cid, "result": "fail", "checks": [{"n": 3, "name": "Budget", "result": "fail", "note": "Total is 24, budget is 22."}]}
        else:
            r["validation"] = {"character_id": cid, "result": "pass", "checks": []}
        r["state_changes"].append({"op": "merge", "entity": "character", "id": cid, "patch": patch})
        r["results"][cid] = [item("Sheet checked", kind="system")]
        CHECK["payloads"].append(req["payload"])
    elif kind == "character_confirm":
        r["state_changes"] += [
            {"op": "merge", "entity": "character", "id": cid, "patch": {"status": "active"}},
            {"op": "merge", "entity": "game", "id": g["id"], "patch": {"clock": {"tick": 1, "day": 1, "block": "Morning"}}}]
        others = [c for c in env["characters"] if c.get("status") in ("validated", "active") and c["id"] != cid]
        if not others or all(c["status"] == "active" for c in others):
            r["state_changes"].append({"op": "merge", "entity": "game", "id": g["id"], "patch": {"phase": "active"}})
        r["results"][cid] = [item("Welcome", kind="system")]
    elif kind == "action":
        txt = req["text"]
        if txt.startswith("search"):
            r["handling"] = "autonomous"
            r["action"] = {"parsed": {"blocks": [{"block": "Morning", "intent": txt}]}}
            r["state_changes"].append({"op": "append", "entity": "character", "id": cid, "path": "tick_state.blocks_used", "doc": "Morning"})
            r["results"][cid] = [item("You search the room.")]
            r["events"].append({"id": "ev_1", "tick": g["clock"]["tick"], "day": 1, "block": "Morning", "location_id": "loc_tolland_house",
                                "summary": "GM view", "participants": [cid], "witnesses": [c["id"] for c in env["characters"] if c["id"] != cid],
                                "character_summaries": {c["id"]: ("You search." if c["id"] == cid else "You see someone search the drawer.") for c in env["characters"]},
                                "visibility": "gm", "tags": []})
            for c in env["characters"]:
                if c["id"] != cid:
                    r["results"][c["id"]] = [item("Someone opens the drawer and takes a revolver.", kind="witness")]
        else:
            r["handling"] = "queued"
            r["action"] = {"parsed": {"blocks": [{"block": "Afternoon", "intent": txt}]}}
            r["results"][cid] = [item("Noted. The world answers at the tick.")]
    elif kind == "decision":
        r["state_changes"].append({"op": "merge", "entity": "character", "id": cid, "patch": {"is_alive": False, "death": {"tick": 1, "cause": "fall", "summary": "You fell."}}})
        if req["payload"].get("choice") == "chosen":
            r["decisions"].append({"id": "d9", "character_id": cid, "tick": 1, "summary": "Jumped", "gm_impact": "x", "tags": ["chosen_death"]})
        r["results"][cid] = [item("You die.")]
    else:
        r["handling"] = "answered"
        r["results"][cid or pid] = [item("Answer")]
    return r


def game_pkg(**kw):
    d = {"title": "Run", "language": "en", "display_name": "Jorge", "lethality": "moderate", "pace": "slow",
         "tick_interval_hours": 24, "tick_span": "day", "pvp": "soft"}
    d.update(kw)
    if d.get("illustrations") == "on" and not d.get("image_style"):
        d["image_style"] = "Gothic ink-and-watercolour illustration, Massachusetts 1925, damp fog, sodium-yellow lamplight, muted greens and browns."
    return d


def new_game(eng, player, adv=ADV, language=None, settings=None):
    """create_game starts a work package; the client answers it with submit_package."""
    out = eng.create_game(player, adv, language=language, settings=settings)
    pkg = out["package"]
    s = settings or {}
    return eng.submit_package(player, pkg["task_id"], game_pkg(**{k: v for k, v in s.items() if k in ("lethality", "pvp", "pace", "tick_span", "tick_interval_hours", "visibility", "illustrations", "image_style")}))


def char_pkg(name="Iris Calder", concept="a reporter", **kw):
    d = {"route": "generate", "name": name, "concept": concept, "personal_goal": "find Tom",
         "sheet": {"groups": {"action": {"Health": {"max": 8, "cur": 8}}}, "derived": {}, "unrated": []},
         "known_background": ["Tom is my friend."], "language": "en"}
    d.update(kw)
    return d


def new_char(eng, player, gid, concept="a reporter", replaces=None):
    pkg = eng.generate_character(player, gid, "generate", concept=concept, replaces_character_id=replaces)["package"]
    return eng.submit_package(player, pkg["task_id"], char_pkg(concept=concept))


@pytest.fixture
def world():
    CHECK["fail_next"] = 0
    CHECK["payloads"] = []
    store = MemoryStore()
    gm = ScriptedGM(standard_gm)
    clock = {"t": datetime(2026, 11, 1, 9, 0, tzinfo=timezone.utc)}
    eng = Engine(store, gm, now_fn=lambda: clock["t"])
    return eng, store, gm, clock


def start_solo(eng, player="p_jorge"):
    out = new_game(eng, player, ADV, language="en")
    gid = out["game_id"]
    ch = eng.generate_character(player, gid, "pregen", pregen_id="pregen_test_pc")
    cid = ch["deliveries"][0]["character_id"]
    eng.submit_action(player, gid, "character_confirm", "yes", cid, {"approved": True})
    return gid, cid


# ---------------------------------------------------------------- files and prompt
def test_files_and_prompt():
    assert "fear_itself" in files.rulesets()
    assert ADV in files.adventure_files()
    adv = files.adventure_record_from_file(files.adventure_files()[ADV])
    s = prompt.system_prompt("fear_itself", adv)
    for marker in ("DOCUMENT 1: PROTOCOL", "DOCUMENT 2: ORACLES", "DOCUMENT 3: STATE CONTRACT", "DOCUMENT 4: THE RULESET", "DOCUMENT 5: THE ADVENTURE"):
        assert marker in s
    assert s.index("DOCUMENT 3") < s.index("DOCUMENT 4") < s.index("DOCUMENT 5")


def test_gm_files_are_independent_of_ruleset_and_adventure():
    banned = re.compile(r"Fear Itself|GUMSHOE|Genius Loci|Danvers|Eleanor|Berger|Hallett|file 0\d|AI_GM|Sense Trouble|Perception Drift|check_reality|Haven\b|Slips?\b|Risk Factor|Stability|Hit Threshold|Core Clue", re.I)
    for name in ("protocol.md", "oracles.md", "state_and_messages.md"):
        text = files.gm_file(name)
        hits = banned.findall(text)
        assert not hits, (name, hits[:5])


# ---------------------------------------------------------------- game flow
def test_setup_and_start_solo(world):
    eng, store, gm, clock = world
    out = new_game(eng, "p_jorge", ADV, language="en")
    assert out["setup"] and out["setup"][0]["items"][0]["facts"][0]["text"] == "Setup questions"
    gid = out["game_id"]
    game, _ = store.get("game", gid)
    assert game["settings"]["lethality"] == "moderate" and game["phase"] == "setup"
    gid, cid = start_solo(eng, "p_ana")
    game, _ = store.get("game", gid)
    assert game["phase"] == "active" and game["format"] == "solo" and game["party_size_at_start"] == 1
    assert game["clock"]["tick"] == 1 and game["ticks"][0]["status"] == "open"
    sa, _ = store.get("submit_action", f"{gid}:1")
    assert cid in sa["actions"]
    player, _ = store.get("player", "p_ana")
    assert player["characters"][0]["character_id"] == cid and cid not in json.dumps(player["games"])
    # the system prompt carries the five documents and the call used the JSON mode
    assert "DOCUMENT 5: THE ADVENTURE" in gm.calls[0][0]


def test_autonomous_then_queued_closes_tick_in_solo(world):
    eng, store, gm, clock = world
    gid, cid = start_solo(eng)
    r = eng.submit_action("p_jorge", gid, "action", "search the desk", cid)
    assert r["handling"] == "autonomous"
    c, _ = store.get("character", cid)
    assert c["tick_state"]["blocks_used"] == ["Morning"] and len(c["tick_state"]["autonomous_action_ids"]) == 1
    assert c["events"][0]["summary"] == "You search."
    r = eng.submit_action("p_jorge", gid, "action", "visit Larry in the afternoon", cid)
    assert r["handling"] == "resolved_tick" and r["tick_resolved"]
    game, _ = store.get("game", gid)
    assert game["clock"]["tick"] == 2
    assert [t["status"] for t in game["ticks"]] == ["resolved", "open"]
    assert game["ticks"][0]["results"][cid]
    sa1, _ = store.get("submit_action", f"{gid}:1")
    assert [a["status"] for a in sa1["actions"][cid]] == ["resolved_now", "resolved"]
    sa2, _ = store.get("submit_action", f"{gid}:2")
    assert sa2["actions"][cid] == []
    c, _ = store.get("character", cid)
    assert c["tick_state"] == {"tick": 2, "blocks_used": [], "queued_action_ids": [], "autonomous_action_ids": []}
    # nothing is left undelivered and a second resolve is a no-op
    assert eng.get_results("p_jorge", gid)["deliveries"] == []


def test_resolve_tick_is_idempotent(world):
    eng, store, gm, clock = world
    gid, cid = start_solo(eng)
    game, ver = store.get("game", gid)
    game["ticks"][0]["status"] = "resolved"   # as if another worker already finished tick 1
    store.put("game", gid, game, ver, {"phase": "active", "tick_closes": game["clock"]["tick_closes"]})
    calls = len(gm.calls)
    out = eng.resolve_tick(gid)
    assert out["resolved"] is False and out["reason"] == "already resolved"
    assert len(gm.calls) == calls                 # the GM is not called again
    # a tick claimed by a live worker is not resolved twice either
    game, ver = store.get("game", gid)
    game["ticks"][0]["status"] = "resolving"
    game["ticks"][0]["resolving_since"] = clock["t"].isoformat()
    store.put("game", gid, game, ver, {"phase": "active", "tick_closes": game["clock"]["tick_closes"]})
    assert eng.resolve_tick(gid)["resolved"] is False and len(gm.calls) == calls


def test_party_witness_say_and_privacy(world):
    eng, store, gm, clock = world
    out = new_game(eng, "p_jorge", ADV)
    gid = out["game_id"]
    eng.join_game("p_ana", gid)
    a = eng.generate_character("p_jorge", gid, "pregen", pregen_id="x")["deliveries"][0]["character_id"]
    b = new_char(eng, "p_ana", gid, "a doctor")["deliveries"][0]["character_id"]
    eng.submit_action("p_jorge", gid, "character_confirm", "", a, {"approved": True})
    eng.submit_action("p_ana", gid, "character_confirm", "", b, {"approved": True})
    game, _ = store.get("game", gid)
    assert game["phase"] == "active" and game["format"] == "party"
    # Eleanor searches the drawer: Marcus sees it (witness), and the event is copied to both characters
    eng.submit_action("p_jorge", gid, "action", "search the drawer", a)
    got = eng.get_results("p_ana", gid)
    assert got["deliveries"][0]["character_id"] == b
    kinds = {i["item_kind"] for i in got["deliveries"][0]["items"]}
    assert "witness" in kinds
    assert "revolver" in json.dumps(got)
    cb, _ = store.get("character", b)
    assert cb["events"][-1]["summary"] == "You see someone search the drawer."
    game, _ = store.get("game", gid)
    assert game["events"][-1]["summary"] == "GM view"
    # speech: same place, delivered without calling the GM
    calls = len(gm.calls)
    r = eng.submit_action("p_jorge", gid, "say", "Hello Marcus", a, {"to": b})
    assert len(gm.calls) == calls
    r2 = eng.get_results("p_ana", gid)
    assert any('says to you: "Hello Marcus"' in f["text"] for i in r2["deliveries"][0]["items"] for f in i["facts"])
    # speech from far away is refused
    cb, _ = store.get("character", b)
    cb["location"]["id"] = "loc_elsewhere"
    store.put("character", b, cb, store.get("character", b)[1], {"game_id": gid, "player_id": "p_ana", "is_alive": True})
    with pytest.raises(EngineError):
        eng.submit_action("p_jorge", gid, "say", "Hello?", a, {"to": b})
    # a client never receives the other player's private data
    blob = json.dumps(eng.get_results("p_ana", gid))
    assert "gm_only" not in blob and "inbox" not in blob
    # another player cannot use my character
    with pytest.raises(EngineError):
        eng.submit_action("p_ana", gid, "action", "search x", a)


def test_gm_response_with_forbidden_write_is_rejected_then_retried(world):
    eng, store, gm, clock = world
    gid, cid = start_solo(eng)
    state = {"n": 0}

    def rule(env, n):
        r = base()
        state["n"] += 1
        if state["n"] == 1:
            r["state_changes"] = [{"op": "append", "entity": "character", "id": cid, "path": "inbox", "doc": {"x": 1}}]
        else:
            assert "previous_errors" in env
            r["handling"] = "answered"
            r["results"][cid] = [item("ok")]
        return r
    eng.gm.rule = rule
    r = eng.submit_action("p_jorge", gid, "free_query", "what do I know?", cid)
    assert state["n"] == 2 and r["handling"] == "answered"
    c, _ = store.get("character", cid)
    assert all("x" not in i for i in c["inbox"])


def test_fixed_definitions_cannot_be_edited(world):
    eng, store, gm, clock = world
    gid, cid = start_solo(eng)
    seq = []

    def rule(env, n):
        r = base()
        seq.append(n)
        doc = {"name": "Mr. Hale", "role": "clerk", "trait": "ink", "goal": "x", "secret": "y", "base_stats": {"tier": "ordinary"}}
        r["state_changes"] = [{"op": "upsert", "entity": "npc", "id": "npc_hale", "doc": doc},
                              {"op": "upsert", "entity": "npc_state", "id": "npc_hale", "doc": {"status": "active", "location_id": "loc_tolland_house"}}]
        if len(seq) > 1:
            r["state_changes"].append({"op": "merge", "entity": "npc", "id": "npc_hale", "patch": {"name": "Changed"}})
        r["handling"] = "answered"
        r["results"][cid] = [item("ok")]
        return r
    eng.gm.rule = rule
    eng.submit_action("p_jorge", gid, "free_query", "who is here", cid)  # creates npc and state
    assert store.get("npc", f"{gid}:npc_hale")[0]["scope"] == {"adventure_id": None, "game_id": gid}
    assert store.get("npc_state", f"{gid}:npc_hale")[0]["game_id"] == gid
    with pytest.raises(EngineError):
        eng.submit_action("p_jorge", gid, "free_query", "again", cid)  # re-creating or editing the fixed npc is always rejected


def test_death_lethality_and_replacement(world):
    eng, store, gm, clock = world
    # moderate: death is allowed and offers replacement in the same game
    gid, cid = start_solo(eng)
    eng.submit_action("p_jorge", gid, "decision", "", cid, {"prompt_id": "q", "choice": "walk"})
    c, _ = store.get("character", cid)
    assert c["is_alive"] is False and c["status"] == "dead"
    p, _ = store.get("player", "p_jorge")
    assert p["characters"][0]["is_alive"] is False
    with pytest.raises(EngineError):
        eng.submit_action("p_jorge", gid, "action", "search", cid)  # dead characters cannot act
    r = new_char(eng, "p_jorge", gid, "a nurse", cid)
    new = r["deliveries"][0]["character_id"]
    assert new != cid
    c, _ = store.get("character", cid)
    n, _ = store.get("character", new)
    assert c["replaced_by_character_id"] == new and n["replaces_character_id"] == cid and all(f["source"].startswith("background") for f in n["knowledge"]["facts"])
    game, _ = store.get("game", gid)
    assert game["roster"][0]["character_id"] == new and game["roster_history"][0]["character_id"] == cid
    # a live character cannot be replaced
    with pytest.raises(EngineError):
        new_char(eng, "p_jorge", gid, "x", new)


def test_low_lethality_blocks_unchosen_death(world):
    eng, store, gm, clock = world
    out = new_game(eng, "p_jorge", ADV, settings={"lethality": "low"})
    gid = out["game_id"]
    cid = eng.generate_character("p_jorge", gid, "pregen")["deliveries"][0]["character_id"]
    eng.submit_action("p_jorge", gid, "character_confirm", "", cid, {})
    n = {"i": 0}
    orig = eng.gm.rule

    def rule(env, k):
        n["i"] += 1
        return orig(env, k)
    eng.gm.rule = rule
    with pytest.raises(EngineError):
        eng.submit_action("p_jorge", gid, "decision", "", cid, {"choice": "walk"})  # GM kills without a chosen_death decision, rejected twice
    c, _ = store.get("character", cid)
    assert c["is_alive"] is True
    eng.submit_action("p_jorge", gid, "decision", "", cid, {"choice": "chosen"})
    c, _ = store.get("character", cid)
    assert c["is_alive"] is False


def test_tick_due_and_resolve_due(world):
    eng, store, gm, clock = world
    out = new_game(eng, "p_jorge", ADV)
    gid = out["game_id"]
    eng.join_game("p_ana", gid)
    a = eng.generate_character("p_jorge", gid, "pregen")["deliveries"][0]["character_id"]
    b = new_char(eng, "p_ana", gid, "d")["deliveries"][0]["character_id"]
    eng.submit_action("p_jorge", gid, "character_confirm", "", a, {})
    eng.submit_action("p_ana", gid, "character_confirm", "", b, {})
    assert eng.resolve_due()["checked"] == 0
    clock["t"] += timedelta(hours=25)
    out = eng.resolve_due()
    assert out["checked"] == 1 and out["results"][0]["resolved"] is True
    game, _ = store.get("game", gid)
    assert game["clock"]["tick"] == 2 and game["clock"]["tick_closes"] > game["ticks"][0]["closes_at"]
    c, _ = store.get("character", a)
    assert c["participation"]["missed_ticks"] == 1
    # the first tick is never resolved twice
    assert eng.resolve_due()["checked"] == 0


def test_get_character_and_story_summary(world):
    eng, store, gm, clock = world
    gid, cid = start_solo(eng)
    eng.save_story_summary("p_jorge", gid, cid, "Eleanor arrived in Danvers.", 1)
    v = eng.get_character("p_jorge", gid, cid)
    assert v["character"]["story_summary"] == "Eleanor arrived in Danvers."
    assert "gm_only" not in json.dumps(v) and "inbox" not in json.dumps(v)


def adventure_pkg(**kw):
    body = "A long player-safe premise. " * 30
    secret = "The GM only plan. " * 40
    content = (f"# PART A: PLAYER-SAFE\n{body}\n\n# PART B: GM ONLY\n## The truth\n{secret}\n## Cast\nNPCs.\n## Places\nPlaces.\n"
               f"## Timeline and clock\nDays.\n## Clue matrix\nClues.\n## Finale\nFinale.\n## Endings\nEndings.\n\n# PART C: IDS\n{secret}")
    d = {"title": "The Quiet Mill", "generation": "full", "era": "1930", "place": "New England", "players": {"min": 1, "max": 3},
         "recommended": {"tick_span": "day", "tick_interval_hours": 24, "lethality": "high"}, "pace_options": ["slow"], "language": "en",
         "summary": "A mill.", "content": content,
         "npcs": [{"id": "npc_miller", "name": "Miller", "role": "owner"}], "locations": [{"id": "loc_mill", "name": "The mill"}]}
    d.update(kw)
    return d


def test_adventure_package_flow(world):
    eng, store, gm, clock = world
    calls = len(gm.calls)
    out = eng.generate_adventure("p_jorge", "fear_itself", seed_text="a haunted mill", generation="full")
    pkg = out["package"]
    assert len(gm.calls) == calls                     # the creative work is not done by the AI Master
    assert pkg["task"] == "generate_adventure" and "Generate the truth first" in pkg["instructions"]
    ctx = pkg["context"]
    assert ctx["ruleset_text"] and ctx["oracles_text"] and len(ctx["dice"]["d6"]) == 60 and ctx["seed_text"] == "a haunted mill"
    assert pkg["submission"]["tool"] == "submit_package" and "content" in pkg["submission"]["schema"]
    bad = eng.submit_package("p_jorge", pkg["task_id"], adventure_pkg(content="# PART A\nshort", players={"min": 3, "max": 1}))
    assert bad["accepted"] is False and bad["attempts_left"] == 4 and len(bad["problems"]) >= 2
    bad = eng.submit_package("p_jorge", pkg["task_id"], adventure_pkg(npcs=[{"id": "Miller", "name": "x"}]))
    assert bad["accepted"] is False and any("npc" in x for x in bad["problems"])
    ok = eng.submit_package("p_jorge", pkg["task_id"], adventure_pkg())
    assert ok["accepted"] is True
    aid = ok["adventure"]["id"]
    assert "content" not in ok["adventure"] and "GM only plan" not in json.dumps(ok)
    adv, _ = store.get("adventure", aid)
    assert adv["source"] == "generated" and adv["owner_player_id"] == "p_jorge" and "GM only plan" in adv["content"]
    assert store.get("npc", f"{aid}:npc_miller")[0]["scope"]["adventure_id"] == aid
    assert any(a["id"] == aid for a in eng.list_adventures("p_jorge")["adventures"])
    assert not any(a["id"] == aid for a in eng.list_adventures("p_other")["adventures"])
    assert "GM only plan" not in json.dumps(eng.list_adventures("p_jorge"))
    with pytest.raises(EngineError):                 # a finished task cannot be reused
        eng.submit_package("p_jorge", pkg["task_id"], adventure_pkg())
    new_game(eng, "p_jorge", aid)
    system = eng.gm.calls[-1][0]
    assert "GM only plan" in system and "written by a player's client" in system
    gp = eng.create_game("p_jorge", aid)["package"]
    assert "GM only plan" not in json.dumps(gp)


def test_emergent_adventure_needs_a_seed(world):
    eng, store, gm, clock = world
    pkg = eng.generate_adventure("p_jorge", "fear_itself", seed_text="x", generation="emergent")["package"]
    r = eng.submit_package("p_jorge", pkg["task_id"], adventure_pkg(generation="emergent"))
    assert r["accepted"] is False and any("seed" in x for x in r["problems"])
    seed = {"truth": "t", "hook": "h", "stake": "s", "antagonist": "a", "clock_ticks": 5,
            "anchor_npcs": ["a", "b", "c", "d"], "first_place": "p", "opening_handout": "o"}
    assert eng.submit_package("p_jorge", pkg["task_id"], adventure_pkg(generation="emergent", seed=seed))["accepted"] is True


def test_unknown_ruleset_and_missing_seed_refused(world):
    eng, *_ = world
    with pytest.raises(EngineError):
        eng.generate_adventure("p_jorge", "nope", seed_text="x")
    with pytest.raises(EngineError):
        eng.generate_adventure("p_jorge", "fear_itself")


def test_game_package_flow(world):
    eng, store, gm, clock = world
    out = eng.create_game("p_jorge", ADV, language="es", settings={"lethality": "high"})
    pkg = out["package"]
    assert pkg["task"] == "create_game" and pkg["context"]["defaults"]["lethality"] == "high" and pkg["context"]["defaults"]["language"] == "es"
    assert pkg["context"]["adventure"]["title"] and "player_safe_text" not in pkg["context"]["adventure"]
    assert "PART B" not in json.dumps(pkg)
    bad = eng.submit_package("p_jorge", pkg["task_id"], game_pkg(lethality="deadly", pace="warp", tick_interval_hours=0))
    assert bad["accepted"] is False and len(bad["problems"]) == 3
    ok = eng.submit_package("p_jorge", pkg["task_id"], game_pkg(lethality="low", title="My run", pvp="none"))
    assert ok["accepted"] is True and ok["game_id"] and ok["setup"]
    game, _ = store.get("game", ok["game_id"])
    assert game["settings"]["lethality"] == "low" and game["settings"]["pvp"] == "none" and game["title"] == "My run"
    assert game["roster"][0]["player_id"] == "p_jorge"


def test_character_package_flow_and_injection_is_dropped(world):
    eng, store, gm, clock = world
    gid = new_game(eng, "p_jorge", ADV)["game_id"]
    pkg = eng.generate_character("p_jorge", gid, "generate", concept="a reporter")["package"]
    ctx = pkg["context"]
    assert pkg["task"] == "generate_character" and "validation checklist" in pkg["instructions"].lower()
    assert "GUMSHOE" in ctx["ruleset_text"] and ctx["game"]["expected_party_size"] == 1
    safe = ctx["adventure"]["player_safe_text"]
    assert safe and "# PART B" not in safe and "# PART C" not in safe and "The truth (what is really going on)" not in safe
    calls = len(gm.calls)
    evil = char_pkg(gm_only={"drift": 99}, status="active", is_alive=False, inbox=[{"x": 1}], client_sync={"version": 99},
                    settings={"safety": {"lines": ["gore"]}, "standing_orders": {"hold": "stay", "evil": "x"}},
                    inventory=[{"item": "press card", "qty": 1}], relationships=[{"with_id": "npc_sam", "attitude": "ally", "trust": 9}])
    r = eng.submit_package("p_jorge", pkg["task_id"], evil)
    assert r["accepted"] is True and len(gm.calls) == calls + 1       # one cross-check by the AI Master
    cid = r["character_id"]
    c, _ = store.get("character", cid)
    assert c["gm_only"] == {} and c["is_alive"] is True and c["status"] == "validated" and c["client_sync"]["version"] < 99
    assert all("x" not in i for i in c["inbox"])
    assert c["name"] == "Iris Calder" and c["sheet"]["groups"]["action"]["Health"]["cur"] == 8
    assert c["inventory"][0]["item"] == "press card" and c["relationships"][0]["trust"] == 3
    assert c["settings"]["safety"]["lines"] == ["gore"] and "evil" not in c["settings"]["standing_orders"]
    assert c["knowledge"]["facts"][0]["confidence"] == "hearsay"
    assert CHECK["payloads"][-1]["generated_locally"] is True and CHECK["payloads"][-1]["route"] == "provided"
    eng.submit_action("p_jorge", gid, "character_confirm", "", cid, {"approved": True})
    assert store.get("game", gid)[0]["phase"] == "active"


def test_character_package_rejections_and_gm_failure_retry(world):
    eng, store, gm, clock = world
    gid = new_game(eng, "p_jorge", ADV)["game_id"]
    pkg = eng.generate_character("p_jorge", gid, "generate", concept="x")["package"]
    tid = pkg["task_id"]
    bad = eng.submit_package("p_jorge", tid, char_pkg(name="", sheet={"groups": {"action": {"Health": {"max": 8, "cur": 5}}}}))
    assert bad["accepted"] is False and len(bad["problems"]) == 2 and bad["attempts_left"] == 4
    CHECK["fail_next"] = 1
    r = eng.submit_package("p_jorge", tid, char_pkg())
    assert r["accepted"] is False and any("Budget" in p for p in r["problems"]) and r["attempts_left"] == 3
    r = eng.submit_package("p_jorge", tid, char_pkg(concept="fixed"))
    assert r["accepted"] is True
    chars = [c for c, _ in store.find("character", game_id=gid)]
    assert len(chars) == 1                                   # the failed attempt's draft was reused, not duplicated
    with pytest.raises(EngineError):
        eng.submit_package("p_ana", tid, char_pkg())
    with pytest.raises(EngineError):
        eng.submit_package("p_jorge", "t_nope", char_pkg())


def test_task_expiry_and_attempt_limit(world):
    eng, store, gm, clock = world
    pkg = eng.generate_adventure("p_jorge", "fear_itself", seed_text="x", generation="full")["package"]
    clock["t"] += timedelta(hours=49)
    with pytest.raises(EngineError):
        eng.submit_package("p_jorge", pkg["task_id"], adventure_pkg())
    pkg = eng.generate_adventure("p_jorge", "fear_itself", seed_text="x", generation="full")["package"]
    for _ in range(5):
        assert eng.submit_package("p_jorge", pkg["task_id"], {})["accepted"] is False
    with pytest.raises(EngineError):
        eng.submit_package("p_jorge", pkg["task_id"], adventure_pkg())


def test_replacement_by_package_after_death(world):
    eng, store, gm, clock = world
    gid, cid = start_solo(eng)
    eng.submit_action("p_jorge", gid, "decision", "", cid, {"choice": "walk"})
    pkg = eng.generate_character("p_jorge", gid, "generate", concept="a nurse", replaces_character_id=cid)["package"]
    assert pkg["context"]["replaces"]["character_id"] == cid and pkg["context"]["replaces"]["how_it_ended"] == "You fell."
    CHECK["fail_next"] = 1
    r = eng.submit_package("p_jorge", pkg["task_id"], char_pkg(concept="a nurse"))
    assert r["accepted"] is False
    r = eng.submit_package("p_jorge", pkg["task_id"], char_pkg(concept="a nurse"))
    assert r["accepted"] is True
    game, _ = store.get("game", gid)
    assert len(game["roster_history"]) == 1 and game["roster"][0]["character_id"] == r["character_id"]
    n, _ = store.get("character", r["character_id"])
    assert n["replaces_character_id"] == cid and n["knowledge"]["facts"][0]["text"] == "Tom is my friend."
    assert store.get("character", cid)[0]["replaced_by_character_id"] == r["character_id"]
    with pytest.raises(EngineError):
        eng.generate_character("p_jorge", gid, "generate", concept="x", replaces_character_id=r["character_id"])


def test_envelope_hides_other_characters_knowledge_in_intake(world):
    eng, store, gm, clock = world
    out = new_game(eng, "p_jorge", ADV)
    gid = out["game_id"]
    eng.join_game("p_ana", gid)
    a = eng.generate_character("p_jorge", gid, "pregen")["deliveries"][0]["character_id"]
    b = new_char(eng, "p_ana", gid, "d")["deliveries"][0]["character_id"]
    eng.submit_action("p_jorge", gid, "character_confirm", "", a, {})
    eng.submit_action("p_ana", gid, "character_confirm", "", b, {})
    eng.submit_action("p_jorge", gid, "free_query", "?", a)
    env = gm.calls[-1][1]
    mine = next(c for c in env["characters"] if c["id"] == a)
    other = next(c for c in env["characters"] if c["id"] == b)
    assert "knowledge" in mine and "knowledge" not in other and "inbox" not in mine
    assert "dice" in env and len(env["dice"]["d6"]) >= 60
