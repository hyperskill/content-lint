from __future__ import annotations

from enum import StrEnum, unique


@unique
class BlockName(StrEnum):
    TEXT = 'text'
    CODE = 'code'
    PYCHARM = 'pycharm'
    CHOICE = 'choice'
