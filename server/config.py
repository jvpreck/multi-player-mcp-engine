"""Environment-driven settings. Nothing here touches the network."""
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GM_DIR = ROOT / "gm"
ADVENTURES_DIR = ROOT / "adventures"
RULESETS_DIR = ROOT / "rulesets"

GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-3.5-flash-lite")
GEMINI_THINKING_LEVEL = os.environ.get("GEMINI_THINKING_LEVEL", "medium")
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
}
TASK_TTL_HOURS = 48
TASK_MAX_ATTEMPTS = 5

BLOCKS = ["Morning", "Afternoon", "Evening", "Night"]
SPAN_BLOCKS = {"day": 4, "block": 1, "beat": 1}
SAY_MAX_CHARS = 500
