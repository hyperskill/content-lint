from __future__ import annotations

from content_lint.lint import check_step_text
from content_lint.types import (
    CodeStepOptions,
    IssueLevel,
    PyCharmStepOptions,
    Settings,
    StageData,
    StepBlock,
)


def test_step_no_critical_issues(settings: Settings) -> None:
    step_data = StepBlock(
        name='pycharm',
        text='Step text',
        options=PyCharmStepOptions(files=[]),
    )

    issues = check_step_text(
        step_data, settings, step_index=2, stage=StageData(is_template_based=False)
    )

    assert len(issues) == 0
    assert any(issue[0] == IssueLevel.ERROR for issue in issues) is False


def test_step_has_critical_issues(settings: Settings) -> None:
    block = StepBlock(
        name='code',
        text='Step text',
        options=CodeStepOptions(code_templates={}),
    )

    issues = check_step_text(
        block, step_index=2, stage=StageData(is_template_based=False), settings=settings
    )

    assert len(issues) == 1
    assert any(issue[0] == IssueLevel.ERROR for issue in issues) is True
