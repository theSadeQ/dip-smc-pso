#======================================================================================\\\
#======================== scripts/test_collection_validator.py ========================\\\
#======================================================================================\\\

"""
Robust test collection validation and infrastructure resilience checker.

This module provides comprehensive validation of test collection infrastructure,
encoding issue detection, and system health monitoring for the DIP-SMC-PSO project.
"""

import os
import sys
import json
import subprocess
import time
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass, asdict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class TestCollectionReport:
    """Comprehensive test collection analysis report."""
    total_tests_collected: int
    collection_time_seconds: float
    encoding_issues: List[Dict[str, str]]
    bom_files: List[str]
    collection_errors: List[str]
    failed_modules: List[str]
    infrastructure_health: Dict[str, Any]
    recommendation: str
    timestamp: str


class TestCollectionValidator:
    """Robust test collection validation with infrastructure resilience."""

    def __init__(self, project_root: Optional[Path] = None):
        self.project_root = project_root or Path.cwd()
        self.test_dir = self.project_root / "tests"

    def validate_encoding_integrity(self) -> Tuple[List[str], List[Dict[str, str]]]:
        """Validate encoding integrity across all Python files."""
        bom_files = []
        encoding_issues = []

        logger.info("Scanning for encoding issues...")

        for py_file in self.project_root.rglob("*.py"):
            try:
                # Check for BOM
                with open(py_file, 'rb') as f:
                    raw_content = f.read()
                    if raw_content.startswith(b'\xef\xbb\xbf'):
                        bom_files.append(str(py_file.relative_to(self.project_root)))

                # Validate UTF-8 decoding
                with open(py_file, 'r', encoding='utf-8') as f:
                    f.read()

            except UnicodeDecodeError as e:
                encoding_issues.append({
                    'file': str(py_file.relative_to(self.project_root)),
                    'error': str(e),
                    'error_type': 'UnicodeDecodeError'
                })
            except Exception as e:
                encoding_issues.append({
                    'file': str(py_file.relative_to(self.project_root)),
                    'error': str(e),
                    'error_type': type(e).__name__
                })

        return bom_files, encoding_issues

    def collect_tests_with_resilience(self) -> Tuple[int, float, List[str], List[str]]:
        """Collect tests with comprehensive error handling and resilience."""
        start_time = time.time()
        collection_errors = []
        failed_modules = []

        try:
            # Run pytest collection with detailed output
            result = subprocess.run(
                [sys.executable, "-m", "pytest", "--collect-only", "--tb=short"],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=60  # 1 minute timeout
            )

            collection_time = time.time() - start_time

            # Parse output for test count
            output_lines = result.stdout.split('\n')
            total_tests = 0

            for line in output_lines:
                if "tests collected" in line:
                    try:
                        total_tests = int(line.split()[0])
                        break
                    except (ValueError, IndexError):
                        continue

            # Parse errors
            if result.stderr:
                collection_errors.extend(result.stderr.split('\n'))

            # Check for import failures
            for line in output_lines:
                if "ERRORS" in line or "ImportError" in line or "ModuleNotFoundError" in line:
                    failed_modules.append(line.strip())

            return total_tests, collection_time, collection_errors, failed_modules

        except subprocess.TimeoutExpired:
            collection_time = time.time() - start_time
            collection_errors.append("Test collection timed out after 60 seconds")
            return 0, collection_time, collection_errors, failed_modules

        except Exception as e:
            collection_time = time.time() - start_time
            collection_errors.append(f"Unexpected error during collection: {str(e)}")
            return 0, collection_time, collection_errors, failed_modules

    def assess_infrastructure_health(self) -> Dict[str, Any]:
        """Comprehensive infrastructure health assessment."""
        health = {
            'test_directory_exists': self.test_dir.exists(),
            'conftest_files': [],
            'pytest_config': None,
            'import_paths': [],
            'dependency_status': {},
            'python_version': sys.version,
            'test_structure_score': 0.0
        }

        # Check conftest.py files
        for conftest in self.project_root.rglob("conftest.py"):
            health['conftest_files'].append(str(conftest.relative_to(self.project_root)))

        # Check pytest configuration
        for config_file in ['pytest.ini', 'pyproject.toml', 'setup.cfg']:
            config_path = self.project_root / config_file
            if config_path.exists():
                health['pytest_config'] = config_file
                break

        # Check critical imports
        critical_imports = ['pytest', 'numpy', 'scipy', 'hypothesis']
        for module in critical_imports:
            try:
                __import__(module)
                health['dependency_status'][module] = 'available'
            except ImportError:
                health['dependency_status'][module] = 'missing'

        # Assess test structure
        if self.test_dir.exists():
            test_files = list(self.test_dir.rglob("test_*.py"))
            src_files = list((self.project_root / "src").rglob("*.py")) if (self.project_root / "src").exists() else []

            if src_files:
                health['test_structure_score'] = min(len(test_files) / len(src_files), 1.0)
            else:
                health['test_structure_score'] = 0.0

        return health

    def generate_recommendations(self,
                                bom_files: List[str],
                                encoding_issues: List[Dict[str, str]],
                                collection_errors: List[str],
                                infrastructure_health: Dict[str, Any]) -> str:
        """Generate actionable recommendations based on validation results."""
        recommendations = []

        if bom_files:
            recommendations.append(f"Remove BOM from {len(bom_files)} files")

        if encoding_issues:
            recommendations.append(f"Fix encoding issues in {len(encoding_issues)} files")

        if collection_errors:
            recommendations.append(f"Resolve {len(collection_errors)} collection errors")

        if not infrastructure_health['test_directory_exists']:
            recommendations.append("Create tests/ directory")

        if infrastructure_health['dependency_status'].get('pytest') != 'available':
            recommendations.append("Install pytest dependency")

        if infrastructure_health['test_structure_score'] < 0.5:
            recommendations.append("Improve test coverage structure")

        if not recommendations:
            return "Test collection infrastructure is healthy and resilient"

        return "Recommendations: " + ", ".join(recommendations)

    def run_comprehensive_validation(self) -> TestCollectionReport:
        """Run comprehensive test collection validation."""
        logger.info("Starting comprehensive test collection validation...")

        # Encoding validation
        bom_files, encoding_issues = self.validate_encoding_integrity()
        logger.info(f"Found {len(bom_files)} BOM files, {len(encoding_issues)} encoding issues")

        # Test collection
        total_tests, collection_time, collection_errors, failed_modules = self.collect_tests_with_resilience()
        logger.info(f"Collected {total_tests} tests in {collection_time:.2f}s")

        # Infrastructure health
        infrastructure_health = self.assess_infrastructure_health()

        # Generate recommendations
        recommendation = self.generate_recommendations(
            bom_files, encoding_issues, collection_errors, infrastructure_health
        )

        report = TestCollectionReport(
            total_tests_collected=total_tests,
            collection_time_seconds=collection_time,
            encoding_issues=encoding_issues,
            bom_files=bom_files,
            collection_errors=[e for e in collection_errors if e.strip()],
            failed_modules=failed_modules,
            infrastructure_health=infrastructure_health,
            recommendation=recommendation,
            timestamp=time.strftime("%Y-%m-%d %H:%M:%S")
        )

        logger.info(f"Validation complete: {recommendation}")
        return report


def main():
    """Main entry point for test collection validation."""
    validator = TestCollectionValidator()
    report = validator.run_comprehensive_validation()

    # Save report
    report_path = Path("validation") / "test_collection_validation_report.json"
    report_path.parent.mkdir(exist_ok=True)

    with open(report_path, 'w') as f:
        json.dump(asdict(report), f, indent=2)

    print(f"\nTest Collection Validation Report")
    print(f"{'='*50}")
    print(f"Total Tests Collected: {report.total_tests_collected}")
    print(f"Collection Time: {report.collection_time_seconds:.2f}s")
    print(f"BOM Files: {len(report.bom_files)}")
    print(f"Encoding Issues: {len(report.encoding_issues)}")
    print(f"Collection Errors: {len(report.collection_errors)}")
    print(f"Infrastructure Health Score: {report.infrastructure_health.get('test_structure_score', 0):.2f}")
    print(f"\n{report.recommendation}")
    print(f"\nReport saved to: {report_path}")


if __name__ == "__main__":
    main()