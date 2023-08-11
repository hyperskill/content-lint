from __future__ import annotations

import re
from typing import cast

from content_lint.constants import BlockName
from content_lint.types import ChoiceStepOption, Settings, StageData, StepBlock

PATTERN = re.compile(r"[a-zA-Z0-9!@#$%^&*()_+-={}\[\]|\\:;\"\'<>,?/~`]")


def remove_dots_in_the_string(text: str) -> str:
    if text.endswith('.....'):
        return text
    if text.endswith('....'):
        return text[:-1]
    if text.endswith('...'):
        return text
    if text.endswith('..'):
        return text[:-1]
    if text == '.' or text.endswith(r'\.'):
        return text
    if PATTERN.search(text) and text[-1] == '.':
        return text[:-1]
    return text


def remove_dots(
    block: StepBlock,
    settings: Settings,
    *,
    step_index: int | None = None,
    stage: StageData | None = None,
) -> None:
    if block['name'] != BlockName.CHOICE:
        return

    options = cast(list[ChoiceStepOption], block['options'])

    for option in options:
        if isinstance(option, dict) and 'text' in option:
            option['text'] = remove_dots_in_the_string(option['text'])
