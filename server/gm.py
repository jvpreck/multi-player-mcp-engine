"""The AI Master call. Gemini runs at thinking level `medium`. The client is injectable for tests."""
import json
import re

from . import config


class GMError(Exception):
    pass


class GMBusy(Exception):
    """The AI Master cannot be called right now because of a quota. Nothing was sent. Try again later."""


class Usage:
    """Counts requests per tier, per day (provider day, Pacific time) and per minute, in the database, so that all server instances share it."""

    def __init__(self, store, now_fn=None, sleep=None):
        from datetime import datetime, timezone
        self.store = store
        self.now_fn = now_fn or (lambda: datetime.now(timezone.utc))
        self.sleep = sleep or __import__("time").sleep

    def _day(self, now, tier="light"):
        from zoneinfo import ZoneInfo
        return now.astimezone(ZoneInfo(config.QUOTA_TZ.get(tier, config.GEMINI_QUOTA_TZ))).strftime("%Y-%m-%d")

    def reserve(self, tier):
        """'ok' and counts the request, or 'day' (daily quota used up) or 'minute' (too many in the last 60 seconds)."""
        from .db import Conflict
        lim = config.GEMINI_LIMITS[tier]
        for _ in range(4):
            now = self.now_fn()
            t = now.timestamp()
            key = f"{tier}:{self._day(now, tier)}"
            doc, ver = self.store.get("usage", key)
            doc = doc or {"id": key, "tier": tier, "day": self._day(now, tier), "count": 0, "recent": []}
            doc["recent"] = [x for x in doc.get("recent", []) if t - x < 60]
            if doc["count"] >= lim["rpd"]:
                return "day"
            if len(doc["recent"]) >= lim["rpm"]:
                return "minute"
            doc["count"] += 1
            doc["recent"].append(t)
            try:
                self.store.put("usage", key, doc, ver)
                return "ok"
            except Conflict:
                continue
        return "ok"  # heavy contention on the counter: do not block play over bookkeeping

    def reserve_waiting(self, tier):
        """For the light tier: a short wait is fine, a long one is not."""
        waited = 0
        while True:
            r = self.reserve(tier)
            if r != "minute" or waited >= config.LIGHT_MAX_WAIT_SECONDS:
                return r
            self.sleep(2)
            waited += 2

    def today(self):
        out = {}
        for tier in config.GEMINI_LIMITS:
            doc = self.store.get("usage", f"{tier}:{self._day(self.now_fn(), tier)}")[0] or {}
            out[tier] = {"used_today": doc.get("count", 0), "daily_limit": config.GEMINI_LIMITS[tier]["rpd"],
                         "per_minute_limit": config.GEMINI_LIMITS[tier]["rpm"],
                         "model": {"tick": config.GEMINI_MODEL_TICK, "light": config.GEMINI_MODEL_LIGHT, "image": config.IMAGE_MODEL}[tier]}
        return out


class GeminiGM:
    """Routes each request to a tier. `tick` (strong) is used for closing a tick and checking a character; everything else is `light`.
    If the strong model's daily quota is used up, or it fails with a quota or server error, the request goes to the light model and
    `last["degraded"]` says so. If the strong model is only over its per-minute limit, the request is deferred (GMBusy) and the
    scheduler tries again on its next run. If the light model is out of quota, GMBusy tells the player to try later."""

    def __init__(self, api_key=None, usage=None):
        self._client = None
        self._api_key = api_key
        self.usage = usage
        self.last = {}

    def _get(self):
        if self._client is None:
            import os
            from google import genai
            self._client = genai.Client(api_key=self._api_key or os.environ["GEMINI_API_KEY"])
        return self._client

    def _generate(self, model, level, system, user):
        from google.genai import types
        cfg = types.GenerateContentConfig(
            system_instruction=system,
            response_mime_type="application/json",
            thinking_config=types.ThinkingConfig(thinking_level=level),
            http_options=types.HttpOptions(timeout=config.GEMINI_TIMEOUT_SECONDS * 1000),
        )
        return self._get().models.generate_content(model=model, contents=user, config=cfg).text or ""

    @staticmethod
    def _retryable(e):
        m = f"{type(e).__name__} {e}".lower()
        return any(x in m for x in ("429", "resource_exhausted", "quota", "500", "502", "503", "504", "unavailable", "overloaded", "deadline"))

    def call(self, system: str, user: str, tier: str = "light") -> str:
        degraded = None
        if tier == "tick":
            r = self.usage.reserve("tick") if self.usage else "ok"
            if r == "minute":
                raise GMBusy("the strong AI Master model is at its per-minute limit; the tick will be retried shortly")
            if r == "ok":
                try:
                    out = self._generate(config.GEMINI_MODEL_TICK, config.GEMINI_THINKING_LEVEL_TICK, system, user)
                    self.last = {"tier": "tick", "model": config.GEMINI_MODEL_TICK, "degraded": None}
                    return out
                except Exception as e:
                    if not self._retryable(e):
                        raise
                    degraded = "strong model unavailable (" + type(e).__name__ + ")"
            else:
                degraded = "strong model daily quota used up"
        r = (self.usage.reserve_waiting("light") if self.usage else "ok")
        if r != "ok":
            raise GMBusy("the AI Master is busy right now (request quota). Please try again in a few minutes"
                         if r == "minute" else "the AI Master has reached its daily request quota. Please try again tomorrow")
        out = self._generate(config.GEMINI_MODEL_LIGHT, config.GEMINI_THINKING_LEVEL, system, user)
        self.last = {"tier": "light", "model": config.GEMINI_MODEL_LIGHT, "degraded": degraded}
        return out


_FENCE = re.compile(r"^```(?:json)?\s*|\s*```$", re.I)


def parse(text: str) -> dict:
    t = _FENCE.sub("", (text or "").strip())
    try:
        data = json.loads(t)
    except json.JSONDecodeError as e:
        raise GMError(f"GM returned invalid JSON: {e}")
    if not isinstance(data, dict):
        raise GMError("GM response is not an object")
    data.setdefault("status", "ok")
    for k in ("state_changes", "events", "decisions", "messages", "dice_log", "errors", "shared_digest"):
        data.setdefault(k, [])
    data.setdefault("results", {})
    if not isinstance(data["results"], dict):
        raise GMError("results must be an object keyed by recipient")
    return data
