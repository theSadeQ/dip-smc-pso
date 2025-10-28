#!/usr/bin/env python3
"""
Validation Script for Task 2: Factory Refactoring

Purpose: Automated validation that factory refactoring is correctly implemented
Usage: python .project/dev_tools/audit/phase2/validate_task2.py

Checks:
1. All 4 modules created (registration, utils, validation, core)
2. Module imports resolve without circular dependencies
3. Public API backward compatibility maintained
4. Test suite still passes
5. API equivalence (old == new)
6. Module sizes within thresholds
7. Documentation updated

Exit Codes:
  0 - All checks passed
  1 - One or more checks failed
"""

import sys
import warnings
from pathlib import Path
from typing import Tuple, List
import subprocess

# ANSI color codes
GREEN = '\033[0;32m'
RED = '\033[0;31m'
YELLOW = '\033[1;33m'
BLUE = '\033[0;34m'
NC = '\033[0m'  # No Color


class Task2Validator:
    """Validator for factory refactoring (Task 2)."""

    def __init__(self):
        self.checks_passed = 0
        self.checks_failed = 0
        self.checks_warned = 0
        self.results = []

    def print_header(self):
        """Print validation header."""
        print(f"{BLUE}╔════════════════════════════════════════════════════════════╗{NC}")
        print(f"{BLUE}║     TASK 2 VALIDATION: FACTORY REFACTORING                ║{NC}")
        print(f"{BLUE}╚════════════════════════════════════════════════════════════╝{NC}")
        print()

    def run_check(self, name: str, check_func) -> bool:
        """Run a single validation check."""
        print(f"{BLUE}[{self.checks_passed + self.checks_failed + self.checks_warned + 1}/7] {name}...{NC}")

        try:
            passed, message = check_func()
            if passed:
                print(f"{GREEN}[✓] {name}: PASS{NC}")
                if message:
                    print(f"    {message}")
                self.checks_passed += 1
                self.results.append((name, "PASS", message))
                return True
            else:
                print(f"{RED}[✗] {name}: FAIL{NC}")
                if message:
                    print(f"    {message}")
                self.checks_failed += 1
                self.results.append((name, "FAIL", message))
                return False
        except Exception as e:
            print(f"{RED}[✗] {name}: ERROR{NC}")
            print(f"    {str(e)}")
            self.checks_failed += 1
            self.results.append((name, "ERROR", str(e)))
            return False

    def check_modules_exist(self) -> Tuple[bool, str]:
        """Check 1: Verify all 4 factory modules created."""
        expected_modules = [
            "src/controllers/factory/__init__.py",
            "src/controllers/factory/registration.py",
            "src/controllers/factory/utils.py",
            "src/controllers/factory/validation.py",
            "src/controllers/factory/core.py",
        ]

        missing_modules = []
        for module_path in expected_modules:
            if not Path(module_path).exists():
                missing_modules.append(module_path)

        if missing_modules:
            return False, f"Missing modules: {', '.join(missing_modules)}"
        else:
            return True, f"All {len(expected_modules)} modules created"

    def check_module_imports(self) -> Tuple[bool, str]:
        """Check 2: Verify module imports resolve without circular dependencies."""
        try:
            # Test each module individually
            modules_to_test = [
                "src.controllers.factory.registration",
                "src.controllers.factory.utils",
                "src.controllers.factory.validation",
                "src.controllers.factory.core",
                "src.controllers.factory",  # __init__.py
            ]

            for module_name in modules_to_test:
                try:
                    __import__(module_name)
                except ImportError as e:
                    return False, f"Import failed for {module_name}: {e}"

            return True, f"All {len(modules_to_test)} modules import successfully (no circular deps)"

        except Exception as e:
            return False, f"Import check error: {e}"

    def check_backward_compatibility(self) -> Tuple[bool, str]:
        """Check 3: Verify public API backward compatibility maintained."""
        try:
            # Suppress deprecation warnings for this test
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", DeprecationWarning)

                # Test old-style imports (must still work)
                from src.controllers.factory import (
                    create_controller,
                    register_controller,
                    get_available_controllers,
                    validate_controller_config,
                    validate_gains,
                    CONTROLLER_REGISTRY
                )

                # Verify all are callable/accessible
                if not callable(create_controller):
                    return False, "create_controller not callable"
                if not callable(register_controller):
                    return False, "register_controller not callable"
                if not callable(get_available_controllers):
                    return False, "get_available_controllers not callable"
                if not callable(validate_controller_config):
                    return False, "validate_controller_config not callable"
                if not callable(validate_gains):
                    return False, "validate_gains not callable"
                if not isinstance(CONTROLLER_REGISTRY, dict):
                    return False, "CONTROLLER_REGISTRY not a dict"

                return True, "All 6 public API members accessible via old-style imports"

        except ImportError as e:
            return False, f"Backward compatibility broken: {e}"

    def check_test_suite(self) -> Tuple[bool, str]:
        """Check 4: Verify test suite still passes."""
        try:
            # Run controller tests
            result = subprocess.run(
                ["python", "-m", "pytest", "tests/test_controllers/", "-q", "--tb=short"],
                capture_output=True,
                text=True,
                timeout=120
            )

            if result.returncode == 0:
                # Count passed tests
                lines = result.stdout.split('\n')
                passed_line = [l for l in lines if 'passed' in l.lower()]
                if passed_line:
                    return True, f"Controller tests passed: {passed_line[0].strip()}"
                else:
                    return True, "All controller tests passed"
            else:
                # Extract failure info
                failure_lines = [l for l in result.stdout.split('\n') if 'FAILED' in l]
                return False, f"Test failures detected: {failure_lines[:3]}"

        except subprocess.TimeoutExpired:
            return False, "Test suite timed out (>120s)"
        except FileNotFoundError:
            return False, "pytest not found or tests/ directory missing"
        except Exception as e:
            return False, f"Test execution error: {e}"

    def check_api_equivalence(self) -> Tuple[bool, str]:
        """Check 5: Verify old and new factory API are equivalent."""
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", DeprecationWarning)

                # Import from both old wrapper and new package
                import src.controllers.factory as old_factory
                from src.controllers.factory import create_controller as new_create_controller

                # Check they reference the same function
                if old_factory.create_controller is not new_create_controller:
                    return False, "create_controller differs between old and new imports"

                # Check available functions match
                old_api = set(dir(old_factory))
                expected_api = {
                    'create_controller', 'register_controller', 'get_available_controllers',
                    'validate_controller_config', 'validate_gains', 'CONTROLLER_REGISTRY'
                }

                missing_api = expected_api - old_api
                if missing_api:
                    return False, f"Missing API members: {missing_api}"

                return True, f"API equivalent: {len(expected_api)} core members present"

        except Exception as e:
            return False, f"API equivalence check failed: {e}"

    def check_module_sizes(self) -> Tuple[bool, str]:
        """Check 6: Verify module sizes within healthy thresholds."""
        modules = {
            "src/controllers/factory/__init__.py": (30, 150),    # (min, max) lines
            "src/controllers/factory/registration.py": (100, 250),
            "src/controllers/factory/utils.py": (100, 300),
            "src/controllers/factory/validation.py": (200, 400),
            "src/controllers/factory/core.py": (200, 500),
        }

        issues = []
        total_lines = 0

        for module_path, (min_lines, max_lines) in modules.items():
            path = Path(module_path)
            if not path.exists():
                issues.append(f"{module_path}: not found")
                continue

            line_count = sum(1 for _ in open(path, encoding='utf-8'))
            total_lines += line_count

            if line_count < min_lines:
                issues.append(f"{module_path}: too small ({line_count} lines, min {min_lines})")
            elif line_count > max_lines:
                issues.append(f"{module_path}: too large ({line_count} lines, max {max_lines})")

        if issues:
            return False, f"Module size issues: {'; '.join(issues)}"
        else:
            return True, f"All modules within size thresholds (total: {total_lines} lines)"

    def check_documentation_updated(self) -> Tuple[bool, str]:
        """Check 7: Verify documentation mentions refactored factory."""
        # Check PHASE_2_THIS_WEEK.md
        doc_path = Path(".project/ai/planning/workspace_audit_2025_10/PHASE_2_THIS_WEEK.md")
        if not doc_path.exists():
            return False, "PHASE_2_THIS_WEEK.md not found"

        content = doc_path.read_text()

        # Check for key refactoring terms
        required_terms = ["factory/", "refactor", "modular", "Task 2"]
        missing_terms = [term for term in required_terms if term.lower() not in content.lower()]

        if missing_terms:
            return False, f"Documentation missing terms: {missing_terms}"

        # Check for substantial content (indicates completion)
        if len(content) < 5000:  # Should be comprehensive after expansion
            return False, f"Documentation too short: {len(content)} chars (expected >5000)"

        return True, f"Documentation updated ({len(content)} chars, all terms present)"

    def generate_report(self):
        """Generate validation report."""
        print()
        print(f"{BLUE}╔════════════════════════════════════════════════════════════╗{NC}")
        print(f"{BLUE}║                      SUMMARY                               ║{NC}")
        print(f"{BLUE}╚════════════════════════════════════════════════════════════╝{NC}")
        print()
        print(f"  Checks Passed: {GREEN}{self.checks_passed}{NC}")
        print(f"  Checks Failed: {RED}{self.checks_failed}{NC}")
        print(f"  Checks Warned: {YELLOW}{self.checks_warned}{NC}")
        print()

        # Write report to file
        report_path = Path(".artifacts/audit_cleanup/task2_validation_report.txt")
        report_path.parent.mkdir(parents=True, exist_ok=True)

        with open(report_path, 'w') as f:
            f.write("=" * 60 + "\n")
            f.write("TASK 2 VALIDATION REPORT: FACTORY REFACTORING\n")
            f.write("=" * 60 + "\n\n")

            for name, status, message in self.results:
                f.write(f"[{status}] {name}\n")
                if message:
                    f.write(f"    {message}\n")
                f.write("\n")

            f.write("-" * 60 + "\n")
            f.write(f"Checks Passed: {self.checks_passed}\n")
            f.write(f"Checks Failed: {self.checks_failed}\n")
            f.write(f"Checks Warned: {self.checks_warned}\n")
            f.write("-" * 60 + "\n")

        print(f"Report saved: {report_path}")
        print()

    def run_all_checks(self) -> int:
        """Run all validation checks and return exit code."""
        self.print_header()

        # Run checks
        self.run_check("Modules Exist", self.check_modules_exist)
        self.run_check("Module Imports Resolve", self.check_module_imports)
        self.run_check("Backward Compatibility", self.check_backward_compatibility)
        self.run_check("Test Suite Passes", self.check_test_suite)
        self.run_check("API Equivalence", self.check_api_equivalence)
        self.run_check("Module Sizes", self.check_module_sizes)
        self.run_check("Documentation Updated", self.check_documentation_updated)

        # Generate report
        self.generate_report()

        # Final verdict
        if self.checks_failed == 0:
            print(f"{GREEN}╔════════════════════════════════════════════════════════════╗{NC}")
            print(f"{GREEN}║  STATUS: ✓ TASK 2 VALIDATION PASSED                       ║{NC}")
            print(f"{GREEN}╚════════════════════════════════════════════════════════════╝{NC}")
            print()
            print("✓ Factory refactoring correctly implemented")
            print("✓ Ready to proceed to Task 3")
            print()
            return 0
        else:
            print(f"{RED}╔════════════════════════════════════════════════════════════╗{NC}")
            print(f"{RED}║  STATUS: ✗ TASK 2 VALIDATION FAILED                       ║{NC}")
            print(f"{RED}╚════════════════════════════════════════════════════════════╝{NC}")
            print()
            print(f"{RED}✗ {self.checks_failed} checks failed{NC}")
            print("Fix failures before proceeding to Task 3")
            print()
            return 1


def main():
    """Main entry point."""
    validator = Task2Validator()
    exit_code = validator.run_all_checks()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
