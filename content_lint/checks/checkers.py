from __future__ import annotations

import re
from typing import TYPE_CHECKING, TypedDict

from content_lint.types import IssueLevel, Settings, StepData

if TYPE_CHECKING:
    from re import Match
    from typing import Final


class CheckResult(TypedDict):
    level: IssueLevel
    message: str


CHECK_BY_PATTERN: Final[dict[re.Pattern[str], CheckResult]] = {
    re.compile(r'[а-яё]+', re.IGNORECASE | re.UNICODE): {  # noqa: RUF001
        'level': IssueLevel.WARNING,
        'message': 'Ln {line}, Col {column} (Global Pos {position}): '
        'Unexpected cyrillic letter(s): "{match[0]}".',
    },
    re.compile(r'[‘’“”]+', re.IGNORECASE | re.UNICODE): {  # noqa: RUF001
        'level': IssueLevel.WARNING,
        'message': 'Ln {line}, Col {column} (Global Pos {position}): '
        'Unusual quote(s) ({match[0]}) instead of '
        'normal ones (\' or ").',
    },
    re.compile(r'<a.*?>([\s\S]{0,9})</a>', re.IGNORECASE | re.UNICODE): {
        'level': IssueLevel.WARNING,
        'message': 'Ln {line}, Col {column} (Global Pos {position}): '
        'Link (href) with the length less than 10 ({match[1]}).',
    },
}


def _position_by_match(text: str, match: Match[str]) -> tuple[int, ...]:
    start = match.start()
    line = text.count('\n', 0, start) + 1
    column = start - text.rfind('\n', 0, start)
    position = start + 1
    return line, column, position


def simple_checker(
    step: StepData, settings: Settings
) -> tuple[tuple[IssueLevel, str], ...]:
    issues: list[tuple[IssueLevel, str]] = []
    text = step['text']

    for pattern, options in CHECK_BY_PATTERN.items():
        iterator = pattern.finditer(text)

        for match in iterator:
            line, column, position = _position_by_match(text, match)
            issues.append(
                (
                    options['level'],
                    options['message'].format(
                        line=line, column=column, position=position, match=match
                    ),
                )
            )

    return tuple(issues)


FORMULA_PATTERN: Final = re.compile(
    r'<span class="math-tex">.*</span>', re.IGNORECASE | re.UNICODE
)
HYPHEN_PATTERN: Final = re.compile(r' --? ', re.IGNORECASE | re.UNICODE)


def hyphen_checker(
    step: StepData, settings: Settings
) -> tuple[tuple[IssueLevel, str], ...]:
    text = step['text']
    iterator = FORMULA_PATTERN.finditer(text)
    formulas_indexes = {match.span() for match in iterator}

    iterator = HYPHEN_PATTERN.finditer(text)
    issues = []
    for match in iterator:
        if any(
            indexes[0] <= match.start() < indexes[1] for indexes in formulas_indexes
        ):
            continue

        line, column, position = _position_by_match(text, match)
        issues.append(
            (
                IssueLevel.WARNING,
                f'Ln {line}, Col {column} (Global Pos {position}): '
                f'Hyphen ({match[0]}) instead of a dash (–).',  # noqa: RUF001
            )
        )

    return tuple(issues)
