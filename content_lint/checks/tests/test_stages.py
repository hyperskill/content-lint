from __future__ import annotations

from content_lint.checks.stages import check_stages
from content_lint.types import (
    CodeStepOptions,
    IssueLevel,
    PyCharmStepOptions,
    Settings,
    StageData,
    StepData,
)


def test_stage_without_template_based_project(settings: Settings) -> None:
    step = StepData(
        name='pycharm',
        step_index=2,
        text='Some text',
        options=PyCharmStepOptions(
            files=[{'name': 'src/Main.java', 'is_visible': True}],
        ),
        stage=StageData(is_template_based=False),
    )

    issues = check_stages(step, settings)

    assert len(issues) == 1
    assert issues[0][0] == IssueLevel.ERROR
    assert issues[0][1].startswith('This step is a stage.')


def test_stage_with_template_based_project(settings: Settings) -> None:
    step_data = StepData(
        name='pycharm',
        step_index=2,
        text='Some text',
        options=CodeStepOptions(
            code_templates={},
        ),
        stage=StageData(is_template_based=True),
    )

    issues = check_stages(step_data, settings)

    assert len(issues) == 0
