from __future__ import annotations

import re
from typing import TYPE_CHECKING

from content_lint.helpers import replace

if TYPE_CHECKING:
    from typing import Final

    from content_lint.typing import Replacement, StepData

PRE_META_TAGS_REGEX: Final = re.compile(
    r'\s*(?:<\w+>)?(?:\[(PRE|META)])+[\s\S]*?(?:\[/(PRE|META)])+(?:</\w+>)?\s*',
    re.IGNORECASE,
)

REPLACE: Final[dict[re.Pattern[str], Replacement]] = {PRE_META_TAGS_REGEX: ''}


def prepare_meta(step: StepData) -> None:
    step['text'] = replace(step['text'], REPLACE)
