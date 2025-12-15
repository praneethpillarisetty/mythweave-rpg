from __future__ import annotations

import random
import re
from typing import Dict, List

_DICE_RE = re.compile(r"^\s*(\d*)\s*[dD]\s*(\d+)\s*([+-]\s*\d+)?\s*$")


def roll_formula(formula: str) -> Dict[str, object]:
    """
    Supports:
      - 1d20+3
      - 2d6+1
      - d20 (same as 1d20)
      - 3D8-2
    """
    m = _DICE_RE.match(formula)
    if not m:
        raise ValueError("Expected NdM(+/-K), e.g. 1d20+3 or 2d6-1")

    n_str, sides_str, mod_str = m.group(1), m.group(2), m.group(3)
    n = int(n_str) if n_str else 1
    sides = int(sides_str)

    if n <= 0:
        raise ValueError("Number of dice must be >= 1")
    if sides <= 1:
        raise ValueError("Sides must be >= 2")

    modifier = 0
    if mod_str:
        modifier = int(mod_str.replace(" ", ""))

    rolls: List[int] = [random.randint(1, sides) for _ in range(n)]
    total = sum(rolls) + modifier

    return {
        "formula": f"{n}d{sides}{modifier:+d}" if modifier else f"{n}d{sides}",
        "rolls": rolls,
        "modifier": modifier,
        "total": total,
    }
