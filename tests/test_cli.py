from vaultlint.cli import main, run


def test_cli_functions():
    """Test that CLI functions return 0."""
    assert main() == 0
    assert run() == 0
