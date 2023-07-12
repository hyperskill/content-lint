from __future__ import annotations

import re
from collections.abc import Callable

Replacement = str | Callable[[re.Match[str]], str]


def replace(text: str, replace_map: dict[re.Pattern[str], Replacement]) -> str:
    for pattern, replacement in replace_map.items():
        text = pattern.sub(replacement, text)

    return text
