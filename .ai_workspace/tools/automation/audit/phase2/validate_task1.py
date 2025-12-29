#!/usr/bin/env python3
"""
Validation Script for Task 1: Optimizer Deprecation

Purpose: Automated validation that src.optimizer deprecation is correctly implemented
Usage: python .ai_workspace/dev_tools/audit/phase2/validate_task1.py

Checks:
1. Deprecation warnings fire on import
2. Backward compatibility maintained
3. New location works correctly
4. API equivalence (old == new)
5. Test suite still passes
6. Documentation updated

Exit Codes:
  0 - All checks passed
  1 - One or more checks failed
"""

import sys
import warnings
import subprocess
import importlib
from pathlib import Path
from typing import Tuple, List

# ANSI color codes
GREEN = '\033[0;32m'
RED = '\033[0;31m'
YELLOW = '\033[1;33m'
BLUE = '\033[0;34m'
NC = '\033[0m'  # No Color


class Task1Validator:
    """Validator for optimizer deprecation (Task 1)."""

    def __init__(self):
        self.checks_passed = 0
        self.checks_failed = 0
        self.checks_warned = 0
        self.results = []

    def print_header(self):
        """Print validation header."""
        print(f"{BLUE}╔════════════════════════════════════════════════════════════╗{NC}")
        print(f"{BLUE}║     TASK 1 VALIDATION: OPTIMIZER DEPRECATION              ║{NC}")
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

    def check_deprecation_warning(self) -> Tuple[bool, str]:
        """Check 1: Verify deprecation warning fires on import."""
        # Capture warnings
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always", DeprecationWarning)

            # Force reload to ensure warning fires
            if "src.optimizer" in sys.modules:
                del sys.modules["src.optimizer"]

            # Import and check for warning
            import src.optimizer

            # Check if any DeprecationWarning was raised
            deprecation_warnings = [warning for warning in w
                                    if issubclass(warning.category, DeprecationWarning)]

            if deprecation_warnings:
                warning_msg = str(deprecation_warnings[0].message)
                if "src.optimizer" in warning_msg and "deprecated" in warning_msg.lower():
                    return True, f"Warning message: {warning_msg[:80]}..."
                else:
                    return False, f"Warning exists but message unclear: {warning_msg[:80]}"
            else:
                return False, "No DeprecationWarning detected on import"

    def check_backward_compatibility(self) -> Tuple[bool, str]:
        """Check 2: Verify old imports still work."""
        try:
            # Suppress warnings for this test
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", DeprecationWarning)

                # Test old import path
                from src.optimizer.pso_optimizer import PSOTuner

                # Verify it's a class
                if not isinstance(PSOTuner, type):
                    return False, "PSOTuner is not a class"

                # Check for basic expected methods
                expected_methods = ["optimize", "__init__"]
                missing_methods = [m for m in expected_methods if not hasattr(PSOTuner, m)]

                if missing_methods:
                    return False, f"Missing expected methods: {missing_methods}"

                return True, f"PSOTuner class: {PSOTuner.__name__}"

        except ImportError as e:
            return False, f"Import failed: {e}"

    def check_new_location_works(self) -> Tuple[bool, str]:
        """Check 3: Verify new import location works."""
        try:
            from src.optimization.algorithms.pso_optimizer import PSOTuner

            if not isinstance(PSOTuner, type):
                return False, "PSOTuner is not a class"

            return True, f"PSOTuner class: {PSOTuner.__name__}"

        except ImportError as e:
            return False, f"New location import failed: {e}"

    def check_api_equivalence(self) -> Tuple[bool, str]:
        """Check 4: Verify old and new imports reference same class."""
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", DeprecationWarning)

                from src.optimizer.pso_optimizer import PSOTuner as OldPSO
                from src.optimization.algorithms.pso_optimizer import PSOTuner as NewPSO

                # Check if they're the same object
                if OldPSO is not NewPSO:
                    return False, "Old and new imports reference DIFFERENT classes"

                # Check API equivalence
                old_methods = set(dir(OldPSO))
                new_methods = set(dir(NewPSO))

                if old_methods == new_methods:
                    return True, f"Identical APIs: {len(old_methods)} methods/attributes"
                else:
                    diff_old = old_methods - new_methods
                    diff_new = new_methods - old_methods
                    return False, f"API mismatch - Old only: {diff_old}, New only: {diff_new}"

        except Exception as e:
            return False, f"API equivalence check failed: {e}"

    def check_test_suite(self) -> Tuple[bool, str]:
        """Check 5: Verify test suite still passes."""
        try:
            # Run pytest on optimizer tests
            result = subprocess.run(
                ["python", "-m", "pytest", "tests/test_optimizer/", "-q", "--tb=short"],
                capture_output=True,
                text=True,
                timeout=60
            )

            if result.returncode == 0:
                # Count passed tests
                lines = result.stdout.split('\n')
                passed_line = [l for l in lines if 'passed' in l.lower()]
                if passed_line:
                    return True, f"Tests passed: {passed_line[0].strip()}"
                else:
                    return True, "All tests passed"
            else:
                # Extract failure info
                failure_lines = [l for l in result.stdout.split('\n') if 'FAILED' in l]
                return False, f"Test failures: {failure_lines[:3]}"

        except subprocess.TimeoutExpired:
            return False, "Test suite timed out (>60s)"
        except FileNotFoundError:
            return False, "pytest not found or tests/ directory missing"
        except Exception as e:
            return False, f"Test execution error: {e}"

    def check_migration_guide_exists(self) -> Tuple[bool, str]:
        """Check 6: Verify migration guide created."""
        guide_path = Path("docs/migration/optimizer_deprecation.md")

        if not guide_path.exists():
            return False, f"Migration guide not found: {guide_path}"

        # Check file has content
        content = guide_path.read_text()
        if len(content) < 100:
            return False, f"Migration guide too short: {len(content)} bytes"

        # Check for key sections
        required_sections = ["Migration", "src.optimizer", "src.optimization"]
        missing_sections = [s for s in required_sections if s not in content]

        if missing_sections:
            return False, f"Missing sections in guide: {missing_sections}"

        return True, f"Migration guide exists: {len(content)} bytes"

    def check_documentation_updated(self) -> Tuple[bool, str]:
        """Check 7: Verify documentation references updated."""
        # Check README.md
        readme_path = Path("README.md")
        if not readme_path.exists():
            return False, "README.md not found"

        readme_content = readme_path.read_text()

        # Count references to old vs new
        old_refs = readme_content.count("src.optimizer")
        new_refs = readme_content.count("src.optimization")

        if old_refs > 0:
            # Check if these are in deprecation warnings or migration guide
            # (acceptable context)
            if "deprecated" in readme_content.lower() or "migration" in readme_content.lower():
                return True, f"Old refs: {old_refs} (in deprecation context), New refs: {new_refs}"
            else:
                return False, f"README still has {old_refs} non-deprecated old refs"
        else:
            return True, f"README clean: {new_refs} new refs, 0 old refs"

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
        report_path = Path(".artifacts/audit_cleanup/task1_validation_report.txt")
        report_path.parent.mkdir(parents=True, exist_ok=True)

        with open(report_path, 'w') as f:
            f.write("=" * 60 + "\n")
            f.write("TASK 1 VALIDATION REPORT: OPTIMIZER DEPRECATION\n")
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
        self.run_check("Deprecation Warning Fires", self.check_deprecation_warning)
        self.run_check("Backward Compatibility", self.check_backward_compatibility)
        self.run_check("New Location Works", self.check_new_location_works)
        self.run_check("API Equivalence", self.check_api_equivalence)
        self.run_check("Test Suite Passes", self.check_test_suite)
        self.run_check("Migration Guide Exists", self.check_migration_guide_exists)
        self.run_check("Documentation Updated", self.check_documentation_updated)

        # Generate report
        self.generate_report()

        # Final verdict
        if self.checks_failed == 0:
            print(f"{GREEN}╔════════════════════════════════════════════════════════════╗{NC}")
            print(f"{GREEN}║  STATUS: ✓ TASK 1 VALIDATION PASSED                       ║{NC}")
            print(f"{GREEN}╚════════════════════════════════════════════════════════════╝{NC}")
            print()
            print("✓ Optimizer deprecation correctly implemented")
            print("✓ Ready to proceed to Task 2")
            print()
            return 0
        else:
            print(f"{RED}╔════════════════════════════════════════════════════════════╗{NC}")
            print(f"{RED}║  STATUS: ✗ TASK 1 VALIDATION FAILED                       ║{NC}")
            print(f"{RED}╚════════════════════════════════════════════════════════════╝{NC}")
            print()
            print(f"{RED}✗ {self.checks_failed} checks failed{NC}")
            print("Fix failures before proceeding to Task 2")
            print()
            return 1


def main():
    """Main entry point."""
    validator = Task1Validator()
    exit_code = validator.run_all_checks()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
