#!/usr/bin/env python3
"""
Automated fixer for Phase 4 remaining issues (89 total).
Handles E402, E722, E741, F841 with appropriate fixes or noqa comments.
"""

import re
import sys
from pathlib import Path

def add_noqa_to_imports_after_syspath(filepath):
    """Add noqa: E402 to imports after sys.path.insert."""
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    modified = False
    in_import_block = False
    syspath_seen = False

    for i, line in enumerate(lines):
        # Detect sys.path.insert
        if 'sys.path.insert' in line:
            syspath_seen = True
            in_import_block = True
            continue

        # If we're after sys.path and see an import without noqa
        if syspath_seen and in_import_block:
            if line.strip().startswith(('import ', 'from ')):
                if '# noqa: E402' not in line and line.strip():
                    lines[i] = line.rstrip() + '  # noqa: E402\n'
                    modified = True
            elif line.strip() and not line.strip().startswith('#'):
                # End of import block
                in_import_block = False

    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(lines)
    return modified

def fix_specific_issues():
    """Fix specific known issues."""
    fixes = [
        # E722 - Bare except
        ('scripts/analysis/screenshot_docs.py', 121, 'except:', 'except Exception:  # noqa: E722'),
        ('scripts/docs/generate_code_docs.py', 528, 'except:', 'except Exception:  # noqa: E722'),
        ('scripts/optimization/auto_complete_when_ready.py', 83, 'except:', 'except Exception:  # noqa: E722'),
        ('scripts/optimization/check_pso_completion.py', 46, 'except:', 'except (ValueError, TypeError):  # noqa: E722'),
        ('scripts/optimization/monitor_pso.py', None, 'except:', 'except Exception:  # noqa: E722'),

        # E741 - Ambiguous variable name
        ('scripts/coverage/quick_baseline.py', 13, 'lines = [l for l in content', 'lines = [line for line in content'),

        # F841 - Remove unused variables
        ('scripts/coverage/coverage_report.py', 192, '                color_code = ""', '                pass  # color_code unused'),
        ('scripts/optimization/watch_pso.py', 88, '    overall_pct =', '    # overall_pct =  # Unused'),
        ('scripts/validate_documentation.py', 226, '        tutorial_order = [', '        # tutorial_order = [  # Unused'),
        ('scripts/validate_memory_optimization.py', 25, '    state_dim = 6', '    # state_dim = 6  # Unused'),
        ('scripts/validate_memory_optimization.py', 33, '    baseline_start_mem =', '    # baseline_start_mem =  # Unused'),
        ('scripts/validate_memory_optimization.py', 53, '    optimized_start_mem =', '    # optimized_start_mem =  # Unused'),
        ('scripts/validate_memory_optimization.py', 115, '    state_dim = 6', '    # state_dim = 6  # Unused'),
        ('scripts/validate_memory_optimization.py', 130, '        x_curr = x0', '        # x_curr = x0  # Unused'),
        ('scripts/validate_memory_pool.py', 54, '        initial_memory =', '        # initial_memory =  # Unused'),
    ]

    fixed_count = 0
    for filepath_str, line_num, old_text, new_text in fixes:
        filepath = Path(filepath_str)
        if not filepath.exists():
            continue

        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        modified = False
        if line_num:
            # Fix specific line
            if line_num - 1 < len(lines) and old_text in lines[line_num - 1]:
                lines[line_num - 1] = lines[line_num - 1].replace(old_text, new_text)
                modified = True
        else:
            # Fix all occurrences
            for i, line in enumerate(lines):
                if old_text in line:
                    lines[i] = line.replace(old_text, new_text)
                    modified = True

        if modified:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.writelines(lines)
            print(f"[FIXED] {filepath_str}:{line_num or 'multiple'}")
            fixed_count += 1

    return fixed_count

def main():
    fixed_count = 0

    # Fix E402 - imports after sys.path.insert
    print("=== Fixing E402 (Imports After sys.path) ===")
    for script_file in Path('scripts/optimization').glob('*.py'):
        if add_noqa_to_imports_after_syspath(script_file):
            print(f"[FIXED] {script_file}: added E402 noqa to imports")
            fixed_count += 1

    # Fix specific issues
    print("\n=== Fixing Specific Issues (E722, E741, F841) ===")
    fixed_count += fix_specific_issues()

    print(f"\n[SUCCESS] Fixed issues in {fixed_count} operations")
    return 0

if __name__ == "__main__":
    sys.exit(main())
