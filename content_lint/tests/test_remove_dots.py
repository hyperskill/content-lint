from __future__ import annotations

import pytest

from content_lint.constants import BlockName
from content_lint.transform.plain_text.remove_dots import (
    remove_dots,
    remove_dots_in_the_string,
)
from content_lint.types import ChoiceStepOption, Settings, StepData


@pytest.mark.parametrize(
    ('text', 'result'),
    [
        ('test.....', 'test.....'),
        ('test....', 'test...'),
        ('test...', 'test...'),
        ('test..', 'test.'),
        ('.', '.'),
        (r'test\.', r'test\.'),
        ('test.', 'test'),
        ('test', 'test'),
        (
            'Compilation error: cannot use [3]int{...} '
            '(type [3]int) as type int in assignment.',
            'Compilation error: cannot use [3]int{...} '
            '(type [3]int) as type int in assignment',
        ),
        (
            'Depending on the programming language, the shapes of blocks change.',
            'Depending on the programming language, the shapes of blocks change',
        ),
        (
            'If the date column is not an index, '
            'we need to run df.set_index(["date"]).',
            'If the date column is not an index, '
            'we need to run df.set_index(["date"])',
        ),
        (
            'Add server.error.include-message=always to application.properties',
            'Add server.error.include-message=always to application.properties',
        ),
        (
            'Because of its approach: running the app - cleaning - running again etc..',
            'Because of its approach: running the app - cleaning - running again etc.',
        ),
        (
            'To explain the meaning of suffixes like SNAPSHOT, M, etc.',
            'To explain the meaning of suffixes like SNAPSHOT, M, etc',
        ),
        ('', ''),
        ('head [OPTION]... [FILE LIST]...', 'head [OPTION]... [FILE LIST]...'),
    ],
)
def test_remove_dots_in_the_string(text: str, result: str) -> None:
    assert remove_dots_in_the_string(text) == result


def test_remove_dots(settings: Settings) -> None:
    step_data = StepData(
        step_index=1,
        name=BlockName.CHOICE,
        text='text',
        options=[
            ChoiceStepOption(text='test.....', feedback='', is_correct=False),
            ChoiceStepOption(text='test....', feedback='', is_correct=True),
            ChoiceStepOption(text='test...', feedback='', is_correct=False),
            ChoiceStepOption(text='test..', feedback='', is_correct=False),
            ChoiceStepOption(text='.', feedback='', is_correct=False),
            ChoiceStepOption(text=r'test\.', feedback='', is_correct=False),
            ChoiceStepOption(text='test.', feedback='', is_correct=False),
            ChoiceStepOption(text='test', feedback='', is_correct=False),
        ],
    )

    remove_dots(step_data, settings)

    assert step_data == {
        'step_index': 1,
        'name': 'choice',
        'text': 'text',
        'options': [
            {'text': 'test.....', 'feedback': '', 'is_correct': False},
            {'text': 'test...', 'feedback': '', 'is_correct': True},
            {'text': 'test...', 'feedback': '', 'is_correct': False},
            {'text': 'test.', 'feedback': '', 'is_correct': False},
            {'text': '.', 'feedback': '', 'is_correct': False},
            {'text': r'test\.', 'feedback': '', 'is_correct': False},
            {'text': 'test', 'feedback': '', 'is_correct': False},
            {'text': 'test', 'feedback': '', 'is_correct': False},
        ],
    }


def test_remove_dots_no_options_key(settings: Settings) -> None:
    step = StepData(
        step_index=1,
        name=BlockName.CHOICE,
        text='text',
        options=[],
    )

    remove_dots(step, settings)

    assert step == {
        'step_index': 1,
        'name': 'choice',
        'text': 'text',
        'options': [],
    }
