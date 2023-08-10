from __future__ import annotations

import re
from collections.abc import Callable
from enum import StrEnum, unique
from typing import NotRequired, Protocol, TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    from bs4 import BeautifulSoup

Replacement = str | Callable[[re.Match[str]], str]


class Settings(TypedDict):
    supported_code_templates_languages: set[str]


@unique
class IssueLevel(StrEnum):
    __slots__ = ()

    WARNING = 'warning'
    ERROR = 'error'


class FileData(TypedDict):
    name: str
    is_visible: bool


class StageData(TypedDict):
    is_template_based: bool


class CodeStepOptions(TypedDict):
    code_templates: dict[str, str]


class PyCharmStepOptions(TypedDict):
    files: NotRequired[list[FileData]]
    language: NotRequired[str]


class ChoiceStepOption(TypedDict):
    text: str
    is_correct: bool
    feedback: str


class TextStepOptions(TypedDict):
    pass


class StepBlock(TypedDict):
    name: str
    text: str
    options: CodeStepOptions | list[
        ChoiceStepOption
    ] | TextStepOptions | PyCharmStepOptions


class StepTransformer(Protocol):
    def __call__(
        self,
        block: StepBlock,
        settings: Settings,
        *,
        step_index: int | None = None,
        stage: StageData | None = None,
    ) -> None:
        """Make step block transformations."""
        ...


class StepChecker(Protocol):
    def __call__(
        self,
        block: StepBlock,
        settings: Settings,
        *,
        step_index: int | None = None,
        stage: StageData | None = None,
    ) -> tuple[tuple[IssueLevel, str], ...]:
        """Check step block."""
        ...


class StepHtmlTransformer(Protocol):
    def __call__(self, bs: BeautifulSoup, settings: Settings) -> None:
        """Make step block transformations."""
        ...


class ToCogniterraTransformer(Protocol):
    def __call__(self, block: StepBlock, settings: Settings) -> None:
        """Make step block transformations to cogniterra format."""
        ...
