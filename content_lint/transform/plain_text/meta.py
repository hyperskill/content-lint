from __future__ import annotations

import re
from typing import TYPE_CHECKING

from content_lint.helpers import replace

if TYPE_CHECKING:
    from typing import Final

    from content_lint.types import Replacement, Settings, StageData, StepBlock

PRE_META_TAGS_REGEX: Final = re.compile(
    r'\s*(?:<\w+>)?(?:\[(PRE|META)])+[\s\S]*?(?:\[/(PRE|META)])+(?:</\w+>)?\s*',
    re.IGNORECASE,
)

REPLACE: Final[dict[re.Pattern[str], Replacement]] = {PRE_META_TAGS_REGEX: ''}


def prepare_meta(
    block: StepBlock,
    settings: Settings,
    *,
    step_index: int | None = None,
    stage: StageData | None = None,
) -> None:
    block['text'] = replace(block['text'], REPLACE)
