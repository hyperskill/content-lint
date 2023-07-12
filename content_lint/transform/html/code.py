from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from bs4 import BeautifulSoup


def prepare_code_sections(bs: BeautifulSoup) -> None:
    codes = bs.find_all('code')
    default_language = 'java'
    for code in codes:
        language = code.attrs.get('class')
        if language and 'language-no-highlight' not in language:
            default_language = language[0]
            break

    for code in codes:
        if 'data-highlight-only' in code.attrs:
            del code.attrs['data-highlight-only']
        code.attrs.setdefault('class', default_language)
