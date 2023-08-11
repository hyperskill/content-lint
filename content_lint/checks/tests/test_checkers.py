from __future__ import annotations

from content_lint.checks.checkers import hyphen_checker, simple_checker
from content_lint.constants import BlockName
from content_lint.types import (
    CodeStepOptions,
    CodeStepSource,
    IssueLevel,
    Settings,
    StepBlock,
)


def test_hyphen(settings: Settings) -> None:
    step = StepBlock(
        name=BlockName.CODE,
        text='Some - text',
        options=CodeStepOptions(code_templates={}),
        source=CodeStepSource(code=''),  # TODO: Add templates to source
    )

    issues = hyphen_checker(step, settings)

    assert len(issues) == 1
    assert issues[0][0] == IssueLevel.WARNING
    assert issues[0][1] == (
        'Ln 1, Col 5 (Global Pos 5): '
        'Hyphen ( - ) instead of a dash (–).'  # noqa: RUF001
    )


def test_hyphen_inside_formula(settings: Settings) -> None:
    step = StepBlock(
        name=BlockName.CODE,
        text='m - 1 some text \n'
        '<span class="math-tex">(n - 1)</span> some text k - 1',
        options=CodeStepOptions(code_templates={}),
        source=CodeStepSource(code=''),  # TODO: Add templates to source
    )

    issues = hyphen_checker(step, settings)

    assert len(issues) == 2  # noqa: PLR2004
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


def test_doubled_hyphen(settings: Settings) -> None:
    step = StepBlock(
        name='code',
        text='Some -- text',
        options=CodeStepOptions(code_templates={}),
        source=CodeStepSource(code=''),  # TODO: Add templates to source
    )

    issues = hyphen_checker(step, settings)

    assert len(issues) == 1
    assert issues[0][0] == IssueLevel.WARNING
    assert issues[0][1] == (
        'Ln 1, Col 5 (Global Pos 5): '
        'Hyphen ( -- ) instead of a dash (–).'  # noqa: RUF001
    )


def test_cyrillic_letters_has_not_cyrillic(settings: Settings) -> None:
    step = StepBlock(
        name='code',
        text='Some text',
        options=CodeStepOptions(code_templates={}),
        source=CodeStepSource(code=''),  # TODO: Add templates to source
    )

    issues = simple_checker(step, settings)

    assert not issues


def test_cyrillic_letters_has_cyrillic(settings: Settings) -> None:
    step = StepBlock(
        name=BlockName.TEXT, text='Hello wоrld', source=None  # noqa: RUF001
    )

    issues = simple_checker(step, settings)

    assert len(issues) == 1
    assert issues[0][0] == IssueLevel.WARNING
    assert issues[0][1] == (
        'Ln 1, Col 8 (Global Pos 8): '
        'Unexpected cyrillic letter(s): "о".'  # noqa: RUF001
    )


def test_unusual_quotes(settings: Settings) -> None:
    step = StepBlock(
        name=BlockName.TEXT,
        text='Some ‘quoted text’',  # noqa: RUF001
        source=None,
    )

    issues = simple_checker(step, settings)

    assert len(issues) == 2  # noqa: PLR2004
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


def test_unusual_doubled_quotes(settings: Settings) -> None:
    step = StepBlock(
        name=BlockName.TEXT,
        text='Some “quoted text”',
        source=None,
    )

    issues = simple_checker(step, settings)

    assert len(issues) == 2  # noqa: PLR2004
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
