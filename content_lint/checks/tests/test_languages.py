from __future__ import annotations

from content_lint.checks.languages import check_languages
from content_lint.constants import BlockName
from content_lint.types import (
    CodeStepOptions,
    CodeStepSource,
    IssueLevel,
    Settings,
    StepBlock,
)


def test_code_step_without_code_templates(settings: Settings) -> None:
    step = StepBlock(
        name=BlockName.CODE,
        text='Some text',
        options=CodeStepOptions(code_templates={}),
        source=CodeStepSource(code=''),  # TODO: Add templates to source
    )

    issues = check_languages(step, settings)

    assert len(issues) == 1
    assert issues[0][0] == IssueLevel.ERROR
    assert issues[0][1] == 'Step block should have at least one code template language'


def test_code_step_more_than_one_code_templates(settings: Settings) -> None:
    step = StepBlock(
        name=BlockName.CODE,
        text='Some text',
        options=CodeStepOptions(
            code_templates={'go': 'go code', 'java17': 'java17 code'}
        ),
        source=CodeStepSource(code=''),  # TODO: Add templates to source
    )

    issues = check_languages(step, settings)

    assert len(issues) == 0


def test_code_step_not_supported_language(settings: Settings) -> None:
    step = StepBlock(
        name=BlockName.CODE,
        text='Some text',
        options=CodeStepOptions(code_templates={'python2': 'python2 code'}),
        source=CodeStepSource(code=''),  # TODO: Add templates to source
    )

    issues = check_languages(step, settings)

    assert len(issues) == 1
    assert issues[0][0] == IssueLevel.ERROR
    assert issues[0][1].startswith('Language "python2" is not supported.')


def test_code_step_few_not_supported_languages(settings: Settings) -> None:
    step = StepBlock(
        name=BlockName.CODE,
        text='Some text',
        options=CodeStepOptions(
            code_templates={'python2': 'python2 code', 'rust': 'rust code'}
        ),
        source=CodeStepSource(code=''),  # TODO: Add templates to source
    )

    issues = check_languages(step, settings)

    assert len(issues) == 1
    assert issues[0][0] == IssueLevel.ERROR
    assert issues[0][1].startswith(
        'Languages "python2", "rust" contain unsupported languages.'
    )


def test_code_step_supported_language(settings: Settings) -> None:
    step = StepBlock(
        name=BlockName.CODE,
        text='Some text',
        options=CodeStepOptions(code_templates={'python3': 'python3 code'}),
        source=CodeStepSource(code=''),  # TODO: Add templates to source
    )

    issues = check_languages(step, settings)

    assert len(issues) == 0


def test_code_step_contains_supported_and_unsupported_language(
    settings: Settings,
) -> None:
    step_data = StepBlock(
        name='code',
        text='Step text',
        options=CodeStepOptions(  # TODO: Don't use options
            code_templates={
                'python3': 'python3 code',
                'python2': 'python2 code',
            }
        ),
        source=CodeStepSource(code=''),  # TODO: Add templates to source
    )

    issues = check_languages(step_data, settings)

    assert len(issues) == 1
    assert issues[0][0] == IssueLevel.ERROR
    assert issues[0][1].startswith(
        'Languages "python3", "python2" contain unsupported languages.'
    )
