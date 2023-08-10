from __future__ import annotations

from typing import Final, TYPE_CHECKING

from bs4 import BeautifulSoup

from content_lint.checks.checkers import hyphen_checker, simple_checker
from content_lint.checks.languages import check_languages
from content_lint.checks.stages import check_stages
from content_lint.transform.html.code import prepare_code_sections
from content_lint.transform.html.headers import prepare_headers
from content_lint.transform.html.images import prepare_images
from content_lint.transform.html.links import prepare_links
from content_lint.transform.plain_text.alerts import (
    prepare_alerts,
)
from content_lint.transform.plain_text.meta import prepare_meta
from content_lint.transform.plain_text.remove_dots import remove_dots
from content_lint.transform.plain_text.text import clear_text_from_title, prepare_text
from content_lint.transform.plain_text.video import (
    prepare_video,
)
from content_lint.transform.to_cogniterra.alerts import prepare_alerts_for_cogniterra
from content_lint.transform.to_cogniterra.video import prepare_video_for_cogniterra

if TYPE_CHECKING:
    from content_lint.types import (
        IssueLevel,
        Settings,
        StepChecker,
        StepData,
        StepHtmlTransformer,
        StepTransformer,
        ToCogniterraTransformer,
    )

PLAIN_TEXT_FIXERS: Final[tuple[StepTransformer, ...]] = (
    prepare_meta,
    prepare_text,
    clear_text_from_title,
    prepare_alerts,
    prepare_video,
    remove_dots,
)

HTML_FIXERS: Final[tuple[StepHtmlTransformer, ...]] = (
    prepare_headers,
    prepare_links,
    prepare_code_sections,
    prepare_images,
)


def fix_step_text(step: StepData, settings: Settings) -> None:
    for plain_text_operation in PLAIN_TEXT_FIXERS:
        plain_text_operation(step, settings)

    bs = BeautifulSoup(step['text'], 'lxml')

    for html_operation in HTML_FIXERS:
        html_operation(bs, settings)

    if (body := bs.body) is None:
        return

    step['text'] = ''.join(map(str, body.contents))


CHECKERS: tuple[StepChecker, ...] = (
    simple_checker,
    hyphen_checker,
    check_stages,
    check_languages,
)


def check_step_text(step: StepData, settings: Settings) -> list[tuple[IssueLevel, str]]:
    all_issues: list[tuple[IssueLevel, str]] = []

    for checker in CHECKERS:
        issues = checker(step, settings)
        all_issues.extend(issues)

    return all_issues


def lint(step: StepData, settings: Settings) -> list[tuple[IssueLevel, str]]:
    fix_step_text(step, settings)
    return check_step_text(step, settings)


TO_COGNITERRA_TRANSFORMERS: tuple[ToCogniterraTransformer, ...] = (
    prepare_alerts_for_cogniterra,
    prepare_video_for_cogniterra,
)


def transform_for_cogniterra(step: StepData, settings: Settings) -> None:
    for operation in TO_COGNITERRA_TRANSFORMERS:
        operation(step, settings)
