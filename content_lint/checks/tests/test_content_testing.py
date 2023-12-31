from __future__ import annotations

import pytest

from content_lint.constants import BlockName
from content_lint.transform.plain_text.text import clear_text_from_title
from content_lint.types import Settings, StepBlock


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
def test_clear_text_from_title(
    stepik_text: str, hyperskill_text: str, settings: Settings
) -> None:
    step = StepBlock(name=BlockName.TEXT, text=stepik_text, source=None)

    clear_text_from_title(step, settings, step_index=1)

    assert hyperskill_text == step['text']
