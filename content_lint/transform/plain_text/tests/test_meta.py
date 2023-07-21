from __future__ import annotations

from content_lint.transform.plain_text.meta import prepare_meta


def test_prepare_meta() -> None:
    text = """<p>Prerequisites:</p>
        <p>Some text</p>"""

    same_text = prepare_meta(text)
    assert same_text == text


def test_prepare_meta_when_has_text() -> None:
    text = """<p>[PRE]</p>

        <p>Prerequisites:</p>

        <ul>
            <li>topic1</li>
            <li>topic2</li>
        </ul>

        <p>[/PRE]</p>

        <p>Some text</p>"""

    text = prepare_meta(text)
    assert text == '<p>Some text</p>'

    text = """<p>Some text 1</p>
        <p>[META]</p>
        <p>Additional info</p>
        <p>[/META]</p>
        <p>Some texts 2</p>"""

    text = prepare_meta(text)
    assert text == '<p>Some text 1</p><p>Some texts 2</p>'
