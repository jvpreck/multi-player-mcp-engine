import json
from datetime import datetime, timedelta, timezone

import pytest

from server import admin, config
from server.db import MemoryStore
from server.engine import Engine, EngineError
from server.gm import Usage
from server.images import ImageError, ImageService, MemoryImageStorage
from test_engine import ScriptedGM, standard_gm, ADV, new_game, CHECK


class Clock:
    def __init__(self):
        self.t = datetime(2026, 11, 1, 9, tzinfo=timezone.utc)

    def __call__(self):
        return self.t


class FakeProvider:
    def __init__(self):
        self.calls = []
        self.fail = False
        self.ok = True

    def configured(self):
        return self.ok

    def generate(self, prompt):
        self.calls.append(prompt)
        if self.fail:
            raise ImageError("provider down")
        return b"\xff\xd8fakejpeg", "image/jpeg"


PROPOSALS = {"items": None}


def gm_rule(env, n):
    r = standard_gm(env, n)
    if env["mode"] == "resolve_tick":
        ids = [c["id"] for c in env["characters"]]
        r["illustrations"] = [dict(i, visible_to=[x if x != "FIRST" else ids[0] for x in i["visible_to"]]) for i in (PROPOSALS["items"] or [])]
    return r


@pytest.fixture
def world():
    store, clock = MemoryStore(), Clock()
    prov, storage = FakeProvider(), MemoryImageStorage()
    CHECK["fail_next"] = 0
    PROPOSALS["items"] = [{"prompt": "A wet stone road at dusk, a lone lamp, mist, wide shot, 1925", "caption": "The road to the hill", "visible_to": ["FIRST"]}]
    eng = Engine(store, ScriptedGM(gm_rule), now_fn=clock, images=ImageService(prov, storage, Usage(store, clock)))
    return eng, store, prov, storage, clock


def start(eng, player, illustrations="on"):
    gid = new_game(eng, player, ADV, settings={"illustrations": illustrations})["game_id"]
    cid = eng.generate_character(player, gid, "pregen", pregen_id="pregen_test_pc")["deliveries"][0]["character_id"]
    eng.submit_action(player, gid, "character_confirm", "yes", cid, {"approved": True})
    return gid, cid


def test_option_is_offered_only_when_the_provider_is_set_up(world):
    eng, store, prov, storage, clock = world
    pkg = eng.create_game("p_a", ADV)["package"]
    assert pkg["context"]["options"]["illustrations"] == ["off", "on"]
    prov.ok = False
    pkg = eng.create_game("p_a", ADV)["package"]
    assert pkg["context"]["options"]["illustrations"] == ["off"]
    r = new_game(eng, "p_a", ADV, settings={"illustrations": "on"})
    assert r["accepted"] is False and "not available" in " ".join(r["problems"])
    assert new_game(eng, "p_a", ADV)["accepted"] is True                      # off is always fine
    plain = Engine(store, ScriptedGM(gm_rule))                                  # no image service at all
    assert plain.create_game("p_a", ADV)["package"]["context"]["options"]["illustrations"] == ["off"]


def test_proposals_are_queued_only_when_on_and_bad_ones_dropped(world):
    eng, store, prov, storage, clock = world
    gid, cid = start(eng, "p_a")
    PROPOSALS["items"] += [{"prompt": "x", "caption": "too short", "visible_to": ["FIRST"]},
                           {"prompt": "A long enough prompt but nobody can see it", "caption": "c", "visible_to": ["c_unknown"]},
                           {"prompt": "A third valid one beyond the per-tick limit", "caption": "c", "visible_to": ["FIRST"]}]
    eng.resolve_tick(gid)
    imgs = [d for d, _ in store.find("image", game_id=gid)]
    assert len(imgs) == 1 and imgs[0]["status"] == "pending" and imgs[0]["visible_to"] == [cid] and prov.calls == []
    gid2, _ = start(eng, "p_b", illustrations="off")
    eng.resolve_tick(gid2)
    assert store.find("image", game_id=gid2) == []                              # off: the AI Master's proposals are ignored


def test_draw_deliver_list_and_ask_again(world):
    eng, store, prov, storage, clock = world
    gid, cid = start(eng, "p_a")
    eng.resolve_tick(gid)
    iid = store.find("image", game_id=gid)[0][0]["id"]
    assert eng.get_image("p_a", gid, iid)["status"] == "pending"
    assert eng.list_images("p_a", gid)["images"][0]["status"] == "pending"
    out = eng.process_images()
    assert out["generated"] == 1 and len(storage.files) == 1
    path = next(iter(storage.files))
    assert path == f"{gid}/{iid}.jpg" and "wet stone road" in prov.calls[0] and prov.calls[0].startswith(config.IMAGE_STYLE)
    # the player is told once
    first = eng.get_results("p_a", gid)
    assert [i["image_id"] for i in first["illustrations"]] == [iid] and first["illustrations"][0]["caption"] == "The road to the hill"
    assert eng.get_results("p_a", gid)["illustrations"] == []
    # asking for it gives a short-lived link, and again gives another, also later in time
    a = eng.get_image("p_a", gid, iid)
    assert a["status"] == "ready" and a["url"].endswith(f"expires_in={config.IMAGE_URL_TTL_SECONDS}") and path in a["url"]
    assert a["expires_in_seconds"] == config.IMAGE_URL_TTL_SECONDS
    clock.t += timedelta(days=10)                                               # long after the first link expired
    b = eng.get_image("p_a", gid, iid)
    assert b["status"] == "ready" and path in b["url"] and b["expires_in_seconds"] == config.IMAGE_URL_TTL_SECONDS
    assert [i["image_id"] for i in eng.list_images("p_a", gid)["images"]] == [iid]
    # the record holds no link and no image bytes
    rec = store.get("image", iid)[0]
    assert "url" not in json.dumps(rec) and rec["path"] == path and rec["status"] == "ready"


def test_only_the_characters_who_saw_it_can_get_it(world):
    eng, store, prov, storage, clock = world
    gid, cid = start(eng, "p_a")
    eng.join_game("p_b", gid)
    eng.generate_character("p_b", gid, "pregen", pregen_id="pregen_test_pc")
    eng.resolve_tick(gid)
    eng.process_images()
    iid = store.find("image", game_id=gid)[0][0]["id"]
    with pytest.raises(EngineError):
        eng.get_image("p_b", gid, iid)                                          # was not in visible_to
    assert eng.list_images("p_b", gid)["images"] == []
    with pytest.raises(EngineError):
        eng.get_image("p_c", gid, iid)                                          # not even in the game
    with pytest.raises(EngineError):
        eng.get_image("p_a", gid, "img_nope")
    assert eng.get_results("p_b", gid)["illustrations"] == []


def test_failures_quota_budget_and_expiry(world):
    eng, store, prov, storage, clock = world
    gid, cid = start(eng, "p_a")
    eng.resolve_tick(gid)
    iid = store.find("image", game_id=gid)[0][0]["id"]
    prov.fail = True
    assert eng.process_images()["failed"] == 0 and store.get("image", iid)[0]["status"] == "pending"   # one more try allowed
    assert eng.process_images()["failed"] == 1 and store.get("image", iid)[0]["status"] == "failed"
    assert eng.get_image("p_a", gid, iid)["status"] == "failed"
    # no time left in the function: nothing is drawn, the picture stays queued
    prov.fail = False
    PROPOSALS["items"][0]["caption"] = "second"
    eng.submit_action("p_a", gid, "action", "wait", cid)
    eng.resolve_tick(gid)
    pend = [d for d, _ in store.find("image", game_id=gid, status="pending")]
    assert pend                                     # a solo action closes the tick at once, so there can be more than one
    assert eng.process_images(budget_seconds=1) == {"generated": 0, "failed": 0, "dropped": 0} and prov.calls.__len__() == 2
    # the daily guard stops generation but leaves the picture queued
    store.t["usage"].clear()
    u = Usage(store, clock)
    config.GEMINI_LIMITS["image"]["rpd"], saved = 0, config.GEMINI_LIMITS["image"]["rpd"]
    try:
        assert eng.process_images()["generated"] == 0
    finally:
        config.GEMINI_LIMITS["image"]["rpd"] = saved
    assert store.get("image", pend[0]["id"])[0]["status"] == "pending"
    # a picture nobody could draw in three days is dropped
    clock.t += timedelta(days=config.IMAGE_PENDING_DAYS, hours=1)
    assert eng.process_images()["dropped"] == len(pend)


def test_only_the_host_of_the_game_sets_options(world):
    eng, store, prov, storage, clock = world
    gid, cid = start(eng, "p_a", illustrations="off")
    eng.join_game("p_b", gid)
    with pytest.raises(EngineError):
        eng.set_game_options("p_b", gid, "on")
    assert eng.set_game_options("p_a", gid, "on")["illustrations"] == "on"
    with pytest.raises(EngineError):
        eng.set_game_options("p_a", gid, "maybe")
    prov.ok = False
    with pytest.raises(EngineError):
        eng.set_game_options("p_a", gid, "on")                                  # not set up on this server


def test_deleting_a_game_deletes_its_pictures(world):
    eng, store, prov, storage, clock = world
    gid, cid = start(eng, "p_a")
    eng.resolve_tick(gid)
    eng.process_images()
    assert storage.files and store.find("image", game_id=gid)
    out = admin.run(eng, "delete_game", {"game_id": gid})
    assert out["records"]["image"] == 1 and storage.files == {} and store.find("image", game_id=gid) == []
    assert admin.run(eng, "generate_images")["generated"] == 0
    assert admin.run(eng, "gm_usage")["usage"]["image"]["model"] == config.IMAGE_MODEL


def test_scheduler_draws_pictures_after_resolving(world):
    eng, store, prov, storage, clock = world
    gid, cid = start(eng, "p_a")
    clock.t += timedelta(days=2)
    out = eng.resolve_due()
    assert out["images"]["generated"] == 1 and len(storage.files) == 1
