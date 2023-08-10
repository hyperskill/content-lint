from __future__ import annotations

from content_lint.constants import BlockName
from content_lint.transform.plain_text.video import prepare_video
from content_lint.types import Settings, StepBlock, TextStepOptions


def test_load_video_from_stepik(settings: Settings) -> None:
    block = StepBlock(
        name=BlockName.TEXT,
        text="""
    [video width="320" height="240" controls]
      [source src="movie.mp4" type="video/mp4"]
      [source src="movie.ogg" type="video/ogg"]
      Your browser does not support the video tag.
    [/video]
    """,
        options=TextStepOptions(),
    )

    prepare_video(block, settings)

    assert (
        block['text']
        == """
    <video width="320" height="240" controls>
      <source src="movie.mp4" type="video/mp4">
      <source src="movie.ogg" type="video/ogg">
      Your browser does not support the video tag.
    </video>
    """
    )
