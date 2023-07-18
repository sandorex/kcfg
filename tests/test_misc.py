# misc tests

import kcfg

def test_version_api():
    assert kcfg.__version_api__ == kcfg.__version__.replace('.', '')

def test_path_expansion(tmp_path, monkeypatch):
    file = tmp_path / 'testfile'
    file_key = '__testfile'

    # TODO this is the only way i can think of to test this without refactoring
    # patch the list of files to see if it expands properly
    with monkeypatch.context() as m:
        m.setitem(kcfg.PREDEFINED_FILES, file_key, str(file))

        try:
            kcfg.main(['__testfile/Group/Key', '--write', 'Value'])
        except SystemExit:
            pass

    assert file.read_text() == r"""[Group]
Key=Value

"""

    # just in case to catch if it did not revert it
    assert file_key not in kcfg.PREDEFINED_FILES


