#!/usr/bin/env python3
"""
Automated fixer for Phase 5 Round 2: F821 undefined name errors.
Adds missing imports for the 58 F821 issues identified.
"""

import re
from pathlib import Path

# Define fixes by file
fixes = [
    # pso_optimizer.py - Missing logger import (22 occurrences)
    {
        "file": "src/optimization/algorithms/pso_optimizer.py",
        "action": "add_import",
        "import_line": "import logging",
        "after_imports": True,
        "add_logger_init": "logger = logging.getLogger(__name__)"
    },

    # control_analysis.py - Missing scipy functions
    {
        "file": "src/analysis/performance/control_analysis.py",
        "action": "replace",
        "old": "return controllability_mat(A, B)",
        "new": "from scipy.signal import cont2discrete\n        from scipy.linalg import ctrb\n        return ctrb(A, B)"
    },
    {
        "file": "src/analysis/performance/control_analysis.py",
        "action": "replace",
        "old": "return observability_mat(A, C)",
        "new": "from scipy.linalg import observability_matrix\n        return observability_matrix(A, C)"
    },

    # protocols.py - Missing Tuple import
    {
        "file": "src/interfaces/core/protocols.py",
        "action": "add_import",
        "import_line": "from typing import Tuple"
    },

    # factory.py - Missing pickle import
    {
        "file": "src/interfaces/data_exchange/factory.py",
        "action": "add_import",
        "import_line": "import pickle"
    },

    # hardware/factory.py - Missing asyncio import
    {
        "file": "src/interfaces/hardware/factory.py",
        "action": "add_import",
        "import_line": "import asyncio"
    },

    # monitoring/metrics_collector.py - Missing asyncio import
    {
        "file": "src/interfaces/monitoring/metrics_collector.py",
        "action": "add_import",
        "import_line": "import asyncio"
    },

    # optimization/__init__.py - Missing numpy import
    {
        "file": "src/optimization/__init__.py",
        "action": "add_import",
        "import_line": "import numpy as np"
    },

    # context.py - Missing List import
    {
        "file": "src/optimization/core/context.py",
        "action": "add_import",
        "import_line": "from typing import List"
    },

    # vector_sim.py - Missing Iterable import
    {
        "file": "src/simulation/engines/vector_sim.py",
        "action": "add_import",
        "import_line": "from collections.abc import Iterable"
    },
]

def add_import_to_file(filepath: Path, import_line: str, logger_init: str = None):
    """Add import statement to file if not already present."""
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Check if import already exists
    if any(import_line in line for line in lines):
        print(f"  [OK] Import already exists: {import_line}")
        return False

    # Find insertion point (after other imports)
    insert_idx = 0
    in_docstring = False
    found_import = False

    for i, line in enumerate(lines):
        stripped = line.strip()

        # Track docstrings
        if stripped.startswith('"""') or stripped.startswith("'''"):
            in_docstring = not in_docstring
            continue

        if in_docstring:
            continue

        # Skip comments and empty lines at top
        if stripped.startswith('#') or not stripped:
            continue

        # Found an import
        if stripped.startswith(('import ', 'from ')):
            found_import = True
            insert_idx = i + 1
        elif found_import and not stripped.startswith(('import ', 'from ')):
            # First non-import line after imports
            break

    # Insert the import
    lines.insert(insert_idx, f"{import_line}\n")

    # Add logger initialization if requested
    if logger_init:
        lines.insert(insert_idx + 1, f"{logger_init}\n\n")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(lines)

    print(f"  [+] Added import: {import_line}")
    if logger_init:
        print(f"  [+] Added: {logger_init}")
    return True

def main():
    project_root = Path(__file__).parent.parent
    total_fixes = 0

    print("Phase 5 Round 2: Fixing F821 undefined name errors\n")

    # Group fixes by file
    files_to_fix = {}
    for fix in fixes:
        filepath = project_root / fix["file"]
        if filepath not in files_to_fix:
            files_to_fix[filepath] = []
        files_to_fix[filepath].append(fix)

    # Apply fixes
    for filepath, file_fixes in files_to_fix.items():
        print(f"\nFixing {filepath.relative_to(project_root)}:")

        for fix in file_fixes:
            if fix["action"] == "add_import":
                import_line = fix["import_line"]
                logger_init = fix.get("add_logger_init")
                if add_import_to_file(filepath, import_line, logger_init):
                    total_fixes += 1

    print(f"\n[DONE] Applied {total_fixes} fixes")
    print("\nRemaining F821 errors will need manual review:")
    print("  - Forward references (TYPE_CHECKING)")
    print("  - Optional dependencies (CMAES, BayesianOptimization)")
    print("  - Undefined classes (Hardware classes, OptimizationResult)")
    print("  - Variable typos (epsilon)")

if __name__ == "__main__":
    main()
