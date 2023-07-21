from __future__ import annotations

import pytest
from transform.plain_text.text import clear_text_from_title


@pytest.mark.parametrize(
    ('stepik_text', 'hyperskill_text'),
    [
        ('<p> <br> [TITLE]some text[/TITLE]<br/> <br>abc</p>', '<p>abc</p>'),
        ('<p>[TITLE]some text[/TITLE]<br/><br />abc</p>', '<p>abc</p>'),
        ('<p> [TITLE]some text[/TITLE]<br/><br />abc</p>', '<p>abc</p>'),
        ('<p><br/> <br />[TITLE]some text[/TITLE] abc</p>', '<p>abc</p>'),
        (
            '<p><br/> <p><br />[TITLE]some text[/TITLE]</p> abc</p>',
            '<p><br/> <p></p> abc</p>',
        ),
    ],
)
def test_clear_text_from_title(stepik_text: str, hyperskill_text: str) -> None:
    actual = clear_text_from_title(stepik_text)

    assert hyperskill_text == actual
