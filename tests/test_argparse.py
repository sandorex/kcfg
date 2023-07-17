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

