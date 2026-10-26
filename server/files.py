"""Loads the gm/, rulesets/ and adventures/ markdown files and their front matter."""
import re
from functools import lru_cache
from pathlib import Path

import yaml

from . import config

_FM = re.compile(r"\A---\n(.*?)\n---\n", re.S)


def split_front_matter(text: str):
    m = _FM.match(text)
    if not m:
        return {}, text
    meta = yaml.safe_load(m.group(1)) or {}
    return meta, text[m.end():]


@lru_cache(maxsize=None)
def read(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


def _list(directory: Path):
    out = {}
    if not directory.exists():
        return out
    for p in sorted(directory.glob("*.md")):
        meta, body = split_front_matter(read(str(p)))
        if not meta.get("id"):
            continue
        meta = dict(meta)
        meta["file"] = f"{directory.name}/{p.name}"
        out[meta["id"]] = {"meta": meta, "body": body, "path": str(p)}
    return out


def rulesets():
    return _list(config.RULESETS_DIR)


def adventure_files():
    return _list(config.ADVENTURES_DIR)


def gm_file(name: str) -> str:
    return read(str(config.GM_DIR / name))


def adventure_record_from_file(entry: dict) -> dict:
    m = entry["meta"]
    return {
        "id": m["id"], "title": m.get("title", m["id"]), "source": "file",
        "file": m["file"], "content": None, "ruleset_id": m.get("ruleset"),
        "generation": m.get("generation", "supplied"), "era": m.get("era"),
        "players": m.get("players", {"min": 1, "max": 5}),
        "recommended": m.get("recommended", {}),
        "pace_options": m.get("pace_options", []), "language": m.get("language", "en"),
        "summary": m.get("summary", ""), "seed": None, "owner_player_id": None,
        "pregenerated": m.get("pregenerated", []),
    }
