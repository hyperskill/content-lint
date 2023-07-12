from __future__ import annotations

import re
from typing import TYPE_CHECKING

from apps.steps.content_testing.helpers import replace

if TYPE_CHECKING:
    from typing import Final

    from content_lint.typing import Replacement, StepData

ZERO_WIDTH_SPACES: Final = re.compile(r'[\ufeff\u200b]', re.IGNORECASE)
SPACES: Final = re.compile(r'[^\S\n\t]|[\u180e]', re.IGNORECASE)

REPLACE: Final[dict[re.Pattern[str], Replacement]] = {
    ZERO_WIDTH_SPACES: '',
    SPACES: ' ',
}


def prepare_text(step: StepData) -> None:
    step['text'] = replace(step['text'], REPLACE)
