# vaultlint - Obsidian vault linter
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


import click
from rich.console import Console


@click.command()
@click.argument('vault_path', type=click.Path(exists=True), default='.')
@click.option(
    '-s',
    '--spec',
    type=click.Path(exists=True),
    required=False,
    help="Specification file for structure checking",
)
@click.option('--verbose', '-v', count=True, help="Increase verbosity level")
def cli(vault_path, spec, verbose):
    console = Console()
    console.print(f"Linting vault at {vault_path}", style="bold blue")
    if spec:
        console.print(f"Using specification file: {spec}", style="dim")
    if verbose >= 1:
        console.print("Verbose mode enabled", style="dim")
    if verbose >= 2:
        console.print("Extra verbose details...", style="yellow")
    # Placeholder for actual linting logic
    console.print("Linting complete!", style="green")


def main() -> int:
    return cli.main(standalone_mode=False)
