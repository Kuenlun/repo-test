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


"""Script to pass quality-checks CI job for merge approval."""

import subprocess
import sys

from rich.console import Console
from rich.panel import Panel

console = Console()

checks = []
try:
    console.print("🔍 GPL Headers...", style="blue")
    subprocess.run(["python", "scripts/check_gpl_headers.py"], check=True)
    checks.append("✅ GPL Headers")

    console.print("🔧 Ruff (check & format)...", style="blue")
    subprocess.run(["ruff", "check", "--fix", "."], check=True)
    subprocess.run(["ruff", "format", "."], check=True)
    checks.append("✅ Ruff (Check & Format)")

    console.print("🧪 Tests & coverage...", style="blue")
    subprocess.run(["pytest", "--cov", "--cov-fail-under=100"], check=True)

    checks.append("✅ Tests & Coverage")

    summary = "\n".join(checks) + "\n\n🎉 ALL CHECKS PASSED!"
    console.print(Panel(summary, style="bold green", title="Summary"))
except subprocess.CalledProcessError as e:
    failed_check = f"❌ {e.cmd}"
    summary = "\n".join(checks) + f"\n{failed_check}" if checks else failed_check
    console.print(Panel(summary, style="bold red", title="Summary"))
    sys.exit(1)
