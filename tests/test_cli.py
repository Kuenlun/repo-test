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


from vaultlint.cli import main, run


def test_cli_functions():
    """Test that CLI functions return 0."""
    assert main() == 0
    assert run() == 0
