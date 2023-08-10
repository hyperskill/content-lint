from __future__ import annotations

import pytest

from content_lint.constants import BlockName
from content_lint.transform.plain_text.text import prepare_text
from content_lint.types import CodeStepOptions, Settings, StepData, TextStepOptions


@pytest.mark.parametrize(
    ('stepik_text', 'hyperskill_text'),
    [
        (
            """
<h1><b>Json</b></h1>
Sometimes, we need to send some data from the server to the client in JSON form.

<code class="language-json">
{
  "field_name": "volume",
  "value": 100
}
</code>
<h2>Using</h2>
Example:
<code>
{
  "header": "Something"
}
</code>

<a href="https://wikiperdia.org">More info</a>
""",
            """
<h1><b>Json</b></h1>
Sometimes, we need to send some data from the server to the client in JSON form.

<code class="language-json">
{
  "field_name": "volume",
  "value": 100
}
</code>
<h2>Using</h2>
Example:
<code>
{
  "header": "Something"
}
</code>

<a href="https://wikiperdia.org">More info</a>
""",
        )
    ],
)
def test_prepare_text(
    stepik_text: str, hyperskill_text: str, settings: Settings
) -> None:
    step_data = StepData(
        name='code',
        text=stepik_text,
        step_index=1,
        options=CodeStepOptions(code_templates={}),
    )
    prepare_text(step_data, settings)

    assert hyperskill_text == step_data['text']

    # repeat prepare

    prepare_text(step_data, settings)

    assert hyperskill_text == step_data['text']


def test_clean_zero_width_spaces(settings: Settings) -> None:
    step = StepData(
        name=BlockName.TEXT,
        text='t\ufeffe\u200bxt',
        step_index=1,
        options=TextStepOptions(),
    )

    prepare_text(step, settings)

    assert step['text'] == 'text'


def test_clean_spaces(settings: Settings) -> None:
    step = StepData(
        name=BlockName.TEXT,
        text='t\u00a0e\u1680x\u180et\u2000t\u2001e\u2002 \u2003t\u2004e\u2005'
        '\t\u2006\u2007text\u2008\u2009_\u200a\n\u2028\u2029\u202f\u205fx\u3000',
        step_index=1,
        options=TextStepOptions(),
    )

    prepare_text(step, settings)

    assert step['text'] == 't e x t t e   t e \t  text  _ \n    x '
