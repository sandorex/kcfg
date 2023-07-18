# general tests on real files using main

import kcfg

TEXT = """[Group 1][Group 2][Group 3]
Key1=One
Key2=Two
"""

def test_write(tmp_path):
    file = tmp_path / 'write'
    file.write_text(TEXT)

    try:
        kcfg.main(['--file', str(file), '/Group 1/Group 2/Group 3/Key2', '--write', 'Three'])
    except SystemExit:
        pass

    assert file.read_text() == r"""[Group 1][Group 2][Group 3]
Key1=One
Key2=Three

"""

    try:
        kcfg.main(['--file', str(file), '/Group 1/Group 2/Group 3/Key3', '--write', 'Three'])
    except SystemExit:
        pass

    assert file.read_text() == r"""[Group 1][Group 2][Group 3]
Key1=One
Key2=Three
Key3=Three

"""

def test_read(tmp_path, capsys):
    file = tmp_path / 'read'
    file.write_text(TEXT)

    try:
        kcfg.main(['--file', str(file), '/Group 1/Group 2/Group 3/Key2'])
    except SystemExit:
        pass

    captured = capsys.readouterr()

    assert captured.out == 'Two\n'

    # make sure the file is not modified
    assert file.read_text() == TEXT

def test_delete(tmp_path):
    file = tmp_path / 'delete'
    file.write_text(TEXT)

    try:
        kcfg.main(['--file', str(file), '/Group 1/Group 2/Group 3/Key2', '--delete'])
    except SystemExit:
        pass

    assert file.read_text() == """[Group 1][Group 2][Group 3]
Key1=One

"""

