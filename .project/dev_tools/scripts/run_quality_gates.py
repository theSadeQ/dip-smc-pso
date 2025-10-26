#======================================================================================\\\
#============================ scripts/run_quality_gates.py ============================\\\
#======================================================================================\\\

"""
Quality Gate Validation Framework
Comprehensive validation system for coverage targets and quality standards.
"""

import subprocess
import json
import sys
import os
from pathlib import Path
from typing import Dict, List, Any, Tuple
import argparse


class QualityGateValidator:
    """Ultimate Orchestrator quality gate validation system."""

    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path)
        self.results = {
            "validation_timestamp": "",
            "overall_status": "pending",
            "gates": {},
            "coverage_summary": {},
            "recommendations": []
        }

    def run_comprehensive_validation(self) -> Dict[str, Any]:
        """Execute all quality gates with failure tolerance."""
        print("🔵 Ultimate Orchestrator: Initiating Comprehensive Quality Gate Validation")

        # Gate 1: Infrastructure Health
        gate1_result = self._validate_infrastructure_health()
        self.results["gates"]["infrastructure_health"] = gate1_result

        # Gate 2: Safety-Critical Coverage (100% required)
        gate2_result = self._validate_safety_critical_coverage()
        self.results["gates"]["safety_critical_coverage"] = gate2_result

        # Gate 3: Critical Components Coverage (>=95% required)
        gate3_result = self._validate_critical_components_coverage()
        self.results["gates"]["critical_components_coverage"] = gate3_result

        # Gate 4: Overall Coverage (>=85% required)
        gate4_result = self._validate_overall_coverage()
        self.results["gates"]["overall_coverage"] = gate4_result

        # Gate 5: Theoretical Validation (mathematical properties)
        gate5_result = self._validate_theoretical_properties()
        self.results["gates"]["theoretical_validation"] = gate5_result

        # Gate 6: Performance Benchmarks
        gate6_result = self._validate_performance_benchmarks()
        self.results["gates"]["performance_validation"] = gate6_result

        # Calculate overall status
        self._calculate_overall_status()

        # Generate recommendations
        self._generate_recommendations()

        return self.results

    def _validate_infrastructure_health(self) -> Dict[str, Any]:
        """Validate test infrastructure health."""
        print("\n📊 Gate 1: Test Infrastructure Health Validation")

        result = {
            "gate_id": "infrastructure_health",
            "status": "unknown",
            "requirements_met": [],
            "requirements_failed": [],
            "details": {}
        }

        # Test collection validation
        try:
            collect_result = subprocess.run(
                ["python", "-m", "pytest", "--collect-only", "-q"],
                capture_output=True, text=True, timeout=60
            )

            if collect_result.returncode == 0:
                result["requirements_met"].append("Test collection operational")
                result["details"]["test_collection"] = "SUCCESS"
                print("  ✓ Test collection operational")
            else:
                result["requirements_failed"].append("Test collection failed")
                result["details"]["test_collection"] = f"FAILED: {collect_result.stderr[:200]}"
                print(f"  ✗ Test collection failed: {collect_result.stderr[:100]}")

        except subprocess.TimeoutExpired:
            result["requirements_failed"].append("Test collection timeout")
            result["details"]["test_collection"] = "TIMEOUT"
            print("  ✗ Test collection timeout")
        except Exception as e:
            result["requirements_failed"].append(f"Test collection error: {str(e)}")
            result["details"]["test_collection"] = f"ERROR: {str(e)}"
            print(f"  ✗ Test collection error: {str(e)}")

        # Coverage tool validation
        try:
            coverage_result = subprocess.run(
                ["python", "-m", "pytest", "--version"],
                capture_output=True, text=True, timeout=30
            )

            if coverage_result.returncode == 0:
                result["requirements_met"].append("Pytest available")
                result["details"]["pytest_available"] = "SUCCESS"
                print("  ✓ Pytest available")
            else:
                result["requirements_failed"].append("Pytest unavailable")
                result["details"]["pytest_available"] = "FAILED"
                print("  ✗ Pytest unavailable")

        except Exception as e:
            result["requirements_failed"].append(f"Pytest validation error: {str(e)}")
            result["details"]["pytest_available"] = f"ERROR: {str(e)}"
            print(f"  ✗ Pytest validation error: {str(e)}")

        # Set overall gate status
        if len(result["requirements_failed"]) == 0:
            result["status"] = "passed"
            print("  🟢 Infrastructure Health: PASSED")
        else:
            result["status"] = "failed"
            print("  🔴 Infrastructure Health: FAILED")

        return result

    def _validate_safety_critical_coverage(self) -> Dict[str, Any]:
        """Validate 100% coverage on safety-critical components."""
        print("\n🔴 Gate 2: Safety-Critical Coverage Validation (100% Required)")

        result = {
            "gate_id": "safety_critical_coverage",
            "status": "unknown",
            "coverage_target": 100.0,
            "coverage_achieved": 0.0,
            "modules_tested": [],
            "modules_failed": [],
            "details": {}
        }

        safety_critical_modules = [
            "tests/test_controllers/smc/core/",
            "tests/test_controllers/base/"
        ]

        for module in safety_critical_modules:
            if os.path.exists(module):
                try:
                    # Run coverage for specific safety-critical module
                    coverage_cmd = [
                        "python", "-m", "pytest", module,
                        "--cov=src/controllers/smc/core",
                        "--cov=src/controllers/base",
                        "--cov-report=json:safety_critical_coverage.json",
                        "--cov-fail-under=100",
                        "-x"  # Stop on first failure for safety-critical
                    ]

                    coverage_result = subprocess.run(
                        coverage_cmd, capture_output=True, text=True, timeout=120
                    )

                    if coverage_result.returncode == 0:
                        result["modules_tested"].append(module)
                        print(f"  ✓ {module}: 100% coverage achieved")
                    else:
                        result["modules_failed"].append(module)
                        print(f"  ✗ {module}: Coverage below 100%")

                except subprocess.TimeoutExpired:
                    result["modules_failed"].append(f"{module} (timeout)")
                    print(f"  ✗ {module}: Timeout")
                except Exception as e:
                    result["modules_failed"].append(f"{module} (error: {str(e)})")
                    print(f"  ✗ {module}: Error - {str(e)}")
            else:
                result["modules_failed"].append(f"{module} (missing)")
                print(f"  ✗ {module}: Directory missing")

        # Calculate overall safety-critical coverage
        if len(result["modules_failed"]) == 0 and len(result["modules_tested"]) > 0:
            result["status"] = "passed"
            result["coverage_achieved"] = 100.0
            print("  🟢 Safety-Critical Coverage: PASSED (100%)")
        else:
            result["status"] = "failed"
            result["coverage_achieved"] = 0.0  # Conservative estimate
            print("  🔴 Safety-Critical Coverage: FAILED")

        return result

    def _validate_critical_components_coverage(self) -> Dict[str, Any]:
        """Validate >=95% coverage on critical components."""
        print("\n🔵 Gate 3: Critical Components Coverage Validation (≥95% Required)")

        result = {
            "gate_id": "critical_components_coverage",
            "status": "unknown",
            "coverage_target": 95.0,
            "coverage_achieved": 0.0,
            "components": {},
            "details": {}
        }

        critical_components = {
            "controller_factory": {
                "test_path": "tests/test_controllers/factory/",
                "cov_path": "src/controllers/factory"
            },
            "optimization": {
                "test_path": "tests/test_optimization/",
                "cov_path": "src/optimizer"
            },
            "simulation_core": {
                "test_path": "tests/test_simulation/core/",
                "cov_path": "src/core"
            }
        }

        total_coverage = 0.0
        successful_components = 0

        for component_name, paths in critical_components.items():
            if os.path.exists(paths["test_path"]):
                try:
                    coverage_cmd = [
                        "python", "-m", "pytest", paths["test_path"],
                        f"--cov={paths['cov_path']}",
                        f"--cov-report=json:{component_name}_coverage.json",
                        "--cov-fail-under=95",
                        "-q"
                    ]

                    coverage_result = subprocess.run(
                        coverage_cmd, capture_output=True, text=True, timeout=180
                    )

                    if coverage_result.returncode == 0:
                        result["components"][component_name] = {"status": "passed", "coverage": 95.0}
                        total_coverage += 95.0
                        successful_components += 1
                        print(f"  ✓ {component_name}: ≥95% coverage achieved")
                    else:
                        result["components"][component_name] = {"status": "failed", "coverage": 0.0}
                        print(f"  ✗ {component_name}: Coverage below 95%")

                except subprocess.TimeoutExpired:
                    result["components"][component_name] = {"status": "timeout", "coverage": 0.0}
                    print(f"  ✗ {component_name}: Timeout")
                except Exception as e:
                    result["components"][component_name] = {"status": "error", "coverage": 0.0}
                    print(f"  ✗ {component_name}: Error - {str(e)}")
            else:
                result["components"][component_name] = {"status": "missing", "coverage": 0.0}
                print(f"  ✗ {component_name}: Test directory missing")

        # Calculate overall critical component coverage
        if successful_components > 0:
            result["coverage_achieved"] = total_coverage / len(critical_components)
            if result["coverage_achieved"] >= 95.0:
                result["status"] = "passed"
                print(f"  🟢 Critical Components Coverage: PASSED ({result['coverage_achieved']:.1f}%)")
            else:
                result["status"] = "failed"
                print(f"  🔴 Critical Components Coverage: FAILED ({result['coverage_achieved']:.1f}%)")
        else:
            result["status"] = "failed"
            result["coverage_achieved"] = 0.0
            print("  🔴 Critical Components Coverage: FAILED (No components tested)")

        return result

    def _validate_overall_coverage(self) -> Dict[str, Any]:
        """Validate >=85% overall system coverage."""
        print("\n📊 Gate 4: Overall System Coverage Validation (≥85% Required)")

        result = {
            "gate_id": "overall_coverage",
            "status": "unknown",
            "coverage_target": 85.0,
            "coverage_achieved": 0.0,
            "details": {}
        }

        try:
            coverage_cmd = [
                "python", "-m", "pytest", "tests/",
                "--cov=src",
                "--cov-report=json:overall_coverage.json",
                "--cov-fail-under=85",
                "-q", "--tb=no"
            ]

            coverage_result = subprocess.run(
                coverage_cmd, capture_output=True, text=True, timeout=300
            )

            # Try to read coverage data even if command failed
            try:
                with open("overall_coverage.json", "r") as f:
                    coverage_data = json.load(f)
                    result["coverage_achieved"] = coverage_data.get("totals", {}).get("percent_covered", 0.0)
                    result["details"]["coverage_data"] = coverage_data.get("totals", {})

            except (FileNotFoundError, json.JSONDecodeError):
                result["coverage_achieved"] = 0.0
                result["details"]["coverage_data"] = "unavailable"

            if result["coverage_achieved"] >= 85.0:
                result["status"] = "passed"
                print(f"  🟢 Overall Coverage: PASSED ({result['coverage_achieved']:.1f}%)")
            else:
                result["status"] = "failed"
                print(f"  🔴 Overall Coverage: FAILED ({result['coverage_achieved']:.1f}%)")

        except subprocess.TimeoutExpired:
            result["status"] = "timeout"
            result["details"]["error"] = "Coverage collection timeout"
            print("  ⏰ Overall Coverage: TIMEOUT")
        except Exception as e:
            result["status"] = "error"
            result["details"]["error"] = str(e)
            print(f"  ✗ Overall Coverage: ERROR - {str(e)}")

        return result

    def _validate_theoretical_properties(self) -> Dict[str, Any]:
        """Validate mathematical properties and theoretical correctness."""
        print("\n🔬 Gate 5: Theoretical Property Validation")

        result = {
            "gate_id": "theoretical_validation",
            "status": "unknown",
            "properties_tested": [],
            "properties_passed": [],
            "properties_failed": [],
            "details": {}
        }

        theoretical_test_patterns = [
            "tests/test_physics/",
            "tests/test_analysis/performance/",
            "-k", "stability or lyapunov or convergence"
        ]

        try:
            theory_cmd = [
                "python", "-m", "pytest"
            ] + theoretical_test_patterns + ["-v", "--tb=short"]

            theory_result = subprocess.run(
                theory_cmd, capture_output=True, text=True, timeout=180
            )

            if theory_result.returncode == 0:
                result["status"] = "passed"
                result["properties_tested"] = ["Mathematical stability", "Convergence properties"]
                result["properties_passed"] = result["properties_tested"]
                print("  🟢 Theoretical Validation: PASSED")
            else:
                result["status"] = "failed"
                result["properties_tested"] = ["Mathematical stability", "Convergence properties"]
                result["properties_failed"] = result["properties_tested"]
                print("  🔴 Theoretical Validation: FAILED")

        except subprocess.TimeoutExpired:
            result["status"] = "timeout"
            print("  ⏰ Theoretical Validation: TIMEOUT")
        except Exception as e:
            result["status"] = "error"
            result["details"]["error"] = str(e)
            print(f"  ✗ Theoretical Validation: ERROR - {str(e)}")

        return result

    def _validate_performance_benchmarks(self) -> Dict[str, Any]:
        """Validate performance benchmarks."""
        print("\n⚡ Gate 6: Performance Benchmark Validation")

        result = {
            "gate_id": "performance_validation",
            "status": "unknown",
            "benchmarks_run": 0,
            "benchmarks_passed": 0,
            "details": {}
        }

        try:
            benchmark_cmd = [
                "python", "-m", "pytest", "tests/test_benchmarks/",
                "--benchmark-only",
                "--benchmark-json=benchmark_results.json",
                "-q"
            ]

            benchmark_result = subprocess.run(
                benchmark_cmd, capture_output=True, text=True, timeout=240
            )

            if benchmark_result.returncode == 0:
                result["status"] = "passed"
                result["benchmarks_run"] = 1  # Placeholder
                result["benchmarks_passed"] = 1
                print("  🟢 Performance Benchmarks: PASSED")
            else:
                result["status"] = "failed"
                result["benchmarks_run"] = 1
                result["benchmarks_passed"] = 0
                print("  🔴 Performance Benchmarks: FAILED")

        except subprocess.TimeoutExpired:
            result["status"] = "timeout"
            print("  ⏰ Performance Benchmarks: TIMEOUT")
        except Exception as e:
            result["status"] = "error"
            result["details"]["error"] = str(e)
            print(f"  ✗ Performance Benchmarks: ERROR - {str(e)}")

        return result

    def _calculate_overall_status(self):
        """Calculate overall validation status."""
        gates = self.results["gates"]

        # Critical gates that must pass
        critical_gates = ["infrastructure_health", "safety_critical_coverage"]
        critical_passed = all(
            gates.get(gate, {}).get("status") == "passed"
            for gate in critical_gates
        )

        # Important gates (high weight)
        important_gates = ["critical_components_coverage", "overall_coverage"]
        important_passed = sum(
            1 for gate in important_gates
            if gates.get(gate, {}).get("status") == "passed"
        )

        # Optional gates (informational)
        optional_gates = ["theoretical_validation", "performance_validation"]
        optional_passed = sum(
            1 for gate in optional_gates
            if gates.get(gate, {}).get("status") == "passed"
        )

        if critical_passed and important_passed >= 1:
            if important_passed == 2 and optional_passed >= 1:
                self.results["overall_status"] = "excellent"
            elif important_passed == 2:
                self.results["overall_status"] = "good"
            else:
                self.results["overall_status"] = "acceptable"
        else:
            self.results["overall_status"] = "failed"

    def _generate_recommendations(self):
        """Generate actionable recommendations based on gate results."""
        recommendations = []
        gates = self.results["gates"]

        for gate_id, gate_result in gates.items():
            if gate_result.get("status") == "failed":
                if gate_id == "infrastructure_health":
                    recommendations.append({
                        "priority": "critical",
                        "area": "Infrastructure",
                        "action": "Fix test collection and pytest configuration issues",
                        "commands": ["python -m pytest --collect-only -v"]
                    })
                elif gate_id == "safety_critical_coverage":
                    recommendations.append({
                        "priority": "critical",
                        "area": "Safety-Critical Coverage",
                        "action": "Achieve 100% coverage on safety-critical components",
                        "commands": ["python -m pytest tests/test_controllers/smc/core/ --cov=src/controllers/smc/core --cov-report=html"]
                    })
                elif gate_id == "critical_components_coverage":
                    recommendations.append({
                        "priority": "high",
                        "area": "Critical Components",
                        "action": "Improve coverage on controller factory and optimization modules",
                        "commands": ["python -m pytest tests/test_controllers/factory/ tests/test_optimization/ --cov=src/controllers/factory --cov=src/optimizer --cov-report=html"]
                    })
                elif gate_id == "overall_coverage":
                    recommendations.append({
                        "priority": "medium",
                        "area": "Overall Coverage",
                        "action": "Add tests to reach 85% overall coverage target",
                        "commands": ["python -m pytest tests/ --cov=src --cov-report=html --cov-report=missing"]
                    })

        self.results["recommendations"] = recommendations

    def save_results(self, filename: str = "quality_gate_results.json"):
        """Save validation results to file."""
        output_path = self.base_path / "validation" / filename
        output_path.parent.mkdir(exist_ok=True)

        with open(output_path, "w") as f:
            json.dump(self.results, f, indent=2)

        print(f"\n📄 Results saved to: {output_path}")
        return output_path


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(description="Quality Gate Validation Framework")
    parser.add_argument("--gate", choices=["all", "infrastructure", "safety", "critical", "overall", "theoretical", "performance"],
                       default="all", help="Specific gate to validate")
    parser.add_argument("--output", default="quality_gate_results.json", help="Output filename")
    parser.add_argument("--base-path", default=".", help="Base project path")

    args = parser.parse_args()

    validator = QualityGateValidator(args.base_path)

    if args.gate == "all":
        results = validator.run_comprehensive_validation()
    else:
        # Individual gate validation (simplified for this version)
        results = validator.run_comprehensive_validation()

    # Save results
    output_path = validator.save_results(args.output)

    # Print summary
    print(f"\n🔵 Ultimate Orchestrator Quality Gate Summary:")
    print(f"Overall Status: {results['overall_status'].upper()}")

    for gate_id, gate_result in results["gates"].items():
        status_emoji = "🟢" if gate_result["status"] == "passed" else "🔴" if gate_result["status"] == "failed" else "⚠️"
        print(f"{status_emoji} {gate_id}: {gate_result['status']}")

    if results["recommendations"]:
        print(f"\n📋 Recommendations ({len(results['recommendations'])}):")
        for i, rec in enumerate(results["recommendations"][:3], 1):
            print(f"{i}. [{rec['priority'].upper()}] {rec['area']}: {rec['action']}")

    # Exit code based on overall status
    if results["overall_status"] in ["excellent", "good", "acceptable"]:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()