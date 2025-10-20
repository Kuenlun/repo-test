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


import logging
import os
import sys
from pathlib import Path

import click
from rich.logging import RichHandler
from rich.traceback import install as rich_traceback_install

# Exit codes
EXIT_OK = 0
EXIT_ERROR = 1
EXIT_USAGE_ERROR = 2
EXIT_KEYBOARD_INTERRUPT = 130


def configure_logging(verbosity: int) -> None:
    """Map -v levels to logging levels and set up Rich logging output."""
    level = logging.WARNING
    if verbosity == 1:
        level = logging.INFO
    elif verbosity >= 2:
        level = logging.DEBUG

    logging.basicConfig(
        level=level,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True)],
        force=True,  # ensures reconfiguration even if logging was set earlier
    )


@click.command(context_settings={"show_default": True})
@click.version_option(package_name="vaultlint")
@click.argument(
    "vault_path",
    type=click.Path(
        path_type=Path, exists=True, dir_okay=True, file_okay=False, readable=True
    ),
    default=".",
)
@click.option(
    "-s",
    "--spec",
    type=click.Path(
        path_type=Path, exists=True, dir_okay=False, file_okay=True, readable=True
    ),
    required=False,
    help="Specification file used to validate the vault structure.",
)
@click.option(
    "--verbose", "-v", count=True, help="Increase verbosity. Use -vv for debug."
)
@click.option("--dry-run", is_flag=True, help="Run checks without modifying anything.")
@click.option("--quiet", "-q", is_flag=True, help="Suppress non-error console output.")
def cli(
    vault_path: Path, spec: Path | None, verbose: int, dry_run: bool, quiet: bool
) -> int:
    """VaultLint CLI."""
    # Rich traceback for nicer errors during development
    rich_traceback_install(show_locals=verbose >= 2)
    configure_logging(verbose)
    return EXIT_OK


def main() -> int:
    """Execute VaultLint CLI and return exit status."""
    try:
        # Run Click without standalone mode to handle SystemExit manually
        exit_result = cli.main(standalone_mode=False)
        return exit_result if isinstance(exit_result, int) else EXIT_ERROR

    except click.ClickException as e:
        e.show()
        return e.exit_code

    except SystemExit as e:
        code = e.code
        return code if isinstance(code, int) else EXIT_ERROR

    except KeyboardInterrupt:
        click.echo("Interrupted by user.", err=True)
        return EXIT_KEYBOARD_INTERRUPT

    except BrokenPipeError:
        # Downstream pipe closed (e.g., "| head")
        try:
            sys.stderr.close()
        except Exception:
            pass
        return EXIT_OK

    except Exception as e:
        # Catch-all for unexpected errors
        click.echo(f"Unexpected error: {e}", err=True)
        if os.environ.get("DEBUG"):
            import traceback

            traceback.print_exc()
        return EXIT_ERROR
