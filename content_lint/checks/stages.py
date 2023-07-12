from __future__ import annotations

from content_lint.constants import PYCHARM_BLOCK_NAME
from content_lint.typing import IssueLevel, StepData


def check_stages(step: StepData) -> tuple[tuple[IssueLevel, str], ...]:
    if (
        not step['stage']
        or step['stage']['is_template_based']
        or step['block_name'] != PYCHARM_BLOCK_NAME
        or step['step_index'] == 1
    ):
        return ()

    files = step['files']

    if any(file.get('is_visible', True) for file in files):
        return (
            (
                IssueLevel.ERROR,
                f"This step is a stage. This stage's project is not template based. "
                f"Therefore Stage #{step['step_index']} can't have new visible files.",
            ),
        )

    return ()
