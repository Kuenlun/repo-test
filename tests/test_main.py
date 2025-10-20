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


import runpy
import sys

import pytest


def test_main_module_exits_zero():
    """Test that __main__.py exits with code 0."""
    original_argv = sys.argv
    sys.argv = ["vaultlint"]
    try:
        with pytest.raises(SystemExit) as exc:
            runpy.run_module("vaultlint", run_name="__main__")
        assert exc.value.code in (0, None)
    finally:
        sys.argv = original_argv
