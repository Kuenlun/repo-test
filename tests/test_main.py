import runpy

import pytest


def test_main_module_exits_zero():
    """Test that __main__.py exits with code 0."""
    with pytest.raises(SystemExit) as exc:
        runpy.run_module("vaultlint", run_name="__main__")
    assert exc.value.code == 0
