import json
from datetime import datetime, timedelta, timezone

import pytest

from server import config
from server.db import MemoryStore
from server.engine import Engine, EngineError
from server.gm import GeminiGM, GMBusy, Usage
from test_engine import ScriptedGM, standard_gm, start_solo, CHECK


class Clock:
    def __init__(self):
        self.t = datetime(2026, 11, 1, 9, tzinfo=timezone.utc)

    def __call__(self):
        return self.t


@pytest.fixture
def world():
    store, clock = MemoryStore(), Clock()
    gm = ScriptedGM(standard_gm)
    CHECK["fail_next"] = 0
    return Engine(store, gm, now_fn=clock), store, gm, clock


def test_engine_picks_the_tier(world):
    eng, store, gm, clock = world
    gid, cid = start_solo(eng)
    assert "tick" in gm.tiers                      # the character cross-check uses the strong model
    gm.tiers.clear()
    eng.submit_action("p_jorge", gid, "free_query", "what do I see?", cid)
    assert gm.tiers and set(gm.tiers) == {"light"}  # single-player requests use the light model
    gm.tiers.clear()
    eng.resolve_tick(gid)
    assert gm.tiers == ["tick"]                     # closing the tick uses the strong model


def usage(store, clock):
    return Usage(store, clock, sleep=lambda s: clock.__setattr__("t", clock.t + timedelta(seconds=s)))


def test_usage_limits_per_minute_and_per_day(monkeypatch):
    monkeypatch.setitem(config.GEMINI_LIMITS, "tick", {"rpd": 3, "rpm": 2})
    store, clock = MemoryStore(), Clock()
    u = usage(store, clock)
    assert [u.reserve("tick") for _ in range(3)] == ["ok", "ok", "minute"]
    clock.t += timedelta(seconds=61)
    assert u.reserve("tick") == "ok"
    clock.t += timedelta(seconds=61)
    assert u.reserve("tick") == "day"               # three used today
    # the quota day follows Pacific time: 09:00 UTC on 1 Nov is 02:00 on 1 Nov in Los Angeles; 08:00 UTC next day is still 1 Nov
    clock.t = datetime(2026, 11, 2, 7, 59, tzinfo=timezone.utc)
    assert u.reserve("tick") == "day"
    clock.t = datetime(2026, 11, 2, 9, 0, tzinfo=timezone.utc)
    assert u.reserve("tick") == "ok"                # a new Pacific day
    assert u.today()["tick"]["used_today"] == 1


class FakeGemini(GeminiGM):
    def __init__(self, usage, fail=None):
        super().__init__(usage=usage)
        self.sent = []
        self.fail = fail

    def _generate(self, model, level, system, user):
        self.sent.append((model, level))
        if self.fail and model == config.GEMINI_MODEL_TICK:
            raise self.fail
        return "{}"


def test_models_and_thinking_level_are_configured():
    assert config.GEMINI_MODEL_TICK == "gemini-3.8-flash" and config.GEMINI_MODEL_LIGHT == "gemini-3.5-flash-lite"
    assert config.GEMINI_THINKING_LEVEL == "medium" and config.GEMINI_THINKING_LEVEL_TICK == "medium"


def test_strong_model_for_ticks_light_for_the_rest():
    store, clock = MemoryStore(), Clock()
    g = FakeGemini(usage(store, clock))
    g.call("s", "u", tier="tick")
    assert g.sent[-1] == (config.GEMINI_MODEL_TICK, "medium") and g.last["degraded"] is None
    g.call("s", "u")
    assert g.sent[-1] == (config.GEMINI_MODEL_LIGHT, "medium")


def test_falls_back_to_light_when_the_strong_daily_quota_is_gone(monkeypatch):
    monkeypatch.setitem(config.GEMINI_LIMITS, "tick", {"rpd": 1, "rpm": 4})
    store, clock = MemoryStore(), Clock()
    g = FakeGemini(usage(store, clock))
    g.call("s", "u", tier="tick")
    clock.t += timedelta(seconds=61)
    g.call("s", "u", tier="tick")
    assert g.sent[-1][0] == config.GEMINI_MODEL_LIGHT and "quota" in g.last["degraded"]


def test_falls_back_to_light_when_the_strong_model_errors():
    store, clock = MemoryStore(), Clock()
    g = FakeGemini(usage(store, clock), fail=RuntimeError("429 RESOURCE_EXHAUSTED"))
    g.call("s", "u", tier="tick")
    assert [m for m, _ in g.sent] == [config.GEMINI_MODEL_TICK, config.GEMINI_MODEL_LIGHT] and g.last["degraded"]
    g2 = FakeGemini(usage(store, clock), fail=ValueError("bad request: invalid schema"))
    with pytest.raises(ValueError):                 # a real bug is not hidden by the fallback
        g2.call("s", "u", tier="tick")


def test_strong_per_minute_limit_defers_instead_of_degrading(monkeypatch):
    monkeypatch.setitem(config.GEMINI_LIMITS, "tick", {"rpd": 18, "rpm": 1})
    store, clock = MemoryStore(), Clock()
    g = FakeGemini(usage(store, clock))
    g.call("s", "u", tier="tick")
    with pytest.raises(GMBusy):
        g.call("s", "u", tier="tick")
    assert len(g.sent) == 1


def test_light_waits_a_little_then_gives_up(monkeypatch):
    monkeypatch.setitem(config.GEMINI_LIMITS, "light", {"rpd": 450, "rpm": 1})
    store, clock = MemoryStore(), Clock()
    g = FakeGemini(usage(store, clock))
    g.call("s", "u")
    with pytest.raises(GMBusy):                     # the minute does not clear within the short wait
        g.call("s", "u")
    monkeypatch.setitem(config.GEMINI_LIMITS, "light", {"rpd": 1, "rpm": 9})
    clock.t += timedelta(days=1)
    g.call("s", "u")
    with pytest.raises(GMBusy) as e:
        g.call("s", "u")
    assert "daily" in str(e.value)


def test_a_deferred_tick_stays_open_and_is_retried(world):
    eng, store, gm, clock = world
    gid, cid = start_solo(eng)
    real = gm.call
    state = {"busy": True}

    def call(system, user, tier="light"):
        if state["busy"] and tier == "tick":
            raise GMBusy("the strong AI Master model is at its per-minute limit")
        return real(system, user, tier)
    gm.call = call
    out = eng.resolve_tick(gid)
    assert out["resolved"] is False and "per-minute" in out["reason"]
    g, _ = store.get("game", gid)
    assert next(t for t in g["ticks"] if t["n"] == g["clock"]["tick"])["status"] == "open"
    state["busy"] = False
    assert eng.resolve_tick(gid)["resolved"] is True


def test_light_quota_error_reaches_the_player_as_a_plain_message(world):
    eng, store, gm, clock = world
    gid, cid = start_solo(eng)
    gm.call = lambda *a, **k: (_ for _ in ()).throw(GMBusy("the AI Master is busy right now (request quota). Please try again in a few minutes"))
    with pytest.raises(EngineError) as e:
        eng.submit_action("p_jorge", gid, "free_query", "hello", cid)
    assert "busy" in str(e.value)
