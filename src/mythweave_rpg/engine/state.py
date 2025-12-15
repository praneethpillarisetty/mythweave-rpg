from __future__ import annotations

from typing import Any, Dict, Optional


class GameState:
    def __init__(self):
        self.pack: Optional[Dict[str, Any]] = None
        self.scene_index: Dict[str, Dict[str, Any]] = {}
        self.current_scene_id: Optional[str] = None

    def load_pack(self, pack: Dict[str, Any]) -> None:
        self.pack = pack
        self.scene_index = {s["id"]: s for s in pack.get("scenes", [])}
        self.current_scene_id = pack.get("startSceneId") or (
            pack["scenes"][0]["id"] if pack.get("scenes") else None
        )

    def current_scene(self) -> Optional[Dict[str, Any]]:
        if not self.current_scene_id:
            return None
        return self.scene_index.get(self.current_scene_id)

    def goto_scene(self, scene_id: str) -> None:
        if scene_id in self.scene_index:
            self.current_scene_id = scene_id
