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


"""
Script to verify that all .py files start exactly with the required GPL v3 header
"""

import sys
from pathlib import Path

# The EXACT GPL header that must appear at the start of every .py file
REQUIRED_GPL_HEADER = '''# vaultlint - Obsidian vault linter
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


'''


def check_gpl_header(file_path: Path) -> bool:
    """
    Check if a file starts EXACTLY with the required GPL v3 header.

    Returns:
        bool: True if the file starts exactly with the required header
    """
    try:
        with open(file_path, encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"⚠️  Could not read {file_path}: {e}")
        return False

    # Check if file starts exactly with the required GPL header
    return content.startswith(REQUIRED_GPL_HEADER)


def main():
    print("🔍 Checking that all .py files start EXACTLY with GPL v3 header...\n")

    # Find all .py files in the project
    root = Path(".")
    py_files = list(root.rglob("*.py"))

    if not py_files:
        print("⚠️  No .py files found")
        return 0

    failed_files = []

    for py_file in sorted(py_files):
        if check_gpl_header(py_file):
            print(f"✅ {py_file}")
        else:
            print(f"❌ {py_file}")
            failed_files.append(py_file)

    # Summary
    print("\n" + "━" * 50)
    print("📊 Summary:")
    print(f"   Total files: {len(py_files)}")
    print(f"   Passed: {len(py_files) - len(failed_files)}")
    print(f"   Failed: {len(failed_files)}")
    print("━" * 50)

    if not failed_files:
        print("\n🎉 All Python files start exactly with the required GPL v3 header")
        return 0
    else:
        print(f"\n❌ {len(failed_files)} file(s) missing GPL header")
        print("\n💡 Each .py file must start EXACTLY with this header:")
        print(REQUIRED_GPL_HEADER)
        return 1


if __name__ == "__main__":
    sys.exit(main())
