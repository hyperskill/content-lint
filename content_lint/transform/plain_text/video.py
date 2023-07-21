from __future__ import annotations

import re
from typing import TYPE_CHECKING

from content_lint.helpers import replace

if TYPE_CHECKING:
    from typing import Final

    from content_lint.types import Replacement, StepData

VIDEO_TAGS_REGEX: Final = re.compile(r'\[video(.*?)]([\s\S]*?)\[/video]', re.IGNORECASE)
HTML_VIDEO_TAGS: Final = r'<video\g<1>>\g<2></video>'
SOURCE_TAGS_REGEX: Final = re.compile(r'\[source(.*?)]', re.IGNORECASE)
HTML_SOURCE_TAGS: Final = r'<source\g<1>>'

REPLACE_TO_HYPERSKILL_FORMAT: Final[dict[re.Pattern[str], Replacement]] = {
    VIDEO_TAGS_REGEX: HTML_VIDEO_TAGS,
    SOURCE_TAGS_REGEX: HTML_SOURCE_TAGS,
}


def prepare_video(step: StepData) -> None:
    step['text'] = replace(step['text'], REPLACE_TO_HYPERSKILL_FORMAT)
