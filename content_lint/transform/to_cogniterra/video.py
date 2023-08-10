from __future__ import annotations

import re
from typing import Final, TYPE_CHECKING

from content_lint.helpers import replace, Replacement

if TYPE_CHECKING:
    from content_lint.types import Settings, StepData

HTML_VIDEO_ALERT_TAGS_REGEX: Final = re.compile(
    r'<video(.*?)>([\s\S]*?)</video>', re.IGNORECASE
)
VIDEO_TAGS: Final = r'[video\g<1>]\g<2>[/video]'
HTML_SOURCE_ALERT_TAGS_REGEX: Final = re.compile(r'<source(.*?)>', re.IGNORECASE)
SOURCE_TAGS: Final = r'[source\g<1>]'

REPLACE_TO_STEPIK_FORMAT: Final[dict[re.Pattern[str], Replacement]] = {
    HTML_VIDEO_ALERT_TAGS_REGEX: VIDEO_TAGS,
    HTML_SOURCE_ALERT_TAGS_REGEX: SOURCE_TAGS,
}


def prepare_video_for_cogniterra(step: StepData, settings: Settings) -> None:
    step['text'] = replace(step['text'], REPLACE_TO_STEPIK_FORMAT)
