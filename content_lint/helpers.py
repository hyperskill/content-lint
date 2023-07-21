from __future__ import annotations

import re
import unicodedata
from collections.abc import Callable

Replacement = str | Callable[[re.Match[str]], str]


def replace(text: str, replace_map: dict[re.Pattern[str], Replacement]) -> str:
    for pattern, replacement in replace_map.items():
        text = pattern.sub(replacement, text)

    return text


def slugify(value: str, allow_unicode: bool = False) -> str:
    """Convert to ASCII if 'allow_unicode' is False.

    Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = (
            unicodedata.normalize('NFKD', value)
            .encode('ascii', 'ignore')
            .decode('ascii')
        )
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')
