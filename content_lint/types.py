from __future__ import annotations

import re
from collections.abc import Callable
from enum import StrEnum, unique
from typing import NotRequired, TypedDict

from bs4 import BeautifulSoup

Replacement = str | Callable[[re.Match[str]], str]


@unique
class IssueLevel(StrEnum):
    __slots__ = ()

    WARNING = 'warning'
    ERROR = 'error'


class FileData(TypedDict):
    is_visible: bool


class StageData(TypedDict):
    is_template_based: bool


class StepOptions(TypedDict):
    code_templates: dict[str, str]
    files: NotRequired[list[FileData]]
    language: NotRequired[str]


class ChoiceStepOption(TypedDict):
    text: str
    is_correct: bool
    feedback: str


class StepData(TypedDict):
    name: str
    text: str
    step_index: int
    options: StepOptions | list[ChoiceStepOption]
    stage: NotRequired[StageData]


StepTransformer = Callable[[StepData], None]
StepHtmlTransformer = Callable[[BeautifulSoup], None]
StepChecker = Callable[[StepData], tuple[tuple[IssueLevel, str], ...]]
ToCogniterraTransformer = Callable[[StepData], None]
