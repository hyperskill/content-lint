from __future__ import annotations

from types import IssueLevel, StageData, StepData, StepOptions

from checks.stages import check_stages


def test_stage_without_template_based_project() -> None:
    step_data = StepData(
        name='pycharm',
        step_index=2,
        text='Some text',
        options=StepOptions(
            code_templates={},
        ),
        stage=StageData(is_template_based=False),
    )

    issues = check_stages(step_data)

    assert len(issues) == 1
    assert issues[0][0] == IssueLevel.ERROR
    assert issues[0][1].startswith('This step is a stage.')


def test_stage_with_template_based_project() -> None:
    step_data = StepData(
        name='pycharm',
        step_index=2,
        text='Some text',
        options=StepOptions(
            code_templates={},
        ),
        stage=StageData(is_template_based=True),
    )

    issues = check_stages(step_data)

    assert len(issues) == 0
