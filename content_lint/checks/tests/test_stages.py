from __future__ import annotations

from content_lint.checks.stages import check_stages
from content_lint.types import (
    CodeStepOptions,
    CodeStepSource,
    IssueLevel,
    PyCharmStepSource,
    Settings,
    StageData,
    StepBlock,
)


def test_stage_without_template_based_project(settings: Settings) -> None:
    step = StepBlock(
        name='pycharm',
        text='Some text',
        source=PyCharmStepSource(
            files=[{'name': 'src/Main.java', 'text': '//', 'is_visible': True}],
        ),
    )

    issues = check_stages(
        step, settings, step_index=2, stage=StageData(is_template_based=False)
    )

    assert len(issues) == 1
    assert issues[0][0] == IssueLevel.ERROR
    assert issues[0][1].startswith('This step is a stage.')


def test_stage_with_template_based_project(settings: Settings) -> None:
    step_data = StepBlock(
        name='pycharm',
        text='Some text',
        options=CodeStepOptions(
            code_templates={},
        ),
        source=CodeStepSource(code=''),  # TODO: Add templates to source
    )

    issues = check_stages(
        step_data, settings, step_index=2, stage=StageData(is_template_based=True)
    )

    assert len(issues) == 0
