# VaultLint - Obsidian Vault Linter
# Copyright (C) 2025  Juan Luis Leal Contreras (Kuenlun)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


from unittest import mock

import click

import vaultlint.cli as cli

# =============================================================================
# Main function tests
# =============================================================================


def test_main_click_exception(monkeypatch):
    """Test that main handles click.ClickException correctly."""
    exc = click.ClickException("error")
    mock_show = mock.Mock()
    exc.show = mock_show

    monkeypatch.setattr(cli.cli, "main", mock.Mock(side_effect=exc))
    exit_code = cli.main()

    assert exit_code == exc.exit_code


def test_main_system_exit(monkeypatch):
    """Test that main handles SystemExit correctly."""
    # Test with integer code
    expected_code = cli.EXIT_USAGE_ERROR
    monkeypatch.setattr(
        cli.cli, "main", mock.Mock(side_effect=SystemExit(expected_code))
    )
    assert cli.main() == expected_code

    # Test with non-integer code
    monkeypatch.setattr(cli.cli, "main", mock.Mock(side_effect=SystemExit("error")))
    assert cli.main() == cli.EXIT_ERROR


def test_main_keyboard_interrupt(monkeypatch):
    """Test that main handles KeyboardInterrupt correctly."""
    monkeypatch.setattr(cli.cli, "main", mock.Mock(side_effect=KeyboardInterrupt))
    assert cli.main() == cli.EXIT_KEYBOARD_INTERRUPT


def test_main_broken_pipe_error(monkeypatch):
    """Test that main handles BrokenPipeError correctly."""
    mock_stderr = mock.Mock()
    monkeypatch.setattr(cli.sys, "stderr", mock_stderr)
    monkeypatch.setattr(cli.cli, "main", mock.Mock(side_effect=BrokenPipeError))

    assert cli.main() == cli.EXIT_OK
    mock_stderr.close.assert_called_once()


def test_main_broken_pipe_error_close_fails(monkeypatch):
    """Test BrokenPipeError when stderr.close() raises an exception."""
    mock_stderr = mock.Mock()
    mock_stderr.close.side_effect = Exception("Close failed")
    monkeypatch.setattr(cli.sys, "stderr", mock_stderr)
    monkeypatch.setattr(cli.cli, "main", mock.Mock(side_effect=BrokenPipeError))

    assert cli.main() == cli.EXIT_OK


def test_main_unexpected_exception(monkeypatch):
    """Test that main handles unexpected exceptions correctly."""
    monkeypatch.setattr(
        cli.cli, "main", mock.Mock(side_effect=ValueError("Unexpected error"))
    )
    assert cli.main() == cli.EXIT_ERROR


def test_main_unexpected_exception_with_debug(monkeypatch):
    """Test unexpected exception with DEBUG environment variable set."""
    monkeypatch.setenv("DEBUG", "1")
    monkeypatch.setattr(
        cli.cli, "main", mock.Mock(side_effect=RuntimeError("Debug error"))
    )
    assert cli.main() == cli.EXIT_ERROR


# =============================================================================
# Logging configuration tests
# =============================================================================


def test_configure_logging():
    """Test that configure_logging sets the correct logging level."""
    import logging

    # Test default (WARNING)
    cli.configure_logging(0)
    assert logging.getLogger().level == logging.WARNING

    # Test INFO level (-v)
    cli.configure_logging(1)
    assert logging.getLogger().level == logging.INFO

    # Test DEBUG level (-vv or more)
    cli.configure_logging(2)
    assert logging.getLogger().level == logging.DEBUG
