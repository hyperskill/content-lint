from __future__ import annotations

from typing import Final, TYPE_CHECKING

from bs4 import BeautifulSoup

from content_lint.checks.checkers import hyphen_checker, simple_checker
from content_lint.checks.languages import check_languages
from content_lint.checks.meta import check_meta_tags
from content_lint.checks.stages import check_stages
from content_lint.transform.html.code import prepare_code_sections
from content_lint.transform.html.headers import prepare_headers
from content_lint.transform.html.images import prepare_images
from content_lint.transform.html.links import prepare_links
from content_lint.transform.plain_text.alerts import (
    prepare_alerts,
)
from content_lint.transform.plain_text.meta import prepare_meta
from content_lint.transform.plain_text.text import prepare_text
from content_lint.transform.plain_text.video import (
    prepare_video,
)
from content_lint.transform.to_cogniterra.alerts import prepare_alerts_for_cogniterra
from content_lint.transform.to_cogniterra.video import prepare_video_for_cogniterra

if TYPE_CHECKING:
    from content_lint.typing import (
        IssueLevel,
        StepChecker,
        StepData,
        StepHtmlTransformer,
        StepTransformer,
        ToCogniterraTransformer,
    )

PLAIN_TEXT_OPERATIONS: Final[tuple[StepTransformer, ...]] = (
    prepare_meta,
    prepare_text,
    prepare_alerts,
    prepare_video,
)

HTML_OPERATIONS: Final[tuple[StepHtmlTransformer, ...]] = (
    prepare_headers,
    prepare_links,
    prepare_code_sections,
    prepare_images,
)


def fix_step_text(step: StepData) -> None:
    for plain_text_operation in PLAIN_TEXT_OPERATIONS:
        plain_text_operation(step)

    bs = BeautifulSoup(step['text'], 'lxml')

    for html_operation in HTML_OPERATIONS:
        html_operation(bs)

    if (body := bs.body) is None:
        return

    step['text'] = ''.join(map(str, body.contents))


def check_step_text(step: StepData) -> list[tuple[IssueLevel, str]]:
    checkers: tuple[StepChecker, ...] = (
        check_meta_tags,
        simple_checker,
        hyphen_checker,
        check_stages,
        check_languages,
    )

    all_issues: list[tuple[IssueLevel, str]] = []

    for checker in checkers:
        issues = checker(step)
        all_issues.extend(issues)

    return all_issues


def lint(step: StepData) -> list[tuple[IssueLevel, str]]:
    fix_step_text(step)
    return check_step_text(step)


TO_COGNITERRA_TRANSFORMERS: tuple[ToCogniterraTransformer, ...] = (
    prepare_alerts_for_cogniterra,
    prepare_video_for_cogniterra,
)


def transform_for_cogniterra(step: StepData) -> None:
    for operation in TO_COGNITERRA_TRANSFORMERS:
        operation(step)
