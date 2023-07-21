from __future__ import annotations

from bs4 import BeautifulSoup

from content_lint.transform.html.code import prepare_code_sections


def test_prepare_code_sections_when_has_language() -> None:
    text = """<code class="language-no-highlight">code1</code>
        <code class="language-kotlin">code2</code>
        <code>code3</code>"""

    expected = """<html><body><code class="language-no-highlight">code1</code>
<code class="language-kotlin">code2</code>
<code class="language-kotlin">code3</code></body></html>"""

    bs = BeautifulSoup(text, 'lxml')

    prepare_code_sections(bs)

    assert str(bs) == expected


def test_prepare_code_sections_when_no_language() -> None:
    text = """<code class="language-no-highlight">code1</code>
        <code>code2</code>"""

    expected = """<html><body><code class="language-no-highlight">code1</code>
<code class="java">code2</code></body></html>"""

    bs = BeautifulSoup(text, 'lxml')

    prepare_code_sections(bs)

    assert str(bs) == expected


def test_prepare_code_sections_remove_data_highlight_only() -> None:
    text = '<code data-highlight-only="true">code1</code>'

    expected = '<html><body><code class="java">code1</code></body></html>'

    bs = BeautifulSoup(text, 'lxml')
    prepare_code_sections(bs)

    assert str(bs) == expected
