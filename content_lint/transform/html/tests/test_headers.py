from __future__ import annotations

from bs4 import BeautifulSoup

from content_lint.transform.html.headers import prepare_headers


def test_remove_bold_text() -> None:
    text = (
        'prefix <h1> before bold <b>Some text</b> after bold</h1><b>'
        'Bold outside header</b><h1><strong>'
        'Strong inside header </strong></h1>'
    )
    bs = BeautifulSoup(text, 'lxml')

    prepare_headers(bs)

    assert str(bs) == (
        '<html><body><p>prefix </p><h1 id="before-bold-some-text-after-bold"> '
        'before bold Some text after bold</h1>'
        '<b>Bold outside header</b>'
        '<h1 id="strong-inside-header">Strong inside header </h1></body></html>'
    )


def test_replace_secondary_header() -> None:
    text = '<h2>some text</h2>'
    bs = BeautifulSoup(text, 'lxml')

    prepare_headers(bs)

    assert str(bs) == '<html><body><h5 id="some-text">some text</h5></body></html>'


def test_replace_secondary_header_7() -> None:
    text = '<h7>some text</h7>'
    bs = BeautifulSoup(text, 'lxml')

    prepare_headers(bs)

    assert str(bs) == '<html><body><h5 id="some-text">some text</h5></body></html>'


def test_add_header_id() -> None:
    text = '<h1>some text</h1>'
    bs = BeautifulSoup(text, 'lxml')

    prepare_headers(bs)

    assert str(bs) == '<html><body><h1 id="some-text">some text</h1></body></html>'


def test_fix_doubled_header_id() -> None:
    text = '<h1 id="some-text" id="some-text">some text</h1>'
    bs = BeautifulSoup(text, 'lxml')

    prepare_headers(bs)

    assert str(bs) == '<html><body><h1 id="some-text">some text</h1></body></html>'


def test_replace_exist_header_id() -> None:
    text = '<h1 id="custom-header-id">some text</h1>'
    bs = BeautifulSoup(text, 'lxml')

    prepare_headers(bs)

    assert str(bs) == '<html><body><h1 id="some-text">some text</h1></body></html>'


def test_replace_marked_list_inside_header() -> None:
    text = '<h2>some text<ol><li> item </li></ol><ul><li> item </li></ul></h2>'
    bs = BeautifulSoup(text, 'lxml')

    prepare_headers(bs)

    assert str(bs) == '<html><body><h5 id="some-text">some text</h5></body></html>'


def test_remove_empty_headers() -> None:
    text = '<H1></H1><H1>header</H1><h2></h2>'
    bs = BeautifulSoup(text, 'lxml')

    prepare_headers(bs)

    assert str(bs) == '<html><body><h1 id="header">header</h1></body></html>'
