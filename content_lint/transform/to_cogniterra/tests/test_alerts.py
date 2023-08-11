from __future__ import annotations

import pytest

from content_lint.constants import BlockName
from content_lint.transform.to_cogniterra.alerts import prepare_alerts_for_cogniterra
from content_lint.types import Settings, StepBlock

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
    ('result', 'text'),
    [
        *test_cases_for_prepare_alerts,
        (
            '<div> class="alert alert-primary">Some text</div>',
            '<div> class="alert alert-primary">Some text</div>',
        ),
    ],
)
def test_prepare_alerts_to_stepik_format(
    text: str, result: str, settings: Settings
) -> None:
    step = StepBlock(name=BlockName.TEXT, text=text, source=None)
    prepare_alerts_for_cogniterra(step, settings)

    assert step['text'] == result
