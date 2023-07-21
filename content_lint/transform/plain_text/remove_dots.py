import re
from content_lint.typing import StepData

PATTERN = re.compile(r"[a-zA-Z0-9!@#$%^&*()_+-=\{\}\[\]|\\:;\"\'<>,?/~`]")


def remove_dots_in_the_string(text: str) -> str:
    if text.endswith("....."):
        return text
    if text.endswith("...."):
        return text[:-1]
    if text.endswith("..."):
        return text
    if text.endswith(".."):
        return text[:-1]
    if text == '.' or text.endswith("\."):
        return text
    if PATTERN.search(text) and text[-1] == '.':
        return text[:-1]
    return text


def remove_dots(step_block: StepData) -> None:
    try:
        options = step_block['options']
    except:
        return

    for option in options:
        result = remove_dots_in_the_string(option['text'])
        option['text'] = result
