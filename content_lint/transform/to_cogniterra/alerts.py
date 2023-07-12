from __future__ import annotations

import re
from typing import Final, TYPE_CHECKING

from content_lint.helpers import replace

if TYPE_CHECKING:
    from content_lint.typing import Replacement, StepData

ALERT_TAGS: Final = r'[ALERT-\g<1>]\g<2>[/ALERT]'
HTML_DIV_ALERT_TAGS_REGEX: Final = re.compile(
    r'<div class="alert alert-(.*?)">([\s\S]*?)</div>', re.IGNORECASE
)

REPLACE_TO_COGNITERRA_FORMAT: Final[dict[re.Pattern[str], Replacement]] = {
    HTML_DIV_ALERT_TAGS_REGEX: ALERT_TAGS,
}


def prepare_alerts_for_cogniterra(step: StepData) -> None:
    step['text'] = replace(step['text'], REPLACE_TO_COGNITERRA_FORMAT)