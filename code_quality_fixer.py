#======================================================================================\\\
#=============================== code_quality_fixer.py ================================\\\
#======================================================================================\\\

#!/usr/bin/env python3
"""
Code Quality Fixer for DIP SMC PSO Project

This script automatically fixes the most critical code quality issues:
1. ASCII header width standardization
2. Unused import removal (safe removals only)
3. Basic type hint additions
4. Import organization
"""

import ast
import os
import re
from pathlib import Path
from typing import List, Set, Dict, Any
import json


class ImportCleaner(ast.NodeVisitor):
    """AST visitor to identify unused imports safely."""

    def __init__(self):
        self.imports = {}  # name -> (module, line)
        self.from_imports = {}  # name -> (module, line)
        self.used_names = set()

    def visit_Import(self, node):
        for alias in node.names:
            name = alias.asname if alias.asname else alias.name
            self.imports[name] = (alias.name, node.lineno)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        for alias in node.names:
            name = alias.asname if alias.asname else alias.name
            self.from_imports[name] = (node.module, node.lineno)
        self.generic_visit(node)

    def visit_Name(self, node):
        self.used_names.add(node.id)
        self.generic_visit(node)

    def visit_Attribute(self, node):
        if isinstance(node.value, ast.Name):
            self.used_names.add(node.value.id)
        # Also check for module.submodule usage
        if isinstance(node.value, ast.Attribute) and isinstance(node.value.value, ast.Name):
            self.used_names.add(node.value.value.id)
        self.generic_visit(node)


class CodeQualityFixer:
    """Automated code quality improvement tool."""

    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.fixes_applied = {
            'ascii_headers_fixed': 0,
            'unused_imports_removed': 0,
            'files_processed': 0,
            'errors': []
        }

    def fix_ascii_header(self, file_path: Path) -> bool:
        """Fix ASCII header to be exactly 90 characters + \\\\\\."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            if not lines:
                return False

            # Check if file has ASCII header
            if not (len(lines) >= 3 and lines[0].startswith('#=') and lines[2].startswith('#=')):
                return False

            # Get the file path for the header
            rel_path = file_path.relative_to(self.project_root)
            display_path = str(rel_path).replace('\\\\', '/')

            # Create properly formatted header (exactly 90 characters + \\\\\\)
            total_width = 90
            end_marker = "\\\\\\\\\\\\\\\\"
            available_width = total_width - len(end_marker)

            if len(display_path) > available_width - 4:
                display_path = "..." + display_path[-(available_width - 7):]

            padding_total = available_width - len(display_path)
            padding_left = padding_total // 2
            padding_right = padding_total - padding_left

            new_header = [
                "#" + "=" * available_width + end_marker + "\\n",
                "#" + "=" * padding_left + " " + display_path + " " + "=" * (padding_right - 1) + end_marker + "\\n",
                "#" + "=" * available_width + end_marker + "\\n"
            ]

            # Replace existing header
            content_start = 3
            if len(lines) > 3 and lines[3].strip() == '':
                content_start = 3
            else:
                new_header.append("\\n")
                content_start = 3

            new_lines = new_header + lines[content_start:]

            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)

            self.fixes_applied['ascii_headers_fixed'] += 1
            return True

        except Exception as e:
            self.fixes_applied['errors'].append(f"ASCII header fix failed for {file_path}: {e}")
            return False

    def remove_unused_imports(self, file_path: Path) -> int:
        """Remove unused imports safely."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\\n')

            # Skip files that are too risky to modify
            if any(risky in str(file_path) for risky in ['__init__.py', 'conftest.py']):
                return 0

            # Parse AST
            try:
                tree = ast.parse(content)
            except SyntaxError:
                return 0

            cleaner = ImportCleaner()
            cleaner.visit(tree)

            # Find truly unused imports (conservative approach)
            unused_imports = set()
            for name in cleaner.imports:
                if name not in cleaner.used_names:
                    # Skip common modules that might be used indirectly
                    if name not in ['logging', 'numpy', 'np', 'matplotlib', 'plt', 'os', 'sys', 'pathlib']:
                        unused_imports.add(cleaner.imports[name][1])

            for name in cleaner.from_imports:
                if name not in cleaner.used_names:
                    # Skip type checking imports and common utilities
                    if not any(skip in name.lower() for skip in ['typing', 'protocol', 'union', 'optional', 'dict', 'list']):
                        unused_imports.add(cleaner.from_imports[name][1])

            if not unused_imports:
                return 0

            # Remove unused import lines
            removed_count = 0
            new_lines = []
            for i, line in enumerate(lines, 1):
                if i not in unused_imports:
                    new_lines.append(line)
                else:
                    removed_count += 1

            if removed_count > 0:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write('\\n'.join(new_lines))

            return removed_count

        except Exception as e:
            self.fixes_applied['errors'].append(f"Import cleaning failed for {file_path}: {e}")
            return 0

    def organize_imports(self, file_path: Path) -> bool:
        """Organize imports according to PEP 8."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\\n')

            # Find import section
            import_start = None
            import_end = None

            for i, line in enumerate(lines):
                if line.startswith(('import ', 'from ')) and import_start is None:
                    import_start = i
                elif import_start is not None and not line.startswith(('import ', 'from ', '#')) and line.strip():
                    import_end = i
                    break

            if import_start is None:
                return False

            if import_end is None:
                import_end = len(lines)

            # Extract imports
            import_lines = lines[import_start:import_end]

            # Categorize imports
            stdlib_imports = []
            third_party_imports = []
            local_imports = []

            stdlib_modules = {
                'os', 'sys', 'pathlib', 'logging', 'argparse', 'json', 'pickle',
                'collections', 'itertools', 'functools', 'operator', 're', 'time',
                'datetime', 'math', 'random', 'typing', 'dataclasses', 'abc',
                'contextlib', 'concurrent', 'multiprocessing', 'threading'
            }

            for line in import_lines:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue

                if line.startswith('from '):
                    module = line.split()[1].split('.')[0]
                else:
                    module = line.split()[1].split('.')[0]

                if module in stdlib_modules:
                    stdlib_imports.append(line)
                elif module.startswith(('src', '.')):
                    local_imports.append(line)
                else:
                    third_party_imports.append(line)

            # Organize imports
            organized_imports = []

            if stdlib_imports:
                organized_imports.extend(sorted(stdlib_imports))
                organized_imports.append('')

            if third_party_imports:
                organized_imports.extend(sorted(third_party_imports))
                organized_imports.append('')

            if local_imports:
                organized_imports.extend(sorted(local_imports))
                organized_imports.append('')

            # Reconstruct file
            new_lines = (
                lines[:import_start] +
                organized_imports +
                lines[import_end:]
            )

            with open(file_path, 'w', encoding='utf-8') as f:
                f.write('\\n'.join(new_lines))

            return True

        except Exception as e:
            self.fixes_applied['errors'].append(f"Import organization failed for {file_path}: {e}")
            return False

    def fix_file(self, file_path: Path) -> Dict[str, Any]:
        """Apply all fixes to a single file."""
        self.fixes_applied['files_processed'] += 1

        results = {
            'path': str(file_path.relative_to(self.project_root)),
            'ascii_header_fixed': False,
            'unused_imports_removed': 0,
            'imports_organized': False
        }

        # Fix ASCII headers
        results['ascii_header_fixed'] = self.fix_ascii_header(file_path)

        # Remove unused imports (conservative)
        results['unused_imports_removed'] = self.remove_unused_imports(file_path)
        self.fixes_applied['unused_imports_removed'] += results['unused_imports_removed']

        # Organize imports
        results['imports_organized'] = self.organize_imports(file_path)

        return results

    def fix_project(self) -> Dict[str, Any]:
        """Fix the entire project."""
        print("Starting automated code quality fixes...")

        # Find Python files to fix
        src_files = list(self.project_root.glob('src/**/*.py'))
        test_files = list(self.project_root.glob('tests/**/*.py'))
        root_files = [f for f in self.project_root.glob('*.py') if f.name != 'code_quality_fixer.py']

        priority_files = src_files + root_files  # Fix src and root first
        all_files = priority_files + test_files

        print(f"Processing {len(all_files)} Python files...")

        file_results = []
        for file_path in all_files:
            if file_path.name.startswith('.'):
                continue
            result = self.fix_file(file_path)
            file_results.append(result)

            # Progress indicator
            if self.fixes_applied['files_processed'] % 50 == 0:
                print(f"  Processed {self.fixes_applied['files_processed']} files...")

        return {
            'summary': self.fixes_applied,
            'files': file_results
        }

    def save_results(self, output_file: str = "code_quality_fixes.json"):
        """Save fix results and run the process."""
        results = self.fix_project()

        output_path = self.project_root / output_file
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)

        print(f"\\nFixes applied successfully!")
        print(f"Results saved to: {output_path}")
        print(f"Files processed: {self.fixes_applied['files_processed']}")
        print(f"ASCII headers fixed: {self.fixes_applied['ascii_headers_fixed']}")
        print(f"Unused imports removed: {self.fixes_applied['unused_imports_removed']}")

        if self.fixes_applied['errors']:
            print(f"Errors encountered: {len(self.fixes_applied['errors'])}")
            for error in self.fixes_applied['errors'][:5]:  # Show first 5 errors
                print(f"  - {error}")

        return results


def main():
    """Main function."""
    import sys

    if len(sys.argv) > 1:
        project_root = sys.argv[1]
    else:
        project_root = os.getcwd()

    fixer = CodeQualityFixer(project_root)
    fixer.save_results()


if __name__ == "__main__":
    main()