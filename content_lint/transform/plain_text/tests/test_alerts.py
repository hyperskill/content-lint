from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from content_lint.constants import BlockName
from content_lint.transform.plain_text.alerts import prepare_alerts
from content_lint.types import StepBlock, TextStepOptions

if TYPE_CHECKING:
    from content_lint.types import Settings

test_cases_for_prepare_alerts = {
    (
        '[ALERT-primary]Some text[/ALERT]',
        '<div class="alert alert-primary">Some text</div>',
    ),
    (
        '<p>[ALERT-warning]<strong>Important</strong> text.[/ALERT]</p>',
        '<p><div class="alert alert-warning">'
        '<strong>Important</strong> text.</div></p>',
    ),
    (
        '[ALERT-primary]Some\ntext[/ALERT]',
        '<div class="alert alert-primary">Some\ntext</div>',
    ),
}


@pytest.mark.parametrize(
    ('text', 'result'),
    [
        *test_cases_for_prepare_alerts,
        ('[]ALERT-primary[]Some text[/ALERT]', '[]ALERT-primary[]Some text[/ALERT]'),
    ],
)
def test_prepare_alerts_to_hyperskill_format(
    text: str, result: str, settings: Settings
) -> None:
    step = StepBlock(name=BlockName.TEXT, text=text, options=TextStepOptions())

    prepare_alerts(step, settings, step_index=1)

    assert step['text'] == result
