from __future__ import annotations

from checks.meta import check_meta_tags

from content_lint.types import IssueLevel


def test_meta_tag() -> None:
    step = StepFactory()

    step.step_block.block = {'raw_text': '[pre][/pre]'}
    step.step_block.save(update_fields=['block'])

    issues = check_meta_tags(step)

    assert len(issues) == 0


def test_unexpected_closing_meta_tag() -> None:
    step = StepFactory()

    step.step_block.block = {'raw_text': '[meta][/meta][/pre]'}
    step.step_block.save(update_fields=['block'])

    issues = check_meta_tags(step)

    assert len(issues) == 1
    assert issues[0][0] == IssueLevel.ERROR
    assert issues[0][1] == 'Unexpected closing tag `[/pre]`:14'


def test_two_unexpected_closing_meta_tag() -> None:
    step = StepFactory()

    step.step_block.block = {'raw_text': '[/pre][/meta]'}
    step.step_block.save(update_fields=['block'])

    issues = check_meta_tags(step)

    assert len(issues) == 2
    assert issues[0][0] == IssueLevel.ERROR
    assert issues[0][1] == 'Unexpected closing tag `[/pre]`:1'
    assert issues[1][0] == IssueLevel.ERROR
    assert issues[1][1] == 'Unexpected closing tag `[/meta]`:7'


def test_wrong_closing_meta_tag() -> None:
    step = StepFactory()

    step.step_block.block = {'raw_text': '[pre][/meta]'}
    step.step_block.save(update_fields=['block'])

    issues = check_meta_tags(step)

    assert len(issues) == 1
    assert issues[0][0] == IssueLevel.ERROR
    assert issues[0][1] == 'Expected `[/pre]`, but got `[/meta]`:6'


def test_unclosing_meta_tag() -> None:
    step = StepFactory()

    step.step_block.block = {'raw_text': '[pre][/pre][alert-warning]'}
    step.step_block.save(update_fields=['block'])

    issues = check_meta_tags(step)

    assert len(issues) == 1
    assert issues[0][0] == IssueLevel.ERROR
    assert issues[0][1] == 'Unclosed tag `[alert]`:12'


def test_unclosing_meta_tag_2() -> None:
    step = StepFactory()

    step.step_block.block = {'raw_text': '[pre][meta][/meta]'}
    step.step_block.save(update_fields=['block'])

    issues = check_meta_tags(step)

    assert len(issues) == 1
    assert issues[0][0] == IssueLevel.ERROR
    assert issues[0][1] == 'Expected `[/pre]`, but got `[meta]`:6'
