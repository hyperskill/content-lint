from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from bs4 import BeautifulSoup

    from content_lint.types import Settings


def prepare_links(bs: BeautifulSoup, settings: Settings) -> None:
    links = bs.find_all('a')
    for link in links:
        link['target'] = '_blank'
