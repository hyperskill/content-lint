from __future__ import annotations

import re
from typing import TYPE_CHECKING

from content_lint.helpers import replace

if TYPE_CHECKING:
    from typing import Final

    from content_lint.types import Replacement, Settings, StageData, StepBlock

ZERO_WIDTH_SPACES: Final = re.compile(r'[\ufeff\u200b]', re.IGNORECASE)
SPACES: Final = re.compile(r'[^\S\n\t]|[\u180e]', re.IGNORECASE)

REPLACE: Final[dict[re.Pattern[str], Replacement]] = {
    ZERO_WIDTH_SPACES: '',
    SPACES: ' ',
}


def prepare_text(
    block: StepBlock,
    settings: Settings,
    *,
    step_index: int | None = None,
    stage: StageData | None = None,
) -> None:
    block['text'] = replace(block['text'], REPLACE)


TITLE_REGEX: Final = re.compile(r'\[TITLE](.+)\[/TITLE]', re.IGNORECASE)
BR_TAGS: Final = r'<br\s*\/?>'
TITLE_WITH_EXTRA_TAGS_REGEX: Final = re.compile(
    rf'(?:\s*{BR_TAGS})*\s*{TITLE_REGEX.pattern}\s*(?:{BR_TAGS}\s*)*', re.IGNORECASE
)


def clear_text_from_title(
    block: StepBlock,
    settings: Settings,
    *,
    step_index: int | None = None,
    stage: StageData | None = None,
) -> None:
    text = block['text']
    match_obj = TITLE_WITH_EXTRA_TAGS_REGEX.search(text)
    if not match_obj:
        return

    start_idx = match_obj.start()
    end_idx = match_obj.end()

    block['text'] = text[:start_idx] + text[end_idx:]
