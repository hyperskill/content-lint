from __future__ import annotations

import re
from collections.abc import Callable
from enum import StrEnum, unique
from typing import NotRequired, TypedDict

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


class StepData(TypedDict):
    name: str
    text: str
    step_index: int
    options: CodeStepOptions | list[
        ChoiceStepOption
    ] | TextStepOptions | PyCharmStepOptions
    stage: NotRequired[StageData]


StepTransformer = Callable[[StepData, Settings], None]
StepHtmlTransformer = Callable[[BeautifulSoup, Settings], None]
StepChecker = Callable[[StepData, Settings], tuple[tuple[IssueLevel, str], ...]]
ToCogniterraTransformer = Callable[[StepData, Settings], None]
