from __future__ import annotations

from typing import TYPE_CHECKING

from content_lint.helpers import slugify

if TYPE_CHECKING:
    from bs4 import BeautifulSoup


def prepare_headers(bs: BeautifulSoup) -> None:
    headers = bs.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'h8', 'h9'])
    for header in headers:
        for tag in header.find_all(['b', 'strong']):
            tag.replaceWith(tag.text)

        for tag in header.find_all(['ol', 'ul']):
            tag.replaceWith('')

        header_id = slugify(header.text)
        header['id'] = header_id

        if header.name != 'h1':
            header.name = 'h5'

        if not header.text.strip():
            header.replaceWith('')
            continue
