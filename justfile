PYTHON_VENV := "venv"
PYTHON_EXE := PYTHON_VENV / "bin" / "python3"

# build python package using flit
build: _venv
    "{{PYTHON_EXE}}" -m flit build --no-use-vcs

# run tests
test *args: _venv-test
    "{{PYTHON_EXE}}" -m pytest {{args}} tests/

# tests then builds and pushes to pypi
publish: test _venv
    "{{PYTHON_EXE}}" -m flit publish

# clean built packages
clean:
    rm -r "{{PYTHON_VENV}}"

# creates a venv and installs deps if not already done
_venv:
    test -d "{{PYTHON_VENV}}" || python3 -m venv "{{PYTHON_VENV}}"
    test -f "{{PYTHON_VENV}}/bin/flit" || "{{PYTHON_EXE}}" -m pip install flit
    test -f "{{PYTHON_VENV}}/bin/kcfg" || "{{PYTHON_EXE}}" -m flit install --symlink

# creates a venv and installs testing deps if not already done
_venv-test: _venv
    test -f "{{PYTHON_VENV}}/bin/pytest" || "{{PYTHON_EXE}}" -m pip install pytest
