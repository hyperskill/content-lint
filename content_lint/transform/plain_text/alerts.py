from __future__ import annotations

import re
from typing import TYPE_CHECKING

from content_lint.helpers import replace

if TYPE_CHECKING:
    from typing import Final

    from content_lint.types import Replacement, Settings, StepData

ALERT_TAGS_REGEX: Final = re.compile(
    r'\[ALERT-(.*?)]([\s\S]*?)\[/ALERT]', re.IGNORECASE
)
HTML_DIV_ALERT_TAGS: Final = r'<div class="alert alert-\g<1>">\g<2></div>'

REPLACE_TO_HYPERSKILL_FORMAT: Final[dict[re.Pattern[str], Replacement]] = {
    ALERT_TAGS_REGEX: HTML_DIV_ALERT_TAGS,
}


def prepare_alerts(step: StepData, settings: Settings) -> None:
    step['text'] = replace(step['text'], REPLACE_TO_HYPERSKILL_FORMAT)
