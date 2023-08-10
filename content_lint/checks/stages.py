from __future__ import annotations

from typing import cast

from content_lint.constants import BlockName
from content_lint.types import IssueLevel, PyCharmStepOptions, Settings, StepData


def check_stages(
    step: StepData, settings: Settings
) -> tuple[tuple[IssueLevel, str], ...]:
    if (
        not step['stage']
        or step['stage']['is_template_based']
        or step['name'] != BlockName.PYCHARM
        or step['step_index'] == 1
    ):
        return ()

    options = cast(PyCharmStepOptions, step['options'])
    files = options['files']

    if any(file.get('is_visible', True) for file in files):
        return (
            (
                IssueLevel.ERROR,
                f"This step is a stage. This stage's project is not template based. "
                f"Therefore Stage #{step['step_index']} can't have new visible files.",
            ),
        )

    return ()
