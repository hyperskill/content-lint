from __future__ import annotations

import re
from typing import TYPE_CHECKING

from content_lint.checks.checkers import IssueLevel

if TYPE_CHECKING:
    from typing import Final

    from content_lint.typing import StepData

TAG_PATTERN: Final = re.compile(r'\[(/?)(pre|meta|alert)[^]]*]', re.IGNORECASE)


def check_meta_tags(step: StepData) -> tuple[tuple[IssueLevel, str], ...]:
    issues = []
    current_tag: str | None = None
    current_tag_position = 0

    for match in TAG_PATTERN.finditer(step['text']):
        is_closed, tag_name = match.groups()
        if is_closed:
            if not current_tag:
                issues.append(
                    (
                        IssueLevel.ERROR,
                        f'Unexpected closing tag `[/{tag_name}]`:{match.start() + 1}',
                    )
                )
            elif current_tag != tag_name:
                issues.append(
                    (
                        IssueLevel.ERROR,
                        f'Expected `[/{current_tag}]`, '
                        f'but got `[/{tag_name}]`:{match.start() + 1}',
                    )
                )
        elif current_tag:
            issues.append(
                (
                    IssueLevel.ERROR,
                    f'Expected `[/{current_tag}]`, '
                    f'but got `[{tag_name}]`:{match.start() + 1}',
                )
            )

        current_tag = None if is_closed else tag_name
        current_tag_position = match.start() + 1

    if current_tag:
        issues.append(
            (IssueLevel.ERROR, f'Unclosed tag `[{current_tag}]`:{current_tag_position}')
        )

    return tuple(issues)
