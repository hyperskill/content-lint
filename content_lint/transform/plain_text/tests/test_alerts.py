from __future__ import annotations

import pytest
from transform.plain_text.alerts import prepare_alerts

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
def test_prepare_alerts_to_hyperskill_format(text: str, result: str) -> None:
    text = prepare_alerts(text)
    assert text == result
