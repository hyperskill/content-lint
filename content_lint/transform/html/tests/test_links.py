from __future__ import annotations

from bs4 import BeautifulSoup

from content_lint.transform.html.links import prepare_links


def test_prepare_links() -> None:
    text = '<a href="https://somelink.com" rel="nofollow">Wikipedia</a>'
    bs = BeautifulSoup(text, 'lxml')

    prepare_links(bs)

    assert str(bs) == (
        '<html><body><a '
        'href="https://somelink.com" '
        'rel="nofollow" '
        'target="_blank">Wikipedia</a></body></html>'
    )
    bs = BeautifulSoup(text, 'lxml')

    prepare_links(bs)

    assert str(bs) == (
        '<html><body><a '
        'href="https://somelink.com" '
        'rel="nofollow" '
        'target="_blank">Wikipedia</a></body></html>'
    )
