from __future__ import annotations

from content_lint.checks.languages import check_languages
from content_lint.types import IssueLevel, StepData, StepOptions


def test_code_step_without_code_templates() -> None:
    step = StepFactory(block_name=BlockName.CODE)

    step.step_block.block = {'options': {'code_templates': {}}}
    step.step_block.save(update_fields=['block'])

    issues = check_languages(step)

    assert len(issues) == 1
    assert issues[0][0] == IssueLevel.ERROR
    assert issues[0][1] == 'Step block should have at least one code template language'


def test_code_step_more_than_one_code_templates() -> None:
    step = StepFactory(block_name=BlockName.CODE)

    step.step_block.block = {
        'options': {'code_templates': {'go': 'go code', 'java17': 'java17 code'}}
    }
    step.step_block.save(update_fields=['block'])

    issues = check_languages(step)

    assert len(issues) == 0


def test_code_step_not_supported_language() -> None:
    step = StepFactory(block_name=BlockName.CODE)

    step.step_block.block = {'options': {'code_templates': {'python2': 'python2 code'}}}
    step.step_block.save(update_fields=['block'])

    issues = check_languages(step)

    assert len(issues) == 1
    assert issues[0][0] == IssueLevel.ERROR
    assert issues[0][1].startswith('Language "python2" is not supported.')


def test_code_step_few_not_supported_languages() -> None:
    step = StepFactory(block_name=BlockName.CODE)
    step.step_block.block = {
        'options': {'code_templates': {'python2': 'python2 code', 'rust': 'rust code'}}
    }
    step.step_block.save(update_fields=['block'])

    issues = check_languages(step)

    assert len(issues) == 1
    assert issues[0][0] == IssueLevel.ERROR
    assert issues[0][1].startswith(
        'Languages "python2", "rust" contain unsupported languages.'
    )


def test_code_step_supported_language() -> None:
    step = StepFactory(block_name=BlockName.CODE)

    step.step_block.block = {'options': {'code_templates': {'python3': 'python3 code'}}}
    step.step_block.save(update_fields=['block'])

    issues = check_languages(step)

    assert len(issues) == 0


def test_code_step_contains_supported_and_unsupported_language() -> None:
    step_data = StepData(
        name='code',
        text='Step text',
        options=StepOptions(
            code_templates={
                'python3': 'python3 code',
                'python2': 'python2 code',
            }
        ),
    )

    issues = check_languages(step_data)

    assert len(issues) == 1
    assert issues[0][0] == IssueLevel.ERROR
    assert issues[0][1].startswith(
        'Languages "python3", "python2" contain unsupported languages.'
    )
