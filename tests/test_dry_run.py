# tests whether dry run is actually dry

import kcfg

# TODO test and check modification time just in case, so you can be sure its not modified or even opened for writing

TEXT = """[Group 1][Group 2][Group 3]
Key1=One
Key2=Two
"""

def test_dry_write(tmp_path):
    file = tmp_path / 'write'
    file.write_text(TEXT)

    mtime = file.stat().st_mtime

    try:
        kcfg.main(['--dry-run', '--file', str(file), '/Group 1/Group 2/Group 3/Key2', '--write', 'Three'])
    except SystemExit:
        pass

    assert file.read_text() == TEXT

    assert file.stat().st_mtime == mtime

    try:
        kcfg.main(['--dry-run', '--file', str(file), '/Group 1/Group 2/Group 3/Key3', '--write', 'Three'])
    except SystemExit:
        pass

    assert file.read_text() == TEXT

    assert file.stat().st_mtime == mtime

def test_dry_read(tmp_path, capsys):
    '''Basically should work the same as regular, dry run does nothing when
    reading'''
    file = tmp_path / 'read'
    file.write_text(TEXT)

    mtime = file.stat().st_mtime

    try:
        kcfg.main(['--dry-run', '--file', str(file), '/Group 1/Group 2/Group 3/Key2'])
    except SystemExit:
        pass

    captured = capsys.readouterr()

    assert captured.out == 'Two\n'

    # make sure the file is not modified
    assert file.read_text() == TEXT

    assert file.stat().st_mtime == mtime

def test_dry_delete(tmp_path):
    file = tmp_path / 'delete'
    file.write_text(TEXT)

    mtime = file.stat().st_mtime

    try:
        kcfg.main(['--dry-run', '--file', str(file), '/Group 1/Group 2/Group 3/Key2', '--delete'])
    except SystemExit:
        pass

    # it should not change
    assert file.read_text() == TEXT

    assert file.stat().st_mtime == mtime
