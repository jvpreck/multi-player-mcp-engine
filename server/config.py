"""Environment-driven settings. Nothing here touches the network."""
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GM_DIR = ROOT / "gm"
# Adventures hold secrets, so they are NOT in this public repository. They are read from a private GitHub repository
# with a read-only token. ADVENTURES_DIR (a local folder) overrides that, for development and tests only.
ADVENTURES_REPO = os.environ.get("ADVENTURES_REPO", "jvpreck/rpg_adventures")
ADVENTURES_REF = os.environ.get("ADVENTURES_REF", "main")
ADVENTURES_CACHE_SECONDS = int(os.environ.get("ADVENTURES_CACHE_SECONDS", "300"))
ADVENTURES_DIR = Path(os.environ["ADVENTURES_DIR"]) if os.environ.get("ADVENTURES_DIR") else None
RULESETS_DIR = ROOT / "rulesets"

# Two tiers. "tick" is the strong, scarce model: closing a tick with every player's actions, and checking a character sheet.
# "light" is the fast, plentiful model: everything a single player does between ticks. GEMINI_MODEL is the old name for the light model.
GEMINI_MODEL_TICK = os.environ.get("GEMINI_MODEL_TICK", "gemini-3.8-flash")
GEMINI_MODEL_LIGHT = os.environ.get("GEMINI_MODEL_LIGHT") or os.environ.get("GEMINI_MODEL") or "gemini-3.5-flash-lite"
GEMINI_THINKING_LEVEL = os.environ.get("GEMINI_THINKING_LEVEL", "medium")
GEMINI_THINKING_LEVEL_TICK = os.environ.get("GEMINI_THINKING_LEVEL_TICK", GEMINI_THINKING_LEVEL)
# Free-tier quotas with a little headroom (the provider's figures were 20 per day and 5 per minute, 500 per day and 10 per minute).
GEMINI_LIMITS = {
    "tick": {"rpd": int(os.environ.get("GEMINI_TICK_RPD", "18")), "rpm": int(os.environ.get("GEMINI_TICK_RPM", "4"))},
    "light": {"rpd": int(os.environ.get("GEMINI_LIGHT_RPD", "450")), "rpm": int(os.environ.get("GEMINI_LIGHT_RPM", "9"))},
}
GEMINI_QUOTA_TZ = "America/Los_Angeles"  # provider quotas reset at midnight Pacific
LIGHT_MAX_WAIT_SECONDS = 8
GM_MAX_ATTEMPTS = int(os.environ.get("GM_MAX_ATTEMPTS", "2"))

TABLES = {
    "player": "gm_players",
    "adventure": "gm_adventures",
    "npc": "gm_npcs",
    "location": "gm_locations",
    "game": "gm_games",
    "character": "gm_characters",
    "npc_state": "gm_npc_states",
    "location_state": "gm_location_states",
    "submit_action": "gm_submit_actions",
    "task": "gm_tasks",
    "key": "gm_keys",
    "usage": "gm_usage",
}
TASK_TTL_HOURS = 48
TASK_MAX_ATTEMPTS = 5

BLOCKS = ["Morning", "Afternoon", "Evening", "Night"]
SPAN_BLOCKS = {"day": 4, "block": 1, "beat": 1}
SAY_MAX_CHARS = 500
