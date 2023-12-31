from __future__ import annotations

from typing import cast, TYPE_CHECKING

from content_lint.checks.checkers import IssueLevel
from content_lint.constants import BlockName
from content_lint.types import CodeStepOptions, StageData

if TYPE_CHECKING:
    from content_lint.types import Settings, StepBlock


def check_languages(
    block: StepBlock,
    settings: Settings,
    *,
    step_index: int | None = None,
    stage: StageData | None = None,
) -> tuple[tuple[IssueLevel, str], ...]:
    if block['name'] != BlockName.CODE:
        return ()

    options = cast(CodeStepOptions, block['options'])
    code_templates = options.get('code_templates')
    if not code_templates:
        return (
            (
                IssueLevel.ERROR,
                'Step block should have at least one code template language',
            ),
        )

    supported_code_templates_languages = settings['supported_code_templates_languages']

    if not all(
        language in supported_code_templates_languages for language in code_templates
    ):
        more_than_one_lang = len(code_templates) > 1
        languages = [f'"{lang}"' for lang in code_templates]
        message = (
            'contain unsupported languages'
            if more_than_one_lang
            else 'is not supported'
        )
        return (
            (
                IssueLevel.ERROR,
                f'Language{"s" if more_than_one_lang else ""} {", ".join(languages)} '
                f'{message}. '
                f'Supported languages: {", ".join(supported_code_templates_languages)}',
            ),
        )

    return ()
