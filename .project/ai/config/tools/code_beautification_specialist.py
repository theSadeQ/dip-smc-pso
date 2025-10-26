#==========================================================================================\\\
#========================== agents/code_beautification_specialist.py ===================\\\
#==========================================================================================\\\

"""Code Beautification & Directory Organization Specialist Agent.

This agent systematically enforces coding standards, directory organization,
and implements the distinctive ASCII header style across the DIP SMC PSO codebase.
"""

import os
import re
import json
import logging
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass, asdict
from datetime import datetime

logger = logging.getLogger(__name__)


@dataclass
class StyleViolation:
    """Represents a code style violation found during audit."""
    file_path: str
    violation_type: str
    line_number: Optional[int]
    description: str
    severity: str  # 'critical', 'major', 'minor'


@dataclass
class DirectoryAuditResult:
    """Results from directory structure audit."""
    misplaced_files: List[str]
    missing_test_files: List[str]
    naming_violations: List[str]
    orphaned_files: List[str]


@dataclass
class BeautificationResults:
    """Results from code beautification process."""
    files_processed: int
    headers_added: int
    imports_reorganized: int
    type_hints_added: int
    violations_fixed: int
    errors: List[str]


class CodeBeautificationSpecialist:
    """Specialist agent for code beautification and directory organization."""

    def __init__(self, root_path: Path):
        """Initialize the beautification specialist.

        Args:
            root_path: Root directory of the DIP SMC PSO project
        """
        self.root_path = Path(root_path)
        self.src_path = self.root_path / "src"
        self.tests_path = self.root_path / "tests"

        # Expected directory structure
        self.expected_structure = {
            "src": {
                "controllers": ["classic_smc.py", "sta_smc.py", "adaptive_smc.py",
                              "hybrid_adaptive_sta_smc.py", "swing_up_smc.py",
                              "mpc_controller.py", "factory.py"],
                "core": ["dynamics.py", "dynamics_full.py", "simulation_runner.py",
                        "simulation_context.py", "vector_sim.py"],
                "plant": {"models": {"simplified": [], "full": [], "lowrank": []},
                         "configurations": [], "core": []},
                "optimizer": ["pso_optimizer.py"],
                "utils": {"validation": [], "control": [], "monitoring": [],
                         "visualization": [], "analysis": [], "types": [],
                         "reproducibility": [], "development": []},
                "hil": ["plant_server.py", "controller_client.py"]
            },
            "tests": {
                "test_controllers": [],
                "test_core": [],
                "test_integration": [],
                "test_benchmarks": []
            }
        }

    def generate_ascii_header(self, file_path: Path) -> str:
        """Generate ASCII header for a Python file.

        Args:
            file_path: Path to the Python file

        Returns:
            ASCII header string with proper formatting
        """
        # Calculate relative path from project root
        try:
            rel_path = file_path.relative_to(self.root_path)
        except ValueError:
            # File is outside project root, use just filename
            rel_path = file_path.name

        # Convert to string and ensure .py extension is included
        path_str = str(rel_path).replace("\\", "/")
        if not path_str.endswith(".py"):
            path_str += ".py"

        # Calculate padding for centering
        total_width = 90
        border_chars = 2  # Two `=` on each side of content
        backslash_chars = 3  # `\\\` at the end
        available_width = total_width - border_chars - len(path_str) - backslash_chars

        left_padding = available_width // 2
        right_padding = available_width - left_padding

        # Generate header lines
        top_line = "=" * (total_width - 3) + "\\\\\\"
        middle_line = "=" * left_padding + " " + path_str + " " + "=" * right_padding + "\\\\\\"
        bottom_line = "=" * (total_width - 3) + "\\\\\\"

        return f"#{top_line}\n#{middle_line}\n#{bottom_line}\n"

    def audit_directory_structure(self) -> DirectoryAuditResult:
        """Audit the current directory structure against expected layout.

        Returns:
            Directory audit results with violations and recommendations
        """
        misplaced_files = []
        missing_test_files = []
        naming_violations = []
        orphaned_files = []

        # Check for Python files in src/
        if self.src_path.exists():
            for py_file in self.src_path.rglob("*.py"):
                rel_path = py_file.relative_to(self.src_path)

                # Check naming conventions
                if not self._is_valid_python_filename(py_file.name):
                    naming_violations.append(str(py_file))

                # Check if corresponding test file exists
                test_file_path = self._get_expected_test_path(py_file)
                if not test_file_path.exists():
                    missing_test_files.append(str(py_file))

        # Check for orphaned files in root
        for item in self.root_path.iterdir():
            if item.is_file() and item.suffix == ".py":
                if item.name not in ["simulate.py", "streamlit_app.py", "run_tests.py"]:
                    orphaned_files.append(str(item))

        return DirectoryAuditResult(
            misplaced_files=misplaced_files,
            missing_test_files=missing_test_files,
            naming_violations=naming_violations,
            orphaned_files=orphaned_files
        )

    def audit_code_style(self) -> List[StyleViolation]:
        """Audit code style across all Python files.

        Returns:
            List of style violations found
        """
        violations = []

        for py_file in self.root_path.rglob("*.py"):
            violations.extend(self._audit_file_style(py_file))

        return violations

    def beautify_file(self, file_path: Path) -> Dict[str, any]:
        """Beautify a single Python file.

        Args:
            file_path: Path to the Python file to beautify

        Returns:
            Dictionary with beautification results
        """
        if not file_path.exists() or file_path.suffix != ".py":
            return {"success": False, "error": "File does not exist or is not a Python file"}

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            original_content = content
            changes_made = []

            # Add ASCII header if missing
            if not self._has_ascii_header(content):
                header = self.generate_ascii_header(file_path)
                content = header + "\n" + content
                changes_made.append("Added ASCII header")

            # Organize imports
            if self._needs_import_organization(content):
                content = self._organize_imports(content)
                changes_made.append("Organized imports")

            # Fix line width violations
            content = self._fix_line_width(content)
            if content != original_content:
                changes_made.append("Fixed line width violations")

            # Write back if changes were made
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)

            return {
                "success": True,
                "changes_made": changes_made,
                "file_path": str(file_path)
            }

        except Exception as e:
            logger.error(f"Error beautifying {file_path}: {e}")
            return {"success": False, "error": str(e)}

    def beautify_repository(self) -> BeautificationResults:
        """Beautify the entire repository.

        Returns:
            Comprehensive beautification results
        """
        files_processed = 0
        headers_added = 0
        imports_reorganized = 0
        type_hints_added = 0
        violations_fixed = 0
        errors = []

        for py_file in self.root_path.rglob("*.py"):
            try:
                result = self.beautify_file(py_file)
                files_processed += 1

                if result["success"]:
                    changes = result.get("changes_made", [])
                    if "Added ASCII header" in changes:
                        headers_added += 1
                    if "Organized imports" in changes:
                        imports_reorganized += 1
                    violations_fixed += len(changes)
                else:
                    errors.append(f"{py_file}: {result.get('error', 'Unknown error')}")

            except Exception as e:
                errors.append(f"{py_file}: {str(e)}")

        return BeautificationResults(
            files_processed=files_processed,
            headers_added=headers_added,
            imports_reorganized=imports_reorganized,
            type_hints_added=type_hints_added,
            violations_fixed=violations_fixed,
            errors=errors
        )

    def generate_audit_report(self, output_path: Path) -> Dict[str, any]:
        """Generate comprehensive audit report.

        Args:
            output_path: Path to save the audit report

        Returns:
            Summary of audit findings
        """
        # Perform audits
        directory_audit = self.audit_directory_structure()
        style_violations = self.audit_code_style()

        # Generate report
        report = {
            "timestamp": datetime.now().isoformat(),
            "project_root": str(self.root_path),
            "directory_audit": asdict(directory_audit),
            "style_violations": [asdict(v) for v in style_violations],
            "summary": {
                "total_style_violations": len(style_violations),
                "critical_violations": len([v for v in style_violations if v.severity == "critical"]),
                "misplaced_files": len(directory_audit.misplaced_files),
                "missing_test_files": len(directory_audit.missing_test_files)
            }
        }

        # Save report
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)

        return report["summary"]

    def _has_ascii_header(self, content: str) -> bool:
        """Check if file content has proper ASCII header."""
        lines = content.split('\n')
        if len(lines) < 3:
            return False

        # Check for pattern of three lines starting with # and containing ===
        header_pattern = re.compile(r'^#=+\\\\\\$')
        return all(header_pattern.match(lines[i]) for i in range(3))

    def _is_valid_python_filename(self, filename: str) -> bool:
        """Check if filename follows Python naming conventions."""
        if not filename.endswith('.py'):
            return False

        name = filename[:-3]  # Remove .py extension
        return name.islower() and '_' in name or name.isidentifier()

    def _get_expected_test_path(self, src_file: Path) -> Path:
        """Get expected path for test file corresponding to source file."""
        rel_path = src_file.relative_to(self.src_path)
        test_filename = f"test_{src_file.name}"

        # Map src directories to test directories
        if rel_path.parts[0] == "controllers":
            return self.tests_path / "test_controllers" / test_filename
        elif rel_path.parts[0] == "core":
            return self.tests_path / "test_core" / test_filename
        else:
            return self.tests_path / test_filename

    def _audit_file_style(self, file_path: Path) -> List[StyleViolation]:
        """Audit style for a single file."""
        violations = []

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            lines = content.split('\n')

            # Check for ASCII header
            if not self._has_ascii_header(content):
                violations.append(StyleViolation(
                    file_path=str(file_path),
                    violation_type="missing_ascii_header",
                    line_number=1,
                    description="Missing ASCII header",
                    severity="major"
                ))

            # Check line width
            for i, line in enumerate(lines, 1):
                if len(line) > 90:
                    violations.append(StyleViolation(
                        file_path=str(file_path),
                        violation_type="line_too_long",
                        line_number=i,
                        description=f"Line exceeds 90 characters ({len(line)} chars)",
                        severity="minor"
                    ))

        except Exception as e:
            violations.append(StyleViolation(
                file_path=str(file_path),
                violation_type="file_read_error",
                line_number=None,
                description=f"Could not read file: {e}",
                severity="critical"
            ))

        return violations

    def _needs_import_organization(self, content: str) -> bool:
        """Check if imports need reorganization."""
        # Simple heuristic: if imports are not grouped properly
        lines = content.split('\n')
        import_lines = [i for i, line in enumerate(lines) if line.strip().startswith(('import ', 'from '))]

        if len(import_lines) < 2:
            return False

        # Check if imports are grouped (standard, third-party, local)
        # This is a simplified check
        return True  # For now, always reorganize if imports exist

    def _organize_imports(self, content: str) -> str:
        """Organize imports according to PEP 8."""
        # This is a simplified implementation
        # In practice, you might want to use isort or similar tools
        lines = content.split('\n')

        # Find import lines
        import_lines = []
        other_lines = []

        for line in lines:
            if line.strip().startswith(('import ', 'from ')) and not line.strip().startswith('#'):
                import_lines.append(line)
            else:
                other_lines.append(line)

        # Sort imports (simplified)
        import_lines.sort()

        # Reconstruct content
        # Find where imports should go (after header and docstring)
        insert_point = 0
        for i, line in enumerate(other_lines):
            if line.strip() and not line.startswith('#') and '"""' not in line:
                insert_point = i
                break

        # Insert organized imports
        result_lines = other_lines[:insert_point] + import_lines + other_lines[insert_point:]
        return '\n'.join(result_lines)

    def _fix_line_width(self, content: str) -> str:
        """Fix lines that exceed 90 character limit."""
        lines = content.split('\n')
        fixed_lines = []

        for line in lines:
            if len(line) <= 90:
                fixed_lines.append(line)
            else:
                # Simple line breaking (can be improved)
                if ' ' in line:
                    # Try to break at a reasonable point
                    break_point = line.rfind(' ', 0, 88)
                    if break_point > 60:  # Don't break too early
                        fixed_lines.append(line[:break_point])
                        fixed_lines.append('    ' + line[break_point:].lstrip())
                    else:
                        fixed_lines.append(line)  # Keep as is if can't break nicely
                else:
                    fixed_lines.append(line)  # Keep as is if no spaces

        return '\n'.join(fixed_lines)


def deploy_code_beautification_specialist(root_path: str = ".") -> Dict[str, any]:
    """Deploy the code beautification specialist agent.

    Args:
        root_path: Root path of the DIP SMC PSO project

    Returns:
        Deployment results and summary
    """
    specialist = CodeBeautificationSpecialist(Path(root_path))

    # Generate audit report
    audit_report_path = Path(root_path) / "beautification" / "audit_report.json"
    audit_summary = specialist.generate_audit_report(audit_report_path)

    # Perform beautification
    beautification_results = specialist.beautify_repository()

    # Save beautification results
    results_path = Path(root_path) / "beautification" / "beautification_results.json"
    results_path.parent.mkdir(parents=True, exist_ok=True)
    with open(results_path, 'w', encoding='utf-8') as f:
        json.dump(asdict(beautification_results), f, indent=2)

    return {
        "audit_summary": audit_summary,
        "beautification_results": asdict(beautification_results),
        "status": "completed",
        "timestamp": datetime.now().isoformat()
    }


if __name__ == "__main__":
    # Run beautification specialist
    result = deploy_code_beautification_specialist()
    print(json.dumps(result, indent=2))