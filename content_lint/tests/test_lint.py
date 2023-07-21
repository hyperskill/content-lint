from __future__ import annotations

from content_lint.lint import check_step_text
from content_lint.types import IssueLevel, StageData, StepData, StepOptions


def test_step_no_critical_issues() -> None:
    step_data = StepData(
        name='pycharm',
        text='Step text',
        step_index=2,
        options=StepOptions(code_templates={}),
        stage=StageData(is_template_based=False),
    )

    issues = check_step_text(step_data)

    assert len(issues) == 1
    assert any(issue[0] == IssueLevel.ERROR for issue in issues) is False


def test_step_has_critical_issues() -> None:
    step_data = StepData(
        name='code',
        text='Step text',
        step_index=2,
        options=StepOptions(code_templates={}),
        stage=StageData(is_template_based=False),
    )

    issues = check_step_text(step_data)

    assert len(issues) == 1
    assert any(issue[0] == IssueLevel.ERROR for issue in issues) is True
