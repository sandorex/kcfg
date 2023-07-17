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

