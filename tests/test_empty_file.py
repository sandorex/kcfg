# testing writing to empty files

import kcfg

def test_write_empty(tmp_path):
    file = tmp_path / 'write_empty'

    try:
        kcfg.main(['--file', str(file), '/Group/Key', '--write', 'Value'])
    except SystemExit:
        pass

    assert file.read_text() == r"""[Group]
Key=Value

"""

def test_read_empty(tmp_path, capsys):
    file = tmp_path / 'read_empty'

    try:
        kcfg.main(['--file', str(file), '/Group/Key'])
    except SystemExit:
        pass

    captured = capsys.readouterr()

    # there should be no logging to stdout even without quiet
    assert captured.out == ''

def test_delete_empty(tmp_path):
    file = tmp_path / 'delete_empty'

    # this test is kinda useless but eh

    try:
        kcfg.main(['--file', str(file), '/Group/Key', '--delete'])
    except SystemExit:
        pass

