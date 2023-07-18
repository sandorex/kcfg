# basic sanity check whether the argument parsing is working properly

import pytest
import kcfg

def main_wrapper(args):
    '''Wraps kcfg.main to catch exit'''
    with pytest.raises(SystemExit) as e:
        kcfg.main(args)

    return e

def test_argparse_no_args():
    e = main_wrapper([])

    assert e.type == SystemExit
    assert e.value.code == 2, 'positional argument is missing so exit code should be 2'

def test_argparse_help():
    e = main_wrapper(['--help'])

    assert e.type == SystemExit
    assert e.value.code == 0, 'help should exit cleanly with exit code 0'

def test_version(capsys):
    '''Basic test that tests whether the args are parsed properly'''
    e = main_wrapper(['--version'])

    captured = capsys.readouterr()

    assert e.type == SystemExit
    assert e.value.code == 0, 'version should exit cleanly with exit code 0'
    assert captured.out.strip() == "kcfg " + kcfg.__version__
    assert captured.err == ""

def test_argparse_bad_args(tmp_path, capsys, monkeypatch):
    # test without file provided
    e = main_wrapper(['/Group/Key'])

    captured = capsys.readouterr()

    assert e.type == SystemExit
    assert e.value.code == 1
    assert captured.out.strip() == ''
    assert 'No file specified' in captured.err.strip()

    # just in case it breaks it wont fuck up your real configuration
    with monkeypatch.context() as m:
        m.setitem(kcfg.PREDEFINED_FILES, 'tempfile', str(tmp_path / 'tempfile'))

        # test if it fails when --write and --delete are set at the same time
        e = main_wrapper(['tempfile/Group/Key', '--write', '', '--delete'])
        assert e.type == SystemExit
        assert e.value.code == 1

    # test if it fails with invalid file alias
    e = main_wrapper(['tempfile/Group/Key', '--write', ''])
    assert e.type == SystemExit
    assert e.value.code == 1


