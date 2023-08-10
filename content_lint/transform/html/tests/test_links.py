from __future__ import annotations

from typing import TYPE_CHECKING

from bs4 import BeautifulSoup

from content_lint.transform.html.links import prepare_links

if TYPE_CHECKING:
    from content_lint.types import Settings


def test_prepare_links(settings: Settings) -> None:
    text = '<a href="https://somelink.com" rel="nofollow">Wikipedia</a>'
    bs = BeautifulSoup(text, 'lxml')

    prepare_links(bs, settings)

    assert str(bs) == (
        '<html><body><a '
        'href="https://somelink.com" '
        'rel="nofollow" '
        'target="_blank">Wikipedia</a></body></html>'
    )
    bs = BeautifulSoup(text, 'lxml')

    prepare_links(bs, settings)

    assert str(bs) == (
        '<html><body><a '
        'href="https://somelink.com" '
        'rel="nofollow" '
        'target="_blank">Wikipedia</a></body></html>'
    )
