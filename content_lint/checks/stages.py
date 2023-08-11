from __future__ import annotations

from typing import cast

from content_lint.constants import BlockName
from content_lint.types import (
    IssueLevel,
    PyCharmStepSource,
    Settings,
    StageData,
    StepBlock,
)


def check_stages(
    block: StepBlock,
    settings: Settings,
    *,
    step_index: int | None = None,
    stage: StageData | None = None,
) -> tuple[tuple[IssueLevel, str], ...]:
    if (
        not stage
        or stage['is_template_based']
        or block['name'] != BlockName.PYCHARM
        or step_index == 1
    ):
        return ()

    source = cast(PyCharmStepSource, block['source'])
    files = source['files']

    if any(file.get('is_visible', True) for file in files):
        return (
            (
                IssueLevel.ERROR,
                f"This step is a stage. This stage's project is not template based. "
                f"Therefore Stage #{step_index} can't have new visible files.",
            ),
        )

    return ()
