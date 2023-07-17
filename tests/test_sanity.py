import pytest

def test_sanity_pass():
    assert True

@pytest.mark.xfail(raises=RuntimeError)
def test_sanity_fail():
    raise RuntimeError()

