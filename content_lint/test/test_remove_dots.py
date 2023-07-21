from content_lint.transform.plain_text.remove_dots import remove_dots_in_the_string, remove_dots
from content_lint.typing import StepData


def test_remove_dots_in_the_string():
    assert remove_dots_in_the_string('test.....') == 'test.....'
    assert remove_dots_in_the_string('test....') == 'test...'
    assert remove_dots_in_the_string('test...') == 'test...'
    assert remove_dots_in_the_string('test..') == 'test.'
    assert remove_dots_in_the_string('.') == '.'
    assert remove_dots_in_the_string('test\.') == 'test\.'
    assert remove_dots_in_the_string('test.') == 'test'
    assert remove_dots_in_the_string('test') == 'test'
    assert remove_dots_in_the_string(
        'Compilation error: cannot use [3]int{...} (type [3]int) as type int in assignment.') \
           == 'Compilation error: cannot use [3]int{...} (type [3]int) as type int in assignment'
    assert remove_dots_in_the_string('Depending on the programming language, the shapes of blocks change.') \
           == 'Depending on the programming language, the shapes of blocks change'
    assert remove_dots_in_the_string('If the date column is not an index, we need to run df.set_index(["date"]).') \
           == 'If the date column is not an index, we need to run df.set_index(["date"])'
    assert remove_dots_in_the_string('Add server.error.include-message=always to application.properties') \
           == 'Add server.error.include-message=always to application.properties'
    assert remove_dots_in_the_string('Because of its approach: running the app – cleaning – running again etc..') \
           == 'Because of its approach: running the app – cleaning – running again etc.'
    assert remove_dots_in_the_string('To explain the meaning of suffixes like SNAPSHOT, M, etc.') \
           == 'To explain the meaning of suffixes like SNAPSHOT, M, etc'
    assert remove_dots_in_the_string('') == ''
    assert remove_dots_in_the_string('head [OPTION]... [FILE LIST]...') == 'head [OPTION]... [FILE LIST]...'


def test_remove_dots():
    step_data = {
        'step_index': 0,
        'block_name': 'block',
        'text': 'text',
        'code_templates': {},
        'supported_code_templates_languages': (),
        'files': (),
        'stage': None,
        'options': [
            {'text': 'test.....'},
            {'text': 'test....'},
            {'text': 'test...'},
            {'text': 'test..'},
            {'text': '.'},
            {'text': 'test\.'},
            {'text': 'test.'},
            {'text': 'test'}
        ]
    }

    remove_dots(step_data)

    assert step_data == {
        'step_index': 0,
        'block_name': 'block',
        'text': 'text',
        'code_templates': {},
        'supported_code_templates_languages': (),
        'files': (),
        'stage': None,
        'options': [
            {'text': 'test.....'},
            {'text': 'test...'},
            {'text': 'test...'},
            {'text': 'test.'},
            {'text': '.'},
            {'text': 'test\.'},
            {'text': 'test'},
            {'text': 'test'}
        ]
    }


def test_remove_dots_no_options_key():
    step_block: StepData = {
        'step_index': 0,
        'block_name': 'block_name',
        'text': 'text',
        'code_templates': {},
        'supported_code_templates_languages': (),
        'files': (),
        'stage': None,
        'options': ()
    }
    remove_dots(step_block)
    assert step_block == {
        'step_index': 0,
        'block_name': 'block_name',
        'text': 'text',
        'code_templates': {},
        'supported_code_templates_languages': (),
        'files': (),
        'stage': None,
        'options': ()
    }