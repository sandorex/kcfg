# testing the path parsing and rejection

# '/Group 1/Group 2/Key' - path without file specified
# 'kcminputrc/Group 1/Group 2/Key' - path with file alias specified

import pytest
import kcfg

def test_invalid_paths():
    PATHS = [
        'Group',
        'Group/',
        '/Group',
        'File/Group'
        '/',
        '',
        '@',
        '?',
        ' ',
        '\t',
    ]
    for path in PATHS:
        with pytest.raises(RuntimeError) as e:
            kcfg._parse_path(path)

        # leading slash should be stripped
        if path.endswith('/'):
            path = path[:-1]

        # i am lazy to match each case and message
        assert e.value.args[0].startswith(f"Invalid path '{path}'")

def test_slashing_the_slashes():
    '''Testing ability to ignore duplicate slashes'''
    assert kcfg._parse_path('//////One////////Two////////') == (['One', 'Two'], '')

    # odd number of slashes
    with pytest.raises(RuntimeError) as e:
        kcfg._parse_path('/' * 11)

    assert e.value.args[0].startswith("Invalid path '/'")

    # even number of slashes
    with pytest.raises(RuntimeError) as e:
        kcfg._parse_path('/' * 10)

    assert e.value.args[0].startswith("Invalid path '/'")

def test_parsing():
    assert kcfg._parse_path('/Group/Key') == (['Group', 'Key'], '')
    assert kcfg._parse_path('File/Group/Group 2/Key') == (['Group', 'Group 2', 'Key'], 'File')
    assert kcfg._parse_path('File/Group/Key') == (['Group', 'Key'], 'File')

    # some involving spaces
    assert kcfg._parse_path('Really Long File Name/Group With Spaces/Even Key With Spaces') == (
        ['Group With Spaces', 'Even Key With Spaces'], 'Really Long File Name'
    )

