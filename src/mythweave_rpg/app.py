from __future__ import annotations

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

from .engine.pack_loader import list_packs, load_pack
from .engine.state import GameState
from .engine.dice import roll_formula

APP_TITLE = "Mythweave RPG"


class MythweaveApp(toga.App):
    def startup(self):
        self.state = GameState()

        # --- Campaigns tab ---
        self.pack_selector = toga.Selection(
            items=[],
            on_change=self._on_select_pack,
            style=Pack(flex=1),
        )

        self.pack_details = toga.Label(
            "Choose a campaign pack to begin.",
            style=Pack(padding=(10, 0)),
        )

        self.scene_title = toga.Label(
            "—",
            style=Pack(padding=(10, 0), font_weight="bold"),
        )

        self.scene_text = toga.MultilineTextInput(
            readonly=True,
            style=Pack(flex=1, padding=(10, 0)),
        )

        self.choices_box = toga.Box(style=Pack(direction=COLUMN, padding=(10, 0), gap=8))

        campaigns_left = toga.Box(style=Pack(direction=COLUMN, padding=10, gap=10, width=320))
        campaigns_left.add(toga.Label("Campaigns", style=Pack(font_weight="bold")))
        campaigns_left.add(self.pack_selector)
        campaigns_left.add(self.pack_details)

        campaigns_right = toga.Box(style=Pack(direction=COLUMN, padding=10, gap=10))
        campaigns_right.add(self.scene_title)
        campaigns_right.add(self.scene_text)
        campaigns_right.add(toga.Label("Choices", style=Pack(font_weight="bold")))
        campaigns_right.add(self.choices_box)

        campaigns_tab = toga.SplitContainer(
            content=[campaigns_left, campaigns_right],
            style=Pack(flex=1),
        )

        # --- Dice tab ---
        self.dice_formula = toga.TextInput(
            placeholder="e.g. 1d20+3 or 2d6+1",
            style=Pack(flex=1),
        )

        self.dice_result = toga.MultilineTextInput(
            readonly=True,
            style=Pack(flex=1, padding_top=10),
        )

        roll_btn = toga.Button("Roll", on_press=self._on_roll_dice, style=Pack(width=120))

        dice_row = toga.Box(style=Pack(direction=ROW, gap=10))
        dice_row.add(self.dice_formula)
        dice_row.add(roll_btn)

        dice_tab = toga.Box(style=Pack(direction=COLUMN, padding=10))
        dice_tab.add(toga.Label("Dice Roller", style=Pack(font_weight="bold")))
        dice_tab.add(dice_row)
        dice_tab.add(self.dice_result)

        # --- Tabs ---
        self.tabs = toga.OptionContainer(style=Pack(flex=1))
        self.tabs.add("Campaigns", campaigns_tab)
        self.tabs.add("Dice", dice_tab)

        # Window
        self.main_window = toga.MainWindow(title=APP_TITLE)
        self.main_window.content = self.tabs
        self.main_window.show()

        # Load pack list
        self._refresh_pack_list()

    # -------------------------
    # Campaigns
    # -------------------------
    def _refresh_pack_list(self):
        packs = list_packs()
        if not packs:
            self.pack_selector.items = ["(No packs found)"]
            self.pack_selector.enabled = False
            self.pack_details.text = "No campaign packs were found in the app bundle."
            return

        self._pack_index = {p["title"]: p["id"] for p in packs}
        self.pack_selector.items = list(self._pack_index.keys())
        self.pack_selector.enabled = True
        self.pack_details.text = "Select a pack to load its story."

    def _on_select_pack(self, widget):
        if not getattr(self, "_pack_index", None):
            return
        title = self.pack_selector.value
        if not title:
            return

        pack_id = self._pack_index.get(title)
        if not pack_id:
            return

        pack = load_pack(pack_id)
        if pack is None:
            self.pack_details.text = f"Failed to load pack: {pack_id}"
            return

        self.state.load_pack(pack)
        self.pack_details.text = pack["meta"].get("description", "")
        self._render_scene()

    def _render_scene(self):
        scene = self.state.current_scene()
        if not scene:
            self.scene_title.text = "—"
            self.scene_text.value = "No scene loaded."
            self._set_choices([])
            return

        self.scene_title.text = scene.get("title", "Untitled Scene")
        self.scene_text.value = scene.get("text", "")

        choices = scene.get("choices", []) or []
        self._set_choices(choices)

    def _set_choices(self, choices):
        self.choices_box.children.clear()

        if not choices:
            self.choices_box.add(toga.Label("No choices available.", style=Pack()))
            return

        for ch in choices:
            label = ch.get("label", "Continue")
            next_id = ch.get("nextSceneId")

            def _make_handler(next_scene_id):
                def _handler(widget):
                    if next_scene_id:
                        self.state.goto_scene(next_scene_id)
                        self._render_scene()
                return _handler

            btn = toga.Button(label, on_press=_make_handler(next_id), style=Pack(padding=(6, 0)))
            self.choices_box.add(btn)

    # -------------------------
    # Dice
    # -------------------------
    def _on_roll_dice(self, widget):
        formula = (self.dice_formula.value or "").strip()
        if not formula:
            self.dice_result.value = "Enter a dice formula like 1d20+3"
            return

        try:
            result = roll_formula(formula)
        except ValueError as e:
            self.dice_result.value = f"Invalid formula:\n{e}"
            return

        lines = []
        lines.append(f"Formula: {result['formula']}")
        lines.append(f"Rolls:   {', '.join(map(str, result['rolls']))}")
        if result["modifier"] != 0:
            lines.append(f"Mod:     {result['modifier']:+d}")
        lines.append(f"Total:   {result['total']}")
        self.dice_result.value = "\n".join(lines)


def main():
    return MythweaveApp(APP_TITLE)
