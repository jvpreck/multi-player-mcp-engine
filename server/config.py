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
    # images: Cloudflare gives 10,000 Neurons a day. klein 4B costs about 26 per 512 output tile, 5 per input tile: a 1024 picture with
    # references is about 120, a 512 reference about 26. Calls per day are kept low enough for a mix of both.
    "image": {"rpd": int(os.environ.get("IMAGE_RPD", "80")), "rpm": int(os.environ.get("IMAGE_RPM", "10"))},
}
GEMINI_QUOTA_TZ = "America/Los_Angeles"  # provider quotas reset at midnight Pacific
QUOTA_TZ = {"tick": GEMINI_QUOTA_TZ, "light": GEMINI_QUOTA_TZ, "image": "UTC"}  # Cloudflare's free allowance resets at 00:00 UTC

# Illustrations (Cloudflare Workers AI, FLUX.2 klein 4B, which accepts reference images). Needs CLOUDFLARE_ACCOUNT_ID and CLOUDFLARE_API_TOKEN; without them the option is unavailable.
IMAGE_MODEL = os.environ.get("IMAGE_MODEL", "@cf/black-forest-labs/flux-2-klein-4b")
IMAGE_SIZE = int(os.environ.get("IMAGE_SIZE", "1024"))  # every picture shown to players
IMAGE_REF_SIZE = int(os.environ.get("IMAGE_REF_SIZE", "512"))  # reference sheet images, and the largest input the model takes
# Used only for a game that has illustrations on but no style of its own (each game normally gets one, immutable, when it is created).
IMAGE_STYLE = os.environ.get("IMAGE_STYLE", "Atmospheric painterly illustration, muted colours, dramatic light, no text, no letters, no watermark.")
IMAGE_BUCKET = os.environ.get("IMAGE_BUCKET", "gm-images")
IMAGE_URL_TTL_SECONDS = int(os.environ.get("IMAGE_URL_TTL_SECONDS", "900"))
IMAGES_PER_TICK = int(os.environ.get("IMAGES_PER_TICK", "2"))  # most the AI Master may ask for in one response
IMAGES_PER_RUN = int(os.environ.get("IMAGES_PER_RUN", "6"))  # generation calls, a portrait takes four  # most generated per scheduler run, to stay inside the function time
IMAGE_MAX_ATTEMPTS = 2
PORTRAITS_PER_RESPONSE = 3
STYLE_MIN, STYLE_MAX = 40, 700
IMAGE_TIMEOUT_SECONDS = 25
FUNCTION_BUDGET_SECONDS = int(os.environ.get("FUNCTION_BUDGET_SECONDS", "50"))  # Vercel maxDuration is 60
IMAGE_PENDING_DAYS = 3  # a picture not drawn after this long is dropped
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
    "image": "gm_images",
}
TASK_TTL_HOURS = 48
TASK_MAX_ATTEMPTS = 5

BLOCKS = ["Morning", "Afternoon", "Evening", "Night"]
SPAN_BLOCKS = {"day": 4, "block": 1, "beat": 1}
SAY_MAX_CHARS = 500
