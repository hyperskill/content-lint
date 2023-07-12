from __future__ import annotations

import re
from collections.abc import Callable
from enum import StrEnum, unique
from typing import TypedDict

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


class StepData(TypedDict):
    step_index: int
    block_name: str
    text: str
    code_templates: dict[str, str]
    supported_code_templates_languages: tuple[str]
    files: tuple[FileData, ...]
    stage: StageData | None


StepTransformer = Callable[[StepData], None]
StepHtmlTransformer = Callable[[BeautifulSoup], None]
StepChecker = Callable[[StepData], tuple[tuple[IssueLevel, str], ...]]
ToCogniterraTransformer = Callable[[StepData], None]
