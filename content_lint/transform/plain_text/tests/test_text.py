from __future__ import annotations

import pytest

from content_lint.transform.plain_text.text import prepare_text
from content_lint.types import StepData, StepOptions


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
            """<h1 id="json">Json</h1>
Sometimes, we need to send some data from the server to the client in JSON form.

<code class="language-json">
{
  "field_name": "volume",
  "value": 100
}
</code>
<h5 id="using">Using</h5>
Example:
<code class="language-json">
{
  "header": "Something"
}
</code>
<a href="https://wikiperdia.org" target="_blank">More info</a>
""",
        )
    ],
)
def test_prepare_text(stepik_text: str, hyperskill_text: str) -> None:
    step_data = StepData(
        name='code', text=stepik_text, options=StepOptions(code_templates={})
    )
    prepare_text(step_data)

    assert hyperskill_text == step_data['text']

    # repeat prepare

    prepare_text(step_data)

    assert hyperskill_text == step_data['text']


def test_clean_zero_width_spaces() -> None:
    text = 't\ufeffe\u200bxt'

    same_text = prepare_text(text)
    assert same_text == 'text'


def test_clean_spaces() -> None:
    text = (
        't\u00a0e\u1680x\u180et\u2000t\u2001e\u2002 \u2003t\u2004e\u2005'
        '\t\u2006\u2007text\u2008\u2009_\u200a\n\u2028\u2029\u202f\u205fx\u3000'
    )

    same_text = prepare_text(text)
    assert same_text == 't e x t t e   t e \t  text  _ \n    x '
