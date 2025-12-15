from __future__ import annotations

import json
from typing import Any, Dict, List, Optional
import importlib.resources as ir

from .pack_schema import validate_pack

_PACKS_DIR = "packs"


def list_packs() -> List[Dict[str, str]]:
    """
    Returns a list of {id, title} from all *.json files in packs/.
    Uses importlib.resources so it works when packaged.
    """
    base = ir.files("mythweave_rpg").joinpath(_PACKS_DIR)

    packs: List[Dict[str, str]] = []
    try:
        for entry in base.iterdir():
            if entry.is_file() and entry.name.endswith(".json"):
                try:
                    data = json.loads(entry.read_text(encoding="utf-8"))
                    meta = data.get("meta", {})
                    pack_id = meta.get("id") or entry.stem
                    title = meta.get("title") or entry.stem
                    packs.append({"id": pack_id, "title": title, "filename": entry.name})
                except Exception:
                    continue
    except Exception:
        return []

    packs.sort(key=lambda p: p["title"].lower())
    return packs


def load_pack(pack_id: str) -> Optional[Dict[str, Any]]:
    """
    Load a pack by scanning packs/ and matching meta.id.
    """
    base = ir.files("mythweave_rpg").joinpath(_PACKS_DIR)

    try:
        for entry in base.iterdir():
            if not (entry.is_file() and entry.name.endswith(".json")):
                continue
            data = json.loads(entry.read_text(encoding="utf-8"))
            meta = data.get("meta", {})
            if (meta.get("id") or entry.stem) == pack_id:
                validate_pack(data)
                return data
    except Exception:
        return None

    return None
