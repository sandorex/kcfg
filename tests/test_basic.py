# contains basic tests, reading and writing to known file

import kcfg
import io

EXAMPLE_CONFIG_TEXT = r"""
[ColorEffects:Inactive]
ChangeSelectionColor=true
Color=112,111,110
ColorAmount=0.025000000000000001
ContrastAmount=0.10000000000000001
ContrastEffect=2
Enable=false
IntensityAmount=0

[KFileDialog Settings]
Automatically select filename extension=true
Breadcrumb Navigation=false
PathCombo Completionmode=5
Show Inline Previews=true
Show Preview=false
Show hidden files=false
Sort by=Name
Speedbar Width=138
View Style=DetailTree
"""

# this should always correspond to EXAMPLE_CONFIG_FILE
EXAMPLE_CONFIG_DATA = {
    # tests if all these kinds of data is read as simple string
    'ColorEffects:Inactive': {
        'ChangeSelectionColor': 'true',
        'Color': '112,111,110',
        'ColorAmount': '0.025000000000000001',
        'ContrastAmount': '0.10000000000000001',
        'ContrastEffect': '2',
        'Enable': 'false',
        'IntensityAmount': '0',
    },

    # this part has a lot of spaces in key names
    'KFileDialog Settings': {
        'Automatically select filename extension': 'true',
        'Breadcrumb Navigation': 'false',
        'PathCombo Completionmode': '5',
        'Show Inline Previews': 'true',
        'Show Preview': 'false',
        'Show hidden files': 'false',
        'Sort by': 'Name',
        'Speedbar Width': '138',
        'View Style': 'DetailTree',
    }
}

def test_basic_read():
    fp = io.StringIO(EXAMPLE_CONFIG_TEXT)
    data = kcfg.read_file(fp)

    assert data == EXAMPLE_CONFIG_DATA

def test_basic_write():
    fp = io.StringIO()
    kcfg.write_file(fp, EXAMPLE_CONFIG_DATA)

    # NOTE: calling strip cause configparser can add some newlines
    assert fp.getvalue().strip() == EXAMPLE_CONFIG_TEXT.strip()

TEST_DATA = { 'Test': { 'Key': 'Value' } }
def test_set():
    data = {}
    kcfg.set_section_key(data, 'Test', 'Key', 'Value')
    assert data == TEST_DATA

    # set on empty section
    data = { 'Test': {} }
    kcfg.set_section_key(data, 'Test', 'Key', 'Value')
    assert data == TEST_DATA

    # set when the key already exists
    # with different value
    data = { 'Test': { 'Key': 'Value2' } }
    kcfg.set_section_key(data, 'Test', 'Key', 'Value')
    assert data == TEST_DATA

    # set when multiple other keys already exist
    data = { 'Test': { 'Key1': 'Value1', 'Key2': 'Value2' } }
    kcfg.set_section_key(data, 'Test', 'Key3', 'Value3')
    assert data == { 'Test': { 'Key1': 'Value1', 'Key2': 'Value2', 'Key3': 'Value3' } }

    # same value
    data = TEST_DATA
    kcfg.set_section_key(data, 'Test', 'Key', 'Value')
    assert data == TEST_DATA

def test_read():
    assert kcfg.read_section_key(TEST_DATA, 'Test', 'Key') == 'Value'

    # default default is None
    assert kcfg.read_section_key(TEST_DATA, 'Test', 'Key2') is None

    # custom default
    assert kcfg.read_section_key(TEST_DATA, 'Test', 'Key2', 1) == 1

def test_delete():
    # with empty
    data = {}
    assert kcfg.delete_section_key(data, 'Test', 'Key') is None

    # with empty section
    data = { 'Test': {} }
    assert kcfg.delete_section_key(data, 'Test', 'Key') is None

    # with set key
    data = TEST_DATA
    assert kcfg.delete_section_key(data, 'Test', 'Key') == 'Value'

