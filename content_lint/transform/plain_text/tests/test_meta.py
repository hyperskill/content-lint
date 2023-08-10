from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from content_lint.constants import BlockName
from content_lint.transform.plain_text.meta import prepare_meta
from content_lint.types import StepData, TextStepOptions

if TYPE_CHECKING:
    from content_lint.types import Settings


@pytest.mark.parametrize(
    ('text', 'expected_text'),
    [
        (
            """<p>Prerequisites:</p>
<p>Some text</p>""",
            """<p>Prerequisites:</p>
<p>Some text</p>""",
        ),
        (
            """<p>[PRE]</p>

<p>Prerequisites:</p>

<ul>
    <li>topic1</li>
    <li>topic2</li>
</ul>

<p>[/PRE]</p>

<p>Some text</p>""",
            '<p>Some text</p>',
        ),
        (
            """<p>Some text 1</p>
<p>[META]</p>
<p>Additional info</p>
<p>[/META]</p>
<p>Some texts 2</p>""",
            '<p>Some text 1</p><p>Some texts 2</p>',
        ),
    ],
)
def test_prepare_meta_when_has_text(
    text: str, expected_text: str, settings: Settings
) -> None:
    step = StepData(
        name=BlockName.TEXT, text=text, step_index=1, options=TextStepOptions()
    )

    prepare_meta(step, settings)
    assert step['text'] == expected_text
