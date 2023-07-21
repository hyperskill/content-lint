from __future__ import annotations

from content_lint.checks.checkers import hyphen_checker, simple_checker
from content_lint.types import IssueLevel, StepData


def test_hyphen() -> None:
    step = StepFactory()

    step.step_block.block = {'text': 'Some - text'}
    step.step_block.save(update_fields=['block'])

    issues = hyphen_checker(step)

    assert len(issues) == 1
    assert issues[0][0] == IssueLevel.WARNING
    assert issues[0][1] == (
        'Ln 1, Col 5 (Global Pos 5): '
        'Hyphen ( - ) instead of a dash (–).'  # noqa: RUF001
    )


def test_hyphen_inside_formula() -> None:
    step = StepFactory()

    step.step_block.block = {
        'text': 'm - 1 some text \n'
        '<span class="math-tex">(n - 1)</span> some text k - 1'
    }
    step.step_block.save(update_fields=['block'])

    issues = hyphen_checker(step)

    assert len(issues) == 2
    assert issues[0][0] == IssueLevel.WARNING
    assert issues[0][1] == (
        'Ln 1, Col 2 (Global Pos 2): '
        'Hyphen ( - ) instead of a dash (–).'  # noqa: RUF001
    )

    assert issues[1][0] == IssueLevel.WARNING
    assert issues[1][1] == (
        'Ln 2, Col 50 (Global Pos 67): '
        'Hyphen ( - ) instead of a dash (–).'  # noqa: RUF001
    )


def test_doubled_hyphen() -> None:
    step_data = StepData(name='code', text='Some -- text')

    issues = hyphen_checker(step_data)

    assert len(issues) == 1
    assert issues[0][0] == IssueLevel.WARNING
    assert issues[0][1] == (
        'Ln 1, Col 5 (Global Pos 5): '
        'Hyphen ( -- ) instead of a dash (–).'  # noqa: RUF001
    )


def test_cyrillic_letters_has_not_cyrillic() -> None:
    step = StepFactory()

    step.step_block.block = {'text': 'Some text'}
    step.step_block.save(update_fields=['block'])

    issues = simple_checker(step)

    assert not issues


def test_cyrillic_letters_has_cyrillic() -> None:
    step = StepFactory()

    step.step_block.block = {'text': 'Hello wоrld'}  # noqa: RUF001
    step.step_block.save(update_fields=['block'])

    issues = simple_checker(step)

    assert len(issues) == 1
    assert issues[0][0] == IssueLevel.WARNING
    assert issues[0][1] == (
        'Ln 1, Col 8 (Global Pos 8): '
        'Unexpected cyrillic letter(s): "о".'  # noqa: RUF001
    )


def test_unusual_quotes() -> None:
    step = StepFactory()

    step.step_block.block = {'text': 'Some ‘quoted text’'}  # noqa: RUF001
    step.step_block.save(update_fields=['block'])

    issues = simple_checker(step)

    assert len(issues) == 2
    assert issues[0][0] == IssueLevel.WARNING
    assert issues[0][1] == (
        'Ln 1, Col 6 (Global Pos 6): Unusual quote(s) (‘) '  # noqa: RUF001
        'instead of normal ones (\' or ").'
    )
    assert issues[1][0] == IssueLevel.WARNING
    assert issues[1][1] == (
        'Ln 1, Col 18 (Global Pos 18): Unusual quote(s) (’) '  # noqa: RUF001
        'instead of normal ones (\' or ").'
    )


def test_unusual_doubled_quotes() -> None:
    step = StepFactory()

    step.step_block.block = {'text': 'Some “quoted text”'}
    step.step_block.save(update_fields=['block'])

    issues = simple_checker(step)

    assert len(issues) == 2
    assert issues[0][0] == IssueLevel.WARNING
    assert issues[0][1] == (
        'Ln 1, Col 6 (Global Pos 6): '
        'Unusual quote(s) (“) instead of normal ones (\' or ").'
    )
    assert issues[1][0] == IssueLevel.WARNING
    assert issues[1][1] == (
        'Ln 1, Col 18 (Global Pos 18): '
        'Unusual quote(s) (”) instead of normal ones (\' or ").'
    )
