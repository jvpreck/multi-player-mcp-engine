"""The AI Master call. Gemini runs at thinking level `medium`. The client is injectable for tests."""
import json
import re

from . import config


class GMError(Exception):
    pass


class GeminiGM:
    def __init__(self, api_key=None):
        self._client = None
        self._api_key = api_key

    def _get(self):
        if self._client is None:
            import os
            from google import genai
            self._client = genai.Client(api_key=self._api_key or os.environ["GEMINI_API_KEY"])
        return self._client

    def call(self, system: str, user: str) -> str:
        from google.genai import types
        cfg = types.GenerateContentConfig(
            system_instruction=system,
            response_mime_type="application/json",
            thinking_config=types.ThinkingConfig(thinking_level=config.GEMINI_THINKING_LEVEL),
        )
        r = self._get().models.generate_content(model=config.GEMINI_MODEL, contents=user, config=cfg)
        return r.text or ""


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
