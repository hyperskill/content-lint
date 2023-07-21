from __future__ import annotations

import pytest
from transform.to_cogniterra.alerts import prepare_alerts_for_cogniterra

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
def test_prepare_alerts_to_stepik_format(text: str, result: str) -> None:
    prepare_alerts_for_cogniterra(text)
    assert text == result
