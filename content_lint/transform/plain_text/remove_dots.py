from __future__ import annotations

import re
from typing import cast

from constants import CHOICE_BLOCK_NAME

from content_lint.types import ChoiceStepOption, StepData

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
    if text == '.' or text.endswith('.'):
        return text
    if PATTERN.search(text) and text[-1] == '.':
        return text[:-1]
    return text


def remove_dots(step_block: StepData) -> None:
    if step_block['name'] != CHOICE_BLOCK_NAME:
        return

    options = cast(list[ChoiceStepOption], step_block['options'])

    for option in options:
        option['text'] = remove_dots_in_the_string(option['text'])
