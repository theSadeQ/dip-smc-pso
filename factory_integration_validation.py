#======================================================================================\\\
#========================= factory_integration_validation.py ==========================\\\
#======================================================================================\\\

"""
Comprehensive Factory Integration Validation Script.

Validates the complete controller factory integration including:
- Controller creation for all types
- PSO integration compatibility
- Parameter bounds validation
- Stability constraints verification
- Error handling robustness
- Performance benchmarking
"""

import time
import traceback
import numpy as np
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass

# Import factory components
from src.controllers.factory import (
    create_controller, list_available_controllers, get_default_gains,
    SMCType, create_pso_controller_factory, get_gain_bounds_for_pso,
    CONTROLLER_REGISTRY
)
from src.config import load_config


@dataclass
class ValidationResult:
    """Results of a validation test."""
    test_name: str
    passed: bool
    message: str
    execution_time: float = 0.0
    details: Dict[str, Any] = None


class FactoryIntegrationValidator:
    """Comprehensive factory integration validation."""

    def __init__(self):
        self.results: List[ValidationResult] = []
        self.config = None

    def run_all_validations(self) -> Dict[str, Any]:
        """Run all validation tests."""
        print("Controller Factory Integration Validation")
        print("=" * 60)

        # Load configuration
        try:
            self.config = load_config('config.yaml')
            self._add_result("Configuration Loading", True, "Configuration loaded successfully")
        except Exception as e:
            self._add_result("Configuration Loading", False, f"Failed: {e}")
            return self._generate_report()

        # Run validation categories
        self._validate_controller_creation()
        self._validate_pso_integration()
        self._validate_parameter_bounds()
        self._validate_stability_constraints()
        self._validate_error_handling()
        self._validate_performance()

        return self._generate_report()

    def _add_result(self, test_name: str, passed: bool, message: str,
                   execution_time: float = 0.0, details: Dict[str, Any] = None):
        """Add a validation result."""
        result = ValidationResult(
            test_name=test_name,
            passed=passed,
            message=message,
            execution_time=execution_time,
            details=details or {}
        )
        self.results.append(result)

        # Print result
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} {test_name}: {message}")
        if execution_time > 0:
            print(f"   ⏱️ Execution time: {execution_time:.3f}s")

    def _validate_controller_creation(self):
        """Test controller creation for all types."""
        print("\n📋 Testing Controller Creation")
        print("-" * 30)

        available_controllers = list_available_controllers()
        registry_controllers = list(CONTROLLER_REGISTRY.keys())

        # Test available vs registry consistency
        missing_from_available = set(registry_controllers) - set(available_controllers) - {'mpc_controller'}
        if missing_from_available:
            self._add_result(
                "Registry Consistency",
                False,
                f"Controllers in registry but not available: {missing_from_available}"
            )
        else:
            self._add_result("Registry Consistency", True, "All registry controllers are available")

        # Test individual controller creation
        creation_times = {}
        for controller_type in available_controllers:
            start_time = time.perf_counter()
            try:
                controller = create_controller(controller_type)
                execution_time = time.perf_counter() - start_time
                creation_times[controller_type] = execution_time

                # Validate controller interface
                assert hasattr(controller, 'gains'), f"Controller {controller_type} missing gains property"
                assert hasattr(controller, 'compute_control'), f"Controller {controller_type} missing compute_control method"
                assert hasattr(controller, 'reset'), f"Controller {controller_type} missing reset method"

                # Check gains count
                expected_count = CONTROLLER_REGISTRY[controller_type]['gain_count']
                actual_count = len(controller.gains)
                assert actual_count == expected_count, f"Expected {expected_count} gains, got {actual_count}"

                self._add_result(
                    f"Create {controller_type}",
                    True,
                    f"Created with {len(controller.gains)} gains",
                    execution_time,
                    {"gains": controller.gains, "type": type(controller).__name__}
                )

            except Exception as e:
                execution_time = time.perf_counter() - start_time
                self._add_result(
                    f"Create {controller_type}",
                    False,
                    f"Failed: {str(e)[:100]}",
                    execution_time
                )

        # Performance summary
        if creation_times:
            avg_time = np.mean(list(creation_times.values()))
            max_time = max(creation_times.values())
            self._add_result(
                "Creation Performance",
                max_time < 0.1,  # Should be fast
                f"Avg: {avg_time:.3f}s, Max: {max_time:.3f}s",
                details=creation_times
            )

    def _validate_pso_integration(self):
        """Test PSO integration compatibility."""
        print("\n🎯 Testing PSO Integration")
        print("-" * 30)

        smc_types = [SMCType.CLASSICAL, SMCType.ADAPTIVE, SMCType.SUPER_TWISTING, SMCType.HYBRID]

        for smc_type in smc_types:
            start_time = time.perf_counter()
            try:
                # Test PSO bounds retrieval
                lower_bounds, upper_bounds = get_gain_bounds_for_pso(smc_type)
                assert len(lower_bounds) == len(upper_bounds), "Bounds length mismatch"
                assert all(l < u for l, u in zip(lower_bounds, upper_bounds)), "Invalid bounds: lower >= upper"

                # Test PSO factory creation
                controller_factory = create_pso_controller_factory(smc_type, self.config)

                # Check required PSO attributes
                assert hasattr(controller_factory, 'n_gains'), "Missing n_gains attribute"
                assert hasattr(controller_factory, 'controller_type'), "Missing controller_type attribute"
                assert hasattr(controller_factory, 'max_force'), "Missing max_force attribute"

                # Test valid gains creation
                test_gains = self._generate_valid_test_gains(smc_type, lower_bounds, upper_bounds)
                test_controller = controller_factory(test_gains)

                # Test PSO wrapper interface
                assert hasattr(test_controller, 'compute_control'), "PSO wrapper missing compute_control"
                assert hasattr(test_controller, 'validate_gains'), "PSO wrapper missing validate_gains"

                execution_time = time.perf_counter() - start_time
                self._add_result(
                    f"PSO {smc_type.value}",
                    True,
                    f"Full PSO integration working",
                    execution_time,
                    {
                        "n_gains": controller_factory.n_gains,
                        "bounds_range": [len(lower_bounds), len(upper_bounds)],
                        "test_gains": test_gains
                    }
                )

            except Exception as e:
                execution_time = time.perf_counter() - start_time
                self._add_result(
                    f"PSO {smc_type.value}",
                    False,
                    f"Failed: {str(e)[:100]}",
                    execution_time
                )

    def _generate_valid_test_gains(self, smc_type: SMCType, lower_bounds: List[float],
                                  upper_bounds: List[float]) -> List[float]:
        """Generate valid test gains for a controller type."""
        # Use 70% of range for safer testing
        test_gains = [l + 0.7 * (u - l) for l, u in zip(lower_bounds, upper_bounds)]

        # Special handling for STA-SMC K1 > K2 constraint
        if smc_type == SMCType.SUPER_TWISTING and len(test_gains) >= 2:
            # Ensure K1 > K2 with margin
            test_gains[0] = upper_bounds[0] * 0.8  # K1
            test_gains[1] = upper_bounds[1] * 0.6  # K2, ensure K1 > K2

        return test_gains

    def _validate_parameter_bounds(self):
        """Test parameter bounds validation."""
        print("\n📏 Testing Parameter Bounds")
        print("-" * 30)

        for controller_type in list_available_controllers():
            try:
                # Test default gains
                default_gains = get_default_gains(controller_type)
                controller = create_controller(controller_type, gains=default_gains)

                self._add_result(
                    f"Default Gains {controller_type}",
                    True,
                    f"Default gains valid: {default_gains}"
                )

                # Test boundary conditions
                registry_info = CONTROLLER_REGISTRY[controller_type]
                n_gains = registry_info['gain_count']

                # Test minimal positive gains
                minimal_gains = [0.1] * n_gains
                if controller_type == 'sta_smc' and len(minimal_gains) >= 2:
                    minimal_gains[0] = 0.2  # K1 > K2
                    minimal_gains[1] = 0.1  # K2

                try:
                    controller = create_controller(controller_type, gains=minimal_gains)
                    self._add_result(
                        f"Minimal Gains {controller_type}",
                        True,
                        f"Minimal positive gains accepted: {minimal_gains}"
                    )
                except Exception as e:
                    self._add_result(
                        f"Minimal Gains {controller_type}",
                        False,
                        f"Minimal gains rejected: {str(e)[:80]}"
                    )

            except Exception as e:
                self._add_result(
                    f"Bounds {controller_type}",
                    False,
                    f"Bounds validation failed: {str(e)[:100]}"
                )

    def _validate_stability_constraints(self):
        """Test stability constraint enforcement."""
        print("\n⚖️ Testing Stability Constraints")
        print("-" * 30)

        # Test STA-SMC K1 > K2 constraint
        try:
            invalid_gains = [5.0, 10.0, 1.0, 1.0, 1.0, 1.0]  # K1 < K2, should fail
            controller = create_controller('sta_smc', gains=invalid_gains)
            self._add_result(
                "STA-SMC K1 > K2 Constraint",
                False,
                "Invalid gains K1 <= K2 were accepted (should be rejected)"
            )
        except Exception as e:
            if "K1 > K2" in str(e):
                self._add_result(
                    "STA-SMC K1 > K2 Constraint",
                    True,
                    "K1 <= K2 properly rejected"
                )
            else:
                self._add_result(
                    "STA-SMC K1 > K2 Constraint",
                    False,
                    f"Unexpected error: {str(e)[:80]}"
                )

        # Test positive gains requirement
        try:
            negative_gains = [-1.0, 5.0, 1.0, 1.0, 1.0, 1.0]
            controller = create_controller('classical_smc', gains=negative_gains)
            self._add_result(
                "Positive Gains Constraint",
                False,
                "Negative gains were accepted (should be rejected)"
            )
        except Exception as e:
            if "positive" in str(e).lower():
                self._add_result(
                    "Positive Gains Constraint",
                    True,
                    "Negative gains properly rejected"
                )
            else:
                self._add_result(
                    "Positive Gains Constraint",
                    False,
                    f"Unexpected error: {str(e)[:80]}"
                )

        # Test hybrid controller surface gains validation
        try:
            # Test with wrong number of gains
            invalid_hybrid_gains = [1.0, 2.0, 3.0]  # Should be 4 gains
            controller = create_controller('hybrid_adaptive_sta_smc', gains=invalid_hybrid_gains)
            self._add_result(
                "Hybrid Gains Count",
                False,
                "Wrong number of gains accepted (should be rejected)"
            )
        except Exception as e:
            if "4" in str(e) or "exactly" in str(e).lower():
                self._add_result(
                    "Hybrid Gains Count",
                    True,
                    "Invalid gain count properly rejected"
                )
            else:
                self._add_result(
                    "Hybrid Gains Count",
                    False,
                    f"Unexpected error: {str(e)[:80]}"
                )

    def _validate_error_handling(self):
        """Test error handling robustness."""
        print("\n🛡️ Testing Error Handling")
        print("-" * 30)

        # Test invalid controller type
        try:
            controller = create_controller('nonexistent_controller')
            self._add_result(
                "Invalid Controller Type",
                False,
                "Invalid controller type was accepted"
            )
        except ValueError as e:
            if "Unknown controller type" in str(e):
                self._add_result(
                    "Invalid Controller Type",
                    True,
                    "Invalid controller type properly rejected"
                )
            else:
                self._add_result(
                    "Invalid Controller Type",
                    False,
                    f"Unexpected error type: {str(e)[:80]}"
                )
        except Exception as e:
            self._add_result(
                "Invalid Controller Type",
                False,
                f"Unexpected error: {str(e)[:80]}"
            )

        # Test with None gains
        try:
            controller = create_controller('classical_smc', gains=None)
            self._add_result(
                "None Gains Handling",
                True,
                "None gains handled gracefully (uses defaults)"
            )
        except Exception as e:
            self._add_result(
                "None Gains Handling",
                False,
                f"None gains caused error: {str(e)[:80]}"
            )

        # Test with empty gains list
        try:
            controller = create_controller('classical_smc', gains=[])
            self._add_result(
                "Empty Gains Handling",
                False,
                "Empty gains list was accepted"
            )
        except Exception as e:
            self._add_result(
                "Empty Gains Handling",
                True,
                "Empty gains list properly rejected"
            )

    def _validate_performance(self):
        """Test performance characteristics."""
        print("\n⚡ Testing Performance")
        print("-" * 30)

        # Batch controller creation test
        n_iterations = 10
        controller_types = list_available_controllers()

        start_time = time.perf_counter()
        successful_creations = 0

        for _ in range(n_iterations):
            for controller_type in controller_types:
                try:
                    controller = create_controller(controller_type)
                    successful_creations += 1
                except Exception:
                    pass

        total_time = time.perf_counter() - start_time
        avg_time_per_creation = total_time / successful_creations if successful_creations > 0 else float('inf')

        # Performance thresholds
        fast_creation = avg_time_per_creation < 0.01  # 10ms per controller
        reasonable_creation = avg_time_per_creation < 0.1   # 100ms per controller

        if fast_creation:
            performance_level = "Excellent"
        elif reasonable_creation:
            performance_level = "Good"
        else:
            performance_level = "Needs Improvement"

        self._add_result(
            "Creation Performance",
            reasonable_creation,
            f"{performance_level}: {avg_time_per_creation:.4f}s avg ({successful_creations} controllers)",
            total_time,
            {
                "total_time": total_time,
                "successful_creations": successful_creations,
                "avg_time_per_creation": avg_time_per_creation,
                "performance_level": performance_level
            }
        )

    def _generate_report(self) -> Dict[str, Any]:
        """Generate comprehensive validation report."""
        passed_tests = [r for r in self.results if r.passed]
        failed_tests = [r for r in self.results if not r.passed]

        pass_rate = len(passed_tests) / len(self.results) * 100 if self.results else 0
        total_execution_time = sum(r.execution_time for r in self.results)

        print("\n" + "=" * 60)
        print("📊 VALIDATION SUMMARY")
        print("=" * 60)
        print(f"Total Tests: {len(self.results)}")
        print(f"Passed: {len(passed_tests)} ({pass_rate:.1f}%)")
        print(f"Failed: {len(failed_tests)}")
        print(f"Total Execution Time: {total_execution_time:.3f}s")

        if failed_tests:
            print("\n❌ FAILED TESTS:")
            for test in failed_tests:
                print(f"  - {test.test_name}: {test.message}")

        # Determine overall status
        if pass_rate >= 95:
            overall_status = "EXCELLENT"
        elif pass_rate >= 85:
            overall_status = "GOOD"
        elif pass_rate >= 70:
            overall_status = "ACCEPTABLE"
        else:
            overall_status = "NEEDS_IMPROVEMENT"

        print(f"\n🎯 OVERALL STATUS: {overall_status}")
        print("=" * 60)

        return {
            "overall_status": overall_status,
            "pass_rate": pass_rate,
            "total_tests": len(self.results),
            "passed_tests": len(passed_tests),
            "failed_tests": len(failed_tests),
            "total_execution_time": total_execution_time,
            "results": [
                {
                    "test_name": r.test_name,
                    "passed": r.passed,
                    "message": r.message,
                    "execution_time": r.execution_time,
                    "details": r.details
                }
                for r in self.results
            ],
            "failed_test_names": [r.test_name for r in failed_tests]
        }


def main():
    """Run factory integration validation."""
    validator = FactoryIntegrationValidator()

    try:
        report = validator.run_all_validations()

        # Save detailed report
        import json
        with open('factory_validation_report.json', 'w') as f:
            json.dump(report, f, indent=2)

        print(f"\n📝 Detailed report saved to: factory_validation_report.json")

        # Return exit code based on results
        return 0 if report["overall_status"] in ["EXCELLENT", "GOOD"] else 1

    except Exception as e:
        print(f"\n💥 Validation failed with error: {e}")
        traceback.print_exc()
        return 2


if __name__ == "__main__":
    exit(main())