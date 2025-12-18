#!/usr/bin/env python3
"""
Automated multi-statement line fixer for Phase 3 test code quality.
Targets E701/E702 issues with intelligent splitting.
"""

import re
import sys
from pathlib import Path

def fix_multistatement_lines(filepath):
    """Fix multi-statement lines in a file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    modified = False
    new_lines = []
    i = 0

    while i < len(lines):
        line = lines[i]

        # Pattern 1: class Sim: attr = val; attr2 = val2
        if re.match(r'^(\s+)(class \w+):\s+(\w+\s*=.*?);(.*)$', line):
            match = re.match(r'^(\s+)(class \w+):\s+(\w+\s*=.*?);(.*)$', line)
            indent, class_def, first_attr, rest = match.groups()
            new_lines.append(f"{indent}{class_def}:\n")
            new_lines.append(f"{indent}    {first_attr}\n")
            # Handle remaining attributes
            remaining = rest.strip()
            while ';' in remaining:
                attr, remaining = remaining.split(';', 1)
                new_lines.append(f"{indent}    {attr.strip()}\n")
                remaining = remaining.strip()
            if remaining:
                new_lines.append(f"{indent}    {remaining}\n")
            modified = True

        # Pattern 2: attr = Cls(); attr2 = val
        elif re.match(r'^(\s+)(\w+\s*=.*?\(\));(.*)$', line):
            match = re.match(r'^(\s+)(\w+\s*=.*?\(\));(.*)$', line)
            indent, first_stmt, rest = match.groups()
            new_lines.append(f"{indent}{first_stmt}\n")
            new_lines.append(f"{indent}{rest.strip()}\n")
            modified = True

        # Pattern 3: x = val; y = val; z = val
        elif re.match(r'^(\s+)(\w+\s*=.*?);(.*)$', line) and 'class' not in line:
            match = re.match(r'^(\s+)(\w+\s*=.*?);(.*)$', line)
            indent, first_stmt, rest = match.groups()
            new_lines.append(f"{indent}{first_stmt}\n")
            # Handle remaining statements
            remaining = rest.strip()
            while ';' in remaining:
                stmt, remaining = remaining.split(';', 1)
                new_lines.append(f"{indent}{stmt.strip()}\n")
                remaining = remaining.strip()
            if remaining:
                new_lines.append(f"{indent}{remaining}\n")
            modified = True

        # Pattern 4: import os; sys.path...
        elif re.match(r'^(import .+);(.*)$', line):
            match = re.match(r'^(import .+);(.*)$', line)
            first_import, rest = match.groups()
            new_lines.append(f"{first_import}\n")
            new_lines.append(f"{rest.strip()}\n")
            modified = True

        else:
            new_lines.append(line)

        i += 1

    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        return True
    return False

if __name__ == "__main__":
    files = [
        "tests/test_controllers/mpc/test_mpc_consolidated.py",
        "tests/test_controllers/test_smc_guardrails_consolidated.py",
        "tests/test_plant/core/test_dynamics.py",
        "tests/test_utils/test_development/run_crossfield_tests.py",
    ]

    for file in files:
        filepath = Path(file)
        if filepath.exists():
            if fix_multistatement_lines(filepath):
                print(f"[FIXED] {file}")
            else:
                print(f"[SKIP] {file} - no changes needed")
        else:
            print(f"[ERROR] {file} not found")
