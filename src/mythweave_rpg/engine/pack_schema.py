from __future__ import annotations

from typing import Any, Dict


def _require(obj: Dict[str, Any], key: str, typ):
    if key not in obj:
        raise ValueError(f"Missing required key: {key}")
    if not isinstance(obj[key], typ):
        raise ValueError(f"Key '{key}' must be {typ.__name__}")
    return obj[key]


def validate_pack(pack: Dict[str, Any]) -> None:
    if not isinstance(pack, dict):
        raise ValueError("Pack must be a JSON object.")

    meta = _require(pack, "meta", dict)
    _require(meta, "packVersion", int)
    _require(meta, "id", str)
    _require(meta, "title", str)
    _require(meta, "description", str)

    scenes = _require(pack, "scenes", list)
    if not scenes:
        raise ValueError("Pack must contain at least 1 scene.")

    scene_ids = set()
    for s in scenes:
        if not isinstance(s, dict):
            raise ValueError("Each scene must be an object.")
        sid = _require(s, "id", str)
        scene_ids.add(sid)
        _require(s, "title", str)
        _require(s, "text", str)

        choices = s.get("choices", [])
        if not isinstance(choices, list):
            raise ValueError(f"Scene {sid}: choices must be a list.")

        for c in choices:
            if not isinstance(c, dict):
                raise ValueError(f"Scene {sid}: choice must be an object.")
            _require(c, "label", str)
            if "nextSceneId" in c and c["nextSceneId"] is not None and not isinstance(c["nextSceneId"], str):
                raise ValueError(f"Scene {sid}: nextSceneId must be a string or null.")

    start_scene = pack.get("startSceneId") or scenes[0].get("id")
    if start_scene not in scene_ids:
        raise ValueError("startSceneId does not exist in scenes.")
